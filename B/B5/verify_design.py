from pathlib import Path
import sys,argparse,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def accepted_image(evidence):
    record=json.loads((ROOT/evidence/'run.json').read_text());assert record['status']=='PASS'
    files=[r for r in record['inputs'] if r['path'].endswith('.bin')];assert len(files)==1
    row=files[0];p=Path(row['path']);assert sha(p)==row['sha256'];return p,row['sha256']

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=['rtl','netlist'],required=True);parser.add_argument('--program',default='all',choices=['all','hello','hazards','fence-prefetch','microbench','rtthread']);parser.add_argument('--fault-reset',action='store_true');parser.add_argument('--netlist',default='B/B5/netlist/ysyx_00000000.v');parser.add_argument('--fast-memory',action='store_true');args=parser.parse_args()
    assert not args.fault_reset or args.mode=='rtl'
    model=ROOT/'B/models/nangate45/sim/cells.v';assert json.loads((ROOT/'reports/B5_cell_models.json').read_text())['status']=='PASS'
    tb=ROOT/'B/B5/cpu_four_state_tb.sv';suite=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite');iv=suite/'bin/iverilog';vvp=suite/'bin/vvp';guard=ROOT/'B/runtime/budget_exec.py'
    label=args.mode+('-bad-reset' if args.fault_reset else '');folder=WORK/'b5'/label;folder.mkdir(parents=True,exist_ok=True);executable=folder/'cpu.vvp'
    if args.mode=='rtl':
        sources=[*sorted((ROOT/'B/soc/rtl').glob('*.sv')),*sorted((ROOT/'B/soc/rtl').glob('*.v'))]
        if args.fault_reset:
            original=ROOT/'B/soc/rtl/ysyx_00000000_pipe.sv';text=original.read_text();assert text.count('fetch_pc<=RESET_PC;')==1
            broken=folder/'ysyx_00000000_pipe.sv';broken.write_text(text.replace('fetch_pc<=RESET_PC;','/* injected omission of fetch-PC reset */'))
            sources=[broken if p==original else p for p in sources]
        defines=['-DSYNTHESIS',"-DC5_RESET_PC=32'h80000000",'-DB_PIPELINE=1','-DB_FORWARD=1','-DB_PREDICT=2','-DB_FETCH_PIPELINED=1','-DB_ICACHE_ENABLE=1','-DB_ICACHE_LINES=4','-DB_ICACHE_WORDS=8','-DB_ICACHE_WAYS=2','-DB_ICACHE_BURST=1']
    else:
        netlist=(ROOT/args.netlist).resolve();assert netlist.is_relative_to(ROOT.resolve()) and netlist.is_file();sources=[netlist,model];defines=[]
    budget=ROOT/'artifacts/B5/design'/label/'build-budget.json'
    run('B5/design/'+label+'/build',['python3',guard,'--report',budget,'--',iv,'-g2012','-s','cpu_four_state_tb','-o',executable,*defines,tb,*sources],inputs=[iv,tb,*sources],outputs=[executable,budget],timeout=300,resume=True)
    baseline=json.loads((ROOT/'reports/B_standalone_pipeline-final.json').read_text())['runs']
    pipeline=json.loads((ROOT/'reports/B4_functional_pipeline-final.json').read_text())['runs']
    jobs=['hello'] if args.fault_reset else ['hello','hazards','fence-prefetch','microbench','rtthread'] if args.program=='all' else [args.program];rows=[]
    for name in jobs:
        row=next(r for r in (pipeline if name in ('hazards','fence-prefetch') else baseline) if r['name']==name)
        image,expected_hash=accepted_image(row['evidence']);data=image.read_bytes();words=(len(data)+3)//4;hexfile=folder/(name+'.hex')
        lines=[]
        for offset in range(0,len(data),4):
            chunk=data[offset:offset+4];lines.append('xx'*(4-len(chunk))+''.join(f'{b:02x}' for b in chunk[::-1]))
        hexfile.write_text('\n'.join(lines)+'\n')
        tag='B5/design/'+label+'/'+name;out=ROOT/'artifacts'/tag;out.mkdir(parents=True,exist_ok=True);budget=out/'budget.json'
        maximum=20000000 if name in ('microbench','rtthread') else 200000
        text,err,record=run(tag,['python3',guard,'--kind','simulation','--report',budget,'--',vvp,executable,'+IMAGE='+str(hexfile),'+WORDS='+str(words),'+MAX_CYCLES='+str(maximum),'+FAST='+str(int(args.fast_memory))],inputs=[vvp,executable,image,hexfile],outputs=[budget],expected=(1 if args.fault_reset else 0,),timeout=14400 if args.mode=='netlist' else 900)
        if args.fault_reset:assert 'AXI_AR_UNKNOWN' in text+err
        else:
            assert 'B5_PROGRAM_PASS' in text and 'B5_CYCLE_LIMIT' not in text and 'RESOURCE_LIMIT' not in text
            marker={'hello':'B_FAST_HELLO_PASS','microbench':'MicroBench PASS','rtthread':'C5_RTTHREAD_PASS'}.get(name)
            if marker:assert marker in text
            if name=='microbench':assert text.count('Passed.')==10 and 'insufficient memory' not in text
            if name=='rtthread':assert 'C5_CONTEXT_PASS a=12 b=12' in text
        match=re.search(r'B5_PROGRAM_PASS cycles=(\d+) reads=(\d+) beats=(\d+) writes=(\d+) pages=(\d+)',text)
        net_hash=sha(sources[0]) if args.mode=='netlist' else None
        rows.append({'name':name,'status':'PASS_MISSING_RESET_REJECTED' if args.fault_reset else 'PASS','mode':args.mode,'fast_memory':args.fast_memory,'executable_sha256':sha(executable),'netlist_sha256':net_hash,'image_sha256':expected_hash,'hex_sha256':sha(hexfile),'wall_seconds':record['elapsed_seconds'],'counts':dict(zip(['cycles','read_transactions','read_beats','write_transactions','resident_pages'],map(int,match.groups()))) if match else None,'evidence':'artifacts/'+tag})
        import fcntl
        with (WORK/'b5-report.lock').open('a+') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            path=ROOT/('reports/B5_'+label+'.json');prior_doc=json.loads(path.read_text()) if path.exists() else {};prior=prior_doc.get('runs',[])
            if prior_doc and prior_doc.get('netlist_sha256')!=net_hash:
                dump(ROOT/'artifacts/B5/design'/label/'report-history'/(str(time.time_ns())+'.json'),prior_doc);prior=[]
            merged=[r for r in prior if r['name'] not in {x['name'] for x in rows}]+rows
            dump(path,{'status':'PASS_COMPLETED_RUNS','mode':args.mode,'fault_reset':args.fault_reset,'executable_sha256':sha(executable),'netlist_sha256':net_hash,'runs':merged,'scope':'Icarus four-state execution at the public AXI boundary. Unwritten RAM and non-reset cache data remain X; control/address and active write-byte unknowns are rejected. Fixed-reset mapped CPU uses a two-instruction Flash trampoline to the program at0x80000000. Sparse model covers128MiB addresses with8MiB resident pages, and actual page usage is recorded. Fast-memory runs remove artificial bus wait cycles while preserving the full program, four-state memory, and every checker. Zero-delay functional cell simulation, no SDF/timing-signoff claim.'})
    print('B5_DESIGN_PASS',label,','.join(jobs))

if __name__=='__main__':main()

from pathlib import Path
import sys,argparse,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--variant',required=True);parser.add_argument('--size',choices=['test','train'],default='test');parser.add_argument('--trace',action='store_true');parser.add_argument('--frequency-mhz',type=int,default=400);parser.add_argument('--padding',type=int,default=0);args=parser.parse_args()
    assert 100<=args.frequency_mhz<=2000
    revision=subprocess.check_output(['/mnt/d/Git/Git/cmd/git.exe','-C','/workspace/projects/ysyx_f_to_b','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    assert 0<=args.padding<=4096 and args.padding%4==0
    base=WORK/'soc/workbench';am=base/'abstract-machine';app=base/'microbench';arch='riscv32e-ysyxsoc-sdram128-p'+str(args.frequency_mhz)+('-pad'+str(args.padding) if args.padding else '')
    for name in ['start.S','trm.c','ioe.c','lshrdi3.S','ps2.h']:
        shutil.copyfile(ROOT/'B/soc/am'/name,am/'am/src/riscv/ysyxsoc'/name)
    for name in ['cte.c','trap.S']:shutil.copyfile(ROOT/'B/B1'/name,am/'am/src/riscv/ysyxsoc'/name)
    shutil.copyfile(ROOT/'B/soc/am/ysyxsoc.mk',am/'scripts/platform/ysyxsoc.mk')
    link=am/'scripts/ysyxsoc-code-sdram128.ld';arch_text='SOC_CLOCK_MHZ := '+str(args.frequency_mhz)+'\ninclude $(AM_HOME)/scripts/riscv32e-ysyxsoc-sdram128.mk\n'
    if args.padding:
        text=link.read_text();needle='__text_start = .;';assert text.count(needle)==1
        target=am/'scripts'/('ysyxsoc-code-sdram128-pad'+str(args.padding)+'.ld');target.write_text(text.replace(needle,needle+' . += '+str(args.padding)+';'))
        arch_text+='LDSCRIPTS := $(filter-out $(AM_HOME)/scripts/ysyxsoc-code-sdram128.ld,$(LDSCRIPTS)) $(AM_HOME)/scripts/'+target.name+'\n';link=target
    (am/'scripts'/(arch+'.mk')).write_text(arch_text)
    suffix='-pad'+str(args.padding) if args.padding else ''
    image=app/'build'/('microbench-'+arch+'.bin');elf=image.with_suffix('.elf');tag='B3/perf/'+args.variant+'-'+args.size+suffix
    inputs=[p for p in sorted(app.rglob('*')) if p.is_file() and 'build' not in p.relative_to(app).parts]+[*sorted((am/'am/src/riscv/ysyxsoc').glob('*')),link,am/'scripts'/(arch+'.mk')]
    run('B3/images/'+args.size,['make','-j4','ARCH='+arch,'mainargs='+args.size,'insert-arg'],cwd=app,env={'AM_HOME':str(am)},inputs=inputs,outputs=[image,elf],timeout=240)
    frozen=WORK/'b3/images'/str(args.frequency_mhz)/(args.size+suffix);frozen.mkdir(parents=True,exist_ok=True);shutil.copyfile(image,frozen/'image.bin');shutil.copyfile(elf,frozen/'image.elf');image=frozen/'image.bin';elf=frozen/'image.elf'
    build=next(r for r in json.loads((ROOT/'reports/B_soc_soc_build.json').read_text())['variants'] if r['variant']==args.variant);exe=Path(build['executable']);assert sha(exe)==build['sha256'];ref=WORK/'nemu-ref/build/riscv32-nemu-interpreter-so'
    out=ROOT/'artifacts'/tag;out.mkdir(parents=True,exist_ok=True);report=out/'simulation.json';budget=out/'budget.json';trace=out/'retired.bin'
    command=['python3',ROOT/'B/runtime/budget_exec.py','--kind','simulation','--report',budget,'--',exe,'--flash',image,'--ref',ref,'--report',report,'--max-cycles',str(200000000 if args.size=='test' else 40000000000),'--progress-cycles','100000000',*(['--perf-trace',trace] if args.trace else [])]
    execution_record=out/'run/run.json';before_run_hash=sha(execution_record) if execution_record.exists() else None
    run(tag+'/run',command,inputs=[exe,ref,image,elf],outputs=[report,budget,*([trace] if args.trace else [])],timeout=240 if args.size=='test' else 43200,resume=True)
    execution_hash=sha(execution_record);reused=before_run_hash==execution_hash
    data=json.loads(report.read_text());p=data['performance'];assert data['result']=='GOOD_TRAP' and data['diff_checked']+data['device_sync_checked']==data['instructions']
    assert sum(p['class_counts'])==data['instructions'] and sum(p['class_cycles'])==p['core_cycles'] and sum(p['state_cycles'])==p['core_cycles']
    if build.get('pipeline'):
        assert p['ifu_responses']>=data['instructions'] and 0<=p['ifu_requests']-p['ifu_responses']<=1
        events=p['pipeline_events'];assert events[8]+events[10]==data['instructions'] and events[9]+events[10]==data['instructions']
    else:assert p['ifu_responses']==data['instructions']
    assert p['lsu_requests']==p['lsu_responses']==sum(p['class_counts'][1:3])
    assert p['exu_completions']+p['lsu_responses']==data['instructions']
    assert sum(p['ifu_absence'])+p['ifu_responses']==p['core_cycles']
    if 'fetch_latency_hit_miss_bypass' in p:
        assert sum(p['fetch_latency_hit_miss_bypass'])==p['ifu_latency_sum']
        assert sum(p['data_counts'])==p['lsu_responses'] and sum(p['data_latency'])==p['lsu_latency_sum']
    if args.trace:assert trace.stat().st_size==20*data['instructions']
    uart=bytes.fromhex(data['uart']['hex']).decode('ascii');assert 'PASS' in uart and 'FAIL' not in uart,uart
    prior_path=out/'performance-row.json';prior=json.loads(prior_path.read_text()) if prior_path.exists() else None
    measurement_revision=revision
    if reused and prior:
        assert prior['simulation']==data and prior['image_sha256']==sha(image)
        measurement_revision=prior['git_commit']
    elif reused:measurement_revision=None
    row={'variant':args.variant,'size':args.size,'padding':args.padding,'status':'PASS','model_frequency_mhz':args.frequency_mhz,'git_commit':measurement_revision,'invocation_git_commit':revision,'reused_saved_execution':reused,'run_record_sha256':execution_hash,'source_inputs':build['inputs'],'image':str(image),'elf':str(elf),'image_sha256':sha(image),'elf_sha256':sha(elf),'simulation':data,'uart':uart,'ipc':data['instructions']/p['core_cycles'],'evidence':'artifacts/'+tag,'trace':str(trace) if args.trace else None,'trace_format':'little-endian20-byte record: pc,inst,next_pc,data_address,memory_flags'}
    dump(out/'performance-row.json',row)
    import fcntl
    with (WORK/'performance-report.lock').open('a+') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        report=ROOT/'reports/B3_performance.json';rows=json.loads(report.read_text())['runs'] if report.exists() else [];rows=[r for r in rows if (r['variant'],r['size'],r.get('padding',0))!=(args.variant,args.size,args.padding)]+[row];dump(report,{'status':'PASS_COMPLETED_RUNS','runs':rows})
    print('B3_PERF_PASS',args.variant,args.size,data['cycles'],data['instructions'],row['ipc'],flush=True)

if __name__=='__main__':main()

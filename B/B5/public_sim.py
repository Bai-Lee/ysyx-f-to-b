"""Run a caller-supplied BIN through the exported RTL or a supplied netlist."""
from pathlib import Path
import sys,argparse,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--image',required=True);parser.add_argument('--netlist')
    parser.add_argument('--cells',default=str(ROOT/'B/models/nangate45/sim/cells.v'))
    parser.add_argument('--max-cycles',type=int,default=20000000)
    args=parser.parse_args();image=Path(args.image).resolve();assert image.is_file()
    data=image.read_bytes();assert 0<len(data)<=4*1048576
    mode='netlist' if args.netlist else 'rtl';stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    folder=WORK/'b5/public'/mode/stamp;folder.mkdir(parents=True)
    hexfile=folder/'image.hex';lines=[]
    for offset in range(0,len(data),4):
        part=data[offset:offset+4];lines.append('xx'*(4-len(part))+''.join(f'{x:02x}' for x in part[::-1]))
    hexfile.write_text('\n'.join(lines)+'\n');exe=folder/'sim.vvp'
    suite=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite/bin')
    tb=ROOT/'B/B5/cpu_four_state_tb.sv'
    sources=[Path(args.netlist).resolve(),Path(args.cells).resolve()] if args.netlist else [ROOT/'B/soc/build/ysyx_00000000.sv']
    assert all(p.is_file() for p in sources)
    tag='B5/public/'+mode+'/'+stamp;budget=ROOT/'artifacts'/tag/'budget.json'
    run(tag+'/build',[suite/'iverilog','-g2012','-s','cpu_four_state_tb','-o',exe,tb,*sources],inputs=[suite/'iverilog',tb,*sources],outputs=[exe],timeout=180)
    output,errors,record=run(tag+'/run',['python3',ROOT/'B/runtime/budget_exec.py','--kind','simulation','--report',budget,'--',suite/'vvp',exe,'+IMAGE='+str(hexfile),'+WORDS='+str(len(lines)),'+MAX_CYCLES='+str(args.max_cycles),'+FAST=0'],inputs=[suite/'vvp',exe,image,hexfile],outputs=[budget],timeout=14400)
    assert 'B5_PROGRAM_PASS' in output and 'B5_BAD_TRAP' not in output
    print(output)
    report=ROOT/'reports/B5_public_entrypoints.json';prior=json.loads(report.read_text()) if report.exists() else {'runs':[]}
    prior['runs'].append({'mode':mode,'status':'PASS','image_sha256':sha(image),'source_sha256':[sha(p) for p in sources],'evidence':'artifacts/'+tag,'elapsed_seconds':record['elapsed_seconds']})
    prior['status']='PASS_COMPLETED_RUNS';prior['scope']='Local public make contract, not official CI. Programs use the documented standalone AM ABI at0x80000000, reached from the fixed Flash reset using a two-instruction trampoline.'
    dump(report,prior)

if __name__=='__main__':main()

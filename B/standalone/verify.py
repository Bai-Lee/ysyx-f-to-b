from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'B1'))
from common import *
from verify import compile_app,rt_build

def main():
    p=argparse.ArgumentParser();p.add_argument('--label',default='multicycle-cache128');p.add_argument('--size',choices=['test','train'],default='test');p.add_argument('--only',choices=['hello','microbench','rtthread']);a=p.parse_args()
    base=WORK/'soc/workbench';am=base/'abstract-machine';arch='riscv32e-bnpc';rows=[]
    b=next(x for x in json.loads((ROOT/'reports/B_standalone_builds.json').read_text())['variants'] if x['label']==a.label);exe=Path(b['executable']);assert sha(exe)==b['sha256'];ref=WORK/'fast-nemu-ref/build/riscv32-nemu-interpreter-so'
    jobs=[a.only] if a.only else ['hello','microbench','rtthread']
    for name in jobs:
        if name=='hello':image,elf=compile_app('fast-hello',arch,{'main.c':'#include <am.h>\n#include <klib.h>\nint main(const char*a){(void)a;printf("B_FAST_HELLO_PASS\\n");return 0;}\n'},am)
        elif name=='rtthread':image,elf=rt_build(arch,am)
        else:
            app=base/'microbench';image=app/'build'/('microbench-'+arch+'.bin');elf=image.with_suffix('.elf')
            inputs=[p for p in sorted(app.rglob('*')) if p.is_file() and 'build' not in p.relative_to(app).parts]+[am/'scripts/bnpc.ld',*sorted((am/'am/src/riscv/bnpc').glob('*'))]
            run('B/standalone/images/microbench-'+a.size,['make','-j4','ARCH='+arch,'mainargs='+a.size,'insert-arg'],cwd=app,env={'AM_HOME':str(am)},inputs=inputs,outputs=[image,elf],timeout=240,resume=True)
        label=a.label+'-'+name+'-'+a.size;out=ROOT/'artifacts/B/standalone/validation'/label;out.mkdir(parents=True,exist_ok=True);report=out/'simulation.json';budget=out/'budget.json'
        run('B/standalone/validation/'+label,['python3',ROOT/'B/runtime/budget_exec.py','--report',budget,'--',exe,'--image',image,'--ref',ref,'--report',report,'--max-cycles','4000000000','--seed','0x2607b309'],inputs=[exe,ref,image,elf],outputs=[report,budget],timeout=600 if a.size=='test' else 7200,expected=(1 if b['mutant'] else 0,))
        result=json.loads(report.read_text());assert result['diff_enabled']
        if b['mutant']:assert result['result']=='DIFF_FAIL'
        else:
            assert result['result']=='GOOD_TRAP' and result['diff_checked']+result['device_sync_checked']==result['instructions']
            text=bytes.fromhex(result['uart_hex']).decode('ascii');assert {'hello':'B_FAST_HELLO_PASS','microbench':'MicroBench PASS','rtthread':'C5_RTTHREAD_PASS'}[name] in text
        rows.append({'name':name,'size':a.size,'status':'PASS','simulation':result,'image':str(image),'elf':str(elf),'image_sha256':sha(image),'elf_sha256':sha(elf),'evidence':'artifacts/B/standalone/validation/'+label})
    path=ROOT/('reports/B_standalone_'+a.label+'.json');dump(path,{'status':'PASS','runs':rows,'scope':'Same RTL CPU/cache and AXI boundary with a fast functional RAM/UART model; every retirement compared to independent NEMU. Random deterministic channel stalls. No SoC timing or memory-pin performance claim.'});print('B_STANDALONE_PASS',a.label)

if __name__=='__main__':main()

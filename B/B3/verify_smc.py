from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'B1'))
from common import *
from verify import compile_app

def main():
    am=WORK/'soc/workbench/abstract-machine';arch='riscv32e-bnpc';ref=WORK/'fast-nemu-ref/build/riscv32-nemu-interpreter-so';rows=[]
    builds=json.loads((ROOT/'reports/B_standalone_builds.json').read_text())['variants']
    for label,fence,diff,expected in [('multicycle-cache128',0,False,0),('multicycle-cache128',1,True,0),('bad-fence-cache128',1,True,1)]:
        name=f'smc-fence{fence}';sources={'smc.S':f'#define WITH_FENCE {fence}\n'+(ROOT/'B/B3/smc.S').read_text()}
        image,elf=compile_app(name,arch,sources,am)
        build=next(b for b in builds if b['label']==label);exe=Path(build['executable']);assert sha(exe)==build['sha256']
        tag='B3/smc/'+label+'-fence'+str(fence);out=ROOT/'artifacts'/tag;out.mkdir(parents=True,exist_ok=True);result=out/'simulation.json';trace=out/'retired.bin'
        stdout,stderr,_=run(tag,[exe,'--image',image,*(['--ref',ref] if diff else ['--no-diff']),'--report',result,'--trace',trace,'--max-cycles','1000000'],inputs=[exe,ref,image,elf],outputs=[result,trace],expected=(expected,),timeout=60)
        data=json.loads(result.read_text())
        if expected:assert data['result']=='DIFF_FAIL' and 'DIFF_INSTRUCTION' in stderr
        else:assert data['result']=='GOOD_TRAP'
        rows.append({'label':label,'fence':bool(fence),'diff_enabled':diff,'status':'PASS_FAULT_REJECTED' if expected else 'PASS','simulation':data,'evidence':'artifacts/'+tag})
    dump(ROOT/'reports/B3_smc.json',{'status':'PASS','runs':rows,'scope':'RAM function returns1, store changes ADDI immediate to2. Without FENCE.I the characterized cache returns stale1 and the bounded program confirms it; this is permitted RISC-V behavior and explicitly uses no eager-coherent reference. With FENCE.I every retirement/instruction byte is checked by NEMU and the function returns2. Disabling invalidation gives a precise instruction mismatch; no timeout is accepted as a counterexample.'})
    print('B3_SMC_FENCE_PASS')

if __name__=='__main__':main()

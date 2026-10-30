from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'B1'))
from common import *
from verify import compile_app,context_sources

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--label',required=True);a=parser.parse_args();rows=[]
    am=WORK/'soc/workbench/abstract-machine';ref=WORK/'fast-nemu-ref/build/riscv32-nemu-interpreter-so'
    build=next(b for b in json.loads((ROOT/'reports/B_standalone_builds.json').read_text())['variants'] if b['label']==a.label);exe=Path(build['executable']);assert sha(exe)==build['sha256']
    jobs=[('hazards',{'main.S':(ROOT/'B/B4/programs/hazards.S').read_text()}),('fence-prefetch',{'main.S':(ROOT/'B/B4/programs/fence-prefetch.S').read_text()}),('context',context_sources(16)),('cycle',{'main.c':(ROOT/'B/B1/cycle-test.c').read_text()})]
    if build.get('fault_fence_flush'):jobs=[jobs[1]]
    if build.get('fault_raw'):jobs=[jobs[0]]
    for name,sources in jobs:
        image,elf=compile_app('b4-'+name,'riscv32e-bnpc',sources,am)
        tag='B4/functional/'+a.label+'-'+name;out=ROOT/'artifacts'/tag;out.mkdir(parents=True,exist_ok=True);result=out/'simulation.json';trace=out/'retired.bin'
        negative=build.get('fault_fence_flush',False) or build.get('fault_raw',False)
        stdout,stderr,_=run(tag,[exe,'--image',image,'--ref',ref,'--report',result,'--trace',trace,'--delay','7','--max-cycles','5000000'],inputs=[exe,ref,image,elf],outputs=[result,trace],expected=(1 if negative else 0,),timeout=90)
        data=json.loads(result.read_text())
        if negative:
            assert data['result']=='DIFF_FAIL'
            assert ('DIFF_INSTRUCTION' in stderr) if build.get('fault_fence_flush') else ('DIFF_GPR' in stderr)
        else:
            assert data['result']=='GOOD_TRAP' and data['diff_checked']+data['device_sync_checked']==data['instructions']
            if name=='context':assert data['ecalls']==data['mrets']==52
        rows.append({'name':name,'status':'PASS_FAULT_REJECTED' if negative else 'PASS','simulation':data,'evidence':'artifacts/'+tag,'image_sha256':sha(image)})
    dump(ROOT/('reports/B4_functional_'+a.label+'.json'),{'status':'PASS','runs':rows,'configuration':build,'scope':'Complete GPR/PC/instruction/memory comparisons to NEMU on randomized ready/valid stalls, independently generated arithmetic/memory checks, precise control redirects, real CTE/CSR tests and an explicit stale-prefetch FENCE.I fixture. Finite instruction streams, not a universal proof.'});print('B4_FUNCTIONAL_PASS',a.label)

if __name__=='__main__':main()

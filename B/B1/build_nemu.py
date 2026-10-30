from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    rows=[]
    for mode,nemu in [('native',BENCH/'nemu'),('reference',WORK/'nemu-ref')]:
        env={'NEMU_HOME':str(nemu),'USE_PINNED_DIFF_SO':'1','LD_LIBRARY_PATH':str(BENCH/'nemu/tools/capstone/repo')}
        if mode=='native':
            cfg=nemu/'configs/c2_io_defconfig'
            run('B1/nemu/'+mode+'-config',['make','-j4','c2_io_defconfig'],cwd=nemu,env=env,inputs=[cfg],outputs=[nemu/'.config'])
        else:
            cfg=nemu/'configs/b1_ref_defconfig'
            if not cfg.exists():shutil.copyfile(nemu/'.config',cfg)
            run('B1/nemu/'+mode+'-config',['make','-j4','b1_ref_defconfig'],cwd=nemu,env=env,inputs=[cfg],outputs=[nemu/'.config'])
        inputs=[p for p in sorted(nemu.rglob('*')) if p.is_file() and p.suffix in ('.c','.h') and not any(x in p.relative_to(nemu).parts for x in ['tools','build'])]
        inputs+=[nemu/'.config',nemu/'Makefile',ROOT/'B/runtime/budget_exec.py']
        exe=nemu/'build'/('riscv32-nemu-interpreter' + ('-so' if mode=='reference' else ''))
        budget=ROOT/'artifacts/B1/nemu'/mode/'budget.json'
        command=['make','-j4',*(['LIBS=-lreadline -ldl'] if mode=='reference' else [])]
        run('B1/nemu/'+mode,['python3',ROOT/'B/runtime/budget_exec.py','--report',budget,'--',*command],cwd=nemu,env=env,inputs=inputs,outputs=[exe,budget],timeout=240,resume=True)
        rows.append({'mode':mode,'executable':str(exe),'sha256':sha(exe),'config_sha256':sha(nemu/'.config')})
    dump(ROOT/'reports/B1_nemu_build.json',{'status':'BUILT_NOT_FUNCTIONALLY_ACCEPTED','variants':rows})

if __name__=='__main__':main()

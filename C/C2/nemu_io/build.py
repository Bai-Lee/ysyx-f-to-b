from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=['feature','performance','both'],default='both');args=parser.parse_args()
    n=BENCH/'nemu';d=ROOT/'C/C2/nemu_io';out=d/'runtime';out.mkdir(exist_ok=True)
    env={'NEMU_HOME':str(n),'USE_PINNED_DIFF_SO':'1','LD_LIBRARY_PATH':str(n/'tools/capstone/repo')}
    prior=ROOT/'reports/C2_nemu_build.json';rows=json.loads(prior.read_text())['variants'] if prior.exists() else []
    for mode in (['feature','performance'] if args.mode=='both' else [args.mode]):
        config=n/'configs'/('c2_io_defconfig' if mode=='feature' else 'c2_perf_defconfig')
        run('C2/nemu_io/build/'+mode+'-configure',['make','-j1',config.stem],cwd=n,env=env,inputs=[config,n/'Kconfig'],outputs=[n/'.config'],resume=True)
        directory=n/'build'/mode
        exe=directory/'riscv32-nemu-interpreter'
        sources=[p for p in n.rglob('*') if p.is_file() and p.suffix in ('.c','.h') and 'tools' not in p.relative_to(n).parts and 'build' not in p.relative_to(n).parts]
        run('C2/nemu_io/build/'+mode,['make','-j1','BUILD_DIR='+str(directory)],cwd=n,env=env,inputs=[n/'.config',*sources],outputs=[exe],timeout=300,resume=True)
        # NTFS stores the byte snapshot; execute the actual ELF on ext4.
        frozen=out/('nemu-c2-'+mode);shutil.copyfile(exe,frozen);cfg=out/(mode+'.config');shutil.copyfile(n/'.config',cfg)
        command=[exe,'-b','--report='+str(directory/'builtin.json')]
        if mode=='feature':command+=['--diff='+str(n/'tools/spike-diff/build/riscv32-spike-so')]
        run('C2/nemu_io/build/'+mode+'-builtin',command,cwd=n,env={**env,'SDL_VIDEODRIVER':'dummy'},inputs=[exe],outputs=[directory/'builtin.json'])
        result=json.loads((directory/'builtin.json').read_text());assert result['result']=='GOOD_TRAP' and result['diff_enabled']==(mode=='feature')
        content=cfg.read_text()
        if mode=='performance':
            assert all('# CONFIG_'+x+' is not set' in content for x in ['TRACE','DIFFTEST','WATCHPOINT','CC_DEBUG'])
            o,_,_=run('C2/nemu_io/build/performance_symbols',['nm',exe],inputs=[exe]);assert not any(name in o for name in [' dtrace_before',' dtrace_after',' dtrace_access',' disassemble'])
        rows=[r for r in rows if r['mode']!=mode]
        rows.append({'mode':mode,'executable':str(exe),'sha256':sha(exe),'snapshot':str(frozen.relative_to(ROOT)),'configuration':str(cfg.relative_to(ROOT)),'configuration_sha256':sha(cfg),'builtin':result})
    # Restore the normal feature config for subsequent C work; binaries remain separate.
    run('C2/nemu_io/build/restore_feature_config',['make','-j1','c2_io_defconfig'],cwd=n,env=env,inputs=[n/'configs/c2_io_defconfig'],outputs=[n/'.config'])
    dump(ROOT/'reports/C2_nemu_build.json',{'status':'PASS_BUILTIN_ONLY','variants':rows,'scope':'Separate real compiled feature and debug/trace/watch/DiffTest-free performance binaries. Full program tests follow.'})

if __name__=='__main__':main()

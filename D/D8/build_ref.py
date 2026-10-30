from pathlib import Path
import sys,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    d=ROOT/'D/D8';source=BENCH/'nemu';n=WORK/'nemu-ref';n.mkdir(exist_ok=True)
    # A separate source/configuration tree keeps the interactive NEMU executable
    # and its tested native configuration available throughout NPC development.
    for directory in ['src','include','scripts','configs']:
        shutil.copytree(source/directory,n/directory,dirs_exist_ok=True)
    for name in ['Makefile','Kconfig']:shutil.copyfile(source/name,n/name)
    for directory in ['kconfig','fixdep']:
        shutil.copytree(source/'tools'/directory,n/'tools'/directory,dirs_exist_ok=True)
    shutil.copyfile(source/'tools/difftest.mk',n/'tools/difftest.mk')
    rel='src/cpu/difftest/ref.c';prefix=re.match(r'/\*.*?\*/\s*',(source/rel).read_text(),re.S).group()
    p=n/rel;p.write_text(prefix+(ROOT/'D/nemu_overlay'/rel).read_text())
    cfg=n/'configs/dstage_ref_defconfig';cfg.write_text('CONFIG_ISA_riscv=y\nCONFIG_ENGINE_INTERPRETER=y\nCONFIG_TARGET_SHARE=y\nCONFIG_CC_O2=y\n# CONFIG_CC_DEBUG is not set\n# CONFIG_CC_ASAN is not set\n# CONFIG_TRACE is not set\n# CONFIG_DIFFTEST is not set\nCONFIG_MBASE=0x80000000\nCONFIG_MSIZE=0x08000000\n# CONFIG_MEM_RANDOM is not set\n# CONFIG_DEVICE is not set\n# CONFIG_WATCHPOINT is not set\n')
    env={'NEMU_HOME':str(n)}
    run('D8/ref/configure',['make','-j1','dstage_ref_defconfig'],cwd=n,env=env,inputs=[cfg,n/'Kconfig'],outputs=[n/'.config',n/'include/generated/autoconf.h'])
    so=n/'build/riscv32-nemu-interpreter-so'
    run('D8/ref/build',['make','-j1','LIBS=-lreadline -ldl'],cwd=n,env=env,inputs=[p,n/'.config',n/'src/isa/riscv32/inst.c',n/'src/memory/paddr.c'],outputs=[so],timeout=300)
    probe=WORK/'build/ref-probe';run('D8/ref/probe-build',['gcc','-std=c11','-Wall','-Wextra','-Werror',d/'ref_probe.c','-ldl','-o',probe],inputs=[d/'ref_probe.c'],outputs=[probe])
    o,e,_=run('D8/ref/probe',[probe,so],inputs=[probe,so]);assert 'REF_API_PASS' in o
    for mode,message in [('range','REF_MEMORY_RANGE'),('interrupt','REF_INTERRUPT_UNSUPPORTED')]:
        o,e,_=run('D8/ref/probe-'+mode,[probe,so,mode],inputs=[probe,so],expected=(-6,));assert message in o+e
    dump(ROOT/'reports/D8_reference.json',{'status':'PASS','shared_object':str(so),'sha256':sha(so),'configuration':str(n/'.config'),'configuration_sha256':sha(n/'.config'),'abi':'32 x uint32_t GPR followed by uint32_t PC (132 bytes); memcpy/regcpy direction 0 TO_DUT, 1 TO_REF','verified':['1000 bidirectional memory copies','GPR/PC both directions','x0 hard zero','exec(1),exec(2),store/load state','clean repeated init','memory bounds rejected','unused interrupt API explicitly rejects'], 'evidence':'artifacts/D8/ref'})

if __name__=='__main__':main()

from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    base=WORK/'soc/workbench';am=base/'abstract-machine';dest=am/'am/src/riscv/bnpc';dest.mkdir(parents=True,exist_ok=True)
    source=ROOT/'B/standalone/am'
    for name in ['ioe.c','trm.c','lshrdi3.S','ps2.h']:
        text=(ROOT/'B/soc/am'/name).read_text()
        if name=='trm.c':text=text.replace('void halt(int code) {','void halt(int code) {\n  *(volatile uint32_t*)0x10001000u=(uint32_t)code;\n  *(volatile uint32_t*)0x10001004u=0xb00d600du;')
        if name=='ioe.c':
            text=text.replace('.present=true,.has_accel=false','.present=false,.has_accel=false')
            text=text.replace('case AM_INPUT_CONFIG:((AM_INPUT_CONFIG_T*)buf)->present=true;','case AM_INPUT_CONFIG:((AM_INPUT_CONFIG_T*)buf)->present=false;')
        (dest/name).write_text(text)
    for name in ['cte.c','trap.S']:shutil.copyfile(ROOT/'B/B1'/name,dest/name)
    shutil.copyfile(source/'start.S',dest/'start.S');shutil.copyfile(source/'linker.ld',am/'scripts/bnpc.ld');shutil.copyfile(source/'bnpc.mk',am/'scripts/platform/bnpc.mk')
    (am/'scripts/riscv32e-bnpc.mk').write_text((ROOT/'B/soc/am/riscv32e-ysyxsoc.mk').read_text().replace('platform/ysyxsoc.mk','platform/bnpc.mk'))
    ref=WORK/'fast-nemu-ref';original=WORK/'nemu-ref'
    if not ref.exists():shutil.copytree(original,ref,ignore=shutil.ignore_patterns('.git','build','__pycache__'))
    changed=['src/isa/riscv32/inst.c','src/isa/riscv32/system/intr.c','src/isa/riscv32/init.c','include/b_csr.h']
    for name in changed:shutil.copyfile(original/name,ref/name)
    text=(original/'src/memory/paddr.c').read_text()
    assert text.count('{0x80000000,0x400000,false,"PSRAM",NULL}')==1
    text=text.replace('{0x80000000,0x400000,false,"PSRAM",NULL}','{0x80000000,0x8000000,false,"FAST_RAM",NULL}')
    text=text.replace(' {0xa0000000,0x8000000,false,"SDRAM",NULL},\n','')
    (ref/'src/memory/paddr.c').write_text(text)
    env={'NEMU_HOME':str(ref)}
    run('B/standalone/reference-config',['make','-j4','b1_ref_defconfig'],cwd=ref,env=env,inputs=[ref/'configs/b1_ref_defconfig'],outputs=[ref/'.config'])
    exe=ref/'build/riscv32-nemu-interpreter-so'
    inputs=[p for p in sorted(ref.rglob('*')) if p.is_file() and p.suffix in ('.c','.h') and not any(x in p.relative_to(ref).parts for x in ['tools','build'])]
    run('B/standalone/reference-build',['make','-j4','LIBS=-lreadline -ldl'],cwd=ref,env=env,inputs=inputs+[ref/'.config'],outputs=[exe],timeout=180,resume=True)
    dump(ROOT/'reports/B_standalone_setup.json',{'status':'BUILT_NOT_FUNCTIONALLY_ACCEPTED','reference':str(exe),'reference_sha256':sha(exe),'memory':'128MiB byte RAM at0x80000000; same independent NEMU instruction/CSR implementation, separate region table. SoC reference unchanged.','am':str(am),'arch':'riscv32e-bnpc','exit_mailbox':'0x10001000 code;0x10001004 magic0xb00d600d, then EBREAK. Used by four-state and gate-level tests without DPI.'})
    print('B_STANDALONE_PREPARED')

if __name__=='__main__':main()

from pathlib import Path
import sys,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    n=BENCH/'nemu';overlay=ROOT/'D/nemu_overlay'
    for p in sorted(overlay.rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(overlay);dest=n/rel;dest.parent.mkdir(parents=True,exist_ok=True)
        original=ARCHIVE/'repos/NJU-ProjectN__nemu__ics2024'/rel
        match=re.match(r'/\*.*?\*/\s*',original.read_text(),re.S) if original.exists() else None
        prefix=match.group(0) if match else ''
        dest.write_text(prefix+p.read_text())
    for name,rel in [('debug_core.c','src/monitor/sdb/debug_core.c'),('debug_core.h','include/debug_core.h')]:shutil.copyfile(ROOT/'D/runtime'/name,n/rel)
    shutil.copyfile(ROOT/'D/D2/gen_expr.c',n/'tools/gen-expr/gen-expr.c')
    workmake=BENCH/'Makefile';text=workmake.read_text();text=re.sub(r'^STUID = .*$', 'STUID = LOCAL_D_STAGE',text,flags=re.M);text=re.sub(r'^STUNAME = .*$', 'STUNAME = Independent_Local_Implementation',text,flags=re.M);workmake.write_text(text)
    original=ARCHIVE/'repos/NJU-ProjectN__nemu__ics2024/src/monitor/monitor.c';text=original.read_text()
    placeholder='  Log("Exercise: Please remove me in the source code and compile NEMU again.");\n  assert(0);'
    assert placeholder in text;text=text.replace(placeholder,'  /* Required framework onboarding placeholder completed; architectural checks remain enabled. */')
    (n/'src/monitor/monitor.c').write_text(text)
    original=ARCHIVE/'repos/NJU-ProjectN__nemu__ics2024/src/cpu/cpu-exec.c';text=original.read_text()
    anchor='    trace_and_difftest(&s, cpu.pc);';assert anchor in text
    text=text.replace(anchor,anchor+'\n#ifdef CONFIG_WATCHPOINT\n    extern bool sdb_check_watchpoints(void);\n    if(nemu_state.state==NEMU_RUNNING && sdb_check_watchpoints()) nemu_state.state=NEMU_STOP;\n#endif')
    (n/'src/cpu/cpu-exec.c').write_text(text)
    kconfig=(ARCHIVE/'repos/NJU-ProjectN__nemu__ics2024/Kconfig').read_text()
    (n/'Kconfig').write_text(kconfig+'\nconfig WATCHPOINT\n  bool "Enable debugger watchpoints"\n  depends on TARGET_NATIVE_ELF\n  default y\n')
    config=n/'configs/dstage_pa1_defconfig';config.write_text('CONFIG_ISA_riscv=y\nCONFIG_ENGINE_INTERPRETER=y\nCONFIG_TARGET_NATIVE_ELF=y\nCONFIG_CC_O2=y\nCONFIG_CC_DEBUG=y\nCONFIG_CC_ASAN=y\nCONFIG_TRACE=y\nCONFIG_ITRACE=y\nCONFIG_MBASE=0x80000000\nCONFIG_MSIZE=0x08000000\n# CONFIG_MEM_RANDOM is not set\n# CONFIG_DEVICE is not set\n')
    env={'NEMU_HOME':str(n)}
    run('D2/nemu/configure',['make','-j1','dstage_pa1_defconfig'],cwd=n,env=env,inputs=[config,n/'Kconfig'],timeout=120,outputs=[n/'.config',n/'include/generated/autoconf.h'])
    changed=[n/p.relative_to(overlay) for p in overlay.rglob('*') if p.is_file()]+[n/'src/monitor/sdb/debug_core.c',n/'include/debug_core.h',n/'src/monitor/monitor.c',n/'src/cpu/cpu-exec.c',n/'.config']
    exe=n/'build/riscv32-nemu-interpreter';run('D2/nemu/build',['make','-j1'],cwd=n,env=env,inputs=changed,outputs=[exe],timeout=300)
    run('D2/nemu/builtin',[exe,'-b'],cwd=n,env=env,inputs=[exe,n/'tools/capstone/repo/libcapstone.so.5'])
    dump(ROOT/'reports/D2_nemu_build.json',{'status':'PASS_BUILD_AND_BUILTIN_ONLY','runtime':str(n),'executable':str(exe),'sha256':sha(exe),'inputs':[{'path':str(p),'sha256':sha(p)} for p in changed],'upstream':'8e7a0fecc95b5b5d2c1f6be0ec1b703da93356c0','instruction_scope':'Original PA1 minimal four-instruction scaffold retained; full RV32IM belongs to D3.'})

if __name__=='__main__':main()

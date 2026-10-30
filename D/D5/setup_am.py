from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    am=BENCH/'abstract-machine';n=BENCH/'nemu';scope=ROOT/'D/D5';patched=[]
    for name in ['string.c','stdio.c','alloc.c']:
        dest=am/'klib/src'/name;text=(ROOT/'D/klib_overlay'/name).read_text()
        if name=='stdio.c':
            original=(ARCHIVE/'repos/NJU-ProjectN__abstract-machine__ics2026/klib/src/stdio.c').read_text();tail=original[original.index('int __am_vsscanf_internal'):];text=text.rsplit('#endif',1)[0]+tail
        dest.write_text(text);patched.append(dest)
    stdlib=am/'klib/src/stdlib.c';original=(ARCHIVE/'repos/NJU-ProjectN__abstract-machine__ics2026/klib/src/stdlib.c').read_text();start=original.index('void *malloc(');end=original.index('void exit(',start)
    tail=original[end:].replace('void exit(int status) {\n  halt(status);\n}','#ifndef __ISA_NATIVE__\nvoid exit(int status) {\n  halt(status);\n}\n#endif')
    stdlib.write_text(original[:start]+'/* Allocation is implemented in alloc.c, with a native-host bridge. Native exit is provided by glibc. */\n\n'+tail);patched.append(stdlib)
    native=am/'scripts/native-klib.mk';native.write_text('include $(AM_HOME)/scripts/native.mk\nARCH_H := arch/native.h\nCFLAGS += -D__NATIVE_USE_KLIB__\n');patched.append(native)
    make=am/'Makefile';text=make.read_text();text=text.replace('ifneq ($(filter $(ARCH),native),)','ifneq ($(filter $(ARCH),native native-klib),)');make.write_text(text);patched.append(make)
    timer=am/'am/src/platform/nemu/ioe/timer.c';text=timer.read_text();text=text.replace('  uptime->us = 0;','  uint32_t lo = inl(RTC_ADDR);\n  uint32_t hi = inl(RTC_ADDR + 4);\n  uptime->us = ((uint64_t)hi << 32) | lo;');timer.write_text(text);patched.append(timer)
    mf=BENCH/'am-kernels/tests/cpu-tests/Makefile';text=mf.read_text();old='\t@grep -q "FAIL" $(RESULT) | grep -v "wrong\\]"; FAIL=$$?; rm $(RESULT); test $$FAIL -ne 0'
    if old in text:text=text.replace(old,'\t@if grep -q "FAIL" $(RESULT); then exit 1; fi');mf.write_text(text)
    patched.append(mf)
    tests=BENCH/'am-kernels/tests/klib-tests';tests.mkdir(exist_ok=True);shutil.copyfile(scope/'portable_tests.c',tests/'main.c');(tests/'Makefile').write_text('NAME = klib-tests\nSRCS = main.c\ninclude $(AM_HOME)/Makefile\n')
    config=n/'configs/dstage_am_defconfig';base=(n/'configs/dstage_rv32im_defconfig').read_text().replace('# CONFIG_DEVICE is not set','CONFIG_DEVICE=y\nCONFIG_HAS_SERIAL=y\nCONFIG_HAS_TIMER=y\n# CONFIG_HAS_KEYBOARD is not set\n# CONFIG_HAS_VGA is not set\n# CONFIG_HAS_AUDIO is not set\n# CONFIG_HAS_DISK is not set\n# CONFIG_HAS_SDCARD is not set');config.write_text(base)
    env={'NEMU_HOME':str(n),**json.loads((ROOT/'reports/D_spike_support.json').read_text())['env'],'SDL_VIDEODRIVER':'dummy','SDL_AUDIODRIVER':'dummy'}
    run('D5/nemu/configure',['make','-j1','dstage_am_defconfig'],cwd=n,env=env,inputs=[config,n/'Kconfig'],outputs=[n/'.config'])
    exe=n/'build/riscv32-nemu-interpreter';run('D5/nemu/build',['make','-j1'],cwd=n,env=env,inputs=[n/'.config',n/'src/isa/riscv32/inst.c',n/'src/memory/paddr.c'],outputs=[exe],timeout=300)
    # The standard one-command AM run also rebuilds the upstream Spike adapter.
    run('D5/spike/full_target',['make','-j1'],cwd=n/'tools/spike-diff',env=env,inputs=[n/'tools/spike-diff/Makefile',n/'tools/spike-diff/difftest.cc'],outputs=[n/'tools/spike-diff/build/riscv32-spike-so'],timeout=600)
    saved=scope/'runtime_patch';saved.mkdir(exist_ok=True)
    for p in patched:
        rel=p.relative_to(BENCH);dest=saved/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
    dump(ROOT/'reports/D5_setup.json',{'status':'PASS_SETUP_NOT_FULL_RUNTIME_TEST','patched_files':[{'path':str(p),'sha256':sha(p)} for p in patched],'native_klib':'Separate native-klib architecture prevents stale libc-only archives; native allocator deliberately delegates to locked glibc, while bare-metal uses own allocator.','nemu':str(exe),'nemu_sha256':sha(exe),'spike':str(n/'tools/spike-diff/build/riscv32-spike-so'),'environment':env})
    print('D5_SETUP_PASS',flush=True)

if __name__=='__main__':main()

from pathlib import Path
import sys,shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *

D=ROOT/'C/C2/nemu_io';N=BENCH/'nemu';APPS=WORK/'c2-nemu-apps'

def save_original(path):
    rel=path.relative_to(BENCH);target=D/'upstream'/rel;target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists():shutil.copyfile(path,target)

def main():
    assert not (ROOT/'reports/C2_nemu_setup.json').exists(),'C2 NEMU already initialized'
    APPS.mkdir(exist_ok=True)
    for name in ('am-kernels','fceux-am'):
        target=APPS/name
        if not target.exists():shutil.copytree(BENCH/name,target,symlinks=True,ignore=shutil.ignore_patterns('.git','build','__pycache__'))
    # Preserve the workbench git-logging macro while the app tree is independent.
    shutil.copyfile(BENCH/'Makefile',APPS/'Makefile')
    run('C2/nemu_io/setup/git_init',['git','init'],cwd=APPS)
    run('C2/nemu_io/setup/git_name',['git','config','user.name','Local C2 NEMU applications'],cwd=APPS)
    run('C2/nemu_io/setup/git_email',['git','config','user.email','local-c2@invalid.example'],cwd=APPS)
    (APPS/'.gitignore').write_text('**/build/\n**/*.o\n')
    run('C2/nemu_io/setup/git_add',['git','add','.'],cwd=APPS)
    run('C2/nemu_io/setup/git_commit',['git','-c','gc.auto=0','commit','-m','Freeze C2 application inputs'],cwd=APPS)
    changed=[]
    for source in sorted((D/'am').glob('*.c')):
        target=BENCH/'abstract-machine/am/src/platform/nemu/ioe'/source.name;save_original(target);shutil.copyfile(source,target);changed.append(target)
    path=N/'src/device/vga.c';save_original(path);text=path.read_text()
    old='''  // TODO: call `update_screen()` when the sync register is non-zero,
  // then zero out the sync register'''
    assert old in text
    text=text.replace(old,'''  if (vgactl_port_base[1] != 0) {
    IFDEF(CONFIG_VGA_SHOW_SCREEN, update_screen());
    vgactl_port_base[1] = 0;
  }''')
    text=text.replace('  vgactl_port_base[0] = (screen_width() << 16) | screen_height();','  vgactl_port_base[0] = (screen_width() << 16) | screen_height();\n  vgactl_port_base[1] = 0;')
    path.write_text(text);changed.append(path)
    path=N/'src/device/io/map.c';save_original(path);text=path.read_text()
    text=text.replace('static void check_bound(IOMap *map, paddr_t addr)', 'static void check_bound(IOMap *map, paddr_t addr, int len)')
    text=text.replace('Assert(addr <= map->high && addr >= map->low,','Assert(addr <= map->high && addr >= map->low && (uint32_t)(len - 1) <= map->high - addr,')
    text=text.replace('  check_bound(map, addr);','  check_bound(map, addr, len);')
    text=text.replace('word_t map_read(', (D/'io_trace.inc').read_text()+'\nword_t map_read(')
    text=text.replace('  return ret;\n}', "  c2_device_trace(map, 'R', addr, len, ret);\n  return ret;\n}")
    text=text.replace('  invoke_callback(map->callback, offset, len, true);',"  invoke_callback(map->callback, offset, len, true);\n  c2_device_trace(map, 'W', addr, len, data);")
    path.write_text(text);changed.append(path)
    path=N/'Kconfig';save_original(path);text=path.read_text();needle='config DIFFTEST\n';assert needle in text
    text=text.replace(needle,'config DTRACE\n  depends on TRACE && DEVICE\n  bool "Enable bounded named-device trace"\n  default n\n\n'+needle);path.write_text(text);changed.append(path)
    # Truly remove inherited trace hooks in the performance configuration.
    path=N/'include/dtrace.h';save_original(path);text=path.read_text();start=text.index('void dtrace_start(');end=text.rfind('#endif')
    declarations=text[start:end]
    noops='''static inline void dtrace_start(void) {}
static inline void dtrace_finish(void) {}
static inline int dtrace_legacy_allow(void) { return 0; }
static inline void dtrace_before(uint32_t p,uint32_t i) { (void)p;(void)i; }
static inline void dtrace_after(uint32_t p,uint32_t i,uint32_t n) { (void)p;(void)i;(void)n; }
static inline void dtrace_access(uint32_t p,char o,uint32_t a,unsigned l,uint32_t d) { (void)p;(void)o;(void)a;(void)l;(void)d; }
static inline void dtrace_error(void) {}
'''
    text=text[:start]+'#ifdef CONFIG_TRACE\n'+declarations+'#else\n'+noops+'#endif\n'+text[end:];path.write_text(text);changed.append(path)
    path=N/'src/utils/trace_adapter.c';save_original(path);text=path.read_text();text=text.replace('static dtrace_context *context;','#ifdef CONFIG_TRACE\nstatic dtrace_context *context;\nstatic unsigned active_modes;')
    text=text.replace('  context=dtrace_create(', '  active_modes=modes;\n  context=dtrace_create(').replace('if(context)disassemble(', 'if(context && (active_modes & 1))disassemble(')
    path.write_text(text+'\n#endif /* CONFIG_TRACE */\n');changed.append(path)
    # The default upstream run target always rebuilds Spike (PHONY). Declare the
    # already accepted shared object as a pinned external input for these runs.
    path=N/'tools/difftest.mk';save_original(path);text=path.read_text();text=text.replace('ifndef CONFIG_DIFFTEST_REF_NEMU','ifneq ($(USE_PINNED_DIFF_SO),1)\nifndef CONFIG_DIFFTEST_REF_NEMU').replace('.PHONY: $(DIFF_REF_SO)\nendif','.PHONY: $(DIFF_REF_SO)\nendif # USE_PINNED_DIFF_SO\nendif')
    path.write_text(text);changed.append(path)
    config=(N/'.config').read_text().replace('# CONFIG_HAS_KEYBOARD is not set','CONFIG_HAS_KEYBOARD=y').replace('# CONFIG_HAS_VGA is not set','CONFIG_HAS_VGA=y\nCONFIG_VGA_SHOW_SCREEN=y\nCONFIG_VGA_SIZE_400x300=y').replace('CONFIG_TIMER_GETTIMEOFDAY=y','# CONFIG_TIMER_GETTIMEOFDAY is not set').replace('# CONFIG_TIMER_CLOCK_GETTIME is not set','CONFIG_TIMER_CLOCK_GETTIME=y')
    config+='\nCONFIG_DTRACE=y\n';(N/'configs/c2_io_defconfig').write_text(config)
    perf=config.replace('CONFIG_TRACE=y','# CONFIG_TRACE is not set').replace('CONFIG_ITRACE=y','# CONFIG_ITRACE is not set').replace('CONFIG_DIFFTEST=y','# CONFIG_DIFFTEST is not set').replace('CONFIG_WATCHPOINT=y','# CONFIG_WATCHPOINT is not set').replace('CONFIG_DTRACE=y','# CONFIG_DTRACE is not set')
    # VGA/keyboard are absent in the performance-only binary, while RTC/serial stay.
    perf=perf.replace('CONFIG_HAS_KEYBOARD=y','# CONFIG_HAS_KEYBOARD is not set').replace('CONFIG_HAS_VGA=y','# CONFIG_HAS_VGA is not set')
    (N/'configs/c2_perf_defconfig').write_text(perf)
    menu=APPS/'am-kernels/tests/am-tests';shutil.copyfile(D/'trm_only.c',menu/'c2_trm_only.c')
    path=menu/'Makefile';path.write_text(path.read_text().replace('include $(AM_HOME)/Makefile','ifneq ($(ARCH),native)\nSRCS += c2_trm_only.c\nendif\ninclude $(AM_HOME)/Makefile'))
    overlay=D/'installed';overlay.mkdir(exist_ok=True)
    for p in changed:
        target=overlay/p.relative_to(BENCH);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
    dump(ROOT/'reports/C2_nemu_setup.json',{'status':'PASS_SOURCE_SETUP_NOT_EXECUTION','changed':[{'path':str(p),'sha256':sha(p)} for p in changed],'apps':str(APPS),'timer_contract':'High read snapshots both RTC words; AM reads high then low and subtracts IOE initialization baseline.','performance_contract':'Separate output path and configuration; CONFIG_TRACE disables all inherited hooks, watchpoints/DiffTest/debug/DTRACE off.'})
    print('C2_NEMU_IO_INSTALLED',flush=True)

if __name__=='__main__':main()

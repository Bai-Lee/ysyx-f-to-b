from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    base=WORK/'c4/workbench';base.mkdir(parents=True,exist_ok=True);am=base/'abstract-machine'
    if not am.exists():shutil.copytree(BENCH/'abstract-machine',am,symlinks=True,ignore=shutil.ignore_patterns('.git','build','__pycache__'))
    source=WORK/'c2-nemu-apps/am-kernels/benchmarks/microbench';app=base/'microbench'
    if not app.exists():shutil.copytree(source,app,symlinks=True,ignore=shutil.ignore_patterns('build','.git'))
    hello=base/'hello'
    if not hello.exists():shutil.copytree(BENCH/'am-kernels/kernels/hello',hello,ignore=shutil.ignore_patterns('build'))
    shutil.copyfile(BENCH/'Makefile',base/'Makefile')
    if not (base/'.git').exists():
        run('C4/apps/git-init',['git','init'],cwd=base)
        run('C4/apps/git-name',['git','config','user.name','Local C4 engineering'],cwd=base)
        run('C4/apps/git-email',['git','config','user.email','local-c4@invalid.example'],cwd=base)
        (base/'.gitignore').write_text('**/build/\n**/*.o\n')
        run('C4/apps/git-add',['git','add','.'],cwd=base)
        run('C4/apps/git-baseline',['git','-c','gc.auto=0','commit','-m','Freeze C4 AM and application inputs'],cwd=base)
    calibration=ROOT/'C/C4/clock_config.json'
    hz=json.loads(calibration.read_text())['ticks_hz'] if calibration.exists() else 100000000
    script=am/'scripts/riscv32e-c4.mk';script.write_text('include $(AM_HOME)/scripts/riscv32e-npc.mk\nCFLAGS += -DC4_RTL_TIMER -DC4_CLINT_HZ='+str(hz)+'u\n')
    timer=am/'am/src/riscv/npc/timer.c'
    source=ROOT/'C/C4/am_timer.c';shutil.copyfile(source,timer)
    npc=base/'npc';npc.mkdir(exist_ok=True);ref=WORK/'nemu-ref/build/riscv32-nemu-interpreter-so'
    (npc/'Makefile').write_text('.DEFAULT_GOAL := all\nC4_MODE ?= 6\nSIM := '+str(WORK/'c4/build')+'/mode$(C4_MODE)/sim\nNPC_ARGS ?=\nall:\n\ttest -x $(SIM)\nsim: all\n\t$(SIM) --image "$(IMAGE)" --elf "$(ELF)" --ref '+str(ref)+' --report "$(IMAGE).npc.json" --max-cycles 20000000000 $(NPC_ARGS)\ninclude ../Makefile\n.PHONY: all sim\n')
    probe=base/'clock-probe';probe.mkdir(exist_ok=True)
    shutil.copyfile(ROOT/'C/C4/clock_probe.c',probe/'main.c');(probe/'Makefile').write_text('NAME = clock-probe\nSRCS = main.c\ninclude $(AM_HOME)/Makefile\n')
    dump(ROOT/'reports/C4_app_setup.json',{'status':'PASS_SOURCE_SETUP','workbench':str(base),'timer_source':str(source.relative_to(ROOT)),'timer_sha256':sha(source),'scope':'Private C4 AM/app tree. riscv32e-npc retains C++ microsecond model; riscv32e-c4 converts actual RTL cycle ticks using default100MHz or an explicit calibration hook. All source inputs and benchmark validators remain unchanged.'})
    print('C4_PRIVATE_APPS_READY',flush=True)
if __name__=='__main__':main()

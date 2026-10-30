from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
base=ROOT/'C/C5';nv=WORK/'c5/nvboard';generated=WORK/'c5/build/30000000-cycle-psram4m-qpi-sdram16x1-opt'
flags=subprocess.check_output(['sdl2-config','--cflags'],text=True).split()
run('C5/sim/gui-syntax',['g++','-std=c++17','-fsyntax-only','-Wall','-Wextra','-DC5_ENABLE_NVBOARD','-I'+str(generated),'-I'+str(VROOT/'include'),'-I'+str(VROOT/'include/vltstd'),'-I'+str(nv/'usr/include'),*flags,base/'sim/runner.cpp',WORK/'c5/nvboard_bind.cpp'],inputs=[base/'sim/runner.cpp',*sorted((base/'sim').glob('*.hpp')),WORK/'c5/nvboard_bind.cpp'],timeout=60)
print('C5_GUI_HOST_SYNTAX_PASS_NOT_RUNTIME',flush=True)

from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
BENCH7=WORK/'workbench-e7'
def env7(extra=None):
 e={'AM_HOME':str(BENCH7/'abstract-machine'),'NPC_HOME':str(BENCH7/'npc'),'BENCH_HOME':str(BENCH7/'archbench'),'YSYX_HOME':str(BENCH7),'nproc':'1'}
 if extra:e.update(extra)
 return e

from pathlib import Path
import sys,re
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *

source=ROOT/'D/runtime/sources/pa/e1e078e85812b41f.md';text=source.read_text()
blocks=re.findall(r'```c\n(.*?)```',text,re.S)
original=next(s for s in blocks if 'uint8_t R[NREG]' in s and 'int main()' in s)
d=ROOT/'C/C2/nemu_io/compiler';d.mkdir(exist_ok=True);raw=d/'yemu-original.c';raw.write_text(original)
instrumented=d/'yemu-trace.c';needle='    exec_once();';assert needle in original
instrumented.write_text(original.replace(needle,needle+'\n    printf("YEMU_STATE pc=%u r0=%u r1=%u z=%u halt=%d\\n",pc,R[0],R[1],M[7],halt);'))
exe=WORK/'c2-host/yemu';run('C2/pa2/yemu/build',['gcc','-std=gnu11','-Wall','-Wextra','-Werror',instrumented,'-o',exe],inputs=[raw,instrumented,source],outputs=[exe])
o,_,_=run('C2/pa2/yemu/run',[exe],inputs=[exe]);rows=[list(map(int,m)) for m in re.findall(r'YEMU_STATE pc=(\d+) r0=(\d+) r1=(\d+) z=(\d+) halt=(\d+)',o)]
expected=[[1,33,0,0,0],[2,33,33,0,0],[3,16,33,0,0],[4,49,33,0,0],[5,49,33,49,0],[6,98,33,49,0],[7,98,33,49,1]]
assert rows==expected and 'The result of 16 + 33 is 49' in o
dump(ROOT/'reports/C2_pa2_yemu.json',{'status':'PASS','source':str(source),'source_sha256':sha(source),'state_columns':['pc','r0','r1','M[7]','halt'],'states':rows,'scope':'Original teaching YEMU plus observation-only printf, actual GCC build. After storing49 the source continues into data: x=0x10 doublesr0; y=0x21 is invalid and halts. Host bit-field layout verified only for this compiler; original course code is not altered.'})
print('C2_YEMU_TRACE_PASS',flush=True)

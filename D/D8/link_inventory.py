from pathlib import Path
import sys,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
suite=BENCH/'archbench';am=BENCH/'abstract-machine';rows=[]
for cwd in sorted((suite/'bench').iterdir()):
    if not cwd.is_dir():continue
    o,e,r=run('D8/link_inventory/'+cwd.name,['make','-j1','ARCH=riscv32e-npc','mainargs=test','image'],cwd=cwd,inputs=[cwd/'Makefile',suite/'Makefile',am/'klib/build/klib-riscv32e-npc.a'],env={'BENCH_HOME':str(suite),'nproc':'1'},expected=(0,2),timeout=300)
    symbols=sorted(set(re.findall(r"undefined reference to [`']([^']+)'",e)))
    rows.append({'program':cwd.name,'status':'LINKED' if r['exit_code']==0 else 'MISSING_INTERFACES' if symbols else 'BUILD_FAILURE','missing_symbols':symbols,'exit_code':r['exit_code']})
    dump(ROOT/'reports/D8_link_inventory.json',{'status':'DIAGNOSTIC_NOT_RUNTIME_ACCEPTANCE','rows':rows})
print('LINK_INVENTORY',sorted({s for r in rows for s in r['missing_symbols']}),flush=True)

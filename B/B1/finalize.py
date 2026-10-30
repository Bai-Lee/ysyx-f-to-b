from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    for name in ['native','npc']:assert json.loads((ROOT/f'reports/B1_{name}.json').read_text())['status']=='PASS'
    evidence=['reports/B1_native.json','reports/B1_npc.json','reports/B1_spike_environment.json','B/B1/NOTES.md']
    for task in ['B1-M001','B1-M002','B1-M003','B1-M005']:
        mark([task],'PASS',evidence,'Fresh B execution with positive/negative controls, independent differential comparisons and exception traces. Scope is synchronous machine mode; details in B1 notes.')
    mark(['B1-M004'],'PASS_ADAPTED',evidence,'Actual startup reads and prints project vendor/id; no student identity or official qualification is asserted.')
    specs=json.loads((ROOT/'B/runtime/course_specs.json').read_text())
    nested=[]
    for record in specs['nested_source_records']:
        status='PASS' if record['classification']=='公开任务' else 'REVIEWED_BACKGROUND_OR_RULE'
        nested.append({'id':record['id'],'status':status,'evidence':evidence,'scope':'RISC-V path and RT-Thread prefix; x86/MIPS examples are explanatory only.'})
    dump(ROOT/'reports/B1_AUDIT.json',{'status':'PASS_PUBLIC_ENGINEERING','nested_records':nested,'evidence':evidence,'exclusions':['B1 personal C-stage application','PA4 Nanos-lite and later user processes','full privileged ISA and asynchronous interrupts']})
    print('B1_PUBLIC_ENGINEERING_PASS')

if __name__=='__main__':main()

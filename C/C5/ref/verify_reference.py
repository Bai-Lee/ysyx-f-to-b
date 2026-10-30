from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
source=ROOT/'C/C5/ref/check_reference.py';report=ROOT/'reports/C5_reference_build.json'
data=json.loads(report.read_text());exe=Path(data['binary']);assert sha(exe)==data['sha256'];rows=[]
for name,options,expected,marker in [('positive',[],0,'C5_REFERENCE_MEMORY_AND_MROM_INSTRUCTIONS_PASS'),('span',['--bad-span'],-6,'REF_MEMORY_RANGE'),('rom-write',['--bad-rom-write'],-6,'C5_READONLY_REGION')]:
    out,err,record=run('C5/reference/'+name,['python3',source,*options],inputs=[source,exe],expected=(expected,))
    assert marker in out+err;rows.append({'name':name,'status':'PASS','expected_exit':expected,'evidence':'artifacts/C5/reference/'+name})
data['status']='PASS_MEMORY_REGIONS_AND_MROM_EXECUTION_CONTROLS';data['controls']=rows;dump(report,data)
print('C5_REFERENCE_CONTROLS_PASS',flush=True)

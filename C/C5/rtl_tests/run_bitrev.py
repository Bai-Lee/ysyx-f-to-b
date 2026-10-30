from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
iverilog=Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin/iverilog');vvp=iverilog.parent/'vvp'
sources=[ROOT/'C/C5/perip/bitrev/bitrev.v',ROOT/'C/C5/rtl_tests/bitrev_tb.sv'];out=WORK/'c5/bitrev-unit';out.mkdir(parents=True,exist_ok=True);rows=[]
for name,bad,exit_code,marker in [('good',0,0,'BITREV_ALL256_AND_ABORT_RESET_PASS'),('echo-mutant',1,1,'BIT_REVERSE')]:
    exe=out/(name+'.vvp');tag='C5/bitrev-unit/'+name
    run(tag+'/compile',[iverilog,'-g2012','-s','bitrev_tb','-Pbitrev_tb.BAD='+str(bad),'-o',exe,*sources],inputs=sources,outputs=[exe])
    text,err,row=run(tag+'/run',[vvp,exe],inputs=[exe],expected=(exit_code,));assert marker in text+err
    rows.append({'name':name,'status':'PASS','expected_exit':exit_code,'evidence':row['name']})
dump(ROOT/'reports/C5_bitrev_unit.json',{'status':'PASS_FOUR_STATE_ALL_INPUTS_AND_MUTANT','runs':rows,'sources':[{'path':str(p),'sha256':sha(p)} for p in sources]})
print('C5_BITREV_FOUR_STATE_PASS',flush=True)

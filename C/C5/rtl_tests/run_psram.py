from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
iverilog=Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin/iverilog');vvp=iverilog.parent/'vvp'
sources=[ROOT/'C/C5/perip/psram/psram.v',ROOT/'C/C5/rtl_tests/psram_tb.sv'];out=WORK/'c5/psram-unit';out.mkdir(parents=True,exist_ok=True);rows=[]
cases=[('good',0,0,0,'PSRAM_PIN_PROTOCOL_PASS'),('wrong-data',1,0,1,'PSRAM_READ_DATA'),('no-powerup-clock',0,1,1,'PSRAM_CE_HIGH_CLOCK_REQUIRED'),
       ('outside-model',0,2,1,'PSRAM_ADDRESS_OUTSIDE_MODEL'),('bus-contention',0,3,1,'PSRAM_READ_DATA'),('unsupported',0,4,1,'PSRAM_UNSUPPORTED_COMMAND')]
for name,bad,scenario,expected,marker in cases:
    image=out/(name+'.vvp');tag='C5/psram-unit/'+name
    run(tag+'/compile',[iverilog,'-g2012','-DSYNTHESIS=1','-s','psram_tb','-Ppsram_tb.BAD_DATA='+str(bad),'-Ppsram_tb.SCENARIO='+str(scenario),'-o',image,*sources],inputs=sources,outputs=[image])
    text,err,r=run(tag+'/run',[vvp,image],inputs=[image],expected=(expected,),timeout=30);assert marker in text+err
    rows.append({'name':name,'status':'PASS','expected_exit':expected,'stdout':text,'evidence':r['name']})
dump(ROOT/'reports/C5_psram_model.json',{'status':'PASS_FOUR_STATE_PIN_PROTOCOL_AND_CONTROLS','runs':rows,'model_sha256':sha(sources[0]),
     'scope':'4KiB initial model. SPIEB/38,6dummy clocks, nibble order, allbytevalues,1024-byte pagewrap,35enter/F5exitQPI, high-Z direction and aborted partial writes tested. Wrong data, missing power-up clock, capacity overrun, host contention and unsupported command rejected. Zero initialization is deterministic model state; no analog/PVT/refresh claim.'})
print('C5_PSRAM_PIN_MODEL_PASS',flush=True)

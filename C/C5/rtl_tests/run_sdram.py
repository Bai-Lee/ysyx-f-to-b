from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
iverilog=Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin/iverilog');vvp=iverilog.parent/'vvp'
sources=[ROOT/'C/C5/perip/sdram/sdram.v',ROOT/'C/C5/rtl_tests/sdram_tb.sv'];out=WORK/'c5/sdram-unit';out.mkdir(parents=True,exist_ok=True);rows=[]
for name,scenario,bad,expected,marker in [('good',0,False,0,'SDRAM_PIN_PROTOCOL_PASS'),('wrong-data',0,True,1,'SDRAM_READ_DATA'),('no-active',1,False,1,'SDRAM_ACCESS_WITHOUT_ACTIVE_ROW'),('bad-mode',2,False,1,'SDRAM_UNSUPPORTED_MODE'),('floating-write',3,False,1,'SDRAM_WRITE_UNKNOWN_LOW')]:
    image=out/(name+'.vvp');tag='C5/sdram-unit/'+name
    run(tag+'/compile',[iverilog,'-g2012','-s','sdram_tb','-Psdram_tb.SCENARIO='+str(scenario),*(['-DC5_SDRAM_BAD_READ'] if bad else []),'-o',image,*sources],inputs=sources,outputs=[image],timeout=60)
    text,err,record=run(tag+'/run',[vvp,image],inputs=[image],expected=(expected,),timeout=30);assert marker in text+err
    rows.append({'name':name,'status':'PASS','expected_exit':expected,'stdout':text,'evidence':'artifacts/'+tag})
pdf=ARCHIVE/'assets/offline/www.mouser.com/datasheet/2/12/alliance_MT48LC-1155509.pdf'
dump(ROOT/'reports/C5_sdram_model.json',{'status':'PASS_ISOLATED_FOUR_STATE_PIN_PROTOCOL','runs':rows,'model_sha256':sha(sources[0]),'spec':{'path':str(pdf),'sha256':sha(pdf),'revision':'Micron256Mb_sdr Rev.W05/15','pages':[45,48,50,58]},'scope':'Small32KiB instance with real4banks/512columns/8rows. CL2/3, BL1/2/4/8, sequential/interleaved wrap, distinct bank/row data, byte masks, read DQM latency, CKE command suspension, highZ, precharge and refresh. Incorrect data and invalid commands rejected. Full32MiB/4-chip CPU acceptance is separate. No electrical/retention or arbitrary overlapped-read pipeline claim.'})
print('C5_SDRAM_MODEL_PASS',flush=True)

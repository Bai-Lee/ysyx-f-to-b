from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
iv=Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin/iverilog');vvp=iv.parent/'vvp';base=ROOT/'C/C5/perip/psram'
sources=[base/'psram.v',base/'psram_top_apb.v',base/'efabless/EF_PSRAM_CTRL.v',base/'efabless/EF_PSRAM_CTRL_wb.v',ROOT/'C/C5/rtl_tests/psram_controller_tb.sv']
out=WORK/'c5/psram-controller';out.mkdir(parents=True,exist_ok=True);rows=[]
for mode in [0,1]:
    tag='C5/psram-controller/'+('qpi' if mode else 'spi');image=out/f'mode{mode}.vvp'
    run(tag+'/compile',[iv,'-g2012','-DSYNTHESIS=1','-DC5_PSRAM_QPI='+str(mode),'-s','psram_controller_tb','-o',image,*sources],inputs=sources,outputs=[image])
    text,error,r=run(tag+'/run',[vvp,image],inputs=[image],timeout=30)
    assert 'PSRAM_CONTROLLER_PASS checks=11 qpi='+str(mode) in text
    rows.append({'mode':mode,'status':'PASS','stdout':text,'evidence':r['name']})
dump(ROOT/'reports/C5_psram_controller.json',{'status':'PASS_SPI_QPI_MASKS_AND_WARM_RESET','runs':rows,'sources':[{'path':str(p),'sha256':sha(p)} for p in sources],
     'scope':'Actual preserved Efabless data paths with parameterized command phase and authored initialization: CE-high clock, safe quad F5 resynchronization, optional serial35 entry. Byte/half/word stores, aligned readback, page boundaries, zero-strobe no-op, unsupported noncontiguous mask SLVERR and warm-reset data/mode preservation.'})
print('C5_PSRAM_CONTROLLERS_PASS',flush=True)

from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    rtl=ROOT/'B/soc/perip/amba/axi4_delayer.v';cpp=ROOT/'B/B3/axi_delay_test.cpp';rows=[]
    for ratio,bad in [(256,0),(320,0),(512,0),(1408,0),(512,1)]:
        label=f'axi-delay-{ratio}-bad{bad}';out=WORK/'b3/unit'/label;out.mkdir(parents=True,exist_ok=True);exe=out/'sim'
        run('B3/unit/'+label+'/build',[VERILATOR,'--cc','--exe','--build','-j','4','--trace','--assert','-Wall','-Wno-fatal','--top-module','axi4_delayer','--Mdir',out,'-o','sim',f'-GRATIO_Q={ratio}',f'-GFAULT_SCALE={bad}',rtl,cpp],inputs=[VERILATOR,rtl,cpp],outputs=[exe],timeout=180,resume=True)
        wave=ROOT/'artifacts/B3/unit'/label/'timing.vcd'
        text,err,_=run('B3/unit/'+label+'/run',[exe,str(ratio),wave],inputs=[exe],outputs=[wave],expected=(1 if bad else 0,))
        assert ('AXI_DELAY_MISMATCH' in err) if bad else ('AXI_DELAY_PASS' in text)
        rows.append({'ratio_q':ratio,'negative':bool(bad),'status':'PASS_BAD_CALIBRATION_REJECTED' if bad else 'PASS','wave':str(wave),'wave_sha256':sha(wave),'result':text.strip(),'evidence':'artifacts/B3/unit/'+label})
    dump(ROOT/'reports/B3_axi_delay_unit.json',{'status':'PASS','runs':rows,'contract':'Read/write timers start at the first upstream VALID, including downstream address wait. Independent read and write lanes;1/4/8-beat reads buffered with per-beat due time ceil((device_response-start)*r), stable responses under upstream backpressure. AW/W accepted in either order, single writes calibrated. Burst writes excluded by an explicit assertion. Device response latency at least one edge; one outstanding transaction per lane.'})
    print('B3_AXI_DELAY_UNIT_PASS')

if __name__=='__main__':main()

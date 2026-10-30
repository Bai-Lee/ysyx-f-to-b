from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    rtl=ROOT/'B/soc/perip/amba/apb_delayer.v';cpp=ROOT/'B/B3/apb_test.cpp';rows=[]
    for ratio,bad in [(256,False),(320,False),(512,False),(1408,False),(512,True)]:
        label='apb-'+str(ratio)+('-bad' if bad else '');out=WORK/'b3/unit'/label;out.mkdir(parents=True,exist_ok=True);exe=out/'sim'
        run('B3/unit/'+label+'/build',[VERILATOR,'--cc','--exe','--build','-j','4','--trace','--assert','-Wall','-Wno-fatal','--top-module','apb_delayer','--Mdir',out,'-o','sim','-GRATIO_Q='+str(ratio),'-GFAULT_EXTRA='+str(int(bad)),rtl,cpp],inputs=[VERILATOR,rtl,cpp],outputs=[exe],timeout=180,resume=True)
        wave=ROOT/'artifacts/B3/unit'/label/'timing.vcd'
        text,err,row=run('B3/unit/'+label+'/run',[exe,str(ratio),wave],inputs=[exe],outputs=[wave],expected=(1 if bad else 0,))
        assert ('APB_DELAY_MISMATCH' in err) if bad else ('APB_CALIBRATION_PASS' in text)
        rows.append({'ratio_q':ratio,'fraction_bits':8,'negative':bad,'status':'PASS_WRONG_DELAY_REJECTED' if bad else 'PASS','wave':str(wave),'wave_sha256':sha(wave),'evidence':'artifacts/B3/unit/'+label})
    dump(ROOT/'reports/B3_apb_unit.json',{'status':'PASS','runs':rows,'contract':'t0 is the sampled APB setup edge, k is device completion distance. Upstream completion is ceil(k*ratio_q/256); extra cycles accumulate ratio_q-256 per device cycle. Error/data are buffered, device completion occurs once, back-to-back setup supported. Unity is exact bypass. Positive ratios1,1.25,2,5.5; variable service1..33 and read/write strobes/error responses.'})
    print('B3_APB_UNIT_PASS')

if __name__=='__main__':main()

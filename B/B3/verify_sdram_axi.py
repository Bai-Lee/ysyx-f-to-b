from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    controller=ROOT/'B/soc/perip/sdram/b_sdram32_axi.v';model=ROOT/'B/soc/perip/sdram/sdram.v';cpp=ROOT/'B/B3/sdram_axi_test.cpp';scope=ROOT/'B/B3/rtl';scope.mkdir(exist_ok=True)
    text=controller.read_text().split('module b_sdram32_axi',1)[1].split('  output wire sdram_clk',1)[0].rstrip().rstrip(',')
    text='module b_sdram_axi_test'+text.replace('POWERUP_CYCLES=10000','POWERUP_CYCLES=10').replace('output reg','output wire')+'\n);\n'
    text+='wire sdram_clk,sdram_cke,sdram_ras,sdram_cas,sdram_we;wire [RANKS-1:0] sdram_cs;wire [12:0] sdram_a;wire [1:0] sdram_ba;wire [3:0] sdram_dqm;wire [31:0] sdram_dq;\n'
    text+='b_sdram32_axi #(.RANKS(RANKS),.POWERUP_CYCLES(POWERUP_CYCLES)) controller(.*);\nsdram memory(.clk(sdram_clk),.cke(sdram_cke),.cs(sdram_cs),.ras(sdram_ras),.cas(sdram_cas),.we(sdram_we),.a(sdram_a),.ba(sdram_ba),.dqm(sdram_dqm),.dq(sdram_dq));\nendmodule\n'
    wrapper=scope/'b_sdram_axi_test.sv';wrapper.write_text(text);rows=[]
    for bad in [False,True]:
        label='sdram-axi'+('-bad-read' if bad else '');out=WORK/'b3/unit'/label;out.mkdir(parents=True,exist_ok=True);exe=out/'sim'
        run('B3/unit/'+label+'/build',[VERILATOR,'--cc','--exe','--build','-j','4','--trace','--assert','-Wall','-Wno-fatal','--top-module','b_sdram_axi_test','--Mdir',out,'-o','sim','-DC5_SDRAM_DQ=32','-DC5_SDRAM_RANKS=2',*(['-DC5_SDRAM_BAD_READ'] if bad else []),wrapper,controller,model,cpp],inputs=[VERILATOR,wrapper,controller,model,cpp],outputs=[exe],timeout=300,resume=True)
        wave=ROOT/'artifacts/B3/unit'/label/'burst.vcd'
        stdout,stderr,_=run('B3/unit/'+label+'/run',[exe,wave],inputs=[exe],outputs=[wave],expected=(1 if bad else 0,),timeout=120)
        assert ('SDRAM_DATA_MISMATCH' in stderr) if bad else ('SDRAM_AXI_PASS writes=768 reads=128 beats=672 distinct_words=256' in stdout)
        rows.append({'negative':bad,'status':'PASS_CORRUPT_READ_REJECTED' if bad else 'PASS','output':stdout.strip(),'wave_sha256':sha(wave),'evidence':'artifacts/B3/unit/'+label})
    dump(ROOT/'reports/B3_sdram_axi_unit.json',{'status':'PASS','runs':rows,'seed':'0x2607b318','scope':'Real fourx16 SDRAM pin models,128MiB address layout; selected boundary words in both ranks/all banks/first and last rows/first and last burst windows. Independent byte-mask model, random AW/W order and response backpressure,1/4/8 beat reads. This boundary suite is not a full-address sweep; full-range CPU patterns remain separate.'})
    print('B3_SDRAM_AXI_UNIT_PASS')

if __name__=='__main__':main()

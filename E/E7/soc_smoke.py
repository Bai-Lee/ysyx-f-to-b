"""Resource-bounded SoC build/small program preflight, not the large regression."""
from common7 import *
from wave_check import clock_periods
import resource,struct
def addi(rd,rs,imm):return ((imm&4095)<<20)|(rs<<15)|(rd<<7)|0x13
def lui(rd,imm):return (imm<<12)|(rd<<7)|0x37
def store(rs,base,imm,byte=False):return (((imm&4095)>>5)<<25)|(rs<<20)|(base<<15)|((0 if byte else 2)<<12)|((imm&31)<<7)|0x23
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
 p=ROOT/'E/E7';builddir=WORK/'build/E7/soc';exe=builddir/'sim'
 run('E7/soc_smoke/link',['make','-C',builddir,'-f','VSimTop.mk','-j1','OPT_FAST=-O3','OPT_SLOW=-O3'],inputs=[builddir/'VSimTop.mk',p/'soc_runner.cpp',p/'rtl/minirv_bus.sv',p/'rtl/ysyx_00000000.sv'],timeout=240,outputs=[exe])
 o,e,r=run('E7/soc_smoke/flash_stub',[exe,'--assert-flash','--max-cycles','100000'],inputs=[exe],expected=(-6,),timeout=20);assert 'EXPECTED_FIRST_FLASH_READ addr=0' in e
 words=[lui(1,0x10000),addi(2,0,0x80),store(2,1,3,True),addi(2,0,13),store(2,1,0,True),addi(2,0,0),store(2,1,1,True),addi(2,0,3),store(2,1,3,True),addi(2,0,65),store(2,1,0,True),lui(1,0x80000),lui(3,0x100),addi(3,3,0x73),store(3,1,0),addi(10,0,0),(1<<15)|0x67]
 image=p/'programs/soc_smoke.bin';image.write_bytes(struct.pack('<'+'I'*len(words),*words));result=ROOT/'artifacts/E7/soc_smoke/boot/result.json'
 rows=[]
 for ratio in [1,3,7]:
  result=ROOT/'artifacts/E7/soc_smoke'/('ratio_'+str(ratio))/'result.json';trace=WORK/('soc_smoke_'+str(ratio)+'.vcd')
  o,e,r=run('E7/soc_smoke/ratio_'+str(ratio),[exe,'--image',image,'--report',result,'--ratio',str(ratio),'--trace',trace,'--trace-cycles','20000','--max-cycles','1000000'],inputs=[exe,image],outputs=[result],timeout=30)
  d=json.loads(result.read_text());assert d['result']=='GOOD_TRAP' and d['serial_matches'] and d['serial_bytes']==1 and d['serial_framing_errors']==0
  assert result.with_suffix('.json.serial.txt').read_text()=='A';wave=clock_periods(trace);assert abs(wave['cpu_to_soc_frequency_ratio']-ratio)<0.001
  shutil.copyfile(trace,result.with_suffix('.vcd'));rows.append({'ratio':ratio,'simulation':d,'clock_wave_check':wave})
 dump(ROOT/'reports/E7_soc_smoke.json',{'status':'PASS_SMOKE','simulation':rows[0]['simulation'],'ratio_tests':rows,'scope':'Actual provided SoC: flash fetch, APB UART initialization and physical TX bit decoding, write ebreak instruction into PSRAM and execute it; complete software/reference comparison at1/3/7clock ratios with parsedwaveforms. Full loader, official test suites, GUI and performance still pending.'})
 print('SOC_REAL_FLASH_PSRAM_UART_SMOKE_PASS',flush=True)
if __name__=='__main__':main()

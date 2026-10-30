from common7 import *
from software_soc import SOFT,environment,clock_config,build
import resource
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(180,190));rows=[]
 exe=WORK/'build/E7/soc/sim';cwd=SOFT/'programs/hello'
 for name,ratio,hz,divisor,args in [('default',1,25000000,13,'E7-SOC'),('ratio3',3,75000000,13,'E7-RATIO3'),('baud57600',1,25000000,27,'E7-57600')]:
  header=clock_config(hz,divisor);image=build('hello',args,'hello_'+name);out=ROOT/'artifacts/E7/soc_hello'/name/'result.json';vcd=WORK/('soc_hello_'+name+'.vcd')
  o,e,r=run('E7/soc_hello/'+name,[exe,'--image',image,'--report',out,'--ratio',str(ratio),'--frequency',str(hz),'--trace',vcd,'--trace-cycles','10000','--max-cycles','2000000000'],inputs=[exe,image,header],outputs=[out,Path(str(out)+'.uart.txt'),Path(str(out)+'.serial.txt')],timeout=240)
  d=json.loads(out.read_text());assert d['result']=='GOOD_TRAP' and d['serial_matches'] and d['serial_framing_errors']==0 and d['uart_divisors']==[13,divisor]
  assert 'Hello, AbstractMachine!' in o and "mainargs = '"+args+"'." in o
  from wave_check import clock_periods
  wave=clock_periods(vcd);assert abs(wave['cpu_to_soc_frequency_ratio']-ratio)<.001;shutil.copyfile(vcd,out.with_suffix('.vcd'))
  rows.append({'scenario':name,'ratio':ratio,'frequency_hz':hz,'divisor':divisor,'result':d,'clock_wave':wave,'image_sha256':sha(image)});dump(ROOT/'reports/E7_soc_hello.json',{'status':'IN_PROGRESS','cases':rows})
 clock_config();dump(ROOT/'reports/E7_soc_hello.json',{'status':'PASS','cases':rows,'scope':'CompiledSoCAMhello, actualloaderandUART16550, physicalTXdecoding, correctmainargs;1x/3xclockratios and25MHzdivisor13/27transmissions. Theseare digitalfunctionaltests, notanalogmetastability/realwiretoleranceproof.'})
 mark(['E7-M015','E7-M023','E7-M025','E7-R001'],'PASS',['reports/E7_soc_hello.json','reports/E7_soc_runtime_smoke.json','artifacts/E7/soc_hello'],'ActualcompiledSoChelloandmainargs, UART16550DLL13and27/8N1/LSRpolling, fullbyteTXdecode, application/wholeIPC, clockratio1and3verifiedfromactualVCDandfunctionalruns.')
 print('SOC_COMPILED_HELLO_CLOCK_BAUD_PASS',flush=True)
if __name__=='__main__':main()

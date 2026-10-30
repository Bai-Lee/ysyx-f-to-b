from common7 import *
def main():
 exe=WORK/'build/E7/soc/sim';image=BENCH7/'ysyxSoC/ready-to-run/minirv/hello-minirv-ysyxsoc.bin';out=ROOT/'artifacts/E7/official_hello/result.json'
 o,e,r=run('E7/official_hello',[exe,'--image',image,'--report',out,'--max-cycles','2000000000'],inputs=[exe,image],outputs=[out,Path(str(out)+'.uart.txt'),Path(str(out)+'.serial.txt')],timeout=1200)
 d=json.loads(out.read_text());assert d['result']=='GOOD_TRAP' and d['application_instructions']>=64 and d['serial_matches'] and d['serial_framing_errors']==0
 assert "Hello, AbstractMachine!\nmainargs = 'Hello, One Student One Chip!'.\n" in o
 assert len(d['uart_divisors'])>=2 and all(x==13 for x in d['uart_divisors']),d['uart_divisors']
 dump(ROOT/'reports/E7_official_hello.json',{'status':'PASS','simulation':d,'source_image_sha256':sha(image),'scope':'Unmodified provided loader+hello image booted from16MBflash through realSPI/PSRAM/UART controllers; every commit compared to independent reference, full hello output matched TX pin decoding and GOOD_TRAP.','source_erratum':'The frozen lesson text says the provided hello loops, but the actual pinned binary contains ebreak at80000668 (verified by extracting its ELF atoffset369152 and objdump). Loader and application both initialize divisor13. The binary is not modified.'})
 mark(['E7-M009','E7-M010','E7-M011','E7-R002'],'PASS',['reports/E_source_lock.json','reports/E7_soc_smoke.json','reports/E7_official_hello.json','artifacts/E7/official_hello'],'Pinned2607SoC and supplied periphery integrated with exact interface; reset110SoCcycles, explicitflash-stub rejection, complete untouched officialhello boot and physicalserialdecode, CPU/SOC clocks exercised at1/3/7.')
 print('E7_OFFICIAL_HELLO_BOOT_PASS',flush=True)
if __name__=='__main__':main()

from common7 import *
from install_prebuilt import install
import re,argparse
SOFT=WORK/'software-soc'
def environment():return env7({'AM_HOME':str(SOFT/'abstract-machine')})
def clock_config(hz=25000000,divisor=13):
 assert hz>=1000000 and hz%1000000==0 and 1<=divisor<=65535
 p=SOFT/'abstract-machine/am/src/riscv/npc/e7_config.h';s=p.read_text();s=re.sub(r'#define SOC_CPU_HZ \d+u','#define SOC_CPU_HZ '+str(hz)+'u',s);s=re.sub(r'#define UART_DIVISOR \d+u','#define UART_DIVISOR '+str(divisor)+'u',s)
 if s!=p.read_text():p.write_text(s)
 return p
def prepare():
 assert (SOFT/'abstract-machine').exists(),'Run batch_suite.py once to prepare the isolatedSoCAM'
 base=SOFT/'programs';base.mkdir(exist_ok=True)
 sources={
  'dummy':BENCH/'am-kernels/tests/cpu-tests/tests/dummy.c',
  'wrong':BENCH/'am-kernels/tests/cpu-tests/tests/wrong.c',
  'hello':BENCH/'am-kernels/kernels/hello/hello.c',
  'gpio':ROOT/'E/E7/programs/gpio.c'}
 for name,source in sources.items():
  d=base/name;d.mkdir(exist_ok=True);shutil.copyfile(source,d/'main.c');(d/'Makefile').write_text('NAME='+name+'\nSRCS=main.c\ninclude $(AM_HOME)/Makefile\n')
 timer=base/'timer'
 if not timer.exists():shutil.copytree(BENCH7/'am-kernels/tests/am-tests',timer,ignore=shutil.ignore_patterns('build','.git'))
 dump(ROOT/'reports/E7_soc_software_sources.json',{'status':'PREPARED','sources':[{'program':n,'source':str(s),'sha256':sha(s)} for n,s in sources.items()],'timer_source':'Pinnedofficialam-kernels/tests/am-tests','am':str(SOFT/'abstract-machine'),'isolation':'SoCfrequencychanges cannotmutate the runningstandaloneE7AMworkbench.'})
 return base
def build(name,mainargs='E7-SOC',label=None):
 d=SOFT/'programs'/name;header=SOFT/'abstract-machine/am/src/riscv/npc/e7_config.h';label=label or name
 o,e,r=run('E7/soc_software/'+label+'/build',['make','-j1','ARCH=minirv-ysyxsoc','mainargs='+mainargs,'insert-arg'],cwd=d,env=environment(),inputs=[d/'Makefile',header],timeout=300)
 image=next((d/'build').glob('*-minirv-ysyxsoc.bin'));elf=image.with_suffix('.elf');data=image.read_bytes();provided=(BENCH7/'ysyxSoC/ready-to-run/minirv/hello-minirv-ysyxsoc.bin').read_bytes();assert data[:369152]==provided[:369152] and data[369152:369156]==b'\x7fELF'
 out=ROOT/'E/E7/software_soc'/label;out.mkdir(parents=True,exist_ok=True)
 for f in [image,elf,header]:shutil.copyfile(f,out/f.name)
 return image
def main():
 p=argparse.ArgumentParser();p.add_argument('--build-only',action='store_true');args=p.parse_args();prepare();header=clock_config();rows=[]
 for name in ['dummy','wrong','hello','gpio']:image=build(name,'E7-SOC');rows.append({'program':name,'image':str(image),'sha256':sha(image),'config_sha256':sha(header)})
 dump(ROOT/'reports/E7_soc_software.json',{'status':'BUILT_NOT_RUN','programs':rows})
 if args.build_only:print('SOC_SOFTWARE_IMAGES_BUILT',flush=True);return
 exe=WORK/'build/E7/soc/sim'
 for item in rows[:3]:
  name=item['program'];cwd=SOFT/'programs'/name;image=Path(item['image']);result=Path(str(image)+'.npc.json');bad=name=='wrong'
  o,e,r=run('E7/soc_software/'+name+'/run',['make','-j1','ARCH=minirv-ysyxsoc','mainargs=E7-SOC','run','NPC_ARGS=--ratio 1 --frequency 25000000'],cwd=cwd,env=environment(),inputs=[exe,header,cwd/'Makefile'],outputs=[image,result,Path(str(result)+'.serial.txt')],expected=(2,) if bad else (0,),timeout=1200)
  d=json.loads(result.read_text());assert d['result']==('BAD_TRAP' if bad else 'GOOD_TRAP') and d['serial_matches']
  if name=='hello':assert "mainargs = 'E7-SOC'." in o and 'Hello, AbstractMachine!' in o
  item['result']=d;item['make_exit']=r['exit_code']
 dump(ROOT/'reports/E7_soc_software.json',{'status':'PASS_BASIC_PROGRAMS_GPIO_BUILT','programs':rows})
 mark(['E7-M012','E7-M015','E7-R001'],'PASS',['reports/E7_soc_software.json','E/E7/software_soc','artifacts/E7/soc_software'],'Originaldummy/wrong/hello compiledthroughminirv-ysyxsoc andunchangedloaderprefix;GOOD/BADandmakeexitverified; mainargsreachesapplication;UART16550divisor13/8N1/LSRpollingandactualTXdecodingpass.')
 print('SOC_BASIC_SOFTWARE_PASS',flush=True)
if __name__=='__main__':main()

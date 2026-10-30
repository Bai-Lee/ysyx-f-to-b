from common7 import *
from software_soc import SOFT,environment
import resource
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(40,45));rows=[]
 for name in ['dummy','wrong']:
  cwd=SOFT/'programs'/name;image=cwd/'build'/(name+'-minirv-ysyxsoc.bin');result=Path(str(image)+'.npc.json')
  o,e,r=run('E7/soc_runtime_smoke/'+name,['make','-j1','ARCH=minirv-ysyxsoc','mainargs=E7-SOC','run','NPC_ARGS=--ratio 1 --frequency 25000000 --max-cycles 20000000'],cwd=cwd,env=environment(),inputs=[image,SOFT/'abstract-machine/am/src/riscv/npc/trm.c'],outputs=[result],expected=(2,) if name=='wrong' else (0,),timeout=60)
  d=json.loads(result.read_text());assert d['result']==('BAD_TRAP' if name=='wrong' else 'GOOD_TRAP') and d['serial_matches'];assert len(d['uart_divisors'])==2 and all(x==13 for x in d['uart_divisors'])
  rows.append({'program':name,'make_exit':r['exit_code'],'result':d})
 dump(ROOT/'reports/E7_soc_runtime_smoke.json',{'status':'PASS','programs':rows,'scope':'ActualAM-builtSoCdummyandwrong; bothloaderandapplicationUARTinitializationobserved; normal/failurestatuspropagatedthroughmake.'})
 print('SOC_RUNTIME_DUMMY_WRONG_PASS',flush=True)
if __name__=='__main__':main()

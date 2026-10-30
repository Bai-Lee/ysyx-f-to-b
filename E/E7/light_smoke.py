"""Bounded light check while E6 runs: <=512MiB address space, <=30 CPU seconds/process.
Large bus regressions and SoC compilation remain serial heavy work.
"""
from common7 import *
import resource
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024))
 resource.setrlimit(resource.RLIMIT_CPU,(30,30))
 p=ROOT/'E/E7';rows=[]
 for name,mode in [('valid',3),('ifu',1),('lsu',2),('random',3)]:
  run('E7/light_smoke/build_'+name,['python3',p/'build.py','--mode',name],inputs=[p/'build.py',p/'rtl/minirv_bus.sv',p/'bus_runner.cpp'],timeout=90)
  exe=WORK/'build/E7'/name/'sim';image=BENCH/'am-kernels/kernels/hello/build/hello-minirv-npc.bin'
  for delay in ([5,10,20,0] if name=='random' else [1]):
   result=ROOT/'artifacts/E7/light_smoke'/('hello_'+name+'_'+str(delay))/'result.json';event=result.with_suffix('.csv');vcd=WORK/('smoke_'+name+'_'+str(delay)+'.vcd')
   o,e,r=run('E7/light_smoke/hello_'+name+'_'+str(delay),[exe,'--image',image,'--mode',str(mode),'--report',result,'--events',event,'--trace',vcd,'--max-cycles','1000000','--uart-random',*(['--random','--seed','260707'] if delay==0 else ['--delay',str(delay)])],inputs=[exe,image],outputs=[result,event],timeout=30)
   d=json.loads(result.read_text());assert 'Hello, AbstractMachine!' in o and d['result']=='GOOD_TRAP';shutil.copyfile(vcd,result.with_suffix('.vcd'))
   if name=='ifu':assert d['ipc']==.5
   rows.append({'name':name,'delay':delay,'result':d})
 dump(ROOT/'reports/E7_bus_smoke.json',{'status':'PASS_SMOKE','cases':rows,'limits':'One hello program; full official regression and train table remain separate pending work.'})
 run('E7/light_smoke/csr',['python3',p/'csr_tests.py'],inputs=[p/'csr_tests.py'],timeout=30)
 print('E7_LIGHT_SMOKE_PASS',flush=True)
if __name__=='__main__':main()

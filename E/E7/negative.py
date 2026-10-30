from common7 import *
import resource
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
 p=ROOT/'E/E7';run('E7/negative/build',['python3',p/'build.py','--mode','valid'],inputs=[p/'build.py',p/'bus_runner.cpp'],timeout=120)
 exe=WORK/'build/E7/valid/sim';image=BENCH/'am-kernels/kernels/hello/build/hello-minirv-npc.bin';rows=[]
 for name,flag in [('read_corruption','--inject-read-bit'),('double_store','--inject-double-store'),('positive','')]:
  out=ROOT/'artifacts/E7/negative'/name/'result.json';o,e,r=run('E7/negative/'+name,[exe,'--image',image,'--report',out,'--uart-random','--max-cycles','1000000',*([flag] if flag else [])],inputs=[exe,image],outputs=[out],expected=(1,) if flag else (0,),timeout=20)
  d=json.loads(out.read_text());assert d['result']==('DIFF_FAIL' if flag else 'GOOD_TRAP');rows.append({'case':name,'result':d,'diagnostic':e})
 dump(ROOT/'reports/E7_bus_negative.json',{'status':'PASS','cases':rows,'scope':'Faults injected only by explicit test-only harness flags. Wrong RAM read and duplicate same-value store both rejected; unchanged positive path still passes. This does not change the RTL or relax any reference comparison.'})
 print('E7_BUS_NEGATIVE_CONTROLS_PASS',flush=True)
if __name__=='__main__':main()

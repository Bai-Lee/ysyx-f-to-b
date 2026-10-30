from pathlib import Path
import sys,csv
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 rt=ROOT/'E/runtime';p=ROOT/'E/E7';sources=[ROOT/'E/E5/rtl/minirv_decode.sv',ROOT/'E/E5/rtl/minirv_regfile.sv',p/'rtl/minirv_bus.sv'];cpp=p/'bus_runner.cpp';rows=[]
 hello=BENCH/'am-kernels/kernels/hello/build/hello-minirv-npc.bin'
 cases=[]
 for folder in [BENCH/'riscv-tests/build',BENCH/'am-kernels/tests/cpu-tests/build']:
  cases.extend((f.parent.parent.name+'_'+f.stem,f) for f in sorted(folder.glob('*-minirv-npc.bin')) if not f.name.startswith('wrong-'))
 for name,mode in [('ifu',1),('lsu',2),('valid',3),('random',3)]:
  run('E7/bus_'+name+'/prepare',['python3',p/'build.py','--mode',name],inputs=[p/'build.py',*sources,cpp],timeout=300)
  exe=WORK/'build/E7'/name/'sim'
  delays=[1,5,10,20] if name=='valid' else [0] if name=='random' else [1]
  for delay in delays:
   tag='E7/bus_'+name+'/delay_'+str(delay);dest=ROOT/'artifacts'/tag;dest.mkdir(parents=True,exist_ok=True)
   out=dest/'hello.json';event=dest/'hello.csv';vcd=WORK/('hello_'+name+'_'+str(delay)+'.vcd')
   args=[exe,'--image',hello,'--mode',str(mode),'--report',out,'--uart-random','--events',event,'--trace',vcd]+(['--random','--seed','260707'] if delay==0 else ['--delay',str(delay)])
   o,e,r=run(tag+'/hello',args,inputs=[exe,hello],outputs=[out,event],timeout=300);data=json.loads(out.read_text());assert data['result']=='GOOD_TRAP'
   shutil.copyfile(vcd,dest/'hello.vcd');trace=list(csv.DictReader(event.open()));assert int(trace[-1]['cycle'])==data['cycles']
   if name=='ifu':assert abs(data['ipc']-.5)<1e-12
   if name=='lsu':assert data['ipc']<.5
   # No duplicate request while an IFU transaction is outstanding; CSV plus VCD provide independent cycle evidence.
   pending=False;last_commit=0;instruction_latencies=[]
   for t in trace:
    if t['ifu_resp']=='1':assert pending;pending=False
    if t['ifu_req']=='1':assert not pending;pending=True
    if t['commit']=='1':
     cycle=int(t['cycle']);latency=cycle-last_commit;last_commit=cycle;opcode=int(t['commit_inst'],16)&127
     if name=='ifu':assert latency==2
     if name=='lsu':assert latency==(3 if opcode==3 else 2)
     if name=='valid' and delay==1:assert latency==(3 if opcode in [3,35] else 2)
     instruction_latencies.append(latency)
   assert not pending
   rec={'mode':name,'delay':delay,'hello':data,'instruction_latency_min':min(instruction_latencies),'instruction_latency_max':max(instruction_latencies),'waveform_sha256':sha(dest/'hello.vcd'),'programs':[]}
   for test,image in cases:
    result=dest/(test+'.json');args=[exe,'--image',image,'--mode',str(mode),'--report',result,'--uart-random']+(['--random','--seed','260707'] if delay==0 else ['--delay',str(delay)])
    o,e,r=run(tag+'/programs/'+test,args,inputs=[exe,image],outputs=[result],timeout=600);d=json.loads(result.read_text());assert d['result']=='GOOD_TRAP';rec['programs'].append({'test':test,'result':d,'image_sha256':sha(image)})
   rows.append(rec);dump(ROOT/'reports/E7_bus_tests.json',{'status':'IN_PROGRESS','records':rows})
 dump(ROOT/'reports/E7_bus_tests.json',{'status':'PASS','records':rows,'scope':'One outstanding transaction per port; fixed 1/5/10/20 and LFSR1..31 delays, independent IFU/LSU request-delay LFSRs. Directed/random simulation is not an unbounded proof.'})
 print('E7_BUS_TESTS_PASS',flush=True)
if __name__=='__main__':main()

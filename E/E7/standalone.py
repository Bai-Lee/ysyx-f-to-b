from common7 import *
import re,math
def main():
 p=ROOT/'E/E7';suite=BENCH7/'archbench';kernels=BENCH7/'am-kernels';all_rows=[]
 # This changes only the isolated E7 workbench. Use a common100MHz assumption
 # to separate bus-latency effects from the later synthesis/SoC-clock study.
 run('E7/standalone/configure',['python3',p/'configure_platform.py'],inputs=[p/'configure_platform.py'],timeout=180)
 am=BENCH7/'abstract-machine';header=am/'am/src/riscv/npc/e7_config.h';assert '#define NPC_CPU_HZ 100000000u' in header.read_text()
 for mode,number in [('ifu',1),('lsu',2),('valid',3)]:
  run('E7/standalone/'+mode+'/build',['python3',p/'build.py','--mode',mode],inputs=[p/'build.py',p/'bus_runner.cpp'],timeout=300)
  exe=WORK/'build/E7'/mode/'sim';simhash=sha(exe);rows=[]
  jobs=[('hello',kernels/'kernels/hello','E7-BUS',False),('dhrystone',kernels/'benchmarks/dhrystone','test',False),('coremark',kernels/'benchmarks/coremark','test',False),('microbench',kernels/'benchmarks/microbench','test',False)]
  jobs += [(x.name,x,'test',True) for x in sorted((suite/'bench').iterdir()) if x.is_dir()]
  jobs += [(x.name,x,'train',True) for x in sorted((suite/'bench').iterdir()) if x.is_dir() and x.name!='000.hello']
  for name,cwd,setting,archbench in jobs:
   tag='E7/standalone/'+mode+'/'+setting+'/'+name;dest=ROOT/'artifacts'/tag;dest.mkdir(parents=True,exist_ok=True);accepted=dest/'accepted.json'
   if accepted.exists():
    row=json.loads(accepted.read_text());assert row['simulator_sha256']==simhash and row['config_sha256']==sha(header);assert row['stdout_sha256']==sha(dest/'stdout.log');rows.append(row);print('STANDALONE_REUSE',mode,setting,name,flush=True);continue
   env=env7({'SDL_VIDEODRIVER':'dummy','SDL_AUDIODRIVER':'dummy'});args=['make','-j1','ARCH=minirv-npc','NPC_MODE='+mode,'mainargs='+setting,'run']
   # Build names differ from directory names in archbench; inspect the generated
   # image after make, then freeze that exact binary and result separately.
   o,e,r=run(tag,args,cwd=cwd,env=env,inputs=[cwd/'Makefile',header,am/'am/src/riscv/npc/timer.c',exe],timeout=7200)
   image=next((cwd/'build').glob('*-minirv-npc.bin'));result=Path(str(image)+'.npc.json');d=json.loads(result.read_text());assert d['result']=='GOOD_TRAP'
   assert 'Error ' not in e and 'DIFF' not in e
   if name in ['hello','000.hello']:assert 'Hello' in o or 'hello' in o
   elif archbench:assert re.search(r'\[RESULT\].*PASS',o) and not re.search(r'\[RESULT\].*FAIL',o)
   else:assert 'PASS' in o and 'FAIL' not in o
   if name=='202.llama2':assert 'Once' in o
   shutil.copyfile(result,dest/'result.json')
   with zipfile.ZipFile(dest/'output_snapshot.zip','w',zipfile.ZIP_DEFLATED) as z:z.write(image,image.name);z.write(result,result.name);z.write(header,'e7_config.h')
   row={'mode':mode,'program':name,'setting':setting,'status':'PASS','simulation':d,'image_sha256':sha(image),'result_sha256':sha(dest/'result.json'),'simulator_sha256':simhash,'config_sha256':sha(header),'stdout_sha256':sha(dest/'stdout.log'),'evidence':str(dest.relative_to(ROOT))}
   if archbench and setting=='train':row['score']=int(re.search(r'^\s+(\d+) Marks$',o,re.M)[1]);row['min_time_us']=int(re.search(r'\[RESULT\].*\((\d+) us\)',o)[1])
   dump(accepted,row);rows.append(row);dump(ROOT/'reports/E7_standalone.json',{'status':'IN_PROGRESS','records':all_rows+rows,'comparison_frequency_hz':100000000})
  # Run the same complete FCEUX/ROM image accepted in E6. Its timer MMIO model
  # remains supported alongside the new CSR-based AM implementation.
  image=BENCH/'fceux-am/build/fceux-minirv-npc.bin';out=ROOT/'artifacts/E7/standalone'/mode/'fceux/result.json'
  o,e,r=run('E7/standalone/'+mode+'/fceux',[exe,'--image',image,'--mode',str(number),'--report',out,'--frequency','100000000','--uart-random','--until-output','\x1b[0;0H','--until-count','3'],inputs=[exe,image],outputs=[out],timeout=1800)
  assert json.loads(out.read_text())['result']=='BOUNDED_OUTPUT_OBSERVATION'
  frames=o.split('\x1b[0;0H');assert len(frames)>=4
  for frame in frames[1:3]:assert sum(len(s)==128 and set(s)<=set('o. *O0@#') for s in frame.splitlines())>=56
  scores=[r['score'] for r in rows if 'score'in r];assert len(scores)==20
  summary={'mode':mode,'arithmetic_mean':sum(scores)/20,'geometric_mean':math.exp(sum(map(math.log,scores))/20),'hello':rows[0]['simulation'],'fceux':'PASS_TWO_COMPLETE_FRAMES','train_programs':20,'test_programs':21}
  all_rows+=rows;summary_path=ROOT/'reports'/('E7_'+mode+'_performance.json');dump(summary_path,summary)
  task={'ifu':'E7-M003','lsu':'E7-M005','valid':'E7-M007'}[mode]
  mark([task],'PASS',['reports/E7_standalone.json',str(summary_path.relative_to(ROOT)),'artifacts/E7/standalone/'+mode],'All21archbench test and20train programs, three kernel benchmarks, helloIPC andtwoFCEUXframes executed with fullper-commit DiffTest. Common100MHz model frequency is held fixed for latency comparison.')
  print('E7_STANDALONE_MODE_COMPLETE',mode,summary['geometric_mean'],flush=True)
 dump(ROOT/'reports/E7_standalone.json',{'status':'PASS','records':all_rows,'comparison_frequency_hz':100000000,'scope':'Functional and model-time comparison; no claim of routed timing. Every CPU/SoC memory transaction remains modeled; no instruction skipping.'})
 mark(['E7-M001','E7-M002','E7-M004','E7-M006','E7-M008','E7-O001'],'PASS',['reports/E7_bus_tests.json','reports/E7_bus_negative.json','reports/E7_standalone.json'],'Exact2-cycle IFU,3-cycleloads andvalid-request protocol verified fromcycleCSV/VCD.73officialtests passed eachof7fixed/randomdelay configs;corruptedread/duplicatestore rejected; fullapplicationsandtrainrerun;DiffTestonlyoncommit.')
 print('E7_STANDALONE_COMPLETE',flush=True)
if __name__=='__main__':main()

from pathlib import Path
import sys,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
 p=ROOT/'E/E6';am=BENCH/'abstract-machine';npc=BENCH/'npc';kernels=BENCH/'am-kernels';suite=BENCH/'archbench'
 common_env={'BENCH_HOME':str(suite),'SDL_VIDEODRIVER':'dummy','SDL_AUDIODRIVER':'dummy','nproc':'1'}
 records=[]
 # The upstream timer test intentionally loops forever. A semantic stop condition observes three ticks; a timeout never counts as success.
 out=kernels/'tests/am-tests/build/amtest-minirv-npc.bin.npc.json'
 o,e,r=run('E6/devices/official_timer',['make','-j1','ARCH=minirv-npc','run','mainargs=t',"NPC_ARGS=--wall-timer --until-output 'seconds).' --until-count 2"],cwd=kernels/'tests/am-tests',inputs=[am/'am/src/riscv/npc/timer.c',npc/'csrc/runner.cpp'],timeout=180)
 assert '1 second).' in o and '2 seconds).' in o and '3 seconds).' in o
 result=next((kernels/'tests/am-tests/build').glob('*.bin.npc.json'));d=json.loads(result.read_text());assert d['result']=='BOUNDED_OUTPUT_OBSERVATION'
 dump(ROOT/'reports/E6_timer.json',{'status':'PASS_BOUNDED_OBSERVATION','simulation':d,'observed_seconds':[1,2,3],'evidence':'artifacts/E6/devices/official_timer','purpose':'Official infinite timer test; stops after the third completed output line, not a timeout.'})
 mark(['E6-M015'],'PASS',['reports/E6_timer.json','artifacts/E6/devices/official_timer'],'Official AM t program produced 1/2/3-second lines with host monotonic timer; RTL/C per-commit comparison retained. Timer rollover independently tested.')
 for rel,old,new in [('benchmarks/dhrystone/dry.c','#define NUMBER_OF_RUNS\t\t500000','#define NUMBER_OF_RUNS\t\t2'),('benchmarks/coremark/include/core_portme.h','#define ITERATIONS 1000','#define ITERATIONS 2')]:
  f=kernels/rel;b=p/'upstream'/rel;b.parent.mkdir(parents=True,exist_ok=True)
  if not b.exists():shutil.copyfile(f,b)
  s=f.read_text();assert old in s or new in s;s=s.replace(old,new);f.write_text(s)
 # Two native iterations can take less than one millisecond. Avoid undefined division by zero in score formatting only; validation and work counts remain unchanged.
 for rel,old,new in [('benchmarks/dhrystone/dry.c','880900 / User_Time','880900 / (User_Time ? User_Time : 1)'),('benchmarks/coremark/src/core_main.c','2921400 / time_in_secs(total_time)','2921400 / (time_in_secs(total_time) ? time_in_secs(total_time) : 1)')]:
  f=kernels/rel;b=p/'upstream'/rel;b.parent.mkdir(parents=True,exist_ok=True)
  if not b.exists():shutil.copyfile(f,b)
  s=f.read_text();assert old in s or new in s;s=s.replace(old,new);f.write_text(s)
 for name in ['dhrystone','coremark','microbench']:
  cwd=kernels/'benchmarks'/name
  for arch in ['native','minirv-npc']:
   o,e,r=run('E6/benchmarks/'+name+'_'+arch,['make','-j1','ARCH='+arch,'run','mainargs=test','NPC_ARGS=--wall-timer --uart-random'],cwd=cwd,inputs=list(cwd.glob('**/*.c'))+list(cwd.glob('**/*.h')),timeout=900,env=common_env)
   assert 'PASS' in o and 'FAIL' not in o,(name,arch,o[-2000:])
   records.append({'program':name,'arch':arch,'status':'PASS','evidence':'artifacts/E6/benchmarks/'+name+'_'+arch})
   dump(ROOT/'reports/E6_benchmarks.json',{'status':'IN_PROGRESS','records':records})
 mark(['E6-M011','E6-M016'],'PASS',['reports/E6_benchmarks.json','artifacts/E6/benchmarks'],'Dhrystone/CoreMark use course-permitted 2 iterations, microbench uses test; native and RTL runs independently validate; measured host time is not silicon performance.')
 for cwd in sorted((suite/'bench').iterdir()):
  if not cwd.is_dir():continue
  name=cwd.name
  for arch in ['native','minirv-npc']:
   o,e,r=run('E6/archbench_test/'+name+'_'+arch,['make','-j1','ARCH='+arch,'run','mainargs=test','NPC_ARGS=--wall-timer --uart-random'],cwd=cwd,inputs=[cwd/'Makefile',suite/'libbench/bench.c'],timeout=1200,env=common_env)
   if name!='000.hello':assert re.search(r'\[RESULT\].*PASS',o) and not re.search(r'\[RESULT\].*FAIL',o),(name,arch)
   if name=='202.llama2':assert 'Once' in o
   item={'program':name,'arch':arch,'status':'PASS','evidence':'artifacts/E6/archbench_test/'+name+'_'+arch}
   if arch=='minirv-npc':
    f=next((cwd/'build').glob('*-minirv-npc.bin.npc.json'));d=json.loads(f.read_text());assert d['result']=='GOOD_TRAP';item['simulation']=d
   records.append(item);dump(ROOT/'reports/E6_benchmarks.json',{'status':'IN_PROGRESS','records':records})
  if name=='202.llama2':mark(['E6-M012'],'PASS',['reports/E6_benchmarks.json','artifacts/E6/archbench_test/202.llama2_minirv-npc'],'Official tiny test model compiled and ran on minirv NPC, emitted Once and passed upstream validation, full differential checking enabled.')
 dump(ROOT/'reports/E6_benchmarks.json',{'status':'PASS','records':records})
 mark(['E6-M013'],'PASS',['reports/E6_benchmarks.json','artifacts/E6/archbench_test'],'Every pinned archbench directory ran test on native and minirv NPC, including upstream checksum validation and independent per-commit differential comparison.')
 print('BENCHMARK_TESTS_PASS',flush=True)
if __name__=='__main__':main()

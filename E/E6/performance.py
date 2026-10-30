"""Serial per-program checkpoints, retaining the upstream workloads/scoring.
The interrupted upstream run.sh attempt has no parent exit record; it is not a
completed suite. Each program here saves its own accepted result immediately.
"""
from pathlib import Path
import sys,re,math,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=['wall','100MHz','1000MHz','synthesis','all'],default='all');option=parser.parse_args()
 suite=BENCH/'archbench';names=sorted(p.name for p in (suite/'bench').iterdir() if p.is_dir() and p.name!='000.hello');freq=json.loads((ROOT/'reports/E6_synthesis.json').read_text())['frequency_hz'];sim=BENCH/'npc/build/sim';simhash=sha(sim)
 modes=[('wall','--wall-timer --uart-random','E6-M018'),('100MHz','--frequency 100000000 --uart-random','E6-M019'),('1000MHz','--frequency 1000000000 --uart-random','E6-M020'),('synthesis','--frequency '+str(freq)+' --uart-random','E6-M022')]
 reports=[];aggregate=ROOT/'reports/E6_performance.json'
 if aggregate.exists():reports=json.loads(aggregate.read_text())['runs']
 for mode,args,task in modes:
  if option.mode!='all' and mode!=option.mode:continue
  rows=[]
  for name in names:
   tag='E6/performance/'+mode+'/programs/'+name;dest=ROOT/'artifacts'/tag;dest.mkdir(parents=True,exist_ok=True);checkpoint=dest/'accepted.json'
   if checkpoint.exists():
    item=json.loads(checkpoint.read_text());assert item['simulator_sha256']==simhash
    assert sha(dest/'stdout.log')==item['stdout_sha256'] and sha(dest/'result.json')==item['result_sha256'];rows.append(item);print('PERFORMANCE_REUSE',mode,name,flush=True);continue
   cwd=suite/'bench'/name;result=next((cwd/'build').glob('*-minirv-npc.bin.npc.json'));image=next((cwd/'build').glob('*-minirv-npc.bin'))
   env={'BENCH_HOME':str(suite),'nproc':'1','NPC_ARGS':args+' --max-cycles 100000000000'}
   o,e,r=run(tag,['make','-j1','ARCH=minirv-npc','mainargs=train','run'],cwd=cwd,env=env,inputs=[cwd/'Makefile',suite/'libbench/bench.c',sim,BENCH/'abstract-machine/am/src/riscv/npc/timer.c'],outputs=[result,image],timeout=7200)
   assert re.search(r'\[RESULT\].*PASS',o) and not re.search(r'\[RESULT\].*FAIL',o),name
   assert 'GOOD_TRAP' in e and 'Error ' not in e,name
   score=int(re.search(r'^\s+(\d+) Marks$',o,re.M)[1]);time_us=int(re.search(r'\[RESULT\].*\((\d+) us\)',o)[1]);d=json.loads(result.read_text());assert d['result']=='GOOD_TRAP' and d['ebreak_calls']==1
   shutil.copyfile(result,dest/'result.json')
   item={'program':name,'mode':mode,'status':'PASS','score':score,'min_time_us':time_us,'simulation':d,'stdout_sha256':sha(dest/'stdout.log'),'result_sha256':sha(dest/'result.json'),'image_sha256':sha(image),'simulator_sha256':simhash,'evidence':str(dest.relative_to(ROOT))}
   dump(checkpoint,item);rows.append(item)
   report={'mode':mode,'status':'IN_PROGRESS','rows':rows};reports=[x for x in reports if x['mode']!=mode]+[report];dump(aggregate,{'status':'IN_PROGRESS','runs':reports})
  values=[x['score'] for x in rows];arithmetic=sum(values)/len(values);geometric=math.exp(sum(math.log(x) for x in values)/len(values))
  import numpy as np
  assert abs(arithmetic-float(np.mean(values)))<1e-8 and abs(geometric-float(np.exp(np.log(values).mean())))<1e-8
  record={'mode':mode,'status':'PASS','arithmetic_mean':arithmetic,'geometric_mean':geometric,'rows':rows,'simulator_sha256':simhash,'interpretation':'Host-simulation throughput only' if mode=='wall' else 'Modeled CPU time; frequency assumed' if mode!='synthesis' else 'Pre-layout synthesis-frequency estimate, not physical signoff'}
  reports=[x for x in reports if x['mode']!=mode]+[record];dump(aggregate,{'status':'PASS' if len(reports)==4 and all(x['status']=='PASS' for x in reports) else 'IN_PROGRESS','runs':reports})
  mark([task],'PASS',['reports/E6_performance.json','artifacts/E6/performance/'+mode],f'All {len(names)} official train workloads ran serially with full per-commit differential checks. Per-program process exits, upstream validators, input/output snapshots and arithmetic/geometric means audited. Original upstream script attempt retained separately as interrupted.')
  print('PERFORMANCE_MODE_DONE',mode,geometric,flush=True)
 if len(reports)==4 and all(x['status']=='PASS' for x in reports):
  modes={x['mode']:x for x in reports};ratios=[]
  for a,b in zip(modes['100MHz']['rows'],modes['1000MHz']['rows']):
   assert a['program']==b['program']
   ratio=a['min_time_us']/b['min_time_us']
   # Upstream genann prints subtest times and llama2 prints tokens/s inside the
   # timed region. Changing frequency therefore changes printf/division/UART
   # work too; equal instruction counts or a fixed20us absolute error is not
   # an applicable invariant. Require near10x model time, then verify score
   # rounding independently from the measured time ratio.
   assert abs(ratio/10-1)<0.001,(a['program'],ratio)
   low=1 if a['score']==1 else max(1,math.floor(a['score']*ratio)-1)
   high=max(1,math.ceil((a['score']+1)*ratio))
   assert low<=b['score']<=high,(a['program'],a['score'],b['score'],ratio)
   ratios.append({'program':a['program'],'score_ratio':b['score']/a['score'],'time_ratio':ratio,'total_instruction_difference':b['simulation']['instructions']-a['simulation']['instructions'],'score_rounding_interval_1000MHz':[low,high]})
  d=json.loads(aggregate.read_text());d['1000_vs_100_MHz_ratios']=ratios;d['scaling_check']={'status':'PASS','relative_time_tolerance':0.001,'observed_max_relative_time_error':max(abs(r['time_ratio']/10-1) for r in ratios),'source_explanation':['archbench/bench/200.genann/minctest.h prints measured subtest microseconds inside bench_run','archbench/bench/202.llama2/run.c:815-859 prints computed tokens/s inside bench_run'],'rejected_assumption':'An initial fixed20us discrepancy limit incorrectly assumed frequency-independent formatted output and instruction counts; exact differences and both original logs are retained. No benchmark workload, algorithm validator or per-instruction differential check was changed.'};dump(aggregate,d)
if __name__=='__main__':main()

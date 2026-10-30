from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from ecc_rpc import Rpc
def main():
 p=argparse.ArgumentParser();p.add_argument('--name',choices=['light_preflight','cpu_area','cpu_baseline'],required=True);p.add_argument('--prepare-only',action='store_true');p.add_argument('--isolate-steps',action='store_true');p.add_argument('--rss-mib',type=int,default=3000);p.add_argument('--timeout',type=int,default=7200);a=p.parse_args();workspace=WORK/'physical'/a.name
 assert workspace.is_dir();lock=json.loads((ROOT/'reports/E_backend_compatible_tools.json').read_text());ecc=Path(lock['ecc']);patches=[];tag='E8/physical/'+a.name
 for file in sorted((workspace/'config').glob('*.json')):
  data=json.loads(file.read_text());changes=[]
  def visit(x,path=''):
   if isinstance(x,dict):
    for k,v in x.items():
     if k in ['thread_number','-thread_number','thread_num','num_threads'] and str(v)!='2':changes.append({'path':path+'/'+k,'before':v,'after':2});x[k]='2' if isinstance(v,str) else 2
     else:visit(v,path+'/'+k)
   elif isinstance(x,list):
    for i,v in enumerate(x):visit(v,path+'/'+str(i))
  visit(data)
  if changes:
   backup=ROOT/'artifacts'/tag/'initial_config'/file.name;backup.parent.mkdir(parents=True,exist_ok=True)
   if not backup.exists():shutil.copyfile(file,backup)
   dump(file,data);patches.append({'file':str(file),'changes':changes})
 if patches:dump(ROOT/'artifacts'/tag/'thread_limits.json',patches)
 if a.prepare_only:print('PHYSICAL_LIMITS_READY',a.name,flush=True);return
 memory={s.split(':',1)[0]:int(s.split()[1]) for s in Path('/proc/meminfo').read_text().splitlines() if s.startswith(('MemTotal:','MemAvailable:'))}
 assert memory['MemAvailable']>=max(768,a.rss_mib+256)*1024,'Insufficient available memory for the selected backend budget'
 if a.rss_mib>1440:assert memory['MemTotal']>=3584*1024,'The approved4GiBWSLconfiguration has not yet taken effect'
 env={'PATH':lock['yosys_root']+'/bin:'+os.environ['PATH'],'CUDA_VISIBLE_DEVICES':'','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}
 inputs=[ecc,*sorted((workspace/'config').glob('*.json')),*sorted((workspace/'origin').glob('*'))];inputs=[x for x in inputs if x.is_file()]
 if a.name=='light_preflight':resource.setrlimit(resource.RLIMIT_CPU,(600,610))
 reports=[];tool_digest=sha(ecc)
 try:
  current=json.loads((workspace/'home/flow.json').read_text())
  jobs=[s['name'] for s in current['steps'] if s['state']!='Success'] if a.isolate_steps else [None]
  for step in jobs:
   label=tag+('/'+step if step else '');report=ROOT/'artifacts'/label/'budget.json';reports.append(str(report.relative_to(ROOT)))
   assert sha(ecc)==tool_digest,'ECC executable changed between steps'
   selection=['--only',step] if step else ['--resume']
   command=['python3',ROOT/'E/runtime/budget_exec.py','--rss-mib',str(a.rss_mib),'--metric','pss','--report',report,'--','taskset','-c','0,1',ecc,'run','--workspace',workspace,*selection,'--jsonl']
   run(label+'/run',command,env=env,inputs=inputs if not step else [x for x in inputs if x!=ecc],outputs=[workspace/'home/flow.json',report],timeout=a.timeout)
   state=json.loads((workspace/'home/flow.json').read_text())
   if step:assert next(s['state'] for s in state['steps'] if s['name']==step)=='Success',step
 finally:
  flow=json.loads((workspace/'home/flow.json').read_text())
  dump(ROOT/'reports'/('E8_physical_'+a.name+'.json'),{'status':'FLOW_EXECUTED_REQUIRES_SIGNOFF_REVIEW','workspace':str(workspace),'flow':flow,'resource_evidence':reports,'ecc':str(ecc),'ecc_sha256':tool_digest,'isolated_steps':a.isolate_steps,'policy':'Eachselectedstepusesofficial--only inafreshprocess; noflowstate/checklist/qualitygateediting. Allmandatoryflowstepsandactualsignoffinspectionstillrequired.'})
 with Rpc(tag+'/inspect') as rpc:
  opened=rpc.call('workspace.open',{'directory':str(workspace)});review=rpc.call('workspace.inspect_signoff',{'workspaceId':opened['workspaceId']},timeout=180)
  dump(ROOT/'reports'/('E8_signoff_'+a.name+'.json'),review)
 print('PHYSICAL_FLOW_RETURNED',a.name,review['status'],flush=True)
if __name__=='__main__':main()

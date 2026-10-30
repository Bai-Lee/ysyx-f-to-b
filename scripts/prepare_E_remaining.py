from evidence import *
import shutil
def main():
    scope=ROOT/'E/runtime';scope.mkdir(parents=True,exist_ok=True)
    ledger=ROOT/'config/task_status.json';d=json.loads(ledger.read_text('utf8'));rows=[r for r in d['tasks'] if r['id'].split('-')[0] in ['E5','E6','E7','E8','E9']]
    assert len(rows)==96
    arc=ROOT.parents[1]/'YSYX_F_B_Archive';sources=[]
    for stage in ['E5','E6','E7','E8','E9']:
        p=ROOT/'E'/stage;(p/'sources').mkdir(parents=True,exist_ok=True)
        r=next(r for r in rows if r['id'].startswith(stage+'-'));s=r['source'];assert sha(arc/s['raw'])==s['source_sha256']
        source=arc/s['markdown'];dest=p/'sources'/(stage+'.md');shutil.copyfile(source,dest)
        sources.append({'stage':stage,'source':str(source),'copy':str(dest),'sha256':sha(source),'raw_sha256':s['source_sha256'],'url':s['url'],'version':s['version']})
    dump(scope/'course_specs.json',{'status':'FROZEN_REQUIREMENTS_NOT_VERDICT','tasks':rows,'sources':sources})
    b=ROOT/'config/history'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f');b.mkdir(parents=True)
    for n in ['task_status.json','execution_policy.json']:shutil.copyfile(ROOT/'config'/n,b/n)
    d.update(current_stage='E5',stage_status='IN_PROGRESS',next_stage='E5 through E9');dump(ledger,d)
    p=ROOT/'config/execution_policy.json';d=json.loads(p.read_text('utf8'));d.update(current_scope='Complete all remaining E5-E9 engineering tasks and audit the whole E stage; preserve earlier results and user-excluded personal processes.',stop_after='E',user_resume='继续推进E阶段的所有');dump(p,d)
    print('REMAINING_E_FROZEN',len(rows),flush=True)
if __name__=='__main__':main()

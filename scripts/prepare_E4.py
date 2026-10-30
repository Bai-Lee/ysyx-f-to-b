from evidence import *
import shutil

def main():
    arc=ROOT.parents[1]/'YSYX_F_B_Archive';rows=json.loads((ROOT/'config/task_status.json').read_text('utf8'))['tasks']
    chosen=[r for r in rows if r['id'].startswith(('E4-','NJU-'))]
    folder=ROOT/'E/E4';(folder/'sources').mkdir(parents=True,exist_ok=True)
    files={}
    for row in chosen:
        s=row['source'];raw=arc/s['raw'];assert sha(raw)==s['source_sha256']
        md=arc/s['markdown'];dest=folder/'sources'/md.name
        if md.name not in files:shutil.copyfile(md,dest);files[md.name]={'source':str(md),'copy':str(dest),'sha256':sha(dest),'raw_sha256':s['source_sha256'],'url':s['url'],'version':s['version']}
    dump(folder/'course_specs.json',{'tasks':chosen,'sources':list(files.values()),'status':'FROZEN_REQUIREMENTS_NOT_VERDICT'})
    history=ROOT/'config/history'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f');history.mkdir(parents=True)
    for name in ['task_status.json','execution_policy.json']:shutil.copyfile(ROOT/'config'/name,history/name)
    d=json.loads((ROOT/'config/task_status.json').read_text('utf8'));d.update(current_stage='E4',stage_status='IN_PROGRESS',next_stage='E4');dump(ROOT/'config/task_status.json',d)
    d=json.loads((ROOT/'config/execution_policy.json').read_text('utf8'));d['current_scope']='Implement and validate E4 with existing tools/offline sources; no Logisim computer use';dump(ROOT/'config/execution_policy.json',d)
    print('E4_FROZEN',len(chosen),len(files),flush=True)

if __name__=='__main__':main()

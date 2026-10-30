"""Freeze the next authorized stage without changing the course or E runtime."""
from evidence import *
import shutil, re

def main():
    arc=ROOT.parents[1]/'YSYX_F_B_Archive'
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    backup=ROOT/'config/history'/('before_D_'+stamp);backup.mkdir(parents=True)
    for name in ('task_status.json','execution_policy.json','toolchain.json'):
        shutil.copyfile(ROOT/'config'/name,backup/name)
    ledger=json.loads((ROOT/'config/task_status.json').read_text('utf8'))
    rows=[x for x in ledger['tasks'] if re.match(r'^D[1-9]-',x['id'])]
    assert len(rows)==103 and all(x['status'] in ('NOT_RUN','EXCLUDED_SCOPE') for x in rows)
    runtime=ROOT/'D/runtime';runtime.mkdir(parents=True,exist_ok=True)
    sources=[]
    for stage in range(1,10):
        name=f'D{stage}';dest=ROOT/'D'/name/'sources';dest.mkdir(parents=True,exist_ok=True)
        source=arc/'docs/markdown/D'/f'{name}.md';copy=dest/source.name
        assert not copy.exists(),f'already prepared: {copy}'
        shutil.copyfile(source,copy)
        raw=arc/'docs/raw_html/D'/f'{name}.html'
        sources.append({'stage':name,'source':str(source),'copy':str(copy),'sha256':sha(source),'raw_sha256':sha(raw)})
    refs=[];rd=ROOT/'D/runtime/sources/pa';rd.mkdir(parents=True,exist_ok=True)
    for source in sorted((arc/'references/markdown').glob('*.md')):
        first=source.read_text('utf8').splitlines()[0]
        if not re.search(r'ysyx\.oscc\.cc/docs/ics-pa/(1\.[1-7]|2\.[1-4]|FAQ)\.html',first):continue
        copy=rd/source.name;shutil.copyfile(source,copy)
        refs.append({'source':str(source),'copy':str(copy),'sha256':sha(source),'header':first})
    dump(runtime/'course_specs.json',{'status':'FROZEN_REQUIREMENTS_NOT_VERDICT','tasks':rows,'sources':sources,'pa_sources':refs,'D9':'Original page contains only construction notice; no invented assignment.'})
    old=json.loads((ROOT/'reports/E_delivery_archive.json').read_text('utf8'))
    zipfile=ROOT/'YSYX_E_DELIVERY.zip';digest=sha(zipfile)
    assert digest in json.dumps(old)
    dump(ROOT/'reports/D_baseline.json',{'status':'PASS','timestamp':stamp,'E_zip_sha256':digest,'E_audit_sha256':sha(ROOT/'reports/E_AUDIT.json'),'git_head':subprocess.check_output(['D:/Git/Git/cmd/git.exe','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),'source_count':len(sources),'pa_sources':len(refs),'scope_records':len(rows),'core_records':sum(x['classification']=='PUBLIC_CORE_TASK' for x in rows),'preservation':'E source, simulation runtimes and ZIP retained; D has separate code, builds and evidence.'})
    ledger.update(current_stage='D',stage_status='IN_PROGRESS',next_stage=None,stop_after='D',completion_scope=None)
    ledger.pop('completed_at',None);dump(ROOT/'config/task_status.json',ledger)
    p=ROOT/'config/execution_policy.json';policy=json.loads(p.read_text('utf8'))
    policy.update(current_scope='Complete D1-D8 public engineering work and D9 source-scope audit, preserving F/E results and exclusions.',stop_after='D',user_resume='继续完成D阶段',source_instruction='2026-10-26 user explicitly authorized continuing and completing D stage; supersedes stop after E.')
    dump(p,policy)
    # Independent copy: later D changes cannot affect E verification scripts.
    common=(ROOT/'E/runtime/common.py').read_text('utf8').replace("WORK=Path('/home/USER/e-stage')","WORK=Path('/home/USER/d-stage')").replace("ROOT/'reports/E_remaining_results.json'","ROOT/'reports/D_results.json'").replace('User-approved WSL memory change is recorded in E_backend_memory_update.json.','Existing user-approved 4 GiB WSL limit is reused; no system settings changed.').replace('documented in E_runtime_budget.json','recorded in D_PREFLIGHT.json')
    (runtime/'common.py').write_text(common,encoding='utf8')
    dest=ROOT.parents[1]/'downloads/ysyx_d_stage/sources';dest.mkdir(parents=True,exist_ok=True)
    name='NJU-ProjectN__nemu__ics2024';repo=arc/'repos'/name
    meta=json.loads((arc/'inventory/repo_metadata'/f'{name}.json').read_text('utf8'))
    git='D:/Git/Git/cmd/git.exe';head=subprocess.check_output([git,'-C',str(repo),'rev-parse','HEAD'],text=True).strip();assert head==meta['commit']
    tar=dest/f'{name}.tar.gz'
    r=run('D/sources/nemu',[git,'-c','core.autocrlf=false','-C',repo,'archive','--format=tar.gz','-o',tar,'HEAD'],timeout=180);assert r['status']=='PASS'
    dump(ROOT/'reports/D_source_lock.json',{'status':'PASS','repositories':[{'name':name,'commit':head,'archive':str(tar),'sha256':sha(tar),'original':str(repo)}],'inherited_source_lock':'reports/E_source_lock_canonical.json'})
    print('D_PREPARED',len(rows),'records',len(refs),'PA source documents',flush=True)

if __name__=='__main__':main()

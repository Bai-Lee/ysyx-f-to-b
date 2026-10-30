from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,time,os,sys
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def dump(p,v):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
def run(name,cmd,inputs=(),timeout=90,env=None,cwd=ROOT,expected=0):
    folder=ROOT/'artifacts'/name;folder.mkdir(parents=True,exist_ok=True)
    if (folder/'run.json').exists():
        import shutil
        history=folder/'attempts'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f');history.mkdir(parents=True)
        for filename in ('run.json','stdout.log','stderr.log','input_snapshot.zip'):
            if (folder/filename).exists():shutil.copyfile(folder/filename,history/filename)
    start=time.monotonic();before=[{'path':str(p),'sha256':sha(p)} for p in inputs]
    if inputs:
        import zipfile
        with zipfile.ZipFile(folder/'input_snapshot.zip','w',zipfile.ZIP_DEFLATED) as z:
            for i,p in enumerate(inputs):z.write(p,f'{i:02d}_{Path(p).name}')
    try:
        q=subprocess.run(list(map(str,cmd)),cwd=cwd,env=env,capture_output=True,timeout=timeout)
        code=q.returncode;out=q.stdout;err=q.stderr;status='PASS' if (code in expected if isinstance(expected,(tuple,list,set)) else code==expected) else 'FAIL'
    except subprocess.TimeoutExpired as e:code=None;out=e.stdout or b'';err=e.stderr or b'';status='TIMEOUT'
    (folder/'stdout.log').write_bytes(out);(folder/'stderr.log').write_bytes(err)
    after=[{'path':str(p),'sha256':sha(p)} for p in inputs];unchanged=before==after
    if not unchanged:status='FAIL'
    row={'name':name,'timestamp':datetime.now(timezone.utc).isoformat(),'command':list(map(str,cmd)),'cwd':str(cwd),'exit_code':code,'expected_exit':list(expected) if isinstance(expected,set) else expected,'status':status,'elapsed_seconds':round(time.monotonic()-start,3),'timeout_seconds':timeout,'inputs':before,'inputs_after':after,'inputs_unchanged':unchanged,'stdout_sha256':sha(folder/'stdout.log'),'stderr_sha256':sha(folder/'stderr.log')}
    dump(folder/'run.json',row);print(name,status,'exit',code,'seconds',row['elapsed_seconds'],flush=True)
    if status not in ('PASS',):print(out.decode('utf8','replace')[-3000:],err.decode('utf8','replace')[-1500:],flush=True)
    return row

def mark(ids,status,evidence,details=''):
    path=ROOT/'config/task_status.json';data=json.loads(path.read_text('utf8'));wanted=set(ids)
    for row in data['tasks']:
        if row['id'] in wanted:row.update(status=status,evidence=[str(p) for p in evidence],result_details=details,updated=datetime.now(timezone.utc).isoformat())
    missing=wanted-{r['id'] for r in data['tasks']}
    if missing:raise ValueError('Unknown task IDs '+str(missing))
    dump(path,data)

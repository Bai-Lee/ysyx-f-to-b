from pathlib import Path
import os,sys,json,hashlib,subprocess,time,datetime,shlex
PROJECT=Path('/workspace/projects/ysyx_f_to_b')
LAB=Path('/home/USER/e3-lab/missing-semester')
OUT=PROJECT/'artifacts/E3/MS'
LAB.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,d):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2))
def run(tag,args,cwd=LAB,expected=(0,),timeout=40,inputs=(),stdin=None):
    dest=OUT/tag;dest.mkdir(parents=True,exist_ok=True)
    if (dest/'run.json').exists():
        import shutil
        hist=dest/'attempts'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f');hist.mkdir(parents=True)
        for n in ('run.json','stdout.log','stderr.log','stdin.log','input_snapshot.zip'):
            if (dest/n).exists():shutil.copyfile(dest/n,hist/n)
    before=[{'path':str(p),'sha256':sha(p)} for p in inputs];started=time.monotonic()
    if inputs:
        import zipfile
        with zipfile.ZipFile(dest/'input_snapshot.zip','w',zipfile.ZIP_DEFLATED) as z:
            for i,p in enumerate(inputs):z.write(p,f'{i:02d}_{Path(p).name}')
    import pwd
    env=os.environ.copy();env.update(LC_ALL='C',TERM='xterm',COLUMNS='80',LINES='24',SHELL=pwd.getpwuid(os.getuid()).pw_shell)
    try:
        q=subprocess.run(args,cwd=cwd,env=env,input=stdin.encode() if isinstance(stdin,str) else stdin,capture_output=True,timeout=timeout);rc=q.returncode;out=q.stdout;err=q.stderr;status='PASS' if rc in expected else 'FAIL'
    except subprocess.TimeoutExpired as e:rc=None;out=e.stdout or b'';err=e.stderr or b'';status='TIMEOUT'
    (dest/'stdout.log').write_bytes(out);(dest/'stderr.log').write_bytes(err)
    if stdin is not None:(dest/'stdin.log').write_bytes(stdin.encode() if isinstance(stdin,str) else stdin)
    row={'name':tag,'status':status,'command':args,'cwd':str(cwd),'exit_code':rc,'expected_exit':list(expected),'elapsed_seconds':round(time.monotonic()-started,3),'timeout_seconds':timeout,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':before,'inputs_after':[{'path':str(p),'sha256':sha(p)} for p in inputs],'stdout_sha256':sha(dest/'stdout.log'),'stderr_sha256':sha(dest/'stderr.log')}
    dump(dest/'run.json',row);print(tag,status,'exit',rc,flush=True)
    if status!='PASS':print(err.decode('utf8','replace')[-1500:]);raise AssertionError(tag)
    return out.decode('utf8','replace'),err.decode('utf8','replace'),row
def shell(tag,text,**kwargs):
    source=OUT/tag/'command.sh';source.parent.mkdir(parents=True,exist_ok=True);source.write_text(text)
    return run(tag,['bash',str(source)],inputs=[source],**kwargs)
def record(ids,status,evidence,detail):
    p=PROJECT/'reports/E3_MS_results.json';d=json.loads(p.read_text()) if p.exists() else {'records':[]};rows={r['id']:r for r in d['records']}
    for id_ in ids:rows[id_]={'id':id_,'status':status,'evidence':evidence,'details':detail}
    dump(p,{'status':'IN_PROGRESS','records':sorted(rows.values(),key=lambda r:r['id'])})

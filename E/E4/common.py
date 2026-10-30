from pathlib import Path
import os,sys,json,hashlib,subprocess,time,datetime,zipfile,shutil,resource
ROOT=Path('/workspace/projects/ysyx_f_to_b')
WORK=Path('/home/USER/e4-lab');WORK.mkdir(exist_ok=True)
OUT=ROOT/'artifacts/E4';OUT.mkdir(parents=True,exist_ok=True)
VROOT=Path('/home/USER/tools/verilator-stable-src')
VERILATOR=VROOT/'bin/verilator'
NVBOARD=Path('/home/USER/ysyx-workbench/nvboard')
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
def run(tag,args,inputs=(),cwd=WORK,timeout=90,expected=(0,),env=None):
    d=OUT/tag;d.mkdir(parents=True,exist_ok=True)
    if (d/'run.json').exists():
        h=d/'attempts'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f');h.mkdir(parents=True)
        for n in ['run.json','stdout.log','stderr.log','input_snapshot.zip']:
            if (d/n).exists():shutil.copyfile(d/n,h/n)
    before=[{'path':str(p),'sha256':sha(p)} for p in inputs]
    if inputs:
        with zipfile.ZipFile(d/'input_snapshot.zip','w',zipfile.ZIP_DEFLATED) as z:
            for i,p in enumerate(inputs):z.write(p,f'{i:03d}_{Path(p).name}')
    variables=os.environ.copy();variables.update(VERILATOR_ROOT=str(VROOT),NVBOARD_HOME=str(NVBOARD),LC_ALL='C',SHELL='/bin/bash',OMP_NUM_THREADS='2',MAKEFLAGS='-j2')
    if env:variables.update(env)
    t=time.monotonic()
    try:q=subprocess.run(list(map(str,args)),cwd=cwd,env=variables,capture_output=True,timeout=timeout);rc=q.returncode;o=q.stdout;e=q.stderr;status='PASS' if rc in expected else 'FAIL'
    except subprocess.TimeoutExpired as x:rc=None;o=x.stdout or b'';e=x.stderr or b'';status='TIMEOUT'
    (d/'stdout.log').write_bytes(o);(d/'stderr.log').write_bytes(e)
    row={'status':status,'name':tag,'command':list(map(str,args)),'cwd':str(cwd),'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':round(time.monotonic()-t,3),'exit_code':rc,'expected_exit':list(expected),'timeout_seconds':timeout,'inputs':before,'inputs_after':[{'path':str(p),'sha256':sha(p)} for p in inputs],'stdout_sha256':sha(d/'stdout.log'),'stderr_sha256':sha(d/'stderr.log'),'budget':'WSL2 2GiB RAM/2GiB swap; make<=j2; one heavy task'}
    dump(d/'run.json',row);print(tag,status,rc,flush=True)
    if status!='PASS':print(o.decode(errors='replace')[-1200:]+e.decode(errors='replace')[-3500:]);raise AssertionError(tag)
    return o.decode(errors='replace'),e.decode(errors='replace'),row
def result(ids,evidence,detail,status='PASS'):
    p=ROOT/'reports/E4_results.json';d=json.loads(p.read_text()) if p.exists() else {'records':[]};r={x['id']:x for x in d['records']}
    for i in ids:r[i]={'id':i,'status':status,'evidence':evidence,'details':detail}
    dump(p,{'status':'IN_PROGRESS','records':list(r.values())})
def build(top,sources,harness,name,defines=(),trace=True,extra=(),flags=(),additional_inputs=()):
    target=WORK/'build'/name;target.mkdir(parents=True,exist_ok=True)
    cmd=[VERILATOR,'--cc','--exe','--build','-j','2','--assert','-Wall','--top-module',top,'--Mdir',target,'-o',name]
    if trace:cmd+=['--trace']
    cmd += list(flags)+['+define+'+d for d in defines]+list(sources)+[harness]+list(extra)
    run('build/'+name,cmd,inputs=[*sources,harness,*[p for p in extra if isinstance(p,Path) and p.is_file()],*additional_inputs],timeout=240)
    return target/name

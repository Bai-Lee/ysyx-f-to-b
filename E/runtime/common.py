from pathlib import Path
import os,sys,json,hashlib,subprocess,time,datetime,zipfile,shutil,resource,signal
ROOT=Path('/workspace/projects/ysyx_f_to_b')
ARCHIVE=Path('/workspace/YSYX_F_B_Archive')
WORK=Path('/home/USER/e-stage');WORK.mkdir(exist_ok=True)
BENCH=WORK/'workbench'
VROOT=Path('/home/USER/tools/verilator-stable-src');VERILATOR=VROOT/'bin/verilator'
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def dump(p,x):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
def run(tag,args,inputs=(),cwd=WORK,timeout=120,expected=(0,),env=None,outputs=()):
    d=ROOT/'artifacts'/tag;d.mkdir(parents=True,exist_ok=True)
    if (d/'run.json').exists() or (d/'started.json').exists():
        h=d/'attempts'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f');h.mkdir(parents=True)
        for n in ['run.json','started.json','stdout.log','stderr.log','input_snapshot.zip','output_snapshot.zip']:
            if (d/n).exists():shutil.copyfile(d/n,h/n)
        if not (d/'run.json').exists():
            dump(h/'incomplete.json',{'status':'UNKNOWN','reason':'Saved launch has no completion record. No prior success inferred; preserved before retry.'})
    before=[{'path':str(p),'sha256':sha(p)} for p in inputs]
    if inputs:
        with zipfile.ZipFile(d/'input_snapshot.zip','w',zipfile.ZIP_DEFLATED) as z:
            for i,p in enumerate(inputs):z.write(p,f'{i:03d}_{Path(p).name}')
    variables=os.environ.copy();variables.update(VERILATOR_ROOT=str(VROOT),LC_ALL='C',SHELL='/bin/bash',OMP_NUM_THREADS='1',MAKEFLAGS='-j1',AM_HOME=str(BENCH/'abstract-machine'),NPC_HOME=str(BENCH/'npc'))
    if env:variables.update(env)
    mem={}
    for line in Path('/proc/meminfo').read_text().splitlines():
        key,value=line.split(':',1)
        if key in ['MemTotal','MemAvailable','SwapTotal','SwapFree']:mem[key+'_KiB']=int(value.split()[0])
    limits={'linux_memory_before':mem,'address_space_limit_bytes':list(resource.getrlimit(resource.RLIMIT_AS)),'cpu_time_limit_seconds':list(resource.getrlimit(resource.RLIMIT_CPU)),'makeflags':variables.get('MAKEFLAGS'),'omp_threads':variables.get('OMP_NUM_THREADS')}
    started={'status':'STARTED_NOT_A_COMPLETION','name':tag,'command':list(map(str,args)),'cwd':str(cwd),'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':before,'resource_limits':limits,'timeout_seconds':timeout}
    dump(d/'started.json',started)
    usage_before=resource.getrusage(resource.RUSAGE_CHILDREN);t=time.monotonic()
    with (d/'stdout.log').open('wb') as out,(d/'stderr.log').open('wb') as err:
        p=subprocess.Popen(list(map(str,args)),cwd=cwd,env=variables,stdout=out,stderr=err,start_new_session=True)
        started['pid']=p.pid;started['process_group']=p.pid;dump(d/'started.json',started)
        try:
            rc=p.wait(timeout=timeout);status='PASS' if rc in expected else 'RESOURCE_LIMIT' if rc==-signal.SIGXCPU or (rc==125 and any(Path(str(a)).name=='budget_exec.py' for a in args)) else 'FAIL'
        except subprocess.TimeoutExpired:
            os.killpg(p.pid,signal.SIGTERM)
            try:p.wait(timeout=5)
            except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
            rc=None;status='TIMEOUT'
    row={'status':status,'name':tag,'command':list(map(str,args)),'cwd':str(cwd),'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':round(time.monotonic()-t,3),'exit_code':rc,'expected_exit':list(expected),'timeout_seconds':timeout,'inputs':before,'inputs_after':[{'path':str(p),'sha256':sha(p)} for p in inputs],'stdout_sha256':sha(d/'stdout.log'),'stderr_sha256':sha(d/'stderr.log'),'budget':'Actual Linux memory/swap and per-process limits are recorded below. Compile j1; bounded concurrency and backend CPU affinity documented in E_runtime_budget.json. User-approved WSL memory change is recorded in E_backend_memory_update.json.','resource_limits':limits}
    usage_after=resource.getrusage(resource.RUSAGE_CHILDREN);row['child_resource_usage']={'user_seconds':usage_after.ru_utime-usage_before.ru_utime,'system_seconds':usage_after.ru_stime-usage_before.ru_stime,'maxrss_kib_upper_bound_including_prior_children':usage_after.ru_maxrss}
    row['task_environment']={k:variables[k] for k in ['AM_HOME','NPC_HOME','BENCH_HOME','VERILATOR_ROOT','NVBOARD_HOME','LC_ALL','SHELL','MAKEFLAGS','OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','CUDA_VISIBLE_DEVICES','YOSYS_SYNTH_STRATEGY','nproc','NPC_ARGS','SDL_VIDEODRIVER','SDL_AUDIODRIVER'] if k in variables}
    row['outputs']=[{'path':str(p),'sha256':sha(p)} if Path(p).is_file() else {'path':str(p),'missing':True} for p in outputs]
    if outputs:
        with zipfile.ZipFile(d/'output_snapshot.zip','w',zipfile.ZIP_DEFLATED) as z:
            for i,p in enumerate(outputs):
                if Path(p).is_file():z.write(p,f'{i:03d}_{Path(p).name}')
    dump(d/'run.json',row);print(tag,status,rc,flush=True)
    o=(d/'stdout.log').read_text(errors='replace');e=(d/'stderr.log').read_text(errors='replace')
    if status!='PASS':print(o[-1800:]+e[-3500:],flush=True);raise AssertionError(tag)
    return o,e,row
def mark(ids,status,evidence,details):
    p=ROOT/'reports/E_remaining_results.json';d=json.loads(p.read_text()) if p.exists() else {'records':[]};rows={r['id']:r for r in d['records']}
    for i in ids:rows[i]={'id':i,'status':status,'evidence':evidence,'details':details}
    dump(p,{'status':'IN_PROGRESS','records':list(rows.values())})
def build(tag,top,sources,cpp,extra=(),flags=(),additional_inputs=()):
    d=WORK/'build'/tag;d.mkdir(parents=True,exist_ok=True)
    cmd=[VERILATOR,'--cc','--exe','--build','-j','1','--assert','-Wall','--top-module',top,'--Mdir',d,'-o','sim',*flags,*sources,*cpp,*extra]
    run(tag+'/build',cmd,inputs=[*sources,*cpp,*[p for p in extra if isinstance(p,Path) and p.is_file()],*additional_inputs],timeout=300)
    return d/'sim'

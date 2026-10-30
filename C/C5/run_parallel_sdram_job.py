"""Detached, resumable full128MiB phase batch for the user-authorized throughput mode."""
from pathlib import Path
import argparse,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from resource_policy import windows_available_bytes,linux_memory,POLICY_PATH


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--launch',action='store_true');args=parser.parse_args()
    folder=ROOT/'artifacts/C5/parallel-full128-job';folder.mkdir(parents=True,exist_ok=True);state=folder/'status.json'
    source=Path(__file__).resolve()
    os.environ['YSYX_HOST_MEMORY_SAMPLE']=str(ROOT/'temp/host-memory')
    os.environ['YSYX_REQUIRE_HOST_MEMORY_SAMPLE']='1'
    if args.launch:
        for proc in Path('/proc').glob('[0-9]*'):
            try:command=(proc/'cmdline').read_bytes().decode().split('\0')
            except (FileNotFoundError,PermissionError,ProcessLookupError):continue
            if len(command)>1 and command[1] in [str(source),str(ROOT/'C/C5/run_full_sdram_job.py')] and '--launch' not in command:
                raise RuntimeError('An existing full-memory job is active: '+proc.name)
        pilot=json.loads((ROOT/'reports/C5_parallel_sdram_pilot.json').read_text());assert pilot['status'].startswith('PASS') and pilot['speedup']>1
        policy=load_policy();assert windows_available_bytes()>=policy['windows_start_available_mib']*1024**2 and linux_memory()['MemAvailable']>=policy['linux_running_available_mib']*1024**2
        stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')
        with (folder/('launcher-'+stamp+'.stdout.log')).open('xb') as out,(folder/('launcher-'+stamp+'.stderr.log')).open('xb') as err:
            process=subprocess.Popen(['python3',source],cwd=WORK,stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True,close_fds=True)
        print('PARALLEL_FULL128_LAUNCHED',process.pid,flush=True);return
    if state.exists():
        history=folder/'attempts'/str(time.time_ns());history.mkdir(parents=True)
        for name in ['status.json','stdout.log','stderr.log','input_snapshot.zip']:
            if (folder/name).exists():shutil.copyfile(folder/name,history/name)
    profile=json.loads(POLICY_PATH.read_text())['limits']['C_parallel_validation']
    command=['python3',ROOT/'C/C5/parallel_sdram.py','--bytes','134217728','--jobs',str(profile['max_simulators']),'--label','full128']
    inputs=[source,ROOT/'C/C5/parallel_sdram.py',ROOT/'C/C5/programs/mem-sweep-phase.c',ROOT/'C/C5/programs/mem-sweep-asm.S',ROOT/'C/runtime/budget_exec.py',ROOT/'C/runtime/resource_policy.py',ROOT/'scripts/host_memory_monitor.py',POLICY_PATH]
    with zipfile.ZipFile(folder/'input_snapshot.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for i,path in enumerate(inputs):archive.write(path,f'{i:03d}_{path.name}')
    record={'status':'RUNNING','worker_pid':os.getpid(),'command':list(map(str,command)),'cwd':str(WORK),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':[{'path':str(p),'sha256':sha(p)} for p in inputs],
        'environment':{key:os.environ[key] for key in ['YSYX_HOST_MEMORY_SAMPLE','YSYX_REQUIRE_HOST_MEMORY_SAMPLE']},
        'scope':'Each independently reset pattern covers full128MiB. One aggregate PSS guard supervises all concurrent simulators. Individual completed patterns resume only after exact hash/result verification.'}
    dump(state,record);start=time.monotonic()
    with (folder/'stdout.log').open('wb') as out,(folder/'stderr.log').open('wb') as err:
        process=subprocess.Popen(list(map(str,command)),cwd=WORK,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
        record['driver_pid']=process.pid;dump(state,record);rc=process.wait()
    record.update(status='PASS' if rc==0 else 'FAIL',exit_code=rc,elapsed_seconds=time.monotonic()-start,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        inputs_after=[{'path':str(p),'sha256':sha(p)} for p in inputs],stdout_sha256=sha(folder/'stdout.log'),stderr_sha256=sha(folder/'stderr.log'))
    assert record['inputs_after']==record['inputs'];dump(state,record)
    print('PARALLEL_FULL128_JOB_'+record['status'],flush=True);raise SystemExit(rc)


if __name__=='__main__':main()

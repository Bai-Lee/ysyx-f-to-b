"""Start the long C5 worker without tying it to a Windows wsl.exe client."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,subprocess,sys
from resource_policy import linux_memory,load_policy,windows_available_bytes

ROOT=Path(__file__).resolve().parents[1]
WORK=Path('/home/USER/b-stage')


def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--probe',action='store_true');args=parser.parse_args()
    worker=ROOT/'C5/run_full_sdram_job.py'
    # ROOT here is the C directory; report/artifact paths belong to its parent.
    project=ROOT.parent
    for proc in Path('/proc').glob('[0-9]*'):
        try:
            command=(proc/'cmdline').read_bytes().decode().split('\0')
        except (FileNotFoundError,PermissionError,ProcessLookupError):continue
        if len(command)>1 and Path(command[0]).name.startswith('python') and command[1]==str(worker):
            raise RuntimeError('An existing C5 full-memory worker is active: '+proc.name)
    policy=load_policy();host=windows_available_bytes();linux=linux_memory()
    assert host>=policy['windows_start_available_mib']*1024**2,'Windows start headroom'
    assert linux['MemAvailable']>=policy['linux_running_available_mib']*1024**2,'WSL start headroom'
    if args.probe:
        folder=project/'artifacts/C/detach-probe'
        command=[sys.executable,ROOT/'runtime/budget_exec.py','--report',folder/'resources.json','--',sys.executable,'-c',
                 'import time; time.sleep(15); print("DETACHED_BUDGET_PROBE_COMPLETED", flush=True)']
    else:
        state=project/'artifacts/C5/full128-job/status.json'
        if state.exists():assert json.loads(state.read_text())['status']!='RUNNING','Resolve the stale RUNNING record before restarting.'
        probe=json.loads((project/'artifacts/C/detach-probe/resources.json').read_text())
        assert probe['status']=='PASS' and probe['elapsed_seconds']>=15 and len(probe['timeline'])>=3,'Detached monitor probe must pass first'
        folder=project/'artifacts/C5/full128-job'
        command=[sys.executable,worker]
    folder.mkdir(parents=True,exist_ok=True)
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    stdout=folder/('detached-'+stamp+'.stdout.log');stderr=folder/('detached-'+stamp+'.stderr.log')
    with stdout.open('xb') as out,stderr.open('xb') as err:
        process=subprocess.Popen(list(map(str,command)),cwd=WORK,stdin=subprocess.DEVNULL,stdout=out,stderr=err,
                                 start_new_session=True,close_fds=True)
    record={'status':'LAUNCHED_NOT_ACCEPTED','pid':process.pid,'command':list(map(str,command)),'cwd':str(WORK),
        'timestamp':stamp,'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
        'launcher_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'stdout':str(stdout),'stderr':str(stderr),
        'windows_available_before':host,'linux_memory_before':linux,'policy':policy,
        'scope':'New Linux session, no inherited terminal/stdin/stdout/stderr. The Windows wsl.exe invocation exits after launching. No service, scheduled task or persistent system setting is created. This survives caller exit, not WSL termination or a machine reboot.'}
    write(folder/('detached-launch-'+stamp+'.json'),record)
    print(json.dumps(record),flush=True)


if __name__=='__main__':main()

"""Foreground worker for the optional hidden Windows/WSL long-run launcher."""
from pathlib import Path
import sys,os,signal
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    folder=ROOT/'artifacts/C5/full128-job';folder.mkdir(parents=True,exist_ok=True);status=folder/'status.json'
    if status.exists():
        previous=json.loads(status.read_text());pid=previous.get('worker_pid')
        command_file=Path('/proc',str(pid),'cmdline') if pid else None
        actual_command=command_file.read_bytes().split(b'\0') if command_file and command_file.exists() else []
        if previous.get('status')=='RUNNING' and pid!=os.getpid() and str(Path(__file__)).encode() in actual_command:raise RuntimeError('Existing full128 worker is still present')
        attempt=folder/'attempts'/str(time.time_ns());attempt.mkdir(parents=True)
        for name in ['status.json','worker.stdout.log','worker.stderr.log','source_snapshot.zip']:
            if (folder/name).exists():shutil.copyfile(folder/name,attempt/name)
    driver=ROOT/'C/C5/verify_sdram.py';command=['python3',str(driver),'--width','32','--ranks','2','--bytes','134217728','--assembly-loop']
    sources=[Path(__file__),driver,ROOT/'C/C5/programs/mem-sweep-asm.c',ROOT/'C/C5/programs/mem-sweep-asm.S',ROOT/'C/runtime/common.py',ROOT/'C/runtime/budget_exec.py',ROOT/'C/runtime/resource_policy.py',ROOT/'C/runtime/launch_detached.py']
    with zipfile.ZipFile(folder/'source_snapshot.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for index,path in enumerate(sources):archive.write(path,f'{index:02d}_{path.name}')
    record={'status':'RUNNING','worker_pid':os.getpid(),'command':command,'cwd':str(WORK),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_files':[{'path':str(path),'sha256':sha(path)} for path in sources],'purpose':'Full128MiB four-chipSDRAM acceptance; actualsimulator itself is supervised by budget_exec.py. No pass until child and required coverage assertions complete.'}
    dump(status,record);start=time.monotonic()
    with (folder/'worker.stdout.log').open('wb') as out,(folder/'worker.stderr.log').open('wb') as err:
        process=subprocess.Popen(command,cwd=WORK,stdout=out,stderr=err,stdin=subprocess.DEVNULL)
        record['driver_pid']=process.pid;dump(status,record);rc=process.wait()
    record.update(exit_code=rc,elapsed_seconds=time.monotonic()-start,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout_sha256=sha(folder/'worker.stdout.log'),stderr_sha256=sha(folder/'worker.stderr.log'))
    record['status']='PASS' if rc==0 else 'FAIL'
    if rc==0:
        result=next(row for row in json.loads((ROOT/'reports/C5_sdram_sweep.json').read_text())['runs'] if row['width']==32 and row['ranks']==2 and row['bytes']==134217728 and row.get('assembly_loop') and not row['corrupt'])
        assert result['status']=='PASS';record['accepted_result']=result;record['result_report_sha256']=sha(ROOT/'reports/C5_sdram_sweep.json')
    dump(status,record);print('C5_FULL128_JOB_'+record['status'],rc,flush=True);raise SystemExit(rc)


if __name__=='__main__':main()

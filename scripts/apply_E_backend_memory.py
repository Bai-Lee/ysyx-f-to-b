"""Apply the user's approved4GiB limit only after all active verification finishes."""
from evidence import *
import time
def decode(data):
    return data.decode('utf-16-le' if b'\x00' in data else 'utf-8-sig').replace('\x00','').strip('\ufeff\r\n ')
def main():
    for name in ['E8_final_mapped','E7_soc_performance']:
        assert json.loads((ROOT/'reports'/(name+'.json')).read_text('utf8'))['status']=='PASS',name+' is not complete'
    record=ROOT/'reports/E_backend_memory_update.json';d=json.loads(record.read_text('utf8'));config=Path('/home/USER/.wslconfig');assert sha(config)==d['after_sha256']
    command=['wsl','-d','YSYX-Linux','-u','ysyx','--exec','python3','-c','import json;from pathlib import Path;print(json.dumps({s.split(":",1)[0]:int(s.split()[1]) for s in Path("/proc/meminfo").read_text().splitlines() if s.startswith(("MemTotal:","MemAvailable:","SwapTotal:","SwapFree:"))}))']
    probe=subprocess.run(command,capture_output=True,timeout=60);assert probe.returncode==0,decode(probe.stderr);observed=json.loads(decode(probe.stdout))
    if observed['MemTotal']>=3584*1024:
        d.update(status='APPLIED_AND_VERIFIED',actual_linux_memory_KiB=observed,applied_at=datetime.now(timezone.utc).isoformat(),activation='Already effective after the completed jobs and subsequent WSL launch; no explicit shutdown needed.');dump(record,d);print(json.dumps(d,ensure_ascii=False),flush=True);return
    running=subprocess.check_output(['wsl','--list','--running','--quiet']);names=[n.strip() for n in decode(running).splitlines() if n.strip()];assert names==['YSYX-Linux'],names
    check=subprocess.run(['wsl','-d','YSYX-Linux','-u','ysyx','--exec','python3','/workspace/projects/ysyx_f_to_b/E/runtime/check_wsl_idle.py'],capture_output=True);assert check.returncode==0,decode(check.stdout)+decode(check.stderr)
    idle=json.loads(decode(check.stdout));assert idle['status']=='IDLE'
    shutdown=run('E8/memory/restart',['wsl','--shutdown'],timeout=30);assert shutdown['status']=='PASS'
    process=subprocess.run(command,capture_output=True,timeout=60);assert process.returncode==0,decode(process.stderr);memory=json.loads(decode(process.stdout));assert memory['MemTotal']>=3584*1024,memory
    d.update(status='APPLIED_AND_VERIFIED',running_distributions_before=names,idle_guard=idle,actual_linux_memory_KiB=memory,applied_at=datetime.now(timezone.utc).isoformat(),restart_stderr=decode(process.stderr));dump(record,d);print(json.dumps(d,ensure_ascii=False),flush=True)
if __name__=='__main__':main()

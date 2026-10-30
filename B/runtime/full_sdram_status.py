"""Read live process identity as well as files; stale progress is never RUNNING."""
from pathlib import Path
import json,datetime

ROOT=Path('/workspace/projects/ysyx_f_to_b')
FOLDER=ROOT/'artifacts/B4/parallel-sdram/release-full128'

def read(path):return json.loads(path.read_text()) if path.exists() else None
def live(pid,required):
    try:
        proc=Path('/proc')/str(pid);state=(proc/'stat').read_text().rsplit(')',1)[1].split()[0]
        command=(proc/'cmdline').read_bytes().decode(errors='replace').split('\0')
        return state!='Z' and all(str(value) in command for value in required)
    except (FileNotFoundError,ProcessLookupError,PermissionError):return False

def main():
    driver=read(FOLDER/'driver/run.json');started=read(FOLDER/'driver/started.json');rows=[]
    finished=bool(driver and (not started or driver.get('timestamp','')>=started.get('timestamp','')))
    active=bool(started and live(started.get('pid'),[str(ROOT/'B/runtime/budget_exec.py')]))
    state=driver['status'] if finished else 'RUNNING' if active else 'UNKNOWN_NO_LIVE_DRIVER'
    for phase in range(8):
        folder=FOLDER/f'phase-{phase}';record=read(folder/'run.json');launch=read(folder/'started.json')
        done=bool(record and (not launch or record.get('timestamp','')>=launch.get('timestamp','')))
        running=bool(launch and live(launch.get('pid'),[str(folder/'simulation.json')]))
        row={'phase':phase,'status':record['status'] if done else 'RUNNING' if running else 'NOT_COMPLETED'}
        if running:
            lines=(folder/'stderr.log').read_text(errors='replace').splitlines();progress=next((x for x in reversed(lines) if x.startswith('C5_PROGRESS')),'no progress frame yet');row['progress']=progress
        if done:row['seconds']=round(record['elapsed_seconds'],2)
        rows.append(row)
    print(json.dumps({'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'driver':state,'driver_live':active,'phases':rows},ensure_ascii=False),flush=True)

if __name__=='__main__':main()

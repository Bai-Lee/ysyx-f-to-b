"""Launch independently bounded gate-level program checks after a passing pilot."""
from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    p=argparse.ArgumentParser();p.add_argument('--program',required=True,choices=['microbench','rtthread']);a=p.parse_args()
    proof=json.loads((ROOT/'reports/B5_netlist.json').read_text());timing=json.loads((ROOT/'reports/B5_final_timing.json').read_text())
    assert proof['netlist_sha256']==timing['netlist_sha256'] and any(r['name']=='hello' and r['status']=='PASS' for r in proof['runs'])
    source=ROOT/'B/B5/verify_design.py'
    for proc in Path('/proc').glob('[0-9]*'):
        try:cmd=(proc/'cmdline').read_bytes().decode(errors='replace').split('\0')
        except (FileNotFoundError,ProcessLookupError,PermissionError):continue
        if str(source) in cmd and '--program' in cmd and cmd[cmd.index('--program')+1]==a.program:raise RuntimeError('Program already running: '+proc.name)
    folder=ROOT/'artifacts/B5/gate-jobs'/a.program;folder.mkdir(parents=True,exist_ok=True);stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    command=['python3',source,'--mode','netlist','--program',a.program,'--fast-memory']
    stdout=folder/(stamp+'.stdout.log');stderr=folder/(stamp+'.stderr.log')
    with stdout.open('xb') as out,stderr.open('xb') as err:process=subprocess.Popen(list(map(str,command)),cwd=WORK,stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True,close_fds=True)
    dump(folder/(stamp+'.json'),{'status':'LAUNCHED_NOT_ACCEPTED','pid':process.pid,'command':list(map(str,command)),'stdout':str(stdout),'stderr':str(stderr),'netlist_sha256':timing['netlist_sha256'],'scope':'Complete test-scale program, Icarus four-state functional memory, no instruction truncation. Each simulator registers one slot under the shared B memory guard.'})
    print('GATE_PROGRAM_LAUNCHED',a.program,process.pid)
if __name__=='__main__':main()

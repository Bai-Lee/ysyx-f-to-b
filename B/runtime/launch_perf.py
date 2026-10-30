"""Launch a bounded validated performance run with no terminal dependency."""
from common import *
import argparse
from resource_policy import windows_available_bytes,load_policy

def main():
    p=argparse.ArgumentParser();p.add_argument('--variant',required=True);p.add_argument('--frequency-mhz',type=int,default=400);p.add_argument('--padding',type=int,default=0);a=p.parse_args()
    pilot=next(r for r in json.loads((ROOT/'reports/B3_performance.json').read_text())['runs'] if r['variant']==a.variant and r['size']=='test' and r.get('padding',0)==a.padding)
    assert pilot['status']=='PASS'
    worker=ROOT/'B/B3/perf.py'
    for proc in Path('/proc').glob('[0-9]*'):
        try:cmd=(proc/'cmdline').read_bytes().decode(errors='replace').split('\0')
        except (FileNotFoundError,ProcessLookupError,PermissionError):continue
        if str(worker) in cmd and '--variant' in cmd and cmd[cmd.index('--variant')+1]==a.variant:raise RuntimeError('The same performance variant is already running: '+proc.name)
    assert windows_available_bytes()>=load_policy()['windows_start_available_mib']*1024**2
    folder=ROOT/'artifacts/B3/performance-jobs'/a.variant;folder.mkdir(parents=True,exist_ok=True);stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    command=['python3',worker,'--variant',a.variant,'--size','train','--frequency-mhz',str(a.frequency_mhz),'--padding',str(a.padding)]
    stdout=folder/(stamp+'.stdout.log');stderr=folder/(stamp+'.stderr.log')
    with stdout.open('xb') as o,stderr.open('xb') as e:
        process=subprocess.Popen(list(map(str,command)),cwd=WORK,stdin=subprocess.DEVNULL,stdout=o,stderr=e,start_new_session=True,close_fds=True)
    record={'status':'LAUNCHED_NOT_ACCEPTED','pid':process.pid,'command':list(map(str,command)),'stdout':str(stdout),'stderr':str(stderr),'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'timestamp':stamp,'pilot_cycles':pilot['simulation']['cycles'],'pilot_wall_seconds':pilot['simulation']['wall_seconds'],'scope':'Task-local background worker. Child simulator is registered with the aggregate6GiB B guard. No service or scheduled automation; completion is accepted only from final run/report assertions.'}
    dump(folder/(stamp+'.json'),record);print(json.dumps(record),flush=True)
if __name__=='__main__':main()

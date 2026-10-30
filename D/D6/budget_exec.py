"""Bound resident memory of a process group; leave virtual mappings unrestricted."""
import argparse,os,signal,subprocess,time,json
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('--rss-mib',type=int,default=1100);p.add_argument('--metric',choices=['rss','pss'],default='rss');p.add_argument('--report',required=True);p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args();command=a.command[1:] if a.command[:1]==['--'] else a.command
 child=subprocess.Popen(command,start_new_session=True);start=time.monotonic();peak=peak_pss=0;low=0;reason=None;minimum_available=None;timeline=[]
 def stop(signum,frame):
  nonlocal reason
  reason='PARENT_TERMINATED';os.killpg(child.pid,signal.SIGTERM)
 signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
 while child.poll() is None:
  rss=pss=0
  for proc in Path('/proc').glob('[0-9]*'):
   try:
    fields=(proc/'stat').read_text().rsplit(')',1)[1].split()
    if int(fields[2])==child.pid:
     current=int(fields[21])*os.sysconf('SC_PAGE_SIZE');rss+=current
     try:pss+=int(next(s.split()[1] for s in (proc/'smaps_rollup').read_text().splitlines() if s.startswith('Pss:')))*1024
     except (FileNotFoundError,ProcessLookupError,PermissionError,StopIteration):pss+=current
   except (FileNotFoundError,ProcessLookupError,PermissionError,ValueError):pass
  peak=max(peak,rss);peak_pss=max(peak_pss,pss);available=int(next(s.split()[1] for s in Path('/proc/meminfo').read_text().splitlines() if s.startswith('MemAvailable:')))*1024
  minimum_available=available if minimum_available is None else min(minimum_available,available)
  measured=rss if a.metric=='rss' else pss
  if not timeline or time.monotonic()-start-timeline[-1]['elapsed_seconds']>=5:timeline.append({'elapsed_seconds':time.monotonic()-start,'rss_bytes':rss,'pss_bytes':pss,'available_bytes':available})
  low=low+1 if measured>a.rss_mib*1024**2 else 0
  if low>=3 or available<192*1024**2:
   reason='RESOURCE_LIMIT';os.killpg(child.pid,signal.SIGTERM)
  if reason:
   try:child.wait(timeout=5)
   except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
   break
  time.sleep(.5)
 rc=child.wait();path=Path(a.report);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps({'status':reason or ('PASS' if rc==0 else 'CHILD_FAILURE'),'exit_code':rc,'elapsed_seconds':time.monotonic()-start,'peak_group_rss_bytes':peak,'peak_group_pss_bytes':peak_pss,'metric':a.metric,'memory_limit_bytes':a.rss_mib*1024**2,'minimum_system_available_bytes':minimum_available,'timeline':timeline,'command':command},indent=2))
 return 125 if reason=='RESOURCE_LIMIT' else 143 if reason else rc
if __name__=='__main__':raise SystemExit(main())

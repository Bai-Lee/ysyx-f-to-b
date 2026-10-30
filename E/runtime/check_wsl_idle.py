"""Read-only guard before the authorized WSL memory-limit restart."""
from pathlib import Path
import os,json
allowed={os.getpid(),1};pid=os.getpid()
while pid>1:
 fields=Path('/proc',str(pid),'stat').read_text().rsplit(')',1)[1].split();pid=int(fields[1]);allowed.add(pid)
unexpected=[]
for proc in Path('/proc').glob('[0-9]*'):
 try:
  pid=int(proc.name);command=(proc/'comm').read_text().strip();args=(proc/'cmdline').read_bytes()
  if pid in allowed or not args or command in ['init','Relay']:continue
  unexpected.append({'pid':pid,'command':command})
 except (FileNotFoundError,ProcessLookupError,PermissionError):pass
print(json.dumps({'status':'IDLE' if not unexpected else 'BUSY','unexpected_processes':unexpected}))
raise SystemExit(0 if not unexpected else 2)

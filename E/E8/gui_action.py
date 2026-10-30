from pathlib import Path
import sys,os,json,subprocess,time,re,datetime
root=Path('/workspace/projects/ysyx_f_to_b');dest=root/'artifacts/E8/gui';state=json.loads((dest/'session-started.json').read_text());env=os.environ.copy();env['DISPLAY']=state['display'];mode=sys.argv[1]
if not state.get('xauthority'):
 values=(Path('/proc')/str(state['pid'])/'environ').read_bytes().split(b'\0');state['xauthority']=next(x.split(b'=',1)[1].decode() for x in values if x.startswith(b'XAUTHORITY='));(dest/'session-started.json').write_text(json.dumps(state,indent=2))
env['XAUTHORITY']=state['xauthority']
name=subprocess.check_output(['xdotool','getwindowname',state['window_id']],env=env,text=True);owner=int(subprocess.check_output(['xdotool','getwindowpid',state['window_id']],env=env,text=True));assert owner==state['pid'],(name,owner)
if mode=='click':command=['xdotool','mousemove',sys.argv[2],sys.argv[3],'click','1']
elif mode=='key':command=['xdotool','key','--clearmodifiers',sys.argv[2]]
elif mode=='type':command=['xdotool','type','--clearmodifiers','--delay','1',sys.argv[2]]
elif mode=='scroll':
 count=int(sys.argv[2]);assert 1<=count<=20;command=['xdotool','mousemove','1100','800','click','--repeat',str(count),'--delay','50','5']
elif mode=='shot':
 assert re.fullmatch(r'[a-zA-Z0-9_-]+',sys.argv[2]);time.sleep(1);command=['scrot','-o',str(dest/(sys.argv[2]+'.png'))]
else:raise ValueError(mode)
result=subprocess.run(command,env=env,capture_output=True,text=True,timeout=15);record={'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':command,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr};file=dest/'interactions.json';rows=json.loads(file.read_text()) if file.exists() else [];rows.append(record);file.write_text(json.dumps(rows,indent=2));assert result.returncode==0,result.stderr;print(mode,'OK',flush=True)

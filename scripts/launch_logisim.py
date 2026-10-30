from evidence import *
policy=ROOT/'config/execution_policy.json'
if policy.exists() and json.loads(policy.read_text('utf8')).get('allow_logisim_gui') is False:
    raise SystemExit('Logisim GUI route disabled by user. Use command-line RTL or native headless validation.')
cfg=json.loads((ROOT/'config/toolchain.json').read_text('utf8'));classes=ROOT/'temp/java-classes'
cmd=[cfg['java']['executable'],'-Xmx512m','-Duser.language=en','-Duser.country=US','-Dfile.encoding=UTF-8','-Djava.util.prefs.PreferencesFactory=LocalPrefsFactory','-cp',str(classes)+';'+cfg['logisim']['jar'],'com.cburch.logisim.Main','--locale','en','--no-splash','--geometry','1300x900']
if len(sys.argv)>1:cmd.append(sys.argv[1])
out=(ROOT/'artifacts/logisim_gui.stdout.log').open('ab');err=(ROOT/'artifacts/logisim_gui.stderr.log').open('ab')
child=subprocess.Popen(cmd,cwd=ROOT,stdout=out,stderr=err,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0));dump(ROOT/'artifacts/logisim_gui_process.json',{'pid':child.pid,'command':cmd,'cwd':str(ROOT),'purpose':'F2 and F3 GUI circuit operations; process-local preferences only'});print('LOGISIM_GUI_PID',child.pid)

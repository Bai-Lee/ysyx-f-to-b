"""Open the real ECOS desktop on the completed CPU workspace for visual review."""
from pathlib import Path
import sys,select
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 root=Path('/home/USER/tools/e-stage/ecos-alpha9/squashfs-root');workspace=WORK/'physical/cpu_baseline';dest=ROOT/'artifacts/E8/gui';dest.mkdir(exist_ok=True)
 if (dest/'session-started.json').exists():
  prior=dest/'attempts'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f');prior.mkdir(parents=True)
  for file in dest.iterdir():
   if file.is_file():shutil.copyfile(file,prior/file.name)
 close_request=dest/'close.request';close_request.unlink(missing_ok=True)
 assert json.loads((ROOT/'reports/E8_signoff_cpu_baseline.json').read_text())['status'] in ['attention','ready']
 profile=WORK/'ecos_gui_profile';env=os.environ.copy();env.update(XDG_CONFIG_HOME=str(profile/'config'),XDG_CACHE_HOME=str(profile/'cache'),LIBGL_ALWAYS_SOFTWARE='1',CUDA_VISIBLE_DEVICES='',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PATH='/home/USER/tools/e-stage/oss-20260821/oss-cad-suite/bin:'+env['PATH'])
 runtime=profile/'runtime';runtime.mkdir(parents=True,exist_ok=True);runtime.chmod(0o700);env.update(XDG_RUNTIME_DIR=str(runtime),ECOS_GPU_CANVAS='0');env.pop('WAYLAND_DISPLAY',None)
 libraries=Path('/home/USER/tools/e-stage/gui-libs/usr/lib/x86_64-linux-gnu')
 if libraries.exists():env.update(LD_LIBRARY_PATH=str(libraries)+':'+str(root),VK_ICD_FILENAMES=str(root/'vk_swiftshader_icd.json'))
 command=[str(root/'ecos-studio'),str(workspace),'--disable-gpu','--disable-dev-shm-usage'];start=time.monotonic();commands=[]
 with (dest/'stdout.log').open('wb') as out,(dest/'stderr.log').open('wb') as err:
  app=subprocess.Popen(command,cwd=WORK,env=env,stdout=out,stderr=err,start_new_session=True)
  def call(args):
   r=subprocess.run(args,env=env,capture_output=True,text=True,timeout=15);commands.append({'command':args,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr});assert r.returncode==0,r.stderr;return r.stdout
  try:
   window=None
   for _ in range(200):
    found=subprocess.run(['xdotool','search','--onlyvisible','--name','ECOS'],env=env,capture_output=True,text=True)
    if found.returncode==0:window=found.stdout.splitlines()[-1];break
    assert app.poll() is None,(app.returncode,(dest/'stderr.log').read_text()[-2500:]);time.sleep(.2)
   assert window,'ECOS window not found';call(['xdotool','windowsize',window,'1500','1000']);call(['xdotool','windowmove',window,'40','30']);call(['xdotool','windowfocus','--sync',window]);time.sleep(10);call(['scrot','-o',str(dest/'initial.png')])
   state={'status':'OPEN_PENDING_VISUAL_REVIEW','display':env.get('DISPLAY'),'window_id':window,'pid':app.pid,'command':command,'workspace':str(workspace),'executable_sha256':sha(root/'ecos-studio-bin'),'initial_image_sha256':sha(dest/'initial.png'),'commands':commands};dump(dest/'session-started.json',state);print('ECOS_GUI_READY',json.dumps(state),flush=True)
   deadline=time.monotonic()+900
   while app.poll() is None and time.monotonic()<deadline:
    if close_request.exists():break
    time.sleep(.2)
  finally:
   if app.poll() is None:
    try:call(['xdotool','key','--window',window,'ctrl+q']);app.wait(timeout=10)
    except Exception:
     try:os.killpg(app.pid,signal.SIGTERM)
     except ProcessLookupError:pass
     try:app.wait(timeout=10)
     except subprocess.TimeoutExpired:os.killpg(app.pid,signal.SIGKILL);app.wait()
  dump(dest/'session-end.json',{'status':'CLOSED','exit_code':app.returncode,'elapsed_seconds':time.monotonic()-start,'commands':commands,'stdout_sha256':sha(dest/'stdout.log'),'stderr_sha256':sha(dest/'stderr.log')})
  close_request.unlink(missing_ok=True)
 print('ECOS_GUI_SESSION_CLOSED',flush=True)
if __name__=='__main__':main()

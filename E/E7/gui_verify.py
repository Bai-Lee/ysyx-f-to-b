from common7 import *
from software_soc import SOFT
import signal,re
def main():
 d=ROOT/'artifacts/E7/gui';d.mkdir(exist_ok=True)
 if (d/'run.json').exists():
  prior=d/'attempts'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f');prior.mkdir(parents=True)
  for f in d.iterdir():
   if f.is_file():shutil.copyfile(f,prior/f.name)
 exe=WORK/'build/E7/soc_gui/sim';image=SOFT/'programs/gpio/build/gpio-minirv-ysyxsoc.bin';report=d/'result.json';commands=[]
 env=os.environ.copy();env.update(NVBOARD_HOME=str(BENCH7/'nvboard'),SDL_RENDER_DRIVER='software',SDL_AUDIODRIVER='dummy',SHELL='/bin/bash')
 def cmd(args):
  r=subprocess.run(args,env=env,capture_output=True,text=True,timeout=10);commands.append({'command':args,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr});assert r.returncode==0,r.stderr;return r.stdout
 out=(d/'stdout.log').open('wb');err=(d/'stderr.log').open('wb');start=time.monotonic()
 args=[str(exe),'--image',str(image),'--report',str(report),'--gui','--hold-gui','--ratio','1','--max-cycles','2000000000']
 proc=subprocess.Popen(args,env=env,cwd=WORK,stdout=out,stderr=err,stdin=subprocess.PIPE,start_new_session=True)
 def wait_text(s,timeout):
  end=time.monotonic()+timeout
  while time.monotonic()<end:
   if s in (d/'stdout.log').read_text(errors='replace'):return
   assert proc.poll() is None,(proc.returncode,(d/'stderr.log').read_text()[-1500:]);time.sleep(.1)
  raise AssertionError('Missing output '+s)
 try:
  window=None
  for i in range(150):
   q=subprocess.run(['xdotool','search','--onlyvisible','--name','^NVBoard'],env=env,capture_output=True,text=True)
   if q.returncode==0:window=q.stdout.splitlines()[-1];break
   assert proc.poll() is None;time.sleep(.1)
  assert window;cmd(['xdotool','windowfocus','--sync',window]);geo={k:int(v) for k,v in re.findall(r'^(X|Y|WIDTH|HEIGHT)=(\d+)$',cmd(['xdotool','getwindowgeometry','--shell',window]),re.M)}
  wait_text('LOCKED: set switches to A55A',600);time.sleep(.3);cmd(['scrot','-o',str(d/'locked.png')])
  mask=0
  def set_switches(value):
   nonlocal mask
   for i in range(16):
    if (mask^value)&(1<<i):
     x=round(geo['X']+(70+(15-i)*30)*geo['WIDTH']/1280);y=round(geo['Y']+420*geo['HEIGHT']/960)
     cmd(['xdotool','mousemove',str(x),str(y)]);cmd(['xdotool','mousedown','1']);time.sleep(.05);cmd(['xdotool','mouseup','1']);time.sleep(.05)
   mask=value
  set_switches(0xffff);time.sleep(1);assert 'UNLOCKED' not in (d/'stdout.log').read_text();cmd(['scrot','-o',str(d/'wrong_password.png')])
  set_switches(0xa55a);wait_text('UNLOCKED',180);time.sleep(.4);cmd(['scrot','-o',str(d/'walking.png')]);wait_text('SOC_DONE_HOLD',180);time.sleep(.6);cmd(['scrot','-o',str(d/'completed.png')])
  data=json.loads(report.read_text());assert data['result']=='GOOD_TRAP' and data['serial_matches'] and data['serial_framing_errors']==0
  gpio_reads=json.loads(Path(str(report)+'.switches.json').read_text());assert gpio_reads.get('65535',0)>=100 and gpio_reads.get(str(0xa55a),0)>0
  values=[x[1] for x in data['led_sequence']];assert values==[1<<i for i in range(16)]+[0xa55a],values
  patterns=['abcdef','bc','abdeg','abcdg','bcfg','acdfg','acdefg','abc','abcdefg','abcdfg','abcefg','cdefg','adef','bcdeg','adefg','aefg']
  def segment(digit):return 255-sum(1<<(7-('abcdefg'.index(letter))) for letter in patterns[digit])
  expected=[segment((26070001>>(4*i))&15) for i in range(8)];assert data['segments']==expected,(data['segments'],expected)
  assert Path(str(report)+'.uart.txt').read_bytes()==Path(str(report)+'.serial.txt').read_bytes()
  proc.stdin.write(b'q\n');proc.stdin.flush();rc=proc.wait(timeout=10);assert rc==0
 finally:
  if proc.poll() is None:os.killpg(proc.pid,signal.SIGTERM);proc.wait(timeout=5)
  out.close();err.close()
 result={'status':'PASS_PENDING_VISUAL_REVIEW','command':args,'exit_code':rc,'elapsed_seconds':time.monotonic()-start,'binary_sha256':sha(exe),'image_sha256':sha(image),'stdout_sha256':sha(d/'stdout.log'),'stderr_sha256':sha(d/'stderr.log'),'simulation':data,'wrong_password_read_count':gpio_reads['65535'],'switch_reads':gpio_reads,'project_id':26070001,'project_id_hex':f'{26070001:08x}','display':os.environ.get('DISPLAY'),'commands':commands,'screenshots':[{'file':str(f.relative_to(ROOT)),'sha256':sha(f)} for f in [d/'locked.png',d/'wrong_password.png',d/'walking.png',d/'completed.png']],'scope':'Real upstream NVBoard, actual GPIO switches clicked through X11, UART decoded from actual SoC TX pins and displayed, LEDs/segments driven by actual compiled software/MMIO.'}
 dump(ROOT/'reports/E7_gui.json',result);dump(d/'run.json',result);print('E7_GUI_RUNTIME_PASS_PENDING_VISUAL_REVIEW',flush=True)
if __name__=='__main__':main()

from pathlib import Path
import sys,ctypes,signal,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def child():
    d=ROOT/'artifacts/D8/keyboard/session';d.mkdir(parents=True,exist_ok=True)
    if (d/'started.json').exists():
        history=d/'attempts'/str(time.time_ns());history.mkdir(parents=True)
        for p in list(d.iterdir()):
            if p.is_file():shutil.copyfile(p,history/p.name)
    exe=BENCH/'am-kernels/tests/am-tests/build/amtest-native.elf';env=os.environ.copy();env.update(SDL_AUDIODRIVER='dummy',SDL_RENDER_DRIVER='software',mainargs='k')
    log=(d/'stdout.log').open('wb');err=(d/'stderr.log').open('wb');command=['stdbuf','-oL',str(exe)];start=time.monotonic()
    proc=subprocess.Popen(command,env=env,cwd=WORK,stdout=log,stderr=err,start_new_session=True)
    dump(d/'started.json',{'command':command,'pid':proc.pid,'binary_sha256':sha(exe),'display':env.get('DISPLAY')})
    def terminate(signum,frame):raise SystemExit(143)
    signal.signal(signal.SIGTERM,terminate)
    commands=[]
    def invoke(args):
        q=subprocess.run(args,env=env,capture_output=True,text=True,timeout=10);commands.append({'command':args,'exit':q.returncode,'stdout':q.stdout,'stderr':q.stderr});assert q.returncode==0;return q.stdout
    try:
        window=None
        for _ in range(100):
            q=subprocess.run(['xdotool','search','--onlyvisible','--name','Native Application'],env=env,capture_output=True,text=True)
            if q.returncode==0:window=q.stdout.splitlines()[-1];break
            assert proc.poll() is None;time.sleep(.05)
        assert window;invoke(['xdotool','windowfocus','--sync',window])
        for key in ['j','Left']:
            invoke(['xdotool','keydown',key]);time.sleep(.15);invoke(['xdotool','keyup',key]);time.sleep(.15)
        # Request SDL's ordinary close path with WM_DELETE_WINDOW on this
        # program's window in the private Xvfb display; no user windows exist.
        class Data(ctypes.Union):_fields_=[('l',ctypes.c_long*5),('b',ctypes.c_char*20)]
        class Client(ctypes.Structure):_fields_=[('type',ctypes.c_int),('serial',ctypes.c_ulong),('send_event',ctypes.c_int),('display',ctypes.c_void_p),('window',ctypes.c_ulong),('message_type',ctypes.c_ulong),('format',ctypes.c_int),('data',Data)]
        class Event(ctypes.Union):_fields_=[('client',Client),('pad',ctypes.c_long*24)]
        x=ctypes.CDLL('libX11.so.6');x.XOpenDisplay.argtypes=[ctypes.c_char_p];x.XOpenDisplay.restype=ctypes.c_void_p
        display=x.XOpenDisplay(None);assert display
        x.XInternAtom.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_int];x.XInternAtom.restype=ctypes.c_ulong
        event=Event();event.client.type=33;event.client.send_event=1;event.client.display=display;event.client.window=int(window);event.client.format=32
        event.client.message_type=x.XInternAtom(display,b'WM_PROTOCOLS',0);event.client.data.l[0]=x.XInternAtom(display,b'WM_DELETE_WINDOW',0)
        x.XSendEvent.argtypes=[ctypes.c_void_p,ctypes.c_ulong,ctypes.c_int,ctypes.c_long,ctypes.POINTER(Event)];x.XSendEvent.restype=ctypes.c_int
        assert x.XSendEvent(display,int(window),0,0,ctypes.byref(event));x.XFlush.argtypes=[ctypes.c_void_p];x.XFlush(display);x.XCloseDisplay.argtypes=[ctypes.c_void_p];x.XCloseDisplay(display)
        rc=proc.wait(timeout=10);assert rc==0
    finally:
        if proc.poll() is None:os.killpg(proc.pid,signal.SIGTERM);proc.wait(timeout=5)
        log.close();err.close()
    text=(d/'stdout.log').read_text();events=re.findall(r'Got\s+\(kbd\):\s+(\w+)\s+\((\d+)\)\s+(DOWN|UP)',text)
    for key in ['J','LEFT']:assert (key,'DOWN') in [(a,c) for a,b,c in events] and (key,'UP') in [(a,c) for a,b,c in events]
    result={'status':'PASS','binary_sha256':sha(exe),'exit_code':rc,'elapsed_seconds':time.monotonic()-start,'events':events,'commands':commands,'stdout_sha256':sha(d/'stdout.log'),'stderr_sha256':sha(d/'stderr.log'),'scope':'Unmodified official native AM keyboard program; real X11 J and Left down/up events and normal SDL quit in isolated Xvfb. Not a test of every keyboard layout or physical device.'}
    dump(d/'run.json',result);dump(ROOT/'reports/D8_native_keyboard.json',result)

def main():
    cwd=BENCH/'am-kernels/tests/am-tests';exe=cwd/'build/amtest-native.elf'
    run('D8/keyboard/build',['make','-j1','ARCH=native','mainargs=k'],cwd=cwd,inputs=[cwd/'Makefile',cwd/'src/tests/keyboard.c'],outputs=[exe],timeout=180)
    run('D8/keyboard/execute',['xvfb-run','-a','-s','-screen 0 1024x768x24','python3',Path(__file__),'--child'],inputs=[Path(__file__),exe],timeout=45)

if __name__=='__main__':child() if '--child' in sys.argv else main()

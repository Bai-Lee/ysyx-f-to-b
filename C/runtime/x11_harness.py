"""Only for an isolated Xvfb owned by a test; never searches the user display."""
import ctypes,os,signal,subprocess,time,shutil,json,hashlib
from pathlib import Path

def close_window(window):
    class Data(ctypes.Union):_fields_=[('l',ctypes.c_long*5),('b',ctypes.c_char*20)]
    class Client(ctypes.Structure):_fields_=[('type',ctypes.c_int),('serial',ctypes.c_ulong),('send_event',ctypes.c_int),('display',ctypes.c_void_p),('window',ctypes.c_ulong),('message_type',ctypes.c_ulong),('format',ctypes.c_int),('data',Data)]
    class Event(ctypes.Union):_fields_=[('client',Client),('pad',ctypes.c_long*24)]
    x=ctypes.CDLL('libX11.so.6');x.XOpenDisplay.argtypes=[ctypes.c_char_p];x.XOpenDisplay.restype=ctypes.c_void_p
    display=x.XOpenDisplay(None);assert display
    x.XInternAtom.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_int];x.XInternAtom.restype=ctypes.c_ulong
    event=Event();event.client.type=33;event.client.send_event=1;event.client.display=display;event.client.window=int(window);event.client.format=32
    event.client.message_type=x.XInternAtom(display,b'WM_PROTOCOLS',0);event.client.data.l[0]=x.XInternAtom(display,b'WM_DELETE_WINDOW',0)
    x.XSendEvent.argtypes=[ctypes.c_void_p,ctypes.c_ulong,ctypes.c_int,ctypes.c_long,ctypes.POINTER(Event)];x.XSendEvent.restype=ctypes.c_int
    assert x.XSendEvent(display,int(window),0,0,ctypes.byref(event))
    x.XFlush.argtypes=[ctypes.c_void_p];x.XFlush(display);x.XCloseDisplay.argtypes=[ctypes.c_void_p];x.XCloseDisplay(display)

class NativeSession:
    def __init__(self,exe,args,folder,env_extra=None,title='Native Application',command=None,cwd=None):
        assert os.environ.get('C_PRIVATE_XVFB')=='1','Use only from xvfb-run with the private-display flag.'
        self.folder=Path(folder);self.folder.mkdir(parents=True,exist_ok=True);self.commands=[]
        if (self.folder/'session.json').exists() or (self.folder/'stdout.log').exists():
            dest=self.folder/'attempts'/str(time.time_ns());dest.mkdir(parents=True)
            for p in list(self.folder.iterdir()):
                if p.is_file():shutil.copyfile(p,dest/p.name)
        self.env=os.environ.copy();self.env.update(mainargs=args,SDL_AUDIODRIVER='dummy',SDL_RENDER_DRIVER='software',SHELL='/bin/bash')
        if env_extra:self.env.update(env_extra)
        self.out=(self.folder/'stdout.log').open('wb');self.err=(self.folder/'stderr.log').open('wb');self.start=time.monotonic()
        self.command=['stdbuf','-oL',*map(str,command)] if command else ['stdbuf','-oL',str(exe)]
        self.proc=subprocess.Popen(self.command,env=self.env,stdout=self.out,stderr=self.err,start_new_session=True,cwd=cwd or self.folder)
        self.window=None
        for _ in range(100):
            q=subprocess.run(['xdotool','search','--onlyvisible','--name',title],env=self.env,capture_output=True,text=True)
            if q.returncode==0:self.window=q.stdout.splitlines()[-1];break
            assert self.proc.poll() is None,'Native program exited before showing its window';time.sleep(.1)
        assert self.window,'No test window'
        self.call(['xdotool','windowfocus','--sync',self.window])
    def call(self,args):
        q=subprocess.run(list(map(str,args)),env=self.env,capture_output=True,text=True,timeout=10)
        self.commands.append({'command':list(map(str,args)),'exit_code':q.returncode,'stdout':q.stdout,'stderr':q.stderr});assert q.returncode==0,q.stderr
        return q.stdout
    def key(self,action,key):self.call(['xdotool',action,key])
    def capture(self,name):
        p=self.folder/(name+'.png');self.call(['scrot','-u','-o',p]);return p
    def finish(self,escape=False):
        if escape:self.key('key','Escape')
        else:close_window(self.window)
        rc=self.proc.wait(timeout=10);assert rc==0
        self.out.close();self.err.close()
        self.result={'status':'PASS','command':self.command,'mainargs':self.env['mainargs'],'display':self.env['DISPLAY'],'exit_code':rc,'elapsed_seconds':time.monotonic()-self.start,'commands':self.commands,'termination':'program Escape path' if escape else 'ordinary SDL WM_DELETE_WINDOW, bounded observation'}
        (self.folder/'session.json').write_text(json.dumps(self.result,indent=2));return self.result
    def cleanup(self):
        if self.proc.poll() is None:os.killpg(self.proc.pid,signal.SIGTERM);self.proc.wait(timeout=5)
        if not self.out.closed:self.out.close();self.err.close()

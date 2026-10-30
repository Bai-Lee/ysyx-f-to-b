"""Real X11/SDL/GTK interactions on an isolated xvfb-run display.

No substitute HTML board or synthesized waveform screenshot is used.
"""
from common import *
import re,signal

screens=[];sessions=[];commands=[]
def xd(*args):
    command=['xdotool',*map(str,args)];q=subprocess.run(command,capture_output=True,text=True,timeout=10)
    commands.append({'command':command,'exit_code':q.returncode,'stdout':q.stdout,'stderr':q.stderr})
    assert q.returncode==0,(command,q.stderr)
    return q.stdout
def window(name):
    end=time.monotonic()+8
    while time.monotonic()<end:
        q=subprocess.run(['xdotool','search','--onlyvisible','--name',name],capture_output=True,text=True)
        if q.returncode==0:return int(q.stdout.splitlines()[-1])
        time.sleep(.05)
    raise AssertionError('Window did not appear: '+name)
def geometry(w):
    return {k:int(v) for k,v in re.findall(r'^(X|Y|WIDTH|HEIGHT)=(\d+)$',xd('getwindowgeometry','--shell',w),re.M)}
def shot(name,w,led=None,extra=None):
    time.sleep(.12);p=OUT/'gui'/(name+'.png');g=geometry(w)
    if p.exists():
        history=OUT/'gui/history'/str(time.time_ns());history.mkdir(parents=True);shutil.copyfile(p,history/p.name)
    run('gui/capture_'+name,['scrot','-o',str(p)])
    screens.append({'name':name,'path':str(p.relative_to(ROOT)),'geometry':g,'led_expected':led,'sha256':sha(p),**(extra or {})});return p
class App:
    def __init__(self,mode,official=False):
        self.mode=mode;self.official=official;self.tag='official' if official else 'mode'+str(mode)
        self.base=OUT/'gui'/self.tag;self.base.mkdir(parents=True,exist_ok=True)
        if (self.base/'stdout.log').exists():
            history=self.base/'attempts'/str(time.time_ns());history.mkdir(parents=True)
            for n in ['stdout.log','stderr.log','session.json']:
                if (self.base/n).exists():shutil.copyfile(self.base/n,history/n)
        self.out=(self.base/'stdout.log').open('wb');self.err=(self.base/'stderr.log').open('wb')
        exe=NVBOARD/'example/build/top' if official else WORK/'build/lab_board/lab_board'
        self.cmd=[str(exe)] if official else [str(exe),str(mode),str(ROOT/'E/E4/data/f6_output.hex')]
        env=os.environ.copy();env['NVBOARD_HOME']=str(NVBOARD);env['SDL_RENDER_DRIVER']='software';env['SHELL']='/bin/bash'
        self.start=time.monotonic();self.p=subprocess.Popen(self.cmd,cwd=NVBOARD/'example' if official else WORK,env=env,stdout=self.out,stderr=self.err,stdin=subprocess.PIPE,start_new_session=True)
        self.w=window('^NVBoard');self.g=geometry(self.w);self.mask=0;xd('windowfocus','--sync',self.w)
        time.sleep(.15);assert self.p.poll() is None
    def state(self):
        lines=(self.base/'stdout.log').read_text(errors='replace').splitlines();states=[l for l in lines if l.startswith('STATE ')]
        assert states,lines[-4:]
        return {k:int(v) for k,v in re.findall(r'(\w+)=(\d+)(?: |$)',states[-1])}
    def wait(self,**values):
        end=time.monotonic()+4
        while time.monotonic()<end:
            s=self.state()
            if all(s.get(k)==v for k,v in values.items()):return s
            time.sleep(.01)
        raise AssertionError((self.tag,values,self.state()))
    def point(self,x,y):
        return round(self.g['X']+x*self.g['WIDTH']/1280),round(self.g['Y']+y*self.g['HEIGHT']/960)
    def click(self,x,y):
        # --sync waits for motion and can hang when the pointer is already here.
        xx,yy=self.point(x,y);xd('mousemove',xx,yy);xd('mousedown',1);time.sleep(.045);xd('mouseup',1);time.sleep(.045)
    def switches(self,mask):
        for i in range(12):
            if (self.mask^mask)&(1<<i):self.click(70+(15-i)*30,420)
        self.mask=mask
        if not self.official:self.wait(sw=mask)
    def step(self):self.click(535,265)
    def close(self):
        if self.p.poll() is None:
            if self.official:self.p.terminate()
            else:self.p.stdin.write(b'q\n');self.p.stdin.flush()
        rc=self.p.wait(timeout=5);self.out.close();self.err.close()
        # SDL may translate SIGTERM into SDL_QUIT, whose upstream handler exits0.
        expected=[0,-signal.SIGTERM] if self.official else [0];assert rc in expected,(self.tag,rc,(self.base/'stderr.log').read_text())
        row={'status':'PASS','command':self.cmd,'cwd':str(NVBOARD/'example' if self.official else WORK),'exit_code':rc,'expected_exit':expected,'stdout_sha256':sha(self.base/'stdout.log'),'stderr_sha256':sha(self.base/'stderr.log'),'binary_sha256':sha(self.cmd[0]),'elapsed_seconds':round(time.monotonic()-self.start,3),'bounded_stop':'Original infinite example sent SIGTERM after display/interaction; SDL_QUIT may yield normal exit0' if self.official else 'Own harness normal exit via stdin q','display':os.environ['DISPLAY']}
        dump(self.base/'session.json',row);sessions.append(row)
def main():
    (OUT/'gui').mkdir(exist_ok=True);app=None
    try:
        app=App(0,True);shot('official_before',app.w);app.switches(1);shot('official_after_switch',app.w,extra={'interaction':'Physical SDL switch toggled through X11 mouse event'});app.close();app=None
        for mode in [0,1,2,3,4,5,6,7,8,9,10]:
            app=App(mode)
            if mode==0:
                for value,led in [(0,0),(1,1),(3,0),(2,1)]:
                    app.switches(value);app.wait(led=led);shot('dual_'+str(value),app.w,led)
            elif mode==1:
                for value,led in [(256,0),(270,19),(384,23)]:
                    app.switches(value);app.wait(led=led);shot('encoder_'+str(value),app.w,led)
            elif mode==2:
                for value,led in [(0x17,40),(0x178,49),(0x678,129),(0x788,1)]:
                    app.switches(value);app.wait(led=led);shot('alu_'+str(value),app.w,led)
            elif mode==3:
                for led in [128,64,32,16,136]:app.step();app.wait(led=led)
                shot('lfsr',app.w,136)
            elif mode==4:
                app.switches(0x181);app.step();app.wait(led=129)
                app.switches(0x400);app.step();app.wait(led=192);shot('shift',app.w,192)
            elif mode==5:
                app.switches(1)
                for _ in range(4):app.step()
                app.wait(led=65);shot('fsm_four_zeros',app.w,65)
                app.step();app.wait(led=65)
                app.switches(3);app.step();app.wait(led=80)
                for _ in range(3):app.step()
                app.wait(led=129);shot('fsm_four_ones',app.w,129)
            elif mode==6:
                xd('keydown','a');app.wait(key=28,ascii=97,active=1,count=1);time.sleep(.8);app.wait(count=1);shot('keyboard_a',app.w,0,{'key':28,'ascii':97,'count':1,'active':1})
                xd('keyup','a');app.wait(active=0,key=0,ascii=0,count=1);shot('keyboard_release',app.w,0,{'active':0})
                xd('keydown','Shift_L');app.wait(mods=1);xd('keydown','w');app.wait(key=29,ascii=87,count=2);shot('keyboard_shift_w',app.w,1,{'ascii':87,'count':2})
                xd('keyup','w');xd('keyup','Shift_L');app.wait(active=0,mods=0)
                xd('keydown','Control_L');app.wait(mods=2);shot('keyboard_ctrl',app.w,2);xd('keyup','Control_L');app.wait(mods=0)
            elif mode==7:
                time.sleep(.5);shot('vga_static',app.w,0,{'vga_pattern':True})
            elif mode==8:
                time.sleep(.25);first=app.state();shot('vga_moving_1',app.w,0,{'motion_state':first});time.sleep(.75);second=app.state();assert (first['x'],first['y'])!=(second['x'],second['y']);shot('vga_moving_2',app.w,0,{'motion_state':second})
            elif mode==9:
                app.wait(led=55);shot('cpu_sum55',app.w,55)
            else:
                end=time.monotonic()+6;seen=[]
                while time.monotonic()<end and len(seen)<5:
                    val=app.state()['led']
                    if not seen or val!=seen[-1]:seen.append(val)
                    time.sleep(.02)
                assert len(seen)>=5 and all(v and v&(v-1)==0 for v in seen)
                assert all(b==((a<<1)|(a>>15))&65535 for a,b in zip(seen,seen[1:]))
                shot('running_light',app.w,extra={'observed_sequence':seen})
            app.close();app=None
        # API commands come from the installed official GTKWave des.tcl example.
        script=OUT/'gui/wave.tcl';script.write_text('''set selected [list]
set n [gtkwave::getNumFacs]
for {set i 0} {$i<$n} {incr i} {
 set name [gtkwave::getFacName $i]
 puts "FAC $name"
 if {[regexp {^TOP\\.(a|b|f)$} $name]} {lappend selected $name}
}
set added [gtkwave::addSignalsFromList $selected]
puts "SIGNALS_ADDED $added"
gtkwave::/Edit/Set_Trace_Max_Hier 0
gtkwave::/Time/Zoom/Zoom_Full
gtkwave::setMarker 30
flush stdout
''')
        for ext in ['vcd','fst']:
            base=OUT/'gui'/('gtkwave_'+ext);base.mkdir(exist_ok=True)
            with (base/'stdout.log').open('wb') as o,(base/'stderr.log').open('wb') as e:
                cmd=['gtkwave','-f',str(OUT/'waves'/('dual.'+ext)),'-S',str(script),'-4','splash_disable 1']
                p=subprocess.Popen(cmd,stdout=o,stderr=e,env=os.environ.copy())
                try:
                    w=window('GTKWave');time.sleep(.4);shot('gtkwave_'+ext,w)
                    text=(base/'stdout.log').read_text();assert 'SIGNALS_ADDED 3' in text,text
                finally:p.terminate();rc=p.wait(timeout=5)
            dump(base/'session.json',{'status':'PASS','command':cmd,'exit_code':rc,'expected_exit':[rc],'bounded_stop':'Viewer intentionally closed after Tcl signal loading and screenshot','stdout_sha256':sha(base/'stdout.log'),'stderr_sha256':sha(base/'stderr.log')})
        dump(ROOT/'reports/E4_gui.json',{'status':'PASS_RUNTIME_PENDING_PIXEL_REVIEW','display':'isolated Xvfb1600x1200, real GTKWave and upstream SDL NVBoard','screens':screens,'sessions':sessions,'commands':commands,'gui_portability':'Virtual X display, not physical FPGA or WSLg/Windows desktop automation.'})
        print('GUI_RUNTIME_PASS',len(screens),flush=True)
    finally:
        if app is not None and app.p.poll() is None:app.p.terminate();app.p.wait(timeout=5);app.out.close();app.err.close()
        dump(OUT/'gui/progress.json',{'screens':screens,'sessions':sessions,'commands':commands})
if __name__=='__main__':main()

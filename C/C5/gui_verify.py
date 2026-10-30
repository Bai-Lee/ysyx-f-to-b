from pathlib import Path
import sys,argparse,re,signal
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from support import select_build
from x11_harness import NativeSession

DEFAULT_VARIANT='30000000-cycle-psram4m-qpi-sdram32x2-opt-gui'


def disable_private_repeat(environment):
    import ctypes
    assert os.environ.get('C_PRIVATE_XVFB')=='1' and environment['DISPLAY']==os.environ['DISPLAY']
    class KeyboardState(ctypes.Structure):
        _fields_=[('key_click_percent',ctypes.c_int),('bell_percent',ctypes.c_int),('bell_pitch',ctypes.c_uint),('bell_duration',ctypes.c_uint),('led_mask',ctypes.c_ulong),('global_auto_repeat',ctypes.c_int),('auto_repeats',ctypes.c_char*32)]
    library=ctypes.CDLL('libX11.so.6');library.XOpenDisplay.argtypes=[ctypes.c_char_p];library.XOpenDisplay.restype=ctypes.c_void_p
    display=library.XOpenDisplay(environment['DISPLAY'].encode());assert display
    library.XGetKeyboardControl.argtypes=[ctypes.c_void_p,ctypes.POINTER(KeyboardState)]
    library.XAutoRepeatOff.argtypes=[ctypes.c_void_p];library.XSync.argtypes=[ctypes.c_void_p,ctypes.c_int];library.XCloseDisplay.argtypes=[ctypes.c_void_p]
    before=KeyboardState();after=KeyboardState()
    try:
        library.XGetKeyboardControl(display,ctypes.byref(before));library.XAutoRepeatOff(display);library.XSync(display,0)
        library.XGetKeyboardControl(display,ctypes.byref(after));assert after.global_auto_repeat==0
    finally:library.XCloseDisplay(display)
    return {'display':environment['DISPLAY'],'api':'XAutoRepeatOff after SDL window initialization','before':before.global_auto_repeat,'after':after.global_auto_repeat,'scope':'Only this test-owned Xvfb server; user display is not accessed.'}


def target(case):
    if case in ['rtthread','rtbench','rtguard']:
        return json.loads((ROOT/'reports/C5_rtthread_apps_sdram128.json').read_text())
    name,memory,arguments={'gpio':('gpio-demo','sdram32',''),'keyboard':('am-tests','sdram32','k'),
        'video':('am-tests','sdram32','v'),'typing':('typing-game','sdram128',''),'fceux':('fceux','sdram128','interaction')}[case]
    return next(r for r in json.loads((ROOT/'reports/C5_app_builds.json').read_text())['builds'] if (r['name'],r['memory'],r['arguments'])==(name,memory,arguments))


class Session(NativeSession):
    def __init__(self,*args,**kwargs):
        try:super().__init__(*args,**kwargs)
        except BaseException:
            if hasattr(self,'proc'):self.cleanup()
            raise
    def click(self,x,y):
        self.call(['xdotool','mousemove',round(self.geometry['X']+x*self.geometry['WIDTH']/1280),round(self.geometry['Y']+y*self.geometry['HEIGHT']/960)])
        self.call(['xdotool','click','1'])
    def complete(self,trigger,expected_exit=0):
        rc=self.proc.wait(timeout=10);assert rc==expected_exit,rc
        self.out.close();self.err.close()
        result={'status':'COMPLETED_OBSERVATION','command':self.command,'display':self.env['DISPLAY'],'exit_code':rc,'elapsed_seconds':time.monotonic()-self.start,'commands':self.commands,'termination':trigger}
        dump(self.folder/'session.json',result);return result


def child(case,variant):
    import numpy as np
    from PIL import Image
    job=target(case);exe=Path(select_build(variant)['executable']);image=Path(job['image']);elf=Path(job['elf']);ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
    assert sha(image)==job['image_sha256'] and sha(elf)==job['elf_sha256']
    folder=ROOT/'artifacts/C5/gui'/case/'session';folder.mkdir(parents=True,exist_ok=True)
    simulation=folder/'simulation.json';resources=folder/'resources.json';ppm=folder/'last-frame.ppm';nvtx=folder/'nvboard-tx.bin';nvrx=folder/'nvboard-rx.bin'
    command=['python3',ROOT/'C/runtime/budget_exec.py','--report',resources,'--',exe,'--gui','--flash',image,'--ref',ref,'--report',simulation,'--vga-ppm',ppm,'--uart-bit-cycles','16','--max-cycles','100000000000','--progress-cycles','100000000']
    s=Session(exe,'',folder,title='^NVBoard',command=command,cwd=WORK/'c5',env_extra={'NVBOARD_HOME':str(WORK/'c5/nvboard'),'C5_NVBOARD_TX_LOG':str(nvtx),'C5_NVBOARD_RX_LOG':str(nvrx)})
    try:
        s.geometry={key:int(value) for key,value in re.findall(r'^(X|Y|WIDTH|HEIGHT)=(\d+)$',s.call(['xdotool','getwindowgeometry','--shell',s.window]),re.M)}
        input_policy=disable_private_repeat(s.env)
    except BaseException:
        s.cleanup();raise
    screenshots=[];observations={'input_policy':input_policy};completed=None
    def log():return (folder/'stdout.log').read_text(errors='replace').replace('\r','')
    def wait(predicate,seconds=300,interval=.25):
        end=time.monotonic()+seconds
        while time.monotonic()<end:
            if predicate():return
            if s.proc.poll() is not None:raise AssertionError('Simulator exited early: '+(folder/'stderr.log').read_text()[-1800:])
            time.sleep(interval)
        raise AssertionError('Observation deadline expired; no pass inferred from this timeout')
    def capture(name):
        path=s.capture(name);screenshots.append(path);return path
    def canvas(path):
        picture=Image.open(path).convert('RGB');w,h=picture.size
        return np.array(picture.crop((0,h//2,w//2,h)))
    def image_until(name,predicate,seconds=600):
        end=time.monotonic()+seconds;path=folder/(name+'.png')
        while time.monotonic()<end:
            assert s.proc.poll() is None,(folder/'stderr.log').read_text()[-2000:]
            s.capture(name);pixels=canvas(path)
            if predicate(pixels):screenshots.append(path);return pixels
            time.sleep(2)
        raise AssertionError('No qualifying native NVBoard image before deadline')
    def type_command(text):
        wait(lambda:log().rstrip().endswith('msh />'),seconds=240)
        time.sleep(.2)
        echo='msh />'+text+'\n';previous_echoes=log().count(echo)
        s.click(900,220);s.call(['xdotool','type','--clearmodifiers','--delay','120',text]);s.key('key','Return')
        wait(lambda:log().count(echo)>previous_echoes,seconds=60)
    def keyboard_focus():s.click(1080,900)
    def stable_game(name):
        previous=None;stable=0
        def check(pixels):
            nonlocal previous,stable
            # The emulator first displays a uniform gray initialization rectangle.
            # The authored ROM's running checkerboard has many colored pixels.
            # Do not treat a slow-to-change startup screen as the released-button baseline.
            h,w=pixels.shape[:2];center=pixels[h*3//8:h*5//8,w*3//8:w*5//8]
            colored=np.max(center,axis=2).astype(int)-np.min(center,axis=2).astype(int)>16
            if np.count_nonzero(colored)<2000:
                previous=None;stable=0;return False
            stable=stable+1 if previous is not None and np.array_equal(previous,pixels) else 0
            previous=pixels.copy();return stable>=3
        return image_until(name,check,seconds=900)
    try:
        if case=='gpio':
            wait(lambda:'LOCKED: set switches to A55A' in log());time.sleep(.6);capture('locked')
            mask=0
            def switches(value):
                nonlocal mask
                for bit in range(16):
                    if (mask^value)&(1<<bit):s.click(70+(15-bit)*30,420);time.sleep(.07)
                mask=value
            switches(0xffff);time.sleep(1);assert 'UNLOCKED' not in log();capture('wrong-password')
            switches(0xa55a);wait(lambda:'UNLOCKED' in log());time.sleep(4);capture('walking')
            wait(lambda:'C5_GPIO_DONE' in log());time.sleep(.8);capture('complete')
            completed=s.finish();observations['password']='FFFF blocked;A55A continued through software MMIO polling'
        elif case=='keyboard':
            wait(lambda:'Try to press any key' in log());time.sleep(.5)
            s.click(900,220);s.call(['xdotool','type','--clearmodifiers','--delay','120','Za0?']);s.key('key','Return')
            wait(lambda:all('(%d)'%value in log() for value in [90,97,48,63,10]));capture('uart-input')
            keyboard_focus()
            for key in ['a','Escape','Prior']:
                s.key('keydown',key);time.sleep(.3);s.key('keyup',key);time.sleep(.3)
            wait(lambda:all(re.search(r'Got\s+\(kbd\):\s+'+key+r'\s+\(\d+\)\s+'+state,log()) for key in ['A','ESCAPE','PAGEUP'] for state in ['DOWN','UP']))
            time.sleep(.8);capture('ps2-input');completed=s.finish()
            observations['keyboard_events']=re.findall(r'Got\s+\(kbd\):\s+(\w+)\s+\((\d+)\)\s+(DOWN|UP)',log())
        elif case=='video':
            wait(lambda:log().count('FPS =')>=1,seconds=900);time.sleep(.7)
            first=canvas(capture('first-picture'));assert np.count_nonzero(np.any(first!=0,axis=2))>20000
            fps_count=log().count('FPS =');wait(lambda:log().count('FPS =')>fps_count,seconds=900);time.sleep(.7)
            second=canvas(capture('animated-picture'))
            assert np.count_nonzero(np.any(first!=second,axis=2))>10000
            observations['changed_native_canvas_pixels']=int(np.count_nonzero(np.any(first!=second,axis=2)))
            observations['completed_program_fps_reports']=re.findall(r'(\d+): FPS = (\d+)',log())
            completed=s.finish()
        elif case=='typing':
            wait(lambda:log().count('Hit:')>=4,seconds=900);keyboard_focus();first=canvas(capture('before-hit'))
            # The unseeded original project RNG starts with Q; use actual PS/2 input.
            s.key('keydown','q');time.sleep(.4);s.key('keyup','q')
            wait(lambda:any(int(hit)>0 for hit in re.findall(r'Hit:\s*(\d+)',log())),seconds=180)
            time.sleep(.8);second=canvas(capture('after-hit'))
            observations.update({'hit_counts':[int(v) for v in re.findall(r'Hit:\s*(\d+)',log())],
                          'changed_native_canvas_pixels':int(np.count_nonzero(np.any(first!=second,axis=2)))})
            assert observations['changed_native_canvas_pixels']>5
            s.key('key','Escape');wait(lambda:s.proc.poll() is not None,seconds=180);completed=s.complete('Original typing-game Escape -> CPU GOOD_TRAP')
        elif case=='fceux':
            keyboard_focus();released=stable_game('released');s.key('keydown','j')
            pressed=image_until('pressed',lambda a:np.count_nonzero(np.any(a!=released,axis=2))>10000,seconds=900)
            # Wait for the complete stable rendered result before releasing the button.
            pressed=stable_game('pressed-stable');s.key('keyup','j')
            recovered=image_until('released-again',lambda a:np.count_nonzero(np.any(a!=released,axis=2))<100,seconds=900)
            observations.update({'changed_on_J':int(np.count_nonzero(np.any(pressed!=released,axis=2))),
                          'not_recovered_after_release':int(np.count_nonzero(np.any(recovered!=released,axis=2))),
                          'rom_sha256':sha(ROOT/'C/C2/homebrew/interaction.nes')})
            assert observations['changed_on_J']>10000
            s.key('key','Escape');wait(lambda:s.proc.poll() is not None,seconds=180);completed=s.complete('Original FCEUX Escape -> CPU GOOD_TRAP')
        elif case in ['rtbench','rtguard']:
            wait(lambda:'msh />utest_list' in log() and log().rstrip().endswith('msh />'),seconds=900)
            time.sleep(.5)
            if case=='rtbench':
                type_command('am_microbench test');wait(lambda:'C5_AM_EXIT name=microbench code=0' in log(),seconds=300)
                assert log().count(' Passed.')==10 and 'mode=private guards=1 allocator=-1' in log()
                type_command('am_hello reset');wait(lambda:'C5_AM_EXIT name=hello code=0' in log(),seconds=180)
                assert 'mode=klib guards=1 allocator=1' in log()
            else:
                type_command('c5_guard_test');wait(lambda:'C5_AM_EXIT name=guard_negative code=82' in log(),seconds=180)
                assert 'mode=private guards=0 allocator=-1' in log()
            time.sleep(.6);capture('heap-check');type_command('c5_done');wait(lambda:s.proc.poll() is not None,seconds=180)
            completed=s.complete('Explicitapplicationheapownership/guardtest',expected_exit=1 if case=='rtguard' else 0)
        elif case=='rtthread':
            wait(lambda:'msh />utest_list' in log(),seconds=900);time.sleep(.8);capture('scripted-boot')
            initial=log().count('RT-Thread shell commands:');type_command('help')
            wait(lambda:log().count('RT-Thread shell commands:')>initial,seconds=180)
            type_command('c5_no_such_command');wait(lambda:'c5_no_such_command' in log() and ('not found' in log().lower() or 'command not' in log().lower()),seconds=180)
            type_command('c5_context_test');wait(lambda:'C5_CONTEXT_PASS a=12 b=12' in log(),seconds=180);capture('interactive-shell')
            type_command('am_hello again');wait(lambda:'C5_AM_EXIT name=hello code=0' in log(),seconds=180)
            type_command('am_fceux interaction');wait(lambda:'C5_AM_START name=fceux' in log(),seconds=180)
            keyboard_focus();released=stable_game('rt-fceux-released');s.key('keydown','j')
            image_until('rt-fceux-pressed',lambda a:np.count_nonzero(np.any(a!=released,axis=2))>10000,seconds=900)
            s.key('keyup','j');s.key('key','Escape');wait(lambda:'C5_AM_EXIT name=fceux code=0' in log(),seconds=300)
            type_command('am_hello after');wait(lambda:log().count('C5_AM_EXIT name=hello code=0')>=2,seconds=180)
            type_command('am_microbench test');wait(lambda:'C5_AM_EXIT name=microbench code=0' in log(),seconds=600)
            assert log().count(' Passed.')==10 and 'MicroBench PASS' in log()
            time.sleep(.8);capture('returned-shell');observations['app_exits']=re.findall(r'C5_AM_EXIT name=(\w+) code=(\d+)',log())
            assert all(int(code)==0 for _,code in observations['app_exits'])
            type_command('c5_done');wait(lambda:s.proc.poll() is not None,seconds=180);completed=s.complete('Typed c5_done after real AMapp return to shell')
        else:raise ValueError(case)
        data=json.loads(simulation.read_text());assert data['result'] in (['BAD_TRAP'] if case=='rtguard' else ['GOOD_TRAP','GUI_OBSERVATION_STOP'])
        if case=='rtguard':assert data['a0']==84
        assert data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
        assert data['minimum_nonzero_sp']>=0x0f000000
        tx=bytes.fromhex(data['uart']['hex']);assert not data['uart']['capture_truncated']
        assert bytes.fromhex(data['uart_pin']['hex'])==tx and data['uart_pin']['framing_errors']==0
        assert nvtx.read_bytes()==tx,'NVBoard actual TX decoder differs from FIFO and independent pin decoder'
        rx=nvrx.read_bytes() if nvrx.exists() else b''
        assert bytes.fromhex(data['uart_rx_pin']['hex'])==rx and data['uart_rx_pin']['framing_errors']==0
        assert data['pins']['ps2_frame_errors']==0 and data['pins']['vga_frames']>0
        if 'ps2_queue' in data:
            assert data['ps2_queue']['dropped']==data['ps2_queue']['invalid']==0
            observations['ps2_queue']=data['ps2_queue']
        if case=='gpio':
            assert [value for _,value in data['pins']['led_changes']]==[1<<i for i in range(16)]+[0xa55a]
            reads=dict(data['pins']['switch_reads']);assert reads.get(0xffff,0)>=100 and reads.get(0xa55a,0)>0
            codes=[0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90,0x88,0x83,0xc6,0xa1,0x86,0x8e]
            assert data['pins']['segments']==[codes[(0x26070001>>(4*i))&15] for i in range(8)]
        if case in ['typing','fceux','rtthread','rtbench']:assert data['result']=='GOOD_TRAP'
        if case in ['fceux','rtthread']:
            assert sum(code==0x3b for _,code in data['pins']['ps2_scans'])==2,'One J make and one J break required'
        if case=='keyboard':assert rx==b'Za0?\n'
        record={'status':'PASS_PENDING_VISUAL_REVIEW','case':case,'variant':variant,'image_sha256':sha(image),'elf_sha256':sha(elf),'executable_sha256':sha(exe),'reference_sha256':sha(ref),'session':completed,'observations':observations,'simulation_summary':{key:data[key] for key in ['result','cycles','instructions','wall_seconds','diff_checked','device_sync_checked','minimum_nonzero_sp','pins','traps']},'uart_tx_bytes':len(tx),'uart_rx_bytes':len(rx),'screenshots':[{'path':str(path.relative_to(ROOT)),'sha256':sha(path)} for path in dict.fromkeys(screenshots)],'evidence':'artifacts/C5/gui/'+case,'scope':'Real upstream NVBoard on a privateXvfb display, X11mouse/key events, actual fullSoC pins, independentUARTdecoders, per-instructionNEMU. ControlledGUIclose is explicitly a bounded observation, not completion of an infinite program.'}
        dump(ROOT/('reports/C5_gui_'+case+'.json'),record);dump(folder/'acceptance.json',record)
        print('C5_GUI_RUNTIME_PASS_PENDING_VISUAL_REVIEW',case,flush=True)
    finally:
        if s.proc.poll() is None:s.cleanup()
        if not s.out.closed:s.out.close()
        if not s.err.closed:s.err.close()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('case',choices=['gpio','keyboard','video','typing','fceux','rtthread','rtbench','rtguard']);parser.add_argument('--variant',default=DEFAULT_VARIANT);parser.add_argument('--child',action='store_true');args=parser.parse_args()
    if args.child:child(args.case,args.variant);return
    job=target(args.case);exe=Path(select_build(args.variant)['executable'])
    run('C5/gui/'+args.case+'/launch',['xvfb-run','-a','-s','-screen 0 1600x1200x24 -nolisten tcp -r','env','C_PRIVATE_XVFB=1','python3',Path(__file__),'--child',args.case,'--variant',args.variant],inputs=[Path(__file__),exe,Path(job['image']),Path(job['elf']),WORK/'c5/nvboard/build/nvboard.a',ROOT/'C/runtime/x11_harness.py'],outputs=[ROOT/('reports/C5_gui_'+args.case+'.json')],timeout=3600)


if __name__=='__main__':main()

from pathlib import Path
import sys,re,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from x11_harness import NativeSession

def child():
    import numpy as np
    from PIL import Image
    name=sys.argv[sys.argv.index('--child')+1];folder=ROOT/'artifacts/C2/native'/name/'session';base=WORK/'c2-native'
    screen=name in ('solid','gradient');exe=base/('screensaver/build/screensaver-native.elf' if screen else 'am-tests/build/amtest-native.elf')
    arg={'solid':'solid-audit','gradient':'audit','timer':'t','keyboard':'k','video':'v'}[name]
    s=NativeSession(exe,arg,folder);observations={}
    def pixels(path):return np.asarray(Image.open(path).convert('RGB'))
    try:
        if name=='solid':
            time.sleep(.7);path=s.capture('blue');a=pixels(path);assert a.shape[:2]==(600,800),a.shape
            assert np.all(a==np.array([0,0,255],dtype=np.uint8)),'400x300 logical framebuffer must fill the scaled 800x600 native surface blue'
            observations={'logical_size':[400,300],'physical_capture_size':[800,600],'all_pixels_blue':True};s.finish(escape=True)
        elif name=='gradient':
            time.sleep(.8);first=s.capture('normal');s.key('keydown','j');time.sleep(1.05)
            second=s.capture('accelerated');s.key('keydown','Left');time.sleep(.3)
            s.key('keyup','j');time.sleep(.35);s.key('keyup','Left');time.sleep(.8);third=s.capture('released');s.finish(escape=True)
            log=(folder/'stdout.log').read_text();frames=[tuple(map(int,(a,b,int(c,16),d,e))) for a,b,c,d,e in re.findall(r'SCREEN_FRAME us=(\d+) step=(\d+) color=([0-9a-f]+) held=(\d+) interval=(\d+)',log)]
            medians={}
            for state in (0,1):
                deltas=[b[0]-a[0] for a,b in zip(frames,frames[1:]) if (a[3]>0)==bool(state) and (b[3]>0)==bool(state)]
                assert len(deltas)>=10;medians[state]=statistics.median(deltas)
            assert medians[0]/medians[1]>2.5,medians
            assert 'held=2' in log and re.search(r'SCREEN_KEY code=49 down=0 held=1',log) and re.search(r'SCREEN_KEY code=75 down=0 held=0',log)
            assert any(f[1]==120 for f in frames) and 'SCREEN_EXIT' in log
            assert np.count_nonzero(np.any(pixels(first)!=pixels(second),axis=2))>400000
            assert np.count_nonzero(np.any(pixels(second)!=pixels(third),axis=2))>400000
            observations={'frames':len(frames),'normal_median_us':medians[0],'held_median_us':medians[1],'measured_rate_ratio':medians[0]/medians[1],'multi_key_release_correct':True,'endpoint_seen':True}
        elif name=='timer':
            time.sleep(3.3);s.capture('timer_window');s.finish();log=(folder/'stdout.log').read_text()
            assert all(f'{n} second' in log for n in (1,2,3));observations={'observed_seconds':[1,2,3],'scope':'Infinite official app, bounded observation followed by normal SDL close.'}
        elif name=='keyboard':
            for key in ('j','Left'):
                s.key('keydown',key);time.sleep(.15);s.key('keyup',key);time.sleep(.15)
            s.finish();log=(folder/'stdout.log').read_text();events=re.findall(r'Got\s+\(kbd\):\s+(\w+)\s+\((\d+)\)\s+(DOWN|UP)',log)
            for key in ('J','LEFT'):
                for state in ('DOWN','UP'):assert (key,state) in [(a,c) for a,b,c in events]
            observations={'events':events}
        else:
            time.sleep(.8);p=s.capture('frame1');time.sleep(.5);q=s.capture('frame2');s.finish()
            a=pixels(p);b=pixels(q);changed=int(np.count_nonzero(np.any(a!=b,axis=2)));colors=len(np.unique(b.reshape(-1,3),axis=0))
            assert changed>100000 and colors>=128,(changed,colors);observations={'changed_pixels':changed,'unique_colors':colors}
        row={'status':'PASS','case':name,'executable_sha256':sha(exe),'observations':observations,'session':s.result,'stdout_sha256':sha(folder/'stdout.log'),'stderr_sha256':sha(folder/'stderr.log'),'images':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in folder.glob('*.png')]}
        dump(folder/'verified.json',row);print('NATIVE_CASE_PASS',name,flush=True)
    finally:s.cleanup()

def main():
    base=WORK/'c2-native';base.mkdir(exist_ok=True);screen=base/'screensaver';screen.mkdir(exist_ok=True)
    source=ROOT/'C/C2/screensaver'
    for name in ('screensaver.c','screensaver_core.h','Makefile'):shutil.copyfile(source/name,screen/name)
    tests=base/'am-tests'
    if not tests.exists():shutil.copytree(BENCH/'am-kernels/tests/am-tests',tests,ignore=shutil.ignore_patterns('build'))
    for mutant in (False,True):
        exe=base/('core-bad' if mutant else 'core-good')
        run('C2/screensaver/'+('bad' if mutant else 'good')+'-build',['gcc','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-fno-pie','-no-pie',*(['-DSCREEN_BAD_BLEND'] if mutant else []),source/'core_test.c','-o',exe],inputs=[source/'core_test.c',source/'screensaver_core.h'],outputs=[exe])
        o,e,_=run('C2/screensaver/'+('bad' if mutant else 'good')+'-run',[exe],inputs=[exe],expected=(1,) if mutant else (0,))
        assert 'SCREEN_ASSERT' in e if mutant else 'SCREEN_CORE_PASS transitions=7744' in o
    for name,cwd in [('screen',screen),('am-tests',tests)]:
        run('C2/native/'+name+'-build',['make','-j1','ARCH=native'],cwd=cwd,inputs=[cwd/'Makefile',*sorted(cwd.glob('*.c'))],outputs=[cwd/'build'/('screensaver-native.elf' if name=='screen' else 'amtest-native.elf')],timeout=240)
    rows=[]
    for name in ('solid','gradient','timer','keyboard','video'):
        run('C2/native/'+name+'/launch',['xvfb-run','-a','-s','-screen 0 1024x768x24','python3',Path(__file__),'--child',name],inputs=[Path(__file__),ROOT/'C/runtime/x11_harness.py'],env={'C_PRIVATE_XVFB':'1'},timeout=35)
        rows.append(json.loads((ROOT/'artifacts/C2/native'/name/'session/verified.json').read_text()))
    dump(ROOT/'reports/C2_native_io.json',{'status':'PASS_BOUNDED_GUI_AND_CONTROLS','screensaver_core_cases':7744,'wrong_blend_rejected':True,'runs':rows,'scope':'Unchanged official native t/k/v; authored 400x300 screensaver real SDL display, keyboard acceleration/release and Escape termination. Isolated Xvfb; no claim of physical monitor protection or every keyboard layout.'})
    print('C2_NATIVE_IO_PASS',flush=True)

if __name__=='__main__':child() if '--child' in sys.argv else main()

from pathlib import Path
import sys,re,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
from x11_harness import NativeSession
from run_programs import compile_app,binaries,APPS,D,N

def prepare(name):
    extra=[];arg=''
    if name=='initial-canvas':
        cwd=APPS/'initial-canvas';cwd.mkdir(exist_ok=True)
        shutil.copyfile(D/'initial_canvas.c',cwd/'main.c')
        (cwd/'Makefile').write_text('NAME = initial-canvas\nSRCS = main.c\nINC_PATH += $(AM_HOME)/am/src\nLDFLAGS += --wrap=__am_gpu_init\ninclude $(AM_HOME)/Makefile\n')
    elif name in ('timer','keyboard','video'):
        cwd=APPS/'am-kernels/tests/am-tests';arg={'timer':'t','keyboard':'k','video':'v'}[name]
    elif name=='fceux':
        cwd=APPS/'fceux-am';arg='interaction';rom=ROOT/'C/C2/homebrew/interaction.nes';shutil.copyfile(rom,cwd/'nes/rom/interaction.nes')
        target=cwd/'nes/gen/interaction.c';target.parent.mkdir(exist_ok=True);target.write_bytes(b'const\n'+subprocess.check_output(['xxd','-i','rom/interaction.nes'],cwd=cwd/'nes'))
        config=cwd/'src/config.h';config.write_text(config.read_text().replace('//#define HAS_GUI','#define HAS_GUI'))
    else:
        cwd=APPS/'am-kernels/kernels'/name
        if name=='demo':arg='1'
        if name=='litenes':
            rom=ROOT/'C/C2/homebrew/interaction.nes';data=rom.read_bytes();replacement=cwd/'c2-cc0-rom.c'
            replacement.write_text('/* Project CC0 test ROM; original mario-rom.c retained but not linked. */\nchar rom_mario_nes[] = {\n'+','.join(str(x) for x in data)+'\n};\n')
            make=cwd/'Makefile.cc0';make.write_text('NAME = litenes\nSRCS = $(filter-out src/mario-rom.c,$(shell find src -name "*.c")) c2-cc0-rom.c\ninclude $(AM_HOME)/Makefile\n');extra=['-f',make]
        if name=='bad-apple':
            media=json.loads((ROOT/'reports/C2_nemu_media.json').read_text());ff=Path(media['executable']);assert sha(ff)==media['sha256']
            build=cwd/'build';build.mkdir(exist_ok=True);source=cwd/'bad-apple.mp4'
            commands=[('video',['-f','image2pipe','-s','80x25','-vcodec','rawvideo','-pix_fmt','monow'],build/'video.frame'),('audio',['-vn','-acodec','pcm_s16le','-f','s16le','-ac','1','-ar','44100'],build/'audio.pcm')]
            for mode,options,out in commands:
                run('C2/pa2/media/'+mode,[ff,'-y','-threads','1','-filter_threads','1','-filter_complex_threads','1','-i',source,*options,'-threads','1',out],cwd=cwd,env=media['environment'],inputs=[ff,source],outputs=[out],timeout=240,resume=True)
            bad=D/'results/bad-media.bin';bad.parent.mkdir(exist_ok=True);bad.write_text('not a media stream\n')
            o,e,_=run('C2/pa2/media/negative',[ff,'-v','error','-i',bad,'-f','null','-'],env=media['environment'],inputs=[ff,bad],expected=(1,));assert 'Invalid data' in e
    image,elf=compile_app('gui-'+name,cwd,arg,extra)
    return image,elf

def child(name):
    import numpy as np
    from PIL import Image
    manifest=json.loads((D/'results/gui_inputs.json').read_text());job=manifest[name]
    exe=binaries()['feature'];folder=ROOT/'artifacts/C2/pa2/gui'/name/'session';folder.mkdir(parents=True,exist_ok=True);report=folder/'nemu.json'
    args=[exe,'-b','--diff=none','--elf='+job['elf'],'--report='+str(report),job['image']]
    trace=folder/'device.trace'
    s=NativeSession(exe,'',folder,title='riscv32-NEMU',command=args,cwd=N,env_extra={'C_DTRACE_FILE':str(trace),'C_DTRACE_LIMIT':'128'})
    observations={};start=time.monotonic()
    def log():return (folder/'stdout.log').read_text(errors='replace')+(folder/'stderr.log').read_text(errors='replace')
    def pixels(path):return np.array(Image.open(path).convert('RGB'))
    def until(predicate,seconds=60):
        while time.monotonic()-start<seconds:
            assert s.proc.poll() is None,'NEMU exited before observation'
            if predicate():return
            time.sleep(.1)
        raise AssertionError('Observation deadline exceeded; this is not a successful timeout')
    def first_image():
        path=s.capture('first');a=pixels(path)
        return path,a
    try:
        if name=='initial-canvas':
            until(lambda:'INITIAL_CANVAS 400 300' in log(),20)
            values=np.arange(120000,dtype=np.uint32).reshape(300,400)
            expected=np.stack([(values>>16)&255,(values>>8)&255,values&255],axis=2).astype(np.uint8)
            expected=np.repeat(np.repeat(expected,2,axis=0),2,axis=1)
            until(lambda:np.array_equal(pixels(s.capture('initialized')),expected),30)
            observations={'logical_size':[400,300],'all_480000_captured_pixels_match':True,'formula':'framebuffer[i]=i, exact nearest-neighbor SDL x2 scaling'}
        elif name=='timer':
            until(lambda:all(f'{n} second' in log() for n in (1,2,3)),20)
            observations={'seconds':[1,2,3]}
        elif name=='keyboard':
            time.sleep(.3)
            for key in ('j','Left'):
                s.key('keydown',key);time.sleep(.3);s.key('keyup',key);time.sleep(.3)
            until(lambda:len(re.findall(r'Got\s+\(kbd\):',log()))>=4,15)
            events=re.findall(r'Got\s+\(kbd\):\s+(\w+)\s+\((\d+)\)\s+(DOWN|UP)',log())
            for key in ('J','LEFT'):
                for state in ('DOWN','UP'):assert (key,state) in [(a,c) for a,b,c in events]
            observations={'events':events}
        elif name=='bad-apple':
            until(lambda:log().count('\x1b[0;0H')>=4,45)
            frames=log().split('\x1b[0;0H')[1:]
            complete=[]
            for frame in frames[:-1]:
                lines=[s for s in frame.splitlines() if len(s)==80 and set(s)<=set('X.')]
                if len(lines)>=25:complete.append(lines[:25])
            assert len(complete)>=2
            observations={'complete_ascii_frames':len(complete),'frame_dimensions':[80,25],'audio_present':False,'scope':'Visual/character playback in NEMU; NEMU audio is optional and not enabled.'}
        else:
            path=folder/'probe.png'
            def nonblack():
                s.capture('probe');a=pixels(path);return int(np.count_nonzero(np.any(a!=0,axis=2)))>200
            until(nonblack,60);first,a=first_image()
            if name in ('fceux','litenes'):
                def color_state(label,blue):
                    sample=pixels(s.capture(label)).astype(np.int16);r,g,b=sample[:,:,0],sample[:,:,1],sample[:,:,2]
                    nblue=int(np.count_nonzero((b>2*r)&(b>g)&(b>60)));nred=int(np.count_nonzero((r>2*b)&(r>g)&(r>60)))
                    return (nblue>10000 and nred<nblue//5) if blue else (nred>10000 and nblue<nred//5)
                until(lambda:color_state('first',True),60);a=pixels(folder/'first.png')
                s.key('keydown','j')
                until(lambda:color_state('pressed',False),60);b=pixels(folder/'pressed.png')
                s.key('keyup','j')
                until(lambda:color_state('released',True),75);c=pixels(folder/'released.png')
                observations={'changed_on_J':int(np.count_nonzero(np.any(a!=b,axis=2))),'changed_after_release':int(np.count_nonzero(np.any(b!=c,axis=2))),'ROM_sha256':sha(ROOT/'C/C2/homebrew/interaction.nes')}
                assert observations['changed_after_release']>5000
            else:
                if name=='slider':time.sleep(5.5)
                else:time.sleep(.6)
                if name=='typing-game':s.key('key','a');time.sleep(.5)
                if name=='snake':s.key('key','Right');time.sleep(.3)
                # Guest rendering speed is measured by completed output, not a
                # fixed host delay. Keep the same pixel-change assertion.
                until(lambda:np.count_nonzero(np.any(pixels(s.capture('second'))!=a,axis=2))>20,60)
                second=folder/'second.png';b=pixels(second)
                changed=int(np.count_nonzero(np.any(a!=b,axis=2)))
                assert changed>20,(name,changed)
                observations={'changed_pixels':changed,'distinct_colors':len(np.unique(b.reshape(-1,3),axis=0))}
        session=s.finish();simulation=json.loads(report.read_text());assert simulation['result']=='QUIT' and not simulation['diff_enabled']
        dt=trace.read_text();assert 'map=' in dt and len(dt.splitlines())<=129
        row={'status':'PASS_BOUNDED_OBSERVATION','name':name,'observations':observations,'simulation':simulation,'session':session,'executable_sha256':sha(exe),'image_sha256':sha(job['image']),'elf_sha256':sha(job['elf']),'device_trace_sha256':sha(trace),'images':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in folder.glob('*.png')],'scope':'Actual NEMU device integration and guest program, terminated by SDL close after semantic observations. Independent ISA DiffTest is disabled here for GUI speed; command-line correctness suite separately uses Spike.'}
        dump(folder/'verified.json',row);print('C2_NEMU_GUI_PASS',name,flush=True)
    finally:s.cleanup()

def main(names):
    resultfile=ROOT/'reports/C2_nemu_gui.json';prior=json.loads(resultfile.read_text()).get('runs',[]) if resultfile.exists() else [];rows={r['name']:r for r in prior}
    inputs=D/'results/gui_inputs.json';jobs=json.loads(inputs.read_text()) if inputs.exists() else {}
    for name in names:
        image,elf=prepare(name);jobs[name]={'image':str(image),'elf':str(elf)};dump(inputs,jobs)
        run('C2/pa2/gui/'+name+'/launch',['xvfb-run','-a','-s','-screen 0 1024x768x24','python3',Path(__file__),'--child',name],inputs=[Path(__file__),ROOT/'C/runtime/x11_harness.py',binaries()['feature'],image,elf],env={'C_PRIVATE_XVFB':'1'},timeout=90)
        rows[name]=json.loads((ROOT/'artifacts/C2/pa2/gui'/name/'session/verified.json').read_text());dump(resultfile,{'status':'IN_PROGRESS','runs':list(rows.values())})
    required={'initial-canvas','timer','keyboard','video','slider','typing-game','demo','bad-apple','snake','litenes','fceux'}
    dump(resultfile,{'status':'PASS_BOUNDED_GUI' if required<=set(rows) else 'IN_PROGRESS','runs':list(rows.values()),'required':sorted(required),'scope':'Eleven real NEMU sessions including exact full-screen initialization; demonstration suite includes seven required application families, with one selected demo (Langton ant). CC0 ROM substituted via separate build manifests, original commercial-ROM source retained. No physical audio claim.'})

if __name__=='__main__':
    if '--child' in sys.argv:child(sys.argv[sys.argv.index('--child')+1])
    else:
        p=argparse.ArgumentParser();p.add_argument('names',nargs='*');a=p.parse_args();main(a.names or ['timer','keyboard','video','slider','typing-game','demo','bad-apple','snake','litenes','fceux'])

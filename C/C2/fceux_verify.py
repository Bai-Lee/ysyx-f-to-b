# C replay derived from the accepted D FCEUX harness; actual source and byte hashes retained.
from pathlib import Path
import sys,signal,wave,struct,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def gui():
 import numpy as np
 from PIL import Image
 d=ROOT/'artifacts/C2/fceux/native_session';d.mkdir(parents=True,exist_ok=True)
 if (d/'run.json').exists():
  history=d/'attempts'/str(time.time_ns());history.mkdir(parents=True)
  for file in list(d.iterdir()):
   if file.is_file():shutil.copyfile(file,history/file.name)
 exe=WORK/'c2-npc-apps/fceux-am/build/fceux-native.elf';pcm=WORK/'fceux_native_audio.raw'
 if pcm.exists():pcm.rename(WORK/('fceux_native_audio-'+str(time.time_ns())+'.raw'))
 env=os.environ.copy();env.update(SDL_AUDIODRIVER='disk',SDL_DISKAUDIOFILE=str(pcm),SDL_DISKAUDIODELAY='20',SDL_RENDER_DRIVER='software',SHELL='/bin/bash',mainargs='interaction')
 commands=[]
 def cmd(args):
  q=subprocess.run(args,env=env,capture_output=True,text=True,timeout=15);commands.append({'command':args,'exit':q.returncode,'stdout':q.stdout,'stderr':q.stderr});assert q.returncode==0,q.stderr;return q.stdout
 started=time.monotonic();out=(d/'stdout.log').open('wb');err=(d/'stderr.log').open('wb');proc=subprocess.Popen([str(exe)],env=env,cwd=WORK,stdout=out,stderr=err,start_new_session=True)
 times={}
 try:
  window=None
  for i in range(100):
   q=subprocess.run(['xdotool','search','--onlyvisible','--name','Native Application'],env=env,capture_output=True,text=True)
   if q.returncode==0:window=q.stdout.splitlines()[-1];break
   assert proc.poll() is None;time.sleep(.1)
  assert window;cmd(['xdotool','windowfocus','--sync',window])
  time.sleep(2);cmd(['scrot','-o',str(d/'released.png')]);times['released_bytes']=pcm.stat().st_size
  cmd(['xdotool','keydown','j']);time.sleep(2);cmd(['scrot','-o',str(d/'pressed.png')]);times['pressed_bytes']=pcm.stat().st_size
  cmd(['xdotool','keyup','j']);time.sleep(2);cmd(['scrot','-o',str(d/'released_again.png')]);times['released_again_bytes']=pcm.stat().st_size
  cmd(['xdotool','key','q']);rc=proc.wait(timeout=10);assert rc==0
 finally:
  if proc.poll() is None:os.killpg(proc.pid,signal.SIGTERM);proc.wait(timeout=5)
  out.close();err.close()
 a=np.array(Image.open(d/'released.png').convert('RGB'));b=np.array(Image.open(d/'pressed.png').convert('RGB'));c=np.array(Image.open(d/'released_again.png').convert('RGB'))
 changed=int(np.any(a!=b,axis=2).sum());recovered=int(np.any(a!=c,axis=2).sum());assert changed>10000 and recovered<changed*.05,(changed,recovered)
 samples=np.frombuffer(pcm.read_bytes(),dtype='<i2');assert len(samples)>44100 and np.max(np.abs(samples.astype(np.int32)))>100
 # Analyze steady pieces of the actual SDL callback output, not a synthesized reference waveform.
 pitch=[]
 for end in [times['released_bytes']//2,times['pressed_bytes']//2,times['released_again_bytes']//2]:
  clip=samples[max(0,end-22050):end].astype(float);clip-=clip.mean();spec=np.abs(np.fft.rfft(clip*np.hanning(len(clip))));frequencies=np.fft.rfftfreq(len(clip),1/44100);spec[(frequencies<100)|(frequencies>2000)]=0;pitch.append(float(frequencies[int(spec.argmax())]))
 assert abs(pitch[0]-440)<15 and abs(pitch[1]-220)<15 and abs(pitch[2]-440)<15,pitch
 wav=d/'captured_audio.wav'
 with wave.open(str(wav),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(44100);f.writeframes(pcm.read_bytes())
 row={'status':'PASS','command':[str(exe)],'binary_sha256':sha(exe),'rom_sha256':sha(ROOT/'C/C2/homebrew/interaction.nes'),'elapsed_seconds':time.monotonic()-started,'exit_code':rc,'display':os.environ.get('DISPLAY'),'commands':commands,'changed_pixels_on_J':changed,'pixels_not_recovered':recovered,'pitch_hz':pitch,'audio_sha256':sha(wav),'stdout_sha256':sha(d/'stdout.log'),'stderr_sha256':sha(d/'stderr.log'),'scope':'Real upstream FCEUX on native AM/SDL under isolated Xvfb; X11 keyboard input, actual rendered framebuffer and SDL audio callback PCM verified. No physical loudspeaker verification or commercial-game ROM.'}
 dump(d/'run.json',row);dump(ROOT/'reports/C2_fceux_native.json',row)
 print('FCEUX_NATIVE_VIDEO_KEY_AUDIO_PASS',flush=True)

def main():
 rom=ROOT/'C/C2/homebrew/interaction.nes';fceux=WORK/'c2-npc-apps/fceux-am';shutil.copyfile(rom,fceux/'nes/rom/interaction.nes')
 # Upstream build-roms.py only generates absent files and otherwise ignores ROM changes.
 generated=fceux/'nes/gen/interaction.c';generated.parent.mkdir(exist_ok=True)
 generated.write_bytes(b'const\n'+subprocess.check_output(['xxd','-i','rom/interaction.nes'],cwd=fceux/'nes'))
 config=fceux/'src/config.h';source=config.read_text();config.write_text(source.replace('//#define HAS_GUI','#define HAS_GUI'))
 run('C2/fceux/native_build',['make','-j1','ARCH=native','mainargs=interaction'],cwd=fceux,inputs=[config,rom],outputs=[fceux/'build/fceux-native.elf'],timeout=600)
 run('C2/fceux/native_gui',['xvfb-run','-a','-s','-screen 0 1024x768x24','python3',Path(__file__),'--gui'],inputs=[rom,fceux/'build/fceux-native.elf',Path(__file__)],timeout=60)
 config.write_text(config.read_text().replace('#define HAS_GUI','//#define HAS_GUI'))
 o,e,r=run('C2/fceux/npc_ascii',['make','-j1','ARCH=riscv32e-npc','run','mainargs=interaction',"NPC_ARGS=--wall-timer --uart-random --until-output '\033[0;0H' --until-count 3"],cwd=fceux,inputs=[config,rom,BENCH/'npc/build/sim',WORK/'nemu-ref/build/riscv32-nemu-interpreter-so'],outputs=[fceux/'build/fceux-riscv32e-npc.bin',fceux/'build/fceux-riscv32e-npc.elf',fceux/'build/fceux-riscv32e-npc.bin.npc.json'],timeout=1800)
 assert o.count('\x1b[0;0H')>=3
 lines=[x for x in o.splitlines() if len(x)==128 and set(x)<=set('o. *O0@#')];assert len(lines)>=112 and any(len(set(x))>1 for x in lines)
 result=json.loads((fceux/'build/fceux-riscv32e-npc.bin.npc.json').read_text());assert result['result']=='BOUNDED_OUTPUT_OBSERVATION'
 dump(ROOT/'reports/C2_fceux_ascii.json',{'status':'PASS_BOUNDED_OBSERVATION','simulation':result,'completed_frame_rows':len(lines),'rom_sha256':sha(rom),'scope':'Two complete 128-column character frames observed, stopped at third frame header; no claim of indefinite gameplay.'})
if __name__=='__main__':gui() if '--gui' in sys.argv else main()

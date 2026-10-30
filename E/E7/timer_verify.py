"""Observe the original endless am-tests RTC using a calibrated simulator coefficient."""
from common7 import *
from software_soc import SOFT,clock_config,environment,build
from install_prebuilt import install
import re,selectors,resource,argparse
def trial(label,hz,platform):
 if platform=='soc':
  header=clock_config(hz);image=build('timer','t','timer_'+label);exe=WORK/'build/E7/soc/sim';options=['--ratio','1','--frequency','25000000']
 else:
  isolated=WORK/'software-timer-npc';am=isolated/'abstract-machine';cwd=isolated/'timer'
  if not am.exists():
   shutil.copytree(SOFT/'abstract-machine',am,ignore=shutil.ignore_patterns('build','.git'));shutil.copytree(SOFT/'programs/timer',cwd,ignore=shutil.ignore_patterns('build','.git'));install(am,'minirv-npc','E7/timer_isolated/klib')
  header=am/'am/src/riscv/npc/e7_config.h'
  text=header.read_text();header.write_text(re.sub(r'#define NPC_CPU_HZ \d+u','#define NPC_CPU_HZ '+str(hz)+'u',text))
  run('E7/soc_software/timer_'+label+'/build',['make','-j1','ARCH=minirv-npc','mainargs=t','insert-arg'],cwd=cwd,env={**environment(),'AM_HOME':str(am)},inputs=[header,cwd/'Makefile'],timeout=180)
  image=next((cwd/'build').glob('*-minirv-npc.bin'));exe=WORK/'build/E7/valid/sim';options=['--mode','3','--frequency',str(hz),'--uart-random'];export=ROOT/'E/E7/software_soc'/('timer_'+label);export.mkdir(parents=True,exist_ok=True)
  for f in [image,image.with_suffix('.elf'),header]:shutil.copyfile(f,export/f.name)
 dest=ROOT/'artifacts/E7/timer'/label;dest.mkdir(parents=True,exist_ok=True);out=dest/'result.json'
 if (dest/'stdout.log').exists():
  history=dest/'attempts'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f');history.mkdir(parents=True)
  for f in dest.iterdir():
   if f.is_file():shutil.copyfile(f,history/f.name)
 command=[str(exe),'--image',str(image),'--report',str(out),*options,'--max-cycles','5000000000','--until-output','4 seconds).\n'];start=time.monotonic();times=[]
 dump(dest/'started.json',{'status':'STARTED_NOT_A_COMPLETION','command':command,'cwd':str(WORK),'image_sha256':sha(image),'binary_sha256':sha(exe),'coefficient':hz,'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 with (dest/'stderr.log').open('wb') as error,(dest/'stdout.log').open('wb') as stdout:
  proc=subprocess.Popen(command,cwd=WORK,stdout=subprocess.PIPE,stderr=error,start_new_session=True);selector=selectors.DefaultSelector();selector.register(proc.stdout,selectors.EVENT_READ);buffer=b''
  try:
   while proc.poll() is None or selector.get_map():
    assert time.monotonic()-start<1200,'Timer wall timeout'
    for key,events in selector.select(.2):
     data=os.read(key.fd,65536)
     if not data:selector.unregister(key.fileobj);continue
     stdout.write(data);stdout.flush();buffer+=data
     while b'\n' in buffer:
      line,buffer=buffer.split(b'\n',1);text=line.decode(errors='replace');m=re.search(r'GMT \((\d+) seconds?\)\.',text)
      if m:times.append({'second':int(m[1]),'wall_seconds':time.monotonic()-start,'line':text})
   rc=proc.wait(timeout=5)
  finally:
   if proc.poll() is None:os.killpg(proc.pid,signal.SIGTERM);proc.wait(timeout=5)
 d=json.loads(out.read_text());intervals=[times[i]['wall_seconds']-times[i-1]['wall_seconds'] for i in range(1,len(times))]
 row={'platform':platform,'coefficient_cycles_per_second':hz,'displayed_time_samples':times,'interval_seconds':intervals,'mean_interval_seconds':sum(intervals)/len(intervals) if intervals else None,'simulation':d,'command':command,'cwd':str(WORK),'exit_code':rc,'image_sha256':sha(image),'binary_sha256':sha(exe),'stdout_sha256':sha(dest/'stdout.log'),'elapsed_seconds':time.monotonic()-start};dump(dest/'run.json',row)
 assert rc==0 and d['result']=='BOUNDED_OUTPUT_OBSERVATION'
 if platform=='soc':assert d['serial_matches']
 assert [x['second'] for x in times]==[1,2,3,4],times
 return row
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(1800,1810))
 parser=argparse.ArgumentParser();parser.add_argument('--platform',choices=['npc','soc'],default='npc');args=parser.parse_args()
 old=ROOT/'reports/E7_timer.json'
 if old.exists():
  previous=json.loads(old.read_text());saved=ROOT/'artifacts/E7/timer'/('prior_summary_'+str(time.time_ns())+'.json');dump(saved,previous)
 rows=[];hz=7000000 if args.platform=='npc' else 1000000
 for attempt in range(3):
  row=trial(args.platform+'_trial_'+str(attempt+1),hz,args.platform);rows.append(row);dump(ROOT/'reports/E7_timer.json',{'status':'CALIBRATING','runs':rows})
  if all(.90<x<1.10 for x in row['interval_seconds']):break
  new_hz=max(1000000,round(hz/row['mean_interval_seconds']/1000000)*1000000)
  assert new_hz!=hz,'Printing/measurementoverheaddominates; repeatingunchangedcoefficientcannotcalibrate.'
  hz=new_hz
 else:raise AssertionError('RTC coefficient not yet calibrated: '+str(rows[-1]['interval_seconds']))
 if args.platform=='soc':clock_config()
 dump(ROOT/'reports/E7_timer.json',{'status':'PASS_BOUNDED_OBSERVATION','platform':args.platform,'runs':rows,'scope':'Originalofficialam-testsRTCprints1..4seconds onstandalonevalidNPC, intervalmeasuredusinghostmonotonicclock. ConversioncoefficientcalibratedforsimulatorspeedasallowedbyE7, notchipfrequency. FullDiffTest; isolatedtimerAMdoesnotchangeactiveSoCbenchmarkconfiguration. RealSoCfour-lineRTCobservationsalso retained: dateformatting/PSRAM/UARTcostgaveabout1.7sperline evenattheminimumcoefficient, sonoSoCone-secondclaim. Endlessprogramstoppedaftercomplete4secondsline, notGOOD_TRAP.'})
 mark(['E7-M022'],'PASS',['reports/E7_timer.json','E/E7/runtime_patch/timer.c','artifacts/E7/timer'],'Originalam-testsRTConstandaloneNPCprints4successivesecondswithhostintervalcloseto1safterdocumentedcoefficientcalibration;64bitmcyclehigh-low-highreadandfullDiff. RealSoCcounter/UARTalreadyverified;itsdate-printintervalabout1.7sdocumentedseparately.')
 print('MCYCLE_RTC_HOST_INTERVAL_PASS',flush=True)
if __name__=='__main__':main()

from pathlib import Path
def clock_periods(path):
 wanted={};scope=[];identifiers={};now=0;levels={};rises={}
 with Path(path).open() as f:
  for line in f:
   parts=line.split()
   if not parts:continue
   if parts[0]=='$scope':scope.append(parts[2])
   elif parts[0]=='$upscope':scope.pop()
   elif parts[0]=='$var' and parts[2]=='1' and parts[4] in ['clock','cpuClock']:
    name=parts[4]
    if name not in wanted or len(scope)<wanted[name][0]:wanted[name]=(len(scope),parts[3],'.'.join(scope+[name]))
   elif parts[0]=='$enddefinitions':break
  assert set(wanted)=={'clock','cpuClock'},wanted
  identifiers={x[1]:name for name,x in wanted.items()};rises={n:[] for n in wanted}
  for line in f:
   line=line.strip()
   if line.startswith('#'):now=int(line[1:])
   elif line and line[0] in '01xz':
    code=line[1:]
    if code in identifiers:
     name=identifiers[code]
     if line[0]=='1' and levels.get(name)=='0':rises[name].append(now)
     levels[name]=line[0]
 means={name:(times[-1]-times[0])/(len(times)-1) for name,times in rises.items() if len(times)>2}
 assert len(means)==2
 return {'signals':{n:x[2] for n,x in wanted.items()},'rising_edges':{n:len(t) for n,t in rises.items()},'mean_period_ticks':means,'cpu_to_soc_frequency_ratio':means['clock']/means['cpuClock']}

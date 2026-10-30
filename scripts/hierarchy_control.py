from logisim_circuits import *
from evidence import *
def main():
    p=Project('hier4');c=p.circuit('buffer4');a=c.io('A',4);b=c.split(a);c.io('Y',4,True,c.join(b))
    t=p.circuit('hier4');a=t.io('A',4);outs=t.sub('buffer4',{'A':a});t.io('Y',4,True,outs['Y'])
    path=ROOT/'F/circuits/hierarchy_control.circ';p.write(path)
    vec=ROOT/'F/vectors/hierarchy_control.txt';vec.write_text('A Y\n'+''.join(f'{n} {n}\n' for n in range(16)),encoding='utf8')
    cfg=json.loads((ROOT/'config/toolchain.json').read_text('utf8'));j=cfg['java']['executable'];cp=str(ROOT/'temp/java-classes')+';'+cfg['logisim']['jar'];prefix=[j,'-Xmx512m','-Djava.awt.headless=true','-Duser.language=en','-Dfile.encoding=UTF-8','-Djava.util.prefs.PreferencesFactory=LocalPrefsFactory','-cp',cp,'CircuitRunner']
    result=run('preflight/splitter_hierarchy',prefix+[path,'buffer4',vec,'hier4',vec],[path,vec],timeout=30)
    return 0 if result['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())

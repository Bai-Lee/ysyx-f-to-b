from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
scons=Path('/home/USER/tools/scons-4.0.1/bin/scons');work=WORK/'c5/scons-controls';rows=[]
for name in ['good','missing-source']:
    folder=work/name;folder.mkdir(parents=True,exist_ok=True)
    (folder/'SConstruct').write_text("Program('control', ['"+('main.c' if name=='good' else 'absent.c')+"'])\n")
    (folder/'main.c').write_text('int main(void){return 0;}\n')
    tag='C5/rtthread/scons-controls/'+name
    out,err,record=run(tag,[scons,'-Q','-j1'],cwd=folder,inputs=[scons,folder/'SConstruct',folder/'main.c'],outputs=[folder/'control'] if name=='good' else [],expected=(0 if name=='good' else 2,),timeout=30)
    if name=='good':run(tag+'-execute',[folder/'control'],inputs=[folder/'control'])
    else:assert 'absent.c' in err and ('not found' in err or 'do not know' in err)
    rows.append({'name':name,'status':'PASS','exit_code':record['exit_code'],'evidence':'artifacts/'+tag})
dump(ROOT/'reports/C5_scons_controls.json',{'status':'PASS','runs':rows,'scope':'Actual SCons dependency/build/execute positive andmissing-source failure; privateportable4.0.1package, no systemPython changes.'})
print('C5_SCONS_CONTROLS_PASS',flush=True)

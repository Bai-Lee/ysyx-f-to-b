from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime'))
from common import *
base=ROOT/'C/C5';am=WORK/'c5/workbench/abstract-machine';out=WORK/'c5/gpu-driver-unit';out.mkdir(parents=True,exist_ok=True);rows=[]
for name in ['good','bad-row-stride']:
    folder=out/name;folder.mkdir(exist_ok=True);text=(base/'am/ioe.c').read_text()
    if name!='good':assert text.count('destination+=640')==1;text=text.replace('destination+=640','destination+=639')
    (folder/'ioe.c').write_text(text);shutil.copyfile(base/'am/ps2.h',folder/'ps2.h');exe=folder/'test';tag='C5/gpu-driver/'+name
    inputs=[base/'rtl_tests/gpu_driver_test.c',folder/'ioe.c',folder/'ps2.h',am/'am/include/am.h',am/'am/include/amdev.h']
    run(tag+'/build',['gcc','-std=c11','-O2','-Wall','-Wextra','-DARCH_H="arch/riscv.h"','-I'+str(folder),'-I'+str(am/'am/include'),'-I'+str(am/'klib/include'),base/'rtl_tests/gpu_driver_test.c','-o',exe],inputs=inputs,outputs=[exe],timeout=60)
    run(tag+'/run',[exe],inputs=[exe],expected=(0 if name=='good' else 1,),timeout=10)
    rows.append({'name':name,'status':'PASS','expected_exit':0 if name=='good' else 1,'evidence':'artifacts/'+tag})
dump(ROOT/'reports/C5_gpu_driver.json',{'status':'PASS_NATIVE_LOGIC_AND_NEGATIVE','runs':rows,'scope':'ExactC5ioe.c compiled with the real AM headers and test framebuffer address.13rectangles independently scored per sourcepixel, clipping onall4sides, zero/sync-only, INT_MIN outsidecoordinates, originalsourcepitch and8wordguards. Wrongdestinationrowstride rejected. Does not replace actualCPU/NVBoard acceptance.'})
print('C5_GPU_DRIVER_PASS',flush=True)

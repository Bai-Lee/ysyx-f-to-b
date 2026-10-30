from pathlib import Path
import sys,resource
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(20,25))
 root=Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite/bin');wd=WORK/'build/E8/profile/14';p=ROOT/'E/E8';plugin=wd/'vpi_memory.vpi';rows=[]
 src=[ROOT/'E/E5/rtl/minirv_decode.sv',ROOT/'E/E5/rtl/minirv_regfile.sv',ROOT/'E/E7/rtl/minirv_bus.sv',ROOT/'E/E7/rtl/ysyx_00000000.sv',p/'gate_system.sv',p/'iverilog_top.sv']
 for case,fault in [('positive',False),('unreset',True)]:
  vvp=wd/('control_'+case+'.vvp');out=ROOT/'artifacts/E8/icarus14_controls'/case/'result.json'
  run('E8/icarus14_controls/'+case+'/compile',[root/'iverilog','-g2012','-DSYNTHESIS',*(['-DFAULT_RESET_STATE'] if fault else []),'-s','iverilog_top','-o',vvp,*src],inputs=src)
  o,e,r=run('E8/icarus14_controls/'+case+'/run',[root/'vvp','-M'+str(wd),'-mvpi_memory',vvp,'+image='+str(p/'examples/correct.bin'),'+report='+str(out),'+max_cycles=1000'],inputs=[vvp,plugin,p/'examples/correct.bin'],outputs=[out],expected=(1,) if fault else (0,));d=json.loads(out.read_text());assert d['exit_code']==(1 if fault else 0)
  if fault:assert 'UNKNOWN_BUS_CONTROL' in o
  rows.append({'case':case,'result':d,'exit_code':r['exit_code']})
 vvp=wd/'x_argument.vvp';source=p/'examples/x_argument.v'
 run('E8/icarus14_controls/x_argument/compile',[root/'iverilog','-g2012','-s','x_argument','-o',vvp,source],inputs=[source])
 o,e,r=run('E8/icarus14_controls/x_argument/run',[root/'vvp','-M'+str(wd),'-mvpi_memory',vvp,'+image='+str(p/'examples/correct.bin')],inputs=[vvp,plugin,p/'examples/correct.bin']);assert 'EXPECTED_X_ARGUMENT_REJECTION' in o and 'X/Z memory argument' in o
 dump(ROOT/'reports/E8_icarus14_controls.json',{'status':'PASS','cases':rows,'unknown_argument':'PASS_EXPECTED_REJECTION','tools':[{'path':str(x),'sha256':sha(x)} for x in [root/'iverilog',root/'vvp',plugin]],'scope':'Version14recheckedwithpositiveactualRTL,missingresetnegative,andX/ZVPIargumentrejection. FinalmappedrunusesunchangedoriginalUDPmodels.'})
 print('ICARUS14_X_NEGATIVE_CONTROLS_PASS',flush=True)
if __name__=='__main__':main()

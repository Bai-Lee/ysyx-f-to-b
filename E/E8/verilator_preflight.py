from pathlib import Path
import sys,resource
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
 p=ROOT/'E/E8';rt=ROOT/'E/runtime';sources=[ROOT/'E/E5/rtl/minirv_decode.sv',ROOT/'E/E5/rtl/minirv_regfile.sv',ROOT/'E/E7/rtl/minirv_bus.sv',ROOT/'E/E7/rtl/ysyx_00000000.sv',p/'gate_system.sv'];rows=[]
 for fault in [False,True]:
  name='unreset_2state' if fault else 'correct_2state'
  exe=build('E8/'+name,'gate_system',sources,[p/'gate_runner.cpp'],flags=['-DSYNTHESIS',*(['-DFAULT_RESET_STATE'] if fault else []),'--timescale','1ns/1ns','-MAKEFLAGS','OPT_FAST=-O3 OPT_SLOW=-O3','-CFLAGS','-O3 -I'+str(p)+' -I'+str(rt)],additional_inputs=[p/'memory_model.hpp',rt/'memory.hpp'])
  image=p/'examples/correct.bin';result=ROOT/'artifacts/E8'/name/'result.json'
  o,e,r=run('E8/'+name+'/run',[exe,'--image',image,'--report',result,'--max-cycles','1000'],inputs=[exe,image],outputs=[result]);d=json.loads(result.read_text());assert d['result']=='GOOD_TRAP'
  rows.append({'case':name,'result':d})
 dump(ROOT/'reports/E8_two_state_control.json',{'status':'PASS_CONTROL','cases':rows,'interpretation':'The intentionally unreset FSM happens to start at zero in default two-state Verilator, so it passes here but is rejected by four-state Icarus. The mutant is never selected for production RTL/netlist.'})
 print('E8_TWO_VS_FOUR_STATE_CONTROL_COMPLETE',flush=True)
if __name__=='__main__':main()

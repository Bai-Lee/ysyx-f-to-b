"""Bounded CPU-only four-state regression:512MiB,600CPU seconds per process."""
from pathlib import Path
import sys,resource
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(600,610))
 p=ROOT/'E/E8';rt=ROOT/'E/runtime';work=WORK/'build/E8/vpi';sources=[ROOT/'E/E5/rtl/minirv_decode.sv',ROOT/'E/E5/rtl/minirv_regfile.sv',ROOT/'E/E7/rtl/minirv_bus.sv',ROOT/'E/E7/rtl/ysyx_00000000.sv',p/'gate_system.sv',p/'iverilog_top.sv']
 run('E8/rtl_icarus/vpi_build',['iverilog-vpi','-I'+str(rt),'-I'+str(p),p/'vpi_memory.cpp'],cwd=work,inputs=[p/'vpi_memory.cpp',p/'memory_model.hpp',rt/'memory.hpp'])
 exe=work/'rtl_programs.vvp';run('E8/rtl_icarus/compile',['iverilog','-g2012','-DSYNTHESIS','-s','iverilog_top','-o',exe,*sources],inputs=sources)
 rows=[]
 for item in json.loads((ROOT/'reports/E8_software.json').read_text())['programs']:
  image=Path(item['image']);assert sha(image)==item['sha256'];out=ROOT/'artifacts/E8/rtl_icarus'/item['name']/'result.json'
  o,e,r=run('E8/rtl_icarus/'+item['name'],['vvp','-M'+str(work),'-mvpi_memory',exe,'+image='+str(image),'+report='+str(out),'+max_cycles=50000000'],inputs=[exe,work/'vpi_memory.vpi',image],outputs=[out,Path(str(out)+'.uart.txt')],timeout=900)
  d=json.loads(out.read_text());assert d['result']=='GOOD_TRAP' and d['exit_writes']==1
  assert ('MicroBench PASS' if item['name']=='microbench' else 'Hello, AbstractMachine!') in o
  rows.append({'name':item['name'],'result':d,'elapsed_seconds':r['elapsed_seconds']})
 dump(ROOT/'reports/E8_rtl_icarus.json',{'status':'PASS','programs':rows,'scope':'Actual four-state CPU RTL and VPI memory; official hello and complete microbench test workload with original algorithm checks; no X/Z control or unknown memory arguments permitted.'})
 mark(['E8-M004','E8-M005'],'PASS',['reports/E8_vpi_preflight.json','reports/E8_two_state_control.json','reports/E8_rtl_icarus.json','artifacts/E8/rtl_icarus'],'Official Icarus/VPI example plus negative controls; complete microbench andhello passedfour-stateRTL; missing-reset mutant rejected despite passing defaulttwo-stateVerilator.')
 print('E8_FOUR_STATE_PROGRAMS_PASS',flush=True)
if __name__=='__main__':main()

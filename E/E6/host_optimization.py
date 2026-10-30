from pathlib import Path
import sys,resource
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
 npc=BENCH/'npc';sources=[npc/'vsrc'/n for n in ['minirv_decode.sv','minirv_regfile.sv','minirv_single.sv','npc_sim.sv']]
 exe=build('E6/host_o3','npc_sim',sources,[npc/'csrc/runner.cpp'],extra=[npc/'build/ref.o'],flags=['--timescale','1ns/1ns',"-GRESET_PC=32'h80000000",'-MAKEFLAGS','OPT_FAST=-O3 OPT_SLOW=-O3','-CFLAGS','-O3 -g'],additional_inputs=[npc/'csrc/ref.h',npc/'csrc/memory.hpp'])
 rows=[]
 prior=json.loads((ROOT/'reports/E6_official_tests.json').read_text())
 for suite in prior['suites']:
  cwd=BENCH/'riscv-tests' if suite['suite']=='riscv-tests' else BENCH/'am-kernels/tests/cpu-tests'
  for old in suite['tests']:
   name=old['test'];image=cwd/'build'/(name+'-minirv-npc.bin');result=ROOT/'artifacts/E6/host_o3'/suite['suite']/name/'result.json'
   o,e,r=run('E6/host_o3/'+suite['suite']+'/'+name,[exe,'--image',image,'--base','0x80000000','--mem-mb','128','--devices','--report',result,'--max-cycles','20000000'],inputs=[exe,image],outputs=[result],timeout=20)
   d=json.loads(result.read_text());assert d['result']=='GOOD_TRAP' and d['cycles']==old['simulation']['cycles'] and d['gpr']==old['simulation']['gpr']
   rows.append({'suite':suite['suite'],'test':name,'cycles':d['cycles'],'old_wall_seconds':old['simulation']['wall_seconds'],'optimized_wall_seconds':d['wall_seconds']})
 a=sum(x['old_wall_seconds'] for x in rows);b=sum(x['optimized_wall_seconds'] for x in rows)
 dump(ROOT/'reports/E6_host_optimization.json',{'status':'PASS','simulator':str(exe),'sha256':sha(exe),'speed_ratio_on_73_tests':a/b,'tests':rows,'change':'Same RTL, reference and harness; Verilator-generated Make OPT_FAST/OPT_SLOW explicitly O3. Default -Os previously appeared after -CFLAGS -O3. CPU model behavior/cycles/GPR and full DiffTest unchanged. Separate executable; current train batch not modified.'})
 print('HOST_OPTIMIZATION_VALIDATED_SPEED_RATIO',a/b,flush=True)
if __name__=='__main__':main()

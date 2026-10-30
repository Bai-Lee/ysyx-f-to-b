from pathlib import Path
import sys,gzip,resource
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(60,70))
 p=ROOT/'E/E8';rt=ROOT/'E/runtime';pdk=Path('/home/USER/tools/icsprout55-e-stage');models=[pdk/('IP/STD_cell/ics55_LLSC_H7C_V1p10C100/ics55_LLSC_H7C'+v+'/verilog/ics55_LLSC_H7C'+v+'.v') for v in ['R','L']]
 dest=p/'netlists';dest.mkdir(exist_ok=True);rows=[];work=WORK/'build/E8/vpi'
 for name in ['baseline','area']:
  zipped=ROOT/'E/E7/synthesis'/name/'e7_minirv_Synthesis_sim.v.gz';net=dest/(name+'.v');net.write_bytes(gzip.decompress(zipped.read_bytes()))
  vvp=work/('netlist_'+name+'.vvp')
  run('E8/mapped_'+name+'/icarus_compile',['iverilog','-g2012','-Dfunctional','-s','iverilog_top','-o',vvp,net,*models,p/'gate_system.sv',p/'iverilog_top.sv'],inputs=[net,*models,p/'gate_system.sv',p/'iverilog_top.sv'],timeout=90)
  exe=build('E8/mapped_'+name,'gate_system',[net,*models,p/'gate_system.sv'],[p/'gate_runner.cpp'],flags=['--no-timing','--timescale','1ns/1ns','-Dfunctional','-D__VERILATOR__','-Wno-fatal','-Wno-DECLFILENAME','--output-split','5000','--output-split-cfuncs','500','-MAKEFLAGS','OPT_FAST=-O3 OPT_SLOW=-O3','-CFLAGS','-O3 -I'+str(p)+' -I'+str(rt)],additional_inputs=[p/'memory_model.hpp',rt/'memory.hpp'])
  for engine in ['iverilog','verilator']:
   for case in ['correct','bad_exit']:
    image=p/'examples'/(case+'.bin');out=ROOT/'artifacts/E8'/('mapped_'+name)/(engine+'_'+case)/'result.json'
    cmd=['vvp','-M'+str(work),'-mvpi_memory',vvp,'+image='+str(image),'+report='+str(out),'+max_cycles=1000'] if engine=='iverilog' else [exe,'--image',image,'--report',out,'--max-cycles','1000']
    o,e,r=run('E8/mapped_'+name+'/'+engine+'_'+case,cmd,inputs=[vvp if engine=='iverilog' else exe,image,work/'vpi_memory.vpi'] if engine=='iverilog' else [exe,image],outputs=[out],expected=(0,) if case=='correct' else (1,),timeout=30)
    d=json.loads(out.read_text());assert d['exit_code']==(0 if case=='correct' else 1);rows.append({'variant':name,'engine':engine,'case':case,'result':d})
 dump(ROOT/'reports/E8_mapped_preflight.json',{'status':'PASS_SMALL_NETLIST_CONTROLS','cases':rows,'library_models':[{'path':str(x),'sha256':sha(x)} for x in models],'scope':'Actual baseline andAREA mappedstandardcells tested inbothsimulators; small positive/negativeexit casesonly. Completehello/microbenchmappedtests stillpending.'})
 print('MAPPED_NETLIST_BOTH_SIMULATORS_SMALL_CONTROLS_PASS',flush=True)
if __name__=='__main__':main()

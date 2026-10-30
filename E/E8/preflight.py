from pathlib import Path
import sys,struct,resource
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
 p=ROOT/'E/E8';rt=ROOT/'E/runtime';work=WORK/'build/E8/vpi';work.mkdir(parents=True,exist_ok=True);example=p/'examples';example.mkdir(exist_ok=True)
 c=example/'hello.c';v=example/'hello.v'
 c.write_text('''/* Adapted from archived official Icarus usage/vpi.html worked example. */
#include <vpi_user.h>
static PLI_INT32 hello(PLI_BYTE8 *p){(void)p;vpi_printf("Hello, World!\\n");return 0;}
static void register_hello(void){s_vpi_systf_data t={0};t.type=vpiSysTask;t.tfname="$hello";t.calltf=hello;vpi_register_systf(&t);}
void (*vlog_startup_routines[])(void)={register_hello,0};
''');v.write_text('module main; initial $hello; endmodule\n')
 run('E8/preflight/vpi_example_compile',['iverilog-vpi',c],cwd=work,inputs=[c])
 run('E8/preflight/verilog_example_compile',['iverilog','-g2012','-s','main','-o',work/'hello.vvp',v],inputs=[v])
 o,e,r=run('E8/preflight/vpi_example_run',['vvp','-M'+str(work),'-mhello',work/'hello.vvp'],inputs=[work/'hello.vpi',work/'hello.vvp']);assert o.strip()=='Hello, World!'
 o,e,r=run('E8/preflight/vpi_missing_module',['vvp',work/'hello.vvp'],inputs=[work/'hello.vvp'],expected=(1,255));assert '$hello' in e+o
 run('E8/preflight/memory_vpi_compile',['iverilog-vpi','-I'+str(rt),'-I'+str(p),p/'vpi_memory.cpp'],cwd=work,inputs=[p/'vpi_memory.cpp',p/'memory_model.hpp',rt/'memory.hpp'])
 sources=[ROOT/'E/E5/rtl/minirv_decode.sv',ROOT/'E/E5/rtl/minirv_regfile.sv',ROOT/'E/E7/rtl/minirv_bus.sv',ROOT/'E/E7/rtl/ysyx_00000000.sv',p/'gate_system.sv',p/'iverilog_top.sv'];rows=[]
 for name,value,fault in [('correct',0,False),('bad_exit',1,False),('unreset_state',0,True)]:
  words=[0xf00000b7,((value&4095)<<20)|(2<<7)|0x13,(2<<20)|(1<<15)|(2<<12)|0x23,0x00000513,0x00100073]
  image=example/(name+'.bin');image.write_bytes(struct.pack('<5I',*words));exe=work/(name+'.vvp');out=ROOT/'artifacts/E8/preflight'/name/'result.json'
  run('E8/preflight/'+name+'/compile',['iverilog','-g2012','-DSYNTHESIS',*(['-DFAULT_RESET_STATE'] if fault else []),'-s','iverilog_top','-o',exe,*sources],inputs=sources)
  o,e,r=run('E8/preflight/'+name+'/run',['vvp','-M'+str(work),'-mvpi_memory',exe,'+image='+str(image),'+report='+str(out),'+max_cycles=1000'],inputs=[exe,image,work/'vpi_memory.vpi'],outputs=[out],expected=(0,) if name=='correct' else (1,))
  d=json.loads(out.read_text());assert d['exit_code']==(0 if name=='correct' else 1)
  if fault:assert 'UNKNOWN_BUS_CONTROL' in o
  rows.append({'case':name,'result':d,'stdout':o})
 run('E8/preflight/x_argument/compile',['iverilog','-g2012','-s','x_argument','-o',work/'x_argument.vvp',example/'x_argument.v'],inputs=[example/'x_argument.v'])
 o,e,r=run('E8/preflight/x_argument/run',['vvp','-M'+str(work),'-mvpi_memory',work/'x_argument.vvp','+image='+str(example/'correct.bin')],inputs=[work/'x_argument.vvp',work/'vpi_memory.vpi',example/'correct.bin']);assert 'EXPECTED_X_ARGUMENT_REJECTION' in o and 'X/Z memory argument' in o
 dump(ROOT/'reports/E8_vpi_preflight.json',{'status':'PASS','cases':rows,'scope':'Official VPI hello and missing-plugin negative; real CPU four-state RTL/VPI memory, valid/invalid tohost, unreset FSM X control rejected. Mapped netlist and microbench remain pending.'})
 print('E8_VPI_AND_FOUR_STATE_PREFLIGHT_PASS',flush=True)
if __name__=='__main__':main()

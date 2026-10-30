from common import *
import re

def main():
    d=WORK/'preflight';d.mkdir(parents=True,exist_ok=True)
    suite=Path('/home/USER/tools/e-stage/oss-20261022/oss-cad-suite')
    older=Path('/home/USER/tools/e-stage/oss-20260821/oss-cad-suite')
    chosen={'gcc':Path('/usr/bin/gcc'),'gdb':Path('/usr/bin/gdb'),'riscv_gcc':Path('/usr/bin/riscv64-linux-gnu-gcc'),'verilator':VERILATOR,'iverilog':suite/'bin/iverilog','yosys':older/'bin/yosys','dot':older/'bin/dot'}
    rows=[]
    for key,exe in chosen.items():
        flags=['-V'] if key in ('iverilog','yosys','dot') else ['--version']
        o,e,r=run('D/preflight/version/'+key,[exe,*flags],inputs=[exe],timeout=30)
        rows.append({'name':key,'path':str(exe),'sha256':sha(exe),'version':(o+e).splitlines()[:2]})
    good=d/'good.c';good.write_text('#include <assert.h>\nint main(void){assert(3+4==7);return 0;}\n')
    bad=d/'bad.c';bad.write_text('#include <assert.h>\nint main(void){assert(3+4==8);return 0;}\n')
    for name,p in [('good',good),('bad',bad)]:
        exe=d/name;run('D/preflight/c_'+name+'_build',['gcc','-std=c11','-Wall','-Wextra','-Werror',p,'-o',exe],inputs=[p],outputs=[exe])
        run('D/preflight/c_'+name,[exe],inputs=[exe],expected=(0,) if name=='good' else (-6,))
    rtl=d/'counter.sv';rtl.write_text('module counter(input clock,reset,output reg [3:0] q); always @(posedge clock) if(reset) q<=0; else q<=q+1; endmodule\n')
    tb=d/'tb.sv';tb.write_text('module tb; reg clock=0,reset=1; wire [3:0] q; counter d(clock,reset,q); always #5 clock=~clock; initial begin #11;reset=0;#10;if(q!=1) $fatal(1,"bad counter");$display("COUNTER_PASS");$finish;end endmodule\n')
    out=d/'counter.vvp'
    run('D/preflight/iverilog_build',[suite/'bin/iverilog','-g2012','-s','tb','-o',out,rtl,tb],inputs=[rtl,tb],outputs=[out])
    o,_,_=run('D/preflight/iverilog_run',[suite/'bin/vvp',out],inputs=[out]);assert 'COUNTER_PASS' in o
    fault=d/'fault.sv';fault.write_text(rtl.read_text().replace('q+1','q+2'))
    run('D/preflight/iverilog_fault_build',[suite/'bin/iverilog','-g2012','-s','tb','-o',d/'fault.vvp',fault,tb],inputs=[fault,tb])
    run('D/preflight/iverilog_fault',[suite/'bin/vvp',d/'fault.vvp'],inputs=[d/'fault.vvp'],expected=(1,))
    cpp=d/'counter.cpp';cpp.write_text('#include "Vcounter.h"\n#include <cassert>\nint main(){Vcounter c;c.clock=0;c.reset=1;c.eval();c.clock=1;c.eval();assert(c.q==0);c.clock=0;c.reset=0;c.eval();c.clock=1;c.eval();assert(c.q==1);return 0;}\n')
    obj=d/'obj'
    run('D/preflight/verilator_build',[VERILATOR,'--cc','--exe','--build','-j','1','--top-module','counter','--Mdir',obj,'-o','sim',rtl,cpp],inputs=[rtl,cpp],timeout=180,outputs=[obj/'sim'])
    run('D/preflight/verilator_run',[obj/'sim'],inputs=[obj/'sim'])
    run('D/preflight/yosys',[older/'bin/yosys','-p',f'read_verilog {rtl}; prep -top counter; check -assert; stat; write_json {d}/counter.json'],inputs=[rtl],outputs=[d/'counter.json'])
    run('D/preflight/riscv_compile',['riscv64-linux-gnu-gcc','-march=rv32im','-mabi=ilp32','-ffreestanding','-c','-x','c',good,'-o',d/'rv32.o','-I','/usr/riscv64-linux-gnu/include'],inputs=[good],expected=(0,1))
    # A libc header need not support RV32; use a genuine freestanding control.
    rv=d/'rv.c';rv.write_text('unsigned add(unsigned a,unsigned b){return a+b;}\n')
    run('D/preflight/riscv_freestanding',['riscv64-linux-gnu-gcc','-march=rv32im','-mabi=ilp32','-ffreestanding','-nostdlib','-c',rv,'-o',d/'rv32.o'],inputs=[rv],outputs=[d/'rv32.o'])
    o,_,_=run('D/preflight/riscv_readelf',['riscv64-linux-gnu-readelf','-h',d/'rv32.o'],inputs=[d/'rv32.o']);assert 'ELF32' in o and 'RISC-V' in o
    prior=json.loads((ROOT/'reports/E_toolchain_final.json').read_text());old={x['path']:x for x in prior['binary_fingerprints']}
    for row in rows:row['matches_E_final_lock']=old.get(row['path'],{}).get('sha256')==row['sha256'] if row['path'] in old else None
    dump(ROOT/'reports/D_PREFLIGHT.json',{'status':'PASS_CORE_TOOLS_PENDING_SMALL_DEPENDENCIES','capabilities':['C/C++ and RV32 cross compilation','Verilator RTL simulation','Icarus four-state simulation','Yosys synthesis','Graphviz diagrams','existing locked ECC and ICsprout55 libraries'],'tools':rows,'new_dependencies':['portable Clang 15 for required LLVM IR observations','Capstone 5.0.6 for NEMU/NPC disassembly','Spike reference if PA2 independent DiffTest requires it'],'runtime_root':str(WORK),'resource_policy':{'heavy_jobs':1,'compile_jobs':1,'light_jobs_max':2,'wsl_memory_gib':4,'no_global_configuration_changes':True},'limits':['Only the listed controls have been run in D.','Course source, official admission and actual learner mastery remain separate.','E physical qualification is not a D CPU physical qualification.'],'evidence':'artifacts/D/preflight'})
    print('D_PREFLIGHT_CORE_PASS',flush=True)

if __name__=='__main__':main()

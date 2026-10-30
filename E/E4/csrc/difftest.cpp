#include "Vcpu_top.h"
#include "verilated.h"
#include "semu.h"
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
static bool compare(const Vcpu_top&d,const Semu&r,unsigned oldpc,unsigned ins,unsigned step){
    bool diff=false;
    if(d.pc!=r.pc){fprintf(stderr,"DIFF step=%u pc_before=0x%02x instruction=0x%02x PC dut=0x%02x ref=0x%02x\n",step,oldpc,ins,d.pc,r.pc);diff=true;}
    for(int i=0;i<4;i++){unsigned value=(d.gpr_state>>(8*i))&255;
      if(value!=r.r[i]){fprintf(stderr,"DIFF step=%u pc_before=0x%02x instruction=0x%02x GPR%d dut=0x%02x ref=0x%02x\n",step,oldpc,ins,i,value,r.r[i]);diff=true;}}
    if(d.led!=r.led||d.hex_value!=r.display){fprintf(stderr,"DIFF IO step=%u pc_before=0x%02x led=%u/%u display=%u/%u\n",step,oldpc,d.led,r.led,d.hex_value,r.display);diff=true;}
    return !diff;
}
int main(int argc,char**argv){
    if(argc!=4)return 2;bool random=!strcmp(argv[1],"random");int limit=atoi(argv[2]);if(limit<1||limit>1000000)return 2;
    FILE*trace=fopen(argv[3],"w");if(!trace)return 3;uint8_t memory[256]={0};if(!random&&semu_load(argv[1],memory))return 3;
    VerilatedContext ctx;ctx.commandArgs(argc,argv);Vcpu_top d{&ctx};Semu ref;semu_reset(&ref,1);
    auto tick=[&](){d.clk=0;d.eval();d.clk=1;d.eval();};d.reset=1;tick();d.reset=0;
    uint32_t rng=260704;unsigned covered[256]={0};
    for(int i=0;i<limit;i++){
        rng=rng*1664525u+1013904223u;bool rst=random&&i&&i%1009==0;
        unsigned ins=random?(rng>>24):memory[d.pc],sw=(rng>>8)&255,button=(rng>>16)&255,oldpc=d.pc;
        d.instruction=ins;d.switches=sw;d.buttons=button;d.reset=rst;
        if(rst)semu_reset(&ref,1);else semu_step(&ref,ins,sw,button);
        tick();covered[ins]++;
        if(!compare(d,ref,oldpc,ins,i)){fclose(trace);d.final();return 1;}
        fprintf(trace,"%d,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u,%u\n",i,oldpc,ins,sw,button,rst,d.pc,d.gpr_state&255,(d.gpr_state>>8)&255,(d.gpr_state>>16)&255,d.gpr_state>>24,d.led,d.hex_value);
    }
    if(random){for(unsigned n:covered)if(!n)return 4;}
    printf("PASS DiffTest cycles=%d seed=260704 pc=%u R=%u,%u,%u,%u LED=%u HEX=%u all_opcodes=%d\n",limit,d.pc,ref.r[0],ref.r[1],ref.r[2],ref.r[3],d.led,d.hex_value,random);
    fclose(trace);d.final();return 0;
}

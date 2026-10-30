#include "Vsequential.h"
#include "verilated.h"
#include <cstdio>
#include <cstdlib>
#include <set>
static unsigned long long checks=0;
static void eq(unsigned a,unsigned b,const char*s){++checks;if(a!=b){fprintf(stderr,"FAIL %s actual=%u expected=%u\n",s,a,b);exit(1);}}
int main(int argc,char**argv){
  VerilatedContext ctx;ctx.commandArgs(argc,argv);Vsequential d{&ctx};
  auto tick=[&](){d.clk=0;d.eval();d.clk=1;d.eval();};
  auto reset=[&](){d.reset=1;d.reset_n=0;tick();d.reset=0;d.reset_n=1;};reset();d.enable=1;
  for(unsigned value=0;value<256;value++)for(unsigned mode=0;mode<8;mode++)for(unsigned serial=0;serial<2;serial++){
    d.mode=1;d.data=value;tick();eq(d.q,value,"load");d.mode=mode;d.serial_in=serial;tick();unsigned want=0;
    switch(mode){case 0:want=0;break;case 1:want=value;break;case 2:want=value/2;break;case 3:want=value*2%256;break;
      case 4:want=value/2+(value&128);break;case 5:want=value/2+128*serial;break;case 6:want=value/2+128*(value%2);break;case 7:want=value*2%256+value/128;break;}
    eq(d.q,want,"shift-mode");d.enable=0;tick();eq(d.q,want,"hold");d.enable=1;
  }
  reset();d.load=1;d.data=1;tick();d.load=0;unsigned ref=1;std::set<unsigned> seen;
  for(int i=0;i<255;i++){
    eq(d.lfsr,ref,"LFSR");if(!seen.insert(d.lfsr).second||!d.lfsr)return 2;
    unsigned feedback=((ref/16)^(ref/8)^(ref/4)^ref)&1;ref=ref/2+128*feedback;tick();
  }
  eq(seen.size(),255,"period cardinality");eq(d.lfsr,1,"period wraps");
  d.load=1;d.data=0;tick();eq(d.lfsr,0,"zero injection");d.load=0;tick();eq(d.lfsr,1,"zero recovery");
  for(unsigned bits=0;bits<4096;bits++){
    reset();unsigned count=0,last=0;
    for(unsigned i=0;i<12;i++){
      unsigned w=(bits>>i)&1;d.w=w;d.eval();unsigned next=(count&&w==last)?count+1:1;
      eq(d.z_mealy,next>=4,"Mealy before sample");tick();count=next;last=w;
      eq(d.z,count>=4,"Moore after sample");eq(d.z_onehot,d.z,"onehot equivalent");
      unsigned state=(w?5:1)+(count>4?3:count-1);eq(d.state,state,"binary state");eq(d.onehot,1u<<state,"onehot state");
    }
  }
  // Exact original 5,000,001-cycle update interval, bounded and without a huge trace.
  reset();eq(d.light,1,"light reset");unsigned expected=1;
  for(unsigned i=0;i<80000017;i++){
    tick();if(i%5000001==0){expected=((expected<<1)|(expected>>15))&65535;eq(d.light,expected,"light rotation");}
    if(i%5000001==1)eq(d.light,expected,"light hold");
  }
  printf("PASS sequential checks=%llu lfsr_period=255 fsm_traces=4096 light_cycles=80000017\n",checks);d.final();return 0;
}

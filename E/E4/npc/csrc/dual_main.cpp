#include "Vdual.h"
#include "verilated.h"
#ifdef TRACE_FST
#include "verilated_fst_c.h"
using Trace=VerilatedFstC;
const char* filename="dual.fst";
#else
#include "verilated_vcd_c.h"
using Trace=VerilatedVcdC;
const char* filename="dual.vcd";
#endif
#include <cstdio>
int main(int argc,char**argv){VerilatedContext ctx;ctx.commandArgs(argc,argv);ctx.traceEverOn(true);Vdual d{&ctx};Trace trace;d.trace(&trace,5);trace.open(filename);
  for(int i=0;i<16;i++){int a=(i/2)%2,b=i%2;d.a=a;d.b=b;d.eval();trace.dump(ctx.time());ctx.timeInc(10);
    printf("%d,%d,%d,%d\n",i*10,a,b,d.f);if(d.f!=(a+b)%2){fprintf(stderr,"FAIL XOR a=%d b=%d actual=%d expected=%d\n",a,b,d.f,(a+b)%2);trace.close();return 1;}}
  trace.close();d.final();puts("PASS XOR 16 samples 4 input combinations");return 0;}

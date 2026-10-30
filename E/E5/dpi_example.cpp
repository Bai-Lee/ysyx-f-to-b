#include "Vdpi_example.h"
#include "Vdpi_example__Dpi.h"
#include "verilated.h"
#include <cstdio>
int add(int a,int b){
#ifdef BAD_DPI
  return a-b;
#else
  return a+b;
#endif
}
int main(int argc,char**argv){VerilatedContext ctx;ctx.commandArgs(argc,argv);Vdpi_example d{&ctx};
 const int pairs[][2]={{1,2},{-7,10},{3,-9},{-8,-3},{2147483646,1},{-2147483647,-1}};
 for(auto &p:pairs){d.a=p[0];d.b=p[1];d.eval();if(int(d.result)!=p[0]+p[1]){fprintf(stderr,"DPI_MISMATCH a=%d b=%d actual=%d expected=%d\n",p[0],p[1],int(d.result),p[0]+p[1]);return 1;}}
 puts("PASS official DPI add example plus6 signed boundary pairs");d.final();return 0;
}

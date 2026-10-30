#include "Vcomb.h"
#include "verilated.h"
#include <cstdint>
#include <cstdio>
#include <cstdlib>
static uint64_t checks=0;
static void eq(uint64_t got,uint64_t want,const char*what,int a=0,int b=0,int op=0){
  ++checks;if(got!=want){std::fprintf(stderr,"FAIL %s a=%d b=%d op=%d actual=%llu expected=%llu\n",what,a,b,op,(unsigned long long)got,(unsigned long long)want);std::exit(1);}
}
static int sign4(int a){return a<8?a:a-16;}
int main(int argc,char**argv){
  VerilatedContext ctx;ctx.commandArgs(argc,argv);Vcomb d{&ctx};
  const unsigned seg[]={0x40,0x79,0x24,0x30,0x19,0x12,0x02,0x78};
  for(int en=0;en<2;en++)for(int x=0;x<256;x++){
    d.en=en;d.x=x;d.eval();int p=0;for(int i=0;i<8;i++)if(x&(1<<i))p=i;
    eq(d.dec24,en?(1<<(x%4)):0,"decode24",x,en);eq(d.dec38,en?(1<<(x%8)):0,"decode38",x,en);
    eq(d.prio,en?p:0,"priority",x,en);eq(d.prio_valid,en&&x,"priority-valid",x,en);eq(d.seg,seg[en?p:0],"sevenseg",x,en);
    int low=x%16,v=en&&low&&!(low&(low-1)),plain=0;for(int i=0;i<4;i++)if(low==(1<<i))plain=i;
    eq(d.enc42_valid,v,"ordinary-valid",x,en);eq(d.enc42,v?plain:0,"ordinary-code",x,en);
  }
  for(int a=0;a<256;a++)for(int b=0;b<256;b++)for(int ci=0;ci<2;ci++){
    d.a=a;d.b=b;d.cin=ci;d.eval();int value=a+b+ci;int s8=(a<128?a:a-256)+(b<128?b:b-256)+ci;
    eq(d.sum8,value&255,"sum8",a,b,ci);eq(d.carry8,value>255,"carry8",a,b,ci);eq(d.ov8,s8< -128||s8>127,"overflow8",a,b,ci);
    int lo=(a%16)+(b%16)+ci,sg=sign4(a%16)+sign4(b%16)+ci;
    eq(d.sum4,lo&15,"sum4",a,b,ci);eq(d.carry4,lo>15,"carry4",a,b,ci);eq(d.ov4,sg< -8||sg>7,"overflow4",a,b,ci);
    eq(d.fa_s,((a&1)+(b&1)+ci)&1,"full-adder-s");eq(d.fa_c,((a&1)+(b&1)+ci)>1,"full-adder-c");
  }
  int wrong_method2=0;
  for(int a=0;a<16;a++)for(int b=0;b<16;b++)for(int op=0;op<8;op++){
    d.a=a;d.b=b;d.op=op;d.eval();int value=0,math=0;
    switch(op){case 0:math=sign4(a)+sign4(b);value=(a+b)&15;break;
      case 1:math=sign4(a)-sign4(b);value=(a-b)&15;break;case 2:value=(~a)&15;break;
      case 3:value=a&b;break;case 4:value=a|b;break;case 5:value=a^b;break;
      case 6:value=sign4(a)<sign4(b);break;case 7:value=a==b;break;}
    eq(d.alu,value,"alu",a,b,op);eq(d.alu_z,value==0,"zero",a,b,op);
    eq(d.alu_c,op==0?a+b>15:op==1?a>=b:0,"carry/no-borrow",a,b,op);
    eq(d.alu_o,op<=1&&(math< -8||math>7),"overflow",a,b,op);
    if(op>=6){eq(d.less_s,sign4(a)<sign4(b),"signed less",a,b);eq(d.less_u,a<b,"unsigned less",a,b);}
    if(op==1){int neg=(-b)&15;bool bad=((a>>3)==(neg>>3))&&((value>>3)!=(a>>3));wrong_method2+=bad!=bool(math< -8||math>7);}
  }
  eq(wrong_method2,16,"minimum-negative counterexamples");
  for(int a=0;a<256;a++)for(int sh=0;sh<8;sh++)for(int left=0;left<2;left++)for(int ar=0;ar<2;ar++){
    d.a=a;d.shamt=sh;d.left=left;d.arithmetic=ar;d.eval();unsigned want=left?(a<<sh)&255:(a>>sh);
    if(!left&&ar&&(a&128)&&sh)want|=(255<<(8-sh))&255;
    eq(d.shift8,want,"barrel8",a,sh,2*left+ar);
  }
  uint32_t rng=260704;
  for(int n=0;n<4096;n++)for(unsigned sh=0;sh<32;sh++){
    rng=rng*1664525u+1013904223u;d.data32=rng;d.shamt32=sh;
    for(int kind=0;kind<3;kind++){
      d.left=kind==0;d.arithmetic=kind==2;d.eval();uint32_t want=kind==0?rng<<sh:rng>>sh;
      if(kind==2&&(rng&0x80000000u)&&sh)want|=~0u<<(32-sh);
      eq(d.shift32,want,"barrel32",n,sh,kind);
    }
  }
  std::printf("PASS comb checks=%llu method2_counterexamples=%d seed=260704\n",(unsigned long long)checks,wrong_method2);d.final();return 0;
}

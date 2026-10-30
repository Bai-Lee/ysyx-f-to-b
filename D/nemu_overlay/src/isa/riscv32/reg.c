#include <isa.h>
#include "local-include/reg.h"
#include <errno.h>
const char *regs[]={"$0","ra","sp","gp","tp","t0","t1","t2","s0","s1","a0","a1","a2","a3","a4","a5","a6","a7","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","t3","t4","t5","t6"};
void isa_reg_display(void){for(int i=0;i<32;i++)printf("REG x%-2d %-3s 0x%08x %u\n",i,regs[i],cpu.gpr[i],cpu.gpr[i]);printf("PC 0x%08x\n",cpu.pc);}
word_t isa_reg_str2val(const char *s,bool *success){
 *success=false;if(!s)return 0;if(!strcmp(s,"pc")){*success=true;return cpu.pc;}
 if(!strcmp(s,"0")||!strcmp(s,"zero")||!strcmp(s,"$0")){*success=true;return 0;}
 if(!strcmp(s,"fp")){*success=true;return cpu.gpr[8];}
 for(int i=0;i<32;i++)if(!strcmp(s,regs[i])){*success=true;return cpu.gpr[i];}
 if(s[0]=='x'&&s[1]){char *end;errno=0;unsigned long i=strtoul(s+1,&end,10);if(!errno&&!*end&&i<32){*success=true;return cpu.gpr[i];}}
 return 0;
}

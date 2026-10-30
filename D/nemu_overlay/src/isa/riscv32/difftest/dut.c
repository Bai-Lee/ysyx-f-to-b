#include <isa.h>
#include <cpu/difftest.h>
#include "../local-include/reg.h"
bool isa_difftest_checkregs(CPU_state *ref_r,vaddr_t pc){
 bool ok=true;
 if(cpu.pc!=ref_r->pc){fprintf(stderr,"DIFF_MISMATCH at=0x%08x PC dut=0x%08x ref=0x%08x\n",pc,cpu.pc,ref_r->pc);ok=false;}
 for(int i=0;i<32;i++)if(cpu.gpr[i]!=ref_r->gpr[i]){fprintf(stderr,"DIFF_MISMATCH at=0x%08x x%d dut=0x%08x ref=0x%08x\n",pc,i,cpu.gpr[i],ref_r->gpr[i]);ok=false;}
 return ok;
}
void isa_difftest_attach(void){}

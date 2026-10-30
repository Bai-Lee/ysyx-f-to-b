#include <isa.h>
#include <cpu/cpu.h>
#include <difftest-def.h>
#include <memory/paddr.h>

/* Stable local ABI: 32 little-endian uint32 GPR followed by uint32 PC. */
_Static_assert(sizeof(CPU_state)==33*sizeof(uint32_t),"unexpected RV32 reference ABI");
static void check_span(paddr_t address,size_t n){
  Assert((uint64_t)address>=CONFIG_MBASE && (uint64_t)address<=(uint64_t)CONFIG_MBASE+CONFIG_MSIZE &&
         n<=(uint64_t)CONFIG_MBASE+CONFIG_MSIZE-address,"REF_MEMORY_RANGE address=%08x size=%zu",address,n);
}
__EXPORT void difftest_memcpy(paddr_t addr,void *buf,size_t n,bool direction){
  check_span(addr,n);Assert(buf||n==0,"REF null memory buffer");if(!n)return;
  if(direction==DIFFTEST_TO_REF)memcpy(guest_to_host(addr),buf,n);
  else memcpy(buf,guest_to_host(addr),n);
}
__EXPORT void difftest_regcpy(void *dut,bool direction){
  Assert(dut,"REF null register buffer");
  if(direction==DIFFTEST_TO_REF){memcpy(&cpu,dut,sizeof cpu);cpu.gpr[0]=0;}
  else memcpy(dut,&cpu,sizeof cpu);
}
__EXPORT void difftest_exec(uint64_t n){cpu_exec(n);}
__EXPORT void difftest_raise_intr(word_t no){panic("REF_INTERRUPT_UNSUPPORTED number=%u; outside D-stage TRM",no);}
__EXPORT void difftest_init(int port){
  (void)port;void init_mem(void);extern uint64_t g_nr_guest_inst;
  init_mem();memset(guest_to_host(CONFIG_MBASE),0,CONFIG_MSIZE);memset(&cpu,0,sizeof cpu);
  g_nr_guest_inst=0;nemu_state.state=NEMU_STOP;nemu_state.halt_pc=0;nemu_state.halt_ret=0;init_isa();
}

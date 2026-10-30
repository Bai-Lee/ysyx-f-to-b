/***************************************************************************************
* Copyright (c) 2014-2024 Zihao Yu, Nanjing University
*
* NEMU is licensed under Mulan PSL v2.
* You can use this software according to the terms and conditions of the Mulan PSL v2.
* You may obtain a copy of Mulan PSL v2 at:
*          http://license.coscl.org.cn/MulanPSL2
*
* THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
* EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
* MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
*
* See the Mulan PSL v2 for more details.
***************************************************************************************/

#include <isa.h>
#include <cpu/cpu.h>
#include <difftest-def.h>
#include <memory/paddr.h>
extern void c5_csr_reset(void);

/* Stable local ABI: 32 little-endian uint32 GPR followed by uint32 PC. */
_Static_assert(sizeof(CPU_state)==33*sizeof(uint32_t),"unexpected RV32 reference ABI");
extern bool c5_memory_span(paddr_t address,size_t n);
static void check_span(paddr_t address,size_t n){
 Assert(c5_memory_span(address,n),"REF_MEMORY_RANGE address=%08x size=%zu",address,n);
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
  init_mem();memset(&cpu,0,sizeof cpu);
  g_nr_guest_inst=0;nemu_state.state=NEMU_STOP;nemu_state.halt_pc=0;nemu_state.halt_ret=0;init_isa();
  /* init_isa's standalone demonstration image must not prefill SoC PSRAM. */
  init_mem();
  c5_csr_reset();
}

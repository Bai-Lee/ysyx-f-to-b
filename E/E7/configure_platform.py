from common7 import *
from install_prebuilt import install
def main():
 am=BENCH7/'abstract-machine';npc=BENCH7/'npc';p=ROOT/'E/E7';patch=p/'runtime_patch';patch.mkdir(exist_ok=True)
 trm='''#include <am.h>
#include <klib-macros.h>
#include "e7_config.h"
extern char _heap_start, _pmem_start;
int main(const char *args);
#ifdef __PLATFORM_YSYXSOC
#define PMEM_SIZE (8 * 1024 * 1024)
#else
#define PMEM_SIZE (128 * 1024 * 1024)
#endif
Area heap = RANGE(&_heap_start, (uintptr_t)&_pmem_start + PMEM_SIZE);
static const char mainargs[MAINARGS_MAX_LEN] = TOSTRING(MAINARGS_PLACEHOLDER);
void putch(char ch) {
#ifdef __PLATFORM_YSYXSOC
  volatile uint8_t *uart=(volatile uint8_t *)0x10000000u;
  while ((uart[5] & 0x20u) == 0) {}
  uart[0]=(uint8_t)ch;
#else
  while (*(volatile uint32_t *)0x10000004u == 0) {}
  *(volatile uint8_t *)0x10000000u = (uint8_t)ch;
#endif
}
void halt(int code) {
  asm volatile("mv a0, %0; ebreak" : : "r"(code) : "a0", "memory");
  while (1) {}
}
void _trm_init() {
#ifdef __PLATFORM_YSYXSOC
  volatile uint8_t *uart=(volatile uint8_t *)0x10000000u;
  uart[3]=0x80; uart[0]=UART_DIVISOR&0xff; uart[1]=(UART_DIVISOR>>8)&0xff;
  uart[3]=0x03; uart[1]=0; uart[2]=0x07;
#endif
  halt(main(mainargs));
}
'''
 timer='''#include <am.h>
#include "e7_config.h"
static uint64_t boot_cycles;
static uint64_t read_cycles(void) {
  uint32_t hi,lo,again;
  /* A high-low-high retry also works when the 64-bit counter crosses a boundary. */
  do {
    asm volatile("csrr %0, mcycleh":"=r"(hi));
    asm volatile("csrr %0, mcycle":"=r"(lo));
    asm volatile("csrr %0, mcycleh":"=r"(again));
  } while (hi!=again);
  return ((uint64_t)hi<<32)|lo;
}
void __am_timer_init() { boot_cycles=read_cycles(); }
void __am_timer_uptime(AM_TIMER_UPTIME_T *uptime) {
#ifdef __PLATFORM_YSYXSOC
  const uint32_t hz=SOC_CPU_HZ;
#else
  const uint32_t hz=NPC_CPU_HZ;
#endif
  uptime->us=(read_cycles()-boot_cycles)/(hz/1000000u);
}
void __am_timer_rtc(AM_TIMER_RTC_T *rtc) {
  *rtc=(AM_TIMER_RTC_T){.year=1900};
}
'''
 config='#ifndef E7_CONFIG_H\n#define E7_CONFIG_H\n#define NPC_CPU_HZ 100000000u\n#define SOC_CPU_HZ 25000000u\n#define UART_DIVISOR 13u\n#endif\n'
 for n,s in [('trm.c',trm),('timer.c',timer),('e7_config.h',config)]:
  (am/'am/src/riscv/npc'/n).write_text(s);(patch/n).write_text(s)
 mk=am/'scripts/platform/npc.mk';s=mk.read_text().replace('sim IMAGE="$(IMAGE).bin"','sim PLATFORM="$(PLATFORM)" IMAGE="$(IMAGE).bin"');mk.write_text(s);shutil.copyfile(mk,patch/'npc.mk')
 smk=am/'scripts/minirv-ysyxsoc.mk';smk.write_text('include $(AM_HOME)/scripts/minirv-npc.mk\nimage: image-dep\n\tcd $(AM_HOME)/../ysyxSoC/ready-to-run/minirv && bash gen.sh $(IMAGE).elf $(IMAGE).bin\n');shutil.copyfile(smk,patch/smk.name)
 mf='''.DEFAULT_GOAL := all
PLATFORM ?= npc
NPC_MODE ?= $(if $(filter ysyxsoc,$(PLATFORM)),soc,valid)
NPC_ARGS ?=
BIN := /home/USER/e-stage/build/E7/$(NPC_MODE)/sim
PYTHON := python3
BUILDER := /workspace/projects/ysyx_f_to_b/E/E7/build.py
SOURCES := /workspace/projects/ysyx_f_to_b/E/E5/rtl/minirv_decode.sv /workspace/projects/ysyx_f_to_b/E/E5/rtl/minirv_regfile.sv /workspace/projects/ysyx_f_to_b/E/E7/rtl/minirv_bus.sv
ifneq ($(filter soc soc_gui,$(NPC_MODE)),)
SOURCES += /workspace/projects/ysyx_f_to_b/E/E7/rtl/ysyx_00000000.sv /workspace/projects/ysyx_f_to_b/E/E7/rtl/mygpio_top_apb.v
HARNESS := /workspace/projects/ysyx_f_to_b/E/E7/soc_runner.cpp
else
HARNESS := /workspace/projects/ysyx_f_to_b/E/E7/bus_runner.cpp
endif
all: $(BIN)
$(BIN): $(SOURCES) $(BUILDER) $(HARNESS)
\t$(PYTHON) $(BUILDER) --mode $(NPC_MODE)
sim: $(BIN)
\t$(call git_commit, "sim RTL") # DO NOT REMOVE THIS LINE!!!
ifneq ($(filter soc soc_gui,$(NPC_MODE)),)
\t$(BIN) --image "$(IMAGE)" --report "$(IMAGE).npc.json" $(if $(filter soc_gui,$(NPC_MODE)),--gui,) --max-cycles 100000000000 $(NPC_ARGS)
else
\t$(BIN) --image "$(IMAGE)" --mode $(if $(filter ifu,$(NPC_MODE)),1,$(if $(filter lsu,$(NPC_MODE)),2,3)) --report "$(IMAGE).npc.json" --frequency 100000000 --uart-random --max-cycles 100000000000 $(NPC_ARGS)
endif
include ../Makefile
YSYX_HOME := $(abspath ..)
STUID :=
STUNAME := AI_E_STAGE
MAKEOVERRIDES += YSYX_HOME=$(YSYX_HOME) STUID= STUNAME=$(STUNAME)
.PHONY: all sim
'''
 (npc/'Makefile').write_text(mf);(patch/'NPC.Makefile').write_text(mf)
 fixed=patch/'minirv-common.fixed.sh'
 if fixed.exists():shutil.copyfile(fixed,am/'tools/minirv/minirv-common.sh')
 # Replace only the provided empty GPIO exercise module in the E7 working copy.
 gpio=BENCH7/'ysyxSoC/perip/gpio/mygpio_top_apb.v';original=p/'upstream/mygpio_top_apb.v';original.parent.mkdir(exist_ok=True)
 if not original.exists():shutil.copyfile(gpio,original)
 shutil.copyfile(p/'rtl/mygpio_top_apb.v',gpio)
 dest=BENCH7/'am-kernels/tests/e7-gpio';dest.mkdir(exist_ok=True);shutil.copyfile(p/'programs/gpio.c',dest/'main.c');(dest/'Makefile').write_text('NAME=e7-gpio\nSRCS=main.c\ninclude $(AM_HOME)/Makefile\n')
 for arch in ['minirv-npc','minirv-ysyxsoc']:install(am,arch,'E7/klib/'+arch)
 dump(ROOT/'reports/E7_platform_patch.json',{'status':'PREPARED_NOT_YET_VALIDATED','files':[{'path':str(f),'sha256':sha(f)} for f in patch.iterdir()],'clock_settings':{'standalone_hz':100000000,'soc_hz':25000000,'uart_divisor':13},'note':'Standalone comparisons hold a common assumed100MHz; final SoC experiments use measured synthesis limits. UART divisor13 matches the actual supplied-loader transactions observed in loader_pilot.'})
 print('E7_PLATFORM_PREPARED',flush=True)
if __name__=='__main__':main()

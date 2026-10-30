from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    d=ROOT/'D/D8';npc=BENCH/'npc';am=BENCH/'abstract-machine';n=BENCH/'nemu'
    (npc/'csrc').mkdir(parents=True,exist_ok=True);(npc/'vsrc').mkdir(exist_ok=True)
    for name in ['rv32e_core.sv','npc_sim.sv']:shutil.copyfile(d/name,npc/'vsrc'/name)
    for name in ['runner.cpp','memory.hpp']:shutil.copyfile(d/name,npc/'csrc'/name)
    for name in ['debug_core.c','debug_core.h','trace_core.c','trace_core.h']:shutil.copyfile(ROOT/'D/runtime'/name,npc/'csrc'/name)
    cap=n/'tools/capstone/repo';ref=Path(json.loads((ROOT/'reports/D8_reference.json').read_text())['shared_object'])
    make=npc/'Makefile';make.write_text('''.DEFAULT_GOAL := all
VERILATOR := '''+str(VERILATOR)+'''
BUILD ?= $(CURDIR)/build
BIN := $(BUILD)/sim
FAULT_ADDI ?= 0
RTL := $(CURDIR)/vsrc/rv32e_core.sv $(CURDIR)/vsrc/npc_sim.sv
CPP := $(CURDIR)/csrc/runner.cpp
HEADERS := $(wildcard $(CURDIR)/csrc/*.h) $(CURDIR)/csrc/memory.hpp
CORE := $(BUILD)/debug_core.o $(BUILD)/trace_core.o
NPC_ARGS ?=
all: $(BIN)
$(BUILD)/%.o: $(CURDIR)/csrc/%.c $(HEADERS)
	mkdir -p $(BUILD)
	gcc -std=c11 -O3 -g -Wall -Wextra -Werror -c $< -o $@
$(BIN): $(RTL) $(CPP) $(HEADERS) $(CORE)
	VERILATOR_ROOT='''+str(VROOT)+''' $(VERILATOR) --cc --exe --build -j 1 --assert -Wall --timescale 1ns/1ns --top-module npc_sim -GFAULT_ADDI=$(FAULT_ADDI) --Mdir $(BUILD) -o sim -CFLAGS '-O3 -g -Wall -Wextra -Werror -I'''+str(cap/'include')+''' -I$(CURDIR)/csrc' -LDFLAGS '-L'''+str(cap)+''' -l:libcapstone.so.5 -Wl,-rpath,'''+str(cap)+''' -ldl' $(RTL) $(CPP) $(CORE)
sim: $(BIN)
	$(call git_commit, "sim RV32E RTL")
	$(BIN) --image "$(IMAGE)" --elf "$(ELF)" --ref '''+str(ref)+''' --max-cycles 10000000000 --report "$(IMAGE).npc.json" $(NPC_ARGS)
include ../Makefile
YSYX_HOME := $(abspath ..)
STUID := LOCAL_D_STAGE
STUNAME := Independent_Local_Implementation
MAKEOVERRIDES += YSYX_HOME=$(YSYX_HOME) STUID=$(STUID) STUNAME=$(STUNAME)
.PHONY: all sim
''')
    # Reuse the already documented UART/RTC platform convention, with explicit
    # copies; no edits to E's snapshots or execution trees.
    before=d/'upstream';before.mkdir(exist_ok=True)
    for name,rel in [('trm.c','am/src/riscv/npc/trm.c'),('timer.c','am/src/riscv/npc/timer.c'),('npc.mk','scripts/platform/npc.mk')]:
        target=am/rel
        if not (before/name).exists():shutil.copyfile(target,before/name)
        content=(ROOT/'E/E6/runtime_snapshot'/name).read_text()
        if name=='npc.mk':
            content=content.replace('IMAGE="$(IMAGE).bin" NPC_ARGS=', 'IMAGE="$(IMAGE).bin" ELF="$(IMAGE).elf" NPC_ARGS=')
            content=content.replace('           riscv/npc/cte.c \\\n','').replace('           riscv/npc/trap.S \\\n','')
        target.write_text(content)
    isa=am/'scripts/riscv32e-npc.mk';content=isa.read_text();content=content.replace('-march=rv32e_zicsr','-march=rv32e')
    isa.write_text(content) # No CSR instructions are admitted in the D-stage TRM.
    inputs=[make,*list((npc/'vsrc').glob('*.sv')),*list((npc/'csrc').glob('*')),ref,cap/'libcapstone.so.5']
    exe=npc/'build/sim';run('D8/npc/build',['make','-j1'],cwd=npc,inputs=inputs,outputs=[exe],timeout=300)
    dump(ROOT/'reports/D8_build.json',{'status':'BUILT_NOT_YET_QUALIFIED','executable':str(exe),'sha256':sha(exe),'reference':str(ref),'capstone':str(cap/'libcapstone.so.5'),'inputs':[{'path':str(p),'sha256':sha(p)} for p in inputs]})

if __name__=='__main__':main()

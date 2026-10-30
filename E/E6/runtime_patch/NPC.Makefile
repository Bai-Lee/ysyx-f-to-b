.DEFAULT_GOAL := all
VERILATOR := /home/USER/tools/verilator-stable-src/bin/verilator
BUILD := $(CURDIR)/build
BIN := $(BUILD)/sim
RTL := $(addprefix $(CURDIR)/vsrc/, minirv_decode.sv minirv_regfile.sv minirv_single.sv npc_sim.sv)
CPP := $(CURDIR)/csrc/runner.cpp
HEADERS := $(CURDIR)/csrc/ref.h $(CURDIR)/csrc/memory.hpp
NPC_ARGS ?=
all: $(BIN)
$(BUILD)/ref.o: $(CURDIR)/csrc/ref.c $(CURDIR)/csrc/ref.h
	mkdir -p $(BUILD)
	gcc -std=c11 -O3 -g -Wall -Wextra -Werror -c $< -o $@
$(BIN): $(RTL) $(CPP) $(HEADERS) $(BUILD)/ref.o
	VERILATOR_ROOT=/home/USER/tools/verilator-stable-src $(VERILATOR) --cc --exe --build -j 1 --assert -Wall --timescale 1ns/1ns --top-module npc_sim "-GRESET_PC=32'h80000000" --Mdir $(BUILD) -o sim -CFLAGS '-O3 -g' $(RTL) $(CPP) $(BUILD)/ref.o
sim: $(BIN)
	$(call git_commit, "sim RTL") # DO NOT REMOVE THIS LINE!!!
	$(BIN) --image "$(IMAGE)" --base 0x80000000 --mem-mb 128 --devices --max-cycles 10000000000 --report "$(IMAGE).npc.json" $(NPC_ARGS)
include ../Makefile
YSYX_HOME := $(abspath ..)
STUID :=
STUNAME := AI_E_STAGE
MAKEOVERRIDES += YSYX_HOME=$(YSYX_HOME) STUID= STUNAME=$(STUNAME)
.PHONY: all sim

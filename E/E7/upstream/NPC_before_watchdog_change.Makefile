.DEFAULT_GOAL := all
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
	$(PYTHON) $(BUILDER) --mode $(NPC_MODE)
sim: $(BIN)
	$(call git_commit, "sim RTL") # DO NOT REMOVE THIS LINE!!!
ifeq ($(NPC_MODE),soc)
	$(BIN) --image "$(IMAGE)" --report "$(IMAGE).npc.json" $(NPC_ARGS)
else
	$(BIN) --image "$(IMAGE)" --mode $(if $(filter ifu,$(NPC_MODE)),1,$(if $(filter lsu,$(NPC_MODE)),2,3)) --report "$(IMAGE).npc.json" --frequency 100000000 --uart-random $(NPC_ARGS)
endif
include ../Makefile
YSYX_HOME := $(abspath ..)
STUID :=
STUNAME := AI_E_STAGE
MAKEOVERRIDES += YSYX_HOME=$(YSYX_HOME) STUID= STUNAME=$(STUNAME)
.PHONY: all sim

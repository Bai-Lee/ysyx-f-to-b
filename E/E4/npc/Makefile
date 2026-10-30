.DEFAULT_GOAL := all
VERILATOR ?= /home/USER/tools/verilator-stable-src/bin/verilator
BUILD_DIR := $(CURDIR)/build
BIN := $(BUILD_DIR)/dual
SOURCES := $(CURDIR)/vsrc/dual.sv $(CURDIR)/csrc/dual_main.cpp
all: $(BIN)
$(BIN): $(SOURCES)
	mkdir -p $(BUILD_DIR)
	VERILATOR_ROOT=/home/USER/tools/verilator-stable-src $(VERILATOR) --cc --exe --build -j 2 --assert -Wall --trace --top-module dual --Mdir $(BUILD_DIR) -o dual $(SOURCES)
sim: $(BIN)
	$(call git_commit, "sim RTL") # DO NOT REMOVE THIS LINE!!!
	cd $(BUILD_DIR) && ./dual
include ../Makefile
YSYX_HOME := $(abspath ..)
STUID :=
STUNAME := AI_AUTONOMOUS_ENGINEERING_TEST
MAKEOVERRIDES += YSYX_HOME=$(YSYX_HOME) STUID= STUNAME=$(STUNAME)
.PHONY: all sim

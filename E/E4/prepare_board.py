from common import *
def main():
    p=ROOT/'E/E4/constr';p.mkdir(exist_ok=True)
    lines=['top=lab_board','sw ('+', '.join('SW'+str(i) for i in reversed(range(12)))+')','btn (BTNL, BTNU, BTNR, BTND, BTNC)','led ('+', '.join('LD'+str(i) for i in reversed(range(16)))+')']
    for i in range(8):lines.append('seg'+str(i)+' ('+', '.join('SEG'+str(i)+c for c in 'ABCDEFG')+', DEC'+str(i)+'P)')
    for x in ['VGA_HSYNC','VGA_VSYNC','VGA_BLANK_N']:lines.append(x+' '+x)
    for x in 'RGB':lines.append('VGA_'+x+' ('+', '.join('VGA_'+x+str(i) for i in reversed(range(8)))+')')
    lines+=['ps2_clk PS2_CLK','ps2_data PS2_DAT','uart_tx UART_TX']
    (p/'lab_board.nxdc').write_text('\n'.join(lines)+'\n')
    npc=ROOT/'E/E4/npc';(npc/'vsrc').mkdir(parents=True,exist_ok=True);(npc/'csrc').mkdir(exist_ok=True)
    shutil.copyfile(ROOT/'E/E4/rtl/dual.sv',npc/'vsrc/dual.sv');shutil.copyfile(ROOT/'E/E4/csrc/dual_test.cpp',npc/'csrc/dual_main.cpp')
    (npc/'Makefile').write_text('''.DEFAULT_GOAL := all
VERILATOR ?= /home/USER/tools/verilator-stable-src/bin/verilator
BUILD_DIR := $(CURDIR)/build
BIN := $(BUILD_DIR)/dual
SOURCES := $(CURDIR)/vsrc/dual.sv $(CURDIR)/csrc/dual_main.cpp
all: $(BIN)
$(BIN): $(SOURCES)
\tmkdir -p $(BUILD_DIR)
\tVERILATOR_ROOT=/home/USER/tools/verilator-stable-src $(VERILATOR) --cc --exe --build -j 2 --assert -Wall --trace --top-module dual --Mdir $(BUILD_DIR) -o dual $(SOURCES)
sim: $(BIN)
\t$(call git_commit, "sim RTL") # DO NOT REMOVE THIS LINE!!!
\tcd $(BUILD_DIR) && ./dual
include ../Makefile
YSYX_HOME := $(abspath ..)
STUID :=
STUNAME := AI_AUTONOMOUS_ENGINEERING_TEST
MAKEOVERRIDES += YSYX_HOME=$(YSYX_HOME) STUID= STUNAME=$(STUNAME)
.PHONY: all sim
''')
    target=Path('/home/USER/ysyx-workbench/npc')
    original_ignore=OUT/'framework/original/npc_gitignore'
    if not original_ignore.exists():shutil.copyfile(target/'.gitignore',original_ignore)
    text=original_ignore.read_text()
    (npc/'.gitignore').write_text(text+'\n!*.sv\n!*.nxdc\n')
    shutil.copytree(npc,target,dirs_exist_ok=True)
    print('BOARD_AND_NPC_PREPARED',flush=True)
if __name__=='__main__':main()

from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
    p=ROOT/'E/E6';am=BENCH/'abstract-machine';npc=BENCH/'npc';(npc/'csrc').mkdir(exist_ok=True);(npc/'vsrc').mkdir(exist_ok=True)
    for src in (ROOT/'E/E5/rtl').glob('*.sv'):shutil.copyfile(src,npc/'vsrc'/src.name)
    for name in ['ref.c','ref.h','runner.cpp','memory.hpp']:shutil.copyfile(ROOT/'E/runtime'/name,npc/'csrc'/name)
    makefile='''.DEFAULT_GOAL := all
VERILATOR := /home/USER/tools/verilator-stable-src/bin/verilator
BUILD := $(CURDIR)/build
BIN := $(BUILD)/sim
RTL := $(addprefix $(CURDIR)/vsrc/, minirv_decode.sv minirv_regfile.sv minirv_single.sv npc_sim.sv)
CPP := $(CURDIR)/csrc/runner.cpp
HEADERS := $(CURDIR)/csrc/ref.h $(CURDIR)/csrc/memory.hpp
NPC_ARGS ?=
all: $(BIN)
$(BUILD)/ref.o: $(CURDIR)/csrc/ref.c $(CURDIR)/csrc/ref.h
\tmkdir -p $(BUILD)
\tgcc -std=c11 -O3 -g -Wall -Wextra -Werror -c $< -o $@
$(BIN): $(RTL) $(CPP) $(HEADERS) $(BUILD)/ref.o
\tVERILATOR_ROOT=/home/USER/tools/verilator-stable-src $(VERILATOR) --cc --exe --build -j 1 --assert -Wall --timescale 1ns/1ns --top-module npc_sim "-GRESET_PC=32'h80000000" --Mdir $(BUILD) -o sim -CFLAGS '-O3 -g' $(RTL) $(CPP) $(BUILD)/ref.o
sim: $(BIN)
\t$(call git_commit, "sim RTL") # DO NOT REMOVE THIS LINE!!!
\t$(BIN) --image "$(IMAGE)" --base 0x80000000 --mem-mb 128 --devices --max-cycles 10000000000 --report "$(IMAGE).npc.json" $(NPC_ARGS)
include ../Makefile
YSYX_HOME := $(abspath ..)
STUID :=
STUNAME := AI_E_STAGE
MAKEOVERRIDES += YSYX_HOME=$(YSYX_HOME) STUID= STUNAME=$(STUNAME)
.PHONY: all sim
'''
    (npc/'Makefile').write_text(makefile)
    ignore=npc/'.gitignore';text=ignore.read_text()
    for rule in ['!*.sv','!*.hpp']:
        if rule not in text.splitlines():text+='\n'+rule+'\n'
    ignore.write_text(text)
    trm=am/'am/src/riscv/npc/trm.c';source=trm.read_text()
    old='void halt(int code) {\n  while (1);\n}'
    new='void halt(int code) {\n  asm volatile("mv a0, %0; ebreak" : : "r"(code) : "a0", "memory");\n  while (1);\n}'
    if old in source:source=source.replace(old,new)
    else:assert 'asm volatile("mv a0, %0; ebreak"' in source
    trm.write_text(source)
    platform=am/'scripts/platform/npc.mk';text=platform.read_text();text=text.replace('echo "TODO: add command here to run simulation"','$(MAKE) -s -C $(NPC_HOME) sim IMAGE="$(IMAGE).bin" NPC_ARGS="$(NPC_ARGS)"');platform.write_text(text)
    tests=BENCH/'am-kernels/tests/cpu-tests';mf=tests/'Makefile';text=mf.read_text()
    old='\t@grep -q "FAIL" $(RESULT) | grep -v "wrong\\]"; FAIL=$$?; rm $(RESULT); test $$FAIL -ne 0'
    new='\t@if grep -q "FAIL" $(RESULT); then exit 1; fi'
    if old in text:text=text.replace(old,new)
    else:assert new in text
    mf.write_text(text)
    run('E6/runtime/npc_build',['make','-j1'],cwd=npc,inputs=[npc/'Makefile',trm,platform],timeout=300)
    records=[]
    for name,expected in [('dummy',0),('wrong',2)]:
        image=tests/'build'/(name+'-minirv-npc.bin');result=Path(str(image)+'.npc.json')
        o,e,r=run('E6/runtime/'+name,['make','-j1','ARCH=minirv-npc','ALL='+name,'run','YSYX_HOME='+str(BENCH),'STUID=','STUNAME=AI_E_STAGE'],cwd=tests,inputs=[trm,platform,mf],expected=(expected,),timeout=180,outputs=[result])
        result_data=json.loads(result.read_text());assert result_data['ebreak_calls']==1 and result_data['result']==('GOOD_TRAP' if name=='dummy' else 'BAD_TRAP')
        assert ('***FAIL***' in o)==(name=='wrong')
        records.append({'program':name,'make_exit':r['exit_code'],'simulation':result_data,'result_sha256':sha(result)})
    out=p/'runtime_patch';out.mkdir(exist_ok=True)
    for name,file in [('trm.c',trm),('npc.mk',platform),('cpu-tests.Makefile',mf),('NPC.Makefile',npc/'Makefile')]:shutil.copyfile(file,out/name)
    dump(ROOT/'reports/E6_halt_and_exit.json',{'status':'PASS','records':records,'notes':'Original CPU-test parent recipe hid failures via a grep-q pipeline; fixed aggregation, with deliberate wrong retained as a separate expected-rejection control.'})
    mark(['E6-M003','E6-M004','E6-M005','E6-M006'],'PASS',['reports/E6_halt_and_exit.json','artifacts/E6/runtime','E/E6/runtime_patch'],'AM embeds a0 result plus ebreak. make uses its just-built binary path; dummyGOOD/exit0, wrongBAD/make-nonzero; error aggregation is verified rather than trusting text alone.')
    print('AM_TERMINATION_AND_ERROR_PROPAGATION_PASS',flush=True)
if __name__=='__main__':main()

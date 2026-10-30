from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
 npc=BENCH/'npc';rt=ROOT/'E/runtime';sources=[npc/'vsrc'/n for n in ['minirv_decode.sv','minirv_regfile.sv','minirv_single.sv','npc_sim.sv']]
 exe=build('E6/fault_sign','npc_sim',sources,[npc/'csrc/runner.cpp'],extra=[npc/'build/ref.o'],flags=['--timescale','1ns/1ns',"-GRESET_PC=32'h80000000",'+define+FAULT_SIGN_EXT','-CFLAGS','-O3'],additional_inputs=[npc/'csrc/memory.hpp',npc/'csrc/ref.h'])
 mf=npc/'Makefile';s=mf.read_text()
 if 'SIM ?=' not in s:s=s.replace('NPC_ARGS ?=','SIM ?= $(BIN)\nNPC_ARGS ?=').replace('\t$(BIN) --image','\t$(SIM) --image');mf.write_text(s)
 cwd=BENCH/'riscv-tests';image=cwd/'build/addi-minirv-npc.bin';result=Path(str(image)+'.npc.json')
 o,e,r=run('E6/fault_sign/make_reject',['make','-j1','ARCH=minirv-npc','ALL=addi','run','SIM='+str(exe)],cwd=cwd,inputs=[mf,exe],outputs=[result],expected=(2,),timeout=180)
 d=json.loads(result.read_text());assert d['result']=='DIFF_FAIL' and 'DIFF step=' in e and '***FAIL***' in o
 dump(ROOT/'reports/E6_difftest_negative.json',{'status':'PASS_EXPECTED_REJECTION','fault':'FAULT_SIGN_EXT','make_exit':r['exit_code'],'simulation':d,'diagnostic':e[-2500:]})
 # Restore an ordinary valid run to prove the failure is caused by the injected RTL error.
 run('E6/fault_sign/positive_control',['make','-j1','ARCH=minirv-npc','ALL=addi','run'],cwd=cwd,inputs=[npc/'build/sim',mf],outputs=[result],timeout=180)
 assert json.loads(result.read_text())['result']=='GOOD_TRAP'
 mark(['E6-M008'],'PASS',['reports/E6_difftest_negative.json','artifacts/E6/fault_sign'],'Actual RTL sign-extension mutant produces first-mismatch PC/instruction/register diagnostic, simulator nonzero and top-level make FAIL; valid control restored and passes.')
 print('E6_DIFFTEST_MAKE_NEGATIVE_PASS',flush=True)
if __name__=='__main__':main()

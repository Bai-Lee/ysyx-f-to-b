from pathlib import Path
import sys,tarfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
def main():
    p=ROOT/'E/E6';back=p/'upstream';back.mkdir(exist_ok=True)
    am=BENCH/'abstract-machine'
    for name in ['am/src/riscv/npc/trm.c','am/src/riscv/npc/timer.c','scripts/platform/npc.mk','scripts/isa/riscv.mk']:
        src=am/name;dst=back/name;dst.parent.mkdir(parents=True,exist_ok=True)
        if not dst.exists():shutil.copyfile(src,dst)
    tests=BENCH/'am-kernels/tests/cpu-tests'
    dst=back/'cpu-tests.Makefile'
    if not dst.exists():shutil.copyfile(tests/'Makefile',dst)
    # Empty hosted-glibc32 ABI stubs are an overlay for this freestanding target.
    overlay=p/'toolchain/gnu';overlay.mkdir(parents=True,exist_ok=True)
    (overlay/'stubs-ilp32.h').write_text('/* Bare-metal only: no hosted glibc32 ABI is linked. */\n')
    isa=am/'scripts/isa/riscv.mk';text=isa.read_text()
    line='\nCFLAGS += -I'+str(overlay.parent)+'\n'
    if str(overlay.parent) not in text:isa.write_text(text+line)
    run('E6/toolchain/riscv32_dummy',['make','-j1','ARCH=riscv32-nemu','ALL=dummy','YSYX_HOME='+str(BENCH),'STUID=','STUNAME=AI_E_STAGE'],cwd=tests,timeout=180)
    run('E6/toolchain/minirv_dummy_original',['make','-j1','ARCH=minirv-npc','ALL=dummy','YSYX_HOME='+str(BENCH),'STUID=','STUNAME=AI_E_STAGE'],cwd=tests,timeout=180)
    image=tests/'build/dummy-minirv-npc.bin';elf=tests/'build/dummy-minirv-npc.elf'
    assert image.exists() and elf.exists()
    source=ROOT/'E/E5/rtl';rt=ROOT/'E/runtime';obj=WORK/'lib/ref.o'
    files=[source/n for n in ['minirv_decode.sv','minirv_regfile.sv','minirv_single.sv','npc_sim.sv']]
    exe=build('E6/npc','npc_sim',files,[rt/'runner.cpp'],extra=[obj],flags=['--timescale','1ns/1ns',"-GRESET_PC=32'h80000000",'-CFLAGS','-O3'],additional_inputs=[rt/'memory.hpp',rt/'ref.h'])
    folder=ROOT/'artifacts/E6/dummy_original';folder.mkdir(parents=True,exist_ok=True)
    trace=WORK/'dummy_original.csv';report=folder/'result.json'
    o,e,r=run('E6/dummy_original/run',[exe,'--image',image,'--base','0x80000000','--mem-mb','128','--steps','20000','--expect','0','--max-cycles','20000','--trace',trace,'--report',report],inputs=[exe,image],outputs=[trace,report],timeout=90)
    assert 'REQUESTED_STEPS_COMPLETE' in e and json.loads(report.read_text())['ebreak_calls']==0
    o,e,r=run('E6/dummy_original/symbols',['riscv64-linux-gnu-nm','-S','-n',elf],inputs=[elf])
    halt=next((line for line in o.splitlines() if line.endswith(' halt')),None)
    symbol=halt or next(line for line in o.splitlines() if line.endswith(' _trm_init'));cols=symbol.split();start=int(cols[0],16);size=int(cols[1],16)
    last=[int(line.split(',')[1],16) for line in trace.read_text().splitlines()[-64:]];assert all(start<=pc<start+size for pc in last),(symbol,last[:8])
    if halt is None:assert min(last)>=start+max(0,size-64)
    o,e,r=run('E6/dummy_original/halt_disassembly',['riscv64-linux-gnu-objdump','-d','-Mno-aliases','--start-address='+hex(start),'--stop-address='+hex(start+size),elf],inputs=[elf]);assert 'jalr' in o and 'ebreak' not in o
    dump(ROOT/'reports/E6_original_dummy.json',{'status':'PASS_BOUNDED_OBSERVATION','image':str(image),'sha256':sha(image),'elf':str(elf),'containing_symbol':symbol,'halt_inlined':halt is None,'last_pc_values':sorted(set(last)),'result':json.loads(report.read_text()),'runtime_binary':str(exe),'scope':'Original AM halt loop observed forrequested20000 commits; compiler may inline it into _trm_init; not falsely reported as a terminating program.'})
    mark(['E6-M002'],'PASS',['reports/E6_original_dummy.json','artifacts/E6/dummy_original'],'Real cross compilation and NPC image load at0x80000000; originalAM code reaches and remains in the halt symbol range,128MiB model and bounded observation explicit.')
    print('E6_ORIGINAL_DUMMY_PASS',flush=True)
if __name__=='__main__':main()

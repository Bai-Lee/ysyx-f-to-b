from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    am=BENCH/'abstract-machine';root=ROOT/'D/D5/toolchain';gnu=root/'gnu';gnu.mkdir(parents=True,exist_ok=True)
    (gnu/'stubs-ilp32.h').write_text('/* Task-local freestanding RV32 ABI overlay. No hosted glibc ILP32 implementation is supplied or linked. */\n')
    p=am/'scripts/isa/riscv.mk';text=p.read_text();line='\n# D-stage bare-metal compilation; system toolchain headers remain unchanged.\nCFLAGS += -ffreestanding -I'+str(root)+'\n'
    if str(root) not in text:p.write_text(text+line)
    probe=root/'probe.c';probe.write_text('#include <stdint.h>\n#include <limits.h>\n_Static_assert(sizeof(uint32_t)==4,"uint32");\n_Static_assert(sizeof(void*)==4,"RV32 pointers");\n_Static_assert(__STDC_HOSTED__==0,"freestanding");\nint f(void){return CHAR_BIT;}\n')
    obj=WORK/'D5/header_probe.o';run('D5/headers/probe',['riscv64-linux-gnu-gcc','-march=rv32im','-mabi=ilp32','-ffreestanding','-I'+str(root),'-Wall','-Werror','-c',probe,'-o',obj],inputs=[probe,gnu/'stubs-ilp32.h'],outputs=[obj])
    o,_,_=run('D5/headers/elf',['riscv64-linux-gnu-readelf','-h',obj],inputs=[obj]);assert 'ELF32' in o and 'RISC-V' in o
    dest=ROOT/'D/D5/runtime_patch/abstract-machine/scripts/isa/riscv.mk';dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
    dump(ROOT/'reports/D5_headers.json',{'status':'PASS_FREESTANDING_ONLY','overlay':str(gnu/'stubs-ilp32.h'),'sha256':sha(gnu/'stubs-ilp32.h'),'flags':['-ffreestanding','-march=rv32im','-mabi=ilp32'],'system_headers_changed':False,'not_provided':'Hosted 32-bit RISC-V glibc ABI; these images are statically linked against AM/owned klib with the bare-metal linker.'})

if __name__=='__main__':main()

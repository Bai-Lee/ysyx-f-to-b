from pathlib import Path
import sys,re,struct
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    d=ROOT/'D/D8';out=d/'results';npc=BENCH/'npc';am=BENCH/'abstract-machine';lock=json.loads((ROOT/'reports/D8_build.json').read_text());exe=Path(lock['executable']);ref=Path(lock['reference'])
    devices=WORK/'build/d8-device-tests'
    run('D8/devices/build',['g++','-std=c++17','-g','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-fno-pie','-no-pie',d/'device_tests.cpp','-o',devices],inputs=[d/'device_tests.cpp',d/'memory.hpp'],outputs=[devices])
    o,_,_=run('D8/devices/run',[devices],inputs=[devices],env={'ASAN_OPTIONS':'detect_leaks=1'});assert 'DEVICE_PASS' in o
    ready=int(re.search(r'ready=(\d+)',o)[1])
    tests=BENCH/'am-kernels/tests/klib-tests';report=tests/'build/klib-tests-riscv32e-npc.bin.npc.json';elf=tests/'build/klib-tests-riscv32e-npc.elf'
    o,e,_=run('D8/klib/portable',['make','-j1','ARCH=riscv32e-npc','run','NPC_ARGS=--uart-random'],cwd=tests,inputs=[tests/'Makefile',tests/'main.c',exe,ref,*[am/'klib/src'/x for x in ['string.c','stdio.c','alloc.c','stdlib.c']]],outputs=[report,elf],timeout=180)
    r=json.loads(report.read_text());assert 'KLIB_PORTABLE_PASS' in o and r['result']=='GOOD_TRAP' and r['diff_checked']+r['device_sync_checked']==r['instructions']
    source=out/'signedness.c';source.write_text('typedef signed int i32;typedef unsigned int u32;\ni32 signed_add(i32 a,i32 b){return a+b;}\nu32 unsigned_add(u32 a,u32 b){return a+b;}\ni32 signed_less(i32 a,i32 b){return a<b;}\ni32 unsigned_less(u32 a,u32 b){return a<b;}\n')
    obj=out/'signedness.o';run('D8/signedness/compile',['riscv64-linux-gnu-gcc','-O2','-march=rv32e','-mabi=ilp32e','-c',source,'-o',obj],inputs=[source],outputs=[obj])
    o,_,_=run('D8/signedness/disassembly',['riscv64-linux-gnu-objdump','-d','-M','no-aliases',obj],inputs=[obj])
    blocks={m[1]:m[2] for m in re.finditer(r'<(\w+)>:\n(.*?)(?=\n[0-9a-f]+ <|\Z)',o,re.S)}
    words=lambda text:re.findall(r'^\s*[0-9a-f]+:\s+([0-9a-f]{8})',text,re.M)
    assert words(blocks['signed_add'])==words(blocks['unsigned_add']) and 'slt\t' in blocks['signed_less'] and 'sltu\t' in blocks['unsigned_less']
    (out/'signedness.txt').write_text(o)
    dump(ROOT/'reports/D8_extra.json',{'status':'PASS','uart_ready':ready,'uart_polls':100000,'sanitizers':'ASAN+UBSAN on device model','portable_klib':r,'signed_add_equals_unsigned_add_encoding':True,'signed_comparison_distinct':True,'scope':'Model time/byte-lane/resource boundaries, same 5007-case klib suite rebuilt for RV32E, and actual compiler signedness experiment.'})

if __name__=='__main__':main()

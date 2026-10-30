from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    subprocess.run(['python3',str(ROOT/'C/C5/prepare_am.py')],check=True)
    base=WORK/'c5/workbench';am=base/'abstract-machine';app=base/'lshr-test';app.mkdir(exist_ok=True)
    values=[0,1,0x80000000,0xffffffff,0x8000000000000000,0xffffffffffffffff,0x0123456789abcdef,0xdeadbeef10203040]
    rows=[]
    for value in values:
        expected=[value>>i for i in range(64)]
        rows.append('{0x%08xu,0x%08xu,{'%(value&0xffffffff,value>>32)+','.join('0x%08xu'%(v&0xffffffff) for v in expected)+'},{'+','.join('0x%08xu'%(v>>32) for v in expected)+'}}')
    (app/'vectors.h').write_text('static const struct {uint32_t lo,hi,expected_lo[64],expected_hi[64];} cases[]={'+','.join(rows)+'};\n')
    (app/'main.c').write_text('''#include <am.h>
#include <stdint.h>
#include "vectors.h"
extern uint64_t __lshrdi3(uint64_t,int);
int main(const char *args){
 (void)args;
 for(unsigned n=0;n<8;n++)for(unsigned shift=0;shift<64;shift++){
  union {uint64_t full;struct {uint32_t lo,hi;} half;} input,output;
  input.half.lo=cases[n].lo;input.half.hi=cases[n].hi;
  output.full=__lshrdi3(input.full,shift);
  if(output.half.lo!=cases[n].expected_lo[shift]||output.half.hi!=cases[n].expected_hi[shift])halt(61);
 }
 return 0;
}
''')
    (app/'bad.S').write_text('.section .text.__lshrdi3,"ax",@progbits\n.globl __lshrdi3\n__lshrdi3:\n  ret\n')
    build=next(r for r in json.loads((ROOT/'reports/C5_soc_build.json').read_text())['variants'] if r['reset_pc']==0x30000000 and r.get('cycle_sim',False) and not r.get('fast_flash',False) and not r.get('mutant',False) and not r.get('psram_qpi',False) and r.get('psram_bytes',4096)==4096)
    exe=Path(build['executable']);ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so';accepted=[]
    for name,bad in [('good',False),('unchanged-value-mutant',True)]:
        make=app/('Makefile.'+name);make.write_text('NAME = lshr-'+name+'\nSRCS = main.c'+(' bad.S' if bad else '')+'\ninclude $(AM_HOME)/Makefile\n')
        image=app/'build'/('lshr-'+name+'-riscv32e-ysyxsoc-flash.bin');elf=image.with_suffix('.elf');tag='C5/lshr/'+name
        run(tag+'/build',['make','-j1','-f',make,'ARCH=riscv32e-ysyxsoc-flash','insert-arg'],cwd=app,env={'AM_HOME':str(am),'NPC_HOME':str(base/'npc')},inputs=[make,app/'main.c',app/'vectors.h',*([app/'bad.S'] if bad else []),ROOT/'C/C5/am/lshrdi3.S'],outputs=[image,elf],timeout=180)
        result=ROOT/'artifacts'/tag/'simulation.json'
        run(tag+'/run',[exe,'--flash',image,'--ref',ref,'--report',result,'--max-cycles','20000000'],inputs=[exe,image,elf,ref],outputs=[result],expected=(1 if bad else 0,),timeout=180)
        data=json.loads(result.read_text());assert data['result']==('BAD_TRAP' if bad else 'GOOD_TRAP') and data['a0']==(61 if bad else 0)
        accepted.append({'name':name,'status':'PASS','simulation':data,'evidence':'artifacts/'+tag})
    dump(ROOT/'reports/C5_lshr.json',{'status':'PASS_512_PYTHON_GOLDENS_AND_WRONG_HELPER','runs':accepted,'values':[hex(v) for v in values],
         'scope':'Actual RV32E ABI helper,8 independent Python-generated64-bit values over every shift0..63. No recursive C right-shift implementation; unchanged-value helper is rejected. Needed by -Os generated calls in the existing64-bit division code.'})
    print('C5_LOGICAL_SHIFT64_HELPER_PASS',flush=True)


if __name__=='__main__':main()

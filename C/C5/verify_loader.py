from pathlib import Path
import sys,argparse,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from support import select_build


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--build-only',action='store_true');parser.add_argument('--variant',default='30000000-cycle-psram4m-qpi');args=parser.parse_args()
    subprocess.run(['python3',str(ROOT/'C/C5/prepare_am.py')],check=True)
    base=WORK/'c5/workbench';am=base/'abstract-machine';rows=[]
    payload='''#include <am.h>
#include <stdint.h>
#include <klib.h>
static const uint32_t table[2048]={TABLE};
static uint32_t initialized[4]={0x78563412,0x13579bdf,0x2468ace0,0xffffffff};
static uint32_t zeroed[256];
int main(const char *args){
 (void)args;volatile const uint32_t *p=table;
 for(unsigned i=0;i<2048;i++)if(p[i]!=(0x13579bdfu^(i*0x10203u)))halt(73);
 if(initialized[0]!=0x78563412u||initialized[3]!=0xffffffffu)halt(74);
 for(unsigned i=0;i<256;i++){if(zeroed[i])halt(75);zeroed[i]=i;}
 initialized[1]^=initialized[2];
 if(initialized[1]!=0x373f373fu)halt(76);
 printf("C5_LOADER_PAYLOAD_PASS words=2048 bss=256\\n");return 0;
}
'''.replace('TABLE',','.join(hex(0x13579bdf^(i*0x10203))+'u' for i in range(2048)))
    for name,profile in [('single','psram'),('two-stage','psram-ssbl'),('missing-ssbl','psram-ssbl')]:
        app=base/('loader-'+name);app.mkdir(exist_ok=True);(app/'main.c').write_text(payload)
        source='main.c'
        if name=='missing-ssbl':
            text=(ROOT/'C/C5/am/start.S').read_text();assert 'sw a0,0(t1)' in text
            (app/'bad-start.S').write_text(text.replace('sw a0,0(t1)','nop # fault injection: omit SSBL copy',1));source+=' bad-start.S'
        (app/'Makefile').write_text('NAME = loader-'+name+'\nSRCS = '+source+'\ninclude $(AM_HOME)/Makefile\n')
        arch='riscv32e-ysyxsoc-'+profile;image=app/'build'/('loader-'+name+'-'+arch+'.bin');elf=image.with_suffix('.elf');tag='C5/loader/'+name
        inputs=[app/'main.c',app/'Makefile',*sorted(app.glob('*.S')),*sorted((am/'am/src/riscv/ysyxsoc').glob('*')),am/'scripts/ysyxsoc-code-psram.ld']
        run(tag+'/build',['make','-j1','ARCH='+arch,'insert-arg'],cwd=app,env={'AM_HOME':str(am)},inputs=inputs,outputs=[image,elf],timeout=180)
        text,_,_=run(tag+'/symbols',['riscv64-linux-gnu-nm','-n',elf],inputs=[elf]);symbols={v[2]:int(v[0],16) for line in text.splitlines() if len(v:=line.split())==3 and re.fullmatch('[0-9a-fA-F]+',v[0])}
        assert symbols['_start']==0x30000000 and symbols['main']>=0x80000000
        if name!='single':assert symbols['__ssbl_start']==0x0f000000 and 0<symbols['__ssbl_end']-symbols['__ssbl_start']<=2048
        if args.build_only:continue
        exe=Path(select_build(args.variant)['executable']);ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
        directory=ROOT/'artifacts'/tag;result=directory/'simulation.json';budget=directory/'resources.json'
        run(tag+'/run',['python3',ROOT/'C/runtime/budget_exec.py','--report',budget,'--',exe,'--flash',image,'--ref',ref,'--report',result,'--max-cycles','100000000'],inputs=[exe,ref,image,elf],outputs=[result,budget],expected=(3 if name=='missing-ssbl' else 0,),timeout=180)
        data=json.loads(result.read_text());uart=bytes.fromhex(data['uart']['hex']).decode('ascii')
        assert data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
        if name=='missing-ssbl':assert data['result']=='NPC_FAULT' and data['pc']==symbols['__ssbl_start']
        else:
            assert data['result']=='GOOD_TRAP' and 'C5_LOADER_PAYLOAD_PASS words=2048 bss=256' in uart
            assert data['retired_by_region'][2]>0 and data['retired_by_region'][3]>0
            assert (data['retired_by_region'][1]>0)==(name=='two-stage')
        rows.append({'name':name,'status':'PASS','result':data['result'],'cycles':data['cycles'],'instructions':data['instructions'],'wall_seconds':data['wall_seconds'],'retired_by_region':data['retired_by_region'],'uart':uart,'symbols':symbols,'image_sha256':sha(image),'elf_sha256':sha(elf),'evidence':'artifacts/'+tag})
    if not args.build_only:
        assert rows[1]['cycles']<rows[0]['cycles']
        dump(ROOT/'reports/C5_loader.json',{'status':'PASS_FSBL_SSBL_PSRAM_AND_NEGATIVE','runs':rows,'cycle_ratio_two_over_single':rows[1]['cycles']/rows[0]['cycles'],'scope':'FSBL executes inFlash and copies SSBL toSRAM; SSBL actually retires inSRAM and copies text/rodata/data plus zeroesBSS inPSRAM, then main executes inPSRAM. Same2048word independent expected table and initialized/BSS checks in both profiles. Omitting only SSBL copy traps at its actual SRAM entry. Every non-MMIO instruction checked by NEMU.'})
        mark(['C5-M030'],'PASS',['reports/C5_loader.json'],'Real FlashFSBL toSRAMSSBL toPSRAM execution, complete data/rodata/BSS initialization, faster measured loading, and missing-SSBL copy negative.')
    print('C5_LOADER_BUILT' if args.build_only else 'C5_LOADER_PASS',flush=True)


if __name__=='__main__':main()

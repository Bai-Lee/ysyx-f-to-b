from pathlib import Path
import sys,argparse,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from support import select_build


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['data','code'],default='data');parser.add_argument('--build-only',action='store_true');parser.add_argument('--variant',default='30000000-cycle-psram4m-qpi');args=parser.parse_args()
    subprocess.run(['python3',str(ROOT/'C/C5/prepare_am.py')],check=True)
    base=WORK/'c5/workbench';am=base/'abstract-machine';app=base/'microbench';ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
    build=select_build(args.variant);exe=Path(build['executable'])
    arch='riscv32e-ysyxsoc-'+('flash-psram' if args.stage=='data' else 'psram');image=app/'build'/('microbench-'+arch+'.bin');elf=image.with_suffix('.elf')
    source=[p for p in sorted(app.rglob('*')) if p.is_file() and 'build' not in p.relative_to(app).parts and '.git' not in p.relative_to(app).parts]
    source += [*sorted((am/'am/src/riscv/ysyxsoc').glob('*')),am/'scripts/platform/ysyxsoc.mk',am/'scripts'/('ysyxsoc-psram-data.ld' if args.stage=='data' else 'ysyxsoc-code-psram.ld')]
    tag='C5/psram-apps/'+args.stage
    run(tag+'/build',['make','-j1','ARCH='+arch,'mainargs=test','insert-arg'],cwd=app,env={'AM_HOME':str(am),'NPC_HOME':str(base/'npc')},inputs=source,outputs=[image,elf],timeout=300)
    nm=Path(shutil.which('riscv64-linux-gnu-nm'));text,_,_=run(tag+'/symbols',[nm,'-n',elf],inputs=[nm,elf])
    symbols={v[2]:int(v[0],16) for line in text.splitlines() if len(v:=line.split())==3 and re.fullmatch('[0-9a-fA-F]+',v[0])}
    assert symbols['_start']==0x30000000 and symbols['_stack_pointer']==0x0f002000 and symbols['_heap_end']==0x80400000
    assert 0x80000000<=symbols['_heap_start']<symbols['_heap_end']
    assert (0x30000000<=symbols['main']<0x31000000) if args.stage=='data' else (0x80000000<=symbols['main']<0x80400000)
    if args.build_only:print('C5_PSRAM_APPS_BUILD_ONLY',args.stage,flush=True);return
    out=ROOT/'artifacts'/tag;result=out/'simulation.json';resources=out/'resources.json'
    run(tag+'/run',['python3',ROOT/'C/runtime/budget_exec.py','--report',resources,'--',exe,'--flash',image,'--ref',ref,'--report',result,'--max-cycles','3000000000'],inputs=[exe,image,elf,ref],outputs=[result,resources],timeout=1800)
    data=json.loads(result.read_text());uart=bytes.fromhex(data['uart']['hex']).decode('ascii')
    assert data['result']=='GOOD_TRAP' and data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
    assert uart.count(' Passed.')==10 and 'Ignored' not in uart and 'Failed.' not in uart and 'MicroBench PASS' in uart
    assert data['mrom_dpi_calls']==0 and data['psram']['qpi_entries']==1 and data['psram']['maximum_byte_address']>4095
    assert data['psram']['commands_spi_read_write_qpi_read_write'][:2]==[0,0]
    if args.stage=='code':assert data['retired_by_region'][3]>1000 and data['retired_by_region'][2]>0
    else:assert data['retired_by_region'][3]==0 and data['retired_by_region'][2]==data['instructions']
    p=ROOT/'reports/C5_psram_apps.json';rows=json.loads(p.read_text()).get('runs',[]) if p.exists() else []
    row={'stage':args.stage,'status':'PASS_ALL10_ORIGINAL_TESTS','simulation':data,'symbols':symbols,'uart':uart,'image_sha256':sha(image),'elf_sha256':sha(elf),'evidence':'artifacts/'+tag}
    rows=[r for r in rows if r['stage']!=args.stage]+[row]
    dump(p,{'status':'PASS_COMPLETED_PROFILES','runs':rows,'scope':'Original microbench test settings and validators; all10 execute.4MiB PSRAM holds data/heap. Code profile additionally relocates text/rodata and actually retires instructions from PSRAM after Flash bootstrap; stack remains SRAM.'})
    if args.stage=='data':mark(['C5-M026'],'PASS',['reports/C5_psram_apps.json'],'All10 original microbench test cases run on full-capacity PSRAM data/heap; no insufficient-memory exclusions.')
    else:
        baseline=next(r for r in rows if r['stage']=='data');assert data['cycles']<baseline['simulation']['cycles']
        mark(['C5-M028'],'PASS',['reports/C5_psram_apps.json'],'Flash bootloader copies MicroBench text/rodata/data intoPSRAM, SRAM stack retained. All10 test cases pass; measured fewer cycles than Flash-XIP execution.')
    print('C5_PSRAM_MICROBENCH_ALL10_PASS',args.stage,flush=True)


if __name__=='__main__':main()

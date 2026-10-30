from pathlib import Path
import sys,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    subprocess.run(['python3',str(ROOT/'C/C5/prepare_am.py')],check=True)
    base=WORK/'c5/workbench';am=base/'abstract-machine';origin=WORK/'c2-nemu-apps/am-kernels/benchmarks'
    ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
    build=next(r for r in json.loads((ROOT/'reports/C5_soc_build.json').read_text())['variants'] if r['reset_pc']==0x30000000 and r.get('cycle_sim',False) and not r.get('fast_flash',False) and not r.get('mutant',False) and not r.get('psram_qpi',False) and r.get('psram_bytes',4096)==4096)
    exe=Path(build['executable']);assert sha(exe)==build['sha256'];env={'AM_HOME':str(am),'NPC_HOME':str(base/'npc')};rows=[]
    for name in ['coremark','microbench']:
        app=base/name
        if not app.exists():shutil.copytree(origin/name,app,ignore=shutil.ignore_patterns('build','.git'))
    port=base/'coremark/include/core_portme.h';original=(origin/'coremark/include/core_portme.h').read_text()
    adapted=original.replace('#define ITERATIONS 1000','#ifndef ITERATIONS\n#define ITERATIONS 1000\n#endif')
    assert adapted!=original
    port.write_text(adapted)
    coremake=base/'coremark/Makefile';coremake.write_text('NAME = coremark\nSRCS = $(shell find src/ -name "*.c")\nCFLAGS += -DITERATIONS=1\ninclude $(AM_HOME)/Makefile\n')
    plans=[('hello','',False),('coremark','',True),('microbench','test',True)]
    for name,args,large in plans:
        app=base/name;image=app/'build'/(name+'-riscv32e-ysyxsoc-flash.bin');elf=image.with_suffix('.elf');tag='C5/flash-boot/'+name
        sources=[p for p in sorted(app.rglob('*')) if p.is_file() and 'build' not in p.relative_to(app).parts and '.git' not in p.relative_to(app).parts]
        sources += [*sorted((am/'am/src/riscv/ysyxsoc').glob('*')),am/'scripts/ysyxsoc-flash.ld',am/'scripts/platform/ysyxsoc.mk']
        run(tag+'/build',['make','-j1','ARCH=riscv32e-ysyxsoc-flash','mainargs='+args,'insert-arg'],cwd=app,env=env,inputs=sources,outputs=[image,elf],timeout=300)
        assert image.stat().st_size<16*1024*1024
        if large:assert image.stat().st_size>4096
        out=ROOT/'artifacts'/tag;out.mkdir(parents=True,exist_ok=True);result=out/'simulation.json'
        stdout,stderr,record=run(tag+'/run',[exe,'--flash',image,'--ref',ref,'--report',result,'--max-cycles','2000000000'],inputs=[exe,image,elf,ref],outputs=[result],timeout=1800)
        data=json.loads(result.read_text());assert data['result']=='GOOD_TRAP' and data['diff_enabled'] and data['diff_checked']+data['device_sync_checked']==data['instructions']
        assert data['mrom_dpi_calls']==0 and data['retired_by_region'][2]==data['instructions'] and data['flash_dpi_calls']>=data['instructions']
        assert data['spi']['transfers']==data['flash_dpi_calls'] and data['spi']['incomplete_bits']==0
        uart=bytes.fromhex(data['uart']['hex']).decode('ascii');assert data['uart']['dropped']==0
        details={}
        if name=='hello':assert uart=="Hello, AbstractMachine!\nmainargs = ''.\n"
        elif name=='coremark':
            assert 'Running CoreMark for 1 iterations' in uart and 'CoreMark PASS' in uart
            details={'iterations':1,'certified_score':False,'reason':'C5 course explicitly suggests reducing CoreMark run length for slow Flash execution; original checksum validation retained.'}
        else:
            passed=[m.group(1) for m in re.finditer(r'\[([^]]+)\][^\n]*Passed\.',uart)]
            skipped=[m.group(1) for m in re.finditer(r'\[([^]]+)\][^\n]*Ignored \(insufficient memory\)',uart)]
            assert len(passed)==7 and set(skipped)=={'bf','dinic','lzip'} and 'MicroBench PASS' in uart and 'Failed.' not in uart
            details={'passed':passed,'insufficient_heap':skipped,'scope':'SRAM heap is too small for these three original test settings; not counted as executing all10 tests.'}
        rows.append({'name':name,'status':'PASS_WITH_DECLARED_SCOPE','binary_bytes':image.stat().st_size,'simulation':data,
                     'image_sha256':sha(image),'elf_sha256':sha(elf),'uart':uart,'details':details,'evidence':'artifacts/'+tag,'wall_seconds_with_launch':record['elapsed_seconds']})
        dump(ROOT/'reports/C5_flash_boot.json',{'status':'IN_PROGRESS','runs':rows})
    dump(ROOT/'reports/C5_flash_boot.json',{'status':'PASS_FLASH_RESET_AND_LARGER_PROGRAMS','runs':rows,
         'coremark_adaptation':{'original_header_sha256':sha(origin/'coremark/include/core_portme.h'),'C5_header_sha256':sha(port),'change':'Make original ITERATIONS macro overridable; C5-only functional run selects1 iteration. No algorithm or CRC checks removed.'},
         'scope':'Reset PC0x30000000; actual real-SPI XIP instruction fetches, zero MROM reads, Flash image/data LMA and SRAM data/BSS/stack. Hello, larger printf/CoreMark and MicroBench programs execute. CoreMark not a certified performance score; three MicroBench heap exclusions explicitly retained until PSRAM stage.'})
    mark(['C5-M022'],'PASS',['reports/C5_flash_boot.json'],'Real Flash reset/XIP boot, original hello, larger printf/CoreMark and MicroBench with explicit SRAM heap exclusions.')
    print('C5_FLASH_BOOT_LARGE_PROGRAMS_PASS',flush=True)


if __name__=='__main__':main()

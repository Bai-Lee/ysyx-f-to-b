from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *


def main():
    subprocess.run(['python3',str(ROOT/'C/C5/prepare_am.py')],check=True)
    base=WORK/'c5/workbench';am=base/'abstract-machine';cpu=base/'cpu-tests'
    build=next(r for r in json.loads((ROOT/'reports/C5_soc_build.json').read_text())['variants'] if r['reset_pc']==0x20000000 and not r.get('mutant',False) and not r.get('psram_qpi',False) and r.get('psram_bytes',4096)==4096 and not r.get('fast_flash',False) and not r.get('cycle_sim',False))
    exe=Path(build['executable']);assert sha(exe)==build['sha256'];ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
    cases=sorted((cpu/'tests').glob('*.c'))
    original=json.loads((ROOT/'reports/D8_official_tests.json').read_text())['programs']
    expected_names={r['name'] for r in original if r['suite']=='cpu'}
    assert len(expected_names)==35 and {p.stem for p in cases}==expected_names|{'wrong'}
    rows=[];env={'AM_HOME':str(am),'NPC_HOME':str(base/'npc')}
    runtime=[*sorted((am/'am/src/riscv/ysyxsoc').glob('*')),am/'scripts/ysyxsoc-mrom.ld',am/'scripts/platform/ysyxsoc.mk']
    for source in cases:
        name=source.stem
        if name=='hello-str':continue
        manifest=cpu/('C5-Makefile.'+name);manifest.write_text('NAME = '+name+'\nSRCS = tests/'+source.name+'\ninclude $(AM_HOME)/Makefile\n')
        image=cpu/'build'/(name+'-riscv32e-ysyxsoc.bin');elf=image.with_suffix('.elf');tag='C5/cpu-tests/'+name
        run(tag+'/build',['make','-j1','-f',manifest,'ARCH=riscv32e-ysyxsoc','insert-arg'],cwd=cpu,env=env,inputs=[source,manifest,*runtime],outputs=[image,elf],timeout=180,resume=True)
        assert image.stat().st_size<=4096
        out=ROOT/'artifacts'/tag;out.mkdir(parents=True,exist_ok=True);report=out/'simulation.json'
        expected=1 if name=='wrong' else 0
        stdout,stderr,record=run(tag+'/run',[exe,'--mrom',image,'--ref',ref,'--report',report,'--max-cycles','50000000'],inputs=[exe,image,elf,ref],outputs=[report],timeout=180,resume=True,expected=(expected,))
        simulation=json.loads(report.read_text());assert simulation['result']==('BAD_TRAP' if expected else 'GOOD_TRAP') and simulation['diff_enabled'] and simulation['diff_checked']+simulation['device_sync_checked']==simulation['instructions']
        rows.append({'name':name,'status':'PASS_REJECTED' if expected else 'PASS','source_sha256':sha(source),'image_sha256':sha(image),'elf_sha256':sha(elf),'simulation':simulation,'evidence':'artifacts/'+tag})
        dump(ROOT/'reports/C5_cpu_tests.json',{'status':'IN_PROGRESS','runs':rows})
    assert len(rows)==35 and sum(r['name']!='wrong' for r in rows)==34
    dump(ROOT/'reports/C5_cpu_tests.json',{'status':'PASS_34_ORIGINAL_CPU_TESTS','runs':rows,
         'scope':'All34 original positive cpu-tests required at this stage plus the original wrong.c negative; hello-str is explicitly deferred at this MROM/SRAM stage. Original checks retained; new AM bootloader uses real SRAM data/BSS/stack and MROM code. Each non-MMIO instruction checked by NEMU, MMIO effects independently validated and synchronized.'})
    mark(['C5-M010'],'PASS',['reports/C5_cpu_tests.json','reports/C5_ram.json'],'Data LMA/VMA, poisoned .data/.bss omission controls and all34 required original CPU programs passed on actual MROM/SRAM SoC.')
    print('C5_ALL_34_MROM_SRAM_CPU_TESTS_PASS',flush=True)


if __name__=='__main__':main()

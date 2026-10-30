"""Final complete-SoC CPU regression, preserving the original sources/checks."""
from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
from support import select_build


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--build-only',action='store_true');args=parser.parse_args()
    base=WORK/'c5/workbench';am=base/'abstract-machine';cpu=base/'cpu-tests';arch='riscv32e-ysyxsoc-sdram32'
    variant='30000000-cycle-psram4m-qpi-sdram32x2-opt';exe=Path(select_build(variant)['executable']);ref=WORK/'c5/nemu-ref/build/riscv32-nemu-interpreter-so'
    cases=sorted((cpu/'tests').glob('*.c'));original=json.loads((ROOT/'reports/D8_official_tests.json').read_text())['programs'];names={r['name'] for r in original if r['suite']=='cpu'}
    assert len(names)==35 and {p.stem for p in cases}==names|{'wrong'};rows=[]
    for source in cases:
        name=source.stem;makefile=cpu/('C5-final-Makefile.'+name);makefile.write_text('NAME = '+name+'\nSRCS = tests/'+source.name+'\ninclude $(AM_HOME)/Makefile\n')
        image=cpu/'build'/(name+'-'+arch+'.bin');elf=image.with_suffix('.elf');tag='C5/final-cpu/'+name
        run(tag+'/build',['make','-j1','-f',makefile,'ARCH='+arch,'insert-arg'],cwd=cpu,env={'AM_HOME':str(am)},inputs=[source,makefile,*sorted((am/'am/src/riscv/ysyxsoc').glob('*')),am/'scripts/ysyxsoc-code-sdram32.ld'],outputs=[image,elf],timeout=180,resume=True)
        if args.build_only:continue
        folder=ROOT/'artifacts'/tag;report=folder/'simulation.json';budget=folder/'resources.json';bad=name=='wrong'
        run(tag+'/run',['python3',ROOT/'C/runtime/budget_exec.py','--report',budget,'--',exe,'--flash',image,'--ref',ref,'--report',report,'--max-cycles','100000000'],inputs=[exe,ref,image,elf],outputs=[report,budget],expected=(1 if bad else 0,),timeout=180,resume=True)
        data=json.loads(report.read_text());assert data['result']==('BAD_TRAP' if bad else 'GOOD_TRAP') and data['diff_enabled']
        assert data['diff_checked']+data['device_sync_checked']==data['instructions'] and data['retired_by_region'][4]>0
        rows.append({'name':name,'status':'PASS_REJECTED' if bad else 'PASS','source_sha256':sha(source),'image_sha256':sha(image),'elf_sha256':sha(elf),'cycles':data['cycles'],'instructions':data['instructions'],'result':data['result'],'evidence':'artifacts/'+tag})
        dump(ROOT/'reports/C5_final_cpu.json',{'status':'IN_PROGRESS','variant':variant,'runs':rows})
    if not args.build_only:
        assert len(rows)==36 and sum(r['status']=='PASS' for r in rows)==35
        dump(ROOT/'reports/C5_final_cpu.json',{'status':'PASS_35_ORIGINAL_POSITIVES_AND_WRONG_REJECTED','variant':variant,'executable_sha256':sha(exe),'reference_sha256':sha(ref),'runs':rows,'scope':'FinalcompleteSoC with32-bit/two-rankSDRAM andimplementedperipherals,35unchangedoriginalpositiveCPUtests includinghello-str pluswrong.c negative. RealFlashFSBL/SRAMSSBL/SDRAMcode andfull non-MMIO NEMU comparison. Complements the preserved34test MROM-stage acceptance; not anall-RISC-V-compliance proof.'})
    print('C5_FINAL_CPU_BUILT' if args.build_only else 'C5_FINAL_35_CPU_TESTS_PASS',flush=True)


if __name__=='__main__':main()

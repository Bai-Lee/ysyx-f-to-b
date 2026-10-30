"""Final complete-SoC CPU regression, preserving the original sources/checks."""
from pathlib import Path
import sys,argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'soc'))
from common import *
from support import select_build


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--build-only',action='store_true');args=parser.parse_args()
    base=WORK/'soc/workbench';am=base/'abstract-machine';cpu=base/'cpu-tests';arch='riscv32e-ysyxsoc-sdram128-p325'
    if not cpu.exists():
        origin=Path('/home/USER/c-stage/c5/workbench/cpu-tests');assert origin.is_dir();copied=[]
        for source in sorted(origin.rglob('*')):
            relative=source.relative_to(origin)
            if not source.is_file() or any(part in ['build','.git','__pycache__'] for part in relative.parts) or source.name.startswith('C5-'):continue
            target=cpu/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target);assert sha(source)==sha(target)
            copied.append({'source':str(source),'target':str(target),'sha256':sha(target)})
        dump(ROOT/'reports/B_cpu_source_copy.json',{'status':'PASS_SOURCE_COPY_ONLY','files':copied,'scope':'Necessary unchanged original CPU test sources copied from the accepted C workbench; no old source or binary moved or overwritten. Individual test hashes are checked against C5_final_cpu before execution.'})
    variant='b5-release';exe=Path(select_build(variant)['executable']);ref=WORK/'nemu-ref/build/riscv32-nemu-interpreter-so'
    cases=sorted((cpu/'tests').glob('*.c'));original=json.loads((ROOT/'reports/D8_official_tests.json').read_text())['programs'];names={r['name'] for r in original if r['suite']=='cpu'}
    assert len(names)==35 and {p.stem for p in cases}==names|{'wrong'};rows=[]
    for source in cases:
        name=source.stem
        baseline=next(r for r in json.loads((ROOT/'reports/C5_final_cpu.json').read_text())['runs'] if r['name']==name)
        assert sha(source)==baseline['source_sha256'],'Original CPU fixture changed: '+name
        makefile=cpu/('B-final-Makefile.'+name);makefile.write_text('NAME = '+name+'\nSRCS = tests/'+source.name+'\ninclude $(AM_HOME)/Makefile\n')
        image=cpu/'build'/(name+'-'+arch+'.bin');elf=image.with_suffix('.elf');tag='B4/final-cpu/'+name
        run(tag+'/build',['make','-j4','-f',makefile,'ARCH='+arch,'insert-arg'],cwd=cpu,env={'AM_HOME':str(am)},inputs=[source,makefile,*sorted((am/'am/src/riscv/ysyxsoc').glob('*')),am/'scripts/ysyxsoc-code-sdram128.ld'],outputs=[image,elf],timeout=180,resume=True)
        if args.build_only:continue
        folder=ROOT/'artifacts'/tag;report=folder/'simulation.json';budget=folder/'resources.json';bad=name=='wrong'
        run(tag+'/run',['python3',ROOT/'B/runtime/budget_exec.py','--kind','simulation','--report',budget,'--',exe,'--flash',image,'--ref',ref,'--report',report,'--max-cycles','100000000'],inputs=[exe,ref,image,elf],outputs=[report,budget],expected=(1 if bad else 0,),timeout=180,resume=True)
        data=json.loads(report.read_text());assert data['result']==('BAD_TRAP' if bad else 'GOOD_TRAP') and data['diff_enabled']
        assert data['diff_checked']+data['device_sync_checked']==data['instructions'] and data['retired_by_region'][4]>0
        rows.append({'name':name,'status':'PASS_REJECTED' if bad else 'PASS','source_sha256':sha(source),'image_sha256':sha(image),'elf_sha256':sha(elf),'cycles':data['cycles'],'instructions':data['instructions'],'result':data['result'],'evidence':'artifacts/'+tag})
        dump(ROOT/'reports/B4_final_cpu.json',{'status':'IN_PROGRESS','variant':variant,'runs':rows})
    if not args.build_only:
        assert len(rows)==36 and sum(r['status']=='PASS' for r in rows)==35
        dump(ROOT/'reports/B4_final_cpu.json',{'status':'PASS_35_ORIGINAL_POSITIVES_AND_WRONG_REJECTED','variant':variant,'executable_sha256':sha(exe),'reference_sha256':sha(ref),'runs':rows,'scope':'FinalcompleteSoC with32-bit/two-rankSDRAM andimplementedperipherals,35unchangedoriginalpositiveCPUtests includinghello-str pluswrong.c negative. RealFlashFSBL/SRAMSSBL/SDRAMcode andfull non-MMIO NEMU comparison. Complements the preserved34test MROM-stage acceptance; not anall-RISC-V-compliance proof.'})
    print('B_FINAL_CPU_BUILT' if args.build_only else 'B_FINAL_35_CPU_TESTS_PASS',flush=True)


if __name__=='__main__':main()

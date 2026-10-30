from pathlib import Path
import sys,re,tarfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    lock=json.loads((ROOT/'reports/D8_build.json').read_text());exe=Path(lock['executable']);ref=Path(lock['reference']);am=BENCH/'abstract-machine';rows=[]
    for suite,cwd,archive_name in [('riscv',BENCH/'riscv-tests','NJU-ProjectN__riscv-tests-am__master'),('cpu',BENCH/'am-kernels/tests/cpu-tests','NJU-ProjectN__am-kernels__ics2026')]:
        files=sorted((cwd/('isa/rv32ui' if suite=='riscv' else 'tests')).glob('*.S' if suite=='riscv' else '*.c'))
        files=[p for p in files if p.stem not in ('fence_i','ma_data','wrong')]
        archive=Path('/workspace/downloads/ysyx_e_stage/sources/canonical')/(archive_name+'.tar.gz')
        with tarfile.open(archive) as original:
            for p in files:
                rel=str(p.relative_to(cwd if suite=='riscv' else BENCH/'am-kernels'));assert original.extractfile(rel).read()==p.read_bytes(),p
        for source in files:
            name=source.stem;base=cwd/'build'/(name+'-riscv32e-npc');image=Path(str(base)+'.bin');elf=Path(str(base)+'.elf');report=Path(str(image)+'.npc.json')
            command=['make','-j1','ARCH=riscv32e-npc','ALL='+name,'run']
            if suite=='riscv':command.append('TEST_ISA=i')
            inputs=[source,cwd/'Makefile',am/'Makefile',am/'scripts/riscv32e-npc.mk',am/'scripts/isa/riscv.mk',am/'scripts/platform/npc.mk',am/'klib/build/klib-riscv32e-npc.a',exe,ref]
            o,e,r=run('D8/official/'+suite+'/'+name,command,cwd=cwd,inputs=inputs,outputs=[image,elf,report],timeout=300,resume=True)
            result=json.loads(report.read_text());assert result['result']=='GOOD_TRAP' and result['diff_enabled'] and result['gpr'][0]==0 and result['ebreak_calls']==1 and result['diff_checked']+result['device_sync_checked']==result['instructions'],(name,result)
            assert '***FAIL***' not in o and re.search(r'\[\s*'+re.escape(name)+r'\]\s*\x1b\[1;32mPASS',o)
            a,_,_=run('D8/official/'+suite+'/'+name+'-abi',['riscv64-linux-gnu-readelf','-h','-A',elf],inputs=[elf],resume=True)
            assert 'RVE' in a and 'rv32e' in a and '_m2p' not in a and '_c2p' not in a
            rows.append({'suite':suite,'name':name,'status':'PASS','source_sha256':sha(source),'image_sha256':sha(image),'elf_sha256':sha(elf),'simulation':result,'evidence':'artifacts/D8/official/'+suite+'/'+name,'elapsed_seconds':r['elapsed_seconds']})
            dump(ROOT/'reports/D8_official_tests.json',{'status':'IN_PROGRESS','programs':rows})
    dump(ROOT/'reports/D8_official_tests.json',{'status':'PASS','positive_count':len(rows),'riscv_count':sum(r['suite']=='riscv' for r in rows),'cpu_count':sum(r['suite']=='cpu' for r in rows),'programs':rows,'excluded':['fence_i','ma_data','wrong (separate negative)'],'isa_boundary':'The earlier eight RV32M assembly tests are not RV32E programs. They remain validated under D3 and are not counted as D8 positives; a raw MUL instruction is explicitly rejected. C multiplication/division is recompiled to software helper calls.','source_preservation':'Test bodies byte-identical to locked archives. Rebuilt each with ARCH=riscv32e-npc; RVE ELF flag and ISA attributes checked.','executable_sha256':sha(exe),'reference_sha256':sha(ref)})
    print('D8_OFFICIAL_PASS',len(rows),flush=True)

if __name__=='__main__':main()

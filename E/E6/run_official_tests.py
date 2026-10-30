from pathlib import Path
import sys,tarfile,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    am=BENCH/'abstract-machine'
    archive=ARCHIVE/'assets/offline/ysyx.oscc.cc/slides/resources/archive/klib-minirv-npc.tar.bz2'
    lib=am/'klib/build/klib-minirv-npc.a';lib.parent.mkdir(exist_ok=True)
    backup=ROOT/'E/E6/upstream/klib-minirv-npc.a'
    if lib.exists() and not backup.exists():shutil.copyfile(lib,backup)
    with tarfile.open(archive) as t:lib.write_bytes(t.extractfile('klib-minirv-npc.a').read())
    lib.touch()
    dump(ROOT/'reports/E6_klib_source.json',{'source':str(archive),'sha256':sha(archive),'library_sha256':sha(lib),'policy':'Official precompiled library explicitly supplied by E6; original source archive preserved.'})
    rows=[]
    for name,cwd,extra in [('riscv-tests',BENCH/'riscv-tests',['TEST_ISA=i']),('cpu-tests',BENCH/'am-kernels/tests/cpu-tests',[])]:
        if name=='riscv-tests':
            allnames=sorted(p.stem for p in (cwd/'isa/rv32ui').glob('*.S'));excluded=['fence_i','ma_data'];names=[n for n in allnames if n not in excluded]
        else:
            allnames=sorted(p.stem for p in (cwd/'tests').glob('*.c'));excluded=['wrong'];names=[n for n in allnames if n not in excluded];extra=['ALL='+' '.join(names)]
        outputs=[cwd/'build'/(n+'-minirv-npc.bin.npc.json') for n in names]
        o,e,r=run('E6/official/'+name,['make','-j1','ARCH=minirv-npc','run',*extra,'YSYX_HOME='+str(BENCH),'STUID=','STUNAME=AI_E_STAGE'],cwd=cwd,timeout=3600,inputs=[cwd/'Makefile',lib,am/'am/src/riscv/npc/trm.c',BENCH/'npc/csrc/runner.cpp',BENCH/'npc/build/sim'],outputs=outputs)
        results=[]
        for n,f in zip(names,outputs):
            d=json.loads(f.read_text());assert d['result']=='GOOD_TRAP' and d['exit_code']==0 and d['ebreak_calls']==1,(n,d)
            results.append({'test':n,'image_sha256':sha(cwd/'build'/(n+'-minirv-npc.bin')),'result_sha256':sha(f),'simulation':d})
        assert len(re.findall(r'\[\s*[^]]+\]\s*\x1b\[1;32mPASS',o))==len(names),(name,len(names))
        rows.append({'suite':name,'status':'PASS','tests':results,'excluded':excluded,'exclusion_reason':'Official Makefile defaults exclude fence_i and ma_data; wrong is an intentional failure separately verified in E6_halt_and_exit.json.'})
        dump(ROOT/'reports/E6_official_tests.json',{'status':'IN_PROGRESS' if name=='riscv-tests' else 'PASS','library_sha256':sha(lib),'suites':rows})
        mark(['E6-M007' if name=='riscv-tests' else 'E6-M009'],'PASS',['reports/E6_official_tests.json','artifacts/E6/official/'+name],f'{len(names)} official tests compiled and executed with every committed instruction checked against independent C reference; exact test list and source defaults retained.')
    print('OFFICIAL_TESTS_PASS',flush=True)
if __name__=='__main__':main()

from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    p=ROOT/'D/D5';source=ROOT/'D/klib_overlay/alloc.c';build=WORK/'D5';build.mkdir(exist_ok=True)
    flags=['-std=c11','-O1','-g','-Wall','-Wextra','-Werror','-fno-builtin','-fsanitize=address,undefined','-fno-omit-frame-pointer']
    obj=build/'alloc.o';run('D5/allocator/build',['gcc',*flags,'-DD_KLIB_HOST_TEST','-Dmalloc=d_malloc','-Dcalloc=d_calloc','-Drealloc=d_realloc','-Dfree=d_free','-c',source,'-o',obj],inputs=[source],outputs=[obj])
    exe=build/'allocator';run('D5/allocator/test_build',['gcc',*flags,p/'allocator_test.c',obj,'-o',exe],inputs=[p/'allocator_test.c',obj],outputs=[exe])
    o,_,_=run('D5/allocator/test',[exe],inputs=[exe],env={'ASAN_OPTIONS':'detect_leaks=1:halt_on_error=1','UBSAN_OPTIONS':'halt_on_error=1'},timeout=60);assert 'ALLOCATOR_PASS' in o
    bad=build/'alloc-calloc-mutant.c';bad.write_text(source.read_text().replace('if(p)memset(p,0,total)','if(p)memset(p,0x11,total)'));assert bad.read_text()!=source.read_text()
    badobj=build/'alloc-bad.o';badexe=build/'allocator-bad'
    run('D5/allocator/mutant_build',['gcc',*flags,'-DD_KLIB_HOST_TEST','-Dmalloc=d_malloc','-Dcalloc=d_calloc','-Drealloc=d_realloc','-Dfree=d_free','-c',bad,'-o',badobj],inputs=[bad],outputs=[badobj])
    run('D5/allocator/mutant_link',['gcc',*flags,p/'allocator_test.c',badobj,'-o',badexe],inputs=[p/'allocator_test.c',badobj],outputs=[badexe])
    _,error,_=run('D5/allocator/mutant',[badexe],inputs=[badexe],expected=(-6,),env={'ASAN_OPTIONS':'detect_leaks=1:halt_on_error=1','UBSAN_OPTIONS':'halt_on_error=1'});assert 'Assertion' in error
    shutil.copyfile(source,BENCH/'abstract-machine/klib/src/alloc.c')
    dest=p/'runtime_patch/abstract-machine/klib/src/alloc.c';dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
    dump(ROOT/'reports/D5_allocator.json',{'status':'PASS','seed':'0x2607d5','random_operations':10000,'fragmentation_stress_blocks':512,'negative_control':'calloc writes 0x11 instead of zero; unchanged unit assertions reject it','properties':['16-byte alignment','physical block bounds, contiguity and previous/next links','free-list exact membership and absence of cycles','no adjacent uncoalesced free blocks','no overlap of live allocations','preserve data through realloc and neighbor growth','calloc zero','multiplication/alignment overflow rejected','failure preserves original pointer','coalescing permits large allocation after release'],'sanitizers':['AddressSanitizer','UndefinedBehaviorSanitizer'],'implementation_sha256':sha(source),'scope':'Bare-metal allocator tested in a controlled host arena. D8 improved free-list search and local coalescing after profiling; old source and failed slow run preserved. Native AM uses glibc allocation for host startup, explicitly separate.','evidence':'artifacts/D5/allocator'})

if __name__=='__main__':main()

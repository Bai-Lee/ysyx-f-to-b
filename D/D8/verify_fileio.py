from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *
d=ROOT/'D/D8';source=ROOT/'D/klib_overlay/fileio.c';exe=WORK/'build/fileio-test'
run('D8/fileio/build',['gcc','-std=c11','-O1','-g','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-fno-pie','-no-pie','-DD_FILE_TEST_PREFIX',source,d/'fileio_test.c','-o',exe],inputs=[source,d/'fileio_test.c'],outputs=[exe])
o,e,_=run('D8/fileio/test',[exe],inputs=[exe],env={'ASAN_OPTIONS':'detect_leaks=1'});assert 'FILEIO_PASS' in o
bad=d/'results/fileio-missing-eof.c';old='if(got<wanted)s->eof=1;';assert old in source.read_text();bad.write_text(source.read_text().replace(old,'if(got<wanted)s->eof=0;'))
badexe=WORK/'build/fileio-mutant'
run('D8/fileio/mutant-build',['gcc','-std=c11','-O1','-g','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-fno-pie','-no-pie','-DD_FILE_TEST_PREFIX',bad,d/'fileio_test.c','-o',badexe],inputs=[bad,d/'fileio_test.c'],outputs=[badexe])
_,error,_=run('D8/fileio/mutant',[badexe],inputs=[badexe],expected=(-6,),env={'ASAN_OPTIONS':'detect_leaks=1'});assert 'd_feof' in error
target=BENCH/'abstract-machine/klib/src/fileio.c';shutil.copyfile(source,target)
dump(ROOT/'reports/D8_fileio.json',{'status':'PASS_HOST_TESTS_INSTALLED_FOR_TARGET','source_sha256':sha(source),'stdout':o,'reference':'glibc fmemopen/fread/ftell/feof/fscanf plus independently constructed output bytes','sanitizers':['ASAN','UBSAN'],'scope':'AM embedded RAM files; 64 named files, 29 nonstandard open streams, 64MiB per writable file, one-MiB formatted output bound. Opaque FILE API only; no POSIX/filesystem/stdio-internals compatibility claim.'})

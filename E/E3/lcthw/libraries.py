from native import *
import shutil
def main():
    d=SRC/'library';d.mkdir(exist_ok=True)
    for sub in ('src','tests','build'):(d/sub).mkdir(exist_ok=True)
    (d/'src/dbg.h').write_text(block(20,0))
    (d/'src/libex29.c').write_text(block(29,0))
    original_loader=d/'ex29_original.c';original_loader.write_text(block(29,1))
    lib=BIN/'libex29_original.so'
    run('ex29/library',['gcc','-std=gnu17','-Wall','-g','-O0','-fPIC','-shared','-I'+str(d/'src'),str(d/'src/libex29.c'),'-o',str(lib)],inputs=[d/'src/libex29.c',d/'src/dbg.h'])
    loader,_,_=build('ex29_original',files=[original_loader],flags=['-I'+str(d/'src'),'-ldl'])
    for fn,arg,expected in [('print_a_message','hello there','A STRING: hello there\n'),('uppercase','hello there','HELLO THERE\n'),('lowercase','HELLO tHeRe','hello there\n')]:
        o,e,r=execute('ex29_'+fn,loader,[str(lib),fn,arg],vg=True);assert o==expected and 'ERROR SUMMARY: 0 errors' in e
    for name,args in [('intended_fail',[str(lib),'fail_on_purpose','i fail']),('missing_symbol',[str(lib),'not_a_symbol','x']),('missing_library',[str(lib)+'.missing','x','x']),('argc',[str(lib),'uppercase'])]:
        execute('ex29_'+name,loader,args,expected=(1,))
    damaged=BIN/'libex29_bad.so';data=bytearray(lib.read_bytes());data[0]^=255;damaged.write_bytes(data)
    o,e,r=execute('ex29_corrupt',loader,[str(damaged),'uppercase','abc'],expected=(1,));assert 'invalid ELF' in e
    for option in ['RTLD_NOW','RTLD_LAZY']:
        s=d/(option+'.c');s.write_text(block(29,1).replace('RTLD_NOW',option))
        x,_,_=build('ex29_'+option,files=[s],flags=['-I'+str(d/'src'),'-ldl'])
        o,e,r=execute('ex29_'+option,x,[str(lib),'uppercase','hello']);assert o=='HELLO\n'
    run('ex29_man',['man','-P','cat','3','dlopen'])
    # Length-aware exported functions coexist with the original ABI.
    extra=r'''
#include <stddef.h>
int uppercase_n(const unsigned char *msg,size_t n){for(size_t i=0;i<n;i++)putchar(toupper(msg[i]));return 0;}
int lowercase_n(const unsigned char *msg,size_t n){for(size_t i=0;i<n;i++)putchar(tolower(msg[i]));return 0;}
int print_a_message_n(const unsigned char *msg,size_t n){fputs("A STRING: ",stdout);return fwrite(msg,1,n,stdout)==n?0:1;}
'''
    (d/'src/libex29.c').write_text(block(29,0)+extra)
    (d/'tests/minunit.h').write_text(block(30,0))
    test=block(30,4).replace('build/libYOUR_LIBRARY.so','build/libex29.so')
    (d/'tests/ex29_tests.c').write_text(test)
    (d/'src/demo.h').write_text('int lab_add(int,int);\n')
    (d/'src/demo.c').write_text('#include "demo.h"\nint lab_add(int a,int b){return a+b;}\n')
    (d/'tests/demo_tests.c').write_text('#include <demo.h>\nint main(void){return lab_add(2,3)!=5;}\n')
    make='''CC=gcc
CFLAGS=-std=gnu17 -g -O2 -Wall -Wextra -Isrc -fPIC
LIBNAME?=ex29
SOURCES=$(wildcard src/*.c)
OBJECTS=$(SOURCES:.c=.o)
TEST_SRC=$(wildcard tests/*_tests.c)
TESTS=$(TEST_SRC:.c=)
TARGET=build/lib$(LIBNAME).a
SHARED=build/lib$(LIBNAME).so
.PHONY: all tests test clean check
all: $(TARGET) $(SHARED) tests
build:
\tmkdir -p build
$(TARGET): $(OBJECTS) | build
\tar rcs $@ $(OBJECTS)
$(SHARED): $(OBJECTS) | build
\t$(CC) -shared $^ -o $@
tests/%_tests: tests/%_tests.c $(TARGET) $(SHARED)
\t$(CC) $(CFLAGS) $< $(TARGET) -ldl -o $@
tests test: $(TESTS)
\tsh tests/runtests.sh
clean:
\trm -f $(OBJECTS) $(TESTS) $(TARGET) $(SHARED) tests/tests.log
BADFUNCS='[^_.>a-zA-Z0-9](str(n?cpy|n?cat|xfrm|n?dup|str|pbrk|tok|_)|stpn?cpy|a?sn?printf|byte_)'
check:
\t@grep -En $(BADFUNCS) $(SOURCES) || true
'''
    (d/'Makefile').write_text(make)
    runner='''#!/bin/sh
set -eu
found=0
for test_file in tests/*_tests; do
 if [ -f "$test_file" ]; then
  found=1
  if "$test_file" 2>>tests/tests.log; then printf '%s PASS\\n' "$test_file"; else tail tests/tests.log; exit 1; fi
 fi
done
test "$found" -eq 1
'''
    (d/'tests/runtests.sh').write_text(runner)
    # Preserve the book template, including its historical recipes, separately.
    (d/'Makefile.reference').write_text(block(28,1))
    work=common.LAB/'library';work.mkdir(exist_ok=True)
    shutil.copytree(d,work,dirs_exist_ok=True)
    run('library/build',['make','-j2','all'],cwd=work,inputs=list(d.glob('src/*'))+[d/'Makefile'])
    o,e,r=run('library/tests',['make','test'],cwd=work);assert 'ALL TESTS PASSED' in o
    run('library/memcheck_tests',['valgrind','--error-exitcode=99','--leak-check=full','tests/ex29_tests'],cwd=work)
    driver=write('length_loader.c',r'''#include <stdio.h>
#include <dlfcn.h>
#include <stddef.h>
typedef int(*F)(const unsigned char*,size_t);
int main(int argc,char**argv){if(argc!=2)return 2;void*h=dlopen(argv[1],RTLD_NOW);if(!h)return 3;F f=(F)dlsym(h,"uppercase_n");if(!f)return 4;unsigned char data[4]={'a',0,'b',255};int rc=f(data,4);dlclose(h);return rc;}
''')
    x,_,_=build('length_loader',files=[driver],flags=['-ldl'])
    execute('length_loader',x,[str(work/'build/libex29.so')],vg=True)
    assert (common.OUT/'length_loader/run/stdout.log').read_bytes()==b'A\0B\xff'
    # Valid test vs deliberately wrong expectation verifies the harness fails.
    (work/'tests/deliberate_tests.c').write_text('int main(void){return 1;}\n')
    run('library/negative_harness',['make','test'],cwd=work,expected=(2,))
    for name in ['deliberate_tests.c','deliberate_tests']:(work/'tests'/name).unlink()
    run('library/positive_again',['make','test'],cwd=work)
    # Read and test BADFUNCS as a lexical heuristic, including its limits.
    probes=work/'function-probes.txt';probes.write_text(' strcpy(x,y);\n snprintf(b,n,"%s",s);\n obj.strcpy(x);\n my_strcpy(x);\nstrcpy(x,y);\n')
    regex=r'[^_.>a-zA-Z0-9](str(n?cpy|n?cat|xfrm|n?dup|str|pbrk|tok|_)|stpn?cpy|a?sn?printf|byte_)'
    o,e,r=run('library/badfuncs',['grep','-En',regex,str(probes)])
    assert '1:' in o and '2:' in o and '3:' not in o and '4:' not in o and '5:' not in o
    # Clean reusable skeleton contains no exercise29 symbols or source.
    skeleton=SRC/'c_skeleton';skeleton.mkdir(exist_ok=True)
    for sub in ('src','tests'):(skeleton/sub).mkdir(exist_ok=True)
    for name in ('demo.c','demo.h','dbg.h'):shutil.copyfile(d/'src'/name,skeleton/'src'/name)
    for name in ('minunit.h','demo_tests.c','runtests.sh'):shutil.copyfile(d/'tests'/name,skeleton/'tests'/name)
    (skeleton/'Makefile').write_text(make.replace('LIBNAME?=ex29','LIBNAME?=starter'))
    clean=common.LAB/'clean_skeleton';shutil.copytree(skeleton,clean,dirs_exist_ok=True)
    run('skeleton/build',['make','-j2','all'],cwd=clean)
    assert not any('ex29' in f.read_text(errors='replace') for f in skeleton.rglob('*') if f.is_file())
    # C test runner: preserve child exit status, reject empty suites.
    c_runner=write('runtests.c',r'''#include <dirent.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
int main(void){DIR*d=opendir("tests");if(!d)return 2;struct dirent*e;int found=0;while((e=readdir(d))){size_t n=strlen(e->d_name);if(n<6||strcmp(e->d_name+n-6,"_tests"))continue;char p[512];if(snprintf(p,sizeof p,"tests/%s",e->d_name)>=(int)sizeof p){closedir(d);return 2;}found=1;pid_t child=fork();if(child<0){closedir(d);return 2;}if(!child){execl(p,p,(char*)0);_exit(127);}int status;if(waitpid(child,&status,0)<0||!WIFEXITED(status)||WEXITSTATUS(status)!=0){closedir(d);return 1;}}closedir(d);return found?0:1;}
''')
    cr,_,_=build('c_test_runner',files=[c_runner],strict=True)
    run('c_runner/pass',[str(cr)],cwd=clean)
    fail=clean/'tests/fail_tests';fail.write_text('#!/bin/sh\nexit 7\n');fail.chmod(0o755)
    run('c_runner/fail',[str(cr)],cwd=clean,expected=(1,));fail.unlink()
    run('c_runner/pass_again',[str(cr)],cwd=clean)
    verdict(['LCT-28-BASE']+[f'LCT-28-X{i:02}' for i in range(1,4)],'PASS_ADAPTED',['library/build','library/badfuncs','library/negative_harness'],'Real static/shared libraries and nonempty positive/negative tests. Book recipe spaces restored to TAB; link libraries moved after source/object arguments for modern linker ordering. BADFUNCS is a textual warning heuristic, not a proof of vulnerability or safety.')
    verdict(['LCT-29-BASE','LCT-29-BREAK']+[f'LCT-29-X{i:02}' for i in range(1,5)],'PASS',['ex29/library','ex29_corrupt','ex29_RTLD_NOW','ex29_RTLD_LAZY','length_loader','library/tests','ex29_man'],'Actual shared object/loader, all normal/error cases, corrupted ELF rejection, explicit-length interface handles embeddedNUL and0xff, real unit-test target, RTLD_NOW/LAZY and manuals.')
    verdict(['LCT-30-BASE','LCT-30-X01','LCT-30-X02'],'PASS',['library/tests','library/negative_harness','skeleton/build','c_runner/fail'],'Original minunit actual four tests populated and executed; clean skeleton copied/built without ex29; C fork/exec runner tested with success and failure, not just an empty suite.')
    print('LIBRARIES_AND_TEST_FRAMEWORK_DONE',flush=True)
if __name__=='__main__':main()

from native import *
import shutil
def main():
    d=SRC/'macros_scope';d.mkdir(exist_ok=True);(d/'dbg.h').write_text(block(20,0));(d/'ex20.c').write_text(block(20,1))
    records=[]
    for name,text,flags in [('ex20',block(20,1),[]),('ex20_top_ndebug','#define NDEBUG\n'+block(20,1),[]),('ex20_flag_ndebug',block(20,1),['-DNDEBUG'])]:
        source=d/(name+'.c');source.write_text(text);exe,_,_=build(name,files=[source],flags=flags)
        o,e,r=run(name+'/run',['valgrind','--error-exitcode=99',str(exe),'definitely-missing-file'],cwd=d,inputs=[source,d/'dbg.h',exe])
        assert 'ERROR SUMMARY: 0 errors' in e and '[ERROR]' in e and '[INFO]' in e
        assert ('DEBUG ' in e)==(not flags and not name.endswith('top_ndebug'))
    enhanced=block(20,0).replace('%s:%d','%s:%d:%s').replace('__FILE__, __LINE__,','__FILE__, __LINE__, __func__,')
    (d/'dbg_function.h').write_text(enhanced)
    s=d/'ex20_functions.c';s.write_text(block(20,1).replace('"dbg.h"','"dbg_function.h"'))
    exe,_,_=build('ex20_functions',files=[s]);o,e,r=run('ex20_functions/run',[str(exe),'definitely-missing-file'],cwd=d,inputs=[s,d/'dbg_function.h',exe]);assert 'test_log_err' in e and 'test_check' in e
    verdict(['LCT-20-BASE']+[f'LCT-20-X{i:02}' for i in range(1,4)],'PASS',['ex20/run','ex20_top_ndebug/run','ex20_flag_ndebug/run','ex20_functions/run'],'Original macro error paths and cleanup tested; NDEBUG removes debug output but does not remove check/goto behavior; function/file/line included in derived macros.')
    for name,index in [('ex22.h',0),('ex22.c',1),('ex22_main.c',2)]:(d/name).write_text(block(22,index))
    make=d/'Makefile';make.write_text('''CC=gcc
CFLAGS=-std=gnu17 -Wall -g -O0
.PHONY: all clean
all: scopes
scopes: ex22.o ex22_main.o
\t$(CC) $^ -o $@
%.o: %.c ex22.h dbg.h
\t$(CC) $(CFLAGS) -c $< -o $@
clean:
\trm -f ex22.o ex22_main.o scopes
''')
    # Native filesystem avoids DrvFS metadata semantics; source copies stay separate.
    work=common.LAB/'scopes';work.mkdir(exist_ok=True)
    for name in ('Makefile','dbg.h','ex22.h','ex22.c','ex22_main.c'):shutil.copyfile(d/name,work/name)
    run('ex22_make',['make','-j2'],cwd=work,inputs=[d/'Makefile',d/'ex22.h',d/'ex22.c',d/'ex22_main.c'])
    o,e,r=run('ex22/run',['valgrind','--error-exitcode=99',str(work/'scopes')],cwd=work)
    for value in ['age: 37','now: 100','THE_SIZE is: 1000','THE SIZE is now: 9','first: 1.000000','again: 2.000000','more: 10.000000','scope_demo: 4']:assert value in e
    assert 'ERROR SUMMARY: 0 errors' in e
    verdict(['LCT-22-BASE','LCT-22-X05'],'PASS',['ex22_make','ex22/run'],'Real separate object compilation/linking; static lifetime retains ratio, file-static age exposed only by accessors, local shadowing leaves caller count4.')
    hidden=d/'hidden.c';hidden.write_text('#include <stdio.h>\nextern int THE_AGE;extern double ratio;int main(void){printf("%d %f",THE_AGE,ratio);}\n')
    _,o,e=build('ex22_hidden',files=[d/'ex22.c',hidden],expected=(1,));assert 'undefined reference' in e
    bad=SRC/'scope_bad_extern';bad.mkdir(exist_ok=True)
    for n in ('dbg.h','ex22.c','ex22_main.c'):shutil.copyfile(d/n,bad/n)
    (bad/'ex22.h').write_text(block(22,0).replace('extern int THE_SIZE;','int THE_SIZE;'))
    _,o,e=build('ex22_multiple_definition',files=[bad/'ex22.c',bad/'ex22_main.c'],expected=(1,));assert 'multiple definition' in e
    _,o,e=build('const_write','int main(void){const int x=1;x=2;return x;}',strict=True,expected=(1,));assert 'read-only' in e
    _,o,e=build('register_address','int main(void){register int x=1;int *p=&x;return *p;}',strict=True,expected=(1,));assert 'register' in e
    ptr=write('scope_pointer.c',r'''#include <assert.h>
#include <stdio.h>
static int hidden=3;
int *expose(void){return &hidden;}
void value(int x){x=8;}
void pointer(int *x){*x=8;}
int main(void){int a=1;value(a);assert(a==1);pointer(&a);assert(a==8);int *p=expose();*p=11;assert(*expose()==11);puts("PASS value, pointer, static lifetime");}
''')
    exe,_,_=build('scope_pointer',files=[ptr]);o,e,r=execute('scope_pointer',exe,vg=True);assert 'PASS value' in o and 'ERROR SUMMARY: 0 errors' in e
    exe,_,_=build('scope_invalid',r'''#include <stdio.h>
static const int immutable=3;
int main(void){*(volatile int *)&immutable=4;printf("%d\n",immutable);return 0;}
''')
    o,e,r=execute('scope_invalid',exe,vg=True,expected=(-11,99));assert 'Bad permissions' in e or 'Invalid write' in e
    recurse=write('stack_overflow.c',r'''#include <stdio.h>
volatile unsigned depth=0;
__attribute__((noinline)) void recurse(void){volatile char block[1024];block[0]=(char)depth++;recurse();if(block[0]==123)puts("unreachable");}
int main(void){recurse();return 0;}
''')
    exe,_,_=build('stack_overflow',files=[recurse],flags=['-fno-optimize-sibling-calls'])
    o,e,r=shell('stack_overflow/run','ulimit -s 128\nexec '+str(exe)+'\n',expected=(-11,139),timeout=10)
    wrapper=common.LAB/'limited_stack.sh';wrapper.write_text('#!/bin/sh\nulimit -s 128\nexec "$@"\n');wrapper.chmod(0o755)
    o,e,r=run('stack_overflow/gdb',['gdb','--batch','-q','-ex','set pagination off','-ex','set exec-wrapper '+str(wrapper),'-ex','run','-ex','bt 8','-ex','print depth',str(exe)],timeout=20)
    assert 'SIGSEGV' in o and o.count('recurse')>=3 and re.search(r'\$1 = [1-9]',o)
    verdict(['LCT-22-BREAK']+[f'LCT-22-X{i:02}' for i in range(1,5)],'PASS',['ex22_hidden','ex22_multiple_definition','const_write','scope_pointer','scope_invalid','stack_overflow/gdb'],'Compiler/linker enforcement, real pointer escape to live static object, by-value vs pointer update, bad write diagnostics and bounded128KiB stack exhaustion with GDB backtrace. No global stack limit or ptrace policy changed.')
    print('MACROS_SCOPE_DONE',flush=True)
if __name__=='__main__':main()

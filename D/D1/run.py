from pathlib import Path
import sys,re,statistics,gzip
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

def main():
    scope=ROOT/'D/D1';src=scope/'src';src.mkdir(exist_ok=True);out=scope/'results';out.mkdir(exist_ok=True)
    build=WORK/'D1';build.mkdir(exist_ok=True)
    lock=json.loads((ROOT/'reports/D_clang.json').read_text());clang=lock['compiler'];env=lock['env']
    files={
      'preprocess.c':'// source exercise, D1 preprocessing\n#include <stdio.h>\n#define MSG "Hello \\\nWorld!\\n"\n#define _str(x) #x\n#define _concat(a,b) a##b\nint main(void){printf(MSG /* "hi!\\n" */);\n#ifdef __riscv\nprintf("Hello RISC-V!\\n");\n#endif\n_concat(pr,intf)(_str(RISC-V));return 0;}\n',
      'add.c':'#include <stdio.h>\nint main(void){int x=10,y=20;int z=x+y;printf("z = %d\\n",z);return 0;}\n',
      'volatile.c':'#include <stdio.h>\nint main(void){volatile int x=10,y=20;int z=x+y;printf("z = %d\\n",z);return 0;}\n',
      'sum.c':'#include <stdio.h>\n#include <stdlib.h>\nint main(int argc,char **argv){unsigned long long n=argc==2?strtoull(argv[1],0,10):100000000ULL;if(n>1000000000ULL)return 2;unsigned long long sum=0;for(unsigned long long i=1;i<=n;i++)sum+=i;printf("%llu\\n",sum);return 0;}\n',
      'source_unsequenced.c':'#include <stdio.h>\nstatic void f(int x,int y){printf("x = %d, y = %d\\n",x,y);}\nint main(void){int i=1;f(i++,i++);return 0;}\n',
      'unspecified_order.c':'#include <stdio.h>\nstatic int left(void){puts("LEFT");return 1;}\nstatic int right(void){puts("RIGHT");return 2;}\nstatic void f(int x,int y){printf("%d %d\\n",x,y);}\nint main(void){f(left(),right());return 0;}\n',
      'sequenced.c':'#include <stdio.h>\nint main(void){int i=1;int x=i++;int y=i++;printf("x = %d, y = %d\\n",x,y);return 0;}\n',
      'source_bounds.c':'#include <stdio.h>\nint main(void){int a[10]={0};printf("a[10] = %d\\n",a[10]);return 0;}\n',
      'header_ok.c':'#include <stdio.h>\n#ifndef D_CUSTOM_STDIO_SELECTED\n#error wrong header selected\n#endif\nint main(void){return D_CUSTOM_STDIO_SELECTED!=2607;}\n',
    }
    for n,t in files.items():(src/n).write_text(t)
    inc=src/'include';inc.mkdir(exist_ok=True);(inc/'stdio.h').write_text('#ifndef D_CUSTOM_STDIO_H\n#define D_CUSTOM_STDIO_H\n#define D_CUSTOM_STDIO_SELECTED 2607\nint printf(const char *, ...);\n#endif\n')
    empty=src/'empty.c';empty.write_text('/* macro inventory */\n')
    def job(name,cmd,inputs=(),outputs=(),expected=(0,),timeout=60):
        folder=ROOT/'artifacts/D1'/name
        if '--resume' in sys.argv and (folder/'run.json').exists():
            prior=json.loads((folder/'run.json').read_text())
            valid=prior['status']=='PASS' and prior['command']==list(map(str,cmd))
            valid=valid and prior['inputs']==[{'path':str(p),'sha256':sha(p)} for p in inputs]
            valid=valid and all(Path(x['path']).is_file() and sha(x['path'])==x.get('sha256') for x in prior.get('outputs',[]))
            if valid:return (folder/'stdout.log').read_text(),(folder/'stderr.log').read_text(),prior
        return run('D1/'+name,cmd,inputs=inputs,outputs=outputs,expected=expected,timeout=timeout,env=env,cwd=build)
    macros={}
    for arch,cc in [('host','gcc'),('riscv','riscv64-linux-gnu-gcc')]:
        target=out/f'{arch}.i';job('preprocess_'+arch,[cc,'-E',src/'preprocess.c','-o',target],inputs=[src/'preprocess.c'],outputs=[target])
        text=target.read_text();assert re.search(r'printf\("Hello World!\\n"\s*\)',text) and 'printf("RISC-V")' in text
        assert ('printf("Hello RISC-V!\\n")' in text)==(arch=='riscv')
        o,_,_=job('macros_'+arch,[cc,'-dM','-E',empty],inputs=[empty]);(out/f'{arch}-macros.txt').write_text('\n'.join(sorted(o.splitlines()))+'\n');macros[arch]=dict(re.findall(r'^#define (\S+) (.*)$',o,re.M))
    _,search,_=job('header_search',['gcc','-E','-v',src/'preprocess.c','-o','/dev/null'],inputs=[src/'preprocess.c']);assert '#include <...> search starts here:' in search
    job('custom_header_preprocess',['gcc','-E','-I',inc,src/'header_ok.c','-o',out/'custom.i'],inputs=[src/'header_ok.c',inc/'stdio.h'],outputs=[out/'custom.i']);assert 'return 2607!=2607' in (out/'custom.i').read_text()
    job('custom_header_bad',['gcc','-fsyntax-only',src/'header_ok.c'],inputs=[src/'header_ok.c'],expected=(1,))
    job('clang_phases',[clang,'-ccc-print-phases',src/'add.c'],inputs=[src/'add.c'])
    job('clang_tokens',[clang,'-Xclang','-dump-tokens','-fsyntax-only',src/'add.c'],inputs=[src/'add.c'])
    job('clang_ast',[clang,'-Xclang','-ast-dump','-fsyntax-only',src/'add.c'],inputs=[src/'add.c'])
    for n,source,opt in [('O0','add.c','-O0'),('O1','add.c','-O1'),('volatile_O1','volatile.c','-O1')]:
        ll=out/f'{n}.ll';job('llvm_'+n,[clang,'-S','-emit-llvm',opt,src/source,'-o',ll],inputs=[src/source],outputs=[ll])
    ll0=(out/'O0.ll').read_text();ll1=(out/'O1.ll').read_text();llv=(out/'volatile_O1.ll').read_text()
    assert 'add nsw i32' in ll0 and re.search(r'@printf\([^\n]*i32[^\n]*30\)',ll1)
    assert 'load volatile i32' in llv and 'store volatile i32' in llv and 'add nsw i32' in llv
    for opt in ['O0','O1']:
        asm=out/f'rv64-{opt}.s';obj=out/f'rv64-{opt}.o';elf=out/f'rv64-{opt}.elf'
        job('rv64_asm_'+opt,[clang,'--target=riscv64-linux-gnu','--gcc-toolchain=/usr','-'+opt,'-S',src/'add.c','-o',asm],inputs=[src/'add.c'],outputs=[asm])
        job('rv64_obj_'+opt,[clang,'--target=riscv64-linux-gnu','-c',asm,'-o',obj],inputs=[asm],outputs=[obj])
        job('rv64_link_'+opt,['riscv64-linux-gnu-gcc',obj,'-o',elf],inputs=[obj],outputs=[elf])
        for kind,p in [('object',obj),('executable',elf)]:
            o,_,_=job('disassembly_'+opt+'_'+kind,['riscv64-linux-gnu-objdump','-dr',p],inputs=[p]);(out/f'{opt}-{kind}-disasm.txt').write_text(o)
        job('rv64_headers_'+opt,['riscv64-linux-gnu-readelf','-hSrs',elf],inputs=[elf])
    timings=[];n=100000000;answer=str(n*(n+1)//2)
    for opt in ['O0','O1','O2']:
        exe=build/f'sum-{opt}';job('sum_build_'+opt,['gcc','-std=c11','-'+opt,'-Wall','-Wextra','-Werror',src/'sum.c','-o',exe],inputs=[src/'sum.c'],outputs=[exe])
        times=[]
        for repeat in range(3):
            o,_,row=job('sum_'+opt+'_'+str(repeat),[exe,str(n)],inputs=[exe]);assert o.strip()==answer;times.append(row['elapsed_seconds'])
        job('sum_reject_'+opt,[exe,'1000000001'],inputs=[exe],expected=(2,))
        o,_,_=job('sum_disassembly_'+opt,['objdump','-dr',exe],inputs=[exe]);(out/f'sum-{opt}.txt').write_text(o)
        timings.append({'optimization':opt,'n':n,'result':answer,'wall_seconds':times,'median_seconds':statistics.median(times)})
    host=build/'startup';job('startup_build',['gcc','-g','-O0','-no-pie',src/'add.c','-o',host],inputs=[src/'add.c'],outputs=[host])
    script=src/'startup.gdb';script.write_text('set pagination off\nset confirm off\nset backtrace past-main on\nset backtrace past-entry on\nstarti\nx/i $pc\nbreak _start\ncontinue\nbt\nx/8i $pc\nbreak *main\ncontinue\nbt\nset $main_return = *(void **)$rsp\ntbreak *$main_return\ncontinue\nx/i $pc\nbt\ncatch syscall exit_group\ncontinue\nbt\ncontinue\nquit\n')
    o,e,_=job('startup_gdb',['gdb','-q','-batch','-x',script,host],inputs=[script,host]);assert 'main' in o and 'exit_group' in o and '_start' in o
    job('startup_strace',['strace','-f','-e','trace=execve,write,exit_group',host],inputs=[host])
    observations=[]
    for compiler,cc in [('gcc','gcc'),('clang',clang)]:
        for name in ['source_unsequenced','unspecified_order','sequenced','source_bounds']:
            exe=build/f'{compiler}-{name}';_,warnings,_=job(compiler+'_'+name+'_build',[cc,'-std=c11','-O0','-Wall','-Wextra',src/(name+'.c'),'-o',exe],inputs=[src/(name+'.c')],outputs=[exe])
            seen=[]
            for repeat in range(2):
                o,_,_=job(compiler+'_'+name+'_'+str(repeat),[exe],inputs=[exe]);seen.append(o.strip())
                if name=='sequenced':assert o.strip()=='x = 1, y = 2'
                if name=='unspecified_order':assert set(o.splitlines()[:2])=={'LEFT','RIGHT'} and o.splitlines()[-1]=='1 2'
            observations.append({'compiler':compiler,'case':name,'observed_output':seen,'diagnostic':warnings.strip(),'fixed_output_assertion':name=='sequenced','source_classification_corrected':name=='source_unsequenced'})
    ub=build/'bounds-sanitized';job('bounds_ubsan_build',['gcc','-O0','-g','-fsanitize=undefined','-fno-sanitize-recover=all',src/'source_bounds.c','-o',ub],inputs=[src/'source_bounds.c'],outputs=[ub])
    _,e,_=job('bounds_ubsan',[ub],inputs=[ub],expected=(1,));assert 'out of bounds' in e
    man=Path(clang).resolve().parents[2]/'share/man/man1/clang-15.1.gz'
    if man.exists():(out/'clang-15-man.roff').write_bytes(gzip.decompress(man.read_bytes()))
    report={'status':'PASS','records':16,'timings':timings,'macro_differences':{k:{a:macros[a].get(k) for a in macros} for k in ['__x86_64__','__riscv','__riscv_xlen','__LP64__','__SIZEOF_POINTER__','__BYTE_ORDER__']},'ir_observation':{'O0_add':True,'O1_constant_30':True,'volatile_load_store_retained':True},'behavior_observations':observations,'source_corrections':[{'source':'D/D1/sources/D1.md:991','correction':'f(i++,i++) modifies the same scalar without sequencing and has undefined behavior in C11, not merely unspecified argument order. Preserve observed executions, never constrain them to the two printed examples.','authority':'ISO C11 draft N1570 6.5 paragraph 2; 6.5.2.2 paragraph 10','url':'https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf'},{'correction':'The linked N1570 document is a C11 committee draft, although the course calls it C99 in places.'},{'correction':'Higher optimization levels do not guarantee faster execution on every program or target.'}],'evidence':'artifacts/D1','outputs':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in sorted(out.iterdir()) if p.is_file()]}
    dump(ROOT/'reports/D1_experiments.json',report)
    mark([f'D1-M{i:03d}' for i in range(1,17)],'PASS',['reports/D1_experiments.json','D/D1/results','artifacts/D1'],'Real compiler, LLVM IR, cross-toolchain, timing, GDB/strace and UB diagnostics. Source misclassification explicitly corrected from N1570.')
    print('D1_EXPERIMENTS_PASS',flush=True)

if __name__=='__main__':main()

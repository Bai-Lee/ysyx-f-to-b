from pathlib import Path
import sys,json,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evidence import *
from lct_early import lp,SOLUTION,BIN

def main():
    rows=[];observed=[]
    def linux(name,args,inputs,expected=0):
        q=run('E3/lcthw/extra/'+name,['wsl.exe','-d','YSYX-Linux','-u','ysyx','--exec','env','LC_ALL=C',*map(str,args)],inputs,expected=expected,timeout=40)
        assert q['status']=='PASS';rows.append(q)
        folder=ROOT/'artifacts/E3/lcthw/extra'/name
        return (folder/'stdout.log').read_text('utf8',errors='replace'),(folder/'stderr.log').read_text('utf8',errors='replace')
    src=SOLUTION/'supplement.c';exe=BIN/'supplement.elf'
    linux('supplement_compile',['gcc','-std=c17','-Wall','-Wextra','-Werror','-O0','-g',lp(src),'-o',lp(exe)],[src])
    out,err=linux('supplement_valgrind',['valgrind','--error-exitcode=99','--leak-check=full',lp(exe)],[src,exe])
    assert 'ERROR SUMMARY: 0 errors' in err
    assert out=='ABI int=4 long=8 pointer=8 CHAR_BIT=8\nNAME bytes=5a 65 64 00 packed=0064655a\nPASS formats unsigned_promotions arrays safe_object_copy\n'
    src=SOLUTION/'abi_probe.c';exe=BIN/'abi_linux.elf'
    linux('abi_linux_compile',['gcc','-std=c17','-Wall','-Werror',lp(src),'-o',lp(exe)],[src])
    out,err=linux('abi_linux',[lp(exe)],[src,exe]);assert out=='int=4 long=8 pointer=8 CHAR_BIT=8\n'
    gcc=Path(r'D:\msys64\ucrt64\bin\gcc.exe');native=BIN/'abi_windows.exe';env=os.environ.copy();env['PATH']=str(gcc.parent)+';'+env.get('PATH','')
    q=run('E3/lcthw/extra/abi_windows_compile',[gcc,'-std=c17','-Wall','-Werror',src,'-o',native],[src],env=env);assert q['status']=='PASS';rows.append(q)
    q=run('E3/lcthw/extra/abi_windows',[native],[src,native],env=env);assert q['status']=='PASS';rows.append(q)
    assert (ROOT/'artifacts/E3/lcthw/extra/abi_windows/stdout.log').read_text('utf8').strip()=='int=4 long=4 pointer=8 CHAR_BIT=8'

    # Deliberately too-large literals: compiler diagnostic + observed target-specific result.
    for name,decl,fmt in [
        ('long_overflow_literal','long x=9223372036854775808L;','%ld'),
        ('unsigned_too_large','unsigned long x=18446744073709551616UL;','%lu')]:
        src=SOLUTION/(name+'.c');src.write_text('#include <stdio.h>\nint main(void){'+decl+'printf("'+fmt+'\\n",x);return 0;}\n',encoding='utf8',newline='\n');exe=BIN/(name+'.elf')
        out,err=linux(name+'_compile',['gcc','-std=c17','-Wall','-Wconversion','-O0','-g',lp(src),'-o',lp(exe)],[src])
        assert 'warning:' in err
        out,err=linux(name,[lp(exe)],[src,exe]);observed.append({'name':name,'observed_stdout':out,'scope':'Out-of-range literal/conversion observation on this GCC target, not portable behavior.'})
    src=SOLUTION/'signed_overflow.c';src.write_text('#include <stdio.h>\n#include <limits.h>\nint main(void){volatile long two=2;long x=LONG_MAX;printf("%ld\\n",x*two);return 0;}\n',encoding='utf8',newline='\n')
    exe=BIN/'signed_overflow.elf'
    linux('signed_overflow_compile',['gcc','-std=c17','-Wall','-Werror','-O0','-g','-fsanitize=undefined','-fno-sanitize-recover=all',lp(src),'-o',lp(exe)],[src])
    out,err=linux('signed_overflow',[lp(exe)],[src,exe],expected=1);assert 'signed integer overflow' in err
    src=SOLUTION/'misaligned_pun.c';src.write_text('#include <stdio.h>\nint main(void){_Alignas(int) unsigned char bytes[8]={1,2,3,4,5,6,7,8};int *p=(int *)(bytes+1);printf("%d\\n",*p);return 0;}\n',encoding='utf8',newline='\n')
    exe=BIN/'misaligned_pun.elf'
    linux('misaligned_compile',['gcc','-std=c17','-Wall','-O0','-g','-fsanitize=undefined','-fno-sanitize-recover=all',lp(src),'-o',lp(exe)],[src])
    out,err=linux('misaligned',[lp(exe)],[src,exe],expected=1);assert 'misaligned address' in err
    result={'status':'PASS','runs':rows,'out_of_range_observations':observed,'abi_comparison':{'native_Windows_x86_64':'LLP64: int4,long4,pointer8','Linux_x86_64':'LP64: int4,long8,pointer8'},'scope':'Selected additional exercises for printf formats, unsigned wrapping/promotions, array element writes, legal memcpy packing and invalid alignment; not a verdict for all LCTHW extras.','timestamp':datetime.now(timezone.utc).isoformat()}
    dump(ROOT/'reports/E3_LCT_early_extra_results.json',result);print('E3_LCT_EARLY_EXTRA PASS',len(rows),'actual commands',flush=True)

if __name__=='__main__':main()

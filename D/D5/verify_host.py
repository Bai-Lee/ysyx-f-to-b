from pathlib import Path
import sys,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import *

FUNCTIONS=['strlen','strcpy','strncpy','strcat','strcmp','strncmp','memset','memcpy','memmove','memcmp','strchr','strrchr','printf','vprintf','vsprintf','sprintf','snprintf','vsnprintf']
def main():
    p=ROOT/'D/D5';sources=ROOT/'D/klib_overlay';build=WORK/'D5';build.mkdir(exist_ok=True)
    flags=['-std=c11','-O1','-g','-Wall','-Wextra','-Werror','-fno-builtin','-fsanitize=address,undefined','-fno-omit-frame-pointer']
    objects=[]
    for name in ['string','stdio']:
        obj=build/(name+'.o');run('D5/host/'+name+'_build',['gcc',*flags,'-DD_KLIB_HOST_TEST',*['-D'+x+'=d_'+x for x in FUNCTIONS],'-c',sources/(name+'.c'),'-o',obj],inputs=[sources/(name+'.c')],outputs=[obj]);objects.append(obj)
    exe=build/'compare';run('D5/host/compare_build',['gcc',*flags,p/'host_compare.c',*objects,'-o',exe],inputs=[p/'host_compare.c',*objects],outputs=[exe])
    o,_,_=run('D5/host/compare',[exe],inputs=[exe],env={'ASAN_OPTIONS':'detect_leaks=1:halt_on_error=1','UBSAN_OPTIONS':'halt_on_error=1'},timeout=90);checks=int(re.search('checks=(\d+)',o).group(1))
    # Deliberately omit the terminating NUL in strcpy/strcat; fixed reference remains unchanged.
    bad=build/'bad_string.c';bad.write_text((sources/'string.c').read_text().replace('do{*dst++=*src;}while(*src++);','while(*src){*dst++=*src++;}'))
    bo=build/'bad_string.o';run('D5/host/mutant_build',['gcc',*flags,'-DD_KLIB_HOST_TEST',*['-D'+x+'=d_'+x for x in FUNCTIONS],'-c',bad,'-o',bo],inputs=[bad],outputs=[bo])
    mutant=build/'bad_compare';run('D5/host/mutant_link',['gcc',*flags,p/'host_compare.c',bo,objects[1],'-o',mutant],inputs=[p/'host_compare.c',bo,objects[1]],outputs=[mutant])
    _,e,r=run('D5/host/mutant_rejected',[mutant],inputs=[mutant],expected=(-6,),env={'ASAN_OPTIONS':'detect_leaks=1:halt_on_error=1','UBSAN_OPTIONS':'halt_on_error=1'});assert 'Assertion' in e
    dump(ROOT/'reports/D5_host_klib.json',{'status':'PASS','comparisons':checks,'reference':'Native glibc functions, plus unchanged guard bytes and return pointers; comparison source compiled separately from renamed candidate functions.','sanitizers':['AddressSanitizer','UndefinedBehaviorSanitizer'],'negative_control':'Missing string terminator rejected by same unchanged assertions','printf_scope':'integer/string/char/pointer/percent; flags, width, precision, hh/h/l/ll/z/t/j. No floating conversion or %n claim; widths above 1,000,000 are resource-rejected.','evidence':'artifacts/D5/host'})
    print('D5_HOST_KLIB_PASS',checks,flush=True)

if __name__=='__main__':main()

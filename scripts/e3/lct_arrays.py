from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evidence import *
from lct_early import SOLUTION,BIN,lp

def main():
    runs=[];observations=[]
    text8=(SOLUTION/'ex8.c').read_text('utf8');text9=(SOLUTION/'ex9.c').read_text('utf8')
    needle='    // WARNING: On some systems';assert text8.count(needle)==1
    assign8=text8.replace(needle,"    areas[0] = 100; name[0] = 'T'; full_name[0] = 'T'; areas[1] = name[0];\n\n"+needle)
    needle='    numbers[3] = 4;';assert text9.count(needle)==1
    chars9=text9.replace(needle,needle+'''
    numbers[0]='A'; numbers[1]='B'; numbers[2]='C'; numbers[3]='D';
    printf("numbers-as-characters: %c%c%c%c\\n",numbers[0],numbers[1],numbers[2],numbers[3]);''')
    needle="    char name[4] = {'a'};";assert text9.count(needle)==1
    pun9=text9.replace(needle,needle+'''
    int *wrong_view = (int *)name;
    printf("wrong-int-array: %d %d %d %d\\n", wrong_view[0], wrong_view[1], wrong_view[2], wrong_view[3]);''')
    for name,text,mode in [('ex8_assignments',assign8,'good'),('ex9_char_numbers',chars9,'good'),('ex9_int_array_pun',pun9,'observe'),('ex9_int_array_pun_asan',pun9,'asan')]:
        src=SOLUTION/(name+'.c');src.write_text(text,encoding='utf8',newline='\n');exe=BIN/(name+'.elf');flags=['-std=c17','-Wall','-Werror','-O0','-g']
        if mode=='asan':flags+=['-fsanitize=address,undefined','-fno-sanitize-recover=all']
        q=run('E3/lcthw/arrays/'+name+'/compile',['wsl.exe','-d','YSYX-Linux','-u','ysyx','--exec','gcc',*flags,lp(src),'-o',lp(exe)],[src],timeout=30);assert q['status']=='PASS';runs.append(q)
        args=['valgrind','--error-exitcode=99',lp(exe)] if mode!='asan' else [lp(exe)]
        expected=0 if mode=='good' else [0,99,11,139] if mode=='observe' else 1
        q=run('E3/lcthw/arrays/'+name+'/run',['wsl.exe','-d','YSYX-Linux','-u','ysyx','--exec',*args],[src,exe],expected=expected,timeout=30);assert q['status']=='PASS';runs.append(q)
        folder=ROOT/'artifacts/E3/lcthw/arrays'/name/'run';out=(folder/'stdout.log').read_text('utf8');err=(folder/'stderr.log').read_text('utf8')
        if name=='ex8_assignments':assert 'The first area is 100, the 2nd 84.' in out and 'name="Ted" and full_name="Ted A. Shaw"' in out
        if name=='ex9_char_numbers':assert 'numbers-as-characters: ABCD' in out and 'numbers: 65 66 67 68' in out
        if mode=='good':assert 'ERROR SUMMARY: 0 errors' in err
        if mode=='asan':assert 'stack-buffer-overflow' in err
        observations.append({'name':name,'mode':mode,'exit_code':q['exit_code'],'valgrind_zero_error':'ERROR SUMMARY: 0 errors' in err,'asan_bounds_error':'stack-buffer-overflow' in err})
    dump(ROOT/'reports/E3_LCT_array_variants.json',{'status':'PASS','scope':'Original examples8/9 array writes and integer reinterpretation activities','runs':runs,'observations':observations})
    print('E3_EXACT_ARRAY_ACTIVITIES PASS',len(runs),'commands',flush=True)

if __name__=='__main__':main()

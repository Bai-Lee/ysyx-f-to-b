"""Modify the actual exercise7 variable, retaining the rest of its example."""
from pathlib import Path
import sys,re,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evidence import *
from lct_early import SOLUTION,BIN,lp

def main():
    base=(SOLUTION/'ex7.c').read_text('utf8')
    original='long universe_of_defects = 1L * 1024L * 1024L * 1024L;'
    assert base.count(original)==1
    runs=[];observations=[]
    for name,decl,expected in [
        ('one','long universe_of_defects = 1L;',1),
        ('thousand','long universe_of_defects = 1024L;',1024),
        ('long_max','long universe_of_defects = LONG_MAX;',9223372036854775807),
        ('long_too_large','long universe_of_defects = 9223372036854775808L;',None),
        ('ulong_too_large','unsigned long universe_of_defects = 18446744073709551616UL;',None)]:
        text='#include <limits.h>\n'+base.replace(original,decl)
        # The original expression already converts long to double; make its
        # intended (possibly rounded) floating division explicit for -Wconversion.
        text=text.replace('expected_bugs / universe_of_defects','expected_bugs / (double)universe_of_defects')
        if name.startswith('ulong'):text=text.replace('%ld bugs.','%lu bugs.')
        src=SOLUTION/('ex7_'+name+'.c');src.write_text(text,encoding='utf8',newline='\n');exe=BIN/('ex7_'+name+'.elf')
        flags=['-std=c17','-Wall','-Wconversion','-O0','-g']
        if expected is not None:flags.append('-Werror')
        q=run('E3/lcthw/literals/'+name+'/compile',['wsl.exe','-d','YSYX-Linux','-u','ysyx','--exec','gcc',*flags,lp(src),'-o',lp(exe)],[src],timeout=30);assert q['status']=='PASS';runs.append(q)
        warning=(ROOT/'artifacts/E3/lcthw/literals'/name/'compile/stderr.log').read_text('utf8')
        if expected is None:assert 'warning:' in warning
        args=[lp(exe)]
        if expected is not None:args=['valgrind','--error-exitcode=99',*args]
        r=run('E3/lcthw/literals/'+name+'/run',['wsl.exe','-d','YSYX-Linux','-u','ysyx','--exec',*args],[src,exe],timeout=30);assert r['status']=='PASS';runs.append(r)
        output=(ROOT/'artifacts/E3/lcthw/literals'/name/'run/stdout.log').read_text('utf8')
        match=re.search(r'The entire universe has (-?\d+) bugs\.',output);assert match
        if expected is not None:
            assert int(match[1])==expected
            assert 'ERROR SUMMARY: 0 errors' in (ROOT/'artifacts/E3/lcthw/literals'/name/'run/stderr.log').read_text('utf8')
        observations.append({'name':name,'printed_universe':int(match[1]),'stdout':output,'kind':'defined_value_check' if expected is not None else 'out_of_range_compiler_extension_observation'})
    dump(ROOT/'reports/E3_LCT_literals.json',{'status':'PASS','runs':runs,'observations':observations,'scope':'LCT-07-X01/X02/X03; out-of-range examples are observed diagnostics/results, not portable correct C.'})
    print('E3_EX7_LITERAL_VARIANTS PASS',len(observations),flush=True)

if __name__=='__main__':main()

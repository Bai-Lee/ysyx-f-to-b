"""Execute the small LCTHW0-9 examples; original snippets remain unchanged."""
from pathlib import Path
import sys,json,re,shutil,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evidence import *

BASE=ROOT/'E/E3/lcthw'
SOLUTION=BASE/'solutions/early'
BIN=ROOT/'artifacts/E3/lcthw/early/bin'
SPEC=json.loads((ROOT/'E/E3/course_specs.json').read_text('utf8'))
CHAPTERS={r['chapter']:r for r in SPEC['chapters']}

def lp(p):
    p=Path(p).resolve()
    assert p.drive.lower()=='d:'
    return '/mnt/d'+p.as_posix()[2:]

def original(ch,idx=0):
    row=next(b for b in CHAPTERS[ch]['blocks'] if b['index']==idx)
    p=Path(row['path']);assert sha(p)==row['sha256']
    return p

def write(name,text):
    p=SOLUTION/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    SOLUTION.mkdir(parents=True,exist_ok=True);BIN.mkdir(parents=True,exist_ok=True)
    cases=[];observations=[]
    reuse_count=0
    def linux(name,args,inputs=(),expected=0,timeout=35,contains=None,err_contains=None,exact=None):
        nonlocal reuse_count
        command=['wsl.exe','-d','YSYX-Linux','-u','ysyx','--exec','env','LC_ALL=C',*map(str,args)]
        folder=ROOT/'artifacts/E3/lcthw/early'/name;cached=False;q=None
        if '--resume' in sys.argv and (folder/'run.json').exists():
            prior=json.loads((folder/'run.json').read_text('utf8'))
            cached=prior['status']=='PASS' and prior['command']==command and prior['expected_exit']==expected and all(Path(x['path']).exists() and sha(x['path'])==x['sha256'] for x in prior['inputs']) and all(sha(folder/(s+'.log'))==prior[s+'_sha256'] for s in ('stdout','stderr'))
            if cached and name.endswith('/compile') and expected==0:
                exe=Path('D:'+str(args[-1])[6:]);known=[]
                for next_step in ('execute','valgrind'):
                    candidate=folder.parent/next_step/'run.json'
                    if candidate.exists():known += [v['sha256'] for v in json.loads(candidate.read_text('utf8'))['inputs'] if v['path']==str(exe)]
                cached=exe.exists() and sha(exe) in known
            if cached:q=prior;reuse_count+=1
        if not cached:q=run('E3/lcthw/early/'+name,command,inputs,timeout=timeout,expected=expected)
        assert q['status']=='PASS',name
        folder=ROOT/'artifacts/E3/lcthw/early'/name
        out=(folder/'stdout.log').read_bytes();err=(folder/'stderr.log').read_text('utf8',errors='replace')
        if contains:assert contains in out.decode('utf8',errors='replace'),(name,out)
        if err_contains:assert err_contains in err,(name,err)
        if exact is not None:assert out==exact.encode('utf8'),(name,repr(out),repr(exact))
        cases.append({'name':name,'status':'PASS','reused_unchanged_evidence':cached,'execution':q})
        dump(ROOT/'reports/E3_LCT_early_results.json',{'status':'IN_PROGRESS','cases':cases,'undefined_behavior_observations':observations})
        return out,err
    def compile_(name,src,strict=False,sanitize=False,expected=0):
        exe=BIN/(name+'.elf');flags=['-std=c17','-Wall','-O0','-g']
        if strict:flags+=['-Werror']
        if sanitize:flags+=['-fsanitize=address,undefined','-fno-sanitize-recover=all','-fno-omit-frame-pointer']
        out,err=linux(name+'/compile',['gcc',*flags,lp(src),'-o',lp(exe)],[src],expected=expected)
        return exe,err
    def execute(name,exe,src,exact=None,vg=False,bad=False,sanitized=False):
        args=[lp(exe)];expected=0
        if vg:
            args=['valgrind','--error-exitcode=99','--track-origins=yes','--leak-check=full',*args]
            if bad:expected=[0,99,11,139]
        elif sanitized:expected=[1,11,139]
        elif bad:expected=[0,1,2,11,126,139]
        out,err=linux(name+('/valgrind' if vg else '/execute'),args,[src,exe],expected=expected,exact=exact,timeout=35)
        if vg and not bad:assert 'ERROR SUMMARY: 0 errors' in err
        if vg and cases[-1]['execution']['exit_code'] in (11,139):assert 'SIGSEGV' in err
        if vg and bad:observations.append({'name':name,'valgrind_reported_error':not bool(re.search(r'ERROR SUMMARY:\s+0 errors',err)),'scope':'Observation of a deliberately undefined program, not a correctness verdict.'})
        if sanitized:assert ('AddressSanitizer' in err and ('buffer-overflow' in err or 'SEGV' in err)) or 'runtime error:' in err
        return out,err

    expected={
      1:'Hello world.\n',3:'I am 10 years old.\nI am 72 inches tall.\n',
      5:'You are 100 miles away.\n',
      6:'You are 100 miles away.\nYou have 2.345000 levels of power.\nYou have 56789.453200 awesome super powers.\nI have an initial A.\nI have a first name Zed.\nI have a last name Shaw.\nMy whole name is Zed A. Shaw.\n',
      7:'You have 100 bugs at the imaginary rate of 1.200000.\nThe entire universe has 1073741824 bugs.\nYou are expected to have 120.000000 bugs.\nThat is only a 1.117587e-07 portion of the universe.\nWhich means you should care 0%.\n',
      8:'The size of an int: 4\nThe size of areas (int[]): 20\nThe number of ints in areas: 5\nThe first area is 10, the 2nd 12.\nThe size of a char: 1\nThe size of name (char[]): 4\nThe number of chars: 4\nThe size of full_name (char[]): 12\nThe number of chars: 12\nname="Zed" and full_name="Zed A. Shaw"\n',
      9:'numbers: 0 0 0 0\nname each: a \0 \0 \0\nname: a\nnumbers: 1 2 3 4\nname each: Z e d \0\nname: Zed\nanother: Zed\nanother each: Z e d \0\n'}
    fixed={}
    for ch in (1,3,5,6,7,8,9):
        src=original(ch)
        exe,err=compile_(f'ex{ch}_original',src,expected=1 if ch==6 else 0)
        if ch==6:assert 'error:' in err
        else:execute(f'ex{ch}_original',exe,src,exact=expected[ch])
        text=src.read_text('utf8')
        if ch in (1,7):text='#include <stdio.h>\n'+text
        if ch==6:assert text.startswith('include <stdio.h>');text='#'+text
        if ch==8:text=text.replace('%ld','%zu')
        repair=write(f'ex{ch}.c',text);fixed[ch]=repair
        exe,err=compile_(f'ex{ch}_defined',repair,strict=True)
        assert 'warning:' not in err
        execute(f'ex{ch}_defined',exe,repair,exact=expected[ch],vg=True)

    src=original(4,1);exe,err=compile_('ex4_original_bad',src)
    assert 'warning:' in err
    out,err=execute('ex4_original_bad',exe,src,vg=True,bad=True)
    assert 'uninitialised' in err
    text=src.read_text('utf8').replace('int height;','int height = 72;').replace('printf("I am %d years old.\\n");','printf("I am %d years old.\\n", age);')
    src4=write('ex4_fixed.c',text);exe,err=compile_('ex4_fixed',src4,strict=True)
    execute('ex4_fixed',exe,src4,exact=expected[3],vg=True)

    # Compile diagnostics and real runtime observations for deliberate printf bugs.
    mutations=[
      ('ex3_missing_argument',3,'printf("I am %d years old.\\n", age);','printf("I am %d years old.\\n");'),
      ('ex3_uninitialized_age',3,'int age = 10;','int age;'),
      ('ex3_wrong_pointer',3,'printf("I am %d years old.\\n", age);','printf("I am %s years old.\\n", age);'),
      ('ex6_wrong_argument_order',6,'first_name, initial, last_name','initial, first_name, last_name'),
      ('ex6_integer_as_pointer',6,'printf("I have a first name %s.\\n", first_name);','printf("I have a first name %s.\\n", distance);'),
      ('ex7_nul_as_pointer',7,'printf("Which means you should care %d%%.\\n",','printf("Which means you should care %s%%.\\n",'),
      ('ex9_uninitialized_array',9,"char name[4] = {'a'};","char name[4];")]
    for name,ch,old,new in mutations:
        text=fixed[ch].read_text('utf8');assert text.count(old)==1,name
        src=write(name+'.c',text.replace(old,new));exe,err=compile_(name,src)
        if name!='ex9_uninitialized_array':assert 'warning:' in err,name
        out,runtime_err=execute(name,exe,src,vg=True,bad=True)
        if name=='ex9_uninitialized_array':assert 'uninitialised' in runtime_err

    # Stack/global boundary errors may be invisible to Memcheck; ASan provides a second check.
    text8=fixed[8].read_text('utf8')
    nozero=text8.replace("'S', 'h', 'a', 'w', '\\0'","'S', 'h', 'a', 'w'")
    assert nozero!=text8
    match=re.search(r'    char full_name\[\] = \{.*?    \};\n',nozero,re.S);assert match
    global_nozero=nozero[:match.start()]+nozero[match.end():]
    global_nozero=global_nozero.replace('int main',match[0].strip()+'\n\nint main',1)
    bounds=[('ex8_no_terminator_stack',nozero),('ex8_no_terminator_global',global_nozero),('ex8_bad_index',text8.replace('areas[0], areas[1]','areas[10], areas[1]')),
            ('ex9_overwritten_terminator',fixed[9].read_text('utf8').replace("name[3] = '\\0';","name[3] = 'A';")),
            ('ex9_full_initializer',fixed[9].read_text('utf8').replace("char name[4] = {'a'};","char name[4] = {'a','a','a','a'};"))]
    for name,text in bounds:
        src=write(name+'.c',text);exe,err=compile_(name,src);execute(name,exe,src,vg=True,bad=True)
        instrumented,err=compile_(name+'_asan',src,sanitize=True);execute(name+'_asan',instrumented,src,sanitized=True)

    # A literal pointer is not a modifiable character array.
    text=fixed[9].read_text('utf8').replace("char name[4] = {'a'};",'char *name = "a";')
    src=write('ex9_literal_not_modifiable.c',text);exe,err=compile_('ex9_literal_not_modifiable',src)
    out,err=execute('ex9_literal_not_modifiable',exe,src,vg=True,bad=True)
    assert 'SIGSEGV' in err or 'Bad permissions' in err
    text=fixed[9].read_text('utf8').replace("char name[4] = {'a'};","char *name = (char[4]){'a',0,0,0};")
    src=write('ex9_modifiable_pointer.c',text);exe,err=compile_('ex9_modifiable_pointer',src,strict=True)
    execute('ex9_modifiable_pointer',exe,src,vg=True,exact=expected[9])

    # Extra printing and an ELF-header corruption of a COPY, not the good binary.
    text=fixed[1].read_text('utf8').replace('    return 0;','    puts("line 1"); puts("line 2"); puts("line 3"); puts("line 4"); puts("line 5");\n    return 0;')
    src=write('ex1_more_lines.c',text);exe,err=compile_('ex1_more_lines',src,strict=True)
    execute('ex1_more_lines',exe,src,exact=expected[1]+''.join(f'line {i}\n' for i in range(1,6)))
    bad=BIN/'ex1_corrupted.elf';data=bytearray(exe.read_bytes());rng=random.Random(260703);offset=rng.randrange(4);data[offset]^=255;bad.write_bytes(data)
    linux('ex1_corrupted',['bash','-c',lp(bad)],[exe,bad],expected=[2,126],err_contains='cannot execute binary file')

    # Actual man pages are stored as stdout logs, not merely named in a checklist.
    for name,section,page in [('puts','3','puts'),('printf','3','printf'),('make','1','make'),('gcc','1','gcc'),('cc','1','cc')]:
        out,err=linux('man_'+name,['man','-P','cat',section,page],contains={'puts':'puts','printf':'printf','make':'make','gcc':'-Wall','cc':'-g'}[name],timeout=45)

    # Real default Make target, clean/rebuild, and an invalid-recipe negative control.
    work=ROOT/'artifacts/E3/lcthw/early/make_lab';work.mkdir(exist_ok=True)
    for ch in (1,3):shutil.copyfile(fixed[ch],work/f'ex{ch}.c')
    mk=work/'Makefile';mk.write_text('CC=cc\nCFLAGS=-Wall -g\nPROGRAMS=ex1 ex3\n.PHONY: all clean\nall: $(PROGRAMS)\nclean:\n\trm -f $(PROGRAMS)\n',encoding='utf8',newline='\n')
    inputs=[mk,work/'ex1.c',work/'ex3.c']
    linux('make_default',['make','-C',lp(work),'-j1'],inputs)
    linux('make_ex1_run',[lp(work/'ex1')],inputs+[work/'ex1'],exact=expected[1])
    linux('make_ex3_run',[lp(work/'ex3')],inputs+[work/'ex3'],exact=expected[3])
    broken=work/'Makefile.bad';broken.write_text(mk.read_text('utf8').replace('\trm -f','rm -f'),encoding='utf8',newline='\n')
    linux('make_missing_tab',['make','-C',lp(work),'-f','Makefile.bad','clean'],[broken],expected=2,err_contains='missing separator')
    linux('make_clean',['make','-C',lp(work),'clean'],inputs)
    assert not (work/'ex1').exists() and not (work/'ex3').exists()
    linux('make_rebuild',['make','-C',lp(work),'-j1','all'],inputs)
    assert (work/'ex1').exists() and (work/'ex3').exists()

    result={'status':'PASS_TEST_BATCH_NOT_WHOLE_CHAPTER_COMPLETION','scope':'Small original/fixed programs and selected break/extra activities from LCTHW0-9. Missing research/source-build/remaining extras are not auto-marked complete.','cases':cases,'undefined_behavior_observations':observations,'original_source_preserved':True,'light_only':True,'timestamp':datetime.now(timezone.utc).isoformat()}
    dump(ROOT/'reports/E3_LCT_early_results.json',result)
    print('E3_LCT_EARLY_BATCH PASS',len(cases),'validated command records;',reuse_count,'reused unchanged in this debugging session; chapter completion not yet asserted',flush=True)

if __name__=='__main__':main()

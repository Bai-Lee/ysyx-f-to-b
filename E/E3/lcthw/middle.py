from native import *
import string,errno,subprocess,shlex
def main():
    states=['California','Oregon','Washington','Texas'];names=['Alan','Frank','Mary','John','Lisa'];ages=[23,43,12,89,2]
    executables={}
    for ch in range(10,17):
        exe,_,_=build('ex'+str(ch)+'_original',block(ch));executables[ch]=exe
        args=['hello','A 12\tZ'] if ch in (10,11,14) else ['abcdeAEIOUyYyyyy123'] if ch==13 else []
        o,e,r=execute('ex'+str(ch)+'_original',exe,args,vg=True);assert 'ERROR SUMMARY: 0 errors' in e
        if ch in (10,11):
            expected=''.join(f'arg {i}: {v}\n' for i,v in enumerate([str(exe)]+args) if i or ch==11)+''.join(f'state {i}: {v}\n' for i,v in enumerate(states));assert o==expected
        elif ch==12:assert o=='You only have one argument. You suck.\n'
        elif ch==13:
            lines=[]
            for i,c in enumerate(args[0]):
                if c.lower() in 'aeiou':lines.append(f"{i}: '{c.upper()}'")
                elif c.lower()=='y':
                    if i>2:lines.append(f"{i}: 'Y'")
                else:lines.append(f'{i}: {c} is not a vowel')
            assert o.splitlines()==lines
        elif ch==14:
            expected=''.join(''.join(f"'{c}' == {ord(c)} " for c in v if c in string.ascii_letters+' \t')+'\n' for v in [str(exe)]+args);assert o==expected
        elif ch==15:
            matches=re.findall(r'(Alan|Frank|Mary|John|Lisa) (?:has|is|lived) (\d+)',o);assert matches==list(zip(names,map(str,ages)))*4
        else:
            assert re.findall(r'Name: (.*)',o)==['Joe Alex','Frank Blank']*2
            assert list(map(int,re.findall(r'Age: (\d+)',o)))==[32,20,52,40]
            assert list(map(int,re.findall(r'Height: (\d+)',o)))==[64,72,62,72]
            assert list(map(int,re.findall(r'Weight: (\d+)',o)))==[140,180,180,200]
        verdict([f'LCT-{ch:02}-BASE'],'PASS',[f'ex{ch}_original'],'Original code compiled and run in Linux; output checked independently, Memcheck0 errors. POSIX strdup is compiled in GNU17 mode.')
    # Argument boundaries and alternate language, including actual OS exec limit.
    py=write('ex10_python.py','import sys\nfor i,v in enumerate(sys.argv[1:],1):print(f"arg {i}: {v}")\nfor i,v in enumerate(["California","Oregon","Washington","Texas"]):print(f"state {i}: {v}")\n')
    o,_,_=execute('ex10_many',executables[10],['x']*10000);assert 'arg 10000: x\n' in o
    alt,_,_=run('ex10_python',['python3',str(py),*(['x']*10000)],inputs=[py]);assert alt==o
    try:subprocess.run([str(executables[10]),'x'*140000],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    except OSError as err:assert err.errno==errno.E2BIG;dump(common.OUT/'ex10_exec_limit.json',{'errno':err.errno,'meaning':'OS rejected oversized single argument before program execution, not a program crash.'})
    else:raise AssertionError('Expected Linux per-argument limit')
    variants=[(10,'for(i = 1;','for(i = 0;'),
              (11,'i = 0;  // watch for this','/* deliberately keep previous i */')]
    for ch,old,new in variants:
        text=block(ch).replace(old,new);exe,_,_=build(f'ex{ch}_index_variant',text)
        o,_,_=execute(f'ex{ch}_index_variant',exe,['a','b','c','d'])
        if ch==10:assert 'arg 0: '+str(exe) in o
        else:assert 'state 0:' not in o # i==argc>=4, so second loop skipped.
    exe,_,_=build('ex10_bad_count',block(10).replace('num_states = 4','num_states = 8'),flags=['-fsanitize=address,undefined','-fno-sanitize-recover=all'])
    o,e,r=execute('ex10_bad_count',exe,expected=(1,-11));assert 'buffer-overflow' in e or 'out of bounds' in e
    exe,_,_=build('ex11_uninitialized',block(11).replace('int i = 0;','int i;'))
    o,e,r=execute('ex11_uninitialized',exe,expected=(0,99,-11),vg=True);assert 'uninitialised' in e
    exe,_,_=build('ex11_no_progress',block(11).replace('        i++;','        /* no progress */',1))
    o,e,r=shell('ex11_bounded_nontermination',f'timeout 0.2s {shlex.quote(str(exe))} > /dev/null\n',expected=(124,),timeout=5)
    dump(common.OUT/'ex11_nontermination_note.json',{'inner_result':'TIMEOUT','proof':'i=0 remains invariant, argc>=1, first while condition stays true. Timeout alone is not a proof or correct-program PASS.'})
    verdict(['LCT-10-BREAK','LCT-11-BREAK'],'PASS',['ex10_many','ex10_python','ex10_exec_limit.json','ex10_bad_count','ex11_uninitialized','ex11_bounded_nontermination','ex11_nontermination_note.json'],'Real failures/observations retained; oversized argv is OS E2BIG. Nontermination has static invariant explanation and separately labeled timeout.')
    # Branch boundaries, altered Boolean condition, omitted else, correct user argument wording.
    for n in (0,1,2,3,8):
        o,_,_=execute(f'ex12_argc_{n}',executables[12],['x']*n)
        assert ('only have one' in o if n==0 else "Here's your arguments" in o if n<3 else 'too many' in o)
    text=block(12).replace('argc > 1 && argc < 4','argc > 1 || argc < 4')
    exe,_,_=build('ex12_or_fault',text);o,_,_=execute('ex12_or_fault',exe,['x']*5);assert 'too many' not in o and "Here's" in o
    text=block(12).replace('    } else {\n        printf("You have too many arguments. You suck.\\n");\n','')
    # Remove the complete final else without changing braces in other branches.
    text=block(12).replace(' else {\n        printf("You have too many arguments. You suck.\\n");\n    }','')
    exe,_,_=build('ex12_missing_else',text);o,_,_=execute('ex12_missing_else',exe,['x']*5);assert o==''
    fixed=block(12).replace('You only have one argument. You suck.','No user arguments: argv[0] is the executable.').replace('for(i = 0; i < argc;','for(i = 1; i < argc;')
    exe,_,_=build('ex12_correct_message',fixed,strict=True);o,_,_=execute('ex12_correct_message',exe);assert 'No user arguments' in o
    verdict(['LCT-12-BREAK','LCT-12-X02','LCT-12-X04'],'PASS',['ex12_or_fault','ex12_missing_else','ex12_correct_message'],'Argument-count boundaries tested; wrong branch coverage is a logic error even without a crash; corrected argv0 wording.')
    # Y fall-through is observed at positions0..3, no guessed switch behavior.
    text=block(13).replace('printf("%d: \'Y\'\\n", i);\n                }\n                break;','printf("%d: \'Y\'\\n", i);\n                    break;\n                }')
    exe,_,_=build('ex13_y_break_inside',text)
    original,_,_=execute('ex13_y_original',executables[13],['yyyY']);changed,_,_=execute('ex13_y_changed',exe,['yyyY'])
    assert original=="3: 'Y'\n" and changed.count('not a vowel')==3 and "3: 'Y'" in changed
    no_break=block(13).replace('                break;','                /* fall through */',1)
    exe,_,_=build('ex13_no_break',no_break);o,_,_=execute('ex13_no_break',exe,['a']);assert "'A'" in o and "'E'" in o
    verdict(['LCT-13-BREAK','LCT-13-X05'],'PASS',['ex13_no_break','ex13_y_original','ex13_y_changed'],'Actual fall-through experiments including Y with break inside/outside if.')
    text=block(14).replace('int can_print_it(char ch);','').replace('void print_letters(char arg[]);','')
    _,o,e=build('ex14_no_declarations',text,strict=True,expected=(1,));assert 'implicit declaration' in e
    exe,_,_=build('ex14_overrun_argv',block(14).replace('print_arguments(argc, argv);','print_arguments(argc+1, argv);'),flags=['-fsanitize=address,undefined','-fno-sanitize-recover=all'])
    o,e,r=execute('ex14_overrun_argv',exe,expected=(1,-11));assert 'runtime error:' in e or 'AddressSanitizer' in e
    for page in ('isalpha','isblank'):run('ex14_man_'+page,['man','-P','cat','3',page])
    verdict(['LCT-14-BREAK'],'PASS',['ex14_no_declarations','ex14_overrun_argv'],'Removed prototypes diagnosed by compiler; argv[argc] is NULL and argc+1 eventually dereferences it.')
    exe,_,_=build('ex15_wrong_type',block(15).replace('int *cur_age = ages;','int *cur_age = (int *)names;'))
    o,_,_=execute('ex15_wrong_type',exe);assert re.findall(r'(Alan|Frank|Mary|John|Lisa) (?:has|is|lived) (\d+)',o)!=list(zip(names,map(str,ages)))*4
    exe,_,_=build('ex15_wrong_bounds',block(15).replace('(cur_age - ages) < count','(cur_age - ages) <= count'),flags=['-fsanitize=address,undefined','-fno-sanitize-recover=all'])
    o,e,r=execute('ex15_wrong_bounds',exe,expected=(1,-11));assert 'buffer-overflow' in e
    verdict(['LCT-15-BREAK'],'PASS',['ex15_wrong_type','ex15_wrong_bounds'],'Wrong object type changes values; one-past-end dereference caught by ASan. Reverse traversal is separately implemented without forming before-begin pointers.')
    for name,text in [('null_destroy',block(16).replace('Person_destroy(joe);','Person_destroy(NULL);')),
                      ('no_destroy',block(16).replace('    Person_destroy(joe);','').replace('    Person_destroy(frank);','')),
                      ('name_leak',block(16).replace('    free(who->name);','')),
                      ('null_print',block(16).replace('Person_print(joe);','Person_print(NULL);',1))]:
        exe,_,_=build('ex16_'+name,text)
        o,e,r=execute('ex16_'+name,exe,vg=True,expected=(-6,-11,99))
        if 'leak' in name or name=='no_destroy':assert re.search(r'definitely lost:\s+[1-9]',e)
        if name=='null_destroy':assert 'Assertion' in e
        if name=='null_print':assert 'Invalid read' in e
    verdict(['LCT-16-BREAK'],'PASS',['ex16_null_destroy','ex16_no_destroy','ex16_name_leak','ex16_null_print'],'Real assert failure, whole-object leaks, name-only leaks and invalid read. -g is not the assertion-enable switch; NDEBUG controls assertions.')
    print('LCT_MIDDLE_BASE_AND_BREAK_DONE',flush=True)
if __name__=='__main__':main()

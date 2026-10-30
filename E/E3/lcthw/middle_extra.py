from native import *
def main():
    src=SRC/'middle_extensions.c';exe,_,_=build('middle_extensions',files=[src],strict=True)
    for n in (0,1,4,12):
        args=['AEIOUyyyY abc123']*n
        o,e,r=execute('middle_extensions_'+str(n),exe,args,vg=True)
        assert 'PASS middle extensions' in o and 'ERROR SUMMARY: 0 errors' in e
        actual=re.findall(r'vowel:(\d+):(\d+):(.)',o)
        expected=[(str(k),str(i),c.lower() if c.lower() in 'aeiou' or c.lower()=='y' and i>2 else '-') for k,arg in enumerate(args,1) for i,c in enumerate(arg)]
        assert actual==expected
        for method in range(4):
            matches=re.findall(f'method{method}:([^:]+):(\\d+)',o)
            assert matches==list(zip(['Alan','Frank','Mary','John','Lisa'],['23','43','12','89','2']))
        assert re.findall(r'reverse-age:(\d+)',o)==['2','89','12','43','23']
        assert 'char:65\nchar:90\n' in o # Length-controlled routine crossed embedded NUL.
        pairs=re.findall(r'address:(0x[0-9a-f]+):(0x[0-9a-f]+)',o);assert len(pairs)==5 and all(a==b for a,b in pairs)
        assert [int(a,16)-int(pairs[0][0],16) for a,b in pairs]==[0,4,8,12,16]
        assert 'stack:Stack Joe:32:62:140' in o
    null=block(10).replace('"California", "Oregon",','"California", NULL,')
    exe,_,_=build('ex10_null',null);o,e,r=execute('ex10_null',exe,vg=True,expected=(0,99,-11));assert 'state 1:' in o or 'SIGSEGV' in e
    dump(common.OUT/'ex10_null_observation.json',{'stdout':o,'exit_code':r['exit_code'],'meaning':'NULL is a null pointer constant; %s requires a valid terminated string. Observed glibc behavior is not a portable C guarantee.'})
    ids=[f'LCT-10-X{i:02}' for i in range(1,5)]+[f'LCT-11-X{i:02}' for i in range(1,5)]+['LCT-12-X01','LCT-12-X03']+[f'LCT-13-X{i:02}' for i in range(1,5)]+[f'LCT-14-X{i:02}' for i in range(1,4)]+[f'LCT-15-X{i:02}' for i in range(1,9)]+[f'LCT-16-X{i:02}' for i in range(1,4)]
    verdict(ids,'PASS',['middle_extensions_0','middle_extensions_1','middle_extensions_4','middle_extensions_12','ex10_null_observation.json'],'Native assertions and independent output/stride oracle cover comma-loop sequencing, short circuit, bounded shallow copies, reverse traversal, switch/if equivalents, fixed-length functions including embedded NUL, all four pointer/index forms, and by-value stack structs. Notes explain applicable scope.')
    print('MIDDLE_EXTENSIONS_PASS',len(ids),flush=True)
if __name__=='__main__':main()

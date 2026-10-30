from native import *
import struct,random,os
def main():
    stack=write('stack.c',r'''#include <stdio.h>
int main(void){int a[8],n=0,v;char op;while(scanf(" %c",&op)==1){if(op=='+'){if(scanf("%d",&v)!=1)return 2;if(n==8)puts("FULL");else{a[n++]=v;puts("OK");}}else if(op=='-'){if(!n)puts("EMPTY");else printf("%d\n",a[--n]);}else return 2;}return 0;}
''')
    exe,_,_=build('stack',files=[stack],strict=True)
    class Stack:
        def __init__(self):self.values=[]
        def push(self,v):
            if len(self.values)==8:return 'FULL'
            self.values.append(v);return 'OK'
        def pop(self):return str(self.values.pop()) if self.values else 'EMPTY'
    model=Stack();rng=random.Random(260717);commands=[];expected=[]
    for k in range(2000):
        if (k<12 or rng.randrange(2)):
            value=rng.randrange(-1000,1001);commands.append('+ '+str(value));expected.append(model.push(value))
        else:commands.append('-');expected.append(model.pop())
    o,e,r=execute('stack',exe,vg=True,stdin='\n'.join(commands)+'\n');assert o.splitlines()==expected and 'ERROR SUMMARY: 0 errors' in e
    verdict(['LCT-17-X08'],'PASS',['stack'],'Independent Python and C capacity8 stacks agree on2000 operations including full and empty; data-structure stack is distinct from call-stack memory.')
    original,_,_=build('ex18_original',block(18,2))
    o,e,r=execute('ex18_original',original,['4','1','7','3','2','0','8'],vg=True)
    assert o.splitlines()==['0 1 2 3 4 7 8 ','8 7 4 3 2 1 0 ','3 4 2 7 1 0 8 '] and 'ERROR SUMMARY: 0 errors' in e
    verdict(['LCT-18-BASE'],'PASS',['ex18_original'],'All three printed rows match the archived worked example. strange_order is not a general strict ordering; it is not described as a valid universal comparator.')
    text=block(18,2).replace('    free(sorted);',r'''    free(sorted);
    unsigned char *data=(unsigned char *)cmp;
    printf("CODE:");for(i=0;i<25;i++)printf("%02x:",data[i]);printf("\n");
''')
    code,_,_=build('ex18_codebytes',text)
    o,e,r=execute('ex18_codebytes',code,['4','1','7','3','2','0','8'])
    lines=[bytes.fromhex(x.replace(':','')) for x in re.findall(r'^CODE:(.*)$',o,re.M)]
    raw=code.read_bytes();assert raw[:6]==b'\x7fELF\x02\x01'
    shoff=struct.unpack_from('<Q',raw,40)[0];ents,nsh=struct.unpack_from('<HH',raw,58)
    sections=[struct.unpack_from('<IIQQQQIIQQ',raw,shoff+i*ents) for i in range(nsh)]
    symbols={}
    for sec in sections:
        if sec[1]!=2:continue
        strings=sections[sec[6]];names=raw[strings[4]:strings[4]+strings[5]]
        for off in range(sec[4],sec[4]+sec[5],sec[9]):
            nm,info,other,idx,val,size=struct.unpack_from('<IBBHQQ',raw,off)
            name=names[nm:].split(b'\0',1)[0].decode()
            if name in ('sorted_order','reverse_order','strange_order'):
                s=sections[idx];symbols[name]={'offset':s[4]+val-s[3],'size':size}
    for data,name in zip(lines,['sorted_order','reverse_order','strange_order']):
        info=symbols[name];assert data==raw[info['offset']:info['offset']+25]
        run('ex18_hex_'+name,['xxd','-g','1','-s',str(info['offset']),'-l','25',str(code)],inputs=[code])
    dump(common.OUT/'ex18_symbol_map.json',{'ELF64_little_endian':True,'symbols':symbols,'read_length':25,'scope':'Runtime code bytes match ELF offsets on this AMD64 ELF target;25bytes may include a following symbol, not claimed as complete function length.'})
    hexfile=write('ex18_modified.hex',raw.replace(b'USAGE: ex18',b'USAGE: EX18',1).hex())
    changed=BIN/'ex18_modified.elf';changed.write_bytes(b'')
    run('ex18_hex_edit',['xxd','-r','-p',str(hexfile),str(changed)],inputs=[hexfile])
    assert changed.read_bytes()==raw.replace(b'USAGE: ex18',b'USAGE: EX18',1)
    if not os.access(changed,os.X_OK):
        import shutil
        executable_copy=common.LAB/'ex18_modified.elf';shutil.copyfile(changed,executable_copy);executable_copy.chmod(0o755);changed=executable_copy
    o,e,r=execute('ex18_modified',changed,expected=(1,));assert 'USAGE: EX18' in o
    wrong=block(18,2).replace('test_sorting(numbers, count, sorted_order);','test_sorting(numbers, count, puts);')
    _,o,e=build('ex18_wrong_callback',wrong,strict=True,expected=(1,));assert 'incompatible' in e
    null=block(18,2).replace('test_sorting(numbers, count, sorted_order);','test_sorting(numbers, count, NULL);')
    null_exe,_,_=build('ex18_null_callback',null)
    o,e,r=execute('ex18_null_callback',null_exe,['2','1'],vg=True,expected=(-11,99));assert 'Invalid' in e or 'invalid' in e
    sort,_,_=build('sort_callbacks',files=[SRC/'sort_callbacks.c'],strict=True)
    o,e,r=execute('sort_callbacks',sort,vg=True);assert 'PASS 260' in o and 'ERROR SUMMARY: 0 errors' in e
    verdict(['LCT-18-BREAK']+[f'LCT-18-X{i:02}' for i in range(1,6)],'PASS',['ex18_symbol_map.json','ex18_hex_edit','ex18_modified','ex18_wrong_callback','ex18_null_callback','sort_callbacks'],'Actual code-byte inspection and binary-string edit; signature error/NULL call; bubble/insertion through sort and comparator callbacks checked against qsort for0..64 elements and both directions, including integer extrema without subtraction overflow.')
    print('FUNCTION_POINTERS_AND_STACK_DONE',flush=True)
if __name__=='__main__':main()

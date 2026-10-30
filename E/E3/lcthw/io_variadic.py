from native import *
import os
def main():
    d=SRC/'io';d.mkdir(exist_ok=True);(d/'dbg.h').write_text(block(20,0))
    src=d/'ex24.c';src.write_text(block(24));exe,_,_=build('ex24',files=[src])
    data='Alice\nSmith\n27\n2\n12.5\n'
    o,e,r=execute('ex24',exe,vg=True,stdin=data);assert 'Age: 27' in o and 'Eyes: Green' in o and 'Income: 12.500000' in o and 'ERROR SUMMARY: 0 errors' in e
    for name,input_ in [('bad_age','Alice\nSmith\nbad\n'),('bad_eye','Alice\nSmith\n27\n0\n'),('bad_float','Alice\nSmith\n27\n2\nbad\n')]:
        execute('ex24_'+name,exe,stdin=input_,expected=(255,))
    fixed,_,_=build('io_safe',files=[SRC/'io_safe.c'],strict=True)
    for name,input_,expected in [('valid',' A li ce \n Sm ith \n27\n2\n12.5\n','Alice|Smith|27|Green|12.500000\n'),('negative_age','A\nB\n-1\n5\n0\n','A|B|-1|Other|0.000000\n')]:
        o,e,r=execute('io_safe_'+name,fixed,stdin=input_,vg=True);assert o==expected and 'ERROR SUMMARY: 0 errors' in e
    for i,input_ in enumerate(['A\nB\n99999999999999999999\n2\n1\n','A\nB\n12junk\n2\n1\n','A\nB\n12\n9\n1\n','A\nB\n12\n2\nnan\n','A'*101+'\nB\n12\n2\n1\n','A\n']):
        o,e,r=execute('io_safe_bad'+str(i),fixed,stdin=input_,expected=(1,),vg=True);assert 'ERROR SUMMARY: 0 errors' in e
    scanf=d/'ex24_scanf.c';scanf.write_text(block(24).replace('fscanf(stdin,','scanf('))
    scanf_exe,_,_=build('ex24_scanf',files=[scanf]);oo,ee,rr=execute('ex24_scanf',scanf_exe,stdin=data)
    original_out=(common.OUT/'ex24/run/stdout.log').read_text();assert oo==original_out
    token,_,_=build('scanf_delimiter',r'''#include <stdio.h>
int main(void){char s[100];if(scanf("%50s",s)!=1)return 1;printf("%s|next=%d\n",s,getchar());return 0;}
''',strict=True)
    o,_,_=execute('scanf_delimiter',token,stdin='Alice\n');assert o=='Alice|next=10\n'
    # The width50 is safe for100 bytes; it leaves the delimiter rather than eating it.
    gets,_,_=build('gets_unsafe',r'''#include <stdio.h>
#include <stdlib.h>
extern char *gets(char *);
int main(void){char *p=malloc(16);if(!p)return 2;gets(p);free(p);return 0;}
''',flags=['-fstack-protector-all'])
    detected=False
    for i in range(8):
        sample=os.urandom(256)
        o,e,r=execute('gets_fuzz'+str(i),gets,stdin=sample,vg=True,expected=(0,99,-6,-11))
        if 'Invalid write' in e:detected=True;break
    assert detected
    badsrc=d/'ex24_bad_eyes.c';badsrc.write_text(block(24).replace('    check(you.eyes <= OTHER_EYES && you.eyes >= 0, "Do it right, that\'s not an option.");',''))
    bad,_,_=build('ex24_bad_eyes',files=[badsrc],flags=['-fsanitize=address,undefined','-fno-sanitize-recover=all'])
    o,e,r=execute('ex24_bad_eyes',bad,stdin='A\nB\n20\n1000\n1\n',expected=(1,-11));assert 'out of bounds' in e
    reader,_,_=build('bounded_file_reader',r'''#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int argc,char **argv){if(argc!=3)return 2;size_t cap=strtoul(argv[2],0,10);if(cap>1000000)return 2;unsigned char *a=malloc(cap+2);if(!a)return 2;a[0]=a[cap+1]=0xcc;if(!cap){free(a);return 1;}unsigned char *s=a+1;s[0]=0;FILE *f=fopen(argv[1],"rb");if(!f){free(a);return 1;}size_t n=0;char ch;while(n+1<cap&&fscanf(f,"%c",&ch)==1)s[n++]=(unsigned char)ch;s[n]=0;if(a[0]!=0xcc||a[cap+1]!=0xcc)return 3;for(size_t i=0;i<n;i++)printf("%02x",(unsigned)s[i]);printf("\n");fclose(f);free(a);return 0;}
''',strict=True)
    sample=common.LAB/'reader.bin';sample.write_bytes(bytes(range(32)))
    for cap in (0,1,2,8,33,100):
        o,e,r=execute('reader_'+str(cap),reader,[str(sample),str(cap)],expected=(1,) if cap==0 else (0,),vg=True)
        if cap:assert o.strip()==sample.read_bytes()[:cap-1].hex()
        assert 'ERROR SUMMARY: 0 errors' in e
    verdict(['LCT-24-BASE','LCT-24-BREAK']+[f'LCT-24-X{i:02}' for i in range(1,5)],'PASS',['ex24','io_safe_valid','io_safe_bad0','ex24_scanf','scanf_delimiter','gets_fuzz'+str(i),'ex24_bad_eyes','reader_100'],'Original input, strict line/strto conversion, whitespace removal and length-bounded file reading tested; original width50 is not an overflow and leaves newline. Unsafe gets is isolated with recorded urandom bytes; removed eye bounds triggers sanitizer.')
    source=d/'ex25.c';source.write_text(block(25));base,_,_=build('ex25_original',files=[source])
    input25='Alice\nQ\nSmith\n27\n'
    o,e,r=execute('ex25_original',base,stdin=input25,vg=True);assert 'Age: 27' in o and "Initial: 'Q'" in o and 'ERROR SUMMARY: 0 errors' in e
    # Missing vararg size remains a violated calling contract, not something va_arg can detect.
    wrong=d/'ex25_wrong_args.c';wrong.write_text(block(25).replace('read_scan("%s", MAX_DATA, &first_name)','read_scan("%s", &first_name)'))
    bad,_,_=build('ex25_wrong_args',files=[wrong])
    stdin_file=write('wrong_args_input.txt',input25)
    shell('ex25_wrong_args/run',f'ulimit -v 65536\nexec {bad} < {stdin_file}\n',expected=(1,255,-11,139),timeout=10)
    text=block(25)
    start=text.index('int read_string(');end=text.index('int read_scan(')
    functions=r'''int read_string(char **out_string,int max_buffer){
    *out_string=NULL;if(max_buffer<1||max_buffer>1000000)return -1;
    char *p=malloc((size_t)max_buffer+1);if(!p)return -1;
    int ch,overflow=0;size_t n=0;
    while((ch=fgetc(stdin))!=EOF&&ch!='\n'){if(ch==0)overflow=1;if(n<(size_t)max_buffer)p[n++]=(char)ch;else overflow=1;}
    p[n]=0;if(overflow||(ch==EOF&&n==0)){free(p);return -1;}*out_string=p;return 0;
}
int read_int(int *out_int){
    char *p=NULL,*end;int rc=read_string(&p,MAX_DATA);if(rc)return -1;
    errno=0;long v=strtol(p,&end,10);int bad=end==p||errno||v<INT_MIN||v>INT_MAX;
    while(isspace((unsigned char)*end)){end++;}
    if(*end)bad=1;
    if(!bad){*out_int=(int)v;}
    free(p);return bad?-1:0;
}
int tiny_print(const char *fmt,...){
    va_list ap;va_start(ap,fmt);int count=0;
    for(size_t i=0;fmt[i];i++){
        if(fmt[i]!='%'){if(putchar(fmt[i])==EOF){va_end(ap);return -1;}count++;continue;}
        i++;int rc=0;
        if(fmt[i]=='d')rc=printf("%d",va_arg(ap,int));
        else if(fmt[i]=='c')rc=printf("%c",va_arg(ap,int));
        else if(fmt[i]=='s'){char *s=va_arg(ap,char *);if(!s){va_end(ap);return -1;}rc=printf("%s",s);}
        else if(fmt[i]=='%'){putchar('%');rc=1;}
        else{va_end(ap);return -1;}
        if(rc<0){va_end(ap);return -1;}count+=rc;
    }
    va_end(ap);return count;
}
'''
    text=text[:start]+functions+text[end:];text='#include <limits.h>\n#include <ctype.h>\n'+text
    text=text.replace('*out_char = fgetc(stdin);','int input_char=fgetc(stdin);\n                    check(input_char!=EOF,"EOF reading character");\n                    *out_char=(char)input_char;')
    text=text.replace('            fgetc(stdin);','            int literal=fgetc(stdin);\n            check(literal==(unsigned char)fmt[i],"Literal mismatch");')
    text=text.replace('    rc = read_scan("%d", &age);','    rc = read_scan("%d", &age);\n    check(rc==0,"Failed age");')
    text=text.replace('printf("First Name: %s", first_name);','printf("First Name: %s\\n", first_name);').replace('printf("Last Name: %s", last_name);','printf("Last Name: %s\\n", last_name);')
    pos=text.index('int main(');text=text[:pos]+text[pos:].replace('printf(','tiny_print(').replace('error:\n    return -1;','error:\n    free(first_name);free(last_name);\n    return -1;')
    fixedsrc=d/'ex25_fixed.c';fixedsrc.write_text(text);fixed,_,_=build('ex25_fixed',files=[fixedsrc])
    o,e,r=execute('ex25_fixed',fixed,stdin=input25,vg=True);assert 'Age: 27' in o and 'First Name: Alice\n' in o and 'ERROR SUMMARY: 0 errors' in e
    for i,data in enumerate(['Alice\nQ\nSmith\nbad\n','Alice\n', 'x'*101+'\nQ\nSmith\n20\n','A\nQ\nB\n99999999999999999999\n']):
        o,e,r=execute('ex25_fixed_bad'+str(i),fixed,stdin=data,vg=True,expected=(255,));assert 'ERROR SUMMARY: 0 errors' in e and 'in use at exit: 0 bytes' in e
    run('ex25_man',['man','-P','cat','3','stdarg'])
    verdict(['LCT-25-BASE','LCT-25-BREAK']+[f'LCT-25-X{i:02}' for i in range(1,4)],'PASS',['ex25_original','ex25_wrong_args','ex25_fixed','ex25_fixed_bad0','ex25_man'],'Actual varargs example and violated-contract observation; derived malloc/fgetc line reader bounds and drains input, rejects numeric junk/overflow, checks EOF and literal separators, and cleans previous allocations. Own%d/%c/%s/%% formatter used by main; not claimed to implement all printf syntax.')
    print('IO_VARIADIC_DONE',flush=True)
if __name__=='__main__':main()

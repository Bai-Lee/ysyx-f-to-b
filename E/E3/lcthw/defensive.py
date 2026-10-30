from native import *
import shutil
def main():
    d=SRC/'defensive';d.mkdir(exist_ok=True);(d/'dbg.h').write_text(block(20,0))
    raw=d/'ex27_verbatim.c';raw.write_text(block(27))
    _,o,e=build('ex27_verbatim',files=[raw],expected=(1,));assert 'error:' in e
    fixed=d/'ex27_book.c';fixed.write_text('#'+block(27)) # Missing preprocessor '#' is preserved in original, repaired only in copy.
    exe,_,_=build('ex27_book',files=[fixed]);o,e,r=execute('ex27_book',exe,vg=True);assert 'ERROR SUMMARY: 0 errors' in e
    # A numeric check placed after subtraction is too late for INT_MIN capacity.
    trial=d/'ex27_overflow.c';trial.write_text('#include <limits.h>\n#define main original_main\n#include "ex27_book.c"\n#undef main\nint main(void){char from[3]={1,2,3},to[8];return safercopy(3,from,INT_MIN,to);}\n')
    bad,_,_=build('ex27_overflow',files=[trial],flags=['-fsanitize=undefined','-fno-sanitize-recover=all'])
    o,e,r=execute('ex27_overflow',bad,expected=(1,));assert 'signed integer overflow' in e
    gap=d/'ex27_gap.c';gap.write_text('#define main original_main\n#include "ex27_book.c"\n#undef main\nint main(void){char from[3]={\'a\',\'b\',\'c\'},to[8];safercopy(3,from,8,to);puts(to);return 0;}\n')
    bad,_,_=build('ex27_gap',files=[gap]);o,e,r=execute('ex27_gap',bad,vg=True,expected=(99,));assert 'uninitialised' in e
    source=write('defensive_copy.c',r'''#include <assert.h>
#include <limits.h>
#include <string.h>
#include <stdio.h>
/* Caller guarantees readable from_len bytes and writable to_len bytes. */
int bounded_copy(int from_len,const char *from,int to_len,char *to){
    if(from_len<0||to_len<=0||!to||(!from&&from_len))return -1;
    int n=from_len<to_len-1?from_len:to_len-1;
    if(n)memmove(to,from,(size_t)n);to[n]=0;return n;
}
int main(void){
    char input[32];for(int i=0;i<32;i++)input[i]=(char)('A'+i%26);
    for(int n=0;n<=16;n++)for(int cap=1;cap<=17;cap++){
        unsigned char box[32];memset(box,0xcc,sizeof box);
        int copied=bounded_copy(n,input,cap,(char*)box+1);int wanted=n<cap-1?n:cap-1;
        assert(copied==wanted&&box[0]==0xcc&&box[cap+1]==0xcc&&box[1+wanted]==0);
        assert(memcmp(box+1,input,(size_t)wanted)==0);
    }
    char out[8];assert(bounded_copy(3,input,INT_MIN,out)==-1);
    assert(bounded_copy(-1,input,8,out)==-1);assert(bounded_copy(1,NULL,8,out)==-1);
    assert(bounded_copy(0,NULL,8,out)==0&&out[0]==0);
    char overlap[16]="abcdef";assert(bounded_copy(6,overlap,7,overlap+1)==6);assert(strcmp(overlap+1,"abcdef")==0);
    puts("PASS bounded copy contracts");return 0;
}
''')
    good,_,_=build('defensive_copy',files=[source],flags=['-fsanitize=address,undefined','-fno-sanitize-recover=all'])
    o,e,r=execute('defensive_copy',good);assert 'PASS bounded copy contracts' in o
    verdict(['LCT-27-BASE','LCT-27-X01'],'PASS_ADAPTED',['ex27_verbatim','ex27_book','ex27_overflow','ex27_gap','defensive_copy'],'Original missing# repaired in copy; reviewed numeric overflow before validation and uninitialized output gap. Defined preconditions, overlap behavior, immediate terminator and automated boundary/negative tests. Raw original remains unchanged.')
    # Review an actual separate upstream tool; do not invent a vulnerability to publish.
    xxd=PROJECT/'artifacts/E3/xxd/build/xxd'
    data=common.LAB/'xxd_review.bin';data.write_bytes(bytes(range(64)))
    o,e,r=run('review/xxd_bound',[str(xxd),'-c','-1',str(data)],inputs=[xxd,data],expected=(1,))
    o,e,r=run('review/xxd_slice',[str(xxd),'-p','-s','7','-l','13',str(data)],inputs=[xxd,data]);assert ''.join(o.split())==data.read_bytes()[7:20].hex()
    run('review/xxd_missing',[str(xxd),str(data)+'.missing'],expected=(2,))
    verdict(['LCT-27-X02'],'PASS_REVIEW_NO_CONFIRMED_BUG',['review/xxd_bound','review/xxd_slice','review/xxd_missing','reports/E3_xxd_build.json'],'Reviewed pinned official xxd argument-size checks, input/output error paths and Makefile; exercised invalid columns, bounded slice and missing file. No confirmed new upstream bug in reviewed scope, so conditional patch-submission requirement did not arise.')
    print('DEFENSIVE_REVIEW_DONE',flush=True)
if __name__=='__main__':main()

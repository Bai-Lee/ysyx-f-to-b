#include <assert.h>
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

#include "semu.h"
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
int main(int argc,char**argv){
    if(argc!=4)return 2;
    char*end;errno=0;long cycles=strtol(argv[2],&end,10);
    if(errno||*end||cycles<1||cycles>1000000)return 2;
    if(strcmp(argv[3],"0")&&strcmp(argv[3],"1"))return 2;
    int mode=argv[3][0]-'0';
    uint8_t memory[256];if(semu_load(argv[1],memory))return 3;
    Semu s;semu_reset(&s,mode);
    for(long i=0;i<cycles;i++){uint8_t old=s.pc,ins=memory[s.pc];semu_step(&s,ins,0,0);
        printf("%ld,%u,%u,%u,%u,%u,%u,%u,%u,%u\n",i,old,ins,s.pc,s.r[0],s.r[1],s.r[2],s.r[3],s.led,s.display);}
    return 0;
}

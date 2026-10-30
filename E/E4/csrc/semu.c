#include "semu.h"
#include <stdio.h>
#include <string.h>
void semu_reset(Semu*s,int enhanced){memset(s,0,sizeof *s);s->enhanced=enhanced;}
void semu_step(Semu*s,uint8_t ins,uint8_t switches,uint8_t buttons){
    unsigned op=ins>>6,dst=(ins>>4)&3,left=(ins>>2)&3,right=ins&3;
    unsigned next=(unsigned)s->pc+1;
    switch(op){
    case 0:s->r[dst]=(uint8_t)((unsigned)s->r[left]+s->r[right]);break;
    case 1:
        if(s->enhanced){
            unsigned device=ins&7;
            if(ins&8){if(device==0)s->led=s->r[dst];else if(device==1)s->display=s->r[dst];}
            else s->r[dst]=device==0?switches:device==1?buttons:0;
        }break;
    case 2:s->r[dst]=s->enhanced?(uint8_t)((ins&3)<<(2*((ins>>2)&3))):(ins&15);break;
    case 3:
        if(s->r[0]!=s->r[right]){
            unsigned field=(ins>>2)&15;
            if(s->enhanced){int displacement=field<8?(int)field:(int)field-16;next=(unsigned)((int)s->pc+displacement);}
            else next=field;
        }break;
    }
    s->pc=(uint8_t)next;
}
int semu_load(const char*path,uint8_t memory[256]){
    FILE*f=fopen(path,"r");if(!f)return -1;unsigned value;size_t n=0;int rc;
    while((rc=fscanf(f,"%x",&value))==1){if(value>255||n>=256){fclose(f);return -1;}memory[n++]=(uint8_t)value;}
    int ok=(rc==EOF&&n==256);fclose(f);return ok?0:-1;
}

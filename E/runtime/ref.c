#include "ref.h"
#include <string.h>
void minirv_reset(MiniState*s,uint32_t pc){memset(s,0,sizeof(*s));s->pc=pc;}
static int32_t signed12(uint32_t value){return (int32_t)(value&2047u)-(int32_t)(value&2048u);}
int minirv_step(MiniState*s,MiniBus*bus,MiniEvent*e){
    memset(e,0,sizeof(*e));e->pc=s->pc;
    if(s->halted)return -1;
    if(s->pc%4){s->fault=2;return -1;}
    uint32_t ins;
    if(bus->read(bus->opaque,s->pc,4,0,&ins)){s->fault=4;return -1;}
    e->inst=ins;e->next_pc=s->pc+4u;
    unsigned opcode=ins&127u,rd=(ins>>7)&31u,funct3=(ins>>12)&7u,r1=(ins>>15)&31u,r2=(ins>>20)&31u;
    int32_t imm=signed12(ins>>20);uint32_t value=0;unsigned valid=0,uses1=0,uses2=0;
    if(ins==0x00100073u){s->halted=1;valid=1;}
    else if(opcode==0x13&&funct3==0){valid=1;uses1=1;e->regwrite=1;}
    else if(opcode==0x33&&funct3==0&&(ins>>25)==0){valid=1;uses1=uses2=1;e->regwrite=1;}
    else if(opcode==0x37){valid=1;e->regwrite=1;}
    else if(opcode==0x67&&funct3==0){valid=1;uses1=1;e->regwrite=1;}
    else if(opcode==0x03&&(funct3==2||funct3==4)){valid=1;uses1=1;e->regwrite=1;e->load=1;e->size=funct3==2?4:1;}
    else if(opcode==0x23&&(funct3==2||funct3==0)){valid=1;uses1=uses2=1;e->store=1;e->size=funct3==2?4:1;imm=signed12(((ins>>25)<<5)|((ins>>7)&31));}
    if(!valid||(e->regwrite&&rd>=16)||(uses1&&r1>=16)||(uses2&&r2>=16)){s->fault=1;return -1;}
    uint32_t a=uses1?s->r[r1]:0,b=uses2?s->r[r2]:0;
    switch(opcode){
    case 0x13:value=a+(uint32_t)imm;break;
    case 0x33:value=a+b;break;
    case 0x37:value=ins&0xfffff000u;break;
    case 0x67:e->next_pc=(a+(uint32_t)imm)&~1u;value=s->pc+4u;if(e->next_pc%4){s->fault=2;return -1;}break;
    case 0x03:case 0x23:
        e->addr=a+(uint32_t)imm;
        if(e->size==4&&e->addr%4){s->fault=3;return -1;}
        if(e->load){if(bus->read(bus->opaque,e->addr,e->size,1,&value)){s->fault=4;return -1;}e->data=value;}
        else {e->data=e->size==1?(b&255u):b;if(bus->write(bus->opaque,e->addr,e->size,e->data)){s->fault=4;return -1;}}
        break;
    default:break;
    }
    e->rd=rd;
    if(e->regwrite&&rd!=0)s->r[rd]=value;
    s->r[0]=0;s->pc=e->next_pc;return 0;
}

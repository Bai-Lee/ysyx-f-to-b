#include "dtrace.h"
/***************************************************************************************
* Copyright (c) 2014-2024 Zihao Yu, Nanjing University
*
* NEMU is licensed under Mulan PSL v2.
* You can use this software according to the terms and conditions of the Mulan PSL v2.
* You may obtain a copy of Mulan PSL v2 at:
*          http://license.coscl.org.cn/MulanPSL2
*
* THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
* EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
* MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
*
* See the Mulan PSL v2 for more details.
***************************************************************************************/

#include "local-include/reg.h"
#include <cpu/cpu.h>
#include <cpu/ifetch.h>
#include <cpu/decode.h>
#include <cpu/difftest.h>

/* Use unsigned arithmetic and explicit signed lifting, avoiding host signed overflow. */
static uint32_t sext(uint32_t x,unsigned bits){uint32_t sign=1u<<(bits-1);return (x^sign)-sign;}
static int64_t signed32(uint32_t x){return (int64_t)x-(x>>31?INT64_C(4294967296):0);}
static uint32_t asr32(uint32_t x,unsigned sh){sh&=31;if(!sh)return x;return (x>>sh)|((x>>31)?(~UINT32_C(0)<<(32-sh)):0);}
static uint32_t traced_read(uint32_t pc,uint32_t addr,unsigned len){
  uint32_t value=vaddr_read(addr,len);dtrace_access(pc,'R',addr,len,value);return value;
}
static void traced_write(uint32_t pc,uint32_t addr,unsigned len,uint32_t value){
  vaddr_write(addr,len,value);dtrace_access(pc,'W',addr,len,value & (len==4?UINT32_MAX:((1u<<(len*8))-1)));
}
static void rejected(Decode *s,const char *reason){
  fprintf(stderr,"INSTRUCTION_REJECT pc=0x%08x inst=0x%08x reason=%s\n",s->pc,s->isa.inst,reason);
  nemu_state.state=NEMU_ABORT;nemu_state.halt_pc=s->pc;nemu_state.halt_ret=1;s->dnpc=s->pc;
}

/* C5 machine-mode subset; GPR/PC DiffTest ABI stays unchanged. */
static uint32_t mstatus,mtvec,mscratch,mepc,mcause;
void c5_csr_reset(void){mstatus=0x1800;mtvec=mscratch=mepc=mcause=0;}
static uint32_t *csr_storage(unsigned number){
 switch(number){case 0x300:return &mstatus;case 0x305:return &mtvec;case 0x340:return &mscratch;case 0x341:return &mepc;case 0x342:return &mcause;default:return NULL;}
}
static bool csr_read(unsigned number,uint32_t *value,bool *readonly){
 uint32_t *storage=csr_storage(number);*readonly=false;
 if(storage){*value=*storage;return true;}
 *readonly=true;
 switch(number){case 0xf11:*value=0x79737978;return true;case 0xf12:*value=0x26070001;return true;case 0xf13:*value=1;return true;case 0xf14:*value=0;return true;default:return false;}
}
static void csr_write(unsigned number,uint32_t value){
 uint32_t *storage=csr_storage(number);Assert(storage,"CSR_STORAGE");
 if(number==0x300)value=0x1800|(value&0x88);
 if(number==0x305)value=(value&~3u)|((value&3u)==1?1u:0u);
 if(number==0x341)value&=~3u;
 *storage=value;
}

int isa_exec_once(Decode *s){
  s->dnpc=s->pc;
  if(s->pc&3){s->isa.inst=0;rejected(s,"instruction address misaligned");return 0;}
  uint32_t i=inst_fetch(&s->snpc,4);s->isa.inst=i;s->dnpc=s->snpc;dtrace_before(s->pc,i);
  unsigned op=i&127,rd=(i>>7)&31,f3=(i>>12)&7,rs1=(i>>15)&31,rs2=(i>>20)&31,f7=i>>25;
  uint32_t a=cpu.gpr[rs1],b=cpu.gpr[rs2],value=0,addr=0,next=s->snpc;
  uint32_t ii=sext(i>>20,12),si=sext(((i>>25)<<5)|((i>>7)&31),12);
  uint32_t bi=sext(((i>>31)<<12)|(((i>>7)&1)<<11)|(((i>>25)&63)<<5)|(((i>>8)&15)<<1),13);
  uint32_t ji=sext(((i>>31)<<20)|(((i>>12)&255)<<12)|(((i>>20)&1)<<11)|(((i>>21)&1023)<<1),21);
  bool write=true,legal=true;
  switch(op){
    case 0x37:value=i&0xfffff000u;break;
    case 0x17:value=s->pc+(i&0xfffff000u);break;
    case 0x6f:value=s->snpc;next=s->pc+ji;break;
    case 0x67:if(f3)legal=false;value=s->snpc;next=(a+ii)&~1u;break;
    case 0x63:{
      write=false;bool take=false;
      switch(f3){case 0:take=a==b;break;case 1:take=a!=b;break;case 4:take=signed32(a)<signed32(b);break;
      case 5:take=signed32(a)>=signed32(b);break;case 6:take=a<b;break;case 7:take=a>=b;break;default:legal=false;break;}
      if(take){next=s->pc+bi;}
      break;
    }
    case 0x03:
      addr=a+ii;
      switch(f3){case 0:value=sext(traced_read(s->pc,addr,1),8);break;case 1:value=sext(traced_read(s->pc,addr,2),16);break;
      case 2:value=traced_read(s->pc,addr,4);break;case 4:value=traced_read(s->pc,addr,1);break;case 5:value=traced_read(s->pc,addr,2);break;default:legal=false;break;}
      break;
    case 0x23:
      write=false;addr=a+si;
      switch(f3){case 0:traced_write(s->pc,addr,1,b);break;case 1:traced_write(s->pc,addr,2,b);break;case 2:traced_write(s->pc,addr,4,b);break;default:legal=false;break;}
      break;
    case 0x13:
      switch(f3){
      case 0:value=a+ii;break;
      case 2:value=signed32(a)<signed32(ii);break;case 3:value=a<ii;break;
      case 4:value=a^ii;break;case 6:value=a|ii;break;case 7:value=a&ii;break;
      case 1:if(f7)legal=false;value=a<<rs2;break;
      case 5:if(f7!=0&&f7!=0x20)legal=false;value=f7==0x20?asr32(a,rs2):a>>rs2;break;
      default:legal=false;break;
      }
      break;
    case 0x33:
      if(f7==1){
        switch(f3){
        case 0:value=(uint32_t)((uint64_t)a*b);break;
        case 1:value=(uint32_t)((uint64_t)(signed32(a)*signed32(b))>>32);break;
        case 2:value=(uint32_t)((uint64_t)(signed32(a)*(int64_t)b)>>32);break;
        case 3:value=(uint32_t)(((uint64_t)a*b)>>32);break;
        case 4:value=b?(uint32_t)(signed32(a)/signed32(b)):UINT32_MAX;break;
        case 5:value=b?a/b:UINT32_MAX;break;
        case 6:value=b?(uint32_t)(signed32(a)%signed32(b)):a;break;
        case 7:value=b?a%b:a;break;
        }
      }else{
        switch(f3){
        case 0:if(f7!=0&&f7!=0x20)legal=false;value=f7==0x20?a-b:a+b;break;
        case 1:if(f7)legal=false;value=a<<(b&31);break;
        case 2:if(f7)legal=false;value=signed32(a)<signed32(b);break;
        case 3:if(f7)legal=false;value=a<b;break;
        case 4:if(f7)legal=false;value=a^b;break;
        case 5:if(f7!=0&&f7!=0x20)legal=false;value=f7==0x20?asr32(a,b):a>>(b&31);break;
        case 6:if(f7)legal=false;value=a|b;break;
        case 7:if(f7)legal=false;value=a&b;break;
        }
      }
      break;
    case 0x0f:write=false;legal=(f3==0||f3==1);break; /* single-hart, no cache: FENCE / Zifencei */
    case 0x73:
      write=false;
      if(i==0x00100073){difftest_skip_ref();NEMUTRAP(s->pc,cpu.gpr[10]);}
      else if(i==0x00000073){mepc=s->pc;mcause=11;mstatus=0x1800|((mstatus&8)<<4);next=mtvec&~3u;}
      else if(i==0x30200073){next=mepc;mstatus=0x1880|((mstatus&0x80)>>4);}
      else if(f3==1||f3==2||f3==3||f3==5||f3==6||f3==7){
        unsigned number=i>>20,action=f3&3;uint32_t old=0,operand=(f3&4)?rs1:a;bool readonly=false;
        bool modifies=action==1||rs1!=0;
        legal=csr_read(number,&old,&readonly)&&!(modifies&&readonly);
        if(legal){
          uint32_t updated=action==1?operand:action==2?(old|operand):(old&~operand);
          if(modifies)csr_write(number,updated);
          value=old;write=true;
        }
      }else legal=false;
      break;
    default:legal=false;break;
  }
  if(!legal){rejected(s,"unsupported or reserved encoding");return 0;}
  if(next&3){rejected(s,"instruction target misaligned");return 0;}
  if(write&&rd)cpu.gpr[rd]=value;
  cpu.gpr[0]=0;s->dnpc=next;return 0;
}

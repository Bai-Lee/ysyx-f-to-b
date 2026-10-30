/* D_STAGE_FULL_SPAN: little-endian host, defined unaligned byte copy; full access checked. */
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


#include <memory/paddr.h>
#include <isa.h>
typedef struct {paddr_t base;size_t size;bool readonly;const char *name;uint8_t *data;} Region;
static Region regions[]={
 {0x0f000000,0x2000,false,"SRAM",NULL},
 {0x20000000,0x1000,true,"MROM",NULL},
 {0x30000000,0x1000000,true,"FLASH",NULL},
 {0x80000000,0x400000,false,"PSRAM",NULL},
 {0xa0000000,0x8000000,false,"SDRAM",NULL},
 {0xc0000000,0x1000,false,"CHIPLINK_TEST",NULL}
};
static Region *find_region(paddr_t addr,size_t n){
 for(size_t i=0;i<ARRLEN(regions);i++){
  Region *r=&regions[i];
  if((uint64_t)addr>=r->base&&n<=r->size&&(uint64_t)addr-r->base<=r->size-n)return r;
 }
 return NULL;
}
bool c5_memory_span(paddr_t addr,size_t n){return find_region(addr,n)!=NULL;}
uint8_t *guest_to_host(paddr_t addr){
 Region *r=find_region(addr,1);Assert(r&&r->data,"C5_REF_ADDRESS %08x",addr);
 return r->data+(addr-r->base);
}
paddr_t host_to_guest(uint8_t *host){
 uintptr_t h=(uintptr_t)host;
 for(size_t i=0;i<ARRLEN(regions);i++){
  uintptr_t start=(uintptr_t)regions[i].data;
  if(h>=start&&h-start<regions[i].size)return regions[i].base+(h-start);
 }
 panic("C5_REF_HOST_ADDRESS");return 0;
}
void init_mem(void){
 for(size_t i=0;i<ARRLEN(regions);i++){
  Region *r=&regions[i];if(!r->data)r->data=malloc(r->size);
  Assert(r->data,"C5_REF_ALLOC %s",r->name);memset(r->data,0,r->size);
 }
}
word_t paddr_read(paddr_t addr,int len){
 Assert((len==1||len==2||len==4)&&c5_memory_span(addr,(size_t)len),"C5_REF_READ_SPAN addr=%08x len=%d",addr,len);
 word_t data=0;memcpy(&data,guest_to_host(addr),(size_t)len);return data;
}
void paddr_write(paddr_t addr,int len,word_t value){
 Region *r=find_region(addr,(size_t)len);
 Assert((len==1||len==2||len==4)&&r,"C5_REF_WRITE_SPAN addr=%08x len=%d",addr,len);
 Assert(!r->readonly,"C5_READONLY_REGION addr=%08x region=%s",addr,r->name);
 memcpy(guest_to_host(addr),&value,(size_t)len);
}

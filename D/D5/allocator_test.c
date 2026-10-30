#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>
#include <stdalign.h>
extern void klib_heap_reset(void *,void *);
extern int klib_heap_validate(void);
extern void *d_malloc(size_t),*d_calloc(size_t,size_t),*d_realloc(void *,size_t);
extern void d_free(void *);
static alignas(16) unsigned char arena[65536];
static uint32_t state=0x2607d5;
static uint32_t next(void){state^=state<<13;state^=state>>17;state^=state<<5;return state;}
int main(void){
 klib_heap_reset(arena+1,arena+sizeof(arena)-1);assert(klib_heap_validate());
 assert(!d_malloc(SIZE_MAX));assert(!d_calloc(SIZE_MAX,2));d_free(NULL);
 void *fragmented[512];
 for(unsigned i=0;i<512;i++){fragmented[i]=d_malloc(8);assert(fragmented[i]);memset(fragmented[i],(int)(i&255),8);}
 assert(klib_heap_validate());
 for(unsigned i=0;i<512;i+=2)d_free(fragmented[i]);
 assert(klib_heap_validate());
 for(unsigned i=1;i<512;i+=2){void *q=d_realloc(fragmented[i],80);assert(q);for(unsigned j=0;j<8;j++)assert(((unsigned char*)q)[j]==(i&255));fragmented[i]=q;}
 assert(klib_heap_validate());
 for(unsigned i=1;i<512;i+=2)d_free(fragmented[i]);
 assert(klib_heap_validate());
 void *p[32]={0};size_t len[32]={0};unsigned char mark[32]={0};unsigned successes=0;
 for(unsigned step=0;step<10000;step++){
  unsigned id=next()%32,op=next()%3;size_t size=next()%2048+1;
  if(p[id]){
   for(size_t i=0;i<len[id];i++){assert(((unsigned char *)p[id])[i]==mark[id]);}
   if(op==0){d_free(p[id]);p[id]=NULL;len[id]=0;}
   else{void *q=d_realloc(p[id],size);if(q){for(size_t i=0;i<(size<len[id]?size:len[id]);i++){assert(((unsigned char *)q)[i]==mark[id]);}p[id]=q;len[id]=size;memset(q,mark[id],size);successes++;}}
  }else{
   p[id]=op==0?d_calloc(size,1):d_malloc(size);
   if(p[id]){if(op==0){for(size_t i=0;i<size;i++){assert(((unsigned char *)p[id])[i]==0);}}len[id]=size;mark[id]=(unsigned char)(id+step);memset(p[id],mark[id],size);successes++;}
  }
  assert(klib_heap_validate());
  for(unsigned i=0;i<32;i++)if(p[i]){
   assert((uintptr_t)p[i]%16==0);
   for(unsigned j=0;j<i;j++)if(p[j])assert((uintptr_t)p[i]+len[i]<=(uintptr_t)p[j]||(uintptr_t)p[j]+len[j]<=(uintptr_t)p[i]);
  }
 }
 for(unsigned i=0;i<32;i++){d_free(p[i]);}assert(klib_heap_validate());
 void *big=d_malloc(65000);assert(big);memset(big,0x5a,65000);assert(!d_realloc(big,SIZE_MAX));assert(((unsigned char *)big)[0]==0x5a&&((unsigned char *)big)[64999]==0x5a);
 assert(d_realloc(big,0)==NULL);assert(klib_heap_validate());
 printf("ALLOCATOR_PASS steps=10000 fragmentation_blocks=512 successful_changes=%u seed=0x2607d5\n",successes);return 0;
}

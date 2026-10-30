#include <stddef.h>
#include <stdint.h>
#ifdef D_KLIB_HOST_TEST
#include <string.h>
#else
#include <klib.h>
#endif
#if !defined(__ISA_NATIVE__) || defined(__NATIVE_USE_KLIB__) || defined(D_KLIB_HOST_TEST)
#if defined(__ISA_NATIVE__) && !defined(D_KLIB_HOST_TEST)
/* Native AM uses glibc before its heap is initialized. Keep host allocation in
 * glibc while testing our string/format routines; bare-metal allocation is below. */
extern void *__libc_malloc(size_t),*__libc_calloc(size_t,size_t),*__libc_realloc(void *,size_t);
extern void __libc_free(void *);
void *malloc(size_t n){return __libc_malloc(n);}
void *calloc(size_t n,size_t s){return __libc_calloc(n,s);}
void *realloc(void *p,size_t n){return __libc_realloc(p,n);}
void free(void *p){__libc_free(p);}
#else
typedef struct Block {size_t size,used;struct Block *next;unsigned available;} Block;
#define ALIGNMENT 16u
#define HEADER_SIZE ((sizeof(Block)+ALIGNMENT-1)&~(size_t)(ALIGNMENT-1))
static Block *first;
static uintptr_t heap_begin,heap_end;
void klib_heap_reset(void *begin,void *end){
 uintptr_t lo=(uintptr_t)begin,hi=(uintptr_t)end;first=NULL;heap_begin=heap_end=0;
 if(lo>UINTPTR_MAX-(ALIGNMENT-1))return;
 lo=(lo+ALIGNMENT-1)&~(uintptr_t)(ALIGNMENT-1);hi&=~(uintptr_t)(ALIGNMENT-1);
 if(hi<=lo||hi-lo<HEADER_SIZE+ALIGNMENT)return;
 heap_begin=lo;heap_end=hi;first=(Block *)lo;first->size=hi-lo-HEADER_SIZE;first->used=0;first->next=NULL;first->available=1;
}
static void initialize(void){
#ifndef D_KLIB_HOST_TEST
 if(!first)klib_heap_reset(heap.start,heap.end);
#endif
}
int klib_heap_validate(void){
 if(!first)return heap_begin==heap_end;
 uintptr_t at=heap_begin;unsigned visits=0;
 for(Block *b=first;b;b=b->next){
  if(++visits>1000000||(uintptr_t)b!=at||at%ALIGNMENT||at>heap_end||heap_end-at<HEADER_SIZE)return 0;
  if(b->size%ALIGNMENT||b->used>b->size||b->size>heap_end-at-HEADER_SIZE)return 0;
  at+=HEADER_SIZE+b->size;
  if((b->next==NULL)!=(at==heap_end))return 0;
 }
 return at==heap_end;
}
void *malloc(size_t size){
 initialize();if(size>SIZE_MAX-(ALIGNMENT-1))return NULL;
 size_t need=size?(size+ALIGNMENT-1)&~(size_t)(ALIGNMENT-1):ALIGNMENT;
 for(Block *b=first;b;b=b->next){
  if(!b->available||b->size<need)continue;
  if(b->size-need>=HEADER_SIZE+ALIGNMENT){
   Block *tail=(Block *)((unsigned char *)b+HEADER_SIZE+need);
   tail->size=b->size-need-HEADER_SIZE;tail->used=0;tail->available=1;tail->next=b->next;b->next=tail;b->size=need;
  }
  b->available=0;b->used=size;return (unsigned char *)b+HEADER_SIZE;
 }
 return NULL;
}
void free(void *ptr){
 if(!ptr){return;}
 Block *block=(Block *)((unsigned char *)ptr-HEADER_SIZE);block->available=1;block->used=0;
 for(Block *b=first;b&&b->next;){
  if(b->available&&b->next->available){b->size+=HEADER_SIZE+b->next->size;b->next=b->next->next;}
  else b=b->next;
 }
}
void *calloc(size_t n,size_t size){
 if(size&&n>SIZE_MAX/size)return NULL;
 size_t total=n*size;void *p=malloc(total);if(p)memset(p,0,total);return p;
}
void *realloc(void *ptr,size_t size){
 if(!ptr)return malloc(size);
 if(!size){free(ptr);return NULL;}
 Block *b=(Block *)((unsigned char *)ptr-HEADER_SIZE);
 if(size<=b->size){b->used=size;return ptr;}
 void *next=malloc(size);if(!next)return NULL;
 memcpy(next,ptr,b->used);free(ptr);return next;
}
#endif
#endif

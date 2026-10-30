#include <stddef.h>
#include <stdint.h>
#ifdef D_KLIB_HOST_TEST
#include <string.h>
#include <assert.h>
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
typedef struct Block {
 size_t size,used;
 struct Block *previous,*next,*previous_free,*next_free;
 unsigned available;
} Block;
#define ALIGNMENT 16u
#define HEADER_SIZE ((sizeof(Block)+ALIGNMENT-1)&~(size_t)(ALIGNMENT-1))
static Block *first,*first_free;
static uintptr_t heap_begin,heap_end;
void klib_heap_reset(void *begin,void *end){
 uintptr_t lo=(uintptr_t)begin,hi=(uintptr_t)end;first=first_free=NULL;heap_begin=heap_end=0;
 if(lo>UINTPTR_MAX-(ALIGNMENT-1))return;
 lo=(lo+ALIGNMENT-1)&~(uintptr_t)(ALIGNMENT-1);hi&=~(uintptr_t)(ALIGNMENT-1);
 if(hi<=lo||hi-lo<HEADER_SIZE+ALIGNMENT)return;
 heap_begin=lo;heap_end=hi;first=first_free=(Block *)lo;
 *first=(Block){.size=hi-lo-HEADER_SIZE,.available=1};
}
static void initialize(void){
#ifndef D_KLIB_HOST_TEST
 if(!first)klib_heap_reset(heap.start,heap.end);
#endif
}
int klib_heap_validate(void){
 if(!first)return !first_free&&heap_begin==heap_end;
 uintptr_t at=heap_begin;unsigned visits=0,free_blocks=0;Block *previous=NULL;
 for(Block *b=first;b;b=b->next){
  if(++visits>1000000||(uintptr_t)b!=at||at%ALIGNMENT||at>heap_end||heap_end-at<HEADER_SIZE)return 0;
  if(b->previous!=previous||b->available>1||b->size%ALIGNMENT||b->used>b->size||b->size>heap_end-at-HEADER_SIZE)return 0;
  if(b->available)free_blocks++;
  else if(b->previous_free||b->next_free)return 0;
  at+=HEADER_SIZE+b->size;
  if((b->next==NULL)!=(at==heap_end))return 0;
  if(b->next&&(uintptr_t)b->next!=at)return 0;
  if(b->available&&b->next&&b->next->available)return 0;
  previous=b;
 }
 if(at!=heap_end)return 0;
 unsigned free_visits=0;Block *prior_free=NULL;
 for(Block *f=first_free;f;f=f->next_free){
  if(++free_visits>free_blocks||(uintptr_t)f<heap_begin||(uintptr_t)f>heap_end-HEADER_SIZE||(uintptr_t)f%ALIGNMENT)return 0;
  if(!f->available||f->previous_free!=prior_free)return 0;
  int found=0;for(Block *b=first;b;b=b->next)if(b==f){found=1;break;}
  if(!found)return 0;
  prior_free=f;
 }
 return free_visits==free_blocks;
}
static void unlink_free(Block *b){
 assert(b->available);
 if(b->previous_free)b->previous_free->next_free=b->next_free;
 else{assert(first_free==b);first_free=b->next_free;}
 if(b->next_free)b->next_free->previous_free=b->previous_free;
 b->previous_free=b->next_free=NULL;
}
static void link_free(Block *b){
 assert(b->available);b->previous_free=NULL;b->next_free=first_free;
 if(first_free)first_free->previous_free=b;
 first_free=b;
}
static void split_tail(Block *b,size_t need){
 if(b->size-need<HEADER_SIZE+ALIGNMENT)return;
 Block *tail=(Block *)((unsigned char *)b+HEADER_SIZE+need);
 *tail=(Block){.size=b->size-need-HEADER_SIZE,.previous=b,.next=b->next,.available=1};
 if(tail->next)tail->next->previous=tail;
 b->next=tail;b->size=need;link_free(tail);
}
void *malloc(size_t size){
 initialize();if(size>SIZE_MAX-(ALIGNMENT-1))return NULL;
 size_t need=size?(size+ALIGNMENT-1)&~(size_t)(ALIGNMENT-1):ALIGNMENT;
 for(Block *b=first_free;b;b=b->next_free){
  assert(b->available);if(b->size<need)continue;
  unlink_free(b);b->available=0;split_tail(b,need);b->used=size;return (unsigned char *)b+HEADER_SIZE;
 }
 return NULL;
}
void free(void *ptr){
 if(!ptr){return;}
 assert((uintptr_t)ptr>=heap_begin+HEADER_SIZE&&(uintptr_t)ptr<heap_end&&(uintptr_t)ptr%ALIGNMENT==0);
 Block *b=(Block *)((unsigned char *)ptr-HEADER_SIZE);assert(!b->available);
 b->available=1;b->used=0;link_free(b);
 if(b->previous&&b->previous->available){
  Block *left=b->previous;unlink_free(b);left->size+=HEADER_SIZE+b->size;left->next=b->next;
  if(left->next)left->next->previous=left;
  b=left;
 }
 if(b->next&&b->next->available){
  Block *right=b->next;unlink_free(right);b->size+=HEADER_SIZE+right->size;b->next=right->next;
  if(b->next)b->next->previous=b;
 }
}
void *calloc(size_t n,size_t size){
 if(size&&n>SIZE_MAX/size)return NULL;
 size_t total=n*size;void *p=malloc(total);if(p)memset(p,0,total);return p;
}
void *realloc(void *ptr,size_t size){
 if(!ptr)return malloc(size);
 if(!size){free(ptr);return NULL;}
 if(size>SIZE_MAX-(ALIGNMENT-1))return NULL;
 Block *b=(Block *)((unsigned char *)ptr-HEADER_SIZE);
 if(size<=b->size){b->used=size;return ptr;}
 size_t need=(size+ALIGNMENT-1)&~(size_t)(ALIGNMENT-1);
 if(b->next&&b->next->available&&b->size+HEADER_SIZE+b->next->size>=need){
  Block *right=b->next;unlink_free(right);b->size+=HEADER_SIZE+right->size;b->next=right->next;
  if(b->next)b->next->previous=b;
  split_tail(b,need);b->used=size;return ptr;
 }
 void *next=malloc(size);if(!next)return NULL;
 memcpy(next,ptr,b->used);free(ptr);return next;
}
#endif
#endif

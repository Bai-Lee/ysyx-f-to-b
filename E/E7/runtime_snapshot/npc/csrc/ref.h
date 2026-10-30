#ifndef MINIRV_REF_H
#define MINIRV_REF_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
typedef struct {uint32_t pc,r[16];unsigned halted,fault;} MiniState;
typedef int (*MiniRead)(void*,uint32_t,unsigned,int,uint32_t*);
typedef int (*MiniWrite)(void*,uint32_t,unsigned,uint32_t);
typedef struct {void *opaque;MiniRead read;MiniWrite write;} MiniBus;
typedef struct {uint32_t pc,inst,next_pc,addr,data;unsigned load,store,size,rd,regwrite;} MiniEvent;
void minirv_reset(MiniState*,uint32_t);
int minirv_step(MiniState*,MiniBus*,MiniEvent*);
#ifdef __cplusplus
}
#endif
#endif

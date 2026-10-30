#ifndef D_STAGE_DEBUG_CORE_H
#define D_STAGE_DEBUG_CORE_H
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#ifdef __cplusplus
extern "C" {
#endif
typedef bool (*DReadReg)(void *,const char *,uint32_t *);
typedef bool (*DReadMem)(void *,uint32_t,uint32_t *);
typedef struct {DReadReg reg;DReadMem mem;void *opaque;} DExprContext;
bool d_expr(const char *,const DExprContext *,uint32_t *,char *,size_t);
#define D_WATCH_COUNT 32
#define D_WATCH_EXPR 1024
typedef struct {int next;bool active;uint32_t value;char expression[D_WATCH_EXPR];} DWatch;
typedef struct {DWatch slots[D_WATCH_COUNT];int head,free_head;} DWatchPool;
void d_wp_init(DWatchPool *);
int d_wp_add(DWatchPool *,const char *,const DExprContext *,char *,size_t);
bool d_wp_delete(DWatchPool *,int);
bool d_wp_check(DWatchPool *,const DExprContext *,FILE *);
void d_wp_info(const DWatchPool *,FILE *);
bool d_wp_invariant(const DWatchPool *);
#ifdef __cplusplus
}
#endif
#endif

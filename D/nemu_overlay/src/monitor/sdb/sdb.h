#ifndef D_NEMU_SDB_H
#define D_NEMU_SDB_H
#include <common.h>
#include <debug_core.h>
word_t expr(char *,bool *);
extern DExprContext sdb_expr_context;
bool sdb_read_word(uint32_t,uint32_t *);
bool sdb_check_watchpoints(void);
void sdb_watch_add(const char *);
void sdb_watch_delete(int);
void sdb_watch_info(void);
#endif

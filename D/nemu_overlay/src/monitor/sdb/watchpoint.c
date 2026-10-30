#include "sdb.h"
static DWatchPool pool;
void init_wp_pool(void){d_wp_init(&pool);}
bool sdb_check_watchpoints(void){return d_wp_check(&pool,&sdb_expr_context,stdout);}
void sdb_watch_add(const char *text){
#ifndef CONFIG_WATCHPOINT
  (void)text;puts("WATCH_DISABLED_BY_CONFIG");return;
#else
  char error[160];int id=d_wp_add(&pool,text,&sdb_expr_context,error,sizeof(error));
  if(id<0)printf("WATCH_ERROR %s\n",error);else printf("WATCH_ADDED %d %s\n",id,text);
  assert(d_wp_invariant(&pool));
#endif
}
void sdb_watch_delete(int id){printf("%s %d\n",d_wp_delete(&pool,id)?"WATCH_DELETED":"WATCH_ERROR_NO_ID",id);assert(d_wp_invariant(&pool));}
void sdb_watch_info(void){d_wp_info(&pool,stdout);}

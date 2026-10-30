#include <isa.h>
#include <cpu/cpu.h>
#include <readline/readline.h>
#include <readline/history.h>
#include <ctype.h>
#include <errno.h>
#include "sdb.h"
static bool is_batch_mode=false;
void init_regex(void);
void init_wp_pool(void);
static char *trim(char *s){if(!s)return NULL;while(isspace((unsigned char)*s))s++;size_t n=strlen(s);while(n&&isspace((unsigned char)s[n-1]))s[--n]=0;return s;}
static bool count(const char *s,uint32_t max,uint32_t *v){
 if(!s||!*s||*s=='-'){return false;}
 errno=0;char *end;unsigned long n=strtoul(s,&end,10);
 while(isspace((unsigned char)*end)){end++;}
 if(errno||end==s||*end||n>max){return false;}
 *v=(uint32_t)n;return true;
}
void sdb_set_batch_mode(void){is_batch_mode=true;}
void init_sdb(void){init_regex();init_wp_pool();}
void sdb_mainloop(void){
 if(is_batch_mode){cpu_exec(UINT64_MAX);return;}
 for(;;){
  char *line=readline("(nemu) ");if(!line)break;
  if(*line)add_history(line);
  char *cmd=trim(line),*args=cmd;while(*args&&!isspace((unsigned char)*args))args++;
  if(*args){*args++=0;args=trim(args);}else args=NULL;
  if(!*cmd){free(line);continue;}
  if(!strcmp(cmd,"q")){nemu_state.state=NEMU_QUIT;free(line);break;}
  else if(!strcmp(cmd,"help"))puts("c | q | si [N] | info r | info w | x N EXPR | p EXPR | w EXPR | d ID");
  else if(!strcmp(cmd,"c")){if(args&&*args)puts("COMMAND_ERROR c takes no arguments");else cpu_exec(UINT64_MAX);}
  else if(!strcmp(cmd,"si")){uint32_t n=1;if(args&&(!count(args,1000000,&n)||!n))puts("COMMAND_ERROR invalid step count");else cpu_exec(n);}
  else if(!strcmp(cmd,"info")){if(args&&!strcmp(args,"r"))isa_reg_display();else if(args&&!strcmp(args,"w"))sdb_watch_info();else puts("COMMAND_ERROR info r|w");}
  else if(!strcmp(cmd,"p")){bool ok=false;word_t v=expr(args,&ok);if(ok)printf("EXPR_VALUE %u 0x%08x\n",v,v);}
  else if(!strcmp(cmd,"w"))sdb_watch_add(args);
  else if(!strcmp(cmd,"d")){uint32_t id;if(!count(args,31,&id))puts("COMMAND_ERROR invalid watchpoint id");else sdb_watch_delete((int)id);}
  else if(!strcmp(cmd,"x")){
   if(!args){puts("COMMAND_ERROR x N EXPR");free(line);continue;}
   char *address=args;while(*address&&!isspace((unsigned char)*address))address++;
   if(*address)*address++=0;
   uint32_t n;if(!count(args,256,&n)||!n){puts("COMMAND_ERROR invalid scan count");free(line);continue;}
   bool ok=false;uint32_t a=expr(trim(address),&ok);
   if(ok)for(uint32_t i=0;i<n;i++){uint32_t v;if((uint64_t)a+4*i>UINT32_MAX||!sdb_read_word(a+4*i,&v)){puts("MEMORY_ERROR outside RAM");break;}printf("MEMORY 0x%08x: 0x%08x\n",a+4*i,v);}
  }else printf("COMMAND_ERROR unknown command '%s'\n",cmd);
  free(line);
 }
 clear_history();
}

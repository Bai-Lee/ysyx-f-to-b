#include "trace_core.h"
#include <stdio.h>
int main(int argc,char **argv){
  if(argc!=2&&argc!=3)return 3;
  char error[256];dtrace_context *t=dtrace_create(argc==3?"/dev/stdout":NULL,argv[1],argc==3?4:0,10,error,sizeof error);
  if(!t){fprintf(stderr,"ELF_REJECT %s\n",error);return 2;}
  if(argc==3)dtrace_commit(t,0x80000000,0x000000ef,0xfffffff4);
  printf("ELF_ACCEPT symbols=%zu\n",dtrace_symbol_count(t));dtrace_destroy(t);return 0;
}

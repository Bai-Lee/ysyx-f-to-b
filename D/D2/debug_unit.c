#include "debug_core.h"
#include <assert.h>
#include <string.h>
#include <stdlib.h>
#include <inttypes.h>
typedef struct {uint32_t a0,word;unsigned reads;} State;
static bool reg(void *o,const char *s,uint32_t *v){State *p=o;if(!strcmp(s,"a0")){*v=p->a0;return true;}if(!strcmp(s,"pc")){*v=0x80000000;return true;}return false;}
static bool mem(void *o,uint32_t a,uint32_t *v){State *p=o;p->reads++;if(a!=0x80000000)return false;*v=p->word;return true;}
int main(int argc,char **argv){
 State s={7,0x12345678,0};DExprContext c={reg,mem,&s};char error[128];uint32_t v;
 struct {const char *e;uint32_t value;} good[]={
 {"1+2*3",7},{"(1+2)*3",9},{"10-3-2",5},{"24/4/2",3},{"0xffffffff+1",0},
 {"-1",UINT32_MAX},{"--5",5},{"!0",1},{"1!=2==1",1},{"1+2==3&&4!=5",1},
 {"$a0 + 3",10},{"*$pc",0x12345678},{"0&&1/0",0},{"1||*0",1},{"0&&$absent",0},
 {"  ( 10u +\t2 ) * 3 ",36},{"0x80000000 / 2",0x40000000}
 };
 for(size_t i=0;i<sizeof(good)/sizeof(good[0]);i++){
  bool ok=d_expr(good[i].e,&c,&v,error,sizeof(error));
  if(!ok)fprintf(stderr,"EXPRESSION_REJECTED %s: %s\n",good[i].e,error);
  assert(ok);assert(v==good[i].value);
 }
 assert(s.reads==1);
 const char *bad[]={""," ","1+","(1","1)","1 2","1/0","1/(2-2)","$missing","*0","4294967296","0x100000000","184467440737095516160","a+1","0&&(1+)","0x","1===1"};
 for(size_t i=0;i<sizeof(bad)/sizeof(bad[0]);i++){v=0x98765432;assert(!d_expr(bad[i],&c,&v,error,sizeof(error)));assert(v==0x98765432&&error[0]);}
 char many[18000];memset(many,'(',1000);memset(many+1000,')',1000);many[2000]=0;assert(!d_expr(many,&c,&v,error,sizeof(error)));
 for(int i=0;i<8194;i++){many[i]=(i%2)?'+':'1';}
 many[8194]=0;assert(!d_expr(many,&c,&v,error,sizeof(error)));
 memset(many,'1',17000);many[17000]=0;assert(!d_expr(many,&c,&v,error,sizeof(error)));
 DWatchPool p;d_wp_init(&p);assert(d_wp_invariant(&p));
 assert(d_wp_add(&p,"1/0",&c,error,sizeof(error))==-1);assert(d_wp_invariant(&p));
 for(int i=0;i<32;i++){assert(d_wp_add(&p,"$a0",&c,error,sizeof(error))==i);assert(d_wp_invariant(&p));}
 assert(d_wp_add(&p,"$a0",&c,error,sizeof(error))==-1);assert(!d_wp_delete(&p,32));assert(!d_wp_delete(&p,-1));
 assert(!d_wp_check(&p,&c,stdout));s.a0=8;assert(d_wp_check(&p,&c,stdout));assert(!d_wp_check(&p,&c,stdout));
 for(int i=0;i<32;i+=2){assert(d_wp_delete(&p,i));assert(!d_wp_delete(&p,i));assert(d_wp_invariant(&p));}
 for(int i=0;i<16;i++)assert(d_wp_add(&p,"$a0+1",&c,error,sizeof(error))>=0);
 for(int i=31;i>=0;i--){assert(d_wp_delete(&p,i));assert(d_wp_invariant(&p));}
 if(argc==2){
  FILE *f=fopen(argv[1],"r");assert(f);char *line=NULL;size_t cap=0;unsigned count=0;
  while(getline(&line,&cap,f)>0){char *end;unsigned long want=strtoul(line,&end,10);assert(end!=line&&want<=UINT32_MAX);assert(d_expr(end,&c,&v,error,sizeof(error)));if(v!=(uint32_t)want){fprintf(stderr,"MISMATCH %s got=%u expected=%lu\n",end,v,want);return 2;}count++;}
  free(line);fclose(f);printf("RANDOM_EXPRESSIONS_PASS %u\n",count);assert(count>0);
 }
 puts("DEBUG_CORE_PASS");return 0;
}

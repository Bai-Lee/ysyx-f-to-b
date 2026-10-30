/* Authored D-stage debugger core; 32-bit unsigned expression semantics. */
#include "debug_core.h"
#include <regex.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <stdarg.h>
#include <inttypes.h>

enum {T_SKIP=256,T_NUMBER,T_REGISTER,T_EQ,T_NE,T_AND,T_OR,T_END};
typedef struct {const char *pattern;int kind;regex_t compiled;} Rule;
static Rule rules[]={
 {"^[[:space:]]+",T_SKIP,{0}}, {"^0[xX][0-9a-fA-F]+[uU]?",T_NUMBER,{0}},
 {"^[0-9]+[uU]?",T_NUMBER,{0}}, {"^\\$\\$?[a-zA-Z0-9_]+",T_REGISTER,{0}},
 {"^==",T_EQ,{0}}, {"^!=",T_NE,{0}}, {"^&&",T_AND,{0}}, {"^\\|\\|",T_OR,{0}},
 {"^\\+",'+',{0}}, {"^-",'-',{0}}, {"^\\*",'*',{0}}, {"^/",'/',{0}},
 {"^!",'!',{0}}, {"^\\(",'(',{0}}, {"^\\)",')',{0}}
};
typedef struct {int kind;uint32_t number;char name[32];} Token;
typedef struct {Token *tokens;size_t count,pos;bool ok;const DExprContext *ctx;char *err;size_t cap;} Parser;
static bool rules_ready=false;
static void fail(Parser *p,const char *fmt,...){
 if(!p->ok)return;
 p->ok=false;
 if(p->err&&p->cap){va_list ap;va_start(ap,fmt);vsnprintf(p->err,p->cap,fmt,ap);va_end(ap);}
}
static int precedence(int k){
 switch(k){case T_OR:return 1;case T_AND:return 2;case T_EQ:case T_NE:return 3;
 case '+':case '-':return 4;case '*':case '/':return 5;default:return 0;}
}
static uint32_t parse(Parser *p,int min,bool evaluate,unsigned depth);
static uint32_t prefix(Parser *p,bool evaluate,unsigned depth){
 if(depth>256){fail(p,"expression nesting exceeds 256");return 0;}
 if(p->pos>=p->count){fail(p,"missing operand");return 0;}
 Token *t=&p->tokens[p->pos++];uint32_t v=0;
 if(t->kind==T_NUMBER)return t->number;
 if(t->kind==T_REGISTER){
  if(evaluate&&(!p->ctx||!p->ctx->reg||!p->ctx->reg(p->ctx->opaque,t->name,&v)))fail(p,"unknown register $%s",t->name);
  return v;
 }
 if(t->kind=='('){v=parse(p,1,evaluate,depth+1);if(p->tokens[p->pos].kind!=')')fail(p,"missing closing parenthesis");else p->pos++;return v;}
 if(t->kind=='+'||t->kind=='-'||t->kind=='!'||t->kind=='*'){
  v=prefix(p,evaluate,depth+1);
  if(!p->ok||!evaluate)return 0;
  if(t->kind=='-')return 0u-v;
  if(t->kind=='!')return !v;
  if(t->kind=='*'){
   uint32_t data=0;if(!p->ctx||!p->ctx->mem||!p->ctx->mem(p->ctx->opaque,v,&data))fail(p,"invalid 32-bit memory read at 0x%08" PRIx32,v);
   return data;
  }
  return v;
 }
 fail(p,"expected a number, register or unary expression");return 0;
}
static uint32_t parse(Parser *p,int min,bool evaluate,unsigned depth){
 uint32_t lhs=prefix(p,evaluate,depth);
 while(p->ok){
  int op=p->tokens[p->pos].kind,prec=precedence(op);if(prec<min)break;p->pos++;
  bool rhs_eval=evaluate&&!(op==T_AND&&!lhs)&&!(op==T_OR&&lhs);
  uint32_t rhs=parse(p,prec+1,rhs_eval,depth+1);
  if(!p->ok||!evaluate)continue;
  switch(op){
   case '+':lhs+=rhs;break;case '-':lhs-=rhs;break;case '*':lhs*=rhs;break;
   case '/':if(!rhs)fail(p,"division by zero");else lhs/=rhs;break;
   case T_EQ:lhs=lhs==rhs;break;case T_NE:lhs=lhs!=rhs;break;
   case T_AND:lhs=lhs&&rhs;break;case T_OR:lhs=lhs||rhs;break;
   default:fail(p,"internal parser error");break;
  }
 }
 return lhs;
}
bool d_expr(const char *text,const DExprContext *ctx,uint32_t *result,char *error,size_t cap){
 if(error&&cap)error[0]=0;
 Token tokens[4097];Parser p={tokens,0,0,true,ctx,error,cap};
 if(!text||strlen(text)>16384){fail(&p,"expression missing or longer than 16384 bytes");return false;}
 if(!rules_ready){
  for(size_t i=0;i<sizeof(rules)/sizeof(rules[0]);i++)if(regcomp(&rules[i].compiled,rules[i].pattern,REG_EXTENDED)!=0){fail(&p,"regex setup failed");return false;}
  rules_ready=true;
 }
 size_t off=0;
 while(text[off]&&p.ok){
  bool matched=false;
  for(size_t i=0;i<sizeof(rules)/sizeof(rules[0]);i++){
   regmatch_t m;if(regexec(&rules[i].compiled,text+off,1,&m,0)!=0||m.rm_so!=0)continue;
   size_t len=(size_t)m.rm_eo;matched=true;
   if(rules[i].kind!=T_SKIP){
    if(p.count>=4096){fail(&p,"more than 4096 tokens");break;}
    Token *t=&tokens[p.count++];memset(t,0,sizeof(*t));t->kind=rules[i].kind;
    if(t->kind==T_REGISTER){if(len-1>=sizeof(t->name)){fail(&p,"register name too long");break;}memcpy(t->name,text+off+1,len-1);}
    if(t->kind==T_NUMBER){
     char literal[40];if(len>=sizeof(literal)){fail(&p,"integer literal too long");break;}
     memcpy(literal,text+off,len);literal[len]=0;
     if(literal[len-1]=='u'||literal[len-1]=='U')literal[len-1]=0;
     errno=0;char *end;unsigned long long n=strtoull(literal,&end,(len>2&&literal[0]=='0'&&(literal[1]=='x'||literal[1]=='X'))?16:10);
     if(errno||*end||n>UINT32_MAX){fail(&p,"integer literal exceeds uint32");break;}t->number=(uint32_t)n;
    }
   }
   off+=len;break;
  }
  if(!matched)fail(&p,"invalid token at byte %zu",off);
 }
 tokens[p.count]=(Token){.kind=T_END};
 if(!p.ok)return false;
 if(!p.count){fail(&p,"empty expression");return false;}
 uint32_t value=parse(&p,1,true,0);
 if(p.ok&&tokens[p.pos].kind!=T_END)fail(&p,"unexpected trailing token");
 if(p.ok&&result)*result=value;
 return p.ok;
}
void d_wp_init(DWatchPool *p){memset(p,0,sizeof(*p));p->head=-1;p->free_head=0;for(int i=0;i<D_WATCH_COUNT;i++)p->slots[i].next=i+1<D_WATCH_COUNT?i+1:-1;}
int d_wp_add(DWatchPool *p,const char *text,const DExprContext *ctx,char *error,size_t cap){
 uint32_t v;if(!text||strlen(text)>=D_WATCH_EXPR){if(error&&cap)snprintf(error,cap,"watch expression too long or missing");return -1;}
 if(!d_expr(text,ctx,&v,error,cap))return -1;
 if(p->free_head==-1){if(error&&cap)snprintf(error,cap,"watchpoint pool exhausted");return -1;}
 int id=p->free_head;DWatch *w=&p->slots[id];p->free_head=w->next;
 w->next=p->head;p->head=id;w->active=true;w->value=v;strcpy(w->expression,text);return id;
}
bool d_wp_delete(DWatchPool *p,int id){
 if(id<0||id>=D_WATCH_COUNT||!p->slots[id].active)return false;
 int *link=&p->head;while(*link!=-1&&*link!=id)link=&p->slots[*link].next;
 if(*link!=id)return false;
 *link=p->slots[id].next;p->slots[id].active=false;p->slots[id].next=p->free_head;p->free_head=id;return true;
}
bool d_wp_check(DWatchPool *p,const DExprContext *ctx,FILE *out){
 bool changed=false;
 for(int id=p->head;id!=-1;id=p->slots[id].next){
  DWatch *w=&p->slots[id];uint32_t v;char error[128];
  if(!d_expr(w->expression,ctx,&v,error,sizeof(error))){fprintf(out,"WATCH_ERROR %d %s\n",id,error);changed=true;continue;}
  if(v!=w->value){fprintf(out,"WATCH_HIT %d old=0x%08" PRIx32 " new=0x%08" PRIx32 " expression=%s\n",id,w->value,v,w->expression);w->value=v;changed=true;}
 }
 return changed;
}
void d_wp_info(const DWatchPool *p,FILE *out){
 unsigned n=0;
 for(int id=p->head;id!=-1;id=p->slots[id].next){const DWatch *w=&p->slots[id];fprintf(out,"WATCH %d value=0x%08" PRIx32 " %s\n",id,w->value,w->expression);n++;}
 fprintf(out,"WATCH_COUNT %u\n",n);
}
bool d_wp_invariant(const DWatchPool *p){
 bool seen[D_WATCH_COUNT]={false};int count=0;
 for(int list=0;list<2;list++)for(int id=list?p->free_head:p->head;id!=-1;id=p->slots[id].next){
  if(id<0||id>=D_WATCH_COUNT||seen[id]||p->slots[id].active!=(list==0))return false;
  seen[id]=true;count++;
 }
 return count==D_WATCH_COUNT;
}

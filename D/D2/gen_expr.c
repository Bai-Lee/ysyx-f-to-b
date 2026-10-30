#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <unistd.h>
#include <sys/wait.h>
#include <inttypes.h>
static uint32_t rng=0x2607d2u;
static uint32_t next(void){rng^=rng<<13;rng^=rng>>17;rng^=rng<<5;return rng;}
static char expression[8192];static size_t used;
static void put(const char *s){size_t n=strlen(s);assert(used+n<sizeof(expression));memcpy(expression+used,s,n+1);used+=n;}
static void space(void){if(next()%3==0)put(" ");}
static void number(uint32_t n){char b[32];snprintf(b,sizeof(b),"%" PRIu32,n);put(b);}
static void gen(unsigned depth){
 space();
 if(depth==0||next()%4==0){number(next());space();return;}
 put("(");gen(depth-1);space();unsigned op=next()%4;put((const char *[]){"+","-","*","/"}[op]);space();
 /* Nonzero unsigned divisor by construction; the compiler, not this generator, computes the oracle. */
 if(op==3)number(1+(next()%65535));else gen(depth-1);
 put(")");space();
}
static void emit_unsigned(FILE *f,const char *s){
 while(*s){if(*s>='0'&&*s<='9'){do fputc(*s++,f);while(*s>='0'&&*s<='9');fputc('u',f);}else fputc(*s++,f);}
}
int main(int argc,char **argv){
 unsigned total=argc>1?(unsigned)strtoul(argv[1],NULL,0):10000;if(argc>2)rng=(uint32_t)strtoul(argv[2],NULL,0);if(!rng)rng=1;
 assert(total>0&&total<=100000);fprintf(stderr,"GEN_EXPR seed=%" PRIu32 " count=%u batch=128\n",rng,total);
 const char *base=getenv("TMPDIR");if(!base)base="/tmp";char dir[1024],source[1100],binary[1100];
 assert(snprintf(dir,sizeof(dir),"%s/d-expr-XXXXXX",base)<(int)sizeof(dir));assert(mkdtemp(dir));
 snprintf(source,sizeof(source),"%s/oracle.c",dir);snprintf(binary,sizeof(binary),"%s/oracle",dir);
 for(unsigned start=0;start<total;start+=128){
  FILE *f=fopen(source,"w");assert(f);fputs("#include <stdio.h>\n#include <stdint.h>\nint main(void){\n",f);
  for(unsigned i=start;i<total&&i<start+128;i++){
   used=0;expression[0]=0;gen(1+next()%6);
   fputs("printf(\"%u ",f);fputs(expression,f);fputs("\\n\", (uint32_t)(",f);emit_unsigned(f,expression);fputs("));\n",f);
  }
  fputs("return 0;}\n",f);fclose(f);
  pid_t pid=fork();assert(pid>=0);if(!pid){execlp("gcc","gcc","-std=c11","-O0","-Wall","-Werror",source,"-o",binary,(char *)NULL);_exit(127);}
  int status;assert(waitpid(pid,&status,0)==pid&&WIFEXITED(status)&&WEXITSTATUS(status)==0);
  fflush(stdout);pid=fork();assert(pid>=0);if(!pid){execl(binary,binary,(char *)NULL);_exit(127);}
  assert(waitpid(pid,&status,0)==pid&&WIFEXITED(status)&&WEXITSTATUS(status)==0);
 }
 assert(unlink(source)==0);assert(unlink(binary)==0);assert(rmdir(dir)==0);return 0;
}

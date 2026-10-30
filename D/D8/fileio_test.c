#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <limits.h>
FILE *d_fopen(const char*,const char*);int d_fclose(FILE*);
size_t d_fread(void*,size_t,size_t,FILE*);size_t d_fwrite(const void*,size_t,size_t,FILE*);
int d_fseek(FILE*,long,int);long d_ftell(FILE*);int d_feof(FILE*);int d_ferror(FILE*);void d_clearerr(FILE*);int d_fflush(FILE*);
int d_getc(FILE*);int d_fprintf(FILE*,const char*,...);int d_fscanf(FILE*,const char*,...);
extern FILE *d_stdout;
struct file {const char *name;uint8_t *base;uint32_t size;};
static uint8_t data[257];
static uint8_t numbers[]=" -2147483648 2147483647\n17 -5\t99 0\nword Z";
static uint8_t formats[]="0xdeadbeef 777 4294967295 012 -32768 -128";
static struct file input_files[]={{"bytes",data,sizeof data},{"numbers",numbers,sizeof numbers-1},{"formats",formats,sizeof formats-1},{NULL,NULL,0}};
struct file *__am_filelist=input_files;
static char console[1024];static size_t console_size;
void putch(char c){assert(console_size<sizeof console);console[console_size++]=c;}
int main(void){
  for(unsigned i=0;i<sizeof data;i++)data[i]=(uint8_t)(i*37);
  unsigned checks=0;
  for(size_t size=1;size<=17;size++)for(size_t count=1;count<=31;count++){
    FILE *d=d_fopen("bytes","rb"),*r=fmemopen(data,sizeof data,"rb");assert(d&&r);
    uint8_t actual[1024],expected[1024];memset(actual,0xa5,sizeof actual);memset(expected,0xa5,sizeof expected);
    assert(d_fread(actual+3,size,count,d)==fread(expected+3,size,count,r));assert(memcmp(actual,expected,sizeof actual)==0);
    assert(d_ftell(d)==ftell(r));assert(!!d_feof(d)==!!feof(r));assert(d_fclose(d)==0&&fclose(r)==0);checks++;
  }
  FILE *d=d_fopen("bytes","r");assert(d);assert(d_fseek(d,-3,SEEK_END)==0&&d_ftell(d)==254);assert(d_getc(d)==data[254]);
  assert(d_fseek(d,2,SEEK_CUR)==0&&d_ftell(d)==257);assert(!d_feof(d));assert(d_getc(d)==EOF&&d_feof(d));d_clearerr(d);assert(!d_feof(d));
  assert(d_fseek(d,-1,SEEK_SET)==-1&&d_ftell(d)==257);d_clearerr(d);
  uint8_t byte;assert(d_fread(&byte,SIZE_MAX,2,d)==0&&d_ferror(d));assert(d_fclose(d)==0);
  assert(!d_fopen("absent","r")&&!d_fopen("bytes","garbage"));
  FILE *open[29];for(unsigned i=0;i<29;i++){open[i]=d_fopen("bytes","rb");assert(open[i]);}assert(!d_fopen("bytes","rb"));for(unsigned i=0;i<29;i++)assert(d_fclose(open[i])==0);
  d=d_fopen("output","w+");assert(d);assert(d_fwrite(data,1,sizeof data,d)==sizeof data);assert(d_fseek(d,300,SEEK_SET)==0);assert(d_fwrite("XYZ",1,3,d)==3);assert(d_fseek(d,0,SEEK_SET)==0);
  uint8_t expected[303]={0},actual[303];memcpy(expected,data,sizeof data);memcpy(expected+300,"XYZ",3);assert(d_fread(actual,1,sizeof actual,d)==sizeof actual&&memcmp(actual,expected,sizeof actual)==0);assert(d_fclose(d)==0);
  d=d_fopen("output","a+");assert(d);assert(d_fseek(d,0,SEEK_SET)==0);assert(d_fwrite("!",1,1,d)==1&&d_ftell(d)==304);assert(d_fclose(d)==0);
  d=d_fopen("output","r");assert(d);assert(d_fseek(d,-1,SEEK_END)==0&&d_getc(d)=='!');assert(d_fwrite("x",1,1,d)==0&&d_ferror(d));assert(d_fclose(d)==0);
  assert(!d_fopen("output","wx"));
  d=d_fopen("numbers","r");FILE *r=fmemopen(numbers,sizeof numbers-1,"r");assert(d&&r);
  for(unsigned i=0;i<3;i++){int a,b,x,y;assert(d_fscanf(d,"%d %d",&a,&b)==fscanf(r,"%d %d",&x,&y));assert(a==x&&b==y&&d_ftell(d)==ftell(r));checks++;}
  char a[8],b[8],c,x;assert(d_fscanf(d," %7s %c",a,&c)==fscanf(r," %7s %c",b,&x));assert(!strcmp(a,b)&&c==x);assert(d_fscanf(d,"%d",&checks)==EOF);d_fclose(d);fclose(r);
  d=d_fopen("format","w+");assert(d);assert(d_fprintf(d,"%d %s %08x",-12,"hello",0xab)==18);assert(d_fseek(d,0,SEEK_SET)==0);char formatted[32]={0};assert(d_fread(formatted,1,18,d)==18&&strcmp(formatted,"-12 hello 000000ab")==0);d_fclose(d);
  d=d_fopen("formats","r");r=fmemopen(formats,sizeof formats-1,"r");unsigned u1,u2,u3,v1,v2,v3;int n1,n2;short s1,s2;signed char b1,b2;
  assert(d_fscanf(d,"%x %o %u %3d %hd %hhd",&u1,&u2,&u3,&n1,&s1,&b1)==6);assert(fscanf(r,"%x %o %u %3d %hd %hhd",&v1,&v2,&v3,&n2,&s2,&b2)==6);assert(u1==v1&&u2==v2&&u3==v3&&n1==n2&&s1==s2&&b1==b2);d_fclose(d);fclose(r);checks++;
  d=d_fopen("bytes","r+");assert(d);assert(d_fwrite("Z",1,1,d)==1&&data[0]==0);assert(d_fseek(d,0,SEEK_SET)==0&&d_getc(d)=='Z');d_fclose(d);
  d=d_fopen("limit","w");assert(d);assert(d_fseek(d,LONG_MAX,SEEK_SET)==0);assert(d_fwrite("Z",1,1,d)==0&&d_ferror(d));d_fclose(d);
  assert(d_fprintf(d_stdout,"console %d",7)==9);assert(console_size==9&&!memcmp(console,"console 7",9));assert(d_fflush(NULL)==0);
  printf("FILEIO_PASS comparisons=%u plus boundaries stream-limit seek write append scanner console\n",checks);
  return 0;
}

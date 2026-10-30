/* Bounded, in-memory FILE API for AM's generated __am_filelist.
 * FILE is treated as opaque by supported clients. This is not a hosted libc,
 * POSIX filesystem, or implementation of glibc FILE internals. */
#include <stdio.h>
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <limits.h>
#if !defined(__ISA_NATIVE__) || defined(D_FILE_TEST_PREFIX)
#ifdef D_FILE_TEST_PREFIX
#define fopen d_fopen
#define fclose d_fclose
#define fread d_fread
#define fwrite d_fwrite
#define fseek d_fseek
#define ftell d_ftell
#define feof d_feof
#define ferror d_ferror
#define clearerr d_clearerr
#define fflush d_fflush
#define fgetc d_fgetc
#define getc d_getc
#define fputc d_fputc
#define putc d_putc
#define fputs d_fputs
#define vfprintf d_vfprintf
#define fprintf d_fprintf
#define vfscanf d_vfscanf
#define fscanf d_fscanf
#undef stdin
#undef stdout
#undef stderr
#define stdin d_stdin
#define stdout d_stdout
#define stderr d_stderr
#endif
extern void putch(char);
struct file {const char *name;uint8_t *base;uint32_t size;};
__attribute__((weak)) struct file *__am_filelist;
enum {D_FILES=64,D_STREAMS=32,D_FILE_MAX=64*1024*1024};
typedef struct {int used,owned;char name[256];uint8_t *data;size_t size,capacity;} DFile;
typedef struct {int used,kind,readable,writable,append,eof,error,pushed;size_t position;DFile *file;} DStream;
static DFile files[D_FILES];
static DStream streams[D_STREAMS]={
  {.used=1,.kind=1,.readable=1,.pushed=-1},
  {.used=1,.kind=2,.writable=1,.pushed=-1},
  {.used=1,.kind=2,.writable=1,.pushed=-1}};
FILE *stdin=(FILE*)&streams[0],*stdout=(FILE*)&streams[1],*stderr=(FILE*)&streams[2];
static DStream *stream(FILE *fp){
  uintptr_t p=(uintptr_t)fp,lo=(uintptr_t)streams,hi=(uintptr_t)(streams+D_STREAMS);
  if(p<lo||p>=hi||(p-lo)%sizeof(DStream))return NULL;
  DStream *s=(DStream*)fp;return s->used?s:NULL;
}
static DFile *find_file(const char *name){
  for(unsigned i=0;i<D_FILES;i++)if(files[i].used&&!strcmp(files[i].name,name))return &files[i];
  return NULL;
}
static DFile *new_file(const char *name){
  size_t n=strlen(name);if(!n||n>=sizeof files[0].name)return NULL;
  for(unsigned i=0;i<D_FILES;i++)if(!files[i].used){files[i].used=1;memcpy(files[i].name,name,n+1);return &files[i];}
  return NULL;
}
static DFile *get_file(const char *name){
  DFile *f=find_file(name);if(f)return f;
  if(__am_filelist)for(const struct file *a=__am_filelist;a->name;a++)if(!strcmp(a->name,name)){
    f=new_file(name);if(!f)return NULL;f->data=a->base;f->size=f->capacity=a->size;return f;
  }
  return NULL;
}
static int reserve(DFile *f,size_t length){
  if(length>D_FILE_MAX)return 0;
  if(f->owned&&length<=f->capacity)return 1;
  size_t capacity=f->capacity?f->capacity:256;if(capacity<length){while(capacity<length){if(capacity>D_FILE_MAX/2){capacity=D_FILE_MAX;break;}capacity*=2;}}
  if(capacity>D_FILE_MAX)return 0;
  uint8_t *data=f->owned?realloc(f->data,capacity):malloc(capacity);if(!data)return 0;
  if(!f->owned&&f->size)memcpy(data,f->data,f->size);
  f->data=data;f->capacity=capacity;f->owned=1;return 1;
}
FILE *fopen(const char *name,const char *mode){
  if(!name||!mode||!strchr("rwa",mode[0])||!mode[0])return NULL;
  int plus=0,binary=0,exclusive=0;
  for(const char *p=mode+1;*p;p++){
    if(*p=='+'&&!plus)plus=1;else if(*p=='b'&&!binary)binary=1;else if(*p=='x'&&!exclusive&&mode[0]=='w')exclusive=1;else return NULL;
  }
  DStream *s=NULL;for(unsigned i=3;i<D_STREAMS;i++)if(!streams[i].used){s=&streams[i];break;}if(!s)return NULL;
  DFile *f=get_file(name);if((mode[0]=='r'&&!f)||(exclusive&&f))return NULL;
  if(!f)f=new_file(name);
  if(!f)return NULL;
  if(mode[0]=='w'){if(f->owned)free(f->data);f->data=NULL;f->size=f->capacity=0;f->owned=1;}
  *s=(DStream){.used=1,.readable=mode[0]=='r'||plus,.writable=mode[0]!='r'||plus,.append=mode[0]=='a',.pushed=-1,.file=f};
  if(mode[0]=='a'&&!plus)s->position=f->size;
  return (FILE*)s;
}
int fclose(FILE *fp){DStream *s=stream(fp);if(!s)return EOF;s->used=0;return 0;}
int fgetc(FILE *fp){
  DStream *s=stream(fp);if(!s)return EOF;if(!s->readable){s->error=1;return EOF;}
  if(s->pushed>=0){int c=s->pushed;s->pushed=-1;s->position++;return c;}
  if(s->kind==1||s->position>=s->file->size){s->eof=1;return EOF;}
  return s->file->data[s->position++];
}
int getc(FILE *fp){return fgetc(fp);}
static int unread(DStream *s,int c){
  if(c==EOF||s->pushed>=0)return EOF;
  s->pushed=(unsigned char)c;s->eof=0;if(s->position)s->position--;return s->pushed;
}
size_t fread(void *ptr,size_t size,size_t count,FILE *fp){
  DStream *s=stream(fp);if(!s||!size||!count)return 0;
  if(!s->readable||!ptr||count>SIZE_MAX/size){s->error=1;return 0;}
  size_t wanted=size*count,got=0;uint8_t *p=ptr;
  if(s->pushed>=0){p[got++]=(uint8_t)s->pushed;s->pushed=-1;s->position++;}
  if(s->kind!=1&&s->position<s->file->size){size_t n=s->file->size-s->position;if(n>wanted-got)n=wanted-got;memcpy(p+got,s->file->data+s->position,n);s->position+=n;got+=n;}
  if(got<wanted)s->eof=1;
  return got/size;
}
size_t fwrite(const void *ptr,size_t size,size_t count,FILE *fp){
  DStream *s=stream(fp);if(!s||!size||!count)return 0;
  if(!s->writable||!ptr||count>SIZE_MAX/size){s->error=1;return 0;}
  size_t n=size*count;
  if(s->kind==2){const unsigned char *p=ptr;for(size_t i=0;i<n;i++)putch((char)p[i]);s->position+=n;return count;}
  if(s->append)s->position=s->file->size;
  if(s->position>D_FILE_MAX||n>D_FILE_MAX-s->position||!reserve(s->file,s->position+n)){s->error=1;return 0;}
  if(s->position>s->file->size)memset(s->file->data+s->file->size,0,s->position-s->file->size);
  memcpy(s->file->data+s->position,ptr,n);s->position+=n;if(s->position>s->file->size)s->file->size=s->position;return count;
}
int fseek(FILE *fp,long offset,int whence){
  DStream *s=stream(fp);if(!s||s->kind)return -1;
  int64_t base=whence==SEEK_SET?0:whence==SEEK_CUR?(int64_t)s->position:whence==SEEK_END?(int64_t)s->file->size:-1;
  if(base<0||offset< -base||offset>LONG_MAX-base){s->error=1;return -1;}
  s->position=(size_t)(base+offset);s->pushed=-1;s->eof=0;return 0;
}
long ftell(FILE *fp){DStream *s=stream(fp);if(!s||s->position>LONG_MAX)return -1;return (long)s->position;}
int feof(FILE *fp){DStream *s=stream(fp);return s?s->eof:0;}
int ferror(FILE *fp){DStream *s=stream(fp);return s?s->error:1;}
void clearerr(FILE *fp){DStream *s=stream(fp);if(s)s->eof=s->error=0;}
int fflush(FILE *fp){return !fp||stream(fp)?0:EOF;}
int fputc(int c,FILE *fp){unsigned char byte=(unsigned char)c;return fwrite(&byte,1,1,fp)==1?byte:EOF;}
int putc(int c,FILE *fp){return fputc(c,fp);}
int fputs(const char *s,FILE *fp){size_t n=strlen(s);return fwrite(s,1,n,fp)==n?0:EOF;}
int vfprintf(FILE *fp,const char *fmt,va_list ap){
  char small[256];va_list copy;va_copy(copy,ap);int n=vsnprintf(small,sizeof small,fmt,copy);va_end(copy);
  if(n<0||n>1024*1024){DStream *s=stream(fp);if(s)s->error=1;return -1;}
  char *buffer=small;
  if((size_t)n>=sizeof small){buffer=malloc((size_t)n+1);if(!buffer)return -1;va_copy(copy,ap);int m=vsnprintf(buffer,(size_t)n+1,fmt,copy);va_end(copy);if(m!=n){free(buffer);return -1;}}
  int result=fwrite(buffer,1,(size_t)n,fp)==(size_t)n?n:-1;if(buffer!=small)free(buffer);return result;
}
int fprintf(FILE *fp,const char *fmt,...){va_list ap;va_start(ap,fmt);int n=vfprintf(fp,fmt,ap);va_end(ap);return n;}
static int space(int c){return c==' '||c=='\n'||c=='\t'||c=='\r'||c=='\f'||c=='\v';}
static int skip_space(FILE *fp,DStream *s){int c;do{c=fgetc(fp);}while(c!=EOF&&space(c));if(c!=EOF)unread(s,c);return c;}
/* Required scanf subset: integer d/u/x/o, s/c, assignment suppression, widths,
 * h/hh/l/ll and literal %. Floating conversion/scansets are explicit errors. */
int vfscanf(FILE *fp,const char *fmt,va_list ap){
  DStream *s=stream(fp);if(!s||!s->readable)return EOF;int assigned=0;
  while(*fmt){
    if(space((unsigned char)*fmt)){while(space((unsigned char)*fmt))fmt++;skip_space(fp,s);continue;}
    if(*fmt!='%'){int c=fgetc(fp);if(c!=*fmt){if(c!=EOF)unread(s,c);return c==EOF&&!assigned?EOF:assigned;}fmt++;continue;}
    fmt++;if(*fmt=='%'){int c=fgetc(fp);fmt++;if(c!='%'){if(c!=EOF)unread(s,c);return c==EOF&&!assigned?EOF:assigned;}continue;}
    int suppress=0,width=0,length=0;if(*fmt=='*'){suppress=1;fmt++;}
    while(*fmt>='0'&&*fmt<='9'){if(width>100000){s->error=1;return assigned;}width=width*10+*fmt++-'0';}
    if(*fmt=='h'){length=-1;fmt++;if(*fmt=='h'){length=-2;fmt++;}}else if(*fmt=='l'){length=1;fmt++;if(*fmt=='l'){length=2;fmt++;}}
    char conversion=*fmt;if(!conversion){s->error=1;return assigned;}fmt++;
    if(conversion!='c'&&skip_space(fp,s)==EOF)return assigned?assigned:EOF;
    if(conversion=='s'||conversion=='c'){
      int maximum=width?width:(conversion=='c'?1:1048576),got=0;char *dest=suppress?NULL:va_arg(ap,char*);int c=0;
      while(got<maximum&&(c=fgetc(fp))!=EOF){if(conversion=='s'&&space(c)){unread(s,c);break;}if(dest)dest[got]=(char)c;got++;}
      if(!got)return c==EOF&&!assigned?EOF:assigned;
      if(dest&&conversion=='s')dest[got]=0;
      if(!suppress)assigned++;
      continue;
    }
    if(!strchr("duxo",conversion)){s->error=1;return assigned;}
    unsigned base=conversion=='x'?16:conversion=='o'?8:10;int maximum=width?width:96,c=fgetc(fp),negative=0,digits=0;
    if(c=='+'||c=='-'){negative=c=='-';maximum--;c=maximum?fgetc(fp):EOF;}
    if(base==16&&c=='0'&&maximum>1){int next=fgetc(fp);if(next=='x'||next=='X'){maximum-=2;c=maximum?fgetc(fp):EOF;}else if(next!=EOF)unread(s,next);}
    uint64_t value=0;
    while(maximum>0&&c!=EOF){
      unsigned digit=c>='0'&&c<='9'?(unsigned)(c-'0'):c>='a'&&c<='f'?(unsigned)(c-'a'+10):c>='A'&&c<='F'?(unsigned)(c-'A'+10):99;
      if(digit>=base)break;
      if(value>(UINT64_MAX-digit)/base){s->error=1;return assigned;}
      value=value*base+digit;digits++;maximum--;c=maximum?fgetc(fp):EOF;
    }
    if(c!=EOF)unread(s,c);
    if(!digits)return assigned;
    uint64_t bits=negative?UINT64_C(0)-value:value;
    if(!suppress){
      if(conversion=='d'){
        if(length==2)*va_arg(ap,long long*)=(long long)bits;else if(length==1)*va_arg(ap,long*)=(long)bits;else if(length==-1)*va_arg(ap,short*)=(short)bits;else if(length==-2)*va_arg(ap,signed char*)=(signed char)bits;else *va_arg(ap,int*)=(int)bits;
      }else{
        if(length==2)*va_arg(ap,unsigned long long*)=bits;else if(length==1)*va_arg(ap,unsigned long*)=(unsigned long)bits;else if(length==-1)*va_arg(ap,unsigned short*)=(unsigned short)bits;else if(length==-2)*va_arg(ap,unsigned char*)=(unsigned char)bits;else *va_arg(ap,unsigned*)=(unsigned)bits;
      }
      assigned++;
    }
  }
  return assigned;
}
int fscanf(FILE *fp,const char *fmt,...){va_list ap;va_start(ap,fmt);int n=vfscanf(fp,fmt,ap);va_end(ap);return n;}
#endif

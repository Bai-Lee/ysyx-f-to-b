/* Independent exercise17 extension. Fixed little-endian format, not struct dumps. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <string.h>
#include <errno.h>
#include <limits.h>
typedef struct {size_t max_rows,max_data,stride,total;unsigned char *bytes;} Database;
typedef struct {FILE *file;Database db;} Connection;
static void cleanup(Connection *c){if(c->file)fclose(c->file);free(c->db.bytes);c->file=NULL;c->db.bytes=NULL;}
static void fail(Connection *c,const char *s){fprintf(stderr,"ERROR: %s\n",s);cleanup(c);exit(1);}
static uint64_t number(Connection *c,const char *s){
    char *end;errno=0;if(!*s||*s=='-')fail(c,"invalid number");
    unsigned long long n=strtoull(s,&end,10);if(errno||*end)fail(c,"invalid number");return (uint64_t)n;
}
static uint64_t get64(const unsigned char *p){uint64_t n=0;for(unsigned i=0;i<8;i++)n|=(uint64_t)p[i]<<(8*i);return n;}
static void put64(unsigned char *p,uint64_t n){for(unsigned i=0;i<8;i++)p[i]=(unsigned char)(n>>(8*i));}
static uint32_t get32(const unsigned char *p){uint32_t n=0;for(unsigned i=0;i<4;i++)n|=(uint32_t)p[i]<<(8*i);return n;}
static void put32(unsigned char *p,uint32_t n){for(unsigned i=0;i<4;i++)p[i]=(unsigned char)(n>>(8*i));}
static uint64_t checksum(const unsigned char *p,size_t n){
    uint64_t h=UINT64_C(14695981039346656037);
    for(size_t i=0;i<n;i++){h^=p[i];h*=UINT64_C(1099511628211);}return h;
}
static void dimensions(Connection *c,uint64_t fields,uint64_t rows){
    if(!fields||!rows||fields>(SIZE_MAX-5)/3)fail(c,"invalid dimensions");
    c->db.max_data=(size_t)fields;c->db.max_rows=(size_t)rows;c->db.stride=5+3*(size_t)fields;
    if(rows>SIZE_MAX/c->db.stride)fail(c,"size overflow");
    c->db.total=(size_t)rows*c->db.stride;
    if(c->db.total>LONG_MAX-32)fail(c,"file size overflow");
}
static void allocate(Connection *c){c->db.bytes=calloc(1,c->db.total);if(!c->db.bytes)fail(c,"allocation failed");}
static unsigned char *row(Connection *c,size_t index){if(index>=c->db.max_rows)fail(c,"id out of range");return c->db.bytes+index*c->db.stride;}
static void load(Connection *c,const char *path){
    unsigned char h[32];c->file=fopen(path,"rb+");if(!c->file)fail(c,"open failed");
    if(fread(h,1,32,c->file)!=32||memcmp(h,"YSYXDB01",8))fail(c,"bad header");
    dimensions(c,get64(h+8),get64(h+16));
    if(fseek(c->file,0,SEEK_END)||ftell(c->file)!=(long)(32+c->db.total))fail(c,"wrong file length");
    rewind(c->file);if(fseek(c->file,32,SEEK_SET))fail(c,"seek failed");allocate(c);
    if(fread(c->db.bytes,1,c->db.total,c->file)!=c->db.total)fail(c,"read failed");
    if(checksum(c->db.bytes,c->db.total)!=get64(h+24))fail(c,"checksum mismatch");
    for(size_t i=0;i<c->db.max_rows;i++){
        unsigned char *r=row(c,i);if(r[0]>1)fail(c,"invalid set flag");
        if(r[0])for(size_t k=0;k<3;k++)if(!memchr(r+5+k*c->db.max_data,0,c->db.max_data))fail(c,"unterminated field");
    }
}
static void save(Connection *c){
    unsigned char h[32];memcpy(h,"YSYXDB01",8);put64(h+8,c->db.max_data);put64(h+16,c->db.max_rows);put64(h+24,checksum(c->db.bytes,c->db.total));
    rewind(c->file);
    if(fwrite(h,1,32,c->file)!=32||fwrite(c->db.bytes,1,c->db.total,c->file)!=c->db.total||fflush(c->file))fail(c,"write failed");
}
static void show(Connection *c,size_t i){
    unsigned char *r=row(c,i);if(!r[0])fail(c,"id not set");
    printf("%zu\t%s\t%s\t%s\t%" PRIu32 "\n",i,(char *)r+5,(char *)r+5+c->db.max_data,(char *)r+5+2*c->db.max_data,get32(r+1));
}
int main(int argc,char **argv){
    Connection local={0};Connection *c=&local;
    if(argc<3||strlen(argv[2])!=1)fail(c,"usage");
    char action=argv[2][0];
    if(action=='c'||action=='p'){
        if(argc!=5)fail(c,"create/probe needs field bytes and rows");
        dimensions(c,number(c,argv[3]),number(c,argv[4]));allocate(c);
        if(action=='p'){printf("allocated=%zu checksum=%" PRIu64 "\n",c->db.total,checksum(c->db.bytes,c->db.total));cleanup(c);return 0;}
        c->file=fopen(argv[1],"wb+");if(!c->file)fail(c,"create failed");save(c);
    }else{
        load(c,argv[1]);
        if(action=='s'){
            if(argc!=8)fail(c,"set needs id,name,email,city,age");
            size_t i=(size_t)number(c,argv[3]);unsigned char *r=row(c,i);if(r[0])fail(c,"already set");
            uint64_t age=number(c,argv[7]);if(age>UINT32_MAX)fail(c,"age overflow");
            r[0]=1;put32(r+1,(uint32_t)age);
            for(size_t k=0;k<3;k++)snprintf((char *)r+5+k*c->db.max_data,c->db.max_data,"%s",argv[4+k]);
            save(c);
        }else if(action=='g'||action=='d'){
            if(argc!=4)fail(c,"id required");
            size_t i=(size_t)number(c,argv[3]);unsigned char *r=row(c,i);
            if(action=='g')show(c,i);else{memset(r,0,c->db.stride);save(c);}
        }else if(action=='l'){
            if(argc!=3)fail(c,"list argument count");
            for(size_t i=0;i<c->db.max_rows;i++)if(row(c,i)[0])show(c,i);
        }else if(action=='f'){
            if(argc!=5)fail(c,"find needs field and query");
            int column=!strcmp(argv[3],"name")?0:!strcmp(argv[3],"email")?1:!strcmp(argv[3],"city")?2:!strcmp(argv[3],"age")?3:-1;
            if(column<0)fail(c,"unknown field");
            uint64_t age=column==3?number(c,argv[4]):0;
            for(size_t i=0;i<c->db.max_rows;i++){
                unsigned char *r=row(c,i);if(!r[0])continue;
                if(column==3?(age==get32(r+1)):(strstr((char *)r+5+(size_t)column*c->db.max_data,argv[4])!=NULL))show(c,i);
            }
        }else fail(c,"unknown action");
    }
    cleanup(c);return 0;
}

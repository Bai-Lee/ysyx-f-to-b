#include <stdio.h>
#include <dlfcn.h>
#include <stddef.h>
typedef int(*F)(const unsigned char*,size_t);
int main(int argc,char**argv){if(argc!=2)return 2;void*h=dlopen(argv[1],RTLD_NOW);if(!h)return 3;F f=(F)dlsym(h,"uppercase_n");if(!f)return 4;unsigned char data[4]={'a',0,'b',255};int rc=f(data,4);dlclose(h);return rc;}

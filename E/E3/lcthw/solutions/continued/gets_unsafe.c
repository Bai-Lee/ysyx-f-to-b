#include <stdio.h>
#include <stdlib.h>
extern char *gets(char *);
int main(void){char *p=malloc(16);if(!p)return 2;gets(p);free(p);return 0;}

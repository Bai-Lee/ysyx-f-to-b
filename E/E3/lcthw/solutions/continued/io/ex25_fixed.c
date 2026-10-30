#include <limits.h>
#include <ctype.h>
/** WARNING: This code is fresh and potentially isn't correct yet. */

#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include "dbg.h"

#define MAX_DATA 100

int read_string(char **out_string,int max_buffer){
    *out_string=NULL;if(max_buffer<1||max_buffer>1000000)return -1;
    char *p=malloc((size_t)max_buffer+1);if(!p)return -1;
    int ch,overflow=0;size_t n=0;
    while((ch=fgetc(stdin))!=EOF&&ch!='\n'){if(ch==0)overflow=1;if(n<(size_t)max_buffer)p[n++]=(char)ch;else overflow=1;}
    p[n]=0;if(overflow||(ch==EOF&&n==0)){free(p);return -1;}*out_string=p;return 0;
}
int read_int(int *out_int){
    char *p=NULL,*end;int rc=read_string(&p,MAX_DATA);if(rc)return -1;
    errno=0;long v=strtol(p,&end,10);int bad=end==p||errno||v<INT_MIN||v>INT_MAX;
    while(isspace((unsigned char)*end)){end++;}
    if(*end)bad=1;
    if(!bad){*out_int=(int)v;}
    free(p);return bad?-1:0;
}
int tiny_print(const char *fmt,...){
    va_list ap;va_start(ap,fmt);int count=0;
    for(size_t i=0;fmt[i];i++){
        if(fmt[i]!='%'){if(putchar(fmt[i])==EOF){va_end(ap);return -1;}count++;continue;}
        i++;int rc=0;
        if(fmt[i]=='d')rc=printf("%d",va_arg(ap,int));
        else if(fmt[i]=='c')rc=printf("%c",va_arg(ap,int));
        else if(fmt[i]=='s'){char *s=va_arg(ap,char *);if(!s){va_end(ap);return -1;}rc=printf("%s",s);}
        else if(fmt[i]=='%'){putchar('%');rc=1;}
        else{va_end(ap);return -1;}
        if(rc<0){va_end(ap);return -1;}count+=rc;
    }
    va_end(ap);return count;
}
int read_scan(const char *fmt, ...)
{
    int i = 0;
    int rc = 0;
    int *out_int = NULL;
    char *out_char = NULL;
    char **out_string = NULL;
    int max_buffer = 0;

    va_list argp;
    va_start(argp, fmt);

    for(i = 0; fmt[i] != '\0'; i++) {
        if(fmt[i] == '%') {
            i++;
            switch(fmt[i]) {
                case '\0':
                    sentinel("Invalid format, you ended with %%.");
                    break;

                case 'd':
                    out_int = va_arg(argp, int *);
                    rc = read_int(out_int);
                    check(rc == 0, "Failed to read int.");
                    break;

                case 'c':
                    out_char = va_arg(argp, char *);
                    int input_char=fgetc(stdin);
                    check(input_char!=EOF,"EOF reading character");
                    *out_char=(char)input_char;
                    break;

                case 's':
                    max_buffer = va_arg(argp, int);
                    out_string = va_arg(argp, char **);
                    rc = read_string(out_string, max_buffer);
                    check(rc == 0, "Failed to read string.");
                    break;

                default:
                    sentinel("Invalid format.");
            }
        } else {
            int literal=fgetc(stdin);
            check(literal==(unsigned char)fmt[i],"Literal mismatch");
        }

        check(!feof(stdin) && !ferror(stdin), "Input error.");
    }

    va_end(argp);
    return 0;

error:
    va_end(argp);
    return -1;
}



int main(int argc, char *argv[])
{
    char *first_name = NULL;
    char initial = ' ';
    char *last_name = NULL;
    int age = 0;

    tiny_print("What's your first name? ");
    int rc = read_scan("%s", MAX_DATA, &first_name);
    check(rc == 0, "Failed first name.");

    tiny_print("What's your initial? ");
    rc = read_scan("%c\n", &initial);
    check(rc == 0, "Failed initial.");

    tiny_print("What's your last name? ");
    rc = read_scan("%s", MAX_DATA, &last_name);
    check(rc == 0, "Failed last name.");

    tiny_print("How old are you? ");
    rc = read_scan("%d", &age);
    check(rc==0,"Failed age");

    tiny_print("---- RESULTS ----\n");
    tiny_print("First Name: %s\n", first_name);
    tiny_print("Initial: '%c'\n", initial);
    tiny_print("Last Name: %s\n", last_name);
    tiny_print("Age: %d\n", age);

    free(first_name);
    free(last_name);
    return 0;
error:
    free(first_name);free(last_name);
    return -1;
}

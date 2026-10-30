#include <stdio.h>
#include <ctype.h>
#include "dbg.h"


int print_a_message(const char *msg)
{
    printf("A STRING: %s\n", msg);

    return 0;
}


int uppercase(const char *msg)
{
    int i = 0;

    // BUG: \0 termination problems
    for(i = 0; msg[i] != '\0'; i++) {
        printf("%c", toupper(msg[i]));
    }

    printf("\n");

    return 0;
}

int lowercase(const char *msg)
{
    int i = 0;

    // BUG: \0 termination problems
    for(i = 0; msg[i] != '\0'; i++) {
        printf("%c", tolower(msg[i]));
    }

    printf("\n");

    return 0;
}

int fail_on_purpose(const char *msg)
{
    return 1;
}

#include <stddef.h>
int uppercase_n(const unsigned char *msg,size_t n){for(size_t i=0;i<n;i++)putchar(toupper(msg[i]));return 0;}
int lowercase_n(const unsigned char *msg,size_t n){for(size_t i=0;i<n;i++)putchar(tolower(msg[i]));return 0;}
int print_a_message_n(const unsigned char *msg,size_t n){fputs("A STRING: ",stdout);return fwrite(msg,1,n,stdout)==n?0:1;}

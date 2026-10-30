#include <stdio.h>
#include <limits.h>
int main(void) {
    printf("int=%zu long=%zu pointer=%zu CHAR_BIT=%d\n",
           sizeof(int),sizeof(long),sizeof(void *),CHAR_BIT);
    return 0;
}

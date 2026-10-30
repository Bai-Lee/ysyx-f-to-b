#include <assert.h>
#include <stdio.h>
#include <stddef.h>
#include <stdint.h>
#include <inttypes.h>
#include <limits.h>
#include <string.h>

int main(void) {
    char text[128];
    int written = -1;
    int numbers[4] = {1, 2, 3, 4};
    char name[4] = {'Z','e','d','\0'};
    unsigned long wrap = ULONG_MAX;
    uint32_t packed;
    unsigned char roundtrip[4];
    signed char tiny = -5;
    short small = -12;
    long large = -123;
    long long larger = -1234567890123LL;
    intmax_t widest = -987654321;
    ptrdiff_t difference = &numbers[3] - &numbers[0];

    snprintf(text,sizeof text,"%#x %#o %08u",42u,42u,42u);
    assert(strcmp(text,"0x2a 052 00000042")==0);
    snprintf(text,sizeof text,"[%8.3s][%-5s][%s]","abcdef","xy","");
    assert(strcmp(text,"[     abc][xy   ][]")==0);
    snprintf(text,sizeof text,"%.2f %+.1f %.1a",3.14159,-0.0,1.5);
    assert(strcmp(text,"3.14 -0.0 0x1.8p+0")==0);
    snprintf(text,sizeof text,"%hhd %hd %ld %lld %jd %zu %td %.2Lf",
             tiny,small,large,larger,widest,sizeof name,difference,1.25L);
    assert(strcmp(text,"-5 -12 -123 -1234567890123 -987654321 4 3 1.25")==0);
    snprintf(text,sizeof text,"hi%n",&written);
    assert(written==2 && strcmp(text,"hi")==0);
    snprintf(text,sizeof text,"A%cB%cC%cD",'\t','\n','\r');
    assert(strcmp(text,"A\tB\nC\rD")==0);

    ++wrap;
    assert(wrap==0); /* Defined unsigned arithmetic modulo 2^width. */
    assert(100 * '\0' == 0);
    assert((int)'A' * 2 == 130); /* ASCII on these explicitly tested targets. */
    numbers[0]=100;
    numbers[1]='Q';
    name[0]='R';
    name[1]=(char)101;
    assert(numbers[0]==100 && numbers[1]==81 && strcmp(name,"Red")==0);
    snprintf(text,sizeof text,"%c %d %02x",numbers[1],name[0],(unsigned)(unsigned char)name[0]);
    assert(strcmp(text,"Q 82 52")==0);
    name[0]='Z';
    assert(sizeof name==4 && CHAR_BIT==8 && sizeof packed==4);
    memcpy(&packed,name,sizeof packed); /* No alignment or strict-aliasing violation. */
    memcpy(roundtrip,&packed,sizeof roundtrip);
    assert(memcmp(roundtrip,name,sizeof name)==0);
    printf("ABI int=%zu long=%zu pointer=%zu CHAR_BIT=%d\n",
           sizeof(int),sizeof(long),sizeof(void *),CHAR_BIT);
    printf("NAME bytes=%02x %02x %02x %02x packed=%08" PRIx32 "\n",
           (unsigned)roundtrip[0],(unsigned)roundtrip[1],
           (unsigned)roundtrip[2],(unsigned)roundtrip[3],packed);
    puts("PASS formats unsigned_promotions arrays safe_object_copy");
    return 0;
}

#include <stdint.h>
#include <limits.h>
_Static_assert(sizeof(uint32_t)==4,"uint32");
_Static_assert(sizeof(void*)==4,"RV32 pointers");
_Static_assert(__STDC_HOSTED__==0,"freestanding");
int f(void){return CHAR_BIT;}

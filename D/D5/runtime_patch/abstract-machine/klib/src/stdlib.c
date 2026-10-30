#include <klib.h>

#if !defined(__ISA_NATIVE__) || defined(__NATIVE_USE_KLIB__)
static unsigned long int next = 1;

int rand(void) {
  // RAND_MAX assumed to be 32767
  next = next * 1103515245 + 12345;
  return (unsigned int)(next/65536) % 32768;
}

void srand(unsigned int seed) {
  next = seed;
}

int abs(int x) {
  return (x < 0 ? -x : x);
}

#define def_strtoXXX(type, name) \
  type name(const char *nptr, char **endptr, int base) { \
    type x = 0; \
    while (isspace(*nptr)) { nptr ++; } \
    if (base == 0) { \
      base = (nptr[0] != '0') ? 10 : (tolower(nptr[1]) == 'x' ? 16 : 8); \
    } \
    if ((base == 16) && (nptr[0] == '0' && tolower(nptr[1]) == 'x')) { nptr += 2; } \
    while (isalnum(*nptr)) { \
      if (base == 8  && !(*nptr >= '0' && *nptr <= '7')) break; \
      if (base == 10 && !isdigit(*nptr)) break; \
      if (base == 16 && !isxdigit(*nptr)) break; \
      int d = isalpha(*nptr) ? tolower(*nptr) - 'a' + 10 : *nptr - '0'; \
      x = x * base + d; \
      nptr ++; \
    } \
    if (endptr) { \
      *(const char **)endptr = nptr; \
    } \
    return x; \
  }

def_strtoXXX(long, strtol)
def_strtoXXX(unsigned long, strtoul)
def_strtoXXX(long long, strtoll)
def_strtoXXX(unsigned long long, strtoull)

int atoi(const char* nptr) {
  return strtol(nptr, NULL, 10);
}

/* Allocation is implemented in alloc.c, with a native-host bridge. */

#ifndef __ISA_NATIVE__
void exit(int status) {
  halt(status);
}
#endif

#endif

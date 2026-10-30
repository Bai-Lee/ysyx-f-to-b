#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#ifndef INJECT_FAULT
#define INJECT_FAULT 0
#endif
static volatile int running_total;
__attribute__((noinline)) static int sum_sequence(const int *values, size_t count) {
  for (size_t i = 0; i < count; ++i) {
    int term = values[i];
    if (INJECT_FAULT && i == 3) term += 1;
    running_total += term;
  }
  return running_total;
}
int main(void) {
  const int values[] = {1, 2, 3, 4, 5};
  int result = sum_sequence(values, sizeof values / sizeof values[0]);
  printf("SUM_RESULT=%d expected=15\n", result);
  fflush(stdout);
  assert(result == 15);
  return 0;
}

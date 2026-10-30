#include <stdio.h>
#include "api.h"
int main(void) {
  int result = add_to_counter(5);
  printf("%s counter=%d zero=%d\n", banner, result, zero_counter);
  return result == 15 && counter == 15 && zero_counter == 0 ? 0 : 1;
}

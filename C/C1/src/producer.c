#include "api.h"
int counter = 7;
int zero_counter;
const char banner[] = "ELF_LINK_PASS";
static int bias = 3;
int add_to_counter(int value) {
  counter += value + bias;
  return counter;
}

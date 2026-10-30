#include <stdio.h>
int main(void) {
  int i=0, sum=0;
  while(i!=10) { i=i+1; sum=sum+i; }
  printf("sum = %d\n",sum);
  return 0;
}

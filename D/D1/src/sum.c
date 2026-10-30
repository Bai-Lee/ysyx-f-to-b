#include <stdio.h>
#include <stdlib.h>
int main(int argc,char **argv){unsigned long long n=argc==2?strtoull(argv[1],0,10):100000000ULL;if(n>1000000000ULL)return 2;unsigned long long sum=0;for(unsigned long long i=1;i<=n;i++)sum+=i;printf("%llu\n",sum);return 0;}

#define _POSIX_C_SOURCE 200809L
#include <lcthw/extensions.h>
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include <time.h>
#include <assert.h>
static uint64_t comparisons;
static int cmp(const void *a,const void *b){comparisons++;int x=*(const int*)a,y=*(const int*)b;return(x>y)-(x<y);}
static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return (double)t.tv_sec+1e-9*(double)t.tv_nsec;}
int main(int argc,char **argv){
    if(argc!=3)return 2;int method=atoi(argv[1]),n=atoi(argv[2]);if(n<1||n>100000||method<0||method>3)return 2;
    int *data=malloc((size_t)n*sizeof(int));assert(data);unsigned seed=260733u+(unsigned)n;
    for(int i=0;i<n;i++){seed=seed*1664525u+1013904223u;data[i]=(int)(seed%100000);}
    double elapsed=0;uint64_t rounds=0,total_cmp=0;
    while(elapsed<3.0){
        comparisons=0;double start=now();List *input=List_create();assert(input);
        for(int i=0;i<n;i++){if(method==3)assert(List_insert_sorted(input,&data[i],cmp)==0);else List_push(input,&data[i]);}
        List *result=input;
        if(method==0)List_bubble_sort(input,cmp);
        else if(method==1){result=List_merge_sort(input,cmp);List_destroy(input);}
        else if(method==2)List_bottom_up_sort(input,cmp);
        elapsed+=now()-start;total_cmp+=comparisons;rounds++;
        assert(result->count==n);ListNode *p=result->first;
        while(p&&p->next){assert(*(int*)p->value<=*(int*)p->next->value);p=p->next;}
        List_destroy(result);
    }
    printf("%d,%d,%" PRIu64 ",%.9f,%.3f,%.3f\n",method,n,rounds,elapsed,elapsed*1e6/(double)rounds,(double)total_cmp/(double)rounds);
    free(data);return 0;
}

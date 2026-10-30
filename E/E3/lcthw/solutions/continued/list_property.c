#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <lcthw/extensions.h>
typedef struct{int key,index;} Item;
static int cmp(const void *a,const void *b){const Item *x=a,*y=b;return (x->key>y->key)-(x->key<y->key);}
static int reference_cmp(const void *a,const void *b){const Item *x=*(Item *const *)a,*y=*(Item *const *)b;int c=cmp(x,y);return c?c:(x->index>y->index)-(x->index<y->index);}
static void verify(List *l,void **ref,int n){
    assert(l->count==n);ListNode *prev=NULL,*p=l->first;
    for(int i=0;i<n;i++){assert(p&&p->prev==prev&&p->value==ref[i]);prev=p;p=p->next;}
    assert(!p&&prev==l->last);ListNode *next=NULL;p=l->last;
    for(int i=n;i>0;){--i;assert(p&&p->next==next&&p->value==ref[i]);next=p;p=p->prev;}
    assert(!p&&next==l->first);
}
int main(void){
    int values[4096];void *ref[4096];int count=0;unsigned rng=260732;List *l=List_create();assert(l);
    for(int step=0;step<3000;step++){
        rng=rng*1664525u+1013904223u;int op=(int)(rng%6);values[step]=step;
        if(op==0){List_push(l,&values[step]);ref[count++]=&values[step];}
        else if(op==1){List_unshift(l,&values[step]);memmove(ref+1,ref,(size_t)count*sizeof(void*));ref[0]=&values[step];count++;}
        else if(op==2){void *v=List_pop(l);assert(v==(count?ref[--count]:NULL));}
        else if(op==3){void *v=List_shift(l);assert(v==(count?ref[0]:NULL));if(count){count--;memmove(ref,ref+1,(size_t)count*sizeof(void*));}}
        else if(op==4){List *copy=List_copy_nodes(l);assert(copy);verify(copy,ref,count);if(count)assert(copy->first!=l->first);List_destroy(copy);}
        else{int at=count?(int)(rng%(unsigned)(count+1)):0;List *tail=List_split_transfer(l,at);assert(tail);verify(l,ref,at);verify(tail,ref+at,count-at);assert(List_concat_transfer(l,tail)==0);assert(!tail->count);List_destroy(tail);}
        verify(l,ref,count);assert(List_concat_transfer(l,l)==-1);assert(List_split_transfer(l,count+1)==NULL);
    }
    List_destroy(l);
    for(int n=0;n<=64;n++){
        Item data[64];Item *expected[64];
        for(int i=0;i<n;i++){rng=rng*1664525u+1013904223u;data[i]=(Item){(int)(rng%17)-8,i};expected[i]=&data[i];}
        qsort(expected,(size_t)n,sizeof(Item*),reference_cmp);
        for(int method=0;method<4;method++){
            List *input=List_create();assert(input);for(int i=0;i<n;i++){if(method==3)assert(List_insert_sorted(input,&data[i],cmp)==0);else List_push(input,&data[i]);}
            List *result=input;
            if(method==0)assert(List_bubble_sort(input,cmp)==0);
            else if(method==1){result=List_merge_sort(input,cmp);assert(result!=input);}
            else if(method==2)assert(List_bottom_up_sort(input,cmp)==0);
            verify(result,(void**)expected,n);
            if(result!=input)List_destroy(result);List_destroy(input);
        }
    }
    puts("PASS 3000 ownership operations and260 stable sorting cases");return 0;
}

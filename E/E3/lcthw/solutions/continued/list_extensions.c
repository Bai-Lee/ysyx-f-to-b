#include <lcthw/list.h>
#include <lcthw/list_algos.h>
#include <limits.h>

/* Copies nodes; values remain borrowed. */
List *List_copy_nodes(const List *list){
    List *out=List_create();if(!out)return NULL;
    for(ListNode *p=list->first;p;p=p->next){int before=out->count;List_push(out,p->value);if(out->count!=before+1){List_destroy(out);return NULL;}}
    return out;
}
/* Transfers nodes; source becomes empty and retains its own header. */
int List_concat_transfer(List *dst,List *src){
    if(!dst||!src||dst==src||dst->count>INT_MAX-src->count)return -1;
    if(!src->count)return 0;
    if(dst->last){dst->last->next=src->first;src->first->prev=dst->last;}else dst->first=src->first;
    dst->last=src->last;dst->count+=src->count;src->first=src->last=NULL;src->count=0;return 0;
}
List *List_split_transfer(List *src,int at){
    if(!src||at<0||at>src->count)return NULL;
    List *tail=List_create();if(!tail)return NULL;
    if(at==src->count)return tail;
    ListNode *cut=src->first;for(int i=0;i<at;i++)cut=cut->next;
    tail->first=cut;tail->last=src->last;tail->count=src->count-at;
    if(cut->prev){src->last=cut->prev;src->last->next=NULL;}else src->first=src->last=NULL;
    cut->prev=NULL;src->count=at;return tail;
}
int List_insert_sorted(List *list,void *value,List_compare cmp){
    if(!list||list->count==INT_MAX)return -1;
    ListNode *next=list->first;while(next&&cmp(next->value,value)<=0)next=next->next;
    ListNode *node=calloc(1,sizeof *node);if(!node)return -1;node->value=value;node->next=next;
    if(next){node->prev=next->prev;next->prev=node;}else{node->prev=list->last;list->last=node;}
    if(node->prev)node->prev->next=node;else list->first=node;
    ++list->count;return 0;
}
int List_bottom_up_sort(List *list,List_compare cmp){
    if(list->count<2)return 0;
    for(size_t width=1;width<(size_t)list->count;width*=2){
        ListNode *p=list->first,*head=NULL,*tail=NULL;
        while(p){
            ListNode *q=p;size_t left=0,right=width;
            for(size_t i=0;i<width&&q;i++){left++;q=q->next;}
            while(left||(right&&q)){
                ListNode *take;
                if(!left){take=q;q=q->next;right--;}
                else if(!right||!q){take=p;p=p->next;left--;}
                else if(cmp(p->value,q->value)<=0){take=p;p=p->next;left--;}
                else{take=q;q=q->next;right--;}
                take->prev=tail;if(tail)tail->next=take;else head=take;tail=take;
            }
            p=q;
        }
        tail->next=NULL;list->first=head;list->last=tail;
    }
    return 0;
}

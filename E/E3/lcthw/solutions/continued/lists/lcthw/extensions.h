#include <lcthw/list.h>
#include <lcthw/list_algos.h>
List *List_copy_nodes(const List *);
int List_concat_transfer(List *,List *);
List *List_split_transfer(List *,int);
int List_insert_sorted(List *,void *,List_compare);
int List_bottom_up_sort(List *,List_compare);

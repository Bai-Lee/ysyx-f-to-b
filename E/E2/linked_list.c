/* E2 independent competence branch. No external linked-list implementation used.
 * C17 singly linked list; failure-atomic insert; stable recursive merge sort.
 * The test reference is a contiguous integer array, not a second linked list.
 */
#include <assert.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node { int value; struct Node *next; } Node;
typedef struct List { Node *head, *tail; size_t length; } List;
static size_t live_nodes;
static long allocation_limit = -1;

void list_limit_allocations(long limit) { allocation_limit = limit; }
size_t list_live_nodes(void) { return live_nodes; }
List *list_create(void) { return calloc(1, sizeof(List)); }
size_t list_size(const List *list) { return list->length; }

static Node *new_node(int value) {
    Node *node;
    if (allocation_limit == 0) return NULL;
    node = malloc(sizeof(*node));
    if (!node) return NULL;
    if (allocation_limit > 0) --allocation_limit;
    node->value = value; node->next = NULL; ++live_nodes;
    return node;
}
static void release_node(Node *node) {
    assert(live_nodes != 0); --live_nodes; free(node);
}
int list_insert(List *list, size_t index, int value) {
    Node *node, *previous;
    if (index > list->length) return 0;
    node = new_node(value);
    if (!node) return 0;
    if (index == 0) {
        node->next = list->head; list->head = node;
        if (list->length == 0) list->tail = node;
    } else {
        previous = list->head;
        for (size_t i = 1; i < index; ++i) previous = previous->next;
        node->next = previous->next; previous->next = node;
        if (index == list->length) list->tail = node;
    }
    ++list->length;
    return 1;
}
int list_get(const List *list, size_t index, int *value) {
    const Node *node;
    if (index >= list->length || value == NULL) return 0;
    node = list->head;
    for (size_t i = 0; i < index; ++i) node = node->next;
    *value = node->value; return 1;
}
int list_erase(List *list, size_t index, int *value) {
    Node *node, *previous = NULL;
    if (index >= list->length) return 0;
    node = list->head;
    for (size_t i = 0; i < index; ++i) { previous = node; node = node->next; }
    if (previous) previous->next = node->next; else list->head = node->next;
    if (node == list->tail) list->tail = previous;
    if (value) *value = node->value;
    --list->length; release_node(node); return 1;
}
void list_clear(List *list) {
    Node *node = list->head;
    while (node) { Node *next = node->next; release_node(node); node = next; }
    list->head = NULL; list->tail = NULL; list->length = 0;
}
void list_destroy(List *list) { if (list) { list_clear(list); free(list); } }
void list_reverse(List *list) {
    Node *previous = NULL, *node = list->head;
    list->tail = list->head;
    while (node) {
        Node *next = node->next; node->next = previous; previous = node; node = next;
    }
    list->head = previous;
}
static Node *merge_sorted(Node *left, Node *right) {
    Node dummy = {0, NULL}, *last = &dummy;
    while (left && right) {
        if (left->value <= right->value) { last->next = left; left = left->next; }
        else { last->next = right; right = right->next; }
        last = last->next;
    }
    last->next = left ? left : right;
    return dummy.next;
}
static Node *merge_sort(Node *head) {
    Node *slow, *fast, *second;
    if (!head || !head->next) return head;
    slow = head; fast = head->next;
    while (fast && fast->next) { slow = slow->next; fast = fast->next->next; }
    second = slow->next; slow->next = NULL;
    return merge_sorted(merge_sort(head), merge_sort(second));
}
void list_sort(List *list) {
    list->head = merge_sort(list->head); list->tail = list->head;
    if (list->tail) while (list->tail->next) list->tail = list->tail->next;
}
/* Returns full length, copies at most capacity entries; NULL is allowed at cap0. */
size_t list_snapshot(const List *list, int *values, size_t capacity) {
    const Node *node = list->head; size_t count = 0;
    while (node) {
        if (count < capacity) values[count] = node->value;
        ++count; node = node->next;
    }
    return count;
}
int list_validate(const List *list) {
    const Node *slow = list->head, *fast = list->head, *last = NULL;
    size_t count = 0;
    while (fast && fast->next) {
        slow = slow->next; fast = fast->next->next;
        if (slow == fast) return 0;
    }
    for (const Node *node = list->head; node; node = node->next) { ++count; last = node; }
    return count == list->length && last == list->tail &&
        ((count == 0) == (list->head == NULL && list->tail == NULL));
}

#ifndef LIST_LIBRARY
static void verify(const List *list, const int *reference, size_t count) {
    int snapshot[512];
    assert(count <= 512);
    assert(list_validate(list)); assert(list_size(list) == count);
    assert(list_snapshot(list, snapshot, 512) == count);
    for (size_t i = 0; i < count; ++i) assert(snapshot[i] == reference[i]);
    assert(list_live_nodes() == count);
}
static uint32_t next_random(uint32_t *state) {
    uint32_t x = *state; x ^= x << 13; x ^= x >> 17; x ^= x << 5; *state = x; return x;
}
static int order_ints(const void *a, const void *b) {
    const int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}
int main(void) {
    List *list = list_create(); int reference[512] = {0}; size_t length = 0;
    uint32_t seed = UINT32_C(260702); size_t operations = 0;
    assert(list); verify(list, reference, 0);
    assert(!list_insert(list, SIZE_MAX, 4)); assert(!list_get(list, 0, NULL));
    for (size_t i = 0; i < 20000; ++i) {
        unsigned op = next_random(&seed) % 7;
        size_t index = (size_t)next_random(&seed) % (length + 2);
        int value = (int)(next_random(&seed) % 2001) - 1000, old = INT_MIN;
        if (i % 31 == 0) value = INT_MAX;
        if (i % 37 == 0) value = INT_MIN;
        if (length > 200) op = 5;
        if (op == 0 || op == 1) {
            int success = list_insert(list, index, value);
            assert(success == (index <= length));
            if (success) {
                memmove(reference + index + 1, reference + index, (length-index)*sizeof(int));
                reference[index] = value; ++length;
            }
        } else if (op == 2) {
            int success = list_erase(list, index, &old);
            assert(success == (index < length));
            if (success) {
                assert(old == reference[index]);
                memmove(reference + index, reference + index + 1, (length-index-1)*sizeof(int)); --length;
            } else assert(old == INT_MIN);
        } else if (op == 3) {
            list_reverse(list);
            for (size_t j = 0; j < length/2; ++j) { int tmp = reference[j]; reference[j] = reference[length-j-1]; reference[length-j-1] = tmp; }
        } else if (op == 4) { list_sort(list); qsort(reference, length, sizeof(int), order_ints); }
        else if (op == 5) { list_clear(list); length = 0; }
        else {
            list_limit_allocations(0); assert(!list_insert(list, length/2, value)); list_limit_allocations(-1);
        }
        verify(list, reference, length); ++operations;
    }
    list_clear(list); verify(list, reference, 0); list_clear(list); list_destroy(list); list_destroy(NULL);
    assert(list_live_nodes() == 0);
    printf("PASS E2 linked_list selftest operations=%zu live_nodes=%zu\n",operations,list_live_nodes());
    return 0;
}
#endif

/* Deliberately incorrect negative control: Valgrind must reject this binary. */
#include <stdlib.h>
int main(void) {
    volatile size_t length = 17;
    char *buffer = malloc(length);
    if (!buffer) return 2;
    buffer[length] = 1; /* Deliberate one-byte out-of-bounds write. */
    return 0;          /* Deliberate leak. */
}

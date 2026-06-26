#define _GNU_SOURCE
#include <unistd.h>
#include <stdlib.h>

void abort(void) {
    _exit(134);
}

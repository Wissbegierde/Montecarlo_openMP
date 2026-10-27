#include <stdio.h>
#include "rng_lcg.h"

int main(void) {
    unsigned int a = 2221886u, b = 2221886u;
    unsigned long long n = 2000000ull;
    unsigned long long i;
    for (i = 0; i < n; i++)
        lcg_rand(&a);
    lcg_skip(&b, n);
    printf("estado paso a paso: %u\n", a);
    printf("estado con skip:    %u\n", b);
    return a == b ? 0 : 1;
}

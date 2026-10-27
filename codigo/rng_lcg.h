#ifndef RNG_LCG_H
#define RNG_LCG_H

/* LCG de tipo rand_r (glibc): X_{n+1} = a X_n + c  (mod 2^32).
   Salida en {0,...,32767}. El salto permite que cada hilo arranque
   N/p muestras mas adelante en el mismo flujo, sin solaparse. */

#define LCG_A 1103515245u
#define LCG_C 12345u
#define LCG_RAND_MAX 32767

static inline unsigned int lcg_rand(unsigned int *estado) {
    *estado = (*estado) * LCG_A + LCG_C;
    return (*estado / 65536u) % 32768u;
}

/* Avanza n pasos: X <- a^n X + c (a^n-1)/(a-1)  (mod 2^32). */
static inline void lcg_skip(unsigned int *estado, unsigned long long n) {
    unsigned int a_cur = LCG_A;
    unsigned int c_cur = LCG_C;
    unsigned int a_n = 1u;
    unsigned int c_n = 0u;
    while (n > 0ull) {
        if (n & 1ull) {
            c_n = a_cur * c_n + c_cur;
            a_n = a_cur * a_n;
        }
        c_cur = c_cur * (a_cur + 1u);
        a_cur = a_cur * a_cur;
        n >>= 1;
    }
    *estado = a_n * (*estado) + c_n;
}

#endif

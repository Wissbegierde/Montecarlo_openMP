/* montecarlo_omp.cpp -- Monte Carlo paralelo con OpenMP.
   Uso: ./montecarlo_omp <N> <p>
   Compilar: gcc -O2 -fopenmp montecarlo_omp.cpp -o montecarlo_omp -lm

   Cada muestra i consume 2 llamadas al LCG. El hilo que recibe el bloque
   estatico [i0, i1) salta 2*i0 pasos desde SEMILLA_BASE. Asi el flujo
   global es el de la version secuencial y la estimacion no depende de p. */
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include "rng_lcg.h"

#define SEMILLA_BASE 2221886u

int main(int argc, char *argv[]) {
    long N = (argc > 1) ? atol(argv[1]) : 100000000L;
    int p = (argc > 2) ? atoi(argv[2]) : 0;
    if (p > 0)
        omp_set_num_threads(p);

    long dentro = 0;
    long i0 = -1L;
    unsigned int estado = 0;
    double t0 = omp_get_wtime();

    /* schedule(static): un bloque contiguo por hilo; el salto es 2*(N/p)
       llamadas al LCG (dos por muestra), sin solapar flujos. */
#pragma omp parallel for schedule(static) reduction(+ : dentro) firstprivate(i0) private(estado)
    for (long i = 0; i < N; i++) {
        if (i0 < 0) {
            i0 = i;
            estado = SEMILLA_BASE;
            lcg_skip(&estado, 2ull * (unsigned long long)i0);
        }
        double x = lcg_rand(&estado) / (double)LCG_RAND_MAX;
        double y = lcg_rand(&estado) / (double)LCG_RAND_MAX;
        if (x * x + y * y <= 1.0)
            dentro++;
    }

    double t1 = omp_get_wtime();
    int p_usado = 0;
#pragma omp parallel
    {
#pragma omp master
        p_usado = omp_get_num_threads();
    }
    double I = (double)dentro / (double)N;
    double pi_hat = 4.0 * I;

    printf("N: %ld\n", N);
    printf("hilos: %d\n", p_usado);
    printf("aciertos: %ld\n", dentro);
    printf("Estimacion de la integral: %.10f\n", I);
    printf("Estimacion de pi: %.10f\n", pi_hat);
    printf("Error |pi_hat - pi|: %.6e\n",
           pi_hat > 3.141592653589793 ? pi_hat - 3.141592653589793
                                      : 3.141592653589793 - pi_hat);
    printf("T(%d): %.6f s\n", p_usado, t1 - t0);
    return 0;
}

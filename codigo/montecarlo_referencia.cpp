/* montecarlo_referencia.cpp -- version secuencial de referencia.
   Estima I = integral_0^1 sqrt(1-x^2) dx y pi = 4*I.
   Uso: ./montecarlo_referencia <N>
   Compilar: gcc -O2 -fopenmp montecarlo_referencia.cpp -o montecarlo_referencia -lm */
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include "rng_lcg.h"

#define SEMILLA_BASE 2221886u

int main(int argc, char *argv[]) {
    long N = (argc > 1) ? atol(argv[1]) : 100000000L;
    unsigned int estado = SEMILLA_BASE;
    long dentro = 0;

    double t0 = omp_get_wtime();
    for (long i = 0; i < N; i++) {
        double x = lcg_rand(&estado) / (double)LCG_RAND_MAX;
        double y = lcg_rand(&estado) / (double)LCG_RAND_MAX;
        if (x * x + y * y <= 1.0)
            dentro++;
    }
    double t1 = omp_get_wtime();

    double I = (double)dentro / (double)N;
    double pi_hat = 4.0 * I;
    printf("N: %ld\n", N);
    printf("hilos: 1\n");
    printf("aciertos: %ld\n", dentro);
    printf("Estimacion de la integral: %.10f\n", I);
    printf("Estimacion de pi: %.10f\n", pi_hat);
    printf("Error |pi_hat - pi|: %.6e\n", pi_hat > 3.141592653589793 ? pi_hat - 3.141592653589793 : 3.141592653589793 - pi_hat);
    printf("T(1): %.6f s\n", t1 - t0);
    return 0;
}

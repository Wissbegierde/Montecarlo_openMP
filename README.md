# Parcial 2 — Integración de Monte Carlo con OpenMP

## Estructura del proyecto

```
parcial_2/
├── codigo/
│   ├── rng_lcg.h                    # Generador LCG con función de salto O(log n)
│   ├── montecarlo_referencia.cpp    # Versión secuencial de referencia
│   ├── montecarlo_omp.cpp           # Versión paralela con OpenMP
│   └── graficar_error_montecarlo.py # Script para gráfica de error vs N
│
└── informe/
    ├── informe.tex                  # Informe COMPLETO (todas las partes I, II y III)
    ├── informe_entregable.tex       # Informe ENTREGABLE (solo lo solicitado)
    ├── datos/
    │   ├── tiempos.csv              # Tiempos de ejecución base
    │   └── schedule_comparison.csv  # Comparación static vs dynamic (5 corridas)
    └── figuras/
        ├── error_vs_n.pdf           # Gráfica de error vs N
        ├── speedup_vs_p.pdf         # Gráfica de speedup vs p
        └── graficar_speedup.py      # Script para generar la gráfica de speedup
```

## Dos informes

- **`informe.tex`** — Documento completo con **todas** las respuestas de las tres partes (I, II y III), incluyendo la comparación schedule(static) vs schedule(dynamic) y todos los análisis detallados. Útil como referencia.

- **`informe_entregable.tex`** — Contiene **solo lo requerido** para la entrega:
  - Parte I: preguntas teóricas (I.1, I.2, I.3)
  - Parte III: análisis de desempeño (III.1–III.5) con tabla de speedup y gráfica S(p) vs p
  - Anexo: bitácora de uso de IA

## Compilación

```bash
# Compilar el informe entregable
cd informe
pdflatex informe_entregable.tex
pdflatex informe_entregable.tex   # segunda pasada para referencias

# Generar la gráfica de speedup (requiere matplotlib)
cd figuras
python graficar_speedup.py
```

## Ejecución del código

```bash
cd codigo

# Compilar
gcc -O2 -fopenmp montecarlo_referencia.cpp -o montecarlo_referencia -lm
gcc -O2 -fopenmp montecarlo_omp.cpp -o montecarlo_omp -lm

# Ejecutar secuencial
./montecarlo_referencia 100000000

# Ejecutar paralelo con p hilos
./montecarlo_omp 100000000 4
```

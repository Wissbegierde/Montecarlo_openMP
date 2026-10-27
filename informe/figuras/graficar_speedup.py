"""Genera la grafica S(p) vs p con linea ideal y curva de Amdahl."""
import matplotlib.pyplot as plt
import numpy as np

# Datos medidos
p_vals = np.array([1, 2, 4, 8])
S_med  = np.array([1.000, 1.964, 3.866, 7.313])

# Linea ideal
p_fine = np.linspace(1, 8, 100)
S_ideal = p_fine

# Amdahl con f=0.9884
f = 0.9884
S_amdahl = 1.0 / ((1 - f) + f / p_fine)

fig, ax = plt.subplots(figsize=(6, 4.5))

ax.plot(p_fine, S_ideal,  '--', color='#888888', linewidth=1.2, label='Ideal $S=p$')
ax.plot(p_fine, S_amdahl, '-',  color='#2196F3', linewidth=1.5, label='Amdahl ($f=0.9884$)')
ax.plot(p_vals, S_med,    'o-', color='#E91E63', linewidth=1.8, markersize=7,
        label='Medido', zorder=5)

ax.set_xlabel('Número de hilos $p$')
ax.set_ylabel('Speedup $S(p)$')
ax.set_title('Speedup vs. número de hilos ($N=10^8$)')
ax.set_xticks(p_vals)
ax.set_yticks(range(0, 10))
ax.set_xlim(0.5, 8.5)
ax.set_ylim(0, 9)
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig('speedup_vs_p.pdf', bbox_inches='tight')
fig.savefig('speedup_vs_p.png', dpi=150, bbox_inches='tight')
print("Guardado: speedup_vs_p.pdf y speedup_vs_p.png")

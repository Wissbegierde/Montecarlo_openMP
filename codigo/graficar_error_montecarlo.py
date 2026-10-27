"""Genera datos y figura del error de Monte Carlo ~ 1/sqrt(N).

Uso:
    python graficar_error_montecarlo.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

RAIZ = Path(__file__).resolve().parents[1]
DIR_DATOS = RAIZ / "informe" / "datos"
DIR_FIG = RAIZ / "informe" / "figuras"

I_EXACTA = np.pi / 4.0
P = I_EXACTA
SIGMA1 = np.sqrt(P * (1.0 - P))  # desv. de una Bernoulli

N_VALORES = np.array(
    [1_000, 2_000, 4_000, 8_000, 16_000, 32_000, 64_000, 128_000, 256_000, 512_000, 1_024_000],
    dtype=np.int64,
)
N_REPLICAS = 80
SEMILLA = 2221886


def estimar(n: int, rng: np.random.Generator) -> float:
    x = rng.random(n)
    y = rng.random(n)
    return float(np.mean(x * x + y * y <= 1.0))


def generar_datos() -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(SEMILLA)
    filas = []
    for n in N_VALORES:
        for r in range(N_REPLICAS):
            hat = estimar(int(n), rng)
            filas.append(
                {
                    "N": int(n),
                    "replica": r,
                    "estimador": hat,
                    "error": hat - I_EXACTA,
                    "error_abs": abs(hat - I_EXACTA),
                }
            )
    replicas = pd.DataFrame(filas)
    resumen = (
        replicas.groupby("N", as_index=False)
        .agg(
            rmse=("error", lambda e: float(np.sqrt(np.mean(np.square(e))))),
            error_abs_medio=("error_abs", "mean"),
        )
        .assign(sigma_teorica=lambda d: SIGMA1 / np.sqrt(d["N"]))
    )
    return replicas, resumen


def graficar(replicas: pd.DataFrame, resumen: pd.DataFrame, destino: Path) -> None:
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.15)
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.4))

    ax = axes[0]
    sns.scatterplot(
        data=replicas,
        x="N",
        y="error_abs",
        ax=ax,
        alpha=0.18,
        s=18,
        color="#4c72b0",
        linewidth=0,
        legend=False,
        zorder=1,
    )
    sns.lineplot(
        data=resumen,
        x="N",
        y="rmse",
        ax=ax,
        color="#c44e52",
        marker="o",
        linewidth=2.2,
        label="RMSE empírico",
        zorder=3,
    )
    sns.lineplot(
        data=resumen,
        x="N",
        y="sigma_teorica",
        ax=ax,
        color="#55a868",
        linestyle="--",
        linewidth=2.0,
        label=r"$\sigma = C/\sqrt{N}$",
        zorder=2,
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"Número de muestras $N$")
    ax.set_ylabel(r"Error absoluto $|\hat I_N - I|$")
    ax.set_title(r"El error cae como $1/\sqrt{N}$")
    ax.legend(frameon=True, loc="upper right")

    ax2 = axes[1]
    base = resumen.iloc[0]
    n0, rmse0, sig0 = base["N"], base["rmse"], base["sigma_teorica"]
    costo = pd.DataFrame(
        {
            "N": resumen["N"],
            "factor_N": resumen["N"] / n0,
            "error_relativo_rmse": resumen["rmse"] / rmse0,
            "error_relativo_teor": resumen["sigma_teorica"] / sig0,
            "mitad": 0.5,
            "un_decimo": 0.1,
        }
    )
    sns.lineplot(
        data=costo,
        x="factor_N",
        y="error_relativo_rmse",
        ax=ax2,
        color="#c44e52",
        marker="o",
        linewidth=2.2,
        label="RMSE / RMSE$(N_0)$",
    )
    sns.lineplot(
        data=costo,
        x="factor_N",
        y="error_relativo_teor",
        ax=ax2,
        color="#55a868",
        linestyle="--",
        linewidth=2.0,
        label=r"$1/\sqrt{N/N_0}$",
    )
    ax2.axhline(0.5, color="#8172b3", linestyle=":", linewidth=1.6, label="error a la mitad")
    ax2.axvline(4.0, color="#8172b3", linestyle=":", linewidth=1.6)
    ax2.axhline(0.1, color="#ccb974", linestyle=":", linewidth=1.6, label="un dígito (÷10)")
    ax2.axvline(100.0, color="#ccb974", linestyle=":", linewidth=1.6)
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlabel(r"Factor de costo $N/N_0$  ($N_0=10^3$)")
    ax2.set_ylabel("Error relativo al de $N_0$")
    ax2.set_title("Mitad del error: $\\times 4$ muestras; un dígito: $\\times 100$")
    ax2.legend(frameon=True, loc="lower left", fontsize=8)

    fig.tight_layout()
    destino.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destino, dpi=200, bbox_inches="tight")
    fig.savefig(destino.with_suffix(".png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    DIR_DATOS.mkdir(parents=True, exist_ok=True)
    DIR_FIG.mkdir(parents=True, exist_ok=True)

    replicas, resumen = generar_datos()
    replicas.to_csv(DIR_DATOS / "replicas_error.csv", index=False)
    resumen.to_csv(DIR_DATOS / "resumen_error.csv", index=False)

    graficar(replicas, resumen, DIR_FIG / "error_vs_n.pdf")
    print(resumen.to_string(index=False))
    print(f"\nDatos: {DIR_DATOS}")
    print(f"Figura: {DIR_FIG / 'error_vs_n.pdf'}")


if __name__ == "__main__":
    main()

"""Option (c) test: a script writes committed figure files; the page shows them.

Run from the repo root:  python research/scripts/degree_plot.py
Writes research/img/degree-{transparent,white}.{svg,png} and degree-dark.svg.
"""
import hashlib
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "img"
OUT.mkdir(exist_ok=True)

# Deterministic SVG output: fixed hash salt and no date metadata, so a rerun with
# unchanged code gives a byte-identical file and `git diff` shows only real changes.
plt.rcParams["svg.hashsalt"] = "nets-notes"

# Provenance stamp: each SVG records the script that made it and the script's sha256,
# so research/scripts/check_figures.sh can flag a stale figure in CI without Python.
SRC = Path(__file__).resolve()
META = {
    "Date": None,
    "Source": "research/scripts/" + SRC.name,
    "Identifier": "sha256:" + hashlib.sha256(SRC.read_bytes()).hexdigest(),
}

G = nx.barabasi_albert_graph(5000, 3, seed=42)
k = np.array([d for _, d in G.degree()])
vals, counts = np.unique(k, return_counts=True)
pk = counts / counts.sum()


def plot():
    fig, ax = plt.subplots(figsize=(5, 3.2))
    ax.loglog(vals, pk, "o", ms=3, label=r"BA, $N=5000$, $m=3$")
    kk = np.logspace(np.log10(3), np.log10(vals.max()), 50)
    ax.loglog(kk, 2 * 3**2 * kk**-3.0, "-", label=r"$2m^2 k^{-3}$")
    ax.set_xlabel(r"degree $k$")
    ax.set_ylabel(r"$p_k$")
    ax.legend(frameon=False)
    fig.tight_layout()
    return fig


fig = plot()
for bg in ("transparent", "white"):
    kw = dict(transparent=True) if bg == "transparent" else dict(facecolor="white")
    fig.savefig(OUT / f"degree-{bg}.svg", metadata=META, **kw)
    fig.savefig(OUT / f"degree-{bg}.png", dpi=150, **kw)

# A dark-theme variant, for swapping with `:class: hidden dark:block`.
with plt.style.context("dark_background"):
    plot().savefig(OUT / "degree-dark.svg", metadata=META, transparent=True)

print("wrote", sorted(p.name for p in OUT.glob("degree-*")))

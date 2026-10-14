"""Option (b) test: build and execute research/figure-companion.ipynb locally.

Run from the repo root:  python research/scripts/make_companion.py
The executed notebook (with outputs) is committed; CI renders it without a kernel.
"""
from pathlib import Path

import nbformat
from nbclient import NotebookClient

NB = Path(__file__).resolve().parent.parent / "figure-companion.ipynb"

cells = [
    nbformat.v4.new_markdown_cell(
        "# Figure pipeline test, companion notebook\n\n"
        "Throwaway notebook for issue #77 (option (b)). Executed locally and committed "
        "with outputs; `figure-static.md` embeds its labelled figure."
    ),
    nbformat.v4.new_code_cell(
        "#| label: fig-companion-ws\n"
        "import matplotlib.pyplot as plt\n"
        "import networkx as nx\n"
        "import numpy as np\n"
        "\n"
        "ps = np.logspace(-4, 0, 25)\n"
        "C0 = nx.average_clustering(nx.watts_strogatz_graph(1000, 10, 0, seed=0))\n"
        "L0 = nx.average_shortest_path_length(nx.watts_strogatz_graph(1000, 10, 0, seed=0))\n"
        "C, L = [], []\n"
        "for p in ps:\n"
        "    G = nx.connected_watts_strogatz_graph(1000, 10, p, seed=1)\n"
        "    C.append(nx.average_clustering(G) / C0)\n"
        "    L.append(nx.average_shortest_path_length(G) / L0)\n"
        "fig, ax = plt.subplots(figsize=(5, 3.2))\n"
        "ax.semilogx(ps, C, 'o', label='$C(p)/C(0)$')\n"
        "ax.semilogx(ps, L, 's', label='$L(p)/L(0)$')\n"
        "ax.set_xlabel('rewiring probability $p$')\n"
        "ax.legend(frameon=False)\n"
        "plt.show()",
        metadata={"tags": ["hide-input"]},
    ),
]
nb = nbformat.v4.new_notebook(
    cells=cells,
    metadata={"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}},
)
NotebookClient(nb, timeout=600, kernel_name="python3").execute()
nbformat.write(nb, NB)
print("wrote", NB)

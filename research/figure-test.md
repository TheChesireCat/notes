---
title: Figure pipeline test, executed code cells
short_title: Exec test
description: Throwaway page for issue #77, testing build-time execution of figure code.
kernelspec:
  name: python3
  display_name: Python 3
---

Throwaway test page for issue #77 (option (a), in-page code cells). Built with
`myst build --html --execute`.

## 1. `hide-input` on a matplotlib figure

The cell below has `:tags: [hide-input]` and a `#| label: fig-er-degree` label.

```{code-cell} python
:tags: [hide-input]
#| label: fig-er-degree
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

G = nx.gnp_random_graph(2000, 0.003, seed=1)
k = np.array([d for _, d in G.degree()])
fig, ax = plt.subplots(figsize=(5, 3.2))
ax.hist(k, bins=range(k.max() + 2), density=True, alpha=0.7, label="ER sample")
ax.set_xlabel("degree $k$")
ax.set_ylabel("$p_k$")
ax.legend(frameon=False)
plt.show()
```

## 2. Embedding the labelled cell with `{figure}`

:::{figure} #fig-er-degree
:label: fig-er-embedded
Degree distribution of $G(N=2000, p=0.003)$, embedded from the labelled cell above.
:::

A cross-reference to it: [](#fig-er-embedded).

## 3. A ~30 s simulation

SIR (discrete time, $\mu = 1$) on a Barabási–Albert graph, 2800 runs at each of 15
values of $\beta$. Code folded with `hide-input`.

```{code-cell} python
:tags: [hide-input]
#| label: fig-sir-sweep
import time

t0 = time.time()
rng = np.random.default_rng(0)
H = nx.barabasi_albert_graph(2000, 3, seed=1)
nbrs = [list(H.neighbors(i)) for i in H]


def sir(beta, mu=1.0):
    state = np.zeros(len(nbrs), int)
    s0 = rng.integers(len(nbrs))
    state[s0] = 1
    inf = [s0]
    while inf:
        new = []
        for i in inf:
            for j in nbrs[i]:
                if state[j] == 0 and rng.random() < beta:
                    state[j] = 1
                    new.append(j)
        for i in inf:
            if rng.random() < mu:
                state[i] = 2
            else:
                new.append(i)
        inf = [i for i in set(new) if state[i] == 1]
    return (state == 2).mean()


betas = np.linspace(0.01, 0.3, 15)
R = 2800
r_inf = np.array([[sir(b) for _ in range(R)] for b in betas])
fig, ax = plt.subplots(figsize=(5, 3.2))
ax.plot(betas, r_inf.mean(1), "o-")
ax.set_xlabel(r"$\beta$")
ax.set_ylabel(r"$\langle r_\infty \rangle$")
plt.show()
print(f"simulation wall time: {time.time() - t0:.1f} s")
```

## 2b. Showing the figure once: `remove-output` and `remove-cell` cells, embedded

The cell below is tagged `[hide-input, remove-output]`: its code stays folded here, and its
figure appears only through the `{figure}` embed after it.

```{code-cell} python
:tags: [hide-input, remove-output]
#| label: fig-ba-ccdf
B = nx.barabasi_albert_graph(3000, 2, seed=3)
kb = np.sort([d for _, d in B.degree()])
fig, ax = plt.subplots(figsize=(5, 3.2))
ax.loglog(kb, 1 - np.arange(len(kb)) / len(kb), ".")
ax.set_xlabel("degree $k$")
ax.set_ylabel(r"$P(K \geq k)$")
plt.show()
```

:::{figure} #fig-ba-ccdf
:label: fig-ba-ccdf-embedded
:alt: Log-log complementary CDF of BA degrees.
CCDF of BA degrees, embedded from a `remove-output` cell.
:::

The next cell is tagged `remove-cell`; it is embedded below.

```{code-cell} python
:tags: [remove-cell]
#| label: fig-hidden-cell
fig, ax = plt.subplots(figsize=(4, 2.5))
ax.plot(np.arange(10), np.arange(10) ** 2, "s-")
ax.set_title("from a remove-cell cell")
plt.show()
```

:::{figure} #fig-hidden-cell
:label: fig-hidden-cell-embedded
Embedded from a `remove-cell` cell.
:::

## 4. Dark mode, executed outputs

Default inline PNG (matplotlib's white figure face):

```{code-cell} python
:tags: [remove-input]
fig, ax = plt.subplots(figsize=(4, 2.5))
ax.plot([1, 2, 3], [1, 4, 9], "o-")
ax.set_title("inline PNG, white face")
plt.show()
```

Inline PNG with a transparent figure face:

```{code-cell} python
:tags: [remove-input]
fig, ax = plt.subplots(figsize=(4, 2.5))
fig.patch.set_alpha(0)
ax.patch.set_alpha(0)
ax.plot([1, 2, 3], [1, 4, 9], "o-")
ax.set_title("inline PNG, transparent")
plt.show()
```

Inline SVG (`InlineBackend.figure_formats = ['svg']`), white and transparent:

```{code-cell} python
:tags: [remove-input]
%config InlineBackend.figure_formats = ['svg']
fig, ax = plt.subplots(figsize=(4, 2.5))
ax.plot([1, 2, 3], [1, 4, 9], "o-")
ax.set_title("inline SVG, white face")
plt.show()
fig, ax = plt.subplots(figsize=(4, 2.5))
fig.patch.set_alpha(0)
ax.patch.set_alpha(0)
ax.plot([1, 2, 3], [1, 4, 9], "o-")
ax.set_title("inline SVG, transparent")
plt.show()
```

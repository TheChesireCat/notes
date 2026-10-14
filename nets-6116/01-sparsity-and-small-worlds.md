---
title: Sparsity and Small-Worldness of Network Models
short_title: Sparsity & small worlds
subject: NETS 6116 · Topic
description: The asymptotic definitions of sparse, ultrasparse, small-world and ultrasmall-world graph sequences, why they apply to models and not to single networks, and the typical-distance scalings of ER, configuration-model and preferential-attachment graphs.
tags: [sparsity, small-world, ultrasmall-world, typical-distance, asymptotics, erdos-renyi, configuration-model, preferential-attachment]
---

:::{tip} TL;DR
- **Sparsity and small-worldness belong to sequences of graphs** $G_N$ with $N \to \infty$, that is, to models. They do not belong to any one finite network. A single sample can look empty even when its model is dense: $G(N,p)$ with $N = 10^{10}$ and $p = 10^{-10^{10}}$ is almost surely empty. Real networks are called sparse only by intuition, or from their growth history.
- **Density classes (Krioukov):** *dense* if $\langle k \rangle_N \sim N$ (that is, $L \sim N^2$); *sparse* if $\langle k \rangle_N \ll N$; *ultrasparse*, a subset of sparse, if $\langle k \rangle_N$ stays bounded ($\langle k \rangle_N \to c < \infty$). Mathematicians and physicists use "sparse" and "dense" differently for the in-between regime $1 \ll \langle k \rangle \ll N$.
- **World classes**, defined by the mean distance $\bar d_N$ over pairs at finite positive distance: a *small world* has $\bar d_N \ll N^{\varepsilon}$ for every $\varepsilon > 0$; an *ultrasmall world* has $\bar d_N \ll \log^{\varepsilon} N$ for every $\varepsilon > 0$; anything else is a *large world* (lattices, chains, random trees).
- **Distance scalings to remember:**
  - ER with $\langle k \rangle \to c > 1$: $\bar d_N \approx \ln N / \ln c$.
  - Power-law configuration model (CM) and preferential attachment (PA), by degree exponent $\gamma$:
    - $\gamma > 3$: $\bar d_N \approx \ln N / \ln \nu$, where $\nu = \langle k(k-1)\rangle/\langle k\rangle$ is the mean excess degree;
    - $\gamma = 3$: $\ln N / \ln\ln N$ (PA);
    - $2 < \gamma < 3$: $c\,\ln\ln N / \lvert\ln(\gamma-2)\rvert$, with $c = 2$ for CM and $c = 4$ for PA. **Ultrasmall.**
    - $\gamma < 2$: $\bar d_N \to 2$ or $3$.
- The definitions use only distances between connected pairs, so they ignore connectivity: a perfect matching (disjoint edges) is an "ultrasmall world" even though almost every pair is disconnected.
:::

- **Source.** Krioukov, *Network Science II* lecture notes, ch. 1 (Sparsity) and ch. 2 (Small-worldness). The rigorous distance results come from the probability literature, mainly [](doi:10.1017/9781316795552) (van der Hofstad, *Random Graphs and Complex Networks*, Vol. 2, 2024), plus the primary papers cited at each result. The empirical tables in the notes use the example networks of [](doi:10.1017/9781108653947) (Menczer, Fortunato & Davis, *A First Course in Network Science*, 2020).
- **Builds on.** Degree, distance and density ([Newman ch. 6 notes](../nets-5116/newman/06-mathematics-of-networks.md)); ER graphs and the Watts–Strogatz model ([Barabási ch. 3 notes](../nets-5116/barabasi/03-random-networks.md)).
- **Notation.** Shared symbols as in [](#notation): $N$, $L$, $\langle k\rangle$ for Krioukov's $n$, $m$, $\bar k$, and $d_{\max}$ for his diameter $\mathcal{D}_n$. Page-specific symbols:
  - $\delta_N = L/\binom{N}{2}$ is the **edge density**. Krioukov writes $d$, which here would clash with distance.
  - $\langle d\rangle(G)$ is the mean distance of one graph, and $\bar d_N$ its ensemble average.
  - $\nu = \langle k(k-1)\rangle/\langle k\rangle = \kappa - 1$ is the **mean excess degree**, the branching factor of a configuration model. Krioukov writes $\nu = \langle k^2\rangle/\langle k\rangle$ (see [below](#sec-sparse-results)).

(sec-sparse-setup)=
## Setup and definitions

Every object here is a **graph sequence** $(G_N)_{N \ge 1}$, usually random: one ensemble per size $N$, with $P_N(G)$ the probability of graph $G$. Quantities indexed by $N$ ($\langle k\rangle_N$, $L_N$, $\bar d_N$) are expectations over that ensemble, or values of a single deterministic sequence. Both properties are defined for the **simplest** graphs: simple, undirected and unweighted. A weighted, directed, multilayer or temporal network must first be projected to such a graph, and the answer can depend on how the projection is done.

:::{prf:definition} Asymptotic notation (Krioukov's conventions)
:label: def-sparse-asymptotics

Let $f_N, g_N \ge 0$, and let $c \in (0,\infty)$ be a constant. Then:

| Notation | Meaning | Standard analysis notation |
|---|---|---|
| $f_N \to a$ | $\lim_{N\to\infty} f_N = a$, $a \in [0,\infty]$ | |
| $f_N \ll g_N$ | $f_N / g_N \to 0$ | $f = o(g)$ |
| $f_N \gg g_N$ | $f_N / g_N \to \infty$ | $f = \omega(g)$ |
| $f_N \sim g_N$ | $f_N / g_N \to c$ for **some** $c \in (0,\infty)$ | stronger than $f = \Theta(g)$: the limit must exist |
| $f_N \approx g_N$ | $f_N / g_N \to 1$ | $f \simeq g$, "asymptotic to" |

The examples in the notes are $\log^{100} N \ll N^{0.01}$, $e^{0.01N} \gg N^{100}$, $5N\log N + 7N \sim N \log N$, and $(N^2-2)(3\log N - 5) + 10(N^2-3N) \approx 3N^2\log N$. The informal readings ($0.01 \ll 1$, $1.01 \approx 1$) are also used; the notes put them in quotes when the context leaves it unclear.
:::

Two traps when reading other sources. Barabási and Newman use $\sim$ loosely, to mean "scales as". In analytic number theory, $f \ll g$ means $f = O(g)$, which is the opposite of strict.

:::{prf:definition} Edge density and mean degree
:label: def-sparse-density

For a simple undirected graph with $N$ nodes and $L$ edges,

$$
\delta_N = \frac{L}{\binom{N}{2}}, \qquad \langle k\rangle_N = \frac{2L}{N} = (N-1)\,\delta_N .
$$ (eq-sparse-density)

For a directed graph, $\delta_N = L / [N(N-1)]$ and $\langle k\rangle$ is the mean in-degree (equal to the mean out-degree), $L/N$.
:::

:::{prf:definition} Dense, sparse, ultrasparse
:label: def-sparse-classes

A graph sequence $(G_N)$ is

- **dense** if $\langle k\rangle_N \sim N$, equivalently $\delta_N \sim 1$ or $L_N \sim N^2$;
- **sparse** if $\langle k\rangle_N \ll N$, equivalently $\delta_N \to 0$ or $L_N \ll N^2$;
- **ultrasparse** (a subset of sparse) if $\langle k\rangle_N \to c < \infty$, equivalently $L_N = O(N)$ with a limit.
:::

:::{prf:definition} Distance, mean distance
:label: def-sparse-distance

$d_{ij}(G)$ is the length of a shortest path from $i$ to $j$, with $d_{ii} = 0$ and $d_{ij} = \infty$ if there is no path. The **mean distance** of a graph averages only over pairs at **finite positive** distance:

$$
\langle d\rangle(G) = \frac{\sum_{i,j} d_{ij}(G)\, \mathbb{1}\{d_{ij}(G) \in (0,\infty)\}}{\sum_{i,j} \mathbb{1}\{d_{ij}(G) \in (0,\infty)\}} .
$$ (eq-sparse-mean-distance)

The **typical distance** of a model is its ensemble average,

$$
\bar d_N = \sum_{d=1}^{N-1} d\, P_N(d) = \sum_{G} \langle d\rangle(G)\, P_N(G),
$$ (eq-sparse-typical-distance)

where $P_N(d)$ is the probability that two random nodes at finite positive distance are at distance $d$.
:::

The two expressions in {eq}`eq-sparse-typical-distance` agree exactly only if every graph in the ensemble has the same number of connected pairs. In general the pair-weighted average $\sum_d d\,P_N(d)$ and the graph-weighted average differ by a covariance term. For models with a concentrating giant component the difference vanishes as $N \to \infty$; this is my remark, not the notes'.

:::{prf:definition} Small, ultrasmall and large worlds
:label: def-sparse-worlds

A graph sequence is

- a **small world** if $\bar d_N \ll N^{\varepsilon}$ for every $\varepsilon > 0$, that is, $\bar d_N$ grows slower than any power of $N$;
- an **ultrasmall world** (a subset of small worlds) if $\bar d_N \ll \log^{\varepsilon} N$ for every $\varepsilon > 0$;
- a **large world** otherwise. Typically $\bar d_N \sim N^{\alpha}$ for some $\alpha > 0$.
:::

## Core ideas

### No finite network is sparse or dense

Density and distance classes are statements about limits, so a single network of fixed size $N$ has neither property. The notes give an adversarial example to make the point. Take $G(N,p)$ with **constant** $p$. Its mean degree is $p(N-1) \sim N$, so the model is dense by {prf:ref}`def-sparse-classes`. Now fix $N = 10^{10}$ and $p = 10^{-10^{10}}$:

$$
P(\text{empty graph}) = (1-p)^{\binom{N}{2}} \approx 1 - \binom{N}{2}\,p \approx 1 - \tfrac12\,10^{20 - 10^{10}} \approx 1 .
$$

So a single sample from this dense model is, for any practical purpose, the empty graph. Conversely, a network with $\delta = 0.2$ (the Everglades food web) could come from a sparse model at small $N$.

The notes give three practical consequences:

1. Calling a real network sparse is an **intuition**, or an argument about the model one would use for it. It is not a measurement. The table in the notes shows the densities of twelve real networks clustered near 0, far from uniform random numbers in $[0,1]$. That is suggestive, not a proof.
2. A **history** of the network (snapshots at increasing $N$, as for the Internet) gives real evidence: one can fit how $L$ grows with $N$. It is still not rigorous, because the observed range of $N$ is finite.
3. The same caveat applies to small-worldness. Reporting $\langle d\rangle = 4$ for one network says nothing about $\log N$ against $N^{\varepsilon}$.

Growth histories are where the question becomes empirical. [](doi:10.1145/1081870.1081893) (Leskovec, Kleinberg & Faloutsos, KDD 2005) found **densification**, $L(t) \propto N(t)^{a}$ with $1 < a < 2$, in citation, patent and autonomous-system graphs. In Krioukov's classes such growth is **sparse but not ultrasparse**, since $\langle k \rangle \sim N^{a-1} \to \infty$ while $\langle k \rangle \ll N$.

### Vocabulary differs across fields

| Scaling | $\delta_N$ | $\langle k\rangle_N$ | $L_N$ | Usual name (literature) | This course |
|---|---|---|---|---|---|
| linear in $N$ | $\sim 1$ | $\sim N$ | $\sim N^2$ | dense | dense |
| between | $\ll 1$, $\gg 1/N$ | $1 \ll \langle k\rangle \ll N$ | $N \ll L \ll N^2$ | sparse (maths); "not sparse" or even "dense" (physics) | sparse |
| bounded | $\sim 1/N$ | $\sim 1$ | $\sim N$ | sparse (physics and maths); also "truly sparse" | sparse **and** ultrasparse |
| vanishing | $\ll 1/N$ | $\ll 1$ | $\ll N$ | ultrasparse | ultrasparse |

(The transcription of this table in the lecture notes is ambiguous about which literature label goes with which of the last two rows. The course column and the Venn diagram are unambiguous: ultrasparse means $\langle k\rangle_N \to c < \infty$.)

The trichotomy is **not exhaustive**. A sequence whose $\langle k\rangle_N / N$ oscillates between $0.1$ and $0$ has no limit, so it is neither dense ($\sim$ requires a limit) nor sparse. The same holds for world classes when $\bar d_N$ oscillates. Models met in practice don't do this, but proofs that rely on the classes do need the limits to exist.

### Classifying familiar sequences

| Sequence | $\langle k\rangle_N$ | Density class | $\bar d_N$ | World class |
|---|---|---|---|---|
| Empty graph | $0$ | ultrasparse | undefined (no connected pairs) | — |
| Complete graph $K_N$ | $N-1$ | dense | $1$ | ultrasmall |
| Path (chain) $P_N$ | $2(N-1)/N \to 2$ | ultrasparse | $(N+1)/3$ | large |
| Star $S_N$ | $2(N-1)/N \to 2$ | ultrasparse | $2(N-1)/N \to 2$ | ultrasmall |
| Complete binary tree | $\to 2$ | ultrasparse | $\approx 2\log_2 N$ | small, not ultrasmall |
| Uniform random labelled tree | $\to 2$ | ultrasparse | $\Theta(\sqrt N)$ | large |
| $D$-dimensional lattice | $2D$ | ultrasparse | $\sim N^{1/D}$ | large |
| ER, $\langle k\rangle \to c > 1$ | $c$ | ultrasparse | $\approx \ln N / \ln c$ | small |
| ER, $\langle k\rangle \sim \log N$ | $\to \infty$ | sparse, not ultrasparse | $\approx \ln N/\ln\ln N$ | small |
| ER, $p$ constant | $\sim N$ | dense | $\to 2 - p$ | ultrasmall |
| PA (BA, $m$ edges per node) | $\to 2m$ | ultrasparse | $\ln N/\ln\ln N$ | small |
| CM, $p_k \sim k^{-\gamma}$, $2<\gamma<3$ | bounded | ultrasparse | $\propto \ln\ln N$ | ultrasmall |
| Perfect matching (disjoint edges) | $1$ | ultrasparse | $1$ | ultrasmall (!) |

All trees, and indeed all sequences with $L_N = O(N)$, are ultrasparse, but their world classes span all three. **Sparsity does not imply small-worldness, nor the reverse.** The tree rows are my additions, checked numerically in the [worked example](#sec-sparse-example).

### Why short distances: tree-like expansion

The common mechanism behind every small-world result here is **exponential neighbourhood growth**. In a locally tree-like sparse graph, the number of nodes within distance $\ell$ of a typical node grows like $b^{\ell}$, where $b$ is the branching factor. The ball reaches $N$ nodes when $\ell \approx \ln N / \ln b$, which is logarithmic. Lattices fail because their balls grow only polynomially ($\ell^D$). Ultrasmallness needs a branching factor that itself **grows** along the exploration, which is what happens when hubs are hit with $\langle k^2\rangle = \infty$.

(sec-sparse-results)=
## Key results

:::{prf:theorem} Typical distance in sparse Erdős–Rényi graphs
:label: thm-sparse-er-distance

For $G(N,p)$ with $(N-1)p = \langle k\rangle \to c > 1$, the distance between two uniformly random connected nodes, $H_N$, satisfies

$$
\frac{H_N}{\ln N} \;\xrightarrow{\;\mathbb{P}\;}\; \frac{1}{\ln c},
\qquad\text{so}\qquad
\bar d_N \approx \frac{\ln N}{\ln \langle k\rangle} .
$$ (eq-sparse-er-distance)

Sparse ER is therefore a small world but not an ultrasmall one. Ultrasmallness requires $\ln\langle k\rangle_N \gg \log^{1-\varepsilon} N$ for every $\varepsilon>0$, which holds for instance when $\langle k\rangle_N = N^{a}$ with $a\in(0,1)$: then $\bar d_N \to$ a constant. For constant $p$, $\bar d_N$ stays bounded (and so does the diameter).
:::

The notes state the ultrasmall condition as "$\langle k\rangle \sim N^{\varepsilon}$, $\forall \varepsilon > 0$". Read literally, that condition cannot hold for all $\varepsilon$ at once, so the statement above is my precise form. The notes point to Vol. II of van der Hofstad (Theorem 2.36 or Exercise 6.1) for the proof.

:::{dropdown} Derivation sketch (tree-like approximation)
1. **Local tree-likeness.** In sparse ER, a ball of radius $o(\log N)$ around a node contains no cycles with high probability, because short cycles number $O(1)$ in total.
2. **Branching process.** Exploring outward, each newly reached node has $\mathrm{Bin}(N-1,p) \approx \mathrm{Poisson}(c)$ new neighbours. The number at distance $\ell$ is therefore $Z_\ell \approx c^{\ell}\,W$, where $W$ is the martingale limit of the Galton–Watson process, positive on survival, which is exactly when the node is in the giant component.
3. **Meeting of two balls.** Grow balls of radius $\ell_1$ and $\ell_2$ from $u$ and $v$. Each pair of boundary nodes is joined independently with probability $p = c/N$, so the balls connect once $Z_{\ell_1}Z_{\ell_2}\, c/N \gtrsim 1$, that is, $c^{\ell_1+\ell_2} \approx N$. Hence $d_{uv} \approx \ln N / \ln c$.
4. **Concentration.** The randomness of $W$ shifts $d_{uv}$ only by $O_{\mathbb{P}}(1)$, which is negligible against $\ln N$. That gives convergence in probability of $H_N/\ln N$.

The refined mean-field estimate of [](doi:10.1103/PhysRevE.70.056110) (Fronczak, Fronczak & Hołyst, *PRE* 70, 056110, 2004) keeps the $O(1)$ term: $\bar d_N \approx (\ln N - \gamma_E)/\ln\langle k\rangle + \tfrac12$, where $\gamma_E \approx 0.5772$ is Euler's constant.
:::

:::{prf:theorem} Typical distances in power-law CM and PA
:label: thm-sparse-powerlaw-distance

Let the degrees have a power-law tail $p_k \sim k^{-\gamma}$. The typical distance $H_N$ between connected nodes behaves as follows:

| Regime | Configuration model | Preferential attachment | World class |
|---|---|---|---|
| $\gamma > 3$ (finite variance) | $H_N/\ln N \to 1/\ln\nu$ | $\Theta(\ln N)$ | small |
| $\gamma = 3$ | | $H_N \approx \ln N / \ln\ln N$ (BA, $m\ge2$) | small |
| $2 < \gamma < 3$ (infinite variance) | $H_N \approx \dfrac{2\ln\ln N}{\lvert\ln(\gamma-2)\rvert}$ | $H_N \approx \dfrac{4\ln\ln N}{\lvert\ln(\gamma-2)\rvert}$ | **ultrasmall** |
| $1 < \gamma < 2$ (infinite mean) | $H_N \to 2$ or $3$ | | ultrasmall |

Here $\nu = \langle k(k-1)\rangle/\langle k\rangle > 1$ is the mean excess degree.

Primary sources, by row:
- $\gamma = 3$: the BA diameter, [](doi:10.1007/s00493-004-0002-2) (Bollobás & Riordan, *Combinatorica* 24, 2004).
- $2<\gamma<3$:
  - physics derivation: [](doi:10.1103/PhysRevLett.90.058701) (Cohen & Havlin, *PRL* 90, 058701, 2003);
  - CM proof: [](doi:10.1214/EJP.v12-420) (van der Hofstad, Hooghiemstra & Znamenski, *EJP* 12, 2007);
  - PA: [](doi:10.1007/s10955-010-9921-z) (Dommers, van der Hofstad & Hooghiemstra, *J. Stat. Phys.* 139, 2010).
- $\gamma<2$: [](doi:10.1007/s10687-006-7963-z) (van den Esker, van der Hofstad, Hooghiemstra & Znamenski, *Extremes* 8, 2005).
:::

:::{warning} The branching factor is $\langle k(k-1)\rangle/\langle k\rangle$, not $\langle k^2\rangle/\langle k\rangle$
The lecture notes write $\nu = \langle k^2\rangle/\langle k\rangle$. A node reached along an edge has $k-1$ *further* edges, and the size-biased distribution of $k$ is $kp_k/\langle k\rangle$. The branching factor is therefore $\sum_k (k-1)\,kp_k/\langle k\rangle = \kappa - 1$, which is the $\nu$ of van der Hofstad's theorems and the $z_2/z_1$ of Newman's distance formula. The difference matters: for a 3-regular CM, $\ln N/\ln 2$ is right and $\ln N/\ln 3$ is wrong.
:::

:::{dropdown} Why $\ln\ln N$ when $2<\gamma<3$ (heuristic)
1. **Size-biased tail.** A node reached by following an edge has excess degree with tail $P(K' > k) \sim k^{-(\gamma-2)}$, which has infinite mean when $\gamma < 3$.
2. **Greedy climb.** A node of degree $k$ has $k$ neighbours. The largest of $k$ samples from that tail is of order $k^{1/(\gamma-2)}$. Climbing greedily, the degrees along the path follow $k_{j+1} \approx k_j^{1/(\gamma-2)}$, so $\ln k_j \approx (\gamma-2)^{-j}\ln k_0$: the **log-degree** grows geometrically.
3. **Core.** In a CM, two nodes with $k_i k_j \gtrsim L \sim N$ are adjacent with probability bounded away from zero. Nodes of degree $\gtrsim \sqrt N$ therefore form a dense core of diameter $O(1)$.
4. **Count.** Reaching degree $N^{\Theta(1)}$ needs $(\gamma-2)^{-j} \approx \ln N$, so $j \approx \ln\ln N / \lvert\ln(\gamma-2)\rvert$ steps. Both endpoints must climb, which gives $2\ln\ln N/\lvert\ln(\gamma-2)\rvert$.
5. **PA's factor 4.** In PA the hubs are *old* nodes. A path between two hubs typically passes through a young intermediary, which costs two steps per level of the climb instead of one (Dommers *et al.*).

When $\gamma > 3$, $\nu$ is a finite constant and step 2 has no runaway, so the plain ER-type argument applies with branching factor $\nu$.
:::

:::{prf:proposition} Diameter of ER graphs
:label: prop-sparse-er-diameter

$d_{\max}(G(N,p)) \sim \ln N / \ln(Np)$, with two regimes:

- **Ultrasparse,** $Np \to c > 1$. The ratio $d_{\max} \big/ \frac{\ln N}{\ln c}$ lies in $[1, f(c)]$ with high probability, with $f(c) \ge 1$. The diameter of the giant is strictly longer than the typical distance, because of long thin "hairs" hanging off it. The exact constant is in [](doi:10.1017/S0963548310000325) (Riordan & Wormald, *CPC* 19, 2010).
- **Constant $p$.** The diameter is concentrated on at most two values; in fact $d_{\max} = 2$ with high probability.
:::

:::{important} The definitions ignore connectivity
{eq}`eq-sparse-mean-distance` averages only over pairs at finite distance. A perfect matching has $\langle d\rangle = 1$, so it is an ultrasmall world, even though $\Pr(d_{ij} = \infty) \to 1$ for a random pair. Any statement "model X is a small world" should be read together with the existence and size of a giant component ([Barabási ch. 3 notes](../nets-5116/barabasi/03-random-networks.md)).
:::

(sec-sparse-example)=
## Worked example

**(a) Checking the density table.** The notes tabulate $N$, $L$, density and $\langle k\rangle$ for twelve networks. Recomputing with {eq}`eq-sparse-density` (directed formulas for D-type networks):

| Network | $N$ | $L$ | $\delta$ (computed) | $\delta$ (notes) | $\langle k\rangle$ (computed) |
|---|---|---|---|---|---|
| Facebook Northwestern | 10,567 | 488,337 | $8.7\times10^{-3}$ | 0.009 | 92.4 |
| Enron email (DW) | 87,273 | 321,918 | $4.2\times10^{-5}$ | **0.0004** | 3.7 |
| Internet routers | 190,914 | 607,610 | $3.3\times10^{-5}$ | **0.0003** | 6.4 |
| US air transportation | 546 | 2,781 | $1.9\times10^{-2}$ | 0.02 | 10.2 |
| Everglades food web (DW) | 69 | 916 | $1.9\times10^{-1}$ | 0.2 | 13.3 |

Every $\langle k\rangle$ matches. Two densities in the notes are ten times too large: Enron and Internet routers. The IMDB movies–stars graph is also off by a factor of ten ($5.8\times10^{-6}$ against $6\times10^{-5}$). That graph is bipartite, though, so its density depends on which pairs count as possible. The notes also give $N = 563{,}443$ for IMDB in ch. 1 and $565{,}443$ in ch. 2. None of this changes the qualitative point: every density is $\ll 1$ *for these $N$*.

**(b) ER typical distances.** For $G(N, p)$ with $\langle k\rangle = 4$, the mean distance in the giant component (3 samples, 200 BFS sources each) is:

| $N$ | simulated $\langle d\rangle$ | $\ln N / \ln 4$ | Fronczak *et al.* |
|---|---|---|---|
| $10^3$ | 5.09 | 4.98 | 5.07 |
| $10^4$ | 6.77 | 6.64 | 6.73 |
| $10^5$ | 8.42 | 8.30 | 8.39 |

From $10^3$ to $10^5$ the simulated distance rises by 3.33, against the predicted $2\ln 10/\ln 4 = 3.32$. The leading order {eq}`eq-sparse-er-distance` gets the **slope** right. The $O(1)$ offset is the correction that {prf:ref}`thm-sparse-er-distance` drops, and the Fronczak formula captures most of it.

**(c) Exact distances in a path and a star.** In the path $P_N$ there are $2(N-d)$ ordered pairs at distance $d$. So

$$
\langle d\rangle(P_N) = \frac{\sum_{d=1}^{N-1} 2(N-d)\,d}{N(N-1)} = \frac{N+1}{3},
$$

which gives 3.67, 33.7 and 333.7 at $N = 10, 100, 1000$: a large world. In the star there are $2(N-1)$ ordered hub–leaf pairs at distance 1 and $(N-1)(N-2)$ leaf–leaf pairs at distance 2, so $\langle d\rangle = 2(N-1)/N$, which is 1.8, 1.98 and 1.998. Both graphs are trees with $\langle k\rangle \to 2$, so the same density class contains opposite world classes.

**(d) Trees.** The complete binary tree has $\langle d\rangle = 8.35$, 14.07 and 20.01 at $N = 127$, 1023 and 8191, which is about $2\log_2 N - 6$: logarithmic, so small but not ultrasmall. Uniform random labelled trees at $N = 500$, 2000 and 8000 have $\langle d\rangle \approx 27$, 57 and 128. That is consistent with $\Theta(\sqrt N)$ growth, so they form a large world.

## Assumptions and limitations

- **Untestable on data.** Both properties need $N \to \infty$. Applying them to a real network means positing a model, or extrapolating a growth history. A finite range of $N$ cannot tell $\ln N$ from $N^{0.05}$, or $\ln\ln N$ from a constant.
- **Simplest-graph reduction.** Weighted, directed, temporal or multilayer data must be projected first. Thresholding weights or ignoring direction can move a network between classes. Strongly connected components of directed graphs can be much smaller than the undirected giant.
- **Conditioning on finite distance.** {eq}`eq-sparse-mean-distance` drops disconnected pairs, so world classes say nothing about connectivity (see the perfect matching).
- **Ensemble mean against typical value.** $\bar d_N$ is an average. The theorems are mostly about convergence in probability of the distance between a random pair. These agree when the distribution concentrates, as in all the models above.
- **"Small world" in the Watts–Strogatz sense** also requires high clustering ([](doi:10.1038/30918), *Nature* 393, 1998). Krioukov's definition is distance-only; clustering is treated separately in [Clustering and assortativity](./02-clustering-and-assortativity.md). Sparse ER is a small world here, but not in the Watts–Strogatz sense.
- **Exponents are asymptotic, and convergence in $\gamma$ is slow.** For $2<\gamma<3$ the $\ln\ln N$ regime needs very large $N$ to separate from $\ln N$. Finite-size cutoffs $k_{\max}(N)$ also change the effective $\nu$. Inferring $\gamma$ itself is the subject of [Data binning and power laws](./03-binning-and-power-laws.md).

## Connections

- **NETS 5116.** Barabási's "distance regimes" (ultra-small for $2<\gamma<3$, $\ln\ln N$; small for $\gamma > 3$) are the physics version of {prf:ref}`thm-sparse-powerlaw-distance`; see the [scale-free chapter notes](../nets-5116/barabasi/04-scale-free-networks.md). The BA $\ln N/\ln\ln N$ appears in the [BA-model notes](../nets-5116/barabasi/05-barabasi-albert-model.md). Barabási's claim that real networks are sparse because $L \ll L_{\max}$ is exactly the finite-$N$ intuition that Krioukov warns about. Newman's empirical distance and density tables are in the [ch. 10 notes](../nets-5116/newman/10-structure-of-real-world-networks.md).
- **NETS 6116.** Sparsity decides which limit object is meaningful. Dense sequences converge to non-trivial **graphons**, while sparse sequences converge to the zero graphon ([Hidden variables and graphons](./07-hidden-variables-and-graphons.md)). The configuration model whose distances appear above is built in [Configuration models](./05-configuration-models.md). The ultrasparse regime with bounded $\langle k\rangle$ is where **latent-space models** combine sparsity, small worlds and clustering ([Latent-space models](./08-latent-space-models.md)).
- **PHYS 7335.** The same branching factor $\kappa - 1$ that sets CM distances sets the SIR / bond-percolation threshold $T_c = \langle k\rangle/(\langle k^2\rangle - \langle k\rangle)$ ([SIR as percolation](../phys-7335/07-sir-percolation.md)). A diverging $\langle k^2\rangle$ makes networks ultrasmall *and* removes the epidemic threshold ([heterogeneous mean-field](../phys-7335/05-heterogeneous-mean-field.md)).
- **NETS 7332.** Small-worldness is why an $\ell$-layer GNN's receptive field covers most of the graph after a few layers. Exponential neighbourhood growth drives both oversmoothing and the need for neighbour sampling ([message passing](../nets-7332/basics/05-message-passing-gnns.md), [scaling](../nets-7332/basics/08-scaling-and-generative.md)).

## Self-test

:::{dropdown} Q1. Why can no single finite network be called sparse? What evidence would make the claim reasonable?
The definitions are asymptotic. They concern $\langle k\rangle_N$ as $N \to \infty$ in a sequence or model. A sample from a dense model ($G(N,p)$ with constant but tiny $p$) can be empty, and a sample from a sparse model can have density 0.2 at small $N$. Reasonable evidence is a growth history showing how $L$ scales with $N$, or a mechanistic model whose $\langle k\rangle_N$ is known.
:::

:::{dropdown} Q2. Give the density and world class of: the star, the path, $G(N, 3/N)$, $G(N, 1/2)$, and a perfect matching.
- Star: ultrasparse, ultrasmall ($\langle d\rangle\to 2$).
- Path: ultrasparse, large ($(N+1)/3$).
- $G(N,3/N)$: ultrasparse, small but not ultrasmall ($\ln N/\ln 3$).
- $G(N,1/2)$: dense, ultrasmall ($\bar d \to 1.5$, diameter 2).
- Perfect matching: ultrasparse, ultrasmall but disconnected.
:::

:::{dropdown} Q3. What is the difference between $f \sim g$ and $f \approx g$ in Krioukov's notation? Is $5N\log N + 7N \approx N\log N$?
$f\sim g$ means $f/g \to c \in (0,\infty)$; $f \approx g$ means $f/g \to 1$. $5N\log N + 7N \sim N\log N$ ($c = 5$), but it is not $\approx N\log N$; it is $\approx 5N\log N$.
:::

:::{dropdown} Q4. Derive $\bar d_N \approx \ln N/\ln c$ for sparse ER. What is the right branching factor for a configuration model?
Neighbourhoods are locally tree-like with Poisson($c$) offspring, so about $c^{\ell}$ nodes lie at distance $\ell$. Two balls of sizes $c^{\ell_1}$ and $c^{\ell_2}$ connect when $c^{\ell_1+\ell_2}c/N \approx 1$, so $d \approx \ln N/\ln c$. In a CM, a node reached along an edge has excess degree drawn from $q_k$, so the branching factor is $\nu = \langle k(k-1)\rangle/\langle k\rangle = \kappa - 1$. For Poisson degrees this equals $c$.
:::

:::{dropdown} Q5. Why are power-law CMs with $2<\gamma<3$ ultrasmall? Where do the constants 2 (CM) and 4 (PA) come from?
The size-biased degree tail has infinite mean, so a greedy climb raises the log-degree geometrically, $\ln k_{j+1} \approx \ln k_j/(\gamma-2)$. Reaching the hub core of degree $N^{\Theta(1)}$ takes $\ln\ln N/\lvert\ln(\gamma-2)\rvert$ steps, and both endpoints must climb, which gives the 2. In PA, hubs are old nodes linked through young intermediaries, so each level costs two steps, which gives the 4.
:::

:::{dropdown} Q6. A growing network densifies as $L \propto N^{1.2}$. Classify it.
$\langle k\rangle \propto N^{0.2} \to \infty$ but $\ll N$, so it is sparse and not ultrasparse. A physicist might call it "not sparse".
:::

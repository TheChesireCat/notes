---
title: The dk-Series of Network Properties and Random Graphs
short_title: dk-series
subject: NETS 6116 · Topic
description: The hierarchy of degree-correlation statistics (0k, 1k, 2k, 2.1k, 2.5k, 3k, …) and their maximum-entropy random graphs, why it is monotonic and convergent, how to sample it with dk-swaps, and how it measures how "random" a network property is.
tags: [dk-series, null-models, degree-correlations, joint-degree-distribution, clustering, rewiring, maximum-entropy, microcanonical]
---

:::{tip} TL;DR
- The **$dk$-distribution** of a graph $G_0$ counts its connected $d$-node subgraphs, each labelled by the degrees of its nodes. **0k** is $(N, L)$. **1k** is the degree distribution $p_k$. **2k** is the joint degree distribution $P(k,k')$ of edge endpoints. **3k** is the degree-labelled triangles $P_\Delta$ and open wedges $P_\wedge$. The **$dk$-random graphs** $M_d$ are the *microcanonical* maximum-entropy graphs with $G_0$'s $dk$-sequence: 0k is $G(N,L)$, 1k is $\mathrm{CM}(N,\mathbf{k})$, and 2k is the uniform graph with a given joint degree matrix.
- The series is **monotonic**: the $dk$-statistics determine all lower ones, so the graph sets are nested, $\mathcal{G}_d \subseteq \mathcal{G}_{d-1}$, and the entropy $H_d = \ln \lvert \mathcal{G}_d \rvert$ falls with $d$. It is also **convergent**: at $d=N$ the only graph left is $G_0$. So for any property $g$ the smallest $d_g$ at which $M_{d_g}$ reproduces $g$ exists. That $d_g$ is a **measure of how random $g$ is**: $g$ follows from the $d_g k$-statistics plus maximal randomness.
- Two key identities: $p_k = \dfrac{\langle k\rangle}{k}\sum_{k'}P(k,k')$ (2k fixes 1k), and the clustering spectrum $\bar C(k)$ is a function of $P_\Delta$ (3k fixes clustering). The **assortativity coefficient $r$ is a 2k-property**. Mean clustering $\langle C \rangle$ and $\bar C(k)$ are **not** fixed by 2k, which is why the intermediate levels **2.1k** (2k plus $\langle C \rangle$) and **2.5k** (2k plus $\bar C(k)$) exist.
- **Sampling.** Use $dk$-preserving double-edge swaps. A 1k-swap keeps all degrees. A 2k-swap also requires the two swapped endpoints to have equal degree. The 2k-swap chain is **ergodic** (all realisations are connected). 3k-swaps are almost never available. Levels 2.1k and 2.5k are reached by **Metropolis annealing** over 2k-swaps, with acceptance $\min(1, e^{-\beta\Delta\Phi})$ on a clustering-mismatch energy $\Phi$.
- **Empirical message** (Orsini et al. 2015): most real networks' local *and* global properties (distances, betweenness, spectra, …) are already reproduced by their 2.5k-, often even 2.1k-random graphs. Much apparent "structure" is therefore a consequence of degrees, degree correlations and clustering plus randomness.
:::

- **Source.**
  - Krioukov, *Network Science II* lecture notes, ch. 10 (the $dk$-series), with ch. 8 (unbiased/maximum-entropy models) and ch. 9 (configuration model) as background.
  - [Mahadevan, Krioukov, Fall & Vahdat (SIGCOMM 2006)](doi:10.1145/1159913.1159930); preprint [arXiv:cs/0605007](doi:10.48550/arXiv.cs/0605007). This paper introduced the $dk$-series, for Internet topologies.
  - [Orsini et al. (*Nat. Commun.* 6, 8627, 2015)](doi:10.1038/ncomms9627): the 2.1k/2.5k levels, and the systematic test on real networks.
  - [Harremoës (*IEEE Trans. Inf. Theory* 47, 2039, 2001)](doi:10.1109/18.930936) for the maximum-entropy property of the binomial.
  - [Czabarka, Dutle, Erdős & Miklós (*Discrete Appl. Math.* 2015)](doi:10.1016/j.dam.2014.10.012) for 2k-swap connectivity.
- **Builds on.**
  - [Typicality and maximum-entropy models](./04-typicality-and-max-entropy.md) (microcanonical ensembles and entropy).
  - [Configuration models](./05-configuration-models.md) (the 1k level).
  - [Clustering and assortativity](./02-clustering-and-assortativity.md) (the statistics that 2k and 3k encode).
- **Notation.** Shared symbols as in [](#notation): $N, L, \langle k\rangle, p_k$ correspond to Krioukov's $n, m, \bar k, P(k)$.
  - Page-specific symbols: $P(k,k')$ (joint degree distribution); $P_\Delta, P_\wedge$ (3k distributions); $t$ (number of triangles); $w$ (number of **open** wedges); $\bar C(k)$ (mean clustering of degree-$k$ nodes; Krioukov: $\bar c(k)$); $\mathcal{G}_d(G_0)$ (the set of $dk$-graphs); $H_d$ (its entropy).
  - $\Phi$ is the annealing energy (Krioukov: $H$, renamed here so it doesn't clash with entropy).
  - $\beta$ is a Metropolis inverse temperature, *not* a transmission rate.

(sec-dk-setup)=
## Setup and definitions

The problem the notes start from is a modelling loop. Someone finds that property $f_s$ is ubiquitous, the current best model $M_{s-1}$ doesn't reproduce it, so a new model $M_s$ is built that does, and the loop repeats. The notes give the history of early network science as such a loop: ER → small worlds → scale-free → … Building a model for $f_s$ also often reproduces some *other* property $g$ "for free", because $g$ is a consequence of $f_s$ plus randomness. Examples from the notes:

- ER reproduces the binomial $p_k$, because the binomial is the maximum-entropy degree distribution ({prf:ref}`thm-dk-binomial`).
- ER graphs are small worlds: a minimal amount of randomness already gives $\langle d\rangle \sim \ln N$ ([sparsity and small worlds](./01-sparsity-and-small-worlds.md)).
- Dense ER graphs are ultra-small and strongly clustered, both consequences of density.
- Scale-free configuration-model graphs are ultra-small worlds, a consequence of the degree distribution plus randomness.
- In many networks the rich-club effect is a consequence of degree correlations ([Colizza et al. 2006](doi:10.1038/nphys209)).

The $dk$-series replaces this ad hoc loop with **one systematic hierarchy** of properties $f_d$ and models $M_d$, $d = 0, 1, 2, \dots$, which must satisfy two requirements.

1. **Monotonicity.** $f_d$ determines $f_{d'}$ for every $d' < d$. So the larger $d$ is, (a) the more structure $M_d$ reproduces, and (b) the smaller its graph set.
2. **Convergence.** For every finite $G_0$ there is a finite $D_{G_0}$ such that $M_{D_{G_0}}$ contains only $G_0$ (up to isomorphism).

:::{prf:definition} $dk$-distribution and $dk$-sequence
:label: def-dk-distribution

The **$dk$-distribution** of a graph $G_0$ is the empirical distribution of its connected $d$-node subgraphs, each labelled by the (full-graph) degrees of its nodes, for $d = 0, 1, \dots, N$. The **$dk$-sequence** is the same thing as raw counts. The first levels:

| $d$ | subgraphs | distribution | sequence (counts) |
|---|---|---|---|
| 0k | none | $\langle k\rangle$ | $N, L$ |
| 1k | single nodes | $p_k$ | $N_k$ |
| 2k | edges | $P(k,k')$ | $n(k,k')$: edges between degree-$k$ and degree-$k'$ nodes (the *joint degree matrix*) |
| 3k | triangles, open wedges | $P_\Delta(k,k',k'')$, $P_\wedge(k,k',k'')$ | $n_\Delta$, $n_\wedge$ |
| 4k | the six connected 4-node graphs | $\{P_i(k_1,\dots,k_4)\}_{i=1}^{6}$ | … |

The convention used throughout this page counts **ordered** objects, which makes every identity below exact:

- $P(k,k')$ is the fraction of the $2L$ *directed* edge ends $(u\to v)$ with $k_u=k$, $k_v=k'$. It is symmetric, $P(k,k') = P(k',k)$.
- $P_\Delta(k,k',k'')$ and $P_\wedge(k,k',k'')$ are fractions of ordered 2-paths $x - y - z$ (with $x\neq z$) whose end-nodes are, respectively, adjacent ($6t$ such paths) or not ($2w$ paths). The **middle argument is the centre** $y$.
:::

:::{prf:definition} $dk$-graphs, $dk$-random graphs, $dk$-series
:label: def-dk-random

- The **$dk$-graphs** of $G_0$, $\mathcal{G}_d(G_0)$, are all graphs with the same $dk$-sequence as $G_0$.
- The **$dk$-random graphs** $M_d$ are the *microcanonical* maximum-entropy ensemble on that set: the uniform distribution $P(G) = 1/\lvert\mathcal{G}_d\rvert$, with entropy $H_d = \ln\lvert\mathcal{G}_d\rvert$.
- The **$dk$-series** of $G_0$ is the pair of sequences $(f_d)$ of $dk$-statistics and $(M_d)$ of $dk$-random graphs.

| $d$ | $dk$-random graphs |
|---|---|
| 0k | $G(N,L)$ (Erdős–Rényi, microcanonical) |
| 1k | $\mathrm{CM}(N,\mathbf{k})$ |
| 2k | uniform graphs with the given joint degree matrix $n(k,k')$ |
| 2.1k | 2k plus a given mean clustering $\langle C\rangle$ |
| 2.5k | 2k plus a given clustering spectrum $\bar C(k)$ |
:::

All models in the chapter are **microcanonical**: they fix the statistic exactly. The soft (canonical) analogues are on the [configuration-model](./05-configuration-models.md) and [maximum-entropy](./04-typicality-and-max-entropy.md) pages.

Two scope remarks (my own reading, not from the notes):

- In practice the swaps below preserve **each node's own degree**, not just the counts $N_k$. That is why $M_1$ is $\mathrm{CM}(N,\mathbf{k})$, with a labelled degree sequence, rather than "all graphs with $N_k$ nodes of degree $k$". The two differ only by relabelling nodes of equal degree, so isomorphism classes and entropy differences are unaffected.
- **Isolated nodes and isolated edges** are invisible to the 2k- and 3k-distributions respectively. Monotonicity therefore uses the *sequences*, which carry $N$ and $L$.

(sec-dk-core)=
## Core ideas

### Why ER is the "correct null model of $\langle k\rangle$"

The notes make a point about language. "ER reproduces / models well / is a good null model of" the average degree in exactly the sense that CM is all of those things for the degree sequence. Graphs with a given $\mathbf{k}$ form a subset of the graphs with $L = \frac12\sum_i k_i$: $\mathrm{CM}(N,\mathbf{k}^1)$ and $\mathrm{CM}(N,\mathbf{k}^2)$ are disjoint subsets of $\mathcal{G}(N,L)$ whenever $\sum k^1_i = \sum k^2_i = 2L$. ER is not a *bad* model of $p_k$. It predicts one specific value, the maximally random (binomial) one. The general lesson: **every model predicts some value or distribution for every property**, and the only question is whether that prediction matches.

:::{prf:theorem} Binomial is maximum-entropy (Harremoës 2001)
:label: thm-dk-binomial

Among all distributions of sums of $N-1$ independent Bernoulli variables (with possibly different success probabilities) whose mean is $\langle k\rangle = (N-1)p$, the binomial $\mathrm{Bin}(N-1,p)$ has maximal Shannon entropy.
:::

In the $G(N,p)$ ensemble a node's degree is exactly such a sum, so ER's binomial $p_k$ is "what you get from $\langle k\rangle$ plus maximal randomness".

### The dk hierarchy

Each level of the hierarchy is the degree-labelled census of connected $d$-node subgraphs:

- **2k** is the full description of **two-point degree correlations**. The conditional distribution used throughout the degree-based mean-field literature follows directly: $P(k'\mid k) = P(k,k')/\sum_{k''}P(k,k'') = \langle k\rangle P(k,k')/(k\,p_k)$. The assortativity coefficient $r$ is the Pearson correlation of $P(k,k')$ (the notes' remark), so **$r$ is a 2k-property**.
- **3k** is the degree-labelled triangle and wedge census. It fixes all clustering statistics ({prf:ref}`prop-dk-clustering`).
- For $d>2$ the $dk$-statistics are degree correlations *within* $d$-node subgraphs, which is the reason for the name.

The **$d$-series**, which ignores the degree labels, is a natural alternative. Its sequences are $N$ for $d=1$, $L$ for $d=2$, and $(t,w)$ for $d=3$. It is a poor substitute, for two reasons:

- It is **not monotonic**. $N$ and $L$ are independent apart from $L \le \binom{N}{2}$, and $(t, w)$ does not determine $L$.
- It **converges slowly**, because it throws away the degree labels that make the $dk$-statistics so restrictive. [The worked example](#sec-dk-example) quantifies this on all connected 7-node graphs.

### Explaining a property

Because the series is monotonic and convergent, every property $g$ has a well-defined minimal level

$$
d_g = \min\{d : M_d \text{ reproduces } g\}.
$$ (eq-dk-dg)

- Convergence guarantees that $d_g \le D_{G_0}$ exists.
- Monotonicity guarantees that every $M_{d}$ with $d \ge d_g$ also reproduces $g$.

So $g$ is "explained" as a consequence of $f_{d_g}$ plus randomness. A small $d_g$ means $g$ is **not an independent feature** of the network. The notes call the series "a method to measure the randomness of any network property". "Reproduces" is a statistical judgement: $G_0$'s value of $g$ is typical in $M_d$, as on the [typicality](./04-typicality-and-max-entropy.md) page.

(sec-dk-generation)=
### Generation: $dk$-swaps

The main method is to start from $G_0$ itself, which trivially has the right $dk$-sequence, and randomise it with moves that preserve that sequence. A **double-edge swap** picks two edges $(a,b)$ and $(c,d)$ with four distinct endpoints and replaces them with $(a,d)$ and $(c,b)$. It is rejected if either new edge already exists.

| Swap | Extra condition | Preserves | Notes |
|---|---|---|---|
| 0k | none: move any edge anywhere | $N, L$ | Equivalent to sampling $G(N,L)$ directly |
| 1k | none | every $k_i$ | The degree-preserving rewiring of [Maslov & Sneppen (2002)](doi:10.1126/science.1065103) |
| 2k | $k_b = k_d$ | every $k_i$ and $n(k,k')$ | Node $a$ trades a degree-$k_b$ neighbour for a degree-$k_d = k_b$ neighbour, and so does $c$ |
| 3k | must also preserve all degree-labelled triangles and wedges | 3k-sequence | Almost never available |

:::{prf:theorem} 2k-swaps are ergodic
:label: thm-dk-2k-ergodic

For any realisable joint degree matrix, the set of simple graphs realising it, with each node's degree also fixed, is connected under 2k-swaps.
:::

- The notes state this together with $O(L)$ mixing time, attributed to work by Erdős, Toroczkai, Bassler and Coolen.
- Connectivity is proved in [Czabarka et al. (2015)](doi:10.1016/j.dam.2014.10.012).
- I could not find a general *proof* of $O(L)$ mixing in that literature:
  - [Stanton & Pinar (2012)](doi:10.1145/2133803.2330086) report empirically fast mixing.
  - [Bassler et al. (2015)](doi:10.1088/1367-2630/17/8/083052) avoid the mixing question altogether with an exact importance-sampling construction.

  Treat "$O(L)$" as the practical rate, not as a theorem (my own caveat).
- The notes say 3k-swapping is probably not even ergodic, and that in practice valid 3k-swaps almost never exist, which makes 3k a very tight constraint.

**2.1k and 2.5k.** These levels add a clustering target to 2k. Starting from a 2k-randomised graph, propose 2k-swaps and accept each with the Metropolis rule

$$
P_{\mathrm{acc}} = \min\!\left(1, e^{-\beta\,\Delta\Phi}\right), \qquad \Delta\Phi = \Phi_{\text{after}} - \Phi_{\text{before}},
$$ (eq-dk-metropolis)
with the energies

$$
\Phi_{2.1k}(G) = \bigl\lvert \langle C\rangle_G - \langle C\rangle_{G_0} \bigr\rvert, \qquad
\Phi_{2.5k}(G) = \sum_{i=1}^{N} \bigl\lvert \bar C_G(k_i) - \bar C_{G_0}(k_i) \bigr\rvert .
$$ (eq-dk-energy)

The 2.5k energy sums over *nodes*, so each degree class is weighted by $N_k$. As $\beta\to\infty$ (annealing), the chain is driven to graphs with the target clustering. Continuing with $\Phi$-preserving moves then explores the maximally random graphs with that 2k-sequence and clustering. In the notes' words, the 2.1k- (2.5k-) random graphs are the maximally random graphs with a given joint degree distribution and $\langle C\rangle$ ($\bar C(k)$).

These are **intermediate levels** for a practical reason. Clustering is part of the 3k-statistics, but fixing all of 3k is far too restrictive and 3k-swaps are rarely possible. So 2.1k and 2.5k keep the most important 3k summary and leave the rest random.

(sec-dk-results)=
## Key results

:::{prf:proposition} Monotonicity identities (higher $dk$ fixes lower $dk$)
:label: prop-dk-monotone

With the ordered conventions of {prf:ref}`def-dk-distribution`:

**1k → 0k:** $\langle k\rangle = \sum_k k\,p_k$, and $L = N\langle k\rangle/2$.

**2k → 1k:** for $k \ge 1$,

$$
p_k = \frac{\langle k\rangle}{k}\sum_{k'} P(k,k'), \qquad \frac{1}{\langle k\rangle} = \sum_{k,k'} \frac{P(k,k')}{k}.
$$ (eq-dk-2to1)

**3k → 2k:** for $k + k' > 2$,

$$
P(k,k') = \frac{1}{k+k'-2}\sum_{k''}\Big[\frac{3t}{L}\big(P_\Delta(k',k,k'') + P_\Delta(k,k',k'')\big) + \frac{w}{L}\big(P_\wedge(k',k,k'') + P_\wedge(k,k',k'')\big)\Big].
$$ (eq-dk-3to2)
:::

:::{dropdown} Derivation
**2k → 1k.** Count directed edge ends leaving degree-$k$ nodes in two ways. Each of the $N_k$ such nodes has $k$ of them, so $\sum_{k'} n_{\to}(k,k') = k N_k$, where $n_\to(k,k') = 2L\,P(k,k')$. Dividing by $2L = N\langle k\rangle$ gives $\sum_{k'}P(k,k') = k p_k/\langle k\rangle$, which is the first identity. Summing $p_k$ over $k$ to 1 gives the second: $\langle k\rangle$ is the **harmonic mean of the degree at the end of a random edge end**. So 2k fixes $\langle k\rangle$ as well, but not $p_0$: isolated nodes are invisible.

The notes print $p_k = (k/\bar k)\sum_{k'}P(k,k')$, which has the ratio upside down. The version here is dimensionally forced (a random edge end reaches degree-$k$ nodes in proportion to $k\,p_k$), and I checked it numerically.

**3k → 2k.** Take a directed edge $a\to b$ with $k_a = k$, $k_b = k'$. Paths of length 2 containing it are of two kinds:

- $c - a - b$ (centre $a$), with $c$ any of the $k-1$ other neighbours of $a$;
- $a - b - c$ (centre $b$), with $c$ any of the $k'-1$ other neighbours of $b$.

So each such edge lies in exactly $k + k' - 2$ ordered 2-paths. Summing over the $2L\,P(k,k')$ directed edges of that type gives the count of ordered 2-paths with $(k_y,k_z) = (k,k')$ or $(k_x,k_y) = (k,k')$:

$$
(k+k'-2)\,2L\,P(k,k') = \sum_{k''}\big[T(k',k,k'') + T(k,k',k'')\big],
$$
where $T(x,y,z)$ counts ordered 2-paths by degree and is symmetric under reversal, $T(x,y,z) = T(z,y,x)$. Split $T$ into closed ($6t\,P_\Delta$) and open ($2w\,P_\wedge$) parts and divide by $2L$.

The excluded case $k = k' = 1$ is an isolated edge, which lies in no 2-path. Its count is recovered as $L$ minus all other edges.

**Discrepancy.** The transcribed notes give the prefactor of both the triangle term and the wedge term as $w/m$, but they list $t$ among the quantities used. The triangle prefactor must carry the triangle count: it is $3t/L$ in this normalisation. The exact constants depend on how $P_\Delta$ and $P_\wedge$ are normalised; with the ordered convention above, {eq}`eq-dk-3to2` holds to machine precision on Zachary's karate club ($t = 45$, $w = 393$, $L = 78$).
:::

:::{prf:proposition} 3k fixes clustering
:label: prop-dk-clustering

The mean clustering of degree-$k$ nodes is

$$
\bar C(k) = \frac{3t}{N}\,\frac{\sum_{k',k''}P_\Delta(k,k',k'')}{\binom{k}{2}\,p_k},
$$ (eq-dk-ck)
where the first argument of $P_\Delta$ is the node whose clustering is measured (the ordered triangle census is symmetric, so any position works). Therefore $\langle C\rangle = \sum_k p_k \bar C(k)$ and the transitivity $3t/(3t+w)$ are 3k-properties.
:::

:::{dropdown} Derivation
$\bar C(k) = \frac{1}{N_k}\sum_{i:\,k_i=k} t_i / \binom{k}{2}$, where $t_i$ is the number of triangles at $i$. Each triangle has 6 orderings, and in exactly 2 of them a given corner sits in the first slot. So $\sum_{i:\,k_i=k} t_i = \frac{1}{2}\,6t\sum_{k',k''}P_\Delta(k,k',k'') = 3t\sum_{k',k''}P_\Delta(k,k',k'')$. Substituting $N_k = N p_k$ gives {eq}`eq-dk-ck`, which matches the notes' (10.1).
:::

:::{prf:proposition} Nested graph sets and decreasing entropy
:label: prop-dk-entropy

Monotonicity gives $\mathcal{G}_{d}(G_0) \subseteq \mathcal{G}_{d-1}(G_0)$, hence

$$
H_d = \ln\lvert\mathcal{G}_d\rvert \;\le\; H_{d-1}, \qquad H_0 = \ln\binom{\binom{N}{2}}{L} \;\ge\; H_1 \;\ge\; H_2 \;\ge\; \cdots \;\ge\; H_{D_{G_0}} = \ln\frac{N!}{\lvert\mathrm{Aut}(G_0)\rvert}.
$$ (eq-dk-entropy)
(The last value assumes labelled nodes. If node degrees are also pinned, as with swaps, it becomes the number of degree-preserving relabellings of $G_0$; see the worked example.) **The higher $d$ is, the less random $M_d$ is.**
:::

:::{dropdown} Why the inclusion holds
Suppose $G$ has the same $dk$-sequence as $G_0$. By {prf:ref}`prop-dk-monotone`, the $(d-1)k$-sequence is a function of the $dk$-sequence (together with $N$ and $L$). So $G$ also has the same $(d-1)k$-sequence: $G \in \mathcal{G}_{d-1}$. The uniform distribution on a smaller set has smaller entropy.

Convergence is immediate at $d = N$: the $Nk$-statistic is the degree-labelled graph itself. In practice $D_{G_0}$ is usually tiny (see below).
:::

:::{prf:proposition} Uniform sampling by swaps
:label: prop-dk-uniform

Consider the swap chain that proposes a uniformly random ordered pair of edges and stays put when the swap is invalid. Its proposal is symmetric: if $G\to G'$ is possible, $G'\to G$ is the reverse swap and has the same proposal probability. So the uniform distribution on any swap-connected class is stationary. By {prf:ref}`thm-dk-2k-ergodic` the 2k-swap chain therefore samples $M_2$ uniformly in the long run. Self-loops from rejected proposals make it aperiodic.
:::

Picking uniformly among the *valid* swaps would break this symmetry and bias the sample ([Coolen, De Martino & Annibale 2009](doi:10.1007/s10955-009-9821-2)).

**Empirical result** ([Orsini et al. 2015](doi:10.1038/ncomms9627)). The paper computed $dk$-random graphs at $d = 0, 1, 2, 2.1, 2.5$ for a range of real networks, including the Internet AS topology, the PGP web of trust and the US power grid. It compared a broad set of local and global properties, such as distance distributions, betweenness and spectral properties. In most cases the agreement is already very good at 2.5k, and often at 2.1k. The power grid is the clearest exception, with large-scale geometric structure that degree correlations plus clustering do not capture. Their conclusion: most structure in these networks is "explained" by degree correlations and clustering plus randomness, and statistics beyond 2.5k are rarely needed.

(sec-dk-example)=
## Worked example

All numbers were computed with `networkx` (scripts used seeds 6116 and 1).

### Statistics of a small graph

$G_0$ has $N = 7$ nodes and $L = 8$ edges: two triangles $\{0,1,2\}$ and $\{3,4,5\}$, a bridge $2-3$, and a pendant node $6$ attached to $5$.

| Level | $G_0$'s statistics |
|---|---|
| 0k | $N = 7$, $L = 8$, $\langle k\rangle = 16/7 \approx 2.286$ |
| 1k | $N_1 = 1$, $N_2 = 3$, $N_3 = 3$ |
| 2k | $n(1,3) = 1$, $n(2,2) = 1$, $n(2,3) = 4$, $n(3,3) = 2$ (so $r = -1/3$) |
| 3k | triangles by degree: $(2,2,3)$ once, $(2,3,3)$ once ($t = 2$); open wedges (end, **centre**, end): $(1,\mathbf 3,2)$, $(1,\mathbf 3,3)$, $(2,\mathbf 3,3)\times 3$, $(3,\mathbf 3,3)$ ($w = 6$) |
| clustering | $\bar C(2) = 1$, $\bar C(3) = 1/3$; $\langle C\rangle = 4/7 \approx 0.571$; transitivity $= 6/12 = 0.5$ |

Checks:

- **Harmonic mean.** $1/\sum_{k,k'}P(k,k')/k = 16/7$ recovers $\langle k\rangle$ from 2k alone ({eq}`eq-dk-2to1`).
- **Identities.** {eq}`eq-dk-3to2` and {eq}`eq-dk-ck` hold exactly, for this graph and for the karate club.

### Shrinking graph sets

I enumerated all $\binom{21}{8} = 203{,}490$ labelled graphs on 7 nodes with 8 edges. I kept those with the same **per-node** degrees as $G_0$ (the space the swaps explore), and then those also matching 2k and 3k.

| $d$ | $\lvert\mathcal{G}_d\rvert$ | $H_d = \ln\lvert\mathcal{G}_d\rvert$ | swap-connected? |
|---|---|---|---|
| 0k | 203,490 | 12.22 | — |
| 1k | 243 | 5.49 | yes: 1k-swaps reach all 243 |
| 2k | 108 | 4.68 | yes: 2k-swaps reach all 108 |
| 3k | 18 | 2.89 | — |

The 18 graphs at 3k are **all isomorphic to $G_0$**. This is exactly the number of degree-preserving relabellings: $1!\,3!\,3!/\lvert\mathrm{Aut}(G_0)\rvert = 36/2$. So $D_{G_0} = 3$, while the 2k level still contains non-isomorphic graphs.

### $dk$ versus $d$-series

There are 853 connected graphs on 7 nodes, up to isomorphism. This table shows how many classes each statistic separates them into.

| statistic | classes | uniquely identified graphs | largest class |
|---|---|---|---|
| 0k $(L)$ | 16 | 2 | 138 |
| 1k | 236 | 99 | 20 |
| $d=3$: $(L, t, w)$ | 299 | 134 | 14 |
| 2k | 598 | 445 | 6 |
| 3k | **853** | **853** | 1 |

The degree-labelled 3k-sequence identifies **every** connected 7-node graph. The unlabelled 3-sequence leaves classes of up to 14 graphs. The unlabelled 3-sequence also separates more graphs than the 1k-sequence (299 vs 236 classes) although neither determines the other. This is the non-nestedness of the $d$-series in miniature.

### Discrepancy: the notes' chain and star example

The notes illustrate slow $d$-series convergence with the $N$-chain (path $P_N$) and the $N$-star. They say the 3-sequence fixes neither, but the 3k-sequence fixes both, "so $D_{G_0}=3$ for any $N$". Brute force does not support this as stated:

- **Star.** The degree sequence $(N-1, 1, \dots, 1)$ has a unique realisation, so the star has $D = 1$. Its 3-sequence $(N, N-1, 0, \binom{N-1}{2})$ also identifies it among all graphs on $N \le 7$ nodes.
- **Path, among connected graphs.** The degree sequence of a connected path already forces a path, so $D = 1$ there too.
- **Path, among all graphs.** The disjoint union $C_m \cup P_{N-m}$ has the same $dk$-sequences as $P_N$ for every $d < m$. Computed:
  - $C_4\cup P_6$ vs $P_{10}$ first differ at 4k;
  - $C_5 \cup P_7$ vs $P_{12}$ at 5k;
  - $C_6\cup P_8$ vs $P_{14}$ at 6k.

  So $D_{P_N}$ grows roughly like $N/2$.

The underlying point is still right: degree labels make the $dk$-series converge much faster than the $d$-series (see the table above). Disconnected look-alikes are the main obstruction, which is one reason the literature usually works within connected graphs or the giant component.

### $dk$-random versions of the karate club

The 2k level preserves $r$ exactly, by construction. This table gives the mean ± sd over 20 samples per level:

- **0k:** $G(N,L)$.
- **1k and 2k:** $20L$ accepted swaps.
- **2.1k and 2.5k:** 4,000 further Metropolis 2k-swap proposals, with $\beta = 200$ and $\beta = 20$ respectively.

Path lengths are measured on the giant component; $S$ is the giant-component fraction.

| | $\langle C\rangle$ | transitivity | $r$ | $\langle d\rangle$ | $d_{\max}$ | $S$ |
|---|---|---|---|---|---|---|
| **real** | 0.571 | 0.256 | −0.476 | 2.408 | 5 | 1.000 |
| 0k | 0.150 ± 0.047 | 0.145 ± 0.035 | −0.066 ± 0.089 | 2.391 ± 0.042 | 4.75 ± 0.54 | 0.993 ± 0.013 |
| 1k | 0.361 ± 0.048 | 0.232 ± 0.026 | −0.289 ± 0.051 | 2.267 ± 0.053 | 4.30 ± 0.64 | 1.000 |
| 2k | 0.325 ± 0.052 | 0.170 ± 0.017 | −0.476 (exact) | 2.185 ± 0.022 | 4.00 | 1.000 |
| 2.1k | 0.564 ± 0.010 | 0.234 ± 0.008 | −0.476 | 2.251 ± 0.031 | 4.00 | 1.000 |
| 2.5k | 0.547 ± 0.018 | 0.237 ± 0.006 | −0.476 | 2.247 ± 0.024 | 4.00 | 1.000 |

How to read this table:

- **1k gets about two-thirds of the clustering.** It is not zero: in a small, heterogeneous graph the hubs force triangles. 1k also reproduces about 60% of the disassortativity, the familiar "structural" disassortativity of degree-constrained simple graphs ([Barabási ch. 7](../nets-5116/barabasi/07-degree-correlations.md)).
- **2k fixes $r$ but not clustering.** Its $\langle C\rangle$ is even a little lower than 1k's.
- **2.1k and 2.5k restore clustering and transitivity.** One sample's annealing energy $\Phi_{2.5k}$ fell from 8.4 after 2k-randomisation to 0.49.
- **No level reproduces the diameter of 5 or $\langle d\rangle \approx 2.41$.** The karate club's two-faction split stretches distances, and that mesoscale community structure is not a function of degree correlations plus clustering in a 34-node graph. Here **community structure is a genuinely non-random feature** in the $dk$ sense.

(sec-dk-limitations)=
## Assumptions and limitations

- **Microcanonical only.** Every $M_d$ fixes the statistic exactly. Analytic work is easier with canonical (soft) analogues, which exist for 1k (the [SCM](./05-configuration-models.md)) and 2k, but not easily for 2.1k and 2.5k. The microcanonical and canonical versions are not equivalent when the constraints are extensive in number (see [typicality](./04-typicality-and-max-entropy.md)).
- **Samples, not formulas.** Beyond 1k there are few closed-form predictions. Properties of $M_2$ and higher are estimated by MCMC sampling, so the uniformity guarantee ({prf:ref}`prop-dk-uniform`) and the mixing time matter.
- **Annealed levels are not exactly uniform.** The 2.1k and 2.5k targets are reached by optimisation, and then sampled near $\Phi \approx 0$. The result is "maximally random" only approximately, and depends on $\beta$, the schedule and the stopping tolerance.
- **"Reproduces" needs a statistical test.** $d_g$ depends on how one decides that $G_0$'s value of $g$ is typical in $M_d$ (z-score, tolerance, …). Strongly self-averaging properties are easier to call.
- **Degree-labelled subgraphs explode combinatorially.** Already 4k has six subgraph types times four degree labels. At 3k and beyond almost every real graph is close to unique, so $M_3$ is nearly trivial: very little randomness is left to "explain" anything with.
- **Disconnected look-alikes.** As shown above, $D_{G_0}$ can be large because of disjoint unions. Conditioning on connectedness, or working on the giant component, is a modelling choice the notes leave implicit.
- **Not everything is local.** Geometry, community structure and long-range organisation (the power grid in Orsini et al.; the karate club's diameter above) can need $d$ far beyond 2.5k. For such properties, [latent-space](./08-latent-space-models.md) or [block](./09-stochastic-block-models.md) models are better explanations than ever-higher $d$.

## Connections

- **NETS 5116.**
  - The 0k level is $G(N,L)$ ([Barabási ch. 3](../nets-5116/barabasi/03-random-networks.md)) and the 1k level is the configuration model.
  - The 2k level formalises degree correlations, $\bar k_{nn}(k)$ and $r$ ([Barabási ch. 7](../nets-5116/barabasi/07-degree-correlations.md); [Newman ch. 7](../nets-5116/newman/07-measures-and-metrics.md)).
  - The degree-preserving rewiring used there to detect correlations is the 1k-swap.
- **NETS 6116.**
  - Each $M_d$ is a microcanonical maximum-entropy ensemble ([typicality and max-entropy](./04-typicality-and-max-entropy.md)); $M_1$ is the CM, and its soft cousin is the SCM ([configuration models](./05-configuration-models.md)).
  - The statistics at 2k and 3k are the assortativity and clustering of [clustering and assortativity](./02-clustering-and-assortativity.md).
  - [Hidden-variable models](./07-hidden-variables-and-graphons.md) are a canonical route to prescribed 2k correlations.
  - [Latent-space models](./08-latent-space-models.md) explain clustering geometrically instead of fixing it at 2.5k.
- **PHYS 7335.**
  - Degree-based mean-field theory needs exactly the 2k-statistics. With $P(k'\mid k) = \langle k\rangle P(k,k')/(k p_k)$, the correlated threshold $\lambda_c = 1/\Lambda_{\max}(C)$ is a **2k-property** ([degree-block formalism](../phys-7335/01-degree-block-formalism.md); [heterogeneous mean-field](../phys-7335/05-heterogeneous-mean-field.md)). So $M_2$ is the natural null model for testing HMF predictions.
  - Clustering changes SIR outbreaks beyond what 2k predicts ([SIR and percolation](../phys-7335/07-sir-percolation.md)), which is a case where 2.5k matters.
- **NETS 7332.**
  - Degree-labelled subgraph counts are graphlet features with degree labels ([graph ML tasks and features](../nets-7332/basics/01-graph-ml-tasks-and-features.md)).
  - The first two rounds of 1-WL colour refinement start from degrees (1k) and then use neighbour-degree multisets, a per-node refinement of 2k ([GNN expressive power](../nets-7332/basics/06-gnn-expressive-power.md)).
  - $dk$-random graphs are a principled baseline for graph generative models ([scaling and generative models](../nets-7332/basics/08-scaling-and-generative.md)), and 2.5k is a strong "structure-matched" null. See also [Gjoka, Kurant & Markopoulou (2013)](doi:10.48550/arXiv.1208.3667) on estimating 2.5k from samples.

## Self-test

:::{dropdown} Q1. State the two requirements of the $dk$-series and why together they make $d_g$ meaningful.
**Monotonicity:** $f_d$ fixes all $f_{d'}$ with $d' < d$, so the graph sets are nested. **Convergence:** some finite $D_{G_0}$ pins down $G_0$. Convergence guarantees that a minimal reproducing level $d_g$ exists. Monotonicity guarantees that every higher level also reproduces $g$, so $d_g$ is a threshold, not a coincidence.
:::

:::{dropdown} Q2. Show that the 2k-distribution fixes $\langle k\rangle$. What doesn't it fix?
$\sum_{k'}P(k,k') = k p_k/\langle k\rangle$. Divide by $k$ and sum over $k\ge 1$: $1/\langle k\rangle = \sum_{k,k'}P(k,k')/k$, a harmonic mean over edge ends. It doesn't fix $p_0$: isolated nodes are invisible, so you need $N$ from the sequence.
:::

:::{dropdown} Q3. What condition makes a double-edge swap 2k-preserving, and why?
$(a,b),(c,d) \to (a,d),(c,b)$ requires $k_b = k_d$. Then $a$ swaps one degree-$k_b$ neighbour for another, as does $c$. Every edge's endpoint-degree pair is unchanged, so $n(k,k')$ is preserved. All node degrees are preserved too.
:::

:::{dropdown} Q4. Why do 2.1k and 2.5k exist instead of just using 3k?
3k fixes the full degree-labelled triangle and wedge census. That is so restrictive that almost no 3k-swaps exist, and $M_3$ is close to the single graph $G_0$. 2.1k and 2.5k keep the most important 3k summary, clustering ($\langle C\rangle$ or $\bar C(k)$), on top of 2k, and leave everything else maximally random. They are reached by Metropolis annealing with $\Phi = \lvert\Delta\langle C\rangle\rvert$ or $\sum_i \lvert\Delta\bar C(k_i)\rvert$.
:::

:::{dropdown} Q5. Is the assortativity coefficient $r$ reproduced by 1k-random graphs? By 2k?
By 2k, always: $r$ is the Pearson correlation of $P(k,k')$. By 1k, only partly. Degree-preserving randomisation of a heterogeneous simple graph is already disassortative, because of the structural constraints: about $-0.29$ against the real $-0.48$ for the karate club. The difference is the "genuine" correlation.
:::

:::{dropdown} Q6. Why is the uniform distribution stationary for the swap chain, and what common implementation breaks this?
If proposals are uniform over (ordered) edge pairs and invalid swaps are rejected as self-loops, then $Q(G\to G') = Q(G'\to G)$. A symmetric kernel has the uniform distribution as a stationary distribution, and ergodicity makes it unique. Choosing uniformly among only the valid swaps makes the kernel depend on how many valid moves each graph has, and that biases the chain.
:::

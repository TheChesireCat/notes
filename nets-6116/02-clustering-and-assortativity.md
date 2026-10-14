---
title: Clustering and Assortativity
short_title: Clustering & assortativity
subject: NETS 6116 · Topic
description: The definitions of global, local and degree-dependent clustering and of degree assortativity, why the two clustering averages disagree, and why both properties are well defined for a single graph but problematic as N → ∞.
tags: [clustering, transitivity, assortativity, degree-correlations, structural-cutoff, watts-strogatz]
---

:::{tip} TL;DR
- **Two clustering averages, two different questions.** The global clustering $C = \sum_i t_i / \sum_i \binom{k_i}{2}$ is the probability that a random *wedge* closes into a triangle, so it weights high-degree nodes. The average local clustering $\langle C \rangle$ is the probability that two random neighbours of a random node are linked, so it weights low-degree nodes. On the windmill graph (triangles sharing one hub), $C = 3/(2n+1) \to 0$ while $\langle C \rangle \to 1$.
- **"Strong clustering" is a property of a graph sequence, not of a graph:** $\liminf_{N\to\infty} \langle C \rangle_N > 0$. Sparse ER and configuration-model graphs have $C = O(1/N)$, so a real network's $C$ only says something when compared with a model. Krioukov's heuristic: sparsity is caused by cost, small worlds by randomness, clustering by **geometry**.
- **Degree correlations live in the joint degree distribution** $P(k,k')$. It determines $p_k = \frac{\langle k\rangle}{k}\sum_{k'}P(k,k')$, the conditional $P(k'\mid k) = \langle k\rangle P(k,k')/(k\,p_k)$, and $\bar k_{nn}(k)$. Uncorrelated means $\bar k_{nn}(k) = \kappa = \langle k^2\rangle/\langle k\rangle$ for all $k$.
- **Assortativity $r$** is the Pearson correlation of the degrees at the two ends of a random edge: $r = \dfrac{\langle k\rangle^2\langle kk'\rangle - \langle k^2\rangle^2}{\langle k\rangle\langle k^3\rangle - \langle k^2\rangle^2}$. An increasing (decreasing) $\bar k_{nn}(k)$ forces $r > 0$ ($r < 0$).
- **$r$ breaks down for heavy tails.** For $\gamma < 3$ the structural cutoff $k_s = \sqrt{\langle k\rangle N}$ lies below the natural cutoff $k_{\max} \sim N^{1/(\gamma-1)}$, which forces disassortativity. Yet when $\langle k^3\rangle = \infty$, every limit of $r_N$ is $\ge 0$ (Litvak & van der Hofstad). In practice, plot $\bar k_{nn}(k)$ or use Spearman's rank correlation.
:::

- **Source.**
  - Krioukov, *Network Science II* lecture notes, ch. 3 (Clustering) and ch. 4 (Assortativity).
  - [](doi:10.1038/30918) (Watts & Strogatz, *Nature* 393, 440, 1998): the clustering coefficient and the small-world model.
  - [](doi:10.1103/PhysRevLett.89.208701) and [](doi:10.1103/PhysRevE.67.026126) (Newman, *PRL* 89, 208701, 2002; *PRE* 67, 026126, 2003): the assortativity coefficient.
  - [](doi:10.1103/PhysRevLett.87.258701) (Pastor-Satorras, Vázquez & Vespignani, *PRL* 87, 258701, 2001): $\bar k_{nn}(k)$ and $C(k)$ for the Internet.
  - [](doi:10.1140/epjb/e2004-00038-8) (Boguñá, Pastor-Satorras & Vespignani, *EPJ B* 38, 205, 2004): the structural cutoff.
  - [](doi:10.1103/PhysRevE.87.022801) (Litvak & van der Hofstad, *PRE* 87, 022801, 2013) and [](doi:10.1080/15427951.2013.850455) (van der Hofstad & Litvak, *Internet Math.* 10, 287, 2014): the non-negativity of the limit of $r$.
- **Builds on.** [Sparsity and small-worldness](./01-sparsity-and-small-worlds.md), whose "fixed $N$ versus $N \to \infty$" argument is reused here, and the 5116 notes on [degree correlations](../nets-5116/barabasi/07-degree-correlations.md) and [clustering](../nets-5116/newman/07-measures-and-metrics.md).
- **Notation.** Shared symbols as in [](#notation): $N$, $L$, $\langle k\rangle$, $p_k$ for Krioukov's $n$, $m$, $\bar k$, $P(k)$. Clustering is $C$, $C_i$, $\langle C\rangle$ (Krioukov: $c$, $c_i$, $\bar c$). Krioukov writes the assortativity coefficient $\rho_G$; here it is $r$, because $\rho$ is prevalence elsewhere. Page-specific symbols:
  - $\omega_i = \binom{k_i}{2}$, the number of wedges centred at $i$ (Krioukov: $w_i$);
  - $C(k)$, degree-dependent clustering;
  - $P(k,k')$, the joint degree distribution; $\tilde p_k = k p_k/\langle k\rangle$, the edge-end degree distribution (not the excess-degree $q_k$);
  - $k_s$ and $k_{\max}$, the structural and natural cutoffs.

(sec-clust-setup)=
## Setup and definitions

Throughout, $G$ is a simple undirected graph. Directed networks are symmetrised before measuring clustering, as in Krioukov's table of real networks.

:::{prf:definition} Wedges and triangles
:label: def-clust-wedges

For node $i$ of degree $k_i$:
- $\omega_i = \binom{k_i}{2}$ is the number of pairs of neighbours of $i$, i.e. of **wedges** (paths of length 2) centred at $i$;
- $t_i$ is the number of those pairs that are themselves linked, i.e. the number of triangles containing $i$.

Summing, $\sum_i \omega_i$ is the total number of wedges and $\sum_i t_i = 3 \times (\text{number of triangles})$.
:::

:::{prf:definition} Clustering coefficients
:label: def-clust-coefficients

- **Global clustering** (transitivity): $C = \sum_i t_i \big/ \sum_i \omega_i$.
- **Local clustering** of node $i$: $C_i = t_i/\omega_i$, defined only when $k_i \ge 2$.
- **Degree-dependent clustering**: $C(k) = \frac{1}{N_k}\sum_i C_i\,\mathbb{1}\{k_i = k\}$, defined for $k \ge 2$.
- **Average clustering**: $\langle C\rangle = \frac{1}{N_{>1}}\sum_{i:\,k_i>1} C_i = \sum_{k\ge 2} C(k)\,p_k^{>1}$, where $N_{>1} = N - N_0 - N_1$ and $p_k^{>1} = N_k/N_{>1}$.
:::

Both $C$ and $\langle C\rangle$ lie in $[0,1]$, vanish on triangle-free graphs (trees, bipartite graphs) and equal 1 on complete graphs. Krioukov stresses that setting $C_i = 0$ for $k_i \le 1$ "cannot be rigorously justified". Software often does it anyway: `networkx.average_clustering` counts those nodes as zeros by default, which lowers $\langle C\rangle$ (see the [worked example](#sec-clust-example)).

:::{prf:definition} Strong clustering
:label: def-clust-strong

A network model, i.e. a random-graph sequence $G_N$ with $N \to \infty$, has **strong** (high, non-vanishing) **clustering** if $\liminf_{N\to\infty}\langle C\rangle_N > 0$. The $\liminf$ matters: the limit need not exist.
:::

:::{prf:definition} Joint degree distribution
:label: def-clust-jdd

The **joint degree distribution** (JDD) $P(k,k')$ is the probability that a uniformly random edge, with a uniformly random orientation, joins a node of degree $k$ to a node of degree $k'$. In a fixed graph,

$$
P(k,k') = \frac{L(k,k')}{2L}, \qquad L(k,k') = (1+\delta_{kk'})\,n(k,k'),
$$ (eq-clust-jdd)

where $n(k,k') = n(k',k)$ is the number of edges between degree-$k$ and degree-$k'$ nodes. The factor $1+\delta_{kk'}$ makes $L(k,k')$ count edge *ends*, so $\sum_{k'} L(k,k') = k N_k$, the number of stubs on degree-$k$ nodes. $P(k,k')$ is symmetric and sums to 1.
:::

:::{prf:definition} Assortativity coefficient
:label: def-clust-r

The **assortativity coefficient** $r$ of $G$ is the Pearson correlation coefficient of $k$ and $k'$ under $P(k,k')$. $G$ is **assortative**, **uncorrelated** or **disassortative** if $r > 0$, $r = 0$ or $r < 0$.
:::

(sec-clust-core)=
## Core ideas

### Clustering in real networks, and what "high" means

Krioukov's table of real networks (the same networks as in his sparsity chapter; it appears to come from Menczer, Fortunato & Davis, [](doi:10.1017/9781108653947)) reports $C$ between 0.03 (Twitter US politics) and 0.67 (IMDB co-stars). The bipartite IMDB movies–stars graph has $C = 0$ by construction. The ratio to an ER graph of the same density, $p = 2L/(N(N-1))$, is what makes these numbers striking. I computed it from the table's $N$ and $L$:

| Network | $N$ | $\langle k\rangle$ | $C$ | ER $C = p$ | $C/p$ |
|---|---|---|---|---|---|
| Facebook Northwestern | 10,567 | 92.4 | 0.24 | $8.8\times10^{-3}$ | 27 |
| IMDB co-stars | 252,999 | 8.0 | 0.67 | $3.2\times10^{-5}$ | 21,000 |
| Internet routers | 190,914 | 6.4 | 0.16 | $3.3\times10^{-5}$ | 4,800 |
| World air transportation | 3,179 | 11.7 | 0.49 | $3.7\times10^{-3}$ | 130 |
| *C. elegans* brain | 297 | 15.8 | 0.29 | $5.3\times10^{-2}$ | 5 |

The same caveat as for sparsity and small-worldness applies (see [the previous page](./01-sparsity-and-small-worlds.md)). A single network has one $N$, so "clustering is high" can only mean "high relative to a model with the same $N$ and $\langle k\rangle$", or a statement about the sequence the network is imagined to come from. [](#def-clust-strong) is the formal version.

### Why $C$ and $\langle C\rangle$ disagree

Since $t_i = \omega_i C_i$,

$$
C = \frac{\sum_i \omega_i C_i}{\sum_i \omega_i},
$$ (eq-clust-weighted)

so $C$ is an average of the $C_i$ weighted by $\binom{k_i}{2} \propto k_i^2$, while $\langle C\rangle$ weights all nodes with $k_i \ge 2$ equally. In most real networks $C(k)$ decreases with $k$, often roughly as $k^{-1}$ [](doi:10.1103/PhysRevE.67.026112) (Ravasz & Barabási 2003), so typically $C < \langle C\rangle$. Probabilistically:
- $C$ = P(a uniformly random wedge is closed);
- $\langle C\rangle$ = P(two random neighbours of a uniformly random node with $k \ge 2$ are linked).

Report which one you use; they can differ by an order of magnitude.

### Clustering needs a mechanism, and the simplest one is geometry

In sparse uncorrelated models triangles are rare: ER has $C = p = \langle k\rangle/(N-1)$, and the configuration model has $C = O(1/N)$ when $\langle k^2\rangle$ is finite (see the [key results](#sec-clust-results)). Something must close triangles. Krioukov's position is that the simplest such mechanism is **metric space**: if $i$ is close to $j$ and $j$ to $\ell$, the triangle inequality makes $i$ close to $\ell$, so in a model that links nearby nodes, edges $ij$ and $j\ell$ make $i\ell$ likely. This is made precise in [](doi:10.1103/PhysRevLett.116.208302) (Krioukov 2016) and developed in [latent-space models](./08-latent-space-models.md).

Krioukov's summary of the first three chapters (his heuristic, not a theorem):

| Feature | Sparsity | Small-worldness | Clustering |
|---|---|---|---|
| Cause | cost | randomness | geometry |
| Effect | cost | communication | robustness |

The **Watts–Strogatz model** [](doi:10.1038/30918) was the first model with all three features, and it also builds in the *causes* of the last two. Start from a ring lattice (geometry, hence clustering) and rewire each edge with probability $p$ (randomness, hence shortcuts and $\langle d\rangle \sim \ln N$). For a wide range of small $p$, $C$ stays close to its lattice value while $\langle d\rangle$ has already collapsed ([](#prop-clust-ws)).

### Degree correlations

The JDD is the second level of description after $p_k$ (the "2K" level of the [dk-series](./06-dk-series.md)). Three objects are derived from it:
- the degree distribution, by marginalising ([](#eq-clust-pk));
- the conditional distribution $P(k'\mid k)$, the probability that an edge leaving a degree-$k$ node ends at a degree-$k'$ node ([](#eq-clust-cond)). This is the object in [degree-block epidemic models](../phys-7335/01-degree-block-formalism.md);
- the **average nearest-neighbour degree** $\bar k_{nn}(k) = \sum_{k'} k' P(k'\mid k)$ ([](#eq-clust-knn)), the function people actually plot [](doi:10.1103/PhysRevLett.87.258701).

A network is **uncorrelated** if the two ends of an edge are independent: $P(k,k') = \tilde p_k\,\tilde p_{k'}$ with $\tilde p_k = k p_k/\langle k\rangle$ the degree of a random edge end. Then $P(k'\mid k) = \tilde p_{k'}$ and $\bar k_{nn}(k) = \langle k^2\rangle/\langle k\rangle = \kappa$ for every $k$: the friendship paradox, uniform in $k$.

The scalar summary $r$ ([](#def-clust-r)) compares the edge-end degrees, whose distribution is $\tilde p_k$, not $p_k$. That is why the third moment of $p_k$ appears in its denominator ([](#eq-clust-r)).

### Why assortativity is not as well defined as it looks

Krioukov's verdict: "Hooray, we finally have a property which is well-defined for any given (real) network! Yes, but NO!" $r$ is a number for any finite graph with non-constant degrees. The trouble is the $N\to\infty$ limit:

1. **Moments diverge.** The variance of the edge-end degree is $\langle k^3\rangle/\langle k\rangle - \kappa^2$. If it diverges, the sample Pearson coefficient has no deterministic limit in general. The notes phrase this for an infinite *second* moment ($\gamma<3$); the moment that matters for $r$ is the third ($\gamma<4$).
2. **Structural correlations.** A simple graph cannot hold the edges that an uncorrelated heavy-tailed degree sequence demands between hubs, so the hubs are forced to link to low-degree nodes: disassortativity without any mechanism ([](#prop-clust-cutoff)) [](doi:10.1103/PhysRevE.68.026112) (Park & Newman 2003); [](doi:10.1140/epjb/e2004-00038-8).
3. **But the limit is non-negative.** Litvak & van der Hofstad proved that when $\langle k^3\rangle = \infty$, $r_N$ cannot converge to a negative value ([](#thm-clust-litvak)). Item 2 says hubs avoid each other; item 3 says $r$ cannot show it. The resolution is that $|r_N|$ of a disassortative network shrinks with $N$, so $r$ cannot compare networks of different sizes.

"In summary," Krioukov writes, "people just plot $k_{nn}(k)$ and enjoy the plots." The constructive alternative is a rank correlation (Spearman's $\rho$ of the edge-end degrees), which converges under general conditions [](doi:10.1080/15427951.2013.850455).

(sec-clust-results)=
## Key results

:::{prf:proposition} Global clustering is wedge-weighted local clustering
:label: prop-clust-weighted

$C = \sum_i \omega_i C_i / \sum_i \omega_i$, with $\omega_i = \binom{k_i}{2}$. Hence $C = \langle C\rangle$ whenever $C_i$ is constant over nodes with $k_i \ge 2$, and $C < \langle C\rangle$ whenever $C(k)$ is strictly decreasing and degrees are not all equal.
:::

:::{dropdown} Proof
The first claim is $t_i = \omega_i C_i$ summed over $i$ (nodes with $k_i \le 1$ have $\omega_i = t_i = 0$ and drop out). For the second, group nodes by degree: $C = \sum_k \omega(k) C(k) N_k / \sum_k \omega(k) N_k$ with $\omega(k) = \binom{k}{2}$ increasing in $k$. Write both averages as expectations over $K \sim p^{>1}$: $\langle C\rangle = \mathbb{E}[C(K)]$ and $C = \mathbb{E}[\omega(K) C(K)]/\mathbb{E}[\omega(K)]$. Then $C - \langle C\rangle = \mathrm{Cov}(\omega(K), C(K))/\mathbb{E}[\omega(K)]$. The covariance of an increasing and a decreasing function of the same variable is $\le 0$ (Chebyshev's sum inequality), and strictly negative when both are non-constant on the support.
:::

:::{prf:proposition} Clustering in the null models vanishes
:label: prop-clust-null

- $G(N,p)$: $\mathbb{E}\,C_i = p$ for every node, so $C \to \langle k\rangle/(N-1)$.
- Configuration model with degree distribution $p_k$ [](doi:10.1103/PhysRevE.64.026118), [](doi:10.1137/S003614450342480):

$$
C_{\mathrm{CM}} = \frac{1}{N}\,\frac{\left(\langle k^2\rangle - \langle k\rangle\right)^2}{\langle k\rangle^3}.
$$ (eq-clust-cm)

For Poisson degrees this is $\langle k\rangle/N$, the ER value. For $p_k \sim k^{-\gamma}$ with $k_{\max}\sim N^{1/(\gamma-1)}$, $\langle k^2\rangle \sim N^{(3-\gamma)/(\gamma-1)}$ and $C_{\mathrm{CM}} \sim N^{(7-3\gamma)/(\gamma-1)}$. This vanishes only for $\gamma > 7/3$; below that the formula exceeds 1 for large $N$. That signals the breakdown of the simple-graph assumption (multi-edges between hubs), the same phenomenon as the structural cutoff below.
:::

:::{dropdown} Derivation sketch of [](#eq-clust-cm)
Pick a node with two neighbours $j$ and $\ell$, each reached along an edge. Their *excess* degrees (stubs other than the one used) are independent draws from $q_k = (k+1)p_{k+1}/\langle k\rangle$, with mean $\sum_k k q_k = (\langle k^2\rangle - \langle k\rangle)/\langle k\rangle$. Given excess degrees $a$ and $b$, the probability that some stub of $j$ pairs with some stub of $\ell$ is $\approx ab/(2L) = ab/(N\langle k\rangle)$, assuming $ab \ll N\langle k\rangle$. Average over independent $a$ and $b$: $C \approx \left[(\langle k^2\rangle - \langle k\rangle)/\langle k\rangle\right]^2/(N\langle k\rangle)$. The independence and $ab \ll 2L$ assumptions fail exactly when hubs have $k^2 \gtrsim \langle k\rangle N$.
:::

:::{prf:proposition} Watts–Strogatz clustering
:label: prop-clust-ws

On a ring where every node is linked to its $K$ nearest neighbours on each side (degree $2K$),

$$
C(0) = \frac{3(K-1)}{2(2K-1)} \xrightarrow{K\to\infty} \frac{3}{4}.
$$ (eq-clust-ws)

After rewiring each edge with probability $p$, $C(p) \approx C(0)(1-p)^3$, a result due to [](doi:10.1007/s100510050067) (Barrat & Weigt 2000).
:::

:::{dropdown} Derivation
Label the neighbours of node 0 by ring offsets $\pm1,\dots,\pm K$, so $\omega = \binom{2K}{2} = K(2K-1)$. Two neighbours are linked iff their ring distance is $\le K$.
- Same side: any two offsets in $\{1,\dots,K\}$ are at distance $\le K-1$, so all $\binom{K}{2}$ pairs per side are linked: $K(K-1)$ in total.
- Opposite sides, offsets $-a$ and $+b$ with $a,b\ge1$: their distance $a+b \le K$ holds for $\sum_{a=1}^{K-1}(K-a) = K(K-1)/2$ pairs.

So $t = \tfrac32 K(K-1)$ and $C(0) = t/\omega = 3(K-1)/(2(2K-1))$. After rewiring, a lattice triangle survives only if none of its three edges was rewired, which happens with probability $(1-p)^3$. Triangles created by rewiring are $O(1/N)$, which gives the approximation. Simulations at $N = 2000$ agree to within a few percent; see the [worked example](#sec-clust-example).
:::

:::{prf:theorem} The JDD determines the degree distribution and $\bar k_{nn}$
:label: thm-clust-jdd

For any graph, with $P(k,k')$ as in [](#eq-clust-jdd),

$$
p_k = \frac{\langle k\rangle}{k}\sum_{k'} P(k,k') \qquad (k \ge 1),
$$ (eq-clust-pk)

$$
P(k'\mid k) = \frac{L(k,k')}{k N_k} = \frac{\langle k\rangle\,P(k,k')}{k\,p_k} = \frac{P(k,k')}{\sum_{k''}P(k,k'')},
$$ (eq-clust-cond)

$$
\bar k_{nn}(k) = \sum_{k'} k'\,P(k'\mid k) = \frac{\sum_{k'} k' P(k,k')}{\sum_{k''} P(k,k'')}.
$$ (eq-clust-knn)
:::

:::{dropdown} Derivation
The degree-$k$ nodes carry $kN_k$ stubs, each the end of exactly one edge, so $\sum_{k'}L(k,k') = kN_k$. Divide by $2L = N\langle k\rangle$: $\sum_{k'}P(k,k') = kN_k/(N\langle k\rangle) = k p_k/\langle k\rangle = \tilde p_k$, which rearranges to [](#eq-clust-pk). (The transcribed notes garble the denominator at this intermediate step; the boxed result is correct.) For the conditional, of the $kN_k$ stubs at degree-$k$ nodes, $L(k,k')$ lead to degree-$k'$ nodes, giving the first equality in [](#eq-clust-cond). Substitute $L(k,k') = 2L\,P(k,k')$ and $kN_k = 2L\,\tilde p_k$ for the rest. [](#eq-clust-knn) is the conditional mean.
:::

:::{prf:theorem} Assortativity in terms of degree moments
:label: thm-clust-r

With $\langle k^s\rangle = \sum_k k^s p_k$ and $\langle kk'\rangle = \sum_{k,k'} kk'\,P(k,k')$,

$$
r = \frac{\langle kk'\rangle - \kappa^2}{\langle k^3\rangle/\langle k\rangle - \kappa^2}
= \frac{\langle k\rangle^2\langle kk'\rangle - \langle k^2\rangle^2}{\langle k\rangle\langle k^3\rangle - \langle k^2\rangle^2}.
$$ (eq-clust-r)

Equivalently, over the edge list $\{(j_e, k_e)\}_{e=1}^{L}$ of end degrees [](doi:10.1103/PhysRevLett.89.208701):

$$
r = \frac{L^{-1}\sum_e j_e k_e - \left[L^{-1}\sum_e \tfrac12(j_e+k_e)\right]^2}{L^{-1}\sum_e \tfrac12(j_e^2+k_e^2) - \left[L^{-1}\sum_e \tfrac12(j_e+k_e)\right]^2}.
$$ (eq-clust-r-edges)
:::

:::{dropdown} Derivation
Both marginals of $P(k,k')$ equal the edge-end distribution $\tilde p_k = kp_k/\langle k\rangle$ (from the proof of [](#thm-clust-jdd)). Its moments are $\sum_k k\,\tilde p_k = \langle k^2\rangle/\langle k\rangle = \kappa$ and $\sum_k k^2\tilde p_k = \langle k^3\rangle/\langle k\rangle$. Pearson's coefficient is $\mathrm{Cov}(k,k')/\mathrm{Var}(k)$ (the two variances are equal by symmetry), which is the first form. Multiply numerator and denominator by $\langle k\rangle^2$ for the second. The notes' first form writes $\langle k^2\rangle$ and $\langle\tilde k\rangle$ for these edge-end moments, which reads ambiguously: the moments in the numerator and denominator are over $\tilde p_k$, not $p_k$. [](#eq-clust-r-edges) is the same quantity estimated by averaging each edge in both orientations.
:::

:::{prf:proposition} Monotone $\bar k_{nn}(k)$ fixes the sign of $r$
:label: prop-clust-sign

If $\bar k_{nn}(k)$ is non-decreasing, constant or non-increasing on the support of $\tilde p$, then $r \ge 0$, $r = 0$ or $r \le 0$, with strict inequality when it is non-constant there.
:::

:::{dropdown} Proof
Let $K \sim \tilde p$ be the degree at a random edge end and $K'$ the degree at the other end. By the tower property, $\mathrm{Cov}(K, K') = \mathrm{Cov}(K, \mathbb{E}[K'\mid K]) = \mathrm{Cov}(K, \bar k_{nn}(K))$. The covariance of $K$ with a non-decreasing function of $K$ is $\ge 0$, by Chebyshev's sum inequality or by writing it as $\tfrac12\mathbb{E}[(K-\hat K)(f(K)-f(\hat K))]$ with $\hat K$ an independent copy. It is strictly positive if $f$ is non-constant on the support. The converse fails: $r$ is one number, and a non-monotone $\bar k_{nn}(k)$ can give any sign.
:::

:::{prf:proposition} Structural cutoff and structural disassortativity
:label: prop-clust-cutoff

In an uncorrelated network, the expected number of edges between degree classes is $L(k,k') = (kN_k)(k'N_{k'})/(2L)$. A simple graph needs $L(k,k') \le N_kN_{k'}$, i.e.

$$
kk' \le 2L = \langle k\rangle N \quad\Longrightarrow\quad k_s = \sqrt{\langle k\rangle N}.
$$ (eq-clust-ks)

For $p_k\sim k^{-\gamma}$ the natural cutoff (expected largest degree) is $k_{\max}\sim N^{1/(\gamma-1)}$. For $\gamma<3$, $1/(\gamma-1) > 1/2$, so $k_s \ll k_{\max}$ as $N\to\infty$. There are then not enough hub pairs to hold the hub–hub edges that independence requires, those edges are pushed onto lower-degree partners, and the simple graph is necessarily disassortative [](doi:10.1140/epjb/e2004-00038-8), [](doi:10.1103/PhysRevE.68.026112).
:::

:::{prf:theorem} Non-negativity of the assortativity limit (Litvak & van der Hofstad)
:label: thm-clust-litvak

Let $G_N$ be a graph sequence whose degree distribution has $\langle k^3\rangle_N \to \infty$ (e.g. $p_k\sim k^{-\gamma}$ with $\gamma < 4$). Then every limit in distribution of $r_N$ is non-negative. For disassortative sequences, $r_N \to 0$: the magnitude of negative $r$ decreases with $N$. The notes state it without the moment condition, for any $p_k$ with infinite *second* moment, and cite §1.5 of van der Hofstad's *Random Graphs and Complex Networks* [](doi:10.1017/9781316779422); the primary papers are [](doi:10.1103/PhysRevE.87.022801) and [](doi:10.1080/15427951.2013.850455), which need the *third* moment to diverge. A diverging second moment ($\gamma<3$) implies a diverging third, but $3 < \gamma < 4$ also qualifies.
:::

:::{dropdown} Why (my sketch, not the paper's proof)
Write $r_N$ through [](#eq-clust-r-edges). The denominator is dominated by $\sum_e (j_e^2+k_e^2)$, a sum of squared heavy-tailed variables controlled by the few largest degrees: it scales like $\sum_i k_i^3$. The negative part of the numerator is $\left[\sum_e (j_e+k_e)\right]^2/L$, i.e. $(\sum_i k_i^2)^2/L$. When $\langle k^3\rangle = \infty$, $(\sum_i k_i^2)^2 / (L\sum_i k_i^3) \to 0$ in probability, because the largest $k_i^3$ dominates its sum more strongly than the largest $k_i^2$ dominates its own. The surviving term $\sum_e j_e k_e$ is non-negative, so whatever limit $r_N$ has is $\ge 0$. Van der Hofstad & Litvak prove this first for i.i.d. pairs of heavy-tailed non-negative variables, then for graphs.
:::

(sec-clust-example)=
## Worked example

All numbers were computed with `networkx` 3.x (scratch script, not part of the site).

**Windmill graph $F_n$**: $n$ triangles sharing one hub. The hub has $k = 2n$ and $t = n$; each of the $2n$ leaves has $k = 2$ and $C_i = 1$.
- $C = \dfrac{3n}{n(2n-1) + 2n} = \dfrac{3}{2n+1}$ and $\langle C\rangle = \dfrac{2n + 1/(2n-1)}{2n+1}$.
- Edges: $2n$ of type $(2n, 2)$ and $n$ of type $(2,2)$. In [](#eq-clust-r-edges) the numerator is $-4(n-1)^2/9$ and the denominator $8(n-1)^2/9$, so **$r = -1/2$ for every $n \ge 2$** ($r$ is undefined for $n=1$, where all degrees are equal).

| $n$ | $C$ | $\langle C\rangle$ | $r$ |
|---|---|---|---|
| 2 | 0.600 | 0.867 | −0.5 |
| 5 | 0.273 | 0.919 | −0.5 |
| 100 | 0.0149 | 0.995 | −0.5 |

The windmill is the cleanest illustration of [](#prop-clust-weighted): $C(k)$ falls from 1 at $k=2$ to $1/(2n-1)$ at the hub, and the hub's $\binom{2n}{2}$ wedges dominate $C$.

**Zachary karate club** ($N = 34$, $L = 78$):
- $C = 0.2557$.
- $\langle C\rangle = 0.5879$ under Krioukov's convention (excluding the one node of degree 1), and $0.5706$ from `networkx.average_clustering`, which counts it as a zero.
- $C(k)$ falls overall (not monotonically) from 0.91 at $k=2$ to 0.11 at $k=17$.
- $\bar k_{nn}(k)$ falls from 16.0 at $k=1$ (that node's only neighbour is the hub) to 3.82 at $k=17$. It is close to non-increasing, consistent with $r = -0.4756$ (the moment formula [](#eq-clust-r) gives the same value). Spearman's rank correlation of edge-end degrees is $-0.479$, and $\kappa = 7.77$.

**Structural versus natural cutoff**, for $\gamma = 2.5$, $k_{\min} = 2$ (so $\langle k\rangle = k_{\min}(\gamma-1)/(\gamma-2) = 6$), with $k_{\max} = k_{\min}N^{1/(\gamma-1)}$:

| $N$ | $k_s = \sqrt{\langle k\rangle N}$ | $k_{\max}$ | $k_{\max}/k_s$ |
|---|---|---|---|
| $10^4$ | 245 | 928 | 3.8 |
| $10^6$ | 2,449 | 20,000 | 8.2 |
| $10^8$ | 24,495 | 430,887 | 17.6 |

The gap grows like $N^{1/(\gamma-1) - 1/2} = N^{1/6}$, so in the limit the forced disassortativity of [](#prop-clust-cutoff) only gets stronger.

**Watts–Strogatz**, $N = 2000$, averaged over 3 seeds: for $K = 2$, $C(0) = 0.5$ exactly; at $p = 0.1$, the simulation gives $C = 0.351$ against $C(0)(1-p)^3 = 0.365$. For $K = 5$, $C(0) = 2/3$; at $p = 0.1$, 0.477 against 0.486.

## Assumptions and limitations

- **Finite graph versus sequence.** "High clustering", "assortative" and "disassortative" are only formal for sequences $G_N$. For one network they mean "relative to a null model" (ER, the configuration model, or a [dk-random graph](./06-dk-series.md)), and the answer depends on the null.
- **Nodes with $k \le 1$.** $\langle C\rangle$ depends on whether they are dropped or counted as zeros. Neither choice is canonical; state it.
- **Degree-only correlations.** $r$ and $\bar k_{nn}$ only see degree–degree dependence. Mixing by attributes (homophily) needs the attribute version of $r$ [](doi:10.1103/PhysRevE.67.026126).
- **$r$ is not size-comparable.** For heavy tails, $r$ depends on $N$ ([](#thm-clust-litvak)), so comparing $r$ between a 10⁴-node and a 10⁸-node network is meaningless. Use $\bar k_{nn}(k)$ plots or rank correlations.
- **Structural correlations confound mechanism.** Disassortativity in a $\gamma < 3$ network may be fully explained by the simple-graph constraint. Compare against a degree-preserving randomisation, i.e. the maximum-entropy model with the same degree sequence [](doi:10.1126/science.1065103) (Maslov & Sneppen 2002), before claiming a mechanism.
- **Directed and weighted networks.** Clustering here ignores directions and weights. Directed graphs have four in/out assortativity coefficients.

## Connections

- **NETS 5116.**
  - Barabási ch. 7 ([degree correlations](../nets-5116/barabasi/07-degree-correlations.md)) covers $\bar k_{nn}(k) \sim k^{\mu}$, the structural cutoff (§7.4) and the relation between $\mu$ and $r$.
  - Newman ch. 7 ([measures and metrics](../nets-5116/newman/07-measures-and-metrics.md)) defines transitivity, local clustering and the assortativity coefficient for both degrees and categorical attributes.
  - Newman ch. 10 ([real-world structure](../nets-5116/newman/10-structure-of-real-world-networks.md)) and Barabási ch. 3 ([random networks](../nets-5116/barabasi/03-random-networks.md)) give the empirical clustering values that random graphs fail to reproduce.
- **NETS 6116.**
  - [Sparsity and small-worldness](./01-sparsity-and-small-worlds.md) is the companion "fixed $N$ versus $N \to\infty$" argument.
  - The JDD is the 2K constraint of the [dk-series](./06-dk-series.md), and 2.5K adds $C(k)$.
  - The [configuration models](./05-configuration-models.md) are the null models of [](#prop-clust-null), and their soft versions reproduce structural correlations exactly.
  - Clustering from geometry is the subject of [latent-space models](./08-latent-space-models.md).
- **PHYS 7335.**
  - $P(k'\mid k)$ is the input to the [degree-block formalism](../phys-7335/01-degree-block-formalism.md).
  - The correlated epidemic threshold $\lambda_c = 1/\Lambda_m$ of $C_{kk'} = kP(k'\mid k)$ is on the [heterogeneous mean-field page](../phys-7335/05-heterogeneous-mean-field.md); there, assortativity changes the threshold's value but not its vanishing when $\langle k^2\rangle = \infty$.
  - Clustering slows SIR outbreaks because it wastes transmissions on already-infected neighbours; see [SIR and percolation](../phys-7335/07-sir-percolation.md).
- **NETS 7332.**
  - $C_i$ and $\bar k_{nn}$ are classic hand-crafted node features ([graph ML tasks and features](../nets-7332/basics/01-graph-ml-tasks-and-features.md)).
  - Attribute assortativity is homophily; see [higher-order homophily](../nets-7332/readings/03-higher-order-homophily.md). The hypergraph analogue of clustering is in [representations](../nets-7332/readings/01-representations.md).

## Self-test

:::{dropdown} Q1. Give a probabilistic interpretation of $C$ and of $\langle C\rangle$, and say which one weights hubs more. Construct a graph where $C \to 0$ while $\langle C\rangle \to 1$.
$C$ is the probability that a random wedge is closed, and $\langle C\rangle$ the probability that two random neighbours of a random node (with $k \ge 2$) are linked. $C$ weights node $i$ by $\binom{k_i}{2}$, so hubs dominate. The windmill $F_n$ has $C = 3/(2n+1)\to0$ and $\langle C\rangle\to1$.
:::

:::{dropdown} Q2. Why is "this network is highly clustered" not a formal statement, and what is the formal version?
A single graph has one $N$; there is no limit to take. The formal statement is about a model or sequence: $\liminf_N \langle C\rangle_N > 0$. For a real network one compares with a null model of the same size and density (e.g. $C/p$, or the configuration model's $C$).
:::

:::{dropdown} Q3. Derive $p_k$ and $\bar k_{nn}(k)$ from the JDD. What is $\bar k_{nn}(k)$ in an uncorrelated network?
$\sum_{k'}P(k,k') = kN_k/(2L) = kp_k/\langle k\rangle$, so $p_k = (\langle k\rangle/k)\sum_{k'}P(k,k')$. Then $P(k'\mid k) = P(k,k')/\sum_{k''}P(k,k'')$ and $\bar k_{nn}(k) = \sum_{k'}k'P(k'\mid k)$. If uncorrelated, $P(k,k') = \tilde p_k\tilde p_{k'}$, so $\bar k_{nn}(k) = \langle k^2\rangle/\langle k\rangle$ for every $k$.
:::

:::{dropdown} Q4. Why does $\langle k^3\rangle$ appear in the formula for $r$?
$r$ correlates the degrees at the two ends of an edge. An edge end lands on a node with probability proportional to its degree, so the edge-end distribution is $kp_k/\langle k\rangle$, whose second moment is $\langle k^3\rangle/\langle k\rangle$. That is the variance term in the denominator.
:::

:::{dropdown} Q5. Derive the structural cutoff. When does it bind, and what does it do to $r$?
Uncorrelated wiring needs $L(k,k') = kN_k\,k'N_{k'}/(2L) \le N_kN_{k'}$, i.e. $kk' \le \langle k\rangle N$, so $k_s = \sqrt{\langle k\rangle N}$. It binds when $k_{\max} \sim N^{1/(\gamma-1)}$ exceeds $k_s$, i.e. $\gamma < 3$. Hub–hub edges are then missing, which forces disassortativity even in a maximally random simple graph.
:::

:::{dropdown} Q6. Structural correlations force disassortativity for $\gamma < 3$, yet Litvak & van der Hofstad prove $\lim r_N \ge 0$. Reconcile these. What should you measure instead?
Both hold: the hubs do avoid each other, but when $\langle k^3\rangle = \infty$ the denominator of $r_N$ grows faster than the negative part of its numerator, so $r_N \to 0^-$ or to a non-negative limit. $r$ is a poor, size-dependent statistic for heavy-tailed networks. Plot $\bar k_{nn}(k)$, or use Spearman's rank correlation, which has a proper limit.
:::

:::{dropdown} Q7. Compute $C(0)$ for the Watts–Strogatz ring with $K$ neighbours per side, and explain why $C(p)\approx C(0)(1-p)^3$.
$\omega = K(2K-1)$ neighbour pairs; same-side pairs give $K(K-1)$ links and cross pairs with $a+b\le K$ give $K(K-1)/2$, so $C(0) = 3(K-1)/(2(2K-1))\to3/4$. A lattice triangle survives rewiring iff none of its three edges is rewired, with probability $(1-p)^3$. New triangles from rewiring are $O(1/N)$.
:::

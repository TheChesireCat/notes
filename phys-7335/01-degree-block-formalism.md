---
title: Networks Review and the Degree-Block (Annealed) Formalism
short_title: Degree-block formalism
subject: PHYS 7335 · Topic
description: How a network is compressed into degree classes, the conditional degree distribution and its detailed-balance constraint, the annealed adjacency matrix, and why the heterogeneity ⟨k²⟩/⟨k⟩ will control every threshold.
tags: [degree-based-mean-field, annealed-networks, degree-correlations, scale-free, cutoffs, heterogeneity]
---

:::{tip} TL;DR
- **Degree-block (degree-based mean-field) idea:** treat all nodes of degree $k$ as statistically equivalent, and track one variable per degree class, e.g. $\rho_k = I_k/N_k$, instead of one per node. The total is $\rho = \sum_k p_k \rho_k$.
- A network is then summarised by $p_k$ and the **conditional degree distribution** $P(k'\mid k)$, the probability that an edge leaving a degree-$k$ node reaches a degree-$k'$ node. Edge counting forces **degree detailed balance**, $k\,p_k\,P(k'\mid k) = k'\,p_{k'}\,P(k\mid k')$. For **uncorrelated** networks, $P(k'\mid k) = k'p_{k'}/\langle k\rangle$: a random edge reaches high-degree nodes in proportion to their degree (the friendship paradox).
- Degree-block theory is exactly the dynamics on the **annealed network** $\bar a_{ij} = k_j P(k_i\mid k_j)/(N p_{k_i})$, which is $k_ik_j/(N\langle k\rangle)$ when uncorrelated. It is exact when the wiring reshuffles much faster than the process, and an approximation on static (quenched) networks.
- For uncorrelated networks the degree-class "connectivity matrix" $C_{kk'} = kP(k'\mid k)$ has rank one, and its only non-zero eigenvalue is the **heterogeneity** $\kappa = \langle k^2\rangle/\langle k\rangle$. This is the number that sets epidemic thresholds, e.g. $\lambda_c = \langle k\rangle/\langle k^2\rangle$ for SIS.
- In scale-free networks with $2<\gamma\le 3$, $\langle k^2\rangle$ grows with the cutoff as $k_{\max}^{3-\gamma}$ and diverges as $N\to\infty$. Two cutoffs matter. The **natural cutoff** is $k_{\max} \sim N^{1/(\gamma-1)}$. The **structural cutoff**, $k_s \sim (\langle k\rangle N)^{1/2}$, is the largest degree an uncorrelated network without multi-edges can have.
:::

- **Source.** Course slides on degree-based models (PHYS 7335, Spring 2026). [](doi:10.1103/RevModPhys.87.925) (Pastor-Satorras, Castellano, Van Mieghem & Vespignani, *Rev. Mod. Phys.* 2015), §II and §IV. [](doi:10.1103/PhysRevE.66.047104) (Boguñá & Pastor-Satorras 2002), for correlated networks and detailed balance. [](doi:10.1140/epjb/e2004-00038-8) (Boguñá, Pastor-Satorras & Vespignani 2004), for cutoffs. Course textbook: Barrat, Barthélemy & Vespignani, [](doi:10.1017/CBO9780511791383) (2008).
- **Builds on.** Degree distributions and scale-free networks ([Barabási ch. 4 notes](../nets-5116/barabasi/04-scale-free-networks.md)); degree correlations and $k_{nn}(k)$ ([Barabási ch. 7 notes](../nets-5116/barabasi/07-degree-correlations.md)).
- **Notation.** Shared symbols as in [](#notation). Here $p_k$ is the degree distribution, written $P(k)$ in the review. $N_k = Np_k$ is the number of nodes of degree $k$. $E_{kk'}$ is the number of edge ends from class $k$ to class $k'$, defined in {prf:ref}`def-db-correlations`. $\kappa = \langle k^2\rangle/\langle k\rangle$. $\bar a_{ij}$ is the annealed adjacency. $C_{kk'}$ is the degree-class connectivity matrix.

(sec-db-setup)=
## Setup and definitions

:::{prf:definition} Degree classes and degree-block variables
:label: def-db-classes

The **degree class** $k$ is the set of $N_k = Np_k$ nodes with degree $k$. For a compartment $\alpha$ (S, I, R, …), the **degree-block variable** is the density

$$
\rho^\alpha_k(t) = \frac{N^\alpha_k(t)}{N_k},
\qquad \sum_\alpha \rho^\alpha_k = 1,
\qquad \rho^\alpha(t) = \sum_k p_k\, \rho^\alpha_k(t).
$$ (eq-db-blocks)

$\rho^\alpha_k$ is also the probability that a node of degree $k$ is in compartment $\alpha$. The **degree-based mean-field (DBMF)** approximation assumes that every node of degree $k$ is statistically equivalent.
:::

:::{prf:definition} Moments and heterogeneity
:label: def-db-moments

The moments are $\langle k^n\rangle = \sum_k k^n p_k$, with $\langle k\rangle = 2L/N$. The **heterogeneity parameter** is

$$
\kappa = \frac{\langle k^2\rangle}{\langle k\rangle} = \langle k\rangle + \frac{\sigma_k^2}{\langle k\rangle} \;\ge\; \langle k\rangle,
$$ (eq-db-kappa)

with equality only for regular graphs. A network is *homogeneous* if $\kappa \approx \langle k\rangle$, i.e. $p_k$ is concentrated around $\langle k\rangle$ as in Erdős–Rényi or Watts–Strogatz graphs. It is *heterogeneous* if $\kappa \gg \langle k\rangle$.
:::

:::{prf:definition} Two-point degree correlations
:label: def-db-correlations

Let $E_{kk'}$ count the edge ends that start at a degree-$k$ node and end at a degree-$k'$ node; an edge inside class $k$ counts twice. $E_{kk'}$ is symmetric, and $\sum_{k'} E_{kk'} = kN_k$. The **conditional degree distribution** is

$$
P(k'\mid k) = \frac{E_{kk'}}{k N_k},
\qquad \sum_{k'} P(k'\mid k) = 1.
$$ (eq-db-conditional)

The network is **uncorrelated** if $P(k'\mid k)$ does not depend on $k$. The average nearest-neighbour degree is $\bar k_{nn}(k) = \sum_{k'} k' P(k'\mid k)$. It increases with $k$ in assortative networks and decreases in disassortative ones.
:::

:::{prf:definition} Annealed vs quenched networks
:label: def-db-annealed

- A **quenched** (static) network keeps its adjacency matrix $A$ fixed while the process runs.
- An **annealed** network rewires so much faster than the process that the process only "sees" the probability that $i$ and $j$ are connected, given their degrees:

$$
\bar a_{ij} = \frac{k_j\, P(k_i \mid k_j)}{N\, p_{k_i}}
\;\xrightarrow{\text{uncorrelated}}\;
\frac{k_i k_j}{N\langle k\rangle}.
$$ (eq-db-annealed)

This preserves $p_k$ and $P(k'\mid k)$ and nothing else.
:::

(sec-db-core)=
## Core ideas

### From homogeneous to degree-based mixing (the course slides)

The slides start from **homogeneous mean field**: everyone is in the same class and meets the whole population at random. The discrete-time SIR update is

$$
S(t+1) = S(t) - \beta S(t)\frac{I(t)}{N},\quad
I(t+1) = I(t) + \beta S(t)\frac{I(t)}{N} - \mu I(t),\quad
R(t+1) = R(t) + \mu I(t).
$$ (eq-db-homog)

Copying these equations class by class, $S_k(t+1) = S_k - \beta S_k I/N$, is called out on the slide ("homogeneous interactions???"). The force of infection would then ignore $k$ entirely, which is exactly what a network should change.

The **degree-based** version counts contacts through edges instead:
1. A susceptible node of degree $k$ has $k$ edges.
2. Each edge reaches a degree-$k'$ node with probability $k'N_{k'}/(N\langle k\rangle) = k'p_{k'}/\langle k\rangle$, the uncorrelated $P(k'\mid k)$.
3. That node is infected with probability $I_{k'}/N_{k'}$.

So the probability that **one edge points to an infected node** is

$$
\Theta(t) = \sum_{k'} \frac{k' p_{k'}}{\langle k\rangle}\,\frac{I_{k'}(t)}{N_{k'}}
= \frac{1}{\langle k\rangle}\sum_{k'} k' p_{k'}\, \rho^I_{k'}(t),
$$ (eq-db-theta)

and in a small step $\delta t$ the per-node infection probability is $p_{S_k\to I_k} = \beta\,\delta t\, k\,\Theta$. (The slide writes the per-contact rate as $\lambda$; this page uses $\beta$ for it, as in the shared notation.) The stochastic (chain-binomial) form used in the slides draws

$$
\begin{aligned}
S_{k,t+1} &= S_{k,t} - \mathrm{Bin}(S_{k,t},\, p_{S_k\to I_k}),\\
I_{k,t+1} &= I_{k,t} + \mathrm{Bin}(S_{k,t},\, p_{S_k\to I_k}) - \mathrm{Bin}(I_{k,t},\, \mu\,\delta t),\\
R_{k,t+1} &= R_{k,t} + \mathrm{Bin}(I_{k,t},\, \mu\,\delta t),
\end{aligned}
$$ (eq-db-binomial)

with $S_k+I_k+R_k = N_k$ conserved in each class. (The two binomials in the $I$ line are the same draws as in the $S$ and $R$ lines.) Replacing each binomial by its mean gives the deterministic degree-block equations.

### Deterministic vs stochastic

| | Deterministic degree-block ODEs/maps | Stochastic (chain binomial, Gillespie) |
|---|---|---|
| Variables | expected densities $\rho^\alpha_k$ | integer counts $N^\alpha_k$ |
| Valid when | every relevant class is large ($N_k \gg 1$) and far from extinction | always (for the model) |
| Threshold meaning | $R_0>1$ is necessary **and** sufficient for growth | $R_0>1$ is only **necessary**; early extinction is possible |
| What it misses | fluctuations; *dynamical* correlations between neighbours (e.g. an infected node's neighbours are more likely to be infected) | nothing at model level, but needs many runs |

The RMP review stresses the middle row: for stochastic systems with $R_0>1$, early fluctuations can still end the epidemic. That probability is computed on the [SIR–percolation page](./07-sir-percolation.md).

Classes with large $k$ are the *small* classes in a heavy-tailed network ($N_k \propto k^{-\gamma}$). So the deterministic approximation is worst exactly for the hubs that drive the dynamics (*my comment*).

### The annealed approximation and when it holds

The DBMF equations for any process can be obtained in two equivalent ways. One is to write rate equations directly for the $\rho^\alpha_k$ using the law of mass action. The other is to take individual-based (quenched) mean-field equations in $A$, substitute $a_{ij} \to \bar a_{ij}$ from {eq}`eq-db-annealed`, and average within degree classes (RMP §IV.C). DBMF therefore *equals* IBMF on the annealed graph. The question of validity becomes a question of time scales:

- **Annealed limit** (network evolves much faster than the process). DBMF is the correct mean-field theory. Examples: rapidly changing contacts, and the mixing implied by many agent-based mobility models.
- **Quenched limit** (network static on the time scale of the process). DBMF is an approximation. The relevant object is $A$ itself and its leading eigenvalue $\Lambda_{\max}$; see [quenched mean field](./06-quenched-mean-field.md).
- **Comparable time scales**: temporal or adaptive networks, which neither limit describes.

The slides summarise the payoff. Heterogeneity suppresses the threshold: on random annealed networks $R_0 \to R_0\,\langle k^2\rangle/\langle k\rangle^2$ and the threshold vanishes. On quenched networks the threshold goes as $1/\Lambda_{\max}$. Assortativity and disassortativity shift numbers, but do not change the qualitative threshold behaviour.

### Heavy tails and cutoffs

For $p_k \simeq c\,k^{-\gamma}$ with $k \ge m$:
- $\langle k\rangle$ is finite for $\gamma>2$.
- $\langle k^2\rangle$ is finite only for $\gamma>3$.

For $2<\gamma<3$, $\langle k^2\rangle$ is dominated by the largest degrees, so every finite network's heterogeneity is set by its cutoff:

$$
\langle k^2\rangle \simeq c\int_m^{k_{\max}} k^{2-\gamma}\,dk \;\sim\; k_{\max}^{\,3-\gamma}
\qquad (2<\gamma<3),
\qquad \langle k^2\rangle \sim \ln k_{\max}\quad(\gamma=3).
$$ (eq-db-k2scaling)

Many empirical networks have $2<\gamma<3$ (RMP §II.D), which is why this regime matters. Two cutoffs set $k_{\max}$; they are derived in {prf:ref}`prop-db-cutoffs`.

(sec-db-results)=
## Key results

:::{prf:proposition} Uncorrelated conditional distribution
:label: prop-db-uncorrelated

If $P(k'\mid k)$ does not depend on $k$, then

$$
P(k'\mid k) = \frac{k' p_{k'}}{\langle k\rangle},
\qquad \bar k_{nn}(k) = \frac{\langle k^2\rangle}{\langle k\rangle} = \kappa.
$$ (eq-db-uncorr)
:::

:::{dropdown} Derivation
If the far end of an edge does not depend on the near end, it is simply a uniformly random **edge end**. Class $k'$ owns $k'N_{k'}$ of the $\sum_{k''} k''N_{k''} = N\langle k\rangle = 2L$ edge ends, so the probability is $k'N_{k'}/(N\langle k\rangle) = k'p_{k'}/\langle k\rangle$. Then $\bar k_{nn} = \sum_{k'} k'^2 p_{k'}/\langle k\rangle$.

This is the **friendship paradox** in its mean-field form: the expected degree of a neighbour, $\kappa$, exceeds the expected degree of a node, $\langle k\rangle$, by $\sigma_k^2/\langle k\rangle$ ({eq}`eq-db-kappa`).

The *excess* degree of that neighbour, the number of edges other than the one used to arrive, has mean $\kappa - 1 = G_1'(1)$. This is the branching factor of percolation and SIR (see the [SIR–percolation page](./07-sir-percolation.md)).
:::

:::{prf:proposition} Degree detailed balance
:label: prop-db-detailed-balance

For every undirected network,

$$
k\,p_k\,P(k'\mid k) \;=\; k'\,p_{k'}\,P(k\mid k') \;=\; \frac{E_{kk'}}{N}.
$$ (eq-db-detailed-balance)
:::

:::{dropdown} Derivation
From {eq}`eq-db-conditional`, $k\,p_k\,P(k'\mid k) = k\,\frac{N_k}{N}\,\frac{E_{kk'}}{kN_k} = \frac{E_{kk'}}{N}$. $E_{kk'}$ is symmetric because every edge between classes $k$ and $k'$ contributes one end to each, so the right-hand side is symmetric in $k \leftrightarrow k'$.

Boguñá & Pastor-Satorras (2002) write the common value as $\langle k\rangle P(k,k')$, where $P(k,k')$ is the joint distribution of degrees at the two ends of an edge. Detailed balance is the reason $p_k$ and $P(k'\mid k)$ cannot be chosen independently: any correlated model must satisfy {eq}`eq-db-detailed-balance`. The uncorrelated form {eq}`eq-db-uncorr` satisfies it trivially, since both sides equal $kk'p_kp_{k'}/\langle k\rangle$.
:::

:::{prf:proposition} The annealed graph preserves degrees; degree-block dynamics are linear in $C_{kk'}$
:label: prop-db-annealed-C

1. The annealed adjacency {eq}`eq-db-annealed` has expected row sums $\sum_j \bar a_{ij} = k_i$.
2. Linearising any DBMF contagion model around the disease-free state gives a growth operator proportional to the **connectivity matrix**

$$
C_{kk'} = k\,P(k'\mid k).
$$ (eq-db-C)

$C_{kk'}$ is the mean number of edges from a degree-$k$ node to degree-$k'$ nodes.

3. For uncorrelated networks $C$ has rank one, $C_{kk'} = k \cdot \frac{k'p_{k'}}{\langle k\rangle}$, with right eigenvector $k$ and unique non-zero eigenvalue

$$
\Lambda_M = \frac{\langle k^2\rangle}{\langle k\rangle} = \kappa .
$$ (eq-db-LambdaM)
:::

:::{dropdown} Derivation
1. Sum over the $N p_{k'}$ nodes $j$ of each degree $k'$:
   $$\textstyle\sum_j \bar a_{ij} = \sum_{k'} Np_{k'}\,\frac{k'P(k_i\mid k')}{Np_{k_i}} = \sum_{k'} k_i P(k'\mid k_i) = k_i.$$
   The middle step uses detailed balance {eq}`eq-db-detailed-balance`. (This check is mine.)

2. For SIS, the RMP review (its Eqs. 20–22, following Boguñá & Pastor-Satorras 2002) writes
   $$\dot\rho_k = -\rho_k + \lambda k(1-\rho_k)\sum_{k'}P(k'\mid k)\rho_{k'}$$
   with time in units of $\mu^{-1}$. Dropping the quadratic term gives the Jacobian $J_{kk'} = -\delta_{kk'} + \lambda C_{kk'}$.

3. If $C = u v^\top$ with $u_k = k$ and $v_{k'} = k'p_{k'}/\langle k\rangle$, then $Cu = u\,(v^\top u)$, where $v^\top u = \sum_{k'} k'^2p_{k'}/\langle k\rangle = \kappa$. All other eigenvalues are zero.

So the healthy state is unstable once $\lambda\kappa > 1$, i.e. $\lambda_c = \langle k\rangle/\langle k^2\rangle$. The full derivation and the SIR variant are on the [heterogeneous mean-field page](./05-heterogeneous-mean-field.md). For a regular graph $\kappa = \langle k\rangle$, which recovers the homogeneous result $\lambda_c = 1/\langle k\rangle$, i.e. $R_0 = \beta\langle k\rangle/\mu$ (RMP Eq. 11).
:::

:::{prf:proposition} Natural and structural cutoffs
:label: prop-db-cutoffs

For $p_k \propto k^{-\gamma}$ with minimum degree $m$:

**(i) Natural cutoff.** This is the degree above which we expect at most one node out of $N$ independent draws:

$$
N\int_{k_{\max}}^\infty p(k)\,dk \sim 1 \;\Rightarrow\; k_{\max} \sim m\,N^{1/(\gamma-1)}.
$$ (eq-db-natural)

**(ii) Structural cutoff.** In an uncorrelated network without multiple edges, the number of edges between two classes cannot exceed $N_kN_{k'}$. This forces

$$
k_s \sim (\langle k\rangle N)^{1/2}.
$$ (eq-db-structural)

For $\gamma<3$, $k_{\max} \gg k_s$. Uncorrelated scale-free graphs in this range therefore either have multi-edges, or develop disassortative correlations among the hubs, or must be cut off at $k_s$. The uncorrelated configuration model imposes $k_{\max} \sim N^{1/2}$ for exactly this reason.
:::

:::{dropdown} Derivation
1. With the continuous form $p(k) = (\gamma-1)m^{\gamma-1}k^{-\gamma}$, the tail is $\int_{k_{\max}}^\infty p = (m/k_{\max})^{\gamma-1}$. Setting $N(m/k_{\max})^{\gamma-1}=1$ gives {eq}`eq-db-natural`. The prefactor $m$ is my explicit calculation; the paper states only the scaling with $N$. Boguñá et al. (2004) note that the extreme-value definition gives the same $N$-dependence.

2. Following Boguñá et al. (2004), let $r_{kk'} = E_{kk'}/m_{kk'}$, the ratio of actual to maximal edges between classes, where $m_{kk'} = \min\{kN_k, k'N_{k'}, N_kN_{k'}\}$. For uncorrelated networks $E_{kk'} = kk'N_kN_{k'}/(N\langle k\rangle)$, so in the hub region $r_{kk'} = kk'/(\langle k\rangle N)$. The physical constraint $r_{kk'} \le 1$, evaluated on the diagonal $k = k' = k_s$, gives $k_s^2 = \langle k\rangle N$.

    At $\gamma = 3$ the two cutoffs coincide (as for the BA model). For $\gamma>3$ the natural cutoff is the binding one.
:::

## Worked example

### A six-node graph

The edges are $0\text{–}1, 0\text{–}2, 0\text{–}3, 0\text{–}4, 1\text{–}2, 4\text{–}5$. Node 0 is a hub; there is a triangle $0,1,2$ and a pendant chain $0\text{–}4\text{–}5$. I computed all quantities below with exact fractions.

- **Degrees** $(4,2,2,1,2,1)$, so $L=6$ and $p_1 = 1/3$, $p_2 = 1/2$, $p_4 = 1/6$.
- **Moments:** $\langle k\rangle = 2$, $\langle k^2\rangle = 5$, so $\kappa = 5/2$. A random neighbour has degree $2.5$ on average, against $2$ for a random node.

| $P(k'\mid k)$ | $k'=1$ | $k'=2$ | $k'=4$ | $\bar k_{nn}(k)$ |
|---|---|---|---|---|
| $k=1$ | 0 | 1/2 | 1/2 | 3 |
| $k=2$ | 1/6 | 1/3 | 1/2 | 17/6 |
| $k=4$ | 1/4 | 3/4 | 0 | 7/4 |
| uncorrelated $k'p_{k'}/\langle k\rangle$ | 1/6 | 1/2 | 1/3 | 5/2 |

- **Detailed balance** holds entry by entry. For example, $k=2, k'=4$: $2\cdot\tfrac12\cdot\tfrac12 = \tfrac12$ and $4\cdot\tfrac16\cdot\tfrac34 = \tfrac12$. Both equal $E_{24}/N = 3/6$.
- **Correlations:** $\bar k_{nn}(k)$ falls from 3 to 7/4, so this little graph is **disassortative**. The hub's neighbours have low degree.
- **Connectivity matrix:** the correlated $C_{kk'} = kP(k'\mid k)$ has leading eigenvalue $\Lambda_M = 2.349$, slightly below the uncorrelated prediction $\kappa = 2.5$. The leading eigenvalue of the actual (quenched) adjacency matrix is $\Lambda_{\max}(A) = 2.380$. Three estimates of the same "branching strength" therefore disagree in the second digit.
- **Annealed adjacency:** $\bar a_{ij} = k_ik_j/12$. Its rows sum to the degrees, as {prf:ref}`prop-db-annealed-C` requires. But the hub's self-entry is $\bar a_{00} = 16/12 > 1$, which is not a probability. That happens because $k_0 = 4$ exceeds the structural cutoff $k_s = \sqrt{\langle k\rangle N} = \sqrt{12} \approx 3.46$, a miniature of {prf:ref}`prop-db-cutoffs`.

### How heterogeneity grows with the cutoff

The table uses discrete $p_k \propto k^{-\gamma}$ on $k = 3, \dots, k_{\max}$, with exact sums over the discrete distribution.

| $N$ | $\gamma=2.5$: $k_{\max} = 3N^{2/3}$ | $\kappa$ | $1/\kappa$ | with $k_s = \sqrt{\langle k\rangle N}$: $\kappa$ | $\gamma=3.5$: $\kappa$ |
|---|---|---|---|---|---|
| $10^3$ | 300 | 27.5 | 0.036 | 14.5 | 5.95 |
| $10^4$ | 1392 | 59.3 | 0.017 | 26.1 | 6.55 |
| $10^5$ | 6463 | 127.7 | 0.0078 | 46.7 | 6.95 |
| $10^6$ | 30000 | 275.2 | 0.0036 | 83.4 | 7.20 |
| $10^7$ | 139248 | 592.9 | 0.0017 | 148.4 | 7.36 |

- **$\gamma = 2.5$, natural cutoff:** each decade of $N$ multiplies $k_{\max}$ by $10^{2/3} \approx 4.64$, and $\kappa$ by $4.64^{1/2} \approx 2.15$, as {eq}`eq-db-k2scaling` predicts.
- **$\gamma = 2.5$, structural cutoff:** $\kappa$ grows as $N^{1/4}$ instead (×1.78 per decade).
- **$\gamma = 3.5$:** $\kappa$ saturates near $7.5$.

Read through {prf:ref}`prop-db-annealed-C`, the $1/\kappa$ column is the SIS threshold in DBMF. It drifts to zero with system size when $\gamma<3$ and stays finite when $\gamma>3$.

## Assumptions and limitations

- **Statistical equivalence within a class.** DBMF discards everything about a node except its degree, including clustering, communities, geography and the identity of its neighbours. It is exact only on annealed networks with the prescribed $p_k$ and $P(k'\mid k)$, and is a mean-field closure on static ones.
- **No dynamical correlations.** The mass-action closure factorises joint states of neighbours. In SIR, for example, a susceptible node that has an infected neighbour knows that neighbour was not infected by it, which DBMF ignores. Pair approximations and message passing address this; see the [quenched mean-field page](./06-quenched-mean-field.md).
- **Two-point correlations only.** Even the correlated version keeps only $P(k'\mid k)$. Boguñá & Pastor-Satorras call such networks *Markovian*: higher-order correlations are functions of $p_k$ and $P(k'\mid k)$.
- **Large classes.** Deterministic degree-block equations need $N_k \gg 1$. That fails precisely in the tail of a heavy-tailed $p_k$ (*my comment*).
- **Cutoffs are model-dependent.** Whether the relevant $k_{\max}$ is $N^{1/(\gamma-1)}$, $N^{1/2}$ or something set by biology or cost changes every finite-size number in the table. Statements of the form "the threshold vanishes" are statements about $N \to \infty$.

## Connections

- **NETS 5116.**
  - Heavy tails, $\gamma$ regimes and the natural cutoff are covered in [Barabási ch. 4](../nets-5116/barabasi/04-scale-free-networks.md).
  - $\bar k_{nn}(k)$, structural cutoffs and structural disassortativity are covered in [Barabási ch. 7](../nets-5116/barabasi/07-degree-correlations.md).
  - The friendship-paradox factor $\kappa - 1 = G_1'(1)$ is the Molloy–Reed branching number, also in Barabási ch. 8 on robustness.
- **NETS 6116.** $p_k$ alone is the "1k" level and $P(k'\mid k)$ (equivalently $P(k,k')$) is the "2k" level of the dk-series. The annealed graph is the soft-configuration-model-like ensemble with expected degrees $k_i$ (*my observation*).
- **PHYS 7335.** $\kappa$ reappears as:
  - the stationary-state factor for walkers (see [Random walks](./02-random-walks.md));
  - $R_0$ on networks (see [Thresholds and NGMs](./04-thresholds-and-ngm.md));
  - $\lambda_c$ in [heterogeneous mean field](./05-heterogeneous-mean-field.md);
  - the percolation threshold in [SIR–percolation](./07-sir-percolation.md).

  The annealed vs quenched split organises [quenched mean field](./06-quenched-mean-field.md).
- **NETS 7332.** The annealed $\bar a_{ij} = k_ik_j/(2L)$ is the null model behind modularity, and the rank-one "degree-only" signal that spectral methods and GCN normalisation ([Message-passing GNNs](../nets-7332/basics/05-message-passing-gnns.md)) partly divide out (*my comment*).

## Self-test

:::{dropdown} Q1. Derive $P(k'\mid k)$ for an uncorrelated network and use it to explain the friendship paradox.
If the far end of an edge is independent of the near end, it is a uniform random edge end. Class $k'$ holds $k'N_{k'}$ of the $N\langle k\rangle$ ends, so $P(k'\mid k) = k'p_{k'}/\langle k\rangle$.

The mean degree of a neighbour is then $\langle k^2\rangle/\langle k\rangle = \langle k\rangle + \sigma_k^2/\langle k\rangle \ge \langle k\rangle$: your friends have more friends than you, on average.
:::

:::{dropdown} Q2. State degree detailed balance and say where it comes from.
$k\,p_k\,P(k'\mid k) = k'\,p_{k'}\,P(k\mid k')$. Both sides equal $E_{kk'}/N$, where $E_{kk'}$, the number of edge ends between classes $k$ and $k'$, is symmetric because each edge has one end in each class.
:::

:::{dropdown} Q3. What is the annealed adjacency matrix, and when is degree-based mean field exact?
$\bar a_{ij} = k_jP(k_i\mid k_j)/(Np_{k_i})$, which is $k_ik_j/(N\langle k\rangle)$ when uncorrelated. It is the probability that $i$ and $j$ are linked given their degrees.

DBMF is exactly the mean-field theory on this matrix, so it is exact in the limit where the network rewires much faster than the dynamics (preserving $p_k$ and $P(k'\mid k)$). On static networks it is an approximation.
:::

:::{dropdown} Q4. Why is $\kappa = \langle k^2\rangle/\langle k\rangle$ the relevant number for thresholds?
Linearising degree-block dynamics gives the operator $C_{kk'} = kP(k'\mid k)$. For uncorrelated networks $C = k\,(k'p_{k'}/\langle k\rangle)^\top$ has rank one, and its only non-zero eigenvalue is $\sum_{k'}k'^2p_{k'}/\langle k\rangle = \kappa$. Instability requires $\lambda\kappa > 1$.
:::

:::{dropdown} Q5. For $p_k \propto k^{-\gamma}$ with $2<\gamma<3$, how does $\langle k^2\rangle$ scale with $N$ under the natural cutoff, and under the structural cutoff?
$\langle k^2\rangle \sim k_{\max}^{3-\gamma}$.
- **Natural cutoff:** $k_{\max} \sim N^{1/(\gamma-1)}$, giving $N^{(3-\gamma)/(\gamma-1)}$. For $\gamma=2.5$ that is $N^{1/3}$ for $\langle k^2\rangle$, and also for $\kappa$, since $\langle k\rangle$ is finite.
- **Structural cutoff:** $k_s \sim N^{1/2}$, giving $N^{(3-\gamma)/2}$, i.e. $N^{1/4}$ for $\gamma=2.5$.

Either way $\langle k^2\rangle$ diverges, and so does $\kappa$.
:::

:::{dropdown} Q6. Where does the structural cutoff $k_s \sim \sqrt{\langle k\rangle N}$ come from?
Without multi-edges, at most $N_kN_{k'}$ edges can join classes $k$ and $k'$. An uncorrelated network needs $kk'N_kN_{k'}/(\langle k\rangle N)$ of them. The ratio $kk'/(\langle k\rangle N)$ must stay $\le 1$, which fails for $k = k' > \sqrt{\langle k\rangle N}$.

For $\gamma<3$ the natural cutoff exceeds $k_s$. Such graphs must therefore be cut off at $k_s$, or carry multi-edges, or become disassortative among the hubs.
:::

:::{dropdown} Q7. In the chain-binomial degree-block model, what is the per-step infection probability of a susceptible node of degree $k$, and what does $R_0>1$ guarantee?
$p_{S_k \to I_k} = \beta\,\delta t\,k\,\Theta$, with $\Theta = \sum_{k'}k'p_{k'}\rho^I_{k'}/\langle k\rangle$ the probability that an edge points to an infected node.

$R_0>1$ guarantees growth only in the deterministic limit. Stochastically it is necessary but not sufficient, because the outbreak can still go extinct early.
:::

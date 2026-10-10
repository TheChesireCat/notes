---
title: Quenched Mean-Field Theory and Message Passing for Epidemics
short_title: Quenched mean field
subject: PHYS 7335 · Topic
description: Epidemic thresholds on a fixed network. Individual-based mean field gives 1/Λ_max for SIS, eigenvector localisation decides what that transition means, and message passing gives the SIR threshold through the non-backtracking matrix.
tags: [epidemics, sis, sir, quenched-mean-field, spectral, localisation, non-backtracking, message-passing]
---

:::{tip} TL;DR
- **Quenched mean field (QMF)** keeps the *actual* adjacency matrix and closes the exact SIS equations by assuming that neighbouring nodes are independent: $\dot\rho_i = -\rho_i + \lambda(1-\rho_i)\sum_j A_{ij}\rho_j$. Linear stability gives $\lambda_c^{\mathrm{QMF}} = 1/\Lambda_{\max}$. The same $1/\Lambda_{\max}$ is also a rigorous **lower bound** on the true SIS threshold.
- On power-law networks $\Lambda_{\max} \simeq \max\big(\sqrt{k_{\max}},\, \langle k^2\rangle/\langle k\rangle\big)$. So $\lambda_c^{\mathrm{QMF}} \simeq \langle k\rangle/\langle k^2\rangle$ for $\gamma < 5/2$ and $\simeq 1/\sqrt{k_{\max}}$ for $\gamma > 5/2$. The threshold **vanishes for every $\gamma$** as long as $k_{\max}$ grows with $N$, unlike heterogeneous mean field, which predicts a finite threshold for $\gamma > 3$.
- The mechanism is the **hub**. A star with $k_{\max}$ leaves sustains SIS activity on its own once $\lambda > 1/\sqrt{k_{\max}}$. Whether the transition at $1/\Lambda_{\max}$ is a true endemic one depends on whether the principal eigenvector is **delocalised**, which Goltsev et al. find for $\gamma \le 5/2$. For $\gamma > 5/2$ it is **localised** (inverse participation ratio $=O(1)$) and the transition is only *sub-endemic*.
- **SIR is different.** There is no reinfection, so a hub cannot act as a reservoir. Individual-based mean field for SIR wrongly predicts $1/\Lambda_{\max}$. **Message passing** is exact on locally tree-like graphs and gives the transmissibility threshold $T_c = 1/\Lambda_{\max}(B)$, with $B$ the **non-backtracking** matrix. For any graph, $T_c \ge 1/\Lambda_{\max}(B) \ge 1/\Lambda_{\max}(A)$.
- On large uncorrelated random graphs $\Lambda_{\max}(B) \approx \langle k^2\rangle/\langle k\rangle - 1$, which recovers the percolation and HMF value $T_c = \langle k\rangle/(\langle k^2\rangle - \langle k\rangle)$. That value is finite for $\gamma > 3$ and vanishes for $\gamma < 3$.
:::

- **Source.** Pastor-Satorras, Castellano, Van Mieghem & Vespignani, *Epidemic processes in complex networks*, [](doi:10.1103/RevModPhys.87.925), §§IV.A, V.A.2–V.A.5, V.B.2–V.B.4 (the main reference; "the review" below). Primary papers:
  - Castellano & Pastor-Satorras, [](doi:10.1103/PhysRevLett.105.218701)
  - Goltsev, Dorogovtsev, Oliveira & Mendes, [](doi:10.1103/PhysRevLett.109.128702)
  - Karrer & Newman, [](doi:10.1103/PhysRevE.82.016101)
  - Karrer, Newman & Zdeborová, [](doi:10.1103/PhysRevLett.113.208702)
  - the spectral estimate of Chung, Lu & Vu, [](doi:10.1073/pnas.0937490100)
- **Builds on.** The degree-based treatment in [heterogeneous mean field](./05-heterogeneous-mean-field.md), and Perron–Frobenius and eigenvector centrality from [link analysis](../nets-7332/basics/02-link-analysis.md) and [Newman ch. 7](../nets-5116/newman/07-measures-and-metrics.md).
- **Notation.** Shared symbols as in [](#notation), with time measured in units of $1/\mu$, so that $\lambda = \beta/\mu$. Page-specific symbols:
  - $X_i(t) \in \{0,1\}$: the infection indicator of node $i$, with $\rho_i = \mathbb{E}[X_i]$
  - $\Lambda_1 \equiv \Lambda_{\max}(A)$, with unit principal eigenvector $x$ ($\sum_i x_i^2 = 1$)
  - $B$: the non-backtracking matrix
  - $T$: SIR transmissibility
  - $H^{i\leftarrow j}$: the SIR messages

(sec-qmf-definitions)=
## Setup and definitions

:::{prf:definition} Quenched vs annealed network
:label: def-qmf-quenched

A **quenched** network has a fixed adjacency matrix $A$, and the epidemic runs on that one graph. An **annealed** network is rewired so fast compared with the epidemic that only the ensemble average $\bar a_{ij}$ matters. For uncorrelated networks this average is $\bar a_{ij} = k_i k_j/(N\langle k\rangle)$. Heterogeneous (degree-based) mean field is exact on annealed networks and an approximation on quenched ones.
:::

:::{prf:definition} Exact SIS equations
:label: def-qmf-exact

For SIS with infection rate $\beta$ per edge and recovery rate $\mu$, the infection probabilities obey exactly (the review, eq. 30)

$$
\frac{d\,\mathbb{E}[X_i]}{dt} = \mathbb{E}\Big[-\mu X_i + (1 - X_i)\,\beta \sum_j A_{ij} X_j\Big].
$$ (eq-qmf-exact)

The equation for $\rho_i = \mathbb{E}[X_i]$ involves the pair terms $\mathbb{E}[X_i X_j]$. Writing equations for those brings in triples, and so on, up to $2^N - 1$ equations.
:::

:::{prf:definition} Individual-based (quenched) mean field
:label: def-qmf-ibmf

The **individual-based mean-field** approximation (IBMF, also called QMF or NIMFA, the *N-intertwined* mean-field approximation) closes the hierarchy at the first level, $\mathbb{E}[X_i X_j] = \rho_i \rho_j$:

$$
\frac{d\rho_i}{dt} = -\rho_i + \lambda\,(1 - \rho_i) \sum_{j} A_{ij}\,\rho_j .
$$ (eq-qmf-nimfa)

All of the network's structure is kept; only *dynamical* correlations between neighbours are dropped.
:::

:::{prf:definition} Inverse participation ratio
:label: def-qmf-ipr

For a unit eigenvector $x$, $\mathrm{IPR}(x) = \sum_i x_i^4$. A vector is **delocalised** if $\mathrm{IPR} \to 0$ as $N \to \infty$; a uniform vector has $\mathrm{IPR} = 1/N$. It is **localised** if $\mathrm{IPR} = O(1)$, meaning its weight sits on a finite number of nodes.
:::

:::{prf:definition} Non-backtracking (Hashimoto) matrix
:label: def-qmf-nb

Replace each undirected edge by its two directed versions, giving $2L$ directed edges. Index them $i \leftarrow j$. The non-backtracking matrix is the $2L \times 2L$ matrix

$$
B_{i\leftarrow j,\; k\leftarrow l} = \delta_{jk}\,(1 - \delta_{il}).
$$ (eq-qmf-B)

Edge $k \leftarrow l$ feeds edge $i \leftarrow j$ if it ends where $i \leftarrow j$ starts ($k = j$) and does not come straight back from $i$ ($l \ne i$). Entries of $B^n$ count non-backtracking walks.
:::

(sec-qmf-core)=
## Core ideas

### QMF and HMF are the same equation on different matrices

Substituting the annealed matrix $\bar a_{ij}$ into {eq}`eq-qmf-nimfa` and averaging over degree classes returns the degree-based (HMF) equations exactly (the review, §V.A.2). The uncorrelated $\bar a_{ij} = k_ik_j/(N\langle k\rangle)$ has rank one, and its only non-zero eigenvalue is $\langle k^2\rangle/\langle k\rangle$. So $1/\Lambda_{\max}$ of the annealed matrix *is* the HMF threshold $\langle k\rangle/\langle k^2\rangle$. The two theories therefore disagree exactly when the quenched spectrum differs from the annealed one, that is, when the largest eigenvalue of $A$ is set by something other than $\langle k^2\rangle/\langle k\rangle$. Castellano & Pastor-Satorras make this point: what fails in HMF is the loss of the spectrum, not the neglect of dynamical correlations.

### The spectrum of a heterogeneous network

For random graphs with given expected degrees, Chung, Lu & Vu find that the largest eigenvalue is, up to constants of order one, $\sqrt{k_{\max}}$ when $\sqrt{k_{\max}} > (\langle k^2\rangle/\langle k\rangle)\ln^2 N$ and $\langle k^2\rangle/\langle k\rangle$ when $\langle k^2\rangle/\langle k\rangle > \sqrt{k_{\max}}\ln N$. That is the form quoted by Castellano & Pastor-Satorras, and in short $\Lambda_1 \simeq \max(\sqrt{k_{\max}}, \langle k^2\rangle/\langle k\rangle)$. For $P(k) \sim k^{-\gamma}$ with $2 < \gamma < 3$, $\langle k^2\rangle/\langle k\rangle \sim k_{\max}^{3-\gamma}$. This beats $\sqrt{k_{\max}}$ exactly when $3 - \gamma > 1/2$, which gives the threshold scaling (the review, eq. 35)

$$
\lambda_c^{\mathrm{QMF}} \simeq
\begin{cases}
\langle k\rangle/\langle k^2\rangle, & 2 < \gamma < 5/2,\\[2pt]
1/\sqrt{k_{\max}}, & \gamma > 5/2 .
\end{cases}
$$ (eq-qmf-scaling)

Since $k_{\max}$ grows with $N$ in essentially every random, non-regular network, $\lambda_c^{\mathrm{QMF}} \to 0$ for **every** $\gamma$, Erdős–Rényi graphs included (logarithmically slowly). For $\gamma > 3$ this contradicts the finite HMF threshold.

| | HMF (annealed) | QMF / IBMF (quenched) | Rigorous / numerical status |
|---|---|---|---|
| SIS, $2<\gamma<5/2$ | $\langle k\rangle/\langle k^2\rangle \to 0$ | same, since $\Lambda_1 \approx \langle k^2\rangle/\langle k\rangle$ | QMF and pair-QMF are close to exact in simulations |
| SIS, $5/2<\gamma<3$ | $\langle k\rangle/\langle k^2\rangle \to 0$ | $1/\sqrt{k_{\max}}$, vanishing faster | QMF gives the right scaling with $N$ |
| SIS, $\gamma>3$ | **finite** | $1/\sqrt{k_{\max}} \to 0$ | threshold $\to 0$, but not by the QMF mechanism (see below) |
| SIR, $\gamma<3$ | $\to 0$ | IBMF: $1/\Lambda_1$ | message passing / percolation: $\to 0$ |
| SIR, $\gamma>3$ | **finite** | IBMF: $1/\Lambda_1 \to 0$, which is **wrong** | finite, matching HMF |

The status column summarises the review's §V.A.5 and Castellano & Pastor-Satorras (2010).

### The hub as a self-sustained source

Why $1/\sqrt{k_{\max}}$? Take a star: a hub joined to $k_{\max}$ leaves. Then $\Lambda_1 = \sqrt{k_{\max}}$, and QMF on the star alone has an active steady state for $\lambda > 1/\sqrt{k_{\max}}$ ({prf:ref}`prop-qmf-star`). Infection bounces between the hub and its leaves: the hub reinfects leaves, and any leaf reinfects the hub. In a real network the leaves have other neighbours, so this nucleus of activity seeds the rest of the graph. Castellano & Pastor-Satorras show this numerically. Below the HMF threshold, the number of active nodes in surviving runs tracks that of an isolated star until $k_{\max} > 1/\lambda^2$, and after that it grows like $N$.

### Localisation: when does $1/\Lambda_1$ mean "endemic"?

Just above threshold, QMF gives a prevalence controlled by the principal eigenvector ({prf:ref}`prop-qmf-prevalence`):

$$
\rho \simeq \alpha_1 (\lambda\Lambda_1 - 1), \qquad \alpha_1 = \frac{\sum_i x_i}{N \sum_i x_i^3}.
$$ (eq-qmf-alpha)

If $x$ is delocalised, $x_i \sim N^{-1/2}$ and $\alpha_1 = O(1)$, so a finite fraction is infected and the transition is genuinely endemic. If $x$ is localised on a few nodes, $\alpha_1 = O(1/N)$. Activity is then confined to a finite neighbourhood of the hub, and the transition at $1/\Lambda_1$ is not to an endemic state. Goltsev et al. argue that for power-law networks the principal eigenvector is **delocalised for $\gamma \le 5/2$ and localised for $\gamma > 5/2$**. The review relates the resulting *sub-endemic* state above $1/\Lambda_1$ to a Griffiths phase (Lee et al. 2013).

This does **not** restore a finite threshold. The review summarises the rigorous results as follows:
- Chatterjee & Durrett [](doi:10.1214/09-AOP471) proved that the contact process (SIS) on power-law random graphs has critical value zero.
- Mountford et al. ([arXiv:1203.2972](https://doi.org/10.48550/arXiv.1203.2972)) showed that for any $\lambda > 0$ the time to absorption grows exponentially in $N$, so activity is endemic for every $\lambda > 0$.

For $\gamma > 3$ the physical mechanism is long-range mutual **reactivation of hubs** through chains of intermediate nodes. Boguñá, Castellano & Pastor-Satorras [](doi:10.1103/PhysRevLett.111.068701) model it with a coarse-grained, degree-based theory. In short, QMF gets the *vanishing* right but the *nature* of the transition wrong for $\gamma > 5/2$.

### SIR: no steady state, no reservoir

Applying the same independence closure to SIR again yields $\lambda_c = 1/\Lambda_1$. The review calls this "even qualitatively not correct". It predicts a vanishing threshold for $\gamma > 3$, contradicting exact results and simulations. Sharkey (2011) traces the failure to unphysical terms in which a node is treated as susceptible and infected at once. The physical reason is that an SIR hub can be infected **only once**, so it cannot be the self-sustained source of the SIS story. In Castellano & Pastor-Satorras's simulations on $\gamma = 4.5$ networks the SIR threshold stays finite as $N$ grows, close to the HMF value. Their stated conjecture: on quenched scale-rich networks, models with a steady state (SIS-like) have a vanishing threshold, and models without one (SIR-like) have a finite threshold.

### Message passing for SIR

Karrer & Newman write the SIR dynamics in terms of messages. $H^{i\leftarrow j}(t)$ is the probability that $j$ has *not* transmitted to $i$ by time $t$, computed on the network with $i$ removed (the cavity). Let $z$ be the probability that a node is initially susceptible, and $f(\tau)\,d\tau$ the probability that an infected node transmits along a given edge between $\tau$ and $\tau + d\tau$ after its infection, given that it has not yet recovered. Then

$$
H^{i\leftarrow j}(t) = 1 - \int_0^t f(\tau)\Big[1 - z\!\!\prod_{l \in \mathcal{N}(j)\setminus i}\!\! H^{j\leftarrow l}(t-\tau)\Big] d\tau,
\qquad
\Pr[S_i(t)] = z \prod_{j\in\mathcal{N}(i)} H^{i\leftarrow j}(t).
$$ (eq-qmf-mp)

These equations hold for **arbitrary**, non-exponential infection and recovery time distributions. They are exact on trees and in the large-$N$ limit of locally tree-like graphs. On graphs with loops they give a rigorous bound on outbreak size. The total transmissibility is $T = \int_0^\infty f(\tau)\,d\tau$.

At late times the messages satisfy $H^{i\leftarrow j} = 1 - T + T z \prod_{l} H^{j\leftarrow l}$. This is the bond-percolation message passing of Karrer, Newman & Zdeborová, with occupation probability $T$. Linearising around the no-outbreak fixed point $H \equiv 1$ (for $z \to 1$) gives $\epsilon = T B \epsilon$ for $\epsilon_{i\leftarrow j} = 1 - H^{i\leftarrow j}$. The **non-backtracking** matrix appears because the message from $j$ to $i$ cannot depend on $i$'s own message back to $j$.

(sec-qmf-results)=
## Key results

:::{prf:proposition} QMF epidemic threshold for SIS
:label: prop-qmf-threshold

On a connected undirected network, the disease-free state of {eq}`eq-qmf-nimfa` loses stability at

$$
\lambda_c^{\mathrm{QMF}} = \frac{1}{\Lambda_1}.
$$ (eq-qmf-lc)
:::

:::{dropdown} Derivation
Linearise {eq}`eq-qmf-nimfa` at $\rho = 0$. The Jacobian is $J = -I + \lambda A$, so $J_{ij} = -\delta_{ij} + \lambda A_{ij}$, and its eigenvalues are $-1 + \lambda\Lambda$ for each eigenvalue $\Lambda$ of $A$. The largest is $-1 + \lambda\Lambda_1$. $A$ is non-negative and irreducible, so by Perron–Frobenius $\Lambda_1$ is real and positive, with a positive eigenvector. An endemic solution bifurcates when $\lambda\Lambda_1 = 1$ (the review, eq. 34).
:::

:::{prf:theorem} $1/\Lambda_1$ is a lower bound on the true SIS threshold
:label: thm-qmf-lowerbound

For the exact SIS Markov process on any network, $\lambda_c \ge 1/\Lambda_1$. Moreover, for $\lambda < 1/\Lambda_1$ the mean time to absorption obeys $\mathbb{E}[\tau_{\mathrm{abs}}] \le (\ln N + 1)/(1 - \lambda\Lambda_1)$ (Ganesh, Massoulié & Towsley 2005, [](doi:10.1109/INFCOM.2005.1498374), as stated in the review).
:::

:::{dropdown} Proof sketch (the review, eqs. 41–43)
In {eq}`eq-qmf-exact`, the term $-\beta\sum_j A_{ij}\mathbb{E}[X_i X_j]$ is non-positive. Dropping it gives, exactly, $\dot\rho_i \le -\rho_i + \lambda\sum_j A_{ij}\rho_j$. Collect the $\rho_i$ into a vector $W(t)$. The linear system has a non-negative propagator, so $W(t) \le e^{(\lambda A - I)t}W(0)$ componentwise. If $\lambda\Lambda_1 - 1 < 0$, every mode decays exponentially and the infection dies out fast, so no endemic state exists below $1/\Lambda_1$. QMF therefore *overestimates* spreading, because independence ignores the fact that infected nodes tend to have infected neighbours, who cannot be reinfected.
:::

:::{prf:proposition} $\Lambda_1 \ge \sqrt{k_{\max}}$ on any graph
:label: prop-qmf-sqrtk

For any undirected graph, $\Lambda_1 \ge \sqrt{k_{\max}}$, and hence $\lambda_c^{\mathrm{QMF}} \le 1/\sqrt{k_{\max}}$.
:::

:::{dropdown} Proof (my derivation; Castellano & Pastor-Satorras call it "simple to show")
Let $h$ be a node of degree $k = k_{\max}$. Take the test vector $y_h = 1$, $y_j = 1/\sqrt{k}$ for $j \in \mathcal{N}(h)$, and $0$ elsewhere. Then $y^\top y = 2$. The hub's edges alone contribute $y^\top A y \ge 2 \cdot k \cdot 1 \cdot (1/\sqrt{k}) = 2\sqrt{k}$, and the remaining edges only add non-negative terms. By the Rayleigh quotient, $\Lambda_1 \ge y^\top A y / y^\top y \ge \sqrt{k}$. So unless degrees are bounded, the QMF threshold always vanishes as $N \to \infty$.
:::

:::{prf:proposition} QMF steady state of a star
:label: prop-qmf-star

On a star with $k$ leaves, {eq}`eq-qmf-nimfa` has, for $\lambda > 1/\sqrt{k}$, the active steady state

$$
\rho_{\mathrm{hub}} = \frac{\lambda^2 k - 1}{(1 + \lambda k)\,\lambda}, \qquad
\rho_{\mathrm{leaf}} = \frac{\lambda^2 k - 1}{(1 + \lambda)\,k\,\lambda}
$$ (eq-qmf-star)

(Castellano & Pastor-Satorras 2010, eq. 4).
:::

:::{dropdown} Derivation
By symmetry all leaves share one $\rho_{\mathrm{leaf}}$. The rate equations are $\dot\rho_{\mathrm{hub}} = -\rho_{\mathrm{hub}} + (1-\rho_{\mathrm{hub}})\lambda k \rho_{\mathrm{leaf}}$ and $\dot\rho_{\mathrm{leaf}} = -\rho_{\mathrm{leaf}} + (1 - \rho_{\mathrm{leaf}})\lambda\rho_{\mathrm{hub}}$. Setting both to zero gives $\rho_{\mathrm{hub}} = \lambda k\rho_{\mathrm{leaf}}/(1 + \lambda k\rho_{\mathrm{leaf}})$ and $\rho_{\mathrm{leaf}} = \lambda\rho_{\mathrm{hub}}/(1 + \lambda\rho_{\mathrm{hub}})$. Eliminating $\rho_{\mathrm{leaf}}$ gives {eq}`eq-qmf-star`, which is positive iff $\lambda^2 k > 1$. This matches $\Lambda_1(\text{star}) = \sqrt{k}$.
:::

:::{prf:proposition} Prevalence just above the QMF threshold
:label: prop-qmf-prevalence

To first order in $\tau = \lambda\Lambda_1 - 1 \ll 1$, and provided there is a gap between $\Lambda_1$ and $\Lambda_2$, $\rho = N^{-1}\sum_i\rho_i \simeq \alpha_1\tau$ with $\alpha_1$ as in {eq}`eq-qmf-alpha` (Goltsev et al. 2012, eq. 5; the review, eqs. 36–37).
:::

:::{dropdown} Why localisation makes $\alpha_1 = O(1/N)$
If $x_i = O(1)$ on a bounded set of nodes and is negligible elsewhere, then $\sum_i x_i = O(1)$ and $\sum_i x_i^3 = O(1)$, so $\alpha_1 = O(1/N)$. The infected *number* $N\rho$ stays finite. If instead $x_i \approx N^{-1/2}$ everywhere, then $\sum_i x_i \approx N^{1/2}$ and $\sum_i x_i^3 \approx N^{-1/2}$, so $\alpha_1 = O(1)$. The IPR is a convenient diagnostic of which case holds.
:::

:::{prf:theorem} SIR / percolation threshold from the non-backtracking matrix (Karrer, Newman & Zdeborová 2014)
:label: thm-qmf-nb

For bond percolation with occupation probability $T$, and hence for the final size of SIR with transmissibility $T$, on a sparse, locally tree-like network,

$$
T_c = \frac{1}{\Lambda_{\max}(B)} .
$$ (eq-qmf-Tc)

For any network, $T_c \ge 1/\Lambda_{\max}(B) \ge 1/\Lambda_{\max}(A)$.
:::

:::{dropdown} Proof sketch
*Threshold.* Linearise the late-time message equations around $H \equiv 1$: $\epsilon_{i\leftarrow j} = T\sum_{l \in \mathcal{N}(j)\setminus i}\epsilon_{j\leftarrow l}$, that is, $\epsilon = TB\epsilon$. The trivial fixed point is stable iff $T\,\Lambda_{\max}(B) < 1$.

*Bound with loops.* On a non-tree-like graph the equality in the message equation becomes an inequality, by the Chebyshev integral inequality (as KNZ do, citing Karrer & Newman 2010). Iterating from $H = 1$ then never overshoots the true value, so the computed threshold is never above the true $T_c$.

*$\Lambda(B) \le \Lambda(A)$.* Let $B'_{i\leftarrow j,k\leftarrow l} = \delta_{jk}$, which also allows backtracking. If $w$ is an eigenvector of $A$, then $v_{i\leftarrow j} = w_j$ is an eigenvector of $B'$ with the same eigenvalue, so $\Lambda(B') = \Lambda(A)$. Since $B' - B \ge 0$ entrywise, Perron–Frobenius monotonicity (KNZ use the Collatz–Wielandt formula) gives $\Lambda(B) \le \Lambda(B')$.
:::

Two consequences:
- **Trees.** A tree has no closed non-backtracking walks, so $\Lambda_{\max}(B) = 0$ and there is no finite percolation threshold. A star's SIR outbreak is bounded by its size, whereas $1/\Lambda_1 = 1/\sqrt{k}$ would wrongly suggest one.
- **Random $k$-regular graphs.** $B$ has $k - 1$ non-zero entries per row and column, so $\Lambda(B) = k - 1$ and $T_c = 1/(k-1)$, the correct value. The adjacency bound would give $1/k$.

*My note:* on large uncorrelated random graphs the leading non-backtracking eigenvalue is close to the mean excess degree, $\langle k^2\rangle/\langle k\rangle - 1$. Then {eq}`eq-qmf-Tc` reduces to the Molloy–Reed / generating-function threshold $T_c = \langle k\rangle/(\langle k^2\rangle - \langle k\rangle)$ of [SIR–percolation](./07-sir-percolation.md). The worked example checks this numerically. For exponentially distributed recovery, Newman's mean transmissibility $T = \lambda/(1+\lambda)$ turns this into $\lambda_c = \langle k\rangle/(\langle k^2\rangle - 2\langle k\rangle)$ (the review, eq. 62).

(sec-qmf-example)=
## Worked example

All values below are from numpy/scipy. $\Lambda_{\max}(B)$ was computed both from $B$ directly and from the $2N\times2N$ Ihara–Bass companion matrix $\begin{pmatrix} A & I - D\\ I & 0\end{pmatrix}$; the two agree, e.g. $4.2466$ both ways on a 60-node Erdős–Rényi test graph. *(Using the companion matrix is my computational choice.)* The power-law graphs are configuration-model graphs with $k_{\min} = 3$, simplified to remove multi-edges and self-loops, with a structural cutoff $k \le \sqrt N$ for $\gamma = 2.3$.

| Graph | $N$ | $\langle k\rangle$ | $k_{\max}$ | $\sqrt{k_{\max}}$ | $\frac{\langle k^2\rangle}{\langle k\rangle}$ | $\Lambda_1$ | IPR | $\Lambda_{\max}(B)$ |
|---|---|---|---|---|---|---|---|---|
| star, $k=10$ | 11 | 1.818 | 10 | 3.162 | 5.500 | 3.162 | 0.2750 | 0 |
| star, $k=100$ | 101 | 1.980 | 100 | 10.000 | 50.50 | 10.000 | 0.2525 | 0 |
| random 3-regular | 2000 | 3 | 3 | 1.732 | 3.000 | 3.000 | 0.0005 | 2.000 |
| power law, $\gamma = 2.3$ | 10 000 | 7.264 | 100 | 10.00 | 18.86 | 20.27 | 0.0028 | 17.88 |
| power law, $\gamma = 3.5$ | 10 000 | 4.259 | 137 | 11.70 | 6.906 | 12.20 | 0.1955 | 5.844 |

Thresholds. The SIS columns are in $\lambda$; the SIR columns are in transmissibility $T$.

| Graph | SIS QMF $1/\Lambda_1$ | SIS HMF $\langle k\rangle/\langle k^2\rangle$ | SIR NB $1/\Lambda_{\max}(B)$ | SIR config. model $\frac{\langle k\rangle}{\langle k^2\rangle-\langle k\rangle}$ | SIR-IBMF $1/\Lambda_1$ |
|---|---|---|---|---|---|
| star, $k=100$ | 0.1000 | 0.0198 | $\infty$ | 0.0202 | 0.1000 |
| random 3-regular | 0.3333 | 0.3333 | **0.5000** | 0.5000 | 0.3333 |
| power law, $\gamma = 2.3$ | 0.0493 | 0.0530 | 0.0559 | 0.0560 | 0.0493 |
| power law, $\gamma = 3.5$ | **0.0820** | 0.1448 | **0.1711** | 0.1693 | 0.0820 |

What to read off:
- **Star.** $\Lambda_1 = \sqrt{k}$ exactly, and the eigenvector is localised: $\mathrm{IPR} = 1/4 + 1/(4k)$, with half the weight on the hub. QMF iterated to a fixed point at $k = 100$ gives no activity at $\lambda = 0.08 < 1/\sqrt{100}$. At $\lambda = 0.15$ it gives $\rho_{\mathrm{hub}} = 0.5208$ and $\rho_{\mathrm{leaf}} = 0.0725$, matching {eq}`eq-qmf-star`. HMF, applied to a single star, is meaningless: it averages a hub and leaves into one degree distribution.
- **$\gamma = 2.3$.** $\Lambda_1 \approx \langle k^2\rangle/\langle k\rangle > \sqrt{k_{\max}}$. The eigenvector is delocalised: $\mathrm{IPR} = 0.0028$, about $27/N$. QMF and HMF agree to within 7%.
- **$\gamma = 3.5$.** $\Lambda_1 = 12.2 \approx \sqrt{k_{\max}} = 11.7$, far above $\langle k^2\rangle/\langle k\rangle = 6.9$. The eigenvector is localised: $\mathrm{IPR} = 0.20$, nearly $2000$ times the uniform value. The QMF SIS threshold is about **half** the HMF one, set by a single hub.
- **SIR.** The non-backtracking threshold matches the configuration-model value (0.1711 vs 0.1693 for $\gamma = 3.5$; 0.0559 vs 0.0560 for $\gamma = 2.3$), since $\Lambda(B) \approx \langle k^2\rangle/\langle k\rangle - 1$ (5.84 vs 5.91; 17.88 vs 17.86). SIR-IBMF's $1/\Lambda_1$ is off by a factor of two for $\gamma = 3.5$. On the 3-regular graph, NB gives the exact $T_c = 1/2$, whereas $1/\Lambda_1 = 1/3$.

## Assumptions and limitations

- **QMF is a closure, not an exact theory.** It neglects dynamical correlations: neighbours of an infected node are more likely to be infected, and so less available. That is why it gives a lower bound on $\lambda_c$. Pair-based closures improve it (the review, §V.A.3); some are exact on trees.
- **The asymptotic spectral formula is model-specific.** The Chung–Lu–Vu result is for random graphs with given expected degrees and holds up to constants. Correlations shift $\Lambda_1$. Goltsev et al. find that assortative mixing raises it and disassortative mixing lowers it.
- **$k_{\max}$ fluctuates strongly between realisations** for $\gamma > 3$; both its mean and its standard deviation scale like $N^{1/(\gamma-1)}$. Single-network thresholds are therefore noisy, and Castellano & Pastor-Satorras fix $k_{\max}$ to its mean to compare sizes.
- **Finite size versus the thermodynamic limit.** "Vanishing threshold" is an $N \to \infty$ statement. Real networks have bounded $k_{\max}$ (spatial, temporal and cognitive limits), so effective thresholds are finite, though possibly far below homogeneous estimates (the review, §V.A.6).
- **Message passing needs the graph to be locally tree-like.** With short loops (clustering), it gives a bound rather than the exact value.
- **Mean transmissibility is not exact when $T$ varies between edges.** It gets the threshold and mean outbreak size right but not the outbreak probability (Kenah & Robins; see [SIR–percolation](./07-sir-percolation.md)).
- *My comment:* "threshold" here means a linear-stability or percolation point. For SIS on large power-law graphs the rigorous statement is about exponentially long survival for every $\lambda > 0$, which is not quite the same thing as a mean-field bifurcation.

## Connections

- **PHYS 7335.**
  - [Heterogeneous mean field](./05-heterogeneous-mean-field.md) is QMF applied to the annealed matrix; the two agree iff $\Lambda_1 \approx \langle k^2\rangle/\langle k\rangle$.
  - [SIR–percolation](./07-sir-percolation.md) derives the configuration-model $T_c$ that the non-backtracking threshold reduces to.
  - [Compartmental models](./03-compartmental-models.md) are the well-mixed limit.
  - [Next-generation matrices](./04-thresholds-and-ngm.md): here the next-generation operator is $\lambda A$, with spectral radius $\lambda\Lambda_1$. *My note.*
- **NETS 7332.**
  - The principal eigenvector $x$ is **eigenvector centrality** ([link analysis](../nets-7332/basics/02-link-analysis.md)). QMF says the epidemic onset is shaped like eigenvector centrality.
  - The non-backtracking matrix reappears in spectral community detection and in non-backtracking graph distances (the network-comparison reading).
  - The message passing equations {eq}`eq-qmf-mp` are belief propagation on the cavity graph, the same structure as loopy BP in [label propagation](../nets-7332/basics/04-label-propagation.md).
- **NETS 5116.**
  - Eigenvector centrality and the Perron–Frobenius theorem: [Newman ch. 7](../nets-5116/newman/07-measures-and-metrics.md).
  - Robustness and the Molloy–Reed criterion: [Barabási ch. 8](../nets-5116/barabasi/08-network-robustness.md).
  - The degree-based epidemic threshold: [Barabási ch. 10](../nets-5116/barabasi/10-spreading-phenomena.md).

## Self-test

:::{dropdown} Q1. Derive the QMF SIS threshold and state what it bounds.
Linearising $\dot\rho_i = -\rho_i + \lambda(1-\rho_i)\sum_j A_{ij}\rho_j$ at $\rho = 0$ gives $J = -I + \lambda A$, which becomes unstable at $\lambda = 1/\Lambda_1$. Dropping the non-positive pair term in the exact equations gives $\dot\rho \le (\lambda A - I)\rho$. So the exact process dies out exponentially below $1/\Lambda_1$, which makes $1/\Lambda_1$ a **lower** bound on the true SIS threshold.
:::

:::{dropdown} Q2. When do QMF and HMF give different SIS thresholds on a power-law network, and which hub property drives the difference?
They differ when $\Lambda_1$ is set by $\sqrt{k_{\max}}$ rather than $\langle k^2\rangle/\langle k\rangle$, which happens for $\gamma > 5/2$, since $\langle k^2\rangle/\langle k\rangle \sim k_{\max}^{3-\gamma} < \sqrt{k_{\max}}$ there. The driver is the largest hub and its star: $\Lambda_1 \ge \sqrt{k_{\max}}$ on any graph, so QMF's threshold vanishes whenever $k_{\max}$ diverges, even for $\gamma > 3$.
:::

:::{dropdown} Q3. What does the IPR of the principal eigenvector tell you about the transition at $1/\Lambda_1$?
Just above threshold, $\rho \simeq \alpha_1(\lambda\Lambda_1 - 1)$ with $\alpha_1 = \sum x_i / (N\sum x_i^3)$. If the eigenvector is **delocalised** ($\mathrm{IPR} \to 0$), $\alpha_1 = O(1)$ and the state is endemic. If it is **localised** ($\mathrm{IPR} = O(1)$), $\alpha_1 = O(1/N)$: only a finite cluster around the hub is active, which is a sub-endemic state.
:::

:::{dropdown} Q4. Why does the hub argument make the SIS threshold vanish but not the SIR threshold?
In SIS a hub and its leaves reinfect each other indefinitely: the star is active for $\lambda > 1/\sqrt{k}$ and acts as a reservoir. In SIR a node is infected at most once, so a hub can spread at most one wave and then recovers for good. SIR's final size is a percolation property, set by the non-backtracking spectrum, which a star alone cannot raise.
:::

:::{dropdown} Q5. Why does the *non-backtracking* matrix, rather than $A$, set the SIR/percolation threshold on tree-like graphs?
The cavity message $j \to i$ must be computed without $i$, because $j$ can only have been infected by its *other* neighbours. Linearising the message equations therefore propagates perturbations along directed edges without immediate reversal: $\epsilon = TB\epsilon$. Walks counted by $A$ include backtracking steps that double-count transmission back to the infector. This is why $1/\Lambda(A)$ underestimates $T_c$, e.g. $1/k$ instead of $1/(k-1)$ on a $k$-regular graph.
:::

:::{dropdown} Q6. Order $1/\Lambda_1$, $1/\Lambda_{\max}(B)$ and the true $T_c$ for SIR on a graph with loops, and say what happens on a tree.
$1/\Lambda_1 \le 1/\Lambda_{\max}(B) \le T_c$. The middle quantity equals $T_c$ on locally tree-like graphs. On a finite tree $\Lambda_{\max}(B) = 0$: there is no percolation threshold, and every outbreak is bounded by the tree.
:::

:::{dropdown} Q7. On a large uncorrelated random graph, what does $1/\Lambda_{\max}(B)$ reduce to, and what does that imply for $\gamma > 3$?
$\Lambda_{\max}(B) \approx \langle k^2\rangle/\langle k\rangle - 1$, the mean excess degree, so $T_c \approx \langle k\rangle/(\langle k^2\rangle - \langle k\rangle)$. This is the configuration-model / HMF value. It is finite for $\gamma > 3$, because $\langle k^2\rangle$ is finite there, and vanishes for $\gamma < 3$.
:::

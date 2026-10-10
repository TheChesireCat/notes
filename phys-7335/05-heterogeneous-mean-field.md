---
title: Heterogeneous Mean-Field Epidemics on Networks
short_title: Heterogeneous mean-field
subject: PHYS 7335 · Topic
description: The degree-based (heterogeneous) mean-field theory of SIS and SIR on networks, why the epidemic threshold is set by ⟨k⟩/⟨k²⟩ and vanishes on scale-free networks, and what this implies for immunisation.
tags: [epidemics, sis, sir, mean-field, epidemic-threshold, scale-free, immunisation]
---

:::{tip} TL;DR
- **Heterogeneous mean-field (HMF)**, also called degree-based mean-field (DBMF), treats all nodes of degree $k$ as statistically equivalent. The SIS dynamics then reduces to one equation per degree class: $\dot\rho_k = -\rho_k + \lambda k (1-\rho_k)\,\Theta$. Here $\Theta$ is the probability that an edge points to an infected node, and time is measured in units of $1/\mu$.
- **SIS threshold.** On uncorrelated networks the endemic state exists iff $\lambda > \lambda_c = \langle k \rangle / \langle k^2 \rangle$. With degree correlations, $\lambda_c = 1/\Lambda_m$, where $\Lambda_m$ is the largest eigenvalue of $C_{kk'} = k\,P(k' \mid k)$. A diverging $\langle k^2\rangle$ forces $\lambda_c \to 0$ even with assortative or disassortative mixing.
- **Scale-free networks with $2 < \gamma \le 3$** have no epidemic threshold as $N \to \infty$. Finite networks have a threshold set by the cutoff $k_{\max}$, and it shrinks slowly with $N$. The price is a **tiny prevalence** near $\lambda \to 0$. For the BA network ($\gamma = 3$), $\rho \simeq 2 e^{-1/(m\lambda)}$.
- **SIR.** Annealed HMF gives the same $\lambda_c = \langle k\rangle/\langle k^2\rangle$. On a static network an infected node cannot reinfect the node that infected it. Removing that edge gives $\lambda_c = \langle k\rangle/(\langle k^2\rangle - \langle k\rangle)$. The exact percolation result for exponential recovery times is $\lambda_c = \langle k\rangle/(\langle k^2\rangle - 2\langle k\rangle)$. All three vanish when $\langle k^2\rangle$ diverges.
- **Immunisation.** Random immunisation of a fraction $g$ just rescales $\lambda \to \lambda(1-g)$, so $g_c = 1 - \lambda_c/\lambda \to 1$ on scale-free networks. **Targeting hubs** gives $g_c \simeq e^{-2/(m\lambda)}$ on BA networks. **Acquaintance immunisation** reaches the hubs using only local information, because a random neighbour has degree distribution $\propto k\,P(k)$.
:::

- **Source.**
  - [](doi:10.1103/PhysRevLett.86.3200) (Pastor-Satorras & Vespignani, *PRL* 86, 3200, 2001): the original HMF calculation and the BA prevalence.
  - [](doi:10.1103/RevModPhys.87.925) (Pastor-Satorras, Castellano, Van Mieghem & Vespignani, *Rev. Mod. Phys.* 87, 925, 2015), §§ IV.B, V.A.1, V.B.1 and VI.A: the general correlated threshold, the SIR variants and immunisation.
  - [](doi:10.1103/PhysRevLett.90.028701) (Boguñá, Pastor-Satorras & Vespignani, *PRL* 90, 028701, 2003): correlated networks.
  - [](doi:10.1103/PhysRevE.65.036104) (Pastor-Satorras & Vespignani, *PRE* 65, 036104, 2002): immunisation.
  - [](doi:10.1103/PhysRevLett.91.247901) (Cohen, Havlin & ben-Avraham, *PRL* 91, 247901, 2003): acquaintance immunisation.
  - Course textbook: Barrat, Barthélemy & Vespignani, *Dynamical Processes on Complex Networks* (CUP 2008).
- **Builds on.**
  - Degree classes, $P(k'\mid k)$ and the annealed approximation ([Degree-block formalism](./01-degree-block-formalism.md)).
  - Homogeneous SIS/SIR and $R_0$ ([Compartmental models](./03-compartmental-models.md)).
- **Notation.** Shared symbols as in [](#notation). This page writes the degree distribution as $P(k) \equiv p_k$, following the physics literature.
  - $P(k' \mid k)$: the probability that an edge from a degree-$k$ node ends at a degree-$k'$ node.
  - $\rho_k(t)$: the probability that a degree-$k$ node is infected. $\rho = \sum_k P(k)\rho_k$ is the total prevalence (SIS), and $\rho^R_\infty$ is the final epidemic size (SIR).
  - $\lambda = \beta/\mu$, with $\beta$ the per-edge transmission rate (*not* the PageRank damping factor) and $\mu$ the recovery rate.
  - $g$: the immunised fraction. $m$: the BA minimum degree, so $\langle k \rangle = 2m$.

(sec-hmf-setup)=
## Setup and definitions

:::{prf:definition} Degree-class (HMF) approximation
:label: def-hmf-approx

All nodes with the same degree $k$ are **statistically equivalent**. The state of the system is described by the partial densities $\rho^\alpha_k(t)$, the probability that a degree-$k$ node is in compartment $\alpha$, with $\sum_\alpha \rho^\alpha_k = 1$. A degree-$k$ node connects to a degree-$k'$ node with probability $P(k' \mid k)$, which is the only structure kept beyond $P(k)$.

Equivalently, the adjacency matrix is replaced by its **annealed** ensemble average,

$$
\bar a_{ij} = \frac{k_j\,P(k_i \mid k_j)}{N\,P(k_i)} \quad \xrightarrow{\text{uncorrelated}} \quad \bar a_{ij} = \frac{k_i k_j}{N \langle k \rangle}.
$$ (eq-hmf-annealed)

Rates follow the law of mass action, and expectations of products are factorised.
:::

:::{prf:definition} Uncorrelated network
:label: def-hmf-uncorrelated

A network is **degree-uncorrelated** if $P(k' \mid k) = k' P(k')/\langle k \rangle$, independent of $k$. Following a random edge, you reach a node of degree $k'$ with probability proportional to $k'$, the same bias as in the friendship paradox.
:::

:::{prf:definition} Epidemic threshold
:label: def-hmf-threshold

For SIS, $\lambda_c$ separates an **absorbing phase** ($\rho = 0$ in the stationary state) from an **endemic phase** ($\rho > 0$). For SIR, it separates outbreaks whose final size vanishes as $N \to \infty$ from outbreaks reaching a finite fraction of the population. In the physics language it is the critical point of a non-equilibrium (absorbing-state) phase transition. SIS on a lattice is the contact process.
:::

(sec-hmf-core)=
## Core ideas

### The SIS degree-block equation

Rescale time by $1/\mu$, so the recovery rate is 1 and the infection rate per edge is $\lambda$. A degree-$k$ node recovers at rate 1. While susceptible, it is infected through each of its $k$ edges at rate $\lambda$ times the probability that the edge's other end is infected:

$$
\frac{d\rho_k}{dt} = -\rho_k + \lambda k\,(1-\rho_k) \sum_{k'} P(k' \mid k)\,\rho_{k'}.
$$ (eq-hmf-sis-general)

For uncorrelated networks the sum no longer depends on $k$. It becomes a single function,

$$
\Theta(t) = \sum_{k'} \frac{k' P(k')}{\langle k \rangle}\,\rho_{k'}(t),
\qquad
\frac{d\rho_k}{dt} = -\rho_k + \lambda k\,(1-\rho_k)\,\Theta,
$$ (eq-hmf-sis)

where $\Theta$ is the probability that a **randomly chosen edge** points to an infected node. The edge bias $k'P(k')/\langle k\rangle$ is the whole story: hubs are reached disproportionately often along edges, so they dominate $\Theta$.

Setting $\dot\rho_k = 0$:

$$
\rho_k = \frac{\lambda k \Theta}{1 + \lambda k \Theta},
\qquad
\Theta = \frac{1}{\langle k \rangle} \sum_k k P(k)\,\frac{\lambda k \Theta}{1 + \lambda k \Theta},
\qquad
\rho = \sum_k P(k)\,\rho_k.
$$ (eq-hmf-stationary)

Each $\rho_k$ increases with $k$, so higher-degree nodes are infected more often. The second relation is a **self-consistency equation** for $\Theta(\lambda)$.

### Why heterogeneity matters

On a homogeneous (regular) network, $\langle k^2 \rangle = \langle k \rangle^2$ and the threshold is $\lambda_c = 1/\langle k \rangle$. This is the homogeneous-mixing condition $R_0 = \langle k\rangle\beta/\mu > 1$ (RMP eq. 11). Heterogeneity enters only through $\langle k^2\rangle/\langle k\rangle$, the mean degree of a node reached by following an edge. For heavy-tailed $P(k) \sim k^{-\gamma}$ with $2 < \gamma \le 3$, $\langle k\rangle$ stays finite while $\langle k^2 \rangle \sim k_{\max}^{3-\gamma}$ diverges (logarithmically at $\gamma = 3$). In the PRL's words, the unbounded connectivity fluctuations "play the role of an infinite connectivity".

### Three SIR thresholds and why they differ

The SIR version tracks $\rho^S_k$, $\rho^I_k$ and $\rho^R_k$ with $\dot\rho^R_k = \rho^I_k$. The threshold depends on how faithfully the theory treats the edge along which a node was infected:

| Treatment | Edge factor for a degree-$k'$ infector | Threshold (uncorrelated) |
|---|---|---|
| Annealed HMF (edges reshuffled faster than the epidemic) | $k'$ | $\langle k \rangle / \langle k^2 \rangle$ |
| HMF on a static network: the edge to its own infector is already used | $k' - 1$ | $\langle k \rangle / (\langle k^2 \rangle - \langle k \rangle)$ |
| Exact on locally tree-like static networks, via bond percolation with $T = \lambda/(1+\lambda)$ | (exact) | $\langle k \rangle / (\langle k^2 \rangle - 2\langle k \rangle)$ |

The second row is the **one-step non-backtracking correction**: a node infected through one of its edges can transmit through at most $k'-1$ of them. The RMP calls this modified DBMF "an approximation of the exact result". It gets the qualitative picture right, a vanishing threshold iff $\langle k^2 \rangle$ diverges, but not the exact value. The third row is derived on the [SIR–percolation](./07-sir-percolation.md) page.

### Immunisation

Immunised nodes are removed together with their edges. The aim is to push the threshold above the actual $\lambda$, giving herd immunity. The **immunisation threshold** $g_c(\lambda)$ is the smallest immunised fraction that eradicates the infection.

| Strategy | Information needed | HMF result (SIS) |
|---|---|---|
| **Uniform** (random nodes) | none | Equivalent to $\lambda \to \lambda(1-g)$, so $g_c = 1 - \lambda_c/\lambda = 1 - \dfrac{\langle k\rangle}{\lambda \langle k^2\rangle} \to 1$ on scale-free networks |
| **Proportional** (fraction $g_k$ of degree-$k$ nodes) | each node's degree | Eradication if $g_k \ge 1 - 1/(\lambda k)$, so $g_c = \sum_{k > 1/\lambda} \big(1 - \tfrac{1}{k\lambda}\big) P(k)$, which is $\simeq (m\lambda)^2/3$ for $\gamma = 3$ |
| **Targeted** (the $gN$ highest-degree nodes) | the global degree ranking | Implicit condition $\langle k^2 \rangle_{g_c} / \langle k \rangle_{g_c} = 1/\lambda$ on the pruned network; for BA, $g_c \simeq e^{-2/(m\lambda)}$ |
| **Acquaintance** (immunise a random neighbour of a random node) | only local | A random neighbour has degree $\propto k P(k)$, so hubs are hit preferentially and a small $g_c$ results (Cohen et al., for SIR via percolation) |

Uniform immunisation fails because a rescaling by $(1-g)$ cannot beat a threshold of zero. The other three succeed by removing the high-degree tail that drives $\langle k^2 \rangle$. A random walker that immunises the nodes it visits works like acquaintance immunisation, because its stationary distribution is also $\propto k$ (RMP § VI.A).

(sec-hmf-results)=
## Key results

:::{prf:theorem} SIS threshold, uncorrelated networks
:label: thm-hmf-threshold-unc

Under the HMF approximation on an uncorrelated network, the self-consistency equation {eq}`eq-hmf-stationary` has a solution $\Theta > 0$ (an endemic state) iff

$$
\lambda > \lambda_c = \frac{\langle k \rangle}{\langle k^2 \rangle}.
$$ (eq-hmf-lc)
:::

:::{dropdown} Derivation
Write the self-consistency equation as $\Theta = f(\Theta)$ with

$$
f(\Theta) = \frac{1}{\langle k\rangle} \sum_k k P(k) \frac{\lambda k \Theta}{1 + \lambda k\Theta}.
$$

The function $f$ has these properties:
- $f(0) = 0$;
- $f$ is increasing and strictly concave, since each term $x/(1+x)$ is;
- $f(1) < 1$.

So a non-trivial intersection with the line $y = \Theta$ in $(0,1]$ exists iff the slope at the origin exceeds 1:

$$
f'(0) = \frac{\lambda}{\langle k\rangle}\sum_k k^2 P(k) = \lambda \frac{\langle k^2\rangle}{\langle k\rangle} > 1.
$$

This is PRL eqs. 1–4 and RMP eqs. 24–28. For a regular network it reduces to $\lambda_c = 1/\langle k\rangle$.
:::

:::{prf:theorem} SIS threshold with degree correlations
:label: thm-hmf-threshold-corr

Linearising {eq}`eq-hmf-sis-general` around $\rho_k = 0$ gives $\dot\rho_k \simeq \sum_{k'} J_{kk'} \rho_{k'}$ with $J_{kk'} = -\delta_{kk'} + \lambda C_{kk'}$, where

$$
C_{kk'} = k\,P(k' \mid k).
$$ (eq-hmf-C)

The healthy state is unstable, and an endemic state appears, iff $\lambda > \lambda_c = 1/\Lambda_m$, where $\Lambda_m$ is the largest eigenvalue of $C$. Perron–Frobenius guarantees that $\Lambda_m$ exists and is real and positive, because $C$ is non-negative and assumed irreducible.
:::

:::{dropdown} Derivation, and the uncorrelated limit
Drop the $O(\rho^2)$ term $-\lambda k \rho_k \sum_{k'} P(k'\mid k)\rho_{k'}$. The linear system $\dot{\boldsymbol\rho} = (-I + \lambda C)\boldsymbol\rho$ grows iff $\lambda\Lambda_m - 1 > 0$.

For uncorrelated networks, $C_{kk'} = k\,k' P(k')/\langle k\rangle$ has rank one. Its only non-zero eigenvalue has eigenvector $v_k = k$:

$$
\sum_{k'} \frac{k\, k' P(k')}{\langle k \rangle}\, k' = k \frac{\langle k^2\rangle}{\langle k\rangle},
$$

so $\Lambda_m = \langle k^2\rangle/\langle k\rangle$, recovering {eq}`eq-hmf-lc`. The matrix $C$ is not symmetric, but detailed balance, $k P(k) P(k'\mid k) = k' P(k') P(k\mid k')$, makes it similar to a symmetric matrix.
:::

:::{prf:proposition} Correlations cannot restore a threshold if $\langle k^2 \rangle$ diverges
:label: prop-hmf-correlations

The result is due to Boguñá, Pastor-Satorras & Vespignani (2003). For networks with degree correlations described only by $P(k'\mid k)$ ("unstructured" networks) and satisfying detailed balance, a diverging $\langle k^2 \rangle$ is a **sufficient** condition for $\Lambda_m \to \infty$, and hence $\lambda_c \to 0$, whether mixing is assortative or disassortative.
:::

:::{dropdown} Idea of the proof
A Perron–Frobenius bound on the row sums of $C^2$ gives

$$
\Lambda_m^2 \ge \min_k \sum_{\ell} \ell\,P(\ell\mid k)\,\bar k_{nn}(\ell),
\qquad
\bar k_{nn}(\ell) = \sum_{k'} k' P(k'\mid \ell),
$$

where $\bar k_{nn}$ is the average nearest-neighbour degree. Multiplying detailed balance, $kP(k'\mid k)P(k) = k'P(k\mid k')P(k')$, by $k$ and summing gives the identity $\langle k^2\rangle = \sum_{k'} k'P(k')\,\bar k_{nn}(k')$. When $\langle k^2\rangle \sim k_{\max}^{3-\gamma}$ diverges, the paper shows case by case (disassortative, and assortative with any growth exponent of $\bar k_{nn}$) that the divergence cannot come from the sum alone. So $\bar k_{nn}(\ell)$ must itself diverge on a set of non-zero measure, which makes the lower bound on $\Lambda_m$ diverge.
:::

:::{prf:proposition} Prevalence on the BA network
:label: prop-hmf-ba

Approximate degree as continuous, with $P(k) = 2m^2 k^{-3}$ for $k \ge m$ (so $\langle k\rangle = 2m$). The self-consistency equation then solves exactly:

$$
\Theta(\lambda) = \frac{e^{-1/(m\lambda)}}{m\lambda}\,\big(1 - e^{-1/(m\lambda)}\big)^{-1},
\qquad
\rho \simeq 2\,e^{-1/(m\lambda)} \quad (\lambda \to 0).
$$ (eq-hmf-ba)

There is no threshold, but the prevalence is **exponentially small** in $1/\lambda$: a stretched-exponential approach to zero.
:::

:::{dropdown} Derivation
Substitute into {eq}`eq-hmf-stationary`:

$$
\Theta = \frac{1}{2m}\int_m^\infty 2m^2 k^{-2}\,\frac{\lambda k\Theta}{1+\lambda k\Theta}\,dk
= m\lambda\Theta \int_m^\infty \frac{dk}{k(1+\lambda k \Theta)}
= m\lambda\Theta\,\ln\!\Big(1 + \frac{1}{m\lambda\Theta}\Big).
$$

Dividing by $\Theta \neq 0$ gives $1/(m\lambda\Theta) = e^{1/(m\lambda)} - 1$, which is the stated $\Theta$. For small $\lambda$, $\Theta \approx e^{-1/(m\lambda)}/(m\lambda)$. Inserting it in $\rho = \int P(k)\rho_k\,dk$ and keeping the lowest order gives $\rho \approx 2e^{-1/(m\lambda)}$ (PRL eqs. 5–6). This integral was rechecked for this page; the worked example compares the exact integral with the asymptotic form.
:::

:::{prf:proposition} Critical behaviour (uncorrelated, $P(k) \sim k^{-\gamma}$)
:label: prop-hmf-exponents

Near threshold, $\rho \sim (\lambda - \lambda_c)^{\beta_{\mathrm{SIS}}}$ with

$$
\beta_{\mathrm{SIS}} =
\begin{cases}
1/(3-\gamma) & 2 < \gamma < 3,\\
1/(\gamma - 3) & 3 < \gamma \le 4,\\
1 & \gamma > 4,
\end{cases}
$$ (eq-hmf-exponents)

with the stretched exponential of {eq}`eq-hmf-ba` at $\gamma = 3$ (RMP eq. 29). These exponents are the same as those for bond percolation on the same networks. For $2 < \gamma < 3$, $\beta_{\mathrm{SIS}} > 1$: the threshold vanishes, but prevalence grows very slowly with $\lambda$.
:::

:::{prf:proposition} Early growth time scale (SI/SIR, uncorrelated)
:label: prop-hmf-growth

At short times $\rho^I(t) \sim e^{t/\tau}$ with

$$
\tau = \frac{\langle k\rangle}{\beta\langle k^2\rangle - (\mu+\beta)\langle k \rangle},
$$ (eq-hmf-tau)

which reduces to $\tau = \langle k\rangle/[\beta(\langle k^2 \rangle - \langle k\rangle)]$ for SI ($\mu = 0$). This is RMP eqs. 56–57, after Barthélemy et al. When $\langle k^2\rangle$ diverges, the outbreak is also **instantaneous** in the thermodynamic limit: infection hits hubs first, then cascades down to smaller degree classes.
:::

## Worked example

All numbers below were computed in Python. Power-law networks use $P(k) \propto k^{-\gamma}$ on $k \in [3, k_{\max}]$ with the natural cutoff $k_{\max} = 3N^{1/(\gamma-1)}$. That cutoff is a modelling choice made for this example.

**Thresholds for different degree distributions**

| Network | $N$ | $k_{\max}$ | $\langle k\rangle$ | $\langle k^2\rangle$ | SIS $\langle k\rangle/\langle k^2\rangle$ | SIR, static HMF | SIR, exact (percolation) |
|---|---|---|---|---|---|---|---|
| Poisson, $\langle k\rangle = 6$ | — | — | 6.00 | 42.0 | 0.143 | 0.167 | 0.200 |
| $\gamma = 3.5$ | $10^4$ | 119 | 4.28 | 28.1 | 0.153 | 0.180 | 0.220 |
| $\gamma = 3.5$ | $10^8$ | 4754 | 4.30 | 32.1 | 0.134 | 0.155 | 0.183 |
| $\gamma = 3$ | $10^4$ | 300 | 5.08 | 62.1 | 0.082 | 0.089 | 0.098 |
| $\gamma = 3$ | $10^8$ | 30000 | 5.12 | 121.8 | 0.042 | 0.044 | 0.046 |
| $\gamma = 2.5$ | $10^4$ | 1392 | 7.32 | 433.9 | 0.017 | 0.017 | 0.018 |
| $\gamma = 2.5$ | $10^8$ | 646330 | 7.63 | 9742.7 | 0.0008 | 0.0008 | 0.0008 |

- **$\gamma = 3.5$.** $\langle k^2\rangle$ converges, so the threshold settles at a finite value.
- **$\gamma = 3$.** $\langle k^2\rangle \sim \ln k_{\max}$, so the threshold decays only logarithmically. Even at $N = 10^8$ it is still about $0.04$.
- **$\gamma = 2.5$.** $\langle k^2\rangle \sim k_{\max}^{1/2}$, so the threshold collapses as a power of $N$.
- **The three SIR thresholds** differ by $O(\langle k\rangle/\langle k^2\rangle)$ corrections, which vanish exactly when heterogeneity is strong.

**Correlations: a two-class network.** Take $P(2) = 0.9$ and $P(20) = 0.1$, so $\langle k\rangle = 3.8$, $\langle k^2\rangle = 43.6$ and $\lambda_c^{\mathrm{unc}} = 0.087$. A regular network with the same mean degree would have $1/\langle k\rangle = 0.263$. The edge-end fractions are $q_2 = 0.474$ and $q_{20} = 0.526$. Fix the fraction $x$ of edge-ends linking a degree-2 node to a degree-20 node, set $e_{22} = q_2 - x$ and $e_{20,20} = q_{20} - x$, and take $P(k'\mid k) = e_{kk'}/q_k$:

| Mixing | $x$ | $\Lambda_m$ | $\lambda_c = 1/\Lambda_m$ |
|---|---|---|---|
| assortative | 0.05 | 18.13 | 0.055 |
| assortative | 0.10 | 16.31 | 0.061 |
| uncorrelated ($x = q_2 q_{20}$) | 0.249 | 11.47 $= \langle k^2\rangle/\langle k\rangle$ | 0.087 |
| disassortative | 0.40 | 8.10 | 0.124 |

Assortativity lowers the threshold because hubs reinfect each other; disassortativity raises it. Both effects are finite here, since $\langle k^2\rangle$ is finite.

**BA network, $m = 3$.** The exact continuous-$k$ solution {eq}`eq-hmf-ba`, compared with the lowest-order prevalence:

| $\lambda$ | $\Theta$ | $\rho$ (integral) | $2e^{-1/(m\lambda)}$ |
|---|---|---|---|
| 0.10 | 0.123 | 0.065 | 0.071 |
| 0.15 | 0.270 | 0.177 | 0.217 |
| 0.25 | 0.477 | 0.374 | 0.527 |
| 0.50 | 0.703 | 0.626 | 1.027 (meaningless) |

- **The asymptotic form** is only good for $\lambda \lesssim 0.1$.
- **Degree profile.** At $\lambda = 0.25$, $\rho_k = 0.26, 0.54, 0.78, 0.92, 0.99$ for $k = 3, 10, 30, 100, 1000$: the hubs are almost always infected.
- **Immunisation at $\lambda = 0.25$.** The targeted formula gives $g_c \simeq e^{-8/3} \approx 0.07$. The PRE's simulations at the same $\lambda$ find $g_c \approx 0.16$ on finite BA networks, consistent with the formula being a small-$\lambda$, large-$N$ asymptotic. Uniform immunisation on the $\gamma = 3$ networks of the first table would need $g_c = 1 - \lambda_c/\lambda = 0.67$ at $N=10^4$ and $0.78$ at $N=10^6$, rising towards 1.

## Assumptions and limitations

- **Annealed, not quenched.** HMF is exact for annealed networks, where edges are reshuffled (preserving $P(k)$ and $P(k'\mid k)$) much faster than the epidemic evolves. On a **static** network, the identity of a node's neighbours matters. Individual-based (quenched) mean-field gives $\lambda_c = 1/\Lambda_1$, the inverse leading eigenvalue of the adjacency matrix. That threshold vanishes for *any* growing $k_{\max}$, including $\gamma > 3$, where HMF predicts a finite threshold. The disagreement is about localisation near hubs; see [Quenched mean-field and message passing](./06-quenched-mean-field.md).
- **Degree is the only node property.** Clustering, communities and any structure beyond $P(k'\mid k)$ are discarded. In the NETS 6116 language, HMF is a theory on the 2k-random graph.
- **Factorised expectations.** Dynamical correlations between neighbours, such as an infector and the node it just infected, are neglected. That is why static-network SIR needs the $k'-1$ correction and is still not exact.
- **Thermodynamic limit.** "No threshold" is an $N \to \infty$ statement. Real networks have finite $k_{\max}$ and therefore finite, if small, thresholds.
- **Units of $\lambda$.** Here $\lambda$ is a per-edge rate ratio. Papers that normalise infection per node rather than per edge get different-looking thresholds. *Comment:* always check the convention before comparing numbers.
- **The immunisation results are HMF and SIS** unless stated. Acquaintance immunisation was analysed by Cohen et al. as a percolation problem on uncorrelated networks, which is the SIR setting.

## Connections

- **NETS 5116.**
  - Barabási's spreading chapter ([chapter notes](../nets-5116/barabasi/10-spreading-phenomena.md)) presents this same degree-block calculation.
  - The robustness chapter ([chapter notes](../nets-5116/barabasi/08-network-robustness.md)) has the same $\langle k^2\rangle/\langle k\rangle$ controlling the Molloy–Reed criterion and the vanishing percolation threshold. That is not a coincidence: SIR *is* bond percolation.
  - Targeted immunisation is the epidemic analogue of attack vulnerability.
- **NETS 6116.** $P(k'\mid k)$ is exactly the 2k statistic of the dk-series. HMF's predictions are therefore those of the maximally random graph with given joint degree distribution.
- **PHYS 7335.**
  - The degree-class bookkeeping comes from the [degree-block formalism](./01-degree-block-formalism.md).
  - The homogeneous limit is the [compartmental-model](./03-compartmental-models.md) threshold $R_0 = 1$, and $C_{kk'}$ plays the role of a next-generation matrix ([thresholds and NGMs](./04-thresholds-and-ngm.md)).
  - The exact SIR threshold comes from [SIR–percolation](./07-sir-percolation.md).
  - The quenched corrections are on the [quenched mean-field](./06-quenched-mean-field.md) page.
- **NETS 7332.** The edge-biased distribution $kP(k)/\langle k\rangle$ that drives $\Theta$ is the same one behind the random-walk stationary distribution $\propto k$ on the [link analysis](../nets-7332/basics/02-link-analysis.md) page. It is also why acquaintance and random-walk immunisation find hubs without global information.

## Self-test

:::{dropdown} Q1. Derive $\lambda_c = \langle k\rangle/\langle k^2\rangle$ from the HMF self-consistency equation.
The stationary state has $\rho_k = \lambda k\Theta/(1+\lambda k\Theta)$ and $\Theta = f(\Theta) = \langle k\rangle^{-1}\sum_k kP(k)\,\rho_k(\Theta)$. Since $f(0) = 0$, $f$ is concave and $f(1) < 1$, a non-zero fixed point exists iff $f'(0) = \lambda\langle k^2\rangle/\langle k\rangle > 1$.
:::

:::{dropdown} Q2. Why does $\Theta$ weight infected nodes by $k'P(k')/\langle k\rangle$ rather than by $P(k')$?
$\Theta$ is the probability that the node at the end of a random **edge** is infected, and an edge reaches a degree-$k'$ node with probability proportional to $k'$. The weighting is what makes hubs dominate transmission.
:::

:::{dropdown} Q3. What is $\lambda_c$ with degree correlations, and can disassortative mixing restore a finite threshold on a network with $\gamma = 2.5$?
$\lambda_c = 1/\Lambda_m$, with $\Lambda_m$ the largest eigenvalue of $C_{kk'} = kP(k'\mid k)$. No: for unstructured networks obeying detailed balance, a diverging $\langle k^2\rangle$ is sufficient for $\Lambda_m \to \infty$ (Boguñá, Pastor-Satorras & Vespignani 2003). Correlations change the value on finite networks, not the limit.
:::

:::{dropdown} Q4. Give the three SIR thresholds and say what each one assumes.
- $\langle k\rangle/\langle k^2\rangle$: annealed HMF, where every edge is available.
- $\langle k\rangle/(\langle k^2\rangle - \langle k\rangle)$: static HMF, where the edge to the infector can't be reused, so a node uses $k'-1$ edges.
- $\langle k\rangle/(\langle k^2\rangle - 2\langle k\rangle)$: exact on locally tree-like static networks with exponential recovery times. It follows from the bond-percolation threshold $T_c = \langle k\rangle/(\langle k^2\rangle - \langle k\rangle)$ with $T = \lambda/(1+\lambda)$, i.e. $\lambda_c = T_c/(1-T_c)$.
:::

:::{dropdown} Q5. The BA network has no threshold. Why is this "bad news balanced by good news"?
For any $\lambda > 0$, the infection persists in the infinite network. But the prevalence $\rho \simeq 2e^{-1/(m\lambda)}$ is exponentially small for small $\lambda$. That explains computer viruses that persist at low levels without ever growing explosively, the PRL's original motivation.
:::

:::{dropdown} Q6. Why does random immunisation fail on scale-free networks, and why does acquaintance immunisation work without knowing anyone's degree?
Random immunisation of a fraction $g$ rescales $\lambda \to \lambda(1-g)$, so it needs $\lambda(1-g) < \lambda_c \to 0$, i.e. $g_c \to 1$. A random acquaintance of a random node is reached by following an edge, so its degree is distributed as $kP(k)/\langle k\rangle$. Immunising acquaintances therefore preferentially removes the hubs that make $\langle k^2\rangle$ large.
:::

:::{dropdown} Q7. When is HMF expected to be accurate, and what replaces it on a static network?
It is accurate when the network rewires much faster than the epidemic (annealed limit), and qualitatively for SIR on locally tree-like static networks. On static networks with SIS, use individual-based (quenched) mean-field, where $\lambda_c \approx 1/\Lambda_1$ of the adjacency matrix, or exact percolation / message-passing methods for SIR.
:::

---
title: The SIR–Percolation Mapping and Generating Functions
short_title: SIR and percolation
subject: PHYS 7335 · Topic
description: How the final state of an SIR epidemic on a network maps onto bond percolation, what generating functions then give exactly (threshold, outbreak sizes, epidemic size), and where the mapping breaks.
tags: [sir, percolation, generating-functions, transmissibility, epidemic-threshold, configuration-model]
---

:::{tip} TL;DR
- The **final state** of an SIR outbreak is static. Mark each edge across which infection *would* pass with probability $T$, the **transmissibility**. The set ever infected from a seed is then exactly the cluster of the seed in **bond percolation** with occupation probability $T$. Here $T = 1 - e^{-\beta\tau}$ for a fixed infectious period $\tau$, and $T = \beta/(\beta+\mu)$ for exponentially distributed periods.
- On a configuration-model network the occupied-edge generating functions are $G_0(1 + (x-1)T)$ and $G_1(1 + (x-1)T)$. They give everything in closed form:
  - mean outbreak size $\langle s\rangle = 1 + \dfrac{T G_0'(1)}{1 - T G_1'(1)}$
  - threshold $T_c = \dfrac{1}{G_1'(1)} = \dfrac{\langle k\rangle}{\langle k^2\rangle - \langle k\rangle}$
  - epidemic size $S = 1 - G_0(1 - T + Tu)$, where $u = G_1(1 - T + Tu)$
- **Heavy tails kill the threshold.** For $p_k \sim k^{-\gamma}$ with $\gamma \le 3$, $\langle k^2\rangle \to \infty$ as the cutoff grows, so $T_c \to 0$. This is the same mechanism as the Molloy–Reed robustness of scale-free networks. In rates, the exact SIR threshold is $\lambda_c = \langle k\rangle / (\langle k^2\rangle - 2\langle k\rangle)$. That is *above* both mean-field estimates, $\langle k\rangle/\langle k^2\rangle$ and $\langle k\rangle/(\langle k^2\rangle - \langle k\rangle)$.
- **The mapping is not exact when infectious periods vary** (Kenah & Robins 2007). Edges out of one infector are then correlated through its $\tau_i$. Bond percolation still gives the right $T_c$, the right $\langle s\rangle$ below threshold and the right **final size**. It gives the wrong outbreak-size distribution and the wrong **probability of an epidemic**, which is then strictly *smaller* than the final size. The correct object is a semi-directed *epidemic percolation network*.
- **Random vaccination** of a fraction $g$ adds site percolation on top. The epidemic is stopped when $g > 1 - T_c/T$.
:::

- **Source.** [](doi:10.1103/PhysRevE.66.016128) (Newman, *Spread of epidemic disease on networks*, PRE 66, 016128, 2002; preprint arXiv:cond-mat/0205009). [](doi:10.1103/PhysRevE.76.036113) (Kenah & Robins, *Second look at the spread of epidemics on networks*, PRE 76, 036113, 2007). [](doi:10.1103/RevModPhys.87.925) (Pastor-Satorras, Castellano, Van Mieghem & Vespignani, *Epidemic processes in complex networks*, Rev. Mod. Phys. 87, 925, 2015; §IV.C and §V.B.4).
- **Builds on.** Generating functions for random graphs and the Molloy–Reed criterion ([Barabási ch. 8 notes](../nets-5116/barabasi/08-network-robustness.md)); the giant component of ER graphs ([Barabási ch. 3 notes](../nets-5116/barabasi/03-random-networks.md)); homogeneous SIR and its final-size relation ([Compartmental models](./03-compartmental-models.md)).
- **Notation.** Shared symbols as in [](#notation): $p_k$, $G_0$, $G_1$, $u$, $\beta$ (transmission rate per edge), $\mu$ (recovery rate), $\lambda = \beta/\mu$. Page-specific symbols:
  - $T$: transmissibility.
  - $\tau_i$: infectious period of node $i$.
  - $S$: final **epidemic size**, the fraction of nodes ever infected in a large outbreak. It is *not* the susceptible compartment; compartment densities are written $s, i, r$.
  - $P_\infty$: probability that a single seed causes an epidemic.
  - $\langle s\rangle$: mean size of finite outbreaks.

(sec-sirperc-setup)=
## Setup and definitions

The process is a stochastic SIR model on a fixed contact network. An infective $i$ makes infectious contacts along each of its edges at rate $\beta_{ij}$ and stays infective for a time $\tau_i$, after which it is removed. Infection passes only if the contacted node is still susceptible.

:::{prf:definition} Transmissibility
:label: def-sirperc-transmissibility

The probability that $i$ transmits to a given neighbour $j$ before $i$ recovers is $T_{ij} = 1 - e^{-\beta_{ij}\tau_i}$; in discrete time it is $1 - (1-\beta_{ij})^{\tau_i}$. The **transmissibility** is its average over the distributions of rates and periods (Newman eq. 5):

$$
T = \langle T_{ij} \rangle = 1 - \int_0^\infty \!\! \int_0^\infty d\beta\, d\tau \; Q(\beta)\, P(\tau)\, e^{-\beta\tau}.
$$ (eq-sirperc-T)

Two cases matter in practice. With a fixed period $\tau$ and a fixed rate $\beta$, $T = 1 - e^{-\beta\tau}$. With a fixed rate and exponential periods of mean $1/\mu$ (the Markovian SIR), $T = \beta/(\beta + \mu) = \lambda/(1+\lambda)$.
:::

:::{prf:definition} Configuration-model generating functions
:label: def-sirperc-pgf

For a network drawn uniformly at random with degree distribution $p_k$:

$$
G_0(x) = \sum_k p_k x^k, \qquad G_1(x) = \frac{G_0'(x)}{G_0'(1)} = \sum_k q_k x^k,
$$

where $q_k = (k+1)p_{k+1}/\langle k\rangle$ is the **excess degree** distribution: the number of *other* edges at the end of a randomly chosen edge. Note that $G_0'(1) = \langle k \rangle$ and $G_1'(1) = (\langle k^2\rangle - \langle k\rangle)/\langle k\rangle$.
:::

:::{prf:definition} Bond percolation and clusters
:label: def-sirperc-bond

In **bond percolation** with occupation probability $T$, each edge is independently *occupied* with probability $T$. The **cluster** of a node is the set reachable from it along occupied edges. Above a threshold one cluster, the **giant component**, contains a non-zero fraction of all nodes as $N \to \infty$.
:::

## Core ideas

### Why the final state is a percolation cluster

Picture an outbreak from one seed and mark every edge along which infection passes. An edge $i \to j$ is marked only if $i$ is infected and makes an infectious contact with $j$ before recovering. Whether $j$ was still susceptible decides whether the contact *matters*, not whether it *would have occurred*.

So pre-sample, for every edge, whether it *would* transmit if its tail were infected. The outbreak is then just the set reachable from the seed through such edges. If those edge variables are independent with probability $T$, the outbreak is the seed's bond-percolation cluster (Newman §II; the mapping goes back to Grassberger 1983 and earlier, per the RMP review §V.B.4).

Two consequences follow immediately:
- **Only $T$ matters.** Time courses, latent periods and infectivity profiles all drop out of the final state. An SEIR model with the same $T$ has the same final-size statistics.
- **Not every outbreak above threshold is an epidemic.** A seed in a finite cluster gives a small outbreak even when $T > T_c$. This contrasts with the deterministic fully mixed model, where every introduction above threshold grows.

### Thinning a degree distribution

If a node has $k$ edges and each is occupied independently with probability $T$, the number of occupied edges is $\mathrm{Binomial}(k, T)$. Averaging over $p_k$ (Newman eq. 13):

$$
G_0(x;T) = \sum_k p_k \sum_{m=0}^k \binom{k}{m} T^m (1-T)^{k-m} x^m = \sum_k p_k (1 - T + Tx)^k = G_0\big(1 + (x-1)T\big),
$$ (eq-sirperc-thin)

and likewise $G_1(x;T) = G_1(1 + (x-1)T)$ for the occupied excess edges. In particular $G_0'(1;T) = T\langle k\rangle$ and $G_1'(1;T) = T\,G_1'(1)$.

### Outbreak sizes from self-consistency

Let $H_1(x;T)$ generate the size of the cluster reached by following a random edge, and $H_0(x;T)$ the size of the cluster of a random node. On a locally tree-like network the finite clusters contain no loops, so (Newman eqs. 17–18):

$$
H_1(x;T) = x\, G_1\big(H_1(x;T); T\big), \qquad H_0(x;T) = x\, G_0\big(H_1(x;T); T\big).
$$ (eq-sirperc-H)

The full distribution $P_s$ of finite outbreak sizes comes from the Taylor coefficients of $H_0$. Newman recommends extracting them numerically with the Cauchy contour integral over the unit circle, rather than by repeated differentiation.

### Three thresholds for the same SIR model

For the Markovian SIR, three standard approximations give three different thresholds in $\lambda = \beta/\mu$ (RMP eqs. 50, 57 and 62):

| Approach | $\lambda_c$ | What it assumes |
|---|---|---|
| Annealed degree-based mean field | $\dfrac{\langle k\rangle}{\langle k^2\rangle}$ | Edges are reshuffled constantly, so an infected node may re-infect its own infector's degree class. |
| Degree-based mean field on a static tree | $\dfrac{\langle k\rangle}{\langle k^2\rangle - \langle k\rangle}$ | One edge of each newly infected node is "used up" by its infector. |
| Percolation, exact on locally tree-like static networks | $\dfrac{\langle k\rangle}{\langle k^2\rangle - 2\langle k\rangle}$ | As above, but each edge transmits *at most once*, with probability $T = \lambda/(1+\lambda)$, because recovery competes with transmission. |

*My reading of the gap:* the mean-field equations let an edge carry an expected $\lambda = \beta/\mu$ transmissions, counting repeated contacts along the same edge, where a real edge can infect its end node at most once, with probability $\lambda/(1+\lambda) < \lambda$. All three vanish as $\langle k^2\rangle \to \infty$, so the qualitative heterogeneous-network conclusion is robust. For finite $\langle k^2\rangle$ the mean-field theories *underestimate* the threshold. The heterogeneous mean-field derivation is on [Heterogeneous mean-field epidemics](./05-heterogeneous-mean-field.md).

(sec-sirperc-results)=
## Key results

:::{prf:theorem} Mean outbreak size and the epidemic threshold
:label: thm-sirperc-threshold

Below threshold, the mean outbreak size started by a random seed is (Newman eq. 22)

$$
\langle s \rangle = 1 + \frac{T\, G_0'(1)}{1 - T\, G_1'(1)}.
$$ (eq-sirperc-mean)

It diverges at the **critical transmissibility** (Newman eq. 23)

$$
T_c = \frac{1}{G_1'(1)} = \frac{G_0'(1)}{G_0''(1)} = \frac{\langle k\rangle}{\langle k^2\rangle - \langle k\rangle}.
$$ (eq-sirperc-Tc)

For $T = 1$ this is the Molloy–Reed condition for a giant component, $\langle k^2\rangle > 2\langle k\rangle$.
:::

:::{dropdown} Derivation
Differentiate {eq}`eq-sirperc-H` at $x = 1$, using the fact that every generating function equals 1 there.

- **Edge cluster.** $H_1'(1) = 1 + G_1'(1;T)\, H_1'(1)$, so $H_1'(1) = 1/(1 - T G_1'(1))$.
- **Node cluster.** $H_0'(1) = 1 + G_0'(1;T)\, H_1'(1) = 1 + T G_0'(1)/(1 - T G_1'(1))$.

$H_1'(1)$ is finite only while $T G_1'(1) < 1$. *Interpretation (my note):* $T G_1'(1)$ is the mean number of new infections caused by a node infected *along an edge*. It is the branching factor of the outbreak tree, i.e. the network $R_0$.
:::

:::{prf:theorem} Epidemic size above threshold
:label: thm-sirperc-size

For $T > T_c$, let $u$ be the probability that an edge does *not* lead into the giant cluster: the smallest root in $[0,1)$ of

$$
u = G_1(u; T) = G_1(1 - T + Tu).
$$ (eq-sirperc-u)

Then the epidemic size is (Newman eqs. 25–26)

$$
S = 1 - G_0(u;T) = 1 - G_0(1 - T + Tu).
$$ (eq-sirperc-S)

A node of degree $k$ is infected with probability $1 - v^k$, where $v = 1 - T + Tu$. Infected nodes therefore have higher mean degree than uninfected ones (Newman eqs. 27–28).
:::

:::{dropdown} Derivation
Above threshold, {eq}`eq-sirperc-H` still holds for the *finite* clusters, but $H_0(1;T)$ now sums only to the probability of being in a finite cluster, which is $1 - S$.

Set $u = H_1(1;T)$. Evaluating {eq}`eq-sirperc-H` at $x = 1$ gives $u = G_1(u;T)$ and $1 - S = G_0(u;T)$.

The edge from a node is "safe" with probability $v = (1-T) + Tu$: either it is unoccupied, or it is occupied but leads to a finite cluster. Hence $P(\text{uninfected} \mid k) = v^k$.

For a Poisson graph, $G_0 = G_1 = e^{\langle k\rangle(x-1)}$, so $u = 1 - S$ and {eq}`eq-sirperc-S` becomes

$$
S = 1 - e^{-\langle k\rangle T S},
$$

the ER giant-component equation with $\langle k\rangle \to T\langle k\rangle$. *My note:* this has the same form as the fully mixed final-size relation $r_\infty = 1 - e^{-R_0 r_\infty}$, with $R_0 = T\langle k\rangle$.
:::

:::{prf:proposition} Heavy tails and the vanishing threshold
:label: prop-sirperc-heavy

For $p_k \propto k^{-\gamma}$ on $k_{\min} \le k \le k_{\max}$:
- If $2 < \gamma < 3$, then $\langle k^2\rangle \sim k_{\max}^{3-\gamma} \to \infty$, so $T_c \to 0$ as $k_{\max} \to \infty$.
- At $\gamma = 3$ the divergence is logarithmic, so $T_c \to 0$ only very slowly.
- For $\gamma > 3$, $T_c$ stays finite.

Near threshold $S \sim (T - T_c)^{\beta_{\mathrm{perc}}}$, with $\beta_{\mathrm{perc}} = 1/(3-\gamma)$ for $\gamma < 3$, $1/(\gamma - 3)$ for $3 < \gamma \le 4$, and $1$ for $\gamma \ge 4$ (Cohen et al. 2002, as summarised in the RMP review, eq. 19).
:::

:::{prf:proposition} Degree-dependent transmissibility can forbid epidemics
:label: prop-sirperc-Tk

Let the transmissibility of a node depend on that node, $T_i$. The epidemic threshold is then (Newman eq. 40)

$$
\sum_i k_i\big[(k_i - 1)T_i - 1\big] = 0,
$$

with epidemics possible when the left side is positive. If $T_k = T_1/k$, an epidemic requires $T_1 > \langle k\rangle/(\langle k\rangle - 1) > 1$. That is impossible, so no epidemic ever occurs, whatever the degree distribution (Newman eq. 47).
:::

:::{dropdown} Derivation
The condition is $G_1'(1;\{T_i\}) = 1$, where $G_1(x;\{T_i\}) \propto \sum_i k_i (1 + (x-1)T_i)^{k_i - 1}$. Differentiating at $x=1$ gives $\sum_i k_i (k_i - 1) T_i = \sum_i k_i$.

Substituting $T_k = T_1/k$ gives $\sum_k p_k[(k-1)T_1 - k] > 0$, i.e. $T_1(\langle k\rangle - 1) > \langle k\rangle$.
:::

:::{prf:theorem} Where bond percolation fails (Kenah & Robins 2007)
:label: thm-sirperc-kr

Let the infectious periods $\tau_i$ be i.i.d. with a non-degenerate distribution. The transmissions from $i$ along its $k_i$ edges are then *conditionally* independent given $\tau_i$, with probability $T_{\tau_i}$, but *marginally* dependent. The SIR model is exactly isomorphic to a semi-directed **epidemic percolation network** (EPN): edge $i \to j$ is present when $i$ would infect $j$. In the large-$N$ limit:

- **Outbreak from $i$** = the out-component of $i$.
- **Epidemic threshold** = the appearance of a giant strongly connected component (GSCC).
- **$P_\infty$, the probability of an epidemic**, = the fraction of nodes in the giant in-component.
- **$S$, the epidemic size**, = the fraction of nodes in the giant out-component.

The in-components of the EPN are distributed exactly like bond-percolation clusters with occupation probability $T$. Bond percolation therefore gives the **correct** $T_c$, $\langle s\rangle$ below threshold and $S$. It gives the **wrong** outbreak-size distribution and the wrong $P_\infty$. In fact $P_\infty \le S$, with equality only if $\tau$ is constant or $P_\infty = 0$.
:::

:::{dropdown} Why, and Newman's original claim
Newman (§II) argued that variation in $\beta_{ij}$ and $\tau_i$ "makes no difference whatsoever": the population behaves as if every edge transmitted with probability $T$. He also stated that above threshold the probability that an outbreak becomes an epidemic equals $S(T)$.

Kenah & Robins give a two-line counterexample. Every node has degree 2, and $\tau = \tau_0$ with probability $p$, else $\tau = 0$. A seed produces no further infections with probability $1 - p + p e^{-2\beta_0\tau_0}$, but bond percolation predicts $(1 - p + p e^{-\beta_0\tau_0})^2$. The two differ by $p(1-p)(1 - e^{-\beta_0\tau_0})^2 > 0$.

The reason is that an infector's period is shared by all its outgoing edges: a long-lived infector tends to infect *all* its neighbours, a short-lived one *none*. Looking *backwards*, however, the edges into a node come from *different* infectors with independent $\tau$'s. That is why in-components (which give final size) are bond-percolation clusters while out-components (which give the probability of a large outbreak) are not. The RMP review adds that the bond approximation is also inexact when $\tau$ is fixed but the $\beta_{ij}$ vary (Miller 2007).
:::

:::{prf:proposition} Random vaccination as site percolation
:label: prop-sirperc-vacc

Vaccinate (remove) each node independently with probability $g$ before the outbreak. On the configuration model the threshold becomes $(1-g)\,T\,G_1'(1) = 1$. So the critical vaccination coverage is

$$
g_c = 1 - \frac{T_c}{T}.
$$

*Derivation sketch (mine; Newman §IV notes that the joint site/bond problem is exactly solvable):* an excess edge now leads to a further infection only if it is occupied (probability $T$) *and* its end node is unvaccinated (probability $1-g$). This replaces $T$ by $T(1-g)$ in {eq}`eq-sirperc-Tc`. For $T_c \to 0$, as on heavy-tailed networks, $g_c \to 1$: random vaccination fails, which is why targeted and acquaintance strategies matter ([Heterogeneous mean-field epidemics](./05-heterogeneous-mean-field.md)).
:::

## Worked example

All numbers below were computed in Python. The scripts solved the self-consistency equations by iteration, built the epidemic percolation network explicitly, and ran BFS over it.

**1. Poisson network, $\langle k\rangle = 4$.** Here $G_1'(1) = 4$, so $T_c = 0.25$. In rate units the three thresholds are 0.200 (annealed mean field), 0.250 (static mean field) and **0.333** (exact).

| $T$ | 0.1 | 0.2 | 0.24 | 0.3 | 0.4 | 0.5 | 0.8 | 1.0 |
|---|---|---|---|---|---|---|---|---|
| $\langle s\rangle$ (below $T_c$) | 1.667 | 5.000 | 25.00 | — | — | — | — | — |
| $S$ (above $T_c$) | 0 | 0 | 0 | 0.314 | 0.642 | 0.797 | 0.953 | 0.980 |

**2. Newman's example.** Take $p_k \propto k^{-2}e^{-k/10}$ for $k \ge 1$. Polylogarithm sums give $\langle k\rangle = 1.793$ and $T_c = 0.329$, matching Newman's 0.329 (his simulations give 0.32(2)). A fully mixed model with the same mean number of contacts would put the threshold at $1/\langle k\rangle = 0.558$, so ignoring heterogeneity overestimates the threshold by a factor of 1.7. With cutoff $\kappa = 5$ the threshold is $T_c = 0.608$; with $\kappa = 20$ it is $0.183$.

**3. Vanishing threshold.** Truncated power laws with $k_{\min} = 2$ give $T_c = \langle k\rangle/(\langle k^2\rangle - \langle k\rangle)$ as follows:

| $k_{\max}$ | $10^2$ | $10^3$ | $10^4$ | $10^5$ |
|---|---|---|---|---|
| $\gamma = 2.5$ | 0.087 | 0.026 | 0.0081 | 0.0026 |
| $\gamma = 3.0$ | 0.179 | 0.110 | 0.079 | 0.062 |
| $\gamma = 3.5$ | 0.318 | 0.283 | 0.273 | 0.270 |

For $\gamma = 2.5$, $T_c$ falls by about $10^{-1/2}$ per decade of $k_{\max}$, as $k_{\max}^{-(3-\gamma)}$ predicts. At $\gamma = 3$ it drifts slowly to zero. At $\gamma = 3.5$ it converges.

**4. Kenah–Robins in action.** I simulated a configuration-model graph with Poisson degrees, $N = 20{,}000$ and $\langle k\rangle = 4.007$, at the same $T = 0.5$ under two infectious-period distributions. Each column used 400 random seeds, and an outbreak counted as an epidemic if it reached more than 2,000 nodes.

| | Theory: $P_\infty$ | Theory: $S$ | Simulation: $P_\infty$ | Simulation: $S$ |
|---|---|---|---|---|
| fixed $\tau$, $\beta\tau = \ln 2$ | 0.797 | 0.797 | 0.810 | 0.800 |
| exponential $\tau$, $\lambda = 1$ | **0.639** | 0.797 | **0.640** | 0.799 |

The final size is the same, because bond percolation is right about in-components. The probability of an epidemic drops from 0.80 to 0.64 once periods vary.

In the exponential case, $P_\infty = 1 - v$, where $v = \int_0^\infty e^{-\langle k\rangle T_\tau (1-v)}\, \mu e^{-\mu\tau}\, d\tau$ is the probability that a node infected through an edge leaves only a finite out-component, and $T_\tau = 1 - e^{-\beta\tau}$. This holds for Poisson degrees, where $G_0 = G_1$; it is my specialisation of the Kenah–Robins out-component equations.

**5. Vaccination.** With $\langle k\rangle = 4$ and $T = 0.5$, random vaccination needs $g_c = 1 - 0.25/0.5 = 0.5$.

## Assumptions and limitations

- **Locally tree-like, uncorrelated networks.** The generating-function solution assumes a configuration-model network with no short loops and no degree correlations. Clustering (short loops) makes paths redundant and generally changes the threshold and the size. Degree correlations need the $P(k'|k)$ generalisation (RMP §VII.B).
- **Static network, single seed, large $N$.** Contacts must not rewire during the outbreak. If they do (the annealed limit), the mean-field thresholds of [Heterogeneous mean-field epidemics](./05-heterogeneous-mean-field.md) apply. "Epidemic" means a non-zero fraction as $N \to \infty$; at finite $N$ the threshold is smeared, as in Newman's simulations.
- **Final state only.** Percolation says nothing about *timing*: peak time, growth rate or duration. Those need dynamic approaches such as edge-based compartmental models or message passing ([Quenched mean field and message passing](./06-quenched-mean-field.md)).
- **SIR only.** The mapping needs permanent removal. SIS has a stationary state and no static percolation analogue; its threshold behaviour on networks is different.
- **Heterogeneous periods.** The probability of an epidemic and the outbreak-size distribution require the epidemic percolation network, not bond percolation (Kenah & Robins).

## Connections

- **NETS 5116.**
  - With $T = 1$ this is the Molloy–Reed / Callaway et al. giant-component calculation ([Barabási ch. 8 notes](../nets-5116/barabasi/08-network-robustness.md)). Random failures there are site percolation, and vaccination is the same mathematics.
  - The Poisson case reproduces the ER giant component with mean degree $T\langle k\rangle$ ([Barabási ch. 3 notes](../nets-5116/barabasi/03-random-networks.md)). The epidemic sections of [Barabási ch. 10](../nets-5116/barabasi/10-spreading-phenomena.md) present the mean-field side of the same story.
- **PHYS 7335.**
  - The fully mixed final-size relation ([Compartmental models](./03-compartmental-models.md)) is the Poisson special case.
  - The heterogeneous mean-field threshold ([Heterogeneous mean-field epidemics](./05-heterogeneous-mean-field.md)) agrees qualitatively but sits below the exact one.
  - On networks with loops or localisation, the threshold is governed by spectral quantities such as the non-backtracking matrix ([Quenched mean field and message passing](./06-quenched-mean-field.md)).
  - $T\,G_1'(1)$ is the network $R_0$ that next-generation arguments compute ([Thresholds and next-generation matrices](./04-thresholds-and-ngm.md)).
- **NETS 6116.** The configuration model is the maximum-entropy ensemble for a degree sequence. The tree-like assumption here is exactly its sparse-limit property.
- **NETS 7332.** Directed in- vs out-components are the same objects as in PageRank's reachability analysis ([Link analysis](../nets-7332/basics/02-link-analysis.md)).

## Self-test

:::{dropdown} Q1. Why can the final state of SIR be mapped to percolation, but not the state of SIS?
In SIR every node is infected at most once, and the final infected set is determined by which edges *would* transmit, which is a static random subgraph. In SIS nodes are reinfected repeatedly and the process reaches a dynamic stationary state, so there is no single static subgraph whose clusters give it.
:::

:::{dropdown} Q2. Derive $G_0(x;T) = G_0(1 + (x-1)T)$.
A degree-$k$ node has $\mathrm{Binomial}(k, T)$ occupied edges, with generating function $(1 - T + Tx)^k$. Averaging over $p_k$ gives $\sum_k p_k (1 - T + Tx)^k = G_0(1 - T + Tx)$.
:::

:::{dropdown} Q3. Give $T_c$ for a configuration model, and explain why it goes to zero on scale-free networks.
$T_c = 1/G_1'(1) = \langle k\rangle/(\langle k^2\rangle - \langle k\rangle)$. For $p_k \sim k^{-\gamma}$ with $\gamma \le 3$, $\langle k^2\rangle$ diverges with the cutoff. An edge then leads to a node with a huge expected number of further edges, so any $T > 0$ gives a branching factor $T\,G_1'(1) > 1$.
:::

:::{dropdown} Q4. For Markovian SIR, order the three thresholds $\langle k\rangle/\langle k^2\rangle$, $\langle k\rangle/(\langle k^2\rangle - \langle k\rangle)$ and $\langle k\rangle/(\langle k^2\rangle - 2\langle k\rangle)$, and say what each neglects.
They increase in that order.
- **Annealed mean field** neglects that a new infective's infector is already infected.
- **Static-tree mean field** fixes that, but still lets an edge carry an expected $\lambda$ transmissions.
- **Exact percolation** caps each edge at one transmission, with probability $T = \lambda/(1+\lambda)$, so recovery can beat transmission.
:::

:::{dropdown} Q5. When infectious periods vary, which outbreak quantities does bond percolation still predict correctly, and which not?
- **Correct:** $T_c$, the mean outbreak size below threshold, and the final epidemic size $S$. All of these depend on in-components, or on means equal for in- and out-components.
- **Wrong:** the outbreak-size distribution and the probability of an epidemic $P_\infty$, which depend on out-components. Here $P_\infty < S$.
:::

:::{dropdown} Q6. Why does $T_k = T_1/k$ prevent epidemics on any network?
The threshold condition becomes $T_1(\langle k\rangle - 1) > \langle k\rangle$, i.e. $T_1 > \langle k\rangle/(\langle k\rangle - 1) > 1$. A probability can't exceed 1. Each infective's total expected transmissions, $k T_k = T_1$, are capped below what's needed to sustain a branching process.
:::

:::{dropdown} Q7. A disease has $T = 0.4$ on a network with $\langle k\rangle = 3$ and $\langle k^2\rangle = 15$. What fraction must be randomly vaccinated?
$T_c = 3/(15 - 3) = 0.25$, so $g_c = 1 - 0.25/0.4 = 0.375$.
:::

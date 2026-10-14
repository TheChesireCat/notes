---
title: Configuration Models (CM, SCM, HSCM) and the SCM Equations
short_title: Configuration models
subject: NETS 6116 · Topic
description: The three maximum-entropy ensembles with a given degree sequence (hard, soft, hypersoft), how to count and sample them, the Chung–Lu limit, and when the soft-configuration-model equations have a unique solution.
tags: [configuration-model, soft-configuration-model, maximum-entropy, degree-sequence, chung-lu, hscm, erdos-gallai, beta-model]
---

:::{tip} TL;DR
- **The configuration models are the maximum-entropy ensembles constrained by degrees.** There are three, mirroring $G(N,L)$, $G(N,p)$ and hypergeometric ER:
  - **CM** (microcanonical) is uniform over simple graphs with degree sequence exactly $\mathbf{k}$.
  - **SCM** (canonical) fixes only the *expected* degrees.
  - **HSCM** (hypercanonical) draws $\mathbf{k}$ from a distribution $\rho$ first.
- **The SCM has independent edges with Fermi–Dirac probabilities.** $p_{ij} = 1/(e^{\lambda_i+\lambda_j}+1)$, where the $N$ Lagrange multipliers solve $\sum_{j} p_{ij} = k_i$. Its **classical (sparse) limit** is Chung–Lu, $p_{ij} \approx k_ik_j/(N\langle k\rangle)$. Every graph with the same degree sequence has the same SCM probability, so conditioning the SCM on $\mathbf{k}(G) = \mathbf{k}$ gives back the CM.
- **The CM is hard to count and to sample.** The count is $\lvert\mathcal{G}_N(\mathbf{k})\rvert = \frac{(2L-1)!!}{\prod_i k_i!}\,\mathcal{P}_{\text{simple}}$. Bender–Canfield gives $\mathcal{P}_{\text{simple}} \approx \exp[-(\kappa^2-1)/4]$ with $\kappa = \langle k^2\rangle/\langle k\rangle$. This tends to $0$ when $\langle k^2\rangle$ diverges, so rejection sampling fails on scale-free sequences. That leaves the erased CM, edge-swap MCMC (started from Havel–Hakimi), or exact samplers.
- **The SCM equations are the stationarity conditions of a strictly convex potential.** The potential $\mathcal{F}(\boldsymbol\lambda) = \sum_{i<j}\ln(1+e^{-\lambda_i-\lambda_j}) + \sum_i k_i\lambda_i$ is the negative log-likelihood of the $\beta$-model, and its minimum equals the SCM entropy. Hence **at most one solution** (for $N \ge 3$). A solution **exists iff $\mathbf{k}$ lies in the interior of the degree-sequence polytope**. The condition $k_i \in (0, N-1)$ alone is *not* enough.
- **The HSCM gives a power law with no hard cutoff.** With i.i.d. Pareto hidden degrees ($\gamma > 2$), it is the unbiased (max-entropy) sparse power-law ensemble. Its degrees are mixed-Poisson, and four equivalent generators exist ($\lambda$, $k$, $u$, $x$). At $\gamma = 3$ it is equivalent to *soft* preferential attachment.
:::

- **Source.** Krioukov, *Network Science II* lecture notes, ch. 9 (Configuration model) and appendix A / ch. 15 (Existence and uniqueness of the solution of the SCM equations, by L. Santagata). Primary papers:
  - Bender & Canfield, [](doi:10.1016/0097-3165(78)90059-6) (1978), and Wormald's ICM survey, [](doi:10.1142/9789813272880_0180) (2018): counting.
  - Park & Newman, [](doi:10.1103/PhysRevE.70.066117) (2004): maximum-entropy derivation.
  - Chung & Lu, [](doi:10.1007/PL00012580) (2002): expected-degree model.
  - Chatterjee, Diaconis & Sly, [](doi:10.1214/10-AAP728) (2011): existence of the solution, via the $\beta$-model.
  - van der Hoorn, Lippner & Krioukov, [](doi:10.1007/s10955-017-1887-7) (2018): HSCM.
- **Builds on.** [Typicality and maximum-entropy models](./04-typicality-and-max-entropy.md) (microcanonical / canonical / hypercanonical ensembles, Lagrange multipliers), the configuration-model section of [Barabási ch. 4](../nets-5116/barabasi/04-scale-free-networks.md), and [power laws](./03-binning-and-power-laws.md) (Pareto).
- **Notation.** Shared symbols as in [](#notation); $N$, $L$, $\langle k\rangle$ replace Krioukov's $n$, $m$, $\bar k$.
  - **Degree constraints.** $\mathbf{k} = (k_1,\dots,k_N)$ is the target degree sequence. $k_i(G)$ is the degree of node $i$ in graph $G$; Krioukov writes $d_i(G)$. $\mathcal{G}_N(\mathbf{k})$ is the set of simple graphs on $N$ labelled nodes with degree sequence $\mathbf{k}$, and $\Omega(\mathbf{k}) = \lvert\mathcal{G}_N(\mathbf{k})\rvert$; Krioukov writes $N(n,\mathbf{k})$, which would clash with $N$ here.
  - **SCM variables.** $\lambda_i$ are SCM Lagrange multipliers (**not** the spreading rate), and $q_{ij} = e^{-\lambda_i-\lambda_j}$.
  - **HSCM parameters.** $\alpha = \gamma-1$ (**not** Newman's degree exponent), $\nu$ and $R$ are the HSCM constants, and $\rho$ is the hidden-degree density (**not** prevalence).
  - **$\kappa$.** Without a subscript, $\kappa = \langle k^2\rangle/\langle k\rangle$ as in [](#notation).

(sec-cm-setup)=
## Setup and definitions

Ch. 8 of the notes builds unbiased ensembles by maximising entropy subject to a constraint on a *sufficient statistic*. Here that statistic is the degree. Each choice of constraint type and statistic gives one model:

| Ensemble type | Statistic: mean degree $\langle k\rangle$ | Statistic: degree sequence $\mathbf{k}$ |
|---|---|---|
| Microcanonical (hard) | $G(N,L)$, $L = \tfrac12\langle k\rangle N$ | $\mathrm{CM}(N,\mathbf{k})$ |
| Canonical (soft) | $G(N,p)$, $p = \langle k\rangle/(N-1)$ | $\mathrm{SCM}(N,\mathbf{k})$ |
| Hypercanonical (hypersoft) | $G(N,\rho)$: ER with random $\langle k\rangle \sim \rho$ | $\mathrm{HSCM}(N,\rho)$, $\mathbf{k}\sim\rho$ |

:::{prf:definition} Configuration model
:label: def-cm-cm

For a graphical $\mathbf{k}$, $\mathrm{CM}(N,\mathbf{k})$ is the uniform distribution on $\mathcal{G}_N(\mathbf{k})$:

$$
P_{\mathrm{CM}}(G \mid N,\mathbf{k}) = \frac{\mathbb{1}\{G \in \mathcal{G}_N(\mathbf{k})\}}{\Omega(\mathbf{k})}.
$$ (eq-cm-cm)

$\mathbf{k}$ is **graphical** if $\Omega(\mathbf{k}) > 0$. In the space of simple graphs this is the max-entropy distribution under the hard constraint $k_i(G) = k_i$ for all $i$, and its entropy is $\ln\Omega(\mathbf{k})$.
:::

:::{prf:definition} Soft configuration model
:label: def-cm-scm

$\mathrm{SCM}(N,\mathbf{k})$ is the exponential (Gibbs) distribution on all simple graphs $\mathcal{G}_N$ with one Lagrange multiplier per node:

$$
P_{\mathrm{SCM}}(G \mid N,\mathbf{k}) = \frac{1}{Z}\exp\Big(-\sum_{i=1}^N \lambda_i\,k_i(G)\Big),
$$ (eq-cm-scm-gibbs)

with $\boldsymbol\lambda$ chosen so that $\mathbb{E}[k_i(G)] = k_i$ for every $i$. It maximises $H[P]$ subject to these $N$ soft constraints. The $k_i$ may be any reals, not only integers.
:::

:::{prf:definition} Hypersoft configuration model
:label: def-cm-hscm

$\mathrm{HSCM}(N,\rho)$ is the mixture: draw $\mathbf{k} \sim \rho$, then $G \sim \mathrm{SCM}(N,\mathbf{k})$. In the usual setting, $\rho(\mathbf{k}) = \prod_i \rho(k_i)$, so the hidden degrees are i.i.d. draws from a fixed one-dimensional $\rho$ (e.g. Pareto). The notes' Definition 9.6 writes "$\mathrm{HSCM}(n,\mathbf{k})$ where $\mathbf{k}\sim\rho$", which should read $\mathrm{SCM}$.
:::

Why a hypersoft model at all? Real degree *sequences* churn as networks evolve, but the degree *distribution* is often stable for decades; the notes give the Internet as an example. So the stable object is $\rho$, not $\mathbf{k}$, and $\rho$ is what the ensemble should fix.

(sec-cm-core)=
## Core ideas

### Counting the CM: stubs, pairings and simplicity

Give node $i$ exactly $k_i$ half-edges (**stubs**), $2L = \sum_i k_i$ in total. A uniform random perfect matching of the stubs is the classical **pairing model** (Bollobás; Molloy & Reed, [](doi:10.1002/rsa.3240060204)). Counting pairings and quotienting by stub relabellings gives

$$
\Omega(\mathbf{k}) = \frac{N_p}{N_s}\,\mathcal{P}_{\text{simple}},\qquad N_p = \frac{(2L)!}{L!\,2^L} = (2L-1)!!,\qquad N_s = \prod_{i=1}^N k_i!,
$$ (eq-cm-count)

- $N_p$ counts pairings: all $(2L)!$ orderings, divided by the $L!$ orders of the pairs and the $2^L$ orders within pairs.
- Every *simple* graph in $\mathcal{G}_N(\mathbf{k})$ arises from exactly $N_s$ pairings, since the stubs at each node can be permuted freely.
- $\mathcal{P}_{\text{simple}}$ is the probability that a uniform pairing produces no self-loop and no multi-edge.

Conditioned on being simple, the pairing model is exactly uniform on $\mathcal{G}_N(\mathbf{k})$. All the difficulty sits in $\mathcal{P}_{\text{simple}}$: results are asymptotic and need conditions on $\mathbf{k}$ (see [](#thm-cm-bender-canfield)).

### Generating the CM

The notes list four families of samplers. Generation is hard for the same reason counting is: rejection works only when $\mathcal{P}_{\text{simple}}$ is bounded away from $0$.

| Method | Exact uniform on $\mathcal{G}_N(\mathbf{k})$? | Cost / caveat |
|---|---|---|
| **Pair stubs, reject if not simple** | Yes | Expected $1/\mathcal{P}_{\text{simple}}$ restarts. Fails when $\langle k^2\rangle\to\infty$, because $\mathcal{P}_{\text{simple}}\to 0$ (Janson, [](doi:10.1017/S0963548308009644)). Without rejection it is the CM of *multigraphs*. |
| **Pair stubs, erase loops and multi-edges** (erased CM) | No: the realised degrees fall below $\mathbf{k}$ | Negligible "for many purposes", per van der Hofstad, [](doi:10.1017/9781316779422). The deficit concentrates on hubs. |
| **Degree-preserving edge swaps** ($ab, cd \to ad, cb$; reject if it creates a loop or multi-edge) | Asymptotically, if the chain is symmetric | Start from a Havel–Hakimi graph. $O(L)$ swaps is the *empirical* mixing rule the notes cite (Kim, Toroczkai, Erdős, Miklós & Székely, [](doi:10.1088/1751-8113/42/39/392001)). Rigorous bounds are only polynomial, e.g. Cooper, Dyer & Greenhill, [](doi:10.1017/S0963548306007978), for regular graphs. "Done properly" means a rejected move counts as a step. Choosing only among *valid* moves biases the chain (Coolen, De Martino & Annibale, [](doi:10.1007/s10955-009-9821-2)). |
| **Exact/importance samplers** | Del Genio, Kim, Toroczkai & Bassler ([PLoS ONE 5, e10012, 2010](https://doi.org/10.1371/journal.pone.0010012)): weighted (non-uniform) samples with known weights. Arman, Gao & Wormald [](doi:10.1109/FOCS.2019.00084): exactly uniform. | Arman–Gao–Wormald runs in expected time $O(L)$ if $k_{\max}^4 = O(L)$, which is $\gamma > 5$ for power laws. It is linear for power laws with $\gamma > (21+\sqrt{61})/10 \approx 2.88$. The notes call it the state of the art. |

**Havel–Hakimi** (Havel 1955; Hakimi, [](doi:10.1137/0110037)). This constructs one graph with degree sequence $\mathbf{k}$, or proves none exists:
1. Sort the sequence in non-increasing order.
2. Connect the node with the most remaining stubs, $s$, to the next $s$ nodes with the most remaining stubs.
3. Decrement those $s$ nodes, delete the exhausted node, re-sort and repeat.
4. $\mathbf{k}$ is graphical iff this never asks for more stubs than exist.

### SCM: independent Bernoulli edges with Fermi–Dirac probabilities

For a simple undirected graph, $\sum_i \lambda_i k_i(G) = \sum_{i<j}(\lambda_i+\lambda_j)A_{ij}$. So the Gibbs weight [](#eq-cm-scm-gibbs) **factorises over pairs**, and the partition function is a product:

$$
Z = \prod_{i<j}\big(1+e^{-\lambda_i-\lambda_j}\big),\qquad
P_{\mathrm{SCM}}(G) = \prod_{i<j} p_{ij}^{A_{ij}}(1-p_{ij})^{1-A_{ij}},
$$ (eq-cm-scm-product)

$$
p_{ij} = \frac{q_{ij}}{1+q_{ij}} = \frac{1}{e^{\lambda_i+\lambda_j}+1}.
$$ (eq-cm-scm-p)

Each edge is an independent Bernoulli variable. Its probability has the **Fermi–Dirac** form, with energy $\lambda_i+\lambda_j$ and occupation at most 1, since a pair can carry at most one edge. $G(N,p)$ is the special case $\lambda_i \equiv \lambda$. The multipliers are fixed by matching expected degrees:

$$
\sum_{j \ne i} \frac{1}{e^{\lambda_i+\lambda_j}+1} = k_i,\qquad i = 1,\dots,N.
$$ (eq-cm-scm-eqs)

**To sample:** solve [](#eq-cm-scm-eqs) once, then flip $\binom N2$ independent coins. This costs $O(N^2)$, or $O(N+L)$ with standard tricks for sparse $p_{ij}$.

Two structural facts follow directly from [](#eq-cm-scm-gibbs):
- $P_{\mathrm{SCM}}(G)$ depends on $G$ **only through its degree sequence**. All graphs with the same degree sequence are equiprobable, so conditioning the SCM on $\mathbf{k}(G) = \mathbf{k}$ gives back $\mathrm{CM}(N,\mathbf{k})$.
- In the SCM, degrees *fluctuate*: $k_i(G)$ is a sum of independent Bernoullis, with $\operatorname{Var}k_i(G) = \sum_j p_{ij}(1-p_{ij}) \le k_i$. When the network is sparse, $k_i(G) \approx \mathrm{Poisson}(k_i)$. The relative fluctuation is $\sim k_i^{-1/2}$, which does **not** vanish as $N\to\infty$ at fixed $k_i$. This is the origin of **ensemble non-equivalence** between CM and SCM (Squartini, de Mol, den Hollander & Garlaschelli, [](doi:10.1103/PhysRevLett.115.268701)).

### The SCM as a maximum-likelihood problem

*My observation; the result is standard (Garlaschelli & Loffredo, [](doi:10.1103/PhysRevE.78.015101); Chatterjee, Diaconis & Sly, [](doi:10.1214/10-AAP728)).*

For any observed graph $G^*$ with degree sequence $\mathbf{k}$, the log-likelihood under [](#eq-cm-scm-product) is

$$
-\ln P_{\mathrm{SCM}}(G^* \mid \boldsymbol\lambda) = \sum_{i<j}\ln\big(1+e^{-\lambda_i-\lambda_j}\big) + \sum_i k_i\lambda_i \;=\; \mathcal{F}(\boldsymbol\lambda).
$$ (eq-cm-potential)

So the SCM equations [](#eq-cm-scm-eqs) are the **maximum-likelihood equations of the $\beta$-model**, with $\beta_i = -\lambda_i$. The degree sequence is a sufficient statistic, and the fitted model reproduces the observed degrees in expectation.

$\mathcal{F}$ is linear in $\mathbf{k}$ and $\mathbb{E}[\mathbf{k}(G)] = \mathbf{k}$ at the solution, so $H[P_{\mathrm{SCM}}] = \mathbb{E}[-\ln P(G)] = \mathcal{F}(\boldsymbol\lambda^*) = \min_{\boldsymbol\lambda}\mathcal{F}$. The **SCM entropy is the minimum of the potential**.

### Classical limit: the Chung–Lu model

"Classical" is meant as in statistical physics: Fermi–Dirac occupations become Maxwell–Boltzmann when occupations are small. If $p_{ij} \ll 1$, i.e. $e^{\lambda_i+\lambda_j} \gg 1$, then $p_{ij} \approx e^{-\lambda_i}e^{-\lambda_j}$. Summing gives $k_i \approx e^{-\lambda_i}\sum_j e^{-\lambda_j} =: c\,e^{-\lambda_i}$. Summing again gives $c^2 = \sum_i k_i = N\langle k\rangle$, so

$$
p_{ij} \approx p_{ij}^{\mathrm{CL}} = \min\!\Big(1,\ \frac{k_ik_j}{N\langle k\rangle}\Big),\qquad e^{-\lambda_i} \approx \frac{k_i}{\sqrt{N\langle k\rangle}}.
$$ (eq-cm-chung-lu)

This is the Chung–Lu (expected-degree) model, [](doi:10.1007/PL00012580). It is also Barabási's "hidden parameter" model ([ch. 4](../nets-5116/barabasi/04-scale-free-networks.md)), and it is the edge probability that underlies the uncorrelated $P(k'\mid k) = k'p_{k'}/\langle k\rangle$ of [degree-block mean-field theory](../phys-7335/01-degree-block-formalism.md).

- **The approximation can fail even when degrees are modest.** The truncation at $1$ binds when $k_ik_j > N\langle k\rangle$, i.e. for pairs of nodes above the **structural cutoff** $k_s \sim \sqrt{N\langle k\rangle}$ ([Barabási ch. 7](../nets-5116/barabasi/07-degree-correlations.md)). Truncating removes edges among hubs and so creates disassortativity. The exact SCM saturates smoothly instead.
- **Janson** ([](doi:10.1002/rsa.20297)) shows that CL, SCM and several related rank-1 models are *asymptotically equivalent* (contiguous) under $\sum_{i<j}p_{ij}^2 \to 0$-type conditions. This is the precise sense of "in many other cases" in the notes.

(sec-cm-results)=
## Key results

:::{prf:theorem} Erdős–Gallai
:label: thm-cm-erdos-gallai

A non-increasing sequence $k_1 \ge \dots \ge k_N \ge 0$ of integers is graphical iff $\sum_i k_i$ is even and, for every $j = 1,\dots,N$,

$$
\sum_{i=1}^j k_i \;\le\; j(j-1) + \sum_{i=j+1}^N \min(k_i, j).
$$ (eq-cm-erdos-gallai)
:::

:::{dropdown} Why the inequalities are necessary
The left side counts stub endpoints in the top-$j$ set $S$. Edges inside $S$ use at most $j(j-1)$ of them, because there are at most $\binom j2$ pairs, each with two endpoints. Every other endpoint in $S$ belongs to an edge to some $i \notin S$, and node $i$ can absorb at most $\min(k_i, j)$ such edges. Sufficiency is the hard direction (Erdős & Gallai 1960). Havel–Hakimi gives a constructive alternative.
:::

:::{prf:theorem} Probability that a random pairing is simple (Bender–Canfield)
:label: thm-cm-bender-canfield

For bounded degrees (and, by later work, for broader classes),

$$
\mathcal{P}_{\text{simple}} \;\to\; \exp\!\Big[-\frac{\kappa^2-1}{4}\Big] = e^{-\nu_2/2 - \nu_2^2/4},\qquad \kappa = \frac{\langle k^2\rangle}{\langle k\rangle},\quad \nu_2 = \kappa - 1,
$$ (eq-cm-bender-canfield)

where $\langle k^m\rangle = \frac1N\sum_i k_i^m$.
:::

:::{dropdown} Why, and how to read "≈"
The numbers of self-loops and of double edges in the pairing model are asymptotically independent Poisson variables, with means $\nu_2/2$ and $\nu_2^2/4$:
- A given node $i$ has $\binom{k_i}{2}$ stub pairs, and each is matched with probability $\approx 1/(2L)$. So $\mathbb{E}[\#\text{loops}] \approx \sum_i k_i(k_i-1)/(4L) = \nu_2/2$.
- A similar count over pairs of stub-pairs gives $\nu_2^2/4$ double edges.

$\mathcal{P}_{\text{simple}} = P(\text{both are }0) \to e^{-\nu_2/2}e^{-\nu_2^2/4}$, and $\nu_2/2 + \nu_2^2/4 = ((\nu_2+1)^2-1)/4 = (\kappa^2-1)/4$.

The "$\approx$" is an **asymptotic statement**: the ratio of the two sides tends to $1$ as $N \to \infty$ along a sequence of degree sequences satisfying the theorem's conditions. It is not a bound at finite $N$. Rigorous versions need restrictions on $\mathbf{k}$:
- bounded $k_{\max}$ in the original;
- $\sum_i k_i^2 = O(L)$ in Janson;
- for power laws, $\gamma > 5/2$ (Gao & Wormald, [](doi:10.1016/j.aim.2015.09.002)), and $\gamma > 1+\sqrt3$ for i.i.d. power-law "degrees".

Non-rigorous arguments suggest smaller $\gamma$ also works (Bianconi, Coolen & Pérez Vicente, [](doi:10.1103/PhysRevE.78.016114)). If $\langle k^2\rangle \to\infty$, then $\mathcal{P}_{\text{simple}}\to 0$ (Janson).
:::

:::{prf:theorem} SCM edge probabilities
:label: thm-cm-scm

Under [](#def-cm-scm), edges are independent with $p_{ij}$ given by [](#eq-cm-scm-p), and $\boldsymbol\lambda$ solves [](#eq-cm-scm-eqs). If some $k_i \notin [0, N-1]$ there is no solution, because each $p_{ij}\in[0,1]$ and $p_{ii} = 0$.
:::

:::{prf:theorem} Uniqueness of the SCM solution
:label: thm-cm-uniqueness

For $N \ge 3$, the system [](#eq-cm-scm-eqs) has **at most one** solution $\boldsymbol\lambda^* \in \mathbb{R}^N$. When it exists, $\boldsymbol\lambda^*$ is the unique global minimiser of the strictly convex potential $\mathcal{F}$ in [](#eq-cm-potential).
:::

:::{dropdown} Proof (notes, appendix A, with two small corrections)
**1. Gradient.** Only the pairs containing $i$ involve $\lambda_i$, so

$$
\frac{\partial\mathcal{F}}{\partial\lambda_i} = k_i - \sum_{j\ne i}\frac{e^{-(\lambda_i+\lambda_j)}}{1+e^{-(\lambda_i+\lambda_j)}} = k_i - \sum_{j\ne i}p_{ij}.
$$

So $\nabla\mathcal{F} = 0$ is exactly the system [](#eq-cm-scm-eqs).

**2. Hessian.** $\partial p_{ij}/\partial\lambda_i = -p_{ij}(1-p_{ij})$, the derivative of a logistic function. Writing $w_{ij} = p_{ij}(1-p_{ij})$:

$$
H_{ii} = \sum_{j\ne i} w_{ij},\qquad H_{ij} = w_{ij}\ (i\ne j),
$$

$$
\mathbf{x}^\top H\mathbf{x} = \sum_{i<j} w_{ij}\,(x_i+x_j)^2 .
$$

The sum runs over **unordered** pairs. The notes write $\sum_{i,j}$, which double-counts by a factor of 2; this doesn't affect the sign. $H$ is a signless Laplacian with edge weights $w_{ij}$.

**3. Strict positivity.** For finite $\boldsymbol\lambda$, every $p_{ij}\in(0,1)$, so every $w_{ij} > 0$; the "complete graph" of weights has no missing pair. The notes write $p_{ij} = e^{\lambda_i}/(e^{\lambda_i}+e^{\lambda_j}+1)$ at this step, which is a typo; the logistic form above is what is needed. So $\mathbf{x}^\top H\mathbf{x} = 0$ forces $x_i = -x_j$ for **every** pair. Fix $i$ with $x_i = c$; then all $x_j = -c$ for $j \ne i$. If $N \ge 3$, two distinct nodes $j, l \ne i$ exist, and $x_j = -x_l$ gives $-c = c$, so $c = 0$. Hence $H \succ 0$ and $\mathcal{F}$ is strictly convex on $\mathbb{R}^N$.

**4. Conclusion.** A strictly convex differentiable function has at most one stationary point, which is its global minimum. ∎

**Why $N \ge 3$ is needed.** For $N = 2$ the quadratic form is $w_{12}(x_1+x_2)^2$, which vanishes on $x = (c,-c)$. Only $\lambda_1+\lambda_2$ is identified, and the solution set is a line. The appendix's proof silently uses a third node.
:::

:::{prf:theorem} Existence: the degree-sequence polytope
:label: thm-cm-existence

Let $\mathcal{D}_N \subset \mathbb{R}^N$ be the convex hull of all graphical degree sequences on $N$ nodes. The SCM equations [](#eq-cm-scm-eqs) have a (unique, by [](#thm-cm-uniqueness)) solution **iff $\mathbf{k} \in \operatorname{int}\mathcal{D}_N$**. Equivalently, every inequality below must hold strictly, for all disjoint $S, T \subseteq \{1,\dots,N\}$ with $S \neq \emptyset$:

$$
\sum_{i\in S}k_i - \sum_{i\in T}k_i \;\le\; \lvert S\rvert\,(N-1-\lvert T\rvert).
$$ (eq-cm-polytope)

Chatterjee, Diaconis & Sly, [](doi:10.1214/10-AAP728), who use the inequality description of $\mathcal{D}_N$ due to Mahadev & Peled.
:::

:::{dropdown} Why, and why the notes' remark is not enough
**Why the condition is natural.** The SCM is a regular exponential family with sufficient statistic $\mathbf{k}(G)$. For such a family, the mean map $\boldsymbol\lambda \mapsto \mathbb{E}_{\boldsymbol\lambda}[\mathbf{k}(G)]$ is a diffeomorphism from $\mathbb{R}^N$ onto the interior of the convex hull of the statistic's support, which here is $\operatorname{int}\mathcal{D}_N$.

**Why each inequality is necessary.** Split the expected degrees:
- $\sum_{i\in S}k_i$ is twice the expected number of edges inside $S$, plus the expected number between $S$ and $S^c$.
- $\sum_{i\in T}k_i$ contributes at least the edges between $T$ and $S$.

So the difference is at most twice the edges inside $S$, plus the edges from $S$ to $(S\cup T)^c$. That is at most $\lvert S\rvert(\lvert S\rvert-1) + \lvert S\rvert(N-\lvert S\rvert-\lvert T\rvert) = \lvert S\rvert(N-1-\lvert T\rvert)$. Equality forces some $p_{ij}\in\{0,1\}$, which needs $\lambda_i+\lambda_j = \pm\infty$.

**Why $k_i\in(0,N-1)$ is not sufficient.** The appendix's closing remark claims that $k_i \in (0, N-1)$ for all $i$ guarantees existence. It does not; see the [worked example](#sec-cm-example). I checked numerically that [](#eq-cm-polytope) coincides with the facets of the hull of the 54 graphical sequences for $N = 4$.
:::

:::{prf:theorem} HSCM with Pareto hidden degrees (notes Thm 9.7; van der Hoorn, Lippner & Krioukov 2018)
:label: thm-cm-hscm-pareto

Let $\rho = \mathrm{Pareto}(\langle k\rangle,\gamma)$ with $\gamma>2$. That is, $\rho(k) = \alpha k_{\min}^\alpha k^{-\gamma}$ on $[k_{\min},\infty)$, with $\alpha = \gamma-1$ and $k_{\min} = \langle k\rangle\frac{\gamma-2}{\gamma-1}$, so that the mean is $\langle k\rangle$. Put

$$
\nu = \frac{1}{\langle k\rangle}\Big(\frac{\gamma-1}{\gamma-2}\Big)^2 = \frac{\langle k\rangle}{k_{\min}^2},\qquad R = \tfrac12\ln(\nu N).
$$ (eq-cm-hscm-constants)

Then the following four generators sample the same $\mathrm{HSCM}(N,\rho)$. Each connects $i$ and $j$ independently, with hidden variables drawn i.i.d.:

| Generator | Hidden variable | $p_{ij}$ |
|---|---|---|
| $\lambda$ | $\rho(\lambda) = \alpha e^{\alpha(\lambda-R)}$ on $(-\infty, R]$ | $1/(e^{\lambda_i+\lambda_j}+1)$ |
| $k$ | $\mathrm{Pareto}(\langle k\rangle,\gamma)$ | $1/\big(N\langle k\rangle/(k_ik_j) + 1\big)$ |
| $u$ | $U[0,1]$ | $1/\big(\nu N (u_iu_j)^{1/\alpha} + 1\big)$ |
| $x$ | $U[0,N]$ | $1/\big(\nu N^{1-2/\alpha}(x_ix_j)^{1/\alpha} + 1\big)$ |

Their classical (Chung–Lu) limits drop the "$+1$". For example, $p_k^{\mathrm{CL}} = k_ik_j/(N\langle k\rangle)$.

In this model the degree distribution, and the degree-sequence distribution, converge to the **$\rho$-mixed Poisson**, which is a power law with exponent $\gamma$. The ensemble is unbiased (max-entropy) given $\rho$, with expected degree $\to\langle k\rangle$.
:::

:::{dropdown} Why the four generators agree
All four are monotone reparametrisations of one hidden variable:
- $k = k_{\min}u^{-1/\alpha}$ is inverse-CDF sampling of the Pareto from $u \sim U[0,1]$.
- $e^{-\lambda} = k/\sqrt{N\langle k\rangle}$ is the classical-limit relation [](#eq-cm-chung-lu), taken as an exact change of variables.
- $x = Nu$.

**Check the $\lambda$ generator.** $e^{\lambda_i+\lambda_j} = N\langle k\rangle/(k_ik_j)$, which gives the $k$ generator. The largest $\lambda$ corresponds to $k_{\min}$: $\lambda_{\max} = \tfrac12\ln(N\langle k\rangle/k_{\min}^2) = \tfrac12\ln(\nu N) = R$. Its distribution is $P(\lambda\le\ell) = P\big(k \ge \sqrt{N\langle k\rangle}\,e^{-\ell}\big) = \big(k_{\min}e^{\ell}/\sqrt{N\langle k\rangle}\big)^{\alpha} = e^{\alpha(\ell-R)}$, whose density is $\alpha e^{\alpha(\lambda-R)}$.

**Check the $u$ generator.** $N\langle k\rangle/(k_ik_j) = N\langle k\rangle(u_iu_j)^{1/\alpha}/k_{\min}^2 = \nu N(u_iu_j)^{1/\alpha}$.

**Check the $x$ generator.** $(u_iu_j)^{1/\alpha} = N^{-2/\alpha}(x_ix_j)^{1/\alpha}$. The notes' typeset "$\nu n 1^{-2/\alpha}$" means $\nu N^{1-2/\alpha}$.

**What the theorem adds.** For these hidden variables, the HSCM (an SCM with *random* $\mathbf{k}$, whose $\boldsymbol\lambda$ would need re-solving for every sample) can be sampled by drawing $\boldsymbol\lambda$ directly. This is the notes' "Option 3". Proving that this is the max-entropy ensemble given $\rho$ is the content of van der Hoorn et al.
:::

**Soft preferential attachment.** At $\gamma=3$, $\mathrm{HSCM}(N, \mathrm{Pareto}(\langle k\rangle,3))$ is equivalent to **soft preferential attachment** (SPA). In SPA, a new node attaches with probability proportional to existing nodes' *expected* degrees, not their actual degrees (Krioukov & Ostilli, [](doi:10.1103/PhysRevE.88.022808)). So SPA is the unbiased $\gamma=3$ model, but SPA $\neq$ [Barabási–Albert PA](../nets-5116/barabasi/05-barabasi-albert-model.md), which builds in degree correlations and age effects.

**Limit.** As $\gamma\to\infty$, the Pareto concentrates at $k_{\min}\to\langle k\rangle$, and the HSCM becomes $G(N, p)$ with $p\approx\langle k\rangle/N$. The notes write "$\lim_{n\to\infty}$" here, which must mean $\gamma\to\infty$: for fixed $\gamma$, the $N\to\infty$ limit stays a power law.

(sec-cm-example)=
## Worked example

All numbers were computed in Python by minimising $\mathcal{F}$ with BFGS, enumerating all $2^{15}$ graphs on 6 nodes, and simulating $2\times 10^4$ pairings.

**SCM for $\mathbf{k} = (3,3,2,2,1,1)$, $N = 6$, $L = 6$.**
- The tightest polytope inequality [](#eq-cm-polytope) has slack 2, so a solution exists.
- **Multipliers:** $\boldsymbol\lambda^* = (-1.089, -1.089, 0.276, 0.276, 1.672, 1.672)$. Expected degrees match to $10^{-9}$.
- **Edge probabilities.** High-degree pairs get large $p$ and low-degree pairs small:
  - $p_{12} = 0.898$, $p_{13} = 0.693$, $p_{15} = 0.358$;
  - $p_{34} = 0.365$, $p_{35} = 0.125$, $p_{56} = 0.034$.
- **Chung–Lu would be badly off here.** $p^{\mathrm{CL}}_{12} = 9/12 = 0.75$, and the CL expected degrees are $(2.25, 2.25, 1.67, 1.67, 0.92, 0.92)$, because the graph is small and dense (not sparse). Excluding self-pairs and Maxwell–Boltzmann statistics both cost degree.
- **Degree fluctuations:** $\operatorname{Var}k_1(G) = \sum_j p_{1j}(1-p_{1j}) = 0.977$, so the hubs' degrees fluctuate by about $\pm 1$.
- **Entropy check:** $\mathcal{F}(\boldsymbol\lambda^*) = H[P_{\mathrm{SCM}}] = 7.716$ nats, computed both ways.

**CM for the same $\mathbf{k}$.**
- Brute force finds $\Omega(\mathbf{k}) = 17$ simple graphs, so $H_{\mathrm{CM}} = \ln 17 = 2.833 < 7.716 = H_{\mathrm{SCM}}$. This is as it must be: the uniform distribution on $\mathcal{G}_N(\mathbf{k})$ satisfies the soft constraints, so the canonical max-entropy distribution has at least as much entropy.
- **The SCM rarely hits $\mathbf{k}$ exactly.** Each of the 17 graphs has SCM probability $e^{-7.716} = 4.45\times10^{-4}$. So a draw from the SCM has degree sequence exactly $\mathbf{k}$ only $17 \times 4.45\times 10^{-4} = 0.76\%$ of the time.
- **Exact $\mathcal{P}_{\text{simple}}$.** There are $N_p = 11!! = 10395$ pairings and $N_s = 3!^2\,2!^2 = 144$, so $\mathcal{P}_{\text{simple}} = 17\times144/10395 = 0.235$. Bender–Canfield with $\kappa = 7/3$ gives $e^{-(\kappa^2-1)/4} = 0.329$. At $N = 6$ the asymptotic formula is only indicative.

**Bender–Canfield at scale.**
- **3-regular, $N = 2000$:** $\kappa = 3$ gives $e^{-2} = 0.1353$; the simulated fraction of simple pairings is $0.1348$. Mean numbers of self-loops and double edges were $0.993$ and $1.000$, against Poisson means $\nu_2/2 = 1$ and $\nu_2^2/4 = 1$.
- **Half degree-1, half degree-5, $N = 2000$:** $\kappa = 13/3$ gives $0.0117$; simulation gives $0.0115$. Rejection sampling already needs $\sim 85$ restarts per sample with this mild heterogeneity.

**An interior failure: $k_i\in(0,N-1)$ is not enough.**
- **Non-integer case.** $\mathbf{k} = (2.9, 2.9, 0.1, 0.1)$, $N = 4$, satisfies $k_i \in (0,3)$. But with $S = \{1,2\}$, $T = \{3,4\}$, [](#eq-cm-polytope) gives $5.6 \le 2$, which is false. The numerical solve diverges: $\lvert\lambda_i\rvert$ grows past $10^{150}$ with no fixed point.
- **Integer case.** The *graphical* sequence $(4,3,3,2,1,1)$ lies on the polytope's **boundary**. With $S=\{1,2,3\}$, $T=\{4,5,6\}$, [](#eq-cm-polytope) is tight ($6 = 6$): every graph with this degree sequence has a triangle on $\{1,2,3\}$ and no edges inside $\{4,5,6\}$. The multipliers run off to $\pm\infty$: $p_{12} = p_{13} = p_{23} \to 1$ and $p_{45} = p_{46} = p_{56}\to 0$. A graphical $\mathbf{k}$ (here $\Omega = 5$) can therefore still have no finite SCM solution.

**HSCM finite-size bias.** For $\langle k\rangle = 10$, $\gamma = 2.5$, the constants are $k_{\min} = 3.33$ and $\nu = 0.9$. Numerically integrating $(N-1)\iint p_u\,du\,dv$ gives the expected mean degree:

| $N$ | $10^3$ | $10^4$ | $10^5$ | $10^6$ |
|---|---|---|---|---|
| expected mean degree | 8.20 | 9.24 | 9.70 | 9.89 |

It converges slowly to $\langle k\rangle = 10$, because hub–hub pairs saturate at $p\to1$ instead of exceeding it.

(sec-cm-limits)=
## Assumptions and limitations

- **Which ensemble to use.** CM, SCM and HSCM agree on most *local* sparse statistics, but they are not equivalent.
  - **Degrees.** In the CM, degrees are exact. In the SCM they are Poisson-like. In the HSCM they are $\rho$-mixed Poisson.
  - **Microcanonical vs canonical.** These are non-equivalent under an extensive number of constraints (Squartini et al. 2015): the relative entropy per node does not vanish.
  - **Choose by what is fixed in the data.** Use the CM when the observed $\mathbf{k}$ itself is the constraint, the SCM for a likelihood-based null model of one snapshot, and the HSCM when only the distribution is stable over time.
- **The solution may not exist.** Observed sequences with a dense core or a threshold-graph structure sit on or near the boundary of $\mathcal{D}_N$. Their $\lambda_i$ diverge, numerical solvers become ill-conditioned, and fitted $p_{ij}$ hit $0$ or $1$. Check the slack in [](#eq-cm-polytope) before trusting a fit.
- **Degree-only nulls ignore everything else.** Clustering, assortativity, communities and geometry are all averaged out, so these models are null baselines. To keep $P(k,k')$, use the [dk-series](./06-dk-series.md). For clustering use [latent-space models](./08-latent-space-models.md), and for blocks use [SBMs](./09-stochastic-block-models.md).
- **Erased and Chung–Lu shortcuts are not unbiased.** The erased CM loses hub degree, and Chung–Lu truncation removes hub–hub edges. Both introduce spurious **disassortativity** precisely when $\gamma<3$, i.e. $k_{\max}\gg k_s$. Don't read degree correlations off them.
- **Rigour is limited for heavy tails.** Asymptotic enumeration is proven only for $\gamma>5/2$. Swap-chain mixing for general sequences has no practical rigorous bound.

(sec-cm-connections)=
## Connections

- **NETS 5116.**
  - Barabási's configuration model, degree-preserving randomisation and hidden-parameter model ([ch. 4](../nets-5116/barabasi/04-scale-free-networks.md)) are the CM, the swap chain and Chung–Lu respectively.
  - The structural cutoff ([ch. 7](../nets-5116/barabasi/07-degree-correlations.md)) is where $p^{\mathrm{CL}}$ hits $1$.
  - The Molloy–Reed criterion $\kappa > 2$ ([ch. 8](../nets-5116/barabasi/08-network-robustness.md)) is the giant-component threshold in the CM; the same $\kappa$ appears in Bender–Canfield.
  - The modularity null model ([Newman ch. 7 notes](../nets-5116/newman/07-measures-and-metrics.md)) uses $k_ik_j/2L$, i.e. Chung–Lu.
- **NETS 6116.**
  - The CM/SCM/HSCM triple is the degree-sequence row of the ensemble table in [typicality and maximum entropy](./04-typicality-and-max-entropy.md).
  - The CM is the "1k" level of the [dk-series](./06-dk-series.md).
  - The HSCM is the simplest [hidden-variable model](./07-hidden-variables-and-graphons.md): its connection function is $p(\kappa,\kappa') = 1/(N\langle k\rangle/\kappa\kappa'+1)$, whose Chung–Lu limit $\kappa\kappa'/(N\langle k\rangle)$ is rank-1.
  - The $\mathbb{S}^1$/$\mathbb{H}^2$ [latent-space models](./08-latent-space-models.md) add a geometric term to $\lambda_i+\lambda_j$.
  - The degree-corrected [SBM](./09-stochastic-block-models.md) is the SCM with blocks.
- **PHYS 7335.**
  - Annealed networks and the uncorrelated $P(k'\mid k)$ in [degree-block mean-field](../phys-7335/01-degree-block-formalism.md) are the Chung–Lu limit.
  - The generating-function SIR/percolation calculation ([SIR and percolation](../phys-7335/07-sir-percolation.md)) is exact on the CM, because it is locally tree-like.
  - Thresholds $\lambda_c\propto\langle k\rangle/\langle k^2\rangle$ inherit the CM's $\kappa$.
- **NETS 7332.** The CM is the hand-designed baseline that deep [graph generative models](../nets-7332/basics/08-scaling-and-generative.md) are compared against. Its maximum-likelihood form is the $\beta$-model, a logistic model with one fixed effect per node, $\operatorname{logit}p_{ij} = \beta_i+\beta_j$.

## Self-test

:::{dropdown} Q1. Fill in the 3×2 table of ensembles (hard/soft/hypersoft × $\langle k\rangle$ / $\mathbf{k}$).
| | $\langle k\rangle$ | $\mathbf{k}$ |
|---|---|---|
| hard | $G(N,L)$ | CM |
| soft | $G(N,p)$ | SCM |
| hypersoft | $G(N,\rho)$ | HSCM |

Each row is maximum entropy under hard, expected or distributional constraints.
:::

:::{dropdown} Q2. Derive $p_{ij}$ in the SCM from the Gibbs form. Why are the edges independent?
For simple undirected graphs, $\sum_i\lambda_ik_i(G) = \sum_{i<j}(\lambda_i+\lambda_j)A_{ij}$. The weight factorises over pairs, so $Z = \prod_{i<j}(1+e^{-\lambda_i-\lambda_j})$ and $P(G) = \prod_{i<j}p_{ij}^{A_{ij}}(1-p_{ij})^{1-A_{ij}}$, with $p_{ij} = 1/(e^{\lambda_i+\lambda_j}+1)$. Independence follows from the factorisation, which holds because the constraint is linear in $A$.
:::

:::{dropdown} Q3. Write $\Omega(\mathbf{k})$ in terms of pairings. Why is $\mathcal{P}_{\text{simple}}$ the hard part, and what is its asymptotic value?
$\Omega = \frac{(2L-1)!!}{\prod_i k_i!}\mathcal{P}_{\text{simple}}$. Loops and double edges are asymptotically Poisson with means $\nu_2/2$ and $\nu_2^2/4$, which gives $\mathcal{P}_{\text{simple}}\to e^{-(\kappa^2-1)/4}$. Making this rigorous needs conditions on $\mathbf{k}$, and $\mathcal{P}_{\text{simple}}\to0$ if $\langle k^2\rangle\to\infty$. "$\approx$" means the ratio tends to 1.
:::

:::{dropdown} Q4. Prove that the SCM equations have at most one solution. Where does the proof use $N\ge3$?
The potential $\mathcal{F}(\boldsymbol\lambda) = \sum_{i<j}\ln(1+e^{-\lambda_i-\lambda_j}) + \mathbf{k}\cdot\boldsymbol\lambda$ has gradient $k_i-\sum_jp_{ij}$. Its Hessian quadratic form is $\sum_{i<j}p_{ij}(1-p_{ij})(x_i+x_j)^2$. This vanishes only if $x_i = -x_j$ for all pairs, which with three or more nodes forces $\mathbf{x} = 0$. So $\mathcal{F}$ is strictly convex and has at most one stationary point. For $N=2$ only $\lambda_1+\lambda_2$ is determined.
:::

:::{dropdown} Q5. Give a sequence with all $k_i\in(0,N-1)$ for which the SCM has no solution. What is the correct existence condition?
$(2.9,2.9,0.1,0.1)$: $k_1+k_2-k_3-k_4 = 5.6 > 2 = \lvert S\rvert(N-1-\lvert T\rvert)$. Or the graphical but boundary sequence $(4,3,3,2,1,1)$. A solution exists iff $\mathbf{k}$ is in the interior of the convex hull of graphical sequences (Chatterjee–Diaconis–Sly).
:::

:::{dropdown} Q6. When does Chung–Lu approximate the SCM? What goes wrong for $\gamma<3$?
When $p_{ij}\ll1$ for all pairs, i.e. $k_ik_j\ll N\langle k\rangle$. For $\gamma<3$, $k_{\max}\gg k_s\sim\sqrt{N\langle k\rangle}$, so hub pairs have $k_ik_j/(N\langle k\rangle)>1$. Truncating these at 1 removes hub–hub edges, which lowers hub degrees and creates disassortativity. The exact SCM saturates smoothly instead.
:::

:::{dropdown} Q7. State the four HSCM generators for Pareto $\rho$ and show that the $u$ generator follows from the $k$ generator.
The four generators use $\lambda\sim\alpha e^{\alpha(\lambda-R)}$, $k\sim$ Pareto, $u\sim U[0,1]$ and $x\sim U[0,N]$, with $p = 1/(e^{\lambda_i+\lambda_j}+1)$ in every case. Substituting $k = k_{\min}u^{-1/\alpha}$ into $N\langle k\rangle/(k_ik_j)$ gives $\nu N(u_iu_j)^{1/\alpha}$, with $\nu = \langle k\rangle/k_{\min}^2 = \frac1{\langle k\rangle}(\frac{\gamma-1}{\gamma-2})^2$.
:::

:::{dropdown} Q8. Why is $H_{\mathrm{SCM}}\ge\ln\Omega(\mathbf{k})$, and why does a random SCM graph almost never have degree sequence exactly $\mathbf{k}$?
The uniform distribution on $\mathcal{G}_N(\mathbf{k})$ satisfies the SCM's expected-degree constraints, and the SCM maximises entropy over all distributions that do. Degrees in the SCM are sums of independent Bernoullis with variance $\sum_jp_{ij}(1-p_{ij})$. The probability that all $N$ of them hit their targets simultaneously decays exponentially in $N$; it is 0.76% already for $N=6$ in the worked example.
:::

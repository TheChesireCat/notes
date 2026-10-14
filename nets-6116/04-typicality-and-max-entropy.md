---
title: Network Typicality and Maximum-Entropy (Unbiased) Models
short_title: Typicality and max-entropy
subject: NETS 6116 · Topic
description: What it can and cannot mean for an observed network to be "typical" in a model, and how maximum entropy builds the unbiased micro-, canonical and hypercanonical ensembles that make the notion well defined.
tags: [typicality, maximum-entropy, ergm, gibbs-distribution, ensembles, erdos-renyi, ensemble-equivalence, unlabeled-graphs]
---

:::{tip} TL;DR
- **A single graph $G_0$ cannot be "typical" in an arbitrary model.** The obvious definitions all fail:
  - the most likely graph (the empty graph is the mode of $G(N,p)$ for $p<1/2$);
  - being close in some graph distance;
  - matching one property, or all properties.
  
  Typicality is well defined only when (A.1) a property $f$ **concentrates** and (A.2) $f$ is a **sufficient statistic**, $P(G) = \tilde P[f(G)]$. Then $G_0$ is typical iff $f(G_0) \approx \mathbb{E} f$.
- **A typical network is not the same as a typical value of a property.** Every graph with $\langle k\rangle \approx 10$, including any preferential-attachment graph, is a *typical* $G(N,p)$ graph, because $G(N,p)$ depends only on $L$. The binomial degree distribution is merely *the overwhelmingly most numerous* shape. With $N=10^6$, graphs with a Poisson degree distribution outnumber those with a $k^{-3}$ tail by a factor of about $e^{8.5\times10^6}$.
- **Unbiased model = maximum entropy subject to the constraints.** There are three ensembles:
  - *Microcanonical* (sharp constraints $f_s(G)=f_s^*$) is uniform on the allowed set.
  - *Canonical* (expected constraints $\langle f_s\rangle = f_s^*$) is the Gibbs/exponential-family/ERGM form $P(G) = e^{-\sum_s\lambda_s f_s(G)}/Z$, with $-\partial\ln Z/\partial\lambda_s = f_s^*$.
  - *Hypercanonical* is a mixture of canonical ensembles over random $f^* \sim \rho$.
- **Erdős–Rényi is max-entropy.** $G(N,L)$ is the microcanonical and $G(N,p)$ the canonical max-entropy model for the edge count, with $p = 1/(e^\lambda+1)$ (Fermi–Dirac). Canonical = binomial mixture of microcanonical. Labelled and unlabelled versions are *different* models: $H_D \le H_U \le H_L$.
- **Canonical ensembles always give typical graphs (A.2 holds by construction).** Concentration (A.1) is extra: a convex $\ln Z$ does *not* guarantee it. The Strauss (edges + triangles) model is bimodal.
:::

- **Source.**
  - Krioukov, *Network Science II* lecture notes, ch. 7 (*Network typicality*) and ch. 8 (*Unbiased models*).
  - [](doi:10.1103/PhysRev.106.620) (Jaynes, *Phys. Rev.* 106, 620, 1957): the maximum-entropy principle as inference.
  - [](doi:10.1103/PhysRevE.70.066117) (Park & Newman, *Phys. Rev. E* 70, 066117, 2004): exponential random graphs as Gibbs ensembles.
  - [](doi:10.1103/PhysRevE.106.054308) (Paton, Hartle, Stepanyants, van der Hoorn & Krioukov, *Phys. Rev. E* 106, 054308, 2022): labelled vs unlabelled ER models.
  - [](doi:10.1137/1028156) (Strauss, *SIAM Review* 28, 513, 1986): the edges-plus-triangles model.
  - [](doi:10.1103/PhysRevLett.115.268701) (Squartini, de Mol, den Hollander & Garlaschelli, *PRL* 115, 268701, 2015): breaking of ensemble equivalence.
  - Cover & Thomas, [*Elements of Information Theory*](doi:10.1002/047174882X), ch. 3: the asymptotic equipartition property.
- **Builds on.** $G(N,p)$ and $G(N,L)$ ([Barabási ch. 3 notes](../nets-5116/barabasi/03-random-networks.md)); sparsity and why properties of a single finite graph are not formally defined ([sparsity and small worlds](./01-sparsity-and-small-worlds.md)).
- **Notation.** Shared symbols as in [](#notation), with $N, L, \langle k\rangle$ for Krioukov's $n, m, \bar k$. Also:
  - $N_{\mathrm p} = \binom N2$, the number of node pairs (Krioukov: $n'$). The density is $d = L/N_{\mathrm p}$.
  - Entropy is $H[P]$ (Krioukov: $S[P]$), in nats unless stated otherwise.
  - Constraints are indexed $s = 1,\dots,n_c$ (Krioukov uses $S$ for their number).
  - $\lambda_s$ are Lagrange multipliers, *not* the spreading rate.
  - $\rho(f^*)$ is the hypercanonical distribution of the constraint values. It is not prevalence.
  - $\mathcal{U}$ denotes unlabelled ensembles, $\mathcal{D}$ delabelled ones, and $h(p) = -p\ln p - (1-p)\ln(1-p)$ the binary entropy.

(sec-maxent-setup)=
## Setup and definitions

The meta-problem: given an observed graph $G_0$ and a model $P(G)$ on $\mathcal{G}_N$, decide whether $G_0$ "comes from" $P$.

Why bother? Properties such as sparsity, small-worldness, strong clustering or scale-freeness are statements about **sequences** $N \to \infty$. They make no formal sense for one finite $G_0$, but perfect sense for a model. A *useful* definition of typicality lets us transfer such statements from $P(G)$ to $G_0$.

Two caveats from the notes. $N$ is fixed, because $G_0$ is. And $P(G)$ is often intractable: no closed form exists for preferential attachment.

(sec-maxent-bad-defs)=
### Definitions that fail

| Candidate definition of "$G_0$ is typical" | Why it fails |
|---|---|
| $G_0 = \arg\max_G P(G)$ (maximum likelihood) | In $G(N,L)$ every allowed graph is a maximiser. In $G(N,p)$ with $p<1/2$ the empty graph is the unique mode. |
| $\mathbb{E}_{G\sim P}\, d(G,G_0) < \varepsilon$ for a graph distance $d$ | Depends on $d$, of which there are uncountably many, including adversarial ones such as $d = \pi\,\mathbb{1}\{G_1\ne G_2\}$. A "good" $d$ may not concentrate, may not bound differences in the properties you care about, and its law is usually harder to compute than $P$ itself. |
| $\lVert f(G_0) - \mathbb{E}f \rVert < \varepsilon$ for a property $f$ | Depends on $f$, which can be adversarial ($f = \pi\,\mathbb{1}\{G=G_0\}$). Even a natural $f$ need not concentrate (Strauss model, below). Several dependent properties raise the question of which joint deviation counts. |
| The above for **all** $f$ | No graph is typical in any model, because some $f$ can always be chosen to fail. |

(sec-maxent-good-defs)=
### Definitions that work

:::{prf:definition} Concentration and sufficiency
:label: def-maxent-assumptions

Fix a property $f:\mathcal{G}_N \to \mathbb{R}^D$ and a model $P$.

- **(A.1) Concentration.** Under $G\sim P$, $f(G)$ is sharply peaked at $\bar f = \mathbb{E}f$.
- **(A.2) Sufficiency.** $P(G) = \tilde P[f(G)]$ for some function $\tilde P$, so graphs with equal $f$ are equiprobable. $f$ is then a **sufficient statistic** of $P$.

Example: in $G(N,p)$, $P(G) = p^{L(G)}(1-p)^{N_{\mathrm p}-L(G)}$, so $L$ is sufficient and $L \sim \mathrm{Bin}(N_{\mathrm p},p)$ concentrates.
:::

:::{prf:definition} Typical value of a property
:label: def-maxent-typical-value

If (A.1) holds and $\lVert f(G_0) - \bar f\rVert < \varepsilon$, then $G_0$ has an **$\varepsilon$-typical value of $f$**.

This says nothing about other properties. For example, $G_0$ has a typical degree distribution in $G(N,p)$ if its $p_k$ is $\varepsilon$-close to $\mathrm{Bin}(N-1,p)$. It has a typical degree distribution in PA if $p_k$ is close to the PA limit law.
:::

:::{prf:definition} Typical graph
:label: def-maxent-typical-graph

If (A.1) **and** (A.2) hold for $f$, then $G_0$ is **$\varepsilon$-typical in $P$** iff $\lVert f(G_0) - \bar f\rVert < \varepsilon$.
:::

Why this works: by (A.2) all graphs with the same $f$ have the same probability, and by (A.1) almost all of the mass sits on graphs with $f\approx \bar f$. A graph with $f(G_0)$ far from $\bar f$ is therefore an outlier, and one with $f(G_0)\approx\bar f$ lies in the bulk.

:::{prf:definition} Typical sequence
:label: def-maxent-typical-sequence

For i.i.d. $x_1,\dots,x_n \sim P$, the sequence is **$\varepsilon$-typical** if

$$
e^{-n(H[P]+\varepsilon)} \le \mathbf{P}(x_1,\dots,x_n) \le e^{-n(H[P]-\varepsilon)} .
$$ (eq-maxent-typical-sequence)

A sequence of graphs $G_1,\dots,G_n \stackrel{\text{iid}}{\sim} P(G)$ is $\varepsilon$-typical in $P$ if it is an $\varepsilon$-typical sequence with respect to $P$.
:::

This last definition always works, whether or not $P$ has a sufficient statistic. The price is that it needs many independent graphs, and we usually have one.

:::{prf:definition} Unbiased (maximum-entropy) model
:label: def-maxent-unbiased

Given properties $f_1,\dots,f_{n_c}$ and target values $f_s^*$ (typically measured on $G_0$), the **unbiased model** is

$$
P^* = \arg\max_P H[P], \qquad H[P] = -\sum_{G\in\mathcal{G}} P(G)\ln P(G),
$$ (eq-maxent-principle)

subject to one of three kinds of constraint:

| Ensemble | Constraint | |
|---|---|---|
| **Microcanonical** (sharp) | $f_s(G) = f_s^*$ for every $G$ in the support | (8.1) |
| **Canonical** (soft) | $\langle f_s\rangle = \sum_G P(G) f_s(G) = f_s^*$ | (8.2) |
| **Hypercanonical** (hypersoft) | the $f_s^*$ are themselves random with joint law $\rho(f^*)$ | (8.3) |
:::

The interpretation, following Jaynes: $P^*$ encodes everything known about $\{f_s\}$ and nothing else. It is *not* a claim to be the correct model of $G_0$. It is the **correct null model** given the information in $\{f_s\}$. Krioukov's motivating example: told only that a network has $N$ nodes and $L < N$ edges, answering "a star with a captain at the centre" injects structure (a hub) for which there is no evidence.

(sec-maxent-core)=
## Core ideas

(sec-maxent-typical-vs-value)=
### Typical network vs typical value of a property

$G(N,p)$ "cares" only about $L$. Every graph with $L$ close to $p N_{\mathrm p}$ is a typical $G(N,p)$ graph, whatever its degree sequence, clustering or diameter. That includes a scale-free graph.

The binomial degree distribution is the typical *value* of the degree-distribution property only because of **entropic domination**. Among all graphs with the right $L$, far more have binomial degree sequences than any other shape.

The meditation exercise from the notes makes the point. Generate a PA graph with $\gamma = 3$, $\langle k\rangle = 10$ and $N=10^6$. You **cannot** certify that it is a typical PA graph, because PA has no tractable sufficient statistic, so (A.2) fails. You **can** certify that it is a typical $G(N, p\approx10^{-5})$ graph.

Summary of the notes:
- No network is typical in PA in the sense of {prf:ref}`def-maxent-typical-graph`.
- Any network with mean degree $\langle k\rangle$ is a typical ER graph with $p = \langle k\rangle/(N-1)$.
- The typical *degree distribution* is binomial in ER and a power law in PA.

(sec-maxent-ensembles)=
### The three ensembles and how they nest

- **Microcanonical.** For finite $N$ the set $\mathcal{G}(\{f_s^*\}) = \{G: f_s(G) = f_s^*\ \forall s\}$ is finite (possibly empty), and the max-entropy distribution on a finite set is uniform.
- **Canonical.** Gibbs form, {prf:ref}`thm-maxent-gibbs`. Because the $f_s$ are sufficient statistics, (A.2) holds by construction, so {prf:ref}`def-maxent-typical-graph` applies whenever (A.1) does.
- **Canonical as a mixture of microcanonicals.** Conditioned on $f(G) = \phi$, a canonical ensemble is uniform on $\mathcal{G}(\phi)$:

  $$
  P_{\mathrm{can}}(G\mid f^*) = \frac{1}{\lvert\mathcal{G}(\phi)\rvert}\, P_{\mathrm{can}}(f(G)=\phi \mid f^*), \qquad \phi = f(G).
  $$ (eq-maxent-can-mixture)

  For ER this reads

  $$
  p^{L(G)}(1-p)^{N_{\mathrm p}-L(G)} = \frac{1}{\binom{N_{\mathrm p}}{L}}\cdot\binom{N_{\mathrm p}}{L}p^L(1-p)^{N_{\mathrm p}-L}, \qquad L = L(G).
  $$

  So to sample $G(N,p)$, draw $L\sim\mathrm{Bin}(N_{\mathrm p},p)$ and then $G\sim G(N,L)$.
- **Hypercanonical** = mixture of canonical ensembles over $f^*\sim\rho$. Sample $f^* \sim \rho$, then $G\sim P_{\mathrm{can}}(\cdot\mid f^*)$, which can itself be done by sampling $\phi\sim P_{\mathrm{can}}(\phi\mid f^*)$ and then $G \sim P_{\mathrm{mic}}(\cdot\mid\phi)$.

The nesting is what makes the hypersoft configuration model (HSCM) on the [configuration-models page](./05-configuration-models.md) tractable. It is also why hidden-variable models ([hidden variables and graphons](./07-hidden-variables-and-graphons.md)) are hypercanonical ensembles.

(sec-maxent-labels)=
### Labelled, delabelled and unlabelled models

If X (the client in the notes' story) wants **unlabelled** graphs, $G(N,L)$ is not the answer. Three distinct models exist on the same $N$ and $L$:

| Model | Sample space | Probability of an unlabelled shape $U$ |
|---|---|---|
| Labelled $G(N,L)$ | labelled graphs, uniform | each labelling $1/\binom{N_{\mathrm p}}{L}$ |
| Delabelled $\mathcal{D}(N,L)$ | shapes of $G(N,L)$ samples | $\dfrac{N!/\lvert\mathrm{Aut}(U)\rvert}{\binom{N_{\mathrm p}}{L}}$, so symmetric shapes are rarer |
| Unlabelled $\mathcal{U}(N,L)$ | unlabelled graphs, uniform (max-entropy) | $1/\lvert\mathcal{U}(N,L)\rvert$ |

$\lvert\mathcal{U}(N,L)\rvert$ is given by Pólya counting (Harary & Palmer, *Graphical Enumeration*, 1973, eq. 4.1.8). The canonical unlabelled model $\mathcal{U}(N,p)$ has $P(U)\propto e^{-\lambda L(U)}$ summed over unlabelled graphs. Its $Z$ has no closed form, and it was first studied in 2022 (Paton et al.).

The degree distributions differ too. The notes' figures, from Paton et al., show the unlabelled ER degree distribution is visibly broader than the labelled binomial at the same $\langle k\rangle$.

(sec-maxent-results)=
## Key results

:::{prf:theorem} Microcanonical max-entropy distribution
:label: thm-maxent-micro

The maximum-entropy distribution supported on a finite non-empty set $\mathcal{G}(\{f_s^*\})$ is uniform:

$$
P_{\mathrm{mic}}^*(G) = \frac{\mathbb{1}\{G\in\mathcal{G}(\{f_s^*\})\}}{\lvert\mathcal{G}(\{f_s^*\})\rvert}, \qquad H = \ln\lvert\mathcal{G}(\{f_s^*\})\rvert .
$$ (eq-maxent-micro)

With $f = L$: $G(N,L)$, with $P(G) = 1/\binom{N_{\mathrm p}}{L}$.
:::

:::{dropdown} Proof
For any $P$ on a set of size $M$, $\ln M - H[P] = \sum_G P(G)\ln\frac{P(G)}{1/M} = D_{\mathrm{KL}}(P\,\Vert\,\mathrm{Unif}) \ge 0$, with equality iff $P$ is uniform.
:::

:::{prf:theorem} Canonical max-entropy distribution (Gibbs / ERGM)
:label: thm-maxent-gibbs

Under the soft constraints $\langle f_s\rangle = f_s^*$, the entropy maximiser is

$$
P^*_{\mathrm{can}}(G) = \frac{1}{Z}\exp\Big(-\sum_{s=1}^{n_c}\lambda_s f_s(G)\Big), \qquad Z(\boldsymbol\lambda) = \sum_{G\in\mathcal{G}}\exp\Big(-\sum_s\lambda_s f_s(G)\Big),
$$ (eq-maxent-gibbs)

with the multipliers fixed by

$$
\langle f_s\rangle = -\frac{\partial \ln Z}{\partial\lambda_s} = f_s^*, \qquad s = 1,\dots,n_c .
$$ (eq-maxent-lagrange)

Moreover $\partial^2\ln Z/\partial\lambda_s\partial\lambda_t = \mathrm{Cov}(f_s,f_t)$, so $\ln Z$ is convex. If the $f_s$ are affinely independent on $\mathcal{G}$, it is strictly convex and {eq}`eq-maxent-lagrange` has at most one solution.

These distributions are called **Gibbs/Boltzmann** distributions (physics), the **exponential family** and **exponential random graph models (ERGMs)** (statistics), and **Gibbs measures** (probability).
:::

:::{dropdown} Derivation, and a proof that it is the global maximum
**Lagrangian.** Maximise $H[P] - \sum_s\lambda_s\big(\sum_G P(G)f_s(G) - f_s^*\big) - \nu\big(\sum_G P(G)-1\big)$. Setting $\partial/\partial P(G) = 0$ gives $-\ln P(G) - 1 - \sum_s\lambda_s f_s(G) - \nu = 0$, so $P(G)\propto e^{-\sum_s\lambda_s f_s(G)}$, and normalisation gives $Z$.

**Moment equations.**

$$
-\partial_{\lambda_s}\ln Z = Z^{-1}\sum_G f_s(G)e^{-\sum_t\lambda_t f_t(G)} = \langle f_s\rangle .
$$

Differentiating once more gives $\langle f_sf_t\rangle - \langle f_s\rangle\langle f_t\rangle$. A covariance matrix is positive semidefinite, so $\ln Z$ is convex. It is positive definite unless some combination $\sum_s c_s f_s$ is constant on $\mathcal{G}$.

**Global optimality (Gibbs inequality).** Let $Q$ be any distribution meeting the constraints. Then

$$
H[Q] = -\sum_G Q\ln Q \le -\sum_G Q\ln P^* = \ln Z + \sum_s\lambda_s\langle f_s\rangle_Q = \ln Z + \sum_s\lambda_s f_s^* = H[P^*].
$$

The inequality is $D_{\mathrm{KL}}(Q\Vert P^*)\ge0$. The equalities use only the constraints, which $Q$ and $P^*$ share. Equality holds iff $Q = P^*$.

**Existence** (my comment, standard exponential-family theory; [Wainwright & Jordan 2008](doi:10.1561/2200000001), §3.4). A solution $\boldsymbol\lambda$ with finite entries exists iff $f^*$ lies in the relative interior of the convex hull of $\{f(G): G\in\mathcal{G}\}$. For example, $L^* = 0$ or $L^* = N_{\mathrm p}$ is reached only as $\lambda\to\pm\infty$.
:::

:::{prf:proposition} Erdős–Rényi as the max-entropy model of the edge count
:label: prop-maxent-er

With $f = L$, the microcanonical maximiser is $G(N,L)$.

For the canonical constraint $\langle L\rangle = L^*$, write $q = e^{-\lambda}$. Then

$$
Z = \sum_{\ell=0}^{N_{\mathrm p}}\binom{N_{\mathrm p}}{\ell}q^\ell = (1+q)^{N_{\mathrm p}}, \qquad
d \equiv \frac{L^*}{N_{\mathrm p}} = \frac{q}{1+q} = \frac{1}{e^{\lambda}+1}.
$$ (eq-maxent-fermi-dirac)

This is the **Fermi–Dirac** occupation function: each node pair is an independent two-state "orbital" with energy $\lambda$. Inverting gives $q = d/(1-d)$ and $Z = (1-d)^{-N_{\mathrm p}}$, so

$$
P^*_{\mathrm{can}}(G) = \Big(\tfrac{d}{1-d}\Big)^{L(G)}(1-d)^{N_{\mathrm p}} = d^{L(G)}(1-d)^{N_{\mathrm p}-L(G)},
$$

which is $G(N,p)$ with $p = d$. At $\lambda = 0$, $p = 1/2$: the uniform distribution on all $2^{N_{\mathrm p}}$ labelled graphs.
:::

:::{prf:proposition} Labelled, delabelled and unlabelled entropies
:label: prop-maxent-label-entropy

For the same constraint,

$$
H_D \le H_U \le H_L, \qquad H_L - H_D = \mathbb{E}_{U\sim\mathcal{D}}\Big[\ln\frac{N!}{\lvert\mathrm{Aut}(U)\rvert}\Big].
$$ (eq-maxent-label-entropy)
:::

:::{dropdown} Proof sketch (my derivation)
- $H_D\le H_U$: $\mathcal{U}$ is the max-entropy (uniform) distribution on the same set of shapes that $\mathcal{D}$ lives on.
- $H_U\le H_L$: every unlabelled graph has at least one labelling, so there are at least as many labelled graphs as shapes.
- **Chain rule.** A labelled graph determines its shape $U$. Given $U$, the labelled ensemble is uniform over the $N!/\lvert\mathrm{Aut}(U)\rvert$ labellings of $U$. Hence $H_L = H_D + \mathbb{E}\ln\big(N!/\lvert\mathrm{Aut}(U)\rvert\big)$.

When almost all graphs are asymmetric, $H_L - H_D \approx \ln N!$. That holds for uniformly random graphs ($p = 1/2$; [Erdős & Rényi 1963](doi:10.1007/BF01895716)) and, more generally, for $G(N,L)$ with $\ln N/N \ll L/N_{\mathrm p} \ll 1 - \ln N/N$ ([Wright 1971](doi:10.1007/BF02392023)).

*My comment:* in the sparse regime $\langle k\rangle = O(1)$ there are $\Theta(N)$ isolated nodes and leaves. Then $\ln\lvert\mathrm{Aut}\rvert$ is itself extensive and the correction to $\ln N!$ is not negligible, which is the regime Paton et al. emphasise.
:::

:::{prf:proposition} Edge-sequence typicality is graph typicality in $G(N,p)$
:label: prop-maxent-aep-er

Treat the $N_{\mathrm p}$ edge indicators of $G\sim G(N,p)$ as an i.i.d. Bernoulli($p$) sequence. Its per-symbol log-probability is

$$
-\frac{1}{N_{\mathrm p}}\ln P(G) = h(p) + \frac{\lambda\,\big(L(G) - pN_{\mathrm p}\big)}{N_{\mathrm p}}, \qquad \lambda = \ln\frac{1-p}{p}.
$$ (eq-maxent-aep-er)

So the edge sequence is $\varepsilon$-typical ({prf:ref}`def-maxent-typical-sequence`) iff $\lvert L(G) - \bar L\rvert < \varepsilon N_{\mathrm p}/\lvert\lambda\rvert$. That is exactly {prf:ref}`def-maxent-typical-graph` with $f = L$. This is HW2 in the notes.
:::

:::{dropdown} Derivation
$-\ln P(G) = -L\ln p - (N_{\mathrm p}-L)\ln(1-p)$. Add and subtract $\bar L = pN_{\mathrm p}$:

$$
-\ln P(G) = N_{\mathrm p}h(p) - (L-\bar L)\ln\tfrac{p}{1-p}.
$$

Divide by $N_{\mathrm p}$.

By the AEP (weak law of large numbers applied to $-\ln P(x_i)$), the left side converges to $h(p)$ in probability, because $L/N_{\mathrm p}\to p$.

*Caveat.* When the graphs are sparse, $p\to0$ and $h(p)\to0$, so a fixed $\varepsilon$ becomes vacuous. Use the relative deviation $\lvert{-\ln P}/(N_{\mathrm p}h) - 1\rvert$ instead.

Note that the edges are i.i.d. *within* one $G(N,p)$ graph. This is not the same as $G_i \stackrel{\text{iid}}{\sim} P(G)$ in {prf:ref}`def-maxent-typical-sequence`, a common confusion the notes flag.
:::

:::{prf:proposition} Hypercanonical ER gives power laws from Poisson pieces
:label: prop-maxent-her

Let $\kappa\sim\mathrm{Pareto}$ with mean $\langle k\rangle$ and density exponent $\gamma>2$, and draw $G\sim G(N,p)$ with $p = \min(1,\kappa/N)$. As $N\to\infty$:
- **Conditioned on $G$** (one graph), the degree distribution is $\mathrm{Poisson}(\kappa)$.
- **In the ensemble $G(N,\rho)$**, $P(k) = \int\rho(\kappa)\,\mathrm{Pois}(k;\kappa)\,d\kappa \sim k^{-\gamma}$.

This is the simplest unbiased model with a power-law $P(k)$, even though almost every *graph* in it has a Poisson degree distribution. Moral of the notes: the degree distribution $P(k)$ is not the degree-*sequence* distribution $P(\mathbf{k})$.
:::

(sec-maxent-equivalence)=
### Ensemble equivalence

{eq}`eq-maxent-can-mixture` says the canonical ensemble is a mixture of microcanonical ones weighted by $P_{\mathrm{can}}(\phi)$. When that weight concentrates, the ensembles are **equivalent** in the thermodynamic limit: their entropies agree to leading order and macroscopic properties coincide.

For ER, $H_{\mathrm{can}} - H_{\mathrm{mic}} \simeq \tfrac12\ln\big(2\pi N_{\mathrm p}p(1-p)\big) = O(\ln N)$, negligible against $H = \Theta(N\ln N)$ in the sparse case. See the worked example.

With an *extensive* number of constraints, such as the full degree sequence (CM vs SCM), equivalence can **break**. Squartini et al. show that the relative entropy between the microcanonical and canonical ensembles then grows linearly in $N$. Canonical and microcanonical models with the "same" degree sequence remain measurably different as $N\to\infty$. Details are on the [configuration-models page](./05-configuration-models.md).

(sec-maxent-example)=
## Worked example

All numbers below were computed in Python (numpy/scipy, exact enumeration where stated).

**(a) Labelled vs delabelled vs unlabelled, $N = 3$, $p = 1/2$.**
- *Labelled.* There are 8 labelled graphs, each with $P = 1/8$, so $H_L = 3$ bits.
- *Unlabelled.* There are 4 shapes (with 0, 1, 2 or 3 edges). The unlabelled model makes them equiprobable, so $H_U = 2$ bits.
- *Delabelled.* Pushing $G(3,1/2)$ forward onto shapes gives $(1/8, 3/8, 3/8, 1/8)$ and $H_D = 1.811$ bits.

This confirms $H_D\le H_U\le H_L$.

For $G(4,2)$:
- The 15 labelled graphs split into 3 with two disjoint edges ($\lvert\mathrm{Aut}\rvert = 8$, $4!/8 = 3$) and 12 paths-plus-isolated-node ($\lvert\mathrm{Aut}\rvert = 2$, $4!/2 = 12$).
- So $\mathcal{D}$ gives $(1/5, 4/5)$ and $\mathcal{U}$ gives $(1/2,1/2)$.
- The entropies are $H_L = \log_2 15 = 3.907$, $H_U = 1$ and $H_D = 0.722$ bits.
- Check of {eq}`eq-maxent-label-entropy`: $\tfrac15\log_2 3 + \tfrac45\log_2 12 = 3.185 = H_L - H_D$.

The unlabelled canonical model on $N=3$ has $Z = \sum_{i=0}^{3}q^i$. Its density $d = \tfrac13\langle L\rangle$ agrees with the notes' closed form $\tfrac13\big(1-\tanh\lambda + 1/(1+e^\lambda)\big)$. For example, at $\lambda = 0.5$ both give $d = 0.3051$, and at $\lambda = 2$ both give $0.0517$.

**(b) Fermi–Dirac and equivalence, $N = 1000$, $\langle k\rangle = 10$.**
- $p = 10/999 = 0.010010$, so $\lambda = \ln\big((1-p)/p\big) = 4.594$ and $\bar L = 5000$.
- $H_{\mathrm{can}} = N_{\mathrm p}h(p) = 27\,995.74$ nats and $H_{\mathrm{mic}} = \ln\binom{N_{\mathrm p}}{5000} = 27\,990.57$ nats.
- The difference is $5.173$ nats, matching $\tfrac12\ln(2\pi N_{\mathrm p}p(1-p)) = 5.173$. That is a relative difference of $1.8\times10^{-4}$: the ensembles are equivalent.

**(c) The meditation exercise, $N = 10^6$, $\langle k\rangle = 10$.**
- $N_{\mathrm p} = 5.0\times10^{11}$, $\bar L = 5.0\times10^6$ and $\mathrm{sd}(L) = 2236$, a relative fluctuation of $4.5\times10^{-4}$.
- For any graph with $L = \bar L$, including a PA graph, $-\ln P(G) = N_{\mathrm p}h(p) = 6.26\times10^7$ nats, *exactly* the typical value.
- At $L = \bar L + 1\,\mathrm{sd}$, {eq}`eq-maxent-aep-er` gives a per-pair deviation of $5.1\times10^{-8}$ nats, i.e. $4.1\times10^{-4}$ of $h(p)$.

**(d) Entropic domination.** Fix $N$ and $L$. The number of labelled graphs whose degree distribution is $p_k$ is approximately the number of degree sequences with that empirical distribution, $\approx e^{N H(p_k)}$, times the number of graphs per sequence. By [Bender & Canfield (1978)](doi:10.1016/0097-3165(78)90059-6), the latter is $\approx (2L-1)!!/\prod_i k_i!$ up to an $O(1)$ factor in the exponent.

The $(2L-1)!!$ term is common to both shapes, so per node the log-count differs by $\Delta = [H - \mathbb{E}\ln k!]_{\text{Pois}} - [H - \mathbb{E}\ln k!]_{\text{PL}}$:

| Degree law (mean 10, $k\le1000$) | $\langle k^2\rangle$ | $H(p_k)$ | $\mathbb{E}\ln k!$ | $H - \mathbb{E}\ln k!$ |
|---|---|---|---|---|
| Poisson(10) | 110.0 | 2.561 | 15.587 | −13.026 |
| $p_k\propto(k+11.19)^{-3}$ | 693.6 | 3.178 | 24.720 | −21.542 |

So $\Delta = 8.52$ nats per node. At $N = 10^6$, Poisson-degree graphs outnumber these power-law-degree graphs, and hence outweigh them in $G(N,p)$, by $\approx e^{8.5\times10^6}$.

This is a leading-order heuristic. The Bender–Canfield correction is $O(1)$ in $N$, and it also needs $k_{\max}$ small compared with $\sqrt{L}$, which is borderline here.

**(e) Concentration can fail: the Strauss model on $N = 7$.** Take $P(G)\propto e^{-\lambda_1 L(G) - \lambda_2 t(G)}$, where $t$ is the number of triangles, with $\lambda_1 = 1.55$ and $\lambda_2 = -1$ (rewarding triangles). Exact enumeration over all $2^{21} = 2\,097\,152$ labelled graphs gives:
- $\langle L\rangle = 9.04$ and $\langle t\rangle = 8.37$;
- $P(L)$ has two modes, $L = 4$ ($0.111$) and $L = 21$, the complete graph ($0.089$), separated by a trough of $0.015$ at $L = 14$;
- $P(t = 0) = 0.372$ and $P(t = 35) = 0.089$, but $P(5\le t\le12) = 0.086$.

The "typical" values $\langle L\rangle$ and $\langle t\rangle$ are rarely seen. Sufficiency (A.2) holds, but (A.1) fails, so {prf:ref}`def-maxent-typical-graph` gives no useful notion here.

(sec-maxent-limits)=
## Assumptions and limitations

- **Typicality needs (A.1) and (A.2).** Models defined by a growth process, such as PA or most mechanistic models, usually have no tractable $P(G)$ and no known sufficient statistic. They support only typical *values* of properties or typical *sequences*.
- **A convex $\ln Z$ does not imply concentration.** The notes state Theorem 8.4 as "if things are nice (e.g. $\ln Z$ convex) then $P_{\mathrm{can}}^*$ is sharply peaked". But $\ln Z$ is *always* convex, since its Hessian is a covariance. Convexity guarantees a unique $\boldsymbol\lambda$, not a peaked $P$. The Strauss model in (e) is convex and bimodal.

  In the dense limit, edge–triangle ERGMs with positive triangle weight are asymptotically indistinguishable from mixtures of ER graphs over much of parameter space ([Chatterjee & Diaconis 2013](doi:10.1214/13-AOS1155)). This degeneracy is what [Horvát, Czabarka & Toroczkai (2015)](doi:10.1103/PhysRevLett.114.158701) address; Park & Newman's [mean-field solution of the clustered model](doi:10.1103/PhysRevE.72.026136) shows the corresponding phase transition.
- **Max entropy is a null model, not a mechanism.** $P^*$ answers "what else follows from these constraints alone?". If $G_0$ deviates from $P^*$ in property $g$, then $g$ is *not explained* by $\{f_s\}$. That is information, not a refutation of anything.
- **The answer depends on the sample space.** Labelled, unlabelled and delabelled models of "the same" constraints are different distributions with different degree distributions ({prf:ref}`prop-maxent-label-entropy`). Choose by what the data are: node identities known or not.
- **Microcanonical sets can be empty** (non-graphical constraints), and canonical multipliers may diverge at the boundary of the realisable moment set.
- **Ensembles need not be equivalent** when the number of constraints grows with $N$ (Squartini et al. 2015). Whether to fix the degree sequence exactly or on average is then a modelling choice with measurable consequences.
- **Transcription details in the notes.**
  - Ch. 7 writes the density as $L/N^2$ with $\bar L\approx pN^2$; with $N_{\mathrm p}=\binom N2$ it is $\bar L = pN_{\mathrm p}\approx pN^2/2$.
  - Ch. 7.7 writes $\alpha'$ where $n'$ is meant.
  - Eq. (8.16) drops the minus sign on $\partial\ln Z/\partial\lambda$, but its final closed form is correct (checked numerically above).
  - The caption of the $N=3$ figure lists only three delabelled probabilities; the four are $1/8, 3/8, 3/8, 1/8$.

(sec-maxent-connections)=
## Connections

- **NETS 5116.**
  - $G(N,p)$ and $G(N,L)$ ([Barabási ch. 3 notes](../nets-5116/barabasi/03-random-networks.md)) are the canonical and microcanonical max-entropy models of the edge count. Barabási's "random network" is therefore the *unbiased* null model given only $\langle k\rangle$, not merely the simplest one.
  - Degree-preserving rewiring in [degree correlations](../nets-5116/barabasi/07-degree-correlations.md) samples a microcanonical CM.
  - The empirical-structure comparisons in [Newman ch. 10 notes](../nets-5116/newman/10-structure-of-real-world-networks.md) are implicit typicality tests against such nulls.
- **NETS 6116.**
  - [Sparsity and small worlds](./01-sparsity-and-small-worlds.md) explains why properties need ensembles.
  - [Clustering and assortativity](./02-clustering-and-assortativity.md) are the statistics added in the [dk-series](./06-dk-series.md), which is the hierarchy of max-entropy models with nested sufficient statistics.
  - The [configuration models](./05-configuration-models.md) are the micro, canonical and hypercanonical ensembles for $\mathbf{k}$, with Fermi–Dirac connection probabilities $p_{ij} = 1/(e^{\lambda_i+\lambda_j}+1)$.
  - [Hidden variables and graphons](./07-hidden-variables-and-graphons.md) are hypercanonical ensembles.
  - [Latent-space models](./08-latent-space-models.md) and [SBMs](./09-stochastic-block-models.md) are canonical ensembles with geometric or block constraints.
  - Testing whether data are power-law ([binning and power laws](./03-binning-and-power-laws.md)) is a typical-*value* question.
- **PHYS 7335.**
  - Heterogeneous mean-field thresholds ([HMF](../phys-7335/05-heterogeneous-mean-field.md)) are predictions for the uncorrelated CM. They hold for $G_0$ only to the extent that $G_0$ is typical there.
  - [SIR–percolation](../phys-7335/07-sir-percolation.md) relies on the CM's sparse tree-like limit.
  - [ABC inference](../phys-7335/10-abc-inference.md) is what one does when $P$ is intractable (no sufficient statistic): compare simulated summary statistics, i.e. typical values.
- **NETS 7332.**
  - Graph generative models ([scaling and generative](../nets-7332/basics/08-scaling-and-generative.md)) are evaluated by matching summary-statistic distributions, i.e. typical values rather than typical graphs.
  - ERGMs are the explicit-likelihood counterpart of those models.
  - The WL colour refinement in [GNN expressive power](../nets-7332/basics/06-gnn-expressive-power.md) is about distinguishing *unlabelled* shapes, the same symmetry issue as {prf:ref}`prop-maxent-label-entropy`.

## Self-test

:::{dropdown} Q1. Why is "$G_0$ is the most likely graph in $P$" a bad definition of typicality?
In $G(N,L)$ all allowed graphs are equally likely, so every one is "typical". In $G(N,p)$ with $p<1/2$ the mode is the empty graph, which is wildly atypical because almost all mass sits near $L\approx pN_{\mathrm p}$. Likelihood of a single graph ignores how *many* graphs share its probability.
:::

:::{dropdown} Q2. State the two assumptions behind a well-defined typical graph, and say which one canonical ensembles get for free.
(A.1) Some property $f$ concentrates under $P$. (A.2) $P(G)$ depends on $G$ only through $f(G)$, so $f$ is sufficient. Canonical (Gibbs) ensembles satisfy (A.2) by construction, with the constrained $f_s$ as sufficient statistics. (A.1) must be checked separately, and it fails for the Strauss model.
:::

:::{dropdown} Q3. Derive $G(N,p)$ as a max-entropy model and identify the Fermi–Dirac form.
- Maximise $H$ subject to $\langle L\rangle = L^*$. This gives $P\propto e^{-\lambda L(G)}$.
- $Z = (1+e^{-\lambda})^{N_{\mathrm p}}$, since the pairs factorise, so $\langle L\rangle/N_{\mathrm p} = 1/(e^\lambda+1) = p$.
- Then $P(G) = p^L(1-p)^{N_{\mathrm p}-L}$. Each pair is a fermionic level: occupied (edge) or empty.
:::

:::{dropdown} Q4. A PA graph with $N=10^6$ and $\langle k\rangle = 10$ is a typical graph of which model, and why is its degree distribution nonetheless atypical there?
It is typical in $G(N,p)$ with $p\approx10^{-5}$, because $L$ is the sufficient statistic and its $L$ is typical. Its power-law degree distribution is an atypical *value* of the degree-distribution property. Graphs with binomial degree sequences outnumber power-law ones by roughly $e^{8.5\times10^6}$, but $G(N,p)$ weights all graphs with the same $L$ equally.
:::

:::{dropdown} Q5. How are the micro-, canonical and hypercanonical ensembles related, and how do you sample $G(N,p)$ using $G(N,L)$?
- Canonical is a mixture of microcanonicals weighted by $P_{\mathrm{can}}(f=\phi)$.
- Hypercanonical is a mixture of canonicals over $f^*\sim\rho$.
- To sample $G(N,p)$, draw $L\sim\mathrm{Bin}(N_{\mathrm p},p)$, then a uniform graph with $L$ edges.
:::

:::{dropdown} Q6. Order $H_L$, $H_U$, $H_D$ and say what $H_L - H_D$ measures.
$H_D\le H_U\le H_L$. $H_L - H_D = \mathbb{E}\ln(N!/\lvert\mathrm{Aut}(U)\rvert)$ is the average log number of labellings. It is about $\ln N!$ when typical graphs are asymmetric, and smaller in sparse graphs with many automorphisms.
:::

:::{dropdown} Q7. When does ensemble equivalence break, and why does it matter for the configuration model?
It breaks when the number of constraints is extensive in $N$, for example a full degree sequence. The microcanonical CM and canonical SCM then differ by a relative entropy linear in $N$ (Squartini et al. 2015). Fixing degrees exactly or on average changes predicted properties even as $N\to\infty$.
:::

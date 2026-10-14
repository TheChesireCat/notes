---
title: Hidden-Variable Network Models, Graphons, Exchangeability and Projectivity
short_title: Hidden variables & graphons
subject: NETS 6116 · Topic
description: The two-step hidden-variable recipe behind almost every model in the course, the formulas that turn a connection-probability function into degrees and clustering, graphons as limits of dense graphs, and why exchangeability (Aldous–Hoover) and projectivity pull sparse models in opposite directions.
tags: [hidden-variables, graphons, exchangeability, projectivity, aldous-hoover, graph-limits, hscm, soft-preferential-attachment]
---

:::{tip} TL;DR
- **HVNM recipe.** Draw $x_i \overset{\text{iid}}{\sim} \rho$, then join each pair independently with probability $p_{ij} = p(x_i, x_j)$. Every later model in the course is one of these: SCM/HSCM, latent-space and hyperbolic models, SBMs. By inverse-CDF sampling one can always take $\rho = U(0,1)$, so the model is fully specified by a symmetric function $p:[0,1]^2 \to [0,1]$ (which may depend on $N$).
- **Workhorse formulas.** Expected degree $\bar k(x) = (N-1)\int p(x,x')\rho(x')\,dx'$. Neighbour density $\rho(x' \mid x) = (N-1)\rho(x')p(x',x)/\bar k(x)$. Expected clustering $\bar C(x) = \iint p(x',x'')\,\rho(x'\mid x)\rho(x''\mid x)\,dx'dx''$. In the sparse limit the degree distribution is the $\rho$-mixed Poisson $p_k = \int \rho(x)\, e^{-\bar k(x)}\bar k(x)^k/k!\,dx$.
- **Graphon** = an HVNM with $\rho = U(0,1)$ and an **$N$-independent** $W(x,y)$. Such graphs are **dense**: $\langle k \rangle = (N-1)\iint W$. Graphons are *the* limits of dense graph sequences. If all homomorphism densities $h(F, G_N)$ converge, the limit is $h(F, W)$ for a $W$ that is unique up to measure-preserving relabelling (Lovász–Szegedy).
- **Exchangeability vs sparsity.** If node labels are meaningless, the model must be exchangeable. **Aldous–Hoover**: an infinite jointly exchangeable random graph is a mixture of $W$-random graphs, so it is either dense or empty. *Sparse exchangeable models of infinite graphs do not exist.* $G(N, c/N)$ and the Chung–Lu HSCM escape only because $p$ depends on $N$, and $p \to 0$.
- **Projectivity** (consistency under deleting nodes) is what any realistic *growing* model needs. A projective HVNM cannot have an $N$-dependent $p$. Sparse projective HVNMs work by **expanding the hidden-variable space**: $x \sim U(0, N)$ with a fixed, integrable $p$. Example: the HSCM with $\gamma = 3$, i.e. soft preferential attachment, $p = 1/(\nu\sqrt{x x'} + 1)$.
:::

- **Source.**
  - Krioukov, *Network Science II* lecture notes, ch. 11 (HVNMs) and ch. 12 (graphons, exchangeability, projectivity).
  - Hidden-variable models: [](doi:10.1103/PhysRevLett.89.258702) (Caldarelli, Capocci, De Los Rios & Muñoz 2002), [Söderberg, *Phys. Rev. E* 66, 066121 (2002)](doi:10.1103/PhysRevE.66.066121), [](doi:10.1103/PhysRevE.68.036112) (Boguñá & Pastor-Satorras 2003), [](doi:10.1073/pnas.252631999) (Chung & Lu 2002), and [](doi:10.1002/rsa.20168) (Bollobás, Janson & Riordan 2007, the rigorous "inhomogeneous random graph").
  - Graph limits: [](doi:10.1016/j.jctb.2006.05.002) (Lovász & Szegedy 2006), [](doi:10.1016/j.aim.2008.07.008) (Borgs, Chayes, Lovász, Sós & Vesztergombi 2008), [](doi:10.1007/s00039-010-0044-0) (uniqueness, Borgs, Chayes & Lovász 2010), and the monograph [](doi:10.1090/coll/060) (Lovász 2012).
  - Exchangeability: [](doi:10.1016/0047-259X(81)90099-3) (Aldous 1981), D. Hoover, *Relations on probability spaces and arrays of random variables* (IAS preprint, 1979; no DOI), [](doi:10.48550/arXiv.0712.2749) (Diaconis & Janson 2008), and [](doi:10.1109/TPAMI.2014.2334607) (Orbanz & Roy 2015).
  - Projectivity and the $\gamma = 3$ HSCM: [](doi:10.1214/12-AOS1044) (Shalizi & Rinaldo 2013), [](doi:10.1103/PhysRevE.88.022808) (Krioukov & Ostilli 2013), and [](doi:10.1007/s10955-017-1887-7) (van der Hoorn, Lippner & Krioukov 2018).
- **Builds on.** Maximum-entropy ensembles and ERGMs ([typicality and max-entropy](./04-typicality-and-max-entropy.md)); the SCM and HSCM ([configuration models](./05-configuration-models.md)); dense vs sparse sequences ([sparsity and small worlds](./01-sparsity-and-small-worlds.md)).
- **Notation.** Shared symbols as in [](#notation). $x_i$ is a generic hidden variable with density $\rho(x)$. When it is the expected degree it is written $\kappa_i \sim \rho(\kappa)$. $\rho$ here is never prevalence or a spectral radius. The connection-probability function is $p(x,x')$, written $W(x,y)$ when it is an $N$-independent graphon on $[0,1]^2$. $\bar k(x)$, $\bar t(x)$ and $\bar C(x)$ are the expected degree, triangle count and local clustering of a node at $x$ (Krioukov writes $\bar c(x)$). $h(F,\cdot)$ is a homomorphism density. $G_{ij} \in \{0,1\}$ is the adjacency indicator of the random graph ($= A_{ij}$). $\lambda_{ij}$ are Lagrange multipliers (not spreading rates). $\Pi$ is a probability measure on graphons; Krioukov calls it $\mu$, which here would clash with the recovery rate.

(sec-hvm-setup)=
## Setup and definitions

:::{prf:definition} Hidden-variable network model
:label: def-hvm-hvnm

$\mathrm{HVNM}(N, p, \rho)$ is the random simple graph $G = \{G_{ij}\}_{i<j}$ generated in two steps:

1. $x_i \overset{\text{iid}}{\sim} \rho$ for $i = 1, \dots, N$;
2. conditional on $\mathbf{x}$, $G_{ij} \overset{\text{ind}}{\sim} \mathrm{Bernoulli}\big(p(x_i, x_j)\big)$ for all $i<j$,

where $p$ is a symmetric measurable *connection-probability function*. Either $p$ or $\rho$ (or both) may depend on $N$, and in sparse models they must (see [](#thm-hvm-aldous-hoover)).
:::

The hidden variables abstract node attributes: metadata, "fitness", position in a latent space, or community membership. The model is very general. Krioukov's point is that every model in the rest of the course is an HVNM; they differ only in the choice of $p$ and $\rho$.

:::{prf:definition} Uniform reparametrisation
:label: def-hvm-uniform

Let $F(x) = \int_{-\infty}^x \rho(x')\,dx'$. If $X \sim \rho$ then $U = F(X) \sim U(0,1)$, and conversely $F^{-1}(U) \sim \rho$. Therefore

$$
\mathrm{HVNM}(N, p, \rho) \;=\; \mathrm{HVNM}\big(N, p_u, U(0,1)\big), \qquad p_u(u,u') = p\big(F^{-1}(u), F^{-1}(u')\big).
$$ (eq-hvm-uniform)

The space of HVNMs is therefore the space of symmetric functions $[0,1]^2 \to [0,1]$, possibly indexed by $N$. For a continuous $\rho$, $F^{-1}$ is the quantile function; atoms can be handled with the generalised inverse.
:::

:::{prf:definition} Graphon and $W$-random graph
:label: def-hvm-graphon

A **graphon** is a symmetric measurable $W:[0,1]^2 \to [0,1]$ that does **not** depend on $N$. The HVNM with $\rho = U(0,1)$ and $p = W$ is the **$W$-random graph** $\mathbb{G}(N, W)$; Krioukov calls it the "$p$-random graph". Two graphons are identified, $W \simeq W'$, if $W(x,y) = W'(\sigma(x), \sigma(y))$ a.e. for a measure-preserving $\sigma:[0,1]\to[0,1]$. This is the continuum analogue of relabelling nodes.
:::

In practice "graphon" is also used loosely for the $N$-dependent connection-probability function of any HVNM. Strictly speaking only the $N$-independent case is a graphon.

:::{prf:definition} Homomorphism density
:label: def-hvm-hom

A map $\phi: V(F) \to V(G)$ is a **homomorphism** if every edge of $F$ goes to an edge of $G$. Non-edges are unconstrained, and distinct vertices of $F$ may share an image. Let $\mathrm{hom}(F,G)$ be the number of homomorphisms. Then

$$
h(F,G) = \frac{\mathrm{hom}(F,G)}{N^{\lvert V(F)\rvert}}, \qquad
h(F,W) = \int_{[0,1]^{\lvert V(F)\rvert}} \prod_{\{a,b\} \in E(F)} W(x_a, x_b)\, \prod_{a} dx_a .
$$ (eq-hvm-hom)

$h(F,G)$ is the probability that a uniformly random map is a homomorphism. $h(F,W)$ is the probability that $W$ "generates" every edge of $F$ on $\lvert V(F) \rvert$ fresh uniform points.
:::

:::{prf:definition} Exchangeability
:label: def-hvm-exchangeable

- A sequence $(X_i)_{i \ge 1}$ is **exchangeable** if its law is invariant under every finite permutation of indices.
- A symmetric array $(X_{ij})$ is **jointly exchangeable** if $(X_{ij}) \overset{d}{=} (X_{\pi(i)\pi(j)})$ for every permutation $\pi$; rows and columns are permuted together.
- A network model is **finitely exchangeable** if $P_N(G)$ is invariant under relabelling for each finite $N$, i.e. isomorphic labelled graphs get equal probability. It is **infinitely exchangeable** if the $P_N$ are the marginals of one jointly exchangeable infinite array.
:::

:::{prf:definition} Projectivity
:label: def-hvm-projective

A family of models $\{P_N\}$ is **projective** if there are maps $\pi_{N N'}$ from graphs on $N$ nodes to graphs on $N' < N$ nodes such that:

1. they compose, $\pi_{N'N''} \circ \pi_{NN'} = \pi_{NN''}$; and
2. the push-forward is the smaller model, $(\pi_{NN'})_\sharp P_N = P_{N'}$. That is, generating $G_N \sim P_N$ and applying $\pi_{NN'}$ gives exactly the law of $G_{N'} \sim P_{N'}$.

Equivalently, the model has a **growing formulation**: adding nodes never changes the existing graph.
:::

(sec-hvm-core)=
## Core ideas

### An HVNM is a random mixture of independent-edge graphs

Conditional on $\mathbf{x}$, an HVNM is the *generalised Erdős–Rényi graph* $G(N, \{p_{ij}\})$, with independent edges and pair-specific probabilities. That graph is itself a maximum-entropy model ([](#thm-hvm-ger-ergm)), so an HVNM is a **hypercanonical** ensemble: a canonical ensemble whose parameters $p_{ij} = p(x_i,x_j)$ are random. It is the same three-layer hierarchy (microcanonical → canonical → hypercanonical) as $\mathrm{CM} \to \mathrm{SCM} \to \mathrm{HSCM}$ on the [configuration-model page](./05-configuration-models.md).

| Model | $\rho$ | $p(x,x')$ | Depends on $N$? |
|---|---|---|---|
| $G(N,p)$ | anything | $p$ | only if $p = \langle k\rangle/N$ |
| HSCM / Chung–Lu (sparse) | $\rho(\kappa)$, e.g. Pareto | $\dfrac{1}{\langle k\rangle N/(\kappa\kappa') + 1} \approx \dfrac{\kappa\kappa'}{\langle k\rangle N}$ | yes |
| HSCM in $\lambda$ form | $\rho(\lambda) \propto e^{\alpha\lambda}$ on $(-\infty, R_N]$ | $\dfrac{1}{e^{\lambda+\lambda'}+1}$ | through the support $R_N$ |
| Fitness model (Caldarelli et al.) | fitness density | $f(x)f(x')$, e.g. $\Theta(x+x'-z)$ | usually via a cutoff |
| SBM | block labels | block-constant ([SBM page](./09-stochastic-block-models.md)) | sparse SBM: $\propto 1/N$ |
| Random geometric / latent space | uniform in a space | function of distance ([latent-space page](./08-latent-space-models.md)) | sparse: space volume $\propto N$ |

:::{note} Source note: the HSCM entry in ch. 11
The transcription of ch. 11 §11.2 writes the HSCM connection probability as $1/(kk'/\bar k^2 + 1)$, which *decreases* with the hidden degrees. That is inconsistent with the $k$-generator of Thm 9.7 in ch. 9, $p_k = 1/(\bar k n/(k k') + 1)$, and with the Chung–Lu limit $kk'/(\bar k n)$ used in ch. 12. I use the ch. 9 form.
:::

### Reading structure off $p$ and $\rho$

The formulas below ({ref}`sec-hvm-results`) are all integrals of $p$ against $\rho$. That is why HVNMs are analytically tractable: degrees are first moments of $p(x,\cdot)$, clustering is a triangle integral, and degree correlations come from $\rho(x'\mid x)$. Boguñá & Pastor-Satorras (2003) developed exactly this "propagator" formalism. It gives $P(k'\mid k)$ and $\bar k_{nn}(k)$ in closed form, which is what the degree-block equations on [PHYS 7335](../phys-7335/01-degree-block-formalism.md) need.

### Dense graph limits: three views of convergence

1. **Adjacency-matrix (pixel-picture) convergence.** The *chessboard* graphon $W_G$ of $G$ equals $A_{ij}$ on the square $[\tfrac{i-1}{N}, \tfrac iN) \times [\tfrac{j-1}{N}, \tfrac jN)$. As $N$ grows, the pixel picture of a $\mathbb{G}(N,W)$ sample, with nodes sorted by $x_i$, blurs into $W$. This is intuitive, but it depends on the labelling and is awkward to make precise. It is mostly for visualisation.
2. **Subgraph (homomorphism) density convergence.** $G_N \to W$ if $h(F, G_N) \to h(F,W)$ for **every** finite simple $F$. Small subgraphs act as a basis for comparing graphs: two graphs are close when all their small-pattern densities are close. Homomorphism densities are used because they are algebraically nicer than injective subgraph counts, and for dense graphs the two differ by $O(1/N)$.
3. **Model (sampling) convergence.** Let $P(\cdot \mid W_{G_N})$ be the law of $k$-node $W_{G_N}$-random graphs. $G_N$ converges if these laws converge for every fixed $k$. Krioukov prefers this view because it avoids the "for every finite $F$" clause and is phrased as convergence of *models*.

**Mega-theorem.** These notions, together with convergence in the **cut distance** $\delta_\square(W,W') = \inf_\sigma \sup_{S,T \subseteq [0,1]} \big\lvert \int_{S\times T} (W - W'^\sigma)\big\rvert$, are all equivalent for dense graphs (Borgs et al. 2008; Lovász 2012). The cut distance is my addition here, not in the notes; it is the metric in which the space of graphons, modulo $\simeq$, is **compact**.

### Random limits

For a sequence of *random* graphs, the limit object is in general a **random graphon**: a probability measure $\Pi$ on the compact space of graphons. The model limit is then the mixture $Q(F) = \int P(F \mid W)\, d\Pi(W)$. Krioukov calls this an "ultracanonical" ensemble. A deterministic $W$ is the extreme point $\Pi = \delta_W$.

### Sparse graphs break the theory

If $\langle k \rangle = o(N)$, then $h(K_2, G_N) = \langle k\rangle/N \to 0$, and every other density goes to 0 as well. Every sparse sequence therefore converges to the **zero graphon**, and the theory says nothing. Sparse notions of convergence exist:

- $L^p$ graphons (Borgs, Chayes, Cohn & Zhao, [](doi:10.1090/tran/7543));
- graphexes (Caron & Fox, [](doi:10.1111/rssb.12233); Veitch & Roy, [](doi:10.48550/arXiv.1512.03099));
- local weak (Benjamini–Schramm) convergence ([](doi:10.1214/EJP.v6-96); Aldous & Lyons, [](doi:10.1214/EJP.v12-463)).

Krioukov's assessment: only **local weak convergence** and **projective limits** apply to *ultrasparse* graphs ($\langle k \rangle = O(1)$), and no two sparse notions are known to be equivalent. Model convergence for sparse graphs is unexplored.

### Exchangeability: the formal version of "labels don't matter"

Node labels $1, \dots, N$ are arbitrary. A relabelling either is an automorphism, leaving the labelled graph unchanged, or produces a different labelled graph isomorphic to the original. In both cases a model in which labels are meaningless must give the two graphs equal probability. **Finite exchangeability is therefore a requirement, not an assumption**, for any model of unlabelled structure. Equivalently, the unlabelled graph is a sufficient statistic.

The trouble is the infinite case ([](#thm-hvm-aldous-hoover)). It forces density, and this is the **exchangeability dilemma**:

- exchangeability is required whenever labels carry no meaning, but
- infinitely exchangeable models of sparse graphs cannot exist.

Krioukov half-jokingly calls Aldous–Hoover the "Gödel theorem of network science".

### Projectivity: the formal version of "growth is local"

A realistic growing model must be **local**: adding a node or link cannot instantly rewire the whole existing network. Projectivity is exactly this requirement. If $\{P_N\}$ is projective, then deleting nodes (by the rule $\pi$) from a large sample gives a correctly distributed small sample. Read backwards, $\pi^{-1}$ is a node-addition rule that never touches existing edges. If the model is not projective, no such growth rule exists.

| Model | Projective? | Projective map / growth rule |
|---|---|---|
| Preferential attachment (BA) | yes | delete the newest nodes $N'+1, \dots, N$ |
| $\mathbb{G}(N,W)$, fixed graphon | yes | delete **any** $N-N'$ nodes; grow by drawing $x_N \sim U(0,1)$ and joining it to each $i<N$ with probability $W(x_N, x_i)$ |
| $G(N, \langle k\rangle/N)$ | **no** | $p$ shrinks with $N$, so every existing edge would have to be thinned |
| Chung–Lu HSCM, $p = \kappa\kappa'/(\langle k\rangle N)$ | **no** | same reason |
| HSCM with $\gamma = 3$ (SPA) | **yes**, but hidden | delete the $N-N'$ nodes with the largest $x$ (smallest expected degree) |
| ERGMs with triangle / $k$-star terms | generically **no** | Shalizi & Rinaldo (2013): projective only if the sufficient statistics have *separable increments*, which fails for triangle and $k$-star terms |

**Rule.** In a projective HVNM with a fixed $\rho$, the connection probability **cannot depend on $N$**: the pair $(i,j)$ must have the same marginal edge probability in every $P_N$ that contains both nodes. Sparse *and* projective therefore requires the other lever: let the **support of $\rho$ grow with $N$**, at constant density, while $p$ stays fixed and integrable. Krioukov's meta-observation is that this *hidden-variable-space expansion* is the main mechanism behind projectivity in sparse HVNMs. It returns in random geometric graphs and hyperbolic models, where nodes are sprinkled at constant density into a space of growing volume ([latent-space models](./08-latent-space-models.md)).

Projective and exchangeable formulations can be swapped at finite $N$:

- projective → exchangeable: apply a uniformly random relabelling;
- exchangeable → projective: sort labels by hidden variable.

At $N = \infty$ no uniform random permutation of $\mathbb{N}$ exists, so a sparse projective model has **no** exchangeable version. That is consistent with Aldous–Hoover: in such models, labels (arrival order) do carry meaning. Krioukov's meta-theorem is that every projective model has a projective limit, an infinite object that the finite graphs are marginals of. This is the route to limits of ultrasparse graphs pursued in his lab.

(sec-hvm-results)=
## Key results

### Structural formulas for any HVNM

:::{prf:proposition} Expected degrees, triangles and clustering
:label: prop-hvm-formulas

For $\mathrm{HVNM}(N,p,\rho)$, write $\langle p \rangle = \iint p(x,x')\rho(x)\rho(x')\,dx\,dx'$. Then

$$
\langle L \rangle = \binom N2 \langle p\rangle, \qquad \langle k\rangle = (N-1)\langle p \rangle, \qquad \bar k(x) = (N-1)\int p(x,x')\rho(x')\,dx',
$$ (eq-hvm-degree)

$$
\bar t(x) = \binom{N-1}{2}\iint p(x,x')p(x',x'')p(x'',x)\,\rho(x')\rho(x'')\,dx'dx'', \qquad \langle t \rangle_{\text{total}} = \frac N3 \int \bar t(x)\rho(x)\,dx,
$$ (eq-hvm-triangles)

$$
\rho(x' \mid x) = \frac{(N-1)\,\rho(x')\,p(x',x)}{\bar k(x)}, \qquad
\bar C(x) = \iint p(x',x'')\,\rho(x'\mid x)\,\rho(x''\mid x)\,dx'dx'' = \frac{2(N-1)}{N-2}\,\frac{\bar t(x)}{\bar k(x)^2} \approx \frac{2\,\bar t(x)}{\bar k(x)^2},
$$ (eq-hvm-clustering)

and the mean clustering is $\bar C = \int \bar C(x)\rho(x)\,dx$, excluding nodes of degree 0 and 1.
:::

:::{dropdown} Derivation, and two corrections to the transcribed notes
- **Degrees.** $k_i = \sum_{j \ne i} G_{ij}$. Conditional on $x_i = x$, each of the $N-1$ terms has mean $\int p(x,x')\rho(x')dx'$. Averaging over $x$ gives $\langle k\rangle$, and $\langle L\rangle = N\langle k\rangle/2$.
- **Triangles at $x$.** There are $\binom{N-1}2$ pairs $\{j,l\}$, and the three edges of $ijl$ are conditionally independent given the hidden variables. Each triangle is counted at its three vertices, hence the $N/3$.
- **Neighbour density.** By Bayes, the hidden variable of a node $j$ *given that $j$ is adjacent to $i$* has density $\propto \rho(x')p(x',x)$. The normaliser is $\int \rho p = \bar k(x)/(N-1)$.
- **Clustering.** Given two neighbours of $i$ with hidden variables $x', x''$ drawn independently from $\rho(\cdot\mid x)$, they are adjacent with probability $p(x',x'')$. Substituting $\rho(\cdot\mid x)$:
  $\bar C(x) = \frac{(N-1)^2}{\bar k(x)^2}\iint p\,p\,p\,\rho\rho = \frac{(N-1)^2}{\bar k(x)^2}\cdot\frac{\bar t(x)}{\binom{N-1}{2}} = \frac{2(N-1)}{N-2}\frac{\bar t(x)}{\bar k(x)^2}.$
  For a mixed-Poisson degree $E[k(k-1)\mid x] = \bar k(x)^2$, so this agrees with $2t_i/(k_i(k_i-1))$ to leading order.

*Corrections.*

- The transcription of eq. (11.6) is garbled; the integrand should be $p(x',x'')\rho(x'\mid x)\rho(x''\mid x)$.
- Eq. (11.8) has the prefactor $\frac{n-2}{n-1}$, but the computation above gives its reciprocal $\frac{N-1}{N-2}$. The [worked example](#sec-hvm-example) checks this: with $W = xy$ the reciprocal makes $\bar C(x) = 4/9$ exactly, for every $N$.
- Both versions $\to 1$ as $N \to \infty$, so nothing asymptotic changes.
:::

:::{prf:proposition} Degree distribution: mixed Poisson in the sparse limit
:label: prop-hvm-mixed-poisson

Given $x_i = x$, $k_i$ is a sum of $N-1$ independent Bernoullis with mean $\bar k(x)$. If $\max_{x'} p(x,x') \to 0$, then $k_i \mid x \Rightarrow \mathrm{Poisson}(\bar k(x))$ (Le Cam), and

$$
p_k = \int \rho(x)\, e^{-\bar k(x)}\frac{\bar k(x)^k}{k!}\,dx .
$$ (eq-hvm-mixed-poisson)

A Pareto $\rho(\kappa)$ with $\bar k(\kappa) = \kappa$ therefore gives a power-law $p_k$ with the same exponent $\gamma$ ([power laws](./03-binning-and-power-laws.md)).
:::

### HVNMs are hypercanonical ERGMs

:::{prf:theorem} The generalised ER graph is an ERGM
:label: thm-hvm-ger-ergm

$G(N,\{p_{ij}\})$, with independent edges of probabilities $p_{ij}$, is the maximum-entropy ensemble with the $\binom N2$ sufficient statistics $f_{ij}(G) = G_{ij}$:

$$
P(G) = \prod_{i<j} p_{ij}^{G_{ij}}(1-p_{ij})^{1-G_{ij}} = \frac{1}{Z}\exp\Big(-\sum_{i<j}\lambda_{ij}G_{ij}\Big), \quad
Z = \prod_{i<j}(1 + e^{-\lambda_{ij}}), \quad p_{ij} = \frac{1}{e^{\lambda_{ij}} + 1}.
$$ (eq-hvm-ger)
:::

:::{dropdown} Proof sketch, and why it is a "dull" ERGM
Factorise $\exp(-\sum\lambda_{ij}G_{ij}) = \prod_{i<j} e^{-\lambda_{ij}G_{ij}}$. Each factor normalises to $1 + e^{-\lambda_{ij}}$, so the edges are independent with $P(G_{ij} = 1) = e^{-\lambda_{ij}}/(1+e^{-\lambda_{ij}}) = 1/(e^{\lambda_{ij}}+1)$. Every $p_{ij} \in (0,1)$ is reached by $\lambda_{ij} = \ln(1/p_{ij} - 1)$.

The model is degenerate as an ERGM. With as many constraints as dyads, the corresponding *microcanonical* ensemble fixes every $G_{ij}$ and contains one graph. An HVNM is a hypercanonical mixture of these canonical ensembles, with random $p_{ij} = p(x_i, x_j)$. The SCM is the special case $\lambda_{ij} = \lambda_i + \lambda_j$ ([configuration models](./05-configuration-models.md)).
:::

### Graph limits

:::{prf:theorem} Lovász–Szegedy representation of dense limits
:label: thm-hvm-lovasz-szegedy

Let $(G_N)$ be graphs with $\lvert V(G_N)\rvert \to \infty$. Suppose $h(F, G_N) \to f(F)$ for every finite simple graph $F$. Then there is a graphon $W$ with $f(F) = h(F,W)$ for all $F$, and $W$ is unique up to $\simeq$ (weak isomorphism). Conversely, $\mathbb{G}(N, W) \to W$ almost surely.
:::

:::{dropdown} What is easy and what is hard
- **Easy direction.** For $\mathbb{G}(N,W)$, $E[\hom(F, G_N)]/N^{\lvert V(F)\rvert} = h(F,W) + O(1/N)$. The only discrepancy comes from non-injective maps, which are $O(1/N)$ of all maps. Concentration (bounded differences) and Borel–Cantelli then give almost-sure convergence. This is "trivial" in the notes' words.
- **Hard direction.** *Existence* of a limit object for an arbitrary convergent sequence. Lovász & Szegedy (2006) prove it with a regularity lemma (approximating $G_N$ by step functions) and the martingale convergence theorem. *Uniqueness* up to measure-preserving maps is Borgs, Chayes & Lovász (2010): the moments $h(F,W)$ determine $W$ up to $\simeq$.
- **Interpretation.** It is a representation theorem. Convergent sequences of dense graphs are, in the limit, $W$-random graphs. Homomorphism densities are sufficient statistics, so dense limits are (mixtures of) ERGMs whose sufficient statistics are all subgraph densities. This links to the subgraph-based hierarchy of the [dk-series](./06-dk-series.md).
:::

:::{prf:theorem} Model convergence (Krioukov's preferred form)
:label: thm-hvm-model-convergence

Let $(G_N)$ be graphs of size $N$, and suppose the law $P(H \mid W_{G_N})$ of $W_{G_N}$-random graphs $H$ converges to some $Q(H)$ for each fixed size of $H$. Then there is a unique graphon $W$, up to $\simeq$, with $Q(H) = P(H \mid W)$. For random sequences, $W$ may itself be random: $Q = \int P(\cdot\mid W)\,d\Pi(W)$.
:::

### Exchangeability theorems

:::{prf:theorem} de Finetti
:label: thm-hvm-definetti

An infinite exchangeable sequence of $\{0,1\}$-valued random variables is a mixture of iid Bernoullis. There is a probability measure $\nu$ on $[0,1]$ with $P(X_1 = a_1, \dots, X_n = a_n) = \int_0^1 q^{\sum a_i}(1-q)^{n - \sum a_i}\,d\nu(q)$ for every $n$.
:::

:::{prf:theorem} Aldous–Hoover for random graphs
:label: thm-hvm-aldous-hoover

Let $(G_{ij})_{i<j}$, $i,j \in \mathbb{N}$, be a jointly exchangeable symmetric $\{0,1\}$-array, i.e. the adjacency matrix of an infinitely exchangeable random graph. Then it is a mixture of $W$-random graphs. There is a random graphon $W \sim \Pi$ such that, given $W$,

$$
G_{ij} = \mathbb{1}\{U_{ij} < W(U_i, U_j)\}, \qquad U_i, U_{ij} \overset{\text{iid}}{\sim} U(0,1).
$$ (eq-hvm-aldous-hoover)

**Corollary (no sparse exchangeable graphs).** $E[L_N \mid W] = \binom N2 \int W$, so $L_N/\binom N2 \to \int W$ almost surely. The graph is therefore either **dense** (on the event $\int W > 0$) or **empty** (on $W = 0$ a.e.). It is never sparse with $L_N = o(N^2)$ and $L_N > 0$.
:::

:::{dropdown} Remarks on the proof and the history
- Aldous (1981) and Hoover (1979) proved the representation for general exchangeable arrays, with an additional global variable $U_\emptyset$ that, for graphs, indexes the mixing measure $\Pi$. This was two decades before graphons were defined (around 2003–2006), so neither called $W$ a graphon. Diaconis & Janson (2008) made the connection explicit: extreme points of exchangeable random graphs correspond to $W$-random graphs, and the laws of graph limits correspond to $\Pi$.
- **Corollary.** Given $W$, the $G_{ij}$ are dissociated: disjoint blocks are independent. The edge density of the first $N$ nodes is a U-statistic, whose almost-sure limit is $\iint W$ by the strong law for U-statistics. A sparse sequence has $\int W = 0$, which forces $W = 0$ a.e., and so no edges at all.
- **Apparent counterexamples.** $G(N, c/N)$ and the Chung–Lu HSCM with $p = \kappa\kappa'/(\langle k\rangle N)$ are *finitely* exchangeable for each $N$. They are not marginals of one infinite exchangeable array, because $p$ changes with $N$. Their graphon $\to 0$, so the $N \to \infty$ limit is the empty graph.
:::

### Projectivity of the $\gamma = 3$ HSCM

:::{prf:proposition} The HSCM is projective iff $\gamma = 3$, and then it is soft preferential attachment
:label: prop-hvm-spa

Take $\mathrm{HSCM}(N, \mathrm{Pareto}[\langle k \rangle, \gamma])$, with $\alpha = \gamma - 1$ and $\nu = \frac{1}{\langle k\rangle}\big(\frac{\gamma-1}{\gamma-2}\big)^2$. Reparametrise the hidden degree as $x = N u \sim U(0,N)$, i.e. $\kappa = \kappa_{\min}(N/x)^{1/\alpha}$. The connection probability becomes

$$
p_x(x,x') = \frac{1}{\nu\, N^{1-2/\alpha}(x x')^{1/\alpha} + 1}
\;\approx\; p_x^{\mathrm{CL}} = c\,(x x')^{-1/\alpha}\,N^{\frac 2\alpha - 1}, \qquad c = \frac1\nu = \langle k\rangle\Big(\frac{\gamma-2}{\gamma-1}\Big)^2 .
$$ (eq-hvm-x-generator)

The $N$-dependence disappears **iff $\alpha = 2$, i.e. $\gamma = 3$**, where $p_x = 1/(\nu\sqrt{x x'} + 1)$ with $\nu = 4/\langle k\rangle$. In that case the model is projective by space expansion. Grow it by taking $x_{(N)}$ as the next point of a rate-1 Poisson process on $\mathbb{R}_+$, and joining node $N$ to each $i < N$ with probability $p_x(x_{(N)}, x_{(i)})$. The projective map deletes the nodes with the largest $x$. Because $\bar k(x) \approx \frac{\langle k\rangle}{2}\sqrt{N/x}$, the probability of joining $i$ is $\propto 1/\sqrt{x_{(i)}} \propto \bar k_i$. This is **soft preferential attachment (SPA)**: attachment to *expected* rather than actual degree.
:::

:::{dropdown} Derivation
1. **Pareto via inverse CDF.** $\rho(\kappa) = \alpha\kappa_{\min}^\alpha \kappa^{-\gamma}$ on $[\kappa_{\min},\infty)$, with $\kappa_{\min} = \langle k\rangle\frac{\gamma-2}{\gamma-1}$ so that $E\kappa = \langle k\rangle$. The tail is $P(\kappa > t) = (t/\kappa_{\min})^{-\alpha}$, so $u = (\kappa/\kappa_{\min})^{-\alpha} \sim U(0,1)$ and $\kappa = \kappa_{\min}u^{-1/\alpha}$.
2. **Substitute into the SCM-type $k$-generator** $p = 1/(\langle k\rangle N/(\kappa\kappa') + 1)$. This gives $\langle k\rangle N/(\kappa\kappa') = \frac{\langle k\rangle}{\kappa_{\min}^2}N(uu')^{1/\alpha} = \nu N (uu')^{1/\alpha}$. With $u = x/N$, this becomes $\nu N^{1-2/\alpha}(xx')^{1/\alpha}$. The exponent of $N$ vanishes iff $\alpha = 2$.
3. **Expected degree at $\gamma = 3$.** In the Chung–Lu approximation, $\bar k(x) \approx \int_0^N \frac{c}{\sqrt{xx'}}dx' = 2c\sqrt{N/x} = \frac{\langle k\rangle}2\sqrt{N/x}$. Averaging over $x \sim U(0,N)$ gives $\frac{\langle k\rangle}{2}\int_0^1 v^{-1/2}dv = \langle k\rangle$, as it should. The newest node ($x \approx N$) has $\bar k = O(1)$, while the oldest have $\bar k \sim \sqrt N$, which is the natural cutoff for $\gamma = 3$.
4. **Projectivity.** The points of a homogeneous Poisson process on $[0,N]$ are a restriction of those on $[0, N+1]$, and $p_x$ is $N$-free. Deleting all nodes with $x > N'$ therefore gives exactly a size-$N'$ sample, approximately for a fixed node count and exactly in the Poissonised version. For $\gamma \neq 3$, the $N^{2/\alpha-1}$ factor changes every existing pair's probability when a node is added. In the $\lambda$ form the same obstruction appears as an $N$-dependent density of $\lambda$-points on $(-\infty, R_N]$.
:::

(sec-hvm-example)=
## Worked example

All numbers below were computed with numpy and networkx (seeded simulations).

**1. Homomorphism densities of a 4-node graph.** Take the edges $\{12, 23, 24, 34\}$: a triangle $234$ with a pendant node 1. The notes' figure shows this graph; its printed matrix is not symmetric, but this is the symmetric reading. The degrees are $(1,3,2,2)$, so

| Pattern $F$ | Formula | $h(F,G)$ |
|---|---|---|
| edge $K_2$ | $\sum_{ij}A_{ij}/N^2 = 8/16$ | $0.5$ |
| cherry (path on 3 nodes) | $\sum_i k_i^2/N^3 = 18/64$ | $0.28125$ |
| triangle $K_3$ | $\operatorname{tr}A^3/N^3 = 6/64$ | $0.09375$ |
| 4-cycle $C_4$ | $\operatorname{tr}A^4/N^4 = 28/256$ | $0.109375$ |

The single triangle yields $\hom(K_3,G) = 3! = 6$ maps, which is why homomorphism and injective counts differ by automorphism factors.

**2. The rank-one graphon $W(x,y) = xy$, a dense "Chung–Lu".** Exact predictions from [](#prop-hvm-formulas):

- $\bar k(x) = (N-1)\,x/2$, so degrees are roughly uniform on $[0, (N-1)/2]$ and $\langle k \rangle = (N-1)/4$; the edge density is $h(K_2,W) = 1/4$.
- $\rho(x'\mid x) = 2x'$, independent of $x$: neighbours are biased toward large $x'$ in the same way for everyone, so there are no degree correlations.
- $\bar C(x) = \big(\int_0^1 x'\cdot 2x'\,dx'\big)^2 = (2/3)^2 = 4/9$ for every $x$. The same value follows from $\frac{2(N-1)}{N-2}\bar t(x)/\bar k(x)^2$ with $\bar t(x) = \binom{N-1}{2}x^2/9$, which confirms the corrected prefactor.
- $h(K_3,W) = \big(\int x^2\big)^3 = 1/27 \approx 0.0370$.

One sample with $N = 2000$:

| Quantity | Simulated | Exact given the drawn $x$ | Graphon value |
|---|---|---|---|
| $\langle k\rangle$ | 499.2 | 499.1 | 499.75 |
| edge density $h(K_2,G)$ | 0.2496 | | 0.25 |
| mean $C_i$ (nodes with $k_i>1$) | 0.4420 | 0.4422 | 0.4444 |
| $h(K_3,G)$ | 0.0366 | 0.0367 | 0.0370 |
| slope of $k_i$ against $x_i$ | 998.4 | 999.0 | $(N-1)/2 = 999.5$ |

Clustering ($\approx 4/9$) is far above the edge density ($1/4$), and it does **not** decay with $N$. That is the dense-graph signature. The same structure in a sparse HSCM has $\bar C \to 0$.

**3. Why sparse sequences have the zero graphon.** $h(K_2,G_N) = \langle k\rangle/N$:

| $N$ | $G(N, 0.1)$ | $G(N, 5/N)$ |
|---|---|---|
| 100 | 0.0990 | 0.0495 |
| 1 000 | 0.0999 | 0.0050 |
| 10 000 | 0.1000 | 0.0005 |

**4. SPA ($\gamma = 3$, $\langle k\rangle = 10$, $\nu = 0.4$).** Draw $x$ as a rate-1 Poisson process and connect with $p = 1/(0.4\sqrt{xx'} + 1)$, with no $N$ anywhere in $p$:

| $N$ | simulated $\langle k\rangle$ | expected $\langle k\rangle$ from $p$ | Chung–Lu expectation | $k_{\max}$ |
|---|---|---|---|---|
| 2 000 | 9.58 | 9.43 | 9.66 | 238 |
| 8 000 | 9.86 | 9.88 | 9.96 | 437 |

The mean degree approaches $\langle k\rangle = 10$ from below. The finite-$N$ deficit comes from the newest nodes, which have fewer later arrivals to connect to. $k_{\max}$ grows like $\sqrt N$: $437/238 \approx 1.84$ against $\sqrt 4 = 2$.

## Assumptions and limitations

- **Conditional independence of edges.** Given $\mathbf{x}$, edges are independent. Any clustering or correlation must come from $p$ and $\rho$; there is no "triadic closure" term. That makes the model tractable, and it is also why dense $W$ easily gives non-vanishing clustering while sparse $N$-dependent $p$ typically does not (except geometric $p$; see [latent-space models](./08-latent-space-models.md)).
- **Dense or empty.** Graphon theory and Aldous–Hoover concern dense graphs. Real networks are sparse, often ultrasparse ([sparsity](./01-sparsity-and-small-worlds.md)), so a fixed graphon is the wrong limit object. Fitting a graphon to one sparse network (e.g. by SBM or histogram estimators) is a finite-$N$ approximation, not a limit statement.
- **Exchangeability vs projectivity.** You can have finite exchangeability and sparsity ($N$-dependent $p$), or projectivity and sparsity (space expansion). You cannot have infinite exchangeability and sparsity. Sparse exchangeable alternatives change the notion of exchangeability itself: graphexes are exchangeable in a continuous "time/label" space, not in the node index.
- **Identifiability.** A graphon is identified only up to measure-preserving maps, and from finite data only up to estimation error in cut distance. "The" hidden variables are not uniquely recoverable without extra structure, such as monotone degree ($W(x,\cdot)$ increasing) or geometry.
- **Transcription caveats.** The local source is a machine transcription of handwritten notes. Three spots are corrected on this page: the ch. 11 HSCM formula, eq. (11.6), and the prefactor in (11.8). The chessboard example matrix in ch. 12 is also not symmetric.

## Connections

- **NETS 5116.**
  - $G(N,p)$ is the constant graphon ([Barabási ch. 3 notes](../nets-5116/barabasi/03-random-networks.md)).
  - BA preferential attachment is the prototypical projective growing model, and SPA is its maximum-entropy "soft" cousin ([Barabási ch. 5 notes](../nets-5116/barabasi/05-barabasi-albert-model.md)).
  - Bianconi–Barabási fitness is a hidden variable in a *growing* model, which contrasts with the static Caldarelli et al. fitness HVNM ([Barabási ch. 6 notes](../nets-5116/barabasi/06-evolving-network-framework.md)).
  - $\rho(x'\mid x)$ is the hidden-variable version of $\bar k_{nn}(k)$ ([Barabási ch. 7 notes](../nets-5116/barabasi/07-degree-correlations.md)).
- **NETS 6116.**
  - This page is the umbrella for the models that follow. The SCM/HSCM are HVNMs with Fermi–Dirac $p$ ([configuration models](./05-configuration-models.md)). Latent-space and hyperbolic models are HVNMs with geometric $p$, projective by space expansion ([latent space](./08-latent-space-models.md)). SBMs use block graphons, with degree-corrected versions mixing HSCM and blocks ([SBMs](./09-stochastic-block-models.md)).
  - Subgraph densities as sufficient statistics link to the [dk-series](./06-dk-series.md), and HVNM clustering formulas to [clustering and assortativity](./02-clustering-and-assortativity.md).
- **PHYS 7335.** Annealed (degree-class) mean-field theory needs exactly $P(k'\mid k)$ and $p_k$, which an HVNM supplies in closed form via $\rho(x'\mid x)$ and the mixed-Poisson law ([degree-block formalism](../phys-7335/01-degree-block-formalism.md), [heterogeneous mean-field](../phys-7335/05-heterogeneous-mean-field.md)). For a rank-one $p(x,x') = f(x)f(x')$ the two standard thresholds coincide: the operator's top eigenvalue is $\Lambda_{\max} \approx N\int f^2\rho$, which equals $\langle k^2\rangle/\langle k\rangle$, so $1/\Lambda_{\max} = \langle k\rangle/\langle k^2\rangle$ ([quenched mean-field](../phys-7335/06-quenched-mean-field.md)).
- **NETS 7332.**
  - Graphons are the standard device for **transferability** of GNNs: a GNN trained on $\mathbb{G}(N,W)$ converges to a "graphon neural network" as $N\to\infty$ ([](doi:10.48550/arXiv.2006.03548), Ruiz, Chamon & Ribeiro 2020).
  - Homomorphism counts from trees characterise 1-WL equivalence ([](doi:10.48550/arXiv.1802.08876), Dell, Grohe & Rattan 2018), which links graph limits to [GNN expressive power](../nets-7332/basics/06-gnn-expressive-power.md).
  - Graphon estimation is the classical-statistics baseline for [graph generative models](../nets-7332/basics/08-scaling-and-generative.md).

## Self-test

:::{dropdown} Q1. Why can every HVNM be written with $\rho = U(0,1)$, and what then parametrises the model?
Inverse-CDF sampling: $u = F(x) \sim U(0,1)$, so replace $p$ with $p_u(u,u') = p(F^{-1}(u),F^{-1}(u'))$. The model is then a symmetric function $[0,1]^2\to[0,1]$, possibly depending on $N$. If it does not depend on $N$, it is a graphon.
:::

:::{dropdown} Q2. Write $\bar k(x)$, $\rho(x'\mid x)$ and $\bar C(x)$ for a general HVNM. Compute $\bar C$ for $W = xy$.
$\bar k(x) = (N-1)\int p(x,x')\rho(x')dx'$; $\rho(x'\mid x) = (N-1)\rho(x')p(x',x)/\bar k(x)$; $\bar C(x) = \iint p(x',x'')\rho(x'\mid x)\rho(x''\mid x)$. For $W=xy$, $\rho(x'\mid x) = 2x'$, so $\bar C = (\int 2x'^2)^2 = 4/9$, independent of $x$ and of $N$.
:::

:::{dropdown} Q3. State Aldous–Hoover for graphs and its consequence for sparse networks. Why are $G(N, c/N)$ and Chung–Lu not counterexamples?
An infinitely (jointly) exchangeable random graph is a mixture of $W$-random graphs. Its edge density converges to $\int W$, so it is dense or empty. $G(N,c/N)$ and Chung–Lu are only *finitely* exchangeable: their $p$ depends on $N$, so they are not projections of one infinite exchangeable array, and their graphons tend to 0 (empty limit).
:::

:::{dropdown} Q4. What is projectivity, why should a realistic growing model have it, and why can't a projective HVNM with a fixed $\rho$ have an $N$-dependent $p$?
Push-forward consistency under a compatible family of node-deletion maps; equivalently, a growth rule that never alters existing edges (locality). If $p$ depended on $N$, the marginal probability of an existing edge $ij$ would change when nodes are added, contradicting $(\pi_{NN'})_\sharp P_N = P_{N'}$.
:::

:::{dropdown} Q5. How do sparse models achieve projectivity anyway? Give the HSCM example.
Expand the hidden-variable space: $x \sim U(0,N)$ (a Poisson process at unit density) with a fixed integrable $p$. For the Pareto HSCM, $p_x = 1/(\nu N^{1-2/\alpha}(xx')^{1/\alpha}+1)$ is $N$-free iff $\alpha = 2$ ($\gamma = 3$). The model is then soft preferential attachment, and the projective map deletes the nodes with the largest $x$ (lowest expected degree).
:::

:::{dropdown} Q6. Name three notions of dense-graph convergence and say which ones extend to ultrasparse graphs.
Pixel-picture/adjacency, homomorphism-density, and model (sampling) convergence, plus cut distance; all are equivalent for dense graphs. For ultrasparse graphs every density $\to 0$. According to the notes, only local weak (Benjamini–Schramm) convergence and projective limits are useful there.
:::

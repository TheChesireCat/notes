---
title: Stochastic Block Models as Maximum-Entropy Ensembles
short_title: Stochastic block models
subject: NETS 6116 · Topic
description: The SBM and degree-corrected SBM in their hypercanonical, canonical and microcanonical forms, their sufficient statistics and self-consistency conditions, and the detectability limits of community inference in sparse SBMs.
tags: [stochastic-block-model, dc-sbm, community-structure, maximum-entropy, graphons, detectability, kesten-stigum]
---

:::{tip} TL;DR
- An **SBM** is a latent-variable model in which each node's hidden variable is a discrete **community label** $\sigma_i \in \{1,\dots,q\}$, and edges are independent with probability $B_{\sigma_i \sigma_j}$. It is the discrete counterpart of a soft random geometric graph: a **block graphon** $W(x,y)$ that is constant on rectangles $I_c \times I_{c'}$.
- Its **sufficient statistics** are the block edge counts $L_{cc'}$. The canonical (soft) SBM is the maximum-entropy ensemble with given expected $L_{cc'}$: $P(G) = Z^{-1}\exp(-\sum_{c \le c'} \lambda_{cc'} L_{cc'}(G))$ with $B_{cc'} = 1/(e^{\lambda_{cc'}}+1)$. As with the configuration models, there are **three versions**: hypercanonical (random labels), canonical (fixed labels, soft $L_{cc'}$), microcanonical (exact $L_{cc'}$). All three make sense, because every statistic is discrete.
- A homogeneous SBM has thin-tailed degrees (a mixture of $q$ Poissons in the sparse limit). The **degree-corrected SBM** (DC-SBM = CM + SBM) adds per-node expected degrees $\kappa_i$: in the classical limit $p_{ij} = B_{\sigma_i\sigma_j}\kappa_i\kappa_j/(\langle\kappa\rangle b N)$. Then $\kappa_i$ is the expected degree **only if** $\sum_{c'} s_{c'} B_{cc'} = b$ is the same for every block.
- "Community structure" has no agreed definition, and it is **not** "high modularity". Sparse ER and random regular graphs have modularity bounded away from zero, and random hyperbolic graphs have modularity $\to 1$. The SBM gives communities a generative meaning instead.
- **Detectability (beyond the notes).** In the sparse symmetric SBM with $B_{\mathrm{in}} = c_{\mathrm{in}}/N$ and $B_{\mathrm{out}} = c_{\mathrm{out}}/N$, labels better than chance can be recovered efficiently iff $(c_{\mathrm{in}}-c_{\mathrm{out}})^2 > q^2\langle k\rangle$. This is the Kesten–Stigum bound; for $q=2$ it reads $(c_{\mathrm{in}}-c_{\mathrm{out}})^2 > 2(c_{\mathrm{in}}+c_{\mathrm{out}})$. Below it, no algorithm does better than chance for $q=2$.
:::

- **Source.** Krioukov, *Network Science II* lecture notes, ch. 14 "Stochastic block models". Primary papers:
  - SBM: Holland, Laskey & Leinhardt, *Social Networks* 5, 109 (1983): [](doi:10.1016/0378-8733(83)90021-7).
  - DC-SBM: Karrer & Newman, *PRE* 83, 016107 (2011): [](doi:10.1103/PhysRevE.83.016107).
  - Ensemble entropies: Peixoto, *PRE* 85, 056122 (2012): [](doi:10.1103/PhysRevE.85.056122); microcanonical inference: Peixoto, *PRE* 95, 012317 (2017): [](doi:10.1103/PhysRevE.95.012317).
  - Detectability: Decelle, Krzakala, Moore & Zdeborová, *PRE* 84, 066106 (2011): [](doi:10.1103/PhysRevE.84.066106); Mossel, Neeman & Sly, *PTRF* 162, 431 (2015): [](doi:10.1007/s00440-014-0576-6); Massoulié, *STOC* 2014: [](doi:10.1145/2591796.2591857); Krzakala et al., *PNAS* 110, 20935 (2013): [](doi:10.1073/pnas.1312486110).
  - Review: Abbe, *JMLR* 18(177) (2018): [](doi:10.48550/arXiv.1703.10146).
- **Builds on.** Maximum-entropy ensembles ([Typicality and maximum entropy](./04-typicality-and-max-entropy.md)), the CM/SCM/HSCM triple ([Configuration models](./05-configuration-models.md)), and hidden-variable models and graphons ([Hidden variables and graphons](./07-hidden-variables-and-graphons.md)).
- **Notation.** Shared symbols as in [](#notation). Here $B$ is the **block matrix**, not the non-backtracking matrix; the non-backtracking matrix appears only in the detectability section, written $B_{\mathrm{NB}}$. Page-specific symbols:
  - $q$: number of blocks.
  - $\sigma_i$: block of node $i$ (Krioukov: $c_i$).
  - $N_c$ and $s_c = N_c/N$: size and fraction of block $c$.
  - $L_{cc'}(G)$: number of edges between blocks $c$ and $c'$, or within $c$ when $c = c'$ (Krioukov: $m_{cc'}$).
  - $N_{cc'}$: number of node pairs available to those edges.
  - $\lambda_{cc'}$, $\lambda_i$: Lagrange multipliers.
  - $\kappa_i$: expected degree in the DC-SBM (Krioukov: $k_i$), with density $\rho(\kappa)$ and mean $\langle\kappa\rangle$.
  - $W$: the block graphon (Krioukov: $p(x,x')$).

(sec-sbm-setup)=
## Setup and definitions

Krioukov's framing is a direct analogy with latent-space models ([Latent-space models](./08-latent-space-models.md)). In a soft random geometric graph (SRGG), the hidden variable $x_i$ is a **position**, and the connection probability $W(x,x')$ varies smoothly with distance. In an SBM, $x_i$ encodes only a **community membership**, so $W$ is piecewise constant. Real networks probably sit in between, with a "fuzzy" graphon that has block-like structure and smooth gradients (notes §14.1).

:::{prf:definition} Block graphon
:label: def-sbm-block-graphon

Partition $[0,1]$ into intervals $I_1,\dots,I_q$ with lengths $s_c = \lvert I_c\rvert$, and let $B$ be a symmetric $q\times q$ matrix with entries in $[0,1]$. The **block graphon** is

$$
W(x,y) = \sum_{c,c'=1}^{q} B_{cc'}\,\mathbf{1}\{x \in I_c,\ y \in I_{c'}\}.
$$ (eq-sbm-block-graphon)

A node with hidden variable $x_i$ belongs to **community** (colour) $\sigma_i = c$ iff $x_i \in I_c$.
:::

Special cases show how much the block matrix can express:
- $q = 1$ gives ER $G(N,p)$.
- With $q = 2$, $B_{12} = 0$ gives two disjoint ER graphs, and $B_{11} = B_{22} = 0$ gives a bipartite ER graph.
- A $q \times q$ matrix with $B_{cc} = p > p' = B_{c\neq c'}$ is the **planted partition** (assortative) model. The Girvan–Newman benchmark is an instance ([Barabási ch. 9](../nets-5116/barabasi/09-community-structure.md)).

The three ensembles mirror the ER triple $G(N,\rho)$ / $G(N,p)$ / $G(N,L)$ and the HSCM / SCM / CM triple.

:::{prf:definition} Hypersoft SBM (HS-SBM)
:label: def-sbm-hs

$\mathrm{HS\text{-}SBM}(N, W)$ is the hidden-variable model with uniform hidden variables and a block graphon:
1. draw $x_i \stackrel{\mathrm{iid}}{\sim} \mathcal{U}(0,1)$ for $i = 1,\dots,N$, so $\sigma_i$ is categorical with probabilities $s_c$;
2. draw $A_{ij} \stackrel{\mathrm{ind}}{\sim} \mathrm{Bernoulli}\big(B_{\sigma_i\sigma_j}\big)$ for $i<j$.

Block sizes are random, with $N_c \sim \mathrm{Bin}(N, s_c)$.
:::

:::{prf:definition} Soft (canonical) SBM (S-SBM)
:label: def-sbm-soft

Fix the labels $\boldsymbol\sigma = (\sigma_1,\dots,\sigma_N)$ and the matrix $B$. Then $G \sim \mathrm{S\text{-}SBM}(N,\boldsymbol\sigma,B)$ means $A_{ij} \stackrel{\mathrm{ind}}{\sim} \mathrm{Bernoulli}(B_{\sigma_i\sigma_j})$ for $i<j$. Equivalently, it is the HS-SBM conditioned on $\mathbf{x}$. The number of node pairs available to block pair $(c,c')$ is

$$
N_{cc'} = \begin{cases} N_c N_{c'}, & c \ne c',\\[2pt] \binom{N_c}{2}, & c = c'. \end{cases}
$$ (eq-sbm-pairs)

The extreme cases are $q = 1$, which is ER, and $q = N$, which is the generalised ER model $G(N,\{p_{ij}\})$ in which every pair has its own probability.
:::

:::{prf:definition} Microcanonical SBM
:label: def-sbm-micro

$\mathrm{SBM}(N,\boldsymbol\sigma,\{L_{cc'}\})$ is the **uniform** distribution over all labelled, coloured graphs with colours $\boldsymbol\sigma$ and exactly $L_{cc'}$ edges in each block pair. To sample one, place $L_{cc'}$ edges on node pairs chosen uniformly without replacement from the $N_{cc'}$ available, independently for each $c \le c'$.
:::

The graph space here is the space of graphs that are both **labelled** (node IDs) and **coloured** (communities). In the canonical and microcanonical versions, two graphs with the same $\boldsymbol\sigma$ and the same $\{L_{cc'}\}$ are equiprobable.

(sec-sbm-core)=
## Core ideas

### Not modularity

The notes open with a provocation: nobody knows what "community structure" is, and whatever it is, it is **not** high modularity $Q$.
- Sparse ER graphs have large modularity maxima purely from fluctuations ([](doi:10.1103/PhysRevE.70.025101), Guimerà, Sales-Pardo & Amaral 2004).
- So do random regular graphs ([](doi:10.1093/comnet/cnx046), McDiarmid & Skerman 2018).
- Random hyperbolic graphs, which have no planted blocks at all, have modularity converging to 1 in their realistic regime: power-law degrees, bounded mean degree, non-vanishing clustering ([](doi:10.1093/comnet/cnab051), Chellig, Fountoulakis & Skerman 2022).

The worked example below reproduces the ER effect: Louvain finds $Q \approx 0.45$ in a featureless $G(N,p)$ with $\langle k\rangle = 5$, more than the planted partition of a clearly structured SBM achieves. The SBM replaces "a partition that maximises a score" with "the hidden variables of a generative model". This is a statistical definition: communities are whatever the block structure of the ensemble says they are.

### Expected structure of the homogeneous SBM

In the HS-SBM each node falls in block $c$ with probability $s_c$, so the expected block size is $\bar N_c = s_c N$. Integrating the graphon over the right rectangles gives the expected edge counts and degrees (notes eqs. 14.2–14.4):

$$
\bar L_{cc'} \approx \begin{cases} B_{cc'}\,\bar N_c \bar N_{c'}, & c\neq c',\\ B_{cc}\binom{\bar N_c}{2}, & c=c', \end{cases}
\qquad
\bar k(c) = (N-1)\sum_{c'} s_{c'} B_{cc'},
\qquad
\langle k\rangle = (N-1)\sum_{c,c'} s_c s_{c'} B_{cc'} .
$$ (eq-sbm-expected-degree)

With $W$ fixed as $N$ grows, this is a true (dense) graphon and $\langle k \rangle = \Theta(N)$ ([Sparsity and small worlds](./01-sparsity-and-small-worlds.md)). The usual sparse scaling $B = C/N$ with $C$ fixed makes $\langle k\rangle = O(1)$. But the model then depends on $N$, so it is **not projective**: adding nodes changes the distribution of the existing subgraph ([Hidden variables and graphons](./07-hidden-variables-and-graphons.md)). The notes' alternative is to expand the hidden-variable space, $x \sim \mathcal{U}(0,N)$, and grow $W$ projectively. That is exactly how SRGGs and RHGs get sparsity and projectivity at once.

The degree of a node in block $c$ is a sum of independent binomials. In the sparse limit it is $\mathrm{Poisson}(\bar k(c))$, so the degree distribution of the whole graph is a **mixture of $q$ Poissons**: homogeneous, with no heavy tail. Real networks are heterogeneous ([Binning and power laws](./03-binning-and-power-laws.md)), and fitting a homogeneous SBM to them puts hubs into their own blocks. That is the motivation for degree correction.

### Degree correction = CM + SBM

Krioukov's table (notes §14.3) makes the construction mechanical. Each model is the maximum-entropy ensemble for its sufficient statistics, so combining constraints just adds the Lagrange terms.

| | CM / SCM / HSCM | SBM | DC-SBM = CM + SBM |
|---|---|---|---|
| Sufficient statistics | $\{k_i(G)\}$ | $\{L_{cc'}(G)\}$ | $\{k_i(G)\}$ and $\{L_{cc'}(G)\}$ |
| Canonical $P(G)$ | $Z^{-1}e^{-\sum_i \lambda_i k_i}$ | $Z^{-1}e^{-\sum_{c\le c'}\lambda_{cc'}L_{cc'}}$ | $Z^{-1}e^{-\sum_i \lambda_i k_i - \sum_{c\le c'}\lambda_{cc'}L_{cc'}}$ |
| Canonical $p_{ij}$ | $\dfrac{1}{e^{\lambda_i+\lambda_j}+1}$ | $\dfrac{1}{e^{\lambda_{\sigma_i\sigma_j}}+1}$ | $\dfrac{1}{e^{\lambda_i+\lambda_j+\lambda_{\sigma_i\sigma_j}}+1}$ |
| Hypercanonical $p$ (sparse) | $\approx \dfrac{\kappa\kappa'}{\langle\kappa\rangle N}$ | block $W(x,x')$ | $\approx \dfrac{\kappa\kappa'}{\langle\kappa\rangle b N}\,W(x,x')$ |

:::{prf:definition} Degree-corrected SBM, three versions
:label: def-sbm-dc

- **Hypersoft (HSCM-SBM$(N,\rho,W)$).** Draw $\kappa_i \stackrel{\mathrm{iid}}{\sim}\rho$ and $x_i \stackrel{\mathrm{iid}}{\sim}\mathcal{U}(0,1)$, then $A_{ij}\sim\mathrm{Bernoulli}(p_{ij})$ with $p_{ij}$ given by {eq}`eq-sbm-dc-hyper`.
- **Soft (SCM-SBM$(N,\boldsymbol\kappa,\boldsymbol\sigma,\{L_{cc'}\})$).** Edges are independent with Fermi–Dirac probabilities $p_{ij} = 1/(e^{\lambda_i+\lambda_j+\lambda_{\sigma_i\sigma_j}}+1)$. The multipliers solve
  - the degree constraints, $\sum_j p_{ij} = \kappa_i$ for $i = 1,\dots,N$;
  - the block constraints, $\sum_{i<j} p_{ij}\,\mathbf{1}\{\{\sigma_i,\sigma_j\} = \{c,c'\}\} = L_{cc'}$ for $c\le c'$.
- **Microcanonical (CM-SBM).** The uniform distribution over coloured graphs with exactly the degree sequence $\boldsymbol\kappa$ and exactly $\{L_{cc'}\}$. Sampling it is non-trivial; the notes defer to Peixoto ("Ask Tiago!"), whose `graph-tool` implements microcanonical SBM and DC-SBM sampling and inference ([](doi:10.1103/PhysRevE.95.012317)).
:::

$$
p_{ij} = \frac{\kappa_i\kappa_j}{\langle\kappa\rangle\, b\, N}\,B_{\sigma_i\sigma_j},
\qquad b = \int_0^1 W(x,y)\,dy .
$$ (eq-sbm-dc-hyper)

The SCM-SBM block constraints cannot be arbitrary. Summing the degree constraints over $i \in c$ gives a stub-conservation condition:

$$
\sum_{i:\sigma_i=c}\kappa_i = 2L_{cc} + \sum_{c'\neq c} L_{cc'}\qquad \text{for every } c .
$$ (eq-sbm-stub-conservation)

This is what the notes mean by "self-consistent" expected block edge counts. *My comment:* the same $q$ relations show up as a **gauge freedom** of the multipliers. Shifting $\lambda_i \to \lambda_i + a_{\sigma_i}$ and $\lambda_{cc'} \to \lambda_{cc'} - a_c - a_{c'}$ leaves every $p_{ij}$ unchanged. So $N + q(q+1)/2$ multipliers face $N + q(q+1)/2$ equations, of which $q$ are redundant.

:::{important} SBM versus SRGG: same machinery, different outcome
Degree correction works identically on top of SBMs and on top of latent-space models: add hidden variables $\kappa_i$ (or $\lambda_i$). The results differ because the $x$-part of the graphon differs. A smooth $W(x,x')$ that decays with distance produces clustering. A block $W$ in a fixed number of blocks does not (§[](#sec-sbm-limitations)).
:::

(sec-sbm-results)=
## Key results

:::{prf:theorem} The soft SBM is an exponential random graph with block edge counts as sufficient statistics
:label: thm-sbm-ergm

Define $\lambda_{cc'}$ by $B_{cc'} = 1/(e^{\lambda_{cc'}}+1)$, i.e. $\lambda_{cc'} = \ln\frac{1-B_{cc'}}{B_{cc'}}$. Then

$$
P_{\mathrm{S\text{-}SBM}}(G) = \prod_{c\le c'} B_{cc'}^{\,L_{cc'}(G)}\,(1-B_{cc'})^{\,N_{cc'}-L_{cc'}(G)}
= \frac{1}{Z}\exp\Big(-\sum_{c\le c'}\lambda_{cc'}L_{cc'}(G)\Big),
$$ (eq-sbm-expfam)

with $Z = \prod_{c\le c'}\big(1+e^{-\lambda_{cc'}}\big)^{N_{cc'}}$. The S-SBM is therefore the maximum-entropy (unbiased) canonical ensemble of coloured graphs with given expected $\{L_{cc'}\}$ (notes Thm 14.6), and its entropy is $H = \sum_{c\le c'} N_{cc'}\,h(B_{cc'})$, where $h(p) = -p\ln p-(1-p)\ln(1-p)$.
:::

:::{dropdown} Proof
1. Edges are independent, so $P(G) = \prod_{i<j} p_{ij}^{A_{ij}}(1-p_{ij})^{1-A_{ij}}$, with $p_{ij} = B_{\sigma_i\sigma_j}$.
2. Group the pairs by block pair. Pairs in $(c,c')$ contribute $L_{cc'}$ factors of $B_{cc'}$ and $N_{cc'}-L_{cc'}$ factors of $1-B_{cc'}$. This gives the first equality.
3. Write $B^{L}(1-B)^{N-L} = (1-B)^{N}\big(\tfrac{B}{1-B}\big)^{L} = (1-B)^N e^{-\lambda L}$, using $\tfrac{B}{1-B} = e^{-\lambda}$. Since $1-B = (1+e^{-\lambda})^{-1}$, the prefactor is $Z^{-1}$.
4. The form $Z^{-1}e^{-\sum \lambda_{cc'} L_{cc'}}$ is exactly the Gibbs distribution obtained by maximising $H[P]$ subject to $\langle L_{cc'}\rangle$ fixed ([Typicality and maximum entropy](./04-typicality-and-max-entropy.md)). So the S-SBM *is* that maximum-entropy ensemble, with $\langle L_{cc'}\rangle = N_{cc'}B_{cc'}$.
5. The entropy is that of $\sum_{c\le c'} N_{cc'}$ independent Bernoulli variables.
:::

A consequence for inference: for fixed $\boldsymbol\sigma$, the maximum-likelihood block matrix is the empirical density, $\hat B_{cc'} = L_{cc'}/N_{cc'}$, and the profile log-likelihood is $-\sum_{c\le c'} N_{cc'}\,h(\hat B_{cc'})$. **Maximum likelihood over partitions is minimum ensemble entropy over partitions.** This is the description-length view Peixoto develops ([](doi:10.1103/PhysRevE.85.056122)). The microcanonical entropy is $\ln\prod_{c\le c'}\binom{N_{cc'}}{L_{cc'}}$. By Stirling it is smaller than the canonical one by $\tfrac12\sum_{c \le c'}\ln\!\big(2\pi L_{cc'}(1-B_{cc'})\big) + o(1)$ per block pair, a subleading difference, so the two ensembles are equivalent to leading order.

:::{prf:theorem} DC-SBM self-consistency
:label: thm-sbm-dc-consistency

In the HSCM-SBM with $p_{ij}$ from {eq}`eq-sbm-dc-hyper`, the expected degree of a node with hidden variables $(\kappa, c)$ is

$$
\bar k(\kappa,c) = \frac{\kappa}{b}\sum_{c'} s_{c'} B_{cc'} .
$$ (eq-sbm-dc-degree)

So $\kappa$ is the expected degree for every block iff

$$
\sum_{c'=1}^{q} s_{c'}B_{cc'} = \int_0^1 W(x,y)\,dy = b \quad\text{for all } c,
$$ (eq-sbm-dc-consistency)

i.e. every row of the block graphon has the same mass. When this holds, the degree distribution is the $\rho$-mixed Poisson, exactly as in the HSCM (notes Def. 14.9).
:::

:::{dropdown} Derivation
1. $\bar k(\kappa,c) = N\int p(\kappa,x\in I_c;\kappa',x')\,\rho(\kappa')\,d\kappa'\,dx'$.
2. The probability factorises into a degree part and a block part, so the integral does too: $N\cdot\frac{\kappa}{\langle\kappa\rangle bN}\int\kappa'\rho(\kappa')\,d\kappa' \cdot \int W(x\in I_c, x')\,dx'$.
3. The first integral is $\langle\kappa\rangle$, and the second is $\sum_{c'} s_{c'}B_{cc'}$. This gives {eq}`eq-sbm-dc-degree`.
4. Setting $\bar k(\kappa,c) = \kappa$ for all $c$ gives {eq}`eq-sbm-dc-consistency`. Given $(\kappa, c)$, the degree is a sum of many independent rare Bernoullis, so it is $\mathrm{Poisson}(\kappa)$, and mixing over $\rho$ gives the mixed Poisson.
:::

**Classical limit of the soft DC-SBM** (notes Def. 14.11). When all $\lambda$'s are large (sparse graphs), the Fermi–Dirac probability becomes Boltzmann, $1/(e^{\lambda}+1)\approx e^{-\lambda}$, and factorises:

$$
p_{ij}^{\mathrm{CL}} = e^{-\lambda_i}e^{-\lambda_j}e^{-\lambda_{\sigma_i\sigma_j}} = B_{\sigma_i\sigma_j}\,\frac{\kappa_i\kappa_j}{\langle\kappa\rangle\, b\, N},
\qquad B_{cc'} = \frac{L_{cc'}}{N_{cc'}},\quad b = \sum_{c'} s_{c'}B_{cc'},\quad s_c = \frac{N_c}{N}.
$$ (eq-sbm-cl)

There are two ways to sample it: solve the full system for the $\lambda$'s and use Fermi–Dirac probabilities (exact), or use {eq}`eq-sbm-cl` directly.

*My comment.* With empirical densities $B_{cc'} = L_{cc'}/N_{cc'}$, the quantity $bN$ evaluated for block $c$ is $\big(2L_{cc}+\sum_{c'\ne c}L_{cc'}\big)/N_c$, the mean degree of block $c$. The constant-$b$ condition therefore forces **every block to have the same mean degree** $\langle\kappa\rangle = bN$, and then $p^{\mathrm{CL}}_{ij} = B_{\sigma_i\sigma_j}\kappa_i\kappa_j/\langle\kappa\rangle^2$. Karrer & Newman parameterise differently: $\mathbb{E}[A_{ij}] = \theta_i\theta_j\,\omega_{\sigma_i\sigma_j}$, with $\sum_{i:\sigma_i = c}\theta_i = 1$ and $\omega_{cc'}$ the expected number of edges between blocks ($c = c'$ counted twice). That puts all block-level degree differences into $\omega$, so it needs no equal-means condition ([](doi:10.1103/PhysRevE.83.016107)). Their profile likelihood $\sum_{c,c'}L_{cc'}\ln\frac{L_{cc'}}{K_cK_{c'}}$, with $K_c$ the total degree of block $c$, replaces the homogeneous SBM's $\sum L_{cc'}\ln\frac{L_{cc'}}{N_cN_{c'}}$ (Poisson approximation, sums over ordered block pairs). Swapping $N_c$ for $K_c$ is the whole difference, and it stops the fit from grouping nodes by degree.

### Detectability in sparse SBMs (beyond the notes)

The lecture notes stop at the model. The central inferential result of the last fifteen years is that **communities can be present in the ensemble yet undetectable from the graph**. Consider the symmetric sparse SBM: $q$ equal blocks, $B_{cc} = c_{\mathrm{in}}/N$, $B_{c\neq c'} = c_{\mathrm{out}}/N$, so $\langle k\rangle = (c_{\mathrm{in}}+(q-1)c_{\mathrm{out}})/q$.

:::{prf:theorem} Kesten–Stigum detectability threshold
:label: thm-sbm-ks

Efficient algorithms (belief propagation, non-backtracking spectral clustering) recover a partition positively correlated with $\boldsymbol\sigma$ whenever

$$
\big(c_{\mathrm{in}} - c_{\mathrm{out}}\big)^2 > q^2\,\langle k\rangle
\qquad\Longleftrightarrow\qquad
\frac{\lvert c_{\mathrm{in}}-c_{\mathrm{out}}\rvert}{q} > \sqrt{\langle k\rangle}.
$$ (eq-sbm-ks)

For $q=2$ this reads $(c_{\mathrm{in}}-c_{\mathrm{out}})^2 > 2(c_{\mathrm{in}}+c_{\mathrm{out}})$, and it is sharp: below it, *no* estimator beats chance. The cavity analysis is due to Decelle et al. ([](doi:10.1103/PhysRevE.84.066106)). Impossibility was proved by Mossel, Neeman & Sly ([](doi:10.1007/s00440-014-0576-6)) and achievability by Massoulié ([](doi:10.1145/2591796.2591857)) and Mossel–Neeman–Sly. For larger $q$ (Decelle et al. find $q\ge5$ in the assortative case), there is a range below the KS bound where detection is information-theoretically possible but believed computationally hard ([](doi:10.48550/arXiv.1703.10146)).
:::

:::{dropdown} Heuristic derivation: reconstruction on a tree
1. **Local tree-likeness.** For $\langle k\rangle = O(1)$, the neighbourhood of a node to depth $d \ll \log N$ is a Galton–Watson tree. Each node has $\mathrm{Poisson}(\langle k\rangle)$ children, the same law as the excess degree of a Poisson graph.
2. **Labels as a Markov chain down the tree.** A child has its parent's label with probability $c_{\mathrm{in}}/(q\langle k\rangle)$, and each other label with probability $c_{\mathrm{out}}/(q\langle k\rangle)$. Besides the trivial eigenvalue 1, this transition matrix has the $(q-1)$-fold eigenvalue $\mu = (c_{\mathrm{in}}-c_{\mathrm{out}})/(q\langle k\rangle)$.
3. **Signal against noise.** Infer the root's label from the label counts at depth $d$. The signal, the root-dependent bias of the counts, grows like $(\langle k\rangle\mu)^d$. The noise, the fluctuation of roughly $\langle k\rangle^d$ nearly independent labels, grows like $\langle k\rangle^{d/2}$.
4. The signal wins iff $\langle k\rangle\mu^2 > 1$, which is the Kesten–Stigum condition. Substituting $\mu$ gives {eq}`eq-sbm-ks`.
5. **Spectral version** ([](doi:10.1073/pnas.1312486110)). The non-backtracking matrix $B_{\mathrm{NB}}$ of the sparse SBM has leading eigenvalue $\approx\langle k^2\rangle/\langle k\rangle - 1 = \langle k \rangle$ for Poisson degrees. Its bulk lies in a disc of radius $\sqrt{\langle k\rangle}$, and its informative eigenvalue is $\langle k\rangle\mu = (c_{\mathrm{in}}-c_{\mathrm{out}})/q$. The informative eigenvalue escapes the bulk exactly when {eq}`eq-sbm-ks` holds. The adjacency matrix lacks this property in sparse graphs: eigenvalues from high-degree nodes swamp the informative one.
:::

At the other end, **exact recovery** of every label needs $\langle k\rangle = \Theta(\log N)$. For two equal blocks with $B_{\mathrm{in}} = a\ln N/N$ and $B_{\mathrm{out}} = b\ln N/N$, it is possible iff $(\sqrt a-\sqrt b)^2 > 2$ (Abbe, Bandeira & Hall, [](doi:10.1109/TIT.2015.2490670)). Here $a, b$ are local to this sentence. Sparse SBMs with bounded $\langle k\rangle$ always misclassify a positive fraction of nodes, if only the isolated ones.

(sec-sbm-example)=
## Worked example

All numbers below were computed with numpy/scipy/networkx (seed 1). The planted-partition samples have $N = 2000$, $q = 2$ equal blocks and $\langle k\rangle \approx 5$, so the KS bound needs $\lvert c_{\mathrm{in}}-c_{\mathrm{out}}\rvert > 2\sqrt5 \approx 4.47$. The signal-to-noise ratio $\mathrm{SNR} = (c_{\mathrm{in}}-c_{\mathrm{out}})^2/(2(c_{\mathrm{in}}+c_{\mathrm{out}}))$ is detectable iff $\mathrm{SNR} > 1$.

| Quantity | $c_{\mathrm{in}}=8,\ c_{\mathrm{out}}=2$ | $c_{\mathrm{in}}=6,\ c_{\mathrm{out}}=4$ |
|---|---|---|
| SNR | 1.80 (detectable) | 0.20 (undetectable) |
| $L$, $\langle k\rangle$ | 4984, 4.984 | 5002, 5.002 |
| within / between edges (expected) | 3926 / 1058 (3996 / 1000) | 2894 / 2108 (2997 / 2000) |
| MLE $N\hat B_{\mathrm{in}}$, $N\hat B_{\mathrm{out}}$ | 7.86, 2.12 | 5.79, 4.22 |
| Multipliers $\lambda_{\mathrm{in}}, \lambda_{\mathrm{out}} = \ln\frac{1-B}{B}$ | 5.517, 6.907 | 5.806, 6.213 |
| Modularity of the planted partition (expected $\frac{c_{\mathrm{in}}-c_{\mathrm{out}}}{2(c_{\mathrm{in}}+c_{\mathrm{out}})}$) | 0.288 (0.300) | 0.079 (0.100) |
| Louvain modularity | 0.448 (30 groups) | 0.447 (35 groups) |
| $B_{\mathrm{NB}}$: leading eigenvalue, bulk radius $\sqrt{\lambda_1}$ | 4.917, 2.217 | 4.960, 2.227 |
| $B_{\mathrm{NB}}$: second real eigenvalue (asymptotic $(c_{\mathrm{in}}-c_{\mathrm{out}})/2$) | 2.713 (3.0), outside the bulk | none outside the bulk (1.0 is inside) |
| Fraction correct, sign of $B_{\mathrm{NB}}$ eigenvector | 0.824 | |
| Fraction correct, sign of second adjacency eigenvector | 0.539 | 0.523 |

The non-backtracking spectrum was computed from the $2N\times2N$ Ihara–Bass matrix $\begin{pmatrix}0 & D-I\\ -I & A\end{pmatrix}$, whose eigenvalues are those of $B_{\mathrm{NB}}$ apart from $\pm1$.

What to read off:
- **Detectability is a spectral fact.** In the detectable case, one real eigenvalue (2.71) sits outside the bulk disc (radius 2.22), and its eigenvector labels 82% of nodes correctly. The informative eigenvalue is below its asymptotic value of 3 at this $N$. In the undetectable case, nothing escapes the bulk.
- **Adjacency spectral clustering is near chance** in both cases at $\langle k\rangle = 5$, as Krzakala et al. predict for sparse graphs.
- **Modularity does not measure community structure.** A plain ER graph $G(2000, p)$ with $\langle k\rangle = 4.96$ has Louvain modularity **0.447** (30 groups). That is the same as either SBM, and much more than the 0.288 of the true partition of the detectable SBM. Maximising $Q$ finds "communities" in noise.

**DC-SBM self-consistency.** Take two blocks with $s = (0.25, 0.75)$ and Pareto expected degrees ($\gamma = 2.5$, $\kappa_{\min} = 6$, capped at $\sqrt{N\langle\kappa\rangle}$ to keep $p_{ij}\le1$), with $N = 20{,}000$. Sample $p_{ij}$ from {eq}`eq-sbm-dc-hyper` with $b = s^\top B s$.
- **Consistent.** $B = \begin{pmatrix}0.9 & 0.1\\0.1 & 0.3\overline{6}\end{pmatrix}$ ($B_{22}$ solved from $0.25\cdot0.1+0.75B_{22} = 0.3$) has both row masses 0.300. The ratio of mean degree to mean $\kappa$ is 0.989 in block 1 and 0.999 in block 2; the 1% deficit comes from clipping hub pairs at $p = 1$.
- **Inconsistent.** $B = \begin{pmatrix}0.9 & 0.1\\0.1 & 0.9\end{pmatrix}$ has row masses (0.3, 0.7) and $b = 0.6$. The ratios are 0.507 and 1.155, against the predicted $0.3/0.6 = 0.500$ and $0.7/0.6 = 1.167$ from {eq}`eq-sbm-dc-degree`: $\kappa_i$ is no longer the expected degree.

**Canonical versus microcanonical entropy.** For one block pair with $N_{cc'} = 10^6$ and $L_{cc'} = 1000$: $H_{\mathrm{can}} = N_{cc'}h(B) = 7907.26$ nats and $H_{\mathrm{mic}} = \ln\binom{N_{cc'}}{L_{cc'}} = 7902.88$ nats. The difference, 4.372, matches $\tfrac12\ln(2\pi L(1-B)) = 4.372$.

(sec-sbm-limitations)=
## Assumptions and limitations

- **Edge independence given labels.** Clustering in an SBM comes only from block densities. With a fixed $q$ and sparse $B = C/N$, the expected clustering coefficient is $O(1/N)$, so a sparse SBM with finitely many blocks is **not** strongly clustered. Getting finite clustering needs $q = \Theta(N)$ blocks of bounded size with $B_{cc} = O(1)$. That is a different, highly parameterised model.
- **Not projective in the standard sparse scaling.** $B = C/N$ depends on $N$. Like ER with $p = \langle k\rangle/N$ and the HSCM with $\gamma \neq 3$, the standard sparse SBM has no growing formulation that leaves the existing graph unchanged ([Hidden variables and graphons](./07-hidden-variables-and-graphons.md)).
- **Homogeneous degrees** unless degree-corrected. The Krioukov-style DC-SBM also needs the constant-$b$ condition {eq}`eq-sbm-dc-consistency`. The Karrer–Newman parameterisation avoids it.
- **The number of blocks is a model-selection problem.** Likelihood always increases with $q$. Principled choices use description length or Bayesian nonparametrics, with hierarchical priors to avoid an underfitting limit of $q_{\max} \sim \sqrt N$ ([](doi:10.1103/PhysRevX.4.011047), Peixoto 2014; [](doi:10.1103/PhysRevE.95.012317)).
- **Hard partitions only.** Each node has one block. Overlapping or mixed-membership variants exist, and the notes' own suggestion is a fuzzy graphon somewhere between SBM and SRGG.
- **Detectability results are for the symmetric sparse case.** Thresholds for general $B$, with unequal sizes or degree correction, involve the eigenvalues of the matrix $\big(s_{c'}C_{cc'}\big)$, and the computational gap is a conjecture, not a theorem, for $q\ge 5$ ([](doi:10.48550/arXiv.1703.10146)).
- **Source caveats.**
  - In the transcribed notes, eq. 14.2 begins with a spurious "$\bar m_{cc'} = \bar n_c\bar n_{c'}$". The correct statement is the integral, with the approximations given above.
  - The $q = 3$ example matrix is garbled in the transcription; the intended example is $B_{cc} = p > p' = B_{c\ne c'}$.
  - Def. 14.8 writes $x_i \sim \rho$ where it means $\kappa_i \sim \rho$.
  - The sparse-growth remark writes $\rho = \mathcal{U}(0,n)$ for the distribution of $x$.
  - The hypercanonical CM entry $\frac{kk'}{kn}$ should read $\frac{\kappa\kappa'}{\langle\kappa\rangle N}$.

## Connections

- **NETS 5116.** The planted partition is the Girvan–Newman benchmark, and the LFR benchmark is essentially a DC-SBM with power-law degrees and community sizes ([](doi:10.1103/PhysRevE.78.046110)). Modularity optimisation and its failure modes are in [Barabási ch. 9](../nets-5116/barabasi/09-community-structure.md). Assortative mixing by block is the categorical case of the assortativity coefficient ([Newman ch. 7 notes](../nets-5116/newman/07-measures-and-metrics.md)).
- **NETS 6116.**
  - The S-SBM is the maximum-entropy ensemble for $\{L_{cc'}\}$, as the SCM is for $\mathbf{k}$ ([Typicality and maximum entropy](./04-typicality-and-max-entropy.md), [Configuration models](./05-configuration-models.md)).
  - The block graphon is a step-function graphon. The Szemerédi-regularity view, that any graphon is approximated by block graphons, makes SBMs universal approximators of dense graph limits ([Hidden variables and graphons](./07-hidden-variables-and-graphons.md)).
  - The $dK$-series' $2K$ constraint (joint degree matrix) is a DC-SBM-like constraint with degree classes as blocks ([dk-series](./06-dk-series.md)).
  - SBM versus latent-space models is the discrete-versus-geometric dichotomy of [Latent-space models](./08-latent-space-models.md).
- **PHYS 7335.**
  - Degree classes in heterogeneous mean field are blocks: $C_{kk'}$ is a block matrix over degree classes, and the HMF threshold is set by its leading eigenvalue ([Heterogeneous mean field](../phys-7335/05-heterogeneous-mean-field.md), [Degree-block formalism](../phys-7335/01-degree-block-formalism.md)).
  - The non-backtracking matrix that sets the SIR threshold, $T_c = 1/\Lambda_{\max}(B_{\mathrm{NB}})$, is also the right operator for detecting communities ([Quenched mean field](../phys-7335/06-quenched-mean-field.md)).
  - Metapopulation and age-structured mixing matrices are SBM block matrices.
- **NETS 7332.**
  - Loopy belief propagation for collective classification ([Label propagation](../nets-7332/basics/04-label-propagation.md)) is the algorithm Decelle et al. analyse; it reaches the KS bound and is conjectured to be optimal among efficient algorithms.
  - SBM samples are the standard synthetic benchmark for GNN homophily and heterophily studies ([Node characteristics](../nets-7332/readings/02-node-characteristics.md)).
  - The KS bound limits what any GNN can extract from structure alone in sparse graphs.

## Self-test

:::{dropdown} Q1. Write the canonical SBM as an exponential family. What are the sufficient statistics and the multipliers?
$P(G) = Z^{-1}\exp(-\sum_{c\le c'}\lambda_{cc'}L_{cc'}(G))$. The sufficient statistics are the block edge counts $L_{cc'}$, and the multipliers are $\lambda_{cc'} = \ln\frac{1-B_{cc'}}{B_{cc'}}$, with $Z = \prod_{c\le c'}(1+e^{-\lambda_{cc'}})^{N_{cc'}}$.
:::

:::{dropdown} Q2. Name the three SBM ensembles and say what is random in each.
- **Hypersoft:** labels (so block sizes are binomial) and edges.
- **Soft/canonical:** labels fixed; edges independent, so block edge counts fluctuate.
- **Microcanonical:** labels and every $L_{cc'}$ fixed; the graph is uniform over the coloured graphs consistent with them.
:::

:::{dropdown} Q3. Why does a DC-SBM need $\sum_{c'} s_{c'}B_{cc'}$ to be independent of $c$?
The expected degree of a $(\kappa,c)$ node is $\frac{\kappa}{b}\sum_{c'}s_{c'}B_{cc'}$. For $\kappa$ to be the expected degree in every block, each row mass must equal $b$. Otherwise blocks with heavier rows get inflated degrees.
:::

:::{dropdown} Q4. State the KS threshold for two equal communities and explain it in one sentence.
$(c_{\mathrm{in}}-c_{\mathrm{out}})^2 > 2(c_{\mathrm{in}}+c_{\mathrm{out}})$. Along a locally tree-like neighbourhood, the label signal grows like $(\langle k\rangle\mu)^d$ while the noise grows like $\langle k\rangle^{d/2}$, so reconstruction needs $\langle k\rangle\mu^2>1$. Spectrally, the informative non-backtracking eigenvalue must leave the bulk disc of radius $\sqrt{\langle k\rangle}$.
:::

:::{dropdown} Q5. Give two reasons why "high modularity" is not evidence of communities.
- Sparse ER and random regular graphs have modularity maxima bounded away from zero from fluctuations alone ($Q\approx0.45$ for $G(2000,p)$ with $\langle k\rangle = 5$ in the worked example).
- Random hyperbolic graphs, which are geometric with no planted blocks, have modularity $\to 1$.

Modularity also has a resolution limit: it cannot resolve communities smaller than about $\sqrt{L}$ edges ([](doi:10.1073/pnas.0605965104), Fortunato & Barthélemy 2007).
:::

:::{dropdown} Q6. (Notes' final problem.) Sketch a DC-SBM that is ultrasparse, small-world, strongly clustered, heterogeneous and projective.
*My answer, not from the notes.* Projectivity plus ultrasparsity needs an $N$-independent connection probability on an **expanding** hidden-variable space. So the block index has to live in an infinite space:
- Place nodes by a rate-1 Poisson process on $[0,N)$, and let block $c$ be the unit cell $[c-1,c)$, giving $q\approx N$ blocks of bounded size.
- Choose an $N$-independent block matrix $B_{cc'} = f(\lvert c-c'\rvert)$ with $f(d)\sim d^{-\beta}$ and $1<\beta<2$:
  - integrable, so the graph is ultrasparse and projective;
  - long-ranged enough to be small-world;
  - $B_{cc} = O(1)$, so it is clustered.
- Multiply by $\kappa_i\kappa_j$ with Pareto $\kappa$ for heterogeneity.

The result is a discretised SRGG/RHG. The lesson is that once you ask an SBM for every property of real networks, it turns into a latent-space model.
:::

:::{dropdown} Q7. Why does Karrer–Newman degree correction stop the SBM from splitting hubs from leaves?
The homogeneous SBM's likelihood $\sum L_{cc'}\ln\frac{L_{cc'}}{N_cN_{c'}}$ rewards grouping nodes by degree, because degree is the strongest signal in heterogeneous data. Replacing $N_c$ by the total block degree $K_c$ accounts for degree, so only the residual mixing pattern is attributed to blocks.
:::

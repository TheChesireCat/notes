---
title: Data Binning and Power-Law Degree Distributions
short_title: Binning and power laws
subject: NETS 6116 · Topic
description: How to bin network data correctly, what "the degree distribution is a power law" means rigorously (regular variation), and how the exponent γ is estimated through the extreme value index ξ.
tags: [data-binning, power-laws, regular-variation, extreme-value-theory, hill-estimator, scale-free, degree-distribution]
---

:::{tip} TL;DR
- **Binning depends on what is binned.** For a *function* such as $c(k)$ or $\bar k_{nn}(k)$, average the $y$-values in each bin. For a *distribution* such as $p_k$, use $Y_i = n_i/(N\Delta_i)$: count over (sample size × bin width). Use **log bins** (≈ 20, plotted at the geometric bin centre $\sqrt{b_i b_{i+1}}$) for heavy-tailed data. To average over many sampled graphs, pool the per-node records $(i, k_i, c_i, \ldots)$ *as one huge graph*. Never average per-graph curves.
- **"Power law" means regularly varying.** A distribution is a power law if its CCDF is $\bar F(k) = \ell(k)\,k^{-\alpha}$, with $\ell$ slowly varying ($\ell(tk)/\ell(k) \to 1$). The CCDF exponent is $\alpha = \gamma - 1$. A *pure* power law has constant $\ell$. This is an asymptotic ($k \to \infty$) property, so **no finite degree sequence is a power law**, in the same way that no finite graph is "sparse".
- **Extreme value theory.** Suitably rescaled, the maximum of $N$ i.i.d. samples converges to a GEV law of index $\xi$: **Weibull** for $\xi<0$ (bounded support), **Gumbel** for $\xi=0$, **Fréchet** for $\xi>0$. The Fréchet domain is *exactly* the set of power laws, and $\boxed{\xi = 1/\alpha = 1/(\gamma-1)}$. For a Pareto tail, $\mathbb{E}\,k_{\max} \approx \Gamma(1-\xi)\,k_{\min}N^{\xi}$.
- **Estimating γ.** The good estimators estimate $\xi$ from the $K$ largest degrees, and are consistent when $K\to\infty$ and $K/N\to 0$. These are **Hill** (the MLE for a Pareto tail; always $\hat\xi>0$), **moments** and **kernel**. The **double bootstrap** picks the optimal $K$. Least-squares fits on log–log histograms are biased.
- **On real data, $\hat\gamma$ is heuristic only**, like $\hat k$, $\hat d$ or $\hat c$. On Voitalov et al.'s 35 undirected KONECT networks, the three estimators classify 7 as not power-law, 11 as hardly power-law and 17 as power-law. Ten of the 17 have $\hat\gamma < 3$ by every estimator (divergent second moment).
:::

- **Source.**
  - Krioukov, *Network Science II* lecture notes, ch. 5 (Data binning) and ch. 6 (Power laws).
  - [](doi:10.1103/PhysRevResearch.1.033034) (Voitalov, van der Hoorn, van der Hofstad & Krioukov, *Phys. Rev. Research* 1, 033034, 2019): the definitions, the estimator pipeline and Tables I–III, which ch. 6 reproduces.
  - Primary statistics:
    - [](doi:10.1214/aos/1176343247) (Hill 1975);
    - [](doi:10.1214/aos/1176347397) (Dekkers, Einmahl & de Haan 1989, moments estimator);
    - [](doi:10.1214/aos/1074290333) (Groeneboom, Lopuhaä & de Wolf 2003, kernel estimators);
    - [](doi:10.1006/jmva.2000.1903) (Danielsson, de Haan, Peng & de Vries 2001, double bootstrap).
  - Background:
    - [](doi:10.1017/CBO9780511721434) (Bingham, Goldie & Teugels, *Regular Variation*, 1987);
    - [de Haan & Ferreira, *Extreme Value Theory: An Introduction*, Springer 2006](https://doi.org/10.1007/0-387-34471-3);
    - [](doi:10.2307/1968974) (Gnedenko 1943).
  - The physics-side view of fitting:
    - [](doi:10.1137/070710111) (Clauset, Shalizi & Newman, *SIAM Rev.* 51, 2009);
    - [](doi:10.1080/00107510500052444) (Newman, *Contemp. Phys.* 46, 2005);
    - the opposing verdict in [](doi:10.1038/s41467-019-08746-5) (Broido & Clauset, *Nat. Commun.* 10, 1017, 2019).
- **Builds on.**
  - [Sparsity and small-worldness](./01-sparsity-and-small-worlds.md), for the "properties of graph sequences, not graphs" theme.
  - [Barabási ch. 4](../nets-5116/barabasi/04-scale-free-networks.md) and [Newman ch. 10 notes](../nets-5116/newman/10-structure-of-real-world-networks.md), for the empirical picture.
- **Notation.** Shared symbols as in [](#notation). $N$ is the sample size: the number of degrees in the sequence $\mathbf k$ (Krioukov: $n$).
  - **Clash:** $\alpha = \gamma - 1$ is the **CCDF** exponent on this page, whereas Newman's $\alpha$ is the PDF exponent $\gamma$.
  - Bins are $B_i = [b_i, b_{i+1})$, with width $\Delta_i$ (Krioukov: $L_i$, which clashes with the edge count), count $n_i$ (Krioukov: $S_i$) and number of bins $n_b$ (Krioukov: $\mathcal B$).
  - $\ell(\cdot)$ is a slowly varying function, $\bar F = 1 - F$ is the CCDF, and $k_{(1)} \ge k_{(2)} \ge \dots \ge k_{(N)}$ are the order statistics.
  - $K$ is the number of top order statistics an estimator uses (Krioukov: $\kappa$; renamed to avoid the hidden variable $\kappa_i$).
  - $a$, $s$, $\xi$ are the GEV location, scale and extreme value index.

(sec-pl-setup)=
## Setup and definitions

### Binning

Krioukov's ch. 5 separates two kinds of data that are binned in completely different ways:

1. **Functions** $f(x)$, for example $c(k)$ or $\bar k_{nn}(k)$. The data are pairs $(x_j, y_j = f(x_j))$, $j = 1,\dots,N$.
2. **Distributions** $P(x)$, for example $p_k$. The data are $x_j \sim P$, assumed **i.i.d.**

In both cases the bins $B_i = [b_i, b_{i+1})$, $i = 1,\dots,n_b$, cover the data range, with $b_1 = \min_j x_j$ and $b_{n_b+1} = \max_j x_j$ (the last bin is closed). Write $\Delta_i = b_{i+1}-b_i$ for the bin width and $n_i = \lvert\{j : x_j \in B_i\}\rvert$ for the bin count. What gets plotted is $(X_i, Y_i)$.

:::{prf:definition} Linear and logarithmic bins
:label: def-pl-bins

- **Linear:** $\Delta_i = (b_{n_b+1}-b_1)/n_b$ for all $i$. Plot at $X_i = b_i$ (most common) or at the midpoint.
- **Logarithmic** (needs $b_1 > 0$): bin $q = \ln x$ linearly, $q_i = q_1 + (i-1)\,(q_{n_b+1}-q_1)/n_b$, and set $b_i = e^{q_i}$. Bin widths then grow geometrically, $b_{i+1}/b_i = \text{const}$. Plot at the **geometric centre** $X_i = e^{(q_i+q_{i+1})/2} = \sqrt{b_i b_{i+1}}$, which is the right choice for power-law data ({prf:ref}`prop-pl-geo-centre`).
:::

:::{prf:definition} Binned values
:label: def-pl-binned-values

- For a **function**, $Y_i$ is the mean of the $y_j$ whose $x_j$ fall in $B_i$, $Y_i = \frac{1}{n_i}\sum_{j:\,x_j\in B_i} y_j$.
- For a **distribution**, $Y_i$ estimates the density:

$$
Y_i = \frac{n_i}{N\,\Delta_i}.
$$ (eq-pl-density-bin)

This is because $\mathbb E\, n_i = N\Pr(x\in B_i) \approx N P(X_i)\Delta_i$. It is normalised: $\sum_i Y_i \Delta_i = \tfrac1N \sum_i n_i = 1$.
:::

In code, the first is `scipy.stats.binned_statistic(x, y, statistic='mean', bins=edges)`. The second is `numpy.histogram(x, bins=edges, density=True)`; note that it divides by the bin width, not just by $N$.

### Power laws

:::{prf:definition} Slowly and regularly varying functions
:label: def-pl-regular-variation

A positive function $\ell$ is **slowly varying** if $\lim_{k\to\infty}\ell(tk)/\ell(k) = 1$ for every $t>0$.

- Slowly varying: constants, any $\ell$ with a positive finite limit, and $\ln^{c} k$ for any $c\in\mathbb R$.
- Not slowly varying: $k^{c}$ with $c\neq 0$, and $\sin k$.

A function $f$ is **regularly varying** with index $-\alpha$ ($\alpha>0$) if $f(k) = \ell(k)\,k^{-\alpha}$ with $\ell$ slowly varying.
:::

:::{prf:definition} Power-law distribution
:label: def-pl-power-law

A probability distribution is a **power law** (regularly varying) if its CCDF is regularly varying:

$$
\bar F(k) = \Pr(X > k) = \ell(k)\,k^{-\alpha}, \qquad \alpha = \gamma - 1 > 0 .
$$ (eq-pl-ccdf)

It is a **pure** ("clean") power law if $\ell$ is constant. The Pareto distribution is the canonical example:

$$
P(k) = (\gamma-1)\,k_{\min}^{\gamma-1}\,k^{-\gamma},\quad k\ge k_{\min}>0, \qquad \bar F(k) = (k/k_{\min})^{-\alpha}.
$$ (eq-pl-pareto)
:::

The definition is on the CCDF, not the PDF, on purpose. A regularly varying PDF always gives a regularly varying CCDF ({prf:ref}`thm-pl-karamata`), but not the other way round. So the CCDF definition is the more general one, and the one the estimators actually need.

:::{prf:definition} Extreme value distribution
:label: def-pl-gev

Let $k_{\max} = \max_{i\le N} k_i$ for i.i.d. $k_i\sim P$. If there are constants $c_N>0$ and $d_N$ such that $(k_{\max}-d_N)/c_N$ converges in distribution to a non-degenerate law, that limit is the **generalised extreme value distribution (GEVD)**, with CDF

$$
\mathcal F(x) = \exp\!\Big[-\big(1+\xi\,\tfrac{x-a}{s}\big)^{-1/\xi}\Big] \quad (\xi\neq 0), \qquad \mathcal F(x) = \exp\!\big[-e^{-(x-a)/s}\big] \quad (\xi = 0).
$$ (eq-pl-gev)

Here $a\in\mathbb R$ is the location, $s>0$ the scale, and $\xi\in\mathbb R$ the **extreme value index**. The GEVD is called **Weibull** if $\xi<0$, **Gumbel** if $\xi=0$ and **Fréchet** if $\xi>0$.
:::

:::{prf:definition} Estimator, consistency
:label: def-pl-estimator

An **estimator** $X$ maps a degree sequence $\mathbf k$ to $\hat\xi = X(\mathbf k)$; it may be randomised. It is **consistent** if $\hat\xi\to\xi$ (in probability) as $N\to\infty$, under stated assumptions on how $\mathbf k$ is generated. The usual assumption is i.i.d. samples from $P$. A random $\mathbf k$ (e.g. from a random graph) makes $\hat\xi$ random even if $X$ is deterministic.
:::

(sec-pl-core)=
## Core ideas

### Why log bins, and why only ~20 of them

Heavy-tailed data span several decades. With linear bins, almost all the data fall in the first bin and the tail is a scatter of bins with zero or one count (see the [worked example](#sec-pl-example): 99,984 of $10^5$ samples land in bin 1). Log bins give every decade the same number of bins. In a log bin the count is $n_i \approx N P(X_i)\Delta_i \propto X_i^{1-\gamma}$, which decays more slowly than the density itself, so the tail stays populated longer. Krioukov's rule of thumb is to choose $n_b$ so that every bin is statistically significant: real power-law networks usually need $n_b\in[15,25]$, and $n_b=20$ is the default.

Linear (or no) binning is right for **homogeneous** data, i.e. bell-shaped, binomial or Poisson. Log binning is right for **heterogeneous** data.

### Averaging over an ensemble: pool the records, not the curves

When the task is "average $c(k)$ over $M$ graphs sampled from an ensemble", Krioukov is emphatic:

- **Right:** concatenate per-node records $(i, k_i, c_i, \bar k_{nn,i})$ from *all* graphs, as if they formed one huge graph, then bin once.
- **Wrong:** compute each graph's curve $(k, N_k, c(k), \bar k_{nn}(k))$ and average the curves.

The wrong version gives every graph's estimate of a degree class equal weight, however few nodes that class has in that graph. It therefore overweights rare classes, which are exactly the noisy high-degree ones. The pooled version weights each node equally, which is what the ensemble average $\mathbb E[c_i\mid k_i=k]$ means. The worked example has a two-graph case where the two answers differ by a factor of 2.

### Power laws are asymptotic, so they cannot be read off one network

Krioukov's central observation is that **no empirical $p_k$ of a real network is a power law**. Definition {prf:ref}`def-pl-power-law` is about $k\to\infty$, while a finite network has a finite $k_{\max}$. This is the same situation as sparsity and small-worldness ([page 01](./01-sparsity-and-small-worlds.md)) and strong clustering ([page 02](./02-clustering-and-assortativity.md)), which are properties of *graph sequences*.

There is one important difference. For those properties, the finite-graph statistic ($\langle k\rangle$, $\langle d\rangle$, $\langle C\rangle$) is well defined and easy to compute. A finite degree sequence has **no** $\gamma$ to compute: it has to be *estimated*, under a model of how the sequence was generated. All the good estimators do this through $\xi$.

### Extreme value theory is the right lens

Regular variation is about the tail, and EVT is the theory of tails. **The Fisher–Tippett–Gnedenko theorem** ([](doi:10.2307/1968974)) says that whatever $P$ is, the rescaled maximum can only converge to a degenerate law or to a GEVD. This sorts every "reasonable" distribution into one of three **maximum domains of attraction (MDA)**:

| $\xi$ | MDA | Distributions $P$ in it |
|---|---|---|
| $\xi<0$ | Weibull | bounded support (finite right endpoint) |
| $\xi=0$ | Gumbel | the rest, including exponential, Gaussian and lognormal tails |
| $\xi>0$ | Fréchet | **exactly** the regularly varying distributions |

So "is $p_k$ a power law?" becomes "is $\xi>0$?", and "what is $\gamma$?" becomes "what is $1+1/\xi$?". Moment properties follow directly. For a regularly varying law with CCDF index $\alpha$, $\mathbb E[X^m]<\infty$ iff $m<\alpha$ (and $\mathbb E[X^m] = \infty$ for $m>\alpha$). In particular,

$$
\langle k^2\rangle = \infty \iff \alpha<2 \iff \gamma<3 \iff \xi>\tfrac12 .
$$ (eq-pl-dsm)

This is the condition that kills the epidemic threshold ([PHYS 7335 HMF](../phys-7335/05-heterogeneous-mean-field.md)) and the percolation threshold ([Barabási ch. 8](../nets-5116/barabasi/08-network-robustness.md)). Voitalov et al. call it the **divergent-second-moment (DSM)** class.

### Estimators work on the top $K$ order statistics

The good estimators are $X(\mathbf k, K)$: they look only at the $K$ largest degrees and ignore the rest. Consistency needs $K\to\infty$ (enough tail data, so the variance goes to 0) and $K/N\to0$ (only genuinely extreme data, so the bias from $\ell$ goes to 0). The consistency proofs hold for *any* such $K$ sequence. Which $K$ minimises the error for a given sample is a separate question. Only a few estimators have a proven-optimal, data-driven choice $K^* = Y(\mathbf k)$:

| Estimator $X$ | Formula / idea | Range of $\hat\xi$ |
|---|---|---|
| **Hill** ([](doi:10.1214/aos/1176343247)) | $\hat\xi_{\mathrm H} = \frac1K\sum_{i=1}^K \ln\frac{k_{(i)}}{k_{(K+1)}}$, the MLE for a Pareto tail | always $>0$ |
| **Moments** ([](doi:10.1214/aos/1176347397)) | $\hat\xi_{\mathrm M} = M_1 + 1 - \tfrac12\big(1 - M_1^2/M_2\big)^{-1}$, with $M_r = \frac1K\sum_{i\le K}\ln^r\frac{k_{(i)}}{k_{(K+1)}}$ | any real |
| **Kernel** ([](doi:10.1214/aos/1074290333)) | kernel-weighted versions of Hill-type log-spacing statistics, smoothing over $K$ | any real (the $\infty$ entries in Voitalov's tables come from it and the moments estimator) |

The auxiliary algorithm $Y$ is the **double bootstrap** ([](doi:10.1006/jmva.2000.1903)). It estimates the asymptotic mean-squared error as a function of $K$ from resamples, and returns a $K^*$ that is consistent ($K^*\to\infty$, $K^*/N\to0$) and AMSE-optimal. $Y$ is random, so $X(\mathbf k, Y(\mathbf k))$ is random even for a fixed $\mathbf k$.

The "range" column matters. Hill can only ever report a power law, so a non-power-law verdict ($\hat\xi\le 0$, $\hat\gamma=\infty$) has to come from the moments or kernel estimators. In Voitalov's Table I every $\infty$ is in those two columns.

### Why not fit a line to the log–log histogram?

*Own commentary, following [](doi:10.1137/070710111):* least-squares regression of $\ln Y_i$ on $\ln X_i$ is biased. Its errors are neither Gaussian nor homoscedastic, sparse tail bins dominate, and the result depends on $n_b$ and on where the fit starts. The worked example below gets a slope of $-2.40$ from all occupied log bins and $-2.54$ when bins with fewer than 10 counts are dropped, against a true $-2.5$. Clauset–Shalizi–Newman propose instead:

1. the continuous MLE $\hat\gamma = 1 + n_{\mathrm{tail}}\big[\sum_{k_i\ge k_{\min}}\ln(k_i/k_{\min})\big]^{-1}$, which is the Hill estimator with a fixed threshold;
2. $k_{\min}$ chosen by minimising the Kolmogorov–Smirnov distance;
3. a bootstrap goodness-of-fit $p$-value, and likelihood-ratio tests against alternatives (lognormal, stretched exponential, power law with cutoff).

Their test is for a **pure** power law above $k_{\min}$. Broido & Clauset ([](doi:10.1038/s41467-019-08746-5)) applied it to ~1000 networks and concluded that "scale-free networks are rare". Voitalov et al. test **regular variation** (any slowly varying $\ell$), with estimators proven consistent for that class, and conclude the opposite: "scale-free networks well done". Much of the disagreement is about which definition of "power law" is being tested.

(sec-pl-results)=
## Key results

:::{prf:proposition} Geometric bin centre is exact for $\gamma = 2$
:label: prop-pl-geo-centre

For a pure power-law density $P(x) = Cx^{-\gamma}$ and a log bin $[b, \beta_b b)$ with width ratio $\beta_b>1$, the bin-averaged density $Y = \frac{1}{(\beta_b-1)b}\int_b^{\beta_b b}P(x)\,dx$ equals $P(x^*)$ at

$$
x^* = b\left[\frac{(\gamma-1)(\beta_b-1)}{1-\beta_b^{\,1-\gamma}}\right]^{1/\gamma}.
$$ (eq-pl-xstar)

For $\gamma=2$ this is exactly the geometric centre $b\sqrt{\beta_b}$. For $\gamma\in[2,3]$ and $\beta_b\le 2$, it lies within 2% of the geometric centre, while the arithmetic centre is off by 6–8%.
:::

:::{dropdown} Derivation
$\int_b^{\beta_b b}Cx^{-\gamma}dx = \frac{C b^{1-\gamma}}{\gamma-1}\big(1-\beta_b^{1-\gamma}\big)$. Dividing by the width $(\beta_b-1)b$ and setting the result equal to $C(x^*)^{-\gamma}$ gives {eq}`eq-pl-xstar`. At $\gamma=2$ the bracket is $(\beta_b-1)/(1-\beta_b^{-1}) = \beta_b$, so $x^* = b\beta_b^{1/2}$. The percentages are the computed values in the [worked example](#sec-pl-example).
:::

:::{prf:theorem} Karamata (PDF regularly varying ⇒ CCDF regularly varying)
:label: thm-pl-karamata

If the density is $P(x) = \ell(x)\,x^{-\gamma}$ with $\gamma>1$ and $\ell$ slowly varying, then

$$
\bar F(k) = \int_k^\infty P(x)\,dx \;\sim\; \frac{\ell(k)\,k^{1-\gamma}}{\gamma-1}, \qquad k\to\infty,
$$ (eq-pl-karamata)

so $\bar F$ is regularly varying with index $-\alpha = -(\gamma-1)$. The converse fails.
:::

:::{dropdown} Proof sketch and counterexample
Substitute $x = kt$: $\bar F(k) = k^{1-\gamma}\ell(k)\int_1^\infty \frac{\ell(kt)}{\ell(k)}\,t^{-\gamma}\,dt$. The ratio tends to 1 pointwise by slow variation. **Potter's bounds** ([](doi:10.1017/CBO9780511721434), Thm 1.5.6) give $\ell(kt)/\ell(k)\le A\,t^{\delta}$ for large $k$, $t\ge1$ and any $\delta>0$. Taking $\delta<\gamma-1$ supplies an integrable dominating function, so dominated convergence gives $\int_1^\infty t^{-\gamma}dt = 1/(\gamma-1)$.

**Converse fails.** Take $P(x)\propto \sin^2 x/x^3$ on $x\ge x_0$ (Krioukov's example). Writing $\sin^2 t = (1-\cos 2t)/2$ and integrating by parts, the oscillating part contributes $O(x^{-3})$, so $\bar F(x) \propto \frac{1}{4x^2}+O(x^{-3})$. That is regularly varying with $\alpha = 2$. The PDF vanishes at every $x = n\pi$, so $P(tx)/P(x)$ has no limit and $P$ is *not* regularly varying.
:::

:::{prf:theorem} Fréchet domain and the exponent–index relation
:label: thm-pl-frechet

$P$ is in the Fréchet MDA iff it is regularly varying (Gnedenko 1943). If $\bar F(k) = \ell(k)k^{-\alpha}$, then

$$
\xi = \frac1\alpha = \frac{1}{\gamma-1}.
$$ (eq-pl-xi-gamma)

With $c_N = F^{-1}(1-1/N)$ and $d_N = 0$ (equivalently $a = 1$, $s = \xi$ in {eq}`eq-pl-gev`), the limit law is

$$
\Pr\!\left(\frac{k_{\max}}{c_N}\le x\right)\to e^{-x^{-1/\xi}},\quad x>0,\qquad \mathbb E\!\left[\frac{k_{\max}}{c_N}\right]\to\Gamma(1-\xi)\ \ (\xi<1,\ \text{i.e. } \gamma>2).
$$ (eq-pl-frechet)
:::

:::{prf:corollary} Natural cutoff of a Pareto tail
:label: cor-pl-kmax

For Pareto {eq}`eq-pl-pareto`, $c_N = k_{\min}N^{\xi}$, so

$$
k_{\max} \approx \Gamma(1-\xi)\,k_{\min}\,N^{1/(\gamma-1)} .
$$ (eq-pl-kmax)
:::

:::{dropdown} Derivation for the Pareto case
$\bar F(c_N) = 1/N$ gives $(c_N/k_{\min})^{-\alpha} = 1/N$, i.e. $c_N = k_{\min}N^{1/\alpha} = k_{\min}N^{\xi}$. By independence,

$$\Pr(k_{\max}\le c_N x) = \big(1-\bar F(c_N x)\big)^N = \big(1 - x^{-\alpha}/N\big)^N \to e^{-x^{-\alpha}},$$

which is the Fréchet CDF with $1/\xi = \alpha$. Its mean is $\int_0^\infty \Pr(Z>z)\,dz = \int_0^\infty (1-e^{-z^{-\alpha}})\,dz$. Substituting $u = z^{-\alpha}$ and integrating by parts gives $\Gamma(1-1/\alpha) = \Gamma(1-\xi)$, which is finite iff $\alpha>1$ ($\gamma>2$).

For general regularly varying $\bar F$ the same computation goes through, because $\bar F(c_Nx)/\bar F(c_N)\to x^{-\alpha}$.

**Comparison with Barabási.** [Barabási eq. 4.18](../nets-5116/barabasi/04-scale-free-networks.md) sets $\int_{k_{\max}}^\infty p_k\,dk = 1/N$. That gives the *scale* $c_N = k_{\min}N^{1/(\gamma-1)}$, not the mean. The two differ by the $O(1)$ factor $\Gamma(1-\xi)$, which is 2.68 at $\gamma = 2.5$. The scaling with $N$ is the same.
:::

:::{prf:theorem} Hill is the tail MLE, and its rate
:label: thm-pl-hill

If $k_i$ above a threshold $u$ are exactly Pareto, then $\ln(k_i/u)$ is exponential with mean $\xi$. The MLE of $\xi$ from the exceedances is the mean of the log-excesses. Taking the random threshold $u = k_{(K+1)}$ gives the **Hill estimator**

$$
\hat\xi_{\mathrm H}(K) = \frac1K\sum_{i=1}^{K}\ln\frac{k_{(i)}}{k_{(K+1)}}, \qquad \hat\gamma = 1+\frac{1}{\hat\xi_{\mathrm H}} .
$$ (eq-pl-hill)

For regularly varying $\bar F$ it is consistent whenever $K\to\infty$ and $K/N\to0$. Under a second-order condition on $\ell$ with $\sqrt K\cdot\text{bias}\to 0$, it satisfies $\sqrt K\,(\hat\xi_{\mathrm H}-\xi)\Rightarrow\mathcal N(0,\xi^2)$ ([de Haan & Ferreira 2006](https://doi.org/10.1007/0-387-34471-3), ch. 3).
:::

:::{dropdown} Why the bias–variance trade-off in $K$ is unavoidable
The variance is $\approx\xi^2/K$, so it wants large $K$. But $\ell$ is only asymptotically constant: the lower order statistics come from the region where $\ell(k)$ still varies, and they bias $\hat\xi$. So bias wants small $K/N$. The AMSE-optimal $K^*$ depends on the unknown second-order behaviour of $\ell$. That is why it has to be estimated, which the double bootstrap does. There is no universal "use the top 10%".
:::

:::{prf:proposition} Status of $\hat\gamma$ on real data (Krioukov ch. 6.4)
:label: prop-pl-real-data

Running a consistent pipeline $(X,Y)$ on a real $\mathbf k$ always produces *some* $\hat\gamma$. That number supports only non-rigorous, intuitive conclusions, because:

1. it is unknown whether a real $\mathbf k$ satisfies the assumptions (e.g. i.i.d. samples) under which $(X,Y)$ is consistent;
2. if it does not, it is unknown whether $(X,Y)$ is still consistent;
3. even if consistent, the convergence rate is unknown, so there is no error bar for the given $N$;
4. adversarial sequences that fool $(X,Y)$ at any finite $N$ are easy to build. A density can follow a power law up to $\epsilon N$ and then drop, or follow a non-power law up to $\epsilon N$ and then flatten.

Even so, these estimators are the best available, because they have been validated in controlled settings.
:::

(sec-pl-example)=
## Worked example

All numbers were computed with numpy (`default_rng` with the stated seeds).

**1. Bin centre ({prf:ref}`prop-pl-geo-centre`).** Here $b=1$. The width ratios are $\beta_b = 2$ and $\beta_b = 10^{0.2}\approx1.585$, the latter being 20 bins over four decades.

| $\gamma$ | $\beta_b$ | $x^*$ | geometric $\sqrt{\beta_b}$ | arithmetic $(1+\beta_b)/2$ |
|---|---|---|---|---|
| 2.0 | 2 | 1.4142 | 1.4142 | 1.5000 |
| 2.5 | 2 | 1.4003 | 1.4142 | 1.5000 |
| 3.0 | 2 | 1.3867 | 1.4142 | 1.5000 |
| 2.5 | 1.585 | 1.2534 | 1.2589 | 1.2924 |

**2. Binning $N=10^5$ Pareto samples** ($\gamma=2.5$, $k_{\min}=1$, seed 3).
- **20 linear bins** of width ≈ 295: the counts are 99,984, 7, 5, 2, then mostly zeros. Useless.
- **20 log bins:** counts 47,841, 24,954, 13,035, … , 7, 5, 3, 2, 0, 0, 2 (18 bins non-empty).
- **Least-squares slope** of $\ln Y_i$ vs $\ln X_i$: $-2.40$ using all occupied bins, and $-2.54$ using the 13 bins with at least 10 counts. The true value is $-2.5$.

**3. Pooling vs averaging curves.**
- Graph A has 1 node of degree $k$, with $c_i = 0$. Graph B has 99 nodes of degree $k$, each with $c_i=0.5$.
- **Pooled:** $c(k) = (0 + 99\times0.5)/100 = 0.495$.
- **Averaged curves:** $(0+0.5)/2 = 0.25$, which is wrong by a factor of 2.

**4. Natural cutoff ({prf:ref}`cor-pl-kmax`).** $\gamma=2.5$ gives $\xi = 2/3$, $N=10^5$, $k_{\min}=1$.
- The scale is $c_N = N^{2/3} = 2154$ and $\Gamma(1/3) = 2.679$, so the predicted mean is $\mathbb E\,k_{\max}\approx 5772$.
- Over 2000 replicates the empirical mean of $k_{\max}$ was 5760.
- The median is a more stable summary, because the Fréchet law with $\xi>1/2$ has infinite variance. It is predicted to be $c_N(\ln 2)^{-\xi} = 2751$; the empirical median was 2707.

**5. Estimators on a power law vs a non-power law.** Both samples have $N=10^5$; the third $\hat\xi$ column is the moments estimator, and $\hat\gamma = 1+1/\hat\xi$ throughout.

| Sample (true $\xi$) | $K$ | $\hat\xi_{\mathrm H}$ | $\hat\gamma_{\mathrm H}$ | $\hat\xi_{\mathrm M}$ | $\hat\gamma_{\mathrm M}$ |
|---|---|---|---|---|---|
| Pareto, $\gamma=2.5$ ($0.667$), seed 1 | 100 | 0.576 | 2.74 | 0.514 | 2.95 |
| | 1000 | 0.657 | 2.52 | 0.589 | 2.70 |
| | 10000 | 0.656 | 2.53 | 0.655 | 2.53 |
| Lognormal $(\mu=1,\sigma=1)$ ($0$), seed 2 | 100 | 0.315 | 4.17 | 0.224 | 5.46 |
| | 1000 | 0.330 | 4.03 | 0.292 | 4.42 |
| | 10000 | 0.469 | 3.13 | 0.315 | 4.18 |

On the Pareto sample, the Hill standard error $\xi/\sqrt K$ is 0.058, 0.021 and 0.0066 for the three $K$. For the lognormal, the true $\xi=0$ (Gumbel MDA), yet both estimators report a positive $\hat\xi$, i.e. a "power law" with $\gamma\approx3$–5. Convergence to $\xi=0$ for lognormal tails is notoriously slow. This is item 4 of {prf:ref}`prop-pl-real-data` in miniature.

**6. Reproducing Voitalov et al.'s classification.**
- The classes, applied to the three estimates per network:
  - **NPL** (not power-law): some $\hat\xi\le0$;
  - **HPL** (hardly power-law): all $\hat\xi>0$ but some $\hat\xi\le\tfrac14$ (i.e. $\hat\gamma\ge5$);
  - **DSM**: all $\hat\xi>\tfrac12$ ($\hat\gamma<3$);
  - **PL**: otherwise.
- Applied to the 35 undirected networks of Table I, this gives:
  - NPL 7 (all three road networks, Chicago roads, Livemocha, Reactome, the URV e-mail network);
  - HPL 11 (e.g. power grid, DBLP, actor collaborations);
  - PL 7;
  - DSM 10 (e.g. CAIDA and Route Views ASes, Skitter, YouTube, WordNet).
- This matches Fig. 3a of the paper.

## Assumptions and limitations

- **i.i.d. degrees.** All consistency proofs assume independent samples. The degrees of one graph are dependent: their sum is even, the sequence must be graphical (Erdős–Gallai, [page 05](./05-configuration-models.md)), and in growth models the degrees are correlated.
- **Discreteness.** The EVT results are stated for continuous laws, while degrees are integers with many ties at low $k$. *Own commentary:* ties make the log-spacings in the Hill/kernel formulas zero, so the tail fraction $K$ should sit above the tie-heavy region.
- **Definition-dependence.** "Scale-free or not" depends on whether you test pure power laws above a cutoff (Clauset–Shalizi–Newman, Broido–Clauset) or regular variation (Voitalov et al.). State which you mean.
- **Binning is for display only.** Binned plots are for looking at data. Estimation should use the raw sequence, or the CCDF, which needs no binning at all (*own commentary*, consistent with [](doi:10.1080/00107510500052444)).
- **The transcription's colours.** In the local transcription of Voitalov's Table I, the per-cell colours don't always match the paper's class rules. For example, Flixster is coloured red although no estimate is $\le 0$, which makes it HPL. The counts above were recomputed from the numbers, not the colours.

## Connections

- **NETS 5116.**
  - [Barabási ch. 4](../nets-5116/barabasi/04-scale-free-networks.md) introduces $p_k\sim k^{-\gamma}$, the natural cutoff and log binning heuristically; this page makes those rigorous ({prf:ref}`cor-pl-kmax`).
  - [Newman ch. 10 notes](../nets-5116/newman/10-structure-of-real-world-networks.md) cover CCDF plots and log binning, with Newman's $\alpha$ for our $\gamma$.
  - The $\gamma$ regimes 2–3 that matter for [robustness](../nets-5116/barabasi/08-network-robustness.md) are exactly the DSM class {eq}`eq-pl-dsm`.
- **NETS 6116.**
  - Power laws are, like [sparsity and small-worldness](./01-sparsity-and-small-worlds.md), properties of sequences of graphs.
  - Hypersoft ensembles generate power laws by drawing the hidden variable $\kappa_i$ from a Pareto $\rho(\kappa)$. In the [HSCM](./05-configuration-models.md) and other [hidden-variable models](./07-hidden-variables-and-graphons.md), the degree tail then inherits the exponent of $\rho(\kappa)$.
  - In [hyperbolic latent-space models](./08-latent-space-models.md), $\gamma$ is set by the radial density.
- **PHYS 7335.**
  - $\xi>\tfrac12$ ⇔ $\langle k^2\rangle=\infty$ ⇔ vanishing [HMF epidemic threshold](../phys-7335/05-heterogeneous-mean-field.md) and vanishing [SIR percolation threshold](../phys-7335/07-sir-percolation.md).
  - On finite networks, the threshold is controlled by $k_{\max}\sim N^{\xi}$ from {eq}`eq-pl-kmax`. In the [quenched picture](../phys-7335/06-quenched-mean-field.md), $\Lambda_{\max}\ge\sqrt{k_{\max}}$.
- **NETS 7332.**
  - Degree is the first hand-crafted node feature ([basics 01](../nets-7332/basics/01-graph-ml-tasks-and-features.md)).
  - Comparing degree distributions is a standard check on [graph generative models](../nets-7332/basics/08-scaling-and-generative.md). The same estimator caveats apply when someone reports a generated graph "has $\gamma=2.3$".

## Self-test

:::{dropdown} Q1. You have $c_i$ for every node in 50 sampled graphs. How do you produce one $c(k)$ plot?
Concatenate all $(k_i, c_i)$ records from all 50 graphs into one dataset. Choose log bins in $k$ (about 20). Within each bin, average the $c_i$ ({prf:ref}`def-pl-binned-values`); `scipy.stats.binned_statistic(..., 'mean')` does this. Do **not** average the 50 per-graph $c(k)$ curves, because that overweights sparsely populated degree classes.
:::

:::{dropdown} Q2. What does "the degree distribution is a power law with exponent γ" mean rigorously, and why can't it hold for one network?
The CCDF is $\ell(k)k^{-(\gamma-1)}$ with $\ell$ slowly varying, i.e. the law is regularly varying. Equivalently, it lies in the Fréchet MDA with $\xi = 1/(\gamma-1)$. This is a statement about $k\to\infty$. A finite network has a bounded degree sequence, so the property only makes sense for a sequence of graphs or an ensemble, and $\gamma$ can only be estimated.
:::

:::{dropdown} Q3. Derive $k_{\max}$ for a Pareto tail with exponent γ, and say how it differs from Barabási's natural cutoff.
Set $\bar F(c_N) = 1/N$, which gives $c_N = k_{\min}N^{1/(\gamma-1)}$. Then $\Pr(k_{\max}\le c_N x) = (1-x^{-\alpha}/N)^N\to e^{-x^{-\alpha}}$ (Fréchet), whose mean is $\Gamma(1-\xi)$. So $\mathbb E k_{\max}\approx\Gamma(1-\xi)k_{\min}N^{1/(\gamma-1)}$. Barabási's estimate is $c_N$, which has the same scaling and differs by an $O(1)$ prefactor (2.68 at $\gamma=2.5$).
:::

:::{dropdown} Q4. Why can the Hill estimator never conclude "not a power law", and what is used instead?
$\hat\xi_{\mathrm H}$ is a mean of logs of ratios $k_{(i)}/k_{(K+1)}\ge1$, so it is always positive. The moments and kernel estimators can return $\hat\xi\le0$ (Weibull/Gumbel), so Voitalov et al. classify a network as NPL when any of the three estimators gives $\hat\xi\le0$.
:::

:::{dropdown} Q5. State the two conditions on $K$ for consistency, and explain each.
$K\to\infty$, so the variance $\approx\xi^2/K\to0$. And $K/N\to0$, so only the far tail is used, where $\ell$ is effectively constant and the bias vanishes. The double bootstrap picks the AMSE-optimal $K^*$ satisfying both.
:::

:::{dropdown} Q6. For which γ is ⟨k²⟩ infinite, in terms of ξ, and why does it matter?
$\langle k^2\rangle = \infty$ iff $\alpha<2$, i.e. $\gamma<3$, i.e. $\xi>1/2$. In that regime the heterogeneous mean-field epidemic threshold $\langle k\rangle/\langle k^2\rangle$ and the random-failure percolation threshold both go to 0. Voitalov et al. require *all three* estimators to give $\hat\xi>1/2$ before calling a network DSM.
:::

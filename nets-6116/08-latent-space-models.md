---
title: Latent-Space Models — Random Geometric, Soft Geometric and Hyperbolic Graphs
short_title: Latent-space models
subject: NETS 6116 · Topic
description: How putting nodes in a metric space and connecting them by distance yields sparse, clustered, small-world and (in hyperbolic space) scale-free graphs, with the β-phase diagram, the derivation of μ, and the S¹ ↔ H² isomorphism.
tags: [latent-space-models, random-geometric-graphs, soft-rgg, girg, hyperbolic-graphs, s1-model, maximum-entropy, clustering, small-world, projectivity]
---

:::{tip} TL;DR
- A **latent-space model (LSM)** is a hidden-variable model in which each node's hidden variable is a position $x_i$ in a metric space, and $p_{ij} = p(d(x_i,x_j))$ decreases with distance. The triangle inequality in the space produces **triangles in the graph**, so geometry is the standard explanation for strong clustering.
- **Soft RGG (SRGG).** On a line with unit node density, the Fermi–Dirac choice $p_{ij} = 1/\bigl(1 + (x_{ij}/r_0)^{\beta}\bigr)$ is a grand-canonical ensemble. The inverse temperature $\beta$ fixes the total log-length of the edges, and the chemical potential fixes $\langle k\rangle$. The limit $\beta\to\infty$ gives the sharp RGG and $\beta\to 0$ gives ER.
- **β phase diagram (ultrasparse, $\langle k \rangle$ fixed).** Clustering stays non-zero as $N\to\infty$ **iff $\beta>1$**; the same $\beta>1$ makes $p$ integrable, hence $N$-independent and **projective**. The graph is a **small world iff $\beta<2$**. Only $1<\beta<2$ gives both.
- **S¹ model / GIRG.** $p_{ij} = \bigl[1 + \bigl(x_{ij}/(\mu\kappa_i\kappa_j)\bigr)^{\beta}\bigr]^{-1}$ with $\mu = \dfrac{\beta\sin(\pi/\beta)}{2\pi\langle k\rangle}$, which makes the expected degree of node $i$ equal to $\kappa_i$ (for $\beta>1$). Degrees come from $\rho(\kappa)$; clustering comes from $\beta$.
- **S¹ ↔ H².** Set $r_i = R - 2\ln(\kappa_i/\kappa_0)$ and $R = 2\ln\bigl(N/(\pi\mu\kappa_0^2)\bigr)$. Then $p_{ij} = 1/\bigl(1+e^{\frac{\beta}{2}(d_{\mathbb H}(i,j)-R)}\bigr)$, a purely geometric model on the hyperbolic disk. A radial density $\propto e^{\alpha(r-R)}$ gives $p_k\sim k^{-\gamma}$ with $\gamma = 2\alpha+1$, so points spread **uniformly** over the hyperbolic disk ($\alpha=1$) give $\gamma=3$.
:::

- **Source.**
  - Krioukov, *Network Science II* lecture notes, ch. 13 (Latent space models).
  - Primary papers the chapter builds on:
    - [](doi:10.1198/016214502388618906) (Hoff, Raftery & Handcock, *JASA* 97, 2002): latent-space models in statistics.
    - [](doi:10.1103/PhysRevLett.100.078701) (Serrano, Krioukov & Boguñá, *PRL* 100, 078701, 2008): the $\mathbb{S}^1$ model and $\mu$.
    - [](doi:10.1103/PhysRevE.82.036106) (Krioukov, Papadopoulos, Kitsak, Vahdat & Boguñá, *PRE* 82, 036106, 2010): hyperbolic random graphs, $\gamma = 2\alpha+1$ and the Fermi–Dirac form.
    - [](doi:10.1038/nature11459) (Papadopoulos, Kitsak, Serrano, Boguñá & Krioukov, *Nature* 489, 537, 2012): popularity × similarity, the growing (projective) version.
    - [](doi:10.1016/j.tcs.2018.08.014) (Bringmann, Keusch & Lengler, *Theor. Comput. Sci.* 760, 2019): GIRGs.
    - [](doi:10.1038/s42254-020-00264-4) (Boguñá et al., *Nat. Rev. Phys.* 3, 114, 2021): review of network geometry.
  - Sharp RGGs: [](doi:10.1093/acprof:oso/9780198506263.001.0001) (Penrose, *Random Geometric Graphs*, 2003).
- **Builds on.**
  - Hidden-variable models and the Fermi–Dirac / ERGM correspondence: [Hidden variables and graphons](./07-hidden-variables-and-graphons.md).
  - SCM and HSCM: [Configuration models](./05-configuration-models.md).
  - Maximum-entropy ensembles: [Typicality and maximum entropy](./04-typicality-and-max-entropy.md).
  - Sparsity and small worlds: [Sparsity and small worlds](./01-sparsity-and-small-worlds.md).
- **Notation.** Shared symbols as in [](#notation), including $\kappa_i$, $\rho(\kappa)$, $\lambda_i$, $\theta_i$, $r_i$.
  - Here $\beta$ is the **inverse temperature** (not the transmission rate), and $\mu$ is the **S¹ scale parameter** that fixes $\langle k\rangle$ (not the recovery rate).
  - Krioukov writes $n$, $\bar k$ and $\bar c$; these are $N$, $\langle k\rangle$ and $\langle C\rangle$ here.
  - Page-specific symbols:
    - $x_{ij}$ is the **latent** distance between $i$ and $j$ on the line or circle, with node density 1. It is distinct from the graph distance $d_{ij}$.
    - $d_{\mathbb H}(i,j)$ is the hyperbolic distance.
    - $r_c$ is the sharp-RGG connection radius, and $R$ the hyperbolic disk radius.
    - $\chi_{ij}$ is defined by $p_{ij} = 1/(\chi_{ij}+1)$.
    - $\mathcal{E}_{ij} = \ln x_{ij}$ is the edge "energy".

(sec-lsm-setup)=
## Setup and definitions

:::{prf:definition} Latent-space model
:label: def-lsm-lsm

A **latent-space model** is a hidden-variable network model in which:

1. the hidden variable of node $i$ is a random point $x_i$ of a metric space, drawn from a density $\rho(x)$;
2. edges are independent given the coordinates, with $p_{ij} = \hat p\bigl(d(x_i,x_j)\bigr)$ for a non-increasing $\hat p$.

Probabilists call these *soft random geometric graphs*. Sociologists have used them for social distance since the 1920s; the statistical latent-space model of Hoff et al. (2002) is a logistic $\hat p$ with coordinates estimated from data.
:::

:::{prf:definition} Random geometric graph (1D)
:label: def-lsm-rgg

Place $N$ points i.i.d. uniform on $[0,N]$ (density 1) and connect $i,j$ iff $x_{ij} = \lvert x_i - x_j\rvert < r_c$, i.e. $\hat p(x) = \mathbb{1}\{x<r_c\}$. Every node has the same expected properties, with $\langle k\rangle = 2r_c$ and $p_k \to \mathrm{Poisson}(2r_c)$.
:::

:::{prf:definition} Projectivity and exchangeability
:label: def-lsm-projective

- A model is **projective** if there is a growing algorithm that adds nodes one at a time, never changes the (non-)edges among existing nodes, and generates an infinite graph of the model when run forever. Equivalently, the size-$N$ graph is the induced subgraph of the size-$(N{+}1)$ one.
- A model is **(finitely) exchangeable** if $P(G)$ is invariant under relabelling the nodes.

Examples from the notes:
- **Not projective:** $G(N,p)$ with $p=\langle k\rangle/N$; HSCM with $\gamma\neq3$; and RGGs generated by sprinkling $N$ uniform points on $[0,N]$, because $p$ or the density depends on $N$.
:::

:::{prf:definition} Poisson point process
:label: def-lsm-ppp

A point process on $\mathbb{R}$ is **Poisson of rate 1** if the number of points in any interval of length $\ell$ is $\mathrm{Poisson}(\ell)$, and the counts in disjoint intervals are independent.
:::

## Core ideas

(sec-lsm-generation)=
### Three ways to generate an RGG, and why the third is the right one

| Option | Algorithm | Point process | Problem |
|---|---|---|---|
| 1 | $N$ i.i.d. uniform points on $[0,N]$, connect within $r_c$ | **Binomial**: an interval of length $\ell$ holds $\mathrm{Bin}(N,\ell/N)$ points, so disjoint counts are dependent | Exchangeable but sparse, so by Aldous–Hoover there is no exchangeable $N\to\infty$ limit (the density $1/N\to0$); counts are dependent |
| 2 | Draw $N\sim\mathrm{Poisson}(\bar N)$, then option 1 on $[0,\bar N]$ | **Poisson** of rate 1 on $[0,\bar N]$ | Fixes the dependence, but $N$ is now random and there is still no limit |
| 3 | $x_0 = 0$; for $n=1,2,\dots$: $x_n = x_{n-1} + \mathrm{Exp}(1)$, connect $n$ to every earlier $i$ with $x_n - x_i < r_c$ | Poisson of rate 1 on $\mathbb{R}^+$, points labelled in increasing order | None: projective, and run forever it produces the infinite RGG |

Facts to remember about option 3:

- $x_n \sim \mathrm{Gamma}(n,1)$, so $\langle x_n\rangle = n$ but $x_n\neq n$: one can fix the number of nodes **or** the length of the interval, not both.
- The projective version is **not** exchangeable, and that is fine because labels carry information (the order of arrival).
- For finite $N$ one moves between the two formulations freely. A uniformly random permutation of the labels makes the projective graph exchangeable, and sorting the labels by coordinate makes an exchangeable graph projective. At $N=\infty$ neither works, since there is no uniform distribution on infinitely many permutations.
- Any space of infinite volume (such as $\mathbb{R}^d$, $\mathbb{H}^d$ or non-compact manifolds) can hold infinitely many points at constant density. The same construction therefore works there. The notes stay in one dimension.

(sec-lsm-srgg)=
### Soft RGGs: choosing $p(x)$

Put the node at the origin and the others with density 1 on $[-N/2,N/2]$. The expected degree is

$$
\langle k\rangle \approx 2\int_0^{N/2} p(x)\,dx \;\xrightarrow{N\to\infty}\; 2\int_0^{\infty} p(x)\,dx .
$$ (eq-lsm-kbar)

**Ultrasparsity** ($\langle k\rangle$ constant) together with **projectivity** ($p$ independent of $N$) requires $p$ to be integrable, i.e. to decay faster than $1/x$. The notes take $p(x) = c\,x^{-\beta}$ with $\beta>1$, cap it as $\min(1, c x^{-\beta})$, and recognise the cap as the Chung–Lu-style approximation of the smooth form

$$
p(x) = \frac{1}{x^{\beta}/c + 1} = \frac{1}{e^{\beta\mathcal{E}(x) + \lambda} + 1} = \frac{1}{e^{\beta(\mathcal{E}(x) - \mu_{\mathrm{ch}})} + 1}, \qquad \mathcal{E}(x) = \ln x,\; \lambda = -\ln c,\; \mu_{\mathrm{ch}} = -\lambda/\beta .
$$ (eq-lsm-fd)

Equivalently $p(x) = 1/\bigl(1+(x/r_0)^\beta\bigr)$ with $r_0 = e^{\mu_{\mathrm{ch}}} = c^{1/\beta}$. Krioukov calls the chemical potential $\mu$; it is $\mu_{\mathrm{ch}}$ here to keep $\mu$ for the S¹ scale.

### Statistical-mechanics reading

Because {eq}`eq-lsm-fd` is Fermi–Dirac in $\lambda_{ij} = \beta\mathcal{E}_{ij} + \lambda$, the hidden-variable theorem (Thm 11.2 of the notes; see [Hidden variables and graphons](./07-hidden-variables-and-graphons.md)) says that **with the coordinates frozen** the SRGG is an ERGM:

$$
P(G\mid\{x_i\}) = \frac{1}{Z}\exp\Bigl(-\beta\,\mathcal{E}(G) - \lambda\,L(G)\Bigr), \qquad L(G) = \sum_{i<j}A_{ij},\quad \mathcal{E}(G) = \sum_{i<j}\mathcal{E}_{ij}A_{ij}.
$$ (eq-lsm-ergm)

| Gas of fermions | SRGG |
|---|---|
| particle | edge |
| energy of state $(i,j)$ | $\mathcal{E}_{ij} = \ln x_{ij}$ (log-length) |
| inverse temperature $\beta$ | fixes the mean total log-length $\langle\mathcal{E}\rangle$ |
| chemical potential $\mu_{\mathrm{ch}}$ | fixes the mean number of edges, i.e. $\langle k\rangle$ |

- $\mathcal{E}(G)$ is the log of the product of edge lengths, so it can only be computed from the coordinates: graphs are labelled by both $i$ and $x_i$.
- With **random** coordinates the SRGG is **hypercanonical**, a mixture of ERGMs.
- The microcanonical version is degenerate (essentially one graph), since $\mathcal{E}(G)$ takes real values.

### The two limits of β

- **$\beta\to\infty$ (zero temperature).** $p_{ij}\to\mathbb{1}\{\mathcal{E}_{ij}<\mu_{\mathrm{ch}}\} = \mathbb{1}\{x_{ij}<r_0\}$: the sharp RGG. There are no long edges, so with $r_0$ fixed the graph is a **large world**.
- **$\beta\to0$ (infinite temperature).** For $\beta<1$, $\int^{N}x^{-\beta}dx\sim N^{1-\beta}$ diverges, so one must choose:
  - **Option 1:** keep $p$ fixed (projective) and accept $\langle k\rangle\sim N^{1-\beta}$.
  - **Option 2:** keep $\langle k\rangle$ fixed and accept non-projectivity. Take $p_N(x) = \min(1, c_N x^{-\beta})$ with $c_N\sim N^{\beta-1}$. As $\beta\to0$, $p\to c_N\to\langle k\rangle/N$: **ER**.

  The notes (and this page) use option 2 whenever $\beta<1$.

$$
\text{ER} \xleftarrow{\;\beta\to0\;} \text{SRGG} \xrightarrow{\;\beta\to\infty\;} \text{RGG}
$$

(sec-lsm-dc)=
### Degree correction: GIRGs and the S¹ model

SRGGs are homogeneous (Poisson degrees). The maximum-entropy way to add heterogeneity is to put a Lagrange multiplier on every degree, as in the SCM, **and** keep the geometric term:

| Model | $p_{ij}$ | $P(G\mid\text{hidden variables})\propto$ |
|---|---|---|
| ER | $1/(e^{\lambda}+1)$ | $e^{-\lambda L(G)}$ |
| SCM | $1/(e^{\lambda_i+\lambda_j}+1)$ | $e^{-\sum_i\lambda_i k_i(G)}$ |
| SRGG (ER + geometry) | $1/(e^{\beta\mathcal{E}_{ij}+\lambda}+1)$ | $e^{-\beta\mathcal{E}(G)-\lambda L(G)}$ |
| **DC-SRGG** (SCM + geometry) | $1/(e^{\beta\mathcal{E}_{ij}+\lambda_i+\lambda_j}+1)$ | $e^{-\beta\mathcal{E}(G)-\sum_i\lambda_i k_i(G)}$ |

The DC-SRGG goes under several names:
- **GIRG** (geometric inhomogeneous random graph), because the (H)SCM is an *inhomogeneous random graph*;
- **RHG** (random hyperbolic graph) in its hyperbolic form;
- the **$\mathbb{S}^1$ model** of Serrano et al. (2008) on the circle.

In the hypercanonical version both $x_i$ and $\lambda_i$ (equivalently $\kappa_i$) are random. Mapping $\kappa_i\mapsto u_i = F(\kappa_i)$ through the CDF of $\rho$ turns this into a graphon-like function on $([0,1]\times[0,N])^2$, exactly as for the HSCM.

The hyperbolic picture separates two coordinates of a node:
- the **angle** $\theta_i$ is *similarity*: nearby nodes are alike;
- the **radius** $r_i$ is *popularity*: small $r_i$ means large $\kappa_i$, a hub.

Papadopoulos et al. (2012) make this growing, the *popularity × similarity* model. A new node links to existing nodes that minimise (birth time) × (angular distance), which reproduces preferential attachment as an emergent effect of hyperbolic geometry.

(sec-lsm-results)=
## Key results

:::{prf:theorem} Expected degree in the DC-SRGG and the value of μ
:label: thm-lsm-mu

Let $\kappa_i\sim\rho(\kappa)$ with finite mean $\langle k\rangle$, let $x_i$ be uniform on a circle of circumference $N$ (so $x_{ij} = N/2 - \lvert N/2 - \lvert x_i-x_j\rvert\rvert$), and let $N\gg1$. With $\chi_{ij} = x_{ij}^{\beta}e^{\lambda_i+\lambda_j}$ and $p_{ij} = 1/(\chi_{ij}+1)$, the expected degree of node $i$ converges to $\kappa_i$ if

| | $\beta>1$ | $\beta<1$ |
|---|---|---|
| $\lambda_i$ | $-\beta\ln(\kappa_i/\sqrt{c})$ | $-\ln(\kappa_i/\sqrt{c})$ |
| $\chi_{ij}$ | $\bigl(c\,x_{ij}/(\kappa_i\kappa_j)\bigr)^{\beta}$ | $c\,x_{ij}^{\beta}/(\kappa_i\kappa_j)$ |
| $c$ | $2\langle k\rangle\,\dfrac{\pi/\beta}{\sin(\pi/\beta)}\;\xrightarrow{\beta\to\infty}\;2\langle k\rangle$ | $\dfrac{2^{\beta}\langle k\rangle N^{1-\beta}}{1-\beta}\;\xrightarrow{\beta\to0}\;\langle k\rangle N$ |

For $\beta>1$ write $\mu = 1/c$. This is the $\mathbb{S}^1$ model:

$$
p_{ij} = \frac{1}{1+\left(\dfrac{x_{ij}}{\mu\,\kappa_i\kappa_j}\right)^{\beta}}, \qquad \mu = \frac{\beta\,\sin(\pi/\beta)}{2\pi\langle k\rangle}.
$$ (eq-lsm-s1)
:::

:::{dropdown} Derivation of μ (β > 1)
1. **Expected degree.** Node $i$ sits at the origin. Other nodes have density 1 in $x$ and hidden variable $\kappa'\sim\rho$, independently. Then
   $\bar k(\kappa_i) = \int\rho(\kappa')\,d\kappa'\; 2\int_0^{N/2}\frac{dx}{1+\bigl(x/(\mu\kappa_i\kappa')\bigr)^{\beta}}$.
2. **Large $N$.** For $\beta>1$ the integrand decays like $x^{-\beta}$, which is integrable, so the upper limit can go to $\infty$. This assumes $\mu\kappa_i\kappa'\ll N$, i.e. no node's connection range covers a finite fraction of the circle. Substituting $t = x/(\mu\kappa_i\kappa')$,
   $\bar k(\kappa_i) = 2\mu\kappa_i\langle\kappa\rangle\int_0^{\infty}\frac{dt}{1+t^{\beta}} = 2\mu\kappa_i\langle k\rangle\,\frac{\pi/\beta}{\sin(\pi/\beta)}$.
3. **Fix μ.** Setting $\bar k(\kappa_i) = \kappa_i$ for every $i$ gives the value of $\mu$ in {eq}`eq-lsm-s1`. Because $\bar k$ is linear in $\kappa_i$, one constant fixes all nodes at once. The $\mu$ in the notes' convention $\lambda_i = -\beta\ln(\kappa_i\sqrt{\mu})$ follows directly.
4. **Why β < 1 differs.** For $\beta<1$ the integral diverges at its upper limit, so $c$ must grow with $N$ (option 2 above). With the cap $\min(1,\kappa_i\kappa'/(c x^\beta))$ the integral is $\frac{2\kappa_i\kappa'}{c}\frac{(N/2)^{1-\beta}}{1-\beta}$, and setting $\bar k = \kappa_i$ gives $c = 2^{\beta}\langle k\rangle N^{1-\beta}/(1-\beta)$. As $\beta\to0$, $p_{ij}\to\kappa_i\kappa_j/(\langle k\rangle N)$, the Chung–Lu/HSCM form. The degree is linear in the hidden variable in both regimes; only $c$ changes.
:::

:::{prf:theorem} The β phase diagram of ultrasparse SRGGs
:label: thm-lsm-phases

At $N\to\infty$ with $\langle k\rangle$ fixed:

1. **Clustering** (notes Thm 13.8): $\langle C\rangle>0$ iff $\beta>1$, and $\langle C\rangle(\beta)$ is non-decreasing in $\beta$. It tends to the sharp-RGG value as $\beta\to\infty$, which is $3/4$ in one dimension.
2. **Small-worldness** (notes Thm 13.7): the graph is a small world iff $\beta<2$.

| $\beta$ | strong clustering and projectivity | small world |
|---|---|---|
| $\to0$ (ER), $<1$ | ✗ | ✓ |
| $1<\beta<2$ | ✓ | ✓ |
| $>2$, $\to\infty$ (RGG) | ✓ | ✗ |
:::

:::{dropdown} Why these thresholds (intuition, plus the probability literature)
- **$\beta=1$ (clustering).** For $\beta<1$ the edge-length distribution is dominated by lengths of order $N$. A node's neighbours are then spread over the whole space, and the triangle inequality stops forcing triangles. The notes call this the loss of *geometricity*.
  - For $\beta>1$, $\int p<\infty$, so most edges have length $O(1)$ and neighbours of a node are near each other.
  - The same integrability makes $p$ independent of $N$, so the coincidence of **projectivity** and **clustering** at $\beta>1$ has one cause.
  - The transition itself is analysed by [](doi:10.1038/s42005-022-01023-w) (van der Kolk, Serrano & Boguñá, *Commun. Phys.* 5, 245, 2022). In their *anomalous* transition, clustering decays only logarithmically in $N$ near $\beta=1$. Its weakly geometric side $\beta<1$ is treated in [](doi:10.1103/PhysRevResearch.6.013337) (*PRR* 6, 013337, 2024).
- **$\beta=2$ (small world).** The tail $p\sim x^{-\beta}$ is that of **long-range percolation** with exponent $s=\beta$ in dimension $d=1$, whose chemical distances are known.
  - For $d<s<2d$, distances grow like $(\ln N)^{\Delta}$ with $\Delta = \ln2/\ln(2d/s)$: [](doi:10.1214/009117904000000577) (Biskup, *Ann. Probab.* 32, 2004); and [](doi:10.1002/rsa.1022) (Benjamini & Berger, *RSA* 19, 2001).
  - At $s=2d$, distances grow like $N^{\theta(s)}$ with $\theta\in(0,1)$: [](doi:10.48550/arXiv.1303.3995) (Ding & Sly, 2013).
  - For $s>2d$ they grow linearly: [](doi:10.48550/arXiv.math/0409021) (Berger, 2004).
  - The notes credit the recent understanding of the $\beta=2$ transition to Hutchcroft (2025).

  *My comment:* for $1<\beta<2$, "small world" therefore means **polylogarithmic**, not strictly $\ln N$. The notes' $\checkmark$ uses the looser $d = o(N^{\epsilon})$ sense of [Sparsity and small worlds](./01-sparsity-and-small-worlds.md).
- **RGG clustering = 3/4 (the "Final!" question in the notes).** Two neighbours of a node are i.i.d. uniform on $(-r_c,r_c)$, at positions $u, v$. They are linked iff $\lvert u-v\rvert<r_c$. The complementary region $\lvert u-v\rvert>r_c$ is two corner triangles of total area $(r_c)^2$ out of $(2r_c)^2$, so $\langle C\rangle = 1-\tfrac14 = \tfrac34$. In $d$ dimensions it decreases towards the ER value as $d$ grows: [](doi:10.1103/PhysRevE.66.016121) (Dall & Christensen, *PRE* 66, 2002).
:::

:::{prf:theorem} S¹ ↔ H² isomorphism
:label: thm-lsm-iso

Take the $\mathbb{S}^1$ model {eq}`eq-lsm-s1` with $\beta>1$ and $\kappa_i\ge\kappa_0$. Write the angle $\theta_i = 2\pi x_i/N$, with angular distance $\theta_{ij} = \pi-\lvert\pi-\lvert\theta_i-\theta_j\rvert\rvert$, and set

$$
r_i = R - 2\ln\frac{\kappa_i}{\kappa_0}, \qquad R = 2\ln\frac{N}{\pi\mu\kappa_0^{2}} .
$$ (eq-lsm-radial)

Then, identically,

$$
p_{ij} = \frac{1}{1 + e^{\frac{\beta}{2}\left(d_{ij}^{\approx} - R\right)}}, \qquad d_{ij}^{\approx} = r_i + r_j + 2\ln\frac{\theta_{ij}}{2},
$$ (eq-lsm-h2)

and $d_{ij}^{\approx}$ is the large-$r$ approximation of the distance $d_{\mathbb H}(i,j)$ between $(r_i,\theta_i)$ and $(r_j,\theta_j)$ in the hyperbolic plane of curvature $-1$.
:::

:::{dropdown} Proof
1. **Rewrite the S¹ argument.** The S¹ argument is $\dfrac{x_{ij}}{\mu\kappa_i\kappa_j} = \dfrac{N\theta_{ij}}{2\pi\mu\kappa_i\kappa_j}$. Substitute $\kappa_i = \kappa_0e^{(R-r_i)/2}$:
   $\dfrac{N\theta_{ij}}{2\pi\mu\kappa_0^2}\,e^{(r_i+r_j)/2 - R}$.
2. **Use the definition of $R$.** It gives $N/(\pi\mu\kappa_0^2) = e^{R/2}$, so the argument is
   $\dfrac{\theta_{ij}}{2}\,e^{(r_i+r_j)/2 - R/2} = \exp\!\Bigl[\tfrac12\bigl(r_i+r_j+2\ln\tfrac{\theta_{ij}}{2} - R\bigr)\Bigr]$.
   Raising to the power $\beta$ gives $\chi_{ij} = e^{\frac\beta2(d^{\approx}_{ij}-R)}$, which is exact, not an approximation.
3. **Hyperbolic law of cosines.** $\cosh d_{\mathbb H} = \cosh r_i\cosh r_j - \sinh r_i\sinh r_j\cos\theta_{ij}$. For $r_i,r_j\gg1$ the right side is $\approx\tfrac14 e^{r_i+r_j}(1-\cos\theta_{ij}) = \tfrac12e^{r_i+r_j}\sin^2(\theta_{ij}/2)$. With $\cosh d\approx e^{d}/2$ this gives $d_{\mathbb H}\approx r_i+r_j+2\ln\sin(\theta_{ij}/2)$. That is $\approx d^{\approx}_{ij}$ when $\theta_{ij}$ is small, which it is for the pairs that can connect, since $p$ is non-negligible only when $d\lesssim R$.
4. **Statistical mechanics again.** {eq}`eq-lsm-h2` is Fermi–Dirac in the hyperbolic edge length. With coordinates frozen the RHG is therefore an ERGM with just **two** sufficient statistics: $L(G)$, and the total hyperbolic length $\sum_{i<j}d_{\mathbb H}(i,j)A_{ij}$, at inverse temperature $\beta/2$. The GIRG reading of the same model has $N+1$ statistics: every degree, plus the total log-length.
:::

:::{prf:theorem} Degree exponent from the radial density
:label: thm-lsm-gamma

If $\rho(\kappa) = (\gamma-1)\kappa_0^{\gamma-1}\kappa^{-\gamma}$ on $[\kappa_0,\infty)$ (Pareto), then under {eq}`eq-lsm-radial`

$$
\rho(r) = \alpha\,e^{\alpha(r-R)},\quad 0\le r\le R, \qquad \alpha = \frac{\gamma-1}{2}\;\Longleftrightarrow\;\gamma = 2\alpha+1 .
$$ (eq-lsm-alpha)

For $\gamma=3$ we get $\alpha=1$. That is the area element of the hyperbolic disk ($\propto\sinh r\approx e^{r}/2$), so the nodes are **uniformly distributed over the hyperbolic disk of radius $R$**. Exponential expansion of space alone then produces a power law.
:::

:::{dropdown} Derivation
- Change of variables: $\kappa = \kappa_0e^{(R-r)/2}$ and $\lvert d\kappa/dr\rvert = \kappa/2$. Hence
  $\rho(r) = \rho(\kappa)\,\kappa/2 = \tfrac{\gamma-1}{2}\,(\kappa/\kappa_0)^{-(\gamma-1)} = \tfrac{\gamma-1}{2}\,e^{\frac{\gamma-1}{2}(r-R)}$.
- $\kappa\ge\kappa_0$ means $r\le R$. Requiring $r\ge0$ cuts $\kappa$ off at $\kappa_0e^{R/2}=\sqrt{N/(\pi\mu)}$, the natural cutoff $\propto N^{1/2}$; for $\gamma<3$ this is stricter than $N^{1/(\gamma-1)}$.
- The expected degree equals $\kappa$ (Thm {prf:ref}`thm-lsm-mu`). In the sparse limit the degree is Poisson given $\kappa$, so $p_k$ inherits the $\kappa^{-\gamma}$ tail.
- Conversely, sprinkle points with $\rho(r) = \alpha e^{\alpha(r-R)}$ (Krioukov et al. 2010 write $\alpha$ for the radial exponent and $\zeta$ for $\sqrt{-K}$, giving $\gamma = 2\alpha/\zeta+1$). Then $\kappa(r)\propto e^{(R-r)/2}$ and $\gamma=2\alpha+1$.
:::

:::{prf:theorem} Limits and the RHG "mega-theorem" (notes Thms 13.13–13.14)
:label: thm-lsm-mega

- RHG $\xrightarrow{\beta\to0}$ HSCM for any $\rho(\kappa)$.
- With Pareto $\rho$, RHG $\xrightarrow{\gamma\to\infty}$ SRGG.
- Together with the two SRGG limits, these form a commuting square:
  $\begin{array}{ccc}\text{RHG}&\xrightarrow{\gamma\to\infty}&\text{SRGG}\\ {\scriptstyle\beta\to0}\downarrow&&\downarrow{\scriptstyle\beta\to0}\\ \text{HSCM}&\xrightarrow{\gamma\to\infty}&\text{ER}\end{array}$
- Clustering in the RHG behaves as in the SRGG: $\langle C\rangle = 0$ for $\beta<1$, increasing in $\beta$ for $\beta>1$. Gugelmann, Panagiotou & Peter compute it for the threshold model: [](doi:10.1007/978-3-642-31585-5_51) (ICALP 2012).

| | $2<\gamma<3$ | $\gamma>3$ |
|---|---|---|
| $\beta<1$ (incl. HSCM) | ultra-small world, zero clustering | small world, zero clustering |
| $1<\beta<\infty$ | ultra-small world, positive clustering | small world for $\beta<2$, positive clustering |
| $\beta\to\infty$ (sharp) | ultra-small world, positive clustering | large world, positive clustering |

Hubs with $2<\gamma<3$ keep distances ultra-small ($\ln\ln N$) whatever $\beta$ is. Only without them does $\beta>2$ produce a large world.
:::

### Summary of the models in the notes

| Property | ER | HSCM | SRGG | RHG / GIRG |
|---|---|---|---|---|
| $p_{ij}$ | $\sim\langle k\rangle/N$ | $\sim\kappa_i\kappa_j/N$ | $\sim x_{ij}^{-\beta}$ | $\sim(\kappa_i\kappa_j/x_{ij})^{\beta}$ |
| ultrasparse | ✓ | ✓ | ✓ | ✓ |
| small world | ✓ | ✓ | ✓ if $\beta<2$ | ✓ if $\gamma<3$ or $\beta<2$ |
| strong clustering | ✗ | ✗ | ✓ if $\beta>1$ | ✓ if $\beta>1$ |
| heterogeneous degrees | ✗ | ✓ | ✗ | ✓ |
| projective | ✗ | only $\gamma=3$ | ✓ if $\beta>1$ | ✓ if $\beta>1$ |
| finitely exchangeable | ✓ | ✓ | ✓ (non-projective form) | ✓ (non-projective form) |
| infinitely exchangeable | ✗ | ✗ | ✗ | ✗ |

The notes close with three remarks:
- Watts–Strogatz is SRGG-like but not projective.
- Preferential attachment is HSCM-like but projective.
- The only other known unbiased maximum-entropy model with the RHG's signature (projective, but not infinitely exchangeable) is the degree-corrected SBM ([Stochastic block models](./09-stochastic-block-models.md)).

(sec-lsm-example)=
## Worked example

All numbers below were computed with numpy/networkx (fixed seeds). Nodes were placed on a circle of circumference $N=2000$ with $p_{ij}$ from {eq}`eq-lsm-s1`.

**1. The value of μ.** For $\langle k\rangle = 10$:

| $\beta$ | $\frac{\pi/\beta}{\sin(\pi/\beta)}$ | $\mu$ |
|---|---|---|
| 1.5 | 2.418 | 0.02067 |
| 2 | $\pi/2 = 1.571$ | $1/(10\pi) = 0.03183$ |
| 3 | 1.209 | 0.04135 |
| $\to\infty$ | 1 | $1/(2\langle k\rangle) = 0.05$, i.e. sharp radius $r_0 = \mu\kappa^2 = 5$ and $\langle k\rangle = 2r_0$ |

**2. Clustering grows with β (homogeneous SRGG, $\kappa_i\equiv10$).** One sample per $\beta$:

| $\beta$ | 1.5 | 2 | 3 | 5 | 20 |
|---|---|---|---|---|---|
| measured $\langle k\rangle$ | 9.46 | 9.76 | 9.81 | 9.83 | 9.92 |
| $\langle C\rangle$ | 0.180 | 0.325 | 0.506 | 0.642 | 0.735 |

- $\langle C\rangle$ increases monotonically towards the sharp-RGG value $3/4$. A Monte Carlo check of the $3/4$ with $10^6$ pairs gives 0.7498.
- $\langle k\rangle$ falls short of 10 most at $\beta=1.5$. The $x^{-\beta}$ tail beyond $N/2$ is cut off, and for $\beta$ near 1 that missing tail is large.
- The same truncation slows convergence for $\beta<1$. Integrating the Fermi–Dirac form at $\beta=0.8$ gives $\bar k = 8.34$, $9.47$ and $10.00$ for $N = 4\times10^3$, $4\times10^5$ and $4\times10^7$.

**3. Heterogeneous S¹ ($\gamma=2.5$, $\beta=2$).** The hidden variables are $\kappa_i\sim$ Pareto with $\kappa_0 = \langle k\rangle(\gamma-2)/(\gamma-1) = 3.33$.
- The sample mean was $\bar\kappa = 8.99$, not 10. Heavy tails make $\bar\kappa$ noisy, so $\mu$ was set from $\bar\kappa$. Measured $\langle k\rangle = 8.61$, $\langle C\rangle = 0.445$, transitivity $0.123$, $k_{\max} = 434$.
- Degree tracks the hidden variable:

| $\kappa$ bin | nodes | mean $\kappa$ | mean expected degree $\sum_j p_{ij}$ | mean measured degree |
|---|---|---|---|---|
| $[3.33,4)$ | 474 | 3.65 | 3.55 | 3.52 |
| $[4,6)$ | 733 | 4.83 | 4.73 | 4.64 |
| $[6,12)$ | 500 | 8.07 | 8.07 | 7.87 |
| $[12,30)$ | 218 | 17.93 | 17.55 | 17.91 |
| $\ge30$ | 75 | 63.42 | 57.69 | 57.41 |

  The top bin falls short because hubs violate the $\mu\kappa\kappa'\ll N$ assumption of the derivation: their connection range is a sizeable part of the circle.
- **Mapping to H².** {eq}`eq-lsm-radial` gives $R = 2\ln\bigl(N/(\pi\mu\kappa_0^2)\bigr) = 14.78$ and radii $r_i\in[4.32,14.78]$ (none negative). For three random pairs, $p_{ij}$ from the S¹ formula and from {eq}`eq-lsm-h2` agree to machine precision. For example, pair (0,1) gives $2.598\times10^{-6}$ both ways.
- The approximate distance $d^{\approx}$ exceeds the exact hyperbolic distance by 0.25–0.72 for these pairs. These pairs are far apart and almost never linked. The gap shrinks as $r_i, r_j$ grow and $\theta_{ij}$ shrinks, which is where links actually occur.
- A log-linear fit of the radial histogram over $[R-6,R]$ gives slope 0.69, against $\alpha = (\gamma-1)/2 = 0.75$ from {eq}`eq-lsm-alpha`.

## Assumptions and limitations

- **One dimension.** The notes work on $\mathbb{R}^+$ or $\mathbb{S}^1$. In $d$ dimensions the integrability threshold becomes $\beta>d$ and the small-world threshold $\beta<2d$ (from long-range percolation). Clustering of the sharp RGG falls with $d$ (Dall & Christensen 2002).
- **Finite-size effects are large.**
  - Near $\beta=1$ convergence in $N$ is very slow (worked example 2), and van der Kolk et al. find clustering vanishing only logarithmically there.
  - With $\gamma<3$ the hubs saturate (worked example 3).
  - The heavy-tailed sample mean $\bar\kappa$ fluctuates strongly between realisations.
- **The H² form is exact only through $d^{\approx}$.** Using the true hyperbolic distance with a sharp threshold is a slightly different model. It agrees in the thermodynamic limit but not node by node near the disk centre.
- **Projectivity and labels.** Projective formulations are not exchangeable, so they cannot be graphon models. Sparse exchangeable infinite graphs do not exist (Aldous–Hoover; see [Hidden variables and graphons](./07-hidden-variables-and-graphons.md)). LSMs give up infinite exchangeability by design.
- **Is the latent space real?** That the generative model fits does not identify the geometry.
  - Krioukov argues that strong clustering *implies* a latent geometry under weak conditions: [](doi:10.1103/PhysRevLett.116.208302) (*PRL* 116, 208302, 2016).
  - Inferring coordinates (HyperMap; Mercator, [](doi:10.1088/1367-2630/ab57d2), *New J. Phys.* 21, 2019; Hoff et al.'s MCMC) is a separate, non-convex estimation problem that the notes do not cover.
- **What the model leaves out.** Communities appear only as angular inhomogeneities in $\rho(\theta)$, and degree correlations are fixed by $\beta$ and $\gamma$. Weighted, directed and temporal extensions exist but are outside the chapter.

## Connections

- **NETS 5116.**
  - ER is the $\beta\to0$, $\gamma\to\infty$ corner of the model square ([Barabási ch. 3](../nets-5116/barabasi/03-random-networks.md)), and the RHG is a geometric origin for the power laws of [Barabási ch. 4](../nets-5116/barabasi/04-scale-free-networks.md).
  - Popularity × similarity explains preferential attachment ([Barabási ch. 5](../nets-5116/barabasi/05-barabasi-albert-model.md)) as greedy optimisation in hyperbolic space.
  - The high clustering of real networks this model reproduces is catalogued in [Newman ch. 10](../nets-5116/newman/10-structure-of-real-world-networks.md).
  - Greedy routing on the inferred coordinates (Boguñá, Krioukov & Claffy, [](doi:10.1038/nphys1130), *Nat. Phys.* 5, 2009; Internet mapping, [](doi:10.1038/ncomms1063), *Nat. Commun.* 1, 2010) is the geometric answer to network navigation.
- **NETS 6116.**
  - The Fermi–Dirac / ERGM correspondence and the graphon representation come from [Hidden variables and graphons](./07-hidden-variables-and-graphons.md).
  - $\beta\to0$ recovers the HSCM of [Configuration models](./05-configuration-models.md).
  - The clustering and small-world thresholds are the model answer to [Clustering and assortativity](./02-clustering-and-assortativity.md) and [Sparsity and small worlds](./01-sparsity-and-small-worlds.md).
  - The DC-SBM in [Stochastic block models](./09-stochastic-block-models.md) is the only other maximum-entropy model with the same projective-but-not-exchangeable signature.
  - The dk-series ([dk-series](./06-dk-series.md)) shows how much clustering is left unexplained by degree correlations alone.
- **PHYS 7335.**
  - Strong clustering and geometry break the tree-like assumptions of [heterogeneous mean-field](../phys-7335/05-heterogeneous-mean-field.md) and [SIR percolation](../phys-7335/07-sir-percolation.md); [quenched mean-field](../phys-7335/06-quenched-mean-field.md) still applies.
  - Spatial embedding is also the premise of [metapopulation models](../phys-7335/09-metapopulation-models.md).
- **NETS 7332.**
  - Hoff et al.'s latent-space model is the statistical ancestor of the **distance-based decoders** in [shallow embeddings](../nets-7332/basics/03-shallow-embeddings.md). Hyperbolic embeddings and hyperbolic GNNs (HGCN) exploit the same fact: trees and scale-free graphs embed with low distortion in $\mathbb{H}^2$.
  - The *spatial dependency* of [Representations](../nets-7332/readings/01-representations.md) is exactly an LSM assumption.

## Self-test

:::{dropdown} Q1. Why does the same condition, β > 1, give both projectivity and non-vanishing clustering?
Both come from integrability of $p(x)\sim x^{-\beta}$.

- If $\int_0^\infty p<\infty$, then $\langle k\rangle = 2\int p$ is finite with $p$ independent of $N$, so the model can be grown node by node without changing old edges.
- In the same regime typical edges have length $O(1)$, so a node's neighbours are close to each other and the triangle inequality produces triangles.

For $\beta<1$, keeping $\langle k\rangle$ fixed forces $c_N\to0$ (non-projective), and edges have length $\sim N$ (no geometry, no clustering).
:::

:::{dropdown} Q2. Derive μ in the S¹ model.
$\bar k(\kappa) = 2\mu\kappa\langle k\rangle\int_0^\infty\frac{dt}{1+t^\beta} = 2\mu\kappa\langle k\rangle\frac{\pi/\beta}{\sin(\pi/\beta)}$. Setting this to $\kappa$ gives $\mu = \beta\sin(\pi/\beta)/(2\pi\langle k\rangle)$. This needs $\beta>1$ and $N\gg\mu\kappa\kappa'$; it is valid for any $\rho(\kappa)$ with finite mean.
:::

:::{dropdown} Q3. What is the clustering of the 1D sharp RGG, and why?
$3/4$. Two neighbours are i.i.d. uniform in $(-r_c,r_c)$ and are linked iff within $r_c$ of each other. The excluded region is $1/4$ of the square.
:::

:::{dropdown} Q4. Map the S¹ model to H². What radial density gives γ = 3?
Set $r = R - 2\ln(\kappa/\kappa_0)$ and $R = 2\ln(N/(\pi\mu\kappa_0^2))$. Then $p = 1/(1+e^{\frac\beta2(d-R)})$ with $d = r+r'+2\ln(\theta/2)\approx d_{\mathbb H}$.

Pareto $\gamma$ maps to $\rho(r)\propto e^{\alpha(r-R)}$ with $\alpha=(\gamma-1)/2$. So $\gamma=3$ means $\alpha=1$: points uniform in the hyperbolic disk.
:::

:::{dropdown} Q5. Give the phase diagram of the ultrasparse SRGG in β, and the statistical-physics meaning of β and μ_ch.
- $\beta<1$: small world, no clustering (ER-like).
- $1<\beta<2$: clustered small world.
- $\beta>2$: clustered large world, with the RGG at $\beta=\infty$.

With the coordinates frozen the model is an ERGM. $\beta$ is the inverse temperature, conjugate to the total log edge length. $\mu_{\mathrm{ch}}$ is the chemical potential, conjugate to the edge count (it fixes $\langle k\rangle$).
:::

:::{dropdown} Q6. Why is the 1D RGG built by sprinkling N uniform points on [0, N] unsatisfactory as a model of an infinite network, and what fixes it?
The point process is binomial, so counts in disjoint intervals are dependent. The model is finitely exchangeable but sparse, so by Aldous–Hoover it has no infinite exchangeable limit.

Growing the graph with i.i.d. $\mathrm{Exp}(1)$ spacings gives a rate-1 Poisson process on $\mathbb{R}^+$ and a projective model. Labels are ordered by position, which costs exchangeability but nothing else.
:::

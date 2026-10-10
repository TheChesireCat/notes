---
title: Label Propagation and Collective Classification
short_title: Label propagation
subject: NETS 7332 · Basics
description: How to classify the unlabelled nodes of a graph by exploiting label correlations along edges, from relational and iterative classifiers to harmonic label propagation, Correct & Smooth and loopy belief propagation.
tags: [node-classification, semi-supervised, label-propagation, homophily, collective-classification, belief-propagation]
---

:::{tip} TL;DR
- **Collective classification** labels all unlabelled nodes *jointly*. It relies on the **first-order Markov assumption** $P(Y_v \mid \text{everything}) = P(Y_v \mid \mathcal{N}(v))$ and on label correlation along edges, which comes from **homophily**, **influence**, or both. Observational data cannot generically tell those two apart.
- **Label propagation is a quadratic smoothness problem.** Clamped labels give the **harmonic solution** $f_U = (D_{UU} - A_{UU})^{-1} A_{UL} f_L$. Each unlabelled score is the average of its neighbours' scores, which equals the probability that a random walk started there is absorbed at a labelled node of that class. Soft labels give the **Zhou et al. closed form** $F^* = (1-\alpha)(I - \alpha S)^{-1} Y$ with $S = D^{-1/2} A D^{-1/2}$. The iteration $F \leftarrow \alpha S F + (1-\alpha) Y$ converges for any $\alpha \in (0,1)$ because $\operatorname{spec}(S) \subseteq [-1, 1]$.
- Both are **low-pass filters** on the graph spectrum. They work when the edge homophily ratio $h$ is high and *systematically fail* under heterophily ($h \to 0$), where label signals live at high graph frequencies.
- **Relational** and **iterative classification** are the classical heuristics. The relational classifier averages neighbours' class probabilities without features. Iterative classification trains $\phi_1(x_v)$ and $\phi_2(x_v, z_v)$, where $z_v$ summarises the neighbours' labels. Neither has a general convergence guarantee.
- **Correct & Smooth (C&S)** is the modern form. Fit a feature-only base predictor, then *propagate its training residuals* to correct correlated errors, then *propagate the corrected predictions*. On OGB-Products this lifts an MLP from 63.4% to 84.2% accuracy without training a GNN.
:::

- **Source.** Leskovec, *CS224W* (Fall 2021), lecture 5 "Label Propagation for Node Classification" ([slides](https://snap.stanford.edu/class/cs224w-2021/slides/05-message.pdf)). Zhu, Ghahramani & Lafferty, *ICML* 2003 ([pdf](https://mlg.eng.cam.ac.uk/zoubin/papers/zgl.pdf)). Zhou, Bousquet, Lal, Weston & Schölkopf, *NeurIPS* 16, 2004 ([pdf](https://proceedings.neurips.cc/paper_files/paper/2003/file/87682805257e619d49b8e0dfdc14affa-Paper.pdf)). Correct & Smooth: [](doi:10.48550/arXiv.2010.13993). Collective-classification survey: [](doi:10.1609/aimag.v29i3.2157). Macskassy & Provost, *JMLR* 8, 2007 ([pdf](https://www.jmlr.org/papers/volume8/macskassy07a/macskassy07a.pdf)).
- **Builds on.** The graph Laplacian ([Newman ch. 6 notes](../../nets-5116/newman/06-mathematics-of-networks.md)); random walks and personalised PageRank ([link analysis](./02-link-analysis.md)).
- **Notation.** Shared symbols as in [](#notation). The graph is undirected and possibly weighted, so $A = A^\top$ and $k_i = \sum_j A_{ij}$. Other symbols on this page:
  - $c$: the number of classes.
  - $\mathcal{V}_L$, $\mathcal{V}_U$: labelled and unlabelled nodes. Blocks of a matrix are written $A_{UL}$, $D_{UU}$, and so on.
  - $Y \in \{0,1\}^{N \times c}$: one-hot labels, with zero rows for $v \in \mathcal{V}_U$.
  - $F \in \mathbb{R}^{N \times c}$: soft label scores. In the binary case, $f$ is the score of class 1.
  - $P = D^{-1} A$: the random-walk transition matrix.
  - $S = D^{-1/2} A D^{-1/2}$: the symmetrically normalised adjacency.
  - $x_v$: the feature vector of node $v$.

(sec-lp-setup)=
## Setup and definitions

:::{prf:definition} Semi-supervised (transductive) node classification
:label: def-lp-task

We are given a graph $G$, possibly node features $X$, and the labels $Y_v$ of a subset $\mathcal{V}_L$ of nodes. The task is to predict the labels of $\mathcal{V}_U = V \setminus \mathcal{V}_L$. The setting is *transductive*: the unlabelled nodes, and their edges, are visible at training time.
:::

:::{prf:definition} Homophily, influence and the edge homophily ratio
:label: def-lp-homophily

Labels are correlated along edges for two classical reasons:
- **Homophily**: similar nodes tend to link. Ties form *because of* the attribute.
- **Influence** (contagion): linked nodes become similar. The attribute changes *because of* the tie.

A common scalar summary is the **edge homophily ratio** of Zhu et al. (2020) [](doi:10.48550/arXiv.2006.11468):

$$
h = \frac{\lvert \{ (u,v) \in E : Y_u = Y_v \} \rvert}{\lvert E \rvert},
$$ (eq-lp-h)

the fraction of intra-class edges. Strong homophily means $h \to 1$, and strong heterophily means $h \to 0$.
:::

:::{prf:definition} Collective classification and the first-order Markov assumption
:label: def-lp-markov

**Collective classification** assigns labels to all of $\mathcal{V}_U$ jointly, letting predicted labels inform one another. It is usually made tractable by the **first-order Markov assumption** (Macskassy & Provost 2007):

$$
P\!\left(Y_v \mid G \setminus v\right) = P\!\left(Y_v \mid \mathcal{N}(v)\right).
$$ (eq-lp-markov)

A node's label depends on the rest of the network only through its neighbours: their labels, and possibly their features.
:::

In general, a node's label may depend on three things: its own features, its neighbours' labels, and its neighbours' features. The methods below differ in which of these they use and in how they resolve the circularity: neighbours' labels are themselves unknown.

## Core ideas

(sec-lp-why)=
### Why labels correlate, and why that is not causal

Homophily and influence both produce $h$ above its baseline, and label propagation exploits either one. The *direction* of causation is irrelevant for prediction. It matters, though, the moment the predictions are read causally. Shalizi & Thomas show that in observational network data, homophily, contagion and covariate effects are **generically confounded**: telling them apart requires strong parametric or covariate-adequacy assumptions [](doi:10.1177/0049124111404820).

A raw $h$ also ignores chance. With class sizes, measured by edge ends, $a_r$, a random graph has $h \approx \sum_r a_r^2$. Newman's modularity of the class partition, $Q = \sum_r (e_{rr} - a_r^2)$, is precisely $h$ minus that baseline. ($e_{rr}$ is the fraction of edges joining two class-$r$ nodes, so $h = \sum_r e_{rr}$.)

(sec-lp-relational)=
### Relational classifier: neighbour averaging without features

This is the weighted-vote relational neighbour (wvRN) classifier of Macskassy & Provost, run with relaxation labelling, as presented in CS224W.
- **Initialise.** Labelled nodes get their true class probabilities. Unlabelled nodes start uniform ($P(Y_v = 1) = 0.5$ in the binary case), or at the class prior.
- **Update.** Visit the unlabelled nodes (in random order in CS224W), and set, for each class $c'$,

$$
P(Y_v = c') = \frac{1}{\sum_{u} A_{vu}} \sum_{u} A_{vu}\, P(Y_u = c').
$$ (eq-lp-wvrn)

- **Stop** at convergence or after a maximum number of iterations.

CS224W lists two weaknesses: **convergence is not guaranteed**, and **features are not used**.

*My comment.* For the version above, with labelled nodes clamped on an undirected graph, {eq}`eq-lp-wvrn` is exactly a Gauss–Seidel sweep for the harmonic equations {eq}`eq-lp-harmonic`. It therefore *does* converge whenever every connected component of the graph contains a labelled node: $\rho(P_{UU}) < 1$ makes the linear iteration contractive. Macskassy & Provost likewise note that the Zhu et al. harmonic solution is "essentially identical" to wvRN, but with exact inference. The non-convergence warning applies to the general family: directed or unclamped variants, and nonlinear local classifiers as in ICA below.

(sec-lp-ica)=
### Iterative classification (ICA)

Iterative classification brings features back in by training two classifiers on the labelled nodes:
- **Base classifier** $\phi_1(x_v)$: predicts $Y_v$ from $v$'s own features.
- **Relational classifier** $\phi_2(x_v, z_v)$: predicts $Y_v$ from $x_v$ plus a fixed-length **summary $z_v$ of neighbour labels**. Options for $z_v$ include a histogram (counts or fractions) of each label in $\mathcal{N}(v)$, the most common label, or the number of distinct labels. In directed graphs one can use separate incoming and outgoing summaries.

It then runs in two phases:
1. **Bootstrap.** Label $\mathcal{V}_U$ with $\phi_1$.
2. **Iterate.** For each $v \in \mathcal{V}_U$, recompute $z_v$ from the current labels of $\mathcal{N}(v)$, then relabel $v$ with $\phi_2$. Repeat until the labels stabilise or a maximum number of iterations is reached.

$\phi_2$ is trained using *true* neighbour labels on the training set, but at test time it runs on *predicted* ones. *My comment:* this train–test mismatch, together with the nonlinearity of $\phi_2$, is why nothing makes the iteration a contraction. As with the relational classifier, convergence is not guaranteed. ICA, together with Gibbs sampling, loopy belief propagation and mean-field relaxation labelling, are the four inference algorithms compared in the collective-classification survey of Sen et al.

(sec-lp-lp)=
### Label propagation as optimisation

Both classical label-propagation methods minimise a **smoothness + fit** objective over soft labels. They differ in how hard the fit is enforced.

| | Harmonic functions (Zhu, Ghahramani & Lafferty 2003) | Local and global consistency (Zhou et al. 2004) |
|---|---|---|
| Objective | $\tfrac12 \sum_{ij} A_{ij} (f_i - f_j)^2 = f^\top \mathcal{L} f$, subject to $f_L = Y_L$ (hard clamp) | $\tfrac12 \sum_{ij} A_{ij} \big\lVert F_i/\sqrt{k_i} - F_j/\sqrt{k_j} \big\rVert^2 + \mu \sum_i \lVert F_i - Y_i \rVert^2$ |
| Operator | random walk $P = D^{-1}A$, combinatorial Laplacian | normalised $S = D^{-1/2} A D^{-1/2}$, normalised Laplacian $I - S$ |
| Labelled nodes | fixed exactly | may drift; labelled and unlabelled rows are both fitted to $Y$ |
| Solution | $f_U = (D_{UU} - A_{UU})^{-1} A_{UL} Y_L$ | $F^* = (1-\alpha)(I - \alpha S)^{-1} Y$, with $\alpha = 1/(1+\mu)$ |
| Iteration | $f_U \leftarrow P_{UU} f_U + P_{UL} Y_L$ | $F \leftarrow \alpha S F + (1-\alpha) Y$ |
| Interpretation | absorption probabilities of a random walk; electric-network potentials | a diffusion kernel; personalised-PageRank-like ([below](#prop-lp-ppr)) |

In both, the predicted class is $\arg\max_{c'} F_{vc'}$. Zhu et al. also propose **class mass normalisation**, which rescales the columns of $F$ to match the class priors, to counter imbalance.

(sec-lp-cs)=
### Correct & Smooth

Huang et al. (2021) show that the label-propagation ideas above, bolted onto a *graph-free* model, match or beat GNNs on transductive benchmarks. The graph is used only in post-processing, and nothing is trained end to end.

1. **Base predictor.** Train a linear model or shallow MLP $f(x_v)$ with cross-entropy on the training nodes $\mathcal{L}_t$. This gives soft predictions $Z \in \mathbb{R}^{N \times c}$, whose rows are softmax outputs.
2. **Correct.** The premise is that base-predictor errors are *positively correlated along edges*.
   - Form the residual matrix $E$: $E_{\mathcal{L}_t} = Y_{\mathcal{L}_t} - Z_{\mathcal{L}_t}$, with zero rows elsewhere. The sign is ground truth minus prediction, as in the CS224W slides and the reference code. Equation (1) of arXiv v2 prints it reversed while still *adding* $\hat E$.
   - Smooth $E$ with the Zhou et al. iteration $E^{(t+1)} = (1-\alpha) E + \alpha S E^{(t)}$. This solves $\min_W \operatorname{tr}\!\big(W^\top (I - S) W\big) + \mu \lVert W - E \rVert_F^2$.
   - Propagation shrinks the residual mass, since $\lVert E^{(t)} \rVert_2 \le \lVert E \rVert_2$, so $\hat E$ is rescaled before it is added. **Autoscale** sets each unlabelled row to $Z_i + \sigma\, \hat E_i / \lVert \hat E_i \rVert_1$, with $\sigma$ the mean $\ell_1$ training residual. **FDiff-scale** instead diffuses with training errors clamped (a harmonic-style $D^{-1}A$ iteration) and adds $s \hat E$ with a tuned $s$.
3. **Smooth.**
   - Set $G = Z^{(r)}$, then reset the training rows to $Y$. Validation labels may be reset too, which helps further.
   - Iterate $G^{(t+1)} = (1-\alpha) G + \alpha S G^{(t)}$.
   - Predict $\arg\max_{c'} \hat Y_{vc'}$. The scores are not probabilities.

On OGB-Products (Huang et al. Table 2), the MLP base predictor reaches **63.41%**. Adding C&S raises it to **84.18%** (FDiff-scale), above both plain label propagation (74.76%) and a plain GCN (75.64%). CS224W reports 80.34% for smoothing alone, so the correct step adds about 4 points.

(sec-lp-bp)=
### Loopy belief propagation

The probabilistic version of collective classification models labels as a **pairwise Markov random field**:

$$
P(y \mid x) = \frac{1}{Z(x)} \prod_{i} \phi_i(y_i) \prod_{(i,j) \in E} \psi_{ij}(y_i, y_j).
$$ (eq-lp-mrf)

- The node potential $\phi_i$ absorbs evidence from $i$'s own features and from observed neighbours.
- The edge potential $\psi_{ij}$ encodes label compatibility. A homophilous $\psi$ favours $y_i = y_j$; a heterophilous one need not.

The marginals are intractable in general. **Loopy belief propagation (LBP)** passes normalised messages until they stabilise, then reads off beliefs (Sen et al., Algorithm 3):

$$
m_{i \to j}(y_j) \propto \sum_{y_i} \psi_{ij}(y_i, y_j)\, \phi_i(y_i) \prod_{k \in \mathcal{N}(i) \setminus j} m_{k \to i}(y_i),
\qquad
b_i(y_i) \propto \phi_i(y_i) \prod_{j \in \mathcal{N}(i)} m_{j \to i}(y_i).
$$ (eq-lp-bp)

- On a **tree** these are Pearl's sum-product equations and the beliefs are the exact marginals.
- On a **loopy** graph LBP may fail to converge. When it does converge, the beliefs are only approximate: Yedidia, Freeman & Weiss showed that LBP fixed points are stationary points of the Bethe free energy, a variational approximation (as summarised by Sen et al.).
- Excluding the recipient $j$ from the product is what distinguishes message passing from naive averaging. Learned GNN message passing keeps the "aggregate over neighbours" skeleton but replaces the products and sums with learned functions ([message-passing GNNs](./05-message-passing-gnns.md)).

(sec-lp-results)=
## Key results

:::{prf:theorem} Harmonic solution (Zhu, Ghahramani & Lafferty 2003)
:label: thm-lp-harmonic

Assume every connected component of $G$ contains a labelled node. Then the minimiser of $\tfrac12 \sum_{ij} A_{ij}(f_i - f_j)^2$ subject to $f_L = Y_L$ is unique and satisfies

$$
f_U = (D_{UU} - A_{UU})^{-1} A_{UL}\, f_L = (I - P_{UU})^{-1} P_{UL}\, f_L .
$$ (eq-lp-harmonic)

Equivalently, $f$ is **harmonic** on $\mathcal{V}_U$: $f_v = \frac{1}{k_v} \sum_u A_{vu} f_u$. For a binary 0/1 labelling, $f_v$ is the probability that a random walk started at $v$ is absorbed at a class-1 labelled node, with the labelled nodes acting as an absorbing boundary. By the maximum principle, $0 \le f_v \le 1$.
:::

:::{dropdown} Derivation
- Write $E(f) = f^\top \mathcal{L} f$ with $\mathcal{L} = D - A$. Fix $f_L$ and set $\partial E / \partial f_U = 2(\mathcal{L} f)_U = 0$. This gives $(D_{UU} - A_{UU}) f_U - A_{UL} f_L = 0$.
- $D_{UU} - A_{UU}$ is weakly diagonally dominant. In each component it is strictly dominant in at least one row, namely a node adjacent to a labelled node, and the component is irreducible. So the matrix is nonsingular, and it is positive definite. This gives uniqueness and {eq}`eq-lp-harmonic`.
- Equivalently, $P_{UU}$ is substochastic with spectral radius $\rho(P_{UU}) < 1$. Then $(I - P_{UU})^{-1} = \sum_t P_{UU}^t$, and $[P_{UU}^t P_{UL}]_{vl}$ is the probability that the walk from $v$ first hits labelled node $l$ at step $t+1$. Summing over $t$ gives absorption probabilities.
- Jacobi or Gauss–Seidel sweeps of $f_U \leftarrow P_{UU} f_U + P_{UL} f_L$ contract at rate $\rho(P_{UU})$. This is why the clamped relational classifier converges.
:::

:::{prf:theorem} Local and global consistency (Zhou et al. 2004)
:label: thm-lp-lgc

For $\alpha \in (0,1)$, the iteration $F^{(t+1)} = \alpha S F^{(t)} + (1-\alpha) Y$ converges from any $F^{(0)}$ to

$$
F^* = (1-\alpha)(I - \alpha S)^{-1} Y = (1-\alpha) \sum_{t \ge 0} \alpha^t S^t Y,
$$ (eq-lp-lgc)

which is the unique minimiser of $\operatorname{tr}\!\big(F^\top (I - S) F\big) + \mu \lVert F - Y \rVert_F^2$, with $\alpha = 1/(1+\mu)$.
:::

:::{dropdown} Derivation
- **Spectrum.** $S = D^{-1/2} A D^{-1/2}$ is similar to the stochastic matrix $P = D^{-1} A$, so $\operatorname{spec}(S) \subseteq [-1, 1]$. Its top eigenvector is $D^{1/2}\mathbf 1$, with eigenvalue 1.
- **Iteration.** Hence $\rho(\alpha S) = \alpha < 1$. Unrolling, $F^{(t)} = (\alpha S)^t F^{(0)} + (1-\alpha) \sum_{i<t} (\alpha S)^i Y$. The first term vanishes and the Neumann series converges to $(I - \alpha S)^{-1}$.
- **Objective.** The quadratic form $\tfrac12 \sum_{ij} A_{ij} \lVert F_i/\sqrt{k_i} - F_j/\sqrt{k_j} \rVert^2$ equals $\operatorname{tr}(F^\top (I - S) F)$. Setting the gradient to zero gives $2(I - S) F + 2\mu (F - Y) = 0$, i.e. $(I - \tfrac{1}{1+\mu} S) F = \tfrac{\mu}{1+\mu} Y$, which is {eq}`eq-lp-lgc`.
- **Uniqueness.** $I - \alpha S$ is positive definite, so the minimiser is unique.
:::

:::{prf:proposition} Label propagation is a low-pass filter
:label: prop-lp-lowpass

Let $S = \sum_m \lambda_m u_m u_m^\top$. Then

$$
F^* = \sum_m \frac{1-\alpha}{1 - \alpha \lambda_m}\, u_m u_m^\top Y .
$$ (eq-lp-filter)

Each spectral component of $Y$ is scaled by $g(\lambda) = (1-\alpha)/(1-\alpha\lambda)$. This gain is increasing in $\lambda$. It equals $1$ at $\lambda = 1$, the smooth, low-frequency end, and $(1-\alpha)/(1+\alpha)$ at $\lambda = -1$, the oscillating, high-frequency end.
:::

:::{dropdown} Consequences (my derivation; the heterophily statement follows Zhu et al. 2020)
- Substituting the eigendecomposition into {eq}`eq-lp-lgc` gives {eq}`eq-lp-filter` directly.
- **As $\alpha \to 1$**, $g$ concentrates on $\lambda = 1$, so $F^*$ tends to a multiple of $D^{1/2}\mathbf 1$ in every column. The scores flatten toward a degree-weighted constant and the class margins vanish. The worked example below shows this at $\alpha = 0.99$.
- **Heterophily.** Zhu et al. (2020, Theorem 3) prove that a label signal with a lower edge homophily ratio has more energy in the high-frequency part of the Laplacian spectrum. A low-pass filter suppresses exactly that part. So harmonic or LGC propagation degrades as $h$ falls, and on a bipartite-like labelling it predicts the *opposite* class.
- **Example.** On the path $1 - 2 - 3$, label nodes 1 and 3 as A while node 2 is truly B. Then $h = 0$, and the harmonic score of node 2 is the average of its neighbours: certainly A.
:::

:::{prf:proposition} Label propagation and personalised PageRank
:label: prop-lp-ppr

Zhou et al.'s variant $F^* = (I - \alpha P^\top)^{-1} Y$ has, for undirected $A$, $P^\top = A D^{-1}$. That is the column-stochastic walk matrix in our $A_{ij} = $ ($j \to i$) convention. Column $c'$ of $(1-\alpha) F^*$ is therefore the personalised PageRank vector with restart probability $1-\alpha$ and teleport distribution the (unnormalised) indicator of class-$c'$ labelled nodes. Since $(I - \alpha A D^{-1})^{-1} = D (D - \alpha A)^{-1}$, this differs from $(D - \alpha A)^{-1} Y$ only by a positive per-row factor. The $\arg\max$ is therefore the same, which is the "equivalence" Zhou et al. state.
:::

## Worked example

Take two "diamonds" joined by a bridge. All values below were computed numerically and checked against the closed forms.
- **Community A** is $\{1,2,3,4\}$, with edges $1{-}2$, $1{-}3$, $2{-}3$, $2{-}4$, $3{-}4$.
- **Community B** is $\{5,6,7,8\}$, with edges $5{-}6$, $5{-}7$, $6{-}7$, $6{-}8$, $7{-}8$.
- The **bridge** is $4{-}5$.

This gives $N = 8$ and $L = 11$, with degrees $(2,3,3,3,3,3,3,2)$. Node 1 is labelled A and node 8 is labelled B. The true classes follow the communities.

**Homophily.** 10 of the 11 edges are intra-class, so $h = 10/11 \approx 0.909$. Each class holds half the edge ends ($a_A = a_B = 11/22$), so the chance baseline is $0.5$ and $Q = 0.909 - 0.5 \approx 0.409$.

**Label propagation scores.** The table gives the score $P(A)$ for each node under each method. The relational classifier starts unlabelled nodes at 0.5 and sweeps in order $2, \dots, 7$. For LGC (Zhou et al.), the score is the class-A share $F_{vA}/(F_{vA}+F_{vB})$.

| Node | Relational, sweep 1 | Relational, sweep 2 | Harmonic {eq}`eq-lp-harmonic` | LGC $\alpha=0.5$ | LGC $\alpha=0.9$ | LGC $\alpha=0.99$ |
|---|---|---|---|---|---|---|
| 1 (label A) | 1 | 1 | 1 | 0.999 | 0.876 | 0.574 |
| 2 | 0.667 | 0.784 | $5/6 = 0.833$ | 0.986 | 0.796 | 0.551 |
| 3 | 0.722 | 0.805 | $5/6 = 0.833$ | 0.986 | 0.796 | 0.551 |
| 4 | 0.630 | 0.711 | $2/3 = 0.667$ | 0.847 | 0.660 | 0.526 |
| 5 | 0.543 | 0.452 | $1/3 = 0.333$ | 0.153 | 0.340 | 0.474 |
| 6 | 0.348 | 0.250 | $1/6 = 0.167$ | 0.014 | 0.204 | 0.449 |
| 7 | 0.297 | 0.234 | $1/6 = 0.167$ | 0.014 | 0.204 | 0.449 |
| 8 (label B) | 0 | 0 | 0 | 0.001 | 0.124 | 0.426 |

- **The relational classifier reaches the harmonic solution.** Its Gauss–Seidel sweeps converge to the harmonic column, to within $10^{-4}$, after 17 sweeps. Here $\rho(P_{UU}) = 0.805$. Check node 4: $(5/6 + 5/6 + 1/3)/3 = 2/3$.
- **LGC does not clamp labels.** Node 1 itself drifts from 1 to 0.876 at $\alpha = 0.9$.
- **Large $\alpha$ flattens the scores** toward the stationary profile, as {prf:ref}`prop-lp-lowpass` predicts. The eigenvalues of $S$ here are $\{-0.715, -0.539, -0.333, -0.333, -0.175, 0.206, 0.890, 1\}$. At $\alpha = 0.99$ every margin is below $0.08$, although the $\arg\max$ is still correct.

**Correct & Smooth on the same graph.** Now use training nodes $\{1, 3, 8\}$. The feature-only base predictor's errors cluster on the A side of the bridge: it gives node 3 (a training node) $P(A) = 0.40$, and it misclassifies node 4.
- **Base predictions.** $Z_A$ for nodes 1 to 8 is $(0.80, 0.55, 0.40, 0.35, 0.45, 0.30, 0.30, 0.20)$.
- **Residuals.** The training residuals $Y - Z$ in the A column are $+0.20$ (node 1), $+0.60$ (node 3) and $-0.20$ (node 8). The B column is the negative of these.
- **Settings.** $\alpha = 0.8$ in both steps, with Autoscale ($\sigma = 2/3$).

| Unlabelled node | Truth | Base $Z_A$ | Propagated residual $\hat E_A$ | Corrected $Z^{(r)}_A$ | Final $(\hat Y_A, \hat Y_B)$ | Class |
|---|---|---|---|---|---|---|
| 2 | A | 0.55 | $+0.150$ | 0.883 | (0.847, 0.190) | A ✓ |
| 4 | A | **0.35 ✗** | $+0.111$ | 0.683 | (0.719, 0.308) | A ✓ |
| 5 | B | 0.45 | $+0.022$ | **0.783 ✗** | (0.470, 0.557) | B ✓ |
| 6, 7 | B | 0.30 | $-0.014$ | $-0.033$ | (0.228, 0.809) | B ✓ |

- **The correct step fixes node 4.** The large residual at its neighbour, node 3, propagates to it.
- **Autoscale over-corrects node 5.** It rescales *every* unlabelled row to the same $\ell_1$ size $\sigma$, so node 5's tiny $+0.022$ residual becomes a full-sized push toward A.
- **The smooth step repairs node 5** using its B neighbours. The two steps are complementary.
- **On a graph this small, smoothing alone also gets every node right**: node 4 ends at $0.559$ vs $0.467$. The correct step's advantage is a large-graph effect (63.4% → 80.3% smooth-only → 84.2% with C&S on Products).

## Assumptions and limitations

- **Homophily is assumed.** Every method here pushes neighbours' labels together. Under heterophily they are not merely weak but biased toward the wrong answer ({prf:ref}`prop-lp-lowpass`). Heterophily-aware GNN designs, such as separating ego and neighbour embeddings and using higher-order neighbourhoods, are the subject of Zhu et al. (2020).
- **No features (classical LP).** Harmonic and LGC propagation use labels and structure only. ICA and C&S add features, but only through separately trained, non-graph models.
- **Transductive.** Every unlabelled node must be in the graph at inference time, and a new node requires re-propagation.
- **Convergence.** Linear propagations ({prf:ref}`thm-lp-harmonic`, {prf:ref}`thm-lp-lgc`) converge provably. ICA, generic relaxation labelling and loopy BP do not, and their outputs can depend on the update order.
- **Calibration.** C&S and LGC scores are not probabilities: they need not sum to 1 and can be negative.
- **Causal reading.** High $h$ licenses prediction, not a story about why. Homophily and contagion are confounded ([](#sec-lp-why)).

## Connections

- **NETS 5116.**
  - The edge homophily ratio is $\sum_r e_{rr}$ in Newman's mixing-matrix notation. The modularity of the label partition, $\sum_r (e_{rr} - a_r^2)$, is its chance-corrected version ([Newman ch. 7 notes](../../nets-5116/newman/07-measures-and-metrics.md)).
  - $I - S$ is the normalised Laplacian ([Newman ch. 6 notes](../../nets-5116/newman/06-mathematics-of-networks.md)).
- **NETS 6116.** A homophilous labelling is an *assortative* block structure. Label propagation is a low-pass filter, so it is effective precisely in the assortative regime of a stochastic block model.
- **PHYS 7335.** The harmonic solution is a hitting probability for the random walk with labelled nodes as absorbing states. The same first-passage machinery appears in random walks on networks.
- **NETS 7332.**
  - Park & Barabási's dyadicity and heterophilicity ([reading 02](../readings/02-node-characteristics.md)) are chance-corrected edge counts of the same kind as $h$.
  - Higher-order homophily ([reading 03](../readings/03-higher-order-homophily.md)) generalises $h$ to group interactions.
  - LGC is personalised PageRank with class-indicator teleports ([link analysis](./02-link-analysis.md)).
  - C&S's smoothing resembles APPNP and the GCN propagation $\hat A$ ([message-passing GNNs](./05-message-passing-gnns.md)). The differences: C&S propagates softmax outputs and labels, after training, without learning.

## Self-test

:::{dropdown} Q1. State the first-order Markov assumption of collective classification. Which method uses it most literally?
$P(Y_v \mid G \setminus v) = P(Y_v \mid \mathcal{N}(v))$: a label depends on the rest of the network only through its neighbourhood. The relational classifier (wvRN) uses it most literally, since it sets $P(Y_v)$ to the weighted average of its neighbours' class probabilities.
:::

:::{dropdown} Q2. Derive the harmonic solution. When is it unique?
- Minimise $f^\top \mathcal{L} f$ with $f_L$ fixed. Setting the gradient in $f_U$ to zero gives $(D_{UU} - A_{UU}) f_U = A_{UL} f_L$.
- The solution is unique iff every connected component contains a labelled node. Then $D_{UU} - A_{UU}$ is nonsingular, and equivalently $\rho(P_{UU}) < 1$.
- Each $f_v$ is the average of its neighbours' values, and equals the probability that a random walk from $v$ is absorbed at a class-1 label.
:::

:::{dropdown} Q3. Why does $F \leftarrow \alpha S F + (1-\alpha) Y$ converge, and what does it converge to?
- $S$ is similar to the stochastic matrix $D^{-1}A$, so $\operatorname{spec}(S) \subseteq [-1, 1]$ and $\rho(\alpha S) = \alpha < 1$.
- The influence of the initial condition decays like $\alpha^t$, and the Neumann series gives $F^* = (1-\alpha)(I - \alpha S)^{-1} Y$.
- This is the minimiser of $\operatorname{tr}(F^\top (I - S) F) + \mu \lVert F - Y \rVert_F^2$, with $\alpha = 1/(1+\mu)$.
:::

:::{dropdown} Q4. Explain spectrally why label propagation fails under heterophily.
$F^* = \sum_m g(\lambda_m)\, u_m u_m^\top Y$, with $g(\lambda) = (1-\alpha)/(1-\alpha\lambda)$ increasing in $\lambda$. It passes smooth components ($\lambda$ near 1) and damps oscillating ones ($\lambda$ near $-1$). A heterophilous labelling has its energy at high frequencies (Zhu et al. 2020, Thm 3), so propagation suppresses the very signal that encodes the labels, and on bipartite-like labellings it predicts the opposite class.
:::

:::{dropdown} Q5. In C&S, what does each of the two propagations assume? Why is the residual rescaled?
- **Correct** assumes the base predictor's *errors* are positively correlated along edges, so it propagates the training residuals $Y - Z$.
- **Smooth** assumes the *labels* are correlated (homophily), so it propagates the corrected scores, with the training labels reset.
- Propagation is a contraction, $\lVert E^{(t)} \rVert_2 \le \lVert E \rVert_2$, so the spread residual has too little total mass to correct unlabelled nodes. It is rescaled by Autoscale ($\sigma$) or by a tuned $s$ (FDiff-scale).
:::

:::{dropdown} Q6. How do iterative classification and the relational classifier differ? Why can ICA fail to converge?
- The relational classifier ignores features and averages neighbour probabilities.
- ICA trains a base classifier $\phi_1(x_v)$ and a relational classifier $\phi_2(x_v, z_v)$, where $z_v$ summarises neighbour labels, e.g. as a label histogram. It bootstraps with $\phi_1$, then iterates $\phi_2$.
- $\phi_2$ is an arbitrary nonlinear map applied to its own predicted labels, which it was not trained on. The iteration is not a contraction and can oscillate.
:::

:::{dropdown} Q7. What do LBP messages compute? When are the resulting beliefs exact?
- $m_{i \to j}(y_j)$ sums over $y_i$ the product of the edge potential, $i$'s node potential and the messages into $i$ from all neighbours *except* $j$.
- Beliefs are $\phi_i(y_i)$ times the incoming messages.
- They are exact marginals on trees. On loopy graphs LBP may not converge, and its fixed points are only Bethe-free-energy stationary points.
:::

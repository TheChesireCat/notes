---
title: Graph ML Tasks and Traditional Features
short_title: Tasks and features
subject: NETS 7332 · Basics
description: The node-, edge- and graph-level prediction tasks, how to split data for them, and the hand-crafted features (graphlet degree vectors, neighbourhood overlap, Katz, graph kernels) that preceded learned representations.
tags: [graph-ml, link-prediction, graphlets, graph-kernels, weisfeiler-lehman, katz]
---

:::{tip} TL;DR
- Graph ML tasks are classified by **what is predicted**: a node, an edge (or node pair), or a whole graph. They are also classified by **what is observed at test time**. In **transductive** problems the whole graph is seen and only labels are split; in **inductive** problems test nodes or graphs are unseen. Graph classification is only meaningful inductively.
- **Link prediction** splits edges twice. *Message* edges are the input structure; *supervision* edges are the targets and must be **removed** from the graph used to compute features or embeddings, or the target leaks into the input.
- The traditional pipeline is hand-crafted features $\phi$ fed to an off-the-shelf model. **Node features:** centralities, clustering, and the **graphlet degree vector** (counts of the orbit positions a node occupies in small induced subgraphs). **Pair features:** common neighbours, Jaccard, Adamic–Adar, resource allocation, and the **Katz index** $S = (I-\beta A)^{-1} - I$, which converges iff $\beta < 1/\Lambda_{\max}$. **Graph features:** graphlet and WL kernels.
- The **Weisfeiler–Lehman subtree kernel** runs $h$ rounds of colour refinement and compares colour histograms. It costs $O(hL)$ per graph. With uniform initial labels it **cannot distinguish any two $d$-regular graphs of equal size**, which is the same ceiling that later bounds message-passing GNNs.
- Local overlap scores are $0$ for pairs at distance $\ge 3$. Global scores (Katz, random-walk measures) are not, but they inherit a strong degree bias.
:::

- **Source.** Stanford CS224W (Fall 2021), lectures [1](https://snap.stanford.edu/class/cs224w-2021/slides/01-intro.pdf), [2](https://snap.stanford.edu/class/cs224w-2021/slides/02-tradition-ml.pdf) and [8](https://snap.stanford.edu/class/cs224w-2021/slides/08-GNN-application.pdf) (data splits); Hamilton, *Graph Representation Learning*, ch. 2 [](doi:10.1007/978-3-031-01588-5); [Shervashidze et al. (2011), JMLR 12](https://www.jmlr.org/papers/v12/shervashidze11a.html); [Shervashidze et al. (2009), AISTATS](https://proceedings.mlr.press/v5/shervashidze09a.html).
- **Builds on.** Centralities and clustering from [Newman ch. 7 notes](../../nets-5116/newman/07-measures-and-metrics.md); they are not re-derived here.
- **Notation.** Shared symbols as in [](#notation). Here $u, v, w$ are nodes. $S(u,v)$ is a pair score; $\phi(\cdot)$ is a feature map; $h$ is the number of WL iterations; $\mathcal{K}(G, G')$ is a graph kernel. $t_u$ is the number of triangles through $u$. Graphs are undirected unless stated, so $A$ is symmetric.

(sec-tasks-setup)=
## Setup and definitions

:::{prf:definition} Prediction tasks on graphs
:label: def-tasks-levels

Given a graph $G=(V,E)$, possibly with node features $X$:
- **Node-level:** predict $y_v$ for $v \in V$. Examples: protein function, user category.
- **Edge-level:** predict $y_{uv}$ for a pair $(u,v)$. The canonical case is **link prediction**: does $(u,v) \in E$, or will it appear?
- **Graph-level:** predict $y_G$ for each graph in a dataset $\{G_1, \dots, G_M\}$. Example: molecular properties.

CS224W also lists **subgraph/community-level** tasks, such as clustering or detecting a fraud ring.
:::

:::{prf:definition} Transductive vs inductive
:label: def-tasks-transductive

- **Transductive.** The dataset is *one* graph, and the full structure is visible in every split. Only labels (or target edges) are partitioned. This applies only to node- and edge-level tasks.
- **Inductive.** Training, validation and test sets are *different* graphs, or the edges between splits are removed. Each split sees only its own structure, and a model must generalise to unseen nodes or graphs. This applies to all three levels. It is the only well-defined setting for graph classification, because test graphs must be unseen.
:::

:::{prf:definition} Message and supervision edges
:label: def-tasks-message-supervision

In link prediction an edge plays two roles: it is part of the input structure, and it can be a prediction target. So $E$ is split **twice**:
1. **Message edges** form the graph on which features, embeddings or GNN messages are computed. **Supervision edges** are only used as labels in the loss, together with sampled non-edges as negatives.
2. Then train/validation/test.

The **transductive** split commonly uses four disjoint edge sets: training message, training supervision, validation and test.
- Training predicts training-supervision edges from training-message edges.
- Validation predicts validation edges from message + supervision edges.
- Test predicts test edges from all of the above.

In the **inductive** split each graph carries its own message/supervision partition.
:::

There are two standard ways to pose link prediction (CS224W lecture 2):
- **Missing at random.** Delete a random subset of edges and recover them.
- **Links over time** ([Liben-Nowell & Kleinberg, 2007](https://doi.org/10.1002/asi.20591)). Observe $G[t_0, t_0']$ and rank non-adjacent pairs by a score. Then compare the top $n$ against the $n = \lvert E_{\text{new}} \rvert$ edges that appear in $G[t_1, t_1']$.

The temporal version is the honest one for most applications: a randomly deleted edge is not a statistical stand-in for a future edge.

## Core ideas

### The traditional pipeline

A feature map $\phi$ sends a node, a pair or a graph to $\mathbb{R}^d$, and a standard model such as logistic regression, a random forest or a kernel SVM is trained on top of it. All the modelling sits in $\phi$, and none of it is learned. Hand-crafted structural features have one property worth noting: they are **inductive by construction**. $\phi$ can be evaluated on any new graph, unlike the shallow embeddings of [the next pages](./03-shallow-embeddings.md).

### Node features

CS224W splits node features into two kinds:
- **Importance-based:** degree and centralities (eigenvector, betweenness, closeness; see [Newman ch. 7 notes](../../nets-5116/newman/07-measures-and-metrics.md)). These are useful for predicting influential nodes.
- **Structure-based:** degree, clustering coefficient, and the **graphlet degree vector**. These are useful for predicting a node's *role*, e.g. protein function.

:::{prf:definition} Graphlets, orbits, graphlet degree vector
:label: def-tasks-gdv

- A **graphlet** is a small, connected, *induced*, non-isomorphic subgraph.
- Within a graphlet, nodes related by an automorphism occupy the same **orbit**: a position that is structurally indistinguishable.
- The **graphlet degree vector** (GDV) of $u$ counts, for each orbit, how many graphlet instances touch $u$ in that orbit.

On 2–5 nodes there are 30 graphlets with **73 orbits**, so the full GDV is a 73-dimensional node signature ([](doi:10.1093/bioinformatics/btl301)).
:::

Up to 3 nodes there are four orbits:
- $o_0$: endpoint of an edge.
- $o_1$: end of an induced 2-path.
- $o_2$: centre of an induced 2-path.
- $o_3$: node of a triangle.

The first entries are familiar statistics. $o_0 = k_u$ and $o_3 = t_u$. Every pair of neighbours is either an open wedge or closed, so $o_2 = \binom{k_u}{2} - t_u$, and hence

$$
C_u = \frac{t_u}{\binom{k_u}{2}} = \frac{o_3}{o_2 + o_3}.
$$ (eq-tasks-clustering-orbits)

The identity is mine, not the sources'. Degree and clustering are therefore *projections* of the GDV, and the GDV is a strict refinement of both.

**Induced matters.** A triangle on $\{u,v,w\}$ contributes to $o_3$ but *not* to $o_1$ or $o_2$, even though it contains three 2-paths as non-induced subgraphs.

### Pair features for link prediction

All of these are unsupervised scores $S(u,v)$. Used alone, they predict by ranking or thresholding, with $\Pr(A_{uv}=1) \propto S(u,v)$. They can also be fed to a classifier as features. The common-neighbour family uses $\mathcal{N}(u) \cap \mathcal{N}(v)$:

| Score | $S(u,v)$ | Idea |
|---|---|---|
| Common neighbours | $\lvert \mathcal{N}(u) \cap \mathcal{N}(v) \rvert = (A^2)_{uv}$ | triadic closure |
| Jaccard | $\dfrac{\lvert \mathcal{N}(u) \cap \mathcal{N}(v) \rvert}{\lvert \mathcal{N}(u) \cup \mathcal{N}(v) \rvert}$ | normalise away degree |
| Adamic–Adar ([](doi:10.1016/S0378-8733(03)00009-1)) | $\displaystyle\sum_{w \in \mathcal{N}(u) \cap \mathcal{N}(v)} \frac{1}{\log k_w}$ | a shared *low-degree* neighbour is more informative |
| Resource allocation ([](doi:10.1140/epjb/e2009-00335-8)) | $\displaystyle\sum_{w \in \mathcal{N}(u) \cap \mathcal{N}(v)} \frac{1}{k_w}$ | $u$ sends one unit of resource split equally among $w$'s neighbours |
| Preferential attachment ([Liben-Nowell & Kleinberg, 2007](https://doi.org/10.1002/asi.20591)) | $k_u k_v$ | rich-get-richer; needs no shared neighbour |
| Katz ([](doi:10.1007/BF02289026)) | $\displaystyle\sum_{\ell \ge 1} \beta^\ell (A^\ell)_{uv}$ | all walks, discounted by length |

- **AA vs RA.** Adamic–Adar is never undefined: a common neighbour has $k_w \ge 2$, so $\log k_w > 0$. RA penalises hub common neighbours more strongly ($1/k$ vs $1/\log k$). The two differ most when common neighbours are hubs.
- **Local vs global.** Every common-neighbour score is **zero for pairs at distance $\ge 3$** (CS224W lecture 2). Global scores such as Katz, or the random-walk-with-restart score of [the link-analysis page](./02-link-analysis.md), are non-zero for any pair in the same component.
- **Walks, not paths.** $(A^\ell)_{uv}$ counts *walks*, which may revisit nodes. Hamilton's text says "paths" loosely.

### Graph features and kernels

A **graph kernel** $\mathcal{K}(G, G') = \langle \phi(G), \phi(G') \rangle$ is a similarity whose Gram matrix is positive semidefinite, so it can be used directly in a kernel SVM.

- **Bag of nodes.** A histogram of a node statistic, e.g. degrees. This is cheap but blind to how the nodes are arranged.
- **Graphlet kernel** (Shervashidze et al., 2009). For the size-$k$ graphlets $g_1, \dots, g_{n_k}$, let $(f_G)_i$ be the number of $k$-node subsets of $G$ inducing $g_i$; this is the **$k$-spectrum**. Here graphlets are *unrooted* and *need not be connected*, so there are 4 graphlets for $k=3$ and 11 for $k=4$. To remove the effect of graph size, normalise to a distribution $D_G = f_G / \sum_i (f_G)_i$ and set $\mathcal{K}(G,G') = D_G^\top D_{G'}$.
- **Weisfeiler–Lehman subtree kernel** (Shervashidze et al., 2011). It iterates colour refinement and counts colours across *all* iterations; see below.

:::{prf:algorithm} Colour refinement (1-WL) and the WL subtree kernel
:label: alg-tasks-wl

Input: graphs $G, G'$; initial labels $l_0(v)$ (node labels, or a constant); $h$ iterations.

For $i = 1, \dots, h$, for every node $v$ of both graphs:
1. Form the string $s_i(v) = \big(l_{i-1}(v),\ \mathrm{sort}\{\!\{ l_{i-1}(u) : u \in \mathcal{N}(v) \}\!\}\big)$. The node's own colour is the prefix, followed by the sorted multiset of its neighbours' colours.
2. Relabel with an injective compression $l_i(v) = f(s_i(v))$ shared by both graphs, i.e. one hash table.

The feature vector $\phi^{(h)}(G)$ concatenates the colour counts $c_i(G, \sigma)$ for all colours $\sigma$ of iterations $0, \dots, h$. The kernel is $\mathcal{K}^{(h)}_{\mathrm{WL}}(G,G') = \langle \phi^{(h)}(G), \phi^{(h)}(G') \rangle$.
:::

After $i$ rounds, $l_i(v)$ encodes the depth-$i$ rooted **subtree** obtained by unrolling $v$'s neighbourhood, which gives the kernel its name. Hamilton's ch. 2 version hashes only the neighbour multiset. Shervashidze et al. and CS224W prepend the node's own colour; the WL literature uses this form, and it is the one that matches GNN update rules ([GNN expressive power](./06-gnn-expressive-power.md)).

(sec-tasks-results)=
## Key results

:::{prf:theorem} Katz index: closed form and convergence
:label: thm-tasks-katz

For a non-negative adjacency matrix $A$ with spectral radius $\rho(A)$, the series $\sum_{\ell \ge 1} \beta^\ell A^\ell$ converges iff $\beta < 1/\rho(A)$, and then

$$
S_{\mathrm{Katz}} = \sum_{\ell=1}^{\infty} \beta^\ell A^\ell = (I - \beta A)^{-1} - I.
$$ (eq-tasks-katz)

For undirected graphs $\rho(A) = \Lambda_{\max}$, so the condition is $\beta < 1/\Lambda_{\max}$.
:::

:::{dropdown} Derivation
- **Convergence.** Write the partial sum $T_n = \sum_{\ell=0}^{n} (\beta A)^\ell$. Then $T_n (I - \beta A) = I - (\beta A)^{n+1}$. A Neumann series converges iff $(\beta A)^n \to 0$, iff $\rho(\beta A) < 1$. In that case $I - \beta A$ is invertible and $T_n \to (I - \beta A)^{-1}$. Subtracting the $\ell = 0$ term gives {eq}`eq-tasks-katz`.
- **Spectral radius.** By Perron–Frobenius, the spectral radius of a non-negative matrix is itself an eigenvalue, and it is real and non-negative. For symmetric $A$ this is the largest eigenvalue $\Lambda_{\max}$. For directed graphs the condition is still $\beta < 1/\rho(A)$.
- **The source's wording.** Hamilton states the condition as "largest eigenvalue $< 1$". The precise condition is on the spectral radius, which coincides with the largest eigenvalue here because of Perron–Frobenius.
:::

:::{prf:proposition} Two limits of Katz (my derivation)
:label: prop-tasks-katz-limits

1. **Small $\beta$.** For a non-adjacent pair, $S_{\mathrm{Katz}}(u,v) = \beta^2 (A^2)_{uv} + \beta^3 (A^3)_{uv} + O(\beta^4)$. So as $\beta \to 0$, Katz ranks non-edges by **common neighbours** and breaks ties by 3-walks.
2. **$\beta \to 1/\Lambda_{\max}$.** Write $A = \sum_i \lambda_i x_i x_i^\top$. Then $(I - \beta A)^{-1} = \sum_i (1 - \beta \lambda_i)^{-1} x_i x_i^\top$, and in a connected graph the leading term dominates: $S_{\mathrm{Katz}} \propto x_1 x_1^\top$. The ranking collapses to the **product of eigenvector centralities**, a global, degree-like popularity score.
3. **Link to Katz centrality.** The row sums $S_{\mathrm{Katz}}\mathbf{1} = (I - \beta A)^{-1}\mathbf{1} - \mathbf{1}$ are Newman's Katz centrality $x = (I - \alpha A)^{-1}\mathbf{1}$ with $\alpha = \beta$, minus 1.
:::

:::{prf:theorem} Cost of the WL subtree kernel
:label: thm-tasks-wl-cost

On a graph with $L$ edges, $h$ iterations of colour refinement cost $O(hL)$. Multisets are sorted by counting sort over at most $N$ colours. The kernel between two graphs costs $O(hL)$, and the full $M \times M$ kernel matrix for $M$ graphs of size $N$ costs $O(MhL + M^2 hN)$. This is achieved by computing each $\phi^{(h)}(G)$ once and then taking inner products (Shervashidze et al., 2011, Theorems 5 and 7).
:::

For contrast, counting size-$k$ graphlets by enumeration costs $O(N^k)$. This is unavoidable in the worst case because subgraph isomorphism is NP-hard. For degree bounded by $d$, exact counting costs $O(N d^{k-1})$. Shervashidze et al. (2009) also bound how many sampled graphlets suffice to estimate $D_G$.

:::{prf:proposition} WL cannot separate regular graphs
:label: prop-tasks-wl-regular

With uniform initial labels, colour refinement assigns the same colour to every node of a $d$-regular graph at every iteration. Hence any two $d$-regular graphs on $N$ nodes have identical $\phi^{(h)}$ for every $h$, and $\mathcal{K}_{\mathrm{WL}}$ cannot tell them apart.
:::

:::{dropdown} Proof
By induction. At $i=0$ all colours are equal. If all colours are equal at step $i-1$, then every node's string is (that colour, $d$ copies of that colour), so all colours are equal at step $i$. The histogram at every step is $N$ copies of one colour. The colour names agree across the two graphs because the compression $f$ is shared.

The standard example is two disjoint triangles vs a 6-cycle: both are 2-regular on 6 nodes, so WL sees them as the same. A triangle count, i.e. the 3-graphlet spectrum, separates them; see the worked example.
:::

Shervashidze et al. note that 1-WL is a valid isomorphism test for *almost all* graphs. Its blind spots include regular graphs and the Cai–Fürer–Immerman constructions (cited there). *My comment:* "almost all" refers to uniformly random graphs, so it does not make these cases rare in practice: lattices, molecular rings and highly symmetric structures are common.

## Worked example

Take $G$ to be two triangles joined by a bridge. The edges are $\{1,2\}, \{1,3\}, \{2,3\}, \{3,4\}, \{4,5\}, \{4,6\}, \{5,6\}$, so $N = 6$, $L = 7$ and $\Lambda_{\max} = 1 + \sqrt 2 \approx 2.414$.

**Node features**, with GDV entries $(o_0, o_1, o_2, o_3)$:

| Node | $k$ | $t$ | $C$ | GDV |
|---|---|---|---|---|
| 1, 2, 5, 6 | 2 | 1 | 1 | $(2, 1, 0, 1)$ |
| 3, 4 | 3 | 1 | $1/3$ | $(3, 2, 2, 1)$ |

Node 3 is the end of the induced 2-paths 3–4–5 and 3–4–6, so $o_1 = 2$. It is the centre of the open wedges 1–3–4 and 2–3–4, so $o_2 = 2$. As a check of {eq}`eq-tasks-clustering-orbits`, $C_3 = 1/(2+1)$.

**Link scores**, using $\beta = 0.1 < 1/\Lambda_{\max} \approx 0.414$ and natural log:

| Pair | distance | CN | Jaccard | AA | RA | PA | Katz |
|---|---|---|---|---|---|---|---|
| (1, 4) | 2 | 1 | $1/4$ | $1/\ln 3 = 0.910$ | $1/3$ | 6 | 0.0117 |
| (2, 5) | 3 | 0 | 0 | 0 | 0 | 4 | 0.0013 |

For (1,4) the only common neighbour is 3, and $\mathcal{N}(1) \cup \mathcal{N}(4) = \{2,3,5,6\}$. The pair (2,5) is invisible to every local score, while Katz still ranks it, about 9× below (1,4). The closed form {eq}`eq-tasks-katz` matches the truncated series to $10^{-15}$.

**WL subtree kernel, $h = 2$, uniform initial label 1.** Compare $G$ with the 6-cycle $C_6$.
- Iteration 1 recovers degree: colour 2 = "degree 2", colour 3 = "degree 3".
- Iteration 2 separates the bridge nodes from the rest: colour 4 = $(2;\{2,3\})$ and colour 5 = $(3;\{2,2,3\})$ in $G$, while every node of $C_6$ gets colour 6 = $(2;\{2,2\})$.

The feature vectors over colours $1, \dots, 6$ are

$$
\phi(G) = (6, 4, 2, 4, 2, 0), \qquad \phi(C_6) = (6, 6, 0, 0, 0, 6),
$$

so $\mathcal{K}(G, C_6) = 36 + 24 = 60$, with $\mathcal{K}(G,G) = 76$ and $\mathcal{K}(C_6, C_6) = 108$. The cosine-normalised similarity is $60/\sqrt{76 \cdot 108} \approx 0.66$.

**Where WL fails.** For two disjoint triangles vs $C_6$, both $\phi$ vectors are $(6, 6, 6)$ and the kernel equals each self-similarity, so WL rates them identical ([](#prop-tasks-wl-regular)). Their 3-graphlet spectra, ordered (triangle, 2-path, single edge, empty) over all $\binom 63 = 20$ triples, separate them:

| Graph | 3-spectrum |
|---|---|
| $2C_3$ | $(2, 0, 18, 0)$ |
| $C_6$ | $(0, 6, 12, 2)$ |
| $G$ | $(2, 4, 14, 0)$ |

(I computed every number on this page from the edge lists.)

## Assumptions and limitations

- **Features are fixed, not learned.** The analyst decides what matters. CS224W's illustration (lecture 2) labels the same graph two ways, by community membership and by structural role. Structural features such as degree, clustering and GDV capture roles but cannot express the community labelling, which depends on *where* a node sits rather than what its neighbourhood looks like.
- **Degree bias.** Common neighbours, preferential attachment and Katz favour hubs. Jaccard, AA and RA, and Leicht–Holme–Newman (Hamilton ch. 2), normalise or downweight hubs in different ways. There is no universally correct normalisation; it depends on the network and the evaluation.
- **Locality.** Common-neighbour scores encode a triadic-closure assumption. They suit social networks and fail where links are mostly between dissimilar or distant nodes, e.g. bipartite-like or heterophilous graphs. *My comment:* a score that assumes homophily inherits homophily's failure modes; see the NETS 7332 homophily reading.
- **Evaluation leakage.** If supervision edges stay in the graph, scores read the answer:
  - Katz includes the term $\beta A_{uv}$ directly.
  - Jaccard's union grows by $\{u, v\}$.
  - The neighbours' degrees used by AA and RA shift.

  Hence the message/supervision split ([](#def-tasks-message-supervision)). *My comment:* precision@n for "links over time" and AUC on random holdouts measure different things, so a method that wins under one need not win under the other.
- **Kernel scalability.** Kernel SVMs need the $M \times M$ Gram matrix, and graphlet counting is exponential in $k$. WL is the scalable exception, but it carries the regular-graph blind spot.

## Connections

- **NETS 5116.**
  - Degree, centralities and clustering are defined in [Newman ch. 7](../../nets-5116/newman/07-measures-and-metrics.md). Katz *centrality* is the row sum of the Katz *index* ([](#prop-tasks-katz-limits)).
  - The preferential-attachment score $k_u k_v$ is the attachment kernel of the [Barabási–Albert model](../../nets-5116/barabasi/05-barabasi-albert-model.md).
  - Leicht–Holme–Newman similarity normalises walk counts by their configuration-model expectation $k_u k_v / 2L$.
- **NETS 6116.** Degree histograms and wedge or triangle counts are the low orders of the **dk-series**, Krioukov's systematic hierarchy of subgraph constraints. The graphlet spectrum is an unsystematic cousin of it.
- **PHYS 7335.** Katz and random-walk-with-restart scores are sums over walks. They are the same objects that set epidemic thresholds ($\Lambda_{\max}$) and random-walk stationary distributions.
- **NETS 7332.**
  - **Learned features replace hand-crafted ones** in [shallow embeddings](./03-shallow-embeddings.md) and [message-passing GNNs](./05-message-passing-gnns.md).
  - **WL colour refinement** is exactly the upper bound on message-passing expressivity ([GNN expressive power](./06-gnn-expressive-power.md)).
  - **Personalized PageRank** appears in [link analysis](./02-link-analysis.md) and **label propagation** in [label propagation](./04-label-propagation.md).
  - **Readings:** the role-discovery reading (ReFeX/RolX) builds recursive versions of these node features. The graph-distances reading compares graphs without kernels.

## Self-test

:::{dropdown} Q1. Why is graph classification only well defined in the inductive setting, while node classification can be transductive?
A graph-level label belongs to a whole graph, so evaluating it means predicting on graphs not seen in training. A transductive "graph" split would put the test graph in the training input. For node classification, the single graph can be fully observed and only the labels are split.
:::

:::{dropdown} Q2. Describe the four edge sets of a transductive link-prediction split and what each phase predicts from what.
The sets are training message, training supervision, validation and test edges.
- **Train:** message → training supervision.
- **Validation:** message + training supervision → validation.
- **Test:** message + training supervision + validation → test.

Supervision edges are never part of the structure used to compute the score being trained on, so the target cannot leak into the input.
:::

:::{dropdown} Q3. Show that the local clustering coefficient is a function of the first four GDV entries.
$o_3 = t_u$, and every pair of neighbours is either a closed wedge (a triangle) or an open one (the centre orbit $o_2$), so $o_2 + o_3 = \binom{k_u}{2}$. Hence $C_u = o_3/(o_2 + o_3)$.
:::

:::{dropdown} Q4. State the closed form and convergence condition of the Katz index, and what it reduces to as $\beta \to 0$ and as $\beta \to 1/\Lambda_{\max}$.
$S = (I - \beta A)^{-1} - I$, valid iff $\beta < 1/\rho(A)$, which is $1/\Lambda_{\max}$ for undirected graphs.
- As $\beta \to 0$, non-edges are ranked by common neighbours $(A^2)_{uv}$.
- As $\beta \to 1/\Lambda_{\max}$, $S \propto x_1 x_1^\top$, the product of eigenvector centralities.
:::

:::{dropdown} Q5. Why does Adamic–Adar weight common neighbours by $1/\log k_w$, and how does resource allocation differ?
A common neighbour of low degree is stronger evidence of a tie than a hub everyone is linked to. RA uses $1/k_w$, a resource split equally among $w$'s neighbours, and so penalises hubs more strongly than the logarithm does.
:::

:::{dropdown} Q6. Give two non-isomorphic graphs the WL subtree kernel cannot distinguish, and a feature that can.
Two disjoint triangles and $C_6$, both 2-regular on 6 nodes. With uniform labels, colour refinement never splits the single colour class. Their triangle counts (2 vs 0), i.e. their 3-graphlet spectra, differ.
:::

:::{dropdown} Q7. What is the cost of WL colour refinement, and why is it linear in edges?
$O(hL)$ for $h$ iterations. Each iteration builds every node's neighbour-colour multiset, which is $O(L)$ elements in total. It sorts these by counting sort over at most $N$ colours and compresses them with a shared injective map.
:::

---
title: Expressive Power of GNNs — the Weisfeiler–Leman Test and GIN
short_title: Expressive power
subject: NETS 7332 · Basics
description: Why message-passing GNNs can distinguish at most what 1-WL colour refinement can, which aggregators reach that bound, and what both miss.
tags: [gnn, expressivity, weisfeiler-leman, gin, graph-isomorphism, multisets]
---

:::{tip} TL;DR
- A $K$-layer message-passing GNN sees each node only through its **depth-$K$ rooted subtree** (computation tree). Expressive power is therefore the question of whether **distinct subtrees get distinct embeddings**, which holds exactly when each layer is an **injective function of a multiset** of neighbour states.
- **Upper bound** (Xu et al. 2019, Lemma 2; Morris et al. 2019, Thm 1). Any aggregation-based GNN distinguishes at most the graph pairs that **1-WL colour refinement** distinguishes.
- **Matching the bound** (Xu et al., Thm 3). This happens if both the node update $\phi\big(h_v, f(\{\!\{h_u\}\!\})\big)$ and the graph readout are injective on multisets. **GIN** achieves it: $h_v^{(k)} = \mathrm{MLP}^{(k)}\big((1+\epsilon^{(k)})\,h_v^{(k-1)} + \sum_{u\in\mathcal N(v)} h_u^{(k-1)}\big)$, with sum readouts concatenated over layers.
- **Sum > mean > max.** Sum sees the whole multiset, mean only the *distribution* of elements, and max only the underlying *set*. Mean fails on $\{a,b\}$ vs $\{a,a,b,b\}$; max fails on $\{a,b\}$ vs $\{a,a,b\}$. So GCN- and GraphSAGE-style aggregators are strictly weaker than 1-WL.
- **1-WL itself is weak.** It cannot separate regular graphs of equal degree and size, e.g. $C_6$ vs two triangles, or $C_3 \sqcup C_4$ vs $C_7$. It therefore **cannot count triangles** or compute local clustering. Going beyond requires higher-order WL ($k$-GNNs), positional or identity features, or substructure counts.
:::

- **Source.** [](doi:10.48550/arXiv.1810.00826) (Xu, Hu, Leskovec & Jegelka, *How Powerful are Graph Neural Networks?*, ICLR 2019). [](doi:10.1609/aaai.v33i01.33014602) (Morris et al., *Weisfeiler and Leman Go Neural*, AAAI 2019; preprint [arXiv:1810.02244](https://arxiv.org/abs/1810.02244)). Stanford CS224W lecture *Theory of GNNs* ([slides](https://web.stanford.edu/class/cs224w/slides/06-theory.pdf)). WL subtree kernel: Shervashidze et al., [JMLR 12 (2011)](https://jmlr.org/papers/v12/shervashidze11a.html).
- **Builds on.** The message-passing framework ([Message-passing GNNs](./05-message-passing-gnns.md)) and the WL kernel among classical graph features ([Graph-ML tasks and features](./01-graph-ml-tasks-and-features.md)).
- **Notation.** Shared symbols as in [](#notation). Page-specific symbols: $\{\!\{\cdot\}\!\}$ is a multiset; $c^{(t)}(v)$ is the 1-WL colour of $v$ after $t$ rounds; $\mathcal X$ is the (countable) space of node features; $f$, $\phi$ are the aggregation and update maps of a GNN layer.

(sec-wl-definitions)=
## Setup and definitions

:::{prf:definition} Multiset
:label: def-wl-multiset

A **multiset** is a pair $X = (S, m)$ where $S$ is the set of distinct elements and $m: S \to \mathbb{N}_{\ge 1}$ gives each element's multiplicity. The neighbour states $\{\!\{ h_u : u \in \mathcal N(v)\}\!\}$ form a multiset because different neighbours can carry identical vectors.
:::

:::{prf:definition} Aggregation-based GNN
:label: def-wl-gnn

Layer $k$ updates every node by

$$
h_v^{(k)} = \phi^{(k)}\Big( h_v^{(k-1)},\; f^{(k)}\big(\{\!\{ h_u^{(k-1)} : u \in \mathcal N(v) \}\!\}\big) \Big),
$$ (eq-wl-mp)

with $h_v^{(0)} = x_v$. A graph embedding is $h_G = \mathrm{READOUT}\big(\{\!\{ h_v^{(K)} : v \in V\}\!\}\big)$. Unrolling {eq}`eq-wl-mp` shows that $h_v^{(K)}$ is a function of the **depth-$K$ rooted subtree** at $v$: the tree of all length-$\le K$ walks out of $v$, with features at the nodes. Two nodes with identical rooted subtrees receive identical embeddings under *every* such GNN.
:::

:::{prf:definition} 1-WL colour refinement
:label: def-wl-1wl

Start from colours $c^{(0)}(v) = l(v)$, the node labels (all equal for unlabelled graphs). For $t \ge 1$,

$$
c^{(t)}(v) = \mathrm{HASH}\Big( c^{(t-1)}(v),\; \{\!\{ c^{(t-1)}(u) : u \in \mathcal N(v) \}\!\} \Big),
$$ (eq-wl-refine)

where HASH is an **injective** map to fresh colours, shared across the graphs being compared. To compare $G_1$ and $G_2$, run both in parallel. If at some round the **colour histograms** (number of nodes per colour) differ, the graphs are **non-isomorphic**. Otherwise the test is **inconclusive**. Refinement stops once the number of colour classes stops growing, which takes at most $\max(\lvert V(G_1)\rvert, \lvert V(G_2)\rvert)$ rounds. The colour after $t$ rounds encodes the depth-$t$ rooted subtree.
:::

:::{prf:definition} Distinguishing power
:label: def-wl-power

A model $A: \mathcal G \to \mathbb R^d$ **distinguishes** $G_1, G_2$ if $A(G_1) \ne A(G_2)$. Model $A$ is **at most as powerful as** $B$ if every pair $A$ distinguishes is also distinguished by $B$. In node terms (Morris et al.), a colouring $c$ **refines** $d$, written $c \sqsubseteq d$, if $c(v) = c(w) \Rightarrow d(v) = d(w)$.
:::

1-WL never declares isomorphic graphs different, but it can fail to separate non-isomorphic ones. It works for a broad class of graphs, though not all; Xu et al. cite Babai & Kučera (1979) and Cai, Fürer & Immerman (1992) for the precise statements.

(sec-wl-core)=
## Core ideas

### Expressiveness reduces to injectivity on multisets

Because a GNN only ever sees rooted subtrees, the best possible GNN maps **distinct** rooted subtrees to **distinct** vectors. Subtrees are built recursively: a depth-$k$ subtree is a root state plus the multiset of depth-$(k-1)$ child subtrees. The requirement therefore reduces to one step: the update {eq}`eq-wl-mp` must be **injective** as a function of the pair (own state, multiset of neighbour states). This is the same as the injective HASH in {eq}`eq-wl-refine`, which is why 1-WL is the reference point.

### What common aggregators keep

| Aggregator | Captures | Equal on | Used in |
|---|---|---|---|
| **sum** $\sum_{x\in X} f(x)$ | the whole multiset (for suitable $f$, Lemma 5) | only identical multisets | GIN |
| **mean** $\frac{1}{\lvert X\rvert}\sum_{x\in X} f(x)$ | the **distribution** (proportions) | $(S, m)$ and $(S, k\,m)$ for any $k \in \mathbb N_{\ge 1}$ (Cor. 8) | GCN, as analysed by Xu et al. |
| **max** (element-wise) | the **underlying set** | any two multisets with the same distinct elements (Cor. 9) | GraphSAGE-pool |

Mean is weaker than sum because rescaling multiplicities is invisible to it. Max is weaker still because multiplicities are invisible altogether. Xu et al. note that mean can be as good as sum when node features are rich and rarely repeat. That helps explain why mean aggregators do well on node classification with informative features, and poorly on structure with repeated (or no) features.

**GCN's symmetric normalisation.** Xu et al. analyse GCN as a mean over $\mathcal N(v) \cup \{v\}$. Kipf & Welling's actual propagation uses weights $1/\sqrt{(k_u+1)(k_v+1)}$, i.e. the rows of $\hat A$ (see [](#notation)). This is also non-injective. *My own check:* on any $k$-regular graph with constant input features, every row of $\hat A$ sums to $(k+1)/(k+1) = 1$. Aggregation therefore returns the constant feature for **every** $k$, at every layer. A GCN with constant inputs gives all nodes of $C_6$ (2-regular) and of $K_{3,3}$ (3-regular) identical embeddings at every depth, and identical sum or mean readouts too, since both graphs have 6 nodes. 1-WL separates them in one round by degree.

### One-layer perceptrons are not enough

Replacing the MLP by a single layer $\mathrm{ReLU}(Wx)$ without bias can also break injectivity (Xu et al., Lemma 7). Take $X_1 = \{\!\{1,1,1,1,1\}\!\}$ and $X_2 = \{\!\{2,3\}\!\}$. Every entry of $Wx$ has the same sign for all positive scalars $x$, so ReLU acts linearly on each coordinate. Both sums are then $\mathrm{ReLU}(W \cdot 5)$ for **every** $W$. The paper adds that a bias term may restore distinguishability, but a 1-layer perceptron is still not a universal approximator of multiset functions.

### GIN: an injective layer and an injective readout

Lemma 5 and Corollary 6 (below) say that a sum over a learned encoder, plus a slightly weighted root term, is injective. Modelling the encoder and the outer function with one MLP, using the universal approximation theorem, gives the **Graph Isomorphism Network**:

$$
h_v^{(k)} = \mathrm{MLP}^{(k)}\Big( \big(1+\epsilon^{(k)}\big)\, h_v^{(k-1)} + \sum_{u \in \mathcal N(v)} h_u^{(k-1)} \Big),
$$ (eq-wl-gin)

where $\epsilon^{(k)}$ is learnable or fixed; GIN-0 fixes $\epsilon = 0$. With one-hot inputs, the first sum is already injective, so no MLP is needed before it. For graph-level tasks, GIN takes a readout of **every** layer and concatenates them, in the style of Jumping Knowledge networks:

$$
h_G = \mathrm{CONCAT}\Big( \sum_{v \in V} h_v^{(k)} \;\Big|\; k = 0, 1, \dots, K \Big).
$$ (eq-wl-readout)

Shallow layers often generalise better, and deep layers are needed for discrimination. Using sum in {eq}`eq-wl-readout` keeps the readout injective, so GIN provably generalises both the WL test and the WL subtree kernel. The difference from the kernel is that the "colours" are now low-dimensional vectors. Similar subtrees can therefore land near each other, while the one-hot WL colours treat all distinct subtrees as equally different.

### The parallel result: Morris et al. (2019)

Morris et al. reach the same equivalence independently, for "1-GNNs" of the form $f^{(t)}(v) = \sigma\big(f^{(t-1)}(v) W_1^{(t)} + \sum_{w\in\mathcal N(v)} f^{(t-1)}(w) W_2^{(t)}\big)$ and their generalisations.
- **Theorem 1.** For every architecture, every label encoding consistent with $l$, and all weights, the 1-WL colouring refines the GNN's: $c^{(t)} \sqsubseteq f^{(t)}$.
- **Theorem 2.** Conversely, there exist weights such that $c^{(t)} \equiv f^{(t)}$. This already holds for the simple sum architecture above, provided distinct labels are encoded by linearly independent vectors.

Their conclusion is that 1-GNNs inherit all of 1-WL's blind spots. The examples they give are a graph made of a triangle plus a 4-cycle, where every node gets the same colour, and the inability to count triangles.

(sec-wl-beyond)=
### Beyond 1-WL (pointers)

- **$k$-WL and $k$-GNNs.** $k$-WL colours $k$-tuples of nodes. For every $k \ge 2$ there are graphs that $(k{+}1)$-WL separates and $k$-WL does not (Cai–Fürer–Immerman, as cited by Morris et al.). The $k$-WL variant Morris et al. use is as powerful as the "folklore" $(k{-}1)$-WL (Grohe & Otto, as cited). Their $k$-GNNs work on $k$-**sets** (unordered) with local neighbourhoods for scalability. They are "strictly more powerful than 1-GNNs" per the paper's contribution statement, at the cost of $\binom{N}{k}$ objects.
- **Breaking symmetry with features.** Positional or identity information (random or anchor-distance features, node identities) lets message passing tell apart nodes with identical subtrees.
- **Counting substructures.** Injecting cycle or clique counts directly targets 1-WL's best-known failure.

These are the subjects of the course readings on *WL graph kernels and the power of GNNs*, *Stability and counting in GNNs*, *Position- and identity-aware GNNs* and *Graph transformers*.

(sec-wl-results)=
## Key results

All results below assume node features come from a **countable** space $\mathcal X$ and neighbourhood multisets have **bounded size**. Xu et al.'s Lemma 4 shows that hidden features then stay in a countable space at every layer.

:::{prf:lemma} GNNs are at most as powerful as 1-WL (Xu et al., Lemma 2)
:label: lem-wl-upper

Let $G_1, G_2$ be non-isomorphic. If an aggregation-based GNN $A$ maps them to different embeddings, then 1-WL also decides that $G_1$ and $G_2$ are not isomorphic.
:::

:::{dropdown} Proof sketch
Suppose 1-WL fails to separate the graphs, so the colour histograms agree at every round. Show by induction on $k$ that equal WL colours imply equal GNN states: $c^{(k)}(v) = c^{(k)}(u) \Rightarrow h_v^{(k)} = h_u^{(k)}$.
- **Base case.** It holds at $k=0$ because both start from the same labels.
- **Inductive step.** If $v$ and $u$ share a colour at round $k$, then by injectivity of HASH their round-$(k-1)$ colours *and* neighbour-colour multisets agree. By the hypothesis their round-$(k-1)$ states and neighbour-state multisets agree, so {eq}`eq-wl-mp` returns the same value.

The two graphs therefore produce the same multiset of final states, and any permutation-invariant readout gives $A(G_1) = A(G_2)$.
:::

:::{prf:theorem} When a GNN matches 1-WL (Xu et al., Theorem 3)
:label: thm-wl-match

Suppose a GNN updates node features by $h_v^{(k)} = \phi\big(h_v^{(k-1)}, f(\{\!\{h_u^{(k-1)} : u \in \mathcal N(v)\}\!\})\big)$, with $f$ (on multisets) and $\phi$ **injective**, and its graph readout is **injective** on the multiset of node features. Then, with enough layers, it maps any two graphs that 1-WL decides are non-isomorphic to different embeddings.
:::

:::{dropdown} Proof sketch
Show by induction that $h_v^{(k)} = \varphi_k\big(c^{(k)}(v)\big)$ for some **injective** $\varphi_k$.
- **Base case.** At $k=0$, $\varphi_0$ is the identity.
- **Inductive step.** Substituting the hypothesis into the update writes $h_v^{(k)}$ as an injective function $\psi$ of $\big(c^{(k-1)}(v), \{\!\{c^{(k-1)}(u)\}\!\}\big)$, since a composition of injective maps is injective. That pair is $\mathrm{HASH}^{-1}\big(c^{(k)}(v)\big)$, so $\varphi_k = \psi \circ \mathrm{HASH}^{-1}$ is injective.

If 1-WL separates the graphs at round $K$, their colour multisets differ. So do their state multisets, and the injective readout keeps them apart.
:::

:::{prf:lemma} Sum aggregation can be injective (Xu et al., Lemma 5)
:label: lem-wl-sum

There exists $f: \mathcal X \to \mathbb R^n$ such that $h(X) = \sum_{x\in X} f(x)$ is unique for each multiset $X \subset \mathcal X$ of bounded size. Moreover, every multiset function $g$ can be written $g(X) = \varphi\big(\sum_{x\in X} f(x)\big)$ for some $\varphi$.
:::

:::{dropdown} Proof
Enumerate $\mathcal X$ injectively by $Z: \mathcal X \to \mathbb N$, and pick $N$ larger than every multiset size. Set $f(x) = N^{-Z(x)}$. The sum $\sum_{x \in X} N^{-Z(x)}$ is a base-$N$ expansion whose $Z(x)$-th digit is the multiplicity of $x$. Each multiplicity is less than $N$, so there are no carries and the multiset can be read off the digits. Given injectivity, define $\varphi$ on the image by $\varphi(h(X)) = g(X)$. This extends Zaheer et al.'s *Deep Sets* from sets to multisets.
:::

:::{prf:corollary} Injective root-plus-neighbours aggregation (Xu et al., Corollary 6)
:label: cor-wl-eps

There exists $f$ such that, for infinitely many $\epsilon$ (including **every irrational** $\epsilon$), $h(c, X) = (1+\epsilon) f(c) + \sum_{x\in X} f(x)$ is unique for each pair (root $c \in \mathcal X$, bounded multiset $X$). Any function $g(c, X)$ then factors as $\varphi\big(h(c, X)\big)$.
:::

:::{dropdown} Proof
Use the same $f(x) = N^{-Z(x)}$, which is rational, and suppose $h(c, X) = h(c', X')$ with $(c, X) \ne (c', X')$.
- **If $c = c'$**, then $X \ne X'$ and the sums differ by Lemma 5.
- **If $c \ne c'$**, rearrange to $\epsilon\,\big(f(c) - f(c')\big) = \big(f(c') + \sum_{X'} f\big) - \big(f(c) + \sum_X f\big)$. The left side is irrational times a nonzero rational, hence irrational. The right side is rational. That is a contradiction.

Without the $\epsilon$ term ($\epsilon = 0$), the root and a neighbour carrying the same feature would be interchangeable.
:::

:::{prf:corollary} What mean and max can distinguish (Xu et al., Corollaries 8–9)
:label: cor-wl-meanmax

For suitable $f$:
- **Mean.** $\frac{1}{\lvert X\rvert}\sum_X f$ identifies two multisets **iff they have the same distribution**, i.e. $X_2 = (S, k\,m)$ when $X_1 = (S, m)$.
- **Max.** $\max_{x\in X} f(x)$ (into $\mathbb R^\infty$) identifies two multisets **iff they have the same underlying set**.
:::

## Worked example

All numbers below were computed with a short script: joint 1-WL with a shared hash table, plus numpy.

**A pair 1-WL separates, but only in round 2.** Take two connected graphs on 5 nodes and 5 edges with the same degree sequence $(1,2,2,2,3)$:
- $G_1$ is a triangle $\{x, y, z\}$ with a two-edge tail $z - p - \ell$.
- $G_2$ is a 4-cycle $z - y - w - x - z$ with a pendant leaf $\ell$ on $z$.

Start from uniform colours. Round 1 colours are just degrees, so the histograms agree: $\{1{:}1,\ 2{:}3,\ 3{:}1\}$ in both. Round 2 colours are (own degree, multiset of neighbour degrees):

| Round-2 colour | $G_1$ nodes | $G_2$ nodes |
|---|---|---|
| $(1, \{\!\{2\}\!\})$: leaf next to a degree-2 node | $\ell$ | — |
| $(1, \{\!\{3\}\!\})$: leaf next to the hub | — | $\ell$ |
| $(2, \{\!\{1,3\}\!\})$ | $p$ | — |
| $(2, \{\!\{2,3\}\!\})$ | $x, y$ | $x, y$ |
| $(2, \{\!\{2,2\}\!\})$ | — | $w$ |
| $(3, \{\!\{2,2,2\}\!\})$ | $z$ | — |
| $(3, \{\!\{1,2,2\}\!\})$ | — | $z$ |

The histograms differ, so 1-WL declares the graphs non-isomorphic, which is correct. Here the giveaway is the leaf's neighbourhood.

**Pairs 1-WL cannot separate.**
- $C_6$ vs $C_3 \sqcup C_3$: both are 2-regular on 6 nodes. Every node keeps one colour class forever, with histograms $\{c^{(t)}{:}\,6\}$ in both at every round. Yet the first has **0** triangles and the second **2**, and local clustering is $C_i = 0$ vs $C_i = 1$ for every node.
- $C_3 \sqcup C_4$ vs $C_7$ (Morris et al.'s example): both are 2-regular on 7 nodes. All 7 nodes share one colour at every round.

**Aggregators on the multiset counterexamples.** Take one-hot features $a = (1,0)$, $b = (0,1)$ and $f = $ identity.

| Multiset | sum | mean | max |
|---|---|---|---|
| $\{\!\{a,b\}\!\}$ | $(1,1)$ | $(0.5,\,0.5)$ | $(1,1)$ |
| $\{\!\{a,a,b,b\}\!\}$ | $(2,2)$ | $(0.5,\,0.5)$ | $(1,1)$ |
| $\{\!\{a,a,b\}\!\}$ | $(2,1)$ | $(0.667,\,0.333)$ | $(1,1)$ |

Mean confuses rows 1–2. Max confuses all three. Sum separates all three.

**The Lemma 5 encoding.** Take $N = 5$, $Z(a)=1$, $Z(b)=2$, so $f(a) = 0.2$ and $f(b) = 0.04$. Then:
- $\{\!\{a,b\}\!\} \mapsto 0.24$
- $\{\!\{a,a,b\}\!\} \mapsto 0.44$
- $\{\!\{a,a,b,b\}\!\} \mapsto 0.48$
- $\{\!\{b,b,b,b\}\!\} \mapsto 0.16$

All are distinct, because each multiplicity is below 5. The bound matters: five copies of $b$ would give $0.2 = f(a)$, a carry into the next digit.

**GCN normalisation.** Feed constant features into $\hat A$. Both $C_6$ and $K_{3,3}$ return exactly $1$ at every node. A sum aggregator with $\epsilon = 0$ returns $3$ on $C_6$ and $4$ on $K_{3,3}$.

## Assumptions and limitations

- **Countable features.** The theorems are stated for countable feature spaces. Xu et al. say continuous features "need some further considerations" and leave them open.
- **Existence, not learnability.** Theorem 3 and Morris et al.'s Theorem 2 say suitable parameters *exist*. Universal approximation justifies MLPs in principle. *My comment:* nothing guarantees that SGD on finite data finds an injective solution, or that injectivity at training time survives on new graphs.
- **Distinguishing is not generalising.** Separating every 1-WL-distinguishable pair is a capacity statement. Xu et al. stress that a second, separate benefit of GNNs over the WL kernel is placing *similar* subtrees close together. Separating more pairs is not the same as better test accuracy, and mean or max can win when features are rich (Section 5.3 of the paper).
- **Anonymous nodes.** The bound is for message passing on node features alone. Unique identifiers or random features break the symmetry and change the picture; see the [pointers above](#sec-wl-beyond).
- **What 1-WL misses, concretely.** It cannot separate equal-size regular graphs of equal degree, cannot count triangles or cycles, and cannot compute local clustering. In general it confuses graphs whose universal covers (unrolled trees) coincide. That last sentence is *my phrasing* of the rooted-subtree view, not a quoted theorem.

## Connections

- **NETS 7332.**
  - The WL subtree kernel ([Graph-ML tasks and features](./01-graph-ml-tasks-and-features.md)) is 1-WL with colour-count features. GIN is its learnable, low-dimensional version.
  - GCN, GraphSAGE and GAT as instances of {eq}`eq-wl-mp` are covered in [Message-passing GNNs](./05-message-passing-gnns.md).
  - The readings on WL kernels, substructure counting, $*$-aware GNNs and graph transformers all start from the limits on this page.
- **NETS 5116.** Local clustering $C_i$ and triangle counts ([Newman ch. 7 notes](../../nets-5116/newman/07-measures-and-metrics.md)) are exactly the statistics 1-WL-bounded GNNs cannot compute. In the $C_6$ vs $C_3 \sqcup C_3$ example every node has $C_i = 0$ vs $C_i = 1$, yet every node gets the same colour.
- **NETS 6116.** *My observation:* round 1 of 1-WL from uniform colours recovers the degree sequence (the 1k-distribution). The round-2 histogram of (degree, neighbour-degree multiset) determines the joint degree distribution (the 2k-distribution). So two rounds of WL separate any two graphs with different 2k statistics, though not conversely. In the worked example, $G_1$ and $G_2$ share 1k but differ in 2k.

## Self-test

:::{dropdown} Q1. Why does expressive power reduce to injectivity of a function on multisets?
A $K$-layer GNN's output at $v$ depends only on $v$'s depth-$K$ rooted subtree. A depth-$k$ subtree is (root state, multiset of child subtrees). Distinct subtrees map to distinct vectors at every depth iff each layer is injective in (own state, neighbour multiset), by induction on depth.
:::

:::{dropdown} Q2. Give multisets that confuse mean and max, and say what each aggregator actually captures.
- **Mean** confuses $\{\!\{a,b\}\!\}$ and $\{\!\{a,a,b,b\}\!\}$. It captures the **distribution** (proportions).
- **Max** confuses $\{\!\{a,b\}\!\}$ and $\{\!\{a,a,b\}\!\}$. It captures the **underlying set**.
- **Sum**, with a suitable encoder, captures the full multiset.
:::

:::{dropdown} Q3. Why does GIN need the $(1+\epsilon)$ factor?
Without it, the root's own state enters the sum on the same footing as a neighbour's, so (root $a$, neighbours $\{\!\{b\}\!\}$) and (root $b$, neighbours $\{\!\{a\}\!\}$) collide. With an irrational $\epsilon$ and rational encoder $f(x) = N^{-Z(x)}$, the root's contribution carries an irrational part that no neighbour sum can cancel, which makes the pair encoding injective (Corollary 6).
:::

:::{dropdown} Q4. State the upper-bound result and the idea of its proof.
Any aggregation-based GNN distinguishes at most what 1-WL distinguishes (Xu et al. Lemma 2; Morris et al. Thm 1). The proof is an induction showing that equal WL colours imply equal GNN states, because HASH is injective. Graphs with equal colour histograms then give equal state multisets, and so equal readouts.
:::

:::{dropdown} Q5. Name two non-isomorphic graph pairs 1-WL cannot separate. Which classical network statistic does this rule out?
$C_6$ vs two disjoint triangles, and $C_3 \sqcup C_4$ vs $C_7$. All are 2-regular with equal node counts, so every node keeps the same colour. This rules out **triangle counts**, and hence **local clustering**: $0$ vs $1$ in the first pair.
:::

:::{dropdown} Q6. Why is GCN's normalised aggregator not injective even beyond the mean analysis?
On a $k$-regular graph with constant features, every row of $\hat A = \tilde D^{-1/2}(A+I)\tilde D^{-1/2}$ sums to 1. Aggregation returns the constant for every $k$, so $C_6$ and $K_{3,3}$ look identical at every layer. 1-WL separates them immediately by degree.
:::

:::{dropdown} Q7. How do $k$-GNNs go beyond 1-WL, and at what cost?
They pass messages between $k$-element node sets, mirroring the $k$-WL hierarchy, which strictly increases in power with $k$. The cost is $\binom{N}{k}$ objects per graph. Morris et al. use set-based, local neighbourhoods to keep this tractable.
:::

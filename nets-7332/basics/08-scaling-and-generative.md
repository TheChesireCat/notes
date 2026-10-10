---
title: Scaling GNNs and Deep Generative Models for Graphs
short_title: Scaling and generation
subject: NETS 7332 · Basics
description: How neighbour sampling, Cluster-GCN and SGC make GNN training fit in memory, and how GraphRNN learns a distribution over graphs.
tags: [gnn, scalability, neighbour-sampling, cluster-gcn, sgc, graph-generation, graphrnn, gcpn]
---

:::{tip} TL;DR
- A $K$-layer GNN's output at a node depends on its whole $K$-hop neighbourhood. Full-batch training stores $O(KNd)$ embeddings, which does not fit in GPU memory. Naive node mini-batches still have to expand neighbourhoods that grow roughly like $\langle k \rangle^K$.
- There are three fixes, and each drops something different:
  - **Neighbour sampling** (GraphSAGE) caps every node at $s_\ell$ sampled neighbours, giving at most $\prod_\ell s_\ell$ leaves per target. The cost is still exponential in $K$, and the sampling adds gradient variance.
  - **Cluster-GCN** runs full message passing *inside* METIS clusters, at cost linear in $K$. It loses the between-cluster edges and so gives biased gradients, which it partly repairs by batching several random clusters together.
  - **SGC** removes the nonlinearities, precomputes $\hat A^K X$ once, and trains logistic regression on it. It is the cheapest and the least expressive, and works when labels are homophilous.
- **Graph generation** is hard for three reasons: $O(N^2)$ possible edges, up to $N!$ adjacency matrices for the same graph, and long-range dependencies between edges.
- **GraphRNN** models a graph as the sequence $S^\pi$ of adjacency vectors under a node ordering. It factorises $p(S^\pi) = \prod_i p(S_i^\pi \mid S_{<i}^\pi)$ with a graph-level RNN and an edge-level RNN. Under a **BFS** ordering a new node can only link to nodes still in the BFS queue, so each step needs to look back only $M$ nodes, not $N-1$.
- Generated graphs are scored by the **MMD** between the distributions of degree, clustering and 4-node orbit counts in the generated and test sets. ER and BA are the hand-designed baselines that GraphRNN beats.
:::

- **Source.** CS224W (Fall 2021), lectures 15 [*Deep generative models for graphs*](https://snap.stanford.edu/class/cs224w-2021/slides/15-deep-generation.pdf) and 17 [*Scaling up GNNs*](https://snap.stanford.edu/class/cs224w-2021/slides/17-scalable.pdf). Primary papers: GraphSAGE [](doi:10.48550/arXiv.1706.02216), Cluster-GCN [](doi:10.1145/3292500.3330925), SGC [](doi:10.48550/arXiv.1902.07153), GraphRNN [](doi:10.48550/arXiv.1802.08773), GCPN [](doi:10.48550/arXiv.1806.02473).
- **Builds on.** [Message-passing GNNs](./05-message-passing-gnns.md); for the generative half, [random networks](../../nets-5116/barabasi/03-random-networks.md) and the [Barabási–Albert model](../../nets-5116/barabasi/05-barabasi-albert-model.md).
- **Notation.** Shared symbols as in [](#notation). Page-specific symbols:
  - $K$ is the number of GNN layers, and $B$ a mini-batch of target nodes with $b = \lvert B \rvert$.
  - $s_\ell$ is the neighbour fan-out sampled at hop $\ell$ from the target.
  - $c$ is the number of graph partitions and $q$ the number of partitions per batch (Cluster-GCN writes $p$ for $c$).
  - $\pi$ is a node ordering, $S^\pi$ the adjacency-vector sequence, and $M$ the BFS look-back width.

(sec-scale-setup)=
## Setup and definitions

Write one GCN-style layer as $H^{(\ell+1)} = \sigma(\hat A H^{(\ell)} W^{(\ell)})$ with $H^{(0)} = X$; see [message-passing GNNs](./05-message-passing-gnns.md). The output $h_v^{(K)}$ is a function of every feature in the $K$-hop ball around $v$.

:::{prf:definition} Computational graph
:label: def-scale-compgraph

The **computational graph** of target node $v$ in a $K$-layer GNN is the depth-$K$ tree unrolled from $v$. Its children at depth $\ell$ are the (sampled) neighbours of the depth-$(\ell-1)$ nodes. Its leaves carry the input features $x_u$, and its root produces $h_v^{(K)}$.
:::

:::{prf:definition} Neighbour sampling
:label: def-scale-sampling

**Neighbour sampling** replaces $\mathcal N(u)$ at each hop with a fresh uniform sample of fixed size $s_\ell$, drawn with replacement when $k_u < s_\ell$. Pruned this way, the computational graph of each target has at most $\prod_{\ell=1}^{K} s_\ell$ leaves.
:::

:::{prf:definition} Cluster-GCN mini-batch
:label: def-scale-cluster

Partition $V = V_1 \cup \dots \cup V_c$ so that few edges cross between parts (METIS). Writing $A$ in block form $[A_{st}]$, the **block-diagonal approximation** $\bar A = \operatorname{diag}(A_{11}, \dots, A_{cc})$ keeps only within-cluster edges. A batch is the subgraph induced by the union of $q$ randomly chosen clusters, *including* the edges among those $q$ clusters.
:::

:::{prf:definition} Graph sequence (GraphRNN)
:label: def-gen-sequence

Fix a node ordering $\pi$. Then $S^\pi = (S_1^\pi, \dots, S_N^\pi)$, where $S_i^\pi = (A^\pi_{1,i}, \dots, A^\pi_{i-1,i})^\top \in \{0,1\}^{i-1}$ records which of the earlier nodes $\pi(v_1),\dots,\pi(v_{i-1})$ node $\pi(v_i)$ links to. For undirected graphs $S^\pi$ determines $G$.
:::

## Core ideas

### Why full-batch and naive mini-batch training fail

- **Full batch.** One gradient step computes every $h_v^{(\ell)}$, so it stores $O(KNd + Kd^2)$ numbers. The Cluster-GCN paper puts full-graph GCN memory at $O(LNF + LF^2)$ in its own symbols. Fast per epoch, but one update per epoch and no GPU fit at million-node scale. The CS224W slides contrast 10–20 GB of GPU memory with 1–10 TB of CPU memory.
- **Naive mini-batch SGD.** The loss on a node needs its whole $K$-hop ball. On a graph with mean degree $\langle k \rangle$ and little overlap that ball has $\sim \langle k \rangle^K$ nodes, so memory is $O(b\langle k \rangle^K d)$. That is the **neighbourhood expansion** problem.

### Three ways to scale

**1. Neighbour sampling (GraphSAGE).**
- Sample the computational graph top-down from the targets, then aggregate bottom-up. Only nodes in the sampled tree are ever touched.
- GraphSAGE fixes each batch's cost at $O(\prod_{\ell=1}^{K} s_\ell)$ per target. It reports good accuracy with $K = 2$ and $s_1 s_2 \le 500$. Its default is $S_1 = 25$, $S_2 = 10$ in the paper's layer indexing: each target samples 10 direct neighbours and $25 \cdot 10 = 250$ two-hop neighbours.
- Smaller $s_\ell$ means cheaper but noisier aggregation and less stable training. Adding one layer still multiplies the cost by $s$.
- On heavy-tailed graphs uniform samples are mostly low-degree leaves. CS224W suggests keeping the neighbours with the highest random-walk-with-restart score instead ([link analysis](./02-link-analysis.md)).

**2. Cluster-GCN.**
- Instead of a tree per target, run *full* message passing on a small dense subgraph.
- Each batch costs $O(\lVert A_{tt}\rVert_0 d + b d^2)$ time and $O(bKd)$ memory, i.e. $O(bK)$ embeddings, **linear in $K$**.
- Two problems come with partitioning:
  1. The dropped between-cluster edges bias the gradient.
  2. METIS clusters are internally similar, so a single-cluster batch has a skewed label distribution and the batches vary a lot.
- **Stochastic multiple partitions** fixes both partly. Over-partition into many clusters, put $q$ random clusters in each batch, and add back the edges among them. For example, Reddit is split into 1500 clusters with 5 per batch, against 300 clusters with 1 per batch. Each epoch then sees different between-cluster edges, and the variance between batches falls.

**3. Simplified GCN (SGC).**
- Deleting every $\sigma$ collapses a $K$-layer GCN to

$$
\hat Y = \operatorname{softmax}\big(\hat A^{K} X\, \Theta\big), \qquad \Theta = W^{(0)} \cdots W^{(K-1)} .
$$ (eq-scale-sgc)

- $\bar X = \hat A^K X$ is a fixed preprocessing step: $K$ sparse–dense products, which can be done on the CPU. What remains is convex multinomial logistic regression, and the embedding of node $v$ is just row $v$ of $\bar X$.
- SGC reports up to two orders of magnitude speed-up over FastGCN, at accuracy comparable to GCN on standard node-classification benchmarks.
- Spectrally, $\hat A^K$ is a fixed **low-pass filter** on the graph signal $X$. CS224W explains why that is enough: in **homophilous** tasks, repeatedly averaging neighbours' features denoises them. This is the same assumption behind [label propagation](./04-label-propagation.md).

| Method | Memory per batch | Cost in depth $K$ | What it gives up |
|---|---|---|---|
| Full-batch GCN | $O(KNd)$ | linear, but one step per epoch | GPU fit; frequent updates |
| Neighbour sampling | $O(b \prod_\ell s_\ell\, d)$ | exponential ($\times s$ per layer) | exact neighbourhoods (adds variance) |
| Cluster-GCN | $O(bKd)$ | linear | between-cluster edges (biased gradient) |
| SGC | precomputed $\bar X$; $O(bd)$ to train | free after preprocessing | nonlinearity and learned aggregation (expressiveness) |

### Deep generative models for graphs

- **Two tasks.**
  - **Realistic generation:** learn $p_{\text{model}}(G) \approx p_{\text{data}}(G)$ from samples, then sample from it.
  - **Goal-directed generation:** generate graphs that optimise an objective under hard constraints, e.g. drug-like molecules that satisfy chemical valency.
- **Why it is harder than generating images or text:**
  1. The output space is large: $\binom{N}{2}$ possible edges.
  2. Representations are not unique: a graph has up to $N!$ adjacency matrices, so the likelihood of $G$ is a sum over orderings.
  3. Dependencies are long-range: whether an edge exists can hinge on distant parts of the graph.

**GraphRNN.**
- GraphRNN sidesteps $p(G)$ by modelling sequences. Since
  $p(G) = \sum_{S^\pi} p(S^\pi)\, \mathbf 1[f_G(S^\pi) = G]$,
  it learns $p(S^\pi)$ from sequences sampled under random orderings, and samples graphs by sampling sequences.
- The model is hierarchical:
  - The **graph-level RNN** carries state $h_i = f_{\text{trans}}(h_{i-1}, S_{i-1}^\pi)$ and emits $\theta_i = f_{\text{out}}(h_i)$.
  - The **edge-level RNN**, initialised from $h_i$, emits $S_{i,1}^\pi, S_{i,2}^\pi, \dots$ one entry at a time, each conditioned on the earlier entries.
  - **GraphRNN-S**, the simplified variant, instead samples all of $S_i^\pi$ as independent Bernoullis with parameters $\theta_i$.
- Generation stops when an end-of-sequence token is emitted, so graph size is learned too. Training is maximum likelihood on the observed (BFS-ordered) sequences.

**GCPN** treats goal-directed generation as reinforcement learning:
- The *state* is the partial molecular graph, and a GNN policy picks the next bond (or new atom) to add.
- The environment rejects valency-violating actions.
- The *reward* adds small per-step rewards for valid actions to a final property score and an adversarial term that keeps outputs close to the training molecules.
- The policy is trained with PPO after pretraining on expert trajectories.

Both GraphRNN and GCPN build graphs sequentially. GCPN conditions on a GNN embedding of the current graph rather than an RNN state, and steers generation with rewards.

(sec-scale-results)=
## Key results

:::{prf:proposition} Receptive-field size under neighbour sampling
:label: prop-scale-fanout

With fan-outs $s_1, \dots, s_K$ (hop 1 nearest to the target), the computational graph of one target has at most $\prod_{\ell=1}^{K} s_\ell$ leaves and at most $1 + \sum_{j=1}^{K} \prod_{\ell=1}^{j} s_\ell$ nodes. The batch cost is independent of $N$ and of the degree distribution.
:::

:::{dropdown} Why
Each node at depth $j-1$ gets exactly $s_j$ children, sampled with replacement if needed, so depth $j$ has $\prod_{\ell \le j} s_\ell$ nodes. Sum over depths. Duplicate nodes can only make the distinct count smaller. Without sampling, depth $j$ has $\prod$ of the actual degrees along each path, $\approx \langle k \rangle^j$ for low overlap on graphs with light tails. It is even larger on heavy-tailed graphs. A neighbour reached along an edge has on average $\langle k^2\rangle/\langle k\rangle - 1$ further neighbours, which is the same branching argument as for the giant component.
:::

:::{prf:proposition} Cost comparison (CS224W lecture 17)
:label: prop-scale-cost

Embedding $b$ targets with a $K$-layer GNN costs about $b\,s^K$ with fan-out $s$ per layer, and about $K\, b\, \langle k \rangle$ with Cluster-GCN on the induced subgraph. With $s = \langle k \rangle/2$, the Cluster-GCN cost is $2Kbs$: linear in $K$, against $b s^K$.
:::

:::{dropdown} Why
The induced subgraph on $b$ nodes has about $b\langle k\rangle$ edges if the batch's clusters keep most of their edges. Each layer is one sparse product over those edges, so $K$ layers cost $K b \langle k \rangle$. Neighbour sampling instead builds a separate tree for each target and never shares the work between overlapping trees, which is the redundancy CS224W points out.
:::

:::{prf:proposition} BFS ordering bounds the edge look-back (GraphRNN, Prop. 1 and Cor. 1)
:label: prop-gen-bfs

Let $v_1, \dots, v_N$ be a BFS ordering. If $(v_i, v_{j-1}) \in E$ but $(v_i, v_j) \notin E$ for some $i < j$, then $(v_{i'}, v_{j'}) \notin E$ for all $i' \le i$ and $j' \ge j$. Consequently a new node can link only to nodes still in the BFS queue. The number of entries of $S_i^\pi$ the model must predict is $O\big(\max_d \lvert \{v : \operatorname{dist}(v, v_1) = d\}\rvert\big)$, the width of the widest BFS level, and generation costs $O(MN)$.
:::

:::{dropdown} Why (sketch)
When BFS dequeues a node it appends *all* of its undiscovered neighbours at once. Take a node $v_j$ and an earlier node $v_i$, $i<j$. If $v_i$ had been expanded before $v_j$ was discovered, then $v_i$ is not adjacent to $v_j$, since otherwise $v_i$ would have discovered it. So $v_j$'s earlier neighbours are its BFS parent and nodes that were still in the queue when $v_j$ was discovered. Moreover, a BFS queue only ever holds nodes from two consecutive distance levels. GraphRNN then replaces $S_i^\pi$ with a fixed-length vector over the last $M$ nodes, where $M$ is estimated empirically from the training graphs.
:::

**Evaluating generators.** Visual inspection does not scale, and the likelihood is intractable. GraphRNN therefore compares *sets* of graphs:
- For each graph, compute a statistic distribution: degree, clustering, or counts of all 4-node orbits.
- Compare the generated set with the test set using the **maximum mean discrepancy**, $\mathrm{MMD}^2(p,q) = \mathbb E[k(x,x')] + \mathbb E[k(y,y')] - 2\mathbb E[k(x,y)]$.
- The kernel is Gaussian-type on the earth mover's distance between the per-graph distributions for degree and clustering. Orbit-count vectors use an RBF kernel.

On the community dataset (Table 1 of the GraphRNN paper):

| Model | Degree MMD | Clustering MMD | Orbit MMD |
|---|---|---|---|
| Erdős–Rényi | 0.021 | 1.243 | 0.049 |
| Barabási–Albert | 0.268 | 0.322 | 0.047 |
| GraphRNN | **0.014** | **0.002** | **0.039** |

ER matches degrees reasonably but misses clustering by orders of magnitude, which is the familiar failure of ER from NETS 5116.

## Worked example

**Receptive fields on Reddit.** GraphSAGE's Reddit graph has $N = 232{,}965$ posts with $\langle k \rangle = 492$.

| | 1-hop | 2-hop | Nodes in computational graph |
|---|---|---|---|
| Full neighbourhood (tree bound) | 492 | $492^2 = 242{,}064$ | 242,557, i.e. more than $N$: the whole graph |
| Sampled, $s_1 = 10$, $s_2 = 25$ | 10 | 250 | 261 |

So two layers on Reddit already touch essentially every node, while sampling caps it at 261 nodes per target.

**Neighbour sampling vs Cluster-GCN as depth grows.** Take $b = 512$ targets, $\langle k \rangle = 20$ and $s = 10$, using {prf:ref}`prop-scale-cost`:

| $K$ | Sampling, $b s^K$ | Cluster-GCN, $K b \langle k \rangle$ | Ratio |
|---|---|---|---|
| 1 | 5,120 | 10,240 | 0.5 |
| 2 | 51,200 | 20,480 | 2.5 |
| 3 | 512,000 | 30,720 | 16.7 |
| 4 | 5,120,000 | 40,960 | 125 |

At one layer sampling is cheaper. From two layers on, the exponential term dominates.

**A BFS sequence.** Take the 6-node graph with edges $01, 02, 13, 23, 24, 35, 45$. BFS from node 0 visits $0,1,2,3,4,5$, which gives

$$
S_2 = (1),\quad S_3 = (1,0),\quad S_4 = (0,1,1),\quad S_5 = (0,0,1,0),\quad S_6 = (0,0,0,1,1).
$$

Every 1 lies within the last **2** positions, so a look-back of $M = 2$ suffices; the BFS levels have sizes $1,2,2,1$. The non-BFS ordering $0,5,1,4,2,3$ needs a look-back of 4.

On a $10 \times 10$ grid (GraphRNN's grid dataset uses 100–400 nodes), over 200 random orderings:
- A random ordering needs a look-back of 84–99, mean 93.5, out of a possible 99.
- A BFS ordering from a random start needs 11–20, mean 12.9.
- The widest BFS level is 10 from a corner and 18 from the centre, in line with {prf:ref}`prop-gen-bfs`.

(All values computed from the stated graphs.)

## Assumptions and limitations

- **Sampling is not free.** It adds variance, so a smaller fan-out gives less stable training. *My comment:* a sampled mean is an unbiased estimate of the neighbourhood mean within one layer, but once composed through nonlinearities across layers the embedding estimate is biased, and max- or LSTM-type aggregators come with no such guarantee.
- **Cluster-GCN assumes a graph that partitions well.** On graphs without good cuts, many edges are dropped and the gradient bias grows. *My comment:* scale-free hubs make clean partitions hard.
- **SGC's success depends on homophily.** On heterophilous labels a fixed low-pass filter smooths away the signal. Deep powers $\hat A^K$ also over-smooth, a topic of the course's oversmoothing reading.
- **GraphRNN still depends on ordering.** BFS reduces the $N!$ orderings to the number of distinct BFS orderings but not to one. Its likelihood is over sequences, not graphs. And generation takes $O(MN)$ sequential steps; the paper's experiments use graphs of at most about 500 nodes.
- **MMD scores depend on the choices behind them.** The choice of statistics, kernel and bandwidth shapes the result. O'Bray et al. [](doi:10.48550/arXiv.2106.01098) analyse these pitfalls and recommend practices.

## Connections

- **NETS 5116.**
  - [ER](../../nets-5116/barabasi/03-random-networks.md), the configuration model and [Barabási–Albert](../../nets-5116/barabasi/05-barabasi-albert-model.md) are *hand-designed* generative models. Each has a few parameters and reproduces chosen statistics by construction: $\langle k \rangle$, the degree sequence, or $\gamma = 3$.
  - GraphRNN is the opposite trade-off: many learned parameters that fit whatever the training set shows, with no closed-form ensemble to analyse. *My comment:* the BA baseline's poor degree MMD on community graphs reflects *misspecification*, since those graphs are not grown by preferential attachment. It is not evidence against the mechanism.
  - Neighbourhood explosion is the branching of a breadth-first exploration, controlled by the excess degree as in the giant-component calculation.
- **NETS 6116.** Maximum-entropy ensembles and graphons are the principled middle ground. They specify which statistics are constrained and are otherwise maximally random, so likelihoods are explicit. *My comment:* that is a useful lens for asking which statistics an MMD evaluation actually tests.
- **PHYS 7335.** The RWR scores used for importance-based neighbour sampling are personalised random walks, the same objects as random walks on networks in that course.
- **NETS 7332.**
  - SGC is the propagation step of [label propagation](./04-label-propagation.md) applied to features. Its limited expressiveness is the nonlinearity question of [GNN expressive power](./06-gnn-expressive-power.md).
  - The readings on LightGCN (recommendation) and on the GNN design space use the same "linear propagation plus simple model" idea.

## Self-test

:::{dropdown} Q1. Why does mini-batch SGD on node labels not remove the memory problem of a deep GNN?
Each node's loss depends on its whole $K$-hop ball. The batch must still compute about $\langle k \rangle^K$ embeddings per target, so memory is $O(b\langle k \rangle^K d)$: exponential in depth, not proportional to $b$.
:::

:::{dropdown} Q2. With GraphSAGE fan-outs (10 at hop 1, 25 at hop 2), how many nodes does one target's computational graph have at most, and what is the per-batch complexity?
$1 + 10 + 250 = 261$ nodes, with $250$ leaves. The per-batch cost is $O(\prod_\ell s_\ell)$ per target, independent of $N$ and the degree distribution.
:::

:::{dropdown} Q3. What two problems does a single METIS cluster per batch cause, and how does Cluster-GCN fix them?
1. Between-cluster edges are dropped, which biases the gradient.
2. Clusters have skewed label distributions, so batches vary a lot.

The fix: over-partition, combine $q$ random clusters in each batch, and add back the edges among them.
:::

:::{dropdown} Q4. Derive the SGC model from a $K$-layer GCN and say why training it is convex.
Remove each $\sigma$: $H^{(K)} = \hat A(\cdots(\hat A X W^{(0)})\cdots)W^{(K-1)} = \hat A^K X \Theta$ with $\Theta = \prod_\ell W^{(\ell)}$. Then $\operatorname{softmax}(\bar X \Theta)$ with fixed $\bar X = \hat A^K X$ is multinomial logistic regression in $\Theta$, whose cross-entropy loss is convex.
:::

:::{dropdown} Q5. What three properties make graph generation harder than sequence generation?
1. A large output space: $O(N^2)$ potential edges.
2. Non-unique representations: up to $N!$ orderings, so $p(G)$ sums over orderings.
3. Long-range edge dependencies.
:::

:::{dropdown} Q6. Why can't a node added late in a BFS ordering connect to node $v_1$?
$v_1$ is expanded first, so all of its neighbours are discovered then. A node discovered later is not adjacent to $v_1$, or $v_1$ would have discovered it. In general a node's earlier neighbours are its parent and nodes still in the queue when it was discovered. That bounds the look-back by the queue size, which is governed by the widest BFS level.
:::

:::{dropdown} Q7. How does GraphRNN evaluation show that ER is a poor model of community graphs, and which statistic shows it?
Clustering. ER's clustering MMD is 1.243, against 0.002 for GraphRNN, while its degree MMD (0.021) is close to GraphRNN's (0.014). ER gets the degrees roughly right but has vanishing clustering, so it cannot produce dense communities.
:::

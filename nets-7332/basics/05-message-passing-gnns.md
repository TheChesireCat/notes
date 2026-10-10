---
title: "Message-Passing Graph Neural Networks: GCN, GraphSAGE and GAT"
short_title: Message-passing GNNs
subject: NETS 7332 · Basics
description: The message-passing framework, the spectral derivation of GCN, GraphSAGE and GAT, the modern GNN layer, over-smoothing, and how GNNs are trained and evaluated.
tags: [gnn, message-passing, gcn, graphsage, gat, spectral, over-smoothing]
---

:::{tip} TL;DR
- A model on graphs must be **permutation invariant**, $f(PAP^\top, PX) = f(A, X)$, or **permutation equivariant**, $f(PAP^\top, PX) = P\,f(A, X)$. **Message passing** is equivariant by construction: each node applies a shared UPDATE to its own state and a permutation-invariant AGGREGATE of its neighbours' messages. After $K$ layers a node "sees" exactly its **$K$-hop neighbourhood**.
- **GCN** is a first-order spectral filter. Truncate the Chebyshev expansion of $U g_\theta(\Lambda) U^\top$ at $K=1$, set $\lambda_{\max} \approx 2$, tie the two parameters, then apply the **renormalisation trick**. The result is $H^{(\ell+1)} = \sigma(\hat A H^{(\ell)} W^{(\ell)})$ with $\hat A = \tilde D^{-1/2} \tilde A \tilde D^{-1/2}$. A layer costs $O(\lvert E \rvert\, F C)$.
- **GraphSAGE** concatenates a node's own state with an aggregate of its neighbours (mean, LSTM or max-pool). It $\ell_2$-normalises the result and **samples a fixed number of neighbours**, which makes it inductive with a bounded cost per batch. **GAT** replaces fixed weights $1/\sqrt{\tilde d_v \tilde d_u}$ with learned attention, $\alpha_{vu} = \mathrm{softmax}_u\,\mathrm{LeakyReLU}(a^\top [W h_v \Vert W h_u])$, using several heads.
- **Depth hurts plain GNNs (over-smoothing).** With mean-type aggregation and self-loops, the influence of $u$ on $v$ after $K$ layers is proportional to a $K$-step random-walk probability, which tends to the stationary distribution. In the linear case, $\hat A^K X \to v v^\top X$ with $v \propto \tilde D^{1/2}\mathbf 1$, so every node keeps only its degree. The remedies are skip connections, a modest depth, and pre- and post-processing MLPs.
- **Training.** Put a node, edge or graph **head** on the final embeddings and use a supervised loss or a self-supervised one (e.g. random-walk co-occurrence with negative sampling). Distinguish **transductive** test nodes, which take part in message passing, from **inductive** ones, which are unseen during training.
:::

- **Sources.** Kipf & Welling [](doi:10.48550/arXiv.1609.02907); Hamilton, Ying & Leskovec [](doi:10.48550/arXiv.1706.02216); Veličković et al. [](doi:10.48550/arXiv.1710.10903); Defferrard, Bresson & Vandergheynst [](doi:10.48550/arXiv.1606.09375); Hamilton, *Graph Representation Learning*, ch. 5–7 [](doi:10.2200/S01045ED1V01Y202009AIM046); Leskovec, [CS224W (Fall 2021), lectures 6–7](http://snap.stanford.edu/class/cs224w-2021/).
- **Builds on.** [Shallow embeddings](./03-shallow-embeddings.md) (the encoder–decoder view GNNs replace); the graph Laplacian ([Newman ch. 6 notes](../../nets-5116/newman/06-mathematics-of-networks.md)).
- **Notation.** Shared symbols as in [](#notation). Matrices act on **rows**: $H^{(\ell)} \in \mathbb{R}^{N \times F_\ell}$, so $H W$ is a node-wise linear map, and the node-wise form of $HW$ uses $W^\top h_v$. On this page, $\mathcal{L}_{\mathrm{sym}} = I - D^{-1/2} A D^{-1/2} = U \Lambda U^\top$ is the normalised Laplacian, $\tilde d_v = k_v + 1$ is the degree with a self-loop, and $\Vert$ denotes concatenation. Graphs are undirected unless stated otherwise.

(sec-mpgnn-setup)=
## Setup and definitions

The input is a graph with adjacency $A$ and node features $X \in \mathbb{R}^{N \times d}$. The aim is embeddings $z_v$ (or $z_G$ for a whole graph) that a downstream head can use. Shallow encoders learn one free vector per node. They share no parameters, cannot use features, and cannot embed nodes unseen in training. GNNs replace the lookup table with a **shared, local function of features and structure** ([Hamilton et al. 2017](doi:10.48550/arXiv.1706.02216); GRL ch. 5).

Why not just flatten $A$ into an MLP? Because the output would depend on the arbitrary order of the nodes.

:::{prf:definition} Permutation invariance and equivariance
:label: def-mpgnn-perm

Let $P$ be an $N \times N$ permutation matrix. A graph-level function $f$ is **permutation invariant** if $f(PAP^\top, PX) = f(A, X)$. A node-level function is **permutation equivariant** if $f(PAP^\top, PX) = P\,f(A, X)$, so relabelling the nodes permutes the outputs in the same way.
:::

:::{prf:definition} Message-passing layer
:label: def-mpgnn-layer

With $h_v^{(0)} = x_v$, layer $\ell$ computes

$$
m_{\mathcal N(v)}^{(\ell)} = \mathrm{AGGREGATE}^{(\ell)}\big(\{\!\{\, \mathrm{MSG}^{(\ell)}(h_u^{(\ell)}) : u \in \mathcal N(v) \,\}\!\}\big),
\qquad
h_v^{(\ell+1)} = \mathrm{UPDATE}^{(\ell)}\big(h_v^{(\ell)},\, m_{\mathcal N(v)}^{(\ell)}\big),
$$ (eq-mpgnn-layer)

where $\{\!\{\cdot\}\!\}$ is a multiset and AGGREGATE is permutation invariant (sum, mean, max, or attention-weighted sum). After $K$ layers, $z_v = h_v^{(K)}$. MSG, AGGREGATE and UPDATE are shared by all nodes; the superscript only indexes the layer.
:::

:::{prf:definition} Computation graph and receptive field
:label: def-mpgnn-receptive

Unrolling {eq}`eq-mpgnn-layer` for $K$ layers turns node $v$'s computation into a depth-$K$ tree rooted at $v$. The children of each node are its neighbours. The **receptive field** of $v$ is the set of nodes appearing in that tree, which is exactly the $K$-hop neighbourhood $\{u : d_{uv} \le K\}$.
:::

(sec-mpgnn-core)=
## Core ideas

### GCN: a first-order spectral filter

Let $\mathcal L_{\mathrm{sym}} = U \Lambda U^\top$ (see [Newman ch. 6 notes](../../nets-5116/newman/06-mathematics-of-networks.md) for Laplacians). For a scalar signal $x \in \mathbb{R}^N$, $U^\top x$ is its **graph Fourier transform**. A spectral convolution multiplies it by a filter $g_\theta(\Lambda)$:

$$
g_\theta \star x = U\, g_\theta(\Lambda)\, U^\top x .
$$ (eq-mpgnn-spectral)

This costs $O(N^2)$ per multiplication, plus an eigendecomposition. The filter is not spatially localised, and it has $N$ free parameters. Following Hammond et al. [](doi:10.1016/j.acha.2010.04.005), the filter can be approximated by Chebyshev polynomials $T_k$, where $T_0 = 1$, $T_1(x) = x$ and $T_k(x) = 2xT_{k-1}(x) - T_{k-2}(x)$:

$$
g_{\theta'} \star x \approx \sum_{k=0}^{K} \theta'_k\, T_k(\tilde{\mathcal L})\, x,
\qquad
\tilde{\mathcal L} = \tfrac{2}{\lambda_{\max}} \mathcal L_{\mathrm{sym}} - I .
$$ (eq-mpgnn-cheb)

The identity $(U\Lambda U^\top)^k = U \Lambda^k U^\top$ removes the eigendecomposition. A degree-$K$ polynomial in the Laplacian is **$K$-localised**, so it mixes only nodes at most $K$ hops apart, and it costs $O(\lvert E \rvert)$ to apply. This is ChebNet [](doi:10.48550/arXiv.1606.09375). GCN is its first-order special case; the steps are under [Key results](#sec-mpgnn-results).

**Node-wise form.** Row $v$ of $\hat A H W$ gives

$$
h_v^{(\ell+1)} = \sigma\Big( W^{(\ell)\top} \sum_{u \in \mathcal N(v) \cup \{v\}} \frac{h_u^{(\ell)}}{\sqrt{\tilde d_v\, \tilde d_u}} \Big).
$$ (eq-mpgnn-gcn-node)

In message-passing terms, GCN uses symmetric-normalised aggregation and folds the update into a self-loop (GRL eq. 5.16). There is no separate weight for the node's own state.

### GraphSAGE: sample, aggregate, concatenate

For $k = 1, \dots, K$ ([Hamilton et al. 2017](doi:10.48550/arXiv.1706.02216), Alg. 1):

$$
h_{\mathcal N(v)}^{k} = \mathrm{AGGREGATE}_k\big(\{h_u^{k-1} : u \in \mathcal N(v)\}\big),
\quad
h_v^{k} = \sigma\big(W^k \cdot [\,h_v^{k-1} \Vert h_{\mathcal N(v)}^{k}\,]\big),
\quad
h_v^{k} \leftarrow h_v^{k} / \lVert h_v^{k} \rVert_2 .
$$ (eq-mpgnn-sage)

Aggregators:

| Aggregator | Definition | Notes |
|---|---|---|
| **Mean** | elementwise mean of $\{h_u^{k-1}\}$ | The "convolutional" variant, $\sigma(W \cdot \mathrm{MEAN}(\{h_v^{k-1}\} \cup \{h_u^{k-1}\}))$, drops the concatenation and is close to GCN up to normalisation. |
| **LSTM** | LSTM over a **random permutation** of the neighbours | most expressive of the three, but *not* permutation invariant |
| **Pooling** | $\max\big(\{\sigma(W_{\mathrm{pool}} h_u^{k} + b)\}\big)$, elementwise | symmetric and trainable |

The concatenation in {eq}`eq-mpgnn-sage` acts as a **skip connection** between depths: own state and neighbourhood summary keep separate weights. The paper credits it with significant gains. $\mathcal N(v)$ is redrawn as a **fixed-size uniform sample** at every depth. A batch therefore costs $O(\prod_{k=1}^K S_k)$ whatever the degrees are; $K = 2$ with $S_1 S_2 \le 500$ worked well. The weights are shared, so GraphSAGE embeds nodes, and whole graphs, that were never seen in training. This is **inductive** learning.

### GAT: learned neighbour weights

GAT ([Veličković et al. 2018](doi:10.48550/arXiv.1710.10903)) applies a shared linear map $W \in \mathbb{R}^{F' \times F}$. It then scores each edge and normalises the scores over the neighbourhood, which **includes $v$ itself**:

$$
e_{vu} = \mathrm{LeakyReLU}\big(a^\top [\,W h_v \Vert W h_u\,]\big),
\qquad
\alpha_{vu} = \frac{\exp(e_{vu})}{\sum_{w \in \mathcal N(v) \cup \{v\}} \exp(e_{vw})},
\qquad
h'_v = \sigma\Big(\sum_{u \in \mathcal N(v) \cup \{v\}} \alpha_{vu} W h_u\Big),
$$ (eq-mpgnn-gat)

with $a \in \mathbb{R}^{2F'}$ and LeakyReLU slope $0.2$. Restricting the softmax to graph neighbours ("masked attention") is what injects the structure. Without the mask, every node would attend to every node.

**Multi-head attention.** $K$ independent heads are **concatenated** in hidden layers, $h'_v = \Vert_{k=1}^{K} \sigma\big(\sum_u \alpha^k_{vu} W^k h_u\big)$, giving $KF'$ features. In the output layer they are **averaged** before the final nonlinearity. Attention is computed per edge, so the layer parallelises across edges and needs neither an eigendecomposition nor knowledge of the whole graph.

| | GCN | GraphSAGE | GAT |
|---|---|---|---|
| Neighbour weight | fixed, $1/\sqrt{\tilde d_v \tilde d_u}$ | uniform (mean) or learned (pool) | learned, depends on the features $\alpha_{vu}$ |
| Self vs neighbours | self-loop, shared weight | concatenation, separate weights | self in the softmax, shared $W$ |
| Neighbourhood | full | fixed-size sample | full |
| Setting in the paper | transductive (Cora, Citeseer, Pubmed) | inductive | both |

### The modern GNN layer and architecture

CS224W (lecture 7, after You, Ying & Leskovec, *Design Space for GNNs*, [](doi:10.48550/arXiv.2011.08843)) treats the classic layers as starting points for a general layer design:

- **Within a layer:** Linear → BatchNorm (stabilises training) → Dropout (applied to the linear layer in the message function) → Activation → Attention or gating (weights each message) → Aggregation.
- **Between layers:** stack layers, add **skip connections** of the form $F(x) + x$. With $N$ skip connections there are $2^N$ paths through the network, so the model behaves like a mixture of shallow and deep GNNs.
- **Pre-processing MLPs** encode rich node features such as text or images. **Post-processing MLPs** do the reasoning on embeddings, as in graph classification and knowledge graphs. These layers do not pass messages.
- **On depth:** choose $L$ slightly larger than the receptive field the task needs (e.g. guided by the diameter). If more expressivity is needed without more hops, make each layer's transformation an MLP.

(sec-mpgnn-training)=
### Training: heads, losses and splits

| Task | Head on top of $z_v$ | Typical loss |
|---|---|---|
| Node | $\mathrm{softmax}(z_v)$ | $-\sum_{v \in V_{\mathrm{train}}} \log \mathrm{softmax}(z_v, y_v)$ (GRL eq. 6.1) |
| Edge | score $s(z_u, z_v)$, e.g. $z_u^\top z_v$ | binary cross-entropy against sampled non-edges |
| Graph | pooling $z_G = \sum_v z_v / f_n(\lvert V \rvert)$, or attention pooling, then an MLP | cross-entropy or regression |

- **Supervised** training uses labels. **Self-supervised** training uses the graph itself, e.g. GraphSAGE's unsupervised loss $J(z_u) = -\log \sigma(z_u^\top z_v) - Q\,\mathbb{E}_{v_n \sim P_n}\log\sigma(-z_u^\top z_{v_n})$. Here $v$ co-occurs with $u$ on short random walks and $Q$ negatives are drawn from $P_n$, as in the [shallow embedding](./03-shallow-embeddings.md) objectives. The difference is that $z_u$ is now *computed from features*, not looked up.
- **Splits** (GRL §6.1):
  - $V_{\mathrm{train}}$ takes part in message passing and in the loss.
  - **Transductive** test nodes $V_{\mathrm{trans}}$ take part in message passing but have no labels. This is the "semi-supervised" setting.
  - **Inductive** test nodes $V_{\mathrm{ind}}$ and their edges are unobserved during training.
  - One-hot identity features make any GNN transductive.

(sec-mpgnn-results)=
## Key results

:::{prf:proposition} Message passing is permutation equivariant
:label: prop-mpgnn-equivariant

If every AGGREGATE is a function of the **multiset** of neighbour messages, and MSG and UPDATE are shared across nodes, then the map $(A, X) \mapsto H^{(K)}$ defined by {eq}`eq-mpgnn-layer` is permutation equivariant. Any permutation-invariant readout of $H^{(K)}$, such as sum, mean or max pooling, is then permutation invariant.
:::

:::{dropdown} Why
Relabel the nodes by $\pi$. Node $\pi(v)$ then has initial state $x_v$ and neighbourhood $\pi(\mathcal N(v))$, whose multiset of states equals that of $\mathcal N(v)$ (induction on $\ell$). The layer applies the same functions to the same inputs, so $h^{(\ell)}_{\pi(v)}$ after relabelling equals $h^{(\ell)}_v$ before it. That is $H \mapsto PH$. A set function of the rows ignores their order, which gives invariance. (GRL §5.1: equivariance "by design".) The LSTM aggregator breaks the premise, which is why GraphSAGE feeds it a random permutation.
:::

:::{prf:proposition} GCN as a renormalised first-order Chebyshev filter
:label: prop-mpgnn-gcn

Take $K = 1$ in {eq}`eq-mpgnn-cheb`, approximate $\lambda_{\max} \approx 2$, set $\theta = \theta'_0 = -\theta'_1$, and replace $I + D^{-1/2} A D^{-1/2}$ by $\hat A = \tilde D^{-1/2} \tilde A \tilde D^{-1/2}$. For $C$ input channels and $F$ filters this gives

$$
Z = \hat A X \Theta, \quad \Theta \in \mathbb{R}^{C \times F},
\qquad\text{and, stacked,}\qquad
H^{(\ell+1)} = \sigma\big(\hat A H^{(\ell)} W^{(\ell)}\big).
$$ (eq-mpgnn-gcn)

$\hat A X$ is a sparse–dense product, so the layer costs $O(\lvert E \rvert\, F C)$. The two-layer classifier in the paper is $Z = \mathrm{softmax}\big(\hat A\, \mathrm{ReLU}(\hat A X W^{(0)})\, W^{(1)}\big)$.
:::

:::{dropdown} Derivation
1. **$K = 1$.** The filter is linear in $\mathcal L_{\mathrm{sym}}$: $\theta'_0 x + \theta'_1 \tilde{\mathcal L} x$. Expressivity comes from *stacking* layers rather than from high-order polynomials. Kipf & Welling argue this reduces overfitting to local structure on graphs with very broad degree distributions.
2. **$\lambda_{\max} \approx 2$.** The eigenvalues of $\mathcal L_{\mathrm{sym}}$ lie in $[0, 2]$. With $\lambda_{\max} = 2$, $\tilde{\mathcal L} = \mathcal L_{\mathrm{sym}} - I = -D^{-1/2} A D^{-1/2}$, so the filter is $\theta'_0 x - \theta'_1 D^{-1/2} A D^{-1/2} x$. The trainable weights absorb the mismatch in scale.
3. **One parameter.** With $\theta = \theta'_0 = -\theta'_1$, the filter is $\theta\,(I + D^{-1/2} A D^{-1/2})\,x$.
4. **Renormalisation.** $I + D^{-1/2} A D^{-1/2}$ has eigenvalues in $[0, 2]$, so repeating it can blow up or vanish numerically. Replace it by $\hat A$, i.e. add self-loops *before* normalising.
5. **Channels.** Applying one filter per input–output channel pair gives $\hat A X \Theta$.
:::

:::{prf:proposition} Over-smoothing: influence becomes a random-walk distribution
:label: prop-mpgnn-oversmooth

Use a self-loop update with aggregation $\frac{1}{f_n(\lvert \mathcal N(u) \cup \{u\} \rvert)} \sum_{v \in \mathcal N(u) \cup \{u\}} h_v$, where $f_n$ is any differentiable normaliser. Define the influence $I_K(u, v) = \mathbf 1^\top \big(\partial h_v^{(K)} / \partial h_u^{(0)}\big)\mathbf 1$. Then $I_K(u, v) \propto p_{G,K}(u \mid v)$, the probability of visiting $v$ on a length-$K$ random walk started at $u$ (Xu et al. [](doi:10.48550/arXiv.1806.03536), as stated in GRL Thm. 3). As $K \to \infty$ every node's influence profile tends to the stationary distribution of the walk, so the local information is lost. On expander-like graphs this takes only $O(\log N)$ steps.
:::

:::{dropdown} Linear picture (my addition, standard spectral facts)
Drop the nonlinearities and weights, so the layers compute $\hat A^K X$. $\hat A$ is similar to the random-walk matrix $\tilde D^{-1}\tilde A$ of the graph with self-loops. For a connected graph, its eigenvalue $1$ is simple, with eigenvector $v \propto \tilde D^{1/2} \mathbf 1$. Self-loops make the graph non-bipartite, so all other eigenvalues lie strictly inside $(-1, 1)$. Hence $\hat A^K \to v v^\top$ and

$$
\hat A^K X \;\to\; v\,(v^\top X): \qquad \text{row } i \;\propto\; \sqrt{\tilde d_i}\;\cdot\; (v^\top X).
$$

Every node ends up with the *same* vector up to a degree-dependent scale. The [worked example](#sec-mpgnn-example) shows this happening in about 8 layers. Kipf & Welling report the practical consequence: the best results came from 2–3 layers, and models deeper than 7 layers were hard to train without residual connections $H^{(\ell+1)} = \sigma(\hat A H^{(\ell)} W^{(\ell)}) + H^{(\ell)}$.
:::

(sec-mpgnn-example)=
## Worked example

The graph is a triangle $\{1,2,3\}$ with a pendant node $4$ attached to $3$. Degrees with self-loops are $\tilde d = (3, 3, 4, 2)$. Features and weights:

$$
X = \begin{pmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \\ 2 & 0 \end{pmatrix},
\quad
W = \begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix},
\quad
\hat A = \begin{pmatrix}
0.333 & 0.333 & 0.289 & 0 \\
0.333 & 0.333 & 0.289 & 0 \\
0.289 & 0.289 & 0.250 & 0.354 \\
0 & 0 & 0.354 & 0.500
\end{pmatrix}.
$$

For example, $\hat A_{34} = 1/\sqrt{4 \cdot 2} = 0.354$ and $\hat A_{33} = 1/4$. One GCN layer with ReLU:

| Node | $(\hat A X)_v$ | $(\hat A X W)_v$ | $h_v^{(1)} = \mathrm{ReLU}(\cdot)$ |
|---|---|---|---|
| 1 | $(0.622,\ 0.622)$ | $(1.244,\ 0)$ | $(1.244,\ 0)$ |
| 2 | $(0.622,\ 0.622)$ | $(1.244,\ 0)$ | $(1.244,\ 0)$ |
| 3 | $(1.246,\ 0.539)$ | $(1.784,\ -0.707)$ | $(1.784,\ 0)$ |
| 4 | $(1.354,\ 0.354)$ | $(1.707,\ -1.000)$ | $(1.707,\ 0)$ |

- **GCN erases the difference between nodes 1 and 2.** Their features $(1,0)$ and $(0,1)$ differ, but their *closed* neighbourhoods $\mathcal N(v) \cup \{v\} = \{1,2,3\}$ are equal, and so are their degrees. So rows 1 and 2 of $\hat A$ are identical, and every GCN layer gives them the same output whatever $W$ is. (My observation: this holds for any two adjacent nodes with the same closed neighbourhood.)
- **GraphSAGE keeps the difference.** Its input to $W^1$ is $[\,x_v \Vert \mathrm{mean}_{u \in \mathcal N(v)} x_u\,]$. For node 1 this is $(1, 0, 0.5, 1)$; for node 2 it is $(0, 1, 1, 0.5)$. Own and neighbour information get separate weights.
- **Equivariance check.** Relabel by $P$: $f(PAP^\top, PX) = P f(A, X)$ holds numerically.
- **Over-smoothing.** $\hat A$ has eigenvalues $\{-0.148,\ 0,\ 0.564,\ 1\}$. Without self-loops, $I + D^{-1/2}AD^{-1/2}$ has eigenvalues $\{0.271,\ 0.5,\ 1.229,\ 2\}$. That is the instability the renormalisation trick removes. Repeated propagation behaves like this:

| $K$ | node 1 | node 3 | node 4 |
|---|---|---|---|
| 1 | $(0.622,\ 0.622)$ | $(1.246,\ 0.539)$ | $(1.354,\ 0.354)$ |
| 2 | $(0.774,\ 0.570)$ | $(1.149,\ 0.619)$ | $(1.117,\ 0.367)$ |
| 8 | $(0.941,\ 0.540)$ | $(1.095,\ 0.622)$ | $(0.784,\ 0.438)$ |
| 32 | $(0.947,\ 0.539)$ | $(1.093,\ 0.622)$ | $(0.773,\ 0.440)$ |

The limit is $v v^\top X$ with $v = \sqrt{\tilde d}/\lVert\sqrt{\tilde d}\rVert = (0.5,\ 0.5,\ 0.577,\ 0.408)$. Every row equals $\sqrt{\tilde d_i}\cdot(0.547,\ 0.311)$, so the node's own features are gone and only its degree remains.

(All values computed with NumPy.)

## Assumptions and limitations

- **Locality and depth are coupled.** A $K$-layer model sees exactly $K$ hops. Long-range dependencies need depth, and depth brings over-smoothing (here) and over-squashing (a later reading topic).
- **Fixed-weight aggregation and homophily.** GCN and mean aggregation average neighbours, which helps when neighbours share labels (homophily). Hamilton notes that skip and concatenation updates help most on such tasks, for moderately deep models of 2–5 layers. Heterophilous graphs are a separate reading topic.
- **Limited ability to tell structures apart.** Mean and max aggregators cannot tell some different neighbourhood multisets apart, and message passing is at most as discriminative as the 1-WL test. Kipf & Welling's appendix already draws the WL analogy. See [expressive power](./06-gnn-expressive-power.md).
- **Assumptions of GCN.** The derivation assumes an undirected graph (a symmetric $A$, so $\mathcal L_{\mathrm{sym}}$ is diagonalisable with real $U$). $\lambda_{\max} \approx 2$ is a heuristic. *My comment:* filters defined in a particular eigenbasis {eq}`eq-mpgnn-spectral` do not transfer between graphs, but polynomial filters {eq}`eq-mpgnn-cheb` and GCN do, because they are local operators.
- **Cost.** Full-neighbourhood layers have receptive fields that grow exponentially on high-degree graphs. GraphSAGE sampling bounds the cost but adds variance. Scaling is covered in [Scaling and generative models](./08-scaling-and-generative.md).
- **Transductive vs inductive results** are not comparable. Report which split was used. Benchmark pitfalls are a later reading topic.

## Connections

- **NETS 5116.**
  - $\hat A$ is the symmetric normalisation of the random-walk matrix. Its spectrum and $\mathcal L_{\mathrm{sym}}$ come from the Laplacian material in [Newman ch. 6 notes](../../nets-5116/newman/06-mathematics-of-networks.md).
  - Two-hop receptive fields interact with clustering and degree heterogeneity: hubs dominate the computation trees.
- **PHYS 7335.**
  - Over-smoothing is **diffusion to the stationary state** of a random walk ($\pi_i \propto$ degree). This is the same object as random walks on networks in the PHYS 7335 random-walk page.
  - The $\sqrt{\tilde d}$ limit is that stationary distribution, symmetrised.
- **NETS 7332.**
  - GNNs replace the lookup table of [shallow embeddings](./03-shallow-embeddings.md) while keeping their self-supervised objectives.
  - [Label propagation](./04-label-propagation.md) is message passing with no learned weights.
  - The readings on GNNs (GCN, GAT, GraphSAGE), oversmoothing and oversquashing, and WL and GIN build directly on this page.

## Self-test

:::{dropdown} Q1. Why can't you feed the flattened adjacency matrix to an MLP? State the property a node-embedding GNN must satisfy.
The output would depend on the arbitrary node order. A node-level model must be **permutation equivariant**, $f(PAP^\top, PX) = P f(A, X)$. Message passing guarantees this because AGGREGATE is a function of a multiset and the functions are shared.
:::

:::{dropdown} Q2. List the approximations that turn a spectral convolution into the GCN layer.
1. Chebyshev expansion of $g_\theta(\Lambda)$, truncated at $K = 1$.
2. $\lambda_{\max} \approx 2$, giving $\theta'_0 x - \theta'_1 D^{-1/2}AD^{-1/2}x$.
3. Tie $\theta = \theta'_0 = -\theta'_1$, giving $\theta(I + D^{-1/2}AD^{-1/2})x$.
4. Renormalisation: replace that operator by $\tilde D^{-1/2}\tilde A\tilde D^{-1/2}$, because the original has spectrum $[0, 2]$ and is unstable when repeated.
:::

:::{dropdown} Q3. What makes GraphSAGE inductive, and what bounds its cost per batch?
Its weights are shared functions of features, so a new node's embedding can be computed from its features and neighbours, with no lookup table. Sampling a fixed $S_k$ neighbours at each depth bounds a batch at $O(\prod_k S_k)$, whatever the degrees.
:::

:::{dropdown} Q4. Write the GAT attention coefficient. How are multiple heads combined?
$\alpha_{vu} = \mathrm{softmax}_{u \in \mathcal N(v) \cup \{v\}}\, \mathrm{LeakyReLU}(a^\top[W h_v \Vert W h_u])$, with slope $0.2$. Hidden layers **concatenate** the $K$ heads, giving $KF'$ features. The output layer **averages** them and then applies the final nonlinearity.
:::

:::{dropdown} Q5. Why do deep GCNs over-smooth? What is the limit of $\hat A^K X$?
With mean-type aggregation and self-loops, the influence of $u$ on $v$ is proportional to the $K$-step random-walk probability, which converges to the stationary distribution. Linearly, $\hat A^K X \to v v^\top X$ with $v \propto \tilde D^{1/2}\mathbf 1$. Rows differ only by $\sqrt{\tilde d_i}$, so the features are erased. Remedies: few layers (about the needed receptive field), skip or residual connections, and pre- and post-processing MLPs.
:::

:::{dropdown} Q6. Give two nodes with different features that GCN can never tell apart.
Two adjacent nodes with the same closed neighbourhood, e.g. nodes 1 and 2 of a triangle with a pendant attached to the third node. Their rows of $\hat A$ are identical, so $\hat A H W$ assigns them the same output in every layer. GraphSAGE's concatenation $[\,h_v \Vert h_{\mathcal N(v)}\,]$ separates them.
:::

:::{dropdown} Q7. What distinguishes transductive from inductive test nodes?
Transductive test nodes and their edges take part in message passing during training, just without labels in the loss. Inductive test nodes and their edges are completely unseen during training.
:::

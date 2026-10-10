---
title: Shallow Node Embeddings and the Matrix-Factorization View
short_title: Shallow embeddings
subject: NETS 7332 · Basics
description: Lookup-table node embeddings (Laplacian eigenmaps, DeepWalk, node2vec, LINE), how they are trained, and why they all factorize a node-similarity matrix.
tags: [node-embeddings, random-walks, node2vec, deepwalk, line, netmf, laplacian-eigenmaps]
---

:::{tip} TL;DR
- A **shallow embedding** is a lookup table: every node gets its own free vector $z_v \in \mathbb{R}^d$. A **decoder** such as $z_u^\top z_v$ turns pairs of vectors back into a similarity. Methods differ only in three choices: the target similarity $S[u,v]$, the decoder, and the loss.
- **DeepWalk** and **node2vec** take similarity to mean *co-occurrence on short random walks*, and fit it with skip-gram. node2vec biases its walk with weights $\alpha_{pq}(t,x) \in \{1/p,\,1,\,1/q\}$ for $d_{tx} \in \{0,1,2\}$. With $q<1$ the walk moves outward, like DFS, and picks up communities. With $q>1$ it stays local, like BFS. A small $p$ makes it backtrack.
- The full softmax costs $O(N)$ per training pair, because every node needs its own normaliser. **Negative sampling** replaces that normaliser with $b$ draws from a noise distribution. word2vec and LINE draw negatives $\propto k^{3/4}$; CS224W says $\propto k$; Hamilton says the noise is often uniform.
- **NetMF** (Qiu et al. 2018): in the limit of long walks, DeepWalk with negative sampling factorizes the matrix $\log\!\big(\tfrac{\mathrm{vol}(G)}{bT}\sum_{r=1}^{T}P^{r}D^{-1}\big)$, with $P = D^{-1}A$. LINE is the case $T=1$. Spectrally, this is the filter $\tfrac1T\sum_r\lambda^r$ applied to the eigenvalues of $D^{-1/2}AD^{-1/2}$. Random-walk embeddings are therefore spectral methods, close relatives of **Laplacian eigenmaps**.
- Shallow embeddings are **transductive**, ignore node features, need $O(Nd)$ parameters with nothing shared between nodes, and are identifiable only up to rotation. These limitations are what GNNs ([Message-passing GNNs](./05-message-passing-gnns.md)) are built to fix.
:::

- **Source.** Leskovec, *CS224W: Machine Learning with Graphs*, Stanford, Fall 2021, lecture 3 ("Node embeddings"); Hamilton, *Graph Representation Learning* [](doi:10.2200/S01045ED1V01Y202009AIM046), ch. 3. Primary papers: Laplacian eigenmaps [](doi:10.1162/089976603321780317); DeepWalk [](doi:10.1145/2623330.2623732); node2vec [](doi:10.1145/2939672.2939754); LINE [](doi:10.1145/2736277.2741093); NetMF [](doi:10.1145/3159652.3159706); negative sampling in word2vec [](doi:10.48550/arXiv.1310.4546).
- **Builds on.** [Graph ML tasks and features](./01-graph-ml-tasks-and-features.md); random walks and PageRank ([Link analysis](./02-link-analysis.md)); the graph Laplacian ([Newman ch. 6 notes](../../nets-5116/newman/06-mathematics-of-networks.md)).
- **Notation.** Shared symbols as in [](#notation). Graphs on this page are undirected, so $A$ is symmetric and $D = \mathrm{diag}(k_1,\dots,k_N)$.
  - $P = D^{-1}A$ is the random-walk transition matrix, so $P_{ij} = A_{ij}/k_i$.
  - $\mathrm{vol}(G) = \sum_i k_i = 2L$.
  - $Z \in \mathbb{R}^{d \times N}$ is the embedding matrix, with columns $z_v$. CS224W uses this convention; Hamilton uses the transpose.
  - $c_v$ is a separate "context" vector for node $v$.
  - $T$ is the window size, $l$ the walk length, and $b$ the number of negative samples. CS224W writes $k$ for the number of negatives; it is $b$ here to avoid a clash with degree.

(sec-emb-setup)=
## Setup and definitions

:::{prf:definition} Encoder–decoder framework
:label: def-emb-encdec

An **encoder** $\mathrm{enc}: V \to \mathbb{R}^d$ maps nodes to embeddings, $z_v = \mathrm{enc}(v)$. A **pairwise decoder** $\mathrm{dec}: \mathbb{R}^d \times \mathbb{R}^d \to \mathbb{R}$ reconstructs a target node–node similarity, so that $\mathrm{dec}(z_u, z_v) \approx S[u,v]$. Training minimises a reconstruction loss over a set $\mathcal{D}$ of node pairs,

$$
\mathcal{L} = \sum_{(u,v) \in \mathcal{D}} \ell\big(\mathrm{dec}(z_u, z_v),\, S[u,v]\big).
$$ (eq-emb-recon)
:::

:::{prf:definition} Shallow encoder
:label: def-emb-shallow

The encoder is a **shallow embedding** if it is a table lookup, $\mathrm{enc}(v) = Z e_v = z_v$, where $e_v$ is the indicator vector of $v$. Every entry of $Z$ is a free parameter, and the encoder uses neither node features nor graph structure.
:::

The encoder–decoder view makes the classical methods directly comparable. The table below follows Hamilton, Table 3.1.

| Method | Similarity $S[u,v]$ | Decoder | Loss |
|---|---|---|---|
| Laplacian eigenmaps | any symmetric weights $W_{uv}$ (e.g. $A_{uv}$) | $\lVert z_u - z_v \rVert_2^2$ | $\sum W_{uv}\,\mathrm{dec}$, subject to a scale constraint |
| Graph factorization | $A_{uv}$ | $z_u^\top z_v$ | squared error |
| GraRep | $A_{uv}, (A^2)_{uv}, \dots, (A^K)_{uv}$ | $z_u^\top z_v$ | squared error |
| HOPE | general overlap measures (e.g. Katz, Adamic–Adar) | $z_u^\top z_v$ | squared error |
| DeepWalk | $p_{G,T}(v \mid u)$: co-occurrence on uniform walks | softmax of $z_u^\top z_v$ | cross-entropy |
| node2vec | the same, on biased second-order walks | softmax of $z_u^\top z_v$ | cross-entropy |
| LINE (1st / 2nd order) | $A_{uv}$ / the neighbour distribution of $u$ | $\sigma(z_u^\top z_v)$ / softmax | KL divergence |

Random-walk similarity is **stochastic and asymmetric**: $p_{G,T}(v \mid u) \neq p_{G,T}(u \mid v)$ in general. The factorization methods above it use a deterministic similarity, typically symmetric.

## Core ideas

### Laplacian eigenmaps: the spectral baseline

Belkin and Niyogi penalise similar nodes that end up far apart. Writing $\mathcal{L} = D - W$ and stacking the embeddings as rows of $Y \in \mathbb{R}^{N \times d}$:

$$
\tfrac12 \sum_{i,j} W_{ij} \lVert y_i - y_j \rVert^2 = \operatorname{tr}(Y^\top \mathcal{L} Y),
\qquad
Y^\star = \operatorname*{arg\,min}_{Y^\top D Y = I} \operatorname{tr}(Y^\top \mathcal{L} Y).
$$ (eq-emb-le)

The constraint $Y^\top D Y = I$ rules out collapsing everything to a point. The solution is given by the eigenvectors of the **generalized eigenproblem** $\mathcal{L}y = \lambda D y$ with the smallest eigenvalues. The constant eigenvector, with $\lambda = 0$, is discarded, which is what the extra constraint $y^\top D\mathbf 1 = 0$ enforces. Since $D^{-1/2}\mathcal{L}D^{-1/2} = I - D^{-1/2}AD^{-1/2}$, these are the bottom eigenvectors of the normalized Laplacian (after rescaling by $D^{-1/2}$). That makes Laplacian eigenmaps the embedding counterpart of spectral clustering.

### Random-walk embeddings: DeepWalk

DeepWalk treats short random walks as "sentences" and nodes as "words".
- From each node it starts $\gamma$ truncated walks of length $l$, each step going to a uniformly random neighbour.
- For every node in a walk, the nodes within a window of $T$ positions are its **context**, the multiset $N_R(u)$ for walk strategy $R$.
- It then fits the skip-gram model:

$$
\max_{Z} \sum_{u \in V} \sum_{v \in N_R(u)} \log \Pr(v \mid z_u),
\qquad
\Pr(v \mid z_u) = \frac{\exp(z_u^\top z_v)}{\sum_{n \in V} \exp(z_u^\top z_n)}.
$$ (eq-emb-skipgram)

Expanding the log-softmax gives $\max \sum_u \big[-|N_R(u)| \log Z_u + \sum_{v \in N_R(u)} z_v^\top z_u\big]$, with a per-node partition function $Z_u = \sum_{n} \exp(z_u^\top z_n)$. (node2vec's Eq. 2 writes the first term as $-\log Z_u$.) The node2vec paper states that this factorisation rests on two assumptions:
- **conditional independence** of context nodes given $z_u$;
- **symmetry** in feature space.

Two practical points:
- **Cost.** Each $Z_u$ sums over all $N$ nodes. Evaluating {eq}`eq-emb-skipgram` once therefore costs $O(N)$ per (node, context) pair, and $O(N^2)$ per pass over the walks when every node starts a constant number of walks.
- **Approximating the softmax.** The original DeepWalk used **hierarchical softmax**, a binary tree over nodes that brings the cost per pair to $O(\log N)$. node2vec and LINE use negative sampling instead.

(sec-emb-negsampling)=
### Negative sampling

Negative sampling replaces the normalised softmax with a logistic classifier. The classifier separates true pairs $(u,v)$ from $b$ "noise" pairs $(u, n_i)$, where $n_i \sim P_n$:

$$
\log \sigma(z_u^\top z_v) + \sum_{i=1}^{b} \mathbb{E}_{n_i \sim P_n} \big[\log \sigma(-z_u^\top z_{n_i})\big].
$$ (eq-emb-sgns)

What each source actually says about the noise distribution $P_n$:
- **word2vec** (Mikolov et al. 2013) found that the unigram distribution raised to the $3/4$ power works best.
- **LINE** sets $P_n(v) \propto k_v^{3/4}$, using out-degree.
- **CS224W 2021** says to sample negatives with probability proportional to degree. It adds that $b$ is typically 5–20, and that a larger $b$ gives more robust estimates but more bias towards negative events.
- **Hamilton** notes that $P_n$ is often uniform in practice.
- **NetMF** assumes $P_n(j) \propto k_j$ to get a closed form, and notes that a similar result holds for $k_j^{3/4}$.

### node2vec: second-order biased walks

Suppose the walk has just crossed the edge $(t, v)$ and now sits at $v$. node2vec gives the next step $x \in \mathcal{N}(v)$ the unnormalised weight $\pi_{vx} = \alpha_{pq}(t,x)\, w_{vx}$, where

$$
\alpha_{pq}(t,x) =
\begin{cases}
1/p & d_{tx} = 0 \quad (\text{return to } t),\\
1 & d_{tx} = 1 \quad (x \text{ is also a neighbour of } t),\\
1/q & d_{tx} = 2 \quad (\text{move away from } t).
\end{cases}
$$ (eq-emb-node2vec)

Since $x \in \mathcal{N}(v)$ and $t \in \mathcal{N}(v)$, the distance $d_{tx}$ can only be 0, 1 or 2, so two parameters are enough.

- **Return parameter $p$.** If $p > \max(q,1)$, the walk rarely revisits the node it just left. If $p < \min(q,1)$, it backtracks and stays local.
- **In-out parameter $q$.** If $q > 1$, the walk is biased towards nodes near $t$. That approximates **BFS** and gives a "microscopic" view of the neighbourhood, which the paper ties to **structural equivalence**. If $q < 1$, the walk is pushed outward, approximating **DFS**. That gives a "macro" view, which the paper ties to **homophily** and communities.
- **DeepWalk** is the special case $p = q = 1$ (on an unweighted graph).
- **Cost.** The walk is second-order Markov, so precomputing transitions needs $O(a^2 N)$ memory, where $a$ is the average degree. Alias sampling then makes each step $O(1)$.
- **Edge embeddings.** For link prediction, node2vec builds an edge embedding by combining $z_u$ and $z_v$ coordinate-wise: average, Hadamard product, or weighted $\ell_1$ / $\ell_2$.

### LINE: first- and second-order proximity

LINE fits two objectives separately and concatenates the resulting embeddings.

- **First order** (undirected graphs only). The model is $p_1(i,j) = \sigma(u_i^\top u_j)$, fitted to the empirical edge distribution $\hat p_1(i,j) = w_{ij}/\sum w$. Minimising the KL divergence gives $O_1 = -\sum_{(i,j)\in E} w_{ij} \log p_1(i,j)$.
- **Second order.** Each node has a vertex vector $u_i$ and a context vector $c_i$. The model is $p_2(j \mid i) = \exp(c_j^\top u_i)/\sum_n \exp(c_n^\top u_i)$. With a KL loss weighted by $\lambda_i = k_i$, this gives $O_2 = -\sum_{(i,j)\in E} w_{ij} \log p_2(j \mid i)$. The idea is that nodes with similar neighbour (context) distributions should get similar embeddings.
- **Training.** Both objectives are trained with negative sampling {eq}`eq-emb-sgns`, using $P_n \propto k^{3/4}$.

LINE uses no random walks. Even so, it is the $T = 1$ case of the DeepWalk matrix below.

(sec-emb-results)=
## Key results

:::{prf:proposition} What skip-gram with negative sampling fits
:label: prop-emb-sgns-pmi

Use separate vertex vectors $x_w$ and context vectors $y_c$, and suppose every pair $(w,c)$ can take its inner product freely. Let $\#(\cdot)$ count occurrences in the corpus $\mathcal{D}$ of (vertex, context) pairs. Then the SGNS objective is maximised at

$$
x_w^\top y_c = \log \frac{\#(w,c)\,\lvert\mathcal{D}\rvert}{\#(w)\,\#(c)} - \log b,
$$ (eq-emb-pmi)

which is the pointwise mutual information shifted by $\log b$. NetMF uses this result of Levy and Goldberg, with noise $P_n(c) = \#(c)/\lvert\mathcal{D}\rvert$.
:::

:::{dropdown} Derivation sketch
Collect the terms of the expected objective that involve one pair $(w,c)$, and write $z = x_w^\top y_c$:

$$
\#(w,c)\log\sigma(z) + b\,\#(w)\tfrac{\#(c)}{\lvert\mathcal{D}\rvert}\log\sigma(-z).
$$

Use $\tfrac{d}{dz}\log\sigma(z) = \sigma(-z)$ and $\tfrac{d}{dz}\log\sigma(-z) = -\sigma(z)$. Setting the derivative to zero gives $\#(w,c)\,\sigma(-z) = b\,\#(w)\#(c)\,\sigma(z)/\lvert\mathcal{D}\rvert$. Since $\sigma(z)/\sigma(-z) = e^z$, the stationary point is $e^z = \#(w,c)\lvert\mathcal{D}\rvert / \big(b\,\#(w)\#(c)\big)$.

The key assumption is that the pairs decouple, i.e. that $d$ is large enough for every $z_{w,c}$ to be set independently. With a small $d$, the embedding is instead a low-rank approximation to this matrix.
:::

:::{prf:theorem} DeepWalk is implicit matrix factorization (Qiu et al. 2018)
:label: thm-emb-netmf

Let $G$ be undirected, connected and non-bipartite, and let the walk length $l \to \infty$. Then DeepWalk, with window $T$ and $b$ negative samples drawn $\propto k$, converges in probability to factorizing

$$
\log\!\Big(\frac{\mathrm{vol}(G)}{T}\Big(\sum_{r=1}^{T} P^{r}\Big) D^{-1}\Big) - \log b
\;=\; \log\!\Big(\frac{\mathrm{vol}(G)}{bT}\sum_{r=1}^{T} P^{r} D^{-1}\Big),
$$ (eq-emb-netmf)

where $\log$ acts element-wise and the factorization is $XY^\top$ (vertex × context vectors). Setting $T = 1$ gives LINE (2nd order): $\log\big(\mathrm{vol}(G)\, D^{-1}AD^{-1}\big) - \log b$.
:::

:::{dropdown} Derivation sketch
1. **Stationarity.** Under the assumptions, the walk has the unique stationary distribution $k_w/\mathrm{vol}(G)$. The paper starts walks from it, and its Remark 1 notes that a uniform start gives the same limit as $l \to \infty$.
2. **Co-occurrence counts.** Pairs at distance exactly $r$ in the walk occur with frequency $\tfrac{\#(w,c)_r}{\lvert\mathcal{D}_r\rvert} \to \tfrac{k_w}{\mathrm{vol}(G)}(P^r)_{wc}$ (Thm 2.1). Averaging forward and backward offsets over $r = 1,\dots,T$ gives $\tfrac{\#(w,c)}{\lvert\mathcal{D}\rvert} \to \tfrac{1}{2T}\sum_r \big[\tfrac{k_w}{\mathrm{vol}(G)}(P^r)_{wc} + \tfrac{k_c}{\mathrm{vol}(G)}(P^r)_{cw}\big]$ (Thm 2.2). The marginals tend to $k_w/\mathrm{vol}(G)$ and $k_c/\mathrm{vol}(G)$.
3. **Substitute into {eq}`eq-emb-pmi`.** This gives $\tfrac{\mathrm{vol}(G)}{2T}\big[\tfrac{1}{k_c}\sum_r (P^r)_{wc} + \tfrac{1}{k_w}\sum_r (P^r)_{cw}\big]$ (Thm 2.3).
4. **Matrix form.** Reversibility gives $D^{-1}(P^r)^\top = P^r D^{-1}$, because $P^rD^{-1} = D^{-1}(AD^{-1})^{r-1}AD^{-1}$ is symmetric. So the two halves are equal and the matrix is $\tfrac{\mathrm{vol}(G)}{T}\sum_r P^r D^{-1}$, which is {eq}`eq-emb-netmf`.

In practice NetMF factorizes $\log\max(M,1)$ with a truncated SVD. The truncation avoids $\log 0$ on pairs that never co-occur.
:::

:::{prf:proposition} Spectral form of the DeepWalk matrix
:label: prop-emb-filter

Let $D^{-1/2}AD^{-1/2} = U\Lambda U^\top$, whose eigenvalues satisfy $1 = \lambda_1 \ge \dots \ge \lambda_N \ge -1$. These are $1$ minus the normalized-Laplacian eigenvalues. Then

$$
\frac1T\sum_{r=1}^{T} P^{r} D^{-1} = D^{-1/2}\, U\, f_T(\Lambda)\, U^\top D^{-1/2},
\qquad f_T(\lambda) = \frac1T \sum_{r=1}^{T} \lambda^{r}.
$$ (eq-emb-filter)
:::

:::{dropdown} Why, and what it means
$P = D^{-1/2}\big(D^{-1/2}AD^{-1/2}\big)D^{1/2}$, so $P^r = D^{-1/2}U\Lambda^rU^\top D^{1/2}$. Multiplying by $D^{-1}$ on the right gives the claim.

The filter keeps $\lambda = 1$ at full strength, since $f_T(1) = 1$, and averages oscillating powers of negative eigenvalues towards 0. Larger windows therefore act as a **low-pass filter** on the graph spectrum, apart from the element-wise log and the $D^{-1/2}$ scalings. That is the sense in which random-walk embeddings and Laplacian eigenmaps / spectral clustering are the same family. Hamilton states this decomposition with the eigenvectors of the normalized Laplacian; the eigenvectors are shared, but the eigenvalues entering $f_T$ are those of $D^{-1/2}AD^{-1/2}$.
:::

### Embedding whole graphs

The lecture covers three ways to get an embedding $z_G$ for a whole graph:
1. **Pool the node embeddings**, by summing or averaging $z_v$ over the (sub)graph. CS224W attributes this to Duvenaud et al. for molecules.
2. **Add a virtual node** joined to every node of the (sub)graph and embed it as usual. CS224W attributes this to Li et al. 2016.
3. **Anonymous walks** (Ivanov & Burnaev 2018, [](doi:10.48550/arXiv.1805.11921)). Each walk is relabelled by the order in which it first visits each node, so A–B–C–B–C becomes 1–2–3–2–3. $z_G$ is then the empirical distribution of anonymous walks of length $l$, or a learned embedding of them. The number of anonymous walks of length $l$ grows quickly: 5 for $l = 3$ and 877 for $l = 7$.

*My comment:* these counts are the Bell numbers $B_l$. An anonymous walk is a restricted-growth string, and those are in bijection with set partitions of $\{1,\dots,l\}$. I checked this numerically for $l \le 7$.

## Worked example

Take the graph with edges $a\!-\!b$, $a\!-\!c$, $b\!-\!c$, $b\!-\!d$, $d\!-\!e$: a triangle $abc$ with a tail $b\!-\!d\!-\!e$. Degrees are $k = (2,3,2,2,1)$ for $(a,b,c,d,e)$, so $\mathrm{vol}(G) = 10$. All numbers below were computed with numpy.

**node2vec step.** The walk has just gone $a \to b$, so $t = a$ and $v = b$. Its options are $a$ ($d_{ax} = 0$), $c$ ($d_{ac} = 1$) and $d$ ($d_{ad} = 2$).

| $(p, q)$ | $a$ (return) | $c$ (stay near $t$) | $d$ (move out) | behaviour |
|---|---|---|---|---|
| $(1, 1)$ | 0.333 | 0.333 | 0.333 | DeepWalk |
| $(4, 0.5)$ | 0.077 | 0.308 | 0.615 | DFS-like, explores |
| $(1, 2)$ | 0.400 | 0.400 | 0.200 | BFS-like, local |
| $(0.25, 1)$ | 0.667 | 0.167 | 0.167 | backtracks |

**Laplacian eigenmaps, $d = 1$.** The generalized eigenvalues of $\mathcal{L}y = \lambda Dy$ are $0, 0.346, 1.297, 1.5, 1.857$. The first non-trivial eigenvector, normalised so that $y^\top Dy = 1$, is $y = (0.280, 0.086, 0.280, -0.391, -0.598)$. It splits the triangle (positive) from the tail (negative), with $b$ in between, and its objective value $\tfrac12\sum W_{ij}(y_i - y_j)^2 = 0.346$ equals the eigenvalue. The sign of $y$ is arbitrary.

**NetMF matrix at $T = 1$ (LINE), $b = 1$.** $M_{ij} = \mathrm{vol}(G)\,A_{ij}/(k_ik_j)$, so each edge gets weight $10/(k_ik_j)$: $M_{ab} = M_{bc} = M_{bd} = 1.667$, $M_{ac} = 2.5$ and $M_{de} = 5$. The edge between the two lowest-degree nodes gets the largest PMI. Degree normalisation means a rare co-occurrence counts for more than a common one.

**The spectral filter.** The eigenvalues of $D^{-1/2}AD^{-1/2}$ are $(1, 0.654, -0.297, -0.5, -0.857)$. The filter $f_T(\lambda)$ maps them to:

| $T$ | $\lambda = 1$ | $0.654$ | $-0.297$ | $-0.5$ | $-0.857$ |
|---|---|---|---|---|---|
| 1 | 1 | 0.654 | −0.297 | −0.500 | −0.857 |
| 2 | 1 | 0.541 | −0.104 | −0.125 | −0.061 |
| 10 | 1 | 0.186 | −0.023 | −0.033 | −0.036 |

Longer windows suppress the negative, "high-frequency" part of the spectrum.

**Noise distributions over $(a,b,c,d,e)$.**

| Noise | $a$ | $b$ | $c$ | $d$ | $e$ |
|---|---|---|---|---|---|
| $\propto k$ | 0.200 | 0.300 | 0.200 | 0.200 | 0.100 |
| $\propto k^{3/4}$ | 0.202 | 0.274 | 0.202 | 0.202 | 0.120 |
| uniform | 0.200 | 0.200 | 0.200 | 0.200 | 0.200 |

The exponent $3/4$ flattens the distribution towards rarer nodes.

## Assumptions and limitations

- **Transductive.** There is one free vector per training node. A new node, or a new graph, needs further optimisation, so shallow embeddings cannot be used inductively (Hamilton §3.4).
- **No features, no sharing.** The encoder ignores $X$. It has $O(Nd)$ parameters and shares none of them across nodes, which is statistically wasteful and expensive on large graphs.
- **Identifiability.** The inner-product decoder is unchanged under $z_v \mapsto Qz_v$ for any orthogonal $Q$. With separate context vectors, $XY^\top$ is unchanged under $X \mapsto XR$, $Y \mapsto YR^{-\top}$ for any invertible $R$. Laplacian eigenmaps fixes the eigenvectors only up to sign, or up to rotation within a repeated eigenvalue. *My comment:* coordinates from two runs, or two snapshots of a graph, cannot be compared directly. Use invariant quantities (dot products, distances) or align the embeddings first, e.g. by orthogonal Procrustes.
- **Assumptions behind the theory.** NetMF assumes an undirected, connected, non-bipartite graph, infinitely long walks, noise $\propto k$, and enough dimensions for pairs to decouple. Real runs use finite walks and small $d$, so the embedding is a low-rank approximation to {eq}`eq-emb-netmf`.
- **The BFS/DFS story is a heuristic.** node2vec's mapping of $q$ to "structural equivalence vs homophily" is an intuition about which neighbourhoods get sampled, not a theorem. Walks are local either way.
- **Low rank has limits.** Whether low-dimensional dot-product embeddings can reproduce triangle-rich graphs at all is the subject of the course's low-rank readings (Seshadhri et al.; Chanpuriya et al.).

## Connections

- **NETS 5116.**
  - Laplacian eigenmaps are the embedding version of spectral partitioning. Both use the graph Laplacian $\mathcal{L} = D - A$ ([Newman ch. 6 notes](../../nets-5116/newman/06-mathematics-of-networks.md)).
  - HOPE's similarity can be Katz centrality–style path counts.
- **NETS 6116.** *My comment:* an inner-product decoder $\sigma(z_u^\top z_v)$ is a latent-space random-graph model with a dot-product kernel. Fitting shallow embeddings is essentially estimating latent positions, which links to the latent-space and hidden-variable models in Krioukov's notes.
- **PHYS 7335.** NetMF rests on the stationary distribution of the simple random walk, $\pi_w = k_w/\mathrm{vol}(G)$, and on reversibility, $\pi_iP_{ij} = \pi_jP_{ji}$. These are the same facts used for diffusion on networks.
- **NETS 7332.**
  - [Link analysis](./02-link-analysis.md): personalized PageRank and random walks with restart are the other random-walk notion of proximity.
  - [Message-passing GNNs](./05-message-passing-gnns.md): GNNs replace the lookup table with a shared, feature-aware encoder.
  - [Scaling GNNs and generative models](./08-scaling-and-generative.md): scaling.
  - *My comment:* the [representations reading](../readings/01-representations.md) notes that a graph walk is Markovian. node2vec's walk is second-order Markov, i.e. first-order on directed edges $(t,v)$. That is the same move as a higher-order network's path-conditioned states, except that it is used here to *bias* sampling rather than to model observed paths.
  - The node-embedding reading (Laplacian eigenmaps, node2vec, SDNE, STABLE) and the low-rank reading build directly on this page.

## Self-test

:::{dropdown} Q1. In the encoder–decoder view, what are the three choices that distinguish DeepWalk from graph factorization?
1. **Similarity.** DeepWalk uses random-walk co-occurrence $p_{G,T}(v \mid u)$, which is stochastic and asymmetric. Graph factorization uses $A_{uv}$.
2. **Decoder.** DeepWalk uses a softmax over $z_u^\top z_v$. Graph factorization uses the raw inner product.
3. **Loss.** DeepWalk uses cross-entropy. Graph factorization uses squared error.

Both use the same shallow encoder.
:::

:::{dropdown} Q2. Write node2vec's unnormalised transition weight from $v$ to $x$, given that the walk came from $t$. Why are two parameters enough?
$\pi_{vx} = \alpha_{pq}(t,x)\,w_{vx}$, where $\alpha = 1/p$ if $x = t$, $1$ if $x \sim t$, and $1/q$ otherwise. Both $t$ and $x$ are neighbours of $v$, so $d_{tx} \in \{0,1,2\}$.
:::

:::{dropdown} Q3. Which setting of $q$ gives DFS-like exploration, and which notion of similarity does the paper associate with it?
$q < 1$ pushes the walk outward, away from $t$. The paper associates the resulting macro-view with **homophily** and communities. $q > 1$ gives BFS-like walks, associated with **structural equivalence**.
:::

:::{dropdown} Q4. Why is the full softmax objective $O(N^2)$, and what does negative sampling replace it with?
Every node $u$ needs its partition function $Z_u = \sum_n \exp(z_u^\top z_n)$, which costs $O(N)$. With $O(1)$ walks per node, there are $O(N)$ pairs per pass, so $O(N^2)$ in total. Negative sampling replaces $\log\Pr(v \mid z_u)$ with $\log\sigma(z_u^\top z_v) + \sum_{i=1}^{b}\log\sigma(-z_u^\top z_{n_i})$, with $n_i \sim P_n$. That costs $O(b)$ per pair.
:::

:::{dropdown} Q5. State the NetMF matrix for DeepWalk and its $T = 1$ special case.
$\log\big(\tfrac{\mathrm{vol}(G)}{bT}\sum_{r=1}^{T}P^rD^{-1}\big)$, with $P = D^{-1}A$ and the log taken element-wise. At $T = 1$ this is $\log(\mathrm{vol}(G)\,D^{-1}AD^{-1}) - \log b$, the matrix LINE (2nd order) factorizes.
:::

:::{dropdown} Q6. What constraint makes Laplacian eigenmaps well-posed, and which eigenvectors solve it?
The constraint $Y^\top DY = I$ prevents collapse, and $y^\top D\mathbf 1 = 0$ removes the trivial constant solution. The solution is the generalized eigenvectors of $\mathcal{L}y = \lambda Dy$ with the smallest *non-zero* eigenvalues.
:::

:::{dropdown} Q7. Name three limitations of shallow embeddings that motivate GNNs.
Any three of:
- They are **transductive**: unseen nodes can't be embedded without retraining.
- They **ignore node features**.
- They have **$O(Nd)$ parameters with no sharing** between nodes.
- Their coordinates are identifiable only up to rotation or sign.
:::

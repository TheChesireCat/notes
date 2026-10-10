---
title: Notation
short_title: Notation
subject: All courses
description: Symbols shared across every page, and where each textbook differs.
tags: [notation, reference]
---

(notation)=
## Shared notation

All pages use these symbols. A page that departs from them says so in its **Notation** line. Where the source textbooks disagree, the *Elsewhere* column records their choice so equations can be matched against the original.

### Graphs and matrices

| Symbol | Meaning | Elsewhere |
|---|---|---|
| $G = (V, E)$ | graph with node set $V$, edge set $E$ | |
| $N = \lvert V \rvert$ | number of nodes | Newman: $n$ |
| $L = \lvert E \rvert$ | number of edges (links) | Newman: $m$ |
| $A$, $A_{ij}$ | adjacency matrix; $A_{ij}=1$ if there is an edge **from $j$ to $i$** | Same in Barabási and Newman. GNN code (e.g. `edge_index`) usually stores source → target. |
| $W$, $w_{ij}$ | weighted adjacency matrix | |
| $k_i$, $k_i^{\mathrm{in}}$, $k_i^{\mathrm{out}}$ | degree, in-degree, out-degree of node $i$ | |
| $\langle k \rangle$, $\langle k^2 \rangle$ | first and second moments of the degree distribution | Newman: $c$ for mean degree in random-graph chapters |
| $p_k$ | degree distribution, $P(\text{degree}=k)$ | Some papers: $P(k)$ |
| $\gamma$ | degree exponent, $p_k \sim k^{-\gamma}$ | Newman: $\alpha$ |
| $D$ | diagonal degree matrix, $D_{ii} = k_i$ | |
| $\mathcal{L} = D - A$ | combinatorial graph Laplacian | Newman: $L$ (clashes with edge count here) |
| $\Lambda_{\max}$ | largest eigenvalue of $A$ | Newman: $\kappa_1$ |
| $d_{ij}$, $\langle d \rangle$, $d_{\max}$ | shortest-path distance, mean distance, diameter | Newman: $\ell$ |
| $C_i$, $\langle C \rangle$, $C$ | local clustering, mean local clustering, global transitivity | |
| $r$ | degree assortativity coefficient | |
| $Q$ | modularity | |
| $\mathcal{N}(i)$ | neighbourhood of node $i$ | ML papers: $\mathcal{N}(v)$ |

### Random graphs and generating functions

| Symbol | Meaning |
|---|---|
| $G(N, p)$, $G(N, L)$ | Erdős–Rényi ensembles: independent edges with probability $p$, or exactly $L$ edges |
| $G_0(x) = \sum_k p_k x^k$ | degree generating function |
| $G_1(x) = G_0'(x)/G_0'(1)$ | excess-degree generating function |
| $q_k = (k+1)p_{k+1}/\langle k \rangle$ | excess-degree distribution |
| $S$ | fraction of nodes in the giant component |
| $u$ | probability that an edge does not lead to the giant component |
| $f$, $f_c$ | fraction of nodes removed, critical fraction |

### Spreading processes

| Symbol | Meaning |
|---|---|
| $S, I, R$ (or $s, i, r$ as densities) | susceptible, infected, recovered compartments |
| $\beta$ | transmission rate per contact |
| $\mu$ | recovery rate |
| $\lambda = \beta/\mu$ | effective spreading rate |
| $\lambda_c$ | epidemic threshold |
| $R_0$, $R_t$ | basic and effective reproduction numbers |
| $\rho$ | stationary prevalence (SIS) or final epidemic size (SIR) |
| $\Theta$ | probability that an edge points to an infected node (heterogeneous mean-field) |

### Graph machine learning

| Symbol | Meaning |
|---|---|
| $X \in \mathbb{R}^{N \times d}$ | node feature matrix; row $x_v$ |
| $h_v^{(\ell)}$, $H^{(\ell)}$ | embedding of node $v$ / all nodes after layer $\ell$; $H^{(0)} = X$ |
| $z_v$ | final node embedding |
| $W^{(\ell)}$ | learnable weights of layer $\ell$ |
| $\sigma$ | pointwise nonlinearity |
| $\tilde A = A + I$, $\tilde D$ | adjacency with self-loops and its degree matrix |
| $\hat A = \tilde D^{-1/2} \tilde A \tilde D^{-1/2}$ | GCN propagation matrix |

### Higher-order structures

| Symbol | Meaning |
|---|---|
| $\mathcal{H} = (V, \mathcal{E})$ | hypergraph; $\mathcal{E} \subseteq 2^V$ |
| $K$ | simplicial complex |
| $X(G)$ | clique (flag) complex of graph $G$ |
| $d_{\mathcal{H}}(i)$ | hyperdegree: number of hyperedges containing $i$ |
| $\lvert e \rvert$ | cardinality of hyperedge $e$ |

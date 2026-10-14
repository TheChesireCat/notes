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
| $t_i$ | number of triangles containing node $i$ | |
| $\mathrm{vol}(G) = \sum_i k_i = 2L$ | volume of an undirected graph | |
| $\{\!\{\cdot\}\!\}$ | multiset (e.g. of neighbour states) | |

### Random walks and normalised matrices

| Symbol | Meaning | Elsewhere |
|---|---|---|
| $P = D^{-1}A$ | random-walk matrix of an undirected graph; $P_{ij} = A_{ij}/k_i$ is the probability of stepping $i \to j$ | |
| $M = A D_{\mathrm{out}}^{-1}$ | column-stochastic transition matrix of a directed graph, $M_{ij} = A_{ij}/k_j^{\mathrm{out}}$ (step $j \to i$) | CS224W uses the same |
| $D_{\mathrm{out}}$ | diagonal out-degree matrix | |
| $S = D^{-1/2} A D^{-1/2}$ | symmetrically normalised adjacency | |
| $\mathcal{L}_{\mathrm{sym}} = I - S$ | normalised Laplacian | |
| $v$ | teleport / restart distribution (PageRank, PPR, RWR) | |
| $\beta$ | PageRank damping factor (probability of following a link). **Clashes** with the transmission rate; pages using both say which is meant. | Newman: $\alpha$ |

### Network ensembles and latent-variable models

Used mainly on the NETS 6116 pages. Krioukov's notes write $n$, $m$ and $\bar k$ for $N$, $L$ and $\langle k \rangle$; these pages keep the shared symbols. Several of Krioukov's symbols clash with the spreading-process ones, so each page states which meaning applies.

| Symbol | Meaning | Elsewhere / clash |
|---|---|---|
| $\mathcal{G}_N$, $\mathcal{G}$ | set of graphs the ensemble lives on (e.g. simple graphs on $N$ labelled nodes) | |
| $P(G)$ | probability of graph $G$ under an ensemble | |
| $H[P] = -\sum_G P(G)\ln P(G)$ | Shannon (Gibbs) entropy of an ensemble | Not $S$, which is the giant-component size |
| $\mathbf{k} = (k_1,\dots,k_N)$ | degree sequence | |
| $\mathrm{CM}$, $\mathrm{SCM}$, $\mathrm{HSCM}$ | configuration model (microcanonical, fixed $\mathbf{k}$), soft configuration model (canonical, expected $\mathbf{k}$), hypersoft CM (hypercanonical, $\mathbf{k}$ drawn from a distribution) | |
| $\lambda_i$ | Lagrange multiplier conjugate to a constraint. **Clashes** with the spreading rate $\lambda$ | Krioukov: $\lambda$ |
| $p_{ij}$ | probability that edge $ij$ exists | |
| $\kappa_i$, $\rho(\kappa)$ | hidden variable (expected degree) of node $i$ and its density. Always written with a subscript or argument, unlike the scalar $\kappa = \langle k^2\rangle/\langle k\rangle$; $\rho(\kappa)$ is not prevalence or spectral radius | Krioukov: same; Chung–Lu: $w_i$ |
| $W(x,y)$ | graphon $[0,1]^2 \to [0,1]$ (unrelated to the weight matrix $W$) | |
| $\mu$ | global density/scale parameter fixing $\langle k \rangle$ in latent-space models. **Clashes** with the recovery rate | Krioukov: $\mu$ |
| $\beta$ | inverse temperature of latent-space and exponential-random-graph models, controlling clustering. **Clashes** with the transmission rate | Krioukov: $\beta$ |
| $\theta_i$, $r_i$ | angular and radial coordinate of node $i$ in the $\mathbb{S}^1$/$\mathbb{H}^2$ models | |
| $B$, $\sigma_i$ | SBM block-probability matrix and block (community) label of node $i$. Where both appear, the non-backtracking matrix is written $B_{\mathrm{NB}}$ | Many papers: $\omega$, $g_i$ |
| $x_i$, $\rho(x)$ | generic hidden variable and its density, when it is not an expected degree (not the GNN feature row $x_v$) | |
| $h(p) = -p\ln p - (1-p)\ln(1-p)$ | binary entropy of one edge slot | |
| $\alpha$, $\nu$ | **page-local.** $\alpha = \gamma - 1$ (CCDF exponent, HSCM) or the radial exponent with $\gamma = 2\alpha + 1$ ($\mathbb{H}^2$); $\nu$ is the excess-degree branching factor $\langle k(k-1)\rangle/\langle k\rangle$ or an HSCM constant. Each page defines which | Newman: $\alpha = \gamma$ |

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

### Degree classes

| Symbol | Meaning |
|---|---|
| $N_k$ | number of nodes of degree $k$ |
| $\kappa = \langle k^2 \rangle / \langle k \rangle$ | heterogeneity parameter; mean degree of a neighbour reached along a random edge |
| $P(k' \mid k)$ | probability that an edge from a degree-$k$ node ends at a degree-$k'$ node; uncorrelated: $k' p_{k'}/\langle k \rangle$ |
| $\bar k_{nn}(k)$ | mean neighbour degree of degree-$k$ nodes |
| $C_{kk'} = k\,P(k' \mid k)$ | degree-class connectivity matrix (heterogeneous mean-field thresholds) |
| $P(k, k')$ | joint degree distribution: probability that a random edge end pair has degrees $(k, k')$ (the 2k distribution) |
| $C(k)$ | degree-dependent clustering (clustering spectrum); the dk-series page writes $\bar C(k)$ for its ensemble average |
| $k_s$, $k_{\max}$ | structural cutoff $\sim\sqrt{\langle k\rangle N}$ and natural cutoff $\sim N^{1/(\gamma-1)}$ |

### Spreading processes

| Symbol | Meaning |
|---|---|
| $S, I, R$ (or $s, i, r$ as densities) | susceptible, infected, recovered compartments. **Clash:** $S$ is also the giant-component / epidemic size, so pages that need both write densities $s, i, r$ |
| $\beta$ | transmission rate **per contact** (per edge) |
| $\bar\beta = \beta \langle k \rangle$ | per-capita force-of-infection rate under homogeneous mixing; homogeneous-mixing pages that write $\beta$ for this say so |
| $\mu$ | recovery rate |
| $\sigma$ | latent (E → I) rate in SEIR |
| $\lambda = \beta/\mu$ | effective spreading rate (rumour pages use $\lambda$ for the spreading rate itself, and say so) |
| $\lambda_c$ | epidemic threshold |
| $R_0$, $R_t$ | basic and effective reproduction numbers |
| $R_*$ | global invasion threshold of a metapopulation |
| $r$ | early (Malthusian) growth rate, $I(t) \propto e^{rt}$; written $r_g$ where it would clash with the recovered density $r$ |
| $\rho$, $\rho_k$, $\rho_i$ | prevalence (SIS) or final size (SIR); per degree class; per node |
| $\rho(\cdot)$, $s(\cdot)$ | spectral radius and spectral bound of a matrix (always with an argument, to distinguish from prevalence) |
| $\Theta$ | probability that an edge points to an infected node (heterogeneous mean-field) |
| $T$ | transmissibility: probability an infected node transmits along a given edge before recovering |
| $P_\infty$ | probability that a single seed causes a large outbreak |
| $g$, $g_c$ | immunised fraction and its critical value |
| $B$ | non-backtracking (Hashimoto) matrix; SIR threshold $T_c = 1/\Lambda_{\max}(B)$ |
| $\mathrm{IPR}$ | inverse participation ratio of the leading eigenvector (localisation) |
| $\mathcal{L}_{\mathrm{rw}} = I - P$ | random-walk Laplacian |

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
| $\mathcal{V}_L$, $\mathcal{V}_U$ | labelled and unlabelled node sets (semi-supervised node classification) |
| $h$ | edge homophily ratio: fraction of edges joining same-label nodes (not to be confused with $h_v^{(\ell)}$) |
| $\mathcal{R}$ | set of relation (edge) types in a heterogeneous or knowledge graph |

### Higher-order structures

| Symbol | Meaning |
|---|---|
| $\mathcal{H} = (V, \mathcal{E})$ | hypergraph; $\mathcal{E} \subseteq 2^V$ |
| $K$ | simplicial complex |
| $X(G)$ | clique (flag) complex of graph $G$ |
| $d_{\mathcal{H}}(i)$ | hyperdegree: number of hyperedges containing $i$ |
| $\lvert e \rvert$ | cardinality of hyperedge $e$ |

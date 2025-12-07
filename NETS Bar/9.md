# Chapter 9: Community Structure

## Section 9.1: Introduction

Belgium presents an interesting case study of bicultural coexistence, with 59% Flemish Dutch-speakers and 40% Walloon French-speakers. In 2007, Vincent Blondel and colleagues analyzed the country's mobile call network to understand this social structure. They discovered that Belgium's social network breaks into two large clusters with minimal inter-cluster communication, each dominated by speakers of one language.

In network science, a **community** is a group of nodes with higher likelihood of connecting to each other than to nodes outside the group. Communities play crucial roles in:

**Social Networks**: Employees interact more with coworkers than outsiders; friend circles and hobby groups form natural communities. Zachary's Karate Club (Image 9.2) is a classic dataset capturing 78 interactions among 34 club members. When the club split due to conflict between the president and instructor, the split revealed the underlying community structure—a validation point for algorithms.

**Biological Networks**: Communities represent functional modules in cellular networks. Lee Hartwell (pre-Nobel Prize) argued biology must study groups of molecules performing specific functions. The disease module hypothesis proposes that each disease corresponds to a specific neighborhood in the cellular network.

### H1: Fundamental Hypothesis

*A network's community structure is uniquely encoded in its wiring diagram.*

---

## Section 9.2: Basics of Communities

### Defining Communities

Communities are locally dense connected subgraphs, resting on two hypotheses:

**Connectedness Hypothesis**: Each community forms a connected subgraph; nodes must be reachable through community members.

**Density Hypothesis**: Community members connect more frequently to each other than to outsiders.

**Community Definitions**:

- **Cliques**: Complete subgraphs where all nodes connect to each other. Rare in real networks; too restrictive.

- **Strong Communities**: Connected subgraph $C$ where each node $i$ satisfies:
$$k_i^{\text{int}}(C) > k_i^{\text{ext}}(C) \quad (9.1)$$

- **Weak Communities**: Connected subgraph where:
$$\sum_{i \in C} k_i^{\text{int}}(C) > \sum_{i \in C} k_i^{\text{ext}}(C) \quad (9.2)$$

### Number of Communities

**Graph Bisection**: Dividing a network into two groups minimizing inter-group links. The number of ways to partition $N$ nodes into groups of sizes $N_1$ and $N_2$ is:
$$\frac{N!}{N_1! N_2!} \quad (9.3)$$

For equal-sized bisections, this grows exponentially as:
$$\frac{2^{N+1}}{\sqrt{N}} = e^{(N+1)\ln 2 - \frac{1}{2}\ln N} \quad (9.5)$$

**Community Detection**: Networks can be partitioned into arbitrary numbers of groups. The number of possible partitions (Bell numbers) grows faster than exponentially:
$$B_N = \frac{1}{e}\sum_{j=0}^{\infty} \frac{j^N}{j!} \quad (9.6)$$

This fundamental challenge means brute-force approaches are computationally infeasible. We need polynomial-time algorithms.

---

## Section 9.3: Hierarchical Clustering

Hierarchical clustering uses a **similarity matrix** whose elements $x_{ij}$ indicate node distance. Two approaches:

- **Agglomerative**: Merge similar nodes into communities
- **Divisive**: Remove weak links separating communities

### Ravasz Algorithm (Agglomerative)

**Step 1: Topological Overlap Matrix**

$$x_{ij}^o = \frac{J(i,j)}{\min(k_i, k_j) + 1 - \Theta(A_{ij})} \quad (9.7)$$

where $J(i,j)$ is common neighbors plus 1 if $i$ and $j$ are directly connected.

**Step 2: Cluster Similarity**

Three approaches determine community similarity:
- **Single linkage**: minimum $x_{ij}$ between groups
- **Complete linkage**: maximum $x_{ij}$ between groups  
- **Average linkage**: mean $x_{ij}$ (used by Ravasz)

**Step 3: Iterative Merging**

1. Assign each node to its own community
2. Find highest-similarity node/community pair; merge them
3. Recalculate similarities
4. Repeat until all nodes merge

**Step 4: Dendrogram**

A hierarchical tree visualizes the merge sequence. Cutting at different levels yields different partitions.

**Computational Complexity**: $O(N^2)$

### Girvan-Newman Algorithm (Divisive)

Removes high-centrality links connecting different communities.

**Step 1: Define Centrality**

**Link Betweenness**: Number of shortest paths traversing a link. Inter-community links have high betweenness; intra-community links have low betweenness.

**Step 2: Iterative Removal**

1. Calculate link betweenness
2. Remove highest-betweenness link
3. Recalculate betweenness
4. Repeat until all links removed

**Computational Complexity**: $O(L^2 N)$ or $O(N^3)$ for sparse networks

### Hierarchy in Real Networks

**Hierarchical Network Model**: A deterministic model generating nested communities. Start with a fully connected 5-node module; create four replicas and connect peripheral nodes to the central node. Repeat iteratively (Image 9.13).

This model exhibits:

**Scale-Free Property**:
$$\gamma = 1 + \frac{\ln 5}{\ln 4} = 2.161$$

**Size-Independent Clustering**: $C = 0.743$ independent of network size

**Hierarchical Modularity**:
$$C(k) \sim k^{-1} \quad (9.8)$$

High-degree nodes connect different communities (low $C$); low-degree nodes reside in dense communities (high $C$).

---

## Section 9.4: Modularity

### H3: Random Hypothesis

*Randomly wired networks lack inherent community structure.*

Compare actual link density to expected density in randomized networks.

### Modularity Definition

For a partition with $n_c$ communities:
$$M = \sum_{c=1}^{n_c} \left[\frac{L_c}{L} - \left(\frac{k_c}{2L}\right)^2\right] \quad (9.12)$$

where $L_c$ = links within community $c$, $k_c$ = total degree in community $c$.

**Properties**:
- $M = 1$: maximum possible (unrealistic)
- $M = 0$: entire network as one community
- $M < 0$: each node as separate community
- Higher $M$ = better partition

**Resolution Limit**: Modularity maximization merges communities below threshold:
$$k \leq \sqrt{2L} \quad (9.14)$$

Small communities with total degree below this are forced together, regardless of distinctness.

### Greedy Algorithm

Iteratively merge communities maximizing modularity:

1. Each node starts in its own community
2. For each connected community pair, calculate $\Delta M$ if merged
3. Merge pair with largest positive $\Delta M$
4. Record $M$ for each step
5. Select partition with maximum $M$

**Computational Complexity**: $O(N^2)$ or $O(N\log^2 N)$ with optimization

---

## Section 9.5: Overlapping Communities

Nodes often belong to multiple communities (work, family, hobbies). Overlapping community algorithms allow this.

### Clique Percolation (CFinder)

Two $k$-cliques are adjacent if they share $k-1$ nodes. Communities are unions of overlapping cliques.

**Percolation Threshold**: $k$-clique communities emerge above:
$$p_c(k) = \frac{1}{[(k-1)N]^{1/(k-1)}} \quad (9.16)$$

**Computational Complexity**: Exponential in $N$ for finding cliques, but practical for moderate network sizes

### Link Clustering

Clusters links rather than nodes, since links are community-specific.

**Link Similarity**:
$$S((i,k),(j,k)) = \frac{|n_+(i) \cap n_+(j)|}{|n_+(i) \cup n_+(j)|} \quad (9.17)$$

Measures common neighbors of nodes $i$ and $j$.

**Procedure**:
1. Calculate link similarity matrix
2. Apply hierarchical clustering
3. Extract link communities
4. Derive overlapping node communities

---

## Section 9.6: Testing Communities

### Accuracy Benchmarks

**Girvan-Newman Benchmark**: 128 nodes in 4 equal communities. Mixing parameter:
$$\mu = \frac{k^{\text{ext}}}{k^{\text{ext}} + k^{\text{int}}} \quad (9.18)$$

Small $\mu$ = well-separated communities; large $\mu$ = difficult detection.

**Lancichinetti-Fortunato-Radicchi Benchmark**: Power-law degree and community size distributions, more realistic.

**Normalized Mutual Information**:
$$I_n = \frac{\sum_{C_1, C_2} p(C_1, C_2)\log_2 \frac{p(C_1, C_2)}{p(C_1)p(C_2)}}{\frac{1}{2}[H(\{p(C_1)\}) + H(\{p(C_2)\})]} \quad (9.19)$$

where $H(\{p(C)\}) = -\sum_C p(C)\log_2 p(C)$ is Shannon entropy.

- $I_n = 1$: identical partitions
- $I_n = 0$: independent partitions

### Computational Speed

Algorithms vary dramatically in speed:
- **Louvain/Infomap**: $O(L)$ or $O(N\log N)$ — practical for millions of nodes
- **Greedy Modularity**: $O(N^2)$
- **CFinder**: Exponential — slow for large networks

---

## Section 9.7: Characterizing Communities

### Community Size Distribution

Real networks show fat-tailed community size distributions: many small communities coexist with few large ones. Different algorithms may predict different distributions for the same network.

### Link Weights and Communities

**Social Networks**: Strong ties within communities; weak ties between (weak tie hypothesis)

**Transport Systems**: Strong ties between communities (high traffic); weak ties within

### Community Evolution

In social networks:
- **Growth**: Nodes join communities with many existing links
- **Contraction**: Nodes with few community links leave
- **Splitting/Death**: Communities with high external links dissolve
- **Stability**: Larger communities have faster membership change

---

## Section 9.8: Summary

Community identification rests on four hypotheses (Box 9.3):

**Fundamental Hypothesis**: Communities are uniquely encoded in wiring diagrams

**Connectedness and Density Hypothesis**: Communities are locally dense connected subgraphs

**Random Hypothesis**: Random networks lack communities

**Maximal Modularity Hypothesis**: Maximum modularity partition is optimal

Key open questions:
- How do we detect if communities exist without identifying them?
- Must all nodes belong to communities?
- How do communities behave in very dense networks?

Communities demonstrably affect network behavior: information spreads differently within vs. between communities; they influence link weights and correlations. Applications include Web services, marketing, data structure optimization, and social network recommendations.

---

## Section 9.9: Homework

1. Calculate degree exponent for the hierarchical network in Image 9.33
2. Analyze communities on a circle lattice and find optimal partition
3. Show modularity resolution limit prevents detection of small communities
4. Prove modularity maximum cannot exceed 1

---

## Advanced Topics 9.A–9.D

- **9.A**: Derives degree exponent $\gamma = 2.16$ and hierarchical clustering coefficient scaling
- **9.B**: Details modularity derivations
- **9.C**: Describes Louvain algorithm ($O(L)$) and Infomap (entropy-based map equation)
- **9.D**: Derives clique percolation threshold
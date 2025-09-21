# 7️⃣ Measures and Metrics 

<!-- ## Table of Contents

- [7️⃣ Measures and Metrics](#7️⃣-measures-and-metrics)
  - [Table of Contents](#table-of-contents)
  - [Introduction to Network Measures](#introduction-to-network-measures)
  - [Centrality Measures](#centrality-measures)
    - [Degree Centrality](#degree-centrality)
    - [Eigenvector Centrality](#eigenvector-centrality)
    - [Katz Centrality](#katz-centrality)
    - [PageRank](#pagerank)
    - [Hubs and Authorities (HITS)](#hubs-and-authorities-hits)
    - [Closeness Centrality](#closeness-centrality)
    - [Betweenness Centrality](#betweenness-centrality)
  - [Groups and Cohesive Substructures](#groups-and-cohesive-substructures)
    - [Cliques](#cliques)
    - [k-Cores](#k-cores)
    - [k-Components](#k-components)
  - [Transitivity and Clustering](#transitivity-and-clustering)
    - [Global Clustering Coefficient](#global-clustering-coefficient)
    - [Local Clustering](#local-clustering)
    - [Redundancy](#redundancy)
  - [Network Properties](#network-properties)
    - [Reciprocity](#reciprocity)
    - [Signed Networks and Structural Balance](#signed-networks-and-structural-balance)
  - [Similarity and Equivalence](#similarity-and-equivalence)
    - [Structural Equivalence](#structural-equivalence)
    - [Regular Equivalence](#regular-equivalence)
  - [Homophily and Assortative Mixing](#homophily-and-assortative-mixing)
    - [Modularity](#modularity)
    - [Assortativity Coefficient](#assortativity-coefficient)
    - [Degree Assortativity](#degree-assortativity)
  - [Mathematical Reference](#mathematical-reference)
    - [Centrality Measures Summary](#centrality-measures-summary)
    - [Key Matrix Relationships](#key-matrix-relationships)
    - [Network Statistics Formulas](#network-statistics-formulas)
  - [Applications and Case Studies](#applications-and-case-studies)
    - [Social Network Analysis](#social-network-analysis)
    - [Citation Networks](#citation-networks)
    - [Web Networks](#web-networks)
    - [Biological Networks](#biological-networks)
    - [Transportation Networks](#transportation-networks)
  - [Computational Considerations](#computational-considerations)
    - [Scalability Issues](#scalability-issues)
    - [Approximation Methods](#approximation-methods)
    - [Implementation Tips](#implementation-tips)
    - [Software Tools](#software-tools)

--- -->
<!-- 
## Introduction to Network Measures

**Purpose**: Network measures convert complex structural information into interpretable numerical values that capture important properties of networks and individual nodes.

**Historical Context**: Many measures originated in social network analysis (1930s-1960s) but have been adopted across disciplines including computer science, physics, biology, and economics.

**Core Principle**: Transform large volumes of structural data into simple metrics that reveal:
- Node importance and influence
- Community structure
- Information flow patterns
- Network robustness
- Similarity patterns

**Key Categories**:
1. **Node-level measures**: Centrality, clustering, similarity
2. **Edge-level measures**: Reciprocity, structural balance
3. **Network-level measures**: Global clustering, modularity, assortativity

--- -->

## Centrality Measures

Centrality measures identify the most important or influential nodes in a network. Different definitions of "importance" lead to different centrality measures.

### Degree Centrality

**Definition**: The simplest centrality measure based on the number of direct connections.

**Mathematical Formulation**:

**Undirected Networks**:
$$C_D(i) = k_i$$

**Directed Networks**:
- In-degree centrality: $C_D^{in}(i) = k_i^{in}$
- Out-degree centrality: $C_D^{out}(i) = k_i^{out}$

**Normalized Version**:
$$C_D'(i) = \frac{k_i}{n-1}$$

Where $n$ is the total number of nodes.

**Key Properties**:
- Range: $[0, n-1]$ (unnormalized) or $[0, 1]$ (normalized)
- Local measure - only considers immediate neighbors
- Fast computation: $O(m)$ where $m$ is number of edges

**Applications**:
- **Social networks**: Popular individuals (many friends)
- **Citation networks**: Influential papers (highly cited)
- **Web networks**: Important pages (many incoming links)
- **Transportation**: Major hubs (many connections)

**Limitations**:
- Treats all neighbors equally
- Doesn't consider the importance of neighbors
- Purely local view of network position

### Eigenvector Centrality

**Key Insight**: A node's importance should depend on both the number and the importance of its neighbors.

**Mathematical Formulation**:
$$x_i = \kappa^{-1} \sum_{j} A_{ij} x_j$$

**Matrix Form**:
$$\mathbf{Ax} = \kappa \mathbf{x}$$

Where:
- $\mathbf{x}$ is the eigenvector of centrality scores
- $\mathbf{A}$ is the adjacency matrix  
- $\kappa$ is the eigenvalue (largest eigenvalue chosen)

**Perron-Frobenius Theorem**: For adjacency matrices:
- There exists a unique eigenvector with all non-negative components
- This corresponds to the largest eigenvalue
- All components are strictly positive if the graph is connected

**For Directed Networks**:
$$x_i = \kappa^{-1} \sum_j A_{ji} x_j$$

Uses incoming edges to determine centrality.

**Problems in Directed Networks**:
- Nodes with zero in-degree have centrality zero
- Only strongly connected components can have non-zero centrality
- Acyclic networks produce all-zero centrality

**Applications**:
- **Social influence**: People connected to influential people are influential
- **Scientific impact**: Papers cited by important papers are important
- **Web ranking**: Early inspiration for PageRank algorithm

### Katz Centrality

**Motivation**: Solve the zero-centrality problem in directed networks by giving each node a baseline centrality.

**Mathematical Formulation**:
$$x_i = \alpha \sum_j A_{ij} x_j + \beta$$

**Matrix Form**:
$$\mathbf{x} = \alpha \mathbf{Ax} + \beta \mathbf{1}$$

**Solution**:
$$\mathbf{x} = \beta(\mathbf{I} - \alpha \mathbf{A})^{-1}\mathbf{1}$$

With $\beta = 1$:
$$\mathbf{x} = (\mathbf{I} - \alpha \mathbf{A})^{-1}\mathbf{1}$$

**Parameter Constraints**:
- Must have $\alpha < 1/\lambda_1$ where $\lambda_1$ is the largest eigenvalue of $\mathbf{A}$
- If $\alpha \geq 1/\lambda_1$, the series diverges

**Interpretation**:
$$x_i = \beta + \alpha \beta \sum_j A_{ij} + \alpha^2 \beta \sum_j \sum_k A_{ij}A_{jk} + \ldots$$

Each node gets centrality from:
- Base amount: $\beta$
- Immediate neighbors: weighted by $\alpha$
- Two-step neighbors: weighted by $\alpha^2$
- And so on...

**Advantages**:
- Works for directed networks
- All nodes get non-zero centrality
- Considers paths of all lengths with exponential decay

### PageRank

**Motivation**: High-centrality nodes shouldn't pass equal amounts of centrality to all neighbors; centrality should be diluted by out-degree.

**Mathematical Formulation**:
$$x_i = \alpha \sum_j A_{ij} \frac{x_j}{k_j^{out}} + \beta$$

**Matrix Form**:
$$\mathbf{x} = \alpha \mathbf{AD}^{-1}\mathbf{x} + \beta \mathbf{1}$$

**Solution**:
$$\mathbf{x} = \beta(\mathbf{I} - \alpha \mathbf{AD}^{-1})^{-1}\mathbf{1}$$

Where $\mathbf{D}$ is diagonal with $D_{ii} = \max(k_i^{out}, 1)$.

**Random Walk Interpretation**:
- With probability $\alpha$: follow a random outgoing edge
- With probability $1-\alpha$: jump to a random node
- PageRank = stationary probability distribution

**Standard Parameters**:
- $\alpha = 0.85$ (Google's choice)
- $\beta = (1-\alpha)/n$

**Key Properties**:
- Always converges for any $\alpha < 1$
- Handles dangling nodes (zero out-degree)
- Scale-invariant: adding nodes doesn't change relative rankings

**Applications**:
- **Web search**: Original use by Google
- **Social networks**: Influence measurement
- **Citation analysis**: Paper importance
- **Recommendation systems**: Item ranking

### Hubs and Authorities (HITS)

**Concept**: In directed networks, distinguish between two types of important nodes:
- **Authorities**: Contain valuable information (pointed to by many hubs)
- **Hubs**: Point to many valuable authorities

**Mathematical Formulation**:

**Authority centrality**:
$$x_i = \alpha \sum_j A_{ji} y_j$$

**Hub centrality**:
$$y_i = \beta \sum_j A_{ij} x_j$$

**Matrix Form**:
$$\mathbf{x} = \alpha \mathbf{A}^T \mathbf{y}$$
$$\mathbf{y} = \beta \mathbf{A} \mathbf{x}$$

**Eigenvalue Formulation**:
Combining equations:
$$\mathbf{AA}^T \mathbf{x} = \lambda \mathbf{x}$$
$$\mathbf{A}^T\mathbf{A} \mathbf{y} = \lambda \mathbf{y}$$

Where $\lambda = (\alpha\beta)^{-1}$.

**Algorithm**:
1. Initialize $\mathbf{y}^{(0)} = \mathbf{1}$
2. Update authorities: $\mathbf{x}^{(t+1)} = \mathbf{A}^T \mathbf{y}^{(t)}$
3. Update hubs: $\mathbf{y}^{(t+1)} = \mathbf{A} \mathbf{x}^{(t+1)}$
4. Normalize vectors
5. Repeat until convergence

**Applications**:
- **Web search**: Identifying authoritative pages and good hubs
- **Citation networks**: Distinguishing review papers (hubs) from seminal works (authorities)
- **Social networks**: Opinion leaders vs. information brokers

### Closeness Centrality

**Concept**: Measures how close a node is to all other nodes in terms of shortest path distances.

**Mean Distance**:
$$\ell_i = \frac{1}{n-1} \sum_{j \neq i} d_{ij}$$

Where $d_{ij}$ is the shortest path distance from node $i$ to node $j$.

**Closeness Centrality**:
$$C_C(i) = \frac{1}{\ell_i} = \frac{n-1}{\sum_{j \neq i} d_{ij}}$$

**Harmonic Mean Closeness** (handles disconnected networks):
$$C_H(i) = \frac{1}{n-1} \sum_{j \neq i} \frac{1}{d_{ij}}$$

Convention: $1/\infty = 0$ for disconnected pairs.

**Properties**:
- Range: $(0, 1]$ 
- Higher values indicate more central positions
- Requires connected network for standard definition
- $O(n^2)$ or $O(nm)$ computation using BFS

**Applications**:
- **Transportation**: Locations with shortest travel times
- **Communication**: Fastest information spread
- **Supply chains**: Efficient distribution centers
- **Social networks**: Actors who can reach others quickly

**Limitations**:
- Undefined for disconnected networks (standard version)
- Assumes shortest paths are preferred
- All paths weighted equally

### Betweenness Centrality

**Concept**: Measures the extent to which a node lies on the shortest paths between other pairs of nodes.

**Mathematical Formulation**:
$$C_B(i) = \sum_{s \neq i \neq t} \frac{g_{st}(i)}{g_{st}}$$

Where:
- $g_{st}$ = total number of shortest paths from $s$ to $t$
- $g_{st}(i)$ = number of shortest paths from $s$ to $t$ passing through $i$

**Normalized Version**:
$$C_B'(i) = \frac{2}{(n-1)(n-2)} \sum_{s \neq i \neq t} \frac{g_{st}(i)}{g_{st}}$$

**Edge Betweenness**:
$$C_B(e) = \sum_{s,t} \frac{g_{st}(e)}{g_{st}}$$

Where $g_{st}(e)$ is the number of shortest paths from $s$ to $t$ using edge $e$.

**Key Properties**:
- Measures control over information flow
- High betweenness nodes are potential bottlenecks
- Can identify bridge nodes between communities
- Complexity: $O(nm)$ for unweighted graphs (Brandes algorithm)

**Applications**:
- **Social networks**: Brokers who connect different groups
- **Transportation**: Critical junctions that handle traffic
- **Communication**: Nodes that control information flow
- **Biology**: Proteins that mediate between functional modules

**Variations**:
- **Flow betweenness**: Uses maximum flow instead of shortest paths
- **Random walk betweenness**: Based on random walks
- **Current flow betweenness**: Uses electrical network analogy

---

## Groups and Cohesive Substructures

### Cliques

**Definition**: A subset of nodes where every pair is directly connected.

**Mathematical Definition**:
A clique $C$ is a subset of nodes such that for all $i, j \in C$ with $i \neq j$:
$$A_{ij} = 1$$

**Properties**:
- Maximum clique: Largest clique in the network
- Clique number: Size of the maximum clique
- Cliques can overlap (share nodes)
- Complete subgraphs

**Maximal vs. Maximum Cliques**:
- **Maximal clique**: Cannot be extended by adding another node
- **Maximum clique**: Largest possible clique in the network

**Applications**:
- **Social networks**: Tightly-knit groups of friends
- **Biology**: Protein complexes, gene co-expression
- **Market analysis**: Groups of similar products
- **Web**: Clusters of highly-related pages

**Computational Complexity**:
- Finding maximum clique is NP-hard
- Enumerating all maximal cliques: exponential in worst case
- Practical algorithms exist for moderate-sized networks

### k-Cores

**Definition**: A maximal subset of nodes such that each node in the subset has at least $k$ connections to other nodes in the subset.

**Mathematical Definition**:
The $k$-core is the maximal subgraph where every node has degree at least $k$ within the subgraph.

**Core Decomposition Algorithm**:
```
1. Set k = 1
2. While nodes remain:
   a. Remove all nodes with degree < k
   b. Remove their edges
   c. If no nodes removed, increment k
3. Nodes removed at step k form the (k-1)-core shell
```

**Core Number**: 
The core number $c(i)$ of node $i$ is the largest $k$ such that $i$ belongs to the $k$-core.

**Properties**:
- Nested structure: $(k+1)$-core $\subseteq$ $k$-core
- Unique decomposition of network into shells
- Core nodes vs. peripheral nodes
- Linear time algorithm: $O(m)$

**Applications**:
- **Network visualization**: Onion-like structure
- **Community detection**: Core-periphery organization
- **Robustness**: High $k$-core nodes are more robust
- **Influence**: Core nodes often have high influence

**k-Shell**: Nodes with core number exactly $k$ (removed at step $k+1$).

### k-Components

**Definition**: A maximal subset of nodes such that every pair of nodes in the subset is connected by at least $k$ node-disjoint paths.

**Mathematical Definition**:
The $k$-component is a maximal subgraph with vertex connectivity at least $k$.

**Vertex Connectivity**: Minimum number of nodes whose removal disconnects two specific nodes.

**Properties**:
- Nested structure like $k$-cores
- Related to network fault tolerance
- Higher $k$ indicates stronger internal connectivity
- Can have multiple disconnected $k$-components

**Special Cases**:
- $1$-component: Connected component
- $2$-component: Bicomponent (no single point of failure)
- $3$-component: Tricomponent

**Applications**:
- **Robustness analysis**: Fault-tolerant subnetworks  
- **Social cohesion**: Groups that remain connected despite removals
- **Infrastructure**: Critical system components
- **Biology**: Resilient functional modules

**Relationship to k-Cores**:
- $k$-cores: Local property (degree-based)
- $k$-components: Global property (connectivity-based)
- $k$-component $\subseteq$ $k$-core (but not vice versa)

---

## Transitivity and Clustering

### Global Clustering Coefficient

**Concept**: Measures the tendency for networks to form triangles - "the friend of my friend is my friend."

**Definition 1 (Transitivity)**:
$$C = \frac{3 \times \text{number of triangles}}{\text{number of connected triples}}$$

**Definition 2 (Path-based)**:
$$C = \frac{\text{number of closed paths of length 2}}{\text{number of paths of length 2}}$$

**Matrix Formulation**:
$$C = \frac{\text{Tr}(\mathbf{A}^3)}{\text{Tr}(\mathbf{A}^2) - \text{Tr}(\mathbf{A})}$$

Where $\text{Tr}(\mathbf{A}^3)$ counts closed triangles and $\text{Tr}(\mathbf{A}^2)$ counts all length-2 paths.

**Connected Triple**: Three nodes connected by two edges (path of length 2).
**Closed Triple**: Three nodes forming a triangle.

**Properties**:
- Range: $C \in [0, 1]$
- $C = 1$: All connected triples form triangles (complete graph)
- $C = 0$: No triangles (e.g., trees, bipartite graphs)

**Typical Values by Network Type**:
- **Social networks**: $C = 0.1$ to $0.6$
- **Biological networks**: $C = 0.05$ to $0.3$
- **Technological networks**: $C \approx 0.01$ to $0.1$
- **Random networks**: $C = p$ (edge probability)

### Local Clustering

**Local Clustering Coefficient**:
$$C_i = \frac{\text{number of edges between neighbors of } i}{\text{number of possible edges between neighbors of } i} = \frac{2e_i}{k_i(k_i-1)}$$

Where $e_i$ is the number of edges between neighbors of node $i$.

**Alternative Definition**:
$$C_i = \frac{1}{\binom{k_i}{2}} \sum_{j,k} A_{ij}A_{ik}A_{jk}$$

**Watts-Strogatz Clustering**:
Average local clustering across all nodes:
$$C_{WS} = \frac{1}{n} \sum_{i=1}^n C_i$$

**Properties**:
- $C_i \in [0, 1]$
- $C_i = 1$: All neighbors of $i$ are connected (complete neighborhood)
- $C_i = 0$: No edges between neighbors of $i$
- Undefined for nodes with degree $< 2$

### Redundancy

**Definition**: Average number of connections each neighbor of node $i$ has to other neighbors of $i$.

**Mathematical Formulation**:
$$R_i = \frac{1}{k_i} \sum_{j \in N(i)} \sum_{k \in N(i), k \neq j} A_{jk}$$

Where $N(i)$ is the set of neighbors of node $i$.

**Relationship to Local Clustering**:
$$C_i = \frac{R_i}{k_i - 1}$$

**Applications**:
- **Structural holes**: Low $C_i$ indicates brokerage position
- **Information control**: Non-redundant connections provide advantage
- **Social capital**: Bridge different communities
- **Network efficiency**: High redundancy may indicate inefficiency

---

## Network Properties

### Reciprocity

**Concept**: In directed networks, the tendency for edges to be mutual (bidirectional).

**Definition**: Fraction of edges that are reciprocated.

**Mathematical Formulation**:
$$r = \frac{1}{m} \sum_{i,j} A_{ij} A_{ji} = \frac{1}{m} \text{Tr}(\mathbf{A}^2)$$

Where $m$ is the total number of directed edges.

**Alternative Definition** (fraction of node pairs):
$$r' = \frac{2 \times \text{number of bidirectional edges}}{\text{total number of connected pairs}}$$

**Properties**:
- Range: $r \in [0, 1]$
- $r = 0$: No reciprocal edges (completely asymmetric)
- $r = 1$: All edges are reciprocal (symmetric network)

**Typical Values**:
- **Web networks**: $r \approx 0.3$ to $0.5$
- **Email networks**: $r \approx 0.2$ to $0.7$
- **Citation networks**: $r \approx 0.01$ to $0.05$ (naturally asymmetric)
- **Social networks**: $r \approx 0.4$ to $0.8$

**Applications**:
- **Communication**: Measure of two-way interaction
- **Trade**: Bilateral vs. unilateral relationships
- **Trust**: Mutual vs. one-way trust relationships

### Signed Networks and Structural Balance

**Concept**: Networks where edges represent positive (friendship, alliance) or negative (enmity, opposition) relationships.

**Signed Adjacency Matrix**:
$$A_{ij} = \begin{cases} 
+1 & \text{if positive edge from } i \text{ to } j \\
-1 & \text{if negative edge from } i \text{ to } j \\
0 & \text{if no edge}
\end{cases}$$

**Structural Balance Theory**:
A triangle is **balanced** if it has an even number of negative edges.

**Triangle Types**:
1. $(+,+,+)$: All friends - **BALANCED**
2. $(+,-,-)$: Two friends against common enemy - **BALANCED**
3. $(+,+,-)$: Two friends, one enemy - **UNBALANCED**
4. $(-,-,-)$: All enemies - **UNBALANCED** (debatable)

**Balance Score**:
$$B = \frac{\text{number of balanced triangles}}{\text{total number of triangles}}$$

**Harary's Structure Theorem**:
A complete signed graph is balanced if and only if its nodes can be partitioned into two groups such that:
- All edges within groups are positive
- All edges between groups are negative

**Generalized Balance** (Davis):
Allow multiple groups where:
- Intra-group edges are positive
- Inter-group edges are negative

**Applications**:
- **International relations**: Alliance patterns
- **Social groups**: Friendship/enmity dynamics  
- **Opinion formation**: Agreement/disagreement patterns
- **Gene regulation**: Activation/inhibition networks

---

## Similarity and Equivalence

### Structural Equivalence

**Concept**: Two nodes are structurally equivalent if they have identical connection patterns to all other nodes.

**Perfect Structural Equivalence**:
Nodes $i$ and $j$ are structurally equivalent if:
$$A_{ik} = A_{jk} \text{ and } A_{ki} = A_{kj} \text{ for all } k$$

**Similarity Measures**:

**Number of Common Neighbors**:
$$s_{ij} = \sum_k A_{ik} A_{jk}$$

**Cosine Similarity**:
$$\sigma_{ij} = \frac{s_{ij}}{\sqrt{k_i k_j}} = \frac{\sum_k A_{ik} A_{jk}}{\sqrt{k_i k_j}}$$

**Jaccard Coefficient**:
$$J_{ij} = \frac{s_{ij}}{k_i + k_j - s_{ij}}$$

**Pearson Correlation**:
$$\rho_{ij} = \frac{\sum_k (A_{ik} - \bar{A_i})(A_{jk} - \bar{A_j})}{\sqrt{\sum_k (A_{ik} - \bar{A_i})^2 \sum_k (A_{jk} - \bar{A_j})^2}}$$

**Properties**:
- Range: $[0, 1]$ for cosine and Jaccard
- Range: $[-1, 1]$ for correlation
- Symmetric: $\sigma_{ij} = \sigma_{ji}$
- Based only on direct neighbors

### Regular Equivalence

**Concept**: Two nodes are regularly equivalent if they connect to equivalent sets of other nodes (recursive definition).

**Katz-like Similarity**:
$$\sigma_{ij} = \beta \delta_{ij} + \alpha \sum_k A_{ik} \sigma_{kj}$$

**Matrix Form**:
$$\mathbf{\Sigma} = \beta \mathbf{I} + \alpha \mathbf{A} \mathbf{\Sigma}$$

**Solution**:
$$\mathbf{\Sigma} = \beta(\mathbf{I} - \alpha \mathbf{A})^{-1}$$

**Degree-Normalized Version**:
$$\mathbf{\Sigma} = \beta(\mathbf{D} - \alpha \mathbf{A})^{-1}$$

**Interpretation**:
- Considers paths of all lengths between nodes
- Longer paths have exponentially decreasing weight $\alpha^l$
- Captures indirect similarity through network structure

**Applications**:
- **Role analysis**: Nodes with similar structural positions
- **Link prediction**: Nodes likely to form connections
- **Recommendation**: Similar users or items
- **Biology**: Functionally similar genes or proteins

---

## Homophily and Assortative Mixing

**Homophily**: The tendency for similar nodes to be connected ("birds of a feather flock together").

### Modularity

**For Categorical Attributes** (unordered):

**Modularity**:
$$Q = \frac{1}{2m} \sum_{ij} \left(A_{ij} - \frac{k_i k_j}{2m}\right) \delta(g_i, g_j)$$

Where:
- $\delta(g_i, g_j) = 1$ if nodes $i$ and $j$ belong to the same group
- $k_i k_j / 2m$ is the expected number of edges under random mixing

**Alternative Form**:
$$Q = \sum_r (e_r - a_r^2)$$

Where:
- $e_r$ = fraction of edges within group $r$
- $a_r$ = fraction of edge endpoints in group $r$

**Properties**:
- Range: $Q \in [-1, 1]$ (practical range often $[0, 0.3]$ to $[0.7]$)
- $Q > 0$: Assortative mixing (more within-group connections)
- $Q < 0$: Disassortative mixing (fewer within-group connections)
- $Q = 0$: Random mixing

### Assortativity Coefficient

**For Continuous Attributes** (ordered):

**Assortativity Coefficient**:
$$r = \frac{\sum_{ij} (A_{ij} - k_i k_j/2m) x_i x_j}{\sum_{ij} (k_i \delta_{ij} - k_i k_j/2m) x_i x_j}$$

Where $x_i$ is the attribute value for node $i$.

**Pearson Correlation Form**:
$$r = \frac{\text{Cov}(X_i, X_j)}{\sqrt{\text{Var}(X_i)\text{Var}(X_j)}}$$

Where the covariance and variance are computed over all edges.

**Properties**:
- Range: $r \in [-1, 1]$
- $r = 1$: Perfect positive assortativity
- $r = -1$: Perfect negative assortativity  
- $r = 0$: No correlation

### Degree Assortativity

**Special Case**: Assortativity with respect to node degree.

**Degree Assortativity Coefficient**:
$$r = \frac{\sum_{ij} (A_{ij} - k_i k_j/2m) k_i k_j}{\sum_{ij} (k_i \delta_{ij} - k_i k_j/2m) k_i k_j}$$

**Simplified Form**:
$$r = \frac{2m \sum_{ij} A_{ij} k_i k_j - \left(\sum_{ij} A_{ij}(k_i + k_j)\right)^2}{2m \sum_{ij} A_{ij}(k_i^2 + k_j^2) - \left(\sum_{ij} A_{ij}(k_i + k_j)\right)^2}$$

**Network Types**:

**Assortative Networks** ($r > 0$):
- High-degree nodes connect to high-degree nodes
- Creates "rich club" effect
- Common in social networks
- Leads to core-periphery structure

**Disassortative Networks** ($r < 0$):
- High-degree nodes connect to low-degree nodes
- Creates star-like or hub-spoke structures
- Common in technological and biological networks
- More efficient for spreading processes

**Typical Values**:
- **Social networks**: $r = 0.1$ to $0.3$ (assortative)
- **Internet**: $r = -0.2$ (disassortative)
- **Protein networks**: $r = -0.1$ to $-0.3$ (disassortative)
- **Neural networks**: $r = -0.1$ to $-0.2$ (disassortative)

---

## Mathematical Reference

### Centrality Measures Summary

| **Measure** | **Formula** | **Complexity** |
|-------------|-------------|----------------|
| Degree | $C_D(i) = k_i$ | $O(m)$ |
| Eigenvector | $\mathbf{Ax} = \lambda \mathbf{x}$ | $O(n^3)$ or iterative |
| Katz | $\mathbf{x} = (\mathbf{I} - \alpha \mathbf{A})^{-1}\mathbf{1}$ | $O(n^3)$ or iterative |
| PageRank | $\mathbf{x} = (\mathbf{I} - \alpha \mathbf{AD}^{-1})^{-1}\mathbf{1}$ | $O(n^3)$ or iterative |
| Closeness | $C_C(i) = (n-1)/\sum_j d_{ij}$ | $O(nm)$ |
| Betweenness | $C_B(i) = \sum_{st} g_{st}(i)/g_{st}$ | $O(nm)$ |

### Key Matrix Relationships

**Adjacency Matrix Powers**:
- $[\mathbf{A}^2]_{ij}$ = number of length-2 paths from $i$ to $j$
- $[\mathbf{A}^k]_{ij}$ = number of length-$k$ paths from $i$ to $j$
- $\text{Tr}(\mathbf{A}^3) = 6 \times$ number of triangles

**Spectral Properties**:
- Largest eigenvalue $\lambda_1$ relates to connectivity
- Eigenvector centrality uses leading eigenvector
- Spectral gap affects convergence rates

### Network Statistics Formulas

| **Property** | **Formula** |
|--------------|-------------|
| Clustering | $C = 3 \times \text{triangles}/\text{connected triples}$ |
| Reciprocity | $r = \text{Tr}(\mathbf{A}^2)/m$ |
| Modularity | $Q = \frac{1}{2m} \sum_{ij} (A_{ij} - k_i k_j/2m) \delta(g_i, g_j)$ |
| Assortativity | $r = \frac{\text{Cov}(X_i, X_j)}{\sqrt{\text{Var}(X_i)\text{Var}(X_j)}}$ |

---

## Applications and Case Studies

### Social Network Analysis

**Facebook Friendship Networks**:
- High clustering coefficient ($C \approx 0.2$)
- Positive degree assortativity ($r \approx 0.2$)
- Strong homophily by age, location, education

**Twitter Following Networks**:
- Lower clustering than Facebook ($C \approx 0.1$)
- Clear hub structure (celebrities, media)
- Significant reciprocity patterns

**Professional Networks (LinkedIn)**:
- Moderate clustering
- Homophily by industry, location
- Important brokers bridge different sectors

### Citation Networks

**Scientific Paper Citations**:
- Very low clustering ($C < 0.01$)
- Strong negative degree assortativity
- Clear authority/hub structure
- Temporal constraints (can't cite future papers)

**Applications of Centrality**:
- **PageRank**: Identify influential papers
- **Betweenness**: Find interdisciplinary papers
- **Hub/Authority**: Distinguish reviews from seminal works

### Web Networks

**World Wide Web**:
- Scale-free degree distribution
- Small-world properties
- Low clustering coefficient
- Bow-tie structure

**Page Ranking**:
- PageRank revolutionized web search
- Handles link spam better than simple degree
- Considers authority transfer through links

### Biological Networks

**Protein-Protein Interaction**:
- Modular structure (high modularity)
- Scale-free degree distribution
- High clustering within functional modules
- Negative degree assortativity

**Gene Regulatory Networks**:
- Hierarchical structure
- Few master regulators (high betweenness)
- Feed-forward motifs common

### Transportation Networks

**Airport Networks**:
- Small-world properties
- Hub airports with high betweenness
- Geographic constraints affect structure
- Assortative by airport size

**Road Networks**:
- Planar structure (geographic embedding)
- High clustering (local connectivity)
- Different centrality measures identify different types of important locations

---

## Computational Considerations

### Scalability Issues

**Large Network Challenges**:
- Memory requirements for adjacency matrices: $O(n^2)$
- Sparse representations essential for real networks
- Approximation algorithms needed for very large networks

**Complexity Analysis**:
- **Degree centrality**: $O(m)$ - always feasible
- **Betweenness centrality**: $O(nm)$ - challenging for large networks
- **Eigenvector-based measures**: Iterative methods preferred

### Approximation Methods

**Sampling Approaches**:
- **Betweenness**: Sample subset of shortest path pairs
- **Clustering**: Estimate using local samples
- **Centrality**: Use network sampling techniques

**Iterative Algorithms**:
- **Power method**: For eigenvector centrality, PageRank
- **HITS**: Alternating updates for hubs and authorities
- **Convergence**: Monitor relative changes in centrality scores

### Implementation Tips

**Data Structures**:
- Adjacency lists for sparse networks
- Compressed sparse row (CSR) format
- Edge lists for simple algorithms

**Optimization**:
- Exploit network sparsity
- Use parallel algorithms when possible
- Cache intermediate results (e.g., shortest paths)
- Consider network decomposition for very large networks

### Software Tools

**Popular Packages**:
- **NetworkX** (Python): Comprehensive network analysis
- **igraph** (R/Python): Efficient implementations
- **SNAP** (C++): Stanford large network analysis
- **Gephi**: Interactive network visualization

**Performance Considerations**:
- Choose tools based on network size
- Consider distributed computing for massive networks
- GPU acceleration for certain algorithms
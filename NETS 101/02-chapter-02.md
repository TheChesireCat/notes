# 🎨 Graph Theory

## Historical Foundation

### The Bridges of Königsberg (1735)
The birth of graph theory can be traced to a single problem in Königsberg, Eastern Prussia. The city had seven bridges connecting four land areas across the river Pregel.

**The Problem**: Can one walk across all seven bridges exactly once and return to the starting point?

**Euler's Solution**: Leonard Euler proved this was impossible by:
1. Representing each land area as a node (A, B, C, D)
2. Representing each bridge as a link between nodes
3. Observing that nodes with odd degree must be starting or ending points
4. Since all four nodes had odd degree, no such path could exist

**Key Insight**: Network properties are encoded in their structure, independent of our ability to find solutions.

---

## Basic Network Definitions

### Fundamental Components
- **Network/Graph**: A system representation showing components and their interactions
- **Nodes/Vertices**: Individual components of the system
- **Links/Edges**: Direct interactions between components

### Network Parameters
- **Size ($N$)**: Number of nodes in the network
- **Links ($L$)**: Total number of connections between nodes

### Network Types

#### Directed vs Undirected Networks
- **Undirected**: Links have no specified direction (e.g., friendship, power grid)
- **Directed**: Links have a specific direction (e.g., WWW links, phone calls)

#### Network Characteristics
- **Simple Graph**: No multiple links between same node pairs
- **Multigraph**: Multiple links allowed between nodes
- **Self-loops**: Nodes can connect to themselves
- **Weighted Network**: Links have associated weights/strengths

---

## Degree and Degree Distribution

### Node Degree
For undirected networks, the degree $k_i$ of node $i$ represents the number of links connected to that node.

**Total Links Formula**:
$$L = \frac{1}{2}\sum_{i=1}^N k_i$$

The factor $\frac{1}{2}$ corrects for double counting each link.

### Average Degree
$$\langle k \rangle = \frac{1}{N}\sum_{i=1}^N k_i = \frac{2L}{N}$$

### Directed Networks
- **In-degree** ($k_i^{in}$): Number of incoming links
- **Out-degree** ($k_i^{out}$): Number of outgoing links  
- **Total degree**: $k_i = k_i^{in} + k_i^{out}$

For directed networks:
$$L = \sum_{i=1}^N k_i^{in} = \sum_{i=1}^N k_i^{out}$$

$$\langle k^{in} \rangle = \langle k^{out} \rangle = \frac{L}{N}$$

### Degree Distribution
The degree distribution $p_k$ gives the probability that a randomly selected node has degree $k$.

**Normalization**: $\sum_{k=0}^{\infty} p_k = 1$

**Formula**: $p_k = \frac{N_k}{N}$ where $N_k$ is the number of nodes with degree $k$

**Average degree from distribution**: $\langle k \rangle = \sum_{k=0}^{\infty} k p_k$

---

## Adjacency Matrix Representation

### Definition
The adjacency matrix $A$ is an $N \times N$ matrix where:
- $A_{ij} = 1$ if there is a link from node $j$ to node $i$
- $A_{ij} = 0$ otherwise

### Properties
- **Undirected networks**: $A_{ij} = A_{ji}$ (symmetric matrix)
- **Directed networks**: Generally $A_{ij} \neq A_{ji}$

### Degree Calculations from Adjacency Matrix

**Undirected networks**:
$$k_i = \sum_{j=1}^N A_{ij} = \sum_{j=1}^N A_{ji}$$

**Directed networks**:
$$k_i^{in} = \sum_{j=1}^N A_{ij}, \quad k_i^{out} = \sum_{j=1}^N A_{ji}$$

**Total links**: $2L = \sum_{i,j=1}^N A_{ij}$ (for undirected networks)

---

## Network Sparsity

### Complete Graphs
A complete graph connects every node to every other node.
**Maximum possible links**: $L_{max} = \frac{N(N-1)}{2}$

### Sparse Networks
Real networks are sparse: $L \ll L_{max}$

**Consequences**:
- Adjacency matrices are mostly zeros
- More efficient to store link lists rather than full matrices
- Enables efficient algorithms for large networks

---

## Weighted Networks

### Definition
In weighted networks, each link $(i,j)$ has an associated weight $w_{ij}$.

**Weighted adjacency matrix**: $A_{ij} = w_{ij}$

### Metcalfe's Law
**Statement**: The value of a network is proportional to $N^2$

**Reasoning**: 
- Cost grows linearly with $N$
- Benefits grow with number of possible connections $\sim N^2$
- Predicts profitability threshold

**Limitations**:
- Real networks are sparse ($L \ll N^2$)
- Not all links have equal value

---

## Bipartite Networks

### Definition
A bipartite network has nodes divided into two disjoint sets $U$ and $V$ such that links only connect nodes from different sets.

### Projections
From any bipartite network, we can create two projections:
1. **U-projection**: Connect two $U$-nodes if they link to the same $V$-node
2. **V-projection**: Connect two $V$-nodes if they link to the same $U$-node

### Examples
- **Actor-Movie Network**: Actors connected through shared movies
- **Disease-Gene Network**: Diseases connected through shared associated genes
- **Recipe-Ingredient-Compound Network**: Tripartite network linking recipes, ingredients, and flavor compounds

---

## Paths and Distances

### Path Definitions
- **Path**: A sequence of nodes connected by links
- **Path length**: Number of links in the path
- **Shortest path/Distance** ($d_{ij}$): Path with minimum number of links between nodes $i$ and $j$

### Key Distance Measures

#### Network Diameter
$$d_{max} = \max_{i,j} d_{ij}$$
The longest shortest path in the network.

#### Average Path Length
$$\langle d \rangle = \frac{1}{N(N-1)} \sum_{i,j=1,N; i \neq j} d_{ij}$$

### Path Counting from Adjacency Matrix
- **Distance 1**: $A_{ij} = 1$ if directly connected
- **Distance 2**: Number of 2-paths = $[A^2]_{ij}$
- **Distance $d$**: Number of $d$-paths = $[A^d]_{ij}$

### Breadth-First Search (BFS) Algorithm
**Steps**:
1. Start at source node, label it "0"
2. Find neighbors, label them "1", add to queue
3. For each node with label $n$ in queue, label unlabeled neighbors "$n+1$"
4. Continue until target found or queue empty
5. Distance = final label of target node

**Complexity**: $O(N + L)$ - linear in network size

---

## Network Connectedness

### Connected Components
- **Connected**: Path exists between every pair of nodes
- **Disconnected**: At least one pair has $d_{ij} = \infty$
- **Component**: Maximal set of mutually connected nodes
- **Bridge**: Link whose removal disconnects the network

### Component Identification
Use BFS algorithm:
1. Start from random node, find all reachable nodes (component 1)
2. If unlabeled nodes remain, start from unlabeled node (component 2)
3. Repeat until all nodes labeled

### Matrix Representation
Disconnected networks have block-diagonal adjacency matrices with each block representing a component.

---

## Clustering Coefficient

### Local Clustering Coefficient
For node $i$ with degree $k_i$:
$$C_i = \frac{2L_i}{k_i(k_i-1)}$$

where $L_i$ is the number of links between $i$'s neighbors.

**Interpretation**: 
- $C_i = 0$: No links between neighbors
- $C_i = 1$: All neighbors are connected (complete local graph)
- $C_i$ = probability that two neighbors of node $i$ are connected

### Average Clustering Coefficient
$$\langle C \rangle = \frac{1}{N} \sum_{i=1}^N C_i$$

Represents the probability that two neighbors of a randomly selected node are connected.

### Global Clustering Coefficient
$$C_\Delta = \frac{3 \times \text{Number of Triangles}}{\text{Number of Connected Triplets}}$$

where connected triplets are ordered sets ABC with A-B and B-C connections.

**Note**: $\langle C \rangle \neq C_\Delta$ in general

---

## Key Network Properties Summary

### Canonical Network Datasets

| Network | Type | N | L | $\langle k \rangle$ |
|---------|------|---|---|-------------------|
| Internet | Undirected | 192,244 | 609,066 | 6.34 |
| WWW | Directed | 325,729 | 1,497,134 | 4.60 |
| Power Grid | Undirected | 4,941 | 6,594 | 2.67 |
| Email | Directed | 57,194 | 103,731 | 1.81 |
| Protein Interactions | Undirected | 2,018 | 2,930 | 2.90 |

### Important Statistical Measures

**Basic Statistics Review**:
- **Average**: $\langle x \rangle = \frac{1}{N}\sum_{i=1}^N x_i$
- **$n$th moment**: $\langle x^n \rangle = \frac{1}{N}\sum_{i=1}^N x_i^n$
- **Standard deviation**: $\sigma_x = \sqrt{\frac{1}{N}\sum_{i=1}^N (x_i - \langle x \rangle)^2}$
- **Distribution**: $p_x = \frac{1}{N}\sum_i \delta_{x,x_i}$ with $\sum_x p_x = 1$

### Real Network Characteristics
- Most real networks are **sparse** and **connected**
- Often exhibit **small world** property (short average path lengths)
- May show **scale-free** degree distributions
- Display significant **local clustering**
- Can have **hierarchical** structure with degree-dependent clustering

---

## Applications and Extensions

### Network Analysis Tools
- **BFS**: Finding shortest paths and components
- **Adjacency matrices**: Mathematical analysis and path counting  
- **Degree distributions**: Understanding network heterogeneity
- **Clustering coefficients**: Measuring local network density

### Real-World Applications
- **Social networks**: Friendship, collaboration, communication patterns
- **Biological networks**: Protein interactions, metabolic pathways, disease relationships
- **Technological networks**: Internet topology, power grids, transportation
- **Information networks**: Web structure, citation networks, knowledge graphs

### Important Network Types
- **Regular networks**: All nodes have same degree
- **Random networks**: Links placed randomly
- **Small-world networks**: High clustering + short paths
- **Scale-free networks**: Power-law degree distributions
- **Hierarchical networks**: Nested community structure
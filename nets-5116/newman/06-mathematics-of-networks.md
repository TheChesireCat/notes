---
subject: NETS 5116 · Newman ch. 6
short_title: Ch. 6 · Mathematics of networks
---

# 6️⃣ Mathematics of Networks 
<!-- 
## Table of Contents

1. [Introduction](#introduction)
2. [Networks and Their Representation](#networks-and-their-representation)
3. [The Adjacency Matrix](#the-adjacency-matrix)
4. [Weighted Networks](#weighted-networks)
5. [Directed Networks](#directed-networks)
6. [Hypergraphs](#hypergraphs)
7. [Bipartite Networks](#bipartite-networks)
8. [Multilayer and Dynamic Networks](#multilayer-and-dynamic-networks)
9. [Trees](#trees)
10. [Planar Networks](#planar-networks)
11. [Degree](#degree)
12. [Walks and Paths](#walks-and-paths)
13. [Components](#components)
14. [Independent Paths, Connectivity, and Cut Sets](#independent-paths-connectivity-and-cut-sets)
15. [The Graph Laplacian](#the-graph-laplacian)
16. [Key Formulas Summary](#key-formulas-summary)
17. [Important Theorems](#important-theorems) -->

<!-- ## Introduction

This chapter introduces the fundamental mathematical tools from graph theory needed to analyze networks quantitatively. These concepts form the foundation for understanding network structure, dynamics, and applications across various domains.

**Key Learning Objectives:**
- Understand mathematical representations of networks
- Master adjacency matrices and their properties
- Learn about different network types and their characteristics
- Apply mathematical concepts to real-world network problems -->

## Networks and Their Representation

### Basic Definitions

A **network** (or **graph**) consists of:
- **Nodes** (or **vertices**): Individual elements in the network
- **Edges**: Connections between nodes

### Common Network Examples

| Network Type | Node | Edge |
|--------------|------|------|
| Internet | Computer or router | Cable or wireless connection |
| World Wide Web | Web page | Hyperlink |
| Citation network | Article/patent/legal case | Citation |
| Power grid | Generating station/substation | Transmission line |
| Friendship network | Person | Friendship |
| Metabolic network | Metabolite | Metabolic reaction |
| Neural network | Neuron | Synapse |
| Food web | Species | Predation |

### Network Classifications

**Simple Networks:**
- No multiedges (multiple edges between same pair of nodes)
- No self-edges (edges connecting a node to itself)

**Complex Networks:**
- May contain multiedges and/or self-edges
- More general representation of real-world systems

## The Adjacency Matrix

### Definition

For an undirected simple network with $n$ nodes labeled $1, 2, \ldots, n$, the **adjacency matrix** $A$ is an $n \times n$ matrix with elements:

$$A_{ij} = \begin{cases} 
1 & \text{if there is an edge between nodes } i \text{ and } j \\
0 & \text{otherwise}
\end{cases}$$

### Properties of Adjacency Matrices

1. **Symmetric**: For undirected networks, $A_{ij} = A_{ji}$
2. **Diagonal elements**: Zero for simple networks (no self-edges)
3. **Binary entries**: Elements are 0 or 1 for simple networks

### Example

For a simple 6-node network:

$$A = \begin{pmatrix}
0 & 1 & 0 & 0 & 1 & 0 \\
1 & 0 & 1 & 1 & 0 & 0 \\
0 & 1 & 0 & 1 & 1 & 1 \\
0 & 1 & 1 & 0 & 0 & 0 \\
1 & 0 & 1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 & 0
\end{pmatrix}$$

### Representing Complex Networks

**Multiedges**: Matrix element $A_{ij}$ equals the multiplicity of edges between nodes $i$ and $j$

**Self-edges**: Diagonal element $A_{ii} = 2$ for a single self-edge (counts both ends of the edge)

## Weighted Networks

### Definition

Networks where edges have **weights** or **strengths** representing:
- Data flow capacity
- Energy flow
- Frequency of contact
- Physical distances

### Weighted Adjacency Matrix

Matrix elements $A_{ij}$ equal the weights of edges (not just 0 or 1).

### Example

$$A = \begin{pmatrix} 
0 & 2 & 1 \\ 
2 & 0 & 0.5 \\ 
1 & 0.5 & 0 
\end{pmatrix}$$

This represents a network where the connection between nodes 1 and 2 is twice as strong as that between 1 and 3.

### Edge Weights vs. Edge Lengths

- **Weights**: Stronger connections have higher values
- **Lengths**: Closer connections have lower values
- Often inversely related: length $\propto 1/\text{weight}$

## Directed Networks

### Definition

**Directed networks** (digraphs) have edges with specific directions, represented by arrows.

### Adjacency Matrix for Directed Networks

$$A_{ij} = \begin{cases} 
1 & \text{if there is an edge from } j \text{ to } i \\
0 & \text{otherwise}
\end{cases}$$

**Note**: Edge runs from second index to first index ($j \to i$)

### Properties

1. **Asymmetric**: Generally $A_{ij} \neq A_{ji}$
2. **Self-edges**: Represented by $A_{ii} = 1$ (not 2 as in undirected case)

### Acyclic Networks

**Cycle**: Closed loop where all edges point the same way around the loop

**Acyclic network**: Contains no cycles (also called DAG - Directed Acyclic Graph)

#### Key Properties of Acyclic Networks:
- Can be drawn with all edges pointing "downward"
- Adjacency matrix is **upper triangular** when nodes are properly ordered
- Examples: Citation networks, genealogical trees

#### Algorithm to Test for Acyclicity:
1. Find a node with no outgoing edges
2. If none exists → network is cyclic
3. Remove the node and its incoming edges
4. Repeat until all nodes removed → network is acyclic

## Hypergraphs

### Definition

**Hypergraph**: Network where edges (called **hyperedges**) can connect more than two nodes simultaneously.

### Applications

- Family networks (families with multiple members)
- Collaboration networks (multiple authors per paper)
- Social events (multiple participants per event)

### Representation

While mathematically elegant, hypergraphs are less commonly used in practice. Most analyses convert them to **bipartite networks** for easier computation.

## Bipartite Networks

### Definition

**Bipartite network**: Network with two types of nodes where edges only run between nodes of different types.

### Common Examples

| Network | Type 1 Nodes | Type 2 Nodes | Edge Meaning |
|---------|--------------|--------------|--------------|
| Film actors | Actors | Films | Actor appeared in film |
| Scientific collaboration | Authors | Papers | Author wrote paper |
| Recommender systems | Users | Products | User likes product |
| Board networks | Directors | Companies | Director serves on board |

### Mathematical Representation

**Incidence Matrix** $B$ ($g \times n$ matrix):

$$B_{ij} = \begin{cases} 
1 & \text{if item } j \text{ belongs to group } i \\
0 & \text{otherwise}
\end{cases}$$

### One-Mode Projections

Convert bipartite network to single-node-type network:

**Unweighted projection**: Connect two nodes if they share at least one common group

**Weighted projection**: Edge weight = number of common groups

#### Mathematical Formula

Weighted projection matrix: $P = B^T B$
- Off-diagonal elements: $P_{ij}$ = number of groups shared by nodes $i$ and $j$
- Diagonal elements: $P_{ii}$ = number of groups containing node $i$

## Multilayer and Dynamic Networks

### Multilayer Networks

**Structure**: Set of individual networks (layers) plus interlinking edges between layers

**Example**: Transportation network with layers for:
- Airlines (airports + flights)
- Trains (stations + routes)  
- Buses (stops + routes)
- Interlayer edges connect nearby stations/stops

### Multiplex Networks

**Special case**: Same nodes appear in each layer, different edge types

**Examples**:
- Social networks: friendship layer + family layer + work layer
- Communication networks: email layer + phone layer + text layer

### Dynamic/Temporal Networks

**Structure**: Network snapshots at different time points

**Representation**: Sequence of adjacency matrices $A^{(1)}, A^{(2)}, \ldots, A^{(T)}$

**Mathematical Representation**: 
- Multiplex: Set of $n \times n$ matrices $A^a$ for each layer $a$
- Multilayer: Adjacency matrices $A^a$ (possibly different sizes) plus interlayer matrices $B^{\alpha\beta}$

## Trees

### Definition

**Tree**: Connected, undirected network with no loops (cycles)

### Properties

1. **Unique paths**: Exactly one path between any pair of nodes
2. **Edge count**: Tree with $n$ nodes has exactly $n-1$ edges
3. **Planarity**: All trees are planar networks

### Key Characteristics

- **Connected**: Every node reachable from every other
- **Acyclic**: No closed loops
- **Minimal connectivity**: Removing any edge disconnects the network
- **Forest**: Collection of disconnected trees

### Applications

- River networks
- Hierarchical structures
- Phylogenetic trees
- Decision trees
- Computer data structures

### Mathematical Properties

**Proof of $n-1$ edges**: Start with one node, add nodes one at a time. Each new node requires exactly one edge to maintain connectivity without creating cycles.

## Planar Networks

### Definition

**Planar network**: Can be drawn on a plane without edge crossings

### Examples

1. **Trees**: All trees are planar
2. **Road networks**: Approximately planar (bridges/tunnels cause exceptions)
3. **Geographic adjacency**: Countries/states sharing borders

### Four-Color Theorem

Any planar network can be colored with at most 4 colors such that no adjacent nodes have the same color.

### Kuratowski's Theorem

Network is planar if and only if it contains neither:
- $K_5$ (complete graph on 5 nodes)
- $U_{3,3}$ (complete bipartite graph with 3 nodes in each part)

### Practical Considerations

Most real networks are approximately planar rather than exactly planar. No widely accepted measure exists for "degree of planarity."

## Degree

### Definition

**Degree** $k_i$: Number of edges connected to node $i$

### Mathematical Formula

$$k_i = \sum_{j=1}^{n} A_{ij}$$

### Important Relationships

**Total degree**: $\sum_{i=1}^{n} k_i = 2m$

**Mean degree**: $c = \frac{1}{n} \sum_{i=1}^{n} k_i = \frac{2m}{n}$

### Directed Networks

**In-degree**: $k_i^{\text{in}} = \sum_{j=1}^{n} A_{ij}$

**Out-degree**: $k_i^{\text{out}} = \sum_{j=1}^{n} A_{ji}$

**Equal means**: $\langle k^{\text{in}} \rangle = \langle k^{\text{out}} \rangle = \frac{m}{n}$

### Network Density

**Density** $\rho$: Fraction of possible edges actually present

$$\rho = \frac{m}{\binom{n}{2}} = \frac{2m}{n(n-1)} = \frac{c}{n-1}$$

### Sparsity Classifications

- **Dense**: $\rho$ remains non-zero as $n \to \infty$
- **Sparse**: $\rho \to 0$ as $n \to \infty$  
- **Extremely sparse**: Average degree $c$ remains constant as $n \to \infty$

## Walks and Paths

### Definitions

**Walk**: Sequence of nodes where consecutive pairs are connected by edges

**Path** (Self-avoiding walk): Walk that never visits the same node twice

**Length**: Number of edges traversed

### Counting Walks

**Key Result**: Number of walks of length $r$ from node $j$ to node $i$:

$$N_{ij}^{(r)} = [A^r]_{ij}$$

### Applications

**Loops of length $r$**: $L_r = \text{Tr}(A^r) = \sum_{i=1}^{n} [A^r]_{ii}$

### Shortest Paths

**Shortest path** (Geodesic): Walk with minimum number of edges between two nodes

**Shortest distance**: Length of shortest path

**Diameter**: Length of the longest shortest path in the network

### Properties

- Shortest paths are necessarily self-avoiding
- May not be unique
- Form the basis for many centrality measures

## Components

### Definitions

**Component**: Maximal set of nodes where each can reach every other through some path

**Connected network**: Has only one component

**Disconnected network**: Has multiple components

### Adjacency Matrix Structure

For disconnected network, adjacency matrix has **block diagonal** form when nodes are properly ordered.

### Directed Network Components

**Weakly connected**: Components ignoring edge directions

**Strongly connected**: Components requiring directed paths in both directions between all node pairs

**Out-component**: All nodes reachable from a specified starting node

**In-component**: All nodes from which a specified target node is reachable

### Key Properties

- Every node belongs to exactly one component (of each type)
- Strongly connected components must contain cycles
- DAGs have only single-node strongly connected components

## Independent Paths, Connectivity, and Cut Sets

### Definitions

**Edge-independent paths**: Share no edges

**Node-independent paths**: Share no nodes (except endpoints)

**Connectivity**: Number of independent paths between two nodes

### Cut Sets

**Node cut set**: Set of nodes whose removal disconnects specified node pair

**Edge cut set**: Set of edges whose removal disconnects specified node pair

**Minimum cut set**: Smallest cut set for given node pair

### Menger's Theorem

**Statement**: Size of minimum cut set = Number of independent paths

This fundamental result connects:
- Network connectivity (paths)
- Network vulnerability (cut sets)

### Max-Flow/Min-Cut Theorem

**Statement**: In a flow network, maximum flow between two nodes equals the capacity of the minimum cut separating them.

**Applications**:
- Network optimization
- Resource allocation
- Vulnerability analysis

### Weighted Networks

**Generalization**: Maximum flow = Sum of weights on minimum edge cut set

**Computational importance**: Efficient algorithms exist for maximum flow, enabling efficient minimum cut calculation

## The Graph Laplacian

### Definition

The **graph Laplacian** $L$ is an $n \times n$ matrix with elements:

$$L_{ij} = \begin{cases} 
k_i & \text{if } i = j \\
-1 & \text{if } i \neq j \text{ and there is an edge between } i \text{ and } j \\
0 & \text{otherwise}
\end{cases}$$

### Alternative Representations

**Matrix form**: $L = D - A$

where $D$ is the diagonal degree matrix and $A$ is the adjacency matrix.

**Element-wise**: $L_{ij} = k_i \delta_{ij} - A_{ij}$

### Properties

1. **Row sums**: Every row sums to zero
2. **Symmetry**: $L$ is symmetric for undirected networks
3. **Eigenvalues**: All eigenvalues are non-negative
4. **Zero eigenvalue**: Always has at least one zero eigenvalue with eigenvector $(1,1,\ldots,1)$

### Applications

#### Graph Partitioning

**Problem**: Divide nodes into groups minimizing edges between groups

**Formulation**: Minimize $R = \frac{1}{4} s^T L s$ where $s_i = \pm 1$ indicates group membership

#### Network Visualization

**Goal**: Position nodes to minimize edge lengths

**Formulation**: Minimize $\Delta^2 = x^T L x$ where $x_i$ is position of node $i$

#### Random Walks

**Long-term probability**: $p_i = \frac{k_i}{2m}$ (proportional to degree)

**Connection**: Equilibrium satisfies $LD^{-1}p = 0$

#### Resistor Networks

**Kirchhoff's law**: $LV = RI$ where $V$ is voltage vector and $I$ is current vector

**Applications**: Graph sparsification, numerical methods

### Spectral Properties

**Number of zero eigenvalues** = Number of components

**Algebraic connectivity**: Second smallest eigenvalue
- Zero iff network is disconnected  
- Measures how well-connected the network is

**Spectral gap**: Difference between two smallest eigenvalues
- Important for convergence rates
- Related to network expansion properties

## Key Formulas Summary

### Basic Network Properties

| Property | Formula | Description |
|----------|---------|-------------|
| Degree | $k_i = \sum_j A_{ij}$ | Number of edges at node $i$ |
| Total edges | $\sum_i k_i = 2m$ | Handshaking lemma |
| Mean degree | $c = \frac{2m}{n}$ | Average connections per node |
| Density | $\rho = \frac{2m}{n(n-1)}$ | Fraction of possible edges |

### Matrix Operations

| Operation | Formula | Application |
|-----------|---------|-------------|
| Walk counting | $N_{ij}^{(r)} = [A^r]_{ij}$ | Walks of length $r$ |
| Loop counting | $L_r = \text{Tr}(A^r)$ | Closed walks of length $r$ |
| Projection | $P = B^T B$ | Bipartite to unipartite |
| Laplacian | $L = D - A$ | Fundamental matrix |

### Directed Networks

| Property | Formula | Description |
|----------|---------|-------------|
| In-degree | $k_i^{\text{in}} = \sum_j A_{ij}$ | Incoming edges |
| Out-degree | $k_i^{\text{out}} = \sum_j A_{ji}$ | Outgoing edges |
| Mean equality | $\langle k^{\text{in}} \rangle = \langle k^{\text{out}} \rangle$ | Conservation principle |

### Random Walks

| Property | Formula | Description |
|----------|---------|-------------|
| Update rule | $p_i(t) = \sum_j \frac{A_{ij}}{k_j} p_j(t-1)$ | Probability evolution |
| Equilibrium | $p_i = \frac{k_i}{2m}$ | Stationary distribution |
| Edge probability | $P(i \to j) = \frac{1}{2m}$ | Uniform edge traversal |

## Important Theorems

### Fundamental Results

1. **Handshaking Lemma**: $\sum_{i=1}^{n} k_i = 2m$

2. **Tree Characterization**: Connected network with $n$ nodes and $n-1$ edges is a tree

3. **Menger's Theorem**: Number of independent paths = Size of minimum cut set

4. **Max-Flow/Min-Cut Theorem**: Maximum flow = Capacity of minimum cut

5. **Four-Color Theorem**: Any planar network can be colored with ≤ 4 colors

6. **Spectral Theorem for Laplacian**: Number of zero eigenvalues = Number of components

### Practical Implications

These theorems provide:
- **Computational tools** for network analysis
- **Bounds and limits** on network properties  
- **Optimization methods** for network design
- **Fundamental insights** into network structure

<!-- The mathematical framework developed in this chapter forms the foundation for all subsequent network analysis, from centrality measures to community detection to network dynamics. -->
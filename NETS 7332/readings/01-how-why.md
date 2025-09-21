# The Why, How, and When of Representations for Complex Systems

[Link to paper](https://epubs.siam.org/doi/pdf/10.1137/20M1355896)

## 1. Fundamental Definitions and Concepts

### 1.1 Basic Components

**Unit/Element/Node**: An individual object, agent, or part of a system
- Denoted as set $V = \{v_1, v_2, \ldots, v_n\}$ with $n$ nodes

**Relation**: A set $r$ of one or more nodes such that $r \subseteq V$
- **Dyadic relation**: Contains exactly two units ($|r| = 2$)  
- **Polyadic relation**: Contains three or more units ($|r| > 2$)
- Set of relations denoted by $R$

**Property**: Information attached to nodes or relations
- Set of properties $P$ with assignment map $p: V \times R \to P$

**System**: A collection of units $V$, relations $R$, and properties $P$
- Must function completely or interact autonomously with environment
- **Structure**: Patterns found in the set of relations
- **Function/Behavior**: System activity and changes over time

### 1.2 Complex System Characteristics

A **complex system** exhibits:
1. High cardinality collection of objects/agents
2. Nontrivial interactions between components  
3. Collective behavior that is unexpected or emergent from individual parts

**System Fragment**: A subset $(V', R')$ with $V' \subseteq V$ and $R' \subseteq R$
- Researchers typically work with fragments due to scale or measurement limitations

---

## 2. System Dependencies

### 2.1 Definition of Dependencies

**Dependency**: A property where existence of one relation provides information about existence of another relation

Formal definition: Relation $r_1$ is dependent on relation $r_2$ if knowledge of $r_2$'s existence affects the probability of $r_1$'s existence.

### 2.2 Types of Dependencies

#### Subset Dependencies

**Definition**: System exhibits subset dependency if for relation $r \in R$ and $r' \subset r$, we have $r' \in R$ whenever predicate $P(r')$ is true.

**Mathematical Formulation**: 
If $r = \{v_0, \ldots, v_{k-1}\} \in R$ and $r' \subseteq r$, then $r' \in R$ when logical predicate $P$ is satisfied.

**Examples**:
- Words sharing features: if three words share property "round", any two also share it
- Chemical reactions: not all subsets of reactants form independent reactions

#### Temporal Dependencies  

**Definition**: System exhibits temporal dependency if existence of relations at time $t$ affects behavior at time $t' > t$.

**Characteristics**:
- Trajectories may not be Markovian
- Future depends on past trajectories, not just current state
- Common in transportation, information flow systems

**Mathematical Representation**: Higher-order networks encode temporal dependencies by creating nodes from frequent paths/transitions.

#### Spatial Dependencies

**Definition**: System exhibits spatial dependency if distance between nodes influences relation existence probability.

**Formal Definition**: For nodes with spatial coordinates $x_i$ in metric space, spatial dependency exists if:
$$P(\text{relation between } v_1, \ldots, v_k) = f(d(x_1, x_2), d(x_2, x_3), \ldots, d(x_{k-1}, x_k))$$

where $d(\cdot, \cdot)$ is distance function.

**Examples**:
- Brain connectivity: regions more likely to connect to nearby regions
- Social networks: geographic proximity increases friendship probability
- Economic networks: trade relationships affected by distance

### 2.3 External Sources of Dependencies

**Data Availability**: Limited access to complete system
- Sparse snapshots of evolving systems
- Missing interaction data due to measurement limitations

**Data Acquisition/Processing**: 
- Correlation matrices induce transitivity dependencies
- Processing methods may create artificial dependencies

**Research Question**: 
- Definition of relations depends on research focus
- May neglect relevant dependencies if scope too narrow

---

## 3. Mathematical Frameworks

### 3.1 Graphs

**Definition**: A graph $G = (V, E)$ consists of:
- Node set $V$ 
- Edge set $E \subseteq V \times V$ where each edge connects at most two nodes

**Edge Notation**: $\{v_A, v_B\}$ or $v_A - v_B$ for undirected edges

**Key Properties**:
- Only represents dyadic (pairwise) relations
- Well-established mathematical theory (hundreds of years)
- Simple computations and intuitive visualizations
- Cannot capture polyadic interactions directly

**Variations**:
- **Directed graphs**: Edges have direction ($v_A \to v_B$)
- **Weighted graphs**: Weight function $W: E \to \mathbb{R}$
- **Dynamic graphs**: Sequence $G_1, \ldots, G_T$ over time
- **Multilayer graphs**: Multiple graph layers representing different relation types

### 3.2 Simplicial Complexes

**Definition**: A simplicial complex $K = (V, R)$ consists of:
- Vertex set $V$
- Collection of subsets $R$ with **downward closure**: if $r \in R$ and $r' \subset r$, then $r' \in R$

**k-Simplex**: A set of $k+1$ related vertices
- 0-simplex: single vertex
- 1-simplex: edge (2 vertices)  
- 2-simplex: triangle (3 vertices)
- 3-simplex: tetrahedron (4 vertices)

**Downward Closure Property**: 
$$r \in R \text{ and } r' \subseteq r \Rightarrow r' \in R$$

**Key Features**:
- Naturally encodes subset dependencies
- Enables topological analysis (homology, persistent homology)
- **Maximal simplex**: Not contained in any larger simplex
- Can be represented by maximal simplices alone

**Applications**:
- Neural coactivity analysis
- Brain network topology
- Point cloud analysis in data science

### 3.3 Hypergraphs

**Definition**: A hypergraph $H = (V, R)$ consists of:
- Vertex set $V$
- Hyperedge set $R$ where each hyperedge can connect arbitrary number of vertices

**Key Difference from Simplicial Complexes**: No downward closure requirement
- Hyperedge $\{v_1, v_2, v_3\}$ can exist without requiring $\{v_1, v_2\}$ to exist

**Hyperedge Properties**:
- **Cardinality**: Number of vertices in hyperedge
- **Independence**: Each hyperedge exists independently
- Maximum flexibility for representing polyadic relations

**Representation**: Binary incidence matrix of dimensions $|\text{hyperedges}| \times |\text{vertices}|$

**Applications**:
- Email communication networks
- Protein interaction complexes
- Social group interactions
- Chemical reaction networks

### 3.4 Framework Variations

#### Higher-Order Networks (HONs)
- Encode temporal dependencies by representing frequent paths as nodes
- Transform non-Markovian systems into Markovian representations
- Nodes represent transitions, edges represent sequential dependencies

#### Multilayer Networks
- Multiple layers representing different relation types
- **Multiplex networks**: Same nodes across layers, only self-connections between layers
- Useful for systems with multiple interaction modalities

---

## 4. Mathematical Relationships Between Frameworks

### 4.1 Framework Conversions

#### Hypergraph → Simplicial Complex
**Process**: Apply downward closure to all hyperedges
- Take hyperedge $h = \{v_0, \ldots, v_k\}$
- Add all subsets $h' \subseteq h$ as simplices
- **Information Loss**: Forgets independence of original hyperedges

#### Simplicial Complex → Graph  
**Process**: Project to 1-skeleton
- Keep all 1-simplices as edges
- **Information Loss**: Loses polyadic relationship information

#### Graph → Simplicial Complex
**Process**: Fill cliques with simplices (clique/flag complex)
- $(k+1)$-clique becomes $k$-simplex
- **Assumption**: All nodes in clique are functionally related
- May not be appropriate for all systems

#### Graph → Hypergraph
**Process**: Multiple options
1. Each edge becomes hyperedge (preserves structure)
2. Each clique becomes hyperedge (assumes polyadic relations)

### 4.2 Information Preservation

**Key Principle**: Moving "down" the framework ladder loses information; moving "up" requires assumptions.

**Framework Hierarchy** (in terms of expressiveness):
$$\text{Hypergraph} \supseteq \text{Simplicial Complex} \supseteq \text{Graph}$$

**Round-trip Preservation**:
- Graph → Simplicial Complex → Graph: **Preserves original**
- Hypergraph → Simplicial Complex → Graph → Simplicial Complex → Hypergraph: **Does not preserve original**

---

## 5. Analysis Methods for Each Framework

### 5.1 Graph Methods

#### Node-Level Measures

**Degree**: Number of edges incident to node $v_i$
$$k_i = \text{number of edges connected to } v_i$$

**Clustering Coefficient**: Measures local connectivity
$$c_i = \frac{2\mu_i}{k_i(k_i-1)}$$
where $\mu_i$ = number of edges between neighbors of $v_i$

#### Network-Level Measures
- **Average path length**: Mean shortest path between all node pairs
- **Modularity**: Strength of division into communities  
- **Core-periphery structure**: Dense core with sparse periphery
- **Small-world properties**: High clustering, short path lengths

### 5.2 Simplicial Complex Methods

#### Simplex Participation
**Definition**: Vector $P(v_i)$ where $k$-th element = number of $(k-1)$-simplices containing $v_i$

#### Topological Analysis
- **Homology**: Detects topological cavities and holes
- **Persistent homology**: Tracks topological features across scales
- **Betti numbers**: Count holes of different dimensions

#### Dowker Dual
**Construction**: Transpose node-relation incidence matrix
- Swap roles of nodes and relations
- Preserves topological properties (isomorphic homology groups)
- Useful when relations << nodes

### 5.3 Hypergraph Methods

#### Hyperdegree
**Node hyperdegree**: $d_H(v_i)$ = number of hyperedges containing $v_i$

#### Hypergraph Clustering Coefficient
**Extra Overlap** between hyperedges $e_j, e_k$:
$$EO(e_j, e_k) = \frac{|N(D_{j,k}) \cap D_{k,j}| + |D_{j,k} \cap N(D_{k,j})|}{|D_{j,k}| + |D_{k,j}|}$$

where:
- $D_{j,k} = e_j \setminus e_k$
- $N(U)$ = neighbors of nodes in set $U$

**Hypergraph clustering coefficient**:
$$C_H(v_i) = \begin{cases} 
\binom{|M(v_i)|}{2}^{-1} \sum_{e_j,e_k \in M(v_i)} EO(e_j, e_k) & \text{if } d_H(v_i) > 1 \\
0 & \text{if } d_H(v_i) = 1
\end{cases}$$

#### Fill Coefficient
Measures fraction of smaller hyperedges within larger hyperedge:
$$f(h) = \frac{|\{g \in E : g \subset h \text{ and } |g| > 1\}|}{2^{|h|} - 2 - |h|}$$

---

## 6. Practical Examples and Applications

### 6.1 Coauthorship Networks

**System Components**:
- **Units**: Researchers/authors
- **Relations**: Co-authorship on papers

**Dependency Analysis**:
- **Spatial**: Geographic proximity affects collaboration  
- **Temporal**: Past collaborations influence future ones
- **Subset**: Depends on relation definition

**Representation Choices**:
1. **Graph**: Edge if authors collaborated on ≥1 paper
2. **Simplicial Complex**: Simplex for each paper's author set  
3. **Hypergraph**: Hyperedge for each paper's exact author set

**Key Finding**: Different representations yield different author productivity rankings, especially for low-degree authors.

### 6.2 Email Communication

**System Components**:
- **Units**: Email recipients
- **Relations**: Shared email receipt

**Framework Comparison**:
- **Graph clustering** vs **Hypergraph clustering**: Low correlation (r = 0.1)
- Different frameworks recommend different team intervention priorities
- Fill coefficient shows no correlation with clustering measures

### 6.3 Transportation Networks

**Dependencies**:
- **Temporal**: Previous stops affect future routes (non-Markovian)
- **Spatial**: Geographic constraints on connections
- **Subset**: Route segments may/may not be independent

**Higher-Order Networks**: Represent stations with arrival history
- Node $D_B$ = "station D arrived from B"  
- Captures temporal dependencies in graph framework

---

## 7. Framework Selection Guidelines

### 7.1 Decision Criteria

**Choose Graphs when**:
- Only dyadic relations exist
- Temporal dependencies negligible  
- Well-established graph methods needed
- Computational simplicity required

**Choose Simplicial Complexes when**:
- Strong subset dependencies present
- Topological analysis needed
- Mathematical rigor for polyadic relations required
- Downward closure property holds

**Choose Hypergraphs when**:
- Polyadic relations without subset dependencies
- Maximum representational flexibility needed  
- Independent group interactions important
- Absent substructures are meaningful

### 7.2 Common Pitfalls

**Method-Driven Selection**: Don't choose framework based solely on available analysis methods

**Assumption Violations**: Converting between frameworks may violate system properties

**Dependency Neglect**: Failing to identify and encode relevant dependencies

**Scale Mismatch**: Framework choice affects which system properties are visible

---

## 8. Mathematical Formulations Summary

### 8.1 Key Equations

**Graph Clustering Coefficient**:
$$c_i = \frac{2\mu_i}{k_i(k_i-1)}$$

**Hypergraph Extra Overlap**:
$$EO(e_j, e_k) = \frac{|N(D_{j,k}) \cap D_{k,j}| + |D_{j,k} \cap N(D_{k,j})|}{|D_{j,k}| + |D_{k,j}|}$$

**Fill Coefficient**:
$$f(h) = \frac{|\{g \in E : g \subset h \text{ and } |g| > 1\}|}{2^{|h|} - 2 - |h|}$$

**Downward Closure (Simplicial Complexes)**:
$$r \in R \text{ and } r' \subseteq r \Rightarrow r' \in R$$

### 8.2 Framework Relationships

$$\text{Expressiveness: } \text{Hypergraph} \supseteq \text{Simplicial Complex} \supseteq \text{Graph}$$

$$\text{Constraint Level: } \text{Graph} > \text{Simplicial Complex} > \text{Hypergraph}$$

---

## 9. Applications Across Domains

### 9.1 Neuroscience
- **Structural connectome**: Spatial dependencies from anatomical constraints
- **Functional networks**: Temporal dependencies in neural activity
- **Coactivation patterns**: Subset dependencies in neural ensembles

### 9.2 Social Systems  
- **Communication networks**: Temporal patterns in message flows
- **Group membership**: Polyadic relations without subset dependencies
- **Geographic influences**: Spatial dependencies in social ties

### 9.3 Biological Systems
- **Protein complexes**: Subset dependencies in molecular interactions  
- **Metabolic networks**: Directed hypergraphs for reactions
- **Gene regulatory networks**: Temporal dependencies in expression

### 9.4 Transportation
- **Route planning**: Temporal dependencies in passenger flows
- **Network topology**: Spatial constraints from geography
- **Multimodal systems**: Multilayer representations

---

## 10. Study Tips and Key Takeaways

### 10.1 Critical Concepts to Master

1. **Dependency Recognition**: Identify which dependencies exist in given systems
2. **Framework Properties**: Understand mathematical constraints of each framework  
3. **Information Loss**: Know what's lost/assumed in framework conversions
4. **Method Appropriateness**: Match analysis methods to framework and system properties

### 10.2 Common Exam Topics

- Convert between framework representations
- Identify appropriate framework for given system
- Calculate clustering coefficients for different frameworks
- Analyze impact of dependencies on system analysis
- Interpret differences in results across frameworks

### 10.3 Problem-Solving Strategy

1. **Identify system components** (units, relations, properties)
2. **Detect dependencies** (subset, temporal, spatial, external)  
3. **Choose appropriate framework** based on dependencies and research question
4. **Select analysis methods** compatible with framework and system properties
5. **Interpret results** considering framework assumptions and limitations
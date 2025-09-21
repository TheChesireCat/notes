# 8️⃣ Computer Algorithms for Networks


## Key Concepts and Definitions

### Computational Complexity
**Definition**: A measure of how the running time of an algorithm scales with the size of the input (typically network size).

**Big O Notation**: $O(f(n))$ means the running time grows no faster than a constant times $f(n)$ as $n$ becomes large.

**Common Complexity Classes**:
- $O(1)$: Constant time
- $O(\log n)$: Logarithmic time  
- $O(n)$: Linear time
- $O(n \log n)$: Log-linear time
- $O(n^2)$: Quadratic time
- $O(n^k)$ where $k > 2$: Generally too slow for large networks

### Network Parameters
- $n$: Number of nodes
- $m$: Number of edges  
- $c = 2m/n$: Average degree
- For sparse networks: $m \propto n$ (average degree remains constant as $n$ grows)

## Data Structures for Network Storage

### Adjacency Matrix

**Description**: An $n \times n$ matrix $A$ where $A_{ij} = 1$ if there is an edge between nodes $i$ and $j$.

**Memory Requirements**: $O(n^2)$ space

**Operations Complexity**:
| Operation | Time Complexity |
|-----------|----------------|
| Insert edge | $O(1)$ |
| Delete edge | $O(1)$ |
| Find edge | $O(1)$ |
| Enumerate neighbors | $O(n)$ |

**Advantages**:
- Fast edge insertion, deletion, and lookup
- Direct implementation of mathematical formulations
- Constant memory usage regardless of edge count

**Disadvantages**:
- Wasteful for sparse networks (stores many zeros)
- Slow neighbor enumeration
- Large memory footprint: $4n^2$ bytes for integer matrix

**Maximum Network Size** (with 10 GB RAM): $n \approx 50,000$ nodes

### Adjacency List

**Description**: For each node $i$, maintain a list of its neighbors.

**Memory Requirements**: $O(m)$ space (stores $2m$ integers for undirected networks)

**Operations Complexity**:
| Operation | Time Complexity |
|-----------|----------------|
| Insert edge | $O(1)$ |
| Delete edge | $O(m/n)$ |
| Find edge | $O(m/n)$ |
| Enumerate neighbors | $O(m/n)$ |

**Advantages**:
- Memory efficient for sparse networks
- Fast neighbor enumeration
- Scalable to very large networks

**Disadvantages**:
- Slower edge finding and deletion compared to adjacency matrix
- Variable memory usage

### Hybrid and Advanced Representations

**Matrix-List Hybrid**: Combines adjacency matrix with adjacency list using pointers
- All operations in $O(1)$ or $O(m/n)$ time
- High memory usage: $O(n^2 + m)$

**Hash Table Implementation**: Store neighbor lists in hash tables
- Expected $O(1)$ time for all operations
- Higher memory overhead but optimal performance

## Algorithms for Basic Network Quantities

### Degree Calculation

**Adjacency List**: $O(1)$ time (degrees stored separately)
**Adjacency Matrix**: $O(n)$ time (sum row elements)

**Degree Correlation Coefficient**: 
$$r = \frac{\sum_{(i,j) \in E} k_i k_j - \frac{1}{2m}\left(\sum_{(i,j) \in E}(k_i + k_j)\right)^2}{\frac{1}{2}\sum_{(i,j) \in E}(k_i^2 + k_j^2) - \frac{1}{2m}\left(\sum_{(i,j) \in E}(k_i + k_j)\right)^2}$$

Time complexity: $O(m + n)$

### Clustering Coefficients

**Local Clustering Coefficient** for node $i$:
$$C_i = \frac{\text{number of triangles connected to node } i}{\text{number of triples centered on node } i} = \frac{2t_i}{k_i(k_i-1)}$$

**Global Clustering Coefficient**:
$$C = \frac{3 \times \text{number of triangles}}{\text{number of connected triples}}$$

**Algorithm**: For each node, check all pairs of neighbors for connections.

**Time Complexity**: $O\left(\sum_i k_i^2\right) = O(n\langle k^2 \rangle)$

**Issue with Scale-Free Networks**: For power-law degree distributions, $\langle k^2 \rangle$ can be very large, making computation slow.

## Shortest Paths and Breadth-First Search

### Breadth-First Search (BFS)

**Purpose**: Find shortest distances from source node $s$ to all other nodes in the same component.

**Algorithm**:
1. Initialize distance array: $d[s] = 0$, all others unknown
2. Use FIFO queue to process nodes layer by layer
3. For each node at distance $d$, mark unvisited neighbors as distance $d+1$

**Time Complexity**: $O(m + n)$

**Proof of Correctness**: By induction - after round $d$, all nodes at distance $\leq d$ are correctly labeled.

### Implementation Details

**Queue-Based Implementation**:
- Use two pointers: read pointer and write pointer
- Each node appears in queue at most once
- Process nodes in order of increasing distance

**Finding Shortest Paths**:
- Maintain predecessor pointers during BFS
- Creates shortest-path tree rooted at source
- Multiple shortest paths: allow multiple predecessors per node

### Variants of BFS

**Two-Source BFS**: For single pair shortest distance
- Start BFS from both source and target simultaneously  
- Stop when searches meet at common node
- Time complexity: $O(m\sqrt{n})$ on average

**All-Pairs Shortest Paths**: 
- Run BFS from each node
- Time complexity: $O(n(m + n)) = O(n^2)$ for sparse networks

### Betweenness Centrality

**Definition**: Number of shortest paths between all pairs that pass through a given node.

**Naive Algorithm**: $O(n^{3/2}m)$ time - too slow

**Efficient Algorithm**:
1. For each source $s$, run BFS to build shortest-path tree
2. Calculate path counts using tree structure
3. Work backwards from leaves to accumulate betweenness scores

**Time Complexity**: $O(n(m + n)) = O(n^2)$ for sparse networks

**Key Insight**: Exploit shared edges in shortest-path trees to avoid redundant calculations.

## Dijkstra's Algorithm for Weighted Networks

### Problem Setting
Find shortest paths when edges have positive weights/lengths.

### Algorithm
1. Maintain distance estimates (initially $\infty$ except source = 0)  
2. Maintain certainty flags for distances
3. Repeatedly:
   - Select uncertain node with smallest estimated distance
   - Mark its distance as certain
   - Update estimates to its neighbors
   - Continue until all distances are certain

### Correctness Proof
**Key Claim**: Node with smallest uncertain distance estimate has correct shortest distance.

**Proof**: Any alternative shorter path would pass through another uncertain node with smaller estimate - contradiction.

### Implementation and Complexity

**Naive Implementation**: $O(m + n^2)$
- Linear search for minimum distance each round

**Heap-Based Implementation**: $O((m + n) \log n)$  
- Use binary heap to maintain minimum distance
- Extract minimum: $O(\log n)$
- Update distance: $O(\log n)$

## Maximum Flows and Minimum Cuts

### Ford-Fulkerson (Augmenting Path) Algorithm

**Problem**: Find maximum flow from source $s$ to sink $t$ where each edge can carry one unit.

**Key Insight**: Allow flow in both directions along edges, with net flow respecting capacity constraints.

**Algorithm**:
1. Initialize all flows to zero
2. While augmenting path from $s$ to $t$ exists:
   - Find path using BFS (avoiding saturated edges)
   - Add one unit of flow along this path
3. Return total flow found

### Implementation Details

**Flow Representation**: Track net flow on each edge
- Forward flow increases net flow
- Backward flow decreases net flow  
- Net flow must be 0 or 1 in allowed direction

**Path Finding**: Modified BFS that respects capacity constraints

**Time Complexity**: $O(\min(k_s, k_t)(m + n))$ where $k_s, k_t$ are degrees of source and sink
- Average case: $O((m + n)m/n) = O(n)$ for sparse networks

### Correctness Proof

**Max-Flow Min-Cut Theorem**: Maximum flow equals minimum cut size.

**Proof Strategy**: 
1. Show algorithm terminates when no augmenting paths exist
2. Prove that remaining flow is maximum possible
3. Use conservation of flow and capacity constraints

### Finding Independent Paths and Cuts

**Independent Paths**: Remove zero-flow edges from final flow pattern
- Remaining edges form the independent paths
- Trace paths from source to sink

**Minimum Cut Set**: 
1. Perform final BFS from source (respecting flow constraints)
2. Let $V_s$ = reachable nodes, $V_t$ = unreachable nodes  
3. Edges between $V_s$ and $V_t$ form minimum cut

### Node-Independent Paths

**Transformation Method**:
1. Replace undirected edges with bidirectional edges
2. Split each intermediate node into two nodes connected by single edge
3. Apply edge-independent path algorithm
4. Result gives node-independent paths in original network

## Performance Analysis Summary

| Algorithm | Time Complexity | Space Complexity | Best For |
|-----------|----------------|------------------|----------|
| BFS (single source) | $O(m + n)$ | $O(n)$ | Unweighted shortest paths |
| BFS (two source) | $O(m\sqrt{n})$ | $O(n)$ | Single pair distance |
| Dijkstra (naive) | $O(m + n^2)$ | $O(n)$ | Small weighted networks |
| Dijkstra (heap) | $O((m + n)\log n)$ | $O(n)$ | Large weighted networks |
| Betweenness | $O(n(m + n))$ | $O(n + m)$ | Centrality analysis |
| Max flow | $O(\min(k_s, k_t)(m + n))$ | $O(n + m)$ | Connectivity/cuts |

## Practical Considerations

### Software Tools
- **Interactive**: Gephi, Pajek, yEd, Visone
- **Libraries**: NetworkX (Python), igraph (R/Python/C), JUNG (Java)
- **Visualization**: Graphviz

### Memory Management
- Large networks may not fit in RAM
- Cache performance affects algorithm speed  
- Consider memory hierarchy in implementation

### Algorithm Selection
- Choose data structure based on network density and operations needed
- Sparse networks: prefer adjacency lists
- Dense networks or frequent edge queries: consider adjacency matrix
- Complex algorithms: use established libraries when possible

## Key Relationships and Formulas

**Average Degree**: $\langle k \rangle = 2m/n$

**Clustering Coefficient**: $C = \frac{3T}{P}$ where $T$ = triangles, $P$ = connected triples

**Betweenness Centrality**: $g_i = \sum_{s \neq i \neq t} \frac{\sigma_{st}(i)}{\sigma_{st}}$

**Max-Flow Min-Cut**: Maximum flow = Minimum cut size

**Time Scaling**: For sparse networks with constant average degree:
- $O(m + n) \equiv O(n)$  
- $O(m) \equiv O(n)$
- $O(n \log n)$ near-optimal for many problems

<!-- This foundation enables efficient analysis of networks with thousands to millions of nodes, making modern large-scale network science computationally feasible. -->
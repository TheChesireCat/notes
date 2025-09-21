# 🔟 The Structure of Real-World Networks 
<!-- 
**Comprehensive Study Notes**

---

## Overview

This chapter examines the empirical structure of real-world networks by applying theoretical concepts to observed network data. The analysis reveals several **distinctive patterns** that recur across different types of networks:

- **Component structures** with large connected components
- **Short path lengths** (small-world effect)  
- **Power-law degree distributions** (scale-free networks)
- **High clustering coefficients**
- **Assortative/disassortative mixing patterns**

These structural features have profound effects on how networked systems behave and function.

--- -->

## Components

### Components in Undirected Networks

#### Key Concept
A **component** is a maximal set of nodes that are connected to each other through paths in the network.

#### Typical Structure
Most undirected networks exhibit a characteristic component structure:

- **One large component** occupying 50-90% of nodes
- **Multiple small components** with only a few nodes each

#### Mathematical Framework
Let $S$ be the size of the largest component as a fraction of total network size:

$$S = \frac{\text{nodes in largest component}}{n}$$

where $n$ is the total number of nodes.

#### Examples from Real Networks

| Network Type | $S$ Value | Explanation |
|--------------|-------------|-------------|
| Film actors | 0.98 | 98% of actors connected in largest component |
| Internet | 1.00 | All nodes must be connected for communication |
| Web crawl | 1.00 | Crawling method ensures single component |

#### Why Networks Rarely Have Multiple Large Components

**Mathematical argument**: If a network of $n$ nodes had two large components of size $\approx \frac{n}{2}$ each, there would be $\binom{n/2 \cdot n/2}{1} = \frac{n^2}{4}$ possible connections between components. The probability that **none** of these connections exist is extremely low, making multiple large components highly unlikely.

### Components in Directed Networks

#### Strongly Connected Components
A **strongly connected component** is a maximal set of nodes where each node can reach every other node via directed paths.

#### Weakly Connected Components  
A **weakly connected component** treats all edges as undirected - it's the component structure ignoring edge directions.

#### Bow Tie Structure
Directed networks often exhibit a "bow tie" structure:

- **Strongly Connected Component (SCC)**: Core with bidirectional paths
- **In-component**: Nodes that can reach the SCC
- **Out-component**: Nodes reachable from the SCC  
- **Tendrils**: Nodes connected to in/out-components but not SCC

**Example**: World Wide Web structure (circa 2000):
- SCC: 28% of nodes
- In-component: 21% of nodes  
- Out-component: 21% of nodes
- Other components: 30% of nodes

---

## Shortest Paths and Small-World Effect

### Mathematical Definition

#### Mean Distance Between Nodes
For an undirected network, the mean distance from node $i$ to all others:

$$\ell_i = \frac{1}{n} \sum_j d_{ij}$$

where $d_{ij}$ is the shortest path length between nodes $i$ and $j$.

#### Network-Wide Mean Distance
The overall mean distance for the network:

$$\ell = \frac{1}{n} \sum_i \ell_i = \frac{1}{n^2} \sum_{ij} d_{ij}$$

#### Multi-Component Networks
For networks with multiple components $\mathscr{C}_m$:

$$\ell = \frac{\sum_m \sum_{i,j \in \mathscr{C}_m} d_{ij}}{\sum_m n_m^2}$$

where $n_m$ is the number of nodes in component $m$.

### Properties and Implications

#### Small-World Effect
**Definition**: The mean distance $\ell$ is surprisingly small, typically $\ell \propto \log n$.

**Empirical Evidence**: Even networks with millions of nodes show $\ell < 20$, usually $\ell < 10$.

#### Practical Implications
- **Disease/rumor spread**: Reaches population quickly via short paths
- **Internet performance**: Data packets require few hops
- **Social influence**: Ideas spread rapidly through society

#### Diameter vs Mean Distance
- **Diameter**: Length of longest shortest path
- **Mean distance**: Average over all node pairs
- **Preference**: Mean distance is more robust and representative than diameter

### Funneling Effect

**Observation**: In shortest paths from a node, a large fraction often pass through just one or two neighbors.

**Example**: Physics collaboration network - 48% of shortest paths go through single neighbor for nodes with degree ≥ 5.

---

## Degree Distributions

### Basic Definitions

#### Degree Distribution
$p_k$ = fraction of nodes with degree $k$

$$p_k = \frac{\text{number of nodes with degree } k}{n}$$

#### Interpretation as Probability
$p_k$ represents the probability that a randomly chosen node has degree $k$.

#### Degree Sequence  
The set $\{k_1, k_2, \ldots, k_n\}$ of all node degrees.

**Important Note**: Degree distribution does not uniquely determine network structure - multiple networks can have identical degree distributions.

### Right-Skewed Distributions

#### Characteristic Pattern
Most real-world networks show **right-skewed** degree distributions:
- Many nodes with low degree (1, 2, 3 connections)
- Significant "tail" of high-degree nodes (**hubs**)
- Highest degree nodes may connect to 10-20% of network

#### Hub Definition
A **hub** is a node with unusually high degree compared to typical nodes in the network.

### Directed Network Degrees

#### Two Types of Degrees
- **In-degree**: Number of incoming edges
- **Out-degree**: Number of outgoing edges

#### Separate Distributions
Directed networks have two degree distributions: $p^{\text{in}}_k$ and $p^{\text{out}}_k$

#### Joint Distribution
The complete description requires the joint distribution $p_{jk}$ = fraction of nodes with in-degree $j$ and out-degree $k$.

---

## Power Laws and Scale-Free Networks

### Mathematical Form

#### Power Law Definition
A degree distribution follows a **power law** if:

$$p_k = C k^{-\alpha}$$

where:
- $C$ = normalization constant
- $\alpha$ = power-law exponent (typically $2 \leq \alpha \leq 3$)

#### Equivalent Logarithmic Form

$$\ln p_k = -\alpha \ln k + \ln C$$

#### Scale-Free Networks
Networks with power-law degree distributions are called **scale-free networks**.

### Detection Methods

#### Log-Log Plots
Plot $\log p_k$ vs $\log k$:
- **Power law**: Straight line with slope $-\alpha$
- **Problems**: Poor statistics in tail, binning effects

#### Logarithmic Binning
Use bins of increasing width by factor $a$ (commonly $a = 2$):
- Bin $n$ covers interval $[a^{n-1}, a^n)$
- **Normalize** by dividing counts by bin width
- **Advantage**: Equal bin widths on log scale, better statistics

#### Cumulative Distribution Function

$$P_k = \sum_{k'=k}^{\infty} p_{k'} = \text{fraction of nodes with degree } \geq k$$

**Key Property**: If $p_k \propto k^{-\alpha}$, then $P_k \propto k^{-(\alpha-1)}$

**Advantages**:
- No binning required
- Preserves all information
- Better statistics in tail

#### Maximum Likelihood Estimation
**Preferred method** for estimating $\alpha$:

$$\alpha = 1 + N \left( \sum_{i=1}^N \ln \frac{k_i}{k_{\min} - 0.5} \right)^{-1}$$

**Statistical error**:

$$\sigma = \frac{\alpha - 1}{\sqrt{N}}$$

where $N$ = number of nodes with $k \geq k_{\min}$.

### Properties of Power-Law Distributions

#### Normalization
For $p_k = C k^{-\alpha}$ with $k \geq 1$:

$$C = \frac{1}{\zeta(\alpha)}$$

where $\zeta(\alpha) = \sum_{k=1}^{\infty} k^{-\alpha}$ is the Riemann zeta function.

#### Moments
The $m$-th moment:

$$\langle k^m \rangle = \sum_{k=0}^{\infty} k^m p_k$$

**Critical result**: $\langle k^m \rangle$ is finite if and only if $m < \alpha - 1$

**Implications**:
- **Mean** $\langle k \rangle$: Always finite for $\alpha > 2$
- **Second moment** $\langle k^2 \rangle$: Finite only for $\alpha > 3$
- Most real networks have $2 \leq \alpha \leq 3$ → **divergent second moment**

#### Top-Heavy Distributions (Lorenz Curves)
Fraction $W$ of edge-ends connected to fraction $P$ of highest-degree nodes:

$$W = P^{(\alpha-2)/(\alpha-1)}$$

**Example**: Web with $\alpha = 2.2$:
- 50% of links go to top 1.1% of nodes
- Top 50% of nodes receive 89% of links

---

## Other Centrality Measures

### Eigenvector Centrality
- Often follows **power-law distribution** in tail
- Similar to degree centrality but weighted by neighbors' centralities

### Betweenness Centrality
- Typically **right-skewed**, often power-law
- Measures importance for shortest paths

### Closeness Centrality
- **Exception**: Does not follow power law
- Limited range due to diameter bounds
- Bounded between $1$ and $1/\text{diameter}$

---

## Clustering Coefficients

### Global Clustering

#### Definition

$$C = \frac{\text{number of triangles}}{\text{number of connected triples}} \times 3$$

#### Expected Value for Random Networks
For random networks with given degree distribution:

$$C_{\text{random}} = \frac{1}{n} \cdot \frac{\langle k^2 \rangle - \langle k \rangle}{\langle k \rangle^2}$$

#### Empirical Observations
- **Social networks**: $C \gg C_{\text{random}}$ (high clustering)
- **Some technical networks**: $C \ll C_{\text{random}}$ (low clustering)
- **Explanation**: Triadic closure in social networks

### Local Clustering

#### Definition
For node $i$:

$$C_i = \frac{\text{edges between neighbors of } i}{\binom{k_i}{2}}$$

#### Degree Dependence
**Empirical pattern**: $C_i$ decreases with degree $k_i$

**Proposed forms**:
- $C_i \sim k_i^{-0.7}$
- $C_i \sim k_i^{-1}$

**Explanation**: Community structure - small communities have high clustering and low degree.

---

## Assortative Mixing

### Definition
**Assortative mixing**: Tendency of nodes to connect to similar nodes
**Disassortative mixing**: Tendency to connect to dissimilar nodes

### Degree Assortativity

#### Correlation Coefficient

$$r = \frac{\sum_{ij} A_{ij}(k_i - \langle k \rangle)(k_j - \langle k \rangle)}{\sum_{ij} A_{ij}(k_i - \langle k \rangle)^2}$$

#### Computational Form

$$r = \frac{S_1 S_2 - S_3^2}{S_1 S_4 - S_3^2}$$

where:
- $S_1 = \sum_{\text{edges } (i,j)} (k_i + k_j)$
- $S_2 = \sum_{\text{edges } (i,j)} k_i k_j$  
- $S_3 = \sum_i k_i^2$
- $S_4 = \sum_i k_i^3$

#### Empirical Patterns
- **Social networks**: $r > 0$ (assortative)
- **Technical/biological networks**: $r < 0$ (disassortative)

#### Explanations
- **Disassortativity**: Natural tendency in simple networks (no multi-edges)
- **Social assortativity**: Community structure leads to degree correlation

---

## Key Formulas Summary

| Concept | Formula | Description |
|---------|---------|-------------|
| Mean distance | $\ell = \frac{1}{n^2} \sum_{ij} d_{ij}$ | Average shortest path length |
| Power law | $p_k = C k^{-\alpha}$ | Degree distribution form |
| Cumulative distribution | $P_k = \sum_{k'=k}^{\infty} p_{k'}$ | Tail probability |
| MLE exponent | $\alpha = 1 + N(\sum_i \ln \frac{k_i}{k_{\min} - 0.5})^{-1}$ | Power-law exponent estimate |
| Global clustering | $C = \frac{3 \times \text{triangles}}{\text{connected triples}}$ | Network clustering coefficient |
| Local clustering | $C_i = \frac{\text{edges between neighbors}}{\binom{k_i}{2}}$ | Node clustering coefficient |
| Degree assortativity | $r = \frac{S_1 S_2 - S_3^2}{S_1 S_4 - S_3^2}$ | Degree correlation coefficient |

---

## Applications and Examples

### Internet Structure
- **Degree distribution**: Power law with $\alpha \approx 2.1$
- **Clustering**: Lower than random ($C = 0.012$ vs expected $0.84$)
- **Assortativity**: Disassortative ($r = -0.189$)

### World Wide Web
- **In/out-degrees**: Both follow power laws
- **Component structure**: Bow tie with large SCC
- **Lorenz curve**: 50% of links to 1.1% of pages

### Social Networks
- **High clustering**: Much higher than random
- **Assortative mixing**: Positive degree correlation
- **Small world**: Short paths despite high clustering

### Biological Networks
- **Food webs**: Moderate clustering
- **Protein interactions**: Right-skewed degrees
- **Neural networks**: Specific motif patterns

---

## Key Takeaways

1. **Universal patterns** exist across diverse network types
2. **Power-law distributions** are common but not universal
3. **Small-world effect** appears in most large networks
4. **Clustering** varies dramatically by network type and formation mechanism
5. **Degree correlations** distinguish social from technical networks
6. **Component structure** typically features one large component
7. **Mathematical tools** enable quantitative characterization of network structure

These structural patterns have profound implications for:
- **Epidemic spreading** (fast due to short paths)
- **Network robustness** (hubs create vulnerabilities)
- **Search and navigation** (clustering aids local search)
- **Community detection** (degree correlations indicate communities)
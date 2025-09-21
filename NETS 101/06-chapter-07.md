# 🎨 Degree Correlations

## Key Concepts and Definitions

### Degree Correlations
**Definition**: The tendency of nodes with certain degrees to connect preferentially to nodes with specific degrees, deviating from random expectations.

**Three Types of Networks:**
- **Assortative**: High-degree nodes (hubs) tend to connect to other high-degree nodes
- **Disassortative**: High-degree nodes tend to connect to low-degree nodes  
- **Neutral**: Connections follow random expectations with no degree preferences

### Probability of Hub Connection
For random connections, the probability that nodes with degrees $k$ and $k'$ link to each other is:

$$p_{k,k'} = \frac{kk'}{2L}$$

where $L$ is the total number of links in the network.

## Measuring Degree Correlations

### Degree Correlation Matrix
The **degree correlation matrix** $e_{ij}$ represents the probability of finding nodes with degrees $i$ and $j$ at the two ends of a randomly selected link.

**Normalization condition:**
$$\sum_{i,j} e_{ij} = 1$$

**Connection to degree distribution:**
$$\sum_j e_{ij} = q_i$$

where $q_k = \frac{kp_k}{\langle k \rangle}$ is the probability of finding a degree-$k$ node at the end of a randomly selected link.

### Neutral Network Expectation
For neutral networks (no correlations):
$$e_{ij} = q_i q_j$$

### Degree Correlation Function
The **degree correlation function** $k_{nn}(k)$ measures the average degree of neighbors of all degree-$k$ nodes:

$$k_{nn}(k) = \sum_{k'} k' P(k'|k)$$

where $P(k'|k)$ is the conditional probability of reaching a degree-$k'$ node from a degree-$k$ node.

**For neutral networks:**
$$k_{nn}(k) = \frac{\langle k^2 \rangle}{\langle k \rangle}$$

This leads to the **friendship paradox**: our friends are more popular than we are on average.

### Scaling Hypothesis
The degree correlation function often follows a power law:
$$k_{nn}(k) = ak^{\mu}$$

**Interpretation of correlation exponent $\mu$:**
- $\mu > 0$: **Assortative** network
- $\mu = 0$: **Neutral** network  
- $\mu < 0$: **Disassortative** network

### Degree Correlation Coefficient
Alternative single-number measure of correlations:
$$r = \sum_{jk} \frac{jk(e_{jk} - q_j q_k)}{\sigma^2}$$

where $\sigma^2 = \sum_k k^2 q_k - [\sum_k k q_k]^2$

**Range and interpretation:**
- $-1 \leq r \leq 1$
- $r > 0$: Assortative
- $r = 0$: Neutral
- $r < 0$: Disassortative

## Structural Cutoffs

### Origin of Structural Disassortativity
In scale-free networks with $\gamma < 3$, the **structural cutoff** emerges when the expected number of links between large hubs exceeds 1:

$$k_s(N) \sim (\langle k \rangle N)^{1/2}$$

**Consequence**: Networks become structurally disassortative because multiple links between hubs are forbidden in simple networks.

### Conditions for Structural Effects
- **No structural cutoff**: $\gamma \geq 3$ or random networks
- **Structural disassortativity**: Scale-free networks with $\gamma < 3$

### Testing for Structural vs. Real Correlations
Use **degree-preserving randomization**:
1. **R-S (Simple)**: Randomize while forbidding multi-links
2. **R-M (Multi)**: Allow multi-links during randomization

Compare original $k_{nn}(k)$ with randomized versions to determine if correlations are structural or genuine.

## Correlations in Real Networks

### Empirical Observations

**Social Networks**: Generally assortative
- Mobile phone networks: $\mu = 0.33$
- Scientific collaboration: $\mu = 0.16$
- Actor networks: $\mu = 0.34$

**Biological Networks**: Often structurally disassortative
- Protein interactions: $\mu = -0.1$ 
- Metabolic networks: $\mu = -0.76$

**Technological Networks**: Mixed behavior
- Internet: Assortative for small $k$, neutral for large $k$
- WWW: Disassortative, partially structural

**Power Grid**: Nearly neutral ($\mu \approx 0$)

### Mechanisms for Assortativity
- **Community structure**: Tendency to form groups
- **Homophily**: Similar individuals associate
- **Professional/social mechanisms**: Bringing hubs together

## Generating Correlated Networks

### Static Models
**Erdős-Rényi**: Always neutral ($\mu = 0$)

**Configuration Model**: 
- Neutral with multi-links allowed
- Structurally disassortative if simple network required

**Hidden Parameter Model**: 
- Technically neutral
- Shows structural disassortativity: $k_{nn}(k) \sim k^{-1}$

### Growing Networks
**Initial Attractiveness Model**: $\Pi(k) \sim A + k$

Three regimes based on initial attractiveness $A$:

1. **Disassortative** ($-m < A < 0$, $\gamma < 3$):
   $$k_{nn}(k) \sim k^{\frac{|A|}{m}}$$

2. **Neutral** ($A = 0$, $\gamma = 3$):
   $$k_{nn}(k) \sim \frac{m}{2}\ln N$$

3. **Weak Assortative** ($A > 0$, $\gamma > 3$):
   $$k_{nn}(k) \approx (m + A)\ln\left(\frac{k}{m + A}\right)$$

### Xulvi-Brunet & Sokolov Algorithm
**Method to generate maximally correlated networks:**

1. **Link Selection**: Choose two random links connecting nodes $a, b, c, d$ with $k_a \geq k_b \geq k_c \geq k_d$

2. **Rewiring**:
   - **Assortative**: Pair $a$ with $b$, $c$ with $d$
   - **Disassortative**: Pair $a$ with $d$, $b$ with $c$

**Tunable version**: Execute deterministic rewiring with probability $p$

## Impact of Degree Correlations

### Giant Component Formation
**Phase transition effects:**
- **Assortative**: Giant component appears at lower $\langle k \rangle$ (easier formation)
- **Disassortative**: Phase transition delayed (harder formation)
- **Large $\langle k \rangle$**: Assortative networks have smaller giant components

### Path Length Distribution
- **Assortative networks**: Shorter average path length, but larger diameter
- **Reason**: Long chains of degree-2 nodes increase maximum distance

### Other Impacts
- **Disease spreading**: Assortative social networks create hub "reservoirs"
- **Network robustness**: Hub removal less damaging in assortative networks
- **Synchronization**: Affects oscillator synchronization on networks
- **Control theory**: Influences number of control inputs needed
- **Vertex cover problem**: Changes computational complexity

## Mathematical Relationships

### Friendship Paradox
Average degree of neighbors exceeds individual degree:
$$k_{nn} > \langle k \rangle$$

For random networks: $k_{nn} = 1 + \langle k \rangle$

### Correlation Coefficient vs. Exponent
Relationship between $r$ and $\mu$:
- Both measures generally agree on correlation type
- $r$ assumes linear relationship: $k_{nn}(k) \sim rk$
- $\mu$ assumes power law: $k_{nn}(k) \sim k^{\mu}$
- Power law form has better theoretical support

### Directed Networks
Four correlation coefficients for directed networks:
$$r_{\alpha,\beta} = \frac{\sum_{jk} jk(e_{jk}^{\alpha,\beta} - q_{\leftarrow j}^{\alpha} q_{\rightarrow k}^{\beta})}{\sigma_{\leftarrow}^{\alpha} \sigma_{\rightarrow}^{\beta}}$$

where $\alpha, \beta \in \{in, out\}$

## Key Formulas Summary

| Concept | Formula | Meaning |
|---------|---------|---------|
| Hub connection probability | $p_{k,k'} = \frac{kk'}{2L}$ | Random expectation |
| Degree correlation function | $k_{nn}(k) = \sum_{k'} k' P(k'\|k)$ | Average neighbor degree |
| Neutral network | $k_{nn}(k) = \frac{\langle k^2 \rangle}{\langle k \rangle}$ | No correlations |
| Scaling hypothesis | $k_{nn}(k) = ak^{\mu}$ | Power law form |
| Structural cutoff | $k_s(N) \sim (\langle k \rangle N)^{1/2}$ | Simple network limit |
| Correlation coefficient | $r = \sum_{jk} \frac{jk(e_{jk} - q_j q_k)}{\sigma^2}$ | Single number measure |

## Applications and Examples

### Celebrity Dating Example
- Pool of $10^8$ eligible individuals
- 1,000 celebrities total  
- Random probability: $10^{-5}$ for celebrity-celebrity pairing
- Reality: Much higher due to assortative mixing

### Protein Networks
- Hubs avoid other hubs
- Connect preferentially to low-degree nodes
- Structural disassortativity from scale-free property

### Social Networks
- Hubs (popular people) know other hubs
- Community effects enhance assortativity
- Professional networks bring leaders together

This comprehensive overview covers the theoretical foundations, measurement techniques, empirical observations, and practical implications of degree correlations in complex networks.
---
title: The Why, How, and When of Representations for Complex Systems
short_title: Representations
subject: NETS 7332 · Reading
description: How dependencies in a system should drive the choice between graphs, simplicial complexes and hypergraphs, and what is lost or assumed when converting between them.
tags: [representations, hypergraphs, simplicial-complexes, higher-order, dependencies]
---

:::{tip} TL;DR
- Choosing a representation is a modelling decision that comes **after** identifying the system's **dependencies**. A dependency means one relation's existence carries information about another's. The paper names three: **subset**, **temporal** and **spatial**. On top of these come external ones introduced by data availability, by how the data were acquired or processed, and by the research question.
- The three formalisms differ in which relations they can hold. **Graphs** hold only dyadic relations. **Simplicial complexes** hold polyadic relations but must be *downward closed*. **Hypergraphs** hold polyadic relations in which every hyperedge is independent.
- Converting **down** (hypergraph → simplicial complex → graph) *forgets* information. Converting **up** (graph → clique complex → hypergraph) *adds assumptions*. The round trip G → K → H → K → G returns the original graph, but no round trip starting from a hypergraph is guaranteed to.
- Even something as basic as **degree** changes ranking with the representation. On DBLP the Spearman correlation between graph degree and hypergraph degree drops below 0.5 in some years. On Enron, team clustering measured on the graph and on the hypergraph has Spearman $r = 0.1$.
- A method being available only for one formalism (e.g. epidemic thresholds on graphs) is **not** a reason to use that formalism.
:::

- **Source.** [](doi:10.1137/20M1355896) (Torres, Blevins, Bassett & Eliassi-Rad, *SIAM Review* 63(3), 2021; preprint [arXiv:2006.02870](https://arxiv.org/abs/2006.02870)).
- **Builds on.** Basic graph definitions ([Newman ch. 6 notes](../../nets-5116/newman/06-mathematics-of-networks.md)).
- **Notation.** Shared symbols as in [](#notation). Relations are $r \in R$ with $r \subseteq V$, and attributes are given by a map $p: V \times R \to P$.

(sec-repr-definitions)=
## Setup and definitions

The paper's main aim is a shared, domain-agnostic vocabulary. Its pipeline runs: system → dependencies → formalism → (optional) conversion → methods → interpretation.

:::{prf:definition} Units, relations, systems
:label: def-repr-system

- A **unit** (element, node) is an individual part of a system; the set of units is $V$.
- A **relation** is a set $r \subseteq V$ of related units. It is **dyadic** if $\lvert r \rvert = 2$ and **polyadic** if $\lvert r \rvert > 2$. $R$ is the set of relations.
- A **system** is a collection $(V, R)$ that needs no other pieces to function or to interact with its environment. The patterns in $R$ are its **structure**, and its activity over time is its **function**.
- A **complex system** is one whose units and relations together behave qualitatively differently from the units acting alone.
- A **system fragment** is the subset of nodes and relations that is actually observed. Fragments need not function as systems themselves, and almost every dataset is one.
:::

:::{prf:definition} Formalism, representation, encoding
:label: def-repr-formalism

A **formalism** is a mathematical framework (graph, simplicial complex, hypergraph). A **representation** is one concrete object built in that formalism for a specific system or fragment. In programming terms, the formalism is the *class* and the representation the *object*. **Encoding** is the step that turns data into a representation.
:::

:::{prf:definition} Dependency
:label: def-repr-dependency

A **dependency** is a property of a system in which the existence of one relation provides information about the existence of another.
:::

The paper deliberately reserves "higher order" for HONs (see [below](#sec-repr-variations)). It avoids the common use of the term as a synonym for "polyadic".

(sec-repr-dependencies)=
## Core ideas

### Three intrinsic dependencies

| Dependency | Formal statement | Canonical example | Failure if ignored |
|---|---|---|---|
| **Subset** | If $r \in R$ and $r' \subset r$, then $r' \in R$ whenever a predicate $P(r')$ holds. If $P \equiv$ true, *every* subset is a relation. | Objects sharing a feature: if three squares share "square", so does every pair. Chemical reactions **lack** this property: $\{\mathrm{H_2}, \mathrm{O_2}, \mathrm{H_2O}\} \in R$ but $\{\mathrm{O_2}, \mathrm{H_2O}\} \notin R$. | Degree conflates one big group with many separate pairs. "Marta has $p$ contacts" could mean $p$ conversations or one conversation with $p$ people. |
| **Temporal** | The behaviour of a unit at time $t$ affects the behaviour of some unit at $t' > t$, so walks are **non-Markovian**. | Subway routes: the graph of consecutive stops implies a route B–D–E–F that no passenger ever takes. | A graph treats edges $(i,j)$ and $(j,k)$ as independent, so it invents paths and misweights rarely used edges. |
| **Spatial** | The distance between nodes influences the probability of the relation that contains them. Typically $\Pr(r) = f(\text{distances among } r)$. | Brain white-matter tracts and transport links, where long edges are costly. | Structure gets attributed to the wrong cause, e.g. an outbreak blamed on a regional food rather than contact. A costly long edge looks no more important than a cheap short one. |

### External dependencies

Dependencies can also come from outside the system:

- **Data availability.** With only a fragment, the observed subset dependency may reflect sparse sampling rather than the true predicate $P$.
- **Acquisition or processing.** Thresholded correlation matrices induce a **transitivity** dependency, a special case of subset dependency. If A~B and B~C are highly correlated, A~C usually is too, whether or not the system relates them.
- **Research question.** The question fixes what counts as a relation. Take proteins: "two proteins in the same complex" has a subset dependency, but "the set of proteins forming one complex" does not. A question that is too narrow can also hide a dependency that matters, such as spatial confounding in the food-outbreak example.

:::{important} The definition of a relation decides which dependencies a representation carries
Whether a representation exhibits a dependency is often a question of semantics. In the paper's brain example, three definitions of "related" give different results: "all required by a task", "co-active during a task" and "pairwise similar". Only co-activation carries a subset dependency. The bus example works the same way. "Stations forming a whole route" carries no dependency. "Stations sharing a line" carries a subset dependency. "Consecutive stops" is pairwise and fits a graph. None of the three encodes temporal dependency. That requires passenger trajectories, which call for a HON.
:::

(sec-repr-formalisms)=
### The three formalisms

:::{prf:definition} Graph, simplicial complex, hypergraph
:label: def-repr-three

- **Graph.** $G = (V, E)$, where each edge is an unordered pair of nodes. Only dyadic relations are possible.
- **Simplicial complex.** $K = (V, R)$ with **downward closure**: if $r \in R$ and $r' \subset r$, then $r' \in R$. A set of $k+1$ vertices is a **$k$-simplex**. $K$ is fully determined by its **maximal simplices**, so it can be stored as a binary matrix of maximal simplices × vertices.
- **Hypergraph.** $\mathcal{H} = (V, \mathcal{E})$ with $\mathcal{E}$ any set of subsets of $V$, so there is no closure requirement. It is stored as a binary incidence matrix of hyperedges × vertices.
:::

The key difference between a simplicial complex and a hypergraph is the **sub-relation**. Take the relations $\{a,b\}$, $\{a,b,c\}$ and $\{a,b,d\}$. In a simplicial complex, $\{a,b\}$ is by definition a *face* of both triangles. In a hypergraph, you cannot tell whether $\{a,b\}$ is a sub-edge of $\{a,b,c\}$, of $\{a,b,d\}$, of both or of neither. Each hyperedge is an independent observation.

| | Graph | Simplicial complex | Hypergraph |
|---|---|---|---|
| Relations | dyadic only | polyadic, downward closed | polyadic, independent |
| Natural fit | genuinely pairwise systems, path questions | subset dependency with $P \equiv$ true | subset dependency only for *some* subsets, or none |
| Distinctive analysis (per the paper) | core–periphery structure | homology, i.e. cavities | absent substructures, fill coefficient |
| Theory | centuries | applied topology since the 2000s | flexible but fewest formal tools |

(sec-repr-variations)=
### Variations

- **Directed.** In graphs, edges become ordered pairs. In simplicial complexes, simplices carry an *orientation* given by vertex order. In hypergraphs, a **hyperarc** is a pair of disjoint vertex sets (sources, sinks).
- **Weighted.** A weight function $W: R \to \mathbb{R}$. In a simplicial complex the weights must respect closure: $r' \subseteq r \Rightarrow W(r) \le W(r')$, so a face is at least as strong as any simplex containing it. This is what makes a weighted complex a filtration for **persistent homology**. Hypergraph weights carry no such constraint.
- **Dynamic.** A sequence $G_1, \dots, G_T$ on the same node set, and likewise for complexes and hypergraphs. For complexes the matching tools are vineyards and zig-zag persistence.
- **Multilayer / multiplex.** One layer per relation type. A *multiplex* has the same node set in every layer. A dynamic network can be read as a multilayer network whose layers are ordered in time.
- **Higher-order networks (HONs).** Nodes are *path-conditioned states*: station D becomes $D_B$ ("arrived from B") and $D_C$. Transitions are then Markovian on the new node set, so a temporal dependency is encoded inside a graph. At the time of writing HONs were defined only for paths on graphs. Extending them to complexes and hypergraphs was left open.
- **Other formalisms mentioned:** graphons, metapopulation models, random sequences of sets and sheaves.

### Encoding the dependencies

- **Subset → simplicial complex** if *every* subset of a relation is a relation. Use a **hypergraph** if only some are; the predicate $P$ then picks out a particular hypergraph.
- **Temporal → HON**, built from observed paths.
- **Spatial → edge weights**, but the weights may already be in use for something else, e.g. traffic flow versus road length. The paper gives three options: aggregate both into one weight, use a multilayer network with one quantity per layer, or build a joint representation.
- Real systems usually carry several dependencies at once, e.g. subway = temporal + spatial and coauthorship = temporal + subset + spatial. Representing several together is posed as an open problem.

(sec-repr-results)=
## Key results

### Converting between formalisms

| Map | Construction | Cost |
|---|---|---|
| $\mathcal{H} \to K$ | downward closure of each hyperedge; keep the maximal rows of the incidence matrix | **forgets** hyperedges contained in larger ones, and the count of relations each node is in |
| $K \to G$ | 1-skeleton | **forgets** polyadic relations: a filled triangle and a hollow triangle both become a 3-clique |
| $\mathcal{H} \to G$ | join every pair inside a hyperedge | same graph as $\mathcal{H} \to K \to G$ |
| $G \to K$ | **clique (flag) complex** $X(G)$: every $(k{+}1)$-clique becomes a $k$-simplex | **assumes** every clique is a functional group. This fails when three people only ever talk in pairs. |
| $K \to \mathcal{H}$ | (a) every simplex and all its faces become hyperedges, or (b) only maximal simplices do (the conservative choice) | **assumes** which relations are independent |

:::{prf:proposition} Asymmetry of round trips
:label: prop-repr-roundtrip

For any graph $G$, the round trip $G \to X(G) \to \mathcal{H}_{\max} \to X(G) \to G$ returns $G$, using option (b) for $K \to \mathcal{H}$. A round trip starting from a hypergraph does not in general return the original hypergraph.
:::

:::{dropdown} Why
The 1-simplices of $X(G)$ are exactly the edges of $G$. Taking the downward closure of the maximal simplices of $X(G)$ rebuilds $X(G)$. So every step on the way back up is undone exactly on the way down.

In the other direction, the map $\mathcal{H} \to G$ is not injective. (This example is mine, not the paper's.) The hypergraphs $\{\{a,b,c\}\}$ and $\{\{a,b\},\{b,c\},\{a,c\}\}$ both give the triangle on $a, b, c$. No inverse can tell them apart. The general point is that hyperedges are independent of their supersets, so information lost going down cannot be recovered going up.
:::

:::{warning} Convert with care
The paper places conversion as an *optional* pipeline step to be taken "only with extreme care". Every translation either forgets relations and independencies or adds assumptions.
:::

### Methods for each formalism

**Graphs.** Degree $k_i$; local clustering

$$
C_i = \frac{2\mu_i}{k_i (k_i - 1)},
$$ (eq-repr-clustering)

where $\mu_i$ is the number of edges among $i$'s neighbours. Graph methods also include path lengths, centralities, modularity and small-worldness. The paper names **core–periphery** structure as the one statistic it found unique to graphs at the time.

**Simplicial complexes.**
- The **simplex participation** vector $P(v_i)$: its $k$-th entry is the number of $(k-1)$-simplices containing $v_i$.
- Variants are the upper degree and the participation in maximal simplices. There are also simplicial clustering and centrality.
- **Homology** detects cavities, and **persistent homology** tracks them across a weighted complex. Both rely on downward closure, which is why they belong to this formalism.
- The **Dowker dual** transposes the concurrence matrix (simplices × nodes), swapping the roles of nodes and relations. The homology groups of a complex and its Dowker dual are isomorphic. The dual is therefore cheaper to analyse when relations are far fewer than nodes, as in the zebrafish neural recordings. It is the analogue of a line graph.

**Hypergraphs.**
- **Hyperdegree** $d_{\mathcal{H}}(v_i)$ is the number of hyperedges containing $v_i$. It is deliberately *not* stratified by cardinality, because a large hyperedge says nothing about smaller ones.
- The **cardinality** of a hyperedge is $\lvert e \rvert$.
- The **hypergraph clustering coefficient** (as cited in the paper) is built on the **extra overlap** of two hyperedges. With $D_{j,k} = e_j \setminus e_k$ and $\mathcal{N}(U)$ the neighbours of the nodes in $U$:

$$
EO(e_j, e_k) = \frac{\lvert \mathcal{N}(D_{j,k}) \cap D_{k,j} \rvert + \lvert D_{j,k} \cap \mathcal{N}(D_{k,j}) \rvert}{\lvert D_{j,k} \rvert + \lvert D_{k,j} \rvert},
\qquad
C_{\mathcal{H}}(v_i) = \binom{\lvert M(v_i) \rvert}{2}^{-1} \sum_{e_j, e_k \in M(v_i)} EO(e_j, e_k),
$$ (eq-repr-hyperclustering)

where $M(v_i)$ is the set of hyperedges containing $v_i$, and $C_{\mathcal{H}}(v_i) = 0$ if $d_{\mathcal{H}}(v_i) = 1$. When every hyperedge has cardinality 2, this reduces exactly to {eq}`eq-repr-clustering`. Two edges $\{v,a\}$ and $\{v,b\}$ have $EO = 1$ if $a \sim b$ and $0$ otherwise, so the average over pairs of neighbours is $C_i$.

- The **fill coefficient** (introduced in this paper) measures the *absent substructures* that only a hypergraph can express:

$$
f(h) = \frac{\lvert \{ g \in \mathcal{E} : g \subsetneq h,\ \lvert g \rvert > 1 \} \rvert}{2^{\lvert h \rvert} - 2 - \lvert h \rvert}.
$$ (eq-repr-fill)

The denominator counts the possible proper sub-hyperedges of size at least 2. It is $2^{\lvert h \rvert}$ minus the empty set, minus the $\lvert h \rvert$ singletons, minus $h$ itself.

### Empirical results

| Dataset | Comparison | Finding |
|---|---|---|
| DBLP coauthorship: 3,700,681 papers by 1,930,378 authors, 2000–2016, one representation per year | node degree in the graph, the simplicial complex (maximal-simplex participation) and the hypergraph | All three are positively correlated, but **less so at low degree**: the representations agree on the hubs, not on the many small nodes. The Spearman correlation is highest between the simplicial complex and the hypergraph, both of which keep polyadic relations. Graph vs hypergraph falls **below 0.5** in some years. |
| Enron email: 10,883 emails among 148 employees, Mar 1999–Oct 2002; a "team" is an email with 5–25 participants | mean clustering of a team's members, graph {eq}`eq-repr-clustering` vs hypergraph {eq}`eq-repr-hyperclustering` | Spearman $r = 0.1$ ($p = 0.16$), unchanged for minimum team sizes 6, 7 and 8. The two would rank teams for intervention completely differently. The fill coefficient (internal cohesion) shows no visible relation to either. |

The Enron case is the cleanest demonstration. The research question is fixed, the data are complete and dependencies barely interact, yet the representation alone changes the answer.

## Worked example

This is the paper's toy coauthorship system: four papers, $p_1 = \{a_1, a_2\}$, $p_2 = \{a_2, a_4\}$, $p_3 = \{a_1, a_2, a_3\}$ and $p_4 = \{a_3, a_4\}$. Each question you ask of the data gives a different representation:

- "Has this **pair** written together?" gives the **graph**.
- "Is this **set** a subset of some paper's authors?" gives the **simplicial complex**. Its maximal simplices are $\{a_1,a_2,a_3\}$, $\{a_2,a_4\}$ and $\{a_3,a_4\}$.
- "Has **exactly** this set written a paper?" gives the **hypergraph**, with one hyperedge per paper.

| Author | Graph degree | Maximal simplices | Hyperdegree | After $G \to X(G) \to \mathcal{H}$ |
|---|---|---|---|---|
| $a_1$ | 2 | 1 | 2 | 1 |
| $a_2$ | **3** | **2** | **3** | 2 |
| $a_3$ | **3** | **2** | 2 | 2 |
| $a_4$ | 2 | 2 | 2 | 1 |

- **Who is most productive?** The graph and the simplicial complex tie $a_2$ and $a_3$. Only the hypergraph shows that $a_2$ is on more papers than anyone else.
- **How do $a_1$ and $a_4$ collaborate?** In the graph they look the same, since both are linked to $a_2$ and $a_3$. The simplicial complex shows $a_1$ in a three-author group and $a_4$ only in pairs. The hypergraph adds that $a_1$ also has a separate two-author paper with $a_2$.
- **Converting instead of building from the data.** The clique complex of the graph has maximal simplices $\{a_1,a_2,a_3\}$ and $\{a_2,a_3,a_4\}$. The triangle $a_2 a_3 a_4$ is invented, since no paper has those three authors. Turning the maximal simplices into hyperedges then gives two 3-author "papers", and $a_2 \equiv a_3$ and $a_1 \equiv a_4$ in *every* representation.
- **Fill coefficient** of $p_3$: of the 3 possible pairs inside it, only $\{a_1,a_2\}$ is a hyperedge, so $f(p_3) = 1/3$.

(I recomputed all values in the table from the four author lists.)

## Assumptions and limitations

- **Scope.** This is a perspective and tutorial paper, not a theory paper. The dependency taxonomy is explicitly non-exhaustive, and the methods per formalism are a sample, not a survey.
- **Unique to a formalism, as of writing.** Claims like "core–periphery is unique to graphs" or "HONs exist only for graphs" describe the 2020–21 literature. *My comment:* treat them as dated pointers, not as impossibility results.
- **The fill coefficient is proposed here.** In the paper it is illustrated on Enron by eye, not validated as a statistic.
- **"Little correlation" on Enron** is a rank correlation of 0.1 that is not statistically significant ($p = 0.16$). The evidence is that the two clustering coefficients are *not aligned*, not that they are anticorrelated.
- **Several dependencies at once.** The paper poses representing several dependencies together (e.g. temporal + subset) as open. It gives no recipe.

## Connections

- **NETS 5116.**
  - Newman's *bipartite networks* are the same object as a hypergraph's node–hyperedge incidence matrix, and his one-mode projection is the $\mathcal{H} \to G$ map above ([Newman ch. 6 notes](../../nets-5116/newman/06-mathematics-of-networks.md)).
  - Local clustering {eq}`eq-repr-clustering` is the standard Watts–Strogatz definition.
- **NETS 6116.** Graphons are listed here as another formalism. Krioukov's notes treat them as limits of dense graph sequences.
- **PHYS 7335.**
  - The paper's warning example is the **epidemic threshold**. Theory existed for graphs while contagion on hypergraphs and simplicial complexes was still nascent, and that alone does not justify encoding a polyadic system as a graph.
  - Metapopulation models appear here as a formalism of their own.
- **NETS 7332.**
  - Higher-order homophily ([reading 03](./03-higher-order-homophily.md)) measures homophily directly on hypergraphs. That is the polyadic, independent-hyperedge setting this paper argues for when group interactions are the relation.
  - Hypergraph and simplicial neural networks appear later in the course, in the hypergraphs topic.

## Self-test

:::{dropdown} Q1. State the definition of a subset dependency. Give one system that has it and one that does not.
If $r \in R$ and $r' \subset r$, then $r' \in R$ whenever a predicate $P(r')$ holds.
- **Has it ($P \equiv$ true):** objects sharing a visual feature, or neurons co-firing.
- **Lacks it:** chemical reactions. $\{\mathrm{H_2},\mathrm{O_2},\mathrm{H_2O}\}$ is a reaction, but $\{\mathrm{O_2},\mathrm{H_2O}\}$ is not.
:::

:::{dropdown} Q2. Why does the graph of consecutive subway stops misrepresent passenger routes? What fixes it?
A graph assumes walks are Markovian: traversing $(i,j)$ is independent of how you reached $i$. That makes routes like B–D–E–F available even though no passenger takes them. A **HON** fixes this by splitting nodes into path-conditioned states ($D_B$, $D_C$, $E_{DB}$, …), which restores Markovianity on the new node set.
:::

:::{dropdown} Q3. What does each conversion forget or assume: H→K, K→G, G→K?
- **H→K** forgets hyperedges contained in larger ones, and how many relations each node is in.
- **K→G** forgets polyadic relations: a filled triangle looks the same as a hollow one.
- **G→K** (clique complex) assumes every clique is a genuine group.
:::

:::{dropdown} Q4. Why can't simplicial-complex weights be arbitrary, when hypergraph weights can?
Downward closure means any face of a simplex is related at least as strongly as the simplex itself, so weights must satisfy $W(r) \le W(r')$ for $r' \subseteq r$. That monotonicity is what turns a weighted complex into a filtration for persistent homology. Hyperedges are independent, so they carry no such constraint.
:::

:::{dropdown} Q5. Show that the hypergraph clustering coefficient reduces to the graph clustering coefficient for 2-uniform hypergraphs.
Hyperedges at $v$ are edges $\{v,a\}$, so the sets $D$ are $\{a\}$ and $\{b\}$. $EO = (1+1)/2 = 1$ if $a \sim b$ and $0$ otherwise. Averaging over the $\binom{k_v}{2}$ pairs gives $\mu_v / \binom{k_v}{2} = C_v$.
:::

:::{dropdown} Q6. What is the denominator of the fill coefficient counting?
The number of proper subsets of $h$ with at least 2 elements: $2^{\lvert h \rvert} - 1 - \lvert h \rvert - 1$. That is, remove the empty set, the singletons and $h$ itself.
:::

:::{dropdown} Q7. In DBLP, where do the representations disagree most about degree, and why does that matter?
At **low degree**. Hubs rank similarly in all three representations, but the many small-degree nodes do not. Any claim about low-degree nodes, usually the majority, therefore depends on the representation.
:::

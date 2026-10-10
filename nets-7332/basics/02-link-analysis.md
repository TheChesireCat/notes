---
title: Link Analysis — PageRank, Personalized PageRank and Random Walk with Restart
short_title: Link analysis
subject: NETS 7332 · Basics
description: PageRank as the stationary distribution of a teleporting random walk, its personalised variants as node-proximity scores, and how they relate to eigenvector, Katz and HITS centralities.
tags: [pagerank, random-walks, centrality, personalized-pagerank, hits]
---

:::{tip} TL;DR
- **PageRank** solves $r = Mr$ for the column-stochastic matrix $M = A D_{\mathrm{out}}^{-1}$. The vector $r$ is both the leading eigenvector of $M$ and the stationary distribution of a random surfer.
- Plain $M$ fails in two ways. **Spider traps** absorb all the mass, and **dead ends** leak it. **Teleportation** fixes both: $G = \beta M + \tfrac{1-\beta}{N}\mathbf{1}\mathbf{1}^\top$ is strictly positive, so Perron–Frobenius guarantees a unique positive $r$, and power iteration converges from any start.
- Convergence is geometric: $\lVert r^{(t)} - r \rVert_1 \le 2\beta^t$. The eigenvalues of $G$ other than 1 are $\beta$ times those of $M$, so $\lvert\lambda_2(G)\rvert \le \beta$.
- **Personalized PageRank** teleports to a distribution $v$ concentrated on a set $S$; **random walk with restart** has $v = e_q$. The closed form is $r = (1-\beta)(I-\beta M)^{-1}v = (1-\beta)\sum_{t\ge0}\beta^t M^t v$, the end-point distribution of a walk with geometric length.
- Within one family of centralities: eigenvector ($x \propto Ax$), Katz ($x = (I-\alpha A)^{-1}\mathbf 1$) and PageRank (Katz with out-degree normalisation). HITS splits importance into authority (leading eigenvector of $AA^\top$) and hub (leading eigenvector of $A^\top A$).
:::

- **Source.** Leskovec, CS224W (Fall 2021), lecture 4, [*Link Analysis: PageRank*](https://snap.stanford.edu/class/cs224w-2021/slides/04-pagerank.pdf); [](doi:10.1016/S0169-7552(98)00110-X) (Brin & Page 1998); [](doi:10.1137/140976649) (Gleich 2015, *PageRank beyond the web*); Haveliwala & Kamvar, [*The second eigenvalue of the Google matrix*](https://nlp.stanford.edu/pubs/secondeigenvalue.pdf) (Stanford tech. report, 2003); Newman, *Networks* (2nd ed.), §7.1.
- **Builds on.** Eigenvector and Katz centrality ([Newman ch. 7 notes](../../nets-5116/newman/07-measures-and-metrics.md)); the graph-ML task framing in [graph-ML tasks and features](./01-graph-ml-tasks-and-features.md).
- **Notation.** Shared symbols as in [](#notation); in particular $A_{ij}=1$ for an edge $j \to i$. Page-specific symbols:
  - $D_{\mathrm{out}} = \mathrm{diag}(k_1^{\mathrm{out}},\dots,k_N^{\mathrm{out}})$;
  - $M$ is the column-stochastic transition matrix;
  - $r$ is the rank vector;
  - $v$ is the teleport (preference) distribution;
  - $\beta$ is the **damping**, i.e. the probability of following a link. Here $\beta$ is *not* the transmission rate.

(sec-la-definitions)=
## Setup and definitions

Treat a directed graph as a web of pages and hyperlinks. The goal is a score $r_i \ge 0$ with $\sum_i r_i = 1$ that ranks node $i$ by **importance**. Importance comes from in-links, and each in-link counts in proportion to the importance of the node it comes from. The lecture calls this "links as votes".

:::{prf:definition} Flow equations and the stochastic adjacency matrix
:label: def-la-flow

Each node splits its importance evenly over its out-links, so

$$
r_i = \sum_{j \to i} \frac{r_j}{k_j^{\mathrm{out}}}.
$$ (eq-la-flow)

In matrix form $r = Mr$, with $M_{ij} = 1/k_j^{\mathrm{out}}$ if $j \to i$ and $0$ otherwise. Under the convention $A_{ij}=1$ for $j\to i$, this means $M = A D_{\mathrm{out}}^{-1}$. If no node is a dead end, every column of $M$ sums to 1: $M$ is **column stochastic**.
:::

:::{prf:definition} Random surfer
:label: def-la-surfer

A surfer at node $j$ moves to an out-neighbour chosen uniformly at random. If $p^{(t)}$ is the distribution of the surfer's position at time $t$, then $p^{(t+1)} = M p^{(t)}$. A **stationary distribution** is any $p$ with $p = Mp$. So a solution of the flow equations {eq}`eq-la-flow` is *simultaneously* the eigenvector of $M$ with eigenvalue 1 and a stationary distribution of the random surfer.
:::

:::{prf:definition} Dead ends and spider traps
:label: def-la-pathologies

- A **dead end** (dangling node) has $k^{\mathrm{out}} = 0$. Its column of $M$ is zero, so $M$ is only *sub*-stochastic and probability mass leaks out of the system.
- A **spider trap** is a set of nodes with no edges leaving the set, i.e. a closed class of the Markov chain. Repeated multiplication by $M$ moves all the mass into it.
:::

:::{prf:definition} Google matrix and PageRank
:label: def-la-google

With probability $\beta$ the surfer follows a random out-link. With probability $1-\beta$ it **teleports** to a node drawn from a distribution $v$. Dead ends are patched first: from a dead end the surfer teleports with probability 1. The result is

$$
G = \beta M + (1-\beta)\, v \mathbf{1}^\top, \qquad r = G r, \quad \mathbf{1}^\top r = 1.
$$ (eq-la-google)

**PageRank** is the case $v = \mathbf{1}/N$, giving $G = \beta M + \tfrac{1-\beta}{N}\mathbf{1}\mathbf{1}^\top$. The lecture quotes $\beta \in [0.8, 0.9]$ in practice; Brin & Page used $0.85$. With $\beta = 0.8$, the surfer makes about 5 link steps between teleports on average.
:::

:::{prf:definition} Personalized PageRank and random walk with restart
:label: def-la-ppr

- **Personalized** (topic-specific) **PageRank** is {eq}`eq-la-google` with $v$ supported on a set $S$ of query nodes; $v$ can be non-uniform on $S$. It ranks nodes by **proximity to $S$**, not by global importance.
- **Random walk with restart (RWR)** is the special case $v = e_q$: the surfer always restarts at a single node $q$.
:::

(sec-la-core)=
## Core ideas

### Why the eigenvector view and the surfer view coincide

Iterating $p^{(t+1)} = Mp^{(t)}$ from any start is **power iteration** on $M$. Whenever the iteration converges, the limit satisfies $p = Mp$. The lecture's recipe is:

1. Start from $r^{(0)} = \mathbf{1}/N$.
2. Iterate.
3. Stop when $\lVert r^{(t+1)} - r^{(t)}\rVert_1 < \varepsilon$.

It notes that about 50 iterations usually suffice. Gaussian elimination costs $O(N^3)$, which is hopeless at web scale. One power-iteration step costs $O(L)$ because $M$ is sparse, and the teleport term adds only a constant vector.

### What goes wrong without teleportation, and why teleportation fixes it

| Pathology | Effect on $M^t p$ | Fix |
|---|---|---|
| Spider trap (closed class) | all mass ends up inside the trap; the scores are well defined but useless | teleport out with probability $1-\beta$ every step, so the surfer escapes in a geometric number of steps |
| Dead end | $M$ is sub-stochastic; total mass decays to 0 | make the column stochastic: from a dead end, teleport with probability 1 |
| Several closed classes / periodicity | stationary distribution not unique, or iteration oscillates | the teleport term makes every entry of $G$ positive |

The lecture's summary: spider traps are "not a problem" mathematically, but they give the wrong scores. Dead ends *are* a problem, because $M$ then violates the assumptions.

### Handling dead ends: patch the matrix, or renormalise afterwards

There are two common recipes for dead ends:

- **CS224W:** patch each dead-end column of $M$ to $v$ before forming $G$.
- **Newman:** set $D_{ii} = \max(k_i^{\mathrm{out}}, 1)$, solve the *leaky* linear system $x = (I - \beta A D^{-1})^{-1}\mathbf 1$, and use $x$ as the centrality.

These agree up to normalisation. Gleich (2015, Thm 2.5) calls the patched system **strongly preferential** PageRank and the leaky one **pseudo-PageRank**, and proves that normalising the pseudo-PageRank solution recovers strongly preferential PageRank. Gleich also describes two alternatives:
- **weakly preferential:** from a dead end, jump uniformly, whatever $v$ is;
- **sink preferential:** stay at the dead end until a teleport.

These give genuinely different scores. Which one a paper uses is often left implicit.

### Personalisation as proximity

Replacing $\mathbf 1/N$ by $v$ changes the question from "which nodes are important?" to "which nodes are close to $S$?". RWR from $q$ scores node $j$ by how often a walker that keeps restarting at $q$ visits $j$. The lecture lists why this is a good proximity measure: it rewards multiple connections, multiple paths, direct and indirect links, and it accounts for degree.

### HITS: hubs and authorities

Kleinberg's **HITS** (Newman §7.1.5) gives each node two scores:
- **authority** $x$: being pointed to by good hubs;
- **hub** $y$: pointing to good authorities.

With $A_{ij}=1$ for $j\to i$, the definitions are

$$
x_i = \alpha \sum_j A_{ij} y_j, \qquad y_i = \alpha' \sum_j A_{ji} x_j
\quad\Longrightarrow\quad
A A^\top x = \lambda x,\quad A^\top A\, y = \lambda y,\quad \lambda = (\alpha\alpha')^{-1}.
$$ (eq-la-hits)

Both matrices are positive semidefinite and share their nonzero eigenvalues, since $AA^\top x = \lambda x$ implies $A^\top A (A^\top x) = \lambda A^\top x$. One takes the leading eigenvectors. Kleinberg's paper writes $A_{ij}=1$ for $i\to j$, so there the two matrices appear swapped. Check the convention before matching formulas.

### One family of centralities

Newman's Table 7.1 organises the spectral centralities along two choices: whether to divide by out-degree, and whether to add a constant term.

| | constant term | no constant term |
|---|---|---|
| **divide by out-degree** | PageRank $x = (I - \beta AD^{-1})^{-1}\mathbf 1$ | $x = AD^{-1}x$; degree centrality in the undirected case |
| **no division** | Katz $x = (I - \alpha A)^{-1}\mathbf 1$ | eigenvector $x = \Lambda_{\max}^{-1} A x$ |

- **Katz** needs $\alpha < 1/\Lambda_{\max}$ for the series $\sum_t \alpha^t A^t \mathbf 1$ to converge. That series counts walks into $i$, attenuated by length.
- **PageRank** makes the same move, but dilutes each in-link by the source's out-degree. A node pointing at a million pages passes each of them only a sliver of its importance.
- The constant term is what rescues nodes outside strongly connected components, which get zero eigenvector centrality in a directed graph.

(sec-la-results)=
## Key results

:::{prf:theorem} Existence, uniqueness, positivity
:label: thm-la-unique

For $0 \le \beta < 1$ and a teleport vector $v > 0$ (e.g. $v = \mathbf 1/N$), the patched matrix $G$ in {eq}`eq-la-google` is column stochastic with all entries positive. Hence:
- 1 is a simple eigenvalue of $G$, strictly larger in modulus than every other eigenvalue;
- its eigenvector $r$ can be chosen positive, and $\mathbf 1^\top r = 1$ fixes it uniquely;
- the Markov chain is irreducible and aperiodic, and $G^t p \to r$ for every probability vector $p$.
:::

:::{dropdown} Why (Perron–Frobenius)
$G$ is column stochastic: $\mathbf 1^\top G = \beta \mathbf 1^\top M + (1-\beta)(\mathbf 1^\top v)\mathbf 1^\top = \mathbf 1^\top$. So $\mathbf 1$ is a left eigenvector with eigenvalue 1, and the spectral radius is 1, because $\lVert G\rVert_1 = 1$. Every entry is at least $(1-\beta)\min_i v_i > 0$.

For a strictly positive matrix, Perron's theorem says the spectral radius is a simple eigenvalue with a positive eigenvector, and every other eigenvalue has strictly smaller modulus. In Markov-chain language: every state reaches every other state in one step, which gives irreducibility, and $G_{ii} > 0$, which gives aperiodicity. So the chain is ergodic and converges to its unique stationary distribution.

With personalisation ($v$ zero outside $S$), $G$ is no longer strictly positive. Uniqueness still holds, from the linear-system view: $I - \beta M$ is a nonsingular M-matrix, a point Gleich makes.
:::

:::{prf:theorem} Linear-system form and geometric-walk interpretation
:label: thm-la-closed

Let $M$ be column stochastic (dead ends patched) and $0\le\beta<1$. The solution of $r = \beta M r + (1-\beta) v$ is

$$
r = (1-\beta)(I - \beta M)^{-1} v = (1-\beta) \sum_{t=0}^{\infty} \beta^t M^t v .
$$ (eq-la-closed)

The vector $r$ is the distribution of $X_T$, where the walk starts from $v$ and runs for a random time $T$ with $\Pr(T=t) = (1-\beta)\beta^t$.
:::

:::{dropdown} Derivation
Substitute $\mathbf 1^\top r = 1$ into $r = Gr$ to get $Gr = \beta M r + (1-\beta) v$, then rearrange. The Neumann series converges because the spectral radius of $\beta M$ is $\beta < 1$. The $t$-th term $(1-\beta)\beta^t M^t v$ is the probability of stopping after exactly $t$ steps times the distribution after $t$ steps.

**Two consequences:**
- **Linearity in $v$.** The PPR vector for $v = \sum_s w_s e_s$ is $\sum_s w_s\,\mathrm{RWR}(s)$. In particular, global PageRank is the average of the $N$ RWR vectors.
- **Locality.** Small $1-\beta$ means long walks and global scores. Large $1-\beta$ keeps the mass near $S$.

Tong, Faloutsos & Pan [](doi:10.1109/ICDM.2006.70) write RWR as $(1-c)(I-c\tilde W)^{-1}e_i$ and precompute $(I-c\tilde W)^{-1}$ for fast queries.
:::

:::{prf:theorem} Convergence of power iteration
:label: thm-la-rate

Iterate $r^{(t+1)} = \beta M r^{(t)} + (1-\beta) v$ from $r^{(0)} = v$. Then

$$
\lVert r - r^{(t)} \rVert_1 \le 2\beta^t .
$$ (eq-la-rate)

Moreover, if $M$ has eigenvalues $1, \mu_2, \dots, \mu_N$, then $G$ has eigenvalues $1, \beta\mu_2, \dots, \beta\mu_N$. So $\lvert \lambda_2(G) \rvert \le \beta$, with equality when $M$ has at least two closed classes (Haveliwala & Kamvar 2003), as the web graph does.
:::

:::{dropdown} Derivation
**Error bound** (Gleich, Thm 2.2). Subtract the update from the fixed-point equation: $r - r^{(t+1)} = \beta M (r - r^{(t)})$. A column-stochastic $M$ has $\lVert M\rVert_1 = 1$, so the error shrinks by at least a factor $\beta$ per step. The initial error $\lVert r - v\rVert_1$ is at most 2.

**Spectrum.** Both $M$ and $v\mathbf 1^\top$ have $\mathbf 1^\top$ as a left eigenvector: $\mathbf 1^\top M = \mathbf 1^\top$ and $\mathbf 1^\top v \mathbf 1^\top = \mathbf 1^\top$. Take an orthogonal $U$ whose first column is $\mathbf 1/\sqrt N$. Then $U^\top M U$ has first row $e_1^\top$, so

$$
U^\top M U = \begin{pmatrix} 1 & 0 \\ b & \tilde M \end{pmatrix},
$$

and the eigenvalues of $M$ are $1$ together with those of $\tilde M$. The teleport term gives $U^\top v\mathbf 1^\top U = \sqrt N\,(U^\top v)\, e_1^\top$, which is nonzero only in the first column, with top entry $\mathbf 1^\top v = 1$. Hence

$$
U^\top G U = \begin{pmatrix} 1 & 0 \\ \beta b + (1-\beta) d & \beta\tilde M \end{pmatrix}
$$

for some vector $d$. The eigenvalues of $G$ are therefore $1$ and $\beta\mu_2,\dots,\beta\mu_N$. Haveliwala & Kamvar prove the same statement, and the equality case, in the row-stochastic convention.

**Practice.** With $\beta = 0.85$ the bound needs 118 iterations for $10^{-8}$. With $\beta = 0.8$, 50 iterations give $2\cdot 0.8^{50} \approx 3\times 10^{-5}$. The actual rate is $\lvert\beta\mu_2\rvert$, which can be much better than $\beta$ (see the worked example).
:::

:::{prf:proposition} Undirected graphs: the plain random walk is degree-proportional
:label: prop-la-undirected

On a connected undirected graph, $M = AD^{-1}$ has stationary distribution $\pi_i = k_i / 2L$. Without teleportation, "PageRank" therefore carries no information beyond degree. This is Newman's observation that the no-constant-term entry of the table reduces to degree centrality.
:::

:::{dropdown} Why
$(AD^{-1}k)_i = \sum_j A_{ij}\,k_j/k_j = k_i$. Normalise by $\sum_i k_i = 2L$. If the graph is non-bipartite, the walk is also aperiodic and $M^t p \to \pi$. If it is bipartite, $\pi$ is still stationary, but the iteration oscillates.
:::

## Worked example

Take the lecture's three-page web: $y \to y$, $y \to a$, $a \to y$, $a \to m$, $m \to a$. Ordering the nodes $(y, a, m)$ gives $k^{\mathrm{out}} = (2, 2, 1)$ and

$$
M = \begin{pmatrix} 1/2 & 1/2 & 0 \\ 1/2 & 0 & 1 \\ 0 & 1/2 & 0 \end{pmatrix}.
$$

| Setting | Matrix | $r = (r_y, r_a, r_m)$ |
|---|---|---|
| Flow equations, no teleport | $M$ | $(2, 2, 1)/5$; eigenvalues of $M$: $1, 0.309, -0.809$ |
| PageRank, $\beta = 0.8$ | $G$ | $(35, 37, 21)/93 \approx (0.376, 0.398, 0.226)$ |
| RWR from $y$, $\beta = 0.8$ | $v = e_y$ | $(17, 10, 4)/31 \approx (0.548, 0.323, 0.129)$ |
| **Spider trap**: replace $m \to a$ by $m \to m$, no teleport | — | $(0, 0, 1)$: the trap takes everything |
| Spider trap, $\beta = 0.8$ | $G$ | $(7, 5, 21)/33$; $\lambda_2(G) = 0.647 = 0.8 \times 0.809$ |
| **Dead end**: delete $m \to a$, no teleport | — | total mass $\to 0$ |
| Dead end, patched to uniform, $\beta = 0.8$ | $G$ | $(35, 25, 21)/81$, identical to Newman's leaky solve after normalising |

What the table shows:

- **Teleport breaks the tie.** Under pure flow $y$ and $a$ tie at $2/5$. With teleport, $a$ edges ahead of $y$ ($37/93$ vs $35/93$).
- **The RWR vector is local.** From $y$, more than half of the mass stays at the root.
- **Linearity check.** Averaging the RWR vectors from $y$, $a$ and $m$ reproduces the PageRank vector exactly.
- **Convergence is faster than the bound.** Power iteration on the base graph has error $2.4\times10^{-3}$ after 10 steps and $3.2\times10^{-5}$ after 20. That is a contraction of $\approx 0.647 = \beta\lvert\mu_2\rvert$ per step, well inside the bound $2\beta^t$ ($0.21$ and $0.023$).

**HITS on a citation toy.** Take hubs 1, 2 and authorities 3, 4, with edges $1\to3$, $1\to4$, $2\to3$:
- $AA^\top$ has nonzero block $\begin{pmatrix}2&1\\1&1\end{pmatrix}$ on $\{3,4\}$, with leading eigenvalue $\varphi^2 = (3+\sqrt5)/2 \approx 2.618$. Authorities $(x_3, x_4) \propto (1, 0.618)$.
- $A^\top A$ has the same block on $\{1, 2\}$. Hubs $(y_1, y_2) \propto (1, 0.618)$.

Node 3 is the better authority because both hubs cite it. Node 1 is the better hub because it cites both authorities.

(All values computed from the stated graphs, exactly with rational arithmetic where shown as fractions.)

## Assumptions and limitations

- **Conventions differ across sources, and the differences matter.**
  - $\beta$ is the follow-link probability here and in CS224W. Brin & Page call it $d$, Newman calls it $\alpha$, and Tong et al. call it $c$.
  - Tong et al.'s symbol table calls $c$ the "restart probability", yet their equation restarts with probability $1-c$.
  - Gleich builds $P = A^\top D^{+}$ from $A_{ij}=1$ for $i \to j$.
  - *My note:* Brin & Page's printed formula $PR(A) = (1-d) + d\sum PR(T_i)/C(T_i)$ sums to $N$, not 1, despite the text calling it a probability distribution. The same paragraph also describes $d$ as the probability of getting bored, which is the role of $1-d$.
- **Dead-end handling is a modelling choice.** Strongly preferential, weakly preferential and sink preferential PageRank give different scores. Many papers never say which one they use.
- **Uniform teleportation favours many weak nodes.** Every node gets at least $(1-\beta)/N$, so a rank is only meaningful relative to that floor. Link farms can also exploit the in-link structure. *My note:* this is the classic motivation for trust-biased teleport vectors.
- **Choosing $\beta$ is a trade-off, not a theorem.** As $\beta \to 1$ the scores approach the structure-only stationary distribution, which may not exist or may be non-unique, and convergence slows. Small $\beta$ approaches uniform scores, or $v$ itself for PPR.
- **HITS uniqueness.** *My note:* the leading eigenvalue of $AA^\top$ need not be simple, e.g. with disconnected hub–authority communities. Then the HITS scores depend on the starting vector. Newman's Perron–Frobenius argument guarantees non-negativity, not uniqueness, without irreducibility.

## Connections

- **NETS 5116.** PageRank, Katz and eigenvector centrality are the matrix centralities of Newman ch. 7. The "divide by degree / add a constant" table above is his Table 7.1 ([Newman ch. 7 notes](../../nets-5116/newman/07-measures-and-metrics.md)).
- **PHYS 7335.**
  - The random surfer is a discrete-time random walk on a directed network. {prf:ref}`prop-la-undirected` ($\pi_i \propto k_i$) is the starting point of the course's random-walk lectures.
  - Teleportation plays the same role that restart and absorbing boundaries play in diffusion problems.
- **NETS 7332.**
  - RWR and PPR scores are the hand-designed ancestor of the learned random-walk similarities in [shallow embeddings](./03-shallow-embeddings.md) (DeepWalk, node2vec). Both score pairs by co-occurrence on short random walks.
  - *My note:* [label propagation](./04-label-propagation.md) iterates $Y \leftarrow \beta S Y + (1-\beta) Y^{(0)}$, which has exactly the PPR fixed-point structure, with the labels playing the role of $v$.
  - In GNNs, **APPNP** [](doi:10.48550/arXiv.1810.05997) replaces $L$ rounds of message passing with personalised-PageRank propagation of a node's predictions. The teleport back to the root keeps the representation local at any depth. See [message-passing GNNs](./05-message-passing-gnns.md).

## Self-test

:::{dropdown} Q1. Write $M$ in terms of $A$ under the convention $A_{ij}=1$ for $j\to i$. Why is it column stochastic, and when does it fail to be?
$M = A D_{\mathrm{out}}^{-1}$, so $M_{ij} = A_{ij}/k_j^{\mathrm{out}}$. Column $j$ sums to $k_j^{\mathrm{out}}/k_j^{\mathrm{out}} = 1$. It fails at dead ends ($k_j^{\mathrm{out}} = 0$), whose columns are zero.
:::

:::{dropdown} Q2. Distinguish the failure modes of dead ends and spider traps, and say what teleportation does to each.
- **Dead ends** leak probability: $M$ is sub-stochastic and $M^t p \to 0$. The fix is to teleport with probability 1 from them, which makes the matrix stochastic.
- **Spider traps** are closed classes that absorb all the mass. The scores exist but are useless. The fix is to teleport out with probability $1-\beta$ at every step.

With both fixes, $G > 0$ entrywise, which by Perron gives a unique positive stationary vector.
:::

:::{dropdown} Q3. Derive the closed form of personalized PageRank and interpret it probabilistically.
From $r = \beta M r + (1-\beta) v$ we get $r = (1-\beta)(I-\beta M)^{-1}v = (1-\beta)\sum_t \beta^t M^t v$. This is the distribution of the end point of a walk started from $v$ whose length is geometric with $\Pr(T=t) = (1-\beta)\beta^t$.
:::

:::{dropdown} Q4. What controls the convergence rate of power iteration on $G$? Give the worst-case bound.
The error contracts by $\lvert\lambda_2(G)\rvert = \beta\lvert\mu_2(M)\rvert \le \beta$ per step asymptotically, and $\lVert r - r^{(t)}\rVert_1 \le 2\beta^t$ in the worst case. Equality $\lambda_2 = \beta$ holds when $M$ has at least two closed classes.
:::

:::{dropdown} Q5. Why is PageRank without teleport uninformative on a connected undirected graph?
The stationary distribution of $AD^{-1}$ is $\pi_i = k_i/2L$, so the ranking is exactly the degree ranking.
:::

:::{dropdown} Q6. Place eigenvector, Katz and PageRank centrality on Newman's two axes, and state Katz's constraint on $\alpha$.
- Eigenvector: no division, no constant.
- Katz: no division, constant term, $x = (I-\alpha A)^{-1}\mathbf 1$ with $\alpha < 1/\Lambda_{\max}$.
- PageRank: division by out-degree and a constant term, $x = (I-\beta AD^{-1})^{-1}\mathbf 1$.
:::

:::{dropdown} Q7. In HITS with $A_{ij}=1$ for $j\to i$, which matrix gives authorities? Why do the hub and authority problems share an eigenvalue?
Authorities come from $AA^\top$ and hubs from $A^\top A$. If $AA^\top x = \lambda x$, then $A^\top A(A^\top x) = \lambda (A^\top x)$, so the nonzero eigenvalues coincide, and $y \propto A^\top x$.
:::

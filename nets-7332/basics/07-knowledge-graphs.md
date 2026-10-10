---
title: Heterogeneous Graphs and Knowledge Graph Embeddings
short_title: Knowledge graphs
subject: NETS 7332 · Basics
description: Relational GCNs for typed graphs, how knowledge-graph link prediction is trained and evaluated, and which relation patterns TransE, TransR, DistMult, ComplEx and RotatE can represent.
tags: [heterogeneous-graphs, knowledge-graphs, r-gcn, transe, distmult, complex, rotate, link-prediction]
---

:::{tip} TL;DR
- A **heterogeneous graph** has typed nodes and typed edges. A **knowledge graph** (KG) is a heterogeneous graph whose edges are facts $(h, r, t)$, and it is always **incomplete**. The core task is **KG completion**: ranking candidate heads or tails for queries $(h, r, ?)$ and $(?, r, t)$.
- **R-GCN** extends GCN with one weight matrix $W_r$ per relation and direction, plus a self-loop. That makes parameters grow as $\lvert\mathcal{R}\rvert d^2$ per layer. **Basis decomposition** $W_r = \sum_b a_{rb} V_b$ shares weights across relations. A **block-diagonal** $W_r$ sparsifies them.
- **Shallow KG embeddings** score a triple directly:
  - TransE $-\lVert \mathbf{h}+\mathbf{r}-\mathbf{t} \rVert$
  - TransR $-\lVert M_r\mathbf{h}+\mathbf{r}-M_r\mathbf{t} \rVert$
  - DistMult $\langle \mathbf{h},\mathbf{r},\mathbf{t}\rangle$
  - ComplEx $\mathrm{Re}\langle \mathbf{h},\mathbf{r},\bar{\mathbf{t}}\rangle$
  - RotatE $-\lVert \mathbf{h}\circ\mathbf{r}-\mathbf{t} \rVert$ with $\lvert r_i \rvert=1$
- Each scoring function's algebra fixes which **relation patterns** it can represent: symmetry, antisymmetry, inversion, composition and 1-to-N. DistMult is symmetric in $h \leftrightarrow t$ by construction. TransE can only represent a symmetric relation by setting $\mathbf{r}=0$. RotatE represents all four of the logical patterns, but its relations are bijections.
- Evaluation is a **ranking**. Report **MRR** and **Hits@k** in the **filtered** setting, where other known-true answers are removed from the candidate list before ranking.
:::

- **Source.** Stanford CS224W (Fall 2021), Lecture 10, "Heterogeneous Graphs and Knowledge Graph Embeddings" ([slides](https://snap.stanford.edu/class/cs224w-2021/slides/10-kg.pdf)). The primary papers are cited inline: R-GCN [](doi:10.1007/978-3-319-93417-4_38), TransE ([Bordes et al., NeurIPS 2013](https://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data)), TransR [](doi:10.1609/aaai.v29i1.9491), DistMult [](doi:10.48550/arXiv.1412.6575), ComplEx [](doi:10.48550/arXiv.1606.06357), RotatE [](doi:10.48550/arXiv.1902.10197).
- **Builds on.** Message-passing GNNs ([](./05-message-passing-gnns.md)) and shallow encoders ([](./03-shallow-embeddings.md)).
- **Notation.** Shared symbols as in [](#notation). Page-specific symbols:
  - $\mathcal{R}$ is the set of relation types and $\mathcal{A}$ the set of node types.
  - Italic $h, r, t$ name a head entity, a relation and a tail entity.
  - **Bold** $\mathbf{h}, \mathbf{r}, \mathbf{t}$ are their KG embeddings, kept distinct from the GNN hidden states $h_v^{(\ell)}$.
  - $\mathcal{N}_r(v)$ is the set of neighbours $u$ with an edge $(u, r, v)$.
  - $\langle \mathbf{a}, \mathbf{b}, \mathbf{c} \rangle = \sum_i a_i b_i c_i$ is the trilinear product, and $\circ$ is the elementwise product.

(sec-kg-definitions)=
## Setup and definitions

:::{prf:definition} Heterogeneous graph
:label: def-kg-hetero

A **heterogeneous graph** is $G = (V, E, \tau, \phi)$ with:
- a node-type map $\tau: V \to \mathcal{A}$, and
- an edge-type map $\phi: E \to \mathcal{R}$, where each edge $(u, r, v) \in E \subseteq V \times \mathcal{R} \times V$ carries its relation type.

It is *heterogeneous* when $\lvert\mathcal{A}\rvert > 1$ or $\lvert\mathcal{R}\rvert > 1$. CS224W writes the same object as $G = (V, E, R, T)$, with $T(v)$ the node type.
:::

:::{prf:definition} Knowledge graph and KG completion
:label: def-kg-kg

A **knowledge graph** is a heterogeneous graph whose nodes are **entities** and whose edges are **facts** (triples) $(h, r, t)$: head $h$ stands in relation $r$ to tail $t$. Observed KGs are incomplete. **KG completion** asks, for a query $(h, r, ?)$, to rank all candidate tails so that the true ones come first. The query $(?, r, t)$ is handled the same way.
:::

:::{prf:definition} Relation patterns
:label: def-kg-patterns

These follow the RotatE paper's Definitions 1–3 and CS224W's 1-to-N case, with all statements holding for all $x, y, z$:
- **symmetric**: $r(x,y) \Rightarrow r(y,x)$
- **antisymmetric**: $r(x,y) \Rightarrow \lnot r(y,x)$
- $r_1$ is the **inverse** of $r_2$: $r_2(x,y) \Rightarrow r_1(y,x)$
- $r_1$ is **composed** of $r_2$ and $r_3$: $r_2(x,y) \wedge r_3(y,z) \Rightarrow r_1(x,z)$
- **1-to-N**: $r(h,t_1), \dots, r(h,t_n)$ all hold with distinct $t_i$

Examples from the lecture: *Roommate* is symmetric, *Hypernym* is antisymmetric, *Advisor*/*Advisee* are inverses, and "my mother's husband is my father" is a composition. TransE's paper classifies relations as 1-to-1, 1-to-Many, Many-to-1 or Many-to-Many. A side is "Many" if its average number of entities per fixed partner is at least 1.5.
:::

(sec-kg-core)=
## Core ideas

### Relational GCN

R-GCN [](doi:10.1007/978-3-319-93417-4_38) is a GCN in which the message depends on the **type and direction** of the edge:

$$
h_v^{(\ell+1)} = \sigma\!\Big( \sum_{r \in \mathcal{R}} \sum_{u \in \mathcal{N}_r(v)} \frac{1}{c_{v,r}}\, W_r^{(\ell)} h_u^{(\ell)} \;+\; W_0^{(\ell)} h_v^{(\ell)} \Big).
$$ (eq-kg-rgcn)

- **Message.** Each neighbour under relation $r$ sends $m_{u,r} = W_r h_u / c_{v,r}$. The self-loop is "a single self-connection of a special relation type" and sends $W_0 h_v$.
- **Aggregation.** Sum the messages, then apply $\sigma$. This is the message/aggregate split of [](./05-message-passing-gnns.md) with relation-indexed message functions.
- **Normalisation.** $c_{v,r}$ is "problem-specific", e.g. $c_{v,r} = \lvert\mathcal{N}_r(v)\rvert$, as used for entity classification. For link prediction the authors found that normalising **across** relation types, $c_{v,r} = \sum_r \lvert\mathcal{N}_r(v)\rvert$, worked best.
- **Inputs.** If there are no node features, the input is a one-hot vector per node. The first layer is then a learned embedding lookup.
- **Directions.** $\mathcal{R}$ includes inverse directions, so a directed KG with $\lvert\mathcal{R}_0\rvert$ relation types gives $2\lvert\mathcal{R}_0\rvert$ relation-specific matrices plus $W_0$.

**Parameter blow-up and the two regularisers.** One $d^{(\ell+1)} \times d^{(\ell)}$ matrix per relation and layer means the parameter count grows linearly in $\lvert\mathcal{R}\rvert$. The paper warns this "can easily lead to overfitting on rare relations".

| Regulariser | Form | Parameters per layer | Inductive bias |
|---|---|---|---|
| **Basis decomposition** | $W_r^{(\ell)} = \sum_{b=1}^{B} a_{rb}^{(\ell)} V_b^{(\ell)}$ | $B\,d^{(\ell+1)}d^{(\ell)} + B\lvert\mathcal{R}\rvert$ | weight *sharing*: rare relations borrow statistical strength from frequent ones through the shared bases $V_b$ |
| **Block-diagonal** | $W_r^{(\ell)} = \bigoplus_{b=1}^{B} Q_{br}^{(\ell)}$, $Q_{br} \in \mathbb{R}^{(d^{(\ell+1)}/B)\times(d^{(\ell)}/B)}$ | $\lvert\mathcal{R}\rvert\, d^{(\ell+1)} d^{(\ell)} / B$ | *sparsity*: latent features interact only within groups. CS224W: "only nearby neurons/dimensions can interact" |

For entity classification, R-GCN is trained with cross-entropy on labelled nodes. For link prediction it is the **encoder** of an autoencoder whose decoder is a KG scoring function. The paper uses DistMult, $f(s,r,o) = \mathbf{e}_s^\top R_r \mathbf{e}_o$ with $R_r$ diagonal, and reports a 29.8% improvement over a decoder-only DistMult baseline on FB15k-237.

### Training and evaluating link prediction

**Edge splits.** CS224W's protocol for GNN-based KG link prediction splits the edges four ways:
- **Training message edges** are what the GNN propagates over.
- **Training supervision edges** are what it is scored on.
- **Validation** and **test** edges are held out.

At validation time, all training edges, message and supervision alike, are used for message passing. Keeping the message and supervision sets separate stops the model from scoring an edge it has already passed messages along.

**Negatives.** These are made by **corrupting** a positive triple. Replace the tail, $(h, r, t')$, or the head, $(h', r, t)$, but not both. A corrupted triple must not be a known edge: in CS224W's example, $(E, r_3, C)$ "is NOT a negative edge" because it already exists in the training graph.

**Losses.** These differ only in how they separate positive and negative scores:
- **Margin ranking (TransE).** With $d$ the distance, i.e. minus the score:

$$
\mathcal{L} = \sum_{(h,r,t)\in S}\; \sum_{(h',r,t') \in S'_{(h,r,t)}} \big[\gamma + d(\mathbf{h}+\mathbf{r},\mathbf{t}) - d(\mathbf{h}'+\mathbf{r},\mathbf{t}')\big]_+ .
$$ (eq-kg-margin)

  Entity embeddings are constrained to unit $L_2$ norm. This "prevents the training process to trivially minimize $\mathcal{L}$ by artificially increasing entity embeddings norms".
- **Binary cross-entropy (R-GCN, CS224W).** $-\log\sigma(f(\text{pos})) - \log(1-\sigma(f(\text{neg})))$, with $\omega$ negatives per positive in R-GCN.
- **Self-adversarial negative sampling (RotatE).** Weight each negative by $\mathrm{softmax}(\alpha f_r(h'_j, t'_j))$ under the current model. Uniform sampling wastes effort on negatives that are "obviously false as training goes on".

**Metrics.** For each test triple, score the true answer against all corruptions and take the **rank** $\mathrm{RK}$ of the true answer.

$$
\mathrm{Hits@}k = \frac{1}{\lvert Q\rvert}\sum_{q \in Q} \mathbb{1}[\mathrm{RK}_q \le k],
\qquad
\mathrm{MRR} = \frac{1}{\lvert Q\rvert}\sum_{q \in Q} \frac{1}{\mathrm{RK}_q}.
$$ (eq-kg-metrics)

**Raw vs filtered.** In the *raw* setting a corrupted triple that is actually true, e.g. present in the training set, can outrank the test triple. TransE's paper introduced the **filtered** setting to fix this. It removes from the candidate list every corruption that appears in the training, validation or test set, except the test triple itself. Filtered metrics are the standard; R-GCN calls filtered MRR "typically considered more reliable".

:::{warning} Benchmark leakage
FB15k and WN18 contain inverse pairs $(e_1, r, e_2)$ in training and $(e_2, r^{-1}, e_1)$ in test, so much of the task reduces to memorisation. A simple linear-feature baseline (LinkFeat) beat the embedding methods of the time. FB15k-237 removes these pairs, and R-GCN uses it as its primary benchmark. *My comment:* any model that can represent inversion (TransE, ComplEx, RotatE) gets inflated scores on the original datasets.
:::

### Shallow KG embedding models

These are **shallow encoders** in the sense of [](./03-shallow-embeddings.md): one free vector per entity and per relation, learned directly. Each is defined by its scoring function $f_r(h,t)$, where higher means more plausible.

| Model | Score $f_r(h,t)$ | Embedding space | Idea |
|---|---|---|---|
| TransE | $-\lVert \mathbf{h}+\mathbf{r}-\mathbf{t} \rVert$ ($L_1$ or $L_2$) | $\mathbf{h},\mathbf{r},\mathbf{t} \in \mathbb{R}^d$ | relation = translation |
| TransR | $-\lVert M_r\mathbf{h} + \mathbf{r} - M_r\mathbf{t} \rVert$ (paper: squared $L_2$) | $\mathbf{h},\mathbf{t}\in\mathbb{R}^d$, $\mathbf{r}\in\mathbb{R}^k$, $M_r\in\mathbb{R}^{k\times d}$ | project into a relation-specific space, then translate |
| DistMult | $\langle \mathbf{h},\mathbf{r},\mathbf{t}\rangle = \mathbf{h}^\top \mathrm{diag}(\mathbf{r})\, \mathbf{t}$ | $\mathbb{R}^d$ | bilinear with a diagonal relation matrix |
| ComplEx | $\mathrm{Re}\langle \mathbf{h},\mathbf{r},\bar{\mathbf{t}}\rangle$ | $\mathbb{C}^d$ | DistMult in complex space; the conjugate breaks $h\leftrightarrow t$ symmetry |
| RotatE | $-\lVert \mathbf{h}\circ\mathbf{r} - \mathbf{t}\rVert$ with $\lvert r_i\rvert = 1$ | $\mathbb{C}^d$ | relation = elementwise rotation, $r_i = e^{i\theta_{r,i}}$ |

DistMult's diagonal restriction gives "the same number of relation parameters as TransE". ComplEx decomposes the score as $\mathrm{Re}(\mathbf{r})$ weighting a symmetric part plus $\mathrm{Im}(\mathbf{r})$ weighting an antisymmetric part. RotatE in polar form is

$$
\lVert \mathbf{h}\circ\mathbf{r}-\mathbf{t}\rVert = \sqrt{\textstyle\sum_i (m_{h,i}-m_{t,i})^2 + 4 m_{h,i} m_{t,i} \sin^2\!\frac{\theta_{h,i}+\theta_{r,i}-\theta_{t,i}}{2}},
$$ (eq-kg-rotate-polar)

so it reduces to a TransE-like translation on phases when moduli are fixed. RotatE's Theorem 4 says it "can degenerate into TransE".

(sec-kg-results)=
## Key results

### Which patterns each model can represent

The two sources agree on every cell they share except TransR's inversion and composition entries.

| Model | Sym. | Antisym. | Inverse | Compos. | 1-to-N |
|---|---|---|---|---|---|
| TransE | ✗ | ✓ | ✓ | ✓ | ✗ |
| TransR | ✓ | ✓ | ✓ (CS224W) / ✗ (RotatE, as "TransX") | ✓ (CS224W) / ✗ (RotatE) | ✓ |
| DistMult | ✓ | ✗ | ✗ | ✗ | ✓ |
| ComplEx | ✓ | ✓ | ✓ | ✗ | ✓ |
| RotatE | ✓ | ✓ | ✓ | ✓ | ✗ *(my derivation, not in either table)* |

Sources: CS224W Lecture 10's summary table covers TransE, TransR, DistMult and ComplEx in all five columns. RotatE's Table 2 covers TransE, "TransX", DistMult, ComplEx and RotatE, in the four logical columns only.

**Why the TransR entries disagree.** CS224W shows TransR can *represent* inversion by taking $\mathbf{r}_1=-\mathbf{r}_2$ and $M_{r_1}=M_{r_2}$. For composition it constructs an $M_{r_3}$ with $\mathrm{Ker}\,M_{r_3} = \mathrm{Ker}\,M_{r_1} + \mathrm{Ker}\,M_{r_2}$. RotatE's Appendix A argues that TransX models "cannot infer inversion and composition as $g_{r,1}$ and $g_{r,2}$ are invertible matrix multiplications". *My reading:* the two sources use different notions. CS224W asks whether some parameter setting satisfies the rules exactly. RotatE asks whether the pattern is implied by the model class under its own assumptions. Quote the table you are using, with its source.

:::{prf:proposition} DistMult is symmetric
:label: prop-kg-distmult-sym

For every relation $r$ and all entities, $f_r(h,t) = f_r(t,h)$. DistMult therefore represents symmetric relations, but it cannot represent antisymmetry, and it can represent an inverse pair only by setting $\mathbf{r}_1 = \mathbf{r}_2$.
:::

:::{dropdown} Proof
$f_r(h,t) = \sum_i h_i r_i t_i = \sum_i t_i r_i h_i = f_r(t,h)$, because real multiplication commutes.

- **Antisymmetry** would require a high $f_r(h,t)$ alongside a low $f_r(t,h)$, which is impossible since the two are equal.
- **Inverse pair.** If $r_1$ is the inverse of $r_2$, we need $f_{r_2}(h,t) = f_{r_1}(t,h) = f_{r_1}(h,t)$ for all pairs. That forces $\mathbf{r}_1=\mathbf{r}_2$, so *Advisor* and *Advisee* would get the same embedding.
- **Composition.** CS224W's intuition: each (head, relation) pair defines a hyperplane, and a union of multi-hop hyperplanes cannot be expressed as one hyperplane.
:::

:::{prf:proposition} TransE cannot represent a symmetric relation non-trivially
:label: prop-kg-transe-sym

If $r(h,t)$ and $r(t,h)$ both hold exactly, then $\mathbf{h}+\mathbf{r}=\mathbf{t}$ and $\mathbf{t}+\mathbf{r}=\mathbf{h}$, which forces $\mathbf{r}=0$ and $\mathbf{h}=\mathbf{t}$. More generally, for $\mathbf{h}\ne\mathbf{t}$ the best achievable total score is
$$
f_r(h,t)+f_r(t,h) \le -2\lVert \mathbf{h}-\mathbf{t}\rVert < 0 .
$$
:::

:::{dropdown} Proof
Adding the two equations gives $2\mathbf{r}=0$, and then $\mathbf{h}=\mathbf{t}$.

For the bound, apply the triangle inequality: $\lVert \mathbf{h}+\mathbf{r}-\mathbf{t}\rVert + \lVert \mathbf{t}+\mathbf{r}-\mathbf{h}\rVert \ge \lVert (\mathbf{h}+\mathbf{r}-\mathbf{t})-(\mathbf{t}+\mathbf{r}-\mathbf{h})\rVert = 2\lVert \mathbf{h}-\mathbf{t}\rVert$. This bound is my addition, not from the sources.

The other TransE entries:
- **Inversion:** set $\mathbf{r}_1=-\mathbf{r}_2$.
- **Composition:** $\mathbf{r}_3=\mathbf{r}_1+\mathbf{r}_2$.
- **Antisymmetry:** any $\mathbf{r}\neq 0$.
- **No exact 1-to-N:** $\mathbf{t}_1=\mathbf{h}+\mathbf{r}=\mathbf{t}_2$ would collapse distinct tails onto one point.

RotatE's paper notes that this pushes "entities with symmetric relations to be close to each other".
:::

:::{prf:proposition} ComplEx: real relations are symmetric, imaginary ones antisymmetric
:label: prop-kg-complex

If $\mathrm{Im}(\mathbf{r})=0$ then $f_r(h,t)=f_r(t,h)$. If $\mathrm{Re}(\mathbf{r})=0$ then $f_r(h,t)=-f_r(t,h)$. Inversion is represented by $\mathbf{r}_1 = \bar{\mathbf{r}}_2$.
:::

:::{dropdown} Proof
- **Symmetric case.** For real $r_i$, $\mathrm{Re}(r_i h_i \bar t_i) = r_i\,\mathrm{Re}(h_i\bar t_i) = r_i\,\mathrm{Re}(\bar h_i t_i)$, which is the summand of $f_r(t,h)$.
- **Antisymmetric case.** For $r_i = i b_i$, $\mathrm{Re}(i b_i z) = -b_i \mathrm{Im}(z)$, and $\mathrm{Im}(h_i \bar t_i) = -\mathrm{Im}(t_i \bar h_i)$.
- **Inversion.** $\mathrm{Re}\langle \mathbf{h},\mathbf{r},\bar{\mathbf{t}}\rangle = \mathrm{Re}\,\overline{\langle \mathbf{h},\mathbf{r},\bar{\mathbf{t}}\rangle} = \mathrm{Re}\langle \mathbf{t},\bar{\mathbf{r}},\bar{\mathbf{h}}\rangle$, so $\bar{\mathbf{r}}$ scores the reversed triple identically. This is RotatE Appendix A's "complex conjugate of the solution" argument.
- **No composition.** ComplEx "does not model a bijection mapping from $h$ to $t$" (RotatE, App. A).
:::

:::{prf:proposition} RotatE represents symmetry, antisymmetry, inversion and composition
:label: prop-kg-rotate

With $\mathbf{t} = \mathbf{h}\circ\mathbf{r}$ and $\lvert r_i \rvert = 1$:
- $r$ is symmetric iff $r_i = \pm 1$ for all $i$, i.e. $\mathbf{r}\circ\mathbf{r}=\mathbf{1}$
- $r_1$ is the inverse of $r_2$ iff $\mathbf{r}_1 = \bar{\mathbf{r}}_2$
- $r_1$ is composed of $r_2$ and $r_3$ iff $\mathbf{r}_1 = \mathbf{r}_2\circ\mathbf{r}_3$, i.e. phases add: $\theta_1 = \theta_2+\theta_3$
:::

:::{dropdown} Proof sketch (RotatE Appendix B–D)
- **Symmetry:** $\mathbf{y}=\mathbf{r}\circ\mathbf{x}$ and $\mathbf{x}=\mathbf{r}\circ\mathbf{y}$ give $\mathbf{r}\circ\mathbf{r}=\mathbf{1}$. Antisymmetry is the case $\mathbf{r}\circ\mathbf{r}\neq\mathbf{1}$.
- **Inversion:** $\mathbf{y}=\mathbf{r}_1\circ\mathbf{x}$ and $\mathbf{x}=\mathbf{r}_2\circ\mathbf{y}$ give $\mathbf{r}_1=\mathbf{r}_2^{-1}=\bar{\mathbf{r}}_2$, using unit modulus.
- **Composition:** $\mathbf{z}=\mathbf{r}_1\circ\mathbf{x}$, $\mathbf{y}=\mathbf{r}_2\circ\mathbf{x}$ and $\mathbf{z}=\mathbf{r}_3\circ\mathbf{y}$ give $\mathbf{r}_1=\mathbf{r}_2\circ\mathbf{r}_3$.

Unlike TransE, the symmetric case does not force $\mathbf{h}=\mathbf{t}$: a rotation by $\pi$ maps $\mathbf{h}$ to $-\mathbf{h}$. *My derivation, not in either table:* for a fixed $\mathbf{h}$ and $\mathbf{r}$ the exact tail is unique, so RotatE, like TransE, cannot represent 1-to-N relations exactly.
:::

## Worked example

All numbers below were computed in Python with 1- or 2-dimensional embeddings.

**DistMult symmetry.** Take $\mathbf{h}=(0.9,-0.4)$, $\mathbf{t}=(0.2,1.1)$ and $\mathbf{r}=(1.5,0.7)$. Then $f_r(h,t)=f_r(t,h)=-0.038$, and no choice of $\mathbf{r}$ can separate the two directions.

**TransE and a symmetric relation.** Take $\mathbf{a}=(1,0)$ and $\mathbf{b}=(0,1)$.
- With $\mathbf{r}=\mathbf{b}-\mathbf{a}$, $f(a,b)=0$ is perfect but $f(b,a)=-2.828$.
- With $\mathbf{r}=0$, both scores are $-1.414$.
- A grid search over $\mathbf{r}\in[-2,2]^2$ confirms the best total is $-2.828=-2\lVert\mathbf{a}-\mathbf{b}\rVert$, the bound in [](#prop-kg-transe-sym).

**ComplEx.** Take $\mathbf{h}=(0.5+0.5i,\,-0.3+0.8i)$ and $\mathbf{t}=(0.9-0.2i,\,0.4+0.1i)$.
- A real $\mathbf{r}=(1,2)$ gives $f(h,t)=f(t,h)=0.270$.
- A purely imaginary $\mathbf{r}=(i,2i)$ gives $f(h,t)=-1.250$ and $f(t,h)=+1.250$.

**RotatE in $\mathbb{C}^1$.**
- **Inverse.** Let $r_1=e^{i\pi/2}$ and $x=1$, so $y=x r_1=i$. Then $r_2=\bar r_1=e^{-i\pi/2}$ scores $(y,r_2,x)$ at exactly $0$.
- **Composition.** Composing $r_1$ with $r_3=e^{i\pi/3}$ gives a single relation at angle $150^\circ$, which scores $(x, r_1 r_3, z)$ at exactly $0$.
- **Symmetry.** $r=-1$ is symmetric with $\lvert u-v\rvert=2$, so the two entities stay far apart.

**R-GCN parameter count.** Use FB15k-237 with the paper's settings: 237 relations and $d=500$. Assume $\mathcal{R}$ counts both directions plus the self-loop, giving $2\cdot 237+1=475$ matrices per layer. (This is my count. The paper says only that weights depend on "type and direction".)

| Parameterisation | Parameters per layer |
|---|---|
| Full $W_r$ | $475 \cdot 500^2 = 118{,}750{,}000$ |
| Block-diagonal, $5\times5$ blocks (100 blocks; the paper's FB15k-237 choice) | $475 \cdot 100 \cdot 25 = 1{,}187{,}500$ |
| Basis, $B=2$ (the paper's FB15k/WN18 choice) | $2\cdot 500^2 + 2\cdot 475 = 500{,}950$ |

**Raw vs filtered ranking.** The query is $(E, r_3, ?)$ with true answer $D$. The candidate scores are $A{:}\,2.1$, $D{:}\,1.4$, $F{:}\,0.9$, $B{:}\,0.3$ and $C{:}\,-0.5$, and $(E,r_3,A)$ is a known training fact. $D$'s raw rank is 2, and its filtered rank is 1 because $A$ is removed.

Over three test queries with raw ranks $(2,1,5)$ and filtered ranks $(1,1,4)$:

| | MRR | Hits@1 | Hits@3 |
|---|---|---|---|
| Raw | 0.567 | 0.333 | 0.667 |
| Filtered | 0.750 | 0.667 | 0.667 |

## Assumptions and limitations

- **"Can model" means an exact solution exists.** The pattern tables say whether some parameter setting satisfies a logical rule exactly. They say nothing about whether training finds that setting or how well it generalises. The disagreement over TransR shows the claims depend on how the question is framed.
- **Exact 1-to-N vs approximate.** TransE and RotatE fail 1-to-N only in the exact sense. With margins and many dimensions, near-ties are still possible.
- **Closed world for negatives.** Negatives are sampled from triples absent from the KG, but the KG is incomplete, so some "negatives" are true facts. The filtered setting corrects for this only for facts present in some split.
- **Transductive.** Shallow KG embeddings have no vector for an unseen entity. R-GCN with one-hot inputs is still transductive. Basis decomposition helps rare relations, not unseen entities.
- **Benchmark artefacts.** Inverse leakage in FB15k/WN18 inflates scores, so prefer FB15k-237 (RotatE also reports WN18RR, its WordNet counterpart).
- **Binary facts only.** Triples cannot hold n-ary facts directly; the subset and polyadic issues of the representations reading apply.
- **Reasoning beyond one hop.** Answering path and conjunctive queries needs more. Query2box [](doi:10.48550/arXiv.2002.05969) embeds queries as boxes. This is mentioned only as a pointer; it is not covered here.

## Connections

- **NETS 5116.**
  - Multilayer and multiplex networks in Newman's ch. 6 notes ([](../../nets-5116/newman/06-mathematics-of-networks.md)) are heterogeneous graphs with $\lvert\mathcal{A}\rvert=1$ and one layer per relation type.
  - The FB15k mapping-property classes (1-to-1, …, Many-to-Many) are degree statistics per relation: the mean out-degree and in-degree within a layer.
- **NETS 6116.** *My comment:* a KG scoring function passed through a sigmoid, $\Pr[(h,r,t)] = \sigma(f_r(h,t))$, is a **latent-space / hidden-variable** edge model, one per relation type. TransE is distance-based, like the geometric latent-space models. DistMult is a diagonal bilinear (inner-product) model. The difference is that these models are fitted for prediction, not studied as ensembles.
- **PHYS 7335.** No direct counterpart in the course. *My comment:* typed edges are the multilayer setting in which contagion on multiplex networks is studied.
- **NETS 7332.**
  - R-GCN is the relation-typed version of the GCN in [](./05-message-passing-gnns.md).
  - TransE, TransR, DistMult, ComplEx and RotatE are shallow encoders with relation-aware decoders ([](./03-shallow-embeddings.md)).
  - In the language of [the representations reading](../readings/01-representations.md), a KG is a typed, directed, multilayer graph whose relations are dyadic.
  - The syllabus topic *ML on Heterogeneous Graphs* (R-GCN, HGT) builds directly on this page.

## Self-test

:::{dropdown} Q1. Write the R-GCN update. Where do the parameters blow up, and how do the two regularisers fix it?
$h_v^{(\ell+1)} = \sigma\big(\sum_r\sum_{u\in\mathcal{N}_r(v)} c_{v,r}^{-1} W_r h_u + W_0 h_v\big)$. There is one $d\times d$ matrix per relation and direction, so a layer costs $O(\lvert\mathcal{R}\rvert d^2)$.
- **Basis:** $W_r=\sum_b a_{rb}V_b$ shares $B$ bases across all relations, so each relation needs only $B$ scalars.
- **Block-diagonal:** $W_r=\bigoplus_b Q_{br}$ cuts the per-relation cost by a factor of $B$, but features interact only within a block.
:::

:::{dropdown} Q2. Why is DistMult unable to model antisymmetric relations?
$\langle\mathbf{h},\mathbf{r},\mathbf{t}\rangle=\langle\mathbf{t},\mathbf{r},\mathbf{h}\rangle$ for every $\mathbf{r}$, so $(h,r,t)$ and $(t,r,h)$ always get the same score.
:::

:::{dropdown} Q3. How does ComplEx break DistMult's symmetry, and which relation embeddings give symmetric or antisymmetric scores?
It conjugates the tail: $\mathrm{Re}\langle\mathbf{h},\mathbf{r},\bar{\mathbf{t}}\rangle$. A real $\mathbf{r}$ gives a symmetric score. A purely imaginary $\mathbf{r}$ gives an antisymmetric one, $f(h,t)=-f(t,h)$. In general $\mathbf{r}$ mixes the two.
:::

:::{dropdown} Q4. In RotatE, what are the conditions for symmetry, inversion and composition? Why can TransE not do symmetry?
- **RotatE:** symmetry is $r_i=\pm1$, inversion is $\mathbf{r}_1=\bar{\mathbf{r}}_2$, and composition is $\mathbf{r}_1=\mathbf{r}_2\circ\mathbf{r}_3$ (phases add).
- **TransE:** satisfying both $\mathbf{h}+\mathbf{r}=\mathbf{t}$ and $\mathbf{t}+\mathbf{r}=\mathbf{h}$ forces $\mathbf{r}=0$ and $\mathbf{h}=\mathbf{t}$.
:::

:::{dropdown} Q5. Which models can represent 1-to-N relations exactly, and why do TransE and RotatE fail?
TransR, DistMult and ComplEx can. TransR projects distinct tails to the same point: $M_r\mathbf{t}_1=M_r\mathbf{t}_2$. DistMult and ComplEx can give equal scores to several tails. TransE and RotatE fail because each relation maps $\mathbf{h}$ to a single point ($\mathbf{h}+\mathbf{r}$ or $\mathbf{h}\circ\mathbf{r}$), so distinct exact tails would collide.
:::

:::{dropdown} Q6. Define MRR and Hits@k. What does the filtered setting change, and why?
- **MRR** is the mean of $1/\mathrm{RK}$ over queries.
- **Hits@k** is the fraction of queries with $\mathrm{RK}\le k$.
- **Filtered setting:** before ranking, remove every corruption that is a known true triple in train, validation or test, except the test triple itself. Otherwise a correct model is penalised for ranking other true answers above the held-out one.
:::

:::{dropdown} Q7. In CS224W's link-prediction split, why separate training message edges from training supervision edges? What may not be used as a negative?
- **Separate sets:** the model must not be scored on an edge it propagated messages along, which would let it read off the answer.
- **Negatives:** a corrupted triple may not be an existing edge in the message or supervision sets, e.g. $(E,r_3,C)$ in the lecture example.
:::

---
title: Rumour Models, Information Diffusion and Social Contagion
short_title: Rumours and social contagion
subject: PHYS 7335 · Topic
description: Why rumour models have no spreading threshold, how they behave on heterogeneous networks, and how threshold models of social contagion produce cascade windows instead of epidemic thresholds.
tags: [rumour-spreading, maki-thompson, daley-kendall, social-contagion, threshold-models, cascades]
---

:::{tip} TL;DR
- A **rumour model** is SIR with the spontaneous recovery replaced by an **interaction**. A spreader becomes a **stifler** when it contacts someone who already knows the rumour. Ignorant → spreader happens at rate $\lambda$ per contact, and spreader → stifler at rate $\alpha$ per contact with a spreader or stifler. *Daley–Kendall*: $S+S \to R+R$. *Maki–Thompson*: $S+S \to S+R$.
- Under homogeneous mixing the final fraction of people who heard the rumour (the **reliability**) solves $r_\infty = 1 - e^{-(1+\lambda/\alpha)\,r_\infty}$. The slope at $0$ is $1+\lambda/\alpha > 1$ for **every** $\lambda/\alpha > 0$, so there is **no rumour threshold**. For $\lambda = \alpha$, $r_\infty = 0.797$ and about **20.3 %** never hear the rumour.
- The reason is that stifling is **quadratic** in the densities of informed people. It is negligible while almost everyone is ignorant, so nothing opposes the initial growth. Adding linear **forgetting** at rate $\delta$ restores an SIR-like threshold, $\lambda\langle k\rangle/\delta > 1$, which on networks becomes $\propto \langle k\rangle/\langle k^2\rangle$.
- On **scale-free networks** (Moreno, Nekovee & Pacheco 2004), heterogeneity *lowers* the reliability but still introduces no threshold. The reason is that hubs hear the rumour early and then quickly turn into stiflers. With $\gamma = 3$, $\langle k\rangle = 6$ and $\lambda=\alpha=1$, $r_\infty \approx 0.59$, against $0.80$ under homogeneous mixing. The final reliability does not depend on the seed's degree, but **hub seeds reach it faster**.
- **Threshold (complex) contagion** (Watts 2002): a node adopts once a fraction $\ge \phi$ of its neighbours have adopted. A single seed triggers a **global cascade** only if the **vulnerable** nodes ($k \le \lfloor 1/\phi\rfloor$) percolate. With $\rho_k = P[\phi \le 1/k]$ the condition is $\sum_k k(k-1)\rho_k p_k > \langle k\rangle$. This gives a **cascade window** $1 \lesssim \langle k\rangle \lesssim 1/\phi$, so unlike SIR, *more* links eventually *block* spreading.
:::

- **Source.** Course slides, *Social Contagion – Rumor Model*, PHYS 7335, 9 March 2026 ([PDF](https://mobs-lab.github.io/phys7335/slides/Rumor-model-2026.pdf)). [](doi:10.1103/PhysRevE.69.066130) (Moreno, Nekovee & Pacheco, *Phys. Rev. E* 69, 066130, 2004). [](doi:10.1073/pnas.082090499) (Watts, *PNAS* 99, 5766, 2002). [](doi:10.1103/RevModPhys.87.925) (Pastor-Satorras, Castellano, Van Mieghem & Vespignani, *Rev. Mod. Phys.* 87, 925, 2015, §VIII), the review used for the model definitions and later results. The course textbook is Barrat, Barthélemy & Vespignani [](doi:10.1017/CBO9780511791383), ch. 12; I did not have access to it, so nothing here is attributed to it.
- **Builds on.** [Compartmental models](./03-compartmental-models.md) (SIR and the final-size relation), [heterogeneous mean-field](./05-heterogeneous-mean-field.md) (degree-block equations), [SIR and percolation](./07-sir-percolation.md) (generating functions).
- **Notation.** Shared symbols as in [](#notation) ($k$, $\langle k\rangle$, $\langle k^2\rangle$, $p_k$, $G_0$). Page-specific symbols are $i, s, r$ (densities of ignorants, spreaders, stiflers), $\lambda$ (spreading rate per contact), $\alpha$ (stifling rate per contact), $\delta$ (forgetting rate), $\phi$ (adoption threshold) and $\rho_k$ (probability that a degree-$k$ node is vulnerable).

:::{warning} Letter clash with epidemic models
The slides use $I$ = **Ignorant**, $S$ = **Spreader**, $R$ = **Stifler**. In SIR, $S$ is susceptible and $I$ is infected, so the roles of the letters are **swapped**: ignorant ↔ susceptible, spreader ↔ infected, stifler ↔ removed. The RMP review keeps the SIR letters instead. This page follows the slides, using lower-case $i, s, r$ for densities. Also, $\lambda$ here is a per-contact spreading rate, not the shared $\lambda = \beta/\mu$.
:::

(sec-rumour-setup)=
## Setup and definitions

:::{prf:definition} Rumour model (ISR)
:label: def-rumour-model

Each of $N$ individuals is **ignorant** (has not heard the rumour), a **spreader** (actively passing it on) or a **stifler** (knows it but no longer spreads it). Spreaders contact others:

- spreader + ignorant $\xrightarrow{\lambda}$ 2 spreaders;
- spreader + stifler $\xrightarrow{\alpha}$ 2 stiflers (the spreader loses interest);
- spreader + spreader: **Daley–Kendall** $\xrightarrow{\alpha}$ 2 stiflers; **Maki–Thompson** $\xrightarrow{\alpha}$ spreader + stifler (only the *initiating* spreader stifles).

Nobody leaves the stifler state, and the process ends when no spreaders remain. The **reliability** is $r_\infty$, the final fraction of stiflers, i.e. of everyone who heard the rumour.
:::

The models are due to Daley & Kendall [](doi:10.1038/2041118a0) and Maki & Thompson (1973, in a textbook). Both are given here as summarised in the RMP review and the slides.

:::{prf:definition} Homogeneous-mixing equations
:label: def-rumour-mf

The slides give the discrete-time version:

$$
\begin{aligned}
I(t+1) &= I(t) - \lambda\,\frac{S(t)\,I(t)}{N},\\
S(t+1) &= S(t) + \lambda\,\frac{S(t)\,I(t)}{N} - \alpha\,S(t)\,\frac{S(t)+R(t)}{N},\\
R(t+1) &= R(t) + \alpha\,S(t)\,\frac{S(t)+R(t)}{N}.
\end{aligned}
$$ (eq-rumour-discrete)

Stifling is proportional to $S+R$, the number of people who already know, and each such contact stifles **one** spreader. That is the Maki–Thompson rule. In continuous time, with densities and $\langle k\rangle$ contacts per unit time (Moreno et al., eqs. 2–4):

$$
\dot i = -\lambda\langle k\rangle\, i s,\qquad
\dot s = \lambda\langle k\rangle\, i s - \alpha\langle k\rangle\, s\,(s+r),\qquad
\dot r = \alpha\langle k\rangle\, s\,(s+r),
$$ (eq-rumour-ode)

with $i+s+r=1$, $i(0) \approx 1$, $s(0) = 1/N$, $r(0) = 0$.

The slides also give per-step transition probabilities $P_{I\to S} = 1-(1-\lambda/N)^{S(t)}$ and $P_{S\to R} = 1-(1-\alpha/N)^{S(t)+R(t)}$. *My reading:* these are the chain-binomial "force of infection" and "force of stifling": the probability of at least one successful contact, which linearises to {eq}`eq-rumour-discrete` for small $\lambda/N$ and $\alpha/N$.
:::

:::{prf:definition} Threshold model of social contagion (Watts 2002)
:label: def-watts-model

Each node $u$ is **inactive** or **active** and carries a fixed random threshold $\phi_u \sim f(\phi)$. An inactive node with $k_u$ neighbours becomes active once the fraction of its active neighbours is at least $\phi_u$. Activation is permanent. A node is **vulnerable** if a single active neighbour suffices, i.e. $\phi_u \le 1/k_u$, so a degree-$k$ node is vulnerable with probability $\rho_k = P[\phi \le 1/k]$. A **global cascade** is a cascade, started from a single seed, that reaches a finite fraction of an infinite network.
:::

Threshold models come from the social sciences (Granovetter [](doi:10.1086/226707)). The relative-threshold version above is Watts'. Absolute thresholds, where a node needs $m$ active neighbours, are also common, and on heterogeneous networks the two can behave differently (RMP §VIII.A, footnote 7).

(sec-rumour-core)=
## Core ideas

### Why there is no threshold

In SIR the infected decay at a **linear** rate $\mu\, i$, which competes with the growth $\beta\langle k\rangle s\, i$ from the very start. That competition sets $R_0$ and the threshold. In the rumour model a spreader is removed only by contact with someone informed, at rate $\alpha\langle k\rangle s(s+r)$. This term is **quadratic** in the small densities. At $t=0$, $s+r = 1/N \to 0$, so to first order $\dot s = \lambda\langle k\rangle s$ and the rumour always grows. It only slows down once a finite fraction knows it. Moreno et al. stress this: the growth mechanism is the same as in SIR, and the absence of a threshold comes entirely from the decay rule.

A small-population corollary (my observation, checked numerically below): under Maki–Thompson, a lone spreader *cannot* be stifled before it creates a second informed person, since $S+R-1 = 0$. Early stochastic extinction, which is common in SIR near threshold, is therefore rare.

### Rumours on networks

Write $i_k, s_k, r_k$ for densities within degree class $k$ (the annealed, degree-block picture of [the degree-block formalism](./01-degree-block-formalism.md)). The probability that an edge points to a spreader is $\Theta_s = \sum_{k'} k' p_{k'} s_{k'}/\langle k\rangle$, and the probability that it points to someone informed is $\Theta_{sr} = \sum_{k'} k' p_{k'} (s_{k'}+r_{k'})/\langle k\rangle$. Moreno et al. (eqs. 9–11) write:

$$
\dot i_k = -\lambda k\, i_k\, \Theta_s,\qquad
\dot s_k = \lambda k\, i_k\, \Theta_s - \alpha k\, s_k\, \Theta_{sr},\qquad
\dot r_k = \alpha k\, s_k\, \Theta_{sr}.
$$ (eq-rumour-dbmf)

Their main findings come from simulating the stochastic version on uncorrelated scale-free networks with $\gamma = 3$, $\langle k\rangle = 6$ and $N = 10^4$:

- **Reliability is lower than under homogeneous mixing**, and decreases as $\alpha$ grows: $0.592$ at $\alpha = 1$ and $0.988$ at $\alpha = 0.1$ (with $\lambda = 1$; their Table II, classical rule). The mechanism, as the RMP review puts it, is that hubs are informed quickly and then become stiflers quickly, cutting the rumour off from their many neighbours. Still, **no finite threshold appears**.
- The final density of ignorants in class $k$ **decays exponentially in $k$**, with a cutoff well below $k_{\max}$. Hubs almost always hear the rumour; the ignorants are mostly low-degree nodes.
- **$r_\infty$ does not depend on the seed's degree**, unlike SIR, where the outbreak size depends strongly on where it starts. A **hub seed reaches the plateau faster**, so for a fixed time budget, seeding hubs informs more people, by up to about 30 % at intermediate times.
- Alternative decay rules, stifling only on S–S contacts or only on S–R contacts, raise $r_\infty$ but make the process much slower. Moreno et al. frame this as a **reliability vs efficiency** trade-off: for gossip protocols, "efficiency" means reliability achieved per unit time or per unit of traffic.

The review also notes a structural result: on Watts–Strogatz networks, rumour spreading has a transition at a rewiring probability $p_c$ that stays **finite** as $N\to\infty$. Purely geometric small-world crossovers scale as $1/N$, so this transition comes from the dynamics, not only from the geometry.

### Rumour model vs SIR

| | SIR | Rumour (Maki–Thompson) |
|---|---|---|
| Removal | spontaneous, rate $\mu$ (linear in $i$) | by contact with an informed person, rate $\alpha$ (quadratic) |
| Final size | $r_\infty = 1-e^{-R_0 r_\infty}$ | $r_\infty = 1-e^{-(1+\lambda/\alpha) r_\infty}$ |
| Threshold (homogeneous mixing) | $R_0 = \beta\langle k\rangle/\mu > 1$ | none: the effective "$R_0$" $1+\lambda/\alpha$ always exceeds 1 |
| Threshold on SF networks | $\propto \langle k\rangle/\langle k^2\rangle$, vanishing for $\gamma\le 3$ | none; heterogeneity *reduces* $r_\infty$ |
| Dependence on seed | outbreak size depends on the seed | $r_\infty$ independent of seed; speed depends on it |
| With forgetting (rate $\delta$) | — | SIR-like threshold $\propto \langle k\rangle/\langle k^2\rangle$ (Nekovee et al.) |

### Simple vs complex contagion

In SIR every contact with an infected neighbour succeeds independently with probability $p$, so after $K$ exposures the probability of infection is $P_{\inf}(K) = 1-(1-p)^K$. This is concave, and each extra exposure adds less. Social adoption is often **reinforced**: a rumour is more credible, or an innovation more attractive, when it comes from several sources. **Threshold models** make $P_{\inf}(K)$ a *step* in the fraction of exposed neighbours. The Dodds–Watts "generalised contagion" model interpolates between the two: it accumulates random doses with memory, and reduces to SIR or to deterministic or stochastic threshold rules as special cases (RMP Fig. 14 and eq. 94).

## Key results

:::{prf:proposition} Final reliability of the rumour model
:label: prop-rumour-final

For {eq}`eq-rumour-ode` with $s(0) \to 0$ and $r(0) = 0$, the final fraction of stiflers is the nonzero root of

$$
r_\infty = 1 - e^{-(1+\lambda/\alpha)\,r_\infty}.
$$ (eq-rumour-final)

A nonzero root exists for every $\lambda/\alpha > 0$. The spreader density peaks when $i = \alpha/(\alpha+\lambda)$, at

$$
s_{\max} = 1 + \frac{\alpha}{\lambda}\ln\frac{\alpha}{\alpha+\lambda},
$$ (eq-rumour-peak)

which for $\lambda = \alpha$ is $s_{\max} = 1 - \ln 2 \approx 0.307$.
:::

:::{dropdown} Derivation
Divide $\dot s$ by $\dot i$, using $s + r = 1 - i$:

$$
\frac{ds}{di} = -1 + \frac{\alpha}{\lambda}\,\frac{1-i}{i}.
$$

Integrate from $(i, s) = (1, 0)$:

$$
s(i) = \Big(1+\frac{\alpha}{\lambda}\Big)(1-i) + \frac{\alpha}{\lambda}\ln i .
$$

At the end $s = 0$. Writing $r_\infty = 1 - i_\infty$ gives $(1+\alpha/\lambda)\,r_\infty = -(\alpha/\lambda)\ln(1-r_\infty)$, which rearranges to {eq}`eq-rumour-final`. This matches Moreno et al.'s eq. 5 with $\beta = 1+\lambda/\alpha$, and the RMP review's eq. 98, which it gives for both the Daley–Kendall and Maki–Thompson versions on the complete graph.

**No threshold.** The map $g(r) = 1 - e^{-cr}$ has $g(0)=0$ and $g'(0) = c$. A positive fixed point exists iff $c > 1$, and here $c = 1+\lambda/\alpha > 1$ always.

**Peak.** Setting $ds/di = 0$ gives $i_* = \alpha/(\alpha+\lambda)$. Then $(1+\alpha/\lambda)(1-i_*) = 1$, so $s_{\max} = s(i_*) = 1 + (\alpha/\lambda)\ln i_*$, which is {eq}`eq-rumour-peak`. For $\lambda = \alpha$: $s_{\max} = 1 - \ln 2$. (This step is my derivation.)
:::

:::{prf:proposition} Forgetting restores a threshold
:label: prop-rumour-forgetting

Add spontaneous forgetting $s \to r$ at rate $\delta$ to {eq}`eq-rumour-ode`. Under homogeneous mixing the rumour spreads macroscopically iff $\lambda\langle k\rangle > \delta$. In the degree-block equations {eq}`eq-rumour-dbmf` the condition becomes

$$
\frac{\lambda}{\delta} > \frac{\langle k\rangle}{\langle k^2\rangle},
$$

which vanishes as $N \to \infty$ for scale-free networks with $\gamma \le 3$, exactly as for SIS and SIR.
:::

:::{dropdown} Derivation (mine; the network result agrees with Nekovee et al. as reported in the RMP review)
Linearise around $i_k = 1$, $s_k, r_k \to 0$. The stifling term is second order, so $\dot s_k \approx \lambda k\,\Theta_s - \delta s_k$. Multiply by $k p_k/\langle k\rangle$ and sum over $k$:

$$
\dot\Theta_s \approx \Big(\lambda\frac{\langle k^2\rangle}{\langle k\rangle} - \delta\Big)\Theta_s .
$$

$\Theta_s$ grows iff $\lambda\langle k^2\rangle/\langle k\rangle > \delta$. The homogeneous case is $\langle k^2\rangle = \langle k\rangle^2$. The RMP review gives the intuition: forgetting is linear in the spreader density, so it dominates the quadratic stifling while spreaders are rare. That is what makes the model behave like SIR. The theory paper is Nekovee et al. [](doi:10.1016/j.physa.2006.07.017), which I have not read beyond its metadata.
:::

:::{prf:theorem} Watts' cascade condition
:label: thm-watts-cascade

On a locally tree-like random graph with degree distribution $p_k$ and mean degree $z = \langle k\rangle$, define the generating function of vulnerable degrees $G_0(x) = \sum_k \rho_k p_k x^k$. Global cascades from a single seed are possible when the vulnerable cluster percolates:

$$
G_0''(1) = \sum_k k(k-1)\,\rho_k\, p_k \;>\; z .
$$ (eq-watts-cascade)

For a Poisson graph with a uniform threshold $\phi^*$, so that $\rho_k = 1$ for $k \le K^* = \lfloor 1/\phi^*\rfloor$ and $0$ otherwise, the boundary is

$$
z\, Q(K^*-1, z) = 1,
$$

where $Q(a,x)$ is the regularised upper incomplete gamma function. This boundary has **two** roots in $z$, the edges of the **cascade window**, or none.
:::

:::{dropdown} Derivation sketch
Watts' argument: a small seed can only grow through vulnerable neighbours, so it needs a giant connected cluster of vulnerable nodes. Treat the vulnerable subgraph as a branching process. A random edge reaches a vulnerable node with excess-degree distribution $\propto k(k-1)\rho_k p_k$, so the mean number of vulnerable branches is $\sum_k k(k-1)\rho_k p_k / z$. The mean vulnerable-cluster size $H_0'(1)$ diverges when this ratio reaches 1, giving {eq}`eq-watts-cascade`.

For the Poisson case, $\sum_{k \le K} k(k-1) e^{-z}z^k/k! = z^2\,P(\mathrm{Pois}(z) \le K-2) = z^2\, Q(K-1, z)$. (The reduction is Watts'; this one-line check is mine.)

**Why two roots.** $k(k-1)$ increases with $k$ while $\rho_k$ decreases.
- **Lower edge** $z \approx 1$: the network itself barely percolates, the transition is percolative, and cascade sizes are power-law distributed.
- **Upper edge** $\approx 1/\phi$: hubs become stable, the vulnerable cluster fragments, and the transition is **discontinuous**. Near it, cascades are rare but global.
:::

:::{important} Opposite dependence on connectivity
For SIR on a homogeneous network, global spread needs $\lambda > 1/\langle k\rangle$, and more links help. For threshold contagion, global cascades need roughly $\phi < 1/\langle k\rangle$, and more links **hurt**, because each neighbour carries less weight. Destroying clustering by rewiring *shrinks* threshold cascades. The RMP review calls this "the weakness of long ties", after Centola & Macy, in contrast to Granovetter's "strength of weak ties" for simple contagion.
:::

## Worked example

All numbers below come from integrating {eq}`eq-rumour-ode` with RK4, from Gillespie simulation, and from root-finding. The scripts are not part of the site.

**Reliability vs stifling rate** ($\lambda = 1$):

| $\alpha$ | $r_\infty$ from {eq}`eq-rumour-final` | ODE | never hear the rumour |
|---|---|---|---|
| 1 | 0.7968 | 0.7968 | 0.2032 |
| 0.5 | 0.9405 | 0.9405 | 0.0595 |
| 0.25 | 0.9930 | 0.9930 | 0.0070 |
| 0.2 | 0.9975 | 0.9975 | 0.0025 |

These agree with Moreno et al.'s Table I. Even a very weak spreading rate gives macroscopic spread: $\lambda/\alpha = 0.2$ gives $r_\infty = 0.314$, and $\lambda/\alpha = 0.05$ gives $0.094$.

- **Peak.** For $\lambda = \alpha = 1$ and $s(0) = 10^{-4}$, spreaders peak at $s = 0.3069$ (at $t \approx 9.8$), matching $1-\ln 2$.
- **Stochastic check.** I ran 400 Gillespie simulations of Maki–Thompson on a complete graph with $N = 2000$ and $\lambda=\alpha=1$, each from a single spreader. The mean $r_\infty$ was $0.797$, and **every** run spread macroscopically ($r_\infty > 0.5$). There was no early extinction, consistent with the observation in [Why there is no threshold](#sec-rumour-core).
- **Forgetting** ($\lambda = \alpha = \langle k\rangle = 1$): $\delta = 0.5$ gives $r_\infty = 0.454$ and $\delta = 0.9$ gives $0.098$, while $\delta = 1.1$ and $\delta = 2$ give $0$. The threshold sits at $\delta = \lambda\langle k\rangle = 1$, as {prf:ref}`prop-rumour-forgetting` predicts.
- **Heterogeneity.** On Moreno et al.'s scale-free network ($\gamma = 3$, $\langle k\rangle = 6$), $\alpha = 1$ gives $r_\infty = 0.592$, against $0.797$ under homogeneous mixing.

**Watts' cascade window on Poisson graphs** (roots of $zQ(K^*-1,z)=1$):

| $\phi^*$ | $K^*$ | cascade window in $z = \langle k\rangle$ |
|---|---|---|
| 0.10 | 10 | 1.00 – 13.66 |
| 0.14 | 7 | 1.00 – 9.10 |
| 0.18 | 5 | 1.02 – 5.77 |
| 0.25 | 4 | 1.11 – 3.86 |
| 0.30 | 3 | none |

The upper edge tracks $1/\phi^*$ only roughly; for $\phi^* = 0.18$ it is 5.77, against $1/\phi^* = 5.56$. The window depends on $\phi^*$ only through $K^*$, so $\phi^* = 0.18$ and $0.20$ give the same window.

For $\phi^* \ge 1/3$, $z(1+z)e^{-z} \le 0.84 < 1$ for all $z$, so no cascades are possible. The maximum is at $z = (1+\sqrt5)/2$.

Inside the window, at $\phi^* = 0.18$ and $z = 4$: $\sum_k k(k-1)\rho_k p_k = 6.94 > 4$, and 78.5 % of nodes are vulnerable. At $z = 8$ the sum is $2.71 < 8$, so there are no global cascades even though the network is denser.

## Assumptions and limitations

- **Mean-field and homogeneous mixing.** {eq}`eq-rumour-final` ignores fluctuations and structure. Moreno et al.'s Monte Carlo on a Watts–Strogatz network with $\langle k\rangle = 6$ gives 0.813 against 0.797 at $\alpha=1$. Degree-block equations ignore degree correlations and clustering, which matter for threshold models in particular.
- **The decay rule is a modelling choice.** Directed vs symmetric S–S stifling, and stifling on S–S only or S–R only, change $r_\infty$ and the speed. Moreno et al. argue that the classical rule is the best compromise for applications.
- **Watts' condition is a conjecture plus a percolation calculation.** It concerns *single-node* seeds in the limit $N\to\infty$ on tree-like graphs. A finite fraction of initiators can move the window and make even the lower transition discontinuous (Gleeson & Cahalane, as reported in RMP §VIII.A; I have not read the paper). Finite simulations put the boundaries only approximately where theory does (Watts' Fig. 1).
- **Relative vs absolute thresholds.** Results for one do not carry over to the other on heterogeneous networks.
- **Empirical identification is hard.** Distinguishing complex contagion from simple contagion with homophily, from observational data, runs into the homophily–influence confound. *My comment:* rumour-model parameters are rarely estimated directly. Empirical studies of viral marketing and chain letters, reviewed in RMP, find dynamics quite unlike epidemics, such as rapidly saturating adoption probabilities and deep but narrow trees.

## Connections

- **PHYS 7335.**
  - The final-size relation has exactly the form of SIR's $r_\infty = 1 - e^{-R_0 r_\infty}$ ([compartmental models](./03-compartmental-models.md)), with $R_0$ replaced by $1+\lambda/\alpha$, which always exceeds 1.
  - The degree-block equations are the [heterogeneous mean-field](./05-heterogeneous-mean-field.md) machinery with an interaction-driven recovery.
  - Watts' cascade condition is a site-percolation calculation on the vulnerable nodes, built from the same generating functions $G_0$, $G_1$ as [SIR and percolation](./07-sir-percolation.md).
- **NETS 5116.**
  - Barabási ch. 10 covers SIS and SIR on networks ([chapter notes](../nets-5116/barabasi/10-spreading-phenomena.md)). The contrast here is that rumours have no vanishing threshold, because they have no threshold at all.
  - Watts' window is a percolation transition like the giant-component condition of the Molloy–Reed criterion ([robustness notes](../nets-5116/barabasi/08-network-robustness.md)).
- **NETS 7332.**
  - [Label propagation](../nets-7332/basics/04-label-propagation.md) discusses why homophily and influence (contagion) cannot generally be separated from observational data. This is the identification problem for social-contagion models.
  - Choosing seed sets to maximise a threshold or independent cascade is NP-hard (Kempe et al., cited in RMP). It is the influence-maximisation problem behind seeding hubs.
  - Homophily on hypergraphs ([higher-order homophily](../nets-7332/readings/03-higher-order-homophily.md)) is relevant because complex contagion is often modelled on group interactions.

## Self-test

:::{dropdown} Q1. In the rumour model, why does $r_\infty > 0$ for every $\lambda/\alpha > 0$, while SIR needs $R_0 > 1$?
Stifling happens only on contact with an informed person, at a rate $\propto s(s+r)$, which is quadratic in vanishing densities. Initially nothing opposes the growth $\lambda\langle k\rangle s$. Formally, the final-size map $1-e^{-cr}$ has slope $c = 1+\lambda/\alpha > 1$ at $r = 0$, so a positive fixed point always exists. In SIR, recovery $\mu i$ is linear and competes from the start.
:::

:::{dropdown} Q2. Write the Daley–Kendall and Maki–Thompson spreader–spreader rules. Which one do the course equations implement?
Daley–Kendall: $S+S \to R+R$. Maki–Thompson: $S+S \to S+R$. The slides' equations stifle one spreader per contact with $S+R$, so they implement Maki–Thompson, as do Moreno et al. with "directed" contacts.
:::

:::{dropdown} Q3. Derive the fraction that never hears the rumour when $\lambda = \alpha$.
$ds/di = -1 + (1-i)/i$ gives $s = 2(1-i) + \ln i$. Setting $s = 0$ gives $2r_\infty = -\ln(1-r_\infty)$, i.e. $r_\infty = 1 - e^{-2r_\infty}$, so $r_\infty \approx 0.797$ and $i_\infty \approx 0.203$.
:::

:::{dropdown} Q4. How does a scale-free topology change rumour spreading, and why?
It lowers reliability without creating a threshold. Hubs hear the rumour early, then quickly meet informed neighbours and become stiflers, so they stop relaying it to their many low-degree contacts. The final reliability is independent of where it starts, but hub seeds reach it faster.
:::

:::{dropdown} Q5. What restores an epidemic threshold in rumour dynamics, and what is it on a network?
Spontaneous forgetting $s \to r$ at a linear rate $\delta$. Linearising the degree-block equations gives growth iff $\lambda\langle k^2\rangle/\langle k\rangle > \delta$, so $\lambda_c/\delta = \langle k\rangle/\langle k^2\rangle$. This vanishes for scale-free networks with $\gamma \le 3$.
:::

:::{dropdown} Q6. State Watts' cascade condition and explain why there is an upper edge of the window in $\langle k\rangle$.
Cascades need $\sum_k k(k-1)\rho_k p_k > \langle k\rangle$, i.e. the vulnerable nodes must percolate. As $\langle k\rangle$ grows, nodes have more neighbours, so a single active neighbour is a smaller fraction and fewer nodes are vulnerable ($k \le 1/\phi$). The vulnerable cluster fragments at $\langle k\rangle \approx 1/\phi$, and that upper transition is discontinuous.
:::

:::{dropdown} Q7. Why does adding random long-range links help SIR but hurt threshold cascades?
In SIR each link is an independent transmission chance, so more links raise the effective reproduction number. In a threshold model adoption needs a *fraction* of neighbours, so extra links dilute the influence of each active neighbour. Long ties to unexposed regions also cannot deliver the multiple reinforcing exposures that clustering provides.
:::

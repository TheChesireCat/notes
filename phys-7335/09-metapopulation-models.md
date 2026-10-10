---
title: Reaction–Diffusion Processes and Metapopulation Models
short_title: Metapopulations
subject: PHYS 7335 · Topic
description: Epidemics on networks of subpopulations, where individuals react inside nodes and travel along edges, and why SIR spreading then needs a second, mobility-dependent invasion threshold.
tags: [metapopulation, reaction-diffusion, invasion-threshold, mobility, gleam, sir, sis]
---

:::{tip} TL;DR
- A **metapopulation network** treats each node as a *subpopulation*. A node can hold any number of individuals, which makes it "bosonic": nodes have no occupancy limit. Individuals **react** inside nodes, following SIS or SIR with homogeneous mixing, and **diffuse** along edges. The model therefore has two scales: transmission within a node, set by $R_0$, and coupling between nodes, set by mobility.
- **Diffusion alone.** Suppose each individual leaves its node at rate $p$ and picks one of the node's $k$ edges uniformly. On an uncorrelated network the stationary occupancy is then $N_k = (k/\langle k\rangle)\,\bar N$, so hubs are crowded. This is the random-walk stationary law $\propto k$ applied to people.
- **SIS, two kernels.** With **mass action** (force of infection $\beta I/N$, so contacts per person are fixed), the threshold is $\beta/\mu > 1$ and topology does not affect it. With **pseudo-mass action** ($\beta I$, so contacts grow with node population), there is a *density* threshold $\bar N_c = (\langle k\rangle^2/\langle k^2\rangle)\,\mu/\beta$. That threshold tends to 0 on heavy-tailed networks.
- **SIR has a second threshold.** Even when $R_0 > 1$, an outbreak in one node must export infected travellers *before it burns out*. A branching process over subpopulations gives the **global invasion threshold**, valid for $R_0 - 1 \ll 1$:
  $R_* = (R_0 - 1)\,\dfrac{\langle k^2\rangle - \langle k\rangle}{\langle k\rangle^2}\,\dfrac{p \bar N \alpha}{\mu} > 1$.
  This sets a critical mobility $p_c \bar N = \dfrac{\langle k\rangle^2}{\langle k^2\rangle - \langle k\rangle}\dfrac{\mu R_0^2}{2(R_0-1)^2}$. It arises because seeding is stochastic and discrete, so continuous deterministic models miss it.
- **Heterogeneity in mobility lowers $p_c$.** It enters through the same $\langle k^2\rangle$ factor as in heterogeneous mean-field theory. This is the theoretical reason travel restrictions barely work unless they are extreme. Data-driven models such as **GLEaM** build on this: census cells around >3,000 airports, air travel, and gravity-law commuting folded in by time-scale separation.
:::

- **Source.**
  - [](doi:10.1038/nphys560) (Colizza, Pastor-Satorras & Vespignani, *Nature Physics* 3, 276, 2007). I read the arXiv v1, cond-mat/0703129.
  - [](doi:10.1103/PhysRevLett.99.148701) (Colizza & Vespignani, *PRL* 99, 148701, 2007; arXiv:0802.3636).
  - [](doi:10.1016/j.jtbi.2007.11.028) (Colizza & Vespignani, *J. Theor. Biol.* 251, 450, 2008; arXiv:0706.3647).
  - [](doi:10.1038/nphys1944) (Balcan & Vespignani, *Nature Physics* 7, 581, 2011; arXiv:1103.4874).
  - [](doi:10.1073/pnas.0906910106) (Balcan et al., *PNAS* 106, 21484, 2009; arXiv:0907.3304).
  - The review [](doi:10.1103/RevModPhys.87.925) (Pastor-Satorras, Castellano, Van Mieghem & Vespignani, *Rev. Mod. Phys.* 87, 925, 2015), §IX.
  - The course simulator is [GLEaMviz](https://www.gleamviz.org).
- **Builds on.**
  - [Compartmental models and $R_0$](./03-compartmental-models.md): final size and extinction probability.
  - [Random walks on networks](./02-random-walks.md): stationary occupancy $\propto k$.
  - [Heterogeneous mean-field epidemics](./05-heterogeneous-mean-field.md): degree-block equations and the $\langle k^2\rangle$ factor.
- **Notation.** Shared symbols as in [](#notation), with these page-specific choices:
  - The network's nodes are subpopulations. Their number is $V$, and $V_k = V p_k$ of them have degree $k$. The shared notation calls this $N$, but here $N$ counts *people*.
  - $\mathcal N$ is the total number of individuals, and $\bar N = \mathcal N / V$ the mean subpopulation size.
  - $p$ is the per-capita **mobility rate**. Don't confuse it with the degree distribution $p_k$.
  - $\alpha$ is the final attack rate of a local SIR outbreak. The papers write $\bar\alpha$ or $\alpha$.
  - $s_{k'k}$ is the number of infected travellers seeding a degree-$k$ node from a degree-$k'$ node. The papers call this $\lambda_{k'k}$; it is renamed here to avoid a clash with $\lambda = \beta/\mu$.

(sec-meta-definitions)=
## Setup and definitions

:::{prf:definition} Metapopulation network
:label: def-meta-network

A graph with $V$ nodes (subpopulations) and degree distribution $p_k$. Node $i$ holds $N_i \ge 0$ individuals, any non-negative integer including 0, split into compartments (e.g. $S_i + I_i + R_i = N_i$). Within a node individuals mix homogeneously and change state by the disease reactions. Between nodes they move along edges. The total population $\mathcal N = \sum_i N_i$ is conserved.
:::

:::{prf:definition} Degree-block variables
:label: def-meta-blocks

These are averages over the $V_k$ nodes of degree $k$:

$$
N_k = \frac{1}{V_k}\sum_{i:\,k_i = k} N_i, \qquad I_k = \frac{1}{V_k}\sum_{i:\,k_i = k} I_i, \qquad S_k = \frac{1}{V_k}\sum_{i:\,k_i = k} S_i .
$$

The degree-based mean-field assumption is that all nodes of the same degree, and the people in them, are statistically equivalent. It is the same closure as in [heterogeneous mean-field theory](./05-heterogeneous-mean-field.md), applied to *nodes that contain populations*.
:::

:::{prf:definition} Markovian mobility
:label: def-meta-mobility

Let $d_{kk'}$ be the per-capita rate of moving along one particular edge from a degree-$k$ node to a degree-$k'$ node. The total leaving rate is $d_k = k \sum_{k'} P(k'|k)\, d_{kk'}$. Individuals carry no memory of where they came from. Two standard choices:
- **Homogeneous diffusion:** $d_{kk'} = p/k$. Each individual leaves at rate $p$ and picks one of the $k$ edges uniformly.
- **Traffic-driven diffusion:** $d_{kk'} = p\, w_0 (k k')^\theta / T_k$. Here $\langle w_{kk'}\rangle = w_0 (kk')^\theta$ is the mean edge traffic and $T_k = \sum_{k'} w_{kk'}$, so the leaving rate is still $p$. The worldwide air network has $\theta \simeq 0.5$ (cited in Colizza & Vespignani 2008).
:::

:::{prf:definition} Reaction kernels
:label: def-meta-kernels

Let $\Gamma_k$ be the rate at which new infections are generated in a degree-$k$ node, per unit $\beta$.
- **Mass action** (the Nature Physics paper's "type II"): $\Gamma_k = I_k S_k / N_k$. Each individual has a fixed number of contacts, so the force of infection is $\beta I/N$. This is the usual epidemic case.
- **Pseudo-mass action** ("type I"): $\Gamma_k = I_k S_k$. Each susceptible can react with *every* infected individual in the node, so a crowded node is more infectious. The review mentions animal diseases and mobile-phone malware as uses.
:::

:::{prf:definition} Global invasion number $R_*$
:label: def-meta-rstar

$R_*$ is the mean number of subpopulations that one infected subpopulation infects, early in the process when almost every subpopulation is still disease-free. It is $R_0$ lifted from individuals to subpopulations. Global (macroscopic) invasion requires $R_* > 1$ in addition to $R_0 > 1$.
:::

(sec-meta-core)=
## Core ideas

### 1. Diffusion alone: hubs are crowded

The degree-block balance equation for non-interacting diffusing individuals ([RMP review](doi:10.1103/RevModPhys.87.925), eq. 81) is

$$
\frac{dN_k}{dt} = -d_k N_k(t) + k \sum_{k'} P(k'|k)\, d_{k'k}\, N_{k'}(t).
$$ (eq-meta-diffusion)

The first term counts people leaving. The second counts arrivals on each of the $k$ edges from neighbours of every degree $k'$. Its stationary solution ({prf:ref}`prop-meta-occupancy`) puts population proportional to degree, or to $k^{1+\theta}$ when travel follows traffic. *Caveat from Colizza & Vespignani (2008):* in this framework subpopulation sizes are **set by the diffusion**, whereas real populations are independent data. Empirically $N_k \sim k^{\phi}$ with $0.5 \le \phi \le 1.5$, so the model is a first approximation in which $\theta$ tunes the heterogeneity.

### 2. Reaction–diffusion SIS: the kernel decides whether topology matters

The papers use a discrete-time scheme: react first, then every individual diffuses with probability 1, $d_{kk'} = 1/k$. On an uncorrelated network, $P(k'|k) = k'p_{k'}/\langle k\rangle$, and the infected update is (RMP eq. 85)

$$
I_k(t+1) = \frac{k}{\langle k\rangle}\Big[(1-\mu)\,\bar I(t) + \beta\,\Gamma(t)\Big], \qquad \bar I = \sum_k p_k I_k,\quad \Gamma = \sum_k p_k \Gamma_k ,
$$ (eq-meta-sis)

with the matching equation for $S_k$. In the stationary state the two kernels behave completely differently ({prf:ref}`prop-meta-sis`):

| Kernel | Endemic state exists iff | Effect of $\langle k^2\rangle \to \infty$ |
|---|---|---|
| mass action, $\Gamma_k = I_kS_k/N_k$ | $\beta/\mu > 1$ | none: activity per capita is the same in every node |
| pseudo-mass action, $\Gamma_k = I_kS_k$ | $\bar N > \bar N_c = \dfrac{\langle k\rangle^2}{\langle k^2\rangle}\dfrac{\mu}{\beta}$ | $\bar N_c \to 0$: a crowded hub can always sustain infection |

The explanation (Colizza et al. 2007) is that diffusion packs individuals into hubs in proportion to $k$. Under pseudo-mass action a hub's reaction rate grows with its occupancy, so some sufficiently large hub can keep the process alive at any mean density. Under mass action the rate is rescaled by the local population, which erases the advantage. Saldaña's continuous-time version, as cited in the review, gives $\bar N_c \sim k_{\max}^{-1}$ instead.

### 3. Why SIR needs a second threshold

Take the SIR model in each node with $R_0 = \beta/\mu > 1$ and per-capita mobility $p$. There are two limits:
- **$p = 0$:** every outbreak stays where it started.
- **$p \to 1$:** people wander constantly, and the system acts like one well-mixed population, so $R_0 > 1$ gives a global epidemic.

A critical $p_c$ must lie in between. An SIR outbreak in a node is **finite in time**: it produces about $\alpha N_k$ cases, each infectious for about $\mu^{-1}$. Infection spreads to another node only if at least one infected *individual* travels there during that window, *and* the seed then avoids early stochastic extinction. Neither condition exists in a continuous deterministic model. There, any fraction $p\bar I$ of travelling infection, even a "nano-individual", inoculates the next node, so no invasion threshold appears (RMP §IX.B). SIS has no global threshold either: an endemic node exports infection indefinitely, so sooner or later it seeds its neighbours.

The invasion process is analysed as a **Levins-type branching process over subpopulations**, analogous to the branching of individuals that defines $R_0$. Let $D_k^n$ be the number of subpopulations of degree $k$ infected in generation $n$. The result is {prf:ref}`thm-meta-invasion`.

### 4. Beyond memoryless diffusion: recurrent mobility

Real mobility is dominated by **commuting**: bidirectional, recurrent trips in which people remember where home is. Balcan & Vespignani (2011) model individuals who visit a neighbour at rate $\sigma$ and return home after a mean visit time $\tau$. If the disease time-scale $\mu^{-1}$ is much longer than the visit time, the visitor populations sit at quasi-stationary values. Infection then passes between neighbours both through infected visitors and through susceptible visitors who are infected abroad and bring it home. The same subpopulation branching argument, near $R_0 \simeq 1$, then gives a threshold of the form $R_* \propto (R_0-1)^2/R_0^2$, times a population-size factor and a function of $\rho = \sigma\tau$ and of the degree moments up to $\langle k^4\rangle$. The threshold now lives in the $\sigma$–$\tau$ plane. Invasion needs *either* frequent enough visits ($\sigma > \sigma_c$) *or* long enough visits ($\tau > \tau_c$). Heterogeneity again lowers the threshold. *(Text extraction garbled part of their eq. 4, so only its structure is given here, not the full expression.)*

### 5. Data-driven metapopulations: GLEaM

The GLobal Epidemic and Mobility model (Balcan et al. 2009) is a stochastic, discrete-individual metapopulation model at world scale.

**Subpopulations.** A 15′×15′ (arc-minute) population grid from SEDAC's Gridded Population of the World is divided into census areas. Each cell goes to the nearest IATA airport in the same country within 200 km, giving a Voronoi-like tessellation of more than 3,000 airports in 220 countries.

**Long-range mobility.** Air travel is drawn from IATA data. Each of the $N_j$ residents of city $j$ flies to city $\ell$ with probability $\omega_{j\ell}\,\delta t/N_j$, so passenger numbers are multinomial.

**Short-range mobility.** Commuting is built from data for 29 countries on 5 continents. It is fitted by a gravity law $w_{ij} = C\,N_i^{a}N_j^{c}\,e^{-d_{ij}/r}$, with an exponential decay that holds up to about 300 km. (The paper writes $\alpha, \gamma$ for the exponents; renamed here.) Average commuting flows are about an order of magnitude larger than airline flows.

**Time-scale separation.** A day trip of about 1/3 day is far shorter than the about 3-day infectious period, so commuting enters the *force of infection* through stationary visitor populations instead of being simulated trip by trip. With visit rate $\sigma_{ji}$ and mean visit time $\tau$, and writing $\sigma_j = \sum_i \sigma_{ji}$, the stationary split is

$$
X^{[m]}_{jj} = \frac{X^{[m]}_j}{1+\sigma_j\tau}, \qquad X^{[m]}_{ji} = \frac{X^{[m]}_j\,\sigma_{ji}\tau}{1+\sigma_j\tau}.
$$

(The paper uses the return *rate*; I wrote it in terms of the visit time $\tau$ to match Balcan & Vespignani's $\rho = \sigma\tau$.)

**Disease model.** An influenza-like SLIR model: latent period $\varepsilon^{-1} = 1.9$ days, infectious period $\mu^{-1} = 3$ days, asymptomatic fraction $p_a = 0.33$ with relative infectiousness $r_\beta = 0.5$, and a probability 0.5 that symptomatic people still travel. It has $R_0 = \beta\mu^{-1}(1 - p_a + r_\beta p_a)$ and includes seasonality.

**Finding.** In a pandemic-like scenario seeded in Hanoi ($R_0 = 1.9$), adding commuting barely changes the global timing and size compared with airline-only GLEaM. It does increase synchronisation between nearby subpopulations and matters at the periphery of the airline network.

(sec-meta-results)=
## Key results

:::{prf:proposition} Stationary occupancy under diffusion
:label: prop-meta-occupancy

On an uncorrelated network with homogeneous diffusion $d_{kk'} = p/k$, the stationary solution of {eq}`eq-meta-diffusion` is

$$
N_k = \frac{k}{\langle k\rangle}\,\bar N .
$$ (eq-meta-occupancy)

With traffic-driven diffusion $d_{kk'} = p\,w_0(kk')^\theta/T_k$, it is $N_k = \dfrac{k^{1+\theta}}{\langle k^{1+\theta}\rangle}\,\bar N$. Neither depends on $p$, which sets only the relaxation time.
:::

:::{dropdown} Derivation
With $d_{kk'} = p/k$, the leaving rate is $d_k = k\sum_{k'}P(k'|k)\,p/k = p$. Uncorrelated means $P(k'|k) = k'p_{k'}/\langle k\rangle$, so the arrival term is $k\sum_{k'}\frac{k'p_{k'}}{\langle k\rangle}\frac{p}{k'}N_{k'} = \frac{pk}{\langle k\rangle}\bar N$. Setting $dN_k/dt = 0$ gives {eq}`eq-meta-occupancy`, and $\sum_k p_k N_k = \bar N$ checks.

For the traffic case, Colizza & Vespignani (2008) take $T_k = A k^{1+\theta}$ with $A = \langle k^{1+\theta}\rangle w_0/\langle k\rangle$. The same steps give $N_k \propto k^{1+\theta}$, and normalising fixes the constant.
:::

:::{prf:proposition} SIS thresholds in a reaction–diffusion metapopulation
:label: prop-meta-sis

Consider the discrete-time scheme {eq}`eq-meta-sis` on an uncorrelated network, with susceptibles and infecteds both diffusing. Under **mass action**, an endemic state $\bar I > 0$ exists iff $\beta/\mu > 1$. Under **pseudo-mass action**, $\bar I > 0$ exists iff

$$
\bar N > \bar N_c = \frac{\langle k\rangle^2}{\langle k^2\rangle}\,\frac{\mu}{\beta}.
$$ (eq-meta-pseudo)
:::

:::{dropdown} Derivation (mine, following the structure of the Nature Physics paper)
**Stationary state.** Average {eq}`eq-meta-sis` over $p_k$ in the stationary state: $\bar I = (1-\mu)\bar I + \beta\Gamma$, so $\beta\Gamma = \mu\bar I$. Substituting back gives $I_k = (k/\langle k\rangle)\bar I$, and the $S_k$ equation likewise gives $S_k = (k/\langle k\rangle)\bar S$. So $N_k = (k/\langle k\rangle)\bar N$, consistent with {prf:ref}`prop-meta-occupancy`.

**Pseudo-mass action.** $\Gamma = \sum_k p_k I_kS_k = \frac{\langle k^2\rangle}{\langle k\rangle^2}\bar I\bar S$. Then $\beta\Gamma = \mu\bar I$ with $\bar I \ne 0$ gives $\bar S = \frac{\langle k\rangle^2}{\langle k^2\rangle}\frac{\mu}{\beta}$. Because $\bar I = \bar N - \bar S > 0$, this is {eq}`eq-meta-pseudo`.

**Mass action.** $\Gamma = \sum_k p_k I_kS_k/N_k = \sum_k p_k\frac{k}{\langle k\rangle}\frac{\bar I\bar S}{\bar N} = \bar I\bar S/\bar N$. Then $\bar S = \bar N\mu/\beta$, and $\bar I > 0$ iff $\beta/\mu > 1$. The degree moments cancel.

*A discrepancy:* the Nature Physics paper's eq. (6) has $\langle k\rangle^2/\langle k^2\rangle$, matching this derivation. The RMP review's eq. (87) is printed with $\langle k\rangle$ in the numerator, which is not dimensionally a density ratio. I follow the primary paper.
:::

:::{prf:theorem} Global invasion threshold (Colizza & Vespignani 2007)
:label: thm-meta-invasion

Take an SIR metapopulation on an uncorrelated network with homogeneous diffusion $d_{kk'} = p/k$, so that $N_k = k\bar N/\langle k\rangle$. Assume $R_0 - 1 \ll 1$ and that only a small fraction of subpopulations is infected. Then the number of invaded subpopulations grows from one generation to the next iff

$$
R_* = (R_0 - 1)\,\frac{\langle k^2\rangle - \langle k\rangle}{\langle k\rangle^2}\,\frac{p\bar N\alpha}{\mu} > 1 .
$$ (eq-meta-rstar)

Using the near-threshold SIR attack rate $\alpha \simeq 2(R_0-1)/R_0^2$, the **critical mobility** is

$$
p_c\bar N = \frac{\langle k\rangle^2}{\langle k^2\rangle - \langle k\rangle}\,\frac{\mu R_0^2}{2(R_0-1)^2}.
$$ (eq-meta-pc)
:::

:::{dropdown} Derivation (branching process over subpopulations)
**Seeds per edge.** A local outbreak in a degree-$k$ node infects about $\alpha N_k$ people in total. Each is infectious for about $\mu^{-1}$ and moves along a given edge at rate $p/k$. The expected number of infected travellers along one edge during the outbreak is therefore

$$
s_{kk'} = \frac{p}{k}\,\frac{\alpha N_k}{\mu} = \frac{p\bar N\alpha}{\mu\langle k\rangle},
$$

which does not depend on $k$ because $N_k \propto k$.

**Probability a seeded node takes off.** A single infected individual in a large susceptible population goes extinct with probability $1/R_0$. With $s$ independent seeds the probability is $R_0^{-s}$, so an outbreak occurs with probability $1 - R_0^{-s}$.

**Recursion.** Each infected node of degree $k'$ in generation $n-1$ can seed its $k'-1$ neighbours other than the one that infected it. Each of those has degree $k$ with probability $P(k|k')$ and is still uninfected with probability $1 - D_k^{n-1}/V_k$:

$$
D_k^n = \sum_{k'} D_{k'}^{n-1}(k'-1)\,P(k|k')\Big(1 - \frac{D_k^{n-1}}{V_k}\Big)\Big(1 - R_0^{-s_{k'k}}\Big).
$$

**Linearise.** Use three approximations: $1 - R_0^{-s} \simeq s(R_0-1)$; $D_k^{n-1}/V_k \ll 1$; and the uncorrelated form $P(k|k') = kp_k/\langle k\rangle$. Then

$$
D_k^n = (R_0-1)\,\frac{k p_k}{\langle k\rangle^2}\,\frac{p\bar N\alpha}{\mu}\sum_{k'}D_{k'}^{n-1}(k'-1).
$$

Define $\Theta^n = \sum_k D_k^n (k-1)$. Multiplying by $(k-1)$ and summing gives $\sum_k kp_k(k-1) = \langle k^2\rangle - \langle k\rangle$, so

$$
\Theta^n = (R_0-1)\,\frac{\langle k^2\rangle - \langle k\rangle}{\langle k\rangle^2}\,\frac{p\bar N\alpha}{\mu}\;\Theta^{n-1} = R_*\,\Theta^{n-1}.
$$

**Threshold.** Growth requires $R_* > 1$. Putting in $\alpha \simeq 2(R_0-1)/R_0^2$, from expanding the final-size relation $\alpha = 1 - e^{-R_0\alpha}$ near $R_0 = 1$, gives {eq}`eq-meta-pc`.

*My note on the first approximation:* $1 - R_0^{-s} = 1 - e^{-s\ln R_0}$. Replacing it by $s(R_0-1)$ needs **both** $s\ln R_0 \ll 1$ and $\ln R_0 \simeq R_0 - 1$. The worked example shows how fast this breaks down. The papers state only the $R_0 - 1 \ll 1$ condition explicitly.
:::

:::{prf:proposition} Traffic-weighted mobility (Colizza & Vespignani 2008)
:label: prop-meta-theta

With $d_{kk'} = p\,w_0(kk')^\theta/T_k$, the same steps give

$$
R_* = (R_0-1)\,\frac{\langle k^{2+2\theta}\rangle - \langle k^{1+2\theta}\rangle}{\langle k^{1+\theta}\rangle^2}\,\frac{p\bar N\alpha}{\mu},
$$

which reduces to {eq}`eq-meta-rstar` at $\theta = 0$. With $\theta > 0$ the effective heterogeneity is larger, so $p_c$ is lower still. For a homogeneous network in which every node has degree $\bar k$, the threshold becomes $p_c\bar N = \frac{\bar k}{\bar k - 1}\frac{\mu R_0^2}{2(R_0-1)^2}$.
:::

:::{important} Two thresholds
A metapopulation has two thresholds:
- **Local:** $R_0 > 1$. A single seed has a finite chance of a large outbreak *inside* a node.
- **Global:** $R_* > 1$. Mobility is high enough for outbreaks to cascade *between* nodes.

$R_*$ has the same structure as a next-generation number: an outbreak probability per seed, times seeds per edge, times the mean excess degree $(\langle k^2\rangle - \langle k\rangle)/\langle k\rangle$. Balcan & Vespignani compute it as the largest eigenvalue of a subpopulation next-generation matrix.
:::

## Worked example

Every number below comes from a Python script with the parameters shown.

**Occupancy.** Take degree distribution $p_2 = 0.5$, $p_4 = 0.3$, $p_{10} = 0.2$, so $\langle k\rangle = 4.2$, and set $\bar N = 1000$:

| $k$ | $N_k$, homogeneous diffusion ($\theta = 0$) | $N_k$, traffic-driven ($\theta = 0.5$) |
|---|---|---|
| 2 | 476.2 | 279.0 |
| 4 | 952.4 | 789.1 |
| 10 | 2381.0 | 3119.0 |

Both columns average to 1000. Weighting travel by traffic concentrates people in hubs even more.

**Attack rate and the near-threshold approximation.** The exact $\alpha$ solves $\alpha = 1 - e^{-R_0\alpha}$:

| $R_0$ | exact $\alpha$ | $2(R_0-1)/R_0^2$ |
|---|---|---|
| 1.1 | 0.1761 | 0.1653 |
| 1.2 | 0.3137 | 0.2778 |
| 1.5 | 0.5828 | 0.4444 |
| 2.0 | 0.7968 | 0.5000 |

**Outbreak probability per seeded node**, at $R_0 = 1.2$:

| seeds $s$ | $1 - R_0^{-s}$ | $s\ln R_0$ | $s(R_0-1)$ |
|---|---|---|---|
| 0.1 | 0.0181 | 0.0182 | 0.0200 |
| 1 | 0.1667 | 0.1823 | 0.2000 |
| 5 | 0.5981 | 0.9116 | 1.0000 |

The linearisation is accurate only for small $s$. Once there are a few seeds per edge it overstates the outbreak probability badly.

**Invasion threshold.** Take influenza-like parameters $R_0 = 1.2$ and $\mu = 1/3\ \text{day}^{-1}$, with $\bar N = 1000$ and $p = 0.003\ \text{day}^{-1}$, so $p\bar N = 3$ travellers per day. Use $\alpha = 2(R_0-1)/R_0^2$, and write $\chi = (\langle k^2\rangle - \langle k\rangle)/\langle k\rangle^2$:

| mobility network | $\langle k\rangle$ | $\langle k^2\rangle$ | $\chi$ | $p_c\bar N$ | $R_*$ | $R_*$ if $p$ is cut 90% |
|---|---|---|---|---|---|---|
| regular, $k = 10$ | 10 | 100 | 0.900 | 6.667 | 0.450 | 0.045 |
| Poisson, $\langle k\rangle = 10$ (untruncated) | 10 | 110 | 1.000 | 6.000 | 0.500 | 0.050 |
| power law $p_k \propto k^{-2.1}$, $k = 2..1000$ | 8.17 | 992.4 | 14.748 | 0.407 | 7.374 | 0.737 |

At the same mobility, the homogeneous networks are **below** the invasion threshold and the heavy-tailed one is far **above** it, even with a *smaller* mean degree. Cutting all travel by 90% brings the heavy-tailed system only just below $R_* = 1$. That is the quantitative content of the claim that travel restrictions work only when they are extreme. With traffic weighting at $\theta = 0.5$, the factor $\chi$ rises to 109.6 and $p_c\bar N$ drops to 0.055. With the exact $\alpha = 0.3137$ in place of the approximation, the three $R_*$ values become 0.508, 0.565 and 8.328.

## Assumptions and limitations

- **Near-threshold, early-time, tree-like.** The closed form {eq}`eq-meta-rstar` assumes $R_0 - 1 \ll 1$, few infected subpopulations, no loops in the invasion tree, and an uncorrelated mobility network. Away from $R_0 \approx 1$ the threshold is available only as an implicit expression (Colizza & Vespignani 2007).
- **Populations set by diffusion.** $N_k \propto k$ or $k^{1+\theta}$ comes from the mobility model, not from census data.
- **Markovian travel.** Individuals forget where they came from. Commuting breaks this and changes the threshold to depend on visit rate and duration. Travel probability is also assumed the same in every compartment. GLEaM relaxes this: some symptomatic people don't travel.
- **Infinite networks.** In heavy-tailed networks $\langle k^2\rangle$ diverges, so $p_c \to 0$ as size grows. Colizza & Vespignani (2008) note that for infinite networks the equations should be rewritten in densities of infected subpopulations to avoid this divergence. Real networks are finite, so $p_c$ is small but positive.
- **Gravity-law fits are scale-specific.** Balcan et al. (2009) stress that their exponents hold at the airport-centred Voronoi granularity and should not be transferred to other spatial units.
- *My comment:* the SIS results use a discrete-time update in which reaction and diffusion happen in sequence and everyone moves each step. That is a simulation-friendly idealisation, not a model of real travel frequency.

## Connections

- **PHYS 7335.**
  - [Random walks on networks](./02-random-walks.md): the occupancy result is the stationary random-walk distribution $\propto k$.
  - [Heterogeneous mean-field epidemics](./05-heterogeneous-mean-field.md): the $\langle k^2\rangle$ factor plays the same role, and here it lowers a *mobility* threshold rather than a transmission threshold.
  - [Thresholds and next-generation matrices](./04-thresholds-and-ngm.md): $R_*$ is a next-generation number for subpopulations.
  - [Compartmental models and $R_0$](./03-compartmental-models.md): supplies $\alpha$ and the extinction probability $1/R_0$.
  - [SIR–percolation mapping](./07-sir-percolation.md): the factor $(\langle k^2\rangle - \langle k\rangle)/\langle k\rangle$ is the mean excess degree $G_1'(1)$, the same branching factor that governs outbreaks on contact networks.
- **NETS 5116.**
  - Barabási's chapter on [spreading phenomena](../nets-5116/barabasi/10-spreading-phenomena.md) treats individuals as nodes; metapopulations move one level up.
  - The [scale-free networks](../nets-5116/barabasi/04-scale-free-networks.md) notes explain why $\langle k^2\rangle$ diverges for $\gamma \le 3$.
  - The [robustness](../nets-5116/barabasi/08-network-robustness.md) notes use the same excess-degree branching argument (Molloy–Reed).
- **NETS 7332.**
  - The [representations reading](../nets-7332/readings/01-representations.md) lists metapopulation models among the "other formalisms", where nodes carry internal structure.
  - The random-surfer stationary distribution on the [link-analysis page](../nets-7332/basics/02-link-analysis.md) is the same object as {eq}`eq-meta-occupancy`.

## Self-test

:::{dropdown} Q1. Why is a metapopulation model "bosonic", and what does diffusion do to node populations on an uncorrelated network?
Nodes have no occupancy limit: any integer number of individuals can sit at a node. With per-capita leaving rate $p$ and uniform choice of edge, the stationary occupancy is $N_k = (k/\langle k\rangle)\bar N$, so hubs hold more people. With traffic-weighted travel it is $N_k \propto k^{1+\theta}$.
:::

:::{dropdown} Q2. For SIS, why does the threshold depend on topology under pseudo-mass action but not under mass action?
Under pseudo-mass action ($\Gamma_k = I_kS_k$), new infections in a node grow with its occupancy, and diffusion makes occupancy $\propto k$. The density threshold is therefore $\bar N_c = (\langle k\rangle^2/\langle k^2\rangle)\mu/\beta$, which goes to 0 when $\langle k^2\rangle \to \infty$. Under mass action ($\Gamma_k = I_kS_k/N_k$), activity per capita is the same everywhere, the degree moments cancel, and the condition is $\beta/\mu > 1$.
:::

:::{dropdown} Q3. Why can an SIR metapopulation fail to spread globally even though $R_0 > 1$, while an SIS one cannot?
An SIR outbreak in a node is finite: about $\alpha N_k$ cases over about $\mu^{-1}$ each. Unless enough infected *individuals* travel during that window, and their seeds avoid stochastic extinction (probability $R_0^{-s}$), the infection never leaves the node. An SIS endemic node keeps exporting infection forever, so it eventually seeds its neighbours.
:::

:::{dropdown} Q4. Write $R_*$ and say where each factor comes from.
$R_* = (R_0-1)\cdot\frac{\langle k^2\rangle - \langle k\rangle}{\langle k\rangle^2}\cdot\frac{p\bar N\alpha}{\mu}$.
- $\frac{p\bar N\alpha}{\mu\langle k\rangle}$ is the number of infected travellers per edge during an outbreak.
- $(R_0-1)$ times that is the probability a seeded node takes off, from linearising $1 - R_0^{-s}$.
- $\frac{\langle k^2\rangle - \langle k\rangle}{\langle k\rangle}$ is the mean number of onward edges, the excess degree.
:::

:::{dropdown} Q5. Why can't a deterministic ODE metapopulation model show an invasion threshold?
It lets any real-valued fraction of infection travel. An arbitrarily small $p\bar I$ ("nano-individuals") starts exponential growth in every connected node whenever $R_0 > 1$. The threshold depends on the integer nature of travellers and on the stochastic extinction of small seeds.
:::

:::{dropdown} Q6. In the worked example, why does cutting travel by 90% barely bring the heavy-tailed system below threshold?
$R_*$ is linear in $p$, and heterogeneity multiplies it by $\chi = (\langle k^2\rangle - \langle k\rangle)/\langle k\rangle^2 \approx 14.7$ compared with about 1 for a Poisson network. Starting from $R_* \approx 7.4$, a tenfold cut leaves $0.74$, just under 1. The same mobility leaves a homogeneous network at $R_* \approx 0.5$ even without restrictions.
:::

:::{dropdown} Q7. How does GLEaM include commuting without simulating sub-daily trips?
By **time-scale separation**. Commuting visits last about 1/3 day, much shorter than the 3-day infectious period, so visitor numbers are replaced by their quasi-stationary values $X_{ji} = X_j\sigma_{ji}\tau/(1+\sigma_j\tau)$, which enter each subpopulation's force of infection. Air travel is simulated explicitly as multinomial movements of individuals.
:::

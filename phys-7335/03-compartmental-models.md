---
title: Compartmental Models (SI, SIS, SIR, SEIR) and the Basic Reproduction Number
short_title: Compartmental models
subject: PHYS 7335 · Topic
description: Homogeneous-mixing epidemic models as reaction schemes, their threshold at R_0 = 1, and the classical results on growth rate, final size, peak prevalence, herd immunity and early extinction.
tags: [epidemics, compartmental-models, sir, sis, seir, reproduction-number, final-size, branching-process]
---

:::{tip} TL;DR
- An epidemic model is a **reaction scheme** on compartments. SIR is $S + I \xrightarrow{\beta} 2I$ plus $I \xrightarrow{\mu} R$. SIS replaces $R$ by $S$. SEIR inserts a latent class, $S + I \to E + I$ then $E \xrightarrow{\sigma} I$. Under **homogeneous mixing** (mass action), the densities obey ODEs in which the **force of infection** is $\bar\beta\, i$, with $\bar\beta = \beta \langle k \rangle$: a per-contact rate $\beta$ times $\langle k \rangle$ contacts.
- **$R_0 = \bar\beta/\mu = \beta\langle k\rangle/\mu$** is the mean number of secondary cases from one infective in a fully susceptible population. At the start of an outbreak SIS and SIR both grow as $i(t) \simeq i(0)\,e^{(\bar\beta - \mu)t}$, so the threshold is $R_0 = 1$.
- The **SIS endemic state** is $i^* = 1 - 1/R_0$. In **SIR** every outbreak ends, and the **final size** solves $r_\infty = 1 - e^{-R_0 r_\infty}$. This equation has a positive root iff $R_0 > 1$, and near threshold $r_\infty \approx 2(R_0-1)/R_0^2$.
- Two identities follow from $s = 1/R_0$. **Prevalence peaks** when $s = 1/R_0$, at $i_{\max} = 1 - (1 + \ln R_0)/R_0$. **Herd immunity**, the point where $R_t = R_0 s$ falls to 1, needs an immune fraction $1 - 1/R_0$.
- Deterministic $R_0 > 1$ is **necessary but not sufficient** for an outbreak. The early phase is a branching process. One SIR seed with an exponential infectious period dies out with probability **$1/R_0$**.
:::

- **Source.** [](doi:10.1103/RevModPhys.87.925) (Pastor-Satorras, Castellano, Van Mieghem & Vespignani, *Epidemic processes in complex networks*, Rev. Mod. Phys. 87, 925 (2015), §II.A–C). Course slides, *degree-based representation* ([PHYS 7335 site](https://mobs-lab.github.io/phys7335/), weeks 3–4). Course textbook: Barrat, Barthélemy & Vespignani, [](doi:10.1017/CBO9780511791383), ch. 9. Historical origin: [](doi:10.1098/rspa.1927.0118) (Kermack & McKendrick, Proc. R. Soc. A 115, 700–721 (1927)).
- **Builds on.** The network-epidemics overview in [Barabási ch. 10 notes](../nets-5116/barabasi/10-spreading-phenomena.md).
- **Notation.** Shared symbols as in [](#notation). Lower-case $s, i, r$ (and $e$) are densities, $N^\alpha/N$. $\beta$ is the **per-contact** transmission rate and $\bar\beta \equiv \beta\langle k\rangle$ the per-capita rate. $\sigma$ is the $E \to I$ rate, $T_g$ the doubling time and $r_g$ the early growth rate, written $r_g$ so it isn't confused with the recovered density $r$.

(sec-comp-setup)=
## Setup and definitions

:::{prf:definition} Compartmental model as a reaction scheme
:label: def-comp-reactions

The population of $N$ individuals is partitioned into **compartments**. Each individual is in exactly one of them. Transitions are Poisson processes, written as reactions with rates:

| Model | Reactions |
|---|---|
| SI | $S + I \xrightarrow{\beta} 2I$ |
| SIS | $S + I \xrightarrow{\beta} 2I$, $\quad I \xrightarrow{\mu} S$ |
| SIR | $S + I \xrightarrow{\beta} 2I$, $\quad I \xrightarrow{\mu} R$ |
| SIRS | SIR plus $R \xrightarrow{\eta} S$ (waning immunity) |
| SEIR | $S + I \xrightarrow{\beta} E + I$, $\quad E \xrightarrow{\sigma} I$, $\quad I \xrightarrow{\mu} R$ |

The binary reaction is the only interaction. The others are spontaneous, and their mean sojourn times are $1/\mu$ (infectious period) and $1/\sigma$ (latent period).
:::

The Rev. Mod. Phys. review uses the same schemes. It calls the $E\to I$ rate $\gamma$; this page uses $\sigma$, because $\gamma$ is the degree exponent here.

:::{prf:definition} Homogeneous mixing and the force of infection
:label: def-comp-mixing

**Homogeneous mixing** means every individual is equally likely to contact any other. Members of a compartment are then indistinguishable, and the state is just the vector of densities. The **force of infection** $\alpha$ is the rate at which one susceptible is infected. Under the **mass-action law** it is proportional to the infected density:

$$
\alpha = \bar\beta\, i, \qquad \bar\beta = \beta \langle k \rangle,
$$ (eq-comp-force)

where each individual makes $\langle k \rangle$ contacts and each contact with an infective transmits at rate $\beta$.
:::

:::{important} Convention used on this page and on later network pages
The review writes the classical equations with a single per-capita rate (its $\bar\beta$; in its eqs. 6–10, just $\beta$). It then splits it as $\beta k$ for networks, giving $R_0 = \beta\langle k\rangle/\mu$ on a homogeneous network (its eq. 11). This page **keeps $\beta$ per contact** throughout, to match the shared notation and the [heterogeneous mean-field page](./05-heterogeneous-mean-field.md), and writes $\bar\beta = \beta\langle k\rangle$ wherever the classical form is meant. With $\lambda = \beta/\mu$, this gives $R_0 = \lambda \langle k \rangle$.

The two scalings differ in substance. $\alpha \propto i$ (density-dependent) means the number of contacts does not grow with $N$. The alternative $\alpha \propto N^I$ (frequency-scaled) assumes contacts grow with population size. The review notes that intermediate forms $\propto N^{-a}$ also appear.
:::

:::{prf:definition} Basic and effective reproduction numbers
:label: def-comp-r0

The **basic reproduction number** $R_0$ is the expected number of secondary infections caused by one infective introduced into a **fully susceptible** population. The **effective reproduction number** $R_t$ is the same quantity at time $t$, given the current susceptible fraction and any interventions. Under homogeneous mixing, $R_t = R_0\, s(t)$.
:::

(sec-comp-core)=
## Core ideas

### The mean-field equations

Applying mass action to {prf:ref}`def-comp-reactions` gives deterministic ODEs for the densities. They are valid as $N \to \infty$, where fluctuations vanish.

$$
\begin{aligned}
\text{SI:}\quad & \dot i = \bar\beta\, s\, i, & s &= 1 - i,\\
\text{SIS:}\quad & \dot i = \bar\beta\, s\, i - \mu i, & s &= 1 - i,\\
\text{SIR:}\quad & \dot s = -\bar\beta\, s\, i,\quad \dot i = \bar\beta\, s\, i - \mu i,\quad \dot r = \mu i,\\
\text{SEIR:}\quad & \dot s = -\bar\beta\, s\, i,\quad \dot e = \bar\beta\, s\, i - \sigma e,\quad \dot i = \sigma e - \mu i,\quad \dot r = \mu i.
\end{aligned}
$$ (eq-comp-odes)

The SI model, logistic growth $i(t) = i_0 e^{\bar\beta t}/(1 - i_0 + i_0 e^{\bar\beta t})$, is the $\mu \to 0$ limit. It describes the early phase of both SIS and SIR when recovery is slow.

### Linearisation and the threshold

Early on $s \simeq 1$. For both SIS and SIR the infected equation linearises to

$$
\dot i \simeq (\bar\beta - \mu)\, i \quad\Longrightarrow\quad i(t) \simeq i(0)\, e^{r_g t}, \qquad r_g = \bar\beta - \mu = \mu (R_0 - 1),
$$ (eq-comp-growth)

so the outbreak grows iff $R_0 = \bar\beta/\mu > 1$. The doubling time is $T_g = \ln 2 / r_g$. For SEIR the growth rate is the largest eigenvalue of the linearised $(e, i)$ system:

$$
r_g = \tfrac12\Big[-(\sigma + \mu) + \sqrt{(\sigma - \mu)^2 + 4\sigma\bar\beta}\Big],
$$ (eq-comp-seir-growth)

which is smaller than $\bar\beta - \mu$. A latent period does **not** change $R_0 = \bar\beta/\mu$, but it slows the growth. How $r_g$ and $R_0$ relate in general, through the generation-interval distribution, is covered on [the thresholds and next-generation-matrix page](./04-thresholds-and-ngm.md).

### What "threshold" means

The threshold separates two regimes, in the language of non-equilibrium phase transitions that the review adopts:

| | $R_0 < 1$ | $R_0 > 1$ |
|---|---|---|
| SIS | the absorbing healthy state $i = 0$ is the unique stable steady state | endemic steady state $i^* > 0$ |
| SIR | outbreak size $\to 0$ as $N \to \infty$ | an outbreak infecting a finite fraction $r_\infty > 0$ is possible |

The order parameter is the stationary prevalence $\rho$ for SIS and the final size $r_\infty$ for SIR. $\lambda = \beta/\mu$ is the control parameter, with $\lambda_c = 1/\langle k \rangle$ under homogeneous mixing.

### Stochastic picture

In a finite population the reactions are random events. The course slides use a discrete-time **chain-binomial** version. Each step, a susceptible in class $k$ is infected with probability $p_{S_k \to I_k}$, and the number of new infections is $\mathrm{Binom}(S_{k,t}, p_{S_k \to I_k})$. Recoveries are $\mathrm{Binom}(I_{k,t}, \mu\Delta t)$, and the total population is conserved. The continuous-time version is a Markov jump process, simulated exactly with the Gillespie algorithm.

Early on, while $s \simeq 1$, infectives act independently, so the process is a **Galton–Watson branching process**: each infective is replaced by a random number of offspring with mean $R_0$. This is why the deterministic threshold is only **necessary**. Even with $R_0 > 1$, an outbreak seeded by a few cases can go extinct by chance.

### Origin: Kermack and McKendrick (1927)

Kermack & McKendrick introduced the SIR model, as the review cites them. *I could not access the original paper.* The standard reading, my summary and not checked against the text, is this. Their model is more general than {eq}`eq-comp-odes`: infectivity and removal rates depend on the time since infection. They proved a threshold theorem and a final-size relation for that general model. Constant rates give the SIR ODE as a special case.

(sec-comp-results)=
## Key results

:::{prf:theorem} SIS endemic equilibrium
:label: thm-comp-sis

For SIS under homogeneous mixing, the fixed points of $\dot i = \bar\beta(1-i)i - \mu i$ are $i = 0$ and

$$
i^* = 1 - \frac{\mu}{\bar\beta} = 1 - \frac{1}{R_0}.
$$ (eq-comp-sis)

$i^*$ is positive and globally attracting on $(0,1]$ iff $R_0 > 1$. Otherwise $i = 0$ is globally attracting.
:::

:::{dropdown} Derivation
$\dot i = i\,[\bar\beta(1 - i) - \mu]$ is a logistic equation with net growth rate $\bar\beta - \mu$ and carrying capacity $1 - \mu/\bar\beta$. Linearising at $0$ gives eigenvalue $\bar\beta - \mu$. At $i^*$ the eigenvalue is $-(\bar\beta - \mu)$. Exactly one of the two fixed points is stable, according to the sign of $R_0 - 1$, and a one-dimensional flow has no other attractors.
:::

:::{prf:theorem} SIR final-size relation
:label: thm-comp-finalsize

For SIR with $s(0) = 1 - i_0$, $r(0) = 0$ and $i_0 \to 0^+$, the final recovered fraction $r_\infty$ satisfies

$$
r_\infty = 1 - e^{-R_0\, r_\infty}.
$$ (eq-comp-finalsize)

This has a root $r_\infty \in (0,1)$ iff $R_0 > 1$, and the root is unique. Near threshold, $r_\infty \simeq 2(R_0 - 1)/R_0^2$. That approximation, attributed to Bailey (1975), is quoted in the Rev. Mod. Phys. review, §IX (metapopulation models).
:::

:::{dropdown} Derivation (standard; written out here)
1. Divide the $s$ and $r$ equations: $\dfrac{ds}{dr} = -\dfrac{\bar\beta s i}{\mu i} = -R_0\, s$. So $s = s(0)\, e^{-R_0 r}$ along every trajectory.
2. Every epidemic ends ($i \to 0$), because $\dot r = \mu i \ge 0$ and $r \le 1$. So $s_\infty + r_\infty = 1$.
3. With $s(0) \to 1$ this gives $1 - r_\infty = e^{-R_0 r_\infty}$.
4. **Roots.** Let $\phi(x) = 1 - e^{-R_0 x} - x$. Then $\phi(0) = 0$, $\phi'(0) = R_0 - 1$, $\phi(1) = -e^{-R_0} < 0$, and $\phi'' = -R_0^2 e^{-R_0 x} < 0$. Because $\phi$ is strictly concave, it has a zero in $(0,1)$ iff its slope at $0$ is positive, i.e. $R_0 > 1$, and that zero is unique.
5. **Near threshold.** Expand $e^{-R_0 x} \approx 1 - R_0 x + R_0^2 x^2/2$. This gives $x \approx R_0 x - R_0^2 x^2/2$, so $x \approx 2(R_0 - 1)/R_0^2$.
:::

:::{prf:proposition} Peak prevalence and herd immunity
:label: prop-comp-peak

In SIR, $\dot i = i(\bar\beta s - \mu)$ vanishes when $s = 1/R_0$, i.e. when $R_t = 1$. With $s(0) \approx 1$, the peak prevalence is

$$
i_{\max} = 1 - \frac{1 + \ln R_0}{R_0}.
$$ (eq-comp-peak)

If a fraction $g$ is immune before the outbreak, the effective number is $R_0(1-g)$. No outbreak can grow iff

$$
g \ge g_c = 1 - \frac{1}{R_0}.
$$ (eq-comp-herd)
:::

:::{dropdown} Derivation (standard; written out here)
$\dfrac{di}{ds} = -1 + \dfrac{1}{R_0 s}$, so $i + s - \tfrac{1}{R_0}\ln s$ is conserved. At $t = 0$ this quantity is $\approx 1$, since $s \approx 1$ and $\ln s \approx 0$. At the peak, $s = 1/R_0$, so $i_{\max} = 1 - 1/R_0 + \tfrac{1}{R_0}\ln(1/R_0)$, which is {eq}`eq-comp-peak`.

For herd immunity, replace $s(0) = 1$ by $1 - g$ in the linearisation {eq}`eq-comp-growth`. The growth rate becomes $\bar\beta(1-g) - \mu$, which is non-positive iff $g \ge 1 - 1/R_0$. The review defines herd immunity in exactly this sense, as the immunised fraction that raises the effective threshold above the actual $\lambda$.
:::

:::{prf:proposition} Early extinction of a single seed
:label: prop-comp-extinction

In stochastic SIR with constant rates, one infective in a large susceptible population causes only a minor outbreak with probability

$$
q = \min\!\Big(1, \frac{1}{R_0}\Big).
$$ (eq-comp-extinction)

With $n$ initial infectives, $q^n$. The review quotes $P_{\mathrm{ext}} = 1/R_0$ from Bailey (1975).
:::

:::{dropdown} Derivation (my write-up of the standard argument)
While $s \simeq 1$, an infective transmits at rate $\bar\beta$ and recovers at rate $\mu$. Each event is a transmission with probability $p = \bar\beta/(\bar\beta + \mu) = R_0/(1 + R_0)$. So the number of offspring is **geometric**: $P(k) = (1-p)p^k$, with mean $p/(1-p) = R_0$.

The offspring generating function is $g(z) = \dfrac{1-p}{1 - pz} = \dfrac{1}{1 + R_0(1 - z)}$. The extinction probability is the smallest root of $q = g(q)$ in $[0,1]$. Solving $q\,[1 + R_0(1-q)] = 1$ gives $(q-1)(R_0 q - 1) = 0$, so $q = 1/R_0$ when $R_0 > 1$.

The result depends on the infectious-period distribution. A fixed infectious period gives Poisson offspring and $q = e^{-R_0(1-q)}$. That is the same equation as {eq}`eq-comp-finalsize` with $q = 1 - r_\infty$, and it gives a smaller $q$.
:::

## Worked example

Take $\langle k\rangle = 10$ contacts, a per-contact rate $\beta = 0.05\ \text{day}^{-1}$ and $\mu = 0.2\ \text{day}^{-1}$ (a 5-day infectious period). Then $\bar\beta = 0.5\ \text{day}^{-1}$, $\lambda = 0.25$ and $R_0 = 2.5$. Every number below was computed in Python. The ODEs were integrated with RK4 at $\Delta t = 0.01$ days from $i_0 = 10^{-6}$.

| Quantity | Formula | Value |
|---|---|---|
| Early growth rate (SIR/SIS) | $r_g = \bar\beta - \mu$ | $0.30\ \text{day}^{-1}$ |
| Doubling time | $\ln 2 / r_g$ | $2.31$ days |
| SIS endemic prevalence | $1 - 1/R_0$ | $0.600$; the ODE reaches $0.6000$ |
| SIR final size | root of {eq}`eq-comp-finalsize` | $0.8926$; the ODE gives $0.8926$ |
| Near-threshold approximation | $2(R_0-1)/R_0^2$ | $0.48$, a poor fit this far from threshold |
| Susceptible fraction at peak | $1/R_0$ | $0.400$; the ODE gives $0.3999$ |
| Peak prevalence | {eq}`eq-comp-peak` | $0.2335$; the ODE gives $0.2335$, at day 47.4 |
| Herd-immunity threshold | $1 - 1/R_0$ | $0.60$ |
| Extinction from one seed | $1/R_0$ | $0.40$ |

Adding a 3-day latent period ($\sigma = 1/3\ \text{day}^{-1}$, SEIR) leaves $R_0 = 2.5$ and $r_\infty = 0.8926$ unchanged. It cuts the growth rate to $r_g = 0.147\ \text{day}^{-1}$ by {eq}`eq-comp-seir-growth`, which doubles the doubling time to $4.72$ days. The peak becomes lower and later: $i_{\max} = 0.144$ at day 95. (As a check, $(1 + r_g/\sigma)(1 + r_g/\mu) = 2.500 = R_0$, the SEIR growth-rate relation derived on [the thresholds page](./04-thresholds-and-ngm.md).)

**Stochastic check.** I ran 20,000 Gillespie simulations with $N = 1000$ and one seed. The fraction that went extinct before reaching 50 cases was $0.406$, against $1/R_0 = 0.400$ (standard error about $0.004$ per batch of 10,000). Among the major outbreaks in a separate run with $N = 2000$, the mean final size was $0.893$, matching $r_\infty$.

## Assumptions and limitations

- **Homogeneous mixing is the central approximation.** It is the mean-field approximation of statistical physics: exact on high-dimensional lattices, not in low dimensions. On networks it fails badly, because degree heterogeneity changes the threshold. This is the subject of the [degree-block formalism](./01-degree-block-formalism.md) and [heterogeneous mean-field](./05-heterogeneous-mean-field.md) pages. The course slides end on the same point: annealed heterogeneous networks rescale $R_0 \to R_0\langle k^2\rangle/\langle k\rangle^2$.
- **Poisson (Markovian) transitions** imply exponential infectious and latent periods. Realistic, more peaked distributions change the relation between $r_g$ and $R_0$ and the extinction probability ({prf:ref}`prop-comp-extinction`), but not $r_\infty$ for a given $R_0$.
- **Deterministic equations hold only for large $N$.** Small populations, and the early phase of any outbreak, are governed by fluctuations ({prf:ref}`prop-comp-extinction`).
- **$R_0$ is not a property of the pathogen alone.** It includes the contact rate $\langle k\rangle$. The review cites Diekmann et al. (2012) on its weakness on lattices, where network and percolation theory are needed to locate the threshold.
- **The models omit** demography, age structure, behavioural feedback and interventions. Each can be added as extra compartments or time-dependent rates.

## Connections

- **NETS 5116.** [Barabási ch. 10](../nets-5116/barabasi/10-spreading-phenomena.md) sets up the same SI, SIS and SIR models before moving them onto networks. Its homogeneous results are the ones above with $\bar\beta = \beta\langle k\rangle$.
- **PHYS 7335.**
  - The [next-generation matrix](./04-thresholds-and-ngm.md) generalises $R_0 = \bar\beta/\mu$ to many infected compartments.
  - The [degree-block](./01-degree-block-formalism.md) and [heterogeneous mean-field](./05-heterogeneous-mean-field.md) pages replace $\langle k\rangle$ by the degree distribution.
  - The branching-process argument becomes the [SIR–percolation mapping](./07-sir-percolation.md), where $q = 1 - r_\infty$ is no coincidence.
  - [Rumour models](./08-rumor-and-social-contagion.md) change the recovery reaction to a binary one, and the threshold disappears.
- **NETS 7332.** *My comment:* the SIR final-size equation has the same fixed-point form as the self-consistency equations of [label propagation](../nets-7332/basics/04-label-propagation.md) and [PageRank](../nets-7332/basics/02-link-analysis.md). In all three, a global quantity is defined as a fixed point of local averaging.

## Self-test

:::{dropdown} Q1. Write the SIR ODEs under homogeneous mixing and derive the threshold from the linearisation.
$\dot s = -\bar\beta s i$, $\dot i = \bar\beta s i - \mu i$, $\dot r = \mu i$, with $\bar\beta = \beta\langle k\rangle$. With $s \approx 1$: $\dot i \approx (\bar\beta - \mu) i$, so $i$ grows iff $R_0 = \bar\beta/\mu > 1$.
:::

:::{dropdown} Q2. Why does $R_0 = \beta\langle k\rangle/\mu$ on one page and $R_0 = \beta/\mu$ in other texts?
It depends on whether $\beta$ is a **per-contact** rate (multiplied by $\langle k\rangle$ contacts) or already a **per-capita** rate $\bar\beta$. The review uses the per-capita form for the classical equations and $\beta\langle k\rangle/\mu$ for homogeneous networks.
:::

:::{dropdown} Q3. Derive the final-size relation and show a positive solution exists only for $R_0 > 1$.
$ds/dr = -R_0 s$, so $s = e^{-R_0 r}$. At the end $s_\infty = 1 - r_\infty$, giving $r_\infty = 1 - e^{-R_0 r_\infty}$. The function $\phi(x) = 1 - e^{-R_0 x} - x$ is strictly concave, with $\phi(0) = 0$, $\phi'(0) = R_0 - 1$ and $\phi(1) < 0$. It has a root in $(0,1)$ iff $\phi'(0) > 0$.
:::

:::{dropdown} Q4. When does SIR prevalence peak, and what fraction must be immunised to prevent growth?
At $s = 1/R_0$ (so $R_t = 1$), giving $i_{\max} = 1 - (1 + \ln R_0)/R_0$. The herd-immunity threshold is $1 - 1/R_0$.
:::

:::{dropdown} Q5. One infective is introduced with $R_0 = 3$. What is the probability of no major outbreak, and what assumption fixes the answer?
$1/R_0 = 1/3$. This assumes an exponentially distributed infectious period, which makes the offspring number geometric. A fixed infectious period gives Poisson offspring and the smaller root of $q = e^{-3(1-q)}$, about $0.06$.
:::

:::{dropdown} Q6. How does adding a latent period change $R_0$, the growth rate and the final size?
$R_0$ and $r_\infty$ are unchanged, since each infective still causes $\bar\beta/\mu$ cases. The growth rate falls (from $0.30$ to $0.147\ \text{day}^{-1}$ in the example), so the peak is lower and later.
:::

:::{dropdown} Q7. In what sense is the epidemic threshold a phase transition?
$\lambda = \beta/\mu$ is the control parameter, and the stationary prevalence (SIS) or final size (SIR) is the order parameter. As $N \to \infty$ the order parameter is zero for $\lambda \le \lambda_c$ and positive above it. SIS is a non-equilibrium transition into an **absorbing state**, in the same class of models as the contact process.
:::

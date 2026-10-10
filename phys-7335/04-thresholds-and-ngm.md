---
title: Epidemic Thresholds, Next-Generation Matrices and Growth Rates
short_title: Thresholds and NGMs
subject: PHYS 7335 · Topic
description: How to compute R_0 for any compartmental model as the spectral radius of a next-generation matrix, why it is a threshold, and how it relates to the observed growth rate.
tags: [epidemics, R0, next-generation-matrix, threshold, growth-rate, generation-interval]
---

:::{tip} TL;DR
- Linearise the **infected subsystem** at the disease-free state as $x' = (T + \Sigma)\,x$, where **$T$** holds *transmissions* (new infections) and **$\Sigma$** holds *transitions* (progression, recovery, death). Then $K_L = -T\Sigma^{-1}$, and **$R_0 = \rho(-T\Sigma^{-1})$** is its spectral radius (Diekmann, Heesterbeek & Roberts 2010, "DHR"). Here $\rho(\cdot)$ with an argument always means the spectral radius, not prevalence.
- $(-\Sigma^{-1})_{ij}$ is the expected time an individual now in state $j$ will spend in state $i$. So $K_{ij}$ counts the expected new infections in state $i$ caused by one individual infected into state $j$, over its whole infected life.
- **The threshold theorem.** $\operatorname{sign}\, s(T+\Sigma) = \operatorname{sign}(R_0 - 1)$, where $s(\cdot)$ is the spectral bound (largest real part of an eigenvalue). So the disease-free state is stable iff $R_0 < 1$. The growth rate $r = s(T+\Sigma)$ and $R_0$ always agree **in sign**, but not in magnitude.
- **The size of $r$ depends on the generation interval.** For a generation-interval density $g$, the Euler–Lotka relation gives $R_0 = 1/M(-r)$, with $M$ the moment generating function of $g$. SIR gives $R_0 = 1 + r/\mu$, and SEIR gives $R_0 = (1 + r/\sigma)(1 + r/\mu)$. A latent period leaves $R_0$ unchanged but **slows** growth.
- When transmission alternates between two types (sexes, vector and host), the NGM is off-diagonal and **$R_0 = \sqrt{K_{12}K_{21}}$**. It is the *per-generation* factor, the geometric mean over a two-generation cycle. On networks the degree-class NGM has rank one, and it reproduces the heterogeneous mean-field thresholds $\langle k\rangle/\langle k^2\rangle$ (SIS) and $\langle k\rangle/(\langle k^2\rangle - \langle k\rangle)$ (SIR).
:::

- **Source.** Diekmann, Heesterbeek & Roberts, *The construction of next-generation matrices for compartmental epidemic models*, J. R. Soc. Interface 7, 873 (2010) [](doi:10.1098/rsif.2009.0386) (the course reading). Wallinga & Lipsitch, Proc. R. Soc. B 274, 599 (2007) [](doi:10.1098/rspb.2006.3754) for growth rates and generation intervals. Pastor-Satorras, Castellano, Van Mieghem & Vespignani, Rev. Mod. Phys. 87, 925 (2015) [](doi:10.1103/RevModPhys.87.925) for network thresholds. Course: [PHYS 7335](https://mobs-lab.github.io/phys7335/), week 5.
- **Builds on.** Homogeneous-mixing SIR/SEIR and the single-type $R_0$ ([Compartmental models and $R_0$](./03-compartmental-models.md)). Perron–Frobenius and spectral radii ([Link analysis](../nets-7332/basics/02-link-analysis.md)).
- **Notation.** Shared symbols as in [the notation page](../notation.md): $\beta$ transmission rate, $\mu$ recovery rate, $\lambda = \beta/\mu$, $R_0$. In the homogeneous-mixing models on this page $\beta$ is the **per-capita** transmission rate, the $\bar\beta = \beta\langle k\rangle$ of [compartmental models](./03-compartmental-models.md), so $R_0 = \beta/\mu$; in the degree-class section it is the per-edge rate. **Page-specific symbols:**
  - $\rho(\cdot)$, with an argument, is the spectral radius. On its own, without an argument, $\rho$ keeps its shared meaning of prevalence.
  - $s(\cdot)$ is the spectral bound (largest real part of an eigenvalue).
  - $T$, $\Sigma$, $K_L$, $K$, $K_S$ and $E$ are defined below.
  - $\sigma$ is the latent-to-infectious rate, $d$ the natural death rate, $r$ the Malthusian growth rate, and $g(\tau)$ the generation-interval density.
  - DHR write $\gamma$ for recovery and $\mu$ for death. Here recovery is $\mu$ and death is $d$.

(sec-ngm-setup)=
## Setup and definitions

Throughout, the model is a system of ODEs with a **disease-free steady state** (all infected compartments empty). Only the **infected compartments** matter for invasion. Near the disease-free state, susceptibles are at their equilibrium value, and the infected compartments obey a *linear* system.

:::{prf:definition} Infected subsystem and its decomposition
:label: def-ngm-ts

Let $x \in \mathbb{R}^m$ collect the infected compartments (exposed, infectious, carrier, …). Linearising at the disease-free state gives

$$
x' = (T + \Sigma)\,x ,
$$ (eq-ngm-linear)

where:
- **$T$ (transmission)**: $T_{ij}$ is the rate at which an individual in infected state $j$ produces *newly infected* individuals in state $i$. These are "epidemiological births", and $T \ge 0$.
- **$\Sigma$ (transition)**: every other change of infected state, including progression between infected states, recovery and death. It has non-negative off-diagonal entries and spectral bound $s(\Sigma) < 0$, so $\Sigma$ is invertible and $-\Sigma^{-1} \ge 0$.

The split is a modelling choice: *what counts as a new infection*. DHR note that different admissible splits can give different numerical "reproduction numbers", all with the same threshold property.
:::

:::{prf:definition} Next-generation matrices
:label: def-ngm-k

- **Large-domain NGM**: $K_L = -T\Sigma^{-1}$, an $m\times m$ matrix.
  - $(-\Sigma^{-1})_{\ell j}$ is the expected time spent in state $\ell$ by an individual currently in state $j$.
  - So $(K_L)_{ij} = \sum_\ell T_{i\ell}(-\Sigma^{-1})_{\ell j}$ is the expected number of new cases in state $i$ caused by one individual starting in state $j$.
- **States-at-infection** are the states $i$ in which new infections can arrive, i.e. rows of $T$ with a non-zero entry. Let $E$ be the $m \times p$ matrix whose columns are the unit vectors $e_i$ of the $p$ states-at-infection, so that $EE^\top T = T$.
- **The NGM** is the $p\times p$ matrix $K = E^\top K_L E = -E^\top T \Sigma^{-1} E$, restricted to states-at-infection. Its entry $K_{ij}$ is the expected number of new cases with state-at-infection $i$ caused by one individual *newly infected* into state $j$.
- **Small-domain NGM**: if $K$ is singular, factor $T = CR$ with $C$ and $R$ spanning the columns and rows of $T$, and set $K_S = -R\Sigma^{-1}C$. This is the NGM on the **states-of-infectiousness**, the columns of $T$ with a non-zero entry.
:::

:::{prf:definition} Basic reproduction number
:label: def-ngm-r0

$$
R_0 = \rho(K) = \rho(K_L) = \rho(K_S) = \rho\big(-T\Sigma^{-1}\big).
$$ (eq-ngm-r0)

The three matrices share their non-zero eigenvalues. If $Kv = \lambda v$ with $\lambda \neq 0$, then $Ev$ is an eigenvector of $K_L$ with the same eigenvalue. $R_0$ is the asymptotic **per-generation** growth factor of the linearised process. The Perron eigenvector of $K$ gives the distribution of infecteds over states-at-infection in that regime.
:::

:::{prf:definition} Malthusian parameter
:label: def-ngm-r

The **growth rate** is $r = s(T + \Sigma)$, the dominant eigenvalue of the linear system {eq}`eq-ngm-linear`. Near the disease-free state, incidence grows as $e^{rt}$, and the doubling time is $\ln 2 / r$.
:::

**Relation to van den Driessche & Watmough.** Their widely used recipe writes the infected subsystem as $x' = \mathcal{F} - \mathcal{V}$ and sets $R_0 = \rho(FV^{-1})$, with $F$ and $V$ the Jacobians at the disease-free state. *My identification:* $F = T$ and $V = -\Sigma$, so $FV^{-1}$ is exactly DHR's large-domain $K_L$. DHR cite van den Driessche & Watmough (2002) [](doi:10.1016/S0025-5564(02)00108-6) for this decomposition and for an $M$-matrix proof of the threshold result. I have not read that paper directly. DHR's practical point is that working with $K_L$ wastes effort: $K$ or $K_S$ are smaller and have direct epidemiological meaning.

(sec-ngm-core)=
## Core ideas

### The recipe

1. List the infected states $x$.
2. Linearise at the disease-free state.
3. Decide **which flows are new infections**; those go into $T$, everything else into $\Sigma$.
4. Compute $-\Sigma^{-1}$, which holds the expected sojourn times.
5. Form $K = -E^\top T\Sigma^{-1}E$, restricted to states-at-infection. If $K$ is singular, use $K_S$ instead.
6. $R_0 = \rho(K)$. For a $2\times 2$ matrix, $R_0 = \tfrac12\big(\operatorname{tr}K + \sqrt{(\operatorname{tr}K)^2 - 4\det K}\big)$.

Each entry of $K$ can usually be **read off epidemiologically** without inverting anything. It is (probability of surviving each infected stage) × (rate of infecting while infectious) × (expected time infectious). DHR stress this: the matrix formalism checks the reasoning, and the reasoning makes the matrix meaningful.

### Why the per-type structure matters

| Structure of $K$ | $R_0$ | Example |
|---|---|---|
| $1\times 1$ | the single entry | SIR, SEIR |
| rank one, $K = c\,b^\top$ | $\operatorname{tr} K = b^\top c$ | separable mixing $\beta_{ij} = a_i b_j$; degree classes on uncorrelated networks |
| off-diagonal $\begin{pmatrix}0 & K_{12}\\ K_{21} & 0\end{pmatrix}$ | $\sqrt{K_{12}K_{21}}$ | sexually transmitted diseases between two sexes; vector–host |
| general | Perron root | age-structured or multi-population models |

**Why the square root.** With purely alternating transmission, one infected female produces $K_{21}$ infected males on average, and each of those produces $K_{12}$ infected females. Every *two* generations the female line multiplies by $K_{12}K_{21}$, so the per-generation factor is the geometric mean $\sqrt{K_{12}K_{21}}$. The eigenvalues of $K$ are $\pm\sqrt{K_{12}K_{21}}$, because the trace is zero.

The individual entries depend on the population sizes, $K_{12} \propto N_1/N_2$ and $K_{21} \propto N_2/N_1$, but the product does not. That is why DHR's $R_0$ for the two-sex model is independent of $N_1$ and $N_2$.

*My comment.* Reading "$R_0 = K_{12}$" off a single transmission route is the classic mistake here. It can be off by a large factor in either direction (see the [worked example](#sec-ngm-example)).

(sec-ngm-results)=
## Key results

:::{prf:theorem} Threshold property
:label: thm-ngm-threshold

Under the assumptions of {prf:ref}`def-ngm-ts` ($T \ge 0$ non-zero, $\Sigma$ with non-negative off-diagonal entries, $s(\Sigma) < 0$),

$$
\operatorname{sign}\, s(T + \Sigma) \;=\; \operatorname{sign}\,(R_0 - 1).
$$ (eq-ngm-sign)

So $R_0 > 1 \Leftrightarrow r > 0$ and the disease-free state is unstable, and $R_0 < 1 \Leftrightarrow r < 0$ and it is locally stable. This is DHR's Theorem A.1. They note that the original proof in Diekmann & Heesterbeek (2000) was incomplete, and they supply a full one.
:::

:::{dropdown} Proof idea
Let $\Sigma$ have non-negative off-diagonal entries with $s(\Sigma)<0$, and let $T \ge 0$.

1. **Monotonicity.** For $\theta \ge 0$, the spectral bound $s(\theta T + \Sigma)$ is non-decreasing in $\theta$, by Perron–Frobenius for matrices with non-negative off-diagonal entries.
2. **Shifting the eigenvalue.** If $s(T+\Sigma) = r$ with Perron eigenvector $w \ge 0$, then $T w = -(\Sigma - rI) w$. When $r > s(\Sigma)$ this gives $-T(\Sigma - rI)^{-1} u = u$ with $u = -(\Sigma - rI)w$.

   So $1$ is an eigenvalue of the "$r$-discounted" NGM $-T(\Sigma - rI)^{-1}$, which is non-negative. The map $r \mapsto \rho\big(-T(\Sigma - rI)^{-1}\big)$ is decreasing in $r$, because the expected sojourn times shrink when future infections are discounted by $e^{-r t}$.
3. **Comparing with $r = 0$.** At $r = 0$ that radius is $R_0$. So $R_0 > 1$ exactly when the radius hits $1$ at some $r > 0$, i.e. $s(T+\Sigma) > 0$, and $R_0 < 1$ exactly when $r<0$.

The irreducible case uses the Perron eigenvector directly. DHR handle the reducible case by approximation. Step 2 is the matrix form of the Euler–Lotka relation below.
:::

:::{prf:proposition} Growth rate and the generation interval
:label: prop-ngm-el

Let $g(\tau)$ be the generation-interval density: the time from infection of a primary case to infection of a secondary case. If incidence grows as $e^{rt}$, the Euler–Lotka equation gives

$$
\frac{1}{R_0} = \int_0^\infty e^{-r\tau} g(\tau)\, d\tau = M(-r), \qquad\text{so}\qquad R_0 = \frac{1}{M(-r)} ,
$$ (eq-ngm-el)

where $M(z) = \int_0^\infty e^{z\tau} g(\tau)\,d\tau$ is the moment generating function of $g$, assumed to exist at $-r$ (Wallinga & Lipsitch 2007). Special cases from Wallinga & Lipsitch:

| Generation interval | $R_0$ in terms of $r$ |
|---|---|
| exponential with rate $\mu$ (SIR) | $1 + r/\mu$ |
| latent period exponential with rate $\sigma$, then infectious period exponential with rate $\mu$ (SEIR) | $(1 + r/\sigma)(1 + r/\mu)$ |
| fixed, $g = \delta(\tau - T_c)$ | $e^{rT_c}$ |
| normal with mean $T_c$ and standard deviation $s_g$ | $\exp\!\big(rT_c - \tfrac12 r^2 s_g^2\big)$ |

For growing epidemics, the fixed-interval case is an **upper bound**: $1 < R_0 \le e^{rT_c}$ for any $g$ with mean $T_c$ (Jensen's inequality).
:::

:::{dropdown} Derivation
With constant $R_0$, a renewal equation gives the incidence: $i(t) = R_0 \int_0^\infty i(t-\tau)\, g(\tau)\, d\tau$. Substituting $i(t) = i_0 e^{rt}$ and cancelling $e^{rt}$ gives {eq}`eq-ngm-el`.

**SEIR.** The generation interval is a latent time $\sim \mathrm{Exp}(\sigma)$ plus the time to transmission within the infectious period, which is also $\sim\mathrm{Exp}(\mu)$ for constant infectiousness. So $M(-r) = \frac{\sigma}{\sigma + r}\cdot\frac{\mu}{\mu+r}$. Inverting gives $(1+r/\sigma)(1+r/\mu)$.

**Consistency with the matrix view** (my check). For SEIR without demography, $s(T+\Sigma)$ is the positive root of $(z+\sigma)(z+\mu) = \sigma\beta$. Dividing by $\sigma\mu$ gives $(1+z/\sigma)(1+z/\mu) = \beta/\mu = R_0$, the same relation.
:::

:::{prf:proposition} Degree-class NGM on uncorrelated networks (my derivation)
:label: prop-ngm-degree

Take degree classes $k$ with distribution $P(k)$, no degree correlations, per-edge transmission rate $\beta$ and recovery rate $\mu$. Let $x_k$ be the *number* of infected nodes in class $k$, linearised around the disease-free state. A newly infected node lands in class $k$ with the edge-biased probability $kP(k)/\langle k\rangle$. Then

$$
T_{kk'} = \beta\,\frac{kP(k)}{\langle k\rangle}\, m_{k'}, \qquad \Sigma = -\mu I, \qquad
K = \frac{\beta}{\mu}\,\frac{kP(k)}{\langle k\rangle}\, m_{k'} ,
$$ (eq-ngm-degree)

where $m_{k'}$ is the number of edges an infected node of degree $k'$ can transmit along:
- **SIS** (individual-level linearisation): $m_{k'} = k'$.
- **SIR**: $m_{k'} = k' - 1$, because the edge it was infected through leads to a node that is not susceptible.

$K$ has **rank one**, so $R_0 = \operatorname{tr} K$:

$$
R_0^{\mathrm{SIS}} = \lambda\,\frac{\langle k^2\rangle}{\langle k\rangle}, \qquad
R_0^{\mathrm{SIR}} = \lambda\,\frac{\langle k^2\rangle - \langle k\rangle}{\langle k\rangle}.
$$ (eq-ngm-degree-r0)

Setting $R_0 = 1$ recovers the heterogeneous mean-field thresholds $\lambda_c = \langle k\rangle/\langle k^2\rangle$ (SIS) and $\lambda_c = \langle k\rangle/(\langle k^2\rangle - \langle k\rangle)$ (SIR) in the RMP review. The SIR growth rate $s(T+\Sigma) = \beta(\langle k^2\rangle - \langle k\rangle)/\langle k\rangle - \mu$ matches the RMP's initial-growth time scale (their eq. 57).
:::

:::{dropdown} Why rank one, and what it means
Whatever its degree, an infected node sends new infections into degree classes in the same proportions $kP(k)/\langle k\rangle$. So every column of $K$ is a multiple of one vector. The Perron vector is $c_k \propto kP(k)$: early in an outbreak, infected nodes are distributed by **edge-biased** degree, which is why hubs are infected first.

$\operatorname{tr}K = \sum_k \frac{\beta}{\mu}\frac{kP(k)}{\langle k\rangle} m_k$ is the mean number of onward transmissions from a node reached by following a random edge. It diverges with $\langle k^2\rangle$ in scale-free networks with $\gamma \le 3$, so $\lambda_c \to 0$. That is the vanishing threshold derived dynamically in [heterogeneous mean-field epidemics](./05-heterogeneous-mean-field.md).
:::

(sec-ngm-example)=
## Worked example

All numbers below were computed in Python. The matrices were built explicitly, and $R_0$ was taken as a numerical spectral radius.

**1. SEIR without demography**, with $\beta = 0.6$, $\sigma = 0.25$, $\mu = 0.2$ per day. The infected states are $(E, I)$:

$$
T = \begin{pmatrix} 0 & 0.6 \\ 0 & 0\end{pmatrix},\quad
\Sigma = \begin{pmatrix} -0.25 & 0 \\ 0.25 & -0.2\end{pmatrix},\quad
K_L = -T\Sigma^{-1} = \begin{pmatrix} 3 & 3 \\ 0 & 0\end{pmatrix},\quad K = (3).
$$

- $R_0 = 3 = \beta/\mu$, independent of $\sigma$. With a natural death rate $d = 0.01$, $R_0 = \beta\sigma/\big((\sigma+d)(\mu+d)\big) = 2.747$.
- The growth rate is $r = s(T+\Sigma) = 0.1631$ per day, a doubling time of $4.25$ days. Euler–Lotka checks out: $(1 + r/\sigma)(1+r/\mu) = 3.000$.
- Simulating the nonlinear SEIR model with $N = 10^6$ and one initial case, then fitting $\log I$ over days 20–35, gives $r = 0.1631$.
- **An SIR model with the same $R_0 = 3$ grows at $r = \beta - \mu = 0.4$**, a doubling time of $1.73$ days. The latent period reduced the growth rate by a factor of about $2.5$ and left $R_0$ unchanged.

**2. Two sexes** (the structure of DHR §4.1). The infected states are $(E_1, I_1, E_2, I_2)$, with parameters $\beta_1 = 0.8$, $\beta_2 = 0.5$, $\nu_1 = \nu_2 = 0.5$, $\gamma_1 = 0.25$, $\gamma_2 = 0.2$ and death rate $d = 0.01$.

| $N_1/N_2$ | $K_{12}$ | $K_{21}$ | eigenvalues of $K$ | $R_0$ |
|---|---|---|---|---|
| 1 | 3.735 | 1.885 | $\pm 2.654$ | 2.654 |
| 2 | 7.470 | 0.943 | $\pm 2.654$ | 2.654 |

The single-route numbers range from 0.94 to 7.5 as the sex ratio changes. $R_0 = \sqrt{K_{12}K_{21}} = \sqrt{7.04}$ is the same in both rows, and matches DHR's closed form

$$
R_0=\sqrt{\frac{\beta_1\beta_2\,\nu_1\nu_2}{(\nu_1+d)(\nu_2+d)(\gamma_1+d)(\gamma_2+d)}} .
$$

The growth rate $s(T+\Sigma) = 0.207 > 0$ is the same in both rows too.

**3. Singular $K$** (DHR §2.1: one infectious class fed by two latent classes). New infections enter $E_1$ with probability $p$ and $E_2$ with probability $1-p$. With $p = 0.3$, $\nu_1 = 1$, $\nu_2 = 0.1$, $\gamma = 0.2$, $d = 0.02$ and $\beta = 0.5$, the $2\times2$ NGM has $\det K \approx 0$. So $R_0 = \operatorname{tr} K = 1.994$, equal to the scalar $K_S$:

$$
R_0 = \frac{\beta}{\gamma+d}\Big[\frac{p\nu_1}{\nu_1+d} + \frac{(1-p)\nu_2}{\nu_2+d}\Big].
$$

**4. Degree classes**, with $P(k) = (0.4, 0.3, 0.2, 0.1)$ on $k = (1, 2, 3, 10)$. This gives $\langle k\rangle = 2.6$ and $\langle k^2\rangle = 13.4$. Take $\beta = 0.1$ and $\mu = 0.5$, so $\lambda = 0.2$.

| Model | $\lambda_c$ | $R_0 = \rho(K)$ | rank of $K$ | $r = s(T+\Sigma)$ |
|---|---|---|---|---|
| SIS ($m_k = k$) | $0.194$ | $1.031$ | 1 | $+0.015$ |
| SIR ($m_k = k-1$) | $0.241$ | $0.831$ | 1 | $-0.085$ |

At this $\lambda$, SIS invades but SIR does not. The difference is entirely the excluded "parent" edge, which matters when most nodes have small degree.

## Assumptions and limitations

- **This is linear theory at the disease-free state.** $R_0$ says whether an invasion *can* start in a large, fully susceptible population. It says nothing directly about final size, peak or endemic level, which need the nonlinear model. It also says nothing about stochastic extinction early on: even with $R_0 > 1$, a single introduction can die out.
- **The split into $T$ and $\Sigma$ is a modelling decision.** Different "new infection" conventions can change the number called $R_0$ while keeping the threshold at 1 (DHR's footnote). Report how $T$ was chosen.
- **$R_0$ and $r$ agree only in sign.** DHR stress that no general formula links them. The Euler–Lotka relation needs the generation-interval *shape*, and Wallinga & Lipsitch show that the inferred $R_0$ can change substantially with it at fixed $r$.
- **Time-homogeneous parameters and an exponential phase are assumed.** With time-varying contact rates, interventions or depletion of susceptibles, $R_t$ needs renewal-equation estimators rather than $1/M(-r)$.
- **Network caveats** (my comment). The degree-class NGM is the annealed / heterogeneous mean-field picture. On quenched networks the SIS threshold is governed by $1/\Lambda_{\max}$, and hubs can sustain localized activity, so the rank-one NGM can be qualitatively wrong. See [quenched mean-field](./06-quenched-mean-field.md). For SIR, the exact tree-like result is the percolation threshold $T_c = \langle k\rangle/(\langle k^2\rangle - \langle k\rangle)$ in *transmissibility*, not in $\lambda$. See [SIR and percolation](./07-sir-percolation.md).

## Connections

- **PHYS 7335.**
  - [Compartmental models](./03-compartmental-models.md) give the $1\times1$ case.
  - [Heterogeneous mean-field](./05-heterogeneous-mean-field.md) thresholds are the rank-one degree-class NGM above.
  - [Quenched mean-field](./06-quenched-mean-field.md) replaces $K$ by $\lambda A$ (SIS) or a non-backtracking operator (SIR). The spectral-radius logic is the same, but the operator is node-level.
  - [Metapopulation models](./09-metapopulation-models.md) apply the same logic one level up. Subpopulations are the "individuals", and the global invasion threshold $R_*$ is a reproduction number for subpopulations.
  - [ABC inference](./10-abc-inference.md) is how $\beta$, $\sigma$ and $\mu$ get estimated in practice.
- **NETS 5116.** Barabási's spreading chapter derives $\lambda_c = \langle k\rangle/\langle k^2\rangle$ dynamically ([Barabási ch. 10 notes](../nets-5116/barabasi/10-spreading-phenomena.md)). Here it appears as $\rho(K) = 1$.
- **NETS 7332.** $R_0$ is a Perron root, and the Perron eigenvector of $K$ is the "who gets infected" analogue of PageRank's stationary vector ([Link analysis](../nets-7332/basics/02-link-analysis.md)). *My comment:* both are leading eigenvectors of a non-negative operator that redistributes mass along edges.

## Self-test

:::{dropdown} Q1. Define $T$, $\Sigma$, $K_L$ and $K$. What does $(-\Sigma^{-1})_{ij}$ mean?
- $T$ holds rates of new infections, from state $j$ into state $i$.
- $\Sigma$ holds all other flows (progression, recovery, death), with $s(\Sigma) < 0$.
- $K_L = -T\Sigma^{-1}$, and $K = E^\top K_L E$ is its restriction to states-at-infection.
- $(-\Sigma^{-1})_{ij}$ is the expected time an individual currently in state $j$ will spend in state $i$ before leaving the infected states.
:::

:::{dropdown} Q2. Why is $R_0$ for SEIR without demography equal to $\beta/\mu$, independent of $\sigma$? What does $\sigma$ change?
Without death, everyone in $E$ eventually becomes infectious, with probability $\sigma/(\sigma + 0) = 1$, and then infects at rate $\beta$ for an expected time $1/\mu$. So $R_0 = \beta/\mu$. The latency $\sigma$ changes the **timing**: the generation interval lengthens, so $r$ falls, via $R_0 = (1+r/\sigma)(1+r/\mu)$. With death rate $d$, latency also lowers $R_0$ through the survival factor $\sigma/(\sigma+d)$.
:::

:::{dropdown} Q3. In a two-sex model, $K_{12} = 6$ and $K_{21} = 0.5$. What is $R_0$? Will an epidemic invade?
$R_0 = \sqrt{6\times 0.5} = \sqrt 3 \approx 1.73 > 1$, so yes. The female line multiplies by $3$ every two generations. Reading off $K_{21} = 0.5$ alone would wrongly suggest extinction, and $K_{12} = 6$ alone would overstate the per-generation growth.
:::

:::{dropdown} Q4. State the threshold theorem. Does $R_0 = 2$ in one disease and $R_0 = 4$ in another imply that the second grows faster?
$\operatorname{sign}\, s(T+\Sigma) = \operatorname{sign}(R_0 - 1)$. No: $r$ depends on the generation interval as well. A disease with $R_0 = 4$ and a long generation interval can grow more slowly than one with $R_0 = 2$ and a short interval. For fixed intervals, $r = \ln R_0 / T_c$.
:::

:::{dropdown} Q5. Show that the degree-class NGM for SIS on an uncorrelated network gives $\lambda_c = \langle k\rangle/\langle k^2\rangle$. Why does SIR give $\langle k\rangle/(\langle k^2\rangle - \langle k\rangle)$?
- $K_{kk'} = \lambda\, \frac{kP(k)}{\langle k\rangle}\, k'$ has rank one, so $R_0 = \operatorname{tr} K = \lambda\sum_k k^2 P(k)/\langle k\rangle = \lambda\langle k^2\rangle/\langle k\rangle$. Setting this to 1 gives the SIS threshold.
- In SIR, an infected node of degree $k'$ cannot reinfect its infector, so only $k'-1$ edges carry onward transmission. This replaces $k^2$ by $k(k-1)$.
:::

:::{dropdown} Q6. Given an observed early doubling time of 3 days and an SIR-type exponential generation interval with mean 5 days, estimate $R_0$. What is the upper bound for any interval with the same mean?
- $r = \ln 2/3 \approx 0.231$ per day, and $\mu = 1/5$. So $R_0 = 1 + r/\mu = 1 + 0.231\times 5 \approx 2.16$.
- The fixed-interval bound is $e^{rT_c} = e^{1.155} \approx 3.17$.
:::

:::{dropdown} Q7. When is $K$ singular, and what do you do?
$K$ is singular when $T$ has low rank, i.e. all new infections are produced by fewer states-of-infectiousness than there are states-at-infection. Examples are one infectious class feeding several latent classes, or separable mixing $\beta_{ij} = a_i b_j$. Then $R_0 = \operatorname{tr}K$ for rank one. In general, use the small-domain $K_S = -R\Sigma^{-1}C$ from $T = CR$, whose dimension is the number of states-of-infectiousness.
:::

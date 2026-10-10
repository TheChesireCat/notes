---
title: Approximate Bayesian Computation for Epidemic Models
short_title: ABC inference
subject: PHYS 7335 · Topic
description: Likelihood-free Bayesian calibration of stochastic epidemic simulators by rejection, MCMC and sequential Monte Carlo ABC, and what the data can and cannot identify.
tags: [inference, abc, smc, bayesian, calibration, identifiability, sir]
---

:::{tip} TL;DR
- **ABC replaces the likelihood with simulation.** Draw $\theta$, simulate a dataset $x^*$, and keep $\theta$ if $d\big(s(x^*), s(x_0)\big) \le \varepsilon$. The accepted draws sample $\pi\big(\theta \mid d(s(X), s(x_0)) \le \varepsilon\big)$. This is the right tool when a stochastic epidemic simulator is easy to *run* but its likelihood for partially observed data is intractable.
- **There are two separate approximations.** The **tolerance** $\varepsilon > 0$ blurs the posterior. The **summaries** $s$ change its target to $\pi(\theta \mid s(x_0))$ even as $\varepsilon \to 0$. The two coincide with the true posterior only if $s$ is **sufficient**. The acceptance rate falls roughly like $\varepsilon^{n_s}$ in the summary dimension $n_s$, so a few informative summaries beat many.
- **ABC-SMC** (Toni et al. 2009) moves a population of $N$ particles through decreasing tolerances $\varepsilon_1 > \dots > \varepsilon_T$. At each stage it resamples, perturbs with a kernel $K_t$, and reweights by $w_t^{(i)} \propto \pi(\theta_t^{(i)}) \big/ \sum_j w_{t-1}^{(j)} K_t(\theta_t^{(i)} \mid \theta_{t-1}^{(j)})$. In the worked example it needs about 5× fewer simulations than rejection to reach the same $\varepsilon$.
- **Model choice by ABC is fragile.** With insufficient summaries, the ABC Bayes factor converges to the Bayes factor *of the summaries*. That can be unrelated to the true one, even when the summary is sufficient within each model (Robert et al. 2011).
- **Incidence data identify combinations, not rates.** Early exponential growth pins $r = \beta - \mu$ (SIR), not $R_0 = \beta/\mu$. Once an epidemic saturates, the final size barely moves for $R_0 \gtrsim 3$. Posteriors on $(\beta, \mu)$ therefore form a **ridge**, which collapses only if the infectious period is known independently.
:::

- **Source.**
  - [](doi:10.1098/rsif.2008.0172) (Toni, Welch, Strelkowa, Ipsen & Stumpf, *J. R. Soc. Interface* 6, 187–202, 2009; preprint [arXiv:0901.1925](https://arxiv.org/abs/0901.1925)): rejection, MCMC and SMC ABC, and SIR model selection.
  - [](doi:10.1073/pnas.0306899100) (Marjoram et al. 2003): ABC-MCMC.
  - [](doi:10.1093/genetics/162.4.2025) (Beaumont, Zhang & Balding 2002): regression adjustment. I read the abstract only.
  - [](doi:10.1073/pnas.1102900108) (Robert, Cornuet, Marin & Pillai 2011): ABC model choice.
  - The course lists ABC among its topics ([PHYS 7335 site](https://mobs-lab.github.io/phys7335/)).
- **Builds on.** The stochastic SIR model used as the simulator ([Compartmental models](./03-compartmental-models.md)) and the link between growth rate and $R_0$ ([Thresholds and next-generation matrices](./04-thresholds-and-ngm.md)).
- **Notation.** Shared symbols as in [](#notation): $\beta$ is the transmission rate, $\mu$ the recovery rate, $R_0 = \beta/\mu$ for homogeneous SIR. Here the model is homogeneously mixed and $\beta$ is the **per-capita** transmission rate (force of infection $\beta I/N$), the $\bar\beta = \beta\langle k\rangle$ of [compartmental models](./03-compartmental-models.md).
  - Page-specific: $\theta$ parameters, $\pi(\theta)$ prior, $f(x \mid \theta)$ the simulator's (intractable) likelihood, $x_0$ the observed data, $s(\cdot)$ the summary statistics with dimension $n_s$, $\varepsilon$ the tolerance, $K_t$ the perturbation kernel, $w$ the importance weights.
  - The distance is written $d(\cdot,\cdot)$, not $\rho$, because $\rho$ is prevalence on these pages.

(sec-abc-setup)=
## Setup and definitions

The target is the Bayesian posterior $\pi(\theta \mid x_0) \propto f(x_0 \mid \theta)\,\pi(\theta)$. ABC applies when $f$ can be **sampled** (run the simulator) but not **evaluated**.

:::{prf:definition} Likelihood-free setting
:label: def-abc-likelihood-free

A model is *likelihood-free* if, for any $\theta$, we can draw $X \sim f(\cdot \mid \theta)$, but $f(x_0 \mid \theta)$ cannot be computed in reasonable time.

*My example.* For a stochastic epidemic observed as daily case counts, $f(x_0 \mid \theta)$ is a sum over every unobserved infection and recovery time consistent with the counts. On a contact network or a metapopulation it is also a sum over the hidden state of every node. Simulation remains cheap.
:::

:::{prf:definition} ABC posterior
:label: def-abc-posterior

For summaries $s$, a distance $d$ and a tolerance $\varepsilon \ge 0$, the **ABC posterior** is

$$
\pi_\varepsilon(\theta \mid x_0) \;\propto\; \pi(\theta)\; \Pr_{X \sim f(\cdot\mid\theta)}\!\Big[ d\big(s(X), s(x_0)\big) \le \varepsilon \Big],
$$ (eq-abc-posterior)

i.e. the distribution $\pi\big(\theta \mid d(s(x^*), s(x_0)) \le \varepsilon\big)$ that Toni et al. state as the output of every ABC algorithm. Toni et al. compare the full time series directly ($s$ = identity) because their data are values of a dynamical process at fixed time points.
:::

:::{prf:definition} Sufficient statistic
:label: def-abc-sufficient

$s$ is **sufficient** for $\theta$ if $\pi(\theta \mid x) = \pi(\theta \mid s(x))$ for every prior, equivalently $f(x \mid \theta) = g(s(x), \theta)\, h(x)$. Outside exponential families, fixed-dimension sufficient statistics generally do not exist (Robert et al. 2011). Epidemic models are not exponential families, so in practice $s$ is always insufficient.
:::

(sec-abc-core)=
## Core ideas

### Rejection ABC

:::{prf:algorithm} Rejection ABC
:label: alg-abc-rejection

1. Sample $\theta^* \sim \pi(\theta)$.
2. Simulate $x^* \sim f(x \mid \theta^*)$.
3. If $d\big(s(x^*), s(x_0)\big) \le \varepsilon$, accept $\theta^*$; otherwise reject.
4. Repeat until $N$ values are accepted.
:::

Toni et al. and Robert et al. attribute this sampler to Pritchard et al. (1999), with the idea going back to Tavaré et al. (1997). In practice $\varepsilon$ is often set as a **quantile** of the simulated distances: run $M$ simulations and keep the closest fraction $q$. The output is then always $qM$ draws, but $\varepsilon$ depends on the data.

**Acceptance is low when prior and posterior differ.** This is the problem MCMC and SMC address.

### Two approximation layers

1. **Tolerance.** $\pi_\varepsilon$ is the posterior convolved with the acceptance region. Larger $\varepsilon$ means a wider posterior that drifts towards the prior, and in the limit $\varepsilon \to \infty$ it *is* the prior.
2. **Summaries.** As $\varepsilon \to 0$, $\pi_\varepsilon(\theta \mid x_0) \to \pi(\theta \mid s(x_0))$ ([](#prop-abc-limit)). This equals $\pi(\theta \mid x_0)$ only for sufficient $s$. With insufficient $s$, no amount of computation fixes the target. Good summaries are those whose distribution changes most with $\theta$ where the posterior mass is.

**Curse of dimensionality.** For an $n_s$-dimensional summary with locally smooth density, the probability of landing in an $\varepsilon$-ball scales like $\varepsilon^{n_s}$ ([](#prop-abc-dimension)). Adding weakly informative summaries buys little information and costs exponentially in acceptance.

**Regression adjustment** (Beaumont, Zhang & Balding 2002). Fit a *local-linear regression* of simulated parameters on simulated summaries, then substitute the observed summaries into the regression equation. This partially corrects the error from $\varepsilon > 0$ and allows a larger tolerance. *My summary of the usual form:* replace each accepted $\theta_i$ by

$$
\theta_i^{\mathrm{adj}} = \theta_i - \hat b^\top\big(s(x_i) - s(x_0)\big),
$$

with $\hat b$ from a kernel-weighted least-squares fit near $s(x_0)$. I have checked only the abstract for this method.

### ABC-MCMC

:::{prf:algorithm} ABC-MCMC (Marjoram et al. 2003, as stated by Toni et al.)
:label: alg-abc-mcmc

1. Initialise $\theta_0$; set $i = 0$.
2. Propose $\theta^* \sim q(\theta \mid \theta_i)$.
3. Simulate $x^* \sim f(x \mid \theta^*)$.
4. If $d(x_0, x^*) > \varepsilon$, set $\theta_{i+1} = \theta_i$. Otherwise set $\theta_{i+1} = \theta^*$ with probability
   $\alpha = \min\!\Big(1, \dfrac{\pi(\theta^*)\, q(\theta_i \mid \theta^*)}{\pi(\theta_i)\, q(\theta^* \mid \theta_i)}\Big)$, else $\theta_{i+1} = \theta_i$.
5. $i \leftarrow i+1$; go to 2.
:::

The chain has stationary distribution $\pi_\varepsilon$ {eq}`eq-abc-posterior`. With a symmetric proposal, $\alpha$ depends only on the prior, and with a uniform prior $\alpha = 1$. The likelihood ratio of ordinary Metropolis–Hastings is replaced by the binary event "simulation lands within $\varepsilon$". The drawbacks Toni et al. note are correlated samples and long sticking times in low-probability regions.

### ABC-SMC

:::{prf:algorithm} ABC-SMC (Toni et al. 2009)
:label: alg-abc-smc

1. Choose tolerances $\varepsilon_1 > \varepsilon_2 > \dots > \varepsilon_T \ge 0$; set $t = 1$.
2. For $i = 1, \dots, N$:
   - If $t = 1$, draw $\theta^{**} \sim \pi(\theta)$. Otherwise draw $\theta^*$ from the previous population $\{\theta_{t-1}^{(j)}\}$ with probabilities $w_{t-1}^{(j)}$, and perturb: $\theta^{**} \sim K_t(\cdot \mid \theta^*)$. If $\pi(\theta^{**}) = 0$, redraw.
   - Simulate $x^* \sim f(x \mid \theta^{**})$. If $d(x^*, x_0) > \varepsilon_t$, redraw.
   - Set $\theta_t^{(i)} = \theta^{**}$ with weight $w_t^{(i)}$ from {eq}`eq-abc-weights`.
3. Normalise the weights. If $t < T$, set $t \leftarrow t + 1$ and go to 2.
:::

The weights are

$$
w_t^{(i)} = \begin{cases} 1, & t = 1,\\[4pt] \dfrac{\pi(\theta_t^{(i)})}{\sum_{j=1}^N w_{t-1}^{(j)}\, K_t\big(\theta_t^{(i)} \mid \theta_{t-1}^{(j)}\big)}, & t > 1. \end{cases}
$$ (eq-abc-weights)

With $T = 1$ this is rejection ABC. Toni et al. use uniform or Gaussian random-walk kernels. For stochastic models, their Appendix A generalises the scheme by simulating $B_t$ datasets per particle. The intermediate populations show which parameters the data constrain as $\varepsilon_t$ shrinks, so they double as a sensitivity analysis.

### Model selection with ABC

Toni et al. add a model index $m$ to the particles and read off $P(m \mid x_0)$ from the final population. They report two results:

- **Simulated SIR variants.** They compare four models: SIR with births and deaths, SIR with a time delay, SEIR-like with a latent class, and SIRS with waning immunity, on 12 noisy time points of $(S, I, R)$. With noise $\sigma = 1$ no single model wins. With $\sigma = 0.2$ most posterior weight falls on the true model.
- **Tristan da Cunha common cold, October 1967.** The data are 21 days of $I(t)$ and $R(t)$, with $S(0)$ unknown. They used 15 tolerances from 100 down to 13.8 and 1000 particles. The latent-class model came out "only marginally better" than the plain and delayed SIR models, so they suggest model averaging. The inferred $S(0)$ is far below the island's population of about 300. This suggests either prior immunity or that homogeneous mixing is wrong, which is a reminder that ABC calibrates the model you give it.

:::{warning} The Robert et al. (2011) caveat
The ABC estimate of a Bayes factor $B_{12}$ converges to $B_{12}^{\eta}$, the Bayes factor for the *summary* $\eta(y)$. Unless $\eta$ is sufficient **jointly across models**, $B_{12}^\eta$ need not track $B_{12}$. More computation does not help. Their example is Poisson vs geometric data with $\eta = \sum_i y_i$. That statistic is sufficient *within* each model, yet $B_{12}^\eta$ is unrelated to the true Bayes factor. They recommend treating ABC model choice as exploratory, backed by simulation checks of its performance. They also note that schemes whose distance uses the **whole dataset**, with no reduction to summaries, avoid this divergence. They name Toni et al.'s ABC-SysBio as an example. Toni et al.'s SIR model selection compares full time series, so it falls on the safe side of this caveat, though $\varepsilon > 0$ still approximates.
:::

### Practical choices for epidemic curves

- **Distance.** Use a Euclidean distance on the full incidence curve, or on standardised summaries. Summaries should be scaled, e.g. by their prior-predictive median absolute deviation (MAD), so that no single one dominates.
- **Summaries.**
  - Peak time and peak height carry the growth and depletion dynamics.
  - Final size carries $R_0$ through the final-size relation, but only while the epidemic is not saturated.
  - The early growth rate carries $r$.
- **Stochastic fade-out.** Many prior draws with $R_0 > 1$ still go extinct early. They produce tiny outbreaks that are automatically rejected, which is a useful sanity check on the simulator's minor-outbreak probability.
- **Observation model.** Reporting rate and delays belong *inside* the simulator. ABC then handles them at no extra conceptual cost.

(sec-abc-results)=
## Key results

:::{prf:proposition} Zero-tolerance limit
:label: prop-abc-limit

If $s(X)$ has a density $f_s(\cdot \mid \theta)$ continuous at $s(x_0)$, and $d$ is a norm, then as $\varepsilon \to 0$

$$
\pi_\varepsilon(\theta \mid x_0) \;\longrightarrow\; \pi\big(\theta \mid s(x_0)\big) \propto \pi(\theta)\, f_s\big(s(x_0) \mid \theta\big).
$$

If $s$ is sufficient, the limit is the exact posterior $\pi(\theta \mid x_0)$.
:::

:::{dropdown} Derivation sketch (mine; standard)
$\Pr[d(s(X), s(x_0)) \le \varepsilon] = \int_{B_\varepsilon(s(x_0))} f_s(u \mid \theta)\,du = \lvert B_\varepsilon \rvert \big(f_s(s(x_0) \mid \theta) + o(1)\big)$. The volume $\lvert B_\varepsilon \rvert$ does not depend on $\theta$, so it cancels on normalising {eq}`eq-abc-posterior`. Sufficiency gives $f(x \mid \theta) = g(s(x), \theta) h(x)$, so $\pi(\theta \mid x_0) \propto \pi(\theta) g(s(x_0), \theta) \propto \pi(\theta \mid s(x_0))$.
:::

:::{prf:proposition} Acceptance rate and summary dimension
:label: prop-abc-dimension

Under the conditions above, the acceptance probability of rejection ABC is

$$
\Pr(\text{accept}) = \int \pi(\theta) \Pr\big[d(s(X), s(x_0)) \le \varepsilon \mid \theta\big] d\theta \;\approx\; c_{n_s}\, \varepsilon^{n_s}\, m_s\big(s(x_0)\big),
$$

where $m_s$ is the prior-predictive density of $s$ and $c_{n_s}$ is the volume of the unit ball in $\mathbb{R}^{n_s}$. Halving $\varepsilon$ costs a factor $2^{n_s}$ in simulations.
:::

:::{dropdown} Derivation sketch (mine)
Integrate the expansion in the previous dropdown against $\pi(\theta)$. $\int \pi(\theta) f_s(u \mid \theta)\,d\theta = m_s(u)$, and $\lvert B_\varepsilon \rvert = c_{n_s}\varepsilon^{n_s}$.
:::

:::{prf:proposition} Why the ABC-SMC weights are correct
:label: prop-abc-smc-weights

At stage $t > 1$, a particle is proposed from the mixture $q_t(\theta) = \sum_j w_{t-1}^{(j)} K_t(\theta \mid \theta_{t-1}^{(j)})$ and kept only if its simulation falls within $\varepsilon_t$. Importance-weighting the kept particles by $\pi(\theta)/q_t(\theta)$, which is {eq}`eq-abc-weights`, gives a weighted sample from $\pi_{\varepsilon_t}$.
:::

:::{dropdown} Derivation sketch (my reading; Toni et al. derive it from sequential importance sampling in their Appendix A)
The density of a kept particle is proportional to $q_t(\theta) \Pr[d \le \varepsilon_t \mid \theta]$. The target {eq}`eq-abc-posterior` is $\propto \pi(\theta)\Pr[d \le \varepsilon_t \mid \theta]$. Their ratio is $\pi(\theta)/q_t(\theta)$, and the intractable acceptance probability cancels. That cancellation is why the weights need only the prior and the kernel. The usual caveat is that the support of $q_t$ must cover that of the target, which is why particles outside the prior are redrawn.
:::

:::{prf:proposition} What early incidence identifies (SIR)
:label: prop-abc-ridge

In the deterministic SIR model with $S \approx N$ early on, $\dot I = (\beta - \mu) I$, so incidence grows as $e^{rt}$ with $r = \beta - \mu$. Early data therefore constrain $r$ and leave a one-dimensional ridge $\{\beta - \mu = r\}$ along which $R_0 = \beta/\mu = 1 + r/\mu$ varies freely. Fixing the mean infectious period $1/\mu$ breaks the ridge.
:::

:::{dropdown} Derivation sketch
Linearise $\dot I = \beta S I/N - \mu I$ at $S = N$. Each point on the ridge produces the same early trajectory, so up to stochastic noise it has the same likelihood. The relation $R_0 = 1 + r/\mu$ is the Euler–Lotka relation for an exponentially distributed infectious period (see [Thresholds and next-generation matrices](./04-thresholds-and-ngm.md)). Later dynamics, through peak timing and depletion, add information, but the final size saturates: $z_\infty = 1 - e^{-R_0 z_\infty}$ gives $z_\infty = 0.797, 0.940, 0.993, 1.000$ for $R_0 = 2, 3, 5, 10$. So for a large outbreak, $R_0 \gtrsim 3$ is weakly identified even from the full curve.
:::

## Worked example

All numbers below are from a Python script with seed 7335.

**Simulator.** A chain-binomial SIR approximating the continuous-time model:
- $N = 500$, $I(0) = 5$, time step $\Delta t = 0.1$ day.
- Per step, each susceptible is infected with probability $1 - e^{-\beta I \Delta t/N}$, and each infected recovers with probability $1 - e^{-\mu \Delta t}$.
- The data are daily incidence for 60 days.

**"Observed" outbreak.** Generated with $\beta = 0.30$, $\mu = 0.10$ ($R_0 = 3$, $r = 0.20$):
- Final size 474 of 500.
- Peak on day 19, with 29 new cases.
- First 15 days: 0, 1, 2, 5, 2, 7, 5, 10, 10, 10, 8, 14, 11, 22, 15.

**Priors.** $\beta \sim U(0.05, 1)$ and $\mu \sim U(0.02, 0.5)$. In the prior predictive, 72.7% of runs infect more than 10% of the population.

**Rejection ABC.** $M = 200{,}000$ prior simulations, keeping the closest 0.2% (about 400 draws). Three distances were tried: Euclidean on the full curve; Euclidean on four MAD-scaled summaries (peak day, peak height, final size, slope of $\log(1+\text{incidence})$ over days 0–9); and Euclidean on the first 10 days only.

| Data used | $\varepsilon$ | $\beta$ (95%) | $\mu$ (95%) | $\beta-\mu$ (95%) | $R_0$ (95%) | corr$(\beta,\mu)$ |
|---|---|---|---|---|---|---|
| full curve | 28.34 | 0.222–0.542 | 0.024–0.279 | **0.175–0.294** | 1.93–10.4 | 0.94 |
| 4 summaries | 0.50 | 0.238–0.537 | 0.024–0.206 | 0.182–0.343 | 2.37–11.2 | 0.84 |
| first 10 days | 5.83 | 0.241–0.734 | 0.026–0.476 | 0.075–0.380 | 1.17–11.1 | 0.83 |
| full curve, $\mu = 0.1$ known (50,000 sims, keep 1%) | — | **0.272–0.390** | fixed | — | — | — |

What the table shows:

- **The ridge.** $\beta$ and $\mu$ are strongly correlated (0.83–0.94). The combination $\beta - \mu$ is constrained far better than $R_0$, whose interval spans a factor of about 5 even with the full curve. Fixing $\mu$ narrows $\beta$ to 0.27–0.39.
- **Early data are weaker.** Ten days constrain $r$ only loosely and leave both rates almost prior-wide.
- **Summaries vs full curve.** Here the four summaries give a similar posterior to the full curve. They shift it towards larger $\beta - \mu$, because the observed early slope (0.248) is above the deterministic 0.20.
- **Not a bias.** The posteriors centre on $\beta - \mu \approx 0.23$ rather than 0.20 because this realisation grew faster than average. ABC conditions on *this* outbreak, not on the true parameters.

**ABC-SMC** on the full-curve distance, with $N = 1000$ particles. The tolerances were set at the 20%, 5%, 2%, 0.8% and 0.2% quantiles of the prior-predictive distances. The kernel $K_t$ was Gaussian with covariance twice the weighted particle covariance; that is my choice, whereas Toni et al. used uniform random-walk kernels.

| $t$ | $\varepsilon_t$ | simulations | acceptance | effective sample size |
|---|---|---|---|---|
| 1 | 70.8 | 5,130 | 0.195 | 1000 |
| 2 | 43.8 | 7,804 | 0.128 | 954 |
| 3 | 36.1 | 11,117 | 0.090 | 906 |
| 4 | 32.0 | 17,839 | 0.056 | 896 |
| 5 | 28.3 | 53,891 | 0.019 | 935 |

That is 95,781 simulations in total. Rejection at the same final $\varepsilon$ (acceptance 0.002) would need about 500,000 for 1000 draws, so SMC is about 5× cheaper. The final weighted posterior agrees with rejection: $\beta$ 0.223–0.542, $\mu$ 0.025–0.262, $\beta - \mu$ 0.175–0.309, $R_0$ 1.95–9.72, correlation 0.93. The effective sample size, $1/\sum_i w_i^2$, stays above 890.

## Assumptions and limitations

- **$\varepsilon > 0$ always inflates the posterior.** Results should be reported with $\varepsilon$, and checked for stability as $\varepsilon$ decreases. A quantile-based $\varepsilon$ is data-dependent, which is convenient but makes $\varepsilon$ itself random.
- **Summary choice is a modelling decision.** For epidemic curves no low-dimensional sufficient statistic exists. Different summaries emphasise different phases: growth, peak, saturation. They can shift the posterior, as the table shows.
- **Prior sensitivity along non-identified directions.** Along the $\beta$–$\mu$ ridge, the posterior on $R_0$ is shaped by the prior box. Its upper end of about 10 reflects $\mu$'s lower bound.
- **Cost scales with simulations.** ABC is only as feasible as the simulator is fast. For large network or metapopulation simulators, SMC-type schemes, surrogates or emulators are needed. *My comment.*
- **Misspecification is not detected by ABC.** Toni et al.'s Tristan da Cunha estimate of $S(0)$ is the textbook example: a good fit with an implausible parameter.
- **Model choice** inherits the Robert et al. caveat whenever the distance uses summaries rather than the full data.

## Connections

- **PHYS 7335.**
  - The simulator is the stochastic SIR of [Compartmental models](./03-compartmental-models.md).
  - The relation between $r$ and $R_0$ comes from the Euler–Lotka argument in [Thresholds and next-generation matrices](./04-thresholds-and-ngm.md).
  - Calibrating large mobility-driven simulators ([Metapopulation models](./09-metapopulation-models.md)) is the natural large-scale use case. I have not checked which calibration method the GLEaM papers use.
  - On networks ([Heterogeneous mean-field](./05-heterogeneous-mean-field.md)), the likelihood also sums over node states, which makes simulation-based inference the default.
- **NETS 5116.** Spreading on networks ([Barabási ch. 10](../nets-5116/barabasi/10-spreading-phenomena.md)) gives the models whose parameters ABC calibrates.
- **NETS 7332.** Graph generative models are evaluated by comparing *distributions* of simulated and observed statistics with MMD ([Scaling and generative models](../nets-7332/basics/08-scaling-and-generative.md)). *My comment:* that is the same move as an ABC distance on summaries, and kernel distances between simulated and observed datasets have been proposed as ABC distances.

## Self-test

:::{dropdown} Q1. What distribution does rejection ABC sample from, and when does it equal the true posterior?
It samples $\pi\big(\theta \mid d(s(x^*), s(x_0)) \le \varepsilon\big)$. This equals $\pi(\theta \mid x_0)$ only in the limit $\varepsilon \to 0$ **and** if $s$ is sufficient. For $\varepsilon \to 0$ with insufficient $s$, it converges to $\pi(\theta \mid s(x_0))$.
:::

:::{dropdown} Q2. Why not use twenty summaries of the epidemic curve "to be safe"?
The acceptance rate scales roughly like $\varepsilon^{n_s}$. Weakly informative summaries add dimensions, and with them noise in the distance, while adding little information about $\theta$. For a fixed budget you must raise $\varepsilon$, which blurs the posterior.
:::

:::{dropdown} Q3. Write the ABC-SMC weight and explain why the intractable likelihood does not appear in it.
$w_t^{(i)} \propto \pi(\theta_t^{(i)}) / \sum_j w_{t-1}^{(j)} K_t(\theta_t^{(i)} \mid \theta_{t-1}^{(j)})$. The kept particles have density $\propto q_t(\theta) \Pr[d \le \varepsilon_t \mid \theta]$ and the target is $\propto \pi(\theta)\Pr[d \le \varepsilon_t \mid \theta]$. The acceptance probability, the only place the likelihood enters, cancels in the ratio.
:::

:::{dropdown} Q4. With uniform priors and a symmetric proposal, what is the ABC-MCMC acceptance step?
$\alpha = 1$. A proposal is accepted whenever its simulation falls within $\varepsilon$ (and it lies inside the prior support). Otherwise the chain stays put.
:::

:::{dropdown} Q5. Why can't the first two weeks of an outbreak determine $R_0$ in an SIR model?
Early incidence grows like $e^{(\beta-\mu)t}$, which pins $r = \beta - \mu$. Since $R_0 = 1 + r/\mu$, any $\mu$ is compatible: you need the infectious period, or equivalently the generation interval, from elsewhere. In the worked example, fixing $\mu$ narrows $\beta$ from 0.22–0.54 to 0.27–0.39.
:::

:::{dropdown} Q6. What goes wrong with ABC Bayes factors, per Robert et al. (2011)?
They converge to the Bayes factor of the summary statistics, $B_{12}^\eta$, not the true $B_{12}$. Unless the summary is sufficient across models, the two can be unrelated, even when $\eta$ is sufficient within each model (Poisson vs geometric with $\eta = \sum y_i$). More computation does not remove the gap. Distances on the full dataset avoid it.
:::

:::{dropdown} Q7. In Toni et al.'s Tristan da Cunha analysis, what does the low inferred $S(0)$ suggest?
Either most islanders were already immune to that cold strain, or the homogeneous-mixing SIR-type models are a poor description. ABC fitted the models well but cannot tell you the model class is wrong.
:::

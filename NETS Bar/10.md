# Chapter 10: Spreading Phenomena and Epidemic Spreading

## Section 10.1: Introduction

On February 21, 2003, a physician from Guangdong Province in southern China checked into the Metropole Hotel in Hong Kong, carrying what would become known as Severe Acute Respiratory Syndrome (SARS). That night, sixteen other guests and one visitor contracted the disease. These individuals carried the virus to Hanoi, Singapore, and Toronto, sparking outbreaks in each city. Close to half of the 8,100 documented SARS cases were traced back to the Metropole Hotel, making this physician an example of a *super-spreader*—an individual responsible for a disproportionate number of infections during an epidemic.

Network theorists recognize super-spreaders as *hubs*, nodes with exceptional numbers of links in the contact network on which disease spreads. This chapter introduces *network epidemics*, a network-based approach to understanding how the underlying topology of contact networks affects epidemic phenomena.

Infectious diseases account for 43% of the global burden of disease. The diversity of spreading processes on networks is staggering, encompassing:

**Biological**: Airborne diseases (influenza, SARS, tuberculosis), contagious diseases, sexually transmitted diseases (HIV/AIDS), and parasitic infections.

**Digital**: Computer viruses and mobile phone viruses spread via Bluetooth or multimedia messaging services (MMS).

**Social**: The spread of innovations, knowledge, rumors, and memes through social and professional networks.

Despite the diversity of spreading agents and networks, these processes obey common patterns and can be described using the same network-based theoretical framework.

---

## Section 10.2: Epidemic Modeling

Epidemiology relies on two fundamental hypotheses:

**Compartmentalization**: Individuals are classified into states:
- *Susceptible (S)*: Healthy individuals who have not contacted the pathogen
- *Infectious (I)*: Contagious individuals who can infect others
- *Recovered (R)*: Individuals who have recovered and are immune

**Homogenous Mixing**: Each individual has the same chance of contacting an infected individual, eliminating the need to know the precise contact network.

### Susceptible-Infected (SI) Model

Consider a disease spreading in a population of $N$ individuals. Let $S(t)$ denote susceptible individuals and $I(t)$ denote infected individuals. Assuming each individual has $\langle k \rangle$ contacts and transmission probability $\beta$ per unit time, the rate of new infections is:

$$\frac{dI(t)}{dt} = \beta \langle k \rangle \frac{S(t)I(t)}{N}$$

Using fractions $s(t) = S(t)/N$ and $i(t) = I(t)/N$:

$$\frac{di}{dt} = \beta \langle k \rangle i(1 - i) \quad (10.3)$$

where $\beta \langle k \rangle$ is the *transmission rate*. The solution is:

$$i = \frac{i_0 e^{\beta \langle k \rangle t}}{1 - i_0 + i_0 e^{\beta \langle k \rangle t}} \quad (10.4)$$

Key predictions:
- Early infection growth is exponential
- The *characteristic time* is $\tau = \frac{1}{\beta \langle k \rangle}$ (10.5)
- As time progresses, growth slows since fewer susceptible individuals remain

### Susceptible-Infected-Susceptible (SIS) Model

If infected individuals recover at rate $\mu$, becoming susceptible again:

$$\frac{di}{dt} = \beta \langle k \rangle i(1 - i) - \mu i \quad (10.6)$$

The solution approaches an endemic state or disease-free state depending on the *basic reproductive number*:

$$R_0 = \frac{\beta \langle k \rangle}{\mu} \quad (10.10)$$

- If $R_0 > 1$: Endemic state with finite fraction infected: $i(\infty) = 1 - \frac{\mu}{\beta \langle k \rangle}$ (10.8)
- If $R_0 < 1$: Disease-free state (pathogen dies out)

### Susceptible-Infected-Recovered (SIR) Model

Recovered individuals develop immunity rather than becoming susceptible again. The SIR model captures diseases like influenza and SARS.

The SI, SIS, and SIR models agree in early stages but differ for large times: SI leads to universal infection; SIS reaches endemic equilibrium or dies out; SIR results in universal recovery.

---

## Section 10.3: Network Epidemics

Traditional epidemic models assume homogenous mixing, ignoring that individuals contact only network-based neighbors. In reality, individuals vary widely in number of contacts, and contact networks are often scale-free.

### SI Model on a Network

Using the *degree block approximation*, nodes are grouped by degree, and we track $i_k$ (fraction of infected degree-$k$ nodes):

$$\frac{di_k}{dt} = \beta (1 - i_k) k \Theta_k \quad (10.13)$$

where $\Theta_k$ is the fraction of infected neighbors of a susceptible degree-$k$ node.

For early epidemic times:

$$\frac{di_k}{dt} \approx \beta k \Theta_k \quad (10.14)$$

For uncorrelated networks:

$$\frac{di_k}{dt} \approx \beta k i_0 \frac{\langle k \rangle - 1}{\langle k \rangle} e^{t/\tau^{SI}} \quad (10.15)$$

The characteristic time is:

$$\tau^{SI} = \frac{\langle k \rangle}{\beta(\langle k^2 \rangle - \langle k \rangle)} \quad (10.16)$$

This reveals a crucial difference from homogenous models:

- **Random Networks**: $\langle k^2 \rangle = \langle k \rangle(\langle k \rangle + 1)$, giving $\tau_{ER}^{SI} = \frac{1}{\beta \langle k \rangle}$ (10.19)
- **Scale-free Networks with $\gamma \leq 3$**: $\langle k^2 \rangle \to \infty$ in large networks, so $\tau^{SI} \to 0$—*the pathogen spreads instantaneously*

Hubs are infected first because they contact infected nodes through many links, creating super-spreaders.

### SIS Model and Vanishing Epidemic Threshold

For the SIS model on networks:

$$\tau^{SIS} = \frac{\langle k \rangle}{\beta \langle k^2 \rangle - \mu \langle k \rangle} \quad (10.21)$$

Define the *spreading rate*:

$$\lambda = \frac{\beta}{\mu} \quad (10.22)$$

The epidemic threshold $\lambda_c$ below which pathogens die out depends on network topology:

**Random Networks**:
$$\lambda_c = \frac{1}{\langle k \rangle + 1} \quad (10.25)$$

**Scale-free Networks**:
$$\lambda_c = \frac{\langle k \rangle}{\langle k^2 \rangle} \quad (10.26)$$

For scale-free networks with $\gamma < 3$, $\langle k^2 \rangle \to \infty$, so $\lambda_c \to 0$. This means *even weakly infectious viruses can persist in scale-free networks*.

**Two fundamental results**:
1. In large scale-free networks, $\tau = 0$ (instantaneous spreading)
2. In large scale-free networks, $\lambda_c = 0$ (vanishing epidemic threshold)

Both stem from hubs' ability to broadcast pathogens widely.

---

## Section 10.4: Contact Networks

The predictions of network epidemics depend critically on the actual structure of contact networks.

### Sexually Transmitted Diseases

The sex web in Sweden shows a power-law degree distribution ($\gamma = 2.6$–3.1), indicating that most individuals have few partners but a few have hundreds. This scale-free structure lowers both $\tau$ and $\lambda_c$.

### Airborne Diseases

**Global Travel Network**: The air transportation network connecting airports is scale-free with $\gamma = 1.8$, allowing rapid pathogen spread across continents.

**Local Contact Patterns**: Radio-frequency identification (RFID) badges reveal:
- Face-to-face interactions typically show exponential degree distributions
- Contact duration follows power-law distributions
- Link weights (cumulative contact time) are also power-law distributed

### Location Networks

Pathogens spread via *location networks* connecting physical places. Hub locations (malls, airports, schools) link to many smaller locations, enabling rapid disease spread.

### Digital Viruses

Computer and mobile viruses exploit various networks:
- Email viruses spread on scale-free email networks
- MMS viruses exploit mobile call networks (scale-free with high degree exponent)
- Bluetooth viruses spread via co-location networks

---

## Section 10.5: Beyond the Degree Distribution

Real networks have features beyond degree distribution that affect epidemic dynamics.

### Temporal Networks

Most interactions are brief and infrequent. Ignoring timing leads to overestimating outbreak speed and extent. A pathogen can spread only when contact actually occurs.

### Bursty Contact Patterns

Real interevent times follow power-law distributions, not exponential. This creates *bursty* contact patterns—periods of frequent interaction interrupted by long gaps. Burstiness increases the characteristic time $\tau$, causing slower decay of infection.

### Degree Correlations

Assortative networks (high-degree nodes connecting to other high-degree nodes) affect $\lambda_c$:
- Assortative correlations decrease $\lambda_c$ and accelerate spreading
- Disassortative correlations increase $\lambda_c$ and slow spreading
- The fundamental vanishing of $\lambda_c$ in scale-free networks persists despite correlations

### Link Weights and Communities

Information/pathogen flow depends on tie strength:
- Strong ties are typically within communities
- Weak ties bridge communities

In *simple contagion* (single contact sufficient for infection), communities trap pathogens, slowing spread. In *complex contagion* (requiring reinforcement), communities enhance adoption through social reinforcement.

Twitter analysis distinguishes viral memes (spreading across communities via simple contagion) from non-viral memes (trapped in communities via complex contagion).

---

## Section 10.6: Immunization

Immunization strategies aim to minimize pandemic threat given limited resources.

### Random Immunization

Immunizing a random fraction $g$ reduces the effective degree to $\langle k \rangle(1-g)$.

**Random Networks**: Critical immunization rate:
$$g_c = 1 - \frac{\mu}{\beta}\frac{1}{\langle k \rangle + 1} \quad (10.27)$$

**Heterogeneous Networks**: 
$$g_c = 1 - \frac{\mu}{\beta}\frac{\langle k \rangle}{\langle k^2 \rangle} \quad (10.29)$$

For scale-free networks, $g_c \to 1$, meaning we must immunize nearly everyone—impractical.

### Hub Immunization

Immunizing all nodes with degree $k > k'_{max}$ increases the epidemic threshold. By removing hubs, we fragment the contact network, making it harder for pathogens to spread widely.

The epidemic threshold after hub immunization becomes:

$$\lambda'_c \approx \frac{\gamma - 2}{3 - \gamma}\frac{k_{min}^{2-\gamma}}{(k'_{max})^{\gamma-3}} \quad (10.30)$$

### Friendship Paradox Immunization

Since neighbors of random nodes have higher average degree (friendship paradox), we can target hubs without knowing their identities:
1. Choose random fraction $p$ (Group 0)
2. Ask each to nominate a contact (Group 1)
3. Immunize Group 1

This requires less than 30% of population and is more efficient than random immunization across all degree exponents.

---

## Section 10.7: Epidemic Prediction

Real-time pandemic forecasting is now possible through computational models incorporating mobility, demographic, and epidemiological data.

### Real-Time Forecast with GLEAM

The Global Epidemic and Mobility (GLEAM) model:
- Maps geographic locations to network nodes
- Uses airline schedules as links
- Implements network-based epidemic framework
- Estimates parameters from observed global spread patterns

For the 2009 H1N1 pandemic:
- Predicted peak times fell within observed ranges for 87% of countries
- Correctly predicted early November peak (contrary to expected January peak)
- Quantified limited impact of late vaccination campaigns

### Travel Restrictions and Interventions

Simulations show:
- 40% travel reduction delays first infection by <3 days
- 90% reduction delays peak by <20 days
- Travel restrictions delay outbreaks but don't reduce total cases (only slow spread)
- Antiviral treatment delays peaks by 3–4 weeks

### Effective Distance

Physical distance is irrelevant for pathogens using air travel. Define *effective distance* based on the mobility network:

$$d_{ij} = (1 - \ln p_{ij}) \geq 0 \quad (10.31)$$

where $p_{ij}$ is the fraction of travelers from location $i$ going to location $j$.

In effective distance representation, epidemics follow circular wave fronts at constant speed. The arrival time is:

$$T_a = \frac{d_{eff}(P)}{V_{eff}(\beta, R_0, \gamma, \varepsilon)} \quad (10.32)$$

Relative arrival times depend only on effective distances, explaining why different models converge.

---

## Section 10.8: Summary

Network epidemics reveals how topology dramatically affects disease spreading:

**Key Results**:
- Vanishing characteristic time in scale-free networks ($\tau \to 0$)
- Vanishing epidemic threshold in scale-free networks ($\lambda_c \to 0$)
- Hubs are super-spreaders maintaining pathogens in populations
- Random immunization ineffective in heterogeneous networks
- Targeted/selective immunization can restore finite thresholds

The framework unifies diverse spreading phenomena—from pathogens to digital viruses to information—showing that network structure, not biological parameters alone, determines epidemic dynamics.

---

## Advanced Topics

### 10.A: Microscopic Models

The continuum equations derive from microscopic processes: probability of infection during $dt$ is $1 - (1-\beta dt)^{k_i} \approx \beta k_i dt$.

For epidemic persistence, average degree-$k$ node must infect $\beta k/\mu \geq 1$ other nodes during infectious period $1/\mu$.

### 10.B: Analytical Solutions

For uncorrelated networks lacking degree correlations:

$$\Theta_k = \frac{\sum_{k'} (k'-1)p_{k'} i_{k'}}{\langle k \rangle}$$

Solving SI, SIS, and SIR equations yields $\tau$ and $\lambda_c$ in Table 10.3.

### 10.C: Targeted Immunization

Removing high-degree nodes changes degree distribution. For scale-free networks immunizing all nodes with $k > k_0$:

$$\lambda'_c \approx \frac{\gamma - 2}{3 - \gamma}\frac{k_{min}^{2-\gamma}}{(k'_{max})^{\gamma-3}}$$

### 10.D: SIR Model and Percolation

SIR dynamics map to bond percolation with occupation probability $p_b = 1 - e^{-\beta/\mu}$. Infection clusters correspond to percolation components.

---

## References

[1–108] Comprehensive bibliography covering epidemiology, network science, and disease modeling from foundational works to contemporary studies on pandemic forecasting and control.
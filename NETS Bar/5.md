# Chapter 5: The Barabási-Albert Model

## Section 5.1: Introduction

Hubs represent the most striking difference between a random and a scale-free network. On the World Wide Web, they are websites with an exceptional number of links, like google.com or facebook.com; in the metabolic network they are molecules like ATP or ADP, energy carriers involved in an exceptional number of chemical reactions. The very existence of these hubs and the related scale-free topology raises two fundamental questions:

- Why do so different systems as the WWW or the cell converge to a similar scale-free architecture?
- Why does the random network model of Erdős and Rényi fail to reproduce the hubs and the power laws observed in real networks?

The first question is particularly puzzling given the fundamental differences in the nature, origin, and scope of the systems that display the scale-free property:

- The *nodes* of the cellular network are metabolites or proteins, while the nodes of the WWW are documents, representing information without a physical manifestation.
- The *links* within the cell are chemical reactions and binding interactions, while the links of the WWW are URLs, or small segments of computer code.
- The *history* of these two systems could not be more different: The cellular network is shaped by 4 billion years of evolution, while the WWW is less than three decades old.
- The *purpose* of the metabolic network is to produce the chemical components the cell needs to stay alive, while the purpose of the WWW is information access and delivery.

To understand why so *different* systems converge to a *similar* architecture we need to first understand the mechanism responsible for the emergence of the scale-free property. This is the main topic of this chapter. Given the diversity of the systems that display the scale-free property, the explanation must be simple and fundamental. The answers will change the way we model networks, forcing us to move from describing a network's topology to modeling the evolution of a complex system.

**Video 5.1: Scale-free Sonata**

Listen to a recording of Michael Edward Edgerton's *1 sonata for piano*, music inspired by scale-free networks.

---

## Section 5.2: Growth and Preferential Attachment

We start our journey by asking: Why are hubs and power laws absent in random networks? The answer emerged in 1999, highlighting two hidden assumptions of the Erdős-Rényi model, that are violated in real networks. Next we discuss these assumptions separately.

### Networks Expand Through the Addition of New Nodes

The random network model assumes that we have a *fixed* number of nodes, $N$. Yet, *in real networks the number of nodes continually grows thanks to the addition of new nodes*.

Consider a few examples:

- In 1991 the WWW had a single node, the first webpage build by Tim Berners-Lee, the creator of the Web. Today the Web has over a trillion ($10^{12}$) documents, an extraordinary number that was reached through the continuous addition of new documents by millions of individuals and institutions (Image 5.1a).
- The collaboration and the citation network continually expands through the publication of new research papers (Image 5.1b).
- The actor network continues to expand through the release of new movies (Image 5.1c).
- The protein interaction network may appear to be static, as we inherit our genes (and hence our proteins) from our parents. Yet, it is not: The number of genes grew from a few to the over 20,000 genes present in a human cell over four billion years.

Consequently, if we wish to model these networks, we cannot resort to a static model. Our modeling approach must instead acknowledge that networks are the product of a steady growth process.

![The Growth of Networks.](https://networksciencebook.com/images/ch-05/figure-5-1.jpg)

**Image 5.1: The Growth of Networks**

Networks are not static, but grow via the addition of new nodes:

a) The evolution of the number of WWW hosts, documenting the Web's rapid growth. After *http://www.isc.org/solutions/survey/history*.

b) The number of scientific papers published in *Physical Review* since the journal's founding. The increasing number of papers drives the growth of both the science collaboration network as well as of the citation network shown in the figure.

c) Number of movies listed in IMDB.com, driving the growth of the actor network.

### Nodes Prefer to Link to the More Connected Nodes

The random network model assumes that we randomly choose the interaction partners of a node. Yet, *most real networks new nodes prefer to link to the more connected nodes*, a process called *preferential attachment* (Image 5.2).

Consider a few examples:

- We are familiar with only a tiny fraction of the trillion or more documents available on the WWW. The nodes we know are not entirely random: We all heard about Google and Facebook, but we rarely encounter the billions of less-prominent nodes that populate the Web. As our knowledge is biased towards the more popular Web documents, we are more likely to link to a high-degree node than to a node with only few links.
- No scientist can attempt to read the more than a million scientific papers published each year. Yet, the more cited is a paper, the more likely that we hear about it and eventually read it. As we cite what we read, our citations are biased towards the more cited publications, representing the high-degree nodes of the citation network.
- The more movies an actor has played in, the more familiar is a casting director with her skills. Hence, the higher the degree of an actor in the actor network, the higher are the chances that she will be considered for a new role.

In summary, the random network model differs from real networks in two important characteristics:

1. **Growth**

   Real networks are the result of a growth process that continuously increases $N$. In contrast the random network model assumes that the number of nodes, $N$, is fixed.

2. **Preferential Attachment**

   In real networks new nodes tend to link to the more connected nodes. In contrast nodes in random networks randomly choose their interaction partners.

There are many other differences between real and random networks, some of which will be discussed in the coming chapters. Yet, as we show next, these two, *growth* and *preferential attachment*, play a particularly important role in shaping a network's degree distribution.

![Preferential Attachment: a Brief History.](https://networksciencebook.com/images/ch-05/figure-5-2.jpg)

**Image 5.2: Preferential Attachment: a Brief History**

---

## Section 5.3: The Barabási-Albert Model

The recognition that growth and preferential attachment coexist in real networks has inspired a minimal model called the *Barabási-Albert* model, which can generate scale-free networks. Also known as the BA model or the *scale-free model*, it is defined as follows:

We start with $m_0$ nodes, the links between which are chosen arbitrarily, as long as each node has at least one link. The network develops following two steps (Image 5.3):

a) **Growth**

   At each timestep we add a new node with $m$ ($\leq m_0$) links that connect the new node to $m$ nodes already in the network.

   **Preferential attachment**

   The probability $\Pi(k)$ that a link of the new node connects to node $i$ depends on the degree $k_i$ as

$$\Pi(k_i) = \frac{k_i}{\sum_j k_j} \hspace{20 mm} (5.1)$$

Preferential attachment is a probabilistic mechanism: A new node is free to connect to *any* node in the network, whether it is a hub or has a single link. Equation (5.1) implies, however, that if a new node has a choice between a degree-two and a degree-four node, it is twice as likely that it connects to the degree-four node.

![Evolution of the Barabási-Albert Model.](https://networksciencebook.com/images/ch-05/figure-5-3.jpg)

**Image 5.3: Evolution of the Barabási-Albert Model**

The sequence of images shows nine subsequent steps of the Barabási-Albert model. Empty circles mark the newly added node to the network, which decides where to connect its two links ($m$=2) using preferential attachment (5.1). After [9].

After t timesteps the Barabási-Albert model generates a network with $N = t + m_0$ nodes and $m_0 + mt$ links. As Image 5.4 shows, the obtained network has a power-law degree distribution with degree exponent $\gamma$=3. A mathematically self-consistent definition of the model is provided in BOX 5.1.

As Image 5.3 and Video 5.2 indicate, while most nodes in the network have only a few links, a few gradually turn into hubs. These hubs are the result of a *rich-gets-richer phenomenon*: Due to preferential attachment new nodes are more likely to connect to the more connected nodes than to the smaller nodes. Hence, the larger nodes will acquire links at the expense of the smaller nodes, eventually becoming hubs.

**Video 5.2: Emergence of a Scale-free Network**

Watch a video that shows the growth of a scale-free network and the emergence of the hubs in the Barabási-Albert model. Courtesy of Dashun Wang.

In summary, the Barabási-Albert model indicates that two simple mechanisms, *growth* and *preferential attachment*, are responsible for the emergence of scale-free networks. The origin of the power law and the associated hubs is a *rich-gets-richer phenomenon* induced by the coexistence of these two ingredients. To understand the model's behavior and to quantify the emergence of the scale-free property, we need to become familiar with the model's mathematical properties, which is the subject of the next section.

![The Degree Distribution](https://networksciencebook.com/images/ch-05/figure-5-4.jpg)

**Image 5.4: The Degree Distribution**

The degree distribution of a network generated by the Barabási-Albert model. The figure shows $p_k$ for a single network of size $N$=100,000 and $m$=3. It shows both the linearly-binned (purple) and the log-binned version (green) of $p_k$. The straight line is added to guide the eye and has slope $\gamma$=3, corresponding to the network's predicted degree exponent.

### Box 5.1: The Mathematical Definition of the Barabási-Albert Model

![The Linearized Chord Diagram (LCD).](https://networksciencebook.com/images/ch-05/figure-5-5.jpg)

**Image 5.5: The Linearized Chord Diagram (LCD)**

The construction of the LCD, the version of the Barabási-Albert model amenable to exact mathematical calculations. The figure shows the first four steps of the network's evolution for $m$=1

**$G_1^{(0)}$:** We start with an empty network.

**$G_1^{(1)}$:** The first node can only link to itself, forming a self-loop. Self-loops are allowed, and so are multi-links for $m$>1.

**$G_1^{(2)}$:** Node 2 can either connect to node 1 with probability 2/3, or to itself with probability 1/3. According to (5.2), half of the links that the new node 2 brings along is already counted as present. Consequently node 1 has degree $k_1$=2 at node 2 has degree $k_2$=1, the normalization constant being 3.

**$G_1^{(3)}$:** Let us assume that the first of the two $G_1^{(t)}$ network possibilities have materialized. When node 3 comes along, it again has three choices: It can connect to node 2 with probability 1/5, to node 1 with probability 3/5 and to itself with probability 1/5.

The definition of the Barabási-Albert model leaves many mathematical details open:

- It does not specify the precise initial configuration of the first $m_0$ nodes.
- It does not specify whether the $m$ links assigned to a new node are added one by one, or simultaneously. This leads to potential mathematical conflicts: If the links are truly independent, they could connect to the same node $i$, resulting in multi-links.

Bollobás and collaborators proposed the *Linearized Chord Diagram* (LCD) to resolve these problems, making the model more amenable to mathematical approaches.

According to the LCD, for $m$=1 we build a graph $G_1^{(t)}$ as follows (Image 5.5):

1. Start with G1(0), corresponding to an empty graph with no nodes.
2. Given $G_1^{(t-1)}$ generate $G_1^{(t)}$ by adding the node $v_t$ and a single link between $v_t$ and $v_i$, where $v_i$ is chosen with probability

$$p = \begin{cases} \frac{k_i}{2t - 1}, & \text{if } 1 \le i \le t - 1 \\ \frac{1}{2t - 1}, & \text{if } i = t \end{cases} \hspace{20 mm} (5.2)$$

That is, we place a link from the new node $v_t$ to node $v_i$ with probability $k_i/(2t-1)$, where the new link already contributes to the degree of $v_t$. Consequently node $v_t$ can also link to itself with probability $1/(2t - 1)$, the second term in (5.2). Note also that the model permits self-loops and multi-links. Yet, their number becomes negligible in the $t\to\infty$ limit.

For $m$ > 1 we build $G_m^{(t)}$ by adding $m$ links from the new node $v_t$ one by one, in each step allowing the outward half of the newly added link to contribute to the degrees.

---

## Section 5.4: Degree Dynamics

To understand the emergence of the scale-free property, we need to focus on the time evolution of the Barabási-Albert model. We begin by exploring the time-dependent degree of a single node.

In the model an existing node can increase its degree each time a *new* node enters the network. This new node will link to $m$ of the $N(t)$ nodes already present in the system. The probability that one of these links connects to node $i$ is given by (5.1).

Let us approximate the degree $k_i$ with a continuous real variable, representing its expectation value over many realizations of the growth process. The rate at which an existing node $i$ acquires links as a result of new nodes connecting to it is

$$\frac{dk_i}{dt} = m\Pi(k_i) = m\frac{k_i}{\sum_{j = 1}^{N - 1} k_j} \hspace{20 mm} (5.3)$$

The coefficient $m$ describes that each new node arrives with $m$ links. Hence, node $i$ has $m$ chances to be chosen. The sum in the denominator of (5.3) goes over all nodes in the network except the newly added node, thus

$$\sum_{j = 1}^{N - 1} k_j = 2mt - m \hspace{20 mm} (5.4)$$

Therefore (5.4) becomes

$$\frac{dk_i}{dt} = \frac{k_i}{2t - 1} \hspace{20 mm} (5.5)$$

For large t the (-1) term can be neglected in the denominator, obtaining

$$\frac{dk_i}{k_i} = \frac{1}{2}\frac{dt}{t} \hspace{20 mm} (5.6)$$

By integrating (5.6) and using the fact that $k_i(t_i)=m$, meaning that node $i$ joins the network at time $t_i$ with $m$ links, we obtain

$$k_i(t) = m\left(\frac{t}{t_i}\right)^\beta \hspace{20 mm} (5.7)$$

We call $\beta$ the *dynamical exponent* and has the value

$$\beta = \frac{1}{2}$$

Equation (5.7) offers a number of predictions:

- The degree of each node increases following a power-law with the same dynamical exponent $\beta$ =1/2 (Image 5.6a). Hence all nodes follow the same dynamical law.
- The growth in the degrees is sublinear (i.e. $\beta$ < 1). This is a consequence of the growing nature of the Barabási-Albert model: Each new node has more nodes to link to than the previous node. Hence, with time the existing nodes compete for links with an increasing pool of other nodes.
- The earlier node $i$ was added, the higher is its degree $k_i(t)$. Hence, hubs are large because they arrived earlier, a phenomenon called *first-mover advantage* in marketing and business.
- The rate at which the node $i$ acquires new links is given by the derivative of (5.7)

$$\frac{dk_i(t)}{dt} = \frac{m}{2}\frac{1}{\sqrt{t_i t}} \hspace{20 mm} (5.8)$$

indicating that in each time step older nodes acquire more links (as they have smaller $t_i$). Furthermore the rate at which a node acquires links decreases with time as $t^{-1/2}$. Hence, fewer and fewer links go to a node.

![Degree Dynamics.](https://networksciencebook.com/images/ch-05/figure-5-6.jpg)

**Image 5.6: Degree Dynamics**

a) The growth of the degrees of nodes added at time $t$ =1, 10, $10^2$, $10^3$, $10^4$, $10^5$ (continuous lines from left to right) in the Barabási-Albert model. Each node increases its degree following (5.7). Consequently at any moment the older nodes have higher degrees. The dotted line corresponds to the analytical prediction (5.7) with $\beta$ = 1/2.

b) Degree distribution of the network after adding $N$ = $10^2$, $10^4$, and $10^6$ nodes, i.e. at time $t$ = $10^2$, $10^4$, and $10^6$ (illustrated by arrows in (a)). The larger the network, the more obvious is the power-law nature of the degree distribution. Note that we used linear binning for $p^k$ to better observe the gradual emergence of the scale-free state.

In summary, the Barabási-Albert model captures the fact that in real networks nodes arrive one after the other, offering a dynamical description of a network's evolution. This generates a competition for links during which the older nodes have an advantage over the younger ones, eventually turning into hubs.

### Box 5.2: Time in Networks

As we compare the predictions of the network models with real data, we have to decide how to measure *time* in networks. Real networks evolve over rather different time scales:

**World Wide Web**

The first webpage was created in 1991. Given its trillion documents, the WWW added a node each millisecond ($10^3$ sec).

**Cell**

The cell is the result of 4 billion years of evolution. With roughly 20,000 genes in a human cell, on average the cellular network added a node every 200,000 years (~$10^{13}$ sec).

Given these enormous time-scale differences it is impossible to use real time to compare the dynamics of different networks. Therefore, in network theory we use *event time*, advancing our time-step by one each time when there is a change in the network topology.

For example, in the Barabási-Albert model the addition of each new node corresponds to a new time step, hence $t=N$. In other models time is also advanced by the arrival of a new link or the deletion of a node. If needed, we can establish a direct mapping between event time and the physical time.

---

## Section 5.5: Degree Distribution

The distinguishing feature of the networks generated by the Barabási-Albert model is their power-law degree distribution (Image 5.4). In this section we calculate the functional form of $p_k$, helping us understand its origin.

A number of analytical tools are available to calculate the degree distribution of the Barabási-Albert network. The simplest is the *continuum theory* that we started developing in the previous section. It predicts the degree distribution (BOX 5.3),

$$p(k) \approx 2m^{1/\beta} k^{-\gamma} \hspace{20 mm} (5.9)$$

with

$$\gamma = \frac{1}{\beta} + 1 = 3 \hspace{20 mm} (5.10)$$

Therefore the degree distribution follows a power law with degree exponent $\gamma$=3, in agreement with the numerical results (Figures 5.4 and 5.7). Moreover (5.10) links the degree exponent, $\gamma$, a quantity characterizing the network topology, to the dynamical exponent $\beta$ that characterizes a node's temporal evolution, revealing a deep relationship between the network's topology and dynamics.

![Probing the Analytical Predictions.](https://networksciencebook.com/images/ch-05/figure-5-7.jpg)

**Image 5.7: Probing the Analytical Predictions**

a) We generated networks with $N$=100,000 and $m_0$=$m$=1 (blue), 3 (green), 5 (grey), and 7 (orange). The fact that the curves are parallel to each other indicates that $\gamma$ is independent of $m$ and $m_0$. The slope of the purple line is -3, corresponding to the predicted degree exponent $\gamma$=3. Inset: (5.11) predicts $p_k$~2$m^2$, hence $p_k$/2$m^2$ should be independent of $m$. Indeed, by plotting $p_k$/2$m^2$ vs. $k$, the data points shown in the main plot collapse into a single curve.

b) The Barabási-Albert model predicts that $p_k$ is independent of $N$. To test this we plot $p_k$ for $N$ = 50,000 (blue), 100,000 (green), and 200,000 (grey), with $m_0$=$m$=3. The obtained $p_k$ are practically indistinguishable, indicating that the degree distribution is *stationary*, i.e. independent of time and system size.

While the continuum theory predicts the correct degree exponent, it fails to accurately predict the pre-factors of (5.9). The correct pre-factors can be obtained using a master or rate equation approach or calculated exactly using the LCD model (BOX 5.3). Consequently the *exact degree distribution* of the Barabási-Albert model is (ADVANCED TOPICS 5.A)

$$p_k = \frac{2m(m + 1)}{k(k + 1)(k + 2)} \hspace{20 mm} (5.11)$$

Equation (5.11) has several implications:

- For large $k$ (5.11) reduces to $p_k$~ $k^{-3}$, or $\gamma$ = 3, in line with (5.9) and (5.10).
- The degree exponent $\gamma$ is independent of $m$, a prediction that agrees with the numerical results (Image 5.7a).
- The power-law degree distribution observed in real networks describes systems of rather different age and size. Hence, an approriate model should lead to a time-independent degree distribution. Indeed, according to (5.11) the degree distribution of the Barabási-Albert model is independent of both $t$ and $N$. Hence the model predicts the emergence of a *stationary scale-free state*. Numerical simulations support this prediction, indicating that $p_k$ observed for different $t$ (or $N$) fully overlap (Image 5.7b).
- Equation (5.11) predicts that the coefficient of the power-law distribution is proportional to $m(m + 1)$ (or $m^2$ for large $m$), again confirmed by numerical simulations (Image 5.7a, inset).

In summary, the analytical calculations predict that the Barabási-Albert model generates a scale-free network with degree exponent $\gamma$=3. The degree exponent is independent of the $m$ and $m_0$ parameters. Furthermore, the degree distribution is stationary (i.e. time invariant), explaining why networks with different history, size and age develop a similar degree distribution.

### Box 5.3: Continuum Theory

To calculate the degree distribution of the Barabási-Albert model in the continuum approximation we first calculate the number of nodes with degree smaller than $k$, i.e. $k_i(t)$ < $k$. Using (5.7), we write

$$t_i < t\left(\frac{m}{k}\right)^{1/\beta} \hspace{20 mm} (5.12)$$

In the model we add a node at equal time step (BOX 5.2). Therefore the number of nodes with degree smaller than $k$ is

$$t\left(\frac{m}{k}\right)^{1/\beta} \hspace{20 mm} (5.13)$$

Altogether there are $N=m_0+t$ nodes, which becomes $N\approx t$ in the large $t$ limit. Therefore the probability that a randomly chosen node has degree $k$ or smaller, which is the cumulative degree distribution, follows

$$P(k) = 1 - \left(\frac{m}{k}\right)^{1/\beta} \hspace{20 mm} (5.14)$$

By taking the derivative of (5.14) we obtain the degree distribution

$$p_k = \frac{\partial P(k)}{\partial k} = \frac{1}{\beta}\frac{m^{1/\beta}}{k^{1/\beta + 1}} = 2m^2 k^{-3} \hspace{20 mm} (5.15)$$

which is (5.9).

---

## Section 5.6: The Absence of Growth or Preferential Attachment

The coexistence of growth and preferential attachment in the Barabási-Albert model raises an important question: Are they both necessary for the emergence of the scale-free property? In other words, could we generate a scale-free network with only one of the two ingredients? To address these questions, next we discuss two limiting cases of the model, each containing only one of the two ingredients.

### Model A

To test the role of preferential attachment we keep the growing character of the network (ingredient A) and eliminate preferential attachment (ingredient B). Hence, *Model A* starts with $m_0$ nodes and evolves following these steps:

**A. Growth**

At each time step we add a new node with $m(\leq m_0)$ links that connect to $m$ nodes added earlier.

**B. Preferential Attachment**

The probability that a new node links to a node with degree $k_i$ is

$$\Pi(k_i) = \frac{1}{(m_0 + t - 1)} \hspace{20 mm} (5.16)$$

That is, $\Pi(k_i)$ is independent of $k_i$, indicating that new nodes choose randomly the nodes they link to.

The continuum theory predicts that for Model A $k_i(t)$ increases logarithmically with time

$$k_i(t) = m\ln\left(e\frac{m_0 + t - 1}{m_0 + t_i - 1}\right) \hspace{20 mm} (5.17)$$

a much slower growth than the power law increase (5.7). Consequently the degree distribution follows an exponential (Image 5.8a)

$$p(k) = \frac{e}{m}\exp\left(-\frac{k}{m}\right) \hspace{20 mm} (5.18)$$

An exponential function decays much faster than a power law, hence it does not support hubs. Therefore the lack of preferential attachment eliminates the network's scale-free character and the hubs. Indeed, as all nodes acquire links with equal probabilty, we lack a rich-get-richer process and no clear winner can emerge.

### Model B

To test the role of growth next we keep preferential attachment (ingredient B) and eliminate growth (ingredient A). Hence, *Model B* starts with $N$ nodes and evolves following this step:

**B. Preferential Attachment**

At each time step a node is selected randomly and connected to node $i$ with degree $k_i$ already present in the network, where $i$ is chosen with probability $\Pi(k)$. As $\Pi(0)=0$ nodes with $k$=0 are assumed to have $k$=1, otherwise they can not acquire links.

In Model B the number of nodes remains constant during the network's evolution, while the number of links increases linearly with time. As a result for large $t$ the degree of each node also increases linearly with time (Image 5.7b, inset)

$$k_i(t) \approx \frac{2}{N}t \hspace{20 mm} (5.19)$$

Indeed, in each time step we add a new link, without changing the number of nodes.

At early times, when there are only a few links in the network (i.e. $L$ ≪ $N$), each new link connects previously unconnected nodes. In this stage the model's evolution is indistinguishable from the Barabási-Albert model with $m$=1. Numerical simulations show that in this regime the model develops a degree distribution with a power-law tail (Image 5.8b).

Yet, $p_k$ is not stationary. Indeed, after a transient period the node degrees converge to the average degree (5.19) and the degree develops a peak (Image 5.8b). For $t$ → $N(N-1)/2$ the network becomes a complete graph in which all nodes have degree $k_{max}$=$N$-1, hence $p_k$= $\delta(N-1)$.

![Model A and Model B.](https://networksciencebook.com/images/ch-05/figure-5-8.jpg)

**Image 5.8: Model A and Model B**

Numerical simulations probing the role of growth and preferential attachment.

**a) Model A**

Degree distribution for Model A, that incorporates growth but lacks preferential attachment. The symbols correspond to $m_0$=$m$=1 (circles), 3 (squares), 5 diamonds), 7 (triangles) and $N$=800,000. The linear-log plot indicates that the resulting network has an exponential $p_k$, as predicted by (5.18).

Inset: Time evolution of the degree of two nodes added at $t_1$=7 and $t_2$=97 for $m_0$=$m$=3. The dashed line follows (5.17).

**b) Model B**

Degree distribution for Model B, that lacks growth but incorporates preferential attachment, shown for $N$=10,000 and $t$=$N$ (circles), $t$=5$N$ (squares), and $t$=40$N$ (diamonds). The changing shape of $p_k$ indicates that the degree distribution is not stationary.

Inset: Time dependent degrees of two nodes (N=10,000), indicating that $k_i(t)$ grows linearly, as predicted by (5.19). After [11].

In summary, the absence of preferential attachment leads to a growing network with a stationary but exponential degree distribution. In contrast the absence of growth leads to the loss of stationarity, forcing the network to converge to a complete graph. This failure of Models A and B to reproduce the empirically observed scale-free distribution indicates that growth and preferential attachment are simultaneously needed for the emergence of the scale-free property.

---

## Section 5.7: Measuring Preferential Attachment

In the previous section we showed that growth and preferential attachment are jointly responsible for the scale-free property. The presence of growth in real systems is obvious: All large networks have reached their current size by adding new nodes. But to convince ourselves that preferential attachment is also present in real networks, we need to detect it experimentally. In this section we show how to detect preferential attachment by measuring the $\Pi(k)$ function in real networks.

Preferential attachment relies on two distinct hypotheses:

**Hypothesis 1**

The likelihood to connect to a node depends on that node's degree $k$. This is in contrast with the random network model, for which $\Pi(k)$ is independent of $k$.

**Hypothesis 2**

The functional form of $\Pi(k)$ is linear in $k$.

Both hypotheses can be tested by measuring $\Pi(k)$. We can determine $\Pi(k)$ for systems for which we know the time at which each node joined the network, or we have at least two network maps collected at not too distant moments in time.

Consider a network for which we have two different maps, the first taken at time $t$ and the second at time $t + \Delta t$ (Image 5.9a). For nodes that changed their degree during the $\Delta t$ time frame we measure $\Delta k_i = k_i(t+\Delta t)−k_i(t)$. According to (5.1), the relative change $\Delta k_i/\Delta t$ should follow

$$\frac{\Delta k_i}{\Delta t} \sim \Pi(k_i) \hspace{20 mm} (5.20)$$

providing the functional form of preferential attachment. For (5.20) to be valid we must keep $\Delta t$ small, so that the changes in $\Delta k$ are modest. But $\Delta t$ must not be too small so that there are still detectable differences between the two networks.

![Detecting Preferential Attachment.](https://networksciencebook.com/images/ch-05/figure-5-9.jpg)

**Image 5.9: Detecting Preferential Attachment**

a) If we have access to two maps of the same network taken at time $t$ and $t$+$\Delta t$, comparing them allows us to measure the $\Pi(k)$ function. Specifically, we look at nodes that have gained new links thanks to the arrival of the two new green nodes at $t$+$\Delta t$. The orange lines correspond to links that connect previously disconnected nodes, called *internal links*. Their role is discussed in CHAPTER 6.

b) In the presence of preferential attachment $\Delta k/\Delta t$ will depend linearly on a node's degree at time $t$.

c) The scaling of the cumulative preferential attachment function $\pi(k)$ helps us detect the presence or absence of preferential attachment (Image 5.10).

In practice the obtained $\Delta k_i/\Delta t$ curve can be noisy. To reduce this noise we measure the *cumulative preferential attachment function*

$$\pi(k) = \sum_{k_i = 0}^k \Pi(k_i) \hspace{20 mm} (5.21)$$

In the absence of preferential attachment we have $\Pi(k_i)$=constant, hence, $\pi(k)$ ~ $k$ according to (5.21). If linear preferential attachment is present, i.e. if $\Pi(k_i)=k_i$, we expect $\pi(k)$ ~ $k^2$.

Image 5.10 shows the measured $\pi(k)$ for four real networks. For each system we observe a faster than linear increase in $\pi(k)$, indicating the presence of preferential attachment. Image 5.10 also suggests that $\Pi(k)$ can be approximated with

$$\Pi(k) \sim k^\alpha \hspace{20 mm} (5.22)$$

For the Internet and citation networks we have $\alpha$ ≈ 1, indicating that $\Pi(k)$ depends linearly on $k$, following (5.1). This is in line with Hypotheses 1 and 2. For the co-authorship and the actor network the best fit provides $\alpha$=0.9±0.1 indicating the presence of a *sublinear preferential attachment*.

In summary, (5.20) allows us to detect the presence (or absence) of preferential attachment in real networks. The measurements show that the attachment probability depends on the node degree. We also find that while in some systems preferential attachment is linear, in others it can be sublinear. The implications of this non-linearity are discussed in the next section.

![Evidence of Preferential Attachmentt](https://networksciencebook.com/images/ch-05/figure-5-10.jpg)

**Image 5.10: Evidence of Preferential Attachment**

The figure shows the cumulative preferential attachment function $\pi(k)$, defined in (5.21), for several real systems:

a) Citation network.

b) Internet.

c) Scientific collaboration network (neuroscience).

d) Actor network.

In each panel we have two lines to guide the eye: The dashed line corresponds to linear preferential attachment ($\pi(k)$~$k^2$) and the continuous line indicates the absence of preferential attachment ($\pi(k)$~$k$). In line with Hypothesis 1 we detect a $k$-dependence in each dataset. Yet, in (c) and (d) $\pi(k)$ grows slower than $k^2$, indicating that for these systems preferential attachment is sublinear, violating Hypothesis 2. Note that these measurements only consider links added through the arrival of new nodes, ignoring the addition of internal links. After [14].

---

## Section 5.8: Non-linear Preferential Attachment

The observation of sublinear preferential attachment in Image 5.10 raises an important question: What is the impact of this nonlinearity on the network topology? To answer this we replace the linear preferential attachment (5.1) with (5.22) and calculate the degree distribution of the obtained *nonlinear Barabási-Albert model*.

The behavior for $\alpha$=0 is clear: In the absence of preferential attachment we are back to Model A discussed in SECTION 5.4. Consequently the degree distribution follows the exponential (5.17).

For $\alpha$ = 1 we recover the Barabási-Albert model, obtaining a scale-free network with degree distribution (5.14).

Next we focus on the case $\alpha$ ≠ 0 and $\alpha$ ≠ 1. The calculation of $p_k$ for an arbitrary $\alpha$ predicts several scaling regimes (ADVANCED TOPICS 5.B):

### Sublinear Preferential Attachment (0 < α < 1)

For any $\alpha$ > 0 new nodes favor the more connected nodes over the less connected nodes. Yet, for $\alpha$ < 1 the bias is weak, not sufficient to generate a scale-free degree distribution. Instead, in this regime the degrees follow the stretched exponential distribution (SECTION 4.10)

$$p_k \sim k^{-\alpha} \exp\left(\frac{-2\mu(\alpha)}{⟨k⟩(1 - \alpha)}k^{1 - \alpha}\right) \hspace{20 mm} (5.23s)$$

where $\mu(\alpha)$ depends only weakly on $\alpha$. The exponential cutoff in (5.23) implies that sublinear preferential attachment limits the size and the number of the hubs.

Sublinear preferential attachment also alters the size of the largest degree, $k_{max}$. For a scale-free network $k_{max}$ scales polynomially with time, following (4.18). For sublinear preferential attachment we have

$$k_{\max} \sim (\ln t)^{1/(1 - \alpha)} \hspace{20 mm} (5.24)$$

a logarithmic dependence that predicts a much slower growth of the maximum degee than the polynomial. This slower growth is the reason why the hubs are smaller for $\alpha$ < 1 (Image 5.11).

### Superlinear Preferential Attachment (α > 1)

For $\alpha$ > 1 the tendency to link to highly connected nodes is enhanced, accelerating the *rich-gets-richer process*. The consequence of this is most obvious for $\alpha$ > 2, when the model predicts a *winner-takes-all* phenomenon: almost all nodes connect to a few super-hubs. Hence we observe the emergence of a hub-and-spoke network, in which most nodes link directly to a few central nodes. The situation for 1 < $\alpha$ < 2 is less extreme, but similar.

This winner-takes-all process alters the size of the largest hub as well, finding that (Image 5.11).

$$k_{\max} \sim t \hspace{20 mm} (5.25)$$

In summary, nonlinear preferential attachment changes the degree distribution, either limiting the size of the hubs ($\alpha$ < 1), or leading to super-hubs ($\alpha$ > 1, Image 5.12). Consequently, $\Pi(k)$ needs to depend strictly linearly on the degrees for the resulting network to have a pure power law $p_k$. While in many systems we do observe such a linear dependence, in others, like the scientific collaboration network and the actor network, preferential attachment is sublinear. This nonlinear $\Pi(k)$ is one reason the degree distribution of real networks deviates from a pure power-law. Hence for systems with sublinear $\Pi(k)$ the stretched exponential (5.23) should offer a better fit to the degree distribution.

![The Growth of the Hubs.](https://networksciencebook.com/images/ch-05/figure-5-11.jpg)

**Image 5.11: The Growth of the Hubs**

The nature of preferential attachment affects the degree of the largest node. While in a scalefree network ($\alpha$=1) the biggest hub grows as $t^{1/2}$ (green curve, (4.18)), for *sublinear preferential attachment* ($\alpha$ < 1) this dependence becomes logarithmic, following (5.24). For *superlinear preferential attachment* ($\alpha$ > 1) the biggest hub grows linearly with time, always grabbing a finite fraction of all links, following (5.25). The symbols are provided by numerical simulations; the dotted lines represent the analytical predictions.

![Nonlinear Preferential Attachment.](https://networksciencebook.com/images/ch-05/figure-5-12.jpg)

**Image 5.12: Nonlinear Preferential Attachment**

The scaling regimes characterizing the nonlinear Barabási-Albert model. The three top panels show $p_k$ for different $\alpha$ ($N$=$10^4$). The network maps show the corresponding topologies ($N$=100). The theoretical results predict the existence of four scaling regimes:

**No Preferential Attachment (α=0)**

The network has a simple exponential degree distribution, following (5.18). Hubs are absent and the resulting network is similar to a random network.

**Sublinear Regime (0 < α < 1)**

The degree distribution follows the stretched exponential (5.23), resulting in fewer and smaller hubs than in a scale-free network. As $\alpha$ → 1 the cutoff length increases and $p_k$ follows a power law over an increasing range of degrees.

**Linear Regime (α=1)**

This corresponds to the Barabási-Albert model, hence the degree distribution follows a power law.

**Superlinear Regime (α > 1)**

The high-degree nodes are disproportionately attractive. A winner-takes-all dynamics leads to a hub-and-spoke topology. In this configuration the earliest nodes become super hubs and all subsequent nodes link to them. The degree distribution, shown for $\alpha$=1.5 indicates the coexistence of many small nodes with a few *super hubs* in the vicinity of k=$10^4$.

---

## Section 5.9: The Origins of Preferential Attachment

Given the key role preferential attachment plays in the evolution of real networks, we must ask, where does it come from? The question can be broken to two narrower issues:

Why does $\Pi(k)$ depend on $k$?

Why is the dependence of $\Pi(k)$ linear in $k$?

In the past decade we witnessed the emergence of two philosophically different answers to these questions. The first views preferential attachment as the interplay between random events and some structural property of a network. These mechanisms do not require global knowledge of the network but rely on random events, hence we will call them *local* or *random* mechanisms. The second assumes that each new node or link balances conflicting needs, hence they are preceeded by a cost-benefit analysis. These models assume familiarity with the whole network and rely on optimization principles, prompting us to call them *global* or *optimized* mechanisms. In this section we discuss both approaches.

### Local Mechanisms

The Barabási-Albert model postulates the presence of preferential attachment. Yet, as we show below, we can build models that generate scalefree networks apparently without preferential attachment. They work by *generating* preferential attachment. Next we discuss two such models and derive $\Pi(k)$ for them, allowing us to understand the origins of preferential attachment.

**Link Selection Model**

The *link selection model* offers perhaps the simplest example of a local mechanism that generates a scale-free network without preferential attachment. It is defined as follows (Image 5.13):

- *Growth*: At each time step we add a new node to the network.
- *Link Selection*: We select a link at random and connect the new node to one of the two nodes at the two ends of the selected link. The model requires no knowledge about the overall network topology, hence it is inherently local and random. Unlike the Barabási-Albert model, it lacks a built-in $\Pi(k)$ function. Yet, next we show that it generates preferential attachment.

![Link Selection Model.](https://networksciencebook.com/images/ch-05/figure-5-13.jpg)

**Image 5.13: Link Selection Model**

a) The network grows by adding a new node, that selects randomly a link from the network (shown in purple).

b) The new node connects with equal probability to one of the two nodes at the ends of the selected link. In this case the new node connected to the node at the right end of the selected link.

We start by writing the probability $q_k$ that the node at the end of a randomly chosen link has degree $k$ as

$$q_k = Ckp_k \hspace{20 mm} (5.26)$$

Equation (5.26) captures two effects:

- The higher is the degree of a node, the higher is the chance that it is located at the end of the chosen link.
- The more degree-$k$ nodes are in the network (i.e., the higher is $p_k$), the more likely that a degree k node is at the end of the link.

In (5.26) $C$ can be calculated using the normalization condition $\sum q_k$ = 1, obtaining $C$=1/$⟨k⟩$. Hence the probability to find a degree-$k$ node at the end of a randomly chosen link is

$$q_k = \frac{kp_k}{⟨k⟩} \hspace{20 mm} (5.27)$$

Equation (5.27) is the probability that a new node connects to a node with degree $k$. The fact that the bias in (5.27) is linear in k indicates that the link selection model builds a scale-free network by generating linear preferential attachment.

**Copying Model**

While the link selection model offers the simplest mechanism for preferential attachment, it is neither the first nor the most popular in the class of models that rely on local mechanisms. That distinction goes to the *copying model* (Image 5.14). The model mimics a simple phenomena: The authors of a new webpage tend to borrow links from other webpages on related topics. It is defined as follows:

![Copying Model.](https://networksciencebook.com/images/ch-05/figure-5-14.jpg)

**Image 5.14: Copying Model**

The main steps of the copying model. A new node connects with probability $p$ to a randomly chosen target node $u$, or with probability 1-$p$ to one of the nodes the target $u$ points to. In other words, with probabilty 1-$p$ the new node *copies* a link of its target $u$.

In each time step a new node is added to the network. To decide where it connects we randomly select a node $u$, corresponding for example to a web document whose content is related to the content of the new node. Then we follow a two-step procedure (Image 5.14):

i) *Random Connection*: With probability $p$ the new node links to $u$, which means that we link to the randomly selected web document.

ii) *Copying*: With probability 1-$p$ we randomly choose an *outgoing link* of node $u$ and link the new node to the link's target. In other words, the new webpage *copies* a link of node $u$ and connects to its target, rather than connecting to node u directly.

The probability of selecting a particular node in step (i) is 1/$N$. Step (ii) is equivalent with selecting a node linked to a randomly selected link. The probability of selecting a degree-k node through this copying step (ii) is $k$/2$L$ for undirected networks. Combining (i) and (ii), the likelihood that a new node connects to a degree-k node follows

$$\Pi(k) = \frac{p}{N} + \frac{1 - p}{2L}k$$

which, being linear in $k$, predicts a linear preferential attachment

The popularity of the copying model lies in its relevance to real systems:

- *Social Networks*: The more acquaintances an individual has, the higher is the chance that she will be introduced to new individuals by her existing acquaintances. In other words, we "copy" the friends of our friends. Consequently without friends, it is difficult to make new friends.
- *Citation Networks*: No scientist can be familiar with all papers published on a certain topic. Authors decide what to read and cite by "copying" references from the papers they have read. Consequently papers with more citations are more likely to be studied and cited again.
- *Protein Interactions*: Gene duplication, responsible for the emergence of new genes in a cell, can be mapped into the copying model, explaining the scale-free nature of protein interaction networks.

Taken together, we find that both the link selection model and the copying model generate a linear preferential attachment through random linking.

### Optimization

A longstanding assumption of economics is that humans make rational decisions, balancing cost against benefits. In other words, each individual aims to maximize its personal advantage. This is the starting point of rational choice theory in economics and it is a hypothesis central to modern political science, sociology, and philosophy. As we show below, such rational decisions can lead to preferential attachment.

Consider the Internet, whose nodes are routers connected via cables. Establishing a new Internet connection between two routers requires us to lay down a new cable between them. As this is costly, each new link is preceded by a careful cost-benefit analysis. Each new router (node) will choose its link to balance access to good network performance (i.e. proper bandwith) with the cost of laying down a new cable (i.e. physical distance). This can be a conflicting desire, as the closest node may not offer the best network performance

For simplicity let us assume that all nodes are located on a continent with the shape of a unit square. At each time step we add a new node and randomly choose a point within the square as its physical location. When deciding where to connect the new node $i$, we calculate the cost function

$$C_i = \min_j [\delta d_{ij} + h_j] \hspace{20 mm} (5.28)$$

which compares the cost of connecting to each node $j$ already in the network. Here $d_{ij}$ is the Euclidean distance between the new node $i$ and the potential target $j$, and $h_j$ is the network-based distance of node $j$ to the *first node* of the network, which we designate as the desireable "center" of the network, offering the best network performance. Hence $h_j$ captures the "resources" offered by node $j$, measured by its distance to the network's center.

![Optimization Model.](https://networksciencebook.com/images/ch-05/figure-5-15.jpg)

**Image 5.15: Optimization Model**

**(a)** A small network, where the $h_j$ term in the cost function (5.28) is shown for each node. Here hj represents the network-based distance of node $j$ from node $i$=0, designated as the "center" of the network, offering the best network performance. Hence $h_0$=0 and $h_3$=2.

**(b)** A new node (green) will choose the node $j$ to which it connects by minimizing $C_j$ of (5.28).

**(c)-(e)** If $\delta$ is small the new node will connect to the central node with $h_j$ =0. As we increase $\delta$, the balance in (5.28) shifts, forcing the new node to connect to more distant nodes. The panels (c)-(e) show the choice of the new green node makes for different values of $\delta$.

**(f)** The basin of attraction for each node for $\delta$=10. A new node arriving inside a basin will always link to the node at the center of the basin. The size of each basin depends on the degree of the node at its center. Indeed, the smaller is hj, the larger can be the distance to the new node while still minimizing (5.28). Yet, the higher is the degree of node $j$, the smaller is its expected distance to the central node $h_j$.

The calculations indicate the emergence of three distinct network topologies, depending on the value of the parameter $\delta$ in (5.28) and $N$ (Image 5.15):

**Star Network δ < (1/2)^(1/2)**

For $\delta$ = 0 the Euclidean distances are irrelevant, hence each node links to the central node, turning the network into a star. We have a star configuration each time when the $h_j$ term dominates over $\delta d_{ij}$ in (5.28).

**Random Network δ ≥ N^(1/2)**

For very large $\delta$ the contribution provided by the distance term $\delta d_{ij}$ overwhelms $h_j$ in (5.28). In this case each new node connects to the node closest to it. The resulting network will have a bounded degree distribution, like a random network (Image 5.16b).

**Scale-free Network 4 ≤ δ ≤ N^(1/2)**

Numerical simulations and analytical calculations indicate that for intermediate $\delta$ values the network develops a scale-free topology. The origin of the power law distribution in this regime is rooted in two competing mechanisms:

i) *Optimization*: Each node has a basin of attraction, so that nodes landing in this basin will always link to it. The size of each basin correlates with $h_j$ of node $j$ at its center, which in turn correlates with the node's degree $k_j$ (Image 5.15f).

ii) *Randomness*: We choose randomly the location of the new node, ending in one of the $N$ basins of attraction. The node with the largest degree has largest basin of attraction, hence gains the most new nodes and links. This leads to preferential attachment, as documented in Image 5.16d.

![Scaling in the Optimization Model.](https://networksciencebook.com/images/ch-05/figure-5-16.jpg)

**Image 5.16: Scaling in the Optimization Model**

a) The three network classes generated by the optimization model: star, scale-free, and exponential networks. The topology of the network in the unmarked area is unknown.

The vertical boundary of the star configuration is at $\delta$=(1/2)^(1/2). This is the inverse of the maximum distance between two nodes on a square lattice with unit length, over which the model is defined. Therefore if $\delta$ < (1/2)^(1/2), for any new node $\delta d_{ij}$ < 1 and the cost (5.28) of connecting to the central node is $C_i$ = $\delta d_{ij}$+0, always lower than connecting to any other node at the cost of $f(i,j)$ = $\delta d_{ij}$+1. Therefore for $\delta$ < (1/2)^(1/2) all nodes connect to node 0, resulting in a network dominated by a single hub (starand-spoke network (c)).

The oblique boundary of the scale-free regime is $\delta$ = $N^{1/2}$. Indeed, if nodes are placed randomly on the unit square, then the typical distance between neighbors decreases as $N^{−1/2}$. Hence, if $d_{ij}$~$N^{−1/2}$ then $\delta d_{ij}$ ≥ $h_{ij}$ for most node pairs. Typically the path length to the central node $h_j$ grows slower than $N$ (in small-world networks $h_j$~log $N$, in scale-free networks $h_j$~lnln$N$). Therefore $C_i$ is dominated by the $\delta d_{ij}$ term and the smallest $C_i$ is achieved by minimizing the distance-dependent term. Note that strictly speaking the transition only occurs in the $N$ → ∞ limit. In the white regime we lack an analytical form for the degree distribution.

b) Degree distribution of networks generated in the three phases marked in (a) for $N$=$10^4$.

c) Typical topologies generated by the optimization model for selected $\delta$ values. Node size is proportional to its degree.

d) We used the method described in SECTION 5.6 to measure the preferential attachment function. Starting from a network with $N$=10,000 nodes we added a new node and measured the degree of the node that it connected to. We repeated this procedure 10,000 times, obtaining $\Pi(k)$. The plots document the presence of linear preferential attachment in the scale-free phase, but its absence in the star and the exponential phases.

In summary, we can build models that do not have an explicit $\Pi(k)$ function built into their definition, yet they generate a scale-free network. As we showed in this section, these work by inducing preferential attachment. The mechanism responsible for preferential attachment can have two fundamentally different origins (Image 5.17): it can be rooted in random processes, like link selection or copying, or in optimization, when new nodes balance conflicting criteria as they decide where to connect. Note that each of the mechanisms discussed above lead to linear preferential attachment, as assumed in the Barabási-Albert model. We are not aware of mechanisms capable of generating nonlinear preferential attachment, like those discussed in SECTION 5.7.

The diversity of the mechanisms discussed in this section suggest that linear preferential attachment is present in so many and so different systems precisely because it can come from both rational choice and random actions. Most complex systems are driven by processes that have a bit of both. Hence luck or reason, preferential attachment wins either way.

![Luck or Reason: an Ancient Fight.](https://networksciencebook.com/images/ch-05/figure-5-17.jpg)

**Image 5.17: Luck or Reason: an Ancient Fight**

The tension between randomness and optimization, two apparently antagonistic explanations for power laws, is by no means new: In the 1960s Herbert Simon and Benoit Mandelbrot have engaged in a fierce public dispute over this very topic. Simon proposed that preferential attachment is responsible for the power-law nature of word frequencies. Mandelbrot fiercely defended an optimization-based framework. The debate spanned seven papers and two years and is one of the most vicious scientific disagreement on record.

In the context of networks today the argument titled in Simon's favor: The power laws observed in complex networks appear to be driven by randomness and preferential attachment. Yet, the optimization-based ideas proposed by Mandelbrot play an important role in explaining the origins of preferential attachment. So at the end they were both right.

---

## Section 5.10: Diameter and Clustering Coefficient

To complete the characterization of the Barabási-Albert model we discuss the behavior of the network diameter and the clustering coefficient.

### Diameter

The network diameter, representing the maximum distance in the Barabási-Albert network, follows for $m$ > 1 and large $N$

$$⟨d⟩ \sim \frac{\ln N}{\ln \ln N} \hspace{20 mm} (5.29)$$

Therefore the diameter grows slower than ln $N$, making the distances in the Barabási-Albert model smaller than the distances observed in a random graph of similar size. The difference is particularly relevant for large $N$.

Note that while (5.29) is derived for the diameter, the average distance $⟨d⟩$ scales in a similar fashion. Indeed, as we show in Image 5.18, for small $N$ the ln $N$ term captures the scaling of $⟨d⟩$ with $N$, but for large $N$(≥$10^4$) the impact of the logarithmic correction ln ln $N$ becomes noticeable.

![Average Distance.](https://networksciencebook.com/images/ch-05/figure-5-18.jpg)

**Image 5.18: Average Distance**

The dependence of the average distance on the system size in the Barabási-Albert model. The continuous line corresponds to the exact result (5.29), while the dotted line corresponds to the prediction (3.19) for a random network. The analytical predictions do not provide the exact perfactors, hence the lines are not fits, but indicate only the predicted $N$-dependent trends. The results were averaged for ten independent runs for $m$ = 2.

### Clustering Coefficient

The clustering coefficient of the Barabási-Albert model follows (ADVANCED TOPICS 5.C)

$$⟨C⟩ \sim \frac{(\ln N)^2}{N} \hspace{20 mm} (5.30)$$

The prediction (5.30) is quite different from the 1/$N$ dependence obtained for the random network model (Image 5.19). The difference comes in the (ln$N$)$^2$ term, that increases the clustering coefficient for large $N$. Consequently the Barabási-Albert network is locally more clustered than a random network.

![Clustering Coefficient.](https://networksciencebook.com/images/ch-05/figure-5-19.jpg)

**Image 5.19: Clustering Coefficient**

The dependence of the average clustering coefficient on the system size $N$ for the Barabási-Albert model. The continuous line corresponds to the analytical prediction (5.30), while the dotted line corresponds to the prediction for a random network, for which $⟨C⟩$ ~ 1/$N$. The results are averaged for ten independent runs for $m$ = 2. The dashed and continuous curves are not fits, but are drawn to indicate the predicted $N$ dependent trends.

---

## Section 5.11: Summary

The most important message of the Barabási-Albert model is that network structure and evolution are inseparable. Indeed, in the Erdős-Rényi, Watts-Strogatz, the configuration and the hidden parameter models the role of the modeler is to cleverly place the links between a *fixed number of nodes*. Returning to our earlier analogy, the networks generated by these models relate to real networks like a photo of a painting relates to the painting itself: It may look like the real one, but the process of generating a photo is drastically different from the process of painting the original painting. The aim of the Barabási-Albert model is to capture the processes that assemble a network in the first place. Hence, it aims to paint the painting again, coming as close as possible to the original brush strokes. Consequently, the modeling philosophy behind the model is simple: *to understand the topology of a complex system, we need to describe how it came into being*.

Random networks, the configuration and the hidden parameter models will continue to play an important role as we explore how certain network characteristics deviate from our expectations. Yet, if we want to explain the origin of a particular network property, we will have to use models that capture the system's genesis.

The Barabási-Albert model raises a fundamental question: Is the combination of growth and preferential attachment the real reason why networks are scale-free? We offered a *necessary* and *sufficient* argument to address this question. First, we showed that growth and preferential attachment are jointly needed to generate scale-free networks, hence if one of them is absent, either the scale-free property or stationarity is lost. Second, we showed that if they are both present, they do lead to scale-free networks. This argument leaves one possibility open, however: Do these two mechanisms explain the scale-free nature of *all* networks? Could there be some real networks that are scale-free thanks to some completely different mechanism? The answer is provided in SECTION 5.9, where we did encountered the link selection, the copying and the optimization models that do not have a preferential attachment function built into them, yet they do lead to a scale-free network. We showed that they do so by generating a linear $\Pi(k)$. This finding underscores a more general pattern: To date all known models and real systems that are scale-free have been found to have preferential attachment. Hence the basic mechanisms of the Barabási-Albert model appear to capture the origin of their scale-free topology.

The Barabási-Albert model is unable to describe many characteristics of real systems:

- The model predicts $\gamma$=3 while the degree exponent of real networks varies between 2 and 5 (Table 4.2).
- Many networks, like the WWW or citation networks, are directed, while the model generates undirected networks.
- Many processes observed in networks, from linking to already existing nodes to the disappearance of links and nodes, are absent from the model.
- The model does not allow us to distinguish between nodes based on some intrinsic characteristics, like the novelty of a research paper or the utility of a webpage.
- While the Barabási-Albert model is occasionally used as a model of the Internet or the cell, in reality it is not designed to capture the details of any particular real network. It is a minimal, proof of principle model whose main purpose is to capture the basic mechanisms responsible for the emergence of the scale-free property. Therefore, if we want to understand the evolution of systems like the Internet, the cell or the WWW, we need to incorporate the important details that contribute to the time evolution of these systems, like the directed nature of the WWW, the possibility of internal links and node and link removal.

As we show in CHAPTER 6, these limitations can be systematically resolved.

### Box 5.5: At a Glance: Barabási-Albert Model

**Number of Nodes**

$$N = t$$

**Number of Links**

$$N = mt$$

**Average Degree**

$$⟨k⟩ = 2m$$

**Degree Dynamics**

$$k_i(t) = m(t/t_i)^\beta$$

**Dynamical Exponent**

$$\beta = 1/2$$

**Degree Distribution**

$$p_k \sim k^{-\gamma}$$

**Degree Exponent**

$$\gamma = 3$$

**Average Distance**

$$⟨d⟩ \sim \frac{\ln N}{\ln \ln N}$$

**Clustering Coefficient**

$$⟨C⟩ \sim (\ln N)^2 / N$$

---

## Section 5.12: Homework

1. **Generating Barabási-Albert Networks**

   With the help of a computer, generate a network with $N$ = $10^4$ nodes using the Barabási-Albert model with $m$ = 4. Use as initial condition a fully connected network with $m$ = 4 nodes.

   a) Measure the degree distribution at intermediate steps, namely when the network has $10^2$, $10^3$ and $10^4$ nodes.

   b) Compare the distributions at these intermediate steps by plotting them together and fitting each to a power-law with degree exponent $\gamma$. Do the distributions "converge"?

   c) Plot together the cumulative degree distributions at intermediate steps.

   d) Measure the average clustering coefficient in function of $N$.

   e) Following Image 5.6a, measure the degree dynamics of one of the initial nodes and of the nodes added to the network at time $t$ = 100, $t$ = 1,000 and $t$ = 5,000.

2. **Directed Barabási-Albert Model**

   Consider a variation of the Barabási-Albert model, where at each time step a new node arrives and connects with a directed link to a node chosen with probability

$$\Pi(k_i^{in}) = \frac{k_i^{in} + A}{\sum_j (k_j^{in} + A)}$$

   Here $k_i^{in}$ indicates the in-degree of node $i$ and $A$ is the same constant for all nodes. Each new node has $m$ directed links.

   a) Calculate, using the rate equation approach, the in- and out-degree distribution of the resulting network.

   b) By using the properties of the Gamma and Beta functions, can you find a power-law scaling for the in-degree distribution?

   c) For $A$ = 0 the scaling exponent of the in-degree distribution is different from $\gamma$ = 3, the exponent of the Barabási-Albert model. Why?

3. **Copying Model**

   Use the rate equation approach to show that the directed copying model leads to a scale-free network with incoming degree exponent

$$\gamma_i = \frac{2 - p}{1 - p}$$

4. **Growth Without Preferential Attachment**

   Derive the degree distribution (5.18) of Model A, when a network grows by new nodes connecting randomly to $m$ previously existing nodes. With the help of a computer, generate a network of $10^4$ nodes using Model A. Measure the degree distribution and check that it is consistent with the prediction (5.18).

---

## Section 5.13: Advanced Topic 5.A: Deriving the Degree Distribution

A number of analytical techniques are available to calculate the exact form of the degree exponent (5.11). Next we derive it using the rate equation approach. The method is sufficiently general to help explore the properties of a wide range of growing networks. Consequently, the calculations described here are of direct relevance for many systems, from models pertaining to the WWW to describing the evolution of the protein interaction network via gene duplication.

Let us denote with $N(k,t)$ the number of nodes with degree $k$ at time $t$. The degree distribution $p_k(t)$ relates to this quantity via $p_k(t)$ = $N(k,t)$/$N(t)$. Since at each time-step we add a new node to the network, we have $N = t$. That is, at any moment the total number of nodes equals the number of timesteps (BOX 5.2).

We write preferential attachment as

$$\Pi(k) = \frac{k}{\sum_j k_j} = \frac{k}{2mt} \hspace{20 mm} (5.31)$$

where the 2$m$ term captures the fact that in an undirected network each link contributes to the degree of two nodes. Our goal is to calculate the changes in the number of nodes with degree k after a new node is added to the network. For this we inspect the two events that alter $N(k,t)$ and $p_k(t)$ following the arrival of a new node:

i) A new node can link to a degree-$k$ node, turning it into a degree ($k$+1) node, hence *decreasing N(k,t)*.
ii) A new node can link to a degree ($k$-1) node, turning it into a degree $k$ node, hence *increasing N(k,t)*.

The number of links that are expected to connect to degree $k$ nodes after the arrival of a new node is

$$\frac{k}{2mt} \times Np_k(t) \times m = \frac{k}{2}p_k(t) \hspace{20 mm} (5.32)$$

In (5.32) the first term on the l.h.s. captures the probability that the new node will link to a degree-$k$ node (preferential attachment); the second term provides the total number of nodes with degree $k$, as the more nodes are in this category, the higher the chance that a new node will attach to one of them; the third term is the degree of the incoming node, as the higher is m, the higher is the chance that the new node will link to a degree-$k$ node. We next apply (5.32) to cases (i) and (ii) above:

i) The number of degree $k$ nodes that acquire a new link and turn into ($k$+1) degree nodes is

$$\frac{k}{2}p_k(t) \hspace{20 mm} (5.33)$$

ii) The number of degree ($k$-1) nodes that acquire a new link, increasing their degree to $k$ is

$$\frac{k - 1}{2}p_{k-1}(t) \hspace{20 mm} (5.34)$$

Combining (5.33) and (5.34) we obtain the expected number of degree-$k$ nodes after the addition of a new node

$$(N + 1)p_k(t + 1) = Np_k(t) + \frac{k - 1}{2}p_{k-1}(t) - \frac{k}{2}p_k(t) \hspace{20 mm} (5.35)$$

This equation applies to all nodes with degree $k$ > $m$. As we lack nodes with degree $k$=0,1, ... , $m$-1 in the network (each new node arrives with degree $m$) we need a separate equation for degree-$m$ modes. Following the same arguments we used to derive (5.35), we obtain

$$(N + 1)p_m(t + 1) = Np_m(t) + 1 - \frac{m}{2}p_m(t) \hspace{20 mm} (5.36)$$

Equations (5.35) and (5.36) are the starting point of the recursive process that provides $p_k$. Let us use the fact that we are looking for a stationary degree distribution, an expectation supported by numerical simulations (Image 5.6). This means that in the $N = t$ → ∞ limit, $p_k(\infty)$ = $p_k$. Using this we can write the l.h.s. of (5.35) and (5.36) as

$$(N + 1)p_k(t + 1) - Np_k(t) \to Np_k(\infty) + p_k(\infty) - Np_k(\infty) = p_k(\infty) = p_k,$$

$$(N + 1)p_m(t + 1) - Np_m(t) \to p_m$$

Therefore the rate equations (5.35) and (5.36) take the form:

$$p_k = \frac{k - 1}{k + 2}p_{k-1} \quad k > m \hspace{20 mm} (5.37)$$

$$p_m = \frac{2}{m + 2} \hspace{20 mm} (5.38)$$

Note that (5.37) can be rewritten as

$$p_{k+1} = \frac{k}{k + 3}p_k \hspace{20 mm} (5.39)$$

via a $k \to k+1$ variable change.

We use a recursive approach to obtain the degree distribution. That is, we write the degree distribution for the smallest degree, $k$=$m$, using (5.38) and then use (5.39) to calculate $p_k$ for the higher degrees:

$$\begin{array}{l}
p_{m + 1} = \frac{m}{m + 3}p_m = \frac{2m}{(m + 2)(m + 3)} \\
p_{m + 2} = \frac{m + 1}{m + 4}p_{m + 1} = \frac{2m(m + 1)}{(m + 2)(m + 3)(m + 4)} \\
p_{m + 3} = \frac{m + 2}{m + 5}p_{m + 2} = \frac{2m(m + 1)}{(m + 3)(m + 4)(m + 5)} \\
\end{array} \hspace{20 mm} (5.40)$$

At this point we notice a simple recursive pattern: By replacing in the denomerator $m$+3 with k we obtain the probability to observe a node with degree $k$

$$p_k = \frac{2m(m + 1)}{k(k + 1)(k + 2)} \hspace{20 mm} (5.41)$$

which represents the exact form of the degree distribution of the Barabási-Albert model.

Note that:

- For large k (5.41) becomes $p_k$ ~ $k^{-3}$, in agreement with the numerical result.
- The prefactor of (5.11) or (5.41) is different from the prefactor of (5.9).
- This form was derived independently in [12] and [13], and the exact mathematical proof of its validity is provided in [10].

Finally, the rate equation formalism offers an elegant continuum equation satisfied by the degree distribution. Starting from the equation

$$p_k = \frac{k - 1}{2}p_{k-1} - \frac{k}{2}p_k \hspace{20 mm} (5.42)$$

we can write

$$2p_k = (k - 1)p_{k-1} - kp_k = -p_{k-1} - k[p_k - p_{k-1}] \hspace{20 mm} (5.43)$$

$$2p_k = -p_{k-1} - k\frac{p_k - p_{k-1}}{k - (k - 1)} \approx -p_{k-1} - k\frac{\partial p_k}{\partial k} \hspace{20 mm} (5.44)$$

obtaining

$$p_k = -\frac{1}{2}\frac{\partial[kp_k]}{\partial k} \hspace{20 mm} (5.45)$$

One can check that the solution of (5.45) is

$$p_k \sim k^{-3} \hspace{20 mm} (5.46)$$

---

## Section 5.14: Advanced Topic 5.B: Nonlinear Preferential Attachment

In this section we derive the degree distribution of the nonlinear Barabási-Albert model, governed by the preferential attachment (5.22). We follow Ref. [13], but we adjust the calculation to cover $m$ > 1.

Strictly speaking a stationary degree distribution only exists if $\alpha$ ≤ 1 in (5.22). For $\alpha$ > 1 a few nodes attract a finite fraction of links, as explained in SECTION 5.7, and we do not have a time-independent $p_k$. Therefore we limit ourself to the $\alpha$ ≤ 1 case.

We start with the nonlinear Barabási-Albert model, in which at each time step a new node is added with $m$ new links. We connect each new link to an existing node with probability

$$\Pi(k_i) = \frac{k_i^\alpha}{M(\alpha, t)} \hspace{20 mm} (5.47)$$

where $k_i$ is the degree of node $i$, 0 < $\alpha$ ≤ 1 and

$$M(\alpha, t) = t\sum_k k^\alpha p_k(t) = t\mu(\alpha, t) \hspace{20 mm} (5.48)$$

is the normalization factor and $t$=$N(t)$ represents the number of nodes. Note that $\mu$(0, $t$)= $\sum p_k(t)$ =1 and $\mu$(1, $t$) =$\sum_k kp_k(t)$ =$⟨k⟩$=2$mt$/$N$ is the average degree. Since 0 < $\alpha$ ≤ 1,

$$\mu(0, t) \le \mu(\alpha, t) \le \mu(1, t) \hspace{20 mm} (5.49)$$

Therefore in the long time limit

$$\mu(\alpha, t \to \infty) = \text{constant} \hspace{20 mm} (5.50)$$

whose precise value will be calculated later. For simplicity, we adopt the notation $\mu$ ≡ $\mu(\alpha, t$ → ∞)

Following the rate equation approach introduced in ADVANCED TOPICS 5.A, we write the rate equation for the network's degree distribution as

$$(t + 1)p_k(t + 1) = tp_k(t) + \frac{m}{\mu(\alpha, t)}[(k - 1)^\alpha p_{k-1}(t) - k^\alpha p_k(t)] + \delta_{k,m} \hspace{20 mm} (5.51)$$

The first term on the r.h.s. describes the rate at which
# Chapter 3: Random Networks

## Section 3.1: Introduction

Imagine organizing a party for a hundred guests who initially do not know each other. Offer them wine and cheese and you will soon see them chatting in groups of two to three. Now mention to Mary, one of your guests, that the red wine in the unlabeled dark green bottles is a rare vintage, much better than the one with the fancy red label. If she shares this information only with her acquaintances, your expensive wine appears to be safe, as she only had time to meet a few others so far.

The guests will continue to mingle, however, creating subtle paths between individuals that may still be strangers to each other. For example, while John has not yet met Mary, they have both met Mike, so there is an invisible path from John to Mary through Mike. As time goes on, the guests will be increasingly interwoven by such elusive links. With that the secret of the unlabeled bottle will pass from Mary to Mike and from Mike to John, escaping into a rapidly expanding group.

To be sure, when all guests had gotten to know each other, everyone would be pouring the superior wine. But if each encounter took only ten minutes, meeting all ninety-nine others would take about sixteen hours. Thus, you could reasonably hope that a few drops of your fine wine would be left for you to enjoy once the guests are gone.

Yet, you would be wrong. In this chapter we show you why. We will see that the party maps into a classic model in network science called the random network model. And random network theory tells us that we do not have to wait until all individuals get to know each other for our expensive wine to be in danger. Rather, soon after each person meets at least one other guest, an invisible network will emerge that will allow the information to reach all of them. Hence in no time everyone will be enjoying the better wine.

![From a Cocktail Party to Random Networks.](https://networksciencebook.com/images/ch-03/figure-3-1.jpg)

**Image 3.1: From a Cocktail Party to Random Networks**

The emergence of an acquaintance network through random encounters at a cocktail party.

(a) Early on the guests form isolated groups.
(b) As individuals mingle, changing groups, an invisible network emerges that connects all of them into a single network.

---

## Section 3.2: The Random Network Model

Network science aims to build models that reproduce the properties of real networks. Most networks we encounter do not have the comforting regularity of a crystal lattice or the predictable radial architecture of a spider web. Rather, at first inspection they look as if they were spun randomly. Random network theory embraces this apparent randomness by constructing and characterizing networks that are *truly random*.

From a modeling perspective a network is a relatively simple object, consisting of only nodes and links. The real challenge, however, is to decide where to place the links between the nodes so that we reproduce the complexity of a real system. In this respect the philosophy behind a random network is simple: We assume that this goal is best achieved by placing the links randomly between the nodes. That takes us to the definition of a random network (BOX 3.1):

*A random network consists of N nodes where each node pair is connected with probability p.*

### Box 3.1: Defining Random Networks

There are two definitions of a random network:

- *G(N, L)* Model: N labeled nodes are connected with *L* randomly placed links. Erdős and Rényi used this definition in their string of papers on random networks.
  
- *G(N, p)* Model: Each pair of N labeled nodes is connected with probability *p*, a model introduced by Gilbert.

Hence, the *G(N, p)* model fixes the probability *p* that two nodes are connected and the *G(N, L)* model fixes the total number of links *L*. While in the *G(N, L)* model the average degree of a node is simply $\langle k \rangle = 2L/N$, other network characteristics are easier to calculate in the *G(N, p)* model. Throughout this book we will explore the *G(N, p)* model, not only for the ease that it allows us to calculate key network characteristics, but also because in real networks the number of links rarely stays fixed.

To construct a random network we follow these steps:

1. Start with *N* isolated nodes.
2. Select a node pair and generate a random number between 0 and 1. If the number exceeds *p*, connect the selected node pair with a link, otherwise leave them disconnected.
3. Repeat step (2) for each of the $N(N-1)/2$ node pairs.

The network obtained after this procedure is called a *random graph* or a *random network*. Two mathematicians, Pál Erdős and Alfréd Rényi, have played an important role in understanding the properties of these networks. In their honor a random network is called the *Erdős-Rényi network* (BOX 3.2).

### Box 3.2: Random Networks: a Brief History

![Pál Erdős and Alfréd Rényi](https://networksciencebook.com/images/ch-03/figure-3-2.jpg)

**Image 3.2:**

**(a) Pál Erdős (1913-1996)**

Hungarian mathematician known for both his exceptional scientific output and eccentricity. Indeed, Erdős published more papers than any other mathematician in the history of mathematics. He co-authored papers with over five hundred mathematicians, inspiring the concept of *Erdős number*. His legendary personality and profound professional impact has inspired two biographies and a documentary.

**(b) Alfréd Rényi (1921-1970)**

Hungarian mathematician with fundamental contributions to combinatorics, graph theory, and number theory. His impact goes beyond mathematics: The Rényi entropy is widely used in chaos theory and the random network theory he co-developed is at the heart of network science. He is remembered through the hotbed of Hungarian mathematics, the Alfréd Rényi Institute of Mathematics in Budapest.

Anatol Rapoport (1911-2007), a Russian immigrant to the United States, was the first to study random networks. Rapoport's interests turned to mathematics after realizing that a successful career as a concert pianist would require a wealthy patron. He focused on mathematical biology at a time when mathematicians and biologists hardly spoke to each other. In a paper written with Ray Solomonoff in 1951, Rapoport demonstrated that if we increase the average degree of a network, we observe an abrupt transition from disconnected nodes to a graph with a giant component.

The study of random networks reached prominence thanks to the fundamental work of Pál Erdős and Alfréd Rényi. In a sequence of eight papers published between 1959 and 1968, they merged probability theory and combinatorics with graph theory, establishing *random graph theory*, a new branch of mathematics.

The random network model was independently introduced by Edgar Nelson Gilbert (1923-2013) the same year Erdős and Rényi published their first paper on the subject. Yet, the impact of Erdős and Rényi's work is so overwhelming that they are rightly considered the founders of random graph theory.

*"A mathematician is a device for turning coffee into theorems"*

*Alfréd Rényi (a quote often attributed to Erdős)*

---

## Section 3.3: Number of Links

Each random network generated with the same parameters *N*, *p* looks slightly different. Not only the detailed wiring diagram changes between realizations, but so does the number of links *L*. It is useful, therefore, to determine how many links we expect for a particular realization of a random network with fixed *N* and *p*.

The probability that a random network has exactly *L* links is the product of three terms:

1. The probability that L of the attempts to connect the $N(N-1)/2$ pairs of nodes have resulted in a link, which is $p^L$.
2. The probability that the remaining $N(N-1)/2 - L$ attempts have not resulted in a link, which is $(1-p)^{N(N-1)/2-L}$.
3. A combinational factor,

$$\left( {\begin{array}{*{20}c} {\frac{{N(N - 1)}}{2}}  \\ L  \\ \end{array}} \right)$$

counting the number of different ways we can place *L* links among $N(N-1)/2$ node pairs.

We can therefore write the probability that a particular realization of a random network has exactly *L* links as

$$p_L  = \left( {\begin{array}{*{20}c} {\frac{{N(N - 1)}}{2}}  \\ L  \\ \end{array}} \right)p^L (1 - p)^{\frac{{N(N - 1)}}{2} - L} \quad (3.1)$$

As (3.1) is a binomial distribution (BOX 3.3), the expected number of links in a random graph is

$$\langle L \rangle  = \sum\limits_{L = 0}^{\frac{{N(N - 1)}}{2}} {Lp_L }  = p\frac{{N(N - 1)}}{2} \quad (3.2)$$

Hence $\langle L \rangle$ is the product of the probability *p* that two nodes are connected and the number of pairs we attempt to connect, which is $L_{\text{max}} = N(N-1)/2$.

Using (3.2) we obtain the average degree of a random network

$$\langle k \rangle  = \frac{{2\langle L \rangle }}{N} = p(N - 1) \quad (3.3)$$

Hence $\langle k \rangle$ is the product of the probability *p* that two nodes are connected and $(N-1)$, which is the maximum number of links a node can have in a network of size *N*.

In summary the number of links in a random network varies between realizations. Its expected value is determined by *N* and *p*. If we increase *p* a random network becomes denser: The average number of links increase linearly from $\langle L \rangle = 0$ to $L_{\text{max}}$ and the average degree of a node increases from $\langle k \rangle = 0$ to $\langle k \rangle = N-1$.

![Random Networks are Truly Random.](https://networksciencebook.com/images/ch-03/figure-3-3.jpg)

**Image 3.3: Random Networks are Truly Random**

Top Row: Three realizations of a random network generated with the same parameters $p=1/6$ and $N=12$. Despite the identical parameters, the networks not only look different, but they have a different number of links as well ($L=10, 10, 8$).

Bottom Row: Three realizations of a random network with $p=0.03$ and $N=100$. Several nodes have degree $k=0$, shown as isolated nodes at the bottom.

### Box 3.3: Binomial Distribution: Mean and Variance

If we toss a fair coin *N* times, tails and heads occur with the same probability $p = 1/2$. The binomial distribution provides the probability $p_x$ that we obtain exactly *x* heads in a sequence of *N* throws. In general, the binomial distribution describes the number of successes in *N* independent experiments with two possible outcomes, in which the probability of one outcome is *p*, and of the other is $1-p$.

The binomial distribution has the form

$$p_x  = \left( {\begin{array}{*{20}c} N  \\ x  \\ \end{array}} \right)p^x (1 - p)^{N - x}$$

The mean of the distribution (first moment) is

$$\langle x \rangle  = \sum\limits_{x = 0}^N {xp_x }  = Np \quad (3.4)$$

Its second moment is

$$\langle {x^2 } \rangle  = \sum\limits_{x = 0}^N {x^2 p_x }  = p(1 - p)N + p^2 N^2 \quad (3.5)$$

providing its standard deviation as

$$\sigma _x  = \left( {\langle {x^2 } \rangle  - \langle x \rangle ^2 } \right)^{\frac{1}{2}}  = \left[ {p(1 - p)N} \right]^{\frac{1}{2}} \quad (3.6)$$

Equations (3.4) - (3.6) are used repeatedly as we characterize random networks.

---

## Section 3.4: Degree Distribution

In a given realization of a random network some nodes gain numerous links, while others acquire only a few or no links. These differences are captured by the degree distribution, $p_k$, which is the probability that a randomly chosen node has degree *k*. In this section we derive $p_k$ for a random network and discuss its properties.

![Binomial vs. Poisson Degree Distribution.](https://networksciencebook.com/images/ch-03/figure-3-4.jpg)

**Image 3.4: Binomial vs. Poisson Degree Distribution**

The exact form of the degree distribution of a random network is the binomial distribution (left half). For $N \gg \langle k \rangle$ the binomial is well approximated by a Poisson distribution (right half). As both formulas describe the same distribution, they have the identical properties, but they are expressed in terms of different parameters: The binomial distribution depends on *p* and *N*, while the Poisson distribution has only one parameter, $\langle k \rangle$. It is this simplicity that makes the Poisson form preferred in calculations.

### Binomial Distribution

In a random network the probability that node *i* has exactly *k* links is the product of three terms:

- The probability that *k* of its links are present, or $p^k$.
- The probability that the remaining $(N-1-k)$ links are missing, or $(1-p)^{N-1-k}$
- The number of ways we can select *k* links from $N-1$ potential links a node can have, or

$$\left( {\begin{array}{*{20}c} {N - 1}  \\ k  \\ \end{array}} \right)$$

Consequently the degree distribution of a random network follows the binomial distribution

$$p_k  = \left( {\begin{array}{*{20}c} {N - 1}  \\ k  \\ \end{array}} \right)p^k (1 - p)^{N - 1 - k} \quad (3.7)$$

The shape of this distribution depends on the system size *N* and the probability *p*. The binomial distribution (BOX 3.3) allows us to calculate the network's average degree $\langle k \rangle$, recovering (3.3), as well as its second moment $\langle k^2 \rangle$ and variance $\sigma_k$.

### Poisson Distribution

Most real networks are sparse, meaning that for them $\langle k \rangle \ll N$. In this limit the degree distribution (3.7) is well approximated by the Poisson distribution (ADVANCED TOPICS 3.A)

$$p_k  = e^{ - \langle k \rangle } \frac{{\langle k \rangle ^k }}{{k!}} \quad (3.8)$$

which is often called, together with (3.7), the *degree distribution of a random network*.

The binomial and the Poisson distribution describe the same quantity, hence they have similar properties:

- Both distributions have a peak around $\langle k \rangle$. If we increase *p* the network becomes denser, increasing $\langle k \rangle$ and moving the peak to the right.
- The width of the distribution (dispersion) is also controlled by *p* or $\langle k \rangle$. The denser the network, the wider is the distribution, hence the larger are the differences in the degrees.

When we use the Poisson form (3.8), we need to keep in mind that:

- The exact result for the degree distribution is the binomial form (3.7), thus (3.8) represents only an approximation to (3.7) valid in the $\langle k \rangle \ll N$ limit. As most networks of practical importance are sparse, this condition is typically satisfied.
- The advantage of the Poisson form is that key network characteristics, like $\langle k \rangle$, $\langle k^2 \rangle$ and $\sigma_k$, have a much simpler form, depending on a single parameter, $\langle k \rangle$.
- The Poisson distribution in (3.8) does not explicitly depend on the number of nodes *N*. Therefore, (3.8) predicts that the degree distribution of networks of different sizes but the same average degree $\langle k \rangle$ are indistinguishable from each other.

In summary, while the Poisson distribution is only an approximation to the degree distribution of a random network, thanks to its analytical simplicity, it is the preferred form for $p_k$. Hence throughout this book, unless noted otherwise, we will refer to the Poisson form (3.8) as the degree distribution of a random network. Its key feature is that its properties are independent of the network size and depend on a single parameter, the average degree $\langle k \rangle$.

![Degree Distribution is Independent of the Network Size.](https://networksciencebook.com/images/ch-03/figure-3-5.jpg)

**Image 3.5: Degree Distribution is Independent of the Network Size**

The degree distribution of a random network with $\langle k \rangle = 50$ and $N = 10^2, 10^3, 10^4$.

**Small Networks: Binomial** 
For a small network ($N = 10^2$) the degree distribution deviates significantly from the Poisson form (3.8), as the condition for the Poisson approximation, $N \gg \langle k \rangle$, is not satisfied. Hence for small networks one needs to use the exact binomial form (3.7) (green line).

**Large Networks: Poisson** 
For larger networks ($N = 10^3, 10^4$) the degree distribution becomes indistinguishable from the Poisson prediction (3.8), shown as a continuous grey line. Therefore for large *N* the degree distribution is independent of the network size. In the figure we averaged over 1,000 independently generated random networks to decrease the noise.

---

## Section 3.5: Real Networks are Not Poisson

As the degree of a node in a random network can vary between 0 and $N-1$, we must ask, how big are the differences between the node degrees in a particular realization of a random network? That is, can high degree nodes coexist with small degree nodes? We address these questions by estimating the size of the largest and the smallest node in a random network.

Let us assume that the world's social network is described by the random network model. This random society may not be as far fetched as it first sounds: There is significant randomness in whom we meet and whom we choose to become acquainted with.

Sociologists estimate that a typical person knows about 1,000 individuals on a first name basis, prompting us to assume that $\langle k \rangle \approx 1,000$. Using the results obtained so far about random networks, we arrive to a number of intriguing conclusions about a random society of $N \approx 7 \times 10^9$ of individuals (ADVANCED TOPICS 3.B):

- The most connected individual (the largest degree node) in a random society is expected to have $k_{\text{max}} = 1,185$ acquaintances.
- The degree of the least connected individual is $k_{\text{min}} = 816$, not that different from $k_{\text{max}}$ or $\langle k \rangle$.
- The dispersion of a random network is $\sigma_k = \sqrt{\langle k \rangle}$, which for $\langle k \rangle = 1,000$ is $\sigma_k = 31.62$. This means that the number of friends a typical individual has is in the $\langle k \rangle \pm \sigma_k$ range, or between 968 and 1,032, a rather narrow window.

Taken together, in a random society all individuals are expected to have a comparable number of friends. Hence if people are randomly connected to each other, we lack outliers: There are no highly popular individuals, and no one is left behind, having only a few friends. This surprising conclusion is a consequence of an important property of random networks: *in a large random network the degree of most nodes is in the narrow vicinity of* $\langle k \rangle$.

This prediction blatantly conflicts with reality. Indeed, there is extensive evidence of individuals who have considerably more than 1,185 acquaintances. For example, US president Franklin Delano Roosevelt's appointment book has about 22,000 names, individuals he met personally. Similarly, a study of the social network behind Facebook has documented numerous individuals with 5,000 Facebook friends, the maximum allowed by the social networking platform. To understand the origin of these discrepancies we must compare the degree distribution of real and random networks.

### Box 3.4: Why are Hubs Missing?

We first note that the $1/k!$ term in (3.8) significantly decreases the chances of observing large degree nodes. Indeed, the Stirling approximation

$$k! \sim \left[ {\sqrt {2\pi k} } \right]\left( {\frac{k}{e}} \right)^k$$

allows us rewrite (3.8) as

$$p_k  = \frac{{e^{ - \langle k \rangle } }}{{\sqrt {2\pi k} }}\left( {\frac{{e\langle k \rangle }}{k}} \right)^k \quad (3.9)$$

For degrees $k \gg e\langle k \rangle$ the term in the parenthesis is smaller than one, hence for large *k* both $k$-dependent terms in (3.9), i.e. $1/\sqrt{k}$ and $(e\langle k \rangle/k)^k$ decrease rapidly with increasing *k*. Overall (3.9) predicts that in a random network the chance of observing a hub decreases faster than exponentially.

![Degree Distribution of Real Networks.](https://networksciencebook.com/images/ch-03/figure-3-6.jpg)

**Image 3.6: Degree Distribution of Real Networks**

The degree distribution of the (a) Internet, (b) science collaboration network, and (c) protein interaction network. The green line corresponds to the Poisson prediction, obtained by measuring $\langle k \rangle$ for the real network and then plotting (3.8). The significant deviation between the data and the Poisson fit indicates that the random network model underestimates the size and the frequency of the high degree nodes, as well as the number of low degree nodes. Instead the random network model predicts a larger number of nodes in the vicinity of $\langle k \rangle$ than seen in real networks.

---

## Section 3.6: The Evolution of a Random Network

The cocktail party we encountered at the beginning of this chapter captures a dynamical process: Starting with *N* isolated nodes, the links are added gradually through random encounters between the guests. This corresponds to a gradual increase of *p*, with striking consequences on the network topology. To quantify this process, we first inspect how the size of the largest connected cluster within the network, $N_G$, varies with $\langle k \rangle$. Two extreme cases are easy to understand:

- For $p = 0$ we have $\langle k \rangle = 0$, hence all nodes are isolated. Therefore the largest component has size $N_G = 1$ and $N_G/N \to 0$ for large *N*.
- For $p = 1$ we have $\langle k \rangle = N-1$, hence the network is a complete graph and all nodes belong to a single component. Therefore $N_G = N$ and $N_G/N = 1$.

One would expect that the largest component grows gradually from $N_G = 1$ to $N_G = N$ if $\langle k \rangle$ increases from 0 to $N-1$. Yet, as Image 3.7a indicates, this is not the case: $N_G/N$ remains zero for small $\langle k \rangle$, indicating the lack of a large cluster. Once $\langle k \rangle$ exceeds a critical value, $N_G/N$ increases, signaling the rapid emergence of a large cluster that we call the *giant component*. Erdős and Rényi in their classical 1959 paper predicted that the condition for the emergence of the giant component is

$$\langle k \rangle  = 1 \quad (3.10)$$

In other words, we have a giant component if and only if each node has on average more than one link (ADVANCED TOPICS 3.C).

The fact that we need at least one link per node to observe a giant component is not unexpected. Indeed, for a giant component to exist, each of its nodes must be linked to at least one other node. It is somewhat counterintuitive, however, that one link is *sufficient* for its emergence.

We can express (3.10) in terms of *p* using (3.3), obtaining

$$p_c  = \frac{1}{{N - 1}} \approx \frac{1}{N} \quad (3.11)$$

Therefore the larger a network, the smaller *p* is sufficient for the giant component.

The emergence of the giant component is only one of the transitions characterizing a random network as we change $\langle k \rangle$. We can distinguish four topologically distinct regimes, each with its unique characteristics:

### Subcritical Regime: $0 \leq \langle k \rangle \lesssim 1$ ($p \lesssim 1/N$)

For $\langle k \rangle = 0$ the network consists of *N* isolated nodes. Increasing $\langle k \rangle$ means that we are adding $N\langle k \rangle = pN(N-1)/2$ links to the network. Yet, given that $\langle k \rangle \lesssim 1$, we have only a small number of links in this regime, hence we mainly observe tiny clusters.

We can designate at any moment the largest cluster to be the giant component. Yet in this regime the relative size of the largest cluster, $N_G/N$, remains zero. The reason is that for $\langle k \rangle \lesssim 1$ the largest cluster is a tree with size $N_G \sim \ln N$, hence its size increases much slower than the size of the network. Therefore $N_G/N \approx \ln N / N \to 0$ in the $N \to \infty$ limit.

In summary, in the subcritical regime the network consists of numerous tiny components, whose size follows the exponential distribution (3.35). Hence these components have comparable sizes, lacking a clear winner that we could designate as a giant component.

### Critical Point: $\langle k \rangle = 1$ ($p = 1/N$)

The critical point separates the regime where there is not yet a giant component ($\langle k \rangle \lesssim 1$) from the regime where there is one ($\langle k \rangle \gtrsim 1$). At this point the relative size of the largest component is still zero. Indeed, the size of the largest component is $N_G \sim N^{2/3}$. Consequently $N_G$ grows much slower than the network's size, so its relative size decreases as $N_G/N \sim N^{-1/3}$ in the $N \to \infty$ limit.

Note, however, that in absolute terms there is a significant jump in the size of the largest component at $\langle k \rangle = 1$. For example, for a random network with $N = 7 \times 10^9$ nodes, comparable to the globe's social network, for $\langle k \rangle \lesssim 1$ the largest cluster is of the order of $N_G \approx \ln N = \ln (7 \times 10^9) \approx 22.7$. In contrast at $\langle k \rangle = 1$ we expect $N_G \sim N^{2/3} = (7 \times 10^9)^{2/3} \approx 3 \times 10^6$, a jump of about five orders of magnitude. Yet, both in the subcritical regime and at the critical point the largest component contains only a vanishing fraction of the total number of nodes in the network.

In summary, at the critical point most nodes are located in numerous small components, whose size distribution follows (3.36). The power law form indicates that components of rather different sizes coexist. These numerous small components are mainly trees, while the giant component may contain loops. Note that many properties of the network at the critical point resemble the properties of a physical system undergoing a phase transition (ADVANCED TOPICS 3.F).

![Evolution of a Random Network.](https://networksciencebook.com/images/ch-03/figure-3-7.jpg)

**Image 3.7: Evolution of a Random Network**

(a) The relative size of the giant component in function of the average degree $\langle k \rangle$ in the Erdős-Rényi model. The figure illustrates the phase transition at $\langle k \rangle = 1$, responsible for the emergence of a giant component with nonzero $N_G$.

(b) A sample network and its properties in the four regimes that characterize a random network.

### Supercritical Regime: $\langle k \rangle \gtrsim 1$ ($p \gtrsim 1/N$)

This regime has the most relevance to real systems, as for the first time we have a giant component that looks like a network. In the vicinity of the critical point the size of the giant component varies as

$$\frac{{N_G }}{N} \sim \langle k \rangle  - 1 \quad (3.12)$$

or

$$N_G  \sim (p - p_c )N \quad (3.13)$$

where $p_c$ is given by (3.11). In other words, the giant component contains a finite fraction of the nodes. The further we move from the critical point, a larger fraction of nodes will belong to it. Note that (3.12) is valid only in the vicinity of $\langle k \rangle = 1$. For large $\langle k \rangle$ the dependence between $N_G$ and $\langle k \rangle$ is nonlinear.

In summary in the supercritical regime numerous isolated components coexist with the giant component, their size distribution following (3.35). These small components are trees, while the giant component contains loops and cycles. The supercritical regime lasts until all nodes are absorbed by the giant component.

### Connected Regime: $\langle k \rangle \gtrsim \ln N$ ($p \gtrsim \ln N / N$)

For sufficiently large *p* the giant component absorbs all nodes and components, hence $N_G \approx N$. In the absence of isolated nodes the network becomes connected. The average degree at which this happens depends on *N* as (ADVANCED TOPIC 3.E)

$$\langle k \rangle  = \ln N \quad (3.14)$$

Note that when we enter the connected regime the network is still relatively sparse, as $\ln N / N \to 0$ for large *N*. The network turns into a complete graph only at $\langle k \rangle = N - 1$.

In summary, the random network model predicts that the emergence of a network is not a smooth, gradual process: The isolated nodes and tiny components observed for small $\langle k \rangle$ collapse into a giant component through a phase transition (ADVANCED TOPICS 3.F). As we vary $\langle k \rangle$ we encounter four topologically distinct regimes.

The discussion offered above follows an empirical perspective, fruitful if we wish to compare a random network to real systems. A different perspective, with its own rich behavior, is offered by the mathematical literature (BOX 3.5).

### Box 3.5: Network Evolution in Graph Theory

In the random graph literature it is often assumed that the connection probability $p(N)$ scales as $N^z$, where *z* is a tunable parameter between $-\infty$ and 0. In this language Erdős and Rényi discovered that as we vary *z*, key properties of random graphs appear quite suddenly.

A graph has a given property *Q* if the probability of having *Q* approaches 1 as $N \to \infty$. That is, for a given *z* either almost every graph has the property *Q* or almost no graph has it. For example, for *z* less than -3/2 almost all graphs contain only isolated nodes and pairs of nodes connected by a link. Once *z* exceeds -3/2, most networks will contain paths connecting three or more nodes.

![Evolution of a Random Graph.](https://networksciencebook.com/images/ch-03/figure-3-8.jpg)

**Image 3.8: Evolution of a Random Graph**

The threshold probabilities at which different subgraphs appear in a random graph, as defined by the exponent *z* in the $p(N) \sim N^z$ relationship. For $z \lesssim -3/2$ the graph consists of isolated nodes and edges. When *z* passes -3/2 trees of order 3 appear, while at $z = -4/3$ trees of order 4 appear. At $z = 1$ trees of all orders are present, together with cycles of all orders. Complete subgraphs of order 4 appear at $z = -2/3$, and as *z* increases further, complete subgraphs of larger and larger order emerge.

---

## Section 3.7: Real Networks are Supercritical

Two predictions of random network theory are of direct importance for real networks:

1. Once the average degree exceeds $\langle k \rangle = 1$, a giant component should emerge that contains a finite fraction of all nodes. Hence only for $\langle k \rangle \gtrsim 1$ the nodes organize themselves into a recognizable network.
2. For $\langle k \rangle \gtrsim \ln N$ all components are absorbed by the giant component, resulting in a single connected network.

Do real networks satisfy the criteria for the existence of a giant component, i.e. $\langle k \rangle \gtrsim 1$? And will this giant component contain all nodes for $\langle k \rangle \gtrsim \ln N$, or will we continue to see some disconnected nodes and components? To answer these questions we compare the structure of a real network for a given $\langle k \rangle$ with the theoretical predictions discussed above.

The measurements indicate that real networks extravagantly exceed the $\langle k \rangle = 1$ threshold. Indeed, sociologists estimate that an average person has around 1,000 acquaintances; a typical neuron is the human brain has about 7,000 synapses; in our cells each molecule takes part in several chemical reactions.

This conclusion is supported by Table 3.1, that lists the average degree of several undirected networks, in each case finding $\langle k \rangle \gtrsim 1$. Hence the average degree of real networks is well beyond the $\langle k \rangle = 1$ threshold, implying that they all have a giant component. The same is true for the reference networks listed in Table 3.1.

| Network | N | L | $\langle k \rangle$ | ln N |
|---------|---|---|---|---|
| Internet | 192,244 | 609,066 | 6.34 | 12.17 |
| Power Grid | 4,941 | 6,594 | 2.67 | 8.51 |
| Science Collaboration | 23,133 | 94,437 | 8.08 | 10.05 |
| Actor Network | 702,388 | 29,397,908 | 83.71 | 13.46 |
| Protein Interactions | 2,018 | 2,930 | 2.90 | 7.61 |

**Table 3.1: Are Real Networks Connected?**

The number of nodes *N* and links *L* for the undirected networks of our reference network list, shown together with $\langle k \rangle$ and ln *N*. A giant component is expected for $\langle k \rangle \gtrsim 1$ and all nodes should join the giant component for $\langle k \rangle \gtrsim \ln N$. While for all networks $\langle k \rangle \gtrsim 1$, for most $\langle k \rangle$ is under the ln N threshold.

Let us now turn to the second prediction, inspecting if we have single component (i.e. if $\langle k \rangle \gtrsim \ln N$), or if the network is fragmented into multiple components (i.e. if $\langle k \rangle \lesssim \ln N$). For social networks the transition between the supercritical and the fully connected regime should be at $\langle k \rangle \gtrsim \ln(7 \times 10^9) \approx 22.7$. That is, if the average individual has more than two dozens acquaintances, then a random society must have a single component, leaving no individual disconnected. With $\langle k \rangle \approx 1,000$ this condition is clearly satisfied. Yet, according to Table 3.1 many real networks do not obey the fully connected criteria. Consequently, according to random network theory these networks should be fragmented into several disconnected components. This is a disconcerting prediction for the Internet, indicating that some routers should be disconnected from the giant component, being unable to communicate with other routers. It is equally problematic for the power grid, indicating that some consumers should not get power. These predictions are clearly at odds with reality.

In summary, we find that most real networks are in the supercritical regime. Therefore these networks are expected to have a giant component, which is in agreement with the observations. Yet, this giant component should coexist with many disconnected components, a prediction that fails for several real networks. Note that these predictions should be valid only if real networks are accurately described by the Erdős-Rényi model, i.e. if real networks are random. In the coming chapters, as we learn more about the structure of real networks, we will understand why real networks can stay connected despite failing the $\langle k \rangle \gtrsim \ln N$ criteria.

![Most Real Networks are Supercritical.](https://networksciencebook.com/images/ch-03/figure-3-9.jpg)

**Image 3.9: Most Real Networks are Supercritical**

The four regimes predicted by random network theory, marking with a cross the location ($\langle k \rangle$) of the undirected networks listed in Table 3.1. The diagram indicates that most networks are in the supercritical regime, hence they are expected to be broken into numerous isolated components. Only the actor network is in the connected regime, meaning that all nodes are part of a single giant component. Note that while the boundary between the subcritical and the supercritical regime is always at $\langle k \rangle = 1$, the boundary between the supercritical and the connected regime is at ln N, which varies from system to system.

---

## Section 3.8: Small Worlds

The *small world phenomenon*, also known as *six degrees of separation*, has long fascinated the general public. It states that if you choose any two individuals anywhere on Earth, you will find a path of at most six acquaintances between them. The fact that individuals who live in the same city are only a few handshakes from each other is by no means surprising. The small world concept states, however, that even individuals who are on the opposite side of the globe can be connected to us via a few acquaintances.

![Six Degrees of Separation.](https://networksciencebook.com/images/ch-03/figure-3-10.jpg)

**Image 3.10: Six Degrees of Separation**

According to six degrees of separation two individuals, anywhere in the world, can be connected through a chain of six or fewer acquaintances. This means that while Sarah does not know Peter, she knows Ralph, who knows Jane and who in turn knows Peter. Hence Sarah is three handshakes, or three degrees from Peter. In the language of network science six degrees, also called the small world property, means that the distance between any two nodes in a network is unexpectedly small.

In the language of network science the small world phenomenon implies that *the distance between two randomly chosen nodes in a network is short*. This statement raises two questions: What does short (or small) mean, i.e. short compared to what? How do we explain the existence of these short distances?

Both questions are answered by a simple calculation. Consider a random network with average degree $\langle k \rangle$. A node in this network has on average:

- $\langle k \rangle$ nodes at distance one ($d=1$).
- $\langle k \rangle^2$ nodes at distance two ($d=2$).
- $\langle k \rangle^3$ nodes at distance three ($d=3$).
- ...
- $\langle k \rangle^d$ nodes at distance $d$.

For example, if $\langle k \rangle \approx 1,000$, which is the estimated number of acquaintances an individual has, we expect $10^6$ individuals at distance two and about a billion, i.e. almost the whole earth's population, at distance three from us.

To be precise, the expected number of nodes up to distance *d* from our starting node is

$$N(d) \approx 1 + \langle k \rangle  + \langle k \rangle ^2  + ... + \langle k \rangle ^d  = \frac{{\langle k \rangle ^{d + 1}  - 1}}{{\langle k \rangle  - 1}} \quad (3.15)$$

*N(d)* must not exceed the total number of nodes, *N*, in the network. Therefore the distances cannot take up arbitrary values. We can identify the maximum distance, $d_{\text{max}}$, or the network's diameter by setting

$$N(d_{\max } ) \approx N \quad (3.16)$$

Assuming that $\langle k \rangle \gg 1$, we can neglect the (-1) term in the numerator and the denominator of (3.15), obtaining

$$\langle k \rangle ^{d_{\max } }  \approx N \quad (3.17)$$

Therefore the diameter of a random network follows

$$d_{\max }  \approx \frac{{\ln N}}{{\ln \langle k \rangle }} \quad (3.18)$$

which represents the mathematical formulation of the small world phenomenon. The key, however is its interpretation:

- As derived, (3.18) predicts the scaling of the network diameter, $d_{\text{max}}$, with the size of the system, *N*. Yet, for most networks (3.18) offers a better approximation to the average distance between two randomly chosen nodes, $\langle d \rangle$, than to $d_{\text{max}}$. This is because $d_{\text{max}}$ is often dominated by a few extreme paths, while $\langle d \rangle$ is averaged over all node pairs, a process that suppresses the fluctuations. Hence typically the small world property is defined by

$$\langle d \rangle  \approx \frac{{\ln N}}{{\ln \langle k \rangle }} \quad (3.19)$$

describing the dependence of the average distance in a network on *N* and $\langle k \rangle$.

- In general $\ln N \ll N$, hence the dependence of $\langle d \rangle$ on $\ln N$ implies that the distances in a random network are *orders of magnitude smaller than the size of the network*. Consequently by *small* in the "small world phenomenon" we mean that the *average path length or the diameter depends logarithmically on the system size*. Hence, "small" means that $\langle d \rangle$ is proportional to $\ln N$, rather than *N* or some power of *N*.
- The $1/\ln \langle k \rangle$ term implies that the denser the network, the smaller is the distance between the nodes.
- In real networks there are systematic corrections to (3.19), rooted in the fact that the number of nodes at distance $d$ ≫ $\langle d \rangle$ drops rapidly (ADVANCED TOPICS 3.F).

![Why are Small Worlds Surprising?](https://networksciencebook.com/images/ch-03/figure-3-11.jpg)

**Image 3.11: Why are Small Worlds Surprising?**

Much of our intuition about distance is based on our experience with regular lattices, which do not display the small world property:

**1D:** For a one-dimensional lattice (a line of length *N*) the diameter and the average path length scale linearly with *N*: $d_{\text{max}} \sim \langle d \rangle \sim N$.

**2D:** For a square lattice $d_{\text{max}} \sim \langle d \rangle \sim N^{1/2}$.

**3D:** For a cubic lattice $d_{\text{max}} \sim \langle d \rangle \sim N^{1/3}$.

**4D:** In general, for a d-dimensional lattice $d_{\text{max}} \sim \langle d \rangle \sim N^{1/d}$.

These polynomial dependences predict a much faster increase with *N* than (3.19), indicating that in lattices the path lengths are significantly longer than in a random network. For example, if the social network would form a square lattice (2D), where each individual knows only its neighbors, the average distance between two individuals would be roughly $(7 \times 10^9)^{1/2} = 83,666$. Even if we correct for the fact that a person has about 1,000 acquaintances, not four, the average separation will be orders of magnitude larger than predicted by (3.19).

1. The figure shows the predicted *N*-dependence of $\langle d \rangle$ for regular and random networks on a linear scale.
2. The same as in (a), but shown on a log-log scale.

Let us illustrate the implications of (3.19) for social networks. Using $N \approx 7 \times 10^9$ and $\langle k \rangle \approx 10^3$, we obtain

$$\langle d \rangle  \approx \frac{{\ln 7 \times 10^9 }}{{\ln (10^3 )}} = 3.28 \quad (3.20)$$

Therefore, all individuals on Earth should be within three to four handshakes of each other. The estimate (3.20) is probably closer to the real value than the frequently quoted six degrees (BOX 3.7).

Much of what we know about the small world property in random networks, including the result (3.19), is in a little known paper by Manfred Kochen and Ithiel de Sola Pool, in which they mathematically formulated the problem and discussed in depth its sociological implications. This paper inspired the well known Milgram experiment (BOX 3.6), which in turn inspired the *six-degrees of separation* phrase.

While discovered in the context of social systems, the small world property applies beyond social networks (BOX 3.6). To demonstrate this in Table 3.2 we compare the prediction of (3.19) with the average path length $\langle d \rangle$ for several real networks, finding that despite the diversity of these systems and the significant differences between them in terms of *N* and $\langle k \rangle$, (3.19) offers a good approximation to the empirically observed $\langle d \rangle$.

### Box 3.6: 19 Degrees of Separation

How many clicks do we need to reach a randomly chosen document on the Web? The difficulty in addressing this question is rooted in the fact that we lack a complete map of the WWW—we only have access to small samples of the full map. We can start, however, by measuring the WWW's average path length in samples of increasing sizes, a procedure called *finite size scaling*. The measurements indicate that the average path length of the WWW increases with the size of the network as

$$\langle d \rangle  \approx 0.35 + 0.89\ln N$$

In 1999 the WWW was estimated to have about 800 million documents, in which case the above equation predicts $\langle d \rangle \approx 18.69$. In other words in 1999 two randomly chosen documents were on average 19 clicks from each other, a result that became known as *19 degrees of separation*. Subsequent measurements on a sample of 200 million documents found $\langle d \rangle \approx 16$, in good agreement with the $\langle d \rangle \approx 17$ prediction. Currently the WWW is estimated to have about trillion nodes ($N \sim 10^{12}$), in which case the formula predicts $\langle d \rangle \approx 25$. Hence $\langle d \rangle$ is not fixed but as the network grows, so does the distance between two documents.

The average path length of 25 is much larger than the proverbial six degrees (BOX 3.7). The difference is easy to understand: The WWW has smaller average degree and larger size than the social network. According to (3.19) both of these differences increase the Web's diameter.

| Network | N | L | $\langle k \rangle$ | $\langle d \rangle$ | $d_{\max}$ | $\ln N / \ln \langle k \rangle$ |
|---------|---|---|---|---|---|---|
| Internet | 192,244 | 609,066 | 6.34 | 6.98 | 26 | 6.58 |
| WWW | 325,729 | 1,497,134 | 4.60 | 11.27 | 93 | 8.31 |
| Power Grid | 4,941 | 6,594 | 2.67 | 18.99 | 46 | 8.66 |
| Mobile-Phone Calls | 36,595 | 91,826 | 2.51 | 11.72 | 39 | 11.42 |
| Email | 57,194 | 103,731 | 1.81 | 5.88 | 18 | 18.4 |
| Science Collaboration | 23,133 | 93,437 | 8.08 | 5.35 | 15 | 4.81 |
| Actor Network | 702,388 | 29,397,908 | 83.71 | 3.91 | 14 | 3.04 |
| Citation Network | 449,673 | 4,707,958 | 10.43 | 11.21 | 42 | 5.55 |
| E. Coli Metabolism | 1,039 | 5,802 | 5.58 | 2.98 | 8 | 4.04 |
| Protein Interactions | 2,018 | 2,930 | 2.90 | 5.61 | 14 | 7.14 |

**Table 3.2: Six Degrees of Separation**

The average distance $\langle d \rangle$ and the maximum distance $d_{\max}$ for the ten reference networks. The last column provides $\langle d \rangle$ predicted by (3.19), indicating that it offers a reasonable approximation to the measured $\langle d \rangle$. Yet, the agreement is not perfect - we will see in the next chapter that for many real networks (3.19) needs to be adjusted. For directed networks the average degree and the path lengths are measured along the direction of the links.

### Box 3.7: Six Degrees: Experimental Confirmation

The first empirical study of the small world phenomena took place in 1967, when Stanley Milgram, building on the work of Pool and Kochen, designed an experiment to measure the distances in social networks. Milgram chose a stock broker in Boston and a divinity student in Sharon, Massachusetts as *targets*. He then randomly selected residents of Wichita and Omaha, sending them a letter containing a short summary of the study's purpose, a photograph, the name, address and information about the target person. They were asked to forward the letter to a friend, relative or acquaintance who is most likely to know the target person.

Within a few days the first letter arrived, passing through only two links. Eventually 64 of the 296 letters made it back, some, however, requiring close to a dozen intermediates. These completed chains allowed Milgram to determine the number of individuals required to get the letter to the target. He found that the median number of intermediates was 5.2, a relatively small number that was remarkably close to Frigyes Karinthy's 1929 insight (BOX 3.8).

![Six Degrees? From Milgram to Facebook.](https://networksciencebook.com/images/ch-03/figure-3-12.jpg)

**Image 3.12: Six Degrees? From Milgram to Facebook**

(a) In Milgram's experiment 64 of the 296 letters made it to the recipient. The figure shows the length distribution of the completed chains, indicating that some letters required only one intermediary, while others required as many as ten. The mean of the distribution was 5.2, indicating that on average six "handshakes" were required to get a letter to its recipient. The playwright John Guare renamed this "six degrees of separation" two decades later.

(b) The distance distribution, $p_d$, for all pairs of Facebook users worldwide and within the US only. Using Facebook's *N* and *L* (3.19) predicts the average degree to be approximately 3.90, not far from the reported four degrees.

Milgram lacked an accurate map of the full acquaintance network, hence his experiment could not detect the true distance between his study's participants. Today Facebook has the most extensive social network map ever assembled. Using Facebook's social graph of May 2011, consisting of 721 million active users and 68 billion symmetric friendship links, researchers found an average distance 4.74 between the users. Therefore, the study detected only "four degrees of separation", closer to the prediction of (3.20) than to Milgram's six degrees.

*"I asked a person of intelligence how many steps he thought it would take, and he said that it would require 100 intermediate persons, or more, to move from Nebraska to Sharon."*

*Stanley Milgram, 1969*

### Box 3.8: Six Degrees of the WWW

![Six Degrees of the WWW.](https://networksciencebook.com/images/ch-03/figure-box-3-8.jpg)

---

## Section 3.9: Clustering Coefficient

The degree of a node contains no information about the relationship between a node's neighbors. Do they all know each other, or are they perhaps isolated from each other? The answer is provided by the local clustering coefficient $C_i$, that measures the density of links in node *i*'s immediate neighborhood: $C_i = 0$ means that there are no links between *i*'s neighbors; $C_i = 1$ implies that each of the *i*'s neighbors link to each other.

To calculate $C_i$ for a node in a random network we need to estimate the expected number of links $L_i$ between the node's $k_i$ neighbors. In a random network the probability that two of *i*'s neighbors link to each other is *p*. As there are $k_i(k_i - 1)/2$ possible links between the $k_i$ neighbors of node *i*, the expected value of $L_i$ is

$$\langle {L_i } \rangle  = p\frac{{k_i (k_i  - 1)}}{2} \quad (3.20)$$

Thus the local clustering coefficient of a random network is

$$C_i  = \frac{{2\langle {L_i } \rangle }}{{k_i (k_i  - 1)}} = p = \frac{{\langle k \rangle }}{N} \quad (3.21)$$

Equation (3.21) makes two predictions:

1. For fixed $\langle k \rangle$, the larger the network, the smaller is a node's clustering coefficient. Consequently a node's local clustering coefficient $C_i$ is expected to decrease as $1/N$. Note that the network's average clustering coefficient, $\langle C \rangle$ also follows (3.21).
2. The local clustering coefficient of a node is independent of the node's degree.

To test the validity of (3.21) we plot $\langle C \rangle / \langle k \rangle$ in function of *N* for several undirected networks. We find that $\langle C \rangle / \langle k \rangle$ does not decrease as $N^{-1}$, but it is largely independent of *N*, in violation of the prediction (3.21) and point (1) above. In Image 3.13b-d we also show the dependency of $C$ on the node's degree $k_i$ for three real networks, finding that $C(k)$ systematically decreases with the degree, again in violation of (3.21) and point (2).

In summary, we find that the random network model does not capture the clustering of real networks. Instead real networks have a much higher clustering coefficient than expected for a random network of similar *N* and *L*. An extension of the random network model proposed by Watts and Strogatz addresses the coexistence of high $\langle C \rangle$ and the small world property (BOX 3.9). It fails to explain, however, why high-degree nodes have a smaller clustering coefficient than low-degree nodes. Models explaining the shape of $C(k)$ are discussed in Chapter 9.

![Clustering in Real Networks.](https://networksciencebook.com/images/ch-03/figure-3-13.jpg)

**Image 3.13: Clustering in Real Networks**

1. Comparing the average clustering coefficient of real networks with the prediction (3.21) for random networks. The circles and their colors correspond to the networks of Table 3.2. Directed networks were made undirected to calculate $\langle C \rangle$ and $\langle k \rangle$. The green line corresponds to (3.21), predicting that for random networks the average clustering coefficient decreases as $N^{-1}$. In contrast, for real networks $\langle C \rangle$ appears to be independent of *N*.
2. The dependence of the local clustering coefficient, $C(k)$, on the node's degree for (b) the Internet, (c) science collaboration network and (d) protein interaction network. $C(k)$ is measured by averaging the local clustering coefficient of all nodes with the same degree *k*. The green horizontal line corresponds to $\langle C \rangle$.

### Box 3.9: Watts-Strogatz Model

Duncan Watts and Steven Strogatz proposed an extension of the random network model motivated by two observations:

**(a) Small World Property**

In real networks the average distance between two nodes depends logarithmically on *N* (3.18), rather than following a polynomial expected for regular lattices.

**(b) High Clustering**

The average clustering coefficient of real networks is much higher than expected for a random network of similar *N* and *L*.

The *Watts-Strogatz model* (also called the *small-world model*) interpolates between a *regular lattice*, which has high clustering but lacks the small-world phenomenon, and a *random network*, which has low clustering, but displays the small-world property. Numerical simulations indicate that for a range of rewiring parameters the model's average path length is low but the clustering coefficient is high, hence reproducing the coexistence of high clustering and small-world phenomena.

Being an extension of the random network model, the Watts-Strogatz model predicts a Poisson-like bounded degree distribution. Consequently high degree nodes, like those seen in Image 3.6, are absent from it. Furthermore it predicts a *k*-independent $C(k)$, being unable to recover the *k*-dependence observed in Image 3.13b-d. As we show in the next chapters, understanding the coexistence of the small world property with high clustering must start from the network's correct degree distribution.

![The Watts-Strogatz Model.](https://networksciencebook.com/images/ch-03/figure-3-14.jpg)

**Image 3.14: The Watts-Strogatz Model**

(a) We start from a ring of nodes, each node being connected to their immediate and next neighbors. Hence initially each node has $\langle C \rangle = 3/4$ ($p = 0$).

(b) With probability *p* each link is rewired to a randomly chosen node. For small *p* the network maintains high clustering but the random long-range links can drastically decrease the distances between the nodes.

(c) For $p = 1$ all links have been rewired, so the network turns into a random network.

(d) The dependence of the average path length $d(p)$ and clustering coefficient $\langle C(p) \rangle$ on the rewiring parameter *p*. Note that $d(p)$ and $\langle C(p) \rangle$ have been normalized by $d(0)$ and $\langle C(0) \rangle$ obtained for a regular lattice (i.e. for $p=0$ in (a)). The rapid drop in $d(p)$ signals the onset of the small-world phenomenon. During this drop, $\langle C(p) \rangle$ remains high. Hence in the range $0.001 \lesssim p \lesssim 0.1$ short path lengths and high clustering coexist in the network.

---

## Section 3.10: Summary: Real Networks are Not Random

Since its introduction in 1959 the random network model has dominated mathematical approaches to complex networks. The model suggests that the random-looking networks observed in complex systems should be described as purely random. With that it equated complexity with randomness. We must therefore ask:

*Do we really believe that real networks are random?*

The answer is clearly no. As the interactions between our proteins are governed by the strict laws of biochemistry, for the cell to function its chemical architecture cannot be random. Similarly, in a random society an American student would be as likely to have among his friends Chinese factory workers than one of her classmates.

In reality we suspect the existence of a deep order behind most complex systems. That order must be reflected in the structure of the network that describes their architecture, resulting in systematic deviations from a pure random configuration.

The degree to which random networks describe, or fail to describe, real systems, must not be decided by epistemological arguments, but by a systematic quantitative comparison. We can do this, taking advantage of the fact that random network theory makes a number of quantitative predictions:

### Degree Distribution

A random network has a binomial distribution, well approximated by a Poisson distribution in the $k \ll N$ limit. Yet, as shown in Image 3.5, the Poisson distribution fails to capture the degree distribution of real networks. In real systems we have more highly connected nodes than the random network model could account for.

### Connectedness

Random network theory predicts that for $\langle k \rangle \gtrsim 1$ we should observe a giant component, a condition satisfied by all networks we examined. Most networks, however, do not satisfy the $\langle k \rangle \gtrsim \ln N$ condition, implying that they should be broken into isolated clusters (Table 3.1). Some networks are indeed fragmented, most are not.

### Average Path Length

Random network theory predicts that the average path length follows (3.19), a prediction that offers a reasonable approximation for the observed path lengths. Hence the random network model can account for the emergence of small world phenomena.

### Clustering Coefficient

In a random network the local clustering coefficient is independent of the node's degree and $\langle C \rangle$ depends on the system size as $1/N$. In contrast, measurements indicate that for real networks $C(k)$ decreases with the node degrees and is largely independent of the system size (Image 3.13).

Taken together, it appears that the small world phenomena is the only property reasonably explained by the random network model. All other network characteristics, from the degree distribution to the clustering coefficient, are significantly different in real networks. The extension of the Erdős-Rényi model proposed by Watts and Strogatz successfully predicts the coexistence of high $C$ and low $\langle d \rangle$, but fails to explain the degree distribution and $C(k)$. In fact, the more we learn about real networks, the more we will arrive at the startling conclusion that *we do not know of any real network that is accurately described by the random network model*.

This conclusion begs a legitimate question: If real networks are not random, why did we devote a full chapter to the random network model? The answer is simple: The model serves as an important reference as we proceed to explore the properties of real networks. Each time we observe some network property we will have to ask if it could have emerged by chance. For this we turn to the random network model as a guide: If the property is present in the model, it means that randomness can account for it. If the property is absent in random networks, it may represent some signature of order, requiring a deeper explanation. So, the random network model may be the wrong model for most real systems, but *it remains quite relevant for network science* (BOX 3.10).

### Box 3.10: Random Networks and Network Science

The lack of agreement between random and real networks raises an important question: How could a theory survive so long given its poor agreement with reality? The answer is simple: Random network theory was never meant to serve as a model of real systems.

Erdős and Rényi write in their first paper that random networks "may be interesting not only from a purely mathematical point of view. In fact, the evolution of graphs may be considered as a rather simplified model of the evolution of certain communication nets (railways, road or electric network systems, etc.) of a country or some unit." Yet, in the string of eight papers authored by them on the subject, this is the *only* mention of the potential practical value of their approach. The subsequent development of random graphs was driven by the problem's inherent mathematical challenges, rather than its applications.

It is tempting to follow Thomas Kuhn and view network science as a paradigm change from random graphs to a theory of real networks. In reality, there was no network paradigm before the end of 1990s. This period is characterized by a lack of systematic attempts to compare the properties of real networks with graph theoretical models. The work of Erdős and Rényi has gained prominence outside mathematics only after the emergence of network science.

Network theory does not lessen the contributions of Erdős and Rényi, but celebrates the unintended impact of their work. When we discuss the discrepancies between random and real networks, we do so mainly for pedagogical reasons: to offer a proper foundation on which we can understand the properties of real systems.

![Network Science and Random Networks.](https://networksciencebook.com/images/ch-03/figure-3-15.jpg)

**Image 3.15: Network Science and Random Networks**

While today we perceive the Erdős-Rényi model as the cornerstone of network theory, the model was hardly known outside a small subfield of mathematics. This is illustrated by the yearly citations of the first two papers by Erdős and Rényi, published in 1959 and 1960. For four decades after their publication the papers gathered less than 10 citations each year. The number of citations exploded after the first papers on scale-free networks have turned Erdős and Rényi's work into the reference model of network theory.

### Box 3.11: At a Glance: Random Networks

**Definition:** *N* nodes, where each node pair is connected with probability *p*.

**Average Degree:**
$$\langle k \rangle  = p(N - 1)$$

**Average Number of Links:**
$$\langle L \rangle  = \frac{{pN(N - 1)}}{2}$$

**Degree Distribution:**

Binomial Form:
$$p_k  = \left( {\begin{array}{*{20}c} {N - 1}  \\ k  \\ \end{array}} \right)p^k (1 - p)^{N - 1 - k}$$

Poisson Form:
$$p_k  = e^{ - \langle k \rangle } \frac{{\langle k \rangle ^k }}{{k!}}$$

**Giant Component ($N_G$):**
$$\langle k \rangle  < 1: \quad N_G  \sim \ln N$$

$$1 < \langle k \rangle  < \ln N: \quad N_G  \sim N^{\frac{2}{3}}$$

$$\langle k \rangle  > \ln N: \quad N_G  \sim (p - p_c )N$$

**Average Distance:**
$$\langle d \rangle  \propto \frac{{\ln N}}{{\ln \langle k \rangle }}$$

**Clustering Coefficient:**
$$\langle C \rangle  = \frac{{\langle k \rangle }}{N}$$

---

## Section 3.11: Homework

1. **Erdős-Rényi Networks**

   Consider an Erdős-Rényi network with $N = 3,000$ nodes, connected to each other with probability $p = 10^{-3}$.

   (a) What is the expected number of links, $\langle L \rangle$?
   
   (b) In which regime is the network?
   
   (c) Calculate the probability $p_c$ so that the network is at the critical point
   
   (d) Given the linking probability $p = 10^{-3}$, calculate the number of nodes $N^{cr}$ so that the network has only one component.
   
   (e) For the network in (d), calculate the average degree $\langle k^{cr} \rangle$ and the average distance between two randomly chosen nodes $\langle d \rangle$.
   
   (f) Calculate the degree distribution $p_k$ of this network (approximate with a Poisson degree distribution).

2. **Generating Erdős-Rényi Networks**

   Relying on the *G(N, p)* model, generate with a computer three networks with $N = 500$ nodes and average degree (a) $\langle k \rangle = 0.8$, (b) $\langle k \rangle = 1$ and (c) $\langle k \rangle = 8$. Visualize these networks.

3. **Circle Network**

   Consider a network with *N* nodes placed on a circle, so that each node connects to *m* neighbors on either side (consequently each node has degree 2m). Image 3.14(a) shows an example of such a network with $m = 2$ and $N = 20$. Calculate the average clustering coefficient $\langle C \rangle$ of this network and the average shortest path $\langle d \rangle$. For simplicity assume that *N* and *m* are chosen such that $(n-1)/2m$ is an integer. What happens to $\langle C \rangle$ if $N \gg 1$? And what happens to $\langle d \rangle$?

4. **Cayley Tree**

   A Cayley tree is a symmetric tree, constructed starting from a central node of degree *k*. Each node at distance *d* from the central node has degree *k*, until we reach the nodes at distance *P* that have degree one and are called leaves (see Image 3.16 for a Cayley tree with $k = 3$ and $P = 5$.)

   (a) Calculate the number of nodes reachable in t steps from the central node.
   
   (b) Calculate the degree distribution of the network.
   
   (c) Calculate the diameter $d_{\max}$.
   
   (d) Find an expression for the diameter $d_{\max}$ in terms of the total number of nodes *N*.
   
   (e) Does the network display the small-world property?

5. **Snobbish Network**

   Consider a network of *N* red and *N* blue nodes. The probability that there is a link between nodes of identical color is *p* and the probability that there is a link between nodes of different color is *q*. A network is snobbish if $p \gtrsim q$, capturing a tendency to connect to nodes of the same color. For $q = 0$ the network has at least two components, containing nodes with the same color.

   (a) Calculate the average degree of the "blue" subnetwork made of only blue nodes, and the average degree in the full network.
   
   (b) Determine the minimal *p* and *q* required to have, with high probability, just one component.
   
   (c) Show that for large *N* even very snobbish networks ($p \gg q$) display the small-world property.

6. **Snobbish Social Networks**

   Consider the following variant of the model discussed above: We have a network of $2N$ nodes, consisting of an equal number of red and blue nodes, while an *f* fraction of the $2N$ nodes are purple. Blue and red nodes do not connect to each other ($q = 0$), while they connect with probability *p* to nodes of the same color. Purple nodes connect with the same probability *p* to both red and blue nodes

   (a) We call the red and blue communities *interactive* if a typical red node is just two steps away from a blue node and vice versa. Evaluate the fraction of purple nodes required for the communities to be interactive.
   
   (b) Comment on the size of the purple community if the average degree of the blue (or red) nodes is $\langle k \rangle \gg 1$.
   
   (c) What are the implications of this model for the structure of social (and other) networks?

![Cayley Tree.](https://networksciencebook.com/images/ch-03/figure-3-16.jpg)

**Image 3.16: Cayley Tree**

A Cayley Tree With $k = 3$ and $P = 5$.

---

## Section 3.12: Advanced Topic 3.A - Deriving the Poisson Distribution

To derive the Poisson form of the degree distribution we start from the exact binomial distribution (3.7)

$$p_k  = \left( {\begin{array}{*{20}c} {N - 1}  \\ k  \\ \end{array}} \right)p^k (1 - p)^{N - 1 - k} \quad (3.22)$$

that characterizes a random graph. We rewrite the first term on the r.h.s. as

$$\left( {\begin{array}{*{20}c} {N - 1}  \\ k  \\ \end{array}} \right) = \frac{{(N - 1)(N - 1 - 1)(N - 1 - 2)...(N - 1 - k + 1)}}{{k!}} \approx \frac{{(N - 1)^k }}{{k!}} \quad (3.23)$$

where in the last term we used that $k \ll N$. The last term of (3.22) can be simplified as

$$\ln \left[ {(1 - p)^{(N - 1) - k} } \right] = (N - 1 - k)\ln \left( {1 - \frac{{\langle k \rangle }}{{N - 1}}} \right)$$

and using the series expansion

$$\ln (1 + x) = \sum\limits_{n = 1}^\infty  {\frac{{( - 1)^{n + 1} }}{n}x^n  = x - \frac{{x^2 }}{2}}  + \frac{{x^3 }}{3} - ...,\forall |x| \le 1$$

we obtain

$$\ln \left[ {(1 - p)^{(N - 1) - k} } \right] \approx (N - 1 - k)\frac{{\langle k \rangle }}{{N - 1}} =  - \langle k \rangle \left( {1 - \frac{k}{{N - 1}}} \right) \approx  - \langle k \rangle$$

which is valid if $N \gg k$. This represents the *small degree approximation* at the heart of this derivation. Therefore the last term of (3.22) becomes

$$(1 - p)^{N - 1 - k}  = e^{ - \langle k \rangle } \quad (3.24)$$

Combining (3.22), (3.23), and (3.24) we obtain the Poisson form of the degree distribution

$$p_k  = \left( {\begin{array}{*{20}c} {N - 1}  \\ k  \\ \end{array}} \right)p^k (1 - p)^{(N - 1) - k}  = \frac{{(N - 1)^k }}{{k!}}p^k e^{ - \langle k \rangle }  = \frac{{(N - 1)^k }}{{k!}}\left( {\frac{{\langle k \rangle }}{{N - 1}}} \right)^k e^{ - \langle k \rangle }$$

or

$$p_k  = e^{ - \langle k \rangle } \frac{{\langle k \rangle ^k }}{{k!}} \quad (3.25)$$

---

## Section 3.13: Advanced Topic 3.B - Maximum and Minimum Degrees

To determine the expected degree of the largest node in a random network, called the network's *upper natural cutoff*, we define the degree $k_{\text{max}}$ such that in a network of *N* nodes we have at most one node with degree higher than $k_{\text{max}}$. Mathematically this means that the area behind the Poisson distribution $p_k$ for $k \geq k_{\text{max}}$ should be approximately one. Since the area is given by $1-P(k_{\text{max}})$, where $P(k)$ is the cumulative degree distribution of $p_k$, the network's largest node satisfies:

$$N\left[ {1 - P\left( {k_{\max } } \right)} \right] \approx 1 \quad (3.26)$$

We write $\approx$ instead of $=$, because $k_{\text{max}}$ is an integer, so in general the exact equation does not have a solution. For a Poisson distribution

$$1 - P(k_{\max } ) = 1 - e^{ - \langle k \rangle } \sum\limits_{k = 0}^{k_{\max } } {\frac{{\langle k \rangle ^k }}{{k!}}}  = e^{ - \langle k \rangle } \sum\limits_{k = k_{\max }  + 1}^\infty  {\frac{{\langle k \rangle ^k }}{{k!}}}  \approx e^{ - \langle k \rangle } \frac{{\langle k \rangle ^{k_{\max }  + 1} }}{{(k_{\max }  + 1)!}} \quad (3.27)$$

where in the last term we approximate the sum with its largest term.

For $N = 10^9$ and $\langle k \rangle = 1,000$, roughly the size and the average degree of the globe's social network, (3.26) and (3.27) predict $k_{\text{max}} = 1,185$, indicating that a random network lacks extremely popular individuals, or hubs.

We can use a similar argument to calculate the expected degree of the smallest node, $k_{\text{min}}$. By requiring that there should be at most one node with degree smaller than $k_{\text{min}}$ we can write

$$NP(k_{\min }  - 1) \simeq 1 \quad (3.28)$$

For the Erdős-Rényi network we have

$$P(k_{\min }  - 1) = e^{ - \langle k \rangle } \sum\limits_{k = 0}^{k_{\min }  - 1} {\frac{{\langle k \rangle ^k }}{{k!}}} \quad (3.29)$$

Solving (3.28) with $N = 10^9$ and $\langle k \rangle = 1,000$ we obtain $k_{\text{min}} = 816$.

![Minimum and Maximum Degree.](https://networksciencebook.com/images/ch-03/figure-3-17.jpg)

**Image 3.17: Minimum and Maximum Degree**

The estimated maximum degree of a network, $k_{\max}$, is chosen so that there is at most one node whose degree is higher than $k_{\max}$. This is often called the *natural upper cutoff* of a degree distribution. To calculate it, we need to set $k_{\max}$ such that the area under the degree distribution $p_k$ for $k > k_{\max}$ equals $1/N$, hence the total number of nodes expected in this region is exactly one. We follow a similar argument to determine the expected smallest degree, $k_{\min}$.

---

## Section 3.14: Advanced Topic 3.
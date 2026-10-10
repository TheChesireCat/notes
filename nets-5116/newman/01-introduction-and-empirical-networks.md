---
subject: NETS 5116 · Newman ch. 1–5
short_title: Ch. 1–5 · Empirical networks
---

# 🍼 Basics of Network Science 

## Introduction to Networks

### Definition and Basic Concepts

A **network** is a collection of points (nodes/vertices) joined together in pairs by lines (edges). Networks provide a powerful framework for representing and analyzing complex systems across multiple disciplines.

### Four Main Categories of Networks

#### 1. Technological Networks
- **Internet**: Nodes are computers/routers, edges are data connections
- **Telephone networks**: Circuit-switched vs packet-switched systems
- **Power grids**: High-voltage transmission networks
- **Transportation networks**: Airlines, roads, railways
- **Distribution networks**: Pipelines, water/sewer systems

#### 2. Information Networks  
- **World Wide Web**: Directed network where nodes are web pages, edges are hyperlinks
- **Citation networks**: Academic papers connected by bibliographic references
- **Patent networks**: Patents connected by citations
- **Legal networks**: Court opinions connected by precedent citations

#### 3. Social Networks
- **Friendship networks**: People connected by social relationships
- **Professional networks**: Business relationships, collaborations
- **Online social networks**: Facebook, Twitter, LinkedIn connections
- **Communication networks**: Email, phone call patterns

#### 4. Biological Networks
- **Biochemical networks**: Metabolic pathways, protein interactions
- **Neural networks**: Brain cells and their connections  
- **Ecological networks**: Food webs, predator-prey relationships
- **Genetic networks**: Gene regulation patterns

### Key Network Properties

#### Degree
The **degree** of a node is the number of edges connected to it:
- In directed networks: **in-degree** (incoming edges) and **out-degree** (outgoing edges)
- Degree distribution reveals important structural properties
- **Hubs**: Nodes with unusually high degree that can dominate network behavior

#### Distance and Small-World Effect
- **Distance** between nodes = minimum number of edges to traverse
- **Small-world effect**: Mean distance is surprisingly short even in large networks
- Popularized as "six degrees of separation" 
- Critical for information spread and network efficiency

#### Clustering and Community Structure
- Networks often contain **clusters** or **communities**
- Groups of nodes more densely connected internally than externally
- Reveals functional organization and hierarchical structure

## Technological Networks

### The Internet

#### Structure and Organization
The Internet has a hierarchical three-tier structure:
1. **Backbone**: Core high-speed trunk lines operated by Network Backbone Providers (NBPs)
2. **Internet Service Providers (ISPs)**: Regional and local providers
3. **End users**: Individual computers and devices

#### Network Representations
Different levels of granularity are used:
- **Router-level**: Individual routers and connections
- **Subnet-level**: Class C subnets (e.g., 141.211.243.xxx)
- **Domain-level**: Organizational domains (e.g., umich.edu)
- **Autonomous System (AS) level**: Administrative routing domains

#### Measurement Techniques

**Traceroute Method**:
- Uses Time-To-Live (TTL) field in packets
- Systematically increases TTL to map network paths
- Reconstructs topology by combining multiple paths
- Limited by routing policies and network changes

**BGP Routing Tables**:
- Border Gateway Protocol maintains routing information
- AS-level topology from router routing tables
- More complete view of inter-domain structure
- Used by projects like Routeviews

### Power Grids and Transportation Networks

#### Power Grid Characteristics
- Nodes: Generating stations, switching substations
- Edges: High-voltage transmission lines
- Spatial embedding with geographic constraints
- Complex control systems affect behavior beyond pure topology

#### Transportation Networks
- **Airline networks**: Airports connected by routes
- **Road networks**: Intersections connected by road segments  
- **Rail networks**: Stations connected by tracks
- Can be represented as bipartite networks (locations and routes)

## Information Networks

### World Wide Web

#### Network Structure
- **Directed network**: Hyperlinks have specific direction
- **Dynamic content**: Pages generated on-the-fly from databases
- **Component structure**: Not all pages reachable from any starting point

#### Web Crawlers
Process for mapping web structure:
1. Start with initial web page
2. Extract all URLs from page content
3. Download linked pages using breadth-first search
4. Store unique URLs, avoiding duplicates
5. Continue until desired coverage achieved

**Limitations**:
- robots.txt restrictions
- Dynamic page generation
- Network connectivity constraints
- Crawler bias in sampling

### Citation Networks

#### Characteristics
- **Directed edges**: From citing paper to cited paper
- **Acyclic structure**: Citations point backward in time
- Reflects knowledge organization and research relationships

#### Types of Citation Networks
- **Direct citations**: Paper-to-paper references
- **Co-citation networks**: Papers cited together by same source
- **Bibliographic coupling**: Papers citing same sources

#### Data Sources
- **Manual databases**: Science Citation Index, Scopus
- **Automated systems**: Google Scholar, CiteseerX, Citelemx
- **Specialized domains**: arXiv, PubMed, legal databases

### Patent and Legal Citation Networks

#### Patent Citations
- **Defensive citations**: Differentiate from prior art
- **Dependency citations**: Build upon previous inventions
- Nearly acyclic temporal structure
- Available through NBER database, Google Patents

#### Legal Citations
- Court opinions cite precedent cases
- Establish legal reasoning chains
- Available through LexisNexis, Westlaw
- Hierarchical court system creates structured patterns

## Social Networks

### Empirical Methods

#### Direct Questioning
**Name Generators**: Survey questions asking respondents to identify contacts
- Example: "Who are your friends at school?"
- **Fixed choice**: Limited number of responses (e.g., top 8 friends)
- **Free choice**: Unlimited responses

**Issues**:
- Asymmetric nominations (A names B, but B doesn't name A)
- Artificial degree cutoffs in fixed choice studies
- Subjective interpretation of relationship types

#### Survey Types
**Sociometric Studies**: Survey entire population
- Gold standard but labor intensive  
- Example: Zachary's karate club (34 members)

**Ego-centered Studies**: Sample individuals and their immediate contacts
- More scalable for large populations
- Example: General Social Survey (GSS)
- Limited to local network properties

#### Direct Observation
- Labor intensive, limited to small groups
- Useful for animal social networks
- Example: Windsurfer interactions on beach
- Freeman et al. studies in university settings

### Archival and Digital Data Sources

#### Historical Records
- Marriage records, trade relationships
- Example: Padgett & Ansell Florentine families
- Medici family's central position in marriage network

#### Electronic Communications
- **Email networks**: Message logs reveal communication patterns
- **Phone call networks**: Call detail records from telecom companies
- **Mobile phone data**: Includes location information
- **Online social networks**: Facebook, Twitter, LinkedIn data

#### Temporal Dynamics
- Networks change over time
- Longitudinal studies track evolution
- Contact patterns vary by time of day, season
- Event-driven network changes

### Network Sampling Methods

#### Snowball Sampling
Process:
1. Start with initial population member
2. Interview and ask for contacts
3. Interview contacts and get their contacts  
4. Continue through multiple waves

**Bias**: Over-samples high-degree nodes and central actors
**Applications**: Hidden populations (drug users, illegal immigrants)

#### Random Walk Sampling
1. Start with initial individual
2. Interview to determine all contacts
3. Randomly select one contact for next interview
4. Repeat process

**Advantages**:
- Known sampling bias (proportional to degree)
- Can correct for bias using degree information
- Reaches equilibrium faster than snowball sampling

#### Contact Tracing
- Used for disease outbreak investigation
- Follow contacts of infected individuals
- Creates biased sample (over-represents disease carriers)
- Similar bias patterns to snowball sampling

### Small-World Experiments

#### Milgram's Original Study (1960s)
- 96 packages sent from Omaha, Nebraska to Boston target
- 18 packages (19%) reached target
- Average path length: 5.9 steps
- Origin of "six degrees of separation" concept

**Findings**:
- Short paths exist in social networks
- People can navigate these paths with local information
- "Funneling" through highly connected individuals
- "Sociometric superstars" serve as crucial bridges

#### Modern Replications  
**Dodds et al. Email Study**:
- 24,000 email chains, 18 different targets
- Only 1.5% completion rate
- Average length ~4 steps for completed chains
- Estimated true average: 5-7 steps

**Implications**:
- Demonstrates network searchability
- Requires special network structure (Kleinberg's insight)
- Geographic and occupational information most important for routing

## Biological Networks

### Biochemical Networks

#### Metabolic Networks
**Components**:
- **Nodes**: Metabolites (small molecules)
- **Edges**: Chemical reactions
- **Enzymes**: Protein catalysts (not typically nodes)

**Network Representations**:
1. **Bipartite**: Separate nodes for metabolites and reactions
2. **Metabolite projection**: Metabolites connected if in same reaction
3. **Directed projection**: Substrate → product relationships

**Experimental Methods**:
- **Radioactive tracers**: Track isotopes through pathways
- **Concentration manipulation**: Increase substrate/enzyme levels
- **Reaction inhibition**: Block enzymes, observe substrate buildup
- **Knockout experiments**: Genetically remove enzymes

**Databases**: KEGG, MetaCyc

#### Protein-Protein Interaction Networks
**Interactions**:
- Physical binding to form protein complexes
- Usually undirected (mutual binding)
- Can involve 3+ proteins in single complex

**Experimental Methods**:

**Co-immunoprecipitation**:
- Use antibodies to capture target protein
- Identify bound partners in recovered complex
- Reliable but labor intensive

**Two-hybrid Screen**:
- Reconstruct transcription factor when proteins interact
- High-throughput but ~50% false positive rate
- Uses "bait" and "prey" proteins

**Affinity Purification**:
- Tag proteins, use tag-specific antibodies
- More reliable than two-hybrid
- **Tandem affinity purification**: Two-stage process

**Databases**: BioGRID, STRING, IntAct

#### Genetic Regulatory Networks
**Process**:
1. **Transcription**: DNA → RNA via RNA polymerase
2. **Translation**: RNA → Protein via ribosomes
3. **Regulation**: Transcription factors control gene expression

**Network Structure**:
- **Nodes**: Genes/proteins
- **Directed edges**: Regulatory relationships
- **Edge types**: Promoting vs inhibiting regulation

**Experimental Methods**:
- **Electrophoretic mobility shift assay**: Detect DNA-protein binding
- **DNase footprinting**: Identify protected DNA regions
- **Microarrays**: Measure mRNA concentration changes
- **Computational prediction**: Identify promoter sequences

### Neural Networks

#### Neuron Structure and Function
**Components**:
- **Cell body (soma)**: Integrates inputs
- **Dendrites**: Input wires (can be 1-1000+)
- **Axon**: Single output wire
- **Synapses**: Gaps between neurons
- **Action potentials**: Electrical signals (~tens of millivolts)

**Signal Processing**:
1. Chemical neurotransmitters cross synapses
2. Voltage changes in receiving dendrites
3. Soma integrates multiple inputs
4. Fires action potential if threshold exceeded
5. Signal propagates down axon to next neurons

#### Network Representation
- **Nodes**: Individual neurons
- **Directed edges**: Synaptic connections
- **Edge types**: Excitatory (→) vs inhibitory (⊣)
- **Node types**: Different neuron classes

#### Experimental Methods

**Traditional Approaches**:
- **Electron microscopy**: Thin tissue slices
- **Manual reconstruction**: Trace connections by hand
- Example: C. elegans complete wiring diagram (~300 neurons)

**Modern Optical Methods**:
- **Fluorescent proteins**: Genetically encoded markers
- **Brainbow technique**: Random color combinations
- **Confocal microscopy**: 3D optical sectioning
- **Clarity method**: Make tissue transparent
- **Transsynaptic tracing**: Tracers cross synapses

#### Macroscopic Brain Networks
**Nodes**: Entire brain regions (tens to hundreds)
**Connections**: Functional or anatomical links between regions

**Measurement Techniques**:
- **Diffusion MRI**: Detect white matter tracts
- **Functional MRI**: Correlations in activity patterns
- **Non-invasive**: Can study living human brains
- **Resolution**: Millimeter scale (vs micrometer for neurons)

### Ecological Networks

#### Food Webs
**Structure**:
- **Nodes**: Species or trophic species (groups with similar roles)
- **Directed edges**: Energy flow from prey to predator
- **Approximately acyclic**: Clear trophic hierarchy

**Trophic Levels**:
- **Level 1**: Primary producers (plants, phytoplankton)
- **Level 2**: Herbivores
- **Level 3+**: Carnivores, top predators
- **Calculation**: 1 + mean trophic level of prey

**Network Types**:
- **Community webs**: Complete ecosystem
- **Source webs**: Species connected to particular producer
- **Sink webs**: Species connected to particular top predator

**Data Collection**:
- **Direct observation**: Field studies of feeding behavior
- **Gut content analysis**: Dissection of stomach contents
- **Literature compilation**: Synthesize existing knowledge
- **Paleontological webs**: Fossil record analysis

#### Host-Parasite Networks
- **Directed relationships**: Parasite depends on host
- **Multi-level**: Hyperparasites on parasites
- **Agricultural importance**: Livestock and crop pests
- **Size relationships**: Parasites typically smaller than hosts

#### Mutualistic Networks
**Types**:
- **Plant-pollinator**: Insects pollinate flowers
- **Plant-seed disperser**: Animals spread seeds
- **Plant-ant protection**: Ants defend plants

**Structure**:
- **Undirected**: Mutual benefit
- **Often bipartite**: Two distinct species types
- **Example databases**: NCEAS Interaction Web Database

### Network Measurement Challenges

#### Data Quality Issues
- **Sampling bias**: Non-random data collection
- **Measurement error**: False positives/negatives
- **Temporal variation**: Networks change over time
- **Scale limitations**: Technology and resource constraints

#### Methodological Considerations
- **Resolution trade-offs**: Detail vs coverage
- **Cost-benefit analysis**: Accuracy vs efficiency  
- **Validation methods**: Cross-checking different approaches
- **Standardization**: Comparable across studies

#### Emerging Technologies
- **High-throughput methods**: Automated data collection
- **Computational approaches**: Algorithm-assisted analysis
- **Multi-modal integration**: Combine different data types
- **Real-time monitoring**: Dynamic network tracking

## Summary and Applications

### Unifying Principles
1. **Small-world property**: Short average path lengths
2. **Degree heterogeneity**: Broad degree distributions with hubs
3. **Community structure**: Hierarchical organization
4. **Growth and evolution**: Dynamic network formation
5. **Robustness vs fragility**: Resilience to random failures, vulnerability to targeted attacks

### Cross-Disciplinary Tools
- **Visualization methods**: Network drawing algorithms
- **Statistical measures**: Degree distributions, clustering coefficients
- **Mathematical models**: Random graphs, preferential attachment
- **Computational algorithms**: Shortest paths, community detection
- **Dynamical processes**: Information spread, epidemic models

### Future Directions
- **Multilayer networks**: Multiple types of connections
- **Temporal networks**: Explicit time evolution
- **Spatial networks**: Geographic embedding effects
- **Network of networks**: Interdependent systems
- **Machine learning applications**: Automated pattern discovery
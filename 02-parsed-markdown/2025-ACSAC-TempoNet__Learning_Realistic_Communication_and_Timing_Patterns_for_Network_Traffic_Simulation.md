# TempoNet: Learning Realistic Communication and Timing Patterns for Network Traffic Simulation

Kristen Moore<sup>∗</sup>, Diksha Goel<sup>∗</sup>, Cody James Christopher<sup>∗†</sup>, Zhen Wang<sup>∗</sup>,

Minjune Kim<sup>∗</sup>, Ahmed Ibrahim<sup>‡</sup>, Ahmad Mohsin<sup>‡</sup>, Seyit Camtepe<sup>∗</sup>

<sup>∗</sup>CSIRO Data61, Australia

<sup>†</sup>Australian National University, Australia

<sup>‡</sup>Edith Cowan University, Australia

{kristen.moore, diksha.goel, jeff.wang, minjune.kim, seyit.camtepe}@data61.csiro.au,

cody.christopher@anu.edu.au, {ahmed.ibrahim, a.mohsin}@ecu.edu.au

Abstract—Realistic network traffic simulation is critical for evaluating intrusion detection systems, stress-testing network protocols, and constructing high-fidelity environments for cybersecurity training. While attack traffic can often be layered into training environments using red-teaming or replay methods, generating authentic benign background traffic remains a core challenge—particularly in simulating the complex temporal and communication dynamics of real-world networks. This paper introduces TempoNet, a novel generative model that combines multi-task learning with multi-mark temporal point processes to jointly model inter-arrival times and all packet- and flow-header fields. TempoNet captures fine-grained timing patterns and higher-order correlations such as hostpair behavior and seasonal trends, addressing key limitations of GAN-, LLM-, and Bayesian-based methods that fail to reproduce structured temporal variation. TempoNet produces temporally consistent, high-fidelity traces, validated on realworld datasets. Furthermore, we show that intrusion detection models trained on TempoNet-generated background traffic perform comparably to those trained on real data, validating its utility for real-world security applications.

Index Terms—Network Traffic Simulation, Temporal Point Processes, Intrusion Detection, Synthetic Data Generation, Network Data Augmentation

## 1. Introduction

Synthetic network traffic generation is essential for evaluating and optimizing network-based systems in applications such as performance benchmarking, intrusion detection, and cybersecurity training. However, access to realworld network traces is often limited due to privacy, proprietary, and operational security constraints, making it difficult to use authentic data in research or simulation environments. Synthetic data generation offers a promising alternative—allowing researchers to emulate realistic behavior without exposing sensitive information.

Yet without accurate background traffic simulation, Red vs. Blue exercises, cyber deception platforms, and intrusion detection evaluations risk relying on unrealistic assumptions. In cyber range training, for example, the absence of legitimate user activity means blue teams can trivially detect red team attacks by simply observing any traffic at all. As highlighted by Mases et al. [1], the lack of authentic¨ background traffic leads to flawed assessments and diminished training outcomes. Similarly, deception platforms require diverse, natural-looking background flows to sustain adversary engagement and prevent detection of honeypots (e.g., fake user login sessions, or periodic DNS queries). Replaying NetFlow or PCAP traces is brittle, inflexible, and often avoided due to privacy risks and residual metadata leakage [2]—even anonymized traffic can reveal sensitive host or behavioral information through timing patterns and communication structures [3].

A key challenge lies in generating traffic that accurately replicates the complex temporal and communication dynamics of real-world environments. Recent ML-based approaches can produce high-fidelity header data but often struggle to model the multidimensional temporal dependencies present in packet-header (e.g., PCAP) and flow-header (e.g., NetFlow) traces. Generative Adversarial Networks (GANs), for example, are known to struggle with long-range dependencies, and modeling inter-arrival times is explicitly considered out of scope in state-of-the-art GAN-based methods [4], [5]. While diffusion and VAE-based models have shown promise in other domains, they remain underexplored for full-field network traffic simulation due to high inference costs and limited support for multi-field tabular data. Pretrained Large Language Models (LLMs) have recently been adapted for structured data generation, but remain largely untested in capturing higher-order temporal correlations [6]. Temporal Point Processes (TPPs), by contrast, offer a natural framework for modeling time-dependent event sequences, yet existing TPP-based generators are typically limited to producing only one or two event attributes [7]–[10], falling short of the multidimensional realism required for comprehensive traffic simulation.

As a result, synthetic traces often lack the variability and nuance needed for security applications: blue teams and IDS tools trained in these environments can more easily distinguish simulated from real events, undermining both detection effectiveness and training value [11]–[13]. Capturing these complex patterns is essential for robust benchmarking, intrusion detection, cyber range training, and deception systems that aim to reflect operational realities.

This paper introduces TempoNet, a novel generative framework that combines temporal point processes (TPPs) with multi-task learning to generate realistic, temporally consistent packet- and flow-header traces. TempoNet jointly models all header fields—including categorical values (e.g., IP addresses, ports), continuous variables (e.g., inter-arrival times, packet sizes), and discrete counts (e.g., flow duration)—while preserving the interdependencies across them. At its core, the model uses a recurrent neural network (RNN) to encode recent history and a log-normal mixture model TPP to sample inter-arrival times. Task-specific output layers then decode each header field, enabling multi-mark generation within a unified architecture.

TempoNet enables efficient, high-fidelity simulation of network traffic that closely mirrors real-world behavior, capturing both fine-grained timing and higher-order communication patterns such as host-pair burstiness and structured periodicity. These capabilities make it particularly suited for security-critical applications, including adversarial model evaluation, cyber deception, and blue team training.

Our main contributions include:

1. Integrated Generative Model: A novel generative architecture that combines multi-task learning with multi-mark temporal point processes to jointly model inter-arrival times and packet- and flow-header fields, capturing structured temporal patterns such as daily and weekly seasonality.

2. Comprehensive Empirical Evaluation: The first rigorous comparison of GAN-, LLM-, Bayesian-, and TPPbased approaches for modeling temporal and higher-order network communication dynamics. TempoNet outperforms prior methods across fidelity, diversity, and compliance metrics, and handles heterogeneous header fields including numeric, categorical, and temporally structured features such as inter-arrival times with daily and weekly seasonality.

3. Real-World Security Application: Demonstrate the practical utility of TempoNet-generated traffic through an intrusion detection task, using real CIDDS attack data layered on top of synthetic benign traffic.

## 2. Background: Temporal Point Processes

Temporal point processes (TPP) are probabilistic models designed to handle event data that include timestamps. Essentially, a TPP is a stochastic process where the output consists of the event times $\{ t _ { i } \}$ , or equivalently, the interarrival times $\left\{ \tau _ { i } \ : = \ t _ { i } - t _ { i - 1 } \right\}$ between events. These processes offer an intuitive framework for modeling streams of discrete events over time, employing probabilistic distributions. The most basic TPP is the Poisson Process [14], which assumes that events occur independently and that the time between events follows an exponential distribution. Numerous extensions of the Poisson Process have been developed to capture more complex dependencies between event occurrences, including the Hawkes Process [15], a self-exciting process where past events temporarily increase the likelihood of future events.

A TPP is uniquely characterized by its conditional intensity function, which specifies the rate at which events occur based on the event history. Conditional intensity functions offer a straightforward method to define TPPs with predeter mined behavior. However, choosing an appropriate intensity function presents a significant challenge. Simple functions with closed-form log-likelihoods often lack expressiveness, while more complex functions require approximation methods that can lead to noisy gradient estimates during training. An alternative approach, proposed by Shchur et al. [16], directly models the conditional probability density function of inter-event times. This intensity-free approach uses normalizing flows to create flexible TPP models that can approximate any probability density arbitrarily well, including multi-modal ones. Specifically, their LogNormMix model employs a log-normal mixture distribution, offering both flexibility and closed-form sampling capabilities.

A marked TPP builds on the standard TPP by attaching extra information, called marks, to each event. These marks can include details like the event’s size, type, or other characteristics. Unlike standard TPPs, a marked TPP predicts both when events happen and the marks associated with them, allowing for a more detailed understanding of event patterns. However, adding marks significantly increases model complexity and adds to computational demands. Careful design is required to capture how marks relate to each other and to the timing of events. Because of these challenges, existing work in the TPP domain has focused on the simpler task of modeling only one or two event attributes (marks) alongside the event timestamps.

## 3. Preliminaries

## 3.1. Problem formulation

Our input data comprises network traces in two forms: packet headers or flow headers. Packet header traces include details such as source and destination IP addresses, ports and protocol, along with associated metrics like timestamps and packet sizes. For flow header traces, each entry contains the IP 5-tuple (source and destination IPs, ports, and protocol) along with related measurements, including flow start and end times and total bytes transferred.

Our objective is to design a generative model for PCAP and NetFlow traces that achieves high fidelity to the original data, as defined by expert-informed criteria and specific application needs. TempoNet, like most prior work (e.g., [4], [17]–[19]), models only these header-level features and does not attempt to generate payload contents. This design choice is intentional and aligns with the structure of common benchmarks and training environments, such as LANL, OpTC, and GHOSTS, which provide header-only data due to privacy and compliance considerations. Payload modeling introduces additional complexity and remains far less common in practice, as it raises complex privacy, applicationspecific, and modeling challenges.

Instead, TempoNet prioritizes temporal and structural fidelity—dimensions that are underexplored but critically important for evaluating detection models and simulating realistic background traffic. This focus allows our method to remain broadly applicable across diverse environments where payload access is restricted or unavailable.

The evaluation framework includes four key criteria, inspired by recent work [19]:

Realism: Measures how well the synthetic traffic matches the statistical characteristics of real data. We use Earth Mover’s Distance (EMD) for numerical fields (e.g., inter-arrival times) and Jensen-Shannon Divergence (JSD) for categorical fields (e.g., IP addresses, ports). To assess inter-feature relationships, we use Pairwise Correlation Difference (PCD), defined as the $L ^ { 2 }$ norm between correlation matrices of numerical features, and Contingency Matrix Difference (CMD), which compares categorical feature dependencies.

Diversity: Capturing the variability in the data by ensuring the generated traffic maintains a similar level of variance to the real data, assessed using Coverage and Density metrics.

Novelty: Verifying that synthetic samples are not direct copies of the training data, evaluated using metrics like Membership Disclosure.

Compliance: Ensuring adherence to network protocol rules through a Domain Knowledge Check (DKC), which tests the validity of generated traffic against known protocol constraints.

Through this multifaceted evaluation, we aim to develop a model that produces realistic, diverse, and compliant network flow traffic while effectively capturing the intrinsic correlations between features.

## 3.2. Why TPPs?

Although many machine learning-based approaches treat network traffic generation as a time series problem, the underlying process governing packet and flow inter-arrival times is more accurately represented by Temporal Point Processes (TPPs). Recognizing this, several studies have adopted TPPs to demonstrate superior performance in generating, forecasting, and detecting anomalies in traffic timing and volume [7]–[10]. The accurate representation of temporal dynamics in simulated background traffic is crucial for creating realistic cyber range exercises. It creates an authentic environment that mirrors real-world network behavior, increasing the complexity and educational value of exercises. Moreover, they enable effective testing of network intrusion detection and anomaly detection systems, which often rely heavily on temporal cues.

Despite their importance, temporal dynamics are often considered out of scope by state-of-the-art network packet trace generation approaches [4], [19], [20]. Many existing methods focus on replicating distributions of static attributes, such as IPs, ports, and packet sizes, while neglecting the complex temporal dependencies present in real network traffic. This limitation underscores the need for TPP-based approaches, which are inherently designed to model temporal dynamics alongside other traffic attributes.

However, whilst existing TPP approaches excel at capturing temporal patterns, they often overlook the modeling of other critical header trace fields, such as source and destination IP addresses, ports, protocol, and packet sizes, leaving room for improvement in generating fully representative network traffic.

When designing TPP models, three key attributes are crucial [21]:

i) Flexibility: The model should be capable of accurately approximating any probability distribution, including multimodal ones.

ii) Closed-form likelihood: Models with analytically computable likelihood functions are preferable, avoiding slower, less accurate approximation methods that can lead to noisy gradient estimates during training.

iii) Closed-form sampling: The ability to generate samples analytically, particularly through inversion sampling, is vital. Alternatives like the thinning algorithm are inefficient, less precise, and unsuitable for parallel hardware like GPUs.

These properties ensure the model is versatile, computationally efficient, and capable of generating accurate samples, which is particularly important for network traffic simulation. The LogNormMix TPP [16] that we leverage in this work satisfies all three of these properties, whilst other existing approaches are sub-optimal, offering different tradeoffs between the three. In this work we propose a multi-mark TPP that bridges ML- and TPP-based approaches to network traffic simulation.

## 3.3. Why focus on background traffic?

Simulating attack traffic is relatively straightforward: red team exercises, replay frameworks, and automated attack tools make it easy to generate adversarial events in controlled environments. In contrast, capturing or synthesizing realistic background traffic—reflecting the diversity, timing, and structure of normal user activity—is far more difficult. This benign traffic forms the baseline that intrusion detection systems and human analysts rely on to distinguish between normal and malicious behavior. In our own deployments, we collect real attack traces from red team events, making background traffic the missing component needed to build realistic and reusable training environments.

Background traffic is also often unavailable in sensitive environments due to legal, privacy, or operational constraints. Even when replay logs exist, they may lack the diversity, timeliness, and contextual nuance required for generalizable IDS testing or cyber range training. Synthetic generation helps address these gaps—offering flexible, reusable traffic traces that preserve structural and temporal realism without relying on privileged data access.

## 4. TempoNet Methodology

## 4.1. High-level overview

Network Headers. Let $D = \left( t _ { i } , \mathbf { x } _ { i } \right) _ { i = } ^ { N }$ be a header trace dataset, where:

• N is the total number of records (packets or flows)

$t _ { i } \in \mathbb { R } ^ { + }$ is the timestamp of the $i ^ { \bar { t } h }$ record

$\mathbf { x } _ { i } \in X$ is the vector of header fields for the $i ^ { t h }$ record, and $X : = X _ { 1 } \times X _ { 2 } \times \ldots \times X _ { m - 1 }$ , where $X _ { j }$ represents the space of possible values for the $j ^ { t h }$ header field (e.g., IP addresses, ports, protocols).

Sequential Dependency and History Encoding. A key characteristic of network traffic is that the attributes of an incoming packet or flow header can be influenced by the sequence of preceding headers. To capture this historical dependency, we utilize a recurrent neural network (RNN), specifically an LSTM in our implementation. The RNN processes the sequence of past events, denoted as $\mathcal { H } _ { t } : =$ $\{ ( t _ { i } , \mathbf { x } _ { i } ) \in D : t _ { i } < t \}$ , and condenses this information into a fixed-length vector $\pmb { \mathscr { h } } _ { t } \in \mathbb { R } ^ { H }$ . This vector serves as a compact representation of the event history up to time t, providing temporal context for subsequent field prediction modules. Conditioning flow generation on this learned history is critical for modeling burstiness, long-range autocorrelation, and diurnal rhythms. Fixed-window or memory-less methods struggle to reproduce such dependencies, whereas RNNs offer a compact yet expressive summary that enables TempoNet to capture both fine-grained bursts and broader seasonal cycles.

TempoNet design. We frame flow and packet header generation as a multi-task machine learning problem. In this approach:

1) Each task, representing the generation of a specific header field, has its own prediction module and associated negative log-likelihood (NLL) loss function.

2) The fixed-dimensional RNN history vector $\scriptstyle { \hat { h } } _ { t }$ serves as a shared backbone input for all prediction modules.

3) Each prediction module learns the distribution of its respective header field, conditioned on: i) The history embedding vector $\scriptstyle { h _ { t } , }$ ii) Other relevant header trace fields, where applicable. Task-specific output layers act as specialized decoders for each prediction module, tailored to the unique characteristics of the corresponding header field.

4) An equal weighting optimization strategy is used, where the loss weight for each task is set to 1/m in every iteration, where m denotes the number of tasks.

Multi-task Learning vs. Separate Models. TempoNet’s multi-task design ensures that each task (e.g., timing, protocol, ports) benefits from a shared temporal context via a single RNN encoder. This avoids the redundancy of training separate models, each with its own RNN, which would inflate parameter counts, increase training time, and risk inconsistent temporal modeling. By consolidating shared structure into one encoder, TempoNet improves parameter efficiency and enforces consistent temporal dependencies across heterogeneous header fields.

Modeling heterogeneous fields. To accommodate the diversity of header fields, numeric attributes are modeled with a log-normal mixture model as the prediction module (trained using NLL loss), while categorical attributes are modeled with a categorical distribution (trained with categorical cross-entropy loss). Specifically:

• Inter-arrival times: flow and packet inter-arrival times are modeled by the log-normal mixture model TPP, known as LogNormMix. [16].

• Source/destination $I P$ addresses: Host pair selection is formulated as a source-driven process, where the source IP address is selected first using the categorical distribution for the source module. Destination $\mathrm { I P }$ generation is then treated as a multi-class classification problem conditioned on the given source IP.

• Size and flow duration: These are dependent on the specific host pair [22] and are each modeled with a lognormal mixture model, conditioned on the host pair.

• Ports and Protocol: To capture dependence of ports and protocol on the specific host pair, we model these fields with a categorical distribution, conditioned on the host pair, with the destination ports further conditioned on the protocol.

Due to the high number of tasks for NetFlow generation, we separate NetFlow header generation into 2 stages: 1) Temporal communication dynamics: namely, who is communicating with whom and at what times, which includes flow inter-arrival times, host pair, and flow duration. 2. Communication characteristics: which models the specific attributes of the communication, given the host pair from the first stage. This includes ports, network protocol, and total number of bytes.

## 4.2. Neural network architecture

The high-level architecture of TempoNet is shown in Fig. 1. The model consists of various prediction modules. Each NetFlow/packet header is generated sequentially, one field at a time, starting from the arrival time and the host IP pair. The generation of each header field can be conditioned on other features (in addition to the history), such as hostpair, by concatenating the history embedding $\hslash _ { i }$ with a metadata vector ${ \bf \nabla } _ { { \bf \mathcal { y } } _ { i } }$ that encodes the additional features. The resulting context vector $c _ { i } = | { \pmb h } _ { i } | | { \pmb y } _ { i } |$ then serves as input into each header field’s prediction module. Here we outline the composition of each of the prediction modules:

4.2.1. Log-normal mixture modules. The LogNormMix TPP [16] models the probability distribution of timestamped event streams using a log-normal mixture model. Specifically, it models the inter-event arrival times, $\{ \tau _ { i } \}$ , of isolated events by directly learning the conditional probability density function of the time $\tau _ { i }$ until the next event:

$$
p (\tau | \omega , \mu , \sigma) = \sum_ {k = 1} ^ {K} \omega_ {k} \frac {1}{\tau \sigma_ {k} \sqrt {2 \pi}} \exp - \frac {(\log \tau - \mu_ {k}) ^ {2}}{2 \sigma_ {k} ^ {2}}\tag{1}
$$

![](images/3467f072043b9ba429bf338bff546aba7ccac0add45e5a0927b6ce66c2f222bd.jpg)  
Figure 1: TempoNet architecture.

Here K is the number of mixture components, ω denotes the mixture weights, and $\mu$ and σ are the mixture means and standard deviations, respectively. These log-normal mixture model distribution parameters are defined to be an affine function of the context vector $c _ { i } = | { \pmb h } _ { i } | | { \pmb y } _ { i } |$ via:

$$
\begin{array}{l} \omega_ {i} = \operatorname{softmax} (V _ {\omega} c _ {i} + b _ {\omega}) \\ \sigma_ {i} = \exp (V _ {\sigma} c _ {i} + b _ {\sigma}) \\ \mu_ {i} = V _ {\mu} c _ {i} + b _ {\mu} \end{array}
$$

where $\{ V _ { \omega } , V _ { \sigma } , V _ { \mu } , b _ { \omega } , b _ { \sigma } , b _ { \mu } \}$ are learnable parameters, and the softmax and exponential transformations enforce essential constraints on the distribution parameters.

Rationale for Log-normal Mixtures. We adopt log-normal mixtures for inter-arrival time modeling due to their universal approximation property on $\mathbb { R } ^ { + }$ , which allows them to flexibly capture diverse, multi-modal distributions of network timing. Alternative distributions present practical drawbacks for training: log-logistic models exhibit undefined moments, complicating likelihood-based learning, while gamma mixtures require reparameterized sampling, hindering efficient optimization. The log-normal family, by contrast, admits closed-form likelihoods and inversion sampling, enabling stable training and efficient simulation. These properties make it well suited for capturing both the heavy-tailed bursts and regular periodicities characteristic of real network traffic.

Existing TPP literature, however, has generally been limited to modeling only one [16] or two [23] categorical marks, with spatio-temporal variants typically restricted to two categorical or continuous marks for spatial coordinates [24], [25]. To the best of our knowledge, TempoNet is the first to augment a TPP model to jointly learn more than 3 fields of mixed numeric and categorical type, enabling richer and more realistic network traffic simulation.

In TempoNet, the log-normal mixture is applied not only to inter-arrival times but also to other numeric fields where temporal or host-dependent variability is critical:

Timestamps: The metadata vector ${ \bf \nabla } _ { { \bf \theta } } ^ { { \bf \mu } } \left. \begin{array} { r l } \end{array} \right.$ encodes temporalrelated information such as the day of the week and time of day, to help the model learn the seasonality of network traffic on the cyber range’s simulated corporate network.

Size and flow duration: For both the NetFlow/packet size and the flow duration prediction module, the metadata vector y<sub>i</sub> incorporates host IP pair embeddings. The size and flow duration distributions are modeled using the same log-normal mixture approach as the inter-event arrival times τ , following equation 1.

4.2.2. Categorical prediction modules. Categorical prediction modules are used to model selection of the host IP pair, as well as the ports and protocol.

During generation, the class with the highest likelihood is selected.

Source IP module: This incorporates a feedforward network and softmax

, generating output logits that define a categorical distribution over network nodes. The implemented source IP feedforward network in our experiments comprises two fully connected layers with an intervening tanh activation layer.

Destination IP, Port, and Protocol modules:

The prediction module to learn a categorical distribution for the destination IP, port, and protocol fields consists of a fully connected layer plus softmax.

## 4.3. Event generation with TempoNet

TempoNet’s architecture facilitates straightforward header sampling. Numeric fields like the inter-event time τ, flow/packet size, and flow duration are sampled from the log-normal mixture using standard mixture model sampling:

1) Sample the mixture component:

$$
\mathbf {z} \sim C a t e g o r i c a l (\boldsymbol {\omega})
$$

where z is a one-hot vector of size $K .$

2) Sample from the unit Normal distribution:

$$
\varepsilon \sim n (0, 1)
$$

3) Transform the unit normal sample ε to the log-normal distribution for the mixture component z:

$$
\boldsymbol {\tau} = \exp (\pmb {\sigma} ^ {\mathsf {T}} \mathbf {z} \varepsilon + \pmb {\mu} ^ {\mathsf {T}} \mathbf {z})
$$

The host IP pair, ports and protocol of the header are drawn from their respective categorical distributions, with the sampled host IP pair fed as input into the respective selection modules via the metadata vector y<sub>i</sub> as appropriate.

## 5. Evaluation

Our evaluation aims to assess whether TempoNet can produce synthetic traffic that is realistic, diverse, novel, and compliant with protocol rules. We benchmark against leading methods from each category (GAN, LLM, Bayesian), evaluating their ability to replicate both static distributions and temporal dependencies critical for security applications.

## 5.1. Datasets

We evaluate on four publicly available datasets that vary in topology, scale, and protocol mix. LANL [26] contains internal traffic from a large enterprise network. CIDDS [27] provides flow-level data with labeled attacks and external scanning traffic. DC [28] is a lightweight campus network capture. IoT [29] uses the ToN IoT network-flow subset from a heterogeneous IoT/IIoT testbed across multiple sites. We include this dataset primarily as a robustness stress test under distribution shift, since its lab-generated nature and temporal inconsistency make it less directly comparable to enterprise or campus traces. Full dataset descriptions and preprocessing steps are in Appendix A.

## 5.2. Baselines

We compare TempoNet to the following state-of-the-art GAN, LLM, and Bayesian Network generation models<sup>1</sup>.

1) NetShare [4] is a GAN-based approach that adapts and extends the DoppelGANger [18] framework to address the specific challenges associated with generating synthetic IP header traces. It improves fidelity by capturing intra- and inter-epoch correlations, and enhances scalability through fine-tuning and parallel training. However, NetShare is known to be computationally expensive, with the original study requiring a cluster of 200 CPU cores and 1.92 TB of RAM.

2) GReaT [6] generates synthetic tabular data using transformer-based neural networks. The GReaT approach involves two main stages: fine-tuning a pretrained LLM on the tabular data and sampling from the fine-tuned model to generate synthetic data.

3) The $\mathrm { B N } _ { b i n s }$ model studied in [19] is a Bayesian Network-based generative approach that uses a quantile-based discretization strategy for numerical features. This method captures inter-feature dependencies through Conditional Probability Tables (CPTs), enabling efficient modeling of the joint distribution of network flow data. We use the bnlearn Python library implementation of $\mathrm { B N } _ { b i n s }$

Other approaches, such as the VAE-based method Encore [22], focuses solely on modeling flow sizes between host pairs, and is unable to model the other critical header fields (such timestamps or ports) or network-wide dynamics. Similarly, the diffusion-based model in [30] faces challenges with long training times, slow inference, and limited scalability, having only been tested on a small dataset of 30,000 records. As a result both approaches are unsuitable for highfidelity, scalable network traffic modeling, and were ruled out.

## 5.3. Experiments and Metrics

We simulate 9-10 weeks of packet/NetFlow header data for of the 3 main datasets and evaluate the generated traffic against both the real training and test sets using a comprehensive set of metrics. Our evaluation blends established statistical tests with domain-specific diagnostics inspired by real-world security needs such as cyber range exercises.

Reproducibility considerations. For NetShare, we trained using 10 CPU cores and 1.5 TB of RAM on the LANL and DC datasets, compared to the 200 cores and 1.92 TB recommended in the original paper. While this resource gap may have impacted performance, prior independent evaluations [19] also report instability and limited fidelity even under the recommended setup, suggesting that these challenges are partly architectural. We therefore present NetShare as a strong but resource-intensive baseline, while emphasizing TempoNet’s efficiency advantages.

Realism, Diversity, Novelty, and Compliance. We adopt the framework introduced by [19]:

• Realism measures alignment with real data distributions. This includes marginal distribution metrics like Jensen-Shannon Divergence (JSD) and Earth Mover’s Distance (EMD), as well as inter-feature metrics like Pairwise Conditional Distribution (PCD) for numerical correlations and Contingency Matrix Differences (CMD) for categorical dependencies. Lower scores indicate better fidelity.

• Diversity is evaluated using the coverage metric, which assess how broadly synthetic data spans the real distribution’s support. Coverage quantifies the number of synthetic neighborhood spheres that contain each real sample. A low score means that many real samples do not have corresponding generated synthetic samples nearby, revealing that the synthetic distribution fails to sufficiently represent the variability present in the real distribution.

• Novelty is assessed via the Membership Disclosure (MD) metric. MD measures the degree to which synthetic samples differ from the real training data by computing the proportion of synthetic samples that are unusually close based on Hamming distance—to real training data. Rather than rewarding lower MD, we compare against the test set MD score, indicating that the synthetic data has a similar degree of novelty and overlap as real, unseen traffic. Extremely low MD may indicate underfitting or insufficient coverage of realistic behaviors.

• Compliance is measured by Domain Knowledge Check, which validates conditions such as: (i) packet sizes within valid ranges (e.g., minimum 40 bytes for TCP, 28 bytes for UDP) and (ii) appropriate relationships between port numbers and protocols (e.g., port 80 for HTTP, port 53 for DNS). A detailed description of the compliance check is provided in Appendix C.

We use the original TALE metric implementations to ensure consistent and replicable evaluation.

Categorical Field Fidelity. We further assess per-field realism using JSD on key categorical variables: source IP, destination IP, destination port, and protocol. These metrics evaluate whether the model captures structural properties like service use and communication asymmetries.

Temporal and Higher-Order Fidelity. To reflect realworld use in cyber ranges, we evaluate the following.

• Temporal Fidelity is assessed using EMD on interarrival times, flow durations, and seasonality features (hour-of-day, day-of-week). We visualize how well each model reproduces real-world inter-arrival times using quantile–quantile (Q–Q) plots and use boxplots to illustrate alignment in daily and weekly seasonality patterns.

• Host IP pair-level Fidelity evaluations are carried out to assess host IP selection realism. To do this, we examined the 30 most active source/destination IP pairs from the training set for each dataset, and visualized the proportion of packets/flows sent by each source IP and received by each destination IP using box plots.

Interpreting test set performance. TempoNet and all baselines are trained on the training split of each dataset. The Real test set scores reported in our tables are not intended as performance targets, but serve as calibration baselines that illustrate the natural variability between two real-world samples from the same distribution. This contextualization is especially important in metrics like EMD and Diversity, where theoretical optima (e.g., EMD = 0, Diversity = 1) may be unattainable in practice. We include test set values to provide a sanity check: if even two real samples diverge on a metric, then perfect synthetic alignment is neither expected nor required. For metrics like MD, the test set also provides a meaningful novelty baseline. This framing helps calibrate expectations and interpret synthetic performance more realistically.

## 6. Results

## 6.1. Overall realism, diversity, novelty and compliance.

We evaluate model performance across the four criteria using the metrics from Section 5.3, with results shown in Table 1. TempoNet performs strongly across all metrics, ranking first on LANL and DC datasets and second on CIDDS, highlighting its robustness across diverse datasets.

Realism. TempoNet achieves the best density scores on LANL and DC, reflecting its ability to learn and reproduce the joint data distribution. Its design—explicitly conditioning predictions on relevant header fields (e.g., ports on Host IP pairs)—enhances this alignment. TempoNet also excels on CMD and PCD, which measure attribute correlations, consistently ranking first or second. GReaT LLM also performs well, coming in second to TempoNet on both LANL and CIDDS. Meanwhile, $\mathrm { B N } _ { b i n s }$ leads realism on the DC dataset. NetShare, as noted in prior work [19], performs poorly overall on realism.

Diversity. TempoNet shows strong coverage across datasets, generating samples that reflect the breadth of the real data. GReaT ranks second, particularly strong on CIDDS. Examining EMD and JSD reveals further nuances: TempoNet and $\mathrm { B N } _ { b i n s }$ better capture categorical features (higher JSD), while GReaT and NetShare are relatively stronger on numerical ones. TempoNet consistently balances diversity and realism most effectively.

Novelty. We use Membership Disclosure (MD) to assess overfitting. Rather than treating lower MD as inherently better, since real-world network traffic naturally includes repeated structures, we benchmark model MD scores against the Real test set (MD between 7–8 across datasets). An MD score close to the test set indicates that a model captures natural variability without overfitting. GReaT mathces this best on LANL and CIDDS, while TempoNet leads on DC. NetShare, with much lower MD scores, generates traffic overly dissimilar from real patterns. Overall, TempoNet and GReaT best preserve novelty without sacrificing fidelity.

Compliance. Domain Knowledge Compliance (DKC) assesses whether generated traffic adheres to network protocol rules. Notably, the Real test sets themselves exhibit non-zero DKC scores (e.g., 0.006 for DC), indicating that a small proportion of NetFlows and packets in the original datasets do not fully conform to domain constraints—likely due to real-world anomalies or noise. On the DC dataset, TempoNet and $\mathrm { B N _ { b i n s } }$ closely mirror this compliance profile, suggesting they faithfully replicate both typical behavior and occasional irregularities present in the real data. GReaT achieves the lowest DKC scores overall, reflecting strong protocol adherence. Across all datasets, most models produce DKC values comparable to or lower than the test set. Exceptions include NetShare on LANL and TempoNet on CIDDS, which show slightly higher DKC values. Nevertheless, TempoNet maintains strong overall compliance, balancing realism with adherence to domain-specific rules.

TABLE 1: Comparison of 4 models across metrics for realism, diversity, novelty, and compliance. The ”Real test set” row provides a baseline for unseen real data. Bold black text marks the best result, and bold gray text marks the second best. (↑↑) indicates higher is better, (↓↓) lower is better, and (=) closer to the test set is better.

<table><tr><td colspan="2"></td><td colspan="3">Realism</td><td>Diversity</td><td colspan="2">Realism &amp; Diversity</td><td>Novelty</td><td>Compliance</td><td>Rank</td></tr><tr><td>Dataset</td><td>Model</td><td>CMD (↓)</td><td>PCD (↓)</td><td>Density (↑)</td><td>Coverage (↑)</td><td>EMD (↓)</td><td>JSD (↓)</td><td>MD (=)</td><td>DKC (↓)</td><td>Average (↓)</td></tr><tr><td rowspan="5">LANL</td><td>Real test set</td><td>0.049</td><td>0.009</td><td>0.918</td><td>0.802</td><td>0.0011</td><td>0.11</td><td>7.065</td><td>3e-5</td><td>-</td></tr><tr><td>NetShare</td><td>0.327</td><td>0.471</td><td>0.384</td><td>0.269</td><td>0.0349</td><td>0.35</td><td>5.374</td><td>0.050</td><td>3.75</td></tr><tr><td>GReaT</td><td>0.053</td><td>0.006</td><td>0.809</td><td>0.68</td><td>0.124</td><td>0.06</td><td>6.819</td><td>2e-4</td><td>2.25</td></tr><tr><td> $BN_{bins}$ </td><td>0.004</td><td>0.2312</td><td>0.552</td><td>0.288</td><td>0.043</td><td>0.01</td><td>5.938</td><td>1.4e-3</td><td>2.5</td></tr><tr><td>TempoNet (Ours)</td><td>0.043</td><td>0.005</td><td>0.820</td><td>0.767</td><td>0.0006</td><td>0.03</td><td>6.007</td><td>8e-4</td><td>1.5</td></tr><tr><td rowspan="4">CIDDS</td><td>Real test set</td><td>0.068</td><td>0.0098</td><td>0.915</td><td>0.840</td><td>0.00008</td><td>0.12</td><td>7.36</td><td>5e-4</td><td>-</td></tr><tr><td>GReaT</td><td>0.078</td><td>0.0038</td><td>1.053</td><td>0.837</td><td>0.0001</td><td>0.09</td><td>6.46</td><td>8e-4</td><td>1.5</td></tr><tr><td> $BN_{bins}$ </td><td>0.125</td><td>0.491</td><td>0.557</td><td>0.494</td><td>0.06</td><td>0.14</td><td>6.25</td><td>0.008</td><td>2.875</td></tr><tr><td>TempoNet (Ours)</td><td>0.043</td><td>0.0018</td><td>0.684</td><td>0.784</td><td>0.00005</td><td>0.05</td><td>6.37</td><td>0.023</td><td>1.63</td></tr><tr><td rowspan="5">DC</td><td>Real test set</td><td>0.177</td><td>0.073</td><td>0.578</td><td>0.389</td><td>0.022</td><td>0.38</td><td>7.956</td><td>0.006</td><td>-</td></tr><tr><td>NetShare</td><td>0.250</td><td>0.234</td><td>0.301</td><td>0.230</td><td>0.072</td><td>0.72</td><td>3.009</td><td>6e-6</td><td>3.25</td></tr><tr><td>GReaT</td><td>0.205</td><td>0.232</td><td>0.303</td><td>0.223</td><td>0.060</td><td>0.34</td><td>6.819</td><td>1e-6</td><td>2.75</td></tr><tr><td> $BN_{bins}$ </td><td>0.070</td><td>0.030</td><td>0.328</td><td>0.092</td><td>0.24</td><td>0.14</td><td>6.986</td><td>0.008</td><td>2.25</td></tr><tr><td>TempoNet (Ours)</td><td>0.074</td><td>0.120</td><td>0.420</td><td>0.321</td><td>0.036</td><td>0.20</td><td>7.050</td><td>0.008</td><td>1.63</td></tr><tr><td rowspan="4">IoT</td><td>Real test set</td><td>0.688</td><td>0.865</td><td>0.94</td><td>0.1357</td><td>0.0002</td><td>0.551</td><td>5.83</td><td>0.022</td><td>-</td></tr><tr><td>GReaT</td><td>0.115</td><td>0.88</td><td>0.63</td><td>0.530</td><td>338</td><td>0.092</td><td>6.62</td><td>0.043</td><td>1.875</td></tr><tr><td> $BN_{bins}$ </td><td>0.114</td><td>0.451</td><td>0.12</td><td>0.19</td><td>20.00</td><td>0.101</td><td>7.21</td><td>0.039</td><td>2.125</td></tr><tr><td>TempoNet (Ours)</td><td>0.20</td><td>0.88</td><td>0.48</td><td>0.31</td><td>0.00019</td><td>0.180</td><td>5.86</td><td>0.037</td><td>1.875</td></tr></table>

An expanded discussion of the violated DKC rules, their causes, and implications is provided in Appendix C.

IoT Robustness Stress Test. Finally, to probe robustness under distribution shift, we evaluated models on the ToN IoT dataset. Unlike the enterprise and campus traces, IoT is lab-generated, temporally inconsistent, and exhibits extreme skew (with a handful of devices dominating traffic). As expected, no model achieves strong absolute scores on this dataset. The Real test set itself diverges substantially from nominal ideals (e.g., CMD, PCD, coverage, JSD), reflecting mismatches between training and test distributions. This suggests that enforcing those ideals on IoT would amount to overfitting to the training set. In this light, TempoNet’s results, while not always the closest to the ideals, are better aligned with the Real test set’s deviations, whereas competing models achieve superficially lower errors that reflect overfitting rather than fidelity. Notably, TempoNet and the GReaT LLM baseline tie for best overall performance, underscoring the difficulty of this stress-test setting.

Overall Interpretation. LLM-based models like GReaT excel in compliance and numerical feature modeling, while TPP-based models like TempoNet offer superior realism, diversity, and generalization. $\mathrm { \Delta B N _ { b i n s } }$ performs well on correlation-based metrics like CMD but struggles with density and coverage, indicating limitations in capturing the full data distribution. Overall, NetShare under-performs across all criteria, showing limited realism, diversity, and compliance.

## 6.2. Per-Field Categorical Fidelity.

Table 2 reports the Jensen–Shannon Divergence (JSD) between real and generated distributions for key categorical fields: source IP, destination IP, destination port, and protocol. These metrics assess how well each model captures structural properties of network traffic. TempoNet achieves consistently low JSD scores, demonstrating strong alignment with real-world feature distributions.

TABLE 2: Per-field JSD for categorical headers, reported as mean (std) over 10 trials.

<table><tr><td>Dataset</td><td>Model</td><td>Source IP JSD (↓)</td><td>Dst IP JSD (↓)</td><td>Dst Port JSD (↓)</td><td>Protocol JSD (↓)</td></tr><tr><td rowspan="4">LANL</td><td>NetShare</td><td>0.490 (.01)</td><td>1.49 (.44)</td><td>0.45 (.04)</td><td>0.125 (.023)</td></tr><tr><td>GReaT</td><td>0.150 (6e-4)</td><td>0.11 (8e-4)</td><td>0.01 (.001)</td><td>0.004 (.001)</td></tr><tr><td> $BN_{bins}$ </td><td>0.127(4e-4)</td><td>0.033 (.001)</td><td>0.02 (.001)</td><td>0.088 (.061)</td></tr><tr><td>TempoNet</td><td>0.044 (.001)</td><td>0.058 (.001)</td><td>0.02 (.003)</td><td>0.005 (.002)</td></tr><tr><td rowspan="3">CIDDS</td><td>GReaT</td><td>0.32 (3e-4)</td><td>0.66 (2e-4)</td><td>0.06 (4e-4)</td><td>0.003 (5e-4)</td></tr><tr><td> $BN_{bins}$ </td><td>0.32 (9e-5)</td><td>0.66 (3e-4)</td><td>0.06 (.001)</td><td>0.016 (.001)</td></tr><tr><td>TempoNet</td><td>0.05 (.004)</td><td>0.08 (8e-4)</td><td>0.04 (8e-4)</td><td>0.005 (.001)</td></tr><tr><td rowspan="4">DC</td><td>NetShare</td><td>0.83 (.00)</td><td>0.83 (.00)</td><td>0.82 (3e-3)</td><td>0.44 (.06)</td></tr><tr><td>GReaT</td><td>0.23 (8e-4)</td><td>0.41 (2e-4)</td><td>0.82 (3e-5)</td><td>0.061(6e-4)</td></tr><tr><td> $BN_{bins}$ </td><td>0.19 (5e-4)</td><td>0.40 (2e-4)</td><td>0.28 (1e-4)</td><td>0.087 (3e-4)</td></tr><tr><td>TempoNet</td><td>0.20 (.001)</td><td>0.27 (1e-3)</td><td>0.29 (8e-4)</td><td>0.106 (1e-3)</td></tr><tr><td rowspan="3">IoT</td><td>GReaT</td><td>0.075 (.0008)</td><td>0.098 (.0006)</td><td>0.12 (0.0006)</td><td>0.079 (0.0006)</td></tr><tr><td> $BN_{bins}$ </td><td>0.11 (0.0005)</td><td>0.022 (0.0006)</td><td>0.20 (0.0009)</td><td>0.087 (0.001)</td></tr><tr><td>TempoNet</td><td>0.28 (0.07)</td><td>0.24 (0.08)</td><td>0.20 (0.02)</td><td>0.10 (0.005)</td></tr></table>

## 6.3. Temporal fidelity.

We assess the temporal realism and diversity of the models using Earth Mover’s Distance (EMD) on four key features: inter-arrival times (time deltas), hour of day, day of week, and flow duration, across LANL, CIDDS, and DC datasets. We further visualize temporal fidelity via Q–Q plots and seasonality boxplots. Additional visualizations, including CIDDS Q–Q plots and LANL/DC seasonality trends, are included in Appendix B.

Quantitative results. Table 3 shows that TempoNet consistently achieves the lowest EMD scores across most metrics and datasets, indicating strong alignment with real distributions, particularly for inter-arrival times (Time Deltas), flow durations, and broader periodic trends (Hour of Day and Day of Week). GReaT performs well in some cases (e.g., day-of-week on CIDDS) but is inconsistent. $\mathrm { B N _ { b i n s } }$ shows moderate performance, especially on hour-of-day trends, while NetShare yields the highest EMD values, reflecting weak temporal realism.

TABLE 3: EMD between real and simulated data, reported as mean (std) over 10 trials.

<table><tr><td>Dataset</td><td>Model</td><td>Time Deltas EMD (↓)</td><td>Hourly EMD (↓)</td><td>Daily EMD (↓)</td><td>Duration EMD (↓)</td></tr><tr><td rowspan="4">LANL</td><td>NetShare</td><td>30.54 (8.28)</td><td>0.34 (0.01)</td><td>0.47 (0.03)</td><td>133.7 (56.9)</td></tr><tr><td>GReaT</td><td>6.39 (0.02)</td><td>0.48 (0.01)</td><td>0.23 (0.01)</td><td>441 (50.3)</td></tr><tr><td> $BN_{bins}$ </td><td>3.93 (0.03)</td><td>0.36 (0.01)</td><td>0.18 (0.01)</td><td>163886 (1083)</td></tr><tr><td>TempoNet</td><td>0.58 (0.10)</td><td>0.15 (0.06)</td><td>0.10 (0.01)</td><td>0.66 (.01)</td></tr><tr><td rowspan="3">CIDDS</td><td>GReaT</td><td>3e-4 (3e-6)</td><td>2.48 (0.03)</td><td>0.57 (0.02)</td><td>0.13 (4e-4)</td></tr><tr><td> $BN_{bins}$ </td><td>1.70 (1e-3)</td><td>2.41 (4e-3)</td><td>0.61 (1e-3)</td><td>1.16 (2e-4)</td></tr><tr><td>TempoNet</td><td>1e-4 (2e-5)</td><td>0.41 (0.08)</td><td>0.83 (0.05)</td><td>0.02 (.002)</td></tr><tr><td rowspan="4">DC</td><td>NetShare</td><td>6e-4 (8e-5)</td><td>0.93 (0.8)</td><td>0.96 (1.0)</td><td>-</td></tr><tr><td>GReaT</td><td>6.5e-6 (1e-6)</td><td>0.41 (7e-3)</td><td>0.12 (7e-3)</td><td>-</td></tr><tr><td> $BN_{bins}$ </td><td>0.01 (5e-5)</td><td>0.29 (0.01)</td><td>0.28 (2e-3)</td><td>-</td></tr><tr><td>TempoNet</td><td>7e-5 (8e-6)</td><td>0.52 (0.09)</td><td>0.09 (0.03)</td><td>-</td></tr><tr><td rowspan="3">IoT</td><td>GReaT</td><td>2962530 (9368342)</td><td>0.40 (.08)</td><td>0.48 (.01)</td><td>9.43 (.04)</td></tr><tr><td> $BN_{bins}$ </td><td>105170.5 (90518.0)</td><td>0.43 (0.27)</td><td>0.84 (0.51)</td><td>9248.7 (36.4)</td></tr><tr><td>TempoNet</td><td>0.34 (0.17)</td><td>0.62 (0.05)</td><td>0.13 (0.02)</td><td>37.33 (11.46)</td></tr></table>

Q–Q plots of inter-arrival times. Figure 2 (with CIDDS shown in Appendix B (Figure 7)) presents Q– Q plots comparing real and generated inter-arrival time quantiles. Points lying near the red diagonal indicate close distributional match; systematic deviations reflect under- or overestimation of inter-arrival times at specific quantiles. The black points are empirical quantile pairs between the real and synthetic data distributions.

![](images/15fa54b5c1650de1dccbaaebf0afa3d806a4419121a6db4dd64955540325df17.jpg)

![](images/53d61586e5c9d25e30241085f480f05863e9b92e4c1831feacf888bd9e03c9e1.jpg)

![](images/720b2ceb05733c61aa075db6ad7361c65497d498295fe0f7de56326606798cf1.jpg)

![](images/282abb8815ae7ee304826bc26534c188ee9e526e5b66a71c2d23e5b8e0d9e803.jpg)  
Figure 2: Q–Q plots of LANL data flow inter-arrival times: generated vs ground truth.

TempoNet closely tracks the diagonal across datasets, indicating strong fidelity. NetShare diverges sharply at higher quantiles, producing overly long delays. GReaT performs better at lower quantiles but underestimates at the tail. $\mathrm { B N _ { b i n s } }$ shows dataset-dependent artifacts, including step-like quantization on CIDDS. Overall, TempoNet offers the most realistic inter-arrival time modeling.

Boxplots of daily seasonality.

Figure 3 shows hour-of-day trends for CIDDS (LANL in Appendix B (Figure 9)). TempoNet is the only model to closely reproduce the daily rhythms–e.g., mid-day peaks and overnight lulls, which others generate flat or noisy distributions. This suggests that TempoNet captures periodicity at both coarse and fine scales.

![](images/bde4f33f03ccaa3cb3c13313e8fac9daaaa401b644ee841d7a6764a2377288c2.jpg)  
Figure 3: Daily seasonality - CIDDS dataset.

Boxplots of weekly seasonality. Weekly trends are shown in Figure 4 for LANL (DC in Appendix B (Figure 10)). TempoNet again most closely mirrors the ground truth, while $\mathrm { B N _ { b i n s } }$ captures rough trends with some variance. GReaT and NetShare fail to match the pattern, producing flatter or distorted outputs.

![](images/741a080aea3f1a83ee5c864cc5d6d38d8db9cbdd323cedc8fc007b85725a79c2.jpg)  
Figure 4: Weekly seasonality - LANL dataset.

Summary. Across datasets and metrics, TempoNet demonstrates the strongest temporal fidelity, replicating both micro-level timing and macro-level seasonal patterns. Other models lag due to inconsistent or oversimplified generation of temporal features.

## 6.4. Host IP pair-level fidelity.

We evaluate the realism of host IP selection by comparing the distribution of packets or flows across the top 30 most active source/destination IP pairs in each dataset. Figure 5 shows results for LANL; results for CIDDS and DC are in Appendix B (Figures 11 and 12).

For the LANL Dataset, TempoNet and $\mathrm { { B N _ { b i n s } } }$ closely match the real distribution, capturing the relative proportions across host pairs. GReaT moderately aligns but overestimates the 2 most active host pairs. NetShare underestimates across the board, failing to reflect the skew in real traffic.

For CIDDS (Figure 11 in Appendix B), TempoNet again aligns well, especially for high-activity pairs. $\mathrm { B N _ { b i n s } }$ underestimates top pairs but preserves general trends. GReaT overestimates the dominant pairs and shows less accurate overall modeling.

![](images/fa86b483967fa8e34ea16d5bb3bd417d04d72d7693fe616ba69608531518e647.jpg)  
Figure 5: Host Pair Analysis - LANL dataset.

For DC (Figure 12 in Appendix B), TempoNet, $\mathrm { B N _ { b i n s } }$ and GReaT track the overall shape but exhibit localized deviations. NetShare performs poorly, producing flat, unrealistic distributions.

Summary. TempoNet consistently delivers the best host pair fidelity, maintaining both global trends and fine-grained variations across datasets. $\mathrm { B N _ { b i n s } }$ performs well on the LANL dataset but struggles with the other 2 datasets with larger host spaces. GReaT ranks third overall, while Net-Share exhibits the weakest alignment.

## 6.5. Training Time and Model Size Comparison

Table 4 summarizes the training times and model sizes (measured by number of trainable parameters) for each method. NetShare required substantially more memory (1.5 TB RAM) and parallel CPU resources (10 cores), reflecting the high cost of training GANs on complex tabular data. Moreover, NetShare’s publicly available implementation does not support GPU acceleration, further contributing to its extended runtime.

In contrast, all other models—including TempoNet—were trained using a single NVIDIA H100 GPU (96GB VRAM), with 1 CPU core and 100GB system memory. Among them, GReaT required the longest training time and had the largest model size, with over 80 million parameters. Despite its scale, GReaT did not consistently outperform other models, highlighting the cost-performance trade-off in large LLM-based generators.

TempoNet, by comparison, is two orders of magnitude smaller than GReaT, yet achieved comparable or superior results across realism, diversity, and security utility metrics. This highlights the architectural efficiency of combining multi-task learning with a structured temporal model. $\mathrm { { B N } _ { \ b i n s } , }$ while extremely compact and fast to train, underperformed on metrics requiring temporal fidelity. These results demonstrate that TempoNet strikes a compelling balance between modeling capacity, speed, and scalability.

## 6.6. Impact on Intrusion Detection Performance

While generating attack traffic is relatively straightforward—via red teaming in staging environments, replaying previously captured exploits, or automating attacks using known toolchains, the greater challenge lies in simulating the complex, dynamic behavior of real users—the benign background traffic. Without this, intrusion detection systems (IDS) risk being trained on unnaturally clean data, and cyber range exercises can lose operational realism, making detection trivially easy due to the lack of natural network noise.

TABLE 4: Model training time and size.

<table><tr><td>Dataset</td><td>Model</td><td>Train Time (min)</td><td># Params</td></tr><tr><td rowspan="4">LANL</td><td>NetShare</td><td>&gt;3,000</td><td>179,369</td></tr><tr><td>GReaT</td><td>42.14</td><td>81,912,576</td></tr><tr><td> $BN_{bins}$ </td><td>0.02</td><td>4,652</td></tr><tr><td>TempoNet</td><td>4.90</td><td>41,976</td></tr><tr><td rowspan="3">CIDDS</td><td>GReaT</td><td>146.00</td><td>81,912,576</td></tr><tr><td> $BN_{bins}$ </td><td>0.08</td><td>13,518</td></tr><tr><td>TempoNet</td><td>29.7</td><td>68,629</td></tr><tr><td rowspan="4">DC</td><td>NetShare</td><td>&gt;3,000</td><td>179,369</td></tr><tr><td>GReaT</td><td>195.0</td><td>81,912,576</td></tr><tr><td> $BN_{bins}$ </td><td>0.04</td><td>135,059</td></tr><tr><td>TempoNet</td><td>29.7</td><td>128,494</td></tr></table>

To assess whether TempoNet addresses this gap, we evaluated its utility in supporting anomaly-based intrusion detection. This is not a benchmark of IDS performance, but a test of whether synthetic benign traffic preserves enough realism to support effective security tasks. We conducted a three-stage evaluation using the CIDDS-001 dataset:

(1) Synthetic Benign Traffic Generation: We trained TempoNet on the benign portion of the CIDDS-001 dataset and generated synthetic background traffic, previously eval uated in Sections 6.1 and 6.3.

(2) Integration of Real Attacks: We overlaid real, labeled attack flows from the CIDDS-001 test set onto the synthetic benign traffic, preserving original timestamps to maintain realistic temporal context. These attacks are used solely for evaluation and are never seen during training.

(3) Evaluation on Real Data: We evaluate anomaly detectors trained only on benign traffic and tested on a heldout week of CIDDS-001 containing both benign and attack flows, to avoid data leakage and mirror deployment conditions. For each training source (real, TempoNet-generated, GReaT-generated), we fit: i) an Isolation Forest on pointwise flow features; (ii) a sequence LSTM autoencoder over fixed-length windows L, scoring by mean squared reconstruction error; and (iii) a One-Class SVM (RBF). For all three, the decision threshold/hyperparameters are chosen on a benign-only validation split, then held fixed for testing (eg. for the LSTM Autoencoder we fixed the anomaly threshold at the 92nd percentile of reconstruction errors). We report class-specific F1 (benign/attack) and overall accuracy.

Results. Table 5 shows that TempoNet largely preserves detector behavior. For Isolation Forest and the LSTM Autoencoder, TempoNet tracks Real closely (all metric deltas $\leq 0 . 0 3 )$ . For the One-Class SVM, TempoNet shows a small but consistent drop (≈−0.01 Benign-F1, −0.04 Attack-F1, −0.02 Accuracy), yet remains far closer to Real than the GReaT LLM background.

By contrast, the GReaT LLM background exhibits reduced benign fidelity: it inflates One-Class SVM performance while markedly degrading LSTM Autoencoder attack detection (requiring a substantially looser threshold to recover near-real scores), indicating distortions of higherorder/temporal statistics that change class separability.

Takeaway. TempoNet is task-faithful: swapping Real→TempoNet leaves IDS decisions essentially unchanged for tree and sequence models and only modestly shifts a kernel detector, whereas the LLM background induces non-faithful, detector-dependent shifts (inflations or degradations).

TABLE 5: IDS evaluation on CIDDS dataset.

<table><tr><td>IDS</td><td>Metric</td><td>Real</td><td>TempoNet</td><td>GReaT LLM</td></tr><tr><td rowspan="3">Isolation Forest</td><td>Benign F1</td><td>0.95</td><td>0.95</td><td>0.86</td></tr><tr><td>Attack F1</td><td>0.73</td><td>0.70</td><td>0.72</td></tr><tr><td>Accuracy</td><td>0.92</td><td>0.91</td><td>0.82</td></tr><tr><td rowspan="3">LSTM Autoencoder</td><td>Benign F1</td><td>0.97</td><td>0.98</td><td>0.95</td></tr><tr><td>Attack F1</td><td>0.84</td><td>0.83</td><td>0.50</td></tr><tr><td>Accuracy</td><td>0.95</td><td>0.96</td><td>0.91</td></tr><tr><td rowspan="3">One-Class SVM</td><td>Benign F1</td><td>0.970</td><td>0.960</td><td>0.992</td></tr><tr><td>Attack F1</td><td>0.845</td><td>0.803</td><td>0.955</td></tr><tr><td>Accuracy</td><td>0.950</td><td>0.933</td><td>0.987</td></tr></table>

## 7. Discussion & Future Directions

In this work, we introduced TempoNet, a temporal point process (TPP)-based generative model for network traffic simulation. TempoNet demonstrated strong performance across key metrics, including realism, diversity, novelty, and compliance, outperforming state-of-the-art GAN, LLM, and Bayesian Network-based approaches in many areas. While other models capture certain temporal trends, TempoNet is the only approach that consistently models both fine-grained and high-level seasonality across datasets. This fidelity to temporal patterns is essential for applications requiring realistic and dynamic network simulations, such as cyber range training, cyber deception, and networking tasks like intrusion and anomaly detection.

## 7.1. Discussion

Temporal Fidelity for Security and Simulation: TempoNet’s ability to replicate temporal seasonality provides significant advantages across both security and networking applications. In intrusion detection systems (IDS), particularly those based on anomaly detection, the accuracy of benign traffic modeling has a direct impact on false positive rates and overall detection reliability. Much of the existing IDS benchmarking literature focuses on injecting attack traffic into synthetic or anonymized traces, often overlooking the importance of realistic background dynamics. This can lead to overfitting and misleading performance evaluations.

TempoNet addresses this gap by capturing complex temporal patterns—such as daily and weekly seasonality—that reflect real-world usage. In operational training scenarios, particularly in cyber ranges, accurate simulation of benign traffic is essential for both realistic defender experience and reliable performance testing of defence mechanisms. Likewise, in cyber deception systems, realistic temporal dynamics help create engaging environments that sustain adversary interaction and reduce detectability. Beyond security-specific applications, TempoNet-generated datasets also have the potential to benefit broader networking tasks, including telemetry analysis, predictive maintenance, and benchmarking network performance under realistic, timevarying conditions.

Forecasting and Prediction: A unique strength of TPPbased models is their ability to forecast event sequences. While our current focus is on simulation, TempoNet’s architecture can naturally extend to predictive tasks. Its lognormal mixture model allows not only the generation of future traffic patterns but also the estimation of their likelihood, making TempoNet a valuable tool for proactive tasks such as capacity planning, anomaly detection, and predictive maintenance in network management.

Comparison with Existing Methods: TempoNet addresses gaps in existing methods by integrating TPPs with multi-task learning. GAN-based models, such as NetShare, show strength in reproducing numerical marginal feature distributions but struggle with temporal dependencies. LLMbased models, like GReaT, handle categorical features effectively but lack explicit temporal modeling. Bayesian Networks (e.g., BN<sub>bins</sub>) capture static correlations but fail to replicate dynamic patterns.

TempoNet uniquely combines fine-grained temporal modeling with broader seasonal patterns while preserving relationships among header fields, positioning it as a superior solution for diverse use cases. Its use of a flexible, multi-modal log-normal mixture distribution enables rich sampling across the learned data manifold, eliminating the need for explicit diversity-enhancement mechanisms. The architecture is trained to model the overall data distribution rather than memorize individual instances, which naturally promotes generalization and sample-level diversity. This is supported by our Coverage and Density metrics, which quantify how broadly the generated data spans the support of the real distribution.

Regarding novelty, our use of the Membership Disclosure (MD) metric confirms that TempoNet avoids direct memorization. While MD is typically used as a privacy metric, it also serves as a proxy for sample uniqueness, helping to demonstrate that synthetic data points deviate sufficiently from the training set. Together, these results suggest that TempoNet achieves both high fidelity and meaningful novelty, without requiring additional mechanisms for diversity control.

## 7.2. Limitations and Future Work

Limitations: Despite its strengths, TempoNet has several limitations. First, while it captures daily and weekly rhythms well, sparse events remain challenging. The lognormal mixture, being smooth, has a tendency to either overgenerate around rare events or omit them entirely. Second, capturing multiple seasonalities (hourly, daily, weekly) remains difficult—metadata helps with individual cycles, but not with their interactions. Third, long-range dependencies such as rare bursts or gradual drifts are hard to model across multiple time scales. Fourth, the model synthesizes only packet- and flow-header fields rather than payloads, which narrows applicability for payload-centric tasks (e.g., deep packet inspection). Fifth, our evaluation focuses on anomaly-based IDS scenarios, leaving open questions about how well TempoNet-generated traffic supports other IDS paradigms (e.g., signature-based or hybrid systems). Finally, dataset recency remains a limitation: modern, long-duration traces with multi-week coverage are scarce, though we selected datasets with sufficient structural and temporal diversity—including an IoT dataset—for current benchmarks. These constraints highlight the importance of caution when generalizing results, particularly for edge cases or environments underrepresented in our datasets.

Future Work: Addressing these limitations creates several promising directions. Short-term priorities include refining the mixture component to better capture rare bursts and long-term drifts, alongside formal privacy evaluations (e.g., differential privacy guarantees, membership inference testing) to ensure robust protection when releasing synthetic traces. We also aim to validate TempoNet in operational settings by training IDS, stress-testing security tools, and enhancing cyber range training outcomes. Longer-term, expanding to multi-modal data (e.g., payloads, applicationlayer metadata) will enable more comprehensive simulations, while exploring TempoNet for traffic prediction could support early anomaly detection, resource optimization, and proactive defense. Finally, hybrid architectures that integrate TempoNet’s temporal modeling with large language models (LLMs) may combine field-level semantic fidelity with explicit temporal dynamics, advancing both simulation and forecasting in network security.

## 8. Related Work

TPPs for network traffic event modeling. Temporal Point Processes (TPPs) have been widely applied to capture temporal dynamics in network traffic. BURSE [7] and Moore et al. [8] used Markov-modulated Poisson and Hawkes Processes, respectively, to reproduce burstiness and detect changes in flow. Saha et al.’s NTPP [9] combined RMTPP with learning-to-rank, modeling self-excitation and host contention. Price-Williams and Heard [10] proposed a Wold process outperforming Hawkes for inter-arrival time modeling.

These methods model fine-grained timing but typically focus on a small number of features (e.g., timestamps), limiting realism for broader simulation tasks. Beyond network traffic, TPPs have also been applied to social media [16], [31] and spatio-temporal event modeling [24], [25], but existing models rarely scale beyond two marks. Our work extends this line by modeling 7–8 header fields per event, combining temporal fidelity with full-header realism—marking the first such high-fidelity multi-attribute TPP.

ML-based network traffic simulation. ML-based traffic simulation. GAN-based DoppelGANger [18] and its successor NetShare [4] led early efforts in synthetic header trace generation. NetShare extends DoppelGANger to improve fidelity and privacy, but remains unable to model inter-arrival times and is highly resource-intensive (e.g., requiring 200 CPU cores in the original study), creating reproducibility barriers. These issues highlight the trade-off between realism and accessibility in GAN-based methods.

Autoregressive models like STAN [17] use CNNs and mixture density networks for multivariate timeseries, but largely focus on intra-host patterns and lack inter-host dy namics. Diffusion models [30], [32] show promise but are limited by slow inference, making them impractical for highthroughput simulation tasks such as cyber range scenarios.

Encore [22] employs VAEs with GRUs to model flow sizes between host pairs but does not generalize to other attributes or capture full-network dynamics. In contrast, our method offers an efficient, temporally aware alternative that scales to rich, full-header representations needed for highfidelity security applications.

## 9. Conclusion

This paper presented TempoNet, a novel approach to network traffic simulation that combines temporal point processes with multi-task learning to generate high-fidelity packet-header and flow-header traces. Our evaluation on real-world NetFlow and pcap datasets demonstrates TempoNet’s ability to model all header fields while preserving intricate temporal relationships, significantly outperforming existing methods. The log-normal mixture model TPP component proves particularly effective at capturing complex temporal patterns, including daily and weekly variations, that previous approaches struggled to represent. Beyond its strong performance across realism, diversity, and compliance metrics, TempoNet’s ability to generate authentic background traffic addresses a critical need in cybersecurity training and testing environments. These capabilities position TempoNet as a valuable tool for creating more realistic cyber ranges, enabling better training outcomes and more reliable system evaluations.

Importantly, many existing public benchmark datasets used in IDS research contain simulated or anonymized traffic and rely on simplistic background distributions. These datasets limit the generalizability of detection models and under-represent the operational complexity faced by security analysts. Our work addresses this gap by providing a foundation for realistic, temporally coherent background traffic that can be used to train and evaluate intrusion detection models under realistic network load conditions. Future evaluations with TempoNet-enhanced datasets will better reflect the challenges of detecting threats amidst complex, time-varying benign traffic—providing a more credible basis for security model assessment.

## Acknowledgment

This work has been supported by the Cyber Security Research Centre Limited, whose activities are partially funded by the Australian Government’s Cooperative Research Centres Programme.

## References

[1] S. Mases, K. Maennel, M. Toussaint, and V. Rosa, “Success factors ¨ for designing a cybersecurity exercise on the example of incident response,” in 2021 IEEE European Symposium on Security and Privacy Workshops (EuroS&PW). IEEE, 2021, pp. 259–268.

[2] V. Paxson, “End-to-end internet packet dynamics,” in Proceedings of the ACM SIGCOMM’97 conference on Applications, technologies, architectures, and protocols for computer communication, 1997, pp. 139–152.

[3] S. E. Coull, C. V. Wright, F. Monrose, M. P. Collins, M. K. Reiter et al., “Playing devil’s advocate: Inferring sensitive information from anonymized network traces.” in Ndss, vol. 7, 2007, pp. 35–47.

[4] Y. Yin, Z. Lin, M. Jin, G. Fanti, and V. Sekar, “Practical gan-based synthetic ip header trace generation using netshare,” in Proceedings of the ACM SIGCOMM 2022 Conference, 2022, pp. 458–472.

[5] Z. Lin, A. Jain, C. Wang, G. Fanti, and V. Sekar, “Using gans for sharing networked time series data: Challenges, initial promise, and open questions,” in Proceedings of the ACM Internet Measurement Conference, 2020, pp. 464–483.

[6] V. Borisov, K. Sessler, T. Leemann, M. Pawelczyk, and G. Kasneci, “Language models are realistic tabular data generators,” in The Eleventh International Conference on Learning Representations, 2023.

[7] J. Yin, X. Lu, X. Zhao, H. Chen, and X. Liu, “Burse: A bursty and self-similar workload generator for cloud computing,” IEEE Transactions on Parallel and Distributed Systems, vol. 26, no. 3, pp. 668–680, 2015.

[8] M. G. Moore and M. A. Davenport, “Analysis of wireless networks using hawkes processes,” in 2016 IEEE 17th International Workshop on Signal Processing Advances in Wireless Communications (SPAWC). IEEE, 2016, pp. 1–5.

[9] A. Saha, N. Ganguly, S. Chakraborty, and A. De, “Learning network traffic dynamics using temporal point process,” in IEEE INFOCOM 2019 - IEEE Conference on Computer Communications, 2019.

[10] M. Price-Williams and N. A. Heard, “Nonparametric self-exciting models for computer network traffic,” Statistics and Computing, vol. 30, no. 2, pp. 209–220, 2020.

[11] I. O. Lopes, D. Zou, I. H. Abdulqadder, S. Akbar, Z. Li, F. Ruambo, and W. Pereira, “Network intrusion detection based on the temporal convolutional model,” Computers & Security, vol. 135, p. 103465, 2023.

[12] P. F. de Araujo-Filho, M. Naili, G. Kaddoum, E. T. Fapi, and Z. Zhu, “Unsupervised gan-based intrusion detection system using temporal convolutional networks and self-attention,” IEEE Transactions on Network and Service Management, 2023.

[13] W. Wang, Y. Sheng, J. Wang, X. Zeng, X. Ye, Y. Huang, and M. Zhu, “Hast-ids: Learning hierarchical spatial-temporal features using deep neural networks to improve intrusion detection,” IEEE Access, vol. 6, pp. 1792–1806, 2018.

[14] C. Palm, Intensitatsschwankungen im Fernsprechverkehr¨ , ser. Ericsson technics. L. M. Ericcson, 1943. [Online]. Available: https://books.google.com.au/books?id=5cy2NQAACAAJ

[15] A. G. Hawkes, “Spectra of some self-exciting and mutually exciting point processes,” Biometrika, vol. 58, 1971.

[16] O. Shchur, M. Bilos, and S. Gˇ unnemann, “Intensity-free learning of¨ temporal point processes,” in International Conference on Learning Representations, 2019.

[17] S. Xu, M. Marwah, M. Arlitt, and N. Ramakrishnan, “Stan: Synthetic network traffic generation with generative neural models,” in Deployable Machine Learning for Security Defense: Second International Workshop, MLHat 2021, Virtual Event, August 15, 2021, Proceedings 2. Springer, 2021, pp. 3–29.

[18] Z. Lin, A. Jain, C. Wang, G. Fanti, and V. Sekar, “Generating high-fidelity, synthetic time series datasets with doppelganger,” arXiv preprint arXiv:1909.13403, 2019.

[19] A. Schoen, G. Blanc, P.-F. Gimenez, Y. Han, F. Majorczyk, and L. Me, “A tale of two methods: Unveiling the limitations of gan and the rise of bayesian networks for synthetic network traffic generation,” in 2024 IEEE European Symposium on Security and Privacy Workshops (EuroS&PW). IEEE Computer Society, 2024, pp. 273–286.

[20] D. K. Kholgh and P. Kostakos, “Pac-gpt: A novel approach to generating synthetic network traffic with gpt-3,” IEEE Access, 2023.

[21] O. Shchur, A. C. Turkmen, T. Januschowski, and S. G¨ unnemann,¨ “Neural temporal point processes: A review,” in Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence, IJCAI-21, Z.-H. Zhou, Ed. International Joint Conferences on Artificial Intelligence Organization, 8 2021, pp. 4585–4593, survey Track. [Online]. Available: https://doi.org/10.24963/ijcai.2021/623

[22] S. Huang, L. Peng, M. Wang, Y. Liu, Z. Liu, X. Wang, and Y. Cui, “Datacenter network deserves better traffic models,” in Proceedings of the 22nd ACM Workshop on Hot Topics in Networks, 2023, pp. 124–130.

[23] K. Moore, C. J. Christopher, D. Liebowitz, S. Nepal, and R. Selvey, “Modelling direct messaging networks with multiple recipients for cyber deception,” in 2022 IEEE 7th European Symposium on Security and Privacy (EuroS&P), 2022.

[24] R. T. Chen, B. Amos, and M. Nickel, “Neural spatio-temporal point processes,” in International Conference on Learning Representations, 2020.

[25] Z. Zhou, X. Yang, R. Rossi, H. Zhao, and R. Yu, “Neural point process for learning spatiotemporal event dynamics,” in Learning for Dynamics and Control Conference. PMLR, 2022, pp. 777–789.

[26] M. J. Turcotte, A. D. Kent, and C. Hash, “Unified host and network data set,” in Data science for cyber-security. World Scientific, 2019, pp. 1–22.

[27] M. Ring, S. Wunderlich, D. Grudl, and et al., “Creation of flow-based¨ data sets for intrusion detection,” Journal of Information Warfare, vol. 16, no. 4, pp. 41–54, 2017.

[28] T. Benson, A. Akella, and D. A. Maltz, “Network traffic characteristics of data centers in the wild,” in Proceedings of the 10th ACM SIGCOMM conference on Internet measurement, 2010, pp. 267–280.

[29] A. Alsaedi, N. Moustafa, Z. Tari, A. Mahmood, and A. Anwar, “Ton iot telemetry dataset: A new generation dataset of iot and iiot for data-driven intrusion detection systems,” Ieee Access, vol. 8, pp. 165 130–165 150, 2020.

[30] X. Jiang, S. Liu, A. Gember-Jacobson, P. Schmitt, F. Bronzino, and N. Feamster, “Generative, high-fidelity network traces,” in Proceedings of the 22nd ACM Workshop on Hot Topics in Networks, 2023, pp. 131–138.

[31] J. R. Zipkin, F. P. Schoenberg, K. Coronges, and A. L. Bertozzi, “Point-process models of social network interactions: Parameter estimation and missing data recovery,” European journal of applied mathematics, vol. 27, no. 3, pp. 502–529, 2016.

[32] N. Sivaroopan, D. Bandara, C. Madarasingha, G. Jourjon, A. P. Jayasumana, and K. Thilakarathna, “Netdiffus: network traffic generation by diffusion models through time-series imaging,” Computer Networks, p. 110616, 2024.

[33] M. Ring, S. Wunderlich, D. Grudl, and et al., “Flow-based benchmark¨ data sets for intrusion detection,” in Proceedings of the 16th European conference on cyber warfare and security. ACPI, 2017, pp. 361–369.

[34] N. Du, H. Dai, R. Trivedi, U. Upadhyay, M. Gomez-Rodriguez, and L. Song, “Recurrent marked temporal point processes: Embedding event history to vector,” in Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining. ACM, 2016, pp. 1555–1564.

[35] S. Zuo, H. Jiang, Z. Li, T. Zhao, and H. Zha, “Transformer hawkes process,” in International conference on machine learning. PMLR, 2020, pp. 11 692–11 702.

## Appendix

## A. Dataset Details

For our study, our focus on capturing long-term temporal dynamics necessitated the use of datasets spanning at least 3 weeks. As a result, several commonly used datasets were excluded due to the limited timeframe of data captured, which precluded the analysis of important temporal effects in network traffic patterns. Previous works ensure manageable dataset sizes through the use of custom-made synthetic datasets [17], by capping the number of records of realworld datasets (effectively restricting their duration) [4], [17], [19], [22], [30], or by restricting the number of hosts [17], [22]. To maintain a manageable dataset size while preserving the extended timeframe, we restrict the dataset to a subset of hosts, as detailed for each dataset below. This methodology allowed us to balance the need for a comprehensive temporal perspective with practical constraints on data volume. By doing so, we ensured our dataset captured the full spectrum of temporal variations, including daily and weekly patterns, which are crucial for developing high-fidelity network traffic generation models.

Required timespan for training data. While our study uses 3-week spans for three of the dataset, this choice was intentional: it enables evaluation of how well models capture long-term temporal patterns, such as workday vs. weekend activity and diurnal cycles. However, TempoNet does not require a full week of data to function effectively. In settings where fine-grained temporal seasonality is less critical, such as evaluating static intrusion detection rules or testing network infrastructure readiness, models can be trained on smaller samples, including traces as short as a single day or hour, provided they capture the key node-level communication structure.

The primary tradeoff of using less data is a reduction in temporal coverage and structural diversity. Rare services and behaviors, as well as weekly usage rhythms, may be under-represented, which can limit the generality of the generated traffic for downstream tasks. Nevertheless, TempoNet remains applicable across a wide range of dataset sizes, allowing deployment in environments with limited historical data availability.

Dataset Composition. Here is the metadata description for the datasets:

(NetFlow-1) LANL: The Unified Host and Network Dataset [26] is a subset of network and computer (host) events collected from the Los Alamos National Laboratory enterprise network. We take 4 weeks worth of communications between a subset of 52 nodes, amounting to 202,841 NetFlow records. LANL has one dominant, highly active node (12.6% of flows), followed by a broad middle tier where 75% of nodes each contribute between 1–5.5% of flows; only 4% of source IPs send less than 0.1% of flows.

(NetFlow-2) CIDDS: CIDDS [27], [33] emulates a small business network environment, featuring multiple clients and servers (e.g., email, web) with scripted benign user activities as well as real-world external traffic. The dataset creators incorporate injected malicious traffic to create comprehensive datasets for intrusion detection evaluation, however we sample only from the benign data. We took a subset of 140 most active nodes and sampled 10% of their communications over 4 weeks of data collection, amounting to 655,359 NetFlow records. CIDDS has one dominant, highly active node (15.3% of flows), a substantial middle tier where 29% of IPs each contribute 1–7.5% of traffic, and a pronounced long tail with 60% of IPs each sending less than 0.1%.

(NetFlow-3) IoT-TON (IoT): We use the ToN IoT network-flow subset [29], collected from a heterogeneous IoT/IIoT testbed across multiple sites. The dataset is labgenerated rather than drawn from continuous enterprise traffic, and exhibits irregular temporal consistency (many hours contain no flows, while others exceed 6K). After preprocessing we obtain 92 hours of data, amounting to 255,045 flows.

A key complication is that the train and test subsets differ markedly in their marginal distributions, producing atypical “Real” baseline scores in Table 1. This mismatch limits the dataset’s use for precise model benchmarking, but makes it valuable as a robustness stress test. Indeed, traffic distribution is highly polarized: 78% of IPs each contribute less than 0.1% of flows, while a handful of devices dominate up to 40% individually. We therefore retain IoT primarily to probe model behavior under distribution shift and extreme skew, rather than to serve as a direct analogue of enterprise traces.

(PCAP) Data Center (DC): The DC dataset utilzes the packet capture ”UN1” from the data center studied in the IMC 2010 measurement paper [28]. We utilize a subnetwork of 192 most active nodes to obtain 779,364 pcap records. DC has three highly active nodes (9.5%, 10.5%, and 12.4% of flows), a moderate middle tier where 12.5% of nodes each contribute 1–4.5%, and about 12% of IPs send less than 0.1% of traffic.

Taken together, these four datasets provide a spectrum of network dynamics: LANL with one elephant and a broad middle tier, DC with three elephants and a moderate tail, CIDDS with one elephant and an overwhelming population of mice, and IoT-Ton with extreme polarization between a handful of super-elephants and a large majority of tiny contributors. This diversity ensures that TempoNet is evalu-

![](images/d8c6b1a368047f0a97636fea1edda1f801968ef407eec99aa52075aed60d6db9.jpg)

(a) Histograms of per-source IP flow shares across datasets.  
![](images/b21040f1901084590c6d7d93badce28f40bea523f8445a36fff494f288efa0e5.jpg)  
(b) Complementary cumulative distribution function (CCDF) of per-source IP flow shares.

Figure 6: Activity skew across datasets. The CCDF (left) highlights heavy-tailed behavior, while the histograms (right) illustrate the distribution of flow shares across IPs. Together, these plots show that LANL, CIDDS, DC, and IoT-Ton each exhibit distinct skew profiles (see text for details).

ated across both enterprise and IoT settings, under balanced, long-tail, and highly polarized traffic conditions. The corresponding activity histograms and complementary cumulative distribution functions (CCDFs) are shown in Figure 6.

## B. Additional Visualizations and Analyses

This appendix includes additional visualizations referenced in Sections 6.3 and 6.4, which could not be included in the main paper due to space constraints. These include Q–Q plots, seasonality boxplots (daily and weekly), and host IP pair distributions for datasets not shown in the main text. Together, these plots offer a more complete view of the generative models’ temporal and structural fidelity.

1. Temporal Fidelity and Failure Cases. Figures 7 and 8 present Q–Q plots of flow inter-arrival times for CIDDS and IoT datasets, respectively. These visualizations highlight where generative models diverge from real temporal dynamics.

![](images/615ac655975afd8b3d880aa8b44e58ded316ca049926b3e5f8b8a6011ab4ef26.jpg)

![](images/ffa539571683f847f28f95935981893556b2c80a992f8ff257c823bdf3fc4f37.jpg)

![](images/f276fb21c4df98d84cf9f885ada311ea6d183214cd0275e0dfc269f9c27906e6.jpg)  
Figure 7: Q–Q Plots of CIDDS Data Flow Inter-arrival Times: Generated Vs Ground Truth.

![](images/33222d679322de0bb405d8deb38efec781a651bafbf4307ea4fc9f9697952eaa.jpg)

![](images/c51a5cb6e20372a2eadfc9d3b4bad653e24f51b771db3e2c88485e5d1ac81b28.jpg)

![](images/7189c60e3fa9db0af188a6062046ae2e80ce7ea99d4137c022adaf04d7af1647.jpg)  
Figure 8: Q–Q Plots of IOT Data Flow Inter-arrival Times: Generated Vs Ground Truth.

For CIDDS (Figure 7), TempoNet aligns closely with the diagonal across lower and mid quantiles, faithfully reproducing short-to-moderate gaps between flows. Divergence emerges in the tail, where it underproduces very long interarrival times. By contrast, GReaT LLM compresses spacing (inflating mid-quantiles, truncating tails), while $\mathrm { B N _ { b i n s } }$ collapses diverse timings into a narrow range due to its discretization. Overall, TempoNet better captures heavytailed variability, though extreme sparsity remains difficult.

For IoT (Figure 8), all models struggle. $B N _ { b i n s }$ (panel a) collapses almost entirely: its quantiles remain near zero, producing a flat line instead of following the diagonal. This indicates that the baseline fails to reproduce the heavy-tailed inter-arrival distribution, instead generating unrealistically dense bursts with no long idle times.

GReaT LLM (panel b) captures short inter-arrival times moderately well, with lower quantiles tracking the diagonal, but diverges sharply for longer gaps. Beyond ∼50 seconds, the generated values severely underrepresent the long-tail structure of IoT traffic, effectively cutting off extreme delays. In addition, we observed pathological artefacts: some samples contained inter-arrival times far beyond the valid support, with one exceeding 144,000 years. Such behavior highlights how unconstrained text-to-sequence generation can produce implausible temporal values. The net effect is unrealistic traces dominated by bursts, without the long idle periods that occur in practice when IoT devices sleep or remain inactive.

TempoNet (panel c) aligns much more closely with the real distribution across the bulk of inter-arrival times (0–100 seconds), showing that it can represent both short and moderate temporal gaps. However, it truncates the extreme tail: beyond ∼100 seconds, the model underproduces very long idle periods. While this reduces extreme outliers, it also omits a genuine feature of IoT traffic—sporadic device activity separated by long gaps—which is essential for fully realistic simulation.

These plots highlight complementary failure modes across models. $\mathrm { B N _ { b i n s } }$ collapses temporal diversity into unrealistically dense bursts, while GReaT both truncates long gaps and occasionally produces pathological outliers (e.g., inter-arrival times on the order of $1 4 4 { , } 0 0 0$ years). TempoNet avoids such extremes and reproduces realistic short-tomoderate timings more faithfully, but still under-represents the rare, very long idle periods that characterize IoT traffic. Together, these results show that while TempoNet provides the most balanced temporal fidelity, reproducing heavytailed sparsity across scales remains an open challenge.

2. Additional Visualizations. In addition to the temporal fidelity analysis above, we also provide the following seasonality and host-pair fidelity plots across datasets. The seasonality boxplots (Figures 9 and 10) complement Section 6.3, confirming that TempoNet more faithfully reproduces daily and weekly cycles than either baseline. The host-pair fidelity plots (Figures 11 and 12 extend Section 6.4, showing that TempoNet captures the empirical head–tail structure more faithfully than baselines. On CIDDS, $\mathrm { B N _ { b i n s } }$ systematically under-generates the most prominent source–destination pairs, while GReaT heavily over-generates them, inflating the top four pairs well beyond their true frequencies. On DC, GReaT disperses mass erratically across implausible pairs, and NetShare broadly over-disperses, flattening the natural head–tail structure. TempoNet avoids these extremes, striking a closer balance with the real distributions. These supplementary figures are consistent with the quantitative scores reported in the main text, reinforcing that the trends observed for selected datasets generalize across benchmarks.

## C. Compliance Check

The Domain Knowledge Check (DKC) is implemented as a set of 20 lightweight plausibility rules that flag semantically or physically implausible netflow records. The rules are not intended to enforce strict protocol compliance, but rather to identify clearly unrealistic samples (e.g., HTTP traffic over UDP, flows with payload sizes smaller than the minimum Ethernet header, or ICMP flows carrying nonzero byte counts).

Each generated flow is evaluated against all rules, and the DKC score is computed as the proportion of rules violated. Importantly, these rules are applied post hoc for evaluation only: the generative models have no knowledge of them during training. Even real traffic can occasionally violate some rules, reflecting natural variability and noise in network traces.

![](images/1732fc7e6a76fade689575ea6a221f4d18ce9f3fe4af517eb4cea70415ae7f05.jpg)

Figure 9: Daily seasonality of events in LANL dataset: Generated Vs Ground Truth.  
![](images/06994095d56dd0014901841d383cc85081892aba614113e7ca23ce89a67538a9.jpg)  
Figure 10: Weekly seasonality - DC dataset.

![](images/be2a6a5d8361cad97dbe5be8656c9f069c8249221d434537ef88bf94b3bdd29e.jpg)  
Figure 11: Host Pair Analysis - CIDDS dataset.

Table 6 enumerates the full set of rules used in our evaluation. The implementation follows the public codebase of Schoen et al. [19].<sup>2</sup>

DKC Violations. TempoNet exhibits an elevated DKC violation rate on the CIDDS dataset. The most frequently violated constraint requires that flows with service ports 80, 443, 8000, 25, 587 should not target private 192.168.\* addresses. While this rule encodes a sensible expectation for enterprise traffic—where such ports typically indicate external web or mail servers—it is also violated in the CIDDS

![](images/3f5119ff7add409ee0759a9742a28ec978911eb64a830fa11f5690dc18a602b5.jpg)  
Figure 12: Host Pair Analysis - DC dataset.

TABLE 6: Domain Knowledge Check (DKC) rules used to flag implausible netflow records. The implementation follows that Schoen et al. [19] (https://github.com/hallavar/ SyntheticNetflowEvaluation).

<table><tr><td>#</td><td>Rule Description</td></tr><tr><td>1</td><td>TCP traffic on ports reserved for UDP services (53, 137, 138, 5353, 1900, 67, 3544, 8612, 3702, 123).</td></tr><tr><td>2</td><td>UDP traffic on ports typically associated with TCP services (80, 443, 8000, 25, 993, 587, 445, 84, 8088, 8080).</td></tr><tr><td>3</td><td>Destination port 0 with non-ICMP/IGMP traffic.</td></tr><tr><td>4</td><td>ICMP flows with nonzero outgoing bytes.</td></tr><tr><td>5</td><td>ICMP flows with nonzero outgoing packets.</td></tr><tr><td>6</td><td>IGMP flows with nonzero incoming or outgoing bytes.</td></tr><tr><td>7</td><td>NetBIOS/SSDP ports (137, 138, 1900) with nonzero incoming bytes.</td></tr><tr><td>8</td><td>NetBIOS/SSDP ports (137, 138, 1900) with nonzero incoming packets.</td></tr><tr><td>9</td><td>NetBIOS/SSDP ports (137, 138, 1900) not sent to broadcast addresses (.255).</td></tr><tr><td>10</td><td>Flows targeting local/private IPs (192.168.) on external service ports (80, 443, 8000, 25, 587).</td></tr><tr><td>11</td><td>External IPs using local-only service ports (993, 67).</td></tr><tr><td>12</td><td>DNS port 53 flows not directed to a DNS-labeled destination.</td></tr><tr><td>13</td><td>Multicast DNS port 5353 flows not directed to expected group addresses.</td></tr><tr><td>14</td><td>Non-TCP flows with non-empty TCP flag fields.</td></tr><tr><td>15</td><td>Incoming payload smaller than Ethernet header size (bytes &lt; 42 × packets).</td></tr><tr><td>16</td><td>Outgoing payload smaller than Ethernet header size (bytes &lt; 42 × packets).</td></tr><tr><td>17</td><td>Incoming payload larger than maximum frame size (bytes &gt; 65535 × packets).</td></tr><tr><td>18</td><td>Outgoing payload larger than maximum frame size (bytes &gt; 65535 × packets).</td></tr><tr><td>19</td><td>Negative or malformed durations.</td></tr><tr><td>20</td><td>Inconsistent duration/packet relations (e.g., zero duration with multiple packets, or nonzero duration with only a single packet).</td></tr></table>

training and test sets due to dataset construction artefacts. In lab-generated environments, services are often simulated within private address ranges, and in real networks, proxies or relays may legitimately run on internal hosts. TempoNet reproduces these patterns (albeit at a higher rate) rather than correcting them, as it is optimised for statistical fidelity rather than semantic validity. This highlights an important limitation of DKC evaluation: some constraints, while intuitive, are not universally valid across datasets. Future work could refine constraint sets by context or integrate such rules as soft penalties during training to reduce violations.

Beyond this primary rule, two further categories of violations emerged. First, certain violations appeared only in generated traffic: port-53 flows not mapping to DNS servers, and NetBIOS/SSDP traffic (ports 137, 138, 1900) targeting unicast rather than broadcast addresses. These cases reflect TempoNet’s imperfect capture of protocol semantics in CIDDS, as they are absent from the ground truth. Second, other violations were present in both training and generated data—for example, flows with UDP-only service ports (DNS, NetBIOS, SSDP, DHCP, NTP) incorrectly appearing with TCP as the transport protocol. Such cases point to inconsistencies in the source datasets (e.g., NetFlow artefacts or synthetic traces), which the model mirrors rather than correcting. Together, these findings illustrate how DKC evaluation can reveal both dataset–rule mismatches and genuine modelling artefacts, underscoring the need for constraintaware generation or post-processing filters in future work.

## D. Expanded Related Work

TPPs for network and event modeling. Prior TPPbased models like BURSE [7] used Markov Modulated Poisson Processes to capture burstiness and self-similarity in workloads. Moore and Davenport [8] applied a multivariate Hawkes Process to trace datasets, enabling learning of topologies and change detection. NTPP [9] integrates RMTPP [34] with discriminative learning-to-rank modules, modeling bursty dynamics and contention among hosts. Price-Williams and Heard [10] proposed a non-parametric Wold process, outperforming Hawkes in modeling NetFlow event timing.

Beyond network traffic, TPPs have been widely applied in social and communication networks (e.g., email, Reddit, Stack Overflow) [16], [23], [31], [35], and in spatio-temporal event prediction (e.g., earthquakes, disease spread, urban mobility, and neural spike trains) [24], [25]. These works model event timestamps and marks, but typically support only one or two marks. In contrast, our work models seven (PCAP) or eight (NetFlow) marks per event, a significant leap in modeling complexity and application fidelity.

GAN-based traffic models. NetShare [4] builds on DoppelGANger [18] to improve inter- and intra-epoch fidelity via fine-tuning and private training. However, Net-Share does not reproduce inter-arrival time distributions, limiting its realism in time-sensitive domains. Moreover, its computational footprint is substantial—requiring 200 CPU cores and nearly 2 TB RAM across 10 Cloudlab nodes. These compute requirements pose reproducibility challenges, especially for researchers with constrained access. A notable example is the Purdue CS536 Fall 2022 class project, whose GitHub repo documents the difficulties faced in reproducing NetShare due to limited resources.

Diffusion models. Recent efforts apply diffusion models to traffic synthesis, including text-to-traffic paradigms [30] and image-transformed flows [32]. Despite promising results, the inference speed remains a major bottleneck due to their multi-step sampling procedures. This constraint makes diffusion models impractical for real-time or high-frequency scenarios like cyber range training.

Other models. Encore [22] uses VAEs and GRUs to model the temporal dependency of flow sizes across host pairs. However, it only models flow sizes and does not support full header reconstruction. STAN [17] captures intrahost dependencies using CNNs and probabilistic layers but struggles with inter-host traffic realism.
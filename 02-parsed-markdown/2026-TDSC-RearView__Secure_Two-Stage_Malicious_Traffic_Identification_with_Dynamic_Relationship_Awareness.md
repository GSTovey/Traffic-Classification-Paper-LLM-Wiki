# RearView: Secure Two-Stage Malicious Traffic Identification with Dynamic Relationship Awareness

Peng Fang, Ziming Zhao, Member, IEEE, Ziqi Yang, Yixin Jiang, Wenqian Xu, Zhihong Liang, Fan Zhang, Member, IEEE

Abstract—High-throughput enterprise networks face increasingly sophisticated cyber threats, making dependable and realtime malicious traffic detection a cornerstone of cyber security and operational resilience. Existing methods suffer from two critical flaws: lightweight intra-flow approaches lack servicespecific discrimination, leading to high false negatives against mimicry attacks; meanwhile, static graph-based inter-flow methods incur prohibitive latency and memory costs, failing to adapt to dynamic network environments. To address these issues, we propose RearView, a two-stage dynamic relationship-aware framework for real-time malicious traffic identification. First, it deploys service-personalized Variational Autoencoders (VAEs) to rapidly screen and filter out benign traffic. Second, for the remaining suspicious flows, RearView constructs dynamic session graphs and applies anomaly-weighted graph neural networks to uncover hidden inter-flow attack patterns. A streaming cache mechanism ensures this relational mining remains highly efficient and adaptable. Extensive evaluations on four benchmark datasets and one self-constructed CrossAttack dataset show that RearView achieves an average F1-score of 97.79%, outperforming stateof-the-art methods by 10.19% on average. It reduces the false positive rate by 4.99% and false negative rate by 34.44%, while attaining a significantly lower detection latency than contemporary methods of the same type, and exhibits robust resistance against mimicry and data pollution attacks.

Index Terms—Malicious traffic identification, dynamic graph, service-personalized VAE, graph self-supervised learning.

## I. INTRODUCTION

N recent years, enterprise networks have become the frontline of escalating sophisticated cyberattacks, ranging from high-volume Distributed Denial-of-Service (DDoS) and ransomware to highly clandestine Advanced Persistent Threats (APTs) [1], [2]. A defining and formidable trait of these modern threats is their ability to mimic legitimate network behaviors, effectively hiding in plain sight to bypass conventional signature-based or coarse-grained statistical detection mechanisms [3], [4]. Consequently, achieving real-time, high-fidelity malicious traffic identification has become a cornerstone for ensuring the dependability and operational resilience of enterprise infrastructures [5], [6]. Despite extensive research, existing systems still struggle to satisfy the “iron triangle” of security requirements: high accuracy for stealthy threats, sub-millisecond latency for real-time mitigation, and robust adaptability to high-throughput dynamic traffic [7]. These deficiencies stem from two unresolved, fundamental gaps.

![](images/d35178feca64874b87457f98fc8dde587e554f9ddb0283115c4f1b26ea5e27e7.jpg)  
Fig. 1: The proportion of similarity intervals between malicious and benign behaviors with intra-flow features.

First, multi-service traffic conflation leads to unresolvable feature ambiguity for intra-flow based methods. Most prevailing methods rely heavily on intra-flow features (e.g.,, packet length, inter-arrival time, entropy [8], [9], [10], [11]) but treat the diverse ecosystem of benign traffic as a monolithic entity [12], [13]. This “one-size-fits-all” modeling ignores the intrinsic behavioral heterogeneity across services [14]: HTTP traffic exhibits bursty short-packet patterns, while SSH sessions feature persistent, fixed-structure encrypted payloads [15]. When these distinct profiles are conflated, the decision boundary between benign and malicious activities becomes critically obscured. As illustrated in Figure 1, our empirical analysis across five datasets reveals staggering feature overlap: over 31% of malicious sessions in UNSW-NB15 [16] share 30%-40% intra-flow similarity with benign ones, and this overlap reaches 68.78% (90%-100% similarity interval) in our CrossAttack dataset. This ambiguity grants attackers a “mimicry window” that existing intra-flow methods cannot overcome, as they lack service-specific contextualization to distinguish between genuine benign traffic and mimicked malicious traffic.

Second, static Graph Neural Networks (GNNs) suffer from rigidity and label dependency, hindering real-time deployment. To capture inter-flow dependencies (e.g., lateral movement in APTs), GNNs have been introduced [5], [17], but they face a dual bottleneck: (i) Static Graph Paralysis: Most models adopt a batch-wise paradigm, requiring global graph construction from static traffic snapshots before inference [18],

JOURNAL OF LAT<sub>E</sub>X CLASS FILES, VOL. 14, NO. 8, AUGUST 202

[19]. This introduces prohibitive latency and fails to adapt to transient traffic bursts (e.g., IoT flash crowds), violating real-time requirements for high-throughput networks. (ii) Label Dependency: Supervised GNNs demand massive, high-quality adversarial labels. However, zero-day threats and novel APTs are inherently sparse, leading to severe class imbalance, overfitting to known signatures [20], and rendering these models ineffective against emerging threats.

To surmount these barriers, we propose RearView, a novel two-stage framework that decouples rapid benign suppression from deep relational mining through an asymmetric filtering architecture. In the first stage, RearView deploys Service-Personalized Attention-augmented VAEs. Unlike generic models, RearView learns protocol-specific “normalcy” boundaries to eliminate the feature ambiguity exploited by mimicry attacks. This allows for the high-speed filtration of massive benign flows using only lightweight intra-flow features. The second stage targets the remaining suspicious flows by constructing an incremental dynamic session graph. To prevent stealthy attack signals from being diluted during graph aggregation, we propose an anomaly-weighted GraphSAGE-DGI (Deep Graph Infomax) architecture. This mechanism uses anomaly priors from the first stage to weight inter-flow relationships, capturing subtle causalities (e.g., lateral movement) without the overhead of global graph reconstruction or the need for exhaustive attack labels.

The primary contributions of this work are fourfold:

• Service-Personalized Representation Learning: To mitigate the feature ambiguity inherent in serviceagnostic models, we introduce attention-augmented VAEs tailored to specific network protocols. By leveraging service-aware context to disentangle overlapping traffic patterns, RearView significantly reduces false negatives in complex multi-service environments.

• Dynamic Relational Awareness via Self-Supervision: We develop a dynamic session-based graph evolution mechanism coupled with GraphSAGE-DGI. This approach not only eliminates the overhead of global graph reconstruction but also enhances the system’s ability to generalize to unseen zero-day APTs through selfsupervised node embedding.

• Adaptive Resource Management with Streaming Cache: To overcome the memory overhead of continuous graph updates, we implement a FIFO-based streaming cache. This mechanism maintains a fresh view of active session states while strictly bounding resource usage, ensuring efficient performance in high-speed networks.

• Rigorous Empirical Validation: Extensive evaluations on four benchmark datasets and a specialized CrossAttack dataset show that RearView achieves an average F1- score of 97.79%. It outperforms state-of-the-art (SOTA) methods by 10.19% on average while maintaining the low-latency profile required for production enterprise networks.

The remainder of this paper is organized as follows: Section II reviews existing related work. Section III defines the threat model. Section IV presents the technical methodology of the proposed framework. Section V provides comprehensive experimental evaluations and ablation analyses. Section VI discusses the limitations of this work and presents future directions. Finally, Section VII concludes this paper.

## II. RELATED WORK

## A. Intra-flow Feature based Attack Detection

Traditional malicious traffic detection methods primarily leverage intra-flow statistical features, such as packet size distributions, inter-arrival times, and protocol-specific metadata [8], [9], [10], [21], [22]. Flow-centric systems (e.g., FOSS [11]) adopt machine learning classifiers to analyze aggregated flow statistics [23], [24], while they offer computational efficiency, they remain vulnerable to adversarial evasion via traffic morphing [25]. Packet-based approaches [26], [27], [28], [29] improve detection granularity by inspecting payloads and header fields, yet they struggle with encrypted traffic and scalability in high-throughput networks. Recent advances like FlowPic [13] encode flow statistics into imagelike representations for convolutional network analysis, but they fail to distinguish highly similar intra-flow patterns. Methods such as ET-BERT [12] and Trafficformer [30] leverage pre-trained language models for byte-level sequence analysis, yet they overlook inter-flow contextual dependencies. These shortcomings highlight the inherent vulnerability of singlemodal intra-flow methods to feature obfuscation and mimicry attacks.

## B. Graph based Attack Detection

Graph-based detection methods have been developed to model inter-flow contextual relationships, overcoming the limitations of isolated intra-flow analysis [31], [32], [17]. Most of these methods construct static graphs (with IPs, packet lengths, or sessions as nodes) to capture spatial dependencies, but they cannot adapt to the dynamic evolution of attacks. Temporal GNN frameworks including Trident [18], ProGraph [33], and WTAGRAPH [34] strengthen temporal sequence modeling, yet they lack effective mechanisms for fusing crossmodal features. MEMG [35] integrates Markov chains with GNNs to model encrypted traffic as first-order Markov chain graphs, but it incurs excessive computational overhead in large-scale network scenarios. Two core challenges persist for existing graph-based approaches: (i) static graph structures cannot capture temporal causality in multi-stage attacks; and (ii) rigid edge definitions struggle to model indirect adversarial connections. Notably, many graph-based methods rely heavily on Deep Packet Inspection (DPI), which renders them ineffective for encrypted traffic [36]. For example, Kwon et al. [37] analyzed download relationship graphs to detect malware downloads (similar to WebWitness [38]); Invernizzi et al. [39] used graphs constructed from plaintext traffic to locate malware infrastructure. In contrast, RearView constructs interaction graphs without parsing specific application-layer headers, enabling task-agnostic detection of encrypted traffic.

JOURNAL OF LAT<sub>E</sub>X CLASS FILES, VOL. 14, NO. 8, AUGUST 2021

## C. Self-Supervised Learning and Graph Representation

Label scarcity and the evolving nature of zero-day attacks drive the shift from supervised to self-supervised learning for network anomaly detection, which learns robust representations from unlabeled benign traffic [40], [41], [42]. Generative models (e.g., VAEs, GANs) are foundational, defining traffic normalcy via reconstruction error [43], [44]. However, they overfit low-level noise and fail to capture high-level semantic anomalies [45], spurring contrastive learning (CL). CL learns discriminative features by maximizing consistency across flow augmentations [46]; SmartDetector further optimizes CL for encrypted traffic obfuscation [47]. However, CL ignores topological dependencies between flows, leading to graph self-supervised learning (GSSL). GSSL uses mutual information (MI) maximization (pioneered by DGI [48]) to capture structural context. State-of-the-art GSSL methods, such as Anomaly-E [49] and TCG-IDS [50], have exhibited superior performance in malicious traffic detection. Yet these approaches mostly operate on static graph snapshots and employ uniform MI maximization, leading to inadequate sensitivity to the dynamically evolving structural perturbations in network traffic. Recently, the research community has moved toward more sophisticated architectural designs for GSSL, including Masked Graph Transformers and graph contrastive learning frameworks with advanced hard negative mining strategies [51], [52]. These advanced GSSL architectures boost graph representation discriminability but rely on static snapshot modeling and incur heavy computational overhead, rendering them unsuitable for real-time detection in dynamic high-throughput networks.

RearView transcends these limitations by addressing the signal dilution and temporal blindness inherent in current GSSL frameworks. First, unlike uniform MI maximization that allows dominant benign traffic to drown out subtle anomalies, RearView introduces anomaly-weighted MI maximization. By leveraging anomaly priors of the first stage, it selectively amplifies the structural influence of suspicious flows. Second, moving beyond rigid static snapshots, RearView’s dynamic session-graph architecture continuously captures the evolving temporal causality of multi-stage attacks. Empowered by a streaming cache, this synergy achieves high-fidelity zero-day detection without the prohibitive computational overhead that limits current state-of-the-art graph models.

## III. THREAT MODEL AND DESIGN GOALS

Adversary Model. We target sophisticated adversaries (external or insider) employing multi-dimensional evasion techniques to bypass detection systems. These include: (i) traffic morphing to mimic legitimate patterns [53], [54], [7], [55], inducing high intra-flow similarity with benign traffic; (ii) strategic perturbation of statistical features (e.g., packet size distribution, inter-arrival time) to confuse supervised classifiers; and (iii) stealthy anomalies designed to evade unsupervised methods by hiding within the normal variance of unlabeled data. Adversaries may also poison training data with mislabeled samples or inject adversarial examples into inference pipelines. Focusing on encrypted traffic (e.g., SSL/TLS,

SSH), our framework analyzes packet header distributions and behavioral patterns to maintain effectiveness across encrypted communication scenarios.

Design Goals. RearView is designed with three core objectives to address critical limitations in existing traffic detection systems. (i) it must enable generic detection across both encrypted and unencrypted traffic. This ensures adversaries cannot evade detection through traffic encryption [56], [57], [58], as the framework operates independently of payload visibility. (ii) it requires real-time high-speed processing capabilities. Specifically, it must classify encrypted traffic as malicious or benign with minimal detection latency, ensuring compatibility with high-throughput network environments. (iii) it employs unsupervised detection, eliminating reliance on prior knowledge of encrypted malicious traffic. This enables detection of zeroday attacks, i.e., previously undisclosed threats with unknown patterns [7] without using labeled traffic datasets for model training. Notably, these requirements remain unaddressed by existing detection methods [59], highlighting the need for RearView’s novel design.

## IV. DESIGN DETAILS OF REARVIEW

## A. Overview

RearView is predicated on a two-stage asymmetric filtering architecture designed to balance real-time efficiency with highfidelity detection. Rather than treating network defense as a monolithic task, we decouple the process:

Stage 1: Conditional Single-Flow Screening. (§ IV-B) This stage acts as a high-speed filter. It extracts transport-layer statistics from raw flows and routes them into Service-Personalized Attention-VAEs. The goal is to rapidly eliminate the vast majority of benign traffic using only intra-flow features, thereby reducing the computational burden on the system.

Stage 2: Relationship-Aware Graph Refinement. (§ IV-C) For the remaining suspicious flows that exhibit feature ambiguity, this stage shifts to structural analysis. It constructs an incremental dynamic session graph and leverages an anomalyweighted GraphSAGE-DGI model. By combining Stage 1 anomaly priors with inter-flow topologies, it uncovers stealthy coordinated attacks and outputs the final binary classification.

## B. Stage 1: Conditional Single-Flow Screening

The primary objective of Stage 1 is to implement an asymmetric filtering mechanism that achieves maximum benign traffic suppression with minimal computational overhead. By anchoring representation learning to specific service contexts, RearView establishes a fine-grained boundary of normalcy, effectively mitigating the feature ambiguity that attackers exploit during mimicry or obfuscation attacks.

## 1) Service-Centric Grouping and Formalization

Network traffic is inherently heterogeneous. A generic “onesize-fits-all” model often fails to capture the subtle behavioral nuances of individual protocols [14]. By partitioning traffic into service-specific clusters, we transform a complex multiclass anomaly detection problem into a series of simplified, highly specialized one-class modeling tasks.

![](images/3634aaa2d5e57768fa06d758ad76fd34d6b04a2375aa3a34df7a13930b4490e9.jpg)  
Fig. 2: Architecture overview of RearView: two-stage VAE-guided graph-based malicious traffic detection.

![](images/9e07089def005766ec492f85c9fa2e75e534bfa66435b14ded43f3fe7eff2527.jpg)  
Fig. 3: Traffic session graph based on triplets. The vertices in the graph are (ip, port, protocol). The edges in the graph represent sessions.

We formalize the network environment as a collection of persistent services. Each service is uniquely identified by a Service Triplet τ , defined as:

$$
\tau = (i p, p o r t, p r o t o c o l)\tag{1}
$$

For each $\tau ~ \in ~ \mathcal { T } ~ \left( e . g . , ~ \tau ~ = ~ \left( 1 9 2 . 1 6 8 . 1 . 1 , 4 4 3 , 6 \right) \right)$ , we aggregate all associated sessions into a dedicated cluster $\mathcal { F } _ { \tau } = \{ f _ { 1 } , f _ { 2 } , \dotsc , f _ { n } \}$ . To ensure RearView remains robust against encrypted payloads, we extract a d-dimensional feature vector $\mathbf { x } \in \mathbb { R } ^ { d }$ for each flow, comprising transport-layer statistics such as packet size distributions, inter-arrival times, and TCP state flags (as detailed in Table I). Currently, RearView relies on a single transport-layer statistical modality. While effective, single-modality profiles are theoretically vulnerable to adaptive mimicry attacks that manipulate packet sizes and timings. However, RearView’s decoupled architecture is inherently feature-agnostic. Both the VAE and graph stages can seamlessly ingest application-layer metadata or payload features without structural modifications, easily accommodating future multimodal expansions.

To handle large-scale, dynamic environments where service identities may not be pre-configured, we employ a graphtheoretic pruning approach (Algorithm 1). By analyzing the structural properties of the triplet relationship graph (Fig. 3), we distinguish between transient client-side endpoints and persistent service-side anchors based on the inherent asymmetry of connection degrees.

TABLE I: TCP/UDP features for VAE model training.

<table><tr><td colspan="4">Feature</td><td>Dim.</td></tr><tr><td colspan="4">Protocol</td><td>1</td></tr><tr><td rowspan="2">Direction</td><td colspan="3">Sum</td><td rowspan="3">33</td></tr><tr><td>Frame</td><td>IP</td><td>TCP</td></tr><tr><td>Forward Backward Bi-dir</td><td>Packet_num Duration</td><td>Flags_df Flags_mf Flag_offset</td><td>ACK,URG PUSH,RESET SYN,FIN</td></tr><tr><td rowspan="2">Direction</td><td colspan="3">Statistic</td><td rowspan="3">72</td></tr><tr><td colspan="3">Max Min Mean Std</td></tr><tr><td>Forward Backward Bi-dir</td><td colspan="3">Total Length, Time_delta, Calculated Window Size, Scale_factor, Window, TTL</td></tr></table>

```txt
Algorithm 1 Autonomous Service Triplet Discovery
Input: Traffic data D
Output: Service triples T
for each session in D do
    Extract source tuple s = (sip, sport, proto)
    Extract destination tuple d = (dip, dport, proto)
    triples ← triples ∪ {(s, d)}
end for
Initialize G = (V, E) where V = ∅, E = ∅
for (s, d) ∈ triples do
    V ← V ∪ {s, d}, E ← E ∪ {(s, d)}
end for
Compute degree deg(v) = |{u ∈ V|(v, u) ∈ E}| ∀v ∈ V
remove ← ∅
for each node v ∈ V do
    neighbors ← {u ∈ V|(v, u) ∈ E}
    if ∀u ∈ neighbors : deg(u) > deg(v) then
    remove ← remove ∪ {v}
    end if
end for
V' ← V \ remove,    E' ← {(u, v) ∈ E|u ∈ V' ∧ v ∈ V'}
G' = (V', E')
T ← {u ∈ V'|deg(u) > 1}
return T
```

## 2) Attention-Augmented Variational Representation Learning

While VAEs are effective for density estimation, standard architectures treat all input features with equal importance, which may allow low-level statistical noise to contaminate the latent space. We introduce an attention-augmented bottleneck to force the model to prioritize anomaly-sensitive semantic features. The overall architecture is illustrated in Figure $4 .$

![](images/8e3adcc98d9cdafea1df054d08e1821d3c18009010153f039bad92dac6aba00a.jpg)  
Fig. 4: The VAE architecture in RearView.

For each cluster $\mathcal { F } _ { \tau }$ , we deploy a specialized Attention-VAE. The encoder ${ \mathcal { E } } _ { \phi }$ maps input $\textbf { x } \in \ \mathbb { R } ^ { d }$ to a high-level feature map $\textit { h } \in \mathbb { R } ^ { m }$ . To resolve feature importance, we calculate a diagnostic attention vector α:

$$
\boldsymbol {\alpha} = \operatorname{sigmoid} \left(\mathbf {W} _ {a} h + \mathbf {b} _ {a}\right)\tag{2}
$$

The weighted representation $h ^ { \prime } = h \odot \alpha$ is then projected into the parameters of the latent distribution $q _ { \phi } ( { \bf z } | { \bf x } ) =$ $\mathcal { N } ( \mu , \mathrm { d i a g } ( \pmb { \sigma } ^ { 2 } ) )$ .

To ensure the learned representations are both compact and discriminative, we optimize the model using a modified Variational Lower Bound with sparsity constraints:

$$
\mathcal {L} (\phi , \theta) = \mathbb {E} _ {q _ {\phi} (\mathbf {z} | \mathbf {x})} [ \log p _ {\theta} (\mathbf {x} | \mathbf {z}) ] - \beta \mathrm{KL} (q _ {\phi} (\mathbf {z} | \mathbf {x}) \| p (\mathbf {z})) - \lambda \| \boldsymbol {\mu} \| _ {1}\tag{3}
$$

where $\pmb { \mu }$ denotes the mean vector of the latent Gaussian distribution approximated by the VAE encoder. The reconstruction term $\| \mathbf { x } - \hat { \mathbf { x } } \| _ { 2 } ^ { 2 }$ ensures data fidelity, while the β-weighted KL divergence controls the latent space smoothness. Crucially, the $L _ { 1 }$ penalty on $\pmb { \mu }$ encourages a sparse, structured latent organization, which is instrumental in isolating anomalous perturbations from multi-modal benign traffic.

## 3) KDE-driven Probabilistic Anomaly Scoring

The decision boundary for anomaly detection should not be a rigid hyperparameter. Instead, it must be derived from the empirical distribution of benign behavior to provide a statistically sound confidence measure.

To evaluate a test flow $\mathbf { x } ^ { * }$ , we first map it to the learned manifold to obtain two diagnostic metrics: (1) the reconstruction error $\epsilon ^ { * } = \lVert \mathbf { x } ^ { * } - \hat { \mathbf { x } } ^ { * } \rVert ^ { 2 }$ , representing data fidelity; and (2) the latent norm $d ^ { * } = \lVert \mathbf { z } ^ { * } \rVert ^ { 2 }$ , representing the regularity of the latent representation. To bridge these heterogeneous metrics into a unified, interpretable probability space, we employ nonparametric Kernel Density Estimation (KDE).

Let $\mathcal { M } _ { t r a i n } ~ = ~ \{ m _ { i } \} _ { i = 1 } ^ { N }$ be the set of metrics (either ϵ or d) computed from the benign training set. The empirical probability density function $\hat { f } _ { m } ( \cdot )$ is estimated as:

$$
\hat {f} _ {m} (m ^ {*}) = \frac {1}{N h _ {m}} \sum_ {i = 1} ^ {N} K \left(\frac {m ^ {*} - m _ {i}}{h _ {m}}\right), \quad m \in \{\epsilon , d \}\tag{4}
$$

where $K ( \cdot )$ denotes the Gaussian kernel and $h _ { m }$ is the bandwidth optimized via Silverman’s rule of thumb.

Directly using the density value $\hat { f } _ { m } ( m ^ { * } )$ is problematic for cross-service comparison due to varying density scales. We therefore calibrate the scoring by calculating the distribution of densities over the training set itself. We precompute the mean $\mu _ { \hat { f } _ { m } }$ and standard deviation $\sigma _ { \hat { f } _ { m } }$ of the densities of all benign training samples:

$$
\mu_ {\hat {f} _ {m}} = \frac {1}{N} \sum_ {i = 1} ^ {N} \hat {f} _ {m} (m _ {i}), \quad \sigma_ {\hat {f} _ {m}} = \sqrt {\frac {1}{N} \sum_ {i = 1} ^ {N} (\hat {f} _ {m} (m _ {i}) - \mu_ {\hat {f} _ {m}}) ^ {2}}\tag{5}
$$

For a test flow $\mathbf { x } ^ { * }$ , we compute its standardized statistical deviation (Z-score) as $z _ { m } = ( \hat { f } _ { m } ( m ^ { * } ) - \mu _ { \hat { f } _ { m } } ) / \sigma _ { \hat { f } _ { m } }$

To transform these deviations into an anomaly probability prob $\in \ [ 0 , 1 ]$ , we apply a modified sigmoid mapping. Since lower density values indicate a higher likelihood of an anomaly, the final joint Stage 1 anomaly score $p r o b _ { s f }$ is defined as:

$$
p r o b _ {s f} (\mathbf {x} ^ {*}) = \omega \cdot \phi (- z _ {\epsilon}) + (1 - \omega) \cdot \phi (- z _ {d})\tag{6}
$$

where $\begin{array} { r } { \phi ( x ) = \frac { 1 } { 1 + e ^ { - x } } } \end{array}$ is the logistic function, and $\omega \in [ 0 , 1 ]$ is a weighting coefficient that balances the contribution of reconstruction and latent space indicators.

To maintain topological continuity, all session states processed in Stage 1 are asynchronously synchronized to the Stage 2 streaming cache to maintain an up-to-date view of the network’s interaction graph. However, to preserve highthroughput efficiency, the resource-intensive graph refinement and inference processes are not executed globally. Instead, they are selectively triggered: a flow is flagged as a potential seed of interest if $p r o b _ { s f } ( { \bf x } ^ { * } ) ~ > ~ \tau _ { s f } ~ ( \tau _ { s f }$ refers to VAE anomaly threshold). Only when such statistically significant deviations are detected does RearView invoke the Stage 2 relational mining module to perform deep structural analysis. This probabilistic triggering framework ensures that RearView remains dormant during periods of routine benign activity, while maintaining the agility to investigate suspicious patterns within their full topological context.

## C. Stage 2: Relationship-Aware Graph Refinement

While Stage 1 provides rapid per-flow screening, isolated analysis remains vulnerable to stealthy, coordinated attacks that mimic benign statistical profiles. Stage 2 addresses this by shifting from individual features to inter-flow relational context. By modeling traffic as a dynamic interaction graph, we can amplify subtle anomaly signals through neighborhood aggregation and global-local alignment.

## 1) Dynamic Session Graph Construction

Traditional static graphs [19], [18] incur prohibitive latency and fail to adapt to transient traffic shifts. We need a lightweight, incremental structure that captures temporal causality while maintaining a bounded memory footprint for real-time deployment.

FIFO Caching and Anomaly Triggering. RearView maintains a fixed-length FIFO queue $Q = \{ s _ { 1 } , s _ { 2 } , . . . , s _ { L } \}$ to buffer sessions processed by Stage 1. Each session $s _ { i }$ retains its Stage-1 anomaly prior $p r o b _ { s f } ( x ^ { * } )$ (calculated via Eq.6) and latent encoding $\mu .$ The queue Q we designed has the following properties (as shown in Figure 5):

![](images/b9cf0d94f3a7f919cccc32a6126d98f360dc5b445cac57f28a4a80a564783653.jpg)  
Fig. 5: The graph construction process in RearView.

(i) First-In-First-Out Eviction. When $| Q | > L$ , the oldest session $s _ { 1 }$ is evicted to ensure bounded memory usage (sessions <sup>①</sup>, <sup>②</sup>, <sup>③</sup> and $\textcircled{4}$ in Figure 5), which is critical for long-term deployment in high-throughput networks.

(ii) Anomaly Proportion Monitoring. We compute the anomaly proportion $\rho$ of $Q$ as:

$$
\rho = \frac {1}{| Q |} \sum_ {s \in Q} \mathbb {I} (p r o b _ {s f} (s) > \tau_ {s f})\tag{7}
$$

where $\mathbb { I } ( \cdot )$ is the indicator function. Graph construction is triggered only when $\rho > \gamma$ and $| Q | \geq L$ , ensuring that computational resources are focused on suspicious traffic bursts.

Incremental Update and Retirement. We represent the buffered sessions as a directed session graph $\begin{array} { r l } { G } & { { } = } \end{array}$ (V, E, A, X), where nodes V denote IP endpoints and edges $E$ denote bidirectional interactions. A denotes the edge attribute matrix, where each entry $\mathbf { a } _ { u , v } \in \mathbf { A }$ is a feature vector encoding semantic details of the session between u and v. X represents the vertex attribute matrix, where each entry $\mathbf { x } _ { v } \in \mathbf { X }$ is a feature vector capturing properties of source IP or destination IP. To maintain temporal relevance, we implement a session retirement mechanism: once embeddings are generated, the first $p r o b _ { r e t i r e d }$ of sessions in queue $Q$ are evicted. This mechanism prevents stale sessions those no longer reflective of realtime traffic dynamics from distorting the current interaction patterns modeled in the session graph. Meanwhile, retaining the remaining $1 - p r o b _ { r e t i r e d }$ of sessions ensures the preservation of recent interaction cues, effectively avoiding discontinuity in subsequent session relationship mining. For the next queue $Q ^ { \prime }$ (after retirement/eviction), the graph $G ^ { \prime }$ is updated from $G$ via three operations: Vertices with active sessions in $Q ^ { \prime }$ retain their VAE-encoded attributes but update aggregated features. New edges from $Q ^ { \prime }$ are added with initialized anomaly weight. Vertices with no edges in two consecutive graph updates are pruned.

## 2) Anomaly-Weighted GraphSAGE-DGI

Standard GNNs employ uniform aggregation, which allows dominant benign patterns to “smear” or dilute subtle anomaly signals. Furthermore, local interactions must be aligned with the global structural context to distinguish coordinated threats from isolated noise.

Anomaly-Weighted Neighborhood Aggregation. To prioritize suspicious interactions, We design a directional anomalyweighted aggregation mechanism to amplify suspicious interaction cues, consisting of three steps:

(i) Weighted Message Construction (Message Function). For each directed edge $e _ { u , v } \in E$ (connecting source vertex u to destination vertex v), we first compute a weighted edge feature by scaling the original edge feature with the edge’s VAE anomaly probability. This ensures edges with higher anomaly scores contribute more to the neighborhood message.

Formally, let $\mathbf { e } _ { u , v } \in \mathbb { R } ^ { E _ { \mathrm { d i m } } }$ denote the original edge feature; $\omega _ { u , v } \in [ 0 , 1 ]$ denote the VAE anomaly probability of the edge; $\omega _ { u , v } ^ { \mathrm { e x p } } = \omega _ { u , v } \otimes { \bf 1 } _ { 1 \times E _ { \mathrm { d i m } } }$ denote the expanded anomaly weight. The weighted edge feature (message) sent from u to v is:

$$
\mathbf {m} _ {u \rightarrow v} = \mathbf {e} _ {u, v} \odot \omega_ {u, v} ^ {\mathrm{exp}}\tag{8}
$$

where $\odot$ denotes element-wise multiplication. This message, along with the expanded weight $\omega _ { u , v } ^ { \mathrm { e x p } }$ , is passed to the destination vertex v for aggregation.

(ii) Directional Neighborhood Aggregation (Reduce Function). To capture both “outgoing” and “incoming” interaction patterns (critical for distinguishing malicious behaviors like port scanning), we perform aggregation on two directional graphs: the original graph (for forward message passing) and its reversed graph (for in-neighborhoods).

For a vertex v, let $N _ { o u t } ( v ) ~ = ~ \{ u ~ \in ~ V ~ | ~ e _ { u , v } ~ \in ~ E \}$ denote the set of nodes initiating sessions to v. We deliberately designate this as the out-neighborhood $( N _ { o u t } )$ to strictly align with the message-passing mechanics of our GraphSAGE implementation: it represents the collection of source nodes from which relational messages physically flow outward along the directed edges to be aggregated at the destination vertex v. We aggregate the weighted messages from $N _ { o u t } ( v )$ using a weighted average, normalizing by the sum of expanded anomaly weights to avoid bias from varying neighborhood sizes. The aggregated feature is computed as:

$$
\mathbf {a g g} _ {\text { out }} (v) = \frac {\sum_ {u \in N _ {\text { out }} (v)} \mathbf {m} _ {u \rightarrow v}}{\sum_ {u \in N _ {\text { out }} (v)} \omega_ {u , v} ^ {\exp} + \epsilon}\tag{9}
$$

where $\epsilon = 1 0 ^ { - 8 }$ prevents division by zero.

We construct a reversed graph $G _ { \mathrm { r e v } }$ by flipping the direction of all edges in G. For $v ,$ its in-neighborhood in $G$ becomes the out-neighborhood in $G _ { \mathrm { r e v } }$ (denoted $N _ { \mathrm { i n } } ^ { \mathrm { r e v } } ( v ) )$ ). Repeating the weighted average process on $G _ { \mathrm { r e v } }$ gives the in-neighborhood aggregated feature:

$$
\mathbf {a g g} _ {\mathrm{in}} (v) = \frac {\sum_ {w \in N _ {\mathrm{in}} ^ {\mathrm{rev}} (v)} \mathbf {m} _ {w \rightarrow v} ^ {\mathrm{rev}}}{\sum_ {w \in N _ {\mathrm{in}} ^ {\mathrm{rev}} (v)} \omega_ {w , v} ^ {\exp , \mathrm{rev}} + \epsilon}\tag{10}
$$

where $\mathbf { m } _ { w  v } ^ { \mathrm { r e v } }$ and $\omega _ { w , v } ^ { \mathrm { e x p , r e v } }$ are the weighted message and expanded weight in $G _ { \mathrm { r e v } } ,$ , respectively.

In practice, we prioritize the in-neighborhood aggregated feature for final vertex embedding. By reversing original flow edges, the in-neighborhood of an attacker node aggregates all its outgoing sessions, which effectively captures malicious initiation patterns. The final vertex embedding after aggregation is:

$$
\mathbf {z} _ {v} ^ {(1)} = \operatorname{ReLU} \left(W _ {\text { node }} \cdot \mathbf {a g g} _ {\text { in }} (v) + \mathbf {b} _ {\text { node }}\right)\tag{11}
$$

where $W _ { \mathrm { n o d e } } ~ \in ~ \mathbb { R } ^ { H _ { \mathrm { d i m } } \times E _ { \mathrm { d i m } } }$ and $\mathbf { b } _ { \mathrm { n o d e } } \in \mathbb { R } ^ { H _ { \mathrm { d i m } } }$ are learnable parameters, and $H _ { \mathrm { d i m } } = 6 4$ is the hidden dimension.

![](images/d37bb8fcd3405373e3a4550f7676402c814574fa2ae060920e5f55a166ac2e62.jpg)  
Fig. 6: The GraphSAGE-DGI contrastive learning process.

(iii) Edge Embedding Reconstruction. After obtaining aggregated vertex embeddings, we reconstruct the final edge embedding by fusing the source vertex’s aggregated feature with the original edge feature. This preserves both relational context and fine-grained session details.

For edge $e _ { u , v } ,$ let $\mathbf { z } _ { u } ^ { ( 1 ) }$ denote the aggregated embedding of source vertex u. The concatenated feature for the edge is:

$$
\mathbf {c a t} _ {u, v} = \left[ \mathbf {z} _ {u} ^ {(1)} \mid \mathbf {e} _ {u, v} \right]\tag{12}
$$

where $\left[ \cdot \begin{array} { l } { } \end{array} \right] \cdot \mathbf { l }$ denotes feature concatenation. The final edge embedding is then:

$$
\mathbf {z} _ {e _ {u, v}} = W _ {\text { edge }} \cdot \mathbf {c a t} _ {u, v} + \mathbf {b} _ {\text { edge }}\tag{13}
$$

where $W _ { \mathrm { e d g e } } \in \mathbb { R } ^ { 6 4 \times ( H _ { \mathrm { d i m } } + E _ { \mathrm { d i m } } ) }$ and $\mathbf { b } _ { \mathrm { e d g e } } \in \mathbb { R } ^ { 6 4 }$ are learnable parameters. This design retains raw edge features alongside aggregated node representations. It prevents the stage-one anomaly prior from forming a closed feedback loop and preserves full capability to discover novel relational anomalies that may be missed by single-flow detection.

Self-Supervised Refinement with Anomaly-Aware DGI. To align edge embeddings with global graph structure and enhance the discriminability of relational patterns, we design an anomaly-aware Deep Graph Infomax (DGI) framework. This framework departs from vanilla DGI [48] by: (1) using edge embeddings (instead of node embeddings) as the core supervision unit; (2) constructing a global summary from genuine edge embeddings; (3) leveraging a bilinear discriminator to maximize mutual information (MI) between local edge features and the global graph context. The process is illustrated in Figure 6.

(i) Positive/Negative Edge Embedding Generation. The framework first generates two sets of edge embeddings: positive (genuine interaction patterns) and negative (distorted patterns) to form supervision pairs.

Positive Edge Embeddings: For the original graph $G \ =$ $( V , E , \mathbf { A } , \mathbf { X } )$ , we extract the edge embeddings as the positive set:

$$
\mathcal {Z} _ {\mathrm{pos}} = \left\{\mathbf {z} _ {e _ {u, v}} \mid e _ {u, v} \in E \right\}, \quad \mathbf {z} _ {e _ {u, v}} \in \mathbb {R} ^ {6 4}\tag{14}
$$

where $\mathbf { z } _ { e _ { u , v } }$ is the anomaly-weighted edge embedding from Eq. 13, and $| \mathcal { Z } _ { \mathrm { p o s } } | = | E |$ (number of edges in G).

Negative Edge Embeddings: To break genuine relational patterns, we corrupt the edge feature order while preserving node-edge topological connections. Specifically, we generate a random permutation $\pi$ of edge indices and reassign edge features to form a corrupted edge feature matrix $\mathbf { A } _ { \mathrm { c o r r u p t } } = \mathbf { A } [ \pi ]$

Feeding X and $\mathbf { A } _ { \mathrm { c o r r u p t } }$ into the encoder gives the negative edge embedding set:

$$
\mathcal {Z} _ {\text { neg }} = \left\{\mathbf {z} _ {e _ {u, v}} ^ {\text { corrupt }} \mid e _ {u, v} \in E \right\}, \quad \mathbf {z} _ {e _ {u, v}} ^ {\text { corrupt }} \in \mathbb {R} ^ {6 4}\tag{15}
$$

Here, $\mathbf { z } _ { e _ { u , v } } ^ { \mathrm { c o r r u p t } }$ retains the same node connection as $\mathbf { z } _ { e _ { u , v } }$ but has a mismatched edge feature, ensuring the negative set disrupts genuine interaction semantics without altering graph topology.

(ii) Anomaly-Aware Global Summary Construction. The global summary $\mathbf { s } \in \mathbb { R } ^ { 6 4 }$ is designed to capture the dominant interaction pattern of the original graph. Unlike vanilla DGI’s random node pooling, we construct s from positive edge embeddings:

$$
\mathbf {s} = \sigma \left(\frac {1}{| \mathcal {Z} _ {\mathrm{pos}} |} \sum_ {\mathbf {z} \in \mathcal {Z} _ {\mathrm{pos}}} \mathbf {z}\right)\tag{16}
$$

where: $\sigma ( \cdot )$ is the sigmoid function, ensuring numerical stability in subsequent MI calculation; The average pooling over ${ \mathcal { Z } } _ { \mathrm { p o s } }$ ensures s reflects the collective behavior of genuine edges. It is critical for aligning local edge embeddings with global graph context.

This design differs from weighted pooling to avoid overfitting to noisy high-anomaly edges, as verified in code comments where weighted pooling was deprecated in favor of simple averaging.

(iii) Bilinear Discriminator for MI Maximization. To distinguish between genuine (positive) and distorted (negative) edge embeddings, we use a bilinear discriminator that computes the MI between each edge embedding and the global summary. The discriminator’s core is a learnable weight matrix $W _ { \mathrm { d i s c } } \in \mathbb { R } ^ { 6 4 \times 6 4 }$ , initialized via uniform Xavier initialization.

For an edge embedding $\mathbf { z } \in \mathcal { Z } _ { \mathrm { p o s } }$ or $\mathcal { Z } _ { \mathrm { n e g } } .$ the discriminator output (MI score) is:

$$
\operatorname{score} (\mathbf {z}, \mathbf {s}) = \mathbf {z} \cdot W _ {\text { disc }} \cdot \mathbf {s}\tag{17}
$$

where · denotes matrix multiplication. This bilinear formulation captures non-linear dependencies between local edge features and the global summary. It is more expressive than vanilla dot-product MI calculation.

(iv) Self-Supervised Loss Function. The loss function maximizes MI for positive pairs $( \mathcal { Z } _ { \mathrm { p o s } } , \mathbf { s } )$ and minimizes MI for negative pairs $( \mathcal { Z } _ { \mathrm { n e g } } , \mathbf { s } )$ , using Binary Cross-Entropy with Logits Loss:

$$
\mathcal {L} _ {\mathrm{DGI}} = \mathcal {L} _ {\mathrm{BCE}} (\operatorname{score} (\mathcal {Z} _ {\text { pos }}, \mathbf {s}), \mathbf {1}) + \mathcal {L} _ {\mathrm{BCE}} (\operatorname{score} (\mathcal {Z} _ {\text { neg }}, \mathbf {s}), \mathbf {0})\tag{18}
$$

where $\mathbf { 1 } \in \mathbb { R } ^ { | \mathcal { Z } _ { \mathrm { p o s } } | }$ is a vector of ones (labeling positive pairs as “genuine”); $\mathbf { 0 } \in \mathbb { R } ^ { | \mathcal { Z } _ { \mathrm { n e g } } | }$ is a vector of zeros (labeling negative pairs as “distorted”);

$$
\mathcal {L} _ {\mathrm{BCE}} (p, y) = - \frac {1}{N} \sum_ {i = 1} ^ {N} \left(y _ {i} \log \sigma (p _ {i}) + (1 - y _ {i}) \log (1 - \sigma (p _ {i}))\right)
$$

This design ensures edge embeddings are not only discriminative at the local interaction level but also aligned with the global graph’s normal or abnormal patterns, which is critical for refining single-flow detection results.

## 3) Anomaly Detection

After fusing semantic priors and structural context, we require a robust, parameter-free detector to identify outliers in the resulting embedding space without relying on malicious labels. The refined embeddings $\mathbf { z } _ { e }$ are fed into a Cluster-Based Local Outlier Factor (CBLOF) model. During training, we use only edge embeddings from benign sessions to form $\mathcal { Z } _ { \mathrm { b e n i g n } } = \{ \mathbf { z } _ { e _ { i } } \mid e _ { i } \in E _ { \mathrm { b e n i g n } } \}$ . The CBLOF model is trained on ${ \mathcal { Z } } _ { \mathrm { b e n i g n } }$ . The cluster number K is chosen by maximizing the silhouette coefficient, which partitions the benign edge embeddings into $\mathcal { C } _ { 1 } , \ldots , \mathcal { C } _ { K }$ . Each cluster is defined by centroid $\begin{array} { r } { \pmb { \mu } _ { k } = \frac { 1 } { | \mathcal { C } _ { k } | } \sum _ { \mathbf { z } \in \mathcal { C } _ { k } } \mathbf { z } , } \end{array}$ radius $r _ { k } = \mathrm { m a x } _ { \mathbf { z } \in \mathcal { C } _ { k } } \| \mathbf { z } - \pmb { \mu } _ { k } \| _ { 2 }$ , and local threshold $\tau _ { k }$ (95th percentile of distances from $\pmb { \mu } _ { k }$ in $\mathcal { C } _ { k } )$ , avoiding manual tuning.

For test sessions, edge embeddings ${ \mathcal { Z } } _ { \mathrm { t e s t } } = \{ \mathbf { z } _ { e _ { i } } ^ { \mathrm { t e s t } } ~ | ~ e _ { j } ~ \in$ $E _ { \mathrm { t e s t } } \}$ are generated via pre-trained GraphSAGE-DGI, then input to CBLOF for outlier scoring. For $\begin{array} { r l r } { { \bf z } ^ { \mathrm { t e s t } } } & { { } \in } & { \mathcal { Z } _ { \mathrm { t e s t } } , } \end{array}$ $\mathrm { s c o r e } _ { \mathrm { o u t l i e r } } ( \mathbf { z } ^ { \mathrm { t e s t } } )$ quantifies two deviations: the Euclidean distance d to the nearest benign cluster $\mathcal { C } _ { \mathrm { n e a r e s t } } ~ ( d = \| \mathbf { z } ^ { \mathrm { t e s t } } -$ $\mu _ { \mathrm { n e a r e s t } } | | _ { 2 } )$ and the in/out-of-cluster status relative to the cluster radius $r _ { \mathrm { n e a r e s t } }$ . The scoring function is:

$$
\operatorname{score} _ {\text { outlier }} (\mathbf {z} ^ {\text { test }}) = \left\{ \begin{array}{l l} \frac {d}{r _ {\text { nearest }}} \cdot w _ {\text { far}} & d > r _ {\text { nearest }}, \\ \frac {d}{r _ {\text { nearest }}} \cdot w _ {\text { near }} & d \leq r _ {\text { nearest }}, \end{array} \right.\tag{19}
$$

where $w _ { \mathrm { f a r } }$ and $w _ { \mathrm { n e a r } }$ are data-driven scaling factors derived from the quantile ratios of distance distributions over $\mathcal { Z } _ { \mathrm { b e n i g n } }$ $\mathbf { z } ^ { \mathrm { t e s t } }$ is anomalous if its score exceeds global threshold θ, where θ is the 95th percentile of outlier scores computed on ${ \mathcal { Z } } _ { \mathrm { b e n i g n } }$ during training, ensuring consistent alignment with the normal distribution.

## V. EVALUATION

## A. Experiment Setup

Implementation Details. We conducted our experiments on an Ubuntu 22.04.5 server (Linux kernel version 6.8.0) featuring an Intel Xeon Platinum 8352M CPU. The program was executed on a single NVIDIA GeForce RTX 4090 GPU, which operated with the 560.35.03 driver version. The server was configured with 512GB of DDR4 memory, of which 29.27GB was being used. For implementation, we selected Python 3.10.18 as the programming language and leveraged the PyTorch framework (version 1.11.0, compatible with CUDA 12.6) to enhance the functionality and operational efficiency of our experimental workflows<sup>1</sup>. The hyperparameters used in RearView are presented in Table II.

Datasets. A series of public datasets is used for evaluation: (i) CICIDS2017 [60] dataset uses a proposed B-Profile system to generate the normal traffic, meanwhile, a series of intrusion behaviors is involved, including Brute Force, DDoS, etc. (ii) ACIIoT2023 [61] comes from a home IoT environment and simulates real-world scenarios through benign and malicious activities. The data collection lasted for five days and covered reconnaissance, DoS, brute force, and normal network traffic. (iii) UNSW-NB15 [16] dataset was created by the IXIA PerfectStorm tool in the Cyber Range Lab of UNSW Canberra for generating a hybrid of real modern normal activities and synthetic contemporary attack behaviours. The dataset includes 9 malicious behavior, for example Worms and Shell code etc.. (iv) CICAPT2024 [62] dataset contains more than 20 different attack techniques, grouped into eight main attack strategies that are mapped to APT attack scenarios, inspired by APT29 activities.

TABLE II: Hyperparameter settings.

<table><tr><td>parameter</td><td>Value</td><td>Section</td><td>Details</td></tr><tr><td> $\omega$ </td><td>0.9</td><td>IV-B3</td><td>Weighting coefficient in Eq. 6</td></tr><tr><td> $h_{dim}$ </td><td>128→64→32→16</td><td>IV-B2</td><td>VAE hidden dimension</td></tr><tr><td> $\tau_{sf}$ </td><td>0.6</td><td>IV-B2</td><td>VAE anomaly threshold</td></tr><tr><td> $lr_{\text{VAE}}$ </td><td>1e-4</td><td>IV-B2</td><td>VAE learning rate</td></tr><tr><td>epochs</td><td>50</td><td>IV-B2</td><td>Epochs set in VAE training</td></tr><tr><td>batch_size</td><td>32</td><td>IV-B2</td><td>Batch size set in VAE training</td></tr><tr><td>L</td><td>2000</td><td>IV-C1</td><td>FIFO queue length</td></tr><tr><td> $\gamma$ </td><td>1/L</td><td>IV-C1</td><td>Graph initiation threshold</td></tr><tr><td> $prob_{retired}$ </td><td>4/5</td><td>IV-C1</td><td>Graph retired proportion</td></tr><tr><td> $edge_{dim}$ </td><td>64</td><td>IV-C2</td><td>Embedding edge dimension</td></tr><tr><td> $lr_{\text{DGI}}$ </td><td>1e-3</td><td>IV-C2</td><td>Graph learning rate</td></tr><tr><td>epochs</td><td>100</td><td>IV-C2</td><td>Epochs set in graph training</td></tr></table>

To further verify the robustness of RearView, we set up a simulation environment locally and constructed a dataset (CrossAttack) containing cross-session correlation attacks. The construction and evaluation details are shown in Section V-C. This dataset is publicly available online<sup>2</sup>.

Baselines. We use six models as baselines, covering SOTA methods in the traffic analysis landscape. The models are DeepLog [63], FlowLens [23], Whisper [7], HyperVision [32], Trident [18], FOSS [11]. These methods encompass traditional machine learning algorithms and deep learning methods such as Recurrent Neural Networks (RNN). Note that for the baseline Trident [18], the original paper presents three single-class training methods (AE, GNN and RNN). We adopted the GNNbased one for its ability to capture inter-flow relationships. For log analysis-based method DeepLog [63], we used the logs of connections for detection and its original hyper-parameters setting to attain the best accuracy.

Metrics. To give a fair comparison, we employ evaluation metrics commonly used in traffic classification tasks, i.e., Overall Accuracy (Acc), Precision (Pre), Recall (Rec), Weighted F1- Score (F1), False Positive Rate (FPR) and False Negative Rate (FNR) [64].

## B. Performance Evaluation

We conducted unsupervised binary-class anomaly detection, using only benign traffic as the training set. We compared our method against 6 baseline approaches, with the experimental results presented in Table III. Among the results, RearView-VAE refers to the detection performance achieved by our model using only the service-specific VAE from the first stage, while RearView represents the comprehensive detection results of the two-stage framework. As shown in the table, RearView-VAE can achieve detection accuracy comparable to that of the baseline methods; however, it still suffers from a significant number of false positives and false negatives.

TABLE III: Unsupervised evaluation results w.r.t. Accuracy (ACC), Precision (Pre), Recall (Rec) and F1-Score (F1).

<table><tr><td rowspan="2">Dataset Model</td><td colspan="4">CICIDS2017 [60]</td><td colspan="4">ACIIoT2023 [61]</td><td colspan="4">UNSW-NB15 [16]</td><td colspan="4">CICAPT2024 [62]</td><td colspan="4">CrossAttack</td></tr><tr><td>ACC</td><td>Pre</td><td>Rec</td><td>F1</td><td>ACC</td><td>Pre</td><td>Rec</td><td>F1</td><td>ACC</td><td>Pre</td><td>Rec</td><td>F1</td><td>ACC</td><td>Pre</td><td>Rec</td><td>F1</td><td>ACC</td><td>Pre</td><td>Rec</td><td>F1</td></tr><tr><td>DeepLog</td><td>86.64</td><td>87.28</td><td>86.64</td><td>86.77</td><td>80.13</td><td>78.89</td><td>80.13</td><td>79.37</td><td>72.50</td><td>70.04</td><td>72.50</td><td>69.52</td><td>85.58</td><td>97.64</td><td>85.58</td><td>91.07</td><td>90.72</td><td>91.76</td><td>90.72</td><td>90.83</td></tr><tr><td>FlowLens</td><td>84.48</td><td>85.07</td><td>84.48</td><td>84.62</td><td>83.58</td><td>82.42</td><td>83.58</td><td>82.72</td><td>71.03</td><td>68.12</td><td>71.03</td><td>68.06</td><td>88.35</td><td>97.68</td><td>88.35</td><td>92.66</td><td>86.99</td><td>87.96</td><td>86.99</td><td>87.14</td></tr><tr><td>Whisper</td><td>91.53</td><td>92.22</td><td>91.53</td><td>91.66</td><td>86.38</td><td>86.95</td><td>86.38</td><td>86.62</td><td>75.60</td><td>74.25</td><td>75.60</td><td>72.99</td><td>91.13</td><td>97.72</td><td>91.13</td><td>94.21</td><td>93.04</td><td>93.44</td><td>93.04</td><td>93.09</td></tr><tr><td>HyperVision</td><td>92.95</td><td>93.82</td><td>92.95</td><td>93.08</td><td>93.27</td><td>93.62</td><td>93.27</td><td>93.39</td><td>84.62</td><td>84.29</td><td>84.62</td><td>84.08</td><td>93.89</td><td>97.74</td><td>93.89</td><td>95.71</td><td>94.80</td><td>95.07</td><td>94.80</td><td>94.84</td></tr><tr><td>Trident</td><td>93.90</td><td>94.62</td><td>93.90</td><td>94.05</td><td>90.97</td><td>91.40</td><td>90.97</td><td>91.13</td><td>82.13</td><td>81.68</td><td>82.13</td><td>81.29</td><td>92.50</td><td>97.71</td><td>92.50</td><td>94.95</td><td>92.11</td><td>92.57</td><td>92.11</td><td>92.17</td></tr><tr><td>FOSS</td><td>90.11</td><td>90.95</td><td>90.11</td><td>90.28</td><td>88.68</td><td>89.18</td><td>88.68</td><td>88.90</td><td>79.91</td><td>79.21</td><td>79.91</td><td>78.69</td><td>86.94</td><td>97.62</td><td>86.94</td><td>91.85</td><td>92.12</td><td>92.49</td><td>92.12</td><td>92.18</td></tr><tr><td>RearView-VAE</td><td>94.84</td><td>95.55</td><td>94.84</td><td>94.93</td><td>85.93</td><td>85.01</td><td>85.93</td><td>84.77</td><td>76.61</td><td>75.40</td><td>76.61</td><td>74.60</td><td>96.66</td><td>97.84</td><td>96.66</td><td>97.23</td><td>94.04</td><td>94.39</td><td>94.04</td><td>94.08</td></tr><tr><td>RearView</td><td>99.14</td><td>99.17</td><td>99.14</td><td>99.15</td><td>97.86</td><td>98.06</td><td>97.86</td><td>97.90</td><td>94.61</td><td>95.41</td><td>94.61</td><td>94.72</td><td>97.08</td><td>99.11</td><td>97.08</td><td>97.83</td><td>99.38</td><td>99.37</td><td>99.38</td><td>99.37</td></tr></table>

In contrast, RearView outperforms several baseline methods by notable margins: it surpasses FlowLens (an intra-flow statistical feature-based method) by 14.75% F1, HyperVision (a graph clustering method leveraging intra and interflow features) by 5.57% F1, Whisper (a spectral featurebased method) by 10.08% F1, FOSS (an isolation forestbased method) by 9.41% F1, DeepLog (an event log-based method) by 14.28% F1, and Trident (a deep graph neural network-based method) by 7.08% F1. With an average F1 of 0.9779, RearView outperforms 6 traditional methods across 5 datasets, handling both context-associated and independent attack sessions effectively.

To further illustrate the role of the two-stage RearView method in reducing the false positive rate (FPR) and false negative rate (FNR), a comparative chart of FPR and FNR is presented in Figure 7. The upper half of the X-axis in the figure represents the FPR, which refers to the proportion of normal traffic incorrectly identified as malicious traffic; the lower half represents the FNR, i.e., the proportion of malicious traffic that fails to be correctly detected. As observed from the figure, based on the rapid filtering of the first-stage VAEs, the RearView method leverages the advantages of graph selfsupervised learning in the second stage to significantly reduce the FPR, while achieving an almost zero FNR. Specifically, the RearView method achieves an average FPR of 0.0296 and an average FNR of 0.0003 across the five datasets. Compared with other methods, it reduces the average FPR by 4.99% and the average FNR by 34.44%. Crucially, to verify RearView’s capability to suppress absolute false alarm volumes in benign-dominated real-world environments, we comprehensively evaluated the benign classification accuracy of the Stage 1 VAE across these five mainstream datasets. The VAE module achieves a precise benign recognition accuracy of 92.38% on CICIDS2017, 95.64% on ACIIoT2023, 91.88% on UNSW-NB15, 97.63% on CICAPT2024 and 96.96% on CrossAttack, maintaining a high average benign classification accuracy of 94.90%. With this strong recognition capability, most pure-benign graphs will not trigger resource-intensive second-stage inspection, which fundamentally restrains the generation of absolute false positives in large-scale practical deployments.

This joint performance improvement stems from the architectural synergy between both stages: while the first stage successfully handles the baseline benign traffic, the second stage executes graph-based correlation analysis to add critical interflow context to each remaining suspicious session, thereby maximizing the distinguishability of stealthy cyber threats.

![](images/05a5852e36aefa63fa9901fb04f41f4630ce19227bea80abc75c36eae65ea763.jpg)  
Fig. 7: Comparison results of FPR and FNR.

## C. Robustness Evaluation

We validate the robustness of RearView against four typical evasion attacks following adversarial construction paradigms from existing studies [65], [66], [67]. The first two belong to intra-flow and data-level perturbations, while the last two are sophisticated graph-level coordinated evasion attacks: (i) Feature manipulation, where attackers deliberately mimic intraflow features of benign traffic to avoid detection. (ii) Data pollution, where attackers inject benign TCP/UDP encrypted traffic into attack traffic. (iii) IP randomization, where adversaries distribute malicious sessions across diverse source IPs to tamper with topological structures. (iv) Benign decoy injection and causal evasion, where attackers interleave benign flows with malicious ones to dilute anomaly signals and break temporal causal dependencies.

Manipulation Evaluation. To assess the performance of RearView when faced with intra-flow feature similarity, we calculated the similarity between attack sessions and normal sessions using a set of key features, including packet interval, packet size, IP TTL, TCP flags, and UDP length [10], [11], [7], [66], [18]. Notably, the cosine similarity values were normalized to the range of [0, 1] for consistency in analysis. As illustrated in Figure 1, which presents the similarity distribution across five distinct datasets, most samples cluster within the [0, 0.1] interval. However, two datasets exhibit unique patterns that deviate from this trend: ACIIoT2023 [61] has 18.09% of its samples concentrated in the [0.9,1.0] range, while UNSW-NB15 sees 31.51% of its samples fall into the [0.3, 0.4] interval. These distributions pose significant challenges to detection methods that rely solely on intraflow features. Figure 8 further compares the accuracy of different methods across varying similarity intervals. Among the evaluated approaches, baseline methods with the median marked as a dotted line and the standard deviation represented by shaded regions exhibit a more pronounced decline in accuracy as similarity increases. Specifically, RearView’s accuracy decreases by just 6.02% when the similarity interval shifts from 0.1 to 1.0 on four datasets, outperforming HyperVision (which suffers an 10.89% accuracy drop) and Trident (with an 9.84% accuracy reduction) by a substantial margin. This result underscores the value of contextual features: by incorporating such information, detection systems can more effectively identify malicious behaviors even when they share high intra-flow feature similarity with benign sessions.

![](images/ff2c72f0c2b4d9c8465709935bea5ec46ab2aaafd08a87d5403ee996f8dd80ac.jpg)

![](images/65f3163ae0e81547d85271c3a0ff4d1ee68dc8e5e05068ba38a65a870199789c.jpg)

![](images/4fce0d61833254b748dc30e191fd4818d604bfa8ca52d1c85d75650643976124.jpg)

(c) UNSW-NB15  
![](images/6728ff7fced45c911e4f440c161b824cc4d5296066c7738a236a1ecbe880bfec.jpg)  
(d) CICAPT2024  
Fig. 8: Performance comparison results under similar intraflow features on four datasets.

Data Pollution Evaluation. Across four datasets, we simulated data contamination of varying severity by injecting different proportions of benign traffic into each malicious category within the test set, with the injection ratio set to $\textit { p } = \ \{ 0 , 0 . 0 5 , 0 . 1 , \cdot \cdot , 0 . 5 \}$ . Notably, RearView adopts a two-stage detection framework: it employs a service-oriented VAE screening method in the first stage and a graph-based association analysis approach in the second stage. To align the contamination process with the model’s design, we first identify the corresponding benign traffic by leveraging the service triples targeted by the malicious traffic, then modify the associated client IP addresses accordingly. This tailored contamination strategy is designed to more realistically simulate the disguise behaviors of attackers, ensuring the experimental scenario reflects real-world adversarial contexts. As illustrated in Figure 9, RearView demonstrated stable recognition accuracy across four data contamination scenarios. Specifically, when the contamination ratio $p \in [ 0 , 0 . 1 ]$ , most methods maintained favorable recognition robustness. With the further increase in the contamination ratio, the recognition accuracy of baseline methods decreased at an accelerated rate: when $p \ = \ 0 . 5$ the accuracy of most methods fell below 0.7, while RearView still retained high accuracy values. Overall, RearView exhibits the highest level of robustness when addressing data contamination issues. This advantage is primarily attributed to the graph-based self-supervised learning introduced in its second phase, which fully excavates the associative features between different sessions.

IP Randomization Attacks. To evaluate RearView’s resilience against coordinated multi-flow evasion, where adversaries distribute malicious sessions across diverse source IPs to disrupt inter-flow topological structures, we conduct an IP randomization attack experiment. We randomly modify the source IPs of malicious samples in CICIDS2017 [60] and ACI-IoT2023 [62] test sets, with perturbation ratios ranging from 0% to 50%. Figure 10 illustrates detection performance under varying IP perturbation ratios. Even with 50% of malicious source IPs randomized, RearView only experiences a 4.21% F1-score drop, maintaining 94.94% on CICIDS2017 and 93.78% on ACIIoT2023. In contrast, state-of-the-art graphbased methods Trident [18] and HyperVision [32] suffer severe degradations of 17.60% and 13.01%, respectively.

This robustness arises from RearView’s dual-verification mechanism: evasive traffic must bypass both the VAE’s intraflow anomaly check and the graph’s inter-flow contextual consistency check. Simply altering source IPs cannot conceal anomalous service interaction patterns, enabling RearView to effectively counter distributed Sybil-style evasion campaigns. Benign Decoy Injection and Causal Evasion. Sophisticated coordinated evasion often involves injecting benign decoy flows or interleaving legitimate and malicious sessions, which dilutes anomaly signals and disrupts causal dependencies [67]. To evaluate RearView’s ability to detect such deeply concealed cross-session attacks, we constructed the CrossAttack dataset, inspired by real APT tactics. We incorporate three representative attack scenarios (Figure 11): (i) Adversaries perform benign reconnaissance before exploiting vulnerabilities using CVE-2021-3129, then upload shells for control [68]; (ii) Launch SSH brute-force attacks and then masquerade as legitimate users [69]; (iii) Conduct port knocking attacks to maintain backdoors, interleaving benign and malicious behaviors [70]. All scenarios mix legitimate and malicious sessions, making detection difficult for intra-flow-based methods.

We perform comparative experiments on CrossAttack. As shown in Fig. 12(a), the cumulative distribution function (CDF) reveals that 68.78% of malicious traffic exhibits high similarity ([0.9,1.0]) to benign traffic, indicating severe signal dilution. Fig. 12(b) further shows that RearView achieves the lowest FPR and FNR, outperforming other methods in identifying disguised cross-session attacks.

The superior performance stems from RearView’s graphlevel association analysis. By modeling inter-flow dependencies via residual concatenation (Eqs: 12 and 13), malicious context propagates to adjacent benign decoys, rather than being diluted. This enables RearView to accurately identify coordinated attack campaigns, even when malicious flows are deeply concealed within benign traffic and causal relationships are obfuscated.

## D. Ablation Study

To evaluate the contribution of each module in RearView to detection performance, we conducted the following modifications: replacing the service-specific VAE model with a global VAE model (RearView-Base); performing testing using only the first-stage model (RearView-VAE); performing testing using only the second stage (with edge features in the graph modified to original statistical features, denoted as RearView-Graph); replacing the CBLOF clustering method with Isolation Forest (RearView-IF); modifying the weighted edge aggregation in the second stage to unweighted aggregation (RearView-NW); modifying the GraphSAGE-based edge aggregation approach in the second stage to out direction aggregation, denoted as RearView-Out); and changing the edge aggregation mode to bidirectional aggregation (RearView-Bi), with these variants used to assess the contribution of different modules to detection performance. Furthermore, during the graph construction process in RearView’s second stage, a caching strategy and a retirement mechanism are employed to ensure detection efficiency, so we also conducted an ablation study on the key parameters involved in these mechanisms.

![](images/fc9007c92bc0de5bf93ed7dcf46b9639b6523dc6c598de6b78678d72bbc44fa7.jpg)  
(a) CICIDS2017

<table><tr><td rowspan="8"></td><td>DeepLog</td><td>69.52</td><td>68.91</td><td>67.04</td><td>65.39</td><td>63.40</td><td>62.06</td><td>60.06</td><td>58.38</td><td>55.51</td><td>53.97</td><td>50.19</td></tr><tr><td>FlowLens</td><td>68.06</td><td>68.04</td><td>66.68</td><td>65.72</td><td>64.17</td><td>63.11</td><td>62.25</td><td>60.99</td><td>59.58</td><td>58.66</td><td>56.23</td></tr><tr><td>Whisper</td><td>72.99</td><td>72.51</td><td>71.45</td><td>70.83</td><td>69.56</td><td>68.11</td><td>66.79</td><td>66.17</td><td>64.54</td><td>63.17</td><td>61.08</td></tr><tr><td>HyperVision</td><td>84.08</td><td>84.03</td><td>83.25</td><td>82.05</td><td>81.13</td><td>80.03</td><td>78.86</td><td>78.08</td><td>76.66</td><td>75.72</td><td>73.59</td></tr><tr><td>Trident</td><td>81.29</td><td>80.82</td><td>80.25</td><td>79.29</td><td>77.97</td><td>76.94</td><td>75.37</td><td>74.37</td><td>73.29</td><td>72.02</td><td>70.06</td></tr><tr><td>FOSS</td><td>78.69</td><td>78.57</td><td>77.39</td><td>76.45</td><td>75.63</td><td>74.41</td><td>73.37</td><td>72.22</td><td>71.21</td><td>70.58</td><td>68.21</td></tr><tr><td>RearView</td><td>94.72</td><td>94.05</td><td>93.56</td><td>93.26</td><td>92.29</td><td>92.06</td><td>91.13</td><td>89.88</td><td>87.65</td><td>85.43</td><td>84.18</td></tr><tr><td></td><td>p=0</td><td>p=0.05</td><td>p=0.10</td><td>p=0.15</td><td>p=0.20</td><td>p=0.25</td><td>p=0.30</td><td>p=0.35</td><td>p=0.40</td><td>p=0.45</td><td>p=0.50</td></tr></table>

(c) UNSW-NB15

![](images/d5cb6a546663fb04f3fa3de5cf4992786ff7bbeecaef3256d93ed459b4f172a7.jpg)  
(b) ACIIoT2023

<table><tr><td rowspan="9"></td><td colspan="10">(1) CIGART2024</td></tr><tr><td>DeepLog</td><td>91.07</td><td>90.09</td><td>87.15</td><td>84.55</td><td>81.41</td><td>79.30</td><td>76.13</td><td>73.48</td><td>68.95</td></tr><tr><td>FlowLens</td><td>92.66</td><td>92.61</td><td>88.99</td><td>86.38</td><td>82.34</td><td>79.52</td><td>77.23</td><td>73.89</td><td>70.13</td></tr><tr><td>Whisper</td><td>94.21</td><td>93.22</td><td>91.05</td><td>89.78</td><td>87.19</td><td>84.23</td><td>81.53</td><td>80.26</td><td>76.92</td></tr><tr><td>HyperVision</td><td>95.71</td><td>95.60</td><td>93.86</td><td>91.18</td><td>89.12</td><td>86.68</td><td>84.07</td><td>82.34</td><td>79.17</td></tr><tr><td>Trident</td><td>94.95</td><td>94.15</td><td>93.15</td><td>91.49</td><td>89.22</td><td>87.42</td><td>84.72</td><td>82.99</td><td>81.12</td></tr><tr><td>FOSS</td><td>91.85</td><td>91.60</td><td>89.14</td><td>87.18</td><td>85.47</td><td>82.92</td><td>80.74</td><td>78.35</td><td>76.24</td></tr><tr><td>RearView</td><td>97.83</td><td>97.57</td><td>97.09</td><td>96.10</td><td>95.58</td><td>94.52</td><td>93.84</td><td>93.34</td><td>92.39</td></tr><tr><td></td><td>p=0</td><td>p=0.05</td><td>p=0.10</td><td>p=0.15</td><td>p=0.20</td><td>p=0.25</td><td>p=0.30</td><td>p=0.35</td><td>p=0.40</td></tr></table>

(d) CICAPT2024  
Fig. 9: Performance comparison results under imprecise traffic labels on four datasets.

![](images/4da2ae81047909156c8aeec1d74a2fc91c94b31ec11ad2bb44aee296e341b348.jpg)  
Fig. 10: Detection robustness to IP-randomized adversarial attacks. The x-axis represents the source IP perturbation rate (%) within the malicious category.

Module Ablation. Fig. 13(a) reports the detection performance of multiple RearView variants on four datasets to validate the contribution of each core module. Several key conclusions can be summarized as follows: (i) The servicespecific VAE achieves superior detection performance compared with the global VAE scheme. Solely adopting the firststage VAE (RearView-VAE) leads to a significant performance degradation, with the overall F1-score dropping by 10.4%. (ii) The standalone graph-based module (RearView-Graph) yields acceptable detection results, but still suffers from a 4.81% F1- score decline compared to the full model. (iii) Replacing the CBLOF-based anomaly scoring with Isolation Forest brings no performance gain, which demonstrates the superiority of the self-supervised graph embedding learned in the second stage. (iv) The weighted edge aggregation mechanism effectively improves detection accuracy, verifying the positive guidance of Stage-1 anomaly priors. Meanwhile, the promising performance of the unweighted variant in turn indicates that the graph module retains independent anomaly discovery capability and does not rely entirely on Stage-1 outputs. (v) For GraphSAGE-based edge aggregation strategies, inbound aggregation outperforms outbound and bidirectional aggregation. This is because attackers generally launch multiple malicious sessions from fixed source addresses, and inbound aggregation better captures persistent historical behavioral patterns of source nodes.

Parameters Ablation. We conduct comprehensive parameter ablation and sensitivity analysis to investigate the effects of core hyperparameters, including the cache queue length L, graph session retired proportion $p r o b _ { r e t i r e d } ,$ VAE anomaly threshold $\tau _ { s f } ,$ , graph initiation threshold $\gamma ,$ and weighting coefficient ω. The detailed analysis is organized as follows:

(i) Cache Queue Length L. Fig. 13(b) illustrates the impact of the cache queue length parameter L on detection accuracy, where the horizontal axis represents the number of sessions in the cache queue, with values ranging from 200 to 2000. Overall, as the number of sessions in the cache queue increases, the detection accuracy across all four datasets exhibits a corresponding upward trend. This phenomenon can be attributed to the fact that a larger cache queue size allows the system to accumulate more comprehensive historical behavioral information of source addresses, thereby enabling more accurate evaluation of the current session’s legitimacy. Notably, however, an increase in the number of cached sessions also leads to longer queue processing latency, which in turn results in a proportional rise in overall detection latency, a key trade-off to consider.

(ii) Graph Session Retired Proportion $p r o b _ { r e t i r e d } .$ Fig. 13(c) illustrates the impact of the graph retirement mechanism on detection accuracy in the detection process. Specifically, when specific trigger conditions are satisfied, the secondstage graph-based detection is initiated; once detection is completed, a certain percentage of expired sessions stored in memory is cleared. The results indicate that the proportion of sessions retained in memory exerts minimal influence on detection accuracy. This can be attributed to the strong session continuity of the test dataset, even complete cache clearance has no adverse effect on subsequent detection. However, in real-world detection scenarios, retaining a certain percentage of historical sessions in memory can substantially enhance detection accuracy, albeit at the cost of reduced detection efficiency.

(a)  
![](images/94bc292bb229d3f3d585184807d79a85f567ef0ed0bec01c0cef6785aaabb6ee.jpg)

![](images/292a80bcc143d2270210dbacf01882dc918ab8bb655a7c5773a467318842f666.jpg)  
Fig. 11: Three scenarios of cross-session attack behaviors derived from Advanced Persistent Threat (APT) groups.

Fig. 12: Comparison results on CrossAttack.  
![](images/c87d40302e304ad3291c62d04cb21ea9e0d08adad60c1aefc87561600d4be5cc.jpg)  
Fig. 13: Ablation study and sensitivity analysis.

(iii) VAE Anomaly Threshold $\tau _ { s f }$ and Graph Initiation Threshold $\gamma .$ . Two conditions trigger the second-stage graph detection: (1) the graph contains VAE anomaly detection records with $\rho > \gamma$ as shown in Eq.7; (2) the number of sessions in the graph satisfies $| Q | \geq L$ . Actually, three parameters affect graph detection: queue length L, VAE anomaly threshold $\tau _ { s f }$ , and graph initiation threshold γ. We have already conducted an ablation study on L in Figure 13, and now present results for $\tau _ { s f }$ and $\gamma$ (Table IV and Fig. 14).

![](images/6403e9639a7046801fa1c6060df45abd9f73b5877b98c00e67237ac67c066f5a.jpg)  
Fig. 14: VAE and graph trigger threshold sensitivity.

As shown in Table IV, we evaluate the VAE anomaly threshold $\tau _ { s f }$ based on the standalone RearView-VAE model. This parameter serves as a crucial control valve for the proportion of traffic that triggers the second-stage graph detection. When $\tau _ { s f }$ increases, the FPR consistently drops, effectively reducing the number of subsequent graph triggers and improving overall system efficiency. However, this comes at the cost of gradually elevating the FNR (missing some suspicious sessions). Conversely, decreasing $\tau _ { s f }$ eliminates the FNR, ensuring deep mining of stealthy threats, but it increases the FPR, triggering more graph detections and generating a higher absolute number of false positives.

While Fig. 14(a) shows that varying $\tau _ { s f }$ within [0.5, 0.95] has minimal impact on the overall accuracy curve in dense public datasets (due to their uniform attack distribution ensuring graphs trigger frequently regardless of minor threshold shifts), in real-world enterprise networks dominated by benign traffic, this threshold strictly governs the trade-off between detection speed and depth. Fig. 14(b) illustrates the impact of different graph initiation thresholds on detection accuracy. Overall, accuracy shows a downward trend as the threshold increases. The stepped decline arises because, in actual detection, the proportion of anomalous sessions $\rho$ in some graphs fails to meet the condition $\rho > \gamma$ , leading to skipped detection and reduced overall accuracy.

For real-world detection, to prioritize accuracy and ensure no zero-day threats are missed, we recommend setting the VAE anomaly threshold $\tau _ { s f }$ to a conservative value $( e . g . ,$ $\tau _ { s f } = 0 . 6$ set in RearView) and the graph initiation threshold γ to a low value $\begin{array} { r } { ( e . g . , \gamma = \frac { 1 } { L } ) } \end{array}$ . To prioritize efficiency and minimize analyst alert fatigue caused by excessive alarms, both thresholds can be appropriately increased.

(iv) Weighting Coefficient $\omega .$ . We conduct a sensitivity analysis of the weighting coefficient ω in the VAE’s joint anomaly score $p r o b _ { s f } ( \mathbf { x } ^ { * } )$ (Eq. 6) on CICIDS2017 [60] and ACIIoT2023 [62], comparing the full RearView model and the standalone RearView-VAE (as shown in Figure 15). The full model exhibits negligible sensitivity to ω, with F1-score fluctuations of less than 0.1% across $\omega \in [ 0 , 1 ]$ . In contrast, the standalone VAE shows significant sensitivity: performance degrades notably when $\omega < 0 . 5 ,$ , but remains stable and high when $\omega \in [ 0 . 6 , 0 . 9 ]$ . This difference arises because the VAE’s reconstruction error signal (weighted by ω) is more robust to normal traffic fluctuations than the latent space distance signal (weighted by $1 - \omega )$ , while RearView’s two-stage cascaded design compensates for VAE errors via contextual graph analysis, leading to overall insensitivity to ω. For practical deployment, we recommend setting $\omega \in [ 0 . 6 , 0 . 9 ]$ to optimize VAE filtering efficiency, with minor adjustments based on network environment characteristics.

TABLE IV: Threshold sensitivity analysis of standalone RearView-VAE on CICIDS2017. Precision, Recall and F1 are calculated for malicious traffic only.

<table><tr><td>VAE_threshold</td><td>FPR</td><td>FNR</td><td>Precision</td><td>Recall</td><td>F1</td></tr><tr><td>0.60</td><td>0.0762</td><td>0.0000</td><td>0.8621</td><td>1.0000</td><td>0.9260</td></tr><tr><td>0.65</td><td>0.0623</td><td>0.0000</td><td>0.8845</td><td>1.0000</td><td>0.9378</td></tr><tr><td>0.70</td><td>0.0534</td><td>0.0000</td><td>0.8992</td><td>1.0000</td><td>0.9470</td></tr><tr><td>0.75</td><td>0.0443</td><td>0.0000</td><td>0.9150</td><td>1.0000</td><td>0.9556</td></tr><tr><td>0.80</td><td>0.0349</td><td>0.0012</td><td>0.9317</td><td>0.9988</td><td>0.9641</td></tr><tr><td>0.85</td><td>0.0251</td><td>0.0051</td><td>0.9497</td><td>0.9949</td><td>0.9717</td></tr><tr><td>0.90</td><td>0.0141</td><td>0.0082</td><td>0.9710</td><td>0.9918</td><td>0.9813</td></tr><tr><td>0.95</td><td>0.0009</td><td>0.0980</td><td>0.9979</td><td>0.9020</td><td>0.9475</td></tr></table>

![](images/016b67a700c7e381a2840c0e322de273f5729483c970be76ec355b49254340c8.jpg)

![](images/891930fd596c7b2476cc338de82c3ddff8315a975eb9b04e99239cd88afa90d3.jpg)  
Fig. 15: Sensitivity analysis of weighted F1 with varying weight coefficient ω in Eq. 6.

## E. Computational Efficiency Evaluation

Detection Latency Analysis. In this section, we tested the latency of RearView from the moment it receives the first packet of malicious traffic to the successful completion of detection. The comparative experimental results are presented in Fig. 16. As shown in Fig. 16(a), the overall detection latency of our method is approximately 1.7 ms, which is roughly 2 ms lower than that of Trident [18] (a GNN-based method) and DeepLog [63] (an RNN-based method). It also outperforms FOSS [11] (a machine learning-based method). While it is slightly slower than HyperVision [32] (a graph-based detection method) in terms of speed and Whisper [7] (a method that only analyzes packet length), our method achieves performance on par with FlowLens [23], fully meeting the requirements for real-time detection. Notably, the aforementioned results reflect the detection latency of malicious activities as they go through both stages of our detection process. In practice, enterprises generate a large volume of benign traffic. Since the second detection stage will not be activated if no anomalies are identified in the VAE stage, the average detection latency is less than 1 ms.

We tested RearView’s five modules, with results in Fig. 16(b). The two most time-consuming are Module1: feature extraction (41.83%) and Module2: VAE detection (54.17%). Module3: Graph construction takes 1.51%; Module4: Graph embedding and Module5: clustering account for

![](images/4e2ffee0774a842615efa6573ee256c4ec1ff302711eca0e5f0278a47cfbaa6a.jpg)

![](images/b97d09e61c93faa61cfa9f5fe3fe8ceabc1515ae40880ed2b5a1ae8b125ab7ee.jpg)  
Fig. 16: Latency and module time overhead comparison.

2.37% and 0.12%. Across four datasets, RearView’s average detection time is $1 . 7 \times 1 0 ^ { - 3 }$ seconds.

Notably, the aforementioned time corresponds to the sequential detection results across all service triples. The core design intent of service-specific VAEs, however, is to enable end-to-end parallelization. This parallelizable architecture directly addresses the efficiency bottleneck of sequential processing.

Memory Consumption Analysis. In this section, we employed Python’s memory\_profiler to evaluate the actual memory consumption, statistically analyzing the memory increment of each function throughout the process using 61,395 sessions (training + testing) from the ACIIoT2023 dataset [61]. Results show that training 146 VAE models consumes a total of 2255.6 MiB; graph construction for queues with $L = 2 0 0 0$ sessions uses 4.7 MiB; the graph training process utilizes 10.0 MiB; and the clustering process consumes 47.4 MiB.

Excluding the system-related baseline of 140 MiB, GPU memory usage shows efficient, structured growth with VAE models remaining resident on the GPU throughout. For VAE training, memory rose from 140 MiB to 611 MiB after defining the first model, to 957 MiB post-training, and to 1015 MiB after training/loading 146 VAEs. During graph construction, memory increased by 28 MiB to 1043 MiB, with PyTorch managing 85.12 MiB explicit and 88 MiB cache. For graph training, it grew by 222 MiB to 1265 MiB after adding graph model parameters and transient data, alongside resident VAEs, with PyTorch tracking 90.76 MiB and 216 MiB. No uncontrolled growth occurred, the final 1265 MiB underscores efficiency, and discrepancies between nvidia-smi and PyTorch stats stem from DGL/CUDA overhead, not excess usage.

## VI. DISCUSSION AND LIMITATIONS

Operational Feasibility and Absolute False Positive Mitigation. High-throughput enterprise networks are subject to the Base-Rate Fallacy [71], where benign traffic accounts for over 99.9% of total flows. Even a low FPR may thus produce massive alerts and burden SOC analysts. RearView addresses this issue with a two-stage design. The Stage 1 VAE obtains a 94.90% average benign classification accuracy across five datasets, preventing most benign traffic from activating resource-heavy Stage 2 inspection. Taking 1 million benign flows as a conservative baseline, only 51,000 flows (5.10%) proceed to subsequent detection. With the default $\tau _ { s f } = 0 . 6$ and an end-to-end FPR of 2.96%, the pipeline generates roughly 1,510 raw alerts per million flows. For further FP reduction in practical use, post-hoc mitigation techniques can be adopted. As a typical solution, pVoxel [72] utilizes pointcloud analysis to remove structural FP noise automatically. If integrated as a post-processing module, it will significantly reduce the total number of alerts and effectively alleviate the workload of enterprise SOC teams.

Model Update and Deployment. For model updates, unknown service triplets are identified through periodic service aggregation. Legitimate service triplets trigger the training of new VAEs (with existing VAEs remaining unchanged), while unauthorized access is flagged as attacks. Subsequently, the graph model (GraphSAGE-DGI) performs lightweight selfsupervised fine-tuning on recent sessions using the new VAE outputs, eliminating the need for full retraining. For deployment, service-specific VAEs support flexible parallel deployment on edge devices and terminal servers. To adapt to large enterprise networks with hundreds of services, we adopt two optimization strategies: first, distributed parallel training and load balancing to accelerate model training and ensure stable detection under high concurrency; second, service clustering and model sharing. We group functionally similar service triplets and allow them to share one VAE model [73], [27], which effectively cuts down redundant parameters and server memory usage.

Limitations and Future Work. While RearView demonstrates high efficiency and robust detection capabilities, there remain opportunities for further optimization. First, although the current sliding window mechanism effectively captures standard attack correlations, the modeling of extremely protracted dependencies over extended time horizons can be further refined. Second, while the framework operates seamlessly on typical enterprise servers, extending its deployment to ultraconstrained edge environments presents a valuable direction. Third, residual false positives still exist in real imbalanced traffic scenarios, which currently relies on external post-hoc methods for further suppression.

Accordingly, future work will focus on introducing adaptive temporal scales for dynamic graph construction, exploring model compression techniques (e.g., knowledge distillation) to facilitate lightweight edge deployment, investigating lightweight native post-processing strategies to mitigate structural false positives, and extending the framework to a crossmodality paradigm via semi-supervised fusion for enhanced robustness against adaptive mimicry and zero-day evasion attacks [74].

## VII. CONCLUSION

In this paper, we presented RearView, a secure two-stage framework that resolves the inherent tension between highthroughput efficiency and deep relational mining in malicious traffic detection. RearView structurally decouples the detection pipeline and introduces an asymmetric filtering paradigm: the first stage uses service-personalized Attention-VAEs for rapid single-flow screening, selectively activating the second stage. Subsequently, an anomaly-weighted GraphSAGE-DGI module dynamically constructs session graphs to uncover complex inter-flow dependencies, effectively capturing coordinated threats while maintaining bounded memory overhead.

Extensive evaluations across four benchmark datasets and one custom CrossAttack dataset demonstrate that RearView establishes a new state-of-the-art. It achieves an average F1-score of 97.79% and reduces false negatives by 34.44%, all while sustaining a rigorous processing latency of under 2 ms per flow. Furthermore, RearView exhibits exceptional robustness against sophisticated evasion tactics, such as data pollution and traffic morphing, underscoring its practical viability for real-world enterprise networks.

## ACKNOWLEDGMENTS

This work was supported by the National Key R&D Program of China (2023YFB3106800).

## REFERENCES

[1] R. Uetz et al., “You cannot escape me: Detecting evasions of siem rules in enterprise networks,” in USENIX Security. USENIX Association, 2024, pp. 5179–5196.

[2] B. Nour et al., “A survey on threat hunting in enterprise networks,” IEEE Communications Surveys & Tutorials, 2023.

[3] D. Wagner et al., “Mimicry attacks on host-based intrusion detection systems,” in CCS. ACM, 2002, pp. 255–264.

[4] A. Goyal et al., “Sometimes, you aren’t what you do: Mimicry attacks against provenance graph host intrusion detection systems,” in NDSS. The Internet Society, 2023.

[5] X. Hu et al., “Toward early and accurate network intrusion detection using graph embedding,” IEEE Trans. Info. Foren. Sec., vol. 18, pp. 5817–5831, 2023.

[6] Y. Li et al., “Robust online learning against malicious manipulation with application to network flow classification,” in INFOCOM. IEEE, 2021, pp. 1–10.

[7] C. Fu et al., “Realtime robust malicious traffic detection via frequency domain analysis,” in CCS, 2021, pp. 3431–3446.

[8] V. F. Taylor et al., “Appscanner: Automatic fingerprinting of smartphone apps from encrypted network traffic,” in EuroS&P. IEEE, 2016, pp. 439–454.

[9] J. Zhang et al., “Robust network traffic classification,” IEEE/ACM Trans. Netw., vol. 23, no. 4, pp. 1257–1270, 2014.

[10] C. Liu et al., “Fs-net: A flow sequence network for encrypted traffic classification,” in INFOCOM. IEEE, 2019, pp. 1171–1179.

[11] Z. Zhao et al., “Towards fine-grained unknown class detection against the open-set attack spectrum with variable legitimate traffic,” IEEE/ACM Trans. Netw., 2024.

[12] X. Lin et al., “Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in WWW, 2022, pp. 633–642.

[13] T. Shapira et al., “Flowpic: A generic representation for encrypted traffic classification and applications identification,” IEEE Trans. Netw. Ser. Man., vol. 18, no. 2, pp. 1218–1232, 2021.

[14] P. Fang et al., “Sofa: Service-oriented fine-grained attack traffic detection with meta learning,” IEEE/ACM Trans. Netw., vol. 34, pp. 2430–2445, 2025.

[15] J. Heidemann et al., “Modeling the performance of http over several transport protocols,” IEEE/ACM Trans. Netw., vol. 5, no. 5, pp. 616– 630, 2002.

[16] N. Moustafa and J. Slay, “Unsw-nb15: a comprehensive data set for network intrusion detection systems (unsw-nb15 network data set),” in MilCIS. IEEE, 2015, pp. 1–6.

[17] M. Shen et al., “Accurate decentralized application identification via encrypted traffic analysis using graph neural networks,” IEEE Trans. Info. Foren. Sec., vol. 16, pp. 2367–2380, 2021.

[18] Z. Zhao et al., “Trident: A universal framework for fine-grained and class-incremental unknown traffic detection,” in WWW, 2024, pp. 1608– 1619.

[19] T.-D. Pham et al., “Mappgraph: Mobile-app classification on encrypted network traffic using deep graph convolution neural networks,” in ACSAC, 2021, pp. 1025–1038.

[20] W. Xu et al., “When imbalance meets imbalance: Structure-driven learning for imbalanced graph classification,” in WWW, 2024, pp. 905– 913.

[21] Z. Song et al., “I<sup>2</sup>RNN: An incremental and interpretable recurrent neural network for encrypted traffic classification,” IEEE Trans. Depend. Sec. Comput., 2023.

[22] Z. Zhao et al., “Ernn: Error-resilient rnn for encrypted traffic detection towards network-induced phenomena,” IEEE Trans. Depend. Sec Comput., 2023.

[23] D. Barradas et al., “Flowlens: Enabling efficient flow classification for ml-based network security applications.” in NDSS, 2021.

[24] S. Panda et al., “Smartwatch: Accurate traffic analysis and flow-state tracking for intrusion prevention using smartnics,” in CoNEXT. ACM, 2021, pp. 60–75.

[25] H. Yan et al., “Automatic evasion of machine learning-based network intrusion detection systems,” IEEE Trans. Depend. Sec. Comput., vol. 21, no. 1, pp. 153–167, 2023.

[26] M. Shen et al., “Classification of encrypted traffic with second-order markov chains and application attribute bigrams,” IEEE Trans. Info. Foren. Sec., vol. 12, no. 8, pp. 1830–1843, 2017.

[27] Y. Mirsky et al., “Kitsune: an ensemble of autoencoders for online network intrusion detection,” in NDSS. The Internet Society, 2018.

[28] J. Holland et al., “New directions in automated traffic analysis,” in CCS, 2021, pp. 3366–3383.

[29] K. Wang et al., “Anomalous payload-based network intrusion detection,” in RAID. Springer, 2004, pp. 203–222.

[30] G. Zhou et al., “Trafficformer: an efficient pre-trained model for traffic data,” in S&P. IEEE Computer Society, 2024, pp. 102–102.

[31] Y. Hong et al., “Graph based encrypted malicious traffic detection with hybrid analysis of multi-view features,” Info. Sci., vol. 644, p. 119229, 2023.

[32] C. Fu et al., “Detecting unknown encrypted malicious traffic in real time via flow interaction graph analysis,” in NDSS. The Internet Society, 2023.

[33] W. Li et al., “Prograph: Robust network traffic identification with graph propagation,” IEEE/ACM Trans. Netw., vol. 31, no. 3, pp. 1385–1399, 2022.

[34] Z. Yang et al., “Wtagraph: Web tracking and advertising detection using graph neural networks,” in S&P. IEEE Computer Society, 2022, pp. 1540–1557.

[35] W. Cai et al., “Memg: Mobile encrypted traffic classification with markov chains and graph neural network,” in HPCC. IEEE, 2021, pp. 478–486.

[36] F. Tegeler et al., “Botfinder: Finding bots in network traffic without deep packet inspection,” in CoNEXT, 2012, pp. 349–360.

[37] B. J. Kwon et al., “The dropper effect: Insights into malware distribution with downloader graph analytics,” in CCS, 2015, pp. 1118–1129.

[38] T. Nelms et al., “Webwitness: investigating, categorizing, and mitigating malware download paths,” in USENIX Security. USENIX Association, 2015, pp. 1025–1040.

[39] L. Invernizzi et al., “Nazca: Detecting malware distribution in large-scale networks.” in NDSS, vol. 14, 2014, pp. 23–26.

[40] M. Nakıp and E. Gelenbe, “Online self-supervised deep learning for intrusion detection systems,” IEEE Trans. Info. Foren. Sec., vol. 19, pp. 5668–5683, 2024.

[41] J. Gui et al., “A survey on self-supervised learning: Algorithms, applications, and future trends,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 46, no. 12, pp. 9052–9071, 2024.

[42] X. Liu et al., “Self-supervised learning: Generative or contrastive,” IEEE Trans. Know. Data Eng., vol. 35, no. 1, pp. 857–876, 2021.

[43] J. An and S. Cho, “Variational autoencoder based anomaly detection using reconstruction probability,” Special lecture on IE, vol. 2, no. 1, pp. 1–18, 2015.

[44] H. Zenati et al., “Adversarially learned anomaly detection,” in ICDM. IEEE, 2018, pp. 727–736.

[45] Z. Zhang et al., “Backdoor defense via deconfounded representation learning,” in CVPR, 2023, pp. 12 228–12 238.

[46] Y. Yue et al., “Contrastive learning enhanced intrusion detection,” IEEE Trans. Netw. Ser. Man., vol. 19, no. 4, pp. 4232–4247, 2022.

[47] M. Shen et al., “Robust detection of malicious encrypted traffic via contrastive learning,” IEEE Trans. Info. Foren. Sec., 2025.

[48] P. Velickovi ˇ c´ et al., “Deep graph infomax,” in ICLR, 2019.

[49] E. Caville et al., “Anomal-e: A self-supervised network intrusion detection system based on graph neural networks,” Knowledge-based systems, vol. 258, p. 110030, 2022.

[50] C. Wu et al., “Tcg-ids: Robust network intrusion detection via temporal contrastive graph learning,” IEEE Trans. Info. Foren. Sec., 2025.

[51] Z. Hao et al., “Towards expansive and adaptive hard negative mining: Graph contrastive learning via subspace preserving,” in WWW, 2024, pp. 322–333.

[52] C. Niu et al., “Affinity uncertainty-based hard negative mining in graph contrastive learning,” IEEE Trans. Neural Netw. Learn. Syst., vol. 35, no. 9, pp. 11 681–11 691, 2024.

[53] K. Bartos et al., “Optimized invariant representation of network traffic for detecting unseen malware variants,” in USENIX Security. USENIX Association, 2016, pp. 807–822.

[54] C. Fu et al., “Frequency domain feature based robust malicious traffic detection,” IEEE/ACM Trans. Netw., vol. 31, no. 1, pp. 452–467, 2022.

[55] C. Novo et al., “Flow-based detection and proxy-based evasion of encrypted malware c2 traffic,” in AISec. ACM, 2020, pp. 83–91.

[56] B. Anderson and D. McGrew, “Identifying encrypted malware traffic with contextual flow data,” in ALSec, 2016, pp. 35–46.

[57] K. Thomas et al., “Data breaches, phishing, or malware? understanding the risks of stolen credentials,” in CCS, 2017, pp. 1421–1434.

[58] M. Shen et al., “Swallow: a transfer-robust website fingerprinting attack via consistent feature learning,” in CCS, 2025, pp. 1574–1588.

[59] E. Papadogiannaki and S. Ioannidis, “A survey on encrypted network traffic analysis applications, techniques, and countermeasures,” ACM Computing Surveys, vol. 54, no. 6, pp. 1–35, 2021.

[60] I. Sharafaldin et al., “Toward generating a new intrusion detection dataset and intrusion traffic characterization.” ICISSp, vol. 1, no. 2018, pp. 108–116, 2018.

[61] E. A. Nack et al., “Aci-iot-2023: A robust dataset for internet of things network security analysis,” in MILCOM. IEEE, 2024, pp. 1–6.

[62] Canadian Institute for Cybersecurity, “CIC Advanced Persistent Threat Dataset for IIoT 2024,” Canadian Institute for Cybersecurity, Tech. Rep. Accessed: Jan. 15, 2025, 2024. [Online]. Available: https://www.unb.ca/cic/datasets/iiot-dataset-2024.html

[63] M. Du et al., “Deeplog: Anomaly detection and diagnosis from system logs through deep learning,” in CCS, 2017, pp. 1285–1298.

[64] W. Zheng et al., “Learning to classify: A flow-based relation network for encrypted traffic classification,” in WWW, 2020, pp. 13–22.

[65] C. Fu et al., “Detecting tunneled flooding traffic via deep semantic analysis of packet length patterns,” in CCS. ACM, 2024, pp. 3659– 3673.

[66] Z. Zhao et al., “Towards context-aware traffic classification via timewavelet fusion network,” in KDD. ACM, 2025.

[67] L. Gao et al., “Wedjat: Detecting sophisticated evasion attacks via realtime causal analysis,” in SIGKDD, 2025, pp. 342–353.

[68] Mphasis, “Laravel rubycarp hackers linked to 10-year-old crypto mining botnet,” Mphasis, Tech. Rep. Accessed: Sep. 27, 2025, 2024. [Online]. Available: https://www.mphasis.com/content/dam/mphasis-com/global/ en/home/services/cybersecurity/rubycarp-hackers-6.pdf

[69] The MITRE Corporation, “Leviathan australian intrusions,” The MITRE Corporation, Tech. Rep. Accessed: Sep. 27, 2025, 2022. [Online]. Available: https://attack.mitre.org/campaigns/C0049/

[70] The MITRE Corporation, “Promethium,” The MITRE Corporation, Tech. Rep. Accessed: Sep. 27, 2025, 2018. [Online]. Available: https://attack.mitre.org/groups/G0056/

[71] R. Sommer and V. Paxson, “Outside the closed world: On using machine learning for network intrusion detection,” in S&P. IEEE, 2010, pp. 305–316.

[72] C. Fu et al., “Point cloud analysis for ml-based malicious traffic detection: Reducing majorities of false positive alarms,” in CCS, 2023, pp. 1005–1019.

[73] J. Yang et al., “Conditional variational auto-encoder and extreme value theory aided two-stage learning approach for intelligent fine-grained known/unknown intrusion detection,” IEEE Trans. Info. Foren. Sec., vol. 16, pp. 3538–3553, 2021.

[74] C. Fu et al., “Training with only 1.0‰ samples: Malicious traffic detection via cross-modality feature fusion,” in CCS, 2025, pp. 3930– 3944.

![](images/4372cdf27ad19890693292e71a55d048ed8060050f8fd93656fd1c3fb45efd71.jpg)

Peng Fang is a PH.D. student in Zhejiang University, Hangzhou, China. He received his M.S. degree from the School of Computer Science and Technology, University of Science and Technology of China, Hefei, China. His main research interests include encrypted traffic analysis, threat detection and deep learning.

![](images/1dcd3b685b9347e082a304527f701efcafef0d946af4f8729b74371ed7e755d1.jpg)

Zhihong Liang M.S., Director of the Digitalization and Information Security Center, Electric Power Research Institute, China Southern Power Grid (CSG), China. He is a Professor-level Senior Engineer. His research interests include cyberspace security, data security, artificial intelligence and cloud computing.

![](images/27ed708c85320cdd79910636afd4f917f5b4cce0c9f0233170113b16256f2eac.jpg)

Ziming Zhao (Member, IEEE) is a ZJU 100 Young Professor in the School of Software Technology, Zhejiang University, China. He has published more than 60 papers in international journals and conference proceedings, including JSAC, MobiCom, SIGCOMM, DAC, ACL, WWW, INFOCOM, KDD, CCS, RTSS, IJCAI, TSE, TMC, TCAD, ToN, TIFS, TDSC, COSE, DATE, ESE, and AAAI. His research interests include machine learning, traffic identification, network security, and mobile computing.

![](images/6b475d30884dd97ab6f8388c2fcab2358aa63abc9bde64d2e654b29de7dcdfd7.jpg)

![](images/059cdfbbe10b406042ef28528ccaf771361416b1c050095a167e5f09d71dfb86.jpg)

Ziqi Yang received his Ph.D. degree from the National University of Singapore in 2019. He is currently an assistant professor with the College of Computer Science and Technology, Zhejiang University, Hangzhou, China. His research direction includes intersections between security, privacy, and machine learning.

Yixin Jiang Ph.D., First-Class Chief Expert and Professor at the Electric Power Research Institute, China Southern Power Grid (CSG), China. He has published more than 70 papers in international journals and conference proceedings, including JSAC, INFOCOM, TMC, TWC, TVT, TC, TDSC, and TSG. His research interests include cybersecurity, artificial intelligence security, and digital grid.

![](images/81b47766558d73e917889fd3ce95ea579d0d7c62202193113ac15d84ec2a3513.jpg)

![](images/2a13f847d9fda657315511f1a6bb37faa3740c1d3a73efd1882091044a5086dd.jpg)

Fan Zhang (Member, IEEE) received his Ph.D. degree from the Department of Computer Science and Engineering, University of Connecticut, CT, USA, in 2011. He is currently a Full Professor with the College of Computer Science and Technology, Zhejiang University, Hangzhou, China. His research interests include system security, hardware security, network security, cryptography, and computer architecture.

Wenqian Xu M.S., a Researcher at the Electric Power Research Institute, China Southern Power Grid (CSG), China. Her research interests include cybersecurity, artificial intelligence security, and digital grid technologies.
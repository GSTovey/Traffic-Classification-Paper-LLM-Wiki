# Shattering Weak Facades: Trustworthy Detection of Encrypted Malicious Traffic via Uncertainty-Aware Fusion

Meihui Zhong , Chengtai Cao , Wenxin Tai , and Fan Zhou , Member, IEEE

Abstract—Graph Neural Networks (GNNs) are promising for Encrypted Malicious Traffic Detection (EMTD), yet practical deployments often face weak information: broken graph structures, incomplete node features, and scarce training data. Prior methods partially mitigate these issues but still suffer from (i) restricted information propagation range in graph structures, (ii) imprecise graph structure reconstruction resulting in erroneous or missing connections, and (iii) absence of a unified framework to address multiple facets of information sparsity jointly. In response, we propose TrustWI, an uncertainty-aware multi-view framework. It builds three complementary views to recover and enrich signal under weak information: (i) long-range propagation to expand information flow, (ii) post-propagation structural augmentation to repair broken connections, and (iii) view interaction modeling to capture cross-view synergy. We further develop an evidential, uncertainty-aware fusion that quantifies prediction uncertainty at both the view level and the global level, yielding robust decisions. Extensive evaluations across three benchmarks validate the effectiveness of TrustWI, demonstrating substantial improvements in accuracy and trustworthiness under weak information conditions. Notably, our approach advances the state-of-the-art AUC from 85.45% to 89.57% in extreme information-constrained scenarios.

Index Terms—Encrypted malicious detection, multi-view learning, graph neural network (GNN), uncertainty fusion, evidential deep learning.

## I. INTRODUCTION

safeguard for users’ digital activities against unauthorized access. While these protocols strengthen privacy protection and data security, they inadvertently enable cyber-attackers to conceal their malicious behaviors and circumvent detection systems. This evolving security landscape has elevated Encrypted Malicious Traffic Detection (EMTD) to a critical concern in modern cybersecurity. Deep learning has emerged as a powerful solution to this challenge, exhibiting remarkable capabilities in extracting intricate patterns and adapting to dynamic networks [1], [2]. In particular, graph-based methods [3] have garnered substantial attention due to their inherent ability to leverage structural relationships within encrypted communications, significantly improving detection accuracy.

While Graph Neural Networks (GNNs) have demonstrated remarkable effectiveness in EMTD, their success heavily relies on the completeness and reliability of input graph data [4], [5]. Unfortunately, this assumption is rarely satisfied in realworld encrypted traffic scenarios. This gap between the ideal of complete data and the operational reality gives rise to what we term weak information, rooted in three interrelated challenges: Structurally, network-level disruptions like packet loss lead to fragmented connections, while identity obfuscation from NAT and VPNs results in broken graph topologies. Semantically, protocol-level ambiguities such as port sharing and traffic multiplexing dilute the meaning of a flow, making node features inconsistent. Practically, the high cost and complexity of expert annotation for encrypted threats lead to a scarcity oflabeled data. These real-world factorsjointly produce ambiguous host interactions and diluted semantic features, manifesting as broken graph structures, incomplete node features, and limited labeled data, thereby undermining the reliability of detection models [4], [6]. This pervasive information sparsity significantly impairs GNNs capability for effective message propagation and representation learning, ultimately undermining detection efficacy [7], [8].

Recent efforts [6], [9], [10] have introduced feature generation and edge completion techniques to address information deficiency. Nevertheless, these approaches exhibit several fundamental limitations. Firstly, existing feature generation methods [9] attempt to reconstruct incomplete node features by leveraging available feature information and neighborhood structures. To mitigate notorious over-smoothing effects [10], these techniques predominantly employ short-range propagation mechanisms, thereby failing to capture essential long-range dependencies. As illustrated in Fig. 1(a), the red and purple nodes are connected by both short- and long-range edges under ideal conditions. However, when the shorter edge is missing, current models struggle to facilitate effective information exchange between them, resulting in suboptimal feature generation. Secondly, current edge completion approaches [6] adopt a pre-propagation paradigm, where edge enhancement precedes message passing. In scenarios with incomplete node features, this dependence on partial feature information frequently leads to erroneous edge generation or failure to identify legitimate connections (cf. Fig. 1(b)). Furthermore, existing methods typically address individual aspects of information deficiency in isolation, neglecting the interdependent nature of feature and structural incompleteness that co-occurs in real-world scenarios.

![](images/dfb121b8e03fd5c65591a44b48f0f47bfcd7889284bc1fbe49026933386cb2b3.jpg)  
Fig. 1. Sketch of limitations with weak information. (a) Short-range propagation fails to facilitate information exchange between two colored nodes. (b) Pre-propagation edge-completion adds erroneous edges and omits existing ones.

To overcome these limitations, we propose TrustWI, an uncertainty-aware multi-view learning framework that holistically handles various weak information scenarios. Our framework tackles this challenge through multiple views, each targeting specific aspects while considering their potential interactions. For the first challenge, we introduce View-L, a longrange propagation mechanism that enables comprehensive information flow across the graph for robust feature reconstruction. Leveraging these enhanced representations, View-S enriches the structural information through semantic similarity analysis, operating in a post-propagation paradigm to ensure more reliable edge completion. To capture the dynamic interplay between feature enhancement and structural refinement, we further develop View-P, a novel pseudo-view that models how the augmented edges from View-S reciprocally influence the information propagation patterns in View-L.

In TrustWI, the reliability of predictions from each view exhibits considerable variation across different samples, necessitating the development of an effective fusion strategy. While traditional fusion approaches utilize either fixed weights or attention mechanisms based on their feature representations to combine views, these methods prove inadequate in capturing the model’s inherent uncertainty in processing different views. This limitation potentially results in unreliable fusion when certain views generate noisy or incomplete signals [11]. To achieve robust view fusion, we develop an uncertainty-aware strategy grounded in evidential learnin [12]. Specifically, we conceptualize each view’s outputs as evidence contributing to the formation of uncertainty-aware opinions about the final predictions. Through the implementation ofvariational Dirichlet distributions, parameterized by the collected evidence across views, our approach systematically captures the uncertainty associated with each view’s predictions. The final fusion process employs Dempster-Shafer theory [11], providing a rigorous mathematical framework for integrating these uncertainty-aware opinions.

We conduct comprehensive empirical evaluations on three real-world datasets, benchmarking our proposed TrustWI against several state-of-the-art baselines. Experimental results demonstrate TrustWI’s superior performance across diverse weak information scenarios, achieving particularly substantial improvements in detection accuracy when processing extremely sparse signals. Furthermore, TrustWI provides reliable uncertainty estimates for its predictions at both view-specific and global levels, significantly enhancing the overall trustworthiness of detection results.

## II. RELATED WORK

This section reviews three primary research streams relevant to our work, contextualizing our contributions in each domain.

## A. Encrypted Malicious Traffic Detection

Traditional malicious traffic detection methods primarily focused on analyzing plaintext packet payloads [7]. However, the widespread adoption of encryption has rendered these methods largely ineffective, catalyzing the development of learningbased solutions. A pioneering example is Kitsune [2], which employs incremental online learning for adaptive feature extraction. Recent advancements have witnessed the emergence of graph-based methods designed to capture intricate network patterns [13], [14]. Noteworthy contributions include ST-Graph [13], which integrates spatial-temporal features through graph representations, and ContraMTD [14], which leverages graph contrastive learning to model network behaviors.

Handling Weak Information: Real-world encrypted traffic graphs often suffer from incomplete observations, resulting in degraded node features and unreliable connectivity. Prior EMTD studies address such weak information through data completion [8], [15], [16] or robust graph architectures. For example, MI-GNN [17] fuses complementary views via multi-task learning, and RAPIER [8] leverages traffic regularities for anomaly relabeling. Nonetheless, jointly handling broken structures and incomplete features remains challenging.

Beyond EMTD, similar challenges have been extensively studied in the broader graph learning literature under incomplete, partial, or noisy graph settings. Representative studies in this line focus on partial and noisy matching, such as size-varied graphs, outlier nodes, and unreliable correspondences. For instance, [18] formulates unsupervised graph matching under multiple modes and optimizes it via discrepancy minimization; [19] designs a graph-context attention mechanism to improve matching for size-varied graphs; ZAC [20] introduces a zero-assignment constraint to explicitly handle outliers; and COMMON [21] models noisy correspondence with a bi-level formulation. While these works target multi-graph correspondence recovery, they highlight the same difficulty oflearning robust relational patterns from incomplete and noisy signals. In contrast, our work focuses on single-graph EMTD and addresses weak information via uncertainty-aware representation learning and fusion.

## B. Multi-View Learning

Multi-view learning leverages complementary information by jointly modeling shared representations and view-specific structure [22]. The paradigm has progressed from classical CCA [23] to contrastive frameworks, achieving strong results in graph clustering [24], [25] and multi-task learning [26].

To address view-quality variation, DUA-Nets [27] model per-view uncertainty as Gaussian variance $\sigma ^ { 2 }$ . However, this conflates reconstruction difficulty with epistemic uncertainty, potentially yielding unreliable estimates, for example, by inflating σ to suppress reconstruction loss on noisy views. ECNet [26] applies multi-view learning to malicious traffic detection via gated fusion of content and pattern features. While effective, it lacks an explicit reliability model. The fusion is fixed and agnostic to inter-view uncertainty or disagreement, and its scalar confidence is computed separately from fusion, limiting the reflection and propagation of uncertainty. These choices reduce robustness under noise or distribution shift.

Motivated by these limitations, this work introduce a multiview framework with uncertainty-aware view fusion that explicitly models view-level confidence and enhances robustness in weak-information and out-of-distribution scenarios.

## C. Uncertainty Learning

Conventional deep learning models, functioning as deterministic mappings, inherently lack the capability to quantify prediction uncertainty. This limitation is particularly critical in highstakes domains where prediction reliability is essential [28]. The theoretical foundation for uncertainty quantification in deep learning originates from Bayesian neural networks [29], which model network parameters as probability distributions. Given their computational complexity, more tractable approaches have emerged, including Monte Carlo dropout [30], deep ensembles [31], evidential learning [12], and probabilistic logic [32]. This work adapts evidential learning to EMTD, providing a framework for quantifying view-specific uncertainties. This enables dynamic view fusion that adjusts to information sparsity levels, departing from existing deterministic approaches.

## III. METHODOLOGY

This section presents our proposed TrustWI for EMTD under weak information scenarios. We first formalize the problem setting (Section III-A), then detail our framework, which comprises multi-view representation learning (Section III-B), uncertaintyaware view fusion (Section III-C).

## A. Task Definition

Network traffic consists of packets transmitted between host devices. While traffic analysis can be conducted at various granularities (packet, stream, channel, or flow), this study focuses on flow-level analysis. A flow is defined as a sequence of packets sharing a common 4-tuple identifier (source IP address, destination IP address, source port, destination port). This flow-based paradigm facilitates fine-grained detection of malicious network activities.

Following established graph-based EMTD approaches [13], [26], we define a graph $\mathcal { G } = ( \gamma , \mathcal { E } , \mathbf { A } , \mathbf { H } )$ . Here, V is the node set with cardinality $| \nu |$ , where each node $v _ { i }$ represents a unique host identified by its IP address. E denotes the edge set, where an $e _ { i j }$ exists if there is a direct network flow between host $v _ { i }$ and host $v _ { j } . \mathbf { A } \in \{ 0 , 1 \} ^ { ( | \mathcal { V } | \times | \mathcal { V } | ) }$ is the adjacency matrix, where ${ \bf A } _ { i j } = 1$ denotes an edge between nodes $v _ { i }$ and $v _ { j }$ , and ${ \bf A } _ { i j } = 0$ otherwise. $\mathbf { H } \in \mathbb { R } ^ { | \nu | \times d }$ denotes the feature matrix, where each row represents a d-dimensional feature vector of network flow statistics for a host. Consistent with previous studies [14], [26], our proposed model, TrustWI, adopts the semi-supervised learning paradigm. Given $N _ { L }$ labeled training flows (i.e., nodes in G), TrustWI aims to learn a mapping function for unlabeled target nodes:

$$
\hat {\mathbf {y}} _ {t} = \operatorname{TrustWI} (\mathbf {A}, \mathbf {H}, v _ {t} | \Theta),\tag{1}
$$

where $\hat { \mathbf { y } } _ { t }$ is the prediction distribution for target node $v _ { t } .$ , and Θ denotes the model parameters.

Weak Information Scenario: In real-world encrypted network, graph-based intrusion detection often operates under degraded observations due to infrastructure and protocol-level limitations. Packet loss during transmission disrupts flow continuity and results in incomplete or erroneous edge construction. Simultaneously, NAT translation, VPN tunneling, and dynamic IP reassignment obscure host identities and fragment the underlying communication topology. Furthermore, port sharing and traffic multiplexing introduce inconsistencies into flow semantics, while the scarcity of labeled traffic significantly limits the ability to train reliable classifiers.

In practice, encrypted traffic suffers from various structural and semantic degradation sources: (i) packet loss during transmission leads to missing or broken session flows; (ii) NAT, VPNs, and dynamic IP reassignment obscure true host identities and fragment communication graphs; (iii) port sharing and multiplexing introduce inconsistent flow semantics; and (iv) limited labeled data restricts supervised learning. Node features may be incomplete due to encryption or network topology changes. These conditions and limited training samples create “weak information” scenarios that impede effective graph information extraction for EMTD. Formally, broken structures manifest as sparse adjacency matrix A, while incomplete node features are represented by partial feature matrix H. Additionally, the number of labeled samples is scarce $( \mathrm { i . e . , } N _ { L } \ll | \mathcal { V } | )$ . Based on these characteristics, we formalize the concept of an impaired graph:

Definition 1. (Impaired Graph): Let the ideal attributed graph be $G ^ { \star } = ( V , A ^ { \star } , H ^ { \star } )$ , where $A ^ { \star } \in \{ 0 , 1 \} ^ { | V | \times | V | }$ and $H ^ { \star } \in$ $\mathbb { R } ^ { | V | \times d }$ . An impaired graph is the observed graph $\tilde { G } = ( V , \tilde { A } , \tilde { H } )$ generated by

$$
\tilde {A} = A ^ {\star} \odot \Omega_ {A}, \Omega_ {A} \in \{0, 1 \} ^ {| V | \times | V |},
$$

$$
\tilde {H} = H ^ {\star} \odot \Omega_ {H}, \quad \Omega_ {H} \in \{0, 1 \} ^ {| V | \times d},
$$

![](images/f0723ba65d49499c14c946148656fd646127c66bfe0cddf9e81fbf27f1e27e71.jpg)  
Fig. 2. Illustration of our TrustWI. (a) Learning the long-range propagation view (View-L) and structural augmentation view (View-S), then generating View-P based on them. (b) Learning the evidence uncertainty across three views. The Dirichlet distributions derived from these views are dynamically aggregated to capture view-specific uncertainties, yielding a fused Dirichlet distribution (View-F). (c) The proposed evidential learning loss guides model optimization through backpropagation.

where $\odot$ denotes the element-wise product. $\Omega _ { A }$ and $\Omega _ { H }$ model broken structures and incomplete features, respectively. In semisupervised EMTD, we are given a labeled node set $\nu \subset V$ with $| \nu | \ll | V |$ and labels $\mathbf { y } _ { \mathcal { V } } = \{ y _ { i } \} _ { i \in \mathcal { V } }$

As illustrated in Fig. 2, TrustWI transforms an impaired graph into a trustworthy classification. It generates three complementary views: a semantic view from long-range propagation (View-L), a repaired structural view via post-propagation augmentation (View-S), and an interaction view modeling their synergy (View-P). Each view yields an evidential opinion with quantified uncertainty, which are fused via an evidential-fusion rule for a final, robust decision.

## B. Multi-View Learning ofImpaired Graph

1) View-L Based on Long-Range Propagation: Graph Neural Networks (GNNs) facilitate complex relationship modeling by propagating information between neighboring nodes through graph structure. Traditional GNN-based EMTD approaches typically employ shallow architectures with 2∼3 layers [33] to mitigate over-smoothing [10], a phenomenon where excessive neighborhood aggregation leads to indistinguishable node representations. While this design choice proves effective for complete graphs, it becomes inadequate in weak information scenarios, as nodes cannot accumulate sufficient information for representation updates due to broken structures and incomplete features.

To address this challenge, we design a GNN module with long-range propagation mechanisms to enable sufficient information exchange across nodes, providing a long-range view (View-L). It compensates for information loss and captures complex malicious patterns in encrypted traffic by diffusing features over more than three hops, so that each node aggregates context from distant graph regions. Deep propagation can blur node identities, so we re-inject the original feature matrix $\mathbf { H } ^ { ( 0 ) }$ at every step via a restart term weighted by α, anchoring each node and preventing over-smoothing. We employ a diffusion-based propagation mechanism [34] formulated as:

![](images/f6ecd45715428ff8c07c940022763d5a04897702813b7c700a2593244ff699cb.jpg)  
Fig. 3. Conceptual information flow. Each view outputs a subjective opinion $\mathbf { M } ^ { v } = \{ \mathbf { b } ^ { v } , u ^ { v } \}$ , and the final opinion $\mathbf { M } = \{ \mathbf { b } , u \}$ is obtained via DS-based fusion (⊕).

$$
\mathbf {H} ^ {(t + 1)} = (1 - \alpha) \tilde {\mathbf {A}} \mathbf {H} ^ {(t)} + \alpha \mathbf {H} ^ {(0)},\tag{2}
$$

where $\mathbf { H } ^ { ( t ) }$ is the representation after the t-th propagation step $( { \bf H } ^ { ( 0 ) } = { \bf H }$ at initialization), $\alpha \in ( 0 , 1 ]$ is the restart probability, and $\tilde { \mathbf { A } }$ is the row-normalized adjacency matrix derived from A. The first term aggregates information from immediate neighbors, and the second preserves discriminative features while stabilizing long-range flow.

The second term serves multiple crucial purposes. Through periodic injection of original node features during propagation, this term preserves node-specific characteristics while acting as an anchor point to stabilize long-range information flow. This design enables deeper propagation iterations by preventing over-smoothing as nodes balance between accumulating distant information and maintaining their discriminative features. Combining these terms facilitates effective information propagation across longer graph distances while preserving node distinctiveness, particularly in weak information scenarios where local structures are compromised.

Through T propagation iterations, we obtain the final feature matrix H $( \mathrm { i . e . , } \mathbf { H } ^ { ( T ) } )$ that encodes a comprehensive long-range view of the impaired graph G. By employing a larger propagation depth $( T { = } 1 2 { \sim } 2 0 )$ , our method enables nodes to aggregate information beyond immediate neighborhoods, thus addressing missing edges in impaired graphs. The resulting enhanced node representations capture both local structures and global graph context, providing a more complete characterization of node behaviors despite structural impairments.

2) View-S Based on Post-Propagation Structural Augmentation: In encrypted traffic detection, node connectivity plays a vital role, as behavioral patterns during connection establishment and data transmission are key indicators of malicious activities. However, weak information scenarios pose significant challenges due to missing connections. Moreover, isolated nodes in the impaired graph cannot exchange information with others, severely hindering effective information propagation. While traditional approaches attempt to address this through edge-completion techniques based on initial node similarities, these methods show substantial limitations when handling weak information with incomplete node features, often generating false connections while missing genuine relationships. This not only fails to recover the actual network structure but may also introduce noise that compromises detection accuracy.

To address this challenge, we propose a post-propagation structural augmentation that constructs an augmented graph from the updated node semantics H learned in View-L. Leveraging these enriched representations instead of the incomplete initial features reduces both the chance of missing critical edges and the risk of adding spurious ones. Intuitively, we connect two nodes when their View-L embeddings are mutually similar enough to suggest a genuine relationship that the original graph may have missed. This view (View-S) therefore offers more reliable structural recovery with minimal noise. The augmented adjacency matrix A<sup>ˆ</sup> is defined as

$$
\hat {\mathbf {A}} _ {i j} = \left\{ \begin{array}{l l} 1 & s (\overline {{\mathbf {H}}} _ {i}, \overline {{\mathbf {H}}} _ {j}) \geq \min \bigl (\tau (\overline {{\mathbf {H}}} _ {i}, c), \tau (\overline {{\mathbf {H}}} _ {j}, c) \bigr) \\ \mathbf {A} _ {i j} & \text { otherwise } \end{array} \right.,\tag{3}
$$

where A is the original adjacency matrix. The function $s ( \overline { { \mathbf { H } } } _ { i } , \overline { { \mathbf { H } } } _ { j } )$ computes the cosine similarity between nodes $v _ { i }$ and $v _ { j }$ . For node $v _ { i } , \tau ( \overline { { \mathbf { H } } } _ { i } , c )$ is its cosine similarity with its c-th most similar node in H, and $\tau ( \overline { { \mathbf { H } } } _ { j } , c )$ is defined analogously for $v _ { j }$ The threshold c is chosen as $c = \operatorname* { m a x } ( | \mathcal { N } _ { i } | , | \mathcal { N } _ { j } | )$ , where $| \bar { \mathcal { N } } _ { i } |$ and $| { \mathcal { N } } _ { j } |$ are the neighborhood sizes of $v _ { i }$ and $v _ { j }$ in the original graph.

This formulation enables more accurate and contextually aware edge additions to the graph structure. By integrating this structural augmentation, View-S enriches the graph with additional meaningful connections, enhancing encrypted traffic detection through more complete structural information.

3) View-P Based on View Interaction: View-S is derived from View-L through structural augmentation, yet this unidirectional information flow overlooks the potential impact of augmented edges in View-S on the propagation dynamics in View-L. To address this limitation, we introduce a lightweight pseudo-view (View-P) through a computationally efficient twostep process. First, we apply a single iteration of diffusion-based information propagation (Eq. (2) in View-L) to View-S. Then, we concatenate the feature matrix from View-L (i.e., H) with the resultant feature matrix of this diffused View-S. This design effectively captures the complex interactions between views while minimizing trainable parameters and avoiding problematic recursive dependencies.

## C. Uncertainty-Aware View Fusion

After generating multiple views, the final step is to fuse them for a robust prediction. This fusion process is non-trivial in weak information scenarios, where there are two key challenges: 1) individual views may contain unreliable or biased knowledge, making simplistic fusion strategies prone to suboptimal results; and 2) conventional classification models often rely on Softmax, which is known to produce overconfident predictions that can compromise the fusion process.

To address these, we propose an uncertainty-aware view fusion strategy that adaptively integrates multi-view information. This design enhances prediction robustness by: 1) dynamically prioritizing more reliable views based on their sample-specific uncertainty; 2) providing a quantifiable uncertainty score for each prediction as an interpretable reliability indicator; and 3) facilitating practical decision-making by enabling targeted manual scrutiny when model confidence is low. This ensures more reliable EMTD in real-world deployments.

1) Uncertainty Quantification: We introduce an evidencebased framework for uncertainty measurement that goes beyond predicting a single probability vector $\mathbf { p } = [ p _ { 1 } , \dots , p _ { K } ]$ . Following subjective logic [35], we map class-wise belief masses and overall uncertainty to the parameters of a Dirichlet distribution α, enabling explicit per-class evidence together with associated confidence levels. Specifically, we model p as a Dirichlet distribution, the conjugate prior of the multinomial:

$$
\underbrace {\mathbf {p}} _ {D i s t r i b u t i o n} := \underbrace {D i r i c h l e t (\boldsymbol {\alpha})} _ {E v i d e n t i a l P r i o r},\tag{4}
$$

where ${ \pmb { \alpha } } = [ \alpha _ { 1 } , \alpha _ { 2 } , \ldots , \alpha _ { K } ]$ represents the evidential prior parameter, with $\alpha _ { k } = e _ { k } + 1$ for $k \in \{ 1 , \ldots , K \}$ and $e _ { k }$ denoting the accumulated evidence for class k. Based on this formulation, the probability density function of the distribution p is defined as:

$$
D i r (\mathbf {p} \mid \boldsymbol {\alpha}) = \left\{ \begin{array}{l l} \frac {1}{B (\boldsymbol {\alpha})} \prod_ {k = 1} ^ {K} p _ {k} ^ {\alpha_ {k} - 1} & \text { for } \mathbf {p} \in \mathbb {S} _ {K}, \\ 0 & \text { otherwise }, \end{array} \right.\tag{5}
$$

where $\mathbb { S } _ { K }$ denotes the (K-1) dimensional unit simplex of all $\mathbf { p } = [ p _ { 1 } , \dots , p _ { K } ]$ that satisfy $\textstyle \sum _ { k = 1 } ^ { K } p _ { k } = 1$ and $\forall k , 0 \leq p _ { k }$ $\leq 1 . B ( \alpha )$ represents the multinomial Beta function.

Intuitively, each Dirichlet parameter $\alpha _ { k } = e _ { k } + 1$ can be seen as $e _ { k }$ units of evidence poured into the k-th class bucket, and the total evidence S controls how much probability mass is left for uncertainty. This parameterization enables the model to capture both the belief mass $b _ { k } \geq 0$ for each class and the overall uncertainty mass $u \geq 0$ . Given a Dirichlet distribution, they are computed as

$$
b _ {k} = \frac {\alpha_ {k} - 1}{S} = \frac {e _ {k}}{S}, \quad u = \frac {K}{S},\tag{6}
$$

$$
s. t. u + \sum_ {k = 1} ^ {K} b _ {k} = 1, \quad S = \sum_ {k = 1} ^ {K} \alpha_ {k} = \sum_ {k = 1} ^ {K} (e _ {k} + 1),\tag{7}
$$

where K is the number of classes and S is the total evidence.

Learning to Form Opinions: We now elucidate our dualcomponent training paradigm for opinion formation learning. This approach integrates two key mechanisms: (i) evidence amplification to strengthen observed patterns and (ii) evidence attenuation (uncertainty elevation) in response to prediction errors. The first component functions as a data-fitting mechanism for the evidential model, while the second introduces a prior that suppresses spurious evidence and maintains appropriate uncertainty levels.

i) Maximizing the Model Fit: For a given sample $x _ { i } ,$ let $f ( x _ { i } | \Theta )$ denote the output evidence vector, where Θ represents the network parameters. The corresponding Dirichlet distribution is parameterized by $\pmb { \alpha } _ { i } = f ( x _ { i } | \Theta ) + 1$ . After parameter computation, the class probability estimate is obtained from the Dirichlet distribution’s expected value, expressed as $p _ { i k } = \alpha _ { i k } / S _ { i }$ , where $\begin{array} { r } { S _ { i } = \sum _ { k = 1 } ^ { K } \bar { \alpha _ { i k } } } \end{array}$ represents the Dirichlet intensity. Let $\mathbf { y } _ { i } = [ y _ { i 1 } , \dots , y _ { i K } ]$ denote the ground truth label of $x _ { i }$ . We measure the prediction-truth disparity using the crossentropy loss function:

$$
\begin{array}{l} \mathcal {L} _ {i} (\Theta) = \int \left[ \sum_ {k = 1} ^ {K} - y _ {i k} \log (p _ {i k}) \right] \frac {1}{B (\alpha_ {i})} \prod_ {k = 1} ^ {K} p _ {i k} ^ {\alpha_ {i k} - 1} \mathrm{d} \mathbf {p} _ {i} \\ = \sum_ {k = 1} ^ {K} y _ {i k} \left(\psi (S _ {i}) - \psi (\alpha_ {i k})\right), \end{array}\tag{8}
$$

where $\psi ( \cdot )$ denotes the Digamma function.

ii) Minimizing Evidence on Errors: While minimizing the aforementioned loss function optimizes model fit, this alone proves insufficient for handling prediction uncertainties effectively. To address this limitation, we introduce a mechanism that penalizes incorrect predictions by reducing their associated evidence. Specifically, when the model misclassifies traffic, our approach eliminates all evidence, as a Dirichlet distribution with zero evidence corresponds to maximum uncertainty $( u = 1 )$ This is implemented through a Kullback-Leibler (KL) divergence term in the loss function:

$$
\mathcal {L} ^ {R} (\Theta) = K L [ D i r (\mathbf {p} | \tilde {\alpha}) \| D i r (\mathbf {p} | \langle 1, \dots , 1 \rangle) ],\tag{9}
$$

where $\tilde { \alpha }$ denotes α with its ground truth label component replaced by 1. This term is a regularizer for our predictive distribution, penalizing deviations from maximum uncertainty.

The loss function for each view $\mathcal { L } ( \Theta )$ combines two components: the evidence maximization and the regularization:

$$
\mathcal {L} (\Theta) = \sum_ {i = 1} ^ {N _ {L}} \mathcal {L} _ {i} (\Theta) + \lambda_ {e} \mathcal {L} ^ {R} (\Theta),\tag{10}
$$

where $\lambda _ { e }$ is the hyperparameter controlling the trade-off between classification loss and KL divergence. Through this unified objective, the model pursues two complementary goals: maximizing predictive accuracy with sufficient evidence while maintaining appropriate levels of uncertainty in ambiguous cases. This formulation enables a principled balance between confident predictions and uncertainty quantification, yielding more reliable results.

2) Uncertainty-Aware View Fusion: After quantifying uncertainty for each view, we adopt the reduced Dempster-Shafer (DS) combination rule [11] to fuse the distinct views. This fusion mechanism is designed to be both robust and efficient; it dynamically weights each view according to its uncertainty level, separates belief from uncertainty explicitly to handle inter-view conflicts, and maintains lower computational complexity than conventional fusion approaches [36].

For each view, we derive its evidential representation $\mathbb { M } ^ { ( \cdot ) } =$ $\{ \{ b _ { k } ^ { ( \cdot ) } \} _ { k = 1 } ^ { K } , \boldsymbol { u } ^ { ( \cdot ) } \}$ through the uncertainty quantification method detailed in Section III-C1. The fusion of View-L $\mathbb { M } ^ { ( L ) }$ , View-S $\mathbb { M } ^ { ( S ) }$ , and View-P M<sup>(P</sup> <sup>)</sup> follows the combination rule to generate a fused view (View-F), which is formulated as:

$$
\mathbb {M} ^ {(F)} = \mathbb {M} ^ {(L)} \oplus \mathbb {M} ^ {(S)} \oplus \mathbb {M} ^ {(P)} = \{\{b _ {k} ^ {(F)} \} _ {k = 1} ^ {K}, u ^ {(F)} \},\tag{11}
$$

where the fusion of any two views (denoted by $\cdot ^ { \prime }$ and $\cdot ^ { \prime \prime } )$ is calculated as follows:

$$
b _ {k} = \frac {1}{1 - C} (b _ {k} ^ {\prime} b _ {k} ^ {\prime \prime} + b _ {k} ^ {\prime} u ^ {\prime \prime} + b _ {k} ^ {\prime \prime} u ^ {\prime}), u = \frac {1}{1 - C} u ^ {\prime} u ^ {\prime \prime},\tag{12}
$$

where $\begin{array} { r } { C = \sum _ { i \neq j } ^ { K } b _ { i } ^ { \prime } b _ { j } ^ { \prime \prime } } \end{array}$ quantifies the view conflict by aggregating products of belief masses assigned to distinct classes.

The theoretical validity of this fusion approach is established in the supplementary material. The analysis formally justifies our choice of the DS rule, showing it enhances accuracy by incorporating informative views while guaranteeing robustness, as even highly uncertain views do not significantly degrade performance. Furthermore, the analysis proves our method reduces overall prediction uncertainty and prevents false confidence generation by ensuring that high input uncertainty is appropriately propagated to the final output.

Training: We implement a multi-task learning framework to optimize the formation of subjective opinions across all views. The overall loss function is formulated as follows:

$$
\mathcal {L} ^ {a l l} (\Theta) = \mathcal {L} ^ {(L)} (\Theta) + \mathcal {L} ^ {(S)} (\Theta) + \mathcal {L} ^ {(P)} (\Theta) + \mathcal {L} ^ {(F)} (\Theta),\tag{13}
$$

where $\mathcal { L } ^ { ( L ) } ( \Theta ) , \mathcal { L } ^ { ( S ) } ( \Theta ) , \mathcal { L } ^ { ( P ) } ( \Theta )$ , and $\mathcal { L } ^ { ( F ) } ( \Theta )$ denote the loss functions for View-L, View-S, View-P, and View-F, respectively, each calculated according to Eq. (10).

Discussion: The overall information flow of our multi-view framework is summarized in Fig. 3, and the procedure is detailed in Algorithm 1. Conceptually, our design differs from standard Mixture-of-Experts (MoE) models. Each view outputs its own confidence evidence, rather than relying on a separate gating network. We fuse each view opinions via DS theory to obtain both predictions and uncertainty. The views are progressively refined – View-L enhances semantics via long-range propagation, View-S repairs structure using the resulting embeddings, and View-P models their interactions. We adopt Evidential Deep Learning (EDL) since Dirichlet evidence is naturally compatible with DS fusion, whereas MC Dropout or deep ensembles require multiple forward passes and do not provide a principled belief-fusion mechanism.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: Training Algorithm of TrustWI.

Input: Adjacency matrix A; Feature matrix H.
Propagation steps T; Restart probability α.
/* View-L
*/
1 Compute  $\overline{H} \leftarrow$ propagation(A, H, T, α) via Eq. (2);
/* View-S
*/
2 for Each  $v_i \in V$  do
3    for Each  $v_j \in V$  and  $j \neq i$  do
4    Compute  $s_{ij} \leftarrow$ cosine_similarity( $\overline{H}_i$ ,  $\overline{H}_j$ );
5    Compute  $c \leftarrow$ max(|Nᵢ|, |Nⱼ|);
6    Compute threshold  $\tau_{i,c}$  and  $\tau_{j,c} \leftarrow$ similarity to c-th neighbor;
7    if  $s_{ij} &gt; \min(\tau_{i,c}, \tau_{j,c})$  then
8    Add edge (i, j) to augmented edge set  $\hat{A}$ ;
9    end
10    end
11 end
12 // The above procedure corresponds to Eq. (3);
/* View-P
*/
13 Compute H' ← propagation( $\hat{A}$ ,  $\overline{H}$ , 1, α) via Eq. (2);
14 Generate View-P embedding H'' ← CONCAT( $\overline{H}$ , H');
15 for each view do
16    Compute Dir(p(·) | α(·)) ← variational network:
f(·);
17    Generate subjective opinion
M(·) ← Dir(p(·) | α(·));
18 end
/* View-F
*/
19 Generate fused opinion M(F) via Eq. (11);
/* Induce joint evidence
*/
20 Compute S ← K/u, e_k ← b_k × S, α_k ← e_k + 1;
21Generate Dirichlet distribution Dir(p | α) via Eq. (6);
22Compute the overall loss L^all via Eq. (13);
23Update model parameters via gradient descent.

Accuracy (%) 90
(a) TONIoT
(b) DoHBrw
(c) CICIDS
</div>

Fig. 4. Accuracy of methods w.r.t. different feature missing rates on three evaluation datasets.

## IV. EVALUATION

## A. Experimental Setup

Datasets: We evaluate our approach on three real-world datasets: (i) TONIoT [37], an IoT traffic dataset containing 796,380 normal and 21,542,641 malicious instances with 10 attack types across 39 features; (ii) DoHBrw [38], a DNS over HTTPS traffic dataset comprising 19,807 normal and 354,996 malicious instances across 28 features; (iii) CICIDS [39], a network traffic dataset consisting of 931,873 normal and 18,028 malicious instances across 70 features. Table I presents the statistics of the evaluated datasets.

TABLE I  
STATISTICS OF DATASETS. W/ EXTREME DENOTES THE EXTREMELY WEAK INFORMATION SCENARIO

<table><tr><td>Dataset</td><td>#Node</td><td>#Edge</td><td>#Isolated Node</td><td>#Feature</td></tr><tr><td>TONIoT</td><td>1,000,000</td><td>9,287,986</td><td>537,379</td><td>39</td></tr><tr><td>w/ Extreme</td><td>10,000</td><td>2,360</td><td>5,380</td><td>39</td></tr><tr><td>DoHBrw</td><td>269,643</td><td>582,246</td><td>81,501</td><td>29</td></tr><tr><td>w/ Extreme</td><td>2,000</td><td>802</td><td>3,498</td><td>29</td></tr><tr><td>CICIDS</td><td>949,901</td><td>7,947,136</td><td>391,433</td><td>70</td></tr><tr><td>w/ Extreme</td><td>15,000</td><td>271,584</td><td>106,051</td><td>70</td></tr></table>

Testbeds: Our experiments are conducted on a computational platform with an Intel i5-14600KF 3.50 GHz CPU, an NVIDIA GeForce GTX 4060 Ti GPU, and 32 GB of system memory. We use the PyTorch Geometric (PyG) library to implement graphbased encoders for baselines.

Baselines: We compare our TrustWI against three categories of baselines:

(i) Conventional GNNs: GCN [33] is a foundational model for semi-supervised node classification using spectral graph convolutions. GAN [40] uses masked self-attention to weigh neighbor importance, improving upon standard graph convolutions. PPNP [34] decouples feature transformation from propagation, enabling deeper information propagation without the risk of over-smoothing.

(ii) Traffic detection models: Kitsune [2] uses incremental online learning to learn the features of each package. ST-Graph [13] constructs a spatio-temporal graph to model both connection relationships (spatial) and their timing (temporal). MTSecurity [41] fuses byte-level sequence features from a Transformer with graph-based interaction features from a GNN to enhance malicious traffic representation. ContraMTD [14] captures both local behavior features (sequence and density of behaviors) and global interaction features (topological relationships in host interaction graphs) using proposed SEC and DE-GAT mechanisms to handle weak information.

(iii) Weak information-based approaches: Pro-GNN [42] directly models the adjacency matrix with learnable parameters and learns it with GNN alternatively. The low-rank attribute eliminates the opposing edges, while regularization enhances sparsity and smoothness in the features during the learning process. MI-GNN [17] augments the original graph using complementary information (features, labels, and structure) to improve the graph representation and finally uses multi-task view learning to learn three kinds of supplementary graph information, respectively. RAPIER [8] estimates data distribution using a deep generative model and re-labels training data based on the density distribution, thus correcting the label noise. Once corrected, it generates new training data through an improved GAN.

Hyperparameter Tuning: For all methods, we find the best hyperparameters using grid search over a search space:

\- Number of epochs: [100, 200, 400, 500];

\- Learning rate: [1e-1, 1e-2, 1e-3];

TABLE II  
PERFORMANCE COMPARISON OF OUR TRUSTWI WITH BASELINES IN WEAK INFORMATION SCENARIO ACROSS THREE DATASETS. THE BEST AND RUNNER-UERESULTS ARE HIGHLIGHTED IN BOLD AND UNDERLINED, RESPECTIVELY.

<table><tr><td rowspan="2">Dataset Method</td><td colspan="5">TONIoT</td><td colspan="5">DoHBrw</td><td colspan="5">CICIDS</td></tr><tr><td>ACC</td><td>PR</td><td>RC</td><td>F1</td><td>AUC</td><td>ACC</td><td>PR</td><td>RC</td><td>F1</td><td>AUC</td><td>ACC</td><td>PR</td><td>RC</td><td>F1</td><td>AUC</td></tr><tr><td>GCN</td><td>49.80</td><td>35.13</td><td>49.80</td><td>39.26</td><td>72.46</td><td>76.28</td><td>79.35</td><td>76.28</td><td>68.92</td><td>75.36</td><td>55.42</td><td>37.68</td><td>55.42</td><td>43.82</td><td>56.09</td></tr><tr><td>GAT</td><td>57.27</td><td>59.07</td><td>57.27</td><td>54.66</td><td>83.18</td><td>83.69</td><td>83.67</td><td>83.67</td><td>83.67</td><td>83.68</td><td>58.45</td><td>63.50</td><td>58.45</td><td>47.65</td><td>78.69</td></tr><tr><td>PPNP</td><td>70.04</td><td>73.04</td><td>70.04</td><td>68.70</td><td>91.34</td><td>92.83</td><td>93.25</td><td>92.83</td><td>89.52</td><td>51.02</td><td>79.01</td><td>84.94</td><td>86.36</td><td>84.66</td><td>84.12</td></tr><tr><td>Kitsune</td><td>62.01</td><td>51.16</td><td>62.01</td><td>56.02</td><td>59.81</td><td>86.25</td><td>86.81</td><td>86.25</td><td>86.23</td><td>86.42</td><td>73.40</td><td>71.87</td><td>73.40</td><td>71.16</td><td>75.71</td></tr><tr><td>ST-Graph</td><td>68.83</td><td>55.11</td><td>50.33</td><td>50.41</td><td>80.10</td><td>92.38</td><td>93.59</td><td>92.38</td><td>92.88</td><td>79.73</td><td>89.24</td><td>87.00</td><td>90.87</td><td>88.69</td><td>82.51</td></tr><tr><td>MTSecurity</td><td>56.53</td><td>57.38</td><td>53.42</td><td>52.16</td><td>64.15</td><td>84.67</td><td>84.70</td><td>84.67</td><td>84.67</td><td>84.69</td><td>83.02</td><td>83.21</td><td>83.02</td><td>81.00</td><td>84.92</td></tr><tr><td>ContraMTD</td><td>63.05</td><td>51.14</td><td>63.05</td><td>52.75</td><td>81.63</td><td>91.09</td><td>86.37</td><td>91.09</td><td>88.51</td><td>51.32</td><td>61.02</td><td>52.23</td><td>61.02</td><td>55.32</td><td>75.90</td></tr><tr><td>Pro-GNN</td><td>76.57</td><td>74.70</td><td>76.57</td><td>74.70</td><td>83.85</td><td>95.16</td><td>94.69</td><td>95.16</td><td>94.79</td><td>80.19</td><td>90.30</td><td>87.49</td><td>90.30</td><td>88.15</td><td>97.19</td></tr><tr><td>MI-GNN</td><td>74.41</td><td>71.72</td><td>74.41</td><td>72.38</td><td>90.68</td><td>97.03</td><td>96.87</td><td>97.03</td><td>97.89</td><td>84.80</td><td>91.06</td><td>88.26</td><td>91.06</td><td>89.04</td><td>96.97</td></tr><tr><td>RAPIER</td><td>66.77</td><td>53.62</td><td>66.77</td><td>57.14</td><td>89.95</td><td>86.75</td><td>86.81</td><td>86.75</td><td>86.75</td><td>86.79</td><td>85.45</td><td>83.60</td><td>85.45</td><td>83.49</td><td>75.04</td></tr><tr><td>TrustWI (Our)</td><td>77.17</td><td>77.54</td><td>77.17</td><td>76.93</td><td>93.72</td><td>97.44</td><td>97.34</td><td>97.44</td><td>97.36</td><td>87.75</td><td>91.64</td><td>89.63</td><td>91.64</td><td>90.01</td><td>97.37</td></tr><tr><td>Improv. ↑</td><td>0.60</td><td>2.84</td><td>0.60</td><td>2.23</td><td>2.38</td><td>0.41</td><td>0.47</td><td>0.41</td><td>-0.53</td><td>0.96</td><td>0.58</td><td>1.37</td><td>0.58</td><td>0.97</td><td>0.18</td></tr></table>

\- Hidden unit of MLP: [16, 32, 64, 128, 256, 512];

\- Number of attention heads of GAT: [4, 6, 8];

\- Number of layers/propagation iterations T: [3, 4, 6, 8, 12, 16, 20];

\- Restart probability α: [0.01, 0.05, 0.1].

Metrics: To evaluate the model’s performance, we employ multiple metrics: accuracy (ACC), precision (PR), recall (RC), F1-score (F1), and AUC.

Implementation Details: Following standard protocol [43], we simulate ‘weak information’ scenarios by randomly removing 50% of edges and masking 50% of node features with zeros. We perform stratified random sampling to ensure balanced representation of normal and malicious flows. For ‘extremely weak information’ scenarios, less than 2% of labeled nodes are selected while preserving the original class distribution. For non-graph baselines (e.g., Kitsune and RAPIER), only feature incompleteness is simulated, while the graph structure is not constructed. All datasets are split using a 3:1 ratio for training and testing.

We train our model for 1,000 epochs using the AdamW optimizer [44]. The learning rates are set to 0.001, 0.01, and 0.001 for TONIoT, DoHBrw, and CICIDS, respectively. In Eq. (2), the number of propagation steps T is set to 12 for TONIoT and DoHBrw, and 20 for CICIDS, with restart probability α = 0.01. The regularization coefficient λ<sub>e</sub> in Eq. (10) is initialized as 0.01 and linearly increased by 0.01 per epoch until reaching a maximum value of 1. The variational network (f in Fig. 2) is implemented using a two-layer MLP. To facilitate reproducibility and foster future research, we make the source code of TrustWI publicly available.<sup>1</sup>

## B. Experimental Results

1) Evaluation on Benchmarks: Table II presents the detection performance comparison between TrustWI and baselines across three datasets under weak information scenarios. The results demonstrate that TrustWI achieves the best performance in nearly all cases, with only a marginal disadvantage in F1- score compared to MI-GNN on DoHBrw. Notably, on TONIoT, which features more complex malicious traffic distributions, TrustWI significantly improves AUC from 91.34% to 93.72%. This enhancement highlights the model’s effectiveness in leveraging multi-view information integration for robust detection under weak information conditions.

ST-Graph outperforms other traffic detection methods through its spatiotemporal heterogeneous graph design and effective integration of network communication patterns. PPNP achieves strong results by decoupling propagation from prediction, enabling comprehensive neighborhood information assimilation via multi-step iterations. ContraMTD’s performance deteriorates significantly under weak information scenarios, as its effectiveness heavily relies on contrastive learning to capture consistency between local behavior and global interaction features. Methods specifically designed for weak information scenarios, including our TrustWI, demonstrate optimal detection capabilities. Among these approaches, TrustWI achieves superior performance through its novel multi-view information integration and adaptive view fusion, enabling robust detection even with incomplete network data.

As for the scenario where less than 2% training data is available, all models have experienced performance degradation, as expected (shown in Table III). However, our model remains the most effective, and in this case, the role of pseudo-view becomes more evident. With the decrease in sample size, pseudo-view helps to make up for the lack of data, further enhances the robustness of the model, and improves the overall detection performance.

2) Evaluation in Extremely Weak Information Scenario: To further validate TrustWI’s robustness, we conduct a comparative analysis under conditions of extreme information sparsity. Specifically, we evaluate performance using a highly constrained subset of less than 2% of training samples. Results on three datasets are presented in Table III. The DoHBrw empirical results demonstrate that TrustWI significantly outperforms baselines by a large margin. Compared to RAPIER, the bestperforming baseline that only encounters feature incompleteness as a non-graph method, our method substantially improves AUC from 85.45% to 89.57%. This enhancement is significant as TrustWI successfully handles incomplete features and graph structures. The proposed multi-view learning and uncertaintyaware view fusion in TrustWI enable robust detection even with highly limited training data.

TABLE III  
PERFORMANCE COMPARISON OF OUR TRUSTWI WITH BASELINES IN EXTREMELY WEAK INFORMATION SCENARIO ACROSS THREE DATASETS USING A SMALLPART OF TRAINING DATA. THE BEST AND RUNNER-UP RESULTS ARE HIGHLIGHTED IN BOLD AND UNDERLINED, RESPECTIVELY.

<table><tr><td rowspan="2">Dataset Method</td><td colspan="5">TONIoT</td><td colspan="5">DoHBrw</td><td colspan="5">CICIDS</td></tr><tr><td>ACC</td><td>PR</td><td>RC</td><td>F1</td><td>AUC</td><td>ACC</td><td>PR</td><td>RC</td><td>F1</td><td>AUC</td><td>ACC</td><td>PR</td><td>RC</td><td>F1</td><td>AUC</td></tr><tr><td>GCN</td><td>31.73</td><td>39.62</td><td>31.73</td><td>23.37</td><td>79.20</td><td>67.33</td><td>78.31</td><td>67.33</td><td>64.29</td><td>68.23</td><td>37.80</td><td>37.62</td><td>37.80</td><td>31.88</td><td>82.00</td></tr><tr><td>GAT</td><td>50.65</td><td>51.38</td><td>50.65</td><td>45.20</td><td>50.41</td><td>72.83</td><td>74.24</td><td>72.83</td><td>72.27</td><td>72.42</td><td>42.14</td><td>54.12</td><td>42.14</td><td>40.55</td><td>76.50</td></tr><tr><td>PPNP</td><td>54.00</td><td>54.26</td><td>54.00</td><td>54.05</td><td>54.07</td><td>79.00</td><td>79.00</td><td>79.00</td><td>79.00</td><td>78.97</td><td>67.63</td><td>69.67</td><td>67.63</td><td>65.01</td><td>85.17</td></tr><tr><td>Kitsune</td><td>46.58</td><td>48.02</td><td>46.58</td><td>44.28</td><td>88.55</td><td>64.39</td><td>57.38</td><td>53.42</td><td>52.16</td><td>64.15</td><td>63.75</td><td>63.93</td><td>63.75</td><td>63.80</td><td>65.73</td></tr><tr><td>ST-Graph</td><td>57.15</td><td>55.25</td><td>57.15</td><td>52.42</td><td>50.88</td><td>72.83</td><td>74.24</td><td>72.83</td><td>72.27</td><td>72.42</td><td>64.74</td><td>62.32</td><td>64.74</td><td>61.94</td><td>88.10</td></tr><tr><td>MTSecurity</td><td>46.70</td><td>47.31</td><td>46.70</td><td>45.10</td><td>47.25</td><td>78.50</td><td>75.83</td><td>78.50</td><td>76.58</td><td>74.11</td><td>70.82</td><td>69.56</td><td>70.82</td><td>68.67</td><td>84.02</td></tr><tr><td>ContraMTD</td><td>59.11</td><td>42.21</td><td>59.11</td><td>48.64</td><td>79.84</td><td>82.92</td><td>83.04</td><td>82.92</td><td>82.92</td><td>82.98</td><td>60.64</td><td>58.66</td><td>60.64</td><td>58.60</td><td>92.70</td></tr><tr><td>Pro-GNN</td><td>61.71</td><td>57.53</td><td>61.71</td><td>57.42</td><td>84.09</td><td>83.67</td><td>83.69</td><td>83.67</td><td>83.67</td><td>83.68</td><td>73.40</td><td>71.87</td><td>73.40</td><td>71.16</td><td>92.87</td></tr><tr><td>MI-GNN</td><td>62.05</td><td>62.84</td><td>62.05</td><td>60.04</td><td>83.36</td><td>84.42</td><td>84.99</td><td>84.42</td><td>84.39</td><td>84.59</td><td>72.58</td><td>71.27</td><td>72.58</td><td>70.02</td><td>89.49</td></tr><tr><td>RAPIER</td><td>62.56</td><td>58.78</td><td>62.56</td><td>58.33</td><td>84.79</td><td>85.50</td><td>85.51</td><td>85.50</td><td>85.49</td><td>85.45</td><td>74.18</td><td>72.44</td><td>74.18</td><td>72.60</td><td>89.60</td></tr><tr><td>TrustWI (Our)</td><td>63.70</td><td>66.75</td><td>63.70</td><td>62.44</td><td>85.17</td><td>89.67</td><td>89.78</td><td>89.67</td><td>89.65</td><td>89.57</td><td>74.26</td><td>71.85</td><td>74.26</td><td>72.36</td><td>93.26</td></tr><tr><td>Improv. ↑</td><td>1.14</td><td>3.91</td><td>1.14</td><td>2.40</td><td>-3.38</td><td>4.17</td><td>4.27</td><td>4.17</td><td>4.16</td><td>4.12</td><td>0.08</td><td>-0.59</td><td>0.08</td><td>-0.24</td><td>0.39</td></tr></table>

![](images/1fa19a2a55bc58f86e1046e7b874026a0519cc7b168cd826814372156506e07c.jpg)  
Fig. 5. Accuracy of methods w.r.t. different structure degradation rates on three evaluation datasets.

TABLE IV  
AUC UNDER DIFFERENT ANNOTATION RATIOS WITH 50% MISSING STRUCTURE AND FEATURES

<table><tr><td>Label ratio</td><td>GCN</td><td>Pro-GNN</td><td>MI-GNN</td><td>TrustWI (Ours)</td></tr><tr><td>0.5%</td><td>68.45</td><td>78.10</td><td>77.24</td><td>82.35</td></tr><tr><td>1.0%</td><td>73.12</td><td>81.45</td><td>80.15</td><td>83.90</td></tr><tr><td>5.0%</td><td>83.56</td><td>87.10</td><td>86.42</td><td>88.42</td></tr></table>

## 3) Robustness Analysis:

a) Weak Information: To verify our method’s robustness in handling various aspects of missing information, we conducted comparative experiments on datasets with broken structures and incomplete features. As shown in Figs. 4 and 5, we present accuracy values of all methods under different degrees of information loss. Our model shows excellent performance in these scenarios, and even when the degree increases, it always obtains higher accuracy than baseline.

We further evaluate TrustWI under varying annotation ratios (0.5%, 1%, and 5%) with stratified sampling. As shown in the Table IV, our TrustWI achieves the best AUC across all ratios, supporting its robustness under severe label scarcity.

TABLE V  
ACC OF VARIOUS MODELS UNDER DIFFERENT LABEL NOISE RATIOS (OTHER DEGRADATIONS SET TO ZERO)

<table><tr><td>Dataset</td><td>Model</td><td>Clean</td><td>+10% noise</td><td>+30% noise</td><td>+50% noise</td></tr><tr><td rowspan="3">TONIoT</td><td>TrustWI</td><td>91.1</td><td>88.9 (-2.2)</td><td>84.3 (-6.8)</td><td>78.5 (-12.6)</td></tr><tr><td>GCN</td><td>83.6</td><td>75.0 (-8.6)</td><td>66.1 (-17.5)</td><td>55.7 (-27.9)</td></tr><tr><td>GAT</td><td>84.4</td><td>76.3 (-8.1)</td><td>67.0 (-17.4)</td><td>56.9 (-27.5)</td></tr><tr><td rowspan="3">DoHBrw</td><td>TrustWI</td><td>98.5</td><td>97.6 (-0.9)</td><td>96.4 (-2.1)</td><td>95.8 (-2.7)</td></tr><tr><td>GCN</td><td>92.0</td><td>82.8 (-9.2)</td><td>80.3 (-11.7)</td><td>75.9 (-16.1)</td></tr><tr><td>GAT</td><td>94.1</td><td>84.2 (-9.9)</td><td>82.5 (-11.6)</td><td>80.2 (-13.9)</td></tr><tr><td rowspan="3">CICIDS</td><td>TrustWI</td><td>93.1</td><td>91.1 (-2.0)</td><td>89.2 (-3.9)</td><td>88.3 (-4.8)</td></tr><tr><td>GCN</td><td>84.2</td><td>83.0 (-1.2)</td><td>73.4 (-10.8)</td><td>60.2 (-24.0)</td></tr><tr><td>GAT</td><td>85.8</td><td>83.8 (-2.0)</td><td>74.1 (-11.7)</td><td>63.3 (-22.5)</td></tr></table>

TABLE VI

ROBUSTNESS TO TARGETED EDGE INJECTION ATTACKS (REI) ON TONIOT

<table><tr><td>REI</td><td>Simple fusion</td><td>Pre-propagation</td><td>TrustWI (Ours)</td></tr><tr><td>0% (default)</td><td>87.12</td><td>90.85</td><td>93.72</td></tr><tr><td>5%</td><td>80.12</td><td>86.40</td><td>92.15</td></tr><tr><td>10%</td><td>75.66</td><td>81.22</td><td>91.32</td></tr><tr><td>20%</td><td>67.30</td><td>73.95</td><td>88.47</td></tr></table>

b) Label Noise: We further examine robustness to incorrect annotations by injecting label noise. Specifically, 10%, 30%, and 50% of the training labels are randomly flipped, with all other degradations disabled to isolate this effect. As shown in Table V, TrustWI consistently degrades more gracefully than baselines. For example, at 50% noise on TONIoT, TrustWI drops by only 12.6 points, whereas baselines drop by nearly 28 points. This resilience is attributed to our uncertainty-aware fusion, which down-weights conflicting evidence from mislabeled nodes.

c) Adversarial Interference: Further, since graph structure at inference time may be vulnerable to adversarial interference, we evaluate robustness on the TONIoT test set using random edge injection (REI), which injects fake edges between anomalous and benign nodes. Results in Table VI show that all methods degrade as REI increases, while TrustWI remains relatively stable, indicating higher resilience to attack induced structural noise. We attribute this to our uncertainty aware evidential fusion, which reduces the influence of unreliable evidence when the structure is perturbed.

![](images/6f02a4704673fd2e615e83bce28eeeeac55690abfb1cca50895ed125b79a76b3.jpg)  
(a) TONIoT

![](images/5f3d2d014bdb7e0cb0d2ac1b04e5d68b83a8deb595cda9be71536183f0553b0b.jpg)  
Fig. 6. Uncertainty distribution of our TrustWI.

![](images/ce766f3057453080507d642c920a4fca801d64cc69b4dd9da814808662c9184a.jpg)

![](images/111c17c809bf6c41adf1674999aee42213dd9a6edc6188a8966df21f6d28670a.jpg)  
(a) TONIoT

![](images/c1f42398a79c9a51c44ee30609f055068acec500692e4071caab7a483163f06f.jpg)  
(b) DoHBrw

![](images/4c987a8b26e3a1875eaabadc3c2c80e35c2e60d5b9368ce36dabdd7d3121c2cf.jpg)  
(c) CICIDS

Fig. 7. Uncertainty density of TrustWI under noise.  
![](images/a423de493efc72bbcee74028c2ce1ff89d1a6703efa7088307ed130c4d678020.jpg)  
(a) Accuracy

![](images/a26ab8e23402a989abd980eeb6a66b1e0f609ffbd70f964ce4a9e087d76d44cc.jpg)  
(b) Uncertainty  
Fig. 8. Contribution analysis of individual views.

## 4) Qualitative Analysis:

a) Discriminative Power: We visualized the model’s final prediction distribution. As shown in Fig. 6, predictions for both normal and malicious samples are highly concentrated at the extremes of the probability space. This strong intra-cluster cohesion and clear class separation provide qualitative evidence of TrustWI’s high discriminative power.

b) Data Noise: We validated the model’s uncertainty estimation by injecting Gaussian noise into the test data. Fig. 7 shows that the model’s predicted uncertainty increases in direct proportion to the noise intensity (σ). The results show that uncertainty increases proportionally with noise intensity, demonstrating that TrustWI effectively quantifies network noise through uncertainty measures. This capability has significant practical value. For instance, when encountering substantial encrypted malicious traffic, the elevated uncertainty can trigger timely interventions from network administrators.

c) View Contribution Analysis: To analyze the contribution of each view, we visualized their final performance and uncertainty on the DoHBrw dataset as box plots (Fig. 8). The analysis reveals two key findings: 1) the fused View (V-F) achieves a median accuracy competitive with the best-performing individual view (V-S), and 2) V-F exhibits markedly lower and more concentrated uncertainty than any single view. This combination of maintaining accuracy while dramatically reducing uncertainty is the key synergy of our fusion approach. The mechanism enabling this synergy is further illustrated in a visualization of a representative subgraph (Fig. 9). The analysis shows that views more closely resembling the ideal topology consistently yield lower uncertainty. This confirms that our uncertainty-guided mechanism successfully emphasizes more reliable views during fusion, converting complementary evidence into predictions that are both accurate and substantially more reliable.

![](images/fb8b83662a69d856ece4f9ec13b979097c03154329e3f9f7386fdc79d97f9525.jpg)  
Fig. 9. Uncertainty (%) of different views in TrustWI.

## 5) Ablation Study:

a) Multi-View Learning: To validate the advantages of multi-view learning, Table VII (variants (a)–(c)) compares the AUC performance between single-view approaches (View-L et al.) and our multi-view method. The results show that our multi-view methodology significantly outperforms single-view approaches, which are inherently limited in weak information scenarios where individual views may lack reliability. This performance gap demonstrates the importance of multi-view fusion in integrating complementary information from different perspectives for more robust predictions.

b) Evidential Fusion: We compare our evidential fusion with four alternative strategies: Simple Fusion (equal weights for all views), Simple Fusion , Attention Fusion (attention-based integration), and Attention Fusion<sup>-</sup>, where (·)<sup>-</sup> indicates the models without uncertainty learning. Results in Table VII (variants (d)–(g)) show the superiority of our evidential fusion method. In contrast to these variants, our approach leverages the summation operation on Dirichlet distribution for uncertainty-aware fusion, enabling adaptive view importance adjustment. Additionally, comparing variants (d) with (e) and (f) with (g) shows that incorporating uncertainty learning via the regularization term of Eq. (9) improves performance even when uncertainty is not directly used for fusion guidance.

c) Structural Augmentation: Pre-Propagation vs. Post-Propagation: We examine the impact of operation order by comparing structural augmentation before and after long-range propagation. Table VII (variant (h)) demonstrates degraded performance in the pre-propagation setup, indicating that premature structural augmentation introduces incorrect edges due to unreliable initial node semantics. In contrast, our post-propagation design prevents this. It first establishes reliable node embeddings through long-range propagation, and only then performs structural augmentation. This sequence is critical for mitigating the risk of semantic leakage, which we define as the propagation of errors that occurs when noisy or incomplete initial node features are used to infer new graph connections, thereby corrupting the graph’s topology.

TABLE VII  
ABLATION STUDY OF TRUSTWI

<table><tr><td rowspan="2">Method</td><td rowspan="2">Post-Propagation</td><td rowspan="2">Evidential Fusion</td><td rowspan="2">Uncertainty Learning</td><td colspan="2">TONIoT</td><td colspan="2">DoHBrw</td><td colspan="2">CICIDS</td></tr><tr><td>AC</td><td>AUC</td><td>AC</td><td>AUC</td><td>AC</td><td>AUC</td></tr><tr><td>(a) View-L</td><td>√</td><td>-</td><td>√</td><td>57.22</td><td>81.25</td><td>91.33</td><td>90.88</td><td>83.56</td><td>89.12</td></tr><tr><td>(b) View-S</td><td>√</td><td>-</td><td>√</td><td>68.21</td><td>82.77</td><td>92.23</td><td>92.17</td><td>84.17</td><td>88.99</td></tr><tr><td>(c) View-P</td><td>√</td><td>-</td><td>√</td><td>72.59</td><td>85.26</td><td>64.92</td><td>67.03</td><td>81.01</td><td>83.12</td></tr><tr><td>(d) Simple Fusion</td><td>√</td><td>×</td><td>√</td><td>74.25</td><td>87.12</td><td>96.35</td><td>97.22</td><td>88.87</td><td>92.80</td></tr><tr><td>(e) Simple Fusion*</td><td>√</td><td>×</td><td>×</td><td>73.80</td><td>86.90</td><td>93.34</td><td>94.35</td><td>86.84</td><td>90.66</td></tr><tr><td>(f) Attention Fusion</td><td>√</td><td>×</td><td>√</td><td>74.47</td><td>87.15</td><td>96.95</td><td>98.09</td><td>90.82</td><td>92.12</td></tr><tr><td>(g) Attention Fusion*</td><td>√</td><td>×</td><td>×</td><td>74.29</td><td>87.52</td><td>95.06</td><td>96.71</td><td>89.20</td><td>91.73</td></tr><tr><td>(h) Pre-Propagation</td><td>×</td><td>√</td><td>√</td><td>74.87</td><td>90.85</td><td>95.57</td><td>89.92</td><td>85.47</td><td>89.04</td></tr><tr><td>Default</td><td>√</td><td>√</td><td>√</td><td>77.17</td><td>93.72</td><td>97.44</td><td>87.75</td><td>91.64</td><td>97.37</td></tr></table>

TABLE VIII

![](images/fc9801bcd187ea6cd3b57d0960bf6c51da69a2493b7cd9e980de11d9fa6caca5.jpg)  
Fig. 10. Impact of the propagation iteration number T.

## 6) Sensitivity Analysis:

a) Long-Range Propagation: To validate TrustWI’s capability to capture long-range information, we conduct experiments by varying the number of propagation steps in View-L. As shown in Fig. 10, model performance across all datasets peaks at T=12∼20 steps, demonstrating effective long-range information utilization without over-smoothing. These results confirm that long-range propagation is essential for addressing weak information scenarios.

TABLE IX  
Fig. 11. Impact of the restart probability α.  
AUC OF METHODS W.R.T. DIFFERENT GRAPH CONSTRUCTION METHOD ON TONIOT DATASET  
![](images/5635250662f0a907861090525a9ac40f214613cae23249e4c045f5fba6bd18ba.jpg)

b) Restart Probability: Fig. 11 shows model performance across different α values in Eq. (2). When α = 0, excluding the second term, performance deteriorates due to over-smoothing. Conversely, an excessive α reduces the benefits of long-range information propagation. A moderate α achieves optimal performance, demonstrating the importance of combining both long-range and local features.

<table><tr><td>Base graph</td><td>Default</td><td>w/o View-L</td><td>w/o View-S</td></tr><tr><td>Direct communication (Our)</td><td>93.7</td><td>82.8 (-10.9)</td><td>81.3 (-12.4)</td></tr><tr><td>Temporal sequence</td><td>93.2</td><td>82.0 (-11.2)</td><td>80.1 (-13.1)</td></tr><tr><td>Multi-relational</td><td>93.4</td><td>82.3 (-11.1)</td><td>83.9 (-9.5)</td></tr></table>

IMPACT OF NEIGHBOR THRESHOLD AND SIMILARITY METRIC ON AUGMENTATION QUALITY IN TONIOT DATASET

<table><tr><td>Setting</td><td>False edge rate (%)</td><td>AUC (%)</td></tr><tr><td colspan="3">1. Neighbor threshold c</td></tr><tr><td> $c = \max(|\mathcal{N}_i|, |\mathcal{N}_j|)$ </td><td>12.5</td><td>93.7</td></tr><tr><td> $c = 5$ </td><td>7.8</td><td>91.2</td></tr><tr><td> $c = 10$ </td><td>22.1</td><td>91.6</td></tr><tr><td> $c = 20$ </td><td>24.6</td><td>90.1</td></tr><tr><td colspan="3">2. Similarity metric</td></tr><tr><td>Cosine similarity</td><td>14.8</td><td>93.7</td></tr><tr><td>Euclidean distance (L2)</td><td>21.7</td><td>90.8</td></tr><tr><td>Pearson correlation</td><td>15.1</td><td>91.4</td></tr></table>

c) Graph Construction Method: To demonstrate the robustness of our framework and the critical importance of its components, we conducted an ablation study in Table VIII to assess our framework’s robustness to different graph construction methods. The results are twofold: first, with our full components active the AUC is at least 0.932 for every graph and varies by less than half a percentage point. Second, removing either View-L or View-S causes a substantial performance drop of over 10% AUC in all cases. This confirms that the primary driver of TrustWI’s success is its advanced enhancement and fusion components, not the specific initial graph heuristic.

d) Neighbor Threshold and Similarity Metrics: We analyzed the sensitivity ofour structural augmentation by evaluating two key choices: the neighbor threshold c and the similarity metric, with results presented in Table IX. The analysis confirms our design choices. For the neighbor threshold, fixed values present a poor trade-off: a small c $( \mathrm { e } . \mathrm { g } . , c = 5 )$ is too restrictive and omits many true edges, yielding a low AUC of 91.2%, whereas a large $c \left( \mathrm { e . g . , } c = 2 0 \right)$ injects excessive structural noise (a 24.6% false edge rate). Our adaptive method strikes the optimal balance, achieving the highest AUC (93.7%) while maintaining a low false edge rate. Similarly, our chosen cosine similarity proves superior, achieving a better balance of structural repair and final classification performance than the alternatives.

7) Efficiency Analysis: Our framework is designed to be highly scalable, maintaining a time complexity that is linear with respect to the size of the graph. The most intensive step is the long-range propagation in View-L, which operates in $O ( d T \cdot | { \mathcal { E } } | )$ . All other view generation and evidence-learning steps are linear in the number of nodes, resulting in a total time complexity of $\mathcal { O } ( d T \cdot | \mathcal { E } | + d K \cdot | \mathcal { V } | )$ . Beyond complexity, we profile practical efficiency on our platform. The GPU inference latency is 0.1479 s per test node with a peak GPU memory usage of 8.62 MB. The throughput is about 2866 nodes/s, and the model has only 0.059 M parameters.

## V. CONCLUSION

This work addresses the core challenge of EMTD under weak information characterized by broken structures and incomplete features. We proposed TrustWI, a novel uncertaintyaware multi-view learning framework that achieves trustworthy detection under these adverse conditions. Our framework leverages long-range propagation to enrich node features and a post-propagation strategy for robust structural augmentation. By integrating these views through an uncertainty-aware fusion mechanism, yielding high accuracy and reliable predictions. Experiments confirm clear gains over prior work, especially when information sparsity is severe.

Future Work: Despite these advantages, several directions remain for future exploration. First, it is important to further strengthen TrustWI against strong targeted graph attacks and to study defenses. Second, the pseudo-view design is lightweight but may overlook richer structural or temporal cues. We plan to model cross-view dependencies more expressively, for example with graph attention or co-training strategies.

## REFERENCES

[1] M. Zhong, T. Zhong, Y. Wang, K. Chen, and F. Zhou, “Noise resistant encrypted malicious traffic detection through kernel-enhanced contrastive view alignment,” IEEE/ACM Trans. Netw., vol. 34, pp. 1511–1523, 2026.

[2] Y. Mirsky, T. Doitshman, Y. Elovici, and A. Shabtai, “Kitsune: An ensemble of autoencoders for online network intrusion detection,” in Proc. Annu. Netw. Distrib. System Secur. Symp., 2018, pp. 1–15.

[3] N. Xi et al., “GNNDroid: Graph-learning based malware detection for android apps with native code,” IEEE Trans. Dependable Secure Comput., vol. 22, no. 2, pp. 1460–1476, Mar./Apr. 2025.

[4] Y. Liu, K. Ding, J. Wang, V. Lee, H. Liu, and S. Pan, “Learning strong graph neural networks with weak information,” in Proc. ACM SIGKDD Conf. Knowl. Discov. Data Mining, 2023, pp. 1559–1571.

[5] M. Zhong, M. Lin, C. Zhang, and Z. Xu, “A survey on graph neural networks for intrusion detection systems: Methods, trends and challenges,” Comput. Secur., vol. 141, 2024, Art no. 103821.

[6] W. Li, X.-Y. Zhang, H. Bao, H. Shi, and Q. Wang, “ProGraph: Robust network traffic identification with graph propagation,” IEEE/ACM Trans. Netw., vol. 31, no. 3, pp. 1385–1399, Jun. 2023.

[7] S. T. K. Jan et al., “Throwing darts in the dark? Detecting bots with limited data using neural data augmentation,” in Proc. IEEE Symp. Secur. Privacy, 2020, pp. 1190–1206.

[8] Y. Qing et al., “Low-quality training data only? A robust framework for detecting encrypted malicious network traffic,” in Proc. Annu. Netw. Distrib. System Secur. Symp., 2024, pp. 81–95.

[9] X. Jiang, Z. Qin, J. Xu, and X. Ao, “Incomplete graph learning via attributestructure decoupled variational auto-encoder,” in Proc.ACMInt. Conf. Web Search Data Mining, 2024, pp. 304–312.

[10] D. Chen, Y. Lin, W. Li, P. Li, J. Zhou, and X. Sun, “Measuring and relieving the over-smoothing problem for graph neural networks from the topological view,” in Proc. AAAI Conf. Artif. Intell., 2020, pp. 3438–445.

[11] Z. Han, C. Zhang, H. Fu, and J. T. Zhou, “Trusted multi-view classification with dynamic evidential fusion,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 45, no. 2, pp. 2551–2566, Feb. 2023.

[12] M. Sensoy, L. Kaplan, and M. Kandemir, “Evidential deep learning to quantify classification uncertainty,” in Proc. Adv. Neural Inf. Process. Syst., 2018, pp. 3183–3193.

[13] Z. Fu et al., “Encrypted malware traffic detection via graph-based network analysis,” in Proc. Int. Symp. Res. Attacks Intrusions Defenses, 2022, pp. 495–509.

[14] X. Han et al., “ContraMTD: An unsupervised malicious network traffic detection method based on contrastive learning,” in Proc. Int. World Wide Web Conf., 2024, pp. 1680–1689.

[15] J. Yang, Z. Yue, and Y. Yuan, “Deep probabilistic graphical modeling for robust multivariate time series anomaly detection with missing data,” Rel. Eng. System Saf., vol. 238, 2023, Art no. 109410.

[16] M. Dzaferagic, N. Marchetti, and I. Macaluso, “Fault detection and classification in industrial IoT in case of missing sensor data,” IEEE Internet Things J., vol. 9, no. 11, pp. 8892–8900, Jun. 2022.

[17] B. Qiang, Y. Zhou, H. Xu, J. Shi, J. Lin, and Y. Gao, “MI-GNN: Multiinteraction GNN for various weak information learning on graphs,” in Proc. Int. Joint Conf. Neural Netw., 2024, pp. 1–9.

[18] R. Wang, J. Yan, and X. Yang, “Unsupervised learning of graph matching with mixture ofmodes via discrepancy minimization,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 45, no. 8, pp. 10500–10518, Aug. 2023.

[19] Z. Jiang, H. Rahmani, P. Angelov, S. Black, and B. M. Williams, “Graph-context attention networks for size-varied deep graph matching,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., 2022, pp. 2333–2342.

[20] F. Wang, N. Xue, J.-G. Yu, and G.-S. Xia, “Zero-assignment constraint for graph matching with outliers,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., 2020, pp. 3030–3039.

[21] Y. Lin, M. Yang, J. Yu, P. Hu, C. Zhang, and X. Peng, “Graph matching with bi-level noisy correspondence,” in Proc. IEEE/CVF Int. Conf. Comput. Vis., 2023, pp. 23305–23314.

[22] X. Yan, S. Hu, Y. Mao, Y. Ye, and H. Yu, “Deep multi-view learning methods: A review,” Neurocomputing, vol. 448, pp. 106–129, 2021.

[23] G. Andrew, R. Arora, J. Bilmes, and K. Livescu, “Deep canonical correlation analysis,” in Proc. Int. Conf. Mach. Learn., 2013, pp. 1247–1255.

[24] K. Hassani and A. H. Khasahmadi, “Contrastive multi-view representation learning on graphs,” in Proc. Int. Conf. Mach. Learn., 2020, pp. 4116–4126.

[25] E. Pan and Z. Kang, “Multi-view contrastive graph clustering,” in Proc. Adv. Neural Inf. Process. Syst., 2021, pp. 2148–2159.

[26] X. Han, S. Liu, J. Liu, B. Jiang, Z. Lu, and B. Liu, “ECNet: Robust malicious network traffic detection with multi-view feature and confidence mechanism,” IEEE Trans. Inf. Forensics Secur., vol. 19, pp. 6871–6885, 2024.

[27] Y. Geng, Z. Han, C. Zhang, and Q. Hu, “Uncertainty-aware multiview representation learning,” in Proc. AAAI Conf. Artif. Intell., 2021, pp. 7545–7553.

[28] W. Tai, T. Zhong, G. Trajcevski, and F. Zhou, “Redundancy undermines the trustworthiness of self-interpretable GNNs,” in Proc. Int. Conf. Mach. Learn., 2025, vol. 267, pp. 58169–58188.

[29] J. T. Springenberg, A. Klein, S. Falkner, and F. Hutter, “Bayesian optimization with robust Bayesian neural networks,” in Proc. Adv. Neural Inf. Process. Syst., 2016, pp. 4141–4149.

[30] Y. Gal and Z. Ghahramani, “Dropout as a Bayesian approximation: Representing model uncertainty in deep learning,” in Proc. Int. Conf. Mach. Learn., 2016, pp. 1050–1059.

[31] B. Lakshminarayanan, A. Pritzel, and C. Blundell, “Simple and scalable predictive uncertainty estimation using deep ensembles,” in Proc. Adv. Neural Inf. Process. Syst., 2017, pp. 6405–6416.

[32] B. Charpentier, D. Zügner, and S. Günnemann, “Posterior network: Uncertainty estimation without OOD samples via density-based pseudo-counts,” in Proc. Adv. Neural Inf. Process. Syst., 2020, pp. 1356–1367.

[33] T. N. Kipf and M. Welling, “Semi-supervised classification with graph convolutional networks,” in Proc. Int. Conf. Learn. Representations, 2017, pp. 1–14.

[34] J. Klicpera, A. Bojchevski, and S. Günnemann, “Combining neural networks with personalized pagerank for classification on graphs,” in Proc. Int. Conf. Learn. Representations, 2019, pp. 8–14.

[35] A. Jøsang, Subjective Logic. Cham, Switzerland: Springer, 2016.

[36] J. Lu, Z. Wu, Z. Chen, Z. Cai, and S. Wang, “Towards multi-view consistent graph diffusion,” in Proc. ACM Int. Conf. Multimedia, 2024, pp. 186–195.

[37] N. Moustafa, “A new distributed architecture for evaluating AI-based security systems at the edge: Network TON\_IoT datasets,” Sustain. Cities Soc., vol. 72, 2021, Art no. 102994.

[38] M. MontazeriShatoori, L. Davidson, G. Kaur, and A. H. Lashkari, “Detection of DoH tunnels using time-series classification of encrypted traffic,” in Proc. IEEE Int. Symp. Dependable Autonomic Secure Comput., 2020, pp. 63–70.

[39] I. Sharafaldin, A. H. H. Lashkari, and A. A. Ghorbani, “Toward generating a new intrusion detection dataset and intrusion traffic characterization,” in Proc. Int. Conf. Inf. Syst. Secur. Privacy, 2018, pp. 108–116.

[40] P. Veliˇckovi´c, G. Cucurull, A. Casanova, A. Romero, P. Lio, and Y. Bengio, “Graph attention networks,” in Proc. Int. Conf. Learn. Representations, 2018, pp. 1–12.

[41] J. Yang, X. Jiang, Y. Lei, W. Liang, Z. Ma, and S. Li, “MTSecurity: Privacy-preserving malicious traffic classification using graph neural network and transformer,” IEEE Trans. Netw. Service Manag., vol. 21, no. 3, pp. 3583–3597, Jun. 2024.

[42] W. Jin, Y. Ma, X. Liu, X. Tang, S. Wang, and J. Tang, “Graph structure learning for robust graph neural networks,” in Proc. ACM SIGKDD Conf. Knowl. Discov. Data Mining, 2020, pp. 66–74.

[43] J. Zhao et al., “ReTrial: Robust encrypted malicious traffic detection via discriminative relation incorporation and misleading relation correction,” IEEE Trans. Inf. Forensics Secur., vol. 20, pp. 677–692, 2025.

[44] I. Loshchilov and F. Hutter, “Fixing weight decay regularization in Adam,” 2017, arXiv:1711.05101 .
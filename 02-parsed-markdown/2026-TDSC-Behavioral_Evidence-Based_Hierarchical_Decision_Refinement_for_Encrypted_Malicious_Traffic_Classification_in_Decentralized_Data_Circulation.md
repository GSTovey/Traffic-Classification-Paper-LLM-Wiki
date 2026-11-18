IEEE TRANSACTIONS ON DEPENDABLE AND SECURE COMPUTING, VOL. XX, NO. X, X XXXX

# Behavioral Evidence-Based Hierarchical Decision Refinement for Encrypted Malicious Traffic Classification in Decentralized Data Circulation

Mengyu Wang, Chengxiang Si, Zijian Zhang, Senior Member, IEEE, Yi Zhao, Member, IEEE, Peishuai Sun, Weixuan Mao, Wei Liang

Abstract—Ubiquitous encryption protects privacy in decentralized data circulation but also obscures malicious behavior, leaving distributed enterprise nodes largely dependent on flowlevel metadata and statistical context. Existing flat classifiers place benign traffic and all malicious subtypes in a single label space, although evidence sufficient for malicious screening may still be inadequate for fine-grained attribution. To address this mismatch, we propose THEMIS, a payload-free hierarchical framework built on a unified behavior-oriented representation and coordinated two-stage inference. The normalized uncertainty entropy (NUE) feature family captures directional imbalance, temporal irregularity, statistical fluctuation, and interaction disorder from observable flow statistics. Stage-I filters malicious candidates from benign-dominated traffic, while Stage-II performs conditional subtype attribution using pseudo-label self-training and confusion-triggered local experts. A multi-criteria release rule further combines confidence, normalized posterior entropy, and top-two margin, producing a subtype label only when the refined posterior is sufficiently concentrated and separated from competing classes. Experiments on five public datasets and the enterprise-oriented BAI-Net26 dataset achieve Weighted-F1 scores of at least 0.9974 across all datasets and a Macro-F1 of 0.9873 on BAI-Net26, demonstrating the effectiveness of combining behavioral representation, staged inference, local refinement, and selective subtype release.

Index Terms—encrypted malicious traffic, hierarchical classification, flow-based analysis, semi-supervised learning

## I. INTRODUCTION

Malicious encrypted traffic has become a persistent threat to privacy-preserving data circulation across distributed enterprise and cross-institutional networks. Although encryption protects data confidentiality, adversaries increasingly use protocolcompliant encrypted connections to conceal command-andcontrol (C2), propagation, and data-exfiltration activities [1], [2], [3]. Recent threats such as the BRICKSTORM backdoor further demonstrate that malicious communications can be layered over HTTPS, WebSockets, nested TLS, and DNSover-HTTPS [4]. In the decentralized data-circulation setting considered in this work, traffic is observed at geographically or administratively distributed gateways, while payloads cannot be centrally inspected or shared because of privacy and datasovereignty constraints. Malicious intent must therefore be inferred from flow-level behavior, endpoint interactions, timing characteristics, and statistical context.

![](images/169076187b1dd213fec8b5802a9c102843efb21c7cb407838ed140ddd8c541b0.jpg)  
Fig. 1: The raincloud visualization on CIC-UNSW-NB15 reveals substantial overlap not only between benign and malicious flows, but also among malicious categories in representative statistical features, as highlighted by the red boxes.

Existing studies analyze encrypted traffic through metadata, side-channel statistics, reconstructed attributes, temporal patterns, communication structures, and learned representations [5], [6], [7]. Graph-based, interaction-aware, multimodal, contrastive, masked, and sequence-based models further improve encrypted-flow representation and classification [8], [9], [10], [11], [12], [13]. Nevertheless, most methods still place benign traffic and all malicious subtypes within a single classification space. This flat formulation overlooks an important distinction: evidence sufficient to identify a flow as a malicious candidate may still be insufficient to determine its precise attack subtype.

The difficulty is compounded by three characteristics of encrypted gateway traffic. (1) Legitimate synchronization, backup, and cross-domain exchange may resemble malicious behaviors under limited payload and contextual visibility [14], [15]. (2) Benign-dominated traffic makes fine-grained attribution for every connection inefficient. (3) Behavioral evidence such as directional imbalance and irregular timing is often weak and overlapping, and sparse or imbalanced labels further blur the boundaries between adjacent attack subtypes [16], [17], [18], as illustrated in Fig. 1. The central technical problem is therefore to construct discriminative behavioral evidence and coordinate coarse screening with fine-grained attribution according to their different evidence requirements.

To address this problem, we propose THEMIS, a hierarchical framework for payload-free encrypted malicious traffic analysis. Its main methodological contribution is a coordinated twostage inference process built on a unified behavior-oriented representation: THEMIS constructs the normalized uncertainty entropy (NUE) feature family as a multidimensional representation of behavioral disorder, heterogeneity, and variation from observable flow and contextual statistics, uses Stage-I to screen malicious candidates from benign-dominated traffic, and performs conditional subtype attribution in Stage-II. Within Stage-II, semi-supervised learning and a validationguided mixture-of-experts (MoE) mechanism refine subtype predictions, after which a multi-criteria release rule determines whether a fine-grained label should be emitted.

We evaluate THEMIS across five public datasets and one realworld enterprise dataset BAI-Net26, collected and reconstructed in 2026<sup>1</sup>. Extensive empirical results confirm that THEMIS maintains robust performance and manageable computational overhead under rigorous encrypted traffic evaluation protocols.

The main contributions of this paper are summarized as follows:

• We formulate encrypted malicious traffic attribution in decentralized data circulation as a hierarchical staged decision problem and propose THEMIS, a payload-free framework that coordinates Stage-I coarse screening with Stage-II fine-grained attribution, integrating semisupervised subtype learning, confusion-triggered local experts, and multi-criteria release control.

• We design the NUE feature family to represent encrypted flows, effectively capturing inherent imbalance, irregularity, fluctuation, and interaction disorder from observable statistics without relying on payload inspection, thereby aligning with the privacy preservation requirements of distributed multi-party systems.

• We conduct extensive experiments on five public datasets and the enterprise-oriented BAI-Net26 dataset, evaluating end-to-end performance, group-aware generalization, routing behavior, and inference overhead.

The remainder of this paper is organized as follows. Section II reviews related work. Section III formalizes the task and objectives. Section IV details the THEMIS architecture. Section V reports the evaluation. Section VI discusses findings and limitations. Section VII concludes the paper.

## II. RELATED WORK

This section reviews encrypted traffic observability and representation learning, fine-grained malicious traffic attribution, and deployment-oriented decision control. It positions THEMIS as a hierarchical decision framework that complements stronger traffic encoders rather than replacing them.

## A. Encrypted Traffic Observability and Representation

Early studies showed that encrypted malicious traffic can be detected without payload decryption. Anderson et al. [5] and Anderson and McGrew [14] demonstrated the value of TLS metadata, side-channel statistics, and contextual observables. Wang and Thing [6] further showed that carefully designed flow statistics retain strong discriminatory power, while recent feature-engineering work restores traffic-side attributes under payload-free visibility [7]. Surveys and SoK studies summarize the shift from metadata-driven analysis to richer encrypted traffic modeling under modern protocols [19], [20].

Learning-based representation has improved encrypted traffic analysis under weak observability, noisy labels, and distribution shifts. Pre-trained encoders and neural sequence models learn packet- or flow-level representations [12], [21], [22]. Masked modeling and contrastive learning improve robustness when labels are limited or heterogeneous [13], [11]. Graph and interaction-based methods exploit communication structures for encrypted traffic characterization [8], [9]. Other studies explore byte-segment modeling, multimodal fusion, and security oriented learning under limited supervision [10], [23], while robust and semi-supervised methods address distribution shifts and imperfect labels [17], [24]. These methods strengthen feature learning, but stronger representations alone do not determine how coarse maliciousness evidence should be routed, refined, and converted into sufficiently supported subtype decisions. THEMIS addresses this decision-level gap by combining NUE-enhanced representation with staged routing and multicriteria subtype release.

## B. Fine-grained Malicious Traffic Attribution

Fine-grained attribution is harder than benign–malicious detection because adjacent attack stages, variants, and tool families often share encrypted-flow patterns. Subtype labels are also often sparse, delayed, imbalanced, and collected from heterogeneous sources. Strong encoders and graphaware models improve subtype prediction by exploiting richer encrypted-flow structures [9], [10]. Security-oriented and multimodal learning methods further strengthen classification under limited or heterogeneous supervision [17], [23]. However, many approaches still optimize subtype prediction within a single end-to-end label space, making it difficult to separate clearly benign traffic from malicious candidates with wellseparated or ambiguous subtype evidence.

Hierarchical and local expert classifiers are useful because encrypted malicious traffic often contains repeated confusion among adjacent stages or behaviorally similar families. THEMIS follows this view by separating Stage-I benign– malicious routing from Stage-II subtype attribution. It further uses validation-identified local experts as a refinement mechanism, allowing the global classifier to handle broad subtype separation while local experts focus on narrower confused regions.

## C. Deployment-oriented Monitoring and Decision Control

Practical encrypted traffic systems must operate under throughput, latency, and false-alarm constraints. Recent systems emphasize scalable monitoring and high-speed encrypted traffic analysis [16], while deployment-aware studies examine efficient feature extraction under constrained observability [15]. These efforts show that encrypted traffic analysis should be evaluated not only by accuracy but also by operational cost and decision usability. Yet efficiency alone does not determine when the available evidence is sufficient for fine-grained subtype release.

THEMIS uses a staged decision process in which Stage-I reduces the candidate space, Stage-II performs semi-supervised subtype attribution, and selective local experts refine recurrent confusion regions. Its contribution lies in coordinating representation, screening, attribution, and confidence-, entropy-, and margin-based subtype release within a unified framework for encrypted traffic analysis.

## III. THREAT MODEL AND PROBLEM FORMULATION

This section formalizes the problem of encrypted malicious traffic analysis under network-level observability. Because payloads and plaintext application semantics are opaque to the defender, the system must infer risk strictly from trafficside evidence. Crucially, the system must determine not only whether a flow is malicious, but also whether the underlying evidence is sufficiently concentrated and discriminative to support fine-grained malicious subtype attribution.

## A. Threat Model

We assume a distributed enterprise or campus network monitored by edge gateways, branch gateways, core switches, mirror ports, or dedicated probes. The monitoring infrastructure captures flow-level records for north–south traffic and, when available, part of east–west communication. Observable metadata includes the 5-tuple, timestamps, directions, flow duration, packet and byte counts, transmission rates, packet-length statistics, and inter-arrival times. We do not assume access to host telemetry, endpoint logs, decrypted DNS resolutions, plaintext application contents, or payload inspection.

Adversary and capabilities. Adversaries establish encrypted, protocol-compliant communication channels without breaking the underlying cryptography. Malicious behaviors may include reconnaissance probing, persistent command-and-control (C2)

callbacks, lateral movement, or data exfiltration. To resemble routine enterprise activity, adversaries may use low-and-slow transmission, common ports, mainstream protocols, legitimate or compromised infrastructure, and rate or volume shaping. The adversary cannot control the monitoring infrastructure or manipulate the evaluation partitions.

Defender goals and constraints. Defenders require decisions that remain viable under high-volume gateway traffic. A practical system should suppress benign background interference, preserve malicious-candidate recall, and release finegrained subtype attributions only when the supporting evidence is sufficiently concentrated and separated from competing subtypes. Thus, the system should distinguish well-supported subtype decisions from cases in which several malicious categories remain behaviorally ambiguous.

## B. Problem Definition

Encrypted malicious traffic analysis motivates a staged decision architecture. A network flow may exhibit sufficient anomalous behavior to be separated from benign traffic, yet lack the requisite evidence for fine-grained subtype attribution. Conversely, a weakly suspicious flow should not be forced into a fine-grained classification simply because the model is trained over a closed, fixed label set.

Input and representation. Let x denote an intercepted encrypted flow. Let e(x) be the NUE feature family constructed from observable traffic evidence, and let f(x) be the final representation combining basic flow statistics with e(x). The feature family describes directional imbalance, temporal irregularity, statistical fluctuation, and interaction-structure disorder. While intrinsic elements are computed directly from the flow metadata, context-dependent statistics are fitted on the training partition to prevent data leakage, serving only as query references during validation and testing.

Output space. Under the deployment policy studied in this paper, the final hard output is defined as:

$$
\hat {y} (x) \in \{\text {Benign}, 1, \dots , K \},\tag{1}
$$

where Benign denotes the benign-side decision rendered by the model, and $1 , \ldots , K$ denote the known malicious subtypes. The hard output is governed by the staged inference policy: samples not forwarded by Stage-I, or samples whose Stage-II subtype evidence does not satisfy the release condition, are assigned to the benign side. If a ground-truth malicious sample is suppressed in this manner, it is penalized as a false negative for its respective malicious class during end-to-end evaluation, reflecting real-world operational costs.

Subtype posterior and uncertainty. For candidate flows forwarded to Stage-II attribution, let

$$
\mathbf {p} (x) = \bigl (p _ {1} (x), \dots , p _ {K} (x) \bigr), \quad \sum_ {k = 1} ^ {K} p _ {k} (x) = 1,\tag{2}
$$

denote the posterior probability distribution over the known malicious subtypes. We define the maximum subtype confidence as:

$$
m (x) = \max _ {1 \leq k \leq K} p _ {k} (x),\tag{3}
$$

TABLE I: Main notation used in THEMIS.

<table><tr><td>Symbol</td><td>Meaning</td></tr><tr><td> $x$ </td><td>Encrypted flow.</td></tr><tr><td> $\mathbf{b}(x)$ </td><td>Basic observable features.</td></tr><tr><td> $\mathbf{e}(x)$ </td><td>NUE behavioral features.</td></tr><tr><td> $\mathbf{f}(x)$ </td><td>Combined feature representation.</td></tr><tr><td> $K$ </td><td>Number of known malicious subtypes.</td></tr><tr><td> $g(x)$ </td><td>Stage-I maliciousness score.</td></tr><tr><td> $\tau_g$ </td><td>Stage-I routing threshold.</td></tr><tr><td> $a(x)$ </td><td>Stage-I routing decision.</td></tr><tr><td> $\mathbf{p}(x)$ </td><td>Stage-II subtype posterior.</td></tr><tr><td> $m(x), h(x), \Delta(x)$ </td><td>Confidence, normalized entropy, and top-two margin.</td></tr><tr><td> $\tau_p, \tau_m, \tau_h$ </td><td>Pseudo-label acceptance thresholds.</td></tr><tr><td> $G$ </td><td>Confusion region of malicious subtypes.</td></tr><tr><td> $E_G$ </td><td>Local expert for region  $G$ .</td></tr><tr><td> $T_G(x)$ </td><td>Trigger for expert  $E_G$ .</td></tr><tr><td> $s_G, \mu_G$ </td><td>Regional mass and gap thresholds.</td></tr><tr><td> $\tilde{\mathbf{p}}(x)$ </td><td>Refined Stage-II posterior.</td></tr><tr><td> $k(x)$ </td><td>Most likely refined subtype.</td></tr><tr><td> $\tau_c, \tau_e, \tau_\Delta$ </td><td>Subtype-release thresholds.</td></tr><tr><td> $z(x)$ </td><td>Subtype-release decision.</td></tr><tr><td> $\hat{y}(x)$ </td><td>Final output in {Benign, 1, ..., K}.</td></tr></table>

and quantify predictive ambiguity using normalized posterior entropy and the top-two confidence margin, respectively defined as:

$$
h (x) = - \sum_ {k = 1} ^ {K} p _ {k} (x) \log p _ {k} (x) / \log (K),\tag{4}
$$

and

$$
\Delta (x) = p _ {k _ {(1)} (x)} (x) - p _ {k _ {(2)} (x)} (x),\tag{5}
$$

where $k _ { ( 1 ) } ( x )$ and $k _ { ( 2 ) } ( x )$ index the largest and second-largest posterior entries. Larger m(x) and $\Delta ( x )$ indicate stronger subtype commitment, whereas larger h(x) indicates heightened attribution ambiguity. We emphasize that the posterior entropy $h ( x )$ is derived exclusively at decision time from the model’s output space, remaining structurally distinct from the NUE feature family e(x).

Learning objective and deployment constraints. The objective is to learn a staged mapping from x to yˆ(x). Stage-I balances benign-flow suppression against malicious-candidate recall, while Stage-II performs subtype attribution and releases a label only when the refined posterior satisfies the confidence, entropy, and margin criteria. Local experts may refine the posterior, but all routing rules and thresholds are fixed before testing. The main notation is summarized in Table I.

## C. Design Goals

The above formulation shows that encrypted malicious traffic attribution demands a hierarchical decision architecture rather than a conventional flat classifier. A deployable system must address three coupled requirements: separating weak encryptedflow evidence, reducing benign-dominated background interference, and controlling fine-grained subtype release when the posterior remains ambiguous. These requirements lead to the following design goals.

G1: The representation mechanism must expose encryptedflow irregularities that are invisible without payload access. Accordingly, the NUE feature vector e(x) captures behavioral uncertainty from traffic imbalance, temporal irregularity, statistical fluctuation, and interaction disorder.

G2: The decision process must support efficient benignside screening before selective fine-grained attribution. It should reduce benign background interference while preserving malicious-candidate recall.

TABLE II: Organization of the Normalized Uncertainty Entropy feature family.

<table><tr><td>Subcategory</td><td>Description</td></tr><tr><td colspan="2">Interaction Scale</td></tr><tr><td>Host flow volume</td><td>Source-host flow count, indicating activity scale.</td></tr><tr><td>Host popularity</td><td>Flows and distinct sources reaching a destination host.</td></tr><tr><td>Port popularity</td><td>Flows and distinct sources reaching a destination port.</td></tr><tr><td>Packet efficiency</td><td>Bytes per packet, indicating payload density.</td></tr><tr><td>Pair traffic ratio</td><td>Relative scale of source, destination, and pair traffic.</td></tr><tr><td colspan="2">Diversity and Expansion</td></tr><tr><td>Port diversity</td><td>Number of destination ports contacted by a source host.</td></tr><tr><td>Host diversity</td><td>Number of destination hosts contacted by a source host.</td></tr><tr><td>Port span</td><td>Numerical span of contacted destination ports.</td></tr><tr><td>Normalized port span</td><td>Ratios among port range, unique ports, and flows.</td></tr><tr><td>Normalized host diversity</td><td>Ratios of unique hosts to total flows.</td></tr><tr><td colspan="2">Direction and Port Semantics</td></tr><tr><td>Flow direction</td><td>Internal, outbound, or inbound communication.</td></tr><tr><td>Private IP status</td><td>Whether an endpoint uses private address space.</td></tr><tr><td>Port semantics</td><td>Service categories such as Web, SSH, DB, DNS, and RDP.</td></tr><tr><td>Subnet relation</td><td>Whether endpoints lie in the same or nearby subnet.</td></tr><tr><td colspan="2">Temporal and Imbalance Statistics</td></tr><tr><td>Minute fluctuation</td><td>Minute-level variation of flow and port statistics.</td></tr><tr><td>Hour fluctuation</td><td>Hour-level variation of flow and port distributions.</td></tr><tr><td>Burst intensity</td><td>Cross-window ratios indicating burst concentration.</td></tr><tr><td>Pair stability</td><td>Repetition of a source-destination pair across time.</td></tr><tr><td>Packet imbalance</td><td>Forward/backward packet totals and imbalance.</td></tr><tr><td>Byte imbalance</td><td>Forward/backward byte totals and imbalance.</td></tr><tr><td>Mean packet length</td><td>Mean forward/backward packet size.</td></tr><tr><td>Packet dispersion</td><td>Variation of packet sizes within a flow.</td></tr><tr><td>IAT dispersion</td><td>Variation of packet inter-arrival times.</td></tr><tr><td>Log compression</td><td>log1p transform for long-tailed statistics.</td></tr></table>

G3: The attribution component must remain effective when subtype labels are sparse, delayed, imbalanced, or aggregated from heterogeneous sources. It should learn subtype boundaries from limited labeled data, incorporate supplementary supervision when available, and release fine-grained predictions only when the posterior evidence is sufficiently concentrated and discriminative.

These goals correspond to the core components of THEMIS: NUE-enhanced representation, Stage-I coarse screening, and Stage-II fine-grained attribution with semi-supervised learning, local expert refinement, and multi-criteria release control.

## IV. ARCHITECTURE OF THE THEMIS FRAMEWORK

This section presents the architecture of THEMIS. It first constructs a unified behavior-oriented representation, then uses Stage-I for malicious-candidate screening and Stage-II for semisupervised subtype attribution and selective MoE refinement. Their outputs are combined by the final release policy.

## A. Overview of THEMIS

The architecture is driven by the three design goals outlined in Section III. Because encrypted traffic obscures payload semantics, THEMIS derives behavioral evidence from flow statistics and interaction contexts. By separating benign– malicious screening from subtype attribution while coupling their decisions at final release, the framework assigns coarse screening and fine-grained attribution to different inference stages. As illustrated in Fig. 2, THEMIS contains three integrated components:

![](images/25680286973467a374e26b78cdbe4f5a43d80f23c25049855c43c221849bd00e.jpg)  
Fig. 2: Pipeline of THEMIS. Encrypted flows are transformed into a unified behavior-oriented representation, screened by Stage-I, and then processed by Stage-II through global subtype attribution, local-expert refinement, and multi-criteria subtype release.

• Unified preprocessing and NUE-enhanced representation: Raw encrypted-flow records are mapped into a unified feature space and augmented with $\mathbf { e } ( x )$ , which organizes interaction scale and pair relation, diversity and expansion, direction and port semantics, and temporal and imbalance statistics from observable flow and contextual evidence.

• Stage-I (i.e., coarse screening): A lightweight binary routing model reduces benign-side traffic and forwards malicious candidates to Stage-II according to a validation-determined operating point.

• Stage-II (i.e., fine-grained subtype attribution): Operating on the forwarded candidates, Stage-II estimates the conditional subtype posterior, supplements limited supervision through pseudo-label self-training, and selectively refines recurrent confusion regions through MoE modules. The refined evidence is then evaluated by the subtype-release rule before a finegrained label is returned.

## B. Data Preprocessing and NUE-enhanced Representation

NUE construction. Let r(x) collect the observable quantities underlying the descriptors in Table II, which are organized into four complementary groups: interaction scale and pair relation, diversity and expansion, direction and port semantics, and temporal and imbalance statistics. The normalized uncertainty entropy (NUE) feature family $\mathbf { e } ( x )$ is constructed as

$$
\mathbf {e} (x) = \Psi_ {\mathrm{tr}} (\mathbf {r} (x)),\tag{6}
$$

where $\Psi _ { \mathrm { t r } } ( \cdot )$ constructs the listed descriptors and aligns their scales using parameters fitted only on the training partition. Its principal numerical operations are

$$
L (c) = \log (1 + c),\tag{7a}
$$

$$
Q (v _ {1}, v _ {2}) = \frac {v _ {1}}{v _ {2} + \epsilon},\tag{7b}
$$

$$
I (v _ {1}, v _ {2}) = \frac {| v _ {1} - v _ {2} |}{v _ {1} + v _ {2} + \epsilon},\tag{7c}
$$

$$
V (\mathbf {v}) = \frac {\mathrm{std} (\mathbf {v})}{\mathrm{mean} (\mathbf {v}) + \epsilon}.\tag{7d}
$$

Here, $c \geq 0$ is a count-valued observation. In $Q ( \cdot , \cdot )$ and $I ( \cdot , \cdot ) , v _ { 1 } , v _ { 2 } \geq 0$ are the paired measurements specified by the corresponding descriptor; in $V ( \cdot ) , \mathbf { v } = ( v _ { 1 } , \ldots , v _ { n } )$ is a finite nonnegative sequence such as packet sizes, inter-arrival times, or window-level statistics. The natural logarithm is used, mean(·) and std(·) are population statistics over the available entries, and $\epsilon > 0$ prevents division by zero.

The interaction group applies L(·) to packet, byte, host, and pair counts and uses $Q ( \cdot , \cdot )$ or $I ( \cdot , \cdot )$ for relative pair activity. The diversity group applies count compression and relativescale operations to distinct hosts, ports, services, and expansion statistics. The directional group uses paired ratios and imbalance measures for forward–backward quantities together with fixed direction, address-relation, and port-semantic encodings.

The temporal group applies $V ( \cdot )$ and paired imbalance to interarrival and window-level variations. Numerical coordinates are then aligned by the train-fitted transformation. Thus, normalized refers to the combined use of dimensionless ratios, imbalance measures, logarithmic compression, categorical encoding, and training-fitted scale alignment.

The resulting vector preserves interaction concentration, communication diversity, directional asymmetry, temporal fluctuation, and statistical dispersion. The term uncertainty entropy refers to this multidimensional characterization of behavioral disorder and heterogeneity rather than to a single entropy scalar.

The final flow representation is

$$
\mathbf {f} (x) = \Phi (\mathbf {b} (x), \mathbf {e} (x)),\tag{8}
$$

where ${ \bf b } ( x )$ denotes the standardized basic flow descriptors and $\Phi ( \cdot )$ combines the basic and NUE-enhanced representations. The same representation is used by Stage-I for maliciouscandidate screening and Stage-II for conditional subtype attribution.

Although the individual counts, ratios, diversity measures, categorical indicators, and dispersion statistics are established traffic descriptors, NUE organizes and normalizes them into a unified payload-free behavioral profile shared by both inference stages. The contribution of its four feature groups is further examined through group-wise ablation in Section V.

## C. Stage-I: Coarse Screening

Given f(x), the binary Stage-I model outputs the modelestimated maliciousness probability

$$
g (x) = P \bigl (y \neq \text { Benign } \mid \mathbf {f} (x) \bigr), \quad g (x) \in [ 0, 1 ],\tag{9}
$$

where $y \in \{ \mathtt { B e n i g n } , 1 , \dotsc , K \}$ denotes the training label. The value $g ( x )$ is used as a routing score rather than as a claim of probability calibration. The validation-selected threshold $\tau _ { g }$ defines the forwarding decision

$$
a (x) = \mathbb {I} \big [ g (x) \geq \tau_ {g} \big ],\tag{10}
$$

where $\mathbb { I } [ \cdot ]$ is the indicator function. A flow with $a ( x ) = 1$ is forwarded to Stage-II, whereas $a ( x ) = 0$ is assigned to the benign side. The selected $\tau _ { g }$ is fixed before testing, and forwarding identifies a candidate for attribution rather than a final malicious subtype.

## D. Stage-II: Fine-Grained Subtype Attribution

Operating on candidates forwarded by Stage-I, Stage-II estimates the conditional posterior over known malicious subtypes and selectively refines recurrent local ambiguities. Its refined evidence is then evaluated by the final subtyperelease rule.

Semi-supervised learning. The global Stage-II model produces the conditional subtype posterior $\mathbf { p } ( x )$ defined in Section III. Pseudo-label self-training accepts an available unlabeled candidate only when

$$
m (x) \geq \tau_ {p}, \quad \Delta (x) \geq \tau_ {m}, \quad h (x) \leq \tau_ {h}.\tag{11}
$$

Here, $\tau _ { p } , \tau _ { m }$ , and $\tau _ { h }$ are the confidence, margin, and entropy thresholds, respectively. Accepted samples receive the label arg $\mathrm { m a x } _ { 1 \le k \le K } p _ { k } ( x )$ and are added with reduced sample weight. The triplet $( \tau _ { p } , \tau _ { m } , \tau _ { h } )$ is selected during model development and fixed within each run; representative active settings were approximately (0.95, 0.10, 0.20). If no sample satisfies the rule, training remains supervised.

Confusion-aware mixture-of-experts (MoE) refinement. The global model covers all malicious subtypes, while the MoE mechanism targets recurrent confusion regions. Each region $G \subseteq \{ 1 , \dots , K \}$ contains at least two subtype labels, and $E _ { G }$ is trained on samples whose labels belong to $G . \mathrm { ~ A ~ }$ candidate trigger $T _ { G }$ is selected on validation data. According to the retained trigger mode, $T _ { G } ( x ) = 1$ when either the topranked class or at least one of the top-two classes belongs to $G ,$ the regional mass $\textstyle \sum _ { k \in G } p _ { k } ( x )$ is at least $s _ { G } ,$ and the gap between the two largest probabilities within G is at most $\mu _ { G } ;$ any retained secondary condition is applied jointly. Candidate regions are drawn from a small predefined set of recurrent confusion patterns and are evaluated only when sufficient training and validation support is available. Only modules whose routed validation samples meet the support requirement and improve Macro-F1 in the corresponding region are retained.

Retained modules $( G , E _ { G } , T _ { G } )$ are ordered by validation improvement, with routed support breaking ties, and this order is fixed for inference. The first module satisfying $T _ { G } ( x ) = 1$ is activated, so at most one expert is used. Let $G ^ { \star }$ denote the selected region. The entries $[ E _ { G ^ { \star } } ( x ) ] _ { k }$ form a normalized local posterior indexed by the original subtype labels $k \in G ^ { \star }$ . The expert redistributes only the posterior mass assigned to $G ^ { \star }$

$$
\widetilde {p} _ {k} (x) = \left\{ \begin{array}{l l} [ E _ {G ^ {\star}} (x) ] _ {k} \sum_ {j \in G ^ {\star}} p _ {j} (x), & k \in G ^ {\star}, \\ p _ {k} (x), & k \notin G ^ {\star}. \end{array} \right.\tag{12}
$$

If no trigger is satisfied, $\widetilde { \mathbf { p } } ( x ) = \mathbf { p } ( x )$ . Because the local posterior sums to one over $G ^ { \star }$ , the update preserves the total posterior mass and leaves all classes outside the selected region unchanged. The refined subtype prediction is

$$
\bar {k} (x) = \arg \max _ {1 \leq k \leq K} \widetilde {p} _ {k} (x).\tag{13}
$$

Algorithm 1 gives the corresponding offline construction procedure.

Multi-criteria subtype release and final inference policy. For a forwarded flow, the confidence, normalized posterior entropy, and top-two margin defined in Section III are recomputed from $\widetilde { \mathbf { p } } ( x )$ and denoted by $\widetilde { m } ( x ) , \widetilde { h } ( x )$ , and $\widetilde { \Delta } ( x )$ . The subtype-release condition is

$$
z (x) = \mathbb {I} \left[ \widetilde {m} (x) \geq \tau_ {c} \wedge \widetilde {h} (x) \leq \tau_ {e} \wedge \widetilde {\Delta} (x) \geq \tau_ {\Delta} \right].\tag{14}
$$

For $K = 1$ , the definitions in Section III give $\widetilde { h } ( x ) = 0$ and $\widetilde { \Delta } ( x ) = 1$ , so the entropy and margin terms are nonrestrictive and the hierarchy reduces naturally to the binary routing outcome. The triplet $\left( \tau _ { c } , \tau _ { e } , \tau _ { \Delta } \right)$ is selected from a fixed validation grid and locked before testing. For notational simplicity, these symbols denote the retained operating values applied to the predicted class $\bar { k } ( x )$ ; when class-specific selection is not used, they denote the common triplet. When all three criteria were active, a representative configuration was approximately (0.70, 0.75, 0.10). The release rule is evaluated only for forwarded flows, and $z ( x ) = 0$ when $a ( x ) = 0$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Construction of selective MoE modules
Require: global Stage-II model; malicious training/validation data; candidate trigger modes, secondary conditions, support requirement, and candidate values of  $s_{G}$  and  $\mu_{G}$ 
Ensure: ordered retained modules ( $G, E_{G}, T_{G}$ )
1: identify recurrent confusion regions from validation predictions
2: initialize an empty module list
3: for each region G do
4: train  $E_{G}$  on training samples with labels in G
5: select  $T_{G}$  over the trigger modes,  $s_{G}, \mu_{G}$ , and secondary conditions
6: if routed validation samples meet the support requirement and  $E_{G}$  improves regional Macro-F1 then
7: append ( $G, E_{G}, T_{G}$ )
8: end if
9: end for
10: order modules by validation improvement, then routed support
11: return the ordered modules
</div>

The final output is

$$
\hat {y} (x) = \left\{ \begin{array}{l l} \bar {k} (x), & a (x) = 1 \land z (x) = 1, \\ \text { Benign }, & \text { otherwise }. \end{array} \right.\tag{15}
$$

The joint dependence on $a ( x )$ and $z ( x )$ couples the two stages at the decision level. This fixed coupling is the feedback mechanism in THEMIS: Stage-I identifies candidates, while Stage-II can confirm or withhold the subtype output according to the refined evidence. It prevents a flow forwarded by Stage-I from being automatically forced into a malicious subtype and does not update either model during inference. Under the current closed output policy, an unreleased flow is assigned to the benign side and, if malicious in the ground truth, remains counted as a false negative in end-to-end evaluation.

Algorithms 1 and 2 summarize the offline MoE construction and online inference procedures, respectively. Context statistics, normalization parameters, routing settings, pseudo-label criteria, retained MoE modules, trigger configurations, module order, and subtype-release parameters remain fixed during test evaluation.

## V. PERFORMANCE EVALUATION

We evaluate THEMIS across five public encrypted malicious traffic datasets and one real-world enterprise dataset. Our evaluation protocol is designed to quantify component-level contributions while rigorously validating the architectural necessity of the staged formulation.

## A. Experimental Settings

Datasets. We utilize five public datasets: CIC-UNSW-NB15 [25], [26], EarlyCrow [27], DAPT2020 [28], ZAPT-

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 Online inference of THEMIS

Require: encrypted-flow record x; trained Stage-I and Stage-II models; ordered retained modules  $(G, E_{G}, T_{G})$ ; retained values of  $\tau_{g}, \tau_{c}, \tau_{e}$ , and  $\tau_{\Delta}$ 

Ensure: final prediction  $\hat{y}(x)$ 

1: construct  $\mathbf{f}(x)$ ; compute  $g(x)$  using Eq. (9) and  $a(x)$  using Eq. (10)

2: if  $a(x) = 0$  then

3: return Benign

4: end if

5: compute  $\mathbf{p}(x)$ ; set  $\widetilde{\mathbf{p}}(x) \leftarrow \mathbf{p}(x)$ 

6: for each retained  $(G, E_{G}, T_{G})$  in fixed order do

7: if  $T_{G}(x) = 1$  when evaluated from  $\mathbf{p}(x)$  then

8:  $G^{\star} \leftarrow G$ 

9: construct  $\widetilde{\mathbf{p}}(x)$  from  $E_{G^{\star}}(x)$  using Eq. (12)

10: break

11: end if

12: end for

13: compute  $\bar{k}(x)$  using Eq. (13)

14: compute  $\widetilde{m}(x), \widetilde{h}(x)$ , and  $\widetilde{\Delta}(x)$  from  $\widetilde{\mathbf{p}}(x)$ 

15: evaluate  $z(x)$  using Eq. (14) with the retained values for  $\bar{k}(x)$ 

16: if  $z(x) = 1$  then

17: return  $\bar{k}(x)$ 

18: else

19: return Benign

20: end if
</div>

2026 $[ 2 9 ] ^ { 2 } .$ , and Unraveled [30].

To evaluate operational viability, we also introduce the real-world enterprise dataset Behavioral Analysis of Intrusion Network 2026 (BAI-Net26). As detailed in Table III, BAI-Net26 contains one benign baseline and 15 fine-grained malicious categories. These span complex behavioral families, including social engineering, downloader chains, information stealing, remote access, exfiltration, covert backdoor activity, and mixed intrusion behaviors. The dataset includes HTTP, HTTPS, FTP, SMTP, and mixed HTTP/HTTPS traffic, with encrypted HTTPS sessions accounting for most malicious samples. Benign traffic is derived from routine enterprise telemetry, whereas malicious traffic is aggregated from honeypot captures, vetted community threat sharing, and controlled red-team replays conducted under strict organizational authorization.

The traffic was reconstructed from Indicator of Compromise (IOC) evidence and malware-analysis reports, replayed under organizational authorization, and captured at the enterprise gateway. All IP addresses are rigorously anonymized, with only statistical traffic features and semantic annotations retained for release. Ultimately, BAI-Net26 is designed to evaluate family-level and behavior-level discrimination under the extreme heterogeneity of deployment-relevant encrypted traffic environments.

Split and model configuration. All experiments use repeated, group-aware 70%/10%/20% splits over 50 random seeds, and all reported mean and standard-deviation values are computed across these runs. Records sharing the same capture source, malware sample, replay session, campaign, source– destination pair, or adjacent capture context are kept in the same partition whenever such metadata are available. Context statistics and model parameters are learned from the training partition, while routing, expert-activation, and release thresholds are selected from fixed candidate sets on the validation partition for each seed and then held fixed during testing.

TABLE III: Traffic categories in the BAI-Net26 open-world dataset.

<table><tr><td>ID</td><td>Shorthand</td><td>Main Behavior</td><td>Macro Type</td><td>Main Protocol</td></tr><tr><td>1</td><td>Benign</td><td>Browsing, cloud sync, office, streaming, social apps</td><td>Normal Traffic</td><td>-</td></tr><tr><td>2</td><td>ClickFix_SocialEng</td><td>ClickFix-style social engineering and malicious delivery</td><td>Social Engineering</td><td>HTTPS</td></tr><tr><td>3</td><td>Dropper_Latroductus</td><td>Dropper chain leading to Latrodectus and downstream payloads</td><td>Downloader Attack</td><td>HTTPS</td></tr><tr><td>4</td><td>FakeSoftware_Lumma</td><td>Fake-software delivery with Lumma credential and wallet theft</td><td>Information Stealer</td><td>HTTPS</td></tr><tr><td>5</td><td>FakeSoftware_LummaRsockstun</td><td>Lumma infection with Rsockstun remote control</td><td>Combination Attack</td><td>HTTP/HTTPS</td></tr><tr><td>6</td><td>FakeSoftware_LummaSecTop</td><td>Lumma infection with SecTop RAT persistence</td><td>Combination Attack</td><td>HTTPS</td></tr><tr><td>7</td><td>FakeSoftware_LummaBackdoor</td><td>Highly covert Lumma-related backdoor implantation</td><td>Covert Backdoor</td><td>HTTP/HTTPS</td></tr><tr><td>8</td><td>FakeSoftware_LummaMixed</td><td>Mixed infection with Lumma and additional malware</td><td>Mixed Attack</td><td>HTTP/HTTPS</td></tr><tr><td>9</td><td>GoogleFake_KoiStealer</td><td>Google-themed Koi stealer delivery and credential theft</td><td>Information Stealer</td><td>HTTP/HTTPS</td></tr><tr><td>10</td><td>macOS_SafariStealer</td><td>Safari data theft targeting macOS systems</td><td>macOS Stealer</td><td>HTTPS</td></tr><tr><td>11</td><td>KeyLogger_MassLogger</td><td>Keystroke logging with SMTP-based exfiltration</td><td>Data Logger</td><td>SMTP</td></tr><tr><td>12</td><td>SocialPage_NetSupportRAT</td><td>Fake update page deploying NetSupport RAT</td><td>Remote Access Trojan</td><td>HTTPS</td></tr><tr><td>13</td><td>ClickFix_NetSupportRAT</td><td>ClickFix-triggered PowerShell execution and RAT deployment</td><td>Remote Access Trojan</td><td>HTTPS</td></tr><tr><td>14</td><td>VIP_SMTPExfil</td><td>Persistent SMTP-based data exfiltration</td><td>Data Exfiltration</td><td>SMTP</td></tr><tr><td>15</td><td>Phishing_XLoader</td><td>Phishing-delivered XLoader form and credential theft</td><td>Form Stealer</td><td>HTTP</td></tr><tr><td>16</td><td>SocialMedia_FakeSoftware</td><td>Social-media delivery of fake software leading to follow-up intrusion</td><td>Social Engineering</td><td>HTTPS</td></tr></table>

Test data are strictly reserved for final, unobserved performance reporting. Both Stage-I and Stage-II utilize XGBoost as the foundational predictive engine (learning rate: 0.05, subsampling ratio: 0.9, column subsampling ratio: 0.9, L2 regularization: 1.0, maximum 8000 boosting rounds). This standardized protocol is uniformly enforced across all datasets and baseline variants to ensure a fair comparison.

Evaluation metrics. We report macro- and weightedaveraged Precision, Recall, and F1-scores, alongside the multiclass macro ROC-AUC. Precision, Recall, and F1 are computed directly from the final hard decision space formulated in Eq. (15). Under this stringent evaluation paradigm, if a true malicious sample is suppressed and reassigned to Benign due to insufficient attribution confidence, it correctly incurs a strict false-negative penalty for its respective ground-truth malicious class.

Baselines. We benchmark THEMIS against four representative state-of-the-art architectures: TFE-GNN [31], Flow-MAE [13], EarlyCrowAPT [27], and Trident [32]. These methods collectively encompass graph-based encrypted traffic modeling, masked self-supervised representation learning, context-driven advanced persistent threat (APT) detection, and autoencoder-based open-world traffic modeling. All methods use identical data splits, and baselines follow their official implementations and original procedures.

Setup. All empirical evaluations were executed within an Ubuntu environment running Python 3.8, PyTorch 1.13.1, and DGL 1.1.3. Computations were accelerated using a single CUDA-enabled GPU (14.56 GB VRAM) hosted on a machine equipped with an 8-core CPU and 30.97 GB of system RAM.

## B. Overall Performance

Table IV reports the end-to-end results of THEMIS across all six datasets under their available label spaces. The framework remains effective across both public benchmarks and the enterprise dataset. Under the available label spaces, the same hierarchy supports malicious-candidate screening and release control on binary datasets such as ZAPT-2026, while enabling fine-grained attribution when subtype labels are available.

Two observations are most important. First, the gains are not restricted to weighted metrics dominated by head classes; THEMIS also preserves strong macro performance, which shows that the improvements are not obtained merely by fitting the majority traffic mass more aggressively. Second, the advantage is more visible on the harder settings, especially CIC-UNSW-NB15 [25], [26], DAPT2020 [28], and BAI-Net26, where subtype overlap, heterogeneous sources, and weaker labels make flat classification less reliable. This matches the design goals of Sections III and IV: the main value of THEMIS lies in combining behavior-oriented representation, candidatespace purification, and selective attribution rather than simply replacing one classifier with another.

The gap between Weighted-F1 and Macro-F1 on CIC-UNSW-NB15 [25], [26] mainly results from the extreme class imbalance and a small number of difficult malicious subtypes. Benign traffic accounts for 97.47% of the test set and achieves an F1-score of 0.9977, which strongly influences the weighted metric, whereas Macro-F1 gives equal importance to lowsupport classes. In the representative test split shown in Fig. 6, Analysis contains only 77 samples, of which 27 are assigned to Benign; Backdoor and Worms are similarly sensitive to a small number of errors because of their limited support. The main cross-subtype errors occur within the DoS–Exploits– Reconnaissance cluster, where overlapping traffic patterns cause samples to be absorbed by the larger neighboring classes. The metric gap therefore reflects localized difficulty in rare-class preservation and fine-grained malicious discrimination rather than a general failure of benign–malicious separation.

## C. Mechanism Analysis

This subsection examines whether the observed gains align with the intended component roles, focusing on the representation- and feature-level effects of NUE and the candidate-space refinement achieved by Stage-I gating.

TABLE IV: End-to-end performance of THEMIS across six datasets under the available label space of each dataset. Values are reported as mean $\pm \ \mathrm { s t d } .$

<table><tr><td rowspan="2">Dataset</td><td colspan="3">Macro Metrics</td><td colspan="3">Weighted Metrics</td><td rowspan="2">AUC</td></tr><tr><td>Precision</td><td>Recall</td><td>F1</td><td>Precision</td><td>Recall</td><td>F1</td></tr><tr><td>ZAPT-2026</td><td> $0.9999 \pm 0.0001$ </td><td> $0.9996 \pm 0.0002$ </td><td> $0.9998 \pm 0.0001$ </td><td> $0.9999 \pm 0.0001$ </td><td> $0.9999 \pm 0.0001$ </td><td> $0.9999 \pm 0.0001$ </td><td> $0.9996 \pm 0.0001$ </td></tr><tr><td>DAPT2020</td><td> $0.9912 \pm 0.0137$ </td><td> $0.9144 \pm 0.0114$ </td><td> $0.9431 \pm 0.0090$ </td><td> $0.9994 \pm 0.0005$ </td><td> $0.9994 \pm 0.0005$ </td><td> $0.9994 \pm 0.0005$ </td><td> $0.9999 \pm 0.0181$ </td></tr><tr><td>CIC-UNSW-NB15</td><td> $0.8420 \pm 0.0215$ </td><td> $0.7712 \pm 0.0206$ </td><td> $0.7992 \pm 0.0174$ </td><td> $0.9974 \pm 0.0002$ </td><td> $0.9975 \pm 0.0002$ </td><td> $0.9974 \pm 0.0002$ </td><td> $0.9999 \pm 0.0027$ </td></tr><tr><td>Unraveled</td><td> $0.9978 \pm 0.0342$ </td><td> $0.9885 \pm 0.0362$ </td><td> $0.9928 \pm 0.0340$ </td><td> $0.9999 \pm 0.0000$ </td><td> $0.9999 \pm 0.0000$ </td><td> $0.9999 \pm 0.0000$ </td><td> $0.9935 \pm 0.0131$ </td></tr><tr><td>EarlyCrow</td><td> $0.9999 \pm 0.0034$ </td><td> $0.9998 \pm 0.0003$ </td><td> $0.9999 \pm 0.0011$ </td><td> $0.9999 \pm 0.0015$ </td><td> $0.9999 \pm 0.0003$ </td><td> $0.9999 \pm 0.0002$ </td><td> $0.9999 \pm 0.0006$ </td></tr><tr><td>BAI-Net26</td><td> $0.9986 \pm 0.0052$ </td><td> $0.9776 \pm 0.0079$ </td><td> $0.9873 \pm 0.0055$ </td><td> $0.9992 \pm 0.0004$ </td><td> $0.9992 \pm 0.0003$ </td><td> $0.9992 \pm 0.0004$ </td><td> $0.9998 \pm 0.0004$ </td></tr></table>

TABLE V: Stage-I routing behavior across datasets. Benign FFR denotes the fraction of benign samples forwarded to Stage-II, Mal. Dropped denotes the fraction of malicious samples not forwarded, and Stage-II Load Red. denotes the fraction of all samples removed before Stage-II.

<table><tr><td>Dataset</td><td>Mal. Recall</td><td>Benign FFR</td><td>Forwarded Rate</td><td>Mal. Dropped</td><td>Stage-II Load Red.</td></tr><tr><td>ZAPT-2026</td><td>0.9992</td><td>0.0001</td><td>0.1037</td><td>0.0008</td><td>0.8963</td></tr><tr><td>DAPT2020</td><td>0.9993</td><td>0.0002</td><td>0.1819</td><td>0.0007</td><td>0.8181</td></tr><tr><td>CIC-UNSW-NB15</td><td>0.9943</td><td>0.0003</td><td>0.0172</td><td>0.0057</td><td>0.9828</td></tr><tr><td>Unraveled</td><td>0.9999</td><td>0.0001</td><td>0.0472</td><td>0.0001</td><td>0.9528</td></tr><tr><td>EarlyCrow</td><td>0.9999</td><td>0.0001</td><td>0.6100</td><td>0.0001</td><td>0.3900</td></tr><tr><td>BAI-Net26</td><td>0.9992</td><td>0.0015</td><td>0.1821</td><td>0.0008</td><td>0.8179</td></tr></table>

## Representation and feature-level effects of NUE.

Silhouette: -0.018 -> 0.105 DBI: 3.736 -> 3.175  
![](images/e9e8811d49e3a18f7b764db7eb3d8b1850954eb2649fa34521d841fded6d65dd.jpg)  
(a) DAPT2020

Figure 3 presents representative results on DAPT2020 [28], EarlyCrow [27], and BAI-Net26. Raw flow statistics mainly reflect traffic magnitude, leaving many classes entangled, whereas NUE captures temporal, directional, semantic, and host– pair interaction patterns. This improves inter-class separation on DAPT2020 and intra-class compactness on EarlyCrow and BAI-Net26, as reflected by higher Silhouette scores and lower Davies–Bouldin indices. Complementing this representationspace analysis, Fig. 4 shows that the influential NUE groups vary across datasets, indicating that the model draws on different behavioral dimensions under different traffic distributions.

Effect of Stage-I gating. Table V reports the routing behavior of Stage-I as a candidate router. Across datasets, Stage-I preserves almost all malicious traffic while keeping benign false forwarding low, thereby removing many easy benign samples before fine-grained attribution. CIC-UNSW-NB15 achieves the largest Stage-II load reduction, but also exhibits the highest malicious drop rate of 0.57%, with $\tau _ { g }$ set to 0.985 in this experiment. This trade-off is governed by $\tau _ { g } \mathrm { : }$ in recall-critical deployments, lowering the threshold routes more borderline flows to Stage-II and reduces malicious drops, at the direct cost of processing more traffic in the second stage. Figure 5 visualizes the effect on EarlyCrow: after gating, low-risk benign samples are largely removed and the retained samples form a more focused candidate region for Stage-II. Although EarlyCrow forwards more samples because of its larger malicious portion, it still maintains high malicious coverage and very low benign false forwarding. Overall, Stage-I reduces downstream attribution cost with only a small direct

Silhouette: 0.036 -> 0.161 DBI: 4.953 -> 2.850  
![](images/e406ed146a59fa91f5a4c07c05191cdfd3ad17b8a364a6084075ba185f674c5c.jpg)

![](images/99771346b2c804c33fbf496aaa8e71e307edb61ed78829681c958859527a2ca8.jpg)  
(b) EarlyCrow

Silhouette: -0.091 -> 0.104 DBI: 5.612 -> 3.321  
![](images/cc44b5f68564a4752eea997981685fa54b1805a00198cff6a53be3a7765c3684.jpg)

![](images/f447fe06280a6e496d64d8d52a8f15585b325de4812725ba162e65f8a7773b8c.jpg)  
(c) BAI-Net26  
Fig. 3: The horizontal and vertical axes correspond to the first two dimensions of Uniform Manifold Approximation and Projection (UMAP), which projects high-dimensional subtype representations into a two-dimensional space for visualization. NUE improves malicious-subtype compactness and separability, with higher Silhouette scores and lower Davies– Bouldin indices.

miss risk.

## D. Confusion Matrix

Figure 6 shows that the residual errors of THEMIS are highly structured rather than random. Across all six datasets, benign traffic is strongly separated, and most off-diagonal mass remains confined to semantically adjacent malicious classes, indicating that THEMIS learns attack-aware structure rather than only coarse anomaly cues. On BAI-Net26, the remaining errors mainly come from long-tail classes and closely related Lumma variants, while a few early-stage or weaksignal malicious samples drift to Benign. On CIC-UNSW-NB15 [25], [26], the main difficulty lies in the overlap among attack-stage labels, where several malicious classes, especially DoS, Backdoor, Reconnaissance, and Worms, are partially absorbed by Exploits; thus, the challenge is intramalicious ambiguity rather than benign–malicious separation. DAPT2020 [28] is strongly diagonal overall, with residual errors concentrated in a few weak-signal or extremely small classes such as Malware Download, Privilege Escalation, and SQL Injection. EarlyCrow [27] and ZAPT-2026 [29] show very limited confusion because their class boundaries are naturally clearer, whereas Unraveled also shows limited confusion, with only limited confusion between weakly externalized postcompromise behaviors. Overall, the matrices consistently show that THEMIS not only preserves a very stable benign boundary, but also achieves fine-grained malicious attribution in most cases; when errors occur, they are usually local confusions within the correct attack semantic region rather than a collapse into large-scale false alarms or missed detections.

This article has been accepted for publication in IEEE Transactions on Dependable and Secure Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TDSC.2026.3731286  
![](images/d33d127cf9d3ccdf448e24312efae5a464bf6b9c80f861b21cddcd2416258405.jpg)  
(a) ZAPT-2026

![](images/1ab5cb69fa987bc330bbcac5280ebc7c5a8be6bcc2ce848cb25839f34a3a8a6f.jpg)  
(b) DAPT2020

![](images/fc76eb4238a4dcb58efa825d51423884892fb226f3fd948cf2eac4defb8d2d5f.jpg)  
(c) CIC-UNSW-NB15

![](images/2477d13cf0909a7d57f76f9695dd6df998e6085c55d32228b3aadc78e46156b1.jpg)  
(d) Unraveled

![](images/2d2ad353b27299189a18213971fd4fe95ed9aecb84464977cb186bf5e20725bf.jpg)  
(e) EarlyCrow

![](images/5910fa96f8a7d3cef88e30750f3bd23bbd49e23f30168d65ab5425780d8ceb80.jpg)  
(f) BAI-Net26  
Fig. 4: SHAP-based attribution of the four NUE feature groups across datasets, showing dataset-dependent importance patterns.

## E. Suspicious-Class Evaluation

In practical traffic analysis, some malicious flows may not provide sufficient evidence for assignment to a predefined subtype. We therefore introduce an additional Suspicious class to verify that THEMIS can also support such unresolved cases. Samples assigned to Suspicious remain in the metric computation and are treated as errors relative to their groundtruth classes. As shown in Table VIII, Weighted-F1 remains at or above 0.9973 across all datasets. ZAPT-2026, EarlyCrow, and Unraveled retain Macro-F1 scores above 0.99, while BAI-Net26 reaches 0.9871. The main Macro-F1 changes appear on

TABLE VI: End-to-end performance comparison of THEMIS and SOTA methods on different datasets.

<table><tr><td rowspan="2">Dataset</td><td rowspan="2">Method</td><td colspan="3">Macro</td><td colspan="3">Weighted</td><td rowspan="2">AUC</td></tr><tr><td>P</td><td>R</td><td>F1</td><td>P</td><td>R</td><td>F1</td></tr><tr><td rowspan="5">ZAPT-2026</td><td>EarlyCrowAPT</td><td>0.9768</td><td>0.8854</td><td>0.9262</td><td>0.9982</td><td>0.9982</td><td>0.9981</td><td>0.9749</td></tr><tr><td>Flow-MAE</td><td>0.9956</td><td>0.9726</td><td>0.9816</td><td>0.9956</td><td>0.9956</td><td>0.9956</td><td>0.9958</td></tr><tr><td>TFE-GNN</td><td>0.9077</td><td>0.9334</td><td>0.9199</td><td>0.9583</td><td>0.9562</td><td>0.9570</td><td>0.9734</td></tr><tr><td>Trident</td><td>0.9941</td><td>0.9746</td><td>0.9840</td><td>0.9917</td><td>0.9916</td><td>0.9916</td><td>0.9990</td></tr><tr><td>THEMIS</td><td>0.9999</td><td>0.9996</td><td>0.9998</td><td>0.9999</td><td>0.9999</td><td>0.9999</td><td>0.9996</td></tr><tr><td rowspan="5">DAPT2020</td><td>EarlyCrowAPT</td><td>0.1412</td><td>0.1429</td><td>0.1420</td><td>0.9767</td><td>0.9883</td><td>0.9824</td><td>0.9975</td></tr><tr><td>Flow-MAE</td><td>0.4057</td><td>0.3763</td><td>0.3833</td><td>0.9109</td><td>0.9062</td><td>0.9066</td><td>0.9243</td></tr><tr><td>TFE-GNN</td><td>0.3643</td><td>0.3695</td><td>0.3644</td><td>0.9181</td><td>0.9080</td><td>0.9086</td><td>0.9626</td></tr><tr><td>Trident</td><td>0.4148</td><td>0.3944</td><td>0.4033</td><td>0.9188</td><td>0.9203</td><td>0.9190</td><td>0.8372</td></tr><tr><td>THEMIS</td><td>0.9912</td><td>0.9144</td><td>0.9431</td><td>0.9994</td><td>0.9994</td><td>0.9994</td><td>0.9999</td></tr><tr><td rowspan="5">CIC-UNSW-NB15</td><td>EarlyCrowAPT</td><td>0.2491</td><td>0.2400</td><td>0.2444</td><td>0.9920</td><td>0.9565</td><td>0.9742</td><td>0.8764</td></tr><tr><td>Flow-MAE</td><td>0.3204</td><td>0.3781</td><td>0.3376</td><td>0.9944</td><td>0.9935</td><td>0.9939</td><td>0.9877</td></tr><tr><td>TFE-GNN</td><td>0.4876</td><td>0.5368</td><td>0.4924</td><td>0.9549</td><td>0.9509</td><td>0.9497</td><td>0.9811</td></tr><tr><td>Trident</td><td>0.1984</td><td>0.3109</td><td>0.2246</td><td>0.9882</td><td>0.9444</td><td>0.9649</td><td>0.6142</td></tr><tr><td>THEMIS</td><td>0.8420</td><td>0.7712</td><td>0.7992</td><td>0.9974</td><td>0.9975</td><td>0.9974</td><td>0.9999</td></tr><tr><td rowspan="5">Unraveled</td><td>EarlyCrowAPT</td><td>0.3997</td><td>0.4000</td><td>0.3998</td><td>0.9965</td><td>0.9983</td><td>0.9974</td><td>0.8736</td></tr><tr><td>Flow-MAE</td><td>0.6250</td><td>0.7500</td><td>0.6667</td><td>0.9999</td><td>0.9999</td><td>0.9999</td><td>0.9999</td></tr><tr><td>TFE-GNN</td><td>0.2491</td><td>0.2500</td><td>0.2496</td><td>0.9852</td><td>0.9921</td><td>0.9886</td><td>0.9930</td></tr><tr><td>Trident</td><td>0.2583</td><td>0.6667</td><td>0.2619</td><td>0.9983</td><td>0.9534</td><td>0.9753</td><td>0.6408</td></tr><tr><td>THEMIS</td><td>0.9978</td><td>0.9885</td><td>0.9928</td><td>0.9999</td><td>0.9999</td><td>0.9999</td><td>0.9999</td></tr><tr><td rowspan="5">EarlyCrow</td><td>EarlyCrowAPT</td><td>0.9591</td><td>0.9689</td><td>0.9637</td><td>0.9904</td><td>0.9903</td><td>0.9903</td><td>0.9987</td></tr><tr><td>Flow-MAE</td><td>0.4886</td><td>0.4368</td><td>0.4585</td><td>0.9968</td><td>0.9979</td><td>0.9973</td><td>0.9119</td></tr><tr><td>TFE-GNN</td><td>0.5122</td><td>0.5556</td><td>0.5122</td><td>0.9967</td><td>0.9971</td><td>0.9965</td><td>0.9994</td></tr><tr><td>Trident</td><td>0.4966</td><td>0.4328</td><td>0.4312</td><td>0.9887</td><td>0.9643</td><td>0.9760</td><td>0.8901</td></tr><tr><td>THEMIS</td><td>0.9999</td><td>0.9998</td><td>0.9999</td><td>0.9999</td><td>0.9999</td><td>0.9999</td><td>0.9999</td></tr><tr><td rowspan="5">BAI-Net26</td><td>EarlyCrowAPT</td><td>0.1722</td><td>0.1205</td><td>0.0871</td><td>0.6418</td><td>0.6133</td><td>0.5220</td><td>0.6668</td></tr><tr><td>Flow-MAE</td><td>0.4033</td><td>0.3261</td><td>0.3322</td><td>0.9559</td><td>0.9604</td><td>0.9560</td><td>0.9210</td></tr><tr><td>TFE-GNN</td><td>0.5532</td><td>0.5556</td><td>0.5544</td><td>0.9793</td><td>0.9896</td><td>0.9844</td><td>0.9853</td></tr><tr><td>Trident</td><td>0.3180</td><td>0.3551</td><td>0.3005</td><td>0.8117</td><td>0.8125</td><td>0.8031</td><td>0.8490</td></tr><tr><td>THEMIS</td><td>0.9986</td><td>0.9776</td><td>0.9873</td><td>0.9992</td><td>0.9992</td><td>0.9992</td><td>0.9998</td></tr></table>

TABLE VII: End-to-end Macro-F1 under the original setting and distributed three-gateway deployment.

<table><tr><td>Dataset</td><td>Original</td><td>Gateway 0</td><td>Gateway 1</td><td>Gateway 2</td></tr><tr><td>ZAPT-2026</td><td>0.9998</td><td>0.9999</td><td>0.9994</td><td>0.9999</td></tr><tr><td>DAPT2020</td><td>0.9431</td><td>0.9497</td><td>0.9491</td><td>0.9247</td></tr><tr><td>CIC-UNSW-NB15</td><td>0.7992</td><td>0.7638</td><td>0.8027</td><td>0.7970</td></tr><tr><td>Unraveled</td><td>0.9928</td><td>0.9999</td><td>0.9364</td><td>0.9982</td></tr><tr><td>EarlyCrow</td><td>0.9999</td><td>0.9824</td><td>0.9783</td><td>0.9729</td></tr><tr><td>BAI-Net26</td><td>0.9873</td><td>0.9969</td><td>0.9759</td><td>0.9987</td></tr></table>

![](images/f2bdc27e4d16c9457cb66457da1e0ea07bbb04cb6d5eb0d9ce05bc1120ad75dc.jpg)  
(a) Latent space of EarlyCrow (raw features)

BenignMaliciousRejected  
![](images/06e5437a7fcb7a3ec68690e5b572830272d758a266e75c16c9fb754ad4a5b0c1.jpg)  
(b) Latent space of EarlyCrow (Stage-I gating)  
Fig. 5: Feature distribution and Stage-I gating results on EarlyCrow. The axes denote the first two principal components (PC), which are linear projection directions summarizing the main variance of high-dimensional flow representations. Stage-I filters most low-scoring samples and retains suspicious candidates for fine-grained classification.

DAPT2020 and CIC-UNSW-NB15, with decreases of 0.0179 and 0.0288, respectively. Known malicious samples are rarely assigned to Suspicious, with the highest rate being 0.0740% on DAPT2020, mainly among borderline Malware Download, Privilege Escalation, and SQL Injection samples.

The malicious-to-benign rate remains below 0.51% on all datasets and is highest on CIC-UNSW-NB15 [25], [26]. Several categories in this dataset are both sparse and behaviorally overlapping: Analysis, Backdoor, and Worms contain only 77, 84, and 45 samples, respectively, while some DoS flows exhibit characteristics similar to other attack types. Overall, the results show that the additional Suspicious output provides a practical fallback for unresolved subtype evidence while largely preserving performance on known traffic.

## F. Evaluation under Distributed Gateway Deployment

To evaluate THEMIS in a distributed setting, we construct a three-gateway deployment scenario following a federatedlearning-inspired global–local collaboration scheme. For each dataset, traffic is assigned to three logical gateways according to the partitioning protocol in Section V-A, and contextual statistics are computed independently from the traffic observed at each gateway. Each gateway trains a local model, while a shared global model is trained across the gateway data and then returned to each gateway for joint inference. The local and global Stage-I maliciousness scores and Stage-II subtype posteriors are fused using gateway-specific weights.

As shown in Table VII, THEMIS maintains generally strong gateway-level performance under this setting. The three DAPT2020 gateways achieve comparable Macro-F1 despite differences in local data coverage, while two Unraveled gateways maintain high Macro-F1 scores and BAI-Net26 remains consistent across gateway configurations. Larger variations are mainly observed when local partitions contain sparse or behaviorally overlapping subtypes, where limited sample support and changes in local traffic context make fine-grained Stage-II decisions more sensitive. This is reflected in the lower performance on CIC-UNSW-NB15 [25], [26] and one Unraveled gateway. By contrast, datasets with clearer and better-supported subtype structures remain close to the original results. Overall, the experiment indicates that THEMIS retains effective detection and attribution capability in the simulated multi-gateway environment and can adapt to differences in gateway-local traffic distributions.

## G. Comparison

Table VI compares THEMIS with representative SOTA methods under the same end-to-end label space. Most baselines achieve strong Weighted-F1, indicating good performance on benign and frequent classes, but their Macro-F1 decreases on several imbalanced datasets, revealing weaker discrimi nation of rare malicious subtypes. EarlyCrowAPT [27] uses contextual summaries derived from pair-flow, host, URL, and destination profiles, but is closely tied to APT-style web communication. Flow-MAE [13] operates on fixed-length payload-byte patches, whose reconstruction objective is less suited to subtype separation based on aggregate flow behavior. TFE-GNN [31] processes packet-level byte-graph sequences, but graph propagation may smooth minority-class evidence in benign-dominated traffic. Trident [32] uses flow-level statistical vectors and class-specific autoencoders, whose reconstruction errors can be difficult to compare when class sizes differ substantially.

By combining a behavior-oriented representation with hierarchical decision refinement, THEMIS better preserves raresubtype discrimination under class imbalance. This advantage is especially evident on BAI-Net26 and CIC-UNSW-NB15 [25], [26], where similar attack behaviors make Weighted-F1 less representative of fine-grained performance. The corresponding Macro-F1 gains show that THEMIS improves minority-class attribution while maintaining strong overall accuracy.

## H. Computational Overhead

The overhead of THEMIS mainly comes from NUE-based feature construction, Stage-I screening, and conditional Stage-II attribution. Because both stages are implemented with XGBoost, the computation is dominated by tree traversal

(c) CIC-UNSW-NB15  
This article has been accepted for publication in IEEE Transactions on Dependable and Secure Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TDSC.2026.3731286  
![](images/651f99e0fb9925d7a6ef295ac11e1cfcb1e9dcd51664d5275ff87a0cd24b6d2a.jpg)

![](images/5e15fb5288af814a7d50cc18c9c7895437c2ed2abe5f3a30f37e5f51816c5778.jpg)

![](images/c4c4a258ee0e4baf65a1cd0bc7dbd8f6007687b0f300c2effd477f94b54e6501.jpg)

(b) DAPT2020  
![](images/9f72d38d915c7453c4d1e79213bf1a5ceec2a2cf42ac0db53264d66324c4dab7.jpg)  
(d) Unraveled

![](images/1a5c08a8815fd9ddd7b73cc69818656c674baca6de5c95e07ffaa198023d77ce.jpg)  
(e) EarlyCrow

![](images/743bf21242c4354619338815e162865f15aa0c7fded74cf3d1b153af38ef7b58.jpg)  
(f) BAI-Net26  
Fig. 6: Row-normalized confusion matrices on six datasets, showing strong diagonal patterns with residual errors mainly between adjacent malicious classes.

TABLE VIII: End-to-end performance with the Suspicious class. M→B denotes the percentage of malicious samples assigned to Benign, and K→S denotes the percentage of known malicious samples assigned to Suspicious.

<table><tr><td>Dataset</td><td>Original Macro-F1</td><td>Revised Macro-F1</td><td>Original Weighted-F1</td><td>Revised Weighted-F1</td><td>M→B (%)</td><td>K→S (%)</td></tr><tr><td>ZAPT-2026</td><td>0.9998</td><td>0.9999 ▲0.0001</td><td>0.9999</td><td>0.9999</td><td>0.0000</td><td>0.0000</td></tr><tr><td>DAPT2020</td><td>0.9431</td><td>0.9252 ▼0.0179</td><td>0.9994</td><td>0.9992 ▼0.0002</td><td>0.0000</td><td>0.0740</td></tr><tr><td>CIC-UNSW-NB15</td><td>0.7992</td><td>0.7704 ▼0.0288</td><td>0.9974</td><td>0.9973 ▼0.0001</td><td>0.5086</td><td>0.0083</td></tr><tr><td>EarlyCrow</td><td>0.9999</td><td>0.9970 ▼0.0029</td><td>0.9999</td><td>0.9973 ▼0.0026</td><td>0.4358</td><td>0.0000</td></tr><tr><td>BAI-Net26</td><td>0.9873</td><td>0.9871 ▼0.0002</td><td>0.9992</td><td>0.9989 ▼0.0003</td><td>0.0836</td><td>0.0000</td></tr><tr><td>Unraveled</td><td>0.9928</td><td>0.9931 ▲0.0003</td><td>0.9999</td><td>0.9999</td><td>0.0000</td><td>0.0000</td></tr></table>

TABLE IX: Dataset scale and mean time overhead of THEMIS on different datasets.

<table><tr><td>Dataset</td><td>Raw Dataset Size (GB)</td><td>Extracted Dataset Size (GB)</td><td>Training Time (s)</td><td>Inference Time (s)</td></tr><tr><td>ZAPT-2026</td><td>5.30</td><td>0.35</td><td>18.59</td><td>13.50</td></tr><tr><td>DAPT2020</td><td>16.01</td><td>0.04</td><td>49.23</td><td>10.58</td></tr><tr><td>CIC-UNSW-NB15</td><td>100.42</td><td>1.69</td><td>3038.66</td><td>408.63</td></tr><tr><td>Unraveled</td><td>1025.11</td><td>1.96</td><td>1605.46</td><td>272.25</td></tr><tr><td>EarlyCrow</td><td>4.62</td><td>0.39</td><td>1210.84</td><td>163.07</td></tr><tr><td>BAI-Net26</td><td>590.12</td><td>0.40</td><td>209.57</td><td>70.21</td></tr></table>

rather than dense neural operations. In addition, Stage-II is applied only to forwarded candidates, so the fine-grained attribution cost does not scale with all input flows. As shown in Table X, XGBoost provides a favorable overall balance between end-to-end Macro-F1 and memory footprint across datasets, maintaining consistently strong predictive performance while requiring substantially less memory than neural tabular models such as TabNet, FT-Transformer, and ResNet-MLP. Table IX further reports the mean training and inference time of THEMIS across datasets. Training ranges from 18.59 s on ZAPT-2026 [29] to 3038.66 s on CIC-UNSW-NB15 [26], while inference ranges from 10.58 s on DAPT2020 to 408.63 s on CIC-UNSW-NB15. The larger costs on CIC-UNSW-NB15 [25], [26], EarlyCrow, and Unraveled [30] are consistent with their larger scale, stronger imbalance, or higher subtype complexity. Overall, the results suggest that THEMIS remains practical for deployment-relevant encrypted traffic analysis, since the heavier Stage-II attribution is invoked only for the routed subset rather than for every flow.

## I. Backbone Comparison

We compare representative tabular backbones under the same feature space, data split, and training protocol, including

TABLE X: Comparison of different backbone models in terms of end-to-end Macro-F1 and mean memory footprint. The value after each score denotes the absolute difference relative to XGBoost.

<table><tr><td colspan="7">(a) End-to-end Macro-F1</td></tr><tr><td>Backbone</td><td>ZAPT-2026</td><td>DAPT2020</td><td>CIC-UNSW-NB15</td><td>Unraveled</td><td>EarlyCrow</td><td>BAI-Net26</td></tr><tr><td>CatBoost</td><td>0.9185 ▼ 0.0812</td><td>0.9187 ▼ 0.0244</td><td>0.7531 ▼ 0.0461</td><td>0.9579 ▼ 0.0349</td><td>0.9985 ▼ 0.0014</td><td>0.9298 ▼ 0.0575</td></tr><tr><td>LightGBM</td><td>0.4544 ▼ 0.5453</td><td>0.8848 ▼ 0.0583</td><td>0.8230 ▲ 0.0238</td><td>0.9999 ▲ 0.0071</td><td>0.9978 ▼ 0.0021</td><td>0.9467 ▼ 0.0406</td></tr><tr><td>Random Forest</td><td>0.9996 ▼ 0.0001</td><td>0.7487 ▼ 0.1944</td><td>0.7037 ▼ 0.0955</td><td>0.9977 ▲ 0.0049</td><td>0.9963 ▼ 0.0036</td><td>0.9104 ▼ 0.0769</td></tr><tr><td>TabNet</td><td>0.9991 ▼ 0.0006</td><td>0.7600 ▼ 0.1831</td><td>0.5675 ▼ 0.2317</td><td>0.9316 ▼ 0.0612</td><td>0.9847 ▼ 0.0152</td><td>0.7319 ▼ 0.2554</td></tr><tr><td>FT-Transformer</td><td>0.9898 ▼ 0.0099</td><td>0.8697 ▼ 0.0734</td><td>0.5340 ▼ 0.2652</td><td>0.9173 ▼ 0.0755</td><td>0.1567 ▼ 0.8432</td><td>0.7360 ▼ 0.2513</td></tr><tr><td>ResNet-MLP</td><td>0.9971 ▼ 0.0026</td><td>0.6502 ▼ 0.2929</td><td>0.5399 ▼ 0.2593</td><td>0.8832 ▼ 0.1096</td><td>0.1234 ▼ 0.8765</td><td>0.7279 ▼ 0.2594</td></tr><tr><td>TabR</td><td>0.8059 ▼ 0.1938</td><td>0.6738 ▼ 0.2693</td><td>0.5194 ▼ 0.2798</td><td>0.8432 ▼ 0.1496</td><td>0.0958 ▼ 0.9041</td><td>0.7253 ▼ 0.2620</td></tr><tr><td>Ours</td><td>0.9997</td><td>0.9431</td><td>0.7992</td><td>0.9928</td><td>0.9999</td><td>0.9873</td></tr><tr><td colspan="7">(b) Mean Memory Footprint (MB)</td></tr><tr><td>Backbone</td><td>ZAPT-2026</td><td>DAPT2020</td><td>CIC-UNSW-NB15</td><td>Unraveled</td><td>EarlyCrow</td><td>BAI-Net26</td></tr><tr><td>CatBoost</td><td>3803.34 ▲ 2442.81</td><td>3370.37 ▲ 2327.47</td><td>28395.85 ▲ 4272.68</td><td>23843.50 ▲ 2297.11</td><td>13654.18 ▲ 4590.51</td><td>3638.81 ▲ 2367.13</td></tr><tr><td>LightGBM</td><td>3803.31 ▲ 2442.78</td><td>3197.84 ▲ 2154.94</td><td>27852.96 ▲ 3729.79</td><td>22901.37 ▲ 1354.98</td><td>12968.31 ▲ 3904.64</td><td>3400.15 ▲ 2128.47</td></tr><tr><td>Random Forest</td><td>1319.08 ▼ 41.45</td><td>873.79 ▼ 169.11</td><td>23291.68 ▼ 831.49</td><td>17476.12 ▼ 4070.27</td><td>9290.17 ▲ 226.50</td><td>1123.05 ▼ 148.63</td></tr><tr><td>TabNet</td><td>3993.49 ▲ 2632.96</td><td>3706.97 ▲ 2664.07</td><td>52294.15 ▲ 28170.98</td><td>35463.37 ▲ 13916.98</td><td>10795.81 ▲ 1732.14</td><td>1745.69 ▲ 474.01</td></tr><tr><td>FT-Transformer</td><td>3954.48 ▲ 2593.95</td><td>3457.38 ▲ 2414.48</td><td>28614.11 ▲ 4490.94</td><td>23967.09 ▲ 2420.70</td><td>13842.11 ▲ 4778.44</td><td>3660.91 ▲ 2389.23</td></tr><tr><td>ResNet-MLP</td><td>3996.79 ▲ 2636.26</td><td>3706.98 ▲ 2664.08</td><td>52294.29 ▲ 28171.12</td><td>35463.37 ▲ 13916.98</td><td>10285.39 ▲ 1221.72</td><td>3007.28 ▲ 1735.60</td></tr><tr><td>TabR</td><td>3405.89 ▲ 2045.36</td><td>3119.49 ▲ 2076.59</td><td>25147.73 ▲ 1024.56</td><td>21057.38 ▼ 489.01</td><td>11515.44 ▲ 2451.77</td><td>3272.19 ▲ 2000.51</td></tr><tr><td>Ours</td><td>1360.53</td><td>1042.90</td><td>24123.17</td><td>21546.39</td><td>9063.67</td><td>1271.68</td></tr></table>

![](images/7224b34655d1cd1ea9a0d8dc8b5309a05c06c55d639d3a33944c16e6b1c30c20.jpg)  
(a) Macro-F1 versus sub- (b) Macro-F1 versus (c) Macro-F1 versus subtype label rate on CIC- subtype label rate on type label rate on BAI-UNSW-NB15 DAPT2020 Net26  
Fig. 7: Effect of weak subtype supervision on three datasets. Macro-F1 is reported as the fine-grained label rate decreases from 100% to 2%, showing that semi-supervised Stage-II becomes more beneficial when subtype labels are scarce.

Random Forest [33], XGBoost [34], LightGBM [35], CatBoost [36], TabNet [37], FT-Transformer [38], ResNet-style MLP [38], and TabR [39]. We report end-to-end Macro-F1 together with mean memory usage.

Table X shows that tree-based ensembles are better matched to the current task than neural tabular backbones. The reason is that the input space is already highly structured and behaviororiented, combining conventional flow statistics with NUE features that are largely threshold-sensitive, piecewise, and sparse in effect. Such a feature space favors models that can partition heterogeneous decision regions directly and capture localized nonlinear interactions without relying on deeper representation learning.

Within this setting, XGBoost provides the most stable accuracy–efficiency trade-off, especially on the harder datasets with long tails, subtype imbalance, and stronger semantic overlap. By contrast, Random Forest is generally weaker at progressive hard-sample correction, LightGBM and CatBoost are less stable across heterogeneous subtype structures, and neural tabular models bring limited representational gain while incurring substantially higher memory cost. We therefore adopt XGBoost as the default backbone of THEMIS.

## J. Effect of Weak Supervision Under Limited Subtype Labels

We select CIC-UNSW-NB15 [25], [26], DAPT2020, and BAI-Net26 because they represent complex multi-type attacks, cross-source heterogeneous traffic, and fine-grained activity recognition, respectively. These settings allow us to examine whether semi-supervision preserves subtype discrimination as labeled data become scarce, particularly for long-tailed and behaviorally overlapping classes.

Figure 7 compares supervised training, supervised training with class reweighting, and the proposed semi-supervised scheme under different subtype label rates. Overall, semisupervision does not always outperform the supervised baselines when labels are abundant, but its advantage becomes increasingly clear as the label rate decreases. This trend is most evident on DAPT2020 [28] and BAI-Net26, and it also appears on CIC-UNSW-NB15 [25], [26] once the label rate drops to 50% or below. These results indicate that the main value of weak supervision is not to uniformly dominate fully supervised learning, but to preserve fine-grained malicious subtype discriminability when labeled subtype boundaries become insufficient. This behavior is consistent with the design objective of THEMIS, namely, to maintain stable subtype attribution when supervision becomes sparse, delayed, or heterogeneous.

## K. Ablation Study

We remove NUE, feedback, local MoE refinement, and the entire Stage-II module, respectively. Because weighted metrics are close to saturation on several datasets, we focus on Macro-F1 and use weighted metrics as auxiliary evidence.

Removing NUE. Removing NUE causes the largest and most consistent degradation across all datasets. The largest drops occur on DAPT2020 [28] and BAI-Net26, where Macro-F1 decreases from 0.9431 to 0.6019 and from 0.9873 to 0.6318, respectively. Clear degradation is also observed on CIC UNSW-NB15 [25], [26], EarlyCrow [27], Unraveled [30], and

![](images/17631d2a7bfd9c25764ceacd103560081fc0b21281057af702e998f954604625.jpg)

![](images/81fed1f715139effe4678174aa6c724f7d89a21f9e639c467c1cb09b6c01cd3f.jpg)

![](images/73dea7603149a3b8ab0381ffad92af33ab0f4012d29c7df63efaf278dd2b3689.jpg)

![](images/6f6d372a354675ff7d5b1793faab6668628355213e001488b877edb68942ab9c.jpg)

![](images/0d9bbf44ed302b5febf20d5ff1be9304fccca4c1476a5008dfc518b82fffe249.jpg)

![](images/ecf28ce0f86861b479cc1864cd4e5ae7eb5f9d5f15e3dc56f044e31be6486464.jpg)  
Fig. 8: Radar-chart comparison of ablation settings across six metrics. Larger enclosed areas indicate better overall performance. The full THEMIS generally shows the strongest profile, reflecting the contributions of NUE, feedback, MoE, and Stage-II.

![](images/09ae7d36e2cb2c5a7d9f82321ed13063717f9c1396213355531f5ffe2ba9eaf6.jpg)  
(a) ZAPT-2026

![](images/58030005ae8fc91162fd78f8707595292112604cab29fc833c416070f4e771f7.jpg)  
(c) CIC-UNSW-NB15

![](images/9989768aebe40ca06e941f40a50c72a8bc1d698c758843c06014c4b739dc6f5d.jpg)  
(b) DAPT2020

![](images/f57532af944734140e5aa8f3491f1a9cb8b35a773717ed04c187bedd79958915.jpg)  
(e) EarlyCrow

![](images/e5ac884647f07f755918b31a65d61e9ec810d43cf81503afddaeb87e9bc0e6d2.jpg)  
(d) Unraveled

![](images/8fdab1fb30d2088ff545241003d41d702c7b514d5a2dcf26a77aa7ca38c64277.jpg)  
(f) BAI-Net26  
Fig. 9: Group-wise ablation of the four NUE feature categories. −Int., −Div., −Dir., and −Temp. denote the removal of the interaction, diversity, directional, and temporal feature groups, respectively, from the complete NUE representation, while Base denotes the representation without any NUE features. The resulting Macro-F1 scores illustrate the dataset-specific contributions of these feature groups.

ZAPT-2026 [29], with Macro-F1 decreasing to 0.6520, 0.9661, 0.8992, and 0.9903. This confirms that NUE provides important behavioral separability for both benign–malicious screening and subtype preservation. We further remove each NUE feature group from the full representation and report the results in Fig. 9. Removing any group reduces Macro-F1, although the magnitude varies across datasets. This indicates that the four groups provide complementary behavioral information rather than being dominated by a single component.

Removing feedback. Removing feedback yields a smaller but consistent drop. The largest degradations appear on BAI-Net26, DAPT2020 [28], and EarlyCrow [27], where Macro-F1 decreases to 0.8008, 0.8602, and 0.7998, respectively. This indicates that feedback mainly stabilizes end-to-end decisions when Stage-I screening and Stage-II attribution provide partially inconsistent evidence.

Removing MoE. Removing MoE degrades performance on all datasets, with the clearest gains for the full model on BAI-Net26 and DAPT2020 [28]. Compared with NUE, MoE contributes less to global separability and more to local refinement within highly confusable malicious subspaces.

Removing Stage-II. Removing Stage-II verifies the necessity of the hierarchical design itself. The strongest degradation appears on BAI-Net26 and DAPT2020 [28], where Macro-F1 decreases to 0.8021 and 0.7782, respectively. The effect is smaller on EarlyCrow [27] and Unraveled, which indicates that the value of Stage-II grows with subtype overlap, heterogeneity, and open-world complexity.

## VI. DISCUSSION

The results support treating encrypted malicious traffic attribution as a staged decision problem. Stage-I removes many benign samples, while Stage-II performs conditional subtype attribution using pseudo-label self-training and selective local experts. Since the final release rule can withhold weak subtype evidence, a sample forwarded by Stage-I is not automatically assigned a malicious class. Malicious flows returned as Benign remain counted as false negatives in end-to-end evaluation.

This article has been accepted for publication in IEEE Transactions on Dependable and Secure Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TDSC.2026.3731286

NUE strengthens weak behavioral evidence by describing interaction imbalance, temporal irregularity, statistical variation, and communication disorder. The release rule further suppresses uncertain subtype predictions using confidence, normalized posterior entropy, and top-two margin as decision indicators. Under the current output policy, withheld predictions are assigned to Benign for operational handling, while most remaining errors arise from long-tail classes, closely related variants, short early-stage flows, and overlapping traffic patterns. These limitations motivate further work on uncertainty-aware routing and class-balanced refinement for low-support and behaviorally overlapping subtypes.

The robustness of THEMIS under adaptive traffic manipulation remains an important direction for further study. Attackers may reshape transmission rates, burst patterns, packet sizes, or interaction structures to weaken the behavioral irregularities captured by NUE. Future work will evaluate operationally feasible, semantics-preserving perturbations and quantify their effects on Stage-I malicious recall, Stage-II subtype attribution, and the cost of effective evasion.

## VII. CONCLUSION

This paper presented THEMIS, a hierarchical framework for payload-free encrypted malicious traffic analysis. It combines NUE-enhanced behavioral representation, Stage-I maliciouscandidate screening, and Stage-II subtype attribution with semisupervised learning, selective local experts, and multi-criteria release. Fine-grained labels are produced only when the refined posterior provides sufficient decision evidence. Experiments across multiple datasets demonstrate the effectiveness of coordinating behavioral representation, staged inference, local refinement, and selective subtype release.

## REFERENCES

[1] WatchGuard Threat Lab, “Watchguard threat lab reports 40% jump in evasive malware over encrypted connections as cybercriminals embrace stealthy tactics,” https://www.watchguard.com/wgrd-news/press-releases/ q2-2025-internet-security-report, 2025.

[2] CrowdStrike, “Crowdstrike 2026 global threat report: Year of the evasive adversary,” https://go.crowdstrike.com/2026-global-threat-report. html, 2026.

[3] IBM X-Force, “X-force threat intelligence index 2026,” https://www.ibm. com/forms/mkt-1f268, 2026.

[4] “Brickstorm backdoor,” U.S. Cybersecurity and Infrastructure Security Agency, U.S. National Security Agency, and Canadian Centre for Cyber Security, Tech. Rep. AR25-338A, Feb. 2026. [Online]. Available: https://media.defense.gov/2025/Dec/04/2003834878/-1/-1/0/ MALWARE-ANALYSIS-REPORT-BRICKSTORM-BACKDOOR.PDF

[5] B. Anderson, S. Paul, and D. McGrew, “Deciphering malware’s use of tls (without decryption),” Journal of Computer Virology and Hacking Techniques, vol. 14, no. 3, pp. 195–211, 2018.

[6] Z. Wang and V. L. Thing, “Feature mining for encrypted malicious traffic detection with deep learning and other machine learning algorithms,” Computers & Security, vol. 128, p. 103143, 2023.

[7] Z. Chen, G. Cheng, D. Niu, Y. Zhao, Y. Zhou, and S. Jiang, “Ultimate encrypted traffic feature engineering: Https encrypted traffic classification using restored application data unit length,” IEEE Transactions on Dependable and Secure Computing, 2025.

[8] C. Fu, Q. Li, and K. Xu, “Flow interaction graph analysis: Unknown encrypted malicious traffic detection,” IEEE/ACM Transactions on Networking, vol. 32, no. 4, pp. 2972–2987, 2024.

[9] Y. Qing, Q. Yin, X. Deng, Y. Chen, Z. Liu, K. Sun, K. Xu, J. Zhang, and Q. Li, “Low-quality training data only? a robust framework for detecting encrypted malicious network traffic,” 2023.

[10] C. Fu, Q. Li, E. Bertino, and K. Xu, “Training with only 1.0‰ samples: Malicious traffic detection via cross-modality feature fusion,” in Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security, 2025, pp. 3930–3944.

[11] X. Yang, S. Ruan, J. Li, Y. Yue, and B. Sun, “Trafcl: Robust encrypted malicious traffic detection via contrastive learning,” in Proceedings of the 33rd ACM International Conference on Information and Knowledge Management, 2024, pp. 2910–2919.

[12] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in Proceedings of the ACM Web Conference 2022, 2022, pp. 633–642.

[13] Z. Hang, Y. Lu, Y. Wang, and Y. Xie, “Flow-mae: Leveraging masked autoencoder for accurate, efficient and robust malicious traffic classification,” in Proceedings of the 26th International Symposium on Research in Attacks, Intrusions and Defenses, 2023, pp. 297–314.

[14] B. Anderson and D. McGrew, “Identifying encrypted malware traffic with contextual flow data,” in Proceedings of the 2016 ACM workshop on artificial intelligence and security, 2016, pp. 35–46.

[15] S. Xi, T. Fu, K. Bu, C. Yang, Z. Chang, W. Chen, Z. Ma, C. Chen, Y. Shen, and K. Ren, “Mineshark: Cryptomining traffic detection at scale.” in NDSS, 2025.

[16] H. Zhang, G. Liu, X. Shi, Y. Li, D. He, J. Wang, Z. Wang, Y. Zhu, K. Ruan, W. Cao et al., “Achieving high-speed and robust encrypted traffic anomaly detection with programmable switches,” in Proceedings of the ACM SIGCOMM 2025 Conference, 2025, pp. 1254–1256.

[17] M. Shen, J. Wu, K. Ye, K. Xu, G. Xiong, and L. Zhu, “Robust detection of malicious encrypted traffic via contrastive learning,” IEEE Transactions on Information Forensics and Security, 2025.

[18] X. Xiao, W. Xiao, R. Li, X. Luo, H. Zheng, and S. Xia, “Ebsnn: Extended byte segment neural network for network traffic classification,” IEEE Transactions on Dependable and Secure Computing, vol. 19, no. 5, pp. 3521–3538, 2021.

[19] M. Shen, K. Ye, X. Liu, L. Zhu, J. Kang, S. Yu, Q. Li, and K. Xu, “Machine learning-powered encrypted network traffic analysis: A comprehensive survey,” IEEE Communications Surveys & Tutorials, vol. 25, no. 1, pp. 791–824, 2022.

[20] N. Wickramasinghe, A. Shaghaghi, G. Tsudik, and S. Jha, “Sok: Decoding the enigma of encrypted network traffic classifiers,” pp. 1825–1843, 2025.

[21] R. Xie, Y. Wang, J. Cao, E. Dong, M. Xu, K. Sun, Q. Li, L. Shen, and M. Zhang, “Rosetta: Enabling robust tls encrypted traffic classification in diverse network environments with tcp-aware traffic augmentation,” in Proceedings of the ACM turing award celebration conference-China 2023, 2023, pp. 131–132.

[22] Z. Song, Z. Zhao, F. Zhang, G. Xiong, G. Cheng, X. Zhao, S. Guo, and B. Chen, “i<sup>2</sup> rnn: An incremental and interpretable recurrent neural network for encrypted traffic classification,” IEEE Transactions on Dependable and Secure Computing, 2023.

[23] M. Liu, Q. Yang, W. Wang, and S. Liu, “Semi-supervised encrypted malicious traffic detection based on multimodal traffic characteristics,” Sensors, vol. 24, no. 20, p. 6507, 2024.

[24] J. Zhao, Q. Li, Z. Han, J. Fu, G. Nan, M. Shen, and B. K. Bhargava, “Retrial: robust encrypted malicious traffic detection via discriminative relation incorporation and misleading relation correction,” IEEE Trans actions on Information Forensics and Security, vol. 20, pp. 677–692, 2025.

[25] N. Moustafa and J. Slay, “Unsw-nb15: a comprehensive data set for network intrusion detection systems (unsw-nb15 network data set),” in 2015 military communications and information systems conference (MilCIS). IEEE, 2015, pp. 1–6.

[26] H. Mohammadian, A. H. Lashkari, and A. A. Ghorbani, “Poisoning and evasion: Deep learning-based nids under adversarial attacks,” in 2024 21st Annual international conference on privacy, security and trust (PST). IEEE, 2024, pp. 1–9.

[27] A. Alageel and S. Maffeis, “Earlycrow: Detecting apt malware command and control over http (s) using contextual summaries,” in International Conference on Information Security. Springer, 2022, pp. 290–316.

[28] S. Myneni, A. Chowdhary, A. Sabur, S. Sengupta, G. Agrawal, D. Huang, and M. Kang, “Dapt 2020-constructing a benchmark dataset for advanced persistent threats,” in International workshop on deployable machine learning for security defense. Springer, 2020, pp. 138–163.

[29] H. Xu, C. Si, C. Wang, P. Sun, Q. Liu et al., “Aptsniffer: Detecting apt attack traffic using retrieval-augmented large language models,” in ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2025, pp. 1–5.

[30] S. Myneni, K. Jha, A. Sabur, G. Agrawal, Y. Deng, A. Chowdhary, and D. Huang, “Unraveled—a semi-synthetic dataset for advanced persistent threats,” Computer Networks, vol. 227, p. 109688, 2023.

[31] H. Zhang, L. Yu, X. Xiao, Q. Li, F. Mercaldo, X. Luo, and Q. Liu, “Tfe-gnn: A temporal fusion encoder using graph neural networks for fine-grained encrypted traffic classification,” in Proceedings of the ACM web conference 2023, 2023, pp. 2066–2075.

[32] Z. Zhao, Z. Li, Z. Song, W. Li, and F. Zhang, “Trident: A universal framework for fine-grained and class-incremental unknown traffic detection,” in Proceedings of the ACM Web Conference 2024, 2024, pp. 1608–1619.

[33] L. Breiman, “Random forests,” Machine learning, vol. 45, no. 1, pp. 5–32, 2001.

[34] T. Chen and C. Guestrin, “Xgboost: A scalable tree boosting system,” in Proceedings of the 22nd acm sigkdd international conference on knowledge discovery and data mining, 2016, pp. 785–794.

[35] G. Ke, Q. Meng, T. Finley, T. Wang, W. Chen, W. Ma, Q. Ye, and T.-Y. Liu, “Lightgbm: A highly efficient gradient boosting decision tree,” vol. 30, 2017.

[36] L. Prokhorenkova, G. Gusev, A. Vorobev, A. V. Dorogush, and A. Gulin, “Catboost: unbiased boosting with categorical features,” vol. 31, 2018.

[37] S. O. Arik and T. Pfister, “Tabnet: Attentive interpretable tabular learning,” <sup>¨</sup> in Proceedings of the AAAI conference on artificial intelligence, vol. 35, no. 8, 2021, pp. 6679–6687.

[38] Y. Gorishniy, I. Rubachev, V. Khrulkov, and A. Babenko, “Revisiting deep learning models for tabular data,” vol. 34, 2021, pp. 18 932–18 943.

[39] Y. Gorishniy, I. Rubachev, N. Kartashev, D. Shlenskii, A. Kotelnikov, and A. Babenko, “Tabr: Tabular deep learning meets nearest neighbors,” in International Conference on Learning Representations, vol. 2024, 2024, pp. 18 209–18 249.
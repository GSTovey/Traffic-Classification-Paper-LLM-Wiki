# Two Heads Are Better Than One: Models-to-Model Learning for Encrypted Trafic Analysis

Jia Liu , Bin Lu , Qingjun Yuan , Pinghui Wang, Senior Member, IEEE, Yong Yu , Fellow, IEEE, Ding Li , and Jian Chai

Abstract—Encrypted trafic analysis (ETA) plays a critical role in detecting malicious activities. Although machine learningbased ETA has shown significant promise, existing methods heavily depend on large-scale, manually labeled data. Meanwhile, the research community has released numerous publicly available encrypted trafic datasets, as well as many high-performing ETA models. However, the knowledge embedded in these models remains isolated and cannot be directly leveraged by existing approaches. These observations raise a key question: Can we construct a unified model that learns directly from existing ETA models to perform efective ETA, without relying on manually labeled data? Existing paradigms, such as ensemble learning and knowledge distillation, are unable to meet this goal because they struggle with heterogeneous feature spaces and conflicting model predictions. To address these challenges, we propose the Modelsto-Model Learning (M2ML) paradigm, guided by two principles: 1) Knowledge Semantization, which aligns heterogeneous traffic feature spaces into a unified semantic representation; and 2) Credibility-First Arbitration, which resolves inconsistencies among teacher models through their credibility and intermodel consensus. We develop an M2ML framework utilizing a large language model, incorporating Feature-Negative Entropy Injection and Consensus Credibility-Weighted Arbitration to operationalize these principles. Experiments on three publicly available encrypted trafic datasets demonstrate that the M2ML framework eliminates the need for manually labeled data and achieves accuracy surpassing that of the best teacher model. An analysis grounded in information-theoretic principles explains its efectiveness, confirming the M2ML paradigm as a promising paradigm for label-free ETA.

Index Terms—Encrypted trafic analysis, feature-negative entropy injection, consensus credibility-weighted arbitration, label-free.

E <sup>NCRYPTED</sup> <sup>trafic</sup> <sup>has</sup> <sup>become</sup> <sup>the</sup> <sup>dominant</sup> <sup>form</sup> of Internet communication [1], [3]. While encryption ensures user privacy and data security, it also conceals malicious behaviors [4], [5] and renders traditional Deep Packet Inspection (DPI) inefective [6]. As a result, advanced threat detection systems [7] face severe performance degradation, creating a persistent security blind spot in modern networks.

## I. INTRODUCTION

To overcome the encryption barrier, machine learning based encrypted trafic analysis (ETA) [8], [9] has emerged as a core methodology in both academic research and industrial practice. Deep learning models [10], [11], capable of automatically learning statistical features and temporal patterns from trafic, have achieved breakthrough performance in specific tasks such as application trafic identification [12], malicious trafic detection [13], [14]. However, these data-driven approaches rely heavily on large-scale manually labeled data, which are extremely dificult and costly to obtain due to encryption policies, privacy regulations, and the need for expert annotation.

In contrast, the research community has released numerous publicly available encrypted trafic datasets and a variety of open-source ETA models trained on heterogeneous traffic feature spaces. These models exhibit strong task-specific performance, implying that they encode substantial domain knowledge. Yet, this knowledge remains largely isolated within individual models and cannot be leveraged by existing paradigms [15]. These observations raise a key question:

Can we construct a unified model that learns directly from existing ETA models to perform efective ETA, without relying on manually labeled data?

Among existing learning paradigms, ensemble learning (EL) [16] and knowledge distillation (KD) [17] are the closest candidates for reusing knowledge from multiple models. Yet neither paradigm can address the setting considered in this work, where ETA models operate on heterogeneous trafic feature spaces and may produce conflicting predictions. These limitations give rise to two intrinsic challenges:

(1) Heterogeneous Features: ETA models are trained on diverse trafic feature spaces such as statistical flow vectors, packet-length sequences, or byte-distribution, or graph structures, producing feature representations that are inherently incompatible. EL provides no mechanism for aligning or reconciling such heterogeneous representations. KD requires the teacher and student to operate within a shared input domain, allowing the student to approximate the teacher’s output distribution. This assumption holds in vision and natural language processing (NLP), where models consume homogeneous inputs (pixels or tokens); however, it breaks down in cross-feature-space distillation, where no mechanism exists to align incompatible input domains.

(2) Prediction Conflicts: ETA models built on diferent feature spaces possess distinct inductive biases and capture different aspects of encrypted trafic. As a result, their predictions may diverge significantly, even for the same flow. However, EL and KD implicitly assume model reliability and treat all outputs as equally trustworthy. EL aggregates logits or votes without assessing each model’s confidence or consistency, allowing poorly calibrated predictions to bias the ensemble. KD sufers from the same issue: the student learns unreliable or inconsistent teacher logits, thereby introducing additional noise. Without assessing model credibility or resolving intermodel disagreement, these paradigms allow low-quality or inconsistent predictions to dominate the fusion process, ultimately degrading rather than improving performance.

To address these challenges, we propose the Models-to-Model Learning (M2ML) paradigm tailored for ETA. This paradigm enables a unified student model to directly learn and fuse knowledge from multiple heterogeneous teacher models, eliminating the need for manually labeled data. It is guided by two design principles: (1) Knowledge Semantization, which aims to align heterogeneous trafic feature spaces of encrypted trafic models by projecting their representations into a unified semantic space; (2) Credibility-First Arbitration, which resolves inconsistencies among teacher models according to model credibility and inter-model consensus.

Based on these principles, we develop the M2ML framework built upon a large language model (LLM), which operationalizes them through two mechanisms. (1) Feature-Negative Entropy Injection (FNEI) implements Knowledge Semantization by converting diverse trafic features into unified textual representations, thereby aligning the heterogeneous input spaces of teacher models; (2) Consensus Credibility-Weighted Arbitration (CCWA) implements Credibility-First Arbitration by dynamically aggregating teacher models based on both their global credibility and sample-level consensus, efectively reconciling conflicting outputs. These mechanisms together enable eficient, stable, and semantic-level crossmodel knowledge fusion for ETA.

Extensive experiments on three publicly available encrypted trafic datasets demonstrate that the M2ML framework outperforms the best teacher models, without relying on manually labeled data. Furthermore, grounded in information-theoretic principles, we analyze the core mechanisms of the M2ML framework to explain their rationality and efectiveness, confirming the soundness of this new model-centric paradigm.

The contributions of this paper can be summarized as follows:

• Paradigm Innovation: We propose the M2ML paradigm for ETA, which, for the first time, shifts the focus of ETA from data-driven to model-centric learning. It enables a unified student model to learn and fuse knowledge from multiple existing teacher models without requiring any manually labeled data, providing a new foundation in ETA.

Framework Design: We develop an LLM-based M2ML framework that realizes this paradigm through FNEI and CCWA. FNEI aligns the heterogeneous input spaces of teacher models by converting diverse trafic features into unified textual representations, while CCWA dynamically aggregates teacher models based on their global credibility and sample-level consensus. These mechanisms together ensure eficient, stable, and semantic-level knowledge fusion across heterogeneous teacher models.

Empirical and Theoretical Validation: We conduct extensive experiments on three public encrypted traffic datasets, demonstrating that the M2ML framework surpasses the best teacher models without using any manually labeled data. In addition, an information-theoretic analysis verifies the rationality and efectiveness of the M2ML framework, confirming the soundness of this new model-centric learning paradigm.

The remainder of this paper is organized as follows: Section II reviews related work. Section III introduces the M2ML paradigm and its two core design principles. Section IV details the M2ML framework and implementation. Section V presents the experimental setup and results. Section VI discusses limitations. Section VII provides the theoretical analysis from an information-theoretic perspective. Finally, Section VIII concludes the paper and outlines future research directions.

## II. RELATED WORK

## A. Ensemble Learning (EL)

EL improves prediction robustness by combining multiple base learners and has been widely adopted in ETA. Early studies focused on homogeneous ensembles, such as Random Forest [18] and XGBoost [19], based on Bagging or Boosting strategies, which demonstrated stable and reliable performance in statistical feature classification tasks [20]. Subsequent research explored heterogeneous ensembles, combining CNN [22], RNN [23], LSTM [24], and Transformer [25] to jointly capture spatial and temporal characteristics of encrypted flows [26]. To improve deployment eficiency, several lightweight ensemble schemes have been proposed, including dynamic classifier selection and ensemble knowledge distillation, which substantially reduce inference cost while maintaining accuracy [27].

EL has also been applied in broader security [28] and privacy contexts [29], including salience-aware kernel ensembles for scrambled-domain face recognition [30], snapshot ensembles for stabilizing website fingerprinting attacks [31], and random-forest ensembles for confidential inference on encrypted data [32]. These examples demonstrate the generality of EL in high-uncertainty and adversarial environments.

Despite these advances, EL fuses models only at the decision level through averaging or voting, without aligning heterogeneous feature spaces or resolving contradictions across model predictions. In contrast, M2ML aims to construct a unified student model that learns from multiple heterogeneous ETA models, where the teacher models may rely on diferent trafic feature spaces and provide inconsistent supervision.

## B. Knowledge Distillation (KD)

KD was first introduced by Hinton et al. [33], where a compact student model is trained to match the output distribution of a larger teacher model. Subsequent extensions, such as FitNet [34], have enriched the distillation process by incorporating intermediate feature alignment to improve the generalization of the student model.

In recent years, KD has evolved beyond model compression into a key technique for improving model generalization and cross-domain transfer, particularly efective in data-scarce or domain-shifted scenarios. For instance, Liu et al. [35] proposed an Instance Relationship Graph-based distillation method to improve cross-domain adaptability, while Zhu and Wang [36] designed an adaptive distillation framework based on gradient similarity to mitigate optimization bias. More recently, Zhang et al. [37] formulated a causal multi-teacher distillation framework to alleviate performance heterogeneity by leveraging front-door adjustment.

KD has also been widely adopted in network security and ETA. Lu et al. [38] proposed a two-stage distillationaware compression pipeline for trafic classification. Li et al. [39] developed an eficient intrusion detection system for invehicle networks by distilling representations. Dinh et al. [40] leveraged KD in edge computing to construct a compact intrusion detection network. Zhu et al. [41] further combined KD with Neural Architecture Search to automatically design lightweight malware detection models for mobile devices. A similar trend can be observed in NLP, where Sanh et al. [42] compressed BERT to 40% of its original size while retaining around 97% of its performance, and Jiao et al. [43] proposed TinyBERT, which employs multi-stage distillation to systematically enhance both intermediate and output layer knowledge transfer.

Although KD has achieved substantial success in model compression and transfer learning, it generally assumes that teacher and student models operate on a shared input representation. In contrast, M2ML targets heterogeneous ETA models whose inputs may come from diferent trafic feature spaces, and aims to fuse their knowledge into a unified student model.

## III. THE M2ML PARADIGM

## A. Motivation

In ETA, network trafic data are commonly collected as packet capture (PCAP) files. Each communication session can be represented as a flow constructed from the five-tuple (srcIP, dstIP, srcPort, dstPort, protocol). From these flows, statistical or sequential features x (such as packet length, inter-arrival time, transmission direction, and flow duration) are extracted to characterize encrypted behaviors [44] without relying on payload content. A typical ETA learning task can thus be formulated as a mapping $y = f ( x )$ , where f infers encrypted trafic semantics (e.g., application type, anomaly state, or command-and-control (C2) activity) from observed flow features x.

In practice, a variety of ETA models {f} have been independently developed for diferent objectives, including application identification, anomaly detection, and C2 behavior recognition. These models are often trained on distinct feature spaces $\mathcal { X } _ { i }$ and adopt diferent architectures (e.g., CNN for spatial statistical features, LSTM for temporal dependencies, or Transformer for hybrid representations). Despite their efectiveness within specific domains, these models remain fragmented and cannot share knowledge across tasks.

This observation naturally motivates the M2ML paradigm. Instead of learning f directly from manually labeled data, we ask whether it is possible to learn a new model F that unifies and generalizes the knowledge embedded in existing models $\{ f _ { i } \}$ . In other words, rather than mapping data to labels, M2ML seeks to map models to a new model,

$$
F \approx \mathcal {F} (f _ {1}, f _ {2}, \dots , f _ {n}),\tag{1}
$$

where $\mathcal { F } ( \cdot )$ denotes a process that extracts, aligns, and integrates the implicit knowledge within heterogeneous ETA models. This formulation enables the use of existing models as knowledge carriers, eliminating the need for additional manually labeled data. From this model-centric perspective, the M2ML paradigm transforms knowledge transfer from datadriven retraining to model-level synthesis, enabling unified learning across disjoint feature spaces.

## B. Design Principles

The M2ML paradigm is founded on two core design principles, which are summarized in Table I.

1) Knowledge Semantization: Heterogeneous ETA models often rely on disparate feature spaces, for example, statistical flow features, packet-level direction sequences, or temporal burst patterns, each capturing only partial aspects of encrypted behaviors. As a result, knowledge acquired by diferent ETA models exists in isolated feature spaces that lack direct correspondence with one another. This principle advocates projecting heterogeneous numerical trafic features into a unified, shared semantic space. This process, conceptualized as Feature-Negative Entropy Injection, reduces representation ambiguity across feature spaces by introducing semantic priors, thereby enabling the student model to integrate knowledge from heterogeneous teacher models more efectively.

2) Credibility-First Arbitration: ETA models are frequently trained on diverse encrypted trafic datasets, leading to inconsistent or even conflicting predictions for the same encrypted trafic sample (e.g., one model classifies it as video streaming, while another identifies it as VPN tunneling). This principle mitigates this problem through a reliability- and consensusaware prediction fusion strategy. Instead of treating all teacher models equally, it aggregates their predictions based on two complementary factors: (1) the degree of consensus, reflecting inter-model agreement for each encrypted trafic sample; and (2) the credibility weight, determined by each teacher model’s validation performance on benchmark datasets.

TABLE I  
CORE DESIGN PRINCIPLES IN THE M2ML PARADIGM

<table><tr><td>Principle</td><td>Challenge</td><td>Mechanism</td></tr><tr><td>Knowledge Semantization Credibility-First Arbitration</td><td>Knowledge Isolation Decision Conflict</td><td>Feature-Negative Entropy Injection Consensus Credibility-Weighted Arbitration</td></tr></table>

![](images/811cf01002ef7112908f546997d45f601fe53fd68653d7d9b9252744498b7134.jpg)  
Fig. 1. Overview of the M2ML paradigm.

By dynamically balancing consensus and credibility, this principle prioritizes reliable knowledge sources, suppresses noisy or biased predictions, and ultimately produces a robust supervisory distribution that facilitates label-free student model learning in ETA.

## C. Core Mechanism

The M2ML paradigm is designed as a two-stage process, as illustrated in Fig. 1.

1) Training Stage: This stage involves fusing knowledge from multiple heterogeneous teacher models into a unified student model. It includes the following key components:

• Teacher Models $\{ M _ { 1 } , \cdots , M _ { i } , \cdots , M _ { n } \} \colon$ : A set of pretrained, task-specific models covering diverse ETA objectives such as application classification, protocol identification, and anomaly detection. Each teacher model internalizes domain knowledge in its distinct feature space.

• Task Descriptor: Each task is represented by a tuple (task id f eaturepattern), where task id identifies the task type and f eaturepattern specifies how encrypted trafic features are extracted and formatted to match the corresponding teacher model’s input space.

• Teacher Model: Given a task descriptor, the appropriate teacher model M<sub>i</sub> is selected and receives an encrypted trafic sample. It encodes them according to the designated featurepattern and produces task-specific predictions.

• Task Data: Based on the teacher model’s predictions, each encrypted trafic sample is organized into a structured triplet (task id x y), where x denotes the encoded input feature vector and y represents the corresponding teacher predictions. This dataset serves as the knowledge source for the student model learning.

• Student Model: The student model learns to map inputs x to the corresponding teacher predictions y, conditioned on task id. The framework can be extended to incorporate additional teacher models without requiring any architectural modification.

• Student Model (final): The final student model consolidates the knowledge of all teacher models and achieves unified ETA within a single architecture.

2) Inferencing Stage: During inference, the student model follows the feature extraction logic defined by the teacher models. Given an unseen encrypted trafic sample, raw trafic data are processed according to the corresponding teacher-defined feature patterns to obtain heterogeneous feature representations, such as statistical, temporal, and byte-level features. These features are unified through Feature-Negative Entropy Injection to form a shared semantic representation, which is then transformed into structured textual inputs. The student model performs reasoning within this unified semantic representation and generates textual outputs.

## IV. THE M2ML FRAMEWORK

To instantiate the M2ML paradigm, we design an M2ML framework built upon an LLM. The overall workflow is illustrated in Fig. 2.

## A. Data Preprocessing

To ensure reliable and standardized input data for heterogeneous ETA models, a unified preprocessing pipeline is constructed. This stage focuses on cleaning, organizing, and partitioning the raw PCAP file into well-defined flow samples, thereby establishing a consistent and high-quality foundation for subsequent feature extraction and model training. The entire procedure consists of three main steps, as detailed below.

1) Flow Definition: Let $\mathcal { P } ~ = ~ \{ p _ { i } ~ | ~ i ~ = ~ 1 , . . . , T \}$ denote the complete set of captured packets, where T is the total number of captured packets. Each packet $p _ { k }$ is associated with a canonical five-tuple identifier:

$$
\Psi (p _ {i}) = (s r c I P, d s t I P, s r c P o r t, d s t P o r t, p r o t o c o l),\tag{2}
$$

where Ψ(·) denotes the mapping function that extracts the canonical five-tuple identifier from each packet.

A network flow $\ell _ { \phi }$ is then defined as the collection of all packets sharing the same five-tuple:

$$
\ell_ {\phi} = \{p _ {i} \in \mathcal {P} | \Psi (p _ {i}) = \phi \}.\tag{3}
$$

where $\phi$ represents a specific five-tuple value corresponding to the flow identifier.

![](images/e109f9f1fe648f56f50aad3900b1044d18a6e91caabb04d9c7b6f6dae87024ec.jpg)  
Fig. 2. Overall workflow of the M2ML framework.

2) Packet Sampling: To maintain comparable temporal granularity across encrypted trafic samples, each flow $\ell _ { \phi }$ is truncated into a fixed-length packet sequence:

$$
\mathbf {s} _ {\phi} = (p _ {1}, p _ {2}, \dots , p _ {L}), \quad L = 5.\tag{4}
$$

This sampled sequence serves as the basic unit for subsequent feature extraction.

3) Noise Filtering and Dataset Splitting: Malformed or incomplete flows, including those containing retransmissions or corrupted headers, are removed to improve data quality. The cleaned dataset D is then divided into training, validation, and test subsets with a stratified ratio of 8 : 1 : 1, thereby ensuring trafic class balance and consistency across all splits.

## B. Multi-Teacher Models

As illustrated in Fig. 2, the input of this stage is a preprocessed flow sample denoted as $\ell _ { \phi } .$ For each flow sample, the M2ML framework invokes K heterogeneous teacher models in parallel. The i-th teacher model contains its own feature extractor $g _ { i } ( \cdot )$ , which derives a set of native trafic features $x _ { i } = g _ { i } ( \ell _ { \phi } )$ (corresponding to “feature (1), feature $( 2 ) , \ldots ^ { \prime }$ in Fig. 2). Each teacher model then produces a predictive distribution p<sub>i</sub>(y | x<sub>i</sub>), representing the class probabilities (corresponding to “Prediction (1), Prediction (2), ” in Fig. 2). These teacher model predictions are subsequently fused by the Consensus Credibility-Weighted Arbitration mechanism to generate a unified decision distribution q(y | x) (corresponding to “teacher logits” in Fig. 2). To achieve cross-model knowledge fusion and conflict resolution without requiring manually labeled data, this stage consists of two steps: Feature-Negative Entropy Injection and Consensus Credibility-Weighted Arbitration.

1) Feature-Negative Entropy Injection (FNEI): Heterogeneous teacher models often difer in their feature spaces, including dimensional scales and field names, which can lead to uncertainty and inconsistency during the fusion of heterogeneous model knowledge. To address this issue, we propose a FNEI mechanism, a minimal yet efective strategy that converts numerical trafic features into unified textual descriptions, thereby providing a uniform semantic representation. Specifically, for each teacher model’s feature vector $x _ { i } ,$ all indicators are serialized into key–value textual pairs following a fixed template. This unified semantic representation transforms heterogeneous trafic features into interpretable behavioral semantics, establishing a language-based bridge among structurally distinct teacher models. A simplified example is shown below:

###Instruction:

Classify whether the given trafic flow is benign or malicious. The task is malware detection, and you should rely on statistical features.

###Input:

Statistical features: src port= 443 (standard TLS port), dst port= 52345 (non-standard client port), packet count= 17, protocol=TLS...

###Answer:

This flow is malicious.

2) Consensus Credibility-Weighted Arbitration (CCWA): After obtaining multiple predictive distributions $\{ p _ { i } ( y | x _ { i } ) \} _ { i = 1 } ^ { K }$ (K denotes the total number of teacher models), CCWA fuses them into a unified decision distribution q(y | x). The process consists of three substeps.

a) Global credibility: Each teacher model’s credibility is estimated from its accuracy Acc on an independent validation set. The normalized credibility weight for the i-th teacher model is computed as:

$$
\alpha_ {i} = \frac {A c c _ {i} ^ {\gamma}}{\sum_ {j = 1} ^ {K} A c c _ {j} ^ {\gamma}}, \quad \gamma > 0, \sum_ {i = 1} ^ {K} \alpha_ {i} = 1,\tag{5}
$$

where γ controls the sensitivity to model accuracy, and $\alpha _ { i }$ represents the global credibility of each teacher model across all encrypted trafic data.

b) Sample-level consensus: To quantify the pairwise agreement among teacher models on the same encrypted trafic sample, we compute pairwise cosine similarity between their predictive distributions:

$$
\operatorname{sim} (p _ {i}, p _ {j}) = \frac {\langle p _ {i} , p _ {j} \rangle}{\| p _ {i} \| \| p _ {j} \|}, \quad 1 \leq i, j \leq K.\tag{6}
$$

The average consensus score for the i-th teacher model is given by:

$$
s_{i}(\ell_{\phi}) = \frac{1}{K - 1}\sum_{\substack{j = 1\\ j\neq i}}^{K}\text{sim} (p_{i},p_{j}),\tag{7}
$$

and is further normalized by a softmax function:

$$
\beta_ {i} (\ell_ {\phi}) = \frac {\exp (s _ {i} (\ell_ {\phi}))}{\sum_ {j = 1} ^ {K} \exp (s _ {j} (\ell_ {\phi}))},\tag{8}
$$

This produces the sample-level consensus weight $\beta _ { i } ( \ell _ { \phi } )$

c) Adaptive fusion: The final arbitration weight combines both credibility and consensus as:

$$
w _ {i} (\ell_ {\phi}) = \frac {\alpha_ {i} \beta_ {i} (\ell_ {\phi})}{\sum_ {j = 1} ^ {K} \alpha_ {j} \beta_ {j} (\ell_ {\phi})}.\tag{9}
$$

The unified decision distribution is then obtained through a log-opinion pool [45], [46], [47] formulation:

$$
q (y \mid x) = \frac {\prod_ {i = 1} ^ {K} p _ {i} (y \mid x _ {i}) ^ {w _ {i} (\ell_ {\phi})}}{\sum_ {c \in \mathcal {Y}} \prod_ {i = 1} ^ {K} p _ {i} (c \mid x _ {i}) ^ {w _ {i} (\ell_ {\phi})}},\tag{10}
$$

where x represents the joint feature view of the same encrypted trafic sample across all teacher models, y represents the target class, c is used to enumerate all candidate classes, and $\mathcal { V }$ is the set of all possible trafic classes.

## C. Student Model

The student model aims to learn, without any manually labeled data, the collective knowledge from multiple heterogeneous teacher models. Mathematically, the student is trained on a corpus $\mathcal { D } ~ = ~ \{ ( \hat { x } ^ { ( n ) } , q ^ { ( n ) } ) \} _ { n = 1 } ^ { N }$ , where N denotes the total number of encrypted trafic samples, $\hat { x } ^ { ( n ) }$ denotes the textualized trafic feature description generated by the FNEI process, and $q ^ { ( n ) } ( y )$ represents the unified teacher logits obtained from the CCWA mechanism. The learning objective is to align the student model’s predictive distribution $P _ { \theta } ( y$ | xˆ) with q(y | x) over all encrypted trafic samples.

Input Embedding. For each encrypted trafic sample, input sequence $\hat { x } = [ \hat { x } _ { 1 } , \hat { x } _ { 2 } , . . . , \hat { x } _ { L } ]$ is first tokenized and converted into continuous embeddings through a learnable lookup table $E _ { \mathrm { t o k } } \in \mathbb { R } ^ { V \times d }$ , where V is the vocabulary size, d is the hidden layer dimension and, L denotes the sequence length (i.e., the number of tokens). The resulting embedding matrix is denoted as $X ^ { ( 0 ) } \in \mathbb { R } ^ { L \times d }$

$$
X ^ {(0)} = [ E _ {\mathrm{tok}} [ \hat {x} _ {1} ], E _ {\mathrm{tok}} [ \hat {x} _ {2} ], \dots , E _ {\mathrm{tok}} [ \hat {x} _ {L} ] ],\tag{11}
$$

This embedding output serves as the initial hidden representation, denoted by $H ^ { ( 0 ) } = X ^ { ( 0 ) }$ , which is then fed into the first transformer block.

Positional Encoding. Relative positional information is modeled using rotary position embeddings (RoPE) [48], which are applied within the subsequent self-attention layers.

Transformer Blocks. The student model employs a decoder-only transformer comprising 32 stacked blocks, as shown in Fig. 2. Each block transforms the hidden representation from the previous layer $H ^ { ( \ell - 1 ) } \in \mathbb { R } ^ { L \times d }$ into an updated representation $\bar { H } ^ { ( \ell ) } \in \mathbb { R } ^ { L \times d }$ through a series of normalization, attention, and feed-forward operations, where $\ell \in \{ 1 , . . . , 3 2 \}$ indexes the transformer blocks. The detailed formulation of each component is presented below.

1) Root Mean Square Normalization (RMSNorm): To stabilize training and accelerate convergence, each hidden representation $H ^ { ( \ell - 1 ) }$ is normalized using RMSNorm [49], which rescales token representations by their root mean square without mean subtraction as in LayerNorm [50]. Formally,

$$
\widetilde {H} = \mathrm{RMSNorm} (H ^ {(\ell - 1)}),\tag{12}
$$

where $\widetilde { H }$ denotes the normalized hidden layer representation. 2) Multi-Head Self-Attention (MHSA): Attention allows each token to aggregate contextual information from other tokens within the sequence. For each head, the $Q , K ,$ and V vectors projections are obtained as

$$
Q = \widetilde {H} W _ {Q}, \quad K = \widetilde {H} W _ {K}, \quad V = \widetilde {H} W _ {V},\tag{13}
$$

where $W _ { Q } , W _ { K } , W _ { V } \in \mathbb { R } ^ { d \times d _ { k } }$ are learnable matrices, $d _ { k }$ is the per-head dimension. RoPE is applied to $Q$ and K vectors to encode relative positional information. The attention weights are computed by scaled dot-product attention:

$$
A = \text { softmax } \left(\frac {Q K ^ {\top}}{\sqrt {d _ {k}}}\right),\tag{14}
$$

the aggregated context is then projected back:

$$
U = A V W _ {O},\tag{15}
$$

where $W _ { O } ~ \in ~ \mathbb { R } ^ { d _ { k } \times d }$ is the output projection. A residual connection [51] adds the attention output to the input:

$$
\hat {H} = H ^ {(\ell - 1)} + U.\tag{16}
$$

3) Feed Forward Network (FFN): The FFN further transforms each token independently through a two-layer gated multilayer perceptron (MLP) with activation σ(·):

$$
\operatorname{FFN} (z) = W _ {2} \sigma \left(W _ {1} z\right) + b _ {2},\tag{17}
$$

where z represents the input of FFN layer, $W _ { 1 } ~ \in ~ \mathbb { R } ^ { d _ { \mathrm { f f } } \times d }$ and $W _ { 2 } ~ \in ~ \mathbb { R } ^ { d \times d _ { \mathrm { f f } } }$ are learnable projection matrices, $d _ { \mathrm { f f } }$ is the intermediate feed-forward dimension (typically 4d), and $b _ { 2 } \in \mathbb { R } ^ { d }$ is a bias vector.

Output Layer. $H ^ { ( \ell ) }$ obtained after all transformer blocks is normalized by an RMSNorm layer and linearly projected to the prediction space $\mathcal { V }$ to produce the student logits:

$$
\mathbf {o} = W _ {\mathrm{cls}} \operatorname{RMSNorm} \left(H ^ {(\ell)}\right) + b _ {\mathrm{cls}},\tag{18}
$$

TABLE II  
STATISTICS OF EXPERIMENT DATASETS

<table><tr><td>Dataset</td><td>#Flows</td><td>Task</td><td>#Labels</td></tr><tr><td>USTC-TFC [52]</td><td>489,139</td><td>Encrypted Malware Classification</td><td>20</td></tr><tr><td>ISCX-VPN [53]</td><td>311,390</td><td>Encrypted App Classification</td><td>17</td></tr><tr><td>CIC IoT [54]</td><td>1,163,495</td><td>IoT Attack Detection</td><td>7</td></tr></table>

where $W _ { \mathrm { c l s } } \in \mathbb { R } ^ { | \mathcal { V } | \times d }$ and $b _ { \mathrm { c l s } } \in \mathbb { R } ^ { | \mathcal { V } | }$ are learnable parameters. The resulting probability distribution over trafic classes is computed using a softmax function:

$$
P _ {\theta} (y = c \mid \hat {x}) = \frac {\exp (\mathbf {o} _ {c})}{\sum_ {j \in \mathcal {Y}} \exp (\mathbf {o} _ {j})}.\tag{19}
$$

Optimization Objective. The student model is trained to match its predictive distribution $P _ { \theta } ( y \mid \hat { x } )$ to the unified teacher model predictive distribution $q ( y \mid x )$ . This alignment is achieved by minimizing the cross-entropy loss:

$$
\mathcal {L} _ {\mathrm{CE}} = - \sum_ {c \in \mathcal {Y}} q (c \mid x) \log P _ {\theta} (y = c \mid \hat {x}).\tag{20}
$$

## V. EXPERIMENTS

We conduct extensive experiments to assess the M2ML framework. This section covers: (A) experimental setup, (B) evaluation of the M2ML framework, (C) comparison with ensemble learning, (D) comparison with knowledge distillation, (E) influence of the number of teacher models, (F) ablation study, and (G) additional experiments.

## A. Experimental Setup

1) Datasets: We select three publicly available encrypted trafic datasets that cover a range of typical scenarios, including commonly used encrypted communication protocols (e.g., HTTPS, TLS), virtual private network (VPN) tunneling, and IoT environments. Table II summarizes the statistics of the dataset size and trafic categories.

2) Teacher Model Selection and Configuration: We select AppScanner [55], CUMUL [56], BIND [57], and RDP [58] as teacher models based on three criteria: representativeness, diversity of feature spaces, and reproducibility. These models cover diferent ETA scenarios and capture diferent observable trafic patterns, including flow-level statistics, cumulative packet-sequence patterns, bidirectional burst dependence, and peak-level timing statistics. This selection provides a representative, feature-diverse, and reproducible teacher set for evaluating the proposed M2ML framework. Table III summarizes the feature settings and model configurations of the selected teacher models.

3) Evaluation Metrics: To evaluate the overall trafic classification performance, we adopt standard metrics including Accuracy (AC) and F1. These are defined as follows:

$$
\mathrm{AC} = \frac {T P + T N}{T P + T N + F P + F N}\tag{21}
$$

$$
\mathrm{PR} = \frac {T P}{T P + F P}\tag{22}
$$

$$
\mathrm{RE} = \frac {T P}{T P + F N}\tag{23}
$$

$$
\mathrm{F} 1 = \frac {2 \times \mathrm{PR} \times \mathrm{RE}}{\mathrm{PR} + \mathrm{RE}}\tag{24}
$$

Here, T P, T N, FP, and FN denote true positives, true negatives, false positives, and false negatives, respectively. precision (PR) reflects the correctness of positive predictions, recall (RE) reflects the coverage of actual positives, and the F1 balances both.

4) Implementation Details: All experiments are conducted on a single NVIDIA A100 GPU and implemented using the PyTorch 2.3 framework. We adopt Qwen2-7B [59] as the student model and apply parameter-eficient fine-tuning based on the LoRA method [60].

The student model takes the textualized trafic representation generated by FNEI as input, where each sample consists of a task instruction, a task identifier, and the corresponding textual feature description. The output space of the student model is defined according to the trafic classes of each dataset. A linear classification head is attached to the final hidden representation of the backbone to produce student logits, which are then normalized by a softmax function. The student model is optimized to match the CCWA-generated soft target distribution rather than the manually annotated ground-truth labels.

We use the Adam optimizer with an initial learning rate of 1e-4 and a weight decay of 0.01. Each task is trained with a batch size of 64 for a maximum of 10 epochs. All reported results are evaluated using the model checkpoint that achieves the best performance on the validation set.

We apply LoRA adaptation to the feed-forward layers with a low-rank dimension $r \ = \ 8 .$ During fine-tuning, the original Qwen2-7B parameters are frozen, and only the LoRA parameters and the classification head are updated.

## B. Evaluation of the M2ML Framework

To evaluate the efectiveness of the proposed M2ML framework, we use the four heterogeneous ETA teacher models summarized in Table III. For each dataset, we perform a stratified 8:1:1 split into training, validation, and test datasets. Within the training dataset, we generate out-of-fold (OOF) teacher models’ predictions using K-fold cross-validation $( \mathrm { K } \mathrm { = } 5 )$ : the training dataset is partitioned into $\{ F _ { 1 } , . . . , F _ { K } \} ;$ for each fold $F _ { j } ,$ , all four teacher models are trained on $\textstyle \bigcup _ { i \neq j } F _ { i }$ and produce class predictions on the held-out $F _ { j } .$ Concatenating the per-fold outputs yields OOF predictions for the entire training dataset, ensuring no leakage. We then fuse the four teacher models’ predictions using CCWA to obtain consensus targets for the student model. The student model is trained only on the training dataset to match these CCWA consensus targets (no manually annotated labels are used). To ensure fairness, all methods share identical data splits and preprocessing; teacher models are never trained or fine-tuned on the validation or test datasets.

1) Experimental Results on USTC-TFC: The USTC-TFC dataset focuses on encrypted malware trafic classification, containing 489,139 flows and 20 categories (covering typical malicious trafic types such as ransomware and botnets). The core challenge of this dataset lies in the high feature overlap between diferent malicious trafic variants. As shown in Table IV, AppScanner relies on statistical features of flow bursts (e.g., packet length quantiles, bidirectional trafic variance) and a random forest classifier. It excels at capturing malicious behavior patterns in encrypted trafic, achieving an accuracy of 88.74% and an F1 of 89.07%; CUMUL focuses on the cumulative distribution characteristics of encrypted trafic packet sequences but has limited generalization ability to malicious trafic variants, with an accuracy of 87.41% and an F1 of 86.33%; BIND is based on bidirectional dependence features (Bi-Burst size and time tuples), however, its high feature dimensionality and inadequate adaptation to specific behavior patterns of malicious trafic result in weak generalization performance, with an F1 of only 77.18%; RDP depends on statistical moments of flow bursts and port interaction features, which is more suitable for remote operation trafic but insuficient in comprehensively capturing behavior patterns of malicious trafic, achieving an accuracy of 82.32% and an F1 of 83.16%.

TABLE III  
TEACHER MODEL CONFIGURATION

<table><tr><td>Teacher</td><td>Feature Setting</td><td>Model Configuration</td></tr><tr><td>AppScanner</td><td>Flow-level packet-length statistical features</td><td>Random Forest</td></tr><tr><td>CUMUL</td><td>Cumulative packet-sequence features</td><td>Gradient Boosting Decision Tree</td></tr><tr><td>BIND</td><td>Bidirectional burst-dependence features</td><td>Support Vector Machine</td></tr><tr><td>RDP</td><td>Peak-level packet-length and timing statistical features</td><td>Logistic Regression</td></tr></table>

TABLE IV

PERFORMANCE COMPARISON BETWEEN THE M2ML FRAMEWORK AND TEACHER MODELS ON USTC-TFC

<table><tr><td>Method</td><td>Accuracy(%)</td><td>Precision(%)</td><td>Recall(%)</td><td>F1(%)</td></tr><tr><td>AppScanner</td><td>88.74</td><td>92.80</td><td>87.62</td><td>89.07</td></tr><tr><td>CUMUL</td><td>87.41</td><td>87.80</td><td>85.83</td><td>86.33</td></tr><tr><td>BIND</td><td>80.97</td><td>83.07</td><td>76.92</td><td>77.18</td></tr><tr><td>RDP</td><td>82.32</td><td>87.73</td><td>83.67</td><td>83.16</td></tr><tr><td>M2ML</td><td>92.50</td><td>92.99</td><td>90.96</td><td>91.77</td></tr></table>

TABLE V

PERFORMANCE COMPARISON BETWEEN THE M2ML FRAMEWORK AND TEACHER MODELS ON ISCX-VPN

<table><tr><td>Method</td><td>Accuracy(%)</td><td>Precision(%)</td><td>Recall(%)</td><td>F1(%)</td></tr><tr><td>AppScanner</td><td>77.78</td><td>68.32</td><td>69.76</td><td>68.23</td></tr><tr><td>CUMUL</td><td>79.23</td><td>72.62</td><td>71.57</td><td>70.03</td></tr><tr><td>BIND</td><td>68.60</td><td>69.59</td><td>68.60</td><td>66.36</td></tr><tr><td>RDP</td><td>88.65</td><td>85.98</td><td>83.42</td><td>84.52</td></tr><tr><td>M2ML</td><td>89.13</td><td>86.32</td><td>84.08</td><td>85.05</td></tr></table>

The proposed M2ML framework achieves an accuracy of 92.50% and an F1 of 91.77% on this dataset, representing improvements of 3.76 percentage points (PP) and 2.70 PP, respectively, compared to the best teacher model. The performance gain arises from the combined efect of the dual mechanisms, FNEI and CCWA.

2) Experimental Results on ISCX-VPN: The ISCX-VPN dataset is used for encrypted application classification, containing 311,390 flows and 17 categories (covering application types such as video streaming, instant messaging, and VPN tunneling). The key dificulty of this dataset is the high feature similarity between VPN tunnel trafic and regular application trafic. As shown in Table V, RDP excels at capturing port interaction features and burst time patterns of remote access applications, and accurately identifies port mapping relationships of VPN tunnel trafic, achieving an accuracy of 88.65% and an F1 of 84.52%; AppScanner is based on statistical features of application-layer trafic, which performs well in identifying instant messaging applications but has insuficient adaptation to trafic camouflage behavior of VPN tunnels, with an accuracy of 77.78% and an F1 of 68.23%; CUMUL has inadequate adaptation to the long-connection characteristics of VPN trafic, with an accuracy of 79.23% and an F1 of 70.03%; BIND’s bidirectional dependence features have poor adaptability to the trafic patterns of VPN protocols, and feature redundancy leads to insuficient ability to distinguish similar applications, with an F1 of only 66.36%.

TABLE VI  
PERFORMANCE COMPARISON BETWEEN THE M2ML FRAMEWORK AND TEACHER MODELS ON CIC IOT

<table><tr><td>Method</td><td>Accuracy(%)</td><td>Precision(%)</td><td>Recall(%)</td><td>F1(%)</td></tr><tr><td>AppScanner</td><td>64.03</td><td>62.89</td><td>46.94</td><td>50.81</td></tr><tr><td>CUMUL</td><td>63.84</td><td>61.92</td><td>48.43</td><td>51.85</td></tr><tr><td>BIND</td><td>83.40</td><td>87.83</td><td>79.62</td><td>81.51</td></tr><tr><td>RDP</td><td>61.84</td><td>65.49</td><td>41.48</td><td>44.15</td></tr><tr><td>M2ML</td><td>83.79</td><td>90.24</td><td>80.07</td><td>82.42</td></tr></table>

The M2ML framework achieves an accuracy of 89.13% and an F1 of 85.05% on this dataset, improving by 0.48 and 0.53 PP in precision and recall, respectively, compared to the best teacher model. Meanwhile, it also achieves improvements in precision (86.32%) and recall (84.08%).

3) Experimental Results on CIC IoT: The CIC IoT dataset focuses on IoT attack detection, containing 1,163,495 flows and 7 categories (covering typical IoT attacks such as DoS attacks and data exfiltration). The unique challenge of this dataset is that most IoT attack trafic has simplistic features (e.g., fixed packet transmission frequency and unchanged port interaction patterns for DoS attacks). As shown in Table VI, BIND’s bidirectional dependence features have good adaptability to the low-bandwidth and short-connection trafic patterns of IoT devices, and can efectively capture burst interaction features of attack trafic, thus becoming the best teacher model with an accuracy of 83.40% and an F1 of 81.51%; AppScanner’s statistical features have insuficient robustness to the heterogeneity of IoT devices (e.g., trafic diferences between sensors and controllers) and limited ability to identify low-trafic-intensity attacks, with an accuracy of 64.03% and an F1 of 50.81%; CUMUL’s cumulative trafic features are not sensitive enough to capture the burstiness of IoT attacks and have inadequate adaptation to device type diferences, with an accuracy of 63.84% and an F1 of 51.85%; RDP’s core features are statistical moments of remote operation trafic, which cannot efectively identify attack patterns unique to IoT scenarios, resulting in an F1 of only 44.15

TABLE VII  
PERFORMANCE COMPARISON BETWEEN THE M2ML FRAMEWORK AND ENSEMBLE LEARNING ON USTC-TFC

<table><tr><td>Method</td><td>Accuracy(%)</td><td>Precision(%)</td><td>Recall(%)</td><td>F1(%)</td></tr><tr><td>AppScanner</td><td>88.74</td><td>92.80</td><td>87.62</td><td>89.07</td></tr><tr><td>CUMUL</td><td>87.41</td><td>87.80</td><td>85.83</td><td>86.33</td></tr><tr><td>BIND</td><td>80.97</td><td>83.07</td><td>76.92</td><td>77.18</td></tr><tr><td>RDP</td><td>82.32</td><td>87.73</td><td>83.67</td><td>83.16</td></tr><tr><td>EL (Voting)</td><td>86.13</td><td>85.47</td><td>73.66</td><td>74.82</td></tr><tr><td>EL (Averaging)</td><td>87.34</td><td>86.51</td><td>78.10</td><td>78.02</td></tr><tr><td>M2ML</td><td>92.50</td><td>92.99</td><td>90.96</td><td>91.77</td></tr></table>

TABLE VIII

PERFORMANCE COMPARISON BETWEEN THE M2ML FRAMEWORK AND ENSEMBLE LEARNING ON ISCX-VPN

<table><tr><td>Method</td><td>Accuracy(%)</td><td>Precision(%)</td><td>Recall(%)</td><td>F1(%)</td></tr><tr><td>AppScanner</td><td>77.78</td><td>68.32</td><td>69.76</td><td>68.23</td></tr><tr><td>CUMUL</td><td>79.23</td><td>72.62</td><td>71.57</td><td>70.03</td></tr><tr><td>BIND</td><td>68.60</td><td>69.59</td><td>68.60</td><td>66.36</td></tr><tr><td>RDP</td><td>88.65</td><td>85.98</td><td>83.42</td><td>84.52</td></tr><tr><td>EL (Voting)</td><td>82.61</td><td>76.91</td><td>74.62</td><td>74.80</td></tr><tr><td>EL (Averaging)</td><td>85.51</td><td>80.26</td><td>79.02</td><td>79.01</td></tr><tr><td>M2ML</td><td>89.13</td><td>86.32</td><td>84.08</td><td>85.05</td></tr></table>

The M2ML framework achieves an accuracy of 83.79% and an F1 of 82.42% on this dataset, improving by 0.39 and 0.91 PP, respectively, compared to the best teacher model. Although the magnitude of improvement is smaller than that on other datasets, it holds significant value in practical IoT scenarios. A comprehensive analysis of the experimental results across the three datasets reveals that, although the four teacher models each have their advantages, they all have limitations in scenario adaptation (e.g., RDP is suitable for remote operation trafic, and BIND is suitable for IoT short-connection trafic). However, through FNEI and CCWA, the M2ML framework surpasses the performance of the best teacher model under the condition of no manually labeled data.

## C. Comparison With Ensemble Learning (EL)

Two EL baselines were evaluated to compare with the proposed M2ML framework: (1) EL (Voting), which adopts a majority-voting strategy based on the categorical decisions of all teacher models, and (2) EL (Averaging), which linearly averages the predicted probability distributions from multiple teachers.

Tables VII–IX show that the two EL baselines, EL (Voting) and EL (Averaging), behave diferently across the three datasets and are consistently inferior to the M2ML framework. On USTC-TFC and ISCX-VPN, where the performance gap among teacher models is relatively small, majority voting or probability averaging can partially approach the strongest teacher model but never surpass it. The core reason is that both EL variants perform only shallow aggregation at the output layer, neither distinguishing teacher models’ reliability nor exploiting complementary feature representations. On CIC IoT, teacher model performance diverges markedly (only BIND reaches 83.40% accuracy, while the others are around 60%), and both EL methods degrade toward the weak teacher models. In contrast, despite three weak teacher models, the M2ML framework still surpasses the strongest teacher model, reaching 83.79% accuracy.

TABLE IX  
PERFORMANCE COMPARISON BETWEEN THE M2ML FRAMEWORK AND ENSEMBLE LEARNING ON CIC IOT

<table><tr><td>Method</td><td>Accuracy(%)</td><td>Precision(%)</td><td>Recall(%)</td><td>F1(%)</td></tr><tr><td>AppScanner</td><td>64.03</td><td>62.89</td><td>46.94</td><td>50.81</td></tr><tr><td>CUMUL</td><td>63.84</td><td>61.92</td><td>48.43</td><td>51.85</td></tr><tr><td>BIND</td><td>83.40</td><td>87.83</td><td>79.62</td><td>81.51</td></tr><tr><td>RDP</td><td>61.84</td><td>65.49</td><td>41.48</td><td>44.15</td></tr><tr><td>EL (Voting)</td><td>62.93</td><td>63.93</td><td>62.93</td><td>58.72</td></tr><tr><td>EL (Averaging)</td><td>63.39</td><td>65.32</td><td>63.39</td><td>58.96</td></tr><tr><td>M2ML</td><td>83.79</td><td>90.24</td><td>80.07</td><td>82.42</td></tr></table>

The EL baselines aggregate only the final outputs (votes or averaged probabilities) and thus fail to account for (i) the heterogeneity of encrypted trafic features across teacher models and (ii) pronounced diferences in teacher model reliability. By comparison, the M2ML framework overcomes these bottlenecks via FNEI and CCWA: FNEI aligns heterogeneous teacher model trafic feature representations to a semantic space, reducing cross-feature fusion barriers; CCWA introduces both a global reliability weight and a sample-wise consensus weight, and adaptively fuses teacher models accordingly, amplifying high-reliability knowledge while suppressing conflicts and biases.

Across all three datasets, the M2ML framework outperforms both EL baselines and surpasses the strongest single-teacher model, demonstrating superior cross-model knowledge fusion. Crucially, the M2ML framework operates without manually labeled data. Through the combined efect of FNEI and CCWA, it simultaneously addresses heterogeneous trafic feature alignment and reliability imbalances among teacher models, demonstrating practical value for label-free encrypted trafic scenarios such as IoT attack detection and VPN application recognition.

## D. Comparison With Knowledge Distillation (KD)

We further compare the proposed M2ML framework with the KD approach. In this experiment, KD utilizes the highestperforming single-teacher model on each trafic dataset as the knowledge source. Specifically, AppScanner, CUMUL, BIND, and RDP serve as candidate teacher models, and the one achieving the highest validation performance on each trafic dataset is selected as the best teacher.

Across Tables X–XII, the proposed M2ML framework consistently outperforms the label-free KD baseline on all three datasets. Specifically, the M2ML framework improves over KD by +8.20 pp accuracy and +14.85 pp F1 on USTC-TFC, by +6.76 pp accuracy and +11.11 pp F1 on ISCX-VPN, and by +6.89 pp accuracy and +5.08 pp F1 on CIC IoT. These results demonstrate that relying on a single teacher model’s predictions provides limited supervisory information under label-free settings, whereas aggregating multiple heterogeneous teachers yields richer and more stable guidance for student learning.

TABLE X  
PERFORMANCE COMPARISON BETWEEN THE M2ML FRAMEWORK AND KNOWLEDGE DISTILLATION ON USTC-TFC

<table><tr><td>Method</td><td>Accuracy(%)</td><td>Precision(%)</td><td>Recall(%)</td><td>F1(%)</td></tr><tr><td>AppScanner</td><td>88.74</td><td>92.80</td><td>87.62</td><td>89.07</td></tr><tr><td>CUMUL</td><td>87.41</td><td>87.80</td><td>85.83</td><td>86.33</td></tr><tr><td>BIND</td><td>80.97</td><td>83.07</td><td>76.92</td><td>77.18</td></tr><tr><td>RDP</td><td>82.32</td><td>87.73</td><td>83.67</td><td>83.16</td></tr><tr><td>KD</td><td>84.30</td><td>78.32</td><td>76.45</td><td>76.92</td></tr><tr><td>M2ML</td><td>92.50</td><td>92.99</td><td>90.96</td><td>91.77</td></tr></table>

TABLE XI

PERFORMANCE COMPARISON BETWEEN THE M2ML FRAMEWORK AND KNOWLEDGE DISTILLATION ON ISCX-VPN

<table><tr><td>Method</td><td>Accuracy(%)</td><td>Precision(%)</td><td>Recall(%)</td><td>F1(%)</td></tr><tr><td>AppScanner</td><td>77.78</td><td>68.32</td><td>69.76</td><td>68.23</td></tr><tr><td>CUMUL</td><td>79.23</td><td>72.62</td><td>71.57</td><td>70.03</td></tr><tr><td>BIND</td><td>68.60</td><td>69.59</td><td>68.60</td><td>66.36</td></tr><tr><td>RDP</td><td>88.65</td><td>85.98</td><td>83.42</td><td>84.52</td></tr><tr><td>KD</td><td>82.37</td><td>75.10</td><td>73.63</td><td>73.94</td></tr><tr><td>M2ML</td><td>89.13</td><td>86.32</td><td>84.08</td><td>85.05</td></tr></table>

TABLE XII

PERFORMANCE COMPARISON BETWEEN THE M2ML FRAMEWORK AND KNOWLEDGE DISTILLATION ON CIC IOT

<table><tr><td>Method</td><td>Accuracy(%)</td><td>Precision(%)</td><td>Recall(%)</td><td>F1(%)</td></tr><tr><td>AppScanner</td><td>64.03</td><td>62.89</td><td>46.94</td><td>50.81</td></tr><tr><td>CUMUL</td><td>63.84</td><td>61.92</td><td>48.43</td><td>51.85</td></tr><tr><td>BIND</td><td>83.40</td><td>87.83</td><td>79.62</td><td>81.51</td></tr><tr><td>RDP</td><td>61.84</td><td>65.49</td><td>41.48</td><td>44.15</td></tr><tr><td>KD</td><td>76.90</td><td>81.12</td><td>76.82</td><td>77.34</td></tr><tr><td>M2ML</td><td>83.79</td><td>90.24</td><td>80.07</td><td>82.42</td></tr></table>

Our KD baseline does not access manually labeled data. In this setting, supervision is bounded by the teacher model’s noise and calibration, and error patterns tend to propagate to the student model. Consequently, surpassing the teacher model is uncommon in practice. Moreover, KD cannot exploit complementary trafic features, nor does it ofer a mechanism to discount unreliable predictions on a per-sample basis.

The M2ML framework addresses these limitations by FNEI and CCWA. This reliability- and consensus-aware fusion enables multiple weaker yet complementary teacher models to collectively surpass the strongest single teacher model, demonstrating that aggregated weak teacher models can provide stronger guidance than any individual teacher model.

## E. Influence of the Number of Teacher Models

To investigate how the number of teacher models influences the performance of the M2ML framework, we progressively integrate one to four heterogeneous teacher models (AppScanner, CUMUL, BIND, and RDP) and report both AC and F1 on three encrypted trafic datasets in Fig. 3.

From Fig. 3, both AC and F1 exhibit a consistent nonmonotonic pattern: performance decreases when increasing from one to two teacher models, but improves as more teacher models are introduced. The initial decline can be attributed to decision conflicts among heterogeneous teacher models, where contradictory predictions for the same flow introduce noise and weaken the student model’s ability to learn.

![](images/c9c7c6a8e2887a25da1a59b9ab6004b5515fc70dc499db1d9f0a58fa76cbc9f5.jpg)

![](images/539087f3240b1f6f2acaa16fe2a386ffc98d18496d9512aad413f67d75a6c758.jpg)

![](images/d59914ef8ab09517981a6b566f2ec0f972996cc3b8d513a9121b02d6250f42f0.jpg)

![](images/aac7fdeb02951588f290ed2befa3e47883474e2355ad88e580515ea300b168cc.jpg)

![](images/3b7100d40f732a19373f5982ca19b50da6f5d4514e20b07936aa025942eda0e6.jpg)

![](images/c1a887fb6a9bf1f63cae8d6d961b7ff65cc3490b42af57cf687bf61c9db54deb.jpg)  
Fig. 3. Efect of teacher model quantity on the performance of the M2ML framework across three datasets.

TABLE XIII  
ABLATION OF FNEI AND CCWA ACROSS THREE TRAFFIC DATASETS

<table><tr><td rowspan="2">Method</td><td colspan="2">USTC-TFC</td><td colspan="2">ISCX-VPN</td><td colspan="2">CIC IoT</td></tr><tr><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td></tr><tr><td>M2ML</td><td>92.50</td><td>91.77</td><td>89.13</td><td>85.05</td><td>83.79</td><td>82.42</td></tr><tr><td>w/o FNEI</td><td>67.05</td><td>63.64</td><td>69.25</td><td>62.47</td><td>63.23</td><td>60.40</td></tr><tr><td>w/o CCWA</td><td>86.08</td><td>75.63</td><td>83.09</td><td>77.73</td><td>63.01</td><td>58.92</td></tr></table>

As the number of teacher models increases beyond two, the M2ML framework gradually stabilizes and achieves substantial gains. This improvement stems from the CCWA mechanism, whose mode-seeking geometric aggregation suppresses unreliable predictions and amplifies consistent ones, enabling the student model to efectively leverage the collective knowledge of multiple teacher models.

## F. Ablation Study

To quantitatively assess the contribution of each core mechanism, we conduct a comprehensive ablation study focusing on two critical components of the M2ML framework: (1) FNEI and (2) CCWA. All other configurations remain identical to the default setting, and the results are reported in Table XIII.

Removing FNEI causes the most substantial degradation, with average decreases of approximately 22 pp in accuracy and 24 pp in F1 across all three datasets. This highlights the importance of FNEI in constructing a shared semantic representation space that aligns heterogeneous trafic features and facilitates the efective fusion of knowledge between crossteacher models. Removing CCWA results to a reduction of approximately 11 pp in accuracy and 16 pp in F1, confirming that credibility- and consensus-aware arbitration is crucial for mitigating decision conflicts among heterogeneous teacher models. Overall, the complete configuration achieves the best and most stable performance, validating the roles of FNEI and CCWA in the M2ML framework.

![](images/f48cec3f6ee09be13a6a90dd42734dc5abc8327ec79112a2844ec86aa25d2937.jpg)  
Fig. 4. Performance comparison of the M2ML student with deep learningbased teacher models.

![](images/8ccf444da7d242792bb2b26211495b97b556a36c8f17566b546dfb724105ccaa.jpg)  
Fig. 5. Performance comparison of diferent student architectures under the same heterogeneous teacher setting.

## G. Additional Experiments

1) Extension to Deep Learning-Based Teacher Models: To examine whether M2ML can be extended to deep learningbased ETA teachers, we conduct an additional experiment with four representative models, namely ET-BERT [61], YaTC [62], TraficFormer [63], and RBLJAN [64]. Unlike the teacher models based on handcrafted trafic features in the main experiments, these models mainly learn from raw bytes, packet-token sequences, or high-dimensional latent traffic representations. Each deep learning-based model is used as an individual teacher source, and the resulting student performance is reported separately.

As shown in Fig. 4, the student model achieves limited performance when directly learning from these deep learningbased teacher models. Across the three datasets, the accuracy ranges from 41.75% to 49.15%, and F1 score from 40.90% to 48.40%. Among the evaluated teachers, RBLJAN leads to the best average student performance, with an average accuracy of 48.40% and an average F1 score of 47.62%. Nevertheless, the overall performance remains clearly lower than that obtained with the teacher models in the main experiments.

These results indicate that the FNEI mechanism is not suficient for learning knowledge from deep learning-based ETA teachers that rely on raw bytes, packet-token sequences, or latent trafic representations. Directly serializing such representations into textual tokens may weaken structural information such as byte order, packet boundaries, temporal dependencies, or latent feature interactions. As a result, the LLM-based student has dificulty efectively acquiring teacher knowledge from these models.

2) Diferent Student Architectures: To further evaluate the role of the student architecture in heterogeneous teacherknowledge integration, we compare the proposed LLM-based student with four conventional neural architectures, including CNN, RNN, LSTM, and Transformer.

As shown in Fig. 5, conventional student architectures achieve limited performance under the heterogeneous multiteacher setting. Among them, the Transformer-based student performs the best, obtaining accuracies of 86.10%, 85.60%, and 79.85% on USTC-TFC, ISCX-VPN, and CIC IoT, respectively, with corresponding F1 scores of 85.70%, 84.95%, and 78.20%. The average accuracies of CNN, RNN, LSTM, and Transformer are 79.68%, 78.82%, 81.83%, and 83.85%, respectively, while their average F1 scores are 79.67%, 78.75%, 81.40%, and 82.95%, respectively. Although the Transformer student performs better than CNN, RNN, and LSTM, its overall performance is still lower than that of the proposed LLM-based student in the main experiments.

These results indicate that conventional neural architectures have dificulty learning from heterogeneous ETA teachers. Since diferent teachers characterize encrypted traffic from diferent perspectives, CNN-, RNN-, LSTM-, and Transformer-based students typically need to project and fuse heterogeneous trafic features into a unified feature space. However, this process may obscure the specific interpretation of trafic behavior captured by each teacher and weaken the complementarity among teachers. In contrast, the LLMbased student provides a unified textual representation for representing heterogeneous trafic features, making it more suitable for integrating knowledge from heterogeneous ETA teachers.

3) Diferent Student Backbone Sizes and Eficiency: To analyze the impact of student model scale and computational cost, we evaluate the M2ML framework with diferent backbone sizes, including Qwen2-0.5B, Qwen2-1.5B, Qwen2-7B, and Qwen2.5-14B. All backbone variants are trained with the same data splits and LoRA-based fine-tuning settings. In addition to AC and F1, we report the number of trainable parameters, GPU memory consumption, and inference time. The results are summarized in Table XIV.

As shown in Table XIV, smaller backbones are more computationally eficient but provide limited performance for heterogeneous teacher-knowledge integration. Qwen2-0.5B and Qwen2-1.5B require only 2.3M and 4.5M trainable parameters, respectively, but their performance is substantially lower than that of Qwen2-7B across all three datasets. When the backbone size increases to Qwen2-7B, the average AC and F1 improve to 88.47% and 86.41%, respectively, corresponding to gains of 9.73 pp and 9.49 pp over Qwen2-1.5B. However, further increasing the backbone size from Qwen2-7B to Qwen2.5-14B [65] brings only marginal performance gains while introducing much higher computational cost.

These results reveal a clear accuracy-eficiency trade-of: larger backbones can improve the capacity of the student model, but excessive scaling introduces substantially higher computational cost with limited performance benefit.

## VI. DISCUSSION

Although the proposed M2ML framework demonstrates promising performance in learning from multiple heterogeneous ETA teacher models, several limitations remain and deserve further investigation.

## A. Representation of Teacher Knowledge

The efectiveness of the M2ML framework depends on whether the knowledge of teacher models can be adequately exposed to the LLM-based student through FNEI. As shown in the additional experiments, teacher models based on handcrafted trafic features are more suitable for the current FNEI design, because their features usually have clear semantic meaning, such as packet length, burst behavior, and timing statistics. In contrast, deep learning-based teachers that rely on raw bytes, packet-token sequences, or latent trafic representations are more dificult for the student to learn from through direct textualization. This is because important structural information, such as byte order and packet boundaries, may not be well preserved when converted into textual tokens. Future work should explore more efective mapping mechanisms between raw trafic representations and textual semantics, enabling the student model to better acquire knowledge from such teachers.

TABLE XIV  
PERFORMANCE COMPARISON UNDER DIFFERENT BACKBONE SIZES

<table><tr><td rowspan="2">Backbone Size</td><td colspan="2">USTC-TFC</td><td colspan="2">ISCX-VPN</td><td colspan="2">CIC IoT</td><td rowspan="2">Trainable Params (M)</td><td rowspan="2">GPU (GB)</td><td rowspan="2">Inference (second)</td></tr><tr><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td></tr><tr><td>Qwen2-0.5B</td><td>76.50</td><td>76.20</td><td>75.25</td><td>72.30</td><td>69.90</td><td>68.50</td><td>2.3</td><td>2.3</td><td>7.8</td></tr><tr><td>Qwen2-1.5B</td><td>83.60</td><td>82.30</td><td>79.15</td><td>75.37</td><td>73.46</td><td>73.08</td><td>4.5</td><td>5.1</td><td>8.9</td></tr><tr><td>Qwen2-7B</td><td>92.50</td><td>91.77</td><td>89.13</td><td>85.05</td><td>83.79</td><td>82.42</td><td>10.1</td><td>16.5</td><td>12.0</td></tr><tr><td>Qwen2.5-14B</td><td>92.55</td><td>91.80</td><td>89.88</td><td>86.63</td><td>83.63</td><td>82.71</td><td>25.2</td><td>32.0</td><td>18.8</td></tr></table>

## B. Dependence on Teacher Knowledge

The M2ML framework does not rely on manually labeled data for the student model, but it relies on the knowledge provided by existing teacher models. Therefore, the quality, calibration, and reliability of teacher models directly afect the performance of the student model. If a teacher model provides biased, noisy, or incorrect predictions, the student may inherit such erroneous knowledge. Although CCWA considers both global credibility and sample-level consensus to reduce the influence of unreliable predictions, it cannot fully eliminate systematic teacher errors, especially when multiple teachers make similar mistakes or when a high-credibility teacher is wrong on specific samples. Moreover, once incorrect teacher knowledge has been absorbed by the student, correcting it without retraining remains challenging. Future work should incorporate knowledge editing mechanisms to identify and revise unreliable teacher knowledge more eficiently.

## C. Scalability and Eficiency

In this work, LoRA-based fine-tuning reduces the number of trainable parameters and improves the training eficiency of the student model. Nevertheless, the M2ML framework still relies on an LLM-based student during inference, which introduces non-negligible inference costs. As shown in Table XIV, scaling the student backbone from Qwen2-7B to Qwen2.5-14B brings only marginal performance gains, while requiring substantially higher GPU memory and longer inference time. This result indicates that the scalability of the M2ML framework is constrained by inference eficiency, especially in real-time or resource-constrained network-security environments. Future work should explore model quantization, pruning, compression, and inference acceleration techniques to reduce such costs while preserving the knowledge integration capability.

## VII. THEORETICAL ANALYSIS

To further interpret the quantitative improvements observed in our experiments, we provide a theoretical analysis of both FNEI and CCWA.

## A. Efect of FNEI: Semantic Prior Injection and Conditional Entropy Reduction

Removing FNEI forces the student model to directly align heterogeneous numerical trafic features extracted by diferent teacher models. Since these feature spaces are inconsistent and difer in scale, dimensionality, and semantic expressiveness, they make it dificult for the student model to efectively acquire knowledge from heterogeneous teacher models.

FNEI alleviates this issue by converting these heterogeneous trafic features into unified textual descriptions, thereby introducing structured semantic priors that constrain the semantic interpretation of trafic features.

Formally, let X denote the heterogeneous numerical trafic features, U the semantic priors provided by the FNEI templates, and $\hat { X } = \Phi ( X , U )$ the textualized representation. Note that X<sup>ˆ</sup> is a deterministic function of (X U), and thus conditioning on (X U) is equivalent to conditioning on X<sup>ˆ</sup> in terms of available information. Let Y denote the consensus predictive distribution produced by the teacher models. According to the definition of conditional mutual information [66],

$$
I _ {q} (Y; U \mid X) = H _ {q} (Y \mid X) - H _ {q} (Y \mid X, U).\tag{25}
$$

Since $I _ { q } ( Y ; U \mid X ) \geq 0$ , we have

$$
H _ {q} (Y \mid X, U) \leq H _ {q} (Y \mid X),\tag{26}
$$

indicating that the semantic priors U reduce the conditional uncertainty of Y given X. This reduction in conditional uncertainty facilitates the teacher-knowledge acquisition process of the student model, enabling more efective cross-model knowledge fusion.

## B. Efect of CCWA: Mode-Seeking Consensus and Conflict Mitigation

Removing CCWA disrupts the decision fusion process across heterogeneous teacher models. Without CCWA, all teacher model predictions are treated equally, which introduces noise when heterogeneous teacher models disagree on the same trafic sample.

CCWA mitigates this issue by adaptively weighting each teacher model according to its global reliability and sample-level consensus.

Formally, let $\{ p _ { i } ( y \mid x _ { i } ) \} _ { i = } ^ { K }$ denote the teacher model predictive distributions and $w _ { i } ( \ell _ { \phi } )$ denote their arbitration weights. The consensus distribution $q ^ { \star }$ is obtained by minimizing the weighted reverse Kullback–Leibler divergence:

$$
q ^ {\star} = \arg \min _ {q} \sum_ {i = 1} ^ {K} w _ {i} (\ell_ {\phi}) \operatorname{KL} (q \| p _ {i}),\tag{27}
$$

whose unique solution is the normalized weighted geometric mean (Eq. 10). This mode-seeking aggregation emphasizes regions where teacher models agree and suppresses inconsistent predictions. In contrast, minimizing the forward KL divergence yields the linear opinion pool, equivalent to arithmetic averaging or majority voting, which is mean-seeking and tends to over-smooth disagreements.

By employing the reverse-KL formulation, CCWA adaptively balances reliability and consensus, producing a sharper and more informative fused supervisory distribution that efectively reduces decision conflicts and provides stronger guidance for the label-free student model learning.

## C. Joint Theoretical Insights

Together, FNEI and CCWA reduce input-level representation ambiguity and output-level conflict, respectively. These complementary efects explain why the full M2ML framework substantially outperforms variants that remove either mechanism: FNEI aligns heterogeneous feature spaces into a coherent semantic representation, while CCWA consolidates heterogeneous teacher model predictions into a reliability- and consensus-aware supervisory distribution. This dual stabilization of both inputs and outputs is fundamental to enabling efective model-level knowledge fusion in a fully label-free setting.

## VIII. CONCLUSION

In this paper, we address a practical yet underexplored problem in ETA: how to construct a unified model that learns directly from existing ETA models to perform efective ETA, without relying on manually labeled data. We propose the M2ML paradigm and instantiate it with an LLM-based framework guided by two principles. Knowledge Semantization is operationalized via FNEI, which textualizes heterogeneous trafic features to align input spaces. Credibility-First Arbitration is implemented by CCWA, which aggregates teacher models using global reliability and sample-level consensus to resolve predictive conflicts. Extensive experiments on three public encrypted trafic datasets demonstrate the efectiveness of the M2ML paradigm. These results confirm that model-centric learning can serve as a viable alternative to data-driven learning for ETA. Future research will focus on continual learning, enabling the student model to incrementally learn knowledge from newly available teacher models without retraining from scratch.

## REFERENCES

[1] J. Wu et al., “DLET-classifier: A dynamic and lightweight method for encrypted trafic classification,” IEEE Internet Things J., vol. 12, no. 20, pp. 42250–42262, Oct. 2025.

[2] J. Zhao et al., “ReTrial: Robust encrypted malicious trafic detection via discriminative relation incorporation and misleading relation correction,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 677–692, 2025.

[3] X. Wang, Q. Yuan, Y. Wang, J. Teng, J. Tao, and M. Shen, “Zero trust-driven collaborative intrusion detection in IoT: A continuous trust assessment approach,” IEEE Internet Comput., vol. 29, no. 4, pp. 37–47, Sep. 2025.

[4] M. Shen et al., “Real-time website fingerprinting defense via trafic cluster anonymization,” in Proc. IEEE Symp. Secur. Privacy (SP), May 2024, pp. 3238–3256.

[5] M. Shen, J. Zhang, L. Zhu, K. Xu, and X. Du, “Subverting website fingerprinting defenses with robust trafic representation,” in Proc. 32nd USENIX Secur. Symp., 2023, pp. 607–624.

[6] M. Lotfollahi, M. Jafari Siavoshani, R. Shirali Hossein Zade, and M. Saberian, “Deep packet: A novel approach for encrypted traffic classification using deep learning,” Soft Comput., vol. 24, no. 3, pp. 1999–2012, Feb. 2020.

[7] K. Chen et al., “Robust intrusion detection in CPS: A pre-trainingbased multi-view feature collaboration and correlation analysis method,” Comput. Netw., vol. 279, Apr. 2026, Art. no. 112129.

[8] P. Barford, J. Kline, D. Plonka, and A. Ron, “A signal analysis of network trafic anomalies,” in Proc. 2nd ACM SIGCOMM Workshop Internet Measurment (IMW), 2002, pp. 71–82.

[9] R. Sommer and V. Paxson, “Outside the closed world: On using machine learning for network intrusion detection,” in Proc. IEEE Symp. Secur. Privacy, May 2010, pp. 305–316.

[10] M. Shen et al., “Swallow: A transfer-robust website fingerprinting attack via consistent feature learning,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., Nov. 2025, pp. 1574–1588.

[11] Y. He, X. Kang, Q. Yan, and E. Li, “ResNeXt+: Attention mechanisms based on ResNeXt for malware detection and classification,” IEEE Trans. Inf. Forensics Security, vol. 19, pp. 1142–1155, 2024.

[12] Y. Chen, X. Li, J. Wang, W. Ge, and L. Tan, “CorreFlow: A covert fingerprinting modulation for flow correlation in open heterogeneous networks,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 4915–4928, 2025.

[13] M. Shen, J. Wu, K. Ye, K. Xu, G. Xiong, and L. Zhu, “Robust detection of malicious encrypted trafic via contrastive learning,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 4228–4242, 2025.

[14] Q. Meng et al., “When unknown threat meets label noise: A selfcorrecting framework,” IEEE Trans. Depend. Secure Comput., vol. 23, no. 1, pp. 905–922, Jan. 2026.

[15] H. Zheng et al., “Learning from models beyond fine-tuning,” Nature Mach. Intell., vol. 7, no. 1, pp. 6–17, Jan. 2025.

[16] G. I. Webb and Z. Zheng, “Multistrategy ensemble learning: Reducing error by combining ensemble learning techniques,” IEEE Trans. Knowl. Data Eng., vol. 16, no. 8, pp. 980–991, Aug. 2004.

[17] Z. Wang, K. Zhang, S. Yang, D. He, and S. Chan, “Enhancing Android malware detection via knowledge distillation on homogenized function call graphs,” Knowl.-Based Syst., vol. 323, Jul. 2025, Art. no. 113687.

[18] W. Yu and B. Zhou, “Using random forests for eficient identification of decoys under link flooding attacks in SDNs,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 10636–10651, 2025.

[19] R. Ozdemir, M. Tas¸y <sup>¨</sup> urek, and V. Aslantas¸, “Improved marine predators¨ algorithm and extreme gradient boosting (XGBoost) for shipment status time prediction,” Knowl.-Based Syst., vol. 294, Jun. 2024, Art. no. 111775.

[20] G. Aceto, D. Ciuonzo, A. Montieri, and A. Pescape, “Mobile encrypted trafic classification using deep learning: Experimental evaluation, lessons learned, and challenges,” IEEE Trans. Netw. Service Manage., vol. 16, no. 2, pp. 445–458, Jun. 2019.

[21] Q. Meng et al., “Detection of unknown attacks through encrypted trafic: A Gaussian prototype-aided variational autoencoder framework,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 10652–10667, 2025.

[22] R. Lazzarini, H. Tianfield, and V. Charissis, “A stacking ensemble of deep learning models for IoT intrusion detection,” Knowl.-Based Syst., vol. 279, Nov. 2023, Art. no. 110941.

[23] N. Zucchet and A. Orvieto, “Recurrent neural networks: Vanishing and exploding gradients are not the end of the story,” in Proc. Adv. Neural Inf. Process. Syst., 2024, pp. 139402–139443.

[24] F. Laghrissi, S. Douzi, K. Douzi, and B. Hssina, “Intrusion detection systems using long short-term memory (LSTM),” J. Big Data, vol. 8, no. 1, p. 65, Dec. 2021.

[25] A. Vaswani et al., “Attention is all you need,” in Proc. Adv. Neural Inf. Process. Syst., vol. 30, 2017, pp. 1–11.

[26] U. Sa’ad, D. S. Lakew, N.-N. Dao, and S. Cho, “HERALD: Hybrid ensemble approach for robust anomaly detection in encrypted DNS trafic,” J. Netw. Comput. Appl., vol. 244, Dec. 2025, Art. no. 104342.

[27] T. Shapira and Y. Shavitt, “FlowPic: A generic representation for encrypted trafic classification and applications identification,” IEEE Trans. Netw. Service Manage., vol. 18, no. 2, pp. 1218–1232, Jun. 2021.

[28] X. Wang et al., “Entropy-regulated cross-modal generative fusion for multimodal network intrusion detection,” Inf. Fusion, vol. 126, Feb. 2026, Art. no. 103581.

[29] Q. Yuan et al., “Multi-agent for network security monitoring and warning: A generative AI solution,” IEEE Netw., vol. 39, no. 5, pp. 114–121, Sep. 2025.

[30] R. Jiang, S. Al-Maadeed, A. Bouridane, D. Crookes, and M. E. Celebi, “Face recognition in the scrambled domain via salience-aware ensembles of many kernels,” IEEE Trans. Inf. Forensics Security, vol. 11, no. 8, pp. 1807–1817, Aug. 2016.

[31] Y. Wang, H. Xu, Z. Guo, Z. Qin, and K. Ren, “SnWF: Website fingerprinting attack by ensembling the snapshot of deep learning,” IEEE Trans. Inf. Forensics Security, vol. 17, pp. 1214–1226, 2022.

[32] R. Karn, K. Nawaz, and I. Elfadel, “Order-preserving cryptography for the confidential inference in random forests: FPGA design and implementation,” in Proc. 61st ACM/IEEE Design Autom. Conf., Jun. 2024, pp. 1–6.

[33] G. Hinton, O. Vinyals, and J. Dean, “Distilling the knowledge in a neural network,” Comput. Sci., vol. 14, no. 7, pp. 38–39, 2015.

[34] A. Romero, N. Ballas, S. E. Kahou, A. Chassang, C. Gatta, and Y. Bengio, “FitNets: Hints for thin deep nets,” in Proc. Int. Conf. Learn. Represent., 2015.

[35] Y. Liu et al., “Knowledge distillation via instance relationship graph,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2019, pp. 7089–7097.

[36] Y. Zhu and Y. Wang, “Student customized knowledge distillation: Bridging the gap between student and teacher,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), Oct. 2021, pp. 5037–5046.

[37] S. Zhang et al., “Causal distillation for alleviating performance heterogeneity in recommender systems,” IEEE Trans. Knowl. Data Eng., vol. 36, no. 2, pp. 459–474, Feb. 2024.

[38] M. Lu, B. Zhou, and Z. Bu, “Two-stage distillation-aware compressed models for trafic classification,” IEEE Internet Things J., vol. 10, no. 16, pp. 14152–14166, Aug. 2023.

[39] S. Li, Y. Cao, G. Peng, M. Li, W. Sun, and L. Chen, “Eficient intrusion detection for in-vehicle networks using knowledge distillation from BERT to CNN-BiLSTM,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 6398–6412, 2025.

[40] T.-N.-V. Dinh, N.-P.-H. Nguyen, A.-D. Tran, and K.-H. Le, “Knowledge distillation for improved resilience in network intrusion detection systems,” in Proc. Int. Conf. Adv. Technol. Commun. (ATC), Oct. 2024, pp. 185–190.

[41] H. Zhu, M. Xia, L. Wang, Z. Xu, and V. S. Sheng, “A novel knowledge search structure for Android malware detection,” IEEE Trans. Services Comput., vol. 17, no. 6, pp. 3052–3064, Nov. 2024.

[42] V. Sanh, L. Debut, J. Chaumond, and T. Wolf, “DistilBERT, a distilled version of BERT: Smaller, faster, cheaper and lighter,” 2019, arXiv:1910.01108.

[43] X. Jiao et al., “TinyBERT: Distilling BERT for natural language understanding,” in Proc. Findings Assoc. Comput. Linguistics: EMNLP, 2020, pp. 4163–4174.

[44] Q. Meng et al., “Fine-grained detection and analysis of unknown encrypted malicious trafic from mixed noisy labels,” IEEE Trans. Depend. Secure Comput., pp. 1–18, May 2026.

[45] M. Stone, “The opinion pool,” Ann. Math. Statist., vol. 32, no. 4, pp. 1339–1342, 1961.

[46] C. Genest and J. V. Zidek, “Combining probability distributions: A critique and an annotated bibliography,” Stat. Sci., vol. 1, no. 1, pp. 114–135, Feb. 1986.

[47] T. Heskes, “Selecting weighting factors in logarithmic opinion pools,” in Proc. Adv. Neural Inf. Process. Syst., vol. 10, 1997, pp. 266–272.

[48] J. Su, M. Ahmed, Y. Lu, S. Pan, W. Bo, and Y. Liu, “RoFormer: Enhanced transformer with rotary position embedding,” Neurocomputing, vol. 568, Feb. 2024, Art. no. 127063.

[49] B. Zhang and R. Sennrich, “Root mean square layer normalization,” in Proc. Adv. Neural Inf. Process. Syst., vol. 32, 2019, pp. 12360–12371.

[50] J. L. Ba, J. R. Kiros, and G. E. Hinton, “Layer normalization,” 2016, arXiv:1607.06450.

[51] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2016, pp. 770–778.

[52] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware trafic classification using convolutional neural network for representation learning,” in Proc. Int. Conf. Inf. Netw. (ICOIN), Da Nang, Vietnam, Jan. 2017, pp. 712–717.

[53] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of encrypted and VPN trafic using time-related features,” in Proc. 2nd Int. Conf. Inf. Syst. Secur. Privacy, 2016, pp. 407–414.

[54] E. C. P. Neto, S. Dadkhah, R. Ferreira, A. Zohourian, R. Lu, and A. A. Ghorbani, “CICIoT2023: A real-time dataset and benchmark for large-scale attacks in IoT environment,” Sensors, vol. 23, no. 13, p. 5941, Jun. 2023.

[55] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “AppScanner: Automatic fingerprinting of smartphone apps from encrypted network trafic,” in Proc. IEEE Eur. Symp. Secur. Privacy, Mar. 2016, pp. 439–454.

[56] A. Panchenko et al., “Website fingerprinting at internet scale,” in Proc. Netw. Distrib. Syst. Secur. Symp., 2016, p. 23477.

[57] K. Al-Naami et al., “Adaptive encrypted trafic fingerprinting with bidirectional dependence,” in Proc. 32nd Annu. Conf. Comput. Secur. Appl., Dec. 2016, pp. 177–188.

[58] M. Jiang, G. Gou, J. Shi, and G. Xiong, “I know what you are doing with remote desktop,” in Proc. IEEE 38th Int. Perform. Comput. Commun. Conf. (IPCCC), London, U.K., Oct. 2019, pp. 1–7.

[59] A. Yang et al., “Qwen2 technical report,” 2024, arXiv:2407.10671.

[60] E. J. Hu et al., “LoRa: Low-rank adaptation of large language models,” in Proc. ICLR, vol. 1, no. 2, 2022, p. 3.

[61] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “ET-BERT: A contextualized datagram representation with pre-training transformers for encrypted trafic classification,” in Proc. ACM Web Conf., 2022, pp. 633–642.

[62] R. Zhao et al., “Yet another trafic classifier: A masked autoencoder based trafic transformer with multi-level flow representation,” in Proc. AAAI Conf. Artif. Intell., vol. 37, no. 4, 2023, pp. 5420–5427.

[63] G. Zhou, X. Guo, Z. Liu, T. Li, Q. Li, and K. Xu, “TraficFormer: An eficient pre-trained model for trafic data,” in Proc. IEEE Symp. Secur. Privacy (SP), May 2025, pp. 1844–1860.

[64] X. Xiao et al., “RBLJAN: Robust byte-label joint attention network for network trafic classification,” IEEE Trans. Depend. Secure Comput., vol. 22, no. 3, pp. 2161–2178, May 2025.

[65] A. Yang et al., “Qwen2.5 technical report,” 2025, arXiv:2412.15115.

[66] T. M. Cover et al., “Entropy, relative entropy and mutual information,” Elements Inf. Theory, vol. 2, no. 1, pp. 12–13, 1991.
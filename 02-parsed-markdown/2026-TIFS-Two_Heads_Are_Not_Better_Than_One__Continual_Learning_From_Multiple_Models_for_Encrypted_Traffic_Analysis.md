# Two Heads Are Not Better Than One: Continual Learning From Multiple Models for Encrypted Trafic Analysis

Jia Liu , Bin Lu , Qingjun Yuan , Weina Niu , Senior Member, IEEE, Ding Li , Jian Chai, and Yong Yu , Fellow, IEEE

Abstract—Encrypted Trafic Analysis (ETA) is a critical area of research for security monitoring in modern networks. Although machine learning- and deep learning-based ETA methods have shown significant promise, they depend heavily on large-scale, manually labeled data. Meanwhile, the research community has released many high-performing ETA models. However, the knowledge embedded in these models remains siloed and dificult to reuse, as they are trained on heterogeneous feature spaces and task semantics. In practice, such models are typically developed independently at diferent times. Consequently, a unified model cannot be jointly learned from all existing models. Instead, it should learn each model’s knowledge sequentially as it becomes available. These observations raise a key question: Can we construct a unified model that continually learns from multiple existing models? To address this problem, we propose the Dual-Branch Continual Learning (DBCL) framework, which enables a single large language model (LLM)-based student model to continually learn from multiple task-specific teacher models using teacher-generated predictions rather than raw labeled data. DBCL represents heterogeneous trafic features and task semantics in a shared semantic space and mitigates catastrophic forgetting via a dual-branch architecture that balances rapid knowledge acquisition with long-term retention. Experiments across four publicly available datasets of encrypted trafic demonstrate that DBCL consistently outperforms competitive continual learning baselines. Furthermore, we provide information-theoretic and optimization-theoretic analyses that ofer insights into the efectiveness of DBCL, highlighting its potential as a promising ETA approach.

Index Terms—Encrypted trafic analysis, continual learning, large language model, catastrophic forgetting.

## I. INTRODUCTION

modern networks are now overwhelmingly dominated by fully encrypted trafic [1], [2], [3]. While this shift greatly enhances user privacy and data confidentiality [4], it also removes visibility of packet content and key metadata, causing traditional inspection-based threat detection systems to lose efectiveness [5] and leaving critical blind spots in network security monitoring [6].

Encrypted Trafic Analysis (ETA) has emerged as a crucial area for supporting security monitoring [7], trafic management [8], and threat detection [9] in modern encrypted networks. Recent advances, including machine learning (ML) [10], [11], deep learning (DL) [12], [13], and more recently a large language model (LLM) [14], [15], have significantly improved ETA by leveraging statistical patterns, timing structures, and raw trafic byte features. However, these data-driven methods depend on large amounts of manually labeled data [16], which are costly and challenging to acquire in practice due to protocol encryption, strict privacy constraints, and the substantial burden of manual annotation.

In contrast, the research community [17], [18] has released a wide range of ETA models. These models demonstrate strong performance and capture substantial domain knowledge. However, this knowledge remains siloed [19], [20] and is dificult to reuse, as they are trained on heterogeneous feature spaces and task semantics. In practice, such models are typically developed independently at diferent times. Consequently, a unified model cannot be jointly learned from all existing models. Instead, it should learn each model’s knowledge sequentially as it becomes available. These observations raise a practical question:

## Can we construct a unified model that continually learns from multiple existing models?

In practical ETA deployment scenarios, multiple models may be available for diferent tasks. A routing-based strategy is feasible when task boundaries are clear and reliable task assignment is available. However, such a strategy mainly addresses model selection rather than knowledge consolidation. Accordingly, the motivation for constructing a unified model is not merely to avoid repeated model switching [21] during inference, but more importantly to enable continual knowledge consolidation. The primary goal is to continually learn knowledge from multiple existing models while mitigating the forgetting of previously acquired model knowledge. However, this sequential, model-driven learning setting gives rise to two central challenges:

(1) Heterogeneous Features and Task Semantics: Existing ETA models are trained on diverse trafic feature spaces, such as statistical flow vectors, packet-length sequences, byte distributions, and graph structures, resulting in inherently incompatible feature representations. Moreover, each model is tailored to a distinct task (e.g., malware detection, application classification, VPN identification), resulting in heterogeneous task semantics. Prior work on knowledge distillation [22] typically assumes that the teacher and student models operate on compatible input representations and share fixed task semantics, such that the student can be trained to match the teacher outputs. In contrast, ETA models are independently developed under heterogeneous feature spaces and task semantics. This heterogeneity exposes a fundamental gap: there exists no unified mechanism to reconcile incompatible feature spaces and heterogeneous task semantics across independently trained ETA models.

(2) Catastrophic Forgetting of Model Knowledge: A unified ETA model that continually learns from multiple taskspecific teacher models should rapidly learn knowledge from newly arriving teachers while preserving knowledge learned from earlier ones. However, under a fixed model architecture with a shared parameter space, learning from a new teacher requires updating the same set of parameters that encode previously learned teacher knowledge, leading to interference and catastrophic forgetting. Prior work on continual learning [23] is predominantly data-driven and typically assumes a fixed input feature space, where new tasks are accommodated by adapting task-specific outputs and forgetting is evaluated on historical datasets. In contrast, learning from multiple task-specific teacher models involves continual acquisition of model-level knowledge, where each teacher model is built on heterogeneous trafic features and distinct task semantics. This discrepancy reveals a clear research gap: existing methods cannot be directly applied to continually learn and retain teacher model knowledge across heterogeneous input representations and task semantics.

To address these challenges, we propose the Dual-Branch Continual Learning (DBCL) framework, which enables a unified student model to continually learn knowledge from multiple task-specific teacher models using teacher-generated predictions rather than raw labeled data. To handle the heterogeneity in both trafic features and task semantics, we introduce two mechanisms: Negative Entropy Injection (NEI) and Instruction Construction (IC). NEI transforms heterogeneous trafic features and teacher model outputs into unified textual descriptions. At the same time, IC generates task-specific instructions that guide the model in identifying and selecting the relevant trafic features for each task.

To mitigate catastrophic forgetting of previously learned teacher model knowledge, we design a dual-branch LLMbased student model architecture comprising a Fast Learning Adapter (FLA) for rapidly acquiring knowledge from the current teacher model and a Stable Learning Adapter (SLA) for gradually consolidating knowledge from previously learned teachers. Additionally, a reservoir-based memory bufer for replay facilitates the reuse of historical teacher knowledge, while a layer-wise Knowledge Alignment Loss (KAL) prevents semantic drift between the two branches. Together, these components enable DBCL to continually learn from multiple task-specific ETA models.

The contributions of this paper are summarized as follows:

We propose DBCL, a unified framework that shifts ETA’s focus from data-driven learning to model-driven continual learning. DBCL enables a student model to continually learn from multiple task-specific teacher models using teacher-generated predictions rather than raw labeled data, providing a scalable solution for ETA.

We introduce NEI and IC, which unify heterogeneous trafic features and task semantics. DBCL designs a dualbranch, LLM-based student model architecture to mitigate catastrophic forgetting of model knowledge through a reservoir-based replay bufer and layer-wise KAL.

• We design two novel evaluation metrics: Teacher Knowledge Accuracy and Teacher Knowledge Backward Transfer. These metrics quantitatively assess how well the student model acquires knowledge from multiple taskspecific teacher models and retains it over time, ofering a new way to evaluate continual learning in ETA.

• We conduct extensive experiments across four publicly available datasets of encrypted trafic, demonstrating that DBCL outperforms competitive baselines. Additionally, we provide theoretical analysis grounded in information-theoretic and optimization-theoretic perspectives to validate the efectiveness and soundness of DBCL’s core mechanisms.

The remainder of this paper is organized as follows. Section II reviews the related work. Section III describes the proposed system architecture. Section IV presents the experimental setup and results. Section V discusses several issues concerning DBCL. Section VI provides theoretical analysis from information-theoretic and optimization-theoretic perspectives. Finally, Section VII concludes the paper and outlines directions for future research.

## II. RELATED WORK

## A. Encrypted Trafic Analysis (ETA)

Early ETA primarily relied on Deep Packet Inspection [24], which performed security detection by parsing features such as protocols, port numbers, and IP addresses. However, it is inefective at identifying encrypted trafic. To overcome these limitations, researchers began exploring ML. A recent comprehensive survey further summarized encrypted trafic identification and classification techniques, highlighting the challenges and future directions [25]. Taylor et al. [26] proposed the AppScanner framework, which achieves high-accuracy identification even under encrypted trafic. Panchenko et al. [27] introduced CUMUL, a new website fingerprinting attack method that uses 104-dimensional network trafic statistical features for website trafic recognition. Choi et al. [28] also investigated feature extraction for encrypted network trafic to support application classification. These methods primarily rely on manually designed statistical features, which have limited generalization capabilities.

In recent years, DL has become the mainstream approach, capable of automatically extracting temporal features from raw trafic data to improve analysis accuracy. For example, Chakravorty et al. [29] applied DL to anomaly detection in encrypted network trafic, while recent ML approaches have also been explored for intrusion detection without decryption [30]. However, existing DL methods lack interpretability. With the development of Transformer architectures, LLMs have gradually gained attention in ETA. Lin et al. [31] proposed ET-BERT, which improves encrypted trafic classification accuracy by pre-training on unlabeled encrypted trafic data and fine-tuning it for specific tasks. Meng et al. [32] introduced the Net GPT model, based on Transformer architectures, that combines multimodal optimization to enhance network trafic analysis capabilities. Qu et al. [33] proposed the Trafic GPT model, which uses linear attention mechanisms to increase the model’s token length limit, thereby enhancing its applicability. Lin et al. [15] proposed ETooL, an ETA model that combines LLMs with self-supervised instruction tuning to improve classification performance and generalization under non-iid conditions.

Despite these advances, existing ETA methods remain largely data-driven and rely heavily on manually labeled trafic data. In practice, however, such labels are costly and dificult to obtain due to protocol encryption, strict privacy constraints, and the substantial efort required for manual annotation, which significantly limits their applicability in realworld network environments.

## B. Knowledge Distillation (KD)

KD transfers predictive behavior from a high-capacity teacher to a student model by training the student to match the teacher’s outputs, typically using softened probability distributions as supervision [34]. KD has been widely used for model compression and eficient deployment, and has also been extended to settings with limited or unavailable labeled data through proxy data or data-free generation [35], [36].

In network security and trafic analysis, KD has primarily been used as a compression-and-deployment tool to meet latency constraints. For example, Lu et al. [37] propose a two-stage distillation-aware compression pipeline for trafic classification to reduce computation overhead while maintaining accuracy. Li et al. [38] distill a BERT-based teacher into a CNN-BiLSTM student for eficient in-vehicle intrusion detection, demonstrating that KD can preserve detection capability under tight resource budgets, for improving model generalization and cross-domain transfer, particularly efective in data-scarce or domain-shifted scenarios. Liu et al. [39] proposed an Instance Relationship Graph-based distillation method to improve cross-domain adaptability. In contrast, Zhu and Wang [40] designed an adaptive distillation framework based on gradient similarity to mitigate optimization bias. More recently, Wang et al. [41] propose homogenizing function call graphs and performing teacher-student distillation to enhance graph-based malware detection, demonstrating that KD can improve detection performance while maintaining eficiency.

Although existing KD methods have demonstrated efectiveness in model compression and performance preservation, they typically assume that the teacher and student operate on compatible input representations and share fixed task semantics. In ETA, however, task-specific models are independently developed using heterogeneous trafic features and are optimized for distinct task objectives. Consequently, conventional KD does not apply to learning knowledge from heterogeneous ETA models with incompatible feature spaces and task semantics.

## C. Continual Learning (CL)

CL aims to mitigate catastrophic forgetting in sequential learning tasks, enabling a network model to continually learn new knowledge while retaining previously acquired knowledge without accessing the entire historical data [42]. Existing research [43] classifies CL methods into three categories: data replay, parameter isolation, and parameter regularization.

Data replay uses historical samples to maintain performance on previous tasks. Pennisi et al. [44] proposed the Experience Replay (ER) algorithm, which enhances the stability of the network model through sample caching. Lopez-Paz and Ranzato [45] introduced the Gradient Episodic Memory (GEM) algorithm, which introduces episodic memory constraints to achieve more efective knowledge transfer. Later, Chaudhry et al. [46] proposed A-GEM, a more eficient variant that reduces computational and memory requirements while maintaining high task performance. Buzzega et al. [47], and Huang et al. [48] proposed storing historical information using logits to reduce the overhead of directly storing samples. However, as task volume continues to increase, the memory bufer size becomes a bottleneck.

Parameter isolation avoids interference between tasks by assigning independent parameter sub-networks for each task. Du et al. [49] proposed an expandable network that allocates task-specific modules as new tasks arrive, and Ksiazek and Spurek [50] proposed HyperMask to generate task-specific masks that select subnetworks for continual learning. However, the cost of parameter partitioning and adjustment is high.

Regularization-based methods penalize updates to important parameters to preserve knowledge of previous tasks. The Elastic Weight Consolidation (EWC) algorithm, proposed by Li et al. [51], regularizes weight changes when fine-tuning a pretrained model, enabling high-quality generation even with only a few target-domain samples while preserving sourcedomain diversity. Zenke et al. [52], and Aljundi et al. [53] proposed regularization methods that evaluate the importance of neural network parameters and penalize excessive updates to critical parameters to slow down forgetting.

![](images/c6ea369c20c2ac5f0d48fdf78502933c2123a368ebd130eff64e0e536a773947.jpg)  
Fig. 1. Overview of the proposed DBCL Framework.

Although these methods alleviate catastrophic forgetting in sequential learning, they are predominantly designed for data-driven CL, where tasks share a fixed input feature space and forgetting is measured on historical datasets. In contrast, our setting requires continual acquisition of model-level knowledge from multiple task-specific teacher models, each built upon heterogeneous trafic features and distinct task semantics. Given heterogeneous inputs and semantics, directly applying existing replay, isolation, or regularization strategies is insuficient, as the student should preserve previously learned teacher knowledge while adapting to new, incompatible teachers. Therefore, there exists a clear research gap: existing CL methods cannot be directly applied to continually learn and retain teacher model knowledge across heterogeneous input representations and task semantics.

## III. METHOD

In this section, we provide a detailed description of our proposed DBCL framework. Fig. 1 depicts an overview of DBCL, which consists of three stages. (A) Data preprocessing converts raw PCAP files into standardized flow samples by flow definition, packet sampling, noise filtering, and dataset splitting (Section III-A). (B) Task-oriented data construction leverages a task-specific feature extractor and the corresponding teacher model to produce teacher-predicted data, and further bridges heterogeneous feature representations and output semantics via NEI and IC (Section III-B). (C) Dual-branch continual learning trains a single LLM-based student model to continually learn knowledge from multiple teacher models, using FLA, SLA, a memory bufer, and KAL to mitigate catastrophic forgetting of teacher model knowledge (Section III-C). Finally, we design teacher-knowledge evaluation metrics for model-level assessment (Section III-D).

## A. Data Preprocessing

To provide consistent and standardized inputs for multiple task-specific ETA models, we employ a unified preprocessing pipeline. This stage transforms raw PCAP files into welldefined flow samples by cleaning, organizing, and partitioning packets, thereby ofering a reliable basis for subsequent feature extraction and model training. The preprocessing procedure consists of three steps:

(1) Flow Definition. Let $\mathcal { P } = \{ p _ { i } \ | \ i = 1 , . . . , T \}$ denote the set of captured packets, where T is the total number of packets. Each packet $p _ { k }$ is associated with a canonical fivetuple identifier:

$$
\Psi (p _ {i}) = (s r c I P, d s t I P, s r c P o r t, d s t P o r t, p r o t o c o l),\tag{1}
$$

where Ψ(·) denotes the mapping function that extracts the corresponding five-tuple from each packet.

A network flow $\ell _ { \phi }$ is defined as the collection of all packets sharing the same five-tuple:

$$
\ell_ {\phi} = \{p _ {i} \in \mathcal {P} | \Psi (p _ {i}) = \phi \}.\tag{2}
$$

where $\phi$ represents a specific five-tuple value corresponding to the flow identifier.

(2) Packet Sampling. To keep comparable temporal granularity across encrypted trafic samples, each flow $\ell _ { \phi }$ is truncated into a fixed-length packet sequence:

$$
\mathbf {s} _ {\phi} = (p _ {1}, p _ {2}, \dots , p _ {L}), \quad L = 5.\tag{3}
$$

(3) Noise Filtering and Dataset Splitting. To improve data quality, malformed or incomplete flows (e.g., retransmissions or corrupted headers) are discarded. The remaining dataset D is then stratified into training, validation, and test subsets with an 8 : 1 : 1 split, ensuring class balance and consistent evaluation across all splits.

## B. Task-Oriented Data Construction

To enable the LLM-based student model to learn continually from multiple task-specific ETA models without requiring access to raw labeled data during student training, we construct a collection of task-specific datasets:

$$
\mathcal {D} = \{\mathcal {D} _ {1}, \mathcal {D} _ {2}, \ldots , \mathcal {D} _ {T} \},\tag{4}
$$

where T denotes the total number of tasks and $t \in \{ 1 , \ldots , T \}$ refers to the t-th ETA task (e.g., malware detection, encrypted application identification). Each task t is associated with a teacher model $M _ { t } ,$ , which is selected because it achieves the best performance for its corresponding task and therefore serves as a domain specialist.

(1) Task-Specific Feature Extraction. Let $x _ { i } \in \mathcal X$ denote a processed flow sample obtained from Section III-A. Each task t defines a feature extraction function:

$$
\mathcal {F} _ {t}: \mathcal {X} \to \mathbb {R} ^ {d _ {t}},\tag{5}
$$

where $d _ { t }$ denotes the dimensionality of the encrypted trafic feature space required by the best-performing teacher model $M _ { t }$ for task t. Applying $\mathcal { F } _ { t }$ produces the task-specific feature vector:

$$
x _ {i} ^ {(t)} = \mathcal {F} _ {t} (x _ {i}).\tag{6}
$$

(2) Teacher Model prediction. The feature vector $x _ { i } ^ { ( t ) }$ is fed into the corresponding teacher model:

$$
\hat {y} _ {i} ^ {(t)} = M _ {t} (x _ {i} ^ {(t)}),\tag{7}
$$

where $\hat { y } _ { i } ^ { ( t ) } \in \hat { \mathcal { V } }$ denotes the teacher model prediction. Since task t determines both the teacher model $M _ { t }$ and the feature extraction function $\mathcal { F } _ { t } .$ , each constructed flow sample is represented as the triplet (task id<sub>t</sub> $x _ { i } ^ { ( t ) } , ~ \hat { y } _ { i } ^ { ( t ) } )$ , where task $\mathbf { \Pi } _ { i d _ { t } }$ is an identifier (e.g., 0 for malware detection, 1 for encrypted application classification) that specifies the type of ETA task.

(3) Task Data. To bridge the heterogeneity in both trafic features and task semantics, DBCL introduces two mechanisms as follows:

(i) Negative Entropy Injection (NEI). Diferent teacher models are trained on task-specific trafic features with incompatible structures (e.g., statistical vectors, packet sequences, or byte distributions). NEI converts each numerical feature vector $x _ { i } ^ { ( t ) }$ into a semantically meaningful textual description, enabling the LLM to process heterogeneous feature formats within a shared linguistic space. Similarly, the teacher prediction $\hat { y } _ { i } ^ { ( t ) }$ is also textualized. This mechanism produces an interpretable, language-based view of the input-output pair for each task t.

(ii) Instruction Construction. To diferentiate the semantic intent of each task t (e.g., VPN identification vs. Internet-of-Things (IoT) attack detection), we construct a natural language instruction from the task identifier task $i d _ { t } ,$ which explicitly specifies the task goal and indicates the types of trafic features relevant to the task.

Combining the above two mechanisms, each flow sample is represented as follows:

$$
\mathcal {I} _ {i} ^ {(t)} = (I n s t r u c t i o n, I n p u t, A n s w e r),\tag{8}
$$

where the Instruction is derived from task $\ { i d } _ { t } ,$ , the Input is the textualized feature vector $x _ { i } ^ { ( t ) }$ , and the Answer is the textualized teacher prediction $\hat { y } _ { i } ^ { ( t ) }$ . An illustrative structured example is shown below:

## Instruction

Task: IoT attack detection.

Goal: Identify the type of the given network flow.

Decision basis: Statistical trafic characteristics.

Input

Statistical trafic characteristics: protocol=TLS; average packet interval= 0.8 ms; flow duration=...

Answer

This trafic flow is classified as a DDoS attack.

For each task $t ,$ the final dataset is denoted as $\mathcal { D } _ { t } = \{ \mathcal { T } _ { i } ^ { ( t ) } \}$ and the overall multi-task dataset is $\textstyle { \mathcal { D } } = \bigcup _ { t = 1 } ^ { T } { \mathcal { D } } _ { t }$ . For simplicity, we use the same notation and denote the concatenation of the Instruction and Input as $x _ { i } ^ { ( t ) }$ , and the Answer as $\hat { y } _ { i } ^ { ( t ) }$ so that each flow sample is represented as $( x _ { i } ^ { ( t ) } , \hat { y } _ { i } ^ { ( t ) } )$ . These $( x _ { i } ^ { ( t ) } , \hat { y } _ { i } ^ { ( t ) } )$ pairs are conceptually distinct from the numerical feature vector and teacher model prediction defined earlier.

## C. Dual-Branch Continual Learning

To continually learn from multiple task-specific ETA models, we employ a dual-branch architecture based on Qwen [54]. Specifically, it introduces two parallel LoRA-based [55] adapter branches: FLA for rapidly acquiring knowledge from the current teacher model, and SLA for maintaining long-term knowledge accumulated from all previously learned teachers. These two branches work cooperatively through bufer replay and knowledge alignment.

(1) Tokenization and Memory Bufer. Each flow sample $( x _ { i } ^ { ( t ) } , \hat { y } _ { i } ^ { ( t ) } )$ from task t is tokenized using the Qwen Tokenizer to produce an input-output token pair:

$$
\begin{array}{l} s _ {i} ^ {(t)} = (\text { input\_ids } _ {i} ^ {(t)}, \text { output\_ids } _ {i} ^ {(t)}) \\ = \text { Tokenizer } \left(x _ {i} ^ {(t)}, \hat {y} _ {i} ^ {(t)}\right), \end{array}\tag{9}
$$

where input $\mathrm { i d s } _ { i } ^ { ( t ) }$ is the tokenized sequence derived from $x _ { i } ^ { ( t ) }$ , output $\mathrm { \overline { { i d s } } } _ { i } ^ { ( t ) ^ { \prime } }$ is the tokenized sequence derived from the teacher prediction $\hat { y } _ { i } ^ { ( t ) }$ , and $s _ { i } ^ { ( t ) }$ denotes the complete tokenized instance used for training and replay.

Each $s _ { i } ^ { ( t ) }$ is then (i) used immediately as the input to the FLA for learning the knowledge from the current model, and (ii) inserted into a fixed-size memory bufer M, which stores the knowledge from all previously learned models.

To ensure that the memory bufer M retains a balanced representation of knowledge across multiple task-specific ETA models, we adopt reservoir sampling [56], as shown in Algorithm 1.

By the classical theory of reservoir sampling, every previously seen flow sample has probability $| \mathcal { M } | _ { \operatorname* { m a x } } / k$ of being retained, ensuring uniform and unbiased replay of the diverse knowledge learned by all models.

(2) FLA and SLA. DBCL injects the FLA and SLA into each feed-forward network (FFN) layer of Qwen, while keeping all self-attention layers and the final output layer fully frozen. Since Qwen itself follows a Transformer architecture, this design preserves the pretrained Qwen backbone for stable sequence modeling and delegates adaptation to the two lowrank branches.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Reservoir Sampling
Require: Incoming tokenized instance  $s_{k}$ , memory buffer M with maximum capacity  $|M|_{max}$ , index k
Ensure: Updated memory buffer M
1: if  $k \leq |M|_{max}$  then
2: Insert  $s_{k}$  into M at position k
3: else
4: Sample  $j \sim \text{Uniform}\{1, \ldots, k\}$ 
5: if  $j \leq |M|_{max}$  then
6:  $M[j] \leftarrow s_{k}$ 
7: end if
8: end if
</div>

Let $W \in \mathbb { R } ^ { d \times k }$ denote the frozen weight matrix of an FFN linear layer, where $d$ and k are the input and output feature dimensions, respectively. LoRA augments W with a learnable low-rank update:

$$
\hat {W} = W + \Delta W, \qquad \Delta W = U V,\tag{10}
$$

where $\hat { W }$ is the adapted weight matrix, ∆W is a learnable low-rank update, $U \in \mathbb { R } ^ { d \times r }$ and $V \in \mathbb { R } ^ { r \times k }$ are the LoRA factor matrices, and r is the adaptation rank with r  min(d k).

In DBCL, the two branches instantiate the above LoRA formulation with separate low-rank factors while sharing the same frozen backbone weight W. The FLA employs matrices $A \in \mathbb { R } ^ { d \times r }$ and $\boldsymbol { B } \in \mathbb { R } ^ { r \times k }$ 2

$$
\hat {W} _ {\mathrm{FLA}} = W + A B,\tag{11}
$$

where $\hat { W } _ { \mathrm { F L A } }$ denotes the efective FFN weight used when the FLA branch is active, and (A B) play the role of the LoRA factors (U V) for the fast-learning branch. The parameters $( A , B )$ are standard learnable adapter weights and participate in gradient-based optimization during learning.

Similarly, the SLA maintains its own low-rank parameters $C \in \mathbb { R } ^ { d \times r }$ and $\boldsymbol { D } \in \mathbb { R } ^ { r \times k }$ ,

$$
\hat {W} _ {\mathrm{SLA}} = W + C D,\tag{12}
$$

where $\hat { W } _ { \mathrm { S L A } }$ is the efective FFN weight for the stable branch, and (C D) are the LoRA factors corresponding to the SLA. Unlike (A B), the parameters (C D) are not updated by backpropagation; they are maintained as a slowly evolving copy of the FLA adapters, updated via an exponential moving average (EMA) of (A B) (the detailed update rule is given later). Together, the FLA and SLA realize a balance between plasticity and stability on top of the frozen Qwen backbone. For final inference, we use the SLA branch by default, and all reported test results are obtained from it unless otherwise specified.

(3) Learning on the Current Model. We use each $s _ { i } ^ { ( t ) }$ (see Eq. (9)) as input to the Qwen backbone equipped with the FLA branch. The backbone and FLA together produce a hidden representation at every token position. The linear layer then maps the final hidden state at position j to a logit vector $\mathbf { z } _ { j } \in \mathbb { R } ^ { | \mathcal { V } | }$ <sup>|</sup>, where |V| denotes the vocabulary size, and the predictive distribution for the j-th token is ${ \bf p } _ { j } = \mathrm { s o f t m a x } ( { \bf z } _ { j } )$ The token-level autoregressive cross-entropy loss is:

$$
\mathcal {L} _ {\mathrm{CEL}} = - \sum_ {j = 1} ^ {\mathcal {S}} \hat {y} _ {j} ^ {(t)} \log p _ {j},\tag{13}
$$

where S denotes the length of the token sequence, $\hat { y } _ { j } ^ { ( t ) }$ is the target token at position j (from the teacher prediction), and $p _ { j }$ is the predicted probability for the j-th token.

(4) Knowledge Alignment Loss. During learning on task t, DBCL uniformly samples a mini-batch of previously stored tokenized instance $s _ { k } ~ = ~ ( \mathrm { i n p u t \_ i d s } _ { k } .$ output $\mathrm { i d s } _ { k } )$ from the replay bufer M. Each $s _ { k }$ is forwarded through both the FLA and the SLA branches.

For the l-th Transformer layer (from the Qwen model), and for each token position $j \in \{ 1 , \ldots , S \}$ , where S denotes the token sequence length, we obtain the corresponding hidden representations at the j-th token position in the l-th layer: $\mathbf { h } _ { \mathrm { F L A } } ^ { ( \bar { l } , j ) } \in \mathbb { R } ^ { d _ { h } } , \mathbf { h } _ { \mathrm { S L A } } ^ { ( l , j ) } \in \mathbb { R } ^ { d _ { h } }$ , where $d _ { h }$ is the hidden dimensionality of each Transformer layer (and the same for both branches).

To prevent the FLA from drifting away from the stable SLA representation space, DBCL designs a Knowledge Alignment Loss (KAL), which enforces layer-wise and token-wise consistency between the two branches. The alignment loss is defined as:

$$
\mathcal {L} _ {\mathrm{KAL}} = \frac {1}{L} \sum_ {l = 1} ^ {L} \frac {1}{\mathcal {S}} \sum_ {i = 1} ^ {\mathcal {S}} \left\| \mathbf {h} _ {\mathrm{FLA}} ^ {(l, i)} - \mathbf {h} _ {\mathrm{SLA}} ^ {(l, i)} \right\| _ {2} ^ {2}.\tag{14}
$$

Here, L denotes the total number of Transformer layers, and S is the token sequence length.

Unlike consistency regularizers that align only the final output layer, KAL constrains the internal representations at all Transformer layers, thereby preserving multi-level semantic structure and mitigating catastrophic forgetting at the representational level.

(5) Parameter Update. FLA is learned by minimizing the combined loss:

$$
\mathcal {L} _ {\text { total }} = \mathcal {L} _ {\text { CEL }} + \lambda \mathcal {L} _ {\text { KAL }},\tag{15}
$$

where λ is dynamically adjusted during learning to balance the current model learning and knowledge retention. Specifically, λ is updated as follows:

$$
\lambda = \min \left(\lambda_ {\max}, \max \left(\lambda_ {\min}, \frac {\mathcal {L} _ {\mathrm{KAL}}}{\mathcal {L} _ {\mathrm{CEL}} + \varepsilon}\right)\right),\tag{16}
$$

where $\lambda _ { \mathrm { m a x } }$ and $\lambda _ { \operatorname* { m i n } }$ are predefined upper and lower bounds for λ, and ε is a small constant to avoid division by zero. This dynamic adjustment allows the model to prioritize knowledge retention or current model learning based on the the progress of learning.

SLA does not receive gradient updates directly. Instead, its parameters are updated using an exponential moving average (EMA) of the FLA parameters to ensure gradual and stable evolution. The EMA update rule for the SLA parameters is:

$$
\theta_ {\mathrm{SLA}} ^ {(k)} = \alpha \cdot \theta_ {\mathrm{SLA}} ^ {(k - 1)} + (1 - \alpha) \cdot \theta_ {\mathrm{FLA}} ^ {(k)},\tag{17}
$$

where $\theta _ { \mathrm { S L A } } ^ { ( k ) }$ denotes the SLA parameters at the current time step $k , \bar { \theta _ { \mathrm { S L A } } ^ { ( \bar { k } - 1 ) } }$ is the SLA parameters at the previous time step $k - 1 , \ \theta _ { \mathrm { F L A } } ^ { ( k ) }$ represents the FLA parameters at time step k, α $\in [ 0 , 1 ]$ is a hyperparameter controlling the rate of update, ensuring that the SLA parameters evolve slowly and remain consistent with previously learned knowledge.

The EMA-based SLA update is designed to provide a stable consolidation mechanism complementary to the fast adaptation of FLA. While FLA is directly optimized by gradient backpropagation to acquire knowledge from the current teacher model, SLA maintains a smoothed parameter trajectory and gradually incorporates newly acquired teacher knowledge. Directly copying FLA parameters to SLA or updating SLA using the current-task loss would weaken its ability to retain previously learned teacher knowledge. Thus, the two branches separate plastic adaptation from stable consolidation, reducing interference between new and previously learned teacher knowledge.

## D. Teacher Knowledge Evaluation Metrics

To quantitatively assess DBCL’s ability to acquire and retain knowledge from multiple task-specific teacher models, we design two model-level metrics: Teacher Knowledge Accuracy (TA) and Teacher Knowledge Backward Transfer (TBT).

TA measures the student model’s ability to acquire knowledge from teacher models. It is defined as the average accuracy achieved by the student model after learning the knowledge from each teacher model through continual learning, as follows:

$$
\mathrm{TA} = \frac {1}{m} \sum_ {i = 1} ^ {m} R _ {m, i},\tag{18}
$$

where $R _ { m , i }$ denotes the accuracy of the student model after learning the knowledge from teacher model m with respect to teacher model $i ,$ and m is the total number of teacher models. Since the deployment scenario is under teacher-generated supervision, $R _ { m , i }$ is computed as the agreement between the student and teacher predictions (i.e., teacher-generated pseudo labels), rather than accuracy with respect to ground-truth labels.

TBT evaluates knowledge retention by quantifying the backward transfer of teacher knowledge as students acquire knowledge from subsequent teacher models. It is defined as follows:

$$
\mathrm{TBT} = \frac {1}{m - 1} \sum_ {i = 1} ^ {m - 1} \left(R _ {m, i} - R _ {i, i}\right),\tag{19}
$$

where $R _ { m , i }$ denotes the accuracy of the student model after learning the knowledge from teacher model m with respect to teacher model $i , R _ { i , i }$ is the accuracy of the student model right after learning the knowledge from teacher model i, and m is the total number of teacher models.

## IV. EXPERIMENTS

We conduct extensive experiments to assess the DBCL framework. This section covers: (A) experimental setup, (B) multi-teacher knowledge integration performance, (C) teacher-knowledge acquisition and retention analysis, (D) ablation study and (E) additional experiments.

## A. Experimental Setup

(1) Datasets. We evaluate DBCL on four widely used public trafic benchmarks that represent diverse encryptednetwork settings, including TLS/HTTPS application trafic, virtual private network (VPN) tunneled communications, and Internet-of-Things (IoT) environments. The dataset scale and task statistics are summarized in Table I.

(2) Evaluation Metrics. We assess DBCL from two perspectives, including task-level and model-level evaluations.

(i) Task-level Evaluation. To evaluate overall classification performance across tasks, we use standard metrics, including Accuracy (AC) and F1. For each task t, we define a taskspecific label mapping function LabelMap : $\mathcal { V } _ { \mathrm { i d } } ^ { ( t ) }  \mathcal { V } _ { \mathrm { s e m } } ^ { ( t ) }$ which maps each original numerical label to a canonical semantic class name. Teacher predictions and test labels are both converted into this canonical semantic label using LabelMap . During inference, the student generates a textual answer following the predefined response template, such as “This trafic flow is classified as Trojan”. We then extract the predicted class phrase from the generated answer and match it with the canonical semantic label set of the current task. The matched semantic label is used as the predicted class label for AC and F1. If the generated output is empty, malformed, unmatched, or contains multiple conflicting class names, it is treated as an invalid prediction and counted as incorrect.

(ii) Model-level Evaluation. To evaluate DBCL’s ability to learn and retain knowledge from multiple task-specific teacher models, we adopt two model-level metrics including TA and TBT. These are defined as III-D.

(3) Implementation Details. All experiments are conducted on a single NVIDIA A100 GPU and implemented using the PyTorch 2.3 framework. We adopt Qwen3-8B [54] as the base model and apply parameter-eficient continual fine-tuning based on the LoRA method [55]. The overall implementation pipeline and training setup of DBCL are illustrated in Fig. 2.

We use the Adam optimizer with an initial learning rate 1e-4 and a weight decay of 0.01. Each task is trained with a batch size of 64 for up to 4 epochs. All reported results are evaluated using the model checkpoint that achieves the best performance on the validation set.

We inject the FLA into the feed-forward layers using a low-rank parameter $r = 8$ and a dropout rate of 0.1. For the SLA, we set the EMA decay coeficient to $\alpha = 0 . 4$ so that the stable branch updates more conservatively than the fast branch, improving knowledge retention while still allowing gradual consolidation of newly acquired teacher knowledge.

It is worth noting that all reported results are obtained under the unified task-oriented data construction pipeline enabled by NEI and IC. These two mechanisms do not serve as optimization techniques; rather, they define the learning interface between the student and multiple task-specific teacher models.

Since the student model learns teacher knowledge sequentially, the learning order of teacher models may influence the final performance. To mitigate potential order bias, we repeat each experiment with multiple random permutations of teacher model sequences and report the average results across all permutations, ensuring a fair, order-agnostic evaluation.

TABLE I  
STATISTICS OF EXPERIMENT DATASETS

<table><tr><td>Dataset</td><td>#Flows</td><td>Task</td><td>#Labels</td></tr><tr><td>USTC-TFC [57]</td><td>489,139</td><td>1-App Classification</td><td>20</td></tr><tr><td>CSTNET-TLS 1.3 [31]</td><td>46,372</td><td>2-Encrypted App Classification</td><td>120</td></tr><tr><td>ISCXVPN [58]</td><td>311,390</td><td>3-VPN App Classification</td><td>17</td></tr><tr><td>CIC IoT [59]</td><td>1,163,495</td><td>4-IoT Attack Detection</td><td>7</td></tr></table>

![](images/2370662c8372f70e33108f8508d8d4e3a8f403abe5c71620f48171c1b19636df.jpg)  
Fig. 2. Overview of the implementation pipeline and training setup of DBCL.

TABLE II  
OVERALL PERFORMANCE COMPARISON OF THE STUDENT MODEL LEARNED FROM MULTIPLE TASK-SPECIFIC TEACHER MODELS

<table><tr><td rowspan="2">Role</td><td rowspan="2">Method</td><td colspan="2">Task1</td><td colspan="2">Task2</td><td colspan="2">Task3</td><td colspan="2">Task4</td></tr><tr><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td></tr><tr><td rowspan="4">Teacher</td><td>AppScanner</td><td>88.74</td><td>89.07</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr><tr><td>CUMUL</td><td>-</td><td>-</td><td>87.85</td><td>88.05</td><td>-</td><td>-</td><td>-</td><td>-</td></tr><tr><td>BIND</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>83.40</td><td>81.51</td></tr><tr><td>RDP</td><td>-</td><td>-</td><td>-</td><td>-</td><td>88.65</td><td>84.52</td><td>-</td><td>-</td></tr><tr><td rowspan="8">Student</td><td>MoE</td><td>44.63</td><td>45.14</td><td>47.86</td><td>48.41</td><td>54.57</td><td>52.43</td><td>39.61</td><td>38.07</td></tr><tr><td>MIND</td><td>84.78</td><td>84.00</td><td>73.00</td><td>72.93</td><td>74.25</td><td>73.66</td><td>69.10</td><td>69.00</td></tr><tr><td>Seq</td><td>45.39</td><td>44.14</td><td>45.11</td><td>43.87</td><td>54.00</td><td>53.88</td><td>38.99</td><td>37.58</td></tr><tr><td>ER</td><td>63.18</td><td>61.91</td><td>64.70</td><td>64.05</td><td>66.00</td><td>65.02</td><td>61.79</td><td>60.21</td></tr><tr><td>EWC</td><td>68.54</td><td>66.56</td><td>70.24</td><td>69.03</td><td>69.46</td><td>68.68</td><td>60.33</td><td>58.95</td></tr><tr><td>GEM</td><td>80.06</td><td>79.07</td><td>69.83</td><td>68.37</td><td>74.93</td><td>72.35</td><td>57.83</td><td>56.12</td></tr><tr><td>A-GEM</td><td>83.59</td><td>82.44</td><td>70.52</td><td>69.21</td><td>70.00</td><td>69.00</td><td>62.23</td><td>61.83</td></tr><tr><td>DBCL</td><td>86.18</td><td>85.94</td><td>84.26</td><td>83.89</td><td>83.00</td><td>82.95</td><td>75.80</td><td>74.33</td></tr></table>

## B. Multi-Teacher Knowledge Integration Performance

To evaluate the efectiveness of the DBCL framework, we employ four task-specific ETA models as teachers, namely AppScanner [26], CUMUL [27], RDP [60], and BIND [61], each achieving state-of-the-art performance on its corresponding task, as summarized in Table II. For each task, the dataset is stratified into training, validation, and test splits with an 8:1:1 ratio. Within the training split, we generate out-of-fold (OOF) teacher predictions using 5-fold cross-validation: the training data are partitioned into $F _ { 1 } , . . . . , F _ { K }$ , and for each fold $F _ { j } ,$ , the corresponding teacher model is trained on $\textstyle \bigcup _ { i \neq j } F _ { i }$ and produces predictions on the held-out fold. Aggregating predictions across all folds yields OOF predictions for the entire training set, ensuring no information leakage. The student model is trained only on the training data by learning from these teacher-generated predictions, following the continual learning protocol. To ensure fairness, all methods share identical data splits and preprocessing pipelines, and no teacher model is trained or fine-tuned on the validation or test datasets.

We compare DBCL against several competitive model-level CL baselines, each adopting a single strategy to mitigate catastrophic forgetting:

• MoE [62] integrates multiple experts into the student model and employs a gating network to dynamically weight the activated experts for each input.

• MIND [63] is a parameter-isolation method that distills each newly learned teacher model into a task-specific subnetwork while freezing previous sub-networks to reduce forgetting.

• Sequential Learning (Seq) is a naive baseline that continually updates the student model without any mechanism to preserve previously learned teacher knowledge.

• ER [44] maintains a memory bufer of historical teacher knowledge and mitigates forgetting by replaying it during CL.

• EWC [51] alleviates forgetting through parameter regularization based on the Fisher Information Matrix, penalizing changes to parameters that are important for previously learned teacher knowledge.

GEM [45] and A-GEM [46] are gradient-based methods that constrain parameter updates by projecting gradients to reduce interference with previously learned teacher knowledge.

As shown in Table II, MoE obtains an average accuracy of only 46.67%, which is close to Seq with 45.87%, indicating that simply introducing multiple experts cannot efectively mitigate forgetting. MIND introduces parameter isolation to reduce forgetting, yet it tends to map heterogeneous teacher features into a shared representation space. This may ignore the fact that diferent teachers capture diferent trafic patterns, such as packet-length distributions, temporal behaviors, or statistical features. In addition, ETA tasks may have diferent output spaces, e.g., App Classification, VPN App Classification, or IoT Attack Detection, which requires task-specific heads or architectural modifications. These limitations make MIND less robust when learning from multiple heterogeneous teacher models.

Seq sufers from severe performance degradation when integrating knowledge from multiple teacher models. Specifically, Seq achieves only 45.39%, 45.11%, 54.00%, and 38.99% accuracy on tasks 1–4, respectively, indicating pronounced model-level forgetting and poor cross-task generalization. Moreover, the ETA of Seq drops to 38.99%-54.00% across tasks, further confirming its inability to retain knowledge from the teacher model.

Replay-based and regularization-based methods mitigate catastrophic forgetting to a certain extent, yet their performance remains suboptimal when integrating knowledge from multiple teacher models. ER improves task-level accuracy to 63.18% on task1 and 61.79% on task4, demonstrating that replaying historical teacher knowledge can partially preserve previously learned inference behaviors. However, ER still lags significantly behind the teacher models, indicating that simple historical knowledge replay is insuficient to efectively mitigate catastrophic forgetting in sequential multi-teacher learning. EWC further stabilizes learning on early teacher knowledge, achieving 68.54% accuracy on task 1. Nevertheless, its performance on the final task remains limited, with only 60.33% accuracy on task 4. This limitation suggests that global parameter regularization alone cannot efectively retain previously learned teacher knowledge when teacher models are built upon heterogeneous feature spaces and distinct task semantics.

Gradient-based methods, including GEM and A-GEM, further alleviate catastrophic forgetting by explicitly constraining gradient interference between newly learned and previously learned teacher knowledge. Among them, A-GEM achieves accuracies of 83.59%, 70.52%, 70.00%, and 62.23% on tasks 1–4, respectively. Despite these improvements, A-GEM still exhibits noticeable performance degradation on later tasks, particularly task 4, which is learned last in the sequence. This observation indicates that gradient projection alone is insufficient to fully retain previously learned teacher knowledge when integrating multiple teacher models with incompatible feature spaces and task semantics.

In contrast, DBCL consistently achieves the best performance across all four tasks. Specifically, DBCL achieves accuracies of 86.18%, 84.26%, 83.00%, and 75.80% on tasks 1–4, respectively. Notably, DBCL yields a substantial accuracy improvement of +6.70% on task 4 over MIND, which is learned last in the sequence, indicating strong robustness against cumulative forgetting in sequential multi-teacher learning.

The superior performance of DBCL can be attributed to its integrated design that combines structured parameter adaptation with historical teacher knowledge replay. Unlike existing baselines that rely on a single mechanism (e.g., replay, regularization, or gradient projection), DBCL jointly leverages a replay bufer to revisit previously learned teacher knowledge and a dual-branch architecture to control how such knowledge is absorbed and retained. Specifically, FLA enables rapid adaptation to newly introduced teacher models, while SLA consolidates replayed historical teacher knowledge through slow, stable updates. Moreover, the layer-wise knowledge alignment further constrains representational drift across multiple teacher models, ensuring that replayed knowledge remains compatible with newly acquired teacher knowledge.

Overall, the results in Table II demonstrate that DBCL provides a more efective and stable solution for multi-teacher knowledge integration in ETA, significantly outperforming existing CL baselines.

## C. Teacher-Knowledge Acquisition and Retention Analysis

Following the overall performance evaluation, this subsection focuses on teacher knowledge acquisition and retention in multiple teacher CL. In particular, we evaluate how well the student maintains previously acquired teacher knowledge as new teachers are introduced. To this end, we report TA and TBT as defined in Section III-D, respectively.

As shown in Table III, MoE obtains TA values of 73.01%, 73.30%, 74.91%, and 74.88% on AppScanner, CUMUL, RDP, and BIND, respectively, while its TBT remains highly negative, ranging from −35.20% to −33.70%. This indicates that simply introducing multiple experts does not efectively preserve previously acquired teacher knowledge. MIND achieves higher TA values of 88.05%, 85.00%, 83.42%, and 87.65%, and reduces TBT to −10.00%, −15.01%, −13.20%, and −9.60%, respectively. However, it still underperforms DBCL in TA on all four teachers, suggesting that parameter isolation alleviates forgetting but remains insuficient for fully acquiring and retaining heterogeneous teacher knowledge.

Seq yields consistently large negative TBT, e.g., −38.85% on AppScanner, −34.38% on CUMUL, −35.60% on RDP, and −35.98% on BIND, indicating substantial degradation of earlier teacher knowledge after learning new teachers. ER and EWC reduce forgetting compared to Seq (e.g., improving TBT from −38.85% to −20.35% and −21.10% on AppScanner, respectively), but their TA remains markedly below the topperforming methods (e.g., 76.73%/77.10% vs. 91.54% on AppScanner). GEM and A-GEM further increase TA (e.g., up to 86.07% on AppScanner), yet noticeable forgetting persists (e.g., TBT of −11.73% and −11.33% on AppScanner, and −18.08% and −11.83% on BIND), suggesting that reducing gradient interference alone does not entirely prevent the loss of earlier teacher knowledge as more teachers are learned sequentially.

In contrast, DBCL achieves the most favorable balance between teacher-knowledge acquisition and retention. On App-Scanner, DBCL attains a TA of 91.54% and a TBT of only −8.60%, outperforming A-GEM (86.07%, −11.33%) and substantially reducing forgetting relative to Seq (72.91%, −38.85%). Similar advantages are observed for other teacher sequences, where DBCL consistently delivers the highest TA (87.06% on CUMUL, 88.12% on RDP, and 88.01% on BIND) while maintaining the least negative TBT (−9.15%, −12.85%, and −8.43%, respectively). These results indicate that DBCL better preserves previously learned teacher knowledge without sacrificing the efectiveness of learning new teachers.

TABLE III  
PERFORMANCE COMPARISON OF TEACHER-KNOWLEDGE ACQUISITION AND RETENTION IN MULTI-TEACHER CONTINUAL LEARNING

<table><tr><td rowspan="2">Method</td><td colspan="2">AppScanner</td><td colspan="2">CUMUL</td><td colspan="2">RDP</td><td colspan="2">BIND</td></tr><tr><td>TA (%)</td><td>TBT (%)</td><td>TA (%)</td><td>TBT (%)</td><td>TA (%)</td><td>TBT (%)</td><td>TA (%)</td><td>TBT (%)</td></tr><tr><td>MoE</td><td>73.01</td><td>-35.20</td><td>73.30</td><td>-34.21</td><td>74.91</td><td>-33.75</td><td>74.88</td><td>-33.70</td></tr><tr><td>MIND</td><td>88.05</td><td>-10.00</td><td>85.00</td><td>-15.01</td><td>83.42</td><td>-13.20</td><td>87.65</td><td>-9.60</td></tr><tr><td>Seq</td><td>72.91</td><td>-38.85</td><td>71.12</td><td>-34.38</td><td>72.52</td><td>-35.60</td><td>73.23</td><td>-35.98</td></tr><tr><td>ER</td><td>76.73</td><td>-20.35</td><td>74.22</td><td>-25.12</td><td>75.33</td><td>-20.10</td><td>74.84</td><td>-13.98</td></tr><tr><td>EWC</td><td>77.10</td><td>-21.10</td><td>74.49</td><td>-24.42</td><td>77.66</td><td>-18.38</td><td>73.66</td><td>-16.70</td></tr><tr><td>GEM</td><td>83.39</td><td>-11.73</td><td>79.89</td><td>-17.82</td><td>77.01</td><td>-14.75</td><td>83.09</td><td>-18.08</td></tr><tr><td>A-GEM</td><td>86.07</td><td>-11.33</td><td>85.53</td><td>-15.08</td><td>80.60</td><td>-16.07</td><td>84.24</td><td>-11.83</td></tr><tr><td>DBCL</td><td>91.54</td><td>-8.60</td><td>87.06</td><td>-9.15</td><td>88.12</td><td>-12.85</td><td>88.01</td><td>-8.43</td></tr></table>

(a) MoE  
![](images/d2eac8daaeffd1e8f938f1bebdaf9d3846a2314769b76ab725a16b54c3500d1a.jpg)

(b) MIND  
![](images/f93fb2255881c9b056fa288eac9285fe9c5d62deb906784539516a438dabc8ab.jpg)

(c) Seq  
![](images/47d08bcb3bc0290afeb767ccd559e390bfa9fbd97ef2b990bef5ff6161e96159.jpg)

(d) ER  
![](images/6b4f369a5c8d7ba3e727e19cc6df1df93cb51b7e1afaf1a44af25c23a7b2d30f.jpg)

(e) EWC  
![](images/ef3ce119e078da26ef19049fa8485e68883e3711538f705eb2f4b0a809d806e5.jpg)

(f) GEM  
![](images/af476e55749b98e120126d7e10af01c957ce6d5d38ce0939ca10f1b217408bf8.jpg)

(g) A-GEM  
![](images/fc941b7392cb567c06923c859d2aed3d3b036f0c2d6d908fcb4a173b68a7972e.jpg)

(h) DBCL  
![](images/f6560eda20f833fc537c81c23bd7224bd263374fd5fb1fb25b60b147726da4fb.jpg)  
Fig. 3. Accuracy heatmap illustrating teacher knowledge acquisition and retention across diferent continual learning stages.

To further analyze the dynamics of multi-teacher CL, Figure 3 visualizes the accuracy heatmaps at diferent learning stages. The horizontal axis denotes the teacher models, including AppScanner (E1), CUMUL (E2), RDP (E3), and BIND (E4). In contrast, the vertical axis reports the student’s accuracy on all previously learned teacher knowledge after each continual update. The diagonal entries represent the student’s accuracy on the currently learned teacher model after completing its knowledge integration, reflecting the efectiveness of learning new teacher knowledge. In contrast, the of-diagonal entries measure the student’s accuracy on previously learned teacher models, thereby characterizing the degree of teacher-knowledge retention as additional teacher models are sequentially incorporated.

While all methods demonstrate strong adaptation to newly introduced teachers, their retention of teacher knowledge diverges substantially. After learning the final teacher (E4), Seq’s accuracy on the first teacher (E1) drops to 48.5%, indicating severe teacher-knowledge forgetting. ER and EWC also sufer substantial performance degradation under the same setting, with accuracy reductions of up to 38.1% and 33.1%, respectively. In contrast, DBCL maintains an accuracy of 83.60% on E1 after learning E4, corresponding to only 9.9% forgetting. These results indicate that DBCL achieves significantly stronger teacher-knowledge retention throughout the CL process while efectively mitigating cumulative forgetting.

TABLE IV  
ABLATION CONFIGURATIONS FOR UNIFIED SEMANTIC SPACE CONSTRUCTION

<table><tr><td>Configuration</td><td>Meaning</td><td>Description</td></tr><tr><td>w/o NEI</td><td>Remove NEI</td><td>Use simple raw-feature textualization</td></tr><tr><td>w/o IC</td><td>Remove IC</td><td>Remove task instruction</td></tr><tr><td>NEI and IC</td><td>Complete</td><td>NEI, IC</td></tr></table>

## D. Ablation Study

(1) Unified Semantic Space Construction. To empirically validate the roles of NEI and IC, we conduct ablation studies, as summarized in Table IV.

w/o NEI: Without NEI, we replace NEI with a simple rawfeature textualization strategy. As shown in Fig. 4, removing NEI degrades the accuracy on most tasks. The results indicate that this strategy is not suitable for LLM-based student learning, because it provides little semantic information.

w/o IC: We remove the task instruction from the input while keeping NEI. The performance degradation shows that task instructions are important for conveying teacher-specific task semantics. Without such instructions, the student model cannot clearly identify which teacher-related decision rule or feature interpretation should be applied during inference.

![](images/040bb3114e937da3f571a48f5a5c996a7889efa42e7c37be15efe1eb7691b32e.jpg)  
Fig. 4. Accuracy Comparison under NEI and IC Ablations.

TABLE V  
ABLATION CONFIGURATIONS FOR CONTINUAL ANTI-FORGETTING DESIGN

<table><tr><td>Configuration</td><td>Meaning</td><td>Description</td></tr><tr><td>w/o FLA</td><td>Remove FLA</td><td>SLA, KAL</td></tr><tr><td>w/o SLA</td><td>Remove SLA</td><td>FLA, KAL</td></tr><tr><td>w/o KAL</td><td>Remove KAL</td><td>FLA, SLA</td></tr><tr><td>Full</td><td>Complete</td><td>FLA, SLA, KAL</td></tr></table>

![](images/1e1935a4d76f87cbc3e9d9b3097d0f4c01722aad017c855e6528def489df734b.jpg)  
Fig. 5. Training Loss Curve Comparison under Anti-forgetting Component Ablations.

We further note that if the teacher prediction results are not represented through the unified textual format, the student model has to rely on task-specific classification heads. Such a design can achieve comparable performance, but it requires architectural modification whenever a new teacher is introduced. In contrast, IC leverages the generative capability of the LLM and maps teacher outputs into a unified semantic space, allowing the same student architecture to handle diferent tasks.

(2) Continual Anti-forgetting Design. To investigate the individual and joint contributions of the core components in DBCL, we conduct ablation studies, and Table V summarizes the evaluated configurations. All ablation experiments follow the same multi-teacher continual learning protocol as the complete DBCL model; we only remove the corresponding component while keeping the remaining settings unchanged.

As shown in Fig. 5, removing SLA leads to pronounced training instability with sharp oscillations after 1200 steps, whereas the complete model converges faster and more stably. Figures 6 and 7 further report the final task-level performance, revealing the following insights.

![](images/84664515007dba0b5e894654a38757466801352ba590f7c4694372b97e1da132.jpg)  
Fig. 6. Accuracy Comparison under Anti-forgetting Component Ablations.

![](images/ac3daa2506f168c85f1251e6efd68a29fed98ca5c504f106e3a1635d8514044b.jpg)  
Fig. 7. F1 Comparison under Anti-forgetting Component Ablations.

w/o FLA: Without FLA, DBCL exhibits weaker teacherknowledge acquisition capability. Although training remains stable, convergence is delayed, and the final loss stays high. The F1 score further drops to 34.28% on Task 4, indicating reduced adaptability to newly introduced teacher models.

w/o SLA: Removing SLA causes drastic performance degradation (e.g., F1 drops to 44.14% on Task1 and 37.58% on Task4). Together with the loss oscillations in Fig. 5, this highlights the critical role of SLA in stabilizing learning dynamics and preserving previously acquired teacher-knowledge.

w/o KAL: Excluding the knowledge alignment loss moderately degrades performance. Although training stability is largely retained, the F1 scores on all tasks remain below the full model, e.g., 74.29% on Task 1 vs. 85.94% with the whole configuration, demonstrating the importance of KAL in reinforcing consistent teacher-knowledge transfer.

Full: With all components enabled, DBCL achieves the best results across all tasks. It delivers high F1 (e.g., 85.94% on task1) and fast, stable convergence, confirming the complementary synergy of FLA, SLA, and KAL in achieving both rapid teacher-knowledge acquisition and long-term retention.

## E. Additional Experiments

(1) Fine-tuning Module Selection. We further compare three fine-tuning target-module settings, including Attentiononly, FFN-only, and Attention+FFN. As reported in Table VI, FFN-only achieves a better balance between predictive performance and parameter eficiency. Therefore, we adopt FFN-only as the default setting in DBCL.

(2) Impact of Packet Sequence Length. We evaluate DBCL with diferent packet sequence lengths L ∈ {1 3 5 7}, as shown in Table VII. When L is small, the packet sequence provides insuficient trafic context, leading to inferior performance. Performance improves significantly as L increases to 5, but the gain becomes marginal when L further increases to 7. Therefore, we set $L = 5$ as a practical balance between performance and sequence complexity.

TABLE VI  
PERFORMANCE COMPARISON UNDER DIFFERENT FINE-TUNING MODULES

<table><tr><td rowspan="2">Module Selection</td><td rowspan="2">Trainable Params (M)</td><td colspan="2">Task1</td><td colspan="2">Task2</td><td colspan="2">Task3</td><td colspan="2">Task4</td></tr><tr><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td></tr><tr><td>Attention-only</td><td>7.7</td><td>80.12</td><td>79.20</td><td>81.72</td><td>80.33</td><td>79.85</td><td>79.10</td><td>72.30</td><td>70.00</td></tr><tr><td>FFN-only</td><td>14.2</td><td>86.18</td><td>85.94</td><td>84.26</td><td>83.89</td><td>83.00</td><td>82.95</td><td>75.80</td><td>74.33</td></tr><tr><td>Attention + FFN</td><td>21.8</td><td>86.30</td><td>85.00</td><td>83.60</td><td>82.43</td><td>82.73</td><td>80.55</td><td>77.61</td><td>76.20</td></tr></table>

TABLE VII

PERFORMANCE COMPARISON UNDER DIFFERENT PACKET SEQUENCE LENGTHS

<table><tr><td rowspan="2">Packet Sequence Lengths</td><td colspan="2">Task1</td><td colspan="2">Task2</td><td colspan="2">Task3</td><td colspan="2">Task4</td></tr><tr><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td></tr><tr><td>1</td><td>45.11</td><td>43.20</td><td>32.00</td><td>33.40</td><td>30.35</td><td>32.70</td><td>25.08</td><td>24.50</td></tr><tr><td>3</td><td>59.40</td><td>58.10</td><td>45.00</td><td>43.00</td><td>54.26</td><td>53.75</td><td>53.47</td><td>54.08</td></tr><tr><td>5</td><td>86.18</td><td>85.94</td><td>84.26</td><td>83.89</td><td>83.00</td><td>82.95</td><td>75.80</td><td>74.33</td></tr><tr><td>7</td><td>86.10</td><td>85.60</td><td>85.40</td><td>84.70</td><td>83.32</td><td>83.83</td><td>74.50</td><td>73.53</td></tr></table>

TABLE VIII

PERFORMANCE COMPARISON UNDER DIFFERENT TEACHER-NOISE RATIOS

<table><tr><td rowspan="2">Noise Ratio (%)</td><td colspan="2">Task1</td><td colspan="2">Task2</td><td colspan="2">Task3</td><td colspan="2">Task4</td></tr><tr><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td></tr><tr><td>0</td><td>86.18</td><td>85.94</td><td>84.26</td><td>83.89</td><td>83.00</td><td>82.95</td><td>75.80</td><td>74.33</td></tr><tr><td>10</td><td>82.10</td><td>82.60</td><td>79.40</td><td>78.70</td><td>75.32</td><td>73.83</td><td>70.00</td><td>69.00</td></tr><tr><td>20</td><td>79.34</td><td>78.13</td><td>75.20</td><td>73.30</td><td>74.00</td><td>73.00</td><td>63.56</td><td>64.75</td></tr><tr><td>30</td><td>65.78</td><td>63.60</td><td>62.35</td><td>63.47</td><td>60.28</td><td>62.30</td><td>55.06</td><td>54.10</td></tr><tr><td>50</td><td>40.60</td><td>41.30</td><td>32.49</td><td>33.23</td><td>30.20</td><td>30.60</td><td>32.80</td><td>33.40</td></tr></table>

TABLE IX

PERFORMANCE COMPARISON UNDER DIFFERENT BACKBONE SIZES

<table><tr><td rowspan="2">Backbone Size</td><td colspan="2">Task1</td><td colspan="2">Task2</td><td colspan="2">Task3</td><td colspan="2">Task4</td><td rowspan="2">Trainable Params (M)</td><td rowspan="2">GPU (GB)</td><td rowspan="2">Inference (second)</td></tr><tr><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td><td>AC(%)</td><td>F1(%)</td></tr><tr><td>Qwen3-0.6B</td><td>71.70</td><td>71.50</td><td>72.12</td><td>72.63</td><td>68.29</td><td>67.33</td><td>61.41</td><td>60.44</td><td>2.8</td><td>2.5</td><td>7.9</td></tr><tr><td>Qwen3-1.7B</td><td>73.69</td><td>72.50</td><td>74.19</td><td>73.26</td><td>71.63</td><td>70.57</td><td>65.92</td><td>64.83</td><td>5.5</td><td>5.6</td><td>9.1</td></tr><tr><td>Qwen3-4B</td><td>80.29</td><td>80.13</td><td>79.88</td><td>78.63</td><td>75.64</td><td>74.83</td><td>71.45</td><td>70.55</td><td>10.6</td><td>8.1</td><td>11.2</td></tr><tr><td>Qwen3-8B</td><td>86.18</td><td>85.94</td><td>84.26</td><td>83.89</td><td>83.00</td><td>82.95</td><td>75.80</td><td>74.33</td><td>14.2</td><td>18.3</td><td>12.1</td></tr><tr><td>Qwen3-14B</td><td>87.20</td><td>86.50</td><td>84.39</td><td>83.10</td><td>83.60</td><td>83.50</td><td>75.30</td><td>74.80</td><td>21.6</td><td>31.4</td><td>18.16</td></tr></table>

(3) Dependence on Teacher Quality. To analyze the dependence of DBCL on teacher quality, we inject diferent ratios of noise into teacher supervision. As shown in Table VIII, the performance gradually decreases as the teacher-noise ratio increases, indicating that DBCL is limited by the reliability of teacher supervision.

(4) Eficiency Analysis. To analyze the trade-of between model capacity and computational cost, we evaluate DBCL with diferent LLM backbone sizes. As shown in Table IX, smaller backbones require less GPU memory and inference time, but their performance is limited when integrating heterogeneous teacher knowledge. Although the 14B backbone slightly improves some task-level results, it introduces substantially higher memory consumption and inference cost, while the overall gain over the 8B model is limited. Therefore, the

8B backbone provides a favorable accuracy–eficiency tradeof and is adopted as the default backbone in DBCL. Due to GPU memory limitations, we leave the evaluation of larger backbones, such as 32B or 70B, to future work.

(5) Hyperparameter Sensitivity Analysis. To examine the influence of key hyperparameters on DBCL, we conduct a sensitivity analysis on the LoRA rank r, the EMA coeficient α, and the memory bufer size |M|, as shown in Fig. 8. (a) shows that increasing r improves the average accuracy from 77.30% to 82.90%, indicating that a larger adaptation rank enhances teacher-knowledge acquisition. However, the gain becomes marginal when r increases beyond 8, suggesting that r = 8 provides a practical balance between performance and parameter eficiency. (b) shows that $\alpha = 0 . 4$ achieves the best average accuracy, while either a smaller or larger EMA coeficient leads to performance degradation. This indicates that an appropriate EMA update rate is important for balancing fast adaptation and stable knowledge consolidation. (c) shows that a larger memory bufer improves TBT, demonstrating its efectiveness in preserving previously learned teacher knowledge. Nevertheless, increasing |M| also introduces additional memory overhead. Therefore, we set $| \mathcal { M } | = 2 0 0 0$ to balance knowledge retention and memory eficiency.

![](images/2288bda1e7740a32f8632db78912afd131a15ac74f6a042fd1a4dfd29e7b749b.jpg)

![](images/936d1e41c93dfa1a3e5a634d83ae88195734fafdddd655370dcf75756a4a8d40.jpg)

![](images/11a6787de8e3c080fc80ffbb673528c185aaa5df040f0a7c03899d050890182f.jpg)  
Fig. 8. Efects of the LoRA rank, EMA coeficient, and memory bufer size on DBCL.

## V. DISCUSSION

Although DBCL demonstrates promising performance in continual learning from multiple task-specific teacher models, it also has several issues that require further discussion.

Dependence on Teacher Quality. DBCL learns from teacher-generated supervision, and therefore its efectiveness inevitably depends on the quality and consistency of the teacher models. If a teacher model produces incorrect, biased, or poorly calibrated predictions, the student model may inherit such erroneous knowledge. This issue becomes more challenging in multi-teacher continual learning, where diferent teachers may have diferent error patterns or even provide conflicting supervision for semantically related trafic samples. Table VIII shows that unreliable teacher supervision can degrade the student performance, confirming the importance of teacher quality. However, the current framework does not explicitly estimate teacher reliability or correct erroneous knowledge. In future work, we plan to incorporate teacher reliability estimation and conflict detection among teachers to reduce the negative impact of low quality or inconsistent teacher supervision.

Sensitivity to the Quality of Textualization. NEI and IC provide a unified textual interface for heterogeneous trafic features and task semantics, enabling the LLM-based student to continually learn from diferent teachers under a common format. However, converting numerical trafic features and teacher outputs into natural language is not a lossless transformation. Fine-grained temporal patterns, feature correlations, and teacher confidence or calibration information may not be fully preserved in the textual representation. Future extensions may explore hybrid numerical-textual representations, confidence-aware answer formats, and more systematic instruction templates to better preserve low-level trafic semantics and uncertainty information.

Scalability and Deployment Cost. The current evaluation involves four task-specific teacher models, which cover heterogeneous feature spaces and ETA tasks. However, real-world ETA systems may involve a larger number of teacher models developed at diferent times and under diferent environments. Longer continual learning sequences may introduce stronger accumulated forgetting, larger replay memory requirements, and more complex teacher conflicts. We also acknowledge that using Qwen3-8B as the student backbone introduces non-negligible inference costs and a large memory footprint. Although LoRA reduces fine-tuning cost by updating only a small number of trainable parameters, it does not eliminate the deployment cost of the backbone model during inference. Therefore, DBCL does not necessarily guarantee a lower inference cost or memory footprint than each lightweight taskspecific teacher model. Future work will investigate more eficient backbones, model quantization, adapter compression, and dynamic memory management. We will also evaluate DBCL with more teacher models and longer learning sequences to further validate its scalability and practical applicability.

Comparison with a Routing-based Strategy. In practical ETA scenarios, a routing-based strategy is a reasonable alternative. When task boundaries are clearly defined and reliable task assignment is available, a router can first identify the task type or select the appropriate model, and then apply the corresponding task-specific model for inference. This strategy can preserve the specialized capability of each teacher model. However, reliable routing can be non-trivial. For an incoming encrypted trafic sample, a routing-based strategy needs to determine which task-specific model the encrypted trafic sample should be assigned to before inference. This task identification step may be dificult when task boundaries are ambiguous, trafic patterns evolve over time, or labeled data for training a reliable router are unavailable. Moreover, routing and DBCL address diferent objectives. Routing mainly solves the problem of model selection, whereas DBCL focuses on continual model-level knowledge consolidation. Directly deploying multiple teachers through routing preserves the knowledge within separate specialized models, but it does not directly address how the knowledge from these models can be accumulated, transferred, and retained within a unified model. In contrast, DBCL constructs a single evolving student model that continually learns from newly available teachers while retaining previously acquired teacher knowledge.

## VI. THEORETICAL ANALYSIS

## A. Efect of NEI and IC

NEI unifies heterogeneous trafic features and task semantics by transforming both numerical trafic features and teacher predictions into a shared linguistic space.

Formally, let X denote the heterogeneous numerical traffic features, U the semantic priors provided by NEI, and $\hat { X } ~ = ~ \Phi ( X , U )$ the textualized feature representation. Note that X<sup>ˆ</sup> is a deterministic function of (X U), and thus conditioning on (X U) is equivalent to conditioning on X<sup>ˆ</sup> in terms of available information. Let $\hat { Y }$ denote the textualized representations of teacher model predictions provided by NEI. According to the definition of conditional mutual information [64],

$$
I _ {q} (\hat {Y}; U \mid X) = H _ {q} (\hat {Y} \mid X) - H _ {q} (\hat {Y} \mid X, U),\tag{20}
$$

where $I _ { q }$ denotes conditional mutual information and $H _ { q }$ denotes conditional entropy. Since $I _ { q } ( \hat { Y } ; U \mid X ) \ge 0$ , we have

$$
H _ {q} (\hat {Y} \mid X, U) \leq H _ {q} (\hat {Y} \mid X),\tag{21}
$$

indicating that the semantic priors U reduce the conditional uncertainty of $\hat { Y }$ given X. This reduction in conditional entropy stabilizes the student model’s acquisition of teacher knowledge.

IC provides explicit semantic guidance to the student model. Without instructions, the model has to learn a single mapping:

$$
f: \hat {X} \to \hat {Y}.\tag{22}
$$

In particular, there may exist ${ \hat { X } } ^ { * }$ such that

$$
(\hat {X} ^ {*}, \hat {Y} _ {i}) \in \mathcal {D} _ {i}, (\hat {X} ^ {*}, \hat {Y} _ {j}) \in \mathcal {D} _ {j}, \hat {Y} _ {i} \neq \hat {Y} _ {j},\tag{23}
$$

where $i , j \in \{ 1 , \ldots , T \}$ index two distinct teacher models, and $\mathcal { D } _ { i }$ and $\mathcal { D } _ { j }$ denote their corresponding datasets. In such cases, no single-valued function $f ( { \hat { X } } )$ can satisfy all ${ \hat { Y } } ,$ rendering the learning problem ill-posed.

IC reduces this ambiguity by turning the problem into a conditional mapping:

$$
f: (\hat {X}, I) \to \hat {Y},\tag{24}
$$

where I denotes the instruction. This conditional formulation enables the model to activate the appropriate trafic feature interpretation based on the instruction, thereby supporting multi-task ETA within a unified architecture.

## B. Efect of Dual-Branch Continual Learning

When the student model learns sequentially from multiple teacher models, each update shifts the model parameters θ to fit the current teacher. However, this shift may cause θ to deviate from previous optima, resulting in the forgetting of earlier teacher knowledge.

Let ${ \mathcal { L } } ^ { i } ( \theta )$ denote the loss between the student and the i-th teacher model. When learning the j-th teacher model, the total loss is defined as:

$$
\mathcal {L} (\theta) = \mathcal {L} ^ {j} (\theta) + \sum_ {i = 1} ^ {j - 1} \mathcal {L} ^ {i} (\theta).\tag{25}
$$

Since prior knowledge from earlier models is not revisited during learning, we approximate each historical loss ${ \mathcal { L } } ^ { i } ( \theta )$ using a second-order Taylor expansion at the parameter value $\hat { \theta } ^ { i }$ (the student model parameters immediately after learning the i-th teacher):

$$
\begin{array}{l} \mathcal {L} ^ {i} (\theta) \approx \underbrace {\mathcal {L} ^ {i} (\hat {\theta} ^ {i})} _ {\text {(a)}} + \underbrace {(\theta - \hat {\theta} ^ {i}) ^ {\top} \nabla_ {\theta} \mathcal {L} ^ {i} (\hat {\theta} ^ {i})} _ {\text {(b)}} \\ \qquad + \underbrace {\frac {1}{2} (\theta - \hat {\theta} ^ {i}) ^ {\top} \mathbf {H} ^ {i} (\theta - \hat {\theta} ^ {i})} _ {\text {(c)}}, \end{array}\tag{26}
$$

where $\mathbf { H } ^ { i } = \nabla _ { \theta } ^ { 2 } \mathcal { L } ^ { i } ( \hat { \theta } ^ { i } )$ denote the Hessian matrix of the i-th loss.

In practice, since the learning typically converges at the end of each teacher model, the gradient term (b) is near zero and can be ignored. The constant term (a) is also irrelevant to optimization. Therefore, the cumulative objective reduces to:

$$
\mathcal {L} (\theta) = \mathcal {L} ^ {j} (\theta) + \frac {1}{2} \sum_ {i = 1} ^ {j - 1} (\theta - \hat {\theta} ^ {i}) ^ {\top} \mathbf {H} ^ {i} (\theta - \hat {\theta} ^ {i}).\tag{27}
$$

Taking the gradient of Eq. 27 with respect to $\theta ,$ we obtain:

$$
\nabla_ {\theta} \mathcal {L} (\theta) = \nabla_ {\theta} \mathcal {L} ^ {j} (\theta) + \sum_ {i = 1} ^ {j - 1} H ^ {i} (\theta - \hat {\theta} ^ {i}).\tag{28}
$$

Assuming that the parameter θ remains within a neighbor hood $\cup _ { i = 1 } ^ { j - 1 } \bar { \mathcal { N } } ^ { i }$ of previously learned optima (where ${ \mathcal { N } } ^ { i } = \{ \theta$ $d ( \theta , { \hat { \theta } } ^ { i } ) < \delta ^ { i } \} )$ , we can make the approximation:

$$
\sum_ {i = 1} ^ {j - 1} \mathbf {H} ^ {i} (\theta - \hat {\theta} ^ {i}) \approx \left(\sum_ {i = 1} ^ {j - 1} \mathbf {H} ^ {i}\right) (\theta - \hat {\theta} ^ {j - 1}).\tag{29}
$$

Let $\nabla _ { \theta } \mathcal { L } ( \theta ) = 0$ , we can obtain the following iterative update rule: 1

$$
\theta \leftarrow \theta - \alpha \left(\sum_ {i = 1} ^ {j - 1} \mathbf {H} ^ {i}\right) ^ {- 1} \nabla_ {\theta} \mathcal {L} ^ {j} (\theta),\tag{30}
$$

where $\alpha$ is the learning rate, and $\left( \textstyle \sum _ { i = 1 } ^ { j - 1 } \mathbf { H } ^ { i } \right) ^ { - 1 }$ represents the inverse of the accumulated Hessian matrices from all previous teacher models, which suppresses changes to parameters crucial for previous teachers.

The above analysis reveals that catastrophic forgetting arises from unconstrained parameter updates that deviate from the optima of previously learned teacher models. In principle, mitigating forgetting requires suppressing updates along parameter directions that are strongly constrained by the accumulated curvature (Hessian) of historical teacher losses. However, explicitly computing and inverting the aggregated Hessian matrix is infeasible for large-scale neural models.

DBCL provides a practical approximation of this theoretical principle through a dual-branch learning architecture and auxiliary constraints. Specifically, the replay bufer ensures that supervision signals from previously learned teacher models are periodically revisited, which implicitly reintroduces historical loss curvature into the optimization process.

The FLA is designed to rapidly adapt to the current teacher model, capturing task-specific gradients corresponding to $\nabla _ { \boldsymbol { \theta } } \mathcal { L } ^ { j } ( \boldsymbol { \theta } )$ . In contrast, the SLA updated via an exponential moving average, maintains a smoothed parameter trajectory that approximates a long-term consensus of previously learned optima. This separation efectively decomposes the parameter space into plastic and stable components, reducing destructive interference between new and old knowledge.

Furthermore, the KAL enforces consistency at the representation level between the FLA and the SLA on replayed samples. This constraint acts as an implicit second-order regularization, discouraging the FLA from drifting along parameter directions that would significantly alter the representations encoding prior teacher knowledge. As a result, the combined efect of replay, dual-branch parameterization, and representation alignment approximates the ideal Hessian-weighted update rule derived above, without explicitly computing second-order information.

Together, these mechanisms enable DBCL to efectively mitigate forgetting in sequential model-to-model learning while retaining suficient plasticity to acquire new teacher knowledge, as corroborated by the empirical results.

## VII. CONCLUSION

In this paper, we study a practical yet underexplored problem in ETA: how to construct a unified model that continually learns from multiple task-specific ETA models using teachergenerated predictions rather than raw labeled data. To this end, we propose the DBCL framework, which formulates ETA as a continual learning problem at the model level, rather than the conventional data-centric paradigm. DBCL provides an efective solution for unifying heterogeneous feature spaces and task semantics while maintaining long-term teacher knowledge retention. Extensive experiments on four public encrypted trafic datasets reveal three key findings. First, DBCL achieves the best performance, with accuracies of 86.18%, 84.26%, 83.00%, and 75.80% across the four ETA tasks, respectively, showing its ability in consolidating heterogeneous teacher knowledge into a unified student model. Second, DBCL obtains the highest teacher knowledge accuracy across all four teacher models, with TA values of 91.54%, 87.06%, 88.12%, and 88.01%, indicating that it can more efectively acquire knowledge from newly introduced teacher models. Third, DBCL maintains less negative TBT values, suggesting that it better retains previously learned teacher knowledge and efectively mitigates the forgetting of such knowledge. These results empirically validate the feasibility of constructing unified ETA models through continual acquisition of teacher knowledge from multiple task-specific models. Future work will focus on selective teacher knowledge acquisition and reducing the memory overhead of replay bufers, thereby enabling longterm and sustainable model-to-model learning in ETA.

## REFERENCES

[1] M. Shen, J. Wu, K. Ye, K. Xu, G. Xiong, and L. Zhu, “Robust detection of malicious encrypted trafic via contrastive learning,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 4228–4242, 2025.

[2] Q. Meng et al., “Detection of unknown attacks through encrypted trafic: A Gaussian prototype-aided variational autoencoder framework,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 10652–10667, 2025.

[3] J. Kotak, I. Yankelev, I. Bibi, Y. Elovici, and A. Shabtai, “VPN-encrypted network trafic classification using a time-series approach,” IEEE Trans. Netw. Service Manage., vol. 22, no. 2, pp. 2225–2242, Apr. 2025.

[4] Z. Hua, Z. Wang, M. Song, Y. Zheng, G. Xu, and X. Jia, “Enabling secure auditing and deduplication in multi-replica cloud storage,” IEEE Trans. Dependable Secure Comput., vol. 22, no. 6, pp. 6653–6670, Nov. 2025.

[5] Y. Qing et al., “Low-quality training data only? A robust framework for detecting encrypted malicious network trafic,” in Proc. Netw. Distrib. Syst. Secur. Symp., 2024.

[6] J. Yoon, S. Do, D. Kim, T. Chung, and K. Park, “mmTLS: Scaling the performance of encrypted network trafic inspection,” in Proc. USENIX Annu. Tech. Conf. (USENIX ATC), 2024, pp. 631–647.

[7] Q. Yuan et al., “Multi-agent for network security monitoring and warning: A generative AI solution,” IEEE Netw., vol. 39, no. 5, pp. 114–121, Sep. 2025.

[8] X. Wang et al., “Entropy-regulated cross-modal generative fusion for multimodal network intrusion detection,” Inf. Fusion, vol. 126, Feb. 2026, Art. no. 103581.

[9] X. Wang, Q. Yuan, Y. Wang, J. Teng, J. Tao, and M. Shen, “Zero trust-driven collaborative intrusion detection in IoT: A continuous trust assessment approach,” IEEE Internet Comput., vol. 29, no. 4, pp. 37–47, Apr. 2025.

[10] A. Alipour-Fanid, M. Dabaghchian, N. Wang, P. Wang, L. Zhao, and K. Zeng, “Machine learning-based delay-aware UAV detection and operation mode identification over encrypted Wi-Fi trafic,” IEEE Trans. Inf. Forensics Security, vol. 15, pp. 2346–2360, 2020.

[11] M. Shen, Y. Liu, L. Zhu, X. Du, and J. Hu, “Fine-grained webpage fingerprinting using only packet length information of encrypted trafic,” IEEE Trans. Inf. Forensics Security, vol. 16, pp. 2046–2059, 2021.

[12] S. Cui, C. Dong, M. Shen, Y. Liu, B. Jiang, and Z. Lu, “CBSeq: A channel-level behavior sequence for encrypted malware trafic detection,” IEEE Trans. Inf. Forensics Security, vol. 18, pp. 5011–5025, 2023.

[13] X. Xiao et al., “RBLJAN: Robust byte-label joint attention network for network trafic classification,” IEEE Trans. Dependable Secure Comput., vol. 22, no. 3, pp. 2161–2178, May 2025.

[14] L. Yang et al., “Robustness matters: Pre-training can enhance the performance of encrypted trafic analysis,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 10588–10603, 2025.

[15] X. Lin et al., “Respond to change with constancy: Instruction-tuning with LLM for non-I.I.D. network trafic classification,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 5758–5773, 2025.

[16] K. Chen et al., “Robust intrusion detection in CPS: A pre-trainingbased multi-view feature collaboration and correlation analysis method,” Comput. Netw., vol. 279, Apr. 2026, Art. no. 112129.

[17] R. Zhao et al., “Yet another trafic classifier: A masked autoencoder based trafic transformer with multi-level flow representation,” in Proc. AAAI Conf. Artif. Intell., 2023, vol. 37, no. 4, pp. 5420–5427.

[18] G. Zhou, X. Guo, Z. Liu, T. Li, Q. Li, and K. Xu, “TraficFormer: An eficient pre-trained model for trafic data,” in Proc. IEEE Symp. Secur. Privacy (SP), May 2025, pp. 1844–1860.

[19] H. Zheng et al., “Learning from models beyond fine-tuning,” Nature Mach. Intell., vol. 7, no. 1, pp. 6–17, Jan. 2025.

[20] Q. Meng et al., “Fine-grained detection and analysis of unknown encrypted malicious trafic from mixed noisy labels,” IEEE Trans. Dependable Secure Comput., early access, May 28, 2026, doi: 10.1109/ TDSC.2026.3697849.

[21] J. Zhang, S. Elnikety, S. Zarar, A. Gupta, and S. Garg, “Modelswitching: Dealing with fluctuating workloads in machine-learning-asa-service systems,” in Proc. 12th USENIX Workshop Hot Topics Cloud Comput. (HotCloud), 2020.

[22] K. Gai, Z. Wang, J. Yu, and L. Zhu, “MUFTI: Multi-domain distillationbased heterogeneous federated continuous learning,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 2721–2733, 2025.

[23] S. Wang, X. Li, J. Sun, and Z. Xu, “Training networks in null space of feature covariance with self-supervision for incremental learning,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 47, no. 4, pp. 2563–2580, Apr. 2025.

[24] S. A. Baset and H. G. Schulzrinne, “An analysis of the skype peer-topeer internet telephony protocol,” in Proc. IEEE 25th IEEE Int. Conf. Comput. Commun., Apr. 2006, pp. 1–11.

[25] A. Sharma and A. H. Lashkari, “A survey on encrypted network traffic: A comprehensive survey of identification/classification techniques, challenges, and future directions,” Comput. Netw., vol. 257, Feb. 2025, Art. no. 110984.

[26] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “AppScanner: Automatic fingerprinting of smartphone apps from encrypted network trafic,” in Proc. IEEE Eur. Symp. Secur. Privacy, Mar. 2016, pp. 439–454.

[27] A. Panchenko et al., “Website fingerprinting at internet scale,” in Proc. Netw. Distrib. Syst. Secur. Symp., 2016, p. 23477.

[28] Y. Choi, J. Yu, K.-J. Koo, and D. Moon, “Encrypted network trafic feature extraction for application classification,” in Proc. 16th Int. Conf. Inf. Commun. Technol. Converg. (ICTC), Oct. 2025, pp. 938–939.

[29] C. Chakravorty, S. Prajwal, and S. Punith, “Anomaly detection in encrypted network trafic using deep learning,” in Proc. 9th Int. Conf. Comput. Syst. Inf. Technol. Sustain. Solutions (CSITSS), Nov. 2025, pp. 01–07.

[30] H. K. Pedarla, “Encrypted trafic analytics (ETA): Machine learning approaches for intrusion detection without decryption,” Int. J. Sci. Technol., vol. 16, no. 4, pp. 1–10, Nov. 2025.

[31] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “ET-BERT: A contextualized datagram representation with pre-training transformers for encrypted trafic classification,” in Proc. ACM Web Conf., Apr. 2022, pp. 633–642.

[32] X. Meng, C. Lin, Y. Wang, and Y. Zhang, “NetGPT: Generative pretrained transformer for network trafic,” 2023, arXiv:2304.09513.

[33] J. Qu, X. Ma, and J. Li, “TraficGPT: Breaking the token barrier for eficient long trafic analysis and generation,” 2024, arXiv:2403.05822.

[34] G. Hinton, O. Vinyals, and J. Dean, “Distilling the knowledge in a neural network,” 2015, arXiv:1503.02531.

[35] Z. Zhu, J. Hong, and J. Zhou, “Data-free knowledge distillation for heterogeneous federated learning,” in Proc. Int. Conf. Mach. Learn., 2021, pp. 12878–12889.

[36] J. Yoo, M. Cho, T. Kim, and U. Kang, “Knowledge extraction with no observable data,” in Proc. Adv. Neural Inf. Process. Syst., vol. 32, 2019, pp. 2701–2710.

[37] M. Lu, B. Zhou, and Z. Bu, “Two-stage distillation-aware compressed models for trafic classification,” IEEE Internet Things J., vol. 10, no. 16, pp. 14152–14166, Aug. 2023.

[38] S. Li, Y. Cao, G. Peng, M. Li, W. Sun, and L. Chen, “Eficient intrusion detection for in-vehicle networks using knowledge distillation from BERT to CNN-BiLSTM,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 6398–6412, 2025.

[39] Y. Liu et al., “Knowledge distillation via instance relationship graph,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2019, pp. 7096–7104.

[40] Y. Zhu and Y. Wang, “Student customized knowledge distillation: Bridging the gap between student and teacher,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), Oct. 2021, pp. 5057–5066.

[41] Z. Wang, K. Zhang, S. Yang, D. He, and S. Chan, “Enhancing Android malware detection via knowledge distillation on homogenized function call graphs,” Knowl.-Based Syst., vol. 323, Jul. 2025, Art. no. 113687.

[42] F. Ye and A. G. Bors, “Lifelong teacher–student network learning,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 44, no. 10, pp. 6280–6296, Oct. 2022.

[43] M. De Lange et al., “A continual learning survey: Defying forgetting in classification tasks,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 44, no. 7, pp. 3366–3385, Jul. 2022.

[44] M. Pennisi et al., “Experience replay as an efective strategy for optimizing decentralized federated learning,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. Workshops (ICCVW), Oct. 2023, pp. 3368–3375.

[45] D. Lopez-Paz and M. Ranzato, “Gradient episodic memory for continual learning,” in Proc. Adv. Neural Inf. Process. Syst., vol. 30, 2017, pp. 6467–6476.

[46] A. Chaudhry, M. Ranzato, M. Rohrbach, and M. Elhoseiny, “Eficient lifelong learning with a-GEM,” in Proc. Int. Conf. Learn. Represent., 2019.

[47] P. Buzzega, M. Boschini, A. Porrello, D. Abati, and S. Calderara, “Dark experience for general continual learning: A strong, simple baseline,” in Proc. Int. Conf. Neural Inf. Process. Syst., 2020, pp. 15920–15930.

[48] W. Huang, M. Ye, and B. Du, “Learn from others and be yourself in heterogeneous federated learning,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2022, pp. 10143–10153.

[49] F. Du, Y. Yang, Z. Zhao, and Z. Zeng, “Eficient perturbation inference and expandable network for continual learning,” Neural Netw., vol. 159, pp. 97–106, Feb. 2023.

[50] K. Ksi azekand P. Spurek, “HyperMask: Adaptive hypernetwork-based˙ masks for continual learning,” Neural Netw., vol. 191, Nov. 2025, Art. no. 107736.

[51] Y. Li, R. Zhang, J. C. Lu, and E. Shechtman, “Few-shot image generation with elastic weight consolidation,” in Proc. Adv. Neural Inf. Process. Syst., vol. 33, 2020, pp. 15885–15896.

[52] F. Zenke, B. Poole, and S. Ganguli, “Continual learning through synaptic intelligence,” in Proc. Int. Conf. Mach. Learn., 2017, pp. 3987–3995.

[53] R. Aljundi, F. Babiloni, M. Elhoseiny, M. Rohrbach, and T. Tuytelaars, “Memory aware synapses: Learning what (not) to forget,” in Proc. Eur. Conf. Comput. Vis. (ECCV), Sep. 2018, pp. 139–154.

[54] A. Yang et al., “Qwen3 technical report,” 2025, arXiv:2505.09388.

[55] E. J. Hu et al., “LoRa: Low-rank adaptation of large language models,” in Proc. ICLR, 2022, vol. 1, no. 2, p. 3.

[56] J. S. Vitter, “Random sampling with a reservoir,” ACM Trans. Math. Softw., vol. 11, no. 1, pp. 37–57, Mar. 1985.

[57] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware trafic classification using convolutional neural network for representation learning,” in Proc. Int. Conf. Inf. Netw. (ICOIN), Da Nang, Vietnam, Jan. 2017, pp. 712–717.

[58] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of encrypted and VPN trafic using time-related features,” in Proc. 2nd Int. Conf. Inf. Syst. Secur. Privacy, 2016, pp. 407–414.

[59] E. C. P. Neto, S. Dadkhah, R. Ferreira, A. Zohourian, R. Lu, and A. A. Ghorbani, “CICIoT2023: A real-time dataset and benchmark for large-scale attacks in IoT environment,” Sensors, vol. 23, no. 13, p. 5941, Jun. 2023.

[60] M. Jiang, G. Gou, J. Shi, and G. Xiong, “I know what you are doing with remote desktop,” in Proc. IEEE 38th Int. Perform. Comput. Commun. Conf. (IPCCC), London, U.K., Oct. 2019, pp. 1–7.

[61] K. Al-Naami et al., “Adaptive encrypted trafic fingerprinting with bidirectional dependence,” in Proc. 32nd Annu. Conf. Comput. Secur. Appl., Dec. 2016, pp. 177–188.

[62] M. Sun, Y. Wang, T. Feng, D. Zhang, Y. Zhu, and J. Tang, “A stronger mixture of low-rank experts for fine-tuning foundation models,” in Proc. Int. Conf. Mach. Learn., vol. 267, 2025, pp. 57712–57727.

[63] J. Bonato, F. Pelosin, L. Sabetta, and A. Nicolosi, “Mind: Multi-task incremental network distillation,” in Proc. AAAI Conf. Artif. Intell., 2024, vol. 38, no. 10, pp. 11105–11113.

[64] T. M. Cover et al., “Entropy, relative entropy and mutual information,” Elements Inf. Theory, vol. 2, no. 1, pp. 12–13, 1991.
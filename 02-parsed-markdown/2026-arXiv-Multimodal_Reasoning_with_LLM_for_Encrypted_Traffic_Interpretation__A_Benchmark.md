# Multimodal Reasoning with LLM for Encrypted Traffic Interpretation: A Benchmark

Longgang Zhang, Xiaowei Fu, Fuxiang Huang, and Lei Zhang, Senior Member, IEEE

Abstract—Network traffic, as a key media format, is crucial for ensuring security and communications in modern internet infrastructure. While existing methods offer excellent performance, they face two key bottlenecks: (1) They fail to capture multidimensional semantics beyond unimodal sequence patterns. (2) Their “black box” property, i.e., providing only category labels, lacks an auditable reasoning process. We identify a key factor that existing network traffic datasets are primarily designed for classification and inherently lack rich semantic annotations, failing to generate human-readable evidence report. To address data scarcity, this paper proposes a Byte-Grounded Traffic Description (BGTD) benchmark for the first time, combining raw bytes with structured expert annotations. BGTD provides necessary behavioral features and verifiable chains of evidence for multimodal reasoning towards explainable encrypted traffic interpretation. Built upon BGTD, this paper proposes an end-to-end traffic-language representation framework (mmTraffic), a multimodal reasoning architecture bridging physical traffic encoding and semantic interpretation. In order to alleviate modality interference and generative hallucinations, mmTraffic adopts a jointly-optimized perception-cognition architecture. By incorporating a perceptioncentered traffic encoder and a cognition-centered LLM generator, mmTraffic achieves refined traffic interpretation with guaranteed category prediction. Extensive experiments demonstrate that mmTraffic autonomously generates high-fidelity, human-readable, and evidence-grounded traffic interpretation reports, while maintaining highly competitive classification accuracy comparing to specialized unimodal model (e.g., NetMamba). The source code is available at Traffic-Reasoning-Project.

Index Terms—Encrypted traffic classification, network traffic interpretation, large language model, multimodal learning.

# I. INTRODUCTION

N ETWORK traffic analysis is a core pillar for ensuringnetwork security, implementing intrusion detection, and network security, implementing intrusion detection, and conducting traffic engineering. With the widespread deployment of Transport Layer Security (TLS 1.3), Quick UDP Connections (QUIC), and anonymous routing networks such as Tor [9], endto-end encryption has made payload content extremely opaque. This evolution has rendered traditional Deep Packet Inspection (DPI) mechanisms, relying on plaintext signature matching, largely ineffective. Facing this challenge, encrypted traffic classification techniques have emerged. These methods heavily

This work was partially supported by National Natural Science Fund of China under Grants 92570110 and 62271090, Chongqing Natural Science Fund under Grant CSTB2024NSCQ-JQX0038, and National Youth Talent Project. (Corresponding author: Lei Zhang)

L. Zhang, X. Fu and L. Zhang are with the School of Microelectronics and Communication Engineering, Chongqing University, Chongqing 400044, China. (E-mail: zlg502361@gmail.com, xwfu@cqu.edu.cn, leizhang@cqu.edu.cn,)

Fuxiang Huang is with the School of Data Science, Lingnan University, Hong Kong, China. (E-mail: fxhuang1995@gmail.com)

Manuscript received April 19, 2015; revised August 16, 2015.

![](images/7489b0ab3b21fba35f77f89167bb935254d4cfdb41fc780976647587f7085578.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Raw Traffic Bytes"] --> B["Traditional Classifier"]
    B --> C["Malicious (Tor)"]
    C --> D["Offsets 42 has a weight of 0.8* (meaning it has no practical operational value)"]
    E["Raw Traffic Bytes"] --> F["Perception Traffic Encoder"]
    F --> G["Cognitive LLM"]
    G --> H["Evidence-Grounded Forensic Report &quot;class&quot; Malicious (Tor)&quot;traits&quot; TLS 1.3&quot;evidence&quot; high entropy, low ASCII ratio&quot;description&quot; Automated Tor malware C2 beaconing with high-entropy, low throughput payloads &quot;notes&quot; Persistent and low throughput"]
    I["Byte-Grounded Knowledge"] --> J["End"]
    style A fill:#99CCFF,stroke:#333
    style E fill:#99CCFF,stroke:#333
    style I fill:#99CCFF,stroke:#333
    style B fill:#E6F5FF,stroke:#333
    style C fill:#E6F5FF,stroke:#333
    style D fill:#E6F5FF,stroke:#333
    style F fill:#E6F5FF,stroke:#333
    style G fill:#E6F5FF,stroke:#333
    style H fill:#E6F5FF,stroke:#333
    style I fill:#E6F5FF,stroke:#333
```
</details>

Fig. 1. Comparison of traffic analysis paradigms. (a) Traditional classification methods that act as a “black box”, providing only a label and low-level feature weights that lack operational value. (b) Our proposed multimodal reasoning framework, composed of a Traffic Perception Encoder and a Cognitive LLM, instructed by Byte-Grounded Knowledge, generating an evidence-grounded report with human-understandable reasoning and executable insights.

relied on statistical features (e.g., packet size distribution and arrival time intervals, etc.) and machine learning techniques, but struggled to adapt to the highly-dimensional and dynamic adversarial nature of modern network traffic. In contrast, deep learning (DL) models achieved significant performance improvements by automatically extracting hierarchical representations from raw byte sequences. In recent years, inspired by the success of self-supervised pre-training in large models, traffic analysis models based on Transformers [33] and state space models (SSMs) [13] are emerged. For example, ET-BERT [19] introduced a masked burst flow model, MPAF [6] proposed a multi-phase attribute fingerprint, YaTC [38] proposed a multi-level flow representation (MFR) matrix, NetMamba [34] achieved ultra-fast inference using the linear-time complexity of the Mamba architecture, FlowletFormer [22] further optimized alignment capabilities by introducing behavior-semantic-aware Flowlet units, and WF-Transformer [39] further proposed a Transformer-based temporal feature extraction method.

Despite the empirical success of deep representation learning models, contemporary cryptographic traffic analysis models remain constrained by two key bottlenecks: (1) Semantic Void in Unimodal Representations. Existing models essentially perform nonlinear boundary partitioning in a high-dimensional space, directly mapping pure numerical hexadecimal byte sequences to classification labels. In complex enterprise environments, security analysts often encounter the “statistical twin” phenomenon, i.e., benign traffic and malicious traffic employing obfuscation techniques exhibit almost identical statistical distributions. Relying solely on unimodal sequence patterns makes these models inadequate to capture the rich, multidimensional semantics required to distinguish such threats. (2) Black-box Property and Limitations of Traditional Explainable Artificial Intelligence (XAI). Purely statistical classifiers cannot provide human-readable, auditable, protocol-level forensic evidence to justify their decisions. While post-hoc interpretation techniques (e.g., SHAP [25], LIME [30] and Grad-CAM [31]) attempted to address this, they can only generate importance scores for features or attention heatmaps. For frontline Security Operations Center (SOC) analysts, knowing that “the byte with offset 42 has high weight” is of no operational value unless the byte can be logically mapped to a specific protocol anomaly, such as a malformed handshake frame or an illegal cipher suite.

To overcome the aforementioned semantic limitations and black-box constraints, the deep model is expected to learn to map low-level physical bytes to high-level protocol semantics. However, existing network traffic datasets are primarily collected for the traditional classification task, providing only discrete category labels and inherently lacking the rich, multidimensional semantic annotations required, and thus unable to train generative interpretable models. To bridge this fundamental gap, we innovatively construct a Byte-Grounded Traffic Description (BGTD) dataset. To the best of our knowledge, BGTD is the first benchmark that explicitly pairs raw network traffic bytes with structured, rich expert knowledge. To ensure strong generalization capabilities, the dataset integrates six authoritative public repositories covering a broad ecosystem of applications. Beyond basic classification, BGTD provides fine-grained semantic annotations such as discriminative behavioral features, verifiable chains of evidence, and natural language descriptions. These elements are constructed through an automated expert knowledge generation process powered by Claude Opus. By linking numerical payloads with the highlevel forensic information, BGTD provides the key foundational data required for multimodal reasoning.

Building upon this multimodal benchmark, this paper proposes an end-to-end, multi-modal traffic-language representation framework (mmTraffic) to overcome the inherent limitations of semantic void and black-box property in traditional traffic classifiers. Unlike traditional pipelines that strictly freeze the traffic encoder to prevent catastrophic forgetting and often lead to weak semantic alignment, mmTraffic advocates for a joint optimization for perception and cognition modules. By introducing an auxiliary classification head in perception and a semantic-priority guided generation mechanism in cognition, our framework explicitly constrains the continuous feature space and forces the large language model (LLM) to perform accurate classification before reasoning. This intrinsically empowers LLM to understand non-semantic traffic bytes and generate human-readable, evidence-grounded reports.

Fig. 1 describes the paradigm difference between mmTraffic and others. The main contributions are summarized as follows:

• A Byte-grounded traffic description benchmark (BGTD). We construct the first benchmark to explicitly pair raw network traffic bytes with structured expert

knowledge. By providing discriminative behavioral traits and verifiable chains of evidence, BGTD bridges the fundamental data-knowledge gap and enables multimodal reasoning towards interpretable encrypted traffic analysis.

• A multi-modal traffic reasoning framework (mmTraffic). We reformulate encrypted traffic analysis as a jointly optimized multimodal alignment pipeline. By unfreezing the traffic encoder and training it synergistically with the LLM, we achieve a deep semantic mapping from physical network bytes to human-readable concepts.   
• Auxiliary constraint and semantic-priority generation. We introduce a classification head to enforce discriminative constraints on the traffic encoder. Furthermore, we design a semantic-priority generation loss that dynamically assigns higher weights to the categorical tokens, effectively mitigating LLM hallucinations in category prediction and ensuring the quality of generated reports.   
• Superior performance of traffic interpretation with classification. Extensive evaluations across six diverse traffic benchmarks demonstrate that mmTraffic achieves high-fidelity, auditable report generation, while maintaining exceptional classification accuracy.

# II. RELATED WORK

A. Self-supervised Methods for Encrypted Traffic Classification

Large-scale self-supervised representation learning for network traffic is one of the most significant breakthroughs in cybersecurity in recent years. Early efforts primarily adapted paradigms from natural language processing and computer vision. For instance, ET-BERT [19] pioneered the application of transformer architectures to traffic sequences via binary segmentation and masked burst flow modeling. Conversely, YaTC structured raw traffic as a multi-level flow representation (MFR) matrix, employing a dual-attention masked autoencoder to explicitly capture hierarchical packet interactions. To address computational bottlenecks and structural limitations, recent research has shifted towards efficiency and behavioral semantics. NetMamba [34] innovatively introduced state-space model (SSM) [13] via a stride-based representation, achieving faster inference suitable for high-speed networks. Meanwhile, FlowletFormer [22] moved beyond fixed-length truncation by encoding explicit multi-layer protocol semantics based on coherent behavioral interaction units. Beyond masked modeling paradigms, contrastive learning has also been explored as a self-supervised pre-training strategy for encrypted traffic analysis. For instance, SmartDetector [32] proposes a Semantic Attribute Matrix (SAM) representation and designs a traffic data augmentation method to improve robustness against obfuscation strategies such as dummy packet injection, pretraining the detection model via contrastive learning to learn deep representations from unlabeled traffic data.

Despite the diverse architectures and continuous breakthroughs [10] in accuracy, these models share a fundamental limitation: they are entirely constrained by the nature of unimodal black-box classifiers, as shown in Tables I. While they excel at the classification task, they can only map numerical sequences to discrete labels, but fail to reasoning and generate interpretable reports with chains of evidence.

TABLE I COMPARISONS OF DIFFERENT PARADIGMS FOR NETWORK TRAFFIC ANALYSIS. MBM, SBP, MAE, MFM, AND FPT REPRESENT MASKED BYTE MODEL, SEGMENT BURST PREDICTION, MASKED AUTOENCODER, MASKED FLOW MODEL, AND FLOW PREDICTION TASK, RESPECTIVELY. 

<table><tr><td>Model</td><td>Traffic Representation</td><td>Core Structure</td><td>Pre-training</td><td>Limitations</td></tr><tr><td>ET-BERT [19]</td><td>4-hex Bigram / Burst Segmentation</td><td>Transformer Encoder</td><td>MBM / SBP</td><td>Ignores protocol hierarchy; uses natural language subword tokenization</td></tr><tr><td>YaTC [38]</td><td>Multi-level Flow Representation (MFR) Matrix</td><td>Dual-Attention Transformer</td><td>MAE (Matrix Masking)</td><td>Fixed matrix dimensions; truncates long-range session features</td></tr><tr><td>NetMamba [34]</td><td>Stride-based Byte Sequence</td><td>Unidirectional Mamba (SSM)</td><td>Masked Stride Reconstruction</td><td>Purely numerical mapping; lacks interpretability</td></tr><tr><td>FlowletFormer [22]</td><td>Flowlet Behavioral Unit / Field Tokenization</td><td>Transformer Encoder</td><td>MFM / FPT</td><td>Black-box classifier; unable to output forensic reasoning</td></tr></table>

# B. LLMs for Network Security

Early applications of Large Language Models (LLMs) in cybersecurity were primarily limited to plain text tasks, such as threat intelligence aggregation [2], log parsing, and vulnerability description summarization. However, recent study begun to explore domain-specific LLMs capable of directly interpreting underlying telemetry data. TrafficLLM [7] represents a significant attempt to bridge the modality gap. It employs a traffic-domain tokenizer to compress protocol fields by reducing token length to an approximately half. While TrafficLLM [7] has demonstrated the feasibility of feeding continuous/discrete telemetry data into an LLM, this one-tower early fusion architecture suffers from an inherent structural vulnerability. Forcing an LLM to simultaneously process discrete natural language tokens and high-entropy, non-semantic numerical traffic tokens within the same attention layers frequently induces modality interference. Consequently, in high-risk intrusion detection, this architecture may neglect the authenticity of underlying physical bytes in order to maintain the fluency of the language, inevitably generating fictitious security alert logic. In contrast, the proposed mmTraffic explicitly mitigates this limitation by reformulating the architecture as an end-to-end multimodal framework, fundamentally bridges the modality gap, prevents generative hallucinations, and forces the LLM to ground its reasoning in authentic physical bytes.

# C. Multimodal Alignment and Cross-Modal Fusion

The problem of bridging heterogeneous modalities is wellstudied in the vision-language domain. Early approaches to cross-modal alignment include graph-based relational modeling [15] and semantic-driven hashing for large-scale retrieval [4], which established the importance of preserving semantic correspondences across modalities. CLIP [27] demonstrated that contrastive alignment between image and text encoders produces powerful transferable representations. Subsequent works such as LLaVA [20] and InstructBLIP [8] extended this paradigm by using lightweight projection connectors to map frozen visual encoders into the token space of large language models, enabling instruction-following behavior over visual inputs. Flamingo [3] further showed that cross-modal fusion via gated attention layers enables few-shot generalization across diverse vision-language tasks. mmTraffic draws the following insight: rather than relying on disparate training stages with a frozen perception module, we align an active traffic encoder with a language model through a lightweight MLP connector, empowering the LLM to perform encrypted traffic interpretation with rigorous multimodal reasoning.

# D. Explainability in Traffic Analysis

Despite the strong empirical performance of deep traffic classifiers, their black-box nature has motivated a growing body of work on explainable AI (XAI) [5]. Post-hoc techniques such as SHAP [25], LIME [30], and Grad-CAM [31] provide feature-level attribution scores, but cannot produce protocollevel forensic evidence for security analysts. While attentionbased mechanisms have been extended to model inter-modal interactions [23] and structured multimodal representations [14], these approaches remain confined to feature-level enhancement without producing human-readable explanations. DIS-TILLER [1] proposed a multimodal multitask framework that jointly learns traffic representations and human-readable labels, but still lacks free-form natural language generation. mmTraffic addresses this gap by leveraging large language models to produce structured, evidence-grounded forensic reports, moving beyond importance scores toward auditable reasoning chains.

# III. BGTD BENCHMARK FOR TRAFFIC REASONING

# A. Overview

A benchmark that explicitly links raw traffic analysis data with expert-level semantic reasoning is a prerequisite for training a multimodal traffic reasoning framework, but is still unexplored. Therefore, we develop a Byte-Grounded Traffic Description (BGTD) benchmark, which, to the best of our knowledge, bridges the data scarcity and persistent data-knowledge gap in encrypted traffic interpretation for the first time. To ensure the diversity of data distribution and scenarios, the BGTD dataset integrates six authoritative public traffic repositories, covering different network behaviors, application ecosystems, and encryption protocols. Specifically, BGTD deeply integrates cross-platform mobile application traffic (i.e., CrossPlatform-Android [29] and CrossPlatformiOS [29]), cutting-edge TLS 1.3 encrypted web communication (i.e., CSTNet-TLS1.3) [19], complex encrypted VPN tunnels and anonymous routing networks (i.e., ISCXVPN2016 [11] and ISCX-Tor-2016) [17], and hybrid malware traffics containing multiple attack families (i.e., USTC-TFC-2016 [35]). The pipeline for the BGTD dataset is shown in Figure 2.

![](images/d9619d6cebecd2078d79be21b8071e619e6f3f811dad632248c90107f86d09ec.jpg)  
Fig. 2. Pipeline of developing BGTD dataset: (a) session extraction and class balancing from raw PCAP files, (b) fixed-length 10 × 160 NPY array generation via priority-based packet sampling, and (c) LLM-assisted ground-truth synthesis using Claude Opus-4.6 prompted as a senior network security expert.

# B. Session Extraction and Class Balancing

As shown in Figure 2 (a), the raw PCAP files from various datasets undergo a multi-stage preprocessing. First, each PCAP file is partitioned into the standard five-tuple format (i.e., source IP address, destination IP address, source port, destination port, protocol). To mitigate the impact of the long-tail distribution, the original dataset is filtered by category, with lower and upper sample thresholds applied. Categories below the lower threshold are removed, while categories above the upper threshold are sampled according to the threshold. Specific processing methods for each dataset are provided in Sec. V-A1. The statistics of the BGTD dataset are shown in Figure 3.

# C. Fixed-Length Truncation and NPY Array Generation

Each segmented flow from above step is treated as an independent sample. To extract informative byte-level features from the original traffic data, we implement a heuristic prioritybased sampling algorithm, aiming to transform variable-length network flows into fixed-dimensional tensor features. This algorithm does not employ simple sequential truncation or random sampling, but rather comprehensively considers the temporal structure and payload information of the flow. Its specific execution logic is as follows:

• Temporal Keyframe Preservation: The algorithm forcibly preserves the first two packets and the last two packets in the flow sequence. Preserving the header packets is to capture key metadata such as protocol handshakes and control negotiations. Preserving the tail packets helps record the state characteristics.   
• Payload Information Filtering: For packets in the middle of the stream, the algorithm sorts them in descending order based on the transport layer (L4) payload length and prioritizes packets with larger payloads to fill the preset sampling number K (K = 10 in this paper). This strategy is based on the assumption that packets with

Dataset Composition: Sample Counts and Class Distribution   
![](images/1101cebee9a1afb97d88e0e550407a6eb6970333aecc6d964479e10e9e6089d1.jpg)

<details>
<summary>bar_stacked</summary>

| Platform | Train (cls) | Test (cls) |
| :--- | :--- | :--- |
| CrossPlatform Android | 212 | 38,673 |
| CrossPlatform iOS | 196 | 36,535 |
| ISCXVPN 2016 | 7 | 42,000 |
| ISCX-Tor 2016 | 8 | 80,000 |
| CSTNet TLS 1.3 | 120 | 46,372 |
| USTC-TFC 2016 | 12 | 66,388 |
</details>

Fig. 3. Statistical overview of the BGTD dataset.

larger payloads typically carry richer application-layer protocol fingerprints.

• Dimension Alignment and Consistency Guarantee: To ensure every sample has exactly K packets, the algorithm applies two strategies depending on the flow length n. If $n \geq K$ , the first two and last two packets are retained as structural anchors, and the remaining K−4 slots are filled by selecting packets from the middle region in descending order of payload size, prioritizing informationrich packets. If the quota is still unmet, equidistant indices are computed via linspace(0, n−1, deficit) and the corresponding packets are appended. If $n < K$ , all packets are kept and the sequence is extended by cyclic repetition, i.e., position j maps to packet j mod n, until exactly K packets are obtained.

Simultaneously, to ensure the consistency of the input dimensions for subsequent processing and focus on the critical protocol negotiation phase, each packet obtained by the packet sampling algorithm is truncated or padded to a fixed length of 160 bytes. As shown in Figure 2 (b), the 160 bytes consists of a 64-byte header area (i.e., L3/L4 header used to capture protocol metadata) and a 96-byte payload area. Ultimately, each network stream is transformed into a fixed-dimensional tensor $X \in \mathbb { R } ^ { 1 0 \times 1 6 0 }$ containing a custom protocol ID byte, a 63-byte processed header, and a 96-byte payload, which is then flattened into a 1600-dimensional continuous byte matrix. Furthermore, to protect privacy and prevent the model from overfitting specific network identifiers, the system forcibly masks the source and destination IP addresses at the network layer and uses a bucketing mechanism to map transport layer ports into three categories: privileged ports, registered ports, and dynamically private ports. This de-identification strategy forces the model to focus on protocol semantics and payload sequence patterns, thereby improving the model’s generalization ability. Ultimately, for ease of development, the pre-processed traffic data is stored as NPY array.

# D. Automated Expert-Knowledge Generation Pipeline

To construct relationships between traffic data and reliable analysis reports, we resort to large-scale language models to conduct a structured process from low-level data to high-level semantics [21], as shown in Figure 2 (c).

Global and Local Feature Extraction. Firstly, to capture interpretable reasoning evidence, we deploy a Dataset Generation Pipeline Script to extract global statistical features and local byte-level attributes from traffic analysis data X:

• Global Statistical Features: This data includes the duration of traffic, average packet size, throughput (Bps), and the proportion of dominant protocols. These features are transformed into semantic descriptions by script. For example, an average packet length exceeding 800 bytes is mapped to “large-volume data transmission characteristics”.   
• Encryption and Payload Distribution Evaluation: For encrypted traffic, such as TLS 1.3 environments, the Shannon entropy of non-zero payload regions and the proportion of printable ASCII characters are calculated. Based on the statistical distribution of the entire dataset, these continuous indicators are discretized into three levels: low, mid, and high, at the 33rd and 66th percentiles. For example, “low ASCII rate” combined with “high Shannon entropy” will serve as a strong signal of encrypted or compressed data characteristics.   
• Deterministic Pattern Matching: Detect if the payload contains obvious plaintext HTTP methods (e.g., GET, POST, etc.) or TLS record layer header features (e.g., 0x14-0x17 with version number 0x03) via feature matching, providing hard logic support for classification.

Expert Knowledge Base Construction. Secondly, to address the lack of rich semantic descriptions in traditional traffic datasets, this study introduces a large language model (Claude Opus-4.6) to help construct a structured domain expert knowledge base. For each traffic category in the dataset, according to preset Knowledge Base Prompt Template, LLM automatically generates an expert description containing three dimensions: (1) a protocol hint that concisely defines the application or protocol to which the traffic belongs; (2) behavioral characteristics describing 3 to 5 typical patterns of the traffic at the network level; (3) a security context that provides supplementary explanations from a network security and traffic monitoring perspective, identifying the key distinguishable features among easily confused categories. This knowledge base provides powerful domain knowledge for subsequently constructing rich, multi-perspective training texts.

Multi-field Semantic “Label” Generation. Thirdly, upon the above features and expert knowledge base, the dataset generation pipeline conducts a structured process to generate fine-grained semantic labels (i.e., “Target” in Figure 2 (c)), comprising 5 structured fields. The class field provides the ground-truth traffic category label, directly derived from the directory structure of the original dataset after session splitting and class balancing. The traits field encodes five deterministic byte-level attributes extracted from the NPY array: a boolean indicating the presence of TLS record header patterns, a boolean indicating the presence of plaintext HTTP tokens, and three discretized bucket indicators for ASCII ratio, Shannon entropy, and zero-padding ratio, each categorized as low, mid, high based on the 33rd and 66th percentiles of the full data distribution. The evidence field contains 2 to 4 natural language statements constructed by combining the above byte-level traits and global features. Each statement describes a concrete, verifiable observation grounded in the raw byte data (e.g., “High Shannon entropy in non-zero payload regions indicates that the data is highly likely to have been encrypted or compressed”). The description field provides a 2 to 3 sentence behavioral summary that integrates byte-level observations with the expert knowledge base, depicting the protocol attribution, applicationlayer characteristics, and typical communication behavior of the traffic. The notes field supplies a single security-relevant sentence drawn from the knowledge base’s security context, highlighting potential misuse risks, recommended monitoring strategies, or distinguished indicators for anomaly detection.

Ultimately, all five fields are serialized together as a structured JSON object and stored in JSONL format, forming the complete training target for the proposed mmTrafficframework.

# IV. THE PROPOSED MMTRAFFIC

# A. Overview of the Framework

The pipeline of mmTraffic is illustrated in Figure 4. It comprises three highly-collaborative and jointly-optimized modules: Perception module, Alignment module, and Cognition module. First, the Perception module acts as the foundational feature extractor. Unlike previous paradigms that freeze the traffic encoder, our encoder actively participates in the multimodal training phase, updating its parameters to learn languagealigned representations directly from raw traffic bytes. Second, the Alignment module bridges the dedicated traffic latent space and the natural language lexical space. To force this projected space to capture highly discriminative semantics autonomously, we introduce an auxiliary classification head with a dedicated constraint loss. This ensures the continuous features possess clear, linear-separable categorical boundaries before entering the language model. Finally, the Cognition module leverages the aligned multimodal embeddings to perform autoregressive reasoning. To ensure the generated traffic analysis report remains logically rigorous, we propose a Semantic-Priority Guided Generation mechanism. This mechanism dynamically assigns higher optimization weights to the categorical tokens generated at the beginning of the sequence, compelling the large language model (LLM) to perform accurate classification before reasoning about verifiable chains of evidence. By transitioning to an end-to-end joint optimization strategy, mmTraffic empowers the LLM to intrinsically understand and classify non-semantic traffic sequences, successfully achieving accurate classification and evidence-grounded interpretation within a unified framework.

![](images/8b09f5796d7cc3b120b88dc726783b1f622c1a20ed7e8bbd7c1559e6ed9395e3.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Traffic Analysis Report and Category Information"] --> B["Analysis report"]
    B --> C["L_gen = -1/T Σ(t=1^T w_t log P_φ,ω,θ(r_t | E_in, r<t)"]
    C --> D["L_aux = -Σ(c=1^C y_c log(p_cls,c)"]
    D --> E["Auxiliary Cls Head"]
    E --> F["Prompt"]
    F --> G["Large Language Models (LLMs)"]
    G --> H["Analysis Report"]
    H --> I["Behavioral Traits"]
    I --> J["Evidence Chain"]
    J --> K["Description"]
    K --> L["Cognitive Module"]

    subgraph_A["Perception Module"]
        M["X"] --> N["T_θ"]
        N --> O["X_traffic"]
        O --> P["Projection Connector C_ω"]
        P --> Q["H_align"]
        Q --> R["Prompt"]
        R --> S["Large Language Models (LLMs)"]
    end

    subgraph_B["Alignment Module with Auxiliary Classification"]
        T["Header Payload"] --> U["Traffic Encoder"]
        V["X"] --> W["X_traffic"]
        X["W_i and b1"] --> Y["GELU"]
        Z["W2 and b2"] --> AA["GELU"]
        AB["H"] --> AC["H_align"]
    end

    subgraph_C["Alignment Module with Auxiliary Classification"]
        AD["Proposition Connector"] --> AE["C_ω"]
        AF["Projection Connector"] --> AG["C_ω"]
        AH["H_align"] --> AI["H_align"]
        AJ["Prompts"] --> AK["Large Language Models (LLMs)"]
    end

    subgraph_G["Large Language Models (LLMs)"]
        AL["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        AM["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        AN["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        AO["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        AP["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        AQ["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        AR["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        AS["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        AT["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        AU["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        AV["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        AW["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        AX["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        AY["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        AZ["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BA["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BB["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BC["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BD["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BE["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BF["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BG["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BH["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BI["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BJ["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BK["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BL["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BM["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BN["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BO["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BP["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BQ["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BR["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BS["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BT["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BU["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BV["Input: E_in + The traffic has been classified as VoIP + Prompt"]
        BW["Input: E_in + The traffic has been classified as VoIP + Prompt"]
    end

    subgraph_C["Cognitive Module"]
        BX["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BY["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        Z["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AA["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AB["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AC["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AD["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AE["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AF["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AG["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AH["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AI["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AJ["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AK["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AL["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AM["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AN["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AO["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AP["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AQ["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AR["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AS["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AT["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AU["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AV["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AW["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AX["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AY["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        AZ["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BA["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BB["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BC["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BD["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BE["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BF["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BG["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BH["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BI["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BJ["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BK["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BL["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BM["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BN["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BO["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BP["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BQ["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BR["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BS["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BT["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BU["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BV["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BW["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BXN["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BYN["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BZN["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BWN["Input: Synthesized as Plaintext Transmission (No Encryption detected)"]
        BXN --> BZN
    end

    subgraph_C["Cognitive Module"]
    CA["Cognitive Module"] --> CB["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> CC["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> DD["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> DD["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> DD["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> DD["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> DD["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> D["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> D["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> D["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> D["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> D["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] -->D["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] -->D["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] -->D["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] -->D["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] -->D["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> D["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] -->D["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] -->D["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] -->D["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] -->E["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] -->E["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] -->F["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] -->G["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] -->H["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> I["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> J["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> K["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> L["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> M["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> N["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> O["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> P["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> Q["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> R["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> S["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> T["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> U["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> V["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> W["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> X["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> Y["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> Z["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> AA["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> AB["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> AC["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> AD["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> AE["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> AF["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CB["Cognitive Module"] --> AGC["Cognitive Module"]
    subgraph_D["Cognitive Module"]
    CBC3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C3C
```
</details>

Fig. 4. Overview of the mmTraffic framework. (a) The frozen traffic encoder $T _ { \theta }$ extracts high-dimensional features from raw traffic data. (b) The linear connector $C _ { \omega }$ projects traffic features into the LLM token space, with the CGHF mechanism injecting a class-aware anchor token into the input sequence. (c) The LLM $G _ { \phi }$ autoregressively generates a structured forensic report containing behavioral traits, evidence chain, and diagnostic description.

# B. Perception Module

This module receives the raw byte sequence X preprocessed according to the BGTD protocol and performs a highdimensional non-linear mapping via the traffic encoder $T _ { \theta }$ .

High-dimensional Continuous Feature Embedding: The encoder $T _ { \theta }$ processes X to automatically extract complex spatial dependencies and structural patterns of protocol fields, generating a dense feature tensor:

$$
\mathbf {T} _ {\text { traffic }} = T _ {\theta} (\mathbf {X}) \tag {1}
$$

where $T _ { t r a f f i c } \in \mathbb { R } ^ { L \times d _ { t r a f f i c } }$ , L denotes the sequence length, and $d _ { t r a f f i c }$ represents the feature dimension of the traffic encoder.

End-to-End Optimization: In contrast to previous multistage paradigms where the perception module is trained independently and then strictly frozen to prevent catastrophic forgetting, our framework treats $T _ { \theta }$ as an active component within a unified multimodal architecture. The parameters of the traffic encoder are unfrozen and updated during the joint training phase. By receiving gradient feedback backpropagated from both the downstream auxiliary classification head $A _ { \kappa }$ and the cognitive language model, the encoder is explicitly guided to map non-semantic raw bytes into a representation space that is naturally aligned with language-based reasoning.

# C. Alignment Module with Auxiliary Classification

To achieve implicit alignment between the dedicated traffic latent space and the natural language lexical space, mmTraffic deploys a lightweight projection connector $\mathrm { C } _ { \omega }$ . For computational efficiency, we employ a two-layer Multi-Layer Perceptron (MLP) equipped with a Gaussian Error Linear Unit (GELU) activation. Given the continuous traffic embedding $\mathbf { T } _ { \mathrm { t r a f f i c } }$ from the Perception module, the non-linear transformation of $\mathrm { C } _ { \omega }$ is formally defined as:

$$
\mathbf {H} _ {\text { align }} = \mathrm{C} _ {\omega} (\mathbf {T} _ {\text { traffic }}) = \mathbf {W} _ {2} \sigma (\mathbf {W} _ {1} \mathbf {T} _ {\text { traffic }} + \mathbf {b} _ {1}) + \mathbf {b} _ {2} \tag {2}
$$

where $\sigma ( \cdot )$ denotes the GELU activation function, and $\omega =$ $\{ \mathbf { W } _ { 1 } , \mathbf { b } _ { 1 } , \mathbf { W } _ { 2 } , \mathbf { b } _ { 2 } \}$ represents the learnable weight matrices and bias vectors of the connector. The resulting $\mathbf { H } _ { \mathrm { a l i g n } }$ bridges the dimensional gap, projecting the traffic features into the LLM’s lexical space.

Auxiliary Classification. During alignment, simply mapping the dimensions is insufficient to guarantee that the projected tokens carry explicit categorical semantics. To force the continuous feature space to capture highly discriminative information, we introduce an Auxiliary Classification Head, denoted as $\mathrm { A } _ { \kappa }$ atop the projection connector. Specifically, we first apply Global Average Pooling (GAP) across the sequence dimension L of the aligned features $\mathbf { H } _ { \mathrm { a l i g n } }$ to obtain a condensed sequence-level semantic representation $\mathbf { H } _ { \mathrm { p o o l } } \in \mathbb { R } ^ { d _ { \mathrm { h } } }$ :

$$
\mathbf {H} _ {\text { pool }} = \mathrm{GAP} (\mathbf {H} _ {\text { align }}) = \frac {1}{L} \sum_ {i = 1} ^ {L} \mathbf {H} _ {\text { align }} ^ {(i)} \tag {3}
$$

where $\mathbf { H } _ { \mathrm { a l i g n } } ^ { ( i ) }$ represents the i-th token embedding in the sequence, and $d _ { \mathrm { h } }$ is the hidden dimension of the LLM. This pooled representation is then processed by the auxiliary classification head $\mathrm { A } _ { \kappa }$ to predict the discrete probability distribution $\mathbf { p } _ { \mathrm { c l s } } \in \mathbb { R } ^ { C }$ over C predefined traffic classes:

$$
\mathbf {p} _ {\mathrm{cls}} = \mathrm{A} _ {\kappa} (\mathbf {H} _ {\text { pool }}) = \operatorname{Softmax} \left(\mathbf {W} _ {\mathrm{cls}} \mathbf {H} _ {\text { pool }} + \mathbf {b} _ {\mathrm{cls}}\right) \tag {4}
$$

where $\boldsymbol { \kappa } = \{ \mathbf { W } _ { \mathrm { c l s } } , \mathbf { b } _ { \mathrm { c l s } } \}$ are the learnable parameters of $\mathrm { A } _ { \kappa } ,$ mapping the hidden dimension $d _ { \mathrm { h } }$ to the category space $C .$

Then we compute the auxiliary classification loss using the standard cross-entropy objective:

$$
\mathcal {L} _ {\text { aux }} = - \sum_ {c = 1} ^ {C} y _ {c} \log (\mathbf {p} _ {\mathrm{cls}, c}) \tag {5}
$$

where $y _ { c } \in \{ 0 , 1 \}$ is the binary indicator of the ground-truth class label, and $\mathbf { p } _ { \mathrm { c l s } , c }$ is the predicted probability for class c. During the joint training phase, $\mathcal { L } _ { \mathrm { a u x } }$ actively propagates gradient back through $\mathrm { C } _ { \omega }$ and ${ \mathrm { T } } _ { \theta } ,$ strictly anchoring the representation space to the identity of a traffic sample.

# D. Cognition Module

With the auxiliary classification constraint enforcing category-aware features in the alignment stage, the Cognition module calls the large language model $\mathrm { G } _ { \phi }$ to perform autoregressive inference directly from the aligned traffic features, without relying on hard-coded discrete labels. The full input sequence $\mathbf { E } _ { \mathrm { i n } }$ of $\mathrm { G } _ { \phi }$ is constructed by concatenating the aligned traffic tokens $\mathbf { H } _ { \mathrm { a l i g n } }$ and the task instruction prompt $\mathbf { P } \colon$

$$
\mathbf {E} _ {\text {in}} = \left[ \begin{array}{l l} \mathbf {H} _ {\text {align}}; & \mathbf {P} \end{array} \right] \tag {6}
$$

The LLM then autoregressively generates the diagnostic report $\mathbf { R } _ { \mathrm { p r e d } }$ conditioned on this sequence:

$$
\mathbf {R} _ {\text { pred }} = \mathrm{G} _ {\phi} (\mathbf {E} _ {\text { in }}) \tag {7}
$$

In the multi-modal report generation task, the correct identification of the traffic category acts as the foundational premise for all subsequent behavioral descriptions and evidence chains. Standard negative log-likelihood (NLL) loss treats all generated tokens equally, which may lead to the LLM generating fluent but factually incorrect hallucinated reports if the core category is misidentified. To address this, we propose a Semantic-Priority Guided Generation Loss. We assign an amplification weight to the prefix tokens of the target sequence (which correspond to the primary categorical decision in the JSON structure) to explicitly force the LLM to prioritize classification accuracy during the generative process. The weighted generation loss over the expert evidence chains $\mathbf { R } = \{ r _ { 1 } , r _ { 2 } , \ldots , r _ { T } \}$ is formulated as:

$$
\mathcal {L} _ {\text { gen }} = - \frac {1}{T} \sum_ {t = 1} ^ {T} w _ {t} \log P _ {\phi , \omega , \theta} (r _ {t} \mid \mathbf {E} _ {\text { in }}, r _ {<   t}) \tag {8}
$$

where $r _ { < t } = \{ r _ { 1 } , \ldots , r _ { t - 1 } \}$ denotes all ground-truth tokens preceding position t, and wt is the dynamic positional weight defined as:

$$
w _ {t} = \left\{ \begin{array}{l l} 1 + \gamma , & \text { if } t \leq M \\ 1, & \text { otherwise } \end{array} \right. \tag {9}
$$

where M defines the boundary of the critical categorical tokens at the beginning of the sequence, and γ is the boost weight factor applied to strictly penalize misclassifications in the generated text.

Unlike previous paradigms that freeze the traffic encoder, our mmTraffic framework enables end-to-end multimodal alignment. The overall objective function integrates both the token-level generative comprehension and the sequence-level auxiliary classification constraint:

$$
\mathcal {L} _ {\text { total }} = \mathcal {L} _ {\text { gen }} + \lambda \mathcal {L} _ {\text { aux }} \tag {10}
$$

where λ is a hyperparameter balancing the auxiliary classification task. During training, the parameters of the traffic encoder $( \operatorname { T } _ { \theta } ) .$ , projection connector $( \mathrm { C } _ { \omega } ) .$ , auxiliary classification head $( \mathrm { A } _ { \kappa } )$ , and language model $( \mathrm { G } _ { \phi } )$ are jointly optimized.

Algorithm 1 The Training Pipeline of mmTraffic   
Require: Traffic tensor $X \in R^{10 \times 160}$ , ground-truth label y, chain of evidence annotation $R = \{r_1, \ldots, r_T\}$ of BGTD, unfrozen encoder $T_\theta$ , connector $C_\omega$ , auxiliary classification head $A_\kappa$ , LLM $G_\phi$ , task prompt P, auxiliary loss weight $\lambda$ , semantic boost weight $\gamma$ , and threshold M.

Ensure: Predicted traffic class $\hat{y}$ and forensic report $R_{pred}$ .

// Step 1: Perception Module

1: $T_{traffic} \leftarrow T_\theta(X)$ ▷ Extract embeddings via unfrozen encoder

// Step 2: Alignment Module & Auxiliary Constraint

2: $H_{align} \leftarrow C_\omega(T_{traffic})$ ▷ Project to LLM lexical space

3: $H_{pool} \leftarrow GAP(H_{align})$ ▷ Sequence-level global average pooling

4: $p_{cls} \leftarrow A_\kappa(H_{pool})$ ▷ Predict auxiliary class distribution

5: $\hat{y} \leftarrow \arg\max(p_{cls})$ ▷ Traffic classification prediction

// Step 3: Multimodal Construction

6: $E_{in} \leftarrow [H_{align}; P]$ ▷ Directly concatenate features and prompt

// Step 4: Cognition Module & Joint Optimization

7: if training then

8: $L_{aux} \leftarrow -\log(p_{cls,y})$ ▷ Compute auxiliary cross-entropy loss

9: Compute dynamic weights $w_t: 1 + \gamma$ if $t \leq M$ , else 1

10: $L_{gen} \leftarrow -\frac{1}{T} \sum_{t=1}^T w_t \log P_{\phi,\omega,\theta}(r_t | E_{in}, r_{<t})$ ▷ Semantic-priority guided loss

11: $L_{total} \leftarrow L_{gen} + \lambda L_{aux}$ ▷ End-to-end joint objective

12: Update $\{\theta, \omega, \kappa, \phi\}$ via AdamW ▷ Jointly optimize all modules

13: else

14: $R_{pred} \leftarrow G_\phi(E_{in})$ ▷ Autoregressive report generation

15: Parse $R_{pred}$ into JSON format: {class, traits, evidence, description, notes}

16: end if

17: return $\hat{y}$ , $R_{pred}$

In summary, the proposed mmTraffic constructs a closed-loop analysis system from the underlying bit stream to the high-level forensic report through a perception module (feature extraction), an alignment module (cross-space mapping with auxiliary constraint), and a cognition module (logical reconstruction with semantic-priority guidance). This joint optimization empowers the LLM to intrinsically understand non-semantic traffic sequences, ensuring the reliability of the analysis report. To clearly demonstrate the logical pipeline of the above procedure, we summarize mmTraffic in Algorithm 1.

# V. EXPERIMENTS

# A. Experimental Settings

1) Data Preparation: We evaluate the proposed framework on six publicly available network traffic datasets, covering a wide range of traffic types, application ecosystems, and encryption protocols. To reduce the impact of class imbalance, we apply a category filtering strategy to each dataset: classes with fewer than $N _ { \mathrm { m i n } }$ samples are removed, and classes exceeding $N _ { \mathrm { m a x } }$ samples are randomly downsampled to $N _ { \mathrm { m a x } } .$

TABLE II STATISTICS OF THE SIX BENCHMARK DATASETS AFTER PREPROCESSING. 

<table><tr><td>Dataset</td><td>Classes</td><td> $N_{\text{min}}$ </td><td> $N_{\text{max}}$ </td><td>Train</td><td>Test</td></tr><tr><td>CrossPlatform-Android</td><td>212</td><td>50</td><td>2,000</td><td>31,029</td><td>7,644</td></tr><tr><td>CrossPlatform-iOS</td><td>196</td><td>50</td><td>3,000</td><td>29,302</td><td>7,233</td></tr><tr><td>ISCXVPN2016</td><td>7</td><td>200</td><td>6,000</td><td>33,600</td><td>8,400</td></tr><tr><td>ISCX-Tor-2016</td><td>8</td><td>3,000</td><td>10,000</td><td>64,000</td><td>16,000</td></tr><tr><td>CSTNet-TLS1.3</td><td>120</td><td>0</td><td>6,000</td><td>37,148</td><td>9,224</td></tr><tr><td>USTC-TFC-2016</td><td>12</td><td>3,000</td><td>6,000</td><td>53,112</td><td>13,276</td></tr></table>

All datasets are split into training and test sets at an 8:2 ratio. Statistics of the six datasets after the above preprocessing are shown in Tables II. Details of each dataset are as follows:

• CrossPlatform-Android and CrossPlatform-iOS [29]: These two datasets contain mobile application traffic collected from Android and iOS devices across multiple countries and network environments, covering 212 and 196 application categories respectively. We set $N _ { \mathrm { m i n } } = 5 0$ , $N _ { \mathrm { m a x } } = 2 { , } 0 0 0$ for Android and $N _ { \mathrm { m a x } } = 3 { , } 0 0 0$ for iOS, resulting in 38,673 and 36,535 samples after filtering.   
• ISCXVPN2016 [11]: This dataset contains application traffic tunneled through VPN connections, covering 7 categories: Browsing, Chat, Email, FTP, P2P, Streaming, and VoIP. VPN encapsulation adds an additional encryption layer that obscures applicationlayer signatures. We set $N _ { \mathrm { m i n } } = 2 0 0$ and $N _ { \mathrm { m a x } } = 6 { , } 0 0 0$ , yielding 42,000 samples.   
• ISCX-Tor-2016 [17]: This dataset contains traffic routed through the Tor anonymous network, covering 8 traffic categories. Tor’s multi-hop encryption substantially reduces the discriminability of byte-level features, making it one of the most challenging benchmarks in encrypted traffic analysis. We set $N _ { \mathrm { m i n } } ~ = ~ 3 { , } 0 0 0$ and $N _ { \mathrm { m a x } } = 1 0 \small { , } 0 0 0$ , resulting in 80,000 samples.   
• CSTNet-TLS1.3 [19]: This dataset contains web traffic encrypted exclusively with TLS 1.3, covering 120 website categories. Since TLS 1.3 removes observable handshake metadata, certificate-based identification is not applicable. The class distribution is relatively balanced, so $N _ { \mathrm { m i n } } = 0$ and $N _ { \mathrm { m a x } } = 6 , 0 0 0$ , yielding 46,372 samples.   
• USTC-TFC-2016 [35]: This dataset contains both benign application traffic and traffic from 12 malware families, making it the only dataset in our benchmark that includes adversarial network behavior. We set $N _ { \mathrm { m i n } } = 3 { , } 0 0 0$ and $N _ { \mathrm { m a x } } = 6 , 0 0 0$ , resulting in 66,388 samples.

2) Implementation Details: The traffic encoder $\mathrm { T } _ { \theta }$ is instantiated with NetMamba [34]. Unlike previous decoupled methods, $\mathrm { T } _ { \theta }$ is completely unfrozen and fully fine-tuned to actively capture language-aligned semantic representations. The alignment connector $\mathrm { C } _ { \omega }$ is implemented as a two-layer MLP with GELU activation (mlp2x\_gelu) and is also fully fine-tuned, alongside the newly introduced auxiliary classification head $\mathrm { A } _ { \kappa } .$ The cognitive module $\mathrm { G } _ { \phi }$ is instantiated with Qwen3-1.7B [36] and adapted via Low-Rank Adaptation (LoRA) [16]. LoRA is applied to all attention and feed-forward projection modules (specifically <q\_proj>, <k\_proj>, $< \mathrm { v \_ p r o j > } , < \mathrm { \circ \_ p r o j > }$ , <gate\_proj>, <up\_proj>, and <down\_ $\mathrm { \ p r o { j > } } )$ , with an increased rank $r = 3 2$ , scaling factor $\alpha = 6 4 .$ , and a dropout rate of 0.1. Thus, the parameters of $\mathrm { T } _ { \theta } , \mathrm { C } _ { \omega } , \mathrm { A } _ { \kappa } .$ , and the LoRA modules of $\mathrm { G } _ { \phi }$ are jointly updated during the end-to-end training.

For the multi-task optimization objectives, the balancing weight for the auxiliary classification loss is set to $\lambda = 0 . 3$ For the semantic-priority guided generation loss, we set the categorical boundary threshold to $M = 1 5$ and the boost weight factor to $\gamma = 5 . 0 ,$ , firmly anchoring the text generation to the physical traffic identity.

All models are trained for 10 epochs using the AdamW [24] optimizer with a peak learning rate of $\eta = 5 \times 1 0 ^ { - 5 }$ , a weight decay of 0.01, a linear warmup [12] over the first 10% of training steps, and a gradient clipping threshold of 1.0. We utilize BFloat16 [26] mixed-precision and distributed training via DeepSpeed ZeRO-2 [28]. The per-device batch size is set to 3 with a gradient accumulation of 8 steps, yielding a global batch size of $3 \times 8 \times 5 = 1 2 0$ across 5 NVIDIA A800 GPUs.

3) Evaluation Metrics: We evaluate mmTraffic from two complementary perspectives: traffic classification and forensic report generation. The evaluation metrics include:

• Classification Metrics. We report Accuracy to assess the traffic identification performance of the perception module, measured as the proportion of correctly classified samples over the full test set. We additionally report JSON Validity Rate (JSON Valid%), the proportion of model outputs that can be successfully parsed as a valid JSON object containing all required fields, which reflects whether the model has learned the structured output format.   
• Text Generation Metrics. To assess the quality of the generated evidence and description fields, we adopt two complementary metrics: ROUGE-L [18] measures the $F _ { 1 }$ score of the longest common subsequence (LCS) between the generated and reference texts, capturing lexical overlap and word-order consistency. BERTScore [37] computes token-level semantic similarity between generated and reference texts using contextual embeddings from roberta-large (num\_layers=17), loaded from a local checkpoint to ensure reproducibility. We report the macro-averaged BERTScore $\mathrm { F _ { 1 } }$ , computed as the arithmetic mean of per-sample $F _ { 1 }$ scores (harmonic mean of token-level precision and recall) over the full test set. Compared to ROUGE-L, BERTScore is more robust to lexical paraphrasing and stylistic variation between the ground-truth anchor (Claude Opus) and the prediction model (Qwen3-1.7B) [36], and thus a reliable indicator of semantic fidelity when surface-level wording differs.   
• Structural Consistency Metrics. Beyond lexical and semantic similarity, we evaluate the internal quality of generated reports using three reference-free metrics, which are visualized in the radar charts, computed solely over the model’s generated output, requiring no ground-truth text for evaluation. Let N denote the number of samples with valid JSON predictions, and let $e _ { i } , \ d _ { i }$ denote the predicted evidence and description fields of the i-th report, with $c _ { i } ~ = ~ [ e _ { i } ; d _ { i } ]$ denoting their concatenation. Evidence-Trait Consistency (ETC) measures whether the generated evidence text is semantically coherent with

TABLE III RESULTS ON ISCX-TOR-2016, ISCXVPN2016, AND CSTNET-TLS1.3. NETMAMBA IS THE UNIMODAL CLASSIFIER (“–” MEANS NO GENERATION); ZERO-SHOT LLM FEEDS FEATURES DIRECTLY TO LLM WITHOUT TUNING; VANILLA FREEZES THE ENCODER WITHOUT AUXILIARY CONSTRAINTS. BOLD INDICATES THE BEST PER COLUMN WITHIN EACH DATASET GROUP. 

<table><tr><td rowspan="2">Dataset</td><td rowspan="2">Method</td><td>Classification</td><td>Generation</td><td colspan="2">Evidence</td><td colspan="2">Description</td></tr><tr><td>Acc / JClsAcc%</td><td>JSON Valid%</td><td>ROUGE-L</td><td>BERTScore</td><td>ROUGE-L</td><td>BERTScore</td></tr><tr><td rowspan="4">ISCX-Tor-2016</td><td>NetMamba</td><td>0.9961</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr><tr><td>Zero-shot LLM</td><td>0.0003</td><td>100.00%</td><td>0.1247</td><td>0.8322</td><td>0.1164</td><td>0.8469</td></tr><tr><td>Vanilla</td><td>0.7092</td><td>100.00%</td><td>0.6002</td><td>0.9217</td><td>0.5831</td><td>0.9266</td></tr><tr><td>mmTraffic (Ours)</td><td>0.9331</td><td>100.00%</td><td>0.8192</td><td>0.9641</td><td>0.7751</td><td>0.9481</td></tr><tr><td rowspan="4">ISCXVPN2016</td><td>NetMamba</td><td>0.9917</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr><tr><td>Zero-shot LLM</td><td>0.0004</td><td>100.00%</td><td>0.1121</td><td>0.8290</td><td>0.1252</td><td>0.8545</td></tr><tr><td>Vanilla</td><td>0.2987</td><td>100.00%</td><td>0.3597</td><td>0.8881</td><td>0.2020</td><td>0.8679</td></tr><tr><td>mmTraffic (Ours)</td><td>0.9902</td><td>100.00%</td><td>0.8436</td><td>0.9686</td><td>0.6975</td><td>0.9419</td></tr><tr><td rowspan="4">CSTNet-TLS1.3</td><td>NetMamba</td><td>0.8474</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr><tr><td>Zero-shot LLM</td><td>0.0000</td><td>100.00%</td><td>0.2675</td><td>0.8780</td><td>0.1399</td><td>0.8492</td></tr><tr><td>Vanilla</td><td>0.0148</td><td>100.00%</td><td>0.5224</td><td>0.9242</td><td>0.4346</td><td>0.9041</td></tr><tr><td>mmTraffic (Ours)</td><td>0.6448</td><td>100.00%</td><td>0.7188</td><td>0.9538</td><td>0.8007</td><td>0.9710</td></tr></table>

the predicted byte-level trait values, verifying that the model’s reasoning is grounded in the actual traffic features rather than generating plausible-sounding but ungrounded observations. It is computed as:

$$
\mathrm{ETC} = \frac {1}{N} \sum_ {i = 1} ^ {N} \mathbf {1} [ \mathrm{KW} (\mathcal {T} _ {i}) \cap e _ {i} \neq \emptyset ] \tag {11}
$$

where 1[·] is the indicator function that equals 1 if the condition holds and 0 otherwise, KW(Ti) denotes the union of keyword sets of all predicted traits, and $e _ { i }$ denotes the tokens of the predicted evidence text.

Quantitative Claim Rate (QCR) measures the proportion of reports containing at least one concrete numerical observation, such as byte counts, entropy values, or explicit ordinal descriptors. A high QCR indicates that the model produces specific, verifiable reports rather than vague qualitative descriptions. It is computed as:

$$
\mathrm{QCR} = \frac {1}{N} \sum_ {i = 1} ^ {N} \mathbf {1} [ \text { HasQuant } (c _ {i}) ] \tag {12}
$$

where HasQuant(·) is true if $c _ { i }$ contains any percentage, byte quantity, multi-digit number, or ordinal descriptor (high/mid/low), or the keyword ratio.

Protocol Mention Rate (PMR) measures the proportion of reports that explicitly reference at least one network protocol by name or identifier (e.g., TCP, TLS, HTTP, QUIC). Protocol attribution is a fundamental requirement for reports, and a high PMR confirms the model reliably grounds its analysis in appropriate protocol context.

$$
\mathrm{PMR} = \frac {1}{N} \sum_ {i = 1} ^ {N} \mathbf {1} [ \mathcal {P} \cap c _ {i} \neq \emptyset ] \tag {13}
$$

where $\mathcal { P }$ is a predefined set of protocol keywords (e.g., TCP, TLS, HTTP).

We note that reference-based metrics such as ROUGE-L and BERTScore exhibit insensitivity to classification

correctness in fine-grained settings, as the ground-truth descriptions across categories share substantial protocollevel vocabulary. This motivates the introduction of reference-free structural consistency metrics.

# B. Main Results

Tables III and IV present the comparison results with baselines. We report the linear head Accuracy (Acc) for Net-Mamba, while the JSON Classification Accuracy (JClsAcc%) extracted directly from the generated natural language reports for generative models (Zero-shot LLM, Vanilla, and ours).

Evaluation of Classification Performance. NetMamba sets the upper-bound baseline for specialized unimodal classification. As observed, the Zero-shot LLM and Vanilla paradigms suffer a catastrophic drop in classification capability, failing almost entirely on datasets like CSTNet-TLS1.3 (0.0148) and CrossPlatform-iOS (0.0058). This collapse demonstrates that without joint optimization, the semantic gap between physical bytes and the lexical space is insurmountable. In contrast, our proposed mmTraffic successfully bridges this gap. By unfreezing the encoder and applying the auxiliary classification head, mmTraffic recovers robust JSON classification performance (e.g., reaching 0.9902 on ISCXVPN2016 and 0.8865 on CrossPlatform-iOS). While there is a slight inherent alignment tax compared to the pure linear classifier (e.g., 0.9887 for NetMamba vs. 0.8624 for mmTraffic on USTC-TFC-2016) due to the complexity of autoregressive text generation, it remains highly competitive and overwhelmingly surpasses standard multimodal baselines (i.e., zero-shot LLM and Vanilla).

Evaluation of Generation Quality. Generating humanreadable and evidence-grounded reports is the core objective. Unimodal classifiers like NetMamba are fundamentally incapable of generating text. The Vanilla manages to produce fluent text but generates severe hallucinations due to its inability to accurately identify the underlying traffic. Conversely, mmTraffic achieves a JSON validity rate of 100% across all datasets, confirming that the LLM has fully mastered the structured output format. On evidence and description generation, mmTraffic demonstrates overwhelming superiority. For example, it achieves an Evidence ROUGE-L of 0.8436 on ISCXVPN2016 and a Description BERTScore of 0.9710 on CSTNet-TLS1.3. Across all six datasets, the BERTScore consistently remains above 0.90, proving that the generated evidence and behavioral descriptions maintain rigorous semantic alignment with the ground-truth expert annotations.

TABLE IV RESULTS ON CROSSPLATFORM-IOS, CROSSPLATFORM-ANDROID, AND USTC-TFC-2016. NETMAMBA IS THE UNIMODAL CLASSIFIER $( ^ { 6 6 } - ^ { 3 3 }$ MEANS NO GENERATION); ZERO-SHOT LLM FEEDS FEATURES DIRECTLY TO LLM WITHOUT TUNING; VANILLA FREEZES THE ENCODER WITHOUT AUXILIARY CONSTRAINTS. BOLD INDICATES THE BEST PER COLUMN WITHIN EACH DATASET GROUP. 

<table><tr><td rowspan="2">Dataset</td><td rowspan="2">Method</td><td>Classification</td><td>Generation</td><td colspan="2">Evidence</td><td colspan="2">Description</td></tr><tr><td>Acc / JClsAcc%</td><td>JSON Valid%</td><td>ROUGE-L</td><td>BERTScore</td><td>ROUGE-L</td><td>BERTScore</td></tr><tr><td rowspan="4">CrossPlatform-iOS</td><td>NetMamba</td><td>0.9060</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr><tr><td>Zero-shot LLM</td><td>0.0000</td><td>100.00%</td><td>0.1962</td><td>0.8509</td><td>0.1268</td><td>0.8503</td></tr><tr><td>Vanilla</td><td>0.0058</td><td>100.00%</td><td>0.2218</td><td>0.8591</td><td>0.1255</td><td>0.8535</td></tr><tr><td>mmTraffic (Ours)</td><td>0.8865</td><td>100.00%</td><td>0.6880</td><td>0.9387</td><td>0.5972</td><td>0.9283</td></tr><tr><td rowspan="4">CrossPlatform-Android</td><td>NetMamba</td><td>0.9104</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr><tr><td>Zero-shot LLM</td><td>0.0000</td><td>100.00%</td><td>0.0000</td><td>0.0000</td><td>0.0000</td><td>0.8405</td></tr><tr><td>Vanilla</td><td>0.0027</td><td>100.00%</td><td>0.2107</td><td>0.8661</td><td>0.1283</td><td>0.8542</td></tr><tr><td>mmTraffic (Ours)</td><td>0.8654</td><td>100.00%</td><td>0.5482</td><td>0.9060</td><td>0.5605</td><td>0.9299</td></tr><tr><td rowspan="4">USTC-TFC-2016</td><td>NetMamba</td><td>0.9887</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr><tr><td>Zero-shot LLM</td><td>0.0000</td><td>100.00%</td><td>0.1386</td><td>0.8377</td><td>0.1365</td><td>0.8536</td></tr><tr><td>Vanilla</td><td>0.7002</td><td>100.00%</td><td>0.6383</td><td>0.9272</td><td>0.5447</td><td>0.9163</td></tr><tr><td>mmTraffic (Ours)</td><td>0.8624</td><td>100.00%</td><td>0.8853</td><td>0.9769</td><td>0.7714</td><td>0.9527</td></tr></table>

Evaluation of Structural Consistency. A critical observation in multimodal traffic analysis is the ”fluency trap”: models like Vanilla MLM might achieve moderate text generation metrics (e.g., Ev-BS and Desc-BS) by memorizing common vocabulary, even when their classification accuracy (Acc) completely collapses—as starkly visible in the ISCXVPN2016 and CP-Android radar charts. This reveals a fundamental limitation of reference-based metrics in forensics—lexical overlap does not guarantee factual correctness. The radar charts in Figure 5 provide a comprehensive picture of logical rigorousness across six key dimensions. While Vanilla MLM exhibits severely distorted performance profiles , our proposed mmTraffic maintains a robust, near-symmetrical shape that pushes towards the outer boundaries (1.0) across all evaluated datasets. Driven by our semantic-priority guided generation mechanism, mmTraffic ensures that its high structural consistency (ETC, QCR, PMR) is strictly anchored in correct traffic identification, effectively eliminating the multimodal hallucinations prevalent in unconstrained architectures.

# C. Ablation Study

To isolate the contribution of each proposed component in mmTraffic, we conduct an ablation study across two distinct domains: ISCX-Tor-2016 and ISCXVPN2016. As illustrated in Figure 6, we systematically evaluate four configurations: (1) V1 (Vanilla MLLM): freezing the NetMamba encoder and relying solely on the standard Negative Log-Likelihood (NLL) loss; (2) V2 (+ Unfrozen): unfreezing the traffic encoder for end-to-end joint optimization; (3) V3 (+ Auxiliary Head): introducing the auxiliary classification head $( \mathcal { L } _ { \mathrm { a u x } } )$ to the latent space; and

Radar Chart Analysis on Key Metrics   
![](images/de20e0e5e46f39b9e81d816abe9b9fa9b795f28312dc740d997da85cf060eac7.jpg)

Fig. 5. Analysis on Structural Consistency Metrics. The semantic-priority constraints in mmTraffic ensure high logical rigor.   
![](images/acb76256ba4b410a59e15643c9dba3bb500a1a0df1a93d0a9cb7d6739281cc90.jpg)  
Fig. 6. Ablation analysis on ISCX-Tor-2016 and ISCXVPN2016, with respect to the classification and generation metrics for four variants from V1 to V4.

(4) V4 (mmTraffic Full): incorporating the semantic-priority guided generation mechanism $( \mathcal { L } _ { \mathrm { g e n } } )$ .

Breaking the Modality Barrier via Joint Optimization. The initial transition from V1 to V2 in Figure 6 reveals the fundamental bottleneck of cross-modal traffic analysis. In the Vanilla MLLM (V1) setting, the framework suffers a catastrophic failure on ISCXVPN2016 (accuracy at 0.2987) and struggles at 0.7092 on ISCX-Tor-2016. Because raw cryptographic traffic sequences lack the natural lexical alignments found in visual-text data, a frozen encoder fundamentally fails to project these non-semantic bytes into the LLM’s sophisticated cognitive space. Unfreezing the encoder (+ Unfrozen) opens the gradient bottleneck, allowing the perceptual backbone to dynamically adapt its feature extraction guided by the LLM’s generation objective. This mechanistic bridge yields a massive concurrent leap in both text fidelity (e.g., Average ROUGE-L on Tor rises from 0.59 to 0.78) and classification accuracy (0.8674 on Tor and 0.9751 on VPN).

TABLE V ISCX-TOR-2016 FOR SAMPLE #6227: MMTRAFFIC CORRECTLY IDENTIFIES THE CLASS. EVIDENCE AND DESCRIPTION FIELDS ARE ABBREVIATED. GREEN MEANS CORRECTLY INTERPRETED KEY CONTENT. 

<table><tr><td>Field</td><td>mmTraffic (Ours)</td><td>Ground Truth</td></tr><tr><td>Class</td><td>CHAT √</td><td>CHAT</td></tr><tr><td>Traits</td><td>has_tls: truehas_http: falseascii: lowentropy: midzero_pad: mid</td><td>has_tls: truehas_http: falseascii: midentropy: midzero_pad: mid</td></tr><tr><td>Evidence</td><td>(1) TLS record header detected, indicating an encrypted TLS session.(2) TCP dominant (100%), consistent with Tor CHAT profile.(3) Unlike Tor VOIP (codec-driven timing),Tor CHAT has irregular human-conversation-driven timing. ...</td><td>(1) TLS record header detected, indicating an encrypted TLS session.(2) TLS dominant (100%), consistent with Tor CHAT profile.(3) Unlike Tor VOIP (codec-driven timing), Tor CHAT has irregular human-conversation-driven timing. ...</td></tr><tr><td>Description</td><td>TLS record headers present, indicating encrypted transport. Instant messaging and chat protocols (AIM, ICQ, Facebook Chat, Hangouts, Skype Chat) tunneled through Tor onion routing. Dominant protocol: TCP (100%). ...</td><td>TLS record headers present, indicating encrypted transport. Instant messaging and chat protocols (AIM, ICQ, Facebook Chat, Hangouts, Skype Chat) tunneled through Tor onion routing. Dominant protocol: TLS (100%).</td></tr><tr><td>Notes</td><td>Chat over Tor hides who is communicating with whom; message content may still be visible at exit nodes if not end-to-end encrypted.</td><td>Chat over Tor provides metadata anonymity; message content may still be visible at exit nodes if not end-to-end encrypted.</td></tr></table>

TABLE VI CSTNET-TLS1.3 FOR SAMPLE #350: MMTRAFFIC CORRECTLY IDENTIFIES THE CLASS. EVIDENCE AND DESCRIPTION FIELDS ARE ABBREVIATED. GREEN MEANS CORRECTLY INTERPRETED KEY CONTENT. 

<table><tr><td>Field</td><td>mmTraffic (Ours)</td><td>Ground Truth</td></tr><tr><td>Class</td><td>Steam √</td><td>Steam</td></tr><tr><td>Traits</td><td>has_tls: truehas_http: falseascii: midentropy: highzero_pad: low</td><td>has_tls: truehas_http: falseascii: lowentropy: highzero_pad: low</td></tr><tr><td>Evidence</td><td>(1) TLS record header detected, indicating an encrypted TLS session.(2) High Shannon entropy: encrypted or compressed payload.(3) Low zero-padding: sustained bulk data transfer. ...</td><td>(1) TLS record header detected, indicating an encrypted TLS session.(2) Low ASCII with high entropy: encrypted payload.(3) Low zero-padding: sustained bulk data transfer.(4) TCP dominant (84.2%). ...</td></tr><tr><td>Description</td><td>TLS record headers alongside high-entropy payload confirm encrypted communication. Valve Steam gaming platform for game downloads, updates, and multiplayer services over TLS 1.3. Large avg. packet (858 bytes). ...</td><td>TLS record headers alongside high-entropy payload confirm encrypted communication. Valve Steam gaming platform for game downloads, updates, and multiplayer services over TLS 1.3. TCP dominant (84.2%). ...</td></tr><tr><td>Notes</td><td>Game distribution platform; monitor for Steam account phishing; Workshop mods can contain malicious code.</td><td>Game distribution platform; game downloads are very large; monitor for Steam account phishing.</td></tr></table>

Shaping the Latent Space with Auxiliary Constraints. While unfreezing the encoder bridges the modality gap, relying exclusively on the LLM’s autoregressive text-generation loss provides weak and implicit supervision, which is insufficient to disentangle highly overlapping encrypted traffic patterns. The critical inflection point occurs in V3 with the introduction of the auxiliary classification head. By directly penalizing misclassifications at the feature bottleneck, $\mathcal { L } _ { \mathrm { a u x } }$ explicitly reshapes the continuous latent space. It forces the encoder to establish

TABLE VII USTC-TFC-2016 FOR SAMPLE #11786: MMTRAFFIC CORRECTLY IDENTIFIES THE CLASS. EVIDENCE AND DESCRIPTION FIELDS ARE ABBREVIATED. GREEN MEANS CORRECTLY INTERPRETED KEY CONTENT. 

<table><tr><td>Field</td><td>mmTraffic(Ours)</td><td>Ground Truth</td></tr><tr><td>Class</td><td>Outlook √</td><td>Outlook</td></tr><tr><td>Traits</td><td>has_tls: truehas_http: falseascii: lowentropy: midzero_pad: mid</td><td>has_tls: truehas_http: falseascii: lowentropy: highzero_pad: low</td></tr><tr><td>Evidence</td><td>(1) TLS record header detected, indicating an encrypted TLS session.(2) TLS dominant (100%), consistent with Outlook profile.(3) Unlike Gmail (HTTP/2 and QUIC), Outlook uses MAPI protocol. ...</td><td>(1) TLS record header detected, indicating an encrypted TLS session.(2) Low ASCII with high entropy: encrypted payload.(3) Low zero-padding: sustained bulk data transfer.(4) TLS dominant (100%). ...</td></tr><tr><td>Description</td><td>TLS record headers present, indicating encrypted transport. Microsoft Outlook email client using HTTPS and MAPI. Dominant protocol: TLS (100%). ...</td><td>TLS record headers alongside high-entropy payload confirm encrypted communication. Microsoft Outlook email client using HTTPS and MAPI. Dominant protocol: TLS (100%).</td></tr><tr><td>Notes</td><td>Generally benign; verify connections go to Microsoft ASN; anomalous sync volumes may indicate data exfiltration.</td><td>Generally benign; verify connections go to Microsoft ASN; anomalous sync volumes or off-hours activity may indicate data exfiltration via email.</td></tr></table>

hard, discriminative boundaries before the features ever reach the LLM. This explicit concept anchoring effectively resolves perceptual ambiguity, propelling the classification accuracy to 0.9312 on ISCX-Tor-2016 and 0.9819 on ISCXVPN2016, while maintaining strong generative performance.

Synergistic Grounding via Semantic-Priority Generation. The final transition to mmTraffic (Full) demonstrates that our semantic-priority generation loss $( \mathcal { L } _ { \mathrm { g e n } } )$ is not merely a linguistic constraint, but a mechanism for cognitive synergy. In standard unconstrained generation (V3), all tokens are treated equally, leaving the model susceptible to generating fluent but ungrounded priors. By dynamically assigning a heavy penalty weight to the categorical prefix tokens, mmTraffic forces the LLM to commit strictly to a physical traffic identity first. Remarkably, rather than acting as a restrictive trade-off, this strong semantic grounding mechanism stabilizes the reasoning chain, pushing the final classification accuracy to its peak across both domains (0.9331 on Tor and 0.9902 on VPN) and maximizing the structural alignment of the generated evidence (Average BERTScore reaches 0.9561 on Tor and 0.9552 on VPN). This confirms that forcing logical rigorousness inherently enhances the overall multimodal reasoning reliability.

# D. Qualitative Evaluation on Traffic Reasoning

Despite the quantitative evaluations, this section presents qualitative analysis of traffic reasoning on three datasets: ISCX-Tor-2016, CSTNet-TLS1.3, and USTC-TFC-2016.

Qualitative Evaluation. Tables V, VI, and VII present high-quality correct classifications across three datasets: ISCX-Tor-2016, CSTNet-TLS1.3, and USTC-TFC-2016. Despite the diversity of encryption contexts, mmTraffic consistently produces forensically grounded reports that accurately characterize the underlying traffic behavior. The CHAT case from ISCX-Tor-2016 (sample #6227) is particularly illustrative. Although the predicted ascii bucket diverges slightly from the ground truth, the generated description correctly identifies the traffic as instant messaging protocols tunneled through Tor onion routing, accurately attributing it to AIM, ICQ, Facebook Chat, Hangouts, and Skype Chat services. This suggests that the joint optimization between the traffic encoder and the LLM effectively compensates for trait-level uncertainty by grounding generation in a semantically aligned feature space. A similar pattern is observed in the Outlook case from USTC-TFC-2016 (sample#11786). While the predicted entropy and zeropadding buckets differ from the ground truth, the generated description correctly identifies the traffic as Microsoft Outlook using HTTPS and MAPI, and accurately distinguishes it from Gmail by referencing Outlook’s exclusive connection to Microsoft infrastructure. This decoupling between trait accuracy and description quality demonstrates that the auxiliary classification head enforces categorical boundaries in the latent space, anchoring the LLM’s generation to the correct traffic identity even when individual byte-level features are imprecise. The Steam case from CSTNet-TLS1.3 (sample #350) further reinforces this observation: under TLS 1.3 where all flows share identical encryption overhead, mmTraffic produces a platform-specific description referencing Valve Steam’s game downloads and multiplayer services, going beyond what raw byte features alone could support.

TABLE VIII ISCX-TOR-2016 FOR SAMPLE #15750: MMTRAFFIC CORRECTLY IDENTIFIES THE VIDEO CLASS WHILE Vanilla VLM MISCLASSIFIES IT AS BROWSING. EVIDENCE AND DESCRIPTION FIELDS ARE ABBREVIATED. GREEN AND RED MEAN CORRECT AND WRONG INTERPRETATIONS. 

<table><tr><td>Field</td><td>mmTraffic (Ours)</td><td>Vanilla VLM</td><td>Ground Truth</td></tr><tr><td>Class</td><td>VIDEO √</td><td>BROWSING ✗</td><td>VIDEO</td></tr><tr><td>Evidence</td><td>(1) Video streaming services (YouTube, Vimeo) tunneled via Tor onion routing.(2) High throughput (49.8 MB/s) indicates active data exchange.(3)Sustained download dominant over upload, consistent with video consumption. ...</td><td>(1) TLS record header detected, indicating encrypted session.(2)High zero-padding: short flow with small payload.(3) TCP dominant (100%),consistent with HTTPS browsing profile. ...</td><td>(1) TCP dominant (100%), consistent with VIDEO profile.(2) Unlike Tor AUDIO (moderate throughput), VIDEO requires significantly higher bandwidth.(3) Unlike Tor BROWSING (bursty), VIDEO maintains sustained high-throughput download. ...</td></tr><tr><td>Description</td><td>Mixed entropy and ASCII across packet slices.Video streaming services (youtube.com, vimeo.com) tunneled via Tor onion routing.TCP dominant. High throughput (498 KB/s). ...</td><td>TLS record headers indicate encrypted transport.HTTPS/SSL web browsing tunneled through Tor hides both location and activities. High zero-padding suggests background activity. ...</td><td>Mixed entropy and ASCII across packet slices. Video streaming services (YouTube HTML5, YouTube Flash, Vimeo) tunneled through Tor. Dominant protocol: TCP (100%).</td></tr></table>

TABLE IX CSTNET-TLS1.3 FOR SAMPLE #4728: MMTRAFFIC CORRECTLY IDENTIFIES THE AD O B E WHILE Vanilla VLM MISCLASSIFIES IT AS B A I D U.C O M. UNDER TLS 1.3, BYTE-LEVEL FEATURES ARE NEARLY IDENTICAL ACROSS ALL WEBSITES. GREEN AND RED MEAN CORRECT AND WRONG INTERPRETATIONS. 

<table><tr><td>Field</td><td>mmTraffic (Ours)</td><td>Vanilla VLM</td><td>Ground Truth</td></tr><tr><td>Class</td><td>Adobe √</td><td>baidu.com ✗</td><td>Adobe</td></tr><tr><td>Evidence</td><td>(1) TLS record header detected.(2)High Shannon entropy: encrypted or binary payload.(3)Low zero-padding: sustained bulk data transfer. ...</td><td>(1) TLS record header detected.(2) High zero-padding: short flow with small payload.(3) TCP dominant (68.5%),consistent with Baidu&#x27;s search and CDN infrastructure. ...</td><td>(1) TLS record header detected.(2) Low ASCII with high entropy: encrypted payload.(3) TLS dominant (55.6%), consistent with Adobe profile. ...</td></tr><tr><td>Description</td><td>TLS record headers alongside high-entropy payload confirm encrypted communication. Adobe creative software, cloud services, and document management platform over TLS 1.3. ...</td><td>TLS record headers indicate active encrypted communication.Large volume of bulk control-plane packets over TCP. Baidu search and CDN infrastructure. ...</td><td>TLS record headers alongside high-entropy payload confirm encrypted communication. Adobe creative software, cloud services, and document management platform over TLS 1.3. ...</td></tr></table>

TABLE X USTC-TFC-2016 FOR SAMPLE #10195: MMTRAFFIC CORRECTLY IDENTIFIES THE GEODO MALWARE FLOW WHILE Vanilla VLM MISCLASSIFIES IT AS HTBOT. BOTH ARE HTTP-BASED BOTNETS WITH SIMILAR BYTE SIGNATURES. GREEN AND RED MEAN CORRECT AND WRONG INTERPRETATIONS. 

<table><tr><td>Field</td><td>mmTraffic (Ours)</td><td>Vanilla VLM</td><td>Ground Truth</td></tr><tr><td>Class</td><td>Geodo √</td><td>Htbot ✗</td><td>Geodo</td></tr><tr><td>Evidence</td><td>(1)High Shannon entropy: encrypted or binary payload.(2)Low zero-padding: sustained bulk data transfer.(3) TCP dominant (100%).(4) Unlike Zeus (banking only), Geodo also performs spam relay.</td><td>(1) HTTP tokens (GET/POST) indicate plaintext HTTP requests.(2) High ASCII: plaintext application-layer content.(3) Low zero-padding: sustained bulk data transfer. ...</td><td>(1) High zero-padding: short flow, small payload.(2) TCP dominant (100%).(3) Unlike Zeus (banking only), Geodo also performs spam relay. ...</td></tr><tr><td>Description</td><td>Mixed entropy and ASCII characteristics. Geodo/Emotet banking trojan and email spam botnet. Dominant protocol: TCP (100%). ...</td><td>HTTP method tokens and readable ASCII confirm plaintext botnet-driven web scraping or C&amp;C command execution (Htbot). Low throughput suggests sparse traffic. ...</td><td>Mixed entropy and ASCII characteristics. Geodo/Emotet banking trojan and email spam botnet. Dominant protocol: TCP (100%).</td></tr></table>

Qualitative Effect of Joint Optimization. Tables VIII, IX, and X present cases where mmTraffic correctly identifies the traffic category while the Vanilla VLM produces an erroneous classification, revealing how joint optimization resolves the semantic gap that a frozen encoder cannot bridge. Crucially, the misclassifications are not random: the predicted category shares substantial byte-level similarity with the ground truth. On ISCX-Tor-2016, VIDEO is confused with BROWSING because both exhibit similar Tor-tunneled TCP flows and differ primarily in sustained throughput consistency rather than observable byte patterns. On CSTNet-TLS1.3, Adobe is misidentified as baidu.com because TLS 1.3 eliminates all certificate metadata, leaving both flows with nearly identical TLS record headers and entropy profiles that are indistinguishable at the byte level with a frozen encoder. On USTC-TFC-2016, Geodo is confused with Htbot because both are HTTP-based botnets relying on similar C&C communication patterns. This systematic pattern demonstrates that a frozen encoder fails to project fine-grained categorical boundaries into the LLM’s lexical space. By contrast, mmTraffic allows gradient feedback from the auxiliary classification head to actively reshape the encoder’s feature space, forcing it to learn language-aligned representations that carry explicit categorical semantics. The downstream effect is consistent: without joint optimization, the generated reports describe the wrong traffic identity, producing forensically plausible but factually incorrect outputs.

TABLE XI ISCX-TOR-2016 FOR SAMPLE #6622: MMTRAFFIC FAILS TO CLASSIFY. RED MEANS WRONG INTERPRETATIONS IN KEY SEMANTICS. 

<table><tr><td>Field</td><td>mmTraffic (Ours)</td><td>Ground Truth</td></tr><tr><td>Class</td><td>BROWSING ✗</td><td>FILE-TRANSFER</td></tr><tr><td>Traits</td><td>has_tls: falsehas_http: falseascii: lowentropy: midzero_pad: mid</td><td>has_tls: falsehas_http: falseascii: midentropy: lowzero_pad: mid</td></tr><tr><td>Evidence</td><td>(1) TCP dominant (100%), consistent with profile.(2) Unlike direct HTTPS browsing, Tor browsing shows only Tor relay IPs.(3) More bursty than Tor AUDIO or VOIP. ...</td><td>(1) TCP dominant (100%), consistent with FILE-TRANSFER profile.(2) Unlike Tor P2P (bidirectional), FILE-TRANSFER is predominantly unidirectional.(3) FILE-TRANSFER shows sustained throughput vs Tor BROWSING (bursty with idle gaps). ...</td></tr><tr><td>Description</td><td>HTTPS/SSL web browsing tunneled through Tor onion routing, including both direct Tor Browser usage and gateway-proxied SSL browsing. Dominant protocol: TCP. ...</td><td>Mixed entropy and ASCII characteristics. File transfer protocols (FTP, SFTP, Skype file transfer) tunneled through Tor onion routing. Dominant protocol: TCP (100%).</td></tr><tr><td>Notes</td><td>Tor browsing provides strong anonymity; exit node traffic is unencrypted unless HTTPS is used end-to-end.</td><td>File transfer over Tor hides source and destination; commonly used to transfer sensitive documents.</td></tr></table>

TABLE XII CSTNET-TLS1.3 FOR SAMPLE #6404: MMTRAFFIC FAILS TO CLASSIFY. RED MEANS WRONG INTERPRETATIONS IN KEY SEMANTICS. 

<table><tr><td>Field</td><td>mmTraffic (Ours)</td><td>Ground Truth</td></tr><tr><td>Class</td><td>arXiv ✗</td><td>Semantic Scholar</td></tr><tr><td>Traits</td><td>has_tls: truehas_http: falseascii: lowentropy: highzero_pad: mid</td><td>has_tls: truehas_http: falseascii: midentropy: highzero_pad: mid</td></tr><tr><td>Evidence</td><td>(1) TLS record header detected.(2) Low ASCII with high entropy: encrypted payload.(3) TCP dominant (96.8%),consistent with arXiv profile.(4) Similar PDF download pattern to ACM and IEEE. ...</td><td>(1) TLS record header detected.(2) High Shannon entropy: encrypted payload.(3) TCP dominant (97.9%), consistent with Semantic Scholar profile.(4) More API-driven than traditional academic publishers. ...</td></tr><tr><td>Description</td><td>TLS record headers alongside high-entropy payload confirm encrypted communication.arXiv open-access academic preprint repository for physics, math, and CS over TLS 1.3. Large avg. packet (925 bytes). ...</td><td>TLS record headers alongside high-entropy payload confirm encrypted communication. Semantic Scholar AI-powered academic paper search and knowledge graph over TLS 1.3. Large avg. packet (964 bytes). ...</td></tr><tr><td>Notes</td><td>Open academic repository; monitor for automated bulk downloading indicating research scraping bots.</td><td>Allen Institute AI-operated academic search; open access focus means fewer paywall authentication flows.</td></tr></table>

# E. Limitation Analysis

Failure Cases. Tables XI, XII, and XIII present failure cases where mmTraffic produces an incorrect classification. On ISCX-Tor-2016, FILE-TRANSFER is misclassified as BROWSING because both categories produce similar TCP flows under Tor multi-hop encryption, without an observable protocol marker to distinguish sustained file transfer from bursty web browsing. On CSTNet-TLS1.3, Semantic Scholar is misclassified as arXiv because both are open-access academic platforms that share nearly identical TLS 1.3 byte signatures, making them fundamentally indistinguishable at the byte level without application-layer metadata. On USTC-

TABLE XIII USTC-TFC-2016 FOR SAMPLE #4090: MMTRAFFIC FAILS TO CLASSIFY. RED MEANS WRONG INTERPRETATIONS IN KEY SEMANTICS. 

<table><tr><td>Field</td><td>mmTraffic (Ours)</td><td>Ground Truth</td></tr><tr><td>Class</td><td>Geodo ✗</td><td>Htbot</td></tr><tr><td>Traits</td><td>has_tls: falsehas_http: falseascii: highentropy: lowzero_pad: mid</td><td>has_tls: falsehas_http: falseascii: highentropy: lowzero_pad: mid</td></tr><tr><td>Evidence</td><td>(1) High ASCII with low entropy: repetitive plaintext content.(2) DNS dominant (100%), consistent with profile.(3) Unlike Zeus (banking only), Geodo also performs spam relay. ...</td><td>(1) High ASCII with low entropy: repetitive plaintext content.(2) DNS dominant (100%), consistent with Htbot profile.(3) Unlike Miuref (click fraud), Htbot focuses on C&amp;C command execution.</td></tr><tr><td>Description</td><td>Substantial readable ASCII content present. Geodo/Emotet banking tro-jan and email spam botnet. Dominant protocol: DNS (89.1%). Uses HTTP-based C&amp;C more frequently than Zeus.</td><td>Substantial readable ASCII content present. HTTP-based botnet using web proxies for C&amp;C (Htbot). Dominant protocol: DNS (100%).</td></tr><tr><td>Notes</td><td>High-risk banking trojan; block known Geodo C&amp;C IPs; inspect SMTP traffic for spam relay.</td><td>Monitor for HTTP requests with unusual headers; correlate with known Htbot infrastructure.</td></tr></table>

TFC-2016, Htbot is misclassified as Geodo because both are DNS-based botnets with nearly identical ASCII ratios, entropy profiles, and protocol distributions. In all three cases, the misclassification originates at the perceptual stage: even with end-to-end joint optimization, the encoder fails to establish sufficiently discriminative boundaries between classes that share highly similar byte-level signatures. The erroneous categorical prediction then propagates into the cognitive module, producing reports that are internally consistent with the predicted class rather than the ground truth. Despite the prediction errors, this transparency remains an operational advantage: the cognitive module faithfully reflects the perceptual judgment, making the error visible and traceable in the generated report rather than silently absorbed into an opaque label. For a network analyst, the evidence chain in the generated report can be independently verified against the raw traffic, and discrepancies between the reported behavior and observed network activity serve as a natural signal that the classification may warrant further investigation. In security-sensitive applications such as malware triage, encrypted traffic auditing, and network incident response, both high-fidelity generation under correct perception and transparent failure under incorrect perception represent a practical step toward interpretable traffic analysis.

Paradigm, Benchmark and Evaluation. While mmTraffic demonstrates strong performance across diverse encrypted traffic benchmarks, several aspects of the current design require further investigation. The tight coupling between the perceptual and cognitive layers also means that the traffic reasoning quality is inherently linked to the reliability of the traffic encoder. Exploring mechanisms that allow the cognitive layer to express uncertainty or partially recover from perceptual errors represents a promising direction for future work. Additionally, the current benchmark construction pipeline relies on Claude Opus to generate reference reports from structured traffic features. Although this pipeline can produce high-quality annotations, its scalability to open-world applications with new datasets or emerging traffic categories may be limited. Finally, a more comprehensive traffic reasoning evaluation protocol is still a worthwhile avenue.

# VI. CONCLUSION AND FUTURE WORK

This paper addresses multi-modal traffic reasoning for the first time, successfully bridging the gap between highprecision encrypted traffic classification and human-readable forensic report generation. By developing the foundational Byte-Grounded Traffic Description benchmark, i.e., BGTD and proposing a jointly optimized multi-modal traffic reasoning architecture with large language model (LLM), i.e., mmTraffic, we transform encrypted traffic analysis from a black-box classification paradigm to an auditable generative paradigm towards explainable traffic interpretations. Unlike previous decoupled pipelines that freeze the traffic encoder, mmTraffic actively unfreezes the encoder and trains it synergistically with the LLM. Extensive evaluations across six diverse benchmarks demonstrate that mmTraffic achieves high-fidelity, evidencegrounded traffic report generation, while maintaining highly competitive classification accuracy, confirming its success in resolving the semantic gap between physical network bytes and human-understandable concepts.

In future work, one key direction is to optimize inference latency to support real-time flow analytics and introduce uncertainty quantification to allow the cognitive layer to explicitly handle low-confidence perceptual predictions in adversarial scenarios. Furthermore, a more scalable automated annotation process to efficiently extend the framework to emerging cryptographic protocols and open-world traffic categories remains a worthwhile direction.

# REFERENCES

[1] G. Aceto, D. Ciuonzo, A. Montieri, and A. Pescape, “Distiller: Encrypted ´ traffic classification via multimodal multitask deep learning,” Journal of Network and Computer Applications, vol. 183, p. 102985, 2021.   
[2] E. Aghaei, X. Niu, W. Shadid, and E. Al-Shaer, “Securebert: A domainspecific language model for cybersecurity,” in international conference on security and privacy in communication systems, 2022, pp. 39–56.   
[3] J.-B. Alayrac, J. Donahue, P. Luc, A. Miech, I. Barr, Y. Hasson, K. Lenc, A. Mensch, K. Millican, M. Reynolds et al., “Flamingo: a visual language model for few-shot learning,” NeurIPS, pp. 23 716–23 736, 2022.   
[4] Anonymous, “Semantic-driven interpretable deep multi-modal hashing for large-scale multimedia retrieval,” IEEE Transactions on Multimedia, vol. 23, 2021.   
[5] A. B. Arrieta, N. D´ıaz-Rodr´ıguez, J. Del Ser, A. Bennetot, S. Tabik, A. Barbado, S. Garc´ıa, S. Gil-Lopez, D. Molina, R. Benjamins ´ et al., “Explainable artificial intelligence (xai): Concepts, taxonomies, opportunities and challenges toward responsible ai,” Information fusion, vol. 58, pp. 82–115, 2020.   
[6] Y. Chen and Y. Wang, “Mpaf: Encrypted traffic classification with multiphase attribute fingerprint,” IEEE Transactions on Information Forensics and Security, vol. 19, pp. 7091–7105, 2024.   
[7] T. Cui, X. Lin, S. Li, M. Chen, Q. Yin, Q. Li, and K. Xu, “Trafficllm: Enhancing large language models for network traffic analysis with generic traffic representation,” arXiv preprint arXiv:2504.04222, 2025.   
[8] W. Dai, J. Li, D. Li, A. Tiong, J. Zhao, W. Wang, B. Li, P. N. Fung, and S. Hoi, “Instructblip: Towards general-purpose vision-language models with instruction tuning,” NeurIPS, pp. 49 250–49 267, 2023.   
[9] R. Dingledine, N. Mathewson, and P. Syverson, “Tor: The secondgeneration onion router,” 2004.   
[10] W. Dong, J. Yu, X. Lin, G. Gou, and G. Xiong, “Deep learning and pretraining technology for encrypted traffic classification: A comprehensive review,” Neurocomputing, vol. 617, p. 128444, 2025.   
[11] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of encrypted and vpn traffic using time-related,” in ICISSP, 2016, pp. 407–414.

[12] P. Goyal, P. Dollar, R. Girshick, P. Noordhuis, L. Wesolowski, A. Kyrola, ´ A. Tulloch, Y. Jia, and K. He, “Accurate, large minibatch sgd: Training imagenet in 1 hour,” arXiv preprint arXiv:1706.02677, 2017.   
[13] A. Gu and T. Dao, “Mamba: Linear-time sequence modeling with selective state spaces,” in First conference on language modeling, 2024.   
[14] W. Guo, Y. Zhang, X. Cai, L. Meng, J. Yang, and X. Yuan, “Ld-man: Layout-driven multimodal attention network for online news sentiment recognition,” IEEE Transactions on Multimedia, 2020.   
[15] G. Han, M. Lin, Z. Li, H. Zhao, and S. Kwong, “Text-to-image person reidentification based on multimodal graph convolutional network,” IEEE Transactions on Multimedia, vol. 26, 2024.   
[16] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen et al., “Lora: Low-rank adaptation of large language models.” Iclr, 2022.   
[17] A. H. Lashkari, G. D. Gil, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of tor traffic using time based features,” in ISSP, vol. 2, 2017, pp. 253–262.   
[18] C.-Y. Lin, “Rouge: A package for automatic evaluation of summaries,” in Text summarization branches out, 2004, pp. 74–81.   
[19] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in Proceedings of the ACM Web Conference 2022, 2022.   
[20] H. Liu, C. Li, Q. Wu, and Y. J. Lee, “Visual instruction tuning,” NeurIPS, vol. 36, pp. 34 892–34 916, 2023.   
[21] J. Liu, C. Liu, P. Zhou, R. Lv, K. Zhou, and Y. Zhang, “Is chatgpt a good recommender? a preliminary study,” arXiv, 2023.   
[22] L. Liu, R. Li, Q. Li, M. Hou, Y. Jiang, and M. Xu, “Flowletformer: Network behavioral semantic aware pre-training model for traffic classification,” arXiv preprint arXiv:2508.19924, 2025.   
[23] Y. Liu, W. Wei, D. Peng, X.-L. Mao, Z. He, and P. Zhou, “Depth-aware and semantic guided relational attention network for visual question answering,” IEEE Transactions on Multimedia, 2022.   
[24] I. Loshchilov and F. Hutter, “Decoupled weight decay regularization,” arXiv preprint arXiv:1711.05101, 2017.   
[25] S. M. Lundberg and S.-I. Lee, “A unified approach to interpreting model predictions,” NeurIPS, vol. 30, 2017.   
[26] P. Micikevicius, S. Narang, J. Alben, G. Diamos, E. Elsen, D. Garcia, B. Ginsburg, M. Houston, O. Kuchaiev, G. Venkatesh et al., “Mixed precision training,” arXiv preprint arXiv:1710.03740, 2017.   
[27] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark et al., “Learning transferable visual models from natural language supervision,” in ICML, 2021.   
[28] S. Rajbhandari, J. Rasley, O. Ruwase, and Y. He, “Zero: Memory optimizations toward training trillion parameter models,” in SC20: international conference for high performance computing, networking, storage and analysis. IEEE, 2020, pp. 1–16.   
[29] J. Ren, D. Dubois, and D. Choffnes, “An international view of privacy risks for mobile apps,” Tech. Rep, 2019.   
[30] M. T. Ribeiro, S. Singh, and C. Guestrin, “Why should i trust you?” explaining the predictions of any classifier,” in ACM SIGKDD, 2016.   
[31] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, and D. Batra, “Grad-cam: Visual explanations from deep networks via gradient-based localization,” in ICCV, Oct 2017.   
[32] M. Shen, J. Wu, K. Ye, K. Xu, G. Xiong, and L. Zhu, “Robust detection of malicious encrypted traffic via contrastive learning,” IEEE Transactions on Information Forensics and Security, vol. 20, pp. 4228–4242, 2025.   
[33] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, “Attention is all you need,” Advances in neural information processing systems, vol. 30, 2017.   
[34] T. Wang, X. Xie, W. Wang, C. Wang, Y. Zhao, and Y. Cui, “Netmamba: Efficient network traffic classification via pre-training unidirectional mamba,” arXiv preprint arXiv:2405.11449, 2024.   
[35] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware traffic classification using convolutional neural network for representation learning,” in ICOIN, 2017, pp. 712–717.   
[36] A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv et al., “Qwen3 technical report,” arXiv, 2025.   
[37] T. Zhang, V. Kishore, F. Wu, K. Q. Weinberger, and Y. Artzi, “Bertscore: Evaluating text generation with bert,” arXiv, 2019.   
[38] R. Zhao, M. Zhan, X. Deng, Y. Wang, Y. Wang, G. Gui, and Z. Xue, “Yet another traffic classifier: A masked autoencoder based traffic transformer with multi-level flow representation,” in AAAI, vol. 37, 2023.   
[39] Q. Zhou, L. Wang, H. Zhu, T. Lu, and V. S. Sheng, “Wf-transformer: Learning temporal features for accurate anonymous traffic identification by using transformer networks,” IEEE Transactions on Information Forensics and Security, 2024.
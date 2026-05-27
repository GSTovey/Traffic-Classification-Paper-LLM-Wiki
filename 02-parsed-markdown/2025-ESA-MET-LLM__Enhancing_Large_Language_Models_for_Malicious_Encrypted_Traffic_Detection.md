# Journal Pre-proof

MET-LLM: Enhancing Large Language Models for Malicious Encrypted Traffic Detection

Yongjun Huang, Pengfei Du, Ruifan Li, Xiaoyong Li, Lixiang Li

PII: S0957-4174(25)04236-8

DOI: https://doi.org/10.1016/j.eswa.2025.130621

Reference: ESWA 130621

To appear in: Expert Systems With Applications

Received date: 23 July 2025

Revised date: 8 November 2025

Accepted date: 27 November 2025

![](images/dd1fd8bd2b7d4ff77ed15ba87bb4f4b8f32127850cc3684670d22825262fdab3.jpg)

<details>
<summary>text_image</summary>

ISSN 0367-417N
ELENEYER
Expert
Systems
with
Applications
An International
Journal
Editor-in-Chief
Binshan Lin
</details>

Please cite this article as: Yongjun Huang, Pengfei Du, Ruifan Li, Xiaoyong Li, Lixiang Li, MET-LLM: Enhancing Large Language Models for Malicious Encrypted Traffic Detection, Expert Systems With Applications (2025), doi: https://doi.org/10.1016/j.eswa.2025.130621

This is a PDF of an article that has undergone enhancements after acceptance, such as the addition of a cover page and metadata, and formatting for readability. This version will undergo additional copyediting, typesetting and review before it is published in its final form. As such, this version is no longer the Accepted Manuscript, but it is not yet the definitive Version of Record; we are providing this early version to give early visibility of the article. Please note that Elsevier’s sharing policy for the Published Journal Article applies to this version, see: https://www.elsevier.com/about/ policies-and-standards/sharing#4-published-journal-article. Please also note that, during the production process, errors may be discovered which could affect the content, and all legal disclaimers that apply to the journal pertain.

© 2025 Published by Elsevier Ltd.

# MET-LLM: Enhancing Large Language Models for Malicious Encrypted Traffic Detection

Yongjun Huanga, Pengfei Dub, Ruifan Li∗a, Xiaoyong Lic, Lixiang Lic

aSchool of Artificial Intelligence, Beijing University of Posts and Telecommunications

bSchool of Cyberspace Security, Shandong University of Political Science and Law

cSchool of Cyberspace Security, Beijing University of Posts and Telecommunications

# Abstract

Modern networks have spurred growth in both legitimate and malicious activities concealed within encrypted traffic. Traditional machine learning approaches to traffic classification struggle with scalability to new protocols, diverse tasks, and adaptability to emerging threats. To address these issues, we propose MET-LLM, a novel framework for Malicious Encrypted Traffic detection that integrates domain-specific tokenization, a pretrained large language model, and a dynamic adaptive tuning adaptor. MET-LLM addresses the modal gap between natural language and heterogeneous network traffic data by partitioning each traffic sample into distinct headers and payloads and leveraging a specialized tokenizer trained on a large-scale traffic corpus to extend the base vocabulary of the underlying language model. Building on a domainadapted pretrained model fine-tuned on extensive security-related corpora, MET-LLM captures critical contextual nuances distinguishing benign from malicious flows. Its dynamic adaptive tuning adaptor facilitates efficient parameter updates via adaptation prompt injection, adversarial training, and dynamic masking, enabling rapid adaptation to evolving network conditions and attack strategies. Extensive evaluations on benchmark datasets, including ISCX Tor 2016, ISCX VPN 2016, APP-53 2023, and CSTNET 2023, demonstrate that MET-LLM’s superior precision, recall, and F1 scores over stateof-the-art methods, affirming its efficacy and robustness in real-world cybersecurity applications. Our code is publicly available at the website, https://github.com/Superagentsys/MET-LLM.

Keywords: Malicious Encrypted Traffic Detection, Large Language Model, Traffic Embedding, Domain Adaptation.

# 1. Introduction

The rapid development in encrypted network traffic has significantly transformed the landscape of cybersecurity. Although encryption protocols such as Transport Layer Security (TLS) ensure privacy, studies indicate that over 95% of web traffic is encrypted [1, 2]. They present challenges for security monitoring infrastructures. This adoption of encryption is vital for preserving data confidentiality and integrity. However, it has altered how organizations approach threat detection and traffic analysis [3, 4].

As illustrated in Figure 1, encrypted traffic exhibits characteristics that complicate security analysis. Cryptographic transformations obscure payload content, rendering traditional deep packet inspection (DPI) ineffective without private key access. While encryption strengthens communication privacy, it reduces visibility of potential threats within network infrastructure [3, 5]. This limitation has redirected current research towards analytical methodologies based on metadata extraction, statistical pattern recognition, and behavioral modeling for intrusion detection and traffic classification [6, 7].

Threat intelligence highlights the security implications of increased encryption. Malicious actors leverage encryption to obfuscate attack vectors. Studies report that approximately 70% of malware campaigns utilize encrypted channels, a 30% increase since 2018 [8]. Techniques such as SSL/TLS tunneling for command-andcontrol communications, encrypted data exfiltration, and malware delivery mechanisms allow threat actors to blend with legitimate encrypted traffic patterns [9].

Despite advances in machine learning approaches for encrypted traffic analysis, existing solutions exhibit constraints in practical deployment [10, 11, 12]. First, conventional approaches rely on manual feature engineering and struggle to encode the semantic structure of network data, such as protocol structures, timing patterns, and encrypted payloads. This limitation reduces resilience to obfuscation techniques employed by persistent threats [12, 13]. Second, these methods are tailored to specific detection tasks, hindering knowledge transfer and generalization across tasks [14]. Third, existing methods lack the flexibility to adapt to the evolving nature of modern threat landscapes [15].

Recent advances in large language models (LLMs), such as Deepseek [16] and Llama [17], have enhanced the ability to process complex data patterns across diverse domains. Initially designed for text generation, these transformer-based models with extensive parameterization now extend to managing scenarios across different data types. Their strong contextual understanding offers a promising approach for addressing challenges in encrypted traffic analysis [18, 19].

Applying these LLMs to malicious encrypted traffic detection represents an advancement in network security. Though originally designed for natural language processing (NLP) tasks, these transformer-based architectures can identify complex patterns, generalize across classifi-

Email addresses: huangyj2022@bupt.edu.cn (Yongjun Huang ), 002344@sdupsl.edu.cn (Pengfei Du ), rfli@bupt.edu.cn (Ruifan Li∗), lixiaoyong@bupt.edu.cn (Xiaoyong Li), lixiang@bupt.edu.cn (Lixiang Li)

<table><tr><td>Encrypted Payload</td></tr><tr><td>65:a0:b6:23:a7:29:f9:0b:cf:76:bb: 9b:fb:f2:81:e1:72:2e:b7:33:b7:29:f9 9b:fb:f2:81:e1:72:2e:b7:33:b7:29 :f9:fb:f2:81:e1</td></tr><tr><td>IP</td></tr><tr><td>Version: 4 Header Length: 20 bytes Total Length: 1500 bytes Identification: 0x6350 Flags: DF (Don&#x27;t Fragment) TTL: 64 Protocol: TCP (6) Source IP:10.67.797.1 Destination IP: 11.34.2.5</td></tr><tr><td>Ethernet</td></tr><tr><td>Destination MAC: 88:e9:fe:70:51 Source MAC:04:d9:f5:9b:5c Ether Type: 0x0800 (IPv4)</td></tr><tr><td>Frame</td></tr><tr><td>Encapsulation Type: 1 Timestamp: Jul 28, 20214 Frame Length: 1614 bytes</td></tr></table>

Figure 1: A network packet is illustrated with frame, Ethernet, IP, and TCP details with an encrypted payload.

cation objectives, and adapt to new traffic patterns with minimal fine-tuning. These capabilities align with the requirements of network security applications [20, 21].

LLMs offer advantages for the detection of malicious encrypted traffic. First, they could learn complex patterns in encrypted traffic data without relying on extensive manual feature engineering. This is valuable for detecting advanced evasion malware. Second, the transformer architecture captures long-range dependencies within network flows. This enables the identification of attacks spanning multiple connections or extended durations. Third, LLMs’ generalization capabilities allow them to adapt to new threats using task-specific training data. Recent works have explored traffic-specific pre-training and specialized tokenization strategies to better align LLMs with network analysis tasks. For example, TrafficFormer [22] highlights the potential of LLMs in encrypted traffic analysis by integrating NLP into network security.

Based on the aforementioned investigation, we have the following assumption. LLMs could be improved on the analysis of malicious encrypted traffic. However, several challenges hinder their effective application. First, the modality gap between natural language and network data, including structured headers and encrypted payloads, limits the effectiveness of conventional tokenizers [23]. Second, the absence of unified representations of network data complicates the identification of malicious traffic and the LLM’s training for security applications. Third, retraining large-parameter models for evolving threats incurs substantial computational costs, requiring an efficient adaptation mechanism [24].

In this paper, we propose a unified framework,

Malicious Encrypted Traffic Large Language Model (MET-LLM) for malicious encrypted traffic detection. our MET-LLM integrates domain-specific tokenization, a pretrained large language model, and a dynamic adaptive tuning adaptor (DATA). Our framework combines transformer-based representation learning and parameterefficient adaptation mechanisms. Evaluations on four benchmark datasets demonstrate that MET-LLM outperforms current state-of-the-art detection methods, achieving F1 scores exceeding 0.96 across traffic scenarios and attack categories.

Our major contributions are summarized as follows.

• We propose a tokenization strategy that bridges the modality gap between natural language and network traffic data. Each traffic sample is divided into head and payload segments, with segment-specific tokenization applied using Byte Pair Encoding (BPE) trained on a traffic-domain corpus [25]. Our approach enables an effective representation of humanreadable headers and hex-encoded payloads.   
• We leverage a domain-adapted pretrained language model, Deepseek, enhanced with security-specific pretraining. This integration enables the model to capture contextual patterns in network traffic, thus improving the detection of malicious activity.   
We introduce a novel fine-tuning module, DATA. It supports flexible and parameter-efficient model adaptation to evolving operational environments and network conditions. DATA uses adaptation prompt injection, adversarial training, and dynamic masking to ensure robustness against traffic obfuscation and protocol modifications while efficiently integrating new task-specific knowledge.

# 2. Related Work

We divide recent works into two groups, fingerprintingbased methods and deep learning-based methods.

# 2.1. Fingerprinting Based Methods

Fingerprinting approaches represent the earliest systematic attempts to analyze encrypted traffic without decryption. These techniques rely on statistical, temporal, and behavioral features extracted from the network flows to construct distinctive signatures or “fingerprints." The pioneering study by Moore and Zuev [26] showed that supervised learning on statistical flow features could effectively classify traffic, laying the foundation for subsequent research. Taylor et al. [27] extended these concepts with AppScanner, an automated system that leveraged burstlevel statistics and temporal features to fingerprint smartphone applications from encrypted traffic. Their approach achieved 87% accuracy across a diverse range of mobile applications without requiring decryption.

Website fingerprinting has emerged as a prominent research focus within encrypted traffic analysis. Panchenko et al. [28] developed a weight-based classification approach capable of operating on the Internet with strong robustness against various countermeasures, thus maintaining computational efficiency and high accuracy. Hayes and Danezis [29] introduced k-fingerprinting, a scalable framework employing random decision forests to identify website access patterns from encrypted traffic, improving classification accuracy and resilience against minor traffic perturbations. Al-Naami et al. [30] further refined fingerprinting by incorporating bidirectional dependency analysis, which adaptively captures temporal and directional features in encrypted flows. This approach is effective across diverse applications, network environments, and encryption protocols. Further extensions by Sirinam et al. [31] demonstrate that deep learning techniques could circumvent conventional fingerprinting defenses, highlighting the dynamic, adversarial nature of encrypted traffic analysis. Recent progress has aimed to reduce reliance on large labeled datasets. Van Ede et al. [32] proposed FlowPrint, a semi-supervised fingerprinting framework for mobile application identification. By clustering the network flows based on temporal correlations and destination similarity, FlowPrint enables effective classification with minimal labeled data and adapts well to previous unseen applications.

![](images/f8f07882bebdf6fb99a2af4f2382798ee2aa8fdb4a526e14eb893fe0e04e3e54.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["a) Traffic Embedding"] --> B["Raw Traffic"]
    B --> C["Header Segment"]
    C --> D["Feature Extraction"]
    D --> E["Hexadecimal encoding"]
    E --> F["Byte Pair Encoding"]
    F --> G["Structured Input Assembly"]
    G --> H["[CLS"] Header["Head"] Payload["EOS"] Tokens]
    H --> I["DeepSeek (Decoder-only Transformer, 7B)"]
    
    J["b) Domain-Adapted Pretrained LLM"] --> K["Security-Related Corpora"]
    K --> L["Prompt [CLS"]Give... [EOS]]
    L --> M["Traffic Tokens [CLS"]ip.len:200... [Head]7b6c["EOS"]]
    M --> N["DeepSeek"]
    N --> O["DownStream Task"]
    
    P["c) DATA"] --> Q["Pretrained Base Model (Frozen Parameters) + Prompt Parameter (θprompt) + Lora Parameter (θLora) + Classifier Parameter(θclassifier)"]
    Q --> R["Robustness Enhancement"]
    R --> S["Rapid Adaptation Module"]
    S --> T["Parameter Efficient Tun"]
    T --> U["Adversarial Prompt Training w/Noise"]
    T --> V["Dynamic Traffic Masking"]
    U --> W["Malware Traffic Detection"]
    V --> X["Tor Detection"]
```
</details>

Figure 2: The architectural overview of our proposed MET-LLM. Our MET-LLM comprises of three primary components: traffic embedding, pretrained LLM, and DATA. The first component transforms heterogeneous network data into LLM-compatible representations. The second leverages domainadapted contextual modeling. The third enables efficient parameter updates and adaptation to the evolving threats.

# 2.2. Deep Learning Based Methods

Deep learning has significantly advanced encrypted traffic analysis by enabling automatic feature extraction and complex pattern recognition directly from raw traffic data. These approaches have reduced dependence on manual, domain-specific feature engineering while improving classification performance across diverse traffic types. Convolutional Neural Networks (CNNs) were among the first deep learning models applied to this task. Wang et al. [33] highlighted their effectiveness for end-toend encrypted traffic classification by treating raw bytes as one-dimensional input sequences. This approach eliminated the need for manual feature extraction and achieved competitive accuracy on popular benchmarks. Further-

more, Liu et al. [34] introduced Flow Sequence Networks (FS-Net), modeling temporal relationships within network flows. FS-Net captured both short- and long-term dependencies. It significantly surpasses the performance of traditional methods, particularly for traffic with complex temporal patterns.

Recurrent Neural Networks (RNNs) and their variants have been extensively explored for their strength in modeling sequential data. Lotfollahi et al. [15] presented Deep Packet, a comprehensive framework that combines CNNs and stacked autoencoders to perform traffic characterization and application identification directly from encrypted data. The framework effectively adapted to various traffic types without relying on predefined features, yielding high accuracy exceeding 98% for certain applications. For specialized environments, such as Industrial Internet of Things, Lin et al. [35] proposed TSCRNN, integrating convolutional and recurrent layers to efficiently capture both spatial and temporal features from encrypted traffic flows. Designed for resource-constrained environments, TSCRNN delivers strong performance while maintaining computational efficiency.

Graph-based approaches have also revealed considerable potential in encrypted traffic analysis. Shen et al. [36] showed the efficacy of Graph Neural Networks for decentralized identification. Their framework models network traffic as graphs where nodes represent hosts and edges capture communication patterns. This representation enables the detection of advanced applications that distribute traffic across multiple flows. It offers robustness against evasion techniques designed to obfuscate traffic patterns through flow distribution.

The adoption of transformer architectures has recently spurred notable progress in encrypted traffic analysis. The seminal work by He et al. [20] introduced PERT, leveraging self-attention mechanisms to generate robust payload representations and effectively model long-range dependencies, overcoming a critical limitation of earlier methods. Subsequently, Lin et al. [18] developed ET-BERT, adapting BERT’s pre-training objectives to the network domain to create contextualized datagram representations that significantly improved classification accuracy. Recent works have further refined transformer-based techniques. Zhao et al. [19] proposed YATC (Yet Another Traffic Classifier), combining masked autoencoder principles with multi-level flow representation. Zhou et al. [22] introduced TrafficFormer, featuring hierarchical attention mechanisms for capturing multi-scale traffic patterns. Meanwhile, Liu et al. [21] developed NetMamba, a network-specific adaptation of the efficient Mamba. It designed to model long-range dependencies in network traffic classification tasks.

<table><tr><td>Symbol</td><td>Definition</td><td>Ref.</td></tr><tr><td> $x$ </td><td>Raw traffic sample.</td><td>Sec. 3.1</td></tr><tr><td> $(x^{H}, x^{P})$ </td><td>Header and payload segments obtained by splitting  $x$ .</td><td>Sec. 3.1</td></tr><tr><td> $F(x)$ </td><td>Extracted domain features from  $x$ .</td><td>Eq. (1)</td></tr><tr><td>Extractor $(x)$ </td><td>Feature extractor operator returning  $F(x)$ .</td><td>Eq. (1)</td></tr><tr><td> $\tau_{H}(x^{H}), \tau_{P}(x^{P})$ </td><td>Segment tokenizers for header and payload producing token sequences.</td><td>Eq. (2)</td></tr><tr><td> $\{t_{H,i}\}_{i=1}^{m}, \{t_{P,j}\}_{j=1}^{n}$ </td><td>Tokens from header/payload;  $m, n$  are token counts for each segment.</td><td>Eq. (2)</td></tr><tr><td> $T(x)$ </td><td>Assembled token sequence for input to the LLM.</td><td>Eq. (3)</td></tr><tr><td> $\oplus$ </td><td>Sequence concatenation operator.</td><td>Eq. (3)</td></tr><tr><td>[CLS], [HEAD], [BODY]</td><td>Special delimiter tokens for sequence structure.</td><td>Eq. (3)</td></tr><tr><td> $V_{\text {Traffic}}, V_{\text {LLM}}, V_{\text {New}}$ </td><td>Traffic/domain vocabulary, base LLM vocabulary, and newly learned tokens;  $V_{\text {Traffic}} = V_{\text {LLM}} \cup V_{\text {New}}$ .</td><td>Sec. 3.1</td></tr><tr><td> $\text {LLM}_{\theta}(\cdot)$ </td><td>Pretrained backbone mapping tokens to contextual representations.</td><td>Sec. 3.2</td></tr><tr><td> $H, H_{[\text {CLS}]}$ </td><td>Contextual representation matrix and the [CLS] vector used for classification.</td><td>Sec. 3.2</td></tr><tr><td> $C(\cdot)$ </td><td>Classification head producing logits and probabilities.</td><td>Sec. 3.2</td></tr><tr><td>logits,  $\hat{y}$ </td><td>Output logits and predicted probability distribution.</td><td>Sec. 3.2</td></tr><tr><td> $W \in \mathbb{R}^{c \times d}, b \in \mathbb{R}^{c}, c$ </td><td>Classifier parameters and number of classes in softmax prediction  $\hat{y}$ .</td><td>Sec. 3.2</td></tr><tr><td> $\theta_{\text {adapt}}$ </td><td>Trainable adaptor parameters  $\{\theta_{\text {prompt}}, \theta_{\text {lora}}, \theta_{\text {classifier}}\}$ .</td><td>Sec. 3.3</td></tr><tr><td> $P \in \mathbb{R}^{p \times d}, T'(x)$ </td><td>Adaptation prompts (length  $p$ , dim  $d$ ); modified input  $T'(x) = P \oplus T(x)$ .</td><td>Sec. 3.3</td></tr><tr><td> $\delta \sim \mathcal{N}(0, \sigma^{2}I), \sigma$ </td><td>Gaussian noise for adversarial prompt training and its std parameter.</td><td>Sec. 3.3</td></tr><tr><td> $\tilde{x}, M_{H}, M_{P}, p^{H}, p^{P}$ </td><td>Masked sample and header/payload masking operators with rates  $p^{H}, p^{P}$ .</td><td>Sec. 3.3</td></tr><tr><td>CrossEntropy, KL( $\cdot \parallel \cdot$ )</td><td>Task loss and KL divergence for adversarial regularization.</td><td>Sec. 3.3</td></tr><tr><td> $\mathcal{L}_{\text {task}}, \mathcal{R}_{\text {adv}}, \lambda_{1}, \mathcal{L}_{\text {total}}$ </td><td>Task loss, adv. regularizer, its weight, and total objective.</td><td>Sec. 3.3</td></tr><tr><td>conf</td><td>Confidence score max( $\hat{y}$ ) for predicted distribution.</td><td>Alg. 1</td></tr><tr><td>IsTraining, MaxIters,  $\eta$ </td><td>Training flag, max iterations, and learning rate.</td><td>Alg. 1</td></tr><tr><td> $b, n, d, l, r, p$ </td><td>Batch size, token count, hidden size, transformer layers, LoRA rank, prompt length.</td><td>Sec. 3</td></tr><tr><td> $\alpha, \varepsilon$ </td><td>Efficiency constant for attention, FGSM perturbation strength.</td><td>Sec. 3</td></tr></table>

# 3. Methodology

The malicious encrypted traffic detection problem is formulated as a multi-class classification problem. Here, the final result is a probability distribution indicating the likelihood of malicious activity. We define the input set as $X = \{ x , \mathcal { T } , \mathrm { L L M } _ { \theta } , \theta _ { \mathrm { a d a p t } } , C \}$ , where $x , \mathcal { T } , \mathrm { L L M } _ { \theta } , \theta _ { \mathrm { a d a p t } } ,$ and C denote the raw traffic sample, domain-specific tokenizer, pretrained language model, adaptation parameters, and classification head, respectively. Our framework comprises three components, i.e., traffic embedding, domain-adapted pretrained LLM, and DATA. We illustrate our MET-LLM framework in Figure 2. The details are illustrated as follows. In addition, for clarity we collect the mathematical notations, shown in Table 1.

# 3.1. Traffic Embedding

To bridge the substantial representational gap between natural language and network traffic data, we develop a specialized tokenization mechanism that transforms heterogeneous network features into semantically rich input representations. This component mitigates the modality mismatch by implementing segment-specific encoding strategies optimized for the unique characteristics of network traffic. Our approach decomposes raw traffic samples x into two semantically distinct segments, $x $ $( x ^ { H } , x ^ { P } )$ , where $x ^ { H }$ denotes the header segment, containing metadata such as protocol identifiers, sequence numbers, and connection states, and $x ^ { P }$ signifies the payload segment, comprising hexadecimal-encoded content.

To enrich the input representation, we adopt a feature extraction pipeline that integrates domain knowledge with data-driven methods as follows,

$$
F (x) = \text { Extractor } (x), \tag {1}
$$

where Extractor(·) encompasses specialized parsers and heuristic functions derived from network protocol specifications and prior research [34, 36]. These extractors identify salient traffic attributes, such as flow-level statistics, protocol-specific fields, and temporal patterns, relevant to downstream security tasks.

With extracted features, we build a domain specific tokenization vocabulary tailored to network traffic. Conventional LLM tokenizers are ill-equipped to handle networkspecific elements such as IP addresses, port numbers, and hexadecimal sequences [37, 38]. Therefore, we train a Byte Pair Encoding (BPE) model [25] on a large-scale traffic corpus of over 10 million network flows. The resulting vocabulary is defined as $V _ { \mathrm { T r a f f i c } } ~ = ~ V _ { \mathrm { L L M } } ~ \cup ~ V _ { \mathrm { N e w } }$ , where $V _ { \mathrm { L L M } }$ represents the original LLM vocabulary, and

![](images/64fa1732181d3bff0525d51d98a313902e9b4b83761459febacba1fb31b64616.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Network Traffic: 'IP: 192.168.1.1 PORT:80 TCP.seg:22 8b25af'"] --> B["Standard vocabulary [ 'IP':'192'.'168'.'1'.'1' 'PORT':'80' 'TCP.seg':'22 8b25af' "]]
    A --> C["Traffic vocabulary [ 'IP:192.168.1.1'PORT:80' 'TCP.seg':'22 8b25af' "]]
    C --> D["General Language Tokens *standard words:'the', 'and', 'is' *Common number: '1', '2', '80' *Punctuation:.', ',','*'"]
    C --> E["V_LLM"]
    E --> F["Protocol Tokens *TCP.seg','UDP.pkt' *HTTP.req', 'HTTP.resp' *TLS.handshake'"]
    E --> G["V_New"]
    G --> H["Network Identifiers *IP:192.168.0.1', *PORT:80', 'PORT:443' *MAC:addr'"]
    G --> I["Hex Pattern *Hex:8b25', HEX:ff00'"]
```
</details>

Figure 3: The illustration of traffic vocabulary construction.

$V _ { \mathrm { N e w } }$ comprises newly learned tokens tailored to network constructs, including protocol-specific tokens, hexadecimal patterns, and common network identifiers. This extended vocabulary enables more efficient and semantically meaningful tokenization of traffic data, significantly reducing the sequence length compared to character-level encoding while preserving critical information. Figure 3 illustrates the construction of traffic vocabulary.

Next, distinct tokenization functions are applied to each segment as follows:

$$
\tau_ {H} \left(x ^ {H}\right) = \left[ t _ {H, 1}, t _ {H, 2}, \dots , t _ {H, m} \right], \tag {2}
$$

$$
\tau_ {P} (x ^ {P}) = [ t _ {P, 1}, t _ {P, 2}, \ldots , t _ {P, n} ].
$$

where $\tau _ { H }$ means the header tokenizer that preserves structured information as protocol fields, numerical values, and metadata. $\tau _ { P }$ is the payload tokenizer that efficiently encodes binary and hexadecimal content. This dualtokenization approach enables the model to process both human-readable headers and opaque encrypted payloads.

Finally, tokenized segments are concatenated with special delimiter tokens that provide structural guidance to the language model as follows,

$$
T (x) = [ \mathrm{CLS} ] \oplus \tau_ {H} (x ^ {H}) \oplus [ \mathrm{HEAD} ] \oplus \tau_ {P} (x ^ {P}) \oplus [ \mathrm{BODY} ], \tag {3}
$$

in which, the symbol ⊕ denotes sequence concatenation. In addition, [CLS], [HEAD], and [BODY] signify special tokens that mark different components of the traffic. This format enables the model to distinguish between header and payload information while maintaining their contextual relationships.

The tokenization approach is designed to outperform conventional text tokenizers in network traffic analysis. It optimizes sequence length reduction while preserving the semantic integrity essential for downstream analytical tasks. The segment-specific BPE tokenizer provides outof-vocabulary tokens common in network traffic data, addressing the limitations of standard NLP tokenizers when processing network data characterized by distinctive vocabulary patterns and structural heterogeneity.

# 3.2. Domain-Adapted Pretrained LLM

The second component of MET-LLM leverages a pretrained LLM adapted for the security domain. We utilize Deepseek [16] as the foundational model for its strong contextual understanding and adaptability to diverse domains. Deepseek employs a decoder-only transformer architecture with 7 billion parameters. It incorporates rotary positional embeddings, grouped-query attention mechanisms, and a 4,096-token context window. These specifications enable efficient processing of traffic sequences while capturing long-range dependencies for security analysis. Here, we pretrain DeepSeek on security-related corpora, which comprise security documentation and advisories, including Common Vulnerabilities and Exposures reports, security bulletins, technical documentation, and detailed network protocol specifications, particularly RFC documents that describe network protocols and their implementations.

Furthermore, the model is trained on diverse cyber threat intelligence reports, which provide an in-depth analysis of attack methodologies, tactics, techniques, and procedures employed by threat actors. The training data also includes security-focused code repositories and analytical tools related to network security, ensuring exposure to both knowledge and practices in the cybersecurity domain. This domain-specific pretraining equips the model with an understanding of security principles, network protocols, and attack patterns before engaging in traffic classification tasks.

Thus, the pretrained LLM serves as a powerful contextual encoder for tokenized traffic data. Given a tokenized traffic sample T (x) from Eq. (3), the model produces contextualized representations as follows:

$$
H = \operatorname{LLM} _ {\theta} (T (x)), \tag {4}
$$

where $H \in \mathbb { R } ^ { n \times d }$ denotes the matrix of contextualized token embeddings, n represents the sequence length, and d signifies the embedding dimension. Here, θ denotes the complete set of parameters of the pretrained language model operator $\operatorname { L L M } _ { \theta } .$ In our parameter-efficient finetuning setup, θ is kept frozen and only $\theta _ { \mathrm { a d a p t } }$ is updated (see Section 3.3). For our detection task, we extract the embedding corresponding to the [CLS] token and project it through a task-specific classification head as follows,

$$
y = \text { softmax } \left(W \cdot H _ {[ \mathrm{CLS} ]} + b\right), \tag {5}
$$

where $W \in \mathbb { R } ^ { c \times d }$ and $b \in \mathbb { R } ^ { c }$ denote learnable parameters, and c represents the number of classes.

# 3.3. Dynamic Adaptive Tuning Adaptor (DATA)

DATA addresses the need for rapid adaptation to evolving threats and operational environments. It implements a parameter-efficient fine-tuning strategy that enables continuous model updating without full retraining. Formally, DATA comprises a set of trainable parameter modules that interface with the frozen pretrained model as follows,

$$
\theta_ {\text { adapt }} = \{\theta_ {\text { prompt }}, \theta_ {\text { lora }}, \theta_ {\text { classifier }} \}, \tag {6}
$$

where $\theta _ { \mathrm { p r o m p t } }$ means the parameters of adaptation prompts, $\theta _ { \mathrm { L o R A } }$ denotes low-rank adaptation matrices, and θclassifier corresponds to the task-specific classification head. These parameters account for less than 0.1% of the pretrained model’s parameters. Therefore, efficient updates are available while preserving the base model’s abilities, which are particularly effective in dynamic environments requiring immediate adaptation. For instance, when encountering new attack patterns (e.g., modifications in command-andcontrol traffic) or protocol updates, DATA can efficiently adapt the model without compromising its performance on previously learned detection abilities.

One module of DATA is the adaptation prompt, which conditions the model on task-specific contexts. Let $P \in$ $\mathbb { R } ^ { p \times d }$ represent a set of learnable prompt embeddings, where p denotes the prompt length and d signifies the dimension. These prompts are appended to the input sequence, forming the modified sequence $T ^ { \prime } ( x ) = P \oplus T ( x )$ .

These adaptation prompts function as an in-context learning mechanism, guiding the model’s attention and output generation toward task-specific patterns. To enhance robustness against adversarial perturbations, we incorporate noise injection during training as follows,

$$
P ^ {\prime} = P + \delta , \quad \delta \sim \mathcal {N} (0, \sigma^ {2} I), \tag {7}
$$

where $\delta$ represents a perturbation sampled from a Gaussian distribution with a zero mean and an isotropic variance. This adversarial prompt training improves the model’s resilience against traffic obfuscation and evasion techniques in encrypted traffic.

To further improve the robustness against incomplete or corrupted traffic, DATA implements a dynamic masking strategy during fine-tuning. Given a traffic sample x and its corresponding segments, we apply stochastic masking,

$$
\tilde {x} = M (x) = \{M _ {H} (x ^ {H}), M _ {P} (x ^ {P}) \}, \tag {8}
$$

where $M _ { H } ( \cdot )$ and $M _ { P } ( \cdot )$ represent masking operations on the header and payload, respectively. These two operations randomly occlude portions of the input with predefined probabilities as follows,

$$
M _ {H} \left(x _ {i} ^ {H}\right) = \left\{ \begin{array}{l l} [ \text { MASK } ], & \text { with   probability } p ^ {H} \\ x _ {i} ^ {H}, & \text { otherwise } \end{array} \right. \tag {9}
$$

$$
M _ {P} \left(x _ {j} ^ {P}\right) = \left\{ \begin{array}{l l} [ \text { MASK } ], & \text { with   probability } p ^ {P} \\ x _ {j} ^ {P}, & \text { otherwise. } \end{array} \right. \tag {10}
$$

This dynamic masking procedure simulates real-world scenarios where traffic data may be incomplete due to packet loss, fragmentation, or sampling constraints. By training the model, DATA enhances its robustness.

The training objective of DATA integrates the taskspecific loss with other regularization terms as follows,

$$
\mathcal {L} _ {\text { total }} = \mathcal {L} _ {\text { task }} (\tilde {x}; \theta + \Delta \theta) + \lambda_ {1} \mathcal {R} _ {\text { adv }} (P ^ {\prime}), \tag {11}
$$

where $\mathcal { L } _ { \mathrm { t a s k } }$ represents the task-specific loss (e.g., crossentropy for classification), $\mathcal { R } _ { \mathrm { a d v } }$ denotes an adversarial regularization term, and λ1 controls the contribution of the regularization term. The adversarial regularization term is defined as follows,

$$
\mathcal {R} _ {\mathrm{adv}} (P ^ {\prime}) = \mathbb {E} _ {x, \delta} \left[ \mathrm{KL} \left(f _ {\theta} (T ^ {\prime} (x)) \parallel f _ {\theta} (T (x))\right) \right], \tag {12}
$$

where E denotes the model’s expectation operator, $f _ { \theta } ( \cdot )$ represents the model’s output distribution, and KL signifies the Kullback-Leibler divergence. This term promotes prediction consistency between original and perturbed inputs, enhancing robustness against prompt-based attacks.

Thus, DATA achieves rapid and parameter-efficient adaptation to evolving threats and robust detection performance under diverse traffic conditions, including partial data and adversarial perturbations. Our findings demonstrate that DATA-equipped models maintain high detection accuracy even against new attack variants not present in the initial training data. Notably, adaptation can be performed within minutes, significantly reducing update time compared to conventional full model retraining, which may take days or weeks. To be clear, the overall MET-LLM algorithm is outlined in Algorithm 1.

# 3.4. Complexity Analysis

We analyze and optimize the end-to-end per-batch time complexity. Let b denote the batch size, n the postembedding token count per sample, d the hidden size, l the number of transformer layers, r the LoRA rank, and p the prompt length. Traffic embedding (segmentation, feature extraction, and tokenization) requires a linear pass over tokens and thus costs O(bn).

For the decoder-only LLM encoder with l layers and a hidden size of d, the per-batch cost is $O ( b l ( n ^ { 2 } d + n d ^ { 2 } ) )$ , dominated by self-attention $O ( b l n ^ { 2 } d )$ when n is large. In practice, efficient attention kernels $( \mathrm { e . g . }$ , FlashAttention or block-sparse implementations) and mixed-precision execution reduce constant factors in this dominant term while preserving the same asymptotic order.

DATA trains only prompts and low-rank adapters; the number of trainable parameters is $O ( l d r + p )$ . The per-iteration compute matches a forward/backward pass through the (frozen) backbone, but with substantially smaller optimizer overhead than full fine-tuning due to the reduced parameter count.

Thus, the dominant per-batch training cost is $O ( b l ( n ^ { 2 } d +$ $n d ^ { 2 } ) )$ . With efficient attention kernels and implementation optimizations, the dominant attention term is effectively scaled by a constant factor α ≪ 1, so the practical runtime approaches $O ( b l ( \alpha n ^ { 2 } d + n d ^ { 2 } ) )$ .

# 4. Experiments

We present a comprehensive evaluation of MET-LLM’s performance across multiple datasets, benchmark methods, and analytical dimensions. The experimental datasets and preprocessing methods are outlined, followed by implementation details, metrics, and quantitative results.

Our evaluation is guided by three research questions. 1) How does MET-LLM perform compared to state-of-theart methods on diverse encrypted traffic datasets, and what factors contribute to its superior performance? 2) What is the individual impact of each core component (traffic embedding, domain-adapted LLM, and DATA) on overall

Algorithm 1 Iterative training and inference of our MET-LLM.

Input: Raw traffic sample x, domain-specific tokenizer T , domain-adapted LLM LLMθ, DATA parameters $\theta _ { \mathrm { a d a p t } } ,$ classification head C, mode flag IsTraining ∈ {True, False}, maximum iterations MaxIters, learning rate $\eta .$

Initialize: If training, initialize $\theta _ { \mathrm { a d a p t } } ,$ , keep θ frozen.

Output: Prediction ˆy and confidence score conf (or updated $\theta _ { \mathrm { a d a p t } }$ in training).

1: if IsTraining = True then
2:    for $t = 1, 2, \ldots, MaxIters$ do
3:    Split x into header $x^{H}$ and payload $x^{P}$ ; extract $F(x)$ with Eq. 1.
4:    Tokenize each part with Eq. 2 and join them into $T(x)$ per Eq. 3.
5:    Build adaptation prompts, add light Gaussian noise during training, and prepend them to the input.
6:    Mask $x^{H}$ and $x^{P}$ at the given rates and re-tokenize.
7:    Pass $T(x)$ through the frozen backbone, adapt via DATA, and obtain probabilities and confidence from C.
8:    Compute the total loss, update $\theta_{adapt}$ with step size $\eta$ , and stop once validation is met.
9:    end for
10:    return $\theta_{adapt}$ 11: else
12:    Split, tokenize, and assemble $T(x)$ following Eqs. 1–3; prepend adaptation prompts.
13:    Encode with LLM $_{\theta}$ , obtain the adapted representation through DATA, and compute class probabilities with C.
14:    Let $\hat{y}$ be the predicted distribution and conf its maximum component;
15:    return $\hat{y}$ , conf
16: end if

effectiveness, and how do different design choices influence the outcomes? 3) How effective is DATA in terms of parameter efficiency, rapid adaptation to novel threats, adversarial robustness, and dynamic masking strategies?

# 4.1. Datasets and Preprocessing

Datasets. To assess MET-LLM’s effectiveness across diverse encrypted traffic scenarios, we conducted extensive experiments on four benchmark datasets, each offering unique characteristics for evaluating specific aspects of encrypted traffic analysis. The details of these datasets are as follows. 1) ISCX Tor 2016 [39]. This dataset comprises 8,044 flow samples of anonymized traffic generated through the Tor network, including web browsing, email, chat, streaming, file transfers, and malicious activities. Its multi-layer encryption and traffic obfuscation techniques make it a challenging classification task. 2) ISCX VPN 2016 [40]. This dataset features 27,232 Virtual Private Network (VPN)-encrypted flow samples across 14 application classes. It includes both benign applications (web browsing, email, streaming) and potentially malicious patterns encapsulated within VPN protocols, representing enterprise security scenarios. 3) APP-53 2023 [41]. This dataset contains 168,450 flow samples from 53 contemporary applications utilizing modern encryption protocols (TLS 1.3, QUIC, and various proprietary protocols) collected from 2021 - 2023. It represents the complexity and evolution of application-layer encryption with diverse implementations and evasion techniques. 4) CSTNET 2023 [42]. This dataset consists of 93,675 flow samples acquired from real-world enterprise environments, comprising both benign traffic and actual malicious flows captured during security incidents. It spans multiple encryption protocols, network segments, and attack types, providing a realistic evaluation environment.

Preprocessing. For a consistent evaluation, datasets undergo a standard pipeline. Raw traffic captures are transformed into flow- and packet-level representations. Flows are defined by 5-tuple, i.e., source IP, destination IP, source port, destination port, and protocol. For each flow, statistical features are extracted, including temporal patterns, packet size distributions, and protocol-specific attributes. Each dataset is divided into training (70%), validation (15%), and testing (15%) sets using stratified sampling to maintain a consistent distribution.

# 4.2. Baselines

# 4.3. Implementation Details

We leverage Deepseek-R1-7B as the base LLM, selected for its extensive pretraining on 2.8 trillion tokens from security-specific corpora. The model employs a rotary positional embedding and supports a 4,096- token context window. Training is conducted on a server equipped with four NVIDIA A100 GPUs using mixedprecision (FP16) optimization. Gradient accumulation is used to simulate larger batch sizes under memory constraints. Hyperparameters are tuned with grid search, yielding the optimal settings: learning rate $\beta = 5 \times 1 0 ^ { - 5 }$ , batch size = 16, weight decay = 0.01, and gradient clipping = 1. For dynamic adaptation, we implemented prompt tuning with a prompt length of 512 tokens. LoRA is configured with rank r = 16 and scaling factor α = 32, providing a trade-off between adaptation capacity and computational efficiency.

# 4.4. Evaluation Metrics

Our proposed method is evaluated using three standard metrics. Precision is the ratio of true positives to the sum of true and false positives, signifying the accuracy of positive predictions. Recall is the ratio of true positives to the sum of true positives and false negatives, denoting the model’s ability to find all positive instances. F1 is the harmonic mean of precision and recall, providing a balanced assessment, particularly under class imbalance.

# 5. Experimental Results and Analysis

# 5.1. Main Results

Table 2 presents a comprehensive performance evaluation of MET-LLM against 14 established benchmark methods across four diverse datasets. The analysis reveals significant insights into the efficacy of different methodological approaches across various encryption protocols and network traffic environments.

<table><tr><td rowspan="2">METHOD</td><td colspan="3">ISCX Tor 2016</td><td colspan="3">ISCX VPN 2016</td><td colspan="3">APP-53 2023</td><td colspan="3">CSTNET 2023</td></tr><tr><td>P</td><td>R</td><td>F1</td><td>P</td><td>R</td><td>F1</td><td>P</td><td>R</td><td>F1</td><td>P</td><td>R</td><td>F1</td></tr><tr><td>AppScanner [27]</td><td>0.7254</td><td>0.6512</td><td>0.6124</td><td>0.7395</td><td>0.7125</td><td>0.7304</td><td>0.7035</td><td>0.6957</td><td>0.6980</td><td>0.6481</td><td>0.6420</td><td>0.6467</td></tr><tr><td>CUMUL [28]</td><td>0.5671</td><td>0.5731</td><td>0.5628</td><td>0.6322</td><td>0.6824</td><td>0.6570</td><td>0.5563</td><td>0.5467</td><td>0.5480</td><td>0.5373</td><td>0.5217</td><td>0.5274</td></tr><tr><td>BIND [30]</td><td>0.4569</td><td>0.4385</td><td>0.4469</td><td>0.5067</td><td>0.4975</td><td>0.5008</td><td>0.6566</td><td>0.6456</td><td>0.6502</td><td>0.7712</td><td>0.7689</td><td>0.7691</td></tr><tr><td>K-FP [29]</td><td>0.7035</td><td>0.6789</td><td>0.6951</td><td>0.6784</td><td>0.6967</td><td>0.6891</td><td>0.5660</td><td>0.5260</td><td>0.5295</td><td>0.4172</td><td>0.3981</td><td>0.4012</td></tr><tr><td>FlowPrint [32]</td><td>0.4201</td><td>0.3789</td><td>0.3901</td><td>0.7084</td><td>0.6608</td><td>0.6888</td><td>0.4890</td><td>0.5023</td><td>0.4950</td><td>0.2371</td><td>0.2270</td><td>0.2254</td></tr><tr><td>GraphDApp [36]</td><td>0.4789</td><td>0.4878</td><td>0.4781</td><td>0.6478</td><td>0.6488</td><td>0.6476</td><td>0.6860</td><td>0.6450</td><td>0.6550</td><td>0.6329</td><td>0.5965</td><td>0.6078</td></tr><tr><td>FS-Net [34]</td><td>0.6283</td><td>0.6274</td><td>0.5916</td><td>0.7693</td><td>0.7488</td><td>0.7507</td><td>0.8550</td><td>0.8349</td><td>0.8376</td><td>0.8291</td><td>0.8061</td><td>0.8195</td></tr><tr><td>DF [31]</td><td>0.6072</td><td>0.6123</td><td>0.6090</td><td>0.6296</td><td>0.6051</td><td>0.6139</td><td>0.7689</td><td>0.7523</td><td>0.7604</td><td>0.7729</td><td>0.7621</td><td>0.7682</td></tr><tr><td>TSCRNN [35]</td><td>0.9051</td><td>0.9178</td><td>0.9105</td><td>0.9346</td><td>0.9367</td><td>0.9349</td><td>0.7057</td><td>0.6890</td><td>0.6995</td><td>0.7529</td><td>0.7566</td><td>0.7558</td></tr><tr><td>Deeppacket [15]</td><td>0.7456</td><td>0.7469</td><td>0.7400</td><td>0.9467</td><td>0.9508</td><td>0.9503</td><td>0.5590</td><td>0.5489</td><td>0.5506</td><td>0.4013</td><td>0.2965</td><td>0.3890</td></tr><tr><td>PERT [20]</td><td>0.7480</td><td>0.4952</td><td>0.4874</td><td>0.8573</td><td>0.7394</td><td>0.7481</td><td>0.8458</td><td>0.8369</td><td>0.8403</td><td>0.8896</td><td>0.8721</td><td>0.8771</td></tr><tr><td>ET-BERT [18]</td><td>0.9186</td><td>0.9430</td><td>0.9368</td><td>0.9567</td><td>0.9420</td><td>0.9539</td><td>0.8540</td><td>0.8494</td><td>0.8506</td><td>0.9581</td><td>0.9478</td><td>0.9496</td></tr><tr><td>TrafficFormer [22]</td><td>0.9389</td><td>0.9421</td><td>0.9380</td><td>0.9589</td><td>0.9621</td><td>0.9580</td><td>0.7931</td><td>0.7544</td><td>0.7129</td><td>0.8484</td><td>0.8371</td><td>0.8338</td></tr><tr><td>NetMamba [21]</td><td>0.9986</td><td>0.9986</td><td>0.9986</td><td>0.9805</td><td>0.9808</td><td>0.9806</td><td>0.8904</td><td>0.9094</td><td>0.8999</td><td>0.9301</td><td>0.9327</td><td>0.9305</td></tr><tr><td>Our MET-LLM</td><td>0.9790</td><td>0.9771</td><td>0.9781</td><td>0.9850</td><td>0.9940</td><td>0.9980</td><td>0.9425</td><td>0.9415</td><td>0.9315</td><td>0.9618</td><td>0.9602</td><td>0.9610</td></tr></table>

On ISCX Tor 2016 dataset, NetMamba achieved the highest overall performance $( \mathrm { F 1 } = 0 . 9 9 8 6 )$ , followed by MET-LLM $( \mathrm { F 1 } =  { 0 . 9 7 8 1 } )$ , significantly outperforming both traditional and most deep learning-based models. Compared to prior transformer-based models such as ET-BERT $( \mathrm { F 1 } = 0 . 9 3 6 8 )$ and TrafficFormer $( \mathrm { F 1 } = 0 . 9 3 8 0 )$ , MET-LLM’s enhanced performance highlights the effectiveness of its domain-specific tokenization and dynamic adaptation mechanisms when handling Tor’s complex multi-layered encryption. MET-LLM’s balanced precision $( \mathrm { P } = 0 . 9 7 9 0 )$ and recall $( \mathrm { R } = 0 . 9 7 7 1 )$ indicate robust detection capability with sophisticated obfuscation techniques. This finding is essential for minimizing false positives and false negatives in security applications.

On ISCX VPN 2016 dataset, MET-LLM yields the best performance $( \mathrm { F 1 } = 0 . 9 9 8 0 )$ , surpassing even recent architectures such as NetMamba $( \mathrm { F 1 } = 0 . 9 8 0 6 )$ and Traffic-Former $( \mathrm { F 1 } = 0 . 9 5 8 0 )$ . Given the nested encryption in VPN traffic, where multiple protocols are encapsulated within encrypted tunnels, this result underscores MET-LLM’s capacity for deep contextual modeling. In contrast, traditional fingerprinting methods exhibited lower efficacy, with CUMUL $( \mathrm { F 1 } = 0 . 6 5 7 0 )$ and K-FP (F1 = 0.6891) struggling to identify meaningful patterns within tunneled traffic. The performance degradation in nontransformer architectures shows the importance of contextual understanding when analyzing encrypted VPN traffic. MET-LLM’s high recall $( \mathbf { R } = 0 . 9 9 4 0 )$ further demonstrates its ability to identify relevant instances of malicious traffic, a valuable feature in security environments for reducing undetected threats in operational settings.

On APP-53 2023 dataset, the effectiveness of MET-LLM is highlighted on modern application protocols utilizing advanced encryption standards. MET-LLM achieves the highest F1 score of 0.9315, outperforming both NetMamba $( \mathrm { F 1 } = 0 . 8 9 9 9 )$ and TrafficFormer $( \mathrm { F } 1 =$ 0.7129). This substantial gap between MET-LLM and TrafficFormer suggests that TrafficFormer’s hierarchical attention mechanisms may struggle with obfuscation and protocol-level encryption prevalent in contemporary application protocols. Classification error analysis indicates that TrafficFormer faces the challenge of generalizing to custom encryption schemes outside standard TLS implementations, whereas MET-LLM’s domain-adapted pretraining supports broader protocol coverage. MET-LLM’s consistent precision-recall balance $( \mathrm { P } = 0 . 9 4 2 5 .$ , R $= 0 . 9 4 1 5 )$ reflects robust generalization across heterogeneous application traffic patterns, a key requirement for deployment in dynamic, evolving network environments.

On CSTNET 2023 dataset, captured from real-world production networks, MET-LLM outperforms other methods, achieving an $\mathrm { F 1 } = 0 . 9 6 1 0$ compared to NetMamba $( \mathrm { F 1 } = 0 . 9 3 0 5 )$ and TrafficFormer $( \mathrm { F 1 } = 0 . 8 3 3 8 )$ . Its performance is particularly pronounced in detecting complex attack vectors, such as encrypted command-and-control channels and obfuscated data exfiltration attempts. The results reveal a consistent trend: methods incorporating domain-specific knowledge outperform generic approaches, regardless of architectural complexity. This observation highlights the value of MET-LLM’s contextual understanding of network protocols and threat patterns, a core design principle for real-world deployment. While approaches such as BIND achieved relatively high precision $( \mathrm { P } = 0 . 7 7 1 2 )$ , their lower recall $( \mathrm { R } = 0 . 7 6 8 9 )$ indicates reduced effectiveness in identifying diverse or subtle attack patterns. In contrast, MET-LLM maintains a better precision-recall balance, ensuring comprehensive and reliable threat detection.

The evaluation on cross-dataset highlights the robustness and generalization capabilities of various methods. Traditional fingerprinting approaches, such as FlowPrint, demonstrate variability (F1 $\mathrm { s c o r e s } \ = \ 0 . 2 2 5 4 \ - \ 0 . 6 8 8 8 )$ across datasets, indicating sensitivity to dataset-specific characteristics and limited generalization across diverse network environments. Deep learning methods exhibit improved consistency but still display dataset-specific performance. For instance, TSCRNN performs well on the ISCX VPN 2016 dataset (F1 = 0.9349) but underperforms on APP-53 2023 (F1 = 0.6995), indicating specialization on certain traffic patterns. Similarly, NetMamba excels on ISCX Tor 2016 $( \mathrm { F 1 } = 0 . 9 9 8 6 )$ ), but shows fluctuations across datasets, suggesting it may be better suited for specific traffic patterns. In contrast, MET-LLM consistently performs well across all evaluation environments $( \mathrm { F 1 } = 0 . 9 3 1 5 \cdot 0 . 9 9 8 0 )$ , reflecting robust generalization across traffic types and encryption protocols. This is an important requirement for deployment in real-world and heterogeneous network environments.

Statistical analysis confirms that MET-LLM’s performance gains are significant compared to both traditional fingerprinting and most deep learning approaches. While NetMamba slightly outperforms MET-LLM on ISCX Tor 2016, MET-LLM consistently ranks at top performers across all datasets. The observed performance differential between MET-LLM and the most competitive baseline methods (NetMamba and ET-BERT) is not attributable to random experimental variation, indicating that MET-LLM offers a meaningful advancement in encrypted traffic detection rather than marginal improvements.

The consistent performance of MET-LLM stems from its synergetic architectural factors, which address the challenges of encrypted traffic analysis. Its domainspecific tokenization bridges the gap between NLP and network traffic, enabling structured headers and encrypted payloads to be processed within a unified framework. The pretrained language model, trained on security-focused corpora, captures deep contextual relationships often missed by traditional feature-based approaches. Additionally, DATA enables efficient parameter updates in response to domain-specific patterns, allowing the model to adapt to emerging threats without requiring complete retraining. These architectural components form a unified framework in which each element reinforces the others, resulting in robust and adaptable performance across diverse encrypted traffic environments.

The analysis by traffic category further shows the strength of MET-LLM. For interactive traffic, such as remote access and real-time communication, MET-LLM outperforms previous methods. This suggests that its contextual modeling is well suited to bidirectional exchanges and temporal dependencies. Similarly, for traffic employing complex encryption protocols such as perfect forward secrecy and ephemeral key exchanges, MET-LLM keeps robust performance, while other methods decrease. This resilience underscores the effectiveness of its domainadapted pretraining and specialized tokenization in handling advanced cryptographic protocols.

# 5.2. Ablation Study

To validate the contribution of each component of MET-LLM, we conducted an ablation study on the CST-NET 2023 dataset. The results are reported in Table 3. Traffic Tokenization. Removing the custom tokenization module leads to the most significant performance drop, with the F1 score falling from 0.9610 to 0.8957 (6.53% reduction). This substantial impact highlights the inadequacy of conventional text tokenizers for encrypted network traffic data. Further analysis reveals a 12.4% rise in false positives for obfuscated malicious traffic resembling benign patterns. These findings validate our hypothesis that appropriate modal adaptation is a prerequisite for effectively applying LLMs to encrypted traffic analysis.

Domain-Adapted LLM. Replacing the security specialized Deepseek model with a general-purpose LLM of equivalent size (without security-specific pretraining) reduced the F1 score by 4.27%. This decline is most pronounced in detecting sophisticated attacks leveraging protocol-specific evasion techniques, where the model lacked the necessary background knowledge. This result underscores the critical role of domain-specific pretraining in developing foundational security applications to identify subtle anomalies in encrypted traffic.

Table 3: Ablation study on our proposed MET-LLM. 

<table><tr><td>Configuration</td><td>P</td><td>R</td><td>F1</td></tr><tr><td>MET-LLM w/o traffic tokenizer</td><td>0.9127</td><td>0.8794</td><td>0.8957</td></tr><tr><td>MET-LLM w/o domain-adapted LLM</td><td>0.9302</td><td>0.9068</td><td>0.9183</td></tr><tr><td>MET-LLM w/o DATA mechanism</td><td>0.9527</td><td>0.9297</td><td>0.9410</td></tr><tr><td>MET-LLM w/o adversarial training</td><td>0.9578</td><td>0.9429</td><td>0.9502</td></tr><tr><td>MET-LLM w/o dynamic masking</td><td>0.9542</td><td>0.9394</td><td>0.9467</td></tr><tr><td>MET-LLM</td><td>0.9618</td><td>0.9602</td><td>0.9610</td></tr></table>

DATA. The removal of our DATA component and applying standard fine-tuning approaches decease F1 score by 2.00 percentage points. While the impact on static accuracy is moderate, the loss of adaptation efficiency is significant. Without DATA, the model requires 5.8× more trainable parameters and 4.3× longer training time to achieve comparable results. Additional adaptation experiments on emerging threats confirm that DATA-equipped models require 94% fewer computational resources while maintaining performance parity.

To further assess individual contributions within the DATA module, we conduct targeted ablations on adversarial training and dynamic masking. Removing adversarial training reduces the F1 score by 1.08 percentage points, primarily impacting the detection of adversarially crafted traffic. FUrthermore, removing dynamic masking reduces the F1 score by 1.43 percentage points, with the largest impact observed on incomplete or fragmented traffic flows. These findings affirm the complementary role of these modules in enhancing model robustness.

Our analysis reveals strong interaction effects among these components. Joint removal of multiple modules exceeds the sum of individual ablations, indicating synergistic relationships between the specialized tokenization, domain adaptation, and tuning mechanisms. For instance, removing both specialized tokenization and adversarial training decreases the F1 score by 9.17 percentage points, exceeding the combined individual reductions of 7.61 percentage points. This nonlinear degradation highlights that MET-LLM’s components function as an integrated system rather than as isolated modules.

# 5.3. Discussion

Traffic Embedding. To evaluate the effectiveness of our specialized traffic embedding approach, we conduct comparative experiments using various tokenization strategies on CSTNET 2023 dataset. We compare our domain-specific traffic tokenization against standard tokenization techniques commonly used in NLP. Table 4 presents the performance comparison across four configurations: 1) Standard BPE tokenization trained on general text corpora; 2) character-level tokenization treating network data as raw character sequences; 3) hexadecimalspecific tokenization focusing solely on payload representations; and 4) our proposed traffic embedding with domain-specific vocabulary extension.

The results demonstrate that our approach yields optimal performance (F1 = 0.9610) with minimal sequence length (1,247 tokens). In contrast, hexadecimal-only tokenization generates an $\mathrm { F } 1 = 0 . 9 0 2 2$ but lacks comprehensive header representation capabilities, the standard BPE tokenization produces $\mathrm { F 1 } = \mathrm { 0 } . 8 8 3 9$ (representing a 7.71 percentage point reduction compared to our approach), hindered by inadequate handling of network-specific constructs, including IP addresses, port numbers, and protocol identifiers; character-level tokenization yields the lowest $\mathrm { F 1 } = 0 . 8 5 9 6$ , with excessive sequence lengths (4,192 tokens), failing to preserve semantic structure.

<table><tr><td>Tokenization Method</td><td>P</td><td>R</td><td>F1</td><td>Length</td></tr><tr><td>Standard BPE</td><td>0.8924</td><td>0.8756</td><td>0.8839</td><td>2,847</td></tr><tr><td>Character-level</td><td>0.8673</td><td>0.8521</td><td>0.8596</td><td>4,192</td></tr><tr><td>Hexadecimal-only</td><td>0.9156</td><td>0.8892</td><td>0.9022</td><td>1,923</td></tr><tr><td>Our Traffic Embedding</td><td>0.9618</td><td>0.9602</td><td>0.9610</td><td>1,247</td></tr></table>

![](images/64c0b9e89c5461d3bca517b21b55ba7324791fc34a80410259b4a351e7ad635c.jpg)

<details>
<summary>bar</summary>

| Model Configuration        | F1 Score |
| -------------------------- | -------- |
| Full MET-LLM               | 0.961    |
| Without Pre-training       | 0.560    |
| Without Domain Adaptation  | 0.790    |
</details>

Figure 4: Impact of pre-trained knowledge vs. domain-specific adaptation components on detection performance.

These findings confirm that a domain-specific vocabulary to capture network constructs, excelling in representing protocol patterns, IP ranges, and encrypted payload sequences, is essential for both efficiency and superior classification performance when processing extended traffic flows within computational constraints.

Pre-trained vs. Domain Knowledge. To assess the roles of individual factors contributing to MET-LLM’s superior performance, we conduct experiments isolating the contributions of pre-trained knowledge versus domainspecific adaptation on the CSTNET 2023 dataset. Figure 4 shows the results of removing each component. Removing pre-trained knowledge by randomly initializing Deepseek’s weights and training from scratch on encryption traffic datasets dramatically decreases the performance across all datasets (average F1 score reduction of 42.3%). This confirms that LLMs pre-trained on text corpora effectively transfer pattern recognition capabilities to network traffic analysis, enabling the model to identify complex sequential patterns and contextual relationships. This capacity to detect sophisticated obfuscation techniques in encrypted traffic is a key advantage.

Conversely, preserving pre-trained knowledge while removing domain adaptation components (e.g., traffic tokenization and domain-specific fine-tuning) moderately decreases performance by an average of 17.8% across datasets. This finding indicates that while pre-trained knowledge provides a crucial foundation, domain adaptation remains essential for optimal performance in specialized tasks such as encrypted traffic analysis.

LLMs Architecture. We evaluate our MET-LLM’s framework across different foundation models to assess architecture-specific performance characteristics. In addition to our primary Deepseek implementation, we integrate three additional architectures: Llama-2 (7B), Mistral (7B), and OPT (6.7B). Table 5 presents their detection performance on the CSTNET 2023 dataset. All architectures achieve strong performance, with F1 scores exceeding 0.94, demonstrating our framework’s robustness across model variations. Deepseek delivers the highest score $( \mathrm { F } 1 = 0 . 9 6 1 0 )$ . This is likely due to its rotary positional embeddings and security-focused pretraining. Mistral ranked second $( \mathrm { F 1 } = 0 . 9 5 7 9 )$ , with its sliding-window attention mechanism, particularly effective for long traffic sequences, despite reduced parameter counts than other models in some layers. The consistent performance across architectures confirms that MET-LLM’s effectiveness is driven by its components rather than any single model architecture, affirming its transferability.

<table><tr><td>LLM</td><td>Precision</td><td>Recall</td><td>F1 Score</td></tr><tr><td>Deepseek (7B) [16]</td><td>0.9618</td><td>0.9602</td><td>0.9610</td></tr><tr><td>Llama-2 (7B) [17]</td><td>0.9583</td><td>0.9535</td><td>0.9559</td></tr><tr><td>Mistral (7B) [43]</td><td>0.9596</td><td>0.9562</td><td>0.9579</td></tr><tr><td>OPT (6.7B) [44]</td><td>0.9427</td><td>0.9385</td><td>0.9406</td></tr></table>

![](images/d02b3b74cf6927e41bea59c608438963a42f3021da3edb5068c78eac63334ac7.jpg)

<details>
<summary>bar</summary>

| Method          | Parameter Ratio |
| --------------- | --------------- |
| DATA            | 0.0009          |
| Full_Finetune   | 1.0000          |
| Adapter         | 0.0091          |
| Prefix_Tuning   | 0.0045          |
</details>

Figure 5: Parameter efficiency comparison of adaptation methods.

# 5.4. DATA Adaptor Evaluation

DATA in MET-LLM enables rapid and parameterefficient adaptation to emerging threats. We validate its effectiveness through four experiments on CSTNET2023 dataset. Figure 5 presents a parameter efficiency comparison across four fine-tuning methodologies. DATA achieves exceptional efficiency, adjusting only 0.0009% of model parameters, 10.11× and 5× fewer than Adapterbased methods (0.0091%) and Prefix Tuning (0.0045%), while maintaining competitive performance and orders of magnitude below full fine-tuning (100% baseline).

DATA utilizes 0.0014% of base model parameters, with 50,000 dynamic prompt embeddings, 30,000 lowrank adaptation matrices, and 20,000 specialized classifier heads, while preserving 99.9% of full fine-tuning performance. This targeted adaptation strategy concentrates updates on security-critical representations while preserving the underlying model architecture. Since the parameter count remains constant as the backbone grows, DATA scales efficiently to larger models and is well-suited for large-scale deployments. We assess DATA’s ability to rapidly adapt to emerging threats under strict time constraints by simulating the emergence of novel commandand-control communication protocols, representing zeroday attack vectors. Following initial training on established threat categories, we introduce new threat types with limited sample sizes of 100 - 1,000 instances and limited adaptation time to 10 minutes to reflect real-world operational demands.

![](images/1361437c5f7010b40457956269deca0a113743ed37e41f9a7f28acd6a9226203.jpg)

<details>
<summary>bar</summary>

| Sample Size | DATA Adaptation (seconds) | Full Retraining (seconds) |
| :--- | :--- | :--- |
| 100 | 30 | 2500 |
| 500 | 60 | 2400 |
| 1000 | 90 | 2700 |
| 2000 | 120 | 2900 |
</details>

Figure 6: Rapid adaptation performance with varying sample sizes.

![](images/58d9fe19044be37f71b0ce6d360fde69d014c78b41e403fac20c786e9df6048f.jpg)

<details>
<summary>line</summary>

| Perturbation Strength (ε) | Robustness Ratio |
| ------------------------- | ---------------- |
| 0.00                      | 1.0              |
| 0.05                      | 0.9              |
| 0.10                      | 0.8              |
| 0.15                      | 0.7              |
| 0.20                      | 0.6              |
| 0.30                      | 0.5              |
</details>

Figure 7: Adversarial robustness under different attack strengths.

Figure 6 demonstrates DATA’s substantial temporal advantages over traditional full retraining approaches across varying data volumes. Depending on the sample size, DATA completes adaptation in 20 120 seconds, while full retraining requires 3,000 - 6,000 seconds for equivalent performance levels. With just 100 new samples, DATA attains 94.2% detection accuracy within 20 sec- ˜ onds for novel threats, representing a 150× acceleration compared to conventional retraining methodologies. This rapid adaptation capability stems from DATA’s modular architecture, where dynamic prompt embeddings efficiently encode new threat characteristics, LoRA matrices adjust feature representations, and the specialized classifier adapts decision boundaries. Together, these components deliver near real-time threat response essential for maintaining security effectiveness against rapidly evolving attack vectors.

Furthermore, we conduct comprehensive adversarial robustness experiments to evaluate DATA’s resilience against sophisticated evasion techniques commonly used in real-world attack scenarios. The experiments employ the Fast Gradient Signed Method (FGSM) [45] with perturbation strengths of $\varepsilon = 0 . 0 1 – 0 . 2$ . In addition, we evaluate DATA’s performance against traffic obfuscation techniques, including protocol hopping, payload encryption, and time modulation, designed to simulate the evasion strategies of advanced threat actors.

Robustness Improvement by Dynamic Masking Strategies   
![](images/7454090bb839d53c711d240b9803a6665f5bed9edefdd08bd8c7ae2d86ee638a.jpg)

<details>
<summary>line</summary>

| Packet Loss Rate | Adaptive Masking | Structured Masking | Random Masking | No Masking Baseline |
| ---------------- | ---------------- | ------------------ | -------------- | ------------------- |
| 0.05             | 0.94             | 0.93               | 0.91           | 0.88                |
| 0.10             | 0.94             | 0.92               | 0.89           | 0.83                |
| 0.15             | 0.93             | 0.90               | 0.87           | 0.78                |
| 0.20             | 0.92             | 0.89               | 0.85           | -                   |
| 0.25             | 0.92             | 0.87               | 0.83           | -                   |
| 0.30             | 0.92             | 0.86               | 0.81           | -                   |
</details>

Figure 8: Impact of dynamic masking on robustness improvement.

Figure 7 demonstrates DATA’s robustness characteristics across varying perturbation strengths. DATA preserves 92% of its original performance at moderate perturbation levels $( \varepsilon = 0 . 0 5 )$ and retains 82% effectiveness under stronger adversarial conditions $( \varepsilon = 0 . 1 )$ . Even under severe adversarial perturbations $( \varepsilon = 0 . 2 )$ , DATA sustains 60% of baseline performance, outperforming conventional approaches that typically suffer drastic degradation. This resilience derives from DATA’s dynamic masking and adversarial training mechanisms, which foster stable representations resilient to sophisticated obfuscation attempts and adversarial perturbations.

To assess the impact of dynamic masking on model robustness, we simulate information loss scenarios using packet loss rates of 5% - 30%. Three masking strategies, including random, structured, and adaptive, are tested with header and payload masking probabilities set to $p _ { H } \in \{ 0 . 1 , 0 . 2 , 0 . 3 \}$ and $p _ { P } \in \{ 0 . 1 , 0 . 1 5 , 0 . 2 \}$ , respectively. These configurations reflect realistic network conditions, where partial data loss or corruption can occur.

As shown in Figure 8, adaptive masking consistently outperforms both random and structured approaches across all packet loss rates, maintaining an F1 score above 0.92 even at the highest loss levels. Structured masking provides moderate robustness, while random masking exhibits a more pronounced performance decline as loss increases. All masking strategies significantly surpass the no-masking baseline, which degrades rapidly with increasing data loss. These findings confirm that dynamic, context-aware masking strategies, particularly adaptive masking, substantially strengthen the model’s resilience to incomplete or corrupted input data in adverse network environments.

# 6. Limitations

From a systems perspective, the current implementation requires approximately 14 GB of GPU memory and a long context window. Single-GPU throughput is about 2,500 flows per second, which may fall short of strict line-rate detection on very high-speed links. Meeting tighter latency and throughput budgets typically requires additional engineering, including model distillation and quantization, efficient attention kernels, streaming/batching pipelines, and distributed inference designs tailored to deployment constraints.

In addition, regarding generalization and robustness, our experiments involve a subset of protocols and operating environments. The performance may degrade under strong obfuscation, adversarial perturbations, or substantial distribution shift (e.g., unseen protocol stacks or evolving encryption behaviors.

# 7. Conclusion and Future Work

This study proposes MET-LLM, a unified framework for encrypted-traffic detection that merges domainspecific tokenization, pretrained LLM, and DATA components. Our approach bridges the representational gap between NLP and network traffic while enabling powerful contextual understanding. Evaluations across multiple benchmark datasets demonstrate that MET-LLM significantly outperforms state-of-the-art methods, yielding F1 scores exceeding 0.96 across diverse traffic scenarios. Ablation studies confirm that each component contributes substantially to overall accuracy.

In the future, we will explore a multimodal stack, such as bytes, headers, timing, DNS/HTTP logs, TLS, and communication graphs with modality-aware tokenization and lightweight fusion (e.g., Mixture of Experts) that handles corrupted inputs. In addition, for low-sample regimes, we will consider how to synthesize traffic using conditional token generator, such as conditioned on protocol, threat type, header constraints, and flow statistics.

# Acknowledgment

This work was supported in part by the National Key Research and Development Program of China under Grant 2023YFC3305902, in part by the National Natural Science Foundation of China No. 62076032, in part by the China Computer Federation of Zhipu Foundation No. CCF-Zhipu202407, and in part by BUPT Kunpeng & Ascend Center of Cultivation.

# References

[1] Klint Finley. Half the web is now encrypted. that makes everyone safer. Wired, 2019. Accessed: 2024-02-10.   
[2] Google. Https encryption on the web – google transparency report. Google Transparency Report, 2023. Accessed: 2024-02-15.   
[3] Blake Anderson and David McGrew. Tls beyond the browser: Combining end host and network data to understand application behavior. In Proceedings of the 2019 ACM Internet Measurement Conference (IMC ’19), pages 379–392. Association for Computing Machinery, 2019.   
[4] Justine Sherry, Chang Lan, Raluca A. Popa, and Sylvia Ratnasamy. Blindbox: Deep packet inspection over encrypted traffic. In Proceedings of the 2015 ACM Conference on Special Interest Group on Data Communication (SIGCOMM ’15), pages 213–226. Association for Computing Machinery, 2015.   
[5] Robin Sommer and Vern Paxson. Outside the closed world: On using machine learning for network intrusion detection. In 2010 IEEE Symposium on Security and Privacy, pages 305–316. IEEE, 2010.   
[6] T. Velan, M. Cermak, P. Celeda, and M. Drasar. A survey of methods for encrypted traffic classification and analysis. International Journal of Network Management, 25(5):355–374, 2015.   
[7] F. Fusco and L. Deri. High-speed network traffic analysis with commodity multi-core systems. ACM SIGCOMM Computer Communication Review, 40(1):42–47, Jan 2010.   
[8] SM Nazmuz Sakib. Cyber threat intelligence. 2022.

[9] Jiwon Yang and Hyuk Lim. Deep learning approach for detecting malicious activities over encrypted secure channels. IEEE Access, 9:39229–39244, 2021.   
[10] Meng Shen, Ke Ye, Xingtong Liu, Liehuang Zhu, Jiawen Kang, Shui Yu, Qi Li, and Ke Xu. Machine learning-powered encrypted network traffic analysis: A comprehensive survey. IEEE Communications Surveys & Tutorials, 25(1):791–824, 2022.   
[11] Paul Maxwell, Elie Alhajjar, and Nathaniel D Bastian. Intelligent feature engineering for cybersecurity. In 2019 IEEE International Conference on Big Data (Big Data), pages 5005–5011. IEEE, 2019.   
[12] Giuseppe Aceto, Domenico Ciuonzo, Antonio Montieri, and Antonio Pescapé. Mobile encrypted traffic classification using deep learning: Experimental evaluation, lessons learned, and challenges. IEEE transactions on network and service management, 16(2):445–458, 2019.   
[13] Mauro Conti, Luigi Vincenzo Mancini, Riccardo Spolaor, and Nino Vincenzo Verde. Analyzing android encrypted network traffic to identify user actions. IEEE Transactions on Information Forensics and Security, 11(1):114–125, 2015.   
[14] Zhangyang Wang, Shiyu Chang, Jiayu Zhou, Meng Wang, and Thomas S Huang. Learning a task-specific deep architecture for clustering. In Proceedings of the 2016 SIAM International Conference on Data Mining, pages 369–377. SIAM, 2016.   
[15] Mohammad Lotfollahi, Mahdi Jafari Siavoshani, Ramin Shirali Hossein Zade, and Mohammdsadegh Saberian. Deep packet: A novel approach for encrypted traffic classification using deep learning. Soft Computing, 24(3):1999–2012, 2020.   
[16] Xiao Bi, Deli Chen, Guanting Chen, Shanhuang Chen, Damai Dai, Chengqi Deng, Honghui Ding, Kai Dong, Qiushi Du, Zhe Fu, et al. Deepseek llm: Scaling open-source language models with longtermism. arXiv preprint arXiv:2401.02954, 2024.   
[17] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. arXiv preprint arXiv:2307.09288, 2023.   
[18] Xinjie Lin, Gang Xiong, Gaopeng Gou, Zhen Li, Junzheng Shi, and Jing Yu. Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification. In Proceedings of the ACM Web Conference 2022, pages 633–642, 2022.   
[19] Ruijie Zhao, Mingwei Zhan, Xianwen Deng, Yanhao Wang, Yijun Wang, Guan Gui, and Zhi Xue. Yet another traffic classifier: A masked autoencoder based traffic transformer with multi-level flow representation. In Proceedings of the AAAI Conference on Artificial Intelligence, number 4, pages 5420–5427, 2023.   
[20] Hong Ye He, Zhi Guo Yang, and Xiang Ning Chen. Pert: Payload encoding representation from transformer for encrypted traffic classification. In 2020 ITU Kaleidoscope: Industry-Driven Digital Transformation (ITU K), pages 1–8. IEEE, 2020.   
[21] Tongze Wang, Xiaohui Xie, Wenduo Wang, Chuyi Wang, Youjian Zhao, and Yong Cui. Netmamba: Efficient network traffic classification via pre-training unidirectional mamba. In 2024 IEEE 32nd International Conference on Network Protocols (ICNP), pages 1– 11. IEEE, 2024.   
[22] Guangmeng Zhou, Xiongwen Guo, Zhuotao Liu, Tong Li, Qi Li, and Ke Xu. Trafficformer: an efficient pre-trained model for traffic data. In 2025 IEEE Symposium on Security and Privacy (SP), pages 102–102. IEEE Computer Society, 2024.   
[23] Chang Liu, Xiaohui Xie, Xinggong Zhang, and Yong Cui. Large language models for networking: Workflow, advances and challenges. IEEE Network, 2024.   
[24] Neil Houlsby, Andrei Giurgiu, Stanislaw Jastrzebski, Bruna Morrone, Quentin De Laroussilhe, Andrea Gesmundo, Mona Attariyan, and Sylvain Gelly. Parameter-efficient transfer learning for nlp. In International conference on machine learning, pages 2790–2799. PMLR, 2019.   
[25] Rico Sennrich, Barry Haddow, and Alexandra Birch. Neural machine translation of rare words with subword units. In Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 1715–1725, 2016.   
[26] Andrew W Moore and Denis Zuev. Internet traffic classification using bayesian analysis techniques. In Proceedings of the 2005 ACM SIGMETRICS international conference on Measurement and modeling of computer systems, pages 50–60, 2005.   
[27] Vincent F Taylor, Riccardo Spolaor, Mauro Conti, and Ivan Martinovic. Appscanner: Automatic fingerprinting of smartphone apps from encrypted network traffic. In 2016 IEEE European Sympo-

sium on Security and Privacy (EuroS&P), pages 439–454. IEEE Computer Society, 2016.   
[28] Andriy Panchenko, Fabian Lanze, Andreas Zinnen, Martin Henze, Jan Pennekamp, Thomas Engel, and Klaus Wehrle. Website fingerprinting at internet scale. In Proceedings of the 23rd Internet Society (ISOC) Network and Distributed System Security Symposium (NDSS 2016), San Diego, USA, February 2016. Internet Society, 2016.   
[29] Jamie Hayes and George Danezis. k-fingerprinting: A robust scalable website fingerprinting technique. In 25th USENIX Security Symposium (USENIX Security 16), pages 1187–1203, 2016.   
[30] Khaled Al-Naami, Swarup Chandra, Ahmad Mustafa, Latifur Khan, Zhiqiang Lin, Kevin Hamlen, and Bhavani Thuraisingham. Adaptive encrypted traffic fingerprinting with bi-directional dependence. In Proceedings of the 32nd Annual Conference on Computer Security Applications, pages 177–188, 2016.   
[31] Payap Sirinam, Mohsen Imani, Marc Juarez, and Matthew Wright. Deep fingerprinting: Undermining website fingerprinting defenses with deep learning. In Proceedings of the 2018 ACM SIGSAC conference on computer and communications security, pages 1928– 1943, 2018.   
[32] Thijs Van Ede, Riccardo Bortolameotti, Andrea Continella, Jingjing Ren, Daniel J Dubois, Martina Lindorfer, David Choffnes, Maarten Van Steen, and Andreas Peter. Flowprint: Semisupervised mobile-app fingerprinting on encrypted network traffic. In Network and distributed system security symposium (NDSS), volume 27, 2020.   
[33] Wei Wang, Ming Zhu, Jinlin Wang, Xuewen Zeng, and Zhongzhen Yang. End-to-end encrypted traffic classification with onedimensional convolution neural networks. In 2017 IEEE international conference on intelligence and security informatics (ISI), pages 43–48. IEEE, 2017.   
[34] Chang Liu, Longtao He, Gang Xiong, Zigang Cao, and Zhen Li. Fs-net: A flow sequence network for encrypted traffic classification. In IEEE INFOCOM 2019-IEEE Conference On Computer Communications, pages 1171–1179. IEEE, 2019.   
[35] Kunda Lin, Xiaolong Xu, and Honghao Gao. Tscrnn: A novel classification scheme of encrypted traffic based on flow spatiotemporal features for efficient management of iiot. Computer Networks, 190:107974, 2021.   
[36] Meng Shen, Jinpeng Zhang, Liehuang Zhu, Ke Xu, and Xiaojiang Du. Accurate decentralized application identification via encrypted traffic analysis using graph neural networks. IEEE Transactions on Information Forensics and Security, 16:2367–2380, 2021.   
[37] H. Song, M. S. Kim, and J. W. Hong. Nfv and sdn-based security for encrypted traffic analysis. IEEE Communications Magazine, 59(2):48–54, Feb 2021.   
[38] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova. BERT: Pretraining of deep bidirectional transformers for language understanding. In Proceedings of NAACL-HLT, pages 4171–4186, 2019.   
[39] ISCX. Iscx tor 2016 dataset. Dataset, 2016. Accessed: 2023-10- 01.   
[40] A. Shiravi, H. Shiravi, M. Tavallaee, and A. A. Ghorbani. Toward developing a systematic approach to generate benchmark datasets for intrusion detection. In Computers & Security, volume 31, pages 357–374, 2012. Associated dataset: ISCX VPN 2016.   
[41] Chalmers University of Technology. 5g mobile app traffic traces (chalmers 2023). https://ieee-dataport.org/docume nts/5g-mobile-app-traffic-traces-chalmers-2023, 2023. Accessed: 2024-11-14.   
[42] Aamina Hassan. Cstnet, 2024.   
[43] Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux, Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed. Mistral 7b. arXiv preprint arXiv:2310.06825, 2023.   
[44] Susan Zhang, Stephen Roller, Naman Goyal, Mikel Artetxe, Moya Chen, Shuohui Chen, Christopher Dewan, Mona Diab, Xian Li, Xi Victoria Lin, Todor Mihaylov, Myle Ott, Sam Shleifer, Kurt Shuster, Daniel Simig, Punit Singh Koura, Anjali Sridhar, Tianlu Wang, and Luke Zettlemoyer. Opt: Open pre-trained transformer language models, 2022.   
[45] Ian J Goodfellow, Jonathon Shlens, and Christian Szegedy. Explaining and harnessing adversarial examples. arXiv preprint arXiv:1412.6572, 2014.
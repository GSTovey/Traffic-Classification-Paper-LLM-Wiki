Full length article

# PacketPatch: Practical generation and deployment of adversarial packets for byte-feature-based encrypted traffic classification

![](images/69a30036eb9c2dcb878d6d9fe1ecd87b62ae63bda2a9bcdef30b71e3d3ed09f9.jpg)

Yuwei Xu <sup>a,b</sup> <sup>,∗</sup>, Yuanyuan Xu <sup>a</sup> , Yunpeng Bai <sup>a</sup> , Jiahui Chen <sup>a</sup> , Kehui Song <sup>c</sup> , Jie Cao <sup>d</sup> , Qiao Xiang <sup>e</sup> , Guang Cheng <sup>a,b</sup>

<sup>a</sup> School of Cyber Science and Engineering, Southeast University, Nanjing, 211189, China

<sup>b</sup> Purple Mountain Laboratories, Nanjing, 211111, China

<sup>c</sup> School of Software, Tiangong University, Tianjin, 300387, China

<sup>d</sup> Department of Electrical and Computer Engineering, Queen’s University, Kingston, K7L 3N6, Canada

<sup>e</sup> School of Informatics, Xiamen University, Xiamen, 361005, China

## A R T I C L E I N F O

Keywords: Encrypted traffic classification User privacy protection Adversarial examples Black-box assumption Byte features BERT

## A B S T R A C T

In recent years, byte features have been widely adopted in deep learning-based encrypted traffic classification, achieving remarkable performance. While enabling efficient network resource scheduling and enhancing network security, such techniques also pose serious threats to user privacy. To mitigate these risks, generating adversarial packets that evade traffic classifiers has emerged as an effective defensive strategy. However, existing studies face challenges including dependence on unrealistic preconditions, excessive time and band width overhead, and compromised packet usability. To address shortcomings in prior studies, we present PacketPatch, a practical scheme for generating adversarial packets against byte-feature-based encrypted traffic classification (B-ETC). To avoid unrealistic preconditions, we design a BERT-based perturbation vector generator, PatchGenerator, that operates under a black-box assumption by producing perturbations from original packets and random header data without requiring access to model gradients or user behavior history. To reduce time and bandwidth overhead, PatchGenerator generates perturbations with a single forward pass and dynamically adjusts the number of masked bytes according to the packet size, thereby controlling the perturbation length. To ensure packet usability, we further propose a symmetric proxy-based deployment h d h b h b d b h k h d d l d d updating the necessary protocol fields, adversarial packets can successfully pass integrity checks and be seamlessly restored at the receiving end. We evaluate PacketPatch on three datasets and compare it with four state-of-the-art white-box baseline methods. The results show that PacketPatch outperforms the baseline methods in most scenarios. Its average adversarial vector generation time is only 10.078 ms, and its bandwidth overhead is significantly lower than that of template-filling methods. Moreover, experiments on a prototype system confirm that PacketPatch can bypass B-ETC models and restore the original information at the receiver.

## 1. Introduction

The Internet has permeated numerous facets of contemporary society, playing a pivotal role in essential sectors such as finance, healthcare, and education (Aouedi et al., 2025). Consequently, an immense amount of sensitive personal information is continually transmitted across network infrastructure. As the fundamental conduit for informa tion exchange, network traffic is critical to upholding data security and safeguarding privacy (Sharma and Lashkari, 2025). To bolster privacy protection in network communications, a range of encryption protocols, including HTTPS and QUIC, have been widely adopted (Dong et al., 2025).

The rapid evolution of artificial intelligence technology has led to the emergence of deep learning-based encrypted traffic classification (ETC) methods (Sharma and Lashkari, 2025), which are advancing at an impressive rate. These techniques have demonstrated remarkable precision in distinguishing various types of encrypted traffic across a range of network application scenarios, including web browsing (Cheng et al., 2021), mobile application access (Aceto et al., 2019), and Internet of Things transmission (Zhu et al., 2023). Although communication content is protected by encryption protocols, ETC methods can still infer user behavior by leveraging the multi-dimensional features of traffic, posing a potential threat to personal privacy. In actual network environments, skilled adversaries can leverage advanced ETC models to infer sensitive information about access behaviors from encrypted traf fic, thereby compromising user privacy (Papadogiannaki and Ioannidis, 2021).

In the realm of encrypted traffic classification, byte feature-based methods have emerged as the leading technical approach (Lin et al., 2022). These methods use natural language processing (NLP) concepts to treat structured packet byte sequences like text, allowing them to capture both local byte patterns and long-range contextual information. By examining packet headers and some payloads, these methods extract detailed semantic features from encrypted traffic, leading to better classification performance in various scenarios (Wu et al., 2023). Owing to their remarkable advantages in accuracy and applicability, byte feature-based encrypted traffic classification (B-ETC) methods have progressively emerged as a significant tool for malicious attackers to infer user behavior and compromise sensitive information, thereby presenting fresh challenges to current encryption-based network privacy protection approaches (Shen et al., 2022).

In recent years, deep learning models have demonstrated an inherent vulnerability to adversarial examples (AEs) across domains like computer vision (CV) (Dai et al., 2024) and NLP (Ye et al., 2023). Even minor, thoughtfully crafted alterations can dramatically skew the model’s decision-making process. Drawing inspiration from this, the development of adversarial examples aimed at undermining the inference abilities of B-ETC models presents a viable strategy for reducing the threat to user privacy. While recent research (Ding et al., 2022; Sadeghzadeh et al., 2021; Ding et al., 2024; Zhang et al., 2020; Hore et al., 2025; Sun et al., 2025; Kotak and Elovici, 2023; Cao et al., 2024) has delved into this area, the majority concentrates on improving AE success rates against classification models, usually ignoring practical limitations in real-world networks. The specific shortcomings of existing methods can be summarized in the following three aspects.

(1) Unrealistic preconditions. Current methods for generating ad versarial examples frequently rely on idealistic assumptions. Some methods assume the privacy-preserving party has full access to the target ETC model, including its structure, parameters, and gradient information, allowing for constructing adversarial perturbations in a white-box manner (Ding et al., 2024; Sun et al., 2025; Kotak and Elovici, 2023). Some methods utilize a user’s past network behavior, including previously accessed websites or applications, to steer the optimization of adversarial perturbations (Sadeghzadeh et al., 2021). In real-world network environments, a privacy-preserving party is unlikely to obtain such complete information.

(2) Excessive overhead. Although existing studies reduce the accu racy of B-ETC models, they often introduce significant time and bandwidth overhead. Some methods use several rounds of queries to the target model, adjusting perturbations based on feedback until they successfully mislead the model (Zhang et al., 2020; Hore et al., 2025; Sun et al., 2025). This interactive generation process is resource-intensive and suffers from substantial response latency, posing challenges in fulfilling the requirements for realtime transmission. Some methods improve the perturbation effect by adding many redundant bytes to packets, but this greatly increases traffic volume and wastes bandwidth (Ding et al., 2024; Sun et al., 2025: Kotak and Elovici, 2023).

(3) Disrupting packet usability. Unlike images, network data pack ets are strictly constrained by protocols at both the format and semantic levels. In network communication scenarios, even mi nor modifications to data packet fields can disrupt their normal functionality. Changes to packet header fields can disrupt rout ing, connection maintenance, and transmission control, while altering the payload can hinder the receiving end’s ability to read application-layer data. Nevertheless, existing methods inadequately account for these protocol constraints, leading to adversarial examples that can deceive ETC models but do not facilitate normal data transmission (Ding et al., 2022).

Aiming at the shortcomings of previous work, we present PacketPatch. This innovative scheme effectively generates and deploys adversarial packets<sup>1</sup> in real network environments, thereby safeguarding user privacy from B-ETC models. In PacketPatch, we design a packet-level perturbation vector generator and propose a symmetric proxy-based deployment method. The main contributions of this paper can be summarized as the following points.

• <sub>To bypass unrealistic preconditions, we design PatchGenerator,</sub> a perturbation vector generator under the strict black-box assumption. PatchGenerator is built upon BERT and is trained using the same category prediction (SCP) task as well as the spanmasked byte modeling (Span-MBM) task. It can capture deep semantic information from packet bytes, removing reliance on the target model’s gradient information. Moreover, by utilizing the original packet alongside a random header as input and defining the optimization goal to increase the disparity from the original packet while aligning the generated features closer to the random header, the generator eliminates the necessity to obtain prior insights into user access behavior.

• <sub>To reduce time and bandwidth overhead, we focus on comprehen-</sub> sive optimization of PatchGenerator. By generating perturbation vectors through a single forward pass, PatchGenerator avoids the delays associated with multiple iterative queries, thus ensuring real-time performance. By adjusting the number of mask bytes based on packet size, PatchGenerator manages the perturbation vector length effectively. Thus, it safeguards against high bandwidth overheads that may be incurred from unnecessarily padding with excessive bytes.

• <sub>To ensure the usability of adversarial packets, a symmetric proxy-</sub> based deployment method is proposed. At the sending end, the proxy inserts a perturbation vector at the junction of the header and payload, effectively safeguarding against message transmission failures that may arise from corruption in the header fields. Both the packet length and checksum fields are adjusted simultaneously to ensure that adversarial packets can pass the integrity check upon reaching their destination. At the receiver’s end, the proxy precisely eliminates the perturbation vector based on the synchronized configuration, guaranteeing the accurate interpretation of the original information.

• <sub>To validate PacketPatch, we executed comprehensive compara-</sub> tive experiments across three datasets, comparing its effectiveness with four adversarial packet generation methods. The results show that PacketPatch outperforms current state-of-the-art whitebox baselines in most scenarios. Moreover, PacketPatch produces perturbation vectors in just 10.078 ms, well within acceptable network transmission latency limits, while achieving a bandwidth overhead that is considerably lower than that of template-filling methods. Finally, tests on a prototype system show that Packet-Patch’s adversarial packets can successfully bypass B-ETC models and allow the receiving end to accurately recover the original information.

The rest of this paper is organized as follows. In Section 2, we summarize previous related research, covering B-ETC models and their adversarial example generation methods. The overall design of Packet-Patch is introduced in Section 3, following the presentation of the threat model and design goals. In Section 4, we describe PatchGenerator, focusing on its model architecture, training tasks, and the generation of perturbation vectors. Section 5 delves into the practical implementation of adversarial packets, covering system deployment, the construction of adversarial packets, and the restoration of original information. We detail the experimental setup in Section 6 and evaluate PacketPatch’s performance, overhead, and usability in Section 7. Finally, a conclusion is given in Section 8.

## 2. Related work

This section begins with an exploration of the technological ad vancements in B-ETC methods, followed by a comprehensive overview of the existing adversarial example generation techniques for these l f d l

## 2.1. B-ETC methods

Recently, byte features of packets have gained increasing attention in ETC tasks due to their ability to bypass complex feature extraction processes while achieving high classification accuracy. Depend ing on the data representation strategy, existing B-ETC methods can be categorized into three classes: image-based, sequence-based, and contextualized representations.

Some researchers convert the content of packets into image formats and apply deep learning models originally developed for CV to complete traffic classification. At the packet level, the authors of Zhou et al. (2021) mapped the first 1024 bytes of a packet into a 32 × 32 grayscale image, employing 2D-CNNs for classification. Extending this to the session level, in Wang et al. (2017b), the authors pioneered the conversion of the first 784 bytes of a session into 28 × 28 grayscale images, demonstrating that treating raw traffic as visual inputs effectively facil itates malware detection. To further enrich feature expressiveness, the authors of Hu et al. (2023) transformed session bytes into 28 × 28 RGB images. By utilizing multi-channel color encoding rather than simple grayscale intensity, this method captures more complex, fine-grained patterns essential for identifying malware variants.

Acknowledging that network traffic intrinsically consists of sequen tial data streams, some methods focus on sequence-based representation. At the packet level, in Wang et al. (2017a), the authors provided empirical evidence that 1D-CNNs exhibit feature extraction capabilities superior to 2D-CNNs when applied to raw traffic bytes. Capitalizing on this finding, DeepPacket (Lotfollahi et al., 2020), an ETC model utilizing 1D-CNN architecture, was proposed. It processes the entire 1500- byte maximum transmission unit (MTU) of each packet as a unified sequence for classification. For flow-level analysis, TSCRNN (Lin et al., 2021) serves as a hybrid framework that synergizes 1D-CNNs with Bi-LSTMs. By processing the first 15 packets of a flow, this model concurrently extracts intra-packet spatial features and inter-packet temporal dependencies, yielding robust spatiotemporal representations.

Emerging studies have adopted contextualized representation, in spired by NLP, to capture deep semantic dependencies by regarding traffic bytes as semantic tokens. PERT (He et al., 2020) utilizes the ALBERT architecture combined with bigram tokenization to extract dynamic contextual features from packet payloads. Leading this di rection, the authors of Lin et al. (2022) proposed ET-BERT, which adapts the pre-training paradigm to massive unlabeled datasets. By encoding packet bytes into discrete tokens, this method learns contextualized representations of network protocols, effectively modeling the bidirectional context within the traffic.

## 2.2. AE against B-ETC methods

Due to the discrete, non-differentiable nature of network traffic and rigid protocol syntax, constructing adversarial examples for packet bytes is challenging. Existing methods are categorized into gradientbased, query-based, and saliency-based methods, as summarized in Table 1.

To leverage the differentiability of target models, gradient-based methods typically employ optimization strategies that relax the discrete constraints of network traffic by mapping packet bytes into continuous image pixel matrices to compute perturbation directions. Targeting general scenarios, P2I-Adv (Ding et al., 2022) processes packet content into 2D grayscale images and employs mature CV algorithms like FGSM to generate perturbations. However, this method performs irreversible modifications on packet headers. Since network packets have strict structural constraints, such modifications disrupt packet usability and often prevent the receiver from parsing the information. To address the universality issue, the authors of Sadeghzadeh et al. (2021) proposed ANT, which trains specific perturbation vectors for each traffic class and adds them to the packet tail. Nevertheless, its drawback lies in the unrealistic precondition that it necessitates prior knowledge of the user’s browsing behavior, specifically the traffic category, to select targeted parameters. Similarly, UTAA (Ding et al., 2024) generates fixed-length perturbations of 784 bytes based on gradients and applies them via modulo addition. This fixed-length strategy forces the padding of excessive bytes when perturbing short packets, leading to unacceptable bandwidth consumption. In summary, although these methods are computationally efficient, they fundamentally rely on white-box access to the attacker’s model, including model structure and gradients. This requirement limits their application in realistic defense scenarios where model parameters are usually unknown.

In scenarios where gradient information is inaccessible, query-based methods serve as a viable alternative, relying on iterative processes that employ heuristic strategies or reinforcement learning (RL) to explore the perturbation space by continuously probing the target model. In Zhang et al. (2020), the authors analyzed browser parsing mechanisms and proposed MCTS-T, utilizing Monte Carlo Tree Search to iteratively construct adversarial examples that bypass XSS detectors. Expanding on this idea for general traffic, the authors of Hore et al. (2025) designed DeepPackGen, an RL-based generator that modifies specific header fields to bypass detection. Another RL-based method, AdvTg (Sun et al., 2025), tends to introduce excessive padding to ensure evasion, which results in prohibitive costs regarding bandwidth efficiency. The common limitation of this category is the excessive overhead in time consumption. These methods rely on iterative queries to the classification model, refining perturbations based on feedback until deception is achieved. This process is extremely time-consuming, rendering such methods unsuitable for real-time transmission. Furthermore, the reliance on continuous interaction implies they are not strictly black-box methods, as they require a responsive query interface to the specific target model.

Distinct from global perturbation strategies, saliency-based method focus on feature replacement by prioritizing the manipulation of specific critical tokens identified by interpretability tools or vulnerability analysis. A-IOT (Kotak and Elovici, 2023) processes the first 784 bytes into a grayscale image and uses Class Activation Mapping (CAM) to rank pixel importance, retaining only critical bytes in a transmission template. A major downside of this approach is its use of a fixed-length template of 784 bytes, which causes excessive bandwidth consumption when processing shorter packets. More recently, the authors of Cao et al. (2024) introduced BYTEFLIPPING, which utilizes a payload byte vulnerability ranking (PBVR) algorithm to identify and perturb vul nerable bytes specifically. Although some methods in this category attempt to optimize byte selection to preserve semantics, they share a common unrealistic precondition. Calculating saliency maps or vulnerability rankings inherently necessitates white-box access to the attacker’s model, such as internal activation functions or detailed probability outputs, which is rarely available to defenders in practice.

Table 1  
A summary of adversarial example methods against B-ETC models.

<table><tr><td>Ref.</td><td>Method</td><td>Category</td><td>Black-Box</td><td>No-User-Info</td><td>Real-Time</td><td>Limited BWO</td><td>Usability</td></tr><tr><td>Ding et al. (2022)</td><td>P2I-Adv</td><td rowspan="3">Gradient-based</td><td>×</td><td>√</td><td>√</td><td>√</td><td>×</td></tr><tr><td>Sadeghzadeh et al. (2021)</td><td>ANT</td><td>×</td><td>×</td><td>√</td><td>√</td><td>√</td></tr><tr><td>Ding et al. (2024)</td><td>UTAA</td><td>×</td><td>√</td><td>√</td><td>×</td><td>√</td></tr><tr><td>Zhang et al. (2020)</td><td>MCTS-T</td><td rowspan="3">Query-based</td><td>×</td><td>√</td><td>×</td><td>√</td><td>√</td></tr><tr><td>Hore et al. (2025)</td><td>DeepPackGen</td><td>×</td><td>√</td><td>×</td><td>√</td><td>√</td></tr><tr><td>Sun et al. (2025)</td><td>AdvTg</td><td>×</td><td>√</td><td>×</td><td>×</td><td>√</td></tr><tr><td>Kotak and Elovici (2023)</td><td>A-IOT</td><td rowspan="2">Saliency-based</td><td>×</td><td>√</td><td>√</td><td>×</td><td>√</td></tr><tr><td>Cao et al. (2024)</td><td>BYTEFLIPPING</td><td>×</td><td>√</td><td>×</td><td>√</td><td>√</td></tr><tr><td>Ours</td><td>PacketPatch</td><td>Inference-based</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td></tr></table>

![](images/6a0841ae77e16c3ec236aef1f6ef8f4aeccdd425104c4d086ff3c8bff3f8d49a.jpg)  
Fig. 1. The privacy protection scenario of PacketPatch.

## 3. Design of PacketPatch

To systematically address the practical limitations of existing ad versarial attacks, this section articulates the comprehensive design of PacketPatch. We first formally define the threat model to establish a rigorous boundary for the defense, followed by the formulation of critical design goals. Finally, we present the overview of the Packet-Patch framework, demonstrating how these goals are realized through a coherent operational workflow.

## 3.1. Threat model

We consider a typical network communication environment, as illustrated in Fig. 1. In this scenario, network packets are transmitted between client endpoints and remote servers via public networks to deliver internet services. However, this transmission path is inherently vulnerable. Adversaries located at intermediate nodes, such as routers, gateways, and switches, can capture the passing traffic. By leveraging well-trained ETC models, these adversaries analyze packet content to infer sensitive user activities, resulting in privacy leakage.

To formally characterize this threat, we define the problem as follows. Let  represent the space of network packets, where a sensitive packet is denoted as $x \in { \mathcal { X } } .$ . Let $\mathcal { V } = \{ 1 , 2 , \dots , K \}$ denote the set of traffic categories, where $y \in \mathcal { V }$ represents the ground-truth label associated with �. The adversary deploys a well-trained B-ETC model, denoted as $C : \mathcal { X }  \mathcal { Y }$ , which maps the observed packet � to a predicted label. We define the adversary  as a passive eavesdropper characterized by the following three aspects:

Attacker’s Goal: The primary objective of  is to infer the category of the user’s encrypted traffic, thereby facilitating the construction of user profiles or website fingerprinting attacks. To achieve this,  employs � to predict the label of a captured packet �. The adversary aims to maximize the expected classification accuracy over the underlying data distribution . As shown in Eq. (1), where I(⋅) denotes the indicator function, this optimization problem is formulated as:

$$
\max \mathbb {E} _ {(x, y) \sim \mathcal {D}} [ \mathbb {I} (C (x) = y) ].\tag{1}
$$

Attacker’s Knowledge: We adopt a realistic threat setting where  possesses domain knowledge regarding the network environment.  is fully aware of the traffic categories and protocols present in the network and has trained a high-performance � by leveraging abundant publicly available labeled datasets. However,  is oblivious to the existence of any active defense mechanisms, operating under the assumption that the captured traffic consists purely of benign packets rather than adversarial packets.

Attacker’s Capability: The adversary  maintains read-only access to the traffic channel. They can capture, store, and analyze packets flowing through the public network but cannot modify, drop, or inject packets.

Under this threat model, the defender aims to preserve user privacy by generating a perturbation vector � and applying it to the original packet � to construct an adversarial packet ̃�. Consequently, the defender seeks to minimize the expected probability that the attacker successfully identifies the true label � across the data distribution. As formulated in Eq. (2), this optimization goal is defined as:

$$
\min \mathbb {E} _ {(x, y) \sim \mathcal {D}} [ \mathbb {I} (C (\tilde {x}) = y) ].\tag{2}
$$

## 3.2. Design goals

To effectively counter the threats defined in Section 3.1, we delineate five critical design goals for PacketPatch:

( ) hi l k li bili k h f i strictly without access to the target identification model’s internal parameters, gradients, or training data. The defense mechanism relies solely on the input packet features to construct adversarial packets, ensuring robustness in realistic scenarios where attackers conceal their model architectures.

(2) Ensure User-Agnostic Operation: The perturbation generation must rely exclusively on the features of the current packet, independent of any user-specific private information or historical behavioral profiles. This constraint ensures that the privacy protection mechanism itself does not become a source of sensitive data leakage.

(3) Guarantee Real-Time Efficiency: To support high-throughput network environments, the adversarial packet generation process must achieve millisecond-level latency, strictly capping the processing time below 20 ms per packet. The inference overhead must be negligible to ensure that the defense mechanism does not introduce perceptible delays to the user’s communication service.

(4) Maintain Controllable Bandwidth Overhead: The system must strictly limit the size of injected perturbation vectors to avoid network congestion. Specifically, the bandwidth overhead is constrained to a maximum ratio of 10% relative to the original packet size. Furthermore, the total packet length after perturbation is strictly bounded by the standard MTU of 1500 bytes to prevent IP fragmentation or packet drops.

(5) Ensure Packet Validity and Recoverability: The modified packets must strictly adhere to standard network protocol specifications to avoid being filtered by intermediate devices. Crucially, the scheme necessitates a reversible mechanism, ensuring that the legitimate receiver can perfectly remove the perturbation and reconstruct the original payload for correct content parsing.

![](images/a288c35be36a2132591dbfa85a0690a4957d5b7fbcbeb6e43a18d7da838f52b9.jpg)  
Fig. 2. The workflow of PacketPatch.

## 3.3. Overview of PacketPatch

To effectively achieve the design goals outlined in Section 3.2, we propose PacketPatch, a practical adversarial packet construction framework. Structurally, PacketPatch comprises a perturbation vector generator, named PatchGenerator, and a symmetric proxy-based deployment mechanism, which jointly facilitate privacy preservation against B-ETC models while maintaining strict packet recoverability. As illustrated in Fig. 2, the system workflow is systematically organized into four distinct phases:

(1) PatchGenerator Training. We design the PatchGenerator based on the ET-BERT architecture (Lin et al., 2022). To equip this architecture with the specific capability to generate adversarial perturbations, we propose two customized training tasks. The SCP task is designed to capture discriminative features for traffic classification. Meanwhile, the Span-MBM task is formulated to provide context-aware reconstruction capabilities, allowing the model to infer and generate byte sequences consistent with the packet context.

(2) PacketPatch Deployment. The well-trained PatchGenerator is independently deployed on both the client side and the server side. To ensure the reversibility of the perturbation, the configuration file of PacketPatch is synchronized between both parties, defining the critical parameters used for constructing adversarial packets. To ensure noninvasive integration with existing network applications, the deployment is performed through a proxy architecture. This design allows for seamless packet manipulation without requiring modifications to the original application logic.

(3) Adversarial Packet Construction. Due to the bidirectional na ture of network traffic, both the user side and the server side alternately function as the sender and receiver. Before transmitting data, the sender utilizes the deployed PacketPatch system to construct an adversarial packet. The system generates and embeds the perturbation vector into the payload, and the resulting packet is then transmitted across the network.

(4) Original Packet Restoration. Upon receiving the adversarial packet, the receiver activates the restoration process according to the synchronized configuration file. The system removes the perturbation to restore the original packet perfectly. Subsequently, the restored data is parsed following standard protocols, ensuring that the original information is delivered correctly to the application layer.

## 4. PatchGenerator

This section presents the PatchGenerator. First, we introduce the architecture and input representation optimized for packet bytes. Then, we detail the SCP and Span-MBM tasks used to train the model. Finally, we describe the procedure for generating context-aware perturbation vectors.

## 4.1. Model architecture of PatchGenerator

Given the powerful encrypted traffic feature extraction capabilities of the pre-trained ET-BERT model. we adopt ET-BERT as the foundation for PatchGenerator. As illustrated in Fig. 3, the architecture of PatchGenerator is structurally organized into four primary components: the input layer, the embedding layer, the encoder layer, and the task-specific output layer.

(1) Input Layer. The input layer processes raw bytes from two distinct packets into discrete tokens. Following the ET-BERT design, every two consecutive bytes are treated as a single input unit and tokenized via byte-pair encoding (BPE). Diverging from the ET-BERT approach, we optimize the input representation by increasing the sliding window stride from 1 to 2. This adjustment creates non-overlapping input units, allowing the model to cover a broader context of the packet bytes.

![](images/1db16b60884dc3a2ee3d1ee9dbc7eddeaf08ed5fa40f84217ecbc0c7f0d4ca05.jpg)  
Fig. 3. Model architecture of PatchGenerator.

(2) Embedding Layer. To capture multidimensional features of the tokenized inputs, three distinct embedding methods are employed. Token embedding maps the semantic information of byte tokens into dense vectors. Position embedding encodes the sequential order of tokens to preserve positional information within the input sequence. Segment embedding assigns segment A to Packet 1 and segment B to Packet 2, enabling the model to distinguish which packet each token belongs to. All three embeddings share a dimension of 768 and are summed element-wise to form the input for the subsequent encoder layer.

(3) Encoder Layer. Serving as the core feature extractor, this layer employs 12 transformer encoder blocks. Within each block, the input first passes through a multi-head self-attention mechanism with 12 heads to capture global dependencies among byte tokens, then through a position-wise feed-forward network. To facilitate deep network train ing, residual connections and layer normalization are applied after each sub-layer.

(4) Output Layer. The output layer comprises two task-specific heads designed for distinct purposes. To capture discriminative features across traffic categories, the SCP head first extracts the [CLS] token representation $h _ { \mathrm { C L S } } .$ , then predicts categorical consistency between Packet 1 and Packet 2 through fully connected layers (FCLs) with Tanh activation. To enable context-aware byte reconstruction, the Span MBM head first extracts the masked token states $h _ { \mathrm { M A S K } }$ , then generates probability distributions over the token vocabulary through an FCL with Gelu activation, layer normalization, and a softmax decoder.

![](images/361f1530f468dcc7327e2ecdc9fd00a88469fd9b4243a4aeacd9f49e46c0d1c1.jpg)  
Fig. 4. Comparison of byte embedding mechanisms between ET-BERT and PatchGenerator

## 4.2. Input representation of PatchGenerator

The standard ET-BERT employs bi-gram encoding with a sliding window stride of 1. While robust for classification, this representation imposes critical limitations on perturbation generation. The inherent token overlap causes significant content redundancy that complicates packet reconstruction, while the dense stride restricts the effective contextual coverage to only $n + 1$ bytes for a sequence of length �, hindering the capture of long-range dependencies. To address these inefficiencies, we introduce a strategic optimization to the input encoding, as illustrated in Fig. 4. While retaining the bi-gram unit structure, we increase the sliding window stride from 1 to 2. This adjustment creates a non-overlapping input sequence, fundamentally altering how the model interacts with raw packet bytes.

This modification yields three critical advantages. First, the elimination of overlap ensures that adjacent input units no longer share bytes, allowing the generated vectors to be directly interpreted as continuous byte sequences without the need for post-processing. Second, this approach provides extended coverage, where a model input of length � tokens can now process 2� bytes, effectively doubling the contextual information available for perturbation generation. Finally, the modified input representation preserves pre-trained knowledge by sharing half of its content with the original ET-BERT format. This structural alignment ensures that the pre-trained features remain transferable, while the subsequent training process further adapts the PatchGenerator to this optimized input form.

## 4.3. SCP task

To enable PatchGenerator to capture discriminative features across traffic categories, we design the SCP task, which trains the model to determine whether two input packets belong to the same traffic category. The core motivation is that effective adversarial perturbation generation requires the model first to understand categorical differences, as this capability is a prerequisite for generating perturbations that can successfully alter classification outcomes. The implementation of the SCP task proceeds in two sequential stages comprising input construction and model training.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 The input construction of the SCP task.

Require: Collection of packets S, Maximum input length n
Ensure: Paired model input X

1:  $X \leftarrow []$ 
2: for  $(x_i, y_i) \in S$  do
    // Step 1: Packet Pairing
3:  $P_{sameCategory} \leftarrow random(0, 1)$ 
4: if  $P_{sameCategory} &lt; 0.5$  then
5:  $(x_j, y_j) \leftarrow random(\{y_j \neq y_i, (x_j, y_j) \in S\})$ 
6: else
7:  $(x_j, y_j) \leftarrow random(\{y_j = y_i, (x_j, y_j) \in S\})$ 
8: end if
    // Step 2: Dynamic Partition
9:  $P_{x_iStart} \leftarrow random(0, 1)$ 
10: if  $P_{x_iStart} &lt; 0.5$  then
11:  $p_{x_iend} \leftarrow random(0.25, 0.75)$ 
12:  $x_i \leftarrow x_i[0 : p_{x_iend} \times n]$ 
13: else
14:  $p_{x_istart} \leftarrow random(0, 0.5)$ 
15:  $p_{x_iend} \leftarrow random(x_i start, 0.75)$ 
16:  $x_i \leftarrow x_i[p_{x_istart} \times n : p_{x_iend} \times n]$ 
17: end if
18: Update  $x_j$  similar to lines 9-17
    // Step 3: Sequence Assembly
19:  $x \leftarrow [] .expand([CLS], x_i, [SEP], x_j)$ 
20: if len(x) &gt; n then
21:  $x \leftarrow x[0 : n]$ 
22: end if
23: while len(x) &lt; n do
24:    x.append([PAD])
25: end while
26: X.append(x)
27: end for
    return X
</div>

(1) Input Construction. The input construction process is detailed in Algorithm 1. To enhance the model’s generalization capability, we implement a three-step construction strategy:

• <sub>Step 1: Packet Pairing: For each packet</sub> $( x _ { i } , y _ { i } )$ in the dataset, a second packet $( x _ { j } , y _ { j } )$ is randomly selected. To ensure class balance, there is a 50% probability that $x _ { j }$ belongs to the same category as $x _ { i }$ and a 50% probability that it belongs to a different category.

• <sub>Step 2: Dynamic Partition: To prevent overfitting to specific</sub> header fields, each packet undergoes dynamic partition. With 50% probability, the packet is truncated from the header; otherwise, it starts from a random early position. The length is randomly selected between 1/4 and 3/4 of the maximum input length (�).

• <sub>Step 3: Sequence Assembly: The two packets are concatenated</sub> into a single sequence: [CLS] $+ \ x _ { i } + [ \mathsf { S E P } ] + x _ { j } ,$ . The sequence is then padded with [PAD] tokens or truncated to strictly match the fixed input length �.

(2) Model Training. After obtaining the paired input set $X ,$ the model is trained to distinguish whether the packet pair shares the same category. For supervision, we assign the ground-truth label $y =$ 1 to same-category pairs and $y ~ = ~ 0$ to different-category pairs. The model utilizes the hidden state at the [CLS] token position to generate the predicted probability �(same) that the two packets belong to the same category, and conversely �(diff) that they originate from different categories. Based on these definitions and the ground-truth label �, the training objective is to minimize the binary cross-entropy loss function, as defined in Eq. (3):

$$
L o s s _ {S C P} = - [ y \log P (\text { same }) + (1 - y) \log P (\text { diff }) ]\tag{3}
$$

## 4.4. Span-MBM task

Standard Masked Language Modeling (MLM) (Devlin et al., 2019) relies on discrete masking, which is ill-suited for generating continuous adversarial perturbations. To bridge this gap, we design the Span MBM task. By extending the masking mechanism from isolated tokens to continuous segments, this task forces the model to utilize longrange context, thereby equipping PatchGenerator with the capability to synthesize coherent, continuous byte sequences. The implementation proceeds in two stages: input construction and model training.

(1) Input Construction. The detailed construction process of longrange masks is presented in Algorithm 2. Specifically, for an input sample $x = \{ t _ { 1 } , t _ { 2 } , \ldots , t _ { n } \}$ with � tokens, we first determine the total number of tokens to be masked, denoted as $N _ { m a s k }$ . The process proceed in two sequential steps corresponding to the algorithm:

• <sub>Step 1: Span Length and Position Generation. We iteratively</sub> generate the coordinates for each mask span until the cumulative length of masked tokens reaches the target count $N _ { m a s k } .$ . In each iteration, a span length is first randomly sampled, followed by the selection of a starting position uniformly distributed across the sequence. To ensure the validity of the mask, we enforce a strict non-overlapping constraint: any candidate span that intersects with previously selected positions is discarded or re-adjusted.

• <sub>Step 2: Span-Masked Byte Replacement. After determining the</sub> positions, we execute the replacement. Crucially, to compel the model to recover continuous semantics, we apply a probabilistic strategy to the entire span as a whole unit, rather than to individual tokens. For each span, there is an 80% probability of replacing all internal tokens with [MASK], a 10% probability of replacing them with random noise tokens, and a 10% probability of keeping the original tokens unchanged.

(2) Model Training. After obtaining the masked sample ${ \overline { { x } } } ,$ the PatchGenerator is trained to reconstruct the original byte sequence based on the bidirectional context. We utilize an FCL to map the encoder output to the packet vocabulary space. To formulate the optimization objective, let ������� represent the set of all token positions within the selected spans, and �(⋅) denote the probability of correctly predicting the original token $t _ { i } .$ The training goal is to minimize the Negative Log-Likelihood loss, as defined in Eq. (4):

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 The input construction of the Span-MBM task.

Require: Original sample  $x = \{t_{1}, t_{2}, \ldots, t_{n}\}$ , Total number of mask  $N_{mask}$ 

Ensure: Sample after replacing Span-Masked Bytes  $\overline{x}$ 

// Step 1: Span Length and Position Generation

1: cnt ← 0

2: spanPos ← {}

3: while cnt &lt;  $N_{mask}$  do

4: spanLen ← random(0,  $N_{mask}$ )

5: if spanLen + cnt &gt;  $N_{mask}$  then

6: spanLen ←  $N_{mask} - cnt$ 

7: end if

8: do

9: posStart ← random(0, n)

10: if posStart + spanLen &gt; n then

11: spanLen ← n - posStart

12: end if

13: span ← {posStart, ..., posStart + spanLen}

14: while {span ∩ pos|∀pos ∈ spanPos} ≠ ∅

15: spanPos ← spanPos ∪ {span}

16: end while

// Step 2: Span-Masked Byte Replacement

17:  $\overline{x} \leftarrow x$ 

18: for pos ∈ spanPos do

19: p ← random(0, 1)

20: if p &lt; 0.8 then

21: for i ∈ pos do

22:  $\overline{x}[i] \leftarrow [MASK]$ 

23: end for

24: else if p &lt; 0.9 then

25: for i ∈ pos do

26:  $\overline{x}[i] \leftarrow getRandomCharacter()$ 

27: end for

28: else

29: continue

30: end if

31: end for

return  $\overline{x}$
</div>

$$
L o s s _ {S p a n - M B M} = - \sum_ {i \in m a s k P o s} \log (P (\overline {{x}} [ i ] = t _ {i} | \overline {{x}}; \theta))\tag{4}
$$

To integrate the discriminative and generative capabilities devel oped by the two self-supervised tasks, we combine their respective optimization goals. The overall loss function guiding the PatchGenera tor is calculated as the sum of the SCP loss and the Span-MBM loss, as shown in Eq. (5):

$$
L o s s = L o s s _ {S C P} + L o s s _ {S p a n - M B M}\tag{5}
$$

The equal weighting of the two loss terms follows standard practice in BERT pre-training, where multiple objectives are combined without additional coefficients. Both losses are formulated as crossentropy losses on the same numerical scale, which provides a balanced optimization signal without introducing extra hyperparameters.

The Span-MBM objective trains the model to learn the conditional distribution of packet bytes under the given context. This allows the model to generate tokens that follow the statistical patterns observed in the data. By selecting tokens from different parts of the learned distribution, the model can modify the statistical patterns of the packet. These statistical patterns correspond to the features used by B-ETC models for classification. Changing these patterns directly affects the model input, which increases the probability of misclassification. The

SCP objective complements this process by enabling the model to capture differences between traffic categories, providing guidance on how these patterns vary across classes. Together, these two objectives provide both the ability to model byte-level patterns and the ability to control them, which supports the generation of effective adversarial perturbations. This enables the learned distribution to be directly utilized for perturbation generation.

## 4.5. Perturbation vector generation

Upon completing the training of the SCP and Span-MBM tasks, the PatchGenerator acquires dual capabilities: distinguishing traffic categories and predicting masked content based on context. This section details how to leverage these capabilities to generate adversarial perturbation vectors. As illustrated in Fig. 5, the generation process comprises the following four stages:

(1) Input Preparation. Given a target packet, we first separate its header $x _ { h }$ from its payload $x _ { p } .$ The header includes both network-layer and transport-layer headers. The perturbation length $L _ { p a d }$ is set to 10% of the original packet length. This ratio is selected to strictly limit the bandwidth overhead introduced by the perturbation vector relative to the original packet size. For a standard packet with an MTU of 1500 bytes, this yields a perturbation budget of 150 bytes, corresponding to 75 tokens, which keeps the masked portion under 30% of the total input and preserves sufficient context for effective generation. The 10% setting consequently balances perturbation effectiveness against both bandwidth cost and generation quality. A sequence of $L _ { p a d }$ [MASK] tokens is then prepared for insertion.

(2) Sequence Construction. A random index $r ~ \in ~ [ 0 , L _ { \mathrm { p a d } } ]$ is selected to partition the [MASK] sequence into two segments: Pad and Pad . A [SEP] token is inserted at this position as a segment delimiter, followed by a randomly sampled header $h _ { r }$ with a constant length of 40 bytes. The final input sequence $S _ { \mathrm { i n } }$ is constructed as:

$$
S _ {i n} = [ \mathrm{CLS} ] + x _ {h} + P a d _ {1} + [ \mathrm{SEP} ] + h _ {r} + P a d _ {2} + x _ {p}\tag{6}
$$

This structure allows the PatchGenerator to treat the input as two logically segmented packet entities, leveraging contextual information from both the original and random packets. In practice, $h _ { r }$ is drawn uniformly from a pre-constructed header pool that aggregates standard 20-byte IP headers and 20-byte TCP headers extracted from the training dataset. Because the pool encompasses headers from all traffic categories, the probability that $h _ { r }$ shares the same category as the target packet is negligibly small. Consequently, no category label is required at inference time, and the selection is performed purely at random without relving on any user behavior information.

(3) Perturbation Generation. The sequence $S _ { i n }$ is fed into the PatchGenerator, which outputs conditional probability distributions over candidate bytes at each masked position. These distributions reflect the statistical patterns of packet bytes under the given context. To generate adversarial perturbations, we apply distinct selection strategies to the two segments based on different parts of the learned distribution:

• <sub>Pad : The arg min operation selects tokens with the lowest condi-</sub> tional probability under the context of the original header $x _ { h } .$ . This introduces byte patterns that are inconsistent with the original traffic, thereby disrupting feature consistency.

$\mathbf { P a d } _ { 2 } \mathbf { : }$ The arg max operation selects tokens with the highest conditional probability under the context of the injected random header $h _ { r } .$ . This generates byte patterns that are consistent with other traffic categories.

h d l h d l d b f k b given contextual information. The arg min operation selects tokens from low-probability regions of this distribution, while the arg max operation selects tokens from high-probability regions. Their combination changes the statistical patterns of the packet, pushing it away from the original class and toward other classes. Since B-ETC models rely on these statistical patterns to define decision boundaries, such changes increase the probability that the perturbed packet crosses the decision b d hi d d d ifi d l and therefore remains effective in the black-box setting.

![](images/3734726d5076f534c7118372cff12e2ab5944e490cc97f1c08c335a5d002c27b.jpg)  
Fig. 5. The perturbation vector generation process of PatchGenerator.

(4) Vector Assembly. The final perturbation vector � is assembled by concatenating three components:

$$
v = P a d _ {1} + h _ {r} + P a d _ {2}\tag{7}
$$

The random header $h _ { r }$ is retained as it introduces realistic feature patterns from an alternative category. This combined vector is embedded between the transport-layer header and payload of the origina packet, yielding the final adversarial packet. The total perturbation length is fixed at $L _ { p a d }$ + 40 bytes, ensuring a unique mapping between the original and adversarial packet lengths for accurate recovery by the receiver.

## 5. Application of adversarial packets

This section details the practical implementation of the adversarial traffic application system. To validate the effectiveness of the proposed PacketPatch scheme in real-world network environments, we design and implement a prototype system based on a symmetric proxy architecture.

## 5.1. System architecture and deployment

Given the complexity of directly modifying network stacks within user applications, we adopt a non-intrusive symmetric proxy architec ture based on the SOCKS5 protocol, as illustrated in Fig. 6. The system consists of two core components:

(1) Client Proxy: Deployed on the user’s host, this component inter cepts outbound traffic from client applications, such as web browsers. It constructs adversarial packets by embedding perturbations and for wards them to the server proxy.

(2) Server Proxy: Deployed on a remote server, this component receives the adversarial traffic, removes the perturbations to restore the original payload, and forwards the data to the target server.

To ensure the system supports the precise packet manipulation required by adversarial schemes over TCP streams, we implement two critical engineering optimizations:

![](images/3857bcbeac8af4ea913b8d692c80585fe0ee567fa7b310c79fdebd8ecbaccbe9.jpg)  
Fig. 6. System deployment based on symmetric proxy architecture.

• <sub>Disabling Nagle Algorithm: The proxy explicitly disables the Na-</sub> gle algorithm by setting the TCP\_NODELAY option. This prevents the operating system from buffering and merging small packets, ensuring that the boundaries of our constructed adversarial packets are preserved during transmission.

• <sub>Packet Delimiters: Since TCP is a stream-oriented protocol, we</sub> inject specific 4-byte delimiters, specifically the sequence 0xff, 0xfe, 0xfd, 0xfc, into the payload. This allows the receiver to accurately identify the boundaries of adversarial packets within the continuous data stream for correct restoration.

## 5.2. Adversarial packet construction

The construction of adversarial packets is a pipelined process executed at the sending proxy. To ensure robust evasion and valid transmission, the system strictly follows a three-step procedure: Context Acquisition, Perturbation Generation, and Adversarial Encapsulation.

Step 1: Context Acquisition via Packet Sniffing. The Patch-Generator requires the transport-layer header (TCP/IP header) of the target flow as context to generate effective perturbations. Since the SOCKS5 proxy operates at the application layer and lacks direct access to underlying headers, the system employs a parallel packet sniffer thread utilizing raw sockets. To address the synchronization challenge posed by system latency — where capturing the current packet’s header prior to transmission is infeasible — the system retrieves the header of the preceding packet or the TCP handshake packet belonging to the same 5-tuple flow. By leveraging the temporal stability of flow features, this historical header serves as the effective context input $x _ { c o n t e x t } .$

Step 2: Perturbation Generation. The proxy combines the acquired context $x _ { c o n t e x t }$ with the current user payload to construct the model input. This input is fed into the TensorRT-accelerated PatchGen erator engine. Upon receiving the input, the engine executes a single forward pass with FP16 precision to generate the perturbation vector $v .$ This vector is structurally composed of three distinct segments: the first padding sequence $( P a d _ { 1 } ) ,$ a synthesized random header $\left( h _ { r } \right)$ , and the second padding sequence $( P a d _ { 2 } )$

Step 3: Encapsulation and Transmission. To inject the perturbation while maintaining stream integrity, the proxy manipulates the payload buffer before writing to the socket. First, a specific 4-byte delimiter sequence (0xff, 0xfe, 0xfd, 0xfc) is prepended to the buffer to enable the receiver to identify the start of an adversarial block within the continuous TCP stream. Subsequently, the generated perturbation vector � is inserted immediately following the delimiter, placing it at the head of the original payload. Finally, the modified buffer is written to the standard socket interface, where the operating system’s network stack handles the final encapsulation, automatically calculating checksums and assigning sequence numbers.

## 5.3. Original packet restoration

The restoration process occurs at the receiving proxy. Its primary objective is to transparently identify adversarial packets within the incoming traffic stream and recover the original payload for the target application.

Step 1: Boundary Identification and Alignment. Upon receiving data from the TCP stream, the receiver scans the buffer for the predefined 4-byte delimiter (0xff, 0xfe, 0xfd, 0xfc). The detection of this delimiter signals the beginning of an adversarial packet. This mechanism is crucial for handling potential TCP fragmentation or distinct packet merging, ensuring the receiver always processes aligned data blocks.

Step 2: Perturbation Length Derivation. To minimize overhead, the system does not explicitly transmit the length of the perturbation vector. Instead, the receiver calculates it dynamically by employing a synchronized length mapping rule that is configured identically on both the client and server. Based on the total length of the received data block excluding the delimiter, the receiver computes the precise length of the embedded perturbation $L _ { t o t a l \_ p a d } .$ . This deterministic calculation ensures the accurate separation of perturbation and payload without additional signaling.

Step 3: Stripping and Forwarding. With the boundary and length determined, the restoration is executed. The receiver removes the 4- byte delimiter and the subsequent $L _ { t o t a l \_ p a d }$ bytes corresponding to the perturbation vector from the head of the data block. The remaining bytes constitute the pristine original payload. This clean data is then forwarded to the destination application server via a standard socket connection, making the entire adversarial process transparent to the upper-layer service.

## 6. Experiment settings

In this section, we describe the experimental settings in detail, including datasets, B-ETC models, baseline schemes, and evaluation metrics.

## 6.1. Datasets

To comprehensively validate the effectiveness of PacketPatch, we utilized three publicly available datasets representing distinct application scenarios:

• <sub>ISCX-TOR dataset (TOR) (Lashkari et al., 2017) contains traf-</sub> fic generated from accessing services via the Tor network. The dataset categorizes traffic into seven service types (e.g., Browsing, Chat). From these, we selected 16 representative applications as target classes for encrypted traffic classification.

• <sub>ISCX-VPN dataset (VPN) (Draper-Gil et al., 2016) encompasses</sub> 11 distinct traffic types, including six types encapsulated through VPN tunnels and five types corresponding to non-VPN traffic accessing the same services.

• <sub>USTC dataset (USTC) (Wang et al., 2017b) focuses on network</sub> security and contains 20 traffic classes, evenly divided into 10 types of malware traffic and 10 types of benign encrypted traffic.

The detailed distribution of categories and sample counts is presented in Table 2. Note that the VPN dataset is balanced via undersampling, whereas the TOR and USTC datasets preserve their original imbalance due to the scarcity of samples in certain categories. Each dataset is partitioned into training, validation, and testing sets in an 8:1:1 ratio.

## 6.2. B-ETC models

To thoroughly assess the robustness of our method against diverse detection mechanisms, we selected five representative B-ETC models as target models:

• <sub>DeepPacket (Lotfollahi et al., 2020) is a 1D-CNN-based model</sub> that takes raw packet content as input. Each packet is padded or truncated to a unified length of 1500 bytes.

• <sub>LeNet (Zhou et al., 2017) is a classic 2D-CNN-based model</sub> adapted for traffic classification. It reshapes the first 784 bytes of a packet into a 28 × 28 grayscale image for processing.

• <sub>DataNet (Wang et al., 2018) is a lightweight MLP-based model.</sub> While the original implementation uses 1480 bytes, we normalize the input length to 1500 bytes by padding or truncation to maintain consistency with other baselines.

• <sub>TSCRNN (Lin et al., 2021) is a hybrid model that combines CNN</sub> and RNN. It processes a sequence of 15 consecutive packets, where CNN extracts intra-packet features and Bi-LSTM captures inter-packet temporal dependencies.

• <sub>ET-BERT (Lin et al., 2022) is a state-of-the-art model based</sub> on the BERT architecture. Pre-trained on large-scale unlabeled traffic data, it provides strong feature extraction capability and robustness. It uses the first 512 bytes of each packet as input.

## 6.3. Baselines

We compare PacketPatch with three baseline methods that generate adversarial perturbations while preserving packet validity. All baselines are white-box methods requiring model gradient or internal state access:

• <sub>ANT (Sadeghzadeh et al., 2021) computes class-specific Universal</sub> Adversarial Perturbations (UAP). We implement two variants, where perturbations are either appended to the end of packets (ANT-e) or injected between the header and payload (ANT-h). The perturbation budget is set to 10% of the original packet length.

• <sub>A-IOT (Kotak and Elovici, 2023) treats the first 784 bytes of</sub> a packet as a grayscale image and employs Class Activation Mapping (CAM) to identify critical bytes. It constructs adversarial packets by retaining the top 10% most important bytes and filling the remaining positions with the target payload.

• <sub>UTAA (Ding et al., 2024) learns a universal perturbation vector</sub> based on internal model activation values. The perturbation is added to the first 784 bytes of each packet, while preserving the packet header to ensure transmission validity.

Table 2  
Categories and sample counts for three encrypted traffic datasets.

<table><tr><td>Dataset</td><td>Traffic category (Sample count)</td></tr><tr><td>ISCX-TOR(16 Categories)</td><td>Facebook(20066), Imap(21000), Vuze(21000), Skype(21183), SFTP(21000), ICQ(710), Spotify(21000), Hangout(20561), Aim(620), POP(21000), Multiplespeed(21000), FTP(21000), SSL(21000), Youtube(21000), Vimeo(21000), Mam(21000)</td></tr><tr><td>ISCX-VPN(11 Categories)</td><td>Chat(3900), Email(3920), FileTransfer(3363), Streaming(3910), Voip(3036), VPN_Chat(3913), VPN_FileTransfer(3906), VPN_Email(3921), VPN_Stream(3850), VPN_Torrent(3913), VPN_Voip(3920)</td></tr><tr><td>USTC(20 Categories)</td><td>BitTorrent(5500), Facetime(3000), FTP(21000), Gmail(7490), MySQL(21000), Outlook(5487), Skype(4014), SMB(21000), Weibo(21000), WorldOfWarcraft(21000), Cridex(20999), Geodo(20811), Htbot(20999), Miuref(20999), Neris(20225), Nsis-ay(21000), Shifu(20999), Tinba(185), Virut(21451), Zeus(18642)</td></tr></table>

Among the above baselines, ANT and PacketPatch both belong to the perturbation insertion category, where additional bytes are injected into the original packet without modifying existing content. The perturbation budget of ANT is therefore set to 10% of the original packet length, consistent with PacketPatch. In contrast, A-IOT and UTAA operate on fixed-length byte regions, and their fixed-length strategies are integral to their respective method designs. Imposing a percentage-based perturbation budget on these methods would alter their operational mechanisms. All baselines are implemented following their original configurations for faithful reproduction.

## 6.4. Evaluation metrics

We report standard classification metrics: Accuracy (AC), Precision (PR), Recall (RC), and F1 Score (F1). A decrease in these metrics after perturbation indicates effective privacy protection. Additionally, we use the following specific metrics.

Defense Success Rate (DSR): This metric measures the proportion of packets successfully misclassified by the ETC model after perturbation. Let D denote the dataset, and let � ∈ D represent an original packet with $x _ { a d v }$ as its adversarial counterpart. With (⋅) denoting the classifier’s prediction, DSR is calculated as shown in Eq. (8):

$$
D S R = \frac {1}{| \mathbb {D} |} | \{x \mid \mathcal {C} (x _ {a d v}) \neq \mathcal {C} (x), x \in \mathbb {D} \} |\tag{8}
$$

Bandwidth Overhead (BWO): This metric quantifies the additional data volume introduced by the perturbation. Using ���(⋅) to denote the byte length of a packet, the overhead relative to the original packet � and the adversarial packet $x _ { a d v }$ is formulated in Eq. (9):

$$
B W O = \frac {L e n (x _ {a d v}) - L e n (x)}{L e n (x)}\tag{9}
$$

## 7. Experiments and analysis

In this section, we conduct a comprehensive experimental evaluation to validate the effectiveness and practicality of PacketPatch. The analysis is structured into three core dimensions: performance evalu ation, overhead evaluation, and usability verification. Specifically, we address the following research questions:

• <sub>RQ1 (Performance): How effective is PacketPatch in evading</sub> various ETC models across diverse data scenarios, and how does it compare with state-of-the-art baseline methods? (Section 7.1)

• <sub>RQ2 (Key Factors): How does the perturbation length influence</sub> the attack performance, and what are the distinct contributions of the perturbation vector’s individual components to the overall defense success? (Section 7.1)

• <sub>RQ3 (Overhead): What are the costs associated with PacketPatch</sub> in terms of computational latency and bandwidth consumption? (Section 7.2)

• <sub>RQ4 (Usability): Can the adversarial packets generated by the</sub> prototype system be correctly parsed and restored in real-world deployments? (Section 7.3)

## 7.1. Performance evaluation

This subsection addresses RQ1 and RQ2 and is organized into four parts. First, we evaluate the defense effectiveness of PacketPatch under the default configuration. Second, we compare PacketPatch with representative baseline methods. Third, we conduct a sensitivity analysis to examine how the perturbation length affects the defense performance. Fourth, we perform an ablation study to quantify the contributions of individual components.

## 7.1.1. Defense effectiveness analysis

We evaluate the performance of five ETC models under PacketPatch, with the detailed results reported in Table 3. The five ETC models perform consistently well across all three datasets. Most methods achieve identification accuracy exceeding 95% in the majority of scenarios, and maintain performance above 85% even under challenging conditions. However, when perturbed by PacketPatch, their performance declines to varying degrees.

The effectiveness of perturbations with identical intensity varies significantly across datasets. Notably, the TOR dataset shows a less significant decline, while the VPN and USTC datasets decline more pronouncedly. This is primarily due to differences in traffic patterns, which influence how easily a perturbation can shift inputs across the decision boundary of the identification model. Besides, the magnitude of decline varies among the different identification models. LeNet exhibits higher degrees of decline, while the ET-BERT displays a certain level of resilience to the perturbations. This can be attributed to the nature of the models. LeNet, originally designed for image classification, struggles with encrypted traffic since converting packet data into image form disrupts the inherent traffic features. In contrast, ET-BERT benefits from extensive pre-training on diverse traffic data, enabling it to form more accurate decision boundaries and generalize better across scenarios.

The notably low DSR against ET-BERT warrants further analy sis. Since PatchGenerator is derived from the ET-BERT architecture and leverages its pre-trained weights, the generated perturbations are inherently constrained within the feature manifold learned by ET-BERT. Tokens that PatchGenerator deems least probable via the arg min operation and most probable via the arg max operation are assessed through the same representational framework that ET-BERT uses for classification. This homology between the generator and the target model makes it inherently difficult for these perturbations to cross the decision boundaries of ET-BERT itself. This constitutes a known limitation of inference-based adversarial methods when the generator and the target model share the same backbone architecture. However, this constraint is of minimal concern in practical deployment, as a realworld defender typically remains agnostic to the specific classification model utilized by an adversary.

## 7.1.2. Defense effectiveness comparison

We compare PacketPatch with three white-box baseline methods, where the ANT method contains two versions. White-box methods are selected as baselines because they exploit full access to the target model’s gradients and internal structures to construct perturbations, representing the theoretical upper bound of adversarial perturbation effectiveness. Evaluating PacketPatch against this benchmark provide a rigorous validation of its perturbation generation capability under black-box conditions. The performance of each perturbation method on different datasets and identification models is shown in Table 4 It can be seen that the TOR dataset remains the most challenging to perturb, while ET-BERT models also demonstrate resistance to various white-box methods. Substantially, the effect of perturbations remains uncertain across different scenarios. For instance, the TSCRNN demonstrates robustness in some cases. In the ISCX-VPN dataset, its DSR remains low against all perturbation methods. In the USTC dataset, TSCRNN even outperforms ET-BERT when handling the ANT-h perturbation method. However, in other scenarios, such as under the UTAA model in the ISCX-TOR and USTC scenarios, TSCRNN appears more vulnerable to perturbations. These variations highlight the inherent difficulty of perturbing the byte feature of encrypted traffic. Different models exhibit substantially different decision boundaries when applied to other datasets, which leads to fluctuations in the performance of adversarial packet construction methods across scenarios.

Table 3  
Effectiveness of PacketPatch.

<table><tr><td rowspan="2">Dataset</td><td rowspan="2">ETC Models</td><td colspan="4">Without PacketPatch</td><td colspan="5">With PacketPatch</td></tr><tr><td>Acc (%)</td><td>Pre (%)</td><td>Recall (%)</td><td>F1 (%)</td><td>Acc (%)</td><td>Pre (%)</td><td>Recall (%)</td><td>F1 (%)</td><td>DSR (%)</td></tr><tr><td rowspan="5">ISCX-TOR</td><td>DeepPacket</td><td>99.71</td><td>99.71</td><td>99.71</td><td>99.71</td><td>74.68(25.04↓)</td><td>74.68(25.03↓)</td><td>82.06(17.65↓)</td><td>76.00(23.71↓)</td><td>25.33</td></tr><tr><td>LeNet</td><td>98.92</td><td>98.93</td><td>98.92</td><td>98.92</td><td>56.99(41.93↓)</td><td>60.35(38.58↓)</td><td>56.99(41.93↓)</td><td>57.02(41.90↓)</td><td>42.99</td></tr><tr><td>DataNet</td><td>98.23</td><td>98.27</td><td>98.23</td><td>98.21</td><td>73.50(24.73↓)</td><td>76.55(21.72↓)</td><td>73.50(24.73↓)</td><td>73.07(25.15↓)</td><td>26.59</td></tr><tr><td>TSCRNN</td><td>99.54</td><td>99.54</td><td>99.54</td><td>99.54</td><td>74.22(25.32↓)</td><td>82.79(16.76↓)</td><td>74.22(25.32↓)</td><td>72.81(26.73↓)</td><td>25.69</td></tr><tr><td>ET-BERT</td><td>99.84</td><td>99.86</td><td>99.84</td><td>99.84</td><td>99.19(0.65↓)</td><td>99.22(0.64↓)</td><td>99.19(0.65↓)</td><td>99.19(0.65↓)</td><td>0.66</td></tr><tr><td rowspan="5">ISCX-VPN</td><td>DeepPacket</td><td>93.87</td><td>94.44</td><td>93.87</td><td>93.85</td><td>41.14(52.73↓)</td><td>47.19(47.25↓)</td><td>41.14(52.73↓)</td><td>37.04(56.81↓)</td><td>57.37</td></tr><tr><td>LeNet</td><td>86.01</td><td>86.24</td><td>86.01</td><td>85.80</td><td>14.97(71.04↓)</td><td>15.90(70.34↓)</td><td>14.97(71.04↓)</td><td>8.03(77.78↓)</td><td>84.81</td></tr><tr><td>DataNet</td><td>85.91</td><td>86.27</td><td>85.91</td><td>85.81</td><td>27.29(58.62↓)</td><td>31.65(54.62↓)</td><td>27.29(58.62↓)</td><td>23.78(62.03↓)</td><td>70.78</td></tr><tr><td>TSCRNN</td><td>98.66</td><td>98.63</td><td>98.66</td><td>98.64</td><td>59.02(39.64↓)</td><td>56.61(42.02↓)</td><td>59.02(39.64↓)</td><td>53.38(45.25↓)</td><td>40.76</td></tr><tr><td>ET-BERT</td><td>98.00</td><td>98.02</td><td>98.00</td><td>98.00</td><td>80.53(17.47↓)</td><td>82.55(15.47↓)</td><td>80.53(17.47↓)</td><td>80.61(17.40↓)</td><td>18.99</td></tr><tr><td rowspan="5">USTC</td><td>DeepPacket</td><td>98.51</td><td>98.53</td><td>98.51</td><td>98.49</td><td>30.30(68.20↓)</td><td>46.45(52.08↓)</td><td>30.30(68.20↓)</td><td>24.25(74.24↓)</td><td>69.59</td></tr><tr><td>LeNet</td><td>92.93</td><td>93.11</td><td>92.93</td><td>92.79</td><td>13.59(79.35↓)</td><td>12.70(80.41↓)</td><td>13.59(79.35↓)</td><td>9.04(83.75↓)</td><td>86.22</td></tr><tr><td>DataNet</td><td>96.36</td><td>96.37</td><td>96.36</td><td>96.32</td><td>25.28(71.07↓)</td><td>29.13(67.24↓)</td><td>25.28(71.07↓)</td><td>16.98(79.34↓)</td><td>73.99</td></tr><tr><td>TSCRNN</td><td>97.73</td><td>97.83</td><td>97.73</td><td>97.74</td><td>4.85(92.89↓)</td><td>4.21(93.63↓)</td><td>4.85(92.89↓)</td><td>2.23(95.51↓)</td><td>95.25</td></tr><tr><td>ET-BERT</td><td>98.72</td><td>98.68</td><td>98.72</td><td>98.68</td><td>51.25(47.46↓)</td><td>68.86(29.82↓)</td><td>51.25(47.46↓)</td><td>46.52(52.17↓)</td><td>48.15</td></tr></table>

Table 4  
Comparison between PacketPatch and other baseline methods.

<table><tr><td rowspan="2">Dataset</td><td rowspan="2">ETC Models</td><td colspan="2">ANT-e</td><td colspan="2">ANT-h</td><td colspan="2">A-IOT</td><td colspan="2">UTAA</td><td colspan="2">PacketPatch</td></tr><tr><td>Acc (%)</td><td>DSR (%)</td><td>Acc (%)</td><td>DSR (%)</td><td>Acc (%)</td><td>DSR (%)</td><td>Acc (%)</td><td>DSR (%)</td><td>Acc (%)</td><td>DSR (%)</td></tr><tr><td rowspan="5">ISCX-TOR</td><td>DeepPacket</td><td>97.59</td><td>2.16</td><td>68.32</td><td>31.57</td><td>72.05</td><td>28.00</td><td>79.25</td><td>20.83</td><td>74.68</td><td>25.33</td></tr><tr><td>LeNet</td><td>97.84</td><td>1.39</td><td>84.47</td><td>15.46</td><td>74.05</td><td>25.67</td><td>81.72</td><td>18.39</td><td>56.99</td><td>42.99</td></tr><tr><td>DataNet</td><td>84.41</td><td>14.48</td><td>72.18</td><td>27.01</td><td>66.23</td><td>33.71</td><td>56.09</td><td>43.80</td><td>73.50</td><td>26.59</td></tr><tr><td>TSCRNN</td><td>82.13</td><td>17.72</td><td>66.06</td><td>33.89</td><td>91.17</td><td>8.76</td><td>52.74</td><td>47.09</td><td>74.22</td><td>25.69</td></tr><tr><td>ET-BERT</td><td>99.84</td><td>0.00</td><td>99.84</td><td>0.00</td><td>99.34</td><td>0.51</td><td>99.84</td><td>0.00</td><td>99.19</td><td>0.66</td></tr><tr><td rowspan="5">ISCX-VPN</td><td>DeepPacket</td><td>58.11</td><td>38.63</td><td>36.84</td><td>61.63</td><td>33.54</td><td>66.11</td><td>59.38</td><td>40.75</td><td>41.14</td><td>57.37</td></tr><tr><td>LeNet</td><td>78.37</td><td>16.04</td><td>37.82</td><td>60.13</td><td>45.68</td><td>53.98</td><td>14.97</td><td>84.81</td><td>14.60</td><td>85.88</td></tr><tr><td>DataNet</td><td>59.33</td><td>33.65</td><td>39.45</td><td>58.40</td><td>36.16</td><td>61.32</td><td>45.56</td><td>56.08</td><td>27.29</td><td>70.78</td></tr><tr><td>TSCRNN</td><td>77.35</td><td>22.23</td><td>70.57</td><td>29.16</td><td>73.63</td><td>26.19</td><td>63.09</td><td>36.86</td><td>59.02</td><td>40.76</td></tr><tr><td>ET-BERT</td><td>97.28</td><td>0.77</td><td>72.73</td><td>27.00</td><td>88.09</td><td>11.72</td><td>65.39</td><td>34.34</td><td>80.53</td><td>18.99</td></tr><tr><td rowspan="5">USTC</td><td>DeepPacket</td><td>74.37</td><td>24.67</td><td>30.50</td><td>69.32</td><td>47.69</td><td>52.21</td><td>27.93</td><td>71.62</td><td>30.30</td><td>69.59</td></tr><tr><td>LeNet</td><td>78.91</td><td>16.62</td><td>30.40</td><td>67.95</td><td>43.84</td><td>53.78</td><td>12.12</td><td>86.70</td><td>13.59</td><td>86.22</td></tr><tr><td>DataNet</td><td>75.89</td><td>22.04</td><td>34.93</td><td>64.82</td><td>57.36</td><td>42.13</td><td>18.40</td><td>81.47</td><td>25.28</td><td>73.99</td></tr><tr><td>TSCRNN</td><td>68.91</td><td>30.51</td><td>75.72</td><td>23.34</td><td>38.17</td><td>61.56</td><td>8.83</td><td>91.22</td><td>4.85</td><td>95.25</td></tr><tr><td>ET-BERT</td><td>73.68</td><td>25.75</td><td>62.54</td><td>37.04</td><td>75.68</td><td>23.71</td><td>33.09</td><td>66.77</td><td>51.25</td><td>48.15</td></tr></table>

UTAA has the optimal perturbation effect in each scenario because its perturbation surface is the widest, with perturbation vectors added to the first 784 bytes, except for the packet header. However, all other methods choose to insert perturbation vectors at specific positions in the packet, and the original bytes of the packet are not changed, which allows the identification model to still obtain relevant features from the original bytes of the packet.

For a total of 15 scenarios with 5 identification models across, 3 datasets. PacketPatch ranks second in terms of the number of times it achieves optimal perturbation effects in each scenario. It leads ANTe in 15 scenarios, ANT-h in 10 scenarios, A-IOT in 12 scenarios, and

UTAA in 8 scenarios, outperforming these white-box methods. These findings demonstrate that PacketPatch, without access to any target model information, can match or exceed the theoretical upper bounds represented by white-box methods in the majority of scenarios.

## 7.1.3. Perturbation length analysis

Section 4.5 details the rationale behind the length selection of perturbation vectors under the default configuration of PacketPatch from the perspective of method design. This subsection further verifies the rationality of this selection from an experimental perspective. Specifically, we assume that the attacker employs DeepPacket as the ETC model. The random packet header $h _ { r }$ is retained in the perturbation vector, and the total length of $P a d _ { 1 }$ and $P a d _ { 2 }$ is varied from 0% to 12% of the original packet size. This setup allows us to observe how the length of the perturbation affects attack performance across different datasets.

As shown in Fig. 7, it can be seen that as the length of the pertur bation vector increases, the identification accuracy gradually decreases in each data scenario, and the perturbation effect gradually increases. When the filling length increases from 8% to 12%, the growth of perturbation effects in various scenarios tends to flatten out. This is because the total length of $P a d _ { 1 }$ and $P a d _ { 2 }$ is close to the maximum number of [mask] symbols during training, approaching the limit of PacketPatch generating perturbation vectors. If a longer perturbation vector is needed, the input length of PacketPatch should be expanded to add more reference information to ensure the effectiveness of the perturbation vector. This result validates the rationality of the perturbation vector length selection under the default configuration of PacketPatch.

Table 5  
The ablation experiment of PacketPatch.

<table><tr><td rowspan="2">Method</td><td colspan="3">Component</td><td colspan="2">TOR</td><td colspan="2">VPN</td><td colspan="2">USTC</td></tr><tr><td> $Pad_1$ </td><td> $h_r$ </td><td> $Pad_2$ </td><td>Acc (%)</td><td>DSR (%)</td><td>Acc (%)</td><td>DSR (%)</td><td>Acc (%)</td><td>DSR (%)</td></tr><tr><td>PacketPatch</td><td>✓</td><td>✓</td><td>✓</td><td>74.68</td><td>25.33</td><td>41.14</td><td>57.37</td><td>30.30</td><td>69.59</td></tr><tr><td> $\mathcal{W}^1$ </td><td>✓</td><td>✓</td><td>✓</td><td>74.38</td><td>25.63</td><td>42.77</td><td>55.25</td><td>30.14</td><td>69.76</td></tr><tr><td> $\mathcal{W}^2$ </td><td>✓</td><td>✓</td><td>×</td><td>91.21</td><td>8.82</td><td>40.28</td><td>57.93</td><td>29.97</td><td>69.90</td></tr><tr><td> $\mathcal{W}^3$ </td><td>×</td><td>✓</td><td>✓</td><td>69.43</td><td>30.53</td><td>42.82</td><td>54.86</td><td>36.41</td><td>63.36</td></tr><tr><td> $\mathcal{W}^4$ </td><td>✓</td><td>×</td><td>✓</td><td>90.92</td><td>9.07</td><td>50.78</td><td>46.07</td><td>49.14</td><td>50.63</td></tr><tr><td> $\mathcal{W}^5$ </td><td>✓</td><td>×</td><td>×</td><td>91.21</td><td>8.82</td><td>40.65</td><td>57.59</td><td>29.97</td><td>69.90</td></tr><tr><td> $\mathcal{W}^6$ </td><td>×</td><td>×</td><td>✓</td><td>74.75</td><td>25.20</td><td>51.42</td><td>45.36</td><td>57.91</td><td>41.74</td></tr><tr><td> $\mathcal{W}^7$ </td><td>×</td><td>✓</td><td>×</td><td>96.68</td><td>3.36</td><td>46.44</td><td>51.98</td><td>37.08</td><td>62.67</td></tr></table>

![](images/e397bafd7b6ab446e3d98488fffe6714784798ac1398a5f8e9257efd0f47143a.jpg)  
Fig. 7. The impact of PacketPatch with varying perturbation lengths.

## 7.1.4. Ablation study

The perturbation vector generated by PacketPatch comprises three components: the model-generated segments $P a d _ { 1 }$ and $P a d _ { 2 }$ , separated by an intervening random packet header $h _ { r }$ . The combined length of $P a d _ { 1 }$ and $P a d _ { 2 }$ is set to 10% of the original packet length, and $h _ { r }$ is a fixed 40-byte real packet header from a random traffic category. To enhance perturbation diversity, the insertion position of this random header is randomized for each instance.

To systematically analyze the contribution of each component, we select DeepPacket as the target ETC model for the ablation study. DeepPacket adopts a 1D-CNN architecture, which is fundamentally different from the BERT-based PatchGenerator and shares no common representations or pre-trained weights. This setting enables a more objective examination of the perturbation mechanism itself, rather than effects that may arise from architectural alignment.

We design seven ablation variants to analyze the contributions of each component from three perspectives: $\mathcal { W } ^ { 1 }$ examines the length allocation strategy between $P a d _ { 1 }$ and $P a d _ { 2 } ; \mathcal { W } ^ { 2 }$ through $\mathcal { W } ^ { 6 }$ selectively remove individual components to assess their independent contributions and interactions: and $\mathcal { W } ^ { 7 }$ examines the perturbation capability of $h _ { r }$ in isolation. The detailed configuration of each variant is as follows:

$\mathcal { W } ^ { 1 } \bar { : }$ : All three components are retained, and the total perturbation vector length is equal to the default configuration. Unlike the default configuration where $P a d _ { 1 }$ and $P a d _ { 2 }$ are randomly assigned their respective lengths, $h _ { r }$ divides $P a d _ { 1 }$ and $P a d _ { 2 }$ equally to ensure their lengths are identical.

$\mathscr { W } ^ { 2 } \colon P a d _ { 2 }$ is removed by setting its length to zero. $P a d _ { 1 }$ and $h _ { r }$ are retained, and the total perturbation vector length remains equal to the default configuration.

$\mathcal { W } ^ { 3 } \colon P a d _ { 1 }$ is removed by setting its length to zero. $h _ { r }$ and $P a d _ { 2 }$ are retained, and the total perturbation vector length remains equal to the default configuration.

$ { \mathcal { W } ^ { 4 } } : h _ { r }$ is removed, and the perturbation vector consists of $P a d _ { 1 }$ and $P a d _ { 2 }$ only. The perturbation vector length is 10% of the original packet length.

• $w ^ { 5 } ;$ : Only $P a d _ { 1 }$ is retained, with the perturbation vector length set to 10% of the original packet length.

$\mathcal { W } ^ { 6 } \colon$ Only $P a d _ { 2 }$ is retained, with the perturbation vector length set to 10% of the original packet length, the same as $\mathcal { W } ^ { 4 }$ and $\mathcal { W } ^ { 5 }$

$w ? { \mathrm { : } }$ Only the random header $h _ { r }$ is used as the perturbation vector, with a fixed length of 40 bytes.

The results are shown in Table 5. Regarding the individual contrib f $P a d _ { 1 }$ and $P a d _ { 2 } ,$ , comparisons between $\mathcal { W } ^ { 2 }$ and $\mathcal { W } ^ { 3 }$ alongside comparisons between $\mathcal { W } ^ { 5 }$ and $\mathcal { W } ^ { 6 }$ reveal a clear divergence: $P a d _ { 2 }$ contributes more significantly to perturbation effectiveness in the ISCX-TOR dataset, whereas $P a d _ { 1 }$ demonstrates greater impact in the ISCX-VPN and USTC datasets. This discrepancy is attributable to the structure of the perturbation vector: $P a d _ { 1 }$ is separated from $h _ { r }$ by a [SEP] token, which causes the PatchGenerator to treat them as independent, resulting in a lack of semantic correlation between $P a d _ { 1 }$ and the header. Conversely, $P a d _ { 2 }$ d b d b h h d header and the original payload, establishing a strong feature dependency. Consequently, the relative dominance of these two components varies across data scenarios, reflecting the scenario-dependent nature of the perturbation effect.

We further examine the role of $h _ { r }$ . Observations from $\mathcal { W } ^ { 7 }$ indicate that randomly selected packet headers alone can perturb packet byte features to some extent, although their effectiveness is limited in the ISCX-TOR dataset. Comparisons between $\mathcal { W } ^ { 1 }$ and $\mathcal { W } ^ { 4 }$ confirm that $h _ { r }$ contributes meaningfully to the overall perturbation vector. Further analysis comparing $\mathcal { W } ^ { 5 }$ with $\mathcal { W } ^ { 2 }$ reveals that adding ℎ to $P a d _ { 1 }$ leads to minimal improvement, suggesting weak feature correlation. In contrast, the comparison between $\mathcal { W } ^ { 6 }$ and $\mathcal { W } ^ { 3 }$ demonstrates that adding $h _ { r }$ to $P a d _ { 2 }$ results in a substantial boost in perturbation effectiveness. This finding further confirms the structural linkage between $P a d _ { 2 }$ and $h _ { r } ,$ which significantly enhances the overall perturbation effect.

It is also important to address why the default configuration of PacketPatch does not achieve the highest DSR in any individual scenario. As analyzed above, the optimal component varies by scenario: $P a d _ { 2 }$ dominates in ISCX-TOR, while $P a d _ { 1 }$ is more effective in ISCX-VPN and USTC. Consequently, specialized variants such as $\mathcal { W } ^ { 3 }$ , which excludes $P a d _ { 1 } ,$ and $\mathcal { W } ^ { 2 }$ , which excludes $P a d _ { 2 } ,$ , achieve the highest DSRs in their respective favorable scenarios, reaching 30.53% on the TOR dataset and 57.93% and 69.90% on the VPN and USTC datasets, respectively. Since the default configuration distributes the perturbation budget across both $P a d _ { 1 }$ and $P a d _ { 2 }$ via random allocation, it inevitably allocates some capacity to the less effective component in each specific scenario, resulting in slightly suboptimal performance compared to the scenario-specific best variant. Nevertheless, the default configuration consistently maintains competitive performance across all three datasets with DSR values of 25.33%, 57.37%, and 69.59%, closely approaching the scenario-specific optima. Moreover, compared with $\mathcal { W } ^ { 1 }$ which employs equal division, the default random allocation achieves notably better performance on the ISCX-VPN dataset, surpassing the 55.25% accuracy of $\mathcal { W } ^ { 1 }$ with 57.37%. This suggests that stochastic length variation introduces beneficial perturbation diversity. These observations demonstrate that the default configuration offers a robust and balanced trade-off between generality and effectiveness. When the deployment environment is uncertain, this configuration serves as a reliable general-purpose strategy. However, if the maximum perturbation effect is desired for a specific target, the components can be adaptively configured to suit the traffic characteristics and identification models.

Table 6  
The time consumption of PacketPatch.

<table><tr><td>Perturbation stage</td><td>Time consumption (ms/packet)</td></tr><tr><td>Packet Preprocessing</td><td>0.054</td></tr><tr><td>Perturbation Generation</td><td>9.626</td></tr><tr><td>Packet Reconstruction</td><td>0.398</td></tr><tr><td>Total</td><td>10.078</td></tr></table>

Although the ablation study is conducted on a single target model, the observed trends are mainly determined by the construction of the perturbation vector and the generation process of PatchGenerator, rather than being specific to DeepPacket. Specifically, $P a d _ { 1 }$ is generated under the original header context and tends to introduce feature deviations from the original packet representation, while $P a d _ { 2 }$ is generated conditioned on both the random header and the original payload, leading to stronger feature dependency. As these behaviors arise from how the perturbation is constructed and generated, similar relative trends are expected when applied to other target models, although the overall perturbation strength may vary depending on model sensitivity.

## 7.2. Overhead evaluation

This subsection answers RQ3. We first evaluate the time efficiency of PacketPatch by reporting its time consumption. Subsequently, we quantify the bandwidth overhead and compare these costs against representative baseline methods.

## 7.2.1. Time efficiency analysis

We separately calculate the time consumption for each stage of the PacketPatch application process, which is divided into three phases: (1) packet preprocessing, where the system processes the packet into the model input format; (2) perturbation vector generation, where the PatchGenerator performs a single forward pass (with the batch size set to 1 to measure per-sample latency); and (3) adversarial packet construction, where the perturbation vector is inserted into the target packet and the relevant header fields are updated.

As shown in Table 6, the time consumption of PacketPatch mainly occurs during the perturbation vector generation stage, which necessitates a model forward pass. Overall, constructing an adversarial packet using PacketPatch incurs an average latency of approximately 10 ms, demonstrating its feasibility for real-time applications.

## 7.2.2. Bandwidth overhead analysis

We compare the actual bandwidth consumption of various methods across different datasets, as illustrated in Fig. 8. The two versions of ANT exhibit identical BWO. In contrast, A-IOT demonstrates sig nificantly higher BWO than other methods, as it mandates padding packets to a fixed template length regardless of the original packet size. Similarly, UTAA requires padding smaller packets to a fixed size of 784 bytes. PacketPatch incurs a slightly higher BWO than ANT, which is attributable to the inclusion of an additional packet header in its perturbation vector.

Overall, PacketPatch achieves comparable or superior perturbation effects relative to the three white-box baselines, even under black-box assumptions. Furthermore, it effectively balances perturbation effec tiveness with bandwidth overhead.

![](images/424c0ddc76276aebb9798ada8e3b94e3deda96f8b45c3b439f927001e28b51ae.jpg)  
Fig. 8. BWO of various methods under different datasets.

![](images/cf2d0cf1b360c5dfb079369c072556ff970cfbb3a242b0d9c780d66c16fdd03b.jpg)  
Fig. 9. The architecture and deployment of the PacketPatch prototype system.

## 7.3. Usability verification

This subsection answers RQ4. Prototype system deployment presents the end-to-end prototype system and evaluation setting, and Packet Usability Verification demonstrates parsability and restorability with a packet-level example.

## 7.3.1. Prototype system deployment

To strictly verify the practical usability and restorability of adversarial packets in a real-world network environment, we instantiate the symmetric proxy architecture described in Section 5. As illustrated in Fig. 9, the experimental testbed comprises three distinct physical nodes: the user-side device, the server-side proxy, and the application server, all interconnected within a high-speed local area network (LAN).

The specific hardware and software configurations for each node are detailed in Table 7. The user-side device is equipped with a highperformance NVIDIA GeForce RTX 3080 GPU to support the real-time inference requirements of the PacketPatch module. The server-side proxy is deployed on a separate workstation with an RTX 2060 GPU to handle the removal of perturbations. The application server hosts a custom remote computing service on an Ubuntu environment to process user requests.

The network topology is configured to simulate a complete end-toend communication link, as illustrated by the following IP and port configurations:

• <sub>The user-side device (IP: 192.168.1.251) runs the client proxy,</sub> which listens on the local loopback port 1080. It intercept outbound connection requests and encapsulates them with adversarial perturbations.

Table 7  
Hardware and software configuration of the prototype system.

<table><tr><td>Device</td><td>Component</td><td>Specification</td></tr><tr><td rowspan="5">User-Side Device</td><td>OS</td><td>Windows 11 Home</td></tr><tr><td>CPU</td><td>Intel(R) Core(TM) i9-12900 CPU @ 3.19 GHz</td></tr><tr><td>Memory</td><td>64.0 GB</td></tr><tr><td>GPU (VRAM)</td><td>NVIDIA GeForce RTX 3080 (10 GB)</td></tr><tr><td>Network</td><td>Intel Wi-Fi 6 AX201 160MHz</td></tr><tr><td rowspan="5">Server-Side Proxy</td><td>OS</td><td>Windows 10 Pro</td></tr><tr><td>CPU</td><td>Intel(R) Core(TM) i9-10900 CPU @ 2.80 GHz</td></tr><tr><td>Memory</td><td>32.0 GB</td></tr><tr><td>GPU (VRAM)</td><td>NVIDIA GeForce RTX 2060 (6 GB)</td></tr><tr><td>Network</td><td>Intel(R) Wi-Fi 6 AX200 160MHz</td></tr><tr><td rowspan="4">Application Server</td><td>OS</td><td>Ubuntu 22.04 LTS</td></tr><tr><td>CPU</td><td>Intel Core i5-10500T @ 2.3 GHz</td></tr><tr><td>Memory</td><td>8.0 GB</td></tr><tr><td>Network</td><td>Comfast CF-952AX WIFI6 USB</td></tr></table>

• <sub>The traffic is forwarded to the server-side proxy (IP:</sub> 192.168.1.250), which listens on port 1081. This node is responsible for boundary detection and perturbation stripping.

• <sub>Upon restoration, the clean payload is forwarded to the applica</sub> tion server (IP: 192.168.1.252), where the remote computing service listens on port 12345.

To definitively answer RQ4, we design a rigorous verification protocol using the deployed remote computing service. The client application sends 1000 continuous mathematical calculation problems to the appli cation server, with random transmission intervals ranging from 0.5 ms to 5 ms.

In this experiment, the successful receipt of correct calculation answers by the client serves as the ground truth for validating usability. This metric implies two critical outcomes:

• <sub>Parsability: The adversarial packets successfully traverse the net-</sub> work stack and are correctly parsed by the server-side proxy, proving that the injected headers and delimiters comply with protocol standards.

• <sub>Restorability: The server-side proxy successfully identifies the per-</sub> turbation boundaries and restores the original payload to its bit-perfect state. Any error in restoration results in an incorrect calculation answer or a service timeout.

The experimental results confirm a 100% success rate for the 1000 calculation tasks, thereby validating that the adversarial packets generated by the prototype system satisfy the strict correctness requirements of real-world deployments.

## 7.3.2. Packet usability verification

Fig. 10 illustrates the generation of an adversarial packet using PacketPatch. As shown in Fig. 10(a), the original packet size is 584 bytes. Fig. 10(b) displays the generated perturbation vector of 98 bytes, which comprises 58 bytes generated by PacketPatch and a 40-byte ℎ (separated by red dashed lines).

The perturbation vectors are inserted between the header and the payload of the original packet. After inserting the perturbation vectors, critical fields in the original packet are recalculated, including the packet length in the IP header, the IP header checksum, and the checksum of the entire packet in the TCP header. This ensures that the receiver can calculate the original length of the packet upon receiving it and remove the added perturbation vectors, facilitating correct parsing and restoration.

## 8. Conclusion

This study focuses on the generation and deployment of adversarial packets for B-ETC to effectively avert privacy violations linked to user network traffic. In response to the deficiencies identified in existing research, we present PacketPatch, a practical approach for generating and deploying adversarial packets aimed at B-ETC Models. To avoid setting unrealistic preconditions, we design PatchGenerator, a BERTbased perturbation vector generator that operates under a black-box assumption. It produces perturbations from original packets and random header data without requiring access to model gradients or user behavior history. To reduce time and bandwidth overhead, PatchGener ator produces perturbations with a single forward pass and dynamically varies the number of masked bytes based on the packet size, effectively managing the length of the perturbation. To ensure packet usability, we further propose a symmetric proxy-based deployment method. By strategically placing the perturbation vector at the boundary between the packet header and payload, while also updating the relevant protocol fields, adversarial packets can successfully pass integrity checks and be seamlessly restored at the receiving end.

![](images/2b4703fba7ee5f19df46f4d8058897394971246d3caf3e66a54917ea70222370.jpg)  
(b) Packet perturbed by PacketPatch  
Fig. 10. An example of a packet perturbed by PacketPatch.

To validate PacketPatch, we rigorously tested its effectiveness in defense against five B-ETC models across three datasets. It outperforms four leading white-box baselines in most scenarios while maintaining a strict black-box approach. Its average perturbation vector generation time is just 10.078 ms, with much lower bandwidth overhead compared to template-filling methods. Furthermore, we built a prototype system and deploved PacketPatch on it. The test results indicate that Packet-Patch could bypass B-ETC models and successfully recover the original information at the receiving end. Our future studies will investigate innovative approaches to the generation of general adversarial packets and the frameworks for their deployment. By generating a common perturbation vector for packets belonging to the same category, we hope to cut down the generator’s resource use while keeping our defense effectiveness.

## CRediT authorship contribution statement

Yuwei Xu: Writing – review & editing, Supervision, Resources, Project administration, Conceptualization. Yuanyuan Xu: Writing – review & editing, Writing – original draft, Visualization, Validation, Investigation, Formal analysis. Yunpeng Bai: Writing – original draft, Software, Methodology, Formal analysis, Data curation. Jiahui Chen: Writing – review & editing, Validation. Kehui Song: Writing – review & editing, Visualization. Jie Cao: Writing – review & editing, Validation. Qiao Xiang: Writing – review & editing, Validation. Guang Cheng: Writing – review & editing, Validation.

## Declaration of competing interest

The authors declare that they have no known competing finan cial interests or personal relationships that could have appeared to influence the work reported in this paper.

## Acknowledgments

This work was supported in part by the CCF-NSFOCUS ’Kunpeng’ Research Fund, China under Grant No. CCF-NSFOCUS 2024010, in part by the National Key R&D Program of China under Grant No. 2023YFB3106700, and in part by the National Natural Science Foun dation of China under Grant Nos. 62172093 and U22B2025.

## Data availability

Data will be made available on request.

## References

Aceto, G., Ciuonzo, D., Montieri, A., Pescapé, A., 2019. Mobile encrypted traffic classification using deep learning: Experimental evaluation, lessons learned, and challenges. IEEE Trans. Netw. Serv. Manag. 16 (2), 445–458.

Aouedi, O., Le, V.A., Piamrat, K., Ji, Y., 2025. Deep learning on network traffic prediction: Recent advances, analysis, and future directions. ACM Comput. Surv. 57 (6).

Cao, J., Xu, Z., Bai, Y., et al., 2024. Perturbing vulnerable bytes in packets to generate adversarial samples resisting DNN-based traffic monitoring. In: Proceedings of the 23rd IEEE International Conference on Trust, Security and Privacy in Computing and Communications, TrustCom. IEEE, pp. 1015–1021.

Cheng, J., Wu, Y., E, Y., et al., 2021. MATEC: A lightweight neural network for online encrypted traffic classification. Comput. Netw. 199, 108472.

Dai, X., Liang, K., Xiao, B., 2024. Advdiff: Generating unrestricted adversarial examples using diffusion models. In: Proceedings of the 18th European Conference on Computer Vision. ECCV, Springer, pp. 93–109.

Devlin, J., Chang, M.-W., Lee, K., Toutanova, K., 2019. Bert: Pre-training of deep bidirectional transformers for language understanding. In: Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, NAACL-HLT. pp. 4171–4186.

Ding, R., Sun, L., Zang, W., et al., 2024. Towards universal and transferable adversarial attacks against network traffic classification. Comput. Netw. 254, 110790.

Ding, Y., Zhu, G., Chen, D., et al., 2022. Adversarial sample attack and defense method for encrypted traffic data. JEEE Trans. Intell. Transp. Syst. 23 (10). 18024–18039

Dong, W., Yu, J., Lin, X., et al., 2025. Deep learning and pre-training technology for encrypted traffic classification: A comprehensive review. Neurocomputing 617, 128444.

Draper-Gil, G., Lashkari, A.H., Mamun, M.S.I., Ghorbani, A.A., 2016. Characterization of encrypted and vpn traffic using time-related. In: Proceedings of the 2nd International Conference on Information Systems Security and Privacy. ICISSP, pp. 407-414.

He, H., Yang, Z., Chen, X., 2020. PERT: Payload encoding representation from transformer for encrypted traffic classification. In: Proceedings of the 12th ITI Kaleidoscope Academic Conference, ITU K. IEEE, pp. 1–8.

Hore, S., Ghadermazi, J., Paudel, D., et al., 2025. Deep packgen: A deep reinforcement learning framework for adversarial network packet generation, ACM Trans. Priv Secur. 28 (2), 1–33.

Hu, X., Zhu, C., Cheng, G., et al., 2023. A deep subdomain adaptation network with attention mechanism for malware variant traffic identification at an IoT edge gateway. IEEE Internet Things J. 10 (5), 3814–3826.

Kotak, J., Elovici, Y., 2023. Adversarial attacks against IoT identification systems. IEEE Internet Things J. 10 (9), 7868–7883.

Lashkari, A.H., Gil, G.D., Mamun, M.S.I., Ghorbani, A.A., 2017. Characterization of tor traffic using time based features. ICISSP. In: Proceedings of the 3rd Internationa Conference on Information Systems Security and Privacy, vol. 2, pp. 253–262.

Lin, X., Xiong, G., Gou, G., et al., 2022. ET-BERT: A contextualized datagram representation with pre-training transformers for encrypted traffic classification. In: Proceedings of the 31st ACM Web Conference. WWW, pp. 633–642

Lin, K., Xu, X., Gao, H., 2021. TSCRNN: A novel classification scheme of encrypted traffic based on flow spatiotemporal features for efficient mana ement of IIoT. Comput. Netw. 190, 107974.

Lotfollahi, M., Jafari Siavoshani, M., Shirali Hossein Zade, R., Saberian, M., 2020. Deep packet: A novel approach for encrypted traffic classification using deep learning. Soft Comput. 24 (3), 1999–2012.

Papadogiannaki, E., Ioannidis, S., 2021. A survey on encrypted network traffic analysis applications, techniques, and countermeasures. ACM Comput. Surv. 54 (6), 1–35.

Sadeghzadeh, A.M., Shiravi, S., Jalili, R., 2021. Adversarial network traffic: Towards evaluating the robustness of deep-learning-based network traffic classification. IEEE Trans. Netw, Sery, Manag, 18 (2), 1962–1976.

Sharma, A., Lashkari, A.H., 2025. A survey on encrypted network traffic: A comprehensive survey of identification/classification techniques, challenges, and future directions. Comput. Netw. 257, 110984.

Shen, M., Ye, K., Liu, X., et al., 2022. Machine learning-powered encrypted network traffic analysis: A comprehensive survey. IEEE Commun. Surv. Tutor. 25 (1), 791–824.

Sun, P., Yun, X., Li, S., et al., 2025. AdvTG: An adversarial traffic generation framework to deceive DL-based malicious traffic detection models. In: Proceedings of the 34th ACM Web Conference. WWW, ACM, pp. 3147–3159.

Wang, P., Ye, F., Chen, X., Qian, Y., 2018. Datanet: Deep learning based encrypted network traffic classification in sdn home gateway. JEEE Access 6. 55380–55391.

Wang, W., Zhu, M., Wang, J., et al., 2017a. End-to-end encrypted traffic classification with one-dimensional convolution neural networks. In: Proc. of the 15th JEEE International Conference on Intelligence and Security Informatics. ISI, IEEE, pp. 43–48.

Wang, W., Zhu, M., Zeng, X., et al., 2017b. Malware traffic classification using convolutional neural network for representation learning. In: Proceedings of the 31st International Conference on Information Networking. ICOIN. JEEE. pp. 712–717.

Wu, H., Liu, Y., Cheng, G., Hu, X., 2023. RT-CBCH: Real-time VPN traffic service identification based on sampled data in high-speed networks. IEEE Trans. Netw. Sery, Manag, 21 (1), 88–107.

Ye, M., Chen, J., Miao, C., et al., 2023. PAT: Geometry-aware hard-label black-box adversarial attacks on text. In: Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. SIGKDD, pp. 3093–3104.

Zhang, X., Zhou, Y., Pei, S., et al., 2020, Adversarial examples detection for XSS attacks based on generative adversarial networks. JEEE Access 8. 10989–10996

Zhou, Y., Shi, H., Zhao, Y., et al., 2021. Encrypted network traffic identification based on 2d-CNN model. In: Proceedings of the 22nd Asia-Pacific Network Operations and Management Symposium. APNOMS, IEEE, pp. 238–241.

Zhou, H., Wang, Y., Lei, X., Liu, Y., 2017. A method of improved CNN traffic classification. In: Proceedings of the 13th International Conference on Computationa Intelligence and Security. CIS. pp. 177–181.

Zhu, S., Xu, X., Gao, H., Xiao, F., 2023. CMTSNN: A deep learning model for multiclassification of abnormal and encrypted traffic of internet of things. IEEE Internet Things J. 10 (13) 11773–11791
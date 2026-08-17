# LitCVit: A Lightweight Self-Supervised Contrastive Vision Transformer for Encrypted Malicious Trafic Detection

Mehr Un Nisa, Adnan Noor Mian , Senior Member, IEEE, and Mubashir Husain Rehmani , Senior Member, IEEE

Abstract—Malicious trafic detection often requires large, labeled datasets, which are challenging due to privacy concerns, labeling costs, and evolving threat patterns. Although recent self-supervised pretraining methods address this issue, they rely on complex transformer-based architectures that are computationally expensive and have high inference times, making them unsuitable for real-time use. In addition, most existing approaches process packets or flows independently, and often rely on per-packet dataset splits that introduce implicit flowlevel data leakage, thereby limiting their ability to capture meaningful semantic and behavioral relationships across flows for detecting stealthy encrypted threats. To address these issues, we propose LitCVit, a lightweight self-supervised contrastive Vision Transformer-based framework that captures cross-flow semantic and behavioral patterns to generate robust latent representations of encrypted trafic. Without relying on decryption or manually engineered features, our method enables eficient detection of encrypted malicious flows with low inference time. Extensive evaluations on benchmark datasets demonstrate that the proposed framework achieves an average detection accuracy of 98.10% and F1-score of 98.08%. Compared to the best state-of-the-art model, LitCVit achieves an average improvement of 2.49% in F1-score, 2.12% in precision, and 2.50% in recall, highlighting its superior detection capability in encrypted trafic scenarios. Additionally, LitCVit achieves an 8 7× reduction in inference time compared to the best existing self-supervised approach, making it highly suitable for deployment on resource-constrained devices.

Index Terms—Encrypted malicious trafic, self-supervised malicious trafic detection, pre-training models, contrastive learning, malware or attack classification.

## I. INTRODUCTION

HE rapid proliferation of encrypted trafic has not only T enhanced user security and privacy but also created new opportunities for adversaries to conceal malicious activities within encrypted payloads, facilitating sophisticated attacks such as command-and-control (C2). In parallel, the rise of cyber-physical systems and the Internet of Things (IoT)

has further expanded the threat landscape, as cybercriminals increasingly exploit these encrypted channels to launch persistent and evasive attacks, efectively bypassing conventional defenses [1]. Additionally, advancements in encryption protocols, such as TLS 1.3 and DNS over HTTPS, have reduced the availability of previously accessible metadata [2]. These trends emphasize the urgent need for robust and eficient detection techniques to identify malicious patterns within encrypted network trafic.

Artificial intelligence (AI)-based techniques have emerged as an efective alternative to rule-based and signature-based methods for detecting encrypted malicious trafic [3]. Most of these methods rely on manually engineered features extracted from protocol headers, flow, or handshake metadata to identify malicious patterns. However, these methods provide limited visibility into fine-grained encrypted network trafic, leading to higher false alarm rates (FAR), challenges in high-speed trafic processing, and poor generalization across diverse network conditions [4].

End-to-end deep learning methods address the limitations of manual feature engineering by automatically learning relevant features from raw data. However, they require large volumes of labeled data for efective training to achieve satisfactory performance. Acquiring and labeling such data across diverse network environments is a time-consuming and resourceintensive process, often introducing significant security and privacy risks [5]. Self-supervised approaches have emerged to address these challenges by leveraging large volumes of unlabeled data for pretraining. These methods reduce the reliance on labeled datasets and improve generalization across diverse network environments. However, they have complex transformer-based architectures [6], [7], [8], [9] which are unsuitable for real-time intrusion detection due to high computational and latency requirements. Additionally, most techniques process packets independently and adopt per-packet data splits [6], [10], [11], which introduce implicit flow-level data leakage [9] and fail to capture meaningful semantic and behavioral relationships across flows necessary for detecting sophisticated threats.

In this paper, we propose LitCVit, a lightweight contrastive Vision Transformer-based framework, for encrypted malicious trafic detection. Our core idea is to eficiently capture features from raw encrypted trafic at both fine and coarse grained levels through a hierarchy of lightweight encoder blocks.

Moreover, we model semantic and behavioral relationships across flows by clustering semantically similar trafic patterns through contrastive representation learning, aligning flows with similar behaviors in the latent space rather than modeling explicit causal interactions. This enables the model to learn compact and discriminative representations of encrypted trafic flows without requiring large labeled datasets. To enhance computational eficiency, we propose a simple yet efective lightweight architecture that replaces traditional heavy transformer designs, significantly reducing complexity and memory overhead while preserving critical trafic features.

The proposed design significantly reduces trainable parameters (0.658 million) and inference latency (2.32 milliseconds) while preserving strong detection performance. Given its compact design, LitCVit aligns well with the resource constraints of typical edge and IoT devices, as prior studies [12] indicate that models with sub-million parameters, FLOPs in the range of a few million, and inference latencies between 10−500 ms, are considered practically deployable in such environments. Our main contributions are summarized as follows.

• We propose LitCVit framework, which introduces a lightweight architecture tailored for encrypted malicious trafic detection through two key design strategies:

Firstly, LitCVit integrates an eficient convolutional patchify stem and three hierarchical windowed factorized attention (wf-Attention) modules, designed to capture fine-grained intra-flow patterns at byte, packet, and flow levels. This architecture significantly reduces the computational overhead of the vanilla Vision Transformer (ViT) architecture while preserving fine-grained spatial representations of flows.

– Secondly, LitCVit employs contrastive learning to capture semantic and behavioral relationships across flows. By clustering ET-flow with similar patterns, the model learns robust and discriminative representations that separate malicious and benign trafic, thereby enhancing detection performance and generalization across diverse threat scenarios.

• We perform a comprehensive computational complexity analysis, demonstrating that the proposed model operates with substantially fewer parameters and reduced memory usage than conventional multi-head self-attention models, making it highly suitable for resource-constrained deployments.

• We validate LitCVit’s efectiveness and eficiency across six real-world network trafic datasets, demonstrating its superior performance over state-of-the-art self-supervised methods. The model’s lightweight design and low inference latency make it suitable for deployment in resource-constrained environments such as edge and IoT.

The remainder of this paper is organized as follows. Section II reviews related work, Section III introduces the threat model and design goals, Section IV details the architecture of LitCVit, Section V presents the computation complexity analysis, Section VI reports experiments and results, Section VII discusses the findings, Section VIII provides the ablation study, and Section IX concludes the paper.

## II. RELATED WORK

We categorize related work into three types: feature-driven, raw-trafic-based, and pre-training-based techniques.

## A. Feature-Driven Techniques

Feature-driven methods extract fields from encrypted trafic, including header features [13], flow or connection statistics [14], and side-channel features [15], [16] to infer malicious behavioral signatures. Some techniques analyze Secure Sockets Layer/ Transport Layer Security (SSL/TLS) handshakes for features such as cipher suites [17], JA3/JA3S hashes, and self-signed and expired certificates [18].However, TLS 1.3 handshake encryption and manual feature engineering limit their efectiveness in real-time environments.

## B. Raw Bytes-Based Techniques

Raw bytes-based methods use end-to-end deep learning on byte-level trafic via Convolutional Neural Networks (CNNs) [19], [20], hybrid Recurrent Neural Networks (RNNs), Bidirectional Gated Recurrent Units (BiGRUs), and CNNs [21], [22] to capture spatial and temporal features. While efective, they require large labeled datasets, which are dificult to acquire in real time. To overcome this, self-supervised learning techniques have been proposed.

## C. Pre-Training-Based Techniques

Pre-training–based methods reduce reliance on labeled data by learning general trafic representations for downstream finetuning. Natural language processing (NLP)-based architectures model packet- or flow-level byte sequences as linguistic tokens and apply Large Language Models (LLMs) such as Bidirectional Encoder Representations from Transformers (BERT) [6], [10], [11], [23], a Packet-level End-to-end Attentive Network for encrypted trafic classification (PEAN) [24], a Lite BERT (ALBERT) [25], [26], GPT [27], and T5 [9] to learn representations of encrypted trafic. MIETT [28] further models inter-packet dynamics via multi-instance learning with novel flow-level contrastive pre-training tasks to learn representations of encrypted trafic. Similarly, vision-inspired approaches such as Yet another Trafic Classifier (YaTC) [8], Flow-MAE [29], and NetMamba [30] transform trafic into image-like grids and employ ViT-style architectures. Other methods identify malware trafic using channel-level behavior sequences [7], adversarial pre-training [31], and cross-modal contrastive learning (tFusion [32]).

Despite strong results, recent work reveals that many pre-training–based classifiers sufer from shortcut learning, data leakage, and unrealistic evaluation practices, leading to inflated performance and limited generalization [9], [33]. Moreover, their complex architectures lead to high inference costs. In contrast, Our lightweight ViT-based model addresses these issues through leakage-free evaluation, reduced complexity, and windowed factorized attention with contrastive learning.

## III. THREAT MODEL AND DESIGN GOALS

## A. Threat Model

We consider a passive encrypted trafic monitoring scenario where LitCVit operates as a non-intrusive module integrated with a network monitoring device via port mirroring. The adversary communicates over encrypted channels to perform malicious actions such as C2 communication, data exfiltration, ransomware, or denial-of-service (DoS) attacks. We assume the attacker controls the generation of malicious traffic, including payload (prior to encryption), timing behavior, and communication endpoints, but cannot tamper with the monitoring infrastructure. The defender passively observes mirrored trafic, including packet headers and raw encrypted payload bytes, without plaintext access. Labeling is available only during ofline fine-tuning, and no online feedback or adaptation occurs during deployment. Although an adaptive attacker may attempt trafic shaping or padding to mimic benign flows, protocol-constrained header fields and encrypted byte patterns limit complete obfuscation, enabling the model to learn robust structural and semantic representations from raw trafic data. The system operates without prior knowledge of attack signatures and learns generalizable flow representations through contrastive self-supervised pretraining across diverse environments and encryption protocols.

## B. Design Goals and Problem Definition

We aim to design a lightweight and generalizable framework for encrypted malicious trafic detection. Unlike traditional trafic classification, which identifies applications or users, our goal is to determine whether an ET-flow is benign or malicious by passively analyzing encrypted trafic.

1) Problem Formulation: Let $\mathcal { F } = \{ f _ { 1 } , f _ { 2 } , . . . , f _ { N } \}$ denote a set of encrypted trafic flows within a t seconds window, where each flow $f _ { i }$ is uniquely identified by a 5-tuple: $\mathbf { x } _ { i } = { \mathrm { \langle s r c I P } }$ srcPort dstIP dstPort protocoli and $f _ { i } =$ $\{ p _ { i 1 } , p _ { i 2 } , . . . , p _ { i M } \}$ , where each packet $p _ { i j } \in \{ 0 , 1 \} ^ { B }$ represents a fixed-length sequence of B bytes. These packet bytes are encoded into a flow matrix $\mathbf { X } _ { i } \in \mathbb { R } ^ { h \times w }$ , which serves as the input representation for the model. The goal is to learn an encoder function $\mathcal { E } : \mathbb { R } ^ { h \times w }  \mathbf { z } _ { i } \in \mathbb { R } ^ { d }$ that maps ET-flow images to a low-dimensional latent representation $\mathbf { z } _ { i }$

During fine-tuning, the pretrained encoder E is concatenated with a lightweight classifier $\mathcal { C } : \mathbf { z } _ { i }  y _ { i }$ and trained using a small labeled dataset ${ \mathcal { D } } _ { \mathrm { l a b e l e d } } ~ = ~ \{ ( { \bf X } _ { i } , y _ { i } ) \}$ , where $y _ { i } \in \{ 0 , 1 , . . . , C { - } 1 \}$ is the ground truth label. The goal is to accurately detect malicious encrypted flows, while ensuring eficiency, generalization, and low inference latency.

2) Design Goals: To address the scarcity of labeled encrypted malicious trafic, LitCVit aims to learn semantically rich flow-level representations through contrastive self-supervised pretraining, reducing the dependency on manual annotation and rule-based heuristics. The system must be capable of detecting a wide range of threats without relying on protocol-specific features, ensuring robust generalization across diverse encryption protocols and trafic patterns, including 5G and IoT. In addition, the detection pipeline is required to maintain high inference speed and throughput, making it suitable for deployment in high-bandwidth environments.

## C. Design Motivation of the Proposed Architecture

The design of LitCVit is motivated by three key limitations of existing approaches. First, although transformer-based architectures provide strong global context modeling, their quadratic attention complexity makes them unsuitable for resource-constrained environments. Second, classical ML methods depend on handcrafted statistical features that ofer limited adaptability to modern encrypted protocols such as TLS 1.3. Third, lightweight convolutional models capture local spatial patterns but fail to model long-range behavioral dependencies present in encrypted trafic. To address these limitations, LitCVit adopts a hierarchical Vision Transformer with windowed factorized attention, enabling eficient capture of byte, packet, and flow-level semantics within a compact and lightweight architecture. The comparative and ablation results in Section VIII validate these design choices quantitatively.

## IV. PROPOSED ARCHITECTURE

In this section, we present the architecture of the proposed framework for encrypted malicious trafic detection, inspired by the ViT [34]. The proposed architecture utilizes a lightweight convolutional patchify stem, which preserves local spatial features. To further enhance eficiency, we incorporate a multi-scale windowed factorized attention mechanism that decomposes attention operations across byte-level, packetlevel, and flow-level representations, significantly reducing computational complexity and memory overhead. A contrastive loss term is added to the training objective to produce embeddings that distinguish among various ET-flows during the pre-training phase. The overall architecture consists of three phases: Pre-processing, Pre-training, Fine-tuning & Evaluation phase, as illustrated in Fig. 1. Each of these phases is explained in detail in the following sections.

## A. Pre-Processing Phase: Flow-Level Image Construction

To construct a structured and information-preserving representation, we extract ET-flow information directly from the raw Packet Capture (PCAP) file, similar to [8]. Fig. 1 Block A shows the pre-processing phase. We use both unlabeled and labeled PCAP data in preprocessing phase. First, we extract N flows based on IP addresses, port numbers, and transport-layer protocols, port numbers, and the transport layer protocol. Second, each flow is truncated or zero-padded to $M \ : = \ : 5$ packets to ensure fixed-length representation where $p _ { 1 j } , p _ { 2 j } , . . . , p _ { M j }$ represent the M packets of the j-th flow. Ethernet headers are removed and IP addresses and port numbers are anonymized to ensure user privacy and reduce datasetspecific bias. Each packet is encoded using n bytes, reshaped into a two-dimensional matrix of shape $p \times w _ { : }$ , where p denotes the number of rows and w the number of bytes per row. For a flow consisting of M packets, these matrices are vertically stacked to form a single flow-level matrix: $\mathbf { \Delta } : \mathbf { X } _ { i } \in \mathbb { R } ^ { ( M \cdot p ) \times w }$ . In our case, we take $p = 8$ and $w = 4 0$ consisting of $n = 3 2 0$ bytes of a packet. Finally, this matrix is saved as an ET-Flow image, preserving both the internal byte-level structure of packets and their sequential order. The output of this phase consists of labeled and unlabeled ET-Flow images, to be used for finetuning and pre-training, respectively.

![](images/dcb609eddf40f7beb719762d76a873d645164bcdd8d4d0051d54e9f3e1d05fda.jpg)  
Fig. 1. The proposed framework for encrypted malicious trafic detection.

## B. Pre-Training Phase: Contrastive Representation Learning With ViT

The pre-training phase aims to learn robust and discriminative representations of encrypted trafic flows without requiring labeled data. It consists of three main components: a convolutional patchify stem, hierarchical windowed factorized attention (wf-Attention), and a contrastive embedding head. The overall pre-training process is shown in Fig 1 Block B and described in Algorithm 1. The input to this phase is unlabeled ET-flow images generated during the pre-processing stage. These images are first passed through the convolutional patchify stem, which tokenizes them into patch embeddings. The embeddings are then processed by wf-Attention modules of the transformer, enabling multi-scale feature extraction at byte, packet, and flow levels. Finally, the encoder output is passed through the contrastive learning head to produce robust latent representations for downstream fine-tuning. The details of each component are provided in the following subsections.

1) Convolutional Patchify Stem: Unlike traditional patch embeddings [34] that divide images into large patches and apply computationally expensive linear projections with limited spatial inductive bias, our design is inspired by the eficient spatial decomposition in MobileNetV4 [35]. As shown in Algorithm 1 (lines 1-3), the Stem employs depthwise separable convolutions tailored for ET-flows, capturing localized flow patterns early in the network while significantly reducing operations compared to the standard convolutions in [8]. To the best of our knowledge, such convolutional tokenization, based on depthwise and pointwise convolutions, has not been explored in encrypted trafic detection frameworks.

Finally, positional encoding is applied to preserve spatial relationships, and resulting n-dimensional position embeddings are passed to the wf-Attention modules (line 4).

2) Hierarchical Windowed Factorized Attention: To capture multi-scale flow patterns, we adopt a lightweight hierarchical design that models fine-grained encrypted trafic behaviors at the byte, packet, and flow levels. Each stage consists of a lightweight transformer block composed of Layer Normalization followed by a WF-Attention module. To reduce the quadratic cost of multi-head self-attention, we adopt a lowrank factorized attention mechanism that directly projects token sequences into a shared, low-dimensional space (r d), without relying on additional compression matrices, as in Linformer [36], which significantly lowers computational overhead. Furthermore, to avoid costly global attention computations, we employ windowed attention [37] at byte and packet levels, restricting attention to local windows and thus significantly reducing computational overhead while maintaining fine-grained flow representations. This efectively reduces the number of attention computations from O(N<sup>2</sup>) to O(N·w), where w is the window size.

Although windowed attention limits local interactions at early stages long-range dependencies are preserved through hierarchical composition. Byte- and packet-level encoders induce sparse local attention, while the final flow-level global factorized attention produces dense interactions across all packet tokens and the CLS token. Consequently, the stacked attention layers maintain a fully connected token interaction graph, preserving global contextual modeling with reduced complexity. The attention is computed as [36]:

$$
Q = X W _ {Q}, \quad K = X W _ {K}, \quad V = X W _ {V},
$$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 LitCViT Pretraining
Input: ET-Flow image $x \in \mathbb{R}^{B \times C \times H \times W}$, dim $D$, temp. $\tau$
Output: Latent embedding $\mathbf{z}_i$ from encoder $\mathcal{E}$ // Convolutional Patchify Stem
1 $x_1 \leftarrow \text{GELU}(\text{BN}(\text{Conv1D}_{\text{depthwise}}(x)))$
2 $x_2 \leftarrow \text{GELU}(\text{BN}(\text{Conv1D}_{\text{pointwise}}(x_1)))$
3 $\mathbf{E} \leftarrow \text{Flatten}(x_2)$
4 $\mathbf{E} \leftarrow \text{PositionEncoding}(\mathbf{E})$
// Byte-Level Windowed Factorized Attention
5 for each $\mathbf{E}_i$ in $\mathbf{E}$ do
6 $\begin{array}{c}\mathbf{W}_i \leftarrow \text{WindowSlice}(\mathbf{E}_i, p, w) // \text{Slice into } p \times w \text{ windows}\end{array}$
7 $\mathbf{W}_i \leftarrow \text{LayerNorm}(\mathbf{W}_i)$
8 $\mathbf{A}_i \leftarrow \text{FactorizedAttn}(\mathbf{W}_i; \tau_{\text{attn}})$
9 $\mathbf{P}_i \leftarrow \text{Pool}(\mathbf{A}_i) // \text{Packet token}$
// Inter-Packet Windowed Factorized Attention
10 $\mathbf{P} \leftarrow \text{Stack}([\mathbf{P}_1, \ldots, \mathbf{P}_N])$
11 $\mathbf{P} \leftarrow \text{LayerNorm}(\mathbf{P})$
12 $\mathbf{F}_i \leftarrow \text{FactorizedAttn}(\mathbf{P}; \text{stride}, \tau_{\text{attn}})$
// Intra-Flow global Factorized Attention
13 $\mathbf{F} \leftarrow \text{LayerNorm}(\mathbf{F})$
14 $\mathbf{G}_i \leftarrow \text{FactorizedAttn}(\mathbf{F}, \tau_{\text{attn}})$
// Projection Head
15 $\bar{\mathbf{z}}_i \leftarrow \text{Mean}(\mathbf{G}) // \text{Global average pooling}$
16 $\mathbf{z}_i \leftarrow \text{MLP}(\bar{\mathbf{z}}_i)$
// Contrastive Learning
17 for each mini-batch $\{(z_i, z_i^+) \}_{i=1}^N$ do
18 $\begin{array}{c}\mathcal{L}_c \leftarrow \text{ntXentLoss}(\{z_i, z_i^+\}; \tau) // Eq. (1) \\ \text{Backpropagate} \nabla\mathcal{L}_c and update \mathcal{E}\end{array}$
</div>

where $W _ { Q }$ $W _ { K }$ $W _ { V } \in \mathbb { R } ^ { d \times r }$

$$
\text { Attention } (X) = \text { softmax } \left(\frac {Q K ^ {\top}}{\tau_ {a t t n}}\right) V,
$$

where $\tau _ { a t t n }$ is a learnable temperature parameter that controls attention sharpness.

The byte-level encoder (lines 5-9) performs factorized self-attention within fixed-size windows of size w over the byte-level representations to capture local dependencies. The resulting features are pooled into packet-level tokens and passed to a second encoder inter-packet wf-Attention (lines 10-12), which performs inter-packet windowed factorized attention to model to capture cross-packet relationships. The Intra-flow global Fact-Attention (lines 13-14) applies global factorized attention across the entire flow to model long-range dependencies. Between each stage, lightweight depthwise convolutions inject spatial inductive biases and compress intermediate features. Finally, the encoded tokens are aggregated via average pooling and passed through a two-layer MLP projection head to produce compact latent embeddings for contrastive learning.

![](images/a0475d5f8fcbc2767b513462283794b7a9a811f6bd1be6cb541290c83a385ecc.jpg)  
Fig. 2. UMAP visualization of embeddings generated by pre-trained LitCViT

Upon completion of the pre-training phase, during which the ntXent loss is employed to optimize the model parameters, the encoder is preserved and its pre-trained weights are transferred for use in the fine-tuning phase (Block C).

3) Contrastive Embedding Head: We train LitCVit using the Normalized Temperature-scaled Cross Entropy (ntXent) loss [38] (lines 17-19):

$$
\mathcal {L} _ {\mathrm{ntXent}} = - \frac {1}{N} \sum_ {i = 1} ^ {N} \log \frac {\exp \left(\frac {\mathbf {z} _ {i} \cdot \mathbf {z} _ {i} ^ {+}}{\tau}\right)}{\exp \left(\frac {\mathbf {z} _ {i} \cdot \mathbf {z} _ {i} ^ {+}}{\tau}\right) + \sum_ {j = 1 , j \neq i} ^ {N} \exp \left(\frac {\mathbf {z} _ {i} \cdot \mathbf {z} _ {j}}{\tau}\right)},\tag{1}
$$

where $\mathbf { z } _ { i }$ is the embedding of the i-th sample, ${ \pmb z } _ { i } ^ { + }$ is a positive (similar) pair, and $\mathbf { z } _ { j }$ are negative (dissimilar) embeddings. τ is a temperature parameter that adjusts the smoothness of the similarity distribution during contrastive learning.

Fig. 2 shows the quality of the learned embeddings at temperature parameter $\tau \ = \ 0 . 3 ,$ visualized using Uniform Manifold Approximation and Projection (UMAP). UMAP projects high-dimensional representations into 2D space while preserving local and global structures, making it suitable for qualitatively assessing clustering behavior. The visualization indicates that LitCVit forms distinct clusters of benign and malicious encrypted trafic flows, highlighting its ability to capture meaningful flow correlations in a self-supervised manner. Quantitatively, the learned embeddings achieve a cluster purity of 0.7579 and a Normalized Mutual Information (NMI) score of 0.508, indicating reasonably good separability of flow behaviors despite encryption. These representations are expected to become more discriminative during supervised fine-tuning. The impact of diferent τ values on clustering quality is presented in Section VIII. After the pre-training, we freeze the encoder and preserve the learned weights for downstream fine-tuning tasks.

## C. Fine-Tuning & Evaluation Phase: Supervised Adaptation for Malicious Trafic Detection

We fine-tune the pre-trained model to detect various types of malicious encrypted trafic, as illustrated in Block C of Fig. 1. Labeled ET-flow images are first processed through the convolutional patchify stem to generate patch embeddings, which are passed through the pre-trained encoder connected to a lightweight MLP-based classifier. The classifier consists of three fully connected layers with GELU activations and a dropout rate of 0.2, ending in a softmax layer. Final predictions are obtained directly from the supervised softmax probability distribution; LitCVit does not employ reconstruction-based anomaly scoring or threshold-based drift detection. Initially, the encoder is frozen, and only the classification head is trained to prevent overfitting in the early stages. After 100 epochs, the last two encoder blocks are unfrozen to enable the adaptation to the downstream classification task. The model is optimized using the standard multi-class cross-entropy loss $\mathcal { L } _ { \mathrm { C E } }$ [39], as defined in Equation 2. This process of fine-tuning is described in Algorithm 2 (lines 3-13).

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 Fine-Tuning

Input: Pretrained encoder E, number of classes C,
    dataset  $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^N$ 

Output: Fine-tuned classifier M

// Build classifier head

1  $H \leftarrow$  ClassifierHead()
    // Attach classifier to pretrained backbone

2  $M \leftarrow E \oplus H$ 

3 Freeze(E) // Freeze encoder parameters

4 for epoch t = 0 to T do

5    if  $t = T_{freeze}$  then
6    Unfreeze last two transformer blocks of E

7    for each  $(x_i, y_i)$  from D do

8    $z_i \leftarrow \mathcal{E}(x_i)$  // Generate embeddings
9    $h_1 \leftarrow \text{Dropout}(\text{GELU}(\text{FC}_1(z_i)))$ 
10    $h_2 \leftarrow \text{Dropout}(\text{GELU}(\text{FC}_2(h_1)))$ 
11    $\hat{y} \leftarrow \text{softmax}(\text{FC}_{\text{out}}(h_2))$ 
12    Compute loss  $L_{CE}$  // Eq. (2)
13    Backpropagate  $\nabla L_{CE}$  and update parameters
</div>

$$
\mathcal {L} _ {\mathrm{CE}} = - \frac {1}{N} \sum_ {i = 1} ^ {N} \sum_ {k = 1} ^ {C} y _ {i, k} \log (\hat {y} _ {i, k})\tag{2}
$$

Here, N is the number of samples, C is the total number of classes, $y _ { \mathrm { i , k } }$ is a binary indicator and $\hat { y } _ { \mathrm { i , k } }$ is the predicted probability for class k.

In the final stage of our framework, we evaluate the finetuned LitCVit model on labeled test data that was not used during training. This step ensures the model’s ability to generalize from the learned representations to classify unseen encrypted trafic flows accurately.

## V. COMPLEXITY ANALYSIS

We analyze the computational complexity of each component in LitCVit to highlight its architectural eficiency. Despite its multi-stage hierarchical design, the model maintains a low overall computational cost. Similar to [40], we express the complexity in terms of the convolution kernel size $k ,$ the number of tokens $n ,$ input dimension $c _ { i n } ,$ and output embedding dimensions d. We find both time and space complexities of each component as summarized in Table I.

Convolutional patch embedding stem employs a depthwise and pointwise factorization where the depthwise stage processes channels independently with cost $\mathcal { O } ( n \cdot c _ { i n } \cdot k )$ and the pointwise stage costs $O ( n { \cdot } c _ { i n } { \cdot } d )$ . This yields a total complexity of $O ( n \cdot c _ { i n } ( k + d ) )$ , which is substantially lower than the standard convolutional embedding which costs $\mathcal { O } ( n \cdot c _ { i n } \cdot k \cdot d ) )$ when $( k \ \ll \ d ) .$ , while preserving representational capacity. Moreover, hierarchical wf-Attention modules significantly reduce sequence length and the computational cost compared to traditional multi-head attention $\mathcal { O } ( n \cdot h \cdot d ^ { 2 } )$ [40], where h is the number of heads and $d$ is the per-head dimension. In our approach, we employ low-rank factorized attention, resulting in a more eficient complexity of $O ( n \cdot r \cdot w )$ operations for local attention within windows of size w and $O ( n \cdot d \cdot r )$ operations for low-rank projections, where $r \ll d$ is the factorization rank.

TABLE I  
ASYMPTOTIC COMPLEXITY OF LITCVIT COMPONENTS

<table><tr><td>Module</td><td>Time Complexity</td><td>Space Complexity</td></tr><tr><td>Conv. Patchify Stem</td><td> $\mathcal{O}(n \cdot c_{in}(k+d))$ </td><td> $\mathcal{O}(C_{in}(k+d))$ </td></tr><tr><td>wf-Attention modules</td><td> $\mathcal{O}(n \cdot r \cdot w + n \cdot d \cdot r)$ </td><td> $\mathcal{O}(n \cdot (w+d))$ </td></tr><tr><td>Contras. Embed. Head</td><td> $\mathcal{O}(d \cdot h + h \cdot d')$ </td><td> $\mathcal{O}(h+d')$ </td></tr><tr><td>ntXent Loss</td><td> $\mathcal{O}(B^2 \cdot d')$ </td><td> $\mathcal{O}(B \cdot d')$ </td></tr><tr><td>Classifier Head</td><td> $\mathcal{O}(d \cdot h_1 + h_1 \cdot h_2 + h_2 \cdot C)$ </td><td> $\mathcal{O}(h1 + h2 + C)$ </td></tr><tr><td colspan="3"> $n$ : tokens,  $C_{in}$ : input dim.,  $k$ : kernel size,  $d$ : embedding dim.,  $d'$ : projection dim.,  $B$ : batch size,  $r$ : attention rank,  $w$ : window size,  $h$ : MLP hidden dim.</td></tr></table>

During pretraining, full forward and backward passes are computed over the entire architecture, including contrastive objectives. The total pre-training complexity is $O ( n \cdot ( r \cdot w +$ $d \cdot r ) + d \cdot d ^ { \prime } + B ^ { 2 } \cdot d ^ { \prime } )$ , where the first two terms correspond to the attention and projection layers, and the last term arises from the pairwise similarity computations in ntXent. The time complexity is dominated by the higher order of $\mathcal { O } ( B ^ { 2 } \cdot d ^ { \prime } )$ due to the quadratic scaling with batch size, while other components scale linearly with the number of tokens n and remain comparatively lightweight. Similarly, space complexity during pre-training is dominated by $\mathcal { O } ( B { \cdot } d ^ { \prime } )$ term from storing projection embeddings for all samples in the batch, with the remaining components contributing only linear growth in n.

In the fine-tuning phase, we compute the total cost by adding the time complexity of convolutional patchify stem, the last two encoder blocks, and the classification head with a softmax cross-entropy loss. Since contrastive learning is only used during pretraining, computational cost is dominated by the two unfrozen encoder blocks, while the classification head contributes a comparatively small cost. The dominant time cost of fine-tuning phase is $O ( n \cdot r \cdot ( w + d ) )$ . Space complexity is dominated by storing intermediate activations for the two unfrozen encoder blocks, with the classification head adding a negligible footprint compared to pretraining, where batch-wise projection embeddings dominated memory use. The space complexity of fine-tuning phase is $O ( n \cdot ( w + d ) )$

Finally, at inference, the model executes only a lightweight forward pass, without the contrastive head, resulting in an eficient runtime complexity of $\mathcal { O } ( n { \cdot } d { \cdot } r )$ and space complexity of O(n·d). As a result, LitCViT achieves a significantly smaller memory footprint and faster inference.

## VI. IMPLEMENTATION AND EXPERIMENTS

## A. Datasets

To evaluate the performance and generalization of the proposed LitCVit, we utilize four real-world trafic datasets that include benign and malicious network trafic across diverse environments.

USTC-TFC2016 [19] provides encrypted trafic generated by a wide range of benign applications such as Skype, Bit-Torrent, and YouTube, as well as malicious trafic from ten malware families, including Cridex, Geodo, Htbot, Miuref, Neris, Nsis-ay, Shifu, Tinba, Virut, and Zeus. These malware families represent a wide spectrum of attack behaviors: Tinba and Geodo are banking trojans designed for credential theft, Cridex and Zeus are known for man-in-the-browser attacks. Miuref is associated with click fraud campaigns, while Virut represents a polymorphic file-infector. For our analysis, we retain only complete encrypted trafic flows to ensure data integrity and consistency.

CICIOT-2022 [41] is designed for behavioral analysis and intrusion detection in IoT. It contains both benign and malicious trafic, with two primary attack categories: brute-force attacks (performed using Nmap and Hydra) and flooding attacks.

5GAD-2022 [42] is a 5G network trafic dataset collected by Idaho National Research Laboratory. It captures network trafic in simulated 5G environments to support ML-based attack detection. The dataset encompasses 10 attack categories, including reconnaissance, network reconfiguration, and DoS attacks, providing a comprehensive benchmark for evaluating detection models under diverse and realistic 5G threat scenarios.

Malware Capture Facility Project (MCFP) [43], maintained by the Czech Technical University in Prague, provides a rich repository of network trafic captured in controlled environments. For our study, we extracted malicious samples from diverse malware families, such as BitcoinMiner, Botnet, Cobalt, Dridex, and Trojan Downloader. To create a balanced evaluation set, we additionally selected 600 benign PCAP files from the CTU-Normal series.

IoT-23 [44] is a large-scale IoT network trafic dataset containing benign and malicious traces captured from real IoT devices and botnet infections. It includes labeled attack scenarios alongside normal trafic to support intrusion detection and malware analysis research.

TII-SSRC-23 [45]is a network trafic dataset for IDS research containing benign and malicious trafic with 26 attack classes. It covers 8 main trafic types, including background, multimedia, brute-force, DoS, Mirai botnet, and informationgathering activities.

We utilize USTC-TFC2016 and CIC-IoT-2022 datasets during the pretraining phase, allowing the model to learn generalizable encrypted trafic representations. The rest of datasets are used solely during the fine-tuning phase to evaluate the model’s generalization on novel trafic patterns and attack scenarios. Fine-tuning and evaluation are performed on all datasets to ensure a comprehensive assessment of LitCVit’s detection performance across diverse network environments.

## B. Implementation Overview

We adopt a two-phase training strategy of pre-training followed by fine-tuning, with key hyperparameters summarized in Table II. During pre-training, the ntXent optimization is stabilized via cosine learning rate scheduling with linear warmup. A batch size of 128 provides suficient in-batch negative diversity for stable contrastive optimization without requiring a memory bank, as supported by our clustering results in Table VIII. The temperature $\tau \ = \ 0 . 3 .$ , achieve the best clustering performance in terms of purity and NMI. All attention modules adopt low-rank factorized self-attention with r = 16, balancing expressiveness and eficiency.

TABLE II  
KEY HYPERPARAMETERS OF LITCVIT TRAINING

<table><tr><td>Hyperparameter</td><td>Pre-training</td><td>Fine-tuning</td><td>Selection</td></tr><tr><td>Embedding Dim.</td><td>128 / 192*</td><td>128 / 192</td><td>Ablation</td></tr><tr><td>Rank (r)</td><td>16</td><td>16</td><td>Ablation</td></tr><tr><td>Byte / Packet Wind</td><td>5 / 3</td><td>5 / 3</td><td>Pretraining</td></tr><tr><td>Optimizer</td><td>AdamW</td><td>AdamW</td><td>Fixed</td></tr><tr><td>LR Schedule</td><td>Cosine + Warmup</td><td>Cosine + Warmup</td><td>Fixed</td></tr><tr><td>Weight Decay</td><td> $10^{-4}$ </td><td> $10^{-4}$ </td><td>Fixed</td></tr><tr><td>Learning Rate</td><td> $2 \times 10^{-3}$ </td><td> $2 \times 10^{-4}$ </td><td>Tuned</td></tr><tr><td>Batch Size</td><td>128</td><td>64</td><td>Tuned</td></tr><tr><td>Epochs</td><td>—</td><td>500</td><td>—</td></tr><tr><td>Temperature (τ)</td><td>0.3</td><td>—</td><td>Tuned</td></tr></table>

See SectionVIII for embedding dimension trade-off analysis

During fine-tuning, to address severe class imbalance present in datasets such as CICIoT-2022, we employ classweighted cross-entropy with inverse-frequency weights combined with class-balanced sampling, preventing majority class dominance during both pretraining and fine-tuning. To avoid overfitting during early training, The encoder is initially frozen for the first 100 epochs, after which the last two transformer blocks are unfrozen for deeper fine-tuning. All experiments were conducted on Intel i5-7400 CPU, NVIDIA GeForce GTX 1080 GPU, and 32GB RAM using PyTorch.

Fig. 3 shows the accuracy and loss curves during fine-tuning across all datasets, illustrating LitCVit’s stable convergence behavior and robust generalization across diverse trafic scenarios. The model consistently converges within 500 epochs, after which no significant improvements are observed. Training is, therefore, halted to avoid unnecessary computational overhead. Notably, a slight spike in loss and accuracy fluctuation is observed around epoch 100. This is because, at this point, the last two encoder blocks are unfrozen to enable deeper fine-tuning. This controlled unfreezing strategy refines high-level representations while maintaining overall training stability.

## C. Baselines and Evaluation Metrics

To evaluate LitCVit, we select baselines spanning featuredriven, end-to-end, and self-supervised pretraining-based techniques. All methods are retrained on the six datasets using their default hyperparameters for fair comparison.

Feature-driven: AppScanner [14] employs flow-level statistical features with Random Forest (RF) and SVM for application trafic classification. Kitsune [15] is an unsupervised method utilizing packet-level metadata features with an autoencoder ensemble to model benign behavior.

• End-to-end: 2D-CNN [19] transforms raw encrypted trafic into 2D grayscale images classified via convolutional neural networks.

• Self-supervised and representation learning: PEAN [24] pre-trains an attention-based autoencoder to learn generalized trafic embeddings. PERT [46] and ET-BERT [6] adopt BERT-style masked language modeling for contextual trafic representations. YaTC [8] applies a masked autoencoder for pretraining on raw trafic bytes followed by supervised classification. NetMamba [30] is a model based on the Mamba architecture. Pcap-Encoder [9] is a recent representation learning model specifically designed to extract features from protocol headers.

<table><tr><td colspan="5">USTCTFC-2016</td><td colspan="4">CICIoT-2022</td><td colspan="4">5GAD-2022</td></tr><tr><td>Method</td><td>Acc.</td><td>F1</td><td>Prec.</td><td>Recall</td><td>Acc.</td><td>F1</td><td>Prec.</td><td>Recall</td><td>Acc.</td><td>F1</td><td>Prec.</td><td>Recall</td></tr><tr><td>Appscanner</td><td>60.41</td><td>62.53</td><td>62.23</td><td>65.36</td><td>76.52</td><td>75.69</td><td>74.10</td><td>63.52</td><td>51.03</td><td>53.41</td><td>53.23</td><td>52.13</td></tr><tr><td>Kitsune</td><td>88.09</td><td>82.13</td><td>83.64</td><td>84.15</td><td>87.08</td><td>84.26</td><td>81.19</td><td>78.64</td><td>64.23</td><td>65.07</td><td>62.32</td><td>61.23</td></tr><tr><td>2D-CNN</td><td>92.26</td><td>92.05</td><td>92.35</td><td>92.24</td><td>90.07</td><td>90.00</td><td>90.23</td><td>90.41</td><td>89.45</td><td>87.21</td><td>89.23</td><td>88.12</td></tr><tr><td>PEAN</td><td>73.32</td><td>67.91</td><td>67.25</td><td>69.45</td><td>61.59</td><td>63.63</td><td>61.43</td><td>61.54</td><td>51.12</td><td>52.10</td><td>52.10</td><td>52.45</td></tr><tr><td>PERT</td><td>90.23</td><td>90.12</td><td>91.02</td><td>91.03</td><td>91.09</td><td>90.41</td><td>91.25</td><td>91.36</td><td>85.06</td><td>85.4</td><td>85.69</td><td>85.07</td></tr><tr><td>ETBERT</td><td>87.74</td><td>87.47</td><td>85.54</td><td>85.36</td><td>90.35</td><td>90.31</td><td>89.98</td><td>89.78</td><td>92.10</td><td>93.41</td><td>92.07</td><td>91.58</td></tr><tr><td>YaTC</td><td>96.34</td><td>96.33</td><td>96.36</td><td>96.33</td><td>95.85</td><td>95.12</td><td>96.07</td><td>95.43</td><td>96.04</td><td>96.75</td><td>95.04</td><td>95.36</td></tr><tr><td>NetMamba</td><td>95.23</td><td>95.29</td><td>95.56</td><td>95.59</td><td>92.43</td><td>92.49</td><td>92.12</td><td>92.67</td><td>91.34</td><td>87.45</td><td>87.32</td><td>87.19</td></tr><tr><td>Pcap-Encoder</td><td>91.29</td><td>91.52</td><td>91.35</td><td>91.23</td><td>89.45</td><td>87.29</td><td>87.13</td><td>87.35</td><td>89.92</td><td>89.26</td><td>89.72</td><td>89.48</td></tr><tr><td>LitCVit</td><td>98.37</td><td>98.32</td><td>98.25</td><td>98.37</td><td>99.12</td><td>99.11</td><td>99.14</td><td>99.02</td><td>97.24</td><td>97.25</td><td>97.26</td><td>97.24</td></tr><tr><td colspan="5">MCFP</td><td colspan="4">IOT-23</td><td colspan="4">TII-SSRC-23</td></tr><tr><td>Method</td><td>Acc.</td><td>F1</td><td>Prec.</td><td>Recall</td><td>Acc.</td><td>F1</td><td>Prec.</td><td>Recall</td><td>Acc.</td><td>F1</td><td>Prec.</td><td>Recall</td></tr><tr><td>Appscanner</td><td>64.23</td><td>61.03</td><td>61.45</td><td>63.41</td><td>78.08</td><td>77.29</td><td>77.43</td><td>77.12</td><td>57.57</td><td>57.30</td><td>57.24</td><td>57.31</td></tr><tr><td>Kitsune</td><td>78.04</td><td>79.12</td><td>78.68</td><td>78.59</td><td>81.83</td><td>81.45</td><td>80.34</td><td>81.11</td><td>81.23</td><td>91.79</td><td>91.32</td><td>91.45</td></tr><tr><td>2D-CNN</td><td>78.1</td><td>75.12</td><td>78.12</td><td>78.12</td><td>91.38</td><td>91.15</td><td>92.25</td><td>92.25</td><td>78.23</td><td>78.05</td><td>78.10</td><td>77.63</td></tr><tr><td>PEAN</td><td>78.15</td><td>77.18</td><td>78.98</td><td>78.65</td><td>95.69</td><td>92.45</td><td>91.02</td><td>92.45</td><td>89.37</td><td>90.36</td><td>91.27</td><td>90.23</td></tr><tr><td>PERT</td><td>80.22</td><td>80.95</td><td>81.34</td><td>81.03</td><td>89.56</td><td>88.35</td><td>88.33</td><td>88.93</td><td>92.12</td><td>92.45</td><td>92.72</td><td>92.51</td></tr><tr><td>ETBERT</td><td>91.36</td><td>92.36</td><td>91.01</td><td>92.55</td><td>91.38</td><td>89.90</td><td>89.14</td><td>89.55</td><td>83.59</td><td>81.12</td><td>81.45</td><td>81.20</td></tr><tr><td>YaTC</td><td>94.23</td><td>94.15</td><td>94.41</td><td>94.51</td><td>95.78</td><td>95.34</td><td>95.98</td><td>95.31</td><td>93.58</td><td>91.46</td><td>91.50</td><td>91.29</td></tr><tr><td>NetMamba</td><td>81.9</td><td>81.39</td><td>81.7</td><td>89.78</td><td>89.53</td><td>88.91</td><td>99.71</td><td>88.93</td><td>89.37</td><td>87.31</td><td>87.54</td><td>87.31</td></tr><tr><td>PcapEncoder</td><td>88.24</td><td>88.43</td><td>88.51</td><td>89.03</td><td>91.03</td><td>89.20</td><td>89.10</td><td>91.29</td><td>78.24</td><td>77.28</td><td>77.62</td><td>77.29</td></tr><tr><td>LitCVit</td><td>97.67</td><td>97.65</td><td>97.70</td><td>97.54</td><td>98.52</td><td>98.11</td><td>98.71</td><td>98.24</td><td>98.63</td><td>98.05</td><td>98.19</td><td>98.41</td></tr></table>

TABLE III  
A PERFORMANCE COMPARISON OF PROPOSED ARCHITECTURE WITH BASE-LINES  
![](images/ab2927ffcd18f0fec8831b657c17a0bce0b47d1f59f30718835a68bb1138540c.jpg)  
Fig. 3. Accuracy and loss curves during fine-tuning across all datasets. Training converges stably within 500 epochs, with a brief spike around epoch 10 due to unfreezing blocks of the pretrained encoder.

For evaluation, we report accuracy, precision, recall, and F1-score to assess overall classification efectiveness, alongside True Positive Rate (TPR) True Negative Rate (TNR), False Positive Rate (FPR), and False Negative Rate (FNR), to evaluate robustness against false alarms, critical in malicious trafic detection where minimizing missed attacks and false positives is essential.

## VII. RESULTS AND DISCUSSION

We evaluate LitCVit across six real-world network trafic datasets, comparing detection efectiveness and computational eficiency against state-of-the-art methods to demonstrate its suitability for practical deployment. Unless otherwise stated, all reported results correspond to an embedding dimension of d = 192, which achieves the best classification performance as determined by the ablation study in Section VIII. For latencysensitive deployments, d = 128 is recommended as discussed in Section VIII.

## A. Detection Performance

Fig. 4 shows confusion matrices illustrating LitCVit’s classification performance across all datasets, highlighting its strong ability to distinguish attack types and benign trafic with high confidence and minimal misclassifications. For USTC-TFC2016, LitCVit achieves detection rates exceeding 97% for all malware families, except Geodo and Miuref, which attain detection accuracies of 92% and 96%, respectively. For CICIOT-2022, the model efectively identifies brute-force and flooding attacks while maintaining a low false positive rate for benign flows. Notably, 5GAD-2022 and MCFP, IOT-23, and TII-SSRC-23 were kept completely unseen during pretraining, yet LitCVit shows excellent generalization, achieving above 95% detection rate across all classes. In 5GAD-2022, AMF-FakeInsert attack reaches a detection rate of 95%, while all other classes surpass 98%. Similarly, on MCFP and IOT-23, all malware classes are detected with at least 97%, despite the diversity and complexity of their behaviors. Similarly, on TII-SSRC-23, LitCVit accurately separates benign and malicious trafic with detection rates exceeding 97%, confirming its robustness across diverse real-world encrypted trafic scenarios.

![](images/8add263d86e7fe13701d044f850f4ad10cda583476fa40fb24b00281fbf0bdec.jpg)  
Fig. 4. Performance confusion matrices of all datasets.

Fig. 5 demonstrates Precision-Recall (PR) curves to evaluate the proposed framework’s performance on datasets with imbalanced class distributions. Minority malicious trafic classes, such as Miuref and Nsis-ay in USTCTFC, and Hydra in CICIOT, pose detection challenges due to their limited representation in the dataset. Despite this, LitCVit maintains robust detection performance. Despite this, LitCVit maintains robust detection performance, achieving PR-AUC values exceeding 0.97 for all malicious trafic classes of USTCTFC, including Tinba, Geodo, Cridex, Zeus, and Virut. In CICIOT, LitCVit attains a reasonable PR-AUC of 0.70 for the minority Hydra class, while achieving perfect PR-AUC scores of 1.00 for Benign, Flood, and Nmap trafic. The reason is that Hydra has a significantly smaller number of samples. On 5GAD, which consists of eight attacks with a nearly balanced distribution, LitCVit consistently achieves high PR-AUC values, ranging from 0.99 to 1.00, across all classes. Similarly, on MCFP, IOT-23, and TII-SSRC-23, LitCVit maintains strong detection performance, achieving PR-AUC scores exceeding 0.99 across all classes. These results highlight the LitCVit’s strong ability to maintain high precision and recall across all datasets, indicating robust performance with minimal false predictions.

![](images/aefdcadc9388bb6773006d38e116d3fd82314775c35d2683bc6c593932b4b51a.jpg)  
Fig. 5. PR-curves of the proposed LitCVit model on all datasets.

## B. Comparative Performance Analysis

Table III presents a comprehensive comparison of LitCVit against state-of-the-art encrypted trafic detection methods. Across six datasets, LitCVit consistently achieves superior detection performance, outperforming all baselines in terms of accuracy, precision, recall, and F1-score. Notably, it surpasses pretraining-based models PEAN and ET-BERT across all metrics, with accuracy gains of 34.17% and 12.15% on USTC-TFC2016, and 60.9% and 9.7% on CICIOT-2022, respectively. Despite being recent strong baselines, NetMamba and PcapEncoder lag behind LitCVit by 7-9% on most datasets. PcapEncoder is designed for packet-level classification using only header information, when evaluated at the flow level, its performance degrades significantly, highlighting the advantage of LitCVit’s flow-image representation over header-only packet-level approaches. On unseen datasets, 5GAD-2022, MCFP, IOT-23 and TII-SSRC-23 LitCVit maintains an average accuracy improvement of 5-8% over the best baseline, demonstrating strong generalization capabilities. It also achieves the best precision and recall balance, indicating robustness to diverse encrypted trafic patterns and minimizing false predictions.

Fig. 6 provides a detailed comparison of TPR and FPR across all baselines and datasets, providing a comprehensive evaluation of detection capability and false alarm reduction. LitCVit consistently achieves the highest detection rates across all datasets, exceeding 98% on USTC-TFC, CICIoT-2022, MCFP, IOT-23, and TII-SSRC-23, while maintaining strong performance on the diverse 5GAD-2022 dataset with a TPR of 97%. In contrast, feature-driven methods, AppScanner and Kitsune exhibit significantly lower TPRs (52%–64% and 61%–84%, respectively), highlighting their limited capability in handling encrypted trafic scenarios. In terms of false alarms, LitCVit achieves the lowest FPR, remaining below 0.02 across all datasets. Conversely, AppScanner and the self-supervised PEAN sufer from substantially higher FPR values, reaching up to 0.32 and 0.21, respectively. These results demonstrate that LitCVit not only improves detection capability but also efectively minimizes false alarms, ensuring reliable encrypted trafic classification.

![](images/44e88917fbdb162ff2f03602d9dbee75234f4723d4582bf296f6b01cd9b8f9ff.jpg)  
Fig. 6. Comparison of TPR, TNR, FPR, and FNR across all state-of-the-art methods on the USTC-TFC-2016, CICIOT-2022, 5GAD-2022, MCFP, and TII-SSRC-23.

TABLE IV  
THE EFFICIENCY COMPARISON OF PROPOSED LITCVITWITH PRE-TRAINING-BASED TECHNIQUES

<table><tr><td>Method</td><td>GPU Infer (ms)</td><td>CPU Infer (ms)</td><td>Params. M</td></tr><tr><td>PEAN</td><td>83.3127</td><td>2603.18</td><td>2.189</td></tr><tr><td>PERT</td><td>44.7637</td><td>701.23</td><td>53.872</td></tr><tr><td>ETBERT</td><td>46.3854</td><td>723.13</td><td>132.133</td></tr><tr><td>YaTC</td><td>20.1452</td><td>243.293</td><td>1.862</td></tr><tr><td>NetMamba</td><td>10.1452</td><td>112.18</td><td>1.91</td></tr><tr><td>pcapEncoder</td><td>37.771</td><td>423</td><td>223.50</td></tr><tr><td>LitCVit</td><td>2.67</td><td>5.32</td><td>0.321</td></tr></table>

LitCVit demonstrates robust detection performance with minimal variance across datasets, efectively reducing false alarms and maintaining both high detection accuracy and operational stability in diverse and challenging network environments. Its superior performance is due to its hierarchical attention design, which progressively captures fine-grained byte-level and packet-level patterns and global flow-level dependencies. By employing windowed factorized attention, LitCVit focuses on local contexts while preserving essential token interactions, ensuring robust feature extraction throughout the hierarchy. Additionally, contrastive learning with ntXent loss further enhances the learned embeddings by pulling semantically related ET-flows closer and pushing apart dissimilar ones.

## C. Computational and Memory Analysis

Table IV demonstrates that LitCVit ofers an eficient solution for encrypted malicious trafic detection., maintaining a minimal memory footprint of approximately 14.83 MB with only 0.321 million parameters. LitCVit achieves a singlesample inference latency of 2.67 ms on GPU, measured with batch size = 1, 50 warm-up iterations, and 300 timed repetitions with GPU synchronization, making it approximately 8.7 times faster than the fastest self-supervised pretrainingbased method YaTC while achieving superior detection performance. Moreover, the model requires only 115.55 million multiply-accumulate operations (MMACs), making it highly suitable for deployment in resource-constrained environments.

![](images/13c85126db11ae418d26c7630dc79abe05ce352ab88c16a3e2df6ffad82b0e27.jpg)  
Fig. 7. Robustness of LitCVit under adversarial byte perturbations.

This eficiency is achieved primarily due to LitCVit’s lightweight convolutional patchify stem, which efectively reduces the input dimensionality and the low-rank windowed factorized attention mechanism, which drastically cuts down the number of learnable parameters by performing attention in a compressed token space. These design choices preserve the core capabilities of self-attention while significantly lowering computational overhead.

## D. Adversarial Robustness Analysis

To assess robustness against simple adversarial manipulation, two perturbation strategies are simulated: padding-byte insertion and random byte injection. Padding-byte insertion appends null bytes to packet payloads, simulating trafic padding commonly used in protocol obfuscation. Random byte injection replaces a random fraction of payload pixel values with uniform random bytes, simulating arbitrary payload corruption. All perturbations are applied exclusively to payload rows, preserving header structure to reflect realistic encrypted trafic manipulation. Perturbation experiments are conducted on USTC-TFC2016, the most class-diverse dataset with 11 trafic categories. As shown in Fig. 7, LitCVit maintains accuracy above 85% under both strategies even at 20% perturbation, with a maximum degradation of 8.97% for padding-byte insertion and 7.36% for random byte injection. The convergence of both curves at higher perturbation levels indicates consistent resilience independent of perturbation type. These results demonstrate that LitCVit captures structural and semantic trafic patterns at multiple granularities rather than relying on precise byte positions, making it inherently resilient to simple byte-level adversarial perturbations.

TABLE V  
COMPONENT-WISE ABLATION STUDY OF THE PROPOSED LITCVIT ACROSS SIX BENCHMARK DATASETS

<table><tr><td></td><td colspan="2">USTC-TFC2016</td><td colspan="2">CICIOT-2022</td><td colspan="2">5GAD</td><td colspan="2">MCFP</td><td colspan="2">IOT-23</td><td colspan="2">TII-SSRC-23</td></tr><tr><td>Variant</td><td>Acc.</td><td>F1</td><td>Acc.</td><td>F1</td><td>Acc.</td><td>F1</td><td>Acc.</td><td>F1</td><td>Acc.</td><td>F1</td><td>Acc.</td><td>F1</td></tr><tr><td>LitCVit ( PT + WA)</td><td>98.37</td><td>98.32</td><td>99.12</td><td>99.11</td><td>98.87</td><td>98.23</td><td>97.67</td><td>97.65</td><td>98.52</td><td>98.11</td><td>98.63</td><td>98.05</td></tr><tr><td>Full Rank</td><td>97.31</td><td>94.90</td><td>98.46</td><td>98.20</td><td>98.18</td><td>98.45</td><td>96.98</td><td>97.05</td><td>99.21</td><td>99.12</td><td>98.14</td><td>98.45</td></tr><tr><td>w/o Windowed Attn.</td><td>96.98</td><td>96.02</td><td>98.16</td><td>97.79</td><td>98.18</td><td>97.25</td><td>96.54</td><td>96.21</td><td>97.35</td><td>97.19</td><td>97.43</td><td>97.18</td></tr><tr><td>w/o Pre-training</td><td>95.69</td><td>94.78</td><td>95.54</td><td>95.57</td><td>95.14</td><td>95.58</td><td>91.56</td><td>91.04</td><td>92.40</td><td>92.83</td><td>94.36</td><td>94.81</td></tr><tr><td>w/o Conv. Stem</td><td>94.53</td><td>94.31</td><td>96.41</td><td>96.04</td><td>93.94</td><td>93.89</td><td>92.26</td><td>92.94</td><td>97.38</td><td>96.49</td><td>94.00</td><td>94.29</td></tr><tr><td>w/o Packet Encoder</td><td>93.34</td><td>91.24</td><td>91.37</td><td>91.80</td><td>89.34</td><td>89.38</td><td>91.24</td><td>92.43</td><td>92.47</td><td>92.35</td><td>90.29</td><td>90.42</td></tr><tr><td>w/o Byte Encoder</td><td>88.37</td><td>85.20</td><td>83.29</td><td>83.18</td><td>78.20</td><td>79.21</td><td>84.16</td><td>83.95</td><td>81.75</td><td>81.97</td><td>78.31</td><td>78.29</td></tr><tr><td>w/o Flow Encoder</td><td>45.21</td><td>30.29</td><td>51.24</td><td>52.43</td><td>35.98</td><td>35.29</td><td>56.89</td><td>56.74</td><td>48.53</td><td>48.98</td><td>34.19</td><td>33.63</td></tr></table>

Note: PT: self-supervised pre-training, WA: windowed factorized attention. Best results per column are bold, second best are underlined.

## E. Resource-Constrained Inference Analysis

To evaluate deployment feasibility on resource-constrained platforms, LitCVit is evaluated under GPU and CPU settings. Specifically, single-thread CPU inference is conducted on a system with 8 GB RAM and an Intel i5-7400 @ 3.00 GHz, deliberately chosen to simulate resource-constrained deployment conditions. With dim = 128, rank = 16, the model contains only 0.32 M parameters and requires 115.55 MMac. It achieves 2.67 ms per-sample latency on GPU, 5.32 ms under multi-thread CPU execution, and 8.70 $\mathrm { m s } \pm 0 . 9 8$ in single-thread mode. The model maintains a compact memory footprint (14.83 MB total, nearly 4.66 MB runtime overhead), demonstrating real-time capability and suitability for resource-constrained platforms. Physical validation on embedded platforms such as Raspberry Pi or NVIDIA Jetson is left as future work.

## VIII. ABLATION STUDY

## A. Component-Wise Ablation Study

Table V presents a component-wise ablation study of the proposed LitCVit on six benchmark datasets. Removing the flow-level encoder causes the most severe degradation, with Macro-F1 dropping to as low as 30.29% on USTC-TFC2016 and 33.63% on TII-SSRC-23, confirming the importance of global context aggregation across packet tokens for reliable trafic classification. Removing the byte-level encoder results in the second largest performance drop, highlighting the importance of fine-grained byte-level feature extraction in capturing low-level trafic patterns. Without self-supervised pre-training, the performance declines consistently across datasets, demonstrating that pre-training provides meaningful semantic representations. Overall, each component contributes meaningfully to performance, with the hierarchical encoder structure and self-supervised pre-training providing the most significant gains.

## B. Impact of Rank

We conduct an ablation study over rank $r \in \{ 8 , 1 6 , 3 2 , 6 4 \}$ and embedding dimension d ∈ {128 156 192} to analyze their efect on model complexity and inference eficiency. As shown in Fig. 8, parameters and MMACs increase monotonically with both r and $d ,$ confirming predictable scaling behavior. GPU latency remains relatively stable across ranks, while CPU latency grows more noticeably with dimension, reflecting limited CPU parallelism for larger matrix operations. Notably, rank $r = 1 6$ achieves the lowest inference latency across all dimensions. Detection accuracy remains stable across ranks, and the marginal gains at higher ranks confirm that encrypted trafic features lie in a low-dimensional subspace where compact factorized attention is suficient. Thus, $r = 1 6$ and $d = 1 2 8$ are adopted as default for the optimal accuracy–eficiency trade-of.

![](images/07c6bcee6a92b99ee2a667bd582d26a24839aa7e744715d31409d2f60eaa4a22.jpg)

Fig. 8. Model complexity and inference latency vs. rank ∈ {8 16 32 64} for embedding dimensions ∈ {128 156 and192}. x-axis: Rank in all subplots.  
![](images/688dda9e9290479d90ec0b4afcc7f5df962c037417d1948338f75c17115ac3e8.jpg)  
Fig. 9. Inference latency comparison of windowed attention configurations at dim = 128.

![](images/1da06cf12e630c1f781b0ec1945efff0f5ac03e9778f41d305c75bbe03a015dd.jpg)  
Fig. 10. UMAP embeddings of encrypted benign and malicious trafic under diferent temperature values τ of ntXent loss.

TABLE VI  
ABLATION STUDY ON VARIOUS WINDOW CONFIGURATIONS. PERFOR-MANCE IS BEST WITH BOTH PACKET AND BYTE-LEVEL WINDOWS

<table><tr><td rowspan="2">Window Config.</td><td colspan="2">USTC-TFC2016</td><td colspan="2">CICIOT-2022</td><td colspan="2">MCFP</td></tr><tr><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td></tr><tr><td>w/o Windows</td><td>97.58</td><td>97.02</td><td>98.16</td><td>97.79</td><td>96.54</td><td>96.21</td></tr><tr><td>Byte-level Window</td><td>95.80</td><td>93.89</td><td>95.23</td><td>93.56</td><td>94.23</td><td>94.23</td></tr><tr><td>Packet-level Window</td><td>95.08</td><td>92.00</td><td>93.56</td><td>93.54</td><td>94.23</td><td>94.72</td></tr><tr><td>with both Windows</td><td>98.37</td><td>98.32</td><td>99.12</td><td>99.11</td><td>97.67</td><td>97.65</td></tr></table>

## C. Efect of Windowed Attention

Ablation results in Fig. 9 show that GPU inference latency remains invariant across all window configurations (∼ 2 6–2.9 ms), indicating that windowed attention introduces negligible computational overhead on GPU. On CPU, enabling both byte and packet windows reduces latency by 15 − 25% compared to global attention at dim = 128. This suggests that restricting the attention span reduces redundant computation at the CPU level, where parallelism is more limited than on GPU. Table VI further reports consistent improvements in Accuracy and Macro-F1 when both windows are applied. We attribute this to the hierarchical design, where early local attention reduces premature global token mixing and encourages spatially coherent byte and packet patterns, while long-range dependencies are preserved by the flow-level transformer through full global attention across packet tokens.

## D. Performance Comparison With Conventional Models

To justify our architecture, we compare LitCVit against tree-based (RF, XGBoost) and lightweight neural baselines (2DCNN, GRU, BiLSTM) under identical settings. Since tree-based and lightweight neural models are inherently CPUbased, CPU latency is used as the common eficiency metric for fair comparison. Tree-based models use flattened 1600-d ET-flow vectors, while neural baselines use flow-image representations. As shown in Table VII, XGBoost exceeds 90% Macro F1 on USTCTFC and CICIOT but degrades on MCFP, indicating limited generalization. RF incurs high latency (27.46 ms) despite zero trainable parameters due to sequential tree traversal. Lightweight neural models ofer low latency but inconsistent performance (GRU/BiLSTM up to 71.52% Macro F1) with notable MCFP degradation. LitCVit consistently achieves the highest Macro F1 across all datasets with a compact footprint and competitive latency, demonstrating superior generalization-eficiency balance.

TABLE VII  
PERFORMANCE AND EFFICIENCY COMPARISON OF CONVENTIONALLIGHTWEIGHT MODELS WITH LITCVIT

<table><tr><td rowspan="2">Model</td><td colspan="3">Macro-F1 (%)</td><td colspan="3">Efficiency</td></tr><tr><td>USTC</td><td>CICIOT</td><td>MCFP</td><td>cpu Lat (ms)</td><td>Param.(K)</td><td>MACs(M)</td></tr><tr><td>RF</td><td>84.72</td><td>84.03</td><td>62.05</td><td>27.46</td><td>-</td><td>-</td></tr><tr><td>XGB</td><td>92.70</td><td>91.39</td><td>63.54</td><td>1.75</td><td>-</td><td>-</td></tr><tr><td>2DCNN</td><td>89.97</td><td>83.67</td><td>64.54</td><td>0.77</td><td>95.7</td><td>15.75</td></tr><tr><td>BiLSTM</td><td>65.04</td><td>71.52</td><td>70.71</td><td>0.61</td><td>179.2</td><td>7.07</td></tr><tr><td>GRU</td><td>70.66</td><td>71.41</td><td>65.71</td><td>6.99</td><td>135.7</td><td>5.30</td></tr><tr><td>LitCVit</td><td>98.37</td><td>99.11</td><td>97.65</td><td>5.57</td><td>321.81</td><td>115.55</td></tr></table>

TABLE VIII

EFFECT OF TEMPERATURE PARAMETER τ ON CONTRASTIVE VIT

<table><tr><td>τ</td><td>Loss</td><td>Cluster Purity</td><td>NMI</td><td>ARI</td><td>Silhouette Score</td></tr><tr><td>0.1</td><td>0.758</td><td>0.7198</td><td>0.464</td><td>0.2166</td><td>0.4077</td></tr><tr><td>0.3</td><td>2.335</td><td>0.7579</td><td>0.508</td><td>0.2556</td><td>0.4213</td></tr><tr><td>0.5</td><td>3.169</td><td>0.7349</td><td>0.476</td><td>0.2333</td><td>0.6069</td></tr><tr><td>0.7</td><td>3.611</td><td>0.7352</td><td>0.485</td><td>0.2774</td><td>0.7524</td></tr><tr><td>0.9</td><td>3.871</td><td>0.7228</td><td>0.5</td><td>0.3743</td><td>0.8476</td></tr></table>

## E. Impact of Temperature Parameter

The efect of Temperature parameter τ in ntXent loss on clustering quality is illustrated in Fig. 10 and Table VIII. Lower values of τ (e.g., 0.1) yield reduced loss; however, higher values (e.g., 0.9) resulted in improved global structure, as reflected by higher NMI, Adjusted Rand Index (ARI), and Silhouette scores, indicating better separation between benign and malicious trafic. The best overall clustering performance is achieved at τ = 0.3, which provides an efective tradeof between local compactness and global separability in the learned representations.

## IX. CONCLUSION

In this paper, we propose a lightweight self-supervised contrastive vision transformer framework for encrypted malicious trafic detection. The model integrates an eficient convolutional patchify stem to encode local spatial features and employs low-rank windowed factorized self-attention mechanisms at byte, packet, and flow levels to multi-granularity representations. Additionally, a contrastive pretraining objective enables the model to learn ET-flow semantic features without relying on labeled data. Extensive experiments on six real-world datasets demonstrate that the proposed framework outperforms the state-of-the-art method, including recent baselines, achieving 5-8% average accuracy improvement on unseen datasets while maintaining a compact footprint of 0.321 M parameters and 2.67 ms GPU inference latency approximately 8.7 times faster than YaTC. These results validate LitCVit’s strong generalization across diverse attack scenarios while maintaining high eficiency and low inference time, making it highly suitable for deployment in resourceconstrained environments. Future work will explore model compression via pruning and quantization, as well as physical validation on embedded platforms such as Raspberry Pi and NVIDIA Jetson.

## REFERENCES

[1] M. A. I. Mallick and R. Nath, “Navigating the cyber security landscape: A comprehensive review of cyber-attacks, emerging trends, and recent developments,” World Sci. News, vol. 190, no. 1, pp. 1–69, 2024.

[2] J. Ahn, R. Hussain, K. Kang, and J. Son, “Exploring encryption algorithms and network protocols: A comprehensive survey of threats and vulnerabilities,” IEEE Commun. Surveys Tuts., vol. 27, no. 6, pp. 3587–3614, Dec. 2025.

[3] M. Shen et al., “Machine learning-powered encrypted network trafic analysis: A comprehensive survey,” IEEE Commun. Surveys Tuts., vol. 25, no. 1, pp. 791–824, 1st Quart., 2023.

[4] M. Almehdhar et al., “Deep learning in the fast lane: A survey on advanced intrusion detection systems for intelligent vehicle networks,” IEEE Open J. Veh. Technol., vol. 5, pp. 869–906, 2024.

[5] Y. Feng et al., “Unmasking the internet: A survey of fine-grained network trafic analysis,” IEEE Commun. Surveys Tuts., vol. 27, no. 6, pp. 3672–3709, Dec. 2025.

[6] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “ET-BERT: A contextualized datagram representation with pre-training transformers for encrypted trafic classification,” in Proc. ACM Web Conf., Apr. 2022, pp. 633–642.

[7] S. Cui, C. Dong, M. Shen, Y. Liu, B. Jiang, and Z. Lu, “CBSeq: A channel-level behavior sequence for encrypted malware trafic detection,” IEEE Trans. Inf. Forensics Security, vol. 18, pp. 5011–5025, 2023.

[8] R. Zhao et al., “A novel self-supervised framework based on masked autoencoder for trafic classification,” IEEE/ACM Trans. Netw., vol. 32, no. 3, pp. 2012–2025, Jun. 2024.

[9] Y. Zhao, G. Dettori, M. Bofa, L. Vassio, and M. Mellia, “The sweet danger of sugar: Debunking representation learning for encrypted trafic classification,” in Proc. ACM SIGCOMM Conf., Sep. 2025, pp. 296–310.

[10] L. Peng, X. Xie, S. Huang, Z. Wang, and Y. Cui, “Ptu: Pre-trained model for network trafic understanding,” in Proc. IEEE 32nd Int. Conf. Netw. Protocols (ICNP), Oct. 2024, pp. 1–12.

[11] G. Zhou, X. Guo, Z. Liu, T. Li, Q. Li, and K. Xu, “TraficFormer: An eficient pre-trained model for trafic data,” in Proc. IEEE Symp. Secur. Privacy (SP), May 2025, pp. 1844–1860.

[12] S. Naveen and M. R. Kounte, “Compact optimized deep learning model for edge: A review,” Int. J. Electr. Comput. Eng. (IJECE), vol. 13, no. 6, p. 6904, Dec. 2023.

[13] A. A. Bhutta, M. U. Nisa, and A. N. Mian, “Lightweight real-time WiFibased intrusion detection system using LightGBM,” Wireless Netw., vol. 30, no. 2, pp. 749–761, Feb. 2024.

[14] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “Robust smartphone app identification via encrypted network trafic analysis,” IEEE Trans. Inf. Forensics Security, vol. 13, no. 1, pp. 63–78, Jan. 2018.

[15] Y. Mirsky, T. Doitshman, Y. Elovici, and A. Shabtai, “Kitsune: An ensemble of autoencoders for online network intrusion detection,” in Proc. Netw. Distrib. Syst. Secur. Symp., San Diego, CA, USA, 2018.

[16] C. Fu, Q. Li, M. Shen, and K. Xu, “Frequency domain feature based robust malicious trafic detection,” IEEE/ACM Trans. Netw., vol. 31, no. 1, pp. 452–467, Feb. 2023.

[17] B. Anderson, S. Paul, and D. McGrew, “Deciphering malware’s use of TLS (without decryption),” J. Comput. Virol. Hacking Techn., vol. 14, no. 3, pp. 195–211, Aug. 2018.

[18] C. Kondaiah, A. R. Pais, and R. S. Rao, “Enhanced malicious trafic detection in encrypted communication using TLS features and a multiclass classifier ensemble,” J. Netw. Syst. Manage., vol. 32, no. 4, p. 76, Oct. 2024.

[19] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware trafic classification using convolutional neural network for representation learning,” in Proc. Int. Conf. Inf. Netw. (ICOIN), Jan. 2017, pp. 712–717.

[20] L. Yu et al., “PBCNN: Packet bytes-based convolutional neural network for network intrusion detection,” Comput. Netw., vol. 194, Jul. 2021, Art. no. 108117.

[21] T. Shapira and Y. Shavitt, “FlowPic: A generic representation for encrypted trafic classification and applications identification,” IEEE Trans. Netw. Service Manage., vol. 18, no. 2, pp. 1218–1232, Jun. 2021.

[22] A. F. Diallo and P. Patras, “Cluster and conquer: Malicious trafic classification at the edge,” IEEE Trans. Netw. Service Manage., vol. 21, no. 3, pp. 2700–2714, Jun. 2024.

[23] S. Guthula, R. Beltiukov, N. Battula, W. Guo, A. Gupta, and I. Monga, “NetFound: Foundation model for network security,” 2023, arXiv:2310.17025.

[24] P. Lin, K. Ye, Y. Hu, Y. Lin, and C.-Z. Xu, “A novel multimodal deep learning framework for encrypted trafic classification,” IEEE/ACM Trans. Netw., vol. 31, no. 3, pp. 1369–1384, Jun. 2023.

[25] H. Y. He, Z. Guo Yang, and X. N. Chen, “PERT: Payload encoding representation from transformer for encrypted trafic classification,” in Proc. ITU Kaleidoscope, Ind.-Driven Digit. Transformation (ITU K), Dec. 2020, pp. 1–8.

[26] X. Zang, T. Wang, X. Zhang, J. Gong, P. Gao, and G. Zhang, “Encrypted malicious trafic detection based on natural language processing and deep learning,” Comput. Netw., vol. 250, Aug. 2024, Art. no. 110598.

[27] J. Qu, X. Ma, and J. Li, “TraficGPT: Breaking the token barrier for eficient long trafic analysis and generation,” 2024, arXiv:2403.05822.

[28] X.-Y. Chen, L. Han, D.-C. Zhan, and H.-J. Ye, “Miett: Multi-instance encrypted trafic transformer for encrypted trafic classification,” in Proc. 39th AAAI Conf. Artif. Intell., vol. 39, 2025, pp. 15922–15929.

[29] Z. Hang, Y. Lu, Y. Wang, and Y. Xie, “Flow-MAE: Leveraging masked AutoEncoder for accurate, eficient and robust malicious traffic classification,” in Proc. 26th Int. Symp. Res. Attacks, Intrusions Defenses, Oct. 2023, pp. 297–314.

[30] T. Wang, X. Xie, W. Wang, C. Wang, Y. Zhao, and Y. Cui, “Netmamba: Eficient network trafic classification via pre-training unidirectional mamba,” in Proc. IEEE 32nd Int. Conf. Netw. Protocols (ICNP), Oct. 2024, pp. 1–11.

[31] M. Zhan, J. Yang, D. Jia, and G. Fu, “EAPT: An encrypted trafic classification model via adversarial pre-trained transformers,” Comput. Netw., vol. 257, Feb. 2025, Art. no. 110973.

[32] C. Fu, Q. Li, E. Bertino, and K. Xu, “Training with only 1.0% samples: Malicious trafic detection via cross-modality feature fusion,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., Nov. 2025, pp. 3930–3944.

[33] N. Wickramasinghe, A. Shaghaghi, G. Tsudik, and S. Jha, “SoK: Decoding the enigma of encrypted network trafic classifiers,” in Proc. IEEE Symp. Secur. Privacy (SP), May 2025, pp. 1825–1843.

[34] A. Dosovitskiy et al., “An image is worth 16×16 words: Transformers for image recognition at scale,” 2020, arXiv:2010.11929.

[35] D. Qin et al., “Mobilenetv4: Universal models for the mobile ecosystem,” in Proc. Eur. Conf. Comput. Vis., 2024, pp. 78–96.

[36] S. Wang, B. Z. Li, M. Khabsa, H. Fang, and H. Ma, “Linformer: Selfattention with linear complexity,” 2020, arXiv:2006.04768.

[37] Z. Liu et al., “Swin transformer: Hierarchical vision transformer using shifted windows,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), Oct. 2021, pp. 10012–10022.

[38] C. Wen, X. Li, H. Huang, Y.-S. Liu, and Y. Fang, “3D shape contrastive representation learning with adversarial examples,” IEEE Trans. Multimedia, vol. 27, pp. 679–692, 2023.

[39] Z. Zhang and M. R. Sabuncu, “Generalized cross entropy loss for training deep neural networks with noisy labels,” in Proc. Adv. Neural Inf. Process. Syst., vol. 31, 2018, pp. 8792–8802.

[40] A. Vaswani et al., “Attention is all you need,” in Proc. Adv. Neural Inf. Process. Syst., vol. 30, 2017, pp. 5998–6008.

[41] S. Dadkhah, H. Mahdikhani, P. K. Danso, A. Zohourian, K. A. Truong, and A. A. Ghorbani, “Towards the development of a realistic multidimensional IoT profiling dataset,” in Proc. 19th Annu. Int. Conf. Privacy, Secur. Trust (PST), Aug. 2022, pp. 1–11.

[42] C. Coldwell et al., “Machine learning 5G attack detection in programmable logic,” in Proc. IEEE Globecom Workshops (GC Wkshps), Dec. 2022, pp. 1365–1370.

[43] Stratosphere Malware Capture Facility Project Datasets. Accessed: Jul. 2025. [Online]. Available: https://mcfp.felk.cvut.cz/publicDatasets/

[44] S. Garcia, A. Parmisano, and M. J. Erquiaga, “IoT-23: A labeled dataset with malicious and benign IoT network trafic,” Version 1.0.0, Zenodo, Stratosphere Lab., Czech Tech. Univ. Prague, Prague, Czech Republic, 2020, doi: 10.5281/zenodo.4743746.

[45] D. Herzalla, W. T. Lunardi, and M. Andreoni, “TII-SSRC-23 dataset: Typological exploration of diverse trafic patterns for intrusion detection,” IEEE Access, vol. 11, pp. 118577–118594, 2023.

[46] H. He, Z. Yang, and X. Chen, “Payload encoding representation from transformer for encrypted trafic classification,” ZTE Commun., vol. 19, no. 4, p. 90, 2021.
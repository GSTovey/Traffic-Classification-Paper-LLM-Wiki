# AN-Net: an Anti-Noise Network for Anonymous Traffic Classification

Xianwen Deng

School of Electronic Information and Electrical Engineering

Shanghai Jiao Tong University Shanghai, China

2594306528@sjtu.edu.cn

Yijun Wang∗

School of Electronic Information and Electrical Engineering

Shanghai Jiao Tong University Shanghai, China

ericwyj@sjtu.edu.cn

Zhi Xue∗

School of Electronic Information and Electrical Engineering

Shanghai Jiao Tong University Shanghai, China

zxue@sjtu.edu.cn

# ABSTRACT

Anonymous networks employ a triple proxy to transmit packets to enhance user privacy, causing traffic packets from all applications and web services to form a unified flow. The traditional approach of applying flow-level encrypted traffic classification methods to anonymous traffic (i.e., treating consecutive packets as a single flow) is hindered by irrelevant packet noise. Moreover, fluctuations in the network environment can introduce per-packet attribute noise and discrepancies between training and test data. How to extract robust patterns from consecutive packets replete with noise remains a key challenge. In this paper, we propose the Anti-Noise Network (AN-Net) to construct robust short-term representations for a single modality, effectively countering irrelevant packet noise. We also incorporate an enhanced multi-modal fusion approach to combat per-packet attribute noise. AN-Net achieves state-of-the-art performance across two anonymous traffic classification tasks and one VPN traffic classification task, notably elevating the F1 score of SJTU-AN21 to 94.39% (6.24%↑). Our code and dataset are available on https://github.com/SJTU-dxw/AN-Net.

# CCS CONCEPTS

• Information systems → Traffic analysis; • Security and privacy → Network security; • Computing methodologies → Artificial intelligence.

# KEYWORDS

Anonymous Traffic Classification, Irrelevant Packet Noise, Per-Packet Attribute Noise, Short-Term Representation, Multi-Modal Fusion

# ACM Reference Format:

Xianwen Deng, Yijun Wang, and Zhi Xue. 2024. AN-Net: an Anti-Noise Network for Anonymous Traffic Classification. In Proceedings of the ACM Web Conference 2024 (WWW ’24), May 13–17, 2024, Singapore, Singapore. ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/3589334.3645691

![](images/d471db2c8d9eb84fbb225c3c6e9593a978dfcab3916f560e4d9096c9a60ddea4.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph (a) Encrypted Network
        Client1["Client"] -->|Flow I| Tor1["Tor Networks (Triple Proxy)"]
        Client2["Client"] -->|Flow II| Tor1
        Client3["Client"] -->|Flow III| Tor1
        Tor1 -->|Flow I| Websites1["Websites"]
        Tor1 -->|Flow II| Twitter1["Twitter"]
        Tor1 -->|Flow III| Facebook1["Facebook"]
        Tor1 -->|Flow III| S1["S"]
    end
    subgraph (b) Anonymous Network
        Client4["Client"] -->|Flow I| Administrator1["Administrator"]
        Administrator1 -->|Flow I| Tor4
        Administrator1 -->|Flow I| Tor4
        Tor4 -->|Flow I| Facebook2["Facebook"]
        Tor4 -->|Flow I| Twitter2["Twitter"]
        Tor4 -->|Flow I| Facebook3["Facebook"]
        Tor4 -->|Flow I| S2["S"]
    end
```
</details>

Figure 1: Threat models of encrypted network traffic classification and anonymous network traffic classification.

# 1 INTRODUCTION

Network traffic classification plays a critical role in quality of service (QoS) enhancement, resource usage planning, and even malware detection [6, 31, 35]. Recently, various traffic encryption techniques have been employed [18, 28], such as SSL, for protecting user privacy. However, these encryption mechanisms also help malicious traffic evade the surveillance system, thus bringing great challenges to traffic classification [7]. Traditional deep packet inspection (DIP) based methods [15, 32], which explore regular expression for matching the payload data, fail to identify encrypted traffic since the payload data is changed relying on the encryption algorithm. Therefore, encrypted traffic classification has become a research hotspot in recent years.

Over the past decade, many different methods have been proposed to classify encrypted traffic, which can be divided into three categories according to the types of input: statistical feature-based methods, sequential attribute-based methods, and raw traffic-based methods. Early works [2, 3, 12, 13, 37] extract the statistical features at the flow level (e.g., mean, minimum, maximum, and standard deviation of packet sizes in a flow) to train the machine learningbased classifier. These methods rely on expert-designed features heavily and have limited generalization ability. Recently, some deep learning-based methods [24, 26, 34] automatically learn complicated patterns from the raw flow attribute sequences (e.g., packet sizes in a flow), and achieve significant performance improvement. However, these methods require a large number of labeled data to train the deep learning-based models for more robustness. As a comparison, raw traffic-based methods [25, 42] directly capture the implicit and robust patterns in the encrypted payload at flow level using complicated models. In addition to large amounts of labeled data, these methods are also limited by long training time and high requirements on computing resources.

![](images/4cd4cb938ed05e65eb6cf59d1eef7802bdaae8f2e8453b3054b1f2d71917729b.jpg)

<details>
<summary>line</summary>

| Number of Packets | ISCX-Tor Probability (%) | Cross-Platform Probability (%) | Browser Probability (%) |
| ----------------- | ------------------------- | ------------------------------- | ------------------------ |
| 0                 | 100                       | 100                             | 100                      |
| 10                | 66                        | 52                              | 49                       |
| 50                | ~50                       | ~30                             | ~25                      |
</details>

Figure 2: The relationship between the number of consecutive packets and the probability that they belong to the same flow. Consecutive packets in short-term are likely to originate from the same flow.

Most importantly, the majority of encrypted traffic classification methods described above is based on flow-level features. Flow level aggregation is beneficial for extracting robust patterns, but also limits the effectiveness in special cases, e.g., the anonymous network. As illustrated in Figure 1, tor network, the most mainstream anonymous network, uses triple proxy to transmit traffic packets for protecting user privacy. As a result, traffic packets from all applications or web services form a single flow. The conventional approach of applying flow-level encrypted traffic classification methods to anonymous traffic is to take consecutive packets as a flow [45]. Obviously, this approach cannot guarantee that all packets originate from the same web service. Therefore, the key difference between anonymous traffic and encrypted traffic is noise, i.e., irrelevant packets from other flows, denoted as irrelevant packet noise.

Extracting robust patterns from consecutive packets full of noisy packets is crucial for anonymous traffic classification. Fu et.al. [17] found that most flows completed in less that 2 seconds, which indicates that consecutive packets in short-term are likely to originate from the same flow. Inspired by their observation, we visualize the number of consecutive packets and their probability of belonging to the same flow on ISCX-nonTor [22], Cross-Platform [38], and Browser datasets (see Figure 2). For simplicity, we use the first 1 × 104 packets of each pcap file to plot the figure. Results show that consecutive packets in long-term have a high probability of not belonging to the same flow, but packets in short-term are likely to originate from the same. Therefore, anonymous traffic classification methods should learn to model short-term features with low noise and then aggregate them for robust representation.

In addition to irrelevant packet noise, fluctuations in the network environment can introduce noise in the per-packet attributes, denoted as per-packet attribute noise. For example, internal arrival time (IAT) is likely to be affected by network congestion and timeto-live (TTL) may also change due to network routing. Therefore, extracting robust patterns from noisy per-packet attributes is also important for anonymous traffic classification. Considering that traffic packets usually have more than one attribute, e.g., packet size, IAT, TTL, etc., a good idea to combat the interference of per-packet attribute noise is to combine attributes from different modalities.

In this paper, we propose an Anti-Noise Network (AN-Net) for classifying anonymous traffic via short-term representation building and enhanced multi-modal fusion. It aims to learning robust patterns from anonymous traffic full of irrelevant packet noise and per-packet attribute noise. We first propose a Uni-modal Short-term Representation Learning Module. It divides consecutive packets in a "flow" into multiple short-term packet sequences. Short-term features are then extracetd from them by using the Short-term Feature Extraction Module (SFEM). Once short-term features are extracted, they are fed into the Short-term Representation Aggregation Module (SRAM), which aggregates the short-term features into flow-level representation. The SRAM is specifically designed to identify which short-term features come from irrelevant flows and which ones originate from the target flow by adopting a novel high temperature self-attention mechanism, thus helps resist the irrelevant packet noise. Finally, flow-level representations from different modalities are fused in the Enhanced Multi-modal Representation Fusion Module to combat the per-packet attribute noise.

The main contributions of this paper are summarized as follows:

• We present a Uni-modal Short-term Representation Learning Module to construct robust short-term representations for a single modality to resist irrelevant packet noise. We design a novel high temperature self-attention mechanism, which pays less attention to noise packets.   
• We propose to fuse representations from different modalities to combat per-packet attribute noise. A novel representation enhancement strategy is employed to further improve fusion performance.   
• AN-Net achieves SOTA performance over two anonymous traffic classification tasks and one VPN traffic classification task. Moreover, it exhibits strong robustness against injected noise packet attacks.

# 2 RELATED WORK

# 2.1 Conventional Traffic Classification

Port-based methods [30] identify the application type based on the port used. Their efficiency declined with the increase use of dynamic ports [8] and default ports [14]. Payload-based methods [6, 15, 21, 32, 33], also called deep packet inspection (DPI), explore the specific signature strings for matching the payload data. These methods are unable to classify encrypted traffic because the signature strings cannot be obtained from payloads after encryption.

# 2.2 Encrypted Traffic classification

Encrypted traffic classification methods can be divided into three categories according the the types of input: statistical feature-based methods, sequential attribute-based methods, and raw traffic-based methods.

![](images/67a91096493c663bf8406e98a02d19896aa9a6cba59067fcd26156f78fc7d545.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Flow Division"] --> B["Short-Term Feature Extraction"]
    B --> C["Per-Packet Attribute/Payload"]
    C --> D["Packet Parser"]
    D --> E["High Temperature Self-Attention"]
    E --> F["Add & Norm"]
    F --> G["Feed Forward"]
    G --> H["Add & Norm"]
    H --> I["Pooling"]
    I --> J["Uni-Modal Representation"]
    
    subgraph Module_A
        B1["SFEM"] --> B2["SFEM"]
        B3["SFEM"] --> B4["SFEM"]
    end
    
    subgraph Module_B
        M1["Res"] --> M2["Add & Norm"]
        M3["Res"] --> M4["Feed Forward"]
        M5["Res"] --> M6["Add & Norm"]
        M7["Res"] --> M8["Pooling"]
    end
```
</details>

![](images/a494e019b6e17210c1f04576f858077b25b9275b332e5e1df6ceb50305a8605a.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Uni-Modal Representation"] --> B["Selection Module"]
    C["Uni-Modal Representation"] --> B
    D["Uni-Modal Representation"] --> B
    E["Uni-Modal Representation"] --> B
    F["Uni-Modal Representation"] --> B
    G["Uni-Modal Representation"] --> B
    H["Uni-Modal Representation"] --> B
    I["Uni-Modal Representation"] --> B
    J["Uni-Modal Representation"] --> B
    K["Uni-Modal Representation"] --> B
    L["Uni-Modal Representation"] --> B
    M["Uni-Modal Representation"] --> B
    N["Uni-Modal Representation"] --> B
    O["Uni-Modal Representation"] --> B
    P["Uni-Modal Representation"] --> B
    Q["Uni-Modal Representation"] --> B
    R["Uni-Modal Representation"] --> B
    S["Uni-Modal Representation"] --> B
    T["Uni-Modal Representation"] --> B
    U["Uni-Modal Representation"] --> B
    V["Uni-Modal Representation"] --> B
    W["Uni-Modal Representation"] --> B
    X["Uni-Modal Representation"] --> B
    Y["Uni-Modal Representation"] --> B
    Z["Uni-Modal Representation"] --> B
    AA["Uni-Modal Representation"] --> B
    AB["Uni-Modal Representation"] --> B
    AC["Uni-Modal Representation"] --> B
    AD["Uni-Modal Representation"] --> B
    AE["Uni-Modal Representation"] --> B
    AF["Uni-Modal Representation"] --> B
    AG["Uni-Modal Representation"] --> B
    AH["Uni-Modal Representation"] --> B
    AI["Uni-Modal Representation"] --> B
    AJ["Uni-Modal Representation"] --> B
    AK["Uni-Modal Representation"] --> B
    AL["Uni-Modal Representation"] --> B
    AM["Uni-Modal Representation"] --> B
    AN["Uni-Modal Representation"] --> B
    AO["Uni-Modal Representation"] --> B
    AP["Uni-Modal Representation"] --> B
    AQ["Uni-Modal Representation"] --> B
    AR["Uni-Modal Representation"] --> B
    AS["Uni-Modal Representation"] --> B
    AT["Uni-Modal Representation"] --> B
    AU["Uni-Modal Representation"] --> B
    AV["Uni-Modal Representation"] --> B
    AW["Uni-Modal Representation"] --> B
    AX["Uni-Modal Representation"] --> B
    AY["Selection Module"] --> AZ["Selection Module"]
    AZ --> BA["Selection Module"]
    BA --> BB["Selection Module"]
    BB --> BC["Selection Module"]
    BC --> BD["Selection Module"]
    BD --> BE["Selection Module"]
    BE --> BF["Selection Module"]
    BF --> BG["Selection Module"]
    BG --> BH["Selection Module"]
    BH --> BI["Selection Module"]
    BI --> BJ["Selection Module"]
    BJ --> BK["Selection Module"]
    BK --> BL["Selection Module"]
    BL --> BM["Selection Module"]
    BM --> BN["Selection Module"]
    BN --> BO["Selection Module"]
    BO --> BP["Selection Module"]
    BP --> BP1["Selection Module"]
    BP1 --> BP2["Selection Module"]
    BP2 --> BP3["Selection Module"]
    BP3 --> BP4["Selection Module"]
    BP4 --> BP5["Selection Module"]
    BP5 --> BP6["Selection Module"]
    BP6 --> BP7["Selection Module"]
    BP7 --> BP8["Selection Module"]
    BP8 --> BP9["Selection Module"]
    BP9 --> BP10["Selection Module"]
    BP10 --> BP11["Selection Module"]
    BP11 --> BP12["Selection Module"]
    BP12 --> BP13["Selection Module"]
    BP13 --> BP14["Selection Module"]
    BP14 --> BP15["Selection Module"]
    BP15 --> BP16["Selection Module"]
    BP16 --> BP17["Selection Module"]
    BP17 --> BP18["Selection Module"]
    BP18 --> BP19["Selection Module"]
    BP19 --> BP20["Selection Module"]
    BP20 --> BP21["Selection Module"]
    BP21 --> BP22["Selection Module"]
    BP22 --> BP23["Selection Module"]
    BP23 --> BP24["Selection Module"]
    BP24 --> BP25["Selection Module"]
    BP25 --> BP26["Selection Module"]
    BP26 --> BP27["Selection Module"]
    BP27 --> BP28["Selection Module"]
    BP28 --> BP29["Selection Module"]
    BP29 --> BP30["Selection Module"]
    BP30 --> BP31["Selection Module"]
    BP31 --> BP32["Selection Module"]
    BP32 --> BP33["Selection Module"]
    BP33 --> BP34["Selection Module"]
    BP34 --> BP35["Selection Module"]
    BP35 --> BP36["Selection Module"]
    BP36 --> BP37["Selection Module"]
    BP37 --> BP38["Selection Module"]
    BP38 --> BP39["Selection Module"]
    BP39 --> BP40["Selection Module"]
    BP40 --> BP41["Selection Module"]
    BP41 --> BP42["Selection Module"]
    BP42 --> BP43["Selection Module"]
    BP43 --> BP44["Selection Module"]
    BP44 --> BP45["Selection Module"]
    BP45 --> BP46["Selection Module"]
    BP46 --> BP47["Selection Module"]
    BP47 --> BP48["Selection Module"]
    BP48 --> BP49["Selection Module"]
    BP49 --> BP50["Selection Module"]
```
</details>

Figure 3: Overview of AN-Net Framework.

2.2.1 Machine Learning Based Encrypted Traffic Classification. Statistical feature-based methods use ML-based models for classification. These methods propose to leverage statistical features at flowlevel (e.g., mean, minimum, maximum, and standard deviation of packet sizes in a flow) to solve encrypted traffic classification problem combined with machine learning algorithms [1, 4, 12, 27, 37]. AppScanner [37] trains random forest classifiers by exploiting statistical features of packet sizes, while Gerard et.al. [12] trains C4.5 decision tree and KNN classifiers using time-related features. As a supplement of statistical features, Whisper [16] extracts the frequency domain features of flows and uses clustering algorithms for classification. These methods rely heavily on professional knowledge and it is difficult to design generic statistical features to handle different applications.   
2.2.2 Deep Learning Based Encrypted Traffic Classification. Some statistical feature-based methods [44] also apply DL-based models for better representation extraction capabilities, and they also rely on human-designed features and have limited generalization ability. As an alternative, sequential attribute-based methods [5, 24, 26, 34, 36] extracts discriminative representations from raw sequential attributes (e.g., packet sizes in a flow). Flowlens [5] computes for each flow a memory-efficient representation of packet sizes named "flow marker". FlowPic [34] transforms raw packet size sequences and arrival interval sequences in a flow into an intuitive picture. FS-Net [26] uses recurrent neural networks (RNN) to automatically extract representations from raw packet size sequences. Another alternative approach is to learning implicit representations from

raw traffic. Raw traffic-based methods [24, 25, 29, 42] directly capture the implicit and robust patterns in the encrypted payload at flow level using complicated DL-based models.

However, the majority of encrypted traffic classification methods described above is based on flow-level features, which limits their effectiveness in anonymous networks, where the traffic from all applications or web services form a single flow. Moreover, None of these methods paid attention to the unreliability of per-packet attributes and attempted to solve it by combining information from different modalities. In this paper, we propose to build strong shortterm representations to resist irrelevant packet noise, and adopt an enhanced multi-modal fusion module to combat per-packet attribute noise.

# 3 AN-NET

In this paper, we aim to accurately classify anonymous network traffic under the interference of irrelevant packet noise and per-packet attribute noise. To this end, we propose an Anti-Noise network (AN-Net) (see Figure 3) to build strong short-term representations for a single modality to resist irrelevant packet noise (Secion 3.1) and achieve enhanced multi-modal fusion to combat per-packet attribute noise (Secion 3.2).

# 3.1 Short-term Representation Learning

In this section, we propose a Uni-modal Short-term Representation Learning Module to build short-term representations for resisting irrelevant packet noise.

3.1.1 Flow Division and Packet Parsing. Given a "flow" that consists of consecutive packets ?? of length ??, we first divide ?? into ?? parts and obtain multiple short-term consecutive packet sequences: $P = [ P _ { 1 } , P _ { 2 } , \cdot \cdot \cdot , P _ { N } ]$ . As illustrated in Figure $^ { 2 , }$ packets in shortterm are likely to originate from the same flow. Therefore, features extracted from short-term packet sequences are more likely to be immune to the interference of irrelevant packet noise. Then we parse out the short-term per-packet attribute/payload sequences for classification, denoted as $A = [ A _ { 1 } , A _ { 2 } , \cdot \cdot \cdot , A _ { N } ] ,$ , where $A _ { i }$ is a short-term per-packet attribute/payload sequence.

3.1.2 Short-term Feature Extraction. We design two Short-term Feature Extraction Modules (SFEM) to extract short-term features from raw data and statistical data respectively, denoted as Raw-SFEM and Stat-SFEM.

Suppose the input is a short-term per-packet payload sequence $A _ { i } \in \mathbb { R } ^ { l \times d }$ , where ?? is the length of the short-term sequence and ?? is the length of payload, Raw-Stat employs a bidirectional GRU to extract the short-term feature: $F _ { i } = G R U ( A _ { i } ) \ \in \ \mathbb { R } ^ { C } ,$ , where ?? represents the hidden dimension of short-term features. If the input is a short-term per-packet attribute sequence $A _ { i } \in \mathbb { R } ^ { l \times 1 } \left( \mathrm { e . g . } \right.$ packet size), Raw-Stat first embeds each attribute to a vector via an embedding layer, and then also uses a bidirectional GRU to extract the short-term feature $F _ { i } \in \mathbb { R } ^ { C }$ . The extracted short-term features are denoted as ${ \cal F } = [ F _ { 1 } , F _ { 2 } , \cdots , F _ { N } ] \in \mathbb { R } ^ { N \times C }$ .

Stat-SFEM can only deal with attribute sequences. It first extracts 7 general statistical features (i.e., mean, max, min, median, standard deviation, skewness, and kurtosis) and the frequency domain features from these short-term attribute sequences as the shortterm statistical features, denoted as $T = [ T _ { 1 } , T _ { 2 } , \cdot \cdot \cdot , T _ { N } ]$ . Then it employs a MLP to extract the short-term feature $F _ { i }$ for each shortterm statistic feature: $F _ { i } = M L P ( T _ { i } ) \in \mathbb { R } ^ { C }$ . The MLP consists of two fully-connected layers and one ReLU layer between them. Despite its simplicity, the MLP is able to extract discriminative features thanks to the high-level statistical features and the nonlinear transformation of the ReLU layer. Thanks to the high-level statistical features, Stat-SFEM exhibits higher stability than Raw-SFEM when training data collection environment is inconsistent with the actual test environment, as detailed in Section 4.5.

3.1.3 Short-term Representation Aggregation. Once short-term features $F \in \mathbb { R } ^ { N \times C }$ are extracted, we use the Short-term Representation Aggregation Module (SRAM) to aggregate the short-term features $\bar { F } \in \bar { \mathbb { R } } ^ { N \times C }$ into flow-level representation ?? . Since shortterm features may also come from irrelevant flows, it is critical to distinguish among ?? short-term features which ones originate from the irrelevant flow and which ones come from the target flow. We design a novel high temperature self-attention mechanism to achieve this. Specifically, the SRAM is composed of a Transform Layer [39] and a Pooling layer. A normal Transformer layer consists of two key sub-layers: self-attention layer and feed forward layer. Each sub-layer uses the residual structure [19] to avoid the degradation problem that occurs as the depth of the network increases.

Given the short-term features ${ \cal F } = [ F _ { 1 } , F _ { 2 } , \cdots , F _ { N } ] \in \mathbb { R } ^ { N \times C }$ , the self-attention layer first calculate Query Matrix ?? by using linear transformation:

$$
Q = F W ^ {Q} = \left[ q _ {1}, q _ {2}, \dots q _ {N} \right] ^ {T}, \tag {1}
$$

where $W ^ { Q } \in \mathbb { R } ^ { C \times D }$ is learnable parameter, ?? represents the hidden dimension of the self-attention layer, and $q _ { i } \in \mathbb { R } ^ { D }$ denotes the query vector of i-th short-term feature $F _ { i }$ . Similarly, we calculate Key Matrix and Value Matrix by another two linear transformations:

$$
K = F W ^ {K} = \left[ k _ {1}, k _ {2}, \dots k _ {N} \right] ^ {T}, \tag {2}
$$

$$
V = F W ^ {V} = \left[ v _ {1}, v _ {2}, \dots v _ {N} \right] ^ {T}, \tag {3}
$$

where $k _ { i }$ denotes the key vector and $v _ { i }$ denotes the value vector of i-th short-term feature $F _ { i }$ . Then, considering the query vector of i-th short-term feature $q _ { i }$ , we compute the dot products of $q _ { i }$ and key vectors of all short-term features:

$$
S _ {i} = \left[ q _ {i} \cdot k _ {1} ^ {T}, q _ {i} \cdot k _ {2} ^ {T}, \dots , q _ {i} \cdot k _ {N} ^ {T} \right] = \left[ s _ {i 1}, s _ {i 2}, \dots , s _ {i N} \right], \tag {4}
$$

where $s _ { i j }$ is the similarity between $q _ { i }$ and $k _ { j } ,$ , and reflects the importance of j-th short-term feature to i-th short-term feature. Normal self-attention layer scales dot products ???? by $\scriptstyle { \frac { 1 } { \sqrt { D } } }$ before applying a softmax function to make the sum of the elements be 1:

$$
\mathcal {W} _ {i} = \text { softmax } (\frac {S _ {i}}{\sqrt {D}}) = [ w _ {i 1}, w _ {i 2}, \dots , w _ {i N} ], \sum_ {j = 1} ^ {N} w _ {i j} = 1, \tag {5}
$$

The output at i-th position is then calculated using weighted summation over value vectors of all short-term features $V { : }$

$$
z _ {i} = \mathcal {W} _ {i} V = \sum_ {j = 1} ^ {N} w _ {i j} v _ {j}. \tag {6}
$$

Finally, the output of self-attention layer on all short-term features $F$ is represented as: $S e l f A t t n ( F ) = [ z _ { 1 } , z _ { 2 } , \cdot \cdot \cdot , z _ { N } ]$ . The above process can also be expressed in matrix form:

$$
\text { SelfAttn } (F) = \text { softmax } (\frac {Q K ^ {T}}{\sqrt {D}}) V. \tag {7}
$$

As stated above, the original self-attention layer scales the dot products ???? by $\scriptstyle { \frac { 1 } { \sqrt { D } } }$ before applying a softmax function. Wei et.al. [41] demonstrated that increasing the magnitude ||???? || will cause a sharp distribution for softmax weight score $\mathcal { W } _ { i } .$ . Original self-attention layer reduces the magnitude ||???? || by scaling by $\scriptstyle { \frac { 1 } { \sqrt { D } } }$ to avoid the softmax function from producing extremely small weights in $\mathcal { W } _ { i }$ However, in the anonymous traffic classification scenario, since some short-term features may come from irrelevant flows, a sharp distribution for softmax weight score $\mathcal { W } _ { i }$ needs to be generated to resist irrelevant packet noise. To this end, we design a novel high temperature self-attention mechanism by increasing the magnitude of dot products:

$$
H T - S e l f A t t n (F) = \text { softmax } (\frac {\mathcal {N} (Q) \mathcal {N} (K) ^ {T}}{\tau}) V, \tag {8}
$$

where N is the normalize function that makes the vector norm equal to 1 and ?? is the temperature hyper-parameter. Note that the real temperature is the reciprocal of ??. After employing a high temperature, the softmax function produces extremely small weights for short-term features from irrelevant flows. The theoretical analysis of the high temperature self-attention mechanism are detailed in Appendix A.

The feed forward layer can enhance the expression ability of the output features by mapping them to high-latitude space and then back to low-latitude space through two linear transformations. In the middle of them, a GeLU layer [20] is adopted to alleviate the vanishing gradient problem.

Finally, the short-term features are aggregated into flow-level uni-modal representation ?? by using an Average Pooling layer.

# 3.2 Multi-modal Representation Fusion

In this section, we propose the Enhanced Multi-modal Representation Fusion Module to fuse flow-level representations from different modalities for combating per-packet attribute noise.

3.2.1 Modal Selection. Before fusing representations from different modalities, we resort to information leakage [23] to remove useless modalities. We utilize the mutual information between statistical features ?? of each modality and the ground truth labels ?? to measure the importance of this modality:

$$
I (T; G) = H (G) - H (G | T). \tag {9}
$$

Representations from modalities with high information leakage are then fused to obtain the final robust representation.

3.2.2 Representation Enhancement. As mentioned above, the unreliability of per-packet attributes may make the representation of certain modalities full of noise. A conventional approach to combat input noise is to employ data augmentation strategy, which has been widely used in CV [9–11] and NLP [40, 43]. However, due to the limitation of input data type (i.e., numeric values), few data augmentation methods have been proposed to cope with encrypted traffic classification. To this end, we propose a novel representation enhancement strategy to perform data augmentation in representation-level.

Given representations from ?? modalities $[ Z _ { 1 } , Z _ { 2 } , \cdots , Z _ { M } ]$ , we perform data augmentation on representation from each modality, respectively:

$$
\hat {Z} _ {i} = \left\{ \begin{array}{c c} 0, & p \\ B \times Z _ {i}, & 1 - p \end{array} \right. \tag {10}
$$

where ?? is a random probability and ?? is a scaling factor sampled from Beta distribution. Note that the representation-level data augmentation will only be adopted during the training phase. For a uni-modal representation, we randomly drop it to force the model to learn from other modalities, or scale it to make the model learn more robust patterns. We compare the representation enhancement strategy with other fusion techniques and provide a theoretical analysis in Appendix B.

3.2.3 Representation Fusion. We then aggregate the enhanced representations from different modalities into the final multi-modal representation by using an Average Pooling layer:

$$
\overline {{Z}} = A v g P o o l i n g ([ \hat {Z} _ {1}, \hat {Z} _ {2}, \dots , \hat {Z} _ {M} ]). \tag {11}
$$

Finally, we make the prediction on it with a fully-connected layer ${ \hat { Y } } = F C ( { \overline { { Z } } } )$ , and train the whole model through cross-entropy loss:

$$
\mathcal {L} = C E (\hat {Y}, Y), \tag {12}
$$

where ?? is the ground-truth label.

# 4 EXPERIMENTS

# 4.1 Experiment Setup

4.1.1 Datasets. To evaluate the effectiveness and generalization of AN-Net, we conduct experiments on two anonymous traffic datasets [22, 44] and one VPN traffic dataset [12]. Note that we take 100 consecutive packets as a flow. SJTU-AN21 provides a test set separately, which is collected in a different network environment than the training set. For other two datasets, we divide them into the training set and the test set according to the proportion of 80% and 20% for each class.

4.1.2 Baselines. We use seven state-of-the-art flow-level encrypted traffic classification methods covering three basic categories as baselines. For a fair comparison, all methods use the same partitioned flows for training and test.

• AppScanner (Statistical features and ML-based model). AppScanner [37] trains random forest classifiers by exploiting statistical features of packet sizes at flow-level. We retrained the ML-based model using the default hyper-parameter settings in their paper.   
• Decision Tree (Statistical features and ML-based model). Gerard et.al. [12] trains C4.5 decision tree using statistical features of internal arrivals at flow-level. Likewise, we use the default settings.   
• Whisper (Statistical features and ML-based model). Whisper [16] extracts the frequency domain features of packet sizes at flow-level as a supplementation of conventional statistical features, and uses clustering algorithms for classification. We reproduce Whisper on three datasets without modifications and then retrain the ML-based model.   
• Flowlens (Sequential attributes and ML-based model). Flowlens [5] computes for each flow a memory-efficient representation of packet sizes named "flow marker", and uses a Multinomial Naive-Bayes classifier for classification. We retrained the ML-based model using the hyper-parameter settings that produce the most accurate results.   
• FS-Net (Sequential attributes and DL-based model). FS-Net [26] uses recurrent neural networks (RNN) to automatically extract representations from raw packet size sequences. A multi-layer encoder-decoder structure and the reconstruction mechanism are adopted to enhance the effectiveness of features. We use the default hyper-parameter setting in their paper.   
• AttnLSTM (raw traffic and DL-based model). AttnLSTM [42] is an end-to-end network based on the LSTM model to directly perform classification on raw traffic. It introduces an attention mechanism to score the importance of each flow. Similarly, we use the default setting in their paper.   
• ET-Bert (raw traffic and DL-based model). ET-Bert [25] pre-trains deep traffic representations from large-scale unlabeled raw traffic, then fine-tunes on a small amount of labeled data. We re-pretrain the model and finetune it on three datasets, respectively.

4.1.3 Evaluation Metrics and Implementation Details. We evaluate our AN-Net and compare it with other state-of-the-art methods by four typical metrics, including Accuracy (AC), Precision (PR), Recall (RC), and F1 [25, 38, 46]. In the training phase, we train the AN-Net with a stochastic gradient descent (SGD) optimizer, and the learning rate is set to 0.001. The batch size is 64 and the total steps is 50,000. The temperature hyper-parameter ?? is set to 0.1. The probability of randomly drop uni-modal representation ?? is set to 0.2 and the scaling factor ?? is sampled from beta distribution ?? ∼ ???? (4, 4). All the experiments are implemented using Pytorch 1.9.0 and trained on PC with Intel® Xeon® Gold 5218R CPU@2.10GHz, 256 GB RAM, and an NVIDIA GeForce RTX3090 GPU. The modal selection criteria is illustrated in Appendix I. For ISCX-VPN and ISCX-Tor datasets, we use Raw-SFEM for short-term feature extraction. For SJTU-AN21 dataset, we employ Stat-SFEM and drop the payload modality (see Section 4.5 for more details).

Table 1: Comparison Results on SJTU-AN21, ISCX-Tor, and ISCX-VPN datasets. 

<table><tr><td rowspan="2">DatasetMethod</td><td colspan="4">SJTU-AN21</td><td colspan="4">ISCX-Tor</td><td colspan="4">ISCX-VPN</td></tr><tr><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td></tr><tr><td>AppScanner [37]</td><td>0.7181</td><td>0.7535</td><td>0.7181</td><td>0.7038</td><td>0.8203</td><td>0.8117</td><td>0.8203</td><td>0.8022</td><td>0.7293</td><td>0.7378</td><td>0.7293</td><td>0.7193</td></tr><tr><td>Decision Tree [12]</td><td>0.5702</td><td>0.6630</td><td>0.5702</td><td>0.5621</td><td>0.8059</td><td>0.7926</td><td>0.8059</td><td>0.7942</td><td>0.8259</td><td>0.8204</td><td>0.8259</td><td>0.8211</td></tr><tr><td>Whisper [16]</td><td>0.4820</td><td>0.5629</td><td>0.4820</td><td>0.5066</td><td>0.6723</td><td>0.7886</td><td>0.6723</td><td>0.6975</td><td>0.5848</td><td>0.6027</td><td>0.5848</td><td>0.5486</td></tr><tr><td>Flowlens [5]</td><td>0.6943</td><td>0.7576</td><td>0.6943</td><td>0.7128</td><td>0.8003</td><td>0.8703</td><td>0.8003</td><td>0.8256</td><td>0.6336</td><td>0.6674</td><td>0.6336</td><td>0.5820</td></tr><tr><td>FS-Net [26]</td><td>0.8083</td><td>0.8233</td><td>0.8083</td><td>0.7949</td><td>0.9322</td><td>0.9342</td><td>0.9322</td><td>0.9315</td><td>0.8457</td><td>0.8502</td><td>0.8457</td><td>0.8398</td></tr><tr><td>AttnLSTM [42]</td><td>0.8120</td><td>0.8176</td><td>0.8120</td><td>0.8030</td><td>0.9725</td><td>0.9718</td><td>0.9725</td><td>0.9708</td><td>0.9778</td><td>0.9781</td><td>0.9778</td><td>0.9778</td></tr><tr><td>ET-Bert [25]</td><td>0.8661</td><td>0.9163</td><td>0.8661</td><td>0.8815</td><td>0.9525</td><td>0.9514</td><td>0.9525</td><td>0.9445</td><td>0.9885</td><td>0.9895</td><td>0.9885</td><td>0.9888</td></tr><tr><td>AN-Net (ours)</td><td>0.9476</td><td>0.9490</td><td>0.9476</td><td>0.9439</td><td>0.9951</td><td>0.9951</td><td>0.9951</td><td>0.9950</td><td>0.9996</td><td>0.9996</td><td>0.9996</td><td>0.9996</td></tr></table>

# 4.2 Comparison with State-of-the-Art Method

We compare AN-Net with seven state-of-the-art (SOTA) methods on three datasets. The experimental results are shown in Table 1. The seven methods can be devided into three categories: statistical feature-based methods (i.e., AppScanner, Decision Tree, and Whisper), sequential attribute-based methods (i.e., Flowlens and FS-Net), and raw traffic-based methods (i.e., AttnLSTM and ET-Bert).

SJTU-AN21. SJTU-AN21 [44] is a new anonymity network traffic dataset collected in the open network and the test set is collected separately in different network environment. Due to the interference of irrelevant packets and discrepancies between training and test data, previous methods never achieved more than 90% accuracy. According to Table 1, AN-Net significantly outperforms all existing methods. Specifically, AN-Net improves Accuracy and F1 by 8.15% and 6.24% respectively over the existing state of the art (i.e., ET-Bert). Previous methods designed for encrypted traffic classification ignored the noise of irrelevant packets and the unreliability of uni-modal attributes. As a comparison, we build strong short-term features and aggregate them with a carefully designed high temperature self-attention mechanism to resist irrelevant packet noise, and then propose to fuse representations from different modalities to combat per-packet attribute noise. Moreover, Stat-SFEM exhibits strong transfer capabilities thanks to the high-level statistical features when the network environments of the training data and test data are inconsistent (see Section 4.5 for more details).

ISCX-Tor. ISCX-Tor [22] is a frequently used Tor network traffic dataset. Compared with SJTU-AN21, this dataset is less noisy and significantly larger in size. Because of the purity and large amount of data, DL-based methods that directly learn from raw sequential attributes or raw traffic payload (i.e., FS-Net, AttnLSTM, and ET-Bert) perform very well. AN-Net has an accuracy of 99.50% and a F1 of 99.51%, slightly better than these three DL-based methods, and significantly outperforms other four ML-based methods (i.e., AppScanner, Decision Tree, Whisper, and Flowlens). For example, AN-Net achieves 2.42% and 5.05% improvement on F1 over AttnL-STM and ET-Bert, respectively. Although the amount of data is large enough to support raw traffic-based methods to extract implicit and robust features from payload, attributes from other modalities can still help improve model performance.

ISCX-VPN. ISCX-VPN [12] is a commonly used VPN traffic dataset. Similar to anonymous networks, VPN networks use proxies to transmit information for hiding IP information. Therefore, VPN traffic classification also suffers from irrelevant packet noise. AN-Net pushes F1 on ISCX-VPN to 99.96%. Our model achieves more than 15.98% improvement on F1 over statistical-based methods and sequential attribute-based methods, and performs slightly better than two raw traffic-based methods (2.18% and 1.08% improvement on F1 over AttnLSTM and ET-Bert). Moreover, AN-Net exhibits greater robustness against injected noise packet attacks (see Section 4.3).

# 4.3 Robustness Analysis

To evaluate the robustness of AN-Net, we assume that attackers construct injected noise packet attacks, i.e., injecting irrelevant packets into original traffic to evade supervision. In the experiments, for simplicity, we assume attackers randomly select packet sequences from the entire dataset as noise traffic. We then mix original traffic with noise traffic in different ratios, i.e., the proportion of noise traffic ranges from 0 to 75% (see Appendix H for more details). We do not inject a higher proportion of noise traffic because the effectiveness of other methods is already low. Figure 4 shows F1 scores of AN-Net and seven SOTA methods over three datasets under injected noise packet attacks. According to the results, we conclude that attackers cannot confuse AN-Net via injected noise packet attacks. However, attackers can fool other encrypted traffic classification models.

![](images/26bb82292e74691ef05fdae092eaf58ef616ef0e653d6c36a6e92e43d148b688.jpg)

Figure 4: F1 score of AN-Net and seven SOTA methods under injected noise packet attacks.   
Table 2: Ablation study on short-term features and high temperature (HT) self-attention mechanism. 

<table><tr><td rowspan="2">Feature</td><td rowspan="2">HT</td><td colspan="4">Noise Ratio</td></tr><tr><td>0</td><td>1/4</td><td>1/2</td><td>3/4</td></tr><tr><td>Long-Term</td><td>/</td><td>0.9427</td><td>0.9276</td><td>0.9093</td><td>0.7295</td></tr><tr><td rowspan="2">Short-Term</td><td>✘</td><td>0.9352</td><td>0.9329</td><td>0.9327</td><td>0.9068</td></tr><tr><td>✓</td><td>0.9439</td><td>0.9430</td><td>0.9423</td><td>0.9200</td></tr></table>

Raw traffic-based methods (i.e., AttnLSTM and ET-Bert) are very vulnerable to injected noise packet attacks. For instance, the F1 scores of ET-Bert and AttnLSTM on three datasets are reduced by at least 64.6% and 69.6% respectively. Payloads from irrelevant packets can easily lead to incorrect recognition results. Similarly, long-term statistical features (e.g., Maximum value, Mean value) can also be severely corrupted by inserted noise packets. Statistical featurebased methods (i.e., AppScanner, Decision Tree, and Whisper) have at most 43.0%, 36.5%, and 36.7% F1 score decrease over three datasets, respectively. As a comparison, sequential attribute-based methods (i.e., Flowlens and FS-Net) is more robust against irrelevant packet noise, since a part of clean original attribute sequences is retained. However, the F1 scores of FS-Net on the SJTU-AN21 and ISCX-VPN datasets still drop by 17.9% and 16.9%, respectively. In contrast, AN-Net maintains similar classification performance, where the F1 score fluctuations are less than 2.39% on SJTU-AN21 dataset and 0.32% on ISCX-VPN dataset. On ISCX-Tor dataset, due to the large amount of data, the F1 score of AN-Net drops by 8.8% to 90.71%, which is still higher than all other SOTA methods.

In summary, AN-Net can achieve robust classification because of the short-term representation learning and the multi-modal representation fusion. In particular, attackers cannot easily disrupt all short-term features of all modalities and thus AN-Net is robust against injected noise packet attacks.

# 4.4 Ablation Analysis

We provide an ablation analysis to verify the contribution of each component on SJTU-AN21 dataset. In addition to normal traffic, we also perform ablation experiments under injected noise packet attacks to prove the effectiveness of these components against noise.

![](images/ab697342cec19c53dd9e67ff4501a14be7aaf5b95e2d13afa8293cf1c6d6ced0.jpg)

<details>
<summary>line</summary>

| Temperature τ | SJTU-AN21 w/ HT | SJTU-AN21 w/o HT |
| ------------- | --------------- | ---------------- |
| 0.0           | 94.5            | 93.5             |
| 0.2           | 93.7            | 93.5             |
| 0.4           | 93.6            | 93.5             |
| 0.6           | 93.5            | 93.5             |
| 0.8           | 93.5            | 93.5             |
| 1.0           | 93.5            | 93.5             |
</details>

(a) 0% Noise Ratio

![](images/b2d7ed15cc15ec3368c1c9b78dc06a3cf274b32ced6bded362d92b3e9e763d93.jpg)

<details>
<summary>line</summary>

| Temperature τ | SJTU-AN21 w/ HT | SJTU-AN21 w/o HT |
| ------------- | --------------- | ---------------- |
| 0.0           | 91.6            | 90.5             |
| 0.2           | 91.8            | 90.5             |
| 0.4           | 91.6            | 90.5             |
| 0.6           | 91.4            | 90.5             |
| 0.8           | 91.2            | 90.5             |
| 1.0           | 91.0            | 90.5             |
</details>

(b) 75% Noise Ratio   
Figure 5: The impact of the temperature hyper-parameter ??.

4.4.1 Short-term Representation Learning. In this section, we ablate short-term features and high temperature (HT) self-attention mechanism, as shown in Table 2. We do not perform flow division and directly extract long-term statistical features when ablating short-term features. Then we use vanilla self-attention mechanism to substitute high temperature self-attention mechanism. As discussed above (Section 4.3), long-term statistical features are severely corrupted by inserted noise packets. Results show that the F1 score of using long-term features is 19.05% lower than using short-term features when the noise ratio of irrelevant packets is set to 75%. Therefore, it is crucial to model short-term features to combat irrelevant packet noise. Besides, high temperature selfattention mechanism improves model performance through paying less attention to noise packets. This improvement increases as the noise ratio increases, from 0.87% to 1.32%. The visualization of high temperature self-attention mechanism is shown in Appendix F.

We further investigate the impact of the temperature hyperparameter ??, as shown in Figure 5. Results show that AN-Net achieves better performance at higher temperatures. Note that the real temperature is the reciprocal of temperature hyper-parameter ??. The self-attention mechanism with a higher temperature generates a sharper distribution for weight score matrix, thus helps resist the irrelevant packet noise by paying little attention to noisy short-term features from irrelevant packets. When the temperature gradually decreases, the model performance gradually drops to the level of vanilla self-attention mechanism.

Table 3: Ablation study on multi-modalities. 

<table><tr><td>Packet Size</td><td>IAT</td><td>TTL</td><td>TCPFlag</td><td>AC</td><td>F1</td></tr><tr><td>√</td><td>✕</td><td>✕</td><td>✕</td><td>0.7958</td><td>0.8014</td></tr><tr><td>√</td><td>√</td><td>✕</td><td>✕</td><td>0.8314</td><td>0.8304</td></tr><tr><td>√</td><td>√</td><td>√</td><td>✕</td><td>0.9269</td><td>0.9234</td></tr><tr><td>√</td><td>√</td><td>√</td><td>√</td><td>0.9476</td><td>0.9439</td></tr></table>

Table 4: Ablation study on representation enhancement (RE) strategy. 

<table><tr><td rowspan="2">RE</td><td colspan="2">SJTU-AN21</td><td colspan="2">ISCX-Tor</td><td colspan="2">ISCX-VPN</td></tr><tr><td>1/2</td><td>3/4</td><td>1/2</td><td>3/4</td><td>1/2</td><td>3/4</td></tr><tr><td>✘</td><td>0.9378</td><td>0.9101</td><td>0.9334</td><td>0.8934</td><td>0.9957</td><td>0.9881</td></tr><tr><td>✓</td><td>0.9423</td><td>0.9200</td><td>0.9377</td><td>0.9071</td><td>0.9964</td><td>0.9933</td></tr></table>

4.4.2 Multi-modal Representation Fusion. In this section, we first construct an ablation study on multi-modalities. As shown in Table 3, the uni-modal model using packet size only achieves an F1 score of 80.14%. By combining the attributes of other modalities, the F1 score of the multi-modal model is increased to 94.39% (14.25%↑). On the one hand, attributes of different modalities can provide complementary information to support better decision-making. On the other hand, when the network environment fluctuates, the attributes of different modalities can verify each other to combat per-packet attribute noise.

We further construct an ablation study on representation enhancement (RE) strategy. As shown in Table 4, representation enhancement strategy improves model performance through performing data augmentation in representation-level to combat the noise of uni-modal representations. The improvement also increases as the noise ratio increases, from 0.45% to 0.99% on SJTU-AN21 dataset and from 0.43% to 1.37% on ISCX-Tor dataset. The unreliability of per-packet attributes and the noise of irrelevant packets both make the uni-modal representation full of noise. The representation-level data augmentation strategy enables AN-Net to learn robust multimodal representation from noisy uni-modal representations.

# 4.5 Stability Analysis

In this section, we provide an stability analysis to demonstrate that statistical features are more stable than raw attribute sequences or raw traffic payloads when training data collection environment is inconsistent with the actual test environment.

Specifically, we construct an comparison experiment to compare Stat-SFEM and Raw SFEM, and then perform an ablation experiment on the payload modality over SJTU-AN21 dataset. Results are shown in Table 5. It can be concluded that Stat-SFEM outperforms Raw-SFEM by a large margin (4.21% in Accuracy and 3.41% in F1 score) and adding payload modality slightly reduces model

Table 5: Comparison of Stat-SFEM and Raw-SFEM and ablation of payload modality on SJTU-AN21 dataset. 

<table><tr><td>SFEM</td><td>Payload</td><td>AC</td><td>F1</td></tr><tr><td>Raw-SFEM</td><td>✕</td><td>0.9055</td><td>0.9098</td></tr><tr><td rowspan="2">Stat-SFEM</td><td>√</td><td>0.9358</td><td>0.9391</td></tr><tr><td>✕</td><td>0.9476</td><td>0.9439</td></tr></table>

![](images/977435c57090a27c0937e05bb10be622a924ab7b824063b60aafb6439ac45c39.jpg)

<details>
<summary>line</summary>

| Iteration (10³) | Stat Model w/o Payload | Stat M |
| --------------- | ---------------------- | ------ |
| 0               | 0.4                    | 0.35   |
| 10              | 0.15                   | 0.08   |
| 20              | 0.12                   | 0.06   |
| 30              | 0.1                    | 0.05   |
| 40              | 0.09                   | 0.04   |
| 50              | 0.08                   | 0.03   |
</details>

![](images/aacca391c9c8ddfb02fe0a76c0466c7d355c3ab68b81c7d3f616f8dced0a5ee8.jpg)

<details>
<summary>line</summary>

| Iteration (10³) | Raw Model w/o Payload | Model w/ Payload |
| --------------- | --------------------- | ---------------- |
| 0               | 0.7                   | 0.7              |
| 10              | 0.3                   | 0.2              |
| 20              | 0.35                  | 0.2              |
| 30              | 0.4                   | 0.2              |
| 40              | 0.38                  | 0.2              |
| 50              | 0.35                  | 0.2              |
</details>

Figure 6: Training loss and test loss curves during training.

performance (1.18% in Accuracy and 0.48% in F1 score). We further plot the training loss and test loss curves during the training process, as shown in Figure 6. Stat model has the largest training loss, but the smallest test loss, which indicates that learning from raw attribute sequences or raw traffic payloads will suffer from severely overfitting. When training data collection environment is inconsistent with the actual test environment, some specific raw attribute sequences or raw traffic payloads that are very useful in training data may become ineffective in test data. For example, changes in encryption algorithms result in different payloads for the same plaintext. In contrast, high-level statistical features are more stable because they measure the distribution and variation of raw attribute sequences, and thus are more transferable.

# 5 CONCLUSION

In this paper, we propose a new anonymous traffic classification model, AN-Net, to construct robust short-term representations for a single modality and then combine representations from different modalities. AN-Net is able to resist irrelevant packet noise and per-packet attribute noise, thus exhibits strong robustness against injected noise packet attacks. We comprehensively evaluate the effectiveness and generalization of AN-Net on two anonymous traffic datasets and one VPN traffic dataset. Experimental results show that AN-Net achieves a new state-of-the-art performance, notably evelating the F1 score of SJTU-AN21 to 94.39% (6.24%↑). Moreover, AN-Net is more robust than existing works against injected noise packet attacks, because attackers cannot easily disrupt all short-term features of all modalities.

# ACKNOWLEDGMENTS

This work is supported by SJTU-QI’ANXIN Joint Lab of Information System Security. We are grateful to anonymous reviews for their constructive comments to improve this paper.

# REFERENCES

[1] Khaled Al-Naami, Swarup Chandra, Ahmad Mustafa, Latifur Khan, Zhiqiang Lin, Kevin Hamlen, and Bhavani Thuraisingham. 2016. Adaptive encrypted traffic fingerprinting with bi-directional dependence. In Proceedings of the 32nd Annual Conference on Computer Security Applications. 177–188.   
[2] Riyad Alshammari and A Nur Zincir-Heywood. 2008. Investigating two different approaches for encrypted traffic classification. In 2008 Sixth Annual Conference on Privacy, Security and Trust. 156–166.   
[3] Riyad Alshammari and A Nur Zincir-Heywood. 2009. Machine learning based encrypted traffic classification: Identifying ssh and skype. In 2009 IEEE symposium on computational intelligence for security and defense applications. 1–8.   
[4] Blake Anderson, Subharthi Paul, and David McGrew. 2018. Deciphering malware’s use of TLS (without decryption). Journal of Computer Virology and Hacking Techniques 14 (2018), 195–211.   
[5] Diogo Barradas, Nuno Santos, Luís Rodrigues, Salvatore Signorello, Fernando MV Ramos, and André Madeira. 2021. FlowLens: Enabling Efficient Flow Classification for ML-based Network Security Applications.. In NDSS.   
[6] Tomasz Bujlow, Valentín Carela-Español, and Pere Barlet-Ros. 2015. Independent comparison of popular DPI tools for traffic classification. Computer Networks 76 (2015), 75–89.   
[7] Zigang Cao, Gang Xiong, Yong Zhao, Zhenzhen Li, and Li Guo. 2014. A survey on encrypted traffic classification. In Applications and Techniques in Information Security. 73–81.   
[8] Fivos Constantinou and Panayiotis Mavrommatis. 2006. Identifying known and unknown peer-to-peer traffic. In Fifth IEEE International Symposium on Network Computing and Applications (NCA’06). 93–102.   
[9] Ekin D Cubuk, Barret Zoph, Dandelion Mane, Vijay Vasudevan, and Quoc V Le. 2019. Autoaugment: Learning augmentation strategies from data. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 113–123.   
[10] Ekin D Cubuk, Barret Zoph, Jonathon Shlens, and Quoc V Le. 2020. Randaugment: Practical automated data augmentation with a reduced search space. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition workshops. 702–703.   
[11] Terrance DeVries and Graham W Taylor. 2017. Improved regularization of convolutional neural networks with cutout. arXiv preprint arXiv:1708.04552 (2017).   
[12] Gerard Draper-Gil, Arash Habibi Lashkari, Mohammad Saiful Islam Mamun, and Ali A Ghorbani. 2016. Characterization of encrypted and vpn traffic using time-related. In Proceedings of the 2nd international conference on information systems security and privacy (ICISSP). 407–414.   
[13] Maurizio Dusi, Alice Este, Francesco Gringoli, and Luca Salgarelli. 2009. Using GMM and SVM-based techniques for the classification of SSH-encrypted traffic. In 2009 IEEE International Conference on Communications. 1–6.   
[14] Jeffrey Erman, Anirban Mahanti, Martin Arlitt, and Carey Williamson. 2007. Identifying and discriminating between web and peer-to-peer traffic in the network core. In Proceedings of the 16th international conference on World Wide Web. 883–892.   
[15] Michael Finsterbusch, Chris Richter, Eduardo Rocha, Jean-Alexander Muller, and Klaus Hanssgen. 2013. A survey of payload-based traffic classification approaches. IEEE Communications Surveys & Tutorials 16, 2 (2013), 1135–1156.   
[16] Chuanpu Fu, Qi Li, Meng Shen, and Ke Xu. 2021. Realtime robust malicious traffic detection via frequency domain analysis. In Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security. 3431–3446.   
[17] Chuanpu Fu, Qi Li, and Ke Xu. 2023. Detecting Unknown Encrypted Malicious Traffic in Real Time via Flow Interaction Graph Analysis. In 30th Annual Network and Distributed System Security Symposium (NDSS).   
[18] Keke Gai, Meikang Qiu, and Hui Zhao. 2017. Privacy-preserving data encryption strategy for big data in mobile cloud computing. IEEE Transactions on Big Data 7, 4 (2017), 678–688.   
[19] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. 2016. Deep residual learning for image recognition. In Proceedings of the IEEE conference on computer vision and pattern recognition. 770–778.   
[20] Dan Hendrycks and Kevin Gimpel. 2016. Gaussian error linear units (gelus). arXiv preprint arXiv:1606.08415 (2016).   
[21] Ram Keralapura, Antonio Nucci, and Chen-Nee Chuah. 2009. Self-learning peerto-peer traffic classifier. In 2009 Proceedings of 18th International Conference on Computer Communications and Networks. 1–8.   
[22] Arash Habibi Lashkari, Gerard Draper Gil, Mohammad Saiful Islam Mamun, and Ali A Ghorbani. 2017. Characterization of tor traffic using time based features. In International Conference on Information Systems Security and Privacy, Vol. 2. 253–262.   
[23] Shuai Li, Huajun Guo, and Nicholas Hopper. 2018. Measuring information leakage in website fingerprinting attacks and defenses. In Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security. 1977–1992.   
[24] Kunda Lin, Xiaolong Xu, and Honghao Gao. 2021. TSCRNN: A novel classification scheme of encrypted traffic based on flow spatiotemporal features for efficient management of IIoT. Computer Networks 190 (2021), 107974.

[25] Xinjie Lin, Gang Xiong, Gaopeng Gou, Zhen Li, Junzheng Shi, and Jing Yu. 2022. Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification. In Proceedings of the ACM Web Conference 2022. 633–642.   
[26] Chang Liu, Longtao He, Gang Xiong, Zigang Cao, and Zhen Li. 2019. Fs-net: A flow sequence network for encrypted traffic classification. In IEEE INFOCOM 2019-IEEE Conference On Computer Communications. 1171–1179.   
[27] Huisheng Liu, Zhenxing Wang, and Yu Wang. 2012. Semi-supervised encrypted traffic classification using composite features set. Journal of Networks 7, 8 (2012), 1195.   
[28] Junming Liu, Yanjie Fu, Jingci Ming, Yong Ren, Leilei Sun, and Hui Xiong. 2017. Effective and real-time in-app activity analysis in encrypted internet traffic streams. In Proceedings of the 23rd ACM SIGKDD international conference on knowledge discovery and data mining. 335–344.   
[29] Mohammad Lotfollahi, Mahdi Jafari Siavoshani, Ramin Shirali Hossein Zade, and Mohammdsadegh Saberian. 2020. Deep packet: A novel approach for encrypted traffic classification using deep learning. Soft Computing 24, 3 (2020), 1999–2012.   
[30] Yaxuan Qi, Lianghong Xu, Baohua Yang, Yibo Xue, and Jun Li. 2009. Packet classification algorithms: From theory to practice. In IEEE INFOCOM 2009. 648– 656.   
[31] Shahbaz Rezaei and Xin Liu. 2019. Deep learning for encrypted traffic classification: An overview. IEEE communications magazine 57, 5 (2019), 76–81.   
[32] Fulvio Risso, Mario Baldi, Olivier Morandi, Andrea Baldini, and Pere Monclus. 2008. Lightweight, payload-based traffic classification: An experimental evaluation. In 2008 IEEE International Conference on Communications. 5869–5875.   
[33] Matthew Roughan, Subhabrata Sen, Oliver Spatscheck, and Nick Duffield. 2004. Class-of-service mapping for QoS: a statistical signature-based approach to IP traffic classification. In Proceedings of the 4th ACM SIGCOMM conference on Internet measurement. 135–148.   
[34] Tal Shapira and Yuval Shavitt. 2021. FlowPic: A generic representation for encrypted traffic classification and applications identification. IEEE Transactions on Network and Service Management 18, 2 (2021), 1218–1232.   
[35] Hongtao Shi, Hongping Li, Dan Zhang, Chaqiu Cheng, and Xuanxuan Cao. 2018. An efficient feature generation approach based on deep learning and feature selection techniques for traffic classification. Computer Networks 132 (2018), 81–98.   
[36] Payap Sirinam, Mohsen Imani, Marc Juarez, and Matthew Wright. 2018. Deep fingerprinting: Undermining website fingerprinting defenses with deep learning. In Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security. 1928–1943.   
[37] Vincent F Taylor, Riccardo Spolaor, Mauro Conti, and Ivan Martinovic. 2017. Robust smartphone app identification via encrypted network traffic analysis. IEEE Transactions on Information Forensics and Security 13, 1 (2017), 63–78.   
[38] Thijs Van Ede, Riccardo Bortolameotti, Andrea Continella, Jingjing Ren, Daniel J Dubois, Martina Lindorfer, David Choffnes, Maarten van Steen, and Andreas Peter. 2020. Flowprint: Semi-supervised mobile-app fingerprinting on encrypted network traffic. In Network and distributed system security symposium (NDSS), Vol. 27.   
[39] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you need. Advances in neural information processing systems 30 (2017).   
[40] William Yang Wang and Diyi Yang. 2015. That’s so annoying!!!: A lexical and frame-semantic embedding based data augmentation approach to automatic categorization of annoying behaviors using# petpeeve tweets. In Proceedings of the 2015 conference on empirical methods in natural language processing. 2557– 2563.   
[41] Hongxin Wei, Renchunzi Xie, Hao Cheng, Lei Feng, Bo An, and Yixuan Li. 2022. Mitigating neural network overconfidence with logit normalization. In International Conference on Machine Learning. 23631–23644.   
[42] Haipeng Yao, Chong Liu, Peiying Zhang, Sheng Wu, Chunxiao Jiang, and Shui Yu. 2019. Identification of encrypted traffic through attention mechanism based long short term memory. IEEE Transactions on Big Data 8, 1 (2019), 241–252.   
[43] Xiang Zhang, Junbo Zhao, and Yann LeCun. 2015. Character-level convolutional networks for text classification. Advances in neural information processing systems 28 (2015).   
[44] Ruijie Zhao, Xianwen Deng, Yanhao Wang, Libo Chen, Ming Liu, Zhi Xue, and Yijun Wang. 2022. Flow sequence-based anonymity network traffic identification with residual graph convolutional networks. In 2022 IEEE/ACM 30th International Symposium on Quality of Service (IWQoS). 1–10.   
[45] Ruijie Zhao, Yiteng Huang, Xianwen Deng, Zhi Xue, Jiabin Li, Zijing Huang, and Yijun Wang. 2021. Flow Transformer: A Novel Anonymity Network Traffic Classifier with Attention Mechanism. In 2021 17th International Conference on Mobility, Sensing and Networking (MSN). 223–230.   
[46] Wenbo Zheng, Chao Gou, Lan Yan, and Shaocong Mo. 2020. Learning to classify: A flow-based relation network for encrypted traffic classification. In Proceedings of The Web Conference 2020. 13–22.

# A THEORETICAL ANALYSIS OF HT SELF-ATTENTION MECHANISM

We provide a theoretical analysis demonstrating how high temperature self-attention mechanism produces extremely small weights for short-term features of irrelevant flows. As stated in Equation $^ { 5 , }$ normal self-attention layer scales dot products $\mathsf { S } _ { i }$ by $\frac { \hat { 1 } } { \sqrt { D } }$ before applying a softmax function (for simplicity, we omit subscript ??):

$$
\mathbf {W} = \text { softmax } (\frac {\mathrm{S}}{\sqrt {D}}) = [ w _ {1}, w _ {2}, \dots , w _ {N} ], \sum_ {j = 1} ^ {N} w _ {j} = 1. \tag {13}
$$

As a comparison, the high temperature self-attention mechanism increases the magnitude of S through the temperature hyperparameter ??. The vector S can be decomposed into two components:

$$
\mathbf {S} = | | \mathbf {S} | | \cdot \hat {\mathbf {S}}, \tag {14}
$$

where $| | \mathbf { S } | | = \sqrt { s _ { 1 } ^ { 2 } + s _ { 2 } ^ { 2 } + \cdot \cdot \cdot + s _ { N } ^ { 2 } }$ is the Euclidean norm, and $\hat { \mathsf { S } } =$ $[ \hat { s } _ { 1 } , \hat { s } _ { 2 } , \cdots , \hat { s } _ { N } ]$ is the unit vector in the same direction as S. In other word, $| | \mathbf { S } | |$ and $\hat { \mathsf { S } }$ represent the magnitude and the direction of S, respectively. Assume that the dot product calculated from the irrelevant flow is relatively small: $\hat { s } _ { k } = m _ { \ j } ^ { \mathrm { } i n ( \hat { s } _ { j } ) }$ , then the weight for the irrelevant flow $w _ { k }$ can be calculated according to the softmax formula:

$$
w _ {k} = \frac {e ^ {| | S | | \hat {s} _ {k}}}{\sum_ {j = 1} ^ {N} e ^ {| | S | | \hat {s} _ {j}}}. \tag {15}
$$

High temperature self-attention mechanism increases the magnitude of ||S|| through the temperature hyper-parameter ?? and the weight can be expressed as:

$$
w _ {k} ^ {\prime} = \frac {e ^ {\frac {| | \mathbb {S} | |}{\tau} \hat {s} _ {k}}}{\sum_ {j = 1} ^ {N} e ^ {\frac {| | \mathbb {S} | |}{\tau} \hat {s} _ {j}}}, \tag {16}
$$

where ?? ≪ 1 is the pre-defined temperature hyper-parameter. Let $t = | | \mathrm { \bf S } | | \cdot \big ( \frac { 1 } { \tau } - 1 \big ) > 0 \mathrm { ; }$ , then we have:

$$
w _ {k} ^ {\prime} = \frac {e ^ {(| | S | | + t) \hat {s} _ {k}}}{\sum_ {j = 1} ^ {N} e ^ {(| | S | | + t) \hat {s} _ {j}}} = \frac {e ^ {| | S | | \hat {s} _ {k}}}{\sum_ {j = 1} ^ {N} e ^ {| | S | | \hat {s} _ {j} + t (\hat {s} _ {j} - \hat {s} _ {k})}}. \tag {17}
$$

For any $j \in [ 1 , 2 , \cdots , N ]$ , we have $\hat { s } _ { j } - \hat { s } _ { k } \ge 0$ . Then:

$$
w _ {k} ^ {\prime} \leq w _ {k}. \tag {18}
$$

In conclusion, increasing the magnitude ||S|| will cause a sharp distribution for weight score W. By producing extremely small weights for short-term features from irrelevant flows, high temperature self-attention mechanism can effectively resist irrelevant packet noise.

# B THEORETICAL ANALYSIS OF RE STRATEGY

We first conduct comparative experiments on the representation enhancement strategy and other fusion techniques, and then provide a theoretical analysis showcasing how the representation enhancement strategy contributes to learning information from a modality riddled with noise. Our focus is on the Packet Size and TTL modalities for the SJTU-AN21 dataset, with the introduction of 50% noise into the Packet Size modality. Table 6 presents experimental results, emphasizing the superior efficacy of the RE method compared to the other fusion techniques. Furthermore, our analysis reveals two crucial findings:

Table 6: Comparative experimental results on the representation enhancement strategy and other fusion techniques. 

<table><tr><td rowspan="2">Fusion Method</td><td colspan="3">Training Loss</td><td colspan="3">Accuracy</td></tr><tr><td>Size</td><td>TTL</td><td>Fusion</td><td>Size</td><td>TTL</td><td>Fusion</td></tr><tr><td>Add</td><td>2.60</td><td>0.32</td><td>0.05</td><td>0.3511</td><td>0.7576</td><td>0.8826</td></tr><tr><td>Concatenation</td><td>2.69</td><td>0.31</td><td>0.05</td><td>0.2148</td><td>0.7209</td><td>0.8394</td></tr><tr><td>RE</td><td>0.67</td><td>0.13</td><td>0.04</td><td>0.6779</td><td>0.7993</td><td>0.8948</td></tr></table>

• The training loss for all three fusion methods is exceptionally low, indicating that the fused predictions closely align with the corresponding label values across the entire training dataset.   
• In the noise-filled Packet Size modality, the Add and Concatenation fusion methods demonstrate subpar performance.

This indicates that the Add and Concatenation fusion methods overly depend on the TTL modality, neglecting the opportunity to glean information from the Packet Size modality. In contrast, the experimental results of the RE method demonstrate its ability to extract valuable information from the noisy Packet Size modality, achieving an accuracy of 67.79%.

We provide a theoretical analysis of the above phenomena to explain why the Add and Concatenation fusion methods neglect to learn information from the noisy Packet Size modality.

# B.1 Preliminaries

Given the fused representation $\mathbf { Z } = \left[ z _ { 1 } , z _ { 2 } , \cdots , z _ { D } \right]$ , where ?? is the representation dimension. We use a fully-connected layer to compute the output logit:

$$
\begin{array}{l} \mathbf {H} = \left[ h _ {1}, h _ {2}, \dots , h _ {K} \right] = \mathbf {Z W} ^ {T} \\ = \left[ \begin{array}{l l l l} z _ {1} & z _ {2} & \dots & z _ {D} \end{array} \right] \times \left[ \begin{array}{c c c c} w _ {1 1} & w _ {1 2} & \dots & w _ {1 D} \\ w _ {2 1} & w _ {2 2} & \dots & w _ {2 D} \\ \vdots & \vdots & \ddots & \vdots \\ w _ {K 1} & w _ {K 2} & \dots & w _ {K D} \end{array} \right] ^ {T}, \tag {19} \\ \end{array}
$$

where $\mathbf { W } \in \mathbb { R } ^ { K \times D }$ is the weight matrix of the fully-connected layer and ?? is the number of classes. According to the above formula, we have:

$$
h _ {i} = \sum_ {j = 1} ^ {D} z _ {j} w _ {i j}. \tag {20}
$$

Then the softmax output can be calculated by:

$$
\begin{array}{l} \mathbf {Q} = \left[ q _ {1}, q _ {2}, \dots , q _ {K} \right] = \text { softmax } (\mathbf {H}) \\ = \operatorname{softmax} \left(\left[ h _ {1}, h _ {2}, \dots , h _ {K} \right]\right). \\ \end{array}
$$

According to the softmax formula, we have:

$$
q _ {i} = \frac {e ^ {h _ {i}}}{\sum_ {j = 1} ^ {K} e ^ {h _ {j}}}. \tag {22}
$$

The softmax gradient is well known as follows:

$$
\frac {\partial q _ {j}}{\partial h _ {i}} = \left\{ \begin{array}{c} q _ {j} (1 - q _ {j}), i = j \\ - q _ {i} q _ {j}, i \neq j \end{array} \right. \tag {23}
$$

# B.2 Proof

We first solve for the gradient of L with respect to $h _ { i }$ through the chain rule:

$$
\begin{array}{l} \frac {\partial \mathcal {L}}{\partial h _ {i}} = \sum_ {j = 1} ^ {K} \frac {\partial \mathcal {L}}{\partial q _ {j}} \cdot \frac {\partial q _ {j}}{\partial h _ {i}} = - \frac {1}{q _ {k}} \cdot \frac {\partial q _ {k}}{\partial h _ {i}} = (24) \\ = \left\{ \begin{array}{c c} - \frac {1}{q _ {k}} \cdot q _ {k} (1 - q _ {k}) = q _ {k} - 1, & i = k \\ - \frac {1}{q _ {k}} \cdot - q _ {i} q _ {k} = q _ {i}, & i \neq k \end{array} \right. (25) \\ \end{array}
$$

Then we calculate the gradient of L with respect to representation ???? :

$$
\frac {\partial \mathcal {L}}{\partial z _ {i}} = \sum_ {j = 1} ^ {K} \frac {\partial \mathcal {L}}{\partial h _ {j}} \cdot \frac {\partial h _ {j}}{\partial z _ {i}} = \frac {\partial \mathcal {L}}{\partial h _ {k}} \cdot \frac {\partial h _ {k}}{\partial z _ {i}} + \sum_ {j = 1, j \neq k} ^ {K} \frac {\partial \mathcal {L}}{\partial h _ {j}} \cdot \frac {\partial h _ {j}}{\partial z _ {i}}
$$

$$
= (q _ {k} - 1) \cdot w _ {k i} + \sum_ {j = 1, j \neq k} ^ {K} q _ {j} \cdot w _ {j i} = \sum_ {j = 1} ^ {K} q _ {j} w _ {j i} - w _ {k i}.
$$

As mentioned in the above analysis, the training loss of the three fusion methods is very low, which means that the fusion predictions of the model are close to the ground-truth label, that is:

$$
q _ {i} \rightarrow \left\{\begin{array}{l}1, i = k\\0, i \neq k\end{array}\right. \tag {26}
$$

Finally, we have:

$$
\frac {\partial \mathcal {L}}{\partial z _ {i}} \rightarrow 0. \tag {27}
$$

The preceding analysis indicates that when the model acquires sufficient knowledge from a specific modality to generate highconfidence predictions, it tends to disregard learning from other modalities, particularly those with noise. Conversely, the representation enhancement strategy compels the model to glean as much knowledge as feasible from each modality by introducing random adjustments to the weights of individual modalities throughout the training phase. This ensures that the model can effectively learn valuable information even in the presence of noisy modalities.

# C RESULTS ON OTHER ENCRYPTED TRAFFIC DATASETS

We assess the performance of the AN-Net using two additional universal encrypted traffic datasets, namely USTC-TFC and Cross-Platform. The comparison is made against other state-of-the-art methods, and the corresponding experimental results are presented in Table 7. To align with the central theme of the paper, we treat continuous packets as a flow. The superior performance of the AN-Net can be attributed to its robust short-term representations and the incorporation of multi-modal information.

Table 7: Comparison results on two additional universal encrypted traffic datasets. 

<table><tr><td rowspan="2">Method</td><td colspan="2">USTC-TFC</td><td colspan="2">Cross-Platform</td></tr><tr><td>AC</td><td>F1</td><td>AC</td><td>F1</td></tr><tr><td>AppScanner [37]</td><td>0.7907</td><td>0.7893</td><td>0.5554</td><td>0.5469</td></tr><tr><td>Decision Tree [12]</td><td>0.7116</td><td>0.7002</td><td>0.8048</td><td>0.8032</td></tr><tr><td>Whisper [16]</td><td>0.3920</td><td>0.4207</td><td>0.6440</td><td>0.6534</td></tr><tr><td>Flowlens [5]</td><td>0.7582</td><td>0.7473</td><td>0.4600</td><td>0.4488</td></tr><tr><td>FS-Net [26]</td><td>0.9020</td><td>0.8971</td><td>0.8316</td><td>0.8310</td></tr><tr><td>AttnLSTM [42]</td><td>0.9709</td><td>0.9705</td><td>0.9933</td><td>0.9933</td></tr><tr><td>ET-Bert [25]</td><td>0.9829</td><td>0.9832</td><td>0.9937</td><td>0.9937</td></tr><tr><td>AN-Net (ours)</td><td>0.9980</td><td>0.9980</td><td>0.9967</td><td>0.9967</td></tr></table>

# D COMPUTATIONAL COMPLEXITY

We provide details on AN-Net’s implementation and computational complexity on the SJTU-AN21 dataset. A comparison with other deep learning-based methods is shown in Table 8. Experimental results highlight AN-Net as a real-time, lightweight anonymous traffic classification model:

• Real-Time Performance: Inference time for AN-Net is 39.41× $1 0 ^ { - 6 }$ s/pkt, enabling the classification of $2 . 5 \times 1 0 ^ { 3 }$ packets within one second.   
• Lightweight Design: AN-Net exhibits significantly lower memory usage, parameter count, and FLOPs compared to FS-Net [26] and ET-Bert [25], indicating its lightweight nature.

AttnLSTM [42] is another lightweight payload-based traffic classification model that performs well on simple datasets $( i . e . ,$ crossplatform). However, its performance is significantly inferior to AN-Net on the anonymous traffic dataset SJTU-AN21 (see Table 1) and in the face of injected noise packet attacks (see Figure 4). From a practical perspective, we still recommend using AN-Net due to its robustness and real-time capabilities (compared to FS-Net [26] and ET-Bert [25]).

Table 8: Computational complexity comparison with other deep learning-based methods on the SJTU-AN21 dataset. 

<table><tr><td>Method</td><td>Training Time (min)</td><td>Inference Time ( $10^{-6}$ s/packet)</td><td>Memory (MiB)</td><td>Params ( $10^{6}$ )</td><td>FLOPs ( $10^{6}$ )</td></tr><tr><td>FS-Net [26]</td><td>15.83</td><td>13.41</td><td>2813</td><td>5.14</td><td>256.01</td></tr><tr><td>AttnLSTM [42]</td><td>1.93</td><td>4.29</td><td>1385</td><td>0.25</td><td>0.33</td></tr><tr><td>ET-Bert [25]</td><td>49.51</td><td>169.34</td><td>17379</td><td>132.13</td><td>48318.97</td></tr><tr><td>AN-Net (ours)</td><td>18.41</td><td>39.41</td><td>1477</td><td>2.40</td><td>23.94</td></tr></table>

# E RECOGNITION OF SHORT FLOWS

To explore the effectiveness of AN-Net in classifying short flows, we truncated all flows to consecutive packets with a length not exceeding 10. We compared AN-Net with other methods on the SJTU-AN21 dataset, and the experimental results are presented in Table 9. The results indicate that only ET-Bert [25] and AN-Net can effectively classify short flows. ET-Bert achieves stronger robustness through prolonged pre-training on a large amount of unlabeled data. In contrast, AN-Net enhances the classification performance of short flows effectively by aggregating information from multiple modalities.

Table 9: Experimental results on short flows. 

<table><tr><td>Method</td><td>AC</td><td>F1</td></tr><tr><td>AppScanner [37]</td><td>0.5286</td><td>0.4956 (20.08%↓)</td></tr><tr><td>Decision Tree [12]</td><td>0.4074</td><td>0.3966 (16.55%↓)</td></tr><tr><td>Whisper [16]</td><td>0.2590</td><td>0.3141 (19.25%↓)</td></tr><tr><td>Flowlens [5]</td><td>0.5125</td><td>0.4996 (21.32%↓)</td></tr><tr><td>FS-Net [26]</td><td>0.5870</td><td>0.5706 (22.43%↓)</td></tr><tr><td>AttnLSTM [42]</td><td>0.6965</td><td>0.6627 (14.03%↓)</td></tr><tr><td>ET-Bert [25]</td><td>0.8693</td><td>0.8544 (2.71%↓)</td></tr><tr><td>AN-Net (ours)</td><td>0.8987</td><td>0.9002 (4.37%↓)</td></tr></table>

# F VISUALIZATION OF HT SELF-ATTENTION

We visualize the weight score matrix to exhibit how high temperature self-attention mechanism helps resist irrelevant packets noise. Specifically, we first construct a noisy dataset containing 50% irrelevant packets by injecting irrelevant packets, and then train AN-Net with this noisy dataset. The weight score matrices of two special text examples are shown in Figure 7. Each flow is divided into 10 short-term packet sequences. In Figure 7(a), the left half is the target packet sequences, and the right half is the irrelevant packet sequences, which is exactly the opposite of Figure 7(b).

![](images/8da6e3ce7339cf3921fe293b4b917d50e3b422e2ae086158771c045d1b6fa051.jpg)

<details>
<summary>heatmap</summary>

| Short-term Feature | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 | F10 |
|---|---|---|---|---|---|---|---|---|---|---|
| F1 | 0.25 | 0.25 | 0.13 | 0.25 | 0.1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| F2 | 0.25 | 0.25 | 0.13 | 0.25 | 0.1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| F3 | 0.24 | 0.24 | 0.14 | 0.24 | 0.1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| F4 | 0.25 | 0.25 | 0.13 | 0.25 | 0.1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| F5 | 0.24 | 0.24 | 0.14 | 0.24 | 0.1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| F6 | 0.09 | 0.09 | 0.23 | 0.09 | 0.23 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 |
| F7 | 0.09 | 0.09 | 0.23 | 0.09 | 0.23 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 |
| F8 | 0.09 | 0.09 | 0.23 | 0.09 | 0.23 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 |
| F9 | 0.09 | 0.09 | 0.23 | 0.09 | 0.23 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 |
| F10 | 0.09 | 0.09 | 0.23 | 0.09 | 0.23 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 |
(a)
</details>

![](images/a248bbe0336b66d354b151f4ac0dec1b54552dec594346967eeb8edf3caa781e.jpg)

<details>
<summary>heatmap</summary>

| Short-term Feature | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 | F10 |
|---|---|---|---|---|---|---|---|---|---|---|
| F1 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.09 | 0.28 | 0.19 | 0.09 | 0.09 |
| F2 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.09 | 0.28 | 0.19 | 0.09 | 0.09 |
| F3 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.09 | 0.28 | 0.19 | 0.09 | 0.09 |
| F4 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.09 | 0.28 | 0.19 | 0.09 | 0.09 |
| F5 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.09 | 0.28 | 0.19 | 0.09 | 0.09 |
| F6 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.25 | 0.11 | 0.08 | 0.25 | 0.25 |
| F7 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.24 | 0.25 | 0.02 | 0.24 | 0.24 |
| F8 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.25 | 0.25 | 0.01 | 0.25 | 0.25 |
| F9 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.25 | 0.11 | 0.08 | 0.25 | 0.25 |
| F10 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.25 | 0.11 | 0.08 | 0.25 | 0.25 |
(b)
</details>

Figure 7: The visualization of the weight score matrices in the high temperature self-attention mechanism.

It can be concluded that the high temperature self-attention mechanism generates a sharp distribution for weight score matrix and all short-term features (including noisy short-term features) pay little attention to noisy short-term features from irrelevant packets. The high temperature self-attention mechanism increases the magnitude of dot products by the temperature hyper-parameter ??. After employing a high temperature, the softmax function can produce extremely small weights for noisy short-term features from irrelevant packets (0.00 or 0.05 in Figure 7). By combining shortterm features with high temperature self-attention mechanism, AN-Net is effective to resist irrelevant packet noise.

# G ADDITIONAL ROBUSTNESS ANALYSIS

In the Robustness Analysis of Section 4.3, we showcased the superior robustness of AN-Net compared to other methods by injecting irrelevant packets. Next, we provide additional insights into the robustness of AN-Net to training data size. Some deep learning-based methods that autonomously learn from the raw flow attribute sequences (FS-Net [26]) or raw payload (AttnLSTM [42] and ET-Bert [25]) necessitate a substantial amount of annotated data. Through comparative experiments, we controlled the size of the training data on the SJTU-AN21 dataset, and the outcomes are depicted in Table 10. The results indicate that AN-Net performs effectively with a limited dataset, attributed to the utilization of statistical features and the integration of multi-modal information.

Table 10: Robustness to Training Data Size. 

<table><tr><td>Data Size</td><td>100%</td><td>50%</td><td>30%</td><td>10%</td></tr><tr><td>FS-Net [26]</td><td>0.7949</td><td>0.6074</td><td>0.5916</td><td>0.6012</td></tr><tr><td>AttnLSTM [42]</td><td>0.8030</td><td>0.6137</td><td>0.6040</td><td>0.5682</td></tr><tr><td>ET-Bert [25]</td><td>0.8815</td><td>0.8305</td><td>0.7863</td><td>0.5663</td></tr><tr><td>AN-Net (ours)</td><td>0.9439</td><td>0.9207</td><td>0.9153</td><td>0.8930</td></tr></table>

# H INSTRUCTIONS ON MIXING ORIGINALTRAFFIC WITH NOISE TRAFFIC

We introduce irrelevant packet noise by injecting TLS traffic from the CICIOT dataset, as per the Whisper approach. Specifically, for a predetermined input packet sequence ?? and noise ratio ??, we randomly inserted ?? × ?? consecutive TLS noise packets, presented in the form of multiple consecutive packets, into regular traffic containing $L \times ( 1 - \eta )$ consecutive packets.

# I MODAL SELECTION

As mentioned above, before fusing representations from different modalities, we resort to information leakage to remove useless modalities. We compute the mutual information between statistical features of a certain modalities and the ground truth labels to measure the importance of this modality. The calculation results and selection strategies are shown in Table 11. Modalities with lower information leakage are removed to reduce model complexity. Specifically, we remove the IPFlag modality and TTL modality for SJTU-AN21 and ISCX-Tor datasets, respectively. For ISCX-VPN dataset, we drop the IPFlag and TCPFlag modalities.

Table 11: Mutual information and selection strategies of each modality on three datasets. 

<table><tr><td>Dataset</td><td>Metric</td><td>Packet Size</td><td>IAT</td><td>TTL</td><td>IPFlag</td><td>TCPFlag</td></tr><tr><td rowspan="2">SJTU-AN21</td><td>MI</td><td>0.81</td><td>0.81</td><td>1.50</td><td>0.01</td><td>0.99</td></tr><tr><td>Selection</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>√</td></tr><tr><td rowspan="2">ISCX-Tor</td><td>MI</td><td>1.14</td><td>0.82</td><td>0.00</td><td>0.95</td><td>0.84</td></tr><tr><td>Selection</td><td>√</td><td>√</td><td>✗</td><td>√</td><td>√</td></tr><tr><td rowspan="2">ISCX-VPN</td><td>MI</td><td>0.68</td><td>0.75</td><td>1.34</td><td>0.23</td><td>0.42</td></tr><tr><td>Selection</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>✗</td></tr></table>
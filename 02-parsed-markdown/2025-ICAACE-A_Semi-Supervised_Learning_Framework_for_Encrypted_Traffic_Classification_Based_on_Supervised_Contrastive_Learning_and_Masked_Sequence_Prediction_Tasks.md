# A Semi-Supervised Learning Framework for Encrypted Traffic Classification Based on Supervised Contrastive Learning and Masked Sequence Prediction Tasks

Zhongyu Guo

Key Laboratory of Cyberspace Security, Ministry of Education

Zhengzhou, China

godplutohades@gmail.com

Wei Wu

Key Laboratory of Cyberspace Security, Ministry of Education

Zhengzhou, China

goodwuwei18@163.com

Zhaoyun Liu

Key Laboratory of Cyberspace Security, Ministry of Education

Zhengzhou, China

winniejony@gmail.com

Abstract-With the widespread adoption of encryption technologies, the proportion of encrypted traffic in network traffic has significantly increased, making encrypted traffic classification a key technology for enhancing network security and optimizing network performance. Although existing research on encrypted traffic classification has made certain advancements, two major challenges remain: (1) Current classification methods generally lack effective utilization of unlabeled data, limiting models to specific task scenarios and reducing their generalization ability; (2) During pre-training, existing methods often focus solely on unlabeled data, failing to fully leverage label information, which restricts further optimization of the feature space. To address these issues, this paper proposes CoMask, a semi-supervised learning framework for encrypted traffic classification that integrates supervised contrastive learning and masked sequence prediction tasks. The framework uses multi-granularity feature sequences as input and employs a cross-training strategy to collaboratively utilize both labeled and unlabeled data. Specifically, the framework utilizes unlabeled data to perform the masked sequence prediction task to enhance the generalization ability of feature representations, while supervised contrastive learning tasks are conducted using labeled data to optimize the feature space. Experimental results show that CoMask outperforms existing state-of-the-art methods on multiple public datasets, with an average F1 score improvement of 3.3%, demonstrating its effectiveness in handling encrypted traffic classification tasks in both known and unknown category scenarios.

Keywords-component; Encrypted Traffic Classification; Supervised Contrastive Learning; Masked Sequence Prediction; Semi-supervised Learning

Bin Lu\*

Key Laboratory of Cyberspace Security, Ministry of Education

Zhengzhou, China

\* stoneclever@126.com

Man Guo

Key Laboratory of Cyberspace Security, Ministry of Education

Zhengzhou, China

DreamCamellia1118@163.com

Xiangnan Lin

Key Laboratory of Cyberspace Security, Ministry of Education

Zhengzhou, China

wh\_lxnzzz@163.com

# I. INTRODUCTION

Currently, encryption technologies are widely applied in various online services such as e-commerce platforms, social media, streaming services, remote work tools, and online payment systems. While this trend protects user privacy and data security, it also provides covert communication channels for malicious organizations and botnets. According to the Zscaler ThreatLabz 2024 Encryption Attack Report, more than 87% of network threats were transmitted through encrypted channels between October 2023 and September 2024, marking a 10% increase from the previous year [1]. This phenomenon indicates that attackers are increasingly exploiting the concealment of encrypted traffic to bypass traditional detection methods, making encrypted traffic classification (ETC) a critical technology in the field of cybersecurity. Accurate classification of encrypted traffic not only helps in identifying malicious traffic but also has broad applications in other traffic analysis tasks, playing a crucial role in enhancing network security, optimizing traffic management, and ensuring service quality.

Researchers and cybersecurity experts have proposed various methods for encrypted traffic classification, which can generally be categorized into three types: fingerprint-based methods, statistical feature-based methods, and deep learningbased methods. However, existing methods face several challenges in practical applications.

Fingerprint-based methods [2][3][4][5] typically achieve high classification accuracy and can quickly detect known traffic behavior patterns. However, these methods rely on predefined rule sets or signatures, making them less adaptable to dynamic changes in traffic, especially in scenarios where encryption algorithms evolve and network environments undergo frequent changes. As a result, their classification performance may significantly degrade in such contexts. Statistical feature-based methods [6][7][8], on the other hand, classify traffic by analyzing various characteristics such as spatiotemporal features, byte-level statistical features, certificate features, and behavioral features. These methods exhibit better generalization, allowing them to handle the dynamic changes in encrypted traffic and maintain robustness as encryption algorithms continue to evolve. However, the extraction of features typically depends on a considerable amount of prior knowledge and expert experience, which undoubtedly increases the cost of development and maintenance.

In recent years, deep learning-based methods have made significant progress in the field of encrypted traffic classification. These methods [9][10][11] automatically extract complex features through deep learning, significantly enhancing classification performance. However, many deep learning approaches rely on large-scale labeled data, which is both costly and time-consuming to obtain. When faced with unknown traffic data, the generalization ability of the models is limited, requiring the relabeling and retraining of new data, which increases the time and costs in practical applications. In real-world scenarios, unlabeled traffic data far outnumbers labeled data, making the pretraining-finetuning strategy an effective solution. This approach pretrains on a large amount of unlabeled data and finetunes with a small amount of labeled data, partially alleviating the issue of labeled data scarcity. However, existing pretraining methods mainly focus on self-supervised tasks that capture local patterns and payload contexts of individual packets or flows, aiming to learn a general feature representation space for traffic. While this strategy helps capture general traffic characteristics and enhances generalization ability, it fails to fully utilize the label information of known category traffic, resulting in insufficient optimization of global feature representations and limiting further improvement of the feature space's expressive power.

This paper proposes CoMask, a semi-supervised learning framework for encrypted traffic classification that integrates supervised contrastive learning and masked sequence prediction (MSQ) tasks, aiming to address the shortcomings of existing methods in terms of generalization ability and the utilization of labeled data. The CoMask framework consists of two stages: the semi-supervised training stage and the fine-tuning stage. In the first stage, raw bytes of the payload and packet length sequences from traffic data are extracted and concatenated to form the model input. The concatenated multi-granularity sequence features are then learned using a Transformer encoder. During training, the data is divided into labeled and unlabeled portions, with an alternating training strategy employed. Initially, largescale unlabeled data is used for MSQ task training, and as the task converges, limited labeled data is utilized for supervised contrastive learning, aiming to achieve intra-class cohesion and inter-class separation to enhance the feature space's representation ability. This process is iterated to obtain a labeloptimized, multi-granularity traffic feature representation space. In the second stage, compared to purely unsupervised learning methods, the CoMask framework demonstrates superior performance in labeled data classification tasks. Additionally, through fine-tuning on small sample data, CoMask quickly adapts to unseen datasets and achieves optimal classification performance on certain datasets, showcasing its strong generalization ability and effective feature space optimization capacity. The main contributions of this paper are as follows:

We propose a semi-supervised learning framework for encrypted traffic classification, CoMask. To the best of our knowledge, this is the first application of combining supervised contrastive learning with masked sequence prediction (MSQ) tasks for encrypted traffic classification. This framework effectively leverages limited labeled data resources to optimize the traffic feature representation space and enhance classification performance.   
By adopting an alternating training strategy, we address the common challenge in joint training that requires maintaining consistent sample sizes between labeled and unlabeled data. This constraint often hinders the full utilization of unlabeled data and limits the model’s generalization ability. CoMask effectively overcomes this challenge, maximizing the potential of unlabeled data even under limited computational resources.   
Experimental results demonstrate that CoMask achieves new state-of-the-art (SOTA) performance on six encrypted traffic classification tasks. Compared to existing methods, the average F1 score improves by 3.3%, proving its superiority in optimizing the traffic feature space and its strong generalization ability in practical applications.

The structure of this paper is as follows: Section 2 reviews and summarizes existing encrypted traffic classification methods and their limitations. Section 3 details the architecture of the CoMask semi-supervised framework, including the training and fine-tuning stages that combine contrastive learning and MSQ tasks. Section 4 describes the experimental setup and presents results for multiple traffic classification tasks. Finally, Section 5 concludes the paper.

# II. RELATED WORK

# A. Encrypted Traffic Classification Methods

Fingerprint-based Encrypted Traffic Classification: These techniques identify traffic by analyzing the available information in the payload of packets at the application layer, typically relying on the matching of specific character patterns, also known as fingerprints. Hua et al. [12] proposed a variable step-length multi-pattern matching algorithm (VS-DFA) for high-performance deep packet inspection systems. This algorithm draws inspiration from the Winnowing algorithm, where the input data stream and patterns are divided into variable-sized blocks, and a Deterministic Finite Automaton (DFA) is constructed for matching across these blocks. Liu et al. [13] introduced a multi-attribute Markov probability fingerprintbased method (MaMPF) for encrypted traffic classification. This method combines message type sequences and length block sequences, using a power-law distribution to segment packet length sequences, constructing a Markov model to generate multi-attribute probability fingerprints for classification.

Statistical Feature-based Encrypted Traffic Classification: Statistical feature-based methods primarily rely on extracting features from packets or data flows to perform traffic classification. Lan et al. [14] proposed a novel self-attention method, DarknetSec, for darknet traffic classification and application identification. This method captures local spatiotemporal features from the payload content of packets and extracts bypass features from statistical characteristics, integrating a self-attention mechanism into the feature extraction network for classification. Xu et al. [15] proposed the encrypted traffic classification method ETC-PS, which constructs traffic paths and extracts multi-scale path signature features. By combining path transformation techniques, the method enhances feature expression and employs traditional machine learning classifiers for classification. Fu et al. [16] introduced ST-Graph, an encrypted malicious traffic detection system based on graph representation learning. This method constructs a heterogeneous host-server graph, incorporating spatial and temporal features, and uses an improved random walk algorithm to generate edge embedding vectors. Host behavior representations are then generated by propagating the edge embedding information, with a random forest classifier employed for malicious host detection.

Deep Learning-based Encrypted Traffic Classification: With the continuous advancement of artificial intelligence, supervised deep learning methods have become one of the dominant techniques for encrypted traffic classification. Sirinam et al. [17] proposed a deep learning-based website fingerprinting attack method, Deep Fingerprinting. This approach uses Convolutional Neural Networks (CNNs) to automatically extract traffic features, eliminating the tedious process of manual feature design in traditional methods, and achieves an accuracy rate of 98.3% on unprotected Tor traffic. Horowicz et al. [18] introduced a mini-FlowPic-enhanced few-shot traffic classification method. By transforming traffic data into images and integrating image enhancement and contrastive representation learning techniques for network behavior, this method addresses the issue of scarce labeled data and improves classification performance. Lotfollahi et al. [19] proposed a deep learning-based method for encrypted traffic classification, Deep Packet, which combines Stacked Autoencoders (SAE) and CNNs. This method automatically extracts traffic features and classifies encrypted traffic while distinguishing between VPN and non-VPN traffic. Zhang et al. [20] introduced a fine-grained encrypted traffic classification method, TFE-GNN, based on Graph Neural Networks (GNNs). To address the issue of traditional methods treating packet headers and payloads equally, without exploring the potential correlations between bytes, the authors designed a dual-embedding layer traffic graph encoder based on GNN, integrating a cross-gate feature fusion mechanism for encrypted traffic classification.

# B. Application of Contrastive Learning in Encrypted Traffic Classification

In recent years, contrastive learning has emerged as an effective method for optimizing feature representations and has been widely applied in fields such as image recognition and natural language processing. By constructing positive and negative sample pairs and maximizing the similarity between positive samples while minimizing the similarity between negative samples, contrastive learning facilitates the learning of more robust feature representations. As a result, an increasing number of studies have begun to explore the application of contrastive learning in encrypted traffic classification.

Sun et al. [21] proposed CoMDet, a contrastive multimodal pretraining-based method for encrypted malicious traffic detection. CoMDet leverages three independent Transformer encoders to learn multimodal feature representations from unlabeled data, enhancing feature representations by maximizing the mutual information between modalities. Ma et al. [22] introduced a balanced supervised contrastive learning method for encrypted network traffic classification, known as BSCL. This approach converts raw network traffic data into grayscale images and incorporates class mean and class augmentation strategies within the contrastive learning framework to optimize the effectiveness of supervised contrastive learning. Cai et al. [23] proposed an incremental encrypted traffic classification method based on contrastive prototypical networks (CPN). This method selects representative samples and filters ambiguous traffic using a prototype-guided smooth replay module, while mitigating the class imbalance problem and reducing catastrophic forgetting through a contrastive distillation module. Zhang et al. [24] introduced CLE-TFE, a supervised contrastive learning-based framework for encrypted traffic classification. CLE-TFE enhances both packet-level and flow-level feature representations using supervised contrastive learning, and captures fine-grained semantically invariant features between bytes through graph data augmentation techniques. Finamore et al. [25] investigated the application of contrastive learning and data augmentation in traffic classification, proposing a method based on Flowpic input representations, called Replication. This approach performs selfsupervised pretraining using contrastive learning and utilizes data augmentation techniques to generate synthetic samples, enabling high-accuracy classification even with a limited amount of labeled data.

# C. Analysis of Limitations

Table 1 summarizes the differences and limitations of existing encrypted traffic classification methods in terms of data usage, training approaches, and task design. As shown in the table, most existing methods rely heavily on supervised learning. While these methods have achieved relatively good classification results in specific tasks, they are heavily dependent on large amounts of labeled data, which poses a significant challenge in practical network environments where collecting and labeling encrypted traffic is an extremely demanding task. Unsupervised and semi-supervised methods typically train only on unlabeled data, with limited consideration given to the integration of labeled and unlabeled data. For instance, methods such as CoMDet and CPN adopt an unsupervised pretraining followed by supervised fine-tuning approach. While this partially alleviates the problem of insufficient labeled data, their pretraining tasks are primarily based on unsupervised contrastive learning. This approach not

TABLE I. COMPARISON OF ENCRYPTED TRAFFIC CLASSIFICATION METHODS 

<table><tr><td>Method</td><td>Input Data Type</td><td>Contrastive learning</td><td>MLM Task</td><td>Training Method</td></tr><tr><td>VS-DFA[12]</td><td>Labeled</td><td>×</td><td>×</td><td>Supervised</td></tr><tr><td>MaMPF[13]</td><td>Labeled</td><td>×</td><td>×</td><td>Supervised</td></tr><tr><td>DarknetSec[14]</td><td>Labeled</td><td>×</td><td>×</td><td>Supervised</td></tr><tr><td>ETC-PS[15]</td><td>Labeled</td><td>×</td><td>×</td><td>Supervised</td></tr><tr><td>ST-Graph[16]</td><td>Labeled</td><td>×</td><td>×</td><td>Supervised</td></tr><tr><td>DF[17]</td><td>Labeled</td><td>×</td><td>×</td><td>Supervised</td></tr><tr><td>Mini-Flowpic[18]</td><td>Unlabeled</td><td>×</td><td>×</td><td>Unsupervised</td></tr><tr><td>DP[19]</td><td>Labeled</td><td>×</td><td>×</td><td>Supervised</td></tr><tr><td>TFE-GNN[20]</td><td>Labeled</td><td>×</td><td>×</td><td>Semi-supervised</td></tr><tr><td>CoMDet[21]</td><td>Unlabeled</td><td>√</td><td>×</td><td>Semi-supervised</td></tr><tr><td>BSCL[22]</td><td>Labeled</td><td>√</td><td>×</td><td>Supervised</td></tr><tr><td>CPN[23]</td><td>Unlabeled</td><td>√</td><td>×</td><td>Semi-supervised</td></tr><tr><td>CLE-TFE[24]</td><td>Labeled</td><td>√</td><td>×</td><td>Supervised</td></tr><tr><td>Replication[25]</td><td>Unlabeled</td><td>√</td><td>×</td><td>Unsupervised</td></tr><tr><td>Our work</td><td>Labeled and unlabeled</td><td>√</td><td>√</td><td>Semi-supervised</td></tr></table>

only fails to fully exploit valuable labeled data resources but also often relies on data augmentation or unsupervised clustering techniques to construct positive and negative sample pairs. The underlying assumption of such techniques is that traffic samples from the same class exhibit similar feature representations. However, in complex network environments, encrypted traffic data from the same class does not always exhibit consistent features. In contrast, the semi-supervised framework proposed in this paper, CoMask, effectively improves classifier performance by combining both labeled and unlabeled data and employing a cross-training approach that integrates supervised contrastive learning and Masked Sequence Prediction (MSQ) tasks.

# III. METHODOLOGY

This chapter presents a semi-supervised training framework, CoMask, for encrypted traffic classification, which combines supervised contrastive learning and masked prediction tasks. Section 3.1 will introduce the overall architecture of the model. Section 3.2 will provide a detailed explanation of the feature sequence extractor and the method for constructing the input data. Section 3.3 will describe the design of the masked prediction task. Section 3.4 will discuss the implementation of the supervised contrastive learning task, while Section 3.5 will focus on the fine-tuning process of the classification head.

# A. Framework Overview

Traditional encrypted traffic classifiers typically focus on learning a single task and often lack generalization ability for unknown traffic. In contrast, pre-training methods predominantly focus on unsupervised tasks and fail to fully leverage the information in labeled data, thereby underutilizing available labeled data resources. Fig. 1 illustrates the training process of CoMask, which consists of three main stages: Traffic2Token, semi-supervised training, and classification head fine-tuning. Each stage is designed with distinct tasks to collaboratively optimize both feature representation and classification performance.

Traffic2Token Stage: In this stage, the raw network traffic data is first processed by the feature sequence extractor, converting the traffic into feature sequences suitable for input to CoMask. This process involves representation learning at different levels and granularities of the traffic data, ensuring that semantic features of the traffic are captured from multiple dimensions.

Semi-Supervised Training Stage: Semi-supervised training is the core phase of CoMask and includes both the masked sequence prediction task and the supervised contrastive learning task. For unlabeled data (which, for the time being, also includes the labeled data treated as unlabeled), the model performs self-supervised learning through the masked prediction task, learning local feature patterns and contextual information from the traffic data. For labeled data, the model employs supervised contrastive learning to achieve intra-class clustering and inter-class separation in the feature space. By combining labeled and unlabeled data in cross-training, CoMask can effectively leverage existing encrypted traffic data, optimizing the feature space representation and improving generalization capability.

Classification Head Fine-Tuning Stage: After completing the semi-supervised training, the model enters the fine-tuning phase. The goal of this stage is to refine the classification head according to the specific task. Using the feature representations obtained from the semi-supervised training phase, the model undergoes additional training of the classification head, ensuring that the model delivers optimal performance across various encrypted traffic classification tasks. This process enables the model to classify specific traffic types more effectively according to task requirements, enhancing both accuracy and robustness.

![](images/c6f5e2625894e60973a0bfe15f474df39318be7c5b196dd0788305f259ed70ac.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph_CoMask["CoMask"]
        A["Feature Sequence Extractor"] --> B["Multi-Granularity Sequence"]
        B --> C["Packet raw bytes"]
        B --> D["Packet Length"]
        C --> E["Feature Extraction"]
        D --> E
        E --> F["Flow Segmentation"]
        F --> G["PCAP"]
    end

    subgraph_Semi-Supervised_Training["Seismic Training"]
        H["Input Data Construction"] --> I["Raw Bytes Token Sequence b634 01bb ... ab17 6c19"]
        I --> J["Packet Length Token Sequence +66 -66 ... +239 -60"]
        J --> K["[cls"] + RB + [seq] + PL]
        K --> L["Labeled"]
        L --> M["Unlabeled"]
        M --> N["Transformer Encoder"]
        N --> O["Word embedding"]
        N --> P["Position Encoding"]
        N --> Q["Embedding"]
        O --> R["Random Masking"]
        P --> R
        Q --> R
        R --> S["X: Different labeled Y⁻, Same labeled Y⁺"]
        S --> T["Task-specific fine-tuning model"]
    end

    subgraph_Fine-tuning_classificationHead["Fine-tuning classification head"]
        U["Multi-task"] --> V["Encoder"]
        V --> W["Linear2"]
        W --> X["Linear1"]
        X --> Y["Softmax"]
        Y --> Z["Task-specific fine-tuning model"]
    end

    style CoMask fill:#f9f9f9,stroke:#333
    style Semi-Supervised Training fill:#e6f7ff,stroke:#333
```
</details>

Figure 1. CoMask Framework

# B. Traffic2Token

Traffic2Token is the first stage of the CoMask framework, which is divided into two primary components: feature sequence extraction and input data construction. In the feature sequence extraction phase, the raw traffic data is first subjected to bidirectional flow segmentation and feature extraction, transforming the traffic information into two distinct token representations—raw byte token sequences and packet length token sequences. In the input data construction phase, these feature sequences are further processed to form a data format suitable for the model’s input.

# 1) Feature Sequence Extraction

The feature sequence extraction process begins with bidirectional flow segmentation of the raw network traffic data based on a five-tuple (i.e., source IP, destination IP, source port, destination port, and protocol type). Afterward, each segmented flow is treated as an independent sample for multi-granularity feature extraction, and corresponding raw byte token sequences and packet length token sequences are constructed.

Raw Byte Token Sequences: Starting from the 39th byte of each packet, 128 consecutive bytes are extracted as the raw byte sequence of the packet. This selection helps avoid interference from IP addresses and port numbers, and eliminates Ethernet frame and IP header information, which are susceptible to network topology and environmental changes. In constructing

the raw byte token sequence, every two consecutive bytes in the traffic are treated as a single token. For example, four hexadecimal numbers such as {1f, 29, fd, fb} are transformed into a single token sequence {1f29, fdfb}. These byte values are then mapped to a vector space  ranging from 0 to 65535. The formal representation of the raw byte token sequence is as follows:

$$
\text { Raw   bytes } = \left\{b _ {1},..., b _ {1 2 8} \right\}, b _ {i} \in \mathbb {D} \tag {1}
$$

where $b _ { i }$ represents the token corresponding to every two original bytes in the traffic flow.

Packet Length Token Sequences: For each data flow, only the first 32 packets are used to record the packet length. The direction of the data flow is represented by "+" and "-" signs. The packet length information is mapped to a new feature space  , ranging from 65536 to 68564, to avoid overlap with the feature space of the raw byte token sequence. The formal representation of the packet length token sequence is as follows:

$$
\text { Packet   length } = \left\{l _ {1},..., l _ {3 2} \right\}, l \in \mathbb {L} \tag {2}
$$

Where $l _ { i }$ represents the length of each packet.

# 2) Input Data Construction

The objective of the input data construction phase is to convert the extracted feature sequences into a format that can be accepted by the model. In this phase, the raw byte token sequence and packet length token sequence are concatenated to form a complete input sequence. Each input sequence begins with a special [CLS] token and is separated by a [SEP] token, which divides the two token sequences. Additionally, to ensure consistent sequence lengths across batches, the sequences are dynamically padded using the [PAD] token, facilitating batch training. Notably, a [MASK] token is introduced to aid in the subsequent masked sequence prediction task. The [CLS], [SEP], [PAD], and [MASK] tokens are assigned values of 68565, 68566, 68567, and 68568, respectively. The input data X is represented as follows:

$$
X = [ C L S ] + \text { Raw   bytes } + [ S E P ] + \text { Packet   length } + [ P A D ] \tag {3}
$$

Once the input data X is obtained, it is partitioned as follows: For labeled data, it is used exclusively for subsequent supervised learning tasks; while for a combination of labeled and unlabeled data, the entire dataset is treated as unlabeled data for the masked sequence prediction task.

# C. Masked Sequence Prediction

In the masked sequence prediction task, the input X undergoes processing by a random masking module to produce the masked input $\bar { \overline { { X } } }$ . To accelerate model convergence, the masking rate is initially set to 10%, gradually increasing to 15% as the model becomes more refined. Of the masked tokens, 80% are replaced with the [MASK] token, 10% are randomly replaced with other tokens, and the remaining 10% remain unchanged [26]. Special tokens, such as [CLS], [SEP], and [PAD], are exempt from masking, and only meaningful tokens with actual semantic content are subject to masking. Fig 2 illustrates an example of the masking strategy, where the token "0000" is replaced with [MASK], while a token like "0204" may be randomly substituted with "0302".

![](images/cc12582379ed532bbd81783dee738e8451a83446acb98397a66b4fb85b3f4c08.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["0000"] --> B["[MASK"]]
    B --> C["0000"]
    B --> D["8002"]
    B --> E["3908"]
    F["456c"] --> G["0000"]
    G --> H["0302"]
    H --> I["05b4"]
    I --> J["0101"]
    I --> K["0402"]
    I --> L["0103"]
    M["0204"] --> N
```
</details>

Figure 2. Masking Strategy Example

After the masking operation, the input data is passed through a word embedding module. This module consists of an embedding layer and a position encoding layer. Assuming the batch size is m and the padded sequence length is n , the dimension of the masked input data X is $\mathbb { R } ^ { m \times n }$ . In the embedding layer, each input token is mapped to a d - dimensional vector space, resulting in its corresponding embedded representation. During the position encoding process, a positional encoding is added to each token to account for its position within the sequence. This process can be formally expressed as:

$$
X _ {\text { embed }} = \text { word   embedding } (\widetilde {X}), X _ {\text { embed }} \in \mathbb {R} ^ {m \times n \times d} \tag {4}
$$

Where $X _ { e m b e d }$ represents the output of the embedding module applied to $\widetilde { X }$ . Next, $X _ { e m b e d }$ is fed into the Transformer encoder module. The Transformer encoder processes the input using a multi-head self-attention mechanism and a feed-forward neural network, producing an encoded output Encoded :

$$
\text { Encoded } _ {1} = \text { TransformerEncoder } (X _ {\text { embed }}) \tag {5}
$$

Finally, Encoded is mapped to the output dimensions corresponding to the size of the vocabulary via a linear layer. In this process, the model predicts the token at each masked position and maps it to a space of size  . The objective of the masked sequence prediction task is for the encoder to accurately predict the original unmasked sequence based on the masked token sequence. Since this task is inherently a multi-class classification problem, a cross-entropy loss function is used for training, which is defined as follows:

$$
L _ {m s p} = - \sum_ {i = 1} ^ {n} \log \left(P \left(M A S K _ {i} = t o k e n _ {i} \mid \widetilde {X}\right)\right) \tag {6}
$$

Where MASK represents the true token at the masked position in the input sequence. Through the learning of the masked sequence prediction task, the Transformer encoder is able to capture the contextual semantic information contained within the bidirectional flows, thus obtaining a generalizable traffic feature representation that enhances the model's generalization ability.

# D. Supervised Contrastive Learning

To enhance the model’s ability to represent known class samples and construct a more discriminative feature space, we introduce supervised contrastive learning. This method leverages label information to construct positive and negative sample pairs, thereby bringing samples of the same class closer together in the feature space while further separating samples from different classes. This process results in a compact intraclass distribution and clear inter-class boundaries within the feature space.

Algorithm 1 describes the specific process for training each batch in supervised contrastive learning. The feature queue, initialized in line 1, stores the sample features and their corresponding labels. The design of the feature queue is inspired by MoCo [27] and allows for real-time updates to maintain the most recent sample features. This provides more choices for constructing positive and negative sample pairs. Lines 2–6 describe the construction of positive sample pairs. For each sample $x _ { b a t c h } [ i ]$ in the current batch, a random sample with the same label, but from a different instance in the global dataset, is selected to form the positive pair. Lines 7–13 describe the construction of negative sample pairs, which are derived from two sources: (1) samples in the current batch that have a different label from the anchor sample, and (2) samples in the feature queue with a different label from the anchor sample. These two parts of negative samples are merged to form the complete negative sample set. Lines 12–15 update the feature queue, using a "first-in, first-out" (FIFO) strategy to ensure that the queue length does not exceed the set value Q .This design effectively mitigates the issue of limited sample sizes in individual batches and significantly improves the training performance of contrastive learning. Line 16 calculates the supervised contrastive learning loss, maximizing the similarity between positive pairs and minimizing the similarity between negative pairs, thus optimizing the feature space of the model.

Algorithm 1: Supervised Contrastive Learning   
Input: $x_{batch}$ : batch input samples; $y_{batch}$ : batch labels; B: batch size; $F_{queue}$ : feature queue; Q: queue size; $x_{dataset}$ , $y_{dataset}$ : all dataset and labels

Output: $L_{scl}$ : Contrastive loss; $F_{queue}$ : updated feature queue

Require: $z_{dataset}$ : Transformer encoder output; UpdateQueue: ( $F_{queue}$ , features, labels): update feature queue

1: set $F_{queue} = [\text{features:}\{\}, \text{labels:}\{\}]$ ;

2: for each $i \in [0, B]$ do:

3: positive pairs=negative pairs = [ ];

4: pos = { j | $y_{dataset}[j] = y_{batch}[i]$ , $x_{batch}[i] \neq x_{dataset}[j]$ };

5: $x_{pos} = \text{random}(x_{dataset}[pos])$ ;

6: positive pairs.append( $x_{batch}[i]$ , $x_{pos}$ );

7: for each $m \in [0, B]$ do:

8: neg batch = $\{x_{batch}[m] | y_{batch}[m] \neq y_{batch}[i]\}$ ;

9: end for

10: for each $(x_{dataset}[n], y_{dataset}[n]) \in F_{queue}$ ;

11: neg queue = $\{x_{dataset}[n] | y_{dataset}[n] \neq y_{batch}[i]\}$ ;

12: end for

13: negative pairs.append(neg batch, neg queue);

14: UpdateQueue( $F_{queue}$ , $z_{dataset}[i]$ , $y_{batch}[i]$ );

15: While len( $F_{queue}$ ) > Q :

16: $F_{queue} = F_{queue}[B]$ ;

17: $L_{scl}$ (positive pairs, negative pairs);

18: end for

19: return $F_{queue}$ , $L_{scl}$

The loss function is defined as:

$$
L _ {s c l} = - \frac {1}{N} \sum_ {i = 1} ^ {n} \log \frac {\exp \left(\operatorname{sim} \left(z _ {i} , z _ {j} ^ {+}\right) / \tau\right)}{\exp \left(\operatorname{sim} \left(z _ {i} , z _ {j} ^ {+}\right) / \tau + \sum_ {k = 1} ^ {q} \exp \left(\operatorname{sim} \left(z _ {i} , z _ {k} ^ {-}\right) / \tau\right) \right.} \tag {7}
$$

Where $z _ { i }$ represents the feature vector of the current sample, $z _ { j } ^ { + }$ represents the feature vector of the positive sample, and $z _ { k } ^ { - }$ represents the feature vector of the negative sample. The function sim $\left( z _ { a } , z _ { b } \right)$ is the cosine similarity between samples, and  is the temperature parameter.

During the training of the contrastive learning task, the Transformer encoder is responsible for extracting feature representations of the input data. However, directly using the encoder’s output to calculate the contrastive learning loss may cause the feature space to overly fit the contrastive learning objective, thereby reducing the generalizability of the feature representations. This issue is particularly problematic when the model needs to optimize the masked sequence prediction task simultaneously, as it may lead to conflicts between optimization objectives, limiting the generalization capability of the features learned by the encoder.

To address this issue, we adopt the projection head design inspired by SimCLR [28]. The projection head consists of linear layers that map the encoder’s output features to a dedicated projection space to optimize the contrastive learning loss. This design not only enhances the class separability of the feature space but also decouples the optimization objectives of contrastive learning from the feature learning goals of the encoder, effectively mitigating conflicts between the contrastive learning task and the masked sequence prediction task.

# E. Fine-tuning the Classification Head

Fine-tuning the classification head is the final phase of training, aimed at enabling the model to adapt to the classification tasks of different categories of encrypted traffic. In this phase, the parameters of the encoder are first frozen, treating it solely as a feature extraction module, which will no longer participate in subsequent gradient updates. Next, a classification head (Classification Head) structure is designed according to the number of categories in the specific encrypted traffic classification task. This head is used to map the highdimensional features output by the encoder to the task-specific category space. Finally, the model quickly converges and adapts to the new classification task by adjusting only the parameters of the classification head.

# IV. EXPERIMENT

# A. Dataset

In this experiment, we employed six publicly available datasets and one self-collected dataset for training and testing. Specifically, the datasets include DAPT2020 [29], CICAndMal2017 [30], Crossplatform [31], ISCX-Tor-nonTor [32], ISCX-VPN-nonVPN [33], USTC-TFC2016 [34], and XD-TLS (self-collected). Table 2 presents a summary of the datasets used in this study.

TABLE II. DATASET STATISTICS 

<table><tr><td>Dataset Name</td><td>Packets</td><td>Flows</td><td>Labels</td></tr><tr><td>DAPT2020</td><td>1863462</td><td>62576</td><td>20</td></tr><tr><td>CICAndMal2017</td><td>1997120</td><td>71576</td><td>42</td></tr><tr><td>Cross-Platform</td><td>1363761</td><td>48704</td><td>411</td></tr><tr><td>ISCX-Tor-nonTor</td><td>100588</td><td>9676</td><td>16</td></tr><tr><td>ISCX-VPN-nonVPN</td><td>53120</td><td>5602</td><td>12</td></tr><tr><td>USTC-TFC2016</td><td>97115</td><td>9853</td><td>20</td></tr><tr><td>XD-TLS(ours)</td><td>6071244</td><td>34545</td><td>N/A</td></tr></table>

DAPT2020: This dataset is constructed from network traffic captured over a 5-day period, where each day’s data is considered representative of approximately three months of real-world traffic scenarios.   
CICAndMal2017: Released by the Canadian Institute for Cybersecurity, this dataset contains traffic data from Android devices running both benign and malicious applications.   
Cross-Platform: This dataset includes traffic data from the top 100 applications in China, the United States, and India, covering both Android and iOS platforms.   
ISCX-Tor-nonTor: Captured by the Canadian Institute for Cybersecurity, this dataset contains encrypted traffic from 16 applications using the Tor (Onion Router) network.   
ISCX-VPN-nonVPN: This dataset includes traffic data from six communication applications, comparing VPN and non-VPN traffic.   
USTC-TFC2016: A dataset containing both benign and malicious encrypted traffic, consisting of 10 benign and 10 malicious traffic categories.   
XD-TLS: This is a self-collected dataset capturing TLS traffic generated over six days from a campus gateway

As shown in Table 3, the datasets used for training are divided into labeled and unlabeled datasets. The labeled dataset consists of 8 categories from the CICAndMal2017 dataset (referred to as CICAndMal2017-8). The unlabeled dataset includes DAPT2020, CICAndMal2017, XD-TLS, and Crossplatform, with a 9:1 ratio used for the training and validation split. For downstream tasks, the datasets include CICAndMal2017-8, ISCX-Tor-nonTor, ISCX-VPN-nonVPN, and USTC-TFC2016, which are further split into training, validation, and test sets with a ratio of 8:1:1. Specifically, CICAndMal2017-8 is used to evaluate the model’s performance on known categories, while ISCX-Tor-nonTor, ISCX-VPNnonVPN, and USTC-TFC2016 datasets are employed to assess the model’s ability to adapt to and generalize to unseen categories.

TABLE III. DATASET SPLIT 

<table><tr><td>Dataset Category</td><td>Dataset Name</td></tr><tr><td>Labeled Training Data</td><td>CICAndMal2017-8 (Dowgin, Feiwo, Charger, LockerPin, FakeApp, AVforandroid, Beanbot, fakeinst)</td></tr><tr><td>Unlabeled Training Data</td><td>DAPT2020, CICAndMal2017, Crossplatform, XD-TLS1.3</td></tr><tr><td>Downstream Task Data</td><td>CICAndMal2017-8, ISCX-Tor-nonTor, ISCX-VPN-nonVPN, USTC-TFC2016</td></tr></table>

# B. Experimental Details and Evaluation Metrics

The experiments were conducted within the PyTorch 1.13.1 framework and executed on a Linux server equipped with an Intel(R) Xeon(R) Platinum 8163 CPU and a Tesla V100 GPU.

TABLE IV. HYPERPARAMETER CONFIGURATION 

<table><tr><td>Hyperparameter</td><td>Value</td></tr><tr><td>Epoch</td><td>50</td></tr><tr><td>Learning rate</td><td>1e-5</td></tr><tr><td>Optimizer</td><td>AdamW</td></tr><tr><td>Batch size</td><td>16</td></tr><tr><td>d_model</td><td>768</td></tr><tr><td>nhead</td><td>12</td></tr><tr><td>num_encode_layers</td><td>3</td></tr><tr><td>dim_feedforward</td><td>1024</td></tr><tr><td>supervised contrastive temperature</td><td>0.07</td></tr><tr><td>warmup</td><td>0.05</td></tr><tr><td>patience (early stopping)</td><td>10</td></tr></table>

During the model training phase, the first task was the masked sequence prediction task, aimed at enabling the Transformer encoder to learn a more generalized representation of traffic features with enhanced adaptability. Due to the relatively slow convergence of the masked sequence prediction task, the accuracy of the masked sequence prediction and the loss function were monitored in real time throughout the training process. Once an improvement in these metrics was observed for three consecutive epochs, the model switched to the supervised contrastive learning task to optimize the feature space of the labeled data. The training process followed the hyperparameter configuration detailed in Table 4.

TABLE V. COMPARISON RESULTS ON ISCX-TOR, ISCX-NONTOR,CICANDMAL2017-8 

<table><tr><td>Dataset</td><td colspan="4">ISCX-Tor</td><td colspan="4">ISCX-nonTor</td><td colspan="4">CICAndMal2017-8</td></tr><tr><td>Method</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td></tr><tr><td>K-FP</td><td>0.7771</td><td>0.7417</td><td>0.6209</td><td>0.6313</td><td>0.8741</td><td>0.8653</td><td>0.7792</td><td>0.8167</td><td>0.7661</td><td>0.7531</td><td>0.7852</td><td>0.7644</td></tr><tr><td>DF</td><td>0.6514</td><td>0.4803</td><td>0.4767</td><td>0.4719</td><td>0.8568</td><td>0.8003</td><td>0.7415</td><td>0.7590</td><td>0.6187</td><td>0.5941</td><td>0.5971</td><td>0.5897</td></tr><tr><td>AppScanner</td><td>0.7543</td><td>0.6629</td><td>0.6042</td><td>0.6163</td><td>0.8475</td><td>0.8336</td><td>0.8501</td><td>0.8413</td><td>0.6686</td><td>0.5349</td><td>0.4899</td><td>0.4997</td></tr><tr><td>GraphDApp</td><td>0.4286</td><td>0.2557</td><td>0.2509</td><td>0.2281</td><td>0.6936</td><td>0.5447</td><td>0.5398</td><td>0.5352</td><td>0.8605</td><td>0.8143</td><td>0.7393</td><td>0.7627</td></tr><tr><td>ET-BERT</td><td>0.9543</td><td>0.9242</td><td>0.9606</td><td>0.9397</td><td>0.9029</td><td>0.8560</td><td>0.8217</td><td>0.8332</td><td>0.9865</td><td>0.9324</td><td>0.9266</td><td>0.9246</td></tr><tr><td>CoMask</td><td>0.9886</td><td>0.9770</td><td>0.9928</td><td>0.9848</td><td>0.9093</td><td>0.9087</td><td>0.9093</td><td>0.9051</td><td>0.9885</td><td>0.9887</td><td>0.9885</td><td>0.9886</td></tr></table>

TABLE VI. COMPARISON RESULTS ON ISCX-VPN, ISCX-NONVPN,USTC-TFC2016 

<table><tr><td>Dataset</td><td colspan="4">ISCX-VPN</td><td colspan="4">ISCX-nonVPN</td><td colspan="4">USTC-TFC2016</td></tr><tr><td>Method</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td></tr><tr><td>K-FP</td><td>0.8713</td><td>0.8750</td><td>0.8748</td><td>0.8747</td><td>0.7551</td><td>0.7478</td><td>0.7354</td><td>0.7387</td><td>0.8846</td><td>0.8846</td><td>0.8920</td><td>0.8840</td></tr><tr><td>DF</td><td>0.8012</td><td>0.7799</td><td>0.8152</td><td>0.7921</td><td>0.6742</td><td>0.6857</td><td>0.6717</td><td>0.6701</td><td>0.7787</td><td>0.7883</td><td>0.7819</td><td>0.7593</td></tr><tr><td>AppScanner</td><td>0.8889</td><td>0.8679</td><td>0.8815</td><td>0.8722</td><td>0.7576</td><td>0.7594</td><td>0.7465</td><td>0.7486</td><td>0.8954</td><td>0.8984</td><td>0.8968</td><td>0.8892</td></tr><tr><td>GraphDApp</td><td>0.6491</td><td>0.5668</td><td>0.6103</td><td>0.5740</td><td>0.4495</td><td>0.4230</td><td>0.3647</td><td>0.3614</td><td>0.8789</td><td>0.8226</td><td>0.8260</td><td>0.8234</td></tr><tr><td>ET-BERT</td><td>0.9532</td><td>0.9436</td><td>0.9507</td><td>0.9463</td><td>0.9167</td><td>0.9245</td><td>0.9229</td><td>0.9235</td><td>0.9929</td><td>0.9930</td><td>0.9930</td><td>0.9930</td></tr><tr><td>CoMask</td><td>0.9583</td><td>0.9578</td><td>0.9583</td><td>0.9579</td><td>0.9089</td><td>0.8857</td><td>0.9688</td><td>0.9254</td><td>0.9967</td><td>0.9967</td><td>0.9967</td><td>0.9967</td></tr></table>

To comprehensively assess the performance of CoMask, four distinct evaluation metrics were employed. For each class, the recall (Re) metric was used to measure the model's ability to retrieve samples of that class, ensuring no positive samples are missed. The precision (Pr) metric assessed the correctness of the samples returned by the model, ensuring that retrieved samples are indeed positive. The accuracy (Ac) metric provided a global performance measure, quantifying the overall correctness of the model's predictions across all classes. Lastly, the F1 score was calculated to consider the balance between recall and precision. The formulas for these four metrics are as follows:

$$
A c c u r a c y = \frac {T P + T N}{T P + T N + F P + F N} \tag {8}
$$

$$
P r e c i s i o n = \frac {T P}{T P + F P} \tag {9}
$$

$$
\text { Recall } = \frac {T P}{T P + F N} \tag {10}
$$

$$
F 1 - \text { score } = \frac {2 \times \text { Recall } \times \text { Precision }}{\text { Recall } \times \text { Precision }} \tag {11}
$$

# C. Comparative Experiments

To comprehensively evaluate the performance of the CoMask model, five baseline models were selected for comparison, as follows:

K-FP [35]: This model extracts traffic fingerprints using a random forest and applies the k-NN algorithm for open-world classification. It compares the fingerprints of test instances with training instances using Hamming distance for traffic classification.   
DF [17]: This model is the first deep learning-based method optimized for Tor traffic defense mechanisms. It utilizes a multi-layer convolutional neural network architecture that automatically extracts temporal features of traffic and achieves high-accuracy recognition in both defensive and non-defensive scenarios.   
AppScanner [36]: This model leverages the spatiotemporal features of encrypted network traffic and combines support vector machines with random forest machine learning methods to achieve high-precision

real-time fingerprint recognition of smartphone applications.

GraphDApp [37]: The first model to introduce graph neural networks (GNNs) into the encrypted traffic classification of decentralized applications (DApps). By constructing a traffic interaction graph to represent encrypted traffic, it transforms the traffic classification task into a graph classification problem, thereby improving the accuracy of DApp traffic classification.   
ET-BERT [38]: The first model to utilize pre-trained models for encrypted traffic classification. By training two self-supervised tasks related to traffic, it captures the contextual relationships between traffic instances, obtaining a universal data representation and achieving significant results across multiple downstream tasks.

Tables 5, 6 present the comparison results of CoMask across various datasets. With the exception of the ISCX-nonVPN dataset, CoMask achieved the best performance on all datasets. Compared to traditional methods based on statistical features and machine learning algorithms (such as K-FP and AppScanner), CoMask improved the average F1 score by 0.1748 and 0.2073, respectively. In comparison to deep learning-based methods (such as DF and GraphDApp), CoMask achieved improvements of 0.2825 and 0.3456 in average F1 scores, respectively. Furthermore, CoMask outperformed the pretrained model ET-BERT by 0.033 in the average F1 score. These results demonstrate that CoMask not only achieves highprecision classification on known traffic categories (CICAndMal2017-8) but also adapts rapidly to classify unknown categories of traffic through fine-tuning.

For the ISCX-nonVPN dataset, the analysis reveals a significant class imbalance issue, which still presents challenges for CoMask when handling imbalanced data. However, thanks to the optimization of the feature space via the masked sequence prediction task and supervised contrastive learning task, CoMask outperformed most existing classifiers and is capable of addressing a wide range of encrypted traffic classification tasks, showcasing its strong generalization ability.

# D. Ablation Study

To further investigate the contribution of each component in the CoMask model to its overall performance, we conducted four sets of ablation experiments. In these experiments, we removed key components from CoMask, including Masked Sequence Prediction (MSP), Supervised Contrastive Learning (SCL), Raw Byte Token Sequences (RB), and Packet Length

Token Sequences (PL), and compared the model’s performance across different datasets under these modified conditions. The results of the experiments are presented in Table 7, 8.

TABLE VII. ABLATION STUDY OF KEY COMPONENTS ON F1-SCORE FOR ISCX-TOR, ISCX-NONTOR AND CICANDMAL2017-8 DATASETS 

<table><tr><td>Method</td><td>ISCX-Tor</td><td>ISCX-nonTor</td><td>CICAndMal2017-8</td></tr><tr><td>CoMask</td><td>0.9848</td><td>0.9051</td><td>0.9886</td></tr><tr><td>w/o MSP</td><td>0.3124</td><td>0.2275</td><td>0.9763</td></tr><tr><td>w/o SCL</td><td>0.9813</td><td>0.8665</td><td>0.9647</td></tr><tr><td>w/o RB</td><td>0.9155</td><td>0.8238</td><td>0.9302</td></tr><tr><td>w/o PL</td><td>0.9333</td><td>0.8351</td><td>0.9418</td></tr></table>

TABLE VIII. ABLATION STUDY OF KEY COMPONENTS ON F1-SCORE FOR ISCX-VPN, ISCX-NONVPN AND USTC-TFC2016 DATASETS 

<table><tr><td>Method</td><td>ISCX-VPN</td><td>ISCX-nonVPN</td><td>USTC-TFC2016</td></tr><tr><td>CoMask</td><td>0.9579</td><td>0.9254</td><td>0.9967</td></tr><tr><td>w/o MSP</td><td>0.1786</td><td>0.0117</td><td>0.6583</td></tr><tr><td>w/o SCL</td><td>0.9468</td><td>0.9196</td><td>0.9885</td></tr><tr><td>w/o RB</td><td>0.7759</td><td>0.8146</td><td>0.9508</td></tr><tr><td>w/o PL</td><td>0.8188</td><td>0.8485</td><td>0.9493</td></tr></table>

# 1) Detection Analysis on Known and Unknown Categories

To assess the model's detection capability on known and unknown category datasets, we evaluated the model's performance by removing the MSP and SCL modules. The results presented in Table 8 show that removing the MSP module led to a decrease in F1 score by 0.0123 on the CICAndMal2017-8 dataset, and a more significant drop of 0.6757 in the average F1 score across the other datasets. This indicates a substantial degradation in performance. When the SCL module was removed, the classification accuracy on CICAndMal2017-8 dropped further compared to the removal of MSP, but the detection accuracy on other datasets improved. These findings suggest that the MSP module plays a crucial role in learning generalizable representations of traffic features, thus enhancing the model's ability to generalize to unknown categories. On the other hand, the SCL module improves the model’s detection capability for known categories and optimizes the overall feature space representation. The complementary effects of MSP and SCL modules enable CoMask to perform excellently on both known and unknown category detection tasks.

# 2) Analysis of Multi-granularity Feature Sequences

To evaluate the impact of token input feature sequences at different granularities on model performance, we conducted ablation experiments by removing the Raw Byte (RB) and Packet Length (PL) token sequences. After removing the Raw Byte token sequence, the average F1 score dropped by 0.091. In contrast, removing the Packet Length token sequence resulted in a smaller decline of 0.072 in the average F1 score. These results suggest that the Raw Byte token sequence contributes more significantly to capturing the contextual information of traffic bytes and modeling behaviors, thus providing a greater performance boost. However, certain datasets exhibit distinctive characteristics. For example, on the USTC-TFC2016 dataset, the removal of the Packet Length token sequence (PL) led to a more noticeable decline in F1 score than the removal of the Raw Byte token sequence (RB), suggesting that in some traffic types, the Packet Length token sequence may possess stronger representational power.

# E. Hyperparameter Sensitivity Analysis

To further understand the relationship between the performance of the CoMask model and its hyperparameter settings, we conducted a sensitivity analysis focusing on the number of layers in the Transformer encoder and the temperature coefficient in Supervised Contrastive Learning. The number of encoder layers was varied in the range of [1, 6], while the temperature coefficient was explored within the range of [0, 0.1].

![](images/42abe4a69c1d26134994c3a177b9c3d63e3cb3af4cec82b8c3ea83f0cf4290a0.jpg)

<details>
<summary>bar</summary>

| Num_encoder_layers | F1% | Training Time(s) |
|---|---|---|
| 1 | 92 | 9800 |
| 2 | 93 | 10600 |
| 3 | 95 | 11200 |
| 4 | 94 | 11700 |
| 5 | 94 | 12300 |
| 6 | 95 | 14000 |
</details>

Figure 3. Sensitivity Analysis of Encoder Layers

![](images/9d893362518dd4400ea974e20b1c64b0c2260e18d31545550d35f1a13c1bf0aa.jpg)

<details>
<summary>line</summary>

| Temperature | ISCX-Tor | ISCX-nonTor | ISCX-VPN | ISCX-nonVPN | CICAndMal2017-8 | USTC-TFC2016 |
| ----------- | -------- | ----------- | -------- | ----------- | --------------- | ------------ |
| 0.00        | 0.95     | 0.88        | 0.92     | 0.89        | 0.96            | 0.97         |
| 0.02        | 0.96     | 0.89        | 0.93     | 0.90        | 0.97            | 0.98         |
| 0.04        | 0.97     | 0.90        | 0.94     | 0.91        | 0.98            | 0.99         |
| 0.06        | 0.98     | 0.91        | 0.95     | 0.92        | 0.99            | 1.00         |
| 0.08        | 0.98     | 0.91        | 0.95     | 0.92        | 0.99            | 1.00         |
| 0.10        | 0.96     | 0.90        | 0.94     | 0.92        | 0.98            | 0.99         |
</details>

Figure 4. Sensitivity Analysis of Temperature Coefficient

Fig. 3 presents the results of the sensitivity analysis for the number of encoder layers. The experimental results show that as the number of encoder layers increases, both the F1 score and training time exhibit corresponding trends. When the number of layers increased from 1 to 3, the F1 score gradually improved, while the training time also increased. However, as the number of layers increased further from 4 to 6, the F1 score reached a plateau, with the highest value of 96.31 achieved at 6 layers, while the training time reached its maximum. Considering both performance and efficiency, we selected 3 layers as the optimal number of encoder layers.

Next, we performed a sensitivity analysis of the temperature coefficient, the results of which are shown in Fig. 4. As the temperature coefficient increased from 0.01 to 0.07, the F1 score gradually improved, reaching its peak value at 0.07. Beyond this point, the F1 score started to decline. This suggests that the model’s feature optimization achieves the best balance at a temperature coefficient of 0.07, while higher values of the temperature coefficient may lead to a degradation in performance.

# V. CONCLUSIONS

In this paper, we propose CoMask, a semi-supervised learning framework for encrypted traffic classification that integrates supervised contrastive learning and mask prediction tasks. This framework aims to learn a universal feature representation space for traffic by fully leveraging both labeled and unlabeled data. CoMask successfully achieves encrypted traffic classification across multiple scenarios by fine-tuning classification heads for different tasks. The framework adopts a cross-training strategy, combining mask prediction and supervised contrastive learning tasks, which not only improves classification accuracy for known traffic categories but also enables rapid adaptation to classification tasks for unknown traffic.

Through systematic experimental evaluations on six public datasets, the results demonstrate that CoMask outperforms existing methods, with F1 scores improved by 4.51%, 7.19%, 1.13%, 0.19%, 6.4%, and 0.37%, respectively, showcasing its advantages in feature space optimization and generalization capability. Further ablation experiments indicate that the integration of mask prediction tasks, supervised contrastive learning tasks, and multi-granularity feature sequences significantly enhances the overall performance of the model.

# ACKNOWLEDGMENT

This research was supported by the National Natural Science Foundation of China (Nos. 62302520 and 62402524). I would like to express my sincere gratitude to all those who have contributed to and supported this research.

# REFERENCES

[1] Zscaler, https://ir.zscaler.com/news-releases/news-releasedetails/zscaler-finds-over-87-cyberthreats-hide-encrypted-traffic.   
[2] Bujlow T, Carela-Español V, Barlet-Ros P. Independent comparison of popular DPI tools for traffic classification[J]. Computer Networks, 2015, 76: 75-89.   
[3] 2025. Suricata Open Source IDS/IPS/NSM Engine. Retrieved Jan 16, 2025 from https://suricata.io/.   
[4] 2025. The Snort IDS/IPS. Retrieved Jan 16, 2025 from https://www.snort.org/.   
[5] 2020. The Zeek Network Security Monitor. Retrieved Jan 16, 2025 from https://www.zeek.org/.   
[6] Barradas D, Santos N, Rodrigues L. Effective detection of multimedia protocol tunneling using machine learning[C]//27th USENIX Security Symposium (USENIX Security 18). 2018: 169-185.   
[7] Anderson, Blake, and David McGrew. "Machine learning for encrypted malware traffic classification: accounting for noisy labels and non-

stationarity." Proceedings of the 23rd ACM SIGKDD International Conference on knowledge discovery and data mining. 2017.   
[8] Arash Habibi Lashkari., Gerard Draper Gil., Mohammad Saiful Islam Mamun., and Ali A. Ghorbani. 2017. Characterization of Tor traffic using time based features. In International Conference on Information Systems Security and Privacy. 253–262.   
[9] Aceto, Giuseppe, et al. "MIMETIC: Mobile encrypted traffic classification using multimodal deep learning." Computer networks 165 (2019): 106944.   
[10] Aceto, Giuseppe, et al. "DISTILLER: Encrypted traffic classification via multimodal multitask deep learning." Journal of Network and Computer Applications 183 (2021): 102985.   
[11] Wang, Xiangbin, et al. "Combine intra-and inter-flow: A multimodal encrypted traffic classification model driven by diverse features." Computer Networks 245 (2024): 110403.   
[12] N. Hua, H. Song, and T. V. Lakshman, “Variable-Stride Multi-Pattern Matching For Scalable Deep Packet Inspection,” in INFOCOM 2009, IEEE, 2009, pp. 415–423.   
[13] S. Fernandes, R. Antonello, T. Lacerda, A. Santos, D. Sadok, and T. Westholm, “Slimming Down Deep Packet Inspection Systems,” in INFOCOM Workshops 2009, IEEE, 2009, pp. 1–6.   
[14] Lan J, Liu X, Li B, et al. DarknetSec: A novel self-attentive deep learning method for darknet traffic classification and application identification[J]. Computers & Security, 2022, 116: 102663.   
[15] Xu S J, Geng G G, Jin X B, et al. Seeing traffic paths: Encrypted traffic classification with path signature features[J]. IEEE Transactions on Information Forensics and Security, 2022, 17: 2166-2181.   
[16] Fu Z, Liu M, Qin Y, et al. Encrypted malware traffic detection via graphbased network analysis[C]//Proceedings of the 25th International Symposium on Research in Attacks, Intrusions and Defenses. 2022: 495- 509.   
[17] Payap Sirinam, Mohsen Imani, Marc Juárez, and et al. 2018. Deep Fingerprinting: Undermining Website Fingerprinting Defenses with Deep Learning. In Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security, CCS 2018, Toronto, ON, Canada, October 15-19. 1928–1943.   
[18] Eyal Horowicz, Tal Shapira, and Yuval Shavitt. 2022. A Few Shots Traffic Classification with Mini-FlowPic Augmentations. In Proceedings of the 22nd ACM Internet Measurement Conference (IMC ’22). Association for Computing Machinery, New York, NY, USA, 647–654.   
[19] Lotfollahi M, Jafari Siavoshani M, Shirali Hossein Zade R, et al. Deep packet: A novel approach for encrypted traffic classification using deep learning[J]. Soft Computing, 2020, 24(3): 1999-2012.   
[20] Zhang H, Yu L, Xiao X, et al. TFE-GNN: A Temporal Fusion Encoder Using Graph Neural Networks for Fine-grained Encrypted Traffic Classification[C]//Proceedings of the ACM Web Conference 2023. 2023: 2066-2075.   
[21] Sun, Jiakun, et al. "CoMDet: A Contrastive Multimodal Pre-Training Approach to Encrypted Malicious Traffic Detection." 2024 IEEE 48th Annual Computers, Software, and Applications Conference (COMPSAC). IEEE, 2024.   
[22] Ma, Yuxiang, et al. "A balanced supervised contrastive learning-based method for encrypted network traffic classification." Computers & Security 145 (2024): 104023.   
[23] Cai, Wei, et al. "Incremental encrypted traffic classification via contrastive prototype networks." Computer Networks (2024): 110591.   
[24] Zhang, Haozhen, et al. "One Train for Two Tasks: An Encrypted Traffic Classification Framework Using Supervised Contrastive Learning." arXiv preprint arXiv:2402.07501 (2024).   
[25] Finamore, Alessandro, et al. "Replication: Contrastive Learning and Data Augmentation in Traffic Classification Using a Flowpic Input Representation." Proceedings of the 2023 ACM on Internet Measurement Conference. 2023.   
[26] Kenton, Jacob Devlin Ming-Wei Chang, and Lee Kristina Toutanova. "Bert: Pre-training of deep bidirectional transformers for language understanding." Proceedings of naacL-HLT. Vol. 1. No. 2. 2019.

[27] He, Kaiming, et al. "Momentum contrast for unsupervised visual representation learning." Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 2020.   
[28] Chen, Ting, et al. "A simple framework for contrastive learning of visual representations." International conference on machine learning. PMLR, 2020.   
[29] Sowmya Myneni, Ankur Chowdhary, Abdulhakim Sabur, Sailik Sengupta, Garima Agrawal, Dijiang Huang, and Myong Kang."Dapt 2020- constructing a benchmark dataset for advanced persistent threats."In International Workshop on Deployable Machine Learning for Security Defense, pp. 138-163. Springer, Cham, 2020.   
[30] Arash Habibi Lashkari, Andi Fitriah A. Kadir, Laya Taheri, and Ali A. Ghorbani, “Toward Developing a Systematic Approach to Generate Benchmark Android Malware Datasets and Classification”, In the proceedings of the 52nd IEEE International Carnahan Conference on Security Technology (ICCST), Montreal, Quebec, Canada, 2018.   
[31] Thijs van Ede, Riccardo Bortolameotti, Andrea Continella, and et al. 2020. FlowPrint: Semi-Supervised Mobile-App Fingerprinting on Encrypted Network Traffic. In 27th Annual Network and Distributed System Security Symposium, NDSS 2020, San Diego, California, USA, February 23-26, 2020. The Internet Society.   
[32] Arash Habibi Lashkari, Gerard Draper-Gil, Mohammad Saiful Islam Mamun and Ali A. Ghorbani, "Characterization of Tor Traffic Using Time Based Features", In the proceeding of the 3rd International Conference on Information System Security and Privacy, SCITEPRESS, Porto, Portugal, 2017.   
[33] Gerard Drapper Gil, Arash Habibi Lashkari, Mohammad Mamun, Ali A. Ghorbani, "Characterization of Encrypted and VPN Traffic Using Time-Related Features", In Proceedings of the 2nd International Conference on Information Systems Security and Privacy(ICISSP 2016) , pages 407-414, Rome, Italy.   
[34] Wei Wang, Ming Zhu, Xuewen Zeng, and et al. 2017. Malware traffic classification using convolutional neural network for representation learning. In 2017 International Conference on Information Networking, ICOIN 2017, Da Nang, Vietnam, January 11-13, 2017. IEEE, 712–717.   
[35] Jamie Hayes and George Danezis. 2016. k-fingerprinting: a Robust Scalable Website Fingerprinting Technique. In USENIX Security Symposium. 1187–1203.   
[36] Vincent F. Taylor, Riccardo Spolaor, Mauro Conti, and Ivan Martinovic. 2016. AppScanner: Automatic Fingerprinting of Smartphone Apps From Encrypted Network Traffic. In IEEE European Symposium on Security and Privacy. 439–454.   
[37] Meng Shen, Jinpeng Zhang, Liehuang Zhu, Ke Xu, and Xiaojiang Du. 2021. Accurate Decentralized Application Identification via Encrypted Traffic Analysis Using Graph Neural Networks. IEEE Transactions on Information Forensics and Security 16, 1 (2021), 2367–2380.   
[38] Xinjie Lin, Gang Xiong, Gaopeng Gou, Zhen Li, Junzheng Shi, and Jing Yu. 2022. ET-BERT: A Contextualized Datagram Representation with Pre-training Transformers for Encrypted Traffic Classification. In The Web Conference. 633– 642.
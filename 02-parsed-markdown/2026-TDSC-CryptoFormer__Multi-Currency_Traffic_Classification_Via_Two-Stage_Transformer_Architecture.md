# CryptoFormer: Multi-Currency Traffic Classification via Two-Stage Transformer Architecture

Zhenyu Guo, Zijian Zhang<sup>∗</sup>, Member, IEEE, Yan Wu, Jiahang Sun, Jiamou Liu, Xin Li, Yajie Wang, Guoqiang Zhang, Lei Zhang<sup>∗</sup>, and Liehuang Zhu, Senior Member, IEEE

Abstract—Accurate identification of cryptocurrency traffic is essential for regulatory and forensic applications such as anti-money laundering, illicit transaction tracing, and protocolspecific risk assessment. However, real-time classification remains challenging due to encryption heterogeneity across blockchain protocols and the interleaving of multiple currencies in peerto-peer networks. To address this, we propose CryptoFormer, a Transformer-based framework for multi-currency traffic classification. CryptoFormer introduces a two-stage architecture that separately captures packet-level semantics and sessionlevel behavioral patterns. An adaptive gated fusion module further integrates both content and behavioral features, enabling robust representation learning across plaintext and ciphertext protocols without decryption. We also construct a labeled realworld traffic dataset covering eighteen cryptocurrency assets and diverse background noise, capturing protocol diversity and deployment realism. Experimental results show that Crypto-Former achieves a macro F1-score of 95.02%, outperforming strong baselines including ET-BERT and TrafficFormer. Despite its shallow structure and smaller training corpus, CryptoFormer delivers comparable or better accuracy with significantly lower computational overhead, making it suitable for deployment in regulatory, compliance, and edge-monitoring systems.

Index Terms—Cryptocurrencies Identification, Traffic Classification, Transformer, Blockchain Governance.

## I. INTRODUCTION

S decentralized finance continues to evolve, cryptocurrencies such as Bitcoin and Ethereum are playing an increasingly prominent role in global financial ecosystems [1]. According to the CoinGecko 2025 Report, the total cryptocurrency market capitalization has exceeded 3.0 trillion USD, pushing average daily trading volumes to a yearly high of 161.8 billion USD [2]. These transactions generate vast amounts of network traffic across peer-to-peer (P2P) overlays [3], carrying valuable forensic signals embedded in packet behavior, propagation patterns, and encryption schemes. Accurate classification of such traffic is crucial for various regulatory and security applications, including anti-money laundering (AML), fraud detection, illicit transaction tracing, and cross-chain forensics [4]–[6].

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/0c2621e4840ef1066489678da19549a5f778f95f706538aa9b0e639e91a1097e.jpg)  
Fig. 1. Traffic identification task. Traffic identification is a crucial prerequisite for numerous downstream tasks related to blockchain networks.

In particular, real-time identification of the specific cryptocurrency associated with a traffic flow plays a foundational role in risk-sensitive blockchain governance. As shown in Fig. 1, Government agencies and regulatory platforms often rely on network-level observations to detect unauthorized mining, address anonymized transfers, or correlate transaction volume with suspicious actors [7]. Traditional approaches to cryptocurrency traceability have primarily focused on transaction graph analysis or wallet attribution [8]–[10], which rely on access to ledger contents. However, in privacy-centric or encryption-heavy protocols, such as on-chain access, it is limited or obfuscated. Network-layer traffic classification thus serves as a complementary and often necessary source of signals for forensics and enforcement.

Yet, the task of identifying cryptocurrencies directly from network flows remains fundamentally challenging due to several real-world constraints [11]. First, blockchain networks often carry traffic from multiple currencies simultaneously, resulting in interleaved flows with overlapping behaviors and protocol similarities. These include shared protocol primitives (e.g., INV/ADDR/GETDATA messages) [12] or inherited protocol stacks across Bitcoin forks [13]. Second, different currencies adopt diverse cryptographic protocols—ranging from plaintext JSON-RPC [14] to Ethereum’s RLPx [15] and Monero’s Tor-based obfuscation [16]—making semantic feature extraction inconsistent or even infeasible. Third, blockchain traffic typically spans long-lived sessions with sparse and variable interactions [17], where packet content alone is insufficient to capture full transactional context. These factors together pose unique technical bottlenecks for reliable traffic classification.

Existing solutions to traffic identification predominantly fall into two categories: (i) statistical methods leveraging handcrafted flow-level features [17], [18], and (ii) deep learning models adapted from general-purpose architectures such as BERT [19], [20]. While statistical classifiers such as App-Scanner [21] or FS-Net [22] exhibit moderate performance in traditional application-level traffic, they fail to capture protocol-specific variations or cross-currency overlaps. On the other hand, deep learning methods—especially those based on Transformers—have shown promise in encrypted VPN/Tor scenarios by learning semantic embeddings from packet payloads. However, these models typically assume clean session boundaries, single-protocol conditions, and high-quality plaintext input. They lack mechanisms to disentangle protocol semantics from behavioral features, and often depend on largescale pretraining to achieve reasonable generalization.

To address these challenges, we introduce CryptoFormer, a lightweight and protocol-agnostic Transformer framework for multi-currency encrypted traffic classification. CryptoFormer is designed to operate in realistic blockchain communication environments where protocol diversity, encryption heterogeneity, and interleaved currency flows are the norm. It avoids the need for payload decryption or protocol-specific parsers by unifying content and behavior into a joint representation space.

Specifically, CryptoFormer introduces a two-stage Transformer architecture: the first stage extracts packet-level semantic features from byte-level payload embeddings, while the second stage captures flow-level behavioral dynamics through sequential modeling. This design reflects the intuition that packet content and session behavior encode complementary information, especially in sparse or encrypted environments. To further enhance adaptability, we incorporate an adaptive gated fusion module that learns how much to trust each modality based on packet informativeness. For instance, when payloads are ciphertext, the model emphasizes timing, direction, and flag-based features; when plaintext content is present, it adjusts accordingly. This fine-grained gating improves robustness across protocols with varying degrees of observability.

In parallel, we construct a comprehensive multi-currency traffic dataset containing encrypted flows from eighteen cryptocurrency assets: Bitcoin (BTC), Ethereum (ETH), Bitcoin Cash (BCH), Bitcoin SV (BSV), Litecoin (LTC), Dogecoin (DOGE), TRON (TRX), Monero (XMR), Tether USDT (USDT), USD Coin (USDC), PEPE, Chainlink (LINK), Wrapped Ether (WETH), Wrapped Bitcoin (WBTC), Lido Staked Ether (stETH), Uniswap (UNI), Toncoin (TONCOIN), and BNB. These flows are captured using synchronized node-side logging and external packet sniffing in productionsimulated environments. Unlike prior datasets limited to single-protocol capture or synthetic flows, our dataset includes both plaintext and encrypted protocols, background noise, protocol version diversity, and network perturbations, making it a realistic benchmark for encrypted traffic classification.

Our main contributions are summarized as follows:

• We formalize the task of multi-currency encrypted traffic classification and propose CryptoFormer, a lightweight Transformer architecture that achieves strong performance without requiring pretraining or protocol-specific customization.

• We introduce a two-stage representation learning framework that jointly captures packet-level content semantics and session-level behavioral dynamics, enabling robust discrimination under protocol overlap and flow sparsity.

• We design an adaptive gated fusion module that dynamically adjusts the importance of content and behavioral features based on payload informativeness, improving classification across encryption conditions.

• We release a comprehensive labeled dataset of real-world cryptocurrency traffic covering eighteen assets across multiple protocol families, both plaintext and ciphertext protocols, and realistic network conditions, which we hope will benefit future research on encrypted traffic understanding.

## II. RELATED WORK

The evolution of cryptocurrency network traffic classification has progressed through three distinct phases: rule-based matching, machine learning, and deep learning. Early studies predominantly employed expert-driven rule-based methods. Biryukov et al. [23] demonstrated that Bitcoin’s default communication port (8333) could expose transaction behaviors, enabling effective Bitcoin traffic filtering through port analysis. However, advancements in blockchain protocols—particularly the adoption of dynamic port allocation mechanisms—have rendered such methods increasingly obsolete [24].

This limitation prompted researchers to shift toward machine-learning approaches utilizing statistical traffic features. For instance, Kim et al. [25] applied Support Vector Machines (SVM) to Bitcoin identification, achieving 85.7% accuracy by extracting statistical features such as packet sizes and inter-arrival time intervals. While these methods marked a significant advancement, their reliance on manual feature engineering severely limits generalization capabilities when applied to emerging cryptocurrencies [26].

Recent years have witnessed remarkable advancements in deep learning for network traffic classification [27]. Chen et al. [28] pioneered a CNN-based traffic classification model by transforming raw traffic data into grayscale images, achieving effective identification of generic network traffic. To address feature extraction challenges in encrypted traffic, Xu et al. [29] proposed a path signature-based framework, constructing traffic paths using session packet length sequences to extract multi-scale temporal patterns. Meanwhile, Liu et al. [30] developed a flow-aware deep learning model that captures sequential semantic features for classification. Following the emergence of pre-trained models, Lin et al. [20] adapted the BERT architecture to encrypted traffic classification, leveraging language model pre-training to learn semantic traffic representations, which outperformed traditional methods.

While existing approaches have advanced traffic classification, they exhibit critical limitations in multi-currency cryptocurrency environments. Statistical methods and basic

TABLE I  
COMPARISON OF DESIGN WITH STATE-OF-THE-ART CLASSIFIERS

<table><tr><td>Method</td><td>Backbone</td><td>Hierarchical</td><td>Encryption-Aware</td><td>Pretraining-Free</td><td>Multi-Currency Focus</td></tr><tr><td colspan="6">Statistical Methods</td></tr><tr><td>Appscanner [21]</td><td>Random Forest</td><td>×</td><td>×</td><td>√</td><td>×</td></tr><tr><td>Deep Fingerprinting [31]</td><td>CNN</td><td>×</td><td>√</td><td>√</td><td>×</td></tr><tr><td colspan="6">Convolutional / RNN Methods</td></tr><tr><td>Deep Packet [36]</td><td>CNN</td><td>×</td><td>√</td><td>√</td><td>×</td></tr><tr><td>FS-Net [30]</td><td>Bi-GRU</td><td>×</td><td>√</td><td>√</td><td>×</td></tr><tr><td colspan="6">Transformer-based Methods</td></tr><tr><td>PerFormer [37]</td><td>Transformer</td><td>×</td><td>√</td><td>×</td><td>×</td></tr><tr><td>LongFormer [38]</td><td>Transformer</td><td>×</td><td>√</td><td>×</td><td>×</td></tr><tr><td colspan="6">Pre-trained Methods</td></tr><tr><td>TrafficFormer [33]</td><td>Transformer</td><td>√</td><td>√</td><td>×</td><td>×</td></tr><tr><td>ET-BERT [20]</td><td>Transformer</td><td>√</td><td>√</td><td>×</td><td>×</td></tr><tr><td colspan="6">Ours</td></tr><tr><td>CryptoFormer</td><td>Two-Stage Transformer</td><td>√</td><td>√</td><td>√</td><td>√</td></tr></table>

CNNs such as Appscanner [21] and Deep Fingerprinting [31] treat traffic as homogeneous byte streams or shallow statistical aggregates, failing to disentangle content semantics from behavioral dynamics. This is particularly detrimental when payloads are encrypted, rendering content features noisy and unreliable [32]. More recent Transformer-based models such as ET-BERT [20] and TrafficFormer [33] achieve strong performance through large-scale pretraining, yet they implicitly assume semantic patterns are uniformly distributed across a session. They lack a dedicated mechanism to cope with protocol-induced encryption heterogeneity, where payload informativeness varies drastically within the same flow. [34] Furthermore, existing deep models typically ingest sessions as flat sequences, overlooking the natural hierarchy of blockchain communication and leading to suboptimal robustness under flow sparsity and multi-currency interference [35].

CryptoFormer addresses these gaps through a two-stage hierarchical Transformer that decouples packet-level semantics from session-level behavioral patterns, an adaptive gated fusion mechanism that dynamically recalibrates content and behavior contributions based on payload observability, and a lightweight pretraining-free design that achieves superior accuracy with lower computational overhead. Table I contrasts CryptoFormer with representative baselines across key design dimensions.

## III. PRELIMINARIES

## A. Problem Definition

We define multi-currency encrypted cryptocurrency traffic classification as a session-level multi-class classification problem. Let a sequence of packets represent a session:

$$
\mathcal {S} = \{p _ {1}, p _ {2}, \dots , p _ {n} \},
$$

where each packet $p _ { i }$ contains raw payload bytes $b _ { i } \in \{ 0 , 1 \} ^ { l _ { i } }$ of variable length, and associated metadata (e.g., direction, timestamp, length). The session S corresponds to a communication flow involving one of M cryptocurrency protocols or noise background.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/6e2e2a4619bde65ba2e10c42feb46010fd3131f393de5f0f5f12d81ac3ea34f3.jpg)  
Step 3: Send information required  
Fig. 2. Bitcoin node communication protocol. A new transaction triggers message exchanges including announcement (INV), request (GETDATA), and relay (TX), forming structured sessions captured for classification.

Let the set of class labels be:

$$
\mathcal {C} = \{C _ {1}, C _ {2}, \dots , C _ {M}, \text { Noise } \},
$$

where each $C _ { j }$ represents a cryptocurrency (e.g., BTC, ETH), and ”Noise” refers to non-cryptocurrency background traffic. The goal is to learn a mapping function:

$$
f _ {\theta}: \mathcal {S} \mapsto \hat {y}, \quad \hat {y} \in \mathcal {C},
$$

parameterized by $\theta ,$ such that $\hat { y }$ approximates the true class label $y ^ { * }$ of the session S. The model is trained over a dataset:

$$
\mathcal {D} = \{(\mathcal {S} ^ {(i)}, y ^ {(i)}) \} _ {i = 1} ^ {N},
$$

and optimized to minimize a multi-class classification loss (e.g., cross-entropy):

$$
\mathcal {L} = - \sum_ {i = 1} ^ {N} \sum_ {j = 1} ^ {M + 1} \mathbb {I} (y ^ {(i)} = C _ {j}) \log P _ {\theta} (C _ {j} \mid \mathcal {S} ^ {(i)}),
$$

where $P _ { \theta } ( C _ { j } \mid \mathcal { S } )$ denotes the predicted probability that session S belongs to class $C _ { j }$ , and I(·) is the indicator function.

This problem setting captures the key challenges of classifying encrypted, heterogeneous, and multi-currency traffic without access to decrypted content. It also enables rigorous benchmarking across currencies, sessions, and protocol types.

TABLE II  
SUMMARY OF KEY NOTATIONS

<table><tr><td>Symbol</td><td>Description</td></tr><tr><td> $\mathcal{S}$ </td><td>A traffic session consisting of  $n$  packets  $\{p_1, \dots, p_n\}$ </td></tr><tr><td> $p_i$ </td><td>The  $i$ -th packet in the session</td></tr><tr><td> $b_i$ </td><td>Raw payload bytes of packet  $p_i$ </td></tr><tr><td> $\mathbf{e}_i$ </td><td>Byte-level token embedding of  $p_i$ </td></tr><tr><td> $\mathbf{f}_i$ </td><td>Concatenated and normalized behavioral feature vector of  $p_i$ </td></tr><tr><td> $\mathbf{h}_{content_i}$ </td><td>Packet-level semantic representation from Stage I</td></tr><tr><td> $\mathbf{h}_{behavior_i}$ </td><td>Packet-level behavioral metadata embedding</td></tr><tr><td> $\alpha$ </td><td>Adaptive gating coefficient  $\in [0, 1]$ </td></tr><tr><td> $\mathbf{h}_{fusion}$ </td><td>Fused representation after gated combination</td></tr><tr><td> $\mathbf{h}_{session}$ </td><td>Aggregated session-level embedding via mean pooling</td></tr><tr><td> $\mathcal{C}$ </td><td>Set of class labels (18 cryptocurrencies + Noise)</td></tr><tr><td> $\mathcal{D}$ </td><td>Training dataset of sessions and labels</td></tr><tr><td> $M$ </td><td>Number of cryptocurrency classes</td></tr></table>

## B. Cryptocurrency Network Traffic

Cryptocurrency network traffic primarily originates from message propagation between distributed nodes. To maintain global ledger consistency, nodes must broadcast newly generated transactions across the network. This process, driven by distributed ledger technology (DLT) [39], creates bursts of network communication traffic. For instance, in Bitcoin, a new transaction triggers a cascade of message exchanges between validating nodes and their peers, generating structured network sessions that include transaction announcements, verification requests, and confirmation relays, as illustrated in Figure 2.

These interactions are encapsulated within sequences of IP packets, which can be intercepted and parsed to reveal communication patterns and protocol behaviors. Although the general flow logic remains consistent across cryptocurrencies, implementation-level details vary substantially. For example, Bitcoin transmits data in plaintext, while Ethereum uses the RLPx protocol to encrypt all message payloads [15]. This cryptographic heterogeneity—coupled with the diversity of protocol formats and session dynamics—introduces significant challenges for traffic classification systems.

For clarity and ease of reference, Table II summarizes the key mathematical symbols introduced in this section and used throughout the remainder of the paper.

## IV. CRYPTOFORMER: FROM DATASET TO CLASSIFICATION

In this section, we present CryptoFormer, a task-driven, two-stage Transformer framework designed to classify encrypted cryptocurrency traffic under real-world, multi-currency conditions. Fig. 3 provides a schematic overview of the CryptoFormer framework, illustrating the data flow from raw packet capture through tokenization, two-stage Transformer encoding, adaptive fusion, and final classification. We detail each component in the following subsections.

## A. Overview of CryptoFormer

Unlike conventional traffic classifiers, CryptoFormer is developed in response to the unique challenges identified before, including protocol heterogeneity, encryption-induced semantic divergence, multi-currency interference, and the scarcity of cleanly segmented session data. To address these challenges holistically, CryptoFormer integrates both data-centric and model-centric design principles. We begin by detailing our dataset collection and flow construction pipeline, which produces labeled, protocol-agnostic session units suitable for representation learning. We then describe the core components of CryptoFormer: a byte-level tokenization module that enables unified embedding across plaintext and ciphertext; a dual-branch embedding architecture that incorporates both content and behavioral features; a hierarchical Transformer for multi-level feature extraction; and an adaptive gated fusion mechanism to balance semantic and structural signals dynamically. Finally, we explain the classification procedure and optimization strategy, and discuss the framework’s efficiency in deployment scenarios.

Each module in CryptoFormer is tightly aligned with a specific technical challenge, forming a unified solution from data acquisition to model output as shown in Fig. 3.

## B. Data Collection and Flow Construction

To support multi-currency traffic classification under encrypted and heterogeneous network conditions, we construct a labeled cryptocurrency traffic dataset by capturing live communication from actual blockchain nodes. The dataset is designed to reflect real-world deployment settings, capturing protocol diversity, encryption disparity, and interleaved multicurrency flow behaviors.

a) Cryptocurrency Selection: The selection of cryptocurrencies in our dataset follows two principles: market representativeness and protocol diversity. We consulted the CoinMarketCap snapshot from December 2025, which lists the top fifteen assets by market capitalization. From this list we include ten assets: Bitcoin, Ethereum, Tether USDT, USDC, TRON, Dogecoin, Bitcoin Cash, Chainlink, Monero, and Litecoin. Together these ten represent a broad cross-section of the crypto economy, spanning Layer-1 chains, stablecoins, and oracle tokens. In addition, we include several assets outside the top fifteen that hold significant ecosystem roles: WETH and WBTC as the primary wrapped representations of ETH and BTC in decentralized finance, stETH as the leading liquid staking derivative, and PEPE as a representative meme token with high trading volume. We also retain Bitcoin SV to complete the set of major Bitcoin forks. This combination yields a dataset that captures both the economic weight of dominant market participants and the technical diversity of real-world blockchain traffic.

b) Node Deployment and Coverage: We deploy full nodes for eight mainstream cryptocurrencies: BTC, ETH, BCH, BSV, LTC, DOGE, TRON, and XMR. Each node runs the latest official implementation and is connected to the global blockchain network through public IPs to ensure authentic peer-to-peer communication [41]. Additionally, we include background traffic such as DNS, HTTP, and streaming flows, labeled as Noise to simulate open-network environments and test model robustness.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/1920a33fd13acf084c00680141bbfea8ef1284d1b0ce3dcf2c13ddffe245e2f6.jpg)  
Fig. 3. Overall framework of CryptoFormer. Raw packets are segmented into sessions, tokenized via byte-level BPE, and passed through a two-stage Transformer architecture. Stage I extracts packet-level content semantics, Stage II models session-level behavioral dynamics, and an adaptive gated fusion module combines both modalities before final classification.

TABLE III  
TOP 15 CRYPTOCURRENCIES BY MARKET CAPITALIZATION (SNAPSHOT: DECEMBER 28, 2025) [40]

<table><tr><td>Rank</td><td>Name</td><td>Symbol</td><td>Market Cap (USD)</td><td>Price (USD)</td></tr><tr><td>1</td><td>Bitcoin</td><td>BTC</td><td>1,753,953,881,922</td><td>87,835.83</td></tr><tr><td>2</td><td>Ethereum</td><td>ETH</td><td>355,877,262,213</td><td>2,948.57</td></tr><tr><td>3</td><td>Tether USDt</td><td>USDT</td><td>186,688,293,980</td><td>0.9993</td></tr><tr><td>4</td><td>BNB</td><td>BNB</td><td>118,290,532,566</td><td>858.83</td></tr><tr><td>5</td><td>XRP</td><td>XRP</td><td>112,929,746,807</td><td>1.8644</td></tr><tr><td>6</td><td>USDC</td><td>USDC</td><td>76,359,862,909</td><td>0.9998</td></tr><tr><td>7</td><td>Solana</td><td>SOL</td><td>70,459,749,897</td><td>125.20</td></tr><tr><td>8</td><td>TRON</td><td>TRX</td><td>26,979,373,255</td><td>0.2849</td></tr><tr><td>9</td><td>Dogecoin</td><td>DOGE</td><td>20,813,536,578</td><td>0.1238</td></tr><tr><td>10</td><td>Cardano</td><td>ADA</td><td>13,241,227,940</td><td>0.3685</td></tr><tr><td>11</td><td>Bitcoin Cash</td><td>BCH</td><td>12,411,259,641</td><td>621.39</td></tr><tr><td>12</td><td>Chainlink</td><td>LINK</td><td>8,835,112,334</td><td>12.48</td></tr><tr><td>13</td><td>Zcash</td><td>ZEC</td><td>8,726,314,021</td><td>530.16</td></tr><tr><td>14</td><td>Hyperliquid</td><td>HYPE</td><td>8,603,707,638</td><td>25.35</td></tr><tr><td>15</td><td>Monero</td><td>XMR</td><td>8,357,639,383</td><td>453.07</td></tr></table>

c) Traffic Capture and Labeling: Network traffic is collected using passive packet sniffers (e.g., tcpdump) deployed on gateway interfaces [42]. To generate reliable labels, we log node-side transaction records, peer addresses, and session metadata. Each captured flow is aligned with these logs via temporal and connection-level matching, allowing accurate identification of its originating cryptocurrency platform, even in cases where payloads are encrypted or structurally obfuscated [43].

d) Flow Reconstruction and Sub-session Segmentation: Captured traffic is grouped into session flows using 5-tuple identifiers:

$$
(\text { src\_ip }, \text { dst\_ip }, \text { src\_port }, \text { dst\_port }, \text { protocol })
$$

Since blockchain nodes often maintain long-lived connections that span multiple unrelated transactions, we apply a hybrid segmentation strategy [44]:

• A new sub-session is started if the inter-packet interval exceeds 60 seconds.

• Sessions exceeding 10 packets are split into fixed-size sub-sessions.

This ensures semantic coherence within each sub-session, improving the quality of learning signals [45].

e) Preprocessing and Feature Construction: Each subsession is treated as a classification unit. Raw payload bytes are extracted and converted into hexadecimal format for tokenization. Behavioral metadata—including timestamp, inter-arrival delay, TCP flags, window size, and directionality—is extracted from packet headers. Continuous features are normalized via min-max scaling, while categorical flags are one-hot encoded or embedded.

All sequences are padded or truncated to a uniform length to standardize the Transformer input. Padding tokens are masked to prevent their influence on attention computations.

## C. Two-Stage Transformer: Hierarchical Feature Extraction

One of the core technical challenges in cryptocurrency traffic classification arises from multi-currency interference: when nodes concurrently relay traffic for multiple cryptocurrencies, their session flows become structurally entangled and temporally interleaved [46]. These flows often share similar transport-layer properties, making it difficult to disambiguate protocol-specific patterns using shallow or flat models.

To overcome this, CryptoFormer adopts a hierarchical Transformer architecture that explicitly separates local packetlevel semantics from global session-level dynamics. This twostage design enables the model to (1) encode fine-grained semantic and behavioral cues within individual packets, and (2) reason over high-level transaction propagation structures across the session flow.

a) Stage I: Packet-Level Representation: Given an input session $S = \{ p _ { 1 } , p _ { 2 } , . . . , p _ { n } \}$ , each packet $p _ { i }$ is first embedded as a vector $e _ { i }$ representing the tokenized payload contents, as detailed in the previous sections. These vectors form a sequence $E = [ e _ { 1 } , e _ { 2 } , \dots , e _ { n } ]$ which serves as the input to the first Transformer block:

$$
h _ {c o n t e n t _ {i}} = \mathrm{Transformer} _ {1} (e _ {i})
$$

This stage models intra-packet dependencies and local contextual relationships, allowing the model to extract discriminative representations even when payload semantics are partially masked by encryption.

b) Stage II: Flow-Level Representation: In parallel to the content embedding, each packet is associated with a set of behavioral metadata. Discrete features such as direction and TCP flags (SYN, ACK, FIN, RST, PSH, URG) are represented as binary or categorical indicators, while continuous features including inter-arrival interval and window size are normalized to [0, 1] via min-max scaling. These processed features are concatenated into a single vector $\mathbf { f } _ { i } ~ \in ~ \mathbb { R } ^ { d _ { f } }$ , which is then linearly transformed to match the dimension of the content representation:

$$
h _ {b e h a v i o r _ {i}} = \mathbf {W} _ {b} \mathbf {f} _ {i} + \mathbf {b} _ {b} \in \mathbb {R} ^ {d}
$$

where $\mathbf { W } _ { b } \in \mathbb { R } ^ { d \times d _ { f } }$ and $\mathbf { b } _ { b } \in \mathbb { R } ^ { d }$ are learnable parameters. The content representations $h _ { c o n t e n t _ { i } }$ obtained from Stage I are then combined with these behavioral vectors and passed to a second Transformer that aggregates information across the entire session:

$$
h _ {i} = \mathrm{Transformer} _ {2} (F u s i o n (h _ {c o n t e n t _ {i}}, h _ {b e h a v i o r _ {i}}))
$$

This stage captures global transaction flow characteristics, such as propagation timing, packet interaction patterns, and session-specific behaviors unique to each cryptocurrency protocol. By treating the session as a coherent communication unit, this stage enables the model to recognize abstract propagation signatures that cannot be inferred from isolated packets alone.

This two-stage formulation is explicitly aligned with the structural hierarchy of blockchain network communication. Packet-level modeling addresses encryption-induced information loss by maximizing local semantic extraction, while session-level modeling counters cross-currency interference by integrating flow-wide behavior. Importantly, this structure allows the model to decouple visually similar flows (e.g., BTC vs BCH) based on protocol-specific inter-packet dependencies, which are often ignored by single-stage or flat architectures [47].

Empirically, we find that this decomposition significantly improves model robustness under mixed traffic scenarios, especially when cryptocurrencies share similar transport-layer characteristics but differ subtly in message structure or timing patterns.

## D. Adaptive Gated Fusion: Balancing Semantic and Behavioral Cues under Encryption

A critical obstacle in encrypted cryptocurrency traffic classification is the potential semantic degradation caused by ciphertext payloads. In protocols such as Ethereum’s RLPx [15], payload content is fully encrypted, rendering conventional semantic token features weak or uninformative. Relying solely on content embeddings in such settings may lead to high variance or misclassification.

To address this, we design an adaptive gated fusion module that dynamically balances content-derived semantics with behavior-derived structural features. This mechanism enables CryptoFormer to selectively emphasize packet behavior when content is encrypted or sparse and to prioritize content embeddings when payload information is available and meaningful.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/87fb84dbd94ee1c69e3c214ea17fdcbe9a61a9fba091384c93634ce091ba96f0.jpg)  
Fig. 4. Adaptive gated fusion module. Content and behavioral embeddings are linearly projected, and their difference and Hadamard product are concatenated to compute a gating coefficient α. The final fused representation is $\alpha \cdot \tilde { h } _ { \mathrm { c o n t e n t } } + ( 1 - \alpha ) \cdot \tilde { h } _ { \mathrm { b e h a v i o r } } ,$ enabling dynamic weighting based on payload informativeness.

a) Fusion Formulation: Given packet-level representations from Stage I, let $h _ { \mathrm { { c o n t e n t } } } \in \mathbb { R } ^ { d }$ and $h _ { \mathrm { b e h a v i o r } } \in \mathbb { R } ^ { d }$ denote the semantic and behavioral embeddings for a single packet. We first apply learnable linear projections:

$$
\tilde {h} _ {\mathrm{content}} = W _ {c} h _ {\mathrm{content}} + b _ {c}, \quad \tilde {h} _ {\mathrm{behavior}} = W _ {b} h _ {\mathrm{behavior}} + b _ {b}
$$

To capture the interaction between modalities, we compute two auxiliary representations:

$$
h _ {\mathrm{diff}} = \tilde {h} _ {\mathrm{content}} - \tilde {h} _ {\mathrm{behavior}}, \quad h _ {\mathrm{dot}} = \tilde {h} _ {\mathrm{content}} \odot \tilde {h} _ {\mathrm{behavior}}
$$

We concatenate the transformed vectors and pass them through a sigmoid-activated gating function:

$$
\alpha = \sigma \left(W _ {g} \cdot [ \tilde {h} _ {\text { content }}; \tilde {h} _ {\text { behavior }}; h _ {\text { diff }}; h _ {\text { dot }} ] + b _ {g}\right)
$$

The final fused embedding is computed as:

$$
h _ {\mathrm{fusion}} = \alpha \cdot \tilde {h} _ {\mathrm{content}} + (1 - \alpha) \cdot \tilde {h} _ {\mathrm{behavior}}
$$

adaptively combines content and behavioral features, as illustrated in Fig. 4.

This formulation enables dynamic feature selection at the packet level. When encrypted traffic limits the expressiveness of content tokens, the gate suppresses $h _ { \mathrm { { c o n t e n t } } }$ and shifts weight to behavioral cues (e.g., inter-packet timing, SYN/ACK patterns). Conversely, when plaintext protocols like Bitcoin expose rich transaction metadata, the model leverages content semantics as the primary signal.

Unlike static feature fusion strategies, this adaptive gating enhances model flexibility across protocol types, traffic conditions, and flow semantics. It is particularly effective in realworld mixed environments, where packets in the same session may exhibit heterogeneous levels of content informativeness.

Although prior works [48], [49] have explored static feature fusion in traffic analysis. CryptoFormer is the first to implement dynamic, learnable gating over encrypted cryptocurrency flows at fine-grained packet resolution. This innovation directly improves robustness to semantic obfuscation and aligns with the end goal of encryption-agnostic traffic classification.

## E. Session Classification and Optimization

The final goal of CryptoFormer is to assign a sessionlevel label to each input flow, identifying the most likely originating cryptocurrency protocol. Given that each session $\boldsymbol { S } = \{ p _ { 1 } , p _ { 2 } , . . . , p _ { n } \}$ may contain dozens of packets with varying degrees of semantic and behavioral informativeness, the model must effectively aggregate these per-packet representations into a coherent session-level embedding.

a) Flow Representation Aggregation: After the two-stage Transformer encodes each packet and the gated fusion module produces refined per-packet embeddings $\{ h _ { 1 } , h _ { 2 } , \ldots , h _ { n } \}$ , we apply average pooling to form a fixed-length representation for the entire session:

$$
h _ {\text { session }} = \frac {1}{n} \sum_ {i = 1} ^ {n} h _ {i}
$$

This approach preserves the influence of all packets in the session, ensuring robustness across sessions of variable length. Compared to using only the representation of the final packet or a learned aggregation embedding such as the [CLS] token (a special classification token commonly prepended to sequences in BERT-style architectures to aggregate global sequence information) [19], average pooling better reflects the cumulative flow behavior, especially under encryption or mixed-quality packets.

b) Classification Layer: The pooled session representation is passed through a lightweight classification head comprising two fully connected layers and a softmax output:

$$
p (y \mid h _ {\text { session }}) = \operatorname{Softmax} \left(W _ {2} \cdot \tanh (W _ {1} h _ {\text { session }} + b _ {1}) + b _ {2}\right)
$$

where $W _ { 1 } , W _ { 2 }$ and $b _ { 1 } , b _ { 2 }$ are learnable parameters, and $p ( y \mid$ $h _ { \mathrm { s e s s i o n } } ) \ \in \ \mathbb { R } ^ { | \mathcal { C } | }$ is the predicted class distribution over the cryptocurrency set C.

c) Training Objective: CryptoFormer is trained in a supervised manner using multi-class cross-entropy loss. Given a one-hot ground truth label vector $y \in \{ 0 , \bar { 1 } \bar  \} ^ { | \mathcal { C } | }$ , the loss function is:

$$
\mathcal {L} = - \sum_ {c = 1} ^ {| \mathcal {C} |} y _ {c} \log p (y _ {c} \mid h _ {\text { session }})
$$

This objective encourages the model to assign high confidence to the correct class and penalizes ambiguous or incorrect predictions proportionally to their confidence.

d) Optimization and Regularization: We optimize the model using the Adam optimizer with layer normalization and dropout applied to all linear layers. Label smoothing is optionally applied to mitigate overconfidence and improve generalization in the presence of noisy or borderline flows. Training is conducted with early stopping on the validation set to prevent overfitting.

This classification strategy reflects our overarching goal: to achieve high discriminability across multiple cryptocurrencies without relying on protocol-specific assumptions or decrypted payloads. By aggregating rich token and behavioral embeddings, CryptoFormer captures both local structure and global flow intent, enabling accurate inference even under heavy encryption or cross-currency interference.

## F. Efficiency Consideration

In addition to achieving high classification accuracy, Crypto-Former is designed with deployment efficiency as a key objective. Real-world blockchain monitoring systems often require high-throughput packet processing, low-latency inference, and hardware-constrained deployment at edge gateways or compliance monitors. These constraints impose practical limits on model size, inference complexity, and preprocessing cost.

a) Lightweight Architecture: CryptoFormer uses shallow Transformer stacks in both stages, with reduced hidden dimensions and limited attention heads compared to large-scale language models (e.g., ET-BERT [20], TrafficBERT [33]). This design significantly reduces both the parameter count and forward-pass latency. We further eliminate computationally expensive mechanisms such as masked language modeling or next-token prediction, focusing solely on flow-level classification.

b) Tokenizer Simplification: Unlike prior methods that rely on complex deep packet inspection or full protocol parsing, our byte-level Byte Pair Encoding (BPE) operates directly on raw hexadecimal payloads. This allows fast, stateless tokenization that is agnostic to encryption schemes and does not require decryption or pre-parsed fields. The embedding layer is fully shared across protocols, reducing memory footprint and preprocessing latency.

c) Parallelism and Batching: CryptoFormer supports batching and parallel inference across multiple session flows. Since session boundaries are predefined during preprocessing, input sequences can be processed independently and in parallel, leveraging modern hardware accelerators such as GPUs or TPUs.

d) Deployment-Readiness: To validate practical deployability, we evaluate CryptoFormer’s real-time throughput and latency. Empirical results show that it achieves inference speeds up to 2.96× faster than ET-BERT while maintaining comparable or superior accuracy. The model’s compact footprint and protocol-agnostic input make it suitable for integration into existing security appliances, on-premise analysis tools, and lightweight regulatory endpoints.

## V. EVALUATION

We conduct extensive experiments to evaluate the effectiveness of CryptoFormer in classifying encrypted cryptocurrency traffic.

## A. Dataset

Our evaluation is conducted on a custom-constructed, realworld cryptocurrency traffic dataset, which serves as the foundation for training and benchmarking CryptoFormer. The dataset is collected under production-like network environments and reflects diverse protocol characteristics, encryption settings, and communication behaviors.

We include eight widely-used cryptocurrencies: Bitcoin (BTC), Ethereum (ETH), Bitcoin Cash (BCH), Bitcoin SV (BSV), Litecoin (LTC), Dogecoin (DOGE), TRON (TRX), and Monero (XMR), covering both plaintext (e.g., BTC, LTC) and encrypted (e.g., ETH, XMR) protocols. In addition, we incorporate ten prominent tokens and stablecoins to broaden the asset coverage: Tether USDt (USDT), USD Coin (USDC), PEPE, Chainlink (LINK), Wrapped Ether (WETH), Wrapped Bitcoin (WBTC), Lido Staked Ether (stETH), Uniswap (UNI), Toncoin (TONCOIN), and BNB. These span stablecoins, meme tokens, oracle tokens, wrapped assets, liquid staking derivatives, DEX governance tokens, and alternative Layer-1 tokens. Additionally, we incorporate background noise traffic (e.g., DNS, HTTP, streaming) to simulate open-network deployment conditions and assess the model’s resilience against non-cryptocurrency data.

All traffic is captured using passive probes colocated with full blockchain nodes. Session labels are generated through synchronized node logs, allowing accurate mapping between flows and their originating platforms. Each session is reassembled via 5-tuple segmentation and split into sub-sessions based on inter-packet interval and flow length to ensure semantic consistency.

The resulting dataset comprises over 188K labeled session flows with significant variability in flow size, duration, and protocol entropy. Table IV summarizes the statistics and Fig. 5 shows the session flow distribution by platform. Notably, ETH and XMR account for a larger number of flows and file sizes, consistent with their higher transaction volumes and protocol verbosity. Among the additional tokens, USDT and USDC contribute substantial traffic volumes in line with their dominant market positions, while the remaining tokens exhibit moderate but meaningful flow counts. This diversity introduces realistic traffic imbalance and enriches the classification challenge.

This dataset is particularly well-suited for evaluating the multi-currency traffic classification task due to several critical characteristics. First, it spans a broad range of protocol implementations, including plaintext-based protocols such as JSON-RPC (e.g., Bitcoin) and encrypted protocols like Ethereum’s RLPx and Monero’s stealth mechanisms, thus providing a rigorous benchmark for encryption-agnostic representation learning. Second, the session flows exhibit substantial diversity in terms of length, inter-arrival timing, and directionality, closely mirroring real-world P2P communication behaviors. Third, each flow is labeled through synchronized node logs, ensuring precise ground-truth annotations even when payload contents are encrypted or obscured. Lastly, the inclusion of noise traffic—comprising standard internet activities such as web browsing and streaming—enables robust evaluation of false positive resilience in open network environments. These properties collectively ensure that our dataset provides a comprehensive and realistic testbed for deep encrypted traffic classifiers.

TABLE IV  
STATISTICS OF BLOCKCHAIN CRYPTOCURRENCIES TRAFFIC DATA

<table><tr><td>Cryptocurrencies</td><td>Traffic Flows</td><td>Size (MB)</td></tr><tr><td>BTC</td><td>7,413</td><td>785.0</td></tr><tr><td>ETH</td><td>31,978</td><td>852.0</td></tr><tr><td>BCH</td><td>15,156</td><td>147.0</td></tr><tr><td>BSV</td><td>12,210</td><td>45.8</td></tr><tr><td>LTC</td><td>10,283</td><td>66.7</td></tr><tr><td>DOGE</td><td>8,462</td><td>113.0</td></tr><tr><td>TRON</td><td>13,532</td><td>640.0</td></tr><tr><td>XMR</td><td>45,194</td><td>475.0</td></tr><tr><td>USDT</td><td>13,165</td><td>312.4</td></tr><tr><td>USDC</td><td>8,512</td><td>168.9</td></tr><tr><td>PEPE</td><td>2,843</td><td>48.2</td></tr><tr><td>LINK</td><td>2,187</td><td>53.6</td></tr><tr><td>WETH</td><td>2,094</td><td>38.7</td></tr><tr><td>WBTC</td><td>1,607</td><td>42.3</td></tr><tr><td>stETH</td><td>1,452</td><td>27.5</td></tr><tr><td>UNI</td><td>1,338</td><td>35.8</td></tr><tr><td>TONCOIN</td><td>1,086</td><td>19.2</td></tr><tr><td>BNB</td><td>1,047</td><td>24.1</td></tr><tr><td>Noise</td><td>9,130</td><td>218.0</td></tr><tr><td>Total</td><td>188,689</td><td>4113.2</td></tr></table>

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/5bb9f69a54e94b3f9490347c247b4fb9b4c8b1bf86da2aba96bcf620ae184aa8.jpg)  
Fig. 5. Distribution of session flows across the eighteen cryptocurrency assets and background noise in the collected dataset. ETH and XMR account for the largest shares, consistent with their high transaction volumes, while USDT and USDC also contribute substantial traffic.

## B. Baselines

We compare CryptoFormer with several representative traffic classification models:

• Appscanner [21]: A Random Forest model using 54 handcrafted statistical features (e.g., packet lengths, timings).

• Deep Fingerprinting (Deep FP) [31]: A CNN-based attack traffic classification in closed-world settings.

• FS-Net [30]: A bidirectional GRU-based model with reconstruction mechanism for encrypted traffic classification.

• Deeppacket [36]: A CNN-based approach using raw packet payloads to classify encrypted traffic and VPN/non-VPN flows.

• PerFormer [37]: A Transformer-based model efficiently approximating full-rank softmax attention, enabling scalability across large-scale tasks.

TABLE V  
MODEL PERFORMANCE COMPARISON (%)

<table><tr><td>Model</td><td>Accuracy</td><td>Precision</td><td>Recall</td><td>F1</td><td>AUC</td></tr><tr><td colspan="6">Statistical Methods</td></tr><tr><td>Appscanner</td><td>58.47</td><td>59.82</td><td>58.11</td><td>58.95</td><td>57.23</td></tr><tr><td>DeepFP</td><td>68.25</td><td>64.73</td><td>69.28</td><td>66.93</td><td>65.94</td></tr><tr><td colspan="6">Convolutional Methods</td></tr><tr><td>FS-Net</td><td>65.38</td><td>66.12</td><td>70.43</td><td>68.21</td><td>68.79</td></tr><tr><td>Deep Packet</td><td>89.64</td><td>87.91</td><td>86.55</td><td>87.22</td><td>87.43</td></tr><tr><td colspan="6">Transformer-based Methods</td></tr><tr><td>PerFormer</td><td>83.22</td><td>83.76</td><td>82.59</td><td>83.17</td><td>83.50</td></tr><tr><td>LongFormer</td><td>84.39</td><td>85.02</td><td>84.73</td><td>84.87</td><td>85.04</td></tr><tr><td colspan="6">Pre-trained Methods</td></tr><tr><td>TrafficFormer</td><td>93.15</td><td>93.28</td><td>93.04</td><td>93.16</td><td>90.62</td></tr><tr><td>ET-BERT</td><td>93.87</td><td>93.94</td><td>93.55</td><td>93.74</td><td>91.28</td></tr><tr><td colspan="6">Ours</td></tr><tr><td>CryptoFormer</td><td>95.12</td><td>95.18</td><td>94.87</td><td>95.02</td><td>93.46</td></tr></table>

• LongFormer [38]: A Transformer-based model combining local windowed and global attention, enabling efficient processing of long sequences.

• TrafficFormer [33]: A variant of BERT enhanced with packet order prediction as a pretraining task.

• ET-BERT [20]: A BERT-style pretraining model with masked BURST reconstruction and same-origin BURST prediction.

## C. Evaluation Metrics

We treat traffic classification as a multi-class problem and report macro-averaged metrics across all categories: Accuracy, Precision, Recall, and F1-score. Each metric is computed per class and averaged equally [50] to reflect overall performance regardless of class imbalance.

## D. Implementation Settings

All models are implemented using PyTorch. Experiments are conducted on a Tesla V100 GPU with 16GB of memory under Ubuntu 18.04. We use the AdamW optimizer with a learning rate of 2e-5 and weight decay of 0.01. The batch size is set to 8, and early stopping is applied if validation loss does not improve within 3 consecutive epochs.

Each session is standardized by extracting the first 10 packets, with each packet truncated to 32 bytes, ensuring uniform input length across models.

## E. Performance Comparison

We evaluate CryptoFormer against a comprehensive set of baselines, including statistical methods, convolutional neural networks, Transformer-based architectures, and pretrained models, as summarized in Table V. CryptoFormer achieves the best overall results, with an Accuracy of 95.12% and a macro F1-score of 95.02%, demonstrating superior capability in classifying encrypted, multi-currency cryptocurrency traffic.

Statistical methods such as Appscanner and Deep FP exhibit relatively low performance, with F1-scores of 58.95% and 66.93%, respectively. These models depend heavily on handcrafted statistical features that inadequately capture the complex temporal and protocol-specific dynamics of blockchain traffic, especially under encryption and protocol heterogeneity.

Convolutional models, including FS-Net and Deep Packet, improve upon statistical approaches by learning local spatial features from raw packet data or reconstructed flows. Nevertheless, FS-Net’s F1-score 68,21% remains modest, and while Deep Packet attains a higher F1 of 87.22%, their reliance on local features limits their ability to model longrange dependencies and session-level behaviors critical for discriminating currencies with similar payload distributions.

Transformer-based methods such as PerFormer and Long-Former leverage attention mechanisms for efficient sequence modeling. PerFormer and LongFormer achieve moderate accuracy (83.22% and 84.39%) but lack specialized designs for encrypted multi-currency scenarios, leading to suboptimal classification under payload obfuscation and flow sparsity.

Pretrained models, TrafficFormer and ET-BERT, achieve strong performance by utilizing large-scale pretraining with tasks such as packet order prediction and masked token reconstruction. They attain F1-scores of 93.16% and 93.74%, respectively, benefiting from deep Transformer stacks and extensive traffic corpora. However, these models generally treat the traffic as homogeneous sequences, without explicitly disentangling semantic and behavioral features.

In contrast, CryptoFormer attains the highest accuracy and F1-score (95.02%) without requiring any pretraining. Its twostage architecture separately models packet-level content and session-level behavioral patterns, while the adaptive gated fusion dynamically balances these heterogeneous signals based on packet informativeness. This design effectively addresses challenges posed by protocol diversity and encryption.

Notably, CryptoFormer’s performance gain over ET-BERT (1.28% F1) is achieved with a much shallower model—only two Transformer layers—and a significantly smaller training dataset, highlighting its training efficiency and lower computational demand. This efficiency positions CryptoFormer as a practical choice for real-time and resource-constrained deployment in regulatory and forensic environments.

Overall, the extensive comparisons demonstrate Crypto-Former’s effectiveness and efficiency in multi-currency cryptocurrency traffic classification, making it well-suited for deployment scenarios requiring accuracy, interpretability, and computational practicality.

## F. Confusion Matrix Analysis

To gain deeper insight into CryptoFormer’s discriminative behavior, we visualize the per-class classification results using a normalized confusion matrix, as shown in Fig. 6. Each row represents the ground-truth class distribution, while columns indicate predicted classes. The strong diagonal dominance confirms CryptoFormer’s ability to distinguish between different cryptocurrencies with high precision.

All eight cryptocurrency classes, as well as the noise class, achieve F1-scores exceeding 96%, with several categories approaching near-perfect accuracy. Notably, CryptoFormer achieves 99.9% on TRON and 99.8% on Monero—two currencies with distinct propagation characteristics—demonstrating its capability to capture unique session-level patterns even under encryption. These high-precision results suggest that CryptoFormer’s behavioral embedding and flow-level modeling are effective in recognizing protocol-specific state transitions and propagation dynamics.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/8d56d4715acb605c2bd50617913d0dbdf482732af4ce9fe2a343e1dba791b421.jpg)  
Fig. 6. Normalized confusion matrix of CryptoFormer on the original eight cryptocurrencies plus noise. Rows correspond to true labels and columns to predictions. Strong diagonal dominance indicates high discriminability, with only minor confusion among Bitcoin-derived forks (BCH/BSV/LTC) due to shared protocol stacks.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/d4ec5cb2bf5b07b6a1af42f91f158b35a9d1cfe47ae5b34aafe893370d960cd0.jpg)  
Fig. 7. Normalized confusion matrix of CryptoFormer on the ten additional tokens. Stablecoins (USDT, USDC) are well separated, while Ethereum-native tokens (WETH, WBTC, stETH) exhibit moderate intra-ecosystem confusion. TONCOIN and BNB show bidirectional misclassification due to similar independent P2P gossip protocols.

However, some confusion is observed among structurally similar currencies derived from the Bitcoin protocol family, particularly between BCH, BSV, and LTC. These protocols share large portions of their communication stack (e.g., message formats, transaction broadcasting behavior), which leads to overlapping flow characteristics. CryptoFormer occasionally misclassifies BCH as BSV (and vice versa), with a combined total of 23 misclassifications. This is expected given the limited protocol divergence and shared client codebase among these Bitcoin forks.

Ethereum (ETH) also exhibits a small number of misclassifications (12 instances), primarily due to the variability introduced by its RLPx-based encryption layer and transaction relay behaviors. Despite this, CryptoFormer maintains an F1- score of 98.3% on ETH, outperforming all baselines by a notable margin. This underscores the model’s capacity to extract encryption-invariant representations through adaptive fusion of payload and behavioral information.

Importantly, CryptoFormer demonstrates strong resilience to background noise. Among over 9,000 noise samples—comprising HTTP, DNS, video streaming, and unrelated TLS handshakes—only 9 were incorrectly classified as cryptocurrency traffic. This low false positive rate (0.1%) reflects the model’s ability to isolate structural patterns that are truly characteristic of blockchain P2P networks, rather than overfitting to superficial traffic statistics.

We further examine CryptoFormer’s performance on the ten additional tokens using a separate confusion matrix, as shown in Fig. 7. These tokens include stablecoins (USDT, USDC), meme tokens (PEPE), oracle tokens (LINK), wrapped assets (WETH, WBTC), a liquid staking derivative (stETH), a DEX governance token (UNI), and two independent Layer-1 tokens (TONCOIN, BNB).

CryptoFormer achieves strong discriminability on the two dominant stablecoins, with USDT and USDC attaining diagonal accuracies of 93.6% and 95.2%, respectively. The minimal cross-confusion between them (only 15 and 18 samples) indicates that despite their functional similarity, the model captures subtle behavioral differences in their transaction patterns. Among Ethereum-ecosystem tokens, LINK exhibits the highest diagonal accuracy (96.4%), reflecting its distinctive oracle update traffic. In contrast, wrapped assets WETH and WBTC, along with stETH, show moderate confusion with one another (e.g., 4.4% of WBTC samples misclassified as WETH, and 3.6% of WETH as stETH). This is expected, as these tokens share the same underlying P2P network and differ primarily in higher-layer contract interactions, which are less visible at the transport layer.

The two Layer-1 tokens, TONCOIN and BNB, present an interesting case. TONCOIN achieves a diagonal accuracy of 77.2%, with a notable fraction (13.6%) misclassified as BNB. Conversely, BNB attains 82.4% accuracy, with 8.8% confusion toward TONCOIN. This bidirectional confusion likely stems from similarities in their independent P2P gossip protocols and comparable transaction propagation behaviors.

Overall, the confusion matrix analysis reveals a clear correlation between protocol similarity and classification difficulty. Currencies sharing the same wire protocol family exhibit modest confusion: within the Bitcoin-derived forks (BCH, BSV, LTC), misclassification rates range from 1% to 3%, while among Ethereum-native tokens (WETH, WBTC, stETH), cross-confusion remains moderate due to their shared underlying P2P network. In contrast, assets with fundamentally distinct protocol architectures, such as TRON, XMR, and the two stablecoins USDT and USDC, are separated with near-perfect accuracy. Across the ten additional tokens, CryptoFormer maintains an average diagonal accuracy above 85%, demonstrating robust generalization beyond the original eight cryptocurrencies. These observations confirm that CryptoFormer’s hierarchical feature extraction and adaptive fusion effectively capture both fine-grained content semantics and coarse behavioral dynamics, and that its performance degrades gracefully along the expected continuum of protocol overlap rather than being biased toward any specific currency group.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/de78501b3f80fa5885066ce940d12a4c903715a3e72f5e1b49e8f10f6119317c.jpg)  
Fig. 8. Ablation study results on the full eighteen-asset dataset, reporting both Accuracy and F1-score. Removing payload content (w/o P) causes the most severe degradation, confirming that semantic features are the dominant factor. Behavioral features (w/o B) and directional encoding (w/o D) provide complementary benefits, while adaptive gated fusion outperforms static addition and concatenation.

## G. Ablation Study

To comprehensively evaluate the individual contribution of each design component in CryptoFormer, we conduct a series of ablation experiments by systematically removing or replacing key elements of our model. The variants tested are summarized as follows:

• w/o P (Content): The payload feature extractor is removed, thereby excluding semantic content information from the model input.

• w/o B (Behavioral): Behavioral metadata features, which capture traffic patterns and temporal characteristics, are excluded.

• w/o D (Directional): The directional encoding mechanism, designed to incorporate packet flow directionality, is disabled.

• w/ A (Additive): The gated fusion module is replaced with a simple element-wise addition to combine features.

• w/ C (Concat): The gated fusion is substituted by a straightforward concatenation of features before subsequent processing.

The ablation results, illustrated in Fig. 8, are obtained on the full dataset of eighteen cryptocurrency assets described in Section V-A, ensuring that the findings generalize beyond the original eight currencies. The results reveal a clear hierarchy of component importance. Excluding payload content (w/o P) causes the most severe degradation, with Accuracy falling to 68.38% and F1-score to 68.87%. This drop is particularly pronounced for encrypted protocols and Ethereum-based tokens, where content features are already partially obscured, further confirming that semantic information from packet payloads is the dominant factor for classification. Removing behavioral features (w/o B) reduces Accuracy to 92.31% and F1-score to 92.56%, corresponding to declines of 2.81 and 2.46 percentage points respectively. The impact of this ablation is most evident on assets with sparse payload content or high encryption overhead, where the model must rely more heavily on traffic dynamics. Disabling directional encoding (w/o D) yields a smaller but consistent decline (Accuracy 93.47%, F1-score 93.67%), indicating that explicit direction modeling provides a modest yet beneficial signal, especially for interactive protocols with distinct request-response patterns such as TRON and the Bitcoin family.

We also evaluate alternative fusion strategies on the expanded dataset. The proposed gated mechanism outperforms both element-wise addition (Additive: Accuracy 92.82%, F1- score 92.78%) and feature concatenation (Concat: Accuracy 94.16%, F1-score 94.31%). Notably, the gap between static and adaptive fusion widens when evaluating the additional tokens, where the informativeness of payload content varies substantially across stablecoins, wrapped assets, and independent Layer-1 tokens. This observation reinforces that dynamically weighting content and behavior based on packet-level observability is more effective than fixed combinations.

In summary, the ablation study validates the design of CryptoFormer on the expanded eighteen-asset dataset and establishes the relative importance of its components: payload semantics contributes most significantly, followed by behavioral features and directional encoding, while adaptive gated fusion provides a consistent improvement over static alternatives, particularly in heterogeneous multi-currency scenarios.

## H. Computational Efficiency

Beyond classification accuracy, practical deployment in regulatory and edge-monitoring environments imposes strict constraints on computational resources and response time. We therefore evaluate the training and inference efficiency of CryptoFormer against all baseline models under identical hardware conditions using a single NVIDIA Tesla V100 GPU.

Fig. 9 reports the total wall-clock training time on the full dataset. Among Transformer-based models, ET-BERT and TrafficFormer incur the highest training costs (887s and 753s, respectively) due to their deep-layer architectures and large pretraining corpora. PerFormer and LongFormer, despite their efficient attention approximations, still require approximately 590 s to converge. In contrast, CryptoFormer completes training in only 335s, achieving a 2.65× reduction over ET-BERT and outperforming even lightweight CNN-based methods such as DeepPacket (355s) and FS-Net (377s). This efficiency stems from the absence of costly pretraining phases and the use of shallow two-layer Transformers in both processing stages, which dramatically reduce the number of gradient updates and memory accesses.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/d1c0dc3f4dbd426433c61493bf0d46eaebea862fc5dcfebc13b569f35b28aa70.jpg)  
Fig. 9. Training time comparison on the full dataset. CryptoFormer completes training in 335 s, achieving a 2.65× reduction over ET-BERT (887 s) and outperforming even lightweight CNN-based methods. The efficiency gain stems from shallow two-layer Transformers and the absence of costly pretraining phases.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/6526ecaf14ec75017ea1058096ae8f7a431ac11707e1c562c3b5470194bbf5e5.jpg)  
Fig. 10. Inference latency comparison on the test set. CryptoFormer attains the lowest latency (1.15 s/session), a 2.97× speedup over ET-BERT (3.41 s/session) and a 2.58× speedup over TrafficFormer (2.97 s/session). The lightweight tokenization and hierarchical architecture amortize computational cost across packets.

Fig. 10 presents the average per-session inference latency measured on the test set. CryptoFormer attains the lowest latency (1.15 s/session), representing a 2.97× speedup over ET-BERT (3.41 s/session) and a 2.58× speedup over TrafficFormer (2.97 s/session). Notably, CryptoFormer also outperforms CNN and RNN baselines, which are generally considered lightweight. The latency advantage is attributed to two design choices. First, the byte-level BPE tokenization operates directly on raw payloads without deep protocol parsing, eliminating feature engineering overhead. Second, the hierarchical two-stage architecture processes packet content and session behavior separately, allowing the heavier packetlevel encoding to be reused across packets within the same session, thereby amortizing the computational cost.

Taken together, these results demonstrate that CryptoFormer delivers state-of-the-art accuracy without sacrificing efficiency. Its compact parameter footprint and fast inference make it well-suited for deployment on resource-constrained gateways, compliance monitoring appliances, and real-time forensic analysis systems.

## VI. CONCLUSION

This work presents CryptoFormer, a task-driven Transformer framework for encrypted cryptocurrency traffic classification under real-world multi-currency conditions. By combining packet-level semantic extraction and session-level behavioral modeling in a two-stage architecture, Crypto-Former effectively captures the heterogeneous characteristics of blockchain protocols. The proposed adaptive gated fusion mechanism further enhances robustness by dynamically balancing content and behavioral cues, especially under encryption. Extensive experiments on a diverse, real-world dataset demonstrate that CryptoFormer achieves high accuracy with low computational overhead, making it suitable for regulatory and edge deployment scenarios. Future research will explore model adaptation to emerging protocols and integration with real-time blockchain forensics pipelines.

## ACKNOWLEDGMENTS

This work is supported by the National Key Research and Development Program of China under the grant No.2023YFB2704702.

We are grateful to anonymous reviewers for their fruitful comments, corrections, and inspiration to improve this paper.

## REFERENCES

[1] R. Bohme, N. Christin, B. Edelman, and T. Moore, “Bitcoin: Economics,¨ technology, and governance,” Journal of economic Perspectives, vol. 29, no. 2, pp. 213–238, 2015.

[2] CoinGecko, “The coingecko 2025 annual crypto industry report,” https: //www.coingecko.com/research/publications/2025-annual-crypto-report, 2026.

[3] R. Schollmeier, “A definition of peer-to-peer networking for the classification of peer-to-peer architectures and applications,” in Proceedings first international conference on peer-to-peer computing. IEEE, 2001, pp. 101–102.

[4] E. Fletcher, C. Larkin, and S. Corbet, “Countering money laundering and terrorist financing: A case for bitcoin regulation,” Research in International Business and Finance, vol. 56, p. 101387, 2021.

[5] K. G. Al-Hashedi and P. Magalingam, “Financial fraud detection applying data mining techniques: A comprehensive review from 2009 to 2019,” Computer Science Review, vol. 40, p. 100402, 2021.

[6] Y. Elmougy and L. Liu, “Demystifying fraudulent transactions and illicit nodes in the bitcoin network for financial forensics,” in Proceedings of the 29th ACM SIGKDD conference on knowledge discovery and data mining, 2023, pp. 3979–3990.

[7] F. Alvarez, D. Argente, and D. Van Patten, “Are cryptocurrencies currencies? bitcoin as legal tender in el salvador,” Science, vol. 382, no. 6677, p. eadd2844, 2023.

[8] Y. Qi, J. Wu, H. Xu, and M. Guizani, “Blockchain data mining with graph learning: A survey,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 46, no. 2, pp. 729–748, 2023.

[9] Z. Guo, X. Li, J. Liu, Z. Zhang, M. Li, J. Hu, and L. Zhu, “Graphbased covert transaction detection and protection in blockchain,” IEEE Transactions on Information Forensics and Security, vol. 19, pp. 2244– 2257, 2023.

[10] B. Luo, Z. Zhang, Q. Wang, and B. He, “Multi-chain graphs of graphs: A new approach to analyzing blockchain datasets,” Advances in Neural Information Processing Systems, vol. 37, pp. 28 490–28 514, 2024.

[11] L. Lao, Z. Li, S. Hou, B. Xiao, S. Guo, and Y. Yang, “A survey of iot applications in blockchain systems: Architecture, consensus, and traffic modeling,” ACM Computing Surveys (CSUR), vol. 53, no. 1, pp. 1–32, 2020.

[12] H. Qi, J. Wang, W. Li, Y. Wang, and T. Qiu, “A blockchain-driven iiot traffic classification service for edge computing,” IEEE Internet of Things Journal, vol. 8, no. 4, pp. 2124–2134, 2020.

[13] S. Nakamoto, “Bitcoin: A peer-to-peer electronic cash system,” 2008.

[14] K. Ko, C. Lee, T. Jeong, and J. W.-K. Hong, “Design of rpc-based blockchain monitoring agent,” in 2018 International Conference on Information and Communication Technology Convergence (ICTC). IEEE, 2018, pp. 1090–1095.

[15] X. Chen, K. Nguyen, and H. Sekiya, “On the latency performance in private blockchain networks,” IEEE Internet of Things Journal, vol. 9, no. 19, pp. 19 246–19 259, 2022.

[16] Y. Li, G. Yang, W. Susilo, Y. Yu, M. H. Au, and D. Liu, “Traceable monero: Anonymous cryptocurrency with enhanced accountability,” IEEE Transactions on Dependable and Secure Computing, vol. 18, no. 2, pp. 679–691, 2019.

[17] J. Kim, M. Nakashima, W. Fan, S. Wuthier, X. Zhou, I. Kim, and S.-Y. Chang, “A machine learning approach to anomaly detection based on traffic monitoring for secure blockchain networking,” IEEE Transactions on Network and Service Management, vol. 19, no. 3, pp. 3619–3632, 2022.

[18] S. Dong, “Multi class svm algorithm with active learning for network traffic classification,” Expert Systems with Applications, vol. 176, p. 114885, 2021.

[19] J. Devlin, “Bert: Pre-training of deep bidirectional transformers for language understanding,” arXiv preprint arXiv:1810.04805, 2018.

[20] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in Proceedings of the ACM Web Conference 2022, 2022, pp. 633–642.

[21] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “Appscanner: Automatic fingerprinting of smartphone apps from encrypted network traffic,” in 2016 IEEE European Symposium on Security and Privacy (EuroS&P). IEEE, 2016, pp. 439–454.

[22] R. Zhao, M. Zhan, X. Deng, Y. Wang, Y. Wang, G. Gui, and Z. Xue, “Yet another traffic classifier: A masked autoencoder based traffic transformer with multi-level flow representation,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 37, no. 4, 2023, pp. 5420–5427.

[23] A. Biryukov and I. Pustogarov, “Bitcoin over tor isn’t a good idea,” in 2015 IEEE Symposium on Security and Privacy. IEEE, 2015, pp. 122–134.

[24] R. De Silva, W. Guo, N. Ruaro, I. Grishchenko, C. Kruegel, and G. Vigna, “{GuideEnricher}: Protecting the anonymity of ethereum mixing service users with deep reinforcement learning,” in 33rd USENIX Security Symposium (USENIX Security 24), 2024, pp. 3549–3566.

[25] J. Kim, M. Nakashima, W. Fan, S. Wuthier, X. Zhou, I. Kim, and S.- Y. Chang, “Anomaly detection based on traffic monitoring for secure blockchain networking,” in 2021 IEEE International Conference on Blockchain and Cryptocurrency (ICBC). IEEE, 2021, pp. 1–9.

[26] A. Biryukov and S. Tikhomirov, “Transaction clustering using network traffic analysis for bitcoin and derived blockchains,” in IEEE INFO-COM 2019-IEEE Conference on Computer Communications Workshops (INFOCOM WKSHPS). IEEE, 2019, pp. 204–209.

[27] S. Rezaei and X. Liu, “Deep learning for encrypted traffic classification: An overview,” IEEE communications magazine, vol. 57, no. 5, pp. 76– 81, 2019.

[28] Z. Chen, K. He, J. Li, and Y. Geng, “Seq2img: A sequence-to-image based approach towards ip traffic classification using convolutional neural networks,” in 2017 IEEE International conference on big data (big data). IEEE, 2017, pp. 1271–1276.

[29] S.-J. Xu, G.-G. Geng, X.-B. Jin, D.-J. Liu, and J. Weng, “Seeing traffic paths: Encrypted traffic classification with path signature features,” IEEE Transactions on Information Forensics and Security, vol. 17, pp. 2166– 2181, 2022.

[30] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “Fs-net: A flow sequence network for encrypted traffic classification,” in IEEE INFOCOM 2019- IEEE Conference On Computer Communications. IEEE, 2019, pp. 1171–1179.

[31] P. Sirinam, M. Imani, M. Juarez, and M. Wright, “Deep fingerprinting: Undermining website fingerprinting defenses with deep learning,” in Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security, 2018, pp. 1928–1943.

[32] Z. Song, Z. Zhao, F. Zhang, G. Xiong, G. Cheng, X. Zhao, S. Guo, and B. Chen, “I<sup>2</sup>RNN: An Incremental and Interpretable Recurrent Neural Network for Encrypted Traffic Classification,” IEEE Transactions on Dependable and Secure Computing, 2023.

[33] G. Zhou, X. Guo, Z. Liu, T. Li, Q. Li, and K. Xu, “Trafficformer: an efficient pre-trained model for traffic data,” in 2025 IEEE Symposium on Security and Privacy (SP). IEEE Computer Society, 2024, pp. 102–102.

[34] X. Wang, M. He, X. Wang, and S. Guo, “Mtrf: Multidomain transformation representation for network flows in network intrusion detection,” IEEE Transactions on Dependable and Secure Computing, 2025.

[35] R. Zhao, M. Zhan, Q. Li, Z. Liu, X. Deng, Y. Wang, G. Cheng, Z. Xue, and K. Xu, “Learning flow semantics for encrypted traffic analysis: A contrastive pre-training approach,” IEEE Transactions on Dependable and Secure Computing, pp. 1–14, 2026.

[36] M. Lotfollahi, M. Jafari Siavoshani, R. Shirali Hossein Zade, and M. Saberian, “Deep packet: A novel approach for encrypted traffic classification using deep learning,” Soft Computing, vol. 24, no. 3, pp. 1999–2012, 2020.

[37] K. Choromanski, V. Likhosherstov, D. Dohan, X. Song, A. Gane, T. Sarlos, P. Hawkins, J. Davis, A. Mohiuddin, L. Kaiser et al., “Rethinking attention with performers,” arXiv preprint arXiv:2009.14794, 2020.

[38] I. Beltagy, M. E. Peters, and A. Cohan, “Longformer: The longdocument transformer,” arXiv preprint arXiv:2004.05150, 2020.

[39] N. El Ioini and C. Pahl, “A review of distributed ledger technologies,” in OTM Confederated International Conferences” On the Move to Meaningful Internet Systems”. Springer, 2018, pp. 277–288.

[40] CoinMarketCap, “Cryptocurrency historical data snapshot - 28 december 2025,” https://coinmarketcap.com/historical/20251228/, 2025.

[41] J. Yu and A. P. Petropulu, “Study of the effect of the wireless gateway on incoming self-similar traffic,” IEEE Transactions on Signal Processing, vol. 54, no. 10, pp. 3741–3758, 2006.

[42] P. Wang, F. Ye, X. Chen, and Y. Qian, “Datanet: Deep learning based encrypted network traffic classification in sdn home gateway,” IEEE Access, vol. 6, pp. 55 380–55 391, 2018.

[43] W. Meng, W. Li, and J. Zhou, “Enhancing the security of blockchainbased software defined networking through trust-based traffic fusion and filtration,” Information Fusion, vol. 70, pp. 60–71, 2021.

[44] F. Tang, C. Wen, L. Luo, M. Zhao, and N. Kato, “Blockchain-based trusted traffic offloading in space-air-ground integrated networks (sagin): A federated reinforcement learning approach,” IEEE Journal on Selected Areas in Communications, vol. 40, no. 12, pp. 3501–3516, 2022.

[45] Z. Guo, Q. Shang, X. Li, C. Li, Z. Zhang, Z. Zhang, J. Hu, J. An, C. Huang, Y. Chen et al., “Web-ftp: A feature transferring-based pre-trained model for web attack detection,” IEEE Transactions on Knowledge and Data Engineering, vol. 37, no. 3, pp. 1495–1507, 2025.

[46] P. Koshy, D. Koshy, and P. McDaniel, “An analysis of anonymity in bitcoin using p2p network traffic,” in Financial Cryptography and Data Security: 18th International Conference, FC 2014, Christ Church, Barbados, March 3-7, 2014, Revised Selected Papers 18. Springer, 2014, pp. 469–485.

[47] J. Yu, Y. Choi, K. Koo, and D. Moon, “A novel approach for application classification with encrypted traffic using bert and packet headers,” Computer Networks, vol. 254, p. 110747, 2024.

[48] X. Zong, Y. Qi, H. Yan, and Q. Ye, “An intelligent deep learning framework for traffic flow imputation and short-term prediction based on dynamic features,” Knowledge-Based Systems, vol. 300, p. 112178, 2024.

[49] M. Shen, K. Ye, X. Liu, L. Zhu, J. Kang, S. Yu, Q. Li, and K. Xu, “Machine learning-powered encrypted network traffic analysis: A comprehensive survey,” IEEE Communications Surveys & Tutorials, vol. 25, no. 1, pp. 791–824, 2022.

[50] K. Takahashi, K. Yamamoto, A. Kuchiba, and T. Koyama, “Confidence interval for micro-averaged f 1 and macro-averaged f 1 scores,” Applied Intelligence, vol. 52, no. 5, pp. 4961–4972, 2022.

## VII. BIOGRAPHY SECTION

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/f1b10449c04226d5c6267f4c053b1071b40bddb7218a3bd6b4e8674c03d74b90.jpg)

Zhenyu Guo is currently pursuing a Ph.D. degree with the School of Computer Science, Beijing Institute of Technology, Beijing, China. His current research interests include the development of algorithms for deep learning and their application to cyberspace security.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/3e1af262802932150c9958383dff294abe4afbf70133f9e74cd203292de57903.jpg)

Zijian Zhang (zhangzijian@bit.edu.cn) received the Ph.D. degree from the School of Computer Science and Technology, Beijing Institute of Technology. He is now a Professor with the School of Cyberspace Science and Technology, Beijing Institute of Technology. He was a visiting scholar in the Computer Science and Engineering Department, State University of New York at Buffalo in 2015. His research interests include design of authentication and key agreement protocol and analysis of entity behavior and preference.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/a5c4ad5a2b80143995f5c8ebfffba1adbe3f7d08bcfafb6426ba4bcbe979faee.jpg)

Yan Wu is currently pursuing a Ph.D. degree in the School of Cyberspace Science and Technology, Beijing Institute of Technology. She received a B.E.degree and an M.E. degree in engineering from the University of Electronic Science and Technology of China in 2017 and 2020, respectively. Her research interests include blockchain, cryptographic protocols, and network security.

Jiahang Sun (Student Member, IEEE) is currently pursuing a Ph.D. degree in the School of Computer Science and Technology, Beijing Institute of Technology. His research interests include blockchain, anonymous communication, and network security.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/7df9200d9678dcd77980e74eff0d75c97396a9f0a8ea11dabb3fc801c1e0210d.jpg)

Jiamou Liu an Associate Professor at the School of Computer Science, The University of Auckland. He was a Senior Lecturer at Auckland University of Technology between 2011 and 2015. Prior to his current role, Dr. Liu served as a Senior Lecturer at AUT and as a Research Associate at The University of Leipzig. His expertise lies in artificial intelligence, where he has made contributions towards graph data mining, machine learning, and multi-agent systems. He has published over 120 published papers across venues such as AAAI, IJCAI, WWW, and SIGIR.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/c97da2c05a97b134e915e9356e1e4bf96ddd1af9c87b989ed90745ccc664975d.jpg)

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/5a1321e4e788c7a3ee26966064d912b3af9286898bd15aa35789d1946ea60100.jpg)

Xin Li is currently an Associate Professor in the School of Computer Science at Beijing Institute of Technology, China. She received her Ph.D. in Computer Science from Hong Kong Baptist University in 2009. Her research focuses on the development of algorithms for representation learning, reasoning under uncertainty, and machine learning with applications to graph data mining, recommender systems, and robotics.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/a2ac2d655bd51d125aaecd4c4fa115fada0435876be94991273cf060f315020c.jpg)

Yajie Wang received the Ph.D. degree in cyberspace security from the Beijing Institute of Technology, Beijing, China, in 2023. He is currently a Research Fellow with the School of Cyberspace Science and Technology, Beijing Institute of Technology. His research interests include data privacy protection and artificial intelligence security.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/5f77da8a05ab2140637b09af657026ca3f5dd8a7bdf1b79ddb10dd50ddf369ff.jpg)

Guoqiang Zhang received the Master degree in cyberspace security from the Beijing Institute of Technology, Beijing, China, in 2025. His research interests include blockchain, time series analysis, and network security.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/cfe36804cf89cdd48dedab096cfc2d46ae8e28f313d24edff689bc48645c3706.jpg)

Her research interests focus on low-power readout integrated circuit design, cryptographic hardware implementation, network security chip architecture. She is particularly engaged in the hardware security optimization, and physical-layer security enhance

Lei Zhang received the B.S. degree in Electronic Science and Technology from Dalian University of Technology, Dalian, China, in 2008, and the M.S. degree in Microelectronics and Solid-State Electronics from Beijing Institute of Technology, Beijing, China, in 2010.

ment for embedded security chips used in communication and terminal IoT systems.

![](../01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/images/d48e7ca472b9787edabaa099b3b49dac89440c2cbba73d657f40b0560f7d471c.jpg)

Liehuang Zhu is a Full Professor with the School of Cyberspace Science and Technology, Beijing Institute of Technology, Beijing, China. He received his M.S. degree from Wuhan University, Wuhan, China in 2001, and his Ph.D. degree from Beijing Institute of Technology, Beijing, China in 2004, both in computer science. His research interests include data security and privacy protection, blockchain applications, and AI security. He has authored more than 150 journal and conference papers in these areas. He is an Associate Editor of IEEE Transactions on

Vehicular Technology, IEEE Network, and IEEE Internet of Things Journal. He was a Guest Editor of special issue of IEEE Wireless Communications and IEEE Transactions on Industrial Informatics. He has served as Program co-chair of MSN 2017, IWWS 2018, and INTRUST 2014. He received the Best Paper Award at IEEE/ACM IWQoS 2017, IEEE TrustCom 2018, and IEEE IPCCC 2014.
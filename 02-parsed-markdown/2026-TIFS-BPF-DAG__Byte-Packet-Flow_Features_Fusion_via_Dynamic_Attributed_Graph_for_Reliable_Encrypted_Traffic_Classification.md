# BPF-DAG: Byte-Packet-Flow Features Fusion via Dynamic Attributed Graph for Reliable Encrypted Trafic Classification

Yunxiao Shi , Student Member, IEEE, Gaolei Li , Member, IEEE, Jun Wu , Senior Member, IEEE, Jianhua Li , Senior Member, IEEE, and He Fang , Member, IEEE

Abstract—Reliable encrypted trafic classification is crucial for fine-grained and eficient network security management, enabling accurate user behavior recognition and cybercrime forensics. While AI-based methods can automatically extract subtle features from trafic data, existing approaches often fail to efectively capture and integrate features across diferent levels of trafic granularity, namely the byte, packet and flow levels. Current graph-based methods heavily rely on manual feature engineering to construct global IP-based graphs, overlooking critical packetlevel temporal features and byte-level raw information. Focusing on only one or two levels of trafic granularity is unreliable and insuficient, ultimately compromising model accuracy and robustness. To address these limitations, we propose BPF-DAG, a byte-packet-flow feature fusion framework based on dynamic attributed graphs, for reliable encrypted trafic classification. To the best of our knowledge, this is the first method that integrates temporal packet relations into flow interaction patterns while directly leveraging raw byte-level data. Specifically, we introduce a multi-granularity feature fusion strategy that dynamically updates an IP-based graph by iteratively assigning edge attributes derived from evolving flow representations. During the joint training of the Transformer and the graph neural network, temporal representations are learned from raw packet sequences and reflected in edge attributes dynamically for further message aggregation. Experiments on the ISCX VPN-nonVPN, Tor-nonTor, MIRAGE-2019 and MIRAGE-2024 datasets show that BPF-DAG outperforms recent state-of-the-art methods in terms of classification performance.

Index Terms—Encrypted trafic classification, graph neural network, features fusion, transformer, dynamic attributed graph.

## I. INTRODUCTION

sively used to encrypt network trafic, protecting users’ privacy and ensuring anonymity [1]. Since 2019, the proportion of encrypted web trafic has exceeded 90 percent [2]. Meanwhile, the widespread adoption of privacy-enhanced technologies like virtual private network (VPN) and The Onion Router (Tor) [3] is paralleled by a sharp increase in malwares and cyberattacks [4], [5], [6]. Encrypted technologies have been abused by cybercriminals to conceal malicious behaviors, making it dificult to trace trafic sources and posing significant challenges to cybersecurity. Encrypted trafic classification is a fundamental task in the field of cybersecurity, serving as the basis for several tasks such as application identification [7], website fingerprinting [8], and malicious intrusion detection [9]. Highly accurate encrypted trafic classification enables robust user behavior recognition and cyber-crime forensics.

The adoption of encryption protocols significantly curtailed the suficient exploitation of trafic information. Traditional rule-based methods, such as deep packet inspection (DPI) [10], [11], are no longer efective when confronted with encrypted payloads. In recent years, a range of ML-based methods have demonstrated strong performance in encrypted trafic classification [12], [13], [14], [15], [16]. Machine learning (ML)-based methods typically involve two steps: first, extracting hand-crafted statistical features, followed by utilizing traditional machine learning models, such as support vector machines (SVM) and random forests. But the manual feature extraction process is time-consuming and heavily dependent on expert knowledge. Additionally, the granularity of extracted trafic information is often too limited to achieve the reliable encrypted trafic classification. With the rapid advancement of AI [17], [18], [19], [20], deep learning (DL)-based methods have been proposed and have shown excellent performance, as they can automatically extract latent features from raw trafic data [21], [22], [23], [24], [25], [26], [27]. DL-based methods typically transform trafic data into image-like or natural language formats, allowing for the extensive application of computer vision (CV) and natural language processing (NLP) technologies. However, these methods fail to exploit topological patterns in host-to-host communications, i.e., the flow-level trafic information. Fully leveraging the interaction patterns among hosts across a network can further enhance the precision of trafic detection. Recently, graph neural networks (GNNs) [28], [29], [30], [31] have attracted extensive attention for their powerful ability to represent graphs, leading to breakthroughs in fields such as chemistry, physical systems and social networks, among others. GNNs are capable of capturing latent topological patterns via message passing between nodes or edges of a graph. GNN-based methods for encrypted trafic classification can generally be categorized based on their graph construction strategies. One common method involves constructing a packet-level graph, where the packet length sequence of each bidirectional flow is used to model packets as graph nodes. This efectively transforms the trafic classification task into a graph classification problem. However, this approach analyzes each flow independently, lacking a global view of the network connectivity. Another common method attempts to capture trafic interaction patterns by constructing a flow-level global communication graph, where IP addresses are modeled as nodes and trafic flows between hosts are represented as edges. Yet, these approaches rely heavily on feature engineering to initialize graph attributes, without suficiently leveraging byte-level trafic.

To achieve more reliable and accurate encrypted trafic classification, it is imperative to comprehensively exploit multi-granular trafic information to capture discriminative features. In this paper, we propose BPF-DAG, a byte-packet-flow feature fusion-based method via dynamic attributed graphs for reliable encrypted trafic classification. This is the first method that integrates temporal packet relations into flow interaction patterns while directly extracting byte-level features from raw trafic. We introduce a novel multi-granularity feature fusion strategy that comprehensively integrates byte-level, packetlevel, and flow-level trafic features, thereby improving the robustness and efectiveness of the classification.

Specifically, BPF-DAG is composed of three core modules: (1) raw information extraction, (2) flow representation learning, and (3) multi-granularity feature fusion. The first module separately extracts topological and temporal information from raw trafic. The topological information is utilized to construct a global IP-based directed graph that represents flow-level network connectivity. The temporal information refers to the sequences of raw byte packets within each flow, encompassing both packet-level temporal dynamics and bytelevel intrinsic features. In the second module, temporal and topological representations are learned in parallel from the extracted information. Specifically, the Transformer model is employed to capture sequential dependencies in the raw bytebased packet sequences, and the resulting representations are used to initialize the edge attributes in the graph. Concurrently, we propose a novel graph neural network, Directed Edge Sample and Aggregate (DiESAGE), to learn directed edge embeddings by iteratively propagating messages across IP nodes. The output of DiESAGE serves as the flow-level topological representation. In the third module, the temporal and topological representations are fused via linear interpolation to produce the final representation for each flow. During training, temporal flow representations are recomputed after each epoch using the updated Transformer, and the corresponding graph edge attributes are dynamically reassigned. To mitigate memory limitations during joint training of the Transformer and DiESAGE, we adopt a memory bank mechanism that tracks all temporal representations and updates a subset corresponding to the sampled mini-batch.

In summary, the key contributions of our work are outlined as follows:

We propose a byte-packet-flow feature fusion-based reliable encrypted trafic classification method via dynamic attributed graph, called BPF-DAG. BPF-DAG captures packet-level temporal characteristics within each flow and flow-level topological patterns within a global IPbased graph. To the best of our knowledge, this is the first method that integrates packet relations into flow interaction patterns while directly extracting byte-level trafic features, for reliable encrypted trafic classification.

Our approach introduces a multi-granularity features fusion strategy based on dynamic attributed graph, where graph attributes are dynamically assigned with evolving flow representations during each iteration. Temporal representations of flows are computed using an optimized Transformer model after each training epoch, with which the corresponding directed edge attributes are then updated. To reduce the memory overhead, we leverage a technique called Memory Bank to track all temporal representations to decouple the training batch size from the total number of edges.

• To evaluate the classification performance of the proposed BPF-DAG, we compare it with several baselines on six public encrypted trafic datasets, including ISCX-VPN, ISCX-nonVPN, ISCX-Tor, ISCX-nonTor, MIRAGE-2019 and MIRAGE-2024. Experiment results show that BPF-DAG not only outperforms existing SOTA methods by 1.4%, 1.2%, 2.3%, 0.2%, 7.7%, 3.1% in terms of accuracy, but also exhibits relatively lower complexity.

The structure of the paper is as follows: Section II reviews related work, covering ML-based, DL-based, and GNN-based methods, and highlights the diferences between our work and existing approaches. Section III introduces the preliminaries. In Section IV, we describe the designs of our method, including the introduction of overall pipeline and the detailed functions of three sub-modules. In Section V, we experimentally evaluate the performance of our method, including classification performance, few-shot analysis and complexity analysis and compare our results with SOTA methods. Finally, Section VI concludes the paper and discusses future directions.

## II. RELATED WORK

## A. ML-Based Methods

ML-based methods [12], [13], [14], [15], [16], [40] typically consist of two stages: feature engineering and model training. Feature engineering refers to manually extracting statistical features, such as mean packet length, duration, etc. These features are then used as input for ML models such as SVM and Naive Bayes to obtain final classification results. Appscanner [12] takes statistical features derived from packet length sequences as input for training Random Forest classifier. Anderson et al. [41] extract 198 TLS features, including flow metadata, byte distribution, packet lengths, and then apply a logistic regression classifier to classify encrypted trafic. Shi et al. [32] propose a feature optimization approach that eficiently reduces redundant statistical features and mitigates the negative efects of class imbalance. NB-SVM [15] utilizes a naive Bayes feature embedding method to transforms the original features into high-quality data, which is then classified using an SVM. However, ML-based methods depend heavily on expert-designed features and fail to fully exploit raw byte trafic. In contrast, our method does not rely on feature engineering and directly utilizes byte-level trafic data for classification.

## B. DL-Based Methods

DL-based methods are capable of automatically extracting features from raw trafic data, enabling a unified end-to-end framework. Wang et al. were the first to apply representation learning to trafic classification by transforming raw trafic into grayscale images and utilizing convolutional neural networks (CNNs), including both 1D-CNN [21] and 2D-CNN [42], to perform image classification. Building on this, some works [24], [25], [43] have combined CNNs with RNNs to capture temporal characteristics from time-related raw packet sequences. Other methods, such as DF [22] and FS-Net [23], employ DL models to extract sequential features from packet length sequences. XAI [44] investigates trustworthiness and interpretability via explainable AI-based techniques to understand, interpret and improve the behavior of multimodal DL trafic classifiers. Additionally, the pre-training strategy have been applied to encrypted trafic classification by leveraging large amounts of unlabeled trafic data [33], [34], [45]. ET-BERT [34], for instance, converts raw bytes into language-like tokens for pre-training, and then fine-tune the pre-trained model for specific downstream classification tasks. PEAN [46] is a multimodal pre-training-based framework that jointly models raw bytes and packet lengths to classify encrypted traffic. Although these methods successfully extract rich features from raw trafic, they treat each trafic flow independently, neglecting the interrelations inherent in trafic flows.

## C. GNN-Based Methods

Recently, an increasing number of studies have leveraged GNNs to extract topological characteristics of trafic due to their powerful ability to capture structural patterns from graph format data. Hu et al. [35] introduce the Trafic Interaction Graph (TIG) to represent each single flow based on its packet length sequence to capture implicit features in bidirectional client-server interactions, turning DApp fingerprinting into a graph classification problem. Hu et al. [35] construct a flow graph from the initial several interactive packets for each flow, adopt graph2vec algorithm to learn its representation and classify the representations with Random Forest. Zhang et al [38] propose a byte-level trafic graph construction approach that uses the GNN to embed packet header and payload bytes separately and then fuses them together to generate an overall representation. Lo et al. [36] construct a global IP-based graph for all flows where IP addresses and ports are mapped as nodes, trafic flows are mapped as the graph’s edges and edge attributes are initialized with statistical trafic features. It efectively transfers the encrypted trafic classification problem into an edge classification problem. Building on this, Duan et al. [37] propose a Dynamic Line Graph Neural Network (DLGNN)-based method with semisupervised learning. It transforms trafic data into a series of spatio-temporal graphs and employs dynamic GNN to capture the evolving of interaction between IP pairs in each snapshot. Wang et al. [39] introduce a Heterogeneous Temporal Graph (HTGraph) to represent the dynamic feature series of network flows. The HTGraph is based on prior knowledge about feature types and correlations, contributing to learning general and transferable knowledge for trafic classification.

## D. Diferences From Existing Work

Most existing GNN-based methods for encrypted trafic classification treat hosts in the network as nodes and the communication interaction among hosts as edges. Its primary advantage lies in the ability of leveraging GNN to extract the global topology patterns of cyberspace from the host-tohost communication interactions. However, the disadvantages to this method are obvious: it relies on feature engineering to initialize the graph attributes in advance and statistical features fail to adequately capture the temporal characteristics of trafic itself. Although few cutting-edge works like [39] attempt to leverage dynamic graphs to enhancing generalization for encrypted trafic classification, they still have not eliminate the need for feature engineering.

We compare the aforementioned encrypted trafic classification methods with our work in Table I, including ML-based, DL-based and GNN-based methods. In contrast, our method gets rid of the dependence on feature engineering and directly uses the raw-byte trafic within the global IP-based graph. We fully integrate byte-packet-flow multi-granularity features based on dynamic attributed graph to generate more discriminative trafic representations.

## III. PRELIMINARIES

## A. Notation

Encrypted trafic is made up of a sequence of packets transferred among hosts. Based on the level of granularity, trafic can be commonly divided into packets, flows or sessions. A flow represents a series of consecutive packets that share the same five attributes: source IP, destination IP, source port, destination port and protocol. Flows are unidirectional, while sessions refer to bidirectional flows. To learn robust temporal representations from raw-byte flows, we propose a Packet2Vec module, which is designed to convert a packet into a word-like token, similar to those used in NLP. A single packet can be viewed as a sequence of 8-bit bytes, consisting of a plaintextbased header and a ciphertext-based payload. Since each 8-bit byte corresponds to a decimal number ranging from 0 to 255, a packet at timestamp t can be represented as a vector:

$$
P _ {t} = \left[ b _ {h 1} ^ {t}, b _ {h 2} ^ {t}, \dots , b _ {h n} ^ {t}, b _ {p 1} ^ {t}, \dots , b _ {p m} ^ {t} \right], b _ {h i} ^ {t}, b _ {p j} ^ {t} \in [ 0, 2 5 5 ]\tag{1}
$$

TABLE I  
A SUMMARY OF EXISTING APPROACHES

<table><tr><td>Category</td><td>Typical Methods</td><td>Raw bytes-based</td><td>Temporal Feature</td><td>Topological Feature</td><td>Minibatch Training</td><td>Few-shot Setting</td></tr><tr><td rowspan="3">ML-based Methods</td><td>Appscanner [12]</td><td>×</td><td>×</td><td>×</td><td>√</td><td>×</td></tr><tr><td>NB-SVM [15]</td><td>×</td><td>×</td><td>×</td><td>√</td><td>×</td></tr><tr><td>EFOA [32]</td><td>×</td><td>×</td><td>×</td><td>√</td><td>×</td></tr><tr><td rowspan="4">DL-based Methods</td><td>TSCRNN [25]</td><td>√</td><td>√</td><td>×</td><td>√</td><td>×</td></tr><tr><td>FS-Net [23]</td><td>×</td><td>√</td><td>×</td><td>√</td><td>×</td></tr><tr><td>YaTC [33]</td><td>√</td><td>√</td><td>×</td><td>√</td><td>√</td></tr><tr><td>ET-BERT [34]</td><td>√</td><td>√</td><td>×</td><td>√</td><td>√</td></tr><tr><td rowspan="7">GNN-based Methods</td><td>GraphDApp [35]</td><td>√</td><td>√</td><td>×</td><td>√</td><td>×</td></tr><tr><td>Graph2vec+RF [35]</td><td>√</td><td>√</td><td>×</td><td>√</td><td>×</td></tr><tr><td>E-GraphSAGE [36]</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td></tr><tr><td>DLGNN [37]</td><td>√</td><td>√</td><td>√</td><td>×</td><td>√</td></tr><tr><td>TFE-GNN [38]</td><td>√</td><td>√</td><td>×</td><td>√</td><td>×</td></tr><tr><td>K-GetNID [39]</td><td>×</td><td>√</td><td>×</td><td>√</td><td>√</td></tr><tr><td>Ours</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td></tr></table>

where $b _ { h _ { i } } ^ { t }$ and $b _ { p _ { j } } ^ { t }$ denote the decimal values corresponding to header and payload bytes, respectively. A single flow, therefore, can be represented as a 2-dimensional tensor:

$$
f l o w = [ P _ {t _ {1}}, P _ {t _ {2}}, \dots , P _ {t _ {n}} ]\tag{2}
$$

where $P _ { t _ { i } }$ denotes the ith packet in the flow, $t _ { n }$ is the timestamp for it and n is the total number of packets of the flow. In this way, the representation of a flow can be viewed as analogous to sentence embedding in NLP, where multiple word-like vectors (packets) form a flow. This transformation allows us to leverage NLP techniques to extract temporal characteristics from network flows, facilitating a deeper analysis of temporal trafic patterns.

## B. Problem Definition

The goal of encrypted trafic classification is to detect and identify specific trafic categories (e.g., applications and web services) based on the trafic they generate. In this paper, we classify encrypted flows directly from raw byte-level trafic, bypassing the need for statistical features derived through feature engineering. We evaluate our model on two types of encrypted trafic classification tasks: (1) user behavior identification over VPN or Tor (e.g., video streaming, email communication, and file transfer), and (2) encrypted application classification (e.g., Facebook, Spotify, and YouTube). In our experiment, we treat each flow as a data example for training or testing. Our objective is to build an end-toend classification framework f(f low<sub>i</sub>) that predicts the correct label for each flow.

## IV. METHODOLOGY

## A. Overall Framework

In this section, we systematically introduce the proposed method, BPF-DAG, a dynamic attributed graph-based framework that integrates multi-granularity trafic features across the byte, packet, and flow levels. The architecture comprises three core modules: raw information extraction, flow representation learning, and multi-granularity feature fusion. In the first module, we directly extract topological and temporal information from raw trafic data. At the topological level, we construct a global directed IP-based graph by represent ing host communications as directed edges between IP-port pairs. At the temporal level, we extract fixed-length header byte sequences from individual packets, preserving essential byte-level information. The second module learns two complementary representations: temporal representations are obtained using a Transformer encoder that models sequential dependencies within packet sequences, while topological representations are learned via a custom graph neural network named Directed Edge Sample and Aggregate (DiESAGE), which propagates messages along directed edges in the graph. Edge attributes are initialized with temporal features and dynamically updated during training to reflect evolving flow representations. In the third module, we fuse the temporal and topological representations via linear interpolation, enabling the model to generate enriched, discriminative embeddings for flow classification. To eficiently support joint training of the Transformer and GNN under memory constraints, we incorporate a Memory Bank mechanism that maintains and selectively updates temporal representations across training iterations. Figure 1 provides an overview of our proposed end-to-end BPF-DAG method.

## B. Raw Information Extraction

Instead of relying on feature engineering, we directly extract information from raw encrypted trafic as input for subsequent modules. This approach not only maximizes the information available from the raw trafic but also enables an end-to-end trafic classification framework. Given that encryption technology transforms packet payloads into pseudorandom values, we focus exclusively on using the raw plaintext information from the packet headers.

1) Temporal Information Extraction: At the byte level of a flow, each 8-bit byte can be encoded as a decimal number between 0 and 255. At the packet level, each packet can be transformed into a fixed-length vector, as explained in the Preliminaries section. Only the header bytes are used, while the encrypted payload bytes are discarded. The header contains a rich set of discriminative fields that provide key details about the flow, such as packet length, timestamp, and protocol. The vector length of packet header is limited to M bytes, with any excess being truncated. If the header is shorter than M bytes, it is padded with zeros. Thus, a packet at timestamp t can be encoded as a vector:

![](images/d26084b3853e7200c95768f9ed694d3d493e1bdc4061e3f40a0f21ccb2faf51f.jpg)  
Fig. 1. The overview of proposed BPF-DAG Framework. The lower part illustrates how raw byte packet sequences are input into a Transformer to learn temporal representations. The upper part shows that network connectivity information, combined with the learnable temporal representations, is used to construct graphs, which are then processed by DiESAGE to capture topological representations. The left part details the multi-granularity feature fusion process. During the joint training of DiESAGE and the Transformer, the graph is dynamically updated by iteratively assigning edge attributes based on the evolving temporal representations.The Memory Bank technique is used to decouple the training batch size from the total number of edges. The specific module configurations and parameters are presented in Figure 4 and Table III.

$$
P _ {t} = [ b _ {h 1} ^ {t}, b _ {h 2} ^ {t}, \dots , b _ {h M} ^ {t} ], b _ {h i} ^ {t} \in [ 0, 2 5 5 ]\tag{3}
$$

At the flow level, each flow is composed of a sequence of timerelated packets. We take the first N adjacent packets, which form a sequence of N M-dimensional vectors, as the initial representation of the flow. If the flow has fewer than N packets, it is padded with zero vectors. Ultimately, a flow is represented as a two-dimensional tensor of size (N, M):

$$
f l o w _ {i} = \left[ P _ {1}, P _ {2}, \dots , P _ {N} \right], P _ {i} \in \mathbb {R} ^ {M}\tag{4}
$$

In fact, this initial flow representation closely resembles a sentence composed of word vectors. Hence, NLP techniques can naturally be applied to learn the temporal representation of the flow, as discussed in the following section.

2) Topological Information Extraction: Computer networks fundamentally exist as communication graphs, where each host acts as a node, and the communication between hosts represents the links between nodes. From the perspective of a single flow, it can be modeled as a directed edge with two nodes in the communication graph. Four flow fields are extracted to identify the directed edge: source IP address, source port, destination IP address, and destination port. The first two fields are combined into a 2-tuple (source IP address, source port) to represent the source node, while the latter two fields represent the destination node.

To mine the topological information of host-to-host communications, we construct a global IP-based flow interaction graph. The previous temporal information will be integrated into the graph. The initial flow representation flow will be fed into a neural network with learnable parameters to generate its temporal representation, which is utilized to initialize its corresponding edge attribute. Before training, each edge attribute is initialized using the corresponding temporal representation, computed by randomly initialized trainable parameters. During the training process, the edge attributes are dynamically updated and optimized.

In this way, the encrypted trafic classification task is naturally transformed into a directed edge classification problem.

## C. Flow Representation Learning

In this module, based on the temporal and topological information extracted from the raw trafic, we introduce a sequence-based model and a novel graph neural network to learn the temporal and topological representations respectively.

1) Learning Temporal Representations With Transformer: In the Preliminaries Section, we encoded a flow as a sequence of packet vectors, represented as a two-dimensional tensor. The relationship between a flow and its packets is analogous to that of a sentence and its words. Building on this analogy, we utilize the Transformer network [47] to learn temporal representations of trafic flows. We use the same architecture as the classic Transformer encoder.

The classic Transformer architecture, initially designed to address sequence-to-sequence (Seq2Seq) tasks [48], is composed of an encoder block and a decoder block. For our purposes, we employ only the encoder to process the input trafic sequences and generate temporal flow representations. The encoder consists of multiple identical blocks, each containing two primary sublayers: a multi-head self-attention mechanism and a position-wise feed-forward network (FFN). In the first layer, the self-attention mechanism enables each position in the input sequence to pay attention to other positions, capturing time-related characteristics throughout the sequence. For an input sequence $f l o w _ { i } \in \mathbb { R } ^ { N \times M }$ , each selfattention head computes a query matrix Q, key matrix K and value matrix V through the following linear transformations:

$$
Q = Z \mathbf {W} ^ {Q}, K = Z \mathbf {W} ^ {K}, V = Z \mathbf {W} ^ {V}\tag{5}
$$

where $\mathbf { W } ^ { Q } , \mathbf { W } ^ { K } , \mathbf { W } ^ { V } \in \mathbb { R } ^ { M \times d }$ are trainable parameter matrices, $Q , K , V \in \mathbb { R } ^ { N \times d }$ and d is the dimension of the latent representation. The output of the i th self-attention head is computed as:

$$
H e a d _ {i} = \text { Attention } (Q _ {i}, K _ {i}, V _ {i}) = \text { soft } \max \left(\frac {Q _ {i} K _ {i} ^ {T}}{\sqrt {d}}\right) V _ {i}\tag{6}
$$

The attention mechanism is simultaneously applied across several heads, and then the outputs from each head are concatenated and subjected to a final linear transformation:

$$
M u l t i H e a d (Q, K, V) = \mathbf {C O N C A T} (H e a d _ {1}, \dots , H e a d _ {n}) \mathbf {W} ^ {O}\tag{7}
$$

In the second layer, a FFN is employed independently and uniformly to each position. It is composed of two linear transformations with a ReLU activation function in between:

$$
F F N (x) = \max (0, x \mathbf {W} _ {1} + b _ {1}) \mathbf {W} _ {2} + b _ {2}\tag{8}
$$

Additionally, residual connection and layer normalization operations are applied to both sublayers. These techniques enhance gradient flow and facilitate stable training, while supporting deeper network architectures.

$$
Z ^ {\prime} = \text { LayerNorm } (Z + \text { MultiHead } (Q, K, V))\tag{9}
$$

$$
X _ {\text { temporal }} = \text { LayerNorm } (Z ^ {\prime} + F F N (Z ^ {\prime}))\tag{10}
$$

The output of the Transformer, denoted as $X _ { \mathrm { t e m p o r a l } } \in \mathbb { R } ^ { N \times D } .$ is referred to as the temporal representation of the flow.

2) Learning Topological Representations With DiESAGE: To further capture the topological characteristics of trafic through interaction among hosts, we introduce a novel graph neural network named Directed Edge Sample and aggregate (DiESAGE). GraphSAGE (Graph Sample and Aggregate) [31] is a powerful GNN framework designed for generating node embeddings in large graphs, primarily tailored for node classification tasks. However, the traditional GraphSAGE model is specifically designed for learning node embeddings. The existing E-GraphSAGE method [36] is not suited for generating representations for directed edges. To address this limitation, our proposed DiESAGE introduces several modifications to support directed edge embeddings.

The inputs to DiESAGE consist of edge and node features. The edge features are initialized with the temporal representations $X _ { \mathrm { t e m p o r a l } } .$ , which are dynamically updated at each epoch during the training process. Meanwhile, the node features are initialized with constant vectors $\{ 1 \cdots 1 \}$ , where the dimension of each node vector matches that of the edge features.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 DiESAGE Directed Edge Embedding
Input: Graph $\mathcal{G}(\mathcal{V},\mathcal{E})$; input edge attributes $\{\mathbf{e}_{uv},\forall uv\in\mathcal{E}\}$; input node attributes $\{n_v,\forall v\in\mathcal{V}\}=\{1,\ldots,1\}$; depth $K$
Output: Directed edge embeddings $\{z_{uv},\forall uv\in\mathcal{E}\}$
1: $\mathbf{h}_0\leftarrow n_v,\forall v\in\mathcal{V}$
2: $\mathbf{e}_{uv}^0\leftarrow e_{uv},\forall uv\in\mathcal{E}$
3: for $k\leftarrow 1$ to $K$ do
4:    for $u\in\mathcal{V}$ do
5:    $\mathbf{h}_{\mathcal{N}(u)}^k\leftarrow\text{AGG}\left(\left\{\mathbf{e}_{uv}^{k-1},\forall v\in\mathcal{N}(u),uv\in\mathcal{E}\right\}\right)$
6:    $\mathbf{h}_u^k\leftarrow\sigma\left(\mathbf{W}^k\cdot\text{CONCAT}\left(\mathbf{h}_u^{k-1},\mathbf{h}_{\mathcal{N}(u)}^k\right)\right)$
7:    end for
8: end for
9: for $uv\in\mathcal{E}$ do
10:    $z_{uv}=\text{CONCAT}\left(\mathbf{h}_u^K,\mathbf{h}_v^K\right),uv\in\mathcal{E}$
11: end for
12: return $z_{uv}$
</div>

At each iteration, instead of aggregating information from neighboring nodes, DiESAGE aggregates features from directed edges pointing from the node to its neighbors, and subsequently updates the node’s features based on the aggregated information. At the kth layer, the aggregated representation $\mathbf { h } _ { \mathcal { N } ( u ) } ^ { k }$ is computed using a diferentiable aggregation function $A G G ,$ , defined as:

$$
\mathbf {h} _ {\mathcal {N} (u)} ^ {k} = \operatorname{AGG} \left(\left\{\mathbf {e} _ {u v} ^ {k - 1}, \forall v \in \mathcal {N} (u), u v \in \mathcal {E} \right\}\right)\tag{11}
$$

Here, $\{ \nu \ \in \ { \mathcal { N } } ( u ) , u \nu \ \in \ { \mathcal { E } } \}$ represents the set of directed edges pointing from source node u to its neighbor nodes, and $\mathbf { e } _ { u \nu } ^ { k - 1 }$ denotes the edge features at the k − 1th layer. The aggregation function AGG calculates the mean of $\mathbf { e } _ { u \nu } ^ { k - 1 }$ . Next, the aggregated representation $\mathbf { h } _ { \mathcal { N } ( u ) } ^ { k }$ of the neighbor edges is concatenated with the node’s previous representation $\mathbf { h } _ { u } ^ { k - 1 }$ After applying a trainable weight matrix $\mathbf { W } ^ { k }$ and an activation function, the node representation at the kth layer is updated as follows:

$$
\mathbf {h} _ {u} ^ {k} = \sigma \left(\mathbf {W} ^ {k} \cdot \text { CONCAT } \left(\mathbf {h} _ {u} ^ {k - 1}, \mathbf {h} _ {\mathcal {N} (u)} ^ {k}\right)\right)\tag{12}
$$

At depth K, the final representation of the edge $\mathbf { e } _ { u \nu } ^ { K }$ is computed by concatenating representations of node u and v as follows:

$$
X _ {\text { topological }} = \text { CONCAT } \left(\mathbf {h} _ {u} ^ {K}, \mathbf {h} _ {v} ^ {K}\right), u v \in \mathcal {E}\tag{13}
$$

The output of DiESAGE, referred to as the topological representation $X _ { \mathrm { t o p o l o g i c a l } } ~ \in ~ \mathbb { R } ^ { D \times d }$ , captures the topological information of the communication graph. Figure 3 illustrates the process of message propagating through nodes and edges in 1-hop scenario. Algorithm 1 presents the DiESAGE algorithm for directed edge embedding, and the relevant symbols are summarized in Table II.

## D. Multi-Granularity Features Fusion

After capturing both the temporal and topological representations of the trafic, we fuse them via linear interpolation to

![](images/8722ac6d3a5a7255155ae8a6d22bde92545c21dd70fca03364607bb8d8030954.jpg)  
Fig. 2. The schematic illustration of flow preprocessing.

TABLE II  
SUMMARY OF SYMBOLS AND DESCRIPTIONS

<table><tr><td>Symbols</td><td>Descriptions</td></tr><tr><td> $\mathcal{E}$ </td><td>The set of directed edges in Graph  $\mathcal{G}$ </td></tr><tr><td> $\mathcal{V}$ </td><td>The set of nodes in Graph  $\mathcal{G}$ </td></tr><tr><td> $\mathbf{W}^{k}$ </td><td>The trainable weight matrix at the k-th layer</td></tr><tr><td> $\mathbf{h}_{u}^{k}$ </td><td>The embeddings of nodes at the k-th layer</td></tr><tr><td> $\mathbf{e}_{uv}^{k}$ </td><td>The embeddings of edges at the k-th layer</td></tr><tr><td> $\mathbf{z}_{uv}$ </td><td>The final directed edge embeddings</td></tr><tr><td>AGG</td><td>The differentiable aggregator function</td></tr><tr><td> $\mathcal{F}$ </td><td>Input samples of raw byte-based flows</td></tr><tr><td> $\mathcal{N}(u)$ </td><td>The set of neighbors of node  $u$ </td></tr><tr><td> $\sigma$ </td><td>The ReLU activation function</td></tr><tr><td> $X_{\text{temporal}}$ </td><td>Temporal representations extracted with Transformer</td></tr><tr><td> $X_{\text{temporal}}'$ </td><td>A sampled mini-batch of temporal representations</td></tr><tr><td> $X_{\text{topological}}$ </td><td>Topological representations extracted with DiESAGE</td></tr><tr><td> $Z_{\text{temporal}}$ </td><td>Low-dimensional temporal prediction vectors</td></tr><tr><td> $Z_{\text{topological}}$ </td><td>Low-dimensional topological prediction vectors</td></tr><tr><td> $Z_{\text{fusion}}$ </td><td>Final features fusion representations</td></tr><tr><td> $\theta_{\text{BPF-DAG}}$ </td><td>The parameters of model BPF-DAG</td></tr></table>

![](images/e8fa149f715716f707397c2ce8113cb872cbba82e87ad8e4fb62053355b16753.jpg)  
Fig. 3. The illustration of the DiESAGE model in 1-hop propagation scenario.

maximize the extracted trafic information. The cross-entropy loss is employed over labeled edges for jointly optimizing both the Transformer and DiESAGE models. Additionally, a technique called Memory Bank is employed to enable mini-batch gradient descent when training the GNN. The pseudocode of our method is presented in Algorithm 2 and the relevant symbols are summarized in Table II.

```txt
Algorithm 2 Pseudocode of the BPF-DAG Algorithm
Input: Graph G(V, E); raw-byte flows F; input edge attributes {euv, ∀uv ∈ E}; depth K; number of training epochs T; linear interpolation coefficient μ; traffic label Ylabel
Output: Parameters of BPF-DAG model θBPF-DAG
1: for epoch ← 1 to T do
2:    // Update attributes of all edge using Transformer after each epoch
3:    Xtemporal ← TransformerEncoder(F)
4:    Update edge features {euv, ∀uv ∈ E} with Xtemporal
5:    // Set a Memory Bank to track all temporal representations
6:    for Fmini-batch ∈ F do
7:    // Update a subset of edges corresponding to the sampled mini-batch with optimized Transformer
8:    Xtemporal' ← TransformerEncoder(Fmini-batch)
9:    Update edge features {euv, ∀uv ∈ Emini-batch} with Xtemporal'
10:    Xtemporal ← {euv, ∀uv ∈ E}
11:    Xtopological = DiESAGE(euv), ∀uv ∈ E
12:    // Map representations to low-dimensional prediction vectors
13:    Ztemporal ← softmax(W1Xtemporal)
14:    Ztopological ← softmax(W2Xtopological)
15:    // Generate final representations with linear interpolation
16:    Zfusion ← (1 - μ)Ztemporal + μZtopological
17:    Loss ← CrossEntropy(Zfusion, Ylabel)
18:    θBPF-DAG ← Adam(Loss)
19:    end for
20: end for
21: return θBPF-DAG
```

TABLE III  
DETAILED ARCHITECTURE AND PARAMETER STATISTICS OF THE BPF-DAG MODEL

<table><tr><td>Layer (type)</td><td>Input Shape</td><td>Output Shape</td><td>Param #</td></tr><tr><td>Seq Model (Transformer)</td><td>[-1, 10, M]</td><td>[-1, 128]</td><td>1,058,800</td></tr><tr><td>PositionalEncoding</td><td>[-1, 10, M]</td><td>[-1, 10, M]</td><td>0</td></tr><tr><td>4 × TransformerEncoderLayer</td><td>[-1, 10, M]</td><td>[-1, 10, M]</td><td>~1,051,000</td></tr><tr><td>MultiheadAttention</td><td>[-1, 10, M]</td><td>[-1, 10, M]</td><td>14,640 × 4</td></tr><tr><td>FeedForward (Linear1+Linear2)</td><td>[-1, 10, M]</td><td>[-1, 10, M]</td><td>(124,928 + 122,940) × 4</td></tr><tr><td>LayerNorm + Dropout</td><td>[-1, 10, M]</td><td>[-1, 10, M]</td><td>240 × 4</td></tr><tr><td>Linear (fc)</td><td>[-1, M]</td><td>[-1, 128]</td><td>7,808</td></tr><tr><td>Classifier</td><td>[-1, 128]</td><td>[-1, num_classes]</td><td>1,032</td></tr><tr><td>Linear</td><td>[-1, 128]</td><td>[-1, num_classes]</td><td>1,032</td></tr><tr><td>GNN (DiESAGE)</td><td>[edges, 128]</td><td>[edges, num_classes]</td><td>133,640</td></tr><tr><td>SAGE Layer 0</td><td>[edges, 128]</td><td>[edges, 128]</td><td>65,792</td></tr><tr><td>W_msg (Linear)</td><td>[edges, 256]</td><td>[edges, 128]</td><td>32,896</td></tr><tr><td>W_apply (Linear)</td><td>[edges, 256]</td><td>[edges, 128]</td><td>32,896</td></tr><tr><td>SAGE Layer 1</td><td>[edges, 128]</td><td>[edges, 128]</td><td>65,792</td></tr><tr><td>W_msg (Linear)</td><td>[edges, 256]</td><td>[edges, 128]</td><td>32,896</td></tr><tr><td>W_apply (Linear)</td><td>[edges, 256]</td><td>[edges, 128]</td><td>32,896</td></tr><tr><td>MLP Predictor (W)</td><td>[edges, 256]</td><td>[edges, num_classes]</td><td>2,056</td></tr><tr><td>Total Parameters</td><td>-</td><td>-</td><td>1,193,472</td></tr></table>

1) Interpolating Topological and Temporal Representations: To fuse the topological and temporal representations, we linearly interpolate $X _ { \mathrm { t e m p o r a l } }$ and $X _ { \mathrm { t o p o l o g i c a l } }$ , then feed them into a linear layer to obtain the final prediction output. During our experiments, we found that applying an auxiliary transformation before classification improves the overall accuracy. Specifically, we map the temporal and topological representations to low-dimensional prediction vectors through the following auxiliary function:

$$
Z _ {\text { temporal }} = \operatorname{softmax} \left(\mathbf {W} _ {1} X _ {\text { temporal }}\right)\tag{14}
$$

$$
Z _ {\mathrm{topological}} = \text { softmax } (\mathbf {W} _ {2} X _ {\mathrm{topological}})\tag{15}
$$

where $\mathbf { W } _ { 1 } , \mathbf { W } _ { 2 } \in \mathbb { R } ^ { d \times p }$ denote trainable weight matrices, and $p$ represents the number of trafic categories. Next, we apply linear interpolation to obtain the final prediction vector:

$$
Z _ {\text { fusion }} = (1 - \mu) Z _ {\text { temporal }} + \mu Z _ {\text { topological }}\tag{16}
$$

The coeficient $\mu$ is a hyperparameter controlling the balance between temporal and topological information. When $\mu = 0$ only the temporal representation is used, ignoring the topological features of network trafic. Conversely, $\mu = 1$ fully utilizes the topological features, but some temporal characteristics may be lost owing to the graph message-passing process. A balanced value of $0 ~ < ~ \mu ~ < ~ 1$ optimally fuses both the temporal and topological predictions. The cross-entropy loss is employed as the objective function over labeled directed edges:

$$
L = \text { CrossEntropy } (Z _ {\text { fusion }}, Y _ {\text { label }})\tag{17}
$$

2) Updating Graph Attributes With Memory Bank: Throughout training, edge attributes are dynamically updated using $X _ { \mathrm { t e m p o r a l } }$ at each epoch, allowing the temporal representation of each flow to remain optimal during training.

Traditional GNN models typically use full-batch gradient descent, which is unsuitable for our BPF-DAG model for two reasons. First, the scale of the Internet is vast, involving a massive number of IP addresses, which likely makes the graph quite large. Second, simultaneously optimizing both the Transformer and DiESAGE models may lead to memory limitations on the GPU. To address these challenges, we adopt a Memory Bank (MB) technique inspired by contrastive learning methods [49], [50]. MB decouples the mini-batch size from the total number of graph edges by storing their representations.

Specifically, we set a MB to keep track of the temporal representations $X _ { \mathrm { t e m p o r a l } }$ of both labeled and unlabeled flow samples. At the start of each epoch, all $X _ { \mathrm { t e m p o r a l } }$ representations are computed using the current Transformer parameters, and the MB is updated. During each mini-batch iteration, we sample a mini batch from the graph edges, recompute their representations with the current Transformer, and update the corresponding entries in the MB. These updated representations, denoted as $X _ { \mathrm { t e m p o r a l } } { ' }$ , are then fed into the DiESAGE model. The cross-entropy loss for the mini-batch is then computed and backpropagated.

Since $X _ { \mathrm { t e m p o r a l } }$ in the MB are computed at diferent iterations within each epoch, they may become inconsistent. To mitigate this, we use a relatively small learning rate for the Transformer to improve the consistency of stored representations in the MB.

## V. EXPERIMENTS

## A. Experiment Setup

1) Datasets: To comprehensively evaluate the efectiveness of BPF-DAG, we conducted experiments on six public encrypted trafic datasets, including the ISCX VPN-nonVPN dataset [51], the ISCX Tor-nonTor dataset [52], the MIRAGE-2019 dataset [53] and the MIRAGE-2024 dataset [54].

The VPN-nonVPN dataset contains encrypted trafic routed through virtual private networks (VPNs) and regular encrypted trafic, both of which encompass six trafic categories: P2P, VoIP, etc. VPNs are commonly used to bypass censorship and access restricted services, and the use of tunnel technology complicates the identification of applications running through

TABLE IV  
RECOMMENDED HYPERPARAMETER CONFIGURATION FOR BPF-DAG

<table><tr><td>Groups</td><td>Hyperparameter</td><td>Description</td><td>Value</td></tr><tr><td rowspan="4">Model Setup</td><td> $n_e$ </td><td>The number of encoders in Transformer.</td><td>4</td></tr><tr><td> $n_h$ </td><td>The number of headers for multi-head self-attention.</td><td>5</td></tr><tr><td>K</td><td>The number of layers in DiESAGE.</td><td>2</td></tr><tr><td>p</td><td>The dropout rate in each layer.</td><td>0.2</td></tr><tr><td rowspan="4">Traffic Pre-Processing</td><td>N</td><td>The number of the first few packets truncated in each flow.</td><td>10</td></tr><tr><td>M</td><td>The number of the first few raw bytes truncated in each packet.</td><td>60/200</td></tr><tr><td> $D_T$ </td><td>The embedding size of temporal representations.</td><td>128</td></tr><tr><td> $D_S$ </td><td>The embedding size of topological representations.</td><td>128</td></tr><tr><td rowspan="4">Training process</td><td>μ</td><td>The linear interpolation coefficient of topological and temporal representations.</td><td>0.9/0.4</td></tr><tr><td> $LR_T$ </td><td>The initial learning rate of the optimizer for Transformer.</td><td>1e-5</td></tr><tr><td> $LR_S$ </td><td>The initial learning rate of the optimizer for DiESAGE.</td><td>1e-3</td></tr><tr><td>BATCH_SIZE</td><td>The number of training examples during each iteration.</td><td>128</td></tr></table>

VPNs. Similarly, the Tor-nonTor dataset includes trafic collected via onion routers (Tor) and regular encrypted trafic, both featuring eight types of trafic: browsing, audio streaming, chat, video streaming, mail, VoIP, P2P, and file transfer. Tor anonymizes internet activities by encrypting and routing trafic through a distributed network, which adds complexity to trafic classification. The MIRAGE-2019 dataset is a publicly available, human-generated mobile trafic dataset designed for encrypted mobile app trafic analysis. It includes trafic from 40 Android applications across 16 app categories, focusing on common functionalities such as service registration, login, and regular interactions. The release of the MIRAGE-2024 dataset aims to facilitate further research and development in mobile network trafic analysis, focusing on interactive, multi activity apps and activity-level analysis.

2) Data Preprocessing: Firstly, we remove packets irrelevant to the transmitted content of trafic, such as Address Resolution Protocol (ARP) and Internet Control Message Protocol (ICMP) packets. Then, we use SplitCap tool to split the raw trafic datasets into unidirectional flows and each flow is taken as a sample for training or testing. To address the scarcity of flow examples in some datasets, especially Tor dataset, we augment the flow samples by splitting longer flows into shorter ones. The number of splitted flows from the original long flow is no more than 10. Finally, we partition each dataset into training, validation, and testing sets in a 7:1:2 ratio.

3) Implementation Details and Evaluation Metrics: During the raw trafic pre-processing stage of BPF-DAG, we truncate the first 60 and 200 bytes of each raw packet for the ISCX and MIRAGE datasets, respectively. The MIRAGE datasets lacks original pcap files and comprises only transport-layer payload bytes, without the associated packet header information. Therefore, we use only the encrypted payload bytes of the MIRAGE datasets as input. In our experiments, only the first 10 packets of each flow are retained for all datasets, and the remaining packets are discarded. This retained length is considerably shorter than that used in [8], [12], and [22], where some flows include up to 5,000 packets. For training, we utilize the encoder of the Transformer and a two-layer DiESAGE model to implement the BPF-DAG method. The Adam optimizer with a learning rate scheduler is applied, with initial learning rates of 1e-3 for the DiESAGE model and 1e-5 for the Transformer model. The batch size is set to 64, and training runs for 100 epochs. The model is implemented in PyTorch 2.0.1 and trained on a single NVIDIA RTX 4060 GPU. We run each experiment independently 5 times and average the results to reduce the impact of any variability or outliers. Table IV shows the hyperparameters used in BPF-DAG and the recommended values. We provided a module-level overview of the BPF-DAG architecture in Figure 4, a detailed layer-level description in Table III, showing the input/output dimensions and parameter counts for each neural network layer.

![](images/5336b45b14d0c742aa7eedaf9fa1f7c008aa899a8a24e17282913a38db5bc39e.jpg)  
Fig. 4. The module-level overview of BPF-DAG.

To evaluate and compare the classification performance of our method, we utilize the four key metrics: Accuracy (AC), Precision (PR), Recall (RC), and F1-score (F1). They are calculated as shown below.

$$
A c c u r a c y = \frac {T P + T N}{T P + T N + F P + F N}\tag{18}
$$

$$
R e c a l l = \frac {T P}{T P + F N}\tag{19}
$$

$$
P r e c i s i o n = \frac {T P}{T P + F P}\tag{20}
$$

$$
F 1 = 2 \times \frac {\text {Recall} \times \text {Precision}}{\text {Recall} + \text {Precision}}\tag{21}
$$

where TP, FP, TN, and FN represent true positive, false positive, true negative, and false negative, respectively. Considering the imbalanced class distribution of trafic types, macro averaging is applied to calculate the mean values of Accuracy, Precision, Recall, and F1-score in this paper.

$$
M a c r o _ {a v e r a g e} = \frac {1}{k} \sum_ {i = 1} ^ {k} m _ {i}\tag{22}
$$

where m is the classification metric, $m _ { i }$ is the value of classification metric m of class i, and k is the total number of trafic categories.

TABLE V  
EXPERIMENTAL RESULTS ON PUBLIC ISCX VPN-NONVPN DATASETS

<table><tr><td rowspan="2">Category</td><td rowspan="2">Model</td><td colspan="4">ISCX-VPN</td><td colspan="4">ISCX-nonVPN</td></tr><tr><td>AC</td><td>RC</td><td>PR</td><td>F1</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td></tr><tr><td rowspan="2">ML-based Methods</td><td>AppScanner [12]</td><td>0.7490</td><td>0.6138</td><td>0.7153</td><td>0.6176</td><td>0.7140</td><td>0.6406</td><td>0.7298</td><td>0.6524</td></tr><tr><td>CUMUL [13]</td><td>0.6586</td><td>0.5682</td><td>0.6190</td><td>0.5797</td><td>0.6255</td><td>0.5041</td><td>0.5874</td><td>0.4984</td></tr><tr><td rowspan="6">DL-based Methods</td><td>1D-CNN [21]</td><td>0.9540</td><td>0.9313</td><td>0.9472</td><td>0.9387</td><td>0.8483</td><td>0.7910</td><td>0.8264</td><td>0.8042</td></tr><tr><td>2D-CNN [42]</td><td>0.8636</td><td>0.8143</td><td>0.8594</td><td>0.8324</td><td>0.8390</td><td>0.7951</td><td>0.8206</td><td>0.8059</td></tr><tr><td>HAST [43]</td><td>0.9597</td><td>0.9452</td><td>0.9526</td><td>0.9489</td><td>0.8914</td><td>0.8542</td><td>0.8781</td><td>0.8660</td></tr><tr><td>TSCRNN [25]</td><td>0.9535</td><td>0.9439</td><td>0.9416</td><td>0.9424</td><td>0.8471</td><td>0.8069</td><td>0.8120</td><td>0.8089</td></tr><tr><td>ET-BERT [34]</td><td>0.9762</td><td>0.9631</td><td>0.9676</td><td>0.9653</td><td>0.9407</td><td>0.9201</td><td>0.9348</td><td>0.9267</td></tr><tr><td>YaTC [33]</td><td>0.9851</td><td>0.9851</td><td>0.9855</td><td>0.9852</td><td>0.9511</td><td>0.8978</td><td>0.9332</td><td>0.9139</td></tr><tr><td rowspan="3">GNN-based Methods</td><td>E-GraphSAGE [36]</td><td>0.7585</td><td>0.7245</td><td>0.7285</td><td>0.7259</td><td>0.5215</td><td>0.5215</td><td>0.5379</td><td>0.5158</td></tr><tr><td>TFE-GNN [38]</td><td>0.9598</td><td>0.9456</td><td>0.9627</td><td>0.9529</td><td>0.9421</td><td>0.9229</td><td>0.9334</td><td>0.9267</td></tr><tr><td>Ours</td><td>0.9912</td><td>0.9865</td><td>0.9895</td><td>0.9879</td><td>0.9637</td><td>0.9327</td><td>0.9448</td><td>0.9382</td></tr></table>

TABLE VI

EXPERIMENTAL RESULTS ON PUBLIC ISCX TOR-NONTOR DATASETS

<table><tr><td colspan="6">ISCX-Tor</td><td colspan="4">ISCX-nonTor</td></tr><tr><td>Category</td><td>Model</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td></tr><tr><td rowspan="2">ML-based Methods</td><td>AppScanner [12]</td><td>0.6529</td><td>0.5014</td><td>0.6457</td><td>0.4800</td><td>0.7288</td><td>0.5699</td><td>0.6566</td><td>0.6102</td></tr><tr><td>CUMUL [13]</td><td>0.5728</td><td>0.4273</td><td>0.4120</td><td>0.3974</td><td>0.6523</td><td>0.5123</td><td>0.6015</td><td>0.5533</td></tr><tr><td rowspan="6">DL-based Methods</td><td>1D-CNN [21]</td><td>0.9336</td><td>0.9217</td><td>0.9330</td><td>0.9268</td><td>0.9380</td><td>0.8342</td><td>0.8779</td><td>0.8538</td></tr><tr><td>2D-CNN [42]</td><td>0.9336</td><td>0.9220</td><td>0.9239</td><td>0.9221</td><td>0.9253</td><td>0.7864</td><td>0.8435</td><td>0.8109</td></tr><tr><td>HAST [43]</td><td>0.9502</td><td>0.9401</td><td>0.9474</td><td>0.9437</td><td>0.9583</td><td>0.8530</td><td>0.9024</td><td>0.8770</td></tr><tr><td>TSCRNN [25]</td><td>0.9483</td><td>0.9392</td><td>0.9400</td><td>0.9386</td><td>0.9503</td><td>0.8513</td><td>0.8938</td><td>0.8721</td></tr><tr><td>ET-BERT [34]</td><td>0.9561</td><td>0.9247</td><td>0.9457</td><td>0.9339</td><td>0.9732</td><td>0.9244</td><td>0.9398</td><td>0.9320</td></tr><tr><td>YaTC [33]</td><td>0.9497</td><td>0.9368</td><td>0.9474</td><td>0.9400</td><td>0.9776</td><td>0.9297</td><td>0.9528</td><td>0.9402</td></tr><tr><td rowspan="3">GNN-based Methods</td><td>E-GraphSAGE [36]</td><td>0.4647</td><td>0.3866</td><td>0.4502</td><td>0.3717</td><td>0.5764</td><td>0.5764</td><td>0.5729</td><td>0.5659</td></tr><tr><td>TFE-GNN [38]</td><td>0.9163</td><td>0.8712</td><td>0.9195</td><td>0.8832</td><td>0.9756</td><td>0.9421</td><td>0.9524</td><td>0.9471</td></tr><tr><td>Ours</td><td>0.9797</td><td>0.9739</td><td>0.9772</td><td>0.9749</td><td>0.9795</td><td>0.9452</td><td>0.9558</td><td>0.9501</td></tr></table>

## B. Comparison With SOTA Methods

We compare BPF-DAG with a range of baselines and state-of-the-art (SOTA) methods, including (1) ML-based methods: AppScanner [12], CUMUL [13]; (2) DL-based methods: 1D-CNN [21], 2D-CNN [42], TSCRNN [25], HAST [43]; (3) pretraining-based methods: ET-BERT [34], YaTC [33]; (4) GNN-based methods: E-GraphSAGE [36], TFE-GNN [38].

From the comparison results shown in Table V, VI and VII, we can observe that BPF-DAG outperforms all baseline and SOTA methods across all datasets. The experimental results indicate that BPF-DAG outperforms existing SOTA methods by 1.4%, 1.2%, 2.3%, 0.2%, 7.7% and 3.1% in terms of accuracy.

ML-based methods in our experiments perform poorly, largely because they only use the packet length sequence as input features, instead of raw trafic bytes, which is not reliable for encrypted trafic classification. In our experimental setup, the number of packets in each flow is generally small, which is insuficient for ML-based methods to learn discriminative features.

SOTA pretraining-based methods like ET-BERT and YaTC perform well across the datasets. Encryption and anonymity techniques make it challenging for DL-based methods to analyze trafic payloads directly. Pretraining-based methods outperform other DL methods, underscoring the value of pretraining on large-scale trafic data. However, BPF-DAG achieves slightly higher accuracy than these pretraining methods, even without using trafic payloads or pretraining techniques. This highlights our method’s ability to avoid the computing overhead of pretraining while reducing the cost associated with processing payload bytes in each flow sample.

The performance of GNN-based methods, such as TFE-GNN and E-GraphSAGE, varies with their specific graph construction approaches. E-GraphSAGE relies on manually extracted statistical features to initialize edge attributes, lacking an end-to-end framework. Furthermore, its use of only a few low-dimensional statistical features limits its ability to capture discriminative features, resulting in less-than-ideal and unreliable performance. TFE-GNN constructs a byte-level traffic graph where raw bytes are converted into nodes. However, it treats each flow independently, without considering flowlevel interaction patterns, which is not reliable enough. In contrast, BPF-DAG eficiently integrates byte-level, packetlevel and flow-level trafic features, enabling a more reliable and accurate framework.

Figure 5 and 6 present the visualization of normal and normalized confusion matrices on all ISCX datasets, respectively. From the normal confusion matrices, it is clear that the distribution of diferent trafic types within each dataset is imbalanced, especially in the ISCX-nonTor dataset. Despite the imbalance, BPF-DAG delivers satisfactory classification results across all datasets. Additionally, although the ISCX-Tor dataset has considerably fewer samples compared to the others, BPF-DAG outperforms SOTA methods by a significant margin.

TABLE VII  
EXPERIMENTAL RESULTS ON MIRAGE-2019 AND MIRAGE-2024 DATASETS

<table><tr><td colspan="6">MIRAGE-2019</td><td colspan="4">MIRAGE-2024</td></tr><tr><td>Category</td><td>Model</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td></tr><tr><td rowspan="2">ML-basedMethods</td><td>AppScanner [12]</td><td>0.6503</td><td>0.5820</td><td>0.6722</td><td>0.6239</td><td>0.5792</td><td>0.5162</td><td>0.5761</td><td>0.5445</td></tr><tr><td>CUMUL [13]</td><td>0.5955</td><td>0.5209</td><td>0.6056</td><td>0.5601</td><td>0.5573</td><td>0.449</td><td>0.5758</td><td>0.5046</td></tr><tr><td rowspan="6">DL-basedMethods</td><td>1D-CNN [21]</td><td>0.7276</td><td>0.6820</td><td>0.6956</td><td>0.6887</td><td>0.7066</td><td>0.6888</td><td>0.7442</td><td>0.7154</td></tr><tr><td>2D-CNN [42]</td><td>0.6950</td><td>0.6440</td><td>0.6796</td><td>0.6613</td><td>0.6863</td><td>0.6606</td><td>0.7336</td><td>0.6952</td></tr><tr><td>HAST [43]</td><td>0.7442</td><td>0.6935</td><td>0.707</td><td>0.7002</td><td>0.6995</td><td>0.6648</td><td>0.7127</td><td>0.6879</td></tr><tr><td>TSCRNN [25]</td><td>0.7457</td><td>0.7003</td><td>0.7028</td><td>0.7015</td><td>0.7220</td><td>0.7031</td><td>0.7428</td><td>0.7224</td></tr><tr><td>ET-BERT [34]</td><td>0.7140</td><td>0.6600</td><td>0.7502</td><td>0.7022</td><td>0.7500</td><td>0.7045</td><td>0.7154</td><td>0.7099</td></tr><tr><td>YaTC [33]</td><td>0.8314</td><td>0.7944</td><td>0.8225</td><td>0.8082</td><td>0.7935</td><td>0.7728</td><td>0.8192</td><td>0.7953</td></tr><tr><td rowspan="3">GNN-basedMethods</td><td>E-GraphSAGE [36]</td><td>0.7033</td><td>0.6352</td><td>0.6897</td><td>0.6614</td><td>0.6642</td><td>0.5760</td><td>0.6627</td><td>0.6163</td></tr><tr><td>TFE-GNN [38]</td><td>0.7558</td><td>0.7041</td><td>0.7688</td><td>0.7350</td><td>0.7345</td><td>0.6896</td><td>0.7272</td><td>0.7079</td></tr><tr><td>Ours</td><td>0.9083</td><td>0.8929</td><td>0.8999</td><td>0.8964</td><td>0.8247</td><td>0.7988</td><td>0.8400</td><td>0.8189</td></tr></table>

![](images/73319b377f8ba73d02e20d6b9b08c19fadd9f57a58c9d1cea2156665b8a44b80.jpg)  
(a) ISCX-VPN

![](images/f89828d502db5f0f1ddc85705ea61be5ea94e9f0550f5209a4ca5405be29b1d6.jpg)  
(b) ISCX-nonVPN

![](images/3b8fa45bfb95c43bf2a38e7e570d99138598812619ba6b2671bc9478a8771ada.jpg)  
(c) ISCX-Tor

![](images/d6f4072d86cca71b8b78b40ad107c1f0ea7ccde7d9cab330ceb0adaf7f573f08.jpg)  
(d) ISCX-nonTor

Fig. 5. Confusion matrices of BPF-DAG on four datasets.  
![](images/c14489470cb38539f6129a00dcc0d4e165d33f6cebd51d31f4ec7b53723e43db.jpg)  
(a) ISCX-VPN

![](images/daf9565f25488d2db819c0ed433339fe40feb16edb32ac34e172e454dbc9e44b.jpg)  
(b) ISCX-nonVPN

![](images/3e3e98c014fa6bdc41d900641cdc157027e63ae8e980082c9191eb0d5c296518.jpg)  
(c) ISCX-Tor

![](images/0057c617ccd51f323f582f8e7412c8cc9f90dce85c86d4f7b79d025481e9a648.jpg)  
(d) ISCX-nonTor  
Fig. 6. Normalized confusion matrices of BPF-DAG on four datasets.

## C. Ablation Studies

To further assess the contribution of each component in BPF-DAG and verify the reliability of our method, we perform an ablation study on the ISCX-VPN dataset. The results are presented in Table VIII. We denote the extraction of temporal trafic information as $\mathbf { \hat { \Omega } } ^ { \ast } \mathbf { T } ^ { \ast }$ and topological trafic information as $\mathbf { \partial } ^ { 6 } \mathbf { S } ^ { \prime }$ . More specifically, ‘w/o $\mathrm { T } ^ { \bullet }$ in Table VIII refers to the setup where trafic’s statistical features are used to initialize the graph attributes instead of automatically extracting temporal features. This evaluates the impact of the packet-level temporal features and byte-level raw information. ‘w/o $s '$ refers to extracting temporal features from each flow independently, without considering the topological relationships among flows.

TABLE VIII  
ABLATION STUDY OF BPF-DAG ON ISCX-VPN DATASETS

<table><tr><td>Model</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td></tr><tr><td>Ours w/o T</td><td>0.8440</td><td>0.7778</td><td>0.8414</td><td>0.7940</td></tr><tr><td>Ours w/o S</td><td>0.9793</td><td>0.9686</td><td>0.9669</td><td>0.9676</td></tr><tr><td>w AttnLSTM</td><td>0.9886</td><td>0.9876</td><td>0.9826</td><td>0.9846</td></tr><tr><td>w CNN</td><td>0.9587</td><td>0.9315</td><td>0.9500</td><td>0.9387</td></tr><tr><td>w Concatenation</td><td>0.9742</td><td>0.9623</td><td>0.9616</td><td>0.9617</td></tr><tr><td>w Average</td><td>0.9587</td><td>0.9534</td><td>0.9391</td><td>0.9457</td></tr><tr><td>Ours(default)</td><td>0.9912</td><td>0.9865</td><td>0.9895</td><td>0.9879</td></tr></table>

![](images/c9c52e27d729aa335775114a09fd537eee4acc2f6f84a3c0b62f05ee9530df46.jpg)  
(a) ISCX-VPN

![](images/7afd0178ee85ca385dee583437d774b6107b8c57bfa1407f07678391019de706.jpg)  
(b) ISCX-nonVPN

![](images/0efd12128d1617d3cdad7a6edc482b18e5175d0c3fd309a6c60a0ccb437e8d70.jpg)  
(c) ISCX-Tor

![](images/a9f0f1226df914182de12ac3c32ca3958375fb42e23606205189b0444fb4b119.jpg)  
(d) ISCX-nonTor

Fig. 7. t-SNE Visualization of ablation study without using topological features on four datasets.  
![](images/4ddb60b1d008642be081c93c59dff42a2f9cae10c9d117d110515ba7bb4b3513.jpg)  
(a) ISCX-VPN

![](images/680b4ea749bca06c8892f149909a6a29aa592f11e6b8ec629dff5e0f6061b6f8.jpg)  
(b) ISCX-nonVPN

![](images/0f93cae01fe52c1ce0a2ab4663852d8ba4c424bf1b7cca0b2ba838d0625426cc.jpg)  
(c) ISCX-Tor

![](images/6d6342952c5dbea5661abd2130126489185368e0d32ee7b7cd5868beadda2d4b.jpg)  
(d) ISCX-nonTor  
Fig. 8. t-SNE Visualization of the proposed BPF-DAG method on four datasets.

This setup tests the impact of the flow-level features. Additionally, we assess the efectiveness of alternative temporal feature extractor and feature fusion operations, respectively. We replace the ‘Transformer’ module with ‘Attention-based LSTM’ (AttnLSTM) and ‘CNN’ module, to see how these different architectures afect performance in capturing temporal representations. We substitute the linear interpolation operation used to fuse temporal and topological representations with concatenation and average operations to decide the optimal fusion operation.

Based on the ablation study results, we can derive the following conclusions:

• Both temporal and topological information contribute to improving classification performance. In contrast to treating each flow as an isolated entity, fully leveraging and capturing interrelationship between flows helps improve accuracy. Moreover, automatic feature extraction from raw trafic outperforms traditional feature engineering. Automatic extraction not only eliminates the need for manually designing statistical features, but also increases accuracy and reliability of the model.

• Several operations for fusing temporal and topological features were tested, such as concatenation, average, and linear concatenation. The results show that linear interpolation is the most efective for combining the two representations.

The ‘AttnLSTM’ module provides classification accuracy comparable to the default Transformer module, indicating its ability to capture temporal features efectively. The CNN module, however, performs less efectively, likely because it lacks the capacity to capture the sequential, time-related dependencies.

To conclude, the ablation studies confirm that the bytelevel, packet-level and flow-level trafic features all contribute to the model’s accuracy and reliability. Besides, to visualize the improvement brought by flow-level topological features, we use t-distributed stochastic neighbor embedding (t-SNE) to map the final representations to a lower-dimensional space, both with and without topological features, and visualize them as two-dimensional images, as shown in Figure 7 and 8.

![](images/6213f03e6acaf6c5960ccaad66f7354068e3e019cf722c24e6515425539b527f.jpg)  
(a) ISCX-VPN

![](images/085b2e6316847f143437adb23202f69516863662b51fe477e8604f919f49a8c9.jpg)  
(b) ISCX-Tor  
Fig. 9. Comparison results in few-shot settings on ISCX-VPN and ISCX-Tor datasets.

## D. Few-Shot Analysis

To evaluate the performance of BPF-DAG in few-shot scenarios, we designed comparison experiments using varied proportions of data on the ISCX-VPN and ISCX-Tor datasets. Specifically, we randomly selected 10%, 40%, and 70% of the original training samples and conducted classification under the same conditions. We compared BPF-DAG with several baselines as well as SOTA methods, with the comparsion results presented in Figure 9.

The results show that BPF-DAG is the least afected by reduced training data and consistently outperforms other methods across all data proportions. In contrast, common deep learning-based methods (e.g., 1D-CNN, 2D-CNN, TSCRNN) sufer significant performance degradation when the proportion of training data is reduced to 10%. However, the pretraining-based method YaTC is relatively more robust due to its pretraining on large-scale unlabeled data.

TABLE IX  
MODEL FLOPS AND PARAMETERS

<table><tr><td>Model</td><td>Parameters (M)</td><td>FLOPs (M)</td></tr><tr><td>1D-CNN</td><td>3.7E+00</td><td>1.3E+01</td></tr><tr><td>2D-CNN</td><td>2.2E-01</td><td>6.9E+00</td></tr><tr><td>TSCRNN</td><td>8.5E-01</td><td>4.3E+01</td></tr><tr><td>HAST</td><td>4.7E-01</td><td>3.3E+02</td></tr><tr><td>TFE-GNN</td><td>4.4E+01</td><td>2.2E+03</td></tr><tr><td>ET-BERT</td><td>8.6E+01</td><td>1.1E+04</td></tr><tr><td>YaTC</td><td>1.8E+01</td><td>9.1E+02</td></tr><tr><td>BPF-DAG</td><td>1.3E+01</td><td>8.1E+02</td></tr></table>

The strong performance of BPF-DAG in few-shot settings can be attributed to the use of GNNs, which reinforce the interconnected patterns of network flows through message passing in the graph structure. This message-passing mechanism allows BPF-DAG to capture relationships between flows, making it more resilient to limited training data.

## E. Complexity Analysis

To thoroughly assess the trade-of between performance and complexity, we calculate the floating point operations (FLOPs) and model parameter size for both our method and the comparison methods. As shown in Table IX, our model’ s FLOPs and parameter size are approximately 11% and 28% lower, respectively, than those of the SOTA methods.

According to Tables V and VI, it is concluded that BPF-DAG provides a significant performance improvement with tolerable model complexity. While BPF-DAG has higher computational complexity than traditional DL-based methods due to its use of GNN, it delivers superior accuracy. Conversely, although pre-training methods like ET-BERT produce similar classification results to BPF-DAG, their FLOPs and model parameters are several times higher than it. Besides, the pretraining process is time-consuming and excessively high computational complexity is not suitable for real-time trafic detection. To sum up, the computational complexity of BPF-DAG is slightly higher than some classical methods, but it achieves better classification performance compared to SOTA methods.

## F. Parameter Sensitivity Analysis

In this part, we analyze how the classification performance is afected by the sensitivity of two crucial hyperparameters, i.e., the interpolation coeficient $\mu$ and raw byte length m.

1) The Impact of Interpolation Coeficient $\mu .$ The interpolation coeficient $\mu$ controls the tradeof between the temporal representation and topological representation. $\mu = 0$ means only the temporal information of raw trafic is leveraged. When $0 ~ < ~ \mu ~ < ~ 1$ , the temporal and topological representations are fully fused and $\mu$ controls the balance between them. The value of $\mu$ for optimal classification performance is diferent for diferent trafic datasets. Figure 10(a) shows the F1-score results with $\mu$ ranging from 0 to 1 for ISCX-VPN, ISCX-Tor, MIRAGE2019 and MIRAGE2024 datasets.

![](images/33b8be454643e5368b2aa7f049c85247c6c05b9c4efe609a8db84825c8bcc8ce.jpg)  
(a) Interpolation coefficient $\mu$

![](images/4a59d804b9c7fe5d184c3c9604fec6f631cb5850f122dbcc1e4442d5c5a66d64.jpg)  
(b) Raw byte length m  
Fig. 10. Parameter Sensitivity Analysis w.r.t. interpolation coeficient and raw byte length on ISCX-VPN and ISCX-Tor datasets.

$\operatorname { A s } \mu$ increasing from zero, the F1-score consistently increases, which exactly reflects the efectiveness of features fusion. The results show that the optimal values of $\mu$ vary across datasets and do not follow an obvious pattern. Specifically, the optimal values are 0.9 and 0.8 for the ISCX-VPN and ISCX-Tor datasets, respectively, and 0.4 and 0.5 for the MIRAGE-2019 and MIRAGE-2024 datasets, respectively. In conclusion, we can state that appropriately incorporating flowlevel topological patterns into flow representations enables a significant improvement in classification performance.

2) The Impact of Raw Byte Length m: In our experiment, we truncate the first m bytes of each packet header to represent the raw packet. The value of m efects the tradeof between computational overhead and classification performance. From Figure 10(b), we can find that the appropriate range of m is from 50 to 60 and the degree of influence varies for diferent datasets. The decrease of m causes obvious performance degradation for Tor dataset, while the VPN dataset is less afected. To balance the performance and overhead, m is set to 60 for all ISCX datasets.

## VI. CONCLUSION

In this paper, we propose BPF-DAG, a byte-packet-flow features fusion-based reliable encrypted trafic classification method via dynamic attributed graph. This is the first method that integrates temporal packet relations into flow interaction patterns using raw-byte trafic as input, realizing byte-packetflow multi-granularity features fusion. By jointly training a GNN and Transformer, BPF-DAG extracts topological patterns from the flow interaction graph and temporal characteristics from raw byte-based packet sequences. We propose a novel multi-granularity features fusion strategy to fully integrate byte-level, packet-level and flow-level trafic features. During training, the temporal representations of flows are learned from packet sequences using the optimized Transformer after each epoch, and then corresponding directed edge attributes are updated with them. To reduce the memory overhead, we leverage a technique called Memory Bank to track all temporal representations to decouple the training batch size from the total number of edges. Our method has been extensively evaluated on four encrypted trafic datasets, and the experimental results demonstrate that BPF-DAG not only outperforms SOTA methods in terms of accuracy, but also exhibits relatively lower complexity. Furthermore, BPF-DAG exhibits strong performance in few-shot learning scenarios. Looking ahead, we plan to extend our multi-granularity features fusion strategy to unsupervised Intrusion Detection Systems to detect and identify malicious trafic in real-time.

## REFERENCES

[1] R. Sharma, S. Dangi, and P. Mishra, “A comprehensive review on encryption based open source cyber security tools,” in Proc. 6th Int. Conf. Signal Process., Comput. Control (ISPCC), Oct. 2021, pp. 614–619.

[2] E. Papadogiannaki and S. Ioannidis, “A survey on encrypted network trafic analysis applications, techniques, and countermeasures,” ACM Comput. Surv., vol. 54, no. 6, pp. 1–35, Jul. 2022.

[3] E. Ramadhani, “Anonymity communication VPN and tor: A comparative study,” J. Phys., Conf. Ser., vol. 983, Mar. 2018, Art. no. 012060.

[4] K. Thomas et al., “Data breaches, phishing, or malware? Understanding the risks of stolen credentials,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., Oct. 2017, pp. 1421–1434.

[5] G. Pellegrino, M. Johns, S. Koch, M. Backes, and C. Rossow, “Deemon: Detecting CSRF with dynamic analysis and property graphs,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., Oct. 2017, pp. 1757–1771.

[6] B. Anderson and D. McGrew, “Machine learning for encrypted malware trafic classification: Accounting for noisy labels and non-stationarity,” in Proc. 23rd ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining, Halifax, NS, Canada, Aug. 2017, pp. 1723–1732.

[7] T. Van Ede et al., “FlowPrint: Semi-supervised mobile-app fingerprinting on encrypted network trafic,” in Proc. Netw. Distrib. Syst. Secur. Symp. (NDSS), vol. 27, Feb. 2020, pp. 1–18.

[8] Q. Zhou, L. Wang, H. Zhu, T. Lu, and V. S. Sheng, “WF-transformer: Learning temporal features for accurate anonymous trafic identification by using transformer networks,” IEEE Trans. Inf. Forensics Security, vol. 19, pp. 30–43, 2024.

[9] Y. Mirsky, T. Doitshman, Y. Elovici, and A. Shabtai, “Kitsune: An ensemble of autoencoders for online network intrusion detection,” 2018, arXiv:1802.09089.

[10] M. Roesch et al., “Snort: Lightweight intrusion detection for networks,” Lisa, vol. 99, no. 1, pp. 229–238, 1999.

[11] V. Paxson, “Bro: A system for detecting network intruders in real-time,” Comput. Netw., vol. 31, nos. 23–24, pp. 2435–2463, Dec. 1999.

[12] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “AppScanner: Automatic fingerprinting of smartphone apps from encrypted network trafic,” in Proc. IEEE Eur. Symp. Secur. Privacy, Mar. 2016, pp. 439–454.

[13] A. Panchenko et al., “Website fingerprinting at internet scale,” in Proc. Netw. Distrib. Syst. Secur. Symp. (NDSS), vol. 1, 2016, p.23477.

[14] A. S. Jacobs, R. Beltiukov, W. Willinger, R. A. Ferreira, A. Gupta, and L. Z. Granville, “AI/ML for network security: The emperor has no clothes,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., Nov. 2022, pp. 1537–1551.

[15] J. Gu and S. Lu, “An efective intrusion detection approach using SVM with na¨ıve Bayes feature embedding,” Comput. Secur., vol. 103, Apr. 2021, Art. no. 102158.

[16] G. Aceto, D. Ciuonzo, A. Montieri, V. Persico, and A. Pescape, “AI-´ powered internet trafic classification: Past, present, and future,” IEEE Commun. Mag., vol. 62, no. 9, pp. 168–175, Sep. 2024.

[17] Z. Khodaverdian, H. Sadr, and S. A. Edalatpanah, “A shallow deep neural network for selection of migration candidate virtual machines to reduce energy consumption,” in Proc. 7th Int. Conf. Web Res. (ICWR), May 2021, pp. 191–196.

[18] H. Sadr, M. Nazari Soleimandarabi, and Z. Khodaverdian, “Automatic assessment of short answers based on computational and data mining approaches,” J. Decisions Oper. Res., vol. 6, no. 2, pp. 242–255, 2021.

[19] M. Nazari, H. Emami, R. Rabiei, A. Hosseini, and S. Rahmatizadeh, “Detection of cardiovascular diseases using data mining approaches: Application of an ensemble-based model,” Cognit. Comput., vol. 16, no. 5, pp. 2264–2278, Sep. 2024.

[20] H. Sadr, A. Salari, M. T. Ashoobi, and M. Nazari, “Cardiovascular disease diagnosis: A holistic approach using the integration of machine learning and deep learning models,” Eur. J. Med. Res., vol. 29, no. 1, p. 455, Sep. 2024.

[21] W. Wang, M. Zhu, J. Wang, X. Zeng, and Z. Yang, “End-to-end encrypted trafic classification with one-dimensional convolution neural networks,” in Proc. IEEE Int. Conf. Intell. Secur. Informat. (ISI), Jul. 2017, pp. 43–48.

[22] P. Sirinam, M. Imani, M. Juarez, and M. Wright, “Deep fingerprinting: Undermining website fingerprinting defenses with deep learning,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur. (CCS), Toronto, ON, Canada, Oct. 2018, pp. 1928–1943.

[23] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “FS-Net: A flow sequence network for encrypted trafic classification,” in Proc. IEEE INFOCOM Conf. Comput. Commun., Apr. 2019, pp. 1171–1179.

[24] M. Lopez-Martin, B. Carro, A. Sanchez-Esguevillas, and J. Lloret, “Network trafic classifier with convolutional and recurrent neural networks for Internet of Things,” IEEE Access, vol. 5, pp. 18042–18050, 2017.

[25] K. Lin, X. Xu, and H. Gao, “TSCRNN: A novel classification scheme of encrypted trafic based on flow spatiotemporal features for eficient management of IIoT,” Comput. Netw., vol. 190, May 2021, Art. no. 107974.

[26] G. Bovenzi et al., “Benchmarking class incremental learning in deep learning trafic classification,” IEEE Trans. Netw. Service Manage., vol. 21, no. 1, pp. 51–69, Feb. 2024.

[27] A. Nascita, A. Montieri, G. Aceto, D. Ciuonzo, V. Persico, and A. Pescape, “Improving performance, reliability, and feasibility in mul-´ timodal multitask trafic classification with XAI,” IEEE Trans. Netw. Service Manage., vol. 20, no. 2, pp. 1267–1289, Jun. 2023.

[28] T. N. Kipf and M. Welling, “Semi-supervised classification with graph convolutional networks,” 2016, arXiv:1609.02907.

[29] Y. Chen and Y. Wang, “MPAF: Encrypted trafic classification with multi-phase attribute fingerprint,” IEEE Trans. Inf. Forensics Security, vol. 19, pp. 7091–7105, 2024.

[30] P. Velickoviˇ c, G. Cucurull, A. Casanova, A. Romero, P. Li´ o, and´ Y. Bengio, “Graph attention networks,” 2017, arXiv:1710.10903.

[31] W. L. Hamilton, R. Ying, and J. Leskovec, “Inductive representation learning on large graphs,” in Proc. Adv. Neural Inf. Process. Syst., vol. 30, 2017, pp. 1024–1034.

[32] H. Shi, H. Li, D. Zhang, C. Cheng, and X. Cao, “An eficient feature generation approach based on deep learning and feature selection techniques for trafic classification,” Comput. Netw., vol. 132, pp. 81–98, Feb. 2018.

[33] R. Zhao et al., “Yet another trafic classifier: A masked autoencoder based trafic transformer with multi-level flow representation,” in Proc. AAAI Conf. Artif. Intell., 2023, vol. 37, no. 4, pp. 5420–5427.

[34] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “ET-BERT: A contextualized datagram representation with pre-training transformers for encrypted trafic classification,” in Proc. ACM Web Conf., Apr. 2022, pp. 633–642.

[35] X. Hu, W. Gao, G. Cheng, R. Li, Y. Zhou, and H. Wu, “Toward early and accurate network intrusion detection using graph embedding,” IEEE Trans. Inf. Forensics Security, vol. 18, pp. 5817–5831, 2023.

[36] W. W. Lo, S. Layeghy, M. Sarhan, M. Gallagher, and M. Portmann, “E-GraphSAGE: A graph neural network based intrusion detection system for IoT,” in Proc. IEEE/IFIP Netw. Oper. Manage. Symp., Budapest, Hungary, Apr. 2022, pp. 1–9.

[37] G. Duan, H. Lv, H. Wang, and G. Feng, “Application of a dynamic line graph neural network for intrusion detection with semisupervised learning,” IEEE Trans. Inf. Forensics Security, vol. 18, pp. 699–714, 2023.

[38] H. Zhang et al., “TFE-GNN: A temporal fusion encoder using graph neural networks for fine-grained encrypted trafic classification,” in Proc. ACM Web Conf., Apr. 2023, pp. 2066–2075.

[39] M. Wang, N. Yang, and N. Weng, “K-GetNID: Knowledge-guided graphs for early and transferable network intrusion detection,” IEEE Trans. Inf. Forensics Security, vol. 19, pp. 7147–7160, 2024.

[40] I. Akbari et al., “A look behind the curtain: Trafic classification in an increasingly encrypted web,” Proc. ACM Meas. Anal. Comput. Syst., vol. 5, no. 1, pp. 1–26, 2021.

[41] B. Anderson, S. Paul, and D. McGrew, “Deciphering malware’s use of TLS (without decryption),” J. Comput. Virol. Hacking Techn., vol. 14, no. 3, pp. 195–211, Aug. 2018.

[42] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware trafic classification using convolutional neural network for representation learning,” in Proc. Int. Conf. Inf. Netw. (ICOIN), Da Nang, Vietnam, Jan. 2017, pp. 712–717.

[43] W. Wang et al., “HAST-IDS: Learning hierarchical spatial–temporal features using deep neural networks to improve intrusion detection,” IEEE Access, vol. 6, pp. 1792–1806, 2018.

[44] A. Nascita, A. Montieri, G. Aceto, D. Ciuonzo, V. Persico, and A. Pescape, “XAI meets mobile tra´ fic classification: Understanding and improving multimodal deep learning architectures,” IEEE Trans. Netw. Service Manage., vol. 18, no. 4, pp. 4225–4246, Dec. 2021.

[45] G. Zhou, X. Guo, Z. Liu, T. Li, Q. Li, and K. Xu, “TraficFormer: An eficient pre-trained model for trafic data,” in Proc. IEEE Symp. Secur. Privacy (SP), May 2025, pp. 1844–1860.

[46] P. Lin, K. Ye, Y. Hu, Y. Lin, and C.-Z. Xu, “A novel multimodal deep learning framework for encrypted trafic classification,” IEEE/ACM Trans. Netw., vol. 31, no. 3, pp. 1369–1384, Jun. 2023.

[47] A. Vaswani et al., “Attention is all you need,” in Proc. Adv. Neural Inf. Process. Syst., vol. 30, 2025, pp. 5998–6008.

[48] A. Sriram, H. Jun, S. Satheesh, and A. Coates, “Cold fusion: Training Seq2Seq models together with language models,” 2017, arXiv:1708.06426.

[49] Z. Wu, Y. Xiong, S. X. Yu, and D. Lin, “Unsupervised feature learning via non-parametric instance discrimination,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., Jun. 2018, pp. 3733–3742.

[50] K. He, H. Fan, Y. Wu, S. Xie, and R. Girshick, “Momentum contrast for unsupervised visual representation learning,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2020, pp. 9729–9738.

[51] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of encrypted and VPN trafic using time-related,” in Proc. 2nd Int. Conf. Inf. Syst. Security Privacy (ICISSP), 2016, pp. 407–414.

[52] A. H. Lashkari, G. D. Gil, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of Tor trafic using time based features,” in Proc. 3rd Int. Conf. Inf. Syst. Secur. Privacy (ICISSP), Feb. 2017, pp. 253–262.

[53] G. Aceto, D. Ciuonzo, A. Montieri, V. Persico, and A. Pescape,´ “MIRAGE: Mobile-app trafic capture and ground-truth creation,” in Proc. 4th Int. Conf. Comput., Commun. Secur. (ICCCS), Oct. 2019, pp. 1–8.

[54] I. Guarino, D. Ciuonzo, A. Montieri, and A. Pescape, “Mirage-AppxAct-\` 2024: A novel dataset for mobile app and activity trafic analysis,” in Proc. 20th Int. Conf. Wireless Mobile Comput., Netw. Commun. (WiMob), Oct. 2024, pp. 663–666.

![](images/65c38add6a16e76c2138fbcd7f1584e88645506f9cae2c29eaef642f052cd2bc.jpg)  
Yunxiao Shi (Student Member, IEEE) received the B.S. degree in communication engineering from Nanjing University of Posts and Telecommunications, Nanjing, China, in 2023. He is currently pursuing the Ph.D. degree with the School of Electronic Information and Electrical Engineering, Shanghai Jiao Tong University, Shanghai, China. His research interests include encrypted trafic classification, intrusion detection systems, and machine learning for cyber security.

![](images/ee2c69bd18f96c8bd62829d51e62d2e793e5667ae45752cfe270f149ea28d53e.jpg)

Gaolei Li (Member, IEEE) is currently an Associate Professor with the School of Electronic Information and Electrical Engineering, Shanghai Jiao Tong University, Shanghai, China. He has published more than 100 papers, including IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY (IEEE TIFS), IEEE TRANSACTIONS ON DEPEND-ABLE AND SECURE COMPUTING (IEEE TDSC), NDSS, ACM CCS, ACM MM, and AAAI. His research interests include machine learning security and privacy-preserving. He has obtained many

awards, including the Outstanding Paper Award of IEEE ISPA 2024, the Third Prize of Science and Technology Progress Award of China Electric Power Development Acceleration Committee in 2024, the Best Conference Paper Award of China Cryptology Society in 2020, and the Best Conference Paper Award of IEEE CSIM Committee in 2018. He also served as a TPC member for CVPR 2024–2025, AAAI 2023&2024&2025, ACM MM 2023&2024&2025, and ICLR 2025. Besides, he also serves a reviewer for IEEE TIFS, IEEE TDSC, IEEE TRANSACTIONS ON MOBILE COMPUTING, IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS. IEEE/ACM TRANSACTIONS ON NETWORKING, IEEE TRANSACTIONS ON SERVICES COMPUTING, IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARN-ING SYSTEMS, and IEEE TRANSACTIONS ON GREEN COMMUNICATIONS AND NETWORKING.

![](images/84e3d5dbbdd30a4ac19cceeaea743c3a13eaca02a00ec22c2d9e800ec8cbd34e.jpg)

Jun Wu (Senior Member, IEEE) received the Ph.D. degree in information and telecommunication studies from Waseda University, Japan, in 2011. He was a Post-Doctoral Researcher with the Research Institute for Secure Systems, National Institute of Advanced Industrial Science and Technology (AIST), Japan, from 2011 to 2012. He was a Researcher with the Global Information and Telecommunication Institute, Waseda University, from 2011 to 2013. He is currently a Professor with the School of Electronic Information and Electrical Engineering, Shanghai

Jiao Tong University, China. He is also the Dean of the Institute of Cyber Science and Technology and the Vice Director of the National Engineering Research Center for Information Content Analysis Technology, Shanghai Jiao Tong University. He has hosted and participated in a lot of research projects, including the National Natural Science Foundation of China (NFSC), the National 863 Plan and 973 Plan of China, and Japan Society of the Promotion of Science Projects (JSPS). His research interests include the intelligence and security techniques of artificial intelligence, the Internet of Things (IoT), 5G/6G, and molecular communication. He has been the Track Chair of VTC 2019 and VTC 2020 and a TPC Member of more than ten international conferences, including ICC and GLOBECOM. He is the Chair of the IEEE P21451-1-5 Standard Working Group. He has been a Guest Editor of IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS, IEEE TRANSACTIONS ON INTELLIGENT TRANSPORTATION SYSTEMS, IEEE SENSORS JOURNAL, and Sensors. He is an Associate Editor of the IEEE SYSTEMS JOURNAL and IEEE NETWORKING LETTERS.

![](images/1cbccf8aa1bd829646c954efb3e7c357a157c0501fb1d449fdc90aba60101243.jpg)

Jianhua Li (Senior Member, IEEE) is currently a Professor/Ph.D. Supervisor and the Dean of the Institute of Cyber Science and Technology, Shanghai Jiao Tong University, Shanghai, China. He is also the Director of the National Engineering Laboratory for Information Content Analysis Technology and the Engineering Research Center for Network Information Security Management and Service of Chinese Ministry of Education. He has published more than 400 papers, including IEEE TRANSACTIONS ON DEPENDABLE AND SECURE COMPUTING, IEEE

TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY, IEEE TRANSACTIONS ON MOBILE COMPUTING, IEEE TRANSACTIONS ON EMERGING TOPICS IN COMPUTATIONAL INTELLIGENCE, ACM CCS, ACM MobiHoc, IEEE Infocom, and IEEE Globecom. He has published six books and has about 20 patents. He made three standards and has five software copyrights. His research interests include information security, signal processing, and computer network communication. He has got many awards, including the Second Prize of National Technology Progress Award of China in 2005, the First Prize of Science and Technology Progress Award of the Ministry of Education, the First Prize of Science and Technology Progress Award of Shanghai, the IEEE CSIM Committee Best Paper Award in 2016, the IEEE TETC Best Paper Award in 2017, and the ESI Highly Cited Scientist from 2022 to 2024.

![](images/81af54655c511b762013b6cb7299fbd92e9381873ebcf2b6a38f95d961ee5560.jpg)

He Fang (Member, IEEE) received the Ph.D. degree in electrical and computer engineering from Western University, Canada, in 2020. She is currently a Full Professor with Fujian Normal University, China. Her research interests include intelligent security provision and trust management. She has over 60 peer-reviewed journals and conference papers, and won the Best Paper Award from IEEE GLOBECOM 2023. She serves as an Associate Editor for several journals, including IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY and

China Communications. She was also involved in many IEEE conferences as the track chair or the session chair.
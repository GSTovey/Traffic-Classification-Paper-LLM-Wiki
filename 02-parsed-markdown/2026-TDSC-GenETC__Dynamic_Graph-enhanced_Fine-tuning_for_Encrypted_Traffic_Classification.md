# GenETC: Dynamic Graph-enhanced Fine-tuning for Encrypted Traffic Classification

Yunxiao Shi, Member, IEEE, Gaolei Li, Member, IEEE, Jun Wu, Senior Member, IEEE, Jianhua Li, Senior Member, IEEE, Yibin Zhou, Member, IEEE and Wanlei Zhou, Fellow, IEEE

Abstract—Encrypted traffic classification is crucial for adapting to diverse traffic patterns and evolving encryption technologies. However, current methods typically operate in isolation: pre-training methods excel at capturing byte-level semantics but overlook network topology, while graph-based methods capture interaction patterns but rely on hand-crafted statistical features as edge attributes. This reliance on statistical features limits the GNN’s ability to comprehend the complex, obfuscated semantics of modern encrypted traffic. To bridge this gap, we propose GenETC, a unified framework that integrates the generalization strength of traffic pre-training with the structural learning of dynamic graphs. Unlike naive combinations that might perform feature extraction and graph learning sequentially, GenETC introduces a dynamic graph updating strategy. Enabled by a Memory Bank mechanism, this strategy allows edge attributes to be iteratively refined by the pre-trained encoder during joint fine-tuning, realizing the co-evolution of semantic and topological representations. To our knowledge, GenETC is the first method to integrate deep pre-trained flow representations into a dynamic graph learning framework. To verify its effectiveness and transferability, we fine-tune it with a small amount of labeled data across various downstream traffic-specific tasks under a topologyavailable transductive setting. Extensive experiments demonstrate that GenETC achieves state-of-the-art performance across six datasets, with F1-score improvements ranging from approximately 1.1% to 22.7%, particularly delivering substantial gains in highly obfuscated scenarios such as malicious and IoT traffic. Our code is available at https://github.com/SYX0817/GenETC.

Index Terms—Encrypted traffic classification, pre-training, graph neural network, fine-tuning, dynamic graph neural networks.

## I. INTRODUCTION

ODAY, traffic encryption is widely adopted to ensure secure transmissions and safeguard user privacy [1]. Since 2019, the adoption of HTTPS has surpassed 90% across the web [2]. Encryption technologies can thwart information interception and guarantee data integrity. However, the ciphersuite for this purpose is a double-edged sword. Cybercriminals tend to abuse encrypted technologies to conceal their malicious behaviors, such as data exfiltration, malware infections, and botnet attacks [3]–[6]. Encrypted traffic classification is an essential task in the field of cybersecurity, serving as the basis for several traffic-specific tasks such as application identification [7], malicious intrusion detection [8] and website fingerprinting [9]. Generalizable encrypted traffic classification can adapt well to diverse traffic patterns and new environments, which is crucial for improving detection accuracy and robustness.

The adoption of encryption protocols significantly curtailed the sufficient exploitation of traffic information. Traditional rule-based methods, such as deep packet inspection (DPI) [10], [11], are no longer effective when confronted with encrypted payloads. In recent years, a range of machine learning (ML)- based methods have demonstrated satisfactory performance in encrypted traffic classification [9], [12]–[14]. ML-based methods typically involve two steps: first, extracting hand-crafted statistical features, followed by utilizing traditional machine learning models, such as support vector machines (SVM) and random forests. However, the feature extraction process is time-consuming and heavily dependent on expert knowledge. With the rapid advancement of Artificial Intelligence (AI), deep learning (DL)-based methods have been proposed and have shown excellent performance, as they can automatically extract latent features from raw traffic data [15]–[21]. DLbased methods typically transform traffic data into imagelike or natural language formats, allowing for the extensive application of computer vision (CV) and natural language processing (NLP) technologies. Recently, pre-training models have been applied to encrypted traffic classification and have demonstrated excellent performance. They pre-train on large amounts of unlabeled traffic data, learning transferable contextualized representations that improve generalization and accuracy [22]–[24]. Such representations can be easily transferred to the downstream tasks by fine-tuning on a limited amount of labeled data. However, these methods typically treat flows as isolated sequences, failing to exploit the latent topological patterns in host-to-host communications. Neglecting these interaction patterns limits the upper bound of detection precision.

Recently, graph neural networks (GNNs) [25]–[31] have attracted extensive attention for their powerful ability to represent graphs, leading to breakthroughs in fields such as chemistry, physical systems and social networks, among others. GNNs are capable of capturing latent topological patterns via message passing between nodes or edges of a graph. Therefore, graph neural network-based methods have been increasingly applied to encrypted traffic classification in recent years. One common GNN-based method is to construct a global communication graph, where IP addresses are modeled as nodes and traffic flows between hosts are represented as edges. It attempts to capture topological interaction patterns among various flows. Yet, these approaches heavily rely on static feature engineering to initialize graph attributes, thereby failing to extract the rich, deep semantics embedded in raw traffic bytes.

![](images/c54fa762e30f06b3a77a3455356e707dc54ced52c2be8f21db0cb3caa61dd994.jpg)  
Fig. 1: Comparison of existing paradigms and GenETC. (a) Pre-training methods lack flow interactions. (b) GNN-based methods lack learnable semantics. (c) GenETC unifies both via dynamic co-evolution.

However, as illustrated in Fig. 1, current research exhibits a distinct dichotomy. On one hand, pre-training methods leverage large-scale unlabeled data to learn powerful semantic representations from raw bytes, yet they analyze flows in isolation, ignoring the global network topology. On the other hand, graph-based methods effectively capture host interaction patterns but typically rely on feature engineering to initialize edge attributes. These hand-crafted statistical features (e.g., duration, throughput) are often insufficient to characterize the subtle behaviors of advanced encryption protocols or obfuscated malware [32].

To overcome these limitations, we propose GenETC, a model that unifies the semantic power of pre-training with the structural insights of graph neural networks. A key challenge in this unification is how to effectively fuse these two paradigms. A straightforward approach might be to extract static features from a pre-trained model to initialize the graph, but this creates a ”static coupling” where the feature extractor cannot adapt to topological feedback. Instead, GenETC employs a joint fine-tuning mechanism where the GNN backpropagates structural information to update the BERT-based flow representations dynamically. We replace the traditional statistical feature initialization with learnable, evolving representations derived directly from raw bytes.

In summary, the key contributions of our work are outlined as follows:

• We propose GenETC, an encrypted traffic classification framework that unifies the generalization capability of pretraining and structural learning of dynamic graphs. Unlike prior works that rely on static feature transfer, GenETC establishes a dynamic feedback loop, allowing flow semantics and topological patterns to co-evolve end-to-end.

• For the fine-tuning stage, we propose a dynamic graph updating strategy where edge attributes are iteratively refined using ever-optimized flow representations in a transductive setting. To enable this memory-intensive joint optimization, we leverage a Memory Bank mechanism to decouple the training batch size from the global graph structure.

• For the pre-training stage, two unsupervised tasks are designed to learn generic flow representations: Masked Byte Model (MBM) and Bidirectional Flow Association (BFA). The BFA task is specifically designed to capture the inherent bidirectional correlations within network sessions.

• GenETC has demonstrated outstanding generalizability under limited-data setups across various encryption scenarios, achieving state-of-the-art performance on six encrypted traffic classification tasks and significantly outperforming existing methods, with F1-score improvements ranging from 1.1% to 22.7%.

The remainder of this paper is organized as follows: Section II reviews related work. Section III outlines the preliminaries. Section IV details the proposed GenETC framework and its three key modules. Section V presents the experimental evaluation, including baseline comparisons, ablation studies, visualizations, and scalability analysis. Section VI discusses the limitations of our model. Finally, Section VII concludes the paper.

## II. RELATED WORK

## A. ML-based methods

ML-based methods typically consist of two stages: feature engineering and model training. Feature engineering refers to manually extracting statistical features from raw traffic, such as mean packet length, duration, etc. These features are then used as input for ML models to obtain final classification results. Appscanner [12] takes raw packet lengths of flows and their statistical properties as input features, and then pass them on to Random Forest as well as SVM classifier for real-time identification of Android apps. FlowPrint [7] selects the highest ranked features using Adjusted Mutual Information (AMI) and builds a fingerprint database by leveraging cross-correlation and clustering techniques, for efficient fingerprint generation and traffic classification. CUMUL [9] samples 104 intuitive features from the cumulative behavioral representations of Tor traces and performs better in terms of detection accuracy while being computationally more efficient. However, ML-based methods rely heavily on expert-designed statistical features, which is time-consuming and fails to fully leverage raw traffic bytes.

## B. DL-based methods

DL-based methods can automatically extract features from raw traffic bytes, enabling a unified end-to-end framework.

TABLE I: Summary of Existing Encrypted Traffic Classification Approaches

<table><tr><td>Category</td><td>Typical Methods</td><td>Raw bytes-based</td><td>Pre-training</td><td>Global Topology</td><td>Minibatch Training</td><td>Few-shot Setting</td></tr><tr><td rowspan="2">ML-based Methods</td><td>Appscanner [12]</td><td>×</td><td>×</td><td>×</td><td>√</td><td>×</td></tr><tr><td>CUMUL [9]</td><td>×</td><td>×</td><td>×</td><td>√</td><td>×</td></tr><tr><td rowspan="4">DL-based Methods</td><td>TSCRNN [19]</td><td>√</td><td>×</td><td>×</td><td>√</td><td>×</td></tr><tr><td>ET-BERT [22]</td><td>√</td><td>√</td><td>×</td><td>√</td><td>√</td></tr><tr><td>YaTC [23]</td><td>√</td><td>√</td><td>×</td><td>√</td><td>√</td></tr><tr><td>TrafficFormer [33]</td><td>√</td><td>√</td><td>×</td><td>√</td><td>√</td></tr><tr><td rowspan="5">GNN-based Methods</td><td>GraphDApp [34]</td><td>√</td><td>×</td><td>×</td><td>√</td><td>×</td></tr><tr><td>E-GraphSAGE [35]</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td></tr><tr><td>DLGNN [36]</td><td>√</td><td>×</td><td>√</td><td>×</td><td>√</td></tr><tr><td>TFE-GNN [37]</td><td>√</td><td>×</td><td>×</td><td>√</td><td>×</td></tr><tr><td>HyperVision [38]</td><td>×</td><td>×</td><td>√</td><td>√</td><td>×</td></tr><tr><td></td><td>GenETC(Ours)</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td></tr></table>

Wang et al. [15], [39] were the first to apply representation learning to traffic classification by transforming raw traffic into grayscale images and utilizing convolutional neural networks (CNNs) to perform image classification. Building on this, some works [18], [19], [40] have combined CNNs with RNNs to capture temporal characteristics from time-related raw packet sequences. Other methods, such as DF [16] and FS-Net [17], employ DL models to extract sequential features from raw packet length sequences.

A key advantage of pre-training is its strong generalizability, enabling models to learn universal traffic representations adaptable to diverse downstream tasks. Recent studies have shown its great potential in encrypted traffic analysis, especially when labeled data are limited. Pre-training on unlabeled traffic data can significantly improve downstream classification performance. By converting raw traffic into language-like tokens, models such as ET-BERT [22] and TrafficFormer [33] employ Transformer-based architectures with tailored selfsupervised tasks to thoroughly mine deep semantic information for various downstream applications. Similarly, YaTC [23] pre-processes each flow into a grayscale image and adopts the masked autoencoder (MAE) paradigm to conduct pretraining and fine-tuning stage. Furthermore, recent advancements have introduced Large Language Models (LLMs) to this domain to address non-I.I.D. scenarios. For instance, ETooL [41] leverages a self-supervised instruction-tuning paradigm to align traffic structural knowledge with LLMs, enhancing outof-distribution (O.O.D.) generalization against shifting traffic patterns.

Most of these methods extract rich and implicit features directly from raw traffic, but they analyze each flow independently, neglecting the interrelations inherent between flows. In contrast, our method explicitly accounts for the dynamic topological patterns of network connections, providing a more global view of the network.

## C. GNN-based methods

An increasing number of studies have leveraged GNNs to extract topological characteristics of traffic due to their powerful ability to capture structural patterns from graph format data. Shen et al. [42] introduce the Traffic Interaction Graph (TIG), which represents each flow based on its packet length sequence to capture implicit features in bidirectional client-server interactions. Zhang et al. [37] propose a bytelevel traffic graph construction approach that uses GNN to embed packet header and payload bytes separately and then fuses them together to generate an overall representation. Lo et al. [35] construct a global communication graph for all flows where IP addresses and ports are mapped as nodes, traffic flows are mapped as edges and the edge attributes are initialized with statistical traffic features. Building on this, Duan et al. [36] propose a Dynamic Line Graph Neural Network (DLGNN) that converts encrypted traffic into a series of spatiotemporal graphs to capture contextual evolution through consecutive snapshots. Wang et al. [43] introduce the Heterogeneous Temporal Graph (HTGraph) to model dynamic network flows. By leveraging prior knowledge of feature correlations, it helps learn transferable knowledge for traffic classification.

However, existing graph-based methods in traffic classification predominantly utilize static features. While methods like DLGNN and HTGraph use sequential snapshots, they cannot dynamically extract and update byte-level features during graph propagation. GenETC overcomes this limitation by iteratively refining deep byte-level semantics within the graph.

## D. Differences From Existing Studies

Current research exhibits a clear dichotomy. On the one hand, cutting-edge pre-training works excel at mining fundamental semantics from raw traffic bytes but fail to leverage global interaction patterns among flows. On the other hand, while GNN-based methods effectively capture topological characteristics from host-to-host communications, they predominantly rely on expert-designed statistical features to initialize graph attributes, limiting their ability to comprehend the complex, obfuscated semantics of modern encrypted traffic.

We compare the aforementioned methods with our work in Table I. In contrast to existing approaches, our method eliminates the need for feature engineering within the global IP-based graph and integrates topological interaction patterns into the traffic pre-training architecture. This unification of the semantic depth of pre-training and the structural reasoning of dynamic graphs significantly improves the expressiveness of flow representations, enhancing generalization to unseen traffic patterns even with limited labeled data.

## III. PRELIMINARIES

## A. Problem Definition

Encrypted traffic refers to data protected by encryption protocols to ensure confidentiality and integrity during transmission. Such traffic is composed of sequences of packets exchanged between hosts. Depending on the level of granularity, traffic can be divided into packets, flows, or sessions. A flow is defined as a sequence of consecutive packets sharing the same five attributes: source IP, destination IP, source port, destination port, and protocol. Flows are unidirectional, while a session consists of a pair of bidirectional flows. In our experiments, each flow is treated as a data instance for training and evaluation.

Encrypted traffic classification aims to classify network traffic into specific types under diverse encryption scenarios, including user behavior identification, malicious traffic detection, and IoT anomaly recognition. Unlike traditional methods that rely heavily on handcrafted features, our approach performs end-to-end classification directly from raw byte sequences.

## B. Traffic Tokenization

Raw traffic data differs fundamentally from natural language in that it lacks explicit semantic structures and human-readable content. To effectively leverage pre-training techniques for encrypted traffic classification, it is therefore necessary to redefine the notion of a “token” in the context of traffic data and transform raw bytes into word-like token sequences analogous to those in natural language.

Specifically, we segment the raw traffic into byte-pair sequences, treating each pair of adjacent bytes as a token. Since each byte is represented by two hexadecimal digits, a byte-pair corresponds to a 4-digit hexadecimal string. For example, the raw string “e8e7323c6550” is transformed into the sequence e8e7, 323c, 6550. Each byte-pair is mapped to a decimal value in the range [0, 65535], yielding a token vocabulary size of 65,536, corresponding to all possible byte-pair values.

To construct the final input sequence for each flow, we apply a specific truncation and aggregation strategy. Considering that the encrypted payload often consists of high-entropy ciphertext with limited discriminative information, we retain the first 100 bytes of each packet, which encompass the complete protocol headers and a portion of the initial payload, discarding the remaining bytes. We select the first three packets of a flow and concatenate their token sequences directly in chronological order to form the complete token input sequence of a flow.

The special tokens [CLS], [SEP], [PAD] and [MASK] are also used as the traditional BERT architecture does. The [CLS] token is always set as the first token of each sequence, the final hidden state of which is used as the aggregate representation of the whole sequence for classification tasks. The [PAD] token is a padding notation to satisfy the minimum length requirement. The [SEP] token separates two traffic flows in opposite directions, and the [MASK] token enables contextual learning of traffic patterns, both of which are applied only during pre-training.

For each traffic token, its input representations consist of three embeddings: token embeddings, position embeddings and segment embeddings. Token embeddings represent bytepairs as vectors, where each token in the vocabulary is associated with a unique vector in the token embedding matrix. Considering that raw traffic bytes have inherent temporal relationships, position embeddings serve to provide the model with the relative position of byte-pairs. Segment embeddings help the model distinguish between different traffic segments, enabling it to understand their relationships. The input embeddings are calculated by summing up the three embeddings. These three embeddings all have learnable parameters which are continuously updated during pre-training and fine-tuning, capable of learning the optimal embeddings of byte-pairs.

## IV. METHODOLOGY

## A. Overall Framework

In this paper, we aim to address the limitation of static feature coupling inherent in prior works by establishing a unified framework for dynamic feature co-evolution. While pre-training captures intrinsic byte-level semantics and GNNs extract extrinsic topological patterns, treating them as decoupled stages restricts the model’s ability to effectively align these two distinct feature spaces. Therefore, during the finetuning stage, it is essential to integrate the BERT module into the GNN architecture, ensuring that flow representations are jointly optimized to be both semantically rich and topologically discriminative.

To this end, we propose GenETC, a framework comprising three hierarchically integrated modules, as illustrated in Fig. 2. First, serving as the semantic foundation, we pre-train BERT on large-scale unlabeled traffic using two unsupervised tasks to learn generic flow representations, providing transferable knowledge of byte distributions. Next, we construct a global flow interaction graph where nodes represent network entities, and introduce a domain-adapted GNN, named DiESAGE, tailored for capturing edge-centric interaction patterns between flows. Finally, the core innovation lies in the joint fine-tuning stage: we implement a Dynamic Graph Updating strategy where edge attributes are iteratively refreshed by the BERT encoder, creating a feedback loop between semantics and topology. To support this computationally, a Memory Bank mechanism is employed to decouple the training batch size from the global graph scale, ensuring scalability.

## B. Pre-training for Fundamental Semantics Extraction

In order to capture the fundamental semantics within raw traffic data for downstream tasks, we employ the BERT architecture to pre-train on large-scale unlabeled traffic and learn generic flow representations. According to the classic BERT model paradigm, we design two traffic-specific unsupervised tasks, including Masked Byte Model (MBM) and Bidirectional Flow Association (BFA).

![](images/a5cd3dd55a3062e8a62bb19c1aa7ec2e022602d708c249795697dbc6ef952509.jpg)  
Fig. 2: Overview of the proposed GenETC framework. It seamlessly integrates a pre-trained BERT module with a graph neural network (DiESAGE) through a Dynamic Graph Updating strategy. During fine-tuning, flow representations extracted by BERT serve as dynamic edge attributes for the interaction graph, which are iteratively updated via a Memory Bank mechanism to resolve scalability issues. The final classification decision is derived from the fusion of the semantic view (intrinsic features) and the topological view (graph-based patterns).

1) Masked Byte Model: This task is built on the Masked Language Model task within classic BERT. The only difference is that each token corresponds to two adjacent bytes and consecutive tokens lack explicit high-level semantic relations. Assume we have an input sequence $S = [ t _ { 1 } , t _ { 2 } , \cdot \cdot \cdot , t _ { n } ]$ after transforming byte-level traffic into tokens, where $t _ { i }$ denotes the token representing byte-pairs. Then 15% of all tokens in each input sequence are randomly masked, generating a new sequence $S ^ { \prime }$ . The chosen masked tokens are replaced with the [MASK] token, a random token or the unchanged token with the probability of 80%, 10%, 10%, respectively. The objective of this task is to predict the original token $t _ { i }$ at the masked positions, given the context from the surrounding tokens. The cross-entropy loss is used to minimize the prediction error for the masked tokens. For each masked token $t _ { i } ,$ , let the predicted token be $\hat { t } _ { i } .$ , and the cross-entropy loss is:

$$
\mathcal {L} _ {M B M} = - \sum_ {i \in \text { masked   tokens }} \log P \left(\hat {t} _ {i} = t _ {i} \mid S ^ {\prime}; \theta\right)\tag{1}
$$

where log $P \left( \hat { t } _ { i } = t _ { i } \mid S ^ { \prime } ; \theta \right)$ is the predicted probability of token $t _ { i }$ and $\theta$ represents the trainable parameters of BERT.

2) Bidirectional Flow Association: In order to capture the contextual relationships between flows and transfer generic flow representations to graph-based fine-tuning process, we design the bidirectional flow association task. We define two traffic flows in opposite directions within a session as a flowpair, which corresponds to two directed edges in opposite directions in a graph. Capturing the dependency and relationship between flows matters, which provides transferable knowledge of activities of adjacent IP addresses. During the fine-tuning stage, the combination of BERT and GNN will further capture the flow interaction patterns in a more global scope.

In this task, a binarized classifier is trained to predict whether two flows belong to a flow-pair. Specifically, when the flow A and flow B are chosen for each pre-training example, half of the time A and B form a flow-pair truncated from a single session, while the other half, B is a random flow from a different session. For a given input flow-pair (A, B), its ground-truth label $y _ { i } \in [ 0 , 1 ]$ , where 0 indicates the flows are paired and 1 indicates they are unpaired. The cross-entropy loss is used, and it can be formulated as:

$$
\mathcal {L} _ {B F A} = - \log P (\hat {y} _ {i} = y _ {i} \mid (A, B); \theta)\tag{2}
$$

The overall loss function for the pre-training objective is defined as the sum of the above two losses:

$$
\mathcal {L} _ {p r e} = \mathcal {L} _ {M B M} + \mathcal {L} _ {B F A}\tag{3}
$$

## C. Graph Analysis for Interaction Patterns Extraction

To further exploit the topological information of host-tohost communications, we construct a global flow interaction graph and utilize GNN to capture the topological features of flows. In this part, we first introduce the construction of the flow interaction graph and highlight its distinction from prior works. Next, we introduce a GNN tailored for the flow interaction graph and use it to learn the aggregated topological representations of directed edges.

1) Graph Construction: Computer networks fundamentally exist as communication graphs, where each host acts as a node, and the communication between hosts represents the links between nodes. From the perspective of a single flow, it can be modeled as a directed edge with two nodes. Four flow fields are extracted to identify the directed edge: source IP address, source port, destination IP address, and destination port. The first two fields are combined into a 2-tuple (source IP address, source port) to represent the source node, while the latter two fields represent the destination node. Naturally, from the perspective of all captured flows, they can be modelled as a global directed graph operating under a transductive setting, where its edge attributes are assigned with representations of flows. It is obvious that the encrypted traffic classification problem has been transformed into a graph edge classification task.

Critically, while some current methods also construct flow interaction graphs to extract topological features, they rely on feature engineering to obtain statistical flow features, which are then assigned to graph attributes. This way not only fails to achieve an end-to-end encrypted traffic classification framework, but also struggles to extract highly discriminative and optimal flow representations. To solve this issue, we assign the edge attributes with the aforementioned generic flow representations learned from BERT, which has learnable parameters instead of static statistical features.

2) Topological representation learning: To further capture the topological characteristics of traffic through interaction among hosts, we adapt the GraphSAGE architecture to design a domain-specific graph neural network named Directed Edge Sample and aggregate (DiESAGE). GraphSAGE (Graph Sample and Aggregate) [26] is a powerful GNN framework designed for generating node embeddings in large graphs, primarily tailored for node classification tasks. However, the traditional GraphSAGE algorithm is not suited for generating representations for directed edges. To address this limitation, DiESAGE tailors the aggregation logic to support directed edge embeddings, transforming the standard node-wise message passing into an edge-centric updating scheme.

The inputs to DiESAGE consist of edge and node features. The edge features are initialized with the temporal representations $X _ { \mathrm { B E R T } } ,$ which are dynamically updated at each epoch during the training process. Meanwhile, in line with E-GraphSAGE [35], the node features are initialized with constant vectors $\{ 1 , 1 , \cdot \cdot \cdot , 1 \}$ , with each vector having the same dimensionality as the edge features.

At each iteration, instead of aggregating information from neighboring nodes, DiESAGE aggregates features from directed edges pointing from the node to its neighbors, and subsequently updates the node’s features based on the aggregated information. At the kth layer, the aggregated representation $\mathbf { h } _ { \mathcal { N } ( u ) } ^ { k }$ is computed using a differentiable aggregation function AGG, defined as:

$$
\mathbf {h} _ {\mathcal {N} (u)} ^ {k} = \operatorname{AGG} _ {k} \left(\left\{\mathbf {e} _ {u v} ^ {k - 1}, \forall v \in \mathcal {N} (u), u v \in \mathcal {E} \right\}\right)\tag{4}
$$

Here, $\{ v \in \mathcal { N } ( u ) , u v \in \mathcal { E } \}$ represents the set of directed edges pointing from source node u to its neighbor nodes, and $\mathbf { e } _ { u v } ^ { k - 1 }$ denotes the edge features at the k − 1th layer. The aggregation function AGG calculates the mean of $\mathbf { e } _ { u v } ^ { k - 1 }$ . Next, the aggregated representation $\mathbf { h } _ { \mathcal { N } ( u ) } ^ { k }$ of the neighbor edges is concatenated with the node’s prior representation $\mathbf { h } _ { u } ^ { k - 1 }$ After applying a trainable weight matrix $\bar { \mathbf { W } } ^ { k }$ and an activation function, the node representation at the kth layer is updated as follows:

$$
\mathbf {h} _ {u} ^ {k} = \sigma \left(\mathbf {W} ^ {k} \cdot \text { CONCAT } \left(\mathbf {h} _ {u} ^ {k - 1}, \mathbf {h} _ {\mathcal {N} (u)} ^ {k}\right)\right)\tag{5}
$$

At depth K, the final representation of the edge $\mathbf { e } _ { u v } ^ { K }$ is computed by concatenating representations of node u and v as follows:

$$
X _ {\mathrm{GNN}} = \operatorname{CONCAT} \left(\mathbf {h} _ {u} ^ {K}, \mathbf {h} _ {v} ^ {K}\right), u v \in \mathcal {E}\tag{6}
$$

The output of DiESAGE, referred to as the topological representation $X _ { \mathrm { G N N } }$ , captures the topological information of the communication graph.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 DiESAGE for graph directed edge embedding
Input: Graph G(V, E); input edge attributes {e$_{uv}$, ∀uv ∈ E};
input node attributes {n$_{v}$, ∀v ∈ V} = {1, ..., 1}; depth K
Output: Directed edge embeddings {z$_{uv}$, ∀uv ∈ E}
1: h$_{0}$ ← n$_{v}$, ∀v ∈ V
2: e$_{uv}^{0}$ ← e$_{uv}$, ∀uv ∈ E
3: for k ← 1 to K do
4:    for u ∈ V do
5:    h$_{\mathcal{N}(u)}^{k}$ ← AGG ( {e$_{uv}^{k-1}$, ∀v ∈ N(u), uv ∈ E})
6:    h$_{u}^{k}$ ← σ (W$^{k}$ · CONCAT (h$_{u}^{k-1}$, h$_{\mathcal{N}(u)}^{k}$ ))
7:    end for
8: end for
9: for uv ∈ E do
10:    z$_{uv}$ = CONCAT (h$_{u}^{K}$, h$_{v}^{K}$), uv ∈ E
11: end for
12: return z$_{uv}$
</div>

## D. Joint Fine-tuning for Dynamic Feature Fusion

In this part, we fine-tune the model by jointly optimizing BERT and GNN. To provide a theoretical foundation for our integration strategy, we interpret this joint optimization process through the lens of Manifold Alignment [44], [45]. The pretrained BERT module maps raw traffic bytes into a continuous semantic manifold, denoted as $\mathcal { M } _ { s e m }$ , where flows with similar payload patterns lie close to each other. Simultaneously, the global interaction graph defines a topological manifold, $\mathcal { M } _ { t o p } ,$ which clusters flows based on communication proximity and structural roles [46]. Unlike traditional approaches that treat $\mathcal { M } _ { s e m }$ as fixed features, GenETC avoids structural mismatches by dynamically aligning this semantic manifold with the topological structure via backpropagating gradients from the GNN to the BERT encoder. This effectively acts as a form of manifold regularization [47], ensuring that the final flow representations lie on a unified manifold that respects both byte-level semantics and network-level interactions.

Guided by this theoretical perspective, we design a fusion mechanism to integrate these aligned representations and employ a Memory Bank technique to enable efficient mini-batch training.

1) Interpolated Fusion of BERT and GNN Representations: In order to fuse intrinsic semantic features and interactive topological patterns of flows, we propose a logic-level interpolation strategy. Instead of directly concatenating high-dimensional feature vectors, we first map the representations X<sub>BERT</sub> and $X _ { \mathrm { G N N } }$ into the logit space to obtain the classification probability distributions:

$$
\begin{array}{c} Z _ {\mathrm{BERT}} = \operatorname{softmax} (\mathbf {W _ {1}} X _ {\mathrm{BERT}}) \\ Z _ {\mathrm{GNN}} = \operatorname{softmax} (\mathbf {W _ {2}} X _ {\mathrm{GNN}}) \end{array}\tag{7}
$$

where $W _ { 1 } , W _ { 2 } \in \mathbb { R } ^ { p \times d }$ are trainable weight matrices, p denotes the number of traffic categories.

We then compute the linear interpolation of Z<sub>BERT</sub> and Z<sub>GNN</sub> to obtain the final fused prediction:

$$
Z _ {f u s i o n} = (1 - \mu) Z _ {\mathrm{BERT}} + \mu Z _ {\mathrm{GNN}}\tag{8}
$$

where the hyper-parameter $\mu \in [ 0 , 1 ]$ controls the trade-off between semantic and topological perspectives. Specifically, $\mu ~ = ~ 0$ implies reliance solely on raw traffic semantics, ignoring structural context; $\mu = 1$ indicates that the decision depends entirely on topological patterns, potentially overlooking fine-grained payload details. An intermediate value $( 0 ~ < ~ \mu ~ < ~ 1 )$ balances these two views to achieve optimal performance. Finally, the objective function is defined as the cross-entropy loss between the fused prediction and the ground truth:

$$
\mathcal {L} _ {f i n e} = \mathrm{CrossEntropy} (Z _ {f u s i o n}, Y _ {l a b e l})\tag{9}
$$

2) Updating Graph attributes with Memory Bank: To realize the dynamic alignment of $\mathcal { M } _ { s e m }$ and $\begin{array} { r } { \mathcal { M } _ { t o p } , } \end{array}$ , edge attributes must be iteratively updated using $X _ { \mathrm { B E R T } }$ during training. However, traditional full-batch GNN training is computationally prohibitive due to the scale of network traffic and the memory demands of optimizing BERT and DiESAGE simultaneously.

To address these scalability challenges, we adopt a Memory Bank (MB) technique [48], [49]. The MB decouples the minibatch size from the total number of graph edges by explicitly storing the temporal flow representations. Specifically, we maintain an MB to track the representations X<sub>BERT</sub> for all edges. To ensure a baseline of feature freshness, we perform a global, gradient-free inference at the start of each epoch to completely refresh the MB. Operating in a transductive setting, this global MB encompasses all edges, including those from the validation and test splits. This allows the model to leverage the fully observable routing topology as structural prior knowledge during message passing, while their groundtruth labels remain strictly masked. During each training iteration, we sample a mini-batch of edges, recompute their fresh representations using the current BERT encoder, and immediately update the corresponding entries in the MB. These updated features are then fed into the DiESAGE model for topological learning. This mechanism allows gradients to flow back to the BERT encoder.

Note that while asynchronous updates might theoretically introduce feature inconsistencies, our method fundamentally avoids this issue by rigidly decoupling the learning rates of our modules. By applying an extremely small learning rate to the BERT encoder, representation drift within a single epoch is strictly limited. This ensures stored neighbor features remain accurate proxies for their current state, guaranteeing smooth convergence and the stability of the semantic manifold evolution.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 Pseudocode of the GenETC algorithm

Input: Graph  $\mathcal{G}(\mathcal{V},\mathcal{E})$ ; raw-byte flows F; input edge attributes  $\{e_{uv},\forall uv\in\mathcal{E}\}$ ; depth K; number of training epochs T; linear interpolation coefficient  $\mu$ ; traffic label  $Y_{label}$ 

Output: Parameters of GenETC model  $\theta_{GenETC}$ 

1: for epoch  $\leftarrow$  1 to T do

2: // Initialize/Update attributes of all edges using BERT representations after each epoch

3:  $X_{BERT} \leftarrow \text{BERT}(\mathcal{F})$ 

4: Update  $\{e_{uv},\forall uv\in\mathcal{E}\}$  with  $X_{BERT}$ 

5: // Set a Memory Bank to track all BERT representations

6: for  $F_{mini-batch} \in F$  do

7: // Update a subset of edges corresponding to the sampled mini-batch using optimized BERT

8:  $X_{BERT}' \leftarrow \text{BERT}(\mathcal{F}_{\text{mini-batch}})$ 

9: Update  $\{e_{uv},\forall uv\in\mathcal{E}_{\text{mini-batch}}\}$  with  $X_{BERT}'$ 

10:  $X_{BERT} \leftarrow \{e_{uv},\forall uv\in\mathcal{E}\}$ 

11:  $X_{GNN} = \text{DiESAGE}(e_{uv}),\forall uv\in\mathcal{E}$ 

12: // Map representations to low-dimensional prediction vectors

13:  $Z_{BERT} \leftarrow \text{softmax}(\mathbf{W}_{1}X_{BERT})$ 

14:  $Z_{GNN} \leftarrow \text{softmax}(\mathbf{W}_{2}X_{GNN})$ 

15: // Compute final flow representations using linear interpolation

16:  $Z_{fusion} \leftarrow (1-\mu)Z_{BERT} + \mu Z_{GNN}$ 

17:  $L_{fine} \leftarrow CrossEntropy(Z_{fusion},Y_{label})$ 

18:  $\theta_{GenETC} \leftarrow Adam(L_{fine})$ 

19: end for

20: end for

21: return  $\theta_{GenETC}$
</div>

## V. EXPERIMENTS

## A. Experiment Setup

1) Pre-training Datasets: We select three encrypted traffic datasets under various scenarios for pre-training the model, in order to improve its generalizability and versatility. The datasets include CIC-IDS2017 (2017) [50], CICAPT-IIoT (2024) [51] and Browser (2020) [7]. The CIC-IDS2017 dataset provides a comprehensive collection of both benign and various common attack traffic, including Brute Force FTP, DoS, Web Attack, Botnet and so on. The CICAPT-IIoT dataset is generated using a hybrid testbed consisting of real and simulated industrial internet of things (IIoT) components, which is particularly effective for simulating APT scenarios. The Browser dataset contains network traffic generated on Android from the top 1000 websites on Alexa, including

Chrome, Firefox and Samsung Internet. Table II provides detailed information about the three datasets. The total volume of the pre-training dataset is approximately 20 GB, comprising over 600,000 flows. In addition, these datasets ensure a diverse and ample range of protocols, facilitating more effective pretraining. The CIC-IDS2017 dataset includes protocols commonly used in various network attacks and the CICAPT-IIoT dataset contains the protocols used in various APT attack phases. Moreover, the Browser dataset mainly covers the usage of TLS 1.3 protocol in encrypted applications.

TABLE II: Pre-training datasets

<table><tr><td>Datasets</td><td>Size</td><td>Protocols</td></tr><tr><td>CIC-IDS2017 [50]</td><td>10 GB</td><td>TLS 1.2, SFTP, SMTP, SSH, SSDP...</td></tr><tr><td>CICAPT-IIoT [51]</td><td>4.8 GB</td><td>TLS 1.2, SMB, SSH, RDP, SMTP...</td></tr><tr><td>Browser [7]</td><td>6.9 GB</td><td>TLS 1.3, QUIC...</td></tr></table>

2) Fine-tuning Datasets: To comprehensively evaluate the effectiveness and generalizability of GenETC, we conducted experiments on six public encrypted traffic datasets under various network scenarios, including ISCX-VPN, ISCX-Tor, CSTNET-TLS 1.3, CIC-IoT2023 and CIC-AndMal. These datasets correspond to six distinct encrypted traffic classification tasks, each representing a unique real-world application scenario, as shown in Table III.

Task 1: VPN service classification task aims to classify encrypted traffic routed through Virtual Private Networks (VPNs) into specific service types. VPNs, as an example of privacyenhancing tools, are widely used to bypass censorship and access restricted content, making identification challenging due to protocol obfuscation. The ISCX-VPN dataset contains 12 types of encrypted traffic tunneled through both VPN and non-VPN, including email, VoIP, video streaming, etc.

Task 2: VPN application classification task aims to classify VPN traffic into more fine-grained encrypted applications. We further recategorized the ISCX-VPN dataset based on applications, resulting in 29 categories, including Skype, YouTube, Spotify, and others.

Task 3: Tor service type detection task aims to identify the specific traffic type routed through Tor (the Onion Router). Tor anonymizes internet activities by encrypting and routing traffic through a distributed network, which adds complexity to traffic classification. The ISCX-Tor dataset includes traffic collected via Tor, featuring eight categories: browsing, email, file transfer and so on.

Task 4: Website fingerprinting task aims to deanonymize web traffic transmitted through TLS 1.3. The innovations introduced by TLS 1.3 significantly obfuscate traditional metadata leakage channels, such as single-round trip handshakes and perfect forward secrecy mechanisms. The CSTNET-TLS 1.3 dataset comprises encrypted traffic collected over 120 websites implementing the TLS 1.3 protocol.

Task 5: The IoT behavior detection task focuses on identifying network traffic patterns associated with diverse IoT device behaviors and various attack scenarios. The CIC-IoT2023 dataset comprises 33 types of fine-grained attacks along with benign traffic, collected within a large-scale IoT topology, making it a representative benchmark for IoT security analytics.

Task 6: The encrypted malware detection task aims to distinguish malware traffic from benign ones or conduct finegrained classification of malware family behaviors. The CIC-AndMal2017 dataset collects encrypted traffic consisting of 42 unique malware families and benign applications.

TABLE III: Fine-tuning datasets

<table><tr><td>Datasets</td><td>Tasks</td><td>Flows</td><td>Classes</td></tr><tr><td>ISCX-VPN (Service) [52]</td><td>Service Type Identification</td><td>3600</td><td>12</td></tr><tr><td>ISCX-VPN (App) [52]</td><td>Application Fingerprinting</td><td>7818</td><td>29</td></tr><tr><td>ISCX-Tor [53]</td><td>Service Type Identification</td><td>1159</td><td>8</td></tr><tr><td>CSTNET-TLS 1.3 [22]</td><td>Website Fingerprinting</td><td>35464</td><td>120</td></tr><tr><td>CIC-IoT2023 [54]</td><td>IoT Behavior Detection</td><td>10200</td><td>34</td></tr><tr><td>CIC-AndMal [55]</td><td>Encrypted Malware Detection</td><td>12900</td><td>43</td></tr></table>

3) Data Preprocessing: Firstly, we remove packets that are irrelevant to the transmitted content of traffic, such as Address Resolution Protocol (ARP) packets and Internet Control Message Protocol (ICMP) packets. We then use the SplitCap tool to split the raw traffic datasets into unidirectional flows, treating each flow as a sample for training or evaluation. Incomplete or anomalous flows (e.g., those consisting of only a single packet or containing corrupted payloads) are discarded to ensure data integrity. In the ISCX-Tor dataset, protocol anonymization causes most traffic to share identical 5-tuples, creating massive continuous flows. We divide these into shorter segments, strictly limiting the output to a maximum of 10 segments per original flow while ensuring all segments from the same flow remain in the same data split to prevent data leakage. All retained flows are length-normalized by truncating or zero-padding packet sequences to maintain consistent input dimensions. Rather than utilizing the entire massive corpora, we evaluate our framework under a strict limited-data setting by randomly sampling a maximum of 300 flows per class for each dataset. The number of flows retained in each dataset after processing, along with the number of classes per dataset are presented in Table III. Finally, we divide these datasets into training, validation, and testing sets in a ratio of 8:1:1 for all experiments. Importantly, the global flow interaction graph is constructed using all flows across the dataset.

4) Implementation Details and Evaluation Metrics: During the raw traffic pre-processing stage, we retain the first 100 bytes of each packet and discard the remaining bytes. Only the first 3 raw packets of each flow are retained, with the rest discarded. During fine-tuning, we employ the pre-trained BERT architecture together with a two-layer DiESAGE model to constitute our GenETC method. Specifically, we utilize Xavier initialization for the weight matrices in the DiESAGE module to maintain a stable variance of gradients during the initial training phase. We employ the Adam optimizer along with a learning rate scheduler, setting the initial learning rates to 5e-6 for the BERT model and 1e-4 for the DiESAGE model. The learning rate decays by a factor of 0.1 after 30 epochs following a multi-step schedule, and key hyperparameters (e.g., learning rate and batch size) are empirically tuned based on validation performance. Training is conducted for 80 epochs with a batch size of 64. The model is implemented in PyTorch 2.0.1 and trained on a single NVIDIA RTX 4090 GPU. Each experiment is independently repeated ten times, and the average performance is reported.

TABLE IV: Experimental Results on ISCX-VPN(Service), ISCX-VPN(App) and ISCX-Tor Datasets

<table><tr><td>Datasets</td><td colspan="4">ISCX-VPN(Service)</td><td colspan="4">ISCX-VPN(App)</td><td colspan="4">ISCX-Tor</td></tr><tr><td>Methods</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td></tr><tr><td>AppScanner [12]</td><td>0.6210</td><td>0.6164</td><td>0.6187</td><td>0.6175</td><td>0.4720</td><td>0.4078</td><td>0.3536</td><td>0.3788</td><td>0.5288</td><td>0.5288</td><td>0.4645</td><td>0.4832</td></tr><tr><td>XGBoost [56]</td><td>0.8715</td><td>0.8779</td><td>0.8776</td><td>0.8778</td><td>0.7430</td><td>0.6918</td><td>0.7174</td><td>0.7043</td><td>0.8994</td><td>0.8993</td><td>0.9017</td><td>0.9005</td></tr><tr><td>2D-CNN [39]</td><td>0.7944</td><td>0.7935</td><td>0.7905</td><td>0.7920</td><td>0.7067</td><td>0.6745</td><td>0.6927</td><td>0.6835</td><td>0.7155</td><td>0.7004</td><td>0.7402</td><td>0.7198</td></tr><tr><td>DF [16]</td><td>0.8472</td><td>0.8429</td><td>0.8464</td><td>0.8446</td><td>0.7503</td><td>0.7089</td><td>0.7261</td><td>0.7174</td><td>0.8966</td><td>0.9041</td><td>0.8879</td><td>0.8959</td></tr><tr><td>Deep Packet [40]</td><td>0.8472</td><td>0.8490</td><td>0.8447</td><td>0.8469</td><td>0.7940</td><td>0.7496</td><td>0.7618</td><td>0.7556</td><td>0.9052</td><td>0.9033</td><td>0.9229</td><td>0.9130</td></tr><tr><td>TSCRNN [19]</td><td>0.8972</td><td>0.8977</td><td>0.8935</td><td>0.8956</td><td>0.8308</td><td>0.7955</td><td>0.8015</td><td>0.7985</td><td>0.9310</td><td>0.9363</td><td>0.9278</td><td>0.9320</td></tr><tr><td>E-GraphSAGE [35]</td><td>0.5335</td><td>0.5303</td><td>0.5495</td><td>0.5226</td><td>0.2667</td><td>0.2976</td><td>0.3364</td><td>0.3158</td><td>0.5048</td><td>0.4751</td><td>0.4867</td><td>0.4674</td></tr><tr><td>TFE-GNN [37]</td><td>0.8610</td><td>0.8641</td><td>0.8740</td><td>0.8690</td><td>0.7743</td><td>0.7668</td><td>0.7880</td><td>0.7772</td><td>0.8224</td><td>0.7861</td><td>0.8735</td><td>0.8275</td></tr><tr><td>ET-BERT [22]</td><td>0.9246</td><td>0.9290</td><td>0.9250</td><td>0.9270</td><td>0.8721</td><td>0.8418</td><td>0.8469</td><td>0.8443</td><td>0.9655</td><td>0.9769</td><td>0.9688</td><td>0.9728</td></tr><tr><td>YaTC [23]</td><td>0.9304</td><td>0.9327</td><td>0.9295</td><td>0.9311</td><td>0.8953</td><td>0.8682</td><td>0.8740</td><td>0.8711</td><td>0.9532</td><td>0.9494</td><td>0.9547</td><td>0.9504</td></tr><tr><td>TrafficFormer [33]</td><td>0.9302</td><td>0.9321</td><td>0.9294</td><td>0.9307</td><td>0.8926</td><td>0.8722</td><td>0.8762</td><td>0.8742</td><td>0.9741</td><td>0.9772</td><td>0.9743</td><td>0.9758</td></tr><tr><td>GenETC(Ours)</td><td>0.9944</td><td>0.9952</td><td>0.9903</td><td>0.9927</td><td>0.9680</td><td>0.9466</td><td>0.9489</td><td>0.9478</td><td>0.9914</td><td>0.9911</td><td>0.9821</td><td>0.9866</td></tr></table>

TABLE V: Experimental Results on CIC-IoT2023, CIC-AndMal and CSTNET-TLS 1.3 Datasets

<table><tr><td>Datasets</td><td colspan="4">CIC-IoT2023</td><td colspan="4">CIC-AndMal</td><td colspan="4">CSTNET TLS1.3</td></tr><tr><td>Methods</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td></tr><tr><td>AppScanner [12]</td><td>0.2676</td><td>0.2642</td><td>0.3108</td><td>0.2856</td><td>0.0837</td><td>0.0852</td><td>0.0567</td><td>0.0681</td><td>0.1302</td><td>0.1237</td><td>0.1336</td><td>0.1285</td></tr><tr><td>XGBoost [56]</td><td>0.3268</td><td>0.3290</td><td>0.3790</td><td>0.3522</td><td>0.1457</td><td>0.1474</td><td>0.1188</td><td>0.1316</td><td>0.3875</td><td>0.3610</td><td>0.3877</td><td>0.3739</td></tr><tr><td>2D-CNN [39]</td><td>0.3608</td><td>0.3512</td><td>0.3574</td><td>0.3543</td><td>0.1798</td><td>0.1693</td><td>0.1739</td><td>0.1716</td><td>0.2907</td><td>0.2901</td><td>0.2399</td><td>0.2626</td></tr><tr><td>DF [16]</td><td>0.5147</td><td>0.5089</td><td>0.5152</td><td>0.5120</td><td>0.2008</td><td>0.1939</td><td>0.1947</td><td>0.1943</td><td>0.5732</td><td>0.5684</td><td>0.5616</td><td>0.5650</td></tr><tr><td>Deep Packet [40]</td><td>0.4843</td><td>0.4746</td><td>0.4989</td><td>0.4865</td><td>0.1891</td><td>0.1724</td><td>0.1785</td><td>0.1754</td><td>0.6104</td><td>0.6071</td><td>0.5952</td><td>0.6011</td></tr><tr><td>TSCRNN [19]</td><td>0.5049</td><td>0.4965</td><td>0.5150</td><td>0.5056</td><td>0.1791</td><td>0.1632</td><td>0.1888</td><td>0.1750</td><td>0.6642</td><td>0.6623</td><td>0.6536</td><td>0.6579</td></tr><tr><td>E-GraphSAGE [35]</td><td>0.2049</td><td>0.1988</td><td>0.1678</td><td>0.1820</td><td>0.0884</td><td>0.0871</td><td>0.1202</td><td>0.1010</td><td>0.1504</td><td>0.1349</td><td>0.1831</td><td>0.1553</td></tr><tr><td>TFE-GNN [37]</td><td>0.5743</td><td>0.5668</td><td>0.5880</td><td>0.5772</td><td>0.1552</td><td>0.1529</td><td>0.1587</td><td>0.1557</td><td>0.7021</td><td>0.6996</td><td>0.7034</td><td>0.7015</td></tr><tr><td>ET-BERT [22]</td><td>0.7843</td><td>0.7809</td><td>0.7901</td><td>0.7855</td><td>0.5651</td><td>0.5644</td><td>0.5707</td><td>0.5675</td><td>0.9171</td><td>0.9206</td><td>0.9285</td><td>0.9245</td></tr><tr><td>YaTC [23]</td><td>0.7480</td><td>0.7426</td><td>0.7473</td><td>0.7460</td><td>0.5946</td><td>0.5921</td><td>0.6059</td><td>0.5989</td><td>0.8447</td><td>0.8381</td><td>0.8409</td><td>0.8395</td></tr><tr><td>TrafficFormer [33]</td><td>0.7980</td><td>0.7934</td><td>0.8011</td><td>0.7972</td><td>0.5667</td><td>0.5654</td><td>0.5713</td><td>0.5683</td><td>0.9247</td><td>0.9291</td><td>0.9339</td><td>0.9315</td></tr><tr><td>GenETC(Ours)</td><td>0.9333</td><td>0.9273</td><td>0.9409</td><td>0.9341</td><td>0.8481</td><td>0.8236</td><td>0.8284</td><td>0.8260</td><td>0.9569</td><td>0.9595</td><td>0.9586</td><td>0.9591</td></tr></table>

To evaluate and compare the classification performance of our method, we utilize four key metrics: Accuracy (AC), Precision (PR), Recall (RC), and F1-score (F1). Given the imbalanced class distribution in the datasets, macro averaging is applied to calculate the mean values of AC, PR, RC, and F1 across all classes.

## B. Comparison with Baselines

We compare our model against ten state-of-the-art encrypted traffic classification baselines, including two MLbased method (i.e., AppScanner [12], XGBoost [56]), four DLbased methods (i.e., 2D-CNN [39], DF [16], Deep packet [40], TSCRNN [19]), two GNN-based methods (i.e., E-GraphSAGE [35], TFE-GNN [37]) and three pre-training-based methods (ET-BERT [22], YaTC [23], TrafficFormer [33]). For a fair comparison, all baseline models are retrained under the same dataset partitions and preprocessing procedures (e.g., ensuring identical raw-byte truncation lengths) as our proposed method, while strictly adhering to their original hyperparameter settings to ensure their optimal performance.

ML-based methods. It can be observed that ML-based methods demonstrate poorer performance compared to other methods. Specifically, while XGBoost and AppScanner can handle basic service classification, their performance drops significantly on highly obfuscated datasets like CIC-AndMal. On the one hand, the fixed feature engineering diagram is hard to adapt well to the diverse encryption scenarios involved in our experiment; on the other hand, the average truncated length of flows in our experimental setup is relatively short, which is too limited for feature engineering to extract implicit but discriminative statistical features.

DL-based methods. DL models can automatically capture dependencies between adjacent bytes in raw packets to extract discriminative patterns, which exceeds the capability of MLbased methods. The classification results of DL-based methods outperform ML-based methods significantly. The 2D-CNN and DF methods reshape raw traffic into greyscale image and sequence formats, and then fed them into 2D-CNN and 1D-CNN for classification, respectively. The TSCRNN integrates temporal characteristics into traffic features by combining RNN with CNN, which has seen an obvious improvement in terms of accuracy. It indicates that features extracted from raw traffic byte using deep DL can characterize flows more comprehensively and thoroughly.

GNN-based methods. E-GraphSAGE is the first innovative approach to uncover interrelationships between diverse

JOURNAL OF LAT<sub>E</sub>X CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020

flows and leverages GNN to extract topology-enhanced flow representations. However, it relies on feature engineering to initialize graph attributes, unable to process raw traffic byte directly. Besides, its pre-defined statistical features were originally designed for binary intrusion detection scenario. The dimension of its statistical features is too limited to generate flow representations with strong generalizability. It can be expected that this approach will have relatively poorer results. Another GNN-based method, TFE-GNN, construct graphs in a novel way, representing packet bytes as nodes to form byte-level traffic graphs. However, it considers each flow independently, without considering the interrelation between them.

Pre-training methods. The results demonstrate that pretraining methods consistently outperform other methods across multiple benchmarks. Two primary factors contribute to such an improvement. On the one hand, pre-training models with abundant parameters are better equipped to extract fine-grained features and latent valuable patterns from raw traffic bytes. On the other hand, the diversity of encryption techniques hinders accurate traffic detection under limited training data, while pretraining mitigates this limitation by transferring generalizable knowledge of byte-level semantics. The ET-BERT and YaTC process each raw flow into natural language and grayscale figure format respectively, and then apply corresponding mature pre-training diagrams to enhance flow representations. Experimental results show that these pre-training methods consistently improve classification accuracy by at least 5% compared to ordinary DL-based models, underscoring their effectiveness in data-scarce scenarios. Building on these approaches, the recent method TrafficFormer further optimizes pre-training ob jectives and incorporates data augmentation during fine-tuning, achieving additional gains in performance. However, existing works still focus exclusively on analyzing individual flows in isolation, without capturing the interrelationships among different flows within a network. In contrast, our method incorporates topological interaction patterns between flows into the pre-training framework. For instance, if a flow from address A to B contains heavily obfuscated or insufficient byte-level information, related flows, such as those from address A to other endpoints or multi-hop connections, can be leveraged for feature augmentation. By aggregating both the individual flow content and its surrounding topological context, our method generates richer and more discriminative representations. The results validate the effectiveness of our approach, showing that it outperforms all STOA methods significantly across all datasets.

Then we analyze the classification performance from the perspective of each dataset. For the ISCX-Tor dataset, where samples from certain classes are notably scarce, GenETC outperforms other pre-training methods by about 2%. The ISCX-VPN dataset is divided into service-level (12 classes) and more fine-grained application-level (29 classes) categories. GenETC maintains consistently high performance in both scenarios, while DL-based methods show a noticeable degradation in the more granular classification task. For the CSTNET-TLS 1.3 dataset, which presents a highly fine-grained classification task with 120 website categories, GenETC achieves an accuracy improvement of around 4% compared to SOTA method. This indicates that encrypted traffic over TLS 1.3 possesses implicit patterns hidden in topological network connections, which can be mined using GNN for performance improvement. Our method demonstrates significant advantages in classification tasks involving numerous categories, even when training samples are very limited. For the CIC-IoT2023 dataset, which contains 34 traffic classes, most baseline methods achieve moderate performance. In contrast, GenETC achieves a substantial improvement, outperforming the previous best method, TrafficFormer, by approximately 13.7% in F1. This indicates that in large-scale IoT topological scenarios, our method can effectively integrate inter-device topological information into flow representations, significantly enhancing the model’s representational capacity. For the CIC-AndMal dataset, GenETC outperforms all baselines by a large margin across all metrics. DL-based methods yield only around 20% classification accuracy on this dataset, indicating the challenge of extracting discriminative features from highly obfuscated malware traffic. The classification results of pre-training improve by over 20% but still stay at a moderate level. However, GenETC achieves a 22.7% accuracy improvement over YaTC, indicating that our dynamic graph enhanced pre-training framework effectively leverages flow interaction patterns to mitigate ambiguity and obfuscation in flow representations. Ultimately, since most baselines act as strictly inductive independent-flow classifiers, these consistent gains explicitly confirm that leveraging communication topology provides a decisive advantage over traditional flow-only methods.

## C. Ablation Study

In this section, we conduct ablation studies to verify and understand the contribution of each component to GenETC. First, we evaluate the two most crucial components of our model across all datasets respectively, i.e., dynamic graph enhancement and pre-training. Then, we discuss the other components of GenETC across three datasets, including pretraining sub-tasks, typical feature extractors and feature fusion operations.

1) Impact of Dynamic Graph Enhancement: Table VI presents the classification performance across all metrics without topology enhancement, i.e., completely discarding the graph construction and GNN module to solely fine-tune the pre-trained BERT on raw traffic bytes. A degradation in performance is observed across all datasets, though to varying degrees. The CIC-AndMal dataset exhibits the most significant drop, with accuracy decreasing by 27.48%. This can be attributed to the fact that malicious attacks from the same malware family often share a common pool of network entities, making interaction information particularly valuable for distinguishing between classes. The classification performance of CSTNET-TLS 1.3 declines by approximately 3%. This dataset contains 120 fine-grained categories of website traffic, where the traffic from a given website typically shares the same IP address pool. However, because its content is less obfuscated than that of CIC-AndMal, the accuracy drop is less pronounced. The remaining datasets show a decrease in accuracy ranging approximately from 1% to 10%. These results underscore the critical role of extracted interaction patterns; considering the graph module introduces negligible additional parameters, this significant performance gap confirms that the gains originate from the structural advantages of our Dynamic Graph Enhancement mechanism rather than increased model capacity or extensive pre-training alone.

2) Impact of Pre-training: Table VII presents the classification performance of our framework without pre-training. In this configuration, the dynamic graph module is explicitly retained while the BERT encoder is fine-tuned directly from random initialization. It can be observed that all datasets exhibit a noticeable decline in performance. The accuracies of the CIC-IoT2023 and CIC-AndMal datasets decline by 6.53% and 8.98%, respectively, while other datasets experience relatively smaller declines. In our limited-data experimental setting, models trained without pre-training struggle to learn sufficiently discriminative features, inevitably resulting in reduced classification performance. This phenomenon aligns with observations in several prior pre-training approaches (e.g., ET-BERT [22], YaTC [23], TrafficFormer [33]), further supporting the conclusion that pre-training is essential in traffic analysis. It equips models with a foundational understanding of traffic semantics, which can be effectively transferred to a variety of downstream tasks.

3) Impact of Other Components: We further conduct ablation studies on other components of GenETC across the ISCX-VPN(App) and AndMal datasets, specifically focusing on pretraining tasks, typical feature extractors, and feature fusion operations (Table VIII). ‘PT’ and ‘DG’ indicate the incorporation of pre-training and dynamic graph modules during the finetuning stage. First, we validate the pre-training components. ‘w/o MBM’ indicates that the BERT encoder is pre-trained using only the Bidirectional Flow Association (BFA) task, whereas ‘w/o BFA’ indicates that it is pre-trained solely with the Masked Byte Model (MBM). These experiments confirm that our custom pre-training tasks effectively improve the representations of unidirectional flows. Additionally, ‘w/o PT&DG’—a randomly initialized BERT baseline without pretraining $\mathrm { { _ { o r } } }$ graph enhancements—exhibits the lowest performance. Next, replacing the BERT module with Transformer (‘w/ Transformer’) or CNN architectures (‘w/ CNN’) results in a notable performance decline. For the structural module, we compare mean aggregation with max and attention-based aggregation. Although attention-based aggregation achieves comparable performance, it introduces additional trainable parameters and more complex edge-wise attention computation. Max aggregation performs noticeably worse, whereas mean aggregation achieves the best results with a lightweight, parameter-free operation, providing a better balance between classification performance and computational efficiency.

Furthermore, to isolate the benefits of dynamic joint optimization, we evaluate two controls. Freezing the GNN (‘frozen DiESAGE’) simulates a static graph without iterative feature refreshes. The resulting performance drop confirms that our gains stem specifically from dynamic semantic-topological coevolution rather than a static relational signal. Conversely, freezing the semantic encoder (‘frozen BERT’) causes a catastrophic performance collapse. This demonstrates that while pre-training provides generic semantics, end-to-end fine-tuning is indispensable for adapting them to specific downstream tasks, bridging a semantic gap that the GNN alone cannot.

## D. Deep Dive for GenETC

1) Impact of Interpolation Coefficient.: The interpolation coefficient $\mu$ regulates the trade-off between the BERT representations and topological representations. $\mu = 0$ indicates that only the raw traffic byte information is utilized, without incorporating interaction patterns among flows. When $0 ~ < ~ \mu ~ < ~ 1$ , both the intrinsic semantic features and the interactive topological patterns of traffic are integrated, with $\mu$ controlling the relative contribution of each. The optimal value of $\mu$ for achieving the best classification performance varies across different traffic datasets. Fig. 3 presents the F1- score results for all datasets, with $\mu$ ranging from 0 to 1 in increments of 0.1. To provide a clearer illustration, the datasets are divided into two groups according to the variation range of $\mu { : }$ three datasets with large performance fluctuations are shown in Fig. 3(b), while the other three with relatively minor variations are shown in Fig. 3(a). As $\mu$ increasing from zero, the F1-score initially rises sharply, demonstrating the effectiveness of dynamic graph enhancement. However, these polyline patterns do not conform to a consistent trend across all datasets, and the optimal interpolation coefficient differs for each case. This variation inherently reflects the distinct characteristics of specific network environments: datasets with highly obfuscated payloads (e.g., malicious traffic) often favor a higher $\mu$ to rely on stable topological patterns, whereas traffic sharing congested infrastructure benefits from a lower $\mu$ focused on fine-grained semantics. In some datasets, performance even deteriorates after interpolation is applied. Overall, it can be observed that $\mu$ values in the range of 0.3 to 0.5 tend to yield the best classification performance.

![](images/5e4c60495a3d1472cee712fc7ea84fe1298ce40939ee268a8cc1a5091affa784.jpg)  
(a)

![](images/4e3c0799a5500f0acf906bee690261ae821afe8413be0244762dfcb143764bf7.jpg)  
(b)  
Fig. 3: Parameter sensitivity analysis w.r.t. interpolation coefficient $\mu$ across six datasets

2) Impact of Input Traffic Truncation: In the data preprocessing stage for traffic analysis, we retain only the first 100 bytes of each packet within a network flow. The number of retained bytes from each flow sample, denoted as $m ,$ plays a crucial role in balancing computational overhead and classification performance. To investigate this trade-off, we evaluate the impact of different truncation lengths m on model performance across the ISCX-VPN(App) and CIC-IoT2023 datasets.

TABLE VI: Ablation study of classification performance without dynamic graph enhancement

<table><tr><td>Datasets</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td></tr><tr><td>ISCX-VPN (Service)</td><td>93.45%(-5.99%)</td><td>94.02%(-5.50%)</td><td>92.88%(-6.15%)</td><td>93.45%(-5.82%)</td></tr><tr><td>ISCX-VPN (App)</td><td>88.24%(-8.56%)</td><td>86.11%(-8.55%)</td><td>87.52%(-7.37%)</td><td>86.81%(-7.97%)</td></tr><tr><td>ISCX-Tor</td><td>97.66%(-1.48%)</td><td>98.32%(-0.79%)</td><td>97.21%(-1.00%)</td><td>97.76%(-0.90%)</td></tr><tr><td>CIC-IoT2023</td><td>80.42%(-12.91%)</td><td>81.03%(-11.70%)</td><td>79.72%(-14.37%)</td><td>80.37%(-13.04%)</td></tr><tr><td>CIC-AndMal</td><td>57.33%(-27.48%)</td><td>58.11%(-24.25%)</td><td>56.49%(-26.35%)</td><td>57.29%(-25.31%)</td></tr><tr><td>CSTNET-TLS 1.3</td><td>92.72%(-2.97%)</td><td>93.54%(-2.41%)</td><td>92.61%(-3.25%)</td><td>93.07%(-2.84%)</td></tr></table>

TABLE VII: Ablation study of classification performance without pre-training

<table><tr><td>Datasets</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td></tr><tr><td>ISCX-VPN (Service)</td><td>98.20%(-1.24%)</td><td>97.70%(-1.82%)</td><td>98.80%(-0.23%)</td><td>98.25%(-1.02%)</td></tr><tr><td>ISCX-VPN (App)</td><td>94.25%(-2.55%)</td><td>90.31%(-4.35%)</td><td>92.49%(-2.40%)</td><td>91.39%(-3.39%)</td></tr><tr><td>ISCX-Tor</td><td>98.30%(-0.84%)</td><td>98.50%(-0.61%)</td><td>97.50%(-0.71%)</td><td>98.00%(-0.66%)</td></tr><tr><td>CIC-IoT2023</td><td>86.80%(-6.53%)</td><td>85.90%(-6.83%)</td><td>87.20%(-6.89%)</td><td>86.55%(-6.86%)</td></tr><tr><td>CIC-AndMal</td><td>75.83%(-8.98%)</td><td>73.86%(-8.50%)</td><td>74.63%(-8.21%)</td><td>74.24%(-8.36%)</td></tr><tr><td>CSTNET-TLS 1.3</td><td>94.00%(-1.69%)</td><td>95.60%(-0.35%)</td><td>93.40%(-2.46%)</td><td>94.49%(-1.42%)</td></tr></table>

TABLE VIII: Ablation study of components of GenETC across ISCX-VPN(App) and CIC-AndMal datasets

<table><tr><td>Method</td><td>PT</td><td>DG</td><td colspan="2">AC</td><td colspan="2">RC</td><td colspan="2">PR</td><td colspan="2">F1</td></tr><tr><td>w/o MBM</td><td>√</td><td>√</td><td>95.01%</td><td>83.02%</td><td>91.45%</td><td>80.79%</td><td>91.09%</td><td>80.94%</td><td>91.27%</td><td>80.87%</td></tr><tr><td>w/o BFA</td><td>√</td><td>√</td><td>95.78%</td><td>83.72%</td><td>91.81%</td><td>81.05%</td><td>92.12%</td><td>81.41%</td><td>91.96%</td><td>81.23%</td></tr><tr><td>w/o PT&amp;DG</td><td>×</td><td>×</td><td>82.10%</td><td>53.57%</td><td>78.98%</td><td>53.85%</td><td>84.21%</td><td>56.60%</td><td>81.51%</td><td>55.19%</td></tr><tr><td>w/ Transformer</td><td>√</td><td>√</td><td>86.19%</td><td>75.04%</td><td>81.85%</td><td>71.63%</td><td>82.24%</td><td>69.93%</td><td>82.04%</td><td>70.77%</td></tr><tr><td>w/ CNN</td><td>√</td><td>√</td><td>83.25%</td><td>71.71%</td><td>78.54%</td><td>68.76%</td><td>82.99%</td><td>68.62%</td><td>80.71%</td><td>68.69%</td></tr><tr><td>w/ Max</td><td>√</td><td>√</td><td>94.85%</td><td>83.21%</td><td>90.62%</td><td>80.55%</td><td>91.14%</td><td>80.89%</td><td>90.88%</td><td>80.72%</td></tr><tr><td>w/ Attention</td><td>√</td><td>√</td><td>95.83%</td><td>83.85%</td><td>91.56%</td><td>81.12%</td><td>92.18%</td><td>81.75%</td><td>91.87%</td><td>81.43%</td></tr><tr><td>frozen DiESAGE</td><td>√</td><td>×</td><td>93.22%</td><td>81.55%</td><td>90.14%</td><td>78.24%</td><td>91.60%</td><td>79.37%</td><td>90.86%</td><td>78.80%</td></tr><tr><td>frozen BERT</td><td>×</td><td>√</td><td>30.15%</td><td>14.32%</td><td>23.85%</td><td>11.45%</td><td>26.42%</td><td>10.98%</td><td>25.07%</td><td>11.21%</td></tr><tr><td>GenETC(full model)</td><td>√</td><td>√</td><td>96.29%</td><td>84.81%</td><td>92.45%</td><td>82.36%</td><td>92.97%</td><td>82.84%</td><td>92.71%</td><td>82.60%</td></tr></table>

![](images/3fac6c4ba47da6efdd06719368bc21d5e1be0dac47d8f600ad0662bd484b0373.jpg)  
(a) ISCX-VPN (App) dataset

![](images/21416dc8fe4a8fea20633a1bd9b480f60e1bd684614dc265fa284c310db127b6.jpg)  
(b) CIC-IoT2023 dataset  
Fig. 4: Parameter sensitivity analysis w.r.t. traffic truncation parameters m across ISCX-VPN (App) and CIC-IoT2023 dataset

As shown in Fig. 4, experiments were conducted by varying the number of bytes retained from the beginning of each packet. On the ISCX-VPN(App) dataset, the F1 score consistently increases as the retained packet length grows, reaching its highest performance at 100 bytes. In contrast, on the CIC-IoT2023 dataset, the performance stabilizes once the retained length reaches approximately 60 bytes. This observation suggests that under different encryption scenarios, packets carry varying levels of useful information. Therefore, we choose to retain the first 100 bytes of each packet as a balanced compromise between model performance and computational cost, while ensuring that as much informative content as possible is preserved.

Moreover, although both our method and ET-BERT are based on pre-training strategies, our approach consistently achieves significantly higher accuracy across all packet lengths. This demonstrates the effectiveness of our proposed dynamic graph–enhanced pre-training mechanism in capturing richer and more discriminative representations from encrypted traffic.

3) Impact of N-gram BERT Representation: As described in Section III-B, raw input bytes are processed into byte-pair sequences, where each byte-pair, consisting of two adjacent bytes, serves as a token. In our setup, there is no overlap between adjacent tokens, which contrasts with the approaches used in ET-BERT and TrafficFormer. This non-overlapping tokenization significantly reduces computational overhead by nearly half, which is especially valuable for practical encrypted traffic analysis. In this part, we explore the effects of flow representations with and without token overlap on classification performance. We conduct a bigram flow representation for comparison, where one byte is shared between two adjacent tokens. For example, the string ‘e8e7323c65’ will be tokenized into e8e7, e732, 323c, 3c65 under the bigram scheme. We conduct comparison experiments under both non-overlapping and bigram tokenization schemes on the ISCX-VPN (Service) and CIC-IoT2023 datasets. While overlapping tokenization may appear to capture richer contextual information, our experimental results reveal that classification performance remains nearly identical between the two approaches. These results confirm that our chosen non-overlapping tokenization strategy offers a more balanced tradeoff between computational efficiency and classification accuracy, making it wellsuited for real-world encrypted traffic analysis scenarios.

4) Impact of Node-Disjoint Scenarios: To assess how well GenETC generalizes to unfamiliar network environments, we evaluate it under an inductive, node-disjoint train/test split. By ensuring no endpoints are shared between phases, this setup encourages the model to generalize based on learned structural patterns, operating without the direct benefit of transductive message passing.

As shown in Table IX, this shift to an inductive setting leads to a noticeable performance drop compared to the full model, with the F1-score on the CIC-AndMal dataset decreasing from 0.9001 to 0.6282. This drop is highly informative, demonstrating that GenETC achieves its most substantial gains in topology-rich environments by leveraging macroscopic communication regularities. However, this scenario also confirms the framework’s underlying effectiveness. Crucially, the nodedisjoint configuration consistently outperforms the pure semantic baseline (“w/o graph”), maintaining a higher F1-score (0.6282 versus 0.5729 on CIC-AndMal). These results offer a balanced perspective: while transductive structural priors drive the largest performance boosts, the dynamic graph module continues to provide meaningful structural augmentation for entirely unseen entities.

TABLE IX: Performance Comparison under Node-Disjoint Scenario

<table><tr><td>Dataset</td><td>Metric</td><td>w/o graph</td><td>node disjoint</td><td>full model</td></tr><tr><td rowspan="2">CIC-IoT2023</td><td>ACC</td><td>0.8042</td><td>0.8429</td><td>0.9782</td></tr><tr><td>F1</td><td>0.8037</td><td>0.8378</td><td>0.9691</td></tr><tr><td rowspan="2">CIC-AndMal</td><td>ACC</td><td>0.5733</td><td>0.6311</td><td>0.9027</td></tr><tr><td>F1</td><td>0.5729</td><td>0.6282</td><td>0.9001</td></tr></table>

## E. t-SNE Visualization

To further demonstrate the effectiveness of our method, we perform t-SNE visualizations on test samples from two representative datasets, CIC-IoT2023 and CIC-AndMal.

For the comparative experiment, we select two strong pretraining-based baselines, TrafficFormer and YaTC, and visualize their learned feature representations on the CIC-IoT2023 dataset. As illustrated in Fig. 5, our model produces more compact and well-separated clusters, while both TrafficFormer and YaTC exhibit scattered or partially overlapping regions, especially for classes with similar communication patterns. TrafficFormer tends to mix samples from related services due to its limited contextual modeling, and YaTC presents partially entangled clusters that fail to preserve class boundaries. In contrast, GenETC achieves distinct inter-class separability and tighter intra-class cohesion, indicating that our model captures more discriminative and robust representations even under highly similar encrypted IoT traffic.

For the ablation experiment, we visualize learned representations on the CIC-AndMal dataset under three settings: (a) without graph enhancement, (b) without pre-training, and (c) the full GenETC model. As shown in Fig. 6, the model without graph enhancement exhibits the most scattered feature distribution, with many malware families overlapping heavily due to the lack of interaction-aware contextual information. The model without pre-training performs better but still suffers from blurred cluster boundaries, suggesting that pre-training provides valuable prior knowledge for organizing latent features. In contrast, the full GenETC model produces clear, compact clusters with minimal overlap, revealing that dynamic graph enhancement and pre-training contribute synergistically to improving representation quality.

These visualizations further corroborate our quantitative findings: GenETC effectively disentangles complex encrypted traffic distributions, yielding discriminative and robust latent representations across diverse datasets and encryption scenarios.

## F. Scalability Evaluation

To evaluate the scalability of GenETC under realistic network loads, we conduct experiments on the CIC-IoT2023 and CIC-AndMal datasets. Specifically, while strictly maintaining the exact same class composition as the main experiments, we significantly increase the data volume to up to 2,000 samples per class. This generates graphs with approximately 86,000 edges, simulating typical active flow volumes in enterprise networks to rigorously test the model’s capacity and computational efficiency (Tables X and XI).

As detailed in Table XI, while baseline methods like TrafficFormer and YaTC show minor improvements with increased data, they still struggle to capture the complex structural variations inherent in large-scale traffic, resulting in significantly lower performance compared to GenETC. In contrast, our model maintains superior accuracy and F1 scores across both datasets. Crucially, this experiment validates the effectiveness of our Memory Bank mechanism, which successfully decouples memory usage from graph size, preventing Out-Of-Memory (OOM) errors even when processing tens of thousands of concurrent flows. Consequently, we conclude that GenETC is sufficiently scalable for practical deployment in standard network security environments, consistently delivering high performance and stable convergence as data volume increases.

TABLE X: Dataset statistics for scalability experiments

<table><tr><td>Datasets</td><td>#Nodes</td><td>#Edges</td><td>#Classes</td></tr><tr><td>CIC-IoT2023</td><td>34741</td><td>55481</td><td>34</td></tr><tr><td>CIC-AndMal</td><td>43467</td><td>85987</td><td>43</td></tr></table>

TABLE XI: Scalability evaluation results on the CIC-IoT2023 and CIC-AndMal datasets

<table><tr><td rowspan="2">Method</td><td colspan="2">CIC-IoT2023</td><td colspan="2">CIC-AndMal</td></tr><tr><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td></tr><tr><td>TrafficFormer [33]</td><td>0.9286</td><td>0.9295</td><td>0.5726</td><td>0.5744</td></tr><tr><td>YaTC [23]</td><td>0.9079</td><td>0.9140</td><td>0.6131</td><td>0.6101</td></tr><tr><td>Ours</td><td>0.9782</td><td>0.9691</td><td>0.9027</td><td>0.9001</td></tr></table>

![](images/c2b98064cb832a2acd05cd64ced97cba7d6862576cd676d5d8a705981503aede.jpg)  
Fig. 5: t-SNE visualization of learned representations learned by GenETC and two SOTA methods on the CIC-IoT2023 dataset.

![](images/936850b7736451d65efc460f6abf800cb40cd15ca850a514ba39c42b45a697ac.jpg)  
Fig. 6: t-SNE visualization of learned representations from the ablation study on the CIC-AndMal dataset.

## G. Complexity and Cost-Benefit Analysis

To rigorously evaluate the architectural trade-off, we analyze model parameters, resource consumption (FLOPs), and inference latency under standardized conditions (Table XII). Specifically, the reported per-sample inference time explicitly includes neighbor aggregation, Memory Bank refresh, and graph-update overhead, but excludes graph construction.

As shown in Table XII, GenETC’s total parameters and FLOPs remain nearly identical to the TrafficFormer baseline. The BERT backbone overwhelmingly dominates both metrics, while our DiESAGE module accounts for merely ∼0.14M parameters and ∼114M FLOPs. This confirms the computational burden is inherently driven by semantic encoding, with the graph module introducing a negligible compute overhead of less than 1%.

Regarding inference efficiency, GenETC requires 13.74ms per sample versus 5.82ms for TrafficFormer. Despite a negligible FLOPs increase, this latency gap occurs because fetching scattered high-dimensional data from the Memory Bank for neighbor aggregation creates frequent GPU cache misses, shifting the bottleneck to memory bandwidth. Fortunately, practical deployments can mitigate this via High Bandwidth Memory (HBM) GPUs and pipeline optimizations.

Compared to traditional lightweight models (e.g., DF, TSCRNN), GenETC undoubtedly incurs a significantly higher computational cost and inference latency. However, this tradeoff is highly justified in topology-rich environments where traffic is heavily obfuscated and indistinguishable using conventional statistical features. Crucially, our graph’s structural awareness permits aggressive flow truncation into fewer packets and bytes, maintaining accuracy while mitigating computational overhead.

TABLE XII: Comparison of Model Parameters, Inference Time, and FLOPs per Sample

<table><tr><td>Model</td><td>Parameters(M)</td><td>Inference Time(ms)</td><td>FLOPs(M)</td></tr><tr><td>DF</td><td>0.26</td><td>0.16</td><td>18</td></tr><tr><td>TSCRNN</td><td>0.72</td><td>0.21</td><td>24</td></tr><tr><td>TFE-GNN</td><td>44.35</td><td>3.16</td><td>306</td></tr><tr><td>YaTC</td><td>2.15</td><td>4.10</td><td>1440</td></tr><tr><td>TrafficFormer</td><td>131.63</td><td>5.82</td><td>12740</td></tr><tr><td>Ours</td><td>131.78</td><td>13.74</td><td>12854</td></tr></table>

## VI. DISCUSSION

In this section, we discuss the potential limitations of GenETC. 1) While GenETC effectively transfers generic bytelevel semantics across downstream tasks, we acknowledge its limitations in transferring macroscopic graph structures. Consequently, in strictly node-disjoint environments where endpoint identities are completely unseen, the framework experiences a noticeable performance drop. We interpret this as a reflection of the model’s dual capability: while its largest performance gains are naturally obtained in topology-rich transductive environments, GenETC remains fundamentally beneficial even in stricter inductive settings. Despite the absence of familiar endpoints, the graph module still yields a statistically significant improvement over pure semantic baselines by capturing localized, micro-level interaction patterns. 2) Integrating a pre-trained language model with a dynamic GNN introduces architectural complexity and scalability challenges when handling massive concurrent flows. While theoretical FLOPs remain comparable to semantic baselines, the discrete memory access required for graph operations increases inference latency. However, this overhead can be mitigated using High Bandwidth Memory (HBM) GPUs and asynchronous processing pipelines. Furthermore, the module’s utility is scenario-dependent: the latency trade-off is highly justified by substantial accuracy gains in topology-rich tasks (e.g., malware detection), whereas in highly anonymized networks (e.g., Tor), the graph module yields minimal benefit and can be disabled to conserve compute. To improve scalability and robustness in enterprise deployments, future research could combine temporal graph windowing with online updating to manage large-scale traffic and temporal concept drift, while anomalous-edge filtering may mitigate graph poisoning.

## VII. CONCLUSION

In this paper, we propose GenETC, a model that integrates the generalization strength of traffic pre-training with the structural learning of dynamic graphs by establishing a unified framework for dynamic feature co-evolution. It is the first approach to seamlessly integrate flow interaction patterns into the semantic space of pre-trained models via a feedback loop. During pre-training, we employ two domain-adapted tasks to capture the fundamental protocol syntax and interaction logic of raw traffic. During fine-tuning, we implement a dynamic graph updating strategy where edge attributes are iteratively refreshed to mutually refine semantic and topological representations. To verify its effectiveness, we finetune it with limited labeled data across various downstream traffic-specific tasks. Experimental results show that GenETC consistently outperforms state-of-the-art methods across six diverse datasets, demonstrating its robustness particularly in challenging scenarios with high obfuscation and data scarcity. Although this enhanced representational power entails higher computational costs than traditional ML approaches, the model remains practical for medium to high-resource systems, and future work will focus on optimizing it for deployment in resource-constrained environments.

## REFERENCES

[1] R. Sharma, S. Dangi, and P. Mishra, “A comprehensive review on encryption based open source cyber security tools,” in 2021 6th International Conference on Signal Processing, Computing and Control (ISPCC). IEEE, 2021, pp. 614–619.

[2] E. Papadogiannaki and S. Ioannidis, “A survey on encrypted network traffic analysis applications, techniques, and countermeasures,” ACM Computing Surveys (CSUR), vol. 54, no. 6, pp. 1–35, 2021.

[3] K. Thomas, F. Li, A. Zand, J. Barrett, J. Ranieri, L. Invernizzi, Y. Markov, O. Comanescu, V. Eranti, A. Moscicki et al., “Data breaches, phishing, or malware? understanding the risks of stolen credentials,” in Proceedings of the 2017 ACM SIGSAC conference on computer and communications security, 2017, pp. 1421–1434.

[4] G. Pellegrino, M. Johns, S. Koch, M. Backes, and C. Rossow, “Deemon: Detecting csrf with dynamic analysis and property graphs,” in Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security, 2017, pp. 1757–1771.

[5] B. Anderson and D. McGrew, “Machine learning for encrypted malware traffic classification: accounting for noisy labels and non-stationarity,” in Proceedings of the 23rd ACM SIGKDD International Conference on knowledge discovery and data mining, 2017, pp. 1723–1732.

[6] G. Li, J. Wu, S. Li, W. Yang, and C. Li, “Multitentacle federated learning over software-defined industrial internet of things against adaptive poisoning attacks,” IEEE Transactions on Industrial Informatics, vol. 19, no. 2, pp. 1260–1269, 2023.

[7] T. Van Ede, R. Bortolameotti, A. Continella, J. Ren, D. J. Dubois, M. Lindorfer, D. Choffnes, M. Van Steen, and A. Peter, “Flowprint: Semi-supervised mobile-app fingerprinting on encrypted network traffic,” in Network and distributed system security symposium (NDSS), vol. 27, 2020.

[8] Y. Mirsky, T. Doitshman, Y. Elovici, and A. Shabtai, “Kitsune: an ensemble of autoencoders for online network intrusion detection,” arXiv preprint arXiv:1802.09089, 2018.

[9] A. Panchenko, F. Lanze, J. Pennekamp, T. Engel, A. Zinnen, M. Henze, and K. Wehrle, “Website fingerprinting at internet scale.” in NDSS, 2016.

[10] M. Roesch et al., “Snort: Lightweight intrusion detection for networks.” in Lisa, vol. 99, no. 1, 1999, pp. 229–238.

[11] V. Paxson, “Bro: a system for detecting network intruders in real-time,” Computer networks, vol. 31, no. 23-24, pp. 2435–2463, 1999.

[12] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “Appscanner: Automatic fingerprinting of smartphone apps from encrypted network traffic,” in 2016 IEEE European Symposium on Security and Privacy (EuroS&P). IEEE, 2016, pp. 439–454.

[13] K. Al-Naami, S. Chandra, A. Mustafa, L. Khan, Z. Lin, K. Hamlen, and B. Thuraisingham, “Adaptive encrypted traffic fingerprinting with bidirectional dependence,” in Proceedings of the 32nd Annual Conference on Computer Security Applications, 2016, pp. 177–188.

[14] J. Gu and S. Lu, “An effective intrusion detection approach using svm with na¨ıve bayes feature embedding,” Computers & Security, vol. 103, p. 102158, 2021.

[15] W. Wang, M. Zhu, J. Wang, X. Zeng, and Z. Yang, “End-to-end encrypted traffic classification with one-dimensional convolution neural networks,” in 2017 IEEE international conference on intelligence and security informatics (ISI). IEEE, 2017, pp. 43–48.

[16] P. Sirinam, M. Imani, M. Juarez, and M. Wright, “Deep fingerprinting: Undermining website fingerprinting defenses with deep learning,” in Proceedings of the 2018 ACM SIGSAC conference on computer and communications security, 2018, pp. 1928–1943.

[17] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “Fs-net: A flow sequence network for encrypted traffic classification,” in IEEE INFOCOM 2019- IEEE Conference On Computer Communications. IEEE, 2019, pp. 1171–1179.

[18] M. Lopez-Martin, B. Carro, A. Sanchez-Esguevillas, and J. Lloret, “Network traffic classifier with convolutional and recurrent neural networks for internet of things,” IEEE access, vol. 5, pp. 18 042–18 050, 2017.

[19] K. Lin, X. Xu, and H. Gao, “Tscrnn: A novel classification scheme of encrypted traffic based on flow spatiotemporal features for efficient management of iiot,” Computer Networks, vol. 190, p. 107974, 2021.

[20] X. Xiao, W. Xiao, R. Li, X. Luo, H. Zheng, and S. Xia, “Ebsnn: Extended byte segment neural network for network traffic classification,” IEEE Transactions on Dependable and Secure Computing, vol. 19, no. 5, pp. 3521–3538, 2021.

[21] X. Xiao, S. Wang, G. Hu, Q. Li, K. Mao, X. Luo, B. Zhang, and S. Xia, “Rbljan: Robust byte-label joint attention network for network traffic classification,” IEEE Transactions on Dependable and Secure Computing, 2024.

[22] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in Proceedings of the ACM Web Conference 2022, 2022, pp. 633–642.

[23] R. Zhao, M. Zhan, X. Deng, Y. Wang, Y. Wang, G. Gui, and Z. Xue, “Yet another traffic classifier: A masked autoencoder based traffic transformer with multi-level flow representation,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 37, no. 4, 2023, pp. 5420–5427.

[24] H. Y. He, Z. G. Yang, and X. N. Chen, “Pert: Payload encoding representation from transformer for encrypted traffic classification,” in 2020 ITU Kaleidoscope: Industry-Driven Digital Transformation (ITU K). IEEE, 2020, pp. 1–8.

[25] T. N. Kipf and M. Welling, “Semi-supervised classification with graph convolutional networks,” arXiv preprint arXiv:1609.02907, 2016.

[26] W. Hamilton, Z. Ying, and J. Leskovec, “Inductive representation learning on large graphs,” Advances in neural information processing systems, vol. 30, 2017.

[27] P. Velickoviˇ c, G. Cucurull, A. Casanova, A. Romero, P. Lio, and Y. Ben-´ gio, “Graph attention networks,” arXiv preprint arXiv:1710.10903, 2017.

[28] Z. Wu, S. Pan, F. Chen, G. Long, C. Zhang, and S. Y. Philip, “A comprehensive survey on graph neural networks,” IEEE transactions on neural networks and learning systems, vol. 32, no. 1, pp. 4–24, 2020.

[29] H. Zhang, H. Yue, X. Xiao, L. Yu, Q. Li, Z. Ling, and Y. Zhang, “Revolutionizing encrypted traffic classification with mh-net: A multi-view heterogeneous graph model,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 39, no. 1, 2025, pp. 1048–1056.

[30] Y. Shi, G. Li, J. Wu, J. Li, and H. Fang, “Bpf-dag: Byte-packetflow features fusion via dynamic attributed graph for reliable encrypted traffic classification,” IEEE Transactions on Information Forensics and Security, vol. 21, pp. 197–211, 2025.

[31] W. Huang, G. Li, M. Chen, J. Li, and H. Zhu, “Silent penetrator: Breaching cross-domain federated fine-tuning via feature shift-induced backdoor,” IEEE Transactions on Information Forensics and Security, vol. 20, pp. 7106–7120, 2025.

[32] X. Yang, G. Li, K. Zhou, Y. Lai, and J. Li, “Auth-graph: Genaiempowered attribute-masked backdoor for on-demand authorizable graph learning,” Information Fusion, vol. 124, p. 103375, 2025. [Online]. Available: https://www.sciencedirect.com/science/article/pii/ S1566253525004488

[33] G. Zhou, X. Guo, Z. Liu, T. Li, Q. Li, and K. Xu, “Trafficformer: an efficient pre-trained model for traffic data,” in 2025 IEEE Symposium on Security and Privacy (SP). IEEE Computer Society, 2024, pp. 102–102.

[34] X. Hu, W. Gao, G. Cheng, R. Li, Y. Zhou, and H. Wu, “Towards early and accurate network intrusion detection using graph embedding,” IEEE Transactions on Information Forensics and Security, 2023.

[35] W. W. Lo, S. Layeghy, M. Sarhan, M. Gallagher, and M. Portmann, “Egraphsage: A graph neural network based intrusion detection system for iot,” in NOMS 2022-2022 IEEE/IFIP Network Operations and Management Symposium. IEEE, 2022, pp. 1–9.

[36] G. Duan, H. Lv, H. Wang, and G. Feng, “Application of a dynamic line graph neural network for intrusion detection with semisupervised learning,” IEEE Transactions on Information Forensics and Security, vol. 18, pp. 699–714, 2022.

[37] H. Zhang, L. Yu, X. Xiao, Q. Li, F. Mercaldo, X. Luo, and Q. Liu, “Tfe-gnn: A temporal fusion encoder using graph neural networks for fine-grained encrypted traffic classification,” in Proceedings of the ACM Web Conference 2023, 2023, pp. 2066–2075.

[38] C. Fu, Q. Li, and K. Xu, “Detecting unknown encrypted malicious traffic in real time via flow interaction graph analysis,” arXiv preprint arXiv:2301.13686, 2023.

[39] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware traffic classification using convolutional neural network for representation

learning,” in 2017 International conference on information networking (ICOIN). IEEE, 2017, pp. 712–717.

[40] W. Wang, Y. Sheng, J. Wang, X. Zeng, X. Ye, Y. Huang, and M. Zhu, “Hast-ids: Learning hierarchical spatial-temporal features using deep neural networks to improve intrusion detection,” IEEE access, vol. 6, pp. 1792–1806, 2017.

[41] X. Lin, G. Xiong, G. Gou, W. Dong, J. Yu, Z. Li, and W. Xia, “Respond to change with constancy: Instruction-tuning with llm for non-iid network traffic classification,” IEEE Transactions on Information Forensics and Security, 2025.

[42] M. Shen, J. Zhang, L. Zhu, K. Xu, and X. Du, “Accurate decentralized application identification via encrypted traffic analysis using graph neural networks,” IEEE Transactions on Information Forensics and Security, vol. 16, pp. 2367–2380, 2021.

[43] M. Wang, N. Yang, and N. Weng, “K-getnid: Knowledge-guided graphs for early and transferable network intrusion detection,” IEEE Transactions on Information Forensics and Security, 2024.

[44] J. Ham, D. Lee, and L. Saul, “Semisupervised alignment of manifolds,” in International Workshop on Artificial Intelligence and Statistics. PMLR, 2005, pp. 120–127.

[45] C. Wang and S. Mahadevan, “Manifold alignment without correspondence.” in IJCAI, vol. 2, 2009, p. 3.

[46] M. M. Bronstein, J. Bruna, Y. LeCun, A. Szlam, and P. Vandergheynst, “Geometric deep learning: going beyond euclidean data,” IEEE Signal Processing Magazine, vol. 34, no. 4, pp. 18–42, 2017.

[47] M. Belkin, P. Niyogi, and V. Sindhwani, “Manifold regularization: A geometric framework for learning from labeled and unlabeled examples.” Journal of machine learning research, vol. 7, no. 11, 2006.

[48] Z. Wu, Y. Xiong, S. X. Yu, and D. Lin, “Unsupervised feature learning via non-parametric instance discrimination,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2018, pp. 3733– 3742.

[49] K. He, H. Fan, Y. Wu, S. Xie, and R. Girshick, “Momentum contrast for unsupervised visual representation learning,” in Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2020, pp. 9729–9738.

[50] I. Sharafaldin, A. H. Lashkari, A. A. Ghorbani et al., “Toward generating a new intrusion detection dataset and intrusion traffic characterization.” ICISSp, vol. 1, no. 2018, pp. 108–116, 2018.

[51] E. Ghiasvand, S. Ray, S. Iqbal, S. Dadkhah, and A. A. Ghorbani, “Cicapt-iiot: A provenance-based apt attack dataset for iiot environment,” arXiv preprint arXiv:2407.11278, 2024.

[52] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of encrypted and vpn traffic using time-related,” in Proceedings of the 2nd international conference on information systems security and privacy (ICISSP), 2016, pp. 407–414.

[53] A. H. Lashkari, G. D. Gil, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of tor traffic using time based features,” in International Conference on Information Systems Security and Privacy, vol. 2. SciTePress, 2017, pp. 253–262.

[54] S. Dadkhah, H. Mahdikhani, P. K. Danso, A. Zohourian, K. A. Truong, and A. A. Ghorbani, “Towards the development of a realistic multidimensional iot profiling dataset,” in 2022 19th Annual International Conference on Privacy, Security & Trust (PST). IEEE, 2022, pp. 1–11.

[55] A. H. Lashkari, A. F. A. Kadir, L. Taheri, and A. A. Ghorbani, “Toward developing a systematic approach to generate benchmark android malware datasets and classification,” in 2018 International Carnahan conference on security technology (ICCST). ieee, 2018, pp. 1–7.

[56] T. Chen and C. Guestrin, “Xgboost: A scalable tree boosting system,” in Proceedings of the 22nd acm sigkdd international conference on knowledge discovery and data mining, 2016, pp. 785–794.
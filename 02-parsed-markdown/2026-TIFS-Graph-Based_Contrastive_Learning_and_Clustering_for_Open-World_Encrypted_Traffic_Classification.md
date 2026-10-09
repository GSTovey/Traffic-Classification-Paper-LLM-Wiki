# Graph-Based Contrastive Learning and Clustering for Open-World Encrypted Trafic Classification

Jigang Wen , Xiyu Zhang , Kun Xie , Member, IEEE, Yuxiang Zeng, Kun Huang, Yudian Ouyang , and Wei Liang

Abstract—Encrypted trafic classification is essential for modern network management and security, yet remains highly challenging due to payload encryption, data imbalance, and the emergence of unknown trafic classes. Existing methods often assume closed-world settings, rely on handcrafted features, or lack robustness in dynamic environments. To address these limitations, we propose a unified Graph-based Contrastive Learning and Clustering (GCLC) framework for encrypted trafic classification in open-world scenarios. Encrypted flows are modeled as trafic interaction graphs using lightweight packetlevel features. We train a Graph Neural Network (GNN) encoder with a hybrid loss function, integrating supervised contrastive learning and center-aware loss to promote the aggregation of samples into class clusters with clear boundaries between clusters. To enhance robustness under limited and imbalanced data, we design a trafic-aware graph augmentation strategy that simulates the variability of real-world network conditions. To discover new classes, we introduce a Mahalanobis distance-based new class detector and an adaptive model update mechanism that can detect and integrate unseen trafic classes. GCLC is evaluated on 3 public datasets and 1 self-collected dataset. Experimental results show that it outperforms existing methods on 4 evaluation metrics, with an open-set new class recognition accuracy of 95.02%. Even under scenarios of severe class imbalance and unknown classes, it still maintains high performance, exhibits strong robustness and adaptability, confirming the efectiveness of the framework in real-world encrypted dynamic trafic environments.

Index Terms—Encrypted trafic classification, graph augmentation, contrastive learning, graph neural networks (GNNs), graph-level clustering.

## I. INTRODUCTION

E <sup>NCRYPTED</sup> <sup>trafic</sup> <sup>classification</sup> <sup>has</sup> <sup>become</sup> <sup>a</sup> <sup>corner-</sup> stone task in modern networking, enabling a wide range of applications such as intrusion detection, quality-of-service (QoS) provisioning, policy enforcement, and applicationaware resource management. As more network services adopt encryption protocols like TLS, QUIC, and VPN to protect user privacy and circumvent network surveillance [1], [2], traditional classification methods are rapidly becoming obsolete. In this context, the demand for accurate, robust, and adaptive trafic classification under encryption and open-world conditions has grown more urgent than ever.

Traditional deep packet inspection methods, relying on port information [3] or plaintext payloads [4], are inefective under dynamic port allocation and encrypted trafic [5]. In modern encrypted environments, payloads are inaccessible, ports are ambiguous, and trafic patterns are highly variable [1]. Existing machine learning [6], [7], [8] and deep learning [9] approaches based on flow-level statistics partially alleviate these challenges but depend on shallow or handcrafted features, limiting their discriminative power [10], [11]. Moreover, most studies assume a closed-world setting [6], [12], [13], [14], [15], [16], rendering them incapable of handling previously unseen trafic. Overall, these methods remain insuficient for real-world encrypted trafic classification. Through a comprehensive analysis of existing trafic classification systems and their limitations, we identify the following three key challenges in achieving accurate classification in open and encrypted environments:

Challenge 1: Labeled Data Scarcity, Class Imbalance, and Struggles with Maintaining Performance in Dynamic Networks. Real-world trafic data is inherently imbalanced—trafic is predominantly dominated by popular applications, while emerging or specialized services are underrepresented. Moreover, acquiring labeled data is costly, and the existing amount of labeled data is insuficient. Additionally, network anomalies such as packet loss, retransmissions, and delay fluctuations further complicate trafic patterns, posing greater challenges to model robustness. These factors degrade the accuracy and generalization ability of models, especially in dynamic environments.

Challenge 2: Weakly Discriminative Features Lead to Embedding Overlap, Limiting Classification Accuracy.

Existing neural network–based trafic classification methods [9], [13], [14], [17], [18], [19] typically train on a mixture of features—such as statistical descriptors and byte-level signals—but these features often face limitations in their discriminative power [20], [21]. Technically, modern encryption (e.g., TLS 1.3) renders payloads pseudo-random, masking traditional signatures. Furthermore, macroscopic statistical descriptors frequently overlap between functionally similar applications and are highly susceptible to environmental noise like network jitter. Consequently, the embeddings learned for each trafic class exhibit limited separability. Even when some classification models employ contrastive learning [22], [23] to better capture class characteristics, the low-discriminability features still lead to blurry inter-class boundaries. As a result, flows from the same class may vary widely in the feature space, while flows from diferent classes may be indistinguishable, thereby reducing classification accuracy.

Challenge 3: Inability to Discover and Classify Unknown Classes. Most prior works operate under closed-world assumptions, where all trafic classes are known a priori. In real-world scenarios, however, new applications and trafic types constantly emerge. Conventional classifiers struggle to recognize unknown classes, while existing open-set recognition methods often perform poorly on encrypted trafic due to feature ambiguity and dataset imbalance.

To address these challenges, we propose a unified Graphbased Contrastive Learning and Clustering (GCLC) framework for encrypted trafic classification in openworld environments.

Our core idea is to model encrypted trafic as trafic interaction graphs, capturing structural correlations between packets using only lightweight and basic packet-level features such as size, direction, and timestamp. We employ a Graph Neural Network (GNN) encoder to extract high-level representations from these graphs. Besides employing a supervised contrastive learning module to pull positive samples together and push negative samples apart, we also introduce a center-aware loss to further enhance feature discriminability and promote the formation of clear, compact class clusters. In addition, we introduce imbalanced samples to further enhance the model’s robustness in handling dynamic environments and to mitigate data imbalance. Specifically, we propose a domain-specific graph augmentation strategy that generates new samples consistent with the characteristics of complex networks, thereby simulating trafic fluctuations in real-world networks. Finally, to support classification in open-world settings, we integrate a Mahalanobis distance-based new class detector along with an adaptive update mechanism, enabling the discovery and integration of new trafic classes.

## Our approach ofers the following key innovations:

1) Graph-based encrypted trafic modeling: Representing encrypted flows as trafic interaction graphs using simple packet-level features, enabling structural representation without relying on payload inspection or complex handcrafted features.

2) Trafic Graph Augmentation Strategy: Designing a graph-specific augmentation strategy tailored to network trafic, addressing issues of limited labeled data, class imbalance, and robustness in complex network environments by generating new samples aligned with real-world network characteristics.

3) Contrastive Clustering with Center-Aware Loss: Incorporating a residual projection head to preserve sample information, combining supervised contrastive learning with a center-aware objective to help the model learn highly discriminative features for forming well-defined and compact class clusters.

4) Open-World New Class Discovery: Integrating a Mahalanobis distance-based new class detector (for unknown new flows) and an adaptive model update strategy, enabling identification and integration of previously unseen trafic classes.

5) Comprehensive validation: Conducting extensive experiments on three public encrypted trafic datasets and one self-collected dataset. Experimental results show GCLC outperforms existing methods across four evaluation metrics, achieving an open-set discovery accuracy of 95.02%. The framework also demonstrates strong robustness under severe class imbalance and limited labeled data.

## II. RELATED WORK

Network trafic classification is critical for security monitoring, application identification, and network management. However, with the rise of encrypted protocols and increasingly complex trafic patterns, traditional methods have become less efective. This section reviews related work in three key areas: (i) conventional methods, (ii) machine learning-based approaches, and (iii) deep learning and graph-based methods.

Conventional Trafic Classification Methods: Early methods relied on static features such as IANA-assigned port numbers or protocol signatures. Port-based classification is now largely inefective due to port reuse and dynamic allocation (e.g., HTTPS on port 443) [3]. Deep packet inspection (DPI) [4] ofered higher accuracy by analyzing payloads, but it is limited against encrypted protocols (TLS, QUIC, VPN), incurs high computational costs, and raises privacy concerns. These limitations make traditional methods unsuitable for modern encrypted trafic.

Machine Learning-based Trafic Classification Methods: To overcome static rule-based approaches, machine learning (ML) techniques using flow-level statistical features have been explored. These include supervised methods (e.g., decision trees, SVM, random forests, KNN) and unsupervised methods like K-Means clustering [24], [25], [26], [27], [28], [29]. Studies like Williams and Zander [6] compared classifiers (e.g., C4.5, na¨ıve Bayes) with various feature selection strategies, analyzing flow-level features such as packet counts and byte counts. Este et al. [7] applied SVMs to multi-class classification for TCP flows, while Alshamari and Zincir-Heywood [8] focused on encrypted VoIP trafic, finding decision tree models like C4.5 performed best for interpretability. Taylor et al. [12] proposed AppScanner for encrypted mobile apps, though its reliance on static feature templates limits adaptability to openworld scenarios.

Deep Learning and Graph-Based Trafic Classification Methods: Deep learning (DL) models have gained prominence for their ability to automatically learn hierarchical patterns.

![](images/bcc5228a09d6480cf862dd82e18c1d99f1d4d0e91f3d709483bfe107f38ae175.jpg)  
Fig. 1. The client–application trafic interaction process.

CNNs, LSTMs, and MLPs [9], [17], [18], [19] have been applied to raw packet sequences, eliminating manual feature engineering. While efective in closed settings, DL models require large labeled datasets and often fail to generalize to new classes.

Graph-Based Trafic Classification: Graph neural networks (GNNs) have recently been explored for their capacity to capture structural dependencies in trafic. Liu et al. [13] used RNN-based models for encrypted trafic classification, while Shen et al. [14] introduced GraphDApp, which converts trafic into interaction graphs for GNN-based application fingerprinting. Jiang et al. [15] proposed FG-Net, using a flowrelationship graph to improve fingerprint stability, but still relies on supervised labels. Yang et al. [16] integrated GNNs and Transformers in MTSecurity to detect encrypted threats, although it is limited to security-specific use cases.

Open-Set Recognition and Adaptive Methods: To address the emergence of unknown classes, open set recognition (OSR) has gained attention. Threshold-based detectors [5], semisupervised temporal models [30], and masked autoencoder pretraining [10] have been proposed. Le et al. [11] introduced an adaptive model supporting incremental class updates. However, many of these rely on rigid feature templates, lack generalization, or require extensive tuning for deployment in dynamic environments.

Limitations of Existing Work: Despite advances in network trafic classification, existing methods still face significant limitations: real-world datasets are often sparse and imbalanced, making it dificult to train robust models; most approaches rely on closed-world assumptions, limiting their ability to identify new trafic classes; handcrafted or shallow features exhibit weak discriminative power in encrypted or obfuscated environments; unsupervised clustering tends to be fragmented or overlapping, reducing reliability; and incremental models incur high adaptation costs, with frequent updates and hyperparameter tuning constraining their deployment in dynamic network scenarios.

## III. PROBLEM STATEMENT AND MODEL OVERVIEW

## A. Problem Statement

Encrypted trafic classification in open network environments presents significant challenges due to the dynamic and heterogeneous nature of real-world network conditions. This work aims to develop a robust framework capable of accurately classifying both known (labeled) and unknown (unlabeled or new) trafic types, while addressing practical constraints such as limited labeled data, class imbalance, and the presence of emerging applications.

In this context, network trafic is generated as sequences of packets that reflect application-specific communication behaviors. As illustrated in Fig. 1, we collect complete session-level trafic during client-application interactions. Each packet in a session contains essential metadata such as IP addresses, port numbers, and protocol identifiers, which are crucial for routing, parsing, and analysis.

To enable efective classification, we group packets into flows. A flow is defined as a sequence of packets sharing the same 5-tuple, including source/destination IP addresses, source/destination ports, and transport-layer protocol. Notably, we consider bidirectional flows—packets with reversed source and destination fields are treated as part of the same logical flow.

Definition 1 (Flow): Let S denote the set of all observed packets. A flow ${ \textbf { \textit { F } } } \subseteq { \textbf { \textit { S } } }$ is a group of packets such that each packet $\boldsymbol { p } ^ { \mathrm { ~ ~ } } \in ~ \boldsymbol { F } ^ { \mathrm { ~ } }$ shares the same 5-tuple $( I P _ { s } , I P _ { d } , P o r t _ { s } , P o r t _ { d } , P r o t o c o l )$ , where $I P _ { s }$ and $I P _ { d }$ represent the source and destination IP addresses, $P o r t _ { s }$ and $P o r t _ { d }$ represent the source and destination ports, and Protocol is the transport protocol. If the source and destination address pair (i.e., $I P _ { s } , I P _ { d } , P o r t _ { s } , P o r t _ { d } )$ of two packets is reversed, they are still considered to belong to the same flow. That is, when the source and destination fields are swapped, the two packets are still regarded as belonging to the same flow.

In an open environment, the goal of trafic classification is not only to recognize known categories but also to detect and handle unknown categories. During the training phase, the model learns discriminative representations for known categories; during the inference phase, the model determines whether a new flow belongs to a known category or represents a new category. The definition is as follows:

Definition 2 (Open Environment Trafic Classification): Let $\mathcal { C } = \{ C _ { 1 } , C _ { 2 } , . . . , C _ { K } \}$ denote the set of known trafic categories, where each category $C _ { i }$ is associated with a labeled dataset $\mathcal { D } _ { i } = \{ ( f _ { 1 } , l _ { 1 } ) , . . . , ( f _ { m } , l _ { m } ) \}$ , where $f _ { j } \in \mathbb { R } ^ { d }$ is the feature vector and $l _ { j } \in C _ { i }$ is its label.

Assume the classifier M has been trained on these categories. For a new flow $U .$ , the model computes its feature representation $f _ { U } = \Phi ( U )$ . To determine its class membership, the model calculates the distance between $f _ { U }$ and the center $\mu _ { i }$ of each known class. If the distance $d ( f _ { U } , \mu _ { i } )$ is below a predefined threshold , U is assigned to category $C _ { i } ;$ otherwise, it is considered a candidate for a new class.

This paper adopts the Mahalanobis distance [31] as the similarity metric $d ( f _ { U } , \mu _ { i } ) = \ \sqrt { ( f _ { U } - \mu _ { i } ) ^ { \top } \Sigma _ { i } ^ { - 1 } ( f _ { U } - \mu _ { i } ) }$ , where $\mu _ { i }$ and $\Sigma _ { i }$ denote the mean vector and covariance matrix of category $C _ { i } ,$ respectively. In the context of our proposed GCLC framework, this feature representation $f _ { U }$ corresponds precisely to the projected graph embedding $z ^ { \prime }$ extracted by the GNN encoder, which will be detailed in subsequent sections.

## B. Model Overview

To address the challenges of encrypted trafic classification in open environments, we propose a novel framework named Graph-based Contrastive Learning Clustering (GCLC). This framework is designed to simultaneously classify known trafic types and discover new categories adaptively. It consists of two main stages: a training-phase and an execution-phase, as illustrated in Fig. 2.

![](images/f469e7ef2b493623131d44d97e762a15483bde0404863aa743c5866f283837b8.jpg)  
Fig. 2. Overview of the proposed GCLC framework. During training, labeled trafic graphs are used in supervised contrastive clustering to form distinct class clusters. During execution, new flows are embedded and compared against known clusters for classification or new class detection.

## Training Phase Modules:

(1) Trafic Interaction Graph Construction: Packet sequences are aggregated into flows and transformed into graph representations using basic packet-level features. This approach captures application-specific interaction patterns without relying on complex manual features.

(2) Trafic Augmentation: To address the issues of data scarcity, class imbalance, and struggles with maintaining performance in dynamic networks in complex network environments, we propose a graph-based data augmentation strategy. This strategy generates additional samples that align with network characteristics by simulating variations in network behaviors, thereby enhancing the model’s robustness and generalization ability.

(3) Feature Extraction: A Graph Neural Network (GNN) encoder is trained to learn graph-level embeddings. The encoder leverages neighborhood aggregation and shallow architecture to eficiently capture discriminative features.

(4) Graph Contrastive Clustering: In addition to using supervised contrastive learning to encourage embeddings of the same class to cluster tightly while maximizing inter-class separation, we also introduce a center-aware loss to make the boundaries of dificult class clusters clearer and improve cluster compactness.

## Execution Phase Modules:

(1) Trafic Interaction Graph Construction: New flows are processed into graph form using the same procedure as in training.

(2) Trafic Augmentation: The proposed graph-based data augmentation strategy is used to simulate variations in network behaviors, generating samples that align with network characteristics to construct contrastive learning positive and negative sample pairs, addressing the issue of limited data.

(3) Feature Extraction: The pretrained GNN encoder (with frozen parameters) extracts embeddings for incoming flows.

(4) New Class Discoverer: By determining an appropriate threshold based on class-conditional Mahalanobis distances, the distance between each flow embedding and the centers of existing class clusters is compared against the threshold to decide whether the flow belongs to a new class.

## IV. METHODOLOGY

This section presents the detailed design of the proposed framework, encompassing the construction of trafic interaction graphs, the graph augmentation strategy, the design of the graph-based feature extractor, the supervised contrastive clustering mechanism, and the process for discovering new trafic categories.

## A. Trafic Interaction Graph Construction

Modeling encrypted trafic as graphs ofers significant advantages in capturing both structural and temporal dependencies inherent in network flows. Such representations are particularly suitable for variable-length trafic sequences and enable structure-aware learning via Graph Neural Networks (GNNs). This graph-based abstraction enhances the model’s capability to discriminate between trafic categories based on subtle behavioral patterns and communication dynamics.

Due to the heterogeneity of application-layer protocols and communication behaviors, trafic flows inherently exhibit diverse structural patterns. To efectively capture these variations, we construct a Trafic Interaction Graph (TIG) for each flow, based on lightweight packet-level attributes: packet size, direction and inter-arrival time.

As illustrated in Fig. 3, each directed arrow denotes a packet transmission between the client and server. The numeric value indicates the packet size, with its sign representing direction: positive values (in orange) denote upstream packets from client to server, while negative values (in blue) denote downstream packets from server to client.

To retain both temporal correlations and structural semantics, we adopt a graph representation strategy inspired by [32], forming a unified and expressive representation for downstream tasks. The construction of the TIG consists of the following three components:

Vertices: Each node in the TIG corresponds to a packet in the flow. Nodes are annotated with the signed packet size and indexed by their sequence order. Packet direction is encoded by node color (orange for upstream, blue for downstream), and packets with the same direction are grouped into distinct layers to capture directional communication patterns. Within each layer, packets are temporally ordered and connected accordingly.

Edges: Edges in the TIG are categorized into two types:

Intra-layer edges: These edges connect temporally adjacent packets within the same direction (layer), preserving finegrained temporal ordering and local dependencies.

Inter-layer edges: These edges encode transitions between communication directions and are constructed using the following rules: The first node in each layer is connected to the first node in the subsequent layer.The last node in each layer is connected to the last node in the subsequent layer.This design captures the bidirectional nature of application-level interactions.

Edge Weights: To incorporate temporal dynamics, edge weights are assigned based on inter-arrival times between connected packets. Recognizing that network-induced noise (e.g., jitter, delay) may introduce variability, we discretize inter-arrival time into two coarse-grained categories: Shortterm: Intervals less than or equal to 1 second are encoded with a weight of 1. Long-term: Intervals greater than 1 second are encoded with a weight of 0.01. This empirical constant mitigates network noise like collisions. During GNN aggregation, this near-zero weight acts as a soft-pruning mechanism, attenuating message passing across arbitrary delays to focus on semantically meaningful packet bursts.

This coarse-grained time encoding improves robustness to temporal noise while preserving macro-level timing characteristics.

Example Construction: Fig. 4 shows the resulting TIG corresponding to the example flow in Fig. 3, with a packet size sequence $[ 6 4 , - 1 8 4 , 4 8 4 , - 6 4 , - 6 4 , 1 6 0 , 1 1 8 , - 1 6 4 , 6 5 2 ]$ . The vertex set is initialized as $V = [ 6 4 , - 1 8 4 , 4 8 4 , - 6 4 , - 6 4 ,$ , 160, $1 1 8 , \mathit { \Theta } - 1 6 4 , \mathit { \Theta } 6 5 2 ]$ , and edge weights are determined by interarrival intervals $E = [ 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 0 . 0 1 ]$ . Intra-layer and inter-layer edges are established iteratively according to the rules above. The final graph $G = ( V , E )$ represents the desired Trafic Interaction Graph.

![](images/34170d3d6411a490e42dc83e4886bf21a9f74619fa1c7628701d628433aae275.jpg)  
Fig. 3. Packet-level client-server interaction for flows.

![](images/187649f47723e36a47b30a539e19c7138f49eed9e83c875bde12ad7f6dd51fe8.jpg)  
Fig. 4. Trafic interaction graph (TIG) for flows.

## B. Graph Augmentation Strategy for Trafic With Insuficient Labeled Data, Class Imbalance, and Robustness

Real-world trafic datasets often face issues of limited labeled data and class imbalance, with common applications dominating the trafic, while niche or emerging applications are underrepresented. This imbalance causes models to rely heavily on features from the common classes, neglecting the details of the minority classes, leading to poor performance on minority trafic and reduced accuracy. Additionally, due to the high cost of acquiring labeled data, the existing labeled data is insuficient, which lowers the model’s generalization ability.

Network anomalies such as packet loss, retransmissions, and fluctuating delays further complicate trafic patterns, challenging model robustness, especially when labeled data is scarce.

To address these challenges, we propose a domain-specific graph augmentation strategy tailored for TIGs. This method aims to: (i) mitigate class imbalance by synthetically enriching minority class samples, (ii) enhance robustness to networkinduced anomalies, and (iii) preserve the semantic integrity of encrypted trafic behavior.

Let the original dataset be defined as $\mathcal { D } = \{ ( G _ { i } , y _ { i } ) \ | \ i =$ $1 , . . . . , N _ { t o t a l } \}$ , where $G _ { i }$ is a TIG sample and $y _ { i } \in \{ 1 , 2 , . . . , K \}$ is its class label. For a given class $^ { c , }$ let $\mathcal { D } _ { c } = \{ G _ { i } \ | \ y _ { i } = c \}$ and $| \mathcal { D } _ { c } | = n _ { c }$ . We define a set of augmentation operations as $\boldsymbol { \mathcal { A } } \ = \ \{ \mathcal { A } _ { 1 } , \mathcal { A } _ { 2 } , \mathcal { A } _ { 3 } \}$ . where: $\mathcal { A } _ { 1 } \colon$ Random Node Addition (simulating packet retransmission). $\boldsymbol { A } _ { 2 } \colon$ : Random Node Dropping (simulating packet loss). $\mathcal { A } _ { 3 } \colon$ Edge Attribute Perturbation (simulating variable delay).

For any graph G, an augmentation operation is selected uniformly at random $\hat { G } = \mathcal { A } _ { k } ( G ) , \quad k \sim$ Uniform{1 2 3}. Let $\begin{array} { r } { n _ { \operatorname* { m a x } } = \operatorname* { m a x } _ { c } \frac { n _ { c } } { 2 } } \end{array}$ denote the target number of samples per class. Each class c is augmented until $| \mathcal { D } _ { c } ^ { \prime } | = n _ { \operatorname* { m a x } }$ . The final balanced dataset is $\begin{array} { r } { \mathcal { D } ^ { \prime } = \bigcup _ { c = 1 } ^ { \overline { { K } } } \mathcal { D } _ { c } ^ { \prime } } \end{array}$

In practical network environments, events such as packet loss, retransmission, and delay jitter occur infrequently. Therefore, augmentation operations are applied with low probability, simulating realistic noise patterns while preserving the overall semantics of trafic interaction. We now describe each augmentation operation in detail.

![](images/5784a8518539104fb5068c3c0938ab7b9b6c7fbc7b0ca8d7795742e3c1486b5f.jpg)  
Fig. 5. Illustration of various network trafic perturbations: (a) Random node dropping, (b) Random node addition, and (c) Edge attribute perturbation.

Random Node Dropping: To emulate packet loss, a subset of nodes is randomly removed from the TIG. Associated edges are also deleted, and the graph is reindexed to preserve consistency. This simulates scenarios where packets are dropped due to congestion or transmission errors. As encrypted trafic often tolerates minor packet loss without losing its semantic structure, this operation preserves essential flow characteristics. As shown in Fig. 5a, node 9 is removed to simulate packet loss.

Random Node Addition: This operation simulates packet retransmission, which commonly occurs in response to network errors. Within each directional layer of a TIG (i.e., consecutive upstream or downstream packets), a new node is inserted after the last packet. The inserted node inherits the size and direction of its predecessor and is connected to maintain temporal ordering. As shown in Fig. 5b, a duplicate packet is inserted to simulate retransmission.

Edge Attribute Perturbation: To simulate temporal variability (e.g., RTT fluctuations), we randomly perturb a subset of edge weights in the TIG. Specifically, edge weights are toggled between $1  0 . 0 1$ , modeling transitions between short-term and long-term delays. The selection follows an i.i.d. uniform distribution across both intra- and inter-directional edges. As illustrated in Fig. 5c, we simulate delay variation by modifying edge weights.

These augmentation operations collectively enhance the model’s ability to generalize across imbalanced, noisy, and evolving trafic environments.

## C. Feature Extraction

To facilitate efective representation learning over graphstructured trafic data, we propose a feature extraction module that integrates multi-layer graph convolution with residual projection. The objective is to capture both local and global structural patterns within flows, enhance the semantic expressiveness of Trafic Interaction Graphs (TIGs), and produce high-quality embeddings for downstream classification and clustering tasks.

The module consists of three main components: (a) multilayer GraphSN-based graph encoding, (b) hierarchical feature fusion, and (c) a residual projection head.

## Graph Feature Encoding via GraphSN:

In the initial stage of feature extraction, we utilize multiple stacked GraphSN layers to perform node-level message passing and representation learning. Each GraphSN unit incorporates a learnable adjacency adaptation mechanism, allowing dynamic adjustment of the graph structure to suppress over-smoothing while preserving meaningful node-level distinctions. Specifically, the adjusted adjacency matrix A<sup>˜</sup> is computed as $\tilde { \textbf { A } } = ( 1 - \mathbf { I } ) \cdot \mathbf { A } + \mathbf { I } \cdot \mathrm { d i a g } ( e )$ · diag(A), where $\mathbf { A } \in \overline { { \mathbb { R } } } ^ { N _ { \nu } \times N _ { \nu } }$ is the original adjacency matrix, $\mathbf { I } \in \mathbb { R } ^ { N _ { \nu } \times N _ { \nu } }$ is the identity matrix, and $e \in \mathbb { R } ^ { N _ { \nu } }$ is a learnable parameter vector that controls the scaling of self-loops. This formulation enables the model to regulate the influence of each node’s own features during propagation.

Node embeddings are then updated as $\begin{array} { r l r l } { X ^ { \prime } } & { { } } & { = } & { { } } \end{array}$ ReLU  Linear  MLP(A<sup>˜</sup> X), where $\bar { \boldsymbol { X } _ { \mathrm { ~ \scriptsize ~ \in ~ } } } \mathbb { R } ^ { N _ { \nu } \times d }$ is the input node feature matrix, $X ^ { \prime } \in \mathbb { R } ^ { N _ { \nu } \times d ^ { \prime } }$ is the updated node feature matrix, and d and $d ^ { \prime }$ are the input and hidden dimensions, respectively. MLP denotes a multi-layer perceptron, and ReLU is the non-linear activation function. Batch normalization is applied between layers to stabilize training and improve convergence.

## Multi-Scale Feature Fusion:

To preserve information at multiple levels of abstraction, we retain the intermediate outputs from each GraphSN layer. At the end of the encoding phase, we concatenate the outputs of all layers, along with the original input features, to form a multi-scale representation. Let $X ^ { ( l ) } \in \mathsf { \overline { { R } } } ^ { N _ { \nu } \times d ^ { \prime } }$ represent the output of the l-th GraphSN layer. The multi-scale concatenation is $H = \operatorname { C o n c a t } ( X ^ { ( 0 ) } , X ^ { ( 1 ) } , \overbrace { \phantom { \sum _ { k = 1 } ^ { 3 } } } ^ { \cdot } X ^ { ( L ) } ) \in \mathbb { R } ^ { N _ { \nu } \times d ^ { \prime } \cdot ( L + 1 ) }$ , where L is the total number of GraphSN layers, and $d ^ { \prime }$ is the number of hidden units. This fusion strategy ensures that both finegrained local structures and high-level global semantics are captured.

The concatenated node embeddings are aggregated along the node dimension using a readout operation (e.g., summation or mean pooling) to derive a fixed-size graph-level representation vector $z \in \mathbb { R } ^ { d ^ { \prime } \cdot ( L + 1 ) }$ , This aggregated vector z is used as the input to the residual projection head.

## Residual Projection Head:

To project the high-dimensional representation z into a lower-dimensional embedding space suitable for contrastive learning or clustering, we introduce a Residual Projector module. This component follows a dual-path design: The main path applies two fully connected layers interleaved with batch normalization and ReLU activation, focusing on extracting nonlinear transformations. The residual shortcut directly propagates the original input z through a linear projection.The final projected embedding is computed as $z ^ { \prime } = \mathbf { M a i n P a t h } ( z ) +$ Shortcut(z), where $z \in \mathbb { R } ^ { d ^ { \prime } \cdot ( L + 1 ) }$ is the high-dimensional feature vector and $z ^ { \prime } \in \mathbb { R } ^ { d _ { p r o j } }$ is the final projected embedding, with $d _ { p r o j }$ being the projection dimension. This design preserves the semantic continuity of the original features while enhancing the learning of task-relevant representations.

Augmented View Encodingfor Contrastive Learning: To further enhance robustness and generalization, we integrate graph augmentation directly into the feature extraction pipeline. Specifically, two independent augmentations are applied to the input TIG, where each augmentation is randomly selected from the predefined set $\boldsymbol { \mathcal { A } } = \{ \mathcal { A } _ { 1 } , \mathcal { A } _ { 2 } , \mathcal { A } _ { 3 } \}$ . This results in two structurally perturbed but semantically consistent graph views.

![](images/da3026df8d52873eae6584c7c4ecb34f96fe599dce5a1ceacd2b0f14d1d02825.jpg)  
Fig. 6. Illustration of the dual-branch loss: $\mathcal { L } _ { \mathrm { s u p c o n } }$ pulls samples of the same class closer and pushes those of diferent classes apart, while $\mathcal { L } _ { \mathrm { c e n t e r } }$ encourages clustering around class centers and separates diferent class clusters.

These augmented views are processed by a shared encoder, producing embeddings $z _ { 1 } ^ { \prime }$ and $z _ { 2 } ^ { \prime } ,$ which form a positive pair in the contrastive learning framework. This mechanism encourages the model to learn invariant representations under structural perturbations, facilitating improved intra-class compactness and inter-class separation.

To obtain negative pairs, we adopt a supervised contrastive learning strategy: Views from the same class (original and augmented) are treated as positive pairs; Views from diferent classes are treated as negative pairs.

By jointly optimizing both positive and negative objectives, the model learns to distinguish semantically meaningful variations while remaining resilient to structural noise. This ultimately contributes to enhanced classification performance, especially in open and dynamic network environments.

## D. Graph Contrastive Learning Clustering

Trafic flows from the same application class often exhibit latent commonalities, while flows from diferent classes diverge significantly due to variations in protocol stacks, service behaviors, and communication semantics. Our goal is to cluster trafic interaction graphs in the embedding space such that trafic samples from the same class are tightly clustered, while samples from diferent classes are well separated.

To achieve this goal, we employ a dual-branch contrastive learning framework to enhance class discriminability. Unlike traditional methods that rely on simple supervised contrastive learning, we introduce a center-aware loss to form internally compact, clearly separated, and non-confused class clusters. While traditional supervised contrastive learning can bring similar trafic samples closer and push dissimilar ones apart, it struggles when faced with classes that have subtle feature similarities. To address this issue, we incorporate a centeraware loss to improve the separation of hard-to-distinguish clusters, making the overall clustering more compact and ensuring each class forms a distinct cluster. Fig. 6 illustrates the efects of these two loss functions.

The two branches share a common encoder and projection head. Each graph sample is projected into the embedding space, where class cluster centers are also learned. The training objective jointly optimizes the supervised contrastive loss and center-aware loss (composed of intra-class aggregation, interclass separation, and nearest cluster classification), ensuring that similar samples are grouped together in the feature space, diferent class clusters are adequately separated, and classification is achieved using the “sample-nearest cluster” decision.

## Supervised Contrastive Loss:

Given the two augmented views per graph produced by the feature-extraction module (for each original graph $G _ { i }$ we obtain $\tilde { G } _ { i } ^ { ( 1 ) }$ and $\tilde { G } _ { i } ^ { ( 2 ) } )$ , we encode them with shared weights to obtain two embeddings per sample. Denote the (optionally \` -normalized) embeddings by $\hat { \mathbf { z } } _ { u } ^ { \prime } = \mathbf { z } _ { u } ^ { \prime } / \lVert \mathbf { z } _ { u } ^ { \prime } \rVert _ { 2 }$ . For a minibatch of B original graphs, we thus have 2B views; index them by $u \in \{ 1 , . . . , 2 B \}$ with class label $y _ { u }$

We adopt the supervised contrastive objective (one anchor per view). Define the positive set for anchor u as $\mathcal { P } ( u ) =$ $\{ \nu ~ \in ~ \{ 1 , . . . , 2 B \} ~ \backslash ~ \{ u \} ~ | ~ y _ { \nu } ~ = ~ y _ { u } \} ,$ , and define $\begin{array} { r l } { \mathcal { N } ( u ) } & { { } = } \end{array}$ $\left\{ 1 , . . . . , 2 B \right\} \ \backslash$ {u}. The (temperature-scaled) cosine similarity is given by $\begin{array} { r } { s _ { u \nu } = \frac { \hat { \mathbf { z } } _ { u } ^ { \prime \top } \hat { \mathbf { z } } _ { \nu } ^ { \prime } } { \tau } } \end{array}$ . The per-anchor loss and the batch loss are $\begin{array} { r } { \ell _ { u } ^ { \mathrm { s u p } } = - \frac { 1 } { | \mathcal { P } ( u ) | } \sum _ { \nu \in \mathcal { P } ( u ) } ^ { \ast } \log \frac { \exp ( s _ { u \nu } ) } { \sum _ { a \in \mathcal { N } ( u ) } \exp ( s _ { u a } ) } , \mathcal { L } _ { \mathrm { s u p c o n } } = \frac { 1 } { 2 B } \sum _ { u = 1 } ^ { 2 B } \ell _ { u } ^ { \mathrm { s u p } } } \end{array}$ This pulls embeddings of the same class (including cross-view pairs of the same sample/class) together while pushing away embeddings from diferent classes.

## Center-aware Loss:

In addition to using supervised contrastive learning to bring similar samples closer and push dissimilar ones apart, we also introduce a center-aware loss to enhance cluster separation, ensuring each class is compact and distinct. ${ \mathcal { L } } _ { \mathrm { c e n t e r } } = \lambda _ { \mathrm { i n t r a } } { \mathcal { L } } _ { \mathrm { i n t r a } } + \lambda _ { \mathrm { i n t e r } } { \mathcal { L } } _ { \mathrm { i n t e r } } + \lambda _ { \mathrm { c l s } } { \mathcal { L } } _ { \mathrm { c l s } }$ , where the three terms respectively promote (i) $\mathcal { L } _ { \mathrm { { i n t r a } } } \mathrm { { : } }$ intra-class compactness, $( \mathrm { i i } ) \mathcal { L } _ { \mathrm { i n t e r } } \mathrm { : }$ inter-class separation with adaptive margins, and (iii) $\mathcal { L } _ { \mathrm { c l s } }$ :sample-to-own-center nearest-neighbor consistency.

(i) Intra-class Compactness. Let K be the set of classes present in the current training epoch, and $S _ { k } = \{ u : y _ { u } = k \}$ the index set of samples (across both views) of class k, with $S = \textstyle \bigcup _ { k \in { \mathcal { K } } } S _ { k }$ and $| S | = 2 B$ . For each class $k ,$ denote its center by c<sub>k</sub> $\mathbf { c } _ { k }$

We define normalized inverse-distance weights as $\begin{array} { r l } { w _ { u } } & { { } = } \end{array}$ ${ \frac { { \frac { 1 } { d ( { \bf z } _ { u } ^ { \prime } , { \bf c } _ { k } ) + \epsilon } } } { \sum _ { v \in S _ { k } } { \frac { 1 } { d ( { \bf z } _ { v } ^ { \prime } , { \bf c } _ { k } ) + \epsilon } } } } , \quad u \in S _ { k }$ . We penalize the (weighted) squared deviation of samples from their class center:

$$
\mathcal { L } _ { \mathrm { i n t r a } } = \frac { 1 } { | S | } \sum _ { u \in S } w _ { u } \big ( \boldsymbol { \alpha } \cdot d ( \mathbf { z } _ { u } ^ { \prime } , \mathbf { c } _ { y _ { u } } ) \big ) ^ { 2 } ,\tag{1}
$$

where $w _ { u }$ assigns larger weights to samples closer to the class center, allowing prototype updates to be guided by more representative instances while reducing the influence of noisy or outlying samples.

(ii) Inter-class Separation. Let $d _ { i j } = d ( \mathbf { c } _ { i } , \mathbf { c } _ { j } )$ be the center distance for classes $i \neq j .$ We adapt pairwise margins by class dificulty. Define the dificulty of class k by

$$
d _ { k } = \frac { \frac { 1 } { | S _ { k } | } \sum _ { u \in S _ { k } } d ( \mathbf { z } _ { u } ^ { \prime } , \mathbf { c } _ { k } ) } { \frac { 1 } { | K \backslash \{ k \} | } \sum _ { j \in K \backslash \{ k \} } d ( \mathbf { c } _ { k } , \mathbf { c } _ { j } ) } .\tag{2}
$$

Let $\rho \in ( 0 , 1 ) \ ( \mathrm { e . g . } , \rho = 0 . 7 )$ and define the “hard-class” set H as the top-ρ fraction of classes with the largest $d _ { k } .$ . Set the pair-type scaling:

$$
s _ { i j } = \left\{ \begin{array} { l l } { 1 . 5 , \quad i \in { \mathcal { H } } , \ j \in { \mathcal { H } } , } \\ { 1 . 3 , \quad \mathrm { e x a c t l y ~ o n e ~ o f ~ } { i } , { j \in { \mathcal { H } } } , \qquad m _ { i j } = m _ { 0 } \cdot s _ { i j } , } \\ { 1 . 0 , \quad \mathrm { o t h e r w i s e } , } \end{array} \right.
$$

with base margin $m _ { 0 } \ > \ 0$ . We use a non-linear margin penalty

$$
\varphi ( d _ { i j } , m _ { i j } ) = \left\{ \begin{array} { l l } { 5 \left( \displaystyle { \frac { m _ { i j } - d _ { i j } } { m _ { i j } } } \right) ^ { 2 } , } & { d _ { i j } < m _ { i j } , } \\ { \displaystyle { \frac { 1 } { 2 } \exp \left( - \frac { d _ { i j } - m _ { i j } } { 2 } \right) } , } & { d _ { i j } \geq m _ { i j } , } \end{array} \right.
$$

it over unordered pairs $\begin{array} { r } { \mathbf { \mathcal { P } } = \{ ( i , j ) ^ { \prime } \in \mathcal { K } \times \mathcal { K } : i < j \} : \mathcal { L } _ { \mathrm { i n t e r } } = } \end{array}$ $\begin{array} { r } { \frac { 1 } { | \mathcal { P } | } \sum _ { ( i , j ) \in \mathcal { P } } \varphi ( d _ { i j } , \bar { m _ { i j } } ) } \end{array}$

(iii) Nearest Neighbor Margin Loss. For each sample $u ,$ define $d _ { u } ^ { + } = d ( { \bf z } _ { u } ^ { \prime } , { \bf c } _ { y _ { u } } )$ and $\begin{array} { r } { d _ { u } ^ { - } \ = \ \operatorname* { m i n } _ { j \in \mathcal { K } \backslash \{ y _ { u } \} } d ( \mathbf { z } _ { u } ^ { \prime } , \mathbf { c } _ { j } ) } \end{array}$ . We enforce that u is closer to its own center than to any other center by a margin $\begin{array} { r } { \gamma > 0 ; \mathcal { L } _ { \mathrm { c l s } } = \frac { 1 } { | S | } \sum _ { u \in S } w _ { u } [ d _ { u } ^ { + } - d _ { u } ^ { - } + \gamma ] _ { + } } \end{array}$ $[ x ] _ { + } = \operatorname* { m a x } ( x , 0 )$

Weighting by $w _ { u }$ emphasizes boundary and outlying samples.

Final Objective and Prediction:

The total training objective combines supervised contrast and center-aware regularization, ${ \mathcal { L } } _ { \mathrm { t o t a l } } ~ = ~ { \mathcal { L } } _ { \mathrm { s u p c o n } } + \eta { \mathcal { L } } _ { \mathrm { c e n t e r } }$ with trade-of $\eta \ > \ 0 .$ . At inference, we assign labels by nearest center, $\hat { y } = \arg \operatorname* { m i n } _ { k \in \mathcal { K } } d ( \mathbf { z } ^ { \prime } , \mathbf { c } _ { k } )$ , which is consistent with the training-time nearest-center margin term $\mathcal { L } _ { \mathrm { c l s } }$ . During training, we select the sample within each class that has the minimum distance to all other samples as the class center, $\begin{array} { r } { u ^ { \star } = \arg \operatorname* { m i n } _ { u \in S _ { k } } \sum _ { \nu \in S _ { k } } d ( \mathbf { z } _ { u } ^ { \prime } , \mathbf { z } _ { \nu } ^ { \prime } ) , \quad \mathbf { c } _ { k } \gets \mathbf { z } _ { u ^ { \star } } ^ { \prime } } \end{array}$

At the end of each training epoch, we perform a momentum update: $\mathbf { c } _ { k } \gets m \cdot \mathbf { c } _ { k } + ( 1 - m ) \cdot \tilde { \mathbf { c } } _ { k }$ , where $\begin{array} { r } { \widetilde { \mathbf { c } } _ { k } = \sum _ { u \in S _ { k } } w _ { u } \mathbf { z } _ { u } ^ { \prime } } \end{array}$ . We set $m = 0 . 9$ to provide temporal smoothing, which mitigates the “moving target” problem and ensures stable convergence by acting as a consistent anchor in the feature space.

## E. New Class Discoverer

This section presents a new-class discovery method that identifies and clusters unknown classes by combining Mahalanobis distance–based new class detection with eigengapdriven adaptive spectral clustering. First, new samples are detected via Mahalanobis distance, with a global threshold determined via a hold-out validation strategy to prevent data leakage. Next, spectral clustering guided by the eigengap heuristic groups the new samples. After discovering new classes, the model is incrementally updated—covering label assignment, model extension, and contrastive loss updates—enabling dynamic adaptation to new classes and improved classification performance.

Mahalanobis Distance-Based New Class Detection: To detect new classes, we model the distribution of each known class k using its mean $\begin{array} { r c l } { \mu _ { k } } & { = } & { \frac { 1 } { n _ { k } } \sum _ { i = 1 } ^ { n _ { k } } z _ { i } ^ { ' ( k ) } } \end{array}$ and covariance $\begin{array} { r l r } { \Sigma _ { k } } & { = } & { \frac { 1 } { n _ { k } - 1 } \sum _ { i = 1 } ^ { n _ { k } } ( z _ { i } ^ { ' ( k ) } - \mu _ { k } ) ( z _ { i } ^ { ' ( k ) } \hat { \mathrm { ~ - ~ } } \mu _ { k } ) ^ { T } + \beta { \bf I } } \end{array}$ , and compute the Mahalanobis distance for a test sample z<sup>0</sup>, $d _ { M } ( z ^ { \prime } , k ) =$ $\sqrt { ( z ^ { \prime } - \mu _ { k } ) ^ { T } \Sigma _ { k } ^ { - 1 } ( z ^ { \prime } - \mu _ { k } ) }$ . Here, we empirically set the regularization parameter $\beta$ to $1 0 ^ { - 6 }$ . This small constant acts as a numerical stabilizer, ensuring that the high-dimensional covariance matrix remains strictly positive-definite and invertible without distorting the underlying feature distributions.

This distance accounts for feature correlations and is more robust than Euclidean distance in high-dimensional spaces.

To determine the global threshold $\theta _ { \mathrm { g l o b a l } }$ without accessing real novel classes (which would constitute data leakage), we employ a hold-out validation strategy. We partition the known training classes into a fitted subset and a hold-out subset (acting as pseudo-unknown classes). By plotting the ROC curve on this validation set and maximizing the Youden index, we obtain an optimal distance cut-of. Since absolute distance values vary with model capacity and class count, we map this cut-of to its corresponding cumulative percentile $P _ { o p t }$ within the fitted classes’ distance distribution. Finally, we apply this scale-invariant percentile $P _ { o p t }$ to the distance distribution of the final trained model to set the operational threshold $\theta _ { \mathrm { g l o b a l } }$ A test sample is considered new if min<sub>k</sub> $d _ { M } ( z ^ { \prime } , k ) > \theta _ { \mathrm { g l o b a l } }$

Adaptive Clustering via Spectral Eigengap:

For the new sample set $S _ { \mathrm { n e w } }$ , we perform spectral clustering to discover latent classes. A similarity matrix W is built using the RBF kernel, $\begin{array} { r l r } { W _ { i j } } & { { } = } & { \exp \left( \frac { - | z _ { i } ^ { \prime } - z _ { j } ^ { \prime } | ^ { 2 } } { 2 \sigma ^ { 2 } } \right) } \end{array}$ , where $\sigma ~ = ~ \mathrm { m e d i a n } \Big ( d ( z _ { i } ^ { \prime } , z _ { j } ^ { \prime } ) : i < j , z _ { i } ^ { \prime } , z _ { j } ^ { \prime } \in S _ { \mathrm { n e w } } \Big )$ . The normalized Laplacian is defined as ${ \bf L } _ { \mathrm { n o r m } } = { \bf I } - { \bf D } ^ { - 1 / 2 } { \bf W } { \bf D } ^ { - 1 / 2 }$ . We then compute the eigenvalues $\lambda _ { 1 } \leq \ldots \leq \lambda _ { m }$ , and determine the optimal number of clusters $K _ { n e w } ^ { * } = \arg \operatorname* { m a x } _ { K _ { n e w } } ( \lambda _ { K _ { n e w } + 1 } - \lambda _ { K _ { n e w } } )$ based on the eigengap heuristic. This identifies the most significant separation in the spectral domain, after which we apply K-means with $K _ { n e w } ^ { * }$ to cluster the new samples.

Incremental Model Update:

Once new clusters are discovered, the model is updated as follows: Each new cluster $C _ { k _ { n e w } }$ is assigned a temporary mathematical label $K + k _ { n e w }$ , where K is the number of known classes. While the system autonomously isolates these novel clusters, assigning their actual semantic meanings requires a periodic human-in-the-loop review. A new encoder is initialized with shared parameters and an updated output layer. New samples are integrated into the supervised contrastive loss using updated class labels. New class centers are computed using local density weights, $\begin{array} { r c l } { \mu _ { k _ { n e w } } } & { = } & { \frac { \sum _ { i : y _ { i } = k _ { n e w } } \rho _ { i } z _ { i } } { \sum _ { i : y _ { i } = k _ { n e w } } \rho _ { i } } } \end{array}$ . A test sample is then classified by its closest updated center, $\begin{array} { r } { \hat { y } = \arg \operatorname* { m i n } _ { k = 1 , \ldots , K + K _ { n e w } ^ { * } } \| z - \mu _ { k } \| } \end{array}$ . Using the updated encoder to reassign class labels, recalculating the mean value $\mu _ { K }$ of each class, and updating the similarity matrix and covariance matrix parameters.

## V. EXPERIMENTS

We conduct a series of experiments to evaluate the performance of the proposed GCLC framework, aiming to address the following key questions: 1) How does GCLC perform compared with other methods in the closed-world classification task? 2) Can GCLC efectively identify new classes of trafic in the open-world classification task? 3) Can GCLC enable trafic clusters of each class to have clear boundaries in the feature space? 4) What is the convergence speed and stability of GCLC? 5) How does the choice of threshold afect the performance of new trafic class identification? 6) Can GCLC meet the low-latency inference requirements for realworld deployment? 7) What are the contributions of each key component to the overall performance?

TABLE I  
SUMMARY OF BASELINE METHODS FOR ENCRYPTED TRAFFIC CLASSIFICATION
<table><tr><td>Model</td><td>Year</td><td>Input Features</td><td>Learning Paradigm</td><td>Core Design Idea</td><td>Unknown Flow Recognition</td></tr><tr><td>AppScanner [12]</td><td>2016</td><td>handcrafted Statistical features from TCP flows</td><td>Supervised learning on traditional classes</td><td>Uses self-collected data for mobile app detection under strict conditions</td><td>x</td></tr><tr><td>FS-Net [13]</td><td>2019</td><td>Flow sequences with direction encoding</td><td>Seq2Seq + reconstruction-based learning</td><td>Reconstructs sequence-level features for better flow semantics</td><td>x</td></tr><tr><td>FlowPrint [30]</td><td>2020</td><td>Domain-specific features with temporal correlation</td><td>Semi-supervised learning with labeled anchors</td><td>Uses behavioral fingerprinting based on time-location consistency</td><td>√</td></tr><tr><td>GraphDApp [14]</td><td>2021</td><td>Traffic Interaction Graph(TIG)</td><td>GNN-based supervised training</td><td>Captures flow directionality and structure-aware embeddings</td><td>x</td></tr><tr><td>FG-Net [15]</td><td>2022</td><td>Flow-Relationship Graph(FRG)</td><td>Supervised GNN classification</td><td>Encodes flow-level hierarchy for anomaly and app detection</td><td>x</td></tr><tr><td>YaTC [10]</td><td>2023</td><td>Multi-layer flow visualization with Transformer</td><td>Transformer + MAE pretraining + fine-tuning</td><td>Learns flow patterns adaptively with cross-view supervision</td><td>√</td></tr><tr><td>Velatin [11]</td><td>2024</td><td>Deep features + adaptive classifier</td><td>Supervised + incremental adaptation</td><td>Learns class boundaries adaptively in open environments</td><td>√</td></tr></table>

## A. Experiment Settings

Datasets: To comprehensively evaluate our method, we conduct experiments on four real-world encrypted trafic datasets that span a wide range of applications, network conditions, and trafic behaviors:

APPLICATIONS 21 (Self-Collected): This dataset consists of TLS-encrypted trafic from 21 popular applications. To capture real-world dynamics, data was collected via Wireshark on Windows 10/11 laptops and desktops from Sept. to Nov. 2023, spanning residential Wi-Fi, campus LAN (peak/ofpeak), and 4G/5G hotspots. We use 17,203 flows for training and 4,301 flows for testing.

ISCX-VPN Dataset [33]: A dataset designed for VPN trafic analysis. We extract 13 VPN-related application classes and use 2,660 flows for training and 664 flows for testing.

USTC-TFC Dataset [34]: Comprising trafic from 10 benign applications and 10 malware families. One class is excluded due to extreme imbalance, resulting in 19 active classes. The training and test sets contain 15,667 and 3,741 flows, respectively.

VNAT Dataset [35]: A VPN/Non-VPN dataset with trafic from 10 applications across five functional categories: Streaming, VoIP, Chat, Command & Control, and File Transfer. We use 4,094 flows for training and 1,021 flows for testing.

Baselines: We compare GCLC against seven representative methods, a comparative summary of these baselines is shown in Table I.

The selected baselines cover a variety of classification paradigms, including classical, sequence-based, graph-based, and transformer-based methods. Notably, only models such as FlowPrint [30] and Velatin [11] explicitly support openworld scenarios. Therefore, GCLC is compared with these two models specifically in terms of new trafic identification performance.

Evaluation Metrics: To evaluate classification performance, we adopt four standard metrics: accuracy (AC), precision

(PR), recall (RC), and F1 score. These metrics are defined TP+TN   
as follows: Accuracy $\begin{array} { r } { = \ \frac { \imath \imath \mp \imath \imath } { T P + T N + F P + F N } } \end{array}$ , Precision $\begin{array} { r } { { } = { } \frac { T P } { T P + F P } , } \end{array}$ Recall $\begin{array} { r l r } { \mathrm { ~ } } & { { } } & { = \frac { T P } { T P + F N } , F 1 = 2 \mathrm { ~ } \times \frac { \mathrm { P r e c i s i o n } \times \mathrm { \hat { R e c a l l } } } { \mathrm { P r e c i s i o n } + \mathrm { R e c a l l } } } \end{array}$ , where: $\mathbf { T P } =$ true positives, TN = true negatives, FP = false positives, FN = false negatives.

Implementation Details: All experiments were conducted using PyTorch 2.4.1 with CUDA acceleration. The model was trained on a workstation equipped with an NVIDIA GeForce RTX 4090 GPU.

During training, we used a batch size of 128 and employed the Adam optimizer with an initial learning rate of $2 . 5 \times 1 0 ^ { - 3 }$ A learning rate decay factor of 0.5 was applied when validation performance plateaued. Weight decay (i.e., $L _ { 2 }$ regularization) was set to $2 \times 1 0 ^ { - 3 }$ to prevent overfitting.

The graph augmentation hyperparameters were empirically selected based on validation performance: Node dropping ratio: 0.05, Edge perturbation ratio: 0.10, Node addition ratio: 0.05. These augmentations specifically target minority classes to mitigate imbalance. The 0.05 ratio physically simulates a realistic 5% packet loss and retransmission rate, introducing robust network noise without destroying core structural semantics. Unless otherwise specified, all experiments adhere to this configuration. Each experiment was repeated three times with diferent random seeds, and the average performance is reported.

## B. Closed-World Classification Performance

In closed-world classification tasks, GCLC achieves the best overall performance and obtains the highest scores on most metrics, demonstrating excellent and stable performance. As shown in Table II, GCLC achieves an accuracy of 96.84% on APPLICATIONS21, outperforming the secondbest FG-Net (93.67%) by 3.17%. On the ISCX-VPN dataset, its F1-score reaches 98.08%, exceeding the runner-up by 2.46%. This advantage mainly stems from the graph encoder’s eficient modeling of structural and temporal features, along with the unified integration of graph augmentation, contrastive learning, and residual projection, which together balance eficiency and generalization. Moreover, the multi-metric joint optimization strategy further ensures balanced performance, enabling GCLC to remain stable and efective across domains.

TABLE II  
PERFORMANCE COMPARISON ACROSS MULTIPLE DATASETS AND METHODS
<table><tr><td rowspan="2">Method</td><td colspan="4">APPLICATIONS21</td><td colspan="4">ISCX-VPN</td><td colspan="4">USTC-TFC</td><td colspan="4">VNAT</td></tr><tr><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td></tr><tr><td>AppScanner [12]</td><td>90.33</td><td>89.23</td><td>91.96</td><td>90.57</td><td>78.62</td><td>78.32</td><td>79.19</td><td>78.75</td><td>63.71</td><td>61.09</td><td>64.11</td><td>62.37</td><td>88.62</td><td>87.91</td><td>90.10</td><td>88.26</td></tr><tr><td>FS-Net [13]</td><td>74.89</td><td>73.72</td><td>74.74</td><td>74.23</td><td>82.94</td><td>81.97</td><td>83.12</td><td>82.54</td><td>70.19</td><td>68.10</td><td>71.92</td><td>69.13</td><td>85.10</td><td>83.84</td><td>84.36</td><td>84.47</td></tr><tr><td>FlowPrint [30]</td><td>61.43</td><td>59.29</td><td>61.23</td><td>60.24</td><td>70.21</td><td>69.13</td><td>70.95</td><td>70.03</td><td>58.03</td><td>55.30</td><td>56.21</td><td>56.63</td><td>71.37</td><td>69.84</td><td>72.07</td><td>70.60</td></tr><tr><td>GraphDApp [14]</td><td>79.14</td><td>78.07</td><td>79.13</td><td>78.60</td><td>81.33</td><td>79.96</td><td>80.92</td><td>80.44</td><td>79.02</td><td>78.17</td><td>78.91</td><td>78.59</td><td>85.13</td><td>83.30</td><td>84.92</td><td>84.21</td></tr><tr><td>FG-Net [15]</td><td>93.67</td><td>92.63</td><td>91.26</td><td>91.94</td><td>96.78</td><td>95.08</td><td>96.17</td><td>95.62</td><td>95.33</td><td>93.39</td><td>95.83</td><td>94.35</td><td>98.77</td><td>96.80</td><td>98.94</td><td>97.78</td></tr><tr><td>YaTC [10]</td><td>89.12</td><td>87.82</td><td>89.83</td><td>88.81</td><td>83.28</td><td>81.29</td><td>82.39</td><td>81.84</td><td>80.71</td><td>78.70</td><td>78.62</td><td>79.69</td><td>85.29</td><td>82.19</td><td>82.35</td><td>83.71</td></tr><tr><td>Velatin [11]</td><td>85.67</td><td>84.38</td><td>86.12</td><td>85.24</td><td>91.67</td><td>90.94</td><td>92.16</td><td>91.55</td><td>85.33</td><td>85.78</td><td>86.04</td><td>85.55</td><td>94.20</td><td>93.60</td><td>93.69</td><td>93.90</td></tr><tr><td>Ours</td><td>96.84</td><td>93.12</td><td>97.13</td><td>95.08</td><td>98.16</td><td>97.73</td><td>98.44</td><td>98.08</td><td>96.54</td><td>94.18</td><td>98.09</td><td>95.35</td><td>98.83</td><td>96.47</td><td>99.13</td><td>97.64</td></tr></table>

TABLE III  
NEW CLASS DETECTION ON APPLICATIONS 21
<table><tr><td>Method</td><td>ACC</td><td>PR</td><td>Recall</td><td>F1</td></tr><tr><td>FlowPrint</td><td>57.43</td><td>56.14</td><td>55.84</td><td>55.99</td></tr><tr><td>Velatin</td><td>83.67</td><td>81.97</td><td>82.23</td><td>82.10</td></tr><tr><td>Ours</td><td>95.02</td><td>94.71</td><td>96.45</td><td>95.57</td></tr></table>

## C. Open-World Classification Performance

In the open-world classification task, we evaluate the model’s recognition ability for unseen trafic classes. We constructed an open-world scenario based on the APPLI-CATIONS 21 dataset by removing three application classes from the training set (treated as new classes during testing), and compared GCLC with FlowPrint [30] and Velatin [11], the two models capable of handling open-world scenarios, in terms of new trafic identification performance. To ensure a fair comparison, all models were evaluated using the exact same raw trafic dataset. However, since our proposed graph augmentation strategy involves topological operations specific to Trafic Interaction Graphs (TIGs), it cannot be directly applied to non-graph baseline models. Therefore, FlowPrint and Velatin were evaluated using their native feature extraction pipelines and optimal default configurations as proposed in their respective original papers. This setup ensures that we are comparing the overall architectural designs and core classification logics in their intended, optimal states.

As shown in Table III, GCLC performs excellently in the open-world setting: it achieves an accuracy of 95.02%, significantly outperforming Velatin (83.67%) and FlowPrint (57.43%), while also ranking first in precision, recall, and F1-score.

These results indicate that GCLC possesses strong generalization and robustness in open-world classification of unseen trafic. Its advantages stem from a highly separable embedding space constructed via contrastive learning, the precise detection mechanism based on Mahalanobis distance, and a unified framework integrating new class detection and classification.

TABLE IV  
CLUSTERING METRICS COMPARISON
<table><tr><td>Method</td><td>Clustering Accuracy</td><td>Sil.</td><td>Sep.</td></tr><tr><td>K-means</td><td>25.33</td><td>0.27</td><td>0.35</td></tr><tr><td>SC</td><td>43.93</td><td>0.41</td><td>0.58</td></tr><tr><td>AC</td><td>34.52</td><td>0.33</td><td>0.46</td></tr><tr><td>Ours</td><td>93.42</td><td>0.73</td><td>0.87</td></tr></table>

## D. Clustering Performance Evaluation

## Overall Clustering Performance:

To evaluate the unsupervised clustering capability of the proposed framework, we compared it with three classical algorithms (K-means [29], Spectral Clustering (SC) [36], and Agglomerative Clustering (AC) [37]) on the APPLICA-TIONS 21 dataset. Using three metrics—Clustering Accuracy (ACC), Silhouette Score (Sil.), and Inter-cluster Separation (Sep.)—and verifying via clustering visualization (Fig. 7) and dynamic t-SNE visualization during training (Fig. 8), the results show the proposed method significantly outperforms baselines across all metrics and visualization dimensions.

The proposed method exhibits outstanding performance in all metrics (Tab. IV): it achieves a clustering accuracy of 93.42%, nearly 4 times that of K-means (25.33%) and about 2 times that of SC (43.93%); the Silhouette Score is 0.73 and Inter-cluster Separation is 0.87, both significantly higher than SC’s 0.41 and 0.58. In terms of visualization, baseline algorithms show obvious cluster overlaps (marked by red boxes), while the proposed method yields compact clusters with clear boundaries (Fig. 7).

This result benefits from the integration of a supervised contrastive objective and a center-aware design, enabling tight intra-cluster cohesion and clear inter-cluster boundaries. Dynamic t-SNE visualization reveals that from Epoch 1 to Epoch 40, initially scattered embeddings gradually form compact and well-separated clusters (Fig. 8), intuitively verifying its excellent performance in the process from feature learning to cluster formation, as well as its advantages in intracluster compactness and inter-cluster separability.

![](images/5cc67d02b34b2945d10d6dd7dd3718b4b1cbefe050bb5dacf02bf5adbaa17b02.jpg)  
(a) K-means

![](images/93b6222d792537d0e69e7a2c3cc4f206550ad2da4b24dc05e1591809ba39f217.jpg)  
(b) SC

![](images/54dba6546e958676b6d7348be0a17fcbe23fd540f7f12efe36865f0ace8a471e.jpg)  
(c) AC

![](images/65e8c022b9b5d73b75362d737d216595c507121064821e0d0acd911144d5ded6.jpg)  
(d) Ours  
Fig. 7. Clustering visualization: comparison between our model and three classical clustering algorithms.

![](images/84cc2f15c5f7213c3053959dd2a3cab5ab6aeb12445c972948245678527afb5d.jpg)  
(a) Epoch 1

![](images/7df29bb2dfd975efa1b6184a1cb01e18e5b54927a9eb84bb29b055ee49eba394.jpg)  
(b) Epoch 10

![](images/5437f09e4d47ac713120b066f176c1342b4bcccb2fe2ef8f46f0b97f334bb9ae.jpg)

![](images/5a0417a2ab143f0cdbb210503c0bd8f85ce616c3159744e94db466ed227a0078.jpg)  
(c) Epoch 25  
(d) Epoch 40

Fig. 8. t-SNE visualization: as training proceeds, clusters become progressively compact and well-separated.  
![](images/84eb96101d213c8338b682c48323803006548a6f6899bf9592e549349c3bb6ae.jpg)  
(a) SupCon-only

![](images/97ca6e30a232e204a953c2c5772f0898b62899b91f7a786a0fc4114ac84911b3.jpg)

![](images/1743b8a77b059f09b7076aae2573bd32d6d97fde398b8c6c2b23561c38d35c14.jpg)  
(b) Center-only  
(c) SupCon + Center  
Fig. 9. Ablation t-SNE on APPLICATIONS 21: combining SupCon and Center-aware losses produces the most compact and clearly separated clusters.

Efectiveness of Supervised Contrastive and Center-aware Losses: To evaluate the contribution of the supervised contrastive loss (SupCon) and center-aware loss (Center) to clustering quality, three configurations are designed on the APPLICATIONS 21 dataset: “SupCon-only,” “Center-only,” and “SupCon+Center.” Their performance is compared using clustering accuracy (ACC), Silhouette score (Sil.), inter-cluster separation (Sep.), and t-SNE visualization. The results show that “SupCon+Center” performs best across all metrics, confirming that their combination can significantly improve clustering accuracy, intra-cluster compactness, and inter-cluster separability.

As shown in Table V, “SupCon+Center” achieves an ACC of 93.42%, higher than “SupCon-only” (90.41%) and “Center-only” (89.73%), with superior Sil. and Sep. metrics. In the visualization (Fig. 9), “SupCon-only” exhibits obvious cluster overlaps (marked by red boxes), “Centeronly” still has some cluster mixing (marked by red circles), while “SupCon+Center” produces compact clusters with clear boundaries and no overlaps.

TABLE V  
ABLATION ON LOSS DESIGN: SUPCON-ONLY VS. CENTER-ONLY VS. BOTH (OURS) ON APPLICATIONS 21
<table><tr><td>Setting</td><td>ACC (%)</td><td>Sil.</td><td>Sep.</td></tr><tr><td>SupCon-only</td><td>90.41</td><td>0.67</td><td>0.61</td></tr><tr><td>Center-only</td><td>89.73</td><td>0.54</td><td>0.69</td></tr><tr><td>SupCon + Center</td><td>93.42</td><td>0.73</td><td>0.87</td></tr></table>

This indicates that SupCon excels at bringing similar samples closer and pushing dissimilar ones apart, but lacks suficient inter-cluster boundaries and intra-cluster compactness. Center optimizes cluster boundaries but sufers from scattered intra-cluster samples. The combination leverages the advantages of both local alignment and global structural regularization, thereby improving clustering accuracy and separability.

## E. Convergence Behavior

We conducted experiments on four encrypted trafic datasets, evaluating convergence using four key metrics: ACC, PR, RC, and F1. As shown in Fig. 10, bfGCLC achieves fast convergence across all datasets and metrics, demonstrating its eficient learning capability and strong generalization.

In this experiment, GCLC exhibits rapid convergence on all evaluation metrics. The model reaches over 80% accuracy by the 10th epoch and converges by the 40th epoch, demonstrating its ability to quickly learn discriminative features and achieve high class separability. Recall exceeds 90% at the 10th epoch, confirming GCLC’s stable detection capability even under imbalanced data. F1 scores surpass 95% across all datasets, highlighting its robustness under diverse traffic conditions. These evaluation results validate the model’s robustness, class separability, and generalization ability in various encrypted trafic scenarios.

## F. Threshold Selection and Validation

In the New Class Discoverer module (Sec. IV-E), we determine whether a sample belongs to a new trafic class by calculating its distance to the cluster centers of existing classes. Thus, an efective threshold needs to be selected to separate new classes from known classes. However, selecting this threshold using ground-truth novel classes from the test set violates the strict open-world assumption. To address this, we implemented a zero-leakage hold-out validation strategy to determine the threshold autonomously.

![](images/5508a21856b739d8df1ede6fa0156bea241793d54000db10700a5756aea94611.jpg)  
(a) ACC

![](images/3c4bfabe2127fbb222e659b3c7016f326a76fd2e59ee2dabcc6cb299badcdb2c.jpg)  
(b) PR

![](images/35beec89473f81f6213c441542010d43aafedf3c484c11fe73a8502f115e9e5c.jpg)  
(c) RC

![](images/ac61783fef4b92b2ab9c86e372312f2f9e8a2829e9d87b4b486e3c00d4b62d46.jpg)  
(d) F1

Fig. 10. Performance of GCLC across four datasets and evaluation metrics.  
![](images/97ab3c5fb6cb2c131791920095e5ea5c2db7ea3c74d2a2b0080eefef6530f704.jpg)  
(a) Calibration ROC Curve

![](images/9f8f7e72ca0e51b39adbb1f5ec0ee29ea1f7b3bed5511cb1cc6e5c3acfba9adb.jpg)  
(b) Youden Index

![](images/739759902b3495129b02be70560a751b8bdb504643c50a25154377ba9a18a7cc.jpg)  
(c) Distance Distribution Analysis

![](images/581fb2684a0cfadab80de1afd805c981f5677589b0f917011cd34759753a00e4.jpg)  
(d) Cumulative Distribution Function  
Fig. 11. Threshold selection via ROC and distance distribution analysis, showing clear separation between fitted and hold-out classes.

First, we partitioned the known training dataset into 15 fitted classes and 3 hold-out classes (simulated as pseudounknowns). Using a calibration model trained solely on the fitted classes, we evaluated the Mahalanobis distances for both subsets. As shown in the calibration ROC curve (Fig. 11a and Fig. 11b), the model accurately distinguished the two sets with an AUC of 0.996. By maximizing the Youden index, we identified the optimal absolute cut-of for this calibration state at 216.411.

However, the absolute Mahalanobis distance is highly sensitive to the scale and compactness of the feature space, which naturally shifts when the final model is trained on all 18 known classes. Therefore, instead of transferring a rigid numerical value, we extract and transfer the underlying statistical decision boundary. As depicted in the cumulative distribution function (CDF) and distance distribution plots for the calibration phase (Fig. 11c and Fig. 11d), the optimal threshold of 216.411 accurately intercepts the 98.8th percentile of the fitted classes’ distance distribution. This 98.8% coverage serves as our universal, scale-invariant decision strategy, balancing “known-class coverage” and “new-class misclassification risk”.

For final deployment, we applied this 98.8th percentile rule to the distance distribution of the final 18-class model. In this more tightly clustered feature space, the 98.8th percentile corresponds to an adaptive global threshold of 19.76. As illustrated in the final open-set evaluation (Fig. 12), the transferred threshold of 19.76 precisely separates the density cores of the 18 known classes and the 3 completely unseen real novel classes. The density core of known classes lies almost entirely to the left of the threshold, while that of new classes lies to the right, ultimately achieving minimal distribution overlap. This confirms that transferring the statistical percentile strategy guarantees highly accurate class distinction while strictly adhering to zero-leakage open-world protocols.

![](images/96e597c0739fd0d7736df11a6412fe4cbd430522e83eb0f8e1294f58643a7954.jpg)  
Fig. 12. Density distributions of Mahalanobis distances for known (blue) and novel (red) classes, with the zero-leakage threshold at 19.76 marked by the green dashed line.

## G. Computational Complexity and Latency Analysis

While Mahalanobis detection introduces $O ( d ^ { 2 } )$ inference and $O ( d ^ { 3 } )$ covariance matrix update complexities, GCLC efectively mitigates these for real-time deployment. First, our GNN projects inputs into a highly compact embedding space $( d \approx 1 4 4 )$ , rendering dense operations trivial. On an RTX 4090 GPU, average per-flow inference takes ∼1.8 ms (distance calculation $< 0 . 0 4$ ms). Second, the $O ( d ^ { 3 } )$ matrix inversion is executed asynchronously in the background upon aggregating new-class samples. This periodic update requires merely 1.5 ms, ensuring zero blocking overhead. Thus, GCLC fully satisfies the strict low-latency requirements of dynamic networks.

TABLE VI  
ABLATION STUDY OF KEY COMPONENTS
<table><tr><td>Model</td><td>ACC</td><td>PR</td><td>Recall</td><td>F1</td></tr><tr><td>Full Model</td><td>95.02</td><td>94.71</td><td>96.45</td><td>95.57</td></tr><tr><td>w/o GA</td><td>92.61</td><td>90.01</td><td>92.91</td><td>91.44</td></tr><tr><td>w/o GCC</td><td>66.71</td><td>64.78</td><td>68.59</td><td>66.63</td></tr><tr><td>w/o NCD</td><td>88.68</td><td>78.49</td><td>91.72</td><td>84.59</td></tr><tr><td>w/o GA + NCD</td><td>85.38</td><td>70.72</td><td>87.11</td><td>78.06</td></tr><tr><td>w/o GA + GCC</td><td>49.23</td><td>44.59</td><td>51.90</td><td>47.97</td></tr><tr><td>w/o GCC + NCD</td><td>41.15</td><td>39.93</td><td>42.45</td><td>41.15</td></tr></table>

Abbreviations: GA: Graph Augmentation, GCC: Graph Contrastive Clustering, NCD: New Class Detector.

## H. Ablation Study

To evaluate the contribution of each core component in the framework, we conduct a systematic ablation study on the APPLICATIONS 21 dataset, removing the following modules individually or jointly:

Graph Augmentation (GA): Generates networkcharacteristic-aligned samples to address data scarcity, class imbalance, and robustness issues in complex networks;

Graph Contrastive Clustering (GCC): Learns classdiscriminative embeddings via supervised contrastive and center-aware losses;

New Class Detector (NCD): Enables new class detection and clustering based on Mahalanobis distance to support openworld recognition.

Based on the results in Table VI, the conclusions are as follows:

GA: Removing it reduces accuracy from 95.02% to 92.61% and F1-score from 95.57% to 91.44%, verifying its role in enhancing robustness and reducing overfitting (especially in class-imbalanced scenarios);

GCC: Excluding it leads to a significant performance degradation (F1-score drops to 66.63%), confirming its core position in learning discriminative embeddings and maintaining interclass separability;

NCD: Disabling it severely impairs the model’s ability to handle open-world data (F1-score drops to 84.59%), highlighting its necessity in scenarios with frequent unknown classes.

Complementarity of Components: Removing multiple components significantly degrades performance. Removing GA and NCD together drops the F1-score to 78.06%. Furthermore, removing combinations involving GCC (e.g., GA + GCC, GCC + NCD) results in F1-scores below 50%, reflecting strong synergy. Notably, the simultaneous absence of GCC and NCD causes a near-collapse of classification performance (dropping to an F1-score of 41.15%), making both components foundational to the framework’s success.

The ablation study demonstrates that each module significantly improves GCLC’s performance. The integrated framework excels in accuracy, robustness, and open-world adaptability, validating the value of combining representation learning, data augmentation, and new class detection.

## VI. CONCLUSION

In this paper, we propose a unified graph-based contrastive clustering framework for encrypted trafic classification in open-world environments. By modeling encrypted trafic as interaction graphs, our method enables Graph Neural Networks (GNNs) to capture the macroscopic structural and relational characteristics of network trafic. To tackle data insuficiency and class imbalance, we introduce a domainspecific graph augmentation strategy that improves data diversity and model robustness. Coupled with a supervised contrastive learning module and a center-aware loss, our framework significantly enhances feature discriminability. Furthermore, by integrating a Mahalanobis distance-based detector with an adaptive update mechanism, the framework efectively identifies both known and unseen trafic categories. Extensive evaluations on three public datasets and one selfcollected dataset demonstrate that our approach outperforms state-of-the-art baselines across standard metrics, excelling particularly in clustering quality and new class discovery.

While this work provides a practical solution for dynamic and security-critical environments, we explicitly acknowledge certain theoretical boundaries in our current design. Fundamentally, lightweight packet-level features are inherently weakly discriminative in isolation; the discriminative power of our framework stems entirely from the topological representation, where the GNN aggregates local attributes into structural paradigms. Although our graph augmentation implicitly simulates and defends against real-world partial obfuscation and network jitter, it faces three specific limitations. First, absolute Constant-Bit-Rate (CBR) padding would degrade the graph into a featureless chain, neutralizing our structural approach. Second, our simplistic random node addition strategy fails to capture the intricate topological variations caused by real-world TCP fragmentation, as accurately modeling such behaviors requires stateful parameters (e.g., sequence numbers) that contradict our lightweight premise. Third, while our binary temporal discretization efectively mitigates network jitter, it inevitably sacrifices fine-grained temporal dynamics.

Nevertheless, these limitations highlight clear pathways for future open-world network intelligence research. Future eforts will address these boundaries by exploring learnable, timeaware attention mechanisms and more sophisticated, protocolaware graph augmentation strategies, ultimately enhancing model robustness in highly fragmented and ultra-obfuscated environments.

## REFERENCES

[1] R. Xie et al., “ModelFreeUP: Attacking sparse network monitoring via model-free universal adversarial perturbation,” IEEE Trans. Netw., no. 99, Jan. 2026.

[2] J. Tian et al., “Matrix reshaping for reduced sensing cost and improved data inference in sparse mobile sensing environments,” IEEE Trans. Mobile Comput., vol. 25, no. 4, pp. 5253–5266, Apr. 2026.

[3] Internet Assigned Numbers Authority (IANA). Service Name and Transport Protocol Port Number Registry. Accessed: Jul. 1, 2020. [Online]. Available: https://www.iana.org/assignments/service-namesport-numbers/service-names-port-numbers.xhtml

[4] A. Azab, M. Khasawneh, S. Alrabaee, K.-K.-R. Choo, and M. Sarsour, “Network trafic classification: Techniques, datasets, and challenges,” Digit. Commun. Netw., vol. 10, no. 3, pp. 676–692, Jun. 2024.

[5] J. Zhang, F. Li, F. Ye, and H. Wu, “Autonomous unknownapplication filtering and labeling for DL-based trafic classifier update,” in Proc. IEEE Conf. Comput. Commun. (INFOCOM), Jul. 2020, pp. 397–405.

[6] N. Williams, S. Zander, and G. Armitage, “Evaluating machine learning algorithms for automated network application identification,” Centre Adv. Internet Archit. (CAIA), Swinburne Univ. Technol., Melbourne, VIC, Australia, Tech. Rep. 060410B, Mar. 2006.

[7] A. Este, F. Gringoli, and L. Salgarelli, “Support vector machines for TCP trafic classification,” Comput. Netw., vol. 53, no. 14, pp. 2476–2490, Sep. 2009.

[8] R. Alshammari and A. N. Zincir-Heywood, “An investigation on the identification of VoIP trafic: Case study on gtalk and skype,” in Proc. Int. Conf. Netw. Service Manage., Oct. 2010, pp. 310–313.

[9] Y. Lecun, L. Bottou, Y. Bengio, and P. Hafner, “Gradient-based learning applied to document recognition,” Proc. IEEE, vol. 86, no. 11, pp. 2278–2324, 1998.

[10] R. Zhao et al., “Yet another trafic classifier: A masked autoencoder based trafic transformer with multi-level flow representation,” in Proc. AAAI Conf. Artif. Intell., 2023, vol. 37, no. 4, pp. 5420–5427.

[11] S. Le, Y. Lai, Y. Wang, and H. He, “An adaptive classification and updating method for unknown network trafic in open environments,” Comput. Netw., vol. 238, Jan. 2024, Art. no. 110114.

[12] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “AppScanner: Automatic fingerprinting of smartphone apps from encrypted network trafic,” in Proc. IEEE Eur. Symp. Secur. Privacy (EuroSP), Mar. 2016, pp. 439–454.

[13] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “FS-net: A flow sequence network for encrypted trafic classification,” in Proc. IEEE Conf. Comput. Commun., Apr. 2019, pp. 1171–1179.

[14] M. Shen, J. Zhang, L. Zhu, K. Xu, and X. Du, “Accurate decentralized application identification via encrypted trafic analysis using graph neural networks,” IEEE Trans. Inf. Forensics Security, vol. 16, pp. 2367–2380, 2021.

[15] M. Jiang et al., “Accurate mobile-app fingerprinting using flow-level relationship with graph neural networks,” Comput. Netw., vol. 217, Nov. 2022, Art. no. 109309.

[16] J. Yang, X. Jiang, Y. Lei, W. Liang, Z. Ma, and S. Li, “MTSecurity: Privacy-preserving malicious trafic classification using graph neural network and transformer,” IEEE Trans. Netw. Service Manage., vol. 21, no. 3, pp. 3583–3597, Jun. 2024.

[17] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” Neural Comput., vol. 9, no. 8, pp. 1735–1780, Nov. 1997.

[18] P. Vincent, H. Larochelle, I. Lajoie, Y. Bengio, and P.-A. Manzagol, “Stacked denoising autoencoders: Learning useful representations in a deep network with a local denoising criterion,” J. Mach. Learn. Res., vol. 11, no. 110, pp. 3371–3408, 2010.

[19] F. Rosenblatt, “The perceptron: A probabilistic model for information storage and organization in the brain,” Psychol. Rev., vol. 65, no. 6, pp. 386–408, 1958.

[20] J. Zhou, W. Fu, W. Hu, Z. Sun, T. He, and Z. Zhang, “Challenges and advances in analyzing TLS 1.3-encrypted trafic: A comprehensive survey,” Electronics, vol. 13, no. 20, p. 4000, Oct. 2024.

[21] J.-P. Smith, L. Dolfi, P. Mittal, and A. Perrig, “QCSD: A QUICclientsidewebsite-fingerprinting defence framework,” in Proc. 31st USENIX Secur. Symp. (USENIX Security), 2022, pp. 771–789.

[22] Z. Zhao, Y. Guo, J. H. Wang, H. Wang, C. Zhang, and C. An, “CL-ETC: A contrastive learning method for encrypted trafic classification,” in Proc. IFIP Netw. Conf. (IFIP Networking), Jun. 2022, pp. 1–9.

[23] H. Zhang, X. Xiao, L. Yu, Q. Li, Z. Ling, and Y. Zhang, “One train for two tasks: An encrypted trafic classification framework using supervised contrastive learning,” 2024, arXiv:2402.07501.

[24] S. Huang, K. Chen, C. Liu, A. Liang, and H. Guan, “A statistical-featurebased approach to internet trafic classification using machine learning,” in Proc. Int. Conf. Ultra Modern Telecommun. Workshops, Oct. 2009, pp. 1–6.

[25] C. Cortes and V. Vapnik, “Support-vector networks,” Mach. Learn., vol. 20, no. 3, pp. 273–297, 1995.

[26] D. D. Lewis, “Naive (Bayes) at forty: The independence assumption in information retrieval,” in Proc. Eur. Conf. Mach. Learn. Berlin, Germany: Springer, 1998, pp. 4–15.

[27] L. Breiman, “Random forests,” Mach. Learn., vol. 45, no. 1, pp. 5–32, 2001.

[28] S. L. Salzberg and J. R. Quinlan, C4. 5: Programsfor Machine Learning. San Mateo, CA, USA: Morgan Kaufmann, 1994.

[29] A. Likas, N. Vlassis, and J. J. Verbeek, “The global k-means clustering algorithm,” Pattern Recognit., vol. 36, no. 2, pp. 451–461, Feb. 2003.

[30] T. van Ede et al., “FlowPrint: Semi-supervised mobile-app fingerprinting on encrypted network trafic,” in Proc. Netw. Distrib. Syst. Secur. Symp. (NDSS), 2020, pp. 1–18.

[31] P. C. Mahalanobis, “On the generalised distance in statistics,” Proc. Nat. Inst. Sci. India, vol. 2, no. 1, pp. 49–55, 1936.

[32] Y. Yin et al., “GraphIoT: Lightweight IoT device detection based on graph classifiers and incremental learning,” IEEE Trans. Services Comput., vol. 17, no. 6, pp. 3758–3772, Nov. 2024.

[33] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of encrypted and VPN trafic using time-related features,” in Proc. 2nd Int. Conf. Inf. Syst. Secur. Privacy, Portugal, 2016, pp. 407–414.

[34] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware trafic classification using convolutional neural network for representation learning,” in Proc. Int. Conf. Inf. Netw. (ICOIN), Da Nang, Vietnam, Jan. 2017, pp. 712–717.

[35] S. Jorgensen et al., “Extensible machine learning for encrypted network trafic application labeling via uncertainty quantification,” IEEE Trans. Artif. Intell., vol. 5, no. 1, pp. 420–433, Jan. 2024.

[36] J. Shi and J. Malik, “Normalized cuts and image segmentation,” Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), vol. 22, no. 8, pp. 888–905, 2000.

[37] K. Chidananda Gowda and G. Krishna, “Agglomerative clustering using the concept of mutual nearest neighbourhood,” Pattern Recognit., vol. 10, no. 2, pp. 105–112, Jan. 1978.

![](images/d5be6fe5ba1d14bc8e5b30ec066d80413c9acf8b23682b4ebedab5956e245a47.jpg)  
Jigang Wen received the Ph.D. degree in computer application from Hunan University, Changsha, China, in 2011. He was a Research Assistant with the Department of Computing, The Hong Kong Polytechnic University, Hong Kong, from 2008 to 2010. He is currently with the School of Computer Science and Engineering, Hunan University of Science and Technology, Xiangtan, China. His research interests include wireless network and mobile computing and high-speed network measurement and management.

![](images/1e6ef7b7762fbe58862d8cbd0e7bedf704b3b9192e7c20aaa1a090dc5b3e937e.jpg)

Xiyu Zhang received the B.E. degree from Shaoguan University in 2023. She is currently pursuing the M.S. degree with the School of Computer Science and Engineering, Hunan University of Science and Technology. Her research interests include trafic identification, contrastive learning, network security, and graph neural networks.

![](images/2ef2081c43778bbc2113eec8ae83e311023c3b4a8a171c9e0c90118e3f6d08d7.jpg)

Kun Xie (Member, IEEE) received the Ph.D. degree in computer applications from Hunan University in 2007 and subsequently conducted Post-Doctoral Research with The Hong Kong Polytechnic University. She is currently a second-level Professor and a Doctoral Supervisor with Hunan University, a Director of the Key Laboratory of Supercomputing and Artificial Intelligence Converged Computing, Ministry of Education, and a Chair of both the Academic Committee and the Degree Committee of the College of Computer Science and Electronic

![](images/29cec66a181abc0bb19b8a713e7cadac6ef79105d1cee52e89b16fdf95452503.jpg)

Kun Huang received the B.E., M.E., and Ph.D. degrees in computer science and technology from Hunan University, in 2001, 2004, and 2009, respectively. He is currently an Associate Professor with Peng Cheng Laboratory, China. His research interests include programmable networks, datacenter networks, and emerging networks.

Engineering with Hunan University. She has published more than 170 papers in top-tier conferences and journals, including SIGMOD, CCS, INFOCOM, ICDE, SIGMETRICS, IEEE/ACM TRANSACTIONS ON NETWORKING, IEEE TRANSACTIONS ON MOBILE COMPUTING, IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY, IEEE TRANSACTIONS ON PARALLEL AND DISTRIBUTED SYSTEMS, IEEE TRANSACTIONS ON SER-VICES COMPUTING, IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING, and IEEE TRANSACTIONS ON DEPENDABLE AND SECURE COMPUTING. Her long-standing research interests include matrix/tensor completion, computer networks, network security, and artificial intelligence.

![](images/6e5b8d3c24e26ce7d0e6897cbb7b35296ad5b1cb0036485ac153fb51ad2a8612.jpg)

Yudian Ouyang received the Ph.D. degree in computer science and technology from Hunan University, Changsha, China, in 2024. She is currently a Lecturer with Hunan Normal University. Her research interests include network measurement and analysis, tensor completion, and deep learning.

![](images/878831944dfeba6bc43286d9ab90deaeb458df72765cebddeeb1daeaf8638004.jpg)

Yuxiang Zeng received the bachelor’s degree from Shantou University in 2024. He is currently pursuing the master’s degree with Hunan University, China, under the supervision of Prof. Kun Xie. During his undergraduate studies, he has published five papers, including those in CCF C-ranked conferences, such as IEEE SCC/SSE and IEEE ICPADS. His research interests include deep learning, data mining, and web services.

![](images/9541685782d3579a3a9ebe0445607f81a06f41e295381fdb7dd910f92c265957.jpg)

Wei Liang received the Ph.D. degree in computer science and technology from Hunan University, Changsha, China, in 2013. He was a Post-Doctoral Scholar with Lehigh University, Bethlehem, PA, USA, from 2014 to 2016. He is currently a Professor and the Dean of the School of Computer Science and Engineering, Hunan University of Science and Technology, Xiangtan, China. His research interests include blockchain security technology, network security protection, embedded systems, and hardware IP protection.
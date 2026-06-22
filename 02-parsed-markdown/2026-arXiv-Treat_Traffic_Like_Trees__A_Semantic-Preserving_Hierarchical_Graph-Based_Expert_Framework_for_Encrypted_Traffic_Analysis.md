# Treat Traffic Like Trees: A Semantic-Preserving Hierarchical Graph-Based Expert Framework for Encrypted Traffic Analysis

Yuantu Luo, Jun Tao†, Linxiao Yu, Guang Cheng, Member, IEEE

Abstract—Graph-based deep learning methods have been widely employed in encrypted traffic analysis to exploit latent correlations across different granularities. However, while complex preprocessing pipelines and sophisticated model structures often achieve strong performance, they may obscure inherent protocol semantics during representation learning. Moreover, the hierarchical structure of protocol layers and their corresponding fields, defined by protocol specifications and routinely utilized in manual traffic analysis, remains underexplored in existing learning frameworks. In this paper, we propose Protocol Tree Graph Attention with Mixture of Experts (PTGAMoE), a semantic-preserving hierarchical graph-based expert framework for encrypted traffic analysis. The field-based graph construction and expert committee design enable PTGAMoE to quantify the model’s preferences for specific fields and protocols. Extensive experimental results on representative benchmark datasets under strict no-data-leakage settings demonstrate that PTGAMoE significantly outperforms state-of-the-art (SOTA) models. Furthermore, the semantic-preserving design provides interpretable insights into protocol-level feature importance and expert-level contributions, reflecting the model’s decision-making logic in encrypted traffic classification tasks.

Index Terms—Encrypted traffic classification, Encrypted traffic semantics, Graph Attention Networks, Mixture of Experts

# I. INTRODUCTION

E NCRYPTED traffic has become ubiquitous across vari-ous Internet communication scenarios. Protocols such as TLS, DTLS, and QUIC are commonly used to encapsulate data payloads in applications ranging from web browsing and media streaming to real-time interactions [1]. Furthermore, the widespread deployment of the TLS 1.3 specification has significantly enhanced data privacy, as its advanced cipher suites and secure encapsulation mechanisms mitigate information leakage risks [2] [3]. However, the increasing prevalence of encryption poses significant challenges for network management, as payload-obfuscated packets are inherently difficult to identify and classify.

Machine Learning (ML) and Deep Learning (DL) have demonstrated remarkable success in domains such as Natural Language Processing (NLP) and Computer Vision (CV), prompting significant interest in their application to encrypted

The authors are with the School of Cyber Science and Engineering, Southeast University, Nanjing 211189, China, also with Purple Mountain Laboratories, Nanjing 210096, China, also with Engineering Research Center of Blockchain Application, Supervision and Management (Southeast University), MoE, Nanjing 211189, Jiangsu, China, and also with the Jiangsu Province Engineering Research Center of Security for Ubiquitous Network, Nanjing 211806, China (e-mail: {ytluo, juntao, yulinxiaoybbb, chengguang}@seu.edu.cn).

†Corresponding author.

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible.

traffic analysis. Nevertheless, most supervised learning frameworks require input data to be structured as an N × D dataset S, where N represents the number of entries and D denotes a fixed dimension for each entry. This rigid constraint often leads to a fundamental semantic mismatch and introduces significant noise into the representation learning process.

As illustrated in Fig. 1, TCP-based encrypted packets are constructed according to a layered protocol stack governed by rigorous standards and RFC specifications. While a complete stack typically comprises Ethernet (ETH), Internet Protocol (IP), Transport Control Protocol (TCP), and Transport Layer Security (TLS) layers, not all packets within a flow possess a uniform structure [4]. Depending on their specific function, the composition of layers and fields varies significantly. For instance, session maintenance packets (e.g., keep-alives) may only reach the TCP layer, congestion control mechanisms often introduce variable TCP options, and TLS packets exhibit distinct headers depending on whether they are performing a handshake or transmitting application data. Consequently, traditional preprocessing techniques that rely on padding or truncation to force these heterogeneous packets into fixedshape tensors inevitably disrupt inherent protocol semantics and introduce artificial artifacts.

![](images/6fd0a1f20a5cee33fc23155e324c614c184638c44b5091803e4da201c750662b.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph ETH_Layer
        A["Common Fields"] --> B["Common Fields"]
        C["Options"] --> D["Common Fields"]
        E["e.g., VLAN"] --> F["TLS"]
    end

    subgraph TCP_Layer
        G["Common Fields"] --> H["Common Fields"]
        I["Options"] --> J["Common Fields"]
        K["e.g., MSS, window scale"] --> L["TLS"]
    end

    subgraph IP_Layer
        M["Common Fields"] --> N["Common Fields"]
        O["Options"] --> P["Common Fields"]
        Q["e.g., route, timestamp"] --> R["TLS"]
    end

    subgraph TLS_Layer
        S["Record Header"] --> T["Record Payload"]
        U["Handshake"] --> V["Header"] --> W["Message Data"]
        X["Alert"] --> Y["2 bytes"] --> Z["ChangeCipherSpec"]
        AA["Application Data"] --> AB["1 byte"] --> AC["Encrypted Application Data"]
    end
```
</details>

Fig. 1: Hierarchical field structure of a typical TCP-based encrypted packet conversation.

To address these issues, researchers have explored various techniques, ranging from statistical feature engineering to sophisticated DL model architectures. Statistical attributes, such as flow duration, protocol distributions, and temporal metrics, are extracted to comprehensively capture correlations between traffic flows. Beyond these, graph-based representation learning, particularly Graph Neural Networks (GNNs), has been introduced to exploit latent dependencies within traffic data [5] [6]. Due to the inherent correlation between nodes and edges, GNNs are widely employed to model interactions in packets and flows [7] [8] [9].

However, viewing traffic solely through these feature sets often overlooks the structural nature of layered packets. In practice, traffic analyzers like Wireshark employ dissectors to systematically parse raw data into a hierarchical, tree-like representation termed a Dissection Tree (DT) [10]. Starting from the outermost frame, dissectors recursively expand each encapsulated protocol into its constituent fields. Furthermore, individual fields are often broken down into meaningful subfields, such as specific flags or status codes, revealing multiple layers of semantic detail. Therefore, the resulting structure is an explicit manifestation of a protocol’s syntax and logic, capturing the precise, context-dependent meaning of every byte. Crucially, this tree-like representation is a graph by definition, making it naturally suited for analysis with GNNs.

Additionally, the Mixture of Experts (MoE) architecture has demonstrated significant success within Large Language Models (LLMs) [11]. Beyond its training and inference efficiency, MoE is particularly adept at handling disparate data distributions and multi-modal inputs. A gating network dynamically routes inputs to the most relevant experts, intelligently synthesizing their outputs to produce a final, weighted decision. These two core characteristics, i.e., data specialization and adaptive aggregation, make MoE a highly promising approach for tackling the heterogeneous data structures found in encrypted traffic.

In this paper, we propose Protocol Tree Graph Attention with Mixture of Experts (PTGAMoE). Instead of modeling traffic flows as flat byte sequences or fixed-length feature vectors, PTGAMoE explicitly exploits the protocol parsing structure by representing packet fields as protocol tree graphs that mirror real-world encapsulation semantics. Layer-specific graph attention experts are employed to capture heterogeneous protocol characteristics, and a MoE fusion module adaptively fuses multi-layer representations with optional flowlevel statistics. Finally, a permutation-invariant aggregation mechanism is employed to distill packet-level representations into unified flow descriptors, facilitating robust classification in strict, flow-isolated scenarios. Furthermore, type-aware field embedding and hierarchical gating mechanisms are incorporated to enhance semantic fidelity and interpretability.

Our main contributions can be summarized as follows:

• Protocol Tree Graph Attention (PTGA): We propose a semantic-preserving graph module that explicitly models hierarchical dependencies between protocol fields, ensuring structural integrity without disruptive padding or truncation.   
• Protocol-Aware MoE Architecture: We design a layerwise Mixture of Experts framework that aligns specialized experts with distinct protocol layers, enabling adaptive semantic fusion across heterogeneous and encapsulated protocol structures.   
• Permutation-Invariant Flow Aggregation: We introduce a robust aggregation mechanism to distill packetlevel representations into unified flow descriptors, facilitating accurate classification under strict flow-isolated deployment scenarios.

• Strict No-Leakage Evaluation: We validate our framework on modern TLS1.3 datasets under rigorous no-dataleakage settings. Results show that PTGAMoE significantly outperforms SOTA models (e.g., ET-BERT, YaTC, RBLJAN) while offering quantifiable interpretability via proposed NGI and GCR metrics.

# II. RELATED WORKS

# A. Representation Learning for Encrypted Traffic

Encrypted traffic analysis has evolved from manual feature engineering to deep representation learning. Early works like Kitsune [12] and FS-Net [13] utilized ensembles of autoencoders and recurrent networks to capture flow-level statistics and sequential patterns. With the success of pretraining paradigms, models such as ET-BERT [14], YaTC [15], and the recent TrafficFormer [16] have leveraged Transformers and Masked Autoencoders to learn contextualized datagram representations from large-scale unlabeled data. To improve robustness, data augmentation [17] and semantic analysis of packet patterns [18] have also been explored. Furthermore, context learning has been applied to detect sophisticated DPI evasion [19], while adversarial studies like TANTRA [20] highlight the vulnerability of timing-based features. RBL-JAN [21] comprises a classifier and an adversarial traffic generator at both packet-level and flow-level to capture implicit correlations between bytes and labels, enabling the construction of powerful packet representations. Despite these advances, existing methods predominantly treat traffic as flat byte sequences or statistical vectors, which overlooks the intrinsic inter-relationships between protocol fields, leading to a loss of protocol semantics and limited interpretability.

# B. Graph-Based Modeling in Network Traffic Analysis

To capture structural dependencies, researchers have increasingly adopted Graph Neural Networks (GNNs). For instance, DGNN [22] constructs interaction graphs to identify darknet applications, while FlowGNN [23] models encrypted traffic by exploiting relationships between packets within a flow. Furthermore, DigTraffic [24] further introduces heterogeneous edge designs and graph transformers to represent flow-level message interactions. While these graph-based approaches provide a more flexible relational inductive bias than sequential models, they predominantly focus on interpacket or inter-flow relationships. The internal hierarchical parsing structure of individual packets, as revealed by protocol dissectors, is rarely used as the primary modeling target. In other words, while graphs are employed to model traffic entities, the protocol-level tree structure that governs field dependencies and encapsulation semantics is not explicitly encoded. This leaves a gap between graph-based learning and the intrinsic hierarchical organization of network protocols.

# C. Mixture of Experts for Heterogeneous Traffic Semantics

The Mixture of Experts (MoE) architecture has become a cornerstone of contemporary Large Language Models (LLMs) [25]–[28], demonstrating an exceptional capacity to process heterogeneous data by selectively activating specialized sub-networks [29]. This paradigm has recently extended to time-series foundation models [30] [31] and emerging network traffic foundation models. Within the encrypted traffic classification domain, MoE has shown significant promise. For instance, CL-ViME [32] integrates MoE with contrastive learning to facilitate dual-view feature extraction. However, existing traffic-oriented MoE frameworks typically perform expert routing over flattened sequences or vision-mapped representations, rather than aligning experts with functional protocol layers. Given that network traffic is inherently structured into hierarchical layers with heterogeneous specifications, the protocol stack provides a natural substrate for layer-wise expert specialization. This observation motivates our PTGAMoE framework, which utilizes a dedicated expert committee to model the natural hierarchy of network protocols while preserving structural integrity.

# D. Strict Scenarios in Traffic Classification Tasks

Recently, the research community has voiced significant concerns regarding a credibility crisis in encrypted network traffic classification. Studies indicate that the astonishing performance reported in much of the literature, often exceeding 98% accuracy, is frequently inflated by methodological pitfalls. Specifically, models often become shortcut learners by exploiting Strong Identification Information (SII), such as IP/MAC addresses and port numbers, which act as uninformative artifacts that prevent genuine generalization to real-world scenarios [33]. Furthermore, traditional per-packet dataset splitting introduces severe data leakage, as session-specific implicit identifiers allow models to link test packets to training labels [34]. To address these flaws, researchers advocate for the adoption of Strict Scenarios, which necessitate flow-isolated splitting and the exclusion of SII to rigorously evaluate a model’s ability to learn behavior-driven protocol semantics rather than superficial shortcuts.

# III. OVERVIEW

![](images/c19b7236b3a1fea031a939bad1523447e9fd2dae17bbb36f604bc52e90cd7593.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Field-Level Preprocessing"] --> B["Raw PCAP"]
    B --> C["Heterogeneous Embedding"]
    C --> D["Embedded Tensor"]
    D --> E["Physical Node"]
    D --> F["Abstract Node"]
    E --> G["Protocol Tree Graph Construction"]
    F --> G
    G --> H["Optional Flow Expert"]
    H --> I["Attention-Based Layer Expert"]
    I --> J["Layer Expert Committee"]
    J --> K["Mixture-of-Experts Fusion"]
    K --> L["Flow-Level Aggregation & Prediction"]
    L --> M["Google, Twitter, Facebook, YouTube, Reddit"]
```
</details>

Fig. 2: Overview of the PTGAMoE workflow.

We propose Protocol Tree Graph Attention with Mixture of Experts (PTGAMoE), a structure-aware learning framework designed to preserve the semantic organization of network traffic and enhance the interpretability of protocol-level feature contributions. As illustrated in Fig. 2, the PTGAMoE workflow consists of three main stages: Field-Level Preprocessing, Protocol Tree Graph Construction, and Protocol Tree Graph Attention with Mixture of Experts architecture.

Field-Level Preprocessing. The workflow begins with fieldlevel preprocessing, which transforms raw PCAP files into numerical tensors suitable for representation learning. Instead of treating traffic data as flat byte sequences or fixed-length vectors, PTGAMoE performs semantics-aware field embedding, where each traffic field is embedded according to its inherent type and protocol meaning. Specifically, address fields, numerical fields, and categorical fields are processed via dedicated embedding strategies, yielding a unified tensor that maintains protocol-level semantics while ensuring compatibility with downstream graph modeling.

Protocol Tree Graph Construction. Based on the embedded field representations, PTGAMoE constructs a Protocol Tree Graph (PTG) that explicitly models the hierarchical structure of protocol formats. In the PTG, traffic fields are mapped to graph nodes, and edges are defined according to the parent–child relationships inherent in protocol specifications. Beyond these hierarchical dependencies, we introduce original structural components, including a set of abstract nodes and a global summarizer, to explicitly encode structural protocol identities and facilitate layer-wide semantic exchange. This graph abstraction enables PTGAMoE to represent traffic packets as structured objects rather than flat feature collections, forming the structural foundation for subsequent graph-based learning.

Protocol Tree Graph Attention with Mixture of Experts. Given the constructed PTGs, PTGAMoE employs a layer-wise mixture-of-experts architecture to perform structure-aware representation learning. Each protocol layer is associated with an attention-based graph expert that operates on its corresponding protocol tree graph, enabling the model to capture layer-specific semantics while mitigating noise introduced by heterogeneous packet structures. An optional flow-level expert can be incorporated to leverage aggregated flow statistics when available. The outputs of all experts are adaptively fused through learnable gating mechanisms to generate robust packet-level representations. Furthermore, a permutationinvariant aggregation mechanism is utilized to distill these packet-level signals into a unified flow descriptor, facilitating accurate classification in strict, flow-isolated scenarios. Finally, the resulting flow representation is passed to a prediction head for final classification.

# IV. FIELD-LEVEL PREPROCESSING

This section illustrates the whole procedure of field-level preprocessing, including streaming field extraction and heterogeneous field embedding. These two steps convert raw traffic data into tensors, which can be the standard input in the following models.

The preprocessing stage transforms raw PCAP files into numerical tensors suitable for graph representation learning.

First, raw traffic is parsed into structured field-level attributes using a streaming PCAP-to-CSV converter. To ensure scalability and bounded memory consumption in high-concurrency scenarios, this converter utilizes a chunk-wise parsing strategy (see Appendix A-A).

![](images/fd8eef50115f9c42dd070b47ea360c250093e714ffd06aeddbe2af2461635786.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input x_a^(R)"] --> B["Address Fields"]
    B --> C["Embed CNN GAP"]
    C --> D["Output x_a^(E)"]
    
    E["Input x_n^(R)"] --> F["Numerical Fields"]
    F --> G["Batch Norm Linear"]
    G --> H["Output x_n^(E)"]
    
    I["Input x_c^(R)"] --> J["Categorical Fields"]
    J --> K["Ports Bins Embed"]
    K --> L["Output x_c^(E)"]
    
    M["Input x_a^(E), x_n^(E), x_c^(E)"] --> N["Concat"]
    N --> O["X^(E)"]
    
    style A fill:#f9f,stroke:#333
    style E fill:#f9f,stroke:#333
    style I fill:#f9f,stroke:#333
```
</details>

Fig. 3: The field-level embedding procedure.

Following field extraction from raw PCAPs, the subsequent step is field embedding, which transforms discrete hexadecimal or decimal values into dense vector representations suitable for deep learning models. To address the multi-modal nature of network traffic, including comprising addresses, continuous values and discrete codes, we design a unified embedding module that projects these disparate field types into a shared high-dimensional latent space.

As illustrated in Fig.3, let $X ^ { ( R ) }$ denote an raw CSV input packet, which is decomposed into three subsets, comprising address fields $x _ { a } ^ { ( R ) }$ , numerical fields $x _ { n } ^ { ( R ) }$ and categorical fields $x _ { c } ^ { ( R ) }$ . Consequently, the embedding module includes three specialized sub-components tailored to these distinct data types. The final output is an embedded tensor X(E), $X ^ { ( E ) }$ containing the vector representations $\mathbf { x } _ { a } ^ { ( E ) } , \ \mathbf { x } _ { n } ^ { ( E ) }$ (E )a , x(E )n , and x(E )c $x _ { c } ^ { ( { E } ) }$ corresponding to their respective inputs. Formally, each traffic field is mapped to a fixed-dimensional vector through a typespecific embedding function

$$
\mathbf {x} _ {t} ^ {(E)} = f _ {t} \left(x _ {t} ^ {(R)}\right), \quad t \in \{a, n, c \}, \tag {1}
$$

where $f _ { t } ( \cdot )$ denotes the embedding function for address, numerical, or categorical fields, respectively.

a) Hierarchical Address Embedding (HAE): The HAE module is specifically constructed for IP and MAC addresses. These fields possess a unique hierarchical structure where semantics are encoded in byte-level segments (e.g., subnet masks in IPv4, Organizationally Unique Identifiers in MAC). Treating them as monolithic categorical strings would ignore this intrinsic structure and result in an intractable vocabulary size. To capture this structure, we split an address field $x _ { a } ^ { ( \tilde { R ) } }$ into a sequence of octets $\left( o _ { 1 } , o _ { 2 } , \ldots , o _ { K } \right)$ , where $K \ = \ 4$ for IPv4 and $K = 6$ for MAC. Each octet is independently embedded, and the resulting sequence is aggregated using a 1D Convolutional Neural Network (CNN). This design allows the model to learn local dependencies between adjacent bytes (e.g., network prefixes). Finally, Global Average Pooling (GAP) is applied to obtain a fixed-length representation. The procedure is formalized as

$$
\mathbf {s} _ {a} = \phi_ {\mathrm{oct}} (x _ {a} ^ {(R)}) = (o _ {1}, o _ {2}, \dots , o _ {K}), \tag {2}
$$

$$
\mathbf {x} _ {a} ^ {(E)} = f _ {a} (\mathbf {s} _ {a}) = \operatorname{GAP} \left(\operatorname{CNN} _ {1 \mathrm{D}} \left(\operatorname{Embed} \left(\mathbf {s} _ {a}\right)\right)\right), \tag {3}
$$

where $\phi _ { \mathrm { o c t } } ( \cdot )$ denotes a deterministic transformation that decomposes an address into a sequence of byte-level octets according to protocol specifications. Notably, Embed(·) denotes a generic learnable embedding lookup for discrete symbols, whose parameters are jointly optimized during training.

b) Numerical Field Embedding: This module handles continuous numerical fields (e.g., packet length, window size). Unlike categorical features, these values possess ordinal magnitude semantics. To project them into the target dimension d, we employ a linear transformation block. To ensure numerical stability and accelerate model convergence, Batch Normalization (BatchNorm) is applied prior to the projection:

$$
\mathbf {x} _ {n} ^ {(E)} = \text { Linear } \left(\text { BatchNorm } \left(x _ {n} ^ {(R)}\right)\right). \tag {4}
$$

c) Categorical Field Embedding: Categorical field embedding is applied to discrete protocol fields with finite or discretized vocabularies, such as protocol flags and port numbers. For fields with extremely large or sparse vocabularies (e.g., raw port numbers), we first employ a binning strategy that maps raw values to a smaller set of semantically meaningful bins. This step reduces vocabulary size, alleviates sparsity, and improves representation robustness. After discretization, categorical values are mapped to dense vectors through a learnable embedding function:

$$
\mathbf {x} _ {c} ^ {(E)} = \operatorname{Embed} \left(x _ {c} ^ {(R)}\right). \tag {5}
$$

The final embedded representations of all fields are concatenated into a packed tensor

$$
\mathbf {X} ^ {(E)} = \text { CONCAT } \left(\mathbf {x} _ {a} ^ {(E)}, \mathbf {x} _ {n} ^ {(E)}, \mathbf {x} _ {c} ^ {(E)}\right), \tag {6}
$$

in which the index of each field’s embedding is recorded for the subsequent graph node initialization stage.

# V. LAYER-WISE PROTOCOL TREE GRAPH REPRESENTATION

This section presents the construction of the Protocol Tree Graph (PTG), including its graph representation and the principles used to derive nodes and edges from protocol semantics.

Due to the layered structure of TCP/IP protocol stack, a network packet can naturally be analyzed in a hierarchical manner. Formally, for a specific layer k (e.g., the TLS layer), we define the PTG as an undirected graph

$$
\mathcal {G} _ {k} = \left(\mathcal {V} _ {k}, \mathcal {E} _ {k}\right), \tag {7}
$$

where $\nu _ { k }$ represents the set of nodes corresponding to protocol fields and $\mathcal { E } _ { k }$ denotes the set of edges representing structural dependencies induced by protocol formats.

As illustrated in Fig. 4, the node set $\nu _ { k }$ is constructed through layer-level node extraction and parsing of the packet’s

![](images/4aaeab84bdf8f8d9e2b7cbca9160b9a7e4432dae484eccc3ee3aa88d114c4293.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Layer Nodes Extraction"] --> B["Layer"]
    B --> C["Dissector Tree"]
    C --> D["Semantics Abstraction"]
    D --> E["Physical Node"]
    D --> F["Abstract Node"]
    G["root"] --> H["tls"]
    H --> I["Field"]
    I --> J["Subfields"]
    J --> K["Field (pure semantics)"]
    K --> L["Subfields"]
    M["root"] --> N["tls"]
    N --> O["Field"]
    O --> P["Subfield"]
    P --> Q["Aggregation Field"]
    Q --> R["Subfields"]
    S["root"] --> T["tls"]
    T --> U["Handshake"]
    U --> V["TLS"]
    W["v_sink"] --> X["+ layer-wise sink node"]
    X --> Y["Layer-wise Protocol Tree Graph"]
    Z["e.g."] --> AA["root"]
    AA --> AB["tls"]
    AB --> AC["handshake"]
    AC --> AD["tls.handshake.len"]
```
</details>

Fig. 4: Hierarchical representation of the Protocol Tree Graph (PTG) featuring abstract and physical nodes.

Dissection Tree (DT). We categorize nodes into two types according to their semantic roles:

• Physical Nodes $( \mathcal { V } _ { k } ^ { \mathrm { ( p h y ) } } ) { : }$ Physical nodes correspond to value-carrying protocol fields, which typically appear as leaf nodes in the protocol tree (e.g., tls.record.length, tls.handshake.length). These nodes encode the explicit observable information of network traffic.   
• Abstract Nodes $( \mathcal { V } _ { k } ^ { ( \mathrm { a b s } ) } ) !$ : Abstract nodes represent structural protocol components that do not carry explicit field values. They include protocol layer nodes $v _ { k } ^ { \mathrm { ( l a y e r ) } } \ ( \mathrm { e . g . }$ vk , tls), aggregation fields v(ak $v _ { k } ^ { ( \mathrm { a g g r } ) }$ (e.g., tls.handshake, tls.record), a global virtual root node $( v _ { k } ^ { ( \mathrm { r o o t } ) } )$ ) and a layer-wise sink node v(sik $v _ { k } ^ { ( \mathrm { s i n k } ) }$ nk). Depending on their position in a layer-wise PTG, abstract nodes may aggregate information from descendant nodes. Notably, v(sik $v _ { k } ^ { ( \mathrm { s i n k } ) }$ is designed as a global latent summarizer and an attention aggregation node. It facilitates the capture of holistic layer-specific semantics that transcend the local tree hierarchy, mitigating potential information bottlenecks during deep message passing and ensuring each field node remains context-aware of the entire protocol layer’s state.

Thus, the total node set for protocol k is defined as

$$
\mathcal {V} _ {k} = \mathcal {V} _ {k} ^ {\mathrm{(phy)}} \cup \mathcal {V} _ {k} ^ {\mathrm{(abs)}}. \tag {8}
$$

The edge set $\mathcal { E } _ { k }$ is formally defined as the union of hierarchical protocol edges E(hk $\mathcal { E } _ { k } ^ { \mathrm { ( h i e r ) } }$ and global sink edges $\mathcal { E } _ { k } ^ { ( \mathrm { s i n k } ) }$ Ek :

$$
\mathcal {E} _ {k} = \mathcal {E} _ {k} ^ {\mathrm{(hier)}} \cup \mathcal {E} _ {k} ^ {\mathrm{(sink)}}, \tag {9}
$$

where $\mathcal { E } _ { k } ^ { ( \mathrm { h i e r } ) } = \{ ( u _ { k } , v _ { k } ) | u _ { k } \in \mathrm { C h i l d r e n } ( v _ { k } ) \}$ preserves the intrinsic parent-child relationships referring to the DT. To model long-range dependencies and perform global feature integration, we introduc e E (sink)k $\mathcal { E } _ { k } ^ { ( \mathrm { s i n k } ) } ~ = ~ \{ ( v , v _ { k } ^ { ( \mathrm { s i n k } ) } ) ~ | ~ \forall v ~ \in$ = {(v, v(sik nk)) | ∀v ∈ $\mathcal { V } _ { k } \ \backslash \ \{ v _ { k } ^ { \mathrm { ( s i n k ) } } \} \}$ {v(sink)k }}, establishing a direct information shortcut between every node and the layer-wise sink. In practice, each

Algorithm 1: Protocol Tree Graph Construction   
Input: Dissection tree $\mathcal{T} = (\mathcal{N},\mathcal{R})$ ;
Protocol layer set $\mathcal{L}$ Output: Layer-wise Protocol Tree Graphs $\mathcal{G} = \{\mathcal{G}_k \mid k \in \mathcal{L}\}$ 1 foreach $k \in \mathcal{L}$ do
2 $\mathcal{V}_k \leftarrow \emptyset, \mathcal{V}_k^{(\mathrm{abs})} \leftarrow \emptyset, \mathcal{V}_k^{(\mathrm{phy})} \leftarrow \emptyset;$ 3 $\mathcal{E}_k \leftarrow \emptyset, \mathcal{E}_k^{(\mathrm{hier})} \leftarrow \emptyset, \mathcal{E}_k^{(\mathrm{sink})} \leftarrow \emptyset;$ 4 $\mathcal{N}_k \leftarrow \{n \mid n \in \mathcal{N} \cap \pi(n) = k\}$ ;
5 $\mathcal{R}_k \leftarrow \{(n_p, n_c) \mid (n_p, n_c) \in \mathcal{R} \cap n_p, n_c \in \mathcal{N}_k\}$ ;
6 $\mathcal{V}_k^{(\mathrm{abs})} \leftarrow \mathcal{V}_k^{(\mathrm{abs})} \cup \{v_k^{(\mathrm{root})}, v_k^{(\mathrm{layer})}, v_k^{(\mathrm{aggr})}, v_k^{(\mathrm{sink})}\}$ ;
7 $\mathcal{E}_k^{(\mathrm{hier})} \leftarrow$ 8 $\mathcal{E}_k^{(\mathrm{hier})} \cup \{(v_k^{(\mathrm{root})}, v_k^{(\mathrm{layer})}), (v_k^{(\mathrm{layer})}, v_k^{(\mathrm{aggr})})\}$ ;
8    foreach $n \in \mathcal{N}_k$ do
9    if ISPHYSICAL(n) then
10    | $\mathcal{V}_k^{(\mathrm{phy})} \leftarrow \mathcal{V}_k^{(\mathrm{phy})} \cup \{n\}$ ;
11    end
12    end
13 $\mathcal{V}_k \leftarrow \mathcal{V}_k^{(\mathrm{phy})} \cup \mathcal{V}_k^{(\mathrm{abs})}$ ;
14    foreach $(n_p, n_c) \in \mathcal{R}_k$ do
15    if $n_p, n_c \in \mathcal{V}_k$ then
16    | $\mathcal{E}_k^{(\mathrm{hier})} \leftarrow \mathcal{E}_k^{(\mathrm{hier})} \cup \{(n_p, n_c)\}$ ;
17    end
18    end
19 $\mathcal{E}_k^{(\mathrm{sink})} = \{(v, v_k^{(\mathrm{sink})}) \mid \forall v \in \mathcal{V}_k \setminus \{v_k^{(\mathrm{sink})}\}\}$ ;
20 $\mathcal{E}_k = \mathcal{E}_k^{(\mathrm{hier})} \cup \mathcal{E}_k^{(\mathrm{sink})}$ ;
21 $\mathcal{G}_k = (\mathcal{V}_k, \mathcal{E}_k)$ ;
22 end
23 $\mathcal{G} \leftarrow \{\mathcal{G}_k \mid k \in \mathcal{L}\}$ ;
24 return G;

undirected edge is treated as two directed edges, supporting bidirectional propagation for both fine-grained semantic aggregation and global context distribution.

Algorithm 1 summarizes the construction procedure of layer-wise PTGs from a dissection tree. The input dissection tree is denoted as $\boldsymbol { \mathcal { T } } ~ = ~ ( \boldsymbol { \mathcal { N } } , \boldsymbol { \mathcal { R } } )$ . N represents the set of field-level and structural nodes extracted from the dissection tree. R encodes parent-child relationships induced by protocol formats. The mapping function $\pi ( n )$ associates each dissector node $\textit { n } \in \textit { N }$ with its corresponding protocol layer. The final output is a set of layer-wise PTGs ${ \mathcal { G } } ,$ which serves as structured inputs for subsequent representation learning.

To distinguish physical and abstract nodes and to fully exploit their respective semantic roles, we adopt a differential node initialization strategy. Let $\mathbf { h } _ { v } ^ { ( E ) }$ denote the initial representation of node $v .$

• For physical nodes $v ~ \in ~ \mathcal { V } ^ { \mathrm { ( p h y ) } }$ , we initialize features by extracting the corresponding vector from the packed tensor $X ^ { ( E ) }$ defined in equation (6):

$$
\mathbf {h} _ {v} ^ {(E)} = \text { Slice } (X ^ {(E)}, \mathrm{idx} _ {v}), \tag {10}
$$

where $\operatorname { i d } \mathbf { X } _ { v }$ denotes the index mapping derived from the field-level preprocessing stage.

• For abstract nodes $v \in \mathcal { V } ^ { \mathrm { ( a b s ) } }$ , we assign each node an independent learnable semantic token $\mathbf { t } _ { v } \in \mathbb { R } ^ { D }$ :

$$
\mathbf {h} _ {v} ^ {(E)} = \mathbf {t} _ {v}. \tag {11}
$$

These node-specific semantic tokens are jointly optimized during training, enabling the model to encode structural protocol identities prior to message passing while maintaining a consistent embedding dimensionality.

Distinctions Between DT and PTG: Although the PTG construction is inspired by the DT used in tools such as Wireshark, the two structures differ fundamentally in both purpose and representation. The DT is designed as a protocol parsing structure, aiming to exhaustively decode packet bytes into protocol fields for inspection and debugging. As a result, it treats all parsed fields uniformly and does not explicitly distinguish between value-carrying fields and structural protocol components. In contrast, PTG is constructed explicitly for representation learning. It introduces structurally differentiated abstract nodes to capture protocol hierarchy and packet-level structure, while differentiating between fields with concrete values and structural protocol elements. This abstraction enables PTG to preserve protocol semantics and provide a global, model-friendly representation that is suitable for graph-based learning.

# VI. PROTOCOL TREE GRAPH ATTENTION WITH MIXTURE OF EXPERTS

This section presents the detailed architecture of our semantic-preserving model for encrypted traffic analysis, namely Protocol Tree Graph Attention with Mixture of Experts (PTGAMoE). As illustrated in Fig. 5, PTGAMoE consists of four major components: a Layer Expert Committee, an Optional Flow Expert, a Mixture-of-Experts Fusion module, and a Flow-Level Aggregation & Prediction module.

The LEC extracts structure-aware representations from protocol tree graphs, with each expert generating an intermediate semantic embedding. When enabled, the OFE integrates flowlevel statistical features to provide a holistic network view. Subsequently, the MoEF module adaptively synthesizes these expert outputs to produce refined packet-level representations. Finally, a permutation-invariant mechanism aggregates these signals into a unified flow descriptor for the final classification decision.

# A. Layer Expert Committee

For a conversation involving K protocol layers, the LEC utilizes K attention-based experts, each specialized for a specific layer-wise PTG. Each expert performs structure-aware representation learning through a four-stage pipeline: feature alignment, feature gating, message passing, and graph readout.

a) Feature Alignment: To enable joint graph-based processing, a feature alignment mechanism is introduced to project all node features into a unified hidden space. Let $v \in \mathcal { V } _ { k }$ $\mathbf { h } _ { v } ^ { ( E ) } \in \mathbb { R } ^ { d _ { v } }$ a node in the layer PTG of protocol k, andbe its embedded feature vector obtained from the field-level preprocessing stage in Section IV. A linear alignment function is applied to map h(E)v t $\mathbf { h } _ { v } ^ { ( E ) }$ o a shared hidden dimension D:

$$
\mathbf {h} _ {v} ^ {(0)} = \mathbf {W} _ {d _ {v}} \mathbf {h} _ {v} ^ {(E)} + \mathbf {b} _ {d _ {v}}, \tag {12}
$$

where $\mathbf { W } _ { d _ { v } } ~ \in ~ \mathbb { R } ^ { D \times d _ { v } }$ and $\mathbf { b } _ { d _ { v } }$ are learnable parameters associated with the corresponding input dimensionality. This design allows fields with different semantic types to be jointly processed while preserving their original representations.

b) Feature Gating: To suppress protocol noise and enhance interpretability, we employ a node-level gating mechanism. Specifically, for a layer-wise PTG with $| \nu _ { k } |$ nodes, a gate vector $\pmb { \delta \mathrm { \tau } } _ { k } \in \dot { \mathbb { R } } ^ { | \mathcal { V } _ { k } | }$ is introduced. After applying a sigmoid activation, a field-wise gating vector $\begin{array} { r } { \mathbf { \nabla } g _ { k } = \sigma ( \delta _ { k } ) } \end{array}$ is obtained, where each element $g _ { v }$ corresponds to the importance weight of node v. The gated node representation is then computed as

$$
\tilde {\mathbf {h}} _ {v} ^ {(0)} = g _ {v} \cdot \mathbf {h} _ {v} ^ {(0)}. \tag {13}
$$

The sigmoid function constrains the gating weights to the range (0, 1), enabling soft feature selection while maintaining differentiability. This mechanism enables the model to adaptively emphasize semantically informative protocol fields and provides a natural basis for feature-level interpretability.

c) Structure-aware Message Passing: After feature alignment and gating, each layer expert performs structure-aware message passing on the PTG using a two-layer graph attention architecture.

The first graph attention layer is designed to capture diverse latent semantics from protocol fields through multi-head attention. For a target node $v \in \mathcal V _ { k }$ , its representation after the first attention layer is computed by aggregating messages from its neighbors:

$$
\mathbf {h} _ {v} ^ {(1)} = \left\| \sum_ {h = 1} ^ {H} \alpha_ {v u} ^ {(h)} \mathbf {W} ^ {(h)} \tilde {\mathbf {h}} _ {u} ^ {(0)}, \right. \tag {14}
$$

where α(h)vu $\alpha _ { v u } ^ { ( h ) }$ denotes the attention coefficient of the h-th head, $\mathbf { W } ^ { ( h ) }$ is the corresponding linear projection matrix, and ∥ represents feature concatenation across H attention heads. This multi-head mechanism allows the model to attend to protocol semantics from multiple representation subspaces simultaneously.

The second graph attention layer adopts a single-head attention scheme to further integrate the multi-head representations produced by the first layer. This layer focuses on unifying latent semantic information within the expert, yielding a coherent layer-level representation. Formally, the output of the second attention layer is given by

$$
\mathbf {h} _ {v} ^ {(2)} = \sum_ {u \in \mathcal {N} (v)} \alpha_ {v u} \mathbf {W h} _ {u} ^ {(1)}, \tag {15}
$$

where a single attention head is used to aggregate and refine the representations learned from the previous layer.

Through this hierarchical attention-based message passing process, each layer expert effectively captures both local protocol field interactions and global structural semantics encoded in the protocol tree.

![](images/276c6371b6b63f17794a86abb24114899dfd71f12e3ffcd0e591c808ffe957a8.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Embedded Fields Tensor"] --> B["Feature Align"]
    B --> C["Field-Wise Importance Weights"]
    C --> D["Feature Gating"]
    D --> E["Mixture-of-Experts Fusion"]
    E --> F["Input-Conditioned Gating Network"]
    F --> G["Weighted Aggregation"]
    G --> H["packet-level auxiliary prediction"]
    H --> I["Packet Logits"]
    J["Flow Statistics"] --> K["Structure-Aware Message Passing Attention-Based Layer Expert"]
    K --> L["Optional Flow Expert"]
    M["Field-wise Importance Weights"] --> N["GAT Module 1"]
    N --> O["Target Node"]
    O --> P["Message Passing Head h"]
    P --> Q["Head Concatenate"]
    Q --> R["GAT Module 2"]
    R --> S["Single Head"]
    S --> T["Multi-Head"]
    T --> U["Global Pooling Graph Readout"]
    U --> V["Global Pooling Graph Readout"]
    V --> W["Global Pooling Graph Readout"]
    X["Optional Flow Expert"] --> Y["Flow-Level Aggregation & Prediction"]
    Y --> Z["Flow-Level Representation Aggregation"]
    Z --> AA["Max-Pooling"]
    AA --> AB["LayerNorm"]
    AB --> AC["Linear"]
    AC --> AD["Packet Representation Projection"]
    AD --> AE["Flow-Level Prediction"]
    AE --> AF["Flow-Level Aggregation & Prediction"]
    AG["Layer Expert Committee"] --> AH["Feature Align"]
    AH --> AI["Field-Wise Importance Weights"]
    AI --> AJ["Feature Gating"]
    AJ --> AK["Mixture-of-Experts Fusion"]
    AK --> AL["Input-Conditioned Gating Network"]
    AL --> AM["Weighted Aggregation"]
    AM --> AN["packet-level auxiliary prediction"]
    AN --> AO["Packet Logits"]
```
</details>

Fig. 5: The model design of PTGAMoE.

d) Graph Readout: To obtain a fixed-dimensional representation for each protocol layer, a graph-level readout operation is applied after the final message passing layer. Specifically, node representations are aggregated using a global pooling function:

$$
\mathbf {z} _ {k} = \text { GlobalPool } \left(\left\{\mathbf {h} _ {v} ^ {(2)} \mid v \in \mathcal {V} _ {k} \right\}\right), \tag {16}
$$

where $\mathbf { z } _ { k } \in \mathbb { R } ^ { D }$ denotes the semantic embedding of the k-th protocol layer, and GlobalPool(·) represents a global mean operation. The resulting layer-level embedding $\mathbf { z } _ { k }$ serves as the output of the corresponding protocol layer expert and will be further processed by the mixture-of-experts fusion module.

# B. Optional Flow-Level Expert

In addition to protocol-layer experts operating on packetlevel protocol tree graphs, PTGAMoE optionally incorporates a flow-level expert to capture global traffic characteristics that are not explicitly represented at the packet field level. Flowlevel features summarize the holistic behavior of a traffic conversation, such as temporal patterns and statistical distributions, and therefore provide complementary information to protocol tree representations.

Let $\mathbf { x } _ { f } \in \mathbb { R } ^ { F }$ denote the aggregated flow-level feature vector associated with a traffic conversation, where F is the number of extracted flow statistics. The flow-level expert employs a lightweight feed-forward network to project $\mathbf { x } _ { f }$ into the shared latent space:

$$
\mathbf {z} _ {f} = f _ {\text { flow }} (\mathbf {x} _ {f}), \tag {17}
$$

where $\mathbf { z } _ { f } \in \mathbb { R } ^ { D }$ is the resulting flow-level embedding, whose dimensionality is compatible with the fusion stage.

Unlike protocol-layer experts, which perform structureaware message passing on protocol tree graphs, the flowlevel expert operates on pre-aggregated statistics and captures coarse-grained traffic dynamics. When enabled, the flow-level embedding $\mathbf { z } _ { f }$ is treated as an additional expert output and is jointly fused with protocol-layer embeddings in the subsequent mixture-of-experts fusion stage. When flow-level features are unavailable or intentionally excluded, the flow-level expert can be omitted without affecting the overall architecture. The flow features we used are displayed in the APPENDIX A-C section.

# C. Mixture-of-Experts Fusion

PTGAMoE employs a mixture-of-experts fusion mechanism to adaptively integrate heterogeneous semantic information from different protocol layers and the flow-level expert when enabled. This design allows the model to dynamically adjust the contribution of each expert according to the input traffic characteristics.

Let $\left\{ \mathbf { z } _ { 1 } , \mathbf { z } _ { 2 } , \ldots , \mathbf { z } _ { K } \right\}$ denote the output embeddings of the K protocol-layer experts, where $\mathbf { z } _ { k } \in \mathbb { R } ^ { D }$ represents the semantic embedding of the k-th protocol layer. When the optional flow-level expert is enabled, an additional embedding $\mathbf { z } _ { f } \in \mathbb { R } ^ { D }$ is included. In this situation, we denote the complete set of expert embeddings as $\{ \mathbf { z } _ { k } \} _ { k = 1 } ^ { K ^ { \prime } }$ }K′ , where $K ^ { \prime } = K + \mathbb { I } _ { f }$ . If is a indicator function. When the flow expert is enabled, $\mathbb { I } _ { f } = 1$ , otherwise $\mathbb { I } _ { f } = 0$ .

To enable input-conditioned expert selection, PTGAMoE adopts a lightweight gating network that dynamically computes expert importance for each traffic sample. Specifically, all expert embeddings are first concatenated to form a joint representation:

$$
\mathbf {z} _ {\text { concat }} = \left\| _ {k = 1} ^ {K ^ {\prime}} \mathbf {z} _ {k}. \right. \tag {18}
$$

A gating function $g ( \cdot )$ parameterized by a multi-layer perceptron is then applied to produce expert-level gating scores:

$$
\boldsymbol {\gamma} = g \left(\mathbf {z} _ {\text { concat }}\right), \tag {19}
$$

where $\gamma \in \mathbb { R } ^ { K ^ { \prime } }$ depends on the current input sample.

Instead of enforcing competitive normalization, we employ a sigmoid activation to obtain cooperative expert weights:

$$
\boldsymbol {\omega} = \sigma (\boldsymbol {\gamma}), \tag {20}
$$

where each $\omega _ { k } \in ( 0 , 1 )$ represents the input-dependent contribution of the k-th expert. This cooperative formulation allows multiple layer experts to contribute simultaneously, reflecting the complementary nature of hierarchical protocol semantics. Unlike competitive softmax routing, which enforces mutual exclusion among experts, sigmoid-based gating enables flexible multi-expert collaboration without constraining the weights to sum to one.

The final fused representation is computed as a weighted aggregation of expert embeddings:

$$
\mathbf {z} = \sum_ {k = 1} ^ {K ^ {\prime}} \omega_ {k} \cdot \mathbf {z} _ {k}. \tag {21}
$$

The aggregated representation z is fed into a feed-forward prediction head to produce packet-level class logits:

$$
\hat {\mathbf {y}} ^ {(\mathrm{pkt})} = f _ {\text { pred }} ^ {(\mathrm{pkt})} (\mathbf {z}), \tag {22}
$$

where $f _ { \mathrm { p r e d } } ^ { \mathrm { ( p k t ) } } ( \cdot )$ denotes a multi-layer perceptron with learnable parameters for packet-level prediction.

# D. Flow-Level Aggregation & Prediction

Confront with the strict scenario in traffic classification tasks, PTGAMoE introduces a flow-level aggregation mechanism that integrates packet-level representations within the same traffic flow to produce a unified flow representation.

Let a traffic flow $\bar { \mathcal { F } } = \{ p _ { i } \} _ { i = 1 } ^ { N _ { f } }$ , where $N _ { f }$ denotes the number of packets associated with the flow. For each packet $p _ { i }$ , the model produces a fused representation $\mathbf { z } _ { i }$ and corresponding packet-level logits $\hat { \mathbf { y } } _ { i }$ according to equation (21) and (22).

a) Packet Representation Projection: The packet-level representations are projected into a latent space suitable for flow aggregation:

$$
\mathbf {h} _ {i} = f _ {\mathrm{agg}} (\mathbf {z} _ {i}), \tag {23}
$$

where $f _ { \mathrm { a g g } } ( \cdot )$ is implemented as a linear project layer with layer normalization, and $\mathbf { h } _ { i } \in \mathbb { R } ^ { D ^ { \prime } }$ denotes the projected packet embedding.

b) Flow-Level Representation Aggregation: A permutation-invariant aggregation function is applied to obtain a flow-level represetation:

$$
\mathbf {h} ^ {(\mathcal {F})} = \text { MaxPool } \left(\{\mathbf {h} _ {i} \mid p _ {i} \in \mathcal {F} \}\right). \tag {24}
$$

Here MaxPool(·) represents the max-pooling operation, which is used to emphasize the most informative packet-level signals within each flow by taking the maximum element-wise packet representations. In practice, to ensure computational efficiency and stable training, the aggregation is performed over at most the first $N _ { p }$ packets associated with each flow under a micro-macro batching strategy [35], which is illustrated in the APPENDIX A-B section.

c) Flow-Level Prediction: The aggregated flow-level representation $\mathbf { h } ^ { ( \mathcal { F } ) }$ is then passed through a prediction head to produce flow-level logits:

$$
\hat {\mathbf {y}} ^ {(\text { flow })} = f _ {\text { pred }} ^ {(\text { flow })} (\mathbf {h} ^ {(\mathcal {F})}), \tag {25}
$$

where yˆ denotes the predicted class logits for the entire traffic flow.

Given the ground-truth flow label y, the main classification loss is defined as

$$
\mathcal {L} ^ {\text {(flow)}} = \mathcal {L} _ {f} (\hat {\mathbf {y}} ^ {\text {(pkt)}}, \mathbf {y}), \tag {26}
$$

where $\mathcal { L } _ { f }$ denotes the Focal Loss. To stabilize optimization and preserve packet-level discriminative capability, an auxiliary packet-level loss is additionally introduced:

$$
\mathcal {L} ^ {\mathrm{(pkt)}} = \frac {1}{N} \sum_ {i = 1} ^ {N} \mathcal {L} _ {f} (\hat {\mathbf {y}} ^ {\mathrm{(pkt)}}, \mathbf {y}). \tag {27}
$$

Thus, the final training objective is defined as a weighted combination:

$$
\mathcal {L} = \mathcal {L} ^ {\text {(flow)}} + \lambda_ {1} \mathcal {L} ^ {\text {(pkt)}} + \lambda_ {2} \sum_ {k} \mathcal {H} (\boldsymbol {g} _ {k}), \tag {28}
$$

where $\textstyle \sum _ { k } { \mathcal { H } } ( g _ { k } )$ denotes the feature gating entropy for fieldwise gating vector $\mathbf {  { g } } _ { k } . \ \lambda _ { 1 }$ , set to 0.3 in our experiments, controls the auxiliary packet-level supervision. $\lambda _ { 2 }$ is a small regularization coefficient $( \mathbf { e . g . , 1 0 ^ { - 4 } } )$ that encourages moderate differentiation among field-level gating values.

# VII. EVALUATION

# A. Experimental Settings

a) Datasets: To evaluate the performance of PTGAMoE under a no-leakage experimental scenario, we employ two benchmark datasets covering modern TLS1.3 traffic scenarios.

• CSTNET-TLS1.3 is a public benchmark dataset for TLS1.3-encrypted web traffic classification, consisting of exclusively encrypted sessions across 26 domains without unencrypted traffic components.   
CipherSpectrum is a contemporary public dataset designed for cipher-agnostic encrypted traffic classification tasks, containing 120,000 TLS1.3-encrypted sessions across 41 domains with uniform coverage of three mandated/recommended TLS1.3 cipher suites (1,000 sessions per suite per class).   
b) Baselines: To ensure a fair and comprehensive evaluation, we select three of the most popular state-of-the-art (SOTA) open-source models. Specifically, ET-BERT, YaTC and RBLJAN are chosen to be the baseline SOTA models, representing tokenized pre-training, image-like matrix processing, and byte-level methods, respectively. To rigorously assess genuine classification capabilities, model performance is evaluated under a strict setting where explicit Strong Identification Information (SII) is excluded. This includes Ethernet layer attributes, source/destination IP addresses, source/destination port numbers, and the Server Name Indication (SNI) field within the TLS handshake. Notably, to construct a dataleakage-free experimental scenario, all flows sharing the same 5-tuple are assigned to the same subset, meaning that flows are strictly isolated across the training, validation, and test sets.

c) Metrics: In addition to standard classification metrics derived from the confusion matrix (e.g., macro-F1), we introduce gate-based metrics to analyze the importance and utilization patterns of protocol fields and layer experts in PTGAMoE.

• Normalized Gate Importance (NGI). PTGAMoE employs sigmoid-based gating at both field and expert levels. For field-level analysis, given gate values {gi} with $g _ { i } ~ \in ~ ( 0 , 1 )$ , NGI is defined using temperature-scaled softmax normalization:

$$
\tilde {g} _ {i} = \frac {\exp (g _ {i} / \tau)}{\sum_ {j} \exp (g _ {j} / \tau)}, \tag {29}
$$

where τ controls the sharpness of the distribution and is set to 0.2. For expert-level analysis, let $\omega _ { k } ( { \bf x } )$ denote the input-conditioned expert weight for sample x. We first compute the expected expert importance

$$
\bar {\omega} _ {k} = \mathbb {E} _ {\mathbf {x}} [ \omega_ {k} (\mathbf {x}) ], \tag {30}
$$

and apply the same normalization:

$$
\tilde {\omega} _ {k} = \frac {\exp (\bar {\omega} _ {k} / \tau)}{\sum_ {j} \exp (\bar {\omega} _ {j} / \tau)}. \tag {31}
$$

NGI therefore provides normalized importance scores that enable direct comparison across protocol fields or experts.

• Gate Concentration Ratio (GCR). To measure how concentrated the model’s preference is, we define the Gate Concentration Score as the Shannon entropy of the NGI distribution:

$$
\mathrm{GCS} = - \sum_ {i} \tilde {g} _ {i} \log \tilde {g} _ {i}. \tag {32}
$$

Lower GCS indicates that the model focuses on a small subset of dominant fields or experts, while higher GCS implies more distributed utilization. For a layer or expert containing N gated elements, we additionally examine the Gate Concentration Ratio

$$
\mathrm{GCR} = \frac {\log N}{\mathrm{GCS}} \tag {33}
$$

to characterize how close the distribution is to uniform. When this ratio approaches 1, the NGI distribution is close to uniform, indicating balanced utilization. As the ratio deviates from 1 (e.g., log N/GCS > 1), the model exhibits increasingly selective preference toward a subset of features or experts.

d) Experimental Environment: We implement the PTG-AMoE prototype on a server with an AMD Ryzen 5 5600G CPU, 32 GB memory, an NVIDIA GeForce RTX 4060 GPU (8 GB), and Ubuntu 22.04. The software environment is configured with Python 3.12.8 and PyTorch 2.5.1, with CUDA 12.6 enabled for GPU acceleration. Graph-based operations are implemented using the PyTorch Geometric library (version 2.6.1).

![](images/316dccf6ba28f5b78f3b295d2ce05150c9d029cbe8dcdcaa0f1063c88ca8fd41.jpg)

<details>
<summary>bar</summary>

| Dataset          | ET-BERT | YaTC  | RBLJAN | PTGAMoE (Ours) |
| ---------------- | ------- | ----- | ------ | -------------- |
| CSTNET-TLS1.3    | 64.48   | 83.92 | 79.61  | 92.65          |
| CipherSpectrum   | 28.48   | 61.71 | 55.29  | 87.15          |
</details>

Fig. 6: Macro-F1 performance comparison under strict scenarios.

# B. Classification Performance

We evaluate PTGAMoE against three representative SOTA models, namely ET-BERT, YaTC, and RBLJAN, on two benchmark datasets under strict no-leakage and weak-indicator settings with flow expert disabled. The results are summarized in Fig. 6.

On CSTNET-TLS1.3, PTGAMoE achieves a macro-F1 score of 92.65%, significantly outperforming all baselines. In comparison, RBLJAN and YaTC achieve 83.92% and 79.61%, respectively, while ET-BERT reaches only 64.48%. This demonstrates that PTGAMoE can effectively capture protocol semantics even when strong identification features are removed. On CipherSpectrum, PTGAMoE also achieves the best performance with a macro-F1 of 87.15%, substantially surpassing RBLJAN, YaTC, and ET-BERT. The performance gap is particularly pronounced compared to ET-BERT, whose reliance on sequential patterns becomes insufficient under strict feature constraints.

Overall, PTGAMoE consistently outperforms all baselines across datasets, with improvements of over 8.7% on CSTNET-TLS1.3 and 25.4% on CipherSpectrum compared to the strongest baseline. These results indicate that PTGAMoE provides a more robust and generalizable solution for encrypted traffic classification under realistic deployment conditions.

# C. Field-level Interpretability Analysis

To investigate the decision mechanism of PTGAMoE under strict no-leakage and flow-isolated settings, we analyze field importance using Normalized Gate Importance (NGI) referring to equation (29) and Gate Concentration Ratio (GCR) referring to equation (33).

As shown in Fig. 7, consistent patterns emerge across datasets. At the IP layer, traffic-handling fields such as differentiated services fields and flags are consistently ranked higher than static identifiers (e.g., version-related fields), indicating reliance on packet processing semantics. At the TCP core layer, fields related to flow control and connection state (e.g., window size, header length, and flags) dominate, reflecting connection-level behavior rather than identifier-based cues. For TCP options, structural fields (e.g., SACK, MSS) are generally more important than timestamp-related features, suggesting that temporal signals are not universally dominant. At higher layers, the TLS handshake focuses on negotiation semantics (e.g., signature/hash algorithms and extensions), while the TLS record layer is primarily driven by structural features such as length and aggregation fields. Notably, the sink node appears as a top feature only in certain cases, indicating that it acts as a conditional global aggregator rather than a shortcut feature.

![](images/1374d839fe08d1fb6e991fc7224028d77146b729882ea1bb5f968cadb79b78d4.jpg)

<details>
<summary>bar_line</summary>

| Method | IP NGI Score | TCP Core NGI | TCP Core Bottom2 NGI | TCP Options NGI | TCP Options Bottom2 NGI | TLS Handshake NGI | TLS Handshake Bottom2 NGI | TLS Record Top3 NGI | TLS Record Top3 NGI | TLS Record Bottom2 NGI | TLS Record GCR |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CSTNET-TLS1.3 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 1.00 |
| CiphertextSpectrum | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 1.00 |
| Top3 NGI | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 1.00 |
| Bottom2 NGI | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 1.00 |
| GCR | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 0.85 | 1.00 |
The chart displays a line graph with markers indicating trends across five categories: IP, TCP Core, TCP Options, TLS Handshake, and TLS Record.
</details>

Fig. 7: Field-level importance (NGI) and concentration (GCR) across protocol layers.

Compared to conventional packet-level models, which often rely on strong identifiers (e.g., IP, ports, or SNI), PTGAMoE demonstrates a clear shift toward behavior-driven features, including packet size patterns, transport dynamics, and protocol structure. This confirms that the model captures intrinsic protocol semantics under strict settings.

The GCR analysis further shows that feature importance remains well-distributed within each layer. On CSTNET-TLS1.3, all layers exhibit GCR values close to 1, indicating highly balanced feature utilization. On CipherSpectrum, slightly higher GCR values are observed, peaking at 1.025 particularly in the TLS record layer, which suggests a moderate dataset-specific concentration on structural features.

Overall, these results demonstrate that PTGAMoE performs semantics-aware and distributed reasoning, effectively avoiding shortcut learning while adaptively leveraging both local protocol fields and global context.

D. Layer-level Interpretability Analysis   
![](images/a2f2f2a25c439f833b168f2e7e7ba9e0fbcf93b65ffb164fb2727813585031f9.jpg)

<details>
<summary>bar_line</summary>

| Dataset          | IP    | TLS Handshake | TCP Core | TLS Record | TCP Options | GCR  |
| ---------------- | ----- | ------------- | -------- | ---------- | ----------- | ---- |
| CSTNET-TLS1.3    | 0.48  | 0.03          | 0.42     | 0.03       | 0.03        | 1.55 |
| CipherSpectrum   | 0.20  | 0.15          | 0.10     | 0.17       | 0.17        | 1.05 |
</details>

Fig. 8: Layer-level expert importance and contribution patterns.

TABLE I: Ablation results for SII and Flow Expert (Macro-F1 %). 

<table><tr><td>Setting</td><td>CSTNET-TLS1.3</td><td>CipherSpectrum</td></tr><tr><td>Final (w/o SII, w/o Flow Expert)</td><td>92.65</td><td>87.15</td></tr><tr><td>w SII</td><td>93.05</td><td>94.23</td></tr><tr><td> $\Delta_{\text{SII}}$ </td><td>+0.40</td><td>+7.08</td></tr><tr><td>w Flow Expert</td><td>92.55</td><td>47.27</td></tr><tr><td> $\Delta_{\text{Flow}}$ </td><td>-0.10</td><td>-39.88</td></tr></table>

We further analyze the layer-level expert behavior using NGI and GCR to understand how PTGAMoE allocates importance across protocol layers.

On CSTNET-TLS1.3, the model exhibits strong layer concentration, with IP and TCP core dominating the decision process, while higher-layer experts contribute marginally. This is reflected by a high GCR value of 1.53, indicating that classification primarily relies on transport-level behavior. This suggests that discriminative patterns in this dataset are mainly captured by packet handling and connection dynamics rather than TLS semantics. In contrast, CipherSpectrum shows a much more balanced expert distribution, where all experts contribute evenly to yield a GCR of 1.06. The TLS record expert becomes the most important component, indicating that structural features at the application layer play a dominant role. Meanwhile, IP, TCP options, and TLS handshake also contribute significantly, demonstrating cross-layer collaboration.

These results reveal that PTGAMoE adaptively adjusts expert importance according to dataset characteristics, while avoiding expert collapse. The model selectively emphasizes the most informative protocol layers while maintaining multilayer semantic integration, confirming its ability to capture intrinsic traffic behavior under strict settings.

# E. Impact of Strong Indication Information

To assess whether the performance gain mainly comes from intrinsic protocol semantics or shortcut identity cues, we further compare PTGAMoE under settings with and without strong indication information (SII). The macro-F1 results are reported in Table I, while representative confusion matrices are shown in Fig. 9.

As shown in Table I, the impact of SII is highly datasetdependent. On CSTNET-TLS1.3, the macro-F1 score increases only marginally from 92.65% to 93.05%, indicating that most discriminative information can already be captured from protocol structure, transport behavior, and flow-level dynamics. In contrast, on CipherSpectrum, the macro-F1 score rises substantially from 87.15% to 94.23%, suggesting that this dataset contains much stronger identity-related cues and is therefore more sensitive to shortcut features.

![](images/3333177a64e41aa7a0bce4c966e4398fde51ec8eca78ed662cf85068e7aa3fbd.jpg)  
Fig. 9: Impact of Strong Identification Information (SII) on classification confusion patterns.

The representative confusion matrices of CSTNET-TLS1.3 further support this observation. Even without SII, most selected domains remain well separated, and the residual errors are concentrated in a small number of confusing groups, most notably msn.com, media.net, and ibm.com. Additional minor confusions can also be observed around gitlab.com, mozilla.org, grammarly.com, and notion.so. After introducing SII, these residual errors are only slightly reduced, which is consistent with the marginal overall F1 improvement. This indicates that CSTNET-TLS1.3 is primarily semanticsdominant, where classification mainly relies on intrinsic protocol behavior rather than strong identity indicators.

By contrast, the representative confusion matrices of CipherSpectrum shows a much heavier dependency on SII. Without SII, substantial confusion appears among domains sharing similar infrastructure, service ecosystems, or content delivery patterns. Typical examples include the portal pair web.de and gmx.net, the regional pair yahoo.co.jp and yimg.jp, as well as several Google-related services such as googletagmanager.com, googleapis.com, gstatic.com, and google.com. These confusions are significantly alleviated once SII is introduced, leading to a much cleaner class separation. This behavior indicates that CipherSpectrum is considerably more SII-sensitive, and that strong indicators can simplify the task by providing direct identity cues.

Overall, these results show that the availability of SII can substantially alter task difficulty and evaluation credibility. In particular, the large gain on CipherSpectrum suggests that retaining strong indicators may overestimate model capability by allowing shortcut learning. Therefore, removing SII is necessary for rigorously evaluating whether a model truly learns behavior-driven protocol semantics rather than superficial identifiers. The relatively small performance drop on CSTNET-TLS1.3, together with the still strong performance on CipherSpectrum under the w/o SII setting, demonstrates that PTGAMoE remains effective under strict weak-indicator conditions.

# F. Impact of the Flow Expert

We further evaluate whether an explicit flow-level expert provides additional benefits beyond the proposed flow-level aggregation mechanism.

As shown in TABLE I, the impact of the Flow Expert is highly negative overall. On CSTNET-TLS1.3, the macro-F1 score changes only marginally from 92.65% to 92.55%, indicating that the Flow Expert provides no meaningful improvement. On CipherSpectrum, the macro-F1 score drops drastically from 87.15% to 47.27%, revealing a severe performance degradation.

As shown in Fig. 10, the representative confusion matrices further illustrate this difference. On CSTNET-TLS1.3, the error patterns remain largely similar with and without the Flow Expert, and only minor fluctuations are observed on a few classes. This suggests that the Layer Expert Committee and the flow-level aggregation mechanism already capture most of the useful discriminative information. However, the Flow Expert causes widespread confusion across many classes on CipherSpectrum. Without the Flow Expert, the confusion is relatively structured and primarily occurs within semantically related groups, such as the portal pair web.de and gmx.net, or clusters of tracking and content delivery services (e.g., sharethis.com, flipboard.com, and segment.com). However, after introducing the Flow Expert, the confusion becomes widespread and no longer constrained within these semantic clusters. Many classes that were previously well distinguished, such as sharethis.com, coinbase.com, and hubspot.com, exhibit severe degradation, with predictions spreading across a large number of unrelated classes. This indicates that the Flow Expert introduces a strong noise source that disrupts the learned decision boundaries.

These results suggest that the performance gain of the proposed flow-enhanced framework mainly comes from flowlevel aggregation and supervision, rather than from an explicit Flow Expert based on coarse-grained statistical features. In complex multi-class scenarios such as CipherSpectrum, the Flow Expert may even become misleading, as many classes share similar flow statistics while differing in finer protocol semantics. Therefore, we exclude the Flow Expert in the final configuration and retain only the flow-level aggregation mechanism.

# VIII. CONCLUSION

In this paper, we present PTGAMoE, a protocol-aware framework for encrypted traffic analysis that explicitly models the hierarchical structure of network protocols. By integrating Protocol Tree Graph Attention (PTGA) with a layer-wise Mixture-of-Experts (MoE) architecture, the model captures fine-grained field semantics without disruptive padding. Crucially, we introduce a permutation-invariant flow aggregation mechanism to ensure robust classification within strict scenarios, where the exclusion of strong identification information (SII) and the implementation of flow-isolated splitting prevent the exploitation of deceptive shortcuts. Extensive experiments on modern TLS 1.3 datasets demonstrate that PTGAMoE consistently outperforms SOTA models. Furthermore, hierarchical gating mechanisms and the proposed NGI and GCS metrics provide quantifiable interpretability at both field and protocol levels. These results reinforce that protocol-native structural modeling provides a reliable, semantic-preserving foundation for robust encrypted traffic analysis. Future work will explore extending PTGAMoE to a broader range of protocols (e.g., UDP-based protocols and proxy-related protocols) and more diverse network environments.

![](images/2f97e33d05a69d4f2294dd0089b1ba94116843e80e6c62175ab2d801cc1568b8.jpg)  
Fig. 10: Confusion matrices comparison between settings with and without the Flow Expert.

# REFERENCES

[1] E. Papadogiannaki and S. Ioannidis, “A survey on encrypted network traffic analysis applications, techniques, and countermeasures,” ACM Computing Surveys (CSUR), vol. 54, no. 6, pp. 1–35, 2021.   
[2] C. Cremers, M. Horvat, J. Hoyland, S. Scott, and T. Van Der Merwe, “A comprehensive symbolic analysis of tls 1.3,” in Proceedings of the 2017 ACM SIGSAC conference on computer and communications security, 2017, pp. 1773–1788.   
[3] K. Bhargavan, V. Cheval, and C. Wood, “A symbolic analysis of privacy for tls 1.3 with encrypted client hello,” in Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security, 2022, pp. 365–379.   
[4] E. Rescorla, “The Transport Layer Security (TLS) Protocol Version 1.3,” RFC 8446, Aug. 2018. [Online]. Available: https://www.rfc-editor. org/info/rfc8446   
[5] H. Li, J. Tao, L. Yu, Y. Luo, and Z. Wang, “Gspb: a global-statistic and packet-byte fusion framework for encrypted traffic classification,” Cybersecurity, vol. 8, no. 1, p. 120, 2025.   
[6] X. Tang, J. Tao, and Y. Luo, “Attention-guided multi-view feature fusion for proxy traffic classification,” in International Conference on Neural Information Processing. Springer, 2025, pp. 425–439.   
[7] P. Velickovi ˇ c, G. Cucurull, A. Casanova, A. Romero, P. Li ´ o, and \` Y. Bengio, “Graph attention networks,” in International Conference on Learning Representations, 2018.   
[8] N. Fu, G. Cheng, and X. Su, “Accurate compressed traffic detection via traffic analysis using graph convolutional network based on graph structure feature,” Computer Communications, vol. 207, pp. 128–139, 2023.   
[9] T.-L. Huoh, Y. Luo, P. Li, and T. Zhang, “Flow-based encrypted network traffic classification with graph neural networks,” IEEE Transactions on Network and Service Management, vol. 20, no. 2, pp. 1224–1237, 2022.

[10] G. Combs, “Adding information to the dissection tree,” accessed: 2025- 12-20. [Online]. Available: https://www.wireshark.org/docs//wsdg html chunked/lua module Tree.html   
[11] W. Cai, J. Jiang, F. Wang, J. Tang, S. Kim, and J. Huang, “A survey on mixture of experts in large language models,” IEEE Transactions on Knowledge and Data Engineering, 2025.   
[12] Y. Mirsky, T. Doitshman, Y. Elovici, and A. Shabtai, “Kitsune: An ensemble of autoencoders for online network intrusion detection,” in 25th Annual Network and Distributed System Security Symposium, NDSS 2018. The Internet Society, 2018.   
[13] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “Fs-net: A flow sequence network for encrypted traffic classification,” in IEEE INFOCOM 2019- IEEE Conference On Computer Communications. IEEE, 2019, pp. 1171–1179.   
[14] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in Proceedings of the ACM Web Conference 2022, 2022, pp. 633–642.   
[15] R. Zhao, M. Zhan, X. Deng, Y. Wang, Y. Wang, G. Gui, and Z. Xue, “Yet another traffic classifier: A masked autoencoder based traffic transformer with multi-level flow representation,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 37, no. 4, 2023, pp. 5420–5427.   
[16] G. Zhou, X. Guo, Z. Liu, T. Li, Q. Li, and K. Xu, “Trafficformer: an efficient pre-trained model for traffic data,” in 2025 IEEE symposium on security and privacy (SP). IEEE, 2025, pp. 1844–1860.   
[17] A. Bahramali, A. Bozorgi, and A. Houmansadr, “Realistic website fingerprinting by augmenting network traces,” in Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security, 2023, pp. 1035–1049.   
[18] C. Fu, Q. Li, M. Shen, and K. Xu, “Detecting tunneled flooding traffic via deep semantic analysis of packet length patterns,” in Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security, 2024, pp. 3659–3673.   
[19] S. Zhu, S. Li, Z. Wang, X. Chen, Z. Qian, S. V. Krishnamurthy, K. S. Chan, and A. Swami, “You do (not) belong here: detecting dpi evasion attacks with context learning,” in Proceedings of the 16th International Conference on emerging Networking EXperiments and Technologies, 2020, pp. 183–197.   
[20] Y. Sharon, D. Berend, Y. Liu, A. Shabtai, and Y. Elovici, “Tantra: Timing-based adversarial network traffic reshaping attack,” IEEE Transactions on Information Forensics and Security, vol. 17, pp. 3225–3237, 2022.   
[21] X. Xiao, S. Wang, G. Hu, Q. Li, K. Mao, X. Luo, B. Zhang, and S. Xia, “Rbljan: Robust byte-label joint attention network for network traffic classification,” IEEE Transactions on Dependable and Secure Computing, 2024.   
[22] Y. Zhu, J. Tao, H. Wang, L. Yu, Y. Luo, T. Qi, Z. Wang, and Y. Xu, “Dgnn: Accurate darknet application classification adopting attention graph neural network,” IEEE Transactions on Network and Service Management, 2023.   
[23] T.-L. Huoh, Y. Luo, P. Li, and T. Zhang, “Flow-based encrypted network traffic classification with graph neural networks,” IEEE Transactions on Network and Service Management, vol. 20, no. 2, pp. 1224–1237, 2022.   
[24] X. Qiu, G. Cheng, W. Zhu, D. Niu, and N. Fu, “Dual-channel interactive graph transformer for traffic classification with message-aware flow

representation,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 39, no. 1, 2025, pp. 685–693.   
[25] K. Team, Y. Bai, Y. Bao, G. Chen, J. Chen, N. Chen, R. Chen, Y. Chen, Y. Chen, Y. Chen et al., “Kimi k2: Open agentic intelligence,” arXiv preprint arXiv:2507.20534, 2025.   
[26] C. Riquelme, J. Puigcerver, B. Mustafa, M. Neumann, R. Jenatton, A. Susano Pinto, D. Keysers, and N. Houlsby, “Scaling vision with sparse mixture of experts,” Advances in Neural Information Processing Systems, vol. 34, pp. 8583–8595, 2021.   
[27] L. Xiaomi, B. Xia, B. Shen, D. Zhu, D. Zhang, G. Wang, H. Zhang, H. Liu, J. Xiao, J. Dong et al., “Mimo: Unlocking the reasoning potential of language model–from pretraining to posttraining,” arXiv preprint arXiv:2505.07608, 2025.   
[28] S. Bai, Y. Cai, R. Chen, K. Chen, X. Chen, Z. Cheng, L. Deng, W. Ding, C. Gao, C. Ge et al., “Qwen3-vl technical report,” arXiv preprint arXiv:2511.21631, 2025.   
[29] W. Fedus, B. Zoph, and N. Shazeer, “Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity,” Journal of Machine Learning Research, vol. 23, no. 120, pp. 1–39, 2022.   
[30] S. Xiaoming, W. Shiyu, N. Yuqi, L. Dianqi, Y. Zhou, W. Qingsong, and M. Jin, “Time-moe: Billion-scale time series foundation models with mixture of experts,” in ICLR 2025: The Thirteenth International Conference on Learning Representations. International Conference on Learning Representations, 2025.   
[31] X. Liu, J. Liu, G. Woo, T. Aksu, Y. Liang, R. Zimmermann, C. Liu, J. Li, S. Savarese, C. Xiong et al., “Moirai-moe: Empowering time series foundation models with sparse mixture of experts,” in International Conference on Machine Learning. PMLR, 2025, pp. 38 940–38 962.   
[32] S. Cai, L. Chen, J. Chen, S. Wang, and G. Zhang, “Cl-vime: Contrastive learning and vision mixture of experts for encrypted traffic classification,” IEEE Transactions on Network and Service Management, vol. 23, pp. 1422–1434, 2025.   
[33] N. Wickramasinghe, A. Shaghaghi, G. Tsudik, and S. Jha, “Sok: Decoding the enigma of encrypted network traffic classifiers,” in 2025 IEEE Symposium on Security and Privacy (SP). IEEE, 2025, pp. 1825– 1843.   
[34] Y. Zhao, G. Dettori, M. Boffa, L. Vassio, and M. Mellia, “The sweet danger of sugar: Debunking representation learning for encrypted traffic classification,” in Proceedings of the ACM SIGCOMM 2025 Conference, 2025, pp. 296–310.   
[35] W. Wang, Y. Xia, D. Yang, X. Zhou, and D. Cheng, “Accelerating distributed dlrm training with optimized tt decomposition and microbatching,” in SC24: International Conference for High Performance Computing, Networking, Storage and Analysis. IEEE, 2024, pp. 1– 15.

# APPENDIX A IMPLEMENTATION DETAILS

# A. Streaming Field Extraction in Field-Level Preprocessing

Network traffic can be captured by tools like Wireshark, which saves the captured traffic packets into PCAP files. Due to the long time development and modification of global researchers and developers, Wireshark has abundant inner dissectors for various network protocols. The dissectors dissect the raw packet bytes by the structural protocol architectures and display the dissected packet fields into a dissection tree. The dissection tree not only can be examined in Wireshark GUI, but also can be exported into a detailed PDML (Packet Description Markup Language) file, which conforms to the XML standard and contains details about the packet dissection. Leveraging the PDML file, we can extract the hierarchical fields into the most common CSV format.

However, the PDML file is a double-edged sword, which makes the direct extraction cause huge memory and storage expenditure, because of its global detailed field records for the whole PCAP file. A MB-level PCAP may generate a GBlevel XML, which is unacceptable in the view of memory and storage. To address this issue, we design a streaming PCAP-to-CSV converter that couples tShark’s byte pipe PDML output with chunk-wise constant memory parsing, addressing the bottleneck of traditional offline processing. Each chunk is immediately appended to the target CSV, eliminating GB level temporary files and bounding RAM consumption to $O ( c )$ , in which c is the size of each chunk. Complexity drops from $\Omega ( n )$ memory of the classic PDML to CSV pipeline to $O ( c )$ memory, yielding about 10× peak RAM reduction.

# B. Batch Settings under the Strict Scenario

To support strict flow-isolated training and maximize GPU utilization, we employ a hierarchical micro-macro batching mechanism.

a) Micro-Batch for Flow-centric Truncation: To maintain flow-level structural integrity, each individual flow with $N _ { f }$ packets $\mathcal { F } _ { i } = \{ p _ { i , 1 } , \dots , p _ { i , N _ { f } } \}$ is treated as a single microbatch. We define a micro-batch size $N _ { p }$ (max packets per flow) to truncate or pad the sequences:

$$
\widetilde {\mathcal {F}} _ {i} = \{p _ {i, 1}, \dots , p _ {i, \min (N _ {f}, N _ {p})} \}. \tag {34}
$$

This ensures that all packets within a micro-batch belong to the same flow, preventing cross-flow interference and facilitating the permutation-invariant aggregation stage.

b) Macro-Batch for Parallel GPU Acceleration: For computational efficiency, multiple micro-batches are aggregated into a macro-batch $B _ { t }$ for each optimization step $S _ { t }$ . Given a macro-batch size $K _ { f }$ (flows per step), the batch is constructed as:

$$
\mathcal {B} _ {t} = \bigcup_ {i \in \mathcal {S} _ {t}} \widetilde {\mathcal {F}} _ {i}, \quad | \mathcal {S} _ {t} | = K _ {f}. \tag {35}
$$

This design allows the GPU to process $K _ { f }$ flows in parallel while keeping the total packet count per step bounded by $| B _ { t } | \le K _ { f } N _ { p }$ .

In our implementation, we set $N _ { p } = 6 4$ and $K _ { f } = 6 4$ .

# C. Flow-Level Feature Engineering

When enabled, the flow-level expert utilizes eight statistical features computed by grouping packets according to transportlayer identifiers. To prevent information leakage, all statistics are computed independently for each data split. The features include: (1) count (total packets). (2) length (mean, std. dev., and ratio of packets $> 1 4 0 0$ bytes). (3) IAT (mean, std. dev., and max inter-arrival time). (4) normalized duration (flow duration per packet). Most features are normalized by packet count to ensure consistency across datasets, and timing-related metrics are only extracted when valid timestamps are available.
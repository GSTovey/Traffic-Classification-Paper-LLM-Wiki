# TrafficMoE: Heterogeneity-aware Mixture of Experts for Encrypted Traffic Classification

Qing He, Xiaowei Fu, and Lei Zhang, Senior Member, IEEE

Abstract—Encrypted traffic classification is a critical task for network security. While deep learning has advanced this field, the occlusion of payload semantics by encryption severely challenges standard modeling approaches. Most existing frameworks rely on static and homogeneous pipelines that apply uniform parameter sharing and static fusion strategies across all inputs. This “one-size-fits-all” static design is inherently flawed: by forcing structured headers and randomized payloads into a unified processing pipeline, it inevitably entangles the raw protocol signals with stochastic encryption noise, thereby degrading the fine-grained discriminative features. In this paper, we propose TrafficMoE, a framework that breaks through the bottleneck of static modeling by establishing a Disentangle–Filter–Aggregate (DFA) paradigm. Specifically, to resolve the structural betweencomponents conflict, the architecture disentangles headers and payloads using dual-branch sparse Mixture-of-Experts (MoE), enabling modality-specific modeling. To mitigate the impact of stochastic noise, an uncertainty-aware filtering mechanism is introduced to quantify reliability and selectively suppress highvariance representations. Finally, to overcome the limitations of static fusion, a routing-guided strategy aggregates cross-modality features dynamically, that adaptively weighs contributions based on traffic context. With this DFA paradigm, TrafficMoE maximizes representational efficiency by focusing solely on the most discriminative traffic features. Extensive experiments on six datasets demonstrate TrafficMoE consistently outperforms stateof-the-art methods, validating the necessity of heterogeneityaware modeling in encrypted traffic analysis. The source code is publicly available at https://github.com/Posuly/TrafficMoE main.

Index Terms—Encrypted traffic classification, TrafficMoE.

# I. INTRODUCTION

N ETWORK traffic classification plays a fundamental rolein network security, traffic management, and quality- in network security， traffc management, and qualityof-service (QoS) assurance. With the rapid growth of the Internet and IoT deployments, modern network traffic has become increasingly complex and diverse. In particular, the widespread adoption of encryption technologies (e.g., TLS) and anonymization mechanisms (e.g., VPNs) has significantly challenged traditional traffic analysis techniques, making encrypted traffic classification a critical yet challenging problem.

Early studies mainly relied on port-based and payloadbased methods for traffic classification [1], [2]. While these

This work was partially supported by National Natural Science Fund of China under Grants 92570110 and 62271090, Chongqing Natural Science Fund under Grant CSTB2024NSCQ-JQX0038, and National Youth Talent Project. (Corresponding author: Lei Zhang)

Q. He, X. Fu and L. Zhang are with the School of Microelectronics and Communication Engineering, Chongqing University, Chongqing 400044, China. (E-mail: qinghe@cqu.edu.cn, leizhang@cqu.edu.cn, xwfu@cqu.edu.cn)

Manuscript received April 19, 2021; revised August 16, 2021.

approaches can achieve satisfactory performance in plaintext scenarios, their effectiveness is severely degraded under encrypted traffic. To address this issue, statistical and machine learning–based methods were proposed, leveraging flow-level features such as packet sizes and temporal patterns [3], [4]. Although applicable to encrypted environments, these methods depend heavily on hand-crafted features and often suffer from limited generalization. More recently, deep learning based approaches have demonstrated superior capability in automatically learning discriminative representations from raw traffic data, yet they typically require large-scale labeled datasets and still struggle to generalize across unseen applications and encryption settings [5]–[9]. Inspired by the success of self-supervised learning, pre-training techniques have emerged as a promising paradigm for encrypted traffic classification [10]–[12]. By learning generic traffic representations from large amounts of unlabeled data, these approaches significantly reduce the reliance on labeled samples and improve robustness across domains. Despite these advances, most existing frameworks rely on largely homogeneous modeling pipelines. By employing uniform parameter sharing and static fusion strategies across the whole traffic data, these methods implicitly operate under a stationary assumption: treating the contribution of diverse traffic components across samples equally. This one-size-fits-all design overlooks the complexity of encrypted traffic by simply forcing structurally diverse signals into a static processing pipeline. Consequently, the model lacks flexibility to varying information density inherent in different traffic segments.

However, encrypted traffic is inherently heterogeneous. A typical flow comprises two distinct modalities: headers, which encapsulate deterministic protocol logic, and encrypted payloads, which exhibit high-entropy and stochastic characteristics. Moreover, the discriminative properties of these components are not uniform, which fluctuates depending on the application type and encryption settings. Modeling such dynamic data with static architectures creates a misalignment in inductive bias. Specifically, uniform mechanisms inherently conflate protocol logic with random encryption noise, thereby diminishing the model’s sensitivity to fine-grained features.

From this perspective, current limitations mainly arise from three key factors. First, uniform parameter sharing constrains modeling capacity, failing to decouple the deterministic syntax of headers from the stochastic patterns of payloads. Second, indiscriminate processing treats all tokens equally, allowing inherent encryption noise to propagate and degrade feature quality. Third, static fusion strategies overlook the samplespecific context and the varying discriminative utility of headers as well as payloads across flows. Collectively, these issues facilitate the proposed new framework that explicitly disentangles semantic modeling of headers and encrypted payloads, and dynamically adapts feature integration.

![](images/d3a382d82f18320112cad0762f07af0994d462b6573d912f70ceff434a1c1945.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Message Traffic"] --> B["Preprocess"]
    C["Download Traffic"] --> B
    D["Video Traffic"] --> B
    B --> E["PE"]
    B --> F["HE"]
    E --> G["F"]
    F --> G
    G --> H["Output"]
```
</details>

(a) Existing paradigm

![](images/6ba6f5c0f99d7b044d4b0ec8361792a44d1225bf054b529c47ddbb91ecc74aa0.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Message Traffic"] --> B["Download Traffic"]
    B --> C["Traffic Preprocess"]
    C --> D["Video Traffic"]
    D --> E["FE"]
    E --> F["E"]
    F --> G["UF"]
    G --> H["2A"]
    H --> I["Output"]
    D --> J["PE"]
    J --> K["E"]
    K --> L["UF"]
    L --> M["2A"]
    M --> N["Output"]
```
</details>

(b) TrafficMoE framework   
Fig. 1: Comparison between existing modeling paradigms and the proposed TrafficMoE framework. Existing paradigm (a) typically process heterogeneous traffic components in a unified manner with static fusion strategies, whereas TrafficMoE (b) explicitly disentangles headers and payloads, incorporates uncertainty-aware filtering (UF), and performs conditional aggregation (CA) guided by MoE routing probabilities for adaptive and context-aware integration.

To address this challenge, we propose TrafficMoE, a heterogeneity-aware framework designed to harmonize modeling architectures according to the heterogeneous properties of headers and encrypted payloads in the encrypted traffic. The framework follows a Disentangle–Filter–Aggregate paradigm. Specifically, headers and payloads are decoupled into separate branches, each employing sparse Mixture-of-Experts (MoE) to enable disciminative modeling. To counteract noisy components, an uncertainty-aware filtering mechanism is proposed to quantify token reliability and selectively attenuate high-variance patterns. Finally, a routing-guided fusion strategy dynamically re-weights cross-modality features according to sample-specific context. Through this paradigm, TrafficMoE shifts from the “one-size-fits-all” static modeling to heterogeneity-aware dynamic modeling, strictly optimizing representation capacity for different traffic segments.

Fig. 1 illustrates the key differences between existing traffic classification pipelines and our proposed framework. Fig. 1a indicates that in existing paradigm, headers and payloads are typically processed as largely homogeneous sequences with static fusion strategies, that treat all traffic components equally. This design implicitly assumes uniform contribution from different components, potentially obscuring their individual discriminative representations. In contrast, Fig. 1b indicate TrafficMoE explicitly disentangles the headers and payloads into separate modalities, applies an uncertainty-aware filtering (UF) to suppress unreliable tokens, and performs a routing guided implicit conditional aggregation (CA). This dynamic and context-aware integration allows the model to adaptively leverage heterogeneous traffic cues according to sample-specific characteristics, resulting in more effective and robust representation learning for headers and payloads.

In summary, our contributions are threefold:

• We identify the uniform modeling of headers and payloads without distinction as a fundamental limitation of existing homogeneous pipelines, and reformulate a new encrypted traffic classification framework from a

novel perspective of heterogeneity-aware disentangling modeling across heterogeneous traffic components and sample-dependent contexts.

• We propose TrafficMoE, a heterogeneity-aware sparse Mixture-of-Experts architecture that realizes hierarchical computation for headers and encrypted payloads. The framework follows a Disentangle–Filter–Aggregate paradigm, i.e., explicitly disentangles the headers and payloads as two modalities, filters unreliable tokens via uncertainty weighting and implicitly aggregate features across modalities for encrypted traffic representation.   
• We conduct extensive experiments on six encrypted traffic datasets and demonstrate that TrafficMoE consistently achieves state-of-the-art classification performance compared with existing methods.

# II. RELATED WORK

# A. Encrypted Traffic Classification

Encrypted traffic classification has been extensively studied in network security and traffic analysis, due to the widespread adoption of encryption protocols that invalidate traditional port-based and payload inspection techniques. Early learningbased approaches focused on extracting statistical features or modeling packet sequences to characterize encrypted flows. Deep Packet [5] leverages stacked autoencoders and convolutional networks to classify encrypted applications directly from raw packet bytes, demonstrating the feasibility of deep representation learning in encrypted scenarios. Subsequent studies explored more expressive sequence modeling architectures to capture temporal and structural patterns within traffic flows. Flow-level sequence models, such as FS-Net [13], treat encrypted traffic as ordered packet sequences and employ convolutional or recurrent architectures to learn discriminative flow representations. Hybrid CNN–RNN models further integrate spatial and temporal feature extraction, as exemplified by TSCRNN [14], which is particularly effective in industrial IoT environments. In parallel, several works reformulate traffic as image-like types in order to exploit the maturity of 2D convolutional networks for encrypted traffic classification [15].

More recently, pretraining techniques have emerged as a dominant paradigm for universal representation. ET-BERT [10] introduces transformer-based pretraining on large-scale unlabeled traffic corpora, learning contextualized universal representations transferable to multiple encrypted traffic tasks. Building upon this idea, generative or language-inspired models such as NetGPT [16] and Language of Network [17] further extend pretraining objectives to a unified traffic understanding and generation, showing big potential across diverse downstream applications. Beyond sequence-based modeling, several works explore alternative structural representations to improve robustness under distribution shifts. Transformer variants with multi-instance or hierarchical designs [18] and graph-based flow modeling approaches [19] aim to capture richer intraflow interactions and structural dependencies. Despite these advances, most existing methods still rely on relatively uniform modeling pipelines across heterogeneous traffic components, without distinguishing the treatment of different ingredients in encrypted traffic. This hinders traffic representations.

![](images/d54ea76858ad223c017c90b690cce50ef715c29afcbfd592ba54d406f9b343fd.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Message Traffic"] --> B["Download Traffic"]
    B --> C["Flow"]
    C --> D["Payload"]
    D --> E["Payload MoE Branch"]
    E --> F["Payload MoE Branch"]
    F --> G["Uncertainty-aware Filter"]
    G --> H["Conditional Aggregation"]
    H --> I["Output"]
    
    subgraph Legend
        J["Message Traffic"] --> K["Download Traffic"]
        L["Video Traffic"] --> M["Payload"]
        M --> N["Payload MoE Branch"]
        N --> O["Uncertainty-aware Filter"]
        O --> P["Conditional Aggregation"]
    end
    
    subgraph Legend
        Q["Message Traffic"] --> R["Download Traffic"]
        S["Video Traffic"] --> T["Payload"]
        U["Translation"] --> V["Navigation Map"]
        W["Routing Probability"] --> X["Routing Probability"]
        Y["Fh"] --> Z["Fh"]
        AA["Fph"] --> AB["Fph"]
        AC["Fgg"] --> AD["Fgg"]
    end
    
    subgraph Legend
        AE["Message Traffic"] --> AF["Download Traffic"]
        AG["Video Traffic"] --> AH["Payload"]
        AI["Translation"] --> AJ["Translation Map"]
        AK["Fgg"] --> AL["Fgg"]
    end
    
    style A fill:#f9f,stroke:#333
    style L fill:#f9f,stroke:#333
    style S fill:#f9f,stroke:#333
    style AC fill:#f9f,stroke:#333
    style AG fill:#f9f,stroke:#333
    style S fill:#f9f,stroke:#333
    style AE fill:#ccf,stroke:#333
```
</details>

Fig. 2: Overview of the TrafficMoE framework. The dual-branch MoE architecture explicitly models heterogeneous traffic components, i.e., the Header and Payload branches, which can capture intra-modality patterns, respectively. The uncertaintyaware filter suppresses unreliable tokens, i.e., noisy traffic components, and the conditional aggregation module fuses the final purified features across two modalities (header vs. payload) in a routing-guided manner for encrypted traffic classification.

# B. Mixture-of-Experts and Conditional Modeling

Mixture-of-Experts (MoE) is a classical conditional computation framework for partitioning representation capacity among specialized submodels, where a gating network dynamically routes inputs to a subset of expert networks [20], [21]. This paradigm enables the model to focus representational power on distinct subregions of the input space while minimizing redundant computation. MoE architectures have been revitalized for large-scale neural networks. Shazeer et al. [22] introduced the sparsely-gated MoE layer, which scales model capacity by activating only a few experts per input, enabling models with increased orders of magnitude parameters yet without a proportional increase in computation cost. Extensions such as GShard [23] further demonstrates that conditional routing and automatic partitioning of experts support effective scaling of very large Transformer models. The Switch Transformer [24] refines sparse routing mechanics to improve load balancing and training stability, achieving scalable performance with simplified routing strategies. MoE has also been adapted beyond language modeling into multi-task and multi-modal learning. Multi-Gate Mixture-of-Experts (MMoE) explicitly learns task-specific expert routing to share and specialize features across tasks [25]. In computer vision, sparse MoE variants such as Vision MoE (V-MoE) aggregate conditional expert selection into vision transformer architectures, achieving scalability and competitive accuracy with reduced computation compared to dense models [26].

Despite these advances, most existing MoE designs assume homogeneous input or task-level specialization, while encrypted traffic, by contrast, exhibits intrinsic structural heterogeneity, with headers and payloads carrying fundamentally distinct features. This motivates our TrafficMoE, a dual-branch MoE design, where MoE encoders and routing signals are aligned with heterogeneous traffic components, enabling adaptive and context-aware traffic representation learning.

# III. THE PROPOSED TRAFFICMOE

# A. Overview

Encrypted network traffic exhibits intrinsic modality heterogeneity: the packet headers encode compact and structured protocol semantics with relatively stable patterns, whereas payloads encode long and high-entropy byte sequences with weak and noisy semantics. Directly applying a unified encoder to such inputs without distinction often leads to biased representations. To address this, we propose TrafficMoE, a heterogeneous-aware mixture-of-experts framework by following a Disentangle–Filter–Aggregate paradigm, which is elaborated as Fig. 2. The framework comprises a Header branch and a Payload branch, each performing modality-specific sequence modeling followed by dedicated Mixture-of-Experts (MoE) layers, enabling conditional expert activation tailored to different properties of each modality. Representations from both branches are refined by an Uncertainty-aware Filtering (UF) module, in order to suppress unreliable tokens i.e., noisy traffic components based on attention-derived uncertainty, improving the stability of subsequent integration. The purified header and payload features in each branch are then aggregated via an implicit Conditional Aggregation (CA) mechanism that adaptively adjusts fusion behavior based on internal routing signals. To further enhance cross-modal adaptability and capture global traffic patterns, the aggregated representation is processed by a global MoE branch, producing a unified representation suitable for pre-training or task-specific fine-tuning.

# B. Traffic Preprocessing

The overall preprocessing pipeline is illustrated in Fig. 3. Starting from the raw packet captures, traffic is progressively transformed into structured and length-normalized byte sequences suitable for heterogeneous modeling. The pipeline comprises four stages: flow-level aggregation, packet-level decomposition, byte-level cropping and padding, and stridebased segmentation. Each stage is designed to preserve temporal ordering and structural separability while producing stable tensor inputs for subsequent modality-specific processing.

Stage 1: Flow Splitting. In network traffic analysis, a flow is defined as a sequence of packets sharing the same 5-tuple: source IP, destination IP, source port, destination port, and transport protocol. The raw traffic capture, denoted as T , is first processed by aggregating packets into flows based on the canonical representation:

$$
\mathcal {T} = \{F _ {1}, F _ {2}, \dots , F _ {K} \}. \tag {1}
$$

![](images/e66383dd0ad0e1c75a288725ef277d146db57fb3504017ddcba22fcc389f97d4.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Raw Traffic<br>10110101<br>Pcap File"] --> B["Flows"]
    B --> C["Packet Splitting"]
    C --> D["..."]
    D --> E["Packets"]
    E --> F["Fixed Packets"]
    F --> G["Strides"]
    G --> H["Stride Cutting"]
    
    subgraph "Flow Splitting"
        B
        C
        D
        E
        F
    end
    
    subgraph "Packet Cropping & Padding"
        C
        E
        F
        G
    end
    
    style A fill:#333,stroke:#fff,color:#fff
    style B fill:#999,stroke:#fff,color:#fff
    style C fill:#ff9,stroke:#fff,color:#fff
    style D fill:#ff9,stroke:#fff,color:#fff
    style E fill:#ff9,stroke:#fff,color:#fff
    style F fill:#ff9,stroke:#fff,color:#fff
    style G fill:#ff9,stroke:#fff,color:#fff
    style H fill:#ff9,stroke:#fff,color:#fff
```
</details>

Fig. 3: End-to-end preprocessing pipeline for encrypted traffic. Raw traffic is first segmented into flows using canonical 5- tuple session identification. These flows are further decomposed into packet-level units through packets splitting. Each packet undergoes byte-level cropping and zero-padding to produce fixed-dimensional header and payload segments. The resulting sequence of fixed packets is then partitioned into nonoverlapping strides, enabling consistent, length-normalized inputs for subsequent neural processing while preserving temporal ordering and structural heterogeneity.

where each flow $F _ { k }$ represents an ordered sequence of packets exchanged between a unique pair of endpoints. This splitting preserves session-level temporal dependencies essential for downstream sequence modeling.

Stage 2: Packet Splitting. Each packet $P _ { i }$ within a flow is decomposed into its constituent components: $P _ { i } = ( H _ { i } , B _ { i } )$ , where $H _ { i }$ denotes the header bytes containing protocol metadata and control information, and $B _ { i }$ represents the payload bytes carrying application data. Non-IP packets (e.g., ARP, DHCP) are removed to maintain semantic consistency, and link-layer headers are stripped to eliminate hardwaredependent artifacts and retain protocol-level information.

Stage 3: Packet Cropping & Padding. To produce fixedsize tensor inputs suitable for neural network processing, we constrain each flow to its first M packets. Let $H _ { i } \ =$ $( h _ { i , 1 } , h _ { i , 2 } , \ldots )$ and $B _ { i } ~ = ~ ( b _ { i , 1 } , b _ { i , 2 } , . . . )$ denote the raw byte sequences of the i-th header and payload, respectively. We construct fixed-length feature vectors $\tilde { H } _ { i } ~ \in ~ \mathbb { R } ^ { N _ { h } }$ and $\tilde { B } _ { i } \in \mathbb { R } ^ { N _ { p } }$ by retaining the initial bytes:

$$
\tilde {H} _ {i} = [ h _ {i, 1}, \dots , h _ {i, N _ {h}} ], \quad \tilde {B} _ {i} = [ b _ {i, 1}, \dots , b _ {i, N _ {p}} ]. \tag {2}
$$

To ensure uniformity, zero-padding is applied where the sequence length falls short of the threshold, i.e., $h _ { i , k } = 0$ if $k > | H _ { i } |$ , and similarly for $B _ { i } .$ . Finally, the processed header– payload segments are concatenated in temporal order to form a structured byte sequence:

$$
\mathbf {b} = [ \tilde {H} _ {1}, \tilde {B} _ {1}, \dots , \tilde {H} _ {M}, \tilde {B} _ {M} ], \tag {3}
$$

where its total length $L _ { b } = M ( N _ { h } + N _ { p } )$ .

Stage 4: Stride Cutting. Instead of flattening b into a single long tensor that would impose artificial adjacency between unrelated byte regions, we segment the byte stream into fixedlength strides of size $L _ { s }$ :

$$
\mathbf {s} _ {i} = [ b _ {i L _ {s}}, \dots , b _ {(i + 1) L _ {s} - 1} ], \quad 0 \leq i <   N _ {s}, \tag {4}
$$

where $N _ { s } = L _ { b } / L _ { s }$ . This stride-based segmentation preserves temporal ordering and local contextual structures while normalizing the sequence length for efficient batch training. It further maintains structural separability, enabling header- and payload-specific processing pipelines to operate with their respective modality-aware inductive biases.

# C. Heterogeneous MoE Branches

Encrypted network traffic exhibits intrinsic modality heterogeneity: headers are short, structured, and semantically interpretable, while payloads are long, noisy, and highly variable. Optimizing a single shared encoder for both modalities often leads to biased representation, as the statistical and semantic properties of headers and payloads are fundamentally different. To explicitly account for this heterogeneity, TrafficMoE introduces two dedicated Mixture-of-Experts (MoE) branches—one for headers and another one for payloads. Each branch employs an identical architectural backbone but maintains independent expert sets and gating mechanisms, allowing experts to learn modality-specific distributions. This design leverages the core advantage of MoE: conditional expert activation enables flexible and context-aware modeling of distinct statistical regimes without requiring divergent architectures for each modality.

General MoE Formulation. Each branch adopts a sparse Mixture-of-Experts formulation consisting of a content-aware gating module and an expert pool. Given an input sequence $\bar { \boldsymbol { X } } \in \mathbf { \bar { \mathbb { R } } } ^ { L \times D }$ , the gating network first produces routing logits:

$$
G = \operatorname{Gate} (X) = X W _ {g} + b _ {g} \in \mathbb {R} ^ {L \times E}, \tag {5}
$$

where $W _ { g } \in \mathbb { R } ^ { D \times E }$ and $b _ { g } \in \mathbb { R } ^ { L \times E }$ are learnable parameters. Each row $G _ { \ell }$ represents routing logits that measure the affinity between token $x _ { \ell }$ and each expert.

For each token, only the Top-K experts with the highest routing scores are selected. Formally, let $\tau ( x _ { \ell } )$ denote the index set of the Top-K experts for token xℓ:

$$
\mathcal {T} (x _ {\ell}) = \mathrm{TopK} (G _ {\ell}, K), \tag {6}
$$

where TopK(·) means a top K selection function. The routing weights are then normalized over the selected experts as:

$$
R _ {\ell , i} = \left\{ \begin{array}{l l} \frac {\exp (G _ {\ell , i})}{\sum_ {j \in \mathcal {T} (x _ {\ell})} \exp (G _ {\ell , j})}, & i \in \mathcal {T} (x _ {\ell}), \\ 0, & \text { otherwise }. \end{array} \right. \tag {7}
$$

Each expert produces a transformation output:

$$
F _ {i} = \text { Expert } _ {i} (X), \quad i = 1, \dots , E, \tag {8}
$$

Then, the final MoE output is computed as a sparsely weighted aggregation:

$$
F _ {\ell} = \sum_ {i \in \mathcal {T} (x _ {\ell})} R _ {\ell , i} \cdot F _ {\ell , i}. \tag {9}
$$

Header Branch with Sequence Modeling and Top-K Sparse MoE. Following the above MoE formulation, given structured header tokens $\boldsymbol { X } _ { h } \in \mathbb { R } ^ { L _ { h } \times D }$ that encode stable and protocol-aligned semantics, we first apply a modality-specific sequence modeling block to capture contextual dependencies:

$$
Z _ {h} = \text { SeqBlock } _ {h} (X _ {h}), \tag {10}
$$

where $\mathrm { S e q B l o c k } _ { h } ( \cdot )$ can be instantiated as multi-head selfattention or a state-space model (e.g., Mamba). This block enriches each header token with long-range contextual information while preserving structured protocol semantics.

The contextualized representations $Z _ { h }$ are then routed through a header-specific sparse MoE module. The gating network produces routing logits as:

$$
G _ {h} = \operatorname{Gate} _ {h} (Z _ {h}) \in \mathbb {R} ^ {L _ {h} \times E}. \tag {11}
$$

For each token $z _ { h , \ell } ,$ only the Top-K experts with the highest routing scores are selected:

$$
\mathcal {T} _ {h} (z _ {h, \ell}) = \mathrm{TopK} (G _ {h, \ell}, K), \tag {12}
$$

Then, the routing weights are normalized over the selected experts, formulated as:

$$
R _ {h, \ell , i} = \left\{ \begin{array}{l l} \frac {\exp (G _ {h , \ell , i})}{\sum_ {j \in \mathcal {T} _ {h} (z _ {h , \ell})} \exp (G _ {h , \ell , j})}, & i \in \mathcal {T} _ {h} (z _ {h, \ell}) \\ 0, & \text { otherwise. } \end{array} \right. \tag {13}
$$

Each header expert produces a transformation output:

$$
F _ {i} ^ {(h)} = \text { Expert } _ {i} ^ {(h)} (Z _ {h}), \quad i = 1, \dots , E, \tag {14}
$$

Then, the final header representation is obtained via a sparse aggregation, shown as:

$$
F _ {h, \ell} = \sum_ {i \in \mathcal {T} _ {h} (z _ {h, \ell})} R _ {h, \ell , i} \cdot F _ {\ell , i} ^ {(h)}. \tag {15}
$$

Essentially, each header expert models distinct protocolrelated patterns, such as field interactions, control flags, protocol identifiers, etc. By performing Top-K sparse routing over contextualized features, the header branch encourages structured and semantics-aware expert specialization while maintaining computational efficiency.

Payload Branch with Sequence Modeling and Top-K Sparse MoE. Payload tokens $\boldsymbol { X } _ { p } ~ \in ~ \mathbb { R } ^ { L _ { p } \times \tilde { D } }$ exhibit high entropy, weak semantic locality, and substantial distributional variability due to encryption. Similarly, we first employ a payload-specific sequence modeling block:

$$
Z _ {p} = \text { SeqBlock } _ {p} (X _ {p}), \tag {16}
$$

where $Z _ { p }$ captures long-range statistical dependencies and implicit byte-level correlations within encrypted sequences. The contextualized representations $Z _ { p }$ are then routed through an independent sparse MoE module. The gating network produces routing logits:

$$
G _ {p} = \operatorname{Gate} _ {p} (Z _ {p}) \in \mathbb {R} ^ {L _ {p} \times E}. \tag {17}
$$

For each payload token $z _ { p , \ell } ,$ , the Top-K experts are selected:

$$
\mathcal {T} _ {p} (z _ {p, \ell}) = \mathrm{TopK} (G _ {p, \ell}, K). \tag {18}
$$

Routing weights are normalized over the selected experts:

$$
R _ {p, \ell , i} = \left\{ \begin{array}{l l} \frac {\exp (G _ {p , \ell , i})}{\sum_ {j \in \mathcal {T} _ {p} (z _ {p , \ell})} \exp (G _ {p , \ell , j})}, & i \in \mathcal {T} _ {p} (z _ {p, \ell}) \\ 0, & \text {otherwise.} \end{array} \right. \tag {19}
$$

Each payload expert produces a transformation output:

$$
F _ {i} ^ {(p)} = \text { Expert } _ {i} ^ {(p)} (Z _ {p}), \quad i = 1, \dots , E. \tag {20}
$$

The final payload representation is computed as:

$$
F _ {p, \ell} = \sum_ {i \in \mathcal {T} _ {p} (z _ {p, \ell})} R _ {p, \ell , i} \cdot F _ {\ell , i} ^ {(p)}. \tag {21}
$$

In contrast to the header experts, payload experts tend to capture encrypted textures, statistical regularities, and noiseresilient patterns. The routing behavior in $R _ { p }$ thus reflects distributional similarity rather than explicit semantics. Overall, the sequence modeling blocks and modality-specific MoE modules jointly disentangle contextual dependency modeling from expert specialization. This design enables TrafficMoE to independently encode structured protocol semantics and stochastic encrypted patterns, providing well-conditioned representations $F _ { h }$ and $F _ { p }$ for subsequent computations.

# D. Uncertainty-aware Filtering

Although the heterogeneous MoE branches generate modality-specific representations, encrypted traffic still contains unreliable, indiscriminative and noisy components, particularly within long and noisy payload sequences. Notably, MoE routing primarily encourages expert specialization rather than explicitly assess token reliability. As a result, tokens that exhibit unstable cross-modal interactions may continue to propagate noise to subsequent fusion layers. To address this issue, we introduce an Uncertainty-aware Filter (UF) that estimates token-level uncertainty based on cross-modal interaction between header and payload representations. Instead of relying on internal self-attention responses, UF enables a feature-level similarity computation between two modalities (i.e., headers and payloads), thereby capturing how each token consistently aligns with its cross-modal counterpart. Fig. 4 describes the basic idea of UF for header feature purification (Fig. 4a) and payload feature purification (Fig. 4b). We see that the UF module quantifies this alignment through the cross-modal interaction matrix’s entropy, where low-entropy distributions identify reliable tokens to be retained, while highentropy ones identify noisy components to be suppressed.

Token-wise Uncertainty Estimation. Let $F _ { h , \ell } \in \mathbb { R } ^ { L _ { h } \times d }$ and $F _ { p , \ell } \in \mathbb { R } ^ { L _ { p } \times d }$ denote the header and payload feature matrices, produced by their respective MoE branches. We compute a cross-modal interaction matrix:

$$
A = \text { Softmax } \left(\frac {F _ {h , \ell} F _ {p , \ell} ^ {\top}}{\sqrt {d}}\right), \tag {22}
$$

where $A \in \mathbb { R } ^ { L _ { h } \times L _ { p } }$ measures the alignment strength between header tokens and payload tokens. Each row $A _ { i }$ reflects how header token $h _ { i }$ distributes its interaction over payload tokens.

We hypothesize that reliable tokens exhibit focused interaction patterns, while noisy or weakly informative tokens produce dispersed distributions. Accordingly, we quantify tokenlevel uncertainty via entropy:

$$
H _ {h} (i) = - \sum_ {j = 1} ^ {L _ {p}} A _ {i j} \log \left(A _ {i j} + \epsilon\right), \tag {23}
$$

$$
H _ {p} (j) = - \sum_ {i = 1} ^ {L _ {h}} A _ {i j} \log (A _ {i j} + \epsilon),
$$

![](images/51fdfc53f09edc92c7e5cc7f02552ce51b58fb1d50914ce217c304adb47da652.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input F_h"] --> B["×"]
    C["Input F_p"] --> B
    B --> D["matrix"]
    D --> E["Gate"]
    E --> F["Output"]
    G["Cross-modal interaction matrix"] --> D
    H["High Entropy H Dispersed Noise"] --> I["Gate value g→0"]
    J["Low Entropy H Reliable Token"] --> K["Gate value g→1"]
    L["Alt. Strength"] --> M["Gate"]
    N["Alt. Strength"] --> O["Gate"]
    P["Alt. Strength"] --> Q["Gate"]
    R["F_h"] --> S["Output"]
    T["F_p"] --> S
```
</details>

(a) Header Filtering

![](images/92d2f52229f526cbd8b7c9cf6b78c461c8ad98812afaa4682c56370f399a5e28.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Input Fb"] --> B["Cross-modal interaction matrix"]
    C["Input Fp"] --> B
    B --> D["Gate"]
    D --> E["Output Fpp"]
    F["Low Entropy H Reliable Token"] --> G["Token Index"]
    H["High Entropy H Dispersed Noise"] --> I["Token Index"]
    G --> J["Low Entropy H Reliable Token"]
    I --> K["High Entropy H Dispersed Noise"]
    J --> L["Gate value g→1"]
    K --> M["Gate value g→0"]
```
</details>

(b) Payload Filtering   
Fig. 4: The basic idea of UF, which quantifies the alignment uncertainty via Shannon entropy (H). Sharp distributions in green mean low entropy H and identify reliable metadata to be retained (i.e., the filter $g  1 )$ , while dispersed distributions in red mean high entropy H and identify noisy components to be suppressed (i.e., the filter $g \to 0 )$ .

where ϵ ensures numerical stability and $i \in \{ 1 , \ldots , L _ { h } \}$ means the index of header tokens and $j \in \{ 1 , \ldots , L _ { p } \}$ denotes the index of payload tokens. Clearly, higher entropy indicates ambiguous or inconsistent cross-modal alignment, suggesting lower reliability. In contrast, lower entropy corresponds to a sharp interaction profile, implying stronger structural relevance across modalities. The resulting uncertainty scores are used to softly suppress unreliable tokens through a learnable filtering mechanism before cross-modal fusion.

Filter Weights Computation. To convert the above estimated uncertainty $H _ { h }$ and $H _ { p }$ in Eq. (23) into suppression weights, we introduce a learnable activation function:

$$
\begin{array}{l} g _ {h} ^ {i} = \sigma (w H _ {h} (i) + b), \quad i \in \{1, \dots , L _ {h} \}, \\ i = \left(\text {一} H _ {h} (i) + b\right), \quad i = \{1, \dots , L _ {h} \}. \end{array} \tag {24}
$$

$$
g _ {p} ^ {j} = \sigma (w H _ {p} (j) + b), \quad j \in \{1, \ldots , L _ {p} \},
$$

where $\sigma ( \cdot )$ is the sigmoid function, w and b are learnable weights. For a sequence of tokens, the token-wise activation scores are stacked as weight vector:

$$
\mathbf {g} _ {h} = \left[ g _ {h} ^ {1}, g _ {h} ^ {2}, \dots , g _ {h} ^ {L _ {h}} \right] \in \mathbb {R} ^ {L _ {h}}, \tag {25}
$$

$$
\mathbf {g} _ {p} = [ g _ {p} ^ {1}, g _ {p} ^ {2}, \ldots , g _ {p} ^ {L _ {p}} ] \in \mathbb {R} ^ {L _ {p}},
$$

The above computations enable the model to learn a soft thresholding behavior: larger entropy values are mapped to smaller scores, while tokens with low entropy are retained with higher weights. During training, the function learns to correlate high uncertainty with negative gradients from the classifier, gradually shaping w to enforce stronger suppression on noisy patterns. Thus, the activation score acts as a continuous reliability indicator that dynamically adjusts token contribution on a per-sample and per-token basis, rather than relying on a fixed global filtering rule.

Feature Purification. The gating weights in Eq. (25) are then multiplied element-wise to the MoE outputs of each branch. Denote header features by $F _ { h }$ and payload features by $F _ { p } .$ , the purified feature representations are computed as:

$$
\begin{array}{l} F _ {p h} = \mathbf {g} _ {h} \odot F _ {h}, \\ F _ {p h} = \mathbf {g} _ {h} \odot F _ {h}. \end{array} \tag {26}
$$

$$
F _ {p p} = \mathbf {g} _ {p} \odot F _ {p}.
$$

where ${ \bf g } _ { h } ~ \in ~ \mathbb { R } ^ { L _ { h } }$ and ${ \bf g } _ { p } ^ { \mathrm { ~ ~ } } \in \mathrm { ~ \mathbb { R } ^ { \it L _ { p } } ~ }$ represent the tokenlevel gating vectors for header and payload, respectively. This multiplicative modulation selectively suppresses noisy or unreliable activations while preserving structurally discriminative information. Crucially, the gating is performed at the token level rather than the sequence level, allowing the model to handle fine-grained intra-flow variability common in encrypted traffic. The purified representations $F _ { p h }$ and $F _ { p p }$ are then fed into the subsequent modules for computation.

# E. Implicit Conditional Aggregation

To enable context-aware multi-modal integration while avoiding the rigidity of static fusion schemes, we propose an implicit Conditional Aggregation (CA) mechanism that adaptively modulates cross-modal interactions based on samplespecific traffic characteristics. Instead of introducing an explicit gating network, CA leverages the expert assignment probabilities produced by the MoE routers in the header and payload branches as implicit conditional signals. These probabilities encode internal estimates of feature sparsity, modality saliency and structural heterogeneity, and thus serve as lightweight yet informative context descriptors without additional supervision.

Context Encoding via Router Probabilities. Let $\mathbf { r } _ { h } \in \mathbb { R } ^ { E }$ and $\mathbf { r } _ { p } \in \mathbb { R } ^ { E }$ denote the soft expert-selection distributions from the header and payload MoE routers, respectively. We first project them into a shared conditional space:

$$
\mathbf {c} _ {h} = W _ {h} \mathbf {r} _ {h}, \quad \mathbf {c} _ {p} = W _ {p} \mathbf {r} _ {p}, \tag {27}
$$

where $W _ { h }$ and $W _ { p }$ are learnable linear transformations. The resulting vectors are concatenated and normalized to form a unified conditional descriptor:

$$
\mathbf {c} = \text { Norm } ([ \mathbf {c} _ {h}; \mathbf {c} _ {p} ]), \tag {28}
$$

Physically, this descriptor jointly captures intra-modal complexity and inter-modal complementarity.

Context-Modulated Feature Aggregation. Given the intermediate representations $F _ { p h }$ and $F _ { p p }$ from the header and payload branches, in order to ensure stable relative scaling between modalities while preserving their distinct representational subspaces, we propose the conditional aggregation and modulation followed by feature concatenation:

$$
\mathbf {F} _ {\mathrm{agg}} = \Big [ \alpha (\mathbf {c}) \odot \phi (F _ {p h})  ;   (1 - \alpha (\mathbf {c})) \odot \psi (F _ {p p}) \Big ]. \tag {29}
$$

where $\phi ( \cdot )$ and $\psi ( \cdot )$ denote modality-specific transformations, and $\alpha ( \cdot )$ is tractable conditioned on the descriptor c with softmax activation, $\phi ( \cdot )$ and $\psi ( \cdot )$ denote modality-specific linear projections that transform the header and payload representations into a unified feature space computed by:

$$
\alpha (\mathbf {c}) = \operatorname{Softmax} \left(\mathbf {W} _ {c} \mathbf {c} + \mathbf {b} _ {c}\right),
$$

$$
\phi (F _ {p h}) = F _ {p h} W _ {h}, \tag {30}
$$

$$
\psi (F _ {p p}) = F _ {p p} W _ {p}.
$$

where $\mathbf { W } _ { c }$ and ${ \bf b } _ { c }$ are learnable parameters that generate modality-aware weighting coefficients, while $W _ { h }$ and $W _ { p }$ denote learnable projection matrices for the header and payload representations, respectively.

Adaptive Behavior and Advantages. Unlike the intuitive weighted summation, this formulation explicitly retains modality-specific information, while allowing their contributions to be adaptively modulated based on traffic-specific context. The proposed CA mechanism introduces an implicit condition, whereby fusion behavior is dynamically adapted using internal routing signals without additional gating supervision. By exploiting router probabilities that encode uncertainty, modality reliability and expert specialization patterns, CA achieves minimal parameter overhead, semantic consistency between expert routing and fusion, and improved robustness to heterogeneous and previously unseen encrypted traffic. Empirically, this design yields more expressive and stable representations than static fusion or fixed-weight fusion, particularly under modality-imbalanced conditions.

![](images/8ab3011c850fd375ee85dfc8a95ed282857890993373610531c6da0d577d9856.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Reconstructed Strides"] --> B["Decoder"]
    B --> C["Head MoE Branch"]
    B --> D["Payload MoE Branch"]
    C --> E["Random Masking"]
    D --> F["Position Embedding"]
    D --> G["Stride Embedding"]
    E --> H["0"]
    E --> I["1"]
    E --> J["2"]
    E --> K["3"]
    E --> L["4"]
    E --> M["M-1"]
    E --> N["M"]
    G --> O["..."]
    G --> P["..."]
    G --> Q["..."]
    G --> R["..."]
    G --> S["..."]
    G --> T["..."]
```
</details>

![](images/d1c8c50e7acaf4c9b7374ded8bc4b4b0023a65a15e40956e331d41ad52800221.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["MLP Head"] --> B["Downstream Tasks"]
    B --> C["Forward Class Token"]
    C --> D["TrafficMoE"]
    D --> E["Input Stride Token"]
    E --> F["Position Embedding 0-4"]
    F --> G["Stride Embedding + -"]
    H["Downstream Tasks"] --> I["MLP Head"]
    I --> J["MLP Head *"]
    J --> K["MLP Head *"]
    L["MLP Head *"] --> M["MLP Head *"]
    N["MLP Head *"] --> O["MLP Head *"]
    P["MLP Head *"] --> Q["MLP Head *"]
    R["MLP Head *"] --> S["MLP Head *"]
    T["MLP Head *"] --> U["MLP Head *"]
    V["MLP Head *"] --> W["MLP Head *"]
    X["MLP Head *"] --> Y["MLP Head *"]
    Z["MLP Head *"] --> AA["MLP Head *"]
```
</details>

Fig. 5: Training pipeline of the proposed framework. In the pre-training stage, masked language modeling (MLM) is used to learn contextual representations from header and payload sequences without supervision. In the fine-tuning stage, the pretrained encoders are fine-tuned end-to-end on labeled traffic data through a standard cross-entropy classification objective.

# F. Global MoE Branch

The above CA module aggregates purified header and payload representations into a unified feature space. However, the fused representations may still exhibit substantial variability across traffic patterns. To further enhance crossmodal flexibility while maintaining computational efficiency and structural consistency with modality-specific branches, we introduce a Global Sparse MoE Branch for post-refinement.

Let $F _ { a g g } \in \mathbb { R } ^ { L _ { f } \times \tilde { D } }$ denote the fused feature sequence. A sequence modeling block $\operatorname { S e q B l o c k } _ { g } ( \cdot )$ is first applied to capture contextual dependencies across the unified representation:

$$
Z _ {f} = \text { SeqBlock } _ {g} (F _ {a g g}), \tag {31}
$$

where $\operatorname { S e q B l o c k } _ { g } ( \cdot )$ can be instantiated as a multi-head selfattention module or a state-space model (e.g., Mamba), enabling modeling of long-range token interactions over fused cross-modal features.

Similarly, the contextualized representations $Z _ { f }$ are then processed by a dedicated gating network:

$$
G _ {g} = \operatorname{Gate} _ {g} (Z _ {f}) \in \mathbb {R} ^ {L _ {f} \times E}. \tag {32}
$$

For each token $z _ { f , \ell } ,$ only the Top-K experts with the highest routing scores are selected:

$$
T _ {g} (z _ {f, \ell}) = \mathrm{TopK} (G _ {g, \ell}, K). \tag {33}
$$

Then, the routing weights are normalized over the selected experts:

$$
R _ {g, \ell , i} = \left\{ \begin{array}{l l} \frac {\exp (G _ {g , \ell , i})}{\sum_ {j \in T _ {g} (z _ {f , \ell})} \exp (G _ {g , \ell , j})}, & i \in T _ {g} (z _ {f, \ell}), \\ 0, & \text { otherwise }. \end{array} \right. \tag {34}
$$

Each global expert generates a transformation output of the contextualized features:

$$
F _ {i} ^ {(g)} = \text { Expert } _ {i} ^ {(g)} (Z _ {f}), \quad i = 1, \dots , E. \tag {35}
$$

The final representation is computed via sparse aggregation:

$$
F _ {g, \ell} = \sum_ {i \in T _ {g} (z _ {f, \ell})} R _ {g, \ell , i} \cdot F _ {i, \ell} ^ {(g)}. \tag {36}
$$

Unlike the modality-specific branches that operate on structurally disentangled input, the global experts process alreadyfused cross-modal representations. By performing Top-K sparse routing at this stage, the Global MoE Branch preserves conditional computation consistency across the entire architecture, while enabling high-level expert specialization over unified traffic semantics. This post-refinement further reinforces cross-modal features according to traffic-specific patterns and can be seamlessly exploited in both pre-training and fine-tuning stages.

# G. Training Pipeline of TrafficMoE

The overall training pipeline of TrafficMoE is illustrated in Fig. 5. The framework follows a two-stage optimization strategy consisting of self-supervised pretraining and supervised fine-tuning. In the pretraining stage, modality-specific encoders and MoE routing are initialized through masked language modeling (MLM) on unlabeled traffic flows. Subsequently, the entire architecture—including the MoE branches, UF module, and CA controller—is fine-tuned end-to-end on labeled encrypted traffic data.

Pre-training Stage. To initialize modality-specific encoders and stabilize the heterogeneous MoE routing, we adopt a masked language modeling (MLM) objective tailored to encrypted traffic. Given a flow sample composed of a header token sequence $X _ { h } = \{ x _ { h , i } | i = 1 , \cdot \cdot \cdot , L _ { h } \}$ and a payload token sequence $X _ { p } = \{ x _ { p , i } | i = 1 , \cdot \cdot \cdot , L _ { p } \}$ , we apply random masking to a portion of tokens within each sequence. Let $\tilde { X } _ { h }$ and ${ \tilde { X } } _ { p }$ denote the masked sequences. Following the standard MLM formulation, the objective is to recover masked tokens based on their contextual dependencies. The loss of MLM for each branch is defined as:

$$
\mathcal {L} _ {M L M} ^ {(h)} = - \sum_ {i \in \mathcal {M} _ {h}} \log P (x _ {h, i} \mid \tilde {X} _ {h}), \tag {37}
$$

$$
\mathcal {L} _ {M L M} ^ {(p)} = - \sum_ {i \in \mathcal {M} _ {p}} \log P (x _ {p, i} \mid \tilde {X} _ {p}). \tag {38}
$$

where $\mathcal { M } _ { h }$ and $\mathcal { M } _ { p }$ represent the masked token indices for header and payload. The total pretraining loss is:

$$
\mathcal {L} _ {p r e} = \mathcal {L} _ {M L M} ^ {(h)} + \mathcal {L} _ {M L M} ^ {(p)}. \tag {39}
$$

This pretraining strategy enables the header encoder to learn structural and protocol-specific patterns, while the payload encoder captures semantic and byte-level distributions. Moreover, the MoE architecture benefits from pretraining by allowing experts to specialize organically on different flow characteristics before downstream optimization. The UF module is jointly optimized during pretraining so that unreliable tokens receive appropriately low reliability coefficients, effectively regularizing early-stage representation learning.

Fine-tuning Stage. For the downstream encrypted traffic classification task, both pretrained encoders and the CA module are optimized end-to-end. Given purified header features and purified payload features, the fusion controller generates sample-conditioned fusion coefficients that modulate the contributions of the two branches. The fused representation is fed into a classification head parameterized by $\theta _ { c l s }$ .

Let y denote the ground-truth traffic category, then the model outputs class probabilities:

$$
P (y \mid X _ {h}, X _ {p}) = \text { softmax } \left(\theta_ {c l s} ^ {\top} F _ {a g g}\right). \tag {40}
$$

The fine-tuning objective is the standard cross-entropy loss:

$$
\mathcal {L} _ {c l s} = - \log P (y \mid X _ {h}, X _ {p}). \tag {41}
$$

During fine-tuning, all modules—including the MoE branches, UF reliability modulation, and the CA controller—are jointly optimized. This joint optimization allows the model to adapt the structural and semantic priors to the distributions of encrypted traffic categories in the downstream dataset, yielding robust and discriminative representations.

To summarize, the training procedure of TrafficMoE is presented in Algorithm 1.

# IV. EXPERIMENTS

# A. Experimental Setup

Pre-training Datasets. In the self-supervised pre-training stage, we utilize approximately 30 GB of unlabeled raw network traffic collected from three publicly available repositories: ISCX-VPN2016 (NonVPN portion) [27], CICIDS2017

Algorithm 1 Training Procedure of TrafficMoE

Require: Raw unlabeled traffic $\mathcal { T } _ { u }$ and labeled traffic $\tau _ { l }$ with labels Y , the number E of experts, and the parameter K for Top-K routing.

Ensure: Trained TrafficMoE model.

1: Traffic preprocessing: Split raw traffic into flows and convert each flow into header tokens $X _ { h }$ and payload tokens $X _ { p }$ following the pipeline in Sec. III-B.   
2: Stage I: Self-supervised Pre-training   
3: for each unlabeled training flow from $\mathcal { T } _ { u }$ do   
4: Apply random masking to obtain $\tilde { X } _ { h }$ and ${ \tilde { X } } _ { p } ;$   
5: #Disentangling   
6: Encode the header and payload sequences using modality-specific sequence blocks, respectively;   
7: Perform sparse MoE routing for header and payload branches as presented in Sec. III-C;   
8: #Filtering   
9: Estimate token uncertainty via cross-modal interaction using Eq. (22) and Eq. (23);   
10: Compute filter weights using Eq. (24) and Eq. (25);   
11: Obtain purified features using Eq.(26);   
12: #Aggregation   
13: Perform conditional aggregation (CA) using Eq. (27), Eq. (28) and Eq. (29);   
14: Refine the fused representation using Global MoE branch as presented in Sec. III-F;   
15: Update model parameters using MLM objective as formulated in Eq. (39).   
16: end for   
17: Stage II: Supervised Fine-tuning   
18: for each labeled flow sample from $\tau _ { l }$ do   
19: Forward propagate through TrafficMoE to obtain Aggregation feature $F _ { a g g } ;$   
20: Optimize the classification objective in Eq. (41).   
21: end for   
22: return Fine-tuned TrafficMoE model parameters.

(Monday subset) [28], and the WIDE backbone trace [29]. These datasets jointly provide large-scale, diverse, and naturally distributed encrypted traffic, covering a wide range of real-world scenarios. To construct the training corpus, we extract the first 64 consecutive bytes from the Network layer of each packet, ensuring that the model captures essential structured information from the IP layer and those without relying on task-specific annotations. The three sources contribute complementary traffic characteristics.

Specifically, ISCX-VPN2016 (NonVPN) offers applicationlevel diversity under controlled conditions. CICIDS2017 (Monday) provides clean benign traffic generated in an enterprise-like environment without attacks. The WIDE backbone trace introduces large-volume, naturally occurred Internet backbone flows with substantial protocol and routing variability. The combination of structured laboratory traces and unstructured backbone traffic enhances the robustness and generalization of the pre-trained model across heterogeneous network environments.

Fine-tuning Datasets. For supervised fine-tuning and evaluation, we employ six widely used encrypted traffic datasets: CSTNET-TLS 1.3 [10], ISCX-Tor2016 [30], CIC-IoT2022 [31], USTC-TFC2016 [32], and ISCX-VPN2016 [27] composed of two sub-datasets: ISCX-VPN(APP) and ISCX-VPN(Service). All flows are segmented into packets, and each packet is processed by extracting the first 64 bytes from the network-layer payload, ensuring consistent input format and preserving both protocol headers and encrypted payloads. Detailed statistical information for these datasets is summarized in Table I.

<table><tr><td>Dataset</td><td># Sample</td><td># Category</td></tr><tr><td>CSTNET-TLS 1.3</td><td>46,356</td><td>120</td></tr><tr><td>ISCX-Tor2016</td><td>14,569</td><td>16</td></tr><tr><td>CIC-IoT2022</td><td>22,634</td><td>6</td></tr><tr><td>USTC-TFC2016</td><td>50,677</td><td>20</td></tr><tr><td>ISCX-VPN (APP)</td><td>2,329</td><td>12</td></tr><tr><td>ISCX-VPN (Service)</td><td>3,694</td><td>17</td></tr></table>

TABLE I: Statistical Information of Fine-tuning Datasets

Specifically, CSTNET-TLS 1.3 contains large-scale TLS 1.3 encrypted traffic, representing contemporary application-layer encryption traffic. ISCX-Tor2016 consists of flows routed through the Tor anonymity network, exhibiting heavily obfuscated communication patterns. CIC-IoT2022 captures traffic from diverse IoT devices under both benign and malicious scenarios. USTC-TFC2016 includes balanced benign and malware flows with highly similar encrypted signatures, allowing for fine-grained classification evaluation. The ISCX-VPN (APP) subset aggregates traffic at the application level regardless of service type, while the ISCX-VPN (Service) subset focuses on service-level classification (e.g., Skype text, file transfer, and voice). These six datasets jointly provide a comprehensive benchmark spanning modern encrypted applications, anonymized routing, IoT ecosystems, malware flows, and VPN-obfuscated traffic.

During the fine-tuning stage, each traffic flow is represented by its first five packets, from which 64 bytes are extracted starting at the network layer for each packet. To protect sensitive information and reduce potential dataset-specific biases, the IP addresses and port numbers are randomized, and the TCP timestamp fields are normalized accordingly. Note that, all datasets are constructed from disjoint traffic sources to strictly prevent any form of data leakage.

Evaluation Metrics. We evaluate the classification performance using four standard metrics, including Accuracy (AC), Precision (PR), Recall (RC), and the weighted F1-score (F1). Accuracy measures the overall proportion of correctly classified samples, while Precision and Recall quantify the reliability and completeness of class predictions, respectively. The weighted F1-score accounts for class imbalance by computing the harmonic mean of Precision and Recall, providing a comprehensive assessment across all traffic categories.

Comparison Methods. To comprehensively evaluate the effectiveness of our TrafficMoE framework, we compare against a broad range of representative approaches spanning three main methodological categories.

1) Machine learning-based methods. This category includes AppScanner [33]), BIND [34], and CUMUL [35]. These approaches rely on handcrafted statistical or flow-level features, followed by traditional classifiers such as SVMs, random forests, or k-NN models. Thus, the performance highly depends on feature engineering and they typically struggle to generalize across heterogeneous or encrypted traffic patterns.

2) Deep learning-based methods. We further include several deep neural network models including DF [36], FSNet [13], GraphDapp [37], and Beauty [38], that directly operate on raw packet sequences or intermediate flow representations. These methods leverage CNNs, RNNs, or graph neural network architectures to automatically extract hierarchical traffic features. While more robust than conventional machine learning models, they remain limited by the scale and diversity of supervised training data and often lack the ability to generalize to unseen or novel traffic data or categories.

3) Pretraining-based methods. Finally, we compare against state-of-the-art pretraining approaches, including ET-BERT [10], YaTC [39]), TrafficFormer [11], and FlowletFormer [40]. These frameworks firstly perform pre-training to learn universal traffic semantics in a self-supervised or weaklysupervised manner on large-scale unlabeled corpora, and are subsequently fine-tuned on specific downstream traffic classification datasets. To ensure fair comparisons among different methods, all pretraining-based baselines share the same pretraining datasets and fine-tuning datasets.

# B. Comparison with State-of-the-Art Methods

The results with detailed comparisons to baselines and stateof-the-art methods are summarized in Tables II and III.

As shown in Table II, we have the following observations.

1) ISCX-Tor2016. On this dataset, TrafficMoE achieves a substantial performance improvement over all competing methods, reaching 97.65% for both accuracy and F1-score. In contrast, traditional machine learning-based approaches such as AppScanner, BIND, and CUMUL exhibit limited discriminative capability due to their reliance on handcrafted features. Deep learning-based models, including DF and FSNet, further struggle to capture the complex traffic patterns induced by Tor obfuscation. While pretraining-based methods such as FlowletFormer demonstrate strong performance, TrafficMoE still delivers a clear margin of improvement, highlighting the effectiveness of heterogeneity-aware expert routing architecture under highly anonymized traffic conditions.   
2) CSTNET-TLS. For this dataset that contains diverse TLS-encrypted application traffic, TrafficMoE consistently outperforms all baselines with an F1-score of 86.85%. Compared with feature-based and supervised deep models that suffer from protocol and application variability, Traffic-MoE exhibits superior robustness. Comparing against strong pretraining-based baselines such as ET-BERT, YaTC, and FlowletFormer, our method yields noticeable gains, indicating that explicitly modeling the heterogeneous traffic components for headers and payloads respectively via disentangling is critical for TLS traffic understanding.   
3) CIC-IoT2022. On this large-scale and highly imbalanced IoT traffic dataset, TrafficMoE attains the best overall perfor-

<table><tr><td>Dataset</td><td colspan="4">ISCX-Tor2016</td><td colspan="4">CSTNET-TLS</td><td colspan="4">CIC-IoT2022</td></tr><tr><td>Metric</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td></tr><tr><td>AppScanner [33]</td><td>0.9075</td><td>0.7728</td><td>0.8033</td><td>0.7848</td><td>0.7441</td><td>0.7232</td><td>0.6963</td><td>0.7023</td><td>0.8591</td><td>0.8858</td><td>0.7996</td><td>0.8288</td></tr><tr><td>BIND [34]</td><td>0.9010</td><td>0.8582</td><td>0.8354</td><td>0.8439</td><td>0.4710</td><td>0.4315</td><td>0.4226</td><td>0.4189</td><td>0.7349</td><td>0.6754</td><td>0.6387</td><td>0.6435</td></tr><tr><td>CUMUL [35]</td><td>0.7725</td><td>0.6463</td><td>0.6443</td><td>0.6401</td><td>0.5921</td><td>0.5528</td><td>0.5604</td><td>0.5493</td><td>0.7019</td><td>0.6746</td><td>0.7029</td><td>0.6687</td></tr><tr><td>DF [36]</td><td>0.7401</td><td>0.5918</td><td>0.5611</td><td>0.5492</td><td>0.5729</td><td>0.5398</td><td>0.5144</td><td>0.4933</td><td>0.2746</td><td>0.2140</td><td>0.1870</td><td>0.1647</td></tr><tr><td>FSNet [13]</td><td>0.6967</td><td>0.6159</td><td>0.6061</td><td>0.6028</td><td>0.7814</td><td>0.7670</td><td>0.7316</td><td>0.7311</td><td>0.8077</td><td>0.8250</td><td>0.8333</td><td>0.7804</td></tr><tr><td>GraphDApp [37]</td><td>0.7949</td><td>0.6391</td><td>0.6410</td><td>0.6383</td><td>0.7281</td><td>0.6964</td><td>0.6909</td><td>0.6890</td><td>0.7370</td><td>0.6721</td><td>0.7006</td><td>0.6767</td></tr><tr><td>Beauty [38]</td><td>0.3746</td><td>0.2691</td><td>0.2767</td><td>0.2251</td><td>0.2944</td><td>0.3219</td><td>0.2513</td><td>0.2324</td><td>0.1356</td><td>0.0349</td><td>0.0764</td><td>0.0296</td></tr><tr><td>ET-BERT [10]</td><td>0.8123</td><td>0.7249</td><td>0.8276</td><td>0.7453</td><td>0.7993</td><td>0.7832</td><td>0.7689</td><td>0.7700</td><td>0.8603</td><td>0.8297</td><td>0.8255</td><td>0.8244</td></tr><tr><td>YaTC [39]</td><td>0.9175</td><td>0.7725</td><td>0.7333</td><td>0.7405</td><td>0.8391</td><td>0.8364</td><td>0.8101</td><td>0.8140</td><td>0.8448</td><td>0.8656</td><td>0.8074</td><td>0.8048</td></tr><tr><td>TrafficFormer [11]</td><td>0.8669</td><td>0.7545</td><td>0.7460</td><td>0.7472</td><td>0.7982</td><td>0.7883</td><td>0.7736</td><td>0.7704</td><td>0.8725</td><td>0.8487</td><td>0.8343</td><td>0.8288</td></tr><tr><td>FlowletFormer [40]</td><td>0.9215</td><td>0.9263</td><td>0.9043</td><td>0.9116</td><td>0.8605</td><td>0.8578</td><td>0.8445</td><td>0.8473</td><td>0.9109</td><td>0.8905</td><td>0.8866</td><td>0.8859</td></tr><tr><td>TrafficMoE</td><td>0.9765</td><td>0.9768</td><td>0.9765</td><td>0.9765</td><td>0.8688</td><td>0.8711</td><td>0.8688</td><td>0.8685</td><td>0.9270</td><td>0.9265</td><td>0.9270</td><td>0.9265</td></tr></table>

TABLE II: Comparison results on ISCX-Tor2016, CSTNET-TLS, and CIC-IoT2022 datasets. 

<table><tr><td>Dataset</td><td colspan="4">USTC-TFC</td><td colspan="4">ISCX-VPN (APP)</td><td colspan="4">ISCX-VPN (Service)</td></tr><tr><td>Metric</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td></tr><tr><td>AppScanner [33]</td><td>0.8585</td><td>0.9108</td><td>0.9034</td><td>0.8976</td><td>0.7945</td><td>0.6950</td><td>0.6975</td><td>0.6874</td><td>0.8681</td><td>0.8710</td><td>0.8435</td><td>0.8546</td></tr><tr><td>BIND [34]</td><td>0.7945</td><td>0.7811</td><td>0.7061</td><td>0.7115</td><td>0.6951</td><td>0.6266</td><td>0.5415</td><td>0.5609</td><td>0.8345</td><td>0.7769</td><td>0.7714</td><td>0.7699</td></tr><tr><td>CUMUL [35]</td><td>0.7173</td><td>0.5063</td><td>0.5812</td><td>0.5183</td><td>0.5480</td><td>0.4839</td><td>0.4615</td><td>0.4554</td><td>0.7099</td><td>0.6959</td><td>0.6893</td><td>0.6884</td></tr><tr><td>DF [36]</td><td>0.6452</td><td>0.4019</td><td>0.3685</td><td>0.3059</td><td>0.4935</td><td>0.2449</td><td>0.2592</td><td>0.2289</td><td>0.5018</td><td>0.4664</td><td>0.4773</td><td>0.3934</td></tr><tr><td>FSNet [13]</td><td>0.7558</td><td>0.8167</td><td>0.8407</td><td>0.8042</td><td>0.6316</td><td>0.4899</td><td>0.4833</td><td>0.4677</td><td>0.9087</td><td>0.9051</td><td>0.9054</td><td>0.9051</td></tr><tr><td>GraphDApp [37]</td><td>0.8750</td><td>0.8446</td><td>0.8501</td><td>0.8249</td><td>0.5703</td><td>0.5108</td><td>0.4872</td><td>0.4853</td><td>0.7500</td><td>0.7311</td><td>0.7678</td><td>0.7429</td></tr><tr><td>Beauty [38]</td><td>0.6682</td><td>0.4448</td><td>0.4369</td><td>0.3796</td><td>0.6169</td><td>0.3333</td><td>0.3139</td><td>0.2964</td><td>0.6416</td><td>0.5769</td><td>0.5842</td><td>0.5387</td></tr><tr><td>ET-BERT [10]</td><td>0.9663</td><td>0.9711</td><td>0.9663</td><td>0.9666</td><td>0.7964</td><td>0.7332</td><td>0.7013</td><td>0.7066</td><td>0.8467</td><td>0.8496</td><td>0.8651</td><td>0.8393</td></tr><tr><td>YaTC [39]</td><td>0.9712</td><td>0.9732</td><td>0.9712</td><td>0.9707</td><td>0.8214</td><td>0.7443</td><td>0.7265</td><td>0.7254</td><td>0.9010</td><td>0.8877</td><td>0.8800</td><td>0.8821</td></tr><tr><td>TrafficFormer [11]</td><td>0.9750</td><td>0.9789</td><td>0.9750</td><td>0.9746</td><td>0.7751</td><td>0.7488</td><td>0.6846</td><td>0.6962</td><td>0.8533</td><td>0.8445</td><td>0.8348</td><td>0.8279</td></tr><tr><td>FlowletFormer [40]</td><td>0.9650</td><td>0.9689</td><td>0.9650</td><td>0.9648</td><td>0.8480</td><td>0.8153</td><td>0.7641</td><td>0.7712</td><td>0.9400</td><td>0.9471</td><td>0.9277</td><td>0.9364</td></tr><tr><td>TrafficMoE</td><td>0.9788</td><td>0.9788</td><td>0.9788</td><td>0.9788</td><td>0.8872</td><td>0.8874</td><td>0.8872</td><td>0.8871</td><td>0.9255</td><td>0.9261</td><td>0.9255</td><td>0.9261</td></tr></table>

TABLE III: Comparison results on USTC-TFC, ISCX-VPN (APP), and ISCX-VPN (Service) datasets.

mance with an F1-score of 92.65%. The classical deep models, such as DF, experience severe performance degradation due to their limited capacity to handle diverse IoT behaviors. In contrast, TrafficMoE effectively leverages expert specialization to disentangle heterogeneous IoT traffic patterns, resulting in significant improvements over both supervised and pretrainingbased baselines.

As shown in Table III, we have the following observations.

1) USTC-TFC. This dataset poses a challenging finegrained traffic classification problem with subtle inter-class differences. TrafficMoE achieves an F1-score of 97.88%, outperforming those strong pretraining-based models such as TrafficFormer and FlowletFormer. This demonstrates the superiority of MoE in processing such data, and that uncertaintyaware filtering and conditional aggregation can effectively suppress noisy payload segments and enhance discriminability in fine-grained encrypted traffic scenarios.   
2) ISCX-VPN (APP). On this dataset that focuses on application-level VPN traffic classification, TrafficMoE achieves the highest F1-score of 88.71%. While pretrainingbased approaches already outperform traditional and supervised deep models, the performance is still constrained by

modality noise in VPN tunneling. TrafficMoE mitigates this issue by dynamically allocating experts and adaptively weighing the contributions of different modalities (i.e., header vs. payload), bringing consistent gains for all evaluation metrics.

3) ISCX-VPN (Service). For this dataset that emphasizes service-level semantics under VPN encryption, FlowletFormer achieves the state-of-the-art performance. Nevertheless, TrafficMoE remains highly competitive, achieving an F1-score of 92.61%, which is comparable to FlowletFormer. This observation suggests that while service-level traffic may benefit from fine-grained temporal modeling, TrafficMoE still provides robust and stable performance by jointly exploiting heterogeneous representations and uncertainty-aware filtering.

# C. Ablation Studies

We conduct a widespread ablation experiments for Traffic-MoE by covering heterogeneous MoE structure, key components, and expert number.

Ablation on Heterogeneous MoE Structure. We first investigate the impact of heterogeneous modeling in TrafficMoE by comparing with homogeneous and single-modality variants. The results are reported in Table IV.

![](images/82579cf290844af5db702f16e1a5cc985b24e5f677305a3303043da6e807900a.jpg)

<details>
<summary>line</summary>

| Expert Number | CSTNET | ISCX-Tor |
| ------------- | ------ | -------- |
| 5             | 84.8   | 95.8     |
| 10            | 86.2   | 97.0     |
| 20            | 87.0   | 97.8     |
| 30            | 87.0   | 97.8     |
</details>

(a) Header MoE

![](images/62d35f23ecca6182094662d7221d38d2b2474fe3aea07c06edf46fa4901f578a.jpg)

<details>
<summary>line</summary>

| Expert Number | CSTNET | ISCX-Tor |
| ------------- | ------ | -------- |
| 5             | 84.2   | 95.2     |
| 10            | 86.0   | 96.8     |
| 20            | 87.0   | 97.8     |
| 30            | 87.0   | 97.8     |
</details>

(b) Payload MoE

![](images/039e0a1570763a95b3916194fb738f206b778dcf15a8d0584121ae4915a690ad.jpg)

<details>
<summary>line</summary>

| Expert Number | CSTNET | ISCX-Tor |
| ------------- | ------ | -------- |
| 5             | 85.0   | 95.5     |
| 10            | 86.0   | 97.0     |
| 20            | 87.0   | 97.5     |
| 30            | 87.0   | 97.5     |
</details>

(c) Global MoE   
Fig. 6: Impact of the expert number in MoE for Header branch, Payload branch and the Global module, respectively, on ISCX-Tor2016 and CSTNET-TLS datasets. Clearly, MoE further improves representations.

TABLE IV: Ablation on Heterogeneous MoE Structure. 

<table><tr><td>Method</td><td>Accuracy (%)</td><td>F1 (%)</td></tr><tr><td>Heterogeneous MoE (Full)</td><td>97.65</td><td>97.65</td></tr><tr><td>Homogeneous MoE</td><td>92.21</td><td>92.32</td></tr><tr><td>Header-only</td><td>75.65</td><td>75.65</td></tr><tr><td>Payload-only</td><td>45.12</td><td>45.22</td></tr></table>

We observe that the full heterogeneous MoE achieves the highest performance, with 97.64% accuracy and 97.44% F1- score. When the heterogeneous design is replaced by a homogeneous MoE, where all experts share identical structures and process the mixed inputs of headers and payloads, the performance drops by more than 5% on both metrics. This degradation indicates that simply increasing model capacity via multiple experts is insufficient; instead, explicitly assigning experts to structurally distinct traffic components w.r.t. headers and payloads is critical for effective representation learning.

More severe performance degradation is observed in the single-modality settings. The Header-only variant retains partial discriminative capability, reflecting that the protocol headers encode relatively stable structural cues even under encryption. In contrast, the Payload-only variant exhibits a dramatic performance collapse. This result suggests that the raw encrypted payload bytes are dominated by noisy and weakly discriminative patterns when modeled in isolation, making them unsuitable for standalone classification.

These above results demonstrate the performance gains of TrafficMoE stem from its heterogeneous expert design rather than the MoE architecture alone. By decoupling header-level structural information and payload-level encrypted content into dedicated experts, the model is able to better exploit complementary semantics while suppressing modality-specific noise. This heterogeneous formulation is therefore essential for robust encrypted traffic classification.

Ablation on Several Key Components. Table V further investigates the impact of key functional components in TrafficMoE, including uncertainty-aware filter (UF), conditional aggregation (CA), cross-modal interaction module and pretraining. Removing the UF module leads to a noticeable performance drop, indicating that entropy-based token filtering plays an essential role in suppressing redundant or unreliable tokens. Disabling the CA module also degrades performance, suggesting that adaptive modality weighting and feature aggregation is more effective than static fusion strategies. Further, when the cross-modal interaction module is removed, the model still maintains relatively strong performance, but with a consistent degradation compared to the full model. This implies that explicit cross-modal alignment enhances finegrained discrimination, especially under noisy or ambiguous traffic patterns. Finally, a drastic performance collapse is witnessed without pre-training, demonstrating that largescale self-supervised pre-training is indispensable for learning transferable encrypted traffic representations.

TABLE V: Ablation study of the TrafficMoE. Accuracy and F1-score are reported under different filtering configurations. 

<table><tr><td>Method</td><td>Accuracy (%)</td><td>F1 (%)</td></tr><tr><td>TrafficMoE</td><td>97.65</td><td>97.65</td></tr><tr><td>w/o UF</td><td>95.69</td><td>95.69</td></tr><tr><td>w/o CA</td><td>96.33</td><td>96.33</td></tr><tr><td>w/o Cross-Modal Interaction</td><td>96.87</td><td>96.87</td></tr><tr><td>w/o Pre-training</td><td>73.25</td><td>73.25</td></tr></table>

Overall, these ablation results jointly validate that TrafficMoE benefits from a tightly coupled design combining heterogeneous expert modeling, uncertainty-aware filtering, conditional aggregation, and large-scale pre-training.

Impact of Expert Number. We further investigate the sensitivity of TrafficMoE to the number of experts in different branches, including the Header, Payload, and Global branches. Fig. 6 reports the variation of F1-score with respect to the expert number on ISCX-Tor2016 and CSTNET-TLS datasets.

On ISCX-Tor2016, all three branches as shown in Fig. 6 (a), (b) and (c) exhibit rapid performance improvements when the number of experts increases from 2 to 8, followed by a smoother convergence beyond 16 experts. Notably, the Payload branch shows the most pronounced performance gain in the low-expert regime, reflecting the high heterogeneity and noisy characteristics of Tor-encrypted payloads, which benefit substantially from increased expert diversity. In contrast, the

![](images/43f351d4655deee227625af210c97442348db14312d2a866e088d91b55a7f640.jpg)

<details>
<summary>bar</summary>

|   Experts |   Average Gate Activation per Class |
|----------:|-------------------------------------:|
|         1 |                                  0.4 |
|         2 |                                  0.3 |
|         3 |                                  0.2 |
|         4 |                                  0.1 |
|         5 |                                  0.1 |
|         6 |                                  0.1 |
|         7 |                                  0.1 |
|         8 |                                  0.1 |
|         9 |                                  0.1 |
|        10 |                                  0.1 |
|        11 |                                  0.1 |
|        12 |                                  0.1 |
|        13 |                                  0.1 |
|        14 |                                  0.1 |
|        15 |                                  0.1 |
</details>

(a) Early training stage

![](images/a1aadc4cbe324e78510da3e0bd9f9f2fcfe4969b726dbfc44e6b40cd27d69263.jpg)  
(b) Converged stage   
Fig. 7: Class-wise expert behavior analysis of TrafficMoE. The average expert activation for each traffic class at the early training stage (Epoch 0) and converged stage (Epoch 120) is visualized, respectively. As training progresses, the routing distributions evolve from dispersed and class-agnostic patterns to structured and class-specific activations, indicating the expert specialization is aligned with semantic traffic categories.

Header branch converges more quickly, indicating that headerlevel patterns are relatively more structured. A similar trend is observed on CSTNET-TLS. The F1-score steadily improves with increasing expert numbers across all branches. The Global branch demonstrates relatively stable performance, suggesting that global representations aggregate complementary information from both header and payload streams and are less sensitive to over-parameterization. Increasing the number of experts beyond 16 yields marginal improvements, highlighting a favorable trade-off between performance and efficiency.

Overall, increasing the number of experts consistently improves classification performance across all branches on both datasets, indicating that larger expert pools enable more finegrained specialization and richer representation capacity. The performance gains gradually saturate as the number of experts increases, suggesting that a moderate number of experts is sufficient to balance model capacity and efficiency, while excessive scaling may lead to redundant specialization without significant performance gains.

# D. Expert Behavior and Visualization Analysis

Class-wise Expert Activation Behavior Analysis. To further investigate whether the proposed TrafficMoE learns meaningful expert specialization beyond performance gains, we analyze the class-wise expert activation patterns during training, i.e., expert behavior w.r.t. different classes. Fig. 7 visualizes the average routing weights of experts for each traffic class at the initial training stage (i.e., Epoch 0) and converged stage (i.e., Epoch 120). At the early stage of training, the routing distributions across experts are largely dispersed and exhibit weak class dependency. Different traffic categories activate similar subsets of experts with comparable weights, indicating that the routing mechanism has not yet achieved structured specialization and behaves close to class-agnostic assignment. This observation is consistent with randomly initialized gating functions, where expert selection is primarily driven by stochastic variations rather than semantic distinctions. As training progresses, the activation patterns evolve into significantly more structured and classaware distributions. At the converged stage, each traffic class consistently focuses its activation on a small subset of experts, while suppressing others, leading to clearly distinguishable “expert–class” associations. That is, different classes exhibit distinct expert preference profiles, demonstrating that the routing mechanism adaptively aligns experts with class-specific traffic characteristics.

![](images/1fd341aeed5b4976c1a2afea04d12b250b4df0c3ec52e13d852c339adf90fb0d.jpg)

<details>
<summary>heatmap</summary>

| Token Index (Sequence) | Relative Energy (0.1) |
| :--- | :--- |
| 0 | 0.0 |
| 1 | 0.2 |
| 2 | 0.4 |
| 3 | 0.6 |
| 4 | 0.8 |
| 5 | 1.0 |
</details>

(a) Before UF

![](images/4f158ae008936d0851ebf09640cfb9c5dd6b77f870a12ec08b09ae601742e9d4.jpg)

<details>
<summary>heatmap</summary>

| Token Index (Sequence) | Relative Energy (I_0, I_1) |
| :--- | :--- |
| 0 | 0.0 |
| 1 | 0.2 |
| 2 | 0.4 |
| 3 | 0.6 |
| 4 | 0.8 |
| 5 | 1.0 |
</details>

(b) After UF   
Fig. 8: Visualization of UF module before and after filtering. The heatmaps illustrate the relative feature magnitude of interleaved packet sequences across different traffic samples. The red dashed lines delineate the boundaries between individual network packets, while the white dotted lines separate the header and payload segments within each packet. After filtering, UF drastically suppresses the noisy components with high-energy activations in encrypted payload segments.

These results provide strong evidence that TrafficMoE does not merely rely on increased model capacity, but instead learns semantically meaningful expert specialization through datadriven routing. Such emergent class-aware expert activation supports the effectiveness of the heterogeneous MoE design in capturing diverse traffic patterns and contributes to the interpretability and robustness of the proposed framework.

Visualization of Uncertainty-aware Filtering. To intuitively demonstrate the efficacy of the proposed UF module, we visualize the feature energy magnitude of token sequences before and after the filtering process via $L _ { 2 }$ norm. As shown in Fig. 8, the input sequence preserves the physical temporal structure of raw traffic, interleaving header and payload patches across multiple packets. Before filtering, the encrypted payload segments exhibit dense, high-energy activations with noisy information. After filtering, the high-entropy noisy components are drastically suppressed. Conversely, the reliable header metadata and highly discriminative signatures in payloads are strictly preserved.

# V. CONCLUSION AND FUTURE WORK

In this paper, we present a heterogeneous-aware mixtureof-experts (TrafficMoE) framework for encrypted traffic interpretation, which follows a Disentangle-Filter-Aggregate paradigm. Motivated by the intrinsic structural disparity between headers and payloads, we propose a dual-branch architecture with modality-specific MoE modules to enable conditional expert specialization without cross-modal interference. To further suppress unreliable tokens and noisy components, we propose an Uncertainty-aware Filtering (UF) mechanism that estimates token-level uncertainty from crossmodal interaction entropy, enabling both header and payload feature purification. An implicit Conditional Aggregation (CA)

module, followed by a Global MoE branch, is then designed to adaptively aggregate purified representations and enhance cross-modal adaptability.

Despite its effectiveness, several directions remain for future investigation. First, current expert routing is learned in a datadriven manner without explicit structural priors. Incorporating protocol-level or temporal constraints into the routing process may further enhance interpretability and stability. Second, extending the framework to continual or open-world traffic scenarios, where traffic distributions evolve over time, is challenging, unexplored and an promising direction. Finally, exploring more principled uncertainty estimation strategies beyond entropy-based interaction measures may provide deeper theoretical grounding for reliability-aware modeling in encrypted environments.

# REFERENCES

[1] A. Madhukar and C. Williamson, “A longitudinal study of p2p traffic classification,” in 14th IEEE international symposium on modeling, analysis, and simulation. IEEE, 2006, pp. 179–188.   
[2] J. Sherry, C. Lan, R. A. Popa, and S. Ratnasamy, “Blindbox: Deep packet inspection over encrypted traffic,” in Proceedings of the ACM conference on special interest group on data communication, 2015.   
[3] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “Robust smartphone app identification via encrypted network traffic analysis,” IEEE Transactions on Information Forensics and Security, vol. 13, no. 1, pp. 63–78, 2017.   
[4] A. Panchenko, F. Lanze, J. Pennekamp, T. Engel, A. Zinnen, M. Henze, and K. Wehrle, “Website fingerprinting at internet scale.” in NDSS, vol. 1, 2016, p. 23477.   
[5] M. Lotfollahi, M. Jafari Siavoshani, R. Shirali Hossein Zade, and M. Saberian, “Deep packet: A novel approach for encrypted traffic classification using deep learning,” Soft Computing, vol. 24, no. 3, pp. 1999–2012, 2020.   
[6] M. Lopez-Martin, B. Carro, A. Sanchez-Esguevillas, and J. Lloret, “Network traffic classifier with convolutional and recurrent neural networks for internet of things,” IEEE access, vol. 5, pp. 18 042–18 050, 2017.   
[7] M. Shen, J. Wu, K. Ye, K. Xu, G. Xiong, and L. Zhu, “Robust detection of malicious encrypted traffic via contrastive learning,” IEEE Transactions on Information Forensics and Security, 2025.   
[8] Y. Liu, X. Wang, B. Qu, and F. Zhao, “Atvitsc: A novel encrypted traffic classification method based on deep learning,” IEEE transactions on information forensics and security, vol. 19, pp. 9374–9389, 2024.   
[9] S. Cui, C. Dong, M. Shen, Y. Liu, B. Jiang, and Z. Lu, “Cbseq: A channel-level behavior sequence for encrypted malware traffic detection,” IEEE Transactions on Information Forensics and Security, vol. 18, pp. 5011–5025, 2023.   
[10] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in Proceedings of the ACM Web Conference 2022, 2022, pp. 633–642.   
[11] G. Zhou, X. Guo, Z. Liu, T. Li, Q. Li, and K. Xu, “Trafficformer: an efficient pre-trained model for traffic data,” in 2025 IEEE Symposium on Security and Privacy (SP). IEEE, 2025, pp. 1844–1860.   
[12] M. Zhan, J. Yang, D. Jia, and G. Fu, “Eapt: An encrypted traffic classification model via adversarial pre-trained transformers,” Computer Networks, vol. 257, p. 110973, 2025.   
[13] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “Fs-net: A flow sequence network for encrypted traffic classification,” in IEEE INFOCOM, 2019, pp. 1171–1179.   
[14] K. Lin, X. Xu, and H. Gao, “Tscrnn: A novel classification scheme of encrypted traffic based on flow spatiotemporal features for efficient management of iiot,” Computer Networks, vol. 190, p. 107974, 2021.   
[15] W. Sun, Y. Zhang, J. Li, C. Sun, and S. Zhang, “A deep learning-based encrypted vpn traffic classification method using packet block image,” Electronics, vol. 12, no. 1, p. 115, 2022.   
[16] X. Meng, C. Lin, Y. Wang, and Y. Zhang, “Netgpt: Generative pretrained transformer for network traffic,” arXiv preprint arXiv:2304.09513, 2023.   
[17] D. Zhao, B. Jiang, S. Liu, S. Cui, M. Shen, D. Han, X. Guan, and Z. Lu, “Language of network: A generative pre-trained model for encrypted traffic comprehension,” arXiv preprint arXiv:2505.19482, 2025.

[18] X.-Y. Chen, L. Han, D.-C. Zhan, and H.-J. Ye, “Miett: Multi-instance encrypted traffic transformer for encrypted traffic classification,” in AAAI, vol. 39, no. 15, 2025, pp. 15 922–15 929.   
[19] S. Cui, X. Han, D. Han, Z. Wang, W. Wang, B. Jiang, B. Liu, and Z. Lu, “Fg-sat: Efficient flow graph for encrypted traffic classification under environment shifts,” IEEE Transactions on Information Forensics and Security, 2025.   
[20] R. A. Jacobs, M. I. Jordan, S. J. Nowlan, and G. E. Hinton, “Adaptive mixtures of local experts,” Neural Computation, vol. 3, pp. 79–87, 1991.   
[21] M. I. Jordan and R. A. Jacobs, “Hierarchical mixtures of experts and the em algorithm,” Neural Computation, vol. 6, no. 2, pp. 181–214, 1994.   
[22] N. Shazeer, A. Mirhoseini, K. Maziarz, A. Davis, Q. Le, G. Hinton, and J. Dean, “Outrageously large neural networks: The sparsely-gated mixture-of-experts layer,” arXiv preprint arXiv:1701.06538, 2017.   
[23] D. Lepikhin, H. Lee, Y. Xu, D. Chen, O. Firat, Y. Huang, M. Krikun, N. Shazeer, and Z. Chen, “Gshard: Scaling giant models with conditional computation and automatic sharding,” arXiv, 2020.   
[24] W. Fedus, B. Zoph, and N. Shazeer, “Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity,” Journal of Machine Learning Research, vol. 23, no. 120, pp. 1–39, 2022.   
[25] J. Ma, Z. Zhao, X. Yi, J. Chen, L. Hong, and E. H. Chi, “Modeling task relationships in multi-task learning with multi-gate mixture-of-experts,” in ACM SIGKDD, 2018, pp. 1930–1939.   
[26] C. Riquelme, J. Puigcerver, B. Mustafa, M. Neumann, R. Jenatton, A. Susano Pinto, D. Keysers, and N. Houlsby, “Scaling vision with sparse mixture of experts,” Advances in Neural Information Processing Systems, vol. 34, pp. 8583–8595, 2021.   
[27] G. D. Gil, A. H. Lashkari, M. Mamun, and A. A. Ghorbani, “Characterization of encrypted and vpn traffic using time-related features,” in Proceedings of the 2nd international conference on information systems security and privacy (ICISSP 2016). SciTePress, 2016, pp. 407–414.   
[28] I. Sharafaldin, A. H. Lashkari, A. A. Ghorbani et al., “Toward generating a new intrusion detection dataset and intrusion traffic characterization.” ICISSp, vol. 1, no. 2018, pp. 108–116, 2018.   
[29] K. Cho, K. Mitsuya, and A. Kato, “Traffic data repository at the {WIDE} project,” in USENIX ATC, 2000.   
[30] A. H. Lashkari, G. D. Gil, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of tor traffic using time based features,” in International Conference on Information Systems Security and Privacy, vol. 2. SciTePress, 2017, pp. 253–262.   
[31] S. Dadkhah, H. Mahdikhani, P. K. Danso, A. Zohourian, K. A. Truong, and A. A. Ghorbani, “Towards the development of a realistic multidimensional iot profiling dataset,” in 2022 19th Annual International Conference on Privacy, Security & Trust (PST). IEEE, 2022, pp. 1–11.   
[32] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware traffic classification using convolutional neural network for representation learning,” in ICOIN. IEEE, 2017, pp. 712–717.   
[33] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “Appscanner: Automatic fingerprinting of smartphone apps from encrypted network traffic,” in IEEE European Symposium on Security and Privacy, 2016, pp. 439–454.   
[34] K. Al-Naami, S. Chandra, A. Mustafa, L. Khan, Z. Lin, K. W. Hamlen, and B. Thuraisingham, “Adaptive encrypted traffic fingerprinting with bidirectional dependence,” in Proceedings of the 32nd Annual Conference on Computer Security Applications. ACM, 2016, pp. 177–188.   
[35] A. Panchenko, F. Lanze, J. Pennekamp, T. Engel, A. Zinnen, M. Henze, and K. Wehrle, “Website fingerprinting at internet scale,” in 23rd Annual Network and Distributed System Security Symposium, 2016.   
[36] P. Sirinam, M. Imani, M. Juarez, and M. Wright, “Deep fingerprinting: Undermining website fingerprinting defenses with deep learning,” in ACM SIGSAC, 2018, pp. 1928–1943.   
[37] M. Shen, J. Zhang, L. Zhu, K. Xu, and X. Du, “Accurate decentralized application identification via encrypted traffic analysis using graph neural networks,” IEEE Transactions on Information Forensics and Security, vol. 16, pp. 2367–2380, 2021.   
[38] R. Schuster, V. Shmatikov, and E. Tromer, “Beauty and the burst: Remote identification of encrypted video streams,” in 26th USENIX Security Symposium, 2017, pp. 1357–1374.   
[39] R. Zhao, M. Zhan, X. Deng, Y. Wang, Y. Wang, G. Gui, and Z. Xue, “Yet another traffic classifier: A masked autoencoder based traffic transformer with multi-level flow representation,” in AAAI, vol. 37, no. 4, 2023, pp. 5420–5427.   
[40] L. Liu, R. Li, Q. Li, M. Hou, Y. Jiang, and M. Xu, “Flowletformer: Network behavioral semantic aware pre-training model for traffic classification,” in arXiv, 2025.
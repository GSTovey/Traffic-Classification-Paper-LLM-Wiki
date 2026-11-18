# PP-OpenNet: Privacy-Preserved Open Set Classification for Network Traffic

Jingze Zhang<sup>∗</sup>, Leijie Wu<sup>†</sup>, Xi Peng<sup>†</sup>, Qingqing Yang<sup>†</sup>, Ruilun Liu<sup>‡</sup>, Hong Xu<sup>∗</sup>

<sup>∗</sup>The Chinese University of Hong Kong, Hong Kong, China

<sup>†</sup>Huawei Theory Lab, Hong Kong, China

<sup>‡</sup>University of Hong Kong, Hong Kong, China

Abstract— Network traffic classification is a fundamental and ubiquitous task in a wide range of network applications. It plays a critical role in enhancing the Quality of Service (QoS) for network systems and safeguarding Internet users from potential security threats. However, traditional methods relying on Deep Packet Inspection (DPI) face critical limitations. First, packet header and payload inspection poses severe privacy risks. Second, the rapid proliferation of applications introduces diverse, ”unseen” traffic, complicating classification in open-world scenarios. To address these dual challenges, we propose PP-OpenNet, a lightweight deep-learning architecture for open-set traffic classification that relies solely on packet timestamp and length sequences. PP-OpenNet enhances the performance and computational efficiency by introducing disentangled multi-scale feature extraction and recurrent feature fusion mechanisms. We evaluate it on realworld datasets to demonstrate its superiority over state-of-theart baselines and ablation variants in different open-set metrics. To the best of our knowledge, PP-OpenNet represents a novel solution to the dual challenges of open-set recognition and a privacy-preserving design in network traffic classification.

Index Terms—Network Traffic Classification, Open-Set Classification

## I. INTRODUCTION

Edge devices, including smartphones and smart cars, have seen exponential growth in recent years. This surge has significantly enhanced connectivity and convenience for Internet users, while simultaneously generating vast amounts of network traffic data (NTD) from diverse applications. It is estimated that 63% of global network traffic originates from edge devices [1], with 72.7% of this traffic stemming from popular applications [2]. Despite this volume, research on Network Traffic Classification (NTC) has been outpaced by advancements in Computer Vision (CV) and Natural Language Processing (NLP), particularly regarding open-world adaptability. This gap limits the ability to optimize network resources and extract critical insights from complex, realworld network environments.

A central challenge in advancing NTC is the fundamental tension between classification accuracy and user privacy. The industrial standard, Deep Packet Inspection (DPI), analyzes both packet headers and payloads to identify applications. However, this approach is inherently intrusive. Analyzing packet content risks exposing sensitive personal data (e.g., biometric identifiers) and violates stringent privacy regulations such as GDPR [3]. While recent Deep Learning (DL) methods (e.g., ET-BERT [4]) have improved classification performance, many still rely on analyzing semantic header fields (such as IP addresses) or payload sequences, inheriting these critical privacy vulnerabilities.

Beyond privacy, the deployment of NTC at the network edge introduces three critical challenges: (i). Open-World Dynamics (Unseen Classes): The rapid emergence of new applications introduces traffic patterns distinct from those seen during training. Standard classifiers often struggle to generalize in this setting, unable to distinguish these truly novel patterns from known applications, leading to significant misclassification. (ii). Environmental Sensitivity (Domain Shift): Even for known applications, traffic patterns are highly sensitive to varying network states (e.g., congestion, jitter). This introduces significant statistical noise, requiring models to be robust against environmental variations to maintain generalizability. (iii). Resource Constraints: Classification agents are typically deployed at base stations or edge gateways (see Figure 1) with limited computational power and memory. This makes large, dense models impractical for real-time inference.

To address these challenges, we propose PP-OpenNet, a lightweight and efficient architecture for open-set, application-level network traffic classification. Crucially, to resolve the privacy tension, our method relies solely on nonintrusive metadata: packet timestamps and lengths. This design eliminates the need for payload inspection and ignores semantic header fields entirely, ensuring privacy compliance by default while effectively handling the demands of realworld traffic.

To overcome the information loss inherent in using only metadata, we introduce a disentangled multi-scale feature extractor. This module breaks down feature extraction into lightweight components, including an auxiliary Machine Learning-based module, to capture precise statistical signatures without the heavy computational cost of deep, monolithic networks. Next, we employ a recurrent feature fusion mechanism. Unlike traditional deep stacking, this module models the hierarchical relationships between multi-scale features, effectively integrating shallow and deep representations to maximize information retention.

Finally, we adopt a prototype learning framework to enable robust open-set classification. To improve the computational efficiency of this framework, we introduce a learnable twophase random projection module. Instead of performing costly distance calculations in high-dimensional space, this mechanism maps the fused features into a lower-dimensional space optimized for prototype separation. This approach balances the trade-off between representational power and inference latency, ensuring robust performance on edge devices.

![](images/59439fbd01fa668d86b74d3bdc379ef4fcb88637d07d32f57ede3c35d9632c8f.jpg)  
Fig. 1: A privacy-constrained network traffic classification scenario.

The key contributions of PP-OpenNet are: (i) We propose a new framework for open-world application identification that uniquely integrates strong privacy preservation (metadataonly) with edge-deployment constraints. (ii) We design a hierarchical multi-scale feature extractor and a depth-aware fusion module that capture complex traffic patterns efficiently, reducing reliance on heavy backbones. (iii) We enhance the prototype learning paradigm with a two-phase learnable random projection, facilitating robust open-set detection while minimizing computational overhead.

## II. RELATED WORK

## A. Network Traffic Classification

Existing Network Traffic Classification (NTC) methods struggle to balance classification performance with strict privacy and open-world adaptability. Traditional ML methods rely on feature engineering. Approaches like FlowPrint [5] fingerprint header fields (e.g., IP address), which is efficient but intrusive and brittle against encryption. Conversely, privacy-preserving methods like AppScanner [6] rely solely on statistical features (e.g., packet lengths), but often lack the representational power to generalize in dynamic environments.

Deep Learning (DL) methods automate feature extraction but face similar trade-offs. SOTA models like ET-BERT [4] achieve high accuracy by pre-training on payloads, inherently violating privacy regulations like GDPR. While methods like FlowPic [7] are able to respect the privacy by visualizing traffic metadata, they share a critical limitation with the aforementioned works—the closed-set assumption.

Crucially, an inherent conflict between privacy and openworld adaptability pervades existing research. Most privacypreserving methods operate under a strict closed-set assumption, restricting their utility in networks where new applications constantly emerge. Conversely, the rare exceptions addressing open-set scenarios, such as DeviceMien [8], typically revert to intrusive header analysis to achieve separation. This highlights the specific gap our work addresses: a method that is simultaneously application-level, open-set, and strictly privacy-constrained.

## B. Open-Set Recognition (OSR)

Open-Set Recognition (OSR) addresses the realistic scenario where classes unseen during training appear at test time [9]. Unlike closed-set models that inevitably force novel inputs into known categories, OSR frameworks must accurately classify known instances while effectively rejecting unknown ones. While generative approaches (e.g., [10]) can model data distributions to detect outliers, they are often computationally prohibitive for edge devices. In contrast, discriminative methods like prototype learning [11] offer a lightweight alternative, representing classes as compact centroids to enable efficient rejection suitable for resource-constrained environments.

In the context of Network Traffic Classification, this openset capability is essential due to the constant emergence of new applications and evolving traffic patterns. This dynamic nature creates a significant difficulty for identifying specific Target Applications among diverse unknown traffic. To address this, we exploit a practical advantage: the ease of collecting generic ”Background Traffic” from real-world streams. By incorporating this accessible data during training as an auxiliary class, we further constrain the decision boundaries. This constitutes a practical setting consistent with real-world scenarios, enhancing the model’s ability to distinguish target applications from novel open-set traffic.

## III. METHODOLOGY

This section details the design of PP-OpenNet (Figure 2a). We first formalize the traffic characteristics, then detail the three core modules: Multi-Scale Feature Extraction (MSFE), Recurrent Feature Fusion (RFF), and Prototype Vector Random Projection (PVRP).

## A. Network Traffic Characteristics

Traffic Structure & Variability: Network traffic is a sequential stream of packets. While payload content (I ) is generally invariant, privacy constraints restrict us to metadata $( V _ { s } ;$ timestamp, length), which is highly sensitive to transmission dynamics. We model the collected traffic $( T _ { c } )$ as a distorted version of the source traffic $( T _ { s } ) \colon T _ { c } = A l t e r ( T _ { s } , D _ { s } , S _ { \mathrm { n e t } } , U )$ where external factors such as device state $D _ { s } ,$ , network conditions $S _ { \mathrm { n e t } }$ (e.g., congestion), and user behavior U introduce variance.

Invariant Feature Mapping: Since reversing this alteration is impractical, our goal is to learn a feature mapping $F$ $\mathcal { T }  \mathcal { F }$ that satisfies two competing objectives: invariance to environmental noise $( F ( T _ { c } ) \simeq F ( T _ { c } ^ { \prime } ) )$ and discriminability for open-set recognition $( { \dot { F } } ( { \dot { T } } ^ { ( A ) } ) \not = { \dot { F } } ( T ^ { ( B ) } ) )$ . To achieve this with limited metadata, we propose a framework that explicitly disentangles features across scales rather than relying on deep, monolithic stacking.

## B. Multi-Scale Feature Extraction (MSFE)

Traditional time series feature extraction often relies on stacking deep residual modules (e.g., ResNet [12]) to increase model capacity. However, this approach presents critical limitations for edge-based traffic analysis. First, the continuous stacking of residual blocks incurs prohibitive computational complexity, making such models impractical for resourceconstrained devices. Second, deep architectures learn hierarchies implicitly, lacking explicit boundaries between feature scales. The additive nature of residual connections exacerbates this by propagating shallow, high-frequency noise (e.g., packet jitter) directly into deep layers. This ”feature entanglement” hinders the model’s ability to isolate robust global patterns from transient local noise.

![](images/2086470ad725dcaf6c3549a21a5e5fc943fee5161cd399bae9f9fce1e7cca968.jpg)  
Fig. 2: The PP-OpenNet architecture. (a) Framework overview (unrolled GRU cells share weights). (b) Multi-Scale CNN Embedder (MSCE). (c) Temporal Correlation Extractor (TCE).

To address this, our framework pivots from monolithic depth to disentangled, multi-scale width. We explicitly separate feature extraction into three specialized hierarchies to enforce clear boundaries for the extractions and prevent crossscale noise propagation: (i) Local-Scale: Packet-level correlations captured by a Multi-Scale CNN Embedder (MSCE). (ii) Global-Scale: Session-level temporal dynamics captured by a Temporal Correlation Extractor (TCE). (iii) Domain-Scale: Statistical priors (e.g., frequency moments) calculated by a lightweight ML Feature Extractor.

1) Multi-Scale CNN Embedder (MSCE): To robustly capture local patterns despite input alignment variability, we employ a translation-invariant 1D-CNN. As illustrated in Figure 2b, we adapt the Inception architecture [13] to parallelize feature extraction across diverse granularities. By simultaneously applying convolutional kernels of sizes 1, 3, and 5 alongside a max-pooling branch, this module creates a feature pyramid that captures both fine-grained bursts and aggregated local structures. The resulting multi-scale feature maps are channelconcatenated and compressed via a final stride-5 max-pooling layer, transforming the raw traffic stream into a compact sequence of tokens. Crucially, we intentionally limit the module’s depth to strictly focus on local-scale features; this prevents excessive downsampling, preserving the fine-grained temporal resolution necessary for the subsequent Global-Scale analysis.

2) Temporal Correlation Extractor (TCE): To model the global-scale dependencies across the token sequence generated by the MSCE, we employ a hybrid architecture. Two LSTM layers [14] preserve the sequential flow of events (e.g., requestresponse ordering), preventing the loss of causality.A Multi-Head Self-Attention layer is interposed between the LSTM units. While LSTMs model immediate context, self-attention efficiently captures correlations between distant tokens (e.g., across video buffering cycles). This combination ensures robust modeling of both evolving session behaviors and longrange dependencies that pure CNNs exhibit limited capability in capturing.

3) Machine Learning Feature Extractor: We supplement learned features with explicit domain-scale statistical priors (e.g., skewness, Fourier coefficients). These holistic summaries are computationally inexpensive but highly effective at identifying fundamental behaviors like periodic ”heartbeats,” which are often implicit and hard for DNNs to isolate solely from raw sequences.

## C. Recurrent Feature Fusion (RFF)

Unlike residual architectures that refine features via additive connections—which can accumulate noise and obscure scale boundaries—we premise that multi-scale features exhibit a recurrent dependency: shallow, local structures provide the necessary context to interpret deep, semantic correlations. Furthermore, while deep layers refine task-specific discriminability, they often lose generalizable information critical for recognizing open-set outliers.

To leverage this, we employ a Gated Recurrent Unit (GRU) [15] to sequentially fuse features. First, to handle dimensional discrepancies between modules, we use a lightweight Encode function (linear projection) to map all feature maps into a unified space V. We then initialize the fusion sequence with ML features $( \pmb { x } ^ { ( 0 ) } = \pmb { x } _ { m } )$ as the domain prior, followed by the encoded deep features. The GRU’s unified hidden state simplifies the integration of these heterogeneous representations: ${ \pmb v } ^ { ( i ) } = { \pmb f } _ { \mathrm { G R U } } \bar { \bf ( E n c o d e ( } { \pmb x } ^ { ( i ) } { \bf ) } , { \pmb v } ^ { ( i - 1 ) } { \bf ) }$ . We utilize GRU over LSTM for its single-state efficiency, avoiding the complexity of reconciling dual cell/hidden states. Crucially, the gating mechanism dynamically weights features, allowing the model to selectively filter noise from shallow layers while retaining generalizable patterns that clarify deeper semantic representations. This yields a fused vector v robust to openset variance.

## D. Prototype Vector Random Projection (PVRP)

To enable efficient open-set recognition, we adopt Adversarial Reciprocal Point Learning (ARPL) [11]. In ARPL, classification is governed by the kernel distance $K ( \boldsymbol { v } , \boldsymbol { k } )$ between a sample v (of dimension m) and the class prototype (Reciprocal Point, $\mathcal { P } { r p } )$ . Standard ARPL computes this kernel using a fixed mapping C, which lacks the adaptability required for edge efficiency. We therefore replace C with a Two-Phase Random Projection R. Specifically, we define ${ \mathcal R } ( { \pmb v } ) \ = \ { \pmb R } \cdot { \pmb P } _ { \perp } ( { \pmb v } )$ , where $P _ { \perp }$ is a learnable projector and R is a stochastic diagonal matrix with entries $r _ { i } \sim B e r n o u l l i ( 1 - p )$ (p is the dimension-reduction ratio). This redefines the kernel distance as the stochastic metric $\begin{array} { r } { K _ { \mathcal { R } } ( \pmb { v } , \pmb { k } ) \ = \ \frac { 1 } { m } \| \mathcal { R } ( \pmb { v } ) - \mathcal { P } r p ( \pmb { k } ) \| _ { 2 } ^ { 2 } - \mathcal { R } ( \pmb { v } ) \cdot \mathcal { P } r p ( \pmb { k } ) } \end{array}$ . The final class probability is obtained by applying Softmax over these distances to the class RPs; this probability forms the basis of the optimization objective: min $\mathbb { E } _ { R , v _ { i } } [ - \log p ( \hat { y } _ { i } =$ $k ; K _ { \mathcal { R } } ) ] + \lambda \mathcal { L } _ { m a r g i n }$ (λ is the regularization coefficient). This stochastic design serves a dual purpose: during training, R acts as a regularizer forcing $P _ { \perp }$ to satisfy Johnson-Lindenstrauss guarantees; during inference, we omit R, allowing $P _ { \perp }$ to function as a deterministic ensemble that enhances discrimination without stochastic sampling costs.

## IV. EVALUATION

## A. Dataset and Setup

Dataset Construction: To establish a robust testbed for openworld scenarios, we constructed a composite dataset comprising 361 traces and 82.43 million packets by integrating three widely-used benchmarks: ISCXVPN2016 [16], ISCXTor2016 [17], and VNAT [18]. This fusion encompasses diverse network conditions, including various tunneling protocols (VPN/Tor) and routing paths. Consistent with our privacy-preserving design, we extract only packet timestamp and length sequences, yielding a final set of 49.66k sequences for evaluation.

Preprocessing: To align with the strict latency constraints of edge QoS and the operational standards of our industry partner, we employ ”retroactive slicing.” Traffic is segmented into fixed-length sequences of 1,000 packets with a hard time limit of 2 seconds. Sequences shorter than this window are padded with historical packets (up to 8 seconds prior) to ensure completeness without sacrificing real-time responsiveness.

Open-Set Categorization: We simulate a realistic QoS management scenario by partitioning the dataset into three distinct categories: (i) Target Applications (Known): Comprises four specific, high-bandwidth video streaming applications requiring QoS optimization. (ii) Background Traffic: A diverse set of non-target applications (e.g., browsing, chat) used during training. We utilize this category to emulate the readily available, easy-to-collect traffic inherent in real networks, allowing the model to learn a robust rejection boundary against common noise without expensive labeling. (iii) Unknown: A distinct set of applications, including novel video apps and other services, reserved strictly for testing to evaluate open-set generalization. To ensure rigorous evaluation, the training and testing sets for Target Applications are drawn from disjoint traces. Furthermore, there is no application-class overlap between the Background Traffic and Unknown sets, ensuring the model is tested on truly unseen distributions. We balanced the test set such that Unknown samples constitute 50% of the data.

## B. Experimental Setup

Implementation Details: PP-OpenNet was implemented in PyTorch and trained on a single 24 GB GPU (35.6-TFLOPS FP16) using the AdamW optimizer. To ensure a fair baseline without method-specific tuning, we utilized the default learning rate of 0.001 for all models over 400 epochs. Auxiliary statistical features were extracted using tsfresh [25].

Baselines: We benchmark against two distinct categories of methods: (i) Domain-Specific SOTA: Methods specialized for traffic analysis, including ML-based (CUMUL [19], AppScanner [6]) and DL-based (FlowPic [7], Tik-Tok [20], VarCNN [21], FS-Net [22]); (ii) General Time-Series Models: Stateof-the-art sequence model adaptations, including ResNet (1D variants) [12], InceptionTime [23], and PatchTST [24].

Metrics: We evaluate performance using Open-Set Accuracy (ACC) and Open-Set Classification Rate (OSCR) [26], which jointly evaluates known-class accuracy and unknown-class rejection. We also report UAUROC as an auxiliary metric to diagnose the specific capability of detecting unknown traffic. Efficiency is measured via Inference Time (ms), VRAM, MACs, and Parameter count.

## C. Experimental Result

The comparative results are presented in Table I. PP-OpenNet (projection ratio $p = 0 . 7 5 )$ achieves state-of-the-art performance across key metrics.

Comparative Analysis: PP-OpenNet achieves the highest ACC (94.34%) and OSCR (92.08%), significantly outperforming prior domain-specific models like FS-Net and Var-CNN. Notably, while the ML-based AppScanner achieves high UAUROC (99.39%), its low ACC (89.27%) reveals a critical limitation: statistical features are sufficient for detecting outliers but lack the representational power to accurately distinguish between specific target applications. Furthermore, our model surpasses powerful general-purpose baselines, including ResNet50 and PatchTST. This validates that our domain-aware design—specifically the disentangled Multi-Scale Feature Extraction (MSFE)—is more effective for processing packet metadata than simply applying deeper, generic backbones.

Efficiency and Edge Viability: PP-OpenNet successfully balances high accuracy with the strict resource constraints of edge devices. (i) Computational Efficiency: Compared to ResNet34, PP-OpenNet requires 13.4× fewer MACs (104.8 M vs. 1.4 G) while delivering superior accuracy. This indicates that our architectural choices eliminate the need for the naive parameter scaling typical of deep residual networks. (ii) Deployment Feasibility: In batched inference, our model achieves an ultralow latency of 0.083ms per sample with a modest 364 MB VRAM footprint. In contrast, heavy models like FS-Net (4349 MB VRAM) or ResNet50 (1788 MB VRAM) are impractical for resource-limited edge devices.

TABLE I: Results on the combined dataset.  
(Note: FlowPic tested at 500/1500 resolutions. ResNet/PatchTST variants denote depth. Time/VRAM measured at batch size 1024.)

<table><tr><td>Method</td><td>ACC</td><td>OSCR</td><td>UAUROC</td><td>Infer Time (ms)</td><td>VRAM</td><td>MACs</td><td>#Params</td></tr><tr><td>CUMUL [19]</td><td>65.73</td><td>55.07</td><td>81.62</td><td>-</td><td>-</td><td>-</td><td>-</td></tr><tr><td>AppScanner [6]</td><td>89.27</td><td>82.13</td><td>99.39</td><td>-</td><td>-</td><td>-</td><td>-</td></tr><tr><td>FlowPic (500×500) [7]</td><td>84.80</td><td>83.21</td><td>95.43</td><td>0.60</td><td>6934 MB</td><td>13.2 M</td><td>53.4 k</td></tr><tr><td>FlowPic (1500×1500) [7]</td><td>82.17</td><td>77.10</td><td>93.36</td><td>4.45</td><td>16843 MB</td><td>114.7 M</td><td>309.4 k</td></tr><tr><td>Tik-Tok [20]</td><td>88.71</td><td>86.34</td><td>96.36</td><td>0.069</td><td>6310 MB</td><td>47.79 M</td><td>2.1 M</td></tr><tr><td>VarCNN [21]</td><td>89.99</td><td>86.15</td><td>97.35</td><td>0.16</td><td>299 MB</td><td>362.55 M</td><td>8.69 M</td></tr><tr><td>FS-Net [22]</td><td>88.85</td><td>87.22</td><td>96.34</td><td>0.48</td><td>4349 MB</td><td>2.48 G</td><td>3.39 M</td></tr><tr><td>InceptionTime [23]</td><td>89.37</td><td>86.99</td><td>97.88</td><td>0.15</td><td>778 MB</td><td>499.66 M</td><td>626.95 k</td></tr><tr><td>PatchTST (3-layer) [24]</td><td>87.75</td><td>84.85</td><td>96.32</td><td>0.029</td><td>128 MB</td><td>31.16 M</td><td>567.68 k</td></tr><tr><td>PatchTST (6-layer) [24]</td><td>87.86</td><td>85.42</td><td>96.18</td><td>0.043</td><td>154 MB</td><td>62.01 M</td><td>965.12 k</td></tr><tr><td>PatchTST (9-layer) [24]</td><td>87.04</td><td>84.07</td><td>95.83</td><td>0.059</td><td>160 MB</td><td>92.86 M</td><td>1.36 M</td></tr><tr><td>ResNet18 (1-D) [12]</td><td>90.67±0.93</td><td>88.49±0.88</td><td>97.69±0.65</td><td>0.17</td><td>580 MB</td><td>684.1 M</td><td>4.2 M</td></tr><tr><td>ResNet34 (1-D) [12]</td><td>91.88±0.39</td><td>91.13±1.10</td><td>98.52±0.10</td><td>0.24</td><td>509 MB</td><td>1.4 G</td><td>7.6 M</td></tr><tr><td>ResNet50 (1-D) [12]</td><td>90.99±0.67</td><td>89.66±1.16</td><td>98.08±0.34</td><td>0.66</td><td>1788 MB</td><td>3.2 G</td><td>20.7 M</td></tr><tr><td>PP-OpenNet (ours)</td><td>94.34±0.57</td><td>92.08±1.09</td><td>99.35±0.12</td><td>0.083</td><td>364 MB</td><td>104.8 M</td><td>10.4 M</td></tr></table>

## D. Architecture Analysis and Validation

We conducted in-depth studies to validate the structural decisions behind PP-OpenNet.

Input-Aligned Comparison: To isolate architectural efficacy from input features, we compared PP-OpenNet against ResNet backbones using identical inputs (Figure 3a). Two key insights emerge: (i) Core Robustness: Even without auxiliary ML features, our architecture yields higher OSCR than ResNet34, proving the superiority of our MSFE module for this data modality. (ii) Fusion Capability: Adding auxiliary features boosts PP-OpenNet’s performance but degrades ResNet34. This confirms that standard residual connection can propagate high-frequency statistical noise, whereas our Recurrent Feature Fusion (RFF) module successfully filters noise and integrates heterogeneous information.

Module Design Validation: Figure 3c validates our specific component choices against standard alternatives. (i) MSCE: Our multi-branch design captures local patterns more effectively than standard sequential CNNs. (ii) TCE: The hybrid architecture consistently outperforms standalone blocks (LSTM, Self-Attention) and alternative configurations (Transformer, TCE-SH), confirming the necessity of our specific design for capturing diverse dependencies. (iii) Fusion Logic: Replacing our GRU fusion with LSTM degrades OSCR (92.1% → 89.9%), validating that the streamlined GRU state is more effective for integrating heterogeneous features than the complex dual-state LSTM. (iv) Depth vs. Design: Attempts to improve performance by simply adding depth (MSCE-R-2X) or residual connections (PP-OpenNet-R) resulted in degradation, confirming that ”disentanglement design” is superior to ”monolithic depth” for processing noisy traffic metadata.

Ablation Study: As shown in Figure 3b, removing any core component reduces performance. However, the removal of the Recurrent Feature Fusion (RFF) causes the most severe drop (ACC → 91.79%). This highlights that the intelligent integration of multi-scale features is as critical as the extraction

itself.

Parameter Sensitivity: Figure 3d analyzes the random projection ratio $p .$ Performance peaks at $p = 0 . 7 5$ , effectively balancing the trade-off between dimensionality reduction and information preservation.

Field Validation: In a pilot deployment within commercial 5G network from a top-tier operator, PP-OpenNet processed live traffic from urban base stations. It achieved 94.3% Precision on target applications with 69.8% Recall. The high precision ensures reliable QoS enforcement, while the conservative recall reflects the model’s robust rejection of the highly diverse, open-world noise inherent in live carrier networks.

## V. CONCLUSION

We proposed PP-OpenNet, a privacy-preserving framework for open-set traffic classification on the edge. By strictly utilizing metadata via a novel multi-scale recurrent fusion design, it achieves state-of-the-art accuracy (94.34%) and open-set robustness (92.08% OSCR). Combined with its high computational efficiency and successful field validation, this work demonstrates a practical viability for real-time deployment, paving the way for scalable and secure edge intelligence in evolving network environments.

## VI. ACKNOWLEDGEMENT

Jingze is supported in part by Huawei-CUHK Joint PhD Program (#6906388).

## REFERENCES

[1] R. Daniel, “69 Mobile Internet Traffic Statistics (2025) – Worldwide Data,” https://www.demandsage.com/mobile-internet-traffic/, 2024.

[2] W. Lyn, “25 Top Smartphone Statistics For 2025 (Latest Facts & Trends),” https://bloggingwizard.com/smartphone-statistics/, 2025.

[3] GDPR, “Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation),” https://eur-lex.europa.eu/legalcontent/EN/TXT/?uri=CELEX%3A32016R0679, 2016.

![](images/9c250f4361f46998eb9a536226ee356618305a8d07f3b21c71dd6b1a692c454e.jpg)  
(a) Backbone comparison

![](images/1152490eada8abd3be89d395d7daee642c71c44076d3edb3cb267157ef2c1e72.jpg)  
(b) Component Ablation

![](images/bcc83df5d82a30945c9231ab3d9a48119bd6c92b2d7e02e86a0e2bbd6e191617.jpg)  
(c) Module variations

![](images/305c277d06774a1b465fa8884a94148ffed4ab102fae2ac0af860d2552d121aa.jpg)  
(d) Projection ratio p  
Fig. 3: Benchmarking PP-OpenNet design choices. (a) Input-aligned backbone comparison. (b) Component ablation. (c) Module variations vs. alternatives (-SH: Single-Head, -R: Residual, -2X: Double Depth). (d) Sensitivity to projection ratio p.

[4] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “ET-BERT: A Contextualized Datagram Representation with Pre-training Transformers for Encrypted Traffic Classification,” in WWW ’22: The ACM Web Conference 2022, Virtual Event, 2022, pp. 633–642.

[5] T. van Ede, R. Bortolameotti, A. Continella, J. Ren, D. J. Dubois, M. Lindorfer, D. Choffness, M. van Steen, and A. Peter, “FlowPrint: Semi-Supervised Mobile-App Fingerprinting on Encrypted Network Traffic,” in Network and Distributed System Security Symposium, 2020.

[6] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “Appscanner: Automatic fingerprinting of smartphone apps from encrypted network traffic,” in IEEE European Symposium on Security and Privacy (EuroS&P), 2016.

[7] T. Shapira and Y. Shavitt, “FlowPic: Encrypted Internet Traffic Classification is as Easy as Image Recognition,” in IEEE INFOCOM 2019 - IEEE Conference on Computer Communications Workshops (INFOCOM WKSHPS), 2019, pp. 680–687.

[8] J. Ortiz, C. Crawford, and F. Le, “DeviceMien: network device behavior modeling for identifying unknown IoT devices,” in Proceedings of the International Conference on Internet of Things Design and Implementation, 04 2019, pp. 106—-117.

[9] W. Scheirer, A. Rocha, A. Sapkota, and T. Boult, “Toward Open Set Recognition,” IEEE Transactions on pattern analysis and machine intelligence, vol. 35, no. 7, pp. 1757–1772, 07 2013.

[10] R. Yoshihashi, W. Shao, R. Kawakami, S. You, M. Iida, and T. Naemura, “Classification-Reconstruction Learning for Open-Set Recognition,” in IEEE Conference on Computer Vision and Pattern Recognition, CVPR, 2019.

[11] G. Chen, P. Peng, X. Wang, and Y. Tian, “Adversarial Reciprocal Points Learning for Open Set Recognition,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 44, no. 11, pp. 8065–8081, Nov. 2022.

[12] K. He, X. Zhang, S. Ren, and J. Sun, “Deep Residual Learning for Image Recognition,” in 2016 IEEE Conference on Computer Vision and Pattern Recognition CVPR), 2015, pp. 770–778.

[13] C. Szegedy, W. Liu, Y. Jia, P. Sermanet, S. Reed, D. Anguelov, D. Erhan, V. Vanhoucke, and A. Rabinovich, “Going deeper with convolutions,” in 2015 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2015, pp. 1–9.

[14] S. Hochreiter and J. Schmidhuber, “Long Short-Term Memory,” Neural Computation, vol. 9, no. 8, pp. 1735–1780, 11 1997.

[15] K. Cho, B. van Merrienboer, C. Gulcehre, D. Bahdanau, F. Bougares,¨ H. Schwenk, and Y. Bengio, “Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation,” in Proceed-

ings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP), 10 2014, pp. 1724–1734.

[16] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of Encrypted and VPN Traffic using Time-related Features,” in International Conference on Information Systems Security and Privacy, 02 2016, pp. 407–414.

[17] A. Habibi Lashkari, G. Draper Gil, M. Mamun, and A. Ghorbani, “Characterization of Tor Traffic using Time based Features,” in International Conference on Information System Security and Privacy, 01 2017, pp. 253–262.

[18] S. Jorgensen, J. Holodnak, J. Dempsey, K. de Souza, A. Raghunath, V. Rivet, N. DeMoes, A. Alejos, and A. Wollaber, “Extensible Machine Learning for Encrypted Network Traffic Application Labeling via Uncertainty Quantification,” IEEE Transactions on Artificial Intelligence, vol. 5, no. 1, pp. 420–433, 2024.

[19] A. Panchenko, F. Lanze, A. Zinnen, M. Henze, J. Pennekamp, K. Wehrle, and T. Engel, “Website Fingerprinting at Internet Scale,” in Network and Distributed System Security Symposium, 02 2016.

[20] M. S. Rahman, P. Sirinam, N. Mathews, K. G. Gangadhara, and M. Wright, “Tik-Tok: The utility of packet timing in website fingerprinting attacks,” Proceedings on Privacy Enhancing Technologies, vol. 2020, no. 3, pp. 5–24, 2020.

[21] S. Bhat, D. Lu, A. Kwon, and S. Devadas, “Var-CNN: A Data-Efficient Website Fingerprinting Attack Based on Deep Learning,” Proceedings on Privacy Enhancing Technologies, vol. 4, pp. 292–310, 2019.

[22] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “Fs-net: A flow sequence network for encrypted traffic classification,” in IEEE Conference on Computer Communications (INFOCOM), 2019, 2019, pp. 1171–1179.

[23] H. Ismail Fawaz, B. Lucas, G. Forestier, C. Pelletier, D. F. Schmidt, J. Weber, G. I. Webb, L. Idoumghar, P.-A. Muller, and F. Petitjean, “InceptionTime: Finding AlexNet for Time Series Classification,” Data Mining and Knowledge Discovery, 9 2020.

[24] Y. Nie, N. H. Nguyen, P. Sinthong, and J. Kalagnanam, “A Time Series is Worth 64 Words: Long-term Forecasting with Transformers,” in International Conference on Learning Representations, 2023.

[25] C. Maximilian, B. Nils, N. Julius, and W. K.-L. Andreas, “Time Series FeatuRe Extraction on basis of Scalable Hypothesis tests (tsfresh – A Python package),” Neurocomputing, vol. 307, pp. 72–77, Sep. 2018.

[26] A. R. Dhamija, M. Gunther, and T. Boult, “Reducing Network Agnosto-¨ phobia,” in Advances in Neural Information Processing Systems, 2018.
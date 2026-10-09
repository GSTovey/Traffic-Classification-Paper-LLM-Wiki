# A Priority-Aware Dual-Channel Feature Fusion Method for Urban Rail Service Trafic Classification

Xinpeng Liu<sup>1</sup>, Junhui Zhao<sup>1\*</sup>, Zhengyuan Wu<sup>1</sup>, Huaicheng Li<sup>1</sup>

<sup>1\*</sup>School of Electronic and Information Engineering,Beijing Jiaotong University,Beijing,100044,China.

\*Corresponding author(s). E-mail(s): junhuizhao@hotmail.com; Contributing authors: 24125047@bjtu.edu.cn; 23111011@bjtu.edu.cn; huaichengli@bjtu.edu.cn;

## Abstract

With the deep integration of 5G and IoT in urban rail transit, service trafic grows explosively and accurate classification of heterogeneous service flows is essential for safe and eficient railway operations. Urban rail communication systems are subject not only to operational disturbances such as equipment failures and maintenance interference, but also to complex transmission patterns characterized by the interleaving of multi-service trafic flows. Under these operating conditions, the widespread deployment of proprietary protocols and the high prevalence of encrypted trafic further diminish the applicability of conventional port based and Deep Packet Inspection (DPI) classification methods. To address these challenges, we propose a priority-aware dual-channel feature fusion framework. Raw trafic bytes and statistical features are mapped into grayscale images and processed by a dual-branch architecture: a transfer learning-enhanced ResNet extracts fine-grained byte-level textures, while a lightweight CNN captures macroscopic statistical patterns. A channel attention mechanism dynamically recalibrates cross-modal features, and a novel Priority-Sensitive Loss (PSL) that integrates business-criticality awareness with class-balance weighting to maximize recall for safety-critical services. Evaluated on a real-world urban rail dataset using priority-weighted metrics, the method achieves 98.74% accuracy and 99.24% weighted recall, with recall of 99.94% and 99.41% on the two safety-critical services:Communication-Based Train Control(CBTC) and Emergency Radio Dispatch(ERD), providing a reliable classification foundation for priority-aware resource scheduling in urban rail communications. With only 0.18M parameters and 0.4–0.7 ms end-to-end latency, ofering an excellent balance between high-precision classification, low inference latency, and edge-deployment feasibility

Keywords: Urban Rail Service, Trafic Classification, Dual-Channel Feature Fusion, Transfer Learning

## 1 Introduction

In recent years, with the rapid development of China’s high-speed railway and urban rail transit, the railway transportation system has become an important pillar of the national comprehensive trans portation network, playing a key role in promoting the coordinated development of regional economies and improving social operation eficiency [1]. In this context, railway communication systems are evolving from traditional single-service bearer to multi-service converged bearer, with continuous growth of various service trafic and a significant increase in network load [2]. Specifically, modern railway communication networks need to simultaneously support diversified services such as train operation control, dispatching and command, passenger information service, high definition video surveillance, and intelligent operation and maintenance Internet of Things(IoT) [3], resulting in explosive growth and highly dynamic characteristics of data flows. Meanwhile, diferent services exhibit remarkable diferences in delay, bandwidth, and reliability. For instance, mission-critical railway services such as train control and signaling systems require stringent latency and reliability guarantees, while on-board video backhaul and equipment monitoring data focus more on large bandwidth and fault tolerance. Such diversification and complexity of service requirements impose higher demands on the service capability of communication systems.

Against the background of concurrent multiservices and heterogeneous Quality of Service(QoS) requirements, how to achieve accurate classification and eficient classification of service trafic in railway communication networks has become a prerequisite and key issue for network slicing, diferentiated scheduling, and QoS guarantee [4]. However, the currently deployed service classification methods in railway communication systems mostly rely on port matching or fixed rules tailored to specific systems [5]. Since diferent lines and diferent vendors often adopt proprietary or customized protocols, and with the continuous iteration of services and the emergence of abnormal trafic patterns caused by system faults, traditional methods sufer from severe deficiencies in recognition accuracy and generalization capability when facing protocol heterogeneity, dynamic service changes, and unknown fault scenarios.

Network trafic classification and railway communication service trafic classification share natural homology and task similarity. Both belong to traffic classification tasks in communication networks, are transmitted based on the TCP/IP protocol stack at the bottom layer, and are highly consistent in data structure, trafic generation mechanism, feature extraction method, and classification objective [6]. Specifically, both general Internet trafic and railway dedicated data flows can construct a characterization space through multi-dimensional features such as packet header information, payload distribution, packet length sequence, inter-arrival time, and flow duration. Their underlying logic relies on mining the spatial-temporal correlation and behavior patterns of trafic. Although railway services have domain-specific characteristics such as dedicated scenarios, high realtime requirements, and closed protocols (e.g., some adopt customized application-layer protocols or ded icated bearer networks), their core task is essentially identical to general network trafic classification, that is, to distinguish diferent service types by learning the temporal features, statistical features, and transmission patterns of trafic.

Based on such commonality of underlying mechanisms, the mature feature engineering paradigms and deep learning architectures in general network trafic classification can provide a solid technical foundation for railway scenarios. Only through adaptive migration and optimization for domain characteristics can the classification bottleneck in dedicated scenarios be efectively broken. However, existing methods still exhibit obvious deficiencies in addressing the service classification problem in urban rail communication scenarios. On one hand, a single deep learning model can hardly simultaneously capture both the structural and statistical features of raw trafic, leading to limited feature expression capability. On the other hand, due to the strong specificity and small sample char acteristics of railway services, general network trafic models lack suficient adaptability in this scenario, making it dificult to balance recognition accuracy, real-time performance, and engineering deployability. Therefore, it is urgent to design an eficient service classification method tailored to the characteristics of railway scenarios. To address the above issues, our main contributions can be briefly summarized as below:

• We introduce mature deep learning paradigms from general network trafic classification into railway service classification by adopting an imagebased trafic representation combined with transfer learning, which learns byte-level texture patterns in a protocol-agnostic manner (bypassing protocol-specific parsing) and mitigates the scarcity of labelled urban-rail samples through knowledge transferred from public general-trafic datasets.

• We design a dual-channel cross-modal feature fusion architecture. By jointly learning byte-level textures and flow-level statistical patterns with adaptive channel-attention fusion, it overcomes the representation deficiencies of single-modality models for edge-oriented trafic classification and substantially boosts overall classification performance; as shown in the module-ablation study, it exploits the complementarity of the two branches, which exhibit recognition advantages on diferent services.

• We propose PSL that, while addressing conventional class imbalance, additionally incorporates business-priority weights to enforce stronger gradient penalties on safety-critical services, thereby achieving near-zero-tolerance recall for high-priority classes without sacrificing overall accuracy, ensuring accurate admission of high-priority critical services to downstream urban-rail communication.

## 2 Related Work

Focusing on this issue, existing research has undergone an evolutionary process from rule-driven to datadriven approaches. Early methods primarily relied on port-based or protocol-based matching mechanisms [7] to classify services by querying standard ports or analyzing protocol features. However, in scenarios involving dynamic ports and the prevalence of proprietary protocols, their recognition accuracy decreases significantly. Subsequently, DPI methods enhanced recognition capabilities through sophisticated analysis of data payloads [8]. Nevertheless, these methods rely on expert experience to construct feature rules, which incurs high computational overhead, and their application is restricted under the constraints of encrypted trafic and privacy protection.

To remedy these drawbacks, machine learning techniques have been widely introduced. In the field of network trafic classification, to enhance mode automation and generalization capability, research has gradually shifted towards machine learning-based methods. By extracting statistical features such as packet length distribution and transmission interval, combined with models like Support Vector Machine (SVM) [9], Random Forest [10], and XGBoost [11], service classification is achieved. Although these methods have yielded certain results in structured feature scenarios, their performance is highly dependent on manual feature engineering. Faced with the complexities of diverse service types and significant dynamic trafic changes in railway scenarios, they struggle to achieve stable generalization.

Further progress has been made with the rapid development of deep learning. In recent years, deep learning methods have emerged as a research hotspo in the field of service classification due to their end-to-end feature learning capability. Convolutional Neural Network (CNN)-based models can automati cally extract spatial or temporal features from traffic data [12]. Some studies map network trafic to grayscale images and utilize 2D convolutional structures to explore deep patterns. Meanwhile, models such as LSTM and CNN-LSTM [13] improve recognition performance by fusing temporal information. Additionally, lightweight networks, autoencoders, and attention mechanisms [14] have been introduced to optimize model eficiency and enhance adaptability to encrypted trafic. Overall, existing research is advancing toward the direction of multi-feature fusion and model intelligence.

More recently, self-supervised pre-training has emerged as a promising paradigm for trafic classification. ET-BERT [15]pre-trains a Transformer encoder on large-scale unlabeled encrypted trafic using burst-level masked language modeling, learning contextualized datagram representations that gen eralize across multiple downstream tasks. Trafic-Former [16]introduces fine-grained pre-training tasks that capture packet direction, order, and flow mem bership, combined with a data augmentation strategy to reduce reliance on non-semantic protocol fields. YaTC [17]recasts trafic classification as a masked image modeling problem, applying a vision Transformer to flow-level feature maps. These pre-trainingbased methods achieve strong performance on public benchmarks, but their model scales (typically millions of parameters requiring GPU acceleration) are dificult to reconcile with the resource constraints of vehicle-edge hardware. Recent work has shown that carefully designed lightweight convolutional architec tures can achieve competitive accuracy with substantially lower computational cost in encrypted trafic classification [18], motivating our exploration of a compact CNN-based design for the edge deployment scenario.

Within the railway communication domain, related work on trafic analysis has primarily focused on intrusion detection. MSRNet-GLAM [19] and Gao et al. [20] propose deep learning and machine learning methods for detecting anomalous trafic in train communication networks. These eforts address a binary detection problem, which difers fundamentally from the multi-class operational service classification studied here. The present work focuses on distinguishing normal urban rail service types at the application layer, an area that remains underexplored.

## 3 Methodology

The overall architecture of the proposed model is illustrated in Fig. 1. The raw urban rail trafic is first processed into two distinct image-based representations: the raw trafic channel directly maps the processed byte sequences into a grayscale image to preserve low-level protocol structures, while the statistical feature channel first extracts features such as packet length distribution and inter-arrival times, then concatenates them into a structured statistical block image. These two representations are independently fed into their respective feature extractors. The raw channel employs a modified ResNet initialized with source-domain pre-trained weights to mine deep texture patterns, whereas the statistical channel utilizes a lightweight CNN trained from scratch to capture global statistical distributions. The extracted feature maps are concatenated along the channel dimension and dynamically recalibrated by a channel attention module, which adaptively amplifies the most discriminative representations for each input sample. Finally, the attention-weighted features are passed to a classification head integrated with Dropout, label smoothing, and a priority-sensitive loss function to complete the end-to-end classification process.

## 3.1 Raw Channel Feature Extractor

The raw trafic channel is designed to extract deep texture patterns and protocol structural features from low-level byte sequences. Given the limited sample size of urban rail trafic, this channel employs a modified ResNet architecture integrated with a transfer learning strategy. Let the input feature map be $X \in$ $\mathbb { R } ^ { N \times 1 \times 2 8 \times 2 8 }$ , where N is the batch size. The feature extraction process of the raw channel is formalized as follows. First, the input passes through a 7×7 convolutional layer with stride 2 for initial feature extraction and downsampling:

$$
X _ {1} = \operatorname{ReLU} (\mathrm{BN} (W _ {\text { conv1 }} * X)).\tag{1}
$$

At this stage, the spatial dimension is halved, resulting in an output shape of [N, 64, 14, 14]. Subsequently, a $3 \times 3$ max-pooling layer further compresses the spatial information, producing $X _ { 2 } \in \mathbb { R } ^ { N \times { \hat { 6 } } 4 \times 7 \times 7 }$ Next, a residual learning stage (Layer 1) consisting of two BasicBlocks is applied. Each residual block introduces a skip connection that adds the input to the convolutional output, mitigating the vanishing gradient problem and extracting high-level semantic features. The output of a residual block can be expressed as:

$$
X _ {\mathrm{out}} = F (X _ {\mathrm{in}}, W) + X _ {\mathrm{in}}.\tag{2}
$$

After Layer 1, the feature map dimension remains $[ N , 6 4 , 7 , 7 ]$ . Finally, to align with the output of the statistical channel, an adaptive average pooling layer ensures a fixed spatial size, followed by $\mathrm { ~ a ~ } 1 \times 1$ convolutional layer (Adjust Conv) for channel-wise adjustment. The final output of the raw channel is $F _ { \mathrm { r a w } } \in \mathbb { R } ^ { N \times 6 4 \times 7 \times 7 }$

To alleviate the training bottleneck caused by limited labeled samples in the target urban rail domain, a transfer learning strategy is incorporated into the proposed framework, which has been widely adopted for data-scarce scenarios. Considering that diferent feature modalities exhibit distinct transferability [21], an asymmetric transfer mechanism is employed. Specif ically, transfer learning is applied to the raw trafic channel to facilitate the extraction of low-level texture features. A layer-wise freezing strategy is adopted, where shallow layers (conv1 and bn1) are frozen to retain generic feature representations, while deeper layers remain trainable to adapt high-level semantics to the target domain. In contrast, the statistical channel is trained from scratch to mitigate potential negative transfer. This asymmetric design reflects the distinct transferability of the two modalities. Raw byte images capture transport-layer structural patterns (TCP/IP headers, port numbers, flag fields) that are inherent to the protocol stack and thus largely domain-invariant , which is a property consistent with the transferability of lower-layer CNN features [22]. Statistical features, however, encode application-layer behavioral signatures such as IAT distributions and burstiness profiles, which difer fun damentally between the ISCX source domain (e.g., P2P burst patterns) and the urban rail target domain (e.g., CBTC fixed-period signaling, ERD narrowband voice). Had transfer learning also been applied to the statistical branch, the model would inherit behavioral priors learned from ISCX flows that do not exist in urban rail trafic. These mismatched priors could distort the statistical channel’s early representations and degrade, rather than improve, the identification of safety-critical services. Training the statistical branch from scratch therefore preserves the domain-specific patterns essential for distinguishing control services.

![](images/649f2f5323ae529d9970ca6495e82c5307f66548eb611a8f8f4f02c81f5f9b6f.jpg)  
Fig. 1: Dual Urban Rail Trafic Classification Method

## 3.2 Statistical Channel Feature Extractor

Unlike the raw channel which focuses on low-level byte textures, the statistical channel captures global statistical patterns and temporal distribution modes. The input to this channel is $X _ { \mathrm { s t a t } } ~ \in ~ \mathbb { R } ^ { N } $ ×1×28×28 A lightweight CNN with two convolutional blocks extracts spatial features. Each block consists of a $3 \times 3$ convolution, batch normalization, ReLU, and

$2 \times 2$ max pooling. After two downsampling stages, the network produces the final statistical feature map $F _ { \mathrm { s t a t } } \in \mathbb { R } ^ { N \times { 6 4 } \times 7 \times 7 }$ , which aligns with the raw channel output dimension for subsequent fusion.

## 3.3 Dual Channel Features Concatenate

The dual-channel fusion module integrates raw trafic textures and statistical distributions for crossmodal complementarity. We concatenate raw features $F _ { \mathrm { r a w } } ~ \in ~ \mathbb { R } ^ { \bar { N } \times 6 4 \times 7 \times 7 }$ and statistical features $F _ { \mathrm { s t a t } } \ \in$ R<sup>N×64×7×7</sup> into $F _ { \mathrm { c o n c a t } } ~ \in ~ \mathbb { R } ^ { N \times 1 2 8 \times 7 \times 7 }$ along the channel dimension.

A channel attention mechanism [23] dynamically recalibrates feature weights to enhance discriminative signals and suppress noise. Finally, the refined features are processed by a classifier with global pooling, Dropout, and a fully connected layer.

## 3.4 Loss Function

In general network trafic classification, most existing methods primarily focus on improving classification accuracy and mitigating class imbalance, without explicitly modeling the business priority disparities and QoS heterogeneity inherent in industrial communication scenarios. Cross-entropy loss has been widely adopted in network trafic classification due to its strong stability and efectiveness in probability distribution modeling and classification boundary optimization [24]. In contrast, MSE and $L _ { 2 }$ based losses are mainly designed for regression tasks and usually exhibit weaker sensitivity to probabilistic outputs, which may lead to slow convergence and insuficient optimization of classification boundaries in multiclass classification scenarios. Although the widely used Focal Loss can alleviate class imbalance by emphasizing hard samples [25], in urban rail communication systems, diferent services exhibit significantly different operational criticality and QoS requirements.

Combined with the pronounced long-tailed distribu tion of railway trafic, the standard cross-entropy loss faces a dual challenge in urban rail scenar ios: it is prone to gradient dominance by majority classes while failing to impose suficient misclassifi cation penalties on safety-critical minority services. Therefore, instead of introducing more complex loss structures, this work adopts cross-entropy loss as the optimization foundation and further incorporates two independent weighting coeficients to simultaneously characterize class imbalance and business priority disparities [26]. Specifically, the proposed PSL integrates a sample-balancing weight and a business-priority weight, enabling the optimization objective to bet ter align with the practical reliability requirements of urban rail communication systems.

The first coeficient $\omega _ { c } ^ { \mathrm { p r i o r } }$ explicitly encodes business operational importance and is inversely proportional to the QoS priority value $P _ { c }$ :

$$
\omega_ {c} ^ {\mathrm{prior}} = \frac {1 / P _ {c}}{\sum_ {k = 1} ^ {C} (1 / P _ {k})}.\tag{3}
$$

The second coeficient $\omega _ { c } ^ { \mathrm { b a l } }$ employs a smoothed inverse-frequency strategy to compensate for sample scarcity and prevent gradient explosion from extreme minority classes:

$$
\omega_ {c} ^ {\mathrm{bal}} = \sqrt {\frac {N _ {\mathrm{total}}}{N _ {c}}},\tag{4}
$$

where $C \ = \ 5$ is the number of categories, $N _ { \mathrm { t o t a l } }$ denotes the total training sample count, and $N _ { c }$ is the sample count for class c. The final loss function multiplies these two independent factors to jointly optimize training stability and critical-service reliability:

$$
\mathcal {L} _ {\mathrm{PSL}} = - \frac {1}{N} \sum_ {i = 1} ^ {N} \sum_ {c = 1} ^ {C} \left(\omega_ {c} ^ {\text { prior }} \cdot \omega_ {c} ^ {\text { bal }}\right) y _ {i, c} \log (\hat {y} _ {i, c}),\tag{5}
$$

where N is the batch size, $y _ { i , c } ~ \in ~ \{ 0 , 1 \}$ represents the one-hot ground truth label, and $\hat { y } _ { i , c }$ is the predicted probability. The coeficient $\omega _ { c } ^ { \mathrm { p r i o r } }$ ensures that high-priority services receive larger gradient penalties during backpropagation, while $\bar { \omega } _ { c } ^ { \mathrm { b a l } }$ guarantees suficient gradient updates for minority classes under long-tailed distributions. Combined with label smoothing, this dual-coeficient optimization objective efectively mitigates overfitting and significantly enhances the model’s robustness in classifying critical services under rail environments.Following the service order of Table 2, the products of the two weights are 0.717, 1.538, 0.231, 0.355, and 0.230. The maximum value (1.538) belongs to ERD, the highest-priority yet least-sampled service. The max-to-min weight ratio is 6.7-fold, lower than the raw sample imbalance of 11-fold. These moderate weight magnitudes mitigate potential gradient-explosion concerns, while jointly realizing sample balance and priority awareness.

Table 1: Composition of the ISCX source-domain dataset with five non-VPN service types

<table><tr><td>Service Type</td><td>Representative Applications</td></tr><tr><td>Chat</td><td>Facebook, AIM, ICQ, Skype</td></tr><tr><td>Email</td><td>Outlook, Thunderbird</td></tr><tr><td>P2P</td><td>BitTorrent, Vuze</td></tr><tr><td>Stream</td><td>Netflix, YouTube</td></tr><tr><td>File</td><td>FTP, SMB, SCP</td></tr></table>

## 4 Experiments

In this section, we conduct a series of experiments to comprehensively evaluate the proposed method. We first describe the datasets and data preprocessing steps (section 4.1), followed by the experiment settings (section 4.2) and evaluation metrics (section 4.3). Then, comparative experiments (section 4.4) benchmark our method against existing approaches, including rule-based, traditional machine learning, and deep learning models, on a real-world urban rail dataset. These experiments compare not only classification accuracy but also computational complexity and endto-end latency, demonstrating the engineering feasibility of our method. Next, we perform two ablation studies: the module ablation study (section 4.5) verifies the individual contributions of the dual-channel architecture, transfer learning, and channel attention mechanism, the loss function ablation study (section 4.6) examines the synergistic efect of the business priority weight and class balance weight in the proposed PSL.

## 4.1 Datasets

In this section, we introduce the two datasets used in our experiments: a public network trafic dataset for transfer learning pre-training and a realworld urban rail dataset for evaluating the proposed method. The following subsections describe the composition, collection process, and key characteristics of each dataset.

## 4.1.1 Source Domain Dataset

This study utilizes the ISCX VPN-nonVPN dataset as the source domain dataset [27], constructed by the Canadian Institute for Cybersecurity (CIC) at the University of New Brunswick in 2016. The complete ISCX VPN-nonVPN collection comprises 14 trafic categories (7 VPN-encrypted and 7 non-VPN). From these, we retain five non-VPN service types (Chat, Email, P2P, Streaming, and File) as the source domain for pre-training. We select only the non-VPN subset because its trafic carries transport-level traffic patterns providing diverse byte-level textures for pre-training the raw channel with the five urban rail services without being altered by an additional VPN encapsulation layer, VPN encryption introduces extra headers and padding fields absent in operational rail trafic. The seven VPN categories are excluded for this reason. These five non-VPN types collectively span a diverse range of communication patterns—interactive messaging, bulk transfer, multimedia streaming, and file exchange—providing a suficiently broad pretraining basis for the raw channel’s transfer learning while remaining visually discriminable in the image domain. The detailed composition is summarized in Table 1.

![](images/b69837dd3dc16d84f13c024ff1e999984218316a5a4b85afdeea21b614a7996a.jpg)  
Fig. 2: Real-time I/O throughput curves of five urban rail services by Wireshark

Table 2: Urban rail service types, QoS priorities, resource types, and per-class sample counts

<table><tr><td>Business Type</td><td>Function Description</td><td>Resource Type</td><td>Priority ( $P_c$ )</td><td>Sample</td></tr><tr><td>CBTC</td><td>Train Operation Control</td><td>GBR</td><td>2</td><td>1570</td></tr><tr><td>ERD</td><td>Emergency Radio Dispatch</td><td>GBR</td><td>2</td><td>341</td></tr><tr><td>ATS</td><td>Train Status Monitoring</td><td>GBR</td><td>4</td><td>3776</td></tr><tr><td>PIS</td><td>Passenger Information Service</td><td>Non-GBR</td><td>6</td><td>712</td></tr><tr><td>CCTV</td><td>Platform Video Surveillance</td><td>Non-GBR</td><td>6</td><td>1692</td></tr></table>

## 4.1.2 Urban Rail Dataset

To comprehensively validate the efectiveness of the proposed dual-channel model in urban rail vehicle to-ground communication scenarios, raw PCAP trafic data were collected from a real-world urban rail operational environment over a continuous period. A dedicated dataset was constructed encompassing five core business categories: CBTC, ERD, Automatic Train Supervision (ATS), Passenger Information Service (PIS), and Closed-Circuit Television (CCTV). Based on the priority and delay requirements defined in [28] [29] and the importance of each service as well as the consequences of misclassification, the numerical priority values for the services are determined. The per-class sample counts, functional descriptions, Guaranteed Bit Rate(GBR) resource type and QoS priority mapping are summarized in Table 2. The dataset is partitioned using a flow-level temporal split strategy: within each service class,all captured flows are sorted chronologically by capture timestamp and divided at a 6:2:2 ratio, with earlier flows used for training and later flows for validation and testing. (This implement replaces the random flow-level split adopted in an earlier version of this study, which could result in temporally correlated trafic flows being dis tributed across the training and test sets and thus lead to an overly optimistic estimate of generalization performance.) The temporal split provides a stricter evaluation setting by requiring the model to generalize from earlier trafic observations to later unseen trafic patterns, thereby reducing the risk of temporal leakage. All comparative and ablation experiments reported in this study follow this unified tempora splitting protocol.

Fig. 2 illustrates the real-time I/O throughput curves of these five services captured via Wireshark. Significant modal discrepancies are immediately observable in the temporal domain. As illustrated in the I/O graph, the temporal packet dynamics vary significantly across diferent services. CCTV (red) maintains a high and stable baseline, reflecting continuous video streaming. CBTC (blue) displays moderate, regular fluctuations, corresponding to periodic control signaling. ATS (green) shows the most intense oscillations, driven by frequent device polling. Meanwhile, PIS (orange) and ERD (black) remain at low baselines with only occasional spikes, matching event-driven transmission. This inherent trafic heterogeneity underscores the limitations of single-feature extraction methods and provides a direct empirical basis for employing the proposed dual-channel fusion architecture in our experimental evaluation.

## 4.1.3 Data Preprocessing and Image Mapping

This section details the preprocessing procedures that convert raw trafic data into image-based representations suitable for deep learning models. Specifically, we present two mapping pipelines: one for raw byte sequences and another for statistical features.

1) Raw channel: To transform one-dimensional trafic data into a two-dimensional format suitable for CNNs, we utilize the USTC-TK-2016 toolkit [30] for standardized processing. First, raw pcap files are split into flows based on 5-tuples and cleaned to remove invalid or abnormal flows. For each processed flow, we truncate or pad the byte sequence to a fixed length and map it into a grayscale image $I \in \mathbb { R } ^ { 1 \times H \times W }$ . In this work, the input resolution is fixed at 28×28. This mapping preserves the spatial local correlation of trafic data, allowing diferent business categories to exhibit distinct texture distributions in the image domain. As illustrated in Fig. 3 and Fig. 4, both source-domain conventional trafic and urban rail services exhibit distinctly diferent texture distributions.

![](images/971222ad8a591a288fa3c6f8c67463e7e6c65cbb1e3cf04872841fa96e694b7a.jpg)  
Chat

![](images/46f19c62f8c1d53bbcb71aa3c0411adb8424a6252d0f48898e72c601a0980586.jpg)  
Email

![](images/5b1107d879434eac42a0b0e76a379257b246908f5074828ab36e658dbbb58128.jpg)  
File

![](images/209f9227bebef6024fd2bfdca900396b5958985003cc6164977bd6bd7b15b568.jpg)  
P2P

![](images/a21cebc058c062eefb2b2e4af325c6e1f3c6fa148c4ac6622d6bd6c1a2d5a1af.jpg)  
Fig. 3: Network Trafic Raw Byte Visualization  
Stream

![](images/879d85f69b81cb99a9400fc4c4d2d5a8d4d52afdbdaf139d54087d1e07f48f8c.jpg)

![](images/4eb16aa12a2772c79ad3f5da099298676c28aee6dc3f538fee8e23d0366bf3ce.jpg)  
PIS  
CCTV

![](images/5d5a1b8341c94a1bbd639be8f4ddafba690bc1df025c612fc6cd438c8872c9f5.jpg)  
CBTC

![](images/b785e78b39befe828cf557294c6fc07445de6ac566e7503045307385af1dcb67.jpg)  
ERD

![](images/e81be92153ca3615ce359dfb4e43a6c9e363b0d34b66cfa73bed5b4be582d8ee.jpg)  
ATS  
Fig. 4: Urban Rail Trafic Raw Byte Visualization

2) Stats Channel: To comprehensively characterize the temporal, intensity, and distribution properties of urban rail trafic, we extract 16 core statistical features. To adapt these one-dimensional statistical vectors to the input paradigm of deep learning models, we transform them into two-dimensional grayscale images. The specific processing pipeline is as follows: First, specific normalization rules are applied to each statistical feature to linearly compress the raw values into the range [0, 255], eliminating dimensional discrepancies while preserving the relative magnitude of feature distributions. Subsequently, each of the 16 normalized features is mapped into a $7 \times 7$ feature patch.

![](images/50f16dbdbd77f0bc2a050f6e0157d2e7f86609b505ab3ccb6d96e2a914f6b604.jpg)  
PIS

![](images/9d44431d5d829dad5d083199366a53c9756bf5ac5c1a884a525bb56bf30addd3.jpg)

![](images/f5b82eb269b95b30dfb30ce1b8c0b7fa7a0e668ab9fe623c104a73f908f71191.jpg)  
CCTV

![](images/994bcd7ee616d6bc595d212840992515e87c14d01fc11df463fb15023867b33f.jpg)  
CBTC  
ERD

![](images/67fab866cc65cd99ca9e1ebbd3025099afcf357f9ae22f5a441f92293fd1aadc.jpg)  
ATS  
Fig. 5: Statistical feature image grid (4×4 patches, 16 features) constructed from Urban Rail Trafic

The 16 patches are arranged in a 4×4 grid accord ing to a manually engineered grouping: Row 1 collects flow-scale statistics (flow duration, total packets, total bytes, average packet size); Row 2 groups rate and boundary statistics (byte rate, packet rate, max packet size, min packet size); Row 3 groups temporal statistics (packet size std, average IAT, IAT std, max IAT); and Row 4 collects shape statistics (burstiness, packet size Q1, packet size Q3, coeficient of variation). The features within each row are statistically related. For example, average IAT and IAT std jointly characterize trafic timing regularity, and max IAT and burstiness capture trafic burst characteristics. These relationships are properties of the features themselves; placing statistically related features in adjacent posi tions is, however, a manual engineering choice, and the resulting 2-D layout does not reflect an inherent spatial locality of the raw trafic data. This grouping was adopted to align the input dimension with the raw byte channel and to enable a shared downstream pipeline. As illustrated in Fig. 5, this transformation intuitively preserves the numerical diferences and global distribution patterns of each statistical feature, realizing a cross-modal mapping from onedimensional statistical information to two-dimensional spatial distribution features.Note that this grouping is tailored to our feature set, and its efectiveness on other datasets is not guaranteed due to potential generalization risk.

## 4.2 Experiment Settings

The training hyperparameters are configured as follows. The batch size is set to 16. To accommodate modality-specific convergence dynamics, the initial learning rate for the transfer learning branch in the raw channel is set to $5 \times 1 0 ^ { - 5 }$ , while the statistical branch, attention module, and classification head share a unified rate of $2 \times 1 0 ^ { - 4 }$ . Weight decay is fixed at $6 \times 1 0 ^ { - 4 }$ , and dropout rates of 0.2 and 0.1 are applied to the fully connected layers of the classification head to mitigate overfitting. Regarding the implementation environment, all models are developed in $\mathrm { P y }$ Torch 1.13.1 and accelerated by CUDA 11.6 with cuDNN 8.3.0. All experiments are conducted on a workstation equipped with an Intel Core i7 processor, 8 GB RAM, and an NVIDIA GeForce MX250 GPU (2 GB VRAM).

## 4.3 Evaluation Metrics

All deep-learning experiments are repeated over five independent random seeds—(42, 123, 2024, 7, 99)—that jointly control weight initialization, training-data shufling order, and dropout mask generation. All performance metrics are reported in the format mean±standard deviation across the five runs. The final confusion matrix presented in each experiment is selected as the seed whose accuracy is closest to the five-seed mean.

For non-iterative methods (Port-rule and DPI), the reported standard deviation reflects inherent classification stability across seeds rather than training variability. The five seeds are fixed identically across all compared methods and ablation configurations.

To evaluate model performance against existing trafic classification methods, we adopt Accuracy, Precision, Recall, and F1-score as baseline metrics [31]. Standard macro-averaging treats all classes equally, which fails to reflect the classification performance disparity of safety-critical services in heterogeneous urban rail trafic. To address this, we replace macroaveraging with a priority-weighted mechanism. Perclass metrics are first defined as:

$$
P r e _ {c} = \frac {T P _ {c}}{T P _ {c} + F P _ {c}},\tag{6}
$$

$$
R e c _ {c} = \frac {T P _ {c}}{T P _ {c} + F N _ {c}},\tag{7}
$$

$$
F 1 _ {c} = 2 \times \frac {P r e _ {c} \times R e c _ {c}}{P r e _ {c} + R e c _ {c}},\tag{8}
$$

where $T P _ { c } , F P _ { c } , F N _ { c }$ denote the true positives, false positives, and false negatives for class $c ,$ respectively. These are then aggregated using the normalized priority weight $\omega _ { c } ^ { \mathrm { p r i o r } }$ (inversely proportional to QoS priority $P _ { c } )$ :

$$
W \text {-} X = \sum_ {c = 1} ^ {C} \omega_ {c} ^ {\text { prior }} \cdot X _ {c}, \quad X \in \{P r e, R e c, F 1 \}.\tag{9}
$$

Overall accuracy is computed as the ratio of correctly classified samples to total samples. Crucially, unlike the loss function which incorporates a samplebalance term ω<sup>bal</sup> for training stability, the evaluation metrics strictly utilize $\omega _ { c } ^ { \mathrm { p r i o r } }$ alone. This separation is principled. During training, the optimizer must simultaneously combat the severe class imbalance and prioritize safety-critical services; the product form ensures neither objective is subordinated. During eval uation, the metric must answer that how well are operational safety requirements satisfied? Introducing $\omega _ { b a l } ^ { c }$ into evaluation would inflate the importance of minority classes beyond their actual operational criticality. By restricting evaluation weights to $\omega _ { p r i o r } ^ { c }$ alone, the reported metrics directly quantify QoS com pliance. To ensure fair comparison with methods not explicitly optimized for weighted objectives in comparison experiments, we additionally report standard Macro data, which treats all five classes with equal weight, alongside the priority-weighted metrics in all result tables.

## 4.4 Comparison Experiments

To comprehensively evaluate how well-established network trafic classification methods perform when applied to the urban rail service trafic domain, we conduct a series of comparison experiments on the real-world urban rail dataset, including both traditional methods and advanced deep learning models. This section describes the experimental design, includ ing baseline methods and input paradigms, followed by detailed analysis of classification performance and real-time feasibility.

## 4.4.1 Comparison Experiments Design

Traditional methods include: (1) port-based rule matching (Port-rule), (2) DPI, and (3) Random Forest based on statistical features [32]. These baselines highlight the inherent limitations of rule-driven and simple statistical models when facing real urban-rail transit environment.

For deep learning baselines, we select four rep resentative methods and strictly reproduce them according to the input formats and preprocess ing pipelines described in their original papers: (1) One-Dimensional Convolutional Neural Network (1D CNN) [12], which takes the first 784 raw bytes of each session as input, requiring flow splitting, cleaning, and fixed-length truncation or zero-padding; (2) CNN-LSTM [13], which takes 49 statistical features (e.g., mean packet length, variance, inter-arrival time) extracted from network flows as input, requiring per-flow statistical calculation and normalization; (3) Graph Neural Network (GNN) [33], which takes graph-structured data as input, where each node represents 1,500 raw bytes of a packet, edges represent temporal relationships, and global attributes include five flow-level statistical features, requiring each flow to be mapped to a directed graph; (4) Multi-Task Transformer (MTT) [14], which takes 1,500 raw bytes of a single packet (Ethernet header removed, IP addresses zeroed, TCP/UDP headers unified to 20 bytes) as input, fed directly as a byte sequence without flow reassembly.

The input paradigms directly afect end-to-end latency. Methods such as 1D-CNN and MTT directly ingest raw byte sequences, bypassing feature engineering and format conversion steps, which gives them a latency advantage. In contrast, CNN-LSTM, GNN, and our method incorporate additional data processing pipelines (e.g., sequence framing, graph topology construction, or statistical feature mapping and image generation), which inevitably introduce preprocessing overhead but provide more discriminative features.

All compared models are trained and tested under the same dataset and hardware environment to ensure fairness. Detailed performance comparisons are presented in Table 3, while the computational complexity and end-to-end latency of each model are summarized in Fig. 6 and Fig. 7.

## 4.4.2 Results Analysis

Table 3 reports the five-seed mean ± standard deviation of all methods under the temporal split. The results not only reflect diferences in overall accuracy, but more fundamentally reveal the capability gap among various approaches in handling the intrinsic characteristics of railway trafic, including multiservice concurrency, heterogeneous QoS requirements, and asymmetric misclassification costs.

Traditional rule-based approaches (Port-rule and DPI), which involve no stochastic training, the reported standard deviations reflect the intrinsic stability of their deterministic decision rules over the fixed split, rather than any training randomness, exhibit clear limitations in this scenario. Portrule achieves only $8 3 . 3 6 ( \pm 0 . 0 4 ) \%$ accuracy and DPI reaches $9 1 . 0 6 ( \pm 0 . 0 5 ) \%$ , both with negligible standard deviation,which is an expected consequence of their reliance on fixed protocol signatures rather than learned representations. Their recall on safetycritical services remains inadequate: DPI identifies 89.12% of ERD flows, and Port-rule drops to 73.24%, which is insuficient for reliable detection of safetycritical services. Although Random Forest, trained on handcrafted statistical features, improves accuracy to 88.81(±0.14)%, its relatively large standard deviation, the highest among non-deep methods, indicates that manual feature engineering alone cannot provide stable classification under temporal trafic variation.

Deep learning methods alleviate these limitations through end-to-end feature learning, but their performance diverges sharply depending on the input modality. Raw-byte methods (1D-CNN and MTT) achieve

Table 3: Performance comparison across traditional, ML, and DL methods on the urban rail dataset (five-seed mean±std)

<table><tr><td>Method</td><td>Input</td><td>Acc</td><td>Metric</td><td>PIS</td><td>CCTV</td><td>CBTC</td><td>ERD</td><td>ATS</td><td>Macro</td><td>Weighted</td></tr><tr><td rowspan="3">Port-rule</td><td rowspan="3">Raw Bytes</td><td rowspan="3">83.36(±0.04)</td><td>Recall</td><td>76.90(±0.28)</td><td>77.81(±0.19)</td><td>83.57(±0.32)</td><td>73.24(±0.59)</td><td>87.89(±0.06)</td><td>79.88(±0.11)</td><td>79.68(±0.13)</td></tr><tr><td>Precision</td><td>59.71(±1.51)</td><td>79.36(±1.94)</td><td>92.27(±0.89)</td><td>59.92(±2.20)</td><td>90.31(±0.61)</td><td>76.32(±0.35)</td><td>76.96(±0.69)</td></tr><tr><td>F1-score</td><td>67.21(±1.03)</td><td>78.57(±0.85)</td><td>87.70(±0.38)</td><td>65.90(±1.54)</td><td>89.09(±0.29)</td><td>77.69(±0.28)</td><td>77.92(±0.46)</td></tr><tr><td rowspan="3">DPI</td><td rowspan="3">Raw Bytes</td><td rowspan="3">91.06(±0.05)</td><td>Recall</td><td>89.86(±0.34)</td><td>88.99(±0.12)</td><td>95.16(±0.34)</td><td>89.12(±0.72)</td><td>90.68(±0.06)</td><td>90.76(±0.09)</td><td>91.34(±0.15)</td></tr><tr><td>Precision</td><td>75.53(±1.55)</td><td>87.62(±1.49)</td><td>95.78(±0.87)</td><td>76.03(±2.62)</td><td>96.05(±0.45)</td><td>86.20(±0.42)</td><td>86.59(±0.73)</td></tr><tr><td>F1-score</td><td>82.07(±0.98)</td><td>88.30(±0.70)</td><td>95.47(±0.38)</td><td>82.03(±1.55)</td><td>93.28(±0.19)</td><td>88.23(±0.25)</td><td>88.71(±0.42)</td></tr><tr><td rowspan="3">Random Forest [32]</td><td rowspan="3">Flow Features</td><td rowspan="3">88.81(±0.14)</td><td>Recall</td><td>88.31(±1.05)</td><td>86.92(±0.43)</td><td>92.29(±0.74)</td><td>88.24(±1.61)</td><td>88.34(±0.19)</td><td>88.82(±0.38)</td><td>89.40(±0.39)</td></tr><tr><td>Precision</td><td>70.87(±1.48)</td><td>84.80(±1.56)</td><td>94.97(±0.92)</td><td>71.00(±2.82)</td><td>94.80(±0.61)</td><td>83.29(±0.50)</td><td>83.77(±0.83)</td></tr><tr><td>F1-score</td><td>78.63(±1.20)</td><td>85.84(±0.62)</td><td>93.61(±0.51)</td><td>78.67(±2.16)</td><td>91.46(±0.24)</td><td>85.64(±0.42)</td><td>86.15(±0.59)</td></tr><tr><td rowspan="3">1D-CNN [12]</td><td rowspan="3">Raw Bytes</td><td rowspan="3">89.56(±0.24)</td><td>Recall</td><td>86.76(±1.57)</td><td>83.37(±0.76)</td><td>95.99(±0.82)</td><td>93.53(±2.20)</td><td>89.83(±0.23)</td><td>89.90(±0.57)</td><td>91.94(±0.61)</td></tr><tr><td>Precision</td><td>69.95(±1.91)</td><td>85.80(±1.60)</td><td>95.69(±0.88)</td><td>73.84(±2.62)</td><td>95.39(±0.59)</td><td>84.14(±0.49)</td><td>84.99(±0.79)</td></tr><tr><td>F1-score</td><td>77.45(±1.59)</td><td>84.55(±0.48)</td><td>95.83(±0.52)</td><td>82.51(±2.23)</td><td>92.52(±0.23)</td><td>86.57(±0.50)</td><td>87.98(±0.64)</td></tr><tr><td rowspan="3">CNN-LSTM [13]</td><td rowspan="3">Flow Features</td><td rowspan="3">92.62(±0.09)</td><td>Recall</td><td>89.86(±0.56)</td><td>88.34(±0.40)</td><td>97.39(±0.47)</td><td>95.88(±1.10)</td><td>92.77(±0.14)</td><td>92.85(±0.27)</td><td>94.44(±0.28)</td></tr><tr><td>Precision</td><td>77.46(±1.84)</td><td>89.97(±1.41)</td><td>96.90(±0.83)</td><td>80.80(±3.21)</td><td>96.77(±0.44)</td><td>88.38(±0.58)</td><td>89.02(±0.93)</td></tr><tr><td>F1-score</td><td>83.19(±1.24)</td><td>89.14(±0.49)</td><td>97.14(±0.45)</td><td>87.67(±2.16)</td><td>94.73(±0.17)</td><td>90.37(±0.43)</td><td>91.46(±0.62)</td></tr><tr><td rowspan="3">GNN [33]</td><td rowspan="3">Flow Graph</td><td rowspan="3">91.09(±0.19)</td><td>Recall</td><td>88.45(±1.31)</td><td>85.92(±0.66)</td><td>97.45(±0.67)</td><td>94.41(±1.71)</td><td>90.97(±0.18)</td><td>91.44(±0.48)</td><td>93.31(±0.50)</td></tr><tr><td>Precision</td><td>73.74(±1.91)</td><td>87.77(±1.49)</td><td>96.23(±0.76)</td><td>77.23(±2.56)</td><td>96.14(±0.55)</td><td>86.22(±0.51)</td><td>86.96(±0.76)</td></tr><tr><td>F1-score</td><td>80.42(±1.49)</td><td>86.82(±0.47)</td><td>96.84(±0.46)</td><td>84.94(±1.92)</td><td>93.48(±0.20)</td><td>88.50(±0.46)</td><td>89.77(±0.57)</td></tr><tr><td rowspan="3">MTT [14]</td><td rowspan="3">Raw Bytes</td><td rowspan="3">95.16(±0.06)</td><td>Recall</td><td>94.23(±0.53)</td><td>91.42(±0.19)</td><td>98.92(±0.25)</td><td>98.24(±0.59)</td><td>95.18(±0.06)</td><td>95.60(±0.13)</td><td>96.83(±0.13)</td></tr><tr><td>Precision</td><td>83.86(±1.52)</td><td>93.48(±1.09)</td><td>98.17(±0.69)</td><td>86.58(±2.24)</td><td>98.01(±0.31)</td><td>92.02(±0.30)</td><td>92.49(±0.62)</td></tr><tr><td>F1-score</td><td>88.73(±0.96)</td><td>92.43(±0.44)</td><td>98.54(±0.33)</td><td>92.03(±1.33)</td><td>96.57(±0.14)</td><td>93.66(±0.19)</td><td>94.50(±0.35)</td></tr><tr><td rowspan="3">Ours</td><td rowspan="3">Raw Bytes + Flow Features</td><td rowspan="3">98.74(±0.05)</td><td>Recall</td><td>98.73(±0.28)</td><td>98.76(±0.12)</td><td>99.94(±0.13)</td><td>99.41(±0.72)</td><td>98.17(±0.05)</td><td>99.00(±0.17)</td><td>99.24(±0.23)</td></tr><tr><td>Precision</td><td>95.91(±0.93)</td><td>97.83(±0.39)</td><td>99.37(±0.44)</td><td>96.31(±1.08)</td><td>99.68(±0.14)</td><td>97.82(±0.21)</td><td>97.93(±0.31)</td></tr><tr><td>F1-score</td><td>97.30(±0.50)</td><td>98.29(±0.15)</td><td>99.65(±0.23)</td><td>97.83(±0.64)</td><td>98.92(±0.06)</td><td>98.40(±0.14)</td><td>98.57(±0.21)</td></tr></table>

strong recall on services with fixed packet structures— MTT reaches 98.92% on CBTC—by learning discriminative byte-level patterns directly from payload sequences. However, their recall on variable-content services degrades significantly: 1D-CNN attains only 83.37% on CCTV, where scene-dependent video encoding produces byte textures that difer markedly across time periods. Conversely, flow-feature methods (CNN-LSTM and GNN) capture statistical regularities at the session level, such as packet-length distribu tions and inter-arrival-time statistics, but lack access to the structural cues embedded in raw payloads. As a result, their CBTC recall (97.39% for CNN-LSTM and 97.45% for GNN) consistently trails MTT’s, while their ERD recall remains in the range of 94%–96%. For non-critical services with larger sample sizes, such as ATS and PIS, all deep baselines perform acceptably, with recall above 88%, reflecting the fact that these classes are less sensitive to modality limitations and temporal variation. The accuracy standard deviations reinforce these observations: 1D-CNN (±0.24%) and GNN (±0.19%) are markedly less stable than MTT (±0.06%) and CNN-LSTM (±0.09%), confirming that weaker single-modality models are more vulnerable to random initialization and data partitioning. The complementary strengths of the two modalities, raw-byte methods excelling on fixed-structure control services, flow-feature methods better handling statistical regularity, directly motivate the dual-channel design of our proposed framework.

The proposed method achieves 98.74(±0.05)% accuracy, with recall of 99.94% on CBTC and 99.41% on ERD, and maintains precision above 95.9% across all five service categories. The reported performance gain cannot be attributed to the dual-channel architecture alone, but arises from the joint efect of the dual-channel architecture and the PSL, with the two components contributing to a comparable degree (as can be inferred from the ablation stud ies in Sections 4.5 and 4.6: with the loss fixed, the architecture improves accuracy by 4.23 pp over the best single-channel variant, 94.51% to 98.74%; with the architecture fixed, the PSL improves accuracy by 5.13 pp over cross-entropy training, 93.61% to 98.74%). Notably, under matched cross-entropy training the dual-channel architecture alone reaches 93.61%, slightly below the strongest baseline MTT (95.16%); neither component alone therefore surpasses the strongest baseline.The raw channel, enhanced by transfer learning from the ISCX VPN source domain, supplies fine-grained byte-level textures that prove efective for multimedia services; the statistical channel captures macroscopic temporal patterns such as inter-arrival times and burstiness profiles, which are critical for distinguishing periodic control services. The channel attention mechanism further adaptively fuses these complementary representations, suppressing redundant information and amplifying discrimi native features on a per-sample basis. The ±0.05% accuracy standard deviation—the smallest among all trained models—confirms that this multi-modal archi tecture yields robust convergence, with the two channels providing redundant yet complementary evidence that stabilizes predictions across diferent random seeds.

Under priority-weighted evaluation, the proposed method achieves a Weighted Recall of 0.9924(±0.0023) and a Weighted F1 of 0.9857(±0.0021), exceeding MTT’s 0.9683 and 0.9450, respectively. The standard Macro-F1, which treats all five classes with equal weight, reaches 0.9840, a margin of 0.0474 over MTT (0.9366), confirming that the advantage also holds under the unweighted macro metric and does not depend on the priority weight ing; the weighted metrics are therefore presented as a complementary view that highlights the model’s behavior on safety-critical services. From an engineering standpoint, this level of accuracy on safety-critical control trafic, achieved with only 0.18M parameters, enables reliable automated service diferentiation at the network edge without manual rule configuration, laying the groundwork for downstream tasks such as per-service QoS scheduling and dynamic resource allocation in urban rail communication systems.

In urban rail train-to-ground edge deployment scenarios, computational overhead and end-to-end latency are critical determinants of engineering feasibility. With only 0.18 M parameters (raw-trafic branch: 0.1304 M, 73.7%; statistical-feature branch: 0.0376 M, 21.2%; remaining parameters come from channel-attention module and classification head) and 23.8 M FLOPs as shown in Fig. 6 , the proposed mode is more lightweight than both MTT (41.5 M FLOPs) and 1D-CNN (39.6 M FLOPs). Fig. 7 breaks down the end-to-end latency of each model into preprocessing and inference stages. The proposed method incurs a higher preprocessing overhead (approximately 55% of the total latency, on resource-constrained edge hardware, this preprocessing step may consume a certain amount of CPU cycles and constitute a non-negligible component of the overall system load. ) than 1D-CNN and MTT (approximately 20%), reflecting the cost of constructing two parallel input representations. However, its forward inference latency (0.23–0.28 ms) is competitive with MTT (0.22–0.27 ms), and the endto-end latency (0.4–0.7 ms)(Ranges are conservatively rounded outward (floor/ceil) to guarantee coverage of the measured interval.) remains well within the millisecond-level real-time constraint of CBTC.Thus, the model achieves near-perfect recall on critical services while maintaining competitive latency and the smallest parameter count among compared methods— a practical balance between classification accuracy and edge-deployment eficiency.

![](images/06ba1a9a13e16ecf99ea35c4f380d45bb5ffb4ec86997acec377ba83ba88be7a.jpg)  
Fig. 6: Accuracy vs model complexity comparison: Parameters , FLOPs , and accuracy across five methods on the urban rail dataset.

![](images/8954d7a182c676576ac77c2dfe60fcc554a7782e7b416180fd092fa6fda8a07a.jpg)  
Fig. 7: End-to-end latency breakdown: inference latency and preprocessing latency with dynamic ranges across five classification methods.

![](images/2d8c476fa39964ed22444ea2b33470eaecec666ee0d417fe5c710c05c02bb32f.jpg)  
(a) Per-Class Precision

![](images/5fa45b4126090499ead894ea6dd248eeeed053d93e2581075f97f87099cdd792.jpg)  
(b) Per-Class Recall

![](images/d55488442e0bdc12a2de49dbdf2be0788f55559478560050c269abe301546268.jpg)  
(c) Per-Class F1  
Fig. 8: Per-class precision, recall, and F1-score across ablation configurations (Raw, Raw-TL,Stats, Dual CA OFF, Dual CA-ON)

Table 4: Ablation results: individual and combined contributions of the raw channel, statistical channel, and channel attention

<table><tr><td>Configuration</td><td>Accuracy</td><td>Macro-Precision</td><td>W-Precision</td><td>Macro-Recall</td><td>W-Recall</td><td>Macro-F1</td><td>W-F1</td></tr><tr><td>MLP</td><td>91.49 (± 0.15)</td><td>86.05 (± 0.37)</td><td>86.63 (± 0.47)</td><td>91.17 (± 0.31)</td><td>92.67 (± 0.31)</td><td>88.07 (± 0.36)</td><td>89.00 (± 0.40)</td></tr><tr><td>Stats</td><td>94.51 (± 0.11)</td><td>91.26 (± 0.42)</td><td>91.92 (± 0.65)</td><td>93.93 (± 0.29)</td><td>95.57 (± 0.31)</td><td>92.47 (± 0.32)</td><td>93.61 (± 0.45)</td></tr><tr><td>Raw</td><td>92.38 (± 0.10)</td><td>88.05 (± 0.47)</td><td>88.09 (± 0.75)</td><td>92.93 (± 0.35)</td><td>92.74 (± 0.44)</td><td>90.22 (± 0.37)</td><td>90.16 (± 0.53)</td></tr><tr><td>Raw-TL</td><td>94.19 (± 0.08)</td><td>90.68 (± 0.41)</td><td>90.87 (± 0.65)</td><td>94.43 (± 0.22)</td><td>94.74 (± 0.27)</td><td>92.41 (± 0.31)</td><td>92.65 (± 0.46)</td></tr><tr><td>Dual (CA-OFF)</td><td>96.85 (± 0.08)</td><td>94.68 (± 0.40)</td><td>94.87 (± 0.65)</td><td>97.11 (± 0.19)</td><td>97.57 (± 0.23)</td><td>95.83 (± 0.26)</td><td>96.15 (± 0.39)</td></tr><tr><td>Dual (CA-ON)</td><td>98.74 (± 0.05)</td><td>97.82 (± 0.21)</td><td>97.93 (± 0.31)</td><td>99.00 (± 0.17)</td><td>99.24 (± 0.23)</td><td>98.40 (± 0.14)</td><td>98.57 (± 0.21)</td></tr></table>

## 4.5 Ablation Study on Module

## 4.5.1 Experiment Design

This section is dedicated to systematically validate the contributions of Transfer Learning, Dual-Channel Fusion, and Channel Attention (CA). We design five configurations: (1) Raw channel only (Raw); (2) Raw channel with transfer learning (Raw-TL); (3) Statis tical channel only (Stats); (4) Dual-channel without channel attention (Dual CA-OFF); (5) the complete model with channel attention (Dual CA-ON). We additionally include an MLP baseline that takes the identical 16 statistical features as a flat vector input (3 fully-connected layers, $1 6 \to 2 5 6 \to 1 2 8 \to 5 .$ with ReLU and dropout), without the 2D reshaping step. This configuration isolates the contribution of the con volutional design. All configurations in Table 4 are trained under the full Priority-Sensitive Loss to isolate the architectural contribution.

## 4.5.2 Results Analysis

Table 4 reports the overall accuracy and weighted metrics for the five model configurations. Singlechannel architectures exhibit clear bottlenecks. The raw channel alone yields the lowest accuracy at $9 2 . 3 8 ( \pm 0 . 1 0 ) \%$ . Introducing transfer learning (Raw-TL) improves accuracy by 1.81 pp to 94.19(±0.08)%, with the gain primarily concentrated on control services, demonstrating that source-domain knowledge provides efective priors for structurally stable trafic. The statistical channel achieves slightly higher accuracy than Raw-TL $( 9 4 . 5 1 \pm 0 . 1 1 \% )$ but underperforms on multimedia services (see Fig. 8). For comparison, an MLP processing the same 16 statistical features as a flat vector achieves only $9 1 . 4 9 ( \pm 0 . 1 5 ) \%$ , given the same 16 statistical features, convolutional processing outperforms treating the features as independent inputs. Dual-channel fusion (Dual CA-OFF) substantially boosts accuracy to $9 6 . 8 5 ( \pm 0 . 0 8 ) \%$ , confirming the complementarity between raw textures and statistical features. Incorporating channel attention (Dual CA-ON) further pushes the model to $9 8 . 7 4 ( \pm 0 . 0 5 ) \%$ with the smallest standard deviation among all configurations, confirming that dynamic weighting efectively stabilizes feature fusion and suppresses noise.

Fig. 8 presents the per-class Precision, Recall, and F1-score across configurations, clearly demonstrating modality complementarity and the critical role of attention. Specifically, the Raw channel achieves significantly higher recall than the Stats channel on multimedia services (PIS, CCTV), as multimedia trafic contains rich local spatial textures in raw byte sequences. In contrast, the Stats channel performs better on periodic control services (ERD, ATS) because it efectively captures macro-level patterns such as inter-arrival time and burstiness. Transfer learning primarily improves the Raw channel’s generalization on control services but does not fully close the gap with the Stats channel. Simple dual-channel concatenation (Dual CA-OFF) already combines the strengths of both modalities, leading to substantial recall improvements across all classes, yet some classes (e.g., ERD, CCTV) remain suboptimal. After incorporating attention, the model adaptively suppresses noise from redundant modalities and amplifies discriminative features, further compensating for the weaknesses of each single channel: recall on contro services (where Raw was weak) and on multimedia services (where Stats was weak) are both significantly enhanced. Consequently, recall exceeds 98% for all five business categories, achieving near-zero missed detection for safety-critical services (CBTC, ERD). The ablation study conclusively validates the synergistic gains of transfer learning, dual-channel fusion, and channel attention, demonstrating the proposed architecture’s superior robustness and accuracy in complex urban rail trafic classification.

Table 5: Ablation of loss function design: cross-entropy vs. balance-only, priority-only, and the proposed PSL

<table><tr><td>Loss Function</td><td>Accuracy</td><td>Macro-Precision</td><td>W-Precision</td><td>Macro-Recall</td><td>W-Recall</td><td>Macro-F1</td><td>W-F1</td></tr><tr><td>Cross-Entropy</td><td>93.61 (± 0.16)</td><td>89.89 (± 0.58)</td><td>90.23 (± 0.84)</td><td>92.92 (± 0.49)</td><td>93.28 (± 0.59)</td><td>91.29 (± 0.49)</td><td>91.65 (± 0.66)</td></tr><tr><td>Balance-only</td><td>95.67 (± 0.09)</td><td>92.74 (± 0.36)</td><td>92.89 (± 0.60)</td><td>96.15 (± 0.18)</td><td>96.63 (± 0.16)</td><td>94.33 (± 0.27)</td><td>94.64 (± 0.36)</td></tr><tr><td>Prior-only</td><td>96.02 (± 0.08)</td><td>93.33 (± 0.35)</td><td>93.58 (± 0.65)</td><td>96.58 (± 0.28)</td><td>97.54 (± 0.33)</td><td>94.85 (± 0.29)</td><td>95.44 (± 0.46)</td></tr><tr><td>Ours</td><td>98.74 (± 0.05)</td><td>97.82 (± 0.21)</td><td>97.93 (± 0.31)</td><td>99.00 (± 0.17)</td><td>99.24 (± 0.23)</td><td>98.40 (± 0.14)</td><td>98.57 (± 0.21)</td></tr></table>

## 4.6 Ablation Study on Loss Function

This section is dedicated to validating the efectiveness of the dual-weight design in the proposed PSL.

## 4.6.1 Experiment Design

![](images/e05549235502bcc4f0fe8fee41bed0aed5b33427b517323f8798f036f54bf582.jpg)

We compare four loss function configurations: (1) Standard Cross-Entropy; (2) Prior only (priority weighting without balance); (3) Balance only (class balance without priority rescaling); and (4) Ours (full PSL with both business priority weight $\omega _ { c } ^ { \mathrm { p r i o r } }$ and class balance weight $\omega _ { c } ^ { \mathrm { b a l } } )$ . All configurations share the identical Dual $\mathrm { C A } { - } \mathrm { O N }$ architecture and hyperparameters.All loss configurations, including the crossentropy baseline, were trained and evaluated under the identical class-wise temporal 6:2:2 split with the same five random seeds.

![](images/ff59c4f90566d3a3d5f9c8c4b060a994432c682d5b261008877c882ae46898a2.jpg)

## 4.6.2 Results Analysis

Table 5 summarizes the overall accuracy and weighted metrics for the four loss function configurations. Additionally, to intuitively illustrate the fine-grained classification performance across diferent service types, the confusion matrix on the test set is presented in Fig. 9.

It clearly visualizes the per-class prediction accuracy and misclassification patterns, further validating the efectiveness of the dual-channel fusion architec ture under complex multi-service scenarios. The full PSL achieves the best performance across all indica tors: accuracy of 98.74(±0.05)% and weighted recall of 99.24(±0.23)%. With Prior only, safety-critical services (CBTC and ERD) are well preserved, but recall on low-priority services degrades, yielding a weighted recall of 97.54%. Balance only improves minority-class recall at some cost to the majority class, resulting in a weighted recall of 96.63%. The unweighted crossentropy performs worst across all metrics; notably, recall on the safety-critical ERD class drops to 90.59%, confirming that without explicit weighting, the gradi ent is dominated by the most populous class (ATS). These results demonstrate that the two weighting factors serve complementary roles: $\omega _ { b a l }$ counters the raw sample-size imbalance, while $\omega _ { p r i o r }$ directs the optimizer toward operationally critical services. Neither acting alone achieves both objectives simultaneously.

(a) Cross-entropy  
(b) Prior Weight Only  
![](images/0a49e2eee426460bbefe4e52b69efbb76714beaaa856ddaa5b20102c65afeca3.jpg)

![](images/e520a3fa18cf7fa2ff192c9dd43ebdfe86966de5919b92c585f002cb2a693fc7.jpg)  
(c) Balance Weight Only  
(d) Ours (Dual weights)  
Fig. 9: Confusion matrices comparison of diferent loss function configurations.

The of-diagonal structure of the confusion matrices in ${ \mathrm { F i g . } }$ 9 further clarifies the complementary roles of the two weights. Under cross-entropy, the dominant pattern is a systematic drift of minority-class predictions toward the majority class ATS, regardless of service priority, PIS, CCTV, and ERD are all absorbed into ATS at non-negligible rates. Under balance-only, this majority absorption is substantially reduced, but residual leakage from the smallest classes (particularly ERD) toward ATS persists, because inverse-frequency weighting at the loss level cannot fully compensate for an order-of-magnitude sample-size disparity. Under prior-only, the direction of confusion reverses: ATS samples themselves begin to be misclassified as the highest-priority service ERD, indicating that priority weighting without a balance term overcorrects the decision boundary, pulling majority-class samples toward the safety-critical prediction slots. Only the full PSL, which couples $\omega _ { p r i o r }$ with $\omega _ { b a l } .$ , avoids both failure modes: majority absorption is eliminated and no spurious high-priority over-prediction occurs.

## 5 Conclusion

This paper proposed a priority-aware dual-channel feature fusion framework for classifying encrypted urban rail service trafic. The raw channel, enhanced by ISCX pre-training, extracts protocol-level byte textures; the statistical channel captures flow-level temporal and distributional patterns; channel attention adaptively reweights these two modalities on a per-sample basis; and the PSL directs the optimization toward the operational priority structure, jointly weighting business criticality and class bal ance. Together, these components form an end-toend pipeline that achieves robust identification of safety-critical services on resource-constrained edge hardware.

Under a temporal split with five independent seeds, the method achieves 98.74(±0.05)% accuracy and 99.24(±0.23)% weighted recall, with CBTC and ERD recall reaching 99.94% and 99.41%. The model requires only 0.18M parameters and 0.4–0.7 ms endto-end latency. Ablation studies confirm that the raw and statistical channels contribute complementary information and that channel attention further closes residual performance gaps on both multimedia and control services.

Despite these promising results, several limitations should be acknowledged. (1) The statistical confidence of the metrics for the minority class is inherently limited. Under the temporal split, the ERD test set contains only 68 flows, so its recall is quantized in steps of approximately 1.47% (1/68); the reported 99.41% recall therefore corresponds to zero or one misclassified sample per run. By the rule of three, the 95% confidence upper bound on the missed-detection rate is approximately 4% for ERD and 1% for CBTC, which should be taken into account when interpreting the near-perfect recall of the safety-critical services. (2)The five random seeds control weight initialization, data shufling, and dropout on a single fixed tempo ral split; the reported standard deviations thus reflect training stochasticity rather than sampling uncertainty, since the same 68 ERD test flows are evaluated in all five runs. Second, the dataset was collected from a single operational line over a limited period and is proprietary, so the generalizability of the proposed method to other lines, vendors, or operational environments requires further validation. (3)Although the per-class temporal split prevents leakage of temporally adjacent flows between the training and test sets, residual correlation among flows within the same session may still exist.

## 6 Future Work

Future work will advance this framework toward production deployment along several directions. Model compression via quantization and structured pruning will reduce inference latency to submillisecond levels on low-power on-board processors, enabling integration with existing vehicle-edge hardware. Self-supervised pretraining on unlabeled urban rail trafic, coupled with validation across multiple lines and extended operational periods, will improve generalization and reduce reliance on manually labeled data. Robustness under complex dynamic network conditions, including channel fading, handover-induced packet loss, and bursty interference typical of train-to-ground wireless links, warrants dedicated study. On the application side, the classification output can directly serve as the perception frontend for downstream tasks such as QoS-aware resource scheduling, anomaly detection for equipment fault conditions, and open-set identification of unknown service types, forming a practical bridge from traffic awareness to intelligent network operation and maintenance.

## Acknowledgements

The authors would like to thank the anonymous reviewers for their valuable comments and the Institute of Computing Technologies, China Academy of Railway Sciences Corporation Limited.

## Author Contributions

Xinpeng Liu: Conceptualization, Methodology, Software, Investigation, Formal Analysis, Data Curation, Original Draft, Review & Editing, Visualization; Junhui Zhao: Conceptualization,Review & Supervision; Zhengyuan Wu: Conceptualization, Methodology; Huaicheng Li: Review & Supervision.

## Funding

This work was supported by National Engineering Research Center of System Technology for High Speed Railway and Urban Rail Transit, under Grant No. 2024YJ255.

## Declarations

## Conflict of Interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## Data Availability

The VPN-NonVPN Dataset (ISCXVPN2016) is provided by the Canadian Institute for Cybersecurity (CIC), University of New Brunswick (UNB), and can be accessed at: http://www.unb.ca/cic/datasets/vpn. html. The urban rail transit trafic dataset used in this study is provided by the Institute of Computing Technologies, China Academy of Railway Sciences Corporation Limited. Due to project confidentiality and privacy-related restrictions, the raw data cannot be made publicly available at the present stage.

## References

[1] Zhao, J., Gao, X., Wu, Z., Zhang, Q., Han, H.: Artificial intelligence in rail transit wireless communication systems: Status, challenges and solutions. Physical Communication 67, 102484 (2024) https://doi.org/10.1016/j.phycom.2024.102484

[2] Guha Roy, B., Guha Roy, D., Datta, P., Bhatia Khan, S., Asiri, F., Ayadi, M.: Quality of service-aware 6g- enabled nb-iot for health monitoring in long distance high-speed trains. IEEE Transactions on Consumer Electronics 71(1), 1136–1147 (2025) https://doi.org/10.1109/TCE. 2025.3540197

[3] Chen, W., Ai, B., Sun, Y., Yu, C., Zhang, B., Yuen, C.: Advanced 6 g wireless communication technologies for intelligent high-speed railways. High-speed Railway 3(1), 78–92 (2025)

[4] Wu, Z., Zhao, J., Liu, X., Zhang, Q., Zhang, M., Tian, Y.: Intelligent communication and networking systems for future rail transit. Physical Communication, 103245 (2026)

[5] Pareit, D., Velde, E., Naudts, D., et al.: A novel network architecture for train-to-wayside communication with quality of service over heterogeneous wireless networks. EURASIP J. Wireless Commun. Netw. 2012, 114 (2012) https://doi. org/10.1186/1687-1499-2012-114

[6] Azab, A., Khasawneh, M., Alrabaee, S., Choo, K.-K.R., Sarsour, M.: Network trafic classifica tion: Techniques, datasets, and challenges. Digital Communications and Networks 10(3), 676– 692 (2024) https://doi.org/10.1016/j.dcan.2022. 09.009

[7] Lin, Y.-D., Lu, C.-N., Lai, Y.-C., Peng, W.-H., Lin, P.-C.: Application classification using packet size distribution and port association. Journal of Network and Computer Applications 32(5), 1023–1030 (2009) https://doi.org/10.1016/j.jnca. 2009.03.001 . Next Generation Content Networks

[8] Bujlow, T., Carela-Espa˜nol, V., Barlet-Ros, P.: Independent comparison of popular dpi tools for trafic classification. Computer Networks 76, 75–89 (2015) https://doi.org/10.1016/j.comnet. 2014.11.001

[9] Abdullah, D.M., Abdulazeez, A.M.: Machine learning applications based on svm classification a review. Qubahan Academic Journal 1(2), 81–90 (2021)

[10] Zhai, Y., Zheng, X.: Random forest based trafic classification method in sdn. In: 2018 International Conference on Cloud Computing, Big Data and Blockchain (ICCBB), pp. 1–5 (2018). https: //doi.org/10.1109/ICCBB.2018.8756496

[11] Manju, N., Harish, B.S., Prajwal, V.: Ensemble feature selection and classification of internet trafic using xgboost classifier, 37–44 (2019)

[12] Wang, W., Zhu, M., Wang, J., Zeng, X., Yang, Z.: End-to-end encrypted trafic classification with one-dimensional convolution neural networks. In: 2017 IEEE International Conference on Intelligence and Security Informatics (ISI), pp. 43–48 (2017). https://doi.org/10.1109/ISI.2017. 8004872

[13] Ullah, F., Ullah, S., Srivastava, G., Lin, J.C.- W.: Ids-int: Intrusion detection system using transformer-based transfer learning for imbalanced network trafic. Digital Communications and Networks 10(1), 190–204 (2024) https://doi. org/10.1016/j.dcan.2023.03.008

[14] Zheng, W., Zhong, J., Zhang, Q., Zhao, G.: Mtt: an eficient model for encrypted network trafic classification using multi-task transformer. Applied Intelligence 52(9), 10741–10756 (2022) https://doi.org/10.1007/s10489-021-03032-8

[15] Lin, X., Xiong, G., Gou, G., Li, Z., Shi, J., Yu, J.: Et-bert: A contextualized datagram representation with pre-training transformers for encrypted trafic classification. In: Proceedings of the ACM Web Conference 2022, pp. 633–642 (2022)

[16] Zhou, G., Guo, X., Liu, Z., Li, T., Li, Q., Xu, K.: Traficformer: an eficient pre-trained model for trafic data. In: 2025 IEEE Symposium on Security and Privacy (SP), pp. 1844–1860 (2025). IEEE

[17] Zhao, R., Zhan, M., Deng, X., Wang, Y., Wang, Y., Gui, G., Xue, Z.: Yet another trafic classifier: A masked autoencoder based trafic transformer with multi-level flow representation. In: Proceedings of the AAAI Conference on Artificial Intelligence, vol. 37, pp. 5420–5427 (2023)

[18] Lin, C., Zhang, W., Zuo, T., Zha, C., Jiang, Y., Meng, R., Luo, H., Meng, X., Zhang, Y.: Convolutions are competitive with transformers for encrypted trafic classification with pre-training. arXiv preprint arXiv:2508.02001 (2025)

[19] Chen, Q., He, D., Jin, Z., Ren, Z., Liu, T., Shan, S.: Msrnet-glam: A novel intrusion detection method for train communication network. Simulation Modelling Practice and Theory 138, 103040 (2025)

[20] Gao, B., Bu, B., Zhang, W., Li, X.: An intrusion detection method based on machine learning and state observer for train-ground communication systems. IEEE Transactions on Intelligent Transportation Systems 23(7), 6608–6620 (2021)

[21] Pan, S.J., Yang, Q.: A survey on transfer learning. IEEE Transactions on Knowledge and Data Engineering 22(10), 1345–1359 (2010) https:// doi.org/10.1109/TKDE.2009.191

[22] Yosinski, J., Clune, J., Bengio, Y., Lipson, H.: How transferable are features in deep neural networks? Advances in neural information processing systems 27 (2014)

[23] Hu, J., Shen, L., Sun, G.: Squeeze-and-excitation networks. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pp. 7132–7141 (2018)

[24] Zhao, J., Ren, R., Wu, Y., Zhang, Q., Xu, W., Wang, D., Fan, L.: Seattention-residual based channel estimation for mmwave massive mimo systems in iov scenarios. Digital Communications and Networks 11(3), 778–786 (2025) https://doi. org/10.1016/j.dcan.2024.04.005

[25] Lin, T.-Y., Goyal, P., Girshick, R., He, K., Doll´ar, P.: Focal loss for dense object detection. In: Pro ceedings of the IEEE International Conference on Computer Vision, pp. 2980–2988 (2017)

[26] Elkan, C.: The foundations of cost-sensitive learning. In: International Joint Conference on Artificial Intelligence, vol. 17, pp. 973–978 (2001). Lawrence Erlbaum Associates Ltd

[27] Draper-Gil, G., Lashkari, A.H., Mamun, M.S.I., Ghorbani, A.A.: Characterization of encrypted and vpn trafic using time-related features. In: Proceedings of the 2nd International Con ference on Information Systems Security and Privacy (ICISSP), pp. 407–414. SciTePress, Set´ubal, Portugal (2016). https://doi.org/10. 5220/0005740704070414

[28] Zhang, Q., Zhang, C., Zhao, J., Wang, D., Xu, W.: Dynamic resource allocation for multi-access edge computing in urban rail transit. IEEE Transactions on Vehicular Technology 74(2), 3296–3310 (2025) https://doi.org/10.1109/TVT. 2024.3479215

[29] Zhang, M., Wu, Z., Zhao, J., Zhang, Q., Tian, Y.: Multi-task intelligent scheduling for end-edgecloud collaboration in urban rail transit. Physical Communication, 103149 (2026)

[30] Wang, W., Zhu, M., Zeng, X., Ye, X., Sheng, Y.: Malware trafic classification using convolutional neural network for representation learning. In: 2017 International Conference on Information Networking (ICOIN), pp. 712–717 (2017). IEEE

[31] Ren, R., Wei, M., Zhao, J.: Lightweight lowsnr-robust semantic communication system for autonomous driving. Ad Hoc Networks 194, 104414 (2027) https://doi.org/10.1016/j.adhoc.

[32] Elmaghraby, R.T., Abdel Aziem, N.M., Sobh, M.A., Bahaa-Eldin, A.M.: Encrypted network trafic classification based on machine learning. Ain Shams Engineering Journal 15(2), 102361 (2024) https: //doi.org/10.1016/j.asej.2023.102361

[33] Huoh, T.-L., Luo, Y., Li, P., Zhang, T.: Flow-based encrypted network trafic classification with graph neural networks. IEEE Transactions on Network and Service Management 20(2), 1224–1237 (2023) https://doi.org/ 10.1109/TNSM.2022.3227500
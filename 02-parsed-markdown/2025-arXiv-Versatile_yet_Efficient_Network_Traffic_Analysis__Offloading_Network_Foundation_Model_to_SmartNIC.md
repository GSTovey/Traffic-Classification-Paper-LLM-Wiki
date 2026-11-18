# Versatile yet Efficient Network Traffic Analysis: Offloading Network Foundation Model to SmartNIC

Chungang Lin<sup>†‡</sup>, Xuying Meng<sup>†∗</sup>, Tianyu Zuo<sup>§x</sup>, Weiyao Zhang<sup>†</sup>, Meng Shen<sup>¶</sup>, Ruijie Zhao<sup>∥</sup>, Guanming Che<sup>‡‡</sup>, Ruiqi Meng<sup>‡</sup>, Ziyue Huang<sup>†‡</sup>, Haitong Luo<sup>†‡</sup>, Zhiwei Xu<sup>††</sup>, Yujun Zhang<sup>†‡∗</sup> <sup>†</sup>Institute of Computing Technology, Chinese Academy of Sciences, China.

<sup>‡</sup>University of Chinese Academy of Sciences, China.

<sup>§</sup>University of Virginia, USA. <sup>¶</sup>Beijing Institute of Technology, China. <sup>∥</sup>Southeast University, China.

<sup>‡‡</sup>Northeastern University, China. <sup>††</sup>Haihe Lab of ITAI, China. <sup>∗</sup>Corresponding authors

Abstract—Pervasive encryption makes large-scale labeling infeasible for traffic analysis, while security operations demand edge analysis to avert service degradation and further vulnerabilities. These pressures have produced two disjoint research lines: 1) versatile analysis, via network foundation models for low label dependency, and 2) efficient analysis, via hardware offloading for low analysis latency. However, versatility and efficiency have appeared fundamentally incompatible to co-achieve, with prior work consistently sacrificing one for the other, yet we show that this incompatibility is a consequence of polarized design choices across the three components of traffic analysis systems, i.e., traffic processing, model architecture, and analysis execution.

In response, we present Nepco, a versatile yet efficient network traffic analysis system that offloads network foundation models to SmartNIC. Our key observation is that discriminative traffic information is concentrated in localized byte regions, motivating versatile yet efficient localized byte-sequence modeling rather than inefficient global modeling. To exploit this without incurring the latency bottlenecks of complex encoding steps, we employ a hardware-friendly processing pipeline that directly embeds raw byte sequences. Crucially, to maintain versatility across diverse tasks characterized by spatially shifting features, we propose a pattern-aware convolutional architecture equipped with dedicated scoring and gating mechanisms. By exploiting translation invariance, this design dynamically locates and extracts salient semantic signatures irrespective of their byte-level offsets. We prototype Nepco on the Nvidia BlueField-3 SmartNIC with multiengine collaborative analysis execution. The experimental results demonstrate that Nepco achieves macro F1 competitive with the best performances achieved by 8 state-of-the-art network foundation models, while reducing end-to-end latency by 328× to the millisecond scale. With only 1% labels, Nepco outperforms existing hardware-offloadable models trained on 100% labels.

## I. INTRODUCTION

Network traffic analysis, which aims to uncover latent information from traffic, such as malware families and service types, underpins a broad range of security applications, including website fingerprinting [25], [101], intrusion detection [128], and malware family classification [27]. As today’s networks evolve, performing effective network traffic analysis has become increasingly challenging, driven by two compounding pressures. First, with over 95% of network traffic now encrypted [141], obtaining the large-scale ground-truth labels has become extremely difficult [105]. Second, modern security operations demand low-latency analysis at the network edge with constrained resources, before attacks cause visible service degradation and further security vulnerabilities [3], [4].

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/e1a78730d9ea15822162a8d3e481fceb6d49ea0ca90757bebec3b411449d6f90.jpg)  
Fig. 1: An illustration of the design space of existing solutions and Nepco. By resolving the three polarized design choices across the three components of traffic analysis systems, i.e., traffic processing, model architecture, and analysis execution, Nepco is able to achieve versatile yet efficient traffic analysis.

These two pressures have produced two lines of research in network traffic analysis, i.e., versatile analysis and efficient analysis. Versatile analysis aims for models that generalize across multiple security tasks with only limited labeled data [125]. Inspired by the success of the pre-training and finetuning paradigm in developing visual and large language mod els [26], [30], [45], [94], the network and security community has increasingly explored pre-training on large-scale unlabeled network traffic to develop network foundation models (e.g., [42], [68], [70], [91], [111], [125], [133], [135], [136], [138], to name a few), supporting multi-tasking by fine-tuning with limited labeled data. Efficient analysis, on the other hand, aims to enable low-latency analysis under constrained resources. Hardware offloading is a typical approach: it moves part or all of the analysis pipeline onto programmable hardware, such as programmable switches [50], SmartNICs [83], or FPGAs [5], enabling on-device analysis without host involvement [9], [29], [33]–[37], [71], [120], [130], [139].

However, versatility and efficiency have historically appeared incompatible, and prior work has documented sharp tradeoffs between the two. Naively deploying existing network foundation models (e.g., ET-BERT [68]) onto SmartNICs can incur second-scale inference latency [46], which is far above the sub-second budget that motivates hardware offloading [4]. Conversely, hardware-offloadable models cannot close the gap by simply scaling up training labels. Our measurement study in Section III shows that, even when trained on 140.01× more labeled flows, two state-of-the-art hardware-offloadable models (BoS [123] and Flowrest [1]) still lag behind two network foundation models (ET-BERT [68] and TrafficFormer [138]) by up to 54.17% in macro F1. These observations appear to confirm an incompatibility between versatility and efficiency, posing a critical obstacle for security-sensitive deployments, where defenders must detect threats and respond within tight latency budgets to prevent damage.

Yet a core question remains: “Is this incompatibility fundamental, or a consequence of the design choices each line has made?” We show that this incompatibility is not fundamental, but a consequence of polarized design choices across the three components of traffic analysis systems, i.e., traffic processing, model architecture, and analysis execution.

(1) Traffic Processing. Network foundation models adopt fine-grained semantic inputs that preserve transferable information but require computationally complex encoding, e.g., tokenization [68], [138], unfriendly to edge hardware; hardware-offloadable models, conversely, adopt coarse-grained statistical inputs that are cheap to construct but lose fine-grained information, requiring prolonged traffic observation to compensate.

(2) Model Architecture. Network foundation models mostly adopt expressive Transformer [108] architectures (e.g., BERT-style [68], [125], [138], MAE-style [42], [135]) whose quadratic computational complexity with respect to input sequence length precludes hardware inference; hardware-offloadable models adopt compact model architectures (e.g., Tree [52], Forest [139]), but with limited representational capacity and high label dependency.

(3) Analysis Execution. Network foundation models remain host-centric, gaining the flexibility of general-purpose compute platforms but paying substantial packet-delivery overhead before model inference; hardware-offloadable models stay hardware-centric, gaining line-rate packet processing but at the cost of restricting model inference to constrained hardware primitives.

At each component, each line gains its own strength by sacrificing the other’s. A system co-designed across the three components, in contrast, has the potential to achieve both.

To demonstrate this, in this paper, we present Nepco, a versatile yet efficient network traffic analysis system deployed on SmartNIC. As shown in Fig. 1, existing efforts either achieve efficiency at the cost of high label dependency (e.g., NetBeacon [139], BoS [123]), or achieve versatility at the cost of high analysis latency (e.g., TrafficFormer [138], MM4Flow [125]). Nepco is the first to achieve both. While a recent work [46] attempts to mitigate host-centric bottlenecks via hybrid deployment, it is forced to leave the foundation model inference on the host due to the severe computational complexity of existing models, and thus still incurs second-scale analysis latency. Nepco overcomes this barrier and resolves the polarizations in traffic processing, model architecture, and analysis execution through the following design and implementation:

We design an encoding-free early-stage traffic processing strategy that constructs model inputs from packet byte sequences and preserves fine-grained traffic semantics using byte embeddings. Such byte embeddings can be implemented as hardware table lookups, eliminating the computationally complex encoding steps (e.g., tokenization) required by existing network foundation models. Moreover, the fine-grained semantics preserved by the byte embeddings enable early-stage analysis from only the first few packets of a flow, unlike existing hardware-offloadable models that rely on coarse-grained statistical inputs and thus require prolonged traffic observation (up to 2048 packets [123], [139]). Additionally, prior work has raised evaluation validity concerns about address information leakage [90], [136]. We therefore zero out address-related protocol fields. As a concrete illustration, the macro F1 of Pcap-Encoder [136] changes from 0.5020 to 0.9008 depending on whether this step is applied (see Appendix A).

We design a convolution-based network foundation model that shifts to an O(n) localized and translation-invariant architecture to dynamically locate diverse discriminative byte patterns across different traffic categories. Specifically, while Transformers are the de facto choice for network foundation models, our analysis in Section IV-C reveals that discriminative network information is actually concentrated in localized byte regions. Nepco therefore forgoes the computationally expensive global attention of Transformers in favor of a convolution-based model architecture. We adopt depth-wise convolution [16] as the base operator for its hardware-friendly, channel-parallel computation. To overcome the limitation of standard convolutions that treat all bytes uniformly, we introduce window-wise byte scoring and sequence-wise byte gating to selectively emphasize informative bytes; we also design a continuous byte masking strategy for pre-training, directing the model to explicitly learn these localized traffic patterns.

We implement a prototype of Nepco on the NVIDIA BlueField-3 SmartNIC, and evaluate Nepco extensively with six network traffic analysis tasks. Nepco runs the analysis pipeline on-device by coordinating the programmable NIC hardware with the SoC cores. The NIC filters later-stage packets of already-analyzed flows at line rate, reducing the SoC’s processing load. On the SoC side, multi-engine collaborative execution handles input construction and model inference in parallel with asynchronous filter-rule updates back to the NIC, eliminating delays in updating the NIC filter rules. We further prototype three existing network foundation models [65], [68], [138] on the same SmartNIC for fair end-to-end comparison. The experimental results show that Nepco achieves macro F1 competitive with state-of-the-art network foundation models at millisecond-scale analysis latency, representing a 328× reduction compared with existing network foundation models.

The core contributions of this paper are three-fold:

• We show that the incompatibility between versatility and efficiency in network traffic analysis is not fundamental, but a consequence of the polarized design choices in prior.

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/3402a268dc8c10ec7615bdc514b367a753727e9fc210d6a798696870511e9305.jpg)  
Fig. 2: Conceptual decomposition of the network traffic analysis system into three core components, i.e., traffic processing, model architecture, and analysis execution, on which existing network foundation models and hardware-offloadable models make corresponding design choices to pursue versatile analysis and efficient analysis, respectively.

• We present Nepco, the first network foundation model that supports end-to-end hardware offloading, built on a convolution-based pre-trained model architecture for efficient localized byte-sequence modeling.

• We prototype Nepco on SmartNIC, and conduct extensive evaluations to validate its versatility and efficiency.

This work does not raise any ethical issues.

## II. BACKGROUND

## A. Network Traffic Analysis

Network traffic analysis aims to infer latent information from network traffic, such as malware families and service types, and is essential for network security and management [119], [125], [138]. It supports a broad range of security applications, including website fingerprinting [25], [101], malware classification [27], Internet of Things attack detection [61], and intrusion detection [128]. Several security companies, including ENEA [32], TrafficWiz [107], allot [2], and LiveAction [72], are actively developing network traffic analysis technologies. For instance, LiveAction applies machine learning to analyze encrypted network traffic, supporting threat detection and network monitoring without requiring decryption.

As shown in Fig. 2, the network traffic analysis system can be conceptually divided into three core components based on prior analysis pipelines [109], including 1. Traffic Processing, which converts captured raw network traffic into model inputs that satisfy system requirements; 2. Model Architecture, which is designed to capture different traffic characteristics from the model inputs, and thereby enable their transformation into final analysis outputs; and 3. Analysis Execution, which specifies the hardware platforms or devices on which these components are deployed and executed.

## B. Versatile Analysis with Foundation Models

Versatile analysis refers to a model’s ability to generalize across multiple downstream tasks while requiring only limited labeled data [92], [125]. For instance, MM4Flow [125] aims to obtain versatile network traffic representations to enhance multi-tasking capabilities. This capability is increasingly important because the widespread encryption of network traffic has made large-scale labeled data difficult. A 2024 report from Zscaler shows that 95% of network traffic is encrypted [141], while HCSS and HSD emphasize that labeling massive volumes of network traffic data is extremely time-consuming and difficult for human annotators [105].

The “pre-training and fine-tuning” paradigm has been shown in the natural language processing (NLP) and computer vision (CV) communities to be effective for developing foundation models that support multiple downstream tasks while substantially reducing the dependency on labeled data [8], [26], [30], [45], [58], [94], [95]. Motivated by this, our community has increasingly explored adapting the “pre-training and finetuning” paradigm to network traffic analysis, leading to the development of network foundation models capable of versatile analysis [38], [41], [42], [44], [62]–[66], [68], [70], [80], [90], [91], [93], [111], [124], [125], [133], [135], [136], [138]. Specifically, existing network foundation models first transform raw network traffic into semantically meaningful model inputs suitable for model learning, such as token [68], [80], [125], [138] or patch embeddings [42], [111], [135], and then typically adopt Transformer [108]-based model architectures (e.g., BERT-style [38], [65], [68], [91], [124], [138], GPT2- style [80], [93], MAE-style [42], [135], T5-style [77], [136]), because the self-attention mechanism in the Transformer has been widely proven to effectively capture global information in sequential data [108]. However, due to the Transformer’s quadratic computational complexity with respect to input sequence length [10], [15], current network foundation models are typically deployed on host-side CPU/GPU platforms.

Discussion: The rapid development of network foundation models also raises concerns about evaluation validity, particularly because address leakage (e.g., MAC address and IP address) may induce shortcut learning [90], [118], [136]. To ensure rigorous evaluation, we adopt the following safeguards. (1) Address information is zeroed out or removed in both pre training and fine-tuning to prevent the model from exploiting address-related cues. (2) The pre-training and fine-tuning datasets are kept strictly disjoint to avoid biased estimates of generalization. (3) The fine-tuning data are kept temporally later than the pre-training data to avoid temporal bias.

## C. Efficient Analysis with Hardware Offloading

Efficient analysis, i.e., low-latency network traffic analysis under constrained resource budgets, has long been a fundamental goal in our community [9], [29], [33]–[37], [71], [120], [130], [139]. This arises in operational security settings where the value of detection depends on whether the analysis-and-response loop can be completed before an attack causes visible service degradation [3], [4]. AWS reports that integrating DDoS mitigation with edge services can reduce time-to-mitigate from minutes to sub-second timescales [4]. The same requirement is now shaping data center security infrastructure [85], [87]. In NVIDIA’s public material on the BlueField series, the platform is presented through securityfacing deployments such as accelerating Suricata IDS/IPS, where packet steering and traffic inspection are offloaded from the host in order to improve analysis throughput while reducing compute overhead [83].

TABLE I: Comparison of labeled data dependency between network foundation models and hardware-offloadable models.

<table><tr><td rowspan="2" colspan="2">Methods</td><td colspan="4">Network Foundation Models</td><td colspan="4">Hardware-Offloadable Models</td></tr><tr><td colspan="2">ET-BERT [68]</td><td colspan="2">TrafficFormer [138]</td><td colspan="2">Flowrest [1]</td><td colspan="2">BoS [123]</td></tr><tr><td colspan="2">Setting of Labeled Flows</td><td>5000 Flows</td><td>All Flows</td><td>5000 Flows</td><td>All Flows</td><td>5000 Flows</td><td>All Flows</td><td>5000 Flows</td><td>All Flows</td></tr><tr><td rowspan="3">USTC-TFC (2016) [113]All / 5000 ≈ 3.53</td><td>Precision</td><td> $0.9525 \pm 0.0019$ </td><td> $0.9711 \pm 0.0024$ </td><td> $0.9489 \pm 0.0026$ </td><td> $0.9731 \pm 0.0033$ </td><td> $0.7015 \pm 0.0092$ </td><td> $0.8894 \pm 0.0102$ </td><td> $0.6070 \pm 0.0196$ </td><td> $0.8166 \pm 0.0205$ </td></tr><tr><td>Recall</td><td> $0.9511 \pm 0.0020$ </td><td> $0.9672 \pm 0.0023$ </td><td> $0.9471 \pm 0.0025$ </td><td> $0.9698 \pm 0.0038$ </td><td> $0.7049 \pm 0.0084$ </td><td> $0.8847 \pm 0.0094$ </td><td> $0.6245 \pm 0.0128$ </td><td> $0.8007 \pm 0.0217$ </td></tr><tr><td>Macro F1</td><td> $0.9509 \pm 0.0020$ </td><td> $0.9690 \pm 0.0024$ </td><td> $0.9469 \pm 0.0025$ </td><td> $0.9714 \pm 0.0034$ </td><td> $0.6869 \pm 0.0078$ </td><td> $0.8869 \pm 0.0099$ </td><td> $0.5737 \pm 0.0141$ </td><td> $0.8067 \pm 0.0211$ </td></tr><tr><td colspan="2">Average Performance Improvement</td><td>-</td><td>↑1.85%</td><td>-</td><td>↑2.51%</td><td>-</td><td>↑27.14%</td><td>-</td><td>↑34.45%</td></tr><tr><td colspan="2">Setting of Labeled Flows</td><td>5000 Flows</td><td>All Flows</td><td>5000 Flows</td><td>All Flows</td><td>5000 Flows</td><td>All Flows</td><td>5000 Flows</td><td>All Flows</td></tr><tr><td rowspan="3">CIC-IoMT (2024) [20]All / 5000 ≈ 140.01</td><td>Precision</td><td> $0.8373 \pm 0.0070$ </td><td> $0.8323 \pm 0.0081$ </td><td> $0.8313 \pm 0.0055$ </td><td> $0.8379 \pm 0.0075$ </td><td> $0.4372 \pm 0.0188$ </td><td> $0.7268 \pm 0.0198$ </td><td> $0.1249 \pm 0.0050$ </td><td> $0.3932 \pm 0.0074$ </td></tr><tr><td>Recall</td><td> $0.8223 \pm 0.0082$ </td><td> $0.8202 \pm 0.0090$ </td><td> $0.8261 \pm 0.0056$ </td><td> $0.8333 \pm 0.0081$ </td><td> $0.3914 \pm 0.0051$ </td><td> $0.7188 \pm 0.0192$ </td><td> $0.2382 \pm 0.0033$ </td><td> $0.4138 \pm 0.0090$ </td></tr><tr><td>Macro F1</td><td> $0.8187 \pm 0.0077$ </td><td> $0.8266 \pm 0.0085$ </td><td> $0.8235 \pm 0.0053$ </td><td> $0.8288 \pm 0.0077$ </td><td> $0.3767 \pm 0.0068$ </td><td> $0.7138 \pm 0.0195$ </td><td> $0.1434 \pm 0.0024$ </td><td> $0.3798 \pm 0.0082$ </td></tr><tr><td colspan="2">Average Performance Improvement</td><td>-</td><td>↑0.04%</td><td>-</td><td>↑0.77%</td><td>-</td><td>↑79.79%</td><td>-</td><td>↑151.13%</td></tr></table>

[114]), and resource-adaptive execution (e.g., early quit [23], [115] and dynamic serving [54], [109]). However, these techniques optimize individual pipeline components without eliminating the fundamental bottleneck of host-side execution. NVIDIA reports that host-side software optimizations still consume host CPU cycles, motivating line-rate offloading onto programmable hardware [83]. Non-offloading techniques are therefore insufficient on their own to sustain traffic analysis under production-scale traffic rates.

Hardware offloading is a mainstream approach to efficient network traffic analysis [9], [39], [123], [129], [131], [139], as it delivers high throughput and low latency by moving part or all of the analysis pipeline onto programmable hardware, such as FPGAs [5], programmable switches (P4 switches) [50], and System-on-Chip SmartNICs (SoC SmartNICs) [83]. Prior work [9], [71], [122], [130] initially offloads line-rate traffic processing, e.g., feature collection and summary statistics, to such hardware, while keeping learning-based analysis on the hardware control plane [9], [71] or the host side [122], [130]. More recent works further push model inference itself into FPGAs [35], [75], [82], [103], [106] and P4 switch data planes [1], [52], [121], [123], [131], [139], giving rise to intelligent network dataplanes that reduce cross-plane overhead and alleviate host-side CPU/GPU load. However, the tight constraints of programmable hardware in memory capacity, supported operators, and pipeline primitives force hardware-conscious co-design. As a result, existing works typically rely on readily available packet metadata (e.g., packet header fields) [35], [39], [121], [123], [131], [137] and lightweight flow statistics (e.g., packet length distribution) [52], [103], [106], [129], [132] as model inputs, and mostly adopt tree [52], [106], [121], [132]- or forest [1], [29], [139]-based model architectures. Shallow neural network-based approaches [103], [131], [137], e.g., binary neural network (BNN) [103], require aggressive quantization or structural rewriting, and higher-capacity deep neural networks (e.g., MAE [45]) still often rely on FPGA assistance [39] or end-host GPU collaboration [46].

Discussion: Beyond the hardware offloading, many nonoffloading approaches also pursue efficient network traffic analysis. Their techniques are aligned with the three components in Fig. 2, including traffic feature condensation (e.g., feature subset condensation [116], [117], key byte selection [12], [60]), compact model architecture (e.g., pruning [76], quantization [21], and knowledge distillation [47], [78],

## III. MOTIVATION

The primary goal is to enable versatile yet efficient network traffic analysis, driven by two practical requirements, i.e., the scarcity of large-scale labeled traffic under pervasive encryption and the low-latency constraints of real-world security operations. Prior work has made substantial progress along these two directions separately. Network foundation models advance versatility, whereas hardware offloading technologies advance efficiency. These two lines of work, however, polarize the design of the three core components of traffic analysis systems, i.e., traffic processing, model architecture, and analysis execution. In Fig. 2, we summarize the corresponding polarized design choices for the three core components. As a result, these polarizations make it challenging to achieve versatile yet efficient analysis.

Measurement Study. To further substantiate our analysis of these polarizations, we conduct a measurement study on label dependency. We select two network foundation models (i.e., ET-BERT [68] and TrafficFormer [138]) and two hardwareoffloadable models (i.e., Flowrest [1] and BoS [123]). Following prior work [65], [66], [68], [80], [138], we consider two labeling settings, 5000 flows and all flows, indicating the maximum number of labeled flows per class. For each flow, we only consider the first 5 packets in the flow to set up the early-stage analysis in existing works [65], [66], [68], [80], [125], [138]. We evaluate them on a 10-class malware classification task (on the USTC-TFC [113] dataset) and a 19-class Internet of Medical Things attack identification task (on the CIC-IoMT [20] dataset). To prevent the randomness caused by data sampling, we construct 20 sampled datasets for each task and each labeling setting using different random seeds and report the results with statistical analysis. We use precision, recall, and macro F1 as evaluation metrics.

Challenge 1: Polarization in Traffic Processing.

Driven by the different goals of versatility and efficiency, existing methods are pushed toward two distinct traffic processing strategies, i.e., fine-grained semantics and coarse-grained statistics. Network foundation models adopt fine-grained semantic inputs because such inputs preserve transferable traffic semantics beyond task-specific summary features, and can support early-stage analysis from limited observed traffic (e.g., first 5 packets in a flow [65], [68], [80], [138]). However, they require substantially more complex input encoding, e.g., word tokenization [68], [80], [138], n-gram construction [44], [65], [138], or image transformation [42], [111], [135].

In contrast, existing hardware-offloadable models rely on coarse-grained statistical inputs to keep traffic processing lightweight, low-latency, and simple to construct online, but such inputs require more traffic observation to accumulate sufficient information for high-accuracy analysis [39], [52], [123], [131], [139]. For example, models such as NetBeacon [139] and BoS [123] require continuous packet observation and repeated analysis result updates as more packets arrive (i.e., up to 2048 packets [139]), rather than making highaccuracy traffic analysis from only the first few packets. As shown in TABLE I, under the early-stage analysis setting on CIC-IoMT (using only the first 5 packets per flow), ET-BERT and TrafficFormer achieve macro F1 scores of 0.8187 and 0.8235 with 140.01× fewer labeled flows than BoS, which only reaches 0.3798 even when trained on the all labeledflow training set. This contrast suggests that, in the early-stage setting, additional labeled data offers limited compensation for the information loss inherent in the coarse-grained statistical input adopted by hardware-offloadable models.

Takeaway. Traffic processing is polarized, with fine-grained semantics enabling versatile analysis at the cost of complex input encoding, whereas coarse-grained statistics enable efficient analysis at the cost of prolonged traffic observation.

## Challenge 2: Polarization in Model Architectures.

Model architecture fundamentally shapes the analytical capability of the analysis systems [43], [57], [97], [110], [111]. In network traffic analysis, existing methods have gradually polarized toward two distinct architectural choices, i.e., expressive architectures and compact architectures. Network foundation models typically favor expressive architectures because they learn richer, more transferable traffic representations and therefore rely less on labeled data, albeit at a substantially higher computational cost. The Transformer [108] exemplifies this favor because its ability to capture global dependencies has made it central to network foundation models [38], [41], [44], [62]–[66], [68], [80], [90], [91], [93], [124], [125], [133], [136], [138], but its quadratic complexity with respect to input sequence length leads to inefficient model inference [10], [15].

By contrast, hardware-offloadable models adopt compact architectures to achieve low inference overhead and efficient deployment under resource constraints. This efficiency comes at the cost of weaker representation capacity and greater reliance on labeled data. For instance, NetBeacon [139] requires ∼ 2.6 million labeled training flows in P2P application fingerprinting tasks. Tree [52], [106], [121], [132]- and forest [1], [29], [139]-based architectures remain dominant in hardware-offloadable models. Although recent studies [103], [123], [131], [137] have explored shallow neural networks (e.g., BNN [103], RNN [123]) for hardware offloading, such models still require compression or structural transformation, such as conversion into table-matching logic on P4 switches [123], which often degrades analysis accuracy. As shown in TABLE I, two representative hardware-offloadable models, i.e., Flowrest (forest-based architecture) and BoS (RNN-based architecture), exhibit a strong dependence on labeled data. Specifically, increasing the number of labeled flows by 3.53× to 140.01× leads to average F1-score improvements of 53.47% for Flowrest and 92.80% for BoS.

Takeaway. Model architecture is polarized, with expressive architectures improving versatility but being computationally expensive, whereas compact architectures improve efficiency but depend more heavily on labeled data.

## Challenge 3: Polarization in Analysis Execution.

Analysis execution determines where packet processing and model inference are carried out in an analysis system. In current network traffic analysis systems, the pursuit of versatility and efficiency has led to two diverging execution choices, namely host-centric execution and hardware-centric execution. Network foundation models usually remain host-centric [68], [111], [125], [135], [138], because expressive model architectures (e.g., Transformer) benefit from flexible software environments and general-purpose compute resources. This execution choice, however, forces network packets to be exported from hardware to the host before inference, incurring substantial packet-delivery overhead even before analysis begins. SmartTC [46] shows that merely transferring 1 MB of traffic from the SmartNIC to the host incurs millisecond-level latency, while Google Cloud estimates that full packet mirroring at 100 Gbps can generate up to \$8,046 in daily network cost [18]. This cost is incurred before inference, showing that hostcentric execution preserves model inference flexibility at the expense of packet processing efficiency.

Hardware-offloadable models favor hardware-centric execution because it preserves low-latency packet processing. The cost is that model inference must conform to restricted hardware execution primitives, which directly limits its model inference flexibility. As a result, the original inference pipeline often cannot be preserved and must be further simplified or rewritten for hardware execution. As shown in TABLE I, when BoS is deployed on a P4 switch via table-matching logic, its macro F1 drops to only 0.3798 on the 19-class task of the CIC-IoMT dataset, far below the 0.9230 reported in its original 3-class task on the CIC-IoT dataset [19]. This result shows that hardware-centric execution preserves packet-processing efficiency only by restricting the flexibility of model inference. Takeaway. Analysis execution is polarized, with host-centric execution preserving inference flexibility at the cost of packet processing efficiency, whereas hardware-centric execution preserves processing efficiency at the cost of inference flexibility.

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/f9b59b0bb36b84a5bcdd04abb2c1309431043b3fca51d3c28083c4b31ef5563d.jpg)  
Fig. 3: The overview of Nepco.

## IV. DESIGN OF NEPCO

## A. Overview

We present Nepco, a versatile yet efficient network traffic analysis system natively deployed on SmartNIC. Achieving versatility and efficiency simultaneously is hindered by polarized design choices in three core components of traffic analysis, i.e., traffic processing, model architecture, and analysis execution. Nepco resolves these polarizations through three correspondingly designed components, as illustrated in Fig. 3. Early-Stage Encoding-Free Traffic Processing resolves the polarization in traffic processing with a hardware-friendly pipeline by constructing model inputs from raw packet byte sequences, eliminating the complex encoding steps (e.g., tokenization) required by existing network foundation models. We retain the fine-grained byte-level semantics necessary for versatile analysis while reducing input construction to lightweight memory operations, and further incorporate a laterstage packet filter that drops subsequent packets of alreadyanalyzed flows, reducing packet processing overhead. This design supports both early-stage analysis from the first few packets of a flow and unbiased traffic representation through address field zeroing. Details are presented in Section IV-B.

Localized Pattern-Aware Traffic Modeling resolves the polarization in model architecture by replacing the global attention in existing models with a localized convolution design, reducing computational complexity from $\mathcal { O } ( n ^ { 2 } )$ to O(n). Our key observation is that discriminative traffic information concentrates in localized byte regions rather than spreading across the full byte sequence. We exploit this locality through two mechanisms, i.e., a window-wise byte scoring that assigns an importance score to each byte within a sliding window, and a sequence-wise byte gating that selectively suppresses uninformative bytes across the full sequence. Together, these mechanisms enable the first convolution-based pre-trained network foundation model, which retains sufficient representational capacity for versatile analysis while remaining efficient inference on hardware. Details are presented in Section IV-C. SmartNIC Native Collaborative Execution resolves the polarization in analysis execution by enabling multi-engine collaborative execution across the NIC hardware and the SoC cores of the SmartNIC. The NIC enforcement engine performs line-rate packet filtering, forwarding unanalyzed packets to the packet processing engine, which maintains a per-flow packet pool and enqueues a flow for model inference. The traffic analysis engine on the SoC cores then executes the input construction and the model inference entirely on-device. Critically, the filter rule management engine asynchronously propagates model inference results back to the NIC as updated filter rules, enabling subsequent packets of analyzed flows to be filtered out at line rate without re-invoking the model. This collaborative design eliminates the packet delivery overhead of host-centric execution while preserving the full model inference flexibility. Details are presented in Section IV-D.

## B. Encoding-Free Early-Stage Traffic Processing

We construct model inputs directly from raw packet byte sequences, eliminating the complex encoding steps while preserving full byte-level semantics for versatile analysis. As shown in Fig. 3, this component enables early-stage analysis through packet collection and filtering, and constructs unbiased model inputs via address zeroing and packet concatenation.

Packet Collection and Filter. We collect the first µ packets of each flow for analysis. This is motivated by the observation that the first few packets of a flow already carry sufficient semantic information for accurate analysis, as consistently demonstrated by prior work [6], [7], [112], [126]. We set µ = 5 to align with this established setting [68], [80], [125], [138]. To reduce data processing overhead, we further incorporate the Later-Stage Packet Filter. Specifically, before processing each flow, we actively query the filter rules maintained by the NIC enforcement engine. Flows whose filter rules have already been written into the NIC, i.e., flows that have been analyzed by a prior inference, are filtered without further processing. This filtering step is effective because it decouples the data processing throughput from the total traffic volume; the processing overhead scales with the number of unanalyzed flows rather than the line rate, ensuring that the traffic processing operates only on flows that genuinely require analysis.

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/36aab57cfb5b69d6c7cd75a0e93275126fb033379f03c8ba9c98f209314df1b1.jpg)

(a) Packet from the RTSP BruteForce Category  
![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/68dc8a28148f9beefb9c024d65f727a27accf4b08a474889ff92c1887a51fec0.jpg)  
(b) Packet from the TCP Flood Category  
Fig. 4: Byte importance pattern analysis, showing the Top-5 important protocol fields. As visualizing all traffic samples is infeasible, two representative attack traffic categories (RTSP BruteForce and TCP Flood) on the CIC-IoT dataset are used for illustration, with comprehensive verification across diverse categories and datasets provided in Appendix B.

Unbiased Model Input Construction. For each collected flow, we construct an unbiased flat byte sequence as the model input through three sequential operations. First, address fields are zeroed out at the protocol field level, covering MAC addresses at the Ethernet layer, source/destination IP addresses at the network layer, and source/destination port numbers at the transport layer. This address zeroing is necessary because address information can induce shortcut learning in network foundation models [40], [90], [111], [134], [136], where the model exploits address-related cues rather than learning transferable traffic semantics, leading to biased generalization estimates. Appendix B provides empirical evidence for this. Retaining address fields inflates macro F1 by 5.19% on average, but once test-time address fields are randomized, macro F1 drops by 44.67% on average, confirming that the gains stem from shortcut learning rather than transferable traffic semantics. Second, each packet’s byte sequence is cropped to a fixed length of 128 bytes and zero-padded if shorter, normalizing the per-packet representation to a uniform size. Third, the processed byte sequences of all µ packets are concatenated in arrival order to form a single flat input of µ × 128 bytes, which is directly fed into the traffic modeling component. This concatenation preserves the inter-packet byte ordering that reflects the flow-level traffic semantics, and provides the contiguous traffic structure for traffic modeling.

## C. Localized Pattern-Aware Traffic Modeling

We build a convolution-based pre-trained network foundation model for versatile yet efficient traffic analysis. It is motivated by the observation that discriminative information in network traffic concentrates in localized byte regions, making localized convolution a more suitable architectural choice than global self-attention for inference efficiency.

1) Key Observation: To characterize how discriminative information is concentrated within network traffic, we apply GateKeeper [13], a byte-level attribution method that scores each byte’s contribution to the analysis decision. Fig. 4 illustrates the Top-5 important fields and their corresponding byte positions for two representative traffic categories (i.e., RTSP BruteForce and TCP Flood) on the CIC-IoT [19] dataset. We have the following observations that inform our design, and Appendix B further verifies that these observations generalize across both in-evaluation and out-of-evaluation datasets.

O1: Discriminative information is localized. As shown in Fig. 4, high-importance bytes concentrate in a small number of protocol field regions rather than spreading uniformly across the full byte sequence, indicating that discriminative information in network traffic forms salient semantic signatures that are inherently localized. Appendix B further validates this with right-skewed average Gini coefficients [48] ranging from 0.2961 to 0.4939 across both in-evaluation and out-ofevaluation datasets, indicating that such locality is a general property of network traffic.

O2: Different categories attend to different local regions. Comparing Fig. 4(a) and Fig. 4(b), the two categories concentrate their importance on distinct protocol fields. The RTSP BruteForce category attends primarily to transport-layer fields such as TCP.ack and TCP.seq, while the TCP Flood category attends to network-layer fields such as IP.id and IP.len. This spatial shift of salient semantic signatures across categories demonstrates that byte sequences carry sufficient information to distinguish different traffic categories, motivating a translation-invariant model architecture that locates them irrespective of their byte-level offsets. Appendix B further validates this with pairwise Jensen-Shannon Divergence [67] between per-class field distributions consistently above zero and concentrated at moderate-to-high values.

O3: Discriminative bytes are partial even within a field. Within each high-importance protocol field, only a subset of bytes receives notably high scores, while the remaining bytes in the same field contribute little to the analysis. This intra-field selectivity demonstrates that a standard convolution, treating all bytes equally, is insufficient and motivates selective emphasis on individual bytes. Appendix B further validates this with right-skewed average field-level Gini coefficients [48] ranging from 0.2907 to 0.4389 across diverse datasets.

O4: Address fields attract disproportionate importance. The Top-5 important fields consistently include address-related fields such as Ether.src and TCP.dport, which carry no transferable traffic semantics but receive disproportionately high importance scores. This confirms that address zeroing is necessary not only for evaluation validity but also for directing model learning toward discriminative content. Appendix B further validates this, showing that at least one address-related field appears in the Top-5 most important bytes for 88.16% to 96.75% of traffic samples across diverse datasets.

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/ca704597a60abae4e27e738f095ae5a3ab1df9c55b3de05d7b2c2b4709723a4e.jpg)  
Fig. 5: Architecture of the traffic modeling component.

2) Traffic Convolution Layer: The traffic convolution layer is the core building block of the traffic modeling component. Existing convolution-based traffic analysis methods either apply convolutions to statistical features [14], [89], [98], [99], losing byte-level semantics, or apply standard convolutions directly to raw byte sequences [28], [73], [74], [112], [113], [127], [140], which preserves byte-level information but treats all bytes equally. This uniform treatment is insufficient given the sparse and category-specific importance distribution.

Therefore, we adopt depth-wise convolution [16] as the base operator for its translation invariance, reduced parameter count, and channel-parallel computation pattern well-suited for hardware execution. As shown in Fig. 5, the layer consists of three sequential components. Byte embedding maps the byte sequence into a high-dimensional vector space for model learning. Window-wise byte scoring addresses the intrawindow selectivity in O3 by focusing on discriminative bytes within each local region. Sequence-wise byte gating addresses the sequence-level sparsity in O1 and O2 by suppressing uninformative byte positions across the full sequence.

Byte Embedding. The flat byte sequence consists of $\mu \times 1 2 8$ bytes. Every two consecutive bytes are grouped into one token, following the existing pre-training setting [65], [68], [138], yielding an input token sequence $X = ( t _ { 1 } , \ldots , t _ { N } )$ of length $N = \mu \times 6 4$ . Each token $t _ { i }$ is mapped to a high-dimensional embedding vector $\mathbf { e } _ { i }$ through a learned byte embedding layer, producing the embedding sequence $( \mathbf { e } _ { 1 } , \hdots , \mathbf { e } _ { N } )$

Unlike Transformer-based foundation models, we do not employ positional encoding, as the convolution operation implicitly encodes positional information through its local sliding-window structure. For hardware deployment, the embedding lookup can be implemented as a table-matching operation on programmable hardware, mapping each twobyte token directly to its pre-stored embedding vector and avoiding the large matrix multiplications required by other input representations [65], [68], [125], [138].

Window-wise Byte Scoring. Motivated by O3, window-wise byte scoring assigns a learnable importance score to each byte within the convolution window, enabling the model to selectively focus on the discriminative bytes within each local region rather than treating all bytes uniformly. The byte scores are fixed after training and can be pre-computed and stored as constants on the hardware, reducing the per-inference overhead of the scoring step to a simple weighted accumulation without runtime computation. For each sliding window of fixed length k at layer l, a set of layer-specific learnable weights $\mathbf { w } ^ { ( l ) } \in \bar { \mathbb { R } } ^ { k }$ is optimized to produce a score vector $\pmb { \alpha } ^ { ( l ) }$ , with $\sqrt { d }$ scaling to stabilize training across embedding dimensions:

$$
\alpha_ {i} ^ {(l)} = \frac {\exp (w _ {i} ^ {(l)} / \sqrt {d})}{\sum_ {j = 1} ^ {k} \exp (w _ {j} ^ {(l)} / \sqrt {d})}, i = 1, \ldots , k\tag{1}
$$

where $\alpha _ { i } ^ { ( l ) }$ represents the importance score assigned to the $i -$ th token within the window at layer l. The output embedding $\mathbf { h } _ { t } ^ { ( l ) }$ at position t is computed via depth-wise convolution:

$$
\mathbf {h} _ {t} ^ {(l)} = \sum_ {i = 1} ^ {k} \alpha_ {i} ^ {(l)} \cdot \mathbf {e} _ {t + i - 1} ^ {(l)}, t = 1, \ldots , N\tag{2}
$$

where $\mathbf { e } _ { t + i - 1 } ^ { ( l ) } \in \mathbb { R } ^ { d }$ denotes the input embedding at position t+i−1 at layer l. $( \mathbf { h } _ { 1 } ^ { ( l ) } , \ldots , \mathbf { h } _ { N } ^ { ( l ) } )$ is an intermediate embedding sequence that captures window-level localized patterns.

Sequence-wise Byte Gating. While window-wise byte scoring captures localized patterns within individual windows, certain discriminative patterns span multiple positions in the sequence and require sequence-level selectivity. Motivated by O1 and $\mathbf { O } 2 ,$ sequence-wise byte gating applies an adaptive gating mechanism [24] across the full sequence to emphasize informative byte positions and suppress uninformative ones. Formally, a parallel depth-wise convolution branch with independent learnable weights $\beta ^ { ( l ) } \in \mathbb { R } ^ { k }$ computes the gate for each position directly from the input embeddings, and the final output of the traffic convolution layer is:

$$
\mathbf {o} _ {i} ^ {(l)} = \mathbf {h} _ {i} ^ {(l)} \odot \sigma \left(\sum_ {j = 1} ^ {k} \beta_ {j} ^ {(l)} \cdot \mathbf {e} _ {i + j - 1} ^ {(l)}\right), \quad i = 1, \dots , N\tag{3}
$$

where $\sigma ( \cdot )$ is the sigmoid activation and $\odot$ is element-wise multiplication. The two branches $\mathbf { \alpha } _ { \alpha } ( l )$ and $\beta ^ { ( l ) }$ independently process $\mathbf { e } ^ { ( l ) }$ in parallel, serving as complementary selectivity mechanisms. The output sequence $( \mathbf { o } _ { 1 } ^ { ( \bar { l } ) } , \dots , \mathbf { o } _ { N } ^ { ( \bar { l } ) } )$ serves as the input $\mathbf { e } ^ { ( l + 1 ) }$ to the next traffic convolution layer.

3) Traffic Modeling: We adopt the pre-training and finetuning paradigm to learn generalizable traffic representations. Pre-training. We pre-train Nepco using a continuous byte masking-based pre-training task, in which contiguous spans of tokens are masked [55], and the model is trained to predict the original byte values from the surrounding context. Unlike standard random byte masking [68], [125], [138], which independently masks individual tokens, continuous byte masking explicitly trains the model to capture the structured byte patterns that correspond to protocol fields, which consist of contiguous bytes with fixed lengths and structures. Formally, a mask set $\mathcal { M } _ { \mathrm { m a s k } }$ is constructed by sampling a span length l from a geometric distribution, and the pre-training loss is:

$$
\mathcal {L} = - \frac {1}{| \mathcal {M} _ {\text { mask }} |} \sum_ {m \in \mathcal {M} _ {\text { mask }}} \log P _ {\theta} \left(t _ {m} \mid t _ {1} ^ {\text { mask }}, \dots , t _ {N} ^ {\text { mask }}\right)\tag{4}
$$

where $\theta$ is the model parameters and $t _ { i } ^ { \mathrm { m a s k } }$ is the masked token.

Fine-tuning. For downstream traffic analysis tasks, we conduct model fine-tuning with a task-specific classifier on a small set of labeled flows. A max pooling operation is applied over the full output sequence of the final traffic convolution layer to aggregate flow-level representations. Max pooling selects the peak activation across each feature dimension, which emphasizes the most discriminative local pattern signals in the byte sequence and is directly aligned with the design objective of capturing localized byte-level patterns. The pooled representation is then passed through a Multi-Layer Perceptron (MLP) head to produce the final analysis output.

## D. SmartNIC Native Collaborative Execution

Nepco offloads the network traffic analysis onto the Smart-NIC, advancing beyond prior work that offloads only traffic data processing while leaving model inference on the host side [46]. Four engines collaborate across the NIC and the SoC cores to realize this. The NIC enforcement engine filters laterstage packets at line rate on the NIC hardware. The packet processing engine accumulates per-flow packet bytes on the SoC cores and, once a flow reaches $\mu$ packets, simultaneously triggers the traffic analysis engine and the filter-rule management engine. The traffic analysis engine executes the input construction and the model inference on-device. The filterrule management engine asynchronously installs the inference result as a 5-tuple filter rule on the NIC, so that later-stage packets of the analyzed flow are filtered at line rate.

NIC Enforcement Engine. The NIC enforcement engine installs and enforces 5-tuple-based filter rules on the NIC hardware. Each arriving packet is matched against the filter rules; packets belonging to flows already analyzed by a prior inference are filtered directly at the NIC without entering the SoC processing path, while unmatched packets are forwarded to the RX queue. This design is effective because network foundation models achieve accurate analysis from only the first $\mu$ packets of a flow [68], [125], [138], making later-stage packets redundant for analysis purposes. Discarding them at line rate on the NIC therefore incurs no accuracy loss while eliminating unnecessary SoC-side processing overhead.

Packet Processing Engine. The packet processing engine is implemented on the SoC cores using DPDK [51], which provides polling-mode packet reception and lock-free data structures to sustain high-throughput packet processing without interrupt overhead [46], [123]. It maintains a per-flow packet pool indexed by a lock-free hash table keyed on the 5- tuple. For each packet received from the RX queue, it performs a flow lookup, copies 128 bytes of the packet into the flow’s byte buffer, and increments the per-flow packet counter. When the packet count of a flow reaches $\mu ,$ the engine simultaneously enqueues the flow entry to both the Infer Ring and the Filter Ring, triggering the traffic analysis engine and the filter-rule management engine concurrently. This parallel launch ensures that filter rule installation proceeds concurrently with model inference, minimizing the number of redundant packets that enter the SoC processing path before the filter rule takes effect.

Traffic Analysis Engine. The traffic analysis engine executes the complete inference pipeline on SmartNIC without host involvement. It dequeues flow entries from the Infer Ring, invokes the traffic processing to construct the model input from the accumulated byte buffer, and runs model inference via ONNX Runtime [81]. The resulting analysis result is written back to the flow entry as the final output. Unlike prior hardware offloading work that keeps model inference on the host side [46], the traffic analysis engine runs model inference entirely on-device, eliminating the packet delivery overhead that is otherwise incurred before inference even begins.

Filter-Rule Management Engine. The filter-rule management engine runs on a SoC core, operating asynchronously from the traffic analysis engine. It continuously drains the Filter Ring and, for each dequeued flow entry, constructs a 5-tuple filter rule and updates it on the NIC hardware. Unlike a synchronous design where rule update would block the model inference path, the asynchronous engine fully decouples NIC hardware communication from model inference, ensuring that the latency of rule update does not affect model analysis latency. Combined with the parallel launch from the packet processing engine, this design minimizes the end-to-end window between the first packet of a flow and the moment its subsequent packets are filtered at line rate on the NIC.

## V. EXPERIMENTS

We prototype Nepco in both software and hardware, and evaluate it extensively on six public network traffic datasets, including 83 different traffic categories, against 17 baselines covering traditional ML/DL models, hardware-offloadable models, and network foundation models. In general, the experiments demonstrate that Nepco is able to:

1) achieve overall classification performance competitive with state-of-the-art network foundation models under limited labeled data, while significantly reducing label dependency compared with existing hardware-offloadable models (Section V-B).

2) reduce the analysis latency of existing network foundation models from second-scale to millisecond-scale under hardware deployment, while preserving nanosecond-scale input construction and microsecond-scale queue wait latency (Section V-C).

3) validate the effectiveness of the localized pattern-aware traffic modeling over traffic byte sequences, achieving simultaneous improvements in both classification performance and analysis latency over existing convolutionbased methods (Section V-D).

## A. Experiment Setup

Implementation. We develop both software and hardware prototypes of Nepco. The software prototype follows the same deployment setting as existing network foundation models, running on an end-host server equipped with an NVIDIA H800 GPU [88] and an Intel Xeon Platinum 8458P CPU [49]. We implement the traffic modeling component using PyTorch (v2.3.0 for CUDA v12.4). The hardware prototype is implemented on an NVIDIA BlueField-3 SmartNIC [84], whose NIC is based on ConnectX-7 [86]. We leverage the programmability of the NIC hardware to implement the NIC enforcement engine. The SoC is equipped with 16 cores, which we allocate across the four engines to maximize throughput while ensuring real-time responsiveness. Specifically, 13 cores are dedicated to the traffic analysis engine to parallelize input construction and model inference across concurrent flows, 1 core is assigned to the packet processing engine, and 1 core to the filter-rule management engine. The remaining core is reserved to coordinate inter-engine communication and prevent resource exhaustion. For both prototypes of Nepco, we configure the traffic modeling component with a byte embedding size of 128, a kernel size of 4 in the traffic convolution layer, and a stack of 5 consecutive traffic convolution layers.

TABLE II: Datasets for pre-training and fine-tuning.

<table><tr><td>Dataset</td><td>Year</td><td>Flows</td><td>Pre-train</td><td>Fine-tune</td></tr><tr><td>Bottlenet-HTTPS [100]</td><td>2016</td><td>610,161</td><td>√</td><td>✗</td></tr><tr><td>ISCX-SlowDoS [53]</td><td>2016</td><td>176,211</td><td>√</td><td>✗</td></tr><tr><td>USTC-TFC [113]</td><td>2016</td><td>179,252</td><td>✗</td><td>√ 10-classMalware Family Classification</td></tr><tr><td>ISCX-VPN-App [31]</td><td>2016</td><td>292,922</td><td>✗</td><td>√ 17-classApplication Classification</td></tr><tr><td>ISCX-VPN-Service [31]</td><td>2016</td><td>101,354</td><td>✗</td><td>√ 12-classService Type Identification</td></tr><tr><td>DataCon [22]</td><td>2021</td><td>60,509</td><td>✗</td><td>√ 10-classEncrypted Proxy Identification</td></tr><tr><td>CIC-EVSE [11]</td><td>2024</td><td>2,743,495</td><td>✗</td><td>√ 15-classEVSE Intrusion Classification</td></tr><tr><td>CIC-IoMT [20]</td><td>2024</td><td>6,998,544</td><td>✗</td><td>√ 19-classIoMT Intrusion Classification</td></tr></table>

Testbed. We use a testbed with two servers directly connected with a 200Gbps link, each equipped with a 5.4GHz Intel Core i7-14700 CPU, 64GB DRAM, and a NVIDIA BlueField-3 SmartNIC. We generate traffic in one server (sender) and deploy Nepco on the other server (receiver). We implement two traffic generation methods targeting different evaluation scenarios. For real and continuous latency evaluation, we use DPDK to generate traffic based on packet length and inter-packet interval distributions collected from backbone networks, faithfully reflecting real-world network conditions. We acknowledge that direct deployment in a production environment is infeasible due to privacy and access constraints; the use of distribution-matched synthetic traffic is a standard methodology in prior work [35], [46], [103]. For latency evaluation under diverse network load, we use TCP raw sockets [79] to manually construct IP/TCP headers under controlled New Flow Per Second (NFPS) settings. We estimate a realistic baseline load based on prior measurements. Meta [96] reported in 2015 that its external-facing web servers observe 500 NFPS at the median, and Cisco [17] measured a 3× growth in Internet traffic from 2016 to 2021, suggesting 2,000 NFPS as a reasonable network load for practical deployments. Accordingly, we consider four network load settings, i.e., Extreme Low (NFPS = 5), Low (NFPS = 500), Normal (NFPS = 2,000), and High (NFPS = 5,000), during our evaluation.

Pre-training. We pre-train Nepco on two public network traffic datasets, i.e., Bottlenet-HTTPS [100] and ISCX-SlowDoS [53], comprising 786,372 flows in total, as summarized in TABLE II. Both datasets were collected in 2016 and are kept strictly disjoint from all fine-tuning datasets to avoid biased estimates of generalization, following the evaluation safeguards described in Section II-B. The pre-training runs for 100,000 steps with a learning rate of $1 \times 1 0 ^ { - 3 }$

Fine-tuning. We fine-tune and evaluate Nepco spanning three security analysis tasks, including malware analysis, application fingerprinting, and intrusion detection, as shown in TABLE II. For malware analysis, we evaluate on USTC-TFC [113] to perform fine-grained malware family classification across 10 classes. For application fingerprinting, we evaluate on ISCX-VPN-App [31], ISCX-VPN-Service [31], and DataCon [22] to cover three distinct fingerprinting scenarios, i.e., application classification, service type identification, and encrypted proxy identification, comprising 39 classes in total. For intrusion detection, we evaluate on CIC-EVSE [11] and CIC-IoMT [20] to perform fine-grained intrusion classification across two emerging IoT deployment scenarios, i.e., EV charging stations and IoMT devices. For each fine-tuning dataset, we split the data into training, validation, and test sets at a ratio of 8:1:1, and construct 20 sampled subsets using different random seeds for statistical significance analysis. The fine-tuning runs for 10 epochs with a learning rate of $5 \times 1 0 ^ { - 4 }$

Baselines. We compare Nepco with 17 baselines, including traditional ML/DL models, hardware-offloadable models, and network foundation models, as shown in TABLE III. Unlike our method, existing methods cannot achieve versatile yet efficient traffic analysis. To measure the end-to-end analysis latency of existing network foundation models on SmartNICs, we deploy them onto the same hardware prototype under Nepco’s deployment scheme, with only the traffic processing and model architecture varying across baselines. For existing hardware-offloadable models, since most are designed for FPGAs [35], [103] or P4 switches [1], [52], [121], [123], we implement their software prototypes with corresponding opensource codes to evaluate versatility on the host CPU. Since Nepco is a convolution-based network foundation model, we further consider 4 traditional convolution-based methods [56], [59], [102], [104] to validate the effectiveness of Nepco design. Metrics. We primarily utilize precision, recall, and macro F1 as evaluation metrics, as they are well-suited for reflecting model performance across multi-class analysis tasks and are widely adopted in existing studies [125], [138]. All metrics are computed using Macro Averaging [69] to prevent biased evaluation caused by class imbalance across traffic categories.

## B. Versatility Evaluation

Overall Classification Performance. Compared to existing network foundation models, Nepco achieves consistently competitive performance across all six traffic analysis tasks, as shown in TABLE III, where bold red denotes the best performance among existing network foundation models and bold blue denotes the best among existing hardware-offloadable models. On DataCon, CIC-EVSE, CIC-IoMT, and USTC-

TABLE III: The overall classification performances of Nepco and baselines on six public network traffic datasets.

$$
\mathrm{MacroF1}
$$

$$
0. 0 2 8 9 \pm 0. 0 0 0 2
$$

$$
0. 2 3 7 9 \pm 0. 0 4 6 1
$$

$$
0. 6 4 5 4 \pm 0. 0 0 7 8
$$

$$
0. 4 8 8 1 \pm 0. 0 2 0 3
$$

$$
0. 8 2 0 8 \pm 0. 0 0 5 7
$$

$$
0. 8 1 3 0 \pm 0. 0 0 7 6
$$

$$
0. 6 4 1 2 \pm 0. 0 0 7 8
$$

$$
0. 3 0 4 2 \pm 0. 0 1 1 9
$$

$$
0. 8 0 8 0 \pm 0. 0 0 5 4
$$

$$
0. 6 2 9 0 \pm 0. 0 0 5 4
$$

$$
0. 6 3 1 3 \pm 0. 0 1 0 8
$$

$$
0. 3 8 9 1 \pm 0. 0 0 6 7
$$

$$
0. 6 2 1 5 \pm 0. 0 1 0 2
$$

$$
0. 4 5 1 2 \pm 0. 0 2 6 3
$$

$$
0. 4 3 1 5 \pm 0. 0 1 2 2
$$

$$
0. 5 8 3 9 \pm 0. 0 2 5 1
$$

$$
0. 6 1 8 1 \pm 0. 0 0 8 4
$$

$$
0. 4 1 3 5 \pm 0. 0 1 2 3
$$

$$
0. 5 9 8 1 \pm 0. 0 0 5 7
$$

$$
0. 4 2 1 1 \pm 0. 0 1 0 6
$$

$$
0. 5 8 1 5 \pm 0. 0 1 6 7
$$

$$
0. 3 7 2 0 \pm 0. 0 1 9 4
$$

$$
0. 3 7 1 8 \pm 0. 0 2 1 8
$$

$$
0. 7 8 9 2 \pm 0. 0 0 5 9
$$

$$
0. 4 3 7 2 \pm 0. 0 1 8 8
$$

$$
0. 8 0 0 8 \pm 0. 0 0 4 1
$$

$$
0. 3 9 1 4 \pm 0. 0 0 5 1
$$

$$
0. 4 9 2 9 \pm 0. 0 1 3 5
$$

$$
0. 3 6 0 4 \pm 0. 0 1 2 7
$$

$$
0. 3 4 3 5 \pm 0. 0 2 2 9
$$

$$
0. 4 9 1 7 \pm 0. 0 0 7 7
$$

$$
0. 9 5 0 1 \pm 0. 0 1 9 9
$$

$$
0. 9 6 9 5 \pm 0. 0 0 9 7
$$

$$
0. 4 9 6 4 \pm 0. 0 0 3 4
$$

$$
0. 3 1 8 1 \pm 0. 0 1 7 8
$$

$$
0. 3 6 1 4 \pm 0. 0 1 7 3
$$

$$
0. 4 3 9 8 \pm 0. 0 0 2 8
$$

$$
0. 8 2 3 8 \pm 0. 0 2 8 6
$$

$$
0. 4 5 1 8 \pm 0. 0 1 1 0
$$

$$
0. 8 2 6 7 \pm 0. 0 2 0 8
$$

$$
0. 8 0 2 8 \pm 0. 0 2 1 0
$$

$$
0. 3 9 2 5 \pm 0. 0 0 3 7
$$

$$
0. 3 0 5 5 \pm 0. 0 0 8 9
$$

$$
0. 3 4 9 7 \pm 0. 0 0 4 2
$$

$$
0. 8 2 8 9 \pm 0. 0 1 3 9
$$

$$
0. 1 3 9 2 \pm 0. 0 0 8 6
$$

$$
0. 3 5 5 4 \pm 0. 0 2 1 6
$$

$$
0. 7 7 6 0 \pm 0. 0 0 7 4
$$

$$
0. 2 3 2 2 \pm 0. 0 1 3 5
$$

$$
0. 1 3 7 8 \pm 0. 0 0 7 0
$$

$$
0. 7 6 7 1 \pm 0. 0 0 7 7
$$

$$
0. 2 3 8 2 \pm 0. 0 0 3 3
$$

$$
0. 1 4 3 4 \pm 0. 0 0 2 4
$$

$$
0. 9 8 7 0 \pm 0. 0 0 6 3
$$

$$
0. 8 1 3 8 \pm 0. 0 0 9 9
$$

$$
0. 7 6 6 6 \pm 0. 0 0 6 0
$$

$$
0. 9 8 2 1 \pm 0. 0 0 4 2
$$

$$
0. 7 6 0 1 \pm 0. 0 0 6 2
$$

$$
0. 4 6 4 5 \pm 0. 1 5 5 2
$$

$$
0. 8 1 2 0 \pm 0. 0 0 4 7
$$

$$
0. 5 8 5 5 \pm 0. 0 0 4 7
$$

$$
0. 5 8 9 6 \pm 0. 0 0 6 0
$$

$$
0. 7 5 3 1 \pm 0. 0 1 0 0
$$

$$
0. 7 5 1 1 \pm 0. 0 0 8 9
$$

$$
0. 4 3 0 2 \pm 0. 0 3 3 9
$$

$$
\mathbf {0 . 9 9 2 7 \pm 0 . 0 0 1 8}
$$

$$
0. 7 5 2 0 \pm 0. 0 1 8 7
$$

$$
0. 9 9 0 2 \pm 0. 0 0 3 3
$$

$$
0. 4 4 7 6 \pm 0. 0 2 8 2
$$

$$
0. 8 5 8 8 \pm 0. 0 2 4 7
$$

$$
0. 4 0 5 1 \pm 0. 0 3 2 0
$$

$$
0. 7 1 7 1 \pm 0. 0 1 5 1
$$

$$
0. 9 9 1 4 \pm 0. 0 0 1 6
$$

$$
0. 9 8 7 2 \pm 0. 0 0 3 2
$$

$$
0. 9 8 9 0 \pm 0. 0 0 2 0
$$

$$
0. 5 3 4 4 \pm 0. 0 1 3 9
$$

$$
0. 8 4 9 6 \pm 0. 0 2 3 3
$$

$$
0. 8 6 2 2 \pm 0. 0 2 4 5
$$

$$
0. 8 4 6 3 \pm 0. 0 2 3 1
$$

$$
0. 9 9 0 0 \pm 0. 0 0 2 4
$$

$$
0. 9 9 2 0 \pm 0. 0 0 2 1
$$

$$
0. 8 2 1 0 \pm 0. 0 0 4 5
$$

$$
\mathbf {0 . 9 9 0 8 \pm 0 . 0 0 1 7}
$$

$$
0. 5 6 3 2 \pm 0. 0 0 5 7
$$

$$
\mathbf {0 . 8 7 1 2} \pm 0. 0 2 1 7
$$

$$
\mathbf {0 . 8 5 8 8} \pm 0. 0 2 2 4
$$

$$
0. 8 5 9 4 \pm 0. 0 2 0 3
$$

$$
0. 9 8 8 5 \pm 0. 0 0 2 1
$$

$$
0. 9 9 1 1 \pm 0. 0 0 2 5
$$

$$
0. 8 2 6 7 \pm 0. 0 0 6 7
$$

$$
0. 9 8 8 1 \pm 0. 0 0 2 3
$$

$$
0. 8 1 7 5 \pm 0. 0 0 6 9
$$

$$
0. 8 6 3 1 \pm 0. 0 2 0 8
$$

$$
0. 8 3 4 3 \pm 0. 0 1 1 4
$$

$$
0. 8 5 1 9 \pm 0. 0 1 9 8
$$

$$
0. 9 8 5 5 \pm 0. 0 0 4 5
$$

$$
0. 9 9 1 4 \pm 0. 0 0 3 1
$$

$$
0. 9 8 8 1 \pm 0. 0 0 3 4
$$

$$
\mathbf {0 . 8 3 7 3 \pm 0 . 0 0 7 0}
$$

$$
0. 8 2 1 9 \pm 0. 0 1 8 7
$$

$$
0. 8 5 5 5 \pm 0. 0 1 9 6
$$

$$
0. 8 1 0 4 \pm 0. 0 0 8 8
$$

$$
0. 8 2 2 0 \pm 0. 0 1 9 1
$$

$$
0. 8 1 4 4 \pm 0. 0 0 5 5
$$

$$
\underline {{0 . 9 9 0 9 \pm 0 . 0 0 1 5}}
$$

$$
0. 8 5 8 0 \pm 0. 0 1 9 5
$$

$$
\underline {{0 . 9 9 2 1 \pm 0 . 0 0 0 9}}
$$

$$
\underline {{0 . 9 9 1 4 \pm 0 . 0 0 0 9}}
$$

$$
0. 8 2 5 4 \pm 0. 0 0 7 7
$$

$$
0. 8 4 8 3 \pm 0. 0 1 9 4
$$

$$
\underline {{0 . 8 9 2 2 \pm 0 . 0 1 5 9}}
$$

$$
0. 8 2 2 3 \pm 0. 0 0 8 2
$$

$$
\underline {{0 . 8 8 9 9 \pm 0 . 0 1 2 8}}
$$

$$
\underline {{0 . 8 8 3 8 \pm 0 . 0 1 2 2}}
$$

$$
0. 8 0 7 6 \pm 0. 0 0 9 8
$$

$$
0. 8 3 1 3 \pm 0. 0 0 5 5
$$

$$
\underline {{0 . 8 3 8 9 \pm 0 . 0 0 4 1}}
$$

$$
0. 8 1 7 4 \pm 0. 0 0 3 5
$$

$$
0. 8 1 8 7 \pm 0. 0 0 7 7
$$

$$
0. 8 2 6 1 \pm 0. 0 0 5 6
$$

$$
0. 8 1 7 7 \pm 0. 0 0 6 6
$$

$$
\underline {{0 . 8 2 9 1 \pm 0 . 0 0 6 1}}
$$

$$
\mathbf {0 . 8 2 3 5} \pm 0. 0 0 5 3
$$

$$
\underline {{0 . 8 3 4 1 \pm 0 . 0 0 5 2}}
$$

<table><tr><td rowspan="2" colspan="2">Method</td><td colspan="3">ISCX-VPN-App (2016)</td><td colspan="3">ISCX-VPN-Service (2016)</td><td colspan="3">USTC-TFC (2016)</td></tr><tr><td>Precision</td><td>Recall</td><td>Macro F1</td><td>Precision</td><td>Recall</td><td>Macro F1</td><td>Precision</td><td>Recall</td><td>Macro F1</td></tr><tr><td rowspan="9">ML/DL Models√: Hardware-Offloadable</td><td>FlowPrint</td><td> $0.5959 \pm 0.0139$ </td><td> $0.4115 \pm 0.0112$ </td><td> $0.4334 \pm 0.0140$ </td><td> $0.7166 \pm 0.0215$ </td><td> $0.6860 \pm 0.0187$ </td><td> $0.6638 \pm 0.0181$ </td><td> $0.6764 \pm 0.0158$ </td><td> $0.6693 \pm 0.0135$ </td><td> $0.6636 \pm 0.0141$ </td></tr><tr><td>AppScanner</td><td> $0.7394 \pm 0.0096$ </td><td> $0.5439 \pm 0.0098$ </td><td> $0.5873 \pm 0.0099$ </td><td> $0.8567 \pm 0.0079$ </td><td> $0.7586 \pm 0.0080$ </td><td> $0.7897 \pm 0.0071$ </td><td> $0.8377 \pm 0.0049$ </td><td> $0.6408 \pm 0.0044$ </td><td> $0.6966 \pm 0.0043$ </td></tr><tr><td>XGBoost</td><td> $0.5177 \pm 0.0104$ </td><td> $0.4151 \pm 0.0050$ </td><td> $0.4304 \pm 0.0057$ </td><td> $0.7094 \pm 0.0033$ </td><td> $0.7160 \pm 0.0036$ </td><td> $0.7032 \pm 0.0029$ </td><td> $0.9438 \pm 0.0013$ </td><td> $0.9435 \pm 0.0014$ </td><td> $0.9434 \pm 0.0014$ </td></tr><tr><td>DTree</td><td> $0.4844 \pm 0.0056$ </td><td> $0.4483 \pm 0.0050$ </td><td> $0.4462 \pm 0.0047$ </td><td> $0.7026 \pm 0.0030$ </td><td> $0.7090 \pm 0.0027$ </td><td> $0.6997 \pm 0.0023$ </td><td> $0.9411 \pm 0.0010$ </td><td> $0.9299 \pm 0.0035$ </td><td> $0.9280 \pm 0.0040$ </td></tr><tr><td>Flowrest √</td><td> $0.2983 \pm 0.0136$ </td><td> $0.2350 \pm 0.0050$ </td><td> $0.2278 \pm 0.0061$ </td><td> $0.5263 \pm 0.0205$ </td><td> $0.4572 \pm 0.0100$ </td><td> $0.4429 \pm 0.0111$ </td><td> $0.7015 \pm 0.0092$ </td><td> $0.7049 \pm 0.0084$ </td><td> $0.6869 \pm 0.0078$ </td></tr><tr><td>Leo √</td><td> $0.1839 \pm 0.0083$ </td><td> $0.2645 \pm 0.0043$ </td><td> $0.1543 \pm 0.0029$ </td><td> $0.4105 \pm 0.0048$ </td><td> $0.5097 \pm 0.0065$ </td><td> $0.4193 \pm 0.0057$ </td><td> $0.8268 \pm 0.0035$ </td><td> $0.8130 \pm 0.0028$ </td><td> $0.8104 \pm 0.0026$ </td></tr><tr><td>Mousika √</td><td> $0.4849 \pm 0.0154$ </td><td> $0.3221 \pm 0.0061$ </td><td> $0.3370 \pm 0.0070$ </td><td> $0.6336 \pm 0.0179$ </td><td> $0.4523 \pm 0.0058$ </td><td> $0.4545 \pm 0.0070$ </td><td> $0.7291 \pm 0.0111$ </td><td> $0.7118 \pm 0.0013$ </td><td> $0.6615 \pm 0.0018$ </td></tr><tr><td>EBSNN</td><td> $0.7154 \pm 0.0107$ </td><td> $0.6560 \pm 0.0081$ </td><td> $0.6620 \pm 0.0086$ </td><td> $0.8945 \pm 0.0054$ </td><td> $0.8757 \pm 0.0070$ </td><td> $0.8804 \pm 0.0054$ </td><td> $0.9020 \pm 0.0071$ </td><td> $0.8780 \pm 0.0120$ </td><td> $0.8667 \pm 0.0156$ </td></tr><tr><td>BoS √</td><td> $0.2473 \pm 0.0140$ </td><td> $0.2549 \pm 0.0069$ </td><td> $0.2161 \pm 0.0061$ </td><td> $0.4865 \pm 0.0225$ </td><td> $0.4594 \pm 0.0170$ </td><td> $0.4230 \pm 0.0181$ </td><td> $0.6070 \pm 0.0196$ </td><td> $0.6245 \pm 0.0128$ </td><td> $0.5737 \pm 0.0141$ </td></tr><tr><td rowspan="8">Network Foundation Models√: Hardware-Offloadable</td><td>NetMamba</td><td> $0.6834 \pm 0.0163$ </td><td> $0.5984 \pm 0.0110$ </td><td> $0.6164 \pm 0.0122$ </td><td> $0.8421 \pm 0.0045$ </td><td> $0.7950 \pm 0.0040$ </td><td> $0.8030 \pm 0.0033$ </td><td> $0.9655 \pm 0.0015$ </td><td> $0.9631 \pm 0.0012$ </td><td> $0.9628 \pm 0.0013$ </td></tr><tr><td>YaTC</td><td> $0.6531 \pm 0.0166$ </td><td> $0.5764 \pm 0.0097$ </td><td> $0.5845 \pm 0.0116$ </td><td> $0.8331 \pm 0.0045$ </td><td> $0.7854 \pm 0.0042$ </td><td> $0.7937 \pm 0.0031$ </td><td> $0.9644 \pm 0.0009$ </td><td> $0.9605 \pm 0.0015$ </td><td> $0.9600 \pm 0.0017$ </td></tr><tr><td>Pcap-Encoder</td><td> $0.2951 \pm 0.0312$ </td><td> $0.3060 \pm 0.0231$ </td><td> $0.2813 \pm 0.0255$ </td><td> $0.5357 \pm 0.0504$ </td><td> $0.5203 \pm 0.0355$ </td><td> $0.5020 \pm 0.0397$ </td><td> $0.9298 \pm 0.0090$ </td><td> $0.9232 \pm 0.0105$ </td><td> $0.9228 \pm 0.0108$ </td></tr><tr><td>PERT</td><td> $0.7166 \pm 0.0089$ </td><td> $0.7004 \pm 0.0073$ </td><td> $0.7003 \pm 0.0067$ </td><td> $0.9146 \pm 0.0033$ </td><td> $0.9104 \pm 0.0020$ </td><td> $0.9115 \pm 0.0020$ </td><td> $0.9345 \pm 0.0022$ </td><td> $0.9337 \pm 0.0023$ </td><td> $0.9337 \pm 0.0023$ </td></tr><tr><td>NetGPT</td><td> $0.7222 \pm 0.0065$ </td><td> $0.7226 \pm 0.0097$ </td><td> $0.7154 \pm 0.0091$ </td><td> $0.9211 \pm 0.0028$ </td><td> $0.9196 \pm 0.0019$ </td><td> $0.9190 \pm 0.0014$ </td><td> $0.9607 \pm 0.0017$ </td><td> $0.9597 \pm 0.0017$ </td><td> $0.9596 \pm 0.0017$ </td></tr><tr><td>ET-BERT</td><td> $0.7352 \pm 0.0096$ </td><td> $0.7103 \pm 0.0092$ </td><td> $0.7125 \pm 0.0081$ </td><td> $0.9225 \pm 0.0025$ </td><td> $0.9236 \pm 0.0023$ </td><td> $0.9224 \pm 0.0020$ </td><td> $0.9525 \pm 0.0019$ </td><td> $0.9511 \pm 0.0020$ </td><td> $0.9509 \pm 0.0020$ </td></tr><tr><td>TraGe</td><td> $0.7212 \pm 0.0122$ </td><td> $0.7132 \pm 0.0069$ </td><td> $0.7122 \pm 0.0098$ </td><td> $0.9202 \pm 0.0022$ </td><td> $0.9193 \pm 0.0025$ </td><td> $0.9191 \pm 0.0022$ </td><td> $0.9534 \pm 0.0018$ </td><td> $0.9524 \pm 0.0032$ </td><td> $0.9514 \pm 0.0023$ </td></tr><tr><td>TrafficFormer</td><td> $0.7238 \pm 0.0081$ </td><td> $0.7110 \pm 0.0088$ </td><td> $0.7111 \pm 0.0088$ </td><td> $0.9238 \pm 0.0025$ </td><td> $0.9237 \pm 0.0021$ </td><td> $0.9230 \pm 0.0017$ </td><td> $0.9489 \pm 0.0026$ </td><td> $0.9471 \pm 0.0025$ </td><td> $0.9469 \pm 0.0025$ </td></tr><tr><td></td><td>Nepco √</td><td> $0.7032 \pm 0.0079$ </td><td> $0.7071 \pm 0.0068$ </td><td> $0.7034 \pm 0.0078$ </td><td> $0.9248 \pm 0.0024$ </td><td> $0.9190 \pm 0.0028$ </td><td> $0.9209 \pm 0.0022$ </td><td> $0.9643 \pm 0.0021$ </td><td> $0.9636 \pm 0.0019$ </td><td> $0.9639 \pm 0.0021$ </td></tr></table>

(a) DataCon  
![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/03d00364a576d4c00aea600799f2024d364ff8dfd294141a89004407860ef5ea.jpg)

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/dcc90f5354d7d7675720d7b35360e8eef7fbe560384d1c80fc6a674446db8caf.jpg)  
(b) CIC-EVSE

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/09aeeb6066183f02abc8d042a592ae52a272ef6a99cb552470fc7a8b8215dc84.jpg)  
(c) CIC-IoMT

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/08dec550609abbe54f3af111d9e7e0346b8ede9a5797ea6959a880a55d612fce.jpg)  
(d) ISCX-VPN-App

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/4dbb82e79e03fc8f9801986631049377ae0fdff270330fdc6dfb4ad7660fd0ef.jpg)  
(e) ISCX-VPN-Service

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/fd04cbb7a65e3f74a1e96f81c7b16718da4a9b55fab6eba15831d7b75aebf5f4.jpg)  
Fig. 6: The classification performance comparison under limited labeled data.  
(f) USTC-TFC

TFC, Nepco outperforms existing network foundation models, improving macro F1 by 1.11% to 29.43%. On ISCX-VPN-App and ISCX-VPN-Service, Nepco shows slightly lower performance (within 2%), as several existing models, such as TrafficFormer [138] and NetGPT [80], include these datasets in their pre-training corpora, giving them a data exposure advantage. Overall, Nepco achieves competitive classification performance compared with existing network foundation models across diverse traffic analysis tasks.

99.54%, and over BoS by 276.46%. These results demonstrate that existing hardware-offloadable models suffer from severe accuracy degradation due to their reliance on coarse-grained statistical inputs and compact model architectures, which limit their representational capacity and their ability to generalize across diverse tasks with limited labeled data.

Compared to existing hardware-offloadable models, Nepco delivers substantial improvements across all six tasks while preserving hardware deployability. On average, Nepco improves macro F1 by 160.33% over the existing hardwareoffloadable models. Specifically, Nepco improves over Flowrest by 116.03%, over Leo by 149.30%, over Mousika by

Labeled Data Dependency. We evaluate the labeled data dependency of Nepco and baselines, by varying the labeled data ratio across 0.1%, 0.5%, 1%, 5%, 10%, 50%, and 100%, applied under the same setting of 5,000 flows per class as in the measurement study (Section III). Concretely, a ratio of 1% corresponds to 50 labeled flows per class, which constitutes a genuinely few-shot setting. As shown in Fig. 6, Nepco achieves competitive few-shot performance compared to existing network foundation models, while existing hardwareoffloadable models degrade substantially under label-scarce conditions. Taking DataCon as an example, Nepco achieves a macro F1 of 0.8260 under the 1% labeled data setting, outperforming TrafficFormer (0.7549) and ET-BERT (0.8016). Among hardware-offloadable baselines, the best-performing Mousika reaches only 0.5593 under the 1% labeled data setting, and even Mousika trained on the 100% labeled data (0.7965) falls short of Nepco trained on only 1% of the data (0.8260). This demonstrates that existing hardware-offloadable models cannot compensate for their architectural limitations through additional labeled data.

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/514ea764db61ecc7818cd875996bbcd2ad94adcdac90c1fa2ad8d77d62b064a4.jpg)  
(a) Throughput (Mpps)

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/5848542dd2bff5def88d8d6f07c5239954d4f4f9b80ec598ecf23b25de663a5b.jpg)  
(b) Throughput (Gbps)

Fig. 7: The analysis latency of Nepco under continuous evaluation with varying network throughput on SmartNIC.  
![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/4ca107d4c13ee40646cb4d5d309a71143c63a15fb0cfadac1f8a7081fb9e7e60.jpg)  
(a) Traffic Coll.

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/31d4160365fcc39d0d0ab7abd47a6b0691b111d51e558be96b7afbc93a1c0ae8.jpg)  
(b) Queue Wait

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/14f4d25c84712a26e4b30c6d3b2710a2088f724f2f30bd07b8bfcc030f538021.jpg)  
(c) Input Cons.

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/01a29105ecd2a3f4350dad18f06f640111290644ddc5d7c6009aac05affeef17.jpg)  
(d) Model Infer.

Fig. 8: Latency Breakdown of Nepco on SmartNIC.  
![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/cd2a9f6203b67bc21078782f626d7af56dc3b6439c44419f47df79ba157e3ed7.jpg)  
(a) Host GPU

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/9a440c83e597618e4fbf61acfc6517b94a8ddee86451140de1379f9f1d5f40fc.jpg)  
(b) Host CPU  
Fig. 9: The latency comparison under host GPU and CPU.

## C. Efficiency Evaluation

Throughput and Latency. We evaluate the hardware prototype of Nepco deployed on the SmartNIC under real and continuous traffic over a one-minute measurement window, reporting per-second average throughput and analysis latency. As shown in Fig. 7, under network throughput reaching up to 19.81 Mpps and 165.14 Gbps, Nepco maintains a stable analysis latency between 2.23 ms and 2.47 ms, demonstrating efficient traffic analysis under high-speed network conditions.

We further analyze the latency breakdown of Nepco in Fig. 8. The input construction operates at the ns-scale, the queue wait at the us-scale, and the model inference at the msscale. The negligible input construction overhead confirms that the encoding-free design effectively eliminates the encoding cost of existing network foundation models. Notably, the traffic collection latency substantially exceeds the model inference latency, demonstrating that early-stage analysis from the first µ packets in the flow is critical for achieving low-latency network traffic analysis in practice.

TABLE IV: Comparison results of Nepco and existing foundation models on SmartNICs under different network loads.

<table><tr><td>Network Load</td><td>Method</td><td>Finish Flow Num.</td><td>Avg. Latency [ms]</td><td>P99 Latency [ms]</td></tr><tr><td rowspan="4">Extre. Low NFPS = 5</td><td>ET-BERT</td><td>300</td><td>786.57</td><td>881.37</td></tr><tr><td>TraGe</td><td>300</td><td>781.36</td><td>825.17</td></tr><tr><td>TrafficFormer</td><td>300</td><td>791.50</td><td>887.91</td></tr><tr><td>Nepco</td><td>300</td><td>2.31</td><td>2.61</td></tr><tr><td rowspan="4">Low NFPS = 500</td><td>ET-BERT</td><td>981</td><td>30479.24</td><td>60242.34</td></tr><tr><td>TraGe</td><td>966</td><td>30694.34</td><td>60493.45</td></tr><tr><td>TrafficFormer</td><td>985</td><td>30548.47</td><td>60106.11</td></tr><tr><td>Nepco</td><td>30,000</td><td>2.36</td><td>2.68</td></tr><tr><td rowspan="4">Normal NFPS = 2000</td><td>ET-BERT</td><td>982</td><td>31532.24</td><td>62117.65</td></tr><tr><td>TraGe</td><td>1,007</td><td>31890.26</td><td>62889.06</td></tr><tr><td>TrafficFormer</td><td>998</td><td>31957.56</td><td>63105.05</td></tr><tr><td>Nepco</td><td>120,000</td><td>2.38</td><td>2.69</td></tr><tr><td rowspan="4">High NFPS = 5000</td><td>ET-BERT</td><td>1,053</td><td>33619.74</td><td>65698.44</td></tr><tr><td>TraGe</td><td>992</td><td>31944.91</td><td>62351.57</td></tr><tr><td>TrafficFormer</td><td>1,039</td><td>33027.27</td><td>64730.15</td></tr><tr><td>Nepco</td><td>300,000</td><td>2.41</td><td>2.71</td></tr></table>

To isolate the architectural efficiency of Nepco from hardware-specific accelerations, we evaluate the software prototypes of Nepco and baselines on host GPU and CPU platforms in Fig. 9. On the host GPU, Nepco strictly outperforms existing network foundation models, maintaining an average latency of 0.0178 ms and reducing latency by 11.10× to 98.46×. This highlights the fundamental computational advantage of our localized convolution design over heavy Transformer-based architectures. On the host CPU, Nepco further demonstrates its lightweight nature with an average latency of 0.7395 ms, reducing latency by 43.27× to 408.37×. For the hardware-offloadable baselines, our CPU-based evaluation targets their typical off-switch fallback scenarios. While their native P4/FPGA deployments achieve extreme speeds, this efficiency relies on coarse-grained inputs and compact architectures. As demonstrated in Section V-B, such compromises come at the cost of significantly lower classification performance and greater labeled data dependency.

Diverse Network Loads. We deploy Nepco and three existing network foundation models on the SmartNIC and measure analysis latency under varying network loads characterized by new flows per second (NFPS). As shown in TABLE IV, existing network foundation models achieve line-rate analysis under low network load, but their latency increases significantly as the load grows (e.g., TrafficFormer reaches 791.50 ms at 5 NFPS). In contrast, Nepco maintains millisecondscale latency across four network loads, and achieves linerate analysis even under high load (5,000 NFPS). Notably, under comparable conditions where both Nepco and existing methods achieve line-rate analysis, Nepco reduces latency by up to 328×. Overall, Nepco reduces the analysis latency of network foundation models from the second scale to the millisecond scale, enabling low-latency traffic analysis.

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/7c24a9a360e82e6549225f5c5e73c90d56516d8cc144b694cd665156bf252a47.jpg)  
Fig. 10: Ablation study of Nepco, including the key component ablation (w/o component) and the substitution with existing methods (w/ component replaced by alternative).

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/9f9799e44fc859d872ea5f3af85e54017707295c4b59d312c376d51fd195814f.jpg)  
(a) Convolution Architecture

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/a00e893bdacc41552142dc80033a7e93720556485881952a31e13fd6cfcf46aa.jpg)  
(b) Convolution Layer  
Fig. 11: The comparison with convolution-based methods.

## D. Nepco Deep Dive

Ablation Study. We validate the model architecture design of Nepco in Fig. 10. To begin with, removing window-wise byte scoring leads to a 9.05% drop in macro F1, while replacing it with sequence-level scoring yields only marginal improvement, indicating that localized modeling within each convolution window is essential and cannot be recovered at the sequence level. Although attention-based scoring slightly improves performance (+0.85%), it incurs a 4.74× increase in latency, showing that the proposed design achieves a better efficiency–effectiveness trade-off. Consistent with this, removing sequence-wise byte gating causes an 8.71% drop, and replacing it with ReLU or GeLU brings limited gains, suggesting that adaptive importance estimation is necessary beyond static activations. From the training perspective, replacing continuous byte masking with random masking significantly degrades performance, and removing pre-training further leads to a 15.84% drop, demonstrating the importance of learning generalizable traffic representations. Finally, replacing max pooling with mean or first pooling degrades performance by 3.85% and 11.77%, respectively, as they fail to preserve discriminative localized patterns.

Convolution-based Methods. We compare Nepco against representative convolution-based methods, including Text-CNN [56], VGG [102], LeNet-5 [59], and GoogLeNet [104], which are widely used as model architectures in existing traffic analysis methods [28], [74], [112], [113], [127], [140]. As shown in Fig. 11(a), Nepco outperforms existing convolutionbased methods by 10.03%, 21.28%, 19.85%, and 15.48% in macro F1, demonstrating the effectiveness of Nepco’s localized pattern-aware design for byte sequences. We further analyze the effect of the number of traffic convolution layers in Fig. 11(b). The results show that 5 layers achieve the best trade-off between macro F1 and latency. Fewer layers reduce representation capacity, while more layers increase latency linearly without substantial performance gains.

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/7d86d78e8c834e0dabb4c952274f83984b409098f960b0820e15226288c4c130.jpg)  
(a) Span Length

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/5e222abff2a6f16a81413158a17e0d10b320f5db19a4b374b001c076eb496c93.jpg)  
(b) Packet Count  
Fig. 12: Parameter sensitivity analysis of Nepco.

Parameter Sensitivity Analysis. We analyze the sensitivity of two key parameters in Nepco. Fig. 12(a) shows the effect of the span length in continuous byte masking. A span length between 3 and 7 achieves the best performance, as shorter spans degrade to random masking and fail to capture localized protocol field patterns, while longer spans increase learning difficulty and deviate from the byte length distribution of protocol fields. Fig. 12(b) shows the effect of packet count on classification performance. Increasing the packet count below 5 yields substantial gains, while further increasing from 5 to 10, 50, or even 100 provides diminishing returns. This confirms that fine-grained byte-level semantics reduce reliance on observing more packets, consistent with the early-stage analysis setting adopted by prior works [68], [138].

## VI. DISCUSSION

Pre-training Corpus Scale and Generalizability. The pretraining corpus of Nepco is moderate in scale, in part because we strictly require the pre-training data to predate the finetuning data. This temporal separation avoids using future protocol knowledge to evaluate earlier analysis tasks, which would inflate generalization evaluation. Despite this constraint, Section V-B shows that Nepco achieves classification performance competitive with state-of-the-art network foundation models. Recent work, such as MM4Flow [125], shows that TB-scale pre-training further enhances versatility, which we leave as an orthogonal direction for future work.

Deployment on Other Programmable Hardware. Nepco is prototyped on the SmartNIC, but its design choices can be extended to other programmable hardware platforms. Specifically, Nepco’s window-wise byte scoring uses pre-computed weights that can be realized as table lookups, while its sequence-wise byte gating relies on parallel element-wise operations—both are inherently hardware-friendly. This allows Nepco to align with parallel-compute platforms such as FPGAs and to enable hybrid execution on more constrained platforms such as P4 switches. We believe Nepco’s core design (e.g., efficient localized byte-sequence modeling) has the potential to inform and strengthen network foundation model-based traffic analysis on other programmable hardware platforms.

## VII. CONCLUSION

In this paper, we show that the long-standing challenge between versatile and efficient network traffic analysis is not fundamental but a consequence of polarized design choices in prior work. We present Nepco, which resolves these polarizations and offloads the network foundation model to SmartNIC for versatile yet efficient network traffic analysis. At its core, Nepco is the convolution-based pre-trained network foundation model, performing efficient localized byte-sequence modeling. Across six traffic analysis tasks, Nepco matches or exceeds state-of-the-art network foundation models, while reducing analysis latency by 328× to the millisecond scale on Smart-NIC. With only 1% of labeled data, Nepco surpasses existing hardware-offloadable models trained on 100% labels.

## REFERENCES

[1] A. T.-J. Akem, M. Gucciardo, and M. Fiore, “Flowrest: Practical flowlevel inference in programmable switches with random forests,” in IEEE INFOCOM 2023-IEEE Conference on Computer Communications. IEEE, 2023, pp. 1–10.

[2] allot, “Network traffic identification and classification,” https:// www.allot.com/network-intelligence/technology/traffic-identification/, Accessed March 2026.

[3] Amazon Web Services, “Ddos mitigation - security at the edge: Core principles,” https://docs.aws.amazon.com/whitepapers/ latest/security-at-the-edge/ddos-mitigation.html, 2026.

[4] Amazon Web Services, “Mitigation techniques - aws best practices for ddos resiliency,” https://docs.aws.amazon.com/whitepapers/latest/ aws-best-practices-ddos-resiliency/mitigation-techniques.html, 2026.

[5] AMD, “Amd fpgas,” https://www.amd.com/en/products/ adaptive-socs-and-fpgas/fpga.html, 2026.

[6] B. Anderson and D. McGrew, “Identifying encrypted malware traffic with contextual flow data,” in Proceedings of the 2016 ACM workshop on artificial intelligence and security, 2016, pp. 35–46.

[7] B. Anderson, S. Paul, and D. McGrew, “Deciphering malware’s use of tls (without decryption),” Journal of Computer Virology and Hacking Techniques, vol. 14, no. 3, pp. 195–211, 2018.

[8] M. Awais, M. Naseer, S. Khan, R. M. Anwer, H. Cholakkal, M. Shah, M.-H. Yang, and F. S. Khan, “Foundation models defining a new era in vision: a survey and outlook,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 47, no. 4, pp. 2245–2264, 2025.

[9] D. Barradas, N. Santos, L. Rodrigues, S. Signorello, F. M. Ramos, and A. Madeira, “Flowlens: Enabling efficient flow classification for ml-based network security applications.” in NDSS, 2021.

[10] I. Beltagy, M. E. Peters, and A. Cohan, “Longformer: The longdocument transformer,” arXiv preprint arXiv:2004.05150, 2020.

[11] E. D. Buedi, A. A. Ghorbani, S. Dadkhah, and R. L. Ferreira, “Enhancing ev charging station security using a multi-dimensional dataset: Cicevse2024,” in IFIP Annual Conference on Data and Applications Security and Privacy. Springer, 2024, pp. 171–190.

[12] J. Cao, Y. Xu, and Q. Xiang, “L-etc: A lightweight model based on key bytes selection for encrypted traffic classification,” in ICC 2023- IEEE International Conference on Communications. IEEE, 2023, pp. 2370–2375.

[13] J. Cao, Y. Xu, E. Yu, Q. Xiang, K. Song, L. He, and G. Cheng, “Gatekeeper: An ultralite malicious traffic identification method with dualaspect optimization strategies on iot gateways,” Computer Networks, vol. 250, p. 110556, 2024.

[14] Z. Chen, K. He, J. Li, and Y. Geng, “Seq2img: A sequence-to-image based approach towards ip traffic classification using convolutional neural networks,” in 2017 IEEE International conference on big data (big data). IEEE, 2017, pp. 1271–1276.

[15] R. Child, S. Gray, A. Radford, and I. Sutskever, “Generating long sequences with sparse transformers,” arXiv preprint arXiv:1904.10509, 2019.

[16] F. Chollet, “Xception: Deep learning with depthwise separable convolutions,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2017, pp. 1251–1258.

[17] Cisco, “Global - 2021 forecast highlights,” https://www.cisco.com/ c/dam/m/en us/solutions/service-provider/vni-forecast-highlights/pdf/ Global 2021 Forecast Highlights.pdf, Accessed March 2026.

[18] G. Cloud, “Network pricing,” https://cloud.google.com/vpc/ network-pricing, 2026.

[19] S. Dadkhah, H. Mahdikhani, P. K. Danso, A. Zohourian, K. A. Truong, and A. A. Ghorbani, “Towards the development of a realistic multidimensional iot profiling dataset,” in 2022 19th Annual International Conference on Privacy, Security & Trust (PST). IEEE, 2022, pp. 1–11.

[20] S. Dadkhah, E. C. P. Neto, R. Ferreira, R. C. Molokwu, S. Sadeghi, and A. Ghorbani, “Ciciomt2024: Attack vectors in healthcare devices-a multi-protocol dataset for assessing iomt device security,” 2024.

[21] T. Dahanayaka, Y. Ginige, Y. Huang, G. Jourjon, and S. Seneviratne, “Robust open-set classification for encrypted traffic fingerprinting,” Computer Networks, vol. 236, p. 109991, 2023.

[22] DataCon-Community, “Datacon2021 - encrypted proxy traffic dataset,” https://datacon.qianxin.com/opendata/openpage?resourcesId=10, 2021.

[23] S. Daum, T. Shapira, A. Bremler-Barr, and D. Hay, “Non-uniformity is all you need: Efficient and timely encrypted traffic classification with echo,” in 2025 IEEE 33rd International Conference on Network Protocols (ICNP). IEEE, 2025, pp. 1–12.

[24] Y. N. Dauphin, A. Fan, M. Auli, and D. Grangier, “Language modeling with gated convolutional networks,” in International conference on machine learning. PMLR, 2017, pp. 933–941.

[25] X. Deng, Q. Li, and K. Xu, “Robust and reliable early-stage website fingerprinting attacks via spatial-temporal distribution analysis,” in Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security, 2024, pp. 1997–2011.

[26] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “Bert: Pre-training of deep bidirectional transformers for language understanding,” in Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers), 2019, pp. 4171–4186.

[27] P. Dodia, M. AlSabah, O. Alrawi, and T. Wang, “Exposing the rat in the tunnel: Using traffic analysis for tor-based malware detection,” in Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security, 2022, pp. 875–889.

[28] C. Dong, C. Zhang, Z. Lu, B. Liu, and B. Jiang, “Cetanalytics: Comprehensive effective traffic information analytics for encrypted traffic classification,” Computer Networks, vol. 176, p. 107258, 2020.

[29] Y. Dong, Q. Li, K. Wu, R. Li, D. Zhao, G. Tyson, J. Peng, Y. Jiang, S. Xia, and M. Xu, “Horuseye: A realtime iot malicious traffic detection framework using programmable switches,” in 32nd USENIX Security Symposium (USENIX Security 23), 2023, pp. 571–588.

[30] A. Dosovitskiy, L. Beyer, A. Kolesnikov, D. Weissenborn, X. Zhai, T. Unterthiner, M. Dehghani, M. Minderer, G. Heigold, S. Gelly et al., “An image is worth 16x16 words: Transformers for image recognition at scale,” arXiv preprint arXiv:2010.11929, 2020.

[31] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of encrypted and vpn traffic using time-related,” in Proceedings ofthe 2nd international conference on information systems security and privacy (ICISSP), 2016, pp. 407–414.

[32] ENEA, “Network dpi & traffic classification,” https://www.enea.com/ solutions/traffic-management/dpi-classification-and-monetization/, Accessed March 2026.

[33] C. Fu, Q. Li, E. Bertino, and K. Xu, “Training with only 1.0‰ samples: Malicious traffic detection via cross-modality feature fusion,” in Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security, 2025, pp. 3930–3944.

[34] C. Fu, Q. Li, M. Shen, and K. Xu, “Realtime robust malicious traffic detection via frequency domain analysis,” in Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security, 2021, pp. 3431–3446.

[35] C. Fu, Q. Li, M. Shen, and K. Xu, “Detecting tunneled flooding traffic via deep semantic analysis of packet length patterns,” in Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security, 2024, pp. 3659–3673.

[36] C. Fu, Q. Li, and K. Xu, “Detecting unknown encrypted malicious traffic in real time via flow interaction graph analysis,” arXiv preprint arXiv:2301.13686, 2023.

[37] C. Fu, Q. Li, K. Xu, and J. Wu, “Point cloud analysis for mlbased malicious traffic detection: Reducing majorities of false positive alarms,” in Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security, 2023, pp. 1005–1019.

[38] M. Fu, P. Wang, M. Liu, Z. Zhang, and X. Zhou, “Iov-bert-ids: Hybrid network intrusion detection system in iov using large language models,” IEEE Transactions on Vehicular Technology, vol. 74, no. 2, pp. 1909– 1921, 2024.

[39] X. Gao, T. Li, Y. Zhang, Z. Wang, X. Zeng, S. Yao, and K. Xu, “Fenix: Enabling in-network dnn inference with fpga-enhanced programmable switches,” arXiv preprint arXiv:2507.14891, 2025.

[40] R. Geirhos, J.-H. Jacobsen, C. Michaelis, R. Zemel, W. Brendel, M. Bethge, and F. A. Wichmann, “Shortcut learning in deep neural networks,” Nature Machine Intelligence, vol. 2, no. 11, pp. 665–673, 2020.

[41] S. Guthula, R. Beltiukov, N. Battula, W. Guo, and A. Gupta, “netfound: Foundation model for network security,” arXiv preprint arXiv:2310.17025, 2023.

[42] Z. Hang, Y. Lu, Y. Wang, and Y. Xie, “Flow-mae: Leveraging masked autoencoder for accurate, efficient and robust malicious traffic classification,” in Proceedings of the 26th International Symposium on Research in Attacks, Intrusions and Defenses, 2023, pp. 297–314.

[43] H. He, X. Lin, Z. Weng, R. Zhao, S. Gan, L. Chen, Y. Ji, J. Wang, and Z. Xue, “Code is not natural language: Unlock the power of semanticsoriented graph representation for binary code similarity detection,” in 33rd USENIX Security Symposium, 2024, pp. 1759–1776.

[44] H. Y. He, Z. G. Yang, and X. N. Chen, “Pert: Payload encoding representation from transformer for encrypted traffic classification,” in 2020 ITU Kaleidoscope: Industry-Driven Digital Transformation (ITU K). IEEE, 2020, pp. 1–8.

[45] K. He, X. Chen, S. Xie, Y. Li, P. Dollar, and R. Girshick, “Masked´ autoencoders are scalable vision learners,” in Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2022, pp. 16 000–16 009.

[46] L. Hu, C. Hei, F. Li, C. Gao, J. Shen, and X. Wang, “Smarttc: A real-time ml-based traffic classification with smartnic,” in IEEE/ACM International Symposium on Quality ofService. IEEE, 2025, pp. 1–10.

[47] Z. Huang, C. Lin, W. Zhang, X. Meng, and Y. Zhang, “Distillationenhanced clustering acceleration for encrypted traffic classification,” arXiv preprint arXiv:2508.02282, 2025.

[48] N. Hurley and S. Rickard, “Comparing measures of sparsity,” IEEE Transactions on Information Theory, vol. 55, no. 10, pp. 4723–4741, 2009.

[49] Intel, “Intel xeon platinum 8458p processor,” https: //www.intel.com/content/www/us/en/products/sku/231742/ intel-xeon-platinum-8458p-processor-82-5m-cache-2-70-ghz/ specifications.html, accessed March 2026.

[50] Intel, “Intel tofino intelligent fabric processors,” https: //www.intel.com/content/www/us/en/products/details/network-io/ programmable-ethernet-switch.html, 2026.

[51] Intel, “Data plane development kit,” http://www.dpdk.org, Accessed March 2026.

[52] S. U. Jafri, S. Rao, V. Shrivastav, and M. Tawarmalani, “Leo: Online ml-based traffic classification at multi-terabit line rate,” in 21st USENIX Symposium on Networked Systems Design and Implementation (NSDI 24), 2024, pp. 1573–1591.

[53] H. H. Jazi, H. Gonzalez, N. Stakhanova, and A. A. Ghorbani, “Detecting http-based application layer dos attacks on web servers in the presence of sampling,” Computer Networks, vol. 121, pp. 25–36, 2017.

[54] X. Jiang, S. Liu, S. Naama, F. Bronzino, P. Schmitt, and N. Feamster, “Jiti: Dynamic model serving for just-in-time traffic inference,” Proceedings of the ACM on Networking, vol. 3, no. CoNEXT4, pp. 1–24, 2025.

[55] M. Joshi, D. Chen, Y. Liu, D. S. Weld, L. Zettlemoyer, and O. Levy, “Spanbert: Improving pre-training by representing and predicting spans,” Transactions of the association for Computational Linguistics, vol. 8, pp. 64–77, 2020.

[56] Y. Kim, “Convolutional neural networks for sentence classification,” in Proceedings of the 2014 conference on empirical methods in natural language processing (EMNLP), 2014, pp. 1746–1751.

[57] L. Kurlandski, H. Berger, Y. Pan, and M. Wright, “Beyond raw bytes: Towards large malware language models,” 2026.

[58] Z. Lan, M. Chen, S. Goodman, K. Gimpel, P. Sharma, and R. Soricut, “Albert: A lite bert for self-supervised learning of language representations,” arXiv preprint arXiv:1909.11942, 2019.

[59] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, “Gradient-based learning applied to document recognition,” Proceedings of the IEEE, vol. 86, no. 11, pp. 2278–2324, 2002.

[60] F. Li and F. Ye, “Simplifying data traffic classification with byte importance distillation,” in ICC 2021-IEEE International Conference on Communications. IEEE, 2021, pp. 1–6.

[61] R. Li, S. Liu, H. Hu, Q. Ye, and N. Feamster, “Wifinger: Fingerprinting noisy iot event traffic using packet-level sequence matching,” arXiv preprint arXiv:2508.03151, 2025.

[62] S. Li, Z. Gan, M. Xiao, P. Hu, X. Cheng, C. Wang, and F. Li, “Mota: Mixture of traffic agents for robust network traffic classification,” in 2025 IEEE/ACM 33rd International Symposium on Quality of Service (IWQoS). IEEE, 2025, pp. 1–10.

[63] X. Li, J. Guo, Q. Song, J. Xie, Y. Sang, S. Zhao, and Y. Zhang, “Listen to minority: Encrypted traffic classification for class imbalance with contrastive pre-training,” in Annual IEEE International Conference on Sensing, Communication, and Networking. IEEE, 2023, pp. 447–455.

[64] X. Li, C. Qian, Q. Wang, J. Kong, Y. Wang, Z. Yao, B. Ji, L. Cheng, G. Zhou, and H. Shao, “Lens: A knowledge-guided foundation model for network traffic,” arXiv preprint arXiv:2402.03646, 2024.

[65] C. Lin, Y. Jiang, W. Zhang, X. Meng, T. Zuo, and Y. Zhang, “Trage: A generic packet representation for traffic classification based on header-payload differences,” in 2025 IEEE/ACM 33rd International Symposium on Quality of Service (IWQoS). IEEE, 2025, pp. 1–6.

[66] C. Lin, W. Zhang, H. Luo, X. Meng, and Y. Zhang, “Nethira: A heterogeneity-aware hierarchical pre-trained model for network traffic classification,” arXiv preprint arXiv:2601.22494, 2026.

[67] J. Lin, “Divergence measures based on the shannon entropy,” IEEE Transactions on Information theory, vol. 37, no. 1, pp. 145–151, 2002.

[68] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in Proceedings of the ACM Web Conference 2022, 2022, pp. 633–642.

[69] C. Liu, W. Wang, M. Wang, F. Lv, and M. Konan, “An efficient instance selection algorithm to reconstruct training set for support vector machine,” Knowledge-Based Systems, vol. 116, pp. 58–73, 2017.

[70] Y. Liu, X. Wang, B. Qu, and F. Zhao, “Atvitsc: A novel encrypted traffic classification method based on deep learning,” IEEE transactions on information forensics and security, vol. 19, pp. 9374–9389, 2024.

[71] Z. Liu, H. Namkung, G. Nikolaidis, J. Lee, C. Kim, X. Jin, V. Braverman, M. Yu, and V. Sekar, “Jaqen: A high-performance switchnative approach for detecting and mitigating volumetric ddos attacks with programmable switches,” in 30th USENIX Security Symposium (USENIX Security 21), 2021, pp. 3829–3846.

[72] LiveAction, “Encrypted traffic analysis,” https://www.liveaction.com/ solutions/network-security/encrypted-traffic-analysis/, Accessed March 2026.

[73] M. Lotfollahi, M. Jafari Siavoshani, R. Shirali Hossein Zade, and M. Saberian, “Deep packet: A novel approach for encrypted traffic classification using deep learning,” Soft Computing, vol. 24, no. 3, pp. 1999–2012, 2020.

[74] B. Lu, N. Luktarhan, C. Ding, and W. Zhang, “Iclstm: encrypted traffic service identification based on inception-lstm neural network,” Symmetry, vol. 13, no. 6, p. 1080, 2021.

[75] H. Lu, Z. Ma, X. Li, S. Bi, X. He, and K. Wang, “Traffichd: Efficient hyperdimensional computing for real-time network traffic analytics,” in Proceedings of the 61st ACM/IEEE Design Automation Conference, 2024, pp. 1–6.

[76] M. Lu, B. Zhou, and Z. Bu, “Two-stage distillation-aware compressed models for traffic classification,” IEEE Internet of Things Journal, vol. 10, no. 16, pp. 14 152–14 166, 2023.

[77] J. Luo, Z. Chen, W. Chen, H. Lu, and F. Lyu, “A study on the application of the t5 large language model in encrypted traffic classification,” Peer-to-Peer Networking and Applications, vol. 18, no. 1, p. 15, 2025.

[78] J. Ma, X. Li, H. Luo, and Y. Sun, “Netkd: Towards resource-efficient encrypted traffic classification using knowledge distillation for language models,” in International Conference on Computer Supported Cooperative Work in Design. IEEE, 2024, pp. 3011–3016.

[79] L. man-pages project, “raw(7): Ipv4 raw sockets,” https://man7.org/ linux/man-pages/man7/raw.7.html, Accessed March 2026.

[80] X. Meng, C. Lin, Y. Wang, and Y. Zhang, “Netgpt: Generative pretrained transformer for network traffic,” arXiv preprint arXiv:2304.09513, 2023.

[81] Microsoft, “Onnx runtime,” https://onnxruntime.ai, Accessed March 2026.

[82] A. Monemi, R. Zarei, and M. N. Marsono, “Online netfpga decision tree statistical traffic classifier,” Computer Communications, vol. 36, no. 12, pp. 1329–1340, 2013.

[83] NVIDIA, “Accelerating the suricata ids/ips with nvidia bluefield dpus,” https://developer.nvidia.com/blog/

accelerating-the-suricata-ids-ips-with-nvidia-bluefield-dpus/, Accessed March 2026.

[84] NVIDIA, “Nvidia bluefield-3 networking platform user guide,” https: //docs.nvidia.com/networking/display/bf3dpu/, Accessed March 2026.

[85] NVIDIA, “Nvidia bluefield networking platform,” https://www. nvidia.com/en-us/networking/products/data-processing-unit/, Accessed March 2026.

[86] NVIDIA, “Nvidia connectx-7 adapter cards user manual,” https://docs. nvidia.com/networking/display/connectx7vpi, Accessed March 2026.

[87] NVIDIA, “Nvidia doca software framework,” https://developer.nvidia. com/networking/doca, Accessed March 2026.

[88] NVIDIA, “Nvidia h800 gpu,” https://docs.nvidia.com/ai-enterprise/ release-7/latest/infra-software/vgpu/reference/hopper.html, Accessed March 2026.

[89] Z. Okonkwo, E. Foo, Q. Li, and Z. Hou, “A cnn based encrypted network traffic classifier,” in Proceedings of the 2022 Australasian Computer Science Week, 2022, pp. 74–83.

[90] L. Peng, X. Xie, S. Huang, Z. Wang, and Y. Cui, “Ptu: Pre-trained model for network traffic understanding,” in 2024 IEEE 32nd International Conference on Network Protocols. IEEE, 2024, pp. 1–12.

[91] W. Peng, L. Cui, W. Cai, W. Wang, X. Cui, Z. Hao, and X. Yun, “Bottom aggregating, top separating: An aggregator and separator network for encrypted traffic understanding,” IEEE Transactions on Information Forensics and Security, vol. 20, pp. 1794–1806, 2025.

[92] R. Perez-Jove, C. R. Munteanu, J. Dorado, A. Pazos, and J. V ´ azquez-´ Naya, “Network traffic foundation models: A systematic review,” Computer Networks, p. 111998, 2026.

[93] J. Qu, X. Ma, and J. Li, “Trafficgpt: Breaking the token barrier for efficient long traffic analysis and generation,” arXiv preprint arXiv:2403.05822, 2024.

[94] A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, I. Sutskever et al., “Language models are unsupervised multitask learners,” OpenAI blog, vol. 1, no. 8, p. 9, 2019.

[95] C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y. Zhou, W. Li, and P. J. Liu, “Exploring the limits of transfer learning with a unified text-to-text transformer,” Journal of machine learning research, vol. 21, no. 140, pp. 1–67, 2020.

[96] A. Roy, H. Zeng, J. Bagga, G. Porter, and A. C. Snoeren, “Inside the social network’s (datacenter) network,” in Proceedings of the 2015 ACM Conference on Special Interest Group on Data Communication, 2015, pp. 123–137.

[97] S. S. Roy and S. Nilizadeh, “Phishlang: A real-time, fully clientside phishing detection framework using mobilebert,” arXiv preprint arXiv:2408.05667, 2024.

[98] T. Shapira and Y. Shavitt, “Flowpic: Encrypted internet traffic classification is as easy as image recognition,” in IEEE INFOCOM 2019- IEEE conference on computer communications workshops (INFOCOM WKSHPS). IEEE, 2019, pp. 680–687.

[99] T. Shapira and Y. Shavitt, “Flowpic: A generic representation for encrypted traffic classification and applications identification,” IEEE Transactions on Network and Service Management, vol. 18, no. 2, pp. 1218–1232, 2021.

[100] W. Shbair, T. Cholez, J. Francois, and I. Chrisment, “Https websites dataset,” 4http://betternet.lhs.loria.fr/datasets/https/, 2016.

[101] M. Shen, J. Wu, J. Ai, Q. Li, C. Ren, K. Xu, and L. Zhu, “Swallow: a transfer-robust website fingerprinting attack via consistent feature learning,” in Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security, 2025, pp. 1574–1588.

[102] K. Simonyan and A. Zisserman, “Very deep convolutional networks for large-scale image recognition,” arXiv preprint arXiv:1409.1556, 2014.

[103] G. Siracusano, S. Galea, D. Sanvito, M. Malekzadeh, G. Antichi, P. Costa, H. Haddadi, and R. Bifulco, “Re-architecting traffic analysis with neural network interface cards,” in 19th USENIX symposium on networked systems design and implementation, 2022, pp. 513–533.

[104] C. Szegedy, W. Liu, Y. Jia, P. Sermanet, S. Reed, D. Anguelov, D. Erhan, V. Vanhoucke, and A. Rabinovich, “Going deeper with convolutions,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2015, pp. 1–9.

[105] The Hague Centre for Strategic Studies (HCSS) and The Hague Security Delta (HSD), “Implications of ai and machine learning for cybersecurity: Understanding the strategic and technical significance of technology for security,” Tech. Rep., Accessed March 2026. [Online]. Available: https://securitydelta.nl/media/com hsd/report/234/ document/HSD-Rapport-AI-11619.pdf

[106] D. Tong, Y. R. Qu, and V. K. Prasanna, “Accelerating decision tree based traffic classification on fpga and multicore platforms,” IEEE transactions on parallel and distributed systems, vol. 28, no. 11, pp. 3046–3059, 2017.

[107] TrafficWiz, “Encrypted network traffic visibility simplified,” https: //trafficwiz.com/, Accessed March 2026.

[108] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, “Attention is all you need,” Advances in neural information processing systems, vol. 30, 2017.

[109] G. Wan, S. Liu, F. Bronzino, N. Feamster, and Z. Durumeric, “Cato: End-to-end optimization of ml-based traffic analysis pipelines,” in 22nd USENIX Symposium on Networked Systems Design and Implementation (NSDI 25), 2025, pp. 1523–1540.

[110] T. Wang, X. Xie, W. Wang, C. Wang, J. Liu, B. Huang, Y. Hu, Y. Zhao, and Y. Cui, “Netmamba+: A framework of pre-trained models for efficient and accurate network traffic classification,” arXiv preprint arXiv:2601.21792, 2026.

[111] T. Wang, X. Xie, W. Wang, C. Wang, Y. Zhao, and Y. Cui, “Netmamba: Efficient network traffic classification via pre-training unidirectional mamba,” in 2024 IEEE 32nd International Conference on Network Protocols (ICNP). IEEE, 2024, pp. 1–11.

[112] W. Wang, M. Zhu, J. Wang, X. Zeng, and Z. Yang, “End-to-end encrypted traffic classification with one-dimensional convolution neural networks,” in 2017 IEEE international conference on intelligence and security informatics (ISI). IEEE, 2017, pp. 43–48.

[113] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware traffic classification using convolutional neural network for representation learning,” in 2017 International conference on information networking (ICOIN). IEEE, 2017, pp. 712–717.

[114] X. Wang, Z. Wang, E. Wang, and Z. Sun, “Spatial-temporal knowledge distillation for lightweight network traffic anomaly detection,” Computers & Security, vol. 137, p. 103636, 2024.

[115] Y. Wang, H. He, Y. Lai, and A. X. Liu, “A two-phase approach to fast and accurate classification of encrypted traffic,” IEEE/ACM Transactions On Networking, vol. 31, no. 3, pp. 1071–1086, 2022.

[116] W. Wei, H. Gu, W. Deng, Z. Xiao, and X. Ren, “Abl-tc: A lightweight design for network traffic classification empowered by deep learning,” Neurocomputing, vol. 489, pp. 333–344, 2022.

[117] N. Wickramasinghe, A. Shaghaghi, E. Ferrari, and S. Jha, “Less is more: Simplifying network traffic classification leveraging rfcs,” in Companion Proceedings of the ACM on Web Conference 2025, 2025, pp. 1398–1401.

[118] N. Wickramasinghe, A. Shaghaghi, G. Tsudik, and S. Jha, “Sok: Decoding the enigma of encrypted network traffic classifiers,” in IEEE Symposium on Security and Privacy. IEEE, 2025, pp. 1825–1843.

[119] D. Wu, X. Wang, Y. Qiao, Z. Wang, J. Jiang, S. Cui, and F. Wang, “Netllm: Adapting large language models for networking,” in Proceedings of the ACM SIGCOMM 2024 Conference, 2024, pp. 661–678.

[120] S. Xi, T. Fu, K. Bu, C. Yang, Z. Chang, W. Chen, Z. Ma, C. Chen, Y. Shen, and K. Ren, “Mineshark: Cryptomining traffic detection at scale.” in NDSS, 2025.

[121] G. Xie, Q. Li, G. Duan, J. Lin, Y. Dong, Y. Jiang, D. Zhao, and Y. Yang, “Empowering in-network classification in programmable switches by binary decision tree and knowledge distillation,” IEEE/ACM Transactions on Networking, vol. 32, no. 1, pp. 382–395, 2023.

[122] J. Xing, Q. Kang, and A. Chen, “Netwarden: Mitigating network covert channels while preserving performance,” in 29th USENIX Security Symposium (USENIX Security 20), 2020, pp. 2039–2056.

[123] J. Yan, H. Xu, Z. Liu, Q. Li, K. Xu, M. Xu, and J. Wu, “Brainon-switch: Towards advanced intelligent network data plane via nndriven traffic analysis at line-speed,” in 21st USENIX Symposium on Networked Systems Design and Implementation, 2024, pp. 419–440.

[124] L. Yang, L. Liu, J.-j. Huang, J. Shi, S. Fu, Y. Wang, and J. Su, “Robustness matters: Pre-training can enhance the performance of encrypted traffic analysis,” IEEE Transactions on Information Forensics and Security, 2025.

[125] L. Yang, L. Liu, J. Huang, Z. Liu, S. Liang, S. Fu, and Y. Wang, “Mm4flow: A pre-trained multi-modal model for versatile network traffic analysis,” in Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security, 2025, pp. 1664–1678.

[126] L. Yang, Y. Wang, L. Liu, J. Huang, and S. Fu, “Expmd: an explainable framework for traffic identification based on multi-domain features,” in 2024 IEEE/ACM 32nd International Symposium on Quality of Service (IWQoS). IEEE, 2024, pp. 1–10.

[127] Y. Yu and X. Guan, “Multi-task encrypted network traffic classification based on feature extraction,” in Proceedings of the 2025 4th International Conference on Cryptography, Network Security and Communication Technology, 2025, pp. 11–15.

[128] C. Zha, Z. Wang, Y. Fan, B. Bai, Y. Zhang, S. Shi, and R. Zhang, “Anids: adaptive network intrusion detection system based on clustering and stacked ctgan,” IEEE Transactions on Information Forensics and Security, 2025.

[129] H. Zhang, G. Liu, X. Shi, Y. Li, D. He, J. Wang, Z. Wang, Y. Zhu, K. Ruan, W. Cao et al., “Achieving high-speed and robust encrypted traffic anomaly detection with programmable switches,” in Proceedings of the ACM SIGCOMM 2025 Conference, 2025, pp. 1254–1256.

[130] M. Zhang, G. Li, S. Wang, C. Liu, A. Chen, H. Hu, G. Gu, Q. Li, M. Xu, and J. Wu, “Poseidon: Mitigating volumetric ddos attacks with programmable switches,” in the 27th Network and Distributed System Security Symposium (NDSS 2020), 2020.

[131] Y. Zhang, S. Yao, Y. Feng, K. Chen, T. Li, Z. Liu, Y. Zhao, L. Zhang, X. Gao, F. Xiong et al., “Pegasus: A universal framework for scalable deep learning inference on the dataplane,” in Proceedings of the ACM SIGCOMM 2025 Conference, 2025, pp. 692–706.

[132] Z. Zhang, Z. Luan, Q. Li, Z. Qi, K. Li, Y. Jiang, and Z. Yuan, “Sentinelx: A lightweight malicious traffic detection system based on programmable switches,” in IEEE INFOCOM 2025-IEEE Conference on Computer Communications. IEEE, 2025, pp. 1–10.

[133] F. Zhao, W. Li, H. Bao, Z. Li, G. Zhou, W. Wang, and F. Liu, “Nuwa: Enhancing network traffic analysis with pre-trained side-¨ channel feature imputation,” IEEE Transactions on Networking, 2025.

[134] L. Zhao, Q. Liu, L. Yue, W. Chen, L. Chen, R. Sun, and C. Song, “Comi: Correct and mitigate shortcut learning behavior in deep neural networks,” in Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, 2024, pp. 218–228.

[135] R. Zhao, M. Zhan, X. Deng, F. Li, Y. Wang, Y. Wang, G. Gui, and Z. Xue, “A novel self-supervised framework based on masked autoencoder for traffic classification,” IEEE/ACM Transactions on Networking, vol. 32, no. 3, pp. 2012–2025, 2024.

[136] Y. Zhao, G. Dettori, M. Boffa, L. Vassio, and M. Mellia, “The sweet danger of sugar: Debunking representation learning for encrypted traffic classification,” in Proceedings of the ACM SIGCOMM 2025 Conference, 2025, pp. 296–310.

[137] Z. Zhao, Z. Li, Z. Song, F. Zhang, and B. Chen, “Rids: Towards advanced ids via rnn model and programmable switches co-designed approaches,” in IEEE INFOCOM 2024-IEEE Conference on Computer Communications. IEEE, 2024, pp. 591–600.

[138] G. Zhou, X. Guo, Z. Liu, T. Li, Q. Li, and K. Xu, “Trafficformer: an efficient pre-trained model for traffic data,” in 2025 IEEE symposium on security and privacy (SP). IEEE, 2025, pp. 1844–1860.

[139] G. Zhou, Z. Liu, C. Fu, Q. Li, and K. Xu, “An efficient design of intelligent network data plane,” in 32nd USENIX Security Symposium (USENIX Security 23), 2023, pp. 6203–6220.

[140] Y. Zhou, H. Shi, Y. Zhao, W. Ding, J. Han, H. Sun, X. Zhang, C. Tang, and W. Zhang, “Identification of encrypted and malicious network traffic based on one-dimensional convolutional neural network,” Journal of Cloud Computing, vol. 12, no. 1, p. 53, 2023.

[141] Zscaler, “2024: The year of scaling security efficiencies,” Accessed March 2026.

## APPENDIX

## A. The Impact of Address-related Information

Since existing network foundation models follow the pretraining and fine-tuning paradigm, we examine the impact of address-related information across these two stages and make two experimental observations:

1) In the pre-training stage, introducing address-related pretraining tasks leads to substantial inflation in downstream classification performance.

2) In the fine-tuning stage, retaining address-related information yields spurious classification performance gains that do not survive simple protocol field randomization.

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/506bb0fab10cb4f6c1ace669f274b6ce2ca0e747b3ab98078822ac14e917b7ce.jpg)  
Fig. 13: Impact of address-related pre-training tasks on Pcap-Encoder’s performance across six traffic analysis tasks.

In the pre-training stage, Pcap-Encoder [136] is the only network foundation model (to the best of our knowledge) that explicitly incorporates address-related information into its pre-training tasks, e.g., predicting the IP source/destination addresses of packets. We pre-train two variants of Pcap-Encoder—with and without these tasks—and evaluate them on six traffic analysis tasks. As shown in Fig. 13, removing them causes an average macro F1 drop of 34.69%, e.g., from 0.9008 to 0.5020 on ISCX-VPN-Service. This also explains Pcap-Encoder’s lower performance in TABLE III, where all baselines are evaluated under our unbiased setting.

In the fine-tuning stage, we evaluate four network foundation models—NetGPT, ET-BERT, TraGe, and Traffic-Former—as TABLE III shows that they achieve markedly higher classification performance than other models. We consider three settings: (i) zeroing out address-related fields in both training and test sets, (ii) retaining address-related fields in both, and (iii) retaining address-related fields in training but randomizing them in the test set. As shown in Fig. 14, retaining address fields inflates macro F1 by 5.19% on average over zeroing them out, but once test-time address fields are randomized, macro F1 drops by 44.67% on average. This sharp degradation indicates that the gains from retaining address fields stem from shortcut learning on address-related cues rather than from learning transferable traffic semantics. Therefore, we zero out address-related protocol fields during traffic processing to ensure that the model learns transferable traffic semantics rather than address-related shortcuts, thereby providing unbiased estimates of generalization.

## B. Cross-Dataset Localized Byte-sequence Pattern

We verify that the localized byte-sequence pattern holds across datasets through quantitative analysis, supporting the four observations in Section IV-C. As conducting this analysis on every public dataset is infeasible, we select two representative datasets, i.e., USTC-TFC, which is part of our fine-tuning evaluation, and CIC-IoT, which is held out from both pre-training and fine-tuning, covering both in-evaluation and out-of-evaluation settings. We present four observation supports (OS1–OS4), each providing quantitative analysis for the corresponding observation (O1–O4) in Section IV-C.

OS1: Discriminative information is localized. We compute the Gini coefficient [48] of the byte importance score sequences to quantify how unevenly importance is distributed across byte positions. A value close to 0 indicates uniform distribution, while a value close to 1 indicates concentration on a few bytes. As shown in Fig. 15, the Gini distributions are rightskewed and consistently centered above zero on both datasets, averaging 0.2961 on USTC-TFC (Fig. 15(a)) and 0.4939 on CIC-IoT (Fig. 15(b)). The right-skewed shape indicates that the majority of traffic samples exhibit meaningful locality rather than a small fraction of outliers driving the average upward, confirming that byte importance concentration is a general property of network traffic rather than an artifact of any particular dataset.

Zero out address fields both in the training and test sets  
![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/05cf01967cc1324a00af1c36cb690baf8973e40df6fc1976e1803720df3f47b7.jpg)  
(a) DataCon

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/cc74f05543e7bea2bd028015b772bfd4ea65a3f53c54fe8fbbd184e5c90fb9b0.jpg)  
(b) CIC-EVSE

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/353ef3089b5054ed8d923df4c9123790b7fa7c373d41de10f19ba36438b18663.jpg)  
(c) CIC-IoMT

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/00e7f01fa1ce342cd847d761f37d2d67a8377f13268bf89f53417d8283b99c42.jpg)  
(d) ISCX-VPN-App

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/4731c12f220e2b3aa695bb9f9a4230867a08ce55cee6b5fb636163ef22f20ae6.jpg)  
(e) ISCX-VPN-Service

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/ac39f53322b0daf7ac62a6b015990c21a69d80b8382369dc91d4347b2743e9f1.jpg)  
(f) USTC-TFC

Fig. 14: Impact of address-related information during the fine-tuning stage across six network traffic analysis tasks.  
![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/5218f12c9930c075d4fd0aa7f36a96e8afbca3690986c5ff146e138eddfa9528.jpg)  
(a) Datasets included in the evaluation

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/d03758af0b406aa315af4d5ce5439521fe178a78610f8d7dd187258c01f4daca.jpg)  
(b) Datasets excluded from the evaluation

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/3e800fe45f852c8da3abdd629f5275f389617cc3c57704a91e637f495541ae65.jpg)  
(a) Datasets included in the evaluation

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/eaf5eb8b2f51318f697bf03844cbc866b73a1acc691f87fe7c5dfe631e49ea85.jpg)  
(b) Datasets excluded from the evaluation

Fig. 15: Distribution of Gini coefficients computed on byte importance score sequences.  
![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/0f72cdf0e36e77f50b70475362f7422b23543657aac36940ddf568a67b4f2625.jpg)  
(a) Datasets included in the evaluation

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/bb843c6666098455bb7ca2939dc775fd42e0f675af30b955d5f76957eed8688a.jpg)  
(b) Datasets excluded from the evaluation

Fig. 17: Distribution of per-sequence Gini coefficients of byte importance scores within each Top-5 protocol field.  
![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/fec2315bf2dddef0fd6bccf10611218834cddd90008e085ef3143777d28c322f.jpg)  
(a) Datasets included in the evaluation

![](../01-mineru-output/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC/images/4918d219f8821cde4426cf99aa6d22f92ca2e667891d987ff0e1dfae6d859757.jpg)  
(b) Datasets excluded from the evaluation  
Fig. 16: Distribution of pairwise Jensen-Shannon Divergence between per-class field distributions.  
Fig. 18: Hit frequency of eight address-related protocol fields in the Top-5 most important bytes.

OS2: Different categories attend to different local regions. For each traffic sample, we identify its Top-5 most important protocol fields and aggregate the field-level importance distribution per class. We then compute the pairwise Jensen-Shannon Divergence (JSD) [67] between per-class distributions for every pair of classes, where a higher JSD indicates more divergent field preferences. As shown in Fig. 16, the pairwise JSD distribution is consistently above zero across all class pairs on both datasets, with the bulk of mass concentrated at moderate-to-high divergence values. This confirms that distinct traffic classes concentrate their importance on substantially different protocol field regions, validating that localized modeling retains sufficient discriminative capacity for multi-class analysis.

OS3: Discriminative bytes are partial even within a field.

For each traffic sample, we identify the protocol fields hit by its Top-5 most important bytes and compute the Gini coefficient over the byte importance scores within each such field. As shown in Fig. 17, the field-level Gini is consistently above zero on both datasets, averaging 0.2907 on USTC-TFC (Fig. 17(a)) and 0.4389 on CIC-IoT (Fig. 17(b)), indicating that even within high-importance fields, only a subset of bytes is highly weighted. This intra-field selectivity motivates the window-wise byte scoring in Nepco, which assigns learnable per-position weights within each convolution window rather than treating all bytes uniformly.

OS4: Address fields attract disproportionate importance. For each traffic sample, we measure how often each of the eight address-related protocol fields is hit by its Top-5 most important bytes, and report the At-Least-One Hit@5 metric, defined as the fraction of traffic samples in which at least one address-related field is hit. As shown in Fig. 18, the metric reaches 0.8816 on USTC-TFC (Fig. 18(a)) and 0.9675 on CIC-IoT (Fig. 18(b)), indicating that without address zeroing, address-related fields dominate byte importance in the vast majority of traffic samples. Since these fields carry no transferable traffic semantics, this confirms that address zeroing is necessary not only for evaluation validity but also to redirect the model toward learning the class-discriminative localized traffic patterns.
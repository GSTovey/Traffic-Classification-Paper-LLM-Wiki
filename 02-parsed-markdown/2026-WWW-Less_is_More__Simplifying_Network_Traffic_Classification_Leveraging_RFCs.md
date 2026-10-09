# Less is More: Simplifying Network Trafic Classification Leveraging RFCs

NIMESHA WICKRAMASINGHE, University of New South Wales, Australia

ARASH SHAGHAGHI, University of New South Wales, Australia

ELENA FERRARI, University of Insubria, Italy

SANJAY JHA, University of New South Wales, Australia

The rapid growth of encryption has significantly enhanced privacy and security while posing challenges for network trafic classification. Recent approaches address these challenges by transforming network trafic into text or image formats to leverage deep-learning models originally designed for natural language processing, and computer vision. However, these transformations often contradict network protocol specifications, introduce noisy features, and result in resource-intensive processes. To overcome these limitations, we propose NetMatrix, a minimalistic tabular representation of network trafic that eliminates noisy attributes and focuses on meaningful features leveraging RFCs (Request for Comments) definitions. By combining NetMatrix with a vanilla XGBoost classifier, we implement a lightweight approach, LiM ("Less is More") that achieves classification performance on par with state-of-the-art methods such as ET-BERT and YaTC. Compared to selected baselines, experimental evaluations demonstrate that LiM improves resource consumption by orders of magnitude. Overall, this study underscores the efectiveness of simplicity in trafic representation and machine learning model selection, paving the way towards resource-eficient network trafic classification.

## 1 Introduction

The rapid growth of encrypted network trafic has significantly enhanced user privacy and security. However, it poses challenges for network trafic classification (NTC), a critical task for network management, security monitoring, and quality ofservice provisioning. Traditional classification methods that rely on inspecting packet payloads are rendered inefective by encryption protocols like TLS 1.3 [RFC-8446], which are designed to prevent the extraction of meaningful patterns from encrypted payloads [4].

Although many novel approaches are proposed for NTC, they often make several assumptions and employ methodologies that do not align with modern encryption specifications. Below, we present the resultant chal lenges (C) in NTC by comparing widespread assumptions with modern-day RFCs.

C1.Assumption of implicit patterns in encrypted payloads: Many models operate under the premise that encrypted payloads contain exploitable patterns for classification [4, 9]. This contradicts the TLS 1.3 specification [RFC-8446], which ensures that the same plaintext will always produce diferent ciphertexts due to the use of Authenticated Encryption with Associated Data (AEAD) ciphers and unique initialization vectors (IVs).

C2.Fixed-Size homogeneous representation of payloads: Studies often truncate or pad payloads to create fixed-size inputs. This approach ignores TLS 1.3’s acknowledgment that encrypted packet lengths and timing are susceptible to trafic analysis attacks [RFC-8446]. Padding or truncation does not efectively exploit this vulnerability and may obscure valuable size-related artifacts essential for classification.

C3.Inclusion of header withoutjustification: Including header fields such as IP Identification (IP-ID) [RFC 6274], IP header checksum [RFC-791], sequence and acknowledgment numbers [RFC-9293], and TCP options timestamps [RFC-7323] introduces noise. These fields often contain pseudo-random values initialized per session, adding unnecessary variability to the data.

C4.Representation of network trafic as text or images: Transforming network trafic into textual or visual formats to leverage semantic, syntactic, or spatial relationships using foundation models (e.g., BERT, vision transformers) can hinder the inherent structure of network protocols. Unlike natural language tokens or image pixels, network header attributes typically lack interdependencies, making such representations less efective.

C5.Reliance on TCP/TLS handshake packets: Some classifiers [9] depend on initial handshake packets for classification. However, mechanisms like TCP connection reuse [RFC-9293], TLS 1.3’s 0-RTT data transmis sion, and session resumption via Pre-Shared Keys (PSKs) [RFC-8446] allow communication without frequent handshakes. Consequently, classifiers that rely on handshake packets may fail in these common scenarios.

These challenges underscore the need for a practical and eficient approach to NTC. To bridge this gap, we propose NetMatrix, a novel tabular representation that focuses on capturing meaningful features of network trafic leveraging RFC specifications (§3.1). NetMatrix, paired with a vanilla XGBoost classifier, referred to as LiM <sup>1</sup> (Less is More) (§3.2), achieves performance comparable to resource-intensive deep-learning models while maintaining significantly lower computational overhead (§4.3.1). Moreover, our approach demonstrates the ability to handle high volumes of requests, adapt to new trafic classes within seconds, and operate with enhanced memory and energy eficiency (§4.3.2).

## 2 Literature Review

Encrypted NTC has been a well-researched topic, with numerous models proposed to address the complexities of encryption protocols like TLS 1.3. Notably, methods such as ET-BERT [4] and YaTC [8] have leveraged sophisticated deep learning techniques to classify encrypted trafic efectively.

ET-BERT [4] applies Bidirectional Encoder Representations from Transformers (BERT), originally developed for natural language processing (NLP). The method assumes that encrypted payloads contain implicit patterns that can be exploited for classification (𝐶1). The best performing version ofET-BERT (ET-BERT Packet-wise classifier) truncates payloads and represent network trafic using 128 bytes per packet (𝐶2). This method involves converting binary raw data (i.e. header and encrypted payload) into sequences of tokens. The consequent transformation aims to capture semantic and syntactic relationships within transformed network trafic, analogous to words and sentences in natural language (𝐶4).

Similarly, YaTC [8] proposes representing network trafic as images and employs Masked Autoencoders (MAEs) for classification. Each network session is represented by 1,600 bytes ofraw data, arranged into two-dimensional matrices to form images. This approach attempts to exploit spatial relationships within the transformed network trafic (𝐶4). For trafic representation, YaTC relies on the first 5 packets of a network trafic session (𝐶5).

While ET-BERT and YaTC are known for their great performance [5, 6], other studies have also explored various aspects of encrypted NTC using raw packet data without justifications [3, 7] (𝐶3). However, most existing models for encrypted NTC often face challenges due to their: (1) reliance on encrypted payload content, (2) improper handling of data representations, (3) inclusion of noisy header information, (4) misalignment with protocol specifications, and (5) dependency on handshake packets.

Our work distinguishes itself by fundamentally rethinking the assumptions in the context of modern encryption standards. By aligning our methodology with RFCs and focusing on meaningful, structured data represen tations, we aim to provide a more efective and lightweight solution to encrypted network trafic classification.

## 3 Methodology

In this section, we present our proposed methodology for eficient encrypted network trafic classification. In §3.1, we introduce NetMatrix, the representation that captures the essential features of network trafic according to RFCs. Building upon this representation, in §3.2, we explain the machine learning model selection for experimental evaluation.

## 3.1 NetMatrix

NetMatrix is a concise tabular representation of network trafic designed to overcome the limitations of existing NTC methods. The proposed representation is built upon the following principles aligning to modern-day RFCs such as, RFC-8446, RFC-2328, RFC-4271, RFC-6247, RFC-791, RFC-9293, RFC-7323:

Exclusion of Encrypted Payloads: Recognizing that encrypted payload content lacks exploitable patterns as per TLS 1.3 specifications [RFC-8446], we entirely exclude it from NetMatrix to address (𝐶1).

Utilization of Encrypted Payload Length and Timing: Acknowledging that TLS 1.3 highlights the susceptibility of encrypted packet lengths and timings to trafic analysis attacks [RFC-8446], we incorporate these attributes and solve (𝐶2). Specifically, we use the total length field from the IP header and calculate the interarrival times between packets.

Reduction of Representation Size: By excluding noisy, session-specific header fields—such as IP Identification (IP-ID), checksums, sequence numbers, and TCP timestamps, we focus on stable, meaningful header attributes aligning to RFCs. This reduction minimizes noise and enhances classification performance by concen trating on relevant data, resolving (𝐶3).

Preservation of Inherent Network Trafic Schema: Instead of transforming network trafic into text or images, which can obscure protocol structures, NetMatrix maintains the inherent schema by using a tabular format as a remedy for (𝐶4). This representation preserves the relationships defined by network protocols.

Reliance on Packets Containing Encrypted Data: To ensure practicality, we base our classification on packets that contain encrypted payloads. This approach remains efective even when handshake packets are unavailable as a solution to (𝐶5).

NetMatrix utilizes only three key attributes extracted from network packets to represent a session:

Total Length (IP Header): The total length field in the IP header indicates the size of the entire IP packet, including both the header and the payload.

Time-to-Live (TTL) (IP Header): The TTL field represents the maximum number of hops a packet can traverse before being discarded. While TTL values can vary due to routing changes, they are generally consistent for packets taking the same route between two endpoints. Routing protocols aim for minimal overhead, so minor route fluctuations have limited impact on the TTL upon arrival [RFC-2328, RFC-4271]. Therefore, TTL can provide useful information about network path characteristics.

Inter-Arrival Time: This attribute measures the time diference between two consecutive packets.

NetMatrix represents each network trafic session (i.e., a bidirectional flow between two endpoints) by extracting the aforementioned attributes from five consecutive packets containing encrypted payloads. For each packet, we collect: Total Length (2 bytes), TTL (1 byte), Inter-Arrival Time (calculated, 3 bytes). This results in a compact representation of 30 bytes per session, significantly reducing the data volume compared to existing methods. For instance, ET-BERT uses 620 bytes, and YaTC requires 1,600 bytes to represent a session.

## 3.2 LiM

To complement the eficient representation provided by NetMatrix, we employ a vanilla XGBoost classifier [1]. A highlighted by [2], tree-based models, such as XGBoost, are particularly adept at learning irregular patterns in the target function, and demonstrate superiority on tabular data. This insight justifies our selection of the XGBoos classifier in this study. Its inductive biases make it inherently well-suited for the structured nature of NetMatrix, enabling eficient and accurate classification without requiring the computational resources demanded by deep learning models.

We refer to the integration of NetMatrix with the XGBoost classifier as LiM (Less is More). By utilizing LiM, we demonstrate that a simple machine learning model can achieve performance comparable to state-of-the-art deep learning approaches, such as ET-BERT and YaTC, without the need for complex architectures or extensive computational resources.

## 4 Experimental Evaluation

To validate the efectiveness and eficiency of our proposed approach, we conduct an experimental evaluation focusing on encrypted trafic adhering to TLS 1.3. Our evaluation consists of two main components: (1) assessing classification performance, and (2) analyzing resource consumption.

We utilize the CSTNET-TLS1.3 dataset [4], introduced in the ET-BERT study, which comprises network trafic encrypted with TLS 1.3. This dataset is well-suited for our evaluation as it reflects modern encryption protocols and the associated challenges in NTC. To address the class imbalance issue, we randomly select 10 classes from the dataset, each containing more than 400 samples. For an unbiased evaluation, we provide 400 samples per class to each classifier. This equal provision ensures that no class dominates the training process, and facilitates a fair assessment of resource consumption.

## 4.1 Experimental Setup

4.1.1 Hardware Configuration. : The experiments were conducted on a machine equipped with dual Intel Xeon Silver 4208 CPUs operating at a base clock of 2.10 GHz, with a maximum clock speed of 3.20 GHz. Each processor features 8 cores per socket, for a total of 16 physical cores and 32 threads. The system is equipped with 125 GiB of RAM. For GPU acceleration, the machine houses four NVIDIA Tesla T4 GPUs, each with 16 GiB of dedicated memory, summing up to a total GPU memory capacity of 64 GiB. The GPUs have a maximum power draw capacity of 70W each.

4.1.2 Soware Configuration. : The system runs on Ubuntu 24.04.1 LTS (Noble) as the operating system. The software environment includes Python 3.13.0 as the programming language and the XGBoost 2.1.2 library for implementing and training LiM.

For a comparative analysis, we also evaluated state-of-the-art models ET-BERT and YaTC using their recommended configurations. These models were executed on the same experimental setup to ensure a fair and consistent comparison across diferent classifiers

## 4.2 Evaluation Metrics

The evaluation encompassed both classification performance and resource consumption to provide a comprehensive assessment of each selected model’s efectiveness. For classification performance, we employed standard metrics including accuracy, precision, recall, and F1 score.

Regarding resource consumption, we evaluated latency, memory usage, energy consumption, and throughput. Latency was measured as the time taken by the classifier to process a single input during training, calculated by dividing the total time by the number of training samples. The rest of the matrices were measured during the inference phase. Memory usage referred to the amount of RAM+GPU consumed, an important factor for deployment on devices with limited resources. Energy consumption represented the amount of energy used by the GPU, reflecting the operational cost and sustainability of the model. Throughput indicated the number of inferences the classifier could make per second, providing insight into its ability to handle high-volume trafic, which is essential for network environments with heavy loads.

Table 1. Classification Performance Comparison

<table><tr><td>Model</td><td>Accuracy</td><td>Recall</td><td>Precision</td><td>F1 Score</td></tr><tr><td>ET-BERT [4]</td><td>0.568</td><td>0.568</td><td>0.581</td><td>0.569</td></tr><tr><td>YaTC [8]</td><td>0.963</td><td>0.963</td><td>0.964</td><td>0.963</td></tr><tr><td>LiM</td><td>0.942</td><td>0.942</td><td>0.943</td><td>0.942</td></tr></table>

Table 2. Scalability Comparison

<table><tr><td>Model</td><td>Latency (Sec/Sample)</td><td>Memory (MiB)</td><td>Energy (Watt)</td><td>Throughput (Sample/Sec)</td></tr><tr><td>ET-BERT [4]</td><td>0.4328</td><td>15,189.48</td><td>109</td><td>164.91</td></tr><tr><td>YaTC [8]</td><td>0.1342</td><td>5,352.25</td><td>26</td><td>636.62</td></tr><tr><td>LiM</td><td>0.0005</td><td>196.38</td><td>0</td><td>86,251.23</td></tr></table>

## 4.3 Results and Analysis

## 4.3.1 Classification Performance.

The results, as presented in Table 1, demonstrate the performance of ET-BERT, YaTC, and the proposed LiM classifier.

ET-BERT achieves a classification accuracy of 0.568, with recall and F1 score also at 0.568 and 0.569, respectively, while precision is marginally higher at 0.581. The underperformance is likely due to the constrained training setup (400 samples per class) provided for a fair evaluation across all models.

In contrast, the YaTC model performs significantly better, achieving an accuracy and F1 score of 0.963.

The proposed LiM classifier, when paired with the NetMatrix representation, achieves competitive results with an accuracy of 0.942 and an F1 score of 0.942. Precision and recall are also closely matched at 0.943 and 0.942, respectively, underscoring the model’s robustness across all evaluation metrics.

While LiM slightly trails YaTC in overall performance, its results highlight the strength ofa simple yet efective approach. The combination of the NetMatrix representation and the XGBoost classifier demonstrates that high classification performance can be achieved without reliance on complex architectures, ofering a compelling balance between accuracy and simplicity.

## 4.3.2 Resource Consumption.

The lightweight XGBoost classifier, when paired with the NetMatrix representation (LiM), demonstrates less resource consumption across all evaluated metrics, as shown in Table 2

LiM’s latency is remarkably low at 0.0005 seconds per sample, enabling it to process inputs with near-instantaneous speed. In comparison, ET-BERT exhibits a latency of 0.4328 seconds, which is 86,560% higher, while YaTC has a latency of 0.1342 seconds, 26,840% higher than LiM. This reduction in latency underscores the suitability of LiM for real-time applications where low training times are critical.

In terms of memory usage, LiM consumes only 196.38 MiB of RAM during inference. This represents a signif icant improvement over ET-BERT, which requires 15,189.48 MiB, a 7,735% increase, and YaTC, which consumes

5,352.48 MiB, a 2,725% increase. This low memory footprint makes LiM suitable for deployment on devices with limited computational resources, such as edge devices or IoT systems.

LiM, eliminates the need for GPU utilization during inference, resulting in zero measurable energy consumption. In contrast, ET-BERT consumes 109 watts, while YaTC consumes 26 watts, reflecting operational costs.

Finally, LiM achieves a throughput of 86,251.23 samples per second, demonstrating its ability to handle high trafic volumes. This throughput is 52,302% higher than ET-BERT’s throughput of164.91 samples per second and 13,548% higher than YaTC’s throughput of 636.62 samples per second. The diference in throughput emphasizes LiM’s potential capability for high-demand environments, such as real-time network monitoring and large-scale trafic analysis.

While maintaining competitive classification performance, LiM significantly reduces resource consumption across all dimensions, achieving faster processing, lower memory usage and minimal energy requirements. This makes LiM a practical and sustainable solution for encrypted network trafic classification, particularly in resource-constrained and real-time settings.

## 5 Conclusion and Future Work

This paper addresses critical challenges in encrypted network trafic classification (NTC), including unrealistic assumptions about patterns in encrypted payloads, reliance on noisy or non-informative features, truncation/padding ofpayload data, and the computational ineficiencies ofdeep-learning-based methods. As a solution, we introduce NetMatrix, a streamlined tabular representation of network trafic, designed by leveraging mod ern RFC specifications to focus on meaningful and protocol-compliant attributes. Paired with a vanilla XGBoost classifier, this integration referred to as LiM (Less is More), demonstrates that simplicity can rival complexity.

Experimental evaluations show that LiM delivers competitive classification performance compared to stateof-the-art methods such as, ET-BERT and YaTC, while reducing computational overhead by orders ofmagnitude. These findings emphasize the importance of RFC-compliant trafic representations in tackling the complexities of encrypted NTC, ofering a lightweight solution.

Despite its promise, this study is limited to the CSTNET-TLS1.3 dataset. Future work will expand the approach to a broader range of datasets, encompassing diverse trafic patterns, encryption protocols, and real-world net work conditions. This will ensure LiM’s robustness across various network environments. Additionally, LiM will be evaluated against a wider array of state-of-the-art classifiers to refine its methodology and validate its eficiency further.

By emphasizing the utility of RFC-aligned representations and pursuing these directions, we aim to present LiM as a resource-eficient solution for encrypted NTC across diverse and evolving network landscapes.

## References

[1] Tianqi Chen and Carlos Guestrin et al. 2016. XGBoost: A Scalable Tree Boosting System. In Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining.

[2] Léo Grinsztajn and Edouard Oyallon et al. 2024. Why do tree-based models still outperform deep learning on typical tabular data?. In Proceedings of the 36th International Conference on Neural Information Processing Systems.

[3] Zijun Hang and Yuliang et al Lu. 2023. Flow-MAE: Leveraging Masked AutoEncoder for Accurate, Eficient and Robust Malicious Trafic Classification. In Proceedings of the 26th International Symposium on Research in Attacks, Intrusions and Defenses.

[4] Xinjie Lin and Gang Xiong et al. 2022. ET-BERT: A Contextualized Datagram Representation with Pre-training Transformers for En crypted Trafic Classification. In Proceedings ofthe ACM Web Conference 2022.

[5] Chen Qian and Xiaochang et al Li. 2024. NetBench: A Large-Scale and Comprehensive Network Trafic Benchmark Dataset for Foundation Models . In 2024 IEEE International Workshop on Foundation Models for Cyber-Physical Systems & Internet ofThings (FMSys).

[6] Tongze Wang and Xiaohui Xie et al. 2024. NetMamba: Eficient Network Trafic Classification via Pre-training Unidirectional Mamba.

[7] Haozhen Zhang and Le Yu et al. 2023. TFE-GNN: A Temporal Fusion Encoder Using Graph Neural Networks for Fine-grained Encrypted Trafic Classification. In Proceedings ofthe ACM Web Conference 2023.

[8] Ruijie Zhao and Mingwei Zhan et al. 2023. Yet Another Trafic Classifier: A Masked Autoencoder Based Trafic Transformer with Multi-Level Flow Representation. Proceedings ofthe AAAI Conference on Artificial Intelligence (2023).

[9] Ruijie Zhao and Mingwei Zhan et al. 2024. A Novel Self-Supervised Framework Based on Masked Autoencoder for Trafic Classification. IEEE/ACM Transactions on Networking (2024).
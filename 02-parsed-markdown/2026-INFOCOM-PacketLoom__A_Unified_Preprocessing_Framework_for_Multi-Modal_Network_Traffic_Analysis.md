# PacketLoom: A Unified Preprocessing Framework for Multi-Modal Network Traffic Analysis

Long Li<sup>1</sup>, Guanping Liang<sup>1</sup>, Sudan Li<sup>2</sup>, Biao Han<sup>1,\*</sup>, Xiaoyan Wang<sup>3</sup>

<sup>1,2</sup>College of Computer Science and Technology, National University of Defense Technology, Changsha, 410073, China

<sup>3</sup>Graduate School of Science and Engineering, Ibaraki University, Ibaraki, 316-8511, Japan

Email: <sup>1</sup>{longli, liangguanping22, nudtbill}@nudt.edu.cn, <sup>2</sup>nudtlsd@163.com, <sup>3</sup>xiaoyan.wang.shawn@vc.ibaraki.ac.jp

Abstract—The rise of foundation models in network traffic analysis (NTA) has exposed a critical weakness in data engineering: the preprocessing workflow is severely fragmented. Current practices suffer from an “engineering gap” where tools are isolated by modality, logic is hard-coded into fragile scripts, and iteration is slowed by inefficient caching. To address this, we propose PacketLoom, a unified framework built on a decoupled definitionexecution architecture. Instead of complex scripts, PacketLoom uses a declarative orchestrator to define pipelines, paired with a polymorphic stack that handles multi-modal data uniformly. A specialized transient-resident runtime further optimizes resource usage, enabling rapid experimentation. Evaluations on the ISCX-VPN dataset show that PacketLoom improves downstream model performance (+1.14% F1 for sequential tasks) while reducing code volume by 87.5% and cutting I/O overhead by 16.3× (in spatial tasks).

Index Terms—Network Traffic Analysis, Foundation Models, Data Preprocessing, Multi-modal Learning

## I. INTRODUCTION

Network traffic analysis (NTA) is the cornerstone of network defense. While NTA historically relied on deep packet inspection (DPI), it now faces a major challenge: Transport Layer Security (TLS) encrypts over 90% of web traffic [1]. This “encryption barrier” makes traditional signature matching ineffective, forcing a shift from inspecting payloads to analyzing behavioral patterns. Driven by the success of Deep Learning (DL), the field is now actively exploring foundation models [2] to achieve generalized traffic understanding.

To penetrate this barrier, the research community has innovated by interpreting encrypted traffic through various multimodal lenses. The statistical paradigm [3]–[5] characterizes flows via aggregated metadata, providing the feature basis for classical Machine Learning (ML). The sequential paradigm [6]–[8] treats traffic as ordered sequences, treating packet bytes as “words” to leverage sequence models (e.g., RNNs, Transformers). The spatial paradigm [9]–[11] visualizes traffic as 2D artifacts, enabling Convolutional Neural Networks (CNNs) or Vision Transformers (ViTs) to capture spatial correlations. Finally, the topological paradigm [12]–[14] utilizes graph neural networks (GNNs) to model interaction dynamics, though its structural definitions remain highly heterogeneous compared to the established paradigms.

However, the performance of these advanced models relies heavily on high-quality data engineering, whether extracting precise byte sequences or rasterizing flow images. Yet, a mismatch remains: while analysis methods have evolved into complex, multi-modal systems, the tools for processing traffic data remain fragmented and basic (Table I).

Legacy statistical exporters. Tools like CICFlowMeter [15] and NFStream [16] excel at aggregating flow statistics but are inherently lossy. They discard payload information, rendering them unsuitable for sequential or spatial paradigms that require semantic or pixel-level fidelity.

Log-centric analyzers. Zeek [17] generates rich semantic logs for forensics but is not tensor-native. Parsing verbose text logs incurs high overhead and destroys the compact structure of raw packets required for efficient Deep Learning.

Ad-hoc scripting. Lacking general-purpose toolkits, researchers build project-specific pipelines using libraries like Scapy<sup>1</sup>. They often deploy custom scripts that intertwine extraction logic with control flow and hard-coded parameters (e.g., absolute paths). While sufficient for initial evaluations, such non-standardized, rigid workflows are difficult to maintain or reuse across different experiments.

TABLE I  
COMPARISON OF NTA PREPROCESSING FRAMEWORKS

<table><tr><td>Capability</td><td>CIC</td><td>NFStream</td><td>Zeek</td><td>Scapy</td><td>PacketLoom</td></tr><tr><td>Statistical</td><td>✓</td><td>✓</td><td> $\bigtriangleup$ </td><td>✘</td><td>✓</td></tr><tr><td>Sequential</td><td>✘</td><td> $\bigtriangleup$ </td><td>✘</td><td>✘</td><td>✓</td></tr><tr><td>Spatial</td><td>✘</td><td>✘</td><td>✘</td><td>✘</td><td>✓</td></tr><tr><td>Output</td><td>CSV</td><td>DF</td><td>Log</td><td>Pkt Obj</td><td>Tensor</td></tr><tr><td>Tensor-Native</td><td>✘</td><td>✘</td><td>✘</td><td>✘</td><td>✓</td></tr></table>

✓: Supported, ✗: No/Manual, △: Partial/Inefficient.

This lack of unified tools creates a severe “engineering gap” that fundamentally complicates the production of high-quality datasets. Consequently, we identify three primary challenges:

• C1: Fragmented tools. Existing tools are typically designed for a single modality. For example, a tool optimized for flow statistics often cannot handle the bytelevel tokenization needed for transformers or the image generation required for CNNs. This fragmentation forces researchers to maintain separate, incompatible toolchains for different models.

• C2: Hard-coded logic. Common ad-hoc scripts mix data definition (what to extract) with execution logic (how to read files). Extraction rules are often buried within file processing loops, making the code fragile. A simple parameter change can require editing core logic, making these scripts hard to maintain or reuse across projects.

• C3: Iteration friction. Existing pipelines suffer from severe I/O bottlenecks that hinder rapid experimentation. This manifests in two ways: processing the full data corpus upfront even when only a small fraction is ultimately needed, and strictly dumping all intermediate features to disk before training. Such rigid workflows force timeconsuming regenerations upon even minor configuration changes.

To bridge this gap, we propose PacketLoom<sup>2</sup>, a unified framework built upon a novel decoupled definition-execution architecture. As illustrated in Fig. 2, the framework harmonizes two core components to resolve the engineering gap: (1) The declarative orchestrator addresses usability and robustness by abstracting pipelines into configuration rules; and (2) The polymorphic processing stack addresses fragmentation and iteration friction. By employing a transient-resident runtime, the processing stack enables agile iteration while preserving unified processing capabilities across statistical, sequential, and spatial paradigms.

Our key contributions are summarized as follows:

• Multi-modal versatility: We address toolchain fragmentation (C1) by establishing a universal NTA preprocessing framework. We demonstrate that PacketLoom can faithfully reproduce statistical, sequential, and spatial paradigms with rigorous implementation, ensuring high semantic fidelity (e.g., effectively correcting protocol noise in Email classification tasks).

• Engineering usability: We resolve the coupling of definition and execution (C2) by transforming fragile adhoc scripts into simple, engineering-grade pipelines via the declarative orchestrator. This approach significantly enhances maintainability, achieving an 87.5% reduction in boilerplate code.

• Iteration efficiency: We overcome iteration friction (C3) via a transient-resident runtime that minimizes I/O overheads. By employing select-first processing strategy to avoid full-corpus traversal, and bypassing redundant intermediate disk caching, PacketLoom accelerates end-to-end processing by 2.1× (ET-BERT) and reduces disk reads by 16.3× (YaTC).

The remainder of this paper is organized as follows. Section II details the PacketLoom architecture and its transient-resident runtime. Section III presents the evaluation results on multimodal versatility, engineering usability, iteration efficiency, and discusses current limitations, followed by the conclusion in Section IV.

![](images/e871338347f2f65d33caaeb58b66019e6579b11143cf020e0a7fbc3e80b25ab0.jpg)  
Fig. 1. Configuration for YaTC Reproduction

## II. THE PROPOSED PACKETLOOM ARCHITECTURE

PacketLoom bridges the engineering gap through a decoupled definition-execution architecture. As illustrated in Fig. 2, the framework combines two core components: a declarative orchestrator that ensures engineering usability by decoupling definition from execution, and a polymorphic processing stack, powered by a transient-resident runtime, that guarantees multimodal versatility. These components work together to ensure efficiency: the orchestrator enables flexible logic adaptation, while the runtime minimizes execution latency.

## A. Declarative Orchestrator

To address the rigidity of ad-hoc scripting, this component completely decouples pipeline definition from execution. Instead of hard-coding logic, users define data flows via declarative YAML rules. This configuration-driven approach is pivotal for iteration efficiency, allowing researchers to rapidly pivot between experimental settings without code refactoring. The orchestrator parses these rules and dynamically instantiates the processing chain via a module registry, which maps configuration strings to executable logic. This design allows researchers to inject custom modules without modifying the core framework kernel.

As a concrete example, Fig. 1 illustrates the configuration for reproducing the YaTC [11] spatial pipeline. By abstracting complex logic—such as session reassembly, payload truncation, and spatial rasterization—into declarative rules, this approach eliminates error-prone boilerplate code. It ensures strict reproducibility by making critical parameters (e.g., image dimensions and split ratios) explicit, allowing researchers to validate and modify experiments effortlessly without navigating the underlying codebase.

![](images/caccbbb8d715e6a41e185f3dd5f3cb15d51c0d879198f685bcbb3cbce2d60f4a.jpg)  
Fig. 2. The Architecture of PacketLoom. The system comprises three logical layers: (1) Unified ingestion layer handles physical normalization and stream filtering in a lazy manner; (2) Polymorphic representation layer generates multi-modal tensors via paradigm-specific generators; (3) Refinement & export layer performs in-memory refinement and serializes data into model-ready artifacts.

## B. Polymorphic Processing Stack and Runtime

The polymorphic processing stack executes multi-modal data pipelines through a unified three-layer structure (as detailed in Fig. 2), which is comprehensively powered by a transient-resident runtime.

1) Layer I: Unified Ingestion: This layer serves as the physical normalization engine, abstracting heterogeneous data sources into a standard stream.

• Physical normalizer: To address format fragmentation, the PcapngConverter standardizes diverse capture files, while the Reassembler (wrapping session-layer tools) reconstructs complete logical TCP/UDP sessions from fragmented packet dumps.

• Universal adapter: The BatchPcapLoader functions as the high-throughput ingestion engine. It virtualizes the file system into an infinite TrafficStrand stream, decoupling downstream processors from the underlying physical storage layouts.

• Stream filters: A suite of filters ensures data quality. The PacketFilter removes malformed traffic, while the FlowBurstSplitter handles temporal segmentation (e.g., splitting long-lived flows by timeout), essential for fine-grained behavioral analysis. Finally, the Anonymizer ensures privacy compliance.

2) Layer II: Polymorphic Representation: The core transformation engine features modular “generator banks” that synthesize normalized streams into paradigm-specific tensors.

• Sequential generators: Designed for sequence models. The ByteSeqGen transforms traffic flows into numerical byte sequences via configurable packet sampling, structural extraction (e.g., header/payload split), and adaptive padding/truncation. The TokenSeqGen integrates vocabulary mapping (e.g., HEX-pairs or BERT tokens). Additionally, the StatSeqGen produces statistical time-series (e.g., packet lengths or inter-arrival times), enabling signal-processing approaches.

• Spatial generators: Tailored for computer vision models. The ByteImgGen folds 1D packet streams into 2D rasterized images; the TimeSeriesImgGen converts temporal sequences into visual fields; and the StatImgGen visualizes statistical feature matrices.

• Statistical generators: Developed for classical ML models. It includes: TabularFeatureExtractor for standard flow statistics; ProtocolFieldExtractor for parsing specific fields (e.g., SNI); and Custom FeatureExtractor, an interface for executing userdefined logic.

Remark on topological paradigms: Due to extreme structural heterogeneity in NTA graphs—where node and edge definitions vary drastically across tasks [12]–[14]—enforcing a static topological generator limits flexibility. Instead, PacketLoom delegates topology orchestration to downstream logic. The framework currently focuses on extracting standardized multi-modal representations (e.g., statistical, sequential), which researchers can flexibly map to either node attributes or edge weights for their bespoke GNN designs.

3) Layer III: Refinement and Export: This layer ensures data integrity by isolating transformations to prevent leakage. It refines feature distributions and serializes the dataset into optimized formats for diverse training backends.

• Leakage-free refiners: Unlike rigid ad-hoc scripts, modules such as Normalizer, ImbalanceHandler, and FeatureSelector are fully dataset-aware. They automatically identify training splits to fit parameters (e.g., scalers), subsequently applying them to test sets to strictly prevent data leakage.

• Exporters: The pipeline concludes with versatile serialization. The TensorExporter produces efficient binary tensors (.npy); the VisualArtifactExporter organizes rasterized data into framework-native folder structures; and the TabularExporter generates standard CSV files for classical statistical analysis.

4) Transient-Resident Execution Mechanism: To efficiently support the polymorphic stack under strictly bounded memory constraints, PacketLoom implements a specialized transientresident runtime environment (Algorithm 1):

• Transient zone: The ingestion and representation layers operate on a transient stream. Here, data flows as TrafficStrand objects—heavy abstractions encapsulating raw packets and metadata. These objects are instantiated on-demand via Python generators and are subjected to active garbage collection immediately after processing, ensuring a constant (O(1)) transient memory footprint relative to dataset size.

• Resident zone: Upon tensor generation, the lightweight feature vectors are materialized into a tensor buffer (RAM). This in-memory materialization is essential for enabling downstream global operations, such as stratified splitting and global normalization. These operations require a complete view of the dataset and random access, which are unattainable in a pure stream.

## C. Theoretical Formulation and Analysis

We provide a formal analysis of PacketLoom’s unified representation capability and its efficiency guarantees.

1) Unified Representation Modeling: Let D be the raw traffic stream and C be the configuration context. PacketLoom defines a unified transformation operator Φ that maps the raw stream to a target tensor $\mathcal { T } _ { m }$

$$
\mathcal {T} _ {m} = \Phi (\mathcal {D}, \mathcal {C}), \quad m \in \{\text { Seq }, \text { Spa }, \text { Stat } \}\tag{1}
$$

Unlike ad-hoc scripts hardcoded for specific tasks, Φ is a generic composition of strictly defined sub-operators: Normalizers N, polymorphic generators $G _ { \mathcal { C } }$ , and refiners $R _ { \cal { C } }$ :

$$
\Phi = R _ {\mathcal {C}} \circ G _ {\mathcal {C}} \circ N\tag{2}
$$

This abstraction allows researchers to switch paradigms (e.g., from statistical to spatial) simply by modifying C, without altering the underlying code structure.

2) Efficiency and Complexity Analysis: We formalize the optimization goal as minimizing total latency $T _ { t o t a l }$ subject to a hard memory constraint $M ( t ) \leq M _ { d e v }$

Time Efficiency: Existing pipelines often compromise efficiency by relying on intermediate disk caching. The baseline latency $T _ { b a s e }$ is dominated by the I/O overhead of these intermediate states:

```txt
Algorithm 1 Transient-resident execution
Input: Configuration C, Raw Dataset D
Output: Model-Ready Tensor Set T
1: Phase 1: Initialization
2: Π ← LoadModules(C) // Instantiate generator chain
3: B ← NewTensorBuffer() // Alloc tensor storage
4: Phase 2: Transient Stream Processing (Layer I & II)
5: S ← StreamIngest(D) // Yields heavy TrafficStrand
6: for strandheavy in S do
7:    strandnorm ← Π.Normalize(strandheavy)
8:    tlight ← Π.Generate(strandnorm) // Map to tensor
9:    if tlight ≠ ∅ then
10:    B.Append(tlight) // Materialize into Tensor Buffer
11:    end if
12:    ActiveGC(strandheavy) // Free raw memory immediately
13: end for
14: Phase 3: Refinement (Layer III)
15: Dmatrix ← Stack(B) // Form contiguous tensor
16: Dtrain, Dtest ← Split(Dmatrix, C.ratio)
17: return Serialize(Dtrain, Dtest, C.format)
```

$$
T _ {b a s e} = T _ {p r o c e s s} + T _ {o v e r h e a d} (\mathbf {I} / \mathbf {O} _ {d i s k})\tag{3}
$$

PacketLoom mitigates this redundancy via the transientresident runtime. By enforcing a transient processing policy for intermediate objects, we achieve:

$$
T _ {o u r s} \approx T _ {p r o c e s s} \ll T _ {b a s e}\tag{4}
$$

Space Complexity: The peak memory $M _ { p e a k } ^ { P L }$ is the sum of the transient zone overhead and the resident tensor buffer. Let $S _ { r a w }$ be the input size and σ be the feature compression ratio $( \sigma \ll 1 )$

$$
M _ {p e a k} ^ {P L} = \underbrace {M _ {t r a n s i e n t}} _ {\approx \text {const}} + \underbrace {M _ {r e s i d e n t}} _ {\sigma \cdot S _ {r a w}}\tag{5}
$$

where $M _ { t r a n s i e n t }$ is the active streaming window memory and $M _ { r e s i d e n t }$ is the tensor buffer. The transient zone ensures that raw flow objects are strictly bounded, while the resident zone only accumulates compact tensors. This design ensures that $M _ { p e a k } ^ { \bar { P } L }$ remains within RAM limits $( M _ { l i m i t } )$ for large-scale datasets, enabling the critical shift from I/O-bound to memorybound execution.

## III. EVALUATION

We evaluate PacketLoom across four dimensions corresponding to our core contributions and broader impact: (1) multi-modal versatility, ensuring semantic fidelity for SOTA models; (2) engineering usability, quantifying the reduction in engineering overhead; (3) iteration efficiency, measuring the mitigation of I/O bottlenecks; and (4) discussion, analyzing current limitations and future works.

## A. Experimental Setup

Experiments utilize the ISCX-VPN dataset [18], specifically the Service-level subset defined by ET-BERT [7]. We benchmark against two protocols on an Intel i9-14900K (64GB RAM) Linux server: 1) ET-BERT (end-to-end): Representative of the packet-level sequential paradigm. We compare the full pipeline against the official script (patched for PCAPNG). 2) YaTC (rasterization phase) [11]: Representative of the flowlevel spatial paradigm. We measure rasterization efficiency by feeding both systems identical pre-split PCAPs.

While PacketLoom supports the statistical paradigm, we focus on sequential and spatial paradigms. These modalities impose significantly higher I/O demands, serving as stricter benchmarks for efficiency and fidelity.

## B. Multi-modal Versatility

We fine-tuned ET-BERT and YaTC using datasets generated by Baseline scripts and PacketLoom configuration files. Table II shows the results.

1) Sequential Paradigm (ET-BERT): PacketLoom achieves a +1.20% Accuracy and +1.14% F1-Score boost. This improvement stems from PacketLoom’s rigorous data quality control. Unlike the baseline scripts which indiscriminately extract bytes, PacketLoom’s filters enforce protocol validation (e.g., ensuring IPv4) and prune empty payloads, effectively denoising the training corpus.

2) Spatial Paradigm (YaTC): PacketLoom maintains strict parity (78.41% vs 78.31% accuracy), confirming that our ByteImgGen correctly implements spatial folding without introducing artifacts. In conclusion, the “universal adapter” design introduces zero fidelity loss.

3) Case Study: Protocol Validation Impact: Analyzing the per-class performance for ET-BERT reveals a significant +15.9% F1 increase for the Email class. Inspection shows the raw dataset contains high volumes of non-IP traffic (e.g., ARP) and empty payloads. The baseline script indiscriminately extracts bytes from these packets, introducing noise. In contrast, PacketLoom’s PacketFilter and ByteSeqGen strictly enforce IPv4 validation and payload length checks, purifying the training signal and enhancing model robustness.

TABLE II  
DOWNSTREAM MODEL PERFORMANCE COMPARISON

<table><tr><td>Model Paradigm</td><td>Metric</td><td>Baseline</td><td>PacketLoom</td><td>Diff</td></tr><tr><td rowspan="4">ET-BERT(Sequential)</td><td>Accuracy</td><td>90.27%</td><td>91.47%</td><td>+1.20%</td></tr><tr><td>Precision</td><td>91.41%</td><td>92.42%</td><td>+1.01%</td></tr><tr><td>Recall</td><td>90.33%</td><td>91.51%</td><td>+1.18%</td></tr><tr><td>F1-Score</td><td>90.22%</td><td>91.36%</td><td>+1.14%</td></tr><tr><td rowspan="4">YaTC(Spatial)</td><td>Accuracy</td><td>78.31%</td><td>78.41%</td><td>+0.10%</td></tr><tr><td>Precision</td><td>77.78%</td><td>78.00%</td><td>+0.22%</td></tr><tr><td>Recall</td><td>78.31%</td><td>78.41%</td><td>+0.10%</td></tr><tr><td>F1-Score</td><td>77.77%</td><td>77.99%</td><td>+0.22%</td></tr></table>

## C. Engineering Usability

Beyond performance metrics, we evaluate the engineering usability of PacketLoom by measuring the Source Lines of

Code (SLOC) required to establish a reproducible pipeline. We contrast the original scripts of ET-BERT and YaTC against PacketLoom’s declarative configuration.

1) Code Reduction: As summarized in Table III, PacketLoom significantly reduces the codebase size. For ET-BERT, the original script contains 591 lines of Python code, characterized by hardcoded paths and platform-specific logic. PacketLoom replaces this with a concise 74-line YAML file, achieving an 87.5% reduction in SLOC.

2) Hidden Maintenance Costs: The original scripts incur high hidden costs. For instance, the YaTC script (56 lines) was deceptively simple but lacked essential features like data splitting and error handling. To make it robust and reproducible, we had to add 134 lines of patch code (+239%). In contrast, PacketLoom provides these features out-of-thebox via its DataSplitter and DataCleaner modules, eliminating the need for boilerplate code.

TABLE III  
SLOC COMPARISON: SCRIPTS VS. PACKETLOOM CONFIGURATION

<table><tr><td>Model</td><td>Original Script</td><td>Patched Script $^{\dagger}$ </td><td>PacketLoom</td><td>Reduction</td></tr><tr><td>ET-BERT</td><td>591</td><td>616 (+4.2%)</td><td>74</td><td>87.5%</td></tr><tr><td>YaTC</td><td>56</td><td>190 (+239%)</td><td>35</td><td>37.5%</td></tr></table>

<sup>†</sup>Includes patches for OS compatibility and missing features (e.g., reassemble).

## D. Iteration Efficiency

To quantify PacketLoom’s impact on accelerating experimental iteration, we engaged an alternating execution protocol (Baseline-Ours, Ours-Baseline) across ten rounds to neutralize OS-level disk caching biases. As illustrated in Fig. 3, Packet-Loom demonstrates superior efficiency across both spatial and sequential paradigms.

1) Mitigating I/O Bottlenecks (YaTC): For the spatial paradigm (Fig. 3a), PacketLoom reduces disk reads by 16.3× (27.1 GB → 1.66 GB). Unlike the baseline which parses entire flow files into memory (via rdpcap), PacketLoom’s lazy loader employs early termination, reading only the strictly necessary packets (i.e., first 5) before closing the stream. This translates to a 7.1× speedup (40.6m → 5.7m) and a 3.0× memory reduction (23.0 GB → 7.7 GB), validating the efficacy of the on-demand loading enabled by the transient-resident architecture.

2) The Processing Scope Trade-off (ET-BERT): For the sequential paradigm (Fig. 3b), the baseline exemplifies both friction sources: it first traverses the entire split-file corpus to filter candidates, then samples and serializes the tokenized results into binary files as a training prerequisite. The costly full-corpus traversal dominates initial latency (≈2.8h), while the binary cache, though fast to reload, forces full regeneration upon any pipeline change. PacketLoom adopts a select-first, one-pass strategy: files are pre-sampled and processed lazily through a single pipeline, maintaining tensors in RAM without intermediate disk I/O. This reduces end-to-end latency by 2.1× (2.7h → 1.3h), enabling rapid feedback loops—a critical advantage over the baseline’s rigid processing overhead.

![](images/2583dc98765277a0c9f3ec11c75120d87e77f9c85ac4a284d8dd42b3ecebb9c3.jpg)  
(a) Spatial Paradigm (YaTC)

![](images/790e2d54b5f2aea78955116df47d6a7ba6089701a70dc7065cc56e62103d52a9.jpg)  
(b) Sequential Paradigm (ET-BERT)  
Fig. 3. Normalized Efficiency Comparison. (a) PacketLoom achieves a 16.3× reduction in Disk Read I/O for the YaTC task by employing on-demand lazy loading. (b) For ET-BERT, PacketLoom trades memory for a 2.1× speedup, successfully overcoming the I/O bottleneck.

## E. Discussion

While our evaluation prioritizes computationally intensive sequential and spatial paradigms to validate pipeline robustness, PacketLoom natively supports statistical feature extraction. For topological paradigms, the framework flexibly provisions foundational representations rather than enforcing rigid graph structures. Furthermore, the decoupled architecture readily adapts to broader datasets (e.g., CICIDS-2017 [19]). Unlike generic pipelines (e.g., Spark) lacking network traffic awareness, PacketLoom offers domain-specific operators. Its stateless YAML-driven CLI enables seamless MLOps orchestration (e.g., Airflow). Finally, an open-source release is planned pending necessary intellectual property clearance.

## IV. CONCLUSION

The emerging trend towards foundation models in NTA is bottlenecked by fragmented data engineering. PacketLoom bridges this gap via a decoupled definition-execution architecture, delivering three benefits: (1) multi-modal versatility via a unified operator chain; (2) engineering usability via a configuration-driven orchestrator reducing code by 87.5%; and (3) iteration efficiency via a transient-resident runtime accelerating iteration. PacketLoom thus establishes a scalable foundation for next-generation network intelligence.

## REFERENCES

[1] Google, “Https encryption on the web,” https://transparencyreport. google.com/https/overview?hl=en, 2025, accessed: Jan. 08, 2026.

[2] W. Dong, J. Yu, X. Lin, G. Gou, and G. Xiong, “Deep learning and pretraining technology for encrypted traffic classification: A comprehensive review,” Neurocomputing, vol. 617, p. 128444, 2025.

[3] A. Panchenko, F. Lanze, J. Pennekamp, T. Engel, A. Zinnen, M. Henze, and K. Wehrle, “Website fingerprinting at internet scale.” in NDSS, vol. 1, 2016, p. 23477.

[4] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “Appscanner: Automatic fingerprinting of smartphone apps from encrypted network traffic,” in 2016 IEEE European Symposium on Security and Privacy (EuroS&P), 2016, pp. 439–454.

[5] K. Al-Naami, S. Chandra, A. Mustafa, L. Khan, Z. Lin, K. Hamlen, and B. Thuraisingham, “Adaptive encrypted traffic fingerprinting with bidirectional dependence,” in Proceedings of the 32nd Annual Conference on Computer Security Applications, 2016, pp. 177–188.

[6] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “Fs-net: A flow sequence network for encrypted traffic classification,” in IEEE INFOCOM 2019- IEEE Conference On Computer Communications. IEEE, 2019, pp. 1171–1179.

[7] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in Proceedings of the ACM Web Conference 2022, 2022, pp. 633–642.

[8] H. Y. He, Z. G. Yang, and X. N. Chen, “Pert: Payload encoding representation from transformer for encrypted traffic classification,” in 2020 ITU Kaleidoscope: Industry-Driven Digital Transformation (ITU K). IEEE, 2020, pp. 1–8.

[9] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware traffic classification using convolutional neural network for representation learning,” in 2017 International Conference on Information Networking (ICOIN), 2017, pp. 712–717.

[10] T. Shapira and Y. Shavitt, “Flowpic: Encrypted internet traffic classification is as easy as image recognition,” in IEEE INFOCOM 2019 - IEEE Conference on Computer Communications Workshops (INFOCOM WKSHPS), 2019, pp. 680–687.

[11] R. Zhao, M. Zhan, X. Deng, Y. Wang, Y. Wang, G. Gui, and Z. Xue, “Yet another traffic classifier: A masked autoencoder based traffic transformer with multi-level flow representation,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 37, no. 4, 2023, pp. 5420–5427.

[12] M. Shen, J. Zhang, L. Zhu, K. Xu, and X. Du, “Accurate decentralized application identification via encrypted traffic analysis using graph neural networks,” IEEE Transactions on Information Forensics and Security, vol. 16, pp. 2367–2380, 2021.

[13] E. Caville, W. W. Lo, S. Layeghy, and M. Portmann, “Anomal-e: A selfsupervised network intrusion detection system based on graph neural networks,” Knowledge-Based Systems, vol. 258, p. 110030, 2022.

[14] H. Zhang, L. Yu, X. Xiao, Q. Li, F. Mercaldo, X. Luo, and Q. Liu, “Tfe-gnn: A temporal fusion encoder using graph neural networks for fine-grained encrypted traffic classification,” in Proceedings of the ACM web conference 2023, 2023, pp. 2066–2075.

[15] A. H. Lashkari, G. D. Gil, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of tor traffic using time based features,” in International conference on information systems security and privacy, vol. 2. SciTePress, 2017, pp. 253–262.

[16] Z. Aouini and A. Pekar, “Nfstream: A flexible network data analysis framework,” Computer Networks, vol. 204, p. 108719, 2022.

[17] V. Paxson, “Bro: a system for detecting network intruders in real-time,” Computer Networks, vol. 31, no. 23, pp. 2435–2463, 1999.

[18] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of encrypted and vpn traffic using time-related,” in Proceedings of the 2nd international conference on information systems security and privacy (ICISSP), 2016, pp. 407–414.

[19] I. Sharafaldin, A. H. Lashkari, A. A. Ghorbani et al., “Toward generating a new intrusion detection dataset and intrusion traffic characterization.” ICISSp, vol. 1, no. 2018, pp. 108–116, 2018.
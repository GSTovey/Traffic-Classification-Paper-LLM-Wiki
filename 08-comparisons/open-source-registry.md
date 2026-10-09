---
type: comparison
name: open-source-registry
created: "2026-05-29"
updated: "2026-09-19"
---

# 开源模型/方法注册表

> 本文档汇总知识库中所有论文**已确认开源**的模型和方法，以及**高频被对比但暂未找到开源地址**的重要基线方法。
>
> **维护说明**：每当新论文入库时，应同步更新本表。

---

## 1. 已确认开源的方法/模型

> 论文自身声明并提供了可访问的代码仓库地址。

| # | 方法 | 年份 | 任务 | 代码地址 | 开源内容 | 主要语言 | 对应论文笔记 |
|---|---|---:|---|---|---|---|---|
| 1 | Deep Fingerprinting (DF) | 2018 | 网站指纹攻击 | [GitHub](https://github.com/deep-fingerprinting/df) | 代码 + 数据集 | Keras/TensorFlow | [[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]] |
| 2 | Flowprint | 2020 | 移动应用指纹识别 | [GitHub](https://github.com/Thijsvanede/Flowprint) | 代码 + 数据集 | Python | [[2020-NDSS-Flowprint__Semi-Supervised_Mobile-App_Fingerprinting_on_Encrypted_Network_Traffic]] |
| 3 | Whisper | 2021 | 恶意流量检测 | [GitHub](https://github.com/fuchuanpu/Whisper) | 代码（~3500 LOC） | C/C++ + Python | [[2021-CCS-Realtime_Robust_Malicious_Traffic_Detection_via_Frequency_Domain_Analysis]] |
| 4 | ET-BERT | 2022 | 加密流量分类 | [GitHub](https://github.com/linwhitehat/ET-BERT) | 代码 | Python | [[2022-WWW-ET-BERT__A_Contextualized_Datagram_Representation_with_Pre-training_Transformers_for_Encrypted_Traffic_Classification]] |
| 5 | Separating Flows | 2022 | 隧道流量分离 | [GitLab](https://gitlab.tuwien.ac.at/e389-cnpub/separatingflows/) | 代码 | Python | [[2022-ICMLA-Separating_Flows_in_Encrypted_Tunnel_Traffic]] |
| 6 | YaTC | 2023 | 加密流量分类 | [GitHub](https://github.com/NSSL-SJTU/YaTC) | 代码 | Python | [[2023-AAAI-Yet_Another_Traffic_Classifier_a_Masked_Autoencoder_Based_Traffic_Transformer_With_Multi-level_Flow_Representation]] |
| 7 | LEXNet | 2023 | 流量分类 | [GitHub](https://github.com/XAIseries/LEXNet) | 代码 + 数据集 | Python | [[2023-SIGKDD-A_lightweight__efficient_and_explainable__by__design_convolutional_neural_network_for_internet_traffic_classification]] |
| 8 | Robust Fingerprinting (RF) | 2023 | 网站指纹攻击 | [GitHub](https://github.com/robust-fingerprinting/RF) | 代码 + 防御 + 数据集 | Python | [[2023-USENIX-Subverting_Website_Fingerprinting_Defenses_with_Robust_Traffic_Representation]] |
| 9 | AN-Net | 2024 | 匿名流量分类 | [GitHub](https://github.com/SJTU-dxw/AN-Net) | 代码 + 数据集 | Python | [[2024-WWW-AN-Net__an_Anti-Noise_Network_for_Anonymous_Traffic_Classification]] |
| 10 | Palette | 2024 | 网站指纹防御 | [GitHub](https://github.com/kxdkxd/Palette) | 代码（Tor Pluggable Transport） | Python | [[2024-S&P-Real-Time_Website_Fingerprinting_Defense_via_Traffic_Cluster_Anonymization]] |
| 11 | RobustWF | 2024 | 多标签网站指纹 | [GitHub](https://github.com/chenxiailian/robustweb) | 代码 + 数据集 | Python | [[2024-INFOCOM-Causality_Correlation_and_Context_Learning_Aided_Robust_Lightweight_Multi-Tab_Website_Fingerprinting_Over_Encrypted_Tunnel]] |
| 12 | JA4 Malware Analysis | 2024 | 恶意流量检测 | [GitHub](https://github.com/matousp/malware-analysis) | 代码 + 标注数据集 | Python | [[2024-CNSM-Experience__Report_Using_JA4_Fingerprints_for_Malware_Detection_in_Encrypted_Traffic]] |
| 13 | SoK Decoding | 2025 | 加密流量分类评估 | [GitHub](https://github.com/nime-sha256/chromium-cipher-suite-customizer) | 数据集 + 评估脚本 | Python | [[2025-S&P-SoK_Decoding_the_Enigma_of_Encrypted_Network_Traffic_Classifiers]] |
| 14 | DecETT | 2025 | 加密隧道应用指纹 | [GitHub](https://github.com/DecETT/DecETT) | 代码 | Python | [[2025-WWW-DecETT__Accurate_App_Fingerprinting_Under_Encrypted_Tunnels_via_Dual_Decouple__based_Semantic_Enhancement]] |
| 15 | STAR | 2025 | 零样本网站指纹 | [GitHub](https://github.com/2654400439/STAR-Website-Fingerprinting) | 代码 + STAR-200K 数据集 | Python | [[2025-INFOCOM-STAR__Semantic-Traffic_Alignment_and_Retrieval_for_Zero-Shot_HTTPS_Website_Fingerprinting]] |
| 16 | MET-LLM | 2025 | 恶意加密流量检测 | [GitHub](https://github.com/Superagentsys/MET-LLM) | 代码 | Python | [[2025-ESA-MET-LLM__Enhancing_Large_Language_Models_for_Malicious_Encrypted_Traffic_Detection]] |
| 17 | TFusion | 2025 | 恶意流量检测 | [GitHub](https://github.com/fuchuanpu/TFusion) | 代码 + 附录 | Python | [[2025-CCS-Training_with_Only_1.0 ‰_Samples__Malicious_Traffic_Detection_via_Cross-Modality_Feature_Fusion]] |
| 18 | SweetDanger | 2025 | 加密流量分类评估 | [GitHub](https://github.com/SweetDanger-Polito/SweetDanger) | 代码 + benchmark 数据集 + 方法论 | Python | [[2025-SIGCOMM-The_Sweet_Danger_of_Sugar_Debunking_Representation_Learning_for_Encrypted_Traffic_Classification]] |
| 19 | NetMamba+ | 2026 | 加密流量分类 | [GitHub](https://github.com/UniBuc/NetMamba) | 代码 | Python | [[2026-arXiv-NetMamba+__A_Framework_of_Pre-trained_Models_for_Efficient_and_Accurate_Network_Traffic_Classification]] |
| 20 | FGFR-Net | 2026 | 加密流量分类 | [GitHub](https://github.com/AnaY1115/FGFR_Net) | 代码 | Python | [[2026-JNSM-FGFR-Net_An_Improved_Residual_Network_Encrypted_Traffic_Classification_Model_Based_on_Byte-Level_Traffic_Graphs]] |
| 21 | Criss-cross Transformer (CTT) | 2026 | 加密流量分类/预测 | [GitHub](https://github.com/Amanda-HuaDing/Criss-cross Traffic Transformer) | 代码 | Python | [[2026-TSC-Time_Will_Tell_Criss-cross_Transformer_for_Encrypted_Traffic_Analysis]] |
| 22 | FlowRefiner | 2025 | 流量分类（抗标签噪声） | [GitHub](https://github.com/NSSL-SJTU/FlowRefiner) | 代码 | Python | [[2025-NIPS-FlowRefiner__A_Robust_Traffic_Classification_Framework_against_Label_Noise]] |
| 23 | DAIR-FedMoE | 2025 | 联邦加密流量分类 | [GitHub](https://github.com/dairfedmoe/DairFM) | 代码 | Python | [[2025-TDSC-DAIR-FedMoE__Hierarchical_MoE_for_Federated_Encrypted_Traffic_Classification_under_Compound_Drift]] |
| 24 | Plug-in Enhancement Framework | 2026 | 预训练模型增强 | [GitHub](https://github.com/slg6/Plug-inEnhancementFramework) | 代码 | Python | [[2026-JCN-Plug-in_enhancement_framework__Breaking_through_performance_bottleneck_of_pre-trained_models_for_encrypted_traffic_classification]] |
| 25 | Traffic-Explainer | 2026 | 流量分类可解释性 | [4open.science](https://anonymous.4open.science/r/TrafficExplainer-5E2E/README.md) | 代码 | Python | [[2026-KDD-Building_Transparency_in_Deep_Learning-Powered_Network_Traffic_Classification__A_Traffic-Explainer_Framework]] |
| 26 | TrafficMoE | 2026 | 加密流量分类（MoE） | [GitHub](https://github.com/Posuly/TrafficMoE) | 代码 | Python | [[2026-arXiv-TrafficMoE__Heterogeneity-aware_Mixture_of_Experts_for_Encrypted_Traffic_Classification]] |
| 27 | SUMo | 2024 | Tor 流量关联 | [GitHub](https://github.com/danielaLopes/sumo) | 代码 + 数据集 | Python | [[2024-NDSS-Flow_Correlation_Attacks_on_Tor_Onion_Service_Sessions_with_Sliding_Subset_Sum]] |
| 28 | NetMamba | 2024 | 加密流量分类 | [GitHub](https://github.com/UniBuc/NetMamba) | 代码 | Python | [[2024-ICNP-NetMamba__Efficient_Network_Traffic_Classification_via_Pre-training_Unidirectional_Mamba]]（注：与 NetMamba+ 共用同一仓库） |
| 29 | Multi-ARCL | 2025 | 加密流量分类（持续学习） | [GitHub](https://github.com/sailorlee97/What-changes-you) | 代码 | Python | [[2025-JPDC-Multi-ARCL__Multimodal_adaptive_relay-based_distributed_continual_learning_for_encrypted_traffic_classification]] |
| 30 | ASNet | 2025 | 加密流量分类 | [GitHub](https://github.com/pengwei-iie/ASNET) | 代码 | Python | [[2025-TIFS-Bottom_Aggregating_Top_Separating_An_Aggregator_and_Separator_Network_for_Encrypted_Traffic_Understanding]] |
| 31 | TrafficSliver | 2020 | 网站指纹防御 | [GitHub](https://github.com/TrafficSliver) | 代码 + Tor Pluggable Transport | Python | [[2020-CCS-TrafficSliver__Fighting_Website_Fingerprinting_Attacks_with_Traffic_Splitting]] |
| 32 | FRONT (Zero-delay Defenses) | 2020 | 网站指纹防御 | [GitHub](https://github.com/websitefingerprinting/WebsiteFingerprinting/) | 代码 + 防御实现 | Python | [[2020-USENIX-Zero-delay_Lightweight_Defenses_against_Website_Fingerprinting]] |
| 33 | Surakav | 2022 | 网站指纹防御 | [GitHub](https://github.com/websitefingerprinting/surakav-imp) | 代码 + GAN 训练 + WFDefProxy | Python | [[2022-S&P-Surakav__Generating_Realistic_Traces_for_a_Strong_Website_Fingerprinting_Defense]] |
| 34 | CountMamba | 2025 | 网站指纹攻击 | [GitHub](https://github.com/SJTUdxw/CountMamba-WF) | 代码 | Python | [[2025-S&P-Countmamba__A_Generalized_Website_Fingerprinting_Attack_via_Coarse-Grained_Representation_and_Fine-Grained_Prediction]] |
| 35 | GAPDiS | 2025 | 网站指纹防御 | [GitHub](https://github.com/ByskyXie/GAPDiS) | 代码 | Python | [[2025-CCS-GAPDiS__Gradient-Assisted_Perturbation_Design_via_Sequence_Editing_for_Website_Fingerprinting_Defense]] |
| 36 | CELLSHIFT | 2026 | 网站指纹攻击（数据增强） | [GitHub](https://github.com/robgjansen/cellshift) | 代码 | Python | [[2026-NDSS-CELLSHIFT__RTT-Aware_Trace_Transduction_for_Real-World_Website_Fingerprinting]] |
| 37 | Cease (FRUGAL) | 2026 | 网站指纹防御 | [GitHub](https://github.com/Junowww/FRUGAL-ndss) | 代码 | Python | [[2026-NDSS-Cease_at_the_Ultimate_Goodness__Towards_Efficient_Website_Fingerprinting_Defense_via_Iterative_Mutual_Information_Minimization]] |
| 38 | Lightening (Adaptive Tamaraw) | 2026 | 网站指纹防御 | [GitHub](https://github.com/khashayarkhaj/Adaptive-Tamaraw) | 代码 | Python | [[2026-NDSS-Lightening_the_Load__A_Cluster-Based_Framework_or_A_Lower-Overhead__Provable_Website_Fingerprinting_Defense]] |
| 39 | Holmes | 2024 | 网站指纹攻击（早期阶段） | [GitHub](https://github.com/HolmesWF/Holmes) | 代码 | Python | [[2024-CCS-Robust_and_reliable_early-stage_website_fingerprinting_attacks_via_spatial-temporal_distribution_analysis]] |
| 40 | TMWF | 2023 | 网站指纹攻击（多标签） | [GitHub](https://github.com/jzx-bupt/TMWF) | 代码 | Python | [[2023-CCS-Transformer-based_Model_for_Multi-tab_Website_Fingerprinting_Attack]] |
| 41 | Realistic WF (NetAugment) | 2023 | 网站指纹攻击（数据增强） | [GitHub](https://github.com/SPIN-UMass/Realistic-Website-Fingerprinting-By-Augmenting-Network-Traces) | 代码 | Python | [[2023-CCS-Realistic_Website_Fingerprinting_by_Augmenting_Network_Traces]] |
| 42 | UPGen | 2025 | 审查规避（协议生成） | [GitHub](https://github.com/unblockable/upgen) | 代码 + Proteus + 流量生成器 | Python | [[2025-USENIX-Censorship_Evasion_with_Unidentified_Protocol_Generation]] |
| 43 | Huma | 2026 | 审查规避（Web 隧道） | [Zenodo](https://doi.org/10.5281/zenodo.17790334) | 代码 + 实现 | Python | [[2026-NDSS-Huma__Censorship_Circumvention_via_Web_Protocol_Tunneling_with_Deferred_Traffic_Replacement]] |
| 44 | Censored Planet | 2020 | 审查测量 | [GitHub](https://github.com/censoredplanet) | 代码 + 测量框架 | Python | [[2020-CCS-Censored_Planet__An_Internet-wide__Longitudinal_Censorship_Observatory]] |
| 45 | GFW (USENIX 2023) | 2023 | 审查检测分析 | [GitHub](https://gfw.report/publications/usenixsecurity23/en) | 测量数据 + 分析工具 | Python | [[2023-USENIX-How_the_Great_Firewall_of_China_Detects_and_Blocks_Fully_Encrypted_Traffic]] |
| 46 | LZR | 2021 | 服务发现/隧道检测 | [GitHub](https://github.com/stanford-esrg/lzr) | 代码 | Go | [[2021-USENIX-LZR__Identifying_Unexpected_Internet_Services]] |
| 47 | MH-Net | 2025 | 加密流量分类（多视图异构图） | [GitHub](https://github.com/ViktorAxelsen/MH-Net) | 代码 | Python | [[2025-AAAI-Revolutionizing_Encrypted_Traffic_Classification_with_MH-Net__A_Multi-View_Heterogeneous_Graph_Model]] |
| 48 | FMWF | 2025 | 网站指纹攻击（多标签页少样本） | [GitHub](https://github.com/WW-Meng/FMWF) | 代码 + 数据集 | Python | [[2025-WWW-Beyond_Single_Tabs__A_Transformative_Few-Shot_Approach_to_Multi-Tab_Website_Fingerprinting_Attacks]] |
| 49 | HOLMES & WATSON | 2025 | HTTPS 网站指纹攻击 | [GitHub](https://github.com/2654400439/H123-Website-Fingerprinting) | 代码 + 数据集（1.5TB+） | Python | [[2025-WWW-HOLMES&WATSON__A_Robust_and_Lightweight_HTTPS_Website_Fingerprinting_through_HTTP_Version_Parallelism]] |
| 50 | TabularT-OS | 2026 | 操作系统指纹识别 | [GitHub](https://github.com/rubenpjove/tabularT-OSfingerprinting) | 代码（GNU GPL v3.0） | Python | [[2026-Cybersecurity-Application_of_tabular_transformer_architectures_for_operating_system_fingerprinting]] |
| 51 | FreeUp | 2026 | 加密流量异常检测 | [GitHub](https://github.com/ikun0124/FreeUp) | 代码 | Python | [[2026-INFOCOM-Decompose_to_Understand_Fuse_to_Detect__Frequency-Decoupled_Anomaly_Detection_for_Encrypted_Network_Traffic]] |
| 52 | ConMD | 2026 | 流量异常检测（零正样本） | [GitHub](https://github.com/ikun0124/ConMD) | 代码 | Python | [[2026-TIFS-Contextual_Masking_Distillation_for_Network_Traffic_Anomaly_Detection]] |
| 53 | ResAware | 2026 | 网站指纹攻击（跨环境） | [GitHub](https://github.com/aimafan123/ResAware) | 代码 + 特征化数据集 | Python | [[2026-arXiv-ResAware__Cross-Environment_Website_Fingerprinting_via_Resource-Privileged_Distillation]] |
| 54 | M-En Framework | 2026 | 多环境恶意流量检测 | [GitHub](https://github.com/furqanrustam/M-En-PLS-and-RNN-LSTM-Ubuntu-Simulation)（URL 为推断值，需核实） | 代码 + 数据生成脚本 | Python | [[2026-JCN-A_simulation-based_unified_framework_for_real-time_malicious_traffic_detection_in_multi-environment_networks]] |
| 55 | HTPA 数据集 | 2025 | 混淆 HTTPS 隧道检测 | GitHub（论文 Dataset link，HTTPS Tunneling Predictive Analysis Dataset） | 仅数据集（132 万条流；模型代码未公开） | — | [[2025-JCN-Enhanced_detection_of_obfuscated_HTTPS_tunnel_traffic_using_heterogeneous_information_network]] |
| 56 | Reality Check 数据集 | 2026 | 开放世界 WF 评估 | [OSF](https://osf.io/9m8ea/) | 仅数据集（80 万+ traces） | — | [[2026-arXiv-Reality_Check_for_Tor_Website_Fingerprinting_in_the_Open_World]] |
| 57 | BTRFormer | 2025 | 加密流量分类；恶意流量检测 | [GitHub](https://github.com/yyyjn/BTRFormer) | 部分开源（论文称"Part of code is available"） | PyTorch 1.13.1 + Python 3.9 | [[2025-ICNP-BTRFormer__Hierarchical_Learning_of_Encrypted_Traffic_Using_a_Masked_Autoencoder_with_Block-Based_Traffic_Representation]] |
| 58 | PipHeap | 2025 | 异常检测（网络测量） | [GitHub](https://github.com/PipHeap/PipHeap) | 代码（P4 + C++ 实现） | P4 + C++ | [[2025-IMC-PipHeap__Approximate_Heap_in_the_Pipeline_Empowering_Network_Measurement]] |
| 59 | LotBoNC | 2026 | 恶意流量检测；僵尸网络分类 | [GitHub](https://github.com/watsonhuhpi/LotBoNC) | 代码 | — | [[2026-AsiaCCS-LotBoNC__Novel_Botnet_Traffic_Classification_under_Long-tailed_Distributions]] |
| 60 | PSM | 2026 | — | GitHub（解析稿 URL 含空格，需核实：`https://github.com/zxzx2002/Sketch Migration.git`） | 代码 | — | [[2026-IWQoS-PSM__Timely_and_Resource-Efficient_Sketch_Migration_in_Network_Measurement]] |
| 61 | Mercuriuzz (QUIC 逻辑漏洞挖掘) | 2026 | — | [Zenodo](https://doi.org/10.5281/zenodo.17015304) | artifact 归档（主程序在 GitHub 仓库 Mercuriuzz，解析稿未保留完整 URL） | — | [[2026-NDSS-Identifying_Logical_Vulnerabilities_in_QUIC_Implementations]] |
| 62 | Looma | 2026 | — | [GitHub](https://github.com/uoenoplab/looma) | 实现与基准工具 | — | [[2026-NDSS-Looma__A_Low-Latency_PQTLS_Authentication_Architecture_for_Cloud_Applications]] |
| 63 | TIPSO-GAN | 2026 | 恶意流量检测；异常检测 | [Zenodo](https://doi.org/10.5281/zenodo.17759516) | artifact / 代码归档（未给出 GitHub 仓库） | Python 3.10 + TensorFlow 2.15.0 | [[2026-NDSS-TIPSO-GAN__Malicious_Network_Traffic_Detection_Using_a_Novel_Optimized_Generative_Adversarial_Network]] |
| 64 | CascadeNet | 2026 | 流量表征生成；异常检测 | [GitHub](https://github.com/lurw2000/CascadeNet) | 代码（4000+ 行） | PyTorch 2.1.0 | [[2026-NSDI-CascadeNet__Generating_Network_Traffic_with_High-Fidelity_Temporal_Patterns]] |
| 65 | Iris | 2026 | 隧道检测；加密流量检测 | [GitHub](https://github.com/stanford-esrg/iris) | 代码（Apache 2.0） | Rust | [[2026-NSDI-Iris__Expressive_Traffic_Analysis_for_the_Modern_Internet]] |
| 66 | GTT23 | 2026 | 网站指纹攻击 | [Zenodo](https://doi.org/10.5281/zenodo.10620520) | 仅数据集（真实 Tor 踪迹；受控发布，需申请） | — | [[2026-PAM-A_Measurement_of_Genuine_Tor_Traces_for_Realistic_Website_Fingerprinting]] |
| 67 | DNS Privacy Dataset (DoQ vs DoH/3) | 2026 | — | [Zenodo](https://doi.org/10.5281/zenodo.17860118) | 仅数据集（resolver 特征/时延记录 + 网页加载指标） | — | [[2026-PAM-The_Future_of_DNS_Privacy__A_Comparison_of_DNS_over_QUIC_and_DNS_over_HTTP3]] |
| 68 | C3F (GPU Covert Channel) | 2026 | — | [GitHub](https://github.com/HugoLeoLJH/C3F) | 代码 + 在线 demo | JavaScript + Python | [[2026-S&P-Practical_Covert_Channel_Across_Isolated_Browser_Instances_via_GPU_Command_Queue_Contention]] |
| 69 | AirMask | 2026 | — | [GitHub](https://github.com/smith0818/AirMask) | 代码 + 数据集 | — | [[2026-TDSC-AirMask__Enabling_Air-to-Air_Masking_of_Wireless_Traffic_Fingerprints_in_WiFi-Based_IoT_Environments]] |
| 70 | Stinger | 2026 | 网站指纹防御 | [GitHub](https://github.com/sxy888/Stinger-prototype) | 代码（原型系统）+ 实验细节 | — | [[2026-TIFS-Stinger__A_Light-Weight_Website_Fingerprinting_Defense_Through_Poisoning_Packet_Sequences]] |
| 71 | UTFormer | 2026 | 加密流量分类 | [GitHub](https://github.com/utformer/UTFormer) | 代码 | PyTorch 1.13.1 | [[2026-TIFS-UTFormer__An_Ultra-Lightweight_Transformer_for_Traffic_Classification]] |
| 72 | ISP Forecasting Benchmark | 2026 | 异常检测（ISP 流量预测） | [GitHub](https://github.com/koumajos/isp-forecasting-benchmark) | 代码 + 实验配置 | — | [[2026-TNSM-Comparative_Analysis_of_Deep_Learning_Models_for_Real-World_ISP_Network_Traffic_Forecasting]] |
| 73 | ProtectIT | 2026 | 加密流量分类；应用指纹 | [GitHub](https://github.com/SEAlab-unige/ProtectIT) | 代码 | Keras/TensorFlow | [[2026-TNSM-Hardware-Aware_Neural_Architecture_Search_for_Encrypted_Traffic_Classification_on_Resource-Constrained_Devices]] |
| 74 | HyTMTC | 2026 | 多场景流量分类 | [GitHub](https://github.com/PolinaH/HyTMTC) | 代码（论文称发表后开源） | — | [[2026-TNSM-HyTMTC__A_Pre-Training_Method_for_Multi-Scenario_Network_Traffic_Classification_With_Hybrid_Transformer-Mamba]] |
| 75 | RISK-4-Auto | 2026 | 车载网络流量分类；恶意流量检测 | [GitHub](https://github.com/Anurag-Dutta/RISK-4-Auto) | 代码 + 部分 2D 直方图数据 | — | [[2026-TNSM-RISK-4-Auto__Residually_Interconnected_and_Superimposed_Kolmogorov-Arnold_Networks_for_Automotive_Network_Traffic_Classification]] |
| 76 | WebRTC DTLS-SRTP Artifact (DMS) | 2026 | — | [Zenodo](https://doi.org/10.5281/zenodo.17880120) | artifact（DMS 框架、pcaps、报告、Chromium 补丁、漏洞录像） | — | [[2026-USENIX-Analyzing_the_WebRTC_Ecosystem_and_Breaking_Authentication_in_DTLS-SRTP]] |
| 77 | QUIC-Attacker | 2026 | — | [GitHub](https://github.com/tls-attacker/TLS-Attacker)；[GitHub](https://github.com/tls-attacker/QUIC-Docker-Library) | 代码（QUIC-Attacker 为 TLS-Attacker 套件一部分）+ 15 个 QUIC 实现的 Docker 镜像 | — | [[2026-USENIX-Breaking_the_Boundaries__Analyzing_QUIC_Frame-Packet_Interactions_With_QUIC-Attacker]] |
| 78 | Hop | 2026 | — | [Zenodo](https://doi.org/10.5281/zenodo.17953397) | 源码 + Mininet 脚本 + 测量与绘图脚本 + 文档 | — | [[2026-USENIX-Hop__A_Modern_Transport_and_Remote_Access_Protocol]] |
| 79 | Motion in the Clear (PACMO) | 2026 | 流量分类（VR 行为重建） | [Zenodo](https://doi.org/10.5281/zenodo.20343460) | PACMO Python 实现 + VCR profiling 脚本（原始抓包与运动数据不公开） | Python | [[2026-USENIX-Motion_in_the_Clear__Reconstructing_VR_User_Behavior_from_Network_Traffic]] |
| 80 | Opossum Attack | 2026 | — | [Zenodo](https://doi.org/10.5281/zenodo.17855525) | artifact 归档 | — | [[2026-USENIX-Opossum_Attack__Application_Layer_Desynchronization_using_Opportunistic_TLS]] |
| 81 | Remise | 2026 | — | [Zenodo](https://zenodo.org/records/20438384) | artifact 归档 | — | [[2026-USENIX-Remise__Authorized_Anonymous_Communication_Systems]] |
| 82 | Revelio | 2026 | 应用指纹（VoIP 封锁测量） | [Zenodo](https://doi.org/10.5281/zenodo.20362017) | 代码 / 测量数据 | — | [[2026-USENIX-Revelio__A_Global_Study_of_VoIP_Blocking]] |
| 83 | Tracegram | 2026 | Trace 级流量分析；恶意流量检测 | [GitHub](https://github.com/YuchenZhang-Academic/Tracegram) | 代码（实现与合成示例另见 Zenodo 10.5281/zenodo.17978903；原始数据集受许可限制不重分发） | — | [[2026-USENIX-Tracegram__Framing_Trace-Level_Traffic_Analysis_with_Temporally-Aware_Multiple_Instance_Learning]] |
| 84 | AVP-Inspect | 2026 | — | [GitHub](https://github.com/SECSAT-LAB-GMU/AVP-Inspect) | 代码 | — | [[2026-arXiv-AVP-Inspect__Coordinated_Cyber-Physical_Testing_for_Privacy_Analysis_of_COTS_Apple_Vision_Pro_Applications]] |
| 85 | Synthetic Traffic Generator | 2026 | 加密流量分类；异常检测 | [GitHub](https://github.com/harshilpatel22/Synthetic-Traffic-Generator) | 代码 + 合成数据集 | — | [[2026-arXiv-Generative_AI_for_Encrypted_Traffic_Analysis__Synthetic_Dataset_Generation_and_Classifier_Evaluation]] |
| 86 | PA3 | 2026 | 网站指纹攻击（代理漂移） | [GitHub](https://github.com/wesly2000/PA3) | 源码 + 全部数据集（约 1 TB） | — | [[2026-arXiv-Mitigating_Proxy-Induced_Traffic_Drift_in_Website_Fingerprinting_via_Model-Agnostic_Traffic_Tailoring]] |
| 87 | PERO | 2026 | 加密流量分类；恶意流量检测 | [4open.science](https://anonymous.4open.science/r/PERO-D0A7) | 代码（匿名仓库，称录用后发布完整实现） | PyTorch | [[2026-arXiv-PERO__Efficient_Robust_Post-Training_Foundation_Models_for_Encrypted_Traffic_Classification]] |
| 88 | Pruned Traffic Trees | 2026 | 加密流量分类 | [4open.science](https://anonymous.4open.science/r/pruned_traffic_trees-D08C) | 代码（匿名仓库） | — | [[2026-arXiv-Pruned_Traffic_Trees__Native_Semantic_Compression_with_a_Protocol-Structured_Model_Family_for_Encrypted_Traffic_Classification]] |
| 89 | SoK Flow Labels | 2026 | 流量分类；网站指纹；基准审计 | [4open.science](https://anonymous.4open.science/r/traffic_dataset_audit_script-440B/) | 审计脚本 + 配对语料 | — | [[2026-arXiv-SoK__Where_Do_Flow_Labels_Come_From__Auditing_Label_Provenance_in_Encrypted_Traffic_Benchmarks]] |
| 90 | Colossus (PQ-WF-Eval) | 2026 | 网站指纹攻击；加密流量分类 | [4open.science](http://anonymous.4open.science/r/PQ-WF-Eval) | 代码（匿名仓库） | — | [[2026-arXiv-The_Colossus_with_Feet_of_Clay__Debunking_Encrypted_Traffic_Classifiers_under_PQC_Evolution]] |
| 91 | BBQ (HTTP/2 WF) | 2026 | 网站指纹攻击/防御评测 | [GitHub](https://github.com/bcebere/Understanding-the-Privacy-Preserving-Potential-of-HTTP2-Against-Webpage-Fingerprinting) | 代码（含 wfaudit 工具、采集/重放管线、基准代码） | — | [[2026-arXiv-Understanding_the_Privacy-Preserving_Potential_of_HTTP_2_Against_Webpage_Fingerprinting]] |

---

## 2. 计划开源 / 待确认

> 论文声明将开源但截至当前尚未确认具体地址。

| 方法 | 年份 | 状态 | 说明 | 对应论文笔记 |
|---|---:|---|---|---|
| Swallow | 2025 | 待确认 | 论文声明将发布数据集和源代码，但代码地址为 `github.com/anonymous`，具体地址待确认 | [[2025-CCS-Swallow__A_Transfer-Robust_Website_Fingerprinting_Attack_via_Consistent_Feature_Learning]] |
| Gated Attention for LLM | 2025 | 计划中 | 作者计划基于 Megatron-LM 开源代码，采用 MIT License | [[2025-NIPS-Gated_Attention_for_Larg]] |
| ByteDance | 2026 | 计划中 | 论文提到计划正式发表后在 GitHub 上共享代码和数据 | [[2026-JCN-ByteDance__Let_bytes_perform_brilliantly_in_multi-view_encrypted_traffic_classification]] |
| TrustWI | 2026 | 待确认 | 论文声称开源（"we make the source code of TrustWI publicly available"），但正文未出现仓库 URL | [[2026-TDSC-Shattering_Weak_Facades__Trustworthy_Detection_of_Encrypted_Malicious_Traffic_via_Uncertainty-Aware_Fusion]] |
| DawnGuard | 2026 | 待确认 | 论文声称开源（"We release the dataset and source code of DawnGuard"），但正文未出现仓库 URL | [[2026-TIFS-Early-Stage_Detection_of_Encrypted_Malware_Traffic_via_Multi-Flow_Temporal_Graph_Learning]] |
| FlowSem-MAE | 2026 | 待确认 | 论文声明将在补充材料中提供代码和模型参数，尚未确认具体链接 | [[2026-arXiv-Where_Do_Flow_Semantics_Reside__A_Protocol-Native_Tabular_Pretraining_Paradigm_for_Encrypted_Traffic_Classification]] |
| mmTraffic (Traffic-Reasoning) | 2026 | 待确认 | 论文声称开源（项目名 Traffic-Reasoning-Project），未给出具体仓库 URL | [[2026-arXiv-Multimodal_Reasoning_with_LLM_for_Encrypted_Traffic_Interpretation__A_Benchmark]] |
| Q3Fuzz | 2026 | 待确认 | 论文摘要称 Q3Fuzz 已公开（脚注 1），但解析稿未保留该 URL | [[2026-DSN-Q3Fuzz__Multi-Layered_Stateful_Fuzzing_for_the_QUIC-HTTP_3_Protocol_Stack]] |
| MVPNalyzer | 2026 | 待确认 | 论文承诺开源；项目页 https://censoredplanet.org/#/research/securing-pets，解析稿未给出代码仓库 URL | [[2026-NDSS-MVPNalyzer__An_Investigative_Framework_for_Auditing_the_Security_&_Privacy_of_Mobile_VPNs]] |

---

## 3. 高频对比基线但暂未找到开源地址

> 以下方法被 **3 篇及以上论文**作为 baseline 进行对比，但在知识库中**未找到其开源代码地址**。
> 这些方法对复现和公平对比至关重要，建议后续追踪其代码状态。

### 3.1 加密流量分类领域

| # | 方法 | 任务 | 被对比次数 | 对比它的论文（部分列举） | 说明 |
|---|---|---|---:|---|---|
| 1 | AppScanner | 应用指纹识别 | 10+ | ET-BERT, Flowprint, DecETT, CTT, AN-Net, CoMask, MM4flow, FGFR-Net, MET-LLM, FG-SAT | 经典统计特征方法，几乎所有应用分类论文的 baseline |
| 2 | TSCRNN | 加密流量分类 | 7+ | ET-BERT, TrafficAudio, ByteDance, MT-DEGCL, CTT, MET-LLM, NetMamba+ | RNN-based 分类方法 |
| 3 | BIND | 加密流量分类 | 4+ | ET-BERT, Flowprint, FGFR-Net, MET-LLM, MM4flow | 二分图网络流量表示 |
| 4 | DeepPacket | 加密流量分类 | 3+ | ET-BERT, TrafficAudio, FEC-OSL, CTT | 端到端 CNN 分类 |
| 5 | PERT | 加密流量分类 | 3+ | YaTC, NetMamba+, FEC-OSL, Talk Like a Packet | Transformer 预训练方法 |
| 6 | FlowLens | 应用指纹识别 | 4+ | AN-Net, MOTA, MM4flow, TFusion, DecETT | 流量级应用识别 |
| 7 | LAMBERT | 加密流量分类 | 2+ | NetTTT, NetMamba+ | BiGRU+BERT 架构（需更多确认） |

### 3.2 网站指纹 (WF) 领域

| # | 方法 | 任务 | 被对比次数 | 对比它的论文（部分列举） | 说明 |
|---|---|---|---:|---|---|
| 1 | CUMUL | 网站指纹攻击 | 5+ | DF, ET-BERT, Palette, RobustWF, STAR | 经典统计特征 WF 攻击 |
| 2 | k-Fingerprinting (k-FP) | 网站指纹攻击 | 4+ | DF, ET-BERT, Palette, CoMask | 随机森林 + k-NN 经典方法 |
| 3 | AWF | 网站指纹攻击 | 3+ | DF, Palette, Subverting WF, NetTTT | CNN-based 自动化 WF 攻击 |
| 4 | Var-CNN | 网站指纹攻击 | 3+ | Swallow, Palette, Subverting WF | 多尺度 CNN WF 攻击 |
| 5 | Tik-Tok | 网站指纹攻击 | 3+ | Swallow, Palette, Subverting WF | 利用方向和时间的 WF 攻击 |
| 6 | CountMamba | 网站指纹攻击 | 2 | STAR, Swallow | Mamba-based WF 攻击（较新） |
| 7 | NetCLR | 网站指纹攻击 | 2 | STAR, Swallow | 对比学习 WF 攻击（较新） |

### 3.3 开放集/少样本领域

| # | 方法 | 任务 | 被对比次数 | 对比它的论文 | 说明 |
|---|---|---|---:|---|---|
| 1 | CapsNet (流量领域) | 流量分类 | 3+ | FG-SAT, NetMamba+, MM4flow, CoMask | Capsule Network 在流量中的应用 |
| 2 | AttnLSTM | 流量分类 | 3 | AN-Net, MOTA, MT-DEGCL | 注意力 + LSTM 架构 |
| 3 | CVAE-EVT | 开放集分类 | 1+ | FEC-OSL | 条件 VAE + 极值理论（需更多确认） |
| 4 | Trident | 开放集分类 | 1+ | FEC-OSL | AE/RNN/GNN 三种变体（需更多确认） |

### 3.4 CLET 论文确认有公开实现但知识库中无具体地址

> 以下方法在 CLET 论文 (2026-JKing) 中被明确标注为有公开实现，但知识库中未记录具体 GitHub 地址。建议后续补充。

| 方法 | 说明 |
|---|---|
| FlowPic | 将流量转为图像表示进行分类，被 5+ 篇论文对比 |
| CENTIME | 短期特征编码方法 |
| TFE-GNN | 流量特征增强 GNN，被 5+ 篇论文对比 |
| PEAN | 原型增强注意力网络 |
| SessionVideo | 会话级视频化流量表示 |

> 注：MH-Net 已从本清单移除——已确认开源（https://github.com/ViktorAxelsen/MH-Net），见第 1 节 #47。

---

## 4. 第三方参考工具

> 以下工具在论文中被引用为已有参考实现，非本知识库论文的贡献，但在复现和对比中有参考价值。

### 4.1 流量分析工具

| 工具 | 来源 | 地址 | 用途 |
|---|---|---|---|
| JA3 | Salesforce | [GitHub](https://github.com/salesforce/ja3) | TLS 客户端指纹 |
| JOY | Cisco | [GitHub](https://github.com/cisco/joy/) | 网络流量特征提取与分析 |
| Mercury | Cisco | [GitHub](https://github.com/cisco/mercury) | 加密流量元数据分析 |
| Kitsune | Ben-Gurion Univ. | [GitHub](https://github.com/ymirsky/Kitsune-py) | 轻量级在线恶意流量检测（PyTorch） |

### 4.2 混淆代理/翻墙协议工具

| 工具 | 地址 | 用途 |
|---|---|---|
| Cloak | [GitHub](https://github.com/cbeuw/Cloak) | TLS 插件混淆代理 |
| naiveproxy | [GitHub](https://github.com/klzgrad/naiveproxy) | Chromium 网络栈代理 |
| shadow-tls | [GitHub](https://github.com/ihciah/shadow-tls) | TLS 混淆代理 |
| obfs4 | [GitLab](https://gitlab.com/yawning/obfs4) | Tor 混淆传输协议 |
| simple-obfs | [GitHub](https://github.com/shadowsocks/simple-obfs) | Shadowsocks 简单混淆 |
| Xray-core | [GitHub](https://github.com/XTLS/Xray-core/) | V2Ray 衍生代理内核 |
| v2ray | [GitHub](https://github.com/v2ray/v2raycore) | 网络代理工具 |

### 4.3 基础设施与框架

| 工具 | 来源 | 地址 | 用途 |
|---|---|---|---|
| TrafficLLM | ZGC-LLM-Safety | [GitHub](https://github.com/ZGC-LLM-Safety/TrafficLLM/) | 流量分析大语言模型 |
| Megatron-LM | NVIDIA | [GitHub](https://github.com/NVIDIA/Megatron-LM) | 大规模预训练框架 |
| Website-Fingerprinting-Library | 社区 | [GitHub](https://github.com/Xinhao-Deng/Website-Fingerprinting-Library) | WF 攻击方法集合 |
| net4people/bbs | 社区 | [GitHub](https://github.com/net4people/bbs) | 反审查技术讨论社区 |
| py-virtnet | CN-TU | [GitHub](https://github.com/CN-TU/py-virtnet) | 虚拟网络流量生成 |

---

## 5. 统计摘要

| 类别 | 数量 |
|---|---:|
| 已确认开源（本知识库论文） | 91（含 4 项仅数据集开源） |
| 计划开源 / 待确认 | 9 |
| 高频对比基线无开源地址 | 20+ |
| CLET 论文确认有实现但缺地址 | 5 |
| 第三方参考工具 | 16 |

### 按任务领域分布（已开源）

> 按主要任务域归类（每项记 1 次），合计 91；2026-09-19 批次重新核算。

| 领域 | 已开源数量 | 代表方法 |
|---|---:|---|
| 加密流量分类 | 19 | ET-BERT, YaTC, NetMamba+, TrafficMoE, MH-Net, BTRFormer, UTFormer, PERO, Pruned Traffic Trees |
| 网站指纹（攻击+防御） | 23 | DF, RF, Palette, STAR, CountMamba, CELLSHIFT, Cease, FMWF, Stinger, PA3, BBQ |
| 恶意流量检测/异常检测 | 10 | Whisper, TFusion, MET-LLM, FreeUp, ConMD, LotBoNC, TIPSO-GAN, Tracegram |
| 应用/匿名流量分类 | 4 | Flowprint, AN-Net, DecETT, Motion in the Clear |
| 审查规避/测量 | 5 | UPGen, Huma, Censored Planet, GFW, Revelio |
| 流量关联/匿名攻击 | 1 | SUMo |
| 评估/基准 | 3 | SoK Decoding, SweetDanger, SoK Flow Labels |
| 服务发现/隧道检测 | 3 | Separating Flows, LZR, Iris |
| 可解释性 | 1 | Traffic-Explainer |
| 预训练模型增强 | 1 | Plug-in Enhancement Framework |
| 操作系统指纹识别 | 1 | TabularT-OS |
| 仅数据集开源 | 4 | HTPA, Reality Check, GTT23, DNS Privacy Dataset |
| 网络测量 | 3 | PipHeap, PSM, ISP Forecasting Benchmark |
| 协议安全/设计 | 7 | Mercuriuzz, Looma, WebRTC DTLS-SRTP, QUIC-Attacker, Hop, Opossum, Remise |
| 流量生成/合成 | 2 | CascadeNet, Synthetic Traffic Generator |
| 隐蔽信道 | 1 | C3F |
| 隐私审计 | 1 | AVP-Inspect |
| IoT/车载流量 | 2 | AirMask, RISK-4-Auto |

---

## 6. 维护检查清单

新论文入库时，请逐项检查：

- [ ] 论文 frontmatter 中 `code` 字段是否填写了仓库地址？
- [ ] 论文 Section 7.1 是否提及开源信息？
- [ ] 论文是否将其他方法作为 baseline？如果是，检查该 baseline 是否在本表中记录。
- [ ] 如果论文提出了新方法且已开源，添加到第 1 节。
- [ ] 如果论文声明将开源，添加到第 2 节。
- [ ] 如果 baseline 方法被 3+ 篇论文使用且无开源地址，添加到第 3 节。
- [ ] 如果 baseline 方法有公开实现但地址未记录，添加到第 3.4 节并标记为待补充。

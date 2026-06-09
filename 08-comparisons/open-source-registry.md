---
type: comparison
name: open-source-registry
created: "2026-05-29"
updated: "2026-06-01"
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
| 15 | STAR | 2025 | 零样本网站指纹 | [GitHub](https://github.com/2654400439/STAR-Website-Fingerprinting) | 代码 + STAR-200K 数据集 | Python | [[2025-arXiv-STAR__Semantic-Traffic_Alignment_and_Retrieval_for_Zero-Shot_HTTPS_Website_Fingerprinting]] |
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
| 28 | NetMamba | 2024 | 加密流量分类 | [GitHub](https://github.com/UniBuc/NetMamba) | 代码 | Python | [[2024-arXiv-NetMamba__Efficient_Network_Traffic_Classification_via_Pre-training_Unidirectional_Mamba]]（注：与 NetMamba+ 共用同一仓库） |
| 29 | Multi-ARCL | 2025 | 加密流量分类（持续学习） | [GitHub](https://github.com/sailorlee97/What-changes-you) | 代码 | Python | [[2025-JPDC-Multi-ARCL__Multimodal_adaptive_relay-based_distributed_continual_learning_for_encrypted_traffic_classification]] |
| 30 | ASNet | 2025 | 加密流量分类 | [GitHub](https://github.com/pengwei-iie/ASNET) | 代码 | Python | [[2025-TIFS-Bottom_Aggregating_Top_Separating_An_Aggregator_and_Separator_Network_for_Encrypted_Traffic_Understanding]] |

---

## 2. 计划开源 / 待确认

> 论文声明将开源但截至当前尚未确认具体地址。

| 方法 | 年份 | 状态 | 说明 | 对应论文笔记 |
|---|---:|---|---|---|
| Swallow | 2025 | 待确认 | 论文声明将发布数据集和源代码，但代码地址为 `github.com/anonymous`，具体地址待确认 | [[2025-CCS-Swallow__A_Transfer-Robust_Website_Fingerprinting_Attack_via_Consistent_Feature_Learning]] |
| Gated Attention for LLM | 2025 | 计划中 | 作者计划基于 Megatron-LM 开源代码，采用 MIT License | [[2025-NIPS-Gated_Attention_for_Larg]] |
| ByteDance | 2026 | 计划中 | 论文提到计划正式发表后在 GitHub 上共享代码和数据 | [[2026-JCN-ByteDance__Let_bytes_perform_brilliantly_in_multi-view_encrypted_traffic_classification]] |

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
| MH-Net | 多头注意力网络 |
| SessionVideo | 会话级视频化流量表示 |

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
| 已确认开源（本知识库论文） | 30 |
| 计划开源 / 待确认 | 3 |
| 高频对比基线无开源地址 | 20+ |
| CLET 论文确认有实现但缺地址 | 6 |
| 第三方参考工具 | 16 |

### 按任务领域分布（已开源）

| 领域 | 已开源数量 | 代表方法 |
|---|---:|---|
| 加密流量分类 | 12 | ET-BERT, YaTC, LEXNet, CTT, NetMamba+, FGFR-Net, SweetDanger, TFusion, NetMamba, Multi-ARCL, ASNet, TrafficMoE |
| 网站指纹（攻击+防御） | 6 | DF, RF, Palette, RobustWF, STAR, Swallow（待确认） |
| 恶意流量检测 | 4 | Whisper, TFusion, MET-LLM, JA4 |
| 应用/匿名流量分类 | 3 | Flowprint, AN-Net, DecETT |
| 流量关联/匿名攻击 | 1 | SUMo |
| 评估/基准 | 2 | SoK Decoding, SweetDanger |
| 可解释性 | 1 | Traffic-Explainer |
| 预训练模型增强 | 1 | Plug-in Enhancement Framework |

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

---
type: evidence-migration-map
frozen_on: "2026-11-18"
frozen_counts: {"claims": 185, "relations": 26, "fronts": 7, "ledger": 61}
legacy_ledger_sha256: 9479e624db633270c2fb527c52d96ddff60f0c5a2d770574bd376fa5221f0009
archive_sha256: {"09-claims/claims-index.md": "790d567b14663ae1803476bcc5b3612e987d731686f624d925e8508e8209845b", "09-claims/contradictions.md": "b1e4d89439c484ea1dd75fa0e42a13fea280a1624673ceb17710f54b10461440", "12-research-fronts/multimodal-fusion-strategy.md": "cda492add9649252306fdc605c8c30bc6b5cff53783485bd76b6f88a16c811be", "12-research-fronts/payload-learnability.md": "f63ac5b9ac86268b84ace94a629e7d1f6de50dfd7dab97657ec2dc77248d8476", "12-research-fronts/pretraining-necessity.md": "ae1c06d8bb60155909926da7d8fddf368167ab59b206859f168638532f700233", "12-research-fronts/representation-vs-shallow.md": "ecde2031f2eaeff1e8c2ffee3bd8b5a89a1e6a7adddd04082f633b5049cfbb61", "12-research-fronts/tokenization-optimal.md": "7633f3cc0cdb78a47566cda0cb06d7189e9150a0d9a74b7a04c35e4cacd09b26", "12-research-fronts/tor-over-proxy-low-fpr-detection.md": "fbcf3d2f6faccc98e9de7e9b515fc487ab30787ef45ef8413192b4a99a6ce290", "12-research-fronts/wf-attack-defense-limit.md": "4011278e5e1a00405b183b73721c93badca983b42b3a42c520d96b8902625f26"}
---

# 证据迁移清单

冻结范围为七条前沿、61 条旧证据、185 项历史 Claims 或来源入口、26 项历史关系。旧表行与文献入口以节内序号定位。历史全文及原 ID 保留在来源页面。

新旧 ID 的对应关系表示复核归属。候选证据仍需要逐项签审。处置区分原文已初查、条件差异或资料待核以及范围外保留。相同原文的多个历史条目可映射到同一命题。

## 旧证据账本

| 旧证据 ID | 旧命题 ID | 历史状态 | 来源 | 新命题 ID | 直接派生候选 | 处置依据 |
| --- | --- | --- | --- | --- | --- | --- |
| EV-NEST-01 | NEST-01 | verified | [[03-paper-notes/2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions]] | CLM-0601 | EV-V2-NEST-FACTORIZE | 已定位原文，待签审。定位匹配 RF、输入和树预算的结构消融。 |
| EV-NEST-02 | NEST-02 | verified | [[03-paper-notes/2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions]] | CLM-0602、CLM-0606 | EV-V2-NEST-CONFIRM、EV-V2-NEST-LATER-RESEGMENT | 已定位原文，待签审。拆开确认结果与后来采集、重分段。 |
| EV-NEST-03 | NEST-03 | verified | [[03-paper-notes/2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions]] | CLM-0603 | EV-V2-NEST-CALIBRATION | 已定位原文，待签审。按代理分别保留，包含 Trojan 的反向结果。 |
| EV-NEST-04 | NEST-04 | verified | [[03-paper-notes/2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions]] | CLM-0604、CLM-0605 | EV-V2-NEST-FROZEN-FPR、EV-V2-NEST-SWEPT-FPR | 已定位原文，待签审。拆开冻结 AND、扫阈值及各自分母。 |
| EV-20261026-01 | C-20261026-01 | pending_review | [[03-paper-notes/2026-INFOCOM-ARI-LLM__Autoregressive_Imputation_for_Network_Traffic_Matrix_via_Large_Language_Models]] | — | — | 本轮范围外，保留历史。流量矩阵重构，与七条分类前沿的决策任务不同。 |
| EV-20261026-02 | C-20261026-02 | pending_review | [[03-paper-notes/2026-INFOCOM-Automated_Construction_of_High-Quality_Initial_Seed_Corpus_for_Network_Protocol_Fuzzing]] | — | — | 本轮范围外，保留历史。协议测试语料构造。 |
| EV-20261026-03 | C-20261026-03 | pending_review | [[03-paper-notes/2026-INFOCOM-HF-Transformer__A_Non-Pretrained_Encrypted_Network_Traffic_Classification_Model_Based_on_Packet_Header_Fields]] | CLM-0202 | EV-V2-HF-SUPERVISED | 已定位原文，待签审。由原摘要定位到六基准原表，限定可见包头和监督设置。 |
| EV-20261026-04 | C-20261026-04 | pending_review | [[03-paper-notes/2026-INFOCOM-MonPlan__Taming_Network_Measurement_with_Accurate_and_Resource-Efficient_Sketch-INT_Co-Design]] | — | — | 本轮范围外，保留历史。网内流测量与状态调度。 |
| EV-20261026-05 | C-20261026-05 | pending_review | [[03-paper-notes/2026-INFOCOM-PP-OpenNet__Privacy-Preserved_Open_Set_Classification_for_Network_Traffic]] | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| EV-20261026-06 | C-20261026-06 | pending_review | [[03-paper-notes/2026-INFOCOM-PacketLoom__A_Unified_Preprocessing_Framework_for_Multi-Modal_Network_Traffic_Analysis]] | CLM-0503 | EV-V2-PACKETLOOM-PREPROCESSING | 已定位原文，待签审。已链接实现与复现表，不能据此排列 Tokenization。 |
| EV-20261026-07 | C-20261026-07 | pending_review | [[03-paper-notes/2026-INFOCOM-Practical_VPN_Fingerprinting_using_Coarse_Inference_of_Field_Specifications_in_Data_Channels]] | CLM-0609 | — | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| EV-20261026-08 | C-20261026-08 | pending_review | [[03-paper-notes/2026-INFOCOM-Synecdoche__Efficient_and_Accurate_In-Network_Traffic_Classification_via_Direct_Packet_Sequential_Pattern_Matching]] | — | — | 本轮范围外，保留历史。在线数据面匹配和部署速度。 |
| EV-20261026-09 | C-20261026-09 | pending_review | [[03-paper-notes/2026-INFOCOM-Tap_Dance_on_Android_External_Storage__Covert_Channels_Built_on_File_Operations]] | — | — | 本轮范围外，保留历史。Android 文件侧信道。 |
| EV-20261026-10 | C-20261026-10 | pending_review | [[03-paper-notes/2026-TDSC-A_Unified_Oversampling-Based_Imbalance_Processing_Framework_for_Network_Traffic_Anomaly_Detection]] | — | — | 本轮范围外，保留历史。异常检测训练样本不平衡。 |
| EV-20261026-11 | C-20261026-11 | pending_review | [[03-paper-notes/2026-TDSC-Behavioral_Evidence-Based_Hierarchical_Decision_Refinement_for_Encrypted_Malicious_Traffic_Classification_in_Decentralized_Data_Circulation]] | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| EV-20261026-12 | C-20261026-12 | pending_review | [[03-paper-notes/2026-TDSC-Drift-Aware_Adaptive_Website_Fingerprinting]] | CLM-0304 | EV-V2-WF-DRIFT-AION | 已定位原文，待签审。按目标时间点和测试划分记录；转入关联的时间漂移证据。 |
| EV-20261026-13 | C-20261026-13 | pending_review | [[03-paper-notes/2026-TDSC-Fooling_Multi-Tab_Browsing__Few-Shot_Website_Fingerprinting_Attacks_and_Lightweight_Obfuscation_Defenses]] | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| EV-20261026-14 | C-20261026-14 | pending_review | [[03-paper-notes/2026-TDSC-GenETC__Dynamic_Graph-enhanced_Fine-tuning_for_Encrypted_Traffic_Classification]] | CLM-0203 | EV-V2-GENETC-PRETRAIN | 已定位原文，待签审。已核对保留图模块的预训练消融。 |
| EV-20261026-15 | C-20261026-15 | pending_review | [[03-paper-notes/2026-TDSC-Generating_Adversarial_Network_Traffic_via_Multi-Model_Guided_Adversarial_Diffusion]] | — | — | 本轮范围外，保留历史。通用 IDS 的鲁棒性评测。 |
| EV-20261026-16 | C-20261026-16 | pending_review | [[03-paper-notes/2026-TDSC-Is_the_Data_Really_Noisy_Rethinking_Traffic_Filtering_for_Encrypted_Traffic_Classification]] | CLM-0003、CLM-0007、CLM-0103 | — | 候选或条件差异，待复核。另需核对分组单位、可见字段与标签来源。 |
| EV-20261026-17 | C-20261026-17 | pending_review | [[03-paper-notes/2026-TDSC-QuicReflo__Exploiting_Multi-Flow_Redundancy_for_Restoration-Free_Covert_Communication_Over_QUIC]] | — | — | 本轮范围外，保留历史。QUIC 隐蔽通信机制。 |
| EV-20261026-18 | C-20261026-18 | pending_review | [[03-paper-notes/2026-TDSC-RearView__Secure_Two-Stage_Malicious_Traffic_Identification_with_Dynamic_Relationship_Awareness]] | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| EV-20261026-19 | C-20261026-19 | pending_review | [[03-paper-notes/2026-TDSC-TridentDNS__Detecting_Diverse_DNS_Tunnels_Via_Multidimensional_Features]] | CLM-0609 | — | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| EV-20261026-20 | C-20261026-20 | pending_review | [[03-paper-notes/2026-TIFS-DualGuard__An_Adaptive_Detection_Framework_for_Concurrent_Malicious_and_Normality_Drifts_in_Network_Traffic]] | — | — | 本轮范围外，保留历史。恶意软件概念漂移的训练流程。 |
| EV-20261026-21 | C-20261026-21 | pending_review | [[03-paper-notes/2026-TIFS-Feign_East_Strike_West_Constructing_Covert_Channel_on_TLS_1.3]] | — | — | 本轮范围外，保留历史。TLS 隐蔽信道实验。 |
| EV-20261026-22 | C-20261026-22 | pending_review | [[03-paper-notes/2026-TIFS-InvisiTunnel__Causality-Preserving_Covert_Communication_over_DoH_through_Request_Substitution]] | — | — | 本轮范围外，保留历史。DoH 隧道，与 ToP 低误报任务不同。 |
| EV-20261026-23 | C-20261026-23 | pending_review | [[03-paper-notes/2026-TIFS-Stego-Vector_Driven_Simultaneous_Covert_Channels_in_Streaming_Applications]] | — | — | 本轮范围外，保留历史。流媒体隐蔽信道。 |
| EV-20261026-24 | C-20261026-24 | pending_review | [[03-paper-notes/2026-TIFS-Two_Heads_Are_Better_Than_One__Models-to-Model_Learning_for_Encrypted_Traffic_Analysis]] | CLM-0403 | — | 候选或条件差异，待复核。需匹配视图定义、骨干、标注/训练预算及迁移测试。 |
| EV-20261026-25 | C-20261026-25 | pending_review | [[03-paper-notes/2026-TIFS-Two_Heads_Are_Not_Better_Than_One__Continual_Learning_From_Multiple_Models_for_Encrypted_Traffic_Analysis]] | CLM-0403 | — | 候选或条件差异，待复核。需匹配视图定义、骨干、标注/训练预算及迁移测试。 |
| EV-20261026-26 | C-20261026-26 | pending_review | [[03-paper-notes/2026-TON-Avatar__Securing_Anonymous_Communication_With_Relay_Anonymity]] | — | — | 本轮范围外，保留历史。匿名路由或混合网络的流量关联，目标与七条前沿不同。 |
| EV-20261026-27 | C-20261026-27 | pending_review | [[03-paper-notes/2026-TON-Enabling_Entangled_Cache_Probing_for_Remotely_Reconstructing_DNS_Query_Dynamics]] | — | — | 本轮范围外，保留历史。DNS 缓存与测量任务。 |
| EV-20261026-28 | C-20261026-28 | pending_review | [[03-paper-notes/2026-TON-Encrypted_Network_Traffic_Classification_Using_Generative_and_Contrastive_Self-Supervised_Learning]] | CLM-0204 | — | 候选或条件差异，待复核。单模型/任务结果，需核对同预算的去预训练对照与测试域。 |
| EV-20261026-29 | C-20261026-29 | pending_review | [[03-paper-notes/2026-TON-Fighting_the_Enemy_Within__Traffic_Semantics-Driven_Framework_Against_Noisy_Labels_for_Robust_Traffic_Classification]] | CLM-0003、CLM-0007、CLM-0103 | — | 候选或条件差异，待复核。另需核对分组单位、可见字段与标签来源。 |
| EV-20261026-30 | C-20261026-30 | pending_review | [[03-paper-notes/2026-TON-KAN-Vis__Efficient_and_Lightweight_Visual_Technique_for_Network_Traffic_Classification_Using_KolmogorovArnold_Network]] | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| EV-20261026-31 | C-20261026-31 | pending_review | [[03-paper-notes/2026-TON-Making_the_Best_of_Both_Worlds__Universal_Perturbations_for_Live_Black-Box_Evasion_Against_NIDS_in_Encrypted_Traffic]] | — | — | 本轮范围外，保留历史。通用 IDS 扰动及鲁棒性评估。 |
| EV-20261026-32 | C-20261026-32 | pending_review | [[03-paper-notes/2026-TON-QDCR__DNSQUIC_Cross-Protocol_Traffic_Amplification_for_Denial-of-Service_Attacks]] | — | — | 本轮范围外，保留历史。跨协议流量放大测量。 |
| EV-20261026-33 | C-20261026-33 | pending_review | [[03-paper-notes/2026-TON-SRViT__A_Robust_Online_Encrypted_Traffic_Classification_Based_on_Vision_Transformer]] | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| EV-20261026-34 | C-20261026-34 | pending_review | [[03-paper-notes/2026-TON-When_Pre-Training_Meets_Contrast_Learning__Few-Shot_Encrypted_Traffic_Classification_With_Novelty_Detection]] | CLM-0204 | — | 候选或条件差异，待复核。单模型/任务结果，需核对同预算的去预训练对照与测试域。 |
| EV-COSINT-01 | COSINT-01 | pending_review | [[03-paper-notes/2026-COSINT-北邮时金桥]] | CLM-0607、CLM-0609 | EV-V2-COSINT-DHOR | 相邻任务，留待核验。报告页可定位，五分类与基率保留为相邻信号；完整配置和分母仍待复核。 |
| EV-COSINT-02 | COSINT-02 | pending_review | [[03-paper-notes/2026-COSINT-北邮时金桥]] | CLM-0607、CLM-0609 | EV-V2-COSINT-DHOR | 相邻任务，留待核验。报告页可定位，五分类与基率保留为相邻信号；完整配置和分母仍待复核。 |
| EV-COSINT-03 | COSINT-03 | pending_review | [[03-paper-notes/2026-COSINT-北邮时金桥]] | CLM-0608、CLM-0609 | EV-V2-COSINT-DHBCORR | 相邻任务，留待核验。报告页可定位，双侧候选与资源口径单列，未与单点检测相比较。 |
| EV-COSINT-04 | COSINT-04 | pending_review | [[03-paper-notes/2026-COSINT-北邮时金桥]] | CLM-0608、CLM-0609 | EV-V2-COSINT-DHBCORR | 相邻任务，留待核验。报告页可定位，双侧候选与资源口径单列，未与单点检测相比较。 |
| EV-20261118-GRAPH-CAL | KB-20261118-GRAPH-CAL | pending_review | [[03-paper-notes/2025-NIPS-Self-Supervised_Learning_of_Graph_Representations_for_Network_Intrusion_Detection]] | CLM-0104、CLM-0103 | EV-V2-GRAPHIDS-VERSIONS | 已定位原文，待签审。已从 Table 3 核对同底层语料不同版本和标签校准。 |
| EV-20261118-NEPCO-COST | KB-20261118-NEPCO-COST | pending_review | [[03-paper-notes/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC]] | — | — | 本轮范围外，保留历史。SmartNIC 通量和观察成本。 |
| EV-20261118-NEPCO-BYTE | KB-20261118-NEPCO-BYTE | pending_review | [[03-paper-notes/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC]] | CLM-0504 | — | 候选或条件差异，待复核。需控制预处理、字段可见性及有效字节/Token 预算。 |
| EV-20261118-HAD-DRIFT | KB-20261118-HAD-DRIFT | pending_review | [[03-paper-notes/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection]] | CLM-0609 | — | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| EV-20261118-SAT-RTT | KB-20261118-SAT-RTT | pending_review | [[03-paper-notes/2026-S&P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency]] | CLM-0609 | — | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| EV-20261118-CRYPTO-MODAL | KB-20261118-CRYPTO-MODAL | pending_review | [[03-paper-notes/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture]] | CLM-0005、CLM-0403 | EV-V2-CRYPTO-CONTENT | 已定位原文，待签审。已核对混合语料及内容消融。纯密文归因待单独试验。 |
| EV-20261118-MPA-EXT | KB-20261118-MPA-EXT | pending_review | [[03-paper-notes/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models]] | — | — | 本轮范围外，保留历史。流量矩阵重构扩展。 |
| EV-20261118-PSML-READ | KB-20261118-PSML-READ | pending_review | [[03-paper-notes/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures]] | — | — | 本轮范围外，保留历史。遥测查询校正。 |
| EV-20261118-SEDMS-UPDATE | KB-20261118-SEDMS-UPDATE | pending_review | [[03-paper-notes/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks]] | — | — | 本轮范围外，保留历史。遥测更新开销。 |
| EV-20261118-T2T-COVER | KB-20261118-T2T-COVER | pending_review | [[03-paper-notes/2026-ICML-Threat2Traffic__Multi-Agent_Environment_Synthesis_for_Malware_Traffic_Generation_from_Threat_Intelligence]] | — | — | 本轮范围外，保留历史。威胁行为与合成语料覆盖。 |
| EV-20261118-COSINT-NORMAL-REF | KB-20261118-COSINT-NORMAL-REF | pending_review | [[03-paper-notes/2026-COSINT-北邮时金桥]] | CLM-0609 | — | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| EV-20261118-COSINT-TIMING | KB-20261118-COSINT-TIMING | pending_review | [[03-paper-notes/2026-COSINT-北邮时金桥]] | CLM-0609 | — | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| EV-20261118-COSINT-COST | KB-20261118-COSINT-COST | pending_review | [[03-paper-notes/2026-COSINT-北邮时金桥]] | CLM-0609 | — | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| EV-20261118-L3-T2T-COVERAGE-F1 | KB-20261118-L3-T2T-COVERAGE-F1 | pending_review | [[03-paper-notes/2026-ICML-Threat2Traffic__Multi-Agent_Environment_Synthesis_for_Malware_Traffic_Generation_from_Threat_Intelligence]] | — | — | 本轮范围外，保留历史。威胁行为真值覆盖。 |
| EV-20261118-L3-CONTORTER-UNIT | KB-20261118-L3-CONTORTER-UNIT | pending_review | [[03-paper-notes/2026-S&P-A_Context_Is_Worth_a_Thousand_Lies__Evading_Intrusion_Detectors_via_Intelligent_Context_Distortion]] | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| EV-20261118-L3-CENRL-POOL | KB-20261118-L3-CENRL-POOL | pending_review | [[03-paper-notes/2026-S&P-CenRL__A_Framework_for_Performing_Intelligent_Censorship_Measurements]] | — | — | 本轮范围外，保留历史。主动测量候选池与部署评估。 |
| EV-20261118-L3-DESC-RESOURCE | KB-20261118-L3-DESC-RESOURCE | pending_review | [[03-paper-notes/2026-S&P-Descriptors_of_Exposure__Undermining_Tor_Anonymity_Through_Exploiting_Descriptor_Flood]] | — | — | 本轮范围外，保留历史。Tor 网络资源测量，不测试 ToP 分类。 |
| EV-20261118-L3-SIR-SCALE | KB-20261118-L3-SIR-SCALE | pending_review | [[03-paper-notes/2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR]] | — | — | 本轮范围外，保留历史。流式遥测窗口资源。 |
| EV-20261118-L3-MPA-JOINT | KB-20261118-L3-MPA-JOINT | pending_review | [[03-paper-notes/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models]] | — | — | 本轮范围外，保留历史。流量矩阵任务联合训练。 |

## 历史 Claims

| 迁移编号 | 原位置及题意 | 旧 ID | 新命题 ID | 关联证据 | 处置依据 |
| --- | --- | --- | --- | --- | --- |
| LEG-C-001 | [[claims-index#观点记录]] 第 1 项 · 现有公开数据集（ISCXVPN2016、USTC-TFC2016 等）含 90%+ 未加密流量，导致多数加密流量分类器的高准确率是虚假的 | — | CLM-0004、CLM-0007 | EV-V2-SOK-CORPUS | 已定位原文，待签审。拆出语料盘点。高分类表现的原因另需对照。 |
| LEG-C-002 | [[claims-index#观点记录]] 第 2 项 · 强标识信息（SII：MAC 地址、IP 地址、端口号）是加密流量分类器过拟合的主要来源，匿名化 SII 后 ET-BERT 准确率从 0.96 暴跌至 0.51 | — | CLM-0003、CLM-0007 | EV-V2-SWEET-SPLIT | 已定位原文，待签审。划分与流身份对照有原文锚点，旧条目列举的其余归因需按数据另核。 |
| LEG-C-003 | [[claims-index#观点记录]] 第 3 项 · TLS 1.3 下加密 payload 不包含可学习的内在模式，分类器仅能利用 payload 长度信息 | — | CLM-0001、CLM-0002、CLM-0006、CLM-0007、CLM-0602 | EV-V2-SOK-CIPHERTEXT、EV-V2-LEAKAGE-THEOREM、EV-V2-IMC-REPLICATION、EV-V2-NEST-CONFIRM | 已定位原文，待签审。拆开纯密文对照、定理、统计复核及元数据可用实例。 |
| LEG-C-004 | [[claims-index#观点记录]] 第 4 项 · 已有加密流量表征学习模型（ET-BERT、YaTC、NetMamba 等）报告的高达 98% 的准确率主要源于 per-packet split 导致的数据泄漏，而非真正有意… | — | CLM-0003、CLM-0007 | EV-V2-SWEET-SPLIT | 已定位原文，待签审。划分与流身份对照有原文锚点，旧条目列举的其余归因需按数据另核。 |
| LEG-C-005 | [[claims-index#观点记录]] 第 5 项 · 在正确的 per-flow split 和 frozen encoder 设置下，已有表征学习模型的准确率暴跌至 30%-40%（TLS-120 任务上 ET-BERT F1… | — | CLM-0003、CLM-0007 | EV-V2-SWEET-SPLIT | 已定位原文，待签审。划分与流身份对照有原文锚点，旧条目列举的其余归因需按数据另核。 |
| LEG-C-006 | [[claims-index#观点记录]] 第 6 项 · 在正确的评估设置下，使用手工特征的浅层模型（RF/XGBoost/LightGBM）优于所有深度表征学习模型 | — | CLM-0101、CLM-0103 | EV-V2-SWEET-BASELINES | 已定位原文，待签审。只保留作者所测基线和输入范围；跨模型排序列为问题。 |
| LEG-C-007 | [[claims-index#观点记录]] 第 7 项 · 预训练范式在加密流量分类中极为有效：去除预训练后 ET-BERT 的 F1 从 93.95% 降至 56.38%（-37.57%） | — | CLM-0201、CLM-0204 | EV-V2-ETBERT-PRETRAIN | 已定位原文，待签审。原协议的消融和一般预训练收益分别登记。 |
| LEG-C-008 | [[claims-index#观点记录]] 第 8 项 · 流量字节更类似于图像像素而非自然语言词汇，90% 的最优 mask ratio 远高于 NLP 任务（<20%），说明流量数据存在大量信息冗余 | — | CLM-0504 | — | 候选或条件差异，待复核。需控制预处理、字段可见性及有效字节/Token 预算。 |
| LEG-C-009 | [[claims-index#观点记录]] 第 9 项 · 包长度（packet length）、包方向（packet direction）和包时间（packet timing）是加密流量分析中最常用且最有效的三类特征 | — | CLM-0602、CLM-0401 | EV-V2-NEST-CONFIRM、EV-V2-MM4FLOW-MODAL | 已定位原文，待签审。现有实例可说明所用可见特征；跨任务效用排序待同输入对照。 |
| LEG-C-010 | [[claims-index#观点记录]] 第 10 项 · 深层 CNN（8 层 Conv）能有效攻破 WTF-PAD 防御（90.7% 准确率），但 Walkie-Talkie 的对称 collision 机制仍能限制攻击至约 50% | — | CLM-0301 | EV-V2-DF-DEFENSES | 已定位原文，待签审。已定位闭集表格，两种防御条件分别记录。 |
| LEG-C-011 | [[claims-index#观点记录]] 第 11 项 · 网络流是天然的多模态数据，融合 payload byte stream（内容模态）和 packet length sequence（行为模态）可实现跨任务通用分析，加密隧道网… | — | CLM-0401、CLM-0403 | EV-V2-MM4FLOW-MODAL | 已定位原文，待签审。保留单视图和任务依赖；相对结果与跨任务推广分别处理。 |
| LEG-C-012 | [[claims-index#观点记录]] 第 12 项 · 仅标注千分之一的流量样本即可达到 99.82% 的恶意流量检测精度，超越 14 种现有方法 12.76% 以上 | — | CLM-0403 | — | 候选或条件差异，待复核。需匹配视图定义、骨干、标注/训练预算及迁移测试。 |
| LEG-C-013 | [[claims-index#观点记录]] 第 13 项 · 领域专用 tokenization 是 LLM 应用于流量分析的关键：去除后 F1 下降 6.53%，通用 NLP tokenizer 效果远差于领域 BPE tokeniz… | — | CLM-0501、CLM-0504 | EV-V2-MET-EMBEDDING | 已定位原文，待签审。区分去除该模块与通用 BPE 的两个对照。 |
| LEG-C-014 | [[claims-index#观点记录]] 第 14 项 · 通过动态调整时间间隔大小对齐不同网络条件下的流量分布，仅需每网站 5 个标注样本即可在 WF 防御场景下平均超越 SOTA 攻击 17.50% 的准确率 | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-015 | [[claims-index#观点记录]] 第 15 项 · 对比学习结合语义属性矩阵（SAM）可实现对流量混淆的鲁棒检测，在 evasion attack 场景下 F1 和 AUC 均超过 93%，比 SOTA 平均提升 19.84% | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-016 | [[claims-index#观点记录]] 第 16 项 · 轻量级可解释网络 LEXNet（119k 参数）在 200 类商业级流量数据集上达到 89.7% 准确率，同时提供 100% 忠实的 by-design 解释，远优于 pos… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-017 | [[claims-index#观点记录]] 第 17 项 · 因果链（causality chain）解耦混合流量的方法天然抵抗 packet loss/duplication/disorder，在多标签 WF 场景下 Jaccard … | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-018 | [[claims-index#观点记录]] 第 18 项 · 2-gram tokenization 的 masked token 可由相邻 token 直接推断（如 06D6 和 0100 之间的 mask 必然是 D601），无法学… | — | CLM-0502、CLM-0504 | EV-V2-TRAFFICFORMER-OVERLAP | 已定位原文，待签审。只采用相邻重叠的输入定义；掩码可恢复性和分类收益待测。 |
| LEG-C-019 | [[claims-index#观点记录]] 第 19 项 · 预训练数据规模从 GB 级提升到 TB 级（77.6 TB）带来显著性能增益，数据多样性比模型复杂度更重要 | — | CLM-0204 | — | 候选或条件差异，待复核。单模型/任务结果，需核对同预算的去预训练对照与测试域。 |
| LEG-C-020 | [[claims-index#观点记录]] 第 20 项 · MET-LLM 仅需 100 个新样本和 20 秒即可达到 94.2% 的检测准确率，比完全重训练快 150 倍 | — | CLM-0501、CLM-0504 | — | 候选或条件差异，待复核。目标样本适配耗时和 tokenizer 受控比较对应不同协议。 |
| LEG-C-021 | [[claims-index#观点记录]] 第 21 项 · WSA（Word Sense Aggregation）将 inter-class 高频词重叠降低约 36%（top 10），证明无参数词义聚合可有效改善分类质量 | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-022 | [[claims-index#观点记录]] 第 22 项 · 移除 CSS（Category Semantic Separator）后 macro F1 从 0.9861 暴跌至 0.5998（USTC-TFC task2），证明显式语… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-023 | [[claims-index#观点记录]] 第 23 项 · 简单类别列表 prompt（99.65%）优于复杂指令 prompt（96.23%），证明流量分类场景下无需复杂的 prompt engineering | — | CLM-0504 | — | 候选或条件差异，待复核。需控制预处理、字段可见性及有效字节/Token 预算。 |
| LEG-C-024 | [[claims-index#观点记录]] 第 24 项 · Linear attention 实现 12K token 容量（从 512 扩展），达成 SOTA 分类性能（average F1 +2%）和逼真 pcap 生成（disc… | — | CLM-0504 | — | 候选或条件差异，待复核。需控制预处理、字段可见性及有效字节/Token 预算。 |
| LEG-C-025 | [[claims-index#观点记录]] 第 25 项 · 多模态特征（SIF payload 语义 + 统计特征）达成 F1 0.9356 vs 单模态 0.8141，提升 12.15%，证明多模态融合在加密流量分类中的有效性 | — | CLM-0403 | — | 候选或条件差异，待复核。需匹配视图定义、骨干、标注/训练预算及迁移测试。 |
| LEG-C-026 | [[claims-index#观点记录]] 第 26 项 · 静默应用（silent applications）加速模型稳定性衰减；移除其参数可提升准确率 8.64% 以上，说明持续学习中应识别并处理不活跃类别 | — | — | — | 本轮范围外，保留历史。持续学习中不活跃类别的维护。 |
| LEG-C-027 | [[claims-index#观点记录]] 第 27 项 · NetMamba 是首个将 Mamba/SSM 架构应用于流量分类的工作，速度比 Transformer 快 60 倍且准确率相当 | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-028 | [[claims-index#观点记录]] 第 28 项 · SSM 架构（Mamba）比 Transformer 参数量减少 72 倍但性能接近，多模态融合（头部+载荷）进一步提升 F1 +8.69%；OOD 检测对真实部署至关重要 | — | CLM-0103、CLM-0204、CLM-0403 | — | 候选或条件差异，待复核。原条目合并了参数、表示、初始化与多视图，缺匹配反事实。 |
| LEG-C-029 | [[claims-index#观点记录]] 第 29 项 · 异质 MoE（头部+载荷分开路由）优于同质 MoE，F1 差距 5.33%；预训练不可或缺，去除后 F1 下降 24.4%；Payload-only MoE F1 仅 45.… | — | CLM-0103、CLM-0204、CLM-0403 | — | 候选或条件差异，待复核。原条目合并了参数、表示、初始化与多视图，缺匹配反事实。 |
| LEG-C-030 | [[claims-index#观点记录]] 第 30 项 · 零样本 WF 可匹配其他方法 8-shot 水平；三个对齐锚点（IP 分组、请求-响应、TLS 特征）揭示协议结构泄漏；CMA 贡献最大（+10.75%） | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-031 | [[claims-index#观点记录]] 第 31 项 · DL 分类器大量依赖捷径特征（IP/Timestamp/端口）；遮蔽捷径特征后准确率反常上升（USTC-TFC2016, Ransomware），说明模型存在虚假学习 | — | CLM-0003、CLM-0007 | EV-V2-SWEET-SPLIT、EV-V2-BIAS-FIELD | 已定位原文，待签审。划分与流身份对照有原文锚点，旧条目列举的其余归因需按数据另核。 |
| LEG-C-032 | [[claims-index#观点记录]] 第 32 项 · 线性注意力替代标准注意力实现 12K token 容量，生成质量差距 5-6 倍；可逆 token 实现无损编解码；同时实现分类和生成的首个 GPT-style 流量模型 | — | CLM-0504 | — | 候选或条件差异，待复核。需控制预处理、字段可见性及有效字节/Token 预算。 |
| LEG-C-033 | [[claims-index#观点记录]] 第 33 项 · 单向 Mamba 优于双向（因果性更适合流量序列）；MAE 预训练显著提升性能；参数量仅 Transformer 的 1/85；90% mask ratio 有效（与 YaT… | — | CLM-0204 | — | 候选或条件差异，待复核。单模型/任务结果，需核对同预算的去预训练对照与测试域。 |
| LEG-C-034 | [[claims-index#观点记录]] 第 34 项 · 简单流量调度攻击即可使基于跨层 RTT 的最强住宅代理检测器召回率从 99% 跌至 8%，而流相关性特征+Transformer（CorrTransform）在调度/填充/重… | — | CLM-0609 | — | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| LEG-C-035 | [[claims-index#观点记录]] 第 35 项 · 使用真实 Tor 用户流量作为开放世界非监控集（800K+ traces），DF 攻击仍达 π₁₀=0.956、召回 0.922，首次证明 WF 攻击在真实 Tor 开放世界… | — | CLM-0304 | EV-V2-WF-REALITY | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-036 | [[claims-index#观点记录]] 第 36 项 · 效率优先的加密系统中，只要存在一对统计可区分的应用语义，侧信道泄漏互信息 I(X;Y)>0 就不可避免（侧信道存在性定理），且给出显式下界 I(X;Y) ≥ (1/2ln2)… | — | CLM-0002 | EV-V2-LEAKAGE-THEOREM | 已定位原文，待签审。按定理假设限制正互信息下界的对象。 |
| LEG-C-037 | [[claims-index#观点记录]] 第 37 项 · 字节级掩码预训练迁移性差的根因是归纳偏置错配（冻结编码器评估下准确率从 >90% 骤降至 <47%），改为协议原生表格预训练（FlowSem-MAE）后 50.25M 参数在… | — | CLM-0003、CLM-0007、CLM-0103 | EV-V2-FLOWSEM-FROZEN | 候选或条件差异，待复核。另需核对分组单位、可见字段与标签来源。 |
| LEG-C-038 | [[claims-index#观点记录]] 第 38 项 · 以 ImageNet 预训练教师+上下文掩码蒸馏替代重建式自监督的"零正样本"异常检测范式，仅用正常流量训练即在 DataCon2020/CIC-IDS2017 上分别达 A… | — | — | — | 本轮范围外，保留历史。只以正常流训练的异常检测设定。 |
| LEG-C-039 | [[claims-index#观点记录]] 第 39 项 · 后门学习式 WF 防御以仅 73.7% 数据开销将 RF 攻击准确率从 99% 压至 4.7%（同量级开销下 FRONT 仅 −2%、Palette 31.6% 需 122.… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-040 | [[claims-index#观点记录]] 第 40 项 · 单侧部署的网内混淆（IP 分片+小 TTL 假包+隐式 ICMP）将 Var-CNN 攻击准确率从 99.40% 降至 3.51%（−95.89%），带宽开销仅 6.21%（… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-041 | [[claims-index#观点记录]] 第 41 项 · 不确定性感知融合（证据深度学习+Dempster-Shafer）在 <2% 标注的极端弱信息场景将 DoHBrw AUC 从 85.45% 提升至 89.57%，50% 标签… | — | CLM-0403 | — | 候选或条件差异，待复核。需匹配视图定义、骨干、标注/训练预算及迁移测试。 |
| LEG-C-042 | [[claims-index#观点记录]] 第 42 项 · 通过时间包密度驱动的自调整数据增强+多流时序图学习，仅用完整流量的前 20% 即可达平均 F1 95.11%（较 SOTA YaTC 高 8.7 个百分点） | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-043 | [[claims-index#观点记录]] 第 43 项 · 训练自 D1 的模型在检测未见恶意软件家族的零样本场景保持 F1 91.34%，并在 48:1 极端不平衡下 F1 92.9%，四个早期/鲁棒性场景全面领先 | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-044 | [[claims-index#观点记录]] 第 44 项 · 实测发现决策树各层精度边际贡献递减（前 60% 层即可达 >90% 精度、后 40% 层仅贡献 5-10%），据此关键/普通子树异构切分+两阶段 MILP 部署，将网内检测精… | — | — | — | 本轮范围外，保留历史。网内决策树部署。 |
| LEG-C-045 | [[claims-index#观点记录]] 第 45 项 · 利用训练期才可得的应用层资源序列做特权信息蒸馏（LUPI），在 150 天时间漂移下将 Var-CNN 的 F1 从 72.77% 提升至 81.49%（+8.72），代理漂… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-046 | [[claims-index#观点记录]] 第 46 项 · 单环境训练无法跨环境迁移（IoT→传统 IP 迁移准确率全部 <0.20、反向最高仅 0.46），证实多环境融合数据集（M-En）对真实部署的必要性；且 LR 实时准确率 0… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-047 | [[claims-index#观点记录]] 第 47 项 · 多粒度 Patch Transformer 在 5 标签页混合流量闭世界达 P@5 87.54%、MAP@5 91.63%（超 ARES 3.25pp），开放世界 5-tab… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-048 | [[claims-index#观点记录]] 第 48 项 · 0.321M 参数的轻量自监督对比 ViT 在 6 个真实数据集平均准确率 98.10%，GPU 推理 2.67ms，比最强自监督 baseline（YaTC）快约 8.7 … | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-049 | [[claims-index#观点记录]] 第 49 项 · 模型跨时间泛化能力弱：MAWI 上训练后仅 3 周，恶意流量 F1 即从 53.65% 跌至 17.64%（2021）/9.63%（2023），流量检测模型的时变退化有定量证据 | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-050 | [[claims-index#观点记录]] 第 50 项 · 仅 HTTP/2 资源数量一项应用层特征就泄露 4.28 bit 信息（超过 98% 已知特征），每站仅 1 个参考样本（N=1）即在真实 HTTPS 场景达 87.7% 准… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-051 | [[claims-index#观点记录]] 第 51 项 · 非对称对抗防御 FPD 在平均方向/长度双判别器 DSR 97.10% 下带宽开销仅 1.81%（单页场景 DSR 93.98%），且对再训练攻击保持有效 | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-052 | [[claims-index#观点记录]] 第 52 项 · 对抗训练在 AdvTraffic 类新防御下 DF 准确率仅 10.2%，而条件扩散净化（DTPN）无需重训即可让已有 WF 分类器恢复至 71.0%（去除条件嵌入/分类损失… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-053 | [[claims-index#观点记录]] 第 53 项 · 4-bit+8-bit 多粒度流量单元构建的多视图异构图在 ISCX-VPN 流级 F1 达 0.9941、CIC-IoT 0.9896（Avg Rank 均第一），去除异质… | — | CLM-0504 | — | 候选或条件差异，待复核。需控制预处理、字段可见性及有效字节/Token 预算。 |
| LEG-C-054 | [[claims-index#观点记录]] 第 54 项 · FT-Transformer 在 OS 指纹识别 DAT1 上 F1 90.80（LSTM 仅 76.87），参数量比 TabT 少约 2300 倍（6.6 万–49.6 万… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-055 | [[claims-index#观点记录]] 第 55 项 · 平均每包仅 4 字节的 QUIC 隐蔽信道（基于 MPS 游程序列生成建模）使能力最大化对抗模型下最强检测器 NeuTic 准确率仅约 62.4%，NetBeacon/Flo… | — | — | — | 本轮范围外，保留历史。QUIC 隐蔽信道与通用检测器对照。 |
| LEG-C-056 | [[claims-index#观点记录]] 第 56 项 · 攻击者仅需 +7.4% 带宽开销即可完全规避 FlowLens 的 top-K 选择式测量（FNR 0.928），而 sketch 全量逐流测量无选择逻辑，将 DDoS 检测… | — | — | — | 本轮范围外，保留历史。测量机制与数据面选择。 |
| LEG-C-057 | [[claims-index#观点记录]] 第 57 项 · 多模态 LLM 流量解读（mmTraffic）中解冻流量编码器是关键拐点：Tor 分类准确率从 0.7092 提升至 0.8674（冻结时 ISCXVPN2016 仅 0.2… | — | CLM-0403 | — | 候选或条件差异，待复核。需匹配视图定义、骨干、标注/训练预算及迁移测试。 |
| LEG-C-058 | [[claims-index#观点记录]] 第 58 项 · 控制探测目的地即可制造路径多样性：60 周、120 国、144,418 个住宅代理 vantage point 的测量显示 91.7%（110/120）国家存在审查不一致，仅… | — | — | — | 本轮范围外，保留历史。审查测量路径与位置。 |
| LEG-C-059 | [[claims-index#观点记录]] 第 59 项 · 云商 peering 决定审查暴露且可被规避利用：同国同地不同云平台的审查差最高 66.72（韩国 AWS 98.93% vs GCP 32.21%）、32.32（印度 AW… | — | — | — | 本轮范围外，保留历史。云商互联与审查测量。 |
| LEG-C-060 | [[claims-index#观点记录]] 第 60 项 · 以 AES 16 字节块为单元（4×4 block → 4 包拼成 32×32 矩阵）构造 BTR 表征并用 intra-block/inter-block/inter-pa… | — | CLM-0003、CLM-0007、CLM-0103 | EV-V2-BTR-BLOCK | 候选或条件差异，待复核。另需核对分组单位、可见字段与标签来源。 |
| LEG-C-061 | [[claims-index#观点记录]] 第 61 项 · MAE 预训练收益随数据规模与任务而变：ISCXTor2016 f1 ↓17.91、ISCXVPN2016 ↓12.27，而 CICIoT2022 仅 ↓2.07、USTC-… | — | CLM-0204 | — | 候选或条件差异，待复核。单模型/任务结果，需核对同预算的去预训练对照与测试域。 |
| LEG-C-062 | [[claims-index#观点记录]] 第 62 项 · 把 bin 边界当作以下游模型精度为目标的超参数（TPE 贝叶斯优化 + 嵌套交叉验证）可同时提升精度与压缩表示：包大小维度非均匀化在全部任务、全部表示大小上优于均匀/统计/… | — | CLM-0504 | — | 候选或条件差异，待复核。需控制预处理、字段可见性及有效字节/Token 预算。 |
| LEG-C-063 | [[claims-index#观点记录]] 第 63 项 · 置信度触发的提前分类级联（EC）在几乎不损精度下大幅降时延：VPN Services 平均分类时间 1.01s vs 全时延基线 5s 且最终精度更高；α=5% 时精度损失 … | — | CLM-0609 | — | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| LEG-C-064 | [[claims-index#观点记录]] 第 64 项 · 对比学习的增强方式在长尾场景是生死线：仅用 encoder dropout、p=0.10 时三数据集整体准确率 89.9/91.3/92.9，而 p=0（无增强）骤降至 58… | — | CLM-0204 | — | 候选或条件差异，待复核。单模型/任务结果，需核对同预算的去预训练对照与测试域。 |
| LEG-C-065 | [[claims-index#观点记录]] 第 65 项 · 三阶段渐进框架（流量增强自监督预训练 → 对抗域适配 → 少样本目标适配）可在跨域多标签页 WF 中用极少目标域标注取得领先：5-tab 闭世界 N=10 时 P@5 75.… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-066 | [[claims-index#观点记录]] 第 66 项 · 把加密通信建模为流式时序知识图谱（四元组 (u,p,v,τ) + 时间编码消息传递）并在其上做自监督对比学习，可在完全无标注条件下于 UNSW-NB15/ToN-IoT/CI… | — | CLM-0204 | — | 候选或条件差异，待复核。单模型/任务结果，需核对同预算的去预训练对照与测试域。 |
| LEG-C-067 | [[claims-index#观点记录]] 第 67 项 · 把丢包/乱序下的不完整观测建模为同一流的多视图，并只在可对齐的重叠包集合上做表示与预测两层一致性（重叠门控 w(r)=I(r≥τ)·r^γ，τ=0.2、γ=1.2），可在 K… | — | CLM-0609 | — | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| LEG-C-068 | [[claims-index#观点记录]] 第 68 项 · 明文协议文本特征对细粒度攻击类型分类反而有害：移除文本视图后攻击类型 Macro F1 从 79.40% 升至 91.74%，作者归因于指向同一服务器的不同攻击共享文本签名（… | — | CLM-0403 | — | 候选或条件差异，待复核。需匹配视图定义、骨干、标注/训练预算及迁移测试。 |
| LEG-C-069 | [[claims-index#观点记录]] 第 69 项 · 把锚点流+前后各两流构成的 5 流短窗口上下文编码为 3×40×40 三通道矩阵（Len/Time/Dire，每流 80 patch、共 400 patch）并做包级+流级双… | — | CLM-0204 | — | 候选或条件差异，待复核。单模型/任务结果，需核对同预算的去预训练对照与测试域。 |
| LEG-C-070 | [[claims-index#观点记录]] 第 70 项 · 仅用 ≤MTU 的服务器侧协议级填充（TLS 1.3 record padding / QUIC PADDING）即可在 0.37–0.84% 带宽开销、0.03 MFLOP… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-071 | [[claims-index#观点记录]] 第 71 项 · 在流级划分（5-tuple，无跨集泄漏）的严格评测下，预训练初始化仍带来 3–5 个 F1 点增益且约 200k 步后饱和；消融显示任务特定融合（TSKF）比共享记忆库（MB… | — | CLM-0204 | — | 候选或条件差异，待复核。单模型/任务结果，需核对同预算的去预训练对照与测试域。 |
| LEG-C-072 | [[claims-index#观点记录]] 第 72 项 · 检索式分类（HNSW 最近邻 + 单一全局距离阈值）在加密流量上可与 Random Forest 精度持平（CESNET-TLS22 macro F1 0.923 对 0.9… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-073 | [[claims-index#观点记录]] 第 73 项 · 同分布 F1 98.9 与跨数据集 F1 79–83（recall >0.80）、留一族 LOFO 平均 F1 92.3 之间的落差量化了分布漂移代价；投毒比例从 1% 升到… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-074 | [[claims-index#观点记录]] 第 74 项 · 生成式流量模型必须报告"记忆 vs 生成"：REaLTabFormer 合成记录与训练集完全相同的比例仅 1.7%~56.5%（LLM/Transformer 类缺乏输入噪声… | — | — | — | 本轮范围外，保留历史。生成样本记忆度。 |
| LEG-C-075 | [[claims-index#观点记录]] 第 75 项 · 即使最先进的合成 WF 数据集仍系统性失真：GoodEnough 约 70% 域名中位电路长度顶到 5,000 cell 采集上限（GTT23 仅 32%）；中位域名出现频率… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-076 | [[claims-index#观点记录]] 第 76 项 · 时序对抗 reshaping 下方法分野巨大：MambaTIG F1 92.21%，图方法 MTSecurity 83.34%、ContraMTD 79.84%，而依赖原始包… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-077 | [[claims-index#观点记录]] 第 77 项 · 时序与结构表示的融合方式影响显著：线性插值 Z_fusion=(1−μ)Z_temporal+μZ_topological 优于 Concat（0.9912 vs 0.974… | — | CLM-0402、CLM-0403 | EV-V2-BPFDAG-ABLATION | 已定位原文，待签审。分支和融合差异在同篇表内可比较，跨域待测。 |
| LEG-C-078 | [[claims-index#观点记录]] 第 78 项 · 无监督域适配 + 少样本微调可在跨域 WF 中把所需辅助数据压到 2500 条：WF 数据集 20-shot 精度 97.37±0.07%（WFBDC 81.84、DCWF … | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-079 | [[claims-index#观点记录]] 第 79 项 · 零泄漏开放世界阈值可用分位数迁移得到：用 15 拟合类/3 留出类标定（ROC AUC 0.996），Youden 最优截断 216.411 对应 98.8 分位，迁移到 1… | — | CLM-0609 | — | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| LEG-C-080 | [[claims-index#观点记录]] 第 80 项 · 漂移样本的恶意性可在无人工标注下自动判定：「特征空间 DBSCAN 聚类 ∩ 物理空间宿主交互图聚集」的双空间一致性判据使识别准确率稳定 >97%；去掉任一空间维度后 C-D… | — | — | — | 本轮范围外，保留历史。漂移样本自动判定。 |
| LEG-C-081 | [[claims-index#观点记录]] 第 81 项 · 投毒式二级防御能以远低于伪装式防御的带宽开销取得高 SDR：DF 上 Stinger 平均 SDR 81.83%（带宽开销 12.38%，效率 6.61），AWF 上 83.… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-082 | [[claims-index#观点记录]] 第 82 项 · 关键字节在包内并非均匀分布而是高度聚集：注意力热力图显示关键区集中在 token 1–6（字节 1–96），尾部在约 800/960 字节处另有热点，且 12.7% 的 IS… | — | CLM-0504 | — | 候选或条件差异，待复核。需控制预处理、字段可见性及有效字节/Token 预算。 |
| LEG-C-083 | [[claims-index#观点记录]] 第 83 项 · 包级交互图（burst 建边）与加密无关且存在信息饱和点：每流 K=15 包、header 前 50 字节、payload 前 200 字节、Top-k 中 k=3 最优，n… | — | CLM-0007、CLM-0103、CLM-0504 | — | 候选或条件差异，待复核。特定输入预算和性能拐点保留，切换预算、字段或数据后另核。 |
| LEG-C-084 | [[claims-index#观点记录]] 第 84 项 · 把字节、包长、方向拼进同一条 L=192 的统一多模态 token 序列优于 late fusion：6 个可比数据集上 5 个更高，平均 F1 0.9089→0.9456 | — | CLM-0403 | EV-V2-HYTMTC-FUSION | 候选或条件差异，待复核。需匹配视图定义、骨干、标注/训练预算及迁移测试。 |
| LEG-C-085 | [[claims-index#观点记录]] 第 85 项 · 混合 Transformer-Mamba 骨干显著优于任一单骨干且更省参数：5 数据集均值 Mamba 0.8777 / Transformer 0.8701 / HyTMT… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-086 | [[claims-index#观点记录]] 第 86 项 · 检测式建模几乎免除了标签页数量先验：仅用 3-tab 数据微调的模型在 2–5 tab 混合测试集上 AUC 0.9612（与混合 tab 训练 0.9717 差距 <0.0… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-087 | [[claims-index#观点记录]] 第 87 项 · 在 Instance Separability 假设下把 trace 分析分解为「flow 编码 + 聚合」两阶段，并在 Orthogonality Criterion 下证… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-088 | [[claims-index#观点记录]] 第 88 项 · 仅用 trace 级弱监督即可获得可用的 flow 级归因：DAPT APT 案例中注意力最高分集中于 Privilege Escalation（0.9463）与 Data … | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-089 | [[claims-index#观点记录]] 第 89 项 · 对对抗训练（AT）鲁棒不蕴含对防御感知攻击鲁棒：RegulaTor/Palette/Adaptive Tamaraw 在 AT 攻击下准确率被压至较低水平，但 DAAE 恢复… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-090 | [[claims-index#观点记录]] 第 90 项 · 把建模单元从 TCP 包换成 TLS 记录并分层建模流内/流间依赖，可把 HTTPS WF 在分布偏移下的退化压到 ≤4.91 pp：2,008 类闭世界 95.41%（超 … | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-091 | [[claims-index#观点记录]] 第 91 项 · 漂移缓解所需的协议参数可从极少探针数据稳定估计：探针采样比 20%→5% 时每协议最优覆盖阈值 α* 完全不变（VMess/Shadowsocks 0.50、Trojan 0… | — | CLM-0609 | — | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| LEG-C-092 | [[claims-index#观点记录]] 第 92 项 · 用轻量 MLP 代理（770/385/385）预测样本级交叉熵损失、再按 CVaR 式尾部分数选出 top-B（B=32）样本更新骨干，可把 ET-BERT 在 USTC-T… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-093 | [[claims-index#观点记录]] 第 93 项 · 把压缩单元从权重/通道换成协议树图（PTG）本身，可在 CSTNET-TLS1.3 / CipherSpectrum 上用 0.186M / 0.481M 参数（较 Full… | — | CLM-0504 | — | 候选或条件差异，待复核。需控制预处理、字段可见性及有效字节/Token 预算。 |
| LEG-C-094 | [[claims-index#观点记录]] 第 94 项 · 在严格侧信道特征下可推导出无需训练的平衡准确率上界：继承式基准上界 ≤0.7589（USTC-TFC2016 0.7589、ISCXVPN2016 activity 0.61… | — | CLM-0003、CLM-0007、CLM-0103 | — | 候选或条件差异，待复核。另需核对分组单位、可见字段与标签来源。 |
| LEG-C-095 | [[claims-index#观点记录]] 第 95 项 · 类条件扩散增强（TDDM）是唯一在 TLS-120class 与 VPN-6class 上取得统计显著增益的生成方法（相对无增强的 Melatt，F1 +9.98% / +5… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-096 | [[claims-index#观点记录]] 第 96 项 · TLS 1.3 混合后量子密钥建立（X25519MLKEM768，KeyShare 从 32B 增至 1216/1120B）造成的协议漂移不消灭网站可学习性（匹配域 N-N … | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-097 | [[claims-index#观点记录]] 第 97 项 · 服务端防御的有效性由『泄漏是否集中于单一连接』决定而非防御机制本身：泄漏集中时可只保护最泄漏的单台服务器（Amazon CDN K*=24.47、Reddit 1st-par… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-098 | [[claims-index#观点记录]] 第 98 项 · VR 生态测量：75 款流行 VR 应用中 63 款多人上行链路使用明文 UDP（仅 12 款 DTLS/QUIC），且即使序列化格式未知，运动更新仍在 payload 固定… | — | — | — | 本轮范围外，保留历史。VR 数据采集与明文调查。 |
| LEG-C-099 | [[claims-index#观点记录]] 第 99 项 · VoIP 封锁主要靠 STUN 信令的应用专属属性指纹实现，而非流量统计特征：71 国中 19 国被观测到过滤，且用 P3（仅混淆指纹属性）后响应恢复到 P1 水平（What… | — | — | — | 本轮范围外，保留历史。VoIP 封锁测量。 |
| LEG-C-100 | [[claims-index#观点记录]] 第 100 项 · 应用侧宣称的"不可封锁"与网络侧可识别性存在系统性落差：143/281 应用可被端口/字符串/nDPI 至少一种启发式识别，而 38 个应用显式、58 个应用隐式宣称不可封锁… | — | — | — | 本轮范围外，保留历史。应用可封锁性测量。 |
| LEG-C-101 | [[claims-index#观点记录]] 第 101 项 · 多复合流水线交换机上数组切分式草图布局因冗余测量与流水线间负载失衡而系统性损失精度（最坏 80% 精度下跌、O(10^3) 误报）；改为每数组独占一条流水线的无切片布局并用合… | — | — | — | 本轮范围外，保留历史。遥测草图布局。 |
| LEG-C-102 | [[claims-index#观点记录]] 第 102 项 · 新增证据条目（2026-09-29）：Replicability 复制实验提示 NIST 随机性显著性不足以单独证明可利用的密文非随机模式；该结论需以原文完整统计表和控制条件… | — | CLM-0006、CLM-0007 | EV-V2-IMC-REPLICATION | 已定位原文，待签审。重新登记独立复核的统计信号和会话长度、划分控制。 |
| LEG-C-103 | [[claims-index#2026-09-29 新增待核验 Claims]] 第 1 项 · SemFuzz：语义规则驱动并以预期响应为 oracle 可发现深层协议漏洞；当前证据为论文摘要和评估章节，需核对逐协议表格。 | — | — | — | 本轮范围外，保留历史。协议测试。 |
| LEG-C-104 | [[claims-index#2026-09-29 新增待核验 Claims]] 第 2 项 · FENIX：FPGA增强交换机可在保持较高分类性能的同时实现线速推理；已定位流级 macro-F1=0.890，其他指标待表格核验。 | — | — | — | 本轮范围外，保留历史。网内线速推理。 |
| LEG-C-105 | [[claims-index#2026-09-29 新增待核验 Claims]] 第 3 项 · Wormhole：记忆化/快进可显著加速 LLM 训练包级仿真且 FCT 误差约≤1%；需核对 workload 与并行配置边界。 | — | — | — | 本轮范围外，保留历史。LLM 训练流量仿真。 |
| LEG-C-106 | [[claims-index#2026-09-29 新增待核验 Claims]] 第 4 项 · 高保真合成流量存在可量化隐私泄露风险；攻击适用性依赖生成模型是否保留标识符与完整流。 | — | — | — | 本轮范围外，保留历史。合成数据隐私。 |
| LEG-C-107 | [[claims-index#2026-09-29 新增待核验 Claims]] 第 5 项 · LLM 残差流隐蔽信道在受控开放权重部署中可规避多种检测器；不应外推到闭源 API。 | — | — | — | 本轮范围外，保留历史。LLM 隐蔽信道。 |
| LEG-C-108 | [[claims-index#2026-10-09 CCF-A 深度分析新增待审证据]] 第 1 项 · 2025-WWW-AdvTG__An_Adversarial_Traffic_Generation_Framework_to_Deceive_DL-Based_Malicio… | — | — | — | 本轮范围外，保留历史。通用检测系统鲁棒性。 |
| LEG-C-109 | [[claims-index#2026-10-09 CCF-A 深度分析新增待审证据]] 第 2 项 · 2025-WWW-Facing_Anomalies_Head-On__Network_Traffic_Anomaly_Detection_via_Uncertainty_In… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-110 | [[claims-index#2026-10-09 CCF-A 深度分析新增待审证据]] 第 3 项 · 2025-WWW-Do_Not_Trust_What_They_Tell__Exposing_Malicious_Accomplices_in_Tor_via_Anomalo… | — | — | — | 本轮范围外，保留历史。Tor 电路协作者检测。 |
| LEG-C-111 | [[claims-index#2026-10-09 CCF-A 深度分析新增待审证据]] 第 4 项 · 2026-NDSS-MVPNalyzer__An_Investigative_Framework_for_Auditing_the_Security_&_Privacy_of… | — | CLM-0609 | — | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| LEG-C-112 | [[claims-index#2026-10-09 CCF-A 深度分析新增待审证据]] 第 5 项 · 2026-NDSS-Identifying_Logical_Vulnerabilities_in_QUIC_Implementations：QUIC 逻辑漏洞证据来自实现覆盖… | — | — | — | 本轮范围外，保留历史。协议实现覆盖。 |
| LEG-C-113 | [[claims-index#2026-10-21：NestTor 已核验观点]] 第 1 项 · NestTor 的匹配结构消融 | NEST-01 | CLM-0601 | EV-NEST-01、EV-V2-NEST-FACTORIZE | 已定位原文，待签审。定位匹配 RF、输入和树预算的结构消融。 |
| LEG-C-114 | [[claims-index#2026-10-21：NestTor 已核验观点]] 第 2 项 · NestTor 确认集与后续采集、重分段 | NEST-02 | CLM-0602、CLM-0606 | EV-NEST-02、EV-V2-NEST-CONFIRM、EV-V2-NEST-LATER-RESEGMENT | 已定位原文，待签审。拆开确认结果与后来采集、重分段。 |
| LEG-C-115 | [[claims-index#2026-10-21：NestTor 已核验观点]] 第 3 项 · NestTor 的留一代理校准 | NEST-03 | CLM-0603 | EV-NEST-03、EV-V2-NEST-CALIBRATION | 已定位原文，待签审。按代理分别保留，包含 Trojan 的反向结果。 |
| LEG-C-116 | [[claims-index#2026-10-21：NestTor 已核验观点]] 第 4 项 · NestTor 的冻结工作点和阈值扫描 | NEST-04 | CLM-0604、CLM-0605 | EV-NEST-04、EV-V2-NEST-FROZEN-FPR、EV-V2-NEST-SWEPT-FPR | 已定位原文，待签审。拆开冻结 AND、扫阈值及各自分母。 |
| LEG-C-117 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 1 项 · HF-Transformer: A Non-Pretrained Encrypted Network Traffic Classification Model Based o… | C-20261026-03 | CLM-0202 | EV-20261026-03、EV-V2-HF-SUPERVISED | 已定位原文，待签审。由原摘要定位到六基准原表，限定可见包头和监督设置。 |
| LEG-C-118 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 2 项 · Synecdoche: Efficient and Accurate In-Network Traffic Classification via Direct Packet … | C-20261026-08 | — | EV-20261026-08 | 本轮范围外，保留历史。在线数据面匹配和部署速度。 |
| LEG-C-119 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 3 项 · A Unified Oversampling-Based Imbalance Processing Framework for Network Traffic Anomaly… | C-20261026-10 | — | EV-20261026-10 | 本轮范围外，保留历史。异常检测训练样本不平衡。 |
| LEG-C-120 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 4 项 · Behavioral Evidence-Based Hierarchical Decision Refinement for Encrypted Malicious Traf… | C-20261026-11 | CLM-0103 | EV-20261026-11 | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-121 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 5 项 · Drift-Aware Adaptive Website Fingerprinting 的摘要方法/结果主张需复核 | C-20261026-12 | CLM-0304 | EV-20261026-12、EV-V2-WF-DRIFT-AION | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-122 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 6 项 · Fooling Multi-Tab Browsing: Few-Shot Website Fingerprinting Attacks and Lightweight Obf… | C-20261026-13 | CLM-0304 | EV-20261026-13 | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-123 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 7 项 · GenETC: Dynamic Graph-enhanced Fine-tuning for Encrypted Traffic Classification 的摘要方法/结… | C-20261026-14 | CLM-0203 | EV-20261026-14、EV-V2-GENETC-PRETRAIN | 已定位原文，待签审。已核对保留图模块的预训练消融。 |
| LEG-C-124 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 8 项 · Is the Data Really Noisy? Rethinking Traffic Filtering for Encrypted Traffic Classifica… | C-20261026-16 | CLM-0003、CLM-0007、CLM-0103 | EV-20261026-16 | 候选或条件差异，待复核。另需核对分组单位、可见字段与标签来源。 |
| LEG-C-125 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 9 项 · RearView: Secure Two-Stage Malicious Traffic Identification with Dynamic Relationship A… | C-20261026-18 | CLM-0103 | EV-20261026-18 | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-126 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 10 项 · TridentDNS: Detecting Diverse DNS Tunnels Via Multidimensional Features 的摘要方法/结果主张需复核 | C-20261026-19 | CLM-0609 | EV-20261026-19 | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| LEG-C-127 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 11 项 · Two Heads Are Better Than One: Models-to-Model Learning for Encrypted Traffic Analysis … | C-20261026-24 | CLM-0403 | EV-20261026-24 | 候选或条件差异，待复核。需匹配视图定义、骨干、标注/训练预算及迁移测试。 |
| LEG-C-128 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 12 项 · Two Heads Are Not Better Than One: Continual Learning From Multiple Models for Encrypte… | C-20261026-25 | CLM-0403 | EV-20261026-25 | 候选或条件差异，待复核。需匹配视图定义、骨干、标注/训练预算及迁移测试。 |
| LEG-C-129 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 13 项 · Encrypted Network Traffic Classification Using Generative and Contrastive Self-Supervis… | C-20261026-28 | CLM-0204 | EV-20261026-28 | 候选或条件差异，待复核。单模型/任务结果，需核对同预算的去预训练对照与测试域。 |
| LEG-C-130 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 14 项 · Fighting the Enemy Within: Traffic Semantics-Driven Framework Against Noisy Labels for … | C-20261026-29 | CLM-0003、CLM-0007、CLM-0103 | EV-20261026-29 | 候选或条件差异，待复核。另需核对分组单位、可见字段与标签来源。 |
| LEG-C-131 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 15 项 · KAN-Vis: Efficient and Lightweight Visual Technique for Network Traffic Classification … | C-20261026-30 | CLM-0103 | EV-20261026-30 | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-132 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 16 项 · Making the Best of Both Worlds: Universal Perturbations for Live Black-Box Evasion Agai… | C-20261026-31 | — | EV-20261026-31 | 本轮范围外，保留历史。通用 IDS 扰动及鲁棒性评估。 |
| LEG-C-133 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 17 项 · SRViT: A Robust Online Encrypted Traffic Classification Based on Vision Transformer 的摘要… | C-20261026-33 | CLM-0103 | EV-20261026-33 | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-134 | [[claims-index#2026-10-26 自动提取候选主张（pending_review）]] 第 18 项 · When Pre-Training Meets Contrast Learning: Few-Shot Encrypted Traffic Classification Wi… | C-20261026-34 | CLM-0204 | EV-20261026-34 | 候选或条件差异，待复核。单模型/任务结果，需核对同预算的去预训练对照与测试域。 |
| LEG-C-135 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 1 项 · 2024-CCS-Detecting_tunneled_flooding_traffic_via_deep_semantic_analysis_of_packet_lengt… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-136 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 2 项 · 2024-CCS-Robust_and_reliable_early-stage_website_fingerprinting_attacks_via_spatial-tem… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-137 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 3 项 · 2024-CCS-Towards_fine-grained_webpage_fingerprinting_at_scale | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-138 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 4 项 · 2024-NDSS-Flow_Correlation_Attacks_on_Tor_Onion_Service_Sessions_with_Sliding_Subset_Sum | — | — | — | 本轮范围外，保留历史。双点流关联，区别于单点 ToP 识别。 |
| LEG-C-139 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 5 项 · 2024-NDSS-Low-quality_training_data_only__A_robust_framework_for_detecting_encrypted_ma… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-140 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 6 项 · 2024-NDSS-MirageFlow__A_New_Bandwidth_Inflation_Attack_on_Tor | — | — | — | 本轮范围外，保留历史。Tor 带宽测量。 |
| LEG-C-141 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 7 项 · 2024-S&P-Real-Time_Website_Fingerprinting_Defense_via_Traffic_Cluster_Anonymization | — | CLM-0302 | EV-V2-PALETTE-DEFINED | 已定位原文，待签审。定位 Palette 的闭集实验与重新训练条件。 |
| LEG-C-142 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 8 项 · 2024-USENIX-Fingerprinting_Obfuscated_Proxy_Traffic_with_Encapsulated_TLS_Handshakes | — | CLM-0609 | — | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| LEG-C-143 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 9 项 · 2025-CCS-Fingerprinting_Deep_Packet_Inspection_Devices_by_Their_Ambiguities | — | — | — | 本轮范围外，保留历史。DPI 分类设备测量。 |
| LEG-C-144 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 10 项 · 2025-CCS-GAPDiS__Gradient-Assisted_Perturbation_Design_via_Sequence_Editing_for_Website… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-145 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 11 项 · 2025-CCS-MM4flow__A_Pre-trained_Multi-modal_Model_for_Versatile_Network_Traffic_Analysis | — | CLM-0401 | EV-V2-MM4FLOW-MODAL | 已定位原文，待签审。定位 MM4flow Table 3 的单视图对照。 |
| LEG-C-146 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 12 项 · 2025-CCS-Swallow__A_Transfer-Robust_Website_Fingerprinting_Attack_via_Consistent_Featur… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-147 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 13 项 · 2025-CCS-Training_Robust_Classifiers_for_Classifying_Encrypted_Traffic_under_Dynamic_Ne… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-148 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 14 项 · 2025-CCS-Training_with_Only_1.0 ‰_Samples__Malicious_Traffic_Detection_via_Cross-Modali… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-149 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 15 项 · 2025-NDSS-SketchFeature__High-Quality_Per-Flow_Feature_Extractor_Towards_Security-Aware… | — | — | — | 本轮范围外，保留历史。流级特征抽取部署。 |
| LEG-C-150 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 16 项 · 2025-S&P-Countmamba__A_Generalized_Website_Fingerprinting_Attack_via_Coarse-Grained_Rep… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-151 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 17 项 · 2025-S&P-SoK_Decoding_the_Enigma_of_Encrypted_Network_Traffic_Classifiers | — | CLM-0001、CLM-0004 | EV-V2-SOK-CIPHERTEXT、EV-V2-SOK-CORPUS | 已定位原文，待签审。定位语料组成及内容变换实验。 |
| LEG-C-152 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 18 项 · 2025-S&P-TrafficFormer_An_Efficient_Pre-trained_Model_for_Traffic_Data | — | CLM-0502 | EV-V2-TRAFFICFORMER-OVERLAP | 已定位原文，待签审。定位重叠 bigram 的原文定义。 |
| LEG-C-153 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 19 项 · 2025-USENIX-Censorship_Evasion_with_Unidentified_Protocol_Generation | — | — | — | 本轮范围外，保留历史。协议生成和审查测量。 |
| LEG-C-154 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 20 项 · 2025-USENIX-CertTA__Certified_Robustness_Made_Practical_for_Learning-Based_Traffic_Anal… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-155 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 21 项 · 2026-NDSS-A_Hard-Label_Black-Box_Evasion_Attack_against_ML-based_Malicious_Traffic_Dete… | — | — | — | 本轮范围外，保留历史。通用 IDS 鲁棒性。 |
| LEG-C-156 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 22 项 · 2026-NDSS-Beyond_RTT__An_Adversarially_Robust_Two-Tiered_Approach_for_Residential_Proxy… | — | CLM-0609 | — | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| LEG-C-157 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 23 项 · 2026-NDSS-Cease_at_the_Ultimate_Goodness__Towards_Efficient_Website_Fingerprinting_Defe… | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-158 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 24 项 · 2026-NDSS-Enhancing_Website_Fingerprinting_Attacks_against_Traffic_Drift | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-159 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 25 项 · 2026-NDSS-Huma__Censorship_Circumvention_via_Web_Protocol_Tunneling_with_Deferred_Traff… | — | — | — | 本轮范围外，保留历史。审查规避承载，不提供 ToP 工作点。 |
| LEG-C-160 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 26 项 · 2026-USENIX-Motion_in_the_Clear__Reconstructing_VR_User_Behavior_from_Network_Traffic | — | — | — | 本轮范围外，保留历史。VR 上行加密组成，作为相邻测量记录。 |
| LEG-C-161 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 27 项 · 2026-USENIX-Towards_Practical_Few-shot_Multi-tab_Website_Fingerprinting | — | CLM-0304 | — | 候选或条件差异，待复核。目标站点、防御、基率或观测点与其他试验不同。 |
| LEG-C-162 | [[claims-index#2024–2026 四大安全顶会深度分析证据入口（待审核）]] 第 28 项 · 2026-USENIX-Tracegram__Framing_Trace-Level_Traffic_Analysis_with_Temporally-Aware_Multi… | — | CLM-0103 | — | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-163 | [[claims-index#2026-11-17　2026-COSINT-北邮时金桥 学术报告线索]] 第 1 项 · DHOR 给出最低基率标签下的 81.94% 精确率和 1.43×10⁻⁶ FPR | COSINT-01 | CLM-0607、CLM-0609 | EV-COSINT-01、EV-V2-COSINT-DHOR | 相邻任务，留待核验。报告页可定位，五分类与基率保留为相邻信号；完整配置和分母仍待复核。 |
| LEG-C-164 | [[claims-index#2026-11-17　2026-COSINT-北邮时金桥 学术报告线索]] 第 2 项 · 编码器、邻域判定与哈希设计均在 DHOR 消融中影响精确率 | COSINT-02 | CLM-0607、CLM-0609 | EV-COSINT-02、EV-V2-COSINT-DHOR | 相邻任务，留待核验。报告页可定位，五分类与基率保留为相邻信号；完整配置和分母仍待复核。 |
| LEG-C-165 | [[claims-index#2026-11-17　2026-COSINT-北邮时金桥 学术报告线索]] 第 3 项 · DHBCorr 在每侧 20,000 流时报告精确率 99.33%、TPR 84.85%、FPR 2.9×10⁻⁷ | COSINT-03 | CLM-0608、CLM-0609 | EV-COSINT-03、EV-V2-COSINT-DHBCORR | 相邻任务，留待核验。报告页可定位，双侧候选与资源口径单列，未与单点检测相比较。 |
| LEG-C-166 | [[claims-index#2026-11-17　2026-COSINT-北邮时金桥 学术报告线索]] 第 4 项 · DHBCorr 以每侧 23,312 流支持 5 秒约 5.4×10⁸ 候选对 | COSINT-04 | CLM-0608、CLM-0609 | EV-COSINT-04、EV-V2-COSINT-DHBCORR | 相邻任务，留待核验。报告页可定位，双侧候选与资源口径单列，未与单点检测相比较。 |
| LEG-C-167 | [[claims-index#2026-11-18　批次证据候选]] 第 1 项 · 流级自监督训练与标签校准是两个条件。GraphIDS 用验证标签选模型和阈值，在 CIC-v2 的 PR-AUC 均值低于 Anomal-E。 | KB-20261118-GRAPH-CAL | CLM-0104、CLM-0103 | EV-20261118-GRAPH-CAL、EV-V2-GRAPHIDS-VERSIONS | 已定位原文，待签审。已从 Table 3 核对同底层语料不同版本和标签校准。 |
| LEG-C-168 | [[claims-index#2026-11-18　批次证据候选]] 第 2 项 · SmartNIC 分析速度和完成量随新流负载变化。报告需并列前缀、NFPS、P99 与完成量。 | KB-20261118-NEPCO-COST | — | EV-20261118-NEPCO-COST | 本轮范围外，保留历史。SmartNIC 通量和观察成本。 |
| LEG-C-169 | [[claims-index#2026-11-18　批次证据候选]] 第 3 项 · 局部字节重要性和地址依赖可共存，归因覆盖多个协议头字段。 | KB-20261118-NEPCO-BYTE | CLM-0504 | EV-20261118-NEPCO-BYTE | 候选或条件差异，待复核。需控制预处理、字段可见性及有效字节/Token 预算。 |
| LEG-C-170 | [[claims-index#2026-11-18　批次证据候选]] 第 4 项 · 严重正常性漂移可使以紧密良性为参照的距离模型退化。少量可信的目标域良性用于再锚定时可以部分改善。 | KB-20261118-HAD-DRIFT | CLM-0609 | EV-20261118-HAD-DRIFT | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| LEG-C-171 | [[claims-index#2026-11-18　批次证据候选]] 第 5 项 · 底层链路变化改变 Tor RTT。加权 100 中继部署仿真中约 40.5% 电路平均缩短 21.8 ms。 | KB-20261118-SAT-RTT | CLM-0609 | EV-20261118-SAT-RTT | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| LEG-C-172 | [[claims-index#2026-11-18　批次证据候选]] 第 6 项 · 构造的明密文混合币种数据中，移除包内容后 macro F1 下降，但幅度不能归给密文信号。 | KB-20261118-CRYPTO-MODAL | CLM-0005、CLM-0403 | EV-20261118-CRYPTO-MODAL、EV-V2-CRYPTO-CONTENT | 已定位原文，待签审。已核对混合语料及内容消融。纯密文归因待单独试验。 |
| LEG-C-173 | [[claims-index#2026-11-18　批次证据候选]] 第 7 项 · MPA-LLM 延续 ARI-LLM 的粗到细重构，GÉANT 插补 NRMSE 改善；WS-DREAM 多列误差仍由 ARI-LLM 占优。 | KB-20261118-MPA-EXT | — | EV-20261118-MPA-EXT | 本轮范围外，保留历史。流量矩阵重构扩展。 |
| LEG-C-174 | [[claims-index#2026-11-18　批次证据候选]] 第 8 项 · 对共享计数器的查询校正可改善流包数误差，写入保持原 sketch，读侧新增计算。 | KB-20261118-PSML-READ | — | EV-20261118-PSML-READ | 本轮范围外，保留历史。遥测查询校正。 |
| LEG-C-175 | [[claims-index#2026-11-18　批次证据候选]] 第 9 项 · 动态更新遥测指标可降低部分数据上的上报比例，并承担更多每快照处理成本。 | KB-20261118-SEDMS-UPDATE | — | EV-20261118-SEDMS-UPDATE | 本轮范围外，保留历史。遥测更新开销。 |
| LEG-C-176 | [[claims-index#2026-11-18　批次证据候选]] 第 10 项 · 将输入与验证行为的来源分开能减少直接循环验证；样本级未捕获仍会造成语料覆盖偏差。 | KB-20261118-T2T-COVER | — | EV-20261118-T2T-COVER | 本轮范围外，保留历史。威胁行为与合成语料覆盖。 |
| LEG-C-177 | [[claims-index#2026-11-18　COSINT 联动待验证]] 第 1 项 · 困难背景的得分分布和工作点 | EV-20261118-COSINT-NORMAL-REF | CLM-0609 | EV-20261118-COSINT-NORMAL-REF | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| LEG-C-178 | [[claims-index#2026-11-18　COSINT 联动待验证]] 第 2 项 · 底层路由及跨点匹配条件 | EV-20261118-COSINT-TIMING | CLM-0609 | EV-20261118-COSINT-TIMING | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| LEG-C-179 | [[claims-index#2026-11-18　COSINT 联动待验证]] 第 3 项 · 摘要、编码和查询匹配的成本 | EV-20261118-COSINT-COST | CLM-0609 | EV-20261118-COSINT-COST | 候选或条件差异，待复核。观测点、决策单位、负类或阈值协议与冻结 ToP 工作点不同。 |
| LEG-C-180 | [[claims-index#2026-11-18　深读证据补充]] 第 1 项 · 不同家族的约束提取 F1 不同，整体为 81.0%。行为真值覆盖还需按独立参照衡量。 | EV-20261118-L3-T2T-COVERAGE-F1 | — | EV-20261118-L3-T2T-COVERAGE-F1 | 本轮范围外，保留历史。威胁行为真值覆盖。 |
| LEG-C-181 | [[claims-index#2026-11-18　深读证据补充]] 第 2 项 · 上下文变化后的召回受数据和决策单位影响。OpTC2 对 Flash 与 Threatrace 显示零变化。 | EV-20261118-L3-CONTORTER-UNIT | CLM-0103 | EV-20261118-L3-CONTORTER-UNIT | 候选或条件差异，待复核。未匹配输入、决策结构、划分或训练预算。 |
| LEG-C-182 | [[claims-index#2026-11-18　深读证据补充]] 第 3 项 · 实测每个观测点使用 2,000 次测量。CenRL 从更大的候选池选点，发现量包含候选范围与调度的共同影响。 | EV-20261118-L3-CENRL-POOL | — | EV-20261118-L3-CENRL-POOL | 本轮范围外，保留历史。主动测量候选池与部署评估。 |
| LEG-C-183 | [[claims-index#2026-11-18　深读证据补充]] 第 4 项 · 逻辑缓存占用与 RSS 压力不同。局部资源测量不能直接给出按共识权重计算的网络影响。 | EV-20261118-L3-DESC-RESOURCE | — | EV-20261118-L3-DESC-RESOURCE | 本轮范围外，保留历史。Tor 网络资源测量，不测试 ToP 分类。 |
| LEG-C-184 | [[claims-index#2026-11-18　深读证据补充]] 第 5 项 · 查询结构的寄存器计数需要结合活跃键和窗口语义才能用来核算部署资源。 | EV-20261118-L3-SIR-SCALE | — | EV-20261118-L3-SIR-SCALE | 本轮范围外，保留历史。流式遥测窗口资源。 |
| LEG-C-185 | [[claims-index#2026-11-18　深读证据补充]] 第 6 项 · 统一架构下，阶段参数和联合训练对各任务贡献不同。Abilene 联合训练插补 NMAE 变差、预测 NMAE 改善。 | EV-20261118-L3-MPA-JOINT | — | EV-20261118-L3-MPA-JOINT | 本轮范围外，保留历史。流量矩阵任务联合训练。 |

## 历史矛盾

| 迁移编号 | 原位置及题意 | 拟议 relation_type | 新命题 ID | 关联证据 | 处置依据 |
| --- | --- | --- | --- | --- | --- |
| LEG-R-001 | [[contradictions#矛盾记录]] 第 1 项 · 加密 payload 是否可学习 | method_difference | CLM-0001、CLM-0003、CLM-0006、CLM-0007 | EV-V2-SOK-CIPHERTEXT、EV-V2-SWEET-SPLIT、EV-V2-IMC-REPLICATION | 输入分离与统计假设有差异，尚缺同设置正反结果。 |
| LEG-R-002 | [[contradictions#矛盾记录]] 第 2 项 · 深度学习 vs 传统 ML 在加密流量分类中的优劣 | method_difference | CLM-0003、CLM-0101、CLM-0103 | EV-V2-SWEET-SPLIT、EV-V2-SWEET-BASELINES | 表示、训练协议、数据构成与输入共同改变。 |
| LEG-R-003 | [[contradictions#矛盾记录]] 第 3 项 · WF 攻击是否已攻破现有防御 | temporal_evolution | CLM-0301、CLM-0302、CLM-0304 | EV-V2-DF-DEFENSES、EV-V2-PALETTE-DEFINED | 不同代际防御和数据，各自闭集结果可追原表。 |
| LEG-R-004 | [[contradictions#矛盾记录]] 第 4 项 · 数据集划分方式对结论的影响 | method_difference | CLM-0003 | EV-V2-SWEET-SPLIT | 同一复核中用匹配冻结条件比较两种划分。 |
| LEG-R-005 | [[contradictions#矛盾记录]] 第 5 项 · 表征学习 vs 浅层模型的实际价值 | scope_difference | CLM-0101、CLM-0103、CLM-0401 | EV-V2-SWEET-BASELINES、EV-V2-MM4FLOW-MODAL | 任务、视图与预算不同。 |
| LEG-R-006 | [[contradictions#矛盾记录]] 第 6 项 · 评估指标的选择与结论可靠性 | method_difference | CLM-0103 | — | 宏微聚合评估口径不同；需要相同预测和分母。 |
| LEG-R-007 | [[contradictions#矛盾记录]] 第 7 项 · 流量表示中信息来源的本质 | scope_difference | CLM-0001、CLM-0003、CLM-0007 | EV-V2-SOK-CIPHERTEXT、EV-V2-SWEET-SPLIT | 纯密文对照与含可见字段的字节输入分开。 |
| LEG-R-008 | [[contradictions#矛盾记录]] 第 8 项 · WF 防御的鲁棒性与可迁移攻击 | method_difference | CLM-0302、CLM-0304 | EV-V2-PALETTE-DEFINED | 是否重训、数据和评估条件待匹配。 |
| LEG-R-009 | [[contradictions#矛盾记录]] 第 9 项 · 预训练是否必要 | scope_difference | CLM-0201、CLM-0202、CLM-0204 | EV-V2-ETBERT-PRETRAIN、EV-V2-HF-SUPERVISED | 模型、输入和任务不同，旧“必要性”拆为受控命题。 |
| LEG-R-010 | [[contradictions#矛盾记录]] 第 10 项 · MoE vs SSM vs Transformer 架构选择之争 | method_difference | CLM-0103、CLM-0204、CLM-0403 | — | 骨干与输入、预训练、训练预算混杂。 |
| LEG-R-011 | [[contradictions#矛盾记录]] 第 11 项 · 零样本 vs 少样本 vs 全量训练在 WF 中的可行性 | scope_difference | CLM-0304 | — | 目标标签权限与监控集合分别建条件。 |
| LEG-R-012 | [[contradictions#矛盾记录]] 第 12 项 · 捷径学习风险与 DL 分类器高准确率的可信度 | method_difference | CLM-0003、CLM-0007、CLM-0103 | EV-V2-SWEET-SPLIT | 不同的输入遮蔽、漏划与数据组成应各自核对。 |
| LEG-R-013 | [[contradictions#矛盾记录]] 第 13 项 · 预训练必要性的进一步证据 | scope_difference | CLM-0201、CLM-0203、CLM-0204 | EV-V2-ETBERT-PRETRAIN、EV-V2-GENETC-PRETRAIN | 具体预训练消融和必要性是不同尺度的判断。 |
| LEG-R-014 | [[contradictions#矛盾记录]] 第 14 项 · 多模态融合的收益与代价 | scope_difference | CLM-0401、CLM-0402、CLM-0403 | EV-V2-MM4FLOW-MODAL、EV-V2-BPFDAG-ABLATION | 视图、融合代价和任务不同。 |
| LEG-R-015 | [[contradictions#矛盾记录]] 第 15 项 · 加密流量三类侧信道特征（包长/方向/时序）的效用排序 | unresolved | CLM-0602、CLM-0401、CLM-0403 | EV-V2-NEST-CONFIRM、EV-V2-MM4FLOW-MODAL | 缺三种侧信道同输入、同任务的受控排序。 |
| LEG-R-016 | [[contradictions#矛盾记录]] 第 16 项 · 真实世界 WF 攻击有效性是否成立 | scope_difference | CLM-0303、CLM-0304 | EV-V2-ONLINE-WF | 不同站点选择、监控负类、数据来源和指标。 |
| LEG-R-017 | [[contradictions#矛盾记录]] 第 17 项 · 净化/恢复攻击对 WF 防御的可恢复性是否普适 | method_difference | CLM-0302、CLM-0304 | EV-V2-PALETTE-DEFINED | 各防御与观测条件不同，适用性待受控验证。 |
| LEG-R-018 | [[contradictions#2026-10-21：NestTor 对浅层/深度比较的条件澄清]] 第 1 项 · ToP 上浅层分解系统优于字节/序列深模型，是否证明深度表征无效？ | method_difference | CLM-0102、CLM-0601 | EV-V2-NEST-GATE-CONTROL、EV-V2-NEST-FACTORIZE | 相同门控和端到端协议分开；匹配 RF 是独立对照问题。 |
| LEG-R-019 | [[contradictions#2026-10-26 待核验关系（不改变既有 verdict）]] 第 1 项 · 预训练收益 vs 非预训练路线 | scope_difference | CLM-0201、CLM-0202、CLM-0203、CLM-0204 | EV-V2-ETBERT-PRETRAIN、EV-V2-HF-SUPERVISED、EV-V2-GENETC-PRETRAIN | HF 与 GenETC 各自可读原表，不能直接对照初始化。 |
| LEG-R-020 | [[contradictions#2026-10-26 待核验关系（不改变既有 verdict）]] 第 2 项 · 流量过滤/噪声处理是否总能提升分类 | method_difference | CLM-0003、CLM-0103 | EV-V2-SWEET-SPLIT | 噪声定义、过滤、标签和数据划分不同。 |
| LEG-R-021 | [[contradictions#2026-10-26 待核验关系（不改变既有 verdict）]] 第 3 项 · WF 漂移适应与少样本防御的边界 | scope_difference | CLM-0304 | — | 漂移与多标签页防御需相同站点、采集域和标签权限。 |
| LEG-R-022 | [[contradictions#2026-11-18　待审核的条件差异]] 第 1 项 · GraphIDS / Anomal-E | scope_difference | CLM-0104、CLM-0103 | EV-V2-GRAPHIDS-VERSIONS | CIC v2/v3 底层语料共享，特征与聚合变化。 |
| LEG-R-023 | [[contradictions#2026-11-18　待审核的条件差异]] 第 2 项 · HAD / COSINT 汇报 | scope_difference | CLM-0607、CLM-0609 | EV-V2-COSINT-DHOR | 负类参照、标签与漂移设置不同。 |
| LEG-R-024 | [[contradictions#2026-11-18　待审核的条件差异]] 第 3 项 · CryptoFormer / 预训练基线 | scope_difference | CLM-0005、CLM-0103、CLM-0403 | EV-V2-CRYPTO-CONTENT | 窄任务明密文混合对照与通用表示不同。 |
| LEG-R-025 | [[contradictions#2026-11-18　待审核的条件差异]] 第 4 项 · MPA-LLM / ARI-LLM | scope_difference | — | — | 流量矩阵任务为既有相邻领域，按扩展稿保留。 |
| LEG-R-026 | [[contradictions#2026-11-18　深读证据补充]] 第 1 项 · CenRL 摘要报实测平均约 2.5 倍，§6.2 报 2.75 倍。引用整体增幅前应先核对汇总分母。等预算下不同候选范围的… | method_difference | — | — | 主动测量中汇总分母和候选池不同，留于原议题。 |

## 前沿历史判断

| 迁移编号 | 原位置 | 旧状态 | 新命题 ID | 关联证据 | 处置依据 |
| --- | --- | --- | --- | --- | --- |
| LEG-F-001 | [[multimodal-fusion-strategy#历史研究记录]] | converging | CLM-0005、CLM-0401、CLM-0402、CLM-0403 | EV-V2-CRYPTO-CONTENT、EV-V2-MM4FLOW-MODAL、EV-V2-BPFDAG-ABLATION | 整页证据链和历史判断已留存。保留同任务视图消融，匹配多模态设定后才比较。 |
| LEG-F-002 | [[payload-learnability#历史研究记录]] | converging | CLM-0001、CLM-0002、CLM-0003、CLM-0004、CLM-0005、CLM-0006、CLM-0007、CLM-0602 | EV-V2-SOK-CIPHERTEXT、EV-V2-LEAKAGE-THEOREM、EV-V2-SWEET-SPLIT、EV-V2-SOK-CORPUS、EV-V2-CRYPTO-CONTENT、EV-V2-IMC-REPLICATION、EV-V2-NEST-CONFIRM | 整页证据链和历史判断已留存。拆开密文实验、定理、外层元数据和划分。 |
| LEG-F-003 | [[pretraining-necessity#历史研究记录]] | diverging | CLM-0201、CLM-0202、CLM-0203、CLM-0204 | EV-V2-ETBERT-PRETRAIN、EV-V2-HF-SUPERVISED、EV-V2-GENETC-PRETRAIN | 整页证据链和历史判断已留存。保留原模型消融，另列匹配预算的跨域缺口。 |
| LEG-F-004 | [[representation-vs-shallow#历史研究记录]] | diverging | CLM-0003、CLM-0101、CLM-0102、CLM-0103、CLM-0104、CLM-0401 | EV-V2-SWEET-SPLIT、EV-V2-SWEET-BASELINES、EV-V2-NEST-GATE-CONTROL、EV-V2-GRAPHIDS-VERSIONS、EV-V2-MM4FLOW-MODAL | 整页证据链和历史判断已留存。重核使用不同输入、任务和门控的条件差异。 |
| LEG-F-005 | [[tokenization-optimal#历史研究记录]] | diverging | CLM-0202、CLM-0501、CLM-0502、CLM-0503、CLM-0504 | EV-V2-HF-SUPERVISED、EV-V2-MET-EMBEDDING、EV-V2-TRAFFICFORMER-OVERLAP、EV-V2-PACKETLOOM-PREPROCESSING | 整页证据链和历史判断已留存。区别预处理、字段可见性、Token 定义与预算。 |
| LEG-F-006 | [[tor-over-proxy-low-fpr-detection#历史研究记录]] | diverging | CLM-0102、CLM-0601、CLM-0602、CLM-0603、CLM-0604、CLM-0605、CLM-0606、CLM-0607、CLM-0608、CLM-0609 | EV-V2-NEST-GATE-CONTROL、EV-V2-NEST-FACTORIZE、EV-V2-NEST-CONFIRM、EV-V2-NEST-CALIBRATION、EV-V2-NEST-FROZEN-FPR、EV-V2-NEST-SWEPT-FPR、EV-V2-NEST-LATER-RESEGMENT、EV-V2-COSINT-DHOR、EV-V2-COSINT-DHBCORR | 整页证据链和历史判断已留存。隔离固定工作点、扫阈值、流/窗/流对和各自分母。 |
| LEG-F-007 | [[wf-attack-defense-limit#历史研究记录]] | diverging | CLM-0301、CLM-0302、CLM-0303、CLM-0304 | EV-V2-DF-DEFENSES、EV-V2-PALETTE-DEFINED、EV-V2-ONLINE-WF | 整页证据链和历史判断已留存。按防御谱系、目标集合和训练访问条件复核。 |

---
type: survey
topic: "Malicious Traffic Detection"
status: evolving
created: "2026-05-27"
updated: "2026-08-17"
---

# 恶意流量检测综述 (Survey: Malicious Traffic Detection)

## 1. 综述范围

覆盖从网络流量中识别恶意行为（如恶意软件通信、C&C 连接、DDoS、数据泄露、入侵行为）的方法，包括基于频域分析、对比学习、多模态融合、大语言模型等技术路线。重点关注加密环境下的恶意流量检测和少样本/零样本场景。

## 2. 问题背景

随着 TLS 1.3、QUIC 等加密协议的普及，传统 Deep Packet Inspection (DPI) 对加密载荷失效，恶意流量检测面临重大挑战。攻击者利用加密隧道隐藏恶意通信，同时使用流量混淆技术规避检测。标注恶意流量样本获取困难，且新型攻击不断涌现，监督学习方法难以覆盖所有攻击类型。

核心挑战包括：(1) 加密后载荷不可见；(2) 对抗性 evasion 攻击；(3) 标注数据稀缺和类别不平衡；(4) 概念漂移；(5) 高速网络实时性要求。

## 3. 技术分类

### 3.1 基于频域分析的方法

- **Whisper**：将流量转换为频域表示（DFT），利用频域特征的稳定性和区分性
  - 频域特征具有时移不变性和可加性，在噪声和 packet loss 下保持鲁棒性
  - 仅使用正常流量样本训练 One-Class SVM
  - AUC 0.93-0.999，吞吐量 13.22 Gbps
  - 论文笔记：`[[2021-CCS-Realtime_Robust_Malicious_Traffic_Detection_via_Frequency_Domain_Analysis]]`

### 3.2 基于对比学习的方法

- **SmartDetector**：Semantic Attribute Matrix (SAM) + 对比学习框架
  - SAM 表示流量的语义属性，比原始特征更具区分性
  - InfoNCE loss 学习语义级表示
  - 在对抗逃举场景（evasion attacks）下 F1 > 93%
  - 论文笔记：`[[2025-TIFS-Robust_Detection_of_Malicious_Encrypted_Traffic_via_Contrastive_Learning]]`

- **LitCVit**：轻量自监督对比视觉 Transformer（Nisa et al., TIFS 2026）
  - 卷积 patchify stem + 字节/包/流三级窗口化低秩因子化注意力（wf-Attention）+ ntXent 对比预训练，捕获跨流语义与行为模式
  - 6 个真实数据集平均准确率 98.10%、F1 98.08%，以 0.321M 参数实现约 8.7 倍于最强自监督 baseline 的推理加速，面向边缘/IoT 部署
  - 论文笔记：`[[2026-TIFS-LitCVit__A_Lightweight_Self-Supervised_Contrastive_Vision_Transformer_for_Encrypted_Malicious_Traffic_Detection]]`

### 3.3 基于多模态融合的方法

- **tFusion**：跨模态特征融合 + 拓扑驱动的对比学习
  - 三模态：packet-level、flow-level、host-level 特征
  - Crossmodal Attention 融合不同粒度特征
  - 拓扑驱动对比学习利用网络拓扑结构减少标注依赖
  - 仅需 0.1% 标注数据达 99.82% 准确率
  - 论文笔记：`[[2025-CCS-Training_with_Only_1.0 ‰_Samples__Malicious_Traffic_Detection_via_Cross-Modality_Feature_Fusion]]`

### 3.4 基于大语言模型的方法

- **MET-LLM**：利用大语言模型（Deepseek）进行恶意加密流量检测
  - 领域特定 BPE 编码器：适配流量数据的字节分布，而非使用通用 NLP tokenizer
  - DATA adapter：桥接流量表示与语言模型的语义空间
  - F1 > 0.96
  - 论文笔记：`[[2025-ESA-MET-LLM__Enhancing_Large_Language_Models_for_Malicious_Encrypted_Traffic_Detection]]`

### 3.5 基于 Transformer 特征提取的方法

- **Session-Transformer**：修改 Transformer encoder + DNN 分类器的加密恶意流量检测方法（Wei et al., JIoT 2025）
  - 核心思想：TLS 流量具有请求-响应模型结构，payload 之间存在长度关联、内容关联和时序关联
  - 修改 Transformer encoder 自动提取上下文关联和时序特征，无需解密
  - 使用 DNN 作为分类器进行二分类（恶意 vs 正常）和多分类（恶意软件家族）
  - DataCon2020 召回率 98.34%，CIC-AndMal-2017 精确率 93.54%
  - 局限：仅使用统计特征（ST Feature），未直接处理原始字节
  - 论文笔记：`[[2025-JIoT-A_Detection_Method_for_Malware_Communication_Traffic_via_Encrypted_Traffic_Analysis]]`

### 3.6 基于预训练基础模型的方法

- **ET-BERT**：BERT 预训练 + 微调，ISCX-VPN F1 98.9%
- **YaTC**：MAE 预训练 + 分层注意力，所有数据集 SOTA
- **NetMamba+**：Mamba + 多模态，1.7x 推理加速

### 3.7 基于开放集识别的方法

- **FEC-OSL**：能量模型 + CViT + TAGCN + 自适应深度聚类
  - 端到端开放集半监督学习
  - 99.60% AC
  - 论文笔记：`[[2026-TIFS-End-to-End_Open-Set_Semi-Supervised_Learning_for_Fine-Grained_Encrypted_Traffic_Classification]]`

### 3.8 基于多维异构特征的方法

- **MTBD**：融合 flow-level、host-level、packet-level 三维异构特征
  - Burst filtering 过滤噪声
  - 投票机制整合多粒度检测结果
  - P/R/F1 均达 99%
  - 论文笔记：`[[2022-HPCC-MTBD_HTTPS_Tunnel_Detection_Based_on_Multi-dimension_Traffic_Behaviors_Decision]]`

### 3.9 基于时序图学习的早期检测

- **DawnGuard**：多流时序图学习早期检测（Jia et al., TIFS 2026）
  - 核心思想：时间包密度分析驱动的自调整数据增强聚焦高判别性的早期交互阶段，在主-服务器二分时序图上做时序图学习提取多流关联特征（MGF），ViT 检测器分类
  - 仅用完整流量前 20%（loading ratio）即达平均 F1 95.11%（较 SOTA 高 8.7%），在 48:1 极端不平衡（F1 92.9%）和未见恶意软件（F1 91.34%）场景下保持领先
  - 论文笔记：`[[2026-TIFS-Early-Stage_Detection_of_Encrypted_Malware_Traffic_via_Multi-Flow_Temporal_Graph_Learning]]`

### 3.10 基于不确定性感知融合的方法

- **TrustWI**：不确定性感知多视图融合（Zhong et al., TDSC 2026）
  - 核心思想：以长程扩散传播（View-L）、传播后结构增强（View-S）与伪视图交互（View-P）三个互补视图恢复弱信息（破碎图结构、不完整特征、稀缺标注）下的加密流量信号，证据深度学习 + Dempster-Shafer 规则做视图级与全局级不确定性感知融合
  - 弱信息场景三数据集 AUC 93.72%/87.75%/97.37%，极端信息约束下将 SOTA AUC 从 85.45% 提升至 89.57%（DoHBrw）
  - 论文笔记：`[[2026-TDSC-Shattering_Weak_Facades__Trustworthy_Detection_of_Encrypted_Malicious_Traffic_via_Uncertainty-Aware_Fusion]]`

### 3.11 基于知识蒸馏的零正样本异常检测

- **ConMD**：上下文掩码知识蒸馏（Lian et al., TIFS 2026）
  - 核心思想：以 ImageNet 预训练 WideResNet50（经无关数据集微调）为教师、局部-全局窗口注意力学生骨干 + 上下文增强包级掩码蒸馏，摆脱重建范式的"identical shortcut"问题；推理时融合掩码/非掩码双分支多视图异常打分
  - 仅用正常流量训练（零正样本），DataCon2020/CIC-IDS2017/USTC-TFC2016 上 AUC 86.03%/94.43%/99.97%，相对最强 baseline 分别提升 2.8%/5.1%
  - 论文笔记：`[[2026-TIFS-Contextual_Masking_Distillation_for_Network_Traffic_Anomaly_Detection]]`

### 3.12 基于上下文感知流嵌入的方法

- **FlowXpert**：上下文感知流嵌入（Zha et al., TMC 2026）
  - 核心思想：设计 FlowVision 特征提取工具（丢弃时间/长度类稀疏特征、补充源主机上下文特征）解决流特征稀疏阻碍收敛问题，DBSCAN 伪标签 + 对比学习在 2% 下采样数据上训练流嵌入
  - 在 MAWI/CICIDS-2017/UNSW-NB15 上恶意流量检测优于 Kitsune/HyperVision/ETBert 等 SOTA，端到端延迟 <30µs 可实时部署
  - 论文笔记：`[[2026-TMC-FlowXpert__Context-Aware_Flow_Embedding_for_Enhanced_Traffic_Detection_in_IoT_Network]]`

### 3.13 基于网内检测的方法

- **Proteus**：网内决策树恶意流量检测（Zhu et al., WWW 2026）
  - 核心思想：利用"决策树前 60% 层即可达 >90% 精度"的边际贡献递减观察，将决策树异构切分为 1 棵关键子树 + 若干普通子树，用两阶段 MILP 优化部署到可编程交换机，并在资源变化时在线调优
  - 12.8 Tbps 交换机测试床：分类精度从 67.8% 提升到 78.8%，资源占用最多降低 82.8%，时延最多降低 74.5%
  - 论文笔记：`[[2026-WWW-Proteus__Towards_Accurate_and_Low-overhead_In_Network_Malicious_Traffic_Detection]]`

### 3.14 基于网内特征提取的方法

- **SuperFE**：可扩展灵活的特征提取器（Zhang et al., EuroSys 2025）
  - 核心思想："可编程交换机批处理 + SmartNIC 流式计算"分工架构，配用户友好策略接口（groupby/filter/map/reduce 等）与多粒度分组包向量（MGPV）缓存，为 ML 流量分析应用提供在线特征提取服务
  - 10 个 SOTA 流量分析应用的既有特征提取器仅用 9-101 行策略代码重写，即可从多 100Gbps 原始流量中在线提取特征，吞吐量比软件实现高近两个数量级且检测精度几乎无损
  - 论文笔记：`[[2025-EuroSys-SuperFE__A_Scalable_and_Flexible_Feature_Extractor_for_ML-based_Traffic_Analysis_Applications]]`

- **SketchFeature**：数据平面逐流特征提取（Kim et al., NDSS 2025）
  - 核心思想：首个在可编程交换机数据平面实现 HAF（高分辨率/全流/全范围）三阶逐流特征（IPD/PS 分布）提取的 sketch 方案，"sketch 虚拟化 + 幻影解码 + Bloom filter 成员测试"在 6 MB 内存内以线速完成全流分布测量
  - 系统论证 FlowLens/NetWarden 类"症状检测器"方案存在数据面规避与控制面淹没两类攻击面，端到端检测性能逼近"完美测量"上界
  - 论文笔记：`[[2025-NDSS-SketchFeature__High-Quality_Per-Flow_Feature_Extractor_Towards_Security-Aware_Data_Plane]]`

### 3.15 基于仿真的多环境统一检测框架

- **M-En**：仿真驱动的多环境统一检测框架（Rustam & Jurcut, Computer Networks 2026）
  - 核心思想：用 PLS canonical 交叉分解融合 IoT（IoT23）与传统 IP（CICDDoS2019）流量构建多环境（M-En）数据集，RNN-LSTM 迁移学习提取 32 维时序特征，客户端-服务器批量决策架构（Ubuntu + TCP + pickle）验证部署可行性
  - Logistic Regression 以最低资源开销成为最佳部署模型（离线准确率 0.98、仿真网关评估 0.71）
  - 论文笔记：`[[2026-JCN-A_simulation-based_unified_framework_for_real-time_malicious_traffic_detection_in_multi-environment_networks]]`

## 4. 发展脉络

| 时间 | 里程碑 | 代表工作 | 核心贡献 |
|------|--------|----------|----------|
| 2016-2018 | 传统 ML 方法 | AppScanner, CUMUL | 手工特征 + 传统分类器 |
| 2018-2020 | 深度学习方法 | DF, FS-Net | CNN/LSTM 自动特征学习 |
| 2021 | 频域分析 | Whisper | DFT 特征，13.22 Gbps 吞吐量 |
| 2022 | 预训练范式 | ET-BERT | BERT 预训练加密流量表示 |
| 2025 | Transformer 特征提取 | Session-Transformer | 修改 Transformer encoder + DNN 检测加密恶意流量 |
| 2025 | 对比学习 + 多模态 | SmartDetector, tFusion | 对抗鲁棒，0.1% 标注数据 |
| 2025 | 大语言模型 | MET-LLM | LLM 适配恶意流量检测 |
| 2026 | 开放集识别 | FEC-OSL, UT-PAB | 未知攻击类型泛化 |
| 2025 | 网内特征提取 | SuperFE, SketchFeature | 可编程交换机/SmartNIC 在线特征提取，支撑数据平面安全应用 |
| 2026 | 图学习 + 不确定性 + 蒸馏 + 网内检测 | DawnGuard, TrustWI, ConMD, LitCVit, Proteus | 早期时序图检测；不确定性感知融合；零正样本蒸馏；轻量对比 ViT；网内决策树部署 |
| 2026 | 上下文嵌入 + 多环境仿真 | FlowXpert, M-En | 上下文感知流嵌入；多环境统一检测框架 |

## 5. 代表论文列表

- Whisper (CCS 2021)：频域分析，AUC 0.93-0.999，13.22 Gbps — `[[2021-CCS-Realtime_Robust_Malicious_Traffic_Detection_via_Frequency_Domain_Analysis]]`
- SmartDetector (TIFS 2025)：SAM + 对比学习，F1 > 93% under evasion — `[[2025-TIFS-Robust_Detection_of_Malicious_Encrypted_Traffic_via_Contrastive_Learning]]`
- tFusion (CCS 2025)：跨模态融合 + 拓扑对比学习，0.1% 数据 99.82% — `[[2025-CCS-Training_with_Only_1.0 ‰_Samples__Malicious_Traffic_Detection_via_Cross-Modality_Feature_Fusion]]`
- MET-LLM (ESA 2025)：大语言模型辅助检测，F1 > 0.96 — `[[2025-ESA-MET-LLM__Enhancing_Large_Language_Models_for_Malicious_Encrypted_Traffic_Detection]]`
- FEC-OSL (TIFS 2026)：开放集半监督学习，99.60% AC — `[[2026-TIFS-End-to-End_Open-Set_Semi-Supervised_Learning_for_Fine-Grained_Encrypted_Traffic_Classification]]`
- UT-PAB (JCN 2026)：BERT 预训练 + 原型对齐，H-score 94.77 — `[[2026-JCN-A_prototypical_alignment_approach_to_unknown_traffic_classification_using_BERT]]`
- ET-BERT (WWW 2022)：BERT 预训练加密流量表示 — `[[2022-WWW-ET-BERT__A_Contextualized_Datagram_Representation_with_Pre-training_Transformers_for_Encrypted_Traffic_Classification]]`
- YaTC (AAAI 2023)：MAE 预训练 + 分层注意力 — `[[2023-AAAI-Yet_Another_Traffic_Classifier_a_Masked_Autoencoder_Based_Traffic_Transformer_With_Multi-level_Flow_Representation]]`
- MTBD (HPCC 2022)：三维异构特征 + 投票 — `[[2022-HPCC-MTBD_HTTPS_Tunnel_Detection_Based_on_Multi-dimension_Traffic_Behaviors_Decision]]`
- Session-Transformer (JIoT 2025)：修改 Transformer + DNN 检测加密恶意流量，DataCon2020 召回率 98.34% — `[[2025-JIoT-A_Detection_Method_for_Malware_Communication_Traffic_via_Encrypted_Traffic_Analysis]]`
- LitCVit (TIFS 2026)：轻量自监督对比 ViT 检测加密恶意流量，0.321M 参数 98.10% 准确率 — `[[2026-TIFS-LitCVit__A_Lightweight_Self-Supervised_Contrastive_Vision_Transformer_for_Encrypted_Malicious_Traffic_Detection]]`
- DawnGuard (TIFS 2026)：多流时序图学习的早期加密恶意流量检测，前 20% 流量 F1 95.11% — `[[2026-TIFS-Early-Stage_Detection_of_Encrypted_Malware_Traffic_via_Multi-Flow_Temporal_Graph_Learning]]`
- TrustWI (TDSC 2026)：不确定性感知多视图融合的加密恶意流量可信检测 — `[[2026-TDSC-Shattering_Weak_Facades__Trustworthy_Detection_of_Encrypted_Malicious_Traffic_via_Uncertainty-Aware_Fusion]]`
- ConMD (TIFS 2026)：上下文掩码蒸馏的零正样本流量异常检测 — `[[2026-TIFS-Contextual_Masking_Distillation_for_Network_Traffic_Anomaly_Detection]]`
- FlowXpert (TMC 2026)：上下文感知流嵌入的 IoT 流量检测，端到端延迟 <30µs — `[[2026-TMC-FlowXpert__Context-Aware_Flow_Embedding_for_Enhanced_Traffic_Detection_in_IoT_Network]]`
- Proteus (WWW 2026)：可编程交换机上的低开销网内恶意流量检测，精度 67.8%→78.8% — `[[2026-WWW-Proteus__Towards_Accurate_and_Low-overhead_In_Network_Malicious_Traffic_Detection]]`
- M-En (Computer Networks 2026)：PLS 融合 + RNN-LSTM 迁移学习的多环境实时检测框架 — `[[2026-JCN-A_simulation-based_unified_framework_for_real-time_malicious_traffic_detection_in_multi-environment_networks]]`
- SuperFE (EuroSys 2025)：可编程交换机 + SmartNIC 的在线流量特征提取框架 — `[[2025-EuroSys-SuperFE__A_Scalable_and_Flexible_Feature_Extractor_for_ML-based_Traffic_Analysis_Applications]]`
- SketchFeature (NDSS 2025)：数据平面 HAF 逐流特征提取 sketch — `[[2025-NDSS-SketchFeature__High-Quality_Per-Flow_Feature_Extractor_Towards_Security-Aware_Data_Plane]]`

## 6. 当前趋势

1. **对比学习成为主流**：SmartDetector 和 tFusion 均采用对比学习框架，提升对抗鲁棒性和数据效率
2. **多粒度融合**：从单一 flow-level 特征向 packet/flow/host 多粒度融合演进
3. **少样本/零样本能力**：标注数据稀缺促使研究转向数据高效方法，tFusion 仅需 0.1% 标注数据
4. **大语言模型引入**：MET-LLM 探索将 LLM 的通用知识适配到流量分析领域
5. **开放集识别**：FEC-OSL 和 UT-PAB 关注对未知攻击类型的泛化能力
6. **实时性优化**：Whisper 的频域方法实现 13.22 Gbps 吞吐量，满足高速网络需求

## 7. 关键争议

1. **频域 vs. 时域特征**：Whisper 证明频域特征具有稳定性和区分性，但深度学习方法通常直接在时域上学习，哪种更优？
2. **对比学习的适用边界**：对比学习在恶意流量检测中的效果是否依赖于特定的数据分布和攻击类型？
3. **大语言模型的价值**：MET-LLM 的性能提升是否来自 LLM 的通用知识，还是仅仅因为更大的模型容量？
4. **开放集 vs. 闭集评估**：真实场景中未知攻击的比例远高于实验设置，开放集方法的实际效果如何？
5. **多模态融合的边际收益**：从单模态到多模态的性能提升是否值得额外的计算开销？

## 8. 未来方向

1. **对抗鲁棒性**：面对 traffic morphing、padding、timing perturbation 等 evasion 技术，提升检测鲁棒性
2. **数据高效学习**：利用自监督预训练、对比学习、元学习等技术减少标注依赖
3. **高速网络实时检测**：设计轻量化模型或利用频域特征实现 10Gbps+ 网络的实时检测
4. **跨环境泛化**：不同网络环境、不同时间段的域适应能力
5. **可解释性**：提升检测结果的可解释性，帮助安全运维人员理解告警原因
6. **增量学习**：适应不断变化的攻击手段和正常行为模式

## 9. 可用于写作的观点

- "频域特征具有时移不变性和可加性"——Whisper 利用频域特性在噪声和 packet loss 下保持鲁棒性
- "语义属性比原始特征更具区分性"——SmartDetector 的 SAM 表示在对抗逃举场景下保持 F1 > 93%
- "拓扑结构可减少标注依赖"——tFusion 利用网络拓扑结构驱动对比学习，仅需 0.1% 标注数据
- "领域特定编码器是 LLM 适配的关键"——MET-LLM 的领域特定 BPE 编码器比通用 NLP tokenizer 更适合流量数据
- "开放集识别是真实场景的刚需"——FEC-OSL 和 UT-PAB 关注对未知攻击类型的泛化能力
- "多粒度融合优于单粒度"——MTBD 的三维异构特征（flow/host/packet）投票机制达 99% P/R/F1

## 10. 待补充论文

- AppScanner (EuroS&P 2016)
- CUMUL (2014)
- FS-Net
- Var-CNN
- DeepPacket
- 2D-CNN / 3D-CNN baselines

---
type: method
name: "Self-Supervised Learning"
aliases: ["自监督学习", "SSL"]
tags:
  - self-supervised-learning
  - pre-training
  - traffic-classification
  - representation-learning
created: "2026-05-27"
updated: "2026-09-19"
---

# Self-Supervised Learning（自监督学习）

## 1. 方法定义

自监督学习（Self-Supervised Learning, SSL）是一类利用无标注数据设计辅助预训练任务（pretext task），从数据本身构造监督信号来学习通用表示的方法。在流量分析领域，SSL 通过大规模无标注网络流量数据进行预训练，学习具有泛化能力的流量表示（traffic representation），然后在少量标注数据上微调（fine-tuning）以适配具体的下游分类任务。

常见的自监督预训练任务包括：
- **Masked Language Model (MLM) 范式**：随机遮蔽输入序列中的部分 token，训练模型根据上下文重建被遮蔽内容（如 ET-BERT 的 Masked BURST Model）
- **Masked Autoencoder (MAE) 范式**：遮蔽高比例输入 patches，通过编码器-解码器结构重建原始输入（如 YaTC、NetMamba+）
- **对比学习（Contrastive Learning）范式**：通过构建正负样本对，拉近同类样本的表示、推远异类样本的表示（如 CoMask 的监督对比学习）
- **序列预测（Sequence Prediction）范式**：预测序列中片段的顺序或来源关系（如 ET-BERT 的 Same-origin BURST Prediction）

## 2. 方法解决的问题

1. **标注数据稀缺**：流量分类任务中获取大规模高质量标注数据成本高昂、耗时费力，SSL 利用海量无标注流量数据进行预训练，大幅减少对标注数据的依赖
2. **特征泛化能力不足**：监督学习模型高度依赖训练数据的规模和分布，难以泛化到未见过的加密方式、新应用或新网络环境；SSL 通过学习底层数据结构获得更通用的表示
3. **数据不平衡**：真实流量数据普遍存在长尾分布问题，SSL 预训练可在一定程度上缓解标注数据不平衡对分类性能的影响
4. **新场景适应成本高**：面对新的加密协议或应用类型，纯监督方法需要重新标注和训练；SSL 预训练模型通过少量标注数据微调即可快速适配新任务

## 3. 基本流程

1. **数据准备**：收集大规模无标注网络流量数据（可达数十 GB），按五元组（源 IP、目的 IP、源端口、目的端口、协议类型）切分为流（flow）
2. **流量表示**：将原始二进制流量转换为模型可处理的输入格式，包括 token 化（如 bi-gram 编码、BPE）、构建二维矩阵（如 MFR）或多模态序列（如 stride + packet size + interval）
3. **自监督预训练**：设计预训练任务（如掩码重建、对比学习、序列预测），在无标注数据上训练模型学习通用流量表示
4. **有监督微调**：将预训练模型适配到下游分类任务，通常冻结或微调编码器参数，添加分类头进行端到端训练
5. **推理部署**：使用微调后的模型对新流量进行分类预测

## 4. 输入与输出

| 项目 | 内容 |
|---|---|
| 输入 | 原始网络流量二进制数据（packet bytes、packet size、inter-arrival time 等），经预处理后转换为 token 序列、二维矩阵或多模态特征 |
| 输出 | 流量的高层语义表示（embedding），可用于下游分类、检测、聚类等任务 |
| 适用任务 | 加密流量分类（应用识别、恶意软件检测、VPN/Tor 流量分类）、流量异常检测、少样本流量分类、分布外（OOD）流量检测 |

## 5. 典型模型或算法

| 模型/算法 | 预训练任务 | 骨干架构 | 核心特点 |
|---|---|---|---|
| ET-BERT | Masked BURST Model (MBM) + Same-origin BURST Prediction (SBP) | 12 层双向 Transformer | 首个面向加密流量的 BERT-style 预训练模型，将流量组织为 BURST 序列进行 token 化 |
| YaTC | Masked Autoencoder (90% mask ratio) | Vision Transformer + 分层注意力 | 将流量视为图像而非文本，MFR 矩阵编码 byte/packet/flow 三级信息 |
| CoMask | Masked Sequence Prediction (MSP) + Supervised Contrastive Learning (SCL) | 3 层 Transformer Encoder | 半监督框架，交替训练策略协同利用标注和未标注数据 |
| NetMamba+ | Masked Autoencoder (90% mask ratio for stride) | Mamba (State Space Model) + Flash Attention | 首次将 SSM 引入流量分类，线性复杂度实现高效推理 |

## 6. 优点

1. **减少标注依赖**：利用海量无标注流量数据学习通用表示，仅需少量标注数据即可适配下游任务。ET-BERT 在 10% 标注数据下 F1=87%，远超 Deeppacket 的 44%
2. **强泛化能力**：预训练模型学到的底层流量模式具有跨任务、跨数据集的迁移能力。YaTC 在 Cross-Platform 数据集上预训练将 F1 从 69.93% 提升至 82.35%
3. **多任务兼容**：预训练获得的通用表示可适配多种下游任务（应用分类、恶意软件检测、VPN 识别等），无需为每个任务从头训练
4. **缓解数据不平衡**：预训练阶段不依赖标签信息，可在一定程度上缓解标注数据类别不平衡对分类性能的影响
5. **少样本学习能力**：在标注数据极度稀缺的场景下，SSL 预训练模型仍能保持较高性能

## 7. 局限

1. **预训练计算成本高**：大规模预训练需要大量计算资源（如 ET-BERT 需要 500K 步训练，YaTC 需要 150K 步 + 4x RTX3090，NetMamba+ 需要 4x A100）
2. **预训练数据质量依赖**：预训练效果受限于无标注数据的规模、多样性和覆盖范围；预训练数据中毒（data poisoning）可能引入安全风险
3. **分布偏移敏感**：预训练数据与下游任务数据分布差异较大时，迁移效果可能下降。NetMamba+ 在时序划分下 CSTNET-TLS1.3 准确率下降 8.47%
4. **预训练与微调不一致**：部分方法（如 YaTC）预训练阶段使用 global attention，微调阶段使用分层注意力，存在训练范式不一致的问题
5. **领域适配挑战**：从 NLP/CV 领域迁移的预训练范式可能不完全适配流量数据的特殊性（如流量字节的语义与自然语言词汇差异显著）

## 8. 代表论文

| 论文 | 年份 | 使用方式 | 贡献 |
|---|---:|---|---|
| ET-BERT: A Contextualized Datagram Representation with Pre-training Transformers for Encrypted Traffic Classification | 2022 | MBM + SBP 双任务预训练，BERT-style | 首个面向加密流量设计专属预训练任务的 BERT 模型，提出 Datagram2Token 框架，在 5 个加密流量分类任务上取得 SOTA，通过密码随机性分析提供理论解释 |
| Yet Another Traffic Classifier: A Masked Autoencoder Based Traffic Transformer with Multi-Level Flow Representation | 2023 | MAE 预训练（90% mask ratio），CV-style | 提出 MFR 矩阵编码 byte/packet/flow 三级信息，将流量分析从 NLP 范式转向 CV 范式，分层注意力机制降低复杂度，在 5 个数据集上大幅领先 |
| A Semi-Supervised Learning Framework for Encrypted Traffic Classification Based on Supervised Contrastive Learning and Masked Sequence Prediction Tasks | 2025 | MSP + SCL 交替训练，半监督 | 首次整合监督对比学习与掩码序列预测用于加密流量分类，交替训练策略协同利用标注和未标注数据，平均 F1 提升 3.3% |
| NetMamba+: A Framework of Pre-trained Models for Efficient and Accurate Network Traffic Classification | 2026 | MAE 预训练 + Mamba 架构 | 首次将 Mamba (SSM) 引入流量分类，线性复杂度实现 1.7 倍推理加速，多模态表示融合字节级和传输模式特征 |
| MIETT: Multi-Instance Encrypted Traffic Transformer (AAAI 2025) | 2025 | PRPP（Packet Relative Position Prediction）+ FCL（Flow Contrastive Learning）+ MFP（Masked Flow Prediction） | 提出两个面向流量特性的新 SSL 任务：PRPP 在 packet 级别预测 packet 对的相对位置（时序信号），FCL 在 flow 级别通过对比学习拉近同 flow 内不同 position 的 packet 表示、推远不同 flow 的 packet 表示；添加 PRPP+FCL 后 F1 从 73.62% 提升至 82.36% |
| TraGe: A Generic Packet Representation (IWQoS 2025) | 2025 | Field-level Masking + Random Masking + Dynamic Masking | 提出新的 SSL 掩码策略：对 header 使用 Field-level Masking（从几何分布 Geo(p) 采样连续长度掩码，保持协议字段字节连续性），对 payload 使用 Random Masking（适配非连续字节分布），配合 Dynamic Masking 防止过拟合；移除 FM 后 F1 下降 5.88% |
| TrafficGPT (arXiv 2024) | 2024 | GPT-style 自回归 SSL（next token prediction） | 使用自回归方式（GPT-style）预测下一个 token 进行预训练，通过线性注意力机制支持 12K token 上下文；可逆 token 表示实现 pcap ↔ token 双向映射，同一模型同时支持分类和生成 |
| TrafficMoE (arXiv 2026) | 2026 | 双分支 MLM（Header + Payload 独立遮蔽重建） | 提出异质性感知的 SSL 预训练：对 header 和 payload 分别施加随机 token 遮蔽，使用独立的稀疏 MoE 编码器进行 MLM 重建；预训练同时优化不确定性感知过滤（UF）模块，使不可靠 token 在早期阶段就获得低可靠性系数；MoE 架构在预训练阶段允许专家有机地对不同流量特征进行专业化分工；在 30GB 无标注流量（ISCX-VPN2016 NonVPN + CICIDS2017 + WIDE backbone trace）上预训练，去除预训练后 F1 从 97.65% 骤降至 73.25% |
| STAR (INFOCOM 2026) | 2025 | InfoNCE 跨模态对比学习 + 分类损失 + 类内一致性损失 | 首次为零样本网站指纹设计跨模态 SSL 预训练：双编码器分别处理加密流量轨迹和网站语义逻辑描述，通过 InfoNCE 对比损失对齐配对嵌入空间；辅助分类损失促进类间可分性，类内一致性损失促进同类流量嵌入聚集；引入结构感知数据增强（对两种模态施加语义一致的扰动）；在 150K+ 自动收集的流量-逻辑配对上预训练，无需目标网站流量即可零样本识别 |
| ASNet (TIFS 2025) | 2025 | **反例**：无需 SSL/预训练即达 SOTA | 通过 WSA（无参数词义聚合器）+ CSS（类别约束语义分离器）+ 任务感知提示，直接利用 BERT 已有知识，在 5 个数据集 7 个任务上无需任何自监督预训练即超越需要预训练的 ET-BERT 和 YaTC；证明 SSL/预训练并非流量分类 SOTA 的必要条件 |
| LitCVit (TIFS 2026) | 2026 | 自监督对比预训练（ntXent loss）+ 轻量 ViT | 轻量级对比自监督表征，加密恶意流量检测 |
| MH-Net (AAAI 2025) | 2025 | 对比学习辅助自监督任务 + 多视图异构图 | 多视图异构图表征增强加密流量分类 |
| FlowXpert (TMC 2026) | 2026 | 自监督对比预训练 + DBSCAN 聚类 + 伪标签学习 | 上下文感知流嵌入，IoT 流量检测 |
| ConMD (TIFS 2026) | 2026 | 上下文掩码蒸馏（自监督）+ 知识蒸馏 | 掩码蒸馏表征的零阳性网络流量异常检测 |
| BTRFormer (ICNP 2025) | 2025 | AES 16 字节块 BTR 表征 + 三层注意力的 MAE 掩码重建自监督（默认掩码率 0.9，0.75 最优） | ISCXTor2016 F1 达 100.00%；去掉 BTR 表征改用原始前 1024 字节的 32×32 图像后 F1 跌至 28.26%；掩码率 0.95 过高致重建过难、性能明显下降 |
| LotBoNC (AsiaCCS 2026) | 2026 | 自监督预训练 + 对比学习（encoder dropout 作增强）+ 熵正则化最优传输伪标签与 EM 式原型精化 | 长尾开世界新类发现准确率 60.01%/57.55%/60.15%，最高超基线 19.4 个百分点；对比增强是生死线——p=0 时整体准确率从 89.9/91.3/92.9 骤降至 58.2/61.3/63.5，p=0.50 回落至 70.1/71.5/72.3 |
| CDWF (IWQoS 2026) | 2026 | 流量增强自监督预训练（混合 CNN-Transformer 编码器）作为三阶段框架第一级 | 自监督预训练 + 对抗域适配 + 少样本适配使跨域多标签页 WF 的 5-tab 闭世界 P@5 达 75.80、超最佳基线 32.94 个百分点（tab 数未知时 Precision 72.37%）；去掉预训练侧数据增强 Precision 0.8615→0.7868 |
| Temporal Knowledge Graph Detection (IWQoS 2026) | 2026 | 在流式时序知识图谱（四元组 + 时间编码消息传递）上做自监督时序对比学习，按正常演化轨迹偏差判恶意 | 完全无标注条件下 UNSW-NB15/ToN-IoT/CIC-IoT2023 Macro F1 88.51/89.95/91.17；CIC-IoT2023 上比静态图自监督基线 Anomal-E（53.28）高 37.89 个百分点，后者甚至低于孤立流统计的 Kitsune（87.37） |
| Few-Packet POC (IWQoS 2026) | 2026 | 免预训练：把丢包/乱序下的不完整观测视为多视图，用重叠门控的表示级 + 预测级一致性正则（EMA teacher）提供自监督信号，推理只用单视图 | K=6 扰动下保持 ISCX-VPN 95.57%/ISCX-Tor 94.73%/CIC-IoT 96.60%，前缀依赖的 FS-Net 跌至 53.81%/53.82%/56.03%；不做重叠限制的全局一致性更差（Agreement 0.9210→0.8803），干净训练掉 8.28 个百分点 |
| Odysseus (IWQoS 2026) | 2026 | 包级 + 流级双重掩码 MAE 自监督预训练（400 patch，包级 r=0.9 与流级掩 2 条流二选一） | 无标注上下文预训练 + 上下文到单流蒸馏使 6 个 OOD 场景中 5 个 rank 1；消融中去掉自监督损失跌幅最大（Cross-Time Multi-F1 90.05→81.40），超过去掉流内注意力（−6.85）与 AFP（−2.65） |
| TARL (JCN 2026) | 2026 | MFM（掩码特征建模）+ 服务类型预测（STP）双自监督目标预训练，配共享 memory bank + 任务门控 adapter 多任务微调 | 自监督预训练初始化在流级严格划分下仍带来 3–5 个 F1 点增益（约 200k 步饱和）；四任务 F1 0.840–0.998，消融显示共享记忆库贡献 0.889 vs 完整 0.936 |
| MambaTIG (TDSC 2026) | 2026 | 良性-only 的课程掩码图自监督预训练（TIGPageRank 重要性驱动遮蔽），下游用 LSH kNN 异常检测 | 证明恶意标签并非必要条件：无任何恶意样本即在四数据集取得 98.84%/99.39%/99.49%/99.61% F1；时序对抗 reshaping 下 F1 92.21%，远超依赖原始包或局部序列的 ET-BERT 19.20% 与 Net-Mamba 21.78% |
| Argus (TIFS 2026) | 2026 | 无监督对比学习自编码器 ACLearner 学紧凑表征 + 类别条件重建损失分布 + 双空间一致性判据 | 极端概念漂移下保持 F1 88.22%（监督基线 FS-Net/ACID 崩至 31.55%/24.92%）；漂移样本恶意性由特征空间 DBSCAN 聚类 ∩ 宿主交互图无标注判定，准确率 >97%（去掉任一空间降至 31.97%/28.76%） |
| UTFormer (TIFS 2026) | 2026 | **反例**：不做任何自监督预训练，从零训练超轻量 Transformer（注意力 Top-K 动态字节蒸馏 + 可微架构搜索） | 106 KB 起的最小模型在砍掉 90%–95% 输入字节下保持精度、在线 10 Gbps 线速，算力较 Transformer 类基线降 9.0×–36398.5×；但论文中 Transformer 基线冻结骨干、UTFormer 从零训练，对比预算不对等 |
| HyTMTC (TNSM 2026) | 2026 | 统一多模态 token 序列 + 混合 Mamba-Transformer 骨干做 MLM 掩码预训练 | 7 个公开数据集平均 F1 95.03%；统一多模态序列优于 late fusion（平均 F1 0.9089→0.9456），混合骨干优于单骨干（0.9499 vs 0.8777/0.8701），参数共享后参数 14.49M→8.20M 且 F1 反升 |
| CipherSight (arXiv 2026) | 2026 | 记录-资源特权监督（P1，LUPI 范式）+ MRM 掩码记录建模预训练，微调期用特权语义教师 P2 做特征/逻辑蒸馏（仅训练期可见） | 特权监督收益随漂移类型而变：时移下增益几乎全部来自预训练阶段 P1（92.69→92.99 饱和），地理漂移下需两阶段 + 语义蒸馏（+1.37/+1.55 pp，约为地理漂移总体退化量的 31%）；推理仅需密文可观测元数据 |
| Pruned Traffic Trees (arXiv 2026) | 2026 | PTT-Full 预训练用流级 NT-Xent 自监督（同流两视图为正对、宏批次其他流为负对，同流内不同包永不互为负样本） | 自监督预训练同时产出字段显著性来源并驱动三级压缩链，0.186M 参数保留 Macro-F1 0.9325、有效 GFLOPs 降 98.85%；CSTNET-TLS1.3 上 ET-BERT 在 SII 掩蔽下 F1 仅 0.7759 |
| TDDM-Melatt (arXiv 2026) | 2026 | 外部记忆库 + 竞争门控 LSTM 在匿名化特征上做"无捷径"预训练，抑制伪特征相关性，再以类条件扩散补长尾 | 记忆-扩散框架在严格流级划分下 TLS-120class F1 0.681、延迟 <12 ms；类条件扩散是唯一统计显著的生成式增强（F1 +9.98%/+5.56%），可迁移性取决于骨干（ET-BERT +14.12% vs YaTC −6.61%） |
| The Colossus with Feet of Clay (arXiv 2026) | 2026 | **反例**：检验自监督/预训练字节级表征（ET-BERT/YaTC）在 PQC 协议漂移下的跨域可靠性 | 预训练表征并非天然更鲁棒：Non-PQC→Hybrid-PQC 全部退化（YaTC 1.0000→0.3582、ET-BERT 0.9316→0.6255），且方向+长度+时序的融合在任何设置下都不优于方向+长度，说明增加特征模态换不来跨域鲁棒性 |

## 9. 与其他方法的比较

| 对比维度 | 纯监督学习 | 自监督学习 (SSL) | 半监督学习 |
|---|---|---|---|
| 数据需求 | 仅需标注数据 | 预训练需大量无标注数据，微调需少量标注数据 | 同时利用标注和未标注数据 |
| 标注成本 | 高 | 低（微调阶段） | 中等 |
| 泛化能力 | 受限于训练数据分布 | 强（跨任务、跨数据集迁移） | 中等 |
| 训练流程 | 单阶段 | 预训练 + 微调两阶段 | 联合训练或交替训练 |
| 代表方法 | Deep Packet, FS-Net, AppScanner | ET-BERT, YaTC, NetMamba+ | CoMask |
| 适用场景 | 标注数据充足且任务固定 | 标注稀缺、需跨域迁移、多任务复用 | 有部分标注数据，需利用大量未标注数据 |

## 10. 在流量安全领域的应用价值

1. **加密流量分类**：SSL 是当前加密流量分类的主流预训练范式，能够从加密流量的隐式模式中学习判别性表示，有效应对 TLS 1.3、Tor 等现代加密技术带来的挑战
2. **恶意软件流量检测**：通过预训练学习正常流量和恶意流量的底层模式差异，在标注恶意样本稀缺时仍能实现高精度检测（如 USTC-TFC2016 数据集上各 SSL 方法 F1 均超过 97%）
3. **零日/未知流量识别**：SSL 预训练模型学到的通用表示对训练时未见过的新流量类型具有一定的识别能力，CoMask 在未知类别场景下 F1 达 0.9848
4. **少样本快速部署**：在新网络环境或新应用场景中，SSL 预训练模型仅需少量标注数据微调即可快速部署，降低运维成本
5. **在线流量分析**：SSL 预训练结合高效推理架构（如 NetMamba+ 的 Mamba），可实现 261.87 Mb/s 的在线分类吞吐量，满足实际网络环境的实时性需求

## 11. 后续问题

- 如何降低自监督预训练的计算成本，使其更易于在资源受限环境中使用？
- 预训练数据的时效性问题：互联网服务内容随时间变化，预训练模型的表示能力是否会随时间衰减？是否需要持续学习机制？
- 如何设计更适合流量数据特性的预训练任务，而非直接迁移 NLP/CV 的范式？
- 面对 TLS 1.3 ECH（Encrypted Client Hello）等新型加密机制，SSL 预训练模型如何适应更有限的可见信息？
- 多模态自监督学习（融合字节级、包级、流级、时间序列等多粒度信息）的最优策略是什么？
- 自监督预训练模型的安全性：如何防御预训练数据中毒攻击？
- 不同 SSL 范式（MLM、MAE、对比学习）在流量分析中的适用边界和最优组合方式尚需系统研究

- [[2025-WWW-AdvTG__An_Adversarial_Traffic_Generation_Framework_to_Deceive_DL-Based_Malicious_Traffic_Detection_Models]]（2026 批量深度分析；证据需正文复核）

- [[2025-WWW-Facing_Anomalies_Head-On__Network_Traffic_Anomaly_Detection_via_Uncertainty_Inspired_Inter-Sample_Differences]]（2026 批量深度分析；证据需正文复核）

- [[2026-IMC-Mind_the_Gap__Policy_vs_Reality_in_Post-Quantum_TLS_Deployment]]（2026 批量深度分析；证据需正文复核）

- [[2026-IMC-Quantifying_the_Privacy_Implications_of_High-Fidelity_Synthetic_Network_Traffic]]（2026 批量深度分析；证据需正文复核）

- [[2026-IMC-Replicability__Challenging_the_Myth_of_Randomness_Patterns_in_Encrypted_Traffic]]（2026 批量深度分析；证据需正文复核）

- [[2026-JCN-Towards_adaptive_and_robust_website_fingerprinting_defense_with_multi-agent_deep_reinforcement_learning]]（2026 批量深度分析；证据需正文复核）

- [[2026-JCS-GAN-based_Tor_obfuscated_traffic_identification_on_imbalanced_datasets]]（2026 批量深度分析；证据需正文复核）

- [[2026-JCS-PacketPatch__Practical_generation_and_deployment_of_adversarial_packets_for_byte-feature-based_encrypted_traffic_classification]]（2026 批量深度分析；证据需正文复核）

- [[2026-JCS-Uncovering_robot_joint-level_controller_actions_from_encrypted_network _traffic__Empirical_attacks_and_information-theoretic_bounds]]（2026 批量深度分析；证据需正文复核）

- [[2026-NSDI-SPLIDT__Partitioned_Decision_Trees_for_Scalable_Stateful_Inference_at_Line_Rate]]（2026 批量深度分析；证据需正文复核）

- [[2026-TNSM-Robust_and_Invisible_Flow_Watermarking_With_Invertible_Neural_Network_for_Traffic_Tracking]]（2026 批量深度分析；证据需正文复核）

- [[2026-TNSM-TunnelEye_An_Explainable_Framework_for_Real-Time_Detection_of_Malicious_DoH_Traffic_in_High-Speed_Backbone_Networks]]（2026 批量深度分析；证据需正文复核）

- [[2026-USENIX-DNS_Cache_Poisoning_Like_it’s_2006]]（2026 批量深度分析；证据需正文复核）

- [[2026-USENIX-DaLens__Charting_DNS_Self-Amplification_Threats_at_Large]]（2026 批量深度分析；证据需正文复核）

- [[2026-USENIX-Generating_Precise_Format_Specification_for_Network_Protocols_Through_Adversarial_LLM_Interactions]]（2026 批量深度分析；证据需正文复核）

- [[2026-WWW-Cardinality_is_Not_Enough__Super_Host_Detection_via_Segmented_Cardinality_Estimation]]（2026 批量深度分析；证据需正文复核）

- [[2026-WWW-Eclipse_Attacks_on_Ethereum’s_Peer-to-Peer_Network]]（2026 批量深度分析；证据需正文复核）

- [[2026-WWW-Forge__A_Robust_Multi-tab_Website_Fingerprinting_Attack_Via_Blind_Source_Separation]]（2026 批量深度分析；证据需正文复核）

- [[2026-WWW-Robust_LLM-Based_Website_Fingerprinting_under_Dynamic_Real-World_Conditions]]（2026 批量深度分析；证据需正文复核）

- [[2026-arXiv-Despite_Instructions__Frontier_Agents_Improvise_Covert_Channels_at_Test_Time]]（2026 批量深度分析；证据需正文复核）

- [[2026-arXiv-Exact_Second-Order_Asymptotics_in_Covert_Communication_Over_Discrete_Memoryless_Channels]]（2026 批量深度分析；证据需正文复核）

- [[2026-arXiv-Feedback_Coding_Enables_Inference-Time_Covert_Agentic_Communication]]（2026 批量深度分析；证据需正文复核）

- [[2026-arXiv-Improving_the_Reliability_of_Anomaly_Detection_for_Encrypted_OPC_UA_Traffic_over_Private_5G]]（2026 批量深度分析；证据需正文复核）

- [[2026-arXiv-Secrets_in_Radio_Waves__Towards_Practical_and_Protocol-Agnostic_PHY_Information_Hiding]]（2026 批量深度分析；证据需正文复核）

- [[2026-arXiv-Your_Model_Is_Leaking__Covert_Information_Transfer_through_LLM_Residual_Streams]]（2026 批量深度分析；证据需正文复核）

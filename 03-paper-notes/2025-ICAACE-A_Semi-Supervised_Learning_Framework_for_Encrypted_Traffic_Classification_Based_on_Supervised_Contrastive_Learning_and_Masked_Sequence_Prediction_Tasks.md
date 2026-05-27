---
type: paper
title_original: "A Semi-Supervised Learning Framework for Encrypted Traffic Classification Based on Supervised Contrastive Learning and Masked Sequence Prediction Tasks"
title_cn: "基于监督对比学习和掩码序列预测的加密流量分类半监督学习框架"
authors: ["Zhongyu Guo", "Wei Wu", "Zhaoyun Liu", "Bin Lu", "Man Guo", "Xiangnan Lin"]
year: 2025
venue: "ICAACE 2025"
doi: unknown
url: unknown
pdf: unknown
mineru_md: "02-parsed-markdown/2025-ICAACE-A_Semi-Supervised_Learning_Framework_for_Encrypted_Traffic_Classification_Based_on_Supervised_Contrastive_Learning_and_Masked_Sequence_Prediction_Tasks.md"
status: processed
reading_level: L2
research_area: ["encrypted traffic classification", "semi-supervised learning", "deep learning"]
task: ["traffic classification", "encrypted traffic analysis", "semi-supervised classification"]
method: ["supervised contrastive learning", "masked sequence prediction", "Transformer encoder", "semi-supervised learning", "cross-training"]
dataset: ["DAPT2020", "CICAndMal2017", "Cross-Platform", "ISCX-Tor-nonTor", "ISCX-VPN-nonVPN", "USTC-TFC2016", "XD-TLS"]
code: unknown
relevance: high
created: "2026-05-27"
updated: "2026-05-27"
---

# A Semi-Supervised Learning Framework for Encrypted Traffic Classification Based on Supervised Contrastive Learning and Masked Sequence Prediction Tasks

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | A Semi-Supervised Learning Framework for Encrypted Traffic Classification Based on Supervised Contrastive Learning and Masked Sequence Prediction Tasks |
| 中文标题 | 基于监督对比学习和掩码序列预测的加密流量分类半监督学习框架 |
| 作者 | Zhongyu Guo, Wei Wu, Zhaoyun Liu, Bin Lu, Man Guo, Xiangnan Lin |
| 年份 | 2025 |
| 会议/期刊 | ICAACE 2025 |
| 研究方向 | 加密流量分类、半监督学习 |
| 任务类型 | 加密流量分类（已知类别和未知类别场景） |
| 方法关键词 | supervised contrastive learning, masked sequence prediction (MSQ), Transformer encoder, semi-supervised learning, cross-training strategy |
| 数据集 | DAPT2020, CICAndMal2017, Cross-Platform, ISCX-Tor-nonTor, ISCX-VPN-nonVPN, USTC-TFC2016, XD-TLS |
| 是否开源 | 否 |
| 作者单位 | Key Laboratory of Cyberspace Security, Ministry of Education, Zhengzhou, China |
| 资助 | 国家自然科学基金（Nos. 62302520, 62402524） |

## 1. 一句话总结

> 提出 CoMask 框架，通过交替训练策略整合 supervised contrastive learning 和 masked sequence prediction 任务，充分利用标注和未标注数据优化特征空间，在多个加密流量分类数据集上平均 F1 提升 3.3%。

## 2. 摘要翻译

### 2.1 摘要原文

With the widespread adoption of encryption technologies, the proportion of encrypted traffic in network traffic has significantly increased, making encrypted traffic classification a key technology for enhancing network security and optimizing network performance. Although existing research on encrypted traffic classification has made certain advancements, two major challenges remain: (1) Current classification methods generally lack effective utilization of unlabeled data, limiting models to specific task scenarios and reducing their generalization ability; (2) During pre-training, existing methods often focus solely on unlabeled data, failing to fully leverage label information, which restricts further optimization of the feature space. To address these issues, this paper proposes CoMask, a semi-supervised learning framework for encrypted traffic classification that integrates supervised contrastive learning and masked sequence prediction tasks. The framework uses multi-granularity feature sequences as input and employs a cross-training strategy to collaboratively utilize both labeled and unlabeled data. Specifically, the framework utilizes unlabeled data to perform the masked sequence prediction task to enhance the generalization ability of feature representations, while supervised contrastive learning tasks are conducted using labeled data to optimize the feature space. Experimental results show that CoMask outperforms existing state-of-the-art methods on multiple public datasets, with an average F1 score improvement of 3.3%, demonstrating its effectiveness in handling encrypted traffic classification tasks in both known and unknown category scenarios.

### 2.2 摘要中文翻译

随着加密技术的广泛应用，加密流量在网络流量中的占比显著增加，使得加密流量分类成为提升网络安全和优化网络性能的关键技术。尽管现有研究取得了一定进展，但仍面临两大挑战：(1) 现有分类方法普遍缺乏对未标注数据的有效利用，限制了模型在特定任务场景下的泛化能力；(2) 在预训练阶段，现有方法通常仅关注未标注数据，未能充分利用标注信息，限制了特征空间的进一步优化。为此，本文提出 CoMask，一种整合监督对比学习和掩码序列预测任务的加密流量分类半监督学习框架。该框架以多粒度特征序列作为输入，采用交叉训练策略协同利用标注和未标注数据。具体而言，框架利用未标注数据执行掩码序列预测任务以增强特征表示的泛化能力，同时利用标注数据进行监督对比学习以优化特征空间。实验结果表明，CoMask 在多个公开数据集上超越现有最优方法，平均 F1 分数提升 3.3%，证明其在已知和未知类别场景下处理加密流量分类任务的有效性。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 加密技术广泛应用于电商、社交媒体、流媒体、远程办公和在线支付等领域，87% 以上的网络威胁通过加密通道传播（Zscaler 2024 报告），加密流量分类成为网络安全的关键技术
- 现有深度学习方法依赖大规模标注数据，获取成本高昂且耗时；面对未知流量时泛化能力有限，需要重新标注和训练
- 现有预训练方法（如 ET-BERT）主要基于无监督任务，未能充分利用已知类别流量的标注信息，限制了特征空间的表达能力
- 真实场景中未标注流量数据远多于标注数据，需要一种能够协同利用两种数据的半监督框架

### 3.2 现有方法的痛点和不足

| 现有方法 | 痛点 |
|---|---|
| Fingerprint-based 方法（VS-DFA, MaMPF） | 依赖预定义规则集或签名，对加密算法演进和网络环境变化适应性差 |
| Statistical Feature-based 方法（DarknetSec, ETC-PS） | 特征提取依赖大量先验知识和专家经验，开发维护成本高 |
| Deep Learning-based 方法（DF, Deep Packet, TFE-GNN） | 依赖大规模标注数据，对未知流量泛化能力有限 |
| 纯无监督预训练方法（CoMDet, CPN） | 预训练仅基于无监督对比学习，未能充分利用标注数据资源；依赖数据增强或无监督聚类构建正负样本对，假设同类样本特征相似，但复杂网络环境中该假设不总成立 |
| Replication（无监督 + 数据增强） | 仅用未标注数据训练，未整合标注信息 |

### 3.3 论文的研究假设或核心直觉

- **核心假设**：标注数据和未标注数据可以互补——未标注数据通过掩码序列预测学习通用特征表示，标注数据通过监督对比学习优化特征空间的类别判别能力
- **关键直觉**：通过交替训练（cross-training）策略，让两种任务协同优化同一个 Transformer encoder，既获得泛化能力又获得判别能力
- **多粒度特征**：原始字节序列捕获流量字节级别的上下文信息，包长度序列捕获流量级别的行为模式，两者互补

## 4. 方法设计

### 4.1 方法整体流程

1. **Traffic2Token 阶段**：将原始网络流量转换为特征序列——原始字节 token 序列和包长度 token 序列，拼接后形成模型输入
2. **半监督训练阶段**：采用交替训练策略，先用大规模未标注数据（含标注数据视为未标注）进行 masked sequence prediction 训练，收敛后切换到监督对比学习任务优化标注数据的特征空间，如此迭代
3. **分类头微调阶段**：冻结 encoder 参数，仅训练分类头适配具体分类任务

### 4.2 详细 Pipeline（表格形式）

| 步骤 | 描述 | 技术细节 |
|---|---|---|
| 1. 流量分割 | 基于五元组（源IP、目的IP、源端口、目的端口、协议类型）进行双向流分割 | 每条流作为独立样本 |
| 2. 原始字节提取 | 从每个包的第 39 字节开始提取 128 个连续字节 | 避免 IP 地址、端口号、以太网帧和 IP 头的干扰 |
| 3. 字节 Token 化 | 每两个连续字节作为一个 token | 如 {1f, 29, fd, fb} -> {1f29, fdfb}，映射到 0-65535 |
| 4. 包长度提取 | 每条流取前 32 个包的包长度 | "+" 表示正向、"-" 表示反向，映射到 65536-68564 |
| 5. 输入构建 | [CLS] + Raw_bytes + [SEP] + Packet_length + [PAD] | 特殊 token: [CLS]=68565, [SEP]=68566, [PAD]=68567, [MASK]=68568 |
| 6. 掩码序列预测 | 对输入进行随机掩码（10%-15%），80% 替换为 [MASK]，10% 随机替换，10% 保持不变 | 使用交叉熵损失 L_msp |
| 7. 监督对比学习 | 构建正负样本对，正样本：同类别不同实例；负样本：不同类别（来自 batch 和 feature queue） | 使用温度系数 tau=0.07 的对比损失 L_scl，采用 projection head 解耦优化目标 |
| 8. 交替训练 | MSP 收敛后切换到 SCL，迭代进行 | 监测 MSP 准确率和损失，连续 3 个 epoch 改善后切换 |
| 9. 分类头微调 | 冻结 encoder，仅训练分类头 | 两层线性层 + Softmax |

### 4.3 模型结构或系统模块（表格形式）

| 模块 | 功能 | 输入 | 输出 |
|---|---|---|---|
| 特征序列提取器 | 从原始流量中提取多粒度 token 序列 | PCAP 原始流量 | 原始字节 token 序列 + 包长度 token 序列 |
| 输入数据构建器 | 拼接、添加特殊 token、动态填充 | 两组 token 序列 | 统一长度的输入序列 X |
| 随机掩码模块 | 对输入进行随机掩码处理 | 输入序列 X | 掩码后的输入 X_tilde |
| Embedding 模块 | 词嵌入 + 位置编码 | X_tilde | X_embed (m x n x d) |
| Transformer Encoder | 多头自注意力 + 前馈网络，提取特征表示 | X_embed | Encoded (编码输出) |
| Projection Head | 将 encoder 输出映射到对比学习专用空间 | Encoded 特征 | 投影特征 z（用于计算 L_scl） |
| 线性输出层 | 将 encoder 输出映射到词表大小 | Encoded 特征 | 预测的 token 分布（用于计算 L_msp） |
| 分类头 | 将特征映射到任务类别空间 | Encoded 特征 | 类别预测概率 |
| Feature Queue | 存储历史样本特征，扩充负样本集 | batch 特征和标签 | 更新后的队列（FIFO 策略） |

### 4.4 公式、算法和机制解释

**原始字节 Token 序列**：

$$Raw\ bytes = \{b_1, ..., b_{128}\}, b_i \in \mathbb{D}$$

其中 b_i 为每两个原始字节对应的 token，D 的范围为 0 到 65535。

**包长度 Token 序列**：

$$Packet\ length = \{l_1, ..., l_{32}\}, l \in \mathbb{L}$$

其中 l_i 为每个包的长度，L 的范围为 65536 到 68564。

**输入数据**：

$$X = [CLS] + Raw\ bytes + [SEP] + Packet\ length + [PAD]$$

**掩码序列预测损失**：

$$L_{msp} = -\sum_{i=1}^{n} \log(P(MASK_i = token_i | \widetilde{X}))$$

其中 MASK_i 为掩码位置的真实 token，使用交叉熵损失训练多类分类问题。

**监督对比学习损失**：

$$L_{scl} = -\frac{1}{N} \sum_{i=1}^{n} \log \frac{\exp(sim(z_i, z_j^+) / \tau)}{\exp(sim(z_i, z_j^+) / \tau) + \sum_{k=1}^{q} \exp(sim(z_i, z_k^-) / \tau)}$$

其中 z_i 为当前样本特征，z_j^+ 为正样本特征，z_k^- 为负样本特征，sim 为余弦相似度，tau 为温度参数（0.07）。

**关键机制解释**：

- **交替训练策略**：解决了联合训练中需要标注和未标注数据样本量一致的限制，先用 MSP 利用所有数据学习通用表示，收敛后用 SCL 优化标注数据的特征空间，迭代进行
- **Projection Head**：借鉴 SimCLR 的设计，将 encoder 输出映射到专用投影空间计算对比损失，解耦对比学习目标和 encoder 特征学习目标，避免冲突
- **Feature Queue**：借鉴 MoCo 设计，使用 FIFO 策略实时更新，扩充负样本来源，缓解单 batch 样本量有限的问题
- **多粒度特征**：原始字节序列（128 个 token）捕获字节级上下文，包长度序列（32 个 token）捕获流量级行为模式

### 4.5 方法优势

1. **有效利用未标注数据**：通过 MSQ 任务充分利用大量未标注流量数据学习通用特征表示
2. **充分利用标注信息**：通过 SCL 任务利用标注数据优化特征空间，实现类内聚集和类间分离
3. **已知和未知类别兼顾**：MSP 增强泛化能力（未知类别），SCL 增强判别能力（已知类别），互补效果显著
4. **交叉训练策略**：解决了联合训练中标注和未标注数据量不匹配的问题
5. **多粒度特征输入**：原始字节和包长度两个粒度互补，提升特征表示的全面性
6. **快速适应新任务**：通过微调分类头即可快速适配不同分类任务

### 4.6 方法不足

1. **类别不平衡问题**：在 ISCX-nonVPN 数据集上表现不佳，存在显著的类别不平衡问题
2. **训练复杂度**：交替训练策略增加了训练流程的复杂性，需要监测收敛指标来决定切换时机
3. **MSP 收敛慢**：掩码序列预测任务收敛相对缓慢，影响整体训练效率
4. **计算开销**：Feature Queue 的维护和对比学习的计算增加了内存和计算开销
5. **标注数据来源受限**：标注训练数据仅来自 CICAndMal2017-8 的 8 个类别，标注数据的代表性可能影响模型性能
6. **未考虑时序特征**：输入为扁平化的 token 序列，未显式建模包之间的时序关系

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 对比维度 | 传统深度学习方法 | 纯无监督预训练方法 | CoMask (本文) |
|---|---|---|---|
| 数据利用 | 仅标注数据 | 仅未标注数据 | 标注 + 未标注数据协同 |
| 预训练任务 | 无 | 无监督对比学习或 MLM | MSP + 监督对比学习 |
| 训练策略 | 单阶段监督训练 | 预训练 + 微调 | 交替训练 + 分类头微调 |
| 标注信息利用 | 充分 | 不充分（仅在微调阶段） | 充分（训练和微调阶段） |
| 泛化能力 | 受限于训练类别 | 较强 | 强（已知 + 未知类别） |

### 5.2 创新点分析（表格形式）

| 创新点 | 说明 |
|---|---|
| 首次整合 SCL + MSQ 用于加密流量分类 | 据作者所知，这是首次将监督对比学习与掩码序列预测任务结合应用于加密流量分类 |
| 交替训练策略 | 解决联合训练中标注和未标注数据量需一致的限制，最大化利用未标注数据 |
| 多粒度特征序列输入 | 原始字节序列 + 包长度序列作为输入，从多个维度捕获流量语义特征 |
| 已知和未知类别统一框架 | 同一框架通过 MSP 和 SCL 的互补，同时处理已知类别分类和未知类别泛化 |

### 5.3 适用场景

- 已知类别的加密流量分类（如恶意软件流量识别、应用识别）
- 未知类别的加密流量分类（面对训练时未见过的新流量类型）
- 标注数据稀缺场景下的加密流量分类
- 需要快速适应新分类任务的场景（通过微调分类头）

### 5.4 方法对比表

| 方法 | 数据利用 | 对比学习 | MLM/MSQ 任务 | 训练方式 | 平均 F1 |
|---|---|---|---|---|---|
| K-FP | 标注 | 否 | 否 | 监督 | 0.7752 |
| DF | 标注 | 否 | 否 | 监督 | 0.6570 |
| AppScanner | 标注 | 否 | 否 | 监督 | 0.7106 |
| GraphDApp | 标注 | 否 | 否 | 半监督 | 0.5547 |
| ET-BERT | 未标注 | 是 | 否 | 半监督 | 0.9112 |
| **CoMask** | **标注+未标注** | **是** | **是** | **半监督** | **0.9444** |

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **硬件环境**：Linux 服务器，Intel Xeon Platinum 8163 CPU，Tesla V100 GPU
- **软件环境**：PyTorch 1.13.1
- **训练策略**：先进行 MSP 任务训练，监测准确率和损失，连续 3 个 epoch 改善后切换到 SCL 任务，交替迭代
- **超参数**：Epoch=50, 学习率=1e-5, AdamW 优化器, Batch size=16, d_model=768, nhead=12, encoder 层数=3, dim_feedforward=1024, tau=0.07, warmup=0.05, patience=10

### 6.2 数据集

| 数据集 | 包数 | 流数 | 标签数 | 用途 |
|---|---|---|---|---|
| DAPT2020 | 1,863,462 | 62,576 | 20 | 未标注训练数据 |
| CICAndMal2017 | 1,997,120 | 71,576 | 42 | 标注训练（8类）+ 未标注训练 |
| Cross-Platform | 1,363,761 | 48,704 | 411 | 未标注训练数据 |
| ISCX-Tor-nonTor | 100,588 | 9,676 | 16 | 下游评估任务 |
| ISCX-VPN-nonVPN | 53,120 | 5,602 | 12 | 下游评估任务 |
| USTC-TFC2016 | 97,115 | 9,853 | 20 | 下游评估任务 |
| XD-TLS | 6,071,244 | 34,545 | N/A | 未标注训练数据 |

- 标注训练数据：CICAndMal2017-8（Dowgin, Feiwo, Charger, LockerPin, FakeApp, AVforandroid, Beanbot, fakeinst 共 8 类）
- 未标注训练数据：DAPT2020, CICAndMal2017, Crossplatform, XD-TLS1.3（训练:验证 = 9:1）
- 下游任务数据：CICAndMal2017-8, ISCX-Tor-nonTor, ISCX-VPN-nonVPN, USTC-TFC2016（训练:验证:测试 = 8:1:1）

### 6.3 Baseline

| Baseline | 类型 | 说明 |
|---|---|---|
| K-FP | 传统方法 | 随机森林提取流量指纹，k-NN + Hamming 距离进行开放世界分类 |
| DF | 深度学习 | 首个针对 Tor 流量防御机制优化的 CNN 方法（Deep Fingerprinting） |
| AppScanner | 传统方法 | 利用时空特征 + SVM + 随机森林进行智能手机应用指纹识别 |
| GraphDApp | 深度学习 | 首个将 GNN 引入 DApp 加密流量分类的方法 |
| ET-BERT | 预训练模型 | 首个将预训练模型用于加密流量分类的方法，两个自监督任务 |

### 6.4 评价指标

- **Accuracy (AC)**：全局正确率，衡量模型在所有类别上的整体预测正确性
- **Precision (PR)**：精确率，衡量模型返回样本的正确性
- **Recall (RC)**：召回率，衡量模型检索正样本的能力
- **F1 Score**：精确率和召回率的调和平均，综合衡量分类性能

### 6.5 关键实验结果（表格形式）

**ISCX-Tor / ISCX-nonTor / CICAndMal2017-8 数据集：**

| 方法 | ISCX-Tor F1 | ISCX-nonTor F1 | CICAndMal2017-8 F1 |
|---|---|---|---|
| K-FP | 0.6313 | 0.8167 | 0.7644 |
| DF | 0.4719 | 0.7590 | 0.5897 |
| AppScanner | 0.6163 | 0.8413 | 0.4997 |
| GraphDApp | 0.2281 | 0.5352 | 0.7627 |
| ET-BERT | 0.9397 | 0.8332 | 0.9246 |
| **CoMask** | **0.9848** | **0.9051** | **0.9886** |

**ISCX-VPN / ISCX-nonVPN / USTC-TFC2016 数据集：**

| 方法 | ISCX-VPN F1 | ISCX-nonVPN F1 | USTC-TFC2016 F1 |
|---|---|---|---|
| K-FP | 0.8747 | 0.7387 | 0.8840 |
| DF | 0.7921 | 0.6701 | 0.7593 |
| AppScanner | 0.8722 | 0.7486 | 0.8892 |
| GraphDApp | 0.5740 | 0.3614 | 0.8234 |
| ET-BERT | 0.9463 | 0.9235 | 0.9930 |
| **CoMask** | **0.9579** | 0.9254 | **0.9967** |

**消融实验结果：**

| 方法 | ISCX-Tor | ISCX-nonTor | CICAndMal2017-8 | ISCX-VPN | ISCX-nonVPN | USTC-TFC2016 |
|---|---|---|---|---|---|---|
| CoMask | 0.9848 | 0.9051 | 0.9886 | 0.9579 | 0.9254 | 0.9967 |
| w/o MSP | 0.3124 | 0.2275 | 0.9763 | 0.1786 | 0.0117 | 0.6583 |
| w/o SCL | 0.9813 | 0.8665 | 0.9647 | 0.9468 | 0.9196 | 0.9885 |
| w/o RB | 0.9155 | 0.8238 | 0.9302 | 0.7759 | 0.8146 | 0.9508 |
| w/o PL | 0.9333 | 0.8351 | 0.9418 | 0.8188 | 0.8485 | 0.9493 |

### 6.6 优势最明显的场景

- **已知类别分类**：在 CICAndMal2017-8 上 F1 达 0.9886，相比 ET-BERT 提升 6.4%
- **未知类别泛化**：在 ISCX-Tor 上 F1 达 0.9848，相比 ET-BERT 提升 4.51%，说明 MSP 任务有效增强了泛化能力
- **MSP 的关键作用**：移除 MSP 后未知类别数据集 F1 大幅下降（ISCX-Tor 从 0.9848 降至 0.3124），证明其对泛化能力的核心贡献
- **SCL 的互补作用**：移除 SCL 后已知类别（CICAndMal2017-8）F1 从 0.9886 降至 0.9647，证明其对判别能力的贡献

### 6.7 局限性

1. **类别不平衡敏感**：在 ISCX-nonVPN 数据集上未达到最优，类别不平衡问题仍然存在挑战
2. **MSP 收敛慢**：掩码序列预测任务收敛相对缓慢，需要监测指标决定切换时机，增加了训练流程的复杂性
3. **标注数据范围有限**：标注训练数据仅来自 8 个恶意软件类别，可能影响模型在其他流量类型上的表现
4. **未显式建模时序关系**：输入为扁平化 token 序列，未显式捕获包之间的时序依赖
5. **计算资源需求**：Feature Queue 维护、Transformer Encoder 和对比学习计算需要较大内存和计算资源

## 7. 学习与应用

### 7.1 是否开源？

否。论文未提供代码或开源实现。

### 7.2 复现关键步骤

1. **数据准备**：下载 DAPT2020, CICAndMal2017, Cross-Platform, ISCX-Tor-nonTor, ISCX-VPN-nonVPN, USTC-TFC2016 数据集；准备自采集 XD-TLS 数据
2. **流量分割**：基于五元组对 PCAP 文件进行双向流分割
3. **特征提取**：从每个包第 39 字节开始取 128 字节，每两字节化为一个 token；取前 32 个包的带方向包长度
4. **输入构建**：拼接 [CLS] + Raw_bytes + [SEP] + Packet_length + [PAD]，动态填充
5. **模型构建**：3 层 Transformer Encoder（d_model=768, nhead=12, dim_feedforward=1024）+ Projection Head + 分类头
6. **交替训练**：先训练 MSP（掩码率 10%-15%），监测准确率连续 3 epoch 改善后切换到 SCL，迭代进行
7. **微调**：冻结 encoder，仅训练分类头

### 7.3 关键超参数、预处理和训练细节

| 参数 | 值/说明 |
|---|---|
| Epoch | 50 |
| Learning rate | 1e-5 |
| Optimizer | AdamW |
| Batch size | 16 |
| d_model | 768 |
| nhead | 12 |
| num_encoder_layers | 3 |
| dim_feedforward | 1024 |
| 温度系数 tau | 0.07 |
| warmup | 0.05 |
| patience (early stopping) | 10 |
| 掩码率 | 初始 10%，逐渐增至 15% |
| 掩码替换策略 | 80% [MASK], 10% 随机替换, 10% 不变 |
| 原始字节起始位置 | 第 39 字节 |
| 原始字节长度 | 128 字节（64 个 token） |
| 包长度序列长度 | 前 32 个包 |
| Feature Queue | FIFO 策略，借鉴 MoCo |
| Projection Head | 线性层，借鉴 SimCLR |
| 训练/验证划分 | 未标注数据 9:1，下游任务 8:1:1 |

### 7.4 能否迁移到其他任务？

- **其他加密协议分类**：方法框架通用，可迁移到 TLS、QUIC 等其他加密协议的流量分类
- **恶意流量检测**：已通过 CICAndMal2017 数据集验证，可扩展到更多恶意流量类型
- **VPN 流量识别**：已在 ISCX-VPN-nonVPN 上验证，可进一步扩展
- **IoT 设备识别**：多粒度特征和半监督框架适合 IoT 场景下标注数据稀缺的问题
- **其他序列分类任务**：MSP + SCL 的交替训练思路可推广到其他需要利用标注和未标注数据的序列分类任务

### 7.5 对我的研究有什么启发？

1. **半监督范式**：在加密流量分类中标注数据稀缺是普遍问题，交替训练策略是一种有效利用大量未标注数据的思路
2. **多任务互补设计**：MSP 学习通用表示（泛化），SCL 优化类别边界（判别），两者互补的设计思路值得借鉴
3. **多粒度特征**：原始字节 + 包长度的多粒度输入设计，简单但有效，可在其他流量分析任务中尝试
4. **Projection Head 解耦**：在多任务学习中，使用 projection head 解耦不同任务的优化目标，避免冲突，是一种实用技巧
5. **Feature Queue 扩充负样本**：借鉴 MoCo 的 feature queue 设计，在 batch 较小时有效扩充对比学习的负样本来源
6. **消融实验设计**：论文对 MSP、SCL、RB、PL 四个组件分别消融，清晰展示了各组件的贡献，实验设计值得参考

## 8. 总结

### 8.1 核心思想（不超过20字）

交替训练监督对比学习与掩码预测，协同利用标注和未标注数据。

### 8.2 速记版 Pipeline（3-5步）

1. 将流量转换为多粒度 token 序列（原始字节 + 包长度）作为输入
2. 用未标注数据训练 masked sequence prediction 任务，学习通用特征表示
3. 用标注数据训练 supervised contrastive learning 任务，优化特征空间判别能力
4. 交替迭代步骤 2 和 3，获得兼具泛化和判别能力的 encoder
5. 冻结 encoder，微调分类头适配具体下游分类任务

## 9. Obsidian 知识链接

### 9.1 相关概念

- Encrypted Traffic Classification - 加密流量分类
- Semi-supervised Learning - 半监督学习
- Supervised Contrastive Learning - 监督对比学习
- Masked Language Model (MLM) - 掩码语言模型
- Transformer Encoder - Transformer 编码器
- Feature Representation Learning - 特征表示学习
- Generalization Ability - 泛化能力

### 9.2 相关方法

- SimCLR - 对比学习框架，本文 Projection Head 的设计来源
- MoCo - 动量对比学习，本文 Feature Queue 的设计来源
- ET-BERT - 首个将预训练模型用于加密流量分类的方法
- BERT - 掩码语言模型的原始设计
- Deep Fingerprinting (DF) - 基于 CNN 的网站指纹攻击方法
- K-FP - 基于随机森林的流量指纹方法

### 9.3 相关任务

- Encrypted Malware Traffic Detection - 加密恶意流量检测
- Application Fingerprinting - 应用指纹识别
- Tor Traffic Classification - Tor 流量分类
- VPN Traffic Detection - VPN 流量检测
- Zero-day Traffic Classification - 零日流量分类

### 9.4 可更新的综述页面

- Encrypted Traffic Classification Survey
- Contrastive Learning in Traffic Analysis
- Semi-supervised Methods for Network Traffic

### 9.5 可加入的对比表

- Encrypted Traffic Classification Methods
- Pre-training Methods for Traffic Analysis

## 10. 证据记录（表格形式）

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E1 | 实验结果 | CoMask 在 ISCX-Tor 上 F1=0.9848，超越 ET-BERT 的 0.9397 | Table V |
| E2 | 实验结果 | CoMask 在 CICAndMal2017-8 上 F1=0.9886，超越 ET-BERT 的 0.9246 | Table V |
| E3 | 实验结果 | CoMask 在 USTC-TFC2016 上 F1=0.9967，超越 ET-BERT 的 0.9930 | Table VI |
| E4 | 实验结果 | CoMask 在 ISCX-VPN 上 F1=0.9579，超越 ET-BERT 的 0.9463 | Table VI |
| E5 | 实验结果 | CoMask 在 ISCX-nonVPN 上 F1=0.9254，略高于 ET-BERT 的 0.9235 | Table VI |
| E6 | 消融实验 | 移除 MSP 后 ISCX-Tor F1 从 0.9848 降至 0.3124，ISCX-VPN 从 0.9579 降至 0.1786 | Table VII, VIII |
| E7 | 消融实验 | 移除 SCL 后 CICAndMal2017-8 F1 从 0.9886 降至 0.9647 | Table VII |
| E8 | 消融实验 | 移除 RB 后平均 F1 下降 0.091，移除 PL 后平均 F1 下降 0.072 | Section IV-D |
| E9 | 参数分析 | encoder 层数=3 时 F1=95%，6 层时 F1=96.31% 但训练时间最大 | Figure 3 |
| E10 | 参数分析 | 温度系数 tau=0.07 时 F1 最优，更高值导致性能下降 | Figure 4 |
| E11 | 方法对比 | CoMask 平均 F1 相比 ET-BERT 提升 3.3% | Section IV-C |
| E12 | 统计数据 | 87% 以上网络威胁通过加密通道传播（Zscaler 2024） | Introduction |

## 11. 原始资料链接

- 会议：ICAACE 2025
- 作者单位：Key Laboratory of Cyberspace Security, Ministry of Education, Zhengzhou, China
- 资助：国家自然科学基金（Nos. 62302520, 62402524）
- 关键工具/框架：PyTorch 1.13.1
- 关键参考模型：ET-BERT, SimCLR, MoCo, BERT

## 12. 后续问题

1. **类别不平衡处理**：如何在半监督框架中更好地处理类别不平衡问题？论文在 ISCX-nonVPN 上暴露了此弱点
2. **MSP 收敛加速**：能否设计更高效的预训练任务替代 MSP，加快收敛速度？
3. **动态交替策略**：当前基于连续 3 epoch 改善的切换策略是否最优？能否设计自适应的交替策略？
4. **更多标注数据**：如果标注数据不限于 8 个恶意软件类别，扩展到更多流量类型后性能如何变化？
5. **时序建模**：引入显式的时序建模（如 temporal attention）是否能进一步提升性能？
6. **大规模部署**：在高速网络环境下（10Gbps+），Transformer Encoder 的推理延迟是否可接受？
7. **与其他预训练方法结合**：能否将 CoMask 的思路与 ET-BERT 等预训练方法结合，进一步提升性能？
8. **增量学习**：面对不断出现的新流量类别，如何在 CoMask 框架下实现增量学习而不遗忘旧类别？

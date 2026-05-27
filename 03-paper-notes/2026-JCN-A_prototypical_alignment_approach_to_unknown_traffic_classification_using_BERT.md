---
type: paper
title_original: "A prototypical alignment approach to unknown traffic classification using BERT"
title_cn: "基于 BERT 的原型对齐未知流量分类方法"
authors: ["Minho Cho", "Yongseok Kwon", "Seyoung Ahn", "Sunwon Kwon", "Sunghyun Cho"]
year: 2026
venue: "Journal of Computer Networks (JCN)"
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-JCN-A_prototypical_alignment_approach_to_unknown_traffic_classification_using_BERT.pdf"
mineru_md: "02-parsed-markdown/2026-JCN-A_prototypical_alignment_approach_to_unknown_traffic_classification_using_BERT.md"
status: processed
reading_level: L2
research_area: ["encrypted traffic classification", "network traffic analysis", "open-world recognition"]
task: ["unknown traffic classification", "fine-grained clustering", "open-world traffic classification"]
method: ["BERT", "prototype learning", "contrastive learning", "semi-supervised learning", "masked token prediction"]
dataset: ["ISCX-VPN", "USTC-TFC"]
code: unknown
relevance: high
created: "2026-05-27"
updated: "2026-05-27"
---

# A prototypical alignment approach to unknown traffic classification using BERT

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | A prototypical alignment approach to unknown traffic classification using BERT |
| 中文标题 | 基于 BERT 的原型对齐未知流量分类方法 |
| 作者 | Minho Cho, Yongseok Kwon, Seyoung Ahn, Sunwon Kwon, Sunghyun Cho |
| 年份 | 2026 |
| 会议/期刊 | Journal of Computer Networks (JCN) |
| 研究方向 | 加密流量分类、开放世界流量识别 |
| 任务类型 | 开放世界场景下的未知流量细粒度分类（unknown traffic fine-grained classification） |
| 方法关键词 | BERT, prototype alignment, contrastive learning, semi-supervised learning, masked token prediction |
| 数据集 | ISCX-VPN（约300K flows, 12类）、USTC-TFC（约480K flows, 20类） |
| 是否开源 | 否（作者未获数据共享权限） |
| PDF | 00-inbox/PDFs/2026-JCN-A_prototypical_alignment_approach_to_unknown_traffic_classification_using_BERT.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-JCN-A_prototypical_alignment_approach_to_unknown_traffic_classification_using_BERT.md |

## 1. 一句话总结

> 提出 UT-PAB 框架，通过 BERT 预训练（SLT + MixTMM）和微调（原型对齐 SUP + 对比学习 SSCT）两个阶段，在开放世界场景下实现未知流量的细粒度分类，在 ISCX-VPN 和 USTC-TFC 数据集上总体准确率比 SOTA 方法提升 10.63%~75.34%。

## 2. 摘要翻译

### 2.1 摘要原文

As encrypted internet traffic continues to increase, classifying previously unseen traffic has become a major challenge in real-world network environments. Traditional traffic classification models are designed for closed-world scenarios and struggle to process novel traffic types. To address this in real-world network environments, coarse-grained classification approaches have been proposed, which assign all unknown traffic to a single "unknown" class. However, this coarse-grained labeling limits the model's ability to perform the fine-grained classification of diverse and encrypted traffic behaviors. To address this, we propose Unknown Traffic Prototypical Alignment Bidirectional encoder representations from transformers (UT-PAB), a semi-supervised learning framework for the fine-grained classification of unknown traffic in open-world scenarios. UT-PAB operates in two phases: (1) a pre-training phase that learns general traffic patterns through supervised and masked token prediction tasks, and (2) a fine-tuning phase that refines representations using contrastive learning and prototype-based supervision. These two phases enable the model to cluster unknown traffic by semantic similarity without relying on protocol-specific features. We evaluated the effectiveness of UT-PAB on two benchmark datasets, ISCX-VPN and USTC-TFC, by comparing it against baseline methods based on clustering and representation learning. We conducted extensive experiments on two benchmark datasets across various unknown traffic ratios and demonstrated that the proposed method outperformed state-of-the-art methods by a minimum of 10.63%p and a maximum of 75.34%p improvement in overall accuracy.

### 2.2 摘要中文翻译

随着加密互联网流量持续增长，对先前未见过的流量进行分类已成为真实网络环境中的主要挑战。传统流量分类模型针对封闭世界场景设计，难以处理新型流量类型。为此，已有研究提出了粗粒度分类方法，将所有未知流量归入单一的"未知"类别。然而，这种粗粒度标注限制了模型对多样化加密流量行为进行细粒度分类的能力。为解决此问题，我们提出了 UT-PAB（Unknown Traffic Prototypical Alignment BERT），一种面向开放世界场景中未知流量细粒度分类的半监督学习框架。UT-PAB 分两个阶段运行：（1）通过监督学习和掩码 token 预测任务学习通用流量模式的预训练阶段；（2）利用对比学习和基于原型的监督来精炼表征的微调阶段。这两个阶段使模型能够根据语义相似性对未知流量进行聚类，而无需依赖协议特定特征。我们在 ISCX-VPN 和 USTC-TFC 两个基准数据集上评估了 UT-PAB 的有效性，并与基于聚类和表征学习的基线方法进行了对比。大量实验结果表明，所提方法在不同未知流量比例下的总体准确率比最先进方法至少提升 10.63%，最高提升 75.34%。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 现实网络环境中加密流量持续增长，传统 DPI 方法失效，需要基于 payload 内容的流量分类新范式
- 已有的机器学习分类方法多为封闭世界设计，遇到未知流量时会将其误分类为已知类别，带来安全隐患
- 现有开放世界方法大多只做粗粒度分类（将所有未知流量归为单一"未知"类），无法对未知流量进行细粒度区分，限制了网络管理和安全响应能力
- 已有的细粒度方法（如 K-Means、DBSCAN、representation learning + clustering）仅停留在对模型输出表征的聚类上，无法学习更精细的未知流量表征

### 3.2 现有方法的痛点和不足

| 现有方法 | 痛点 |
|---|---|
| DPI-based methods | 对加密流量无效 |
| 粗粒度 unknown classification（boundary-setting / threshold-based） | 将所有未知流量归为单一类别，无法进行细粒度区分 |
| 传统聚类（K-Means, DBSCAN, AutoClass） | 依赖字节级相似性或统计特征，面对复杂多样流量模式时表现差 |
| Representation learning + clustering（SEEN, Velatin 等） | 仅对模型输出表征做聚类，固定了未知类的决策边界，无法学习更精细的表征 |
| FEAC（Word2Vec + Autoencoder） | 基于协议规范结构特征，对加密流量效果差 |
| MFD&DBSCAN | 基于协议消息格式相似性，加密场景下特征提取困难 |

### 3.3 论文的研究假设或核心直觉

- **核心假设**：通过将监督学习（已知流量模式）和自监督学习（通用字节级依赖关系）结合预训练，再通过原型对齐和对比学习微调，可以在表征空间中为未知流量形成清晰的聚类边界
- **关键直觉**：
  - 预训练阶段的 SLT 任务学习已知流量的判别性模式，建立决策边界参考
  - MixTMM 任务通过掩码 token 预测学习字节级依赖关系，避免过拟合到已知模式
  - 微调阶段的 SUP 通过原型伪标签对未知流量进行细粒度聚类
  - SSCT 通过对比学习增强原型内聚性、拉开原型间距离，形成清晰稳定的聚类边界

## 4. 方法设计

### 4.1 方法整体流程

1. **数据预处理**：从 PCAP 文件中提取会话级流，去除 Ethernet/IP 头部和五元组信息，使用 byte-level bi-gram tokenizer 将 payload 转为 token 序列，加入 token embedding 和 position embedding
2. **预训练阶段**：同时使用有标签数据（SLT 任务）和无标签数据（MixTMM 任务）联合训练，学习通用流量表征
3. **微调阶段**：在无标签数据上构建原型聚类（SUP），通过对比学习增强表征一致性（SSCT），同时保留 SLT 监督信号
4. **Cluster Matching**：使用 Hungarian 算法将预测聚类与真实标签对齐，区分已知和未知流量

### 4.2 详细 Pipeline（表格形式）

| 步骤 | 描述 | 技术细节 |
|---|---|---|
| 1. 数据预处理 | 从 PCAP 提取会话流，去除标识信息 | 移除 Ethernet/IP 头部和源/目的端口号，仅保留 payload |
| 2. Token 化 | Byte-level bi-gram tokenizer | 65536 个 bi-gram token + 5 个特殊 token ([CLS], [PAD], [SEP], [UNK], [MASK])，最大序列长度 128 |
| 3. Embedding | Token Embedding + Position Embedding | 位置索引 0-127，两者相加得到最终输入 embedding |
| 4. 预训练 SLT | 有标签已知流量的监督分类 | [CLS] token 通过分类层预测类别，CE loss |
| 5. 预训练 MixTMM | 无标签数据的掩码 token 预测 | 随机掩码 15% 的 token，预测原始 token，CE loss |
| 6. 联合预训练优化 | L_Pre = L_SLT + L_MixTMM | AdamW optimizer，学习率 5e-5，10 epochs |
| 7. 微调 SUP | 原型伪标签监督 | K-Means 聚类提取原型，分配伪标签，CE loss |
| 8. 微调 SSCT | 对比学习增强一致性 | 15% 掩码生成增强样本，计算 original-augmented 对的 cosine similarity，InfoNCE loss |
| 9. 微调联合优化 | L_Fine = L_SUP + alpha*L_SSCT + beta*L_SLT | alpha=0.05, beta=100, tau=0.05，学习率 1e-5 |
| 10. Cluster Matching | 聚类与真实标签对齐 | Hungarian 算法最大化匹配准确率，聚类数 K 通过 DBI + Max-ACC 方法估计 |

### 4.3 模型结构或系统模块（表格形式）

| 模块 | 功能 | 输入 | 输出 |
|---|---|---|---|
| Data Preprocessing | PCAP 到 token 序列的转换 | PCAP 文件 | bi-gram token 序列 + position embedding |
| Token Embedding Layer | 将 bi-gram token 映射为向量 | token 序列 | token embedding 向量 |
| Transformer Encoder (ET-BERT backbone) | 编码上下文表征 | 输入 embedding | [CLS] 和各 token 的上下文表征 |
| SLT Classifier | 已知流量分类 | [CLS] 表征 | 类别概率分布 |
| MixTMM Predictor | 预测被掩码的 token | masked token 位置的表征 | token 预测概率分布 |
| Prototype Generator (K-Means) | 构建未知流量的原型聚类 | 无标签数据的特征表征 | 聚类原型 {mu_1, mu_2, ..., mu_k} |
| Contrastive Learning Module | 增强表征一致性 | original + augmented 样本 | 对比学习 loss |
| Cluster Matcher (Hungarian) | 聚类与真实标签对齐 | 混淆矩阵 | 最优一一映射 |

### 4.4 公式、算法和机制解释

**SLT Loss（监督已知流量分类）**：

$$L_{SLT} = -\sum_{y_i \in \mathcal{Y}_L} y_i \log P(y_i | X_i; \theta)$$

使用标准 Cross-Entropy loss，通过 [CLS] token 的表征预测已知流量类别标签，建立决策边界。

**MixTMM Loss（掩码 token 预测）**：

$$L_{MixTMM} = -\sum_{i=1}^{m} \log P(t_i = token_i | \tilde{X}_i; \theta)$$

随机选择 15% 的 token 替换为 [MASK]，训练模型预测原始 token，学习字节级依赖关系。15% 的掩码率经消融实验验证为最优（低于 10% 学习信号不足，高于 20% 上下文信息损失过大）。

**预训练联合优化**：

$$L_{Pre} = L_{SLT} + L_{MixTMM}$$

SLT 学习判别性模式，MixTMM 学习通用表征，两者互补防止过拟合到已知模式。

**SUP Loss（原型伪标签监督）**：

$$L_{SUP} = -\sum_{X_i^U \in \mathcal{X}} \tilde{y}_i \log P(\hat{y}_i | X_i^U; \theta)$$

对无标签数据用 K-Means 聚类分配伪标签，然后用 CE loss 进行监督学习，实现未知流量的细粒度分类。聚类数 K 通过 Davies-Bouldin Index (DBI) 最小化自动确定。

**SSCT Loss（自监督对比学习）**：

$$L_{SSCT} = -\sum_{X_i \in T^U} \log \frac{\exp(\text{sim}(X_i, X_i') / \tau)}{\sum_{j=1}^{2B} \exp(\text{sim}(X_i, X_j') / \tau)}$$

其中 sim 为 cosine similarity，tau 为温度参数。将无标签数据的 15% token 替换为随机 token 生成增强样本，使同一数据的原始和增强版本表征相近，不同数据的表征相远。

**微调联合优化**：

$$L_{Fine} = L_{SUP} + \alpha L_{SSCT} + \beta L_{SLT}$$

alpha=0.05（SSCT 权重）、beta=100（SLT 权重）、tau=0.05（温度）。

**Cluster Matching（Hungarian 算法）**：

$$\max_{\pi} \sum_{i=1}^{G} C_{i, \pi(i)}$$

在混淆矩阵 C 上找到预测聚类与真实标签的最优一一映射，最大化匹配准确率。

**关键机制解释**：
- **ET-BERT backbone**：使用预训练的 Encrypted Traffic BERT 模型作为骨干网络，仅微调最后 4 层 Transformer 参数
- **Byte-level bi-gram tokenizer**：将连续两个字节作为一个 token（共 65536 种），捕获相邻字节对关系
- **五元组去除**：移除 Ethernet/IP 头部和端口号，防止模型依赖流标识信息而非 payload 内在特征
- **Max-ACC 聚类数估计**：在有标签子集上搜索不同 K 值的 K-Means 聚类准确率，选择最大化的 K

### 4.5 方法优势

1. **细粒度未知流量分类**：不同于粗粒度方法将所有未知流量归为单一类别，UT-PAB 能将未知流量按语义相似性聚类为多个子类
2. **两阶段互补设计**：预训练同时学习判别性模式（SLT）和通用表征（MixTMM），微调通过原型对齐和对比学习进一步精炼
3. **对加密流量有效**：基于 payload 字节级表征，无需依赖可读的协议字段
4. **去除标识偏差**：移除五元组和头部信息，模型学习 payload 内在模式而非流标识
5. **自动聚类数估计**：通过 DBI + Max-ACC 方法自动确定聚类数，无需人工设定
6. **强大的泛化能力**：在 VPN 与非 VPN 合并的泛化实验中仍显著优于 baseline

### 4.6 方法不足

1. **已知流量分类准确率相对较低**：由于聚类过程的固有特性，已知类的分类准确率低于部分 SOTA 方法（如 Velatin）
2. **计算资源需求大**：需要 GPU 支持，模型参数量 62.6M，主要面向服务器级部署
3. **聚类模糊性**：功能相似的类别（如 Stream 和 VoIP、MySQL 和 Virut/Zeus）容易混淆
4. **数据不可共享**：作者未获数据共享权限，复现可能受限
5. **对动态流量模式的挑战**：如 Cridex 恶意软件产生多样化动态流量模式，难以有效聚类

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 对比维度 | 粗粒度方法 | 传统聚类+表征学习 | UT-PAB（本文） |
|---|---|---|---|
| 分类粒度 | 粗粒度（单一"未知"类） | 粗到中等粒度 | 细粒度（未知流量多子类） |
| 已知/未知区分 | 是 | 是 | 是 + 未知流量内部细分 |
| 表征学习 | 无或简单 | 有但仅聚类输出 | 双阶段深度表征学习 |
| 决策边界 | 固定边界或阈值 | 固定聚类边界 | 动态原型对齐 + 对比学习平滑边界 |
| 预训练策略 | 无 | 无或简单 | SLT + MixTMM 双任务预训练 |
| 对未知流量的处理 | 归为单一类 | 聚类但效果有限 | 原型对齐 + 对比学习增强聚类 |

与已有方法的本质区别：UT-PAB 不仅仅是"训练模型 + 聚类输出"，而是通过专门设计的预训练和微调策略，在表征空间中为未知流量动态构建结构化聚类。

### 5.2 创新点分析（表格形式）

| 创新点 | 说明 |
|---|---|
| UT-PAB 框架 | 首个结合 BERT 预训练与原型对齐的未知流量细粒度分类框架 |
| SLT + MixTMM 双任务预训练 | 监督学习捕获已知模式 + 掩码预测学习通用表征，互补防止过拟合 |
| SUP 原型伪标签 | 基于 K-Means 构建原型聚类，为无标签数据生成伪标签进行监督学习 |
| SSCT 对比学习 | 通过掩码增强的对比学习增强原型内聚性、拉大原型间距离 |
| 联合优化策略 | 预训练和微调阶段各自的联合损失函数设计，平衡多种学习目标 |
| 去除五元组偏差 | 系统性去除头部和端口信息，确保模型基于 payload 内在特征分类 |

### 5.3 适用场景

- 企业网络安全：识别和分类网络中出现的新型未知应用或恶意流量
- 加密流量管理：在 VPN 或 TLS 加密环境下进行应用识别
- 恶意软件检测：发现和聚类新型恶意软件产生的流量模式
- 网络运维：对网络中未注册或未分类的应用流量进行自动化归类
- ISP 服务质量管理：识别新型应用以提供差异化 QoS

### 5.4 方法对比表

| 方法 | 预训练 | 微调 | 聚类策略 | 已知准确率 | 未知准确率 | H-score |
|---|---|---|---|---|---|---|
| K-Means | 无 | 无 | 原始字节聚类 | 低 | 低 | 低 |
| MFD&DBSCAN | 无 | 无 | 格式距离+DBSCAN | ~18% | ~22% | ~17 |
| FEAC | 无 | 无 | Word2Vec+AE+聚类 | ~31% | ~29% | ~25 |
| SEEN | 无 | 对比学习 | Siamese CNN+聚类 | ~94% | ~58% | ~72 |
| Velatin | 无 | 监督学习 | BiLSTM+CNN+聚类 | ~98% | ~56% | ~73 |
| **UT-PAB** | **SLT+MixTMM** | **SUP+SSCT+SLT** | **原型对齐+对比学习** | **~89%** | **~87%** | **~87** |

注：以上数据为 ISCX-VPN 数据集 Scenario V-b (UR=25%) 下的近似平均值。

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **硬件环境**：Ubuntu 22.04, NVIDIA GeForce RTX A5000 GPU
- **软件环境**：PyTorch 1.11.0, Python 3.8.19
- **骨干模型**：预训练 ET-BERT（Encrypted Traffic BERT），仅微调最后 4 层 Transformer
- **优化器**：AdamW，预训练学习率 5e-5，微调学习率 1e-5
- **训练轮次**：预训练和微调各 10 epochs
- **数据划分**：训练:验证:测试 = 8:1:1
- **标签比例**：有标签数据占已知类的 20%
- **每个类最大样本数**：2500 flows（不足则使用全部）
- **评估方式**：每个场景随机选择未知类运行 5 次，报告均值和标准差

### 6.2 数据集

| 数据集 | 总流数 | 类别数 | 类型 | 场景设置 |
|---|---|---|---|---|
| ISCX-VPN | ~300K | 12（6 VPN + 6 非 VPN） | 加密 VPN 流量 | V-a(10 known+2 unknown, UR=15%), V-b(9+3, UR=25%), V-c(8+4, UR=35%) |
| USTC-TFC | ~480K | 20（10 良性 + 10 恶意） | 恶意软件+良性流量 | U-a(17+3, UR=15%), U-b(15+5, UR=25%), U-c(13+7, UR=35%) |

ISCX-VPN 包含 Chat, Email, FT, P2P, Stream, VoIP 及其 VPN 版本。USTC-TFC 包含 Bittorrent, Cridex, Facetime, Ftp, Gmail, MySQL 等良性和恶意流量类别。

### 6.3 Baseline

| Baseline | 方法描述 |
|---|---|
| K-Means | 直接对原始字节级流量数据做 K-Means 聚类 |
| MFD&DBSCAN | 基于 token 格式距离和消息格式距离计算包相似性，用 DBSCAN 聚类 |
| FEAC | Word2Vec 提取协议规范表征 + Autoencoder 降维 + 聚类 |
| SEEN | Siamese Network（1D-CNN）+ 对比损失学习表征 + 聚类 |
| Velatin | BiLSTM + CNN 特征提取 + 树形分类器 + 决策边界 |

### 6.4 评价指标

- **Accuracy (ACC)**：预测标签与真实标签匹配的比例
- **Known Accuracy**：已知类别的分类准确率
- **Unknown Accuracy**：未知类别的分类准确率
- **H-score**：已知和未知准确率的调和平均，避免对某一类偏向

$$H\text{-}score = \frac{2 \cdot ACC_{known} \cdot ACC_{unknown}}{ACC_{known} + ACC_{unknown}}$$

### 6.5 关键实验结果（表格形式）

**ISCX-VPN 数据集：**

| 方法 | V-a H-score | V-a Known | V-a Unknown | V-b H-score | V-b Known | V-b Unknown | V-c H-score | V-c Known | V-c Unknown |
|---|---|---|---|---|---|---|---|---|---|
| K-Means | 18.26 | 21.08% | 22.20% | 20.24 | 20.40% | 23.87% | 19.20 | 23.85% | 16.10% |
| MFD&DBSCAN | 13.46 | 15.83% | 26.55% | 16.75 | 15.45% | 25.25% | 15.17 | 18.07% | 17.56% |
| FEAC | 15.49 | 36.81% | 11.02% | 31.96 | 32.87% | 31.43% | 29.39 | 33.48% | 30.58% |
| SEEN | 73.24 | 93.22% | 60.84% | 72.91 | 94.92% | 59.52% | 60.53 | 94.66% | 44.60% |
| Velatin | 79.83 | 98.21% | 67.83% | 79.63 | 98.63% | 72.31% | 71.52 | 98.29% | 56.82% |
| **UT-PAB** | **94.77** | 91.40% | **98.42%** | **91.46** | 92.55% | **90.97%** | **85.17** | 84.60% | **86.38%** |

**USTC-TFC 数据集：**

| 方法 | U-a H-score | U-a Known | U-a Unknown | U-b H-score | U-b Known | U-b Unknown | U-c H-score | U-c Known | U-c Unknown |
|---|---|---|---|---|---|---|---|---|---|
| K-Means | 38.94 | 41.66% | 40.05% | 41.29 | 41.68% | 42.48% | 38.98 | 45.34% | 35.82% |
| MFD&DBSCAN | 16.82 | 22.72% | 15.23% | 20.93 | 19.69% | 28.75% | 21.13 | 20.46% | 23.89% |
| FEAC | 25.39 | 31.20% | 25.68% | 31.16 | 28.75% | 35.23% | 29.83 | 28.27% | 34.27% |
| SEEN | 76.12 | 94.54% | 63.76% | 72.86 | 96.69% | 58.90% | 68.76 | 95.38% | 53.80% |
| Velatin | 77.43 | 98.46% | 63.83% | 70.78 | 98.92% | 55.22% | 69.22 | 99.34% | 53.19% |
| **UT-PAB** | **87.04** | 87.72% | **86.89%** | **84.16** | 81.94% | **86.81%** | **78.42** | 81.71% | **75.96%** |

**消融实验（Scenario V-b）：**

| 配置 | P-SLT | MixTMM | SUP | F-SLT | SSCT | H-score | Known | Unknown |
|---|---|---|---|---|---|---|---|---|
| (1) 无预训练 | - | - | - | - | - | 21.56 | 25.40% | 18.72% |
| (2) 仅 MixTMM | - | Yes | - | - | - | 27.22 | 26.00% | 29.58% |
| (3) 仅 SLT | Yes | - | - | - | - | 75.53 | 87.20% | 67.27% |
| (4) SLT+MixTMM | Yes | Yes | - | - | - | 78.01 | 86.53% | 73.55% |
| (5) 去 F-SLT | Yes | Yes | Yes | - | Yes | 80.16 | 86.40% | 79.63% |
| (6) 去 SUP | Yes | Yes | - | Yes | Yes | 81.91 | 88.88% | 78.02% |
| (7) 去 SSCT | Yes | Yes | Yes | Yes | - | 83.67 | 91.83% | 77.81% |
| (8) 完整模型 | Yes | Yes | Yes | Yes | Yes | **91.46** | 92.55% | 90.97% |

**泛化实验（ISCX-VPN 6 类合并，UR=35%）：**

| 方法 | H-score | Known (%) | Unknown (%) |
|---|---|---|---|
| SEEN | 65.73 | 77.20% | 58.88% |
| Velatin | 75.81 | 96.71% | 62.60% |
| **UT-PAB** | **85.22** | 92.04% | **81.06%** |

**模型复杂度对比：**

| 模型 | 参数量 (M) | 推理时间 (ms) |
|---|---|---|
| MFD&DBSCAN | - | 0.18 |
| FEAC | 48.8 | 1.04 |
| SEEN | 70.18 | 0.47 |
| Velatin | 5.9 | 0.50 |
| **UT-PAB** | 62.6 | 0.56 |

### 6.6 优势最明显的场景

- **未知流量分类**：UT-PAB 在未知流量准确率上大幅领先所有 baseline，在 ISCX-VPN 上最高达 98.42%，在 USTC-TFC 上最高达 86.89%
- **高未知比例场景**：当 UR 从 15% 增加到 35% 时，UT-PAB 的性能下降相对较小，表现出较强的鲁棒性
- **H-score 综合表现**：在所有 6 个场景中均取得最高 H-score，说明在已知和未知流量之间取得了良好平衡
- **t-SNE 可视化**：UT-PAB 的表征空间对已知和未知类均呈现清晰的聚类分离，而 baseline 方法的未知类表征散布混杂

### 6.7 局限性

1. **已知类准确率相对较低**：在部分场景中低于 Velatin 和 SEEN，因为聚类过程中已知类也可能被错误聚类到其他簇
2. **聚类模糊性问题**：功能相似的类别（如 Stream/VoIP、MySQL/Virut/Zeus）容易混淆
3. **计算资源需求**：62.6M 参数，需要 GPU 支持，不适合边缘设备部署
4. **推理吞吐量**：单 GPU 约 1844 flows/sec，估算网络吞吐量约 1.33 Gb/s，高速网络场景可能不足
5. **数据不可共享限制**：作者声明无数据共享权限
6. **Cridex 等动态恶意流量**：产生多样化动态模式的恶意软件流量难以有效聚类（准确率低于 60%）

## 7. 学习与应用

### 7.1 是否开源？

否。作者声明 "The authors do not have permission to share data"。论文未提供代码仓库链接。

### 7.2 复现关键步骤

1. **数据准备**：下载 ISCX-VPN 和 USTC-TFC 数据集，提取会话级流，去除 Ethernet/IP 头部和端口号
2. **Token 化**：使用 byte-level bi-gram tokenizer 构建 65536 词表，最大序列长度 128，添加 [CLS]/[SEP]/[PAD] 特殊 token
3. **预训练**：加载 ET-BERT 预训练权重，使用 SLT（有标签数据 CE loss）+ MixTMM（无标签数据 15% 掩码预测 loss）联合训练 10 epochs，学习率 5e-5
4. **微调**：用预训练模型提取无标签数据特征，K-Means 聚类生成伪标签（聚类数通过 DBI 最小化确定），联合优化 SUP + SSCT (alpha=0.05, tau=0.05) + SLT (beta=100)，学习率 1e-5
5. **评估**：用 Hungarian 算法将预测聚类与真实标签对齐，计算 H-score 和各类准确率

### 7.3 关键超参数、预处理和训练细节

| 参数 | 值/说明 |
|---|---|
| Backbone | 预训练 ET-BERT，仅微调最后 4 层 Transformer |
| Tokenizer | Byte-level bi-gram，65536 token + 5 special tokens |
| 最大序列长度 | 128 tokens |
| 预训练学习率 | 5e-5 |
| 微调学习率 | 1e-5 |
| 优化器 | AdamW |
| 训练轮次 | 预训练 10 epochs，微调 10 epochs |
| MixTMM 掩码比例 | 15%（最优，消融实验验证） |
| alpha（SSCT 权重） | 0.05 |
| beta（SLT 权重） | 100 |
| tau（SSCT 温度） | 0.05 |
| 聚类数 K | 通过 DBI + Max-ACC 自动估计 |
| 数据划分 | 训练:验证:测试 = 8:1:1 |
| 标签比例 | 已知类的 20% |
| 每类最大样本数 | 2500 flows |
| SSCT 增强方式 | 随机掩码 15% token 替换为随机 token |

### 7.4 能否迁移到其他任务？

- **其他加密协议分类**：ET-BERT backbone 已在多种加密流量上预训练，可直接迁移到其他加密流量分类任务
- **恶意软件家族分类**：USTC-TFC 实验已展示对恶意软件流量的分类能力，可扩展到更多恶意软件家族
- **入侵检测**：未知流量聚类能力可辅助发现新型攻击模式
- **DNS 隧道检测 / 协议隧道检测**：核心的"已知模式学习 + 未知异常发现"思路可迁移
- **IoT 设备识别**：不同 IoT 设备的流量模式可类比为不同的"应用类别"
- **网站指纹识别**：将网站访问流量视为不同的流量类别，利用细粒度分类能力

### 7.5 对我的研究有什么启发？

1. **开放世界思维**：真实网络环境中未知流量不可避免，应将 open-world 问题纳入研究设计
2. **双阶段学习框架**：预训练学习通用表征 + 微调适配特定任务的框架在流量分类中非常有效
3. **去除标识偏差**：去除五元组和头部信息是避免模型捷径学习的重要预处理步骤
4. **原型学习范式**：Prototype-based pseudo-labeling 是处理无标签数据的有效方式，可替代简单的聚类
5. **对比学习增强聚类**：SSCT 通过对比学习平滑聚类边界的思路，适用于任何需要增强聚类质量的场景
6. **消融实验设计**：论文的消融实验清晰展示了每个组件的贡献，是很好的实验设计参考
7. **H-score 评价指标**：调和平均可以平衡已知和未知类的评估，避免偏向某一类

## 8. 总结

### 8.1 核心思想（不超过20字）

BERT预训练+原型对齐实现未知流量细粒度分类。

### 8.2 速记版 Pipeline（3-5步）

1. 去标识预处理：移除头部和五元组，byte-level bi-gam tokenize
2. 双任务预训练：SLT（监督已知分类）+ MixTMM（掩码token预测），学习通用表征
3. 原型微调：K-Means聚类生成伪标签（SUP）+ 对比学习平滑边界（SSCT）+ SLT保持已知知识
4. Cluster Matching：Hungarian算法对齐预测聚类与真实标签
5. 评估：H-score衡量已知和未知分类的综合表现

## 9. Obsidian 知识链接

### 9.1 相关概念

- Encrypted Traffic Classification - 加密流量分类
- Open-World Recognition - 开放世界识别
- Unknown Traffic Classification - 未知流量分类
- Prototype Learning - 原型学习
- Contrastive Learning - 对比学习
- Semi-Supervised Learning - 半监督学习
- Bidirectional Encoder Representations from Transformers (BERT) - BERT 模型
- ET-BERT - 加密流量 BERT 预训练模型

### 9.2 相关方法

- K-Means Clustering - K-Means 聚类
- DBSCAN - 基于密度的聚类
- Hungarian Algorithm - 匈牙利算法
- InfoNCE Loss - 对比学习损失函数
- Masked Language Model (MLM) - 掩码语言模型
- Davies-Bouldin Index - 聚类质量评估指标
- Siamese Network - 孪生网络（SEEN baseline）
- Bi-LSTM - 双向 LSTM（Velatin baseline）

### 9.3 相关任务

- Fine-Grained Traffic Classification - 细粒度流量分类
- Malware Traffic Detection - 恶意软件流量检测
- VPN Traffic Classification - VPN 流量分类
- Application Identification - 应用识别
- Zero-Day Traffic Detection - 零日流量检测
- Network Anomaly Detection - 网络异常检测

### 9.4 可更新的综述页面

- Encrypted Traffic Classification Survey
- Open-World Traffic Classification Methods
- Deep Learning for Network Traffic Analysis
### 9.5 可加入的对比表

- Open-World Traffic Classification Methods Comparison
- Encrypted Traffic Classification Methods
- BERT-based Traffic Analysis Methods
## 10. 证据记录（表格形式）

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E1 | 实验结果 | ISCX-VPN Scenario V-a: UT-PAB H-score 94.77, 远超 Velatin 79.83 和 SEEN 73.24 | Table 3 |
| E2 | 实验结果 | ISCX-VPN Scenario V-b: UT-PAB H-score 91.46, Unknown accuracy 90.97% | Table 3 |
| E3 | 实验结果 | USTC-TFC Scenario U-a: UT-PAB H-score 87.04, Unknown accuracy 86.89% | Table 4 |
| E4 | 实验结果 | 消融实验: 去掉 SLT 后 H-score 从 91.46 降至 80.16（-11.3），SLT 最关键 | Table 5 |
| E5 | 实验结果 | 消融实验: 去掉 SUP 后 H-score 降至 81.91（-9.55），去掉 SSCT 降至 83.67（-7.79） | Table 5 |
| E6 | 实验结果 | 泛化实验（VPN/非VPN合并6类）: UT-PAB H-score 85.22, 超 Velatin 75.81 和 SEEN 65.73 | Table 6 |
| E7 | 模型复杂度 | UT-PAB 参数量 62.6M, 推理时间 0.56ms, 吞吐量约 1844 flows/sec (1.33 Gb/s) | Table 7 |
| E8 | 消融实验 | MixTMM 掩码率 15% 最优，10% 学习信号不足，20% 上下文损失过大 | Table A.1 |
| E9 | 聚类数估计 | ISCX-VPN 真实 12 类，估计 12.8，误差 6.66%；USTC-TFC 真实 20 类，估计 20.8，误差 4% | Table B.1 |
| E10 | 参数调优 | alpha=0.05（H-score最高95.7），beta=100，tau=0.05（H-score最高） | Section 4.2.3, Fig.4 |
| E11 | 可视化 | t-SNE 显示 UT-PAB 对已知和未知类均形成清晰聚类分离，baseline 未知类表征混杂 | Fig.5 |
| E12 | 混淆矩阵 | Stream 和 VoIP 混淆 12.68%（因实时性特征相似）；MySQL 被误分为 Virut/Zeus（因查询-响应模式重叠） | Fig.6 |

## 11. 原始资料链接

- 期刊：Journal of Computer Networks (JCN), Elsevier
- 作者单位：Department of Computer Science and Engineering, Hanyang University, Ansan-si, Gyeonggi-do, South Korea
- 骨干模型：ET-BERT (Encrypted Traffic BERT) [Lin et al., ACM Web Conference 2022]
- 数据集：ISCX-VPN (Canadian Cyber Security Research Center), USTC-TFC
- 资助：Korea Research Institute for defense Technology planning and advancement (KRIT), Korea government DAPA (No. KRIT-CT-22-021)
- 关键依赖库：PyTorch 1.11.0, AdamW optimizer

## 12. 后续问题

1. **已知类准确率提升**：论文已指出这是主要局限，未来可探索 cluster-aware 目标（如 center separation loss、compactness loss）或自适应聚类技术
2. **动态聚类数估计**：当前使用 Max-ACC 需要在有标签子集上搜索，是否可以设计更高效的在线聚类数估计方法？
3. **轻量化部署**：62.6M 参数量较大，是否可以通过知识蒸馏或模型压缩实现在边缘设备上的部署？
4. **对抗性攻击**：如果攻击者故意模仿已知流量的字节模式，原型对齐方法是否仍然有效？
5. **持续学习**：当新的流量类别被识别并标注后，如何增量更新模型而不遗忘已有知识？
6. **聚类模糊性的根本解决**：功能相似的类别（Stream/VoIP、MySQL/Virut）混淆是表征空间的固有局限还是可以通过更好的特征工程解决？
7. **与其他预训练模型的对比**：与更近期的流量预训练模型（如 YaTC、Trafformer）相比，ET-BERT backbone 的优劣如何？
8. **实时流分类**：当前方法需要完整流的 payload，是否可以实现逐包或前 N 包的实时未知流量分类？

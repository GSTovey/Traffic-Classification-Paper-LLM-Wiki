---
type: paper
title_original: "Bottom Aggregating, Top Separating: An Aggregator and Separator Network for Encrypted Traffic Understanding"
title_cn: "底部聚合、顶部分离：用于加密流量理解的聚合器与分离器网络"
authors:
  - Wei Peng
  - Lei Cui
  - Wei Cai
  - Wei Wang
  - Xiaoyu Cui
  - Zhiyu Hao
  - Xiaochun Yun
year: 2025
venue: IEEE Transactions on Information Forensics and Security (TIFS)
doi: "10.1109/TIFS.2025.3529316"
url: unknown
pdf: "../00-inbox/PDFs/2025-TIFS-Bottom_Aggregating_Top_Separating_An_Aggregator_and_Separator_Network_for_Encrypted_Traffic_Understanding.pdf"
mineru_md: "../02-parsed-markdown/2025-TIFS-Bottom_Aggregating_Top_Separating_An_Aggregator_and_Separator_Network_for_Encrypted_Traffic_Understanding.md"
status: processed
reading_level: L2
research_area:
  - encrypted traffic classification
  - pre-trained language model
  - prompt learning
  - word sense aggregating
  - semantic separating
task:
  - VPN classification
  - application classification
  - malware detection
  - IoT attack detection
  - Tor service classification
method:
  - Word Sense Aggregator (WSA)
  - Category-constrained Semantic Separator (CSS)
  - Task-aware Prompts
  - BERT Encoder
  - Parameter-free Aggregation
dataset:
  - ISCXVPN
  - USTC-TFC
  - CICIoT
  - ISCXTor
  - CHNAPP (real-world)
code: "https://github.com/pengwei-iie/ASNET"
relevance: high
created: 2026-06-09
updated: 2026-06-09
---

# Bottom Aggregating, Top Separating: An Aggregator and Separator Network for Encrypted Traffic Understanding

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Bottom Aggregating, Top Separating: An Aggregator and Separator Network for Encrypted Traffic Understanding |
| 中文标题 | 底部聚合、顶部分离：用于加密流量理解的聚合器与分离器网络 |
| 作者 | Wei Peng, Lei Cui, Wei Cai, Wei Wang, Xiaoyu Cui, Zhiyu Hao, Xiaochun Yun |
| 年份 | 2025 |
| 会议/期刊 | IEEE Transactions on Information Forensics and Security (TIFS) |
| 研究方向 | 加密流量分类、预训练语言模型、提示学习、词义聚合、语义分离 |
| 任务类型 | VPN 分类、应用分类、恶意软件检测、IoT 攻击检测、Tor 服务分类 |
| 方法关键词 | WSA, CSS, Task-aware Prompts, BERT, Parameter-free Aggregation |
| 数据集 | ISCXVPN, USTC-TFC, CICIoT, ISCXTor, CHNAPP (real-world) |
| 是否开源 | 是（https://github.com/pengwei-iie/ASNET） |
| PDF | `../00-inbox/PDFs/2025-TIFS-Bottom_Aggregating_Top_Separating_An_Aggregator_and_Separator_Network_for_Encrypted_Traffic_Understanding.pdf` |
| MinerU Markdown | `../02-parsed-markdown/2025-TIFS-Bottom_Aggregating_Top_Separating_An_Aggregator_and_Separator_Network_for_Encrypted_Traffic_Understanding.md` |

---

## 1. 一句话总结

> 提出 ASNet，通过底部无参数词义聚合器（WSA）使 BERT 快速适配流量数据并保持完整词义，顶部类别约束语义分离器（CSS）配合任务感知提示将 packet 级语义显式分离到不同类别的语义空间，无需预训练即在 5 个数据集 7 个任务上达到 SOTA。

---

## 2. 摘要翻译

### 2.1 摘要原文

Encrypted traffic classification refers to the task of identifying the application, service or malware associated with network traffic that is encrypted. Previous methods mainly have two weaknesses. Firstly, from the perspective of word-level (namely, byte-level) semantics, current methods use pre-training language models like BERT, learned general natural language knowledge, to directly process byte-based traffic data. However, understanding traffic data is different from understanding words in natural language, using BERT directly on traffic data could disrupt internal word sense information so as to affect the performance of classification. Secondly, from the perspective of packet-level semantics, current methods mostly implicitly classify traffic using abstractive semantic features learned at the top layer, without further explicitly separating the features into different space of categories, leading to poor feature discriminability. In this paper, we propose a simple but effective Aggregator and Separator Network (ASNet) for encrypted traffic understanding, which consists of two core modules. Specifically, a parameter-free word sense aggregator enables BERT to rapidly adapt to understanding traffic data and keeping the complete word sense without introducing additional model parameters. And a category-constrained semantics separator with task-aware prompts (as the stimulus) is introduced to explicitly conduct feature learning independently in semantic spaces of different categories. Experiments on five datasets across seven tasks demonstrate that our proposed model achieves the current state-of-the-art results without pre-training in both the public benchmark and real-world collected traffic dataset. Statistical analyses and visualization experiments also validate the interpretability of the core modules. Furthermore, what is important is that ASNet does not need pre-training, which dramatically reduces the cost of computing power and time.

### 2.2 摘要中文翻译

加密流量分类是指识别与加密网络流量相关的应用、服务或恶意软件的任务。现有方法主要有两个弱点。首先，从词级别（即字节级别）语义角度，当前方法使用 BERT 等预训练语言模型直接处理基于字节的流量数据。然而，理解流量数据不同于理解自然语言中的词汇，直接在流量数据上使用 BERT 可能破坏内部词义信息，影响分类性能。其次，从 packet 级别语义角度，当前方法大多使用顶层学习的抽象语义特征隐式分类流量，未进一步将特征显式分离到不同类别的语义空间，导致特征区分度差。本文提出简单但有效的聚合器与分离器网络（ASNet），包含两个核心模块：无参数词义聚合器使 BERT 快速适配流量数据理解并保持完整词义，无需引入额外模型参数；类别约束语义分离器配合任务感知提示（作为刺激）显式地在不同类别的语义空间中独立进行特征学习。在 5 个数据集 7 个任务上的实验表明，ASNet 无需预训练即在公开基准和真实流量数据集上达到 SOTA。统计分析和可视化实验验证了核心模块的有效性和可解释性。重要的是，ASNet 不需要预训练，大幅降低了算力和时间成本。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

现有基于 PLM 的加密流量分类方法存在两个核心问题：(1) BERT 的 WordPiece tokenizer 会破坏流量字节的完整词义（如将 "xde" 拆分为 ["x", "##d", "##e"]）；(2) 现有方法使用顶层抽象语义特征隐式分类，未显式分离不同类别的语义空间，导致特征区分度差。

### 3.2 现有方法的痛点和不足

1. **直接使用 BERT**：WordPiece tokenizer 将流量字节拆分为子词，破坏完整词义信息
2. **ET-BERT**：需要大规模数据和计算资源从头预训练，无法利用 BERT 已学到的通用语言知识
3. **YaTC**：将流量数据 patch 化后用 MAE 预训练，同样需要大量计算资源
4. **通用问题**：现有方法隐式使用顶层特征分类，不同类别的语义特征混杂在同一空间

### 3.3 论文的研究假设或核心直觉

流量数据的字节（如 "\x17"）应被视为完整的词义单元，而非被拆分为子词。通过无参数聚合恢复完整词义，配合任务感知提示将不同类别的语义显式分离到独立空间，能显著提升分类性能，且无需预训练。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | BERT 的 WordPiece tokenizer 将 "xde" 拆分为 ["x", "##d", "##e"] | §I |
| 痛点提炼 | 拆分破坏流量字节的完整词义，影响分类性能 | §I, §II-A |
| 问题转化 | 如何在不重新预训练的情况下让 BERT 适配流量数据理解 | §I |
| 文献定位 | ET-BERT/YaTC 需要大规模预训练，无法利用 BERT 通用知识 | §II-B |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | WSA 聚合能降低类间高频词重叠，提升区分度 | WordPiece 拆分破坏词义 | 可视化分析（Fig. 4/5） |
| 辅助假设 | CSS 显式分离语义空间能提升特征区分度 | 隐式分类导致语义混杂 | 消融实验（Table IV/V） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | WSA 使类间高频词重叠降低约 36%（top 10） | §V-A, Fig. 4 |
| 辅助假设 | 支撑 | 移除 CSS 后 USTC-TFC task2 macro F1 从 0.9861 降至 0.5998 | Table IV |

---

## 4. 方法设计

### 4.1 方法整体流程

原始 PCAP → Scapy 解析 → Header + Payload → BERT Tokenizer（保留 token 长度信息）→ BERT Encoder → WSA 聚合（无参数）→ CSS 分离（task-aware prompts）→ MLP 分类器

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | PCAP 文件 | Scapy 解析提取 packet，分为 header 和 payload | 流量字序列 X | 数据准备 |
| Step 2 | 流量字序列 | BERT Tokenizer 分词，保留每个字的 token 长度 | Token 序列 X_sep | 分词 |
| Step 3 | Token 序列 | BERT Encoder 编码 | 隐层表示 H_sep | 上下文编码 |
| Step 4 | H_sep | WSA 按 token 长度聚合（直接相加） | 完整词义表示 H | 词义恢复 |
| Step 5 | H + Prompts | CSS：Prompt Encoder → stimulus → 残差 + 平均池化 | 类别级语义 l_c | 语义分离 |
| Step 6 | l_c | MLP + sigmoid | 类别概率 p_c | 分类 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| BERT Tokenizer | 分词 + 保留长度信息 | 流量字序列 | Token 序列 | → BERT Encoder |
| BERT Encoder | 上下文编码 | Token 序列 | 隐层表示 H_sep | → WSA |
| WSA | 无参数聚合恢复完整词义 | H_sep | H | → CSS |
| Prompt Encoder | 编码任务感知提示 | Prompts P | H' | → CSS |
| CSS | stimulus + 残差 + 池化 | H, H' | 类别级语义 l_c | → Classifier |
| MLP Classifier | sigmoid 分类 | l_c | 类别概率 p_c | 最终输出 |

### 4.4 公式、算法和机制解释

**WSA 聚合**：
- h_i = aggregating(h_{i_1}, ..., h_{i_k}, ...) = h_{i_1} + ... + h_{i_k} + ...
- 将被拆分的子词隐层表示直接相加，恢复完整词义
- 无额外参数，仅利用 tokenizer 保留的长度信息

**CSS stimulus 操作**：
- score = softmax(H · H'^T)，计算流量表示与提示表示的注意力分数
- H''_c = (score · H')W_c + b_c，按类别分离语义
- l_c = average-pooling(H + αH''_c)，残差结构保留原始信息

**分类**：p_c = sigmoid(MLP(l_c))

**Prompt 设计**：最优 prompt 为简单的类别列表（如 "YouTube, Spotify, Skype, Gmail, Facebook ..."），无需复杂指令。

### 4.5 方法优势

1. **无需预训练**：直接利用 BERT 已有知识，大幅降低计算成本
2. **无参数 WSA**：不引入额外参数，仅通过聚合操作恢复词义
3. **显式语义分离**：CSS 将不同类别的特征分离到独立语义空间
4. **任务感知提示**：通过 prompt 注入归纳偏置，增强特征区分度
5. **可解释性**：WSA 和 CSS 均有可视化分析支撑
6. **开源**：代码和数据集将公开

### 4.6 方法不足

1. **依赖 BERT 词表**：WSA 仍受限于 BERT 的原始词表，部分流量字节可能被映射为 [UNK]
2. **单包分析**：当前方法仅分析单个 packet，未建模 flow 级别关系
3. **Prompt 设计依赖经验**：不同任务需要手动设计 prompt，最优 prompt 因任务而异
4. **输入长度敏感**：过长（>256）或过短（<128）的输入长度会降低 macro F1

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 维度 | ET-BERT | YaTC | ASNet |
|---|---|---|---|
| 预训练需求 | 需要大规模预训练 | 需要大规模预训练 | 无需预训练 |
| 词义处理 | 重建词表从头训练 | MAE patch 化 | WSA 无参数聚合 |
| 语义分离 | 隐式分类 | 隐式分类 | CSS 显式分离 |
| 计算成本 | 高 | 高 | 低 |

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| WSA 无参数词义聚合 | 利用 tokenizer 长度信息直接相加恢复词义 | 高 | 是 |
| CSS 类别约束语义分离 | task-aware prompts 显式分离不同类别语义空间 | 高 | 是 |
| 无需预训练的 SOTA | 直接利用 BERT 通用知识达到 SOTA | 高 | 是 |

### 5.3 适用场景

- VPN/非 VPN 分类
- 应用识别（12-21 类）
- 恶意软件检测（二分类）
- IoT 攻击检测
- Tor 服务分类
- 真实世界流量分类（CHNAPP）

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| BERT | 通用语言知识 | WordPiece 破坏流量词义 | WSA 恢复完整词义 |
| ET-BERT | 深度上下文表示 | 需大规模预训练 | 无需预训练即达 SOTA |
| YaTC | 多层次 flow 表示 | 需大规模预训练 | 低计算成本 |
| PacRep | 对比学习优化 | 隐式分类 | CSS 显式语义分离 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- GPU: Tesla A100-80G
- Epoch: 3, Batch size: 64
- 最大输入长度: 256, Prompt 长度: 50
- α: 0.2（grid search）
- 学习率: 1e-5, Adam 优化器
- 评价指标: macro F1, micro F1

### 6.2 数据集

| 数据集 | 总 Packet 数 | 任务 | 类别数 |
|---|---|---|---|
| ISCXVPN | 8,711,211 | task1: VPN 分类, task2: 应用分类 | 2, 12 |
| USTC-TFC | 3,011,831 | task1: 恶意检测, task2: 软件分类 | 2, 19 |
| CICIoT | 4,632,537 | IoT 攻击检测 | 多类 |
| ISCXTor | 4,114,398 | Tor 应用分类 | 13 |
| CHNAPP | 1,287,303 | 真实应用分类 | 6 |

### 6.3 Baseline

**特征方法**：APPS, SMT, DevNet
**字节方法**：Deep Packet, TR-IDS, HEDGE, 3D-CNN
**PLM 方法**：BERT, PacRep, ET-BERT, YaTC, EETS

### 6.4 评价指标

macro F1, micro F1

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| ISCXVPN task1 | macro F1 | 100.00% | 100.00% (YaTC) | 0% | VPN 二分类 |
| ISCXVPN task2 | macro F1 | 99.43% | 96.67% (YaTC) | +2.76% | 应用分类 |
| ISCXVPN task2 | micro F1 | 99.65% | 98.04% (YaTC) | +1.61% | 应用分类 |
| USTC-TFC task1 | macro F1 | 100.00% | 100.00% (YaTC) | 0% | 恶意二分类 |
| USTC-TFC task2 | macro F1 | 98.61% | 97.05% (YaTC) | +1.56% | 软件分类 |
| CICIoT | macro F1 | 94.61% | 92.70% (YaTC) | +1.91% | IoT 攻击 |
| CICIoT | micro F1 | 97.50% | 96.04% (YaTC) | +1.46% | IoT 攻击 |
| ISCXTor | macro F1 | 97.66% | 97.56% (EETS) | +0.10% | Tor 服务 |
| ISCXTor | micro F1 | 99.08% | 98.87% (EETS) | +0.21% | Tor 服务 |
| CHNAPP | macro F1 | 98.10% | 95.10% (PacRep) | +3.00% | 真实应用 |
| CHNAPP | micro F1 | 98.75% | 99.14% (EETS) | -0.39% | 真实应用 |

### 6.6 优势最明显的场景

1. **ISCXVPN task2 应用分类**：macro F1 从 96.67% 提升至 99.43%（+2.76%）
2. **CHNAPP 真实场景**：macro F1 从 95.10% 提升至 98.10%（+3.00%），且无需预训练
3. **CICIoT 不平衡数据**：macro F1 与 micro F1 差距仅 2.89%（其他 PLM 方法差距 4-14%）

### 6.7 局限性

1. 在 ISCXTor micro F1 上略低于 EETS（99.08% vs 99.87%）
2. 输入长度对 macro F1 影响显著（64 vs 256 差距约 11%）
3. "Please think step by step" 类复杂 prompt 反而降低性能
4. 仅分析单个 packet，未建模 flow 级别关系

---

## 7. 学习与应用

### 7.1 是否开源？

是。代码地址：https://github.com/pengwei-iie/ASNET

### 7.2 复现关键步骤

1. 使用 BERT Tokenizer 分词，保留 token 长度信息
2. BERT Encoder 编码得到 H_sep
3. WSA 按 token 长度直接相加聚合
4. CSS：Prompt Encoder 编码类别列表 → stimulus → 残差 + 池化
5. MLP + sigmoid 分类

### 7.3 关键超参数、预训练和训练细节

- Epoch: 3
- Batch size: 64
- 最大输入长度: 256
- Prompt 长度: 50
- α（残差权重）: 0.2
- 学习率: 1e-5
- 优化器: Adam
- 最优 Prompt: 简单类别列表（"YouTube, Spotify, Skype, Gmail, Facebook ..."）

### 7.4 能否迁移到其他任务？

是。WSA 和 CSS 均为通用模块，可迁移到任何需要处理结构化字节数据的任务。Prompt 设计可针对不同场景调整（如恶意检测："Given the following traffic data, is the traffic malicious or benign?"）。

### 7.5 对我的研究有什么启发？

1. **无需预训练的可行性**：直接利用 BERT 通用知识 + 领域适配模块即可达到 SOTA
2. **词义完整性的重要性**：保持字节的完整词义对分类性能有显著影响
3. **显式语义分离**：将不同类别的特征分离到独立空间比隐式分类更有效
4. **Prompt 的力量**：简单的类别列表即可作为有效的归纳偏置
5. **不平稀数据处理**：CSS 能显著缩小 macro F1 与 micro F1 的差距

---

## 8. 总结

### 8.1 核心思想

> WSA 无参数聚合恢复词义 + CSS 显式分离类别语义空间

### 8.2 速记版 Pipeline

1. PCAP → Scapy 解析 → 流量字序列
2. BERT Tokenizer 分词（保留长度信息）
3. BERT Encoder 编码 → H_sep
4. WSA：按 token 长度直接相加 → H
5. CSS：Prompt Encoder → stimulus → 残差 + 池化 → l_c
6. MLP + sigmoid → 分类结果

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[Word Sense Aggregator]]
- [[Category-constrained Semantic Separator]]
- [[Task-aware Prompts]]
- [[Parameter-free Module]]
- [[Prompt Learning for Traffic]]

### 9.2 相关方法

- [[ET-BERT]]
- [[YaTC]]
- [[BERT]]
- [[PacRep]]
- [[EETS]]

### 9.3 相关任务

- [[Encrypted Traffic Classification]]
- [[VPN Classification]]
- [[Application Classification]]
- [[Malware Detection]]
- [[IoT Attack Detection]]
- [[Tor Service Classification]]

### 9.4 可更新的综述页面

- [[PLM-based Traffic Classification Methods]]
- [[Prompt Learning for Network Traffic]]
- [[Pre-training vs No Pre-training for ETC]]

### 9.5 可加入的对比表

- [[Pre-training Cost Comparison]]
- [[Word Sense Preservation Strategies]]
- [[Semantic Separation Methods]]

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| WordPiece 破坏流量词义 | "splitting 'xde' into ['x', '##d', '##e']" | §I |
| WSA 降低类间高频词重叠约 36% | "reduced by about 36% and 24% compared to setting one" | §V-A, Fig. 4 |
| CSS 移除后 macro F1 大幅下降 | USTC-TFC task2: 0.9861 → 0.5998 | Table IV |
| 不需预训练即达 SOTA | "without pre-training, our model surpasses the performance of ET-BERT and YaTC" | §IV-D |
| CICIoT 上 macro-micro 差距仅 2.89% | "the performance gap of ASNet on macro F1 and micro F1 metrics has been reduced to 2.89%" | §IV-D |
| 简单 prompt 优于复杂 prompt | Prompt Two 99.65% vs Prompt Three 96.23% | Table VI |
| 输入长度 256 为最优 | "micro F1 reaches its peak value when the length is 256" | §IV-G |
| WSA 使高频词分布更差异化 | "the distribution of high-frequency word varies significantly across the 4 categories" | §V-B |

---

## 11. 原始资料链接

- PDF：`../00-inbox/PDFs/2025-TIFS-Bottom_Aggregating_Top_Separating_An_Aggregator_and_Separator_Network_for_Encrypted_Traffic_Understanding.pdf`
- MinerU Markdown：`../02-parsed-markdown/2025-TIFS-Bottom_Aggregating_Top_Separating_An_Aggregator_and_Separator_Network_for_Encrypted_Traffic_Understanding.md`
- 代码：https://github.com/pengwei-iie/ASNET

---

## 12. 后续问题

- 能否将 WSA 和 CSS 扩展到 flow 级别建模？
- 连续 prompt（continuous prompts）能否进一步提升性能？
- 在更大规模类别数（如数百类）场景下的表现如何？
- WSA 的加权聚合策略能否进一步优化（如注意力加权）？

---

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

从现有 PLM 方法在加密流量分类中的两个弱点出发（WordPiece 破坏词义 + 隐式分类导致语义混杂），提出 ASNet 的两个核心模块：底部 WSA 无参数聚合恢复词义，顶部 CSS 显式分离类别语义空间，无需预训练即在 5 个数据集 7 个任务上达到 SOTA。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 概述两个弱点和解决方案 | 全文缩影 | "without pre-training" |
| Introduction | 从 word-level 和 packet-level 两个角度建立 Gap | 动机铺垫 | "disrupt internal word sense" |
| Related Work | PLM 和 ETC 方法分类对比 | 技术定位 | 预训练方法的计算成本问题 |
| Method | WSA + CSS 详细设计 | 核心贡献 | WSA 的无参数聚合机制 |
| Experiments | 5 数据集 7 任务全面验证 | 支撑论点 | 无需预训练超越预训练方法 |
| Visualization | WSA/CSS 可解释性分析 | 深化论点 | 高频词重叠降低 36% |
| Conclusion | 总结和未来方向 | 收尾 | 连续 prompt 研究方向 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 理论缺陷 | WordPiece 破坏流量字节的完整词义 | 举例说明 "xde" 拆分 | §I |
| 性能瓶颈 | 隐式分类导致语义混杂，特征区分度差 | 现有方法对比分析 | §I |
| 场景缺失 | 预训练方法计算成本高，无法利用 BERT 通用知识 | ET-BERT/YaTC 的资源需求 | §II-B |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 主实验 | 5 数据集 7 任务全面对比 | 证明 ASNet 无需预训练即达 SOTA |
| 消融实验 | 移除 WSA/CSS | 证明各组件的贡献 |
| Prompt 分析 | 不同 prompt 设计对比 | 证明简单 prompt 的有效性 |
| 输入长度分析 | 不同长度下的性能变化 | 揭示长度敏感性 |
| WSA 可视化 | 高频词重叠和分布分析 | 从数据角度解释 WSA 机制 |
| CSS 可视化 | PCA 投影对比 | 证明 CSS 的语义分离效果 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 从 word-level 和 packet-level 两个角度分析问题 | 双角度问题分析框架 |
| Gap 提出方式 | 用具体例子（"xde" 拆分）说明问题 | 具体例子驱动的 Gap 建立 |
| 方法论证逻辑 | 从数据统计（词频重叠）支撑设计选择 | 数据驱动的设计论证 |
| 实验组织逻辑 | RQ 驱动：主实验 → 消融 → 参数分析 → 可视化 | 层层递进 + 可视化验证 |
| 最值得借鉴的一句话结构 | "understanding traffic data is different from understanding words in natural language" | 领域差异的核心论断 |

---
type: paper
title_original: "TraGe: A Generic Packet Representation for Traffic Classification Based on Header-Payload Differences"
title_cn: "TraGe：基于 Header-Payload 差异的通用数据包表示用于流量分类"
authors:
  - Chungang Lin
  - Yilong Jiang
  - Weiyao Zhang
  - Xuying Meng
  - Tianyu Zuo
  - Yujun Zhang
year: 2025
venue: IWQoS
doi: unknown
url: unknown
pdf: "../00-inbox/PDFs/2025-IWQoS-TraGe_A_Generic_Packet_Representation_for_Traffic_Classification_Based_on_Header-Payload_Differences.pdf"
mineru_md: "../02-parsed-markdown/2025-IWQoS-TraGe_A_Generic_Packet_Representation_for_Traffic_Classification_Based_on_Header-Payload_Differences.md"
status: processed
reading_level: L2
research_area:
  - encrypted traffic classification
  - pre-trained model
  - generic packet representation
task:
  - application classification
  - service identification
method:
  - Pre-training
  - Masked Language Modeling
  - Field-level Masking
  - Dynamic Masking
  - Transformer
  - BERT
dataset:
  - ISCX-VPN
  - USTC-TFC
  - CIC-IoT
code: unknown
relevance: high
created: 2026-06-09
updated: 2026-06-09
---

# TraGe: A Generic Packet Representation for Traffic Classification Based on Header-Payload Differences

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | TraGe: A Generic Packet Representation for Traffic Classification Based on Header-Payload Differences |
| 中文标题 | TraGe：基于 Header-Payload 差异的通用数据包表示用于流量分类 |
| 作者 | Chungang Lin, Yilong Jiang, Weiyao Zhang, Xuying Meng, Tianyu Zuo, Yujun Zhang |
| 年份 | 2025 |
| 会议/期刊 | IWQoS |
| 研究方向 | 加密流量分类、预训练模型、通用数据包表示 |
| 任务类型 | 应用分类（17类）、服务识别（12类） |
| 方法关键词 | Field-level Masking, Dynamic Masking, MLM, BERT, Header-Payload Differentiated Pre-training |
| 数据集 | ISCX-VPN, USTC-TFC, CIC-IoT |
| 是否开源 | 否 |
| PDF | `../00-inbox/PDFs/2025-IWQoS-TraGe_A_Generic_Packet_Representation_for_Traffic_Classification_Based_on_Header-Payload_Differences.pdf` |
| MinerU Markdown | `../02-parsed-markdown/2025-IWQoS-TraGe_A_Generic_Packet_Representation_for_Traffic_Classification_Based_on_Header-Payload_Differences.md` |

---

## 1. 一句话总结

> 提出 TraGe，通过区分 header（连续字节序列）和 payload（非连续字节序列）的特点，分别采用 Field-level Masking（MLM-FM）和 Random Masking（MLM-RM）进行差异化预训练，并引入 Dynamic Masking 防止过拟合，在两个流量分类任务上超越 SOTA 方法最高 6.97%。

---

## 2. 摘要翻译

### 2.1 摘要原文

Traffic classification has a significant impact on maintaining the Quality of Service (QoS) of the network. Since traditional methods heavily rely on feature extraction and large-scale labeled data, some recent pre-trained models manage to reduce the dependency by utilizing different pre-training tasks to train generic representations for network packets. However, existing pre-trained models typically adopt pre-training tasks developed for image or text data, which are not tailored to traffic data. As a result, the obtained traffic representations fail to fully reflect the information contained in the traffic, and may even disrupt the protocol information. To address this, we propose TraGe, a novel generic packet representation model for traffic classification. Based on the differences between the header and payload—the two fundamental components of a network packet—we perform differentiated pre-training according to the byte sequence variations (continuous in the header vs. discontinuous in the payload). A dynamic masking strategy is further introduced to prevent overfitting to fixed byte positions. Once the generic packet representation is obtained, TraGe can be finetuned for diverse traffic classification tasks using limited labeled data. Experimental results demonstrate that TraGe significantly outperforms state-of-the-art methods on two traffic classification tasks, with up to a 6.97% performance improvement.

### 2.2 摘要中文翻译

流量分类对维护网络服务质量（QoS）具有重要影响。由于传统方法严重依赖特征提取和大规模标注数据，一些近期的预训练模型通过利用不同预训练任务训练通用数据包表示来减少这种依赖。然而，现有预训练模型通常采用为图像或文本数据开发的预训练任务，并非针对流量数据定制。因此，获得的流量表示无法充分反映流量中包含的信息，甚至可能破坏协议信息。为此，我们提出 TraGe，一种用于流量分类的新型通用数据包表示模型。基于网络数据包的两个基本组成部分（header 和 payload）之间的差异，根据字节序列的变化特点（header 中连续 vs. payload 中非连续）进行差异化预训练。进一步引入动态掩码策略防止对固定字节位置的过拟合。获得通用数据包表示后，TraGe 可使用有限标注数据微调以适配多种流量分类任务。实验结果表明 TraGe 在两个流量分类任务上显著超越 SOTA 方法，最高提升 6.97%。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

现有预训练模型（PERT、ET-BERT、YaTC、NetGPT）采用的预训练任务源自 NLP/CV 领域，未针对流量数据的特殊结构（header 连续字节 vs. payload 非连续字节）进行定制。

### 3.2 现有方法的痛点和不足

1. **PERT/ET-BERT**：仅基于 payload 进行分类，忽略 header 中的结构化协议信息
2. **NetGPT/YaTC**：将 header 和 payload 统一处理，破坏了 header 字段的字节连续性
3. **通用问题**：使用随机掩码（Random Masking）会破坏 header 字段的连续性，如将 TCP sequence number "b11eac20" 部分掩码，导致模型无法学习完整的协议语义

### 3.3 论文的研究假设或核心直觉

header 和 payload 的字节分布特性根本不同（header 连续 vs. payload 非连续），应采用不同的掩码策略分别预训练，以生成更通用的数据包表示。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 现有预训练模型直接借用 NLP/CV 的预训练任务 | §I |
| 痛点提炼 | 随机掩码破坏 header 字段连续性，无法学习协议语义 | §III-A |
| 问题转化 | 如何根据 header/payload 的字节分布差异设计差异化预训练策略 | §III-A |
| 文献定位 | 现有方法均未考虑 header-payload 结构差异 | §II-C |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 字段级掩码（Field-level Masking）比随机掩码更适合 header 预训练 | header 字段长度分布近似几何分布 | 消融实验（Table IV） |
| 辅助假设 | Dynamic Masking 比 Static Masking 更能提升泛化能力 | 静态掩码导致模型记忆固定位置 | 消融实验（Table IV） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | 移除 FM 后应用分类 F1 下降 5.88% | §IV-C, Table IV |
| 辅助假设 | 支撑 | 移除 DM 后应用分类 F1 下降 1.62% | §IV-C, Table IV |

---

## 4. 方法设计

### 4.1 方法整体流程

原始流量 → Header-Payload 分离 → Header 用 MLM-FM（Field-level Masking）预训练 / Payload 用 MLM-RM（Random Masking）预训练 → Dynamic Masking → 获得通用数据包表示 → Fine-tuning 分类

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | 原始数据包 | 分离 header 和 payload，bi-gram tokenize | Header/Payload token 序列 | 数据准备 |
| Step 2 | Header tokens | 从几何分布 Geo(p) 采样长度 l，连续掩码 l 个 tokens | MLM-FM 预训练 | 保持 header 字段连续性 |
| Step 3 | Payload tokens | 随机选择 r 个 tokens 掩码 | MLM-RM 预训练 | 适配 payload 非连续特性 |
| Step 4 | 掩码位置 | 每次训练动态生成掩码位置 | Dynamic Masking | 防止过拟合 |
| Step 5 | 通用表示 | MLP + Softmax 分类 | 分类结果 | Fine-tuning |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Field-level Masking | 连续掩码 header 字段 | Header token 序列 | 掩码后的 header | MLM-FM 任务 |
| Random Masking | 随机掩码 payload tokens | Payload token 序列 | 掩码后的 payload | MLM-RM 任务 |
| Dynamic Masking | 动态生成掩码位置 | 掩码策略 | 变化的掩码模式 | 防止过拟合 |
| Transformer Encoder | 学习通用表示 | token 序列 | 隐层表示 | 共享 backbone |

### 4.4 公式、算法和机制解释

**Field-level Masking (MLM-FM)**:
- 几何分布 l ~ Geo(p)，p=0.7 时分布与实际 header 字段长度分布近似
- 连续选择 l 个 tokens 进行掩码
- 损失函数：L_MLM-FM = -Σ log P(MASK_i = token_i | θ_H)

**Random Masking (MLM-RM)**:
- 随机选择 r 个 tokens 进行掩码
- 损失函数：L_MLM-RM = -Σ log P(MASK_i = token_i | θ_P)

**Dynamic Masking**: 训练过程中动态生成掩码位置，而非预处理阶段固定

### 4.5 方法优势

1. **结构感知**：根据 header/payload 的字节分布差异进行差异化预训练
2. **无额外开销**：Field-level Masking 无需解析协议头部，使用几何分布近似
3. **泛化能力强**：Dynamic Masking 使模型暴露于更多样的字节组合
4. **通用性**：一次预训练获得的通用表示可适配多种下游任务

### 4.6 方法不足

1. **仅处理单包**：未建模 packet 间关系，可能遗漏 flow 级别信息
2. **几何分布参数敏感**：虽然实验显示 p 在 0.1-0.9 范围内表现稳定，但最优值仍需选择
3. **未考虑协议多样性**：不同协议的 header 字段长度分布可能不同

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 维度 | ET-BERT | YaTC | TraGe |
|---|---|---|---|
| Header 处理 | 忽略 header | 统一处理 | 字段级掩码保持连续性 |
| Payload 处理 | 随机掩码 | MAE patch | 随机掩码 |
| 掩码策略 | Static | Static | Dynamic |
| 预训练任务定制 | NLP 任务直接迁移 | CV 任务直接迁移 | 针对流量数据特点设计 |

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| Header-Payload 差异化预训练 | 根据字节分布特点分别设计 MLM-FM 和 MLM-RM | 高 | 是 |
| Field-level Masking | 用几何分布近似 header 字段长度进行连续掩码 | 高 | 是 |
| Dynamic Masking | 训练时动态生成掩码位置 | 中 | 是 |

### 5.3 适用场景

- VPN 环境下的应用分类
- 服务识别（Chat/VoIP/P2P/Email 等）
- 需要理解协议头部信息的流量分类任务

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| PERT | 简单的 MLM 预训练 | 忽略 header 信息 | 引入 header 预训练 |
| ET-BERT | datagram 级别表示 | 仅 payload，破坏 header 连续性 | 差异化预训练 |
| YaTC | 多层次 flow 表示 | 统一处理 header/payload | 针对性掩码策略 |
| NetGPT | 生成式预训练 | 统一处理破坏协议信息 | 结构感知预训练 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- 预训练：100,000 steps，学习率 1e-3，Geo(p=0.7)
- 微调：10 epochs，学习率 2e-5
- 每 flow 最多 5 packets
- 每类别最多 5000 flows
- 数据划分：8:1:1

### 6.2 数据集

| 数据集 | 来源 | 用途 |
|---|---|---|
| ISCX-VPN | 多应用 VPN 流量 | 应用分类（17类）、服务识别（12类） |
| USTC-TFC | 智能电网流量 | 预训练 |
| CIC-IoT | IoT 流量 | 预训练 |

### 6.3 Baseline

- 统计特征方法：FlowPrint, AppScanner, XGBoost, DTree
- 深度学习方法：FS-Net, EBSNN-L, EBSNN-G, TFE-GNN
- 预训练方法：PERT, ET-BERT, NetGPT, YaTC

### 6.4 评价指标

Precision, Recall, F1-Score

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| 应用分类 | Precision | 75.17% | 74.21% (YaTC) | +0.96% | 17 类应用 |
| 应用分类 | Recall | 75.41% | 71.87% (NetGPT) | +3.54% | 17 类应用 |
| 应用分类 | F1 | 74.84% | 71.82% (NetGPT) | +3.02% | 17 类应用 |
| 服务识别 | Precision | 93.33% | 92.50% (NetGPT) | +0.83% | 12 类服务 |
| 服务识别 | Recall | 93.35% | 91.92% (NetGPT) | +1.43% | 12 类服务 |
| 服务识别 | F1 | 93.31% | 92.07% (NetGPT) | +1.24% | 12 类服务 |

### 6.6 优势最明显的场景

应用分类任务中，TraGe 相比次优方法 NetGPT 在 Recall 上提升 4.93%，F1 上提升 4.20%，在 17 类细粒度分类中优势显著。

### 6.7 局限性

1. 仅在 ISCX-VPN 数据集上进行了分类任务评估
2. 未与其他方法在更多数据集上进行对比
3. 参数敏感性分析中 p 值选择的理论依据不够充分

---

## 7. 学习与应用

### 7.1 是否开源？

否

### 7.2 复现关键步骤

1. 使用 BERT 作为 Transformer Encoder
2. 预训练 100K steps，p=0.7
3. 微调 10 epochs，lr=2e-5
4. 每 flow 最多 5 packets

### 7.3 关键超参数、预训练和训练细节

- 几何分布参数 p: 0.7
- 预训练 steps: 100,000
- 预训练学习率: 1e-3
- 微调 epochs: 10
- 微调学习率: 2e-5
- 每 flow packet 数: 5
- 每类别最大 flow 数: 5000

### 7.4 能否迁移到其他任务？

是。Header-Payload 差异化预训练的思路可迁移到任何需要处理结构化 header + 非结构化 payload 的网络数据分析任务。

### 7.5 对我的研究有什么启发？

1. **数据特性驱动设计**：应根据流量数据本身的特点（而非直接借用 NLP/CV 任务）设计预训练策略
2. **Header 信息的重要性**：header 中的协议字段信息对分类有重要贡献，不应忽略
3. **Dynamic vs Static**：训练时的动态变化比固定的预处理策略更有利于泛化

---

## 8. 总结

### 8.1 核心思想

> 根据 header/payload 字节分布差异进行差异化预训练

### 8.2 速记版 Pipeline

1. 分离 header 和 payload
2. Header: Field-level Masking（几何分布连续掩码）
3. Payload: Random Masking
4. Dynamic Masking 防止过拟合
5. Fine-tuning 分类

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[Field-level Masking]]
- [[Dynamic Masking]]
- [[Header-Payload Differentiated Pre-training]]
- [[Generic Packet Representation]]

### 9.2 相关方法

- [[ET-BERT]]
- [[YaTC]]
- [[NetGPT]]
- [[BERT MLM]]

### 9.3 相关任务

- [[Application Classification]]
- [[Service Identification]]
- [[Encrypted Traffic Classification]]

### 9.4 可更新的综述页面

- [[Pre-training Strategies for Network Traffic]]
- [[Masking Strategies Comparison]]

### 9.5 可加入的对比表

- [[Masking Strategy Comparison]]
- [[Header vs Payload Information Usage]]

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| header 字段长度分布近似几何分布 | Figure 2: "distribution of header protocol field lengths... closely aligns with the geometric distribution" | §III-A |
| Field-level Masking 对应用分类 F1 贡献 5.88% | "eliminating field-level masking leads to a 5.88% decrease in F1-score" | §IV-C |
| Dynamic Masking 对应用分类 F1 贡献 1.62% | "removing dynamic masking causes a 1.62% reduction" | §IV-C |
| TraGe 在应用分类上超越次优方法 6.97% | "TraGe outperforms state-of-the-art pre-trained models, with average performance improvements of... 6.97%" | §IV-B |
| 参数 p 在 0.1-0.9 范围内表现稳定 | "F1-Score fluctuates only slightly within the range of 0.9275 to 0.9323" | §IV-D |

---

## 11. 原始资料链接

- PDF：`../00-inbox/PDFs/2025-IWQoS-TraGe_A_Generic_Packet_Representation_for_Traffic_Classification_Based_on_Header-Payload_Differences.pdf`
- MinerU Markdown：`../02-parsed-markdown/2025-IWQoS-TraGe_A_Generic_Packet_Representation_for_Traffic_Classification_Based_on_Header-Payload_Differences.md`

---

## 12. 后续问题

- 不同协议的 header 字段长度分布是否需要不同的几何分布参数？
- 能否自动检测协议类型并选择最优掩码策略？
- Header-Payload 差异化预训练能否与 flow 级别建模结合？
- 在更多数据集和任务上的泛化能力如何？

---

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

从现有预训练模型直接借用 NLP/CV 任务的局限出发，指出流量数据的 header 和 payload 具有根本不同的字节分布特性，提出差异化预训练策略（Field-level Masking for header + Random Masking for payload），配合 Dynamic Masking，在两个任务上超越 SOTA。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 概述问题和解决方案 | 全文缩影 | "header-payload differences" |
| Introduction | 从传统方法到预训练模型的演进建立 Gap | 动机铺垫 | "existing pre-trained models... not tailored to traffic data" |
| Related Work | 三类方法的系统对比 | 技术定位 | 预训练方法的不足 |
| Method | 差异化预训练设计 | 核心贡献 | Field-level Masking 的几何分布近似 |
| Experiments | RQ1-RQ4 全面验证 | 支撑论点 | 参数敏感性和采样稳定性 |
| Conclusion | 总结和展望 | 收尾 | 通用表示的有效性 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 场景缺失 | 现有方法未考虑 header-payload 结构差异 | 对比分析 4 类预训练方法 | §I, §II-C |
| 理论缺陷 | 随机掩码破坏 header 字段连续性 | 举例说明 TCP sequence number | §III-A |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 主实验 (RQ1) | 全面对比 12 个 baseline | 证明 TraGe 的有效性 |
| 消融实验 (RQ2) | 移除 FM/DM | 证明各组件贡献 |
| 参数分析 (RQ3) | 几何分布参数 p 的影响 | 证明方法的鲁棒性 |
| 采样分析 (RQ4) | 不同随机种子下的稳定性 | 证明泛化能力 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 从 QoS 需求出发 | 应用驱动的问题引入 |
| Gap 提出方式 | 分类现有方法并逐一分析不足 | "However... As a result..." 句式 |
| 方法论证逻辑 | 从数据特点推导设计决策 | 实证支撑（Figure 2 分布对比） |
| 实验组织逻辑 | 4 个 RQ 系统回答 | 研究问题驱动的实验设计 |
| 最值得借鉴的一句话/一段结构 | "the distribution of header protocol field lengths... closely aligns with the geometric distribution" | 用数据统计支撑设计选择 |

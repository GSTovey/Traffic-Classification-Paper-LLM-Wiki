---
type: paper
title_original: "The Sweet Danger of Sugar: Debunking Representation Learning for Encrypted Traffic Classification"
title_cn: "糖的甜蜜危险：揭秘加密流量分类中的表征学习"
authors: ["Yuqi Zhao", "Giovanni Dettori", "Matteo Boffa", "Luca Vassio", "Marco Mellia"]
year: 2025
venue: "ACM SIGCOMM 2025"
doi: "10.1145/3718958.3750498"
url: "https://dl.acm.org/doi/10.1145/3718958.3750498"
pdf: "00-inbox/PDFs/2025-SIGCOMM-The_Sweet_Danger_of_Sugar_Debunking_Representation_Learning_for_Encrypted_Traffic_Classification.pdf"
mineru_md: "02-parsed-markdown/2025-SIGCOMM-The_Sweet_Danger_of_Sugar_Debunking_Representation_Learning_for_Encrypted_Traffic_Classification.md"
status: processed
reading_level: L2
research_area: ["encrypted traffic classification", "representation learning", "reproducibility"]
task: ["traffic classification", "model evaluation", "benchmark design"]
method: ["representation learning", "self-supervised pre-training", "masked autoencoder", "question-answering", "T5", "BERT", "ViT", "Mamba"]
dataset: ["ISCX-VPN", "USTC-TFC", "CSTNET-TLS1.3", "MAWI", "UNSW-NB15"]
code: "https://github.com/SweetDanger-Polito/SweetDanger"
relevance: high
created: "2026-05-27"
updated: "2026-05-27"
---

# The Sweet Danger of Sugar: Debunking Representation Learning for Encrypted Traffic Classification

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | The Sweet Danger of Sugar: Debunking Representation Learning for Encrypted Traffic Classification |
| 中文标题 | 糖的甜蜜危险：揭秘加密流量分类中的表征学习 |
| 作者 | Yuqi Zhao, Giovanni Dettori, Matteo Boffa, Luca Vassio, Marco Mellia |
| 年份 | 2025 |
| 会议/期刊 | ACM SIGCOMM 2025 |
| 研究方向 | 加密流量分类、表征学习、可复现性 |
| 任务类型 | 加密流量分类的模型评估与 benchmark 设计 |
| 方法关键词 | representation learning, self-supervised pre-training, shortcut learning, data leakage, frozen/unfrozen encoder, per-packet vs per-flow split |
| 数据集 | ISCX-VPN, USTC-TFC, CSTNET-TLS1.3, MAWI, UNSW-NB15 |
| 是否开源 | 是（代码、benchmark 数据集和方法论均已开源） |
| PDF | 00-inbox/PDFs/2025-SIGCOMM-The_Sweet_Danger_of_Sugar_Debunking_Representation_Learning_for_Encrypted_Traffic_Classification.pdf |
| MinerU Markdown | 02-parsed-markdown/2025-SIGCOMM-The_Sweet_Danger_of_Sugar_Debunking_Representation_Learning_for_Encrypted_Traffic_Classification.md |

## 1. 一句话总结

> 本文系统性地揭示了已有加密流量表征学习模型（ET-BERT、YaTC、NetMamba 等）在数据准备和评估方法上的严重缺陷，证明其报告的高达 98% 的准确率主要源于 per-packet split 导致的数据泄漏和 shortcut learning，而非真正有意义的表征；在正确的 per-flow split 和 frozen encoder 设置下，这些模型的准确率可暴跌至 30%-40%。

## 2. 摘要翻译

### 2.1 摘要原文

Recently we have witnessed the explosion of proposals that, inspired by Language Models like BERT, exploit Representation Learning models to create traffic representations. All of them promise astonishing performance in encrypted traffic classification (up to 98% accuracy). In this paper, with a networking expert mindset, we critically reassess their performance. Through extensive analysis, we demonstrate that the reported successes are heavily influenced by data preparation problems, which allow these models to find easy shortcuts - spurious correlation between features and labels - during fine-tuning that unrealistically boost their performance. When such shortcuts are not present - as in real scenarios - these models perform poorly. We also introduce Pcap-Encoder, an LM-based representation learning model that we specifically design to extract features from protocol headers. Pcap-Encoder appears to be the only model that provides an instrumental representation for traffic classification. Yet, its complexity questions its applicability in practical settings. Our findings reveal flaws in dataset preparation and model training, calling for a better and more conscious test design. We propose a correct evaluation methodology and stress the need for rigorous benchmarking.

### 2.2 摘要中文翻译

近年来，受 BERT 等语言模型启发，利用表征学习（Representation Learning）模型创建流量表征的提案大量涌现，它们都承诺在加密流量分类中达到惊人的性能（高达 98% 的准确率）。本文以网络专家的视角，对其性能进行了批判性重新评估。通过广泛分析，我们证明这些报告的成功在很大程度上受到数据准备问题的影响，这些问题使模型在 fine-tuning 过程中找到了简单的 shortcut（特征与标签之间的虚假关联），从而不切实地提升了性能。当这些 shortcut 不存在时——如真实场景——这些模型表现很差。我们还提出了 Pcap-Encoder，一种专门设计用于从协议头部提取特征的基于语言模型的表征学习模型。Pcap-Encoder 似乎是唯一能为流量分类提供有意义表征的模型，但其复杂性引发了对其实际应用可行性的质疑。我们的发现揭示了数据集准备和模型训练中的缺陷，呼吁更好、更有意识的测试设计，并提出了正确的评估方法论，强调了严格 benchmarking 的必要性。

## 3. 方法动机

### 3.1 "Sugar"隐喻的深层含义

论文标题中的 "Sweet Danger of Sugar" 是对表征学习在加密流量分类中现状的一个精妙隐喻：

- **"Sweet"（甜蜜）**：表征学习模型报告的 98%+ 准确率就像糖一样令人愉悦和上瘾。这些甜美的结果让研究者和审稿人趋之若鹜，大量论文竞相发表，形成了一个自我强化的正反馈循环。正如摘要所述，这些结果 "falsely close to perfection"（虚假地接近完美）。
- **"Danger"（危险）**：糖的甜蜜背后隐藏着健康风险。同样，这些看似完美的结果掩盖了严重的评估缺陷——数据泄漏、shortcut learning、不合理的训练策略。这些缺陷使得模型学到的不是真正有意义的流量表征，而是利用数据准备中的漏洞进行"作弊"。
- **核心批判**：作者认为表征学习本身并非"有毒"，但当前的研究实践（数据准备、评估方法、结果报告）存在系统性缺陷，使得整个领域建立在一个虚假的基础之上。这类似于 NLP 和 CV 领域早期也曾经历过的类似危机。

### 3.2 作者为什么提出这个方法？

- 近年来大量论文声称基于 BERT/ViT/Mamba 的表征学习模型在加密流量分类上达到 98%+ 的准确率，但这些结果令人怀疑——在网络专家看来，强加密算法下的 payload 字节之间不应存在可学习的语义关联
- 作者发现已有模型的评估流程存在多处严重缺陷，包括数据泄漏、shortcut learning、不合理的数据集划分等
- 论文引用了 Arp et al. (2022) 对过去十年顶级安全会议论文的分析，以及 Jacobs et al. (2022) 关于 "AI/ML for network security: The emperor has no clothes" 的工作，表明 shortcut learning 问题在网络安全 ML 领域是系统性的，而非个案
- Willinger et al. (2025) 更进一步提出了 ML for networking 领域的 "Credibility Crisis"（可信度危机），本文正是对这一危机的具体回应
- 作者希望提出一个公平、标准化的 benchmark 框架来正确评估表征学习在流量分类中的真实能力

### 3.3 现有方法的痛点和不足

| 现有方法/做法 | 痛点 | 严重程度 |
|---|---|---|
| ET-BERT, YaTC, NetMamba, TrafficFormer, netFound 等的 per-packet split | 同一流的数据包同时出现在训练集和测试集，导致严重的数据泄漏；模型可通过 implicit flow ID（SeqNo, AckNo, TCP timestamp，共同构成约 64-bit 的隐式流标识符）将测试包关联到训练集中的类标签 | 致命——可导致 80% 的性能虚假提升 |
| 所有已有模型的 unfrozen encoder 训练 | end-to-end fine-tuning "摧毁"了预训练知识，模型实际上是重新训练而非利用预训练表征；ET-BERT 无预训练（随机初始化）仍达 97.1%，证明预训练几乎无贡献 | 致命——预训练表征质量极低 |
| 对加密 payload 做 MAE 预训练 | 加密后 payload 字节之间不存在语义关联，在加密 payload 上做 masked autoencoder 预训练没有意义；这与 NLP/CV 中 MAE 成功的前提（词/像素间存在强相关性）根本不同 | 根本性——理论基础不成立 |
| 数据集复用（上游预训练 = 下游任务数据） | 违背 ML 最佳实践，导致预训练阶段的过拟合和数据泄漏；ET-BERT 使用 ISCX-VPN 和 CSTNET-TLS1.3 同时用于上下游任务，YaTC 和 NetMamba 甚至使用完全相同的数据集 | 严重——破坏评估有效性 |
| 缺乏 frozen encoder 评估 | 无法验证预训练表征是否真正有意义；frozen encoder 下 71% 的点没有同类邻居（5-NN purity 分析） | 严重——掩盖表征质量问题 |
| 使用 micro F1-Score | 误导性地高估多数类性能，掩盖少数类的糟糕表现；YaTC, NetMamba 和 netFound 均使用 micro F1 | 中等——影响结果解读 |
| 最小包长/流长过滤 | ET-BERT 过滤 <80B 的包，TrafficFormer 过滤 <2kB 或 <3 包的流，netFound 过滤 <6 包的流；这些过滤会移除所有 TCP 信令和确认包，改变分类任务的本质 | 中等——改变任务定义 |

### 3.4 论文的研究假设或核心直觉

- **核心假设**：已有表征学习模型报告的高准确率主要源于评估方法的缺陷（数据泄漏和 shortcut learning），而非真正有意义的流量表征
- **关键直觉 1**：在加密流量中，payload 字节经过加密后已无语义信息。NLP 中 MAE 成功的前提是词与词之间存在语法和语义关联（Chomsky 的句法结构理论），CV 中图像 patch 之间存在空间相关性（Marr 的视觉理论）。但强加密算法（如 AES-GCM）确保密文是伪随机的，字节之间没有可学习的相关性——因此对加密 payload 做 MAE 在理论上就不可行
- **关键直觉 2**：per-packet split 使同一流的包同时出现在训练集和测试集，模型可利用 implicit flow ID（如 TCP SeqNo/AckNo，随机选择于 TCP 三次握手，共同构成约 64-bit 的隐式流标识符）作为 shortcut。这意味着模型只需学会 "这个 SeqNo 范围属于哪个流" 就能完成分类，完全不需要理解流量语义
- **关键直觉 3**：unfrozen encoder 的大量有标签下游训练数据会导致预训练知识被遗忘（catastrophic forgetting），模型本质上是重新训练。5-NN purity 分析显示：frozen encoder 下 71% 的点没有同类邻居，unfrozen 后 97% 的点 5 个邻居全同类——这说明原始表征完全无意义，只有 fine-tuning 后才变得可用
- **关键直觉 4**：已有论文声称 "pre-training allows the model to extract patterns from the encrypted payloads"（ET-BERT 原文），这一论断在密码学上站不住脚。如果加密算法足够强，密文应与随机噪声不可区分，不存在可提取的 "patterns"

## 4. 方法设计

### 4.1 方法整体流程——"揭穿"论文的实验方法论

本文是一篇典型的 "debunking"（揭穿/证伪）论文，其方法论核心不是提出新模型，而是通过精心设计的对照实验系统性地否定已有结论。整体流程如下：

1. **问题识别**：分析已有表征学习模型在数据准备（清理、划分、采样）和训练策略（frozen vs unfrozen）中的缺陷
2. **Benchmark 构建**：定义标准化的数据清理、per-flow split、balanced sampling 流程，在三个公开数据集上构建六个分类任务
3. **模型评估**：在统一 benchmark 下评估五个 SoA 模型（ET-BERT、YaTC、NetMamba、TrafficFormer、netFound），分别测试 frozen 和 unfrozen encoder 设置
4. **Pcap-Encoder 设计**：提出专门从协议头部提取信息的新模型，通过两阶段预训练（Autoencoder + Q&A）
5. **Shortcut 分析**：系统性地识别和量化 implicit flow ID 等 shortcut 对模型性能的影响
6. **与浅层模型对比**：将表征学习模型与使用手工特征的浅层 ML 模型（RF, XGBoost, LightGBM, MLP）进行对比

### 4.2 揭穿已有结论的核心实验设计

本文的实验设计遵循 "控制变量 + 逐步排除" 的思路，通过一系列对照实验逐步揭示已有模型高准确率的真实来源：

**实验 1：Frozen vs Unfrozen Encoder**
- 目的：检验预训练表征是否真正有意义
- 设计：在同一 per-flow split 下，分别测试 frozen 和 unfrozen encoder
- 发现：frozen encoder 下 ET-BERT 在 TLS-120 上 Macro F1 仅 6.7%（vs 原文报告的 96.8%），说明预训练表征几乎无信息量
- 核心论点：如果预训练真的学到了有意义的表征，frozen encoder 应该也能工作

**实验 2：Per-flow vs Per-packet Split**
- 目的：检验 per-packet split 是否引入数据泄漏
- 设计：在同一 unfrozen encoder 下，分别使用 per-flow split 和 per-packet split
- 发现：per-packet split 下 ET-BERT 在 TLS-120 上 F1 为 96.8%，per-flow split 下暴跌至 21.5%——性能下降约 75%
- 核心论点：per-packet split 使同一流的包同时出现在训练集和测试集，模型利用 implicit flow ID 作为 shortcut

**实验 3：逐步移除 Implicit Flow ID（消融实验）**
- 目的：精确定位数据泄漏的来源
- 设计：以 ET-BERT + TLS-120 + per-packet split + unfrozen encoder 为基准，逐步移除 SeqNo/AckNo/Timestamp
- 发现：
  - 原始设置：97.4% accuracy
  - 移除 SeqNo/AckNo/Timestamp（仅测试集）：19.5%（暴跌 80%！）
  - 移除 SeqNo/AckNo/Timestamp（训练+测试集）：52.2%
  - 无预训练（随机初始化）：97.1%（与有预训练几乎相同！）
- 核心论点：模型主要依赖 SeqNo/AckNo/Timestamp 这些 implicit flow ID 进行分类，而非真正理解流量语义

**实验 4：预训练有效性验证**
- 目的：检验预训练是否对下游任务有贡献
- 设计：将 ET-BERT 权重随机初始化，然后 fine-tuning
- 发现：随机初始化的 ET-BERT 在 TLS-120 上达到 97.1%（vs 预训练版本的 97.4%），差异仅 0.3%
- 核心论点：ET-BERT 的预训练几乎无贡献，fine-tuning 阶段重新学习了所有知识

**实验 5：5-NN Purity 嵌入质量分析**
- 目的：直观评估嵌入空间的质量
- 设计：对每个嵌入向量，查找其 5 个最近邻，统计同类邻居比例
- 发现：frozen encoder 下 71% 的点没有同类邻居（0/5 同类），unfrozen 后 97% 的点 5 个邻居全同类
- 核心论点：原始嵌入空间完全没有语义结构，只有 fine-tuning 后才变得可用——但这恰恰说明预训练没有学到有意义的表征

**实验 6：Pcap-Encoder 消融实验**
- 目的：验证 Pcap-Encoder 确实依赖协议头信息
- 设计：分别移除 IP 地址、整个头部、payload
- 发现：
  - 移除 IP 地址：VPN-app F1 从 71.0 降至 52.5，TLS-120 从 63.7 降至 13.0
  - 移除整个头部：VPN-app F1 暴跌至 16.4，TLS-120 暴跌至 1.5
  - 移除 payload：VPN-app F1 从 71.0 降至 66.7（仅小幅下降），TLS-120 保持 63.6（几乎不变）
- 核心论点：Pcap-Encoder 确实依赖协议头部信息而非 payload，且在 "everything encrypted" 场景下 payload 确实无贡献

**实验 7：Shallow Model 特征重要性分析**
- 目的：理解浅层模型依赖哪些特征
- 设计：使用 Random Forest 的特征重要性分数
- 发现（per-packet split, TLS-120）：
  - 有 IP 地址时：最重要的特征是 SRC IP3（0.135）、DST IP2（0.105）等 IP 地址字段
  - 移除 IP 地址后：最重要的特征变为 TCP SeqNo、AckNo 等 implicit flow ID
  - 移除 IP 后准确率从 98.9% 降至 92.6%——说明 implicit flow ID 仍然是主要 shortcut

### 4.3 详细 Pipeline（表格形式）

| 步骤 | 描述 | 技术细节 |
|---|---|---|
| 1. 数据集选择 | 选择三个主流公开数据集 | ISCX-VPN（6 类服务）、USTC-TFC（20 个应用）、CSTNET-TLS1.3（120 个网站） |
| 2. 数据清理 | 过滤无关协议、去除头部信息干扰 | 过滤 ARP/DHCP/STUN 等；ISCX 含 5%、USTC 含 10% 的杂散包；不做最小包长过滤 |
| 3. 数据划分 | 采用 per-flow split 替代 per-packet split | 同一流的所有包要么全在训练集，要么全在测试集；7:1 比例划分 |
| 4. 采样策略 | 训练集通过欠采样实现类别平衡 | 测试集保持原始分布；超过 1000 包的流随机采样 1000 包 |
| 5. 模型评估 | 冻结/解冻 encoder 分别测试 | frozen encoder 验证表征质量；unfrozen encoder 模拟实际 fine-tuning |
| 6. Shortcut 分析 | 移除/随机化 implicit flow ID | 移除 SeqNo、AckNo、TCP timestamp 后观察性能变化 |
| 7. Baseline 对比 | 与浅层 ML 模型对比 | RF、XGBoost、LightGBM、MLP 使用手工提取的协议头字段特征 |

### 4.4 Pcap-Encoder 模型设计——唯一有意义的表征学习尝试

Pcap-Encoder 是本文提出的对照组模型，其设计理念与已有模型根本不同：**只从协议头部提取信息，完全忽略加密 payload**。这是基于一个关键洞察：加密后的 payload 字节之间没有语义关联，对加密 payload 做 MAE 预训练在理论上不可行。

| 模块 | 功能 | 输入 | 输出 |
|---|---|---|---|
| Pcap-Encoder Phase 1 (T5-AE) | 用自编码器将原始包映射到数值空间，适配流量数据格式 | 原始包的 2-byte token 序列 | 包的 768 维表征向量 |
| Pcap-Encoder Phase 2 (Q&A) | 通过问答任务学习协议头语义（8 类问题，50,000 个实例） | 问题 + 包 token（以 </s> 分隔） | 协议头语义增强的表征向量 |
| Mean Pooling Bottleneck | 将多个 token 表征聚合为单个包表征（测试了 First Pooling、Mean Pooling、Luong Attention，Mean Pooling 足够） | T5 encoder 输出的 token 嵌入矩阵 | 768 维包表征 |
| 下游分类头 | 对表征进行分类 | 768 维嵌入向量 | 类别预测 |
| Shallow Baseline | 使用手工特征的 ML 分类 | 手工提取的协议头字段向量（Table 12 列出 IPv4/IPv6/UDP/TCP 的具体字段） | 类别预测 |

**Q&A 预训练的问题设计**（Table 10）：
- 检索类问题：TCP checksum、源/目的 IPv4/IPv6 地址、IPv4/IPv6 ID、TTL 等
- 计算类问题：IPv4/IPv6 校验和是否正确、第三层头部最后一个字节、第三层 payload 长度
- 关键设计原则：避免对应用 payload 提问（除大小外），因为加密阻止了对内容的任何有意义的回答

**Pcap-Encoder 的预训练数据**：MAWI、UNSW-NB15 和作者自己收集的校园网络 trace，共约 1GB / 500k packets，确保空间和时间多样性。

### 4.5 公式、算法和机制解释

**Pcap-Encoder 的 Mean Pooling**：

$$\boldsymbol{r}_i = \frac{\sum_{j=1}^{L} \boldsymbol{e}_{i,j}}{L}$$

其中 $\boldsymbol{e}_{i,j}$ 是第 $i$ 个包的第 $j$ 个 token 的表征，$L$ 是 token 数量。

**5-NN Purity 指标**：对每个嵌入向量，查找其 5 个最近邻，统计同类邻居的比例。若嵌入有意义，多数邻居应同类。这是评估表征质量的直观方法——如果预训练真的学到了有意义的表征，同类样本应该在嵌入空间中聚集。

**Implicit Flow ID 的构成**：
- Explicit Flow ID：5-tuple（源 IP、源端口、目的 IP、目的端口、协议）
- Implicit Flow ID：TCP SeqNo + AckNo（随机选择于三次握手，共同构成约 64-bit 的隐式流标识符）+ TCP Timestamp Option
- 这些字段在 per-packet split 下会"泄漏"流的信息，使模型能将测试包关联到训练集中的类标签

**关键机制解释**：
- **Per-flow split vs Per-packet split**：per-packet split 随机将同一 TCP 流的包分散到训练集和测试集，模型可利用 implicit flow ID（SeqNo, AckNo, TCP timestamp 共同构成约 64-bit 的隐式流标识符）将测试包关联到训练集中的类标签，这是 data leakage 的主要来源
- **Frozen vs Unfrozen encoder**：frozen encoder 评估预训练表征的质量；unfrozen encoder 允许 end-to-end fine-tuning，但大量有标签数据会导致预训练知识被覆盖（catastrophic forgetting）
- **Shortcut learning**：模型学习到的"捷径"（如 IP 地址、SeqNo）在标准 benchmark 上有效，但无法迁移到真实部署场景。这与 Geirhos et al. (2020) 在 Nature Machine Intelligence 上描述的 shortcut learning 问题一致

### 4.6 方法优势

1. **系统性**：首次对加密流量表征学习领域进行全面的批判性评估，覆盖数据准备、训练策略、评估指标等多个维度
2. **公平性**：在统一的 benchmark 下对所有模型使用完全相同的训练/测试划分，确保公平比较
3. **可复现性**：代码、数据集和方法论全部开源（https://github.com/SweetDanger-Polito/SweetDanger）
4. **诊断深度**：通过逐步移除 shortcut（SeqNo/AckNo/Timestamp/IP 地址）的消融实验，精确定位数据泄漏来源
5. **实践指导**：提出了四条具体的最佳实践建议（控制 shortcut learning、验证数据完整性、测试 frozen encoder、对比简单 baseline）
6. **理论支撑**：从密码学角度论证了为什么对加密 payload 做 MAE 不可行，提供了理论基础

### 4.7 方法不足

1. **Pcap-Encoder 复杂度高**：基于 T5-base 架构，训练时间是 RF 的 16 倍，推理时间也是 16 倍
2. **Pcap-Encoder 性能未超越浅层模型**：在相同输入下，手工特征的 RF/XGBoost/LightGBM 均优于 Pcap-Encoder（TLS-120 上 82.4% vs 63.7%），说明自监督特征提取尚不及专家特征工程
3. **未探索更高级的 split 策略**：仅对比了 per-packet 和 per-flow split，未深入研究 per-session、per-client、per-location、per-time 等更有挑战性的划分（论文自己也提到这些是 future work）
4. **仅评估了 6 个任务**：虽然覆盖了不同难度，但任务类型仍有限
5. **对 Pcap-Encoder 的泛化能力缺乏充分验证**：在更复杂场景（如跨网络环境、跨时间）下的表现未知
6. **未讨论对抗性场景**：如果攻击者知道模型使用协议头特征，能否通过协议头伪造来逃避分类？

## 5. 与其他方法对比

### 5.1 被揭穿的具体方法及其误导性声明

本文系统性地揭穿了以下 5 个代表性模型的声称：

**ET-BERT (Lin et al., WWW 2022)**
- 原始声称：在 CSTNET-TLS1.3 上 Macro F1 达 97.4%，声称 "pre-training allows the model to extract patterns from the encrypted payloads"
- 被揭穿的事实：在正确的 per-flow split + frozen encoder 设置下，TLS-120 Macro F1 仅 6.7%（下降 93%！）。随机初始化（无预训练）仍达 97.1%，证明预训练几乎无贡献
- 与本知识库中 ET-BERT 笔记的关联：ET-BERT 笔记中记录的 "ISCX-VPN-Service F1 达 98.9%" 等结果，均基于 per-packet split + unfrozen encoder 的错误设置
- 额外问题：ET-BERT 使用 ISCX-VPN 和 CSTNET-TLS1.3 同时用于上下游任务，存在数据集复用；移除所有 <80B 的包改变了任务定义

**YaTC (Zhao et al., AAAI 2023)**
- 原始声称：在多个任务上达到 98%+ 准确率
- 被揭穿的事实：在 per-flow split + frozen encoder 下，VPN-app F1 仅 44.3%，TLS-120 F1 仅 9.6%
- 额外问题：使用完全相同的数据集进行上下游训练；使用 micro F1-Score 误导性地高估性能

**NetMamba (Wang et al., ICNP 2024)**
- 原始声称：基于 Mamba 架构的高效流量分类
- 被揭穿的事实：在 per-flow split + frozen encoder 下，VPN-app F1 仅 28.4%，TLS-120 F1 仅 4.5%——是所有模型中最差的
- 额外问题：与 YaTC 一样使用完全相同的数据集进行上下游训练

**TrafficFormer (Zhou et al., IEEE S&P 2025)**
- 原始声称：在多个任务上取得优异性能
- 被揭穿的事实：在 per-flow split + frozen encoder 下，VPN-app F1 54.4%，TLS-120 F1 24.0%——在已有模型中相对最好，但仍远低于浅层模型
- 额外问题：丢弃 <10 流的类，限制其他类为 500 流，改变了原始数据分布

**netFound (Guthula et al., arXiv 2023)**
- 原始声称：网络安全基础模型
- 被揭穿的事实：在 per-flow split + frozen encoder 下，VPN-app F1 仅 15.3%，TLS-120 F1 仅 0.5%——几乎等于随机猜测
- 额外问题：使用 BERT Large 架构（1024 维嵌入），推理时间是 RF 的 2048 倍，但性能最差

### 5.2 与主流方法的本质区别

| 对比维度 | 已有表征学习模型 (ET-BERT 等) | 本文方法 (Benchmark + Pcap-Encoder) |
|---|---|---|
| 评估方法 | per-packet split + unfrozen encoder | per-flow split + frozen encoder 优先 |
| 表征来源 | 对加密 payload 做 MAE 预训练 | 仅从协议头部提取信息（忽略 payload） |
| 性能验证 | 在有数据泄漏的设置下报告 98%+ | 在无泄漏设置下真实评估 |
| 核心发现 | 声称预训练能从加密 payload 提取模式 | 证明 frozen encoder 表征质量很低，高性能来自 shortcut |
| 预训练有效性 | 声称预训练是关键 | 证明随机初始化（无预训练）几乎不影响性能 |

### 5.3 创新点分析（表格形式）

| 创新点 | 说明 |
|---|---|
| 首次系统性揭示 shortcut learning 问题 | 通过消融实验证明 per-packet split 的数据泄漏是已有模型高准确率的主要来源；移除 SeqNo/AckNo/Timestamp 后准确率从 97.4% 暴跌至 19.5% |
| Pcap-Encoder 的两阶段预训练 | Phase 1 用自编码器适配流量数据格式，Phase 2 用 Q&A 任务学习协议头语义；是唯一能产生有意义表征的模型 |
| Frozen encoder 评估范式 | 倡导冻结 encoder 来真正测试预训练表征的质量，而非通过 unfrozen fine-tuning "作弊" |
| 标准化 Benchmark 框架 | 定义了统一的数据清理、划分、采样、评估流程，为领域提供了可复现的评估标准 |
| 对已有模型的公平重新评估 | 在完全相同的设置下测试 5 个 SoA 模型，揭示真实性能差距 |
| 密码学角度的理论论证 | 从加密算法的随机性出发，论证对加密 payload 做 MAE 预训练在理论上不可行 |

### 5.4 适用场景

- 评估新的加密流量表征学习模型是否真正有效
- 为流量分类研究提供标准化的 benchmark 和评估方法论
- 指导研究者避免数据准备和模型训练中的常见陷阱
- 验证声称从加密 payload 提取信息的方法的可行性

### 5.5 方法对比表

| 方法 | 预训练架构 | 预训练任务 | 上下游数据集关系 | 数据划分 | Encoder 策略 | VPN-app (16) F1 | TLS-120 F1 |
|---|---|---|---|---|---|---|---|
| ET-BERT | BERT | MAE, SBP | 有交集 | Packet (原始) | Unfrozen | 97.0 (错误设置) | 96.8 (错误设置) |
| YaTC | ViT | MAE | 相同 | Packet (原始) | Unfrozen | 98.5 (错误设置) | 97.7 (错误设置) |
| NetMamba | Mamba | MAE | 相同 | Packet (原始) | Unfrozen | 98.4 (错误设置) | 96.8 (错误设置) |
| TrafficFormer | BERT | MAE, SODF | 有交集 | Packet (原始) | Unfrozen | 95.2 (错误设置) | 83.3 (错误设置) |
| netFound | BERT Large | MAE | 不同 | Flow (原始) | Unfrozen | 89.0 (错误设置) | 67.4 (错误设置) |
| ET-BERT | BERT | MAE, SBP | 有交集 | Flow (正确) | Frozen | 43.7 | 6.7 |
| YaTC | ViT | MAE | 相同 | Flow (正确) | Frozen | 44.3 | 9.6 |
| NetMamba | Mamba | MAE | 相同 | Flow (正确) | Frozen | 28.4 | 4.5 |
| TrafficFormer | BERT | MAE, SODF | 有交集 | Flow (正确) | Frozen | 54.4 | 24.0 |
| netFound | BERT Large | MAE | 不同 | Flow (正确) | Frozen | 15.3 | 0.5 |
| **Pcap-Encoder** | **T5** | **Autoencoder + Q&A** | **不同** | **Flow (正确)** | **Frozen** | **71.0** | **63.7** |
| Shallow (RF) | N/A | N/A | N/A | Flow (正确) | N/A | 81.1 | 78.0 |
| Shallow (XGBoost) | N/A | N/A | N/A | Flow (正确) | N/A | 82.1 | 82.0 |
| Shallow (LightGBM) | N/A | N/A | N/A | Flow (正确) | N/A | 82.6 | 82.4 |

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **硬件环境**：HPC Cluster，配备 NVIDIA Tesla V100 SXM2 GPU
- **实现框架**：Python + PyTorch
- **数据集**：ISCX-VPN（3 个任务）、USTC-TFC（2 个任务）、CSTNET-TLS1.3（1 个任务），共 6 个任务
- **评估设置**：per-flow split（正确）vs per-packet split（对照）；frozen encoder vs unfrozen encoder
- **训练策略**：K-Fold cross-validation（K=3）；训练集通过欠采样实现类别平衡
- **划分比例**：per-flow split 使用 7:1 比例；per-packet split 使用 8:1:1 比例
- **公平性保障**：所有模型和配置使用完全相同的训练/测试划分进行比较

### 6.2 数据集

| 数据集 | 任务 | 类别数 | 训练集 | 测试集 | 描述 |
|---|---|---|---|---|---|
| ISCX-VPN | VPN-binary | 2 | 100,000 | 110,594 | 是否加密 |
| ISCX-VPN | VPN-service | 6 | 120,000 | 111,368 | VoIP, Chat, ... |
| ISCX-VPN | VPN-app | 16 | 33,088 | 111,678 | Gmail, Vimeo, ... |
| USTC-TFC | USTC-binary | 2 | 100,000 | 609,332 | 是否恶意 |
| USTC-TFC | USTC-app | 20 | 69,680 | 609,477 | Gmail, Skype, ... |
| CSTNET-TLS1.3 | TLS-120 | 120 | 98,640 | 553,994 | 120 个网站 |

### 6.3 Baseline

- **已有表征学习模型**：ET-BERT（BERT）、YaTC（ViT）、NetMamba（Mamba）、TrafficFormer（BERT）、netFound（BERT Large）
- **浅层 ML 模型**：Random Forest、XGBoost、LightGBM、MLP，使用手工提取的协议头字段特征（Table 12 列出了 IPv4/IPv6/UDP/TCP 的具体字段，使用 Scapy 提取）
- **消融实验**：移除 IP 地址、移除整个头部、移除 payload、移除预训练、随机化 SeqNo/AckNo/Timestamp

### 6.4 评价指标

- **Accuracy（AC）**：正确预测的比例
- **Macro F1-Score（F1）**：各类别 F1 的算术平均，对少数类和多数类同等加权（推荐使用）
- **5-NN Purity**：嵌入空间中每个点的 5 个最近邻中同类的比例（用于评估嵌入质量）
- 论文批评了 micro F1-Score 的使用（偏向多数类），建议使用 macro F1-Score。YaTC, NetMamba 和 netFound 均使用 micro F1，这会误导性地高估多数类性能

### 6.5 关键实验结果（表格形式）

**Packet-level 分类（per-flow split, frozen encoder）—— Table 3**：

| 模型 | VPN-binary AC/F1 | VPN-service AC/F1 | VPN-app AC/F1 | USTC-binary AC/F1 | USTC-app AC/F1 | TLS-120 AC/F1 |
|---|---|---|---|---|---|---|
| ET-BERT | 84.7/84.6 | 71.7/64.2 | 59.2/43.7 | 100.0/100.0 | 84.9/79.6 | 10.9/6.7 |
| YaTC | 83.9/83.9 | 69.2/60.1 | 60.9/44.3 | 99.5/99.5 | 85.2/78.0 | 15.5/9.6 |
| NetMamba | 75.0/74.5 | 56.9/49.0 | 39.6/28.4 | 97.6/97.5 | 72.5/57.7 | 8.8/4.5 |
| TrafficFormer | 90.9/90.9 | 76.5/69.4 | 67.7/54.4 | 100.0/100.0 | 72.0/65.0 | 29.7/24.0 |
| netFound | 76.0/61.9 | 47.3/36.5 | 32.9/15.3 | 99.4/99.4 | 58.0/30.7 | 1.9/0.5 |
| **Pcap-Encoder** | **99.9/99.9** | **92.1/89.8** | **83.5/71.0** | **100.0/100.0** | **91.0/87.1** | **71.0/63.7** |

**Per-packet split vs Per-flow split 对比（unfrozen encoder, TLS-120）—— Table 5**：

| 模型 | Per-packet AC/F1 | Per-flow AC/F1 | 性能下降 |
|---|---|---|---|
| ET-BERT | 97.4/96.8 | 28.0/21.5 | ~70% |
| YaTC | 98.2/97.7 | 36.6/31.4 | ~60% |
| NetMamba | 97.4/96.8 | 40.7/35.3 | ~60% |
| TrafficFormer | 86.0/83.3 | 43.7/38.9 | ~45% |
| netFound | 71.0/67.4 | 39.9/35.2 | ~35% |
| **Pcap-Encoder** | 88.6/80.3 | **77.3/69.2** | **~10%** |

**Frozen vs Unfrozen Encoder 对比（per-flow split）—— Table 4**：

| 模型 | VPN-app Frozen/Unfrozen F1 | TLS-120 Frozen/Unfrozen F1 | Unfrozen 提升 |
|---|---|---|---|
| ET-BERT | 43.7/69.7 | 6.7/21.5 | +26.0/+14.8 |
| YaTC | 44.3/65.2 | 9.6/31.4 | +20.9/+21.8 |
| NetMamba | 28.4/65.9 | 4.5/35.3 | +37.5/+30.8 |
| TrafficFormer | 54.4/61.0 | 24.0/38.9 | +6.6/+14.9 |
| netFound | 15.3/57.3 | 0.5/35.2 | +42.0/+34.7 |
| **Pcap-Encoder** | **71.0/74.8** | **63.7/69.2** | **+3.8/+5.5** |

**Shallow 模型 vs Pcap-Encoder（per-flow split, frozen encoder, Macro F1）—— Table 8**：

| 模型 | VPN-app (16) | TLS-120 |
|---|---|---|
| RF | 81.1 | 78.0 |
| XGBoost | 82.1 | 82.0 |
| LightGBM | 82.6 | 82.4 |
| MLP | 65.1 | 68.8 |
| Pcap-Encoder | 71.0 | 63.7 |

**Flow-level 分类（per-flow split）—— Table 9**：

| 模型 | VPN-app Frozen/Unfrozen F1 | TLS-120 Frozen/Unfrozen F1 |
|---|---|---|
| ET-BERT | 38.9/54.3 | 13.8/51.5 |
| YaTC | 25.1/54.8 | 27.8/74.8 |
| NetMamba | 13.6/48.6 | 11.3/76.0 |
| TrafficFormer | 36.9/49.2 | 42.3/69.2 |
| netFound | 18.8/52.4 | 22.9/89.7 |
| **Pcap-Encoder** | **62.2/-** | **68.1/-** |

### 6.6 最令人惊讶的实验发现

1. **预训练几乎无贡献**：ET-BERT 随机初始化（无预训练）后 fine-tuning 仍达 97.1%（vs 预训练版本 97.4%），差异仅 0.3%。这意味着 ET-BERT 的整个预训练阶段（Masked Burst Modelling + Same-origin Burst Prediction）对下游任务几乎没有帮助

2. **Implicit flow ID 是主要 shortcut**：移除 SeqNo/AckNo/Timestamp 后，ET-BERT 在 TLS-120 上的准确率从 97.4% 暴跌至 19.5%（下降 80%）。这说明模型主要依赖这些隐式流标识符进行分类，而非理解流量语义

3. **Pcap-Encoder 是唯一鲁棒的模型**：从 per-packet 切换到 per-flow split 时，Pcap-Encoder 仅下降约 10%（88.6% → 77.3%），而其他模型下降 35%-70%。这证明 Pcap-Encoder 确实学到了有意义的表征，而非依赖 shortcut

4. **浅层模型全面碾压表征学习**：在正确的 per-flow split + frozen encoder 设置下，LightGBM（82.4%）在 TLS-120 上超过 Pcap-Encoder（63.7%）近 19 个百分点，超过 ET-BERT（6.7%）约 76 个百分点

5. **5-NN Purity 揭示嵌入空间质量**：frozen encoder 下 71% 的 ET-BERT 嵌入点没有同类邻居，unfrozen 后 97% 的点 5 个邻居全同类。这种极端对比说明原始表征完全没有语义结构

6. **计算效率的巨大差距**：netFound 推理时间是 RF 的 2048 倍，Pcap-Encoder 是 16 倍。即使 Pcap-Encoder 有最好的表征质量，其复杂度也引发了实际应用的可行性问题

7. **ET-BERT 在 TLS-120 上声称的 97.5% Macro F1 差距**：本文在正确设置下仅得 6.7%（frozen）/ 21.5%（unfrozen），差距高达 90+ 个百分点。原因包括：(i) 平衡策略差异（本文用欠采样 stress few-shot）；(ii) 可能存在未移除的 TLS Client Hello 包含明文 SNI

### 6.7 模型效率分析（Figure 6）

| 模型 | 相对训练时间（vs RF） | 相对推理时间（vs RF） |
|---|---|---|
| Shallow (RF) | 1x | 1x |
| NetMamba | 3x | 1x |
| YaTC | 2x | 16x |
| TrafficFormer | 4x | 4x |
| ET-BERT | 16x | 3x |
| Pcap-Encoder | 16x | 16x |
| netFound | 256x | 2048x |

### 6.8 局限性

1. **浅层模型仍优于 Pcap-Encoder**：手工特征 + RF/XGBoost/LightGBM 在所有任务上均超过 Pcap-Encoder，说明表征学习在当前阶段的实际价值有限
2. **Pcap-Encoder 计算开销大**：训练时间是 RF 的 16 倍，推理时间也是 16 倍
3. **未探索更高级的评估设置**：如 per-client、per-location、per-time 等更具挑战性的划分
4. **对对抗性攻击的鲁棒性未知**：如果训练集经过精心策划，模型是否仍能找到其他 shortcut？

## 7. 学习与应用

### 7.1 是否开源？

是。论文提供了代码、benchmark 数据集和方法论，地址为 https://github.com/SweetDanger-Polito/SweetDanger（论文中通过脚注标注）。

### 7.2 复现关键步骤

1. **下载数据集**：获取 ISCX-VPN、USTC-TFC、CSTNET-TLS1.3 三个公开数据集
2. **数据清理**：使用论文定义的协议过滤器（Table 13）过滤无关协议（ARP, DHCP, STUN 等），ISCX 含约 5%、USTC 含约 10% 的杂散包
3. **Per-flow split 划分**：基于 5-tuple 将流划分到训练集和测试集（7:1 比例）
4. **训练集平衡**：通过欠采样使各类别训练样本数一致
5. **模型加载**：从各原始仓库下载预训练模型权重
6. **Frozen encoder 评估**：冻结 encoder 权重，仅训练分类头
7. **Shortcut 分析**：分别随机化 SeqNo/AckNo/Timestamp，观察性能变化

### 7.3 关键超参数、预处理和训练细节

| 参数 | 值/说明 |
|---|---|
| K-Fold | K=3（2/3 训练，1/3 验证） |
| 训练集采样 | 欠采样至少数类样本数 |
| 流长度限制 | 超过 1000 包的流随机采样 1000 包 |
| ET-BERT 学习率 | Unfrozen: 2e-5, 20 epochs; Frozen: 2e-3, 60 epochs |
| YaTC 学习率 | 2e-3, batch 64, 200 epochs |
| TrafficFormer 学习率 | Unfrozen: 2e-5, 20 epochs; Frozen: 1e-4, 60 epochs; Early stop 5 epochs |
| netFound 学习率 | 单 GPU: 2.5e-6; 四 GPU: 1e-5; 100 epochs; Early stop 6 epochs |
| Pcap-Encoder Phase 1 | AdamW, lr=5e-4, linear scaling, batch 8, 15 epochs |
| Pcap-Encoder Phase 2 | 同 Phase 1 学习率, batch 24, 20 epochs |
| 浅层模型 | AutoGluon 自动调参 |
| 分类头 | 两层 MLP + ReLU |

### 7.4 能否迁移到其他任务？

- **网络安全领域的 ML 评估**：本文揭示的 shortcut learning 问题和评估方法论建议可直接迁移到入侵检测、恶意软件分类等任务。Arp et al. (2022) 已证明这些 pitfalls 在安全领域是系统性的
- **其他领域的表征学习评估**：frozen encoder 测试、per-flow split 等思想可推广到任何序列数据的表征学习评估
- **协议头部特征工程**：Table 12 列出的手工特征可直接用于其他流量分类任务的 baseline 构建
- **Pcap-Encoder 的 Q&A 预训练**：可扩展到更多协议字段（如 DNS 的 A/AAAA 记录、TLS 的 SNI 等）

### 7.5 对研究者的四条最佳实践建议

论文明确提出了四条最佳实践，这些建议对整个 AI for Networking 领域都有指导意义：

1. **Control for shortcut learning（控制捷径学习）**：深度模型特别容易利用非预期的模式（如 implicit flow ID）而非真正学习目标任务。研究者应主动识别和消除潜在的 shortcut

2. **Verify data integrity（验证数据完整性）**：确保数据集没有泄漏、伪影或虚假关联，这些会被 ML 模型立即利用为 shortcut。具体措施包括：使用 per-flow split 而非 per-packet split，避免数据集复用，检查隐式标识符

3. **Stress representation learning capabilities（压力测试表征学习能力）**：评估模型是否真正学到了有用的表征——冻结 encoder 进行下游训练。如果 frozen encoder 性能很差，说明预训练没有学到有意义的东西

4. **Consider cost-benefit trade-offs（考虑成本收益权衡）**：将提出的方案与简单 baseline 对比，判断深度学习模型的额外复杂度是否值得。如果浅层模型 + 手工特征就能达到更好效果，那么复杂模型的实际价值就值得质疑

### 7.6 对我的研究有什么启发？

1. **永远检查评估方法**：当结果好得不真实时，首先怀疑数据泄漏和 shortcut learning，而非庆祝模型的强大。本文证明了在加密流量分类领域，98% 的准确率可以完全来自评估缺陷

2. **Frozen encoder 是试金石**：如果 frozen encoder 的表征质量差（如 5-NN purity 中 71% 的点没有同类邻居），说明预训练没有学到有意义的东西。这是一个简单而有效的诊断工具

3. **数据划分至关重要**：在序列数据（流量、文本、时间序列）中，必须确保同一"实体"（流、文档、会话）的数据不会同时出现在训练集和测试集。per-packet split 的数据泄漏可导致 80% 的性能虚假提升

4. **简单 baseline 不可或缺**：任何复杂模型都应与使用专家特征的浅层模型对比，否则无法判断复杂度是否值得。本文中 LightGBM（82.4%）全面碾压所有表征学习模型（最高 63.7%）

5. **加密 payload 的信息极限**：强加密算法下 payload 字节之间没有语义关联，在加密 payload 上做 MAE 预训练理论上就不可行。未来的工作应该聚焦于协议头部、流量统计特征、时间模式等未加密信息

6. **"Too good to be true" 原则**：正如 Willinger et al. (2025) 所述，当 ML for networking 的结果看起来好得不真实时，它通常就是不真实的。研究者应保持批判性思维，而非盲目追求高准确率

7. **与 ET-BERT 笔记的交叉验证**：本知识库中 ET-BERT 笔记记录的 "ISCX-VPN-Service F1 达 98.9%" 等结果，均基于 per-packet split + unfrozen encoder 的错误设置。在正确的 per-flow split + frozen encoder 设置下，ET-BERT 在 TLS-120 上的 Macro F1 仅 6.7%——差距高达 92 个百分点。这提醒我们在阅读任何声称高准确率的论文时，都应仔细检查其评估设置

### 7.7 对未来流量分类研究的方向性启示

1. **回归基础**：与其追求更复杂的模型架构，不如先确保评估方法的正确性。本文证明了评估方法的改进（per-flow split + frozen encoder）比模型架构的改进更重要

2. **聚焦可解释特征**：协议头部的明文字段（如 TTL、Window Size、Packet Length）包含丰富的分类信息，且可解释、可迁移。未来的工作应该更好地利用这些特征

3. **重新审视预训练的价值**：在加密流量场景下，预训练的价值可能被严重高估。如果随机初始化就能达到相同效果，那么预训练阶段的计算开销就是浪费

4. **建立标准化 benchmark**：本文的 benchmark 框架（标准化的数据清理、划分、采样、评估流程）应该成为领域标准，避免每篇论文都使用自定义的评估设置

5. **探索更难的评估设置**：per-client、per-location、per-time 等划分策略更能反映真实部署场景，应该成为未来评估的标准

## 8. 总结

### 8.1 核心思想（不超过20字）

已有加密流量表征学习模型的高准确率源于数据泄漏而非真正表征。

### 8.2 速记版 Pipeline（3-5步）

1. 识别已有模型评估中的三个缺陷：per-packet split 数据泄漏、unfrozen encoder 预训练知识遗忘、加密 payload 上的无效 MAE 预训练
2. 构建标准化 benchmark：per-flow split + frozen encoder + balanced sampling + macro F1
3. 在统一设置下评估 5 个 SoA 模型，发现性能暴跌至 30%-40%
4. 提出 Pcap-Encoder（T5 + Autoencoder + Q&A），是唯一产生有意义表征的模型
5. 验证浅层 ML 模型 + 手工特征仍优于所有表征学习模型

## 9. Obsidian 知识链接

### 9.1 相关概念

- Representation Learning - 表征学习
- Shortcut Learning - 捷径学习
- Data Leakage - 数据泄漏
- Encrypted Traffic Classification - 加密流量分类
- Self-Supervised Learning - 自监督学习
- Transfer Learning - 迁移学习
- Few-Shot Learning - 小样本学习

### 9.2 相关方法

- BERT - Bidirectional Encoder Representations from Transformers
- T5 - Text-to-Text Transfer Transformer
- ViT - Vision Transformer
- Mamba - State Space Model
- Masked Autoencoder (MAE) - 掩码自编码器
- ET-BERT - Encrypted Traffic BERT
- YaTC - Yet another Traffic Classifier
- NetMamba - 基于 Mamba 的网络流量分类
- TrafficFormer - 预训练流量模型
- netFound - 网络安全基础模型
- Pcap-Encoder - 本文提出的协议头表征学习模型

### 9.3 相关任务

- Traffic Classification - 流量分类
- VPN Traffic Detection - VPN 流量检测
- Malware Traffic Detection - 恶意软件流量检测
- Website Fingerprinting - 网站指纹识别
- Protocol Identification - 协议识别

### 9.4 可更新的综述页面

- Encrypted Traffic Classification Survey
- Representation Learning for Networking
- ML Pitfalls in Network Security

### 9.5 可加入的对比表

- Representation Learning Models for Traffic Classification
- Encrypted Traffic Classification Methods
- Shortcut Learning in Network Security

## 10. 证据记录（表格形式）

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E1 | 实验结果 | Per-flow split + frozen encoder 下，ET-BERT 在 TLS-120 上 Macro F1 仅 6.7%（vs 原文报告的 96.8%，差距 92 个百分点） | Table 3 |
| E2 | 实验结果 | Per-packet split + unfrozen encoder 下所有模型达到 86-98% 准确率，但这是错误的评估设置 | Table 5 |
| E3 | 消融实验 | ET-BERT 在 TLS-120 上：移除 SeqNo/AckNo/Timestamp 后准确率从 97.4% 暴跌至 19.5%（下降 80%） | Table 6 |
| E4 | 消融实验 | ET-BERT 无预训练（随机初始化）仍达 97.1%（vs 预训练版本 97.4%），差异仅 0.3%，证明预训练几乎无贡献 | Table 6 |
| E5 | 5-NN 分析 | Frozen encoder 下 71% 的点没有同类邻居；unfrozen 后 97% 的点 5 个邻居全同类 | Figure 4 |
| E6 | 实验结果 | Pcap-Encoder 在 per-flow split frozen 下 TLS-120 F1 为 63.7%，远优于其他模型（最高 TrafficFormer 24.0%） | Table 3 |
| E7 | 实验结果 | 浅层模型（LightGBM）在 TLS-120 上 F1 为 82.4%，超过 Pcap-Encoder 的 63.7%（差距 18.7 个百分点） | Table 8 |
| E8 | 消融实验 | Pcap-Encoder 移除 payload 后 TLS-120 F1 不变（63.6% vs 63.7%），证明其确实忽略 payload | Table 7 |
| E9 | 效率分析 | netFound 推理时间是 RF 的 2048 倍，Pcap-Encoder 是 16 倍 | Figure 6 |
| E10 | 方法论 | 建议使用 per-flow split + frozen encoder + macro F1 作为标准评估方法 | Section 4 |
| E11 | 实验结果 | 从 per-packet 切换到 per-flow split 时，Pcap-Encoder 仅下降约 10%（88.6% → 77.3%），而其他模型下降 35%-70% | Table 5 |
| E12 | 实验结果 | Pcap-Encoder unfrozen 提升仅约 5%（frozen 63.7% → unfrozen 69.2%），而 ET-BERT 提升约 15%（6.7% → 21.5%），说明 Pcap-Encoder 的预训练表征已包含大部分有用信息 | Table 4 |
| E13 | 消融实验 | Pcap-Encoder 移除 IP 地址后 TLS-120 F1 从 63.7% 降至 13.0%，移除整个头部后暴跌至 1.5%，证明协议头部是主要信息来源 | Table 7 |
| E14 | 消融实验 | Pcap-Encoder Phase 1 (Autoencoder) + Phase 2 (Q&A) 的消融：仅用 Q&A 时 TLS-120 F1 为 57.2%（下降 6.5%），仅用 base T5 时暴跌至 2.5% | Table 11 |
| E15 | 实验结果 | 浅层模型移除 IP 地址后，TLS-120 F1 从 78.0% 降至 39.4%（RF），但仍然超过 Pcap-Encoder（63.7% vs 39.4% 时浅层仍有优势） | Table 8 |
| E16 | 特征重要性 | Random Forest 在 TLS-120 per-packet split 下：有 IP 时最重要特征是 SRC IP3（0.135）；移除 IP 后变为 SeqNo/AckNo 等 implicit flow ID | Figure 5 |
| E17 | 实验结果 | Flow-level 分类中，netFound 在 TLS-120 unfrozen 下 F1 达 89.7%，是所有模型中最高的——但其 frozen 下仅 22.9%，说明依赖 fine-tuning 而非预训练表征 | Table 9 |
| E18 | 实验结果 | ET-BERT 声称的 TLS-120 Macro F1 97.5% 与本文正确设置下的 6.7% 差距巨大，原因包括：(i) 平衡策略差异；(ii) 可能存在未移除的 TLS Client Hello 包含明文 SNI | Section 6.2 |

## 11. 原始资料链接

- 论文发表于 ACM SIGCOMM 2025，2025 年 9 月 8-11 日，葡萄牙科英布拉
- DOI: https://doi.org/10.1145/3718958.3750498
- 作者单位：Politecnico di Torino（都灵理工大学），意大利
- 资助来源：Huawei Technologies France 项目 "AISN - AI Secured Networks"；中国国家留学基金委（CSC）；意大利 MUR 的 AI4CTI FISA 项目；SERICS 项目（欧盟 NextGenerationEU）
- 代码和数据：https://github.com/SweetDanger-Polito/SweetDanger
- 相关工具：Scapy（https://scapy.net）用于特征提取，AutoGluon 用于浅层模型调参

## 12. 后续问题

1. **更高难度的评估设置**：per-client、per-location、per-time 等划分策略下模型表现如何？这更接近真实部署场景
2. **Pcap-Encoder 的改进方向**：能否设计更轻量的架构（如小型 Transformer 或知识蒸馏）在保持表征质量的同时降低计算开销？
3. **浅层模型的特征工程自动化**：能否用 NAS 或 AutoML 自动发现比手工特征更好的协议头特征组合？
4. **表征学习的正确应用方式**：在什么条件下表征学习才能真正超越浅层模型？是否需要更大规模、更多样化的预训练数据？
5. **跨域泛化**：在源网络上预训练的模型能否有效迁移到目标网络？不同网络环境的流量分布差异对表征质量的影响如何？
6. **对抗性场景**：如果攻击者知道模型使用协议头特征，能否通过协议头伪造来逃避分类？
7. **与其他领域的类比**：shortcut learning 问题在 NLP 和 CV 中是如何被解决的？这些解决方案能否迁移到流量分类领域？

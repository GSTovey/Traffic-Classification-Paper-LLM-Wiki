---
type: paper
title_original: "Towards Fine-Grained Webpage Fingerprinting at Scale"
title_cn: "面向大规模细粒度网页指纹攻击"
authors:
  - Xiyuan Zhao
  - Xinhao Deng
  - Qi Li
  - Yunpeng Liu
  - Zhuotao Liu
  - Kun Sun
  - Ke Xu
year: 2024
venue: "CCS"
doi: "10.1145/3658644.3690211"
url: ""
pdf: "00-inbox/PDFs/2024-CCS-Towards_fine-grained_webpage_fingerprinting_at_scale.pdf"
mineru_md: "02-parsed-markdown/2024-CCS-Towards_fine-grained_webpage_fingerprinting_at_scale.md"
status: processed
reading_level: L2
research_area:
  - website-fingerprinting
  - traffic-classification
  - privacy-attack
task:
  - webpage-fingerprinting
  - multi-tab-identification
  - fine-grained-traffic-classification
method:
  - metric-learning
  - multi-label-classification
  - data-augmentation
  - proxy-based-loss
  - sample-based-loss
  - k-NN-classifier
dataset:
  - Alexa-1000-webpages
  - unmonitored-9000-webpages
code: "https://github.com/OscarWPF/Oscar"
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

# Oscar: 面向大规模细粒度网页指纹攻击

## 0. 基础信息

| 字段 | 内容 |
|------|------|
| 论文全称 | Towards Fine-Grained Webpage Fingerprinting at Scale |
| 作者 | Xiyuan Zhao, Xinhao Deng, Qi Li, Yunpeng Liu, Zhuotao Liu, Kun Sun, Ke Xu |
| 机构 | 清华大学 INSC & BNRist; 中关村实验室; George Mason University |
| 发表年份 | 2024 |
| 会议/期刊 | CCS 2024 |
| 关键词 | Webpage Fingerprinting, Tor, Privacy, Multi-label Metric Learning, Data Augmentation |
| 代码 | https://github.com/OscarWPF/Oscar |

## 1. 一句话总结

提出 Oscar，一种基于多标签度量学习的大规模细粒度网页指纹攻击框架，能够在多标签（多 tab）场景下从混淆流量中识别不同网页，包括同一网站的不同子页面，Recall@5 相比现有攻击平均提升 88.6%，首次将监控网页规模扩展到 1000 个。

## 2. 摘要翻译

**原文：**
Website Fingerprinting (WF) attacks can effectively identify the websites visited by Tor clients via analyzing encrypted traffic patterns. Existing attacks focus on identifying different websites, but their accuracy dramatically decreases when applied to identify fine-grained webpages, especially when distinguishing among different subpages of the same website. WebPage Fingerprinting (WPF) attacks face the challenges of highly similar traffic patterns and a much larger scale of webpages. Furthermore, clients often visit multiple webpages concurrently, increasing the difficulty of extracting the traffic patterns of each webpage from the obfuscated traffic. In this paper, we propose Oscar, a WPF attack based on multi-label metric learning that identifies different webpages from obfuscated traffic by transforming the feature space. Oscar can extract the subtle differences among various webpages, even those with similar traffic patterns. In particular, Oscar combines proxy-based and sample-based metric learning losses to extract webpage features from obfuscated traffic and identify multiple webpages. We prototype Oscar and evaluate its performance using traffic collected from 1,000 monitored webpages and over 9,000 unmonitored webpages in the real world. Oscar demonstrates an 88.6% improvement in the multi-label metric Recall@5 compared to the state-of-the-art attacks.

**中文翻译：**
网站指纹（WF）攻击可以通过分析加密流量模式有效识别 Tor 客户端访问的网站。现有攻击专注于识别不同网站，但当应用于识别细粒度网页时，其准确率急剧下降，特别是区分同一网站的不同子页面时。网页指纹（WPF）攻击面临高度相似的流量模式和更大规模网页的挑战。此外，客户端经常同时访问多个网页，增加了从混淆流量中提取每个网页流量模式的难度。本文提出 Oscar，一种基于多标签度量学习的 WPF 攻击，通过变换特征空间从混淆流量中识别不同网页。Oscar 可以提取各种网页之间的细微差异，即使是流量模式相似的网页。具体而言，Oscar 结合基于代理和基于样本的度量学习损失，从混淆流量中提取网页特征并识别多个网页。我们原型化了 Oscar 并使用从 1000 个监控网页和超过 9000 个非监控网页收集的真实流量评估其性能。Oscar 在多标签度量 Recall@5 上相比现有攻击平均提升 88.6%。

## 3. 方法动机（Motivation）

### 3.1 问题背景与痛点

- **网站指纹 vs 网页指纹**：现有 WF 攻击专注于识别不同网站，但当应用于细粒度网页识别时性能急剧下降
- **高相似性挑战**：同一网站的不同网页共享相似布局，导致流量模式高度相似，难以在原始特征空间中区分
- **多标签（多 tab）场景**：客户端通常同时访问多个网页，导致流量混淆，提取单个网页的模式更加困难
- **大规模网页监控**：网页规模约为网站的 50 倍，现有方法难以扩展到数千个监控网页
- **类崩溃问题**：在多标签场景下，基于度量学习的方法容易出现类崩溃（所有网页流量聚集到一点）

### 3.2 核心直觉

- **细微差异存在**：即使同一网站的不同网页共享相似布局，其内容和资源仍存在差异，导致局部流量模式的细微变化
- **度量学习变换**：通过度量学习变换特征空间，可以将不同网页的流量分离，在新特征空间中提取细微差异
- **多标签度量学习**：结合基于代理和基于样本的损失，解决多标签场景下的类崩溃问题

## 4. 方法设计（Method Design）

### 4.1 整体流程

```
原始流量 → 数据增强（样本间+样本内） → 特征变换（多标签度量学习） → 网页识别（双 k-NN 分类器）
                                          ↓
                                    代理损失 + 样本损失
                                    (聚合同类 + 分离异类)
```

### 4.2 三大模块

**模块一：数据增强（Data Augmentation）**
- **输入**：原始多标签流量样本
- **处理**：
  - **样本间增强（Inter-sample）**：将两个样本的流量按时间顺序组合，增强不同网页组合的多样性
  - **样本内增强（Intra-sample）**：在单个样本内交换数据包，适应相同网页组合中数据包顺序的变化
- **输出**：增强后的流量样本
- **关键点**：专门针对多标签流量设计的增强方法

**模块二：特征变换（Feature Transformation）**
- **输入**：原始样本和增强样本
- **处理**：
  - 基于 DF（Deep Fingerprint）架构的特征变换模型
  - **代理损失（Proxy-based Loss）**：为每个网页设置代理，聚合同一网页的相关样本
  - **样本损失（Sample-based Loss）**：分离低标签相关性的不相关样本
  - 结合两种损失训练特征变换模型
- **输出**：特征变换模型，将原始特征空间变换到新空间
- **关键点**：解决多标签场景下的类崩溃问题

**模块三：网页识别（Webpage Identification）**
- **输入**：变换后的特征空间中的流量样本
- **处理**：
  - **代理-样本距离分类器**：基于代理和样本之间的距离
  - **样本-样本距离分类器**：基于样本之间的距离
  - 结合两个 k-NN 分类器的分数进行预测
- **输出**：识别的网页标签（多标签）
- **关键点**：利用变换后特征空间的分布特征进行高效识别

### 4.3 关键公式

- **代理损失**：基于代理的损失函数，拉近同一网页的样本与代理的距离
- **样本损失**：基于样本的损失函数，推远不同网页的样本
- **多标签损失**：结合代理损失和样本损失，解决类崩溃问题
- **k-NN 分类**：基于距离的分类，结合代理-样本和样本-样本距离

### 4.4 优缺点

**优势：**
- 首次实现多标签（多 tab）场景下的大规模细粒度网页指纹
- 多标签度量学习有效解决类崩溃问题
- 样本间和样本内增强提高泛化能力
- 双 k-NN 分类器提高识别准确性
- 首次收集多标签网页流量数据集

**局限：**
- 仍需大量监控网页的训练数据
- 在极大规模网页（如数万）下性能可能下降
- 依赖于网页间存在细微差异的假设

## 5. 与其他方法对比（Comparison）

### 5.1 创新点

| 创新点 | 本文方法 | 现有方法 |
|--------|----------|----------|
| 识别目标 | 细粒度网页（同一网站不同子页面） | 网站级别 |
| 多标签场景 | 支持（多 tab 同时访问） | 大多不支持 |
| 网页规模 | 1000+ 监控网页 | 通常 < 100 |
| 度量学习 | 多标签度量学习（代理+样本） | 单标签或对比学习 |
| 数据增强 | 专门针对多标签流量 | 通用增强 |

### 5.2 与 Baseline 对比

与现有 WF 和 WPF 攻击对比：
- k-FP、DF、Tik-Tok、TF（WF 攻击）
- MWF、BAPM、TMWF、ARES（多标签 WF 攻击）
- FineWP、BurNet、GAP-WF（WPF 攻击）

**关键差异**：
- 现有方法在网页识别上性能大幅下降，Oscar 保持高性能
- 现有方法大多不支持多标签场景，Oscar 专门设计
- Oscar 首次将监控规模扩展到 1000+ 网页

## 6. 实验表现（Experiments）

### 6.1 数据集

| 数据集 | 描述 | 规模 |
|--------|------|------|
| 监控网页 | 1000 个监控网页 | 1,000 |
| 非监控网页 | 超过 9000 个非监控网页 | 9,000+ |
| 闭世界设置 | 仅监控网页 | - |
| 开放世界设置 | 监控+非监控网页 | - |

**数据集特点**：首个针对每个网页作为独立类别的多标签网页流量数据集，同时访问的网页数量动态变化。

### 6.2 Baseline 方法

- **WF 攻击**：k-FP, DF, Tik-Tok, TF, MWF, BAPM, NetCLR, TMWF, ARES
- **WPF 攻击**：FineWP, BurNet, GAP-WF

### 6.3 评估指标

- Recall@5（多标签度量）
- Precision
- Recall
- F1-score

### 6.4 关键结果

**闭世界设置：**
- Recall@5 平均提升 88.6%（与现有攻击对比）
- 在 1000 个监控网页上表现优异

**开放世界设置：**
- Recall@5 平均提升 76.7%
- 在 9000+ 非监控网页上保持高性能

**特征变换效果：**
- 变换后不同网页的流量特征相似度平均降低 52.92%
- 证明度量学习有效分离不同网页

**可扩展性：**
- 在不同规模的监控网页上均优于现有方法
- 随着网页规模增加，Oscar 性能下降较慢

## 7. 学习与应用（Learning & Application）

### 7.1 开源情况

- **代码**：https://github.com/OscarWPF/Oscar
- **数据集**：作者发布了首个多标签网页流量数据集
- **可复现性**：提供了完整的代码和数据集

### 7.2 可迁移价值

- **度量学习**：多标签度量学习方法可应用于其他细粒度分类任务
- **数据增强**：样本间和样本内增强方法可应用于其他序列数据分析
- **特征变换**：特征空间变换方法可应用于其他需要区分相似模式的任务
- **多标签分类**：双分类器结合方法可应用于其他多标签分类场景

### 7.3 实际应用场景

- **网页监控**：细粒度监控用户访问的具体网页
- **隐私评估**：评估网页级别隐私保护的有效性
- **内容过滤**：基于网页内容的细粒度过滤

## 8. 总结（Summary）

### 8.1 核心思想

Oscar 的核心思想是通过多标签度量学习变换特征空间，从混淆的多标签流量中提取不同网页的细微差异。样本间和样本内数据增强提高泛化能力，代理损失和样本损失结合解决类崩溃问题，双 k-NN 分类器实现准确的多标签网页识别。

### 8.2 快速流程图

```
输入：多标签流量样本（多 tab 同时访问）
  ↓
数据增强（样本间组合 + 样本内交换）
  ↓
特征变换（多标签度量学习：代理损失 + 样本损失）
  ↓
网页识别（双 k-NN 分类器：代理-样本 + 样本-样本距离）
  ↓
输出：识别的网页标签（多标签）
```

## 9. 知识链接（Knowledge Links）

- [[website-fingerprinting]]：本文的背景任务，Oscar 是其细粒度扩展
- [[traffic-classification]]：更广泛的任务类别
- [[contrastive-learning]]：度量学习与对比学习密切相关
- [[encrypted-traffic-analysis]]：加密流量分析的应用
- [[few-shot-traffic-learning]]：度量学习在少样本场景中的应用

## 10. 证据记录（Evidence）

| 声明 | 证据 | 来源 |
|------|------|------|
| Recall@5 平均提升 88.6% | 闭世界设置，与现有攻击对比 | 论文 §6 实验结果 |
| Recall@5 平均提升 76.7% | 开放世界设置 | 论文 §6 实验结果 |
| 特征相似度降低 52.92% | 特征变换前后对比 | 论文 §4 |
| 网页规模约为网站的 50 倍 | 文献引用 | 论文 §1 |
| 首个多标签网页流量数据集 | 作者声明 | 论文 §1 |

## 11. 原始资料链接（Source Links）

- **PDF**：`00-inbox/PDFs/2024-CCS-Towards_fine-grained_webpage_fingerprinting_at_scale.pdf`
- **MinerU MD**：`02-parsed-markdown/2024-CCS-Towards_fine-grained_webpage_fingerprinting_at_scale.md`

## 12. 后续问题（Open Questions）

1. **更大规模网页**：在数万甚至数十万监控网页下，Oscar 的可扩展性如何？
2. **动态网页**：对于动态生成内容的网页（如社交媒体 feed），识别准确性如何？
3. **防御机制**：是否存在针对 Oscar 的有效防御方法？
4. **实时识别**：Oscar 的计算复杂度是否满足实时识别需求？
5. **跨网站泛化**：在未见过的网站上，Oscar 的泛化能力如何？

---
type: paper
title_original: "THE ADVANCED COMPUTING SYSTEMS ASSOCIATION"
title_cn: ""
authors: []
year: 2026
venue: NSDI
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-NSDI-SPLIDT__Partitioned_Decision_Trees_for_Scalable_Stateful_Inference_at_Line_Rate.pdf"
mineru_md: "02-parsed-markdown/2026-NSDI-SPLIDT__Partitioned_Decision_Trees_for_Scalable_Stateful_Inference_at_Line_Rate.md"
status: processed
reading_level: L2
research_area: []
task: []
method: []
dataset: []
code: unknown
relevance: medium
created: "2026-09-29"
updated: "2026-09-29"
---

# THE ADVANCED COMPUTING SYSTEMS ASSOCIATION

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | THE ADVANCED COMPUTING SYSTEMS ASSOCIATION |
| 年份 | 2026 |
| 会议/期刊 | NSDI |
| PDF | [[2026-NSDI-SPLIDT__Partitioned_Decision_Trees_for_Scalable_Stateful_Inference_at_Line_Rate.pdf]] |
| MinerU Markdown | [[2026-NSDI-SPLIDT__Partitioned_Decision_Trees_for_Scalable_Stateful_Inference_at_Line_Rate.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
Machine learning (ML) is increasingly being deployed in programmable data planes (switches and SmartNICs) to enable real-time traffic analysis, security monitoring, and innetwork decision-making. Decision trees (DTs) are particu larly well-suited for these tasks due to their interpretability and compatibility with data-plane architectures, i.e., match action tables (MATs). However, existing in-network DT im plementations are constrained by the need to compute all input features upfront, forcing models to rely on a small, fixed set of features per flow. This significantly limits model accuracy and scalability under stringent hardware resource constraints. We present SPLIDT, a system that rethinks DT deployment in the data plane by enabling partitioned inference over sliding windows of packets. SPLIDT introduces two key innovations: (1) it groups individual subtrees of a DT into partitions and allows each subtree to have its own feature set, and (2) it lever ages an in-band control channel (via recirculation) to reuse data-plane resources (both stateful registers and match keys) across partitions at line rate. These insights allow SPLIDT to scale the number of stateful features a model can use with out exceeding hardware limits. To support this architecture, SPLIDT incorporates a custom training and design-space exploration (DSE) framework that jointly optimizes feature allocation, tree partitioning, and DT model depth. Evaluation across multiple real-world datasets shows that SPLIDT achieves higher accuracy while supporting up to 5 more stateful features than prior approaches (e.g., NetBeacon and Leo). It maintains the same low time-to-detection (TTD) as these systems, while scaling to millions of flows with minimal recirculation overhead ( 0.05%).

## 3. 方法分析
- 输入：论文所研究的网络流量、协议、系统或安全数据（以全文为准）。
- 处理：论文提出的方法或分析流程（摘要级自动提取，待核验）。
- 输出：分类、检测、预测、攻击/防御或系统验证结果。

## 4. 实验表现
- 数据集：待从全文核验。
- Baseline：unknown。
- 指标与数值：不补造，待表格核验。

## 5. 局限性与复现建议
- 当前笔记完成自动入库和摘要级分析，未替代人工深读。
- 先核验数据来源、代码状态、划分和指标，再决定复现等级。

## 6. 知识链接
- [[traffic-classification]]
- [[encrypted-traffic-analysis]]

## 7. 证据状态
- MinerU：已完成；解析质量需人工抽查。
- Bib 元数据：待官方 API/论文首页核验。


## 深度分析（自动证据提取，需人工复核）

### 研究问题与证据
- 主题线索：encrypted traffic, malicious traffic, anomaly, tor, adversarial, traffic classification。
- 摘要证据：Machine learning (ML) is increasingly being deployed in programmable data planes (switches and SmartNICs) to enable real-time traffic analysis, security monitoring, and innetwork decision-making. Decision trees (DTs) are particu larly well-suited for these tasks due to their interpretability and compatibility with data-plane architectures, i.e., match action tables (MATs). However, existing in-network DT im plementations are constrained by the need to compute all input features upfront, forcing models to rely on a small, fixed set of features per flow. This significantly limits model accuracy and scalability under stringent hardware resource constraints. We present SPLIDT, a system that rethinks DT deployment in the data plane by enabling partitioned inference over sliding windows of packets. SPLIDT introduces two key innovations: (1) it groups individual subtrees of a DT into partitions and allows each subtree to have its own feature set, and (2) it lever ages an in-band control channel (via recirculation) to reuse data-plane resources (both stateful registers and match keys) across partitions at line rate. These insights allow SPLIDT to scale the number of stateful features a model can use with out exceeding hardware limits. To support this architecture, SPLIDT incorporates a custom training and design-space exploration (DSE) framework that jointly optimizes feature allocation, tree partitioning, and DT model depth. Evaluation across multiple real-world datasets shows that SPLIDT achieves higher accuracy while supporting up to 5 more stateful features than prior approaches (e.g., NetBeacon and Leo). It maintains the same low time-to-detection (TTD) as these systems, while scaling to millions of flows with minimal recirculation overhead ( 0.05%).

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


## 深度分析（并行深度分析更新 2026-09-29）

### 方法、实验与证据
SPLIDT以分区决策树将有状态特征推理映射到可编程交换机，使用HyperMapper多目标搜索F1/资源配置；Tofino1实测，支持D1–D7数据集。固定等大小窗口和可信数据中心威胁模型是主要边界，提供artifact实现线索。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。

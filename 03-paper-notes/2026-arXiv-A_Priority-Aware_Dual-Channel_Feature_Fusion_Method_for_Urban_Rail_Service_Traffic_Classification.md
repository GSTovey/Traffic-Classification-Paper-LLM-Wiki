---
type: paper
title_original: "A Priority-Aware Dual-Channel Feature Fusion Method for Urban Rail Service Trafic Classification"
title_cn: ""
authors: []
year: 2026
venue: arXiv
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-arXiv-A_Priority-Aware_Dual-Channel_Feature_Fusion_Method_for_Urban_Rail_Service_Traffic_Classification.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-A_Priority-Aware_Dual-Channel_Feature_Fusion_Method_for_Urban_Rail_Service_Traffic_Classification.md"
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

# A Priority-Aware Dual-Channel Feature Fusion Method for Urban Rail Service Trafic Classification

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | A Priority-Aware Dual-Channel Feature Fusion Method for Urban Rail Service Trafic Classification |
| 年份 | 2026 |
| 会议/期刊 | arXiv |
| PDF | [[2026-arXiv-A_Priority-Aware_Dual-Channel_Feature_Fusion_Method_for_Urban_Rail_Service_Traffic_Classification.pdf]] |
| MinerU Markdown | [[2026-arXiv-A_Priority-Aware_Dual-Channel_Feature_Fusion_Method_for_Urban_Rail_Service_Traffic_Classification.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
With the deep integration of 5G and IoT in urban rail transit, service trafic grows explosively and accurate classification of heterogeneous service flows is essential for safe and eficient railway operations. Urban rail communication systems are subject not only to operational disturbances such as equipment failures and maintenance interference, but also to complex transmission patterns characterized by the interleaving of multi-service trafic flows. Under these operating conditions, the widespread deployment of proprietary protocols and the high prevalence of encrypted trafic further diminish the applicability of conventional port based and Deep Packet Inspection (DPI) classification methods. To address these challenges, we propose a priority-aware dual-channel feature fusion framework. Raw trafic bytes and statistical features are mapped into grayscale images and processed by a dual-branch architecture: a transfer learning-enhanced ResNet extracts fine-grained byte-level textures, while a lightweight CNN captures macroscopic statistical patterns. A channel attention mechanism dynamically recalibrates cross-modal features, and a novel Priority-Sensitive Loss (PSL) that integrates business-criticality awareness with class-balance weighting to maximize recall for safety-critical services. Evaluated on a real-world urban rail dataset using priority-weighted metrics, the method achieves 98.74% accuracy and 99.24% weighted recall, with recall of 99.94% and 99.41% on the two safety-critical services:Communication-Based Train Control(CBTC) and Emergency Radio Dispatch(ERD), providing a reliable classification foundation for priority-aware resource scheduling in urban rail communications. With only 0.18M parameters and 0.4–0.7 ms end-to-end latency, ofering an excellent balance between high-precision classification, low inference latency, and edge-deployment feasibility

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
- 主题线索：anomaly, tor, graph neural, transformer, traffic classification。
- 摘要证据：With the deep integration of 5G and IoT in urban rail transit, service trafic grows explosively and accurate classification of heterogeneous service flows is essential for safe and eficient railway operations. Urban rail communication systems are subject not only to operational disturbances such as equipment failures and maintenance interference, but also to complex transmission patterns characterized by the interleaving of multi-service trafic flows. Under these operating conditions, the widespread deployment of proprietary protocols and the high prevalence of encrypted trafic further diminish the applicability of conventional port based and Deep Packet Inspection (DPI) classification methods. To address these challenges, we propose a priority-aware dual-channel feature fusion framework. Raw trafic bytes and statistical features are mapped into grayscale images and processed by a dual-branch architecture: a transfer learning-enhanced ResNet extracts fine-grained byte-level textures, while a lightweight CNN captures macroscopic statistical patterns. A channel attention mechanism dynamically recalibrates cross-modal features, and a novel Priority-Sensitive Loss (PSL) that integrates business-criticality awareness with class-balance weighting to maximize recall for safety-critical services. Evaluated on a real-world urban rail dataset using priority-weighted metrics, the method achieves 98.74% accuracy and 99.24% weighted recall, with recall of 99.94% and 99.41% on the two safety-critical services:Communication-Based Train Control(CBTC) and Emergency Radio Dispatch(ERD), providing a reliable classification foundation for priority-aware resource scheduling in urban rail communications. With only 0.18M parameters and 0.4–0.7 ms end-to-end latency, ofering an excellent balan

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：未检测到明确 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


### 并行深度分析（2026-09-29）
- 方法/问题：A priority-aware dual-channel framework maps raw bytes and statistical features to grayscale images, uses transfer-learning ResNet plus a second branch and fuses representations for urban-rail service traffic classification. Missing: channel architecture, priority objective, rail datasets, baselines, metrics and deployment constraints.
- 证据边界：以上仅使用对应 MinerU 解析稿摘要及可稳定提取段落；未提取到的数值、数据集、代码和参数均不作推断。
- 复现建议：先核对原文表格、附录、代码仓库和数据划分，再确定 L3/L4 复现。

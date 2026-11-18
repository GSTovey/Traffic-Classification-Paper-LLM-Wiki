---
type: "paper"
title_original: "SEDMS: Space-Efficient Dynamic Metric Selection for Streaming Telemetry in Edge Networks"
title_cn: "SEDMS：边缘流式遥测的低空间动态指标选择"
authors: ["Shuyu Pei", "Kun Xie", "Jigang Wen", "Dafang Zhang", "Yuxiang Chen", "Kun Huang", "Wei Liang", "Gaogang Xie"]
year: 2026
venue: "TON"
source_version: "IEEE Transactions on Networking 34，8091–8106。输入 PDF 为作者稿，卷页来自 Crossref。"
doi: "10.1109/ton.2026.3748593"
url: "https://doi.org/10.1109/ton.2026.3748593"
pdf: "00-inbox/PDFs/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks.pdf"
mineru_md: "02-parsed-markdown/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks.md"
status: "processed"
reading_level: "L3"
research_area: ["网络遥测", "流式特征选择", "漂移"]
task: ["逐设备遥测指标选择", "辅助聚类与异常识别"]
method: ["矩阵 sketch", "谱稀疏选择", "协方差误差更新"]
dataset: ["N-BaIoT：IoT1/IoT2", "Kitsune：KitsuneIoT1/KitsuneIoT2"]
code: "https://github.com/SyCode2005/SEDMS"
relevance: "high"
created: "2026-11-18"
updated: "2026-11-18"
metadata_source: "Crossref"
source_sha256: "332ca58cd22e70dcab7435b4fe266b03901ea0ddf4c2fb3ad3942e3aa1ea66f8"
internal_citation_count: 0
citation_impact: 0.8
composite_weight: 0.68
citation_count_scope: "verified DOI or normalized complete titles in vault References; lower bound"
citation_count_verified: "2026-11-18"
---

# SEDMS: Space-Efficient Dynamic Metric Selection for Streaming Telemetry in Edge Networks

## 0. 论文基础信息

| 项目 | 内容 |
| --- | --- |
| 原文标题 | SEDMS: Space-Efficient Dynamic Metric Selection for Streaming Telemetry in Edge Networks |
| 中文标题 | SEDMS：边缘流式遥测的低空间动态指标选择 |
| 作者 | Shuyu Pei、Kun Xie、Jigang Wen、Dafang Zhang、Yuxiang Chen、Kun Huang、Wei Liang、Gaogang Xie |
| 年份 | 2026 |
| 会议/期刊及版本 | IEEE Transactions on Networking 34，8091–8106。输入 PDF 为作者稿，卷页来自 Crossref。 |
| DOI | 10.1109/ton.2026.3748593 |
| 题录来源 | Crossref |
| 研究方向 | 网络遥测、流式特征选择、漂移 |
| 任务类型 | 逐设备遥测指标选择、辅助聚类与异常识别 |
| 方法关键词 | 矩阵 sketch、谱稀疏选择、协方差误差更新 |
| 数据集 | N-BaIoT：IoT1/IoT2；Kitsune：KitsuneIoT1/KitsuneIoT2 |
| 开源状态 | 论文给出作者代码仓库，原始流量沿用 N-BaIoT 与 Kitsune 来源。 |
| PDF | [[00-inbox/PDFs/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks.pdf]] |
| MinerU Markdown | [[02-parsed-markdown/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks.md]] |

题录核验见 [出版记录](https://doi.org/10.1109/ton.2026.3748593)。

## 1. 一句话总结

SEDMS 为每台边缘设备维护固定大小的遥测矩阵 sketch，在协方差近似失效时更新要上报的指标子集。

## 2. 摘要翻译

### 2.1 摘要原文

见 [[00-inbox/PDFs/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks.pdf]] 第 1 页 Abstract。

### 2.2 摘要中文翻译

实时上报全部指标会占用边缘内存和链路，固定子集又可能跟不上通信分布变化。SEDMS 以有限矩阵 sketch 摘要数据，在摘要上做谱稀疏指标选择，并以协方差近似误差决定是否重选。作者在设备流量聚类和异常检测两类场景评估判别表现和速度。

## 3. 方法动机

不同设备和工作负载下，有区分力的指标会改变。类标签不一定及时可用，网关需要用固定状态保持足够的相关结构，并识别何时原指标子集失去代表性（§I、§III）。

### 3.4 问题发现路径

| 阶段 | 内容 |
| --- | --- |
| 现象观察 | 边缘设备的流量会换主导类别，指标相关结构也随之变化。 |
| 痛点提炼 | 原始快照随时间累积占空间，静态选择不能利用新的结构。 |
| 问题转化 | 固定内存能否维持足够的协方差信息以选出有效指标？ |
| 文献定位 | 用固定子集、动态选择以及不同选择比例的基线区分更新和压缩作用。 |

### 3.5 科学假设形成

使用固定行数的摘要并按协方差变化更新，可以维持低上报比例下的任务质量。

验证方式　统一快照顺序、设备分组及遥测比例，比较静态与动态方法。若更新触发只反映背景切换而下游质量无提升，则收益限于遥测自适应。

已有结果　表 II–III 和 §VII-H 记录下游与代价取舍，快照成本为吞吐倒数。

## 4. 方法设计

### 4.1 输入、处理与输出

| 步骤 | 输入 | 处理 | 输出 |
| --- | --- | --- | --- |
| 逐设备摘要 | 面向设备的包级遥测快照 | 维护有固定行数的矩阵 sketch，达容量后保留主协方差方向 | 可更新的低维摘要 |
| 选择指标 | 摘要的谱结构、指标关联 | 在正交、稀疏等约束下选择固定数量的索引 | 网关上报的指标子集 |
| 动态更新 | 随包更新的近似误差 | 按误差条件触发重选，监测背景变化时稳定性 | 分阶段的子集与下游输出 |

### 4.2 机制与条件

对于 D 个指标和每设备 L 行摘要，存储从历史快照 O(NₜD) 收缩到 O(LD)。谱与稀疏目标利用指标冗余，图正则保留关系。协方差近似提供触发信号，误差界与下游准确率需要各自验证（§IV–VI）。

## 5. 与其他方法对比

与固定子集和 NetScope、InfoSen 等可更新子集比较。NetScope 的快照处理更快，本论文的优势主要在某些数据上保留更少指标而维持有效下游表现。

## 6. 实验表现与局限性

### 6.1 设置、数据与对照

N-BaIoT 两个 IoT 设备子集用于按快照聚类，Kitsune 两个子集用于异常检测，每个包抽出 115 个遥测量。§VII-H 用顺序拼接等条件构造分布变化，逐快照跟踪。

- 基线　LScore、SPCAFS、RUSLP、OCLSP、InfUFS、NetScope、InfoSen。
- 指标　聚类准确率、NMI、F-measure；异常检测性能、保留比例、吞吐与按吞吐推算的平均快照成本。

### 6.2 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 对照 | 差异 | 原文定位 |
| --- | --- | --- | --- | --- | --- |
| IoT1 / IoT2 | 达到所用协议最优指标比例 | 40% / 70% | NetScope 40% / 70% | 相同 | §VII-F 表 II |
| KitsuneIoT1 / KitsuneIoT2 | 达到所用协议最优指标比例 | 40% / 30% | NetScope 50% / 40% | 各少 10 个百分点 | §VII-F 表 II |
| 四个数据子集 | 快照处理量 | 5,495–5,729 / 秒，倒数约 0.18 ms | NetScope 10,135–10,791 / 秒 | SEDMS 吞吐较低 | §VII-G 表 III，非端到端延迟 |

### 6.7 局限性

每设备仍需可用的归属键和持续观测。协方差变化是遥测更新信号，无法单独区分工作负载变化和安全事件。序列拼接的结果要用后续时间或设备验证，快照成本也不等于用户可见的检测时延。

## 7. 学习与应用

### 7.1 开源状态

论文给出作者代码仓库，原始流量沿用 N-BaIoT 与 Kitsune 来源。

[作者公开仓库或产物](https://github.com/SyCode2005/SEDMS)。

### 7.2 复核要点

按设备与自然时间留出评估，各算法使用同样的上报比例和空间预算。用已知负载变化检查触发频次，再同时测未更新时的检测风险和更新后稳定性。

### 7.3 可迁移的研究问题

适合作为 COSINT 大规模观测场景的前端资源对照。将遥测选取、表示和决策分开，并记录删去的指标是否影响困难背景的分数尾部。

## 8. 总结

有界摘要保留结构并指导指标更新。

逐设备摘要 → 选择指标 → 动态更新。

## 9. Obsidian 知识链接

- 概念　[[04-concepts/network-telemetry]]、[[04-concepts/anomaly-detection]]。
- 方法　[[05-methods/streaming-telemetry-sketch]]。
- 任务　[[06-tasks/network-traffic-measurement]]、[[06-tasks/anomaly-detection]]。
- 综述　[[survey-malicious-traffic-detection]]。
- 对比与相邻资料　[[method-comparison-table]]、[[03-paper-notes/2026-COSINT-北邮时金桥]]、[[2025-NDSS-SketchFeature__High-Quality_Per-Flow_Feature_Extractor_Towards_Security-Aware_Data_Plane]]。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
| --- | --- | --- |
| 可直接在有界矩阵摘要上选择指标 | 误差界、实时触发流程 | §IV-B、§VI-A |
| 保留指标比例、下游性能和吞吐存在取舍 | 两类应用四个子集的保留比例与处理量 | §VII-F–H 表 II–III |

## 11. 原始资料链接

- PDF　[[00-inbox/PDFs/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks.pdf]]
- MinerU Markdown　[[02-parsed-markdown/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks.md]]
- MinerU 原始归档　[[01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/full.md]]

## 12. 后续问题

优先检验 §6.7 的主要限制，按 §7.2 记录数据、观测和指标条件。

## 13. 写作叙事与故事线分析

从全量遥测的内存/通信负担与固定子集的陈旧性出发，给出摘要与更新两项机制。实验分别检验判别性、保留比例、速度和分布变化。

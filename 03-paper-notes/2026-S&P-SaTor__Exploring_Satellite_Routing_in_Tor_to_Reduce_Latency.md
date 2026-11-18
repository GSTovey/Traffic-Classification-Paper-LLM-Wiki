---
type: "paper"
title_original: "SaTor: Exploring Satellite Routing in Tor to Reduce Latency"
title_cn: "SaTor：用卫星路由降低 Tor 时延"
authors: ["Haozhi Li", "Tariq Elahi"]
year: 2026
venue: "S&P"
source_version: "IEEE Symposium on Security and Privacy 2026 正式论文。"
doi: "10.1109/sp63933.2026.00068"
url: "https://doi.org/10.1109/sp63933.2026.00068"
pdf: "00-inbox/PDFs/2026-S&P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency.pdf"
mineru_md: "02-parsed-markdown/2026-S&P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency.md"
status: "processed"
reading_level: "L3"
research_area: ["Tor 性能", "匿名网络测量"]
task: ["电路时延测量", "异构链路比较"]
method: ["双宿主链路", "基于实测校准的仿真"]
dataset: ["LENS/Starlink 测量", "RIPE Atlas", "Tor Metrics/Consensus", "Waterloo 双宿主测试床"]
code: "unknown"
relevance: "high"
created: "2026-11-18"
updated: "2026-11-18"
metadata_source: "Crossref"
source_sha256: "7e28ce0f827350f3e949df92e3873c16918ee2b6f42e87f8ade8efe3ec36769a"
internal_citation_count: 0
citation_impact: 0.8
composite_weight: 0.8
citation_count_scope: "verified DOI or normalized complete titles in vault References; lower bound"
citation_count_verified: "2026-11-18"
---

# SaTor: Exploring Satellite Routing in Tor to Reduce Latency

## 0. 论文基础信息

| 项目 | 内容 |
| --- | --- |
| 原文标题 | SaTor: Exploring Satellite Routing in Tor to Reduce Latency |
| 中文标题 | SaTor：用卫星路由降低 Tor 时延 |
| 作者 | Haozhi Li、Tariq Elahi |
| 年份 | 2026 |
| 会议/期刊及版本 | IEEE Symposium on Security and Privacy 2026 正式论文。 |
| DOI | 10.1109/sp63933.2026.00068 |
| 题录来源 | Crossref |
| 研究方向 | Tor 性能、匿名网络测量 |
| 任务类型 | 电路时延测量、异构链路比较 |
| 方法关键词 | 双宿主链路、基于实测校准的仿真 |
| 数据集 | LENS/Starlink 测量；RIPE Atlas；Tor Metrics/Consensus；Waterloo 双宿主测试床 |
| 开源状态 | 本地论文中未确认可用的作者仿真或复现仓库。 |
| PDF | [[00-inbox/PDFs/2026-S&P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency.pdf]] |
| MinerU Markdown | [[02-parsed-markdown/2026-S&P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency.md]] |

题录核验见 [出版记录](https://doi.org/10.1109/sp63933.2026.00068)。

## 1. 一句话总结

SaTor 在保持 Tor 中继选择机制的前提下比较地面与低轨卫星链路，用实测校准仿真，估计哪些电路可获益。

## 2. 摘要翻译

### 2.1 摘要原文

见 [[00-inbox/PDFs/2026-S&P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency.pdf]] 第 1 页 Abstract。

### 2.2 摘要中文翻译

长电路是 Tor 时延的一个来源。偏向距离较短的中继会改变路径随机性，作者研究保持已选中继、在部分中继间采用卫星传输的做法。测量与仿真显示，特定的 100 中继加权部署下，约 40.5% 的电路可平均减少 21.8 ms RTT。

## 3. 方法动机

地面 AS 路径可能因距离、排队或路由绕行增加时延，而卫星链路的收益随位置和负载变化。研究问题是能否保留现有中继选择，又使部分长链路受益（§1、§3–4）。

### 3.4 问题发现路径

| 阶段 | 内容 |
| --- | --- |
| 现象观察 | 地面链路的典型 RTT 与尾部排队表现可能随地理和路由变化。 |
| 痛点提炼 | 为减少 RTT 而重新挑中继将改变 Tor 的既有路径分布。 |
| 问题转化 | 保持相同中继选择，是否能通过不同底层链路减少 RTT？ |
| 文献定位 | 与地面路径按相同中继对比较，补充 ShorTor 的文献对照。 |

### 3.5 科学假设形成

底层路由差异可降低部分电路 RTT，收益随中继部署和链路条件变化。

验证方式　用同中继配对实测校准仿真，报告 weighted 与 top-n。若换运营商和地区后收益消失，则只支持当前测量条件。

已有结果　表 1 报告测量和仿真差异，图 13 给出部署条件的模拟收益。

## 4. 方法设计

### 4.1 输入、处理与输出

| 步骤 | 输入 | 处理 | 输出 |
| --- | --- | --- | --- |
| 确定输入 | 中继、电路、链路位置及 RTT 测量 | 按既有中继选择生成电路样本，整理地面和卫星路径输入 | 可比较的中继对与电路 |
| 校准模型 | 双宿主测试床的两类链路 | 按可观察地理位置和链路 RTT 校准模拟，分析测量与模拟偏差 | 配对链路时延分布 |
| 评估部署 | 不同的卫星中继选择场景 | 测算双接口条件下的 RTT 及获益比例，讨论自治系统可见性和隐私 | 分场景电路收益与安全边界 |

### 4.2 机制与条件

只比较既有中继间的底层链路，中继采样维持论文的既有策略。正文把对偶链路的尾部相关性、部署覆盖和安全可见性分开。随机、带宽加权及高概率中继三种部署是不同方案，受益比例不能混用。

## 5. 与其他方法对比

与默认地面路径直接比较 RTT。与 ShorTor 等文献的比较依赖各自的试验设置。COSINT DHBCorr 使用两端流量相似性，本研究主要测 RTT 及路径可见性，为关联模型增加了值得控制的网络条件。

## 6. 实验表现与局限性

### 6.1 设置、数据与对照

用 Waterloo 双宿主测试床获得地面/卫星的配对观测，以 LENS 与 RIPE Atlas 校准。仿真测试约 10 万个电路，在多种中继覆盖方案下报告收益。实际测量覆盖为校准与检查的一部分。

- 基线　地面 Tor 路径、单卫星与双宿主两类路由、随机/加权/top-n 部署方案。ShorTor 用于文献比较。
- 指标　RTT 改善（ms、百分比）、获益电路比率、尾部时延；另讨论网络观察者可见性。

### 6.2 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 对照 | 差异 | 原文定位 |
| --- | --- | --- | --- | --- | --- |
| 带宽加权 100 中继 | 降低 RTT 的范围和幅度 | 约 40.5% 电路，平均少 21.8 ms | 既有地面路径 | — | §5，图 13 与 Practical Impact 段 |
| top-50 部署模拟 | 降低 RTT 的范围和幅度 | 约 99.3% 电路，平均少 21.9 ms | 既有地面路径 | — | §5 图 13，抽样方案不同 |

### 6.7 局限性

大范围结果主要是经局部实测校准的模拟。端用户页面时间为推算，运营商、路径模型与接入条件会改变收益。论文没有以生产关联检测器为实验对象。

## 7. 学习与应用

### 7.1 开源状态

本地论文中未确认可用的作者仿真或复现仓库。

### 7.2 复核要点

按地理、时间、到达顺序和路由场景复核 RTT 分布。校准样本与检验样本分离，同时报告适用范围、收益和不确定性。

### 7.3 可迁移的研究问题

对 DHBCorr 的节奏证据，可在已授权的原有数据上按 RTT 或抖动分层比较匹配分数。保持候选集合、采集窗口和真实配对固定，避免把网络变化误当表征的失效。

## 8. 总结

借不同底层链路降低已选电路的 RTT。

确定输入 → 校准模型 → 评估部署。

## 9. Obsidian 知识链接

- 概念　[[04-concepts/anonymous-traffic-identification]]、[[04-concepts/network-telemetry]]。
- 任务　[[06-tasks/network-traffic-measurement]]。
- 综述　[[survey-encrypted-traffic-analysis]]。
- 对比与相邻资料　[[method-comparison-table]]、[[03-paper-notes/2026-COSINT-北邮时金桥]]。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
| --- | --- | --- |
| 部分卫星部署可缩短电路 RTT | 双宿主实测校准与部署仿真；weighted-100 单列 | §4–5，表 1、图 13 |
| 尾时延与网络可见性随路由条件变化 | 报告双宿主对照及观察者可见性 | §5–6 |

## 11. 原始资料链接

- PDF　[[00-inbox/PDFs/2026-S&P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency.pdf]]
- MinerU Markdown　[[02-parsed-markdown/2026-S&P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency.md]]
- MinerU 原始归档　[[01-mineru-output/2026-S&P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency/full.md]]

## 12. 后续问题

优先检验 §6.7 的主要限制，按 §7.2 记录数据、观测和指标条件。

## 13. 写作叙事与故事线分析

从降低时延与保持中继随机性的矛盾提出底层链路选择。先校准仿真再扫部署覆盖，最后将时延收益和可见性分别讨论。

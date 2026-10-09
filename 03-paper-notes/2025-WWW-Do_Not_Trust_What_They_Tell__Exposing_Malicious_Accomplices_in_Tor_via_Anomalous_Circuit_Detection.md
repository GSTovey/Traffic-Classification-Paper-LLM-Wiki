---
type: paper
title_original: "Do Not Trust What They Tell: Exposing Malicious Accomplices in Tor via Anomalous Circuit Detection"
title_cn: ""
authors: []
year: 2025
venue: WWW
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2025-WWW-Do_Not_Trust_What_They_Tell__Exposing_Malicious_Accomplices_in_Tor_via_Anomalous_Circuit_Detection.pdf"
mineru_md: "02-parsed-markdown/2025-WWW-Do_Not_Trust_What_They_Tell__Exposing_Malicious_Accomplices_in_Tor_via_Anomalous_Circuit_Detection.md"
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

# Do Not Trust What They Tell: Exposing Malicious Accomplices in Tor via Anomalous Circuit Detection

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Do Not Trust What They Tell: Exposing Malicious Accomplices in Tor via Anomalous Circuit Detection |
| 年份 | 2025 |
| 会议/期刊 | WWW |
| PDF | [[2025-WWW-Do_Not_Trust_What_They_Tell__Exposing_Malicious_Accomplices_in_Tor_via_Anomalous_Circuit_Detection.pdf]] |
| MinerU Markdown | [[2025-WWW-Do_Not_Trust_What_They_Tell__Exposing_Malicious_Accomplices_in_Tor_via_Anomalous_Circuit_Detection.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
The Tor network, while ofering anonymity through trafic routing across volunteer-operated nodes, remains vulnerable to attacks that aim to deanonymize users by correlating trafic patterns between colluded entry and exit nodes in circuits. This paper presents a novel approach for detecting anomalous circuits in the Tor network, and for the first time provides a more comprehensive identification of potential malicious accomplice nodes in Tor by taking roles ofnodes in anomalous circuits into consideration. Our method strategically utilizes modified middle nodes to capture trafic data, followed by a novel circuit classification based on trafic patterns to pinpoint concerned circuits. Two kinds of anomalies are identified: routing anomalies and usage anomalies, that respectively represent the anomalies with explicit or implicit violation of Tor’s circuit construction guidelines. This leads to a successful revealing of totally 1,960 anomalous nodes in Tor. Furthermore, we apply clustering analysis with considering corresponding anomalous circuits and other key characteristics to the detected anomalous nodes, reveal ing potential hidden organizations behind these nodes that can threaten the network’s security. Our findings highlight the neces sity for the Tor project to adopt targeted mitigation strategies to enhance overall network security and privacy.

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
- 主题线索：website fingerprint, anomaly, tor, quic。
- 摘要证据：The Tor network, while ofering anonymity through trafic routing across volunteer-operated nodes, remains vulnerable to attacks that aim to deanonymize users by correlating trafic patterns between colluded entry and exit nodes in circuits. This paper presents a novel approach for detecting anomalous circuits in the Tor network, and for the first time provides a more comprehensive identification of potential malicious accomplice nodes in Tor by taking roles ofnodes in anomalous circuits into consideration. Our method strategically utilizes modified middle nodes to capture trafic data, followed by a novel circuit classification based on trafic patterns to pinpoint concerned circuits. Two kinds of anomalies are identified: routing anomalies and usage anomalies, that respectively represent the anomalies with explicit or implicit violation of Tor’s circuit construction guidelines. This leads to a successful revealing of totally 1,960 anomalous nodes in Tor. Furthermore, we apply clustering analysis with considering corresponding anomalous circuits and other key characteristics to the detected anomalous nodes, reveal ing potential hidden organizations behind these nodes that can threaten the network’s security. Our findings highlight the neces sity for the Tor project to adopt targeted mitigation strategies to enhance overall network security and privacy.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：未检测到明确 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。

## 深度分析（2026-09-29）

- reading_level: L3
- 研究定位：Tor异常电路/恶意协作者识别
- 方法机制：利用改造middle节点采集流量，按路由异常与使用异常分类电路，并结合节点角色和聚类定位潜在协同组织；摘要报告识别1,960个异常节点。
- 输入—处理—输出：Tor流量观测与电路分类；输出异常电路、节点角色和组织聚类。
- 证据边界：摘要明确了异常类型和节点数量；数据采集范围、分类特征、阈值、误报率及代码状态在当前解析证据中未完整确认。
- 联动标签：website-fingerprinting；DNS；anomaly-detection；traffic-security


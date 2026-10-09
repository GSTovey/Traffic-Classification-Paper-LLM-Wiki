---
type: paper
title_original: "THE ADVANCED COMPUTING SYSTEMS ASSOCIATION"
title_cn: ""
authors: []
year: 2026
venue: NSDI
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-NSDI-OpenOptics__Enabling_Open_Research_and_Implementation_of_Optical_Data_Center_Networks.pdf"
mineru_md: "02-parsed-markdown/2026-NSDI-OpenOptics__Enabling_Open_Research_and_Implementation_of_Optical_Data_Center_Networks.md"
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
| PDF | [[2026-NSDI-OpenOptics__Enabling_Open_Research_and_Implementation_of_Optical_Data_Center_Networks.pdf]] |
| MinerU Markdown | [[2026-NSDI-OpenOptics__Enabling_Open_Research_and_Implementation_of_Optical_Data_Center_Networks.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
Optical data center networks (DCNs) are emerging as a promising design for cloud infrastructure. However, existing optical DCN architectures operate as closed ecosystems, tying software solutions to specific optical hardware. We introduce OpenOptics, an open research and development framework that decouples software from hardware, allowing them to evolve independently. OpenOptics features: (1) a time-flow table abstraction as a common interface between optical hardware and software, (2) a unified workflow and user-friendly API for implementing various optical DCNs with simple Python scripts, and (3) a backend system that re architects queue management to support the time-flow tables and provides rich infrastructure services for diverse applica tions. Built on programmable switches, OpenOptics achieves a record-breaking minimum optical circuit duration of 2 µs using commodity devices. We validate OpenOptics’ generality by implementing six optical architectures and seven routing schemes on an optical testbed and conducting benchmarks on a 108-ToR setup, showcasing its efficiency. Additionally, case studies highlight novel research opportunities enabled by OpenOptics.

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
- 主题线索：tor, quic。
- 摘要证据：Optical data center networks (DCNs) are emerging as a promising design for cloud infrastructure. However, existing optical DCN architectures operate as closed ecosystems, tying software solutions to specific optical hardware. We introduce OpenOptics, an open research and development framework that decouples software from hardware, allowing them to evolve independently. OpenOptics features: (1) a time-flow table abstraction as a common interface between optical hardware and software, (2) a unified workflow and user-friendly API for implementing various optical DCNs with simple Python scripts, and (3) a backend system that re architects queue management to support the time-flow tables and provides rich infrastructure services for diverse applica tions. Built on programmable switches, OpenOptics achieves a record-breaking minimum optical circuit duration of 2 µs using commodity devices. We validate OpenOptics’ generality by implementing six optical architectures and seven routing schemes on an optical testbed and conducting benchmarks on a 108-ToR setup, showcasing its efficiency. Additionally, case studies highlight novel research opportunities enabled by OpenOptics.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
Queue occupancy estimation accuracy. The error of queue occupancy estimation (§5.2) is the difference between our estimated queue occupancy (EQO) from the ingress pipeline and the ground-truth queue occupancy read by an egress packet. We measure it with the above setting (in Fig. 11) but combine line-rate traffic and bursty traffic to fill and drain the queue periodically. The estimation accuracy increases with the update interval (Fig. 12). We find 50 ns draws a good balance between the estimation accuracy and the consumption of pipeline processing resources on the ToR. The estimation error is within 725 B, less than half MTU-size packet, and the packet generator sends one packet every 50 ns (or at 20 Mpps), which creates only 1.3% pipeline forward overhead on Tofino2 with 1.5 Bpps processing capacity. Minimum time slice duration. We derive the minimum achievable time slice duration in OpenOptics to evaluate its generality to support various optical proposals. To ensure a duty cycle above 90%, the slice duration is typically set to at least 10× the guardband, which covers the maximum of circuit reconfiguration and unavoidable system delays, preventing data loss. This analysis focuses on system limits, assuming OCS hardware is not a limiting factor, and asks what time slice duration OpenOptics can achieve in that case. The 34 ns queue rotation variance (Fig. 11) should be covered by the guardband. In addition, the queue occupancy estimation error of 725 B (Fig. 12) translates to 58 ns delay under 100 Gbps bandwidth, meaning packets may get impacted by false negatives for 58 ns, where a full queue is mistakenly seen as not full. Besides, our synchronization work shows up to 15 ns sync errors in a 108-ToR optical DCN [30], which requires a guardband of 15 × 2 = 30ns for c

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


## 深度分析（并行深度分析更新 2026-09-29）

### 方法、实验与证据
OpenOptics提供光数据中心网络的开放研究与实现框架，含调度、拥塞检测及pushback机制；MinerU文本显示HOHO在拥塞下易过载，pushback作为补救。具体硬件和端到端指标需继续核对。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。

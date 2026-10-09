---
type: paper
title_original: "Robust Transceiver Design for SIM-Assisted Integrated Sensing and Covert Communications"
title_cn: ""
authors: []
year: 2026
venue: arXiv
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-arXiv-Robust_Transceiver_Design_for_SIM-Assisted_Integrated_Sensing_and_Covert_Communications.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-Robust_Transceiver_Design_for_SIM-Assisted_Integrated_Sensing_and_Covert_Communications.md"
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

# Robust Transceiver Design for SIM-Assisted Integrated Sensing and Covert Communications

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Robust Transceiver Design for SIM-Assisted Integrated Sensing and Covert Communications |
| 年份 | 2026 |
| 会议/期刊 | arXiv |
| PDF | [[2026-arXiv-Robust_Transceiver_Design_for_SIM-Assisted_Integrated_Sensing_and_Covert_Communications.pdf]] |
| MinerU Markdown | [[2026-arXiv-Robust_Transceiver_Design_for_SIM-Assisted_Integrated_Sensing_and_Covert_Communications.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
—Stacked intelligent metasurfaces (SIMs) have emerged as a promising wave-domain processing technology for sixth-generation integrated sensing and communication networks, reducing reliance on complex radio-frequency hardware. Nevertheless, imperfect channel state information (CSI) can compromise sensing performance and communication reliability. Moreover, ensuring covert transmission introduces a further challenge, as the system must sense potential targets while concealing communication activity from unauthorized wardens. These challenges motivate the development of robust SIM-assisted integrated sensing and covert communication (ISACC) systems. In this paper, we investigate the robust transceiver design of a multi-user, multi-target ISACC system under imperfect CSI. We jointly optimize the transmit and receive beamformers, sensing covariance matrix, and SIM phase shifts to maximize the worst-case minimum sensing signal-to-interference-plus-noise ratio. The formulation enforces constraints on bounded channel uncertainties, user qualityof-service requirements, transmit-power budget, SIM phase shifts, and target detection probabilities. Since the formulated problem is highly non-convex, we develop an alternating optimization framework based on the S-procedure, successive convex approximation, and semidefinite relaxation. Furthermore, to reduce computational complexity, we derive exact lowerdimensional representations of the robust sensing linear matrix inequalities (LMIs) involved in transmit/receive-beamformer designs. We further develop a low-complexity phase-update method that avoids the large sensing LMIs. Numerical results demonstrate that the proposed design outperforms random phase shift and fully digital-beamforming benchmarks, while the low-complexity scheme achieves comparable performance to the LMI-based scheme at substantially lower computational cost. Index Terms—Stacked intelligent metasurfaces, integrated sensing and communication, covert communication, imperfect channel state information, robust design.

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
- 主题线索：tor, covert。
- 摘要证据：Index Terms—Stacked intelligent metasurfaces, integrated sensing and communication, covert communication, imperfect channel state information, robust design.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：未检测到明确 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


## 深度分析（并行深度分析更新 2026-09-29）

### 方法、实验与证据
针对SIM辅助一体化感知与隐蔽通信，在不完美CSI下做鲁棒收发机联合设计；仿真随机用户/目标、SIM层间距λ/4，指标含通信与感知权衡。缺少实测硬件和真实信道验证。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。

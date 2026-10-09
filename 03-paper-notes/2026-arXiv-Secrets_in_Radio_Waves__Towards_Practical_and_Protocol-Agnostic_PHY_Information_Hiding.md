---
type: paper
title_original: "Secrets in Radio Waves: Towards Practical and Protocol-Agnostic PHY Information Hiding"
title_cn: ""
authors: []
year: 2026
venue: arXiv
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-arXiv-Secrets_in_Radio_Waves__Towards_Practical_and_Protocol-Agnostic_PHY_Information_Hiding.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-Secrets_in_Radio_Waves__Towards_Practical_and_Protocol-Agnostic_PHY_Information_Hiding.md"
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

# Secrets in Radio Waves: Towards Practical and Protocol-Agnostic PHY Information Hiding

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Secrets in Radio Waves: Towards Practical and Protocol-Agnostic PHY Information Hiding |
| 年份 | 2026 |
| 会议/期刊 | arXiv |
| PDF | [[2026-arXiv-Secrets_in_Radio_Waves__Towards_Practical_and_Protocol-Agnostic_PHY_Information_Hiding.pdf]] |
| MinerU Markdown | [[2026-arXiv-Secrets_in_Radio_Waves__Towards_Practical_and_Protocol-Agnostic_PHY_Information_Hiding.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
—Physical layer (PHY) information hiding supports critical applications, such as digital fingerprinting for transmitter identification and undetectable side channels for covert communication, and has attracted considerable attention from the research community. One category of prior studies focuses on theoretical analysis, proposing techniques such as artificial noise or reconfigurable intelligent surfaces to enable undetectable covert transmission. However, hardware prototypes are rarely presented due to their algorithmic complexity or hard-to-satisfy assumptions. Another category of studies focuses on system-level solutions, achieving PHY information hiding by customizing existing modulation schemes. However, these methods are typically designed for specific wireless protocols, limiting their generalizability. In this work, we introduce a new PHY information hiding paradigm that differs fundamentally from the previous two categories of approaches. Inspired by recent advancements in other domains such as image information hiding, we migrate encoder-decoder neural networks to the PHY information hiding field, embedding secrets by introducing imperceptible distortions within the preamble waveform. Sim-to-real fine-tuning is additionally proposed to tackle unique challenges, e.g., fading and hardware imperfections. The designed methodology is practical and protocol-agnostic. We provide case hardware prototypes of two commercially popular wireless technologies, i.e., LoRa and Bluetooth Low Energy (BLE), using commodity software-defined radio (SDR) transceivers, demonstrating excellent feasibility and generalizability. Index Terms—Physical layer security, wireless steganography, information hiding, deep learning, LoRa, Bluetooth Low Energy

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
- 主题线索：tor, transformer, adversarial, covert。
- 摘要证据：Index Terms—Physical layer security, wireless steganography, information hiding, deep learning, LoRa, Bluetooth Low Energy

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
<table><tr><td rowspan="2">Condition</td><td rowspan="2">Loc.</td><td rowspan="2">Avg. SNR</td><td colspan="3">Metrics</td></tr><tr><td> $SBER_{raw}$ </td><td> $SBER_{fec}$ </td><td>SMER</td></tr><tr><td rowspan="3">LOS</td><td>A</td><td>26.39 dB</td><td>0.0242</td><td>0.0002</td><td>0.0039</td></tr><tr><td>B</td><td>13.37 dB</td><td>0.0423</td><td>0.0021</td><td>0.0456</td></tr><tr><td>C</td><td>6.65 dB</td><td>0.1595</td><td>0.0745</td><td>0.747</td></tr><tr><td>NLOS</td><td>D</td><td>15.07 dB</td><td>0.0464</td><td>0.0021</td><td>0.0419</td></tr></table> TABLE III EXPERIMENTAL RESULTS OF LORA INFORMATION HIDING IN THE OUTDOOR ENVIRONMENT. 120 BITS ARE EMBEDDED WITHIN THE PREAMBLE FIELD. <table><tr><td rowspan="2">Distance</td><td rowspan="2">Avg. SNR</td><td colspan="3">Metrics</td></tr><tr><td> $SBER_{raw}$ </td><td> $SBER_{fec}$ </td><td>SMER</td></tr><tr><td>10 m</td><td>21.17 dB</td><td>0.0363</td><td>0.0012</td><td>0.0219</td></tr><tr><td>20 m</td><td>11.55 dB</td><td>0.0558</td><td>0.0068</td><td>0.0931</td></tr><tr><td>30 m</td><td>8.1 dB</td><td>0.1073</td><td>0.0441</td><td>0.3713</td></tr><tr><td>40 m</td><td>5.25 dB</td><td>0.1698</td><td>0.0951</td><td>0.7386</td></tr></table> The experimental results are presented in Table II. It can be observed that the SMER is lower than 0.05 when the receiver is placed at locations A, B, and D, indicating a promising PHY information hiding performance. However, the SMER at location C is 0.747, which implies that most covert messages cannot be extracted without errors and may need retransmission. The high SMER can be attributed to the low SNR of 6.65 dB on average. Moreover, it can be seen that the SMER for location D is 0.0419, which indicates that the designed LoRa information hiding system can achieve excellent perf

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


## 深度分析（并行深度分析更新 2026-09-29）

### 方法、实验与证据
综述/方案面向协议无关PHY信息隐藏，讨论发射机指纹与不可检测侧信道，强调跨协议通用性和实际部署挑战；需继续提取其具体编码机制与实验设置。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。

---
type: paper
title_original: "Forge: A Robust Multi-tab Website Fingerprinting Atack Via Blind Source Separation"
title_cn: ""
authors: []
year: 2026
venue: WWW
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-WWW-Forge__A_Robust_Multi-tab_Website_Fingerprinting_Attack_Via_Blind_Source_Separation.pdf"
mineru_md: "02-parsed-markdown/2026-WWW-Forge__A_Robust_Multi-tab_Website_Fingerprinting_Attack_Via_Blind_Source_Separation.md"
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

# Forge: A Robust Multi-tab Website Fingerprinting Atack Via Blind Source Separation

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Forge: A Robust Multi-tab Website Fingerprinting Atack Via Blind Source Separation |
| 年份 | 2026 |
| 会议/期刊 | WWW |
| PDF | [[2026-WWW-Forge__A_Robust_Multi-tab_Website_Fingerprinting_Attack_Via_Blind_Source_Separation.pdf]] |
| MinerU Markdown | [[2026-WWW-Forge__A_Robust_Multi-tab_Website_Fingerprinting_Attack_Via_Blind_Source_Separation.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
论文未明确提取摘要。

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
- 主题线索：website fingerprint, tor, transformer, adversarial。
- 摘要证据：MinerU 未稳定提取摘要，不能据此补写贡献。

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。

## 深度分析（2026-09-29）

- reading_level: L3
- 研究定位：多标签WF攻击/BSS
- 方法机制：Forge将多标签WF重构为盲源分离，不预设并发标签数；分离后使用时频双域注意力识别网站，在开放世界、带防御和动态数据上评估，摘要报告多标签开放世界mAP较SOTA平均提升78.6%。
- 输入—处理—输出：输入混合Tor流量；BSS分离潜在标签信号，再输出网站集合及置信度。
- 证据边界：需核验BSS训练目标、标签数估计、开放世界FPR/召回、噪声与防御设置；DOI已见于原文，代码状态未知。
- 联动标签：website-fingerprinting；DNS；anomaly-detection；traffic-security


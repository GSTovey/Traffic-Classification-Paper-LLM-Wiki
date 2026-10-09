---
type: paper
title_original: "Robust LLM-Based Website Fingerprinting under Dynamic Real-World Conditions"
title_cn: ""
authors: []
year: 2026
venue: WWW
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-WWW-Robust_LLM-Based_Website_Fingerprinting_under_Dynamic_Real-World_Conditions.pdf"
mineru_md: "02-parsed-markdown/2026-WWW-Robust_LLM-Based_Website_Fingerprinting_under_Dynamic_Real-World_Conditions.md"
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

# Robust LLM-Based Website Fingerprinting under Dynamic Real-World Conditions

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Robust LLM-Based Website Fingerprinting under Dynamic Real-World Conditions |
| 年份 | 2026 |
| 会议/期刊 | WWW |
| PDF | [[2026-WWW-Robust_LLM-Based_Website_Fingerprinting_under_Dynamic_Real-World_Conditions.pdf]] |
| MinerU Markdown | [[2026-WWW-Robust_LLM-Based_Website_Fingerprinting_under_Dynamic_Real-World_Conditions.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
Website Fingerprinting (WF) attacks aim to infer the websites vis ited by Tor users by analyzing patterns in encrypted network trafic. However, most existing WF attacks are evaluated on trafic collected in controlled environments with fixed configurations, failing to re flect the complexity and variability of real-world conditions. In practice, trafic is far more dynamic and diverse due to heterogeneous network conditions, the large number of subpages within individual websites, and continuous evolution of website content. These factors increase intra-class variability and induce temporal feature drift, which ultimately degrades the long-term efectiveness of existing attacks. In this paper, we propose TraVerse, an LLM-based representation learning framework designed to achieve robust WF attacks under real-world conditions. TraVerse applies architectural adaptation and large-scale fine-tuning on diverse un labeled trafic to learn generalizable and resilient representations that remain efective in dynamic and evolving environments. Fur thermore, TraVerse integrates a lightweight classifier atop the LLM derived representations, enabling accurate website identification and eficient few-shot adaptation with minimal model updates. We prototype TraVerse and conduct comprehensive evaluations using real-user trafic. Experimental results show that TraVerse improves Accuracy@3 by an average of 176.3% and weighted F1 by 343.3% over state-of-the-art baselines, while maintaining strong performance throughout a three-month longitudinal evaluation.

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
- 摘要证据：Website Fingerprinting (WF) attacks aim to infer the websites vis ited by Tor users by analyzing patterns in encrypted network trafic. However, most existing WF attacks are evaluated on trafic collected in controlled environments with fixed configurations, failing to re flect the complexity and variability of real-world conditions. In practice, trafic is far more dynamic and diverse due to heterogeneous network conditions, the large number of subpages within individual websites, and continuous evolution of website content. These factors increase intra-class variability and induce temporal feature drift, which ultimately degrades the long-term efectiveness of existing attacks. In this paper, we propose TraVerse, an LLM-based representation learning framework designed to achieve robust WF attacks under real-world conditions. TraVerse applies architectural adaptation and large-scale fine-tuning on diverse un labeled trafic to learn generalizable and resilient representations that remain efective in dynamic and evolving environments. Fur thermore, TraVerse integrates a lightweight classifier atop the LLM derived representations, enabling accurate website identification and eficient few-shot adaptation with minimal model updates. We prototype TraVerse and conduct comprehensive evaluations using real-user trafic. Experimental results show that TraVerse improves Accuracy@3 by an average of 176.3% and weighted F1 by 343.3% over state-of-the-art baselines, while maintaining strong performance throughout a three-month longitudinal evaluation.

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
- 研究定位：WF表示学习/LLM
- 方法机制：TraVerse对LLM做架构适配并在大规模无标签流量上微调，学习应对网络异质性、子页面多样性和内容演化的表示，再接轻量分类器。
- 输入—处理—输出：输入动态Tor流量；LLM表示编码后输出网站识别。
- 证据边界：需核验预训练语料、时间切分、标签成本、漂移评估、增量更新和算力开销；摘要中的完整指标未抽取。
- 联动标签：website-fingerprinting；DNS；anomaly-detection；traffic-security


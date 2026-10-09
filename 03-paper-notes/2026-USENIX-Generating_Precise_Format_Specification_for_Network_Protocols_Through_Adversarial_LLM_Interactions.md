---
type: paper
title_original: "THE ADVANCED COMPUTING SYSTEMS ASSOCIATION"
title_cn: ""
authors: []
year: 2026
venue: USENIX
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-USENIX-Generating_Precise_Format_Specification_for_Network_Protocols_Through_Adversarial_LLM_Interactions.pdf"
mineru_md: "02-parsed-markdown/2026-USENIX-Generating_Precise_Format_Specification_for_Network_Protocols_Through_Adversarial_LLM_Interactions.md"
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
| 会议/期刊 | USENIX |
| PDF | [[2026-USENIX-Generating_Precise_Format_Specification_for_Network_Protocols_Through_Adversarial_LLM_Interactions.pdf]] |
| MinerU Markdown | [[2026-USENIX-Generating_Precise_Format_Specification_for_Network_Protocols_Through_Adversarial_LLM_Interactions.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
This paper aims to address a significant gap in inferring pre cise format specifications for network protocols, particularly regarding the exact constraints on network packet fields. That is, while current methods can often derive accurate syntactic structures that divide a network packet into multiple fields, they typically struggle to capture the semantic dependencies or constraints among those fields. To address this issue, our central insight is that large language models (LLMs) have proven effective across various tasks, and adversarial interactions among these tasks can significantly alleviate the hallu cination problem. Based on the insight, we propose a novel approach to generating precise protocol formats by adversarially combining LLM-based specification inference and code generation. By inputting the structured RFC documents of network protocols into LLMs, we generate both packet for mats and reference packet parsers that iteratively refine one another to reduce hallucinations: the packet formats allow us to create a variety of network packets for parser testing, while runtime checks in the parsers help identify format errors. Our evaluation of 8 protocols shows a significant increase in preci sion and recall, achieving a 326% improvement over the state of the art in inferring field constraints. Furthermore, the im proved format specifications enable effective fuzzing, leading to the discovery of 24 zero-day vulnerabilities in widely used protocol implementations.

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
- 主题线索：dns, tor, graph neural, adversarial。
- 摘要证据：This paper aims to address a significant gap in inferring pre cise format specifications for network protocols, particularly regarding the exact constraints on network packet fields. That is, while current methods can often derive accurate syntactic structures that divide a network packet into multiple fields, they typically struggle to capture the semantic dependencies or constraints among those fields. To address this issue, our central insight is that large language models (LLMs) have proven effective across various tasks, and adversarial interactions among these tasks can significantly alleviate the hallu cination problem. Based on the insight, we propose a novel approach to generating precise protocol formats by adversarially combining LLM-based specification inference and code generation. By inputting the structured RFC documents of network protocols into LLMs, we generate both packet for mats and reference packet parsers that iteratively refine one another to reduce hallucinations: the packet formats allow us to create a variety of network packets for parser testing, while runtime checks in the parsers help identify format errors. Our evaluation of 8 protocols shows a significant increase in preci sion and recall, achieving a 326% improvement over the state of the art in inferring field constraints. Furthermore, the im proved format specifications enable effective fuzzing, leading to the discovery of 24 zero-day vulnerabilities in widely used protocol implementations.

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
SPAR通过对抗式LLM交互迭代生成正/负数据包并结合RFC和Z3细化格式规范与解析器，直到互相一致；温度0、AutoGen+Z3，八种协议与ParCleanse/ChatAFL比较。路径覆盖和单约束线性否定牺牲理论完备性。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。

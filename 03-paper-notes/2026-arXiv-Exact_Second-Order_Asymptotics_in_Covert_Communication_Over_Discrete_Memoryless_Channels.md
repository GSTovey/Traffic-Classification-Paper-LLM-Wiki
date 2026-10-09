---
type: paper
title_original: "Exact Second-Order Asymptotics for Covert Communication over DMCs with Variational Distance Constraints"
title_cn: ""
authors: []
year: 2026
venue: arXiv
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-arXiv-Exact_Second-Order_Asymptotics_in_Covert_Communication_Over_Discrete_Memoryless_Channels.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-Exact_Second-Order_Asymptotics_in_Covert_Communication_Over_Discrete_Memoryless_Channels.md"
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

# Exact Second-Order Asymptotics for Covert Communication over DMCs with Variational Distance Constraints

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Exact Second-Order Asymptotics for Covert Communication over DMCs with Variational Distance Constraints |
| 年份 | 2026 |
| 会议/期刊 | arXiv |
| PDF | [[2026-arXiv-Exact_Second-Order_Asymptotics_in_Covert_Communication_Over_Discrete_Memoryless_Channels.pdf]] |
| MinerU Markdown | [[2026-arXiv-Exact_Second-Order_Asymptotics_in_Covert_Communication_Over_Discrete_Memoryless_Channels.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
We determine the exact second-order asymptotics of covert communication over binary-input discrete memoryless channels when covertness is measured by variational distance. Previous work by Tahmasbi and Bloch [IEEE Trans. Inf. Theory, Apr. 2019] characterized the first-order asymptotics and derived achievability and converse bounds on the second-order term, but these bounds do not match. The gap arises from an additional penalty of order $n ^ { 1 / 4 }$ in the achievability bound. We show that this penalty can be removed through a sharper analysis of the distribution of the warden’s output induced by pulse-position modulation. Specifically, we express the variational distance through the Bhattacharyya coefficient of two distributions and the expectation of a continuous function of the log-likelihood ratio. Because the resulting expectation involves a continuous function rather than the probability of a likelihoodratio event, an analysis of the characteristic function combined with a Gaussian smoothing argument reduces the approximation error from $O ( n ^ { - 1 / 4 } )$ (derived from the Berry–Esseen bound in prior work) to $O ( n ^ { - 1 / 2 } )$ . With this better controlled approximation error, we manage to derive a matching achievability result to the existing converse result, thus establishing the exact second-order asymptotics

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
- 主题线索：tor, adversarial, covert。
- 摘要证据：We determine the exact second-order asymptotics of covert communication over binary-input discrete memoryless channels when covertness is measured by variational distance. Previous work by Tahmasbi and Bloch [IEEE Trans. Inf. Theory, Apr. 2019] characterized the first-order asymptotics and derived achievability and converse bounds on the second-order term, but these bounds do not match. The gap arises from an additional penalty of order $n ^ { 1 / 4 }$ in the achievability bound. We show that this penalty can be removed through a sharper analysis of the distribution of the warden’s output induced by pulse-position modulation. Specifically, we express the variational distance through the Bhattacharyya coefficient of two distributions and the expectation of a continuous function of the log-likelihood ratio. Because the resulting expectation involves a continuous function rather than the probability of a likelihoodratio event, an analysis of the characteristic function combined with a Gaussian smoothing argument reduces the approximation error from $O ( n ^ { - 1 / 4 } )$ (derived from the Berry–Esseen bound in prior work) to $O ( n ^ { - 1 / 2 } )$ . With this better controlled approximation error, we manage to derive a matching achievability result to the existing converse result, thus establishing the exact second-order asymptotics

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
理论工作研究带变分距离约束的DMC隐蔽通信精确二阶渐近；核心是有限块长下容量、散度和二阶项的严格界。需人工核对定理条件、先验分布与是否可用于网络流量实验。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。

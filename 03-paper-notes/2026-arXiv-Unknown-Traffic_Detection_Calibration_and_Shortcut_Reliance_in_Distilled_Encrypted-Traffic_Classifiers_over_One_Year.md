---
type: paper
title_original: "Unknown-Traffic Detection, Calibration and Shortcut Reliance in Distilled Encrypted-Traffic Classifiers over One Year"
title_cn: ""
authors: []
year: 2026
venue: arXiv
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-arXiv-Unknown-Traffic_Detection_Calibration_and_Shortcut_Reliance_in_Distilled_Encrypted-Traffic_Classifiers_over_One_Year.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-Unknown-Traffic_Detection_Calibration_and_Shortcut_Reliance_in_Distilled_Encrypted-Traffic_Classifiers_over_One_Year.md"
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

# Unknown-Traffic Detection, Calibration and Shortcut Reliance in Distilled Encrypted-Traffic Classifiers over One Year

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Unknown-Traffic Detection, Calibration and Shortcut Reliance in Distilled Encrypted-Traffic Classifiers over One Year |
| 年份 | 2026 |
| 会议/期刊 | arXiv |
| PDF | [[2026-arXiv-Unknown-Traffic_Detection_Calibration_and_Shortcut_Reliance_in_Distilled_Encrypted-Traffic_Classifiers_over_One_Year.pdf]] |
| MinerU Markdown | [[2026-arXiv-Unknown-Traffic_Detection_Calibration_and_Shortcut_Reliance_in_Distilled_Encrypted-Traffic_Classifiers_over_One_Year.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
—Knowledge distillation is the standard way to compress encrypted-traffic classifiers for the edge, and almost all such work judges students by accuracy alone. We ask what else a student inherits: unknown-traffic detection, calibration, shortcut reliance, and whether any survives a year of drift. Resemblance proves little on its own, since soft targets also regularise. We therefore distil one 101k-parameter student from two teachers of equal accuracy but different construction, a fivemember ensemble and a single wider model, so that following one rather than the other is attributable to it. The design was pre-registered before any test result was seen. We tested ten hypotheses on CESNET-TLS-Year22, a year of real TLS traffic, across 18 test windows over 35 weeks. Two are supported: a student’s per-flow unknown-scores shift toward its own teacher, but only at a conventional temperature, not the accuracy-optimal one; and a shortcut-reliant teacher passes its over-confidence to a student that never sees the feature. The drift prediction is reversed under both scores, the gap narrowing rather than widening and the student overtaking under the energy score in two of three replicates, as is the prediction that such a teacher harms its student’s detection, which improves slightly. Shortcut reliance is set by model size, not distillation. Under the logit-based scores nothing else transfers: distillation beats neither a temperature-scaled direct student nor label smoothing. Exploratory analysis shows this turns on the scoring rule: with a feature-space detector the teacher detects unknown traffic 0.073 AUROC better than the direct student, where the energy score sees 0.000, and the conventional-temperature student inherits most of it. Label smoothing, with no teacher, recovers more. Distillation transfers the teacher’s habits; what looks like an inherited ability is available without one. Index Terms—Encrypted traffic classification, knowledge distillation, open-set recognition, calibration, concept drift, shortcut learning, pre-registration.

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
- 主题线索：website fingerprint, encrypted traffic, tor, transformer, traffic classification。
- 摘要证据：Index Terms—Encrypted traffic classification, knowledge distillation, open-set recognition, calibration, concept drift, shortcut learning, pre-registration.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


### 并行深度分析（2026-09-29）
- 方法/问题：A pre-registered one-year CESNET-TLS-Year22 study distils a 101k-parameter student from equal-accuracy teachers and tests unknown detection, calibration and shortcut reliance over 18 windows/35 weeks. It reports teacher-dependent unknown-score and shortcut inheritance at selected temperatures. Missing: full ten-hypothesis outcomes and calibration/unknown metrics.
- 证据边界：以上仅使用对应 MinerU 解析稿摘要及可稳定提取段落；未提取到的数值、数据集、代码和参数均不作推断。
- 复现建议：先核对原文表格、附录、代码仓库和数据划分，再确定 L3/L4 复现。

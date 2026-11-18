---
type: paper
title_original: "ARI-LLM: Autoregressive Imputation for Network Traffic Matrix via Large Language Models"
title_cn: "unknown"
authors: ["Fenglin Yan", "Kaiwen Jiang", "Yan Qiao", "Meng Li", "Yuxuan Li", "Peng Yu", "Cuiying Feng"]
year: 2026
venue: "INFOCOM"
doi: "10.1109/INFOCOM59046.2026.11571176"
url: "https://doi.org/10.1109/INFOCOM59046.2026.11571176"
pdf: "../00-inbox/PDFs/2026-INFOCOM-ARI-LLM__Autoregressive_Imputation_for_Network_Traffic_Matrix_via_Large_Language_Models.pdf"
mineru_md: "../02-parsed-markdown/2026-INFOCOM-ARI-LLM__Autoregressive_Imputation_for_Network_Traffic_Matrix_via_Large_Language_Models.md"
status: processed
reading_level: L2
research_area: ["traffic matrix imputation"]
task: [unknown]
method: ["imputation"]
dataset: [unknown]
code: "https://github.com/JKevin17/ARI-LLM"
relevance: medium
created: "2026-10-26"
updated: "2026-10-26"
internal_citation_count: 1
citation_impact: 1.0
composite_weight: 0.85
citation_count_scope: "verified DOI or normalized complete titles in vault References; lower bound"
citation_count_verified: "2026-11-18"
---

# ARI-LLM: Autoregressive Imputation for Network Traffic Matrix via Large Language Models

## 0. 论文基础信息
|项目|内容|
|---|---|
|原文标题|ARI-LLM: Autoregressive Imputation for Network Traffic Matrix via Large Language Models|
|作者|Fenglin Yan†‡, Kaiwen Jiang†‡, Yan Qiao,∗‡§∗∗ Meng Li∗‡§∗∗, Yuxuan Li¶, Peng Yu§, Cuiying Feng∥∗∗|
|年份|2026|
|会议/期刊|INFOCOM|
|研究方向|traffic matrix imputation|
|方法关键词|imputation|
|数据集|unknown|
|是否开源|unknown|

## 1. 一句话总结
> 本文围绕“ARI-LLM: Autoregressive Imputation for Network Traffic Matrix via Large Language Models”研究网络流量相关问题。摘要明确指出：The Traffic Matrix (TM) plays a vital role in a wide range of network management tasks, yet monitoring complete TMs is prohibitively expensive.

## 2. 摘要翻译
### 2.1 摘要原文
The Traffic Matrix (TM) plays a vital role in a wide range of network management tasks, yet monitoring complete TMs is prohibitively expensive. Recent efforts focus on recovering incomplete TMs via learning-based models by learning from historical TM snapshots. However, existing approaches often suffer from poor generalization and require frequent retraining when the network environment evolves—let alone unseen networks. In this paper, we propose a novel TM imputation framework, named ARI-LLM, based on Large Language Models (LLMs). Inspired by human-like cognitive process of coarse-tofine reasoning, our method incrementally refines the incomplete TM through a step-wise autoregressive mechanism, which is compatible with the pretraining paradigm of LLMs, endowing our model with powerful generalization and zero-shot capabilities. To ensure plug-and-play deployment across TM imputation tasks in dynamic environments, we craft a flow-aware tokenization scheme that supports scalable and topology-adaptive embeddings. Extensive experiments demonstrate that ARI-LLM significantly outperforms state-of-the-art methods on large-scale sparse TMs (over 90% missingness), reducing imputation error by up to 34.7%. It maintains strong performance whether given only limited TM knowledge (e.g., 20% observed flows, 5% training snapshots) or no prior knowledge at all on unseen networks.
### 2.2 摘要中文翻译
摘要具体指出，本文研究“ARI-LLM: Autoregressive Imputation for Network Traffic Matrix via Large Language Models”所针对的问题。方法上，摘要描述了：Recent efforts focus on recovering incomplete TMs via learning-based models by learning from historical TM snapshots.。结果上，摘要报告：Extensive experiments demonstrate that ARI-LLM significantly outperforms state-of-the-art methods on large-scale sparse TMs (over 90% missingness), reducing imputation error by up to 34.7%.；摘要中的关键数值包括 90%, 34.7%, 20%, 5%。以上为基于摘要的忠实中文概括，英文术语和数值仍需对照 PDF 复核。

## 3. 方法动机
论文在 Introduction 中讨论目标任务的现有痛点；未明确量化之处记为 unknown。

## 4. 方法设计
### 4.1 方法整体流程
原始网络数据 → 论文定义的预处理/表示 → 核心模型或算法 → 任务输出。
### 4.2 输入-处理-输出
|输入|处理|输出|
|---|---|---|
|网络数据|预处理并执行核心方法|预测、测量或通信结果|
### 4.3 方法模块
核心模块及参数需以正文 Method 和算法框核验；当前摘要未给出完整细节。

## 5. 与其他方法对比
论文将方法与相关 baseline 比较，具体差异和迁移性需结合实验表核验。

## 6. 实验表现与优势
### 6.1 数据集
unknown（摘要未完整列出）。
### 6.2 Baseline
unknown。
### 6.3 指标
unknown。
### 6.4 关键结果
原文摘要未提供可核对的完整数值表，保留为 unknown。
### 6.5 局限性
代码、跨数据集泛化、部署资源和数据划分细节待人工核验。

## 7. 学习与应用
### 7.1 开源/复现
unknown。建议依据正文复核数据获取、预处理、超参数和训练划分。
### 7.2 迁移启发
可参考其“输入表示—核心方法—任务指标”链条迁移到相近网络任务，但需重新验证。

## 8. 总结
### 8.1 核心思想

摘要所示核心思想：自回归流量矩阵补全与流感知 tokenization；具体模块、数据划分和数值结果以 §2.2 及正文为准。

### 8.2 Pipeline
1. 准备数据；2. 预处理；3. 核心方法；4. 输出；5. 评估。

## 9. Obsidian 知识链接
- [[traffic-classification]]
- [[method-comparison-table]]

## 10. 证据记录
|观点|依据|位置|
|---|---|---|
|研究问题与方法名称|标题、摘要|Abstract|

## 11. 原始资料链接
- MinerU：[[2026-INFOCOM-ARI-LLM__Autoregressive_Imputation_for_Network_Traffic_Matrix_via_Large_Language_Models.md]]

## 12. 后续问题
- 需人工补录正文中的数据集、baseline、指标、结果和开源链接。

## 13. 抽取质量与证据核验
- MinerU 文本可能存在连字符断行、特殊符号替换、公式或表格结构丢失等问题；涉及方法细节、数值和专有名词的内容需回看 PDF。
- DOI、原文链接和代码字段已依据批次元数据及解析文本补入；未发现明确代码仓库时保留 `unknown`。
- 摘要翻译与一句话总结基于元数据摘要生成，仍需人工核对术语、缩写和上下文。


## 2026-11-18　后续扩展

[[03-paper-notes/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models|MPA-LLM]] 在 §I 与 §II-C 明确以前作 ARI-LLM 为起点。扩展增加阶段独立参数及插补、预测、异常检测的统一接口。比较时对照其表 V 的 GÉANT 与 WS-DREAM，并在同团队记录中标注结果依赖。

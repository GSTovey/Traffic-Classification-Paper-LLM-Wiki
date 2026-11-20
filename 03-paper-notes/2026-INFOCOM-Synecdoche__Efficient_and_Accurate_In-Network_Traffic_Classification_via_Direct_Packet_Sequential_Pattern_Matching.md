---
type: paper
title_original: "Synecdoche: Efficient and Accurate In-Network Traffic Classification via Direct Packet Sequential Pattern Matching"
title_cn: "Synecdoche：基于直接包序列模式匹配的高效网内流量分类"
authors: ["Minyuan Xiao", "Yunchun Li", "Yuchen Zhao", "Tong Guan", "Mingyuan Xia", "Wei Li"]
year: 2026
venue: "INFOCOM"
doi: "10.1109/INFOCOM59046.2026.11571501"
url: "https://doi.org/10.1109/INFOCOM59046.2026.11571501"
pdf: "../00-inbox/PDFs/2026-INFOCOM-Synecdoche__Efficient_and_Accurate_In-Network_Traffic_Classification_via_Direct_Packet_Sequential_Pattern_Matching.pdf"
mineru_md: "../02-parsed-markdown/2026-INFOCOM-Synecdoche__Efficient_and_Accurate_In-Network_Traffic_Classification_via_Direct_Packet_Sequential_Pattern_Matching.md"
status: processed
reading_level: L2
research_area: ["traffic classification"]
task: [unknown]
method: ["unknown"]
dataset: [unknown]
code: "https://github.com/swampx/Synecdoche"
relevance: medium
created: "2026-10-26"
updated: "2026-11-20"
---

# Synecdoche: Efficient and Accurate In-Network Traffic Classification via Direct Packet Sequential Pattern Matching

## 0. 论文基础信息
|项目|内容|
|---|---|
|原文标题|Synecdoche: Efficient and Accurate In-Network Traffic Classification via Direct Packet Sequential Pattern Matching|
|作者|Minyuan Xiao, Yunchun Li, Yuchen Zhao, Tong Guan, Mingyuan Xia, Wei Li\* Beihang University|
|年份|2026|
|会议/期刊|INFOCOM|
|研究方向|traffic classification|
|方法关键词|unknown|
|数据集|unknown|
|是否开源|unknown|

## 1. 一句话总结
> 本文围绕“Synecdoche: Efficient and Accurate In-Network Traffic Classification via Direct Packet Sequential Pattern Matching”研究网络流量相关问题。摘要明确指出：Traffic classification on programmable data plane holds great promise for line-rate processing, with methods evolving from per-packet to flow-level analysis for higher accuracy.

## 2. 摘要翻译
### 2.1 摘要原文
Traffic classification on programmable data plane holds great promise for line-rate processing, with methods evolving from per-packet to flow-level analysis for higher accuracy. However, a trade-off between accuracy and efficiency persists. Statistical feature-based methods align with hardware constraints but often exhibit limited accuracy, while online deep learning methods using packet sequential features achieve superior accuracy but require substantial computational resources. This paper presents Synecdoche, the first traffic classification framework that successfully deploys packet sequential features on a programmable data plane via pattern matching, achieving both high accuracy and efficiency. Our key insight is that discriminative information concentrates in short sub-sequences—termed Key Segments—that serve as compact traffic features for efficient data plane matching. Synecdoche employs an "offline discovery, online matching" paradigm: deep learning models automatically discover Key Segment patterns offline, which are then compiled into optimized table entries for direct data plane matching. Extensive experiments demonstrate Synecdoche's superior accuracy, improving F1-scores by up to 26.4% against statistical methods and 18.3% against online deep learning methods, while reducing latency by 13.0% and achieving 79.2% reduction in SRAM usage.
### 2.2 摘要中文翻译
摘要具体指出，本文研究“Synecdoche: Efficient and Accurate In-Network Traffic Classification via Direct Packet Sequential Pattern Matching”所针对的问题。方法上，摘要描述了：Traffic classification on programmable data plane holds great promise for line-rate processing, with methods evolving from per-packet to flow-level analysis for higher accuracy.。结果上，摘要报告：Traffic classification on programmable data plane holds great promise for line-rate processing, with methods evolving from per-packet to flow-level analysis for higher accuracy.；摘要中的关键数值包括 26.4%, 18.3%, 13.0%, 79.2%。以上为基于摘要的忠实中文概括，英文术语和数值仍需对照 PDF 复核。

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

摘要所示核心思想：直连包序列模式匹配的线速分类；具体模块、数据划分和数值结果以 §2.2 及正文为准。

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
- MinerU：[[2026-INFOCOM-Synecdoche__Efficient_and_Accurate_In-Network_Traffic_Classification_via_Direct_Packet_Sequential_Pattern_Matching.md]]

## 12. 后续问题
- 需人工补录正文中的数据集、baseline、指标、结果和开源链接。

## 13. 抽取质量与证据核验
- MinerU 文本可能存在连字符断行、特殊符号替换、公式或表格结构丢失等问题；涉及方法细节、数值和专有名词的内容需回看 PDF。
- DOI、原文链接和代码字段已依据批次元数据及解析文本补入；未发现明确代码仓库时保留 `unknown`。
- 摘要翻译与一句话总结基于元数据摘要生成，仍需人工核对术语、缩写和上下文。

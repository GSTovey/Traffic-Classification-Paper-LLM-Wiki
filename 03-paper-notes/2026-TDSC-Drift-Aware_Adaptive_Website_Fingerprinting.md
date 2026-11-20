---
type: paper
title_original: "Drift-Aware Adaptive Website Fingerprinting"
title_cn: "漂移感知的自适应网站指纹识别"
authors: ["Zhengge Yi", "Tengyao Li", "Jingxi Zhang", "Yifei Meng", "Xiangyang Luo"]
year: 2026
venue: "TDSC"
doi: "10.1109/TDSC.2026.3723526"
url: "https://doi.org/10.1109/TDSC.2026.3723526"
pdf: "../00-inbox/PDFs/2026-TDSC-Drift-Aware_Adaptive_Website_Fingerprinting.pdf"
mineru_md: "../02-parsed-markdown/2026-TDSC-Drift-Aware_Adaptive_Website_Fingerprinting.md"
status: processed
reading_level: L2
research_area: ["website fingerprinting"]
task: [unknown]
method: ["unknown"]
dataset: [unknown]
code: "https://github.com/XinhaoDeng/Website-Fingerprinting-Library"
relevance: medium
created: "2026-10-26"
updated: "2026-11-20"
---

# Drift-Aware Adaptive Website Fingerprinting

## 0. 论文基础信息
|项目|内容|
|---|---|
|原文标题|Drift-Aware Adaptive Website Fingerprinting|
|作者|Zhengge Yi, Tengyao Li, Jingxi Zhang, Yifei Meng, Xiangyang Luo|
|年份|2026|
|会议/期刊|TDSC|
|研究方向|website fingerprinting|
|方法关键词|unknown|
|数据集|unknown|
|是否开源|unknown|

## 1. 一句话总结
> 本文围绕“Drift-Aware Adaptive Website Fingerprinting”研究网络流量相关问题。摘要明确指出：Website fingerprinting (WF) attacks infer websites visited by Tor users from encrypted traffic metadata.

## 2. 摘要翻译
### 2.1 摘要原文
Website fingerprinting (WF) attacks infer websites visited by Tor users from encrypted traffic metadata. Deeplearning-based WF attacks achieve high accuracy under controlled conditions but degrade substantially under traffic drift, where the deployment distribution progressively deviates from the training distribution. Recent unsupervised self-training methods address this problem by using high-confidence predictions on unlabeled drifted traffic as pseudo-labels to refine deployed models. However, fixed unsupervised adaptation strategies cannot adequately handle heterogeneous drift across websites, and severely drifted classes may fail to produce reliable pseudo-labels, resulting in persistent adaptation blind spots. We propose Aion, a hybrid drift-aware adaptive WF framework that combines unsupervised self-training with limited labeled target-domain supervision for continuous deployment under traffic drift. Aion dynamically regulates the source-domain constraint according to measured distributional divergence, broadens pseudo-label coverage through dual-classifier collaborative generation to accelerate performance recovery, and selectively restores supervision for classes where purely unsupervised adaptation fails. Extensive experiments on real Tor traces across multiple drift scenarios show that Aion consistently outperforms existing methods. Under 270 days of real-world traffic drift, Aion achieves F1-scores of 88.14%, 82.84%, and 86.32% in the closed-world, open-world, and streaming settings, exceeding the best baselines by 5.87, 8.90, and 10.92 percentage points, respectively.
### 2.2 摘要中文翻译
摘要具体指出，本文研究“Drift-Aware Adaptive Website Fingerprinting”所针对的问题。方法上，摘要描述了：Recent unsupervised self-training methods address this problem by using high-confidence predictions on unlabeled drifted traffic as pseudo-labels to refine deployed models.。结果上，摘要报告：Deeplearning-based WF attacks achieve high accuracy under controlled conditions but degrade substantially under traffic drift, where the deployment distribution progressively deviates from the training distribution.；摘要中的关键数值包括 270, 88.14%, 82.84%, 86.32%, 5.87, 8.90, 10.92。以上为基于摘要的忠实中文概括，英文术语和数值仍需对照 PDF 复核。

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

摘要所示核心思想：漂移感知的自适应网站指纹；具体模块、数据划分和数值结果以 §2.2 及正文为准。

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
- MinerU：[[2026-TDSC-Drift-Aware_Adaptive_Website_Fingerprinting.md]]

## 12. 后续问题
- 需人工补录正文中的数据集、baseline、指标、结果和开源链接。

## 13. 抽取质量与证据核验
- MinerU 文本可能存在连字符断行、特殊符号替换、公式或表格结构丢失等问题；涉及方法细节、数值和专有名词的内容需回看 PDF。
- DOI、原文链接和代码字段已依据批次元数据及解析文本补入；未发现明确代码仓库时保留 `unknown`。
- 摘要翻译与一句话总结基于元数据摘要生成，仍需人工核对术语、缩写和上下文。

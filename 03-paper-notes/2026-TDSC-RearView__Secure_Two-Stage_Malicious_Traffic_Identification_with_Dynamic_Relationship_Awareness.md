---
type: paper
title_original: "RearView: Secure Two-Stage Malicious Traffic Identification with Dynamic Relationship Awareness"
title_cn: "RearView：基于动态关系感知的两阶段恶意流量识别"
authors: ["Peng Fang", "Ziming Zhao", "Ziqi Yang", "Yixin Jiang", "Wenqian Xu", "Zhihong Liang", "Fan Zhang"]
year: 2026
venue: "TDSC"
doi: "10.1109/TDSC.2026.3720570"
url: "https://doi.org/10.1109/TDSC.2026.3720570"
pdf: "../00-inbox/PDFs/2026-TDSC-RearView__Secure_Two-Stage_Malicious_Traffic_Identification_with_Dynamic_Relationship_Awareness.pdf"
mineru_md: "../02-parsed-markdown/2026-TDSC-RearView__Secure_Two-Stage_Malicious_Traffic_Identification_with_Dynamic_Relationship_Awareness.md"
status: processed
reading_level: L2
research_area: ["encrypted traffic"]
task: ["malicious traffic detection"]
method: ["unknown"]
dataset: ["UNSW-NB15, CrossAttack"]
code: "unknown"
relevance: medium
created: "2026-10-26"
updated: "2026-11-20"
---

# RearView: Secure Two-Stage Malicious Traffic Identification with Dynamic Relationship Awareness

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | RearView: Secure Two-Stage Malicious Traffic Identification with Dynamic Relationship Awareness |
| 中文标题 | unknown |
| 作者 | unknown |
| 年份 | 2026 |
| 会议/期刊 | TDSC |
| 研究方向 | encrypted traffic |
| 任务类型 | malicious traffic detection |
| 方法关键词 | 论文未明确说明 |
| 数据集 | UNSW-NB15, CrossAttack |
| 是否开源 | unknown |
| PDF | [[2026-TDSC-RearView__Secure_Two-Stage_Malicious_Traffic_Identification_with_Dynamic_Relationship_Awareness.pdf]] |
| MinerU Markdown | [[2026-TDSC-RearView__Secure_Two-Stage_Malicious_Traffic_Identification_with_Dynamic_Relationship_Awareness.md]] |

## 1. 一句话总结
> 本文围绕“RearView: Secure Two-Stage Malicious Traffic Identification with Dynamic Relationship Awareness”研究网络流量相关问题。摘要明确指出：High-throughput enterprise networks face increasingly sophisticated cyber threats, making dependable and realtime malicious traffic detection a cornerstone of cyber security and operational resilience.

## 2. 摘要翻译
### 2.1 摘要原文
High-throughput enterprise networks face increasingly sophisticated cyber threats, making dependable and realtime malicious traffic detection a cornerstone of cyber security and operational resilience. Existing methods suffer from two critical flaws: lightweight intra-flow approaches lack servicespecific discrimination, leading to high false negatives against mimicry attacks; meanwhile, static graph-based inter-flow methods incur prohibitive latency and memory costs, failing to adapt to dynamic network environments. To address these issues, we propose RearView, a two-stage dynamic relationship-aware framework for real-time malicious traffic identification. First, it deploys service-personalized Variational Autoencoders (VAEs) to rapidly screen and filter out benign traffic. Second, for the remaining suspicious flows, RearView constructs dynamic session graphs and applies anomaly-weighted graph neural networks to uncover hidden inter-flow attack patterns. A streaming cache mechanism ensures this relational mining remains highly efficient and adaptable. Extensive evaluations on four benchmark datasets and one self-constructed CrossAttack dataset show that RearView achieves an average F1-score of 97.79%, outperforming stateof-the-art methods by 10.19% on average. It reduces the false positive rate by 4.99% and false negative rate by 34.44%, while attaining a significantly lower detection latency than contemporary methods of the same type, and exhibits robust resistance against mimicry and data pollution attacks.
### 2.2 摘要中文翻译
摘要具体指出，本文研究“RearView: Secure Two-Stage Malicious Traffic Identification with Dynamic Relationship Awareness”所针对的问题。方法上，摘要描述了：Existing methods suffer from two critical flaws: lightweight intra-flow approaches lack servicespecific discrimination, leading to high false negatives against mimicry attacks; meanwhile, static graph-based inter-flow methods incur prohibitive latency and memory costs, failing to adapt to dynamic network environments.。结果上，摘要报告：Extensive evaluations on four benchmark datasets and one self-constructed CrossAttack dataset show that RearView achieves an average F1-score of 97.79%, outperforming stateof-the-art methods by 10.19% on average.；摘要中的关键数值包括 97.79%, 10.19%, 4.99%, 34.44%。以上为基于摘要的忠实中文概括，英文术语和数值仍需对照 PDF 复核。

## 3. 方法动机
### 3.1 作者为什么提出这个方法？
摘要明确指出：High-throughput enterprise networks face increasingly sophisticated cyber threats, making dependable and realtime malicious traffic detection a cornerstone of cyber security and operational resilience.
### 3.2 现有方法的痛点和不足
High-throughput enterprise networks face increasingly sophisticated cyber threats, making dependable and realtime malicious traffic detection a cornerstone of cyber security and operational resilience. Existing methods suffer from two critical flaws: lightweight intra-flow approaches lack servicespecific discrimination, leading to high false negatives against mimicry attacks; meanwhile, static gra
### 3.3 论文的研究假设或核心直觉
论文未明确给出可单独检验的假设。
### 3.4 问题发现路径
|阶段|内容|证据来源|
|---|---|---|
|现象观察|网络流量安全任务存在挑战|摘要|
|痛点提炼|需要改进检测、分类或通信能力|摘要|
|问题转化|提出本文方案|摘要/引言|
### 3.5 科学假设形成
论文摘要未说明，需核对正文。

## 4. 方法设计
### 4.1 方法整体流程
输入与输出应以正文方法章节为准；摘要明确研究目标为“RearView: Secure Two-Stage Malicious Traffic Identification with Dynamic Relationship Awareness”。
### 4.2 详细 Pipeline
|步骤|输入|具体操作|输出|作用|
|---|---|---|---|---|
|1|论文定义的输入数据|按摘要所述方法处理|中间表示或状态|形成模型输入|
|2|中间表示|应用论文提出的模型/机制|中间结果|完成建模|
|3|中间结果|生成论文任务输出|预测/重建/检测结果|完成评估|
### 4.3 模型结构或系统模块
模块细节需依据方法章节核对。
### 4.4 公式、算法和机制解释
论文摘要未说明，需核对正文。
### 4.5 方法优势
摘要报告该方法在“RearView: Secure Two-Stage Malicious Traffic Identification with Dynamic Relationship Awareness”任务上的实验表现，具体提升幅度需以结果表核对。
### 4.6 方法不足
论文摘要未说明，需核对正文。

## 5. 与其他方法对比
### 5.1 与主流方法的本质区别
摘要将研究重点明确为“RearView: Secure Two-Stage Malicious Traffic Identification with Dynamic Relationship Awareness”；与既有方法的差异需结合正文比较。
### 5.2 创新点分析
|创新点|具体内容|贡献度|是否可迁移|
|---|---|---|---|
|核心方法设计|摘要提出的模型或机制|中|待验证|
### 5.3 适用场景
适用范围由“RearView: Secure Two-Stage Malicious Traffic Identification with Dynamic Relationship Awareness”的实验对象决定，需结合数据集与部署设置核对。
### 5.4 方法对比表
|方法|优点|缺点|本文改进点|
|---|---|---|---|
|现有方法|相关工作所述|相关工作所述|本文方案|

## 6. 实验表现与优势
### 6.1 实验设计和设置
摘要报告了实验结果；数据集、基线与指标的完整设置需以正文实验章节核对。
### 6.2 数据集
UNSW-NB15, CrossAttack
### 6.3 Baseline
论文摘要未说明，需核对正文。
### 6.4 评价指标
论文摘要未说明，需核对正文。
### 6.5 关键实验结果
|任务/数据集|指标|本文方法|最优对比方法|提升|说明|
|---|---|---:|---:|---:|---|
|malicious traffic detection|unknown|unknown|unknown|unknown|需核对实验表格|
### 6.6 优势最明显的场景
论文摘要未说明，需核对正文。
### 6.7 局限性
论文摘要未说明，需核对正文。

## 7. 学习与应用
### 7.1 是否开源？
unknown
### 7.2 复现关键步骤
1. 获取数据集与预处理配置。
2. 按方法章节实现模型或协议流程。
3. 按论文指标复核。
### 7.3 关键超参数、预处理和训练细节
论文摘要未说明，需核对正文。
### 7.4 能否迁移到其他任务？
未知，需要实验验证。
### 7.5 对我的研究有什么启发？
可作为 encrypted traffic 方法参考。

## 8. 总结
### 8.1 核心思想

摘要所示核心思想：动态关系感知的两阶段恶意流量识别；具体模块、数据划分和数值结果以 §2.2 及正文为准。

### 8.2 速记版 Pipeline
1. 输入流量。 2. 提取表示。 3. 应用模型。 4. 输出结果。 5. 评估。

## 9. Obsidian 知识链接
- [[encrypted-traffic-analysis]]
- [[traffic-classification]]
- [[method-comparison-table]]

## 13. 抽取质量与证据核验
- MinerU 文本可能存在连字符断行、特殊符号替换、公式或表格结构丢失等问题；涉及方法细节、数值和专有名词的内容需回看 PDF。
- DOI、原文链接和代码字段已依据批次元数据及解析文本补入；未发现明确代码仓库时保留 `unknown`。
- 摘要翻译与一句话总结基于元数据摘要生成，仍需人工核对术语、缩写和上下文。

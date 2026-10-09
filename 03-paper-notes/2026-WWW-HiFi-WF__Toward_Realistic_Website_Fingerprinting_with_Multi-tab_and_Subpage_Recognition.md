---
type: paper
title_original: "HiFi-WF: Toward Realistic Website Fingerprinting with Multi-tab and Subpage Recognition"
title_cn: ""
authors: []
year: 2026
venue: WWW
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-WWW-HiFi-WF__Toward_Realistic_Website_Fingerprinting_with_Multi-tab_and_Subpage_Recognition.pdf"
mineru_md: "02-parsed-markdown/2026-WWW-HiFi-WF__Toward_Realistic_Website_Fingerprinting_with_Multi-tab_and_Subpage_Recognition.md"
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

# HiFi-WF: Toward Realistic Website Fingerprinting with Multi-tab and Subpage Recognition

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | HiFi-WF: Toward Realistic Website Fingerprinting with Multi-tab and Subpage Recognition |
| 年份 | 2026 |
| 会议/期刊 | WWW |
| PDF | [[2026-WWW-HiFi-WF__Toward_Realistic_Website_Fingerprinting_with_Multi-tab_and_Subpage_Recognition.pdf]] |
| MinerU Markdown | [[2026-WWW-HiFi-WF__Toward_Realistic_Website_Fingerprinting_with_Multi-tab_and_Subpage_Recognition.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
Website Fingerprinting (WF) is an emerging trafic analysis technique that enables a passive adversary to infer which websites a user visits. However, most existing studies, whether in single tab or multi-tab settings, rely on the unrealistic assumption that users only access website homepages, diverging significantly from real-world browsing behavior. Even recent works extending WF to subpages primarily focus on website-level identification, with out distinguishing which specific subpages are visited, thereby limiting the attack’s granularity and scope. In this paper, we propose HiFi-WF (Hierarchical Fine-grained Website Fingerprinting), a novel framework that breaks the homepage-only assumption and extends WF to multi-tab recognition and fine-grained subpage identification. We formulate the task as a hierarchical multi-label classification problem, jointly modeling the distinctions and correlations between homepages and subpages. To this end, HiFi-WF integrates a unified CNN-based extractor and layered encoder with a Feature Interaction Module based on multi-head cross-attention to capture inter-level dependencies. An Enhanced SubHead enforces hierarchical constraints to suppress invalid subpage predictions, while a cascaded channel–spatial attention mechanism refines discriminative features for precise hierarchical identification. Experi mental results demonstrate that HiFi-WF achieves state-of-the-art performance at both hierarchical levels, attaining F1-scores of 92.1% (homepage) and 81.9% (subpage), thereby validating its efective ness in advancing WF attacks toward realistic, fine-grained, and multi-tab browsing scenarios. Related codes and datasets can be found in https://github.com/wusongyang02-blip/HiFi-WF.

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
- 主题线索：website fingerprint, tor, transformer。
- 摘要证据：Website Fingerprinting (WF) is an emerging trafic analysis technique that enables a passive adversary to infer which websites a user visits. However, most existing studies, whether in single tab or multi-tab settings, rely on the unrealistic assumption that users only access website homepages, diverging significantly from real-world browsing behavior. Even recent works extending WF to subpages primarily focus on website-level identification, with out distinguishing which specific subpages are visited, thereby limiting the attack’s granularity and scope. In this paper, we propose HiFi-WF (Hierarchical Fine-grained Website Fingerprinting), a novel framework that breaks the homepage-only assumption and extends WF to multi-tab recognition and fine-grained subpage identification. We formulate the task as a hierarchical multi-label classification problem, jointly modeling the distinctions and correlations between homepages and subpages. To this end, HiFi-WF integrates a unified CNN-based extractor and layered encoder with a Feature Interaction Module based on multi-head cross-attention to capture inter-level dependencies. An Enhanced SubHead enforces hierarchical constraints to suppress invalid subpage predictions, while a cascaded channel–spatial attention mechanism refines discriminative features for precise hierarchical identification. Experi mental results demonstrate that HiFi-WF achieves state-of-the-art performance at both hierarchical levels, attaining F1-scores of 92.1% (homepage) and 81.9% (subpage), thereby validating its efective ness in advancing WF attacks toward realistic, fine-grained, and multi-tab browsing scenarios. Related codes and datasets can be found in https://github.com/wusongyang02-blip/HiFi-WF.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
Table 5: Two-tab Performance on Homepage and Subpage under Defense of HiFi-WF <table><tr><td rowspan="2">Defense</td><td colspan="5">Homepage</td><td colspan="5">Subpage</td></tr><tr><td>Precision</td><td>Recall</td><td>F1-score</td><td>P@2</td><td>MAP@2</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>P@2</td><td>MAP@2</td></tr><tr><td>Random [25]</td><td>0.902</td><td>0.806</td><td>0.852</td><td>0.860</td><td>0.853</td><td>0.788</td><td>0.725</td><td>0.755</td><td>0.760</td><td>0.741</td></tr><tr><td>WTF-PAD [20]</td><td>0.831</td><td>0.723</td><td>0.773</td><td>0.775</td><td>0.761</td><td>0.711</td><td>0.602</td><td>0.652</td><td>0.632</td><td>0.607</td></tr><tr><td>Front [13]</td><td>0.785</td><td>0.661</td><td>0.718</td><td>0.724</td><td>0.708</td><td>0.554</td><td>0.544</td><td>0.549</td><td>0.588</td><td>0.566</td></tr></table> Table 6: Ablation Experiments on Hierarchical Classification in 2-tab Scenarios of HiFi-WF <table><tr><td rowspan="2">Ablation Module</td><td colspan="5">Homepage</td><td colspan="5">Subpage</td></tr><tr><td>Precision</td><td>Recall</td><td>F1-score</td><td>P@2</td><td>MAP@2</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>P@2</td><td>MAP@2</td></tr><tr><td>w/o Feature Enhancer</td><td>0.959</td><td>0.748</td><td>0.841</td><td>0.788</td><td>0.785</td><td>0.894</td><td>0.711</td><td>0.792</td><td>0.759</td><td>0.751</td></tr><tr><td>w/o Hierarchical Feature Interaction</td><td>0.985</td><td>0.772</td><td>0.866</td><td>0.823</td><td>0.819</td><td>0.824</td><td>0.753</td><td>0.787</td><td>0.785</td><td>0.771</td></tr><tr><td>w/o Enhanced Sub-Head</td><td>0.952</td><td>0.862</td><td>0.905</td><td>0.905</td><td>0.900</td><td>0.869</td><td>0.762</td><td>0.812</td><td>0.799</td><td>0.791</td></tr></table> Experiment 2: Removing 

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。

## 深度分析（2026-09-29）

- reading_level: L3
- 研究定位：层次化多标签WF/子页面识别
- 方法机制：HiFi-WF针对homepage-only假设，联合建模网站与子页面层级，使用CNN extractor、分层encoder、多头交叉注意力Feature Interaction Module及层次约束SubHead。
- 输入—处理—输出：输入多标签、多标签页Tor流量；输出网站层和具体子页面层预测。
- 证据边界：当前证据确认方法定位，具体数据集、层级指标、相对提升和开销待正文核验。
- 联动标签：website-fingerprinting；DNS；anomaly-detection；traffic-security


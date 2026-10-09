---
type: paper
title_original: "AdvTG: An Adversarial Trafic Generation Framework to Deceive DL-Based Malicious Trafic Detection Models"
title_cn: ""
authors: []
year: 2025
venue: WWW
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2025-WWW-AdvTG__An_Adversarial_Traffic_Generation_Framework_to_Deceive_DL-Based_Malicious_Traffic_Detection_Models.pdf"
mineru_md: "02-parsed-markdown/2025-WWW-AdvTG__An_Adversarial_Traffic_Generation_Framework_to_Deceive_DL-Based_Malicious_Traffic_Detection_Models.md"
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

# AdvTG: An Adversarial Trafic Generation Framework to Deceive DL-Based Malicious Trafic Detection Models

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | AdvTG: An Adversarial Trafic Generation Framework to Deceive DL-Based Malicious Trafic Detection Models |
| 年份 | 2025 |
| 会议/期刊 | WWW |
| PDF | [[2025-WWW-AdvTG__An_Adversarial_Traffic_Generation_Framework_to_Deceive_DL-Based_Malicious_Traffic_Detection_Models.pdf]] |
| MinerU Markdown | [[2025-WWW-AdvTG__An_Adversarial_Traffic_Generation_Framework_to_Deceive_DL-Based_Malicious_Traffic_Detection_Models.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
Deep learning-based (DL-based) malicious trafic detection models are efective but vulnerable to adversarial attacks. Existing adver sarial attacks have shown promising results when targeting trafic detection models based on statistics and sequence features. However, these attacks are less efective against models that rely on payload analysis. The main reason is the dificulty in generating semantic, compliant, and functional payloads, which limits their practical application. In this paper, we propose AdvTG, an adversarial trafic generation framework to deceive DL-based malicious trafic based on the large language model (LLM) and reinforcement learning (RL). Specifically, AdvTG is designed to attack various DL-based detection models across diverse payload features and architectures, thereby enhancing the generalization capabilities of the generated adversarial trafic. Moreover, we design a specialized prompt for trafic generation tasks, where functional fields and target types are supplied as input, while non-functional fields are generated to produce the mutated trafic. This fine-tuning endows the LLM with task comprehension and trafic pattern reasoning abilities, al lowing it to generate trafic that remains compliant and functional. Furthermore, leveraging RL, AdvTG automatically selects trafic fields that exhibit more robust adversarial properties. Experimental results show that AdvTG achieves over 40% attack success rate (ASR) across six detection models on four base datasets and two extended datasets, significantly outperforming other adversarial attack methods.

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
- 主题线索：anomaly, tor, transformer, adversarial。
- 摘要证据：Deep learning-based (DL-based) malicious trafic detection models are efective but vulnerable to adversarial attacks. Existing adver sarial attacks have shown promising results when targeting trafic detection models based on statistics and sequence features. However, these attacks are less efective against models that rely on payload analysis. The main reason is the dificulty in generating semantic, compliant, and functional payloads, which limits their practical application. In this paper, we propose AdvTG, an adversarial trafic generation framework to deceive DL-based malicious trafic based on the large language model (LLM) and reinforcement learning (RL). Specifically, AdvTG is designed to attack various DL-based detection models across diverse payload features and architectures, thereby enhancing the generalization capabilities of the generated adversarial trafic. Moreover, we design a specialized prompt for trafic generation tasks, where functional fields and target types are supplied as input, while non-functional fields are generated to produce the mutated trafic. This fine-tuning endows the LLM with task comprehension and trafic pattern reasoning abilities, al lowing it to generate trafic that remains compliant and functional. Furthermore, leveraging RL, AdvTG automatically selects trafic fields that exhibit more robust adversarial properties. Experimental results show that AdvTG achieves over 40% attack success rate (ASR) across six detection models on four base datasets and two extended datasets, significantly outperforming other adversarial attack methods.

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
- 方法/问题：AdvTG uses LLM plus reinforcement learning to generate semantic, protocol-compliant adversarial traffic targeting payload/statistical/sequence detectors; prompt constraints preserve functional fields. Evidence: abstract and method sections in MinerU. Missing: exact RL state/action/reward, datasets, attack success and overhead tables.
- 证据边界：以上仅使用对应 MinerU 解析稿摘要及可稳定提取段落；未提取到的数值、数据集、代码和参数均不作推断。
- 复现建议：先核对原文表格、附录、代码仓库和数据划分，再确定 L3/L4 复现。

---
type: paper
title_original: "Helios: Learning and Adaptation of Matching Rules for Continual In-Network Malicious Trafic Detection"
title_cn: ""
authors: []
year: 2025
venue: WWW
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2025-WWW-Helios__Learning_and_Adaptation_of_Matching_Rules_for_Continual_In_Network_Malicious_Traffic_Detection.pdf"
mineru_md: "02-parsed-markdown/2025-WWW-Helios__Learning_and_Adaptation_of_Matching_Rules_for_Continual_In_Network_Malicious_Traffic_Detection.md"
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

# Helios: Learning and Adaptation of Matching Rules for Continual In-Network Malicious Trafic Detection

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Helios: Learning and Adaptation of Matching Rules for Continual In-Network Malicious Trafic Detection |
| 年份 | 2025 |
| 会议/期刊 | WWW |
| PDF | [[2025-WWW-Helios__Learning_and_Adaptation_of_Matching_Rules_for_Continual_In_Network_Malicious_Traffic_Detection.pdf]] |
| MinerU Markdown | [[2025-WWW-Helios__Learning_and_Adaptation_of_Matching_Rules_for_Continual_In_Network_Malicious_Traffic_Detection.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
Network Intrusion Detection Systems (NIDS) are critical for web security by identifying and blocking malicious trafic. In-network NIDS leverage programmable switches for high-speed trafic pro cessing. However, they are unable to reconcile the fine-grained classification of known classes and the identification of unseen attacks. Moreover, they lack support for incremental updates. In this paper, we propose Helios, an in-network malicious trafic detection system, for continual adaptation in attack-incremental scenarios. First, we design a novel Supervised Mixture Prototypical Learning (SMPL) method combined with clustering initialization to learn prototypes that encapsulate the knowledge, based on the weighted infinity norm distance. SMPL enables known class classification and unseen attack identification through similarity comparison between prototypes and samples. Then, we design boundary calibration and overlap refinement to transform learned prototypes into priority guided matching rules, ensuring precise and eficient in-network deployment. Additionally, Helios supports incremental prototype learning and rule updates, achieving low-cost hardware reconfigu ration. We implement Helios on a Tofino switch and evaluation on three datasets shows that Helios achieves superior performance in classifying known classes (92%+ in ACC and F1) as well as identi fying unseen attacks (62% - 98% in TPR). Helios has also reduced resource consumption and reconfiguration time, demonstrating its scalability and eficiency for real-world deployment.

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
- 主题线索：anomaly, tor。
- 摘要证据：Network Intrusion Detection Systems (NIDS) are critical for web security by identifying and blocking malicious trafic. In-network NIDS leverage programmable switches for high-speed trafic pro cessing. However, they are unable to reconcile the fine-grained classification of known classes and the identification of unseen attacks. Moreover, they lack support for incremental updates. In this paper, we propose Helios, an in-network malicious trafic detection system, for continual adaptation in attack-incremental scenarios. First, we design a novel Supervised Mixture Prototypical Learning (SMPL) method combined with clustering initialization to learn prototypes that encapsulate the knowledge, based on the weighted infinity norm distance. SMPL enables known class classification and unseen attack identification through similarity comparison between prototypes and samples. Then, we design boundary calibration and overlap refinement to transform learned prototypes into priority guided matching rules, ensuring precise and eficient in-network deployment. Additionally, Helios supports incremental prototype learning and rule updates, achieving low-cost hardware reconfigu ration. We implement Helios on a Tofino switch and evaluation on three datasets shows that Helios achieves superior performance in classifying known classes (92%+ in ACC and F1) as well as identi fying unseen attacks (62% - 98% in TPR). Helios has also reduced resource consumption and reconfiguration time, demonstrating its scalability and eficiency for real-world deployment.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：未检测到明确 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


### 并行深度分析（2026-09-29）
- 方法/问题：Helios supports continual in-network malicious traffic detection with supervised mixture prototypical learning, clustering initialization, weighted infinity-norm prototypes, boundary calibration and overlap refinement for known/unseen attacks and incremental updates. Missing: switch target/resource limits, traffic features, attack-incremental schedule and full metrics.
- 证据边界：以上仅使用对应 MinerU 解析稿摘要及可稳定提取段落；未提取到的数值、数据集、代码和参数均不作推断。
- 复现建议：先核对原文表格、附录、代码仓库和数据划分，再确定 L3/L4 复现。

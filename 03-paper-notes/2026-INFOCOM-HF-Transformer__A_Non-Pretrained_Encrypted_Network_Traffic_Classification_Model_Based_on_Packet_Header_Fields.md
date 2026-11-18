---
type: paper
title_original: "HF-Transformer: A Non-Pretrained Encrypted Network Traffic Classification Model Based on Packet Header Fields"
title_cn: "unknown"
authors: ["Zhenzhen Yan", "Lizhi Peng", "Peiqiang Liu", "Yingshuo Bao", "Bo Yang"]
year: 2026
venue: "INFOCOM"
doi: "10.1109/INFOCOM59046.2026.11571583"
url: "https://doi.org/10.1109/INFOCOM59046.2026.11571583"
pdf: "../00-inbox/PDFs/2026-INFOCOM-HF-Transformer__A_Non-Pretrained_Encrypted_Network_Traffic_Classification_Model_Based_on_Packet_Header_Fields.pdf"
mineru_md: "../02-parsed-markdown/2026-INFOCOM-HF-Transformer__A_Non-Pretrained_Encrypted_Network_Traffic_Classification_Model_Based_on_Packet_Header_Fields.md"
status: processed
reading_level: L3
research_area: ["traffic classification"]
task: [unknown]
method: ["Transformer"]
dataset: [unknown]
code: "unknown"
relevance: medium
created: "2026-10-26"
updated: "2026-10-26"
---

# HF-Transformer: A Non-Pretrained Encrypted Network Traffic Classification Model Based on Packet Header Fields

## 0. 论文基础信息
|项目|内容|
|---|---|
|原文标题|HF-Transformer: A Non-Pretrained Encrypted Network Traffic Classification Model Based on Packet Header Fields|
|作者|Zhenzhen Yan1,\*, Lizhi Peng2,3, Peiqiang Liu1, Yingshuo Bao4, and Bo Yang2,3|
|年份|2026|
|会议/期刊|INFOCOM|
|研究方向|traffic classification|
|方法关键词|Transformer|
|数据集|unknown|
|是否开源|unknown|

## 1. 一句话总结
> 本文围绕“HF-Transformer: A Non-Pretrained Encrypted Network Traffic Classification Model Based on Packet Header Fields”研究网络流量相关问题。摘要明确指出：Network traffic classification, aiming to classify network traffic into distinct management groups, plays an indispensable role in network monitoring, QoS, and intrusion detection.

## 2. 摘要翻译
### 2.1 摘要原文
Network traffic classification, aiming to classify network traffic into distinct management groups, plays an indispensable role in network monitoring, QoS, and intrusion detection. The widespread of encryption techniques applied to networks has made accurate traffic classification increasingly challenging. In recent years, raw traffic data as input to deep learning models has been widely adopted due to its high classification accuracy and low reliance on human-engineered features. Yet, a critical challenge remains: different bytes within a packet carry varying levels of discriminative information, and no consensus exists on the optimal representation unit for model input. In this paper, deep analysis of encrypted network traffic data is conducted, and our studies show that as the input to deep learning models, (1) byte-level representation outperforms bit-level encoding; (2) unigram byte features surpass the other ’n’-gram variants (halfgram, bigram, and trigram); (3) packet header bytes are significantly more discriminative than payload bytes, especially in highly encrypted datasets; and (4) certain header fields exhibit higher informativeness. Based on these findings, we propose HF-Transformer, a lightweight, non-pretrained model that leverages optimal header fields for classification. Evaluated across six datasets, HF-Transformer achieves up to 6.04% higher F1-score than SOTA alternatives, demonstrating its efficacy for encrypted traffic classification.
### 2.2 摘要中文翻译
摘要具体指出，本文研究“HF-Transformer: A Non-Pretrained Encrypted Network Traffic Classification Model Based on Packet Header Fields”所针对的问题。方法上，摘要描述了：In recent years, raw traffic data as input to deep learning models has been widely adopted due to its high classification accuracy and low reliance on human-engineered features.。结果上，摘要报告：In recent years, raw traffic data as input to deep learning models has been widely adopted due to its high classification accuracy and low reliance on human-engineered features.。以上为基于摘要的忠实中文概括，英文术语和数值仍需对照 PDF 复核。

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

摘要所示核心思想：仅用包头字段的非预训练 Transformer 分类；具体模块、数据划分和数值结果以 §2.2 及正文为准。

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
- MinerU：[[2026-INFOCOM-HF-Transformer__A_Non-Pretrained_Encrypted_Network_Traffic_Classification_Model_Based_on_Packet_Header_Fields.md]]

## 12. 后续问题
- 需人工补录正文中的数据集、baseline、指标、结果和开源链接。

## 13. 抽取质量与证据核验
- MinerU 文本可能存在连字符断行、特殊符号替换、公式或表格结构丢失等问题；涉及方法细节、数值和专有名词的内容需回看 PDF。
- DOI、原文链接和代码字段已依据批次元数据及解析文本补入；未发现明确代码仓库时保留 `unknown`。
- 摘要翻译与一句话总结基于元数据摘要生成，仍需人工核对术语、缩写和上下文。

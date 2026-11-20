---
type: paper
title_original: "Ultimate Encrypted Traffic Feature Engineering: HTTPS Encrypted Traffic Classification Using Restored Application Data Unit Length"
title_cn: "使用复原应用数据单元长度的 HTTPS 流量分类"
authors: ["Zihan Chen", "Guang Cheng", "Dandan Niu", "Yuyu Zhao", "Yuyang Zhou", "Shanqing Jiang"]
year: 2026
venue: TDSC
doi: "10.1109/tdsc.2025.3615592"
url: "https://doi.org/10.1109/tdsc.2025.3615592"
pdf: "00-inbox/PDFs/2026-TDSC-Ultimate_Encrypted_Traffic_Feature_Engineering_HTTPS_Encrypted_Traffic_Classification_Using_Restored_Application_Data_Unit_Length.pdf"
mineru_md: "02-parsed-markdown/2026-TDSC-Ultimate_Encrypted_Traffic_Feature_Engineering_HTTPS_Encrypted_Traffic_Classification_Using_Restored_Application_Data_Unit_Length.md"
status: processed
reading_level: L2
research_area: ["加密流量分析"]
task: ["HTTPS 应用分类"]
method: ["ADU 长度复原与序列分类"]
dataset: ["CERNET 中两种真实网络场景"]
code: unknown
relevance: medium
created: "2026-09-29"
updated: "2026-11-20"
---

# Ultimate Encrypted Traffic Feature Engineering: HTTPS Encrypted Traffic Classification Using Restored Application Data Unit Length

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Ultimate Encrypted Traffic Feature Engineering: HTTPS Encrypted Traffic Classification Using Restored Application Data Unit Length |
| 年份 | 2026 |
| 会议/期刊 | TDSC |
| PDF | [[2026-TDSC-Ultimate_Encrypted_Traffic_Feature_Engineering_HTTPS_Encrypted_Traffic_Classification_Using_Restored_Application_Data_Unit_Length.pdf]] |
| MinerU Markdown | [[2026-TDSC-Ultimate_Encrypted_Traffic_Feature_Engineering_HTTPS_Encrypted_Traffic_Classification_Using_Restored_Application_Data_Unit_Length.md]] |
| 作者 | Zihan Chen, Guang Cheng, Dandan Niu, Yuyu Zhao, Yuyang Zhou, Shanqing Jiang |
| DOI | [10.1109/tdsc.2025.3615592](https://doi.org/10.1109/tdsc.2025.3615592) |

## 1. 一句话总结

用回归估计应用数据单元长度，再利用复原长度序列做 HTTPS 应用分类。

## 2. 摘要原文
—Over-the-top (OTT) applications mainly communicate through HTTPS, the most famous encryption protocol family on the Internet. The classification of HTTPS encrypted traffic can effectively obtain fine-grained OTT application information for network management and cyber security. As the most expressive feature, the side-channel length sequence is widely used by current research, especially the packet length sequence. However, these attempts ignored interferences from protocol piecewise decoupling and encryption covering, leading to poor performance. Based on the application layer feature engineering theory, we proposed a new metric called Application Data Unit (ADU) length to eliminate the interferences. However, ADU length cannot be obtained directly from packets as the TLS encryption protocol covers the entire application layer, which contains an intrusive and variable HTTP header. Hence, we designed a Length-Correction Multiple Regression Neural Network (LC-MRNN) algorithm to restore the real ADU length sequences accurately. Exhaustive experiments in two scenarios ofthe real CERNET network show that no matter the HTTP-1.1 or HTTP-2.0 protocol, the LC-MRNN model can achieve significantly accurate ADU length restoration. In classification, with the assistance of the LS-LSTM classifier, our method outperforms the state-of-the-art methods with about 4.2% improvement in F1-score (93.52%). Index Terms—Encrypted traffic classification, application layer feature engineering, application data unit, length-correction multiple regression neural network, HTTPS.

## 3. 方法分析

由可见长度观测估计 ADU 长度序列，使用 LC-MRNN 与 LS-LSTM 组织长度恢复和分类。

## 4. 实验表现

- 研究对象：CERNET 中两种真实网络场景。
- 作者报告：摘要在 CERNET 的 HTTP/1.1 与 HTTP/2.0 实验中报告 ADU 可较准确复原，分类 F1 为 93.52%。不同协议和原始包长对照须按正文分读。
- 原文位置：[[02-parsed-markdown/2026-TDSC-Ultimate_Encrypted_Traffic_Feature_Engineering_HTTPS_Encrypted_Traffic_Classification_Using_Restored_Application_Data_Unit_Length|原文解析稿]] · 摘要与原文长度复原和分类对照。

## 5. 局限性与复现建议

复原值是模型估计。作者验证范围是其 CERNET 场景及所测 HTTP/TLS 配置。

## 6. 知识链接
- [[traffic-classification]]
- [[encrypted-traffic-analysis]]

## 7. 证据状态

本页摘要区属于论文级记录。正文方法与结果已对照 [[02-parsed-markdown/2026-TDSC-Ultimate_Encrypted_Traffic_Feature_Engineering_HTTPS_Encrypted_Traffic_Classification_Using_Restored_Application_Data_Unit_Length|原文解析稿]] · 摘要与原文长度复原和分类对照。可引用的结论须保留所列实验条件。

### 并行深度分析（2026-09-29）
- 方法/问题：Ultimate replaces packet-length observations with application-data-unit (ADU) length and uses LC-MRNN to correct TLS-covered headers, aiming at more faithful HTTPS application classification. Missing: correction model details, datasets, baselines, ablations and exact gains.
- 证据边界：以上仅使用对应 MinerU 解析稿摘要及可稳定提取段落；未提取到的数值、数据集、代码和参数均不作推断。
- 复现建议：先核对原文表格、附录、代码仓库和数据划分，再确定 L3/L4 复现。

## 历史自动摘录

> 早期入库生成的字段和占位段落。现行记录见上文。

```markdown
title_cn: ""
research_area: []
task: []
method: []
dataset: []

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。


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


## 7. 证据状态
- MinerU：已完成；解析质量需人工抽查。
- Bib 元数据：待官方 API/论文首页核验。



## 深度分析（自动证据提取，需人工复核）

### 研究问题与证据
- 主题线索：website fingerprint, encrypted traffic, tor, graph neural, transformer, quic, traffic classification。
- 摘要证据：Index Terms—Encrypted traffic classification, application layer feature engineering, application data unit, length-correction multiple regression neural network, HTTPS.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：未检测到明确 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


```

---
type: paper
title_original: "GAN-based Tor obfuscated traffic identification on imbalanced datasets"
title_cn: "面向不平衡数据的 GAN 匿名 Tor 混淆流量识别"
authors: ["Tianbo Lu", "Pengfei Zhao", "Yingjie Cai", "Subatjan Abdulla", "Hanrui Chen"]
year: 2027
venue: "Computers & Security"
doi: "10.1016/j.cose.2026.105167"
url: "https://www.sciencedirect.com/science/article/pii/S0167404826003433"
pdf: "00-inbox/PDFs/2026-JCS-GAN-based_Tor_obfuscated_traffic_identification_on_imbalanced_datasets.pdf"
mineru_md: "02-parsed-markdown/2026-JCS-GAN-based_Tor_obfuscated_traffic_identification_on_imbalanced_datasets.md"
status: processed
reading_level: L2
research_area: ["匿名流量分析"]
task: ["Tor 混淆流量分类"]
method: ["半监督 GAN 与同骨干消融"]
dataset: ["作者采集的 Tor、非 Tor 和五种混淆传输"]
code: unknown
relevance: medium
created: "2026-09-29"
updated: "2026-11-20"
volume: "172"
pages: "105167"
preprint_doi: "10.2139/ssrn.6709728"
---

# GAN-based Tor obfuscated traffic identification on imbalanced datasets

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | GAN-based Tor obfuscated traffic identification on imbalanced datasets |
| 年份 | 2027 |
| 会议/期刊 | Computers & Security |
| PDF | [[2026-JCS-GAN-based_Tor_obfuscated_traffic_identification_on_imbalanced_datasets.pdf]] |
| MinerU Markdown | [[2026-JCS-GAN-based_Tor_obfuscated_traffic_identification_on_imbalanced_datasets.md]] |
| 作者 | Tianbo Lu, Pengfei Zhao, Yingjie Cai, Subatjan Abdulla, Hanrui Chen |
| DOI | [10.1016/j.cose.2026.105167](https://doi.org/10.1016/j.cose.2026.105167) |
| 预印本标识 | 10.2139/ssrn.6709728 |

## 1. 一句话总结

作者在控制类别不均衡的条件下评估少数类特征增强对 Tor 流量识别的贡献。

## 2. 摘要原文
ing relevant features. The framework was evaluated on five datasets across five different traffic fingerprinting tasks, including website fingerprinting on Shadowsocks-obfuscated traffic, and achieved results comparable to or even better than state-of-the-art methods. Al-E’mari et al. (2023) proposed a GAN-based approach for detecting obfuscated Tor traffic by combining bidirectional generative adversarial learning with a vision-transform-style representation. Their work demonstrates the usefulness of adversarial representation learning for obfuscated Tor detection. In contrast, our work focuses on PT-level multi-class identification under class imbalance. Rather than primarily converting traffic into visual representations, our discriminator models the packet-flow-trace hierarchy with CNN and recurrent modules, while the generator performs class-conditioned feature-space augmentation for minority classes. GAN-based Traffic Obfuscation: Several studies focus on reinforcement of obfuscation proxy technologies using adversarial approaches. Sheffey and Aderholdt (2019) trained a GAN network to minimally modify statistical signatures of Tor traffic in a way that hinders classification. Zou et al. (2023) employed Temporal Convolu tional Networks (TCNs) to construct a GAN that learns traffic features to achieve effective mimicry of target traffic. Although there is a wealth of studies on PT improvement, research on GAN-based obfuscated traffic identification is limited. GAN-based Semi-supervised Learning: Ever since the inception of Generative Adversarial Networks (GANs) (Goodfellow et al., 2020), there has been a continuous effort to improve their performance and architecture. Specifically, a number of papers focus on modifying GANs for unsupervised or semi-supervised learning. Springenberg (2015) proposed catGAN to learn a discriminative classifier from unlabeled or partially labeled data. Radford et al. (2015) introduced DCGAN for unsupervised tasks, employing Convolutional Neural Networks (CNNs) for both the generator and discriminator. Salimans et al. (2016) developed an effective semi-supervised learning model based on some of these techniques.

## 3. 方法分析

在作者数据上用半监督模型区分流量类别，以同骨干对照隔离生成器是否参与。

## 4. 实验表现

- 研究对象：作者采集的 Tor、非 Tor 和五种混淆传输。
- 作者报告：论文摘要称近似均衡场景表现具竞争力，同骨干消融在指定不平衡设置中提高 Tor 类召回和 F1 的点估计。
- 原文位置：[[02-parsed-markdown/2026-JCS-GAN-based_Tor_obfuscated_traffic_identification_on_imbalanced_datasets|原文解析稿]] · 本地论文摘要与同骨干消融。

## 5. 局限性与复现建议

结论依赖采集、类比和混淆传输范围。另有 SSRN 预印本与正式卷期，引用时按所用版本定位。

## 6. 知识链接
- [[traffic-classification]]
- [[encrypted-traffic-analysis]]

## 7. 证据状态

本页摘要区属于论文级记录。正文方法与结果已对照 [[02-parsed-markdown/2026-JCS-GAN-based_Tor_obfuscated_traffic_identification_on_imbalanced_datasets|原文解析稿]] · 本地论文摘要与同骨干消融。可引用的结论须保留所列实验条件。

## 深度分析（2026-09-29）

- reading_level: L3
- 研究定位：Tor混淆流量/类别不平衡
- 方法机制：以GAN生成或增强少数类样本，面向类别不平衡下的Tor obfuscated traffic identification；需结合正文确认生成器、判别器、特征表示和分类器耦合方式。
- 输入—处理—输出：输入Tor加密/混淆流量特征；GAN增强训练分布，输出流量类别预测。
- 证据边界：当前摘要抽取不足，具体数据集、指标、提升幅度、消融和代码均待核验，不据此形成定量claim。
- 联动标签：website-fingerprinting；DNS；anomaly-detection；traffic-security

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
- 主题线索：website fingerprint, encrypted traffic, dns, tor, adversarial, covert, quic, traffic classification。
- 摘要证据：MinerU 未稳定提取摘要，不能据此补写贡献。

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

---
type: paper
title_original: "Robust and Reliable Early-Stage Website Fingerprinting Attacks via Spatial-Temporal Distribution Analysis"
title_cn: "基于时空分布分析的鲁棒可靠早期网站指纹攻击"
authors:
  - Xinhao Deng
  - Qi Li
  - Ke Xu
year: 2024
venue: "CCS"
doi: "10.1145/3658644.3670272"
url: ""
pdf: "00-inbox/PDFs/2024-CCS-Robust_and_reliable_early-stage_website_fingerprinting_attacks_via_spatial-temporal_distribution_analysis.pdf"
mineru_md: "02-parsed-markdown/2024-CCS-Robust_and_reliable_early-stage_website_fingerprinting_attacks_via_spatial-temporal_distribution_analysis.md"
status: processed
reading_level: L2
research_area:
  - website-fingerprinting
  - traffic-classification
  - privacy-attack
task:
  - website-fingerprinting
  - early-stage-traffic-identification
  - dark-web-detection
method:
  - supervised-contrastive-learning
  - adaptive-data-augmentation
  - spatial-temporal-distribution-analysis
  - feature-attribution
  - SHAP
dataset:
  - Alexa-top-10k
  - dark-web-80
  - WTF-PAD
  - Walkie-Talkie
  - FRONT
  - RegulaTor
code: "https://github.com/HolmesWF/Holmes"
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

# Holmes: 基于时空分布分析的鲁棒可靠早期网站指纹攻击

## 0. 基础信息

| 字段 | 内容 |
|------|------|
| 论文全称 | Robust and Reliable Early-Stage Website Fingerprinting Attacks via Spatial-Temporal Distribution Analysis |
| 作者 | Xinhao Deng, Qi Li, Ke Xu |
| 机构 | 清华大学 INSC & BNRist; 中关村实验室 |
| 发表年份 | 2024 |
| 会议/期刊 | CCS 2024 |
| 关键词 | Tor, Website Fingerprinting, Spatial-Temporal Analysis, Contrastive Learning, Early-Stage Attack |
| 代码 | https://github.com/HolmesWF/Holmes |

## 1. 一句话总结

提出 Holmes，一种基于时空分布分析和监督对比学习的早期网站指纹攻击方法，能够在页面加载仅完成约 21.71% 时即可准确识别 Tor 用户访问的网站，F1-score 相比现有 DL-based WF 攻击平均提升 169.18%，且在多种防御机制下保持鲁棒性。

## 2. 摘要翻译

**原文：**
Website Fingerprinting (WF) attacks identify the websites visited by users by performing traffic analysis, compromising user privacy. Particularly, DL-based WF attacks demonstrate impressive attack performance. However, the effectiveness of DL-based WF attacks relies on the collected complete and pure traffic during the page loading, which impacts the practicality of these attacks. The WF performance is rather low under dynamic network conditions and various WF defenses, particularly when the analyzed traffic is only a small part of the complete traffic. In this paper, we propose Holmes, a robust and reliable early-stage WF attack. Holmes utilizes temporal and spatial distribution analysis of website traffic to effectively identify websites in the early stages of page loading. Specifically, Holmes develops adaptive data augmentation based on the temporal distribution of website traffic and utilizes a supervised contrastive learning method to extract the correlations between the early-stage traffic and the pre-collected complete traffic. Holmes accurately identifies traffic in the early stages of page loading by computing the correlation of the traffic with the spatial distribution information, which ensures robust and reliable detection according to early-stage traffic. We extensively evaluate Holmes using six datasets. Compared to nine existing DL-based WF attacks, Holmes improves the F1-score of identifying early-stage traffic by an average of 169.18%. Furthermore, we replay the traffic of visiting real-world dark web websites. Holmes successfully identifies dark web websites when the ratio of page loading on average is only 21.71%, with an average precision improvement of 169.36% over the existing WF attacks.

**中文翻译：**
网站指纹（WF）攻击通过流量分析识别用户访问的网站，危害用户隐私。特别是基于深度学习的 WF 攻击展示了出色的攻击性能。然而，DL-based WF 攻击的有效性依赖于页面加载期间收集的完整且纯净的流量，这影响了这些攻击的实际可用性。在动态网络条件和各种 WF 防御下，WF 性能相当低，特别是当分析的流量仅是完整流量的一小部分时。本文提出 Holmes，一种鲁棒可靠的早期 WF 攻击。Holmes 利用网站流量的时空分布分析，在页面加载早期阶段有效地识别网站。具体而言，Holmes 基于网站流量的时间分布开发自适应数据增强，并利用监督对比学习方法提取早期阶段流量与预收集完整流量之间的相关性。Holmes 通过计算流量与空间分布信息的相关性，准确识别页面加载早期阶段的流量，确保基于早期阶段流量的鲁棒可靠检测。我们在六个数据集上广泛评估了 Holmes。与九种现有 DL-based WF 攻击相比，Holmes 在识别早期阶段流量的 F1-score 上平均提升 169.18%。此外，我们重放了访问真实暗网网站的流量。Holmes 在页面加载比例平均仅为 21.71% 时成功识别暗网网站，平均精度提升 169.36%。

## 3. 方法动机（Motivation）

### 3.1 问题背景与痛点

- **Tor 隐私保护的脆弱性**：Tor 是最流行的匿名通信系统，但容易受到 WF 攻击，现有 DL-based WF 攻击准确率超过 95%
- **完整流量收集的不现实性**：现有 WF 攻击依赖页面加载期间收集的完整且纯净的流量，但在实际场景中：
  - 不同网站页面加载时间和数据包数量差异巨大（5.04% 的网站加载时间超过 120 秒或数据包超过 5000）
  - 动态网络条件（不同路径、带宽、延迟）导致同一网站的流量模式变化
  - WF 防御（填充虚假包、延迟包、分裂流量）严重影响攻击效果
  - 现有攻击（如 DF）在某些网站上最低精度仅 54.11%
- **早期流量识别的挑战**：
  - 早期阶段流量包含的网站信息更少，在动态网络条件下更容易误识别
  - 防御机制对早期阶段流量的影响更大
  - 不同网站的页面加载速度差异大，难以统一设置

### 3.2 核心直觉

- **时空分布相关性**：同一网站的早期阶段流量和完整流量之间存在强烈的时空分布相关性，因为它们包含相同的网站信息（如网站内容和元素的部分）
- **时间分布**：通过特征归因方法（SHAP）分析网站流量的时间分布，发现所有网站的早期阶段流量与完整流量共享相似且充足的网站信息
- **空间分布**：在嵌入空间中，同一网站的流量点聚集在一起，可以通过计算未知流量与各网站的相关性进行识别

## 4. 方法设计（Method Design）

### 4.1 整体流程

```
早期阶段流量 → 自适应数据增强 → 监督对比学习 → 空间分布分析 → 网站识别
                (时间分布)        (嵌入空间)      (相关性计算)    (置信度判断)
```

### 4.2 三大模块

**模块一：自适应数据增强（Adaptive Data Augmentation）**
- **输入**：完整流量数据
- **处理**：
  - 使用 SHAP 特征归因方法分析每个网站流量的时间分布
  - 聚合同一网站的多个流量的特征归因结果，得到特征重要性分布
  - 根据网站独特的时间分布，对不同网站的流量应用不同长度的尾部掩码
- **输出**：生成包含充足网站信息的早期阶段流量
- **关键点**：为每个网站自适应地生成早期阶段流量，而不是使用固定设置

**模块二：空间分布分析（Spatial Distribution Analysis）**
- **输入**：早期阶段流量和完整流量
- **处理**：
  - 使用监督对比学习（SCL）将流量特征转换到低维嵌入空间
  - 通过聚合同一网站的早期阶段和完整流量的点，提取它们之间的相关性
  - 在嵌入空间中，每个流量对应一个点
- **输出**：学习到的嵌入空间，同一网站的流量点聚集在一起

**模块三：早期网站识别（Early-Stage Website Identification）**
- **输入**：未知的早期阶段流量
- **处理**：
  - 将未知流量投影到嵌入空间
  - 基于网站流量的空间分布，计算其与每个网站的相关性
  - 对于与所有网站相关性都较低的结果进行拒绝（避免误识别）
- **输出**：识别结果或拒绝（继续收集更多数据包）
- **关键点**：在每个短时间间隔进行攻击，直到网站被高置信度识别

### 4.3 关键公式

- 特征归因：使用 SHAP 值量化每个时间步的特征重要性
- 对比学习损失：监督对比学习损失函数，拉近同一网站的流量，推远不同网站的流量
- 相关性计算：基于嵌入空间中的距离计算流量与网站的相关性

### 4.4 优缺点

**优势：**
- 首个鲁棒可靠的早期阶段 WF 攻击
- 自适应数据增强：根据网站独特的时间分布生成早期阶段流量
- 监督对比学习：有效提取早期阶段和完整流量之间的相关性
- 空间分布分析：准确识别早期阶段流量
- 拒绝机制：避免低置信度的误识别

**局限：**
- 仍需预收集完整流量作为参考
- 在极端防御下性能可能下降
- 依赖于早期阶段流量与完整流量的相关性假设

## 5. 与其他方法对比（Comparison）

### 5.1 创新点

| 创新点 | 本文方法 | 现有方法 |
|--------|----------|----------|
| 攻击时机 | 早期阶段（页面加载部分完成） | 完整页面加载后 |
| 数据增强 | 自适应（基于网站时间分布） | 固定设置 |
| 特征学习 | 监督对比学习（时空分布） | 传统分类学习 |
| 流量收集 | 自适应（动态停止） | 固定时间/数据包数 |
| 鲁棒性 | 多种防御下保持性能 | 防御下性能大幅下降 |

### 5.2 与 Baseline 对比

与 9 种现有 DL-based WF 攻击对比：
- DF（Deep Fingerprint）
- ARES（多标签攻击）
- Tik-Tok
- TF（Triplet Fingerprint）
- 等其他方法

**关键差异**：
- 现有方法依赖完整流量，Holmes 仅需早期阶段流量
- 现有方法在动态网络条件下性能下降严重，Holmes 保持鲁棒
- Holmes 在页面加载早期即可识别，而现有方法需等待加载完成

## 6. 实验表现（Experiments）

### 6.1 数据集

| 数据集 | 描述 | 规模 |
|--------|------|------|
| Alexa-top | Alexa-top 10k 网站 | 10,000 网站 |
| Dark Web | 暗网网站（Tor onion services） | 80 网站 |
| WTF-PAD 防御数据集 | 轻量级填充防御 | - |
| Walkie-Talkie 防御数据集 | 流量分裂防御 | - |
| FRONT 防御数据集 | 前台流量防御 | - |
| RegulaTor 防御数据集 | 规则化防御 | - |

### 6.2 Baseline 方法

- DF（Deep Fingerprint）
- ARES（多标签攻击）
- Tik-Tok
- TF（Triplet Fingerprint）
- NetCLR
- 等其他 9 种 DL-based WF 攻击

### 6.3 评估指标

- F1-score
- Precision
- Recall
- Page Loading Ratio（页面加载比例）

### 6.4 关键结果

**早期阶段流量识别：**
- F1-score 平均提升 169.18%（与 9 种现有方法对比）
- 在页面加载比例平均为 21.71% 时即可成功识别

**暗网网站识别：**
- 80 个真实暗网网站，精度达 85.19%
- 平均页面加载比例仅 21.71%
- 精度平均提升 169.36%

**防御鲁棒性：**
- 在 WTF-PAD、Walkie-Talkie、FRONT、RegulaTor 等防御下保持高性能
- 现有方法在防御下性能大幅下降，Holmes 保持稳定

**自适应流量收集：**
- Holmes 自动停止流量收集当获得足够网站信息
- 不同网站的收集时间不同，适应性强

## 7. 学习与应用（Learning & Application）

### 7.1 开源情况

- **代码**：https://github.com/HolmesWF/Holmes
- **可复现性**：作者提供了完整的代码和数据集

### 7.2 可迁移价值

- **早期流量分析**：可应用于其他需要早期识别的场景（如实时监控）
- **对比学习**：监督对比学习方法可迁移至其他流量分类任务
- **自适应数据增强**：基于特征分布的自适应增强方法可应用于其他领域
- **时空分布分析**：时空特征提取方法可应用于其他序列数据分析

### 7.3 实际应用场景

- **暗网犯罪检测**：在页面加载早期即可识别暗网网站，支持实时监控
- **Tor 流量分析**：对 Tor 匿名通信的流量分析
- **隐私保护评估**：评估 WF 防御的有效性

## 8. 总结（Summary）

### 8.1 核心思想

Holmes 的核心思想是利用同一网站早期阶段流量与完整流量之间的时空分布相关性，通过监督对比学习在嵌入空间中提取这种相关性，实现早期阶段的网站识别。自适应数据增强确保早期阶段流量包含充足网站信息，空间分布分析实现准确识别，拒绝机制避免误识别。

### 8.2 快速流程图

```
输入：早期阶段流量（页面加载部分完成）
  ↓
自适应数据增强（基于网站时间分布）
  ↓
监督对比学习（提取时空分布相关性）
  ↓
空间分布分析（计算与各网站的相关性）
  ↓
置信度判断（高置信度识别 or 拒绝继续收集）
  ↓
输出：识别的网站 or 继续收集更多流量
```

## 9. 知识链接（Knowledge Links）

- [[website-fingerprinting]]：本文的核心任务，通过流量分析识别用户访问的网站
- [[traffic-classification]]：更广泛的任务类别，网站指纹是其子任务
- [[contrastive-learning]]：本文采用监督对比学习方法提取流量相关性
- [[encrypted-traffic-analysis]]：加密流量分析的背景，WF 是其重要应用
- [[transformer]]：虽然本文未使用 Transformer，但对比学习方法在 Transformer 中有广泛应用

## 10. 证据记录（Evidence）

| 声明 | 证据 | 来源 |
|------|------|------|
| Holmes F1-score 平均提升 169.18% | 与 9 种现有 DL-based WF 攻击对比 | 论文 §6 实验结果 |
| 暗网识别精度 85.19% | 80 个真实暗网网站，页面加载比例 21.71% | 论文 §6 实验结果 |
| 页面加载比例 21.71% 即可识别 | 真实暗网流量重放实验 | 论文 §6 实验结果 |
| 5.04% 网站加载时间超过 120 秒 | Alexa-top 10k 网站分析 | 论文 §2.2 |
| 现有方法最低精度仅 54.11% | DF 攻击在某些网站上的精度 | 论文 §2.2 |

## 11. 原始资料链接（Source Links）

- **PDF**：`00-inbox/PDFs/2024-CCS-Robust_and_reliable_early-stage_website_fingerprinting_attacks_via_spatial-temporal_distribution_analysis.pdf`
- **MinerU MD**：`02-parsed-markdown/2024-CCS-Robust_and_reliable_early-stage_website_fingerprinting_attacks_via_spatial-temporal_distribution_analysis.md`

## 12. 后续问题（Open Questions）

1. **极端防御场景**：在更激进的 WF 防御下，Holmes 的性能如何？是否存在防御可以完全规避 Holmes？
2. **开放世界扩展**：在完全开放的世界场景中（未知网站数量极多），Holmes 的可扩展性如何？
3. **多标签浏览**：在多标签同时浏览的场景下，早期阶段流量的识别准确性如何？
4. **实时部署**：Holmes 的计算复杂度和延迟是否满足实时部署需求？
5. **隐私防御设计**：基于 Holmes 的发现，如何设计更有效的 WF 防御机制？

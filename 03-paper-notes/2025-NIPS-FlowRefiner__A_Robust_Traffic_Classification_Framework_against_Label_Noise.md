---
type: paper
title_original: "FlowRefiner: A Robust Traffic Classification Framework against Label Noise"
title_cn: "FlowRefiner: 一种抗标签噪声的鲁棒流量分类框架"
authors:
  - Mingwei Zhan
  - Ruijie Zhao
  - Xianwen Deng
  - Zhi Xue
  - Qi Li
  - Zhuotao Liu
  - Guang Cheng
  - Ke Xu
year: 2025
venue: "NeurIPS"
doi: ""
url: ""
pdf: "00-inbox/PDFs/2025-NIPS-FlowRefiner__A_Robust_Traffic_Classification_Framework_against_Label_Noise.pdf"
mineru_md: "02-parsed-markdown/2025-NIPS-FlowRefiner__A_Robust_Traffic_Classification_Framework_against_Label_Noise.md"
status: processed
reading_level: L2
research_area:
  - traffic-classification
  - robust-machine-learning
  - label-noise
task:
  - traffic-classification
  - label-noise-detection
  - label-correction
method:
  - pre-training
  - MAE
  - Transformer
  - K-means-clustering
  - confidence-guided-correction
  - cross-granularity-classification
dataset:
  - ISCXVPN
  - CrossPlatform
  - USTC-TFC
  - Malware
code: "https://github.com/NSSL-SJTU/FlowRefiner"
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

# FlowRefiner: 抗标签噪声的鲁棒流量分类框架

## 0. 基础信息

| 字段 | 内容 |
|------|------|
| 论文全称 | FlowRefiner: A Robust Traffic Classification Framework against Label Noise |
| 作者 | Mingwei Zhan, Ruijie Zhao, Xianwen Deng, Zhi Xue, Qi Li, Zhuotao Liu, Guang Cheng, Ke Xu |
| 机构 | 上海交通大学; 东南大学; 清华大学 |
| 发表年份 | 2025 |
| 会议/期刊 | NeurIPS 2025 |
| 关键词 | Traffic Classification, Label Noise, Pre-training, Transformer, Robust Learning |
| 代码 | https://github.com/NSSL-SJTU/FlowRefiner |

## 1. 一句话总结

提出 FlowRefiner，一种抗标签噪声的鲁棒通用流量分类框架，通过流量语义驱动的噪声检测器、置信度引导的标签校正机制和跨粒度鲁棒分类器，在 4 个数据集上即使 60% 噪声率下仍保持 70%+ 准确率和 F1-score，显著优于所有 baseline 方法。

## 2. 摘要翻译

**原文：**
Network traffic classification is essential for network management and security. In recent years, deep learning (DL) algorithms have emerged as essential tools for classifying complex traffic. However, they rely heavily on high-quality labeled training data. In practice, traffic data is often noisy due to human error or inaccurate automated labeling, which could render classification unreliable and lead to severe consequences. Although some studies have alleviated the label noise issue in specific scenarios, they are difficult to generalize to general traffic classification tasks due to the inherent semantic complexity of traffic data. In this paper, we propose FLOWREFINER, a robust and general traffic classification framework against label noise. FLOWREFINER consists of three core components: a traffic semantics-driven noise detector, a confidence-guided label correction mechanism, and a cross-granularity robust classifier. First, the noise detector utilizes traffic semantics extracted from a pre-trained encoder to identify mislabeled flows. Next, the confidence-guided label correction module fine-tunes a label predictor to correct noisy labels and construct refined flows. Finally, the cross-granularity robust classifier learns generalized patterns of both flow-level and packet-level, improving classification robustness against noisy labels. We evaluate our method on four traffic datasets with various classification scenarios across varying noise ratios. Experimental results demonstrate that FLOWREFINER mitigates the impact of label noise and consistently outperforms state-of-the-art baselines by a large margin. The code is available at https://github.com/NSSL-SJTU/FlowRefiner.

**中文翻译：**
网络流量分类对网络管理和安全至关重要。近年来，深度学习算法已成为分类复杂流量的重要工具。然而，它们高度依赖高质量的标记训练数据。在实践中，流量数据通常由于人为错误或不准确的自动标记而含有噪声，这可能导致分类不可靠并导致严重后果。尽管一些研究在特定场景中缓解了标签噪声问题，但由于流量数据固有的语义复杂性，它们难以泛化到通用流量分类任务。本文提出 FlowRefiner，一种抗标签噪声的鲁棒通用流量分类框架。FlowRefiner 包含三个核心组件：流量语义驱动的噪声检测器、置信度引导的标签校正机制和跨粒度鲁棒分类器。首先，噪声检测器利用从预训练编码器提取的流量语义来识别错误标记的流。接下来，置信度引导的标签校正模块微调标签预测器以校正噪声标签并构建精炼流。最后，跨粒度鲁棒分类器学习流级和包级的泛化模式，提高对噪声标签的分类鲁棒性。我们在四个流量数据集上评估方法，涵盖不同噪声比率下的各种分类场景。实验结果表明，FlowRefiner 缓解了标签噪声的影响，并始终大幅优于最先进的基线方法。

## 3. 方法动机（Motivation）

### 3.1 问题背景与痛点

- **标签噪声的普遍性**：流量数据标签常因人为错误或自动标记不准确而含有噪声
- **DL 模型的脆弱性**：高容量 DL 模型容易过拟合错误标签，性能严重下降
- **现有方法的局限**：
  - 仅针对恶意流量（二分类），不适用于通用分类
  - 依赖良性-恶意可分性假设，在多样化场景中不成立
  - 计算机视觉领域的标签噪声方法难以迁移到流量数据（结构复杂、语义模糊）
- **流量数据的特殊性**：
  - 结构化数据，插值增强可能无意义
  - 同类流量可能形成多个紧凑簇
  - 不同类流量可能语义相似

### 3.2 核心直觉

- **流量语义**：预训练编码器提取的流量语义可以反映流的内容和功能相似性
- **噪声检测**：相似语义但标签不一致的流很可能是噪声
- **跨粒度学习**：流级和包级的联合学习可以捕获泛化模式，避免记忆噪声

## 4. 方法设计（Method Design）

### 4.1 整体流程

```
原始流量 → 预训练编码器 → 流量语义提取 → 噪声检测 → 标签校正 → 跨粒度分类
            (MAE)         (Transformer)    (K-means)    (置信度)    (流级+包级)
```

### 4.2 三大组件

**组件一：流量语义驱动的噪声检测器（Traffic Semantics-driven Noise Detector）**
- **输入**：原始流量数据
- **处理**：
  - 使用 MAE（Masked Autoencoder）风格的预训练范式训练编码器
  - Transformer 架构作为骨干网络
  - 随机掩码输入并重建缺失部分，学习流量语义
  - 提取 d 维特征向量
  - K-means 细粒度聚类（K = n × C，C 为类别数）
  - 定义每个簇的多数标签
  - 标签不在多数标签中的流被视为噪声
- **输出**：干净流集和噪声流集
- **关键点**：预训练编码器对噪声标签免疫

**组件二：置信度引导的标签校正（Confidence-Guided Label Correction）**
- **输入**：干净流集和噪声流集
- **处理**：
  - 在干净流上微调标签预测器（预训练编码器 + 分类头）
  - 计算噪声流的预测置信度分数
  - **高置信度流（p_i >= τ_h）**：用预测标签替换原始标签
  - **低置信度流（p_i <= τ_l）**：保留原始标签以维持多样性
  - 合并干净流和校正后的噪声流，形成精炼流
- **输出**：精炼流集
- **关键点**：保留语义多样性，避免过度校正

**组件三：跨粒度鲁棒分类器（Cross-Granularity Robust Classifier）**
- **输入**：精炼流集
- **处理**：
  - 共享权重的编码器和分类头
  - 流级分类：输入完整流，预测标签
  - 包级分类：随机选择一个数据包，预测标签
  - 两个任务联合训练
  - 随机包选择引入多样性，避免记忆特定噪声流
- **输出**：鲁棒分类器
- **关键点**：流级和包级的联合学习捕获泛化模式

### 4.3 关键公式

- **K-means 聚类**：$\min_{\mu_k} \sum_{i=1}^{N} \sum_{k=1}^{K} \mathbb{1}(z_i \in C_k) \|z_i - \mu_k\|^2$
- **多数标签**：每个簇中 top m 最频繁的标签
- **标签校正**：$\mathcal{D}_{\text{refined}} = \mathcal{D}_{\text{clean}} \cup \{(x_i, \hat{y}_i) | p_i > \tau_h\} \cup \{(x_i, y_i) | p_i < \tau_l\}$
- **包选择**：$x_i^p = \text{RandomSelect}(\{pac_i^1, pac_i^2, \dots | x_i\})$

### 4.4 优缺点

**优势：**
- 首个针对通用流量分类任务的抗标签噪声框架
- 流量语义驱动的噪声检测对噪声免疫
- 置信度引导的标签校正保留语义多样性
- 跨粒度分类捕获泛化模式，避免记忆噪声
- 在极高噪声率（60%）下仍保持性能

**局限：**
- 预训练需要大量无标签数据
- K-means 聚类参数需要调整
- 在极低噪声率下可能不如专用方法

## 5. 与其他方法对比（Comparison）

### 5.1 创新点

| 创新点 | 本文方法 | 现有方法 |
|--------|----------|----------|
| 任务范围 | 通用流量分类 | 仅恶意流量 |
| 噪声检测 | 流量语义驱动 | 损失值分布 |
| 标签校正 | 置信度引导 | 固定阈值 |
| 分类器 | 跨粒度（流+包） | 单粒度 |
| 噪声容忍 | 60% | 通常 < 40% |

### 5.2 与 Baseline 对比

**流量分类 Baseline：**
- Appscanner, FS-Net（传统方法）
- ET-BERT, MAE, YaTC（预训练方法）
- MCRe（恶意流量标签噪声方法）

**标签噪声学习 Baseline：**
- CE, LSR, Mixup, GCE, SCE, Co-teaching, DivideMix

**关键差异**：
- 现有方法在高噪声率下性能大幅下降，FlowRefiner 保持稳定
- MCRe 仅适用于恶意流量，FlowRefiner 通用
- 计算机视觉方法难以迁移到流量数据

## 6. 实验表现（Experiments）

### 6.1 数据集

| 数据集 | 描述 | 场景 |
|--------|------|------|
| ISCXVPN | VPN 流量分类 | 应用识别 |
| CrossPlatform | 跨平台流量分类 | 应用识别 |
| USTC-TFC | 流量分类 | 恶意流量检测 |
| Malware | 恶意软件流量 | 恶意流量检测 |

**噪声设置**：5%, 10%, 20%, 40%, 60%

### 6.2 Baseline 方法

- 6 个流量分类方法
- 3 个包分类方法
- 6 个通用标签噪声学习方法

### 6.3 评估指标

- Accuracy
- F1-score
- 不同噪声率下的性能

### 6.4 关键结果

**流量分类 Baseline 对比：**
- 在所有数据集和噪声率下均优于所有 baseline
- 60% 噪声率下仍保持 70%+ 准确率和 F1-score
- ISCXVPN 5% 噪声：F1 = 93.34%（vs 最佳 baseline 92.35%）
- ISCXVPN 60% 噪声：F1 = 72.90%（vs 最佳 baseline 70.55%）

**标签噪声学习 Baseline 对比：**
- 大幅领先所有通用标签噪声方法
- 在 60% 噪声率下优势更明显

**类依赖噪声场景：**
- ISCXVPN：F1 = 80.97%（vs 最佳 baseline 77.01%）
- USTC-TFC：F1 = 88.40%（vs 最佳 baseline 86.01%）

**包级分类：**
- 优于高级包分类器
- 展示跨粒度分类的灵活性

## 7. 学习与应用（Learning & Application）

### 7.1 开源情况

- **代码**：https://github.com/NSSL-SJTU/FlowRefiner
- **可复现性**：提供了完整的代码和详细的超参数设置

### 7.2 可迁移价值

- **预训练方法**：MAE 风格的流量预训练方法可应用于其他流量分析任务
- **噪声检测**：流量语义驱动的噪声检测方法可应用于其他低质量数据场景
- **标签校正**：置信度引导的标签校正方法可应用于其他领域
- **跨粒度学习**：流级和包级的联合学习方法可应用于其他结构化数据分析

### 7.3 实际应用场景

- **网络流量分类**：在标签质量差的真实环境中部署分类系统
- **恶意流量检测**：在自动标记不可靠的场景中检测恶意流量
- **数据质量改进**：识别和校正错误标签，提高数据质量

## 8. 总结（Summary）

### 8.1 核心思想

FlowRefiner 的核心思想是利用预训练编码器提取的流量语义检测噪声标签，通过置信度引导的标签校正构建精炼流，使用跨粒度鲁棒分类器学习泛化模式。流量语义对噪声标签免疫，置信度校正保留语义多样性，跨粒度学习避免记忆噪声。

### 8.2 快速流程图

```
输入：带噪声标签的流量数据
  ↓
预训练编码器（MAE + Transformer）
  ↓
流量语义提取（d 维特征向量）
  ↓
噪声检测（K-means 细粒度聚类 + 多数标签）
  ↓
标签校正（置信度引导：高置信替换 + 低置信保留）
  ↓
跨粒度分类（流级 + 包级联合训练）
  ↓
输出：鲁棒流量分类器
```

## 9. 知识链接（Knowledge Links）

- [[traffic-classification]]：本文的核心任务
- [[pre-training-finetuning]]：MAE 预训练方法
- [[self-supervised-learning]]：MAE 的自监督学习范式
- [[transformer]]：编码器架构
- [[encrypted-traffic-analysis]]：加密流量分析的背景

## 10. 证据记录（Evidence）

| 声明 | 证据 | 来源 |
|------|------|------|
| 60% 噪声率下保持 70%+ | 4 个数据集，5 个噪声率 | 论文 §4 实验结果 |
| 大幅优于所有 baseline | 流量分类 + 标签噪声 baseline | 论文 §4 实验结果 |
| 首个通用流量分类抗噪声框架 | 作者声明 | 论文 §1 |
| 预训练编码器对噪声免疫 | MAE 无监督训练 | 论文 §3.1 |
| 跨粒度学习避免记忆噪声 | 流级+包级联合训练 | 论文 §3.3 |

## 11. 原始资料链接（Source Links）

- **PDF**：`00-inbox/PDFs/2025-NIPS-FlowRefiner__A_Robust_Traffic_Classification_Framework_against_Label_Noise.pdf`
- **MinerU MD**：`02-parsed-markdown/2025-NIPS-FlowRefiner__A_Robust_Traffic_Classification_Framework_against_Label_Noise.md`

## 12. 后续问题（Open Questions）

1. **极低噪声率**：在噪声率 < 5% 时，FlowRefiner 是否引入不必要的开销？
2. **预训练数据**：预训练数据的质量和规模对性能的影响如何？
3. **动态噪声**：噪声率随时间变化时，框架的适应能力如何？
4. **多标签分类**：在多标签分类场景下，框架的扩展性如何？
5. **实时应用**：框架的推理延迟是否满足实时分类需求？

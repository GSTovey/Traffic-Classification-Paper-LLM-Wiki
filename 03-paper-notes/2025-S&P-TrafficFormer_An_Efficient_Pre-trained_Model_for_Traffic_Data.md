---
type: paper
title_original: "TrafficFormer: An Efficient Pre-trained Model for Traffic Data"
title_cn: "TrafficFormer: 一种高效的流量数据预训练模型"
authors:
  - Guangmeng Zhou
  - Xiongwen Guo
  - Zhuotao Liu
  - Tong Li
  - Qi Li
  - Ke Xu
year: 2025
venue: "S&P"
doi: ""
url: ""
pdf: "00-inbox/PDFs/2025-S&P-TrafficFormer_An_Efficient_Pre-trained_Model_for_Traffic_Data.pdf"
mineru_md: "02-parsed-markdown/2025-S&P-TrafficFormer_An_Efficient_Pre-trained_Model_for_Traffic_Data.md"
status: processed
reading_level: L2
research_area:
  - traffic-representation-learning
  - pre-training
  - traffic-foundation-model
task:
  - traffic-classification
  - protocol-understanding
  - malware-detection
  - website-fingerprinting
method:
  - Transformer
  - BERT
  - masked-burst-modeling
  - SODF
  - RIFA
  - pre-training-finetuning
dataset:
  - ISCX-VPN-Service
  - Cross-Platform-Android
  - CSTNET-TLS1.3
  - USTC-TFC2016
  - CIC-IDS2017
  - CIC-AndMal2017
code: ""
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

# TrafficFormer: 高效的流量数据预训练模型

## 0. 基础信息

| 字段 | 内容 |
|------|------|
| 论文全称 | TrafficFormer: An Efficient Pre-trained Model for Traffic Data |
| 作者 | Guangmeng Zhou, Xiongwen Guo, Zhuotao Liu, Tong Li, Qi Li, Ke Xu |
| 机构 | 清华大学; 人民大学; 中关村实验室 |
| 发表年份 | 2025 |
| 会议/期刊 | S&P 2025 |
| 关键词 | Traffic Classification, Pre-training, Transformer, BERT, Masked Burst Modeling, SODF, RIFA |
| 代码 | 论文未明确说明 |

## 1. 一句话总结

提出 TrafficFormer，一种高效的流量数据预训练模型，通过 Masked Burst Modeling（MBM）和 Same Origin-Direction-Flow（SODF）多分类任务预训练，以及 Random Initialization Field Augmentation（RIFA）数据增强微调，在 6 个流量分类数据集上 F1-score 提升高达 10%，并在协议理解任务上显著优于现有预训练模型。

## 2. 摘要翻译

**原文：**
Traffic data contains deep domain-specific knowledge, making labeling challenging, and the lack of labeled data adversely impacts the accuracy of learning-based traffic analysis. The pre-training technology is widely adopted in the fields of vision and natural language to address the problem of limited labeled data. However, the exploration in the domain of traffic analysis remains insufficient. This paper proposes an efficient pre-training model, TrafficFormer, for traffic data. In the pre-training stage, TrafficFormer introduces a fine-grained multi-classification task to enhance the representation capabilities of traffic data; in the fine-tuning stage, TrafficFormer proposes a traffic data augmentation method utilizing the random initialization feature of fields, which helps the traffic model focus on key information. We evaluate TrafficFormer using both traffic classification tasks and protocol understanding tasks. The experimental results show that TrafficFormer achieves superior performance on six traffic classification datasets, with improvements of up to 10% in the F1 score and demonstrates significantly superior protocol understanding capabilities compared to existing traffic pre-training models.

**中文翻译：**
流量数据包含深厚的领域特定知识，使得标记具有挑战性，标记数据的缺乏对学习型流量分析的准确性产生不利影响。预训练技术在视觉和自然语言领域被广泛采用以解决标记数据有限的问题。然而，在流量分析领域的探索仍然不足。本文提出一种高效的流量数据预训练模型 TrafficFormer。在预训练阶段，TrafficFormer 引入细粒度多分类任务以增强流量数据的表示能力；在微调阶段，TrafficFormer 提出一种利用字段随机初始化特征的流量数据增强方法，帮助流量模型关注关键信息。我们使用流量分类任务和协议理解任务评估 TrafficFormer。实验结果表明，TrafficFormer 在六个流量分类数据集上取得优越性能，F1-score 提升高达 10%，并在协议理解能力上显著优于现有流量预训练模型。

## 3. 方法动机（Motivation）

### 3.1 问题背景与痛点

- **流量数据标记困难**：
  - 流量数据需要网络协议知识和特定场景经验
  - 攻击相关流量被大量背景流量淹没
  - 流量模式快速变化
  - 手动标记成本高，大规模高质量标记数据稀缺
- **现有预训练方法的局限**：
  - PERT：仅包级预训练，未充分利用流信息
  - ET-BERT：SBP 任务相对简单，学习信息有限
  - YaTC：将流视为图像，未充分利用序列特性
  - 现有方法仅探索流量表示以适应现有预训练技术，未针对流量数据定制

### 3.2 核心直觉

- **流量数据的特殊性**：
  - 顺序数据，类似自然语言，但方向和顺序更关键
  - 数据包顺序错误可能导致丢包（违反交互逻辑）
  - 包头信息存在高度冗余
- **定制化预训练**：
  - 保留掩码建模任务学习序列关系
  - 设计 SODF 任务挖掘方向和顺序信息
  - RIFA 数据增强减少对冗余信息的依赖

## 4. 方法设计（Method Design）

### 4.1 整体流程

```
原始流量 → 数据预处理 → 预训练（MBM + SODF） → 微调（RIFA） → 下游任务
            (bigram,     (Transformer           (数据增强)     (分类/理解)
             BPE)         Encoder)
```

### 4.2 数据预处理

- **输入**：原始十六进制数据包
- **处理**：
  - 流分割：基于 5-tuple 分割为多个流
  - 突发分割：每个流分为多个突发（同方向连续数据包）
  - bigram 转换：每两个相邻字节形成 4 位十六进制字符串
  - BPE 算法：构建最大 65,535 个 token 的语料库
  - 特殊 token：[CLS], [SEP], [PAD], [MASK], [UNK]
- **输出**：token 化的输入序列

### 4.3 预训练任务

**任务一：Masked Burst Modeling（MBM）**
- **输入**：突发序列
- **处理**：
  - 随机掩码部分 token
  - 模型利用上下文信息预测被掩码的 token
  - 交叉熵损失
- **输出**：预测的 token
- **关键点**：学习流量的序列关系

**任务二：Same Origin-Direction-Flow（SODF）多分类**
- **输入**：突发段组合
- **处理**：五个类别
  - 类别 1：正常突发（两个段分离）
  - 类别 2：乱序突发（两个段交换）
  - 类别 3：同流连续突发（两个突发分离）
  - 类别 4：乱序连续突发（两个突发交换）
  - 类别 5：不同流突发组合
- **输出**：类别预测
- **关键点**：同时学习方向、顺序和流信息

**预训练损失**：$loss = loss_{MBM} + loss_{SODF}$

### 4.4 微调阶段：RIFA 数据增强

- **输入**：下游任务的训练数据
- **处理**：
  - 利用字段的随机初始化特征
  - 随机替换某些字段的值
  - 保留流量语义，减少对冗余信息的依赖
- **输出**：增强后的训练数据
- **关键点**：帮助模型快速关注关键信息

### 4.5 下游任务

- **流量分类**：恶意软件检测、网站指纹、VPN 检测等
- **协议理解**（新引入）：
  - 数据包方向识别
  - 丢包检测
  - 乱序检测
  - 数据包预测

### 4.6 优缺点

**优势：**
- 针对流量数据定制的预训练任务
- SODF 任务同时学习方向、顺序和流信息
- RIFA 数据增强保留语义，减少冗余依赖
- 引入协议理解任务，全面评估模型能力
- 在 6 个分类数据集上 F1 提升高达 10%

**局限：**
- 预训练需要大规模无标签流量数据
- SODF 五分类任务设计复杂
- 在极小数据集上可能不如专用方法

## 5. 与其他方法对比（Comparison）

### 5.1 创新点

| 创新点 | 本文方法 | 现有方法 |
|--------|----------|----------|
| 预训练任务 | MBM + SODF（五分类） | MLM, NSP, MIM |
| 微调增强 | RIFA（字段随机初始化） | 无 |
| 评估维度 | 分类 + 协议理解 | 仅分类 |
| 流量表示 | bigram + BPE | bigram, 图, 图像 |
| 方向/顺序学习 | SODF 显式学习 | 隐式或不学习 |

### 5.2 与 Baseline 对比

与现有流量预训练模型对比：
- PERT：包级 MLM
- ET-BERT：突发级 MLM + SBP
- YaTC：图像级 MIM

**关键差异**：
- TrafficFormer 的 SODF 任务比 SBP 更细粒度，学习更多信息
- RIFA 数据增强是 TrafficFormer 独有的微调创新
- 协议理解任务是 TrafficFormer 引入的新评估维度

## 6. 实验表现（Experiments）

### 6.1 数据集

| 数据集 | 描述 | 任务 |
|--------|------|------|
| ISCX-VPN-Service | VPN 服务分类 | 流量分类 |
| CrossPlatform-Android | Android 应用分类 | 流量分类 |
| CSTNET-TLS1.3 | TLS 1.3 流量分类 | 流量分类 |
| USTC-TFC2016 | 流量分类 | 流量分类 |
| CIC-IDS2017 | 入侵检测 | 流量分类 |
| CIC-AndMal2017 | 恶意软件检测 | 流量分类 |
| 协议理解数据集 | 新引入 | 协议理解 |

### 6.2 Baseline 方法

- PERT
- ET-BERT
- YaTC
- 其他流量预训练模型

### 6.3 评估指标

- F1-score
- Accuracy
- 协议理解任务准确率

### 6.4 关键结果

**流量分类：**
- 在 6 个数据集上均取得最佳性能
- F1-score 提升高达 10%
- 优于所有现有预训练模型

**协议理解：**
- 数据包方向识别：显著优于现有方法
- 丢包检测：显著优于现有方法
- 乱序检测：显著优于现有方法
- 数据包预测：显著优于现有方法

**消融研究：**
- MBM 和 SODF 贡献相当
- RIFA 数据增强有效提升微调性能
- SODF 比 SBP 学习更多信息

## 7. 学习与应用（Learning & Application）

### 7.1 开源情况

- **代码**：论文未明确说明
- **可复现性**：提供了详细的算法描述

### 7.2 可迁移价值

- **预训练方法**：MBM 和 SODF 预训练任务可应用于其他流量分析模型
- **数据增强**：RIFA 方法可应用于其他结构化数据分析
- **协议理解**：协议理解任务可作为新的评估维度
- **BPE 应用**：BPE 在流量数据中的应用可推广

### 7.3 实际应用场景

- **恶意软件检测**：在标记数据有限时检测恶意流量
- **网站指纹**：在少量训练样本下识别网站
- **流量分类**：通用流量分类任务
- **协议分析**：理解和分析网络协议行为

## 8. 总结（Summary）

### 8.1 核心思想

TrafficFormer 的核心思想是针对流量数据的特殊性（方向、顺序、冗余）设计定制化的预训练任务。MBM 学习序列关系，SODF 同时学习方向、顺序和流信息，RIFA 数据增强减少对冗余信息的依赖。协议理解任务全面评估模型对流量行为的理解能力。

### 8.2 快速流程图

```
输入：原始十六进制流量数据
  ↓
数据预处理（bigram + BPE + 特殊 token）
  ↓
预训练（MBM：掩码突发建模 + SODF：同源方向流多分类）
  ↓
微调（RIFA：字段随机初始化增强）
  ↓
下游任务（流量分类 / 协议理解）
  ↓
输出：分类结果 / 协议理解结果
```

## 9. 知识链接（Knowledge Links）

- [[traffic-representation-learning]]：本文的核心贡献
- [[traffic-foundation-model]]：流量基础模型的研究方向
- [[pre-training-finetuning]]：预训练-微调范式
- [[transformer]]：模型架构
- [[traffic-classification]]：下游任务
- [[encrypted-traffic-analysis]]：加密流量分析的背景

## 10. 证据记录（Evidence）

| 声明 | 证据 | 来源 |
|------|------|------|
| F1 提升高达 10% | 6 个流量分类数据集 | 论文 §4 实验结果 |
| 协议理解显著优于现有方法 | 4 个协议理解任务 | 论文 §4 实验结果 |
| SODF 比 SBP 学习更多信息 | 消融研究 | 论文 §4 实验结果 |
| RIFA 有效提升微调性能 | 消融研究 | 论文 §4 实验结果 |
| 流量数据方向和顺序更关键 | 领域分析 | 论文 §3 |

## 11. 原始资料链接（Source Links）

- **PDF**：`00-inbox/PDFs/2025-S&P-TrafficFormer_An_Efficient_Pre-trained_Model_for_Traffic_Data.pdf`
- **MinerU MD**：`02-parsed-markdown/2025-S&P-TrafficFormer_An_Efficient_Pre-trained_Model_for_Traffic_Data.md`

## 12. 后续问题（Open Questions）

1. **模型规模**：更大规模的 TrafficFormer（如 large 版本）性能如何？
2. **多语言支持**：对于不同协议和加密方式，预训练的通用性如何？
3. **少样本学习**：在极少量标记数据（如 10 个样本）下，性能如何？
4. **实时推理**：TrafficFormer 的推理延迟是否满足实时需求？
5. **跨域迁移**：在完全不同的网络环境（如 IoT）下，预训练模型的迁移能力如何？

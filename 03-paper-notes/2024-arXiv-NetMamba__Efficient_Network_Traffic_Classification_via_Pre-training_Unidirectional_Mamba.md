---
type: paper
title_original: "NetMamba: Efficient Network Traffic Classification via Pre-training Unidirectional Mamba"
title_cn: "NetMamba：通过预训练单向 Mamba 实现高效网络流量分类"
authors:
  - Tongze Wang
  - Xiaohui Xie
  - Wenduo Wang
  - Chuyi Wang
  - Youjian Zhao
  - Yong Cui
year: 2024
venue: arXiv
doi: unknown
url: https://arxiv.org/abs/2405.xxxxx
pdf: "00-inbox/PDFs/2024-arXiv-NetMamba__Efficient_Network_Traffic_Classification_via_Pre-training_Unidirectional_Mamba.pdf"
mineru_md: "02-parsed-markdown/2024-arXiv-NetMamba__Efficient_Network_Traffic_Classification_via_Pre-training_Unidirectional_Mamba.md"
status: processed
reading_level: L2
research_area:
  - 加密流量分类
  - 预训练模型
  - 状态空间模型
task:
  - 加密应用分类
  - 攻击流量分类
  - 恶意流量分类
method:
  - 单向 Mamba（State Space Model）
  - MAE 预训练
  - Stride-based 流量表示
  - 位置嵌入 + class token
dataset:
  - CrossPlatform (Android)
  - CrossPlatform (iOS)
  - ISCXTor2016
  - ISCXVPN2016
  - CICIoT2022
  - USTC-TFC2016
code: "available (link in paper)"
relevance: high
created: 2026-06-09
updated: 2026-06-09
---

# NetMamba: Efficient Network Traffic Classification via Pre-training Unidirectional Mamba

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | NetMamba: Efficient Network Traffic Classification via Pre-training Unidirectional Mamba |
| 中文标题 | NetMamba：通过预训练单向 Mamba 实现高效网络流量分类 |
| 作者 | Tongze Wang, Xiaohui Xie, Wenduo Wang, Chuyi Wang, Youjian Zhao, Yong Cui |
| 年份 | 2024 |
| 会议/期刊 | arXiv |
| 研究方向 | 加密流量分类 / 预训练模型 / 状态空间模型 |
| 任务类型 | 加密应用分类、攻击流量分类、恶意流量分类 |
| 方法关键词 | Mamba、State Space Model、MAE 预训练、Stride 表示、线性时间复杂度 |
| 数据集 | CrossPlatform (Android/iOS)、ISCXTor2016、ISCXVPN2016、CICIoT2022、USTC-TFC2016 |
| 是否开源 | 是 |
| PDF | `00-inbox/PDFs/2024-arXiv-NetMamba__Efficient_Network_Traffic_Classification_via_Pre-training_Unidirectional_Mamba.pdf` |
| MinerU Markdown | `02-parsed-markdown/2024-arXiv-NetMamba__Efficient_Network_Traffic_Classification_via_Pre-training_Unidirectional_Mamba.md` |

---

## 1. 一句话总结

> 首个将 Mamba（线性时间状态空间模型）应用于网络流量分类的工作，通过单向 Mamba 架构 + MAE 预训练 + 综合流量表示方案，在 6 个数据集上实现 SOTA 分类性能，推理速度比 Transformer 快 60 倍。

---

## 2. 摘要翻译

### 2.1 摘要原文

Network traffic classification is a crucial research area aiming to enhance service quality, streamline network management, and bolster cybersecurity. To address the growing complexity of transmission encryption techniques, various machine learning and deep learning methods have been proposed. However, existing approaches face two main challenges. Firstly, they struggle with model inefficiency due to the quadratic complexity of the widely used Transformer architecture. Secondly, they suffer from inadequate traffic representation because of discarding important byte information while retaining unwanted biases. To address these challenges, we propose NetMamba, an efficient linear-time state space model equipped with a comprehensive traffic representation scheme. We adopt a specially selected and improved unidirectional Mamba architecture for the networking field, instead of the Transformer, to address efficiency issues. In addition, we design a traffic representation scheme to extract valid information from massive traffic data while removing biased information. Evaluation experiments on six public datasets encompassing three main classification tasks showcase NetMamba's superior classification performance compared to state-of-the-art baselines. It achieves accuracy rates exceeding 90%, with some surpassing 99%, across all tasks. Additionally, NetMamba demonstrates excellent efficiency, improving inference speed by up to 60 times while maintaining comparably low memory usage.

### 2.2 摘要中文翻译

网络流量分类是旨在提升服务质量、简化网络管理和增强网络安全的关键研究领域。为应对日益复杂的传输加密技术，各种机器学习和深度学习方法被提出。然而，现有方法面临两大挑战：(1) 广泛使用的 Transformer 架构的二次复杂度导致模型效率低下；(2) 丢弃重要字节信息同时保留不必要偏差导致流量表示不充分。为解决这些挑战，我们提出 NetMamba，一种配备综合流量表示方案的高效线性时间状态空间模型。我们采用经专门选择和改进的单向 Mamba 架构替代 Transformer 以解决效率问题，并设计流量表示方案从海量流量数据中提取有效信息同时消除偏差。在涵盖三个主要分类任务的六个公开数据集上的评估实验表明，NetMamba 的分类性能优于 SOTA 基线，准确率均超过 90%，部分超过 99%。此外，NetMamba 展现出优异的效率，推理速度提升最高达 60 倍，同时保持较低的内存使用。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- Transformer 的二次自注意力复杂度使其不适合实时在线流量分类和资源受限的网络设备
- 现有流量表示方案存在不足：丢弃头部信息、忽略字节平衡、使用不当的数据分割方式

### 3.2 现有方法的痛点和不足

- **效率问题**：Transformer 的 O(L^2) 复杂度在长序列上计算和内存开销大
- **表示问题**：PERT/ET-BERT 丢弃包头信息；2D patch splitting 引入语义无关的垂直偏差；tokenization 引入 OOV 问题
- **现有 Mamba 变体**：未在网络流量领域验证，需选择合适的架构

### 3.3 论文的研究假设或核心直觉

(1) 网络流量的序列特性天然适合单向 Mamba 的前到后处理方式；(2) 1D stride cutting 比 2D patch splitting 更适合保留流量的序列语义；(3) 包头和包载荷的信息都对分类有贡献，不应丢弃。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | Transformer 在 NLP/CV 成功但效率受限，Mamba 在多领域展现优势 | §I, §II |
| 痛点提炼 | 现有流量预训练模型效率低（ET-BERT 187M 参数）、表示不充分 | §I, Table I |
| 问题转化 | 能否用线性时间的 Mamba 替代 Transformer 并改进流量表示？ | §I |
| 文献定位 | Mamba 未在网络流量领域应用，表示方案存在明确缺陷 | §II-B, §II-C |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 单向 Mamba 比 Transformer 更适合处理序列网络流量 | 流量的序列传输特性 + Mamba 的线性复杂度 | 消融实验（Table VI） |
| 辅助假设 1 | 1D stride cutting 优于 2D patch splitting | 网络流量是自然序列数据 | 消融实验 |
| 辅助假设 2 | 保留头部信息对分类至关重要 | 头部包含端口、协议等关键字段 | 消融实验（去掉头部 accuracy 降 15-48%） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | 单向 Mamba 优于双向/级联 Mamba 和 Transformer 变体 | Table VI |
| 辅助假设 1 | 支撑 | Patch splitting 导致最高 1.88% accuracy 下降 | Table VI |
| 辅助假设 2 | 支撑 | 去掉头部 accuracy 下降 15.51%-48.75% | Table VI |

---

## 4. 方法设计

### 4.1 方法整体流程

三阶段：(1) 流量表示——将原始流量转为 stride 序列；(2) 预训练——使用 MAE 结构在无标签数据上学习通用表示；(3) 微调——替换 decoder 为 MLP head 进行下游分类。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | 原始 pcap | Flow splitting（5-tuple）→ Packet parsing（去除以太网头）→ Cropping & Padding（固定 N_h=80, N_p=240）→ Concatenation | 字节数组 [b1,...,bLb] | 标准化输入 |
| Step 2 | 字节数组 | Stride cutting（L_s=4）→ Stride embedding（线性投影 + 位置嵌入 + class token） | Token 序列 X0 | 序列化表示 |
| Step 3 | Token 序列 | Random masking（r=0.9）→ Encoder（4 Mamba blocks）→ Decoder（2 Mamba blocks）→ MSE 重建损失 | 预训练模型 | 学习通用表示 |
| Step 4 | Token 序列 | Encoder → class token → MLP head → Cross-entropy loss | 分类结果 | 下游任务适配 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Stride Embedding | 将 stride 映射到高维空间 | Stride s_i | 嵌入 X0 | 输入 Encoder |
| NetMamba Block (Encoder) | 前向序列建模 | X_{t-1} | X_t | 4 层堆叠 |
| NetMamba Block (Decoder) | 重建 masked stride | Encoder 输出 + mask token | 重建结果 | 2 层堆叠 |
| MLP Head | 分类预测 | Class token | 预测分布 y_hat | 替换 Decoder |

### 4.4 公式、算法和机制解释

- **State Space Model**：h'(t) = Ah(t) + Bx(t), y(t) = Ch(t)，离散化后变为递归形式
- **Selection Mechanism**：Mamba 的核心创新，使参数 B, C, Delta 依赖输入 x，实现内容感知推理
- **NetMamba Block**：Norm → Linear(x, z) → Conv1d(x) → SSM → SiLU gating(z) → residual
- **预训练损失**：MSE(y_real, y_rec)，仅计算 masked stride 的重建误差
- **微调损失**：CrossEntropy(y_hat, y)，使用 class token 的输出进行分类
- **计算复杂度**：SSM = O(LEN) = O(96LD)，远低于 Vanilla Attention = O(4LD^2 + 2L^2D)

### 4.5 方法优势

- 线性时间复杂度，推理速度比 Transformer 快 1.22-60.11 倍
- 参数量最少（2.2M 预训练 / 1.9M 微调），远低于 ET-BERT（187M/136M）
- 综合流量表示保留头部+载荷信息，消除偏差
- 优异的 few-shot 学习能力

### 4.6 方法不足

- 依赖 GPU 硬件，难以部署在资源受限的网络设备上
- 在 CICIoT2022 上略逊于 TFE-GNN（0.72 个百分点）
- 单向处理可能遗漏后续包对前序包的反向依赖
- 未验证在超长流量序列上的表现

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

NetMamba 是首个将 Mamba（而非 Transformer）应用于网络流量分类的工作。其核心区别在于：(1) 使用线性时间 SSM 替代二次时间 attention；(2) 提出综合的流量表示方案同时保留头部和载荷信息。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 单向 Mamba 用于流量 | 选择原始单向架构而非双向/级联变体 | 高 | 是（其他序列流量任务） |
| Stride-based 表示 | 1D stride cutting 保留序列语义 | 高 | 是（其他序列数据） |
| 综合表示方案 | 保留头部+载荷，IP 匿名化，字节平衡 | 中 | 是 |
| MAE 预训练策略 | Masked stride reconstruction | 中 | 是 |

### 5.3 适用场景

- 实时在线加密流量分类（低延迟要求）
- 资源受限的网络设备（小模型、低内存）
- 标注数据有限的场景（few-shot 学习）
- 需要处理多种分类任务的通用流量分析

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| ET-BERT | 强大的预训练表示 | 187M 参数，仅用载荷 | 2.2M 参数，保留头部+载荷 |
| YaTC | 高效设计 | Transformer 二次复杂度 | SSM 线性复杂度，速度提升 2.24 倍 |
| TFE-GNN | 在特定数据集上最优 | 非预训练，泛化差 | 预训练提供更强泛化 |
| FlowPrint | 无需训练 | 基于统计特征，精度有限 | 端到端深度学习 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

6 个公开数据集，3 类任务（加密应用分类、攻击流量分类、恶意流量分类）。预训练 150K steps，batch 128，masking ratio 0.9。微调 120 epochs，batch 64，8:1:1 数据划分。

### 6.2 数据集

| 数据集 | 任务 | 类别数 |
|---|---|---|
| CrossPlatform (Android) | 加密应用分类 | 254 |
| CrossPlatform (iOS) | 加密应用分类 | 253 |
| ISCXTor2016 | Tor 流量分类 | 8 |
| ISCXVPN2016 | VPN 流量分类 | 7 |
| CICIoT2022 | 攻击流量分类 | 6 |
| USTC-TFC2016 | 恶意流量分类 | 20 |

### 6.3 Baseline

- 传统 ML：AppScanner, FlowPrint
- 深度学习：FS-Net, TFE-GNN
- Transformer 预训练：ET-BERT, YaTC, YaTC(OF)
- Transformer 变体：NT-Vanilla, NT-Linear

### 6.4 评价指标

Accuracy (AC), Precision (PR), Recall (RC), weighted F1 Score (F1)

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| CrossPlatform (Android) | F1 | 0.9096 | 0.9077 (YaTC-OF) | +0.19% | |
| CrossPlatform (iOS) | F1 | 0.9305 | 0.9272 (YaTC) | +0.33% | |
| ISCXTor2016 | F1 | 0.9986 | 0.9986 (YaTC-OF) | 持平 | |
| ISCXVPN2016 | F1 | 0.9806 | 0.9848 (YaTC) | -0.42% | 略逊 |
| CICIoT2022 | F1 | 0.9929 | 1.0000 (TFE-GNN) | -0.71% | 略逊 |
| USTC-TFC2016 | F1 | 0.9957 | 0.9970 (YaTC) | -0.13% | 略逊 |
| 推理速度 (batch=64) | samples/s | ~7500 | ~3350 (YaTC-OF) | 2.24x | |
| 推理速度 (batch=5) | samples/s | - | - | 60.11x | vs ET-BERT |

### 6.6 优势最明显的场景

- 大规模应用分类（CrossPlatform 200+ 类别）
- 需要高推理速度的在线分类场景
- 标注数据有限的 few-shot 场景

### 6.7 局限性

- 在 CICIoT2022 上略逊于 TFE-GNN（非预训练模型在特定数据集上可能更优）
- 在 ISCXVPN2016 上略逊于 YaTC
- 当前实现依赖 GPU，无法直接部署在网络设备上

---

## 7. 学习与应用

### 7.1 是否开源？

是

### 7.2 复现关键步骤

1. 数据预处理：5-tuple flow splitting → 去除以太网头 → 裁剪/填充（N_h=80, N_p=240）→ 拼接 → stride cutting（L_s=4）
2. 预训练：MAE 结构，masking ratio 0.9，150K steps，batch 128
3. 微调：替换 decoder 为 MLP head，120 epochs，batch 64

### 7.3 关键超参数、预训练和训练细节

| 参数 | 值 | 说明 |
|---|---|---|
| M | 5 | 每流选取的包数 |
| N_h | 80 | 每包头部字节数 |
| N_p | 240 | 每包载荷字节数 |
| L_s | 4 | Stride 长度 |
| D_enc | 256 | Encoder 隐藏维度 |
| E_enc | 512 | Encoder 扩展维度 |
| r | 0.9 | Masking ratio |
| 预训练 lr | 1e-3 | AdamW |
| 微调 lr | 2e-3 | |

### 7.4 能否迁移到其他任务？

- Stride-based 表示方案可迁移到其他序列流量分析任务
- Mamba 架构可应用于流量生成、异常检测等任务
- 预训练策略可迁移到更大规模的流量基础模型

### 7.5 对我的研究有什么启发？

- Mamba 是 Transformer 在流量分类领域的有力替代，尤其在效率敏感场景
- 流量表示方案的设计（头部+载荷、字节平衡、stride cutting）对性能影响巨大
- 单向 Mamba 适合网络流量的自然序列特性
- 预训练+微调范式在流量领域继续有效

---

## 8. 总结

### 8.1 核心思想

> 用线性时间 Mamba 替代 Transformer，配合综合流量表示实现高效准确分类。

### 8.2 速记版 Pipeline

1. 流量表示：5-tuple 分流 → 裁剪填充 → 拼接 → stride cutting
2. 预训练：MAE 结构，masked stride reconstruction
3. 微调：class token → MLP 分类头
4. 推理：单向 Mamba 线性处理，低延迟高吞吐

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- State Space Model (SSM)
- Mamba 架构
- Masked Autoencoder (MAE)
- 加密流量分类
- 预训练模型

### 9.2 相关方法

- ET-BERT
- YaTC
- Transformer 流量分类

### 9.3 相关任务

- 加密应用分类
- 恶意流量检测
- 攻击流量分类

### 9.4 可更新的综述页面

- 预训练流量模型综述
- 加密流量分类方法对比

### 9.5 可加入的对比表

- 预训练流量模型性能对比
- 流量表示方案对比

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 单向 Mamba 优于双向和级联变体 | 消融实验：双向下降 0.8-10%，级联下降 9-17% | Table VI |
| 头部信息至关重要 | 去掉头部 accuracy 下降 15.51%-48.75% | Table VI |
| Stride cutting 优于 patch splitting | Patch splitting 导致最高 1.88% 下降 | Table VI |
| 预训练带来 0.20%-4.70% 提升 | 预训练 vs 非预训练对比 | Table VI |
| 推理速度提升 1.22-60.11 倍 | 与多种 baseline 对比 | §VII-C |
| 参数量最少（2.2M） | 与其他深度学习方法对比 | Table IV, V |

---

## 11. 原始资料链接

- PDF：`00-inbox/PDFs/2024-arXiv-NetMamba__Efficient_Network_Traffic_Classification_via_Pre-training_Unidirectional_Mamba.pdf`
- MinerU Markdown：`02-parsed-markdown/2024-arXiv-NetMamba__Efficient_Network_Traffic_Classification_via_Pre-training_Unidirectional_Mamba.md`

---

## 12. 后续问题

- Mamba 在流量生成任务上的表现如何？
- 如何在资源受限设备上部署 NetMamba？
- 单向 vs 双向在更长流量序列上的表现差异如何？
- Mamba 能否用于多模态流量分析（包级 + 流级 + 主机级）？

---

## 13. 写作叙事与故事线分析

> 仅对 CCF A/B 级或用户指定深度分析的论文填写本节。

### 13.1 论文主线故事线

论文从 Transformer 在流量分类中的效率瓶颈出发，指出 Mamba 作为线性时间序列模型在 NLP/CV 已展现优势但未被应用于网络领域。作者通过精心选择单向 Mamba 架构、设计综合流量表示方案、采用 MAE 预训练策略，在 6 个数据集上实现 SOTA 性能同时大幅提升推理效率。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 概述效率和性能双提升 | 全文缩影 | - |
| Introduction | 从 Transformer 效率瓶颈引入 | 问题背景 | 二次复杂度限制在线部署 |
| Related Work | Mamba 在其他领域的成功 | 技术可行性 | Mamba 未在网络领域应用 |
| Preliminaries | SSM 基础知识 | 理论铺垫 | Selection mechanism |
| Framework | 三阶段设计概览 | 方法框架 | Stride + MAE + Fine-tune |
| Traffic Representation | 详细表示方案设计 | 核心贡献之一 | Stride cutting vs patch splitting |
| Model Details | 架构和训练策略 | 核心贡献之二 | 单向 Mamba 选择 |
| Evaluation | 全面实验评估 | 证据支撑 | 60x 加速 + SOTA |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 性能瓶颈 | Transformer 二次复杂度限制实时部署 | 计算复杂度对比分析 | §I |
| 表示不足 | 现有方案丢弃头部/忽略字节平衡/不当分割 | Table I 详细对比 | §II-C |
| 场景缺失 | Mamba 未在网络流量领域应用 | 文献空白 | §II-B |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 整体评估 | 证明分类性能 SOTA | 核心有效性 |
| 效率评估 | 证明推理速度优势 | 核心效率 |
| 消融实验 | 归因每个设计选择 | 设计合理性 |
| Few-shot 评估 | 证明泛化能力 | 实用价值 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 从 Transformer 效率瓶颈切入 | 技术瓶颈驱动的架构创新 |
| Gap 提出方式 | 效率 + 表示两个维度并行 | 双 Gap 结构 |
| 方法论证逻辑 | 精心选择 Mamba 变体 + 全新表示方案 | 架构选择 + 数据工程并重 |
| 实验组织逻辑 | 整体 -> 效率 -> 消融 -> few-shot | 全面性评估框架 |
| 局限性讨论方式 | 坦诚承认 GPU 依赖和部分数据集略逊 | 实事求是 |
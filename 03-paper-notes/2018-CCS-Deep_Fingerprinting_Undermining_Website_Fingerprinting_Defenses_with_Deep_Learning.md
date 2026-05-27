---
type: paper
title_original: "Deep Fingerprinting: Undermining Website Fingerprinting Defenses with Deep Learning"
title_cn: "深度指纹：利用深度学习破坏网站指纹防御"
authors:
  - Payap Sirinam
  - Mohsen Imani
  - Marc Juarez
  - Matthew Wright
year: 2018
venue: "ACM CCS 2018"
doi: "10.1145/3243734.3243768"
url: "https://dl.acm.org/doi/10.1145/3243734.3243768"
pdf: "00-inbox/PDFs/2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning.pdf"
mineru_md: "02-parsed-markdown/2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning.md"
status: processed
reading_level: L2
research_area:
  - Website Fingerprinting
  - Traffic Analysis
  - Privacy & Anonymity
task:
  - Website Classification
  - Tor Traffic Analysis
method:
  - CNN
  - Deep Learning
dataset:
  - "Closed-world: 95 sites, 1000 traces/site (Alexa top 100)"
  - "Open-world: 40,716 traces (Alexa top 50,000)"
code: "https://github.com/deep-fingerprinting/df"
relevance: high
created: "2026-05-27"
updated: "2026-05-27"
---

# Deep Fingerprinting: Undermining Website Fingerprinting Defenses with Deep Learning

## 0. 论文基础信息（表格）

| 项目 | 内容 |
|------|------|
| 论文标题 | Deep Fingerprinting: Undermining Website Fingerprinting Defenses with Deep Learning |
| 作者 | Payap Sirinam, Mohsen Imani, Marc Juarez, Matthew Wright |
| 机构 | Rochester Institute of Technology; University of Texas at Arlington; KU Leuven |
| 会议/期刊 | ACM CCS 2018 |
| 发表时间 | 2018年10月 |
| DOI | 10.1145/3243734.3243768 |
| 引用量 | 490 |
| 下载量 | 10,935 |
| 关键词 | Tor; privacy; website fingerprinting; deep learning |

## 1. 一句话总结

提出基于 CNN 的 Deep Fingerprinting (DF) 攻击，在 Tor 无防御场景下达到 98.3% 准确率，首次在闭世界中以 90.7% 准确率有效攻破 WTF-PAD 防御。

## 2. 摘要翻译（原文+中文）

**原文：**
Website fingerprinting enables a local eavesdropper to determine which websites a user is visiting over an encrypted connection. State-of-the-art website fingerprinting attacks have been shown to be effective even against Tor. Recently, lightweight website fingerprinting defenses for Tor have been proposed that substantially degrade existing attacks: WTF-PAD and Walkie-Talkie. In this work, we present Deep Fingerprinting (DF), a new website fingerprinting attack against Tor that leverages a type of deep learning called Convolutional Neural Networks (CNN) with a sophisticated architecture design, and we evaluate this attack against WTF-PAD and Walkie-Talkie. The DF attack attains over 98% accuracy on Tor traffic without defenses, better than all prior attacks, and it is also the only attack that is effective against WTF-PAD with over 90% accuracy. Walkie-Talkie remains effective, holding the attack to just 49.7% accuracy. In the more realistic open-world setting, our attack remains effective, with 0.99 precision and 0.94 recall on undefended traffic. Against traffic defended with WTF-PAD in this setting, the attack still can get 0.96 precision and 0.68 recall.

**中文翻译：**
Website fingerprinting 使本地窃听者能够通过加密连接确定用户正在访问哪些网站。最先进的 website fingerprinting 攻击已被证明对 Tor 仍然有效。最近，针对 Tor 的轻量级 website fingerprinting 防御方案被提出，能显著削弱现有攻击的效果，包括 WTF-PAD 和 Walkie-Talkie。本文提出 Deep Fingerprinting (DF)，一种基于 Convolutional Neural Network (CNN) 的新型 website fingerprinting 攻击方法，采用精心设计的网络架构，并对 WTF-PAD 和 Walkie-Talkie 进行评估。DF 攻击在无防御 Tor 流量上达到超过 98% 的准确率，优于所有先前攻击；它也是唯一能有效攻击 WTF-PAD 的方法，准确率超过 90%。Walkie-Talkie 仍然有效，将攻击限制在仅 49.7% 的准确率。在更现实的 open-world 场景中，DF 攻击在无防御流量上达到 0.99 precision 和 0.94 recall；在 WTF-PAD 防御流量上仍可达 0.96 precision 和 0.68 recall。

## 3. 方法动机（为什么提出、现有痛点、核心直觉）

**现有痛点：**
1. 传统 WF 攻击（k-NN、CUMUL、k-FP）依赖手工设计的特征（如 packet ordering、burst 计数、cumulative sum 等），特征工程耗时且受限于专家经验。
2. 轻量级防御 WTF-PAD 和 Walkie-Talkie 被认为能在合理开销下有效降低传统攻击准确率至 30% 以下，是 Tor 项目实际考虑部署的防御方案。
3. 已有的深度学习方法（SDAE、AWF）虽初步探索了 DL 在 WF 中的应用，但未能超越传统攻击，尤其无法有效攻破防御。

**核心直觉：**
- DL（特别是 CNN）在图像分类等领域已大幅超越传统 ML，且不依赖手工特征设计。
- CNN 通过卷积层可以自动提取层次化特征，具有平移不变性，能检测流量 trace 中任意位置的微小区分模式。
- 更深、更精心设计的 CNN 架构（借鉴 VGG/GoogleNet/ResNet 的设计思想）应当能在 WF 任务上取得显著提升。

**为什么提出 DF：**
- 已有 DL 方法（AWF）架构过于简单（类似 2012 年的 ImageNet），过拟合风险高，且未充分考虑流量数据的特殊性（负值方向信息）。
- 需要一种专门为 WF 任务设计的深度 CNN 模型，充分借鉴计算机视觉领域的最新进展。

## 4. 方法设计（整体流程、详细 Pipeline 表格、模型模块表格、公式解释、优势、不足）

### 整体流程

1. **数据采集**：通过 Tor Browser 访问目标网站，抓取流量 trace
2. **数据预处理**：将流量 trace 转换为 packet direction 序列（+1/-1），截断/填充至固定长度 5000
3. **模型训练**：使用预处理后的数据训练 DF CNN 模型
4. **分类预测**：将待识别的流量 trace 输入训练好的模型，输出网站分类结果

### 详细 Pipeline 表格

| 阶段 | 操作 | 详细说明 |
|------|------|----------|
| 输入表示 | packet direction 序列 | 每个 packet 仅保留方向（+1 outgoing, -1 incoming），忽略 packet size 和 timestamp |
| 输入维度 | 1 x 5000 | 固定长度 5000 cells；短于 5000 的 trace 用零填充，长于 5000 的截断 |
| 特征提取 | 4 个 Block，每 Block 含 2 层 Conv1D | Block1: 32 filters; Block2: 64 filters; Block3: 128 filters; Block4: 256 filters |
| 卷积参数 | Kernel=1x8, Stride=4, Pool=1x8 | 1D 卷积操作，适配流量数据的一维特性 |
| 激活函数 | Block1 用 ELU, 其余用 ReLU | ELU 可处理负值输入（packet direction 为负），保留方向信息 |
| 正则化 | Batch Normalization + Dropout | BN 紧跟每个 Conv 和 FC 层；Dropout 在 Pooling 后（0.1）和 FC 层后（0.7, 0.5） |
| 分类部分 | 2 层 Fully-Connected | 各 512 hidden units，配合 BN 和 Dropout |
| 输出 | Softmax | 95 类（闭世界）或 monitored/unmonitored（开世界） |

### 模型模块表格（DF vs AWF 对比）

| 模块 | DF | AWF |
|------|----|-----|
| 基本块设计 | 每 Block 含 2 个 Conv 层后接 Pooling（类似 VGG） | 每 Block 含 1 个 Conv 层后接 Pooling（类似 ImageNet 2012） |
| 网络深度 | 4 Blocks x 2 Conv = 8 Conv 层 | 3 Blocks x 1 Conv = 3 Conv 层 |
| 滤波器数量 | 逐层递增：32->64->128->256 | 每层固定 32 |
| Batch Normalization | 每个 Conv 和 FC 层后均有 | 无 |
| Dropout 位置 | Pooling 后 0.1 + FC 后 0.7/0.5 | 仅在第一个 Block 前 |
| 激活函数 | Block1: ELU, 后续: ReLU | 全部 ReLU |
| FC 层 | 2 层 FC（512 units）+ BN + Dropout | 直接 Max Pooling -> Prediction |

### 关键设计决策解释

**ELU 激活函数：** 标准 ReLU 将所有负值映射为零，而 WF 输入中负值代表 incoming packet 方向信息。ELU 在负值区间有非零输出，能保留方向信息。实验表明 Block1 使用 ELU + 后续 Block 使用 ReLU 的组合效果最佳。

**逐层递增滤波器数量：** 借鉴层次化特征学习思想——底层提取简单原始特征（如边缘），高层提取抽象组合特征。增加高层滤波器数量能编码更丰富的表示。

**1D 输入 vs 2D 输入：** 实验比较发现 1D 输入训练速度显著快于 2D（相同数据点数），且分类精度略优，因此采用 1D 输入。

### 训练超参数（最终选定值）

| 超参数 | 值 |
|--------|----|
| Input Dimension | 5000 |
| Optimizer | Adamax |
| Learning Rate | 0.002 |
| Training Epochs | 30 |
| Mini-batch Size | 128 |
| [Filter, Pool, Stride] | [8, 8, 4] |
| 激活函数 | ELU (Block1), ReLU (Block2-4) |
| Dropout [Pooling, FC1, FC2] | [0.1, 0.7, 0.5] |
| 数据划分 | 训练:验证:测试 = 8:1:1 |

### 优势

1. **无需手工特征设计**：CNN 自动从原始 packet direction 序列中提取特征
2. **深层架构有效提取特征**：8 层 Conv 远多于 AWF 的 3 层，能捕获更复杂的流量模式
3. **对防御流量有效**：CNN 的卷积操作具有平移不变性，能检测 WTF-PAD 随机 padding 后残留的微小模式
4. **过拟合控制良好**：训练与测试误差率差异小于 2%
5. **迁移性好**：超参数可从无防御场景迁移到防御场景，仅需微调

### 不足

1. **固定输入长度限制**：5000 cells 的截断/填充可能丢失信息（8,121 条 trace 被截断）
2. **仅使用 packet direction**：忽略了 packet size 和 timing 信息
3. **对 Walkie-Talkie 效果有限**：仅 49.7% 准确率（接近理论上限 50%）
4. **训练开销较大**：GPU 下需 64 分钟（30 epochs），无 GPU 约 10 小时
5. **开世界场景性能下降**：WTF-PAD 防御下 recall 仅 0.68

## 5. 与其他方法对比（本质区别、创新点表格、适用场景、方法对比表）

### 本质区别

传统 WF 攻击（k-NN、CUMUL、k-FP）依赖手工特征 + 传统分类器；已有 DL 方法（SDAE、AWF）使用简单网络架构。DF 的核心区别在于：借鉴现代计算机视觉网络（VGG/ResNet）设计思想，构建专为 WF 任务优化的深层 CNN，通过 ELU 激活、BN、层次化滤波器等技术，在不依赖手工特征的情况下实现更强大的特征提取和分类能力。

### 创新点表格

| 创新点 | 说明 |
|--------|------|
| 首个针对 WF 优化的深层 CNN | 8 层 Conv，借鉴 VGG 设计，远深于 AWF 的 3 层 |
| ELU 激活函数用于 WF | 解决 ReLU 丢弃负值方向信息的问题 |
| 层次化滤波器设计 | 逐层递增滤波器数量（32->64->128->256） |
| 全面的过拟合对策 | BN + 多处 Dropout，训练-测试误差差异<2% |
| 首次攻破 WTF-PAD | 闭世界 90.7%，开世界 precision 0.96 / recall 0.68 |
| 大规模数据集评估 | 95 sites x 1000 traces，远大于之前的数据集 |

### 方法对比表

| 方法 | 分类器 | 特征类型 | 闭世界准确率(无防御) | WTF-PAD 准确率 | W-T 准确率 |
|------|--------|----------|---------------------|----------------|------------|
| k-NN | k-Nearest Neighbors | 手工特征（packet ordering, burst count） | 95.0% | 16.0% | 20.2% |
| CUMUL | SVM | Cumulative sum of packet lengths | 97.3% | 60.3% | 38.4% |
| k-FP | Random Forest + k-NN | Random forest leaf features | 95.5% | 69.0% | 7.0% |
| SDAE | Stacked Denoising Autoencoder | 自动特征 | 92.3% | 36.9% | 23.1% |
| AWF | CNN（简单架构） | 自动特征 | 94.9% | 60.8% | 45.8% |
| **DF** | **CNN（深层架构）** | **自动特征** | **98.3%** | **90.7%** | **49.7%** |

## 6. 实验表现（实验设置、数据集、Baseline、指标、关键结果表格、优势场景、局限性）

### 实验设置

- **硬件**：10 台低端机器采集数据；NVIDIA GTX 1070 (8GB GPU) 用于训练
- **软件**：Python + Keras (前端) + TensorFlow (后端)；tor-browser-crawler 驱动 Tor Browser
- **训练策略**：数据划分 8:1:1；30 epochs；Adamax optimizer；learning rate 0.002
- **评估方式**：闭世界用 10-fold cross-validation；开世界用 precision-recall 曲线

### 数据集

| 数据集 | 说明 |
|--------|------|
| 闭世界（无防御） | 95 sites (Alexa top 100)，每 site 1000 traces，共 95,000 traces |
| 开世界（无防御） | 闭世界 + 20,000 unmonitored sites，共 40,716 traces |
| 闭世界（WTF-PAD） | 同闭世界数据集，用 WTF-PAD simulator 保护 |
| 闭世界（Walkie-Talkie） | 使用半双工 Tor Browser 重新抓取，100 sites x 910 traces |
| 闭世界（BuFLO/Tamaraw） | 同闭世界数据集，分别用对应 simulator 保护 |

### Baseline

k-NN、CUMUL、k-FP、AWF、SDAE（均在相同数据集上重新评估）

### 评估指标

- 闭世界：Accuracy
- 开世界：TPR、FPR、Precision、Recall、Precision-Recall 曲线、ROC 曲线

### 关键结果表格

**闭世界 - 无防御：**

| 方法 | Accuracy |
|------|----------|
| SDAE | 92.3% |
| AWF | 94.9% |
| k-NN | 95.0% |
| k-FP | 95.5% |
| CUMUL | 97.3% |
| **DF** | **98.3%** |

**闭世界 - 有防御：**

| 防御 | 带宽开销 | SDAE | DF | AWF | k-NN | CUMUL | k-FP |
|------|---------|------|----|----|------|-------|------|
| BuFLO | 246% | 9.2% | 12.6% | 11.7% | 10.4% | 13.5% | 13.1% |
| Tamaraw | 328% | 11.8% | 11.8% | 12.9% | 9.7% | 16.8% | 11.0% |
| WTF-PAD | 64% | 36.9% | **90.7%** | 60.8% | 16.0% | 60.3% | 69.0% |
| Walkie-Talkie | 31% | 23.1% | **49.7%** | 45.8% | 20.2% | 38.4% | 7.0% |

**开世界 - Precision/Recall：**

| 场景 | DF Precision | DF Recall |
|------|-------------|-----------|
| 无防御 | 0.99 | 0.94 |
| WTF-PAD（高 precision） | 0.96 | 0.68 |
| WTF-PAD（高 recall） | 0.67 | 0.96 |
| Walkie-Talkie | <0.36 | 全范围 |

### 优势场景

1. **无防御 Tor 流量**：98.3% 闭世界准确率，开世界 0.99 precision
2. **WTF-PAD 防御流量**：90.7% 闭世界准确率，大幅领先其他所有攻击方法
3. **小样本学习**：仅 50 traces/site 即可达到 90% 准确率
4. **快速收敛**：10 个 epoch 即可达到约 97% 测试准确率

### 局限性

1. **Walkie-Talkie 仍然有效**：仅 49.7%（接近理论上限 50%），Top-2 准确率 98.44% 说明 DF 能正确识别真实站点和 decoy，但无法区分
2. **开世界 WTF-PAD 场景 recall 偏低**：高 precision 设置下 recall 仅 0.68
3. **BuFLO/Tamaraw 依然难以攻破**：准确率均低于 17%（但这些防御开销过高，不实用）
4. **非对称 collision 下 W-T 安全性下降**：如客户端不遵守对称 collision 规则，DF 准确率升至 87.2%
5. **数据时效性问题**：WF 攻击准确率在 10-14 天后显著下降

## 7. 学习与应用（开源情况、复现步骤、超参数、迁移价值、启发）

### 开源情况

代码和数据已开源：https://github.com/deep-fingerprinting/df

### 复现步骤

1. 使用 tor-browser-crawler 抓取 Tor 流量数据
2. 将流量 trace 转换为 packet direction 序列（+1/-1）
3. 截断/填充至 5000 cells
4. 按 Table 1 超参数构建 DF 模型（Keras + TensorFlow）
5. 8:1:1 划分数据集，训练 30 epochs

### 关键超参数

| 超参数 | 值 | 说明 |
|--------|----|------|
| 输入维度 | 5000 | 经搜索 [500, 7000] 确定 |
| Optimizer | Adamax | 优于 Adam, RMSProp, SGD |
| Learning Rate | 0.002 | |
| Batch Size | 128 | |
| Conv 层数 | 8（4 Blocks x 2） | |
| 滤波器 | [32,32], [64,64], [128,128], [256,256] | 逐层递增 |
| FC 层 | 2 层，各 512 units | |
| Dropout | Pooling 后 0.1, FC1 后 0.7, FC2 后 0.5 | |

### 迁移价值

1. **超参数迁移性**：论文利用 neural network 的 transferability 属性，从无防御场景的超参数迁移到防御场景，仅需微调
2. **架构设计思路可迁移**：Block 设计、ELU/ReLU 组合、BN + Dropout 策略可应用于其他 traffic analysis 任务
3. **1D CNN 适用于序列数据**：该方法可推广到其他加密流量分析任务

### 启发

1. **深度很重要**：DF (8 Conv) 显著优于 AWF (3 Conv)，说明更深的网络在 WF 中更有效
2. **激活函数选择需考虑数据特性**：不能盲目套用图像领域的 ReLU，需根据输入数据特点选择
3. **防御评估需用大样本**：WTF-PAD 在小样本评估中表现良好，但在大样本下被 DF 攻破
4. **对称 collision 是 W-T 的关键安全保证**

## 8. 总结

**核心思想（<=20字）：** 深层 CNN 自动提取流量特征，攻破 WTF-PAD 防御。

**速记 Pipeline（3-5步）：**
1. 抓取 Tor 流量，提取 packet direction 序列
2. 截断/填充至 5000 cells
3. 输入 8 层 Conv1D 网络（ELU+ReLU, BN, Dropout）
4. 2 层 FC + Softmax 输出分类
5. 闭世界 98.3%，WTF-PAD 90.7%

## 9. Obsidian 知识链接

### 相关概念
- Website Fingerprinting
- Traffic Analysis
- Tor Anonymity Network
- Convolutional Neural Network
- Deep Learning

### 相关防御方法
- WTF-PAD
- Walkie-Talkie
- BuFLO
- Tamaraw
- Adaptive Padding

### 相关攻击方法
- k-NN WF Attack
- CUMUL Attack
- k-Fingerprinting
- AWF - Automated Website Fingerprinting
- SDAE - Stacked Denoising Autoencoder

### 相关技术
- ELU Activation Function
- Batch Normalization
- Dropout Regularization
- Transferability in Neural Networks

### 对比表
- WF Attack Comparison Table
- WF Defense Comparison Table

## 10. 证据记录（表格）

| 编号 | 证据内容 | 出处位置 | 备注 |
|------|----------|----------|------|
| E1 | DF 闭世界无防御准确率 98.3% | Table 2 | 所有方法中最高 |
| E2 | DF 对 WTF-PAD 闭世界准确率 90.7% | Table 3 | 远超第二名 k-FP 的 69.0% |
| E3 | DF 对 W-T 闭世界准确率 49.7% | Table 3 | 接近理论上限 50% |
| E4 | DF 开世界无防御 precision=0.99, recall=0.94 | Section 5.7 | |
| E5 | DF 开世界 WTF-PAD precision=0.96, recall=0.68 | Section 5.7 | 高 precision 设置 |
| E6 | 50 traces/site 即可达 90% 准确率 | Figure 5 | DF 和 CUMUL |
| E7 | 10 epochs 即达约 97% 测试准确率 | Figure 4 | 收敛速度快 |
| E8 | Top-2 prediction 对 W-T 准确率 98.44% | Section 5.8 | DF 能识别真实站点和 decoy |
| E9 | 非对称 collision 下 DF 对 W-T 准确率 87.2% | Section 5.8 | 对称 collision 是 W-T 安全关键 |
| E10 | 训练-测试误差差异 <2% | Section 5.2 | 无明显过拟合 |
| E11 | GPU 训练时间 64 分钟（30 epochs） | Section 5.5 | GTX 1070 |
| E12 | WTF-PAD 带宽开销 64%，W-T 带宽 31% + 延迟 34% | Table 3 | |

## 11. 原始资料链接

- 论文 PDF: https://dl.acm.org/doi/10.1145/3243734.3243768
- 代码仓库: https://github.com/deep-fingerprinting/df
- 本地 PDF: `00-inbox/PDFs/2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning.pdf`
- 本地 Markdown: `02-parsed-markdown/2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning.md`

## 12. 后续问题

1. DF 的 1D CNN 架构能否进一步加深（如 16 层 Conv）以提升对 WTF-PAD 的攻击效果？
2. 如何设计能抵抗深层 CNN 攻击的 WF 防御？对抗机器学习（adversarial ML）方向是否可行？
3. Walkie-Talkie 的对称 collision 机制在实际部署中能否真正保证？半双工带来的延迟开销是否可接受？
4. DF 模型在不同时间段采集的数据上表现如何？数据时效性问题（10-14 天后准确率下降）如何缓解？
5. 将 packet size 和 timing 信息重新引入输入是否能进一步提升 DF 的性能？
6. DF 架构能否迁移到其他 traffic analysis 任务（如 encrypted video stream identification）？
7. 开世界场景中，如何进一步提升 DF 对 WTF-PAD 的 recall？是否需要更复杂的二分类策略？
8. 对抗样本（adversarial examples）能否用于生成有效的 WF 防御流量？

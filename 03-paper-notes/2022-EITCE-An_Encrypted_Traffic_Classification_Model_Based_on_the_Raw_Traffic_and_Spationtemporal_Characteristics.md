---
type: paper
title_original: "An Encrypted Traffic Classification Model Based on the Raw Traffic and Spatiotemporal Characteristics"
title_cn: "基于原始流量和时空特征的加密流量分类模型"
authors:
  - Guanglong Zhao
  - Zhen Wang
  - Ziheng Yang
year: 2022
venue: "EITCE 2022 (6th International Conference on Electronic Information Technology and Computer Engineering)"
doi: "10.1145/3573428.3573644"
url: "https://doi.org/10.1145/3573428.3573644"
pdf: "00-inbox/PDFs/2022-EITCE-An_Encrypted_Traffic_Classification_Model_Based_on_the_Raw_Traffic_and_Spationtemporal_Characteristics.pdf"
mineru_md: "02-parsed-markdown/2022-EITCE-An_Encrypted_Traffic_Classification_Model_Based_on_the_Raw_Traffic_and_Spationtemporal_Characteristics.md"
status: processed
reading_level: L2
research_area: "Encrypted Traffic Classification"
task: "加密流量分类（12类，含VPN与Non-VPN）"
method: "ResNet-GRU并行融合模型"
dataset: "ISCX-VPN-NonVPN2016"
code: null
relevance: "中等——提出并行时空特征提取思路，但实验规模和对比有限"
created: "2026-05-27"
updated: "2026-05-27"
tags:
  - traffic-classification
  - deep-learning
  - ResNet
  - GRU
  - encrypted-traffic
  - spatiotemporal-features
---

# An Encrypted Traffic Classification Model Based on the Raw Traffic and Spatiotemporal Characteristics

## 0. 基础信息

| 字段 | 内容 |
|------|------|
| 论文全称 | An Encrypted Traffic Classification Model Based on the Raw Traffic and Spatiotemporal Characteristics |
| 作者 | Guanglong Zhao, Zhen Wang, Ziheng Yang (通讯作者) |
| 机构 | 黑龙江大学电子工程学院 |
| 发表年份 | 2022 |
| 会议/期刊 | EITCE 2022 (6th International Conference on Electronic Information Technology and Computer Engineering) |
| DOI | 10.1145/3573428.3573644 |
| 关键词 | Encrypted Traffic Classification, Deep Learning, ResNet, GRU, Spatiotemporal Features |

## 1. 一句话总结

提出一种基于原始网络流量的 ResNet-GRU 并行融合模型，通过 ResNet 提取空间特征、GRU 提取时序特征后进行特征融合分类，在 ISCX-VPN-NonVPN2016 数据集上 12 类加密流量分类达到 99.36% 准确率。

## 2. 摘要翻译

深度学习技术在加密流量分类中被频繁使用并取得了有效成果。在当前的加密流量分类过程中，网络流量特征提取不够充分，这是一个值得关注的问题。本文提出了一种基于原始网络流量及其时空特征的加密流量分类模型。首先将原始网络流量划分为 session，然后将每个 session 中的数据包分割为 784 字节的切片，用切片数据描述流量。然后，结合 ResNet 和 GRU 模型并行地从原始网络数据中生成特征，分别构建时间特征向量和空间特征向量。最后使用融合特征进行流量分类。实验结果表明，所提模型在 ISCX-NonVPN-VPN2016 数据集上的识别准确率达到了 99.36%，优于现有其他方法。

## 3. 方法动机（Motivation）

### 问题背景

- 互联网中超过 90% 的流量为加密流量，恶意软件可通过加密流量隐藏攻击特征，逃避传统入侵检测机制
- 传统流量分类依赖人工设计的统计特征（如 flow duration、单位时间流量大小等），特征设计与流量类别相关，面对新流量场景可能需要重新设计特征，且存在对原始流量表征不充分的问题

### 现有方法的不足

- **传统机器学习方法**：需要手动提取特征（如 Gil 等人使用时间特征 + C4.5/KNN，Yamansavascular 等人使用 111 个特征 + KNN 达到 93.94%），泛化能力有限
- **Deep Packet (Lotfollahi et al.)**：使用 SAE + 1D-CNN 提取前 1500 字节特征，但忽略了流量的时间序列特征
- **1D-CNN (Wang et al.)**：仅使用 784 字节输入 + 1D-CNN，在 ISCX 数据集上准确率仅 85.8%，特征提取单一
- **CNN+LSTM (Zou et al.)**：采用串行结构，LSTM 的输入是 CNN 提取的空间特征向量而非原始流量，相当于对特征再次提取，未能直接从原始流量中学习时序信息

### 核心动机

现有方法在特征提取上不够充分：要么只提取空间特征、要么只提取时序特征、要么串行处理导致信息损失。需要一种能够同时从原始流量中并行提取空间和时序特征的方法。

## 4. 方法设计（Methodology）

### 4.1 整体架构

模型分为三个模块：数据预处理模块 -> 时空特征提取模块 -> 识别分类模块。核心思路是用 ResNet 和 GRU **并行**提取原始流量的空间特征和时序特征，然后融合后进行分类。

### 4.2 数据预处理模块

预处理包含三个步骤：

**Step 1: 原始流量分割（Traffic Split）**
- 原始流量以 pcap 文件存储，按五元组（源IP、目的IP、源端口、目的端口、传输层协议）将连续的网络流量流分割为离散的 session 单元
- 分割后的 session 存储为新的 pcap 文件

**Step 2: 流量清洗（Traffic Cleaning）**
- 去除重复流量
- 将 MAC 地址和 IP 地址替换为 0x00，避免模型因数据集中固定的主机地址信息产生偏差（防止模型通过 MAC/IP 地址分类导致过拟合）

**Step 3: 流量切片（Traffic Slicing）**
- 截取每个数据包的协议层数据，取前 N 字节（N=784）
- 若流量字节长度小于 784，则用 0x00 填充；若大于 784，则截断 784 字节之后的数据
- 切片前需去除 pcap 文件头信息

### 4.3 时空特征提取模块

**ResNet 分支（空间特征提取）**
- 使用 ResNet-18 结构，包含 4 个 ResLayer，每个 ResLayer 由 2 个 ResBlock 组成
- 利用残差结构增加网络深度，避免梯度爆炸问题
- 输出 256 维空间特征向量
- 关键层参数：Conv1d -> BatchNorm1d -> ResLayer1(784) -> ResLayer2(392) -> ResLayer3(196) -> ResLayer4(98) -> AvgPooling -> 256维向量

**GRU 分支（时序特征提取）**
- 使用 64 个隐藏层，1 个 GRU 结构
- GRU 相比 LSTM 结构更简单（仅含更新门和重置门），参数量更少，训练速度更快
- 利用 GRU 的记忆特性，适合提取网络流量中隐含的时序特征
- 输出 64 维时序特征向量

### 4.4 识别分类模块

- 将 ResNet 输出的 256 维空间特征向量和 GRU 输出的 64 维时序特征向量拼接融合
- 融合特征通过全连接层：FC1(32100, 输出100维) -> FC2(3030, 输出30维) -> FC3(372, 输出12维)
- 最终通过 Softmax 分类器输出 12 类流量标签
- 整个模型通过反向传播更新所有参数，ResNet 和 GRU 网络分别进行反向传播

## 5. 方法对比

| 对比维度 | CNN1D [Wang] | CNN+LSTM [Zou] | CENTIME [Wang Maonan] | 本文 (ResNet-GRU) |
|----------|-------------|----------------|----------------------|-------------------|
| 特征类型 | 仅空间特征 | 空间特征(串行) | 空间特征+统计特征 | 空间+时序特征(并行) |
| 特征提取方式 | 1D-CNN | CNN提取空间后送入LSTM | ResNet+SAE | ResNet+GRU并行 |
| 输入信息利用 | 原始流量 | CNN特征(非原始流量) | 原始流量+人工统计特征 | 原始流量 |
| 是否考虑时序 | 否 | 是(但间接) | 否 | 是(直接) |
| Acc | 0.9617 | 0.9931 | 0.9918 | **0.9936** |

**本文优势分析：**
- CNN1D 仅提取空间特征，特征提取单一
- CNN+LSTM 采用串行结构，LSTM 输入的是 CNN 提取的特征而非原始流量，相当于对特征的二次提取，而非直接从原始流量学习时序信息
- CENTIME 虽然结合了 ResNet 和 SAE，但人工统计特征对流量的刻画较为片面
- 本文并行地从原始流量中提取空间和时序特征，对原始流量的学习更全面

## 6. 实验表现

### 6.1 实验环境

- 平台：Google Colab（Tesla T4 GPU，14G 显存，12G RAM）
- 框架：PyTorch 1.12.1+cu113，Python 3.7
- 训练参数：batch_size=128, epoch=150, learning_rate=0.001, 损失函数=交叉熵, 优化器=Adam

### 6.2 数据集

ISCX-VPN-NonVPN2016 公开数据集，去除模糊标签后保留 12 类流量（6类非VPN + 6类VPN）：

| 流量类别 | 包含内容 | 文件大小 |
|---------|---------|---------|
| Email | Email, Gmail | 13MB |
| VPN-Email | - | 7.8MB |
| Chat | ICQ, AIM, Skype, Facebook, Hangouts | 29.5MB |
| VPN-Chat | - | 27.6MB |
| Streaming | Vimeo, Youtube, Netflix, Spotify | 1.53GB |
| VPN-Streaming | - | 1.37GB |
| File_transfer | Skype, FTPS, SFTP | 17.3GB |
| VPN-File_transfer | - | 279MB |
| VoIP | Facebook, Skype, Hangouts, Voipbuster | 4.48GB |
| VPN-VoIP | - | 360MB |
| P2P | uTorrent, Bittorrent | 96.8MB |
| VPN-P2P | - | 358MB |

### 6.3 评估指标

使用 Accuracy、Precision、Recall、F1-score 四个指标评估模型性能。

### 6.4 核心实验结果

**基线模型对比（Table 4）：**

| 模型 | Acc | Pr | Re | F1 |
|------|-----|-----|-----|-----|
| ResNet（仅空间特征） | 0.9904 | 0.9904 | 0.9904 | 0.9904 |
| GRU（仅时序特征） | 0.7615 | 0.7544 | 0.7615 | 0.7278 |
| **ResNet-GRU（融合模型）** | **0.9936** | **0.9937** | **0.9936** | **0.9936** |

- 相比 ResNet 基线，准确率提升 0.32%
- 相比 GRU 基线，准确率提升 23.21%
- 说明时空特征融合能更充分地提取原始流量信息

**与已有方法对比（Figure 4）：**

| 方法 | Acc | Pr | Re | F1 |
|------|-----|-----|-----|-----|
| CNN1D [8] | 0.9617 | 0.9620 | 0.9617 | 0.9618 |
| CNN+LSTM [9] | 0.9931 | 0.9930 | 0.9931 | 0.9930 |
| CENTIME [10] | 0.9918 | 0.9918 | 0.9918 | 0.9918 |
| **本文** | **0.9936** | **0.9937** | **0.9936** | **0.9936** |

**混淆矩阵分析：**
- 12 类流量中，大部分识别准确率大于 93%
- 最低的类别准确率为 93%（推测为某类 VPN 流量），最高为 100%

## 7. 学习与应用

### 7.1 方法创新点

1. **并行特征提取**：ResNet 和 GRU 并行处理原始流量，分别提取空间和时序特征，避免了串行结构（如 CNN+LSTM）中对特征二次提取导致的信息损失
2. **端到端原始流量处理**：直接使用 784 字节切片作为输入，无需人工设计特征
3. **隐私保护预处理**：将 MAC/IP 地址替换为 0x00，防止模型过拟合到特定主机地址

### 7.2 方法局限性

1. **单数据集验证**：仅在 ISCX-VPN-NonVPN2016 一个数据集上验证，泛化能力未得到充分验证
2. **固定长度截断**：784 字节的固定截断可能丢失长流量的重要信息，或对短流量引入过多填充噪声
3. **分类粒度**：仅支持 12 类粗粒度分类，未涉及 application-level 或 fine-grained 分类
4. **GRU 性能较低**：单独 GRU 模型准确率仅 76.15%，说明 784 字节的原始字节序列作为时序输入效果有限，时序特征提取能力有提升空间
5. **缺乏代码开源**：未提供源代码

### 7.3 可借鉴的技术思路

- 并行多分支特征提取架构（空间 + 时序）可以应用于其他序列分类任务
- 流量预处理中地址替换为 0x00 的做法值得在其他数据集实验中采用
- 784 字节切片策略在多篇论文中被验证为有效，可作为标准预处理方案

## 8. 总结

本文提出了一种基于原始网络流量的 ResNet-GRU 并行融合加密流量分类模型。核心贡献在于：(1) 使用原始流量字节作为输入，避免人工特征设计；(2) 通过 ResNet 和 GRU 并行提取空间和时序特征，较串行方法更充分利用原始流量信息；(3) 在 ISCX-VPN-NonVPN2016 数据集上达到 99.36% 的分类准确率。论文的主要不足是实验验证较为简单（单数据集、少量对比方法），且 GRU 单独表现较差，融合带来的提升主要来自 ResNet 的空间特征。

## 9. 知识链接

### 相关数据集
- ISCX-VPN-NonVPN2016 — 本文使用的数据集，由 UNB ISCX 实验室发布，包含 14 类加密流量（VPN + Non-VPN）

### 相关方法引用
- Deep_Packet [Lotfollahi et al., 2020] — 使用 SAE + 1D-CNN 进行加密流量分类，本文的对比基线之一
- 1D-CNN_Traffic_Classification [Wang et al., 2017] — 使用 784 字节输入 + 1D-CNN，本文的对比基线之一
- CNN-LSTM_Traffic_Classification [Zou et al., 2018] — CNN+LSTM 串行架构，本文的对比基线之一
- CENTIME [Wang Maonan et al., 2020] — ResNet + SAE 框架，本文的对比基线之一

### 方法类别
- 本论文属于 **并行多分支特征融合** 方法，与以下方法类别相关：
  - 串行级联方法（如 CNN+LSTM）
  - 单分支方法（如 1D-CNN、ResNet）
  - 多模态融合方法

## 10. 证据记录

### 关键数据点
- 99.36% — 本文模型在 VPN2016 数据集上的分类准确率
- 99.04% — ResNet 单独使用的分类准确率（仅空间特征）
- 76.15% — GRU 单独使用的分类准确率（仅时序特征），说明原始字节级时序特征提取效果较差
- 0.32% — 相比 ResNet 基线的准确率提升幅度（较小）
- 23.21% — 相比 GRU 基线的准确率提升幅度（较大，但主要因为 GRU 基线本身表现差）
- 784 字节 — 流量切片长度，参考自 [Wang et al., 2017]
- 12 类 — 最终分类类别数（去除模糊标签后从14类减少到12类）

### 重要引用
- [3] Draper-Gil et al., 2016 — ISCX-VPN-NonVPN2016 数据集的发布论文
- [7] Lotfollahi et al., 2020 — Deep Packet，SAE + 1D-CNN 方案
- [8] Wang et al., 2017 — 1D-CNN 方案，784 字节输入的来源
- [9] Zou et al., 2018 — CNN+LSTM 串行方案
- [10] Wang Maonan et al., 2020 — CENTIME 框架

## 11. 原始资料链接

| 资料 | 路径 |
|------|------|
| PDF | `00-inbox/PDFs/2022-EITCE-An_Encrypted_Traffic_Classification_Model_Based_on_the_Raw_Traffic_and_Spationtemporal_Characteristics.pdf` |
| MinerU Markdown | `02-parsed-markdown/2022-EITCE-An_Encrypted_Traffic_Classification_Model_Based_on_the_Raw_Traffic_and_Spationtemporal_Characteristics.md` |
| DOI 链接 | https://doi.org/10.1145/3573428.3573644 |

## 12. 后续问题

1. 如果将 GRU 替换为 Transformer 或 Temporal Convolutional Network (TCN)，时序特征提取效果是否会显著提升？
2. 并行融合 vs 串行融合（如 CNN+LSTM）在更大规模数据集和更多分类类别上是否仍有优势？
3. 784 字节的固定切片长度是否是最优选择？不同长度对分类性能的影响如何？
4. 该方法在不同网络环境（如不同加密协议、不同流量负载）下的泛化能力如何？
5. 能否将空间特征分支替换为更轻量的网络（如 MobileNet），在保持性能的同时降低计算开销？

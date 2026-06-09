---
type: paper
title_original: "Identification of Encrypted Traffic Through Attention Mechanism Based Long Short Term Memory"
title_cn: "基于注意力机制长短期记忆网络的加密流量识别"
authors:
  - Haipeng Yao
  - Chong Liu
  - Peiying Zhang
  - Sheng Wu
  - Chunxiao Jiang
  - Shui Yu
year: 2022
venue: "IEEE Transactions on Big Data"
doi: "10.1109/TBDATA.2019.2940675"
url: ""
pdf: "00-inbox/PDFs/2022-TBD-Identification_of_Encrypted_Traffic_Through_Attention_Mechanism_Based_Long_Short_Term_Memory.pdf"
mineru_md: "02-parsed-markdown/2022-TBD-Identification_of_Encrypted_Traffic_Through_Attention_Mechanism_Based_Long_Short_Term_Memory.md"
status: processed
reading_level: L2
dataset:
  - ISCX-VPN-NonVPN
code: "unknown"
relevance: high
research_area: ["加密流量分类", "注意力机制", "深度学习"]
task: ["加密流量识别", "流量分类"]
method: ["attention-based LSTM", "Bi-LSTM", "cost-sensitive learning"]
created: "2026-05-27"
updated: "2026-05-29"
---

# 0. 元信息

- **标题**: Identification of Encrypted Traffic Through Attention Mechanism Based Long Short Term Memory
- **作者**: Haipeng Yao, Chong Liu, Peiying Zhang, Sheng Wu, Chunxiao Jiang, Shui Yu
- **机构**: 北京邮电大学、中国石油大学（华东）、清华大学、悉尼科技大学
- **期刊**: IEEE Transactions on Big Data (TBD)
- **发表时间**: 2019年9月投稿接收，2022年1月最终版本
- **DOI**: 10.1109/TBDATA.2019.2940675

# 1. 研究动机与问题定义

## 1.1 研究背景

随着数据传输和用户隐私保护需求的增长，越来越多的网络流量采用加密方式传输（如 SSH、VPN、SSL、加密 P2P、VoIP 等）。不同加密算法作用于不同协议层（传输层或应用层），使得 encrypted traffic 分类面临巨大挑战。

## 1.2 现有方法的不足

- **基于端口的方法**：依赖 IANA 标准端口号，但许多协议不遵循标准（如 P2P 使用随机端口，HTTP 使用 80 端口伪装），对加密流量分类失效。
- **Deep Packet Inspection (DPI)**：通过正则表达式匹配 payload，但加密后 payload 数据改变，只能识别粗粒度协议（如 SSL），无法有效识别 encrypted traffic。
- **传统机器学习方法**：需人工提取统计特征（流持续时间、包数量、包长度、字节数、包到达间隔等），依赖先验知识，耗时且无法保证特征的有效性。
- **已有深度学习方法**：多采用 CNN 提取特征，未考虑不同数据包之间的时序特征。

## 1.3 核心研究问题

如何利用深度学习模型自动学习 encrypted traffic 的时序特征，避免复杂的特征工程，并引入 attention mechanism 提升分类精度？

# 2. 主要贡献

1. **将网络流量视为时间序列数据**：以文本数据的方式分析流量，确定最佳流量表示方式（每条流 10 个包，每个包 1500 字节）。
2. **提出两种基于 attention mechanism 的分类模型**：Attention-based LSTM 关注流量中重要的数据包；Hierarchical Attention Network (HAN) 能区分每个包中不同字节的角色。
3. **实验验证**：基于 ISCX VPN-NonVPN 数据集，分类准确率达 91.2%，优于对比方法的最高 89.8%。

# 3. 相关工作

## 3.1 基于机器学习的加密流量分类

- **特征提取方向**：Alshammari 等提取 22 个流特征区分 SSH 和 Skype；Scherrer 等使用非高斯方法和长记忆统计特征；Santos 等提出基于时间序列的 HTTP 分类方法。
- **分类器方向**：C4.5 决策树、SVM、GMM、KNN、Random Forest、MOGA 等多种分类器被应用于加密流量分类。
- **数据集**：ISCX VPN-NonVPN、ISCX Tor-NonTor、Anon17 等。
- **核心问题**：特征选择需要领域先验知识，迁移到新场景困难。

## 3.2 基于深度学习的加密流量分类

- **SAE**: Wang (2015) 首次将深度学习用于流量识别。
- **Deep Packet**: SAE + 两层 CNN，应用分类 F1 达 95%。
- **One-dim CNN**: 将流量表示为图片，应用分类 F1 为 86.6%。
- **CNN+RNN 融合**: Lopez 等整合 CNN 和 RNN，F1 达 95%。
- **BSNN**: 使用 attention encoder 进行协议分类，F1 达 95.8%。
- **本文与 BSNN 的区别**：BSNN 输入为单个数据包（按字节段划分），本文输入为整个流量流（填充为统一维度矩阵并归一化到 [0,1]）。

# 4. 方法论

## 4.1 数据集

使用 **ISCX VPN-NonVPN 数据集**，包含两级分类任务：
- 第一级：协议类型识别（chat、email 等）
- 第二级：应用类型识别（Facebook、Skype 等）

本文从协议类型角度进行分类，包含 6 种 NonVPN 数据和 6 种 VPN 数据。原始数据约 35GB，在 Hadoop 平台上预处理后约 1GB。

## 4.2 数据预处理

### 4.2.1 流量分割

- 使用**五元组**（源 IP、目的 IP、源端口、目的端口、传输层协议）标识流量流
- 将源到目标和目标到源的包合并为**双向流（bi-flow）**
- 使用 SplitCap 工具将 pcap 文件分割为双向流
- 数据类别分布不均衡，采用 cost-sensitive learning 缓解

### 4.2.2 去除无关字段与数据归一化

- 删除数据链路层信息和 IP 地址（避免固定采集 IP 地址引入外部信息偏差）
- 每个字节（8 位）表示为 [0, 255] 的十进制数，归一化到 [0, 1]

### 4.2.3 时间序列表示

- 流量表示为 N x M 维矩阵：N 为流中数据包数量，M 为每个包的字节数
- 包长度不足 M 则补零，超过则截断保留前 M 字节
- 通过数据分布可视化确定最优 N 和 M

### 4.2.4 数据集划分

- 采用 **10-fold cross-validation**
- 训练:验证:测试 = 8:1:1
- VPN 训练集 15,545 条，NonVPN 训练集 22,706 条
- VPN 验证/测试集各 1,943 条，NonVPN 验证/测试集各 2,838 条

## 4.3 LSTM 基础

由于流量数据序列很长（每个包 1500 字节），使用 LSTM 替代原始 RNN。LSTM 通过三个门控函数控制信息流：

- **Forget gate** (遗忘门)：控制上一时刻细胞状态 C_{t-1} 中保留多少信息
- **Input gate** (输入门)：决定当前输入 x_t 中多少信息加入细胞状态
- **Output gate** (输出门)：控制细胞状态 C_t 的输出

关键公式：
- f_t = sigma(W_f * [h_{t-1}, x_t] + b_f)
- i_t = sigma(W_i * [h_{t-1}, x_t] + b_i)
- C_t = f_t * C_{t-1} + i_t * ~C_t
- o_t = sigma(W_o * [h_{t-1}, x_t] + b_o)
- h_t = o_t * tanh(C_t)

## 4.4 Attention Mechanism

采用 Bahdanau attention mechanism 计算所有隐藏向量的权重：

- u_i = tanh(W_p * h_i + b_p)：计算每个包的重要性分数
- alpha_i = exp(u_i^T * u_s) / Sigma_j exp(u_j^T * u_s)：归一化权重
- c = Sigma_i alpha_i * h_i：加权求和得到中间向量

## 4.5 Attention-based LSTM 模型

- 每个数据包 P_i 通过 **Bi-LSTM** 编码为输入向量
- 前向隐藏状态 h_i-> 和后向隐藏状态 h_i<- 拼接为上下文向量 h_i
- h_i 包含前后数据包的信息
- 使用 attention mechanism 计算 h_i 的权重，加权求和得到流量流的编码向量 c
- c 经全连接层和 softmax 层输出分类结果

## 4.6 HAN (Hierarchical Attention Network) 架构

受文本分类领域 HAN 启发，采用两层 LSTM 网络：

- **第一层（字节级）**：以每个字节 b_j 为输入，Bi-LSTM 编码后用 attention mechanism 计算字节权重，加权求和得到向量 p_i 表示每个包的信息
- **第二层（包级）**：以 p_i 为输入，Bi-LSTM 编码后用 attention mechanism 计算包权重，加权求和得到流量流的表示向量 F
- 区别于 Attention-based LSTM：HAN 能区分包中不同字节的角色

## 4.7 输出层与损失函数

- 编码向量 c 经全连接层（dropout = 0.8）到 softmax 层得到概率
- 使用 **cost-sensitive learning** 处理类别不平衡问题
- 损失函数：delta_{n,k} = ln(1 + exp(z_{n,k} * (r_k(x_n) - c_n[k])))
  - 优势：光滑可微，可直接用于神经网络反向传播
- 目标函数：L(theta) = Sigma_n Sigma_k delta_{n,k}

# 5. 实验设置

## 5.1 实验环境

- Ubuntu 14.04, TensorFlow 1.4.0, Python 2.7, NVIDIA 1080Ti, 16GB 内存
- Dropout: 0.8；优化器: Adam（学习率 0.001）；激活函数: ReLU
- Batch size: 64；训练 30 epochs
- Attention-based LSTM: lstm_size=100, hidden_size=128
- HAN: 两层 LSTM 的 lstm_size 均为 128, hidden_size=128
- 基于 TensorFlow 的分布式训练以减少训练时间

## 5.2 评估指标

- **Accuracy (acc)**: 整体分类准确率
- **Precision (P_c)**: 每个类别的精确率
- **Recall (R_c)**: 每个类别的召回率
- **F1 score (F1_c)**: 每个类别的 F1 值

## 5.3 对比实验场景

| 实验 | 描述 | 类别数 |
|------|------|--------|
| Exp 1 | 协议封装流量识别（VPN vs NonVPN） | 2 类 |
| Exp 2 | 常规加密流量分类 | 6 类（VPN） |
| Exp 3 | 协议封装流量分类 | 6 类（NonVPN） |
| Exp 4 | 加密流量分类 | 12 类 |

# 6. 实验结果

## 6.1 数据处理方式的影响

- **去除 DNS 流量**：DNS 用于主机名解析，与主机紧密相关，容易识别但会带来偏差，应去除
- **使用全部数据 vs 仅 L7 数据**：全部数据（去除链路层和 IP 后）比仅 L7 数据准确率高 2-3%，因为包含传输层和部分网络层信息（端口号、包长度等）

## 6.2 最优流量表示

- N（包数量）取值范围：[5, 10, 20]
- M（字节数）取值范围：[500, 1000, 1500]
- **最优组合：N=10, M=1500**，准确率最高

## 6.3 模型性能对比

| 模型 | Exp 1 | Exp 2 | Exp 3 | Exp 4 |
|------|-------|-------|-------|-------|
| **Attention-based LSTM** | **0.997** | **0.893** | **0.948** | **0.912** |
| HAN | 0.995 | 0.851 | 0.929 | 0.895 |
| Deep Packet | 0.992 | 0.868 | 0.923 | 0.898 |
| One-dim CNN | 0.990 | 0.818 | 0.986 | 0.866 |
| C4.5 Decision Tree | 0.900 | 0.890 | 0.870 | 0.800 |
| XGBoost | 0.991 | 0.841 | 0.918 | 0.864 |

**核心发现**：
- Attention-based LSTM 在 Exp 1、3、4 中均取得最佳结果
- 12 类分类（Exp 4）中，Attention-based LSTM 比 One-dim CNN 提升约 5%，在 NonVPN 上提升近 7%
- HAN 整体性能不如 Attention-based LSTM，但在 Exp 1 和 Exp 4 中仍优于 One-dim CNN 和 Decision Tree
- VPN 流量因加密后分布差异明显，比 NonVPN 更容易分类

## 6.4 训练效率

| 模型 | 单 batch 时间 | 总时间 |
|------|-------------|--------|
| Attention-based LSTM | 0.05s | 1783.6s |
| HAN | 1.48s | 53149s |
| Deep Packet | 0.1s | 3600s |
| One-dim CNN | 0.02s | 720s |
| XGBoost | - | 300s |

HAN 耗时最长，主要因为第一层 LSTM 序列过长（字节级处理）。

## 6.5 Attention 权重可视化

- 注意力主要集中在**前 4 个数据包**，因为前几个包携带更多协议相关信息（如 TCP 三次握手）
- 流末尾的包（streaming、torrent、file 协议除外）几乎不贡献分类特征
- 重要字节集中在**数据包头部**，因为包含类别信息的字节通常位于包头

# 7. 方法优势分析

1. **时序建模能力**：将流量视为时间序列，LSTM 能学习相邻包之间的关系，每个隐藏层状态记录所有先前包的信息，捕捉长期依赖关系
2. **Attention 增强**：对所有历史状态信息进行加权求和作为最终编码向量，比仅使用最后一个隐藏层向量包含更多信息
3. **自动特征学习**：避免了传统方法中复杂的特征工程

# 8. 局限性与不足

- HAN 计算开销大（第一层 LSTM 序列过长），训练时间远高于其他模型
- 对 chat 和 email 等短流量、交互频繁的协议分类效果较差（数据分布差异大）
- Attention-based LSTM 在 streaming 和 VoIP 类别上的 precision 低于 One-dim CNN（流量过大，LSTM 难以学习长期关系）
- 仅使用单一 RNN 架构，未结合 CNN 的空间特征提取能力

# 9. 未来工作方向

1. **构建更复杂的混合模型**：CNN + RNN 融合模型，CNN 提取流量特征，RNN 学习时序特征
2. **尝试不同的 attention mechanism**：包括 hard attention 和 local attention
3. **提出更适合深度学习方法的新数据集**

# 10. 关键技术总结

| 技术要素 | 具体方案 |
|----------|----------|
| 流量表示 | N x M 矩阵（N=10 packets, M=1500 bytes），归一化到 [0,1] |
| 特征提取 | Bi-LSTM 编码时序特征 |
| 注意力机制 | Bahdanau attention，计算包/字节级权重 |
| 类别不平衡 | Cost-sensitive learning |
| 正则化 | Dropout (0.8) |
| 优化器 | Adam (lr=0.001) |
| 验证策略 | 10-fold cross-validation, 8:1:1 划分 |
| 大数据处理 | Hadoop 平台预处理, TensorFlow 分布式训练 |

# 11. 对本研究方向的启发

- **流量的时间序列表示**是可行的，将原始字节数据直接作为输入避免了特征工程的局限性
- **Attention mechanism 在流量分类中有效**，能自动学习不同包和字节的重要性，且具有可解释性（可视化注意力权重）
- **分层注意力结构（HAN）**理论上更精细，但实际效果和效率不如单层 attention-based LSTM，提示模型复杂度需与任务匹配
- **数据预处理对结果影响显著**：是否去除 DNS、使用全部数据还是仅 L7、N 和 M 的选择都会显著影响分类性能
- **ISCX VPN-NonVPN 数据集**是该领域的重要 benchmark，便于方法间横向比较

# 12. 参考价值与阅读笔记

- **适用场景**：encrypted traffic 的协议类型和应用类型分类，特别是 VPN 流量识别
- **核心创新点**：将 attention mechanism 引入 LSTM 进行流量分类，提出 attention-based LSTM 和 HAN 两种架构
- **与后续工作的关联**：本文的方法为后续基于 Transformer 的流量分类方法奠定了基础，attention mechanism 已成为流量分类领域的标准组件
- **实验可复现性**：使用公开数据集（ISCX VPN-NonVPN），超参数设置明确，代码基于 TensorFlow 实现
- **关键引用**：
  - [7] Deep Packet（SAE + CNN 基线）
  - [8] One-dim CNN（一维卷积基线）
  - [27] ISCX VPN-NonVPN 数据集及 C4.5 决策树方法
  - [32] BSNN（最接近的对比工作）
  - [33] LSTM 原始论文
  - [34] Bahdanau attention mechanism
  - [35] HAN 原始论文

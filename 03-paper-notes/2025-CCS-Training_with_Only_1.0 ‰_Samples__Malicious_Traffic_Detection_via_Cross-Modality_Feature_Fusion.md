---
type: paper
title_original: "Training with Only 1.0 ‰ Samples: Malicious Traffic Detection via Cross-Modality Feature Fusion"
title_cn: "仅用千分之一样本训练：基于跨模态特征融合的恶意流量检测"
authors: ["Chuanpu Fu", "Qi Li", "Elisa Bertino", "Ke Xu"]
year: 2025
venue: "ACM CCS 2025"
doi: "10.1145/3719027.3765143"
url: "https://doi.org/10.1145/3719027.3765143"
pdf: "00-inbox/PDFs/2025-CCS-Training_with_Only_1.0 ‰_Samples__Malicious_Traffic_Detection_via_Cross-Modality_Feature_Fusion.pdf"
mineru_md: "02-parsed-markdown/2025-CCS-Training_with_Only_1.0 ‰_Samples__Malicious_Traffic_Detection_via_Cross-Modality_Feature_Fusion.md"
status: processed
reading_level: L1
research_area: ["network security", "malicious traffic detection", "machine learning"]
task: ["malicious traffic detection", "few-shot learning", "cross-domain detection"]
method: ["crossmodal attention", "contrastive learning", "AutoML", "time-aware positional encoding", "transformer"]
dataset: ["HyperVision", "CIC-IDS2017", "CIC-IDS2018", "CIC-DDoS2019", "CIC-Android", "CIC-IoT", "CIC-DoH", "CTU-13", "Whisper", "Kitsune", "NetBeacon", "MAWI"]
code: "https://github.com/fuchuanpu/TFusion"
relevance: high
created: "2026-05-27"
updated: "2026-05-27"
---

# Training with Only 1.0 ‰ Samples: Malicious Traffic Detection via Cross-Modality Feature Fusion

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Training with Only 1.0 ‰ Samples: Malicious Traffic Detection via Cross-Modality Feature Fusion |
| 中文标题 | 仅用千分之一样本训练：基于跨模态特征融合的恶意流量检测 |
| 作者 | Chuanpu Fu, Qi Li, Elisa Bertino, Ke Xu |
| 年份 | 2025 |
| 会议/期刊 | ACM SIGSAC Conference on Computer and Communications Security (CCS 2025) |
| 研究方向 | 网络安全、恶意流量检测、少样本学习 |
| 任务类型 | 在极小训练数据集下实现跨网络环境的恶意流量检测 |
| 方法关键词 | crossmodal attention, contrastive learning, AutoML, time-aware positional encoding, topology-driven pretraining |
| 数据集 | HyperVision, CIC-IDS2017/2018, CIC-DDoS2019, CIC-Android, CIC-IoT, CIC-DoH, CTU-13, Whisper, Kitsune, NetBeacon, MAWI（共11个公开数据集 + 1个机构网络部署） |
| 是否开源 | 是（https://github.com/fuchuanpu/TFusion） |
| PDF | 00-inbox/PDFs/2025-CCS-Training_with_Only_1.0 ‰_Samples__Malicious_Traffic_Detection_via_Cross-Modality_Feature_Fusion.pdf |
| MinerU Markdown | 02-parsed-markdown/2025-CCS-Training_with_Only_1.0 ‰_Samples__Malicious_Traffic_Detection_via_Cross-Modality_Feature_Fusion.md |

## 1. 一句话总结

> 将网络流量视为多模态数据（packet、flow、host），通过 crossmodal attention 融合不同粒度特征，并利用 topology-driven contrastive learning 在大规模无标注互联网流量上预训练，使得仅需标注千分之一的流量样本即可实现 99.82% 的恶意流量检测精度，超越 14 种现有方法 12.76% 以上。

## 2. 摘要翻译

### 2.1 摘要原文

Machine Learning (ML) based malicious traffic detection systems can accurately recognize unseen network attacks by learning from large-scale traffic datasets. However, deploying such systems across multiple networks involves substantial efforts to construct large training datasets for each network. This paper addresses the issue of training with minimal datasets, that is, achieving accurate malicious traffic detection by learning a small portion of traffic in entirely new network environments, thereby eliminating prohibitive labor costs associated with traffic dataset construction. We develop tFusion to effectively extract information from limited datasets by treating network traffic data as multimodal data, comprising features from multiple sensory modalities of packets, flows, and hosts. In particular, we design a dedicated crossmodal attention model that fuses fine-grained per-packet sequential features with coarse-grained per-flow and per-host statistical features, to synthesize correlations among the different granularities of traffic features. Moreover, we design a topology-driven contrastive learning approach that pretrains the models while reducing topology-related biases, which allows tFusion to achieve generic detection across various networks. We deploy tFusion in an institutional network and measure its performance over five days. tFusion requires human experts to label only 1.0 ‰ traffic, yet it achieves 99.82% accuracy when detecting various attacks. Meanwhile, it outperforms 14 existing methods by improving over 12.76% accuracy on 11 existing datasets.

### 2.2 摘要中文翻译

基于机器学习的恶意流量检测系统可以通过学习大规模流量数据集来准确识别未见过的网络攻击。然而，将此类系统部署到多个网络中需要为每个网络构建大规模训练数据集，这需要大量的工作量。本文研究最小化训练数据集的问题，即通过在全新网络环境中学习一小部分流量来实现准确的恶意流量检测，从而消除构建流量数据集所带来的高昂人力成本。我们开发了 tFusion，通过将网络流量数据视为多模态数据（包含来自 packet、flow 和 host 多种感知模态的特征），从有限数据集中有效提取信息。具体而言，我们设计了一个专用的 crossmodal attention 模型，将细粒度的 per-packet 序列特征与粗粒度的 per-flow 和 per-host 统计特征融合，以综合不同粒度流量特征之间的相关性。此外，我们设计了一种 topology-driven contrastive learning 方法，在预训练模型的同时减少拓扑相关的偏差，使 tFusion 能够在各种网络中实现通用检测。我们在一个机构网络中部署了 tFusion 并进行了五天的性能测量。tFusion 仅需人工专家标注千分之一的流量，即可在检测各种攻击时达到 99.82% 的准确率。同时，在 11 个现有数据集上，tFusion 比 14 种现有方法提高了 12.76% 以上的准确率。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 基于 ML 的恶意流量检测系统市场价值超过 36.4 亿美元，但扩展部署到新网络时需要为每个网络捕获和标注数百万个数据包，人力成本极高。这是一个**可扩展性瓶颈**：安全市场规模庞大但部署成本限制了保护范围
- 现有方法将流量视为单模态数据（unimodal data），仅分析单一粒度的特征（per-packet、per-flow 或 per-host），导致不同粒度特征之间信息无法综合，需要大规模训练数据集来弥补信息损失
- 多模态 AI 的成功（如 CLIP 联合文本与图像、语音识别综合声学与语言特征）启发作者将网络流量也视为多模态数据

### 3.2 为什么仅需 1‰ 样本就足够？——核心直觉

**为什么现有方法需要大量样本？** 从信息论角度，单模态特征空间中良性与恶意流量分布高度重叠（Figure 1(b)(c)），ML 模型需要大量样本来回归复杂的决策边界。论文给出了具体数据：单模态方法需要 O(10^4) ~ O(10^7) 的训练样本。

**为什么跨模态融合能大幅降低数据需求？** 核心洞察是：不同粒度的特征之间存在**互补性信息**。当 packet 级别的序列特征（细粒度）与 flow/host 级别的统计特征（粗粒度）融合后，联合特征空间的分布更加稀疏（Figure 1(d)），良性与恶意流量的分离度显著提高。这意味着：
1. 决策边界变得更简单，ML 模型可以用更少的样本学习
2. 攻击行为在单一模态中可能伪装（如 Crossfire 攻击模仿正常流量统计特征），但在跨模态关联中会暴露异常——攻击者难以同时操纵所有模态
3. Host 级别的上下文信息（同一地址的流量模式）为 flow 级别检测提供了额外约束

**为什么 1‰ 而非更少？** 论文在 1.0 ‱（万分之一）设置下仍保持 0.9492~0.9864 AUC，说明方法可以承受更极端的数据稀缺。1‰ 是作者选择的"实用"阈值：在机构网络部署中，从 90,319 条流中采样 91 条（约 1‰），两位研究生可在 20 分钟内用 Wireshark 完成标注。

### 3.3 现有方法的痛点和不足

| 现有方法 | 痛点 | 根本原因 |
|---|---|---|
| 单模态方法（nPrintML、FlowLens、NetBeacon 等） | 需要 O(10^4) ~ O(10^7) 训练样本 | 仅分析单一粒度特征，不同粒度之间的关联信息完全丢失 |
| 数据增强方法（NetAugment、Rosetta、ODDS 等） | 监督模型最高仅 0.8813 AUC，比 tFusion 低 10.52~25.52% | 规则仅适用于 Tor/TLS 等特定流量类型，GAN 只能生成恶意特征，跨数据集补充因分布差异无效 |
| 跨数据集补充样本 | 不同网络的流量特征分布差异显著（Figure 1(a)） | 网络服务多样性导致特征分布因网络而异，直接迁移引入噪声 |
| 良性流量分类模型（YaTC、ET-BERT 等） | 在小数据集上 AUC 低于 0.6 | 大型 Transformer 模型参数量大，严重过拟合小数据集 |
| 现有无监督方法（Whisper、HyperVision 等） | 1‰ 数据下 AUC 下降至少 5.226%（HyperVision 下降 0.2985） | 有限数据集无法提供足够的 flow interaction 信息 |
| 监督方法（Taurus/SVM 等） | 1‰ 数据下 AUC 下降至少 14.33%（Taurus 下降 0.129） | 少样本下无法学习复杂决策边界 |

### 3.4 论文的研究假设或核心直觉

- **核心假设**：网络流量本质上是多模态数据，包含 packet 级别的序列特征、flow 级别的统计特征和 host 级别的交互特征，不同粒度特征之间存在可利用的相关性
- **关键直觉（信息论视角）**：单模态特征空间中良性与恶意流量分布密集、难以区分（Figure 1(b)(c)），但多模态融合后的联合特征空间中分布更稀疏（Figure 1(d)），可以弥补传统单模态特征分析中的信息损失。具体地：
  - Crossfire 攻击在 flow 特征空间中与良性流量重叠（Figure 5(b)），但在 tFusion 联合特征空间中明显偏离（Figure 5(c)）
  - DNS 放大攻击在 packet 和 flow 特征空间中均接近良性流量（Figure 6(a)(b)），但跨模态融合后异常明显（Figure 6(c)）
- **拓扑直觉**：同一地址产生的流量在特征空间中应聚集在一起，不论其标签如何，这可以消除网络拓扑相关的偏差。关键观察是：Internet IP 地址在短时间内（如几分钟的数据采集窗口）很少被重新分配，因此地址信息可作为稳定的聚类信号
- **对抗鲁棒性直觉**：现有逃逸攻击仅操纵单一模态的特征（如流量混淆操纵 packet 特征、速率降低操纵 flow 统计），这会破坏跨模态特征之间的正常关联关系，反而使攻击更容易被检测

## 4. 方法设计

### 4.1 三种"模态"的定义

论文将网络流量视为多模态数据，三种模态分别对应不同的观测粒度：

| 模态 | 观测粒度 | 特征类型 | 维度 | 信息内容 |
|---|---|---|---|---|
| Packet 模态 | 单个数据包 | 序列特征（sequential） | H 维（隐藏维度） | 包长、到达时间、包间依赖关系 |
| Flow 模态 | 五元组流 | 统计特征（non-sequential） | 6 维 | 包数、FCT、总字节、最大/最小/平均包长 |
| Host 模态 | 源/目的地址 | 交互特征（non-sequential） | 12 维 | 发送/接收的流数、总包数、总字节（src+dst 各 6 维） |

关键设计决策：**不使用 packet header 字段**（如端口号、TTL）作为特征，因为攻击者可以轻松操纵这些字段进行逃逸攻击。仅使用 packet 的长度和到达时间，这些是攻击者在保持攻击有效性时难以同时操纵的特征。

### 4.2 方法整体流程

1. **Time-Aware Packet Sequence Embedding**：将每个 packet 的长度和到达时间编码为向量，通过 self-attention 提取流内 packet 之间的序列特征
2. **Crossmodal Attention Feature Fusion**：提取 flow 级别统计特征（6 维）和 host 级别交互特征（12 维），设计 crossmodal attention 以 host 特征为 query、flow 特征为 key、packet 特征为 value 进行跨模态特征融合
3. **Topology-Driven Contrastive Learning**：利用大规模无标注互联网流量，以拓扑地址信息驱动的对比学习预训练 attention 模型，减少拓扑偏差
4. **Lightweight ML Detection**：在部署网络中随机采样极少量流量标注后，使用 AutoML 框架选择最优的轻量级监督或无监督模型进行检测

### 4.3 详细 Pipeline（表格形式）

| 步骤 | 描述 | 技术细节 |
|---|---|---|
| 1. 流聚合 | 将 packet 按五元组聚合为 flow | 五元组：transport protocol, src IP, dst IP, src port, dst port |
| 2. Packet Embedding | 将每个 packet 的长度和时间编码为向量 | 长度编码：v = p * M + min(l, M) - 1；时间编码：time-aware positional encoding 使用指数函数和正弦函数 |
| 3. 序列特征提取 | 对每个 flow 的 packet 序列使用 self-attention | Query/Key/Value 线性变换 + scaled dot-product attention + residual connection + GELU + FC层 |
| 4. Flow 统计特征 | 提取 6 维 flow 级别特征 | 包数、流完成时间(FCT)、总字节数、最大/最小/平均包长，进行对数变换 |
| 5. Host 交互特征 | 提取 12 维 host 级别特征 | 对源和目的地址分别计算发送/接收的流数、总包数、总字节数（共 4 x 3 = 12 维） |
| 6. Crossmodal Fusion | 以 host 特征为 Q、flow 特征为 K、packet 特征为 V | 使用 Hadamard product 替代矩阵乘法，支持异构数据融合 + residual connection |
| 7. 对比学习预训练 | 利用无标注互联网流量预训练 | 按地址构建正负样本对，最小化同地址流特征距离、最大化不同地址流特征距离 |
| 8. AutoML 检测 | 训练并选择最优轻量级模型 | 监督：Random Forest, SVM, Decision Tree, RNN；无监督：K-Means, Isolation Forest, AutoEncoder |

### 4.4 模型结构或系统模块（表格形式）

| 模块 | 功能 | 输入 | 输出 |
|---|---|---|---|
| Time-Aware Packet Sequence Embedding | 提取细粒度 packet 级别时空序列特征 | 流的 packet 到达时间和长度序列 | 序列特征向量 p_i |
| Flow Statistical Feature Extraction | 提取 flow 级别统计特征 | 流的 packet 特征矩阵 P | 6 维 flow 特征向量 f_i |
| Host Feature Extraction | 提取 host 级别交互统计特征 | 时间窗口内的所有流 | 12 维 host 特征向量 h_i |
| Crossmodal Attention Feature Fusion | 融合三种模态特征 | h_i (Q), f_i (K), p_i (V) | 融合特征向量 F_i |
| Topology-Driven Contrastive Learning | 预训练 attention 模型 | 大规模无标注互联网流量 | 优化后的模型参数 |
| AutoML Module | 训练并选择最优检测模型 | 少量标注的融合特征 | 最优检测模型及分类结果 |

### 4.5 公式、算法和机制解释

#### 4.5.1 Time-Aware Packet Embedding

**长度编码**：

$$\vec{v}_j^i = \mathcal{I}_i.p \times M + \min(\vec{l}_j^i, M) - 1 \tag{1}$$

变量定义：
- $\mathcal{I}_i.p$：第 i 个流的传输层协议标识符（如 TCP=0, UDP=1）
- $M$：网络可传输的最大包长（超参数）
- $\vec{l}_j^i$：第 i 个流中第 j 个包的长度
- 设计意图：不同协议的相同包长映射到不同的 embedding 空间，避免协议间混淆

**Time-Aware Positional Encoding**：

$$\vec{u}_j^i = \begin{cases} 0, & \text{if } j = 1, \\ 2 \cdot j + 1, & \text{if } T \leq \vec{t}_j^i - \vec{t}_{j-1}^i, \\ 2 \cdot j, & \text{else} \end{cases} \tag{2}$$

$$\mathbf{U}_{j,p} = \begin{cases} \sin(p \cdot e^{-\frac{j \cdot \ln T}{H}}), & \text{if } j \bmod 2 = 0, \\ \cos(p \cdot e^{-\frac{j \cdot \ln T}{H}}), & \text{else} \end{cases} \tag{3}$$

变量定义：
- $\vec{t}_j^i$：第 i 个流中第 j 个包的到达时间戳
- $T$：时间间隔阈值，区分"显著"和"不显著"的包间时间间隔
- $H$：隐藏维度（embedding 维度）
- $1 \leq p \leq H$：embedding 向量的维度索引

关键设计：与 NLP 中仅编码位置顺序的传统 positional encoding 不同，此处同时编码了**位置信息**（j）和**时间间隔信息**（通过阈值 T 区分）。奇偶位置使用 sin/cos 交替编码，指数函数 $e^{-\frac{j \cdot \ln T}{H}}$ 放大位置差异。

**最终 packet 表示**：

$$\mathsf{S}^{(i)} = \mathbf{T}^{(i)} + \mathbf{E}^{(i)}$$

其中 $\mathbf{T}^{(i)} = \mathbf{U}_{\vec{u}^i}$ 是时间位置编码，$\mathbf{E}^{(i)} = \text{Embed}(\vec{v}^i)$ 是长度编码。$\mathsf{S}_j^{(i)}$ 是第 i 个流中第 j 个包的最终向量表示。

#### 4.5.2 Self-Attention 序列特征提取

$$\mathbf{Q}^{(i)} = \mathbf{S}^{(i)} \mathbf{W}^{(Q)\top} + \vec{b}^{(Q)} \tag{4}$$
$$\mathbf{K}^{(i)} = \mathbf{S}^{(i)} \mathbf{W}^{(K)\top} + \vec{b}^{(K)}, \quad \mathbf{V}^{(i)} = \mathbf{S}^{(i)} \mathbf{W}^{(V)\top} + \vec{b}^{(V)} \tag{5}$$

$$\mathbf{A}^{(i)} = \text{Softmax}\left(\frac{\mathbf{Q}^{(i)} \mathbf{K}^{(i)\top}}{\sqrt{H}}\right) \mathbf{V}^{(i)} \tag{6}$$

变量定义：
- $\mathbf{W}^{(Q)}, \mathbf{W}^{(K)}, \mathbf{W}^{(V)} \in \mathbb{R}^{H \times H}$：可训练的权重矩阵
- $\vec{b}^{(Q)}, \vec{b}^{(K)}, \vec{b}^{(V)}$：偏置向量
- $\mathbf{A}^{(i)}$：注意力矩阵，表示 packet 之间的相关性

残差连接 + 前馈网络：

$$\mathbf{M}^{(i)} = \text{GELU}(\text{Linear}(\mathbf{A}^{(i)} + \mathbf{S}^{(i)}; \mathbf{W}_{(H \times 4H)}^{(1)}, \vec{b}^{(1)}))$$
$$\mathbf{U}^{(i)} = \text{Softmax}(\text{Linear}(\mathbf{M}^{(i)}; \mathbf{W}_{(4H \times H)}^{(2)}, \vec{b}^{(2)}) + \mathbf{A}^{(i)})$$

最终取 $\mathbf{U}^{(i)}$ 的第一维 $\vec{p}_i$ 作为该流的 packet 级别序列表示。

**注意力可视化发现**（Figure 3 & 4）：
- 良性流（HTTP 下载、HTTPS 访问、UDP 视频）：注意力值较低，无明显规律
- 恶意流（脉冲 DoS、Telnet 注入、放大攻击）：注意力值显著更高，呈现周期性/规律性模式
- 对角线值不高，说明 packet 不主要关注自身，而是关注与其他 packet 的关系

#### 4.5.3 Flow 统计特征提取

$$\vec{f}^i = \text{Log}\left([N_i, \vec{t}_{N_i}^i - \vec{t}_1^i, \sum_{j=1}^{N_i} \vec{l}_j^i, \min(\vec{l}^i), \max(\vec{l}^i), \frac{1}{N_i}\sum_{j=1}^{N_i} \vec{l}_j^i]^\top + \vec{1}\right) \tag{8}$$

6 维特征含义：
1. $N_i$：流中的包数
2. $\vec{t}_{N_i}^i - \vec{t}_1^i$：流完成时间（FCT）
3. $\sum_{j=1}^{N_i} \vec{l}_j^i$：流的总字节数
4. $\min(\vec{l}^i)$：最小包长
5. $\max(\vec{l}^i)$：最大包长
6. $\frac{1}{N_i}\sum_{j=1}^{N_i} \vec{l}_j^i$：平均包长

对数变换 Log(·+1) 用于提高数值稳定性，压缩大值的尺度差异。

#### 4.5.4 Host 交互特征提取

首先定义查询函数：

$$f_{\text{src}}(s; \mathscr{F}) = \{\mathscr{F}_i | \forall \mathscr{F}_i \in \mathscr{F}, \mathcal{I}_i.s = s\}$$
$$f_{\text{dst}}(d; \mathscr{F}) = \{\mathscr{F}_i | \forall \mathscr{F}_i \in \mathscr{F}, \mathcal{I}_i.d = d\} \tag{9}$$

然后定义发送/接收模式特征：

$$\text{send}(h) = [|f_{\text{src}}(h; \mathcal{F})|, \sum_{\mathcal{F}_j \in f_{\text{src}}} N_j, \sum_{\mathcal{F}_j \in f_{\text{src}}} \sum_{k=1}^{N_j} \vec{l}_k^j]^\top \tag{10}$$
$$\text{receive}(h) = [|f_{\text{dst}}(h; \mathscr{F})|, \sum_{\mathscr{F}_j \in f_{\text{dst}}} N_j, \sum_{\mathscr{F}_j \in f_{\text{dst}}} \sum_{k=1}^{N_j} \vec{l}_k^j]^\top$$

每个 send/receive 向量包含 3 个特征：流数、总包数、总字节数。最终 host 特征：

$$\vec{h}^i = \text{Log}(\text{Cat}(\text{send}(\mathcal{I}_i.s), \text{receive}(\mathcal{I}_i.s), \text{send}(\mathcal{I}_i.d), \text{receive}(\mathcal{I}_i.d))) \tag{11}$$

4 个 send/receive 向量拼接 = 12 维特征。对源地址和目的地址分别计算，捕捉双向流量交互模式。

#### 4.5.5 Cross-Attention 跨模态融合（核心创新）

$$\vec{q}^i = \text{Linear}(\vec{h}^i; \mathbf{W}_{12 \times H}^q, \vec{b}^q) \quad \text{（Host 特征 → Query）}$$
$$\vec{k}^i = \text{Linear}(\vec{f}^i; \mathbf{W}_{6 \times H}^k, \vec{b}^k) \quad \text{（Flow 特征 → Key）}$$
$$\vec{v}^i = \text{Linear}(\vec{p}^i; \mathbf{W}_{H \times H}^v, \vec{b}^v) \quad \text{（Packet 特征 → Value）} \tag{12}$$

$$\vec{C}^i = \text{CrossAtten}(\vec{q}^i, \vec{k}^i, \vec{v}^i) = \text{Softmax}\left(\frac{\vec{q}^i \circ \vec{k}^i}{\sqrt{H}}\right)$$
$$\vec{F}^i = \vec{C}^i \circ \vec{v}^i + \vec{q}^i \tag{13}$$

**关键设计决策**：
- **Q=Host, K=Flow, V=Packet 的选择逻辑**：Host 和 Flow 特征是粗粒度的，无法直接指示细粒度模式，但可以**指导**模型将高注意力权重分配给关键 packet。即 host 上下文告诉模型"哪些 flow 值得关注"，flow 特征告诉模型"哪些 packet 模式重要"
- **Hadamard product (∘) 替代矩阵乘法**：传统 attention 的 Q·K^T 是矩阵乘法，适用于序列数据。但此处 Q（12 维→H 维）和 K（6 维→H 维）来自不同模态的非序列数据，Hadamard product 支持逐元素融合异构数据
- **残差连接** $\vec{F}^i = \vec{C}^i \circ \vec{v}^i + \vec{q}^i$：保留原始 query（host）信息，增强融合特征与 host 上下文的关联

**注意力可视化发现**（Figure 7）：
- 良性流量：跨模态注意力值较低且均匀
- 恶意流量（Crossfire、放大攻击、密码破解、垃圾邮件）：注意力值显著更高，表明异常的跨模态关联
- 这种异常关联是攻击者难以同时操纵所有模态的根本原因

#### 4.5.6 Topology-Driven Contrastive Learning（预训练策略）

**样本构建**：从大规模无标注互联网流量 $\mathcal{F}_T$ 中，筛选发送/接收流数 ≥ B（批大小）的地址：

$$\mathcal{S} = \{\mathcal{F}_i.s | |f_{\text{src}}(\mathcal{F}_i.s; \mathcal{F}_T)| \geq B\}, \quad \mathcal{D} = \{\mathcal{F}_i.d | |f_{\text{dst}}(\mathcal{F}_i.d; \mathcal{F}_T)| \geq B\} \tag{14}$$

对每个地址 h，构建正负样本对：
- 正样本 $\mathcal{C}_{\text{same}}^h$：同一地址产生的 B 条流
- 负样本 $\mathcal{C}_{\text{diff}}^h$：不同地址产生的 B 条流

**对比学习训练**：

$$\mathbf{F}^{(h)} = [\vec{F}^1, \dots, \vec{F}^B, \vec{F}^{B+1}, \dots, \vec{F}^{2B}] \tag{18}$$

投影层（仅用于预训练，推理时不使用）：

$$\mathbf{Q}^{(h)} = \text{proj}(\mathbf{F}^{(h)}) = \text{Linear}(\text{ReLU}(\text{Linear}(\mathbf{F}^{(h)}; \mathbf{W}^1, \vec{b}^1)); \mathbf{W}^2, \vec{b}^2) \tag{20}$$

对比损失（InfoNCE 变体）：

$$l_c^{(h)} = \frac{1}{B} \sum_{i=1}^{B-1} -\ln\left[\frac{e^{\text{Sim}(\vec{q}_i, \vec{q}_{i+1})}}{e^{\text{Sim}(\vec{q}_i, \vec{q}_{i+1})} + e^{\text{Sim}(\vec{q}_i, \vec{q}_{i+B})}}\right] \tag{22}$$

其中 $\text{Sim}(\vec{x}, \vec{y}) = \frac{\vec{x}^\top \cdot \vec{y}}{\|\vec{x}\| \|\vec{y}\|}$ 为余弦相似度。

**与传统对比学习的区别**：
- 不依赖数据增强规则（如图像旋转），直接利用不同地址产生的天然多样的流量模式
- 不依赖标签，仅利用地址信息作为自监督信号
- 预训练目标不是在特定网络上达到高检测精度，而是**消除拓扑偏差**——使模型在不同网络环境中都能有效提取特征

### 4.6 端到端训练流程

```
阶段 1：预训练（离线，一次性）
├── 输入：大规模无标注互联网流量（如 MAWI 176 万条流）
├── 构建对比学习样本对（按地址聚合）
├── 训练 crossmodal attention 模型（~10 分钟，V100 GPU）
└── 输出：预训练好的特征提取器

阶段 2：部署训练（目标网络，每次部署）
├── 从目标网络采样极少量流量（如 91 条，1‰）
├── 人工标注（~20 分钟，Wireshark）
├── 使用预训练模型提取融合特征
├── AutoML 选择最优轻量级模型（~10 分钟）
└── 输出：部署就绪的检测模型

阶段 3：在线检测（实时）
├── 输入：镜像流量
├── 特征提取（packet embedding + self-attention + flow/host 统计 + crossmodal fusion）
├── 轻量级模型推理
└── 输出：攻击流量标识
```

### 4.7 方法优势

1. **极低数据需求**：仅需标注 1.0 ‰（千分之一）的流量样本即可训练，大幅降低人力成本。实验验证仅 50 个样本即可达到 0.9863~0.9946 AUC
2. **跨网络通用性**：通过 topology-driven contrastive learning 消除拓扑偏差，可在全新网络环境中部署
3. **同时支持监督和无监督**：有攻击样本时使用监督模型，仅有良性样本时使用无监督模型
4. **对对抗攻击鲁棒**：crossmodal attention 能捕捉不同粒度特征之间的异常关联，攻击者难以同时操纵所有模态。逃逸攻击下 AUC 仅下降 0.80%，F1 仅下降 1.54%
5. **实时高效**：整体检测延迟 32.23ms，吞吐量 0.7042 MPPS，可处理高速网络流量
6. **全面检测能力**：支持通用检测、对抗攻击鲁棒性、零日攻击检测、加密流量检测和实时检测

### 4.8 方法不足

1. **仅验证了已知对抗攻击的鲁棒性**：论文承认仅针对前人工作中的已知逃逸攻击（traffic obfuscation、sending rate reduction、length manipulation）进行了验证，未来可能出现新的成功逃逸策略
2. **预训练依赖外部数据**：需要大规模无标注互联网流量进行预训练（本文使用 MAWI 骨干网流量 176 万条流/3900 万包）。虽然预训练数据不需要标注，但获取大规模流量数据本身可能有门槛
3. **AutoML 增加了复杂性**：自动模型选择虽然提高了 3.53% 准确率（比随机选择高 3.24%），但增加了系统复杂度和调试难度
4. **概念漂移需关注**：虽然五天部署中 AUROC 和 F1 保持在 0.9803 和 0.9317 以上，但长期部署（数月/数年）的稳定性尚未验证
5. **应用范围有限验证**：多模态策略仅初步应用于 VPN/Tor 流量分类任务（100 个样本下比 YaTC/ET-BERT 提高 2.75~6.62% F1），其他安全任务的适用性有待验证
6. **Host 特征的时间窗口依赖**：Host 交互特征的计算依赖于时间窗口 W 的选择，窗口大小可能影响特征质量

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 对比维度 | 现有单模态方法 | tFusion |
|---|---|---|
| 特征模态 | 单一模态（仅 packet、仅 flow 或仅 host） | 三种模态融合（packet + flow + host） |
| 训练数据需求 | O(10^4) ~ O(10^7) 样本 | O(10) 样本（仅需标注千分之一） |
| 跨网络部署 | 需要为每个网络重新构建大规模数据集 | 通过拓扑驱动预训练实现跨网络通用 |
| 特征融合方式 | 简单拼接或仅使用单一特征 | Crossmodal attention 动态融合 |
| 预训练方法 | 无或依赖标签数据 | 基于拓扑地址信息的对比学习，无需标签 |
| 信息利用效率 | 低（单粒度特征信息损失大） | 高（跨粒度特征互补，信息利用率高） |

### 5.2 与少样本/对比学习方法的对比

| 对比维度 | TIFS 2025 对比学习方法 | tFusion |
|---|---|---|
| 核心思路 | 通过对比学习增强特征表示的区分度 | 通过跨模态融合 + 拓扑驱动对比学习同时解决特征质量和数据稀缺问题 |
| 特征来源 | 通常基于单一模态（如 flow 统计特征） | 三种模态（packet + flow + host）融合 |
| 预训练信号 | 通常依赖标签或数据增强规则 | 仅依赖网络拓扑地址信息，无需标签 |
| 数据需求 | 仍需要一定规模的标注数据 | 仅需 1‰ 标注数据 |
| 跨网络通用性 | 可能受限于特定网络的特征分布 | 通过拓扑驱动预训练消除网络偏差 |

**tFusion 的独特优势**：与纯对比学习方法不同，tFusion 不仅通过对比学习提升特征质量，更通过跨模态融合从根本上改变了特征空间的结构——多模态融合后的特征空间分布更稀疏，良性与恶意流量分离度更高。这两个机制（跨模态融合 + 拓扑对比学习）是互补的：前者提升单个网络内的检测能力，后者提升跨网络的泛化能力。

### 5.3 与数据增强方法的对比

| 方法 | 增强策略 | 监督模型 AUC | 无监督模型 AUC | 局限性 |
|---|---|---|---|---|
| NetAugment | 规则增强（Tor 流量） | 0.8813 | 0.7911 | 仅适用于 Tor 流量 |
| Rosetta | 规则增强（TLS 流量） | 0.8663 | 0.7813 | 仅适用于 TLS 流量 |
| ODDS | GAN 生成 | 0.7404 | 0.7460 | 只能生成恶意特征 |
| MAWI 补充数据 | 跨数据集补充 | 0.8491 | 0.7809 | 分布差异导致效果有限 |
| CIC 补充数据 | 跨数据集补充 | 0.8579 | 0.7763 | 分布差异导致效果有限 |
| **tFusion** | **跨模态融合** | **0.9864** | **0.9492** | 无上述局限性 |

数据增强方法的根本问题：它们试图在**同一特征空间**中生成更多样本，但特征空间本身的区分度不足。tFusion 的思路不同——通过跨模态融合**改变特征空间的结构**，使其本身就具有更高的区分度，因此不需要大量样本。

### 5.4 创新点分析（表格形式）

| 创新点 | 说明 | 与现有方法的区别 |
|---|---|---|
| 多模态流量视角 | 首次将网络流量明确视为多模态数据（packet、flow、host），并设计专用的跨模态特征融合方法 | 现有方法仅使用单一模态或简单拼接 |
| Time-Aware Positional Encoding | 设计了同时编码 packet 位置和到达时间间隔的位置编码算法 | NLP 中的位置编码仅考虑顺序，不考虑时间尺度 |
| Crossmodal Attention 融合机制 | 以 host 特征为 query、flow 特征为 key、packet 特征为 value，使用 Hadamard product 实现异构数据融合 | 现有 attention 方法仅用于同模态序列数据 |
| Topology-Driven Contrastive Learning | 利用网络拓扑地址信息（而非标签）构建对比学习样本，消除拓扑偏差 | 现有对比学习依赖标签或固定规则数据增强 |
| 极低数据量训练框架 | 整体框架使仅需标注千分之一的流量即可达到 99.82% 检测精度 | 现有方法需要 O(10^4)~O(10^7) 样本 |

### 5.5 适用场景

- **新网络快速部署**：在缺乏大规模标注数据的全新网络环境中快速部署恶意流量检测系统
- **企业网络安全**：保护拥有约 100+ 活跃用户的机构网络，检测各类攻击（web 攻击、洪泛攻击、漏洞利用、恶意软件）
- **加密流量检测**：不依赖 payload 内容，可检测加密恶意流量
- **高速网络实时检测**：在 ISP 骨干网等高速网络环境中实现实时检测
- **零日攻击检测**：通过无监督学习检测训练数据中未出现过的未知攻击
- **资源受限场景**：预训练仅需 10 分钟（V100 GPU），部署标注仅需 20 分钟

### 5.6 方法对比表

| 方法 | 特征模态 | 训练数据需求 | 跨网络通用 | 对抗鲁棒 | 加密流量 | 实时检测 | 高效检测 |
|---|---|---|---|---|---|---|---|
| nPrintML | Packet | O(10^5) | 否 | 否 | 是 | 是 | 否 |
| FlowLens | Flow | O(10^4) | 否 | 否 | 是 | 否 | 是 |
| NetBeacon | Flow | O(10^7) | 否 | 否 | 否 | 是 | 是 |
| Kitsune | Packet | O(10^5) | 否 | 否 | 否 | 否 | 否 |
| Whisper | Host | O(10^3) | 否 | 是 | 否 | 是 | 是 |
| HyperVision | Host | O(10^7) | 否 | 否 | 是 | 否 | 是 |
| **tFusion** | **ALL** | **O(10)** | **是** | **是** | **是** | **是** | **是** |

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **测试平台**：DELL 服务器，双 Intel Xeon E2699 v4 CPU，512GB DDR4 内存，Intel 82599SE NIC（2 x 10Gb/s SFP+），Tesla V100 GPU（32GB）
- **实现**：2.7K 行 C++14 和 Python 3.10 代码，使用 libpcap++、PyTorch v1.11.0、scikit-learn v1.1.2
- **数据集**：11 个公开数据集（共 150 种不同攻击），加上 1 个机构网络部署实测
- **预训练数据**：MAWI 骨干网 2023 年 1 月流量，包含 176 万条流（3900 万个包），来自连接日本两个 AS 的光纤链路
- **训练比例**：分别测试了 1.0 ‱、1.0 ‰、1.0% 和 10.0% 的训练样本比例
- **部署实验**：机构网络，140+ 活跃用户，五天持续检测
- **默认设置**：AutoML 限制为 Random Forest（监督）和 K-Means（无监督），以保证与 baseline 的公平比较

### 6.2 数据集

| 数据集 | 类型 | 攻击类型 | 来源 |
|---|---|---|---|
| HyperVision | 高速骨干网 10Gb/s | 洪泛、探测、web 攻击、恶意软件、高级攻击（加密流量） | 光纤链路 |
| CIC-IDS2017 | 企业网络 | 入侵检测 | CIC |
| CIC-IDS2018 | 企业网络 | 入侵检测 | CIC |
| CIC-DDoS2019 | 企业网络 | DDoS 攻击 | CIC |
| CIC-Android | 移动网络 | Android 恶意软件 | CIC |
| CIC-IoT | IoT 网络 | IoT 隐蔽攻击 | CIC |
| CIC-DoH | DNS-over-HTTPS | DoH 隐蔽信道 | CIC |
| CTU-13 | 校园网络 | 僵尸网络 | CTU |
| Whisper | 模拟网络 | 侦察、LFA、脉冲攻击 | Whisper |
| Kitsune | IoT 网络 | IoT 设备攻击 | Kitsune |
| NetBeacon | 私有云 | 各类攻击 | NetBeacon |

注：当数据集不包含良性流量或仅含低速模拟流量时，使用 HyperVision 数据集的良性流量进行补充，以在复杂网络环境中比较。

### 6.3 Baseline

共对比 14 种现有方法：
- **监督方法**：nPrintML (AutoML)、FlowLens (Random Forest)、Taurus (SVM)、NetBeacon (Decision Tree)、BoS (RNN)、N3IC (Binary DNN)
- **无监督方法**：Whisper (K-Means)、Kitsune (AutoEncoder)、EULER (GNN+RNN)、HorusEye (Isolation Forest)、HyperVision (Graph Learning)
- **其他**：FlowMeter-RF、FlowMeter-KM、Jaqen、RAPIER、FSC、FAE
- **数据增强方法**：NetAugment、Rosetta、ODDS、MAWI 补充数据、CIC 补充数据

注：论文还尝试将良性流量分类模型（YaTC、ET-BERT）适配为恶意流量检测，但 AUC 均低于 0.6，因大型 Transformer 模型在小数据集上严重过拟合。

### 6.4 评价指标

- **AUC (AUROC)**：受试者工作特征曲线下面积（主要指标）
- **F1-score**：精确率和召回率的调和平均（主要指标）
- **AUPRC**：精确率-召回率曲线下面积
- **Accuracy (Acc.)**：准确率
- **Precision (Pre.)**：精确率
- **Recall (Rec.)**：召回率
- **TPR/FPR**：真阳性率/假阳性率

### 6.5 关键实验结果（表格形式）

**10.0% 训练数据下的整体 AUC（Table 2）：**

| 方法 | 整体 AUC | 备注 |
|---|---|---|
| 最佳现有方法（Supervised） | ~0.9029 (Taurus/SVM) | 在部分数据集上表现好但不稳定 |
| 最佳现有方法（Unsupervised） | ~0.8534 (HyperVision) | 在 HyperVision 数据集上最优但其他数据集较差 |
| tFusion-RF (Supervised) | **0.9947** | 超越最佳 baseline 9.25~12.76% |
| tFusion-KM (Unsupervised) | **0.9783** | 在所有数据集上表现稳定 |

**1.0 ‰ 训练数据下的整体 AUC（Table 3）：**

| 方法 | 整体 AUC | 相比 10% 数据的下降 |
|---|---|---|
| 最佳现有方法（Supervised） | ~0.7735 (Taurus) | 下降 0.129 AUC（-14.33%） |
| 最佳现有方法（Unsupervised） | ~0.7127 (Whisper) | 下降显著 |
| tFusion-RF (Supervised) | **0.9864** | 仅下降 0.83%（从 0.9947） |
| tFusion-KM (Unsupervised) | **0.9492** | 仅下降 2.97%（从 0.9783） |

**关键发现**：tFusion 在数据量减少 100 倍时，精度下降不到 3%，而现有方法下降 5.26%~34.97%。这证明了跨模态融合特征的信息密度远高于单模态特征。

**不同训练样本数量的精度（Section 5.2 + Appendix C.1）：**

| 训练样本数 | tFusion-RF AUC | tFusion-KM AUC |
|---|---|---|
| 50 | 0.9863 | 0.9675 |
| 100 | 0.9912 | 0.9721 |
| 200 | 0.9946 | 0.9784 |
| 1.0 ‰ (91) | 0.9864 | 0.9492 |

**机构网络部署结果（Table 4）：**

| 攻击类型 | 数量 | AUROC | AUPRC | F1 | 精确率 | 召回率 |
|---|---|---|---|---|---|---|
| Web 攻击 | 7 种 | 0.9975 | 0.9830~0.9960 | 0.9630~0.9960 | 0.9278~0.9931 | 0.9980~0.9988 |
| 洪泛攻击 | 10 种 | 0.9974 | 0.9245~0.9990 | 0.9341~0.9990 | 0.8705~0.9999 | 0.9977~0.9998 |
| 高级攻击 | 9 种 | 0.9975 | 0.9524~0.9993 | 0.9564~0.9993 | 0.9145~0.9999 | 0.9975~0.9999 |
| 恶意软件 | 3 种 | 0.9977 | 0.9988~0.9990 | 0.9988~0.9990 | 0.9993~0.9997 | 0.9978~0.9986 |
| **整体** | **29 种** | **0.9975** | **0.9882** | **0.9890** | **0.9798** | **0.9982** |

部署详情：处理 25.43M 条流（884.25M 个包），其中 4.823% 流与异常行为相关。训练数据仅 91 条流（87 条良性），标注耗时约 20 分钟。误报率 2.322 个/小时，在人工处理能力范围内。

### 6.6 消融实验结果

**特征融合方式对比：**

| 融合方式 | 效果 |
|---|---|
| 仅用 packet 特征 | AUC 最高仅 0.8508（比融合低 14.39%） |
| 仅用 flow 特征 | AUC 最高仅 0.5409（比融合低 45.38%） |
| 仅用 host 特征 | AUC 在 0.5409~0.8508 之间 |
| 简单拼接（concatenation） | 比 tFusion 低 8.06% |
| 简单相加（addition） | 仅达 tFusion 的 87.65% AUC |
| **tFusion crossmodal attention** | **最优** |

**模态消融（逐个移除模态）：**

| 移除的模态 | 监督模型 AUC 下降 | 无监督模型 AUC 下降 |
|---|---|---|
| 移除 packet | 8.50%~14.70% | 3.79%~47.48% |
| 移除 flow | 8.50%~14.70% | 3.79%~47.48% |
| 移除 host | 8.50%~14.70% | 3.79%~47.48% |

**关键结论**：三种模态缺一不可，仅使用单一模态特征 AUC 最多下降 44.09%。

**AutoML 模块贡献：**
- AutoML 选择最优模型比默认模型提高 3.53% 准确率
- AutoML 比随机模型选择提高 3.24% 准确率

### 6.7 对抗鲁棒性实验

**三种逃逸攻击策略：**

| 逃逸策略 | 描述 | tFusion 监督 AUC | tFusion 无监督 AUC |
|---|---|---|---|
| Traffic Obfuscation | 注入良性加密流量（1:4 比例）混淆攻击流量 | 0.9927 | 0.9764 |
| Sending Rate Reduction | 攻击者降低 50% 发送速率 | 0.9927 | 0.9756 |
| Length Manipulation | 模仿良性加密流的包长分布（5% 随机良性流） | 0.9927 | 0.9760 |
| **整体** | 三种策略组合 | **0.9927**（下降 0.80%） | **0.9760**（下降 0.46~0.94%） |

对比：现有非鲁棒方法（如 Kitsune）在逃逸攻击下 AUC 下降 35.40%；现有鲁棒方法（Whisper 下降 3.67%，HyperVision 下降 4.49%）。

**鲁棒性原因**：逃逸攻击仅操纵单一模态的特征，这会破坏跨模态特征之间的正常关联关系，反而使异常更容易被 crossmodal attention 捕捉。

**动态 IP 分配鲁棒性**：使用概率模型模拟 IP 重新分配，tFusion 保留 97.9% 以上准确率。原因：Internet IP 在短时间窗口内很少被重新分配。

### 6.8 性能效率

| 指标 | 数值 |
|---|---|
| 整体检测延迟 | 32.23ms |
| ML 模型延迟 | 9.02ms |
| 网络组件延迟 | 17.22ms |
| Embedding 模块延迟 | 0.23ms |
| Sequence Model 延迟 | 6.34ms |
| Feature Fusion 延迟 | 0.79ms |
| AutoML 延迟 | 2.02ms |
| ML 吞吐量 | 0.7042 MPPS |
| 网络吞吐量 | 1.68 MPPS |
| 预训练时间 | 10.43 分钟（V100 GPU，利用率 13.5%） |
| 预训练数据预处理 | 63.67 秒 |

不同数据集延迟：Whisper 40.70ms、HyperVision 34.21ms、Kitsune 27.89ms、NetBeacon 38.17ms。

效率对比：tFusion 延迟低于 FAE（1.41x）、HyperVision（26.77x）、Whisper（3.28x）；吞吐量高于 FAE（1.05x）和 Whisper（1.23x）。

### 6.9 优势最明显的场景

- **极小训练数据**：仅需 50 个训练样本即可达到 0.9863~0.9946 AUC，远超所有 baseline
- **跨网络通用检测**：在 11 个不同数据集上均表现稳定（AUC 0.9063~1.0000），而现有方法在不同数据集上波动巨大
- **对抗攻击鲁棒性**：在三种逃逸攻击下，AUC 仅下降 0.80%，F1 仅下降 1.54%
- **低速隐蔽攻击检测**：可检测密码破解（109 PPS）、SMTP-over-SSH 垃圾邮件（167 PPS）、SQL 注入（170 PPS）等低速攻击
- **实时检测**：整体延迟 32.23ms，吞吐量 0.7042 MPPS，高于高速 ISP 网络吞吐量（0.28 MPPS）
- **高级攻击检测**：Crossfire LFA、CVE-2020-36516 侧信道、CVE-2016-5696 TCP 劫持、脉冲 DoS 等高级攻击平均 AUC 0.9760

### 6.10 局限性

1. **仅验证已知逃逸攻击**：仅针对已有文献中的对抗策略进行验证，未来可能出现新的逃逸方法
2. **预训练数据依赖**：需要外部大规模无标注互联网流量（MAWI 骨干网数据）
3. **概念漂移长期稳定性**：五天部署中未出现显著漂移，但更长时间的稳定性未验证
4. **多类别分类初步**：仅初步验证了 VPN/Tor 流量分类，多类别恶意流量分类效果待验证
5. **硬件依赖**：需要 GPU（Tesla V100）进行预训练和推理，部署成本较高
6. **训练数据过拟合**：实验发现训练集准确率比测试集高 8.16%，存在轻微过拟合

## 7. 学习与应用

### 7.1 是否开源？

是。代码托管在 https://github.com/fuchuanpu/TFusion。完整附录：https://github.com/fuchuanpu/TFusion/blob/main/tFusion_LongVersion.pdf

### 7.2 复现关键步骤

1. **预训练阶段**：获取大规模无标注互联网流量（如 MAWI 数据集），按源/目的地址构建对比学习样本对
2. **Time-Aware Embedding**：实现 packet 长度编码（协议偏移 + embedding 层）和时间感知位置编码（指数正弦函数）
3. **Self-Attention 序列特征提取**：实现标准 Transformer self-attention，提取 packet 序列特征
4. **Flow/Host 特征提取**：实现 6 维 flow 统计特征和 12 维 host 交互特征提取
5. **Crossmodal Attention 融合**：实现以 Hadamard product 替代矩阵乘法的 cross-attention 机制
6. **对比学习训练**：使用 Adam 优化器，小学习率和权重衰减，训练约 10 分钟（V100 GPU）
7. **部署阶段**：在目标网络随机采样极少量流量（如 91 条），标注后使用 AutoML 训练检测模型

### 7.3 关键超参数、预处理和训练细节

| 参数 | 值/说明 |
|---|---|
| 预训练时间 | ~10.43 分钟（V100 GPU，平均 GPU 利用率 13.5%） |
| 预训练数据量 | 176 万条流（3900 万包），来自 MAWI 骨干网 |
| 预训练批大小 B | 批大小超参数，每批包含同地址和不同地址各 B 条流 |
| 隐藏维度 H | 模型隐藏状态维度 |
| 最大包长 M | 网络可传输的最大包长度 |
| 时间阈值 T | 区分显著时间间隔的阈值 |
| 训练样本比例 | 测试了 1.0 ‱、1.0 ‰、1.0%、10.0% |
| 部署标注样本数 | 91 条流（1.0 ‰），标注为 87 条良性流 |
| AutoML 模型 | 监督：Random Forest, SVM, Decision Tree, RNN；无监督：K-Means, Isolation Forest, AutoEncoder |
| 优化器 | Adam，小学习率 + 权重衰减 |
| 检测延迟 | 整体 32.23ms（ML: 9.02ms, Network: 17.22ms） |
| 吞吐量 | ML: 0.7042 MPPS, Network: 1.68 MPPS |
| 部署用户规模 | 62~140 活跃用户 |
| 五天处理量 | 25.43M 条流（884.25M 个包） |
| 误报率 | 2.322 个/小时 |

### 7.4 为什么跨模态融合对恶意流量检测特别有效？

**根本原因：攻击行为的多尺度特征不一致性**。恶意流量的本质特征是：攻击者需要在某些维度上保持攻击有效性（如发送速率、payload 内容），这必然在某些模态中留下痕迹。但攻击者很难同时在所有模态中完美伪装：

1. **Crossfire 攻击**：通过大量受控设备生成"正常"流量来拥塞关键链路。在 flow 统计特征中与良性流量重叠（Figure 5(b)），但 host 级别的流量交互模式异常（大量地址同时向少量目标发送），packet 级别的序列模式也呈现异常规律性
2. **DNS 放大攻击**：通过少量低速请求触发大量响应。packet 和 flow 特征接近良性（Figure 6(a)(b)），但 host 级别的请求-响应比例异常
3. **逃逸攻击**：攻击者操纵单一模态特征（如注入混淆流量、降低发送速率、模仿包长），但这会破坏跨模态特征之间的正常关联关系，使 crossmodal attention 产生高注意力值

**信息论解释**：单模态特征的信息熵有限，多模态融合后的联合特征空间维度更高、分布更稀疏，信息量更大。用更少的样本就能覆盖特征空间中的关键区域。

### 7.5 1‰ 样本要求的泛化性分析

**1‰ 是否是硬性下限？** 不是。论文实验表明：
- 1.0 ‱（万分之一）下仍保持 0.9492~0.9864 AUC
- 仅 50 个训练样本即可达到 0.9863~0.9946 AUC
- 1‰ 是作者选择的"实用"阈值，平衡了标注成本和检测精度

**什么条件下 1‰ 可能不够？**
- 目标网络的流量模式与预训练数据差异极大（如全新的协议或应用）
- 需要检测的攻击类型在特征空间中与良性流量高度重叠
- 目标网络的活跃地址数量极少（host 特征的统计显著性不足）

**预训练数据的关键作用**：1‰ 的低数据需求依赖于拓扑驱动对比学习的预训练。预训练使模型已经学会了提取有意义的跨模态特征，部署时仅需少量样本校准到目标网络的特征分布。如果没有预训练，1‰ 的数据量可能不足以训练有效的 crossmodal attention 模型。

### 7.6 实际部署的实用价值

**部署成本分析**：
- 预训练：一次性，10 分钟 GPU 时间（可用云 GPU，成本约 $0.5）
- 部署标注：每个新网络约 20 分钟人工标注（91 条流用 Wireshark）
- 运行检测：32ms 延迟，可处理 ISP 级流量

**与传统方案对比**：
- 传统方案：为每个新网络标注数百万数据包，耗时数天到数周，需要专业安全团队
- tFusion：两位研究生 20 分钟完成标注，10 分钟训练模型，即可部署

**适用的部署场景**：
- 企业分支机构快速部署安全检测
- ISP 为新客户提供恶意流量检测服务
- 临时活动（如大型会议）的网络安全保护
- 资源受限的中小型网络

### 7.7 能否迁移到其他任务？

- **VPN/Tor 流量分类**：论文初步验证了在仅 100 个样本下分类 VPN 和 Tor 流量，比 YaTC 提高 2.75~5.75% F1，比 ET-BERT 提高 3.62~6.62% F1
- **良性应用流量分类**：论文指出多模态方法可减少其他学习任务对大规模数据集的依赖
- **入侵检测系统**：crossmodal attention 融合思路可应用于其他需要综合多粒度特征的安全任务
- **恶意软件分类**：不同模态的特征融合可能有助于恶意软件家族分类
- **异常行为检测**：部署中发现 tFusion 能检测到真实用户的异常行为（如 OpenSSH 漏洞探测脚本）

### 7.8 对我的研究有什么启发？

1. **多模态视角**：将网络流量视为多模态数据是一种强大的范式，不同粒度特征之间的相关性包含丰富信息，传统方法仅使用单一粒度特征会损失大量信息。这一思路可推广到其他安全任务
2. **极低数据量训练的可行性**：通过有效的特征融合和预训练策略，可以在极小数据集下实现高性能检测，这对数据稀缺场景非常重要
3. **拓扑驱动预训练**：利用网络拓扑信息（而非标签）构建对比学习信号，是一种通用的跨域预训练策略，可应用于其他网络分析任务。关键洞察是：地址信息是免费的、稳定的自监督信号
4. **Hadamard product 融合**：在融合异构（序列与非序列）数据时，Hadamard product 比矩阵乘法更灵活，这一技巧可推广到其他多模态融合场景
5. **AutoML 的价值**：在特征提取已经充分的情况下，AutoML 可以自动选择最优的轻量级下游模型，简化部署流程
6. **对抗鲁棒性的新思路**：通过跨模态融合，逃逸攻击反而暴露了异常的跨模态关联，这是一种"攻击者越伪装越暴露"的优雅防御机制
7. **与 TIFS 2025 对比学习方法的互补**：tFusion 的跨模态融合和拓扑对比学习可以与纯对比学习方法结合，进一步提升少样本检测性能

## 8. 总结

### 8.1 核心思想（不超过20字）

跨模态注意力融合多粒度流量特征，实现极小数据训练。

### 8.2 速记版 Pipeline（3-5步）

1. 从 packet、flow、host 三个模态提取异构特征（序列特征 + 统计特征 + 交互特征）
2. 设计 crossmodal attention 以 host 为 Q、flow 为 K、packet 为 V 进行特征融合
3. 用 topology-driven contrastive learning 在大规模无标注流量上预训练模型
4. 在目标网络采样极少量流量标注后，用 AutoML 训练轻量级检测模型
5. 仅需千分之一标注流量即可达到 99.82% 检测精度

## 9. Obsidian 知识链接

### 9.1 相关概念

- Malicious Traffic Detection - 恶意流量检测
- Crossmodal Learning - 跨模态学习
- Contrastive Learning - 对比学习
- Attention Mechanism - 注意力机制
- Few-Shot Learning - 少样本学习
- Network Traffic Classification - 网络流量分类
- AutoML - 自动机器学习

### 9.2 相关方法

- Crossmodal Attention - 跨模态注意力
- Topology-Driven Contrastive Learning - 拓扑驱动对比学习
- Time-Aware Positional Encoding - 时间感知位置编码
- Self-Attention / Transformer - 自注意力 / Transformer
- Hadamard Product Fusion - Hadamard 积融合
- Data Augmentation for Traffic - 流量数据增强

### 9.3 相关任务

- Encrypted Malicious Traffic Detection - 加密恶意流量检测
- Zero-Day Attack Detection - 零日攻击检测
- Cross-Network Detection - 跨网络检测
- Evasion Attack Robustness - 对抗逃逸攻击鲁棒性
- Real-Time Traffic Detection - 实时流量检测
- DDoS Detection - DDoS 检测

### 9.4 可更新的综述页面

- ML-Based Malicious Traffic Detection Survey
- Crossmodal Learning for Network Security
- Few-Shot Learning in Security

### 9.5 可加入的对比表

- Malicious Traffic Detection Methods Comparison
- Few-Shot Traffic Detection Methods
- Crossmodal Feature Fusion Methods

## 10. 证据记录（表格形式）

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E1 | 实验结果 | 10.0% 训练数据下 tFusion-RF 整体 AUC 0.9947，超越最佳 baseline 9.25~12.76% | Table 2 |
| E2 | 实验结果 | 1.0 ‰ 训练数据下 tFusion-RF 整体 AUC 0.9864，超越最佳 baseline 21.29%（Taurus 0.7735） | Table 3 |
| E3 | 实验结果 | 1.0 ‱ 训练数据下 tFusion 仍保持 0.9492 AUC（无监督）和 0.9864 AUC（监督），现有方法下降 5.26~34.97% | Section 5.2 |
| E4 | 实验结果 | 机构网络部署五天，整体 AUROC 0.9975，AUPRC 0.9882，F1 0.9890，Recall 0.9982 | Table 4 |
| E5 | 实验结果 | 对抗逃逸攻击下 AUC 仅下降 0.80%，F1 仅下降 1.54%（对比 Kitsune 下降 35.40%） | Figure 12 |
| E6 | 实验结果 | 检测延迟 32.23ms（ML: 9.02ms, Network: 17.22ms），吞吐量 0.7042 MPPS，高于 ISP 网络需求（0.28 MPPS） | Section 5.4 |
| E7 | 实验结果 | 预训练仅需 10.43 分钟（V100 GPU），GPU 利用率仅 13.5%，数据预处理 63.67 秒 | Section 5.4 |
| E8 | 实验结果 | 仅 50 个训练样本即可达到 0.9863~0.9946 AUC | Section 5.2 |
| E9 | 实验结果 | 误报率 2.322 个/小时，在人工处理能力范围内 | Section 5.5 |
| E10 | 消融实验 | 仅用单一模态特征 AUC 最多下降 44.09%（0.5409 vs 0.9818），三种模态缺一不可 | Section 5.2 |
| E11 | 实验结果 | 比数据增强方法（NetAugment、Rosetta、ODDS）监督模型提高 10.52~25.52% AUC，无监督提高 18.45~23.10% | Section 5.2 |
| E12 | 实验结果 | 动态 IP 分配对精度影响有限，保留 97.9% 以上准确率 | Figure 13 |
| E13 | 消融实验 | 简单拼接融合比 crossmodal attention 低 8.06%，简单相加仅达 87.65% AUC | Section 5.2 |
| E14 | 消融实验 | 移除任一模态导致监督模型 AUC 下降 8.50~14.70%，无监督下降 3.79~47.48% | Section 5.2 |
| E15 | 消融实验 | AutoML 选择最优模型比默认模型提高 3.53%，比随机选择提高 3.24% | Section 5.2 |
| E16 | 实验结果 | 部署中处理 25.43M 条流（884.25M 包），4.823% 流与异常相关，62~140 活跃用户 | Section 5.5 |
| E17 | 实验结果 | 低速攻击检测：密码破解 109 PPS、SMTP-over-SSH 垃圾邮件 167 PPS、SQL 注入 170 PPS，AUPRC 0.9718~0.9986 | Table 4 |
| E18 | 实验结果 | 高级攻击检测：Crossfire LFA、CVE-2020-36516 侧信道、CVE-2016-5696 TCP 劫持、脉冲 DoS，平均 AUC 0.9760 | Section 5.2 |
| E19 | 实验结果 | VPN/Tor 分类：仅 100 样本下比 YaTC 提高 2.75~5.75% F1，比 ET-BERT 提高 3.62~6.62% F1 | Section 6 |
| E20 | 实验结果 | 预训练数据稳定性：使用 2023 年 12 个月的 MAWI 数据预训练，时间消耗 7.14~16.58 分钟，平均 10.18 分钟 | Figure 18 |
| E21 | 实验结果 | 训练集准确率比测试集高 8.16%，存在轻微过拟合 | Section 5.2 |
| E22 | 实验结果 | 五天部署中 AUROC 和 F1 保持在 0.9803 和 0.9317 以上，无概念漂移激增 | Section 5.5 |
| E23 | 实验结果 | 检测到真实用户的异常行为（OpenSSH 漏洞探测脚本），AUPRC 0.9524~0.9988 | Section 5.5 |
| E24 | 注意力可视化 | 恶意流的 attention 值显著高于良性流，呈现周期性/规律性模式（脉冲 DoS、放大攻击） | Figure 3, 4 |
| E25 | 特征可视化 | tFusion 联合特征空间中 Crossfire 和放大攻击明显偏离良性流量，而单模态空间中重叠 | Figure 5, 6 |
| E26 | 跨模态注意力 | 恶意流量的跨模态注意力值显著高于良性流量，表明异常的跨模态关联 | Figure 7 |

## 11. 原始资料链接

- 论文发表于 ACM CCS 2025（October 13-17, 2025, Taipei）
- 作者单位：清华大学计算机科学与技术系、清华大学 INSC 和互联网体系结构国家重点实验室、普渡大学计算机科学系、中关村实验室
- DOI: 10.1145/3719027.3765143
- 项目主页/代码：https://github.com/fuchuanpu/TFusion
- 完整附录：https://github.com/fuchuanpu/TFusion/blob/main/tFusion_LongVersion.pdf
- 预训练数据来源：MAWI Working Group Traffic Archive (http://mawi.wide.ad.jp/mawi/)
- 基金资助：国家自然科学基金杰出青年基金（No. 62425201）、创新研究群体（No. 62221003）、重点项目（No. 61932016, No. 62132011）、清华大学海外研究生奖学金（No. 2024072）

## 12. 后续问题

1. **新型对抗攻击**：攻击者是否能设计同时操纵多种模态特征的逃逸策略？论文指出这将开启新的攻防研究方向
2. **长期概念漂移**：在数月甚至数年的部署中，tFusion 是否需要重新预训练或增量学习？
3. **多类别恶意流量分类**：能否将多模态融合方法扩展到恶意流量的细粒度分类（如区分不同恶意软件家族）？
4. **其他安全任务**：多模态策略在网站指纹攻击、应用分类、异常行为检测等其他任务上的效果如何？
5. **边缘设备部署**：在资源受限的边缘设备或 IoT 网关上，tFusion 的轻量化版本是否可行？
6. **预训练数据选择**：不同来源和规模的预训练数据对最终检测精度的影响有多大？
7. **隐私保护**：对比学习中使用地址信息构建样本对是否存在隐私泄露风险？

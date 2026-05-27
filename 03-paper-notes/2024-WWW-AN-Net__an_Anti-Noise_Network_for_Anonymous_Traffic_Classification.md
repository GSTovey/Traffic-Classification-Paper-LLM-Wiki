---
type: paper
title_original: "AN-Net: an Anti-Noise Network for Anonymous Traffic Classification"
title_cn: "AN-Net: 一种用于匿名流量分类的抗噪声网络"
authors: ["Xianwen Deng", "Yijun Wang", "Zhi Xue"]
year: 2024
venue: "ACM Web Conference 2024 (WWW '24)"
doi: "10.1145/3589334.3645691"
url: "https://doi.org/10.1145/3589334.3645691"
pdf: "00-inbox/PDFs/2024-WWW-AN-Net__an_Anti-Noise_Network_for_Anonymous_Traffic_Classification.pdf"
mineru_md: "02-parsed-markdown/2024-WWW-AN-Net__an_Anti-Noise_Network_for_Anonymous_Traffic_Classification.md"
status: processed
reading_level: L2
research_area: ["traffic classification", "anonymous traffic", "encrypted traffic analysis", "deep learning"]
task: ["anonymous traffic classification", "VPN traffic classification", "noise-robust classification"]
method: ["short-term representation learning", "high temperature self-attention", "multi-modal fusion", "representation enhancement", "bidirectional GRU", "Transformer"]
dataset: ["SJTU-AN21", "ISCX-Tor", "ISCX-VPN", "USTC-TFC", "Cross-Platform"]
code: "https://github.com/SJTU-dxw/AN-Net"
relevance: high
created: "2026-05-27"
updated: "2026-05-27"
---

# AN-Net: an Anti-Noise Network for Anonymous Traffic Classification

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | AN-Net: an Anti-Noise Network for Anonymous Traffic Classification |
| 中文标题 | AN-Net: 一种用于匿名流量分类的抗噪声网络 |
| 作者 | Xianwen Deng, Yijun Wang, Zhi Xue |
| 年份 | 2024 |
| 会议/期刊 | ACM Web Conference 2024 (WWW '24), May 13-17, 2024, Singapore |
| 研究方向 | 匿名流量分类、加密流量分析、深度学习 |
| 任务类型 | anonymous network traffic classification（匿名网络流量分类）、VPN traffic classification |
| 方法关键词 | short-term representation learning, high temperature self-attention, multi-modal fusion, representation enhancement, bidirectional GRU |
| 数据集 | SJTU-AN21, ISCX-Tor, ISCX-VPN, USTC-TFC, Cross-Platform |
| 是否开源 | 是 (https://github.com/SJTU-dxw/AN-Net) |
| PDF | 00-inbox/PDFs/2024-WWW-AN-Net__an_Anti-Noise_Network_for_Anonymous_Traffic_Classification.pdf |
| MinerU Markdown | 02-parsed-markdown/2024-WWW-AN-Net__an_Anti-Noise_Network_for_Anonymous_Traffic_Classification.md |

## 1. 一句话总结

> 针对匿名网络（如 Tor）中因 triple proxy 导致的 irrelevant packet noise 和网络环境波动导致的 per-packet attribute noise，提出 AN-Net 通过短期表征学习（short-term representation learning）配合高温自注意力机制（high temperature self-attention）抵抗无关包噪声，并通过增强的多模态融合（enhanced multi-modal fusion）对抗逐包属性噪声，在三个数据集上达到 SOTA，SJTU-AN21 的 F1 提升至 94.39%（6.24% 提升）。

## 2. 摘要翻译

### 2.1 摘要原文

Anonymous networks employ a triple proxy to transmit packets to enhance user privacy, causing traffic packets from all applications and web services to form a unified flow. The traditional approach of applying flow-level encrypted traffic classification methods to anonymous traffic (i.e., treating consecutive packets as a single flow) is hindered by irrelevant packet noise. Moreover, fluctuations in the network environment can introduce per-packet attribute noise and discrepancies between training and test data. How to extract robust patterns from consecutive packets replete with noise remains a key challenge. In this paper, we propose the Anti-Noise Network (AN-Net) to construct robust short-term representations for a single modality, effectively countering irrelevant packet noise. We also incorporate an enhanced multi-modal fusion approach to combat per-packet attribute noise. AN-Net achieves state-of-the-art performance across two anonymous traffic classification tasks and one VPN traffic classification task, notably elevating the F1 score of SJTU-AN21 to 94.39% (6.24%↑). Our code and dataset are available on https://github.com/SJTU-dxw/AN-Net.

### 2.2 摘要中文翻译

匿名网络使用 triple proxy 传输数据包以增强用户隐私，导致来自所有应用和 Web 服务的流量数据包形成统一的流（flow）。将传统的流级别加密流量分类方法应用于匿名流量（即将连续数据包视为一个流）会受到 irrelevant packet noise（无关包噪声）的干扰。此外，网络环境的波动会引入 per-packet attribute noise（逐包属性噪声）以及训练数据和测试数据之间的差异。如何从充满噪声的连续数据包中提取鲁棒的模式仍然是一个关键挑战。本文提出了 Anti-Noise Network（AN-Net），为单一模态构建鲁棒的短期表征（short-term representation），有效对抗 irrelevant packet noise。同时采用增强的多模态融合方法来对抗 per-packet attribute noise。AN-Net 在两个匿名流量分类任务和一个 VPN 流量分类任务上达到了 state-of-the-art 性能，特别是将 SJTU-AN21 的 F1 score 提升至 94.39%（提升 6.24%）。

## 3. 方法动机

### 3.1 匿名流量中的两类噪声问题

匿名网络流量分类的核心困难在于**噪声**，论文精确定义了两类性质不同的噪声：

**Irrelevant Packet Noise（无关包噪声）**：Tor 网络使用 triple proxy（入口节点、中继节点、出口节点）传输流量，所有经过同一 Tor 网关的应用流量被混合成一条 flow。因此，将连续数据包视为一个 flow 时，其中必然包含来自其他应用/服务的数据包，这些就是 irrelevant packets。论文用 Figure 2 定量展示了这一问题的严重性：在 ISCX-Tor 数据集上，10 个连续包来自同一流的可能性约 66%；而 50 个连续包时降至约 50%；100 个包时降至约 25%。这意味着传统 flow-level 方法中大量数据包实际来自不同的服务，形成严重的标签噪声。

**Per-Packet Attribute Noise（逐包属性噪声）**：即使数据包来自目标流，其属性也可能因网络环境波动而不可靠。具体而言：
- **IAT（Internal Arrival Time）**：受网络拥塞、排队延迟影响，同一应用在不同网络条件下 IAT 分布差异显著
- **TTL（Time-to-Live）**：因网络路由变化而改变，不同路径的 TTL 值可能不同
- **Payload**：加密算法更新或 TLS 版本变化导致同一应用的 payload 模式发生改变（论文在 Table 5 中展示了 Stat-SFEM 比 Raw-SFEM 在 SJTU-AN21 上 AC 高 4.21%、F1 高 3.41%，正是因为 raw payload 在跨域场景中过拟合）

### 3.2 现有方法为何在匿名流量场景下失效

现有方法的根本问题在于它们的设计假设与匿名流量的现实不符：

| 方法类别 | 设计假设 | 在匿名流量中的失效原因 |
|---|---|---|
| Statistical feature-based (AppScanner, Decision Tree, Whisper) | 一个 flow 内的数据包来自同一服务 | 长期统计特征（如 flow-level mean、max、std）被 irrelevant packets 严重污染。在 75% 噪声注入下，F1 下降 36-43% |
| Sequential attribute-based (Flowlens, FS-Net) | 包序列的时序模式反映应用行为 | 虽然能自动学习模式，但仍受无关包干扰。FS-Net 在 SJTU-AN21 上 F1 仅 79.49%，75% 噪声下下降 17.9% |
| Raw traffic-based (AttnLSTM, ET-Bert) | payload 包含足够的分类信息 | payload 来自无关包会直接导致错误识别。ET-Bert 在 75% 噪声下 F1 下降超 64.6%，AttnLSTM 下降超 69.6% |

关键洞察：**所有现有方法都没有区分"哪些数据包来自目标流、哪些来自无关流"的能力**。它们要么在 flow-level 上聚合（无法过滤无关包），要么在 raw payload 上直接学习（无法区分 payload 来源）。

### 3.3 "Anti-Noise" 的核心思想

AN-Net 的 anti-noise 策略是**分而治之**：
1. **对抗 irrelevant packet noise**：不直接在 flow-level 学习，而是先将 flow 分割为短期序列（short-term sequences），利用"短期连续包更可能来自同一流"的统计规律从源头降低噪声。然后通过高温自注意力机制（HT-SelfAttention）在聚合阶段进一步抑制无关包的短期特征。
2. **对抗 per-packet attribute noise**：不依赖单一模态，而是融合多个模态（packet size, IAT, TTL, TCPFlag），不同模态在网络波动下的可靠性不同，可以互相验证、互相补偿。同时通过表征增强策略（Representation Enhancement）迫使模型从含噪声的模态中也能学到有用信息。

这一设计的精妙之处在于：**攻击者要同时干扰所有短期序列的所有模态才能成功逃逸**，这在实际中极其困难。

## 4. 方法设计

### 4.1 端到端模型架构

AN-Net 由两个核心模块组成：**Uni-modal Short-term Representation Learning Module**（单模态短期表征学习）和 **Enhanced Multi-modal Representation Fusion Module**（增强多模态表征融合）。整体架构如下：

**阶段一：单模态短期表征学习**
1. **Flow Division（流分割）**：给定一个长度为 L 的连续包序列 P，将其均分为 N 个短期序列 P=[P1, P2, ..., PN]。每个短期序列包含 l=L/N 个连续包。核心直觉来自论文 Figure 2 的实证观察：10 个连续包内来自同一流的可能性约 50-66%，远高于 100 个包时的 25%。
2. **Packet Parsing（包解析）**：从每个短期序列中解析出各模态的属性序列 A=[A1, A2, ..., AN]，包括 packet size、IAT、TTL、IPFlag、TCPFlag 和 payload。
3. **Short-term Feature Extraction（短期特征提取）**：通过 SFEM 从每个 Ai 中提取 C 维特征向量 Fi，得到短期特征矩阵 F=[F1, F2, ..., FN] ∈ R^{N×C}。
4. **Short-term Representation Aggregation（短期表征聚合）**：通过 HT-SelfAttention 机制聚合 F 为流级别单模态表征 Z ∈ R^C，通过平均池化输出。

**阶段二：增强多模态表征融合**
5. **Modal Selection（模态选择）**：基于互信息 I(T;G) 去除低信息泄漏的无用模态。
6. **Representation Enhancement（表征增强）**：在表征级别进行数据增强（随机置零或 Beta 缩放）。
7. **Representation Fusion（表征融合）**：平均池化融合增强后的各模态表征，FC 层 + softmax 输出分类结果。

### 4.2 短期特征提取的两种 SFEM 设计

论文设计了两种 Short-term Feature Extraction Module，针对不同数据特性：

**Raw-SFEM**：直接处理原始属性序列
- 输入：短期序列 Ai ∈ R^{l×d}（payload）或 Ai ∈ R^{l×1}（单一属性如 packet size）
- 处理：对单一属性先通过 embedding layer 映射到向量空间，然后用双向 GRU（Bidirectional GRU）提取时序特征
- 输出：Fi ∈ R^C（C 为 GRU 隐藏维度）
- 适用场景：训练数据与测试数据网络环境一致（如 ISCX-Tor、ISCX-VPN）

**Stat-SFEM**：基于统计特征提取
- 输入：短期序列 Ai ∈ R^{l×1}
- 处理：先提取 7 种统计特征（mean, max, min, median, standard deviation, skewness, kurtosis）和频域特征，然后用两层 MLP（FC → ReLU → FC）提取特征
- 输出：Fi ∈ R^C
- 适用场景：训练数据与测试数据网络环境不一致（如 SJTU-AN21），因为高级统计特征比原始属性序列更稳定、更具迁移性
- 关键优势：Stat-SFEM 在 SJTU-AN21 上比 Raw-SFEM AC 高 4.21%、F1 高 3.41%（Table 5），因为统计特征衡量的是分布和变化，而非具体的原始值

### 4.3 高温自注意力机制（HT-SelfAttention）的完整数学推导

这是论文的核心创新。从标准自注意力出发，逐步推导到高温自注意力：

**标准自注意力**：给定短期特征矩阵 F ∈ R^{N×C}，通过线性变换得到：
- Q = F·W^Q ∈ R^{N×D}（Query 矩阵，W^Q ∈ R^{C×D} 为可学习参数）
- K = F·W^K ∈ R^{N×D}（Key 矩阵）
- V = F·W^V ∈ R^{N×D}（Value 矩阵）

对于第 i 个短期特征的 query 向量 qi，计算与所有 key 向量的点积：
$$S_i = [q_i \cdot k_1^T, q_i \cdot k_2^T, ..., q_i \cdot k_N^T] = [s_{i1}, s_{i2}, ..., s_{iN}]$$

标准自注意力缩放后应用 softmax：
$$W_i = \text{softmax}(S_i / \sqrt{D}) = [w_{i1}, w_{i2}, ..., w_{iN}], \quad \sum_{j=1}^N w_{ij} = 1$$

**高温自注意力的关键修改**：
$$\text{HT-SelfAttn}(F) = \text{softmax}\left(\frac{\mathcal{N}(Q)\mathcal{N}(K)^T}{\tau}\right)V$$

其中：
- **N（归一化函数）**：使向量范数等于 1，确保点积的范围在 [-1, 1] 之间
- **τ（温度超参数）**：τ << 1 表示高温（论文中 τ=0.1）。注意：实际温度是 1/τ，τ 越小温度越高
- **核心区别**：标准自注意力用 1/√D 缩放以避免 softmax 饱和；HT-SelfAttention 故意用极小的 τ 放大点积，使 softmax 产生尖锐分布

**为什么高温能过滤噪声？（理论证明，见 Appendix A）**：

将点积向量 S 分解为幅度 ||S|| 和方向 Ŝ：S = ||S|| · Ŝ。对于来自无关流的短期特征 k，其点积值 ŝ_k = min(ŝ_j) 是最小的。设 t = ||S|| · (1/τ - 1) > 0，则：

$$w_k' = \frac{e^{(||S||+t)\hat{s}_k}}{\sum_{j=1}^N e^{(||S||+t)\hat{s}_j}} = \frac{e^{||S||\hat{s}_k}}{\sum_{j=1}^N e^{||S||\hat{s}_j + t(\hat{s}_j - \hat{s}_k)}}$$

由于对所有 j 都有 ŝ_j - ŝ_k ≥ 0，因此 **w_k' ≤ w_k**，即高温自注意力使无关流的权重严格不大于标准自注意力的权重。

**可视化验证（Figure 7）**：在 50% 噪声注入的实验中，HT-SelfAttention 对无关流的短期特征赋予极小权重（0.00 或 0.05），而对目标流的特征赋予较大权重（0.10-0.28），形成明显的块状对角结构。

**温度参数 τ 的影响（Figure 5）**：
- 0% 噪声时：τ=0.0 对应 F1≈94.5%，τ=1.0 降至约 93.5%（提升约 1%）
- 75% 噪声时：τ=0.0 对应 F1≈91.6%，τ=1.0 降至约 91.0%（提升约 0.6%）
- 结论：高温效应在高噪声场景下更显著，但即使在无噪声时也有小幅提升

### 4.4 多模态融合的完整设计

**模态选择（Modal Selection）**：

利用互信息度量各模态的信息泄漏量：
$$I(T; G) = H(G) - H(G|T)$$

其中 T 是模态的统计特征，G 是真实标签。论文在 Appendix I 中给出了各数据集的具体互信息值：

| 数据集 | Packet Size | IAT | TTL | IPFlag | TCPFlag |
|---|---|---|---|---|---|
| SJTU-AN21 | 0.81 | 0.81 | 1.50 | **0.01** (去除) | 0.99 |
| ISCX-Tor | 1.14 | 0.82 | **0.00** (去除) | 0.95 | 0.84 |
| ISCX-VPN | 0.68 | 0.75 | 1.34 | **0.23** (去除) | **0.42** (去除) |

选择策略：去除互信息最低的模态以降低模型复杂度。

**表征增强策略（Representation Enhancement）的理论分析**：

$$\hat{Z}_i = \begin{cases} 0, & \text{with probability } p=0.2 \\ B \times Z_i, & \text{with probability } 1-p \end{cases}$$

其中 B ~ Beta(4,4) 分布采样。

为什么需要表征增强？论文在 Appendix B 中给出了严格的梯度分析：

当模型从某个模态（如 TTL）获得足够信息产生高置信度预测时（q_k → 1, q_j → 0 for j≠k），损失函数对表征的梯度趋近于 0：
$$\frac{\partial \mathcal{L}}{\partial z_i} = \sum_{j=1}^K q_j w_{ji} - w_{ki} \rightarrow 0$$

这意味着模型会**忽略**从含噪声的模态（如 Packet Size）学习。表征增强通过随机置零迫使模型不能过度依赖任何单一模态，从而从每个模态中都学习到有用信息。

**实验验证（Table 6）**：在 Packet Size 模态注入 50% 噪声的实验中：
- Add 融合：Packet Size 模态的独立准确率仅 35.11%，模型几乎完全依赖 TTL
- Concatenation 融合：Packet Size 模态准确率仅 21.48%，更差
- RE 融合：Packet Size 模态准确率达 67.79%，模型成功从噪声模态中提取了有用信息

### 4.5 训练策略与噪声建模

**训练配置**：
- 优化器：SGD，学习率 0.001
- Batch size：64
- 总训练步数：50,000
- 损失函数：交叉熵 L = CE(Ŷ, Y)
- 温度参数 τ=0.1
- 随机丢弃概率 p=0.2
- 缩放因子 B ~ Beta(4,4)

**噪声注入方式（Appendix H）**：论文使用 CICIOT 数据集的 TLS 流量作为噪声源。对于输入包序列 L 和噪声比例 η，随机插入 η×L 个连续 TLS 噪声包到 L×(1-η) 个正常包中。噪声以连续包的形式注入（而非随机散布），更贴近真实场景。

### 4.6 方法优势

1. **对 irrelevant packet noise 鲁棒**：短期表征学习 + 高温自注意力机制有效过滤无关包，F1 波动在 SJTU-AN21 上仅 2.39%，ISCX-VPN 上仅 0.32%
2. **对 per-packet attribute noise 鲁棒**：多模态融合使得不同模态可以互相验证，单一模态的噪声被其他模态补偿
3. **训练数据效率高**：在仅使用 10% 训练数据时，AN-Net 的 F1 仍达 89.30%，远优于其他方法（ET-Bert 仅 56.63%）
4. **轻量级且实时**：推理时间 39.41 μs/pkt（每秒可分类约 2500 个包），参数量仅 2.40M，内存占用 1477 MiB，远轻于 ET-Bert（132.13M 参数，17379 MiB）
5. **泛化能力强**：Stat-SFEM 在训练数据与测试数据网络环境不一致时表现更优，因为高级统计特征衡量的是分布和变化，而非具体的原始值

### 4.7 方法不足

1. **数据集限制**：主要在三个数据集上验证，其中 SJTU-AN21 是作者团队自己收集的数据集，外部可复现性需进一步验证
2. **噪声模型假设简化**：假设攻击者随机选择 TLS 包序列作为噪声流量，实际对抗场景中攻击者可能故意模仿目标流的统计特征
3. **短期序列长度需调优**：论文未详细讨论如何确定最优的短期序列长度 l（或等价地，分割数 N）
4. **高温参数敏感性**：τ 的选择对性能有一定影响（Figure 5），需要根据场景调优；理论上 τ→0 时梯度可能消失
5. **SFEM 选择依赖人工判断**：需要根据训练数据与测试数据环境是否一致来选择 Stat-SFEM 或 Raw-SFEM，缺乏自动选择机制
6. **Payload 模态的局限**：在跨域场景（SJTU-AN21）中，payload 模态反而降低性能（F1 下降 0.48%），说明 raw payload 特征的迁移性较差

## 5. 与其他方法对比

### 5.1 与 ET-BERT 的深度对比

ET-Bert 是论文中最强的 baseline，也是最直接的对比对象：
- **ET-Bert 的方法**：在大规模无标注原始流量上预训练 Transformer，学习 datagram-level 的上下文化表征，然后在小规模标注数据上微调
- **ET-Bert 的优势**：在干净数据集上表现优异（ISCX-VPN 上 F1=98.88%），预训练带来了较强的泛化能力
- **ET-Bert 的致命弱点**：(1) 在匿名流量场景下，irrelevant packets 的 payload 直接被编码为表征，导致错误分类；(2) 在噪声攻击下极其脆弱——75% 噪声时 F1 下降超 64.6%；(3) 计算资源需求极大（132.13M 参数，训练时间 49.51 分钟，推理时间 169.34 μs/pkt）
- **AN-Net 的优势**：不依赖 raw payload（SJTU-AN21 上 Stat-SFEM 不含 payload 反而更好），通过短期表征 + 多模态融合从根本上解决噪声问题，且模型轻量 55 倍（2.40M vs 132.13M 参数）

### 5.2 与 NetMamba、TrafficLLM 等新方法的对比思路

虽然论文发表于 2024 年 WWW，未直接对比 NetMamba 和 TrafficLLM，但可以从方法论角度分析：

- **NetMamba**：基于 Mamba（State Space Model）的加密流量分类，擅长建模长序列依赖。但在匿名流量场景下，长序列中包含大量 irrelevant packets，Mamba 的序列建模能力反而可能被噪声误导。AN-Net 的短期序列分割策略从源头避免了这一问题。
- **TrafficLLM**：基于大语言模型的流量分类，通过将流量转换为 token 序列进行分类。LLM 的强大表征能力在干净数据上有优势，但面对 irrelevant packet noise 时，token 序列中的噪声 token 同样难以过滤。AN-Net 的高温自注意力机制提供了一种显式的噪声过滤手段。
- **关键区别**：AN-Net 是**专门为噪声场景设计**的，其每个组件（短期分割、HT-SelfAttention、多模态融合、表征增强）都针对噪声鲁棒性。而 NetMamba 和 TrafficLLM 更多关注表征能力的提升，未显式处理噪声问题。

### 5.3 AN-Net 抗噪声能力的本质原因

AN-Net 之所以在噪声下表现优异，根本原因在于其**多层防御机制**：

| 防御层 | 对抗的噪声类型 | 机制 | 效果 |
|---|---|---|---|
| 第一层：短期序列分割 | Irrelevant Packet Noise | 利用"短期包更可能来自同一流"的统计规律 | 从源头降低噪声比例 |
| 第二层：HT-SelfAttention | Irrelevant Packet Noise | 高温 softmax 产生尖锐权重分布，抑制无关流特征 | 对无关流特征权重接近零 |
| 第三层：多模态融合 | Per-Packet Attribute Noise | 不同模态互相验证、互相补偿 | 单模态噪声被其他模态补偿 |
| 第四层：表征增强 | Per-Packet Attribute Noise | 随机置零/缩放迫使模型不依赖单一模态 | 从含噪声模态中也能学习 |
| 第五层：互信息模态选择 | 信息冗余 | 去除低信息泄漏的无用模态 | 降低噪声模态的干扰 |

这种多层防御使得攻击者需要**同时干扰所有短期序列的所有模态**才能成功逃逸，实际中极其困难。

### 5.4 适用场景

- **匿名网络（Tor/I2P）流量分类**：识别通过匿名网络传输的应用类型——AN-Net 的核心设计场景
- **VPN 流量分类**：VPN 同样使用代理传输信息，面临类似的无关包噪声问题
- **存在噪声干扰的加密流量分类场景**：任何 flow 中可能混入无关包的场景
- **训练数据与测试数据网络环境不一致的跨域场景**：使用 Stat-SFEM 可获得更强的迁移性
- **需要实时分类的场景**：推理速度约 2500 pkt/s（39.41 μs/pkt），满足实时需求
- **训练数据有限的场景**：仅用 10% 数据时 F1 仍达 89.30%，远优于 ET-Bert 的 56.63%

### 5.5 方法对比表

| 方法 | 类型 | SJTU-AN21 F1 | ISCX-Tor F1 | ISCX-VPN F1 | 75%噪声下F1波动 | 参数量 | 推理时间(μs/pkt) |
|---|---|---|---|---|---|---|---|
| AppScanner | 统计特征+RF | 0.7038 | 0.8022 | 0.7193 | ≤43%↓ | - | - |
| Decision Tree | 统计特征+C4.5 | 0.5621 | 0.7942 | 0.8211 | ≤36.5%↓ | - | - |
| Whisper | 频域特征+聚类 | 0.5066 | 0.6975 | 0.5486 | ≤36.7%↓ | - | - |
| Flowlens | flow marker+NB | 0.7128 | 0.8256 | 0.5820 | 中等 | - | - |
| FS-Net | RNN enc-dec | 0.7949 | 0.9315 | 0.8398 | ≤17.9%↓ | 5.14M | 13.41 |
| AttnLSTM | LSTM+Attention | 0.8030 | 0.9708 | 0.9778 | ≥69.6%↓ | 0.25M | 4.29 |
| ET-Bert | 预训练Transformer | 0.8815 | 0.9445 | 0.9888 | ≥64.6%↓ | 132.13M | 169.34 |
| **AN-Net** | **短期表征+多模态** | **0.9439** | **0.9950** | **0.9996** | **<2.4%↓** | **2.40M** | **39.41** |

### 5.6 计算复杂度对比

| 方法 | 训练时间(min) | 推理时间(μs/pkt) | 内存(MiB) | 参数量(M) | FLOPs(M) |
|---|---|---|---|---|---|
| FS-Net | 15.83 | 13.41 | 2813 | 5.14 | 256.01 |
| AttnLSTM | 1.93 | 4.29 | 1385 | 0.25 | 0.33 |
| ET-Bert | 49.51 | 169.34 | 17379 | 132.13 | 48318.97 |
| **AN-Net** | **18.41** | **39.41** | **1477** | **2.40** | **23.94** |

AN-Net 在参数量、内存和 FLOPs 上远优于 ET-Bert 和 FS-Net，同时推理速度也快于 ET-Bert 约 4.3 倍。AttnLSTM 虽然更轻量，但其抗噪声能力极差（F1 下降超 69.6%），实际部署价值有限。

## 6. 实验表现与优势

### 6.1 实验设置

- **数据集**：三个主要数据集（SJTU-AN21, ISCX-Tor, ISCX-VPN），两个额外数据集（USTC-TFC, Cross-Platform）
- **流定义**：取 100 个连续数据包作为一个 flow
- **训练设置**：SGD 优化器，学习率 0.001，batch size 64，总步数 50,000，温度参数 τ=0.1，随机丢弃概率 p=0.2，缩放因子 B~Beta(4,4)
- **硬件**：Intel Xeon Gold 5218R CPU@2.10GHz, 256 GB RAM, NVIDIA GeForce RTX3090 GPU
- **实现**：Pytorch 1.9.0
- **SFEM 选择**：ISCX-VPN 和 ISCX-Tor 使用 Raw-SFEM；SJTU-AN21 使用 Stat-SFEM（不含 payload）

### 6.2 主要结果（Table 1）

| 数据集 | 指标 | AN-Net | 最佳 Baseline | 提升幅度 | 备注 |
|---|---|---|---|---|---|
| SJTU-AN21 | AC | 0.9476 | 0.8661 (ET-Bert) | **+8.15%** | 噪声最大+跨域数据集 |
| SJTU-AN21 | F1 | 0.9439 | 0.8815 (ET-Bert) | **+6.24%** | 此前方法从未超过 90% |
| ISCX-Tor | AC | 0.9951 | 0.9725 (AttnLSTM) | +2.26% | 干净大数据集 |
| ISCX-Tor | F1 | 0.9950 | 0.9708 (AttnLSTM) | +2.42% | |
| ISCX-VPN | AC | 0.9996 | 0.9885 (ET-Bert) | +1.11% | VPN 流量 |
| ISCX-VPN | F1 | 0.9996 | 0.9888 (ET-Bert) | +1.08% | |

**额外数据集（Appendix C）**：
| 数据集 | AN-Net F1 | 最佳 Baseline F1 | 提升 |
|---|---|---|---|
| USTC-TFC | 0.9980 | 0.9832 (ET-Bert) | +1.48% |
| Cross-Platform | 0.9967 | 0.9937 (ET-Bert) | +0.30% |

### 6.3 噪声攻击鲁棒性（Figure 4）

注入不同比例（0-75%）的无关包噪声后的 F1 score 变化：

| 方法 | SJTU-AN21 (0%) | SJTU-AN21 (75%) | ISCX-Tor (75%) | ISCX-VPN (75%) | 最大F1下降 |
|---|---|---|---|---|---|
| AppScanner | 0.7038 | ~0.40 | - | - | ≤43% |
| Decision Tree | 0.5621 | ~0.36 | - | - | ≤36.5% |
| Whisper | 0.5066 | ~0.32 | - | - | ≤36.7% |
| FS-Net | 0.7949 | ~0.62 | - | - | ≤17.9% |
| AttnLSTM | 0.8030 | ~0.10 | - | - | ≥69.6% |
| ET-Bert | 0.8815 | ~0.15 | - | - | ≥64.6% |
| **AN-Net** | **0.9439** | **0.9200** | **0.9071** | **0.9933** | **<2.4%** |

关键发现：
- AttnLSTM 和 ET-Bert 在噪声攻击下**几乎完全失效**（F1 下降 64-70%），因为它们直接学习 raw payload，来自无关包的 payload 直接导致错误分类
- 统计特征方法（AppScanner, Decision Tree, Whisper）也严重受损（F1 下降 36-43%），因为长期统计特征被无关包污染
- FS-Net 相对较好（下降 ≤17.9%），因为 RNN 在一定程度上能保留部分干净序列的模式
- **AN-Net 几乎不受影响**（SJTU-AN21 下降仅 2.39%，ISCX-VPN 下降仅 0.32%），因为短期分割 + HT-SelfAttention 能有效过滤无关包

### 6.4 消融实验

**短期特征 vs 长期特征 + HT-SelfAttention（Table 2，在 SJTU-AN21 上）**：

| 特征类型 | HT | 0% 噪声 | 25% 噪声 | 50% 噪声 | 75% 噪声 |
|---|---|---|---|---|---|
| Long-Term | / | 0.9427 | 0.9276 | 0.9093 | 0.7295 |
| Short-Term | ✗ | 0.9352 | 0.9329 | 0.9327 | 0.9068 |
| Short-Term | ✓ | **0.9439** | **0.9430** | **0.9423** | **0.9200** |

关键发现：
- 长期特征在 75% 噪声下 F1 暴跌至 72.95%，而短期特征 + HT 仍保持 92.00%（差距 19.05%）
- HT-SelfAttention 的提升随噪声增加而增大：0% 噪声提升 0.87%，75% 噪声提升 1.32%

**多模态消融（Table 3，在 SJTU-AN21 上）**：

| Packet Size | IAT | TTL | TCPFlag | AC | F1 |
|---|---|---|---|---|---|
| ✓ | ✗ | ✗ | ✗ | 0.7958 | 0.8014 |
| ✓ | ✓ | ✗ | ✗ | 0.8314 | 0.8304 |
| ✓ | ✓ | ✓ | ✗ | 0.9269 | 0.9234 |
| ✓ | ✓ | ✓ | ✓ | **0.9476** | **0.9439** |

关键发现：仅用 packet size 单模态 F1=80.14%，四模态融合后 F1=94.39%（提升 14.25%）。每增加一个模态都有显著提升，说明模态间的互补性很强。

**表征增强消融（Table 4）**：

| RE | SJTU-AN21 (50%) | SJTU-AN21 (75%) | ISCX-Tor (50%) | ISCX-Tor (75%) | ISCX-VPN (50%) | ISCX-VPN (75%) |
|---|---|---|---|---|---|---|
| ✗ | 0.9378 | 0.9101 | 0.9334 | 0.8934 | 0.9957 | 0.9881 |
| ✓ | 0.9423 | 0.9200 | 0.9377 | 0.9071 | 0.9964 | 0.9933 |

关键发现：表征增强的提升随噪声增加而增大（SJTU-AN21：0.45%→0.99%，ISCX-Tor：0.43%→1.37%）。

### 6.5 训练数据效率（Table 10）

| 方法 | 100% 数据 | 50% 数据 | 30% 数据 | 10% 数据 |
|---|---|---|---|---|
| FS-Net | 0.7949 | 0.6074 | 0.5916 | 0.6012 |
| AttnLSTM | 0.8030 | 0.6137 | 0.6040 | 0.5682 |
| ET-Bert | 0.8815 | 0.8305 | 0.7863 | 0.5663 |
| **AN-Net** | **0.9439** | **0.9207** | **0.9153** | **0.8930** |

关键发现：AN-Net 在 10% 数据时 F1 仍达 89.30%，而 ET-Bert 暴跌至 56.63%。这是因为 AN-Net 使用统计特征（Stat-SFEM）和多模态信息，对数据量的依赖较低。

### 6.6 短流分类（Table 9，流长度截断为 10 包）

| 方法 | AC | F1 | F1 下降幅度 |
|---|---|---|---|
| FS-Net | 0.5870 | 0.5706 | 22.43%↓ |
| AttnLSTM | 0.6965 | 0.6627 | 14.03%↓ |
| ET-Bert | 0.8693 | 0.8544 | 2.71%↓ |
| **AN-Net** | **0.8987** | **0.9002** | **4.37%↓** |

关键发现：AN-Net 和 ET-Bert 是仅有的两个能有效分类短流的方法。ET-Bert 通过大规模预训练获得鲁棒性，AN-Net 通过多模态融合补偿信息不足。

### 6.7 优势最明显的场景

1. **SJTU-AN21（噪声最大 + 跨域）**：F1 提升 6.24%，因为该数据集噪声最大且训练/测试环境不一致，Stat-SFEM 的统计特征迁移性优势充分体现
2. **高噪声注入场景**：75% 噪声下其他方法几乎失效，AN-Net 仍保持 90%+ F1
3. **训练数据有限场景**：10% 数据时 F1=89.30%，比 ET-Bert 高 32.67%
4. **短流场景**：10 包时 F1=90.02%，仅次于 ET-Bert 但差距很小

### 6.8 稳定性分析（Table 5，SJTU-AN21）

| SFEM | Payload | AC | F1 | 说明 |
|---|---|---|---|---|
| Raw-SFEM | ✗ | 0.9055 | 0.9098 | 原始属性序列，无 payload |
| Stat-SFEM | ✓ | 0.9358 | 0.9391 | 统计特征 + payload |
| Stat-SFEM | ✗ | **0.9476** | **0.9439** | 统计特征，无 payload（最佳） |

关键发现：(1) Stat-SFEM 比 Raw-SFEM AC 高 4.21%，F1 高 3.41%；(2) 加入 payload 模态反而降低性能（F1 下降 0.48%）。原因：当训练数据与测试数据网络环境不一致时，raw payload 和 raw attribute 序列会过拟合训练环境的特定模式（如加密算法版本），而统计特征衡量的是分布和变化，更具迁移性。

### 6.9 局限性

1. **数据集局限**：SJTU-AN21 是作者自建数据集，外部可复现性需进一步验证
2. **噪声模型假设**：攻击者随机注入 TLS 噪声包的假设较理想化，实际对抗中攻击者可能故意模仿目标流的统计特征
3. **参数选择**：短期序列长度 l、温度参数 τ 等超参数需要针对具体场景调优
4. **Payload 模态的局限**：在跨域场景中 payload 模态反而降低性能，需要根据场景决定是否使用
5. **SFEM 选择依赖人工**：需要人工判断训练/测试环境是否一致来选择 Stat-SFEM 或 Raw-SFEM

## 7. 学习与应用

### 7.1 是否开源？

是。代码和数据集均开源：https://github.com/SJTU-dxw/AN-Net

### 7.2 复现关键步骤

1. **数据准备**：下载 SJTU-AN21、ISCX-Tor、ISCX-VPN 数据集，将连续 100 个包定义为一个 flow
2. **特征提取**：对每个 flow 分割为 N 个短期序列，提取各模态属性（packet size, IAT, TTL, IPFlag, TCPFlag, payload）
3. **模态选择**：计算各模态统计特征与标签的互信息 I(T;G)，去除低信息泄漏模态
4. **模型构建**：搭建 AN-Net 架构（SFEM + HT-SelfAttention + 多模态融合）
5. **训练**：SGD 优化器，lr=0.001，batch_size=64，50000 步，τ=0.1，p=0.2，B~Beta(4,4)
6. **评估**：在测试集上计算 AC, PR, RC, F1，并进行噪声注入鲁棒性测试

### 7.3 关键超参数、预处理和训练细节

| 参数 | 值/说明 |
|---|---|
| 短期序列长度 l | 未明确给出具体值，每个 flow 分为 N 个短期序列 |
| Flow 长度 | 100 个连续包 |
| 温度参数 τ | 0.1（实际温度为 1/τ = 10） |
| 随机丢弃概率 p | 0.2 |
| 缩放因子 B | 从 Beta(4,4) 分布采样（均值 0.5，方差较小，集中在 0.5 附近） |
| 优化器 | SGD，学习率 0.001 |
| Batch size | 64 |
| 总训练步数 | 50,000 |
| 隐藏维度 C | 未明确给出 |
| 自注意力维度 D | 未明确给出 |
| 统计特征 | mean, max, min, median, std, skewness, kurtosis + 频域特征 |
| SFEM 选择 | ISCX-VPN/ISCX-Tor 用 Raw-SFEM；SJTU-AN21 用 Stat-SFEM（不含 payload） |

### 7.4 能否迁移到其他任务？

- **其他加密流量分类**：在 USTC-TFC 和 Cross-Platform 通用加密流量数据集上也验证了有效性（F1 分别为 99.80% 和 99.67%）
- **恶意软件流量检测**：短期表征学习和多模态融合的思路可迁移到恶意软件流量检测场景，因为恶意软件流量也可能混入正常流量中
- **其他存在噪声的序列分类任务**：高温自注意力机制可应用于任何需要从噪声序列中提取鲁棒模式的任务（如音频分类中的背景噪声、传感器数据中的异常读数）
- **跨域流量分类**：Stat-SFEM 的稳定性分析表明统计特征在跨域场景中更鲁棒，这一发现对其他需要跨域迁移的任务也有启发
- **短流分类**：AN-Net 在短流（10 个包）上也表现优异（F1=90.02%），可迁移到需要快速分类的实时场景

### 7.5 与 MOTA 论文噪声注入方法的关系

AN-Net 的噪声鲁棒性设计与 MOTA 论文中通过噪声注入增强模型鲁棒性的思路形成有趣的对比和互补：

| 维度 | AN-Net | MOTA（噪声注入） |
|---|---|---|
| 噪声处理策略 | 显式建模噪声结构，设计针对性过滤机制 | 通过在训练数据中注入噪声，让模型隐式学习噪声鲁棒性 |
| 核心机制 | 短期分割 + HT-SelfAttention + 多模态融合 | 数据增强（噪声注入）+ 模型训练 |
| 噪声类型 | 两类：irrelevant packet noise + per-packet attribute noise | 通用噪声注入 |
| 优势 | 针对性强，效果显著（F1 波动 <2.4%） | 通用性强，不依赖噪声结构的先验知识 |
| 局限 | 需要对噪声结构有一定先验知识 | 噪声注入的分布需要与真实噪声匹配 |

**互补思路**：可以将两种方法结合——用 AN-Net 的短期分割和 HT-SelfAttention 作为模型架构，同时在训练时注入噪声（如 MOTA 的方法）来进一步增强鲁棒性。这种组合可能在更复杂的对抗场景中表现更好。

### 7.6 对我的研究有什么启发？

1. **噪声建模的重要性**：匿名流量分类的核心挑战是噪声（irrelevant packet noise + per-packet attribute noise），显式建模噪声并设计针对性机制是关键。这比简单地增加模型容量更有效——ET-Bert 有 132M 参数但在噪声下仍然失效。
2. **短期特征的直觉**：利用"短期连续包更可能来自同一流"这一简单直觉，可以有效缓解混合流问题。这种利用数据的局部统计规律来降低噪声的方法具有普适性。
3. **高温自注意力的思想**：通过调节 softmax 温度控制注意力分布的尖锐程度，是一个通用且有效的噪声过滤机制。这一思想可以应用于任何注意力机制中需要抑制噪声输入的场景。
4. **多模态融合的互补性**：不同模态在网络波动下的可靠性不同，融合多模态可以互相验证、提高鲁棒性。关键发现是表征增强策略解决了"模型忽略噪声模态"的问题（Appendix B 的梯度分析）。
5. **表征增强 vs 输入增强**：在输入数据类型受限（数值型）时，可以在表征级别进行数据增强。这一思路比传统的输入增强（如加噪声、裁剪）更适合流量数据的特性。
6. **统计特征 vs 原始特征的 trade-off**：统计特征在跨域场景更稳定但可能损失细节；原始特征更精细但易过拟合。AN-Net 的 Stat-SFEM vs Raw-SFEM 的实验（Table 5）清晰地展示了这一 trade-off，对选择特征提取方式有直接指导意义。
7. **轻量级设计的价值**：AN-Net 仅用 2.40M 参数就超过了 132.13M 参数的 ET-Bert，说明针对问题特点设计精巧的架构比盲目增大模型更有效。

## 8. 总结

### 8.1 核心思想（不超过20字）

通过短期表征和多模态融合抵抗匿名流量中的两种噪声。

### 8.2 速记版 Pipeline（3-5步）

1. 将 flow 中连续包分割为多个短期序列（short-term sequences）
2. 用 SFEM（Raw-SFEM 或 Stat-SFEM）提取每个短期序列的特征
3. 用高温自注意力机制（HT-SelfAttention）聚合短期特征，过滤无关包噪声
4. 选择有用的模态，通过表征增强和平均池化融合多模态表征
5. 全连接层输出分类结果，用交叉熵损失训练

## 9. Obsidian 知识链接

### 9.1 相关概念

- Anonymous Traffic Classification - 匿名流量分类
- Encrypted Traffic Classification - 加密流量分类
- Tor Network Traffic Analysis - Tor 网络流量分析
- VPN Traffic Classification - VPN 流量分类
- Noise-Robust Learning - 噪声鲁棒学习
- Multi-Modal Fusion - 多模态融合
- Short-Term Representation - 短期表征

### 9.2 相关方法

- Self-Attention Mechanism - 自注意力机制
- High Temperature Self-Attention - 高温自注意力
- Bidirectional GRU - 双向 GRU
- Representation Enhancement - 表征增强
- Mutual Information for Feature Selection - 基于互信息的特征选择
- Transformer Architecture - Transformer 架构

### 9.3 相关任务

- Anonymous Network Traffic Identification - 匿名网络流量识别
- Tor Traffic Classification - Tor 流量分类
- VPN Traffic Classification - VPN 流量分类
- Robust Traffic Classification under Noise - 噪声下的鲁棒流量分类
- Short Flow Classification - 短流分类

### 9.4 可更新的综述页面

- [[survey-encrypted-traffic-analysis]]
- Anonymous Traffic Classification Methods
- Noise-Robust Traffic Analysis

### 9.5 可加入的对比表

- Anonymous Traffic Classification Methods Comparison
- Encrypted Traffic Classification Methods
- Deep Learning for Traffic Classification

## 10. 证据记录（表格形式）

### 10.1 核心实验结果

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E1 | 主要结果 | AN-Net 在 SJTU-AN21 上 AC=94.76%, F1=94.39%，比 ET-Bert (AC=86.61%, F1=88.15%) 分别提升 8.15% 和 6.24% | Table 1 |
| E2 | 主要结果 | AN-Net 在 ISCX-Tor 上 AC=99.51%, F1=99.50%，比 AttnLSTM (AC=97.25%, F1=97.08%) 分别提升 2.26% 和 2.42% | Table 1 |
| E3 | 主要结果 | AN-Net 在 ISCX-VPN 上 AC=99.96%, F1=99.96%，比 ET-Bert (AC=98.85%, F1=98.88%) 分别提升 1.11% 和 1.08% | Table 1 |
| E4 | 额外数据集 | AN-Net 在 USTC-TFC 上 F1=99.80%（ET-Bert 98.32%），在 Cross-Platform 上 F1=99.67%（ET-Bert 99.37%） | Table 7 |

### 10.2 噪声鲁棒性证据

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E5 | 鲁棒性 | 75% 噪声下 AN-Net 在 SJTU-AN21 的 F1 仅下降 2.39%（0.9439→0.9200），ET-Bert 下降超 64.6%（0.8815→~0.15） | Figure 4 |
| E6 | 鲁棒性 | 75% 噪声下 AN-Net 在 ISCX-VPN 的 F1 仅下降 0.32%（0.9996→0.9933），AttnLSTM 下降超 69.6% | Figure 4 |
| E7 | 鲁棒性 | 75% 噪声下 AN-Net 在 ISCX-Tor 的 F1 下降 8.8%（0.9950→0.9071），但仍高于所有其他方法 | Figure 4 |

### 10.3 消融实验证据

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E8 | 消融-短期vs长期 | 长期特征在 75% 噪声下 F1=72.95%，短期特征+HT 为 92.00%（差距 19.05%） | Table 2 |
| E9 | 消融-HT效果 | HT-SelfAttention 的提升随噪声增加：0% 噪声提升 0.87%，75% 噪声提升 1.32% | Table 2 |
| E10 | 消融-多模态 | 仅 packet size 单模态 F1=80.14%，四模态融合后 F1=94.39%（提升 14.25%） | Table 3 |
| E11 | 消融-表征增强 | 表征增强在 75% 噪声下提升 0.99%（SJTU-AN21）和 1.37%（ISCX-Tor），在 50% 噪声下提升 0.45% 和 0.43% | Table 4 |
| E12 | 消融-Payload | 加入 payload 模态在 SJTU-AN21 上反而降低 F1 0.48%（0.9439→0.9391），因为 raw payload 在跨域场景过拟合 | Table 5 |

### 10.4 稳定性与效率证据

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E13 | 稳定性 | Stat-SFEM 比 Raw-SFEM 在 SJTU-AN21 上 AC 高 4.21%（0.9476 vs 0.9055），F1 高 3.41%（0.9439 vs 0.9098） | Table 5 |
| E14 | 训练效率 | 仅用 10% 训练数据时 AN-Net F1=89.30%，ET-Bert 仅 56.63%（差距 32.67%）；50% 数据时 AN-Net 92.07% vs ET-Bert 83.05% | Table 10 |
| E15 | 短流分类 | 流长度截断为 10 包时 AN-Net F1=90.02%（下降 4.37%），FS-Net 57.06%（下降 22.43%），ET-Bert 85.44%（下降 2.71%） | Table 9 |
| E16 | 计算复杂度 | AN-Net: 2.40M 参数, 1477 MiB 内存, 39.41 μs/pkt 推理, 18.41 min 训练；ET-Bert: 132.13M 参数, 17379 MiB, 169.34 μs/pkt, 49.51 min | Table 8 |

### 10.5 理论分析证据

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E17 | 理论证明 | 高温自注意力使无关流权重 w_k' ≤ w_k（通过分解 S=||S||·Ŝ 并分析温度效应证明） | Appendix A, Eq.14-18 |
| E18 | 理论证明 | 当模型从某模态获得足够信息时（q_k→1），梯度 ∂L/∂z_i → 0，导致模型忽略从含噪声模态学习（Eq.24-27） | Appendix B |
| E19 | 对比实验 | RE 融合使 Packet Size 模态（50% 噪声）准确率达 67.79%，而 Add 融合仅 35.11%，Concatenation 仅 21.48% | Table 6 |
| E20 | 注意力可视化 | HT-SelfAttention 对无关流短期特征赋予极小权重（0.00 或 0.05），对目标流特征赋予较大权重（0.10-0.28），形成块状对角结构 | Figure 7 |

### 10.6 模态互信息证据

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E21 | 模态选择 | SJTU-AN21: Packet Size MI=0.81, IAT MI=0.81, TTL MI=1.50, IPFlag MI=0.01(去除), TCPFlag MI=0.99 | Table 11 |
| E22 | 模态选择 | ISCX-Tor: TTL MI=0.00(去除)；ISCX-VPN: IPFlag MI=0.23(去除), TCPFlag MI=0.42(去除) | Table 11 |

## 11. 原始资料链接

- 论文发表于 ACM Web Conference 2024 (WWW '24), May 13-17, 2024, Singapore
- 作者单位：School of Electronic Information and Electrical Engineering, Shanghai Jiao Tong University
- 开源代码和数据集：https://github.com/SJTU-dxw/AN-Net
- 项目资助：SJTU-QI'ANXIN Joint Lab of Information System Security
- DOI: https://doi.org/10.1145/3589334.3645691

## 12. 后续问题

1. **更复杂的对抗场景**：如果攻击者不是随机注入噪声，而是故意模仿目标流的统计特征，AN-Net 是否仍然有效？
2. **动态短期序列长度**：如何自适应地确定最优的短期序列长度，而不是固定值？
3. **更多模态的探索**：除了 packet size, IAT, TTL, IPFlag, TCPFlag 和 payload，是否有其他有意义的模态可以利用？
4. **在线学习与适应**：网络环境持续变化，AN-Net 能否通过在线学习持续适应新的网络条件？
5. **与其他匿名网络的兼容性**：除 Tor 外，在 I2P、Freenet 等其他匿名网络上的表现如何？
6. **高温自注意力的理论边界**：在什么条件下高温自注意力会失效？是否存在最优的温度选择理论？
7. **Stat-SFEM 与 Raw-SFEM 的自动选择**：能否设计一个机制自动判断应该使用哪种 SFEM，而不是依赖人工经验？
8. **隐私影响**：该技术用于匿名流量分类可能对用户隐私产生影响，如何在安全需求和隐私保护之间取得平衡？

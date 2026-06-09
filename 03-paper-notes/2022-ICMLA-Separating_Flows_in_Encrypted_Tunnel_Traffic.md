---
type: paper
title_original: "Separating Flows in Encrypted Tunnel Traffic"
title_cn: "加密隧道流量中的流分离"
authors:
  - Alexander Hartl
  - Joachim Fabini
  - Tanja Zseby
year: 2022
venue: "ICMLA"
doi: ""
url: ""
pdf: "00-inbox/PDFs/2022-ICMLA-Separating_Flows_in_Encrypted_Tunnel_Traffic.pdf"
mineru_md: "02-parsed-markdown/2022-ICMLA-Separating_Flows_in_Encrypted_Tunnel_Traffic.md"
status: processed
reading_level: L2
dataset:
  - synthetic-flows
  - real-network-traces
code: "https://gitlab.tuwien.ac.at/e389-cnpub/separatingflows/"
relevance: high
research_area: ["加密流量分析", "流分离", "流量去匿名化"]
task: ["流分离", "数据包归属"]
method: ["LSTM", "random projection", "Viterbi search"]
created: "2026-05-27"
updated: "2026-05-29"
---

# Separating Flows in Encrypted Tunnel Traffic

## 0. 基础信息

| 字段 | 内容 |
|------|------|
| 论文全称 | Separating Flows in Encrypted Tunnel Traffic |
| 作者 | Alexander Hartl, Joachim Fabini, Tanja Zseby |
| 机构 | Institute of Telecommunications, TU Wien |
| 发表年份 | 2022 |
| 会议/期刊 | ICMLA (International Conference on Machine Learning and Applications) |
| 关键词 | Tunnel Encryption, Encrypted Traffic Analysis, Deanonymization, Deep Learning, Anomaly Detection, Flow Separation |
| 代码 | https://gitlab.tuwien.ac.at/e389-cnpub/separatingflows/ |

## 1. 一句话总结

提出一种基于深度 LSTM 神经网络的 packet-level anomaly detection 方法，结合类似 Viterbi 的搜索算法，能够在仅观察到加密 tunnel 中多个 flow 交织后的 packet sequence 的情况下，将各 packet 准确归属到其原始 flow，在合成数据和真实网络 trace 上均取得高精度分离效果。

## 2. 摘要翻译

在许多场景中，如无线 Internet 接入或加密 VPN tunnel，加密是逐 packet 进行的。虽然这种加密方式有效保护了传输 payload 的机密性，但它使得涉及 inter-arrival time 和 packet length 的 traffic pattern 对窃听者（如在 air interface 上的监听者）仍然可见。一种广泛存在的信念是，仅通过观察不同并行 flow 的交织 packet，分析和分类相应的 traffic 是非常困难或近乎不可能的。

本文表明，仅从交织 packet sequence 中观察到的 pattern，确实可以将属于不同 flow 的 packet 分离出来。我们设计了一种新颖的深度 recurrent neural network 架构，能够检测 flow 中的个别 anomalous packet。基于该 anomaly detector，我们开发了一种算法来寻找使 anomaly score 最小化的 flow 分离方案。合成 craft 的 flow 和真实网络 trace 上的实验结果表明，我们的方法确实能够以高精度成功分离 flow。

通过从多个交织 flow 中恢复单个 flow 的 packet sequence，本文证明了常见的 packet-level encryption 在需要高级别隐私的场景中可能是不充分的。在防御者方面，我们的方法构成了加密 traffic 分析的有价值工具，同时也为 network intrusion detection 领域贡献了一种新颖的 neural network 架构。

## 3. 方法动机（Motivation）

### 问题背景

- Tunnel encryption（如 VPN、802.11 无线加密）将来自不同应用的 packet 交织加密后在共享链路上传输
- 虽然 payload 被加密，但 packet 长度、inter-arrival time (IAT)、direction 等 traffic pattern 仍然可观测
- 已有研究表明单个 flow 的加密 traffic 可被分类，但前提是 flow 已被预先分离
- 现实场景中多个 flow 的 packet 交织到达，无法直接应用传统的 per-flow 分类方法

### 现有方法的不足

- **已有的加密流量分类研究**：均假设 flow separation 已事先完成，无法处理 tunnel encryption 场景
- **VPN deanonymization 研究**（Appelbaum 等、Bui 等）：关注泄露信息和客户端配置漏洞，而非直接分析加密 traffic pattern
- **Tor deanonymization 攻击**：通常依赖 exit node 关联或 side channel，与本文场景不同
- **Meghdouri 等人 [16]**：仅能估计加密 tunnel 中的 flow 数量，无法执行实际的 flow separation

### 核心动机

证明 tunnel encryption 的隐私保护能力不如普遍认为的那样强——即使 payload 被加密，通过分析 interleaved packet sequence 中的 traffic pattern（packet length、IAT、direction），仍可将 packet 归属到各自的原始 flow，从而为后续的 traffic classification 和 deanonymization 攻击铺平道路。

## 4. 方法设计（Methodology）

### 4.1 整体框架

方法分为两步：
1. **Packet-based Anomaly Detection**：构建一个深度 neural network，评估 flow 中每个 packet 的异常程度（anomaly score），能够检测出 flow 中被混入的来自其他 flow 的 packet
2. **Flow Separation via Search**：基于 anomaly detector，使用类似 Viterbi 的搜索算法寻找使总 anomaly score 最小的 packet-to-flow 分配方案

### 4.2 Anomaly Detector 设计

**基础思想**：基于 Loda（Lightweight On-line Detector of Anomalies）方法，使用 k 个 Random Projection (RP) 构建 histogram 来建模正常数据分布。Loda 的 anomaly score 为：

$$s(\boldsymbol{x}) = - \frac{1}{k} \sum_{i=1}^{k} \ln p_i(\boldsymbol{x}^T \boldsymbol{w}_i)$$

**关键创新**：不能直接使用 Loda 的静态 histogram，因为需要考虑 packet 在 flow 中的位置和上下文。因此用深度 neural network 替代静态 histogram，动态预测下一个 packet 的特征概率分布。

**网络架构**（如论文 Figure 2 所示）：
- 交替部署 4 层 fully connected Leaky ReLU (LReLU) 层和 3 层 LSTM 层
- 每个 RP 维度连接一个 softmax 层（共 50 个 bin）
- 输入：packet 特征的 z-score normalized 向量
- 输出：每个 RP 维度上 50 bin 的概率分布（即 learned histogram）
- 训练损失：categorical cross entropy
- 优化器：Adam，训练至 validation loss 最小值

### 4.3 Packet 特征

每个 packet i 的特征向量为 4 维：

$$\boldsymbol{x}^{(i)} = \left(\mathrm{PD}, \ln \frac{\text{Pkt. length}}{1 \text{Byte}}, \ln \frac{\mathrm{IAT} + 1\mu\mathrm{s}}{1\mathrm{ms}}, \ln \frac{\mathrm{DIAT} + 1\mu\mathrm{s}}{1\mathrm{ms}}\right)^T$$

- **PD (Packet Direction)**：接收为 0，发送为 1
- **Pkt. Length**：packet 长度，取对数
- **IAT (Inter-Arrival Time)**：当前 packet 与该 flow 中前一个 packet 的时间差（不论方向），取对数
- **DIAT (Directional IAT)**：当前 packet 与该 flow 中前一个同方向 packet 的时间差，取对数

IAT 和 DIAT 取对数是为了将宽范围的时间值映射到可管理的范围，并将相对差异转换为绝对差异。

### 4.4 序列依赖建模

Anomaly detector 捕获序列依赖的三种机制：
1. **直接预测**：NN 预测下一个 packet 的特征概率分布，异常 packet 获得低概率
2. **RNN 隐状态**：LSTM 的 recurrent 特性使错误的 packet 序列会导致 NN 预测质量下降（类似 autoencoder 原理）
3. **多 packet 预测**：可选预测下一个或下两个 packet 的特征，联合概率越高表明序列越正确

### 4.5 Flow Separation 算法

**问题形式化**：
- 定义 Association Vector (AV) $\boldsymbol{a} \in \{1, \ldots, F\}^n$，表示每个 packet 属于哪个 flow
- 目标：找到最大似然估计

$$\hat{\boldsymbol{a}} = \arg \max_{\boldsymbol{a}} \sum_{i=1}^{n} \ln P(\boldsymbol{x}^{(i)} \mid \boldsymbol{x}^{(1)}, \dots, \boldsymbol{x}^{(i-1)}, \boldsymbol{a})$$

**搜索策略**：穷举搜索复杂度为 $O(F^n)$，不可行。采用类似 Viterbi 的 beam search：
- 处理每个 packet 后，保留最佳 R 个 AV 候选（如 R=1000）
- 对每个候选，尝试分配到 F 个 flow 中的每一个，评估 anomaly score
- 截断至 top-R 个候选继续迭代
- 最终输出得分最高的 AV

**复杂度**：
- 时间复杂度：$O(RnF)$，内层循环可并行执行，利用 GPU batch 计算
- 空间复杂度：$O(RF) + O(Rn)$

### 4.6 前提条件

方法要求：
1. 已知交织 flow 数量的上界 F（可由 [16] 的方法估计）
2. 加密 traffic 中单个 packet 可区分
3. 可从加密 traffic 推断 packet 长度
4. 可从加密 traffic 推断 packet IAT

这些条件在 IPsec VPN、WireGuard、802.11 无线加密等常见场景中均满足，因为协议设计者通常追求低延迟（逐 packet 加密）和低带宽开销（不做大量 random padding）。

## 5. 方法对比（Comparison Methods）

本文不与传统分类方法对比，而是评估自身不同变体的性能：

| 变体 | 描述 |
|------|------|
| 完整方法 | 使用 IAT + DIAT + PD + Pkt.Length，基于下 2 个 packet 的 RP |
| IAT omitted | 去除 IAT 特征，仅用 DIAT + PD + Pkt.Length |
| No 2-packet proj. | RP 仅基于下一个 packet（而非下两个） |
| With reverse model | 训练反向 flow 模型，正向/反向/正向三轮迭代，利用后验概率作为先验 |

与相关工作的定位差异：
- **vs. 加密流量分类方法 [7-11]**：这些方法假设 flow 已分离，本文解决分离问题
- **vs. VPN/Tor deanonymization [12-15]**：这些方法依赖 side channel 或 attacker-controlled nodes，本文直接分析 traffic pattern
- **vs. Meghdouri 等 [16]**：仅能估计 flow 数量，本文实现实际分离

## 6. 实验表现（Experiments）

### 6.1 数据集

**合成数据**（pyvirtnet 模拟网络，20ms 单向延迟，2ms 标准差）：
- Steady UDP stream：恒定 50ms 间隔，60B/100B/150B/200B 固定 packet size
- Bursty UDP stream：每 15 个 packet 插入 1.5-2.5s 随机间隔
- TCP request-response：2500B 请求、10KiB 响应，3-30s 随机间隔

**真实数据**：
- CIC-IDS-2017 [25]：仅选取 benign traffic
- UNSW-NB15 [26]：仅选取 benign traffic
- MAWI traffic archive [27]：2021 年 6-7 月日本 backbone trace，选取 Zoom (UDP 8801)、Microsoft Teams (UDP 3480)、Cisco Webex (UDP 9000) 视频会议流量
- 充电基础设施 trace：基于 HTTP 的 OCPP 协议，machine-to-machine 通信

### 6.2 评估指标

- **Accuracy**：忽略 flow 排列置换后，正确分配的 packet 比例
- **TrAccuracy (Transition Accuracy)**：下一个同 flow packet 被正确预测的比例，对 flow 交换不敏感但对单 packet 错误更敏感
- **ARI (Adjusted Rand Index)**：聚类评估指标，对随机标签校正后接近 0，对不等长 flow 更公平

### 6.3 合成数据结果（Figure 3，500 次平均）

| 交织 flow 数 | Acc. (omit IAT) | Acc. (no 2-pkt) | Acc. (reverse) | TrAcc. (omit IAT) | ARI (omit IAT) |
|-------------|-----------------|-----------------|----------------|-------------------|----------------|
| 2 | 0.98 | 0.97 | 0.96 | ~0.98 | ~0.93 |
| 3 | 0.97 | 0.95 | 0.94 | ~0.97 | ~0.90 |
| 4 | 0.96 | 0.93 | 0.91 | ~0.96 | ~0.87 |
| 5 | 0.95 | 0.91 | 0.89 | ~0.95 | ~0.85 |

关键发现：
- 所有变体性能差异不大，说明各变体均能充分学习数据 pattern
- TrAccuracy 显著高于 Accuracy，暗示 flow 中间交换是主要错误模式
- 随交织 flow 数增加性能下降，但幅度可控

### 6.4 Ground Truth Rank 分析（Figure 4）

- 跟踪 ground truth solution 在候选集中的排名分布
- 2 个 flow：95 分位数约 10^1，中位数约 10^0
- 5 个 flow：95 分位数约 10^4，中位数约 10^2
- R 需要随 flow 数指数增长以保持 ground truth 不被截断

### 6.5 Steady Flow 深入分析（Figures 5-6）

- 不同 packet size 的 flow：所有情况均达 100% 准确率
- 相同 packet size 的 flow：准确率取决于两 flow 的时间偏移
  - 时间偏移足够大时（远大于 IAT jitter 的标准差）：高准确率
  - 时间偏移接近 0 时：准确率降至约 0.4-0.8（理论极限，相同大小 packet 同时到达无法区分）

### 6.6 真实数据结果（Table I）

| 数据集 | 交织 flow 数 | Acc. (pkt avg) | TrAcc. (pkt avg) | ARI (pkt avg) |
|--------|-------------|----------------|------------------|---------------|
| MAWI | 2 | 0.983 | 0.977 | 0.945 |
| MAWI | 5 | 0.932 | 0.926 | 0.884 |
| CIC-IDS-2017 | 2 | 0.996 | 0.996 | 0.987 |
| CIC-IDS-2017 | 5 | 0.981 | 0.984 | 0.963 |
| UNSW-NB15 | 2 | 0.998 | 0.998 | 0.993 |
| UNSW-NB15 | 5 | 0.991 | 0.989 | 0.979 |

- 真实数据性能与合成数据相当甚至略优
- 真实数据中 TrAccuracy 略低于 Accuracy（与合成数据相反），可能因为短 flow 更多，单 packet 错误更突出
- MAWI 数据性能略低于 CIC-IDS 和 UNSW-NB15，反映了 backbone 流量的更高多样性

## 7. 防御策略（Defenses）

论文提出以下防御建议：
- **避免泄露 packet 来源/接收者信息**：当前 802.11 网络的地址机制与此目标矛盾
- **Packet aggregation 和 fragmentation**：在无法推断原始 packet 长度的条件下可阻止 flow separation
- **IP-TFS**：IPsec 的扩展方案，支持 fragmentation 和 aggregation，以带宽为代价掩盖 traffic pattern
- **一般原则**：若资源允许，应默认采用上述防御策略以增强协议安全性和隐私性
- 随着交织 flow 数增加，计算需求急剧上升且准确率下降，因此多用户 VPN（site-to-site）比单用户多应用 VPN 更难分析

## 8. 总结

本文首次研究了从加密 tunnel traffic 中分离 interleaved flow 的问题。核心贡献包括：
1. 形式化定义了加密 tunnel traffic 的 flow separation 问题并设计了评估指标
2. 设计了基于 LSTM + Random Projection 的 packet-level anomaly detector，能动态建模 flow 中 packet 特征的序列依赖
3. 提出了类似 Viterbi 的 beam search 算法，在多项式时间内近似求解最优 flow 分配
4. 在合成数据和多种真实网络 trace 上验证了方法的有效性

研究揭示了 tunnel encryption 的隐私保护能力被高估——仅凭 traffic pattern 即可恢复 flow 结构，为后续的 traffic classification 和 deanonymization 攻击打开通道。同时该方法也可作为防御者在加密 tunnel 中进行 intrusion detection 的工具。

## 9. 知识链接

### 相关论文

- **Meghdouri 等 [16]**：同一团队的前期工作，使用 deep NN 估计加密 VPN tunnel 中的 flow 数量，本文是其自然延伸——从"估计数量"到"实际分离"
- **Loda [19]**：本文 anomaly detector 的基础方法，使用 Random Projection 构建 ensemble 进行在线异常检测，本文用 NN 替代其静态 histogram
- **Viterbi 算法 [21]**：本文 flow separation 搜索算法的灵感来源，核心差异是本文使用连续状态空间
- **IP-TFS [30]**：IPsec 扩展，本文讨论的防御方案之一

### 概念关联

- **Anomaly Detection in Data Streams**：Loda 是在线流式异常检测的经典方法，本文将其思想与深度学习结合
- **Beam Search**：NLP 中广泛使用的近似搜索策略，本文将其应用于 packet-to-flow 分配问题
- **Traffic Fingerprinting**：本文的方法可视为 flow-level traffic fingerprinting 的逆过程——从混合 trace 中恢复单个 fingerprint

## 10. 证据记录

### 关键数据点

- 合成数据 2 个 flow：Accuracy ~0.98, TrAccuracy ~0.98, ARI ~0.93
- 合成数据 5 个 flow：Accuracy ~0.95, TrAccuracy ~0.95, ARI ~0.85
- UNSW-NB15 2 个 flow：Accuracy 0.998, ARI 0.993
- UNSW-NB15 5 个 flow：Accuracy 0.991, ARI 0.979
- 不同 packet size 的 steady flow：100% 分离准确率
- 同 packet size flow：准确率取决于 flow 间时间偏移相对于 IAT jitter 的大小
- R 的选取：2 个 flow 时 R 约 10^1-10^2 足够；5 个 flow 时需要 R 约 10^3-10^4

### 值得注意的细节

- 各方法变体（含/不含 IAT、单/双 packet prediction、正向/反向模型）之间性能差异很小，说明方法鲁棒性好
- 真实数据中 TrAccuracy < Accuracy，而合成数据中 TrAccuracy > Accuracy，论文解释为真实数据短 flow 更多
- 论文明确指出：当两个同类型同大小 flow 的 packet 恰好同时到达时，理论上无法区分，这是方法的固有限制
- 每个 flow 约 100 个 packet 的合成数据设计避免了评估指标对 flow 长度的偏差

## 11. 原始资料链接

- 论文来源：ICMLA 2022
- 代码仓库：https://gitlab.tuwien.ac.at/e389-cnpub/separatingflows/
- 原始 Markdown 文件：`02-parsed-markdown/2022-ICMLA-Separating_Flows_in_Encrypted_Tunnel_Traffic.md`

## 12. 后续问题

1. 方法的计算复杂度随 flow 数指数增长，是否可以设计更高效的搜索策略（如基于 reinforcement learning 的策略）来降低计算开销？
2. 当 flow 类型相同（如两个相同的 video streaming flow）时，分离的理论极限是什么？是否有信息论层面的分析？
3. 该方法是否可以扩展到更深层嵌套的 encryption stacking 场景（如 VPN over Tor）？
4. 论文仅使用了 PD、packet length、IAT、DIAT 四个特征，加入更多统计特征（如 flow 滑动窗口统计量）是否能提升性能？
5. 在实际部署中，如何处理 flow 数量未知或动态变化的情况（如用户中途打开/关闭应用）？
6. 防御方使用 IP-TFS 等方案后，本方法的攻击效果如何？需要多少额外的 padding/fragmentation 才能有效阻止 flow separation？
7. 该 anomaly detector 的 NN 模型是否可以替换为 Transformer 架构以更好地捕获长距离依赖？

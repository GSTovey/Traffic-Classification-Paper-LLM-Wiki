---
type: paper
title_original: "Detecting Unknown Encrypted Malicious Traffic in Real Time via Flow Interaction Graph Analysis"
title_cn: "通过流交互图分析实时检测未知加密恶意流量"
authors: [Chuanpu Fu, Qi Li, Ke Xu]
year: 2023
venue: "NDSS"
doi: "unknown"
url: "unknown"
pdf: "00-inbox/PDFs/2023-NDSS-Detecting_unknown_encrypted_malicious_traffic_in_real_time_via_flow_interaction_graph_analysis.pdf"
mineru_md: "02-parsed-markdown/2023-NDSS-Detecting_unknown_encrypted_malicious_traffic_in_real_time_via_flow_interaction_graph_analysis.md"
status: processed
reading_level: L2
research_area: [malicious-traffic-detection, encrypted-traffic-analysis]
task: [encrypted-malicious-traffic-detection, unknown-attack-detection]
method: [flow-interaction-graph, unsupervised-learning, graph-analysis]
dataset: [92-datasets, 48-encrypted-attacks]
code: "unknown"
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

## §0 基础信息

| 项目 | 内容 |
|------|------|
| 论文全称 | Detecting Unknown Encrypted Malicious Traffic in Real Time via Flow Interaction Graph Analysis |
| 作者 | Chuanpu Fu, Qi Li, Ke Xu |
| 机构 | 清华大学, 中关村实验室 |
| 发表时间 | 2023 |
| 会议 | NDSS Symposium 2023 |

## §1 一句话总结

提出HyperVision系统，通过构建流交互图捕获多流交互模式，利用无监督图学习方法实时检测未知加密恶意流量，在92个数据集上实现至少0.92 AUC和0.86 F1，检测吞吐量超过80.6 Gb/s，平均延迟0.83秒。

## §2 摘要翻译

**原始摘要：**
Nowadays traffic on the Internet has been widely encrypted to protect its confidentiality and privacy. However, traffic encryption is always abused by attackers to conceal their malicious behaviors. Since the encrypted malicious traffic has similar features to benign flows, it can easily evade traditional detection methods. Particularly, the existing encrypted malicious traffic detection methods are supervised and they rely on the prior knowledge of known attacks (e.g., labeled datasets). Detecting unknown encrypted malicious traffic in real time, which does not require prior domain knowledge, is still an open problem. In this paper, we propose HyperVision, a realtime unsupervised machine learning (ML) based malicious traffic detection system. Particularly, HyperVision is able to detect unknown patterns of encrypted malicious traffic by utilizing a compact in-memory graph built upon the traffic patterns. The graph captures flow interaction patterns represented by the graph structural features, instead of the features of specific known attacks. We develop an unsupervised graph learning method to detect abnormal interaction patterns by analyzing the connectivity, sparsity, and statistical features of the graph, which allows HyperVision to detect various encrypted attack traffic without requiring any labeled datasets of known attacks. Moreover, we establish an information theory model to demonstrate that the information preserved by the graph approaches the ideal theoretical bound. We show the performance of HyperVision by real-world experiments with 92 datasets including 48 attacks with encrypted malicious traffic. The experimental results illustrate that HyperVision achieves at least 0.92 AUC and 0.86 F1, which significantly outperform the state-of-the-art methods. In particular, more than 50% attacks in our experiments can evade all these methods. Moreover, HyperVision achieves at least 80.6 Gb/s detection throughput with the average detection latency of 0.83s.

**中文翻译：**
如今互联网上的流量已被广泛加密以保护其机密性和隐私。然而，流量加密总是被攻击者滥用以隐藏其恶意行为。由于加密恶意流量与正常流量具有相似特征，它很容易逃避传统检测方法。特别是，现有的加密恶意流量检测方法是有监督的，依赖于已知攻击的先验知识（如标记数据集）。实时检测未知加密恶意流量（不需要先验领域知识）仍然是一个开放问题。本文提出HyperVision，一种基于无监督机器学习的实时恶意流量检测系统。特别是，HyperVision能够通过利用基于流量模式构建的紧凑内存图来检测未知模式的加密恶意流量。该图捕获由图结构特征表示的流交互模式，而不是特定已知攻击的特征。作者开发了一种无监督图学习方法，通过分析图的连通性、稀疏性和统计特征来检测异常交互模式，使HyperVision能够在不需要任何已知攻击标记数据集的情况下检测各种加密攻击流量。此外，作者建立了信息论模型来证明图保留的信息接近理想理论边界。通过92个数据集（包括48个加密恶意流量攻击）的真实实验表明，HyperVision至少达到0.92 AUC和0.86 F1，显著优于现有方法。特别是，实验中超过50%的攻击可以逃避所有基线方法。此外，HyperVision至少达到80.6 Gb/s的检测吞吐量，平均检测延迟为0.83秒。

## §3 方法动机

**痛点问题：**
- 加密恶意流量与正常流量特征相似，可逃避现有检测方法
- 现有方法是有监督的，依赖已知攻击的先验知识
- 无法检测未知模式的加密恶意流量（零日攻击）
- 单流特征不足以捕获隐蔽的恶意行为

**核心直觉：**
- 恶意攻击涉及多个攻击步骤，产生独特的流交互模式
- 例如：垃圾邮件机器人与SMTP服务器的交互模式与合法通信显著不同
- 流交互图可以捕获多流之间的交互关系

**方法动机：**
- 需要无监督方法检测未知加密恶意流量
- 流交互图可以保留接近最优的流量信息
- 图结构特征可以捕获异常交互模式

## §4 方法设计

**整体流程：**

```
输入: 实时网络流量
  ↓
Step 1: 图构建 (Graph Construction)
  - 流分类: 短流 vs 长流
  - 短流聚合: 基于相似性聚合大量短流，降低图密度
  - 长流分布拟合: 对长流的包特征进行分布拟合
  - 顶点: 不同IP地址
  - 边: 流交互模式
  ↓
Step 2: 图预处理 (Graph Pre-Processing)
  - 提取连通分量
  - 聚类高-level统计特征
  - 过滤良性分量，减少处理开销
  - 边预聚类: 根据局部邻接特征预聚类
  ↓
Step 3: 异常交互检测 (Abnormal Interaction Detection)
  - 关键顶点检测: 求解顶点覆盖问题
  - 交互模式聚类: 对每个关键顶点的连接边聚类
  - 异常边识别: 通过聚类损失函数识别异常边
  ↓
输出: 加密恶意流量检测结果
```

**关键公式：**
- 流交互熵模型: 分析现有数据源保留的信息量
- 信息论边界: 证明图保留的信息接近理论上限
- 聚类损失函数: 识别异常交互模式

**优势：**
- 无监督检测，无需标记数据集
- 实时检测，吞吐量超过80.6 Gb/s
- 通用检测，可处理加密和非加密流量
- 信息保留接近理论最优

**局限：**
- 需要足够的流交互数据
- 对图构建参数敏感
- 论文未明确说明在极端高流量场景下的性能

## §5 与其他方法对比

**创新点：**
1. 首个基于流交互图的实时无监督加密恶意流量检测系统
2. 开发短流聚合和长流分布拟合的图构建方法
3. 设计轻量级无监督图学习方法
4. 建立信息论模型证明图的信息保留能力

**与基线对比：**
- 对比方法:
  - 基于TLS扩展的方法
  - 基于HTTPS头部的方法
  - 基于时间序列的方法
  - 基于TLS握手的方法
  - 基于流统计的方法
- 改进点:
  - 准确率: 提升13.9%~36.1%
  - 通用性: 可检测加密和非加密流量
  - 实时性: 吞吐量超过80.6 Gb/s
  - 无监督: 不需要标记数据集

## §6 实验表现

**数据集：**
- 92个攻击数据集
- 48种加密恶意流量攻击
- 包括: 加密洪泛流量、Web攻击、恶意软件活动
- 背景流量: 骨干网流量重放

**评估指标：**
- AUC (Area Under Curve)
- F1分数
- 检测吞吐量 (Gb/s)
- 检测延迟 (秒)

**主要结果：**
- AUC: 至少0.92
- F1: 至少0.86
- 检测吞吐量: 至少80.6 Gb/s
- 平均检测延迟: 0.83秒
- 准确率提升: 13.9%~36.1%（相比5种最先进方法）

**关键发现：**
- 超过50%的攻击可逃避所有基线方法
- HyperVision可检测所有加密恶意流量
- 可检测高级侧信道攻击（CVE-2020-36516）
- 可检测新发现的加密货币挖矿攻击

## §7 学习与应用

**开源情况：**
- 论文提到有原型系统，但未明确说明是否开源代码

**复现要点：**
- 需要Intel DPDK进行数据包处理
- 需要构建流交互图
- 需要实现无监督图学习方法
- 需要调整图构建和聚类参数

**迁移价值：**
- 方法可应用于各种网络环境的恶意流量检测
- 流交互图思路可扩展到其他网络安全任务
- 无监督方法可适应新的攻击模式

## §8 总结

**核心思想：** 通过构建流交互图捕获多流交互模式，利用无监督图学习方法实时检测未知加密恶意流量。

**快速流程：**
```
实时流量 → 流分类(短流/长流) → 图构建
    ↓
图预处理(连通分量/聚类) → 关键顶点检测
    ↓
交互模式聚类 → 异常边识别 → 恶意流量检测
```

## §9 知识链接

- [[malicious-traffic-detection]] - 恶意流量检测技术
- [[encrypted-traffic-analysis]] - 加密流量分析方法
- [[graph-neural-network]] - 图神经网络方法
- [[unsupervised-learning]] - 无监督学习
- [[flow-interaction-analysis]] - 流交互分析
- [[real-time-detection]] - 实时检测技术
- [[anomaly-detection]] - 异常检测方法
- [[zero-day-attack]] - 零日攻击检测

## §10 证据记录

| 声明 | 证据 | 证据强度 |
|------|------|----------|
| 超过50%攻击可逃避所有基线方法 | 92数据集实验结果 | 强（大规模实验） |
| AUC至少0.92 | 实验结果 | 强（实验数据） |
| 检测吞吐量至少80.6 Gb/s | DPDK原型性能测试 | 强（性能测试） |
| 图保留的信息接近理论边界 | 信息论模型证明 | 强（理论分析） |
| 流交互模式可区分恶意和正常流量 | 多种攻击类型验证 | 强（实验验证） |

## §11 原始资料链接

- PDF: `00-inbox/PDFs/2023-NDSS-Detecting_unknown_encrypted_malicious_traffic_in_real_time_via_flow_interaction_graph_analysis.pdf`
- MinerU MD: `02-parsed-markdown/2023-NDSS-Detecting_unknown_encrypted_malicious_traffic_in_real_time_via_flow_interaction_graph_analysis.md`

## §12 后续问题

1. 图构建参数如何自动优化？
2. 对于极端高流量场景（如骨干网），方法的可扩展性如何？
3. 是否可以结合半监督学习进一步提升检测准确率？
4. 对于对抗性攻击（攻击者故意模仿正常交互模式）的效果如何？
5. 如何处理分布式攻击（多源攻击者）的场景？

---
type: paper
title_original: "Flow Interaction Graph Analysis: Unknown Encrypted Malicious Traffic Detection"
title_cn: "流交互图分析：未知加密恶意流量检测"
authors:
  - Chuanpu Fu
  - Qi Li
  - Ke Xu
year: 2024
venue: "TNET"
doi: "10.1109/TNET.2024.3370851"
url: ""
pdf: "00-inbox/PDFs/2024-TNET-Flow_Interaction_Graph_Analysis_Unknown_Encrypted_Malicious_Traffic_Detection.pdf"
mineru_md: "02-parsed-markdown/2024-TNET-Flow_Interaction_Graph_Analysis_Unknown_Encrypted_Malicious_Traffic_Detection.md"
status: processed
reading_level: L2
research_area:
  - malicious-traffic-detection
  - encrypted-traffic-analysis
  - graph-learning
task:
  - malicious-traffic-detection
  - unknown-attack-detection
  - realtime-detection
method:
  - graph-learning
  - unsupervised-learning
  - flow-interaction-graph
  - vertex-cover
  - clustering
  - information-theory
dataset:
  - 92-attack-datasets
  - VPC-1500-instances
  - 48-encrypted-attacks
code: ""
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

# HyperVision: 基于流交互图分析的未知加密恶意流量检测

## 0. 基础信息

| 字段 | 内容 |
|------|------|
| 论文全称 | Flow Interaction Graph Analysis: Unknown Encrypted Malicious Traffic Detection |
| 作者 | Chuanpu Fu, Qi Li, Ke Xu |
| 机构 | 清华大学计算机科学与技术系; 清华大学网络科学与网络空间研究所 |
| 发表年份 | 2024 |
| 会议/期刊 | IEEE/ACM Transactions on Networking (TNET) |
| 关键词 | Malicious Traffic Detection, Machine Learning, Graph Learning, Unsupervised Learning, Flow Interaction Graph |
| 代码 | 论文未明确说明 |

## 1. 一句话总结

提出 HyperVision，一种基于流交互图的无监督加密恶意流量检测系统，通过构建流交互模式图并利用图学习检测异常交互模式，实现对未知模式加密恶意流量的实时检测，在 140 个攻击上比现有方法准确率提升 13.9%，检测吞吐量达 15.82 Mpps，平均延迟 0.29 秒。

## 2. 摘要翻译

**原文：**
Nowadays traffic on the Internet has been widely encrypted to protect its confidentiality and privacy. However, traffic encryption is always abused by attackers to conceal their malicious behaviors. Since encrypted malicious traffic is similar to benign flows, it can easily evade traditional detection. In particular, the existing encrypted traffic detection methods are supervised which rely on the prior knowledge of known attacks (e.g., labeled datasets). Detecting unknown encrypted malicious traffic, which does not require prior knowledge, is still an open problem. In this paper, we propose HyperVision, an unsupervised machine learning (ML) based malicious traffic detection system. Particularly, HyperVision is able to detect unknown patterns of encrypted malicious traffic by utilizing a graph built upon flow interaction patterns, instead of learning the features of specific known attacks. We develop an unsupervised graph learning method to detect abnormal interaction patterns by analyzing the graph features, which allows HyperVision to detect unknown attacks without requiring any labeled datasets. Moreover, we establish an information theory model to prove the effectiveness of HyperVision. We show the performance of HyperVision by real-world experiments with 140 attacks. The experimental results illustrate that HyperVision outperforms the state-of-the-art methods by 13.9% accuracy improvement. Moreover, HyperVision achieves 15.82 Mpps detection throughput with the average detection latency of 0.29s.

**中文翻译：**
如今互联网上的流量已被广泛加密以保护其机密性和隐私。然而，流量加密总是被攻击者滥用来隐藏其恶意行为。由于加密恶意流量与良性流相似，它可以轻易逃避传统检测。特别是，现有的加密流量检测方法是监督的，依赖于已知攻击的先验知识（如标记数据集）。检测不需要先验知识的未知加密恶意流量仍然是一个开放问题。本文提出 HyperVision，一种基于无监督机器学习的恶意流量检测系统。特别是，HyperVision 能够通过利用基于流交互模式构建的图来检测未知模式的加密恶意流量，而不是学习特定已知攻击的特征。我们开发了一种无监督图学习方法，通过分析图特征检测异常交互模式，使 HyperVision 能够在不需要任何标记数据集的情况下检测未知攻击。此外，我们建立了信息理论模型来证明 HyperVision 的有效性。我们通过 140 个攻击的真实世界实验展示了 HyperVision 的性能。实验结果表明，HyperVision 比现有方法准确率提升 13.9%。此外，HyperVision 实现了 15.82 Mpps 的检测吞吐量，平均检测延迟为 0.29 秒。

## 3. 方法动机（Motivation）

### 3.1 问题背景与痛点

- **加密恶意流量的隐蔽性**：超过 80% 网站采用 HTTPS，加密恶意流量与良性流相似，可以逃避传统检测
- **现有方法的局限**：
  - 监督方法依赖已知攻击的标记数据集，无法检测未知攻击
  - 单流特征学习无法捕获攻击的多流交互模式
  - 现有方法无法同时检测加密和非加密恶意流量
  - 现有方法无法实现实时高速检测
- **未知攻击检测的挑战**：零日攻击没有先验知识，无法通过监督学习检测

### 3.2 核心直觉

- **流交互模式**：攻击涉及多个攻击步骤，产生与良性不同的流交互模式
- **图表示**：将流交互模式表示为图，利用图结构特征检测异常
- **无监督学习**：通过分析图特征而非学习特定攻击特征，实现未知攻击检测

## 4. 方法设计（Method Design）

### 4.1 整体流程

```
原始流量 → 流分类 → 图构建 → 图预处理 → 异常检测 → 告警
            (短/长流)  (顶点/边)  (连通分量,   (顶点覆盖,
                                    聚类)        聚类)
```

### 4.2 三大模块

**模块一：图构建（Graph Construction）**
- **输入**：原始网络流量
- **处理**：
  - 流分类：将流分为短流和长流
  - 短流聚合：基于相似性聚合大量短流，降低图密度
  - 长流分布拟合：记录长流的数据包特征分布
  - 顶点：不同地址
  - 边：短流聚合或长流分布
- **输出**：流交互图
- **关键点**：分别处理短流和长流，降低图密度同时保留高保真信息

**模块二：图预处理（Graph Pre-Processing）**
- **输入**：流交互图
- **处理**：
  - 提取连通分量
  - 计算分量的高级统计特征
  - 聚类检测仅包含良性交互模式的分量
  - 过滤良性分量，减少图规模
  - 对识别的分量进行边预聚类
- **输出**：预处理后的图
- **关键点**：通过聚类过滤良性分量，减少后续处理开销

**模块三：异常交互检测（Abnormal Interaction Detection）**
- **输入**：预处理后的图
- **处理**：
  - 通过求解顶点覆盖问题识别关键顶点
  - 对每个关键顶点，聚类其连接的边
  - 基于流特征和结构特征进行聚类
  - 计算聚类损失函数识别异常边
  - 异常边指示加密恶意流量
- **输出**：检测到的恶意流量
- **关键点**：顶点覆盖确保最小化聚类数量，实现实时检测

### 4.3 关键公式

- **流记录熵模型**：基于信息理论分析不同数据源保留的信息量
- **顶点覆盖**：$\min |S|$ s.t. 每条边至少有一个端点在 $S$ 中
- **聚类损失**：基于流特征和结构特征的距离度量

### 4.4 优缺点

**优势：**
- 首个实时无监督检测未知加密恶意流量的系统
- 基于流交互图而非单流特征，捕获多流交互模式
- 通用检测：同时检测加密和非加密恶意流量
- 信息理论模型证明图的信息保留接近最优
- 高吞吐量（15.82 Mpps）和低延迟（0.29s）

**局限：**
- 不适用于被动攻击（不生成流量的攻击）
- 短流聚合可能丢失部分信息
- 图构建的计算开销在极大规模流量下可能成为瓶颈

## 5. 与其他方法对比（Comparison）

### 5.1 创新点

| 创新点 | 本文方法 | 现有方法 |
|--------|----------|----------|
| 检测范式 | 无监督（无需标记数据） | 监督（需要标记数据） |
| 特征来源 | 流交互图（多流） | 单流特征 |
| 攻击类型 | 未知攻击 | 已知攻击 |
| 通用性 | 加密+非加密 | 通常仅加密 |
| 实时性 | 高吞吐量+低延迟 | 通常较慢 |

### 5.2 与 Baseline 对比

与 5 种现有方法对比：
- TLS Extensions 方法
- 时间序列方法
- TLS Handshakes 方法
- 流统计方法
- 网络日志方法

**关键差异**：
- 现有方法依赖监督学习和已知攻击知识，HyperVision 无监督
- 现有方法学习单流特征，HyperVision 学习流交互模式
- HyperVision 准确率提升 13.9%

## 6. 实验表现（Experiments）

### 6.1 数据集

| 数据集 | 描述 | 规模 |
|--------|------|------|
| 92 攻击数据集 | 包括 80 个新收集的数据集 | 92 种攻击 |
| VPC 数据集 | 虚拟私有云，1500+ 实例 | 48 种加密攻击 |
| 攻击类型 | 加密洪水、Web 攻击、恶意软件活动 | - |

### 6.2 Baseline 方法

- 5 种现有 state-of-the-art 方法
- 包括监督和无监督方法

### 6.3 评估指标

- Accuracy
- F1-score
- 检测吞吐量（Mpps）
- 检测延迟（秒）
- 误报率

### 6.4 关键结果

**检测准确性：**
- 在 140 个攻击上准确率提升 13.9%
- F1-score 超过 0.86
- 44 种真实隐蔽攻击无法被所有 baseline 识别，HyperVision 成功检测

**检测效率：**
- 检测吞吐量：15.82 Mpps（平均超过 100 Gb/s）
- 平均检测延迟：0.29 秒

**未知攻击检测：**
- 无监督方式检测未知模式攻击
- 包括高级侧信道攻击（CVE-2020-36516）和新发现的加密货币挖矿攻击

**误报率：**
- 真实世界案例中误报极少
- 误报可被轻松过滤

## 7. 学习与应用（Learning & Application）

### 7.1 开源情况

- **代码**：论文未明确说明
- **可复现性**：提供了详细的算法描述和理论分析

### 7.2 可迁移价值

- **图学习方法**：流交互图构建和分析方法可应用于其他网络分析任务
- **无监督检测**：无监督检测范式可应用于其他异常检测场景
- **信息理论分析**：信息保留分析方法可应用于其他数据源评估
- **实时检测**：高效图处理方法可应用于其他实时分析场景

### 7.3 实际应用场景

- **企业网络安全**：实时检测加密恶意流量
- **云安全**：在虚拟私有云中检测攻击
- **入侵检测**：作为入侵检测系统的核心组件
- **威胁情报**：检测未知攻击模式

## 8. 总结（Summary）

### 8.1 核心思想

HyperVision 的核心思想是将流交互模式表示为图，利用无监督图学习检测异常交互模式，实现对未知加密恶意流量的实时检测。短流聚合和长流分布拟合降低图密度同时保留高保真信息，顶点覆盖和聚类实现高效检测，信息理论模型证明图的信息保留接近最优。

### 8.2 快速流程图

```
输入：原始网络流量
  ↓
流分类（短流 vs 长流）
  ↓
图构建（短流聚合 + 长流分布拟合）
  ↓
图预处理（连通分量提取 + 良性分量过滤）
  ↓
异常检测（顶点覆盖 + 聚类）
  ↓
输出：检测到的恶意流量 + 告警
```

## 9. 知识链接（Knowledge Links）

- [[malicious-traffic-detection]]：本文的核心任务
- [[graph-neural-network]]：图学习方法的基础
- [[anomaly-detection]]：无监督异常检测的范式
- [[encrypted-traffic-analysis]]：加密流量分析的背景
- [[tunnel-detection]]：隧道检测的相关任务

## 10. 证据记录（Evidence）

| 声明 | 证据 | 来源 |
|------|------|------|
| 准确率提升 13.9% | 与 5 种现有方法对比，140 个攻击 | 论文 §VIII 实验结果 |
| F1-score 超过 0.86 | 多个攻击数据集 | 论文 §VIII 实验结果 |
| 检测吞吐量 15.82 Mpps | 实时检测实验 | 论文 §VIII 实验结果 |
| 平均检测延迟 0.29 秒 | 实时检测实验 | 论文 §VIII 实验结果 |
| 44 种隐蔽攻击无法被 baseline 识别 | 对比实验 | 论文 §VIII 实验结果 |
| 信息保留接近最优 | 信息理论分析 | 论文 §VII |

## 11. 原始资料链接（Source Links）

- **PDF**：`00-inbox/PDFs/2024-TNET-Flow_Interaction_Graph_Analysis_Unknown_Encrypted_Malicious_Traffic_Detection.pdf`
- **MinerU MD**：`02-parsed-markdown/2024-TNET-Flow_Interaction_Graph_Analysis_Unknown_Encrypted_Malicious_Traffic_Detection.md`

## 12. 后续问题（Open Questions）

1. **图规模扩展**：在极大规模网络（如 ISP 级别）下，图构建和处理的效率如何？
2. **动态网络**：在网络拓扑和流量模式快速变化时，图的更新策略如何？
3. **对抗攻击**：攻击者是否可以通过模仿良性交互模式逃避检测？
4. **多协议支持**：对于新型加密协议，流交互模式的通用性如何？
5. **隐私保护**：图构建过程中是否涉及用户隐私信息？

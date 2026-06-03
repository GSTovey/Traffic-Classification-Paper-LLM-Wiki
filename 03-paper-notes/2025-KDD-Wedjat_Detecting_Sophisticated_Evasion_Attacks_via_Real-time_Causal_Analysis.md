---
type: paper
title_original: "Wedjat: Detecting Sophisticated Evasion Attacks via Real-time Causal Analysis"
title_cn: "Wedjat: 基于实时因果分析的高级逃逸攻击检测"
authors:
  - Li Gao
  - Chuanpu Fu
  - Xinhao Deng
  - Ke Xu
  - Qi Li
year: 2025
venue: "KDD"
doi: "10.1145/3690624.3709218"
url: ""
pdf: "00-inbox/PDFs/2025-KDD-Wedjat_Detecting_Sophisticated_Evasion_Attacks_via_Real-time_Causal_Analysis.pdf"
mineru_md: "02-parsed-markdown/2025-KDD-Wedjat_Detecting_Sophisticated_Evasion_Attacks_via_Real-time_Causal_Analysis.md"
status: processed
reading_level: L2
research_area:
  - malicious-traffic-detection
  - encrypted-traffic-analysis
  - evasion-attack-detection
task:
  - malicious-traffic-detection
  - evasion-attack-detection
  - realtime-detection
method:
  - causal-network
  - belief-propagation
  - packet-embedding
  - DAG
  - unsupervised-learning
dataset:
  - 13-million-flows
  - real-world-enterprise
  - 5-evasion-attacks
code: ""
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

# Wedjat: 基于实时因果分析的高级逃逸攻击检测

## 0. 基础信息

| 字段 | 内容 |
|------|------|
| 论文全称 | Wedjat: Detecting Sophisticated Evasion Attacks via Real-time Causal Analysis |
| 作者 | Li Gao, Chuanpu Fu, Xinhao Deng, Ke Xu, Qi Li |
| 机构 | 清华大学; 中关村实验室 |
| 发表年份 | 2025 |
| 会议/期刊 | KDD 2025 |
| 关键词 | Malicious Traffic Detection, Causal Networks, Evasion Attacks, Real-time Detection, Unsupervised Learning |
| 代码 | 论文未明确说明 |

## 1. 一句话总结

提出 Wedjat，一种基于因果网络的加密恶意流量检测系统，通过建模良性数据包交互模式并利用信念传播实时推断异常因果关系，实现对高级逃逸攻击的鲁棒检测，在真实企业网络 1300 万流上 F1-score 达 0.957，成功检测 5 种逃逸所有现有方法的高级逃逸攻击（F1 > 0.915），检测延迟 < 0.125 秒。

## 2. 摘要翻译

**原文：**
Traffic encryption has been widely adopted to protect the confidentiality and integrity of Internet traffic. However, attackers can also abuse such mechanism to deliver malicious traffic. Particularly, existing methods detecting encrypted malicious traffic are not robust against evasion attacks that manipulate traffic to obfuscate traffic features. Robust detection against evasion attacks remains an open problem. To the end, we develop Wedjat, which utilizes a causal network to model benign packet interactions among relevant flows, such that it recognizes abnormal causality that represents malicious traffic and disrupted causality incurred by evasion attacks. We extensively evaluate Wedjat with millions of flows collected from a real-world enterprise. The experimental results demonstrate that Wedjat achieves an accuracy of 0.957 F1-score when detecting various advanced attacks. Notably, five sophisticated evasion attacks, which have successfully evaded all existing methods, are accurately detected by Wedjat with over 0.915 F1. It demonstrates that Wedjat achieves exceptional robustness against evasions. Meanwhile, Wedjat maintains an outstanding detection latency, i.e., it can predict each packet in less than 0.125 seconds.

**中文翻译：**
流量加密已被广泛采用以保护互联网流量的机密性和完整性。然而，攻击者也可以滥用这种机制来传递恶意流量。特别是，现有检测加密恶意流量的方法对操纵流量以混淆流量特征的逃逸攻击不鲁棒。针对逃逸攻击的鲁棒检测仍然是一个开放问题。为此，我们开发了 Wedjat，它利用因果网络建模相关流之间的良性数据包交互模式，从而识别代表恶意流量的异常因果关系和由逃逸攻击引起的中断因果关系。我们使用从真实世界企业收集的数百万流广泛评估 Wedjat。实验结果表明，Wedjat 在检测各种高级攻击时达到 0.957 F1-score 的准确率。值得注意的是，五种成功逃逸所有现有方法的高级逃逸攻击被 Wedjat 以超过 0.915 F1 准确检测。这表明 Wedjat 对逃逸具有卓越的鲁棒性。同时，Wedjat 保持出色的检测延迟，即每个数据包的预测时间小于 0.125 秒。

## 3. 方法动机（Motivation）

### 3.1 问题背景与痛点

- **加密流量的滥用**：超过 70% 的网络攻击通过加密流量发起，传统 DPI 失效
- **现有方法的逃逸脆弱性**：
  - 现有方法依赖粗粒度流级特征，容易被逃逸攻击操纵
  - 逃逸攻击通过注入扰动（插入虚假包、填充包、延迟包）构造对抗样本
  - 高级逃逸攻击同时操纵多个并发恶意流的特征
- **三类逃逸攻击**：
  - **数据包级逃逸**：操纵单个数据包特征（如填充、延迟、插入）
  - **流级逃逸**：操纵单个流内多个数据包的特征（如流完成时间、流长度）
  - **多流逃逸**：操纵大量相关恶意流（如插入良性流、同时注入扰动）

### 3.2 核心直觉

- **因果关系建模**：逃逸行为违反了网络协议和原始流量行为规定的数据包交互模式
- **良性模式学习**：通过建模良性数据包交互模式，识别偏离良性模式的异常因果关系
- **因果网络**：使用有向无环图（DAG）建模数据包之间的条件概率依赖关系

## 4. 方法设计（Method Design）

### 4.1 整体流程

```
原始数据包 → 数据包嵌入 → 因果网络构建 → 基于推断的检测 → 告警
              (特征提取,    (DAG,           (信念传播,
               聚类净化)     协议语义)        异常识别)
```

### 4.2 三大模块

**模块一：数据包嵌入（Packet Embedding）**
- **输入**：原始数据包
- **处理**：
  - 特征提取：提取数据包包头的侧信道信息（包长度、时间间隔、方向等）
  - 归一化：对所有数据包向量进行归一化
  - 聚类：使用 k-means 将 d 维向量映射到一维
  - 净化：优化聚类数量，最大化聚类结果与真实标签的距离
  - 数据包评分：计算数据包与所属聚类的相似度，结合良性概率得到分数
- **输出**：数据包分数（良性/恶意/未知）
- **关键点**：将非结构化数据包转换为统一的数值表示

**模块二：因果网络构建（Causal Network Construction）**
- **输入**：数据包嵌入结果
- **处理**：
  - 基于有向无环图（DAG）构建因果网络
  - 节点：数据包
  - 边：数据包之间的条件概率依赖关系
  - 基于网络协议语义优化网络结构
  - 压缩冗余节点和边，降低复杂度
- **输出**：稀疏因果网络
- **关键点**：无监督学习，不依赖标记数据

**模块三：基于推断的检测（Inference-based Detection）**
- **输入**：因果网络和数据包分数
- **处理**：
  - 信念传播：利用已知数据包推断未知数据包
  - 比较数据包分数与推断结果
  - 识别异常因果关系（恶意流量）和中断因果关系（逃逸攻击）
- **输出**：检测结果
- **关键点**：实时推断，每个数据包 < 0.125 秒

### 4.3 关键公式

- **数据包评分**：$\operatorname{score}(\boldsymbol{p}^i) = \operatorname{sim}(\boldsymbol{p}^i; C_j) \cdot [2 \times P(+|C_j) - 1]$
- **因果关系**：$P(Y|X) \neq P(Y)$ 表示 $X \implies Y$
- **信念传播**：基于条件概率的推断算法

### 4.4 优缺点

**优势：**
- 首个利用因果网络检测高级逃逸攻击的系统
- 鲁棒性：逃逸行为必然违反因果关系，无法逃避检测
- 实时性：每个数据包检测延迟 < 0.125 秒
- 无监督：不依赖标记数据，可检测未知攻击
- 粒度：数据包级 + 流级 + 多流级检测

**局限：**
- 因果网络构建的计算开销
- 对新型协议的适应性
- 在极高速网络下的可扩展性

## 5. 与其他方法对比（Comparison）

### 5.1 创新点

| 创新点 | 本文方法 | 现有方法 |
|--------|----------|----------|
| 逃逸鲁棒性 | 高（因果关系不可逃逸） | 低（特征可操纵） |
| 检测粒度 | 数据包+流+多流 | 通常仅流级 |
| 学习方式 | 无监督（因果网络） | 监督或无监督 |
| 实时性 | < 0.125 秒/包 | 通常较慢 |
| 攻击类型 | 已知+未知+逃逸 | 通常仅已知 |

### 5.2 与 Baseline 对比

与现有恶意流量检测方法对比：
- Zeek（规则检测）
- Poseidon（流特征）
- nPrintML（AutoML）
- Kitsune（自编码器）
- FS-Net（RNN）
- ET-BERT（Transformer）
- HyperVision（图学习）

**关键差异**：
- 现有方法被 5 种高级逃逸攻击逃逸，Wedjat 成功检测
- Wedjat 在数据包级、流级、多流级均鲁棒
- Wedjat 实时性优于大多数方法

## 6. 实验表现（Experiments）

### 6.1 数据集

| 数据集 | 描述 | 规模 |
|--------|------|------|
| 真实企业网络 | 顶级网络基础设施提供商 | 1300 万流 |
| 恶意流量 | 真实世界威胁 | 多种攻击类型 |
| 逃逸攻击 | 5 种高级逃逸攻击 | - |

### 6.2 Baseline 方法

- 5 种 state-of-the-art 方法
- 包括监督和无监督方法

### 6.3 评估指标

- F1-score
- Accuracy
- 检测延迟（秒）
- 逃逸攻击检测率

### 6.4 关键结果

**整体检测性能：**
- F1-score = 0.957
- 优于 5 种 state-of-the-art 方法

**逃逸攻击检测：**
- 5 种高级逃逸攻击（逃逸所有现有方法）
- Wedjat 检测 F1 > 0.915
- 包括数据包级、流级、多流级逃逸

**实时性：**
- 每个数据包检测延迟 < 0.125 秒
- 满足实时检测需求

**数据集规模：**
- 真实企业网络 1300 万流
- 包含真实世界威胁

## 7. 学习与应用（Learning & Application）

### 7.1 开源情况

- **代码**：论文未明确说明
- **可复现性**：提供了详细的算法描述

### 7.2 可迁移价值

- **因果网络**：因果建模方法可应用于其他需要鲁棒性的检测任务
- **信念传播**：实时推断方法可应用于其他实时分析场景
- **数据包嵌入**：非结构化数据嵌入方法可应用于其他网络数据分析
- **逃逸检测**：逃逸攻击检测方法可应用于其他安全领域

### 7.3 实际应用场景

- **企业网络安全**：实时检测加密恶意流量，抵抗逃逸攻击
- **入侵检测系统**：作为 IDS 的核心组件
- **威胁情报**：检测高级持续威胁（APT）
- **安全运营中心**：实时告警和响应

## 8. 总结（Summary）

### 8.1 核心思想

Wedjat 的核心思想是利用因果网络建模良性数据包交互模式，通过识别异常因果关系检测恶意流量，通过识别中断因果关系检测逃逸攻击。数据包嵌入将非结构化数据包转换为数值表示，因果网络基于协议语义构建，信念传播实现实时推断。逃逸行为必然违反因果关系，因此无法逃避检测。

### 8.2 快速流程图

```
输入：原始数据包流
  ↓
数据包嵌入（特征提取 → 聚类净化 → 评分）
  ↓
因果网络构建（DAG + 协议语义 + 压缩）
  ↓
基于推断的检测（信念传播 + 异常识别）
  ↓
输出：恶意流量检测结果 + 逃逸攻击检测结果
```

## 9. 知识链接（Knowledge Links）

- [[malicious-traffic-detection]]：本文的核心任务
- [[encrypted-traffic-analysis]]：加密流量分析的背景
- [[anomaly-detection]]：异常检测的广义框架
- [[graph-neural-network]]：因果网络与图学习的关系
- [[tunnel-detection]]：隧道检测的相关任务

## 10. 证据记录（Evidence）

| 声明 | 证据 | 来源 |
|------|------|------|
| F1-score = 0.957 | 真实企业网络 1300 万流 | 论文 §5 实验结果 |
| 5 种逃逸攻击检测 F1 > 0.915 | 高级逃逸攻击实验 | 论文 §5 实验结果 |
| 检测延迟 < 0.125 秒 | 实时性实验 | 论文 §5 实验结果 |
| 超过 70% 攻击通过加密流量 | 文献引用 | 论文 §1 |
| 逃逸行为违反因果关系 | 理论分析 | 论文 §3 |

## 11. 原始资料链接（Source Links）

- **PDF**：`00-inbox/PDFs/2025-KDD-Wedjat_Detecting_Sophisticated_Evasion_Attacks_via_Real-time_Causal_Analysis.pdf`
- **MinerU MD**：`02-parsed-markdown/2025-KDD-Wedjat_Detecting_Sophisticated_Evasion_Attacks_via_Real-time_Causal_Analysis.md`

## 12. 后续问题（Open Questions）

1. **因果网络规模**：在极大规模网络下，因果网络的构建和维护效率如何？
2. **新型协议**：对于新型加密协议，因果模式的通用性如何？
3. **对抗因果攻击**：攻击者是否可以通过模仿良性因果模式逃避检测？
4. **分布式部署**：因果网络在分布式环境下的同步和一致性如何？
5. **隐私保护**：因果网络构建过程中是否涉及用户隐私信息？

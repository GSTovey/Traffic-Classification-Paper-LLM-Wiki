---
type: paper
title_original: "Classification of Encrypted Traffic With Second-Order Markov Chains and Application Attribute Bigrams"
title_cn: "基于二阶马尔可夫链和应用属性二元组的加密流量分类"
authors: [Meng Shen, Mingwei Wei, Liehuang Zhu, Mingzhong Wang]
year: 2017
venue: "TIFS"
doi: "10.1109/TIFS.2017.2692682"
url: "unknown"
pdf: "00-inbox/PDFs/2017-TIFS-Classification_of_Encrypted_Traffic_With_Second-Order_Markov_Chains_and_Application_Attribute_Bigrams.pdf"
mineru_md: "02-parsed-markdown/2017-TIFS-Classification_of_Encrypted_Traffic_With_Second-Order_Markov_Chains_and_Application_Attribute_Bigrams.md"
status: processed
reading_level: L2
research_area: [encrypted-traffic-analysis, traffic-classification]
task: [encrypted-traffic-classification, application-identification]
method: [markov-chain, statistical-fingerprinting]
dataset: [campus-network-traffic]
code: "unknown"
relevance: medium
created: "2026-06-03"
updated: "2026-06-03"
---

## §0 基础信息

| 项目 | 内容 |
|------|------|
| 论文全称 | Classification of Encrypted Traffic With Second-Order Markov Chains and Application Attribute Bigrams |
| 作者 | Meng Shen, Mingwei Wei, Liehuang Zhu, Mingzhong Wang |
| 机构 | 北京理工大学, University of the Sunshine Coast |
| 发表时间 | 2017 |
| 期刊/会议 | IEEE Transactions on Information Forensics and Security (TIFS) |
| DOI | 10.1109/TIFS.2017.2692682 |

## §1 一句话总结

提出基于二阶马尔可夫链和应用属性二元组（Certificate包长度 + 首个Application Data大小）的加密流量分类方法，通过增加指纹多样性提升分类准确率，相比现有马尔可夫方法平均提升29%。

## §2 摘要翻译

**原始摘要：**
With a profusion of network applications, traffic classification plays a crucial role in network management and policy-based security control. The widely used encryption transmission protocols, such as the secure socket layer/transport layer security (SSL/TLS) protocols, lead to the failure of traditional payload-based classification methods. Existing methods for encrypted traffic classification cannot achieve high discrimination accuracy for applications with similar fingerprints. In this paper, we propose an attribute-aware encrypted traffic classification method based on the second-order Markov Chains. We start by exploring approaches that can further improve the performance of existing methods in terms of discrimination accuracy, and make promising observations that the application attribute bigram, which consists of the certificate packet length and the first application data size in SSL/TLS sessions, contributes to application discrimination. To increase the diversity of application fingerprints, we develop a new method by incorporating the attribute bigrams into the second-order homogeneous Markov chains. Extensive evaluation results show that the proposed method can improve the classification accuracy by 29% on the average compared with the state-of-the-art Markov-based method.

**中文翻译：**
随着网络应用的激增，流量分类在网络管理和基于策略的安全控制中扮演着关键角色。广泛使用的加密传输协议（如SSL/TLS协议）导致传统的基于载荷的分类方法失效。现有的加密流量分类方法无法对具有相似指纹的应用实现高区分准确率。本文提出一种基于二阶马尔可夫链的属性感知加密流量分类方法。作者首先探索了进一步提升现有方法区分准确率的途径，并发现应用属性二元组（由SSL/TLS会话中的Certificate包长度和首个Application Data大小组成）有助于应用区分。为了增加应用指纹的多样性，作者开发了一种将属性二元组融入二阶齐次马尔可夫链的新方法。大量评估结果表明，该方法相比最先进的马尔可夫方法平均提升29%的分类准确率。

## §3 方法动机

**痛点问题：**
- 传统基于载荷的分类方法在加密流量场景下失效
- 现有基于一阶马尔可夫链的方法在应用指纹相似时区分能力不足
- 例如：LinkedIn和Evernote的SSL/TLS状态转移序列高度相似，导致75%以上的Instagram流量被误分类

**核心直觉：**
- 一阶马尔可夫链仅考虑两个相邻状态，区分度不够
- SSL/TLS会话中的Certificate包长度和首个Application Data大小包含应用特异性信息
- 通过二阶马尔可夫链（考虑连续3个状态）可以捕获更多区分特征

**方法动机：**
- 增加应用指纹的多样性是提升分类准确率的关键
- 结合统计概率和SSL/TLS头部信息可以构建更精确的指纹

## §4 方法设计

**整体流程：**

```
输入: SSL/TLS加密流量
  ↓
Step 1: 提取SSL/TLS消息类型序列（服务端到客户端方向）
  ↓
Step 2: 构建二阶齐次马尔可夫链
  - 状态转移: P(X_t = k | X_{t-1} = j, X_{t-2} = i) = p_{i,j→k}
  - 使用连续3个状态构建转移概率
  ↓
Step 3: 提取应用属性二元组 (Attribute Bigram)
  - Certificate包长度 (22:11消息)
  - 首个Application Data大小 (23:消息)
  ↓
Step 4: 对属性二元组进行聚类
  - 使用K-means聚类算法
  - 设计聚类准确度度量准则（无需重新训练分类器）
  ↓
Step 5: 将聚类结果融入马尔可夫链
  - 扩展状态空间，增加指纹多样性
  ↓
输出: 应用分类结果
```

**关键公式：**
- 一阶转移概率: P(X_t = j | X_{t-1} = i) = p_{i→j}
- 二阶转移概率: P(X_t = k | X_{t-1} = j, X_{t-2} = i) = p_{i,j→k}
- 流量分类概率: P({X_1,...,X_T}) = q_{i_1} × ∏ p_{i_{t-1}→i_t} × w_{i_T}

**优势：**
- 计算复杂度低（相比神经网络方法）
- 无需解密payload，仅利用SSL/TLS头部元数据
- 二阶马尔可夫链在一阶和高阶之间取得平衡

**局限：**
- 依赖SSL/TLS协议，对非SSL/TLS加密流量不适用
- 需要足够的训练数据构建准确的转移概率矩阵

## §5 与其他方法对比

**创新点：**
1. 首次引入应用属性二元组（Attribute Bigram）用于加密流量分类
2. 使用二阶马尔可夫链替代一阶马尔可夫链，增加状态转移的区分度
3. 设计无需重新训练的聚类准确度度量准则

**与基线对比：**
- 对比方法: Korczynski和Duda的一阶马尔可夫链方法（2013年）
- 改进点:
  - 一阶→二阶: 考虑连续3个状态而非2个
  - 增加属性二元组特征: Certificate包长度 + Application Data大小
  - 聚类扩展: 将属性二元组聚类结果融入状态空间

## §6 实验表现

**数据集：**
- 校园网真实流量数据
- 包含多种流行应用（LinkedIn, Evernote, Instagram, Twitter等）

**评估指标：**
- 分类准确率 (Accuracy)
- 真阳性率 (TPR)
- 假阳性率 (FPR)

**主要结果：**
- 整体分类准确率约90%
- 相比一阶马尔可夫链方法平均提升29%
- 对Instagram等相似指纹应用的分类效果显著提升

**关键发现：**
- 一阶马尔可夫链对相似指纹应用（如LinkedIn vs Evernote）误分类严重
- 二阶马尔可夫链有效提升了区分能力
- 属性二元组进一步增强了指纹的唯一性

## §7 学习与应用

**开源情况：**
- 论文未明确说明是否开源代码

**复现要点：**
- 需要SSL/TLS流量数据
- 提取服务端消息类型序列
- 构建二阶马尔可夫链转移概率矩阵
- 提取Certificate包长度和Application Data大小
- 对属性二元组进行K-means聚类

**迁移价值：**
- 方法可应用于其他SSL/TLS加密流量分类场景
- 属性二元组思路可扩展到其他协议特征
- 二阶马尔可夫链框架可与其他特征结合

## §8 总结

**核心思想：** 通过二阶马尔可夫链和应用属性二元组增加加密流量指纹的多样性，提升分类准确率。

**快速流程：**
```
SSL/TLS流量 → 提取消息类型序列 → 二阶马尔可夫链建模
                ↓
        提取属性二元组 → K-means聚类 → 融入马尔可夫链
                ↓
        最大似然分类 → 应用识别结果
```

## §9 知识链接

- [[encrypted-traffic-analysis]] - 加密流量分析核心技术
- [[traffic-classification]] - 流量分类基础方法
- [[markov-chain]] - 马尔可夫链建模方法
- [[ssl-tls-protocol]] - SSL/TLS协议特征提取
- [[statistical-fingerprinting]] - 统计指纹方法
- [[application-identification]] - 应用识别任务

## §10 证据记录

| 声明 | 证据 | 证据强度 |
|------|------|----------|
| 一阶马尔可夫链对相似指纹应用分类效果差 | LinkedIn vs Evernote误分类案例（Fig 2,3） | 强（实验数据） |
| 二阶马尔可夫链提升分类准确率 | 平均提升29% | 强（实验结果） |
| 属性二元组有助于应用区分 | Certificate包长度和Application Data大小的区分度分析 | 中（观察分析） |
| 整体分类准确率约90% | 校园网流量实验结果 | 强（实验数据） |

## §11 原始资料链接

- PDF: `00-inbox/PDFs/2017-TIFS-Classification_of_Encrypted_Traffic_With_Second-Order_Markov_Chains_and_Application_Attribute_Bigrams.pdf`
- MinerU MD: `02-parsed-markdown/2017-TIFS-Classification_of_Encrypted_Traffic_With_Second-Order_Markov_Chains_and_Application_Attribute_Bigrams.md`

## §12 后续问题

1. 二阶马尔可夫链是否可以进一步扩展到更高阶？计算复杂度如何权衡？
2. 属性二元组是否可以扩展到更多SSL/TLS特征？
3. 该方法对TLS 1.3等新版本协议的适用性如何？
4. 如何处理应用指纹随时间变化的问题？
5. 与深度学习方法相比，马尔可夫链方法的优劣势如何？

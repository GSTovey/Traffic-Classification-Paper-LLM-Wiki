---
type: paper
title_original: "Exploring Uncharted Waters of Website Fingerprinting"
title_cn: "探索网站指纹识别的未知领域"
authors:
  - Ishan Karunanayake
  - Jiaojiao Jiang
  - Nadeem Ahmed
  - Sanjay K. Jha
year: 2023
venue: IEEE TIFS
doi: "10.1109/TIFS.2023.3342607"
url: unknown
pdf: "00-inbox/PDFs/2023-TIFS-Exploring_Uncharted_Waters_of_Website_Fingerprinting.pdf"
mineru_md: "02-parsed-markdown/2023-TIFS-Exploring_Uncharted_Waters_of_Website_Fingerprinting.md"
status: processed
reading_level: L2
research_area: ["网站指纹识别", "Tor匿名", "图神经网络", "流量分析"]
task: ["网站指纹识别", "DApp指纹识别", "重载流量分析"]
method: ["GNN", "Graph Fingerprinting Node Classification (GFNC)", "Graph Fingerprinting Graph Classification (GFGC)", "CTDNE", "CNN"]
dataset:
  - NORMAL_TOR_NOREFRESH
  - NORMAL_TOR_REFRESH
  - DAPP_CHROME
  - DAPP_TOR_NOREFRESH
  - DAPP_TOR_REFRESH
code: unknown
relevance: high
created: 2026-06-09
updated: 2026-06-09
---

# Exploring Uncharted Waters of Website Fingerprinting

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Exploring Uncharted Waters of Website Fingerprinting |
| 中文标题 | 探索网站指纹识别的未知领域 |
| 作者 | Ishan Karunanayake, Jiaojiao Jiang, Nadeem Ahmed, Sanjay K. Jha |
| 年份 | 2023 |
| 会议/期刊 | IEEE TIFS |
| DOI | 10.1109/TIFS.2023.3342607 |
| 研究方向 | 网站指纹识别、Tor 匿名性、图神经网络 |
| 任务类型 | 网站指纹识别（WF）、DApp 指纹识别、reload 流量分析 |
| 方法关键词 | GNN、GFNC、GFGC、CTDNE、图分类、节点分类 |
| 数据集 | 5 个自采数据集（NORMAL_TOR_NOREFRESH/REFRESH、DAPP_CHROME/TOR_NOREFRESH/REFRESH） |
| 是否开源 | 否（计划公开） |
| PDF | `../00-inbox/PDFs/2023-TIFS-Exploring_Uncharted_Waters_of_Website_Fingerprinting.pdf` |
| MinerU Markdown | `../02-parsed-markdown/2023-TIFS-Exploring_Uncharted_Waters_of_Website_Fingerprinting.md` |

---

## 1. 一句话总结

> 提出两种基于 GNN 的网站指纹识别技术（GFNC 和 GFGC），在 DApp 指纹识别和 reload 流量场景下优于现有方法，发现 DApp 比传统网站更难被指纹识别。

---

## 2. 摘要翻译

### 2.1 摘要原文

Amidst the rapid technological advancements of today, privacy and anonymity are facing increasing threats. Tor, one of the most widely used anonymity networks, enables users to browse the Internet without their activities being tracked. Extensive research has been conducted on both attacking and defending the anonymity of Tor users. Website Fingerprinting (WF) is one of the popular de-anonymisation techniques employed against Tor users. This paper presents two novel WF techniques based on Graph Neural Networks (GNNs) to explore two relatively understudied avenues of WF: the fingerprintability of Decentralised Applications (DApps) and the impact of reload traffic on WF. Due to the lack of publicly available datasets for DApp traffic and reload traffic suitable for WF, we collected five new datasets for our experiments. Our findings reveal that GNN-based techniques surpass the performance of state-of-the-art WF techniques when reload traffic is used. Meanwhile, certain high-performing state-of-the-art techniques exhibit a significant reduction in accuracy, more than 40%, when reload traffic is used instead of homepage traffic. Additionally, we identify that DApps are less susceptible to fingerprinting than conventional websites, leading to a 25% decrease in accuracy in some state-of-the-art WF techniques.

### 2.2 摘要中文翻译

在当今快速的技术进步中，隐私和匿名性面临日益增长的威胁。Tor 作为最广泛使用的匿名网络之一，使用户能够在不被追踪的情况下浏览互联网。针对 Tor 用户的匿名性，已有大量攻击和防御研究。网站指纹识别（WF）是针对 Tor 用户的一种流行去匿名化技术。本文提出两种基于图神经网络（GNN）的新型 WF 技术，探索两个相对未被充分研究的 WF 方向：去中心化应用（DApps）的可指纹性以及 reload 流量对 WF 的影响。由于缺乏适用于 WF 的 DApp 流量和 reload 流量公开数据集，我们收集了五个新数据集用于实验。研究发现，当使用 reload 流量时，基于 GNN 的技术超越了现有最先进的 WF 技术的性能。同时，某些高性能的现有技术在使用 reload 流量替代首页访问流量时，精度下降超过 40%。此外，我们发现 DApp 比传统网站更不容易被指纹识别，导致某些现有 WF 技术的精度下降约 25%。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

现有 WF 研究主要关注首次访问首页的流量，未考虑 reload 流量和 DApp 流量。GNN 在其他领域展现出强大能力，但在 WF 中应用有限。需要探索这些未被充分研究的 WF 场景。

### 3.2 现有方法的痛点和不足

- 现有 WF 数据集收集于 5 年前，可能不反映当前 Tor 流量特征
- 数据收集使用自动化工具清除缓存，不反映真实用户行为
- Shen et al. 的 GNN-based WF 仅使用 Chrome 流量，未考虑 Tor
- 未与 VarCNN、TikTok 等更强的 baseline 对比
- 未研究 reload 流量和 DApp 流量的指纹识别

### 3.3 论文的研究假设或核心直觉

GNN 能够建模复杂的关系和依赖，可能在 WF 中捕获 CNN 无法捕获的模式。DApp 由于共享通信接口和加密设置，流量可能更难区分。Reload 流量与首次访问流量模式不同，可能影响 WF 性能。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | Web3 和 DApp 的兴起，用户实际浏览行为包含 reload | §I |
| 痛点提炼 | 现有 WF 仅考虑首次首页访问，未覆盖 DApp 和 reload 场景 | §I, §II |
| 问题转化 | DApp 是否比传统网站更难被指纹识别？Reload 流量如何影响 WF？GNN 在这些场景下表现如何？ | §I |
| 文献定位 | Shen et al. 首次探索 DApp 指纹识别，但存在方法论局限 | §II-B |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 1 | DApp 比传统网站更难被指纹识别 | DApp 共享通信接口和加密设置 | 跨数据集对比实验 |
| 核心假设 2 | Reload 流量会降低现有 WF 技术的精度 | 缓存导致流量模式变化 | Reload vs No-refresh 对比 |
| 核心假设 3 | GNN 在 reload 和 DApp 场景下优于 CNN | GNN 能建模复杂关系 | 多方法对比实验 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 1 | 支撑 | TikTok 在 DApp 上精度下降 25% | §V-A.5 |
| 核心假设 2 | 支撑 | AWF 精度下降 6%，TikTok 下降 14% | §V-A.6 |
| 核心假设 3 | 部分支撑 | GNN 在 reload 和 Chrome DApp 上表现最好，但在 Tor DApp 上较差 | §V-A.3, V-A.5, V-A.6 |

---

## 4. 方法设计

### 4.1 方法整体流程

**GFNC（节点分类）**：
1. 将每个流量 trace 表示为图中的节点
2. 客户端和入口守卫作为中心节点
3. 使用手动提取的 175 个特征作为节点属性
4. 使用 GNN 进行节点分类

**GFGC（图分类）**：
1. 为每个流量 trace 创建独立的图
2. 每个包作为一个节点，包大小为节点属性
3. 连续包之间创建边，burst 之间创建额外边
4. 使用 CTDNE 生成图嵌入
5. 使用 GNN 进行图分类

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | 流量 trace | 提取包大小、方向、时间戳 | 元数据 | 特征准备 |
| Step 2 (GFNC) | 元数据 | 构建客户端-守卫-流节点图 | 图结构 | 图表示 |
| Step 2 (GFGC) | 元数据 | 为每个 trace 构建包序列图 | 图结构 | 图表示 |
| Step 3 (GFNC) | 图 + 特征 | GNN 消息传递 + GRU 更新 | 节点标签 | 分类 |
| Step 3 (GFGC) | 图 | CTDNE 嵌入 + MLP 分类 | 图标签 | 分类 |

### 4.3 模型结构或系统模块

**GFNC 模型架构**：
| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 消息函数 (MLP) | 学习节点间消息 | 连接的节点隐藏状态 | 消息 | 传递到聚合 |
| 聚合函数 (Mean) | 聚合邻居消息 | 消息集合 | 聚合消息 | 传递到更新 |
| GRU 更新 | 更新节点隐藏状态 | 聚合消息 + 当前状态 | 新状态 | 迭代更新 |
| 全连接层 | 生成分类输出 | 最终节点状态 | 类别概率 | 最终输出 |

**GFGC 模型架构**：
| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| CTDNE | 生成时序图嵌入 | 带时间边的图 | 嵌入向量 | 输入到 MLP |
| MLP 层 (×4) | 特征提取 | 嵌入向量 | 特征 | 传递到池化 |
| 池化层 | 聚合节点特征 | MLP 输出 | 图表示 | 传递到线性层 |
| 线性层 | 分类 | 图表示 | 类别概率 | 最终输出 |

### 4.4 公式、算法和机制解释

- **GNN 消息传递**：$a_v^k = A(\{h_u^{k-1} | u \in N_v\})$，聚合邻居信息
- **GNN 状态更新**：$h_v^k = B(h_v^{k-1}, a_v^k)$，GRU 更新隐藏状态
- **GFGC 图构建**：每个包为节点，连续包之间创建边，burst 间创建额外时序边
- **CTDNE**：在带时间信息的图上进行时间随机游走，生成网络嵌入

### 4.5 方法优势

- GNN 能建模复杂的流量关系和依赖
- GFNC 是首个基于节点分类的 WF 方法
- GFGC 利用时序信息（CTDNE），增强特征表达
- 在 reload 流量和 Chrome DApp 场景下表现优异
- 提供了 5 个新的公开数据集

### 4.6 方法不足

- GFGC 的 CTDNE 嵌入生成计算开销大（约 400 小时处理完整数据集）
- 在 Tor DApp 流量上 GNN 表现不如 AWF 和 TikTok
- 数据集规模较小（每个网站 50-100 个 trace）
- 手动数据收集可能引入不一致性
- DF 和 GraphDApp 在新数据集上表现较差

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

现有方法主要使用 CNN 处理包方向序列，本文探索 GNN 建模流量的图结构关系，并首次系统研究 DApp 和 reload 流量场景。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| GFNC（节点分类 WF） | 将流量 trace 表示为图中的节点 | 高 | 是 |
| GFGC（图分类 WF） | 使用 CTDNE 生成时序图嵌入 | 高 | 是 |
| DApp WF 系统研究 | 首次在 Tor 下评估 DApp 可指纹性 | 中 | 否 |
| Reload 流量研究 | 首次研究 reload 流量对 WF 的影响 | 中 | 否 |
| 5 个新数据集 | 覆盖多种 WF 场景 | 中 | 是 |

### 5.3 适用场景

- Tor 用户行为分析
- DApp 流量监控
- 网站指纹识别攻击评估
- WF 防御机制测试

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| DF (CNN) | 经典方法 | 不使用时序信息，新数据集表现差 | GNN 建模复杂关系 |
| AWF (多模型) | 灵活 | Reload 流量下降明显 | GNN 在 reload 上更稳定 |
| TikTok (时序+方向) | 使用时序信息 | DApp 上下降 25% | GNN 在 DApp 上表现更好 |
| VarCNN (ResNet) | 数据效率高 | 新数据集表现差 | - |
| GraphDApp (GNN) | 首个 GNN-based | 仅用 Chrome，未开源 | 扩展到 Tor，提供开源 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- Closed-world 和 Open-world 两种场景
- 7 种 WF 技术对比：DF、AWF、VarCNN、TikTok、GraphDApp、GFNC、GFGC
- 5 个数据集，每个 15 个网站，50-100 个 trace/网站
- 60% 训练 / 20% 验证 / 20% 测试
- 评价指标：Top-1 Accuracy、Top-3 Accuracy、Precision、Recall、F1

### 6.2 数据集

| 数据集 | 场景 | 网站数 | Trace 数/网站 |
|---|---|---|---|
| NORMAL_TOR_NOREFRESH | SCN 1: 首次访问正常网站 (Tor) | 15 | 50 |
| NORMAL_TOR_REFRESH | SCN 2: Reload 正常网站 (Tor) | 15 | 50 |
| DAPP_CHROME | SCN 3: Chrome 访问 DApp | 15 | 50 |
| DAPP_TOR_NOREFRESH | SCN 4: 首次访问 DApp (Tor) | 15 | 50 |
| DAPP_TOR_REFRESH | SCN 5: Reload DApp (Tor) | 15 | 50 |

### 6.3 Baseline

- Deep Fingerprinting (DF)
- AWF
- VarCNN
- TikTok
- GraphDApp

### 6.4 评价指标

- Top-1 Accuracy
- Top-3 Accuracy
- Precision / Recall（Combined 数据集）
- F1 Score（Open-world）

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 (GFNC/GFGC) | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| NORMAL_TOR_NOREFRESH | Top-1 | 57.22% / 51.33% | 77.67% (TikTok) | -20.5% | Baseline 场景 |
| DAPP_CHROME | Top-1 | 72.76% / 76.67% | 71.60% (AWF) | +5.2% | GNN 优势场景 |
| DAPP_TOR_REFRESH | Top-1 | 53.75% / 35.33% | 38.80% (TikTok) | +15.0% | GNN 优势场景 |
| NORMAL_TOR_REFRESH | Top-1 | 62.01% / 43.33% | 35.07% (AWF) | +27.0% | Reload 场景 |
| COMBINED_NORMAL | Top-1 | 55.01% / 28.33% | 47.40% (TikTok) | +7.6% | 动态行为 |

### 6.6 优势最明显的场景

- Reload 流量：GFNC 比 AWF 高 27%，比 TikTok 高 30%
- Chrome DApp 流量：GFGC 最高（76.67%）
- 动态用户行为（Combined 数据集）：GFNC 表现最好

### 6.7 局限性

- 数据集规模较小，可能影响泛化性
- GFGC 的 CTDNE 嵌入生成计算开销大
- 在 Tor DApp 场景下 GNN 表现不如传统方法
- 数据集的有效期有限（随 Tor 和网站更新而过时）
- Open-world 实验使用模拟方式

---

## 7. 学习与应用

### 7.1 是否开源？

否（计划公开数据集）

### 7.2 复现关键步骤

1. 使用 Tor Browser 11.5.1 和 Wireshark 手动采集流量
2. 按照 5 个场景分别收集数据集
3. 提取 175 个统计特征（GFNC）或构建图结构（GFGC）
4. 实现 GFNC 模型（消息传递 GNN + GRU）
5. 实现 GFGC 模型（CTDNE + MLP）

### 7.3 关键超参数、预处理和训练细节

**GFNC**：
- 学习率：0.0001
- Dropout：0.2
- 隐藏层数：1
- 聚合函数：Mean
- 激活函数：ReLU

**GFGC**：
- 学习率：0.01
- Dropout：0.5
- MLP 层数：5
- 隐藏单元：64
- CTDNE 维度：32

### 7.4 能否迁移到其他任务？

可以。GNN-based 流量分析方法可以迁移到：
- 恶意流量检测
- 应用识别
- 加密流量分类
- 隧道流量检测

### 7.5 对我的研究有什么启发？

- GNN 在流量分析中具有潜力，特别是在非标准场景下
- Reload 流量是 WF 研究中被忽视的重要场景
- DApp 流量的特殊性使其更难被指纹识别
- 时序信息对 WF 性能有显著影响
- 数据集的时效性是 WF 研究的重要考虑因素

---

## 8. 总结

### 8.1 核心思想

> GNN 建模流量图结构，在 reload 和 DApp 场景下优于 CNN

### 8.2 速记版 Pipeline

1. 收集 5 个 WF 场景的数据集
2. GFNC：构建客户端-守卫-流节点图，用 GNN 分类
3. GFGC：为每个 trace 构建包序列图，用 CTDNE + MLP 分类
4. 与 DF、AWF、TikTok 等 5 种方法对比
5. 在 reload 和 DApp 场景下验证 GNN 优势

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- website fingerprinting
- Tor anonymity
- Graph Neural Networks
- DApp fingerprinting
- reload traffic

### 9.2 相关方法

- Deep Fingerprinting (DF)
- TikTok
- AWF
- VarCNN
- GraphDApp
- CTDNE

### 9.3 相关任务

- website fingerprinting on Tor
- DApp traffic analysis
- traffic classification with GNN

### 9.4 可更新的综述页面

- website fingerprinting survey
- GNN for traffic analysis survey

### 9.5 可加入的对比表

- WF techniques comparison on new datasets
- GNN vs CNN for website fingerprinting

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| DApp 比传统网站更难被指纹识别 | TikTok 精度下降 25% | §V-A.5 |
| Reload 流量降低现有方法精度 | AWF 下降 6%，TikTok 下降 14% | §V-A.6 |
| GNN 在 reload 场景下表现最好 | GFNC Top-1 62.01%，超越所有方法 | §V-A.6 |
| Tor 使 DApp 更难被指纹识别 | 6/7 方法在 Tor DApp 上精度下降 | §V-A.5 |
| 时序信息对 WF 性能至关重要 | 使用时序的方法（TikTok/GFNC）表现更好 | §V-A.3 |
| DF 在新数据集上表现差 | Top-1 仅 8% | Table I |

---

## 11. 原始资料链接

- PDF：`../00-inbox/PDFs/2023-TIFS-Exploring_Uncharted_Waters_of_Website_Fingerprinting.pdf`
- MinerU Markdown：`../02-parsed-markdown/2023-TIFS-Exploring_Uncharted_Waters_of_Website_Fingerprinting.md`

---

## 12. 后续问题

- 如何解决 GFGC 的可扩展性问题？
- 如何改进 GNN 在 Tor DApp 场景下的表现？
- 有哪些其他用户行为（如 referral traffic、click-through traffic）会影响 WF？
- 如何应对 Tor 的 connection-level padding 对 WF 的影响？

---

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

从网站指纹识别研究中两个被忽视的场景（DApp 和 reload 流量）出发，提出两种基于 GNN 的新型 WF 技术，通过收集 5 个新数据集进行系统评估，发现 GNN 在非标准场景下具有优势，但传统方法在某些场景下仍然更强。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 展示核心发现和贡献 | 全文预告 | - |
| Introduction | 从三个研究问题出发 | 问题引入 | DApp 和 reload 的研究空白 |
| Background | 系统梳理 WF 和 GNN 相关工作 | 文献定位 | Shen et al. 的局限 |
| Data Collection | 详细介绍 5 个数据集 | 实验基础 | 手动数据收集方法 |
| Methodology | 介绍 GFNC 和 GFGC | 方法核心 | 图表示的设计 |
| Evaluation | 多维度实验评估 | 验证假设 | GNN 的优势和劣势 |
| Discussion | 深入讨论局限和未来方向 | 反思总结 | GFGC 的可扩展性问题 |
| Conclusion | 总结贡献 | 收束全文 | - |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 场景缺失 | DApp 和 reload 流量的 WF 研究空白 | 文献综述 | §I |
| 评估不足 | Shen et al. 未用 Tor 流量和强 baseline | 方法论对比 | §I |
| 数据缺失 | 缺乏 DApp 和 reload 的公开数据集 | 数据集收集 | §III |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| Closed-world (5 数据集) | 全面评估 7 种方法 | 核心性能对比 |
| Combined 数据集 | 评估动态用户行为 | 接近真实场景 |
| Open-world | 评估实际部署可行性 | 实用性验证 |
| 特征重要性分析 | 理解 GFNC 的工作机制 | 可解释性分析 |
| 可扩展性分析 | 评估 GFGC 的局限 | 讨论改进方向 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 从三个研究问题出发 | 问题驱动的研究框架 |
| Gap 提出方式 | 识别两个被忽视的场景 + 方法论局限 | 场景 + 方法双线 Gap |
| 方法论证逻辑 | 两种 GNN 方法分别设计和评估 | 多方法并行对比 |
| 实验组织逻辑 | 5 个场景 × 7 种方法的全面矩阵 | 系统性的实验设计 |
| 局限性讨论方式 | 详细讨论可扩展性和数据集局限 | 坦诚且有建设性 |
| 最值得借鉴的一句话/一段结构 | "GNN-based techniques surpass the performance of state-of-the-art WF techniques when reload traffic is used" | 用条件限定的方式陈述贡献 |

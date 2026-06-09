---
type: paper
title_original: "Flow Correlation Attacks on Tor Onion Service Sessions with Sliding Subset Sum"
title_cn: "基于滑动子集和的 Tor Onion Service 会话流量关联攻击"
authors:
  - Daniela Lopes
  - Jin-Dong Dong
  - Pedro Medeiros
  - Daniel Castro
  - Diogo Barradas
  - Bernardo Portela
  - Joao Vinagre
  - Bernardo Ferreira
  - Nicolas Christin
  - Nuno Santos
year: 2024
venue: NDSS
doi: unknown
url: unknown
pdf: "../00-inbox/PDFs/2024-NDSS-Flow_Correlation_Attacks_on_Tor_Onion_Service_Sessions_with_Sliding_Subset_Sum.pdf"
mineru_md: "../02-parsed-markdown/2024-NDSS-Flow_Correlation_Attacks_on_Tor_Onion_Service_Sessions_with_Sliding_Subset_Sum.md"
status: processed
reading_level: L2
research_area:
  - flow correlation
  - Tor anonymity
  - onion service deanonymization
  - traffic analysis
task:
  - flow correlation attack
  - onion service session deanonymization
  - circuit fingerprinting
method:
  - Sliding Subset Sum (SUMo)
  - XGBoost (filtering phase)
  - gradient boosting
  - Bayesian optimization
dataset:
  - OSTrain
  - OSValidate
  - OSTest
code: "https://github.com/danielaLopes/sumo"
relevance: high
created: 2026-06-09
updated: 2026-06-09
---

# Flow Correlation Attacks on Tor Onion Service Sessions with Sliding Subset Sum

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Flow Correlation Attacks on Tor Onion Service Sessions with Sliding Subset Sum |
| 中文标题 | 基于滑动子集和的 Tor Onion Service 会话流量关联攻击 |
| 作者 | Daniela Lopes, Jin-Dong Dong, Pedro Medeiros, Daniel Castro, Diogo Barradas, Bernardo Portela, Joao Vinagre, Bernardo Ferreira, Nicolas Christin, Nuno Santos |
| 年份 | 2024 |
| 会议/期刊 | NDSS |
| 研究方向 | 流量关联攻击、Tor 匿名性、onion service 去匿名化 |
| 任务类型 | 流量关联（flow correlation）、onion service 会话去匿名化 |
| 方法关键词 | Sliding Subset Sum (SUMo)、XGBoost、梯度提升、贝叶斯优化、滑动窗口 |
| 数据集 | OSTrain、OSValidate、OSTest（自建，14 个地理位置，48 个 onion service VM） |
| 是否开源 | 是（https://github.com/danielaLopes/sumo） |
| PDF | `../00-inbox/PDFs/2024-NDSS-Flow_Correlation_Attacks_on_Tor_Onion_Service_Sessions_with_Sliding_Subset_Sum.pdf` |
| MinerU Markdown | `../02-parsed-markdown/2024-NDSS-Flow_Correlation_Attacks_on_Tor_Onion_Service_Sessions_with_Sliding_Subset_Sum.md` |

---

## 1. 一句话总结

> 提出 SUMo 流量关联攻击，通过滑动子集和算法和两级过滤流水线，以 99.5% 精确率和 89.6% 召回率去匿名化 Tor onion service 会话，吞吐量比 DeepCoFFEA 高两个数量级。

---

## 2. 摘要翻译

### 2.1 摘要原文

Tor is one of the most popular anonymity networks in use today. Its ability to defend against flow correlation attacks is essential for providing strong anonymity guarantees. However, the feasibility of flow correlation attacks against Tor onion services (formerly known as "hidden services") has remained an open challenge. In this paper, we present an effective flow correlation attack that can deanonymize onion service sessions in the Tor network. Our attack is based on a novel distributed technique named Sliding Subset Sum (SUMo), which can be deployed by a group of colluding ISPs worldwide in a federated fashion. These ISPs collect Tor traffic at multiple vantage points in the network, and analyze it through a pipelined architecture based on machine learning classifiers and a novel similarity function based on the classic subset sum decision problem. These classifiers enable SUMo to deanonymize onion service sessions effectively and efficiently. We also analyze possible countermeasures that the Tor community can adopt to hinder the efficacy of these attacks.

### 2.2 摘要中文翻译

Tor 是当今最流行的匿名网络之一。其抵御流量关联攻击的能力对于提供强匿名性保证至关重要。然而，针对 Tor onion service（前称"hidden services"）的流量关联攻击的可行性一直是一个开放性挑战。本文提出了一种有效的流量关联攻击，可以去匿名化 Tor 网络中的 onion service 会话。该攻击基于一种名为 Sliding Subset Sum (SUMo) 的新型分布式技术，可以由全球一组串通的 ISP 以联邦方式部署。这些 ISP 在网络中的多个有利位置收集 Tor 流量，并通过基于机器学习分类器和基于经典子集和判定问题的新型相似性函数的流水线架构进行分析。这些分类器使 SUMo 能够有效且高效地去匿名化 onion service 会话。我们还分析了 Tor 社区可以采取的可能对策来阻碍这些攻击的效果。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

现有流量关联攻击（DeepCorr、DeepCoFFEA）主要针对 Tor 到 clearnet 的流量，无法直接应用于 onion service 流量。Onion service 流量具有独特的特征（多路复用、固定大小 cell），且存在 base rate fallacy 问题。需要专门针对 onion service 的流量关联方法。

### 3.2 现有方法的痛点和不足

- DeepCorr/DeepCoFFEA 在 onion service 流量上性能下降
- Onion service 的多路复用（多个客户端共享同一 TLS 连接）使关联困难
- Base rate fallacy：onion service 流量远少于 clearnet 流量
- Kwon et al. 的 circuit fingerprinting 因 Tor padding 而失效
- 深度学习方法计算开销大，需要频繁模型更新

### 3.3 论文的研究假设或核心直觉

Onion service 流量的包体积模式可以用子集和问题建模：客户端接收的总字节数应该与 onion service 发送的某个子集的包大小之和匹配。滑动窗口可以处理网络延迟和包重排序带来的扰动。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | Onion service 使用增长，但流量关联研究主要关注 clearnet | §I, §II |
| 痛点提炼 | 现有方法在 onion service 上失效，base rate fallacy 未被解决 | §II-C, §II-D |
| 问题转化 | 如何在 onion service 流量中实现有效的端到端流量关联？ | §II-E |
| 文献定位 | 现有流量关联方法未专门针对 onion service，circuit fingerprinting 因 padding 失效 | §II-D |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 子集和问题可以建模 onion service 流量的体积关联 | 包体积在多跳网络中保持可关联性 | 实验验证 |
| 辅助假设 1 | 基于梯度提升的过滤器可以绕过 Tor padding | padding 不消除客户端/服务端的统计差异 | 实验验证 |
| 辅助假设 2 | SUMo 比深度学习方法更高效 | 子集和计算复杂度低于神经网络 | 性能对比 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | 完美过滤下 99.64% 精确率和 99.65% 召回率 | §V-A |
| 辅助假设 1 | 支撑 | 源分离 AP=1，目标分离 AP=0.99 | §V-B |
| 辅助假设 2 | 支撑 | 吞吐量比 DeepCoFFEA 高约 100 倍 | §V-D |

---

## 4. 方法设计

### 4.1 方法整体流程

SUMo 流水线分为三个阶段：

**过滤阶段（在线，在本地探针上）**：
1. 源分离：区分客户端流量和 onion service 流量
2. 目标分离：从客户端流量中过滤掉访问 clearnet 的流量

**匹配阶段（在线，在关联器上）**：
3. 时间重叠配对：将时间重叠的流配对
4. 桶化：将每个流对的包按时间分桶
5. 滑动子集和：在滑动窗口上计算子集和相似性分数
6. 关联决策：基于阈值判断流对是否关联

**训练阶段（离线）**：
- 训练过滤阶段的 XGBoost 分类器
- 优化匹配阶段的超参数

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | 网络流量 | 包嗅探 + 特征提取 | 流特征向量 | 数据准备 |
| Step 2 | 流特征 | XGBoost 源分离 | 客户端流 / OS 流 | 过滤 |
| Step 3 | 客户端流 | XGBoost 目标分离 | clearnet 流 / onion 流 | 过滤 |
| Step 4 | 客户端流 + OS 流 | 时间重叠配对 | 流对候选 | 配对 |
| Step 5 | 流对 | 桶化（0.5s/桶） | 桶化流对 | 预处理 |
| Step 6 | 桶化流对 | 滑动子集和计算 | 相似性分数向量 | 关联 |
| Step 7 | 分数向量 | 后处理 + 阈值判断 | 关联/非关联 | 决策 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 源分离器 | 区分客户端和 OS 流量 | 流特征 | 客户端/OS 标签 | 输入到目标分离 |
| 目标分离器 | 区分 clearnet 和 onion 流量 | 客户端流特征 | clearnet/onion 标签 | 输入到匹配器 |
| 流对配对器 | 配对时间重叠的流 | 客户端流 + OS 流 | 流对列表 | 输入到桶化器 |
| 桶化器 | 按时间分桶 | 流对 | 桶化流对 | 输入到子集和 |
| 滑动子集和 | 计算体积相似性 | 桶化流对 | 分数向量 | 输入到决策器 |
| 决策器 | 判断关联性 | 分数向量 + 阈值 | 关联结果 | 最终输出 |

### 4.4 公式、算法和机制解释

- **子集和问题**：给定正整数集合 $A = \{a_i\}$ 和正整数 M，寻找 A 的子集使其元素之和等于 M。在 SUMo 中，A 为 OS 发送的包大小，M 为客户端接收的总字节数。
- **松弛子集和**：$\sum_{i=1}^n a_i x_i \in [M-\Delta, M+\Delta]$，允许 $\Delta$ 的误差范围。
- **分数后处理**：连续窗口同分时增加权重，$scores[i] = scores[i] + K \times c(1, i-1)$（K=0.1）。
- **最终分数**：所有窗口分数的平均值。
- **关联决策**：选择最高分的候选流对，若超过阈值则判定为关联。

### 4.5 方法优势

- 首个专门针对 onion service 的流量关联攻击
- 精确率高达 99.5%，有效避免 base rate fallacy
- 吞吐量比 DeepCoFFEA 高两个数量级（~153,000 vs ~1,639 对/秒）
- 训练时间短（6 秒 vs DeepCoFFEA 的一天以上）
- 可绕过 Tor 的 circuit padding 防御
- 开源且提供大规模数据集

### 4.6 方法不足

- 需要多个 ISP 合谋，覆盖范围受限
- 短会话（<6 分钟）的精确率较低
- 热门 onion service 之间容易产生误分类
- 部分覆盖场景下性能下降
- 数据集未覆盖多 tab 场景和多媒体内容
- 未考虑主动流量操纵攻击

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

DeepCorr/DeepCoFFEA 使用深度学习进行流量关联，针对 clearnet 流量设计。SUMo 使用组合优化方法（子集和），专门针对 onion service 流量的体积模式，并通过两级过滤解决 base rate fallacy。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 滑动子集和算法 | 将流量关联转化为子集和问题 | 高 | 是 |
| 绕过 padding 的过滤器 | 基于梯度提升的 circuit fingerprinting | 高 | 是 |
| 分布式流水线架构 | 探针过滤 + 关联器匹配 | 中 | 是 |
| 大规模数据集 | 14 个地理位置，48 个 onion service | 中 | 是 |
| GPU 加速 | OpenCL 并行化子集和计算 | 中 | 是 |

### 5.3 适用场景

- ISP 级别的 Tor 流量监控
- Onion service 去匿名化
- 执法机构的暗网调查
- Tor 匿名性评估

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| DeepCorr | 高精度（clearnet） | 计算开销大，onion service 上失效 | 100x 吞吐量提升 |
| DeepCoFFEA | 较快（clearnet） | 在 onion service 上精度低 | 专门优化 onion service |
| Circuit fingerprinting (Kwon) | 可区分客户端/OS | 因 Tor padding 失效 | 绕过 padding |
| Website fingerprinting | 仅需单端监控 | 无法获取 IP 地址 | 端到端去匿名化 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- 3 个数据集：OSTrain、OSValidate、OSTest
- 14 个地理位置（欧洲、美洲、亚洲、澳洲）
- 48 个 onion service VM，60 个客户端 VM
- 评价指标：Precision、Recall、F1、Throughput
- 对比 DeepCoFFEA

### 6.2 数据集

| 数据集 | Onion 会话 | Clearnet 会话 | Onion 请求 | Clearnet 请求 |
|---|---|---|---|---|
| OSTrain | 14,654 | 8,697 | 71,679 | 39,400 |
| OSValidate | 7,492 | 9,284 | 29,845 | 41,715 |
| OSTest | 7,046 | 7,922 | 28,224 | 35,725 |

### 6.3 Baseline

- DeepCoFFEA（state-of-the-art 流量关联攻击）

### 6.4 评价指标

- Precision（精确率）
- Recall（召回率）
- Throughput（关联吞吐量，对/秒）
- GPU 内存使用

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| 完美过滤，任意时长 | Precision/Recall | 99.64% / 99.65% | - | - | 理想上限 |
| 完美过滤，>6min | Precision/Recall | 100% / 100% | - | - | 长会话完美 |
| 完整流水线，任意时长 | Precision/Recall | 99.5% / 89.6% | - | - | 实际部署 |
| 完整流水线，>6min | Precision/Recall | 99.76% / 92.07% | - | - | 实际部署 |
| Onion service 流量 | Throughput | ~153,000 对/秒 | ~1,639 对/秒 (DeepCoFFEA) | ~100x | 性能优势 |
| GPU 内存 | Memory | 450MB (1.1M 对) | ~2,100MB (60K 对) | ~5x 更少 | 内存效率 |

### 6.6 优势最明显的场景

- 长会话（>6 分钟）：精确率和召回率均接近 100%
- 全覆盖场景：性能最佳
- 高并发场景：即使 onion service 有 10+ 并发会话仍可正确关联
- 大规模部署：吞吐量和内存效率远超 DeepCoFFEA

### 6.7 局限性

- 短会话（<6 分钟）产生大部分误报
- 热门 onion service 之间容易混淆
- 部分覆盖场景下精确率下降
- 需要多个 ISP 合谋
- 未覆盖多 tab 场景
- 未考虑洋葱服务的多媒体内容

---

## 7. 学习与应用

### 7.1 是否开源？

是（https://github.com/danielaLopes/sumo）

### 7.2 复现关键步骤

1. 在 Google Cloud 上部署 48 个 onion service VM 和 60 个客户端 VM
2. 使用 Selenium + tbselenium 自动化浏览
3. 使用 scapy 提取流量特征
4. 训练 XGBoost 分类器（源分离 + 目标分离）
5. 实现 C++ 滑动子集和算法（OpenCL GPU 加速）
6. 使用 hyperopt 进行贝叶斯优化

### 7.3 关键超参数、预处理和训练细节

**过滤阶段（XGBoost）**：
- 学习率：0.1
- 最大深度：3（源分离）/ 15（目标分离）
- 树数量：800
- 训练时间：~6 秒

**匹配阶段**：
- epochSize：5 秒
- epochTolerance：1
- tsInterval：100ms（完美过滤）/ 200ms（不完美过滤）
- bktsPerWindow：4（完美）/ 6（不完美）
- bktsOverlap：2（完美）/ 3（不完美）
- Delta：100（完美）/ 60（不完美）

### 7.4 能否迁移到其他任务？

可以。SUMo 的方法可以迁移到：
- Tor 到 clearnet 的流量关联
- VPN 流量关联
- 其他匿名网络的流量关联
- 网络入侵检测中的流量关联

### 7.5 对我的研究有什么启发？

- 组合优化方法可以替代深度学习进行流量关联
- 两级过滤是解决 base rate fallacy 的有效方法
- 子集和问题可以建模流量的体积关联
- GPU 并行化可以显著提升流量关联的吞吐量
- 数据集的地理分布对评估流量关联攻击至关重要

---

## 8. 总结

### 8.1 核心思想

> 滑动子集和 + 两级过滤 = 高效精准的 onion service 流量关联

### 8.2 速记版 Pipeline

1. 探针提取流量特征
2. XGBoost 源分离（客户端 vs OS）
3. XGBoost 目标分离（clearnet vs onion）
4. 时间重叠配对 + 桶化
5. 滑动子集和计算相似性分数
6. 阈值判断关联结果

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[flow correlation attack]]
- [[Tor onion service]]
- [[subset sum problem]]
- [[base rate fallacy]]
- [[circuit fingerprinting]]

### 9.2 相关方法

- [[DeepCorr]]
- [[DeepCoFFEA]]
- [[Sliding Subset Sum (SUMo)]]
- [[XGBoost]]
- [[Bayesian optimization]]

### 9.3 相关任务

- [[Tor deanonymization]]
- [[onion service traffic analysis]]
- [[ISP-level traffic monitoring]]

### 9.4 可更新的综述页面

- [[flow correlation attacks survey]]
- [[Tor anonymity analysis survey]]

### 9.5 可加入的对比表

- [[flow correlation methods comparison]]
- [[DeepCoFFEA vs SUMo performance]]

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| SUMo 可以高精度关联 onion service 会话 | 完美过滤下 99.64% 精确率和 99.65% 召回率 | §V-A |
| 短会话产生大部分误报 | 误报全部在 <6 分钟会话中 | §V-A, Figure 7 |
| 热门 onion service 容易混淆 | 混淆矩阵显示热门 OS 间误分类多 | §V-A, Figure 9 |
| DeepCoFFEA 在 onion service 上失效 | ROC 曲线接近随机 | §V-C, Figure 14 |
| SUMo 吞吐量高两个数量级 | ~153,000 vs ~1,639 对/秒 | §V-D, Figure 15 |
| 过滤器可绕过 Tor padding | 源分离 AP=1，目标分离 AP=0.99 | §V-B |
| 6 个 AS 合谋可监控 50% guard 流量 | Guard 概率分析 | §V-E |
| 德国单一国家有 10.15% 的去匿名化概率 | 40,000 会话实验 | §V-E |

---

## 11. 原始资料链接

- PDF：`../00-inbox/PDFs/2024-NDSS-Flow_Correlation_Attacks_on_Tor_Onion_Service_Sessions_with_Sliding_Subset_Sum.pdf`
- MinerU Markdown：`../02-parsed-markdown/2024-NDSS-Flow_Correlation_Attacks_on_Tor_Onion_Service_Sessions_with_Sliding_Subset_Sum.md`
- 代码：https://github.com/danielaLopes/sumo
- 数据集：OSTrain (10.5281/zenodo.8362616), OSValidate (10.5281/zenodo.8360991), OSTest (10.5281/zenodo.8359342)

---

## 12. 后续问题

- 如何在部分覆盖场景下提高精确率？
- 如何处理多 tab 浏览场景？
- Onion service 的多媒体内容是否会影响关联效果？
- Tor 社区可以采取哪些更有效的防御措施？
- 如何将 SUMo 扩展到更长时间窗口的关联？

---

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

从 Tor onion service 流量关联攻击的开放性挑战出发，分析现有方法在 onion service 上的三个核心难题（流量分类、性能维护、base rate fallacy），提出基于子集和的 SUMo 方法，通过两级过滤和滑动窗口机制解决了这些难题，在精度和效率上均超越现有方法。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 展示核心贡献和关键结果 | 全文预告 | - |
| Introduction | 从 onion service 的重要性和攻击挑战出发 | 问题引入 | 三个核心难题 |
| Motivation | 详细分析现有方法的不足 | 问题深化 | DeepCorr/DeepCoFFEA 的局限 |
| SUMo Attack | 详细介绍方法设计 | 方法核心 | 子集和的创新应用 |
| Evaluation | 多维度实验评估 | 验证假设 | 高精度和高效率 |
| Countermeasures | 分析可能的防御措施 | 影响评估 | 攻防博弈讨论 |
| Related Work | 系统梳理相关工作 | 文献定位 | 与现有方法的差异 |
| Conclusion | 总结贡献 | 收束全文 | - |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 场景缺失 | Onion service 流量关联未被研究 | 文献综述 | §I, §II-C |
| 性能瓶颈 | 深度学习方法计算开销大 | 方法论对比 | §II-C |
| 理论缺陷 | Base rate fallacy 未被解决 | 问题分析 | §II-D |
| 评估不足 | 现有方法未在 onion service 上评估 | 实验对比 | §V-C |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 完美过滤实验 | 验证匹配阶段的理论上限 | 核心算法验证 |
| 过滤阶段评估 | 验证绕过 padding 的能力 | 关键组件验证 |
| 完整流水线评估 | 验证实际部署效果 | 系统级验证 |
| DeepCoFFEA 对比 | 突出本文方法的优势 | 差异化论证 |
| 吞吐量评估 | 验证实际可行性 | 性能验证 |
| 可行性分析 | 评估实际威胁 | 影响评估 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 从 onion service 的重要性和开放性挑战出发 | 强调问题的开放性 |
| Gap 提出方式 | 三个核心难题的系统分析 | 结构化的问题分解 |
| 方法论证逻辑 | 从探索过程（失败的尝试）到最终方案 | 展示迭代设计过程 |
| 实验组织逻辑 | 从理想条件到实际部署的逐步验证 | 渐进式验证 |
| 局限性讨论方式 | 提出 4 种具体对策 | 攻防双向思考 |
| 最值得借鉴的一句话/一段结构 | "our SUMo classifier yields a throughput two orders of magnitude higher than DeepCoFFEA" | 用数量级对比突出优势 |

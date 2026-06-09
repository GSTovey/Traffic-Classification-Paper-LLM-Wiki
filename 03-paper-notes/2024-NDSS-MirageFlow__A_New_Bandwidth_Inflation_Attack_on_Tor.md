---
type: paper
title_original: "MirageFlow: A New Bandwidth Inflation Attack on Tor"
title_cn: "MirageFlow：一种针对 Tor 的新型带宽膨胀攻击"
authors:
  - Christoph Sendner
  - Jasper Stang
  - Alexandra Dmitrienko
  - Raveen Wijewickrama
  - Murtuza Jadliwala
year: 2024
venue: NDSS
doi: unknown
url: https://www.ndss-symposium.org/
pdf: "../00-inbox/PDFs/2024-NDSS-MirageFlow__A_New_Bandwidth_Inflation_Attack_on_Tor.pdf"
mineru_md: "../02-parsed-markdown/2024-NDSS-MirageFlow__A_New_Bandwidth_Inflation_Attack_on_Tor.md"
status: processed
reading_level: L2
research_area:
  - 匿名通信安全
  - Tor 网络攻击
  - 带宽膨胀攻击
task:
  - 带宽膨胀攻击
  - 流量分类（测量流量 vs 用户流量）
  - Tor 网络安全性分析
method:
  - 资源共享集群攻击
  - IP 过滤流量分类
  - ML 流量分类（SA-CNN + SVM）
  - 概率分析（co-measurement 分析）
dataset:
  - 私有 Tor 测试网络（基于 Chutney）
  - Tor 真实网络 bandwidth files（CollecTor）
code: unknown
relevance: medium
created: 2026-06-09
updated: 2026-06-09
---

# MirageFlow: A New Bandwidth Inflation Attack on Tor

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | MirageFlow: A New Bandwidth Inflation Attack on Tor |
| 中文标题 | MirageFlow：一种针对 Tor 的新型带宽膨胀攻击 |
| 作者 | Christoph Sendner, Jasper Stang, Alexandra Dmitrienko, Raveen Wijewickrama, Murtuza Jadliwala |
| 年份 | 2024 |
| 会议/期刊 | NDSS |
| 研究方向 | 匿名通信安全 / Tor 网络攻击 |
| 任务类型 | 带宽膨胀攻击、流量分类、安全性分析 |
| 方法关键词 | 资源共享集群、C-MirageFlow、D-MirageFlow、IP 过滤、SA-CNN 流量分类 |
| 数据集 | 私有 Tor 测试网络（Chutney）、CollecTor bandwidth files（2022年5-7月） |
| 是否开源 | 否 |
| PDF | `00-inbox/PDFs/2024-NDSS-MirageFlow__A_New_Bandwidth_Inflation_Attack_on_Tor.pdf` |
| MinerU Markdown | `02-parsed-markdown/2024-NDSS-MirageFlow__A_New_Bandwidth_Inflation_Attack_on_Tor.md` |

---

## 1. 一句话总结

> 利用 Tor 中继节点间的资源共享机制，攻击者可通过集群化部署将测量带宽膨胀近 n 倍（C-MirageFlow）或 n*N/2 倍（D-MirageFlow），仅需 10 台服务器即可控制 Tor 网络一半流量。

---

## 2. 摘要翻译

### 2.1 摘要原文

The Tor network is the most prominent system for providing anonymous communication to web users, with a daily user base of 2 million users. However, since its inception, it has been constantly targeted by various traffic fingerprinting and correlation attacks aiming at deanonymizing its users. A critical requirement for these attacks is to attract as much user traffic to adversarial relays as possible, which is typically accomplished by means of bandwidth inflation attacks. This paper proposes a new inflation attack vector in Tor, referred to as MirageFlow, which enables inflation of measured bandwidth. The underlying attack technique exploits resource sharing among Tor relay nodes and employs a cluster of attacker-controlled relays with coordinated resource allocation within the cluster to deceive bandwidth measurers into believing that each relay node in the cluster possesses ample resources. We propose two attack variants, C-MirageFlow and D-MirageFlow, and test both versions in a private Tor test network. Our evaluation demonstrates that an attacker can inflate the measured bandwidth by a factor close to n using C-MirageFlow and nearly half n*N using D-MirageFlow, where n is the size of the cluster hosted on one server and N is the number of servers. Furthermore, our theoretical analysis reveals that gaining control over half of the Tor network's traffic can be achieved by employing just 10 dedicated servers with a cluster size of 109 relays running the MirageFlow attack, each with a bandwidth of 100MB/s.

### 2.2 摘要中文翻译

Tor 网络是为用户提供匿名通信的最重要系统，每日用户量达 200 万。然而，自其诞生以来，就不断受到各种流量指纹和关联攻击的威胁，旨在去匿名化其用户。这些攻击的一个关键前提是尽可能多地将用户流量吸引到攻击者控制的中继节点，这通常通过带宽膨胀攻击来实现。本文提出了一种新的 Tor 膨胀攻击向量，称为 MirageFlow，可实现测量带宽的膨胀。其底层攻击技术利用 Tor 中继节点间的资源共享，在攻击者控制的中继集群内进行协调资源分配，使带宽测量器误认为集群中的每个中继节点都拥有充足资源。我们提出两种攻击变体 C-MirageFlow 和 D-MirageFlow，并在私有 Tor 测试网络中进行了测试。评估表明，攻击者可使用 C-MirageFlow 将测量带宽膨胀近 n 倍，使用 D-MirageFlow 膨胀近 n*N/2 倍。理论分析表明，仅需 10 台专用服务器（每台运行 109 个中继节点集群、带宽 100MB/s）即可控制 Tor 网络一半的流量。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

现有的 Tor 带宽膨胀攻击（如虚假带宽自报告、测量期间丢弃用户流量）仅针对单个中继节点。作者发现 Tor 允许甚至鼓励资源共享（同一 IP 可运行多个中继），这为攻击者提供了通过集群化部署进一步放大膨胀效果的新机会。

### 3.2 现有方法的痛点和不足

- 已知的带宽膨胀攻击（如选择性丢弃用户流量）最高可实现 177 倍膨胀，但仅针对单个中继
- 现有方法未考虑多个共址中继共享资源的场景
- Tor 的带宽测量机制使用 2 跳电路，可被轻易区分于用户流量
- 仅 6 个带宽权威负责测量 7000+ 中继，co-measurement 概率低

### 3.3 论文的研究假设或核心直觉

攻击者可通过在集群内部动态分配全部资源给被测量的中继，使每个中继都能声称拥有整个集群的带宽，从而将膨胀因子从单个中继级别提升到集群级别。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | Tor 允许资源共享，同一 IP 可运行多个中继，且社区正在讨论将限制从 2 提升到 32 | §I, §V |
| 痛点提炼 | 已有膨胀攻击未利用资源共享这一特性，存在攻击放大空间 | §I |
| 问题转化 | 如何利用资源共享将带宽膨胀从单中继级别提升到集群级别？ | §III |
| 文献定位 | 该问题在已有文献中被忽视，现有工作聚焦于单中继攻击 | §VIII |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 共享资源的中继集群可使每个中继声称整个集群的带宽 | Tor 资源共享机制 + 测量电路可区分 | 私有 Tor 网络实验 |
| 辅助假设 | 6 个 BA 测量 7000+ 中继时，co-measurement 概率极低 | 统计分析 bandwidth files | 真实 Tor 数据分析 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | C-MirageFlow 膨胀近 n 倍，D-MirageFlow 膨胀近 n*N/2 倍 | §IV-C, §IV-D |
| 辅助假设 | 支撑 | 30 个共址中继的 co-measurement 概率极低；120 个中继时三重 co-measurement 仅 0.15% | §IV-E |

---

## 4. 方法设计

### 4.1 方法整体流程

攻击分为两阶段：(1) 部署攻击者控制的中继集群；(2) 在检测到测量流量时，将集群全部资源动态分配给被测量的中继，同时丢弃或重定向用户流量。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | Tor 中继配置 | 在单台服务器上部署多个共址中继（进程/Docker/VM） | 中继集群 | 构建攻击基础设施 |
| Step 2 | 入站流量 | Traffic Classifier 检测流量类型（基于 BA IP 过滤） | 测量流量/用户流量标签 | 区分测量与用户流量 |
| Step 3 | 测量流量检测结果 | C-MirageFlow: 将全部主机资源分配给被测中继；D-MirageFlow: 将测量流量重定向到专用高性能服务器 | 膨胀的带宽测量值 | 实现带宽膨胀 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Traffic Classifier | 区分测量流量和用户流量 | 入站数据包 | 流量类型标签 | 驱动资源分配决策 |
| 中继集群（C-MirageFlow） | 运行多个共址中继 | 分类后的流量 | 各中继的处理结果 | 共享物理机资源 |
| 虚拟路由器 + 专用服务器（D-MirageFlow） | 路由和分流测量流量 | 分类后的流量 | 重定向到专用服务器 | 集群共享网络链路 |

### 4.4 公式、算法和机制解释

- **膨胀因子（C-MirageFlow）**：接近 n（集群中继数量）
- **膨胀因子（D-MirageFlow）**：接近 n*N/2（n 为每集群中继数，N 为服务器数）
- **Co-measurement 概率分析**：基于真实 Tor bandwidth files 模拟，使用 39 秒中位测量时长，分析不同集群大小下的同时测量概率
- **所需攻击资源估算**：控制 50% 流量需 678 GBit/s 额外带宽，对应 10 台服务器（每台 100MB/s）× 109 个中继/集群

### 4.5 方法优势

- 膨胀因子可叠加于已知攻击之上（如虚假自报告、丢弃用户流量）
- C-MirageFlow 部署简单（仅需进程级配置）
- D-MirageFlow 成本更低（小服务器 + 多 IP + 专用高性能服务器）
- Co-measurement 概率低，攻击效果稳定

### 4.6 方法不足

- 需要控制多台服务器和多个 IP 地址
- D-MirageFlow 存在 VPN/路由开销导致的带宽损耗
- 大集群时 co-measurement 会降低膨胀效率（120 个中继时约 28 个不活跃贡献）
- 未在真实 Tor 网络上验证（仅私有测试网络）

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

MirageFlow 的核心创新在于利用**资源共享**将膨胀从中继级别提升到集群级别。现有方法（如选择性 DoS）仅针对单个中继，而 MirageFlow 可将整个集群的资源集中给被测中继，实现额外的 n 倍放大。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 集群资源共享攻击 | 多个共址中继共享资源，动态分配给被测中继 | 高 | 是（可扩展到其他资源共享系统） |
| C-MirageFlow 变体 | 单机共址中继 + IP 过滤 | 中 | 否（Tor 特定） |
| D-MirageFlow 变体 | 网络级资源共享 + 专用服务器 | 中 | 否（Tor 特定） |
| Co-measurement 分析 | 基于真实数据的概率建模 | 中 | 是（分析方法可迁移） |
| ML 测量流量检测反驳 | 证明 3 跳电路仍可被 ML 区分 | 中 | 是 |

### 5.3 适用场景

- 攻击者希望最大化 Tor 网络流量控制权
- 国家级攻击者拥有充足计算和网络资源
- 需要结合其他去匿名化攻击（如网站指纹、流关联）的场景

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 虚假带宽自报告 | 简单易行 | 容易被 BA 检测 | 可叠加 MirageFlow |
| 选择性 DoS（丢弃用户流量） | 177 倍膨胀 | 仅针对单中继 | MirageFlow 额外放大 n 倍 |
| FlashFlow（替代测量方案） | 更准确 | 仍可被 MirageFlow 利用 | 证明 FlashFlow 不抗 MirageFlow |
| EigenSpeed（P2P 测量） | 无测量流量 | 易受 Sybil 攻击 | MirageFlow 不适用但指出其弱点 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

在私有 Tor 测试网络上进行，基于 Chutney 配置、Vagrant + VirtualBox 虚拟化。主机：32/64 核、126GB RAM、3.2TB NVMe。测试网络包含 3 个 DA、5 个出口中继、2 个客户端、1 个 BA（SBWS）、1 个 Web 服务器。

### 6.2 数据集

- 私有 Tor 测试网络实验数据
- CollecTor 真实 Tor bandwidth files（2022 年 5-7 月，10,440 文件，2,208 测量轮次）
- Artikel10 中继家族（120 个中继，2069.17 MBps 总带宽）

### 6.3 Baseline

- 无 MirageFlow 的基线测量（约 25 MBps）
- 单个恶意中继丢弃用户流量

### 6.4 评价指标

- 膨胀因子（Inflation Factor）
- SBWS 测量带宽值
- Co-measurement 概率
- 所需攻击资源量

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| C-MirageFlow (5 relays) | 膨胀因子 | ~5x | 1x (baseline) | +4x | 每个中继接近全机带宽 |
| D-MirageFlow (3 clusters, 6 relays each) | 总带宽 | 204.43 MBps | 50 MBps | +4x | 18 个中继共享专用服务器 |
| 理论分析 (10 servers, 109 relays each) | 网络控制比例 | 50% | - | - | 仅需 10 台服务器 |
| Co-measurement (30 relays) | 三重 co-measure 概率 | 0.014% | - | - | 极低概率 |

### 6.6 优势最明显的场景

小到中等规模集群（10-30 个中继），膨胀因子接近线性增长，co-measurement 影响极小。

### 6.7 局限性

- 仅在私有测试网络验证，未在真实 Tor 网络测试
- 大集群（120+ 中继）时膨胀效率下降至约 76% 线性增长
- D-MirageFlow 的 VPN/路由开销导致实际带宽低于理论值
- 未考虑更复杂的防御措施

---

## 7. 学习与应用

### 7.1 是否开源？

否

### 7.2 复现关键步骤

1. 使用 Chutney 搭建私有 Tor 测试网络配置
2. 使用 Vagrant + VirtualBox 创建虚拟化环境，配置带宽限制
3. 部署 SBWS 进行带宽测量
4. 部署恶意中继集群（C-MirageFlow 用进程，D-MirageFlow 用 Docker + 虚拟路由器）
5. 实现 IP-based 流量分类器（基于 Netfilter）

### 7.3 关键超参数、预处理和训练细节

- C-MirageFlow：5 个共址中继，每 VM 2 vCPU + 4GB RAM
- D-MirageFlow：3 个集群 VM（各 6 个 Docker 中继），1 个专用服务器（6 vCPU, 12GB RAM, 50MBps）
- SA-CNN：输入 44 字节（IP 20B + TCP 20B + 4B inter-arrival time），滑动窗口 5 包
- 观察窗口：5 包即可分类，推理时间 < 0.5ms

### 7.4 能否迁移到其他任务？

资源共享攻击思路可迁移到其他依赖带宽/资源测量的分布式系统。SA-CNN + SVM 级联模型可用于其他在线流量分类场景。

### 7.5 对我的研究有什么启发？

- 流量分类不仅用于应用识别，还可用于攻击中的流量区分（测量 vs 用户）
- 资源共享是分布式系统中常被忽视的安全隐患
- ML 方法在即使 3 跳电路下也能有效区分流量类型

---

## 8. 总结

### 8.1 核心思想

> 利用 Tor 中继资源共享实现集群级带宽膨胀。

### 8.2 速记版 Pipeline

1. 部署攻击者控制的中继集群（共享物理机或网络链路）
2. Traffic Classifier 实时检测测量流量（基于 BA IP）
3. C-MirageFlow：将全机资源集中给被测中继
4. D-MirageFlow：将测量流量重定向到专用高性能服务器
5. 每个中继声称拥有整个集群/服务器的带宽

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[Tor 匿名网络]]
- [[带宽膨胀攻击]]
- [[带宽测量机制（SBWS, TorFlow）]]
- [[Sybil 攻击]]
- [[流量分类]]

### 9.2 相关方法

- [[SA-CNN 流量分类]]
- [[选择性 DoS 攻击]]
- [[IP 过滤]]

### 9.3 相关任务

- [[Tor 网络安全性分析]]
- [[匿名通信攻击]]
- [[去匿名化攻击]]

### 9.4 可更新的综述页面

- [[Tor 安全性综述]]
- [[带宽膨胀攻击演进]]

### 9.5 可加入的对比表

- [[带宽膨胀攻击方法对比]]

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| C-MirageFlow 膨胀因子接近 n | 5 个共址中继实验，每个中继测量值超过基线 | §IV-C, Fig. 4 |
| D-MirageFlow 膨胀因子接近 n*N/2 | 3 集群 × 6 中继，总带宽 204.43 MBps | §IV-D, Fig. 5 |
| 10 台服务器可控制 50% 流量 | 曲线拟合 + 678 GBit/s 额外带宽需求 | §IV-F |
| 30 个中继时三重 co-measurement 概率 0.014% | 基于真实 bandwidth files 的模拟分析 | §IV-E |
| ML 可在 3 跳电路下区分流量（F1 > 99%） | SA-CNN + SVM 级联模型实验 | §VI-A |
| Tor 社区讨论将每 IP 中继限制提升到 32 | 引用 Tor 社区讨论 | §V |

---

## 11. 原始资料链接

- PDF：`00-inbox/PDFs/2024-NDSS-MirageFlow__A_New_Bandwidth_Inflation_Attack_on_Tor.pdf`
- MinerU Markdown：`02-parsed-markdown/2024-NDSS-MirageFlow__A_New_Bandwidth_Inflation_Attack_on_Tor.md`

---

## 12. 后续问题

- MirageFlow 在真实 Tor 网络中的实际影响如何？
- 是否有更高效的 co-measurement 检测方法？
- 基于用户流量的带宽估计方法（如 EigenSpeed）能否有效防御此类攻击？
- 如何在不增加网络负载的情况下实现抗膨胀的带宽测量？

---

## 13. 写作叙事与故事线分析

> 仅对 CCF A/B 级或用户指定深度分析的论文填写本节。

### 13.1 论文主线故事线

论文从 Tor 带宽膨胀攻击的已有研究出发，指出现有攻击仅利用单中继的资源。作者观察到 Tor 允许资源共享这一被忽视的特性，提出通过集群化部署将膨胀因子从中继级别提升到集群级别，并通过实验和理论分析证明仅 10 台服务器即可控制 Tor 一半流量。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 概述攻击思路和核心结果 | 全文缩影 | - |
| Introduction | 从 Tor 安全威胁引入，定位带宽膨胀攻击的重要性 | 问题背景 | 资源共享被忽视 |
| Background | 介绍 Tor 带宽测量机制 | 技术铺垫 | 2 跳测量电路可区分 |
| Method | 提出两种攻击变体 | 核心贡献 | C-MirageFlow 和 D-MirageFlow |
| Evaluation | 实验验证 + 概率分析 + 资源估算 | 证据支撑 | 10 台服务器控制 50% |
| Additional Insights | 分析真实 Tor 网络中的可疑中继 | 现实意义 | 存在疑似共址中继 |
| Resilience | 证明替代方案也不抗 MirageFlow | 强化贡献 | ML 可区分 3 跳流量 |
| Countermeasures | 提出缓解措施 | 平衡讨论 | 消除测量流量是根本方案 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 场景缺失 | 现有攻击未考虑资源共享场景 | 矛盾证据（Tor 允许资源共享但未被利用） | §I |
| 评估不足 | 替代测量方案对 MirageFlow 的抗性未被评估 | 性能瓶颈分析 | §VI |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| C-MirageFlow 实验 | 直接验证核心假设 | 证明单机集群可实现 n 倍膨胀 |
| D-MirageFlow 实验 | 扩展到网络级攻击 | 证明跨服务器扩展能力 |
| Co-measurement 分析 | 消除潜在质疑 | 证明攻击在大规模下仍有效 |
| 资源估算 | 量化实际威胁 | 证明攻击的现实可行性 |
| ML 流量分类 | 反驳潜在防御 | 证明 3 跳电路不是有效对策 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 从 Tor 安全生态切入，逐步聚焦到带宽膨胀 | 生态定位 -> 聚焦具体问题 |
| Gap 提出方式 | 通过观察资源共享特性指出已有攻击的盲区 | 利用系统设计特性发现攻击面 |
| 方法论证逻辑 | 先提出核心思想，再分两个变体详细设计 | 核心思想 + 变体对比 |
| 实验组织逻辑 | 小规模验证 -> 概率分析 -> 理论推算 -> 防御反驳 | 逐层递进的威胁论证 |
| 局限性讨论方式 | 在 Countermeasures 章节讨论防御和局限 | 攻防平衡的讨论框架 |
---
type: paper
title_original: "CELLSHIFT: RTT-Aware Trace Transduction for Real-World Website Fingerprinting"
title_cn: "CELLSHIFT: 面向真实世界网站指纹攻击的 RTT 感知流量轨迹转换"
authors: ["Rob Jansen"]
year: 2026
venue: "NDSS 2026"
doi: "10.14722/ndss.2026.231004"
url: "https://www.ndss-symposium.org/ndss2026/"
pdf: ""
mineru_md: "02-parsed-markdown/2026-NDSS-CELLSHIFT__RTT-Aware_Trace_Transduction_for_Real-World_Website_Fingerprinting.md"
status: processed
reading_level: L3
research_area: ["network privacy", "website fingerprinting", "Tor anonymity", "traffic analysis"]
task: ["website fingerprinting", "trace transduction", "data augmentation", "vantage point adaptation"]
method: ["RTT estimation", "cell timestamp shifting", "propagation delay/congestion separation", "trace augmentation"]
dataset: ["GTT23", "Cor(entry-exit) correlated dataset (396x80)", "Tor(entry)/Tor(exit) independent dataset (421x40/60)"]
code: "https://github.com/robgjansen/cellshift"
relevance: high
related_papers: []
kb_read_only: true
promoted_to: ""
created: "2026-06-21"
updated: "2026-06-21"
---

# CELLSHIFT: RTT-Aware Trace Transduction for Real-World Website Fingerprinting

> **个人论文笔记** — 本笔记严格隔离于主知识库。
> `kb_read_only: true`：本笔记可链接到主知识库页面，但不会触发主知识库的任何更新。
> 如需晋升至主知识库，须满足 `publication_status: published/accepted` + `my_confidence: high` + 用户主动要求。

---

## 0. 基础信息

| 字段 | 内容 |
|---|---|
| 标题 | CELLSHIFT: RTT-Aware Trace Transduction for Real-World Website Fingerprinting |
| 作者 | Rob Jansen (U.S. Naval Research Laboratory) |
| 年份 | 2026 |
| 目标/发表 venue | NDSS 2026 (Network and Distributed System Security Symposium) |
| 发表状态 | published |
| DOI | 10.14722/ndss.2026.231004 |
| 关键词 | website fingerprinting, trace transduction, RTT estimation, vantage point shift, data augmentation, Tor |
| 数据集 | GTT23 (13M+ genuine Tor traces), Cor(entry-exit) (396x80 correlated), Tor(entry)/Tor(exit) (421x40/60 independent) |
| 代码仓库 | https://github.com/robgjansen/cellshift |
| 研究方向 | [[website-fingerprinting]], [[encrypted-traffic-analysis]], Tor 匿名通信隐私 |
| Confidence | high |
| 晋升状态 | 未晋升 |

---

## 1. 一句话总结

> 提出 CELLSHIFT 框架，通过从 Tor cell trace 元数据中提取 RTT 估计、分离传播延迟与拥塞、重写 cell 时间戳三个核心步骤，将 exit relay 采集的真实流量轨迹转换为 entry 侧视角的轨迹；其两个具体方法 TRACEMOVE（测试集转换）和 TRACEMORPH（训练集增强）在 10 种 WF 分类器上全面超越 Retracer，且效率提升五个数量级（2,875 traces/s/core vs 0.03 traces/s/core）。

---

## 2. 核心贡献

### 2.1 贡献列表

1. **CELLSHIFT 核心库**：提出从 cell trace 元数据中提取多跳 RTT 估计、分离传播延迟（RTT_min）与拥塞（RTT_i - RTT_min）、并根据目标 vantage point 重写 cell 时间戳的通用算法
2. **TRACEMOVE**：将 exit cell trace 转换为 entry 侧 trace 而不修改原始 RTT，用于产生真实测试集；在 6 种距离函数和 10 种 WF 分类器上全面优于 Retracer
3. **TRACEMORPH**：将每条 exit trace 增强为 n 条具有不同传播延迟和拥塞 profile 的 entry trace，用于产生训练集；在 closed-world 中提升 4-14pp（合成数据）和 5-25pp（真实数据），natural-world 中位 recall 从 0.24 提升至 0.66
4. **大规模真实世界评估**：在 GTT23 数据集上评估 1,200 个分类器，证明方法在真实 Tor 流量上的有效性
5. **高效 Rust 实现开源**：处理速率 2,875-18,706 traces/s/core，比 Retracer 快五个数量级

### 2.2 与领域已有工作的关键区别

| 已有工作 | 差异点 | 位置 |
|---|---|---|
| Retracer [Jansen et al., WPES 2024] | Retracer 需要完整 Tor 网络仿真（495 GiB RAM, 29.9hr/115K traces），CELLSHIFT 仅需数学运算（417 MiB, 40s/115K traces）；Retracer 产生的 entry trace 距离真实 entry trace 反而比原始 exit trace 更远 | §IV-B1, §IV-E |
| OnlineWF [Cherubin et al., USENIX 2022] | OnlineWF 直接在 exit trace 上训练，存在 exit→entry 的位置失配问题（准确率下降 5-93%），CELLSHIFT 通过显式位置转换解决 | §I, §IV-C |
| NetAugment [Bahramali et al., CCS 2023] | NetAugment 是位置无关的 burst 级增强，不支持 cell 时间戳，CELLSHIFT 是 RTT 感知的位置级转换+增强 | §IV-A, §IV-C |

---

## 3. 研究连接（Research Connection）

### 3.1 相关概念

- [[website-fingerprinting]] — 本文核心攻击场景，研究 WF 在真实世界条件下的威胁评估
- [[encrypted-traffic-analysis]] — 流量分析的上位概念，WF 是其在 Tor 匿名网络中的特化
- [[survey-website-fingerprinting]] — WF 领域综述，本文的 trace transduction 方法是对该领域评估方法论的重要补充

### 3.2 相关方法

- [[traffic-representation-learning]] — CELLSHIFT 的 cell trace 转换本质上是一种流量表示变换方法，将 exit 侧表示转换为 entry 侧表示

### 3.3 相关任务

- [[website-fingerprinting]] — WF 攻击的训练/测试数据准备

### 3.4 基于哪些已有论文

- Cherubin et al. (USENIX Security 2022) — 提出在 exit relay 上收集 genuine trace 训练 WF 分类器的范式，但未解决 exit→entry 位置失配
- Jansen et al. (WPES 2024) — 提出 Retracer，通过 Shadow 网络仿真进行 exit→entry 转换，是本文的主要 baseline
- Jansen et al. (arXiv 2024) — 发布 GTT23 数据集，包含 13M+ genuine Tor exit traces
- Wang (IEEE S&P 2020) — 提出高精度 open-world WF 和阈值调优策略，本文采用其优化精度评估框架

### 3.5 与已有 Claims 的关系

| 已有 Claim | 本论文的关系 | 位置 |
|---|---|---|
| WF 在合成数据上性能被高估 (Juárez et al., CCS 2014) | 支撑 — 本文使用 genuine traces 进行更现实的评估 | §II-C |
| Exit→entry 位置失配降低分类器准确率 5-93% (Cherubin et al.; Jansen et al.) | 扩展 — 提出 CELLSHIFT 作为解决方案，将失配影响大幅缩小 | §I, §IV-B |
| 数据增强可提升 WF 鲁棒性 (Bahramali et al., CCS 2023) | 扩展 — 提出位置感知的增强方法 TRACEMORPH，效果远超位置无关增强 | §IV-C |

---

## 4. 关键发现与证据

### 4.1 主要实验结果

**TRACEMOVE 测试集评估（Table II） — 训练集: Tor(entry), 测试集: 各方法转换后的 trace**

| WF 分类器 | Exit Trace | Retracer | TRACEMOVE | TRACEMOVE 提升 vs Exit |
|---|---:|---:|---:|---:|
| AWF | 78% | 59% (-19) | 79% (+1) | +1pp |
| DF | 88% | 81% (-7) | 92% (+4) | +4pp |
| Tik-Tok | 87% | 73% (-14) | 91% (+4) | +4pp |
| VarCNN | 89% | 83% (-6) | 92% (+3) | +3pp |
| Triplet FP | 90% | 85% (-5) | 93% (+3) | +3pp |
| BAPM | 86% | 77% (-9) | 89% (+3) | +3pp |
| ARES | 32% | 25% (-7) | 36% (+4) | +4pp |
| Robust FP | 56% | 52% (-4) | 61% (+5) | +5pp |
| NetCLR | 90% | 88% (-2) | 94% (+4) | +4pp |
| TMWF | 83% | 70% (-13) | 90% (+7) | +7pp |

**TRACEMORPH 训练集评估（Table III） — 训练集: 各方法增强后的 trace, 测试集: Tor(entry)**

| 训练方法 | AWF | DF | TT | VarCNN | TF | BAPM | ARES | RF | NetCLR | TMWF |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| OnlineWF | 65% | 79% | 81% | 78% | 79% | 70% | 36% | 37% | 78% | 77% |
| Retracer | 61% | 83% | 82% | 86% | 84% | 80% | 67% | 73% | 87% | 79% |
| **TRACEMORPH** | **79%** | **90%** | **89%** | **91%** | **91%** | **87%** | 61% | 73% | **91%** | **89%** |
| NetAug | 47% | 66% | - | - | 69% | 49% | - | - | 68% | 62% |
| TRACEMOVE+NetAug | 63% | 83% | - | - | 83% | 72% | - | - | 83% | 81% |

**GTT23 Closed-World 评估（Table IV） — 训练集: GTT100 增强, 测试集: TRACEMOVE 转换的 entry trace**

| WF 分类器 | OnlineWF | Retracer | TRACEMORPH | 提升 |
|---|---:|---:|---:|---:|
| AWF | 33% | 31% | **52%** | +19pp |
| DF | 46% | 46% | **70%** | +24pp |
| VarCNN | 36% | 34% | **59%** | +23pp |
| NetCLR | 42% | 40% | **67%** | +25pp |
| TMWF | 42% | 41% | **67%** | +25pp |

**Natural-World 评估（380 个 per-website 分类器）**

| 指标 | OnlineWF | Retracer | TRACEMORPH |
|---|---:|---:|---:|
| Median Recall | 0.22 | 0.24 | **0.66** |
| Median Precision | **0.30** | 0.21 | 0.19 |
| Median Avg Precision | 0.11 | 0.14 | **0.30** |
| Median Optimized Precision | 0.17 | 0.23 | **0.49** |

**效率评估（Table V）**

| 方法 | Traces 数量 | RAM | CPU | 时间 | 速率 |
|---|---:|---|---:|---|---:|
| Retracer | 115,000 | 495 GiB | 36 | 29.9 hr | 0.03/s/core |
| TRACEMOVE | 115,000 | 417 MiB | 1 | 40 sec | 2,875/s/core |
| TRACEMOVE | 13,900,621 | 4.6 GiB | 1 | 27 min | 8,554/s/core |
| TRACEMORPH (n=10) | 139,006,210 | 5.2 GiB | 1 | 2.1 hr | 18,706/s/core |

### 4.2 关键发现

1. **TRACEMOVE 全面优于 Retracer 作为测试集转换方法**：在 6 种距离函数上均取得最低距离，在 10 种 WF 分类器上均取得最高准确率。意外发现：Retracer 产生的 entry trace 距离真实 entry trace 反而比原始 exit trace 更远，原因是 Retracer 仅重放 DATA cell，丢失了控制 cell（如 BEGIN/END）
2. **TRACEMORPH 在 genuine trace 上的增益远大于 synthetic trace**：合成数据上提升 4-14pp，真实数据上提升 5-25pp，说明 genuine trace 中更复杂和多变的模式为 TRACEMORPH 提供了更丰富的增强空间
3. **TRACEMORPH 特别适合高精度攻击者**：虽然 OnlineWF 的中位 precision 更高（0.30 vs 0.19），但 TRACEMORPH 的中位 optimized precision（保持 recall>=0.2 的最高 precision）远超 OnlineWF（0.49 vs 0.17），表明 TRACEMORPH 训练的分类器具有更好的可调性
4. **增强因子 n_aug 的边际递减效应**：当 n_aug > 4 时，DF 分类器准确率趋于饱和（约 92%），表明额外的 trace 变异性收益递减
5. **CELLSHIFT 可作为位置无关增强器的前置步骤**：TRACEMOVE + NetAugment 的组合比单独使用 NetAugment 提升 14-23pp，证明位置转换是增强的有价值前置步骤

---

## 5. 质量与信心评估

### 5.1 当前状态

| 维度 | 状态 | 备注 |
|---|---|---|
| 实验完整性 | 完整 | 覆盖合成数据（correlated + independent）、真实数据（GTT23 closed-world + natural-world）、效率评估，共 1,200+ 分类器 |
| 写作完整性 | 完整 | 结构清晰，方法描述配有完整伪代码，评估设计严谨 |
| 方法创新性 | 高 | 核心 insight（从 cell trace 元数据提取 RTT 进行位置转换）新颖且优雅，避免了 Retracer 的全网络仿真开销 |
| 实验说服力 | 强 | 多数据集、多分类器、多 baseline 的全面评估；距离评估 + 分类器评估 + 效率评估三维度验证 |
| 与已有工作的区分度 | 明确 | 与 Retracer（仿真方法）、OnlineWF（直接训练）、NetAugment（位置无关增强）均有清晰对比 |

### 5.2 需要改进的地方

1. **Retracer baseline 的公平性问题**：论文发现 Retracer 丢失控制 cell 导致 trace 偏短，但未讨论是否可以通过修复 Retracer 的 cell 过滤逻辑来改善其表现
2. **Natural-world 评估中 precision 下降**：TRACEMORPH 的中位 precision（0.19）低于 OnlineWF（0.30），虽然 optimized precision 更高，但在实际部署中低 precision 意味着大量误报
3. **单一 Tor 实现依赖**：RTT 估计依赖 Tor 协议特定的 CONNECTED→DATA 和 DATA→SENDME 交互模式，如果 Tor 协议变更（如 cc_sendme_inc 参数调整），方法可能需要适配
4. **缺乏对 WF 防御的评估**：论文聚焦于 undefended 场景，未评估 CELLSHIFT 转换后的 trace 在面对 WF 防御（如 WTF-PAD, Front, Surakav）时的表现

### 5.3 是否可以考虑提交/晋升？

> [x] 方法论完整
> [x] 实验覆盖足够
> [x] 写作达到可读标准
> [x] 与已有工作区分度明确
> [x] 局限性已诚实讨论

---

## 6. 开放问题与后续计划

### 6.1 本文遗留的问题

- CELLSHIFT 输出的 trace 在面对 WF 防御时的表现如何？论文在结论中提出 TRACEMOVE/TRACEMORPH 输出可作为防御评估的"undefended"基线，但未实际验证
- Retracer 的 cell 过滤 artifact 是否可以修复？修复后 Retracer 与 CELLSHIFT 的差距是否会缩小？
- 在 multi-tab browsing（MTB）和 webpage fingerprinting（WPF）场景下，CELLSHIFT 的 RTT 估计是否仍然有效？
- CELLSHIFT 对 Tor 协议变更的敏感性如何？如果 Tor 修改了拥塞控制参数（如 cc_sendme_inc），方法的鲁棒性如何？

### 6.2 下一步研究方向

- 将 CELLSHIFT 应用于 WF 防御评估：用 TRACEMOVE 将 genuine exit trace 转换为 entry trace，再在其上模拟 WF 防御，评估防御的真实效果
- 探索 CELLSHIFT 在其他匿名网络（如 I2P、Nym）上的适用性
- 结合 CELLSHIFT 与 Swallow 等迁移鲁棒攻击方法，研究位置转换+特征对齐的协同效果

### 6.3 与我的研究主线的关系

> 本文在我的研究轨迹中处于什么位置？（参照 [[my-research-thread]]）
>
> 本文是 [[website-fingerprinting]] 领域中关于真实世界 WF 评估方法论的重要工作。它解决的是 WF 攻击评估中的一个基础设施问题——如何从 exit relay 采集的真实流量产生 entry 侧的训练/测试数据。这与 [[traffic-representation-learning]] 中流量表示变换的研究方向有交叉，但 CELLSHIFT 的变换是在 Tor 协议层面（cell 时间戳）而非特征层面进行的。

---

## 7. [深度分析] 方法设计详解

### 7.1 方法整体流程

CELLSHIFT 框架由三个逻辑独立的模块组成：

```
Exit Cell Trace (t_i, d_i, c_i)
        |
        v
  [CELLSHIFT 核心库]
    |-- RTT 估计: connected_to_data() + data_to_sendme()
    |-- 传播延迟/拥塞分离: prop_delay() = min(RTTs), congestion() = RTT_i - RTT_min
    |-- Cell 时间戳重写: shift(trace, nhops, new_prop, new_cong)
        |
        +---> [TRACEMOVE] -- 保持原始 RTT，仅转换 vantage point --> Entry 测试集
        |
        +---> [TRACEMORPH] -- 使用增强的 RTT 分布 --> Entry 训练集（n 倍扩充）
```

### 7.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| 1. RTT 估计 | Cell trace (t, d, c) | 从 CONNECTED→DATA 和每 31 个 DATA→SENDME 中提取 RTT | RTT 估计序列 [{time, cell_index}] | 获取电路的动态延迟信息 |
| 2. 传播延迟估计 | RTT 序列 | prop_delay = min(RTTs) | 单一延迟值 | 估计电路路径的物理传播延迟 |
| 3. 拥塞估计 | RTT 序列, 传播延迟 | congestion_i = RTT_i - RTT_min | 拥塞时间序列 | 分离拥塞引起的延迟变化 |
| 4. 时间戳重写 | Cell trace, 目标 hop 数, 新传播延迟, 新拥塞 profile | client→exit cell: t_new = t - latency(rtt, 3) + latency(new_rtt, 3-nhops); client←exit cell: t_new = t + latency(new_rtt, nhops) | 转换后的 cell trace | 模拟从目标 vantage point 观察的 trace |
| 5a. TRACEMOVE | 原始 trace | shift(trace, nhops=2, prop=own_prop, cong=own_cong) | 单条 entry trace | 测试集转换 |
| 5b. TRACEMORPH | 原始 trace, n_aug | 先做 1 次 TRACEMOVE; 再做 n-1 次 shift(trace, 2, prop_dist[i], random_cong) | n 条 entry trace | 训练集增强 |

### 7.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| CELLSHIFT 核心库 | RTT 提取、延迟分离、时间戳重写 | Cell trace + 目标参数 | 转换后的 cell trace | 被 TRACEMOVE 和 TRACEMORPH 调用 |
| TRACEMOVE | Exit→Entry 测试集转换 | Exit cell trace 集合 | Entry cell trace 集合（1:1） | 调用 CELLSHIFT，保持原始 RTT |
| TRACEMORPH | Exit→Entry 训练集增强 | Exit cell trace 集合 + n_aug | Entry cell trace 集合（1:n） | 调用 CELLSHIFT，使用增强 RTT |

### 7.4 公式、算法和机制解释

**RTT 估计的两个来源**：

1. **CONNECTED→DATA**（Pseudocode 2）：当客户端通过 Tor 连接到服务器时，exit relay 发送 CONNECTED cell，客户端回复第一个 DATA cell。这个往返时间即为一次 RTT 估计。适用于所有建立过 exit 连接的电路。

2. **DATA→SENDME**（Pseudocode 3）：Tor 拥塞控制协议中，客户端每收到 cc_sendme_inc=31 个 DATA cell 就发送一个 SENDME cell。exit relay 记录每第 31 个 DATA cell 的发送时间，收到 SENDME 时计算 RTT。每约 10 个数据包（约 15KB 应用数据）可产生一次 RTT 估计。

**Cell 时间戳重写公式**（Pseudocode 6）：

对于 client→exit 方向的 cell（d=+1, exit 是接收方）：
- 先减去 exit 到 client 的 3 跳延迟：t_new = t - latency(rtt, 3) = t - RTT/2
- 再加上 client 到目标 vantage point 的延迟：t_new += latency(new_rtt, 3 - nhops)
- 保持单向流内的时间顺序：t_new = max(t_new, prev_recv)

对于 client←exit 方向的 cell（d=-1, exit 是发送方）：
- 加上 exit 到目标 vantage point 的延迟：t_new = t + latency(new_rtt, nhops)
- 保持单向流内的时间顺序：t_new = max(t_new, prev_send)

其中 latency(rtt, nhops) = rtt / 6 * nhops，将 6 跳的 RTT 按比例分配到 nhops。

**关键 insight：传播延迟 vs 拥塞的分离**：
- 传播延迟（propagation delay）：由 relay 路径的物理位置决定，对同一路径稳定。估计为 RTT_min
- 拥塞（congestion）：由 relay 上的其他流量负载决定，高度动态。估计为 RTT_i - RTT_min
- 这种分离使得 TRACEMORPH 可以独立地增强两个维度：通过从数据集的传播延迟分布中均匀采样来模拟不同 relay 路径，通过随机选择其他 trace 的拥塞 profile 来模拟不同的网络负载

---

## 8. [深度分析] 实验详细分析

### 8.1 实验设计和设置

论文采用三层递进的评估策略：

1. **距离评估（§IV-B1）**：使用 correlated entry-exit trace 数据集（Dataset 1, 396x80），直接衡量转换后 trace 与真实 entry trace 的距离
2. **分类器评估（§IV-B2, §IV-C）**：使用 independent entry-exit trace 数据集（Dataset 2, 421x40/60），在 10 种 WF 分类器上评估转换/增强效果
3. **真实世界评估（§IV-D）**：使用 GTT23 数据集（13M+ traces），进行 closed-world（100 网站）和 natural-world（200 网站, 1,200 分类器）评估

### 8.2 数据集详情

| 数据集 | 来源 | 规模 | Entry/Exit | 用途 |
|---|---|---|---|---|
| Dataset 1 (Cor) | 自建，494 URLs x 100 loads，清洗后 31,680 traces | 396x80 correlated | Entry + Exit（同一电路） | 距离评估 |
| Dataset 2 (Tor) | 来自 Retracer 作者，421 URLs | 421x40 entry + 421x60 exit | 独立采集 | 分类器评估 |
| Dataset 3 (GTT100_cw) | GTT23 子集，top 100 网站 | 100x1000 exit traces | Entry 由 TRACEMOVE 生成 | Closed-world 评估 |
| Dataset 4 (GTT_nw) | GTT23 全集，13 周 | 约 3M exit traces | Entry 由 TRACEMOVE 生成 | Natural-world 评估 |

### 8.3 Baseline 选择理由

| Baseline | 选择理由 | 实现来源 |
|---|---|---|
| OnlineWF [Cherubin et al., 2022] | 直接在 exit trace 上训练的最简单方法，代表"不做转换"的 baseline | 自实现 |
| Retracer [Jansen et al., 2024] | 唯一已发表的 exit→entry 转换方法，通过 Shadow 网络仿真实现 | 获取作者代码 |
| NetAugment [Bahramali et al., 2023] | 位置无关的 SOTA 数据增强方法，代表非位置感知的增强策略 | 获取作者代码 |
| TRACEMOVE+NetAugment | 验证 CELLSHIFT 作为其他增强方法前置步骤的价值 | 自实现组合 |

### 8.4 消融实验

论文未设置传统意义上的消融实验，但通过以下方式提供了等效的分析：

- **增强因子 n_aug 的影响（Figure 4）**：从 n_aug=1 到 n_aug=19，观察 DF 分类器准确率变化。TRACEMORPH 在 n_aug=4 时达到约 91.5%，n_aug>=5 后趋于 92%，显示边际递减
- **Retracer 的 artifact 分析（§IV-B2b）**：发现 Retracer 仅重放 DATA cell，丢失 BEGIN/END 等控制 cell，导致 trace 偏短。这个 artifact 在之前的评估中同时影响训练和测试，掩盖了问题
- **TRACEMOVE 作为前置步骤的效果**：TRACEMOVE+NetAugment vs 单独 NetAugment 的对比（Table III），验证位置转换对位置无关增强器的增益

### 8.5 Case Study / 可视化分析

**距离评估的反直觉发现（Table I）**：Retracer entry trace 与真实 entry trace 的距离（Canberra: 175）竟然大于原始 exit trace 的距离（Canberra: 147），意味着 Retracer 的转换不仅没有改善反而恶化了 trace 的真实性。TRACEMOVE 则正确地降低了距离（Canberra: 126）。

**Natural-world 的 precision-recall 权衡（Figure 5）**：TRACEMORPH 训练的分类器呈现"高 recall、低 precision"的特征（中位 recall 0.66 vs precision 0.19），但通过阈值调优（optimized precision at recall>=0.2），TRACEMORPH 的中位 precision 可达 0.49，远超 OnlineWF 的 0.17。这说明 TRACEMORPH 训练的分类器具有更好的概率校准和可调性。

### 8.6 局限性与失败案例

- **Retracer 在 ARES 上优于 TRACEMORPH**：在 Table III 中，ARES 分类器上 Retracer（67%）超过 TRACEMORPH（61%）6pp。ARES 是基于空间-时间分布分析的方法，可能对仿真环境中的 trace 特征更敏感
- **TRACEMORPH 在 precision 上不如 OnlineWF**：Natural-world 中 OnlineWF 的中位 precision（0.30）高于 TRACEMORPH（0.19），说明增强引入的多样性可能导致更多 false positive
- **低频网站性能差**：ARES 和 RF 在 GTT23 上的准确率仅 17% 和 16%，远低于其他分类器，可能是因为这些方法对数据量更敏感

---

## 9. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| Exit→entry 位置失配降低 WF 准确率 | Table II: Retracer 测试时所有分类器准确率均低于 exit trace | §IV-B2 |
| TRACEMOVE 产生的 trace 比 Retracer 更接近真实 entry trace | Table I: 6 种距离函数上 TRACEMOVE 均最优 | §IV-B1 |
| TRACEMORPH 在 genuine trace 上增益大于 synthetic trace | Table III (synthetic: 4-14pp) vs Table IV (genuine: 5-25pp) | §IV-C, §IV-D1 |
| TRACEMORPH 训练的分类器更适合高精度调优 | Figure 5: optimized precision 0.49 vs 0.17 (OnlineWF) | §IV-D2 |
| CELLSHIFT 效率比 Retracer 高五个数量级 | Table V: 2,875/s/core vs 0.03/s/core | §IV-E |
| Retracer 存在控制 cell 丢失 artifact | §IV-B2b: Retracer 仅重放 DATA cell，导致 trace 偏短 | §IV-B2b |
| 增强因子 n_aug > 4 后边际递减 | Figure 4: DF 准确率在 n_aug>=5 后趋于 92% | §IV-C2 |

---

## 10. 学习与应用

### 10.1 是否开源？

是。Rust 实现已开源：https://github.com/robgjansen/cellshift。Dataset 1 发布于 Zenodo: https://doi.org/10.5281/zenodo.15863906。

### 10.2 复现关键步骤

1. **环境搭建**：安装 Rust 编译器、HDF5 库、ZSTD 库，或使用提供的 Dockerfile
2. **数据准备**：下载 Dataset 1 (tbb_exit.hdf5) 或准备自己的 cell trace 数据（HDF5 格式）
3. **TRACEMOVE 执行**：`cellshift move tbb_exit.hdf5 cellshift_entry_tracemove.hdf5`
4. **TRACEMORPH 执行**：`cellshift morph tbb_exit.hdf5 cellshift_entry_tracemorph4.hdf5 4`（n_aug=4）
5. **WF 分类器训练**：使用 WFLib 或自实现的分类器在 TRACEMORPH 输出上训练，在 TRACEMOVE 输出上测试

### 10.3 关键超参数

| 参数 | 值/说明 |
|---|---|
| cc_sendme_inc | 31（Tor 拥塞控制共识参数，2022 年起固定） |
| Cell trace 长度 N | 5,000（零填充至固定长度） |
| 目标 hop 数 (entry) | 2（entry↔exit 距离） |
| 目标 hop 数 (ISP) | 2.5 |
| 目标 hop 数 (client) | 3 |
| n_aug (增强因子) | 默认 4，实验范围 1-19 |
| 训练轮数 | 100 epochs (Dataset 2), 30 epochs (GTT23) |
| 分类器库 | WFLib (Deng et al., 2024) |

### 10.4 对 WF 研究的意义

**对攻击者**：
- 可利用 exit relay 收集的 genuine trace 产生高质量的 entry 侧训练数据，无需进行昂贵的网络仿真
- TRACEMORPH 使分类器对 relay 路径选择和网络拥塞等非网站相关因素更具鲁棒性
- 高 recall + 可调 precision 的特性使攻击者可根据实际需求调整误报率

**对防御者**：
- TRACEMOVE 可用于在 genuine trace 上模拟防御效果，比在合成数据上评估更真实
- CELLSHIFT 输出可作为"undefended entry trace"基线，在其上叠加防御后评估真实安全性
- 研究应关注统计级别（而非包级别）的流量特征泄露

**对 WF 评估方法论**：
- 本文确立了 CELLSHIFT/TRACEMOVE 作为从 genuine exit trace 产生 entry 测试集的标准方法
- Retracer 不应再被用作测试集转换方法（其 trace 比原始 exit trace 更远离真实 entry trace）
- 未来 WF 研究应采用 genuine trace + CELLSHIFT 的评估范式

### 10.5 能否迁移到其他任务？

- **WF 防御评估**：用 TRACEMOVE 将 genuine exit trace 转换为 entry trace，在其上模拟防御并评估
- **其他匿名网络**：CELLSHIFT 的 RTT 估计依赖 Tor 协议特定的 cell 交互，不能直接用于 I2P/Nym，但"从元数据提取延迟信息进行位置转换"的思路可推广
- **加密流量分析中的 vantage point 适应**：不同网络位置（ISP、CDN、目标服务器）观察到的加密流量模式可能不同，CELLSHIFT 的延迟分离思想可启发类似的位置适应方法
- **网络仿真加速**：CELLSHIFT 作为 Retracer 的轻量替代，可用于需要大规模 trace 转换的网络仿真场景

---

## 11. 总结

### 11.1 核心思想（不超过20字）

从 cell trace 元数据提取 RTT，用数学运算替代网络仿真进行 vantage point 转换。

### 11.2 速记版 Pipeline（3-5步）

1. 从 exit cell trace 的 CONNECTED→DATA 和 DATA→SENDME 交互中提取 RTT 估计序列
2. 分离传播延迟（RTT_min）和拥塞（RTT_i - RTT_min）
3. 用 shift() 函数重写 cell 时间戳，模拟从 entry vantage point 观察
4. TRACEMOVE：保持原始 RTT，1:1 转换（测试集）；TRACEMORPH：使用增强 RTT，1:n 增强（训练集）
5. 在转换/增强后的 trace 上训练和测试 WF 分类器

### 11.3 一句话评价

CELLSHIFT 是 WF 领域的方法论基础设施贡献——它用优雅的数学方法解决了 genuine trace 的 vantage point 适应问题，效率提升五个数量级，使得大规模真实世界 WF 评估变得可行。

---

## 12. 原始资料链接

- PDF: https://dx.doi.org/10.14722/ndss.2026.231004
- MinerU Markdown: 02-parsed-markdown/2026-NDSS-CELLSHIFT__RTT-Aware_Trace_Transduction_for_Real-World_Website_Fingerprinting.md
- 代码仓库: https://github.com/robgjansen/cellshift
- 补充材料/数据集: https://doi.org/10.5281/zenodo.15863906 (Dataset 1 + Rust 实现)
- 作者单位: U.S. Naval Research Laboratory
- 项目资助: Office of Naval Research (ONR)

---

## 13. 后续问题

1. **Retracer 的修复可能性**：Retracer 丢失控制 cell 的 artifact 是否可以修复？修复后与 CELLSHIFT 的差距是否会缩小？
2. **WF 防御评估**：CELLSHIFT 输出的 entry trace 上叠加 WF 防御后，防御效果的评估结果如何？与在合成数据上评估有何差异？
3. **Tor 协议变更的敏感性**：如果 Tor 修改 cc_sendme_inc 参数或引入新的拥塞控制机制，CELLSHIFT 的 RTT 估计是否需要重新校准？
4. **Multi-tab 和 Webpage Fingerprinting**：CELLSHIFT 的 RTT 估计在多标签浏览和页面级指纹场景下是否仍然有效？同一电路的多条 stream 可能导致 RTT 估计混淆
5. **自适应防御**：如果防御者知道攻击者使用 CELLSHIFT，能否设计针对性防御（如在 RTT 模式中注入噪声）？
6. **与其他增强方法的组合**：TRACEMORPH + GAN-based augmentation 或 TRACEMORPH + CIF (Swallow) 的组合效果如何？
7. **GTT23 数据集的持续更新**：GTT23 是 2023 年的数据集，Tor 网络和网站内容已发生变化，是否需要持续更新的 genuine trace 数据集？
8. **CELLSHIFT 的精度上限**：CELLSHIFT 的转换是近似的（基于 RTT 估计而非完整仿真），其理论精度上限是什么？在什么条件下近似会失效？

---
type: paper
title_original: "THE ADVANCED COMPUTING SYSTEMS ASSOCIATION"
title_cn: ""
authors: []
year: 2026
venue: NSDI
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-NSDI-Supercharging_Packet-level_Network_Simulation_of_Large_Model_Training_via_Memoization_and_Fast-Forwarding.pdf"
mineru_md: "02-parsed-markdown/2026-NSDI-Supercharging_Packet-level_Network_Simulation_of_Large_Model_Training_via_Memoization_and_Fast-Forwarding.md"
status: processed
reading_level: L2
research_area: []
task: []
method: []
dataset: []
code: unknown
relevance: medium
created: "2026-09-29"
updated: "2026-09-29"
---

# THE ADVANCED COMPUTING SYSTEMS ASSOCIATION

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | THE ADVANCED COMPUTING SYSTEMS ASSOCIATION |
| 年份 | 2026 |
| 会议/期刊 | NSDI |
| PDF | [[2026-NSDI-Supercharging_Packet-level_Network_Simulation_of_Large_Model_Training_via_Memoization_and_Fast-Forwarding.pdf]] |
| MinerU Markdown | [[2026-NSDI-Supercharging_Packet-level_Network_Simulation_of_Large_Model_Training_via_Memoization_and_Fast-Forwarding.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
Packet-level discrete-event simulation (PLDES) is a preva lent tool for evaluating detailed performance of large model training. Although PLDES offers high fidelity and generality, its slow performance has plagued networking practitioners. Existing optimization techniques either simplify the network model, resulting in large errors; or execute it in parallel using multiple processors, with an upper bound on speedup. This paper explores an alternative optimization direction that reduces the computational loads of PLDES while main taining high fidelity. Our key insight is that, in distributed LLM training, packet-level traffic behaviors often exhibit repetitive contention patterns and steady-states where flow rates stabilize, ignoring these redundant discrete events speeds up the simulation considerably and the error is negligible. We realize this idea by proposing Wormhole, a user-transparent PLDES kernel capable of automatically memoization for unsteady-states and skipping for steady-states. Wormhole adopts network partitioning, state memoization and reuse, and rate-based steady-state identification to accurately determine the periods of each flow’s steady-state, while maintaining simulation consistency after fast-forwarding. Experiments demonstrate that Wormhole can achieve a 744× speedup over the original ns-3 (510× for MoE workload), with a bounded error of <1%. Applying current multithreading parallel tech niques and Wormhole together allows a 1012× speedup, re ducing the simulation time for one GPT-13B training under 128 GPUs from 9 hours to 5 minutes.

## 3. 方法分析
- 输入：论文所研究的网络流量、协议、系统或安全数据（以全文为准）。
- 处理：论文提出的方法或分析流程（摘要级自动提取，待核验）。
- 输出：分类、检测、预测、攻击/防御或系统验证结果。

## 4. 实验表现
- 数据集：待从全文核验。
- Baseline：unknown。
- 指标与数值：不补造，待表格核验。

## 5. 局限性与复现建议
- 当前笔记完成自动入库和摘要级分析，未替代人工深读。
- 先核验数据来源、代码状态、划分和指标，再决定复现等级。

## 6. 知识链接
- [[traffic-classification]]
- [[encrypted-traffic-analysis]]

## 7. 证据状态
- MinerU：已完成；解析质量需人工抽查。
- Bib 元数据：待官方 API/论文首页核验。


## 深度分析（自动证据提取，需人工复核）

### 研究问题与证据
- 主题线索：tor, graph neural, transformer, quic。
- 摘要证据：Packet-level discrete-event simulation (PLDES) is a preva lent tool for evaluating detailed performance of large model training. Although PLDES offers high fidelity and generality, its slow performance has plagued networking practitioners. Existing optimization techniques either simplify the network model, resulting in large errors; or execute it in parallel using multiple processors, with an upper bound on speedup. This paper explores an alternative optimization direction that reduces the computational loads of PLDES while main taining high fidelity. Our key insight is that, in distributed LLM training, packet-level traffic behaviors often exhibit repetitive contention patterns and steady-states where flow rates stabilize, ignoring these redundant discrete events speeds up the simulation considerably and the error is negligible. We realize this idea by proposing Wormhole, a user-transparent PLDES kernel capable of automatically memoization for unsteady-states and skipping for steady-states. Wormhole adopts network partitioning, state memoization and reuse, and rate-based steady-state identification to accurately determine the periods of each flow’s steady-state, while maintaining simulation consistency after fast-forwarding. Experiments demonstrate that Wormhole can achieve a 744× speedup over the original ns-3 (510× for MoE workload), with a bounded error of <1%. Applying current multithreading parallel tech niques and Wormhole together allows a 1012× speedup, re ducing the simulation time for one GPT-13B training under 128 GPUs from 9 hours to 5 minutes.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
Packet-level discrete-event simulation. The pure singleprocess packet-level simulation in ns-3 is full-fidelity but extremely inefficient. During the simulation process, a discrete event level of ${ \cal O } ( 1 0 ^ { 1 2 } )$ can be generated. As shown in Figure 2a, with the increase in cluster scale, the time cost also shows an exponential growth trend, and it takes several weeks to complete the simulation of large-scale clusters. Parallel and distributed DES. UNISON [5] and DONS [19] use multithreading to execute PLDES in parallel on multiple CPUs. But they can only provide sublinear speedups due to the synchronization overhead, which always hits an upper bound, as shown in Figure 2b. Another downside is that it uses up a lot of CPU cores that could be used to run multiple independent experiments in parallel, which would exhibit a linear speedup, since LLM engineers always run multiple sets of experiments at once. Flow-level simulation. Flow-level methods typically fall into two categories. The first computes stable flow rates via maxmin or waterfilling allocation [4, 9, 36, 51, 53, 60, 65]. The second uses analytical models [35,46] or profiling-based techniques [6, 13, 37, 49] to approximate flow completion times. Both ignore packet-level dynamics such as queueing, congestion control, and transient losses, and producing ∼20% FCT error under dynamic LLM workloads (Figure 2c). AI-based methods. AI-based methods [14, 32, 66, 79, 81] are designed to achieve faster performance estimation using neural network models. However, the acquisition of training data incurs high costs. Without a sufficiently large training set, they may not generalize to network scenarios. In Figure 2c, M3 [38] has an error of 10-15% in various scenarios, which is lower than that of flow-level sim

### 局限与复现
This work does not raise any ethical issues.

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


## 深度分析（并行深度分析更新 2026-09-29）

### 方法、实验与证据
Wormhole以记忆化与fast-forwarding加速大模型训练包级仿真；相对ns-3单核GPT/MoE达744×/510×，16核并行达1012×/716×，平均FCT误差≤1%；真实GPT-18B轨迹加速97.75×，与Unison 133.35×。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。

---
type: paper
title_original: "Supercharging Packet-level Network Simulation of Large Model Training via Memoization and Fast-Forwarding"
title_cn: ""
authors: ["Fei Long", "Kaihui Gao", "Li Chen", "Dan Li", "Yiwei Zhang", "Fei Gui", "Yitao Xing", "Wenjia Wei", "Bingyang Liu"]
year: 2026
venue: NSDI
doi: unknown
url: "https://www.usenix.org/conference/nsdi26/presentation/long"
pdf: "00-inbox/PDFs/2026-NSDI-Supercharging_Packet-level_Network_Simulation_of_Large_Model_Training_via_Memoization_and_Fast-Forwarding.pdf"
mineru_md: "02-parsed-markdown/2026-NSDI-Supercharging_Packet-level_Network_Simulation_of_Large_Model_Training_via_Memoization_and_Fast-Forwarding.md"
status: deep-analyzed
reading_level: L3
research_area: ["LLM training simulation", "packet-level discrete-event simulation", "network systems"]
task: ["network simulation", "large-model training evaluation"]
method: ["network partitioning", "flow conflict graph memoization", "steady-state fast-forwarding", "timestamp offsetting"]
dataset: ["SimAI GPT/MoE workloads", "GPT-18B real trace"]
code: unknown
relevance: medium
created: "2026-09-29"
updated: "2026-10-10"
---

# Supercharging Packet-level Network Simulation of Large Model Training via Memoization and Fast-Forwarding

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


## 深度分析（L3 补充，2026-10-09）

### 3. 研究问题、动机与证据边界

#### 3.1 研究问题

Wormhole 研究的是：在保留 packet-level discrete-event simulation（PLDES）队列、拥塞控制、丢包和计算通信重叠语义的条件下，能否跳过 LLM 训练中重复的离散事件，把大规模训练网络仿真的运行时间从小时/周量级降下来。作者将已有路线分为牺牲精度的 flow-level/AI/解析模型和受并行同步上限约束的多核 DES，并把“减少 PLDES 内部工作量”作为与多核并行正交的路线（§1–§2.1）。

#### 3.2 问题发现路径

| 阶段 | 内容 | 证据 |
|---|---|---|
| 现象 | LLM 训练中的 DP/PP/EP 集体通信产生 GB 级大流，PLDES 事件数可超过 O(10^12)；相同冲突模式和稳定速率状态反复出现 | §1、§2.2–§2.3 |
| 痛点 | ns-3 单进程仿真随集群规模近似指数增长；flow-level 方法在动态 LLM 工作负载上约有 20% FCT 误差，多核 DES 加速次线性 | §2.1、Fig. 2 |
| 科学问题 | 哪些网络区域可以独立处理？哪些 transient/steady 事件可以复用或跳过而不破坏时间一致性？ | §1、§3 |
| 方法转化 | 用端口级网络分区隔离状态，用 Flow Conflict Graph（FCG）索引 transient 状态，用发送速率稳定性识别 steady-state，并通过局部时间戳偏移快进 | §3–§6 |

#### 3.3 核心假设及验证状态

| 假设 | 内容 | 验证方式 | 结论边界 |
|---|---|---|---|
| H1 | 同一网络分区的重复流冲突图具有可复用的 transient 收敛过程 | FCG 加权图同构查库，比较 GPT/MoE/真实 trace | 依赖冲突模式可抽象且语义等价；不同拓扑/CCA 的扩展需再验证 |
| H2 | 发送速率稳定时，cwnd、RTT、队列长度和 inflight bytes 也稳定 | Theorem 1 及 Appendix C 证明，§7.3 用 R/I/Q 交叉实验 | 证明假设在论文所建模的收敛 CCA 区间内成立 |
| H3 | 只快进 steady-state 并保持端口缓冲占用，可以保持 packet-level 结果 | 端口暂停、局部事件时间戳偏移、FCT/NRMSE 对 ns-3 对比 | 论文测试为 LLM 训练网络；高度随机/动态工作负载收益会消失 |

### 4. 方法设计

#### 4.1 总体流程

Wormhole 作为 ns-3.17/Open-Usim 的内核扩展运行。首先根据流经过的端口把网络切成互不干扰的 port-level partitions；仿真过程中，分区进入 unsteady-state 时构造 FCG 并查询数据库，命中则直接恢复历史收敛后的快照；未命中则照常执行并存储入口/出口状态。随后对每个分区滑动采样发送速率，在窗口内相对波动低于阈值时进入 steady-state，计算平均速率并暂停该分区端口的事件处理，沿局部事件时间戳跳到流完成、流进入/退出或重路由等中断点。已知中断事件直接确定跳转终点，未知实时事件通过 skip-back 回到最近已知时间点，保持全局时钟顺序（§3–§6）。

#### 4.2 详细 Pipeline

| 步骤 | 输入 | 操作 | 输出 | 证据 |
|---|---|---|---|---|
| 1. 分区 | 静态拓扑、流路径 | 将共享端口的流归入同一连通图；端口是最小粒度 | 网络 partition 集合 | §3.1.1、Appendix A/B |
| 2. FCG 建模 | 分区内流、路径、瞬时速率 | 顶点表示流，边表示共享链路；顶点权重为速率，边权为共享链路数 | `FCG_start` | §4.2 |
| 3. transient 仿真/查库 | `FCG_start`、流大小 | 加权图筛候选，再做图同构；命中则复用历史出口快照，否则执行 CCA 收敛 | `FCG_end`、收敛时间、流状态 | §4.3–§4.4 |
| 4. steady 检测 | 发送速率采样窗口 | 计算最大/最小速率相对波动 `ΔR_l(t)` | steady-state 判定 | Eq. (5)–(6)、§5.1 |
| 5. 快进 | steady 分区、平均速率 | 以窗口平均速率估计后续传输，暂停对应端口使共享 buffer 占用保持不变；局部事件时间戳加 `ΔT` | 跳过 steady 期间的事件 | §6.2–§6.3 |
| 6. 终止/回退 | 新流、流完成、重路由、实时故障 | 跳到已知最早中断点；实时事件晚到时 skip-back | 时间一致的后续仿真 | §5.3、§6.3 |
| 7. 并行 | partitions、Unison LP | 以分区形成更细粒度 LP，查询并发、插入细粒度锁 | Wormhole+Unison | §6.1 |

#### 4.3 公式和误差控制

稳态检测使用

`ΔR_l(t) = (max R(t_k) − min R(t_k)) / mean(R(t_k))`，当 `ΔR_l(t) < θ` 时进入 steady-state（Eq. 5–6）。稳态期间采用窗口平均 `R̂`（Eq. 7）。Theorem 2 给出速率估计相对误差 `< θ/(1−θ)`，Theorem 3 给出 steady duration 相对误差 `< θ`（Eq. 8–9）。窗口长度 `l` 应覆盖至少一个 CCA 速率周期；Appendix F 对 DCTCP 推导 `θ` 应略大于 steady-state 的相对速率波动，`l` 应满足 `Δt(l) ≥ T_C`。默认实验取 `θ=5%`、`l=2000`（§7、Appendix F）。

FCG 数据库只保存分区入口/出口快照、流速率和收敛时间，不保存完整时间演化；其依据是流大小主要决定 steady 持续时间，而 transient 收敛过程由冲突结构决定（§4.3）。这一压缩假设是速度的来源，也是跨场景复用的主要风险点。

#### 4.4 实现细节

- 端口暂停避免 steady 流释放后改变共享 buffer 空间，保持其他分区的丢包时刻一致（§6.2）。
- 不改变全局仿真时钟，只把目标分区事件时间戳整体加上 `ΔT`，并同步调整流大小和序列号（§6.3）。
- 对未知实时事件，先跳到已知最近时间 `T1`；事件真实发生在更早 `T2` 时，将该分区回退到 `T2`（skip-back），随后继续推进（§5.3、§6.3）。

### 5. 与已有路线的本质区别

| 路线 | 速度来源 | 精度代价/限制 | Wormhole 的位置 |
|---|---|---|---|
| ns-3/传统 PLDES | 逐包事件完整执行 | 精度高但事件量巨大 | 保留其语义，跳过可证明的重复区间 |
| flow-level/解析 | 直接求稳定带宽或 FCT | 忽略队列、瞬态丢包和 CCA，论文 Fig. 2 报告约 20% FCT 误差 | 作为低精度替代基线 |
| AI 估计 | 学习性能映射 | 需训练数据，跨场景泛化受限；M3 约 10–15% 误差 | 不依赖训练模型 |
| Unison/DONS | 多核/多进程并行 DES | 同步开销带来次线性上限 | Wormhole 可与 Unison 叠加 |

创新点是把 memoization 与 fast-forwarding 引入 PLDES 内核，并用 partition/FCG/速率稳定性和理论误差上界把跳过行为约束在可解释范围内；它并未改变 CCA、路由或网络拓扑本身。

### 6. 实验设计、数据与结果

#### 6.1 设置

实验服务器为 Linux、双 Intel Xeon、共 56 核、128 GB 内存。拓扑为 4 个 Rail-Optimized Fat-tree，分别模拟 64/128/256/1024 GPU 的 GPT 与 MoE 一次训练迭代；每 GPU 建模为一个 host，以保留多 NIC/交换机连接。GPT 使用 TP(SP)-DP-PP，MoE 使用 TP(SP)-EP-DP-PP，micro-batch=1，global batch=DP×PP。主要 CCA 为 HPCC、DCQCN、TIMELY；除敏感性实验外 `θ=5%`、`l=2000`（§7、Table 1）。

论文还使用 SimAI 生成的 GPT-13B/MoE-8×7B（128 GPU）、GPT-175B/MoE-32×22B（1024 GPU）场景，以及 Nsight Compute 采集的 GPT-18B、256 张 NVIDIA A100、TP8-DP16-PP2-VPP2、micro-batch=1、global batch=512 的真实 trace（§2.2、§7.4）。

#### 6.2 关键结果

| 场景/指标 | Wormhole 结果 | 对比/证据 | 解释边界 |
|---|---:|---|---|
| GPT 单核加速 | 227×–745×；摘要概括最高 744× | ns-3，Fig. 8a | 理想化 LLM 训练工作负载 |
| MoE 单核加速 | 135×–510× | ns-3，Fig. 8a | all-to-all 流使 steady 比例略低 |
| Wormhole+Unison | GPT 最高 1012×，MoE 716×；GPT-13B/128 GPU 从 9 h 降至 5 min | Fig. 8a、§7.1 | 16 核并行，仍依赖 Unison 环境 |
| 事件跳过比例 | GPT >99.5%，MoE >99.2% | Fig. 9b | memoization 与 steady 快进合计 |
| 额外 memoization 加速 | 1.93×–8.43× | Fig. 9a | 在 steady 快进之后的增益 |
| 平均 FCT 误差 | 合成 GPT/MoE 各 CCA 下 ≤1% | Fig. 10 | 相对 ns-3 的 per-flow 平均相对误差 |
| 包级 NRMSE | 多场景 <0.005 | Fig. 11 | first flow 全包 RTT 对 ns-3 |
| 拓扑敏感性 | Fat-tree、Clos、ROFT 速度变化 ≤13%，平均 FCT 误差仍 ≤1% | Fig. 13 | 论文测试的三类 DCN 拓扑 |
| 真实 GPT-18B trace | Wormhole 97.75×，Wormhole+Unison 133.35×；训练时间误差 3.02% | Fig. 14、§7.4 | 复杂 recomputation/硬件波动导致误差高于合成场景；ASTRA-sim+ns-3 为 3.01% |
| 数据库存储 | 1024 GPU 场景 <100 KB | Appendix H | 只存关键 snapshot，不等于完整轨迹 |

#### 6.3 证据边界与局限

1. 论文的 ≤1% 误差主要来自合成/规则化训练工作负载；真实 GPT-18B trace 的端到端训练时间误差约 3.02%，应单独报告。
2. Wormhole 的收益依赖重复冲突和稳定速率。论文明确指出公共云、多租户、高度动态随机流场景下收益可能降到 ns-3 基线水平，但不会额外增加时间或精度损失（§1）。
3. FCG 忽略绝对路径长度和拓扑空间位置，只编码共享链路关系与瞬时速率；该近似在论文场景中可接受，跨拓扑/跨 CCA 的图同构等价性仍需额外验证（§4.2–§4.4）。
4. 端口暂停保持共享 buffer，但会使实现复杂化；实时未知事件依赖 skip-back，若外部事件频繁到达，理论上的快进空间会被侵蚀（§6.2–§6.3）。
5. 实验以一次训练迭代和四类 ROFT 规模为主，未展示更长时间、故障密集或多租户混部的系统性结果。
6. 解析正文只说明基于 ns-3.17/Open-Usim 的二次开发和“数千行代码”，未给出 Wormhole 官方仓库地址，代码状态记为 unknown。

### 7. 学习与应用

#### 7.1 复现路线

1. 按 Table 1 搭建 64/128/256/1024 GPU 对应的 GPT/MoE 流量生成器，在 ns-3.17 或 Open-Usim 中先得到原始 PLDES 结果。
2. 实现 port-level partition，构造包含流顶点、共享链路边、速率和重叠链路数的 FCG；先关闭复用，验证分区状态与原 ns-3 一致。
3. 加入 weighted graph-isomorphism 查库和入口/出口 snapshot，比较命中与未命中的 FCT。
4. 加入 `ΔR_l(t)`、`R̂`、端口暂停和局部时间戳偏移；从 `θ=5%`、`l=2000` 起做阈值敏感性。
5. 与 Unison 组合时，按 partitions 形成更细 LP，检查 16 核加速和数据库并发锁的正确性。
6. 最后在真实 GPT-18B trace 上报告加速与端到端训练时间误差，不能用合成 workload 的 ≤1% 代替真实 trace 结果。

#### 7.2 对流量安全研究的启发

- 可以把“可重复流形态/稳定区间”作为流量分析系统的计算压缩机会，但必须先验证状态等价条件和跨分区缓冲耦合。
- 论文把加速收益、误差上界和阈值选择放在同一条证据链中，适合迁移到加密流量仿真或在线检测的近似评估。
- 当真实流量的重复性不足时，应把 Wormhole 视为自动退化到完整仿真的优化层，而非把合成场景的加速数字外推到生产环境。

### 8. 总结

> 用分区、记忆化和稳态快进压缩 LLM 包级仿真。

速记 Pipeline：端口级分区 → FCG 查库复用 transient → 速率窗口判定 steady → 暂停端口并局部时间戳快进 → 中断/skip-back 恢复 → 与 Unison 并行。

### 9. 关联知识与同步边界

当前库中没有专门的 packet-level LLM simulation 方法页；本次只保留在论文笔记中，不自动创建空白知识页，也不修改 04–09 层共享表。

### 10. 本地证据记录

| 观点 | 原始资料位置 |
|---|---|
| PLDES 事件量、重复冲突和 steady-state 观察 | raw Markdown §1、§2.1–§2.3，Fig. 2–3 |
| partition、FCG、数据库字段与查库 | raw Markdown §3–§4 |
| 稳态判定、Theorem 1–3 与阈值指导 | raw Markdown §5、Appendix C–F |
| 局部端口暂停、时间戳偏移、skip-back | raw Markdown §6、Fig. 7 |
| 加速、误差、敏感性和真实 trace | raw Markdown §7、Fig. 8–14 |
| 1024 GPU 数据库 <100 KB | raw Markdown Appendix H、Fig. 15 |

## 历史自动入库段落说明

- 本笔记前部的自动入库、摘要级或待核验段落是入库时的历史快照，按规范保留以避免删除原始记录。
- 本次新增的深度分析段落、证据记录和局限说明优先；历史段落中的“待深读/待核验”状态不代表当前分析尚未完成。

---
type: paper
title_original: "PipHeap: Approximate Heap in the Pipeline Empowering Network Measurement"
title_cn: "PipHeap：流水线内的近似堆，赋能网络测量"
authors: ["Yuhan Wu", "Fenghao Dong", "Qizhi Chen", "Aomufei Yuan", "Kaicheng Yang", "Hanglong Lv", "Tong Yang", "Wenrui Liu", "Gaogang Xie"]
year: 2025
venue: "ACM IMC 2025"
doi: "10.1145/3730567.3764487"
url: "https://doi.org/10.1145/3730567.3764487"
pdf: "00-inbox/PDFs/2025-IMC-PipHeap__Approximate_Heap_in_the_Pipeline_Empowering_Network_Measurement.pdf"
mineru_md: "02-parsed-markdown/2025-IMC-PipHeap__Approximate_Heap_in_the_Pipeline_Empowering_Network_Measurement.md"
status: processed
reading_level: L2
research_area: ["anomaly-detection"]
task: ["anomaly-detection"]
method: []
dataset: ["CAIDA (2018 IP trace)", "WebPage (fimi.ua.ac.be)"]
code: "https://github.com/PipHeap/PipHeap"
relevance: medium
created: "2026-09-19"
updated: "2026-09-19"
---

# PipHeap: Approximate Heap in the Pipeline Empowering Network Measurement

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | PipHeap: Approximate Heap in the Pipeline Empowering Network Measurement |
| 中文标题 | PipHeap：流水线内的近似堆，赋能网络测量 |
| 作者 | Yuhan Wu\*, Fenghao Dong\*, Qizhi Chen\*, Aomufei Yuan, Kaicheng Yang, Hanglong Lv, Tong Yang†, Wenrui Liu, Gaogang Xie（北京大学；Gaogang Xie 兼中国科学院计算机网络信息中心 / 中国科学院大学；\*共同一作，†通讯作者） |
| 年份 | 2025 |
| 会议/期刊 | ACM Internet Measurement Conference (IMC 2025), October 28–31, 2025, Madison, WI, USA |
| 研究方向 | 可编程交换机上的网络测量（sketch / 重流检测 / 数据平面算法） |
| 任务类型 | 流大小估计、heavy hitter 检测、层次 heavy hitter（HHH）、任意部分键查询、流大小分布/熵/基数估计 |
| 方法关键词 | 数据平面可实现的近似最小堆；AggNode（非对称多数算法 + active score，等价 1/(1+W) 筛孔）+ MaxNode 的二叉树；节点堆叠（stacking）把 2L 级流水线压缩到 L+1；Merge/Skip/Kick 三操作；与 sketch 协作（分离大象流/小鼠流） |
| 数据集 | CAIDA 2018 匿名骨干网 trace（1 分钟，约 27M 包、0.25M 流，仅用源 IP）；WebPage（fimi.ua.ac.be，约 64M item、0.94M 去重 item） |
| 是否开源 | 是：https://github.com/PipHeap/PipHeap（P4 + C++，ref [5]） |
| PDF | 00-inbox/PDFs/2025-IMC-PipHeap__Approximate_Heap_in_the_Pipeline_Empowering_Network_Measurement.pdf |
| MinerU Markdown | 02-parsed-markdown/2025-IMC-PipHeap__Approximate_Heap_in_the_Pipeline_Empowering_Network_Measurement.md |

---

## 1. 一句话总结

> 把传统"气泡上浮"最小堆改造成数据平面可实现的近似堆（AggNode 非对称多数筛 + MaxNode 取大者 + 节点堆叠），与 8 种 sketch 组合后在同等内存下平均降低 33%–97%（均值 78%）的测量误差。

---

## 2. 摘要翻译

### 2.1 摘要原文

Network telemetry has seen an increasing trend of deploying approximate measurement algorithms (e.g., sketches) on programmable switches due to their ability to provide line-rate speed, high measurement accuracy, and low memory cost. Heap, a vital component of many of measurement algorithms, hinders their deployment because of the difficulties in incorporating it into pipelines. In this paper, we introduce PipHeap, a pipeline-friendly, binary-tree-based min heap that can enhance existing sketches without introducing additional errors. Through evaluation with real-world datasets, we demonstrate that PipHeap can reduce the error of these integrated algorithms by 33% to 97% (78% on average) under the same memory allocation. We have successfully implemented PipHeap and its combination with six different sketches in our testbed, and successfully extended other approximate algorithms (e.g. Space-Saving) onto programmable switch platforms. We have made all code associated available as open-source.

### 2.2 摘要中文翻译

网络遥测领域正越来越多地把近似测量算法（如 sketch）部署到可编程交换机上，因为它们能提供线速、高精度与低内存开销。堆（Heap）作为许多测量算法的关键组件，因难以嵌入流水线而阻碍了这类部署。本文提出 PipHeap——一种对流水线友好的、基于二叉树的最小堆，可在**不引入额外误差**的前提下增强现有 sketch。基于真实数据集的评估表明，在同等内存分配下，PipHeap 可把被集成算法的误差降低 33% 到 97%（平均 78%）。我们已在真实测试床上实现 PipHeap 及其与六种不同 sketch 的组合，并成功把其他近似算法（如 Space-Saving）扩展到可编程交换机平台。相关代码已全部开源。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 网络测量（流大小、heavy hitter、流大小分布等）是调度、拥塞控制、负载均衡、流量工程、异常检测等网络功能的前置步骤，而**堆**是其中大量算法（Space Saving、Frequent、Unbiased Space Saving、RHHH 等）的核心组件，堆类算法在估计精度上具有最优的理论性质（`§1`, `§2.1`, `§2.2`）。
- 可编程交换机（RMT/Tofino）是线速测量的理想载体，但**堆无法直接映射到流水线**（`§1`, `§2.3`）。

### 3.2 现有方法的痛点和不足

- **流水线的硬约束**：每个 stage 只能访问自己的 SRAM、一次只能处理一个包、包只能顺序前进，数据不能回流；一次 action 最多访问一个 bucket（含两个连续 32-bit 字段），只能做少量算术与 if-else，读出 1 个 32-bit 结果（`§2.3`）。堆的"bubble-up"需要与父节点比较并交换，天然需要数据回流（`§3.4`）。
- **单节点都难实现**：节点需同时支持 (1) 同 key 合并、(2) 新 key 更大时替换并输出旧 key-值。若把 key 与 value 放同一 stage（同一 bucket）则无法把旧 key 与旧 value 一起读出；若拆到两个 stage，后一 stage 的比较结果无法回传给前一 stage（`§2.3`）。
- **recirculation 路线的固有缺陷**：包重入流水线会把吞吐至少减半量级（10% 包重入即 ≥10% 吞吐损失），带来延迟（PSMM 报告平均约 970µs）、稳定性（丢包导致 sequencer 卡死 >1ms）与资源占用问题（Precision 的期望重入次数随包数按 O(√n) 增长）（`§2.4`）。
- 现有可在数据平面实现的重流方案各有缺陷：Hash Pipe 基于不存在的编程行为模型、无法在真实产品上实现；Elastic 可实现但误差大（搬移后流大小被重置为 1）；Qpipe/Precision 依赖 recirculation（`§6`）。

### 3.3 论文的研究假设或核心直觉

核心直觉：**把堆的插入顺序倒过来**——不从根往下、而是从"叶层"开始，在自下而上的每一级做"Kick/Skip/Merge"三选一决策；底部 AggNode 用非对称多数算法（active score 匹配 +W、不匹配 −1）当作一个筛孔为 1/(1+W) 的筛子，把小鼠流筛掉、让大象流留在底部；再配合上一层 MaxNode 完成"留存较大流"的堆语义。由于决策只看当前节点与当前包（不依赖父节点回传），整个过程可在单向流水线内完成（`§3.1`, `§3.2.1`, `§3.4`）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 最优测量算法（Space Saving/Frequent/USS/RHHH）都以最小堆为骨架，但它们在可编程交换机上"要么无法实现、要么必须 recirculation" | §2.2, §2.4 |
| 痛点提炼 | recirculation 带来吞吐、延迟、稳定性、资源四类代价，且堆的单节点在流水线内都无法实现（key/value 无法跨 stage 协同） | §2.3, §2.4 |
| 问题转化 | 如何在不回流、不增加 recirculation 的前提下，用一个自底向上的近似结构实现"保留最大的若干流"这一堆语义 | §3.1（Kick/Skip 决策）、§3.4 |
| 文献定位 | 已有数据平面重流算法（Elastic 等）误差大；CoCo 曾尝试在数据平面近似实现 USS 但未解决堆的一般化问题；"数据平面上的通用近似堆"是空白 | §2.2, §6 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 一个自底向上、单向流水线的近似堆（AggNode+MaxNode+节点堆叠）可以在数据平面上近似理想堆的行为，与既有 sketch 组合后**不引入额外误差**且在同内存下降低误差 | §3.1–§3.3（AggNode 的筛子性质、MaxNode 的取大者语义） | 与 CPU 上的理想 Space Saving 对比、与 Elastic 对比（Figure 5）、8 种 sketch 组合实验 |
| 辅助假设 | 节点堆叠能把 L 层 AggNode 所需的 stage 数从 2L 降到 L+1，使 12 级流水线可容纳 11 层 | §3.2.3（相邻节点 stage 交错复用） | Tofino 测试床实现（131071 节点） |
| 辅助假设 | PipHeap 作为"前置筛子"把小鼠流交给后续 sketch，可使后续 sketch 的输入分布更平滑、从而提升其精度 | §4.1（"discarded flows" 送入协作者） | 与 CM/Count/FCM/Univmon/NitroCM/Elastic/CoCo 等组合实验 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | CAIDA、240KB 下误差降幅 CM 33%、Count 92%、FCM 85%、Univmon 97%、NitroCM 72%、Elastic 80%、CoCo 87%，平均 78%；PipHeap 精度接近理想 SS | §5.3, Figure 5 |
| 节点堆叠 | 支撑 | Tofino 上实现 131071 节点的 PipHeap（可跟踪 >100K 重流），与 6 种 sketch 组合 | §5.4, Table 3 |
| 前置筛子假设 | 支撑 | Heavy hitter（最频繁 3000 流）检测中 40KB 即达 >80% 精度/召回，Elastic 要到 100KB 才达到 | §5.3.1, Figure 7 |

---

## 4. 方法设计

### 4.1 方法整体流程

PipHeap 是一棵**层数 L、第 i 层含 m_i = ⌊m_{i−1}/2⌋ 个节点**的二叉树：包按 H(KEY) 命中的叶节点进入第 1 层，逐层向上；每层遇到 (1) 同 key → Merge（累加并结束）、(2) 异 key 且节点有 activity → Skip（新流去下一层）、(3) 异 key 且 activity 耗尽 → Kick（新流留下、旧流去下一层）。前 L1 层为 AggNode（非对称多数筛），其余层为 MaxNode（保留较大流）；最后一层若仍发生 Skip/Kick 则丢弃该流。查询时把各层中存储该 KEY 节点的 value 求和（`§3.1`, Algorithm 1–3）。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 哈希定位 | 包 ⟨KEY, VAL⟩ | j ← H(KEY)，落到第 1 层叶节点 | 目标节点 N_1^j | 随机化分流（`§3.1`） |
| Step 2 AggNode 级（1..L1） | ⟨KEY, VAL⟩、当前节点 | 同 key → assist += W、value += VAL 并结束；异 key 且 assist≠0 → assist −1、跳过本层；assist=0 → 换成新流（assist←W, value←VAL），旧流 ⟨key, value⟩ 送下一层 | 可能向上传递的旧流 | 用 1/(1+W) 的"筛孔"筛掉小鼠流（`§3.2`, Algorithm 1） |
| Step 3 MaxNode 级（L1+1..L） | 同上 | 同 key → 合并；否则比较 size：新流大 → 替换并把旧流上送，否则新流上送 | 上送流或结束 | 完成"保留较大者"的堆语义（`§3.3`, Algorithm 3） |
| Step 4 丢弃 | 顶层仍未被存下的流 | 直接丢弃 | — | 近似堆的取舍（`§3.1`） |
| Step 5 查询 | 查询 KEY | 逐层找 N_i^{H(KEY)/2^{i−1}}，若 key 匹配则累加 value | 估计流大小 | 全数据平面可完成查询（`§3.1`, Algorithm 2） |
| Step 6 与 sketch 协作 | 被 PipHeap 丢弃的流 | 送入协作者 sketch（CM/Count/FCM/Univmon/NitroCM/Elastic/CoCo 等）；查询时两侧结果相加 | 更精确的估计 | 大象流留住、小鼠流分布更平滑（`§4.1`, `§5.3`） |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| AggNode（前 L1 层） | 非对称多数聚合：active score 匹配 +W / 不匹配 −1，归零则换流 | 包 ⟨KEY,VAL⟩、节点 {key, assist, value} | Merge 结束 / Skip 上送 / Kick 换出旧流 | 占 2 个 pipeline stage（key+assist 一个、value 一个）；相邻节点可堆叠（`§3.2`） |
| MaxNode（后 L−L1 层） | 基本堆节点语义：两者取大，小者上送 | 同上 | 上送较小流 | 同样 2 stage；用 MAX 逻辑避免三分支比较（`§3.3`） |
| 节点堆叠（stacking） | 把节点 A 的第 2 stage 与节点 B 的第 1 stage 并行 | 上一级的 ρ1 输出 | 决定下一级输入是 new 还是 old 值 | stage 数从 2L 降到 L+1（`§3.2.3`, Figure 2） |
| 协作 sketch | 承接 PipHeap 丢弃的流 | 丢弃流 | 独立的流大小估计 | 查询时与 PipHeap 结果相加；"不引入额外误差"（`§4.1`） |

### 4.4 公式、算法和机制解释

- **AggNode 的筛子性质**：设流密度为包出现概率且包 IID，则密度 < 1/(1+W) 的流一旦被误记进 AggNode，必定在之后某个时刻被逐出——即 AggNode 等价于筛孔大小 1/(1+W) 的筛子，最终把"尺寸小于筛孔"的小鼠流筛走；传统多数算法是 W=1 的特例，会引发过多换出（`§3.2.1`）。
- **active score 不用流大小的原因**：若用流大小参与打分，会额外消耗一倍 stage，破坏堆叠技术的收益（`§3.2.1` 补充说明）；由此漏掉"一次插入的大流"由 MaxNode 兜底（`§3.3`）。
- **单节点实现（2 stage）**：stage 1 读 key/assist 并做条件判断（并行执行、按赋值前的内容判断），stage 2 依 ρ1 ∈ {empty, KEY, old key} 区分 Skip/Merge/Kick，并把需要上送的 ⟨key, value⟩ 组装好（`§3.2.3`, `§3.3`）。
- **查询（Algorithm 2）**：沿 H(KEY) 的路径逐层累加匹配节点的 value；未命中则报 0。

### 4.5 方法优势

- **不引入额外误差**：与协作者组合后整体误差只取决于协作者，可完整继承其性质（单边误差、无偏估计等）（`§4.1`）。
- **不依赖 recirculation**：避免吞吐/延迟/稳定性/资源四类代价（`§2.4`）。
- **通用性**：同一结构同时服务单键查询、HHH、任意部分键查询，并把 RHHH、Space Saving 这类原本无法上数据平面的算法"搬"了上去（`§4`, `§5.3.3`）。
- 在 Tofino 上真实实现：131071 节点，主要资源占用 Stateful ALU 31.25%、Map RAM 26.82%（`§5.4`）。

### 4.6 方法不足

- 顶层仍会被丢弃的流（未被任何节点存下）不可恢复，属近似结构；W 过大反而因小流难以踢出而降低精度（`§5.2.1`）。
- 与协作者组合时，PipHeap 只做"大象/小鼠分流"，小鼠流精度仍取决于协作者 sketch 本身（`§4.1`）。
- 只做到 2 字段/节点的近似语义：查询需逐层扫描路径（L 次查找），且 AggNode 的 assist 只用计数不用 size，机制上牺牲了一般堆的严格序关系（`§3.2.1`, Algorithm 2）。
- 评测仅两个数据集（CAIDA、WebPage），未覆盖真实多租户/多任务并发场景。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

- 与 **recirculation 路线**（Precision、Qpipe）：后者靠把包重入流水线实现多轮更新，PipHeap 用"决策前移 + 自底向上"的单向设计彻底免去重入（`§2.4`, `§3.4`）。
- 与 **Elastic**（唯一可在数据平面无 recirculation 实现的重流方案）：Elastic 在流搬移后把 size 重置为 1，误差大；PipHeap 保留旧流的真实 value 并逐层上送（`§5.2.2`, `§6`）。
- 与 **理想 Space Saving（CPU）**：PipHeap 精度接近理想 SS，说明其堆语义近似得较成功；这是论文自证精度的关键对照（`§5.2.2`, Figure 5）。
- 与 **CoCo**：CoCo 曾尝试在数据平面近似 USS 以实现任意部分键查询，PipHeap 与其组合可继续降低 CoCo 的误差（`§4.3`, `§5.3.4`）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 首个全数据平面近似堆 | 自底向上插入 + Kick/Skip/Merge 三操作，无需数据回流 | 高 | 是（一切需要"保留 top-k 键值对"的数据平面结构） |
| AggNode 非对称多数算法（active score） | 匹配 +W、不匹配 −1，等价 1/(1+W) 筛孔的筛子；W=8 最优 | 高 | 是（重流过滤的一般机制） |
| 节点堆叠（stacking） | 相邻节点 stage 交错，2L → L+1 | 中高 | 是（其他多级数据平面结构的 stage 压缩） |
| 数据平面查询 + 与 sketch 协作 | 支持在数据平面直接输出结果；丢弃流交给协作者且不引入额外误差 | 中 | 是 |
| 把 RHHH/Space Saving 搬上数据平面 | PipHeap 版 RHHH 仅增加 2% AAE（24-bit 前缀查询） | 中 | 是 |

### 5.3 适用场景

- 需要在可编程交换机上做**重流检测 / 流大小估计 / HHH / 任意部分键查询 / 分布与熵估计**的线速测量（`§2.1`, `§4`）。
- 资源受限（12 stage 流水线、SRAM/ALU 紧张）且不允许 recirculation 的部署。
- 不适用：需要严格堆序保证（如精确 top-k 排序）、或流 key 极长导致节点位宽超限的场景。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| Space Saving / Frequent / USS（CPU 堆类） | 精度最优、可报出 elephant flow 的 ID 与大小 | 无法在可编程交换机流水线实现 | PipHeap 以近似结构逼近其精度（CAIDA 上仅略逊于理想 SS） |
| Elastic Sketch（P4） | 可无 recirculation 实现、时延极低 | 流搬移后 size 重置为 1，误差显著；HHH 场景 40KB 时无法达到 >80% 精度 | 与 Elastic 组合后精度/召回全面提升，且 40KB 即达 >80% |
| Precision / Qpipe（recirculation） | 支持 top-k 等复杂操作 | 需重入，吞吐/延迟/稳定性代价大（Precision 重入次数 O(√n)） | 完全不需 recirculation |
| CoCo | 首个支持任意部分键查询的数据平面方案 | 基于近似 USS，精度受限 | 组合后 CAIDA 240KB 下 CoCo 误差降 87% |
| Hash Pipe | 早期重流检测方案 | 基于不存在的编程行为模型，无法在真实产品实现 | 在 Tofino 真机实现 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- 实现：PipHeap 及全部对比算法用 **P4 + C++** 实现；精度实验在 CPU 平台（36 核 Intel i9-10980XE、128GB DDR4、25.4MB L3、4.2GHz）进行；真机实验在 **Tofino** 可编程交换机上（131071 节点 PipHeap 及与六种 sketch 的组合）（`§5.1`, `§5.4`）。
- 组合实验的内存切分约定：一半内存给 PipHeap，另一半留给协作者算法（`§5.3`）。
- 测量模型：经典固定窗口，窗口结束把数据平面数据送控制平面并清空（`§5.4`）。

### 6.2 数据集

- **CAIDA**：2018 年匿名骨干网 trace（高速监控点采集）；受交换机硬件限制只用源 IP（4 字节）作为 ID；使用 1 分钟 trace，约 27M 包、0.25M 流（`§5.1`）。
- **WebPage**：由网页集合构建（fimi.ua.ac.be），每条目 4 字节代表网页中不同条目数；使用其中约 64M item、0.94M 去重 item（`§5.1`）。

### 6.3 Baseline

Space Saving（理想堆，仅 CPU 可跑）、Elastic Sketch（P4 版，4 层、λ=32）、以及作为"协作者"被组合的 sketch：CM、Count、FCM、Univmon、NitroCM、CoCo，另有 SuMax、Space Saving、RHHH 出现在资源表中（`§5.2.2`, `§5.3`, Table 3）。

### 6.4 评价指标

ARE（平均相对误差）、AAE（平均绝对误差）、Precision Rate、Recall Rate（均针对"最频繁 3000 流"集合 S_k 定义）；HHH/部分键查询用 AAE/ARE/Precision/Recall；另有资源占用（SRAM、Map RAM、Hash Bits、TCAM、Stateful ALU、Exact Match Xbar、VLIW Instr）（`§5.1`, `§5.4`, Table 3）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| CAIDA, 240KB, 7 种 sketch | 误差降幅 | 33%–97%（均值 78%） | — | — | CM 33%、Count 92%、FCM 85%、Univmon 97%、NitroCM 72%、Elastic 80%、CoCo 87%（`§5.3`） |
| CAIDA, 240KB, 6 种 sketch（流大小估计） | 误差降幅 | 均值 76% | — | — | CM 33%、Count 92%、FCM 85%、Univmon 97%、NitroCM 72%、Elastic 80%（`§5.3.2`, Figure 6b） |
| RHHH on 数据平面 | 额外 AAE | +2% | 理想 RHHH（CPU） | — | 24-bit 前缀、240KB（`§5.3.3`, Figure 8） |
| CoCo 任意部分键查询 | 误差降幅 | 87% | CoCo 原版 | — | CAIDA 240KB、16-bit 前缀（`§5.3.4`） |
| Heavy hitter 检测（最频繁 3000 流） | Precision/Recall | 40KB 时均 >80% | Elastic @100KB | 同精度下省 60% 内存 | `§5.3.1`, Figure 7 |
| Tofino 资源占用 | Stateful ALU / Map RAM | 10 (31.3%) / 103 (26.8%) | 组合后最高 36.1% / 31.5% | — | Table 3 |

> ⚠️ MinerU 解析问题：正文摘要与 `§5.3` 均称"与 8 种 sketch 组合"，而"Key results"段落只列出 7 种（CM、Count、FCM、Univmon、NitroCM、Elastic、CoCo），第 8 种应为 RHHH（单独在 `§5.3.3` 报告）；另有 `§5.3.2` 的均值写作 76% 与摘要/`§5.3` 的 78% 并存。引用时需注明口径。

### 6.6 优势最明显的场景

- **Univmon（97%）与 Count（92%）**：这两个 sketch 对"输入分布更平滑"最敏感，PipHeap 前置分流收益最大（`§5.3`）。
- **小内存段（<60KB）**：理想 Space Saving 在内存很小时表现不佳，PipHeap 与 Elastic 的差距在此区间最大（`§5.2.2`）。
- **HHH / 任意部分键查询**：使原本只能在 CPU 跑的 RHHH 进入数据平面且仅 +2% AAE（`§5.3.3`）。

### 6.7 局限性

- 精度只在 CPU 平台系统评测；Tofino 实验聚焦资源占用（Table 3）而非在线精度对比（`§5.4`）。
- 数据集只有 CAIDA 与 WebPage 两个，且 CAIDA 只保留源 IP 字段（受交换机限制），键空间与真实五元组有差距（`§5.1`）。
- 参数 W 的最优值（8）是在特定数据集/3000 重流口径下选出的，跨场景是否仍最优未讨论（`§5.2.1`）。
- 未与 recirculation 方案（Precision、Qpipe）做端到端精度对比——论文对 recirculation 的批评基于延迟/吞吐的引用数据（`§2.4`）。

---

## 7. 学习与应用

### 7.1 是否开源？

是。P4 + C++ 实现，仓库：https://github.com/PipHeap/PipHeap（`§5.1`, ref [5]）。

### 7.2 复现关键步骤

1. 在 P4 中实现 AggNode 与 MaxNode：节点含 {key, assist, value} 三字段，按 2 stage/节点的映射落地，并采用 stacking 交错以压缩 stage 数（12 级流水线容纳 11 层）。
2. 配置层数 L、每层节点数 m_i = ⌊m_{i−1}/2⌋，首层哈希 H(·) 把 key 映射到叶节点。
3. 实现三个操作（Merge/Skip/Kick）与 Algorithm 1/3 的分支逻辑（注意交换机不支持三分支，用两分支 + MAX 逻辑实现 MaxNode 的辅助字段更新）。
4. 查询：Algorithm 2 在数据平面沿路径累加匹配节点 value；若要与协作者组合，则把丢弃流送入协作者并相加两侧估计。
5. 评测：CAIDA（只用源 IP）/WebPage，扫内存 30–120KB 与 W∈[1,16]，按最频繁 3000 流计算 ARE/AAE/PR/RR。

### 7.3 关键超参数、预处理和训练细节

- **W = 8 最优**（W∈1–16；W=1 效果差，W>8 后因小流难以踢出而退化）（`§5.2.1`, Figure 4）。
- Elastic 对比配置：P4 版、4 层、λ=32（`§5.2.2`）。
- 组合算法内存对半分；固定窗口测量模型（`§5.3`, `§5.4`）。
- 哈希函数鲁棒性：CRC、Murmur、Farm 结果几乎一致（`§5.1`）。

### 7.4 能否迁移到其他任务？

- **数据平面 top-k/重流结构**：任何需要在交换机内维护"键-值对集合且偏向大值"的任务（如 DDoS 检测、per-flow 特征提取）都可套用 PipHeap 或 AggNode 筛子。
- **stage 压缩技巧**：节点堆叠思路可迁移到其他需要多级状态的数据平面结构（如多级 sketch、状态机）。
- **分层过滤思路**：AggNode（频繁度筛）+ MaxNode（大小筛）的两段式设计可迁移到流分类/特征工程中的"热流先行过滤"。

### 7.5 对我的研究有什么启发？

- "把全局数据结构拆成单向流水线上的近似决策序列"是数据平面算法的通用范式：PipHeap 把堆的全局序关系替换为局部 Kick/Skip 决策 + 概率筛。
- 论文的评测结构值得借鉴：先用 CPU 平台与**理想算法**（Space Saving 上界）对比证明近似质量，再用真机资源表证明可实现性，最后用"与协作者组合"证明通用增益。
- 与流量分析工作结合点：数据平面重流/特征预筛（参见 KB 中 SketchFeature、SuperFE）可作为加密流量分类的在线前置层。

---

## 8. 总结

### 8.1 核心思想

> 用自底向上 + 概率筛的单向结构，在交换机流水线内近似实现最小堆。

### 8.2 速记版 Pipeline

1. 包 ⟨KEY, VAL⟩ 哈希落到第 1 层叶节点。
2. 前 L1 层 AggNode：同 key 合并（assist+W）；否则 assist−1 并跳过；assist=0 则换流、旧流上送。
3. 后 L−L1 层 MaxNode：保留较大流，小者继续上送；顶层仍未存下的流丢弃。
4. 丢弃流交给协作者 sketch；查询时两侧相加。
5. 节点堆叠把 2L 级需求压到 L+1 级，Tofino 上以 131071 节点规模落地。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[anomaly-detection]]（网络测量是异常检测的前置步骤：`§1` 明确列出 anomaly detection 为下游网络功能之一）

### 9.2 相关方法

- 白名单方法页（contrastive-learning / convolutional-network / graph-neural-network / multi-modal-fusion / pre-training-finetuning / self-supervised-learning / state-space-model / transformer）与本论文（数据平面 sketch / 近似堆算法）无直接对应，故不链接。

### 9.3 相关任务

- [[anomaly-detection]]（重流检测等测量结果服务于异常/攻击检测）

### 9.4 可更新的综述页面

- 白名单综述页（survey-encrypted-traffic-analysis / survey-few-shot-learning / survey-malicious-traffic-detection / survey-traffic-foundation-model / survey-website-fingerprinting）均非测量系统方向，本论文不适用，故不链接。

### 9.5 可加入的对比表

- [[method-comparison-table]]（提出新数据结构 PipHeap，可作为数据平面测量方法的对比行）
- [[open-source-registry]]（P4 + C++ 开源：https://github.com/PipHeap/PipHeap）
- [[dataset-comparison-table]]（CAIDA 2018 IP trace 仅用源 IP 的用法值得记录）

### 9.6 相关论文笔记（KB 已有）

- [[2025-NDSS-SketchFeature__High-Quality_Per-Flow_Feature_Extractor_Towards_Security-Aware_Data_Plane]]（同属数据平面 sketch/测量方向；SketchFeature 主张全量逐流测量优于 top-K 选择式测量，与 PipHeap 的"重流优先"近似思路形成对照）
- [[2025-EuroSys-SuperFE__A_Scalable_and_Flexible_Feature_Extractor_for_ML-based_Traffic_Analysis_Applications]]（ML 流量分析的在线特征提取系统，可作为 PipHeap 的下游应用场景）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 堆无法在流水线上实现：key/value 同 stage 则读不出旧值、分 stage 则比较结果无法回传 | 单节点 case study 的两种失败方案分析 | §2.3 |
| recirculation 有四类代价（吞吐 ≥10% 损失、PSMM 约 970µs 延迟、sequencer 失败 >1ms、Precision O(√n) 重入） | §2.4 的四小节引用数据 | §2.4 |
| AggNode 等价于筛孔 1/(1+W) 的筛子（IID 假设下密度 <1/(1+W) 的流必被逐出） | §3.2.1 的密度论证 | §3.2.1 |
| 节点堆叠把 2L 级降为 L+1 级（12 级流水线 → 11 层 AggNode） | §3.2.3 | §3.2.3 |
| W=8 最优（W∈1–16，最频繁 3000 流口径） | Figure 4 与正文结论 | §5.2.1 |
| PipHeap 精度接近理想 Space Saving，明显优于 Elastic（30–120KB 内存区间） | Figure 5 与正文 | §5.2.2 |
| 8 种 sketch 组合：CAIDA 240KB 下误差降 33%–97%，均值 78%；RHHH 仅 +2% AAE | Key results 段与 §5.3.3 | §5.3 |
| Tofino 实现 131071 节点、可跟踪 >100K 重流；最高资源占用 Stateful ALU 31.25%、Map RAM 26.82% | §5.4 与 Table 3 | §5.4 |
| HHH 检测 40KB 达 >80% 精度/召回，Elastic 需 100KB | §5.3.1 | §5.3.1 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2025-IMC-PipHeap__Approximate_Heap_in_the_Pipeline_Empowering_Network_Measurement.pdf
- MinerU Markdown：02-parsed-markdown/2025-IMC-PipHeap__Approximate_Heap_in_the_Pipeline_Empowering_Network_Measurement.md

---

## 12. 后续问题

- 论文声称"与 8 种 sketch 组合"，但 Key results 只列 7 种；另有 SuMax、Space Saving 出现在 Table 3 的资源表中——具体是哪 8 种、第 8 种是否计入 78% 均值，需查 PDF 原文核实（本笔记按"7 种 + RHHH"表述）。
- 误差降幅的统计口径（240KB、CAIDA、7 种 vs 6 种、均值 78% vs 76%）存在多个版本，跨场景引用时需注明数据集/内存/sketch 数。
- Tofino 实验未给在线精度，只给资源：真实线速下的精度退化是否可忽略，论文未验证。
- CAIDA 只用源 IP（4 字节）作为 key：与五元组场景的哈希冲突/流区分度差异未讨论。
- 与 recirculation 方案（Precision/Qpipe）缺少同口径端到端对比；其"更优"结论主要建立在引用文献的延迟/吞吐数据上。

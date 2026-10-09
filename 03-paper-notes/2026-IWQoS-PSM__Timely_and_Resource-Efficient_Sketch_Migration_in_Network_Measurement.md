---
type: paper
title_original: "PSM: Timely and Resource-Efficient Sketch Migration in Network Measurement"
title_cn: "PSM：及时且资源高效的网络测量 Sketch 迁移框架"
authors: [Xun Zhou, Hongyan Liu, Xiang Chen, Zhengyan Zhou, Zihao Cheng, Di Wang, Chunming Wu]
year: 2026
venue: "IEEE/ACM IWQoS 2026"
doi: "10.1109/iwqos70441.2026.11661141"
url: "unknown"
pdf: "00-inbox/PDFs/2026-IWQoS-PSM__Timely_and_Resource-Efficient_Sketch_Migration_in_Network_Measurement.pdf"
mineru_md: "02-parsed-markdown/2026-IWQoS-PSM__Timely_and_Resource-Efficient_Sketch_Migration_in_Network_Measurement.md"
status: processed
reading_level: L2
research_area: []
task: []
method: []
dataset: []
code: "https://github.com/zxzx2002/Sketch Migration.git"
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

# PSM: Timely and Resource-Efficient Sketch Migration in Network Measurement

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | PSM: Timely and Resource-Efficient Sketch Migration in Network Measurement |
| 中文标题 | PSM：及时且资源高效的网络测量 Sketch 迁移框架 |
| 作者 | Xun Zhou, Hongyan Liu, Xiang Chen, Zhengyan Zhou, Zihao Cheng, Di Wang, Chunming Wu（浙江大学控制科学与工程学院 / 福州大学计算机与数据科学学院 / 浙江大学计算机科学与技术学院） |
| 年份 | 2026 |
| 会议/期刊 | IEEE/ACM IWQoS 2026 |
| 研究方向 | 网络测量（network measurement）/ 可编程数据平面（programmable data plane）——⚠️ 知识库 C 节白名单的 11 个概念页均属加密流量分析领域，本篇无对应 slug，frontmatter 的 research_area/task/method 留空 |
| 任务类型 | Sketch 状态迁移（stateful sketch migration between network measurement points） |
| 方法关键词 | PSM migration protocol、Background Flow (BF) strategy、Mirroring and Recirculation (MR) strategy、bitmap、integrity verification、Intel Tofino2 |
| 数据集 | 无公开数据集；评测使用 4 类常用 sketch（Count-Min、Bloom Filter、MV Sketch、Count Sketch）与 2 个 sketch-based NM 应用（heavy hitter、global iceberg） |
| 是否开源 | 是。论文声明 source code 已发布在 GitHub；解析稿给出的 URL 含空格（见 §7.1 与解析问题说明） |
| PDF | 00-inbox/PDFs/2026-IWQoS-PSM__Timely_and_Resource-Efficient_Sketch_Migration_in_Network_Measurement.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-IWQoS-PSM__Timely_and_Resource-Efficient_Sketch_Migration_in_Network_Measurement.md |

> ⚠️ MinerU 解析问题：§I 第 2 段被 IEEE 版权行（`979-8-3195-1703-6/26/$31.00 ©2026 IEEE`）截断，"Inefficient access to sketch counters" 被拆成两段，语义需自行拼接。
> ⚠️ MinerU 解析问题：参考文献 [15] 的 GitHub 地址含空格（`https://github.com/zxzx2002/Sketch Migration.git`），疑为解析产物；笔记按解析稿原样记录，未做"修正"推断。

---

## 1. 一句话总结

> PSM 用"同列并行的 N+3 字段迁移协议 + BF/MR 两种搬运策略 + bitmap 完整性校验"，把 sketch 迁移做到 Tofino2 上 BF 5ms / MR 30ms，且比三种 SOTA 平均省 25% stage、3% SRAM、10% ALU。

---

## 2. 摘要翻译

### 2.1 摘要原文

> Sketches can achieve resource-efficient and high-accurate network measurement (NM) with configurable resource-performance trade-offs. Due to network dynamics, network measurement points (i.e., the switches deployed with sketches) need to reallocate dynamically to cover full traffic. However, using existing approaches to migrate sketches leads to unacceptable latency and resource overhead. In this paper, we propose PSM, a framework for timely and resource-efficient sketch migration. For timeliness, PSM utilizes a protocol that is able to access sketch counters and migrate them in parallel using background traffic. To ensure migration without direct traffic, we leverage programmable switches' mirroring and recirculation functions to generate packets. For resource efficiency, PSM uses bitmap structures and hardware-friendly computations to track the migration progress and verify integrity. We implement PSM on Intel Tofino2 switches and compare PSM with three state-of-the-art approaches through extensive experiments. Results indicate that PSM achieves timely and resource-efficient sketch migration.

### 2.2 摘要中文翻译

> Sketch 通过可配置的资源-性能权衡，能够以低资源开销实现高精度的网络测量（NM）。由于网络动态性，网络测量点（即部署了 sketch 的交换机）需要动态重新分配以覆盖全部流量。然而，使用现有方法迁移 sketch 会带来不可接受的延迟与资源开销。本文提出 PSM——一个及时且资源高效的 sketch 迁移框架。在及时性方面，PSM 采用一套能够访问 sketch 计数器、并借助背景流量并行迁移它们的协议；为在无直达流量时保证迁移，PSM 利用可编程交换机的 mirroring 与 recirculation 功能自行生成报文。在资源效率方面，PSM 使用 bitmap 结构与硬件友好的计算来跟踪迁移进度并验证完整性。我们在 Intel Tofino2 交换机上实现了 PSM，并通过大量实验与三种 state-of-the-art 方法对比，结果表明 PSM 实现了及时且资源高效的 sketch 迁移。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

Sketch 以并行计数器数组的形式在数据平面低成本地完成 heavy hitter、iceberg 等 NM 任务（§I）。但网络动态性使原有 NMP（network measurement point，即部署 sketch 的交换机）不再覆盖全部流量：例如 ECMP 改变流量分布后，源 NMP 必须把 sketch 计数器"捎带"在包头中送到目的 NMP，才能维持有状态测量结果的连续性（§I、§II-A）。

### 3.2 现有方法的痛点和不足

作者梳理了三类需要迁移的实际场景（sketch 负载均衡、NM 意图变化、链路故障，§II-A），并指出三种已有方案（Swing State、P4Sync、RedPlane）的共同短板（§I、§II-C）：

1. **计数器访问低效**：sketch 本质是并行计数器数组，而 P4Sync 受 public register 设计限制一次只能访问一个计数器，串行迁移导致不及时（§II-C）。
2. **交换机资源消耗高**：P4Sync 用 siphash + RSA 做完整性校验，消耗近一半的交换机计算资源；RedPlane 把计算搬到控制面服务器，却引入控制面与数据面之间数百毫秒级的通信开销（§I、§II-C）。
3. **随机迁移的不完备**：Swing State 随机捎带计数器，导致部分计数器被重复迁移、部分从未迁移，重复与不完备同时损害及时性与完整性（§II-C）。

### 3.3 论文的研究假设或核心直觉

核心直觉：迁移的粒度不必是"单个计数器"，而应是**counter 数组中相同列位置的整列**——把 N 个计数器数组同一位置的 N 个计数器一次性装进包头（PSM 协议 N+3 个字段），即可把"迁移所需报文数"从与 N 成正比降为与数组长度 n 成正比；再配合"一个 bitmap 计数器做迁移索引 + 一个 verification bitmap 记录已更新位置"的硬件友好结构，可以不加控制面地完成完整性验证（§III-A、§III-B、§III-C、§III-F）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 网络动态（ECMP 负载均衡、NM 意图变化、链路故障）使原 NMP 无法覆盖全部流量，必须迁移有状态 sketch | §II-A、Fig. 1 |
| 痛点提炼 | 迁移的及时性与交换机资源开销不可兼得：串行访问慢、siphash/RSA 占近半计算资源、控制面方案引入数百毫秒延迟 | §I、§II-C |
| 问题转化 | 如何在**纯数据平面内**并行携带 sketch 计数器，并以极低资源代价跟踪进度、验证完整性？ | §III（含推断：论文未显式给出形式化问题定义） |
| 文献定位 | 迁移任务由 Swing State 首次在 SDN 提出，P4Sync 把随机迁移改进为顺序迁移并做完整性校验，RedPlane 走控制面 + 中间服务器；三者均未解决"并行 + 数据面校验"的组合 | §II-C |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 若按 counter 数组"同列"并行装入包头（N+3 字段协议），并用单计数器 bitmap 跟踪迁移索引、verification bitmap + recirculation 验证完整性，则可同时取得低迁移延迟与低交换机资源占用 | §III-A～§III-F | Intel Tofino2 双交换机实测，对比 SS/PS/RP |
| 辅助假设（如有） | 无背景流量时，交换机可利用自身 mirroring + recirculation 生成迁移报文（MR 策略），使迁移不依赖外部流量 | §III-E | 无背景流量场景下实测 MR 策略延迟 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | BF 策略 5ms 完成迁移；资源上 PSM 比三种 SOTA 平均减少 25% stage、3% SRAM、10% ALU；完整性校验仅 340ns/计数器 | §IV-B (Exp#1, Exp#4, Exp#5)、Table I、Table II |
| 辅助假设 | 支撑 | 无背景流量时 MR 策略将整体迁移延迟维持在 30ms，而 BF 类方法在无背景流量场景无法工作 | §IV-B (Exp#1)、Fig. 7 |

---

## 4. 方法设计

### 4.1 方法整体流程

PSM 把 sketch 迁移建模为"按列搬运"：源 NMP 每收到一个可用报文（背景流量或被镜像/回环的控制包），就读取当前迁移索引、并行读取所有 N 个 counter 数组在该索引处的值、写入包头 PSM 协议字段后发往目的 NMP；目的 NMP 据此更新本地 sketch 并在 verification bitmap 中标记该位置已更新。迁移完成后由交换机内部 recirculation 逐位核对 bitmap，未被更新的位置索引随包头送回源 NMP 触发二次迁移（§III-A、§III-D、§III-F）。

### 4.2 详细 Pipeline

以 BF（Background Flow）策略为主线（§III-D、Fig. 5）：

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | 正常业务包到达源 NMP | 读取交换机内部 timestamp（用于后续计算迁移耗时） | 带内部时间的包 | 为延迟测量埋点 |
| Step 2 | 同上 | 在源 NMP 内复制该包；原包按原逻辑转发 | 原包 + 副本包 | 不影响正常转发 |
| Step 3 | 副本包 | 访问单计数器 bitmap，取值并 +1，得到当前迁移列索引 | 迁移索引 j | 跟踪迁移进度（§III-C） |
| Step 4 | 迁移索引 j | 以 j 并行访问 N 个 counter 数组，取值写入包头 PSM 协议的 N 个 load sketch 字段 | 携带整列计数器值的包 | 并行迁移，降低报文用量 |
| Step 5 | 同上 | 判断迁移是否结束（索引是否等于数组长度 n）；结束则置 if finish=1 | PSM 协议包 | 触发目的端完整性校验 |
| Step 6 | PSM 协议包到达目的 NMP | 更新本地 counters，并更新 verification bitmap 记录已更新位置 | 更新后的目的端 sketch | 状态同步 |
| Step 7 | 迁移结束后的交换机内部包 | recirculation 逐位检查 verification bitmap，未更新位置索引写入包头后送回源 NMP | 缺失位置列表 | 触发二次迁移（§III-F） |

MR（Mirroring and Recirculation）策略流程相近，区别在于用控制包触发、由交换机 mirror 副本并把镜像包送到端口 0 做 recirculation（在 ingress 端口 128 被捕获），通过入端口过滤区分镜像包与正常包（§III-E、Fig. 6）。

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| PSM migration protocol | 承载迁移载荷的包头格式，含 N+3 字段：proto id、read place id、N 个 load sketch、if finish | 整列 counter 值 + 迁移索引 | 可被目的 NMP 解析的协议包 | 协议被 BF 与 MR 两种策略共用（§III-B、Fig. 4） |
| Migration Position Lookup | 单计数器 bitmap 充当迁移索引，包到达即取值 +1 | 到达包 | 当前迁移列索引 j | 为 BF/MR 提供统一迁移顺序（§III-C） |
| BF strategy | 用背景流量复制包捎带计数器 | 正常业务流 | 携带 sketch 的副本包 | 有稳定背景流量时的默认策略（§III-D） |
| MR strategy | 用 mirroring + recirculation 自造迁移包 | 控制包 | 经端口 0 回环的镜像包 | 无背景流量时的替代策略（§III-E） |
| Integrity verification | 目的端 verification bitmap + 内部 recirculation 逐位核对，缺失索引回传源端二次迁移 | verification bitmap | 缺失位置索引列表 | 迁移收尾阶段，保障完整性（§III-F） |

### 4.4 公式、算法和机制解释

- **迁移的形式化描述**（§II-B）：sketch 存放在 N 个等长（长度 n）并行计数器数组 $R_1,\ldots,R_N$ 中，$R_{ij}$ 为数组 $R_i$ 的第 j 个位置；迁移是周期性事件，需把 $\forall i\in[1,N], j\in[1,n]$ 的 $R_{ij}$ 从源 NMP 搬到目的 NMP。
- **并行搬运机制**：PSM 协议一次携带"同一 j 的全部 i"（即整列），因此迁移报文开销 $N_p/n$ 与数组个数 N 解耦（§III-B；Exp#2 中 N=3 时 PS/RP 的报文用量是 PSM 的 3 倍）。
- **硬件约束的处理**：Intel Tofino2 对计数器访问有限制，因此完整性校验被安排在包 recirculation 过程中进行——每轮 recirculation 检查 bitmap 中一个计数器，检查完毕的包被送回源 NMP 触发二次迁移（§III-F）。
- **为何不用控制面**：作者给出"稻草人方案"对比——用 gRPC 让控制面记录进度、校验完整性需要数百毫秒级控制面-数据面通信延迟，与 NM 的及时性要求冲突，因此 PSM 的校验完全在数据平面内实现（§III-F）。

### 4.5 方法优势

1. **及时**：BF 5ms、MR 30ms 完成迁移，PS 需 3 倍于 BF 的时间，RP 达秒级（§IV-B Exp#1）。
2. **省资源**：相对三种 SOTA 平均减少 25% stage、3% SRAM、10% ALU；相比"只含 sketch"的程序仅多占 1.2–1.6 个 stage、3.75% ALU（§IV-B Exp#4、Table I）。
3. **通用**：BF 与 MR 覆盖"有/无背景流量"两类部署场景，拓展了可迁移的适用范围（§III-E）。
4. **完整性可验证**：bitmap + recirculation 以 340ns/计数器的代价完成校验，且不需控制面参与（§IV-B Exp#5、Table II）。

### 4.6 方法不足

1. **仍会损失 NM 效果**：受迁移延迟与不完备性影响，迁移后 heavy hitter / global iceberg 的 recall、F1、RE 较"理想 sketch"（Ideal）仍有下降（§IV-B Exp#3、Fig. 9）。
2. **依赖 Tofino2 特性**：MR 策略依赖 Intel Tofino2 的 mirroring/recirculation 与端口布置（镜像包送端口 0、ingress 端口 128 捕获），可移植到其他可编程流水线需重新适配（§III-E）。
3. **协议字段与数组个数耦合**：包头需携带 N 个 load sketch 字段，N 越大包头越长；实验只验证了 N=3 的配置（§IV-A）。
4. **实验规模有限**：仅两台交换机、10Gbps 链路、DPDK-Pktgen 生成的背景流量，未在真实骨干网或大规模拓扑中验证（§IV-A）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

已有三类方案的迁移机制分别是"随机（SS）—串行单计数器（PS）—控制面中转（RP）"；PSM 的本质区别是把迁移单位从"计数器"提升为"counter 数组的整列"，并把完整性校验从"siphash/RSA 或控制面顺序号"替换为"bitmap + 数据平面 recirculation"。因此 PSM 的报文用量与数组个数无关，且校验不离开数据平面（§II-C、§III-A）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 同列并行迁移协议 | N+3 字段的 PSM 协议按 counter 数组同一位置并行携带 N 个计数器，N=3 时报文用量仅为 PS/RP 的 1/3 | 高 | 是（任何并行计数器结构的状态同步） |
| BF / MR 双策略 | 有背景流量走 BF（复制业务包），无背景流量走 MR（mirroring + recirculation 自造包，端口 0 ↔ 端口 128 回环） | 高 | 部分（MR 依赖 Tofino2 特性） |
| bitmap 进度跟踪 | 单个计数器 bitmap 充当迁移索引，避免复杂的位置维护逻辑 | 中 | 是 |
| 数据平面完整性校验 | verification bitmap + 包内 recirculation 逐位核对，340ns/计数器，无需控制面 | 高 | 是 |
| 二次迁移机制 | 未更新位置索引回传源 NMP 触发补迁，保证最终完整 | 中 | 是 |

### 5.3 适用场景

- 数据中心 / 可编程交换机网络中，因 ECMP 重分布、NM 意图变更或链路故障需要搬迁有状态 sketch 的场合（§II-A）。
- 源、目的 NMP 之间有稳定业务流量的场景（BF 策略最优，5ms）。
- 源、目的 NMP 之间无背景流量的场景（MR 策略，30ms；这是 SS/PS/RP 均无法工作的场景，§III-E、§IV-B）。
- **不适用**：需要跨管理域、跨厂商可编程流水线迁移的场景（依赖 Tofino2 专有特性）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| Swing State (SS) [10] | 首次提出 SDN 中的状态迁移；实现简单 | 随机迁移导致重复/遗漏，overhead=1 时完整度仅 63%，完整迁移需 10 倍以上于 PSM 的报文 | 以"按列 + 索引"消除随机性 |
| P4Sync (PS) [11] | 顺序迁移 + siphash/RSA 完整性校验，可应对丢包 | 一次只能访问一个计数器；siphash/RSA 消耗近半计算资源；耗时约为 BF 的 3 倍、报文用量 3n | 并行整列迁移；以 bitmap 校验替代密码学校验 |
| RedPlane (RP) [12] | 控制面 + 中间服务器，容错性强 | 控制面-数据面通信引入数百毫秒延迟，整体达秒级；报文用量 3n | 校验完全下沉到数据平面 |
| **PSM（本文）** | BF 5ms / MR 30ms；平均省 25% stage、3% SRAM、10% ALU；校验 340ns | 迁移后 NM 应用效果仍略低于 Ideal；依赖 Tofino2 特性；仅验证 N=3 | — |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **测试床**：两台 32×100Gbps Intel Tofino2 交换机分别作为源/目的 NMP；两台服务器（36 核 Intel Xeon Gold 6240C @2.60GHz、128GB RAM）；源侧服务器用 DPDK-Pktgen 25.03.0 打压背景流量，另一台抓包解析；设备间为 10Gbps 链路（§IV-A）。
- **时序测量**：包进入源交换机 ingress 与离开目的交换机 egress 时分别打纳秒级时间戳，接收端解析两时间戳相减得到整体迁移延迟（§IV-B Exp#1）。

### 6.2 数据集

本文不使用流量分类数据集，评测对象为 **4 类常用 sketch**：Count-Min (CM)、Bloom Filter (BL)、MV Sketch (MV)、Count Sketch (CS)，配置参照文献 [25]（MTP）的设置；PSM 协议的可调参数 N 设为 3 以匹配四类 sketch 结构（§IV-A）。NM 应用层使用 **heavy hitter (HH)** 与 **global iceberg (GI)** 两个真实 sketch-based 应用作为效果评测载体（§IV-B Exp#3）。

### 6.3 Baseline

- **SS（Swing State）**：随机迁移，报文开销按文献 [11] 的理论分析结果折算（§IV-B Exp#2）。
- **PS（P4Sync）**：串行迁移 + siphash/RSA 校验。
- **RP（RedPlane）**：控制面中转迁移。
- **Ideal**：不做迁移、直接使用原始 sketch 的参照基线（§IV-B Exp#3）。
- BF 与 MR 因迁移期报文开销相同，Exp#2 中合并记为 "PSM"（§IV-B）。

### 6.4 评价指标

迁移延迟（ns/ms 级时间戳差）、迁移报文开销 $N_p/n$、迁移完整度（completeness）、NM 应用效果（recall / F1 / relative error, RE）、交换机硬件资源占用（Stage、SRAM、ALU、VLIW）（§IV-B、Table I、Table II）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| 迁移延迟（4 类 sketch） | 延迟 | BF 5ms；MR 30ms | PS ≈ 3× BF 时间；RP 秒级 | 最快 | SS 平均需 11 倍数组长度的报文（§IV-B Exp#1、Fig. 7） |
| 迁移报文开销 | $N_p/n$ | PSM：完整迁移所需报文为基数 | PS/RP = 3× PSM | 3 倍效率 | SS：overhead=1 时完整度 63%，overhead=3 时 95%，完整迁移需 >10× PSM（§IV-B Exp#2、Fig. 8） |
| HH / GI 应用效果 | recall / F1 / RE | PSM | SS/PS/RP | recall +8%、F1 +5%、RE −8% | 迁移必然导致效果下降，RP 因更新不及时下降最明显（§IV-B Exp#3、Fig. 9） |
| 硬件资源占用 | Stage / SRAM / ALU / VLIW | PSM-BF 4.6 / 7.70 / 10.00 / 3.45；PSM-MR 4 / 7.81 / 8.33 / 2.50 | PS 9 / 9.78 / 14.95 / 5.06 | 平均 −25% stage、−3% SRAM、−10% ALU | "Only Sketch" 基线为 3.4 / 0.73 / 6.25 / 2.08；PSM 仅多占 1.2–1.6 stage（§IV-B Exp#4、Table I） |
| 完整性校验 | 延迟 / 报文 / stage / VLIW | 340.0 ns / 1 / 2 / 4.69% | PS 440.8 ns / 3n / 2 / 6.25% | VLIW −1.56% | Table II 另有一行 "Optimization"（100.8 ns / 3n-1 / 0 / 1.56%），解析稿正文未说明其含义 |

### 6.6 优势最明显的场景

无背景流量场景是 PSM 的独占优势区间：此时 BF 类方法与 SS/PS/RP 均无法工作，PSM 的 MR 策略仍能以 30ms 完成迁移（§IV-B Exp#1）。此外，在 stage 资源紧张的交换机上，PSM 仅额外占用 1.2–1.6 个 stage（对比 PS/RP 的 4.6–5.6 个，而交换机总共 12 个 stage），避免了"迁移程序挤占其他网络功能"的问题（§IV-B Exp#4）。

### 6.7 局限性

- 迁移后的 sketch 与 Ideal 仍有差距：延迟导致更新不及时、不完备导致内容缺失（§IV-B Exp#3）。
- 实验参数 N 固定为 3，协议在更多 counter 数组（更大 N）下的包头开销未评测（§IV-A）。
- 未讨论迁移期间的一致性语义（如目的端在部分迁移状态下被查询时结果的正确性边界），解析稿未见相关分析。
- 安全维度未展开：迁移报文若被伪造或篡改，bitmap 校验只能发现"缺失"而非"错误值"，解析稿未做对抗性讨论。

---

## 7. 学习与应用

### 7.1 是否开源？

论文声明 source code 已发布在 GitHub（§I 末段、参考文献 [15]）。解析稿给出的地址为 `https://github.com/zxzx2002/Sketch Migration.git`（含空格，疑为解析产物，未做修正推断；知识库若登记请以核实后的真实地址为准）。故本笔记 frontmatter 的 `code` 字段按解析稿原样记录。

### 7.2 复现关键步骤

1. 在 Tofino2（SDE）中实现 PSM 协议头解析/改写与 N 个 counter 数组的并行读（对应 §III-B、§III-C）。
2. 部署 BF 策略：ingress 复制业务包 → 读 bitmap 索引 → 并行读整列计数器 → 写包头 → 转发（§III-D）。
3. 部署 MR 策略：控制包触发 → mirror → 镜像包送到端口 0 回环、在 ingress 端口 128 捕获并过滤 → 循环直至迁移完成（§III-E）。
4. 目的端实现 verification bitmap 更新与迁移结束后的内部 recirculation 逐位校验，缺失索引回传源端触发二次迁移（§III-F）。
5. 用 DPDK-Pktgen 或等价工具构造背景流量，按 §IV-A 的测试床拓扑测量迁移延迟、报文开销与资源占用。

### 7.3 关键超参数、预处理和训练细节

- PSM 协议参数 N = 3（与评测的四类 sketch 结构匹配，§IV-A）；协议字段共 N+3 个（§III-B）。
- 迁移粒度：按 counter 数组列位置逐个推进，索引上限为数组长度 n（§III-C）。
- 评测使用的四类 sketch 配置与 NM 应用参数参照文献 [25]（MTP 的设置）（§IV-A、§IV-B）。
- MR 策略的端口约定：镜像包送端口 0 回环、ingress 端口 128 捕获（§III-E）。
- 无训练过程（非学习方法）。

### 7.4 能否迁移到其他任务？

可迁移点主要在"数据平面内的有状态结构同步"这一类问题上：同列并行携带的状态迁移协议可推广到其他并行计数器结构（如 Count-Min 之外的 sketch 变体、寄存器组）；bitmap + recirculation 的完整性校验模式可复用于任何需要在数据平面内校验状态一致性的场景（如分布式测量任务的状态交接）。但对加密流量分类任务本身无直接方法贡献；若知识库关注"网内测量基础设施"主题，本文可作为 sketch 部署与运维层面的支撑引用。

### 7.5 对我的研究有什么启发？

1. **状态可比性视角**：PSM 指出"sketch 是有状态的、计数器累积值不可丢弃"（§II-A），这与流量分析中"概念漂移需要模型适应"的问题同构——基础设施层面的状态延续性也是测量正确性的前提。
2. **数据平面内做校验的设计哲学**：用 bitmap 这种极简结构与硬件友好的逐位计算替代密码学/控制面方案，提示在流量分析的数据平面部署上应优先考虑"每 stage 可完成的简单计算"。
3. **评测指标设计**：把"迁移方案"对上层 NM 应用效果的折损（recall/F1/RE，§IV-B Exp#3）纳入评测，而不仅看迁移本身的延迟——这种"端到端效果 + 基础设施开销"双层评测值得借鉴。

---

## 8. 总结

### 8.1 核心思想

> 按 counter 数组整列并行捎带，bitmap 校验完整性。

### 8.2 速记版 Pipeline

1. 判定迁移场景（负载均衡 / 意图变化 / 链路故障），确认源-目的 NMP。
2. 源 NMP 取包（背景流量或控制包触发），读单计数器 bitmap 得到迁移列索引并 +1。
3. 按索引并行读取 N 个 counter 数组的整列值，写入包头 N+3 字段的 PSM 协议。
4. 目的 NMP 解析并更新本地 counters 与 verification bitmap；迁移完成时置 if finish。
5. 交换机内 recirculation 逐位核对 bitmap，缺失索引回传源端做二次迁移。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- 无：本篇为网络测量 / 可编程数据平面主题，知识库 C 节白名单的 11 个概念页（均为加密流量分析领域）无对应页面（不做越权链接）。

### 9.2 相关方法

- 无：白名单方法页（transformer、graph-neural-network、pre-training-finetuning 等）与数据平面 sketch 机制无对应。

### 9.3 相关任务

- 无：白名单任务页无 "network measurement / state migration" 对应项。

### 9.4 可更新的综述页面

- 无：白名单综述页均为加密流量分析 / WF / 恶意流量方向，本篇不适合加入。

### 9.5 可加入的对比表

- [[open-source-registry]]（论文声明开源，可登记代码仓库；注意 URL 解析问题见 §7.1）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 三类迁移场景（sketch 负载均衡、NM 意图变化、链路故障）构成迁移需求的现实动机 | 场景描述与 heavy hitter 阈值示例 | §II-A |
| 现有方案的三类缺陷：随机迁移重复/遗漏、串行访问慢、siphash/RSA 占近半计算资源、控制面数百毫秒延迟 | 对 SS/PS/RP 的逐一分析 | §II-C |
| 并行整列迁移把报文开销与数组个数 N 解耦：N=3 时 PS/RP 报文用量为 PSM 的 3 倍 | Exp#2 结果与 $N_p/n$ 定义 | §IV-B (Exp#2)、Fig. 8 |
| PSM 达成 5ms（BF）/ 30ms（MR）迁移延迟，RP 为秒级 | 纳秒时间戳差测量 | §IV-B (Exp#1)、Fig. 7 |
| 迁移使 NM 应用效果下降，PSM 相比 SOTA 提升 recall 8%、F1 5%、降低 RE 8% | HH/GI 两应用的四 sketch 评测 | §IV-B (Exp#3)、Fig. 9 |
| PSM 平均减少 25% stage、3% SRAM、10% ALU；相对 only-sketch 仅多占 1.2–1.6 stage、3.75% ALU | 编译日志统计（12 stage 总量） | §IV-B (Exp#4)、Table I |
| 完整性校验 340ns/计数器、1 个报文、4.69% VLIW，优于 PS 的 440.8ns/3n 报文/6.25% VLIW | 目的交换机 ingress-egress 时间戳 | §IV-B (Exp#5)、Table II |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-IWQoS-PSM__Timely_and_Resource-Efficient_Sketch_Migration_in_Network_Measurement.pdf
- MinerU Markdown：02-parsed-markdown/2026-IWQoS-PSM__Timely_and_Resource-Efficient_Sketch_Migration_in_Network_Measurement.md

---

## 12. 后续问题

- 迁移期间目的 NMP 的 sketch 处于"部分更新"状态，若此时 NM 应用读取会产生什么错误界？解析稿未讨论。
- PSM 协议中 N 个 load sketch 字段的位宽如何随 sketch 类型（CM 计数 vs Bloom 位）适配？解析稿只给了 N=3 的整体配置。
- 迁移包若遭遇丢包/乱序，bitmap 校验可发现"缺失"，但能否发现"值被篡改"？安全语义未展开。
- BF 与 MR 的切换是否需要人工/控制器介入，切换本身有无额外开销？解析稿未明确。
- Table II 中 "Optimization" 一行的含义（100.8ns / 3n-1 报文 / 0 stage）在正文中缺少解释，需查原文图注确认。

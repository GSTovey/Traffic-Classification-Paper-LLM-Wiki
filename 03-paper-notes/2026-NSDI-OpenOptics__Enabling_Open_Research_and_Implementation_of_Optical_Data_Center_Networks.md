---
type: paper
title_original: "OpenOptics: Enabling Open Research and Implementation of Optical Data Center Networks"
title_cn: ""
authors: ["Yiming Lei", "Federico De Marchi", "Jialong Li", "Raj Joshi", "Shu-Ting Wang", "Xiaoqi Chen", "Balakrishnan Chandrasekaran", "Yiting Xia"]
year: 2026
venue: NSDI
doi: unknown
url: "https://www.usenix.org/conference/nsdi26/presentation/lei-optical"
pdf: "00-inbox/PDFs/2026-NSDI-OpenOptics__Enabling_Open_Research_and_Implementation_of_Optical_Data_Center_Networks.pdf"
mineru_md: "02-parsed-markdown/2026-NSDI-OpenOptics__Enabling_Open_Research_and_Implementation_of_Optical_Data_Center_Networks.md"
status: deep-analyzed
reading_level: L3
research_area: ["optical data center networks", "programmable switches", "network systems"]
task: ["optical DCN implementation", "network architecture evaluation"]
method: ["time-flow table", "unified Python APIs", "calendar-queue scheduling", "queue occupancy estimation", "optical-fabric emulation"]
dataset: ["Memcached/Memslap", "Gloo allreduce", "iperf3", "RPC/Hadoop/KV-store traces"]
code: "yes (paper states open source; exact repository URL not listed in parsed text)"
relevance: medium
created: "2026-09-29"
updated: "2026-10-10"
---

# OpenOptics: Enabling Open Research and Implementation of Optical Data Center Networks

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | THE ADVANCED COMPUTING SYSTEMS ASSOCIATION |
| 年份 | 2026 |
| 会议/期刊 | NSDI |
| PDF | [[2026-NSDI-OpenOptics__Enabling_Open_Research_and_Implementation_of_Optical_Data_Center_Networks.pdf]] |
| MinerU Markdown | [[2026-NSDI-OpenOptics__Enabling_Open_Research_and_Implementation_of_Optical_Data_Center_Networks.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
Optical data center networks (DCNs) are emerging as a promising design for cloud infrastructure. However, existing optical DCN architectures operate as closed ecosystems, tying software solutions to specific optical hardware. We introduce OpenOptics, an open research and development framework that decouples software from hardware, allowing them to evolve independently. OpenOptics features: (1) a time-flow table abstraction as a common interface between optical hardware and software, (2) a unified workflow and user-friendly API for implementing various optical DCNs with simple Python scripts, and (3) a backend system that re architects queue management to support the time-flow tables and provides rich infrastructure services for diverse applica tions. Built on programmable switches, OpenOptics achieves a record-breaking minimum optical circuit duration of 2 µs using commodity devices. We validate OpenOptics’ generality by implementing six optical architectures and seven routing schemes on an optical testbed and conducting benchmarks on a 108-ToR setup, showcasing its efficiency. Additionally, case studies highlight novel research opportunities enabled by OpenOptics.

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
- 主题线索：tor, quic。
- 摘要证据：Optical data center networks (DCNs) are emerging as a promising design for cloud infrastructure. However, existing optical DCN architectures operate as closed ecosystems, tying software solutions to specific optical hardware. We introduce OpenOptics, an open research and development framework that decouples software from hardware, allowing them to evolve independently. OpenOptics features: (1) a time-flow table abstraction as a common interface between optical hardware and software, (2) a unified workflow and user-friendly API for implementing various optical DCNs with simple Python scripts, and (3) a backend system that re architects queue management to support the time-flow tables and provides rich infrastructure services for diverse applica tions. Built on programmable switches, OpenOptics achieves a record-breaking minimum optical circuit duration of 2 µs using commodity devices. We validate OpenOptics’ generality by implementing six optical architectures and seven routing schemes on an optical testbed and conducting benchmarks on a 108-ToR setup, showcasing its efficiency. Additionally, case studies highlight novel research opportunities enabled by OpenOptics.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
Queue occupancy estimation accuracy. The error of queue occupancy estimation (§5.2) is the difference between our estimated queue occupancy (EQO) from the ingress pipeline and the ground-truth queue occupancy read by an egress packet. We measure it with the above setting (in Fig. 11) but combine line-rate traffic and bursty traffic to fill and drain the queue periodically. The estimation accuracy increases with the update interval (Fig. 12). We find 50 ns draws a good balance between the estimation accuracy and the consumption of pipeline processing resources on the ToR. The estimation error is within 725 B, less than half MTU-size packet, and the packet generator sends one packet every 50 ns (or at 20 Mpps), which creates only 1.3% pipeline forward overhead on Tofino2 with 1.5 Bpps processing capacity. Minimum time slice duration. We derive the minimum achievable time slice duration in OpenOptics to evaluate its generality to support various optical proposals. To ensure a duty cycle above 90%, the slice duration is typically set to at least 10× the guardband, which covers the maximum of circuit reconfiguration and unavoidable system delays, preventing data loss. This analysis focuses on system limits, assuming OCS hardware is not a limiting factor, and asks what time slice duration OpenOptics can achieve in that case. The 34 ns queue rotation variance (Fig. 11) should be covered by the guardband. In addition, the queue occupancy estimation error of 725 B (Fig. 12) translates to 58 ns delay under 100 Gbps bandwidth, meaning packets may get impacted by false negatives for 58 ns, where a full queue is mistakenly seen as not full. Besides, our synchronization work shows up to 15 ns sync errors in a 108-ToR optical DCN [30], which requires a guardband of 15 × 2 = 30ns for c

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


## 深度分析（并行深度分析更新 2026-09-29）

### 方法、实验与证据
OpenOptics提供光数据中心网络的开放研究与实现框架，含调度、拥塞检测及pushback机制；MinerU文本显示HOHO在拥塞下易过载，pushback作为补救。具体硬件和端到端指标需继续核对。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。


## 深度分析（L3 补充，2026-10-09）

### 3. 研究问题、动机与证据边界

#### 3.1 研究问题

论文把问题定义为：如何为具有不同光交换机结构、重配置粒度和路由策略的光数据中心网络提供一个可复用的端到端系统栈，使软件系统能够独立于光硬件演进，同时保留足够真实的交换机、主机和队列行为。作者指出，现有光 DCN 往往是硬件、控制器、队列管理和路由协议一起定制的封闭生态，研究者难以在不同架构之间复用实现和进行公平比较（§1）。

#### 3.2 问题发现路径

| 阶段 | 内容 | 证据 |
|---|---|---|
| 现象观察 | OCS 是无缓冲的物理层器件，电端点必须按电路可用时间发送和缓存数据；不同光 DCN 方案采用不同控制循环与路由粒度 | §1、§2.1 |
| 工程痛点 | 软硬件紧耦合导致每个方案都要重建系统；既有模拟器没有原生光 DCN 支持，小规模仿真平台最多约 8 个 ToR、10 Gbps | §1 |
| 科学/系统问题 | 需要一个类似传统网络 IP “窄腰”的公共接口，能够表达时间变化的拓扑和跨时间片路由，同时兼容普通流表 | §1、§2.2、§3 |
| 设计答案 | 用到达时间片作为匹配字段、离开时间片作为动作字段的 time-flow table，配合统一编程模型与可编程队列管理 | §3–§5 |

#### 3.3 核心假设及验证状态

| 假设 | 内容 | 验证方式 | 结论边界 |
|---|---|---|---|
| H1 | time-flow table 足以统一 TA、TO 和混合型光 DCN 的路由表达 | 实现 c-Through、Jupiter、Mordia、RotorNet、Opera 及 UCMP/HOHO 等路由 | 证明了表达能力和可运行性；不等于覆盖所有未来 OCS 物理约束（§3、§6） |
| H2 | 以 P4 重构日历队列、暂停/恢复队列和数据面队列占用估计可以支撑微秒级时间片 | Tofino2/OCS testbed、108-ToR benchmark | 论文报告系统上限，不是所有交换芯片的保证（§5、§7） |
| H3 | 同一套 API 和后端能降低跨架构比较与原型实现成本 | 三类 use case、Mininet/BMv2 仿真与真实/仿真 OCS 对照 | 主要以趋势复现和组件测试验证，部分对照工作本身是专有或仅部分实现（§6） |

### 4. 方法设计

#### 4.1 总体流程

用户用静态 JSON 描述设备、端口、OCS 结构、重配置延迟和时间片，再用 Python API 描述拓扑、路由及监控指标。OpenOptics 将拓扑算法编译为 OCS 端口连接，将路由路径分解为各端点的 time-flow table 条目；运行时由可编程交换机/NIC 的日历队列按离开时间片缓存和释放报文。TA 网络周期性收集 traffic matrix 并重新优化拓扑，TO 网络预加载时间片调度，混合网络可以在不同层级分别采用两种流程（§4.1–§4.3）。

#### 4.2 Pipeline

| 步骤 | 输入 | 处理 | 输出 | 证据 |
|---|---|---|---|---|
| 1. 硬件/时间配置 | OCS 结构、端口数、重配置延迟、时间片 | 建立网络对象并校验电路可行性 | 设备与时间配置 | §4.1、Table 1 |
| 2. 拓扑生成 | traffic matrix 或 round-robin 参数 | `topo()` 生成 TA/TO/自定义电路 | 每个时间片的 Circuit 集合 | §4.2 |
| 3. 路由计算 | Circuit、源/目的、时间片 | direct/ECMP/WCMP/kSP 或 VLB/Opera/UCMP/HOHO | Path 集合 | §4.2 |
| 4. 编译与部署 | Path、LOOKUP/MULTIPATH 选项 | 生成逐跳或源路由条目，并映射到 OCS 物理端口 | time-flow table 和 OCS 配置 | §3、§4.2 |
| 5. 时间调度 | 到达时间片、离开时间片 | 按日历队列入队，时间片边界暂停/恢复队列 | 延迟发送的报文 | §5.1 |
| 6. 拥塞/遥测 | 队列入队事件和定时数据面包 | 寄存器估计队列占用，触发延后、丢弃或 pushback | 拥塞反应与 TM/缓冲/链路指标 | §5.2、Appendix A/B |

#### 4.3 关键模块与机制

- **Time-flow table**：到达时间片是 match field，离开时间片是 action field；二者设为 wildcard 时退化为传统 flow table。它可以表达直接等待、跨时间片多跳、静态 TA 路由和源路由（§3）。
- **统一 API**：`connect/topo/deploy_topo` 负责拓扑，`routing/neighbors/earliest_path/deploy_routing` 负责路由，`collect/buffer_usage/bw_usage` 负责监控。TA 和 TO 通过不同参数组合进入同一工作流（§4.2）。
- **日历队列**：每个 egress port 为时间片分配循环队列；报文根据 `departure_ts-arrival_ts` 得到 rank，未来时间片的队列保持 paused，到达目标片时由数据面 packet generator 触发旋转（§5.1）。
- **队列占用估计**：ingress register 在入队时累加字节，packet generator 以固定间隔按带宽×间隔估计出队量。队列满的判定取“可在剩余时间片发送的数据量”和拥塞阈值两者中更早触发者（§5.2、Appendix A）。
- **基础设施服务**：flow aging、libvma 流暂停/恢复、buffer offloading、拥塞检测与 traffic pushback 为不同光架构复用的辅助模块（§5.2、Appendix A/B）。
- **仿真层**：P4 可编程交换机模拟 OCS 的电路开关，BMv2/Mininet 提供无物理设备时的全流程仿真；断路时间片通过查表不匹配而丢弃报文，重配置延迟作为特殊时间片建模（§5.3）。

#### 4.4 机制约束

time-flow table 只抽象影响连通性的“电路开/关”，不刻画器件 bit error rate、插入损耗和串扰；论文假定所接入 OCS 已满足物理层正确运行条件（§3）。队列占用估计依赖 line-rate dequeue 假设，且 packet generator 会消耗少量 ingress pipeline 资源（§5.2、§7）。

### 5. 与已有方法的本质区别

| 对象 | 传统做法 | OpenOptics 的变化 | 证据 |
|---|---|---|---|
| 路由抽象 | 每个架构自定义流表/控制器 | 以时间为一等字段的公共表项，兼容普通流表 | §3 |
| 编程方式 | 手工配置低级 OCS 和流表 | Python 高层 API 编译到设备配置 | §4 |
| 队列管理 | 优先级队列或静态流表 | 由时间片驱动的日历队列、暂停/恢复 | §5.1 |
| 实验平台 | 架构专用模拟器、小规模主机模拟 | 真实 OCS、Tofino2、P4 OCS 仿真和 Mininet 同一接口 | §5.3、§6–§7 |

创新主要是系统抽象和可复用实现，贡献度为高；它不是一种新的拥塞控制或路由最优算法。迁移价值集中在光 DCN 系统研究、可编程交换机调度和跨层实验复现。

### 6. 实验设计、数据与结果

#### 6.1 真实 testbed 与工作负载

Testbed 包含 Polatis Series 6000 MEMS OCS、4 台 EdgeCore DCS810 Intel Tofino2、4 台带 Mellanox ConnectX-5 双口 100 Gbps NIC 的服务器。两台 Tofino2 划分为 8 个逻辑 ToR，第三台模拟可变 OCS 结构，第四台作为电网络；每个 ToR 通过 400 Gbps 链路连到 OCS/电网络，并通过 4×100 Gbps 连到仿真光网络（§6）。Memcached/Memslap 代表 mice 延迟流，Gloo ring allreduce（800 KB–20 MB）代表 elephant 吞吐流。大规模 benchmark 在 108-ToR Opera 结构上回放 RPC、Hadoop、KV-store trace，并将核心链路利用率缩放到 40%（§7）。

#### 6.2 关键结果

| 实验 | 指标与结果 | 证据与边界 |
|---|---|---|
| 架构比较 | c-Through/Jupiter/Mordia、RotorNet/Opera、Clos 的 FCT 趋势与先前工作一致；UCMP 降低 RotorNet 的 FCT；TO 架构 elephant FCT 约为 Clos 的两倍，因电路仅半时可用 | Fig. 8、§6 Case I；趋势复现，不是逐点数值复现 |
| 传输层 | Clos 的 iperf3 约 40 Gbps（CPU 上限）；direct-circuit 约为其一半；调高 TCP dupack threshold 至 5 后混合 RotorNet 接近预期 25 Gbps | Fig. 9、§6 Case II |
| OCS 参数 | VLB 对时间片长度敏感；UCMP 降低敏感性，100 µs 与 200 µs 差异小，2 µs 下更易错过计划时间片 | Fig. 10、§6 Case III |
| 时间精度 | ToR-to-ToR 延迟 1287–1324 ns，方差 34 ns；50 ns 更新间隔下 EQO 误差 ≤725 B，packet generator 约 1.3% pipeline forward overhead | Fig. 11–12、§7 |
| 最小时间片 | 34 ns 延迟方差 + 58 ns EQO 转换延迟 + 30 ns 同步误差，作者加入余量后设 200 ns guardband，得到 2 µs 最小时间片；实验中未观察到丢包 | §7；依赖给定 Tofino2/OCS/同步条件 |
| 资源占用 | 108-ToR observed ToR 上 SRAM 3.8%、TCAM 2.3%、stateful ALU 9.4%、ternary Xbar 13.8%、VLIW 5.6%、exact Xbar 7.8% | Table 2、§7 |
| 缓冲与拥塞 | 300 µs 时间片下 VLB 最大 12.78 MB，低于 Tofino2 64 MB；70% 核心利用率 stress test 中同时启用检测和 pushback 可将 HOHO/Opera/UCMP 的丢包降至 0 | Appendix A/B、Table 3–4 |

#### 6.3 证据边界与局限

1. 108-ToR 是“代表性 ToR + 六条 100 Gbps 链路”的 full-scale time-flow table/仿真网络，不是 108 个完整物理 ToR；规模结论应理解为配置和数据面资源可扩展性证据（§7）。
2. 六种架构的正确性主要通过 FCT/UDP RTT 趋势与已有工作对照，部分被对照实现是专有或只部分实现，因而不能把趋势一致解释为对每个原论文绝对性能的复现（§6）。
3. 2 µs 结果假定 OCS 重配置不是瓶颈，并依赖 nanosecond synchronization、Tofino2 packet generator、日历队列和 200 ns guardband；换硬件需重新测量（§7）。
4. host-centric Corundum NIC 版本仍在开发；当前实现重点是 switch-centric Tofino2 + Mellanox libvma（§5）。
5. 工作负载覆盖 Memcached/Gloo、iperf3 和三类 DCN trace，未给出跨更多生产工作负载、故障注入或长期运行稳定性统计。
6. 论文声称已开源并提供教程/工件，但解析正文未列出确切仓库地址；复现所需的 SDE、OCS 和同步硬件仍构成实际门槛。

### 7. 学习与应用

#### 7.1 复现路线

1. 先在 BMv2/Mininet 实现 time-flow table、日历队列暂停/恢复和 packet-generator 等价机制，验证 TA/TO 的基础路径。
2. 在可编程交换机上部署 P4 版本，使用 Tofino2 或等价设备测量 ToR-to-ToR 延迟、队列轮转误差和 EQO；按论文的 50 ns update interval、200 ns guardband 做初始复现实验。
3. 重建 Memcached/Gloo、iperf3 和 RPC/Hadoop/KV-store trace 场景，分别比较 Clos、RotorNet、Opera、Jupiter、c-Through、Mordia 及 UCMP/HOHO。
4. 最后在代表性 ToR 上填充 108-ToR time-flow table，检查资源表、缓冲分位数、70% 利用率下的拥塞检测与 pushback。

#### 7.2 可迁移启发

- “公共时间语义 + 编译到数据面”适合处理任何需要按时间窗口调度的网络状态，而不局限于光 DCN。
- 队列占用估计和 pushback 体现了控制面慢、数据面快的分层设计，可作为高吞吐流量采集/异常检测系统的工程参照。
- 评估时应把真实硬件、P4 仿真和 Mininet 的证据层级分开，避免把仿真趋势直接写成部署保证。

### 8. 总结

> 用 time-flow table 和可编程日历队列把光 DCN 软硬件解耦。

速记 Pipeline：高层 Python/JSON → 拓扑与路由编译 → time-flow table → 日历队列按时间片调度 → P4/OCS 或 BMv2 执行 → FCT、吞吐、资源和缓冲评估。

### 9. 关联知识与后续同步边界

当前库中没有专门的 optical-DCN 概念页或方法页，本次仅在本笔记中保留候选主题，不自动创建空白页面，也不修改 04–09 层共享表。

### 10. 本地证据记录

| 观点 | 原始资料位置 |
|---|---|
| time-flow table 的字段和向后兼容性 | raw Markdown §3，PDF §3 |
| TA/TO 统一 workflow 与 API | raw Markdown §4，Table 1 |
| 日历队列、队列占用估计、pushback | raw Markdown §5.1–§5.2、Appendix A/B |
| Testbed、Memcached/Gloo/iperf3 与三类 trace | raw Markdown §6–§7 |
| 1287–1324 ns、725 B、2 µs、资源占用 | raw Markdown §7、Fig. 11–12、Table 2 |
| 108-ToR 规模建模限制 | raw Markdown §7 实验设置 |

## 历史自动入库段落说明

- 本笔记前部的自动入库、摘要级或待核验段落是入库时的历史快照，按规范保留以避免删除原始记录。
- 本次新增的深度分析段落、证据记录和局限说明优先；历史段落中的“待深读/待核验”状态不代表当前分析尚未完成。

## 元数据勘误说明

- 前部自动入库块中的机构/来源标题是 OCR 或自动模板残留；以 frontmatter、ACM 论文首页和本次深度分析中的 NSDI 2026 标题与证据为准。

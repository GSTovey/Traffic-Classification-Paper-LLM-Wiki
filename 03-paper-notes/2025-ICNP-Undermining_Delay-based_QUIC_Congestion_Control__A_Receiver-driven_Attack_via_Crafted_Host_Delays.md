---
type: paper
title_original: "Undermining Delay-based QUIC Congestion Control: A Receiver-driven Attack via Crafted Host Delays"
title_cn: "破坏基于时延的 QUIC 拥塞控制：一种通过伪造 Host Delay 的接收端驱动攻击"
authors: ["Shaorui Ren", "Jia Zhang", "Enhuan Dong", "Mingwei Xu", "Yixuan Zhang", "Jiahao Cao", "Jianping Wu"]
year: 2025
venue: "IEEE ICNP 2025"
doi: "10.1109/icnp65844.2025.11192451"
url: "https://doi.org/10.1109/icnp65844.2025.11192451"
pdf: "00-inbox/PDFs/2025-ICNP-Undermining_Delay-based_QUIC_Congestion_Control__A_Receiver-driven_Attack_via_Crafted_Host_Delays.pdf"
mineru_md: "02-parsed-markdown/2025-ICNP-Undermining_Delay-based_QUIC_Congestion_Control__A_Receiver-driven_Attack_via_Crafted_Host_Delays.md"
status: processed
reading_level: L2
research_area: ["encrypted-traffic-analysis"]
task: []
method: []
dataset: []
code: "unknown"
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

# Undermining Delay-based QUIC Congestion Control: A Receiver-driven Attack via Crafted Host Delays

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Undermining Delay-based QUIC Congestion Control: A Receiver-driven Attack via Crafted Host Delays |
| 中文标题 | 破坏基于时延的 QUIC 拥塞控制：一种通过伪造 Host Delay 的接收端驱动攻击 |
| 作者 | Shaorui Ren、Jia Zhang、Enhuan Dong、Mingwei Xu、Yixuan Zhang、Jiahao Cao、Jianping Wu（清华大学；中关村实验室）；通讯作者 Mingwei Xu、Enhuan Dong、Jia Zhang |
| 年份 | 2025 |
| 会议/期刊 | IEEE International Conference on Network Protocols (ICNP 2025) |
| 研究方向 | QUIC 传输层协议安全 / 拥塞控制攻击；与 KB 的加密流量分析主线仅为“同一加密传输底座”层面的弱关联 |
| 任务类型 | 无对应白名单任务（攻击与防御分析，非检测/分类/指纹类任务） |
| 方法关键词 | Host Delay 伪造、Delay Probing（DP）、Host Delay Crafting（HDC，AbsCorr / GradCorr）、Scapegoat Server、放大增益 |
| 数据集 | 无公开数据集（Mininet 仿真 + 10 Gbps 物理测试床） |
| 是否开源 | unknown（论文未给出攻击代码仓库） |
| PDF | 00-inbox/PDFs/2025-ICNP-Undermining_Delay-based_QUIC_Congestion_Control__A_Receiver-driven_Attack_via_Crafted_Host_Delays.pdf |
| MinerU Markdown | 02-parsed-markdown/2025-ICNP-Undermining_Delay-based_QUIC_Congestion_Control__A_Receiver-driven_Attack_via_Crafted_Host_Delays.md |

> 说明：本文不是加密流量分析/分类研究，而是 QUIC 传输层攻击与防御研究。`research_area` 仅能映射到白名单中最接近的 `encrypted-traffic-analysis`（关联点为“QUIC 全连接加密使 on-path 攻击不可行、接收端成为新的攻击面”），属**弱关联**；`task`/`method` 白名单中无协议攻击类条目，故留空。知识层聚合时请单独归档为“加密传输安全”。

## 1. 一句话总结

> 利用 QUIC ACK 帧中由接收端自报、发送端无法验证的 Host Delay 字段，QUDIT 以极小代价（几万字节 ACK 侧流量）把伪造时延对齐瓶颈排队时延以欺骗基于时延的 CCA，使“替罪羊”服务器超发：受害流吞吐最多降 60%、0.3 s 内生效、放大增益 200×–600×。

## 2. 摘要翻译

### 2.1 摘要原文

QUIC gains significant attention due to its superior transmission performance, achieving widespread adoption in both academia and industry. To improve round-trip time (RTT) estimation, QUIC introduces the Host Delay field, enabling senders to exclude receiver-induced delays. Many delay-based congestion control algorithms (CCAs) rely on these RTT estimates to detect congestion and regulate sending rates. However, we find that malicious Host Delay values can distort RTT measurements, causing inappropriate rate adjustments by CCAs. In this paper, we investigate a new class of attacks leveraging maliciously crafted Host Delay values. To our knowledge, we are the first to analyze the vulnerability of Host Delay and present QUDIT, a universal receiver-driven attack targeting delay-based QUIC CCAs. Unlike prior attacks that presume full network queuing delays visibility and undetected injection capabilities, our attacker model only grants the adversary access as a standard QUIC receiver with limited knowledge of bottleneck conditions. We minimally modify the QUIC receiver to infer bottleneck queuing behavior in real time. Based on these inferences, we design dynamic Host Delay crafting strategies tailored to the specific behavior of various delay-based CCAs and accounting for random network fluctuations. Our attack prompts the sender to overshoot its rate, leading to excessive bandwidth consumption at the bottleneck and degradation of competing flows. Results demonstrate the throughput degradation of victim flow achieves up to 60% within 0.3 s and amplification gains between 200× and 600×. We propose defenses mitigating QUDIT, with vulnerabilities reported to IETF and QUIC maintainers.

### 2.2 摘要中文翻译

QUIC 因其优异的传输性能受到广泛关注，并在学术界与工业界被普遍采用。为改进往返时延（RTT）估计，QUIC 引入 Host Delay 字段，使发送端能够排除接收端引入的时延。许多基于时延的拥塞控制算法（CCA）依赖这些 RTT 估计来判断拥塞并调整发送速率。然而我们发现，恶意的 Host Delay 取值可以扭曲 RTT 测量，导致 CCA 做出不恰当的速率调整。本文研究利用恶意构造 Host Delay 的一类新攻击。据我们所知，我们是首个分析 Host Delay 脆弱性的工作，并提出 QUDIT——一种针对基于时延的 QUIC CCA 的通用接收端驱动攻击。与以往假设可完全观测网络排队时延且能不被检测地注入包的攻击不同，我们的攻击者模型仅赋予对手“标准 QUIC 接收端”的身份与有限的瓶颈状态知识。我们对 QUIC 接收端做最小改动，以实时推断瓶颈排队行为。基于这些推断，我们设计了针对不同基于时延 CCA 行为的动态 Host Delay 构造策略，并考虑了网络随机波动的影响。我们的攻击促使发送端超发，导致瓶颈处带宽被过度占用、竞争流性能下降。结果显示受害流吞吐在 0.3 s 内最多下降 60%，放大增益介于 200× 与 600× 之间。我们提出了缓解 QUDIT 的防御方案，并已向 IETF 与 QUIC 维护者报告该漏洞。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- **QUIC 的 Host Delay 设计初衷是提升 RTT 精度**：接收端在 ACK 帧中上报 Host Delay（自收到包到发出 ACK 的接收端内部时延），发送端据此扣除接收端引入的时延，得到更接近网络路径真实状况的 RTT；基于时延的 CCA（Vegas、Copa、Vivace 等）正是靠这一估计判断拥塞（§I、§II-B）。
- **该字段完全由接收端自报且不可验证**：Host Delay 由接收端估计并写入 ACK 帧，攻击者控制接收端即可操纵；论文称这是首个针对 Host Delay 脆弱性的分析（§I、§II-B）。
- **QUIC 的加密封堵了旧攻击面，但打开了新的**：on-path 攻击因 QUIC 与 TLS 1.3 加密（含包头 Packet Number）而“完全不现实”；off-path 攻击可通过入口过滤等阻断；接收端攻击中已知的唯一方案 Optimistic ACK attack 又被 RFC 9000 §21.4 的“随机跳过 packet number”检测机制反制（§II-C）。
- **作者的关键判断**：既然合法发送端（被利用的“替罪羊”服务器）不会被当作攻击者封禁，且 Host Delay 可在合法 ACK 帧内被操纵而不改变 ACK 实际到达时间，那么接收端便可成为稳定、廉价、通用的 CCA 攻击面（§I、§II-C3）。

### 3.2 现有方法的痛点和不足

| 攻击/防御类别 | 代表工作 | 痛点（对攻击者而言） | 证据来源 |
|---|---|---|---|
| On-path 攻击 | [24]–[26] | QUIC 加密 payload 与包头（含 Packet Number），修改/注入几乎必被发现，完全不可行 | §II-C1 |
| Off-path 攻击 | [24]–[26]、Crossfire [32]、Coremelt [33] | 依赖恶意发送端，一经检测即可被入口过滤等封堵，且需大量流量 | §II-C2 |
| 接收端攻击（唯一已知） | Optimistic ACK attack [27] | 被 QUIC §21.4 的 packet number 跳号检测识破，发送端可直接关闭连接 | §II-C3 |
| 现有 CCA 攻击的共同前提 | [24]–[26] | 假设可完全观测网络排队时延、具备不被检测的注入能力，威胁模型过强 | 摘要、§I |
| 防御现状 | 源 IP 封禁、入口过滤 | 对 QUDIT 无效：流量来自合法服务器，封禁会误伤正常服务 | §I |

### 3.3 论文的研究假设或核心直觉

1. **时延估计是 CCA 的信任根**：发送端把 RTT 作为网络状态的“事实”，而 RTT 中扣除的 Host Delay 由接收端提供——只要把 Host Delay 设成接近真实排队时延，`adjusted_rtt` 就会逼近 `min_rtt`，CCA 便误判“无拥塞”，从而超发（§III-C、§IV-B）。
2. **排队时延可被低成本的接收端主动探测**：接收端可通过主动发送 ack-eliciting 帧（MAX DATA）提高 ACK 反馈频率，从而高频采样 RTT 并实时估计排队时延（§IV-A）。
3. **不同 CCA 对时延的用法不同但可被统一**：绝对时延型（Vegas/Copa）与时延梯度型（Vivace）对“高估/低估”的容忍方向相反，因此需要分别校正（AbsCorr / GradCorr），并以双连接并行竞争的方式做通用化（§IV-B）。
4. **放大是协议内禀属性**：CCA 的限速机制本来把协议的天然放大无害化；攻击只是关掉了这道限速阀（§II-C3）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | Host Delay 由接收端声明、发送端不可验证；其上限 max_ack_delay 也由接收端声明（默认 25 ms） | §II-B |
| 痛点提炼 | 已有 CCA 攻击要么在 QUIC 下不可行（on-path）、要么易被封堵（off-path）、要么已被协议反制（Optimistic ACK） | §II-C |
| 问题转化 | 把“如何攻击 QUIC CCA”转化为“如何在仅有接收端权限、无法观测网络的前提下，让发送端高估网络状况” | §III-B、§III-C |
| 文献定位 | 论文自称首个利用 Host Delay 机制攻击 CCA 的工作，也是接收端威胁模型下唯一在 QUIC 中仍有效的方案 | §I、§II-C |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 把 Host Delay 对齐（接近）瓶颈排队时延可使基于时延的 CCA 低估拥塞并超发，进而挤占竞争流带宽 | §IV-B Scenario 1 | 仿真（Vegas/Copa/Vivace）+ 物理测试床 |
| 辅助假设 1 | 接收端可用极小代价（MAX DATA 帧）获取足够 RTT 采样并实时估计排队时延 | §IV-A | Fig. 6 排队时延估计误差分布 |
| 辅助假设 2 | 攻击对非时延型 CCA（CUBIC/BBR）同样有效（通过替罪羊服务器间接影响竞争） | §III-A | §V-C 物理测试床跨 CCA 实验 |
| 辅助假设 3 | 增大 base RTT 不会削弱攻击（max_ack_delay 的相对约束更松） | §V-C | 250 ms vs 25 ms base RTT 对比 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | Vegas 降 40%–60%、Copa 最多约 50%（仿真）、Vivace 约 20% | §V-B |
| 辅助假设 1 | 支撑 | 约 50% 的排队时延估计偏差 <5 ms，仅约 5% 偏差 >15 ms | §V-B（Fig. 6） |
| 辅助假设 2 | 支撑 | 物理测试床：受害流跨 CCA 降 15%–55%；CUBIC 最严重（50%–60%），BBR 约 20% | §V-C（Fig. 9） |
| 辅助假设 3 | 支撑 | 250 ms base RTT 下的降幅比 25 ms 高约 10%；max_ack_delay = 1/10 RTT 时攻击仍显著 | §V-C |

## 4. 方法设计

### 4.1 攻击总体流程

QUDIT 分三步（§III-C，Fig. 2）：

1. **建立攻击流**：攻击者（Client A）以数据接收端身份连接一个使用基于时延 CCA 的合法 QUIC 服务器（Server A，后续成为 scapegoat），且该连接与受害流（Flow B）共享瓶颈（或经过受害链路）。开局即声明一个很大的 `max_ack_delay`，以放宽 Host Delay 的可变范围。
2. **Delay Probing（DP）**：在应用层无数据可发时，主动发送最小结构的 ack-eliciting 帧（MAX DATA）诱导服务器频繁回 ACK，同时覆盖接收端固有的 ACK 聚合与定时逻辑，从而高频获得 RTT 采样并实时估计排队时延。
3. **Host Delay Crafting（HDC）**：按目标 CCA 类型动态构造 Host Delay 值，在估计排队时延附近扫描；发送端据此把 `adjusted_rtt` 压到接近 `min_rtt`，误判无拥塞 → 提高发送速率 → 挤占瓶颈带宽、压制受害流。

### 4.2 详细 Pipeline

| 阶段 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| 连接与声明 | 合法 QUIC 服务器 | 建立与受害流共享瓶颈的连接；声明极大 max_ack_delay | 攻击连接 | 放宽 Host Delay 上限，扩大可操纵区间 |
| 帧构造（DP） | 无足够应用数据 | 发送 MAX DATA（仅一个 Maximum Data 字段）触发 ACK；覆盖 ACK 聚合逻辑 | 高频 ACK 反馈 | 用最小流量换取 RTT 采样；单包可同时承载两类帧 |
| 时延估计 | ACK 帧的 RTT 采样 | queuing delay = adjusted_rtt − min_rtt（Eq. 1） | 排队时延估计 | 与基于时延 CCA 的估计口径对齐 |
| 绝对时延型攻击 | 排队时延估计 | Host Delay_i = queuing delay + AbsCorr，AbsCorr = i − (scanning_range+1)/2；在估计值附近按 1 ms 步长线性扫描 | 一组 Host Delay 值 | 保证至少一次落在有效区间，规避低估（Scenario 3） |
| 梯度型攻击 | 排队时延估计 | Host Delay = queuing delay + GradCorr，GradCorr 取 −threshold，使可检测梯度 < threshold/T_g | 近零 RTT 梯度 | 规避高估（Scenario 2），触发 PCC 的效用最大化超发 |
| 通用化 | 两条连接 | 同时建立两条连接、用不同方式伪造 Host Delay，按平均到达速率差动态掐掉表现差的那条 | 自适应选择 | 应对“目标 CCA 类型未知”的实际场景 |
| 维持攻击 | 持续 RTT 采样 | 每 5 ms 至少发一次 ACK/ack-eliciting 帧 | 持续压制 | 维持收敛后的攻击效果 |

### 4.3 关键公式与机制

**QUIC 侧的 RTT 计算（Table I，攻击的“被利用对象”）**

| 变量 | 计算式 | 说明 |
|---|---|---|
| latest_rtt | ACK Time − Send Time | 原始 RTT 采样 |
| min_rtt | min(latest_rtt) | 最小 RTT 估计（用未扣除 Host Delay 的原始采样，防止低估） |
| Host Delay | min(max_ack_delay, Host Delay Decoded from ACK) | 实际用于 RTT 修正的 Host Delay |
| rtt_sub_HD | latest_rtt − Host Delay | 中间变量 |
| adjusted_rtt | rtt_sub_HD（若 rtt_sub_HD ≥ min_rtt）；否则取 latest_rtt | 被 min_rtt 下界保护的“修正后 RTT” |
| smoothed_rtt | 7/8 × smoothed_rtt + 1/8 × adjusted_rtt | RTT 的 EWMA |
| rttvar | 3/4 × rttvar + 1/4 × \|smoothed_rtt − adjusted_rtt\| | RTT 波动估计 |

**攻击侧公式（§IV-B）**

- 排队时延估计（Eq. 1）：`queuing delay = adjusted_rtt − min_rtt`。
- 绝对时延型（Eq. 2–3）：`Host Delay_i = queuing delay + AbsCorr`，`AbsCorr = i − (scanning_range + 1)/2`；每个扫描周期内以 1 ms 间隔线性扫描，保证反馈值与最优值之差不超过 0.5 ms（等效于“误差 <0.5 ms 的排队时延估计”）。
- 梯度型（Eq. 4–5）：`Host Delay = queuing delay + GradCorr`，GradCorr 取 `−threshold`，使发送端可检测到的最大 RTT 梯度保持在 `threshold / T_g` 以下（T_g 为 CCA 的梯度检测周期）。
- 参数选择（§IV-B3）：`scanning_range` = 1/4 RTT 内的 ACK 反馈数；`threshold` = RTT/10 + 5 ms（第一项补偿网络抖动，第二项覆盖 DP 的发送间隔）。
- 三种场景判据（§IV-B）：**Scenario 1（理想）** rtt_sub_HD = min_rtt，欺骗最大化；**Scenario 2（高估）** rtt_sub_HD < min_rtt → 发送端改用未修正的 latest_rtt，攻击完全失效；**Scenario 3（低估）** rtt_sub_HD > min_rtt → 仅部分失效。绝对时延型可容忍 Scenario 2、需压制 Scenario 3；梯度型相反。

### 4.4 关键设计取舍

| 设计点 | 选择 | 代价/理由 |
|---|---|---|
| ACK 发送间隔 | 选定 5 ms（同一间隔同时用于 ACK 与 ack-eliciting 帧，使二者可装进同一个 QUIC 包） | 间隔过短会增加服务器负担与攻击者带宽开销、降低放大增益；5 ms 下 RTT 测量间隔比普通接收端缩短约 75%，放大增益 >300（Fig. 3） |
| max_ack_delay 声明值 | 声明极大值 | 放宽 Host Delay 可变范围；论文指出默认 25 ms 与最大排队时延量级相当，本就给攻击者留下过大空间 |
| 帧类型选择 | MAX DATA | 语义上频繁发送不引起警觉（本就是通告可发送量的帧），且仅含一个字段，注入数据量最小 |
| 通用化方式 | 双连接并行、择劣断开 | 不同 CCA 的最优伪造方向互斥（对梯度型 CCA，绝对时延型策略“完全失效”），只能靠竞争选择；正常情况下双连接仅共存最初几个 RTT |

## 5. 与其他方法对比

### 5.1 与既有 CCA 攻击的威胁模型对比

| 维度 | On-path 攻击 [24]–[26] | Off-path 攻击 [24]–[26]、Crossfire/Coremelt | Optimistic ACK [27] | QUDIT |
|---|---|---|---|---|
| 攻击者位置 | 瓶颈交换机 | 外部恶意发送端 | 数据接收端 | 数据接收端 |
| QUIC 下可行性 | 不可行（加密保护包头与 payload） | 理论可行但易被封堵（入口过滤） | 可行但被 §21.4 跳号检测反制 | 论文称目前唯一仍有效的接收端方案 |
| 所需网络知识 | 需完全观测排队时延 | 需制造拥塞 | 无需 | 仅需接收端本地的 RTT/ACK 反馈 |
| 流量代价 | 高 | 高（洪泛） | 低 | 极低（几万字节量级），放大 200×–600× |
| 误导方向 | 让受害端“以为拥塞”→降速 | 让受害端“以为拥塞”→降速 | 让发送端超发 | 让发送端超发（并借合法服务器放大） |

### 5.2 攻击对不同 CCA 的效果对比

| 目标 CCA | 类型 | 效果（仿真 20–60 Mbps / 30 ms） | 效果（物理测试床 10 Gbps） |
|---|---|---|---|
| Vegas | 绝对时延阈值 | 受害流降 40%–60% | — |
| Copa | 绝对时延（动态阈值） | 最多约 50%；随带宽上升效果下降 | 约 20%–30% |
| PCC Vivace | 时延梯度 | 约 20%（梯度只能被压到 threshold/T_g，非零） | 论文列为较稳健一类 |
| CUBIC（受害端） | 丢包型 | — | 50%–60%（最严重；因替罪羊超发引发 bufferbloat 与丢包，CUBIC 激进降 CWND） |
| BBR（受害端） | 拥塞型 | — | 约 20% |
| PCC（受害端） | 学习型 | — | 论文列为较稳健一类 |
| 全 CCA 汇总 | — | — | 受害流降 15%–55% |

### 5.3 与 KB 内工作的关系

- 唯一引用到的 KB 论文：`[[2023-NDSS-Detecting_unknown_encrypted_malicious_traffic_in_real_time_via_flow_interaction_graph_analysis]]`（参考文献 [29]，在 §II-C2 作为“可检测恶意发送端”的例子被引用）。
- 与 KB 主线的连接点是**加密传输底座**：QUIC 全连接加密使得基于包内容的检测/分类（ETC、WF）成为唯一可行的分析视角，而本文研究的则是同一加密层之下的传输层控制面攻击——对做 QUIC 流量分析的研究者而言，是“流特征所依赖的传输行为可被恶意端点操纵”的提醒。
- 对基于时序/时延特征的流量分析（如 RTT/抖动敏感的指纹），本文提示：接收端可主动改变发送端的发送节奏与 RTT 测量，可能影响采样所得特征的稳定性（推断，论文未讨论）。

## 6. 实验表现与优势

### 6.1 实验设置

| 项目 | 内容 |
|---|---|
| 实现 | msquic（IETF QUIC 实现）；Copa、PCC、Vegas 分别参考 mvfst、Chrome QUIC、Linux kernel 实现移植进 msquic，统一框架下实验 |
| 仿真环境 | Mininet；瓶颈带宽 20–60 Mbps，RTT 固定 30 ms，瓶颈缓冲区 = 1 BDP；每次运行 100 s 以到达稳态；多次运行取平均（剔除异常连接失败） |
| 物理测试床 | 10 Gbps NIC 端口与 10 G SFP+ 交换机瓶颈，缓冲区可容忍约 30 ms 排队时延；因单条 QUIC 流无法打满 10 Gbps，另加 1 条 Iperf 流维持饱和，共 12 条 QUIC 流 + 1 条 Iperf 流 |
| 配置 | QUIC 流用 msquic 默认配置（1500B MTU）、应用层不限速；攻击者与受害流使用同一算法的相同参数 |
| 评测指标 | 受害流带宽降幅、放大增益（服务器因攻击发出的数据量 / 攻击者自身发出量）、排队时延估计误差、收敛时间与流量开销 |

### 6.2 主结果（仿真，§V-B）

| 实验 | 设置 | 结果 |
|---|---|---|
| 带宽占用 | 20–60 Mbps、30 ms，攻击者与受害端同 CCA | Vegas 受害流降 40%–60%；Copa 最多约 50%（随带宽上升效果减弱）；Vivace 约 20% |
| 放大增益 | 不同瓶颈带宽（Fig. 5） | 约 200 至 >600，随带宽上升而增大（带宽越大，每个 5 ms 周期内被确认的数据越多） |
| 排队时延估计 | 30 Mbps / 30 ms（Fig. 6） | 约 50% 的估计偏差 <5 ms；约 5% 偏差 >15 ms |
| 多受害者 | 40 Mbps / 30 ms，Copa；单受害流与 5 条受害流（Fig. 7–8） | 最初 1/5 的受害流攻击启动后 20 s 内降 20%，且随受害者规模扩大仍维持 |
| 收敛与开销 | §IV-B3 统一框架 | 约 10 个 RTT 内达到稳态效果的 >90%（平均 <0.3 s）；仅需 scapegoat 侧 0.5 MB 数据、攻击者侧几万字节 |
| RTT 依赖性 | Copa，RTT 250 ms | 可把受害流平均吞吐降 25% 以上 |

### 6.3 主结果（物理测试床 10 Gbps，§V-C）

| 实验 | 设置 | 结果 |
|---|---|---|
| 跨 CCA 稳健性 | 攻击者打 Copa 替罪羊服务器；受害端分别为 Copa/BBR/CUBIC/PCC | 受害流降 15%–55%；Copa 20%–30%；CUBIC 50%–60%（最严重）；BBR 约 20%；PCC 较稳健 |
| base RTT 依赖 | 25 ms vs 250 ms | 250 ms 下降幅比 25 ms 高约 10%；即使 max_ack_delay 被限制为 base RTT 的 1/10（250 ms RTT 对应 25 ms）攻击仍显著 |
| 脆弱性根因 | max_ack_delay 设计 | (1) 默认 25 ms 与最大排队时延量级相当，给攻击者过大操纵空间；(2) 攻击者可任意声明极大的 max_ack_delay |

### 6.4 优势与局限

**优势**

- 威胁模型现实：仅需“标准 QUIC 接收端”身份，无需观测网络或注入伪造包；且被利用的是合法可信服务器，源 IP 封禁类防御失效（§I）。
- 代价极低、见效极快：0.3 s 内、几万字节攻击者流量即可达到 200×–600× 放大。
- 覆盖面广：对多种基于时延的 CCA 均有效，并能通过替罪羊机制波及非时延型受害流（含部署最广的 CUBIC）。
- 已负责任披露：向 IETF 提出协议修订建议并与 QUIC 维护者协调（§VI-C）。

**局限（论文自述与推断）**

- 需要“与被攻击流共享瓶颈”的连接条件；论文讨论用 bots 探测瓶颈与共瓶颈判定（参考文献 [25]、[32] 的方法），并指出攻击者与受害者同处接入网（如同一公共 WiFi）时更易满足（§III-A）。
- 梯度型 CCA 的效果天然受限：RTT 梯度只能被压到 `threshold / T_g`（非零），因此 Vivace 仅约 20%（§IV-B2、§V-B）。
- 通用化依赖双连接竞争，存在“最初几个 RTT 内两条连接共存”的窗口；ECMP 等路径分歧下维持双连接时放大因子降到 100 以上（估算自 Fig. 5）（§IV-B3）。
- 效果受网络抖动与估计误差影响；Copa 的效果随带宽上升而减弱，需靠增大 RTT 补偿（§V-B）。
- 未开源，`code` 为 unknown；实验依赖 msquic 内的 CCA 移植，复现门槛较高。

## 7. 学习与应用

### 7.1 可借鉴的研究思路

- **“接收端自报参数不可验证”是一类通用漏洞模式**：凡由对端声明、本端无法验证的控制参数（Host Delay、max_ack_delay）都应进入威胁模型；本文给出了“先声明极大值放宽范围、再在其内精细构造”的完整攻击链。
- **跨算法通用化策略**：面对优化目标互斥的多类算法，用“双连接并行 + 指标竞争选择”实现通用攻击，是工程上可复用的手法（§IV-B3）。
- **防御设计的三层结构**：协议修订（max_ack_delay 改由发送端控制）、实现约束（本地禁用 Host Delay 或验证并动态加权）、网络机制（WFQ 隔离）（§VI-B）——可作为“协议参数致脆弱”类问题的通用防御清单。

### 7.2 对 KB 主线研究的价值

- 直接价值有限（非检测/分类/指纹任务），但有两点间接意义：
  1. **QUIC 加密是流量分析的既定前提**：本文再次确认 on-path 修改/注入在 QUIC 下不可行，侧面支持“加密流量分析必须转向端到端可观测特征”的判断。
  2. **时序特征的可操纵性提醒**：CCA 与 RTT 行为可被端点主动操纵，做时序敏感的分析（如基于 RTT/抖动的检测）时应评估该类干扰。
- 防御建议中的“Host Delay 验证与动态加权”思路，可迁移到任何“对端上报的测量辅助字段”的可信度评估问题。

### 7.3 复现要点

- 需要 msquic 与三种 CCA 的移植（Copa 参考 mvfst、PCC 参考 Chrome QUIC/PCC-Uspace、Vegas 参考 Linux kernel），论文未提供补丁或仓库。
- 仿真参数：20–60 Mbps、30 ms、1 BDP 缓冲、100 s；测试床需 10 Gbps 链路 + 辅助 Iperf 流 + 12 条 QUIC 流。
- 关键超参：ACK/ack-eliciting 发送间隔 5 ms、scanning_range = 1/4 RTT 内 ACK 数、threshold = RTT/10 + 5 ms。

### 7.4 可延伸方向

- 把“端点自报参数不可验证”推广到其他协议（如 GCC/WebRTC 的接收端时延辅助测量，论文 §VI-A 已指出其同样依赖接收端）（§VI-A）。
- 研究该攻击对基于时序的加密流量分析（WF/ETC 特征提取）稳定性的影响——论文未涉及，属推断。

## 8. 总结

QUDIT 把 QUIC 的 Host Delay 机制从“提升 RTT 精度的设计”转化为攻击面：接收端用 MAX DATA 帧以极低代价换取高频 ACK 反馈（RTT 测量间隔缩短约 75%），实时估计瓶颈排队时延，再按 CCA 类型分别用 AbsCorr（绝对时延型）与 GradCorr（梯度型）伪造 Host Delay，使合法服务器误判无拥塞而超发。仿真中 Vegas 受害流降 40%–60%、Copa 约 50%、Vivace 约 20%；物理测试床 10 Gbps 下跨 CCA 降幅 15%–55%，CUBIC 最严重（50%–60%）；放大增益 200×–600×，0.3 s 内生效。防御方案覆盖协议修订、实现约束与 WFQ 三类，漏洞已向 IETF 与 QUIC 维护者披露。本文与 KB 的加密流量分析主线仅有加密传输底座层面的弱关联。

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[encrypted-traffic-analysis]]：弱关联——本文主题为 QUIC 传输层安全，仅因“QUIC 全连接加密封堵 on-path 攻击面、使端点成为新攻击面”而与本概念相邻。

### 9.2 相关方法

- KB 方法白名单（transformer、graph-neural-network、contrastive-learning 等）均不覆盖拥塞控制攻击/协议安全类方法，故不建立方法链接。
- 论文引用的 Vegas、Copa、PCC Vivace、CUBIC、BBR、Optimistic ACK attack、Crossfire、Coremelt 等均不在 KB 论文注册表 A 表中。

### 9.3 相关任务

- KB 任务白名单（website-fingerprinting、traffic-classification、malicious-traffic-detection 等）无“协议攻击/防御”类条目，故不建立任务链接。

### 9.4 相关综述

- 无对应白名单综述页与本文主题相符，不建立链接。

### 9.5 对比与索引

- [[method-comparison-table]]：本文提出了新的攻击方法（QUDIT）并给出与 On-path/Off-path/Optimistic ACK 的威胁模型对比，适宜入表。
- [[open-source-registry]]：不适用（论文未给出攻击代码仓库）。

## 10. 证据记录

| 编号 | 主张 | 证据位置 | 类型 |
|---|---|---|---|
| E1 | Host Delay 由接收端写入 ACK 帧，实际取值受 min(max_ack_delay, 解码值) 约束；max_ack_delay 默认 25 ms 且由接收端声明 | §II-B，Table I | 协议事实 |
| E2 | adjusted_rtt 受 min_rtt 下界保护：rtt_sub_HD < min_rtt 时退回 latest_rtt（Scenario 2 失效机理） | §II-B、§IV-B，Table I | 协议事实 |
| E3 | 5 ms 发送间隔使接收端 RTT 测量间隔缩短约 75%，放大增益 >300 | §IV-A，Fig. 3 | 实测 |
| E4 | 仿真：Vegas 降 40%–60%、Copa 最多约 50%、Vivace 约 20% | §V-B，Fig. 4 | 实测 |
| E5 | 放大增益约 200 至 >600，随带宽上升 | §V-B，Fig. 5 | 实测 |
| E6 | 排队时延估计：约 50% 偏差 <5 ms，约 5% 偏差 >15 ms | §V-B，Fig. 6 | 实测 |
| E7 | 约 10 个 RTT（平均 <0.3 s）收敛到稳态效果 >90%；scapegoat 侧 0.5 MB、攻击者侧几万字节 | §V-B | 实测 |
| E8 | 物理测试床：跨 CCA 受害流降 15%–55%；Copa 20%–30%、CUBIC 50%–60%、BBR 约 20% | §V-C，Fig. 9 | 实测 |
| E9 | 250 ms base RTT 下比 25 ms 降幅高约 10%；max_ack_delay = 1/10 RTT 时攻击仍显著 | §V-C | 实测 |
| E10 | 攻击对 RTT 250 ms 的 Copa 可降其受害流吞吐 25% 以上 | §V-B，Fig. 9 | 实测 |
| E11 | CUBIC 占 Alexa top 20k 站点约 40%，放大实际威胁 | §V-C（引 [22]） | 引用数据 |

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2025-ICNP-Undermining_Delay-based_QUIC_Congestion_Control__A_Receiver-driven_Attack_via_Crafted_Host_Delays.pdf
- MinerU Markdown：02-parsed-markdown/2025-ICNP-Undermining_Delay-based_QUIC_Congestion_Control__A_Receiver-driven_Attack_via_Crafted_Host_Delays.md

## 12. 后续问题

1. §V-C 汇总句称受害流“约 15%–55%”降幅且“regardless of their CCA”，但同段又给出 CUBIC 50%–60%，两个区间不完全一致（60% > 55%），引用时建议直接采用分 CCA 数值。
2. 摘要/§I 的 “up to 60% within 0.3 s” 与 §V-B “收敛到 >90% 稳态效果平均 <0.3 s” 是两种口径（最大降幅 vs 收敛时间），不宜混用。
3. 解析稿中 Eq. (2)/(4) 附近的编号错乱（出现游离的 “(3)”“(5)”），且 GradCorr 的具体取值仅以文字给出（取 −threshold），无独立公式。
4. §V-A 提到 PCC、Vegas 分别参考“mvfast [5]”（应为 mvfst）等实现移植，解析稿中实现细节描述较简，复现需自行对齐版本。
5. 未给出攻击代码或配置脚本；`code` 为 unknown。
6. 未评估攻击对基于时序特征的加密流量分析（WF/ETC）的影响，属可延伸方向（推断）。

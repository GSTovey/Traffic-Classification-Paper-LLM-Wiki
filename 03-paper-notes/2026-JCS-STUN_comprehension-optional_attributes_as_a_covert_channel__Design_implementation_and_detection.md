---
type: paper
title_original: "STUN comprehension-optional attributes as a covert channel: Design, implementation, and detection"
title_cn: "以 STUN 可理解性可选属性为隐蔽信道：设计、实现与检测"
authors: [Gorka Gorrochategui, Unai Zulaika, Pablo Garaizar]
year: 2026
venue: "Computers & Security 2026"
doi: "10.1016/j.cose.2026.105043"
url: "https://doi.org/10.1016/j.cose.2026.105043"
pdf: "00-inbox/PDFs/2026-JCS-STUN_comprehension-optional_attributes_as_a_covert_channel__Design_implementation_and_detection.pdf"
mineru_md: "02-parsed-markdown/2026-JCS-STUN_comprehension-optional_attributes_as_a_covert_channel__Design_implementation_and_detection.md"
status: processed
reading_level: L2
research_area: [tunnel-detection, anomaly-detection]
task: [tunnel-detection, anomaly-detection]
method: []
dataset: [ITC-Net-blend-60, MAWI]
code: "unknown"
relevance: medium
created: "2026-09-19"
updated: "2026-09-19"
---

# STUN comprehension-optional attributes as a covert channel: Design, implementation, and detection

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | STUN comprehension-optional attributes as a covert channel: Design, implementation, and detection |
| 中文标题 | 以 STUN 可理解性可选属性为隐蔽信道：设计、实现与检测 |
| 作者 | Gorka Gorrochategui, Unai Zulaika, Pablo Garaizar（University of Deusto 工学院，西班牙 Bilbao；Basque Government DEUSTEK 组资助） |
| 年份 | 2026 |
| 会议/期刊 | Computers & Security（Elsevier），分配口径 "Computers & Security 2026" |
| 研究方向 | tunnel-detection / anomaly-detection（协议层隐蔽信道 + NIDS 检测缺口） |
| 任务类型 | 隐蔽信道（covert channel）设计与检测；企业边界 NIDS/NGFW 逃逸评估 |
| 方法关键词 | STUN comprehension-optional attributes (0x8000–0xFFFF) 载体、L2 over TAP 隧道、双向 polling、Shannon 熵检测器、Zeek spicy_STUN、Suricata 8 entropy 关键字 |
| 数据集 | ITC-Net-blend-60（合法 RTC 流量基线，3185 条 STUN 消息）、MAWI（2019–2026 纵向 STUN 流量）、Shodan（154,643 台公开 STUN 服务器） |
| 是否开源 | 解析稿自相矛盾：§2 Ethics 称源码不公开（仅对具备机构身份的合格研究者开放），Data availability 却写 "Google Drive Share - PCAPs, Source Code, Scripts, Logs (Original data)" → code: unknown |
| PDF | 00-inbox/PDFs/2026-JCS-STUN_comprehension-optional_attributes_as_a_covert_channel__Design_implementation_and_detection.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-JCS-STUN_comprehension-optional_attributes_as_a_covert_channel__Design_implementation_and_detection.md |

---

## 1. 一句话总结

> 把任意以太网帧塞进 RFC 5389 规定"必须静默忽略"的 STUN 可选属性里，用轮询解决服务器不能主动发包的非对称性，做出可绕过 Snort 3/Suricata/FortiGate/Palo Alto 的全双工 L2 隧道；再用属性值的 Shannon 熵（4.5 bits 阈值）在零误报下 100% 检出。

---

## 2. 摘要翻译

### 2.1 摘要原文

> Real-time communication protocols carry implicit trust at perimeter defenses because enterprise networks must allow them for Voice over IP (VoIP) and Web Real-Time Communication (WEBRTC) operation. Existing covert-channel literature has explored Session Initiation Protocol (SIP) signaling (Mazurczyk and Szczypiorski, 2008). Real-Time Transport Protocol (RTP)/RTCP media (Mazurczyk, 2013: Schmidt et al. 2018). and WEBRTC streams (Barradas et al. 2020; Figueira et al. 2022), but Session Traversal Utilities for NAT (STUN), despite its central role in NAT traversal and its ubiquity in modern networks. has not been investigated as a covert channel carrier. We design a Layer 2 covert channel that encapsulates arbitrary Ethernet frames within STUN comprehension-optional attributes, which RFC 5389 (Rosenberg et al., 2008) requires compliant implementations to silently ignore. A bidirectional polling mechanism overcomes STUN's client–server asymmetry, producing a full-duplex tunnel indistinguishable from legitimate Interactive Connectivity Establishment (ICE) keep-alive traffic [...] Across 3646 data-carrying covert messages, no signature or protocol-aware engine flagged the traffic as anomalous. To address the detection gap, we propose a lightweight Shannon-entropy detector applied to optional attribute payloads. The mean per-attribute entropy of the covert channel reaches 6.247 bits/byte, well above the highest entropy observed in 1358 legitimate STUN messages from the ITC-Net-blend-60 dataset (4.392 bits/byte from Telegram). A 4.5 bits/byte threshold flags all 3646 covert messages while producing zero false positives across the legitimate corpus.

> ⚠️ MinerU 解析问题：摘要中 "Empirical evasion testing was conducted against Snort 3 ... and a FortiGate 40F firewall" 一句在解析稿中因 small-caps/丢词被压缩为残片，已用省略号标出；正文另有零星丢词（如 "Thi trend"、"Laver 2"、"efort"、"diference"）。

### 2.2 摘要中文翻译

实时通信协议在企业边界处享有隐含信任，因为企业网络必须放行它们才能让 VoIP 与 WebRTC 正常工作。既有隐蔽信道文献已研究过 SIP 信令、RTP/RTCP 媒体流与 WebRTC 流，但 STUN（NAT 会话穿越工具）尽管在 NAT 穿越中处于核心地位、且在现代网络中无处不在，却从未被作为隐蔽信道载体研究过。本文设计了一种 L2 隐蔽信道，把任意以太网帧封装进 STUN 的"可理解性可选"（comprehension-optional）属性中——RFC 5389 要求合规实现必须静默忽略这些属性。作者用双向轮询机制克服 STUN 客户端-服务器的非对称性，构造出与合法 ICE 保活流量难以区分的全双工隧道。原型被移植部署到两种架构的嵌入式 Linux 设备（ARM 的 Yealink T19P E2 IP 电话与 MIPS 的 Ubiquiti EdgeRouter X）。在 3646 条携带数据的隐蔽消息上，没有任何基于签名或协议感知的引擎把该流量标为异常。为填补检测缺口，作者提出一个作用于可选属性载荷的轻量 Shannon 熵检测器：隐蔽信道的平均每属性熵为 6.247 bits/byte，远高于 ITC-Net-blend-60 数据集中 1358 条合法 STUN 消息的最高熵（Telegram 的 4.392 bits/byte）。以 4.5 bits/byte 为阈值可标记全部 3646 条隐蔽消息，同时在合法语料上零误报。这些结果暴露了当前网络防御策略中的系统性检测缺口，并提示应把熵感知检测纳入实时通信信令协议的检查体系。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 对手（APT）需要能绕过分界防御的 C2 通道；防御成熟（DPI、行为分析）后，攻击者转向"企业必须放行"的高信任合法协议。
- RTC 协议族是理想载体：防火墙为了 VoIP/WebRTC 必须放行，且信令解析复杂、检查昂贵。
- 作者声称：STUN 作为 RTC 的 NAT 穿越底座，是三条既有研究线（SIP 信令、RTP 媒体、WebRTC 流）都未覆盖的空白（§1、§3）。

### 3.2 现有方法的痛点和不足

| 既有路线 | 代表工作 | 局限 |
|---|---|---|
| SIP 信令字段嵌入 | Mazurczyk & Szczypiorski 2008；Mehić 等 2014；Tsiatsikas 等 2015（SDP） | 修改协议已定义字段，易被字段级完整性校验与统计时序分析发现 |
| RTP/RTCP 媒体嵌入 | Mazurczyk 2013；Schmidt 等 2018（VAD 静默期伪造包） | 依赖媒体会话存在；ML 分类器可针对包时序/长度分布检测 |
| WebRTC 流改造 | Protozoa / Stegozoa / DeltaShaper / Facet | 预设已建立 WebRTC 会话（需 ICE 协商完成），且已有 ML 检测线 |
| TURN 中继滥用 | Crosser 2025（Zoom/Teams TURN 作 C2） | 依赖短时第三方会议凭据，平台可撤销（Zoom 已禁用 P2P TURN 能力） |

作者归纳差异：本文信道位于**控制平面本身**、保持协议合规、无需媒体会话与编解码器改造、不依赖可被撤销的第三方凭据（§3）。

### 3.3 论文的研究假设或核心直觉

核心直觉有两条：(1) 协议预留空间（comprehension-optional 属性范围 0x8000–0xFFFF）是"合规的隐藏空间"——合规实现必须忽略，因此不会产生任何畸形字段供签名/完整性检查触发；(2) 轮询可把 STUN 的半双工请求-响应模型转换成全双工隧道，且这种轮询与合法 ICE 保活同形。检测侧假设：加密载荷使属性值字节接近均匀分布，其 Shannon 熵显著高于任何合法属性值。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 企业防火墙对 STUN/RTC 普遍 allow-by-default；Shodan 收录 154,643 台公开可达 STUN 服务器（2026-02）；MAWI 中 STUN 流 2019→2026 增长 239 倍 | §5.3、§11.1 |
| 痛点提炼 | 白名单式管控在运营上不可行（服务器散布在数百云厂商/ASN、IP 随自动伸缩变化），于是"隐式信任协议而非服务器身份"成为常见安全姿态 | §11.1 |
| 问题转化 | 提出可研究问题：STUN 控制平面能否作为协议合规、无需媒体会话的隐蔽信道载体？现行 NIDS/NGFW 能否发现它？若不能，何种统计信号能检测？ | §1、§5.2、§10 |
| 文献定位 | 既有隐蔽信道研究覆盖 SIP/RTP/WebRTC/TURN 四条线，STUN 控制平面为空白；NIDS 侧只有签名与协议语法两种范式，均无语义深度 | §3、§10.2 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 任意以太网帧可封装进 comprehension-optional 属性，并通过轮询实现全双工隧道，且不触发主流 NIDS/NGFW 告警 | RFC 5389 §7.3.1 "未知可选属性必须被忽略"；§4.2 | 两平台（ARM/MIPS）部署 + 四类检测器实测（§8） |
| 辅助假设 1 | 加密载荷使可选属性值熵显著高于合法 STUN 属性值，故单阈值可零误报检出 | 信息论直觉（§10.1） | ITC-Net-blend-60 合法流量基线 + 3646 条隐蔽消息（§10.1.1） |
| 辅助假设 2 | 同一熵信号可在生产级签名引擎（Suricata 8）中以规则表达 | Suricata 8 引入原生 entropy 关键字 | 阈值扫描 T∈{4.5…6.0}（Table 12） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | Snort 3（47,143 条 Talos 规则）0 告警；Suricata 8 ET Open 仅 ET INFO；FortiGate 40F（全 UTM）与 Palo Alto VM-Series 均判为 STUN、无告警 | §8.2、Table 4、Table 14 |
| 辅助假设 1 | 支撑 | 隐蔽信道熵 6.247 bits（范围 5.154–7.856）vs 合法最高 4.392 bits；4.5 bits 阈值 → 3646/3646 检出、0/1358 误报 | §10.1.1、Table 10 |
| 辅助假设 2 | 部分支撑 | Suricata 8 规则在 T=4.5 时 100% 召回但 5215 FP（精度 41.2%）；需 T=5.75 才能零误报，此时召回降至 56.2% | §10.3、Table 12 |

---

## 4. 方法设计

### 4.1 方法整体流程

两个 client 侧植入（implant）与一个攻击者控制的 relay：relay 监听 UDP/3478 上的 STUN Binding Request；client 把 TAP 接口上的以太网帧切片后写入自定义 comprehension-optional 属性（类型 0x8FAD，落在 0x8000–0xFFFF 预留区）发出；relay 解析属性取出帧，反向数据则缓存在 per-client FIFO 环形缓冲里，等下一个 Binding Request 到达时随 Binding Response 回送（轮询驱动的下行）。可选 ChaCha20 加密。检测侧：Zeek spicy_STUN 逐属性解析并计算属性值的 Shannon 熵，H>4.5 bits 判隐蔽。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 载体选型 | STUN 消息结构 | 比较 Transaction ID（12 B 固定、高熵属正常，弃）、Padding（0–3 B、零值检查，弃）、可选属性（≈1450 B、RFC 要求忽略，选） | 选定 0x8000–0xFFFF 属性区 | 容量与检测风险的权衡（Table 3） |
| Step 2 隧道建立 | TAP 虚拟网卡上的以太网帧 | 分片后以 TLV 写入自定义属性（类型 0x8FAD），UDP/3478 发出 | STUN Binding Request | L2 桥接 |
| Step 3 非对称处理 | 服务器不能主动发包 | client 周期发送 Binding Request 轮询；relay 用 per-client FIFO Ring Buffer 缓存下行数据 | 全双工逻辑 | 半双工协议 → 全双工隧道（§7.2） |
| Step 4 事件循环 | 双向数据流 | 异步 I/O 事件循环 + 非对称缓冲，避免阻塞 | 稳定吞吐 | 资源受限设备可用（§7.1） |
| Step 5 逃逸评估 | 隐蔽流量 pcap | 依次送入 Snort 3、Suricata 8、FortiGate 40F、Palo Alto VM-Series | 告警/分类结果 | 验证检测缺口（§8.2） |
| Step 6 熵检测 | 属性值字节 | Shannon 熵逐属性计算，H>4.5 bits 告警 | 检测结论 | 低误报对策（§10.1） |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Implant（client） | 抓取 TAP 帧、封装、轮询 | TAP 以太网帧 | STUN Binding Request | 部署于 Yealink T19P E2（ARM）/ EdgeRouter X（MIPS）/ 测试用 Debian 主机 |
| Relay（server） | 解封装、缓存下行、回送 | Binding Request | Binding Response + 下行数据 | 部署于 OVH VPS（AS16276） |
| FIFO Ring Buffer | 每客户端下行队列 | relay 收到的下行帧 | 待发送队列 | 解决服务器不能主动发起的问题 |
| 熵检测器（Zeek spicy_STUN） | 逐属性熵计算 | STUN 消息 | 告警 | 高精度第二阶段 |
| Suricata 8 熵规则 | 消息级熵（offset 20 起） | 原始 UDP 载荷 | 告警 | 零工具依赖的前线过滤器 |

### 4.4 公式、算法和机制解释

- 载体合法性依据：RFC 5389 §7.3.1 "Unknown comprehension-optional attributes MUST be ignored by the agent"，且该范围在 RFC 8489（现行标准）中未作修改。
- 熵判据：对每个可选属性的值字节序列计算 Shannon 熵 H（bits/byte），H > 4.5 判隐蔽。
- Suricata 8 规则原型：`content:"|00 01|"; depth:2; content:"|21 12 A4 42|"; offset:4; depth:4; dsize:>50; entropy:offset 20, value >T; sid:9000010;`（Binding Response 用 `content:"|01 01|"` 的对称规则）。限制在于 Suricata 8 无 STUN 应用层解析器，熵只能作用于"头部 20 字节之后所有属性拼接"这一粒度。
- 速率规则原型：`detection_filter:track by_src,count 207,seconds 60`，对隐蔽流量产生 1682 条告警 / 合法语料 0 误报。

### 4.5 方法优势

- 完全协议合规：不改动任何既有字段，不产生畸形值，字段级完整性检查无效。
- L2 隧道语义（TAP）：可直接用于红队横向移动 / 桥接内网，而非仅传文件。
- 载体极难封堵：无需媒体会话、无需第三方凭据，攻击者自建 STUN 端点即可。
- 检测侧给出可部署的零误报方案（Zeek 逐属性熵），并给出在生产 NIDS 中的近似替代（Suricata 8 规则）。

### 4.6 方法不足

- 吞吐受轮询频率与 MTU 限制：局域网上 Yealink 最高 19.61 Mbps（MTU 8000）；EdgeRouter X 的生产 WAN 路径为 41.9/41.4 Mbps，仅为同路径直连 243 Mbps 的 17%。
- 时延增加：RTT 从 33.2 ms 升至 49.4 ms（+16.2 ms），下行还受轮询间隔约束。
- 存在可被检测的结构性异常：近似 MTU 的固定包长、高熵属性值、严格周期性的轮询（作者在 §11.2–11.5 自陈）。
- 熵检测器可被低成本规避：在属性值中交织低熵填充字节即可把每属性熵压到 4.5 以下（§10.1.3）。
- 合法基线代表性受限：ITC-Net-blend-60 为 60 个 Android 应用，不含企业 SIP/IP 电话场景；作者指出目前无公开的企业 VoIP/SIP 全载荷数据集（§10.1.2）。
- 解析稿对"源码公开性"自相矛盾（见 §0 与 §7.1）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 维度 | 既有隐蔽信道（SIP/RTP/WebRTC/TURN） | 本文 STUN 控制平面信道 |
|---|---|---|
| 承载层 | 信令字段调制、媒体流注入、中继凭据滥用 | NAT 穿越控制平面本身 |
| 是否改动既有字段 | 是（调制/复用已定义字段或时序） | 否（只新增 RFC 允许忽略的属性） |
| 是否需要媒体会话 | 需要（ICE 协商完成后才有流） | 不需要 |
| 是否依赖第三方凭据 | Crosser 依赖短时会议凭据（可撤销） | 只需攻击者自建 STUN 端点 |
| 检测现状 | 已有 ML 检测线（包时序/长度） | 本文实测四类检测器全部漏报 |

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| STUN 控制平面作为隐蔽载体 | 首个把 comprehension-optional 属性用于 L2 隧道的设计与实现 | 高 | 是（其他 TLV/可扩展协议同样思路） |
| 轮询式双向化 | 用 client 驱动的轮询把请求-响应协议变为全双工隧道 | 中 | 是（任何非对称协议的隧道化） |
| 嵌入式跨架构可移植性 | ARM/MIPS 双平台实测，证明商品级 VoIP/边缘路由器可被改造为桥 | 中 | 是 |
| 熵检测基线与阈值 | 给出合法 STUN 属性值熵的公开基线（最高 4.392 bits）与 4.5 bits 阈值 | 高 | 是（可直接用于其他协议预留字段检测） |
| 签名引擎 vs 协议语法的量化学差异 | Suricata 8 无 STUN 解析器导致熵粒度被迫粗化，量化了 41.2%→100% 的精度差 | 中 | 是（评估方法论） |

### 5.3 适用场景

进攻侧：红队从被攻陷的 VoIP 电话/边缘路由器做隐蔽横向与 C2；企业网络 allow-by-default 的 STUN 政策下。防御侧：把熵/属性级检查接入 NIDS 作为 RTC 信令的补充监控；对 UDP/3478 做 per-endpoint 限速与服务器白名单（作者承认后者运营上难落地）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| SIP 信令嵌入（Mazurczyk 2008 等） | 早期验证信令平面可行 | 修改既有字段，可被字段完整性/统计检测 | 不改既有字段，只增 RFC 允许忽略的属性 |
| RTP/VAD 媒体嵌入（Schmidt 2018） | 容量可观 | 需媒体会话；ML 检测线成熟 | 无需媒体会话，握手前即可用 |
| WebRTC 流改造（Protozoa/Stegozoa） | 高吞吐、抗封锁（Snowflake 佐证） | 需编解码器改造与已建立会话 | 位于更低协议层，资源受限设备可用 |
| TURN 中继滥用（Crosser 2025） | 借用受信会议域 | 依赖可撤销的短时凭据 | 只需自建 STUN 端点，无平台可撤销面 |
| 签名式 NIDS（Snort 3 / Suricata ET Open） | 部署广、零改造 | 对协议合规信道零告警 | 量化了该缺口并给出熵规则补丁 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

三类实验：(1) 逃逸评估——把隐蔽信道 pcap 依次送 Snort 3（Talos 47,143 规则）、Suricata 8（ET Open）、Zeek（spicy_STUN）、FortiGate 40F（全 UTM，含 DPI/IPS/应用控制）、Palo Alto VM-Series（PAN-OS v11.1.13-h1，AWS EC2）；(2) 性能评估——生产互联网路径（client Debian 13 / AS12338，relay OVH VPS / AS16276，23 跳）验证可用性，LAN 路径做 MTU 扫描，WAN 路径（EdgeRouter X）做可行性验证；(3) 检测评估——熵检测器与 Suricata 8 规则在合法语料上的对照。测试拓扑含 Scenario A/B/C（B 为 FortiGate 40F 垂直架构、C 为 AWS + Palo Alto 虚拟化架构）。

### 6.2 数据集

| 数据集 | 规模 | 用途 |
|---|---|---|
| 自采集隐蔽信道流量 | Zeek 解析 4,575 条 STUN 消息，其中 3,646 条携带数据、929 条为空轮询；tcpdump 计 2,287 请求 + 2,287 响应（Table 11）；平均属性载荷 190.4 B（最大 1596 B） | 攻击侧评估与熵检测真阳性 |
| ITC-Net-blend-60 | 36 GB 原始 PCAP，60 个 Android 应用 × 5 网络场景，59 个可用采集；其中仅 8 个应用产生可完整解析的 STUN 流量，共 3,185 条 STUN 消息、1,358 条含可选属性 | 合法流量基线（FP 计量） |
| MAWI | 每年 2 月第一个周一的 900 秒快照，2019–2026 | STUN 流量纵向趋势（因载荷被移除，仅能用 3478 端口做保守下界估计） |
| Shodan | 154,643 台公开可达 STUN 服务器（2026-02-02） | 基础设施普及度佐证 |

### 6.3 Baseline

四类检测器作为对照：Snort 3（Talos 规则集）、Suricata 8（ET Open；另加本文熵规则）、Zeek（spicy_STUN，另加本文熵脚本）、以及两台 NGFW（FortiGate 40F v7.6.6 build3652 全 UTM；Palo Alto VM-Series PAN-OS v11.1.13-h1）。

### 6.4 评价指标

TP / FP / Recall / Precision（检测侧）；吞吐 Mbps（MTU 扫描 30 runs × 10 s；WAN 60 s iperf3）、RTT / 抖动（100 次 ping）；以及纵向流量倍数与服务器数量。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| 逃逸（Snort 3，47,143 规则） | TP | 0 | — | — | 完全无告警（Table 14） |
| 逃逸（Suricata 8 ET Open） | TP | 0 | — | — | 仅 ET INFO 信息级事件：隐蔽流量 4574 条、合法流量 6459 条，不可区分 |
| 逃逸（FortiGate 40F 全 UTM） | 判定 | 识别为 STUN（app ID 16573） | — | — | 无告警、无阻断 |
| 逃逸（Palo Alto VM-Series） | 判定 | 分类为 STUN | — | — | 无安全告警；逐属性分析留作未来工作 |
| 熵检测（Zeek，逐属性） | Recall / FP | 100.0% (3646/3646) / 0 | — | — | 阈值 4.5 bits；合法最高熵 4.392 bits |
| 熵检测（Suricata 8 规则，消息级） | Recall / Precision | 100.0% / 41.2%（T=4.5, FP 5215） | T=5.75 时 56.2% / 100.0% | — | 粒度粗化导致 4.5 阈值不可用（Table 12） |
| 速率检测（detection_filter，207/60 s） | 告警 / FP | 1682 / 0 | — | — | 隐蔽峰值 2050 请求/60 s，合法峰值 207（Google Meet） |
| 吞吐（Yealink，LAN） | Mbps | 4.11（MTU 500）→ 19.61（MTU 8000） | — | — | 由设备 CPU 与 MTU 限制 |
| 吞吐（EdgeRouter X，WAN） | Mbps | 41.9 / 41.4（MTU 1400） | 直连 243 | 17% | STUN 封装 + 用户态 I/O + ChaCha20 开销 |
| 时延 | ms RTT | 49.4（抖动 3.2） | 基线 33.2（抖动 1.8） | +16.2 ms | 协议开销 + 轮询同步 |
| 基础设施纵向（MAWI） | 倍数 | 2019→2026 STUN 流增长 239× | — | — | 2021 年后与 WebRTC 普及同步上升 |

### 6.6 优势最明显的场景

企业边界对 RTC 采取 allow-by-default 且未部署统计/行为分析的环境——此时隐蔽信道在任何签名引擎下都是"隐形"的；以及资源受限的嵌入式设备（IP 电话、边缘路由器）作为植入点。

### 6.7 局限性

作者自陈 + 笔记补充：严格 STUN 服务器白名单可立即阻断该信道（但运营上罕见）；固定轮询间隔是可被时序分析识别的指纹（当前实现未加抖动）；吞吐受轮询率约束，提高轮询率会增加 PPS 异常暴露面；包长近似恒定（≈1450 B）与合法流量差异明显；熵检测可被自适应填充规避；合法基线不含企业 VoIP/SIP 场景，可能低估合法熵分布上界。

---

## 7. 学习与应用

### 7.1 是否开源？

**原文自相矛盾**：§2 Ethical considerations 明确写 "The source code for the covert channel prototype is not publicly released"，仅对具备机构身份的合格研究者开放；而同篇 Data availability 段写 "Research Link Provided — Google Drive Share - PCAPs, Source Code, Scripts, Logs (Original data)"。两处并列如实记录，`code` 字段填 `unknown`。

### 7.2 复现关键步骤

1. 自建 STUN relay（UDP/3478）与 client implant，使用 comprehension-optional 属性类型 0x8FAD 承载分片后的以太网帧（TAP 接口）。
2. 实现 client 周期性 Binding Request 轮询 + relay 侧 per-client FIFO 环形缓冲，以支持下行。
3. 在目标嵌入式设备（ARM/MIPS）交叉编译部署，验证 NAT 拓扑无关性（所有事务由内网发起）。
4. 采集隐蔽流量 pcap，用 Zeek 8.1.1 + spicy_STUN 逐属性计算 Shannon 熵，验证 4.5 bits 阈值分离度。
5. 在 Suricata 8 用 entropy 关键字写等价规则（注意 offset 20 的粗粒度限制），扫阈值观察 precision/recall 权衡。

### 7.3 关键超参数、预处理和训练细节

属性类型 0x8FAD；tap0 MTU 扫描 500–8000 B；轮询间隔 10 ms（吞吐测试）与保守间隔（隐蔽优先）；ChaCha20 加密载荷；Entropy 阈值 4.5 bits（Zeek）/ 5.75 bits（Suricata 8 规则）；速率阈值 207 请求/60 s/源 IP；Zeek 8.1.1 + spicy_STUN 解析；Suricata 8 `dsize:>50` 过滤短保活。

### 7.4 能否迁移到其他任务？

- **检测范式迁移**：把"协议预留字段的载荷熵 + 属性级粒度"用于其他可扩展协议（SIP 扩展头、QUIC 传输参数、DNS EDNS0 选项、HTTP/2 自定义帧）的隐蔽信道检测。
- **评估范式迁移**：量化"签名引擎 vs 协议语法解析"的检测粒度差异，可作为 NIDS 能力评估的模板。
- **数据侧**：ITC-Net-blend-60 的合法 STUN 属性熵基线（最高 4.392 bits、加权均值 2.95）可直接作为后续工作的对照分布。
- **反面教训**：论文揭示"仅报告召回率"的检测评估不可靠——同一阈值在 Zeek 与 Suricata 上的精度差 58.8 个百分点。

### 7.5 对我的研究有什么启发？

- 加密流量分析的方法论可反向用于隐蔽信道检测：熵/分布类统计量在"载荷为密文"与"载荷为结构化元数据"两种情形下差异极大（6.247 vs 4.392 bits），这是"密文可区分性"的一个具体例证。
- 论文的自陈局限（§10.1.3 自适应填充规避、§11.2 轮询指纹、§11.5 固定包长）实际上是四个可攻击点，可作为隐蔽信道检测研究的选题清单。
- 对"未知/异常流量"评估而言，合法基线的代表性（此处为 Android 应用 vs 企业 VoIP）再次成为结论强度的决定因素。

---

## 8. 总结

### 8.1 核心思想

> 协议"必须忽略"的字段，就是合规的隐藏信道。

### 8.2 速记版 Pipeline

1. 选载体：STUN comprehension-optional 属性（0x8000–0xFFFF），容量 ≈1450 B。
2. 封装：TAP 以太网帧分片写入自定义属性 0x8FAD，UDP/3478 发出（可 ChaCha20 加密）。
3. 双向化：client 轮询 Binding Request，relay 用 FIFO 环缓存在响应中回送下行数据。
4. 部署：ARM IP 电话 / MIPS 边缘路由器；实测四类检测器全部漏报。
5. 检测：Zeek 逐属性 Shannon 熵，H>4.5 bits → 3646/3646 检出、0/1358 误报；Suricata 8 等价规则需 5.75 bits 才能零误报（召回降至 56.2%）。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[tunnel-detection]] — 隐蔽隧道（L2 over STUN）的构造与检测构成本文主线
- [[anomaly-detection]] — 以熵阈值区分隐蔽与合法信令，属统计异常检测范式
- [[malicious-traffic-detection]] — C2 隐蔽信道检测归属恶意流量检测范畴

### 9.2 相关方法

（无直接对应页：本文不使用 kb 方法白名单中的任何方法范式——检测依赖 Shannon 熵与协议语法解析，非机器学习方法。）

### 9.3 相关任务

- [[tunnel-detection]] — 主任务：隐蔽信道设计与识别
- [[anomaly-detection]] — 无监督式的统计异常判别

### 9.4 可更新的综述页面

- [[survey-malicious-traffic-detection]] — 可增补"协议合规型隐蔽信道（covert channel）"这一类 C2 载体及其检测缺口

### 9.5 可加入的对比表

（不适用：本文既非分类方法论文、亦未提出新数据集。）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| Snort 3（47,143 条 Talos 规则）对 3646 条载密消息 0 告警 | Table 14 检测汇总 | §8.2.1、Table 14 |
| Suricata 8 ET Open 仅产生 ET INFO 信息级事件，无法区分隐蔽与合法（隐蔽 4574、合法 6459 条） | Table 11 + Table 14 脚注 | §10.2 |
| FortiGate 40F（全 UTM）识别为 STUN 应用（ID 16573）但无告警 | 逃逸评估 | §8.2.3、Table 4 |
| Palo Alto VM-Series（PAN-OS v11.1.13-h1）分类为 STUN，无安全告警 | 逃逸评估 | §8.1.2 Scenario C |
| 隐蔽信道属性熵均值 6.247 bits（范围 5.154–7.856），合法最高 4.392 bits（Telegram）、加权均值 2.95 bits | Table 9 + Table 10 | §10.1.1 |
| 4.5 bits 阈值下 3646/3646 检出、0/1358 误报（Zeek 逐属性粒度） | Table 10 | §10.1.1 |
| Suricata 8 熵规则（消息级粒度）：T=4.5 → 3646 TP / 5215 FP / 41.2% 精度；T=5.75 → 2049 TP / 0 FP / 56.2% 召回 | Table 12、Table 13 | §10.3 |
| 速率规则 detection_filter 207/60 s → 1682 告警 / 0 误报；但把轮询间隔降到 2 s 即可把速率压到 <30/min 规避 | Table 15 及规则实验 | §11.3 |
| 合法 STUN 中 42.6%（1358/3185）消息本身含可选属性，故"含可选属性"不是有效特征 | Table 8 | §10.1 |
| 隐蔽流量平均属性载荷 190.4 B（最大 1596 B），比合法最大值 24 B（Skype）大一个数量级 | Table 9 | §10.1.1 |
| 吞吐：MTU 500→8000 B 时 4.11→19.61 Mbps（Yealink LAN）；EdgeRouter X 生产 WAN 为 41.9/41.4 Mbps，直连 243 Mbps（17%） | Table 6 + §9.4 | §9.2、§9.4 |
| 时延：RTT 33.2 ms → 49.4 ms（+16.2 ms），抖动 1.8→3.2 ms | Table 7 | §9.3 |
| 纵向：Shodan 收录 154,643 台公开 STUN 服务器（2026-02-02）；MAWI 中 STUN 流 2019→2026 增长 239× | §5.3 | §5.3、§5.3.1 |
| 源码公开性自相矛盾：§2 称不公开，Data availability 称提供 Google Drive 链接 | 两段原文并列 | §2、Data availability |
| 企业侧对策：STUN 服务器白名单可立即阻断但运营不可行；per-endpoint 限速可降带宽而不影响合法信令 | 缓解讨论 | §10、§11.1 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-JCS-STUN_comprehension-optional_attributes_as_a_covert_channel__Design_implementation_and_detection.pdf
- MinerU Markdown：02-parsed-markdown/2026-JCS-STUN_comprehension-optional_attributes_as_a_covert_channel__Design_implementation_and_detection.md

---

## 12. 后续问题

- 熵检测的可规避性（§10.1.3 低熵填充）意味着需要多维联合判据（熵 + 包长分布 + IAT 周期性 + 缺少后续 RTP/SRTP 媒体流），论文只点了方向未做实验。
- 合法基线缺企业 VoIP/SIP 场景，阈值 4.5 bits 的普适性存疑；作者亦承认无公开数据集可用。
- Suricata 8 若引入 STUN 应用层 sticky buffer，规则精度可望与 Zeek 持平——这是"解析深度决定检测上限"的一个干净实验。
- 未与 ML 类检测器（如针对 RTC 时序/长度的分类器）对比，检测能力上界不明。
- 该信道与 ECH/QUIC 等新协议栈共存时（STUN over QUIC、TURN over TLS）的可迁移性未讨论。

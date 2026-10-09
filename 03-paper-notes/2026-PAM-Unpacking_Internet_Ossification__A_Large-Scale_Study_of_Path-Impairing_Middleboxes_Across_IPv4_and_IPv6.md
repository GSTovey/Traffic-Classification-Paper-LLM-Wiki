---
type: paper
title_original: "Unpacking Internet Ossification: A Large-Scale Study of Path-Impairing Middleboxes Across IPv4 and IPv6"
title_cn: "解构互联网僵化：跨越 IPv4 与 IPv6 的路径损伤型中间盒大规模研究"
authors: [Fahad Hilal, Taha Albakour, Oliver Gasser, Kevin Vermeulen]
year: 2026
venue: "PAM 2026"
doi: "unknown"
url: "unknown"
pdf: "00-inbox/PDFs/2026-PAM-Unpacking_Internet_Ossification__A_Large-Scale_Study_of_Path-Impairing_Middleboxes_Across_IPv4_and_IPv6.pdf"
mineru_md: "02-parsed-markdown/2026-PAM-Unpacking_Internet_Ossification__A_Large-Scale_Study_of_Path-Impairing_Middleboxes_Across_IPv4_and_IPv6.md"
status: processed
reading_level: L2
research_area: []
task: []
method: []
dataset: [Tranco Top 1M, Routeviews, CAIDA AS Classification, RIPE Atlas]
code: "unknown"
relevance: medium
created: "2026-09-19"
updated: "2026-09-19"
---

# Unpacking Internet Ossification: A Large-Scale Study of Path-Impairing Middleboxes Across IPv4 and IPv6

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Unpacking Internet Ossification: A Large-Scale Study of Path-Impairing Middleboxes Across IPv4 and IPv6 |
| 中文标题 | 解构互联网僵化：跨越 IPv4 与 IPv6 的路径损伤型中间盒大规模研究 |
| 作者 | Fahad Hilal, Taha Albakour（MPI for Informatics，德国 Saarbrücken）, Oliver Gasser（IPinfo，美国）, Kevin Vermeulen（LIX, CNRS, École Polytechnique，法国） |
| 年份 | 2026 |
| 会议/期刊 | PAM 2026（Passive and Active Measurement） |
| 研究方向 | （kb 概念白名单不含互联网测量/中间盒方向：本笔记对应字段留空，理由见 §9.1） |
| 任务类型 | 互联网规模路径测量：路径损伤型中间盒的普查、定位、纵向动态与运营方调研 |
| 方法关键词 | Yarrpbox（+ECN 扩展）、Highest Confidence Middlebox (HCMB) 度量、9 个观测点、TCP SYN 选项探测（MSS/SACK Permitted/MP Capable/Timestamp）、行为四分类（ND/DT/DF/PB）、供应商指纹识别（Nmap/Censys/SNMPv3） |
| 数据集 | Tranco Top 1M、Routeviews（BGP 映射）、CAIDA AS Classification / AS Relationship、PeeringDB、RIPE Atlas（交叉验证） |
| 是否开源 | 解析稿未提及代码/数据发布；文中称将部署并定期刷新一个供运营商查询的 web 服务，但其 URL 在解析稿中被截断（"The service is available at:" 之后为空）→ code: unknown |
| PDF | 00-inbox/PDFs/2026-PAM-Unpacking_Internet_Ossification__A_Large-Scale_Study_of_Path-Impairing_Middleboxes_Across_IPv4_and_IPv6.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-PAM-Unpacking_Internet_Ossification__A_Large-Scale_Study_of_Path-Impairing_Middleboxes_Across_IPv4_and_IPv6.md |

> 注：解析稿中未见论文自身 DOI/URL（文末参考文献之外的标识缺失），故 `doi`/`url` 填 `unknown`。

---

## 1. 一句话总结

> 用 Yarrpbox 从 9 个观测点探测 251.6M 条 IPv6 与 156.9M 条 IPv4 路径，量化路径损伤型中间盒：IPv6 受累前缀比 IPv4 少 6 倍、AS 少 13 倍，最高 87% 的损伤是剥离 MPTCP 的 MP Capable；并首次给出小时级与跨年（2022→2024）动态，指出设备默认配置可能是主因之一。

---

## 2. 摘要翻译

### 2.1 摘要原文

> The end-to-end principle that limits on-path devices to simple tasks such as forwarding and routing has been one of the backbones of the Internet's architecture. This is, however, being challenged as Internet paths now contain devices that inspect, filter, modify, or even discard packets. Some of these carry out benign and positive undertakings such as balancing resources and thwarting attacks, while others interfere with packets in unexpected ways leading to broken paths, thus inhibiting the deployment of new protocols or even extensions. While Internet ossification has already been studied in prior work, we propose to address new research questions enabled by recent Internetscale middlebox mapping techniques. Combining Internet-scale measurements, measurements towards popular domains, repeated measurements, and longitudinal measurements, both in IPv6 and IPv4, we provide a multi-dimensional study on path-impairing middleboxes in the Internet. Our findings reveal that six times fewer IPv6 prefixes are afected than IPv4 prefixes by path-impairing middleboxes, and that there is an opportunity to switch between IPv4 and IPv6 to evade path-impairing middleboxes. Looking into the nature of path-impairments, we find that up to 87% relate to the usage of Multipath TCP. We also present the first results about the dynamics of these middleboxes, at both short (over hours), and long (over years) time windows. We show that path-impairing middleboxes have a consistent behavior over hours and that their number has tripled since 2022 for IPv6. We complement our measurements with operator perspectives and set up a service designed to help operators uncover and address unintentional path-impairments in their networks. Finally, we highlight default configurations as one potential contributor to path-impairments.

> ⚠️ MinerU 解析问题：abstract 标题被解析为 "Ab t t"，摘要与正文系统性丢失 ff/fi/ffi 连字与 small-caps 字母（"afected"、"trafic"、"diferent"、"of" 应为 "off"）；引文序号 [27]/[34] 在正文中多处指向 Edeline & Donnet 与 Hilal & Gasser 两篇前作，但解析稿的编号在不同段落间存在混用，笔记中一律以作者名指代。

### 2.2 摘要中文翻译

限制在途设备只做转发与路由等简单任务的端到端原则，曾是互联网架构的支柱之一；但如今互联网路径上存在会检查、过滤、修改甚至丢弃数据包的设备，这一原则正受到挑战。这些设备中，有些执行的是良性且积极的工作（如资源均衡、抵御攻击），另一些则以意外方式干扰数据包、导致路径损坏，从而抑制新协议乃至新扩展的部署。互联网僵化（ossification）此前已有研究，本文则借助近期的互联网规模中间盒测绘技术回答新的研究问题。作者结合互联网规模测量、面向热门域名的测量、重复测量与纵向测量，在 IPv6 与 IPv4 两个族上给出一项多维度研究。结果发现：受路径损伤型中间盒影响的 IPv6 前缀比 IPv4 少六倍，并且存在通过在 IPv4/IPv6 之间切换来规避这类中间盒的机会。在损伤性质上，最高 87% 与 Multipath TCP 的使用有关。作者还首次给出这些中间盒在短时（小时级）与长时（年级）窗口上的动态：路径损伤型中间盒的行为在数小时内保持一致，且 IPv6 侧的数量自 2022 年以来增长到三倍。作者用运营商视角补充了测量，并搭建了一个服务以帮助运营商发现并修复其网络中非故意的路径损伤。最后，作者指出设备默认配置是路径损伤的潜在成因之一。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 端到端原则已成"遗物"：路径上遍布防火墙、TCP 加速器、负载均衡器等中间盒；其中一部分会以不可预测的方式干扰新协议/扩展，使 TCP 扩展长期"被打压"，DCCP/SCTP 等替代传输协议难以规模化部署。
- 既有中间盒研究"大多停留在路径维度、且多为一次性快照"（§1）。作者主张把视角从单条路径提升到**受影响的网络与前缀层级**，并补充纵向与短时动态以及运营商视角。

### 3.2 现有方法的痛点和不足

| 既有工作 | 做法 | 局限 |
|---|---|---|
| TBIT（Medina 等） | 用不同 IP/TCP 选项探测 web 服务器 | 能发现中间盒但不能定位 |
| TCP HICCUPS / Honda 等 | 修改 TCP 栈检测在途中间盒 | 需控制连接两端，难以大规模 |
| Tracebox（Edeline & Donnet [27]） | 检测逐跳修改，测 Alexa Top 1M 上的 IPv4 损伤 | 有状态、慢，不适合全网普查；仅 IPv4；VP 为已退役的 PlanetLab |
| Yarrpbox（Hilal & Gasser [34]） | 无状态高速中间盒探测，可在 35–55% 情形定位 | 主要贡献是工具与初步普查，未系统回答前缀/AS 级影响与动态 |
| 本文 | 在前者基础上扩展到 IPv6+IPv4、前缀/AS/域名三层、小时级与跨年动态、成因与运营商调研 | — |

### 3.3 论文的研究假设或核心直觉

核心直觉：路径级统计只能说明"存在损伤"，无法说明损伤在网络结构上的分布与演化；若把损伤映射到 BGP 前缀、AS 与热门域名，并观察其时间动态，可以暴露系统性的僵化模式（例如某一地址族整体更"僵化"、损伤集中在目的网络、默认配置是主因），从而给出可操作的解僵化建议。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 新协议/扩展（QUIC、TLS 1.3、MPTCP）必须"中间盒抗性"或自带回退；TCP 扩展持续被篡改 | §1 |
| 痛点提炼 | 损伤导致路径损坏、调试困难、创新受阻；但社区缺乏对损伤在网络层级分布与演化的量化认识 | §1、§2 |
| 问题转化 | 提出 6 组研究问题（路径/AS 影响、热门域名影响、行为类型、在途位置、时间动态、与运营商互动），并在 Table 1 中逐条对照前作覆盖情况 | §2、Table 1 |
| 文献定位 | 前作覆盖部分维度（多数为单地址族、单次快照、无动态、无运营商互动），本文补足空白 | Table 1 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | IPv6 路径/前缀/AS 受路径损伤型中间盒影响的比例显著低于 IPv4，因而 IPv6 是更少僵化的创新试验场 | §1（推断） | 双族互联网规模测量（§4） |
| 辅助假设 1 | 损伤主要由少数行为类型（如 MP Capable 剥离）主导，且多数中间盒位于目的网络内 | 前作 [27,34] 的线索 | 行为分类统计（§6）+ 拓扑定位（§7） |
| 辅助假设 2 | 路径损伤型中间盒的行为在小时与年级尺度上稳定（非偶发） | §1（推断） | 连续 5 次重复扫描 + 2022/2024 对照（§8） |
| 辅助假设 3 | 部分损伤源于厂商设备的默认配置而非显式策略 | 运营商调研与文献矛盾（§9） | 厂商文档核对 + 设备指纹识别（§10） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | 受损伤路径 IPv6 0.11% vs IPv4 0.24%；受影响前缀 1,808（0.9%）vs 11,423（1.1%）；受影响 AS 339（1%）vs 4,565（6.1%） | §4.2、Table 3 |
| 辅助假设 1 | 支撑 | DF 行为占 IPv6/IPv4 受损路径的约 88%/95%，其中 MP Capable 剥离为主；多数中间盒在目的 AS 内 | §6、§7、Table 6 |
| 辅助假设 2 | 支撑 | 约 80%（IPv6）/96%（IPv4）设备在所有扫描中始终生效；2022 年识别出的 HCMB IP 多数在 2024 年仍在干扰（IPv6 重叠 72.7%，剔除不响应后 91%） | §8.2、§8.5、Table 8 |
| 辅助假设 3 | 部分支撑 | 11 位受访运营商均否认配置过滤策略，但测量显示存在显式策略；Cisco/Citrix/Palo Alto 文档明确默认移除或替换不支持的 TCP 选项为 NOP；识别出 58 家厂商覆盖 2,033 台中间盒（48%） | §9、§10 |

---

## 4. 方法设计

### 4.1 方法整体流程

用 Yarrpbox（无状态、traceroute 风格、Paris traceroute 式探测）向 BGP 宣告前缀与 Tranco Top 1M 解析出的服务器 IP 发送携带四个 TCP 选项（MSS、SACK Permitted、MP Capable、Timestamp）的 TCP SYN；从 ICMP Time-Exceeded 响应中回引的 IP 头/负载提取编码状态，与发出值比对以判定在途修改；用 Highest Confidence Middlebox 度量定位责任设备；再把设备映射到 BGP 前缀/AS/AS 类型与拓扑位置，并在短时与跨年窗口上比较。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 目标选取 | BGP 宣告前缀（IPv6 每前缀 100 个随机地址；IPv4 全部可路由 /24 各 1 个地址）、Tranco Top 1M（massDNS 解析 A/AAAA） | 生成目标列表 | 目标集 | 覆盖全网与热门域名两类视角 |
| Step 2 探测 | TCP SYN（端口 80 与 443），携带 MSS/SACK Permitted/MP Capable/Timestamp；本次扩展 Yarrpbox 支持 ECN | TTL 受限探测 | ICMP Time-Exceeded 响应 | 提取在途修改 |
| Step 3 损伤判定 | 回引字段 vs 原始字段 | 判定是否落在"关键字段集"（IP Payload/Total Length、SACK Permitted、Rcv Window、MP Capable Sender Key、Timestamp、MSS、MP Capable、NOP、Sequence Number） | 损伤记录 | 过滤良性/不确定干扰 |
| Step 4 定位 | 首次报告干扰的跳与其后一跳 | HCMB 度量（可放宽到 AS 级） | HCMB IP / AS 级位置 | 责任设备归因 |
| Step 5 映射与分类 | HCMB IP | 映射到 Routeviews 的 BGP 前缀/AS、CAIDA AS 类型、AS 关系（源网络/对端/提供方/目的网络…） | 前缀/AS/拓扑位置统计 | 回答"影响谁""在哪生效" |
| Step 6 动态与成因 | 5 次连续扫描 + 2022 公开数据 + 厂商文档与指纹 | 稳定性判定、跨年对比、Nmap/Censys/SNMPv3 识别厂商 | 动态与成因结论 | §8、§10 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Yarrpbox（+ECN 扩展） | 无状态高速中间盒探测与定位 | 目标 IP 列表 | 路径与干扰记录 | 核心测量引擎 |
| HCMB 度量 | 从"潜在中间盒跳"筛出高置信中间盒 | 逐跳响应 | HCMB IP / AS 级位置 | 决定归因可信度 |
| 观测点（9 个） | 提供路径多样性 | — | 多视角测量 | 8 个 AWS（六大洲：印度、巴西、德国、美西、南非、澳大利亚、瑞典、美东）+ 1 个大学 VP |
| 行为四分类 | ND / DT / DF / PB（+Multi） | 干扰字段与后果 | 行为标签 | 支撑 §6、§8.4 |
| 辅助数据集 | 富化与交叉验证 | CAIDA、PeeringDB、Routeviews、RIPE Atlas | AS 类型/关系/别名 | 支撑 §4.4、§7、附录 A |

### 4.4 公式、算法和机制解释

- 探测原理：依赖 RFC 1812/4443（IPv6）与 RFC 792——路由器对 TTL 过期包应回引 IP 头与完整负载或前 64 位；Yarrpbox 在探测包中编码状态（目的 IP、TTL 等），未用于编码的字段保持固定值，从而通过比对回引字段发现修改。
- 定位：第一个报告在途干扰的跳记为"潜在中间盒跳"，其回包地址为"潜在中间盒"；若其前一跳紧邻且回引包长不小于前者，则为 HCMB IP；否则放宽到 AS 级。
- 行为四分类：ND（协商破坏，如 SACK Permitted 移除、MP Capable 发送方密钥改动）、DT（流量扰乱，如 TCP Sequence Number 与接收窗口篡改）、DF（特性禁用，如剥离 TCP 选项/禁用 ECN）、PB（潜在阻断，如仅改长度字段——IPv6 下 71%、IPv4 下 99% 的此类改动导致后续无流量）。
- 排除项：IPv6 的 Traffic Class、IPv4 的 DSCP、TCP MSS 数据修改等被视为良性或不确定干扰而不计入。

### 4.5 方法优势

- 无状态设计使其可做互联网规模普查：本次测试路径数约为前作的三倍，观测到的在途路由器 AS 数约为前作的十倍。
- 双地址族 + 多 VP（六大洲，云/学术/ISP）覆盖，避免了单一网络视角的系统偏差。
- 每前缀 100 个随机地址的采样显著提升"前缀是否受损"判定的召回（相对每前缀单地址）。
- 结合测量、运营商调研与厂商文档，形成"观测—归因—建议"闭环。

### 4.6 方法不足

- 观测点有限（9 个），作者承认无法覆盖所有源网络，安静中间盒可能被漏检；IPv4 侧因路由器普遍遵循 RFC 792 仅回引 64 字节，定位不确定性显著更高（>60% 的 IPv4 路由器如此）。
- 仅探测端口 80/443 且 SYN 必带 MP Capable，因此无法观测"因 MP Capable 存在而阻断"的情形。
- AS 类型分析使用 2021 年 CAIDA 分类数据（作者以 AS 类型极少变更为由接受）。
- 解析稿中服务 URL 被截断，无法复核该运营商自助服务。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 维度 | 前作（Tracebox / Yarrpbox 初版） | 本文 |
|---|---|---|
| 规模 | 有限（有状态、慢） | 251.6M IPv6 + 156.9M IPv4 路径 |
| 地址族 | 多为 IPv4 | IPv4 + IPv6 对照 |
| 分析层级 | 路径 | 路径 + 前缀 + AS + 域名 |
| 时间维度 | 单次快照 | 小时级重复 + 2022→2024 纵向 |
| 成因与互动 | 无 | 运营商调研 + 厂商默认配置分析 + 自助服务 |

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| IPv6/IPv4 双族互联网规模中间盒普查 | 前缀/AS 级受损面量化（IPv6 少 6 倍前缀、13 倍 AS） | 高 | 是（任何地址族/协议对照测量） |
| 地址族切换规避的可行性量化 | 6.1% 仅 IPv4 受损域名有 AAAA 记录，可切到 IPv6 获得无损伤路径 | 高 | 是（协议栈选路策略设计） |
| 首次给出中间盒短时与跨年动态 | 小时级稳定性 + IPv6 受损前缀两年翻 3.6 倍 | 高 | 是 |
| 默认配置成因分析 | 厂商文档（Cisco/Citrix/Palo Alto 默认将不支持选项替换为 NOP）+ 58 家厂商覆盖 48% 设备 | 中 | 是（设备合规与采购评估） |
| 运营商调研与自助服务 | 11 份问卷 + 面向运营商的查询服务 | 中 | 是（测量-运维闭环范式） |

### 5.3 适用场景

协议设计者评估新扩展的部署可行性（尤其 MPTCP/ECN/SACK）；运营商自查网络中非故意的策略性损伤；内容/CDN 方判断是否应优先在 IPv6 上启用新特性。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| TBIT | 早期、可探测 ECN/PMTUD/TCP 选项交互 | 只发现不能定位 | 引入 HCMB 定位 |
| Tracebox（Edeline & Donnet） | 逐跳定位、可测多种干扰 | 有状态、慢、仅 IPv4、PlanetLab VP 已退役 | 无状态全网规模 + 双族 + 动态 |
| Yarrpbox 初版（Hilal & Gasser） | 无状态、可定位 35–55% | 仅初步普查 | 系统化研究 + 成因与运营商视角 |
| 本文 | 规模 ×3、AS 覆盖 ×10、双族、纵向 | VP 有限、IPv4 定位不确定性大 | — |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

四类测量：(i) 互联网规模——面向 BGP 宣告前缀的 IPv6（每前缀 100 随机地址）与 IPv4（每个 /24 一地址）扫描，2024 年 3 月（端口 80）与 9 月（端口 443）；(ii) 热门域名——Tranco Top 1M 解析后的服务器 IP，2024 年 7 月末（80）与 9 月首周（443）；(iii) 重复扫描——连续 5 次（IPv6 每次最长 14 h，IPv4 约 3 h）；(iv) 纵向——用 2022 年公开数据 [34] 复刻测量（同 VP、同 TCP 选项、同目标种子）。VP 速率：AWS 1 kpps，大学 VP IPv6 5 kpps / IPv4 20 kpps。

### 6.2 数据集

| 数据集 | 规模 | 用途 |
|---|---|---|
| 前缀级扫描（Table 2） | IPv6：20.2M 目标、1.5M 跳 IP、14.3k AS、251.6M 路径；IPv4：11.7M 目标、1.2M 跳 IP、29.2k AS、156.9M 路径 | 主分析 |
| 热门域名扫描（Table 5 相关） | 423.6k 唯一 IPv6 与 667.6k 唯一 IPv4 服务器 IP；IPv6 1.6M / IPv4 3.1M 路径；IPv6 16.7M 响应/91.5k 路由 IP/3k AS，IPv4 72.9M 响应/284.9k 路由 IP/13.3k AS | 热门域名视角 |
| 2022 对照数据 | IPv6 86.7M 路径（2022）vs 127.6M（2024）；IPv4 87.8M vs 相近 | 纵向对比 |
| 辅助数据 | Routeviews、CAIDA AS Classification（2021）/AS Relationship、PeeringDB、RIPE Atlas（Metis 选 200 AS 探针） | 映射与交叉验证 |

### 6.3 Baseline

历史对照为 Edeline & Donnet [27]（2016 年 Alexa Top 1M、89 个 PlanetLab 节点，报告约 6.5% 的 IPv4 路径受损）与 Hilal & Gasser [34]（2022 年公开数据，用于纵向比较）。

### 6.4 评价指标

受损路径占比、受影响前缀数与占比、受影响 AS 数与占比、HCMB IP 数量、行为类型分布（ND/DT/DF/PB）、拓扑位置分布、设备活跃度（始终生效比例）、跨年重叠率。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文结果 | 对比 | 说明 |
|---|---|---:|---:|---|
| 受损路径 | 占比 | IPv6 0.11%（277.6k）/ IPv4 0.24%（377.4k） | — | 摘要与 §4.2 |
| 跨中间盒路径 | 占比 | IPv6 16.5%（其中良性 16.2%）/ IPv4 19.8%（良性 19.5%） | — | §4.2 |
| 受影响前缀 | 数量（占比） | IPv6 1,808（0.9%）；IPv4 11,423（1.1%） | 6 倍差距 | Table 3 |
| 受影响 AS | 数量（占比） | IPv6 339（1%）；IPv4 4,565（6.1%） | 13 倍差距 | Table 3 |
| 行为分布 | DF 占比 | IPv6 约 88% / IPv4 约 95% 的受损路径 | — | Table 6 |
| MP Capable 剥离 | 受损路径占比 | IPv6 约 86% / IPv4 约 87.4% | — | §4.2、§6 |
| 热门域名受影响 | 目标（域名） | IPv6 125 目标 / 150 域名；IPv4 7,599 目标 / 8,853 域名（59 倍） | — | Table 5、§5.2 |
| 切换机会 | 域名占比 | 仅 IPv4 受损域名中 544 个（6.1%）有 AAAA 记录 | — | §5.2 |
| 拓扑位置 | 目的 AS 内 | IPv4 近 58% 的 HCMB 在 AS 边界、IPv6 达 85%；DF 行为 IPv6 26% / IPv4 65% 在目标 AS | — | §4.3、§7 |
| 短时稳定性 | 始终生效设备 | IPv6 约 80% / IPv4 约 96% | — | §8.2 |
| 纵向（前缀） | 2022→2024 | IPv6 462→1,682（超 3 倍，占宣告前缀 0.2%→0.8%）；IPv4 9,122→10,012（+8.8%） | 宣告数同期 +33.4%（IPv6） | Table 7 |
| 纵向（HCMB IP） | 2022→2024 | IPv6 231→602（72.7% 重叠，剔除不响应后 91%）；IPv4 2,608→2,818（重叠 43%，剔除后 75.5%） | — | Table 8 |
| 纵向（路径受损率） | 2022→2024 | IPv6 0.07%→0.15%（翻倍）；IPv4 0.19%→0.20%（稳定） | — | §8.3 |
| 运营商调研 | 11 份回复 | 全部声称对 TCP 选项"透明"、无显式过滤策略 | 与测量证据矛盾 | §9 |
| 厂商归因 | 58 家厂商 / 2,033 台（48%） | Cisco 447、Palo Alto 329、Check Point 166；722 台仅得通用 Linux 指纹 | — | §10 |

### 6.6 优势最明显的场景

协议扩展（MPTCP/ECN/SACK）的部署决策：数据表明 IPv6 是明显更"不僵化"的试验场，且约 6.1% 仅 IPv4 受损的热门域名可直接切到 IPv6 获得无损伤路径。

### 6.7 局限性

作者自陈：VP 集合有限且观测到 VP 依赖性（无源网络内 VP 时部分中间盒可能漏检）；IPv4 路径受损比例较 2016 年研究（6.5%）低，作者归因于序列号随机化等历史行为消失、VP 集合差异与托管格局变化，并强调自身数字应视为下界。笔记补充：AS 类型分析依赖 2021 年数据；仅测 80/443 端口且固定携带 MP Capable；服务 URL 在解析稿中缺失。

---

## 7. 学习与应用

### 7.1 是否开源？

解析稿未声明代码或数据发布；作者称已搭建供运营商查询的 web 服务并计划定期刷新，但该服务 URL 在解析稿中被截断（"The service is available at:" 后为空），无法确认 → `code: unknown`。

### 7.2 复现关键步骤

1. 用 Yarrpbox（需扩展 ECN 支持）从多 VP 向 BGP 宣告前缀发 TCP SYN（携带 MSS、SACK Permitted、MP Capable、Timestamp），IPv6 每前缀取 100 个随机地址、IPv4 每个可路由 /24 取 1 个。
2. 从 ICMP Time-Exceeded 回引字段比对原始编码值，按关键字段集判定损伤，并用 HCMB 度量定位（必要时放宽到 AS 级）。
3. 用 Routeviews 把目标映射到前缀/AS，用 CAIDA AS Classification/Relationship 与 PeeringDB 判定 AS 类型与拓扑位置。
4. 连续多次扫描评估短时稳定性；用 2022 年公开数据复刻测量做纵向对比（同种子、同选项）。
5. 通过 Nmap/Censys/SNMPv3 做设备指纹识别，并与厂商默认配置文档比对。

### 7.3 关键超参数、预处理和训练细节

探测选项：MSS、SACK Permitted、MP Capable、Timestamp（四项固定携带）；端口 80 与 443；AWS VP 速率 1 kpps，大学 VP IPv6 5 kpps / IPv4 20 kpps；时间窗：2024-03（80）、2024-07 末（80，域名）、2024-09（443）；短时动态 5 次连续扫描（IPv6 每次 ≤14 h、IPv4 ≈3 h）；AS 分类用 CAIDA 2021 数据。

### 7.4 能否迁移到其他任务？

- **测量方法**：把"在途字段修改 → 结构化归因（前缀/AS/类型/拓扑）→ 时间动态"的三段式用于其它在途干扰问题（DNS 篡改、QUIC 版本协商干扰、ECN 部署受阻）。
- **工程启示**：协议栈在 Happy Eyeballs 之外可考虑"优先选择保留所需传输特性的地址族"，本文给出了这一策略的量化依据。
- **合规/采购启示**：默认配置即剥离未知 TCP 选项这一事实，对设备选型与网络审计流程有直接价值。
- **与流量分析的连接**：路径损伤会改变流量可观测特征（如回退到无扩展的 TCP、连接重试），可作为流量分析中"异常来自网络而非端点"的一种解释变量。

### 7.5 对我的研究有什么启发？

- 论文的"证据层级"设计值得借鉴：同一现象在路径、前缀、AS、域名四个粒度上的一致性检验，显著提高了结论稳健性。
- 对"测量即干预"的伦理处理（限速、blocklist、rDNS 说明、ISP 侧在载荷中留联系方式）是可复用的合规模板。
- 一个可迁移的观察：运营商自述与测量结果系统性矛盾（11 位受访者全部否认过滤，但测量发现显式策略）——在涉及网络行为的其他领域（如 QoS 差异化、审查）同样应优先信任测量而非自述。

---

## 8. 总结

### 8.1 核心思想

> IPv6 比 IPv4 少一分僵化：受损前缀少 6 倍、AS 少 13 倍。

### 8.2 速记版 Pipeline

1. Yarrpbox 从 9 个 VP（8 AWS + 1 大学）向 BGP 前缀与 Tranco 服务器 IP 发带 4 个 TCP 选项的 SYN。
2. 从 ICMP 回引字段比对判定损伤，按 ND/DT/DF/PB 分类，用 HCMB 度量定位责任设备。
3. 映射到前缀/AS/域名：受损路径 IPv6 0.11% vs IPv4 0.24%；受影响前缀 1,808 vs 11,423；AS 339 vs 4,565。
4. 行为与位置：DF（MP Capable 剥离）占 ~88%/95%，多数中间盒位于目的网络；约 80%/96% 设备长期稳定生效。
5. 动态与成因：IPv6 受损前缀 2022→2024 由 462 增至 1,682；Cisco/Palo Alto/Check Point 等默认剥离未知选项，运营商却普遍不知情。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

（kb 概念白名单（anomaly-detection、anonymous-traffic-identification、censorship-circumvention、encrypted-traffic-analysis、few-shot-traffic-learning、malicious-traffic-detection、traffic-classification、traffic-foundation-model、traffic-representation-learning、tunnel-detection、website-fingerprinting）均为流量分析/分类/隐私方向，不含互联网测量与协议僵化（ossification）方向。为避免错列，本文 `research_area` 与本节概念链接留空；仅列出主题邻近的 A 表论文笔记。）

- [[2025-CCS-Fingerprinting_Deep_Packet_Inspection_Devices_by_Their_Ambiguities]] — 主题邻近：对在途检测/干扰设备（DPI）的识别与刻画；本文则刻画在途"改写型"设备（未被本文引用）
- [[2020-CCS-Censored_Planet__An_Internet-wide__Longitudinal_Censorship_Observatory]] — 主题邻近：互联网规模的路径干扰纵向观测方法论（未被本文引用）

### 9.2 相关方法

（无直接对应页：kb 方法白名单为机器学习方法类，本文使用无状态主动测量与拓扑归因，不属其中任何一类。）

### 9.3 相关任务

（无直接对应页：任务白名单以分类/检测类任务为主，本文属互联网测量。）

### 9.4 可更新的综述页面

（不适用：现有综述页均面向加密流量分析/少样本/恶意流量/WF/流量基础模型，本文内容不属其中。）

### 9.5 可加入的对比表

（不适用：本文未提出分类方法或新数据集供横向对比。）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 规模：IPv6 20.2M 目标 / 14.3k AS / 251.6M 路径；IPv4 11.7M 目标 / 29.2k AS / 156.9M 路径（约为前作三倍路径、十倍 AS） | Table 2 | §4.1、Table 2 |
| 受损路径 277.6k（IPv6，0.11%）与 377.4k（IPv4，0.24%）；跨中间盒路径 16.5% / 19.8% | 摘要与 §4.2 | §4.2 |
| 受影响前缀：IPv6 1,808（0.9%）vs IPv4 11,423（1.1%）；受影响 AS：339（1%）vs 4,565（6.1%） | Table 3 | §4.2、Table 3 |
| 最高约 87% 的损伤与 MPTCP 相关：MP Capable 剥离占 IPv6 约 86%、IPv4 约 87.4% 的受损路径 | §4.2、Table 6 | §4.2、§6 |
| DF 行为主导：占 IPv6/IPv4 受损路径约 88%/95%（通过 NOP 覆写实现） | Table 6 | §6 |
| 热门域名：IPv6 125 目标/150 域名受损 vs IPv4 7,599 目标/8,853 域名（59 倍） | Table 5 | §5.2 |
| 切换机会：仅 IPv4 受损域名中 544 个（6.1%）有 AAAA 记录；IPv6 受损域名 5.3% 位于 Tranco Top 10k | §5.2 | §5.2 |
| 拓扑：多数中间盒在目的网络（IPv4 近 58% 在 AS 边界，IPv6 达 85%）；Tier-1 中亦有（如 Cogent AS174） | §4.3、§7 | §7 |
| VP 依赖主要来自路径多样性：97.1%（IPv6）/99.7%（IPv4）的中枢 IP 不出现在其它 VP 的路径上 | §4.5 | §4.5 |
| 短时稳定：约 80%（IPv6）/96%（IPv4）设备始终生效；重复扫描结果一致；存在目的地过滤策略的少数证据 | §8.2 | §8.2 |
| 纵向前缀：IPv6 462→1,682（占宣告前缀 0.2%→0.8%），IPv4 9,122→10,012（+8.8%） | Table 7 | §8.3 |
| 纵向设备：HCMB IP 数 IPv6 231→602（重叠 72.7%，剔除不响应后 91%）；IPv4 2,608→2,818（43%→75.5%） | Table 8 | §8.5 |
| 受损路径率：IPv6 0.07%→0.15%（翻倍），IPv4 0.19%→0.20%（稳定）；PB（长度字段破坏）路径在 IPv6 增加近 8 倍 | §8.3 | §8.3 |
| 行为演化：IPv6 侧 MP Capable 移除占比 33.2%→38.3%；Sequence Number 与 Timestamp/SACK 干扰减半；仅长度字段修改翻倍 | Table 10 | §8.4 |
| 运营商调研（11 份回复，2025-05，RIPE/NANOG）：全部自称对 TCP 选项透明、无显式过滤策略，与测量证据矛盾 | §9 | §9 |
| 厂商默认配置：Cisco、Citrix、Palo Alto 文档明确默认移除/替换不支持的 TCP 选项（含 MPTCP）为 NOP；识别 58 家厂商覆盖 2,033 台中间盒（48%），前三为 Cisco 447、Palo Alto 329、Check Point 166 | §10 | §10 |
| 建议：协议设计者优先在 IPv6 上部署创新特性；运营商应剥离而非丢包；Happy Eyeballs 之外可考虑按"是否保留所需传输特性"选路 | §12 | §12 |
| IPv4 受损比例低于 2016 年研究（6.5%），作者归因于序列号随机化等行为消失、VP 集合与托管格局差异，并声明自身数字为下界 | 附录 C | 附录 C |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-PAM-Unpacking_Internet_Ossification__A_Large-Scale_Study_of_Path-Impairing_Middleboxes_Across_IPv4_and_IPv6.pdf
- MinerU Markdown：02-parsed-markdown/2026-PAM-Unpacking_Internet_Ossification__A_Large-Scale_Study_of_Path-Impairing_Middleboxes_Across_IPv4_and_IPv6.md

---

## 12. 后续问题

- VP 依赖无法彻底消除：论文给出 RIPE Atlas 交叉验证（IPv6 约 39% 前缀在任何 VP 都看不到预期中间盒或别名），这类下界如何改进？
- AS 类型使用 2021 年 CAIDA 数据；若用更新分类，结论是否稳定？
- 仅探测 80/443 且固定携带 MP Capable，其他端口/选项组合下的损伤图景未知。
- 服务 URL 在解析稿中缺失，无法复核"运营商自助查询"可用性。
- "默认配置致损"仅是合理推断，作者亦承认缺少 ground truth；需与设备厂商合作才能确证。
- 对流量分析研究的意义尚待展开：路径损伤造成的静默回退（如 MPTCP 退化为普通 TCP、连接重试）会在流量特征上留下何种可观测痕迹？

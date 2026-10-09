---
type: paper
title_original: "Revelio: A Global Study of VoIP Blocking"
title_cn: "Revelio：VoIP 封锁的全球性研究"
authors: ["Arjun Gupta", "Roya Ensafi", "Piyush Kumar", "Devashish Gosain"]
year: 2026
venue: "USENIX Security 2026"
doi: "unknown"
url: "https://www.usenix.org/conference/usenixsecurity26/presentation/gupta"
pdf: "00-inbox/PDFs/2026-USENIX-Revelio__A_Global_Study_of_VoIP_Blocking.pdf"
mineru_md: "02-parsed-markdown/2026-USENIX-Revelio__A_Global_Study_of_VoIP_Blocking.md"
status: processed
reading_level: L2
research_area: ["censorship-circumvention"]
task: ["app-fingerprinting"]
method: []
dataset: []
code: "https://doi.org/10.5281/zenodo.20362017"
relevance: medium
created: "2026-09-19"
updated: "2026-09-19"
---

# Revelio: A Global Study of VoIP Blocking

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Revelio: A Global Study of VoIP Blocking |
| 中文标题 | Revelio：VoIP 封锁的全球性研究 |
| 作者 | Arjun Gupta（IIT Bombay）、Roya Ensafi（University of Michigan）、Piyush Kumar（IIT Delhi）、Devashish Gosain（IIT Bombay） |
| 年份 | 2026 |
| 会议/期刊 | USENIX Security 2026（第 35 届 USENIX Security Symposium，2026-08-12–14，Baltimore, MD, USA） |
| 研究方向 | 网络审查测量（censorship-circumvention）；VoIP/STUN 信令层封锁的远程大规模检测 |
| 任务类型 | 主动审查探测、STUN 中盒（middlebox）指纹与分类、应用专属流量特征提取 |
| 方法关键词 | Zstun（STUN-aware 扫描，基于 Zmap v4.3.4 改造）、差分探测 P1/P2/P3、9 类响应判定表（Cases I–IX）、StunTrace（TTL traceroute 定位中盒）、Hyperquack（HTTP/HTTPS 域级封锁检测）、残余审查（residual censorship）测量 |
| 数据集 | 无公开数据集（自采：71 国、11 个 VoIP 应用、2025-12 每日两次扫描；Hyperquack 7.56M 次可达性测量，2026-01-15–28） |
| 是否开源 | 是：代码与分析脚本已发布（Open Science 节 + 参考文献 [69]：Zenodo "Revelio — Global STUN Measurement Toolkit"，https://doi.org/10.5281/zenodo.20362017）；Hyperquack 数据集公开，STUN 服务器 IP 出于安全考虑未公开 |
| PDF | 00-inbox/PDFs/2026-USENIX-Revelio__A_Global_Study_of_VoIP_Blocking.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-USENIX-Revelio__A_Global_Study_of_VoIP_Blocking.md |

---

## 1. 一句话总结

> 用 STUN 感知扫描（Zstun）+ P1/P2/P3 差分探测远程判定 VoIP 封锁，在 71 国/11 个应用中定位 19 国的 4 类 6 型 STUN 中盒。

---

## 2. 摘要翻译

### 2.1 摘要原文

Online censorship has substantially increased over the past decade. While prior work on censorship detection has largely focused on the web, the landscape and mechanisms of VoIP censorship remain poorly understood. This work presents the first global study of VoIP blocking by introducing Revelio, a system that systematically detects and comprehensively analyzes VoIP censorship at scale. Unlike the only prior work, which is limited to two countries and requires authors to travel to conduct measurements, Revelio remotely uncovers VoIP blocking by carefully crafting probe packets and strategically leveraging IP address space within target countries, enabling detection of otherwise invisible VoIP censorship. Using Revelio, we studied 71 countries, covering 11 widely used VoIP applications. Our findings reveal evidence of VoIP blocking in 19 countries, primarily through targeted interference with the STUN traffic. By studying packet traces, we reverse-engineer censorship behavior and uncover four classes and six subtypes of middleboxes that trigger on unique application-specific STUN packets. We further analyze domain-level blocking at the HTTP and HTTPS layers, revealing cases where only VoIP calling is blocked while messaging remains accessible. Overall, our study advances the understanding of the privacy and censorship community by providing the first comprehensive, global view of an understudied yet highly prevalent form of censorship.

### 2.2 摘要中文翻译

过去十年在线审查显著增加，但既有审查检测工作大多聚焦 Web，VoIP 审查的图景与机制仍鲜为人知。本文提出 Revelio，首个 VoIP 封锁的全球性研究系统，可规模化地系统检测并全面分析 VoIP 审查。与唯一的前人工作（仅覆盖两国、且需要作者亲赴现场测量）不同，Revelio 通过精心构造探测包、并策略性地利用目标国家境内的 IP 地址空间，远程揭示 VoIP 封锁，从而发现原本不可见的 VoIP 审查。我们用 Revelio 研究了 71 个国家、覆盖 11 个广泛使用的 VoIP 应用，发现 19 个国家存在 VoIP 封锁证据，主要形式是针对 STUN 流量的定向干扰。通过分析数据包 trace，我们逆向出审查行为，发现 4 类、6 种子类型的中盒，它们由独特的应用专属 STUN 包触发。我们还分析了 HTTP/HTTPS 层的域级封锁，发现存在"只封锁 VoIP 通话、消息仍可访问"的案例。总体而言，本研究首次给出这一被忽视却高度普遍存在的审查形式的全局视图，推进了隐私与审查社区的理解。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 审查在全球持续上升（`§1`），且从传统 Web 内容封锁演化为更复杂的形态；VoIP 过滤（voice/video call）是被忽视的审查向量，只有零星报道与一项两国实证研究（Lipphardt et al., EuroS&P 2025，即本文参考文献 [41]）（`§1`）。
- VoIP 承载个人、职业与政治通信，但对其"流行程度、机制与影响"缺乏认识（`§1`）。
- 既有唯一实证研究依赖**境内 vantage point**：需要研究者物理旅行并在被审查地区操作测量设备，成本高、难以扩展，并给参与者带来人身与法律风险（`§1`）。

### 3.2 现有方法的痛点和不足

- VoIP 通信主要基于 UDP，难以可靠触发、观测与归因过滤行为；丢包与拥塞等网络artifact 使"有意干扰"与"良性损伤"难以区分（`§1`）。
- 通用全网扫描工具不适用：标准 Zmap 扫描在目标区域几乎发现不了可用的开放 STUN 服务器（`§1`，`§B`）。
- 前人工作 [41] 只覆盖两国、依赖人工 packet trace 分析，无法自动化识别丢包、ICMP 伪装、阈值触发过滤与限速等多种审查行为（`§6`，"Explicit Comparison with Lipphardt et al."）。
- 远程测量缺少境内 ground truth，需要额外的交叉验证机制（`§6`，"Ground Truth"）。

### 3.3 论文的研究假设或核心直觉

核心直觉：**应用专属的 STUN 信令包本身带可指纹属性（unknown attribute、Realm 域名字符串等），审查中盒正是基于这些属性做差异化处置**；因此只要先用 vanilla STUN（P1）与应用专属 STUN（P2）做差分，再用"混淆指纹"的同应用包（P3）做反证，就能在远程条件下把审查与普通网络故障区分开（`Abstract`, `§4.2`）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 审查从 Web 扩展到实时通信；已有两国实证显示系统性的 VoIP 干扰；UDP 层的干扰不易观测 | `§1` |
| 痛点提炼 | 既有研究需研究者入境部署，难以规模化，且无法区分"有意的差异化处置"与丢包/拥塞等自然现象 | `§1`, `§4.2` |
| 问题转化 | 如何远程、可扩展地"主动触发"VoIP 过滤并给出可验证的判定（而非依赖现场 ground truth） | `§4.2`（P1/P2/P3 判定逻辑） |
| 文献定位 | Web 审查测量已成熟（Censored Planet、Hyperquack 等），VoIP/STUN 层只有一篇两国的探索性工作 [41]，属"被忽视 + 方法不可扩展" | `§1`, `§2`, `§3` |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | VoIP 封锁可通过 STUN 协议的差分探测被远程、可扩展地识别；差异响应在 P3（混淆指纹）下消失即证明是审查而非网络故障 | `§4.2` 判定逻辑 | 71 国扫描 + 19 国复现（`§5.3.2`） |
| 辅助假设 | 改造 Zmap 使其解析 STUN 头与属性，可把可发现的 STUN 端点数量提升若干数量级 | `§4.1`, `§B` | Zstun 扫描结果（Figure 3） |
| 辅助假设 | 利用目标国"无响应 IP 空间"能显性化原本不可见的审查（如 ICMP 伪装注入） | `§4.1`, `§5.3.2` | 阿联酋 Case IX（Figure 7）约 1.5M IP 返回伪造 ICMP |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | 19/71 国检测到过滤；P3 混淆属性后响应恢复（如 WhatsApp：409 → 275 → 回升至接近 409）；多扫描间差异 0–12.35% | `§5.3.2`, Figure 5/6 |
| 远程判定可复现 | 支撑 | 从 Amsterdam 之外另用 Bangalore、Sydney、Singapore、San Francisco 验证 19 国，结果一致 | `§5.1` |
| 中盒可被定位与分类 | 支撑 | StunTrace 逆向出 4 类 6 型中盒；表 2 给出 19 国 × 中盒子类型 × 应用的对应关系 | `§5.3.3`, Table 2 |
| 残余审查（状态性） | 支撑 | 触发后按源 IP 封锁（与源端口/应用无关），时长聚类在 1–2 分钟的固定定时器 | `§6`, `§C` |

---

## 4. 方法设计

### 4.1 方法整体流程

Revelio 分两个核心组件（`§1`, `§4`）：**scanner 模块**（构造探测包、执行大规模扫描、在目标国境内寻找可测试端点，并利用无响应 IP 空间做受控触发）与 **detection 模块**（分析响应、按探针类型-响应配对判定审查，并用 StunTrace 定位/刻画中盒）。测量链路为：Zstun 全网扫描发现 STUN 服务器 → 对目标 IP 发 P1/P2/P3 三探针 → 按 9 类案例表判定 → StunTrace TTL 定位中盒 → 与 Hyperquack 域级封锁结果交叉比对。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 端点发现 | 目标国 IPv4 地址空间 | 用 Zstun（改造 Zmap v4.3.4，每个 IP 发 10 个探测包）扫描，解析 UDP 响应中的 STUN 头与属性 | 各国可响应的 STUN 服务器集合 | 获取可远程测试的 vantage point（`§4.1`, `§B`） |
| Step 2 差分探测 | STUN 端点 | P1 = vanilla STUN Allocate；P2 = 应用专属 STUN（携带该应用的指纹属性）；P3 = 混淆指纹后的同应用 STUN | 三类探针的响应矩阵 | 触发并确认差异化处置（`§4.2.2`） |
| Step 3 响应判定 | P1/P2/P3 响应 | 按 Table 1 的 9 类（Case I–IX）判定：绿=非异常、红=审查、黄=非异常但有潜在审查 | 每 IP 的审查标签 | 把"响应差异"转为"审查证据"（`§4.2.3`, Table 1） |
| Step 4 中盒刻画 | 过滤 IP 集合 | 用 StunTrace（TTL 递增的 STUN traceroute）观察路径中断/ICMP 来源，核对 P1/P2/P3 路径差异 | 中盒类型（M1–M4 及子型）与所属 AS | 逆向审查基础设施（`§4.3`, `§5.3.3`） |
| Step 5 域级交叉验证 | 300 个 IM 应用域名 | Hyperquack 对 HTTP（明文）与 HTTPS 发探测，计算 Probe Filtering Rate 与 AS Filtering Rate | 各国域级封锁画像 | 区分"仅封 VoIP 功能"与"整应用封锁"（`§5.4`） |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Zstun | Zmap v4.3.4 的 STUN 感知改造版：通过 `-probe-args=hex:` 指定 UDP payload，修改 `udp_process_packet` 与 `module_udp.c` 的 `fielddef_t fields[]` 以解析 STUN 头/属性 | 目标国 IPv4 空间 + P1/P2/P3 包 | 逐 IP 的 STUN 响应与属性 | 为 detection 模块提供响应矩阵（`§4.1`, `§B`） |
| 指纹生成器 | 从各 VoIP 应用的 Allocate/Binding 报文中提取稳定可指纹属性 | 应用抓包（5 次独立运行） | 各应用指纹特征表 | 决定 P2/P3 的构造（`§4.2.1`, Table 4） |
| detection 判定逻辑 | 按探针-响应配对给出审查/非审查/潜在审查 | P1/P2/P3 响应 | Case I–IX 标签 | 触发 StunTrace 复核（`§4.2.3`） |
| StunTrace | STUN 版 TTL traceroute，定位丢包跳点、判定 ICMP 是否被伪造成来自目的 IP | 过滤 IP + P1/P2/P3 | 中盒位置与类型 | 支撑 M1–M4 分类（`§4.3`, `§5.3.3`） |
| Hyperquack 比对 | HTTP/HTTPS 域级可达性测量与过滤率统计 | 300 个 IM 域名、71 国 | Probe/AS Filtering Rate | 与 STUN 层结论互补（`§5.4`） |

### 4.4 公式、算法和机制解释

- **触发机制**：Allocate 请求里的应用专属属性（如 WhatsApp 的 unknown attribute 0x4000/0x4024/0x4025/0x4002；Telegram 的 Realm `telegram.org` 与目的端口 1400；Signal 的 `turn.cloudflare.com`/`signal.org`）是中盒的匹配依据（`§4.2.1`, Table 4）。论文据 Table 4 说明主流 VoIP 应用"可被简单机制识别与封锁"（`§6`）。
- **判定机制（Table 1 的 9 类）**：按探针（P1–P3）与响应（R1 UDP 响应 / R2 ICMP / R3 无响应）的配对，判定哪些组合构成审查证据。实测中出现的审查相关案例为 IV、V、VII、VIII、IX；论文明确说明**未发现 STUN 投毒**，因此 Case VI 与 VIII 未实际发生（`§5.3.2`）。
- **利用无响应 IP 空间**：对 P1 无响应的 IP 发 P2，若收到 ICMP 错误（本不应有任何响应），即可推断是中间盒伪造目的 IP 注入 ICMP；P3 下该现象大幅回落（`§5.3.2`, Figure 7）。
- **TTL 与路由环**：部分目标 IP 对任意协议/端口、任意 TTL（最高测到 200）均返回 ICMP TTL-expired，作者据此判定这些目的地存在路由环路；StunTrace 证明丢包中盒位于环路由器之前（`§5.3.2`）。
- **状态性判定**：三个观察支持中盒有状态——(1) 仅改动指纹属性（其余头完全相同）不再触发；(2) 触发后对同一 tuple 持续丢弃（残余审查，包括 M4-B/M4-C）；(3) 先发 P1/P3 再发 P2 不被封锁，说明中盒把该 tuple 标记为"安全"（`§5.3.3`, `§C`）。

### 4.5 方法优势

- 全程远程、可规模化：不需要研究者入境或招募志愿者，显著降低人身与法律风险（`§1`, `§Ethical Considerations`）。
- 自带可证伪机制：P3 混淆探针提供了不依赖境内 ground truth 的内部验证（`§6`, "Ground Truth"）。
- 覆盖面广：71 国 × 11 应用，且结论在多测量点（5 地）复现（`§5.1`）。
- 覆盖多层：STUN 层与 HTTP/HTTPS 域层一起测，可区分"封功能"与"封应用"（`§5.4`）。

### 4.6 方法不足

- 无法检测所有类型的 STUN 过滤，例如只针对 egress 流量的审查；作者以沙特为例说明可能有漏检（`§6`, "Challenges in remote censorship detection"）。
- 过滤只影响部分路径：观测到的被丢弃探针比例较小，反映中盒部署的路径覆盖不全，而非过滤强度低（`§5.3.2`）。
- 残余审查 + 远程触发（源 IP 伪装）可能造成 DoS 风险，因此作者保守地不公开 STUN 服务器 IP（`Open Science`）。
- 数据释放策略受限：仅 Hyperquack 数据公开，STUN 端侧数据因风险未公开（`Open Science`）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

与唯一直接前人工作 Lipphardt et al. [41] 相比：后者依赖人工 packet trace 分析、在少数境内 vantage point 上比较"被审查地区 vs 非审查地区"的应用行为；Revelio 则是主动远程测量框架，贡献 STUN 感知全网扫描、差分探针-响应分析与 STUN traceroute，能够识别丢包、ICMP 伪装、阈值触发过滤与限速等更广谱的审查行为，并首次利用无响应 IP 空间推断 ICMP 异常（`§6`, "Explicit Comparison with Lipphardt et al."）。与 Web 审查测量生态（Hyperquack、Censored Planet 类）的关系是互补：Revelio 复用 Hyperquack 做域级对照，但主战场是 UDP/STUN 信令层（`§5.4`）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| Zstun | 将 Zmap 改造为可构造 STUN 探针并解析 STUN 响应的扫描器，可靠发现远多于通用扫描的 STUN 端点 | 高 | 是（其他 UDP 协议扫描的模板） |
| P1/P2/P3 差分判定 | 以"混淆指纹后行为回归"作为审查的内部确证，替代境内 ground truth | 高 | 是（任何基于协议指纹的封锁测量） |
| 无响应 IP 空间利用 | 把本应无响应的地址空间变为审查显影剂，暴露伪造 ICMP 注入 | 高 | 中（依赖具体中盒行为） |
| 中盒分类学（4 类 6 型） | 首次给出 STUN 专用中盒的分类：M1（首次遇到即丢，A 暴露 IP/B 伪装源 IP/C 不暴露）、M2（多次遇到后才丢，阈值触发）、M3（伪造 ICMP 目的不可达）、M4（限速：A 随机丢/B 周期丢/C 等差丢） | 高 | 是（审查基础设施刻画方法论） |
| 残余审查的 UDP 侧测量 | 说明无连接状态下仍存在按源 IP 的持续性封锁（1–2 分钟量级） | 中 | 是 |

### 5.3 适用场景

适合"UDP 信令层审查"的远程大规模测量：VoIP/实时通信封锁、基于协议字段（而非内容）的中盒过滤、需要在不入境条件下获得多国可比证据的审查研究。也适用于评估"封锁是功能级还是应用级"（需配合域级 HTTP/HTTPS 测量）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 境内 vantage point 测量（[41] Lipphardt et al.） | 具备真实 ground truth；可观测端侧完整行为 | 需入境/旅行，成本高、难扩展；对研究者有风险；仅两国 | 全远程、可扩展；用 P3 反证替代现场 ground truth |
| 通用全网扫描（原生 Zmap） | 成熟、快、生态完善 | 无法构造/解析 STUN 语义，目标区域几乎发现不到可用 STUN 服务器 | Zstun 增加 STUN 探针构造与响应解析 |
| Web 域级审查测量（Hyperquack / Censored Planet 类） | 覆盖广、长期可比 | 只覆盖 HTTP/HTTPS 域可达性，看不到 UDP 信令层封锁 | 与 STUN 层结果互补，可区分"封通话"与"封应用" |
| 被动流量分析 | 不干扰网络 | 无法主动触发差异化处置，难以归因 | 主动差分探测 + 中盒定位 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- 测量机位于 Amsterdam（8GB RAM、Ubuntu 22.04、300 Mbps 带宽），另在 Bangalore、Sydney、Singapore、San Francisco 复测 19 个已判定被过滤的国家（`§5.1`）。
- 时间跨度 5 个月（2025-08 – 2025-12），前 4 个月为 pilot（扩展 Zmap、P3 探针、StunTrace、伪造 ICMP 检测），正式测量为 2025-12-01 – 12-30，每日两次扫描；**论文所有结果基于这 1 个月数据**（`§5.1`）。
- Hyperquack 测量于 2026-01-15 – 01-28，每周两次，共 300 个 IM 域名（`§5.4`）。
- 国家集：Freedom on the Net 的 Not Free(21) + Partly Free(28) + 11 个未入榜但可能审查的国家 + 11 个自由国家作对照，共 71 国（`§5.2`）。
- 应用集：从 31 个候选应用中筛出 19 个可发起通话的应用，其中 11 个（WhatsApp、Telegram、Viber、Signal、Messenger、Instagram、Slack、Dialpad、Webex、Jitsi、Wire）可提取出指纹化 STUN 包（`§5.2`, Table 4）。

### 6.2 数据集

无公开数据集；数据为自采测量结果。附录 Table 4 给出 11 个应用的 STUN/TURN 指纹属性清单（Allocate/Binding/Create Permission/Channel Bind/Refresh 等报文类型 + unknown attribute、Realm、目的端口、Lifetime、Software 字段等）（`Table 4`）。

### 6.3 Baseline

没有 ML 意义上的 baseline；对照设计有三类：(1) 11 个"自由国家"对照国，用于排除丢包/路由异常导致的假阳性（`§5.2`）；(2) P1/P3 vs P2 的自身对照（同 IP、同协议、仅指纹属性不同）；(3) 与前人 [41] 的定性对比（`§6`）。

### 6.4 评价指标

- 是否出现差异响应（STUN UDP 响应 / ICMP 错误 / 无响应）以及经 P3 后是否回归（`§4.2.3`）。
- Hyperquack 侧：Probe Filtering Rate（探针被过滤比例）与 AS Filtering Rate（涉及过滤的 AS 占比）（`§5.4`）。
- 稳定性指标：STUN 服务器 churn（重复扫描间新增/移除比例，多数国家 <5%，阿塞拜疆/科威特/卡塔尔/吉尔吉斯斯坦/约旦部分扫描 >10%）（`§5.3.1`）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---|---|---|---|
| 全球 VoIP 封锁检测 | 发现封锁的国家数 | 19 / 71 国 | 前人 [41]：2 国 | 9.5× 国家覆盖 | 主要针对 STUN 流量，涉 5 个应用（WhatsApp、Telegram、Messenger、Signal、Instagram）`§5.3.2` |
| Zstun 端点发现 | 可发现 STUN 服务器 | 71 国均发现（印尼约 1,200 台最多；缅甸 15、阿塞拜疆 24 最少） | 原生 Zmap：目标区域几乎为 0 | 数量级提升 | `§5.3.1`, Figure 3 |
| 阿联酋 WhatsApp（Case IV） | 响应 IP 数（10 包/IP） | P1: 409 → P2: 275 → P3: 回升近 409 | — | — | 明确的应用专属属性过滤 `§5.3.2`, Figure 5 |
| 阿联酋（Case IX） | 伪造 ICMP 的 IP 数 | P2: 约 1.5M 个 IP 返回 ICMP；P3: 仅数千；99.83% 对 P3 无响应 | — | — | 仅阿联酋观测到该形态 `§5.3.2`, Figure 7 |
| 缅甸（Case VII） | ICMP 响应 IP 数 | P1: 4,593 IP 返回 ICMP；P2 对 Messenger 超 90% 无响应 | — | — | 缅甸、约旦、阿塞拜疆、阿联酋均有 `§5.3.2`, Figure 8 |
| 阿联酋（Case II） | TTL-expired / dest-unreachable IP 数 | P1: 15,325 TTL-expired → P2: 7,744 dest-unreachable → P3: 14,286 恢复 TTL-expired | — | — | 配合 StunTrace 确认路由环 + 前置丢包中盒 `§5.3.2`, Figure 9 |
| 阿联酋 ICMP dest-unreachable | 响应 IP 数 | P1: 23,585 → P2: 90,252（3.83×） → P3: 20,640 | — | 3.83× | P2 的 ICMP 由中盒伪造源 IP 注入，P1/P3 的来自端主机 `§5.3.2`, Figure 10 |
| AS 级分布 | 被过滤 AS 占比 | 缅甸 39.68%、阿塞拜疆 36.67%、阿联酋 36.23% 最高；墨西哥 0.84% 最低 | — | — | `§5.3.3`, Table 3 |
| 域级封锁（HTTP） | Probe Filtering Rate | 阿曼对 Viber 100%（AS 过滤率亦 100%）；巴基斯坦对 Telegram 约 97.3% | — | — | `§5.4`, Figure 12a |
| 域级封锁（HTTPS） | Probe Filtering Rate | 土库曼斯坦 100%；中国对 5 个 VoIP 应用与 Wire；俄罗斯对 Telegram/Signal 重度过滤 | — | — | `§5.4`, Figure 12b |
| 探针过滤率 vs AS 过滤率 | Pearson 相关系数 | 0.96 | — | — | 高过滤率几乎总伴随跨 AS 的广域部署 `§5.4` |

### 6.6 优势最明显的场景

- 目标应用使用固定 STUN 属性/域名字符串作为指纹时（Telegram 的 Realm、WhatsApp 的 unknown attribute），检测效果最清晰，且 P3 能干净地证明是审查（多处 P3 后响应恢复到 P1 水平）。
- 需要区分"仅封 VoIP 通话"与"封整个应用"的场景：巴基斯坦（Signal）与缅甸（Telegram）在域级与 STUN 级都封；哈萨克斯坦与卡塔尔只封 HTTPS 域 + STUN；爱沙尼亚与科威特只封 STUN；中国与俄罗斯只做域级封锁而无 STUN 过滤（`§5.4`）。
- 需要刻画审查基础设施的场景：4 类 6 型中盒分类与 AS 归属（Table 2、Table 3）。

### 6.7 局限性

- 无法检测所有 STUN 过滤形态（如只针对 egress），沙特疑似封 WhatsApp 通话但未能检出（`§6`）。
- 远程测量无 ground truth，依赖 P3 反证与 [41] 的境内观测作为外部支撑（`§6`）。
- 过滤可观测比例偏低（部分路径不经过中盒），单看比例会低估审查强度（`§5.3.2`）。
- Binding 报文方面大多未发现过滤，仅 Messenger/Instagram 在阿联酋与缅甸因 unknown attribute `0xdaba` 与 Username `EDGE:EDGE` 被丢（`§6`, `§A`）。

---

## 7. 学习与应用

### 7.1 是否开源？

是。代码与分析脚本按模块发布：`scraping/launcher.sh`（抓取国家 ASN 与前缀）、`protocol_probing/launcher.sh`（Zmap 辅助的 STUN 协议探测）、以及 Zmap 输出的后处理（`Open Science`）。地址见参考文献 [69]：https://doi.org/10.5281/zenodo.20362017 。Hyperquack 测量数据公开；STUN 服务器 IP 出于残余审查 + 源 IP 伪装可造成 DoS 的考虑未公开（`Open Science`）。

### 7.2 复现关键步骤

1. 按国家抓取 ASN 与前缀数据，清洗后生成扫描目标（`scraping/launcher.sh`）。
2. 用 Zstun 扫描，构造 P1（vanilla STUN Allocate）、P2（应用专属 STUN）、P3（混淆指纹），每 IP 发 10 个探针以提高抗丢包能力（`§4.2.2`, `§5.3.2`）。
3. 解析 UDP 响应中的 STUN 头与属性，生成每 IP 的探针-响应矩阵（`§B`）。
4. 按 Table 1 的 Case I–IX 判定审查，取"P1/P2 响应不同、P1/P3 响应相同"的 IP 交集作为 filtered IP 集（`§4.2.3`, `§5.3.2`）。
5. 对 filtered IP 用 StunTrace 做 TTL 递增探测，定位丢包跳点、判定 ICMP 是否伪造，归入 M1–M4 子型（`§4.3`, `§5.3.3`）。
6. 用 Hyperquack 对 IM 域名做 HTTP/HTTPS 探测，计算两个 filtering rate 并做相关性分析（`§5.4`）。

### 7.3 关键超参数、预处理和训练细节

- 每 IP 探测包数 10；判定"稳定 STUN 服务器"的阈值为响应 ≥ 8（`§5.3.2`）。
- 扫描在 300 Mbps 链路上保证一天内完成一轮；每日两次（`§5.1`）。
- 重复扫描的差异容忍：UDP 类 0–12.35%，无响应类 0–10.53%（`§5.3.2`）。
- StunTrace 探测 TTL 最高测到 200 以验证路由环（`§5.3.2`）。
- 残余审查实验发送 200 个包以观测 M4-C 的等差丢包模式（首次丢包在第 1 个，随后第 11/22/34 个，34 之后回绕为 44/55/67）（`§5.3.3`）。
- 无训练过程（非 ML 方法）。

### 7.4 能否迁移到其他任务？

- **协议层差分探测范式**可以迁移到任何"客户端信令带可指纹字段"的协议（如 QUIC/DTLS 握手字段、游戏/直播协议的私有握手），核心是构造"指纹化 vs 混淆化"两版探针做反证。
- **Zstun 式扫描器改造**思路可迁移到其他 UDP 协议的全网测量（在 Zmap probe module 中加解析逻辑而非只判"有/无 UDP 响应"）。
- **无响应 IP 空间利用**可迁移为通用异常显影手段：对"本应无响应"的目标发探针，任何响应都是异常信号（需要谨慎评估对第三方网络的影响与伦理）。
- **残余审查按源 IP 计时**的测量方法可迁移到 TCP 之外的无连接协议的审查持续性研究。

### 7.5 对我的研究有什么启发？

- 该文展示了"差分 + 反证"这一低成本但强力的实验设计：判定结论不是来自单次观测，而是来自"改变一个变量后行为是否回归"，这与 ML 分类器的混淆变量控制思路一致，可借鉴到流量分类的可解释性验证。
- 论文对 ground truth 缺失的坦诚处理（远程测量 vs 境内的 trade-off、依赖 P3 内部验证）是优秀的测量方法论示范。
- Table 4 的应用指纹清单本身可作为一个"应用身份特征"数据集，与 app-fingerprinting 任务相关。
- 中盒分类学（触发时机 × 处置动作）提供了一个把"黑盒行为"结构化的模板：维度拆解为"何时触发（首次/多次）"与"如何处置（丢包/伪造 ICMP/限速）"。

---

## 8. 总结

### 8.1 核心思想

> 差分探针 + 混淆反证，远程显影 VoIP 审查中盒。

### 8.2 速记版 Pipeline

1. 用 Zstun 扫描目标国 IPv4 空间，解析 STUN 响应，建立可测端点集。
2. 对端点发 P1（vanilla STUN）/ P2（应用专属 STUN）/ P3（混淆指纹）三探针。
3. 按 Case I–IX 判定差异化处置，取 P1-P2 不同且 P1-P3 相同的 IP 作为 filtered IP。
4. 用 StunTrace 定位中盒并分类为 M1–M4（含 A/B/C 子型），统计 AS 级分布。
5. 用 Hyperquack 做 HTTP/HTTPS 域级对照，区分"封 VoIP 功能"与"封整个应用"。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[censorship-circumvention]] —— 本文属审查测量/反审查研究谱系：远程检测 19 国的 VoIP（STUN）封锁并逆向其中盒基础设施。
- 说明：本文不涉及加密流量的内容分析（STUN 明文可解析），因此不链接 encrypted-traffic-analysis 概念页。

### 9.2 相关方法

- 暂无白名单内的匹配方法页。本文使用主动探测（active probing）、协议指纹差分与 TTL traceroute，而非 [[transformer]]/[[convolutional-network]] 等 ML 方法，故留空。

### 9.3 相关任务

- [[app-fingerprinting]] —— 机制层面的应用指纹：论文从 11 个 VoIP 应用的 STUN/TURN 报文中提取稳定、应用专属的可指纹属性（Table 4），并据此触发/绕过中盒；注意这属于"协议字段指纹"，非 ML 流量分类意义上的 app fingerprinting。

### 9.4 可更新的综述页面

- 暂无白名单内匹配的综述页（现有 5 个综述页均面向 ML 流量分析主题，本文为测量类工作）。

### 9.5 可加入的对比表

- [[open-source-registry]] —— 本文开源了 Revelio 的扫描与探测代码（Zenodo，ref [69]），可登记为审查测量工具。

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 19/71 国存在 VoIP 过滤，涉及 5 个应用 | 全球扫描结果与 Table 2 国别-中盒-应用对应表 | `§5.3.2`, `§5.3.3`, Table 2 |
| P3 混淆指纹后响应恢复，证明是审查而非网络故障 | WhatsApp 409 → 275 → 回升；沙特 Telegram 245 → 228 → 245 | `§5.3.2`, Figure 5/6 |
| 中盒会伪造目的 IP 注入 ICMP 不可达 | 阿联酋 P2 收到约 1.5M IP 的伪造 ICMP，P3 仅数千，99.83% 无响应 | `§5.3.2`, Figure 7 |
| 中盒具状态性且残余审查按源 IP 生效 | 触发后同 tuple 持续被封、时长聚类在 1–2 分钟；先发 P1/P3 不被封 | `§6`, `§C` |
| 中盒可分类为 4 类 6 型（M1–M4，含子型） | StunTrace 逆向结果与分类描述 | `§5.3.3`, Figure 11 |
| 域级封锁与 STUN 层封锁可解耦 | 巴基斯坦/缅甸双封；哈萨克斯坦/卡塔尔仅域级+STUN；中国/俄罗斯仅域级 | `§5.4`, Figure 12 |
| 应用专属 STUN 指纹易被利用 | 11 个应用的指纹属性表（Realm、unknown attribute、端口、Lifetime、Software） | `§4.2.1`, `§6`, Table 4 |
| Zstun 相对原生 Zmap 的必要性 | 原生 Zmap 在目标区域几乎发现不到可用 STUN 服务器 | `§1`, `§4.1`, `§B` |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-USENIX-Revelio__A_Global_Study_of_VoIP_Blocking.pdf
- MinerU Markdown：02-parsed-markdown/2026-USENIX-Revelio__A_Global_Study_of_VoIP_Blocking.md

---

## 12. 后续问题

- 论文未提供 VoIP 应用的加密/指纹抵抗设计的具体建议，仅指出"协议须为抗审查而设计"——VoIP 应用的抗指纹化改造空间有多大？
- Zstun 的响应解析是否可复用到其他 UDP 协议（如 QUIC initial、游戏协议）的审查测量？改造工作量如何？
- 本方法对"仅针对 egress 的审查"失效，是否有不依赖境内 vantage point 的替代方案？
- 中盒 M4-C 的等差丢包（1/11/22/34…回绕）暗示了什么样的实现（计数器 + 定时器重置）？能否作为中盒实现指纹用于同源判定？
- 与 KB 内审查测量论文（Censored Planet、Shadowsocks）相比，STUN 层审查测量的数据共享困境（IP 敏感）如何在不危及用户的前提下缓解？

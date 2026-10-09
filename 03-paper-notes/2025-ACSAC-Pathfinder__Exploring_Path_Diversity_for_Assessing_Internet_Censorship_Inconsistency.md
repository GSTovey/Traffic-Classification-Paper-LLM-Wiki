---
type: paper
title_original: "Pathfinder: Exploring Path Diversity for Assessing Internet Censorship Inconsistency"
title_cn: "Pathfinder：探索路径多样性以评估互联网审查的不一致性"
authors: [Xiaoqin Liang, Guannan Liu, Lin Jin, Shuai Hao, Haining Wang]
year: 2025
venue: "ACSAC 2025"
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2025-ACSAC-Pathfinder__Exploring_Path_Diversity_for_Assessing_Internet_Censorship_Inconsistency.pdf"
mineru_md: "02-parsed-markdown/2025-ACSAC-Pathfinder__Exploring_Path_Diversity_for_Assessing_Internet_Censorship_Inconsistency.md"
status: processed
reading_level: L2
research_area: [censorship-circumvention]
task: [censorship-measurement]
method: [active-measurement, application-traceroute, resip-vantage-points]
dataset: [Proxyrack-RESIP, Disguiser-domain-list, AWS-GCP-Azure-control-servers]
code: unknown
relevance: high
created: "2026-09-19"
updated: "2026-09-19"
---

# Pathfinder: Exploring Path Diversity for Assessing Internet Censorship Inconsistency

> ⚠️ MinerU 解析问题：fi/ff/fl 连字被系统性替换为符号（`di!erent`→different、`tra#c`→traffic、`con"gurations`→configurations、`speci"c`→specific、`NetShu%e`→NetShuffle、`o#cial`→official、`\$awed`→flawed、`in\$uence`→influence、`Path!nder`/`Path"nder`→Pathfinder），引用时已还原；Table 2/Table 5/Table 6 表头合并单元格解析混乱（ASN 与方向列错位、单元格内多 IP 连写），数值仍可逐项核对。另有三处**原稿内部不一致**需注意：① §5.1 正文称 23 个国家出现 100% 审查不一致，附录 A Table 4 的 100% 区间仅列 19 国，且 90–99% 区间正文写 20 国、表格写 18 国（同阈值口径冲突）；② §5.2 正文「超过 50% 的国家 destination inconsistency 大于 75%，而 20% 的国家大于 30%」两句自相矛盾，疑为丢失小数点（应为 7.5%），本文引用时按「多数国家存在两位数百分比级差异」谨慎表述；③ §6.3 正文写审查设备涉及 AS 8057 (Microsoft Azure)，Table 6 中对应行为 AS 8075（Microsoft Corp.），本文按 AS 8075 引用。

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Pathfinder: Exploring Path Diversity for Assessing Internet Censorship Inconsistency |
| 中文标题 | Pathfinder：探索路径多样性以评估互联网审查的不一致性 |
| 作者 | Xiaoqin Liang（Old Dominion University）, Guannan Liu（Colorado School of Mines）, Lin Jin（University of Delaware）, Shuai Hao（Old Dominion University）, Haining Wang（Virginia Tech） |
| 年份 | 2025 |
| 会议/期刊 | ACSAC 2025（解析稿未给出 DOI） |
| 研究方向 | censorship-circumvention（互联网审查测量：国家内部路径多样性与审查不一致） |
| 任务类型 | 大规模主动测量（审查不一致的量化、归因与规避潜力评估），非机器学习任务 |
| 方法关键词 | 住宅 IP 代理（RESIP）vantage points；多地 back-end 控制服务器制造路径多样性；静态 payload ground truth（源自 Disguiser 思路）；应用层 traceroute；缓存代理剔除与 inbound censor 排除 |
| 数据集 | 自采测量数据：实验 1（IP 目的地方向）144,418 个 VP / 120 国 / 60 周；实验 2（托管平台方向）66,123 个 VP / 120 国 / 36 周；测试域名列表来自 Disguiser 汇编的国别被审域名清单 |
| 是否开源 | 未提及（代码与数据发布方式解析稿未给出；测试域名列表指向 Disguiser 的公开仓库 github.com/e2ecensor/Disguiser_public） |
| DOI | unknown |
| 备注 | 伦理设计：RESIP 经 ToS 确认、每个住宅 IP 每周仅使用一次、探测不触达真实被审内容、获机构 IRB 豁免；附录 A/B 给出国别不一致分档表与完整 traceroute 结果 |

---

## 1. 一句话总结

> 把探测流量指向不同地理/云平台的服务器即可让同一国内外发流量走不同 transit 网络，Pathfinder 由此测得 91.7% 的国家存在审查不一致，且低审查路径可被用于规避。

---

## 2. 摘要翻译

### 2.1 摘要原文

Internet censorship is typically enforced by authorities to achieve information control for a certain group of Internet users. So far existing censorship studies have primarily focused on country-level characterization because (1) in many cases, censorship is enabled by governments with nationwide policies and (2) it is usually hard to control how the probing packets are routed to trigger censorship in different networks inside a country. However, the deployment and implementation of censorship could be highly diverse at the ISP level. In this paper, we investigate Internet censorship from a different perspective by scrutinizing the diverse censorship deployment inside a country. Specifically, by leveraging an end-to-end measurement framework, we deploy multiple geo-distributed back-end control servers to explore various paths from one single vantage point. The generated traffic with the same domain but different control servers' IPs could be forced to traverse different transit networks, thereby being examined by different censorship devices if present. Through our large-scale experiments and in-depth investigation, we reveal that the diversity of Internet censorship caused by different routing paths inside a country is prevalent, implying that (1) the implementations of centralized censorship are commonly incomplete or flawed and (2) decentralized censorship is also common. Moreover, we identify that different hosting platforms also result in inconsistent censorship activities due to different peering relationships with the ISPs in a country. Finally, we present extensive case studies in detail to illustrate the configurations that lead to censorship inconsistency and explore the causes.

### 2.2 摘要中文翻译

互联网审查通常由当局实施，以对特定用户群体实现信息控制。既有审查研究主要停留在国家层面的刻画，原因有二：（1）多数情况下审查由政府的全国性政策驱动；（2）探测包在国内不同网络中的路由难以控制，难以触发并观察不同网络中的审查。然而，审查的部署与实现方式在 ISP 层面可能高度多样。本文从不同角度审视一国**内部**的审查部署多样性：我们借助一套端到端测量框架，部署多个地理分布的后端控制服务器，从单个 vantage point 出发探索多条路径。相同域名、但目的 IP 指向不同控制服务器的流量会被迫经过不同 transit 网络，从而（若存在）被不同审查设备检查。通过大规模实验与深入调查，我们发现由国内不同路由路径造成的审查多样性普遍存在，这意味着（1）集中式审查的实现往往不完整或有缺陷，（2）去中心化审查同样常见。此外，我们发现不同托管平台因其与国内 ISP 不同的 peering 关系，也会导致审查行为不一致。最后，我们用详尽的案例研究展示导致审查不一致的具体配置并探究其成因。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

既有审查测量几乎都在国家层面聚合结论（[29, 30, 40, 43, 44, 48, 50, 55]），默认全国政策一致。但审查的实际部署与实现在 ISP 层面差异很大，国家层面的刻画过粗，无法支撑对审查部署的可靠结论。受测量手段限制：研究者无法控制探测包会经过哪些 transit 网络或网关，因而无法把国内不一致的审查行为归因于「部署多样性」。作者要回答的是：**一国内部不同网络路径上的审查行为到底有多不一致？**

### 3.2 现有方法的痛点和不足

- **国家聚合抹平 ISP 级差异**：分布式 VP 的探测包往往收敛到少数上游 transit 网络（如论文 Figure 1 中的 AS 1），即使另一条路径（AS 2）实施了不同策略也无法被观察到。
- **traceroute / 应用层 traceroute 覆盖有限**：只能沿单一路径逐跳检查，难以在大规模上系统识别不一致。
- **BGP churn 归因法（Cho et al. [14]）**：完全依赖 ICLab [40] 的 VPN 数据，覆盖有限且路径变化随机、不可控；只能捕捉网络级路径变化的有限场景。
- **BreadCrumb [9]**：仅针对 DNS 审查，且只利用路由器负载均衡造成的网络内小尺度路由变化。

### 3.3 论文的研究假设或核心直觉

核心直觉：**审查策略部署在 ISP/transit 网络层面，而流量走哪条路径取决于目的地。** 只要控制探测包的目的地（不同地理位置、不同云平台的服务器 IP），同一 vantage point 的流量就会被迫经过不同 transit 网络，进而（若存在审查设备）被检查或放行——由此把「不可控的路由」变成「可控的实验变量」，实现国内路径维度上的审查不一致测量。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 既有研究报告过个别国家的去中心化信息控制 [22, 51, 62]，且大面积测量显示审查在国家级分布呈 all-or-nothing | §1, §5.1 |
| 痛点提炼 | 分布式探测的目的地相同 → 上游收敛 → 国内 ISP 级审查差异被系统性低估，无法归因 | §3.1, Figure 1 |
| 问题转化 | 将「审查是否不一致」转化为可测量的科学问题：控制目的地制造路径多样性，度量同一国家不同路径上的审查差异 | §3.2, §4 |
| 文献定位 | 处于被忽视位置：BGP churn 归因 [14] 覆盖有限、BreadCrumb [9] 限 DNS、Disguiser [30] 只做真值检测不测不一致 | §1, §8.1 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 H1 | 一国内部由不同路由路径造成的审查不一致是普遍现象（集中式审查实现不完整/有缺陷，或存在去中心化审查） | §1, §3.1 | 60 周全球测量（144K VP / 120 国），VP 级与域级不一致统计 |
| 辅助假设 H2 | 目的地的**地理位置**是造成不一致的主因之一 | §5.2 | 6 台地理分布的 AWS 控制服务器对照 |
| 辅助假设 H3 | 目的地的**托管平台**（云商 peering 关系）同样造成审查不一致，且可被规避利用 | §5.3, §6 | 3 云 × 4 地 12 台控制服务器对照 + 应用层 traceroute 案例 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| H1 | 支撑 | 91.7%（110/120）国家存在不同程度不一致；仅 11（10%）国家不一致率低于 9%；中国、巴基斯坦、科威特审查率与不一致率双双 >92% | §5.1, Figure 6, Table 1 |
| H2 | 支撑 | 目的地不一致在多数国家为两位数百分比级；印度指向 Bahrain 的路径仅 8.4% 被审查，其余路径 37–60%；AS 级最大不一致达 81%（AS 204457, Turkey） | §5.2, Figure 8/9, Table 2 |
| H3 | 支撑 | 韩国 AWS 98.93% vs GCP 32.21%；印度 AWS 50.89% vs GCP 18.57%；案例显示本地 ISP 与 GCP 私有网络直连使流量在到达审查设备前进入云内网络 | §5.3, Table 3, §6.2/§6.3 |

---

## 4. 方法设计

### 4.1 方法整体流程

Pathfinder = 「全球分布式 vantage points」+「多地 back-end 控制服务器（探测目的地）」+「客户端/服务端双侧结果收集」。VP 从 RESIP 服务商 Proxyrack 获取；探测请求的 HTTP Host 头填入该国已确认被审查的域名（取自 Disguiser [30] 汇编的国别清单），目的 IP 设为某台控制服务器的 IP；控制服务器对所有请求返回**静态 payload**（与任何合法页面或封锁页不冲突）作为真值，据此判定请求是否被审查（超时 / 连接被拆 / 收到非静态载荷响应）。同一 VP 对不同控制服务器的请求被强制走不同路径，从而把「路径」变为可控变量，再聚合出 VP 级与域级不一致率。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 获取 VP | Proxyrack RESIP 服务 | 订阅住宅 IP 代理作为 vantage points；每 IP 每周只用一次；每国每周上限 80 个 VP | 全球分布式探测点池 | 逼近真实住宅用户的网络位置与审查暴露 |
| Step 2 VP 预筛 | 每批新 VP | 实时缓存代理检测（两个同域不同目的/载荷的参考服务器，顺序探测）；离线用合法页面 title 标签比对，剔除疑似中间缓存 | 干净 VP 集合（共剔除 164 个） | 避免缓存响应被误判为审查/未审查 |
| Step 3 部署控制服务器 | 云主机 | 实验 1：6 台 AWS（Virginia、California、São Paulo、London、Bahrain、Cape Town）；实验 2：AWS/GCP/Azure ×（Virginia、Sydney、Paris、São Paulo）共 12 台 | 多目的地探测端点 | 制造地理与托管平台两个维度的路径多样性 |
| Step 4 排查 inbound 审查 | 50 台 hide-my-ip VPN | 从多国 VPN 向全部控制服务器发送带测试域名的探测包，确认均能取回静态 payload | inbound 审查已排除的控制服务器 | 避免目的国方向的 inbound 审查污染结果 |
| Step 5 探测与判定 | VP + Host=被审域名 + 目的=控制服务器 IP | HTTP 请求，5 秒超时，超时自动重试 4 次后判为被阻断；收集客户端与服务端双侧响应/连接状态 | 逐请求审查标签 | 以静态载荷为真值，无需人工核验封锁页 |
| Step 6 聚合与案例 | 审查标签 | 按国家/域/AS 聚合 censorship %、inconsistency %、destination/hosting inconsistency；对韩国、印度做 VPN + 应用层 traceroute（每国随机 32 个被审域名 × 12 台控制服务器） | 不一致率统计 + 逐跳审查设备定位 | 量化普遍性并归因到具体 peering 配置 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Vantage Points（RESIP） | 产生出发点流量，模拟住宅用户 | Proxyrack 分配 | HTTP 探测请求 | 向控制服务器发起请求；被预筛模块过滤 |
| Identified Censored Domain List | 提供每国已确认被审域名，避免全量扫描 | Disguiser [30] 汇编（Alexa top 1000 + Citizen Lab） | 国别测试域名清单 | 填充 HTTP Host 头 |
| HTTP Requests | 构造并调度探测（Host 头触发审查，目的 IP 选路） | 域名清单 + 控制服务器 IP | 带真值预期的请求 | 连接 VP 侧与控制服务器侧 |
| Control Server（静态 payload） | 提供不可混淆的响应真值；不同地理位置/云商即不同路径入口 | 收到的 HTTP 请求 | 静态载荷响应 | 决定路径多样性；结果与客户端侧比对 |
| Cache/Inbound 排除 | 剔除中间缓存与目的端 inbound 审查造成的假象 | 参考服务器探测、VPN 探测 | 干净的测量边界 | 在聚合前过滤噪声 |
| Application Traceroute | 逐跳定位审查设备（RESIP 无法改 TTL，改用商用 VPN） | VPN + 增量 TTL 请求 | 路径与审查跳点 | 案例研究模块，解释 §5.3 的宏观结果 |

### 4.4 公式、算法和机制解释

- **VP 级审查率**：censored VPs / evaluated VPs；VP 只要任一请求被审查即计为 censored。
- **VP 级不一致率（inconsistency %）**：在被审查的 VP 中，观察到「不同网络路径间审查行为不一致」的 VP 占比——衡量不一致行为的普遍性。
- **域级审查率**：某国针对某域名的被阻断请求数 / 该域名总请求数；用于域间比较（如泰国 livejasmin 1% vs bongacams 96%）。
- **destination inconsistency**：同一国家内，指向不同控制服务器（不同地理位置）的路径间审查百分比的差值。
- **hosting inconsistency**：同一国家内，指向不同云平台（AWS/GCP/Azure）的路径间审查百分比差值。
- **AS 级不一致**：同一 AS 的探测包指向各控制服务器时，最大与最小审查百分比之差（Table 2 用 81.0% 为最大）。

### 4.5 方法优势

- **路径可控**：不依赖 BGP churn 等随机事件，通过选目的地主动制造路径多样性，可大规模并行。
- **真值判定**：控制服务器静态载荷与合法页面/封锁页均不冲突，判定无需人工核验封锁页。
- **噪声控制完整**：同时处理缓存代理（164 个 VP 被剔除）与目的方 inbound 审查（50 台 VPN 验证）。
- **伦理设计**：探测不触达真实被审内容、每住宅 IP 每周仅用一次、与 Proxyrack ToS 确认并获 IRB 豁免。

### 4.6 方法不足（作者自述 + 范围限制）

- **近 VP 审查漏检**：若审查设备部署在离客户端很近的跳点，同一 VP 的所有路径都会一致地被审，Pathfinder 观察不到（§7）。
- **VP 分布偏斜**：部分国家（瑞士、苏丹、赞比亚）VP 不足 200 个；RESIP 与 VPN 的网络位置偏差（VPN 多在商业数据中心，审查暴露低于住宅网络）。
- **测试域列表继承自 Disguiser**：该列表未考虑不一致性影响，可能漏掉「仅在部分路径被审」的域名。
- **仅覆盖 HTTP**：DNS 与 HTTPS/SNI 审查留作 future work；应用层 traceroute 无法用 RESIP 完成（RESIP 工作在传输层之上，不能改 TTL）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

主流测量（OONI、ICLab、Censored Planet、Quack）以「多点探测 + 国家聚合」刻画审查，探测目的地单一，路径不可控；BGP churn 归因 [14] 依赖随机路由事件且受限于 ICLab 数据；BreadCrumb [9] 依赖路由器负载均衡造成的网络内小尺度变化且仅限 DNS；Disguiser [30] 用静态载荷做精确真值检测但不研究路径维度。Pathfinder 的区别是把「目的地」当作自变量：同一 VP、同一域名，仅改变目的 IP，即可对比不同 transit 网络的审查策略，从「国家聚合」推进到「国内路径分解」。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 路径多样性测量框架 | 多地理/多云控制服务器同时探测，单 VP 即可观察多条路径的审查差异 | 高 | 是（任何中间盒策略测量均可借用「控目的地、造路径」设计） |
| 全球不一致性实证 | 60 周、120 国、144K VP：91.7% 国家存在不一致；严格审查国家（中国/巴基斯坦/科威特）审查率与不一致率双双 >92% | 高 | 是（可作为后续测量的基线结论） |
| 云平台 peering 归因与规避路径 | 云商与本地 ISP 的 peering 决定审查暴露：GCP 私有网络直连使流量绕过上游审查设备；印度→Bahrain 路径仅 8.4% 被审查 | 高 | 是（规避工具的动态选路信号；云商部署决策依据） |

### 5.3 适用场景

- 审查测量：把「一国是否封锁某域名」细化为「哪些路径封锁、哪些不封锁」。
- 规避实践：为代理/中继选择位置与云商（如印度用户选 Bahrain 或 GCP 上的代理）；可与 CenFuzz [50]、Geneva [11]、NetShuffle [35] 等规避框架组合，作为额外的路径维度。
- 服务提供方：将服务托管在审查暴露更低的平台，降低用户访问受阻概率。
- 政策评估：揭示「名义封锁」与「实际执行」之间的落差。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| ICLab [40] | 长期、多国 VPN 测量平台 | 仅用 VPN，路径不可控，覆盖有限 | 用 RESIP + 多目的地提升覆盖并引入路径维度 |
| Censored Planet [48] | 多技术同步、代表性强的全球观测 | 目的地固定，无法归因国内 ISP 级差异 | 在同一国家内分解路径，量化不一致 |
| OONI [21] | 社区驱动、覆盖面广 | 依赖志愿者，路径与部署不可控 | 主动控制目的地，结论可归因 |
| Quack [55] | 可扩展的应用层干扰远程测量 | 不区分路径，仅判定是否被干扰 | 以多目的地对比同一 VP 的多路径行为 |
| BreadCrumb [9] | 揭示 DNS 审查随包参数变化 | 仅 DNS、仅路由器负载均衡的小尺度变化 | 覆盖 HTTP 且路径变化可控、幅度大（跨 transit 网络） |
| Disguiser [30] | 端到端、静态载荷真值、精确定位 | 不研究路径多样性本身 | 复用其真值思路与被审域名列表，补充路径维度测量 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

两组实验：(1) **IP 目的地方向**：6 台 AWS 控制服务器（Virginia、California、São Paulo、London、Bahrain、Cape Town），60 周（2022 夏–2023 秋），144,418 个 VP / 120 国，>50% 国家 VP 超 1,500 个；(2) **托管平台方向**：AWS/GCP/Azure 各在 Virginia、Sydney、Paris、São Paulo 部署 1 台（共 12 台），36 周，66,123 个 VP / 120 国，>50% 国家 VP 超 600 个。探测参数：5 秒超时、超时重试 4 次；每国每周 VP 上限 80；剔除 164 个疑似缓存代理 VP。案例研究用商用 VPN（hide-my-ip）做应用层 traceroute，每国随机 32 个被审域名。

### 6.2 数据集

| 数据/资源 | 规模 | 用途 | 备注 |
|---|---|---|---|
| 实验 1 测量数据（IP 目的地） | 144,418 VP / 120 国 / 60 周 | 全球不一致性统计（§5.1、§5.2） | 覆盖 69 亿（83%）全球人口所在国家（UN 人口口径引用） |
| 实验 2 测量数据（托管平台） | 66,123 VP / 120 国 / 36 周 | 云平台不一致统计（§5.3） | 与实验 1 使用不同 VP 批次（Proxyrack 代理寿命有限） |
| 被审测试域名清单 | 国别清单（Alexa top 1000 + Citizen Lab 来源） | 构造 HTTP Host 头触发审查 | 来自 Disguiser [30]，经其测量验证过 |
| 应用层 traceroute 数据 | 2 国 × 32 域 × 12 控制服务器（2022 年 12 月） | 案例研究逐跳定位审查设备 | 附录 B Table 5/6 给出完整逐跳 AS/IP |

### 6.3 Baseline

本文无机器学习基线；对照对象是**既有测量平台与既有结论**：ICLab [40]、Censored Planet [48]、OONI [21]、Quack [55]、FilterMap [49]、Iris [44]、BreadCrumb [9]、Disguiser [30]（§8.1），以及「审查在国家层面近似 all-or-nothing」的既有观察（Bhaskar et al. [9]，本文 §5.1 复现了该分布）。

### 6.4 评价指标

VP 级审查率（% Censored）、VP 级不一致率（% Incons.）、域级审查率、destination inconsistency（不同目的地路径间审查百分比差）、hosting inconsistency（不同云平台间差值）、AS 级不一致（最大−最小审查百分比）、国家不一致分档计数（附录 A Table 4）。

### 6.5 关键实验结果

| 测量对象 | 指标 | 本文数值 | 对照/基线 | 落差/说明 | 证据 |
|---|---|---|---|---|---|
| 全球不一致普遍性 | 存在不一致的国家占比 | 91.7%（110/120 国） | 既往国家层面刻画默认全国一致 | 集中式审查实施普遍不完整/有缺陷 | §5.1 |
| 不一致严重国家 | 100% 不一致国家数 | 23 国（正文）/ 附录 A 表列 19 国 | 仅 11（10%）国不一致率 <9% | 正文与附录口径冲突（见文首警示） | §5.1, Appendix A |
| 高审查国家的内部一致假象 | 审查率 / 不一致率 | 中国 97.85%/99.27%；巴基斯坦 92.03%/99.49%；科威特 99.85%/93.86% | 哈萨克斯坦 100.00%/48.99% | 「封得严」不等于「封得一致」 | Table 1 |
| 域级不一致 | 同国不同域名审查率 | 泰国 livejasmin 1% vs bongacams 96%；越南 3%–43% | 印度/韩国域间差异较小 | 集中式与去中心化审查可能并存 | §5.1, Figure 7 |
| 目的地维度 | 路径间审查差 | 印度→Bahrain 仅 8.4% 被审，其余路径 37–60%；AS 204457（土耳其）不一致 81.0% | 同表 10 个 AS 全部 ≥59.4% | 目的地位置是主因之一 | §5.2, Table 2, Figure 8 |
| 托管平台维度 | 同地不同云审查差 | 韩国 AWS 98.93% / GCP 32.21% / Azure 76.64%（差 66.72）；印度 50.89/18.57/37.95（差 32.32） | 俄罗斯平台间差仅 11.39% | 16（13.3%）国平台差 >10% | §5.3, Table 3 |
| 案例：韩国 | 逐跳定位 | 3 条 AWS 路径均收 warning.or.kr 封锁页；GCP/Azure 无审查；全部流量经 AS 4766 (Korea Telecom) | 同 ISP 内不同跳点即产生不一致 | KT 与 GCP 私有网络在韩境内直连 | §6.2, Figure 13 |
| 案例：印度 | 逐跳定位 | Azure 路径恒被审；审查设备定位在 AS 9498（Bharti Airtel）；AWS/GCP 经 AS 4755（TATA）无审查 | 疑有审查设备复制 TTL（引用 [30] 的既有发现） | GCP 与 AS 4755 直连 peer 使流量入云内网络 | §6.3, Table 6 |

### 6.6 优势最明显的场景

- **发现可规避路径**：印度→Bahrain（8.4%）、韩国/印度→GCP；论文明确给出「为代理服务器选位置/选云商」的操作性建议。
- **解释既有矛盾的测量结果**：不同研究对同一国家的封锁率报告不一致，可由路径差异解释。
- **支撑规避框架**：把路径选择作为 CenFuzz/Geneva/NetShuffle 之外的正交规避维度。
- **提醒审查方视角的脆弱面**：集中式审查在实现层面漏洞普遍（论文结论之一）。

### 6.7 局限性

- 近 VP 部署的审查设备检测不到；VP 国家分布偏斜（部分国家 <200 个 VP）；VPN-based traceroute 的 vantage 位置偏商业化网络。
- 仅测 HTTP 层审查，DNS/HTTPS-SNI 未覆盖（作者列为 future work）。
- 被审域名清单继承自 Disguiser，可能漏掉路径相关的被审域名。
- 正文与附录在 100%/90–99% 不一致国家计数上不一致（23 vs 19；20 vs 18），引用时须注明口径来源。
- §5.2 的「>75%」与其后分句自相矛盾（疑小数丢失），destination inconsistency 的精确阈值表述存疑。

---

## 7. 学习与应用

### 7.1 是否开源？

解析稿未提及代码或数据发布；测试域名列表指向 Disguiser 的公开仓库（github.com/e2ecensor/Disguiser_public）。控制服务器与 VP 基础设施为作者自建，未承诺复用接口。

### 7.2 复现关键步骤

1. 订阅 RESIP（如 Proxyrack）获取住宅 VP，与平台确认使用条款；实施「每 IP 每周只用一次」与每国每周配额。
2. 在无 inbound 审查的国家/云区域部署多台控制服务器（地理分散 + 跨云商两种配置），并返回与合法页面不冲突的静态 payload。
3. 用缓存代理检测与合法页面 title 比对剔除污染 VP；用第三国 VPN 验证控制服务器方向无 inbound 审查。
4. 以国别被审域名清单构造 HTTP 请求（Host 头填域名、目的 IP 选控制服务器），5 秒超时 + 4 次重试判定审查。
5. 按国家/域名/AS 聚合审查率与不一致率；对重点国家用商业 VPN + 应用层 traceroute 逐跳定位审查设备。

### 7.3 关键超参数、预处理和训练细节

无模型训练。关键测量参数：超时 5 s（作者实测 5 s 无响应则更久也大概率无响应，短于既有工作的 15 s）；重试 4 次；每国每周 VP 上限 80；AS 分析仅保留 ≥80 个 VP 的 AS（共 3,913 个 AS 被采集，最大单 AS 1,186 个 VP）；附录国家分档仅统计 >200 个 VP 的国家；案例 traceroute 每国 32 个域名。

### 7.4 能否迁移到其他任务？

- **DNS / HTTPS-SNI 审查**：同框架可直接扩展（作者 future work），只需替换探测协议与真值判定方式。
- **中间盒策略测量**：任何「按目的地选路、按路径部署策略」的中间盒（限速、内容过滤、QoS 策略）都可复用「控目的地造路径」的设计。
- **CDN/云选路优化**：把「路径多样性」作为可达性设计的自变量（服务方主动选择低审查云商/区域）。

### 7.5 对我的研究有什么启发？

- 测量类研究的实验设计启示：**把不可控的环境变量变成可控的实验变量**（此处是路由），是该论文最可迁移的方法论。
- 报告规范：结论必须带「测量位置/路径」的限定，国家层面的单一数字可能掩盖 ISP 级差异；同理，流量分类/指纹数据集采集也应报告「采集自哪些 AS/地域」。
- 云平台 peering 差异是真实且可利用的网络结构事实，对代理/中继部署与测量基础设施选址有直接指导。
- 与既有工作的对齐：Disguiser 的真值检测思想（静态 payload）在本文被复用于路径维度，提示「复用他作基础设施 + 更换自变量」是一种高效的研究推进方式。

---

## 8. 总结

### 8.1 核心思想

> 换个目的地就换条审查路径，国家审查并不一致。

### 8.2 速记版 Pipeline

1. 订阅住宅 IP 代理（RESIP）获得全球 VP，预筛剔除缓存代理。
2. 部署多台地理分散/跨云商的控制服务器，返回静态 payload 作为真值。
3. 用他国 VPN 验证控制服务器方向无 inbound 审查。
4. VP 以「被审域名 + 不同目的 IP」发请求（5 s 超时 + 4 次重试），双侧收集结果。
5. 聚合审查率与不一致率（VP/域/AS/平台维度），并用应用层 traceroute 案例归因到具体 peering 配置。
6. 结论：91.7% 国家存在不一致；低审查路径（Bahrain、GCP）可用于规避。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[censorship-circumvention]]（本文 §5.4 直接讨论利用路径差异实现规避，并给出与规避框架的组合方式）

### 9.2 相关方法

- [[2020-CCS-Censored_Planet__An_Internet-wide__Longitudinal_Censorship_Observatory]]（[48] 本文引用的全球审查观测平台，作为对照的既有测量体系）
- [[2024-NDSS-On_Precisely_Detecting_Censorship_Circumvention_in_Real-World_Networks]]（同主题 A 表笔记；未被本文引用，为延伸阅读）
- [[2025-USENIX-Censorship_Evasion_with_Unidentified_Protocol_Generation]]（同主题 A 表笔记；未被本文引用，为延伸阅读）
- [[2026-NDSS-Huma__Censorship_Circumvention_via_Web_Protocol_Tunneling_with_Deferred_Traffic_Replacement]]（同主题 A 表笔记；未被本文引用，为延伸阅读）

### 9.3 相关任务

- 库内暂无与「审查测量」对应的任务页；本文与 [[censorship-circumvention]] 概念页的关联最强。

### 9.4 可更新的综述页面

- [[claims-index]]（候选新增：「国家层面的审查刻画会系统性低估 ISP/路径级不一致」——本文以 91.7% 国家存在不一致为实证）
- 库内现有 5 个综述页（加密流量分析/小样本/恶意流量/流量基础模型/网站指纹）均不覆盖审查测量主题，暂无可直接更新的综述页。

### 9.5 可加入的对比表

- [[method-comparison-table]]（§8.1 的测量平台对比：OONI / Quack / FilterMap / ICLab / Censored Planet / Iris / BreadCrumb / Disguiser vs Pathfinder 的覆盖、真值方式与路径控制能力）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 集中式审查的实现普遍不完整或有缺陷，去中心化审查也常见 | 摘要与 §5.1 结论 | Abstract, §5.1 |
| 91.7%（110/120）国家存在审查不一致，仅 11（10%）国低于 9% | 正文统计 | §5.1 |
| 审查分布呈 all-or-nothing：79（66%）国 <20%、21（17.6%）国 >80%、仅 20（16.8%）国居中 | Figure 6 与正文 | §5.1 |
| 34/74（46%）个 VP 超千的国家不一致率 >80%；12 个 VP 少于 500 的国家达 100% 不一致 | 正文 | §5.1 |
| 中国/巴基斯坦/科威特审查率与不一致率双 >92% | Table 1 | §5.1, Table 1 |
| 泰国域级差异：livejasmin 1% vs bongacams 96%；越南 3%–43% | Figure 7 与正文 | §5.1 |
| 印度指向 Bahrain 的路径审查率仅 8.4%，其余 37–60% | Figure 8 与正文 | §5.2 |
| AS 级不一致最高 81.0%（AS 204457，土耳其），前 10 全部 ≥59.4%，其中含零审查路径 | Table 2 | §5.2 |
| 16（13.3%）国云平台间审查差 >10%；韩国差 66.72、印度差 32.32 | Table 3 与正文 | §5.3 |
| 韩国案例：AWS 三路径均收 warning.or.kr 封锁页，GCP/Azure 无审查，全部经 AS 4766 | Figure 13 与正文 | §6.2 |
| 印度案例：Azure 恒被审，审查设备在 AS 9498（Bharti Airtel），疑似 TTL 复制；AWS/GCP 经 AS 4755（TATA）无审查 | Table 6 与正文 | §6.3 |
| 100% 不一致国家计数存在内部冲突：正文 23 国 vs 附录 A Table 4 的 19 国（90–99% 档同样 20 vs 18） | 正文与 Appendix A | §5.1, Appendix A |
| 测量伦理：每住宅 IP 每周仅用一次、不触达真实被审内容、IRB 豁免 | §3.4 | §3.4 |
| 60 周实验、144,418 VP、120 国，覆盖 83% 全球人口所在国家 | §4.1 正文 | §4.1 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2025-ACSAC-Pathfinder__Exploring_Path_Diversity_for_Assessing_Internet_Censorship_Inconsistency.pdf
- MinerU Markdown：02-parsed-markdown/2025-ACSAC-Pathfinder__Exploring_Path_Diversity_for_Assessing_Internet_Censorship_Inconsistency.md

---

## 12. 后续问题

- 23 国（正文）与 19 国（附录 A Table 4）的 100% 不一致计数差异，是人口口径（>200 VP 过滤）还是笔误？90–99% 档（20 vs 18）同理。
- 该框架对 DNS 与 HTTPS/SNI 审查的扩展（作者 future work）是否会呈现同等量级的不一致？
- 不一致的时间稳定性：60 周内路径与审查策略变化如何随时间演化（作者称将继续长期运行）？
- RESIP 网络位置偏斜（数据中心 VPN vs 住宅代理）对不一致率估计的偏差有多大？是否有校准方法？
- 云商 peering 造成的「审查盲区」（如 GCP 私有网络直连）是否会被审查方通过部署在更上游的过滤点封堵？自适应对抗未做。
- 论文未公开数据集，复现该规模测量（144K VP、跨 120 国、60 周）的成本与其他团队的可复现性如何？

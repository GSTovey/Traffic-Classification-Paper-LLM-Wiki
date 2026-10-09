---
type: paper
title_original: "A Measurement of Genuine Tor Traces for Realistic Website Fingerprinting"
title_cn: "面向真实网站指纹的 Tor 真实踪迹测量：GTT23 数据集"
authors: ["Rob Jansen", "Ryan Wails", "Aaron Johnson"]
year: 2026
venue: "PAM 2026"
doi: "unknown"
url: "unknown"
pdf: "00-inbox/PDFs/2026-PAM-A_Measurement_of_Genuine_Tor_Traces_for_Realistic_Website_Fingerprinting.pdf"
mineru_md: "02-parsed-markdown/2026-PAM-A_Measurement_of_Genuine_Tor_Traces_for_Realistic_Website_Fingerprinting.md"
status: processed
reading_level: L3
research_area: ["website-fingerprinting", "anonymous-traffic-identification", "encrypted-traffic-analysis"]
task: ["website-fingerprinting"]
method: []
dataset: ["GTT23", "BigEnough", "GoodEnough"]
code: "https://doi.org/10.5281/zenodo.10620520"
relevance: high
created: "2026-09-19"
updated: "2026-09-19"
---

# A Measurement of Genuine Tor Traces for Realistic Website Fingerprinting

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | A Measurement of Genuine Tor Traces for Realistic Website Fingerprinting |
| 中文标题 | 面向真实网站指纹的 Tor 真实踪迹测量：GTT23 数据集 |
| 作者 | Rob Jansen（美国海军研究实验室 NRL）、Ryan Wails（NRL / Georgetown University）、Aaron Johnson（NRL）|
| 年份 | 2026 |
| 会议/期刊 | Passive and Active Measurement Conference（PAM 2026，第 27 届）；解析稿自述为会议论文的 full version，额外含 Listing 1、Table 1、Appendix A |
| 研究方向 | website-fingerprinting / anonymous-traffic-identification / encrypted-traffic-analysis |
| 任务类型 | WF 数据集的测量与构建（Tor 出口中继侧的真实 cell trace 采集）、WF 数据集生态综述与统计对照评估 |
| 方法关键词 | 出口中继测量（exit-relay measurement）、概率采样（合理否认）、不可逆哈希标签（sha256+已销毁 salt）、cell trace 表示、幂律/base-rate 统计分析、28 个 WF 数据集综述 |
| 数据集 | GTT23（本文构建）；对照数据集 BigEnough、GoodEnough；综述覆盖 2008–2025 年 28 个 WF 数据集 |
| 是否开源 | GTT23 为受控发布：自 2024 年起向验证过的研究者按需提供（§1、§5）；数据集 DOI 10.5281/zenodo.10620520（文中 ref [27]，论文本身未给 DOI/arXiv 标识）|
| PDF | 00-inbox/PDFs/2026-PAM-A_Measurement_of_Genuine_Tor_Traces_for_Realistic_Website_Fingerprinting.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-PAM-A_Measurement_of_Genuine_Tor_Traces_for_Realistic_Website_Fingerprinting.md |

> ⚠️ MinerU 解析问题：(1) 结论段 "available to researchers upon request since 2004 since [27]" 年份系原文笔误（§1 明确写 since 2024），且 "since…since" 重复；(2) Appendix B 的 Table 3 caption 出现严重 small-caps 下标碎片化（`T<sub>a</sub>bl<sub>e</sub> 3 <sub>:</sub>…`），表体单元格亦有错位、跨行信息粘连，引用时需回原文核对；(3) 连字（ligature）普遍丢失：effectiveness→"efectiveness"、suffix→"sufix"、different→"diferent"、offline→"ofline"、efficiency→"eficacy/eficient"；§2.2.2 中编码函数名多次显示为占位符 �（公式本体 Eq.(1) 完整）；(4) 摘要含 "per formance" 断词、`$D S _ { T o r }$` 等 LaTeX 碎片，Listing 1 的 JSON 被逐字符插入空格。

---

## 1. 一句话总结

> 用 8 台 Tor 出口中继做 13 周被动测量，构建首个真实 Tor 踪迹数据集 GTT23（1390 万条电路、114 万域名），并对照 28 个合成 WF 数据集揭示其四类系统性缺陷。

---

## 2. 摘要翻译

### 2.1 摘要原文

> Website fingerprinting (WF) is a dangerous attack on web privacy because it enables an adversary to predict the website a user is visiting, despite the use of encryption, VPNs, or anonymizing networks such as Tor. Previous WF work almost exclusively uses synthetic datasets to evaluate the performance and estimate the feasibility of WF attacks despite evidence that synthetic data misrepresents the real world. In this paper we present GTT23, the first dataset of genuine Tor traces, which we obtain through a large-scale measurement of the Tor network and which is intended especially for WF. It represents real Tor user behavior better than any existing WF dataset, is larger than any existing WF dataset by at least an order of magnitude, and will help ground the future study of realistic WF attacks and defenses. […] We have made GTT23 available to promote reproducible research and to help inspire new directions for future work.

（节选；"performance"/"effectiveness" 原文在解析稿中因连字丢失写作 "per formance"/"efectiveness"，此处按正常拼写还原。）

### 2.2 摘要中文翻译

> 网站指纹（WF）是对网络隐私的危险攻击，即使使用加密、VPN 或 Tor 等匿名网络，攻击者仍能预测用户正在访问的网站。尽管已有证据表明合成数据无法反映真实世界，此前 WF 工作仍几乎完全使用合成数据集来评估攻击性能、估计攻击可行性。本文提出 GTT23——首个真实 Tor 踪迹数据集，通过对 Tor 网络的大规模测量获得，专为 WF 设计。它比任何现有 WF 数据集都更好地代表真实 Tor 用户行为，规模至少比现有最大 WF 数据集大一个数量级，将为今后研究真实的 WF 攻击与防御奠定基础。我们详细评估并综述了 2008 年以来发布的 28 个 WF 数据集，与 GTT23 的特征进行对比，发现合成数据集的常见缺陷使其难以支撑关于"针对真实 Tor 用户的 WF 攻防有效性"的有意义结论。GTT23 已开放以促进可复现研究并启发新的研究方向。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

WF 攻击在 Tor 场景下尤其严重（可破坏 Tor 匿名性）。用 ML 做 WF 需要**带标签**的踪迹：既用于训练分类器，也用于评估攻击效能。但攻击者从入口侧观测时，目标网站信息被 onion routing 加密，无法自行打标。通过综述 2008 年以来的 28 个 WF 数据集，作者发现：除一项研究外，**所有**先前工作都使用自动化浏览器程序化抓取网页来采集带标踪迹——即合成数据集。这类数据集在多个维度上被批评为不代表真实 Tor 流量，并已让 WF 研究落入 base rate fallacy 等常见 ML 评估陷阱。

### 3.2 现有方法的痛点和不足

| 痛点 | 具体表现 | 证据位置 |
|---|---|---|
| 组成单一 | 所有被综述数据集几乎只含 web 流量；真实 Tor 用户会使用多种软件（支持 SOCKS5 的网络应用）、与非 web 服务交互 | §4.1、Appendix B |
| 用户模型简化 | 用单一自动化爬虫（如 tor-browser-selenium）静态抓取，几乎全在客户端位置采集 | §4.1、Appendix B |
| 只取热门页面 | 通常只抓 Alexa/OpenPageRank 榜单首页或随机子页，忽略长尾 | §4.1、Table 3 |
| base rate 不真实 | 不含自然访问频率，导致 FPR/precision 估计失真 | §4.1、§4.2.4 |
| 真实数据不可复现 | 唯一的真实数据工作 Cherubin et al. [10] 采用全在线设置（不持久化真实数据与分类器），结果无法复现、方法难以被后继工作复用 | §1、§2.1 |

### 3.3 论文的研究假设或核心直觉

核心直觉：**出口中继处可以看到电路首流的 DNS 查询**。Tor Browser 会把加载某 URL 的所有流（含第三方域名内嵌对象）分配到与 URL 的 first-party domain name（FPDN）唯一绑定、相互隔离的电路上；因此电路首流 DNS 查询中的 FPDN 可作为该 cell trace 的网站标签。非出口中继因 onion routing 看不到域名。于是：一个受控运行出口中继的测量者，可以被动、大规模地采集**真实用户产生**且**带标**的 cell trace。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 28 个 WF 数据集综述显示：除 1 项外全部用自动化浏览器抓取，数据为合成 | §1、§4.1、Table 3 |
| 痛点提炼 | 合成数据不真实 → 训练/评估偏差 → 落入 base rate fallacy 等评估陷阱 → 无法估计真实世界 WF 性能 | §1、§4.1、§4.2 |
| 问题转化 | 提升为可研究的科学问题：如何在不损害用户隐私与安全的前提下，规模化采集"真实用户 + 真实标签"的 Tor 踪迹？ | §2.2、§2.3、Appendix A |
| 文献定位 | 仅 Cherubin et al. [10] 做过出口侧真实采集，但为全在线、不可复现；后继工作仍继续使用合成数据 | §1 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 H1 | 通过受控出口中继 + 概率采样 + 不可逆编码，可以在满足伦理/隐私要求的前提下规模化采集带 FPDN 标签的真实 Tor 踪迹 | §2.2、Appendix A（推断自测量设计） | 实际执行 13 周测量（8 台出口中继），得 13,900,621 条电路 |
| 辅助假设 H2 | 合成 WF 数据集在 WF 关键特征（trace 长度、类内方差、访问 base rate）上与真实踪迹存在显著统计差异 | §4.2 开头（推断） | 与 BigEnough/GoodEnough 的逐域统计对比（Fig. 6） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| H1 | 支撑 | 13 周测得 13,900,621 条电路 / 1,142,115 个域名 / 68 个端口；IRB 认定非人类受试研究、TRSB 给出 "No Objections" 并要求受控发布 | §3.1、§2.3、Appendix A.5 |
| H2 | 支撑 | GoodEnough 约 70% 域名中位电路长度顶到 5,000 cell 采集上限，GTT23 仅 32%；中位域名出现频率 GTT23 5×10⁻⁴ vs BigEnough 1×10⁻²、GoodEnough 4×10⁻³；GTT23 各百分位 CV 更高 | §4.2.2–§4.2.4, Fig. 6 |

---

## 4. 方法设计

### 4.1 方法整体流程

本文的"方法"是一条**测量方法论 + 数据集构建 + 对照评估**流水线：与 IRB / Tor Research Safety Board（TRSB）协商确定安全边界 → 给 Tor 中继打补丁（电路采样、元数据记录、域编码）→ 在 Calyx Institute 托管的两台机器上运行 8 台出口中继、执行 13 周测量 → 记录电路元数据并加密落盘 → 汇总为 GTT23 → 描述性统计（端口、电路长度、域名分布、类内变异）→ 综述 28 个既有 WF 数据集并把 GTT23 与 BigEnough/GoodEnough 做统计对照。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 电路筛选 | 中继观察到的新电路 | 拒绝非出口型电路（onion-service、内部电路）；对出口型电路按区间做概率采样：高量期拒绝 80%、低量期拒绝 98% | 被选中的出口电路 | 限制数据总量 + 为用户提供合理否认（plausible deniability） |
| Step 2 电路测量 | 被选中电路 | 迭代构造元数据记录，直到电路关闭或观测到 N 个 cell（先到者为准）；记录 `(time, direction, cell command, relay command)` 四元组 | circuit metadata record（Listing 1） | 得到可做 WF 的 cell trace 与标签 |
| Step 3 隐私编码 | 域名、最短私有后缀 | 施加 H(x)=base64encode(sha256(x‖salt))，salt 随机选定、全测量期固定、事后销毁 | 不可逆的域名标签 | 保护目的地隐私，同时保证数据集内标签一致 |
| Step 4 导出与落盘 | 元数据记录 | 经 Tor 控制接口导出到外部进程 → 压缩 → 公钥加密 → 写持久化存储（私钥离线保存） | 加密存储的测量记录 | 防未授权解密 |
| Step 5 数据集汇总 | 全部记录 | 合并为 GTT23（2023 年，13 周） | GTT23 数据集 | 供研究者按需申请 |
| Step 6 分析与对照 | GTT23 + 28 个既有数据集 | 描述统计（Fig. 1–5）；综述 28 个数据集（Table 2/3）；与 BigEnough、GoodEnough 做逐域统计对照（Fig. 6） | 缺陷清单 + 统计差异证据 | 论证合成数据集不可替代真实数据 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 打补丁的 Tor 出口中继 | 电路采样 + 元数据记录 + 域名编码 | 真实电路与 cell 流 | 内存中的元数据记录 | 全流程核心；被动运行，不改协议、不增网络负载 |
| 采样器（Circuit Selection） | 按测量区间的高/低量级拒绝 80%/98% 出口电路 | 新电路事件 | 是否测量该电路 | 与 Step 1 对应；提供合理否认 |
| 编码函数 H(·) | 对域名与最短私有后缀做 sha256+base64 不可逆编码 | 域名字符串、salt | 定长随机字符串标签 | salt 事后销毁，映射不可复现 |
| 外部导出进程 | 压缩、公钥加密、写盘 | 元数据记录 | 加密持久化记录 | 私钥离线存放 |
| 分析流水线 | 端口/长度/域名分布、幂律拟合、CV/CD、base rate 计算 | GTT23 | Fig. 1–5 统计结果 | 支撑 §3.2 与 §4.2 |
| 对照评估组件 | 28 数据集综述 + 与 BigEnough/GoodEnough 逐域对比 | GTT23 + 既有数据集 | 缺陷清单与差异证据 | §4.1/§4.2 |

### 4.4 公式、算法和机制解释

1) **标签编码（Eq. 1）**：H(x) = base64encode(sha256(x ‖ salt))。salt 均匀随机、全测量中继固定、测量结束后销毁；base64encode 与 sha256 用 Tor 内部实现。域名字段记 H(D)，`shortest_private_suffix` 记 H(S)（S 用 Mozilla public suffix list + libpsl 计算最短私有后缀）。
2) **cell trace 表示**：某一网络位置的电路流量可表示为按时间排序的 (direction, time) 序列（每个 cell 一项），即 cell trace——这是 Tor 场景 WF 的常用输入形式（Tor 定长 cell；WF 分类器通常只知道 cell 出现时刻与方向）。
3) **FPDN 标注机制**：Tor Browser 计算 URL 的首方域名 FPDN，并把加载该 URL 的所有流（含第三方域名）放在与 FPDN 唯一绑定的隔离电路上；访问新网站会新建电路、先解析 FPDN 的 DNS，再加载页面；同一网站的后续子页面复用同一电路。因此"电路首流 DNS 查询"即网站标签。
4) **幂律拟合**：每域名电路数服从幂律（shape=0.023，loc=0.769，scale=1,495,234），少量热门域名主导、长尾极长。
5) **类内变异度量**：变异系数 CV = 标准差/均值（Fig. 5 显示过半域名 CV>1）；离散系数 CD = 方差/均值（多数域名的电路长度相对方差达数百 cell）。
6) **base rate 与精度机制**：开放世界二分类中负类由所有非监控站点构成，FPR（由负类 base rate 决定）直接决定 precision；多分类（开放/闭世界）中总体准确率取决于各类 base rate。故 base rate 真实性是评估 WF 攻击的前提。

### 4.5 方法优势

- **真实性**：真实用户 + 真实服务 + 自然 base rate，覆盖非 web 服务与长尾域名（4% 电路来自非 web 常见端口）。
- **规模**：13,900,621 条电路 / 1,142,115 个域名，比此前最大数据集（AWF，2.3×10⁶）大一个数量级，满足现代深度学习对样本量的需求。
- **伦理设计**：数据最小化、被动无协议改动、采样带来合理否认、不存绝对时间戳、不可逆哈希标签、公钥加密落盘、私钥离线。
- **可复现与可复用**：与 Cherubin et al. 的全在线方案不同，GTT23 是持久化数据集，可训练也可测试，支持离线/在线流式两种用法。

### 4.6 方法不足

- 标签经不可逆哈希：无法与带真实域名标签的其他数据集直接合成（作者提出用自监督预训练 + 少样本微调规避）。
- 出口侧视角：观测点与"客户端侧攻击者"不同，直接测量可能高估客户端可见的耗时（作者团队后续的 Retracer / CellShift 工作正是为此做踪迹变换）。
- 无绝对时间戳、采样稀疏（80% 域名只有 1 条电路），限制了时序漂移类研究与按域名细粒度分析。
- 采集于 2023 年、8 台中继：覆盖的是当时 Tor 网络与用户行为的一个截面。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

主流做法（28 个数据集中的 27 个）是"客户端位置的自动化爬虫 + 已知目标清单"，标签来自抓取脚本本身；本文是"出口中继位置的被动观测 + 首流 DNS 的 FPDN"，标签来自真实用户的真实访问行为。前者可以在任意时间、任意目标上按需造数据但牺牲真实性；后者牺牲目标可控性换取真实性与自然 base rate。与同样在出口侧采集的 Cherubin et al. [10] 相比，本文的关键区别是**离线持久化**（可复现、可训练）而非全在线评估。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 首个真实 Tor 踪迹数据集 GTT23 | 13 周、8 台出口中继、13,900,621 条带 FPDN 标签电路 | 高 | 否（数据本身不可迁移，但方法论可） |
| 安全可复现的采集方法论 | 采样+合理否认、salt 销毁的不可逆标签、加密落盘、无绝对时间戳，经 IRB/TRSB 审核 | 高 | 是 |
| 28 个 WF 数据集系统综述 | 2008–2025，按 Year/Activity/User model/Software/Size/Availability/Attacks 多维对比（Table 3） | 中高 | 是（可直接用于数据集选择与评审） |
| 真实 vs 合成的量化差异证据 | 首长度、类内方差、base rate 三维度逐域对照 | 高 | 是 |

### 5.3 适用场景

WF 攻击/防御的训练与测试（尤其对 FPR、precision 敏感的开放世界与 base-rate 评测）；WF 防御在真实流量上的有效性检验；Tor 流量统计（此前测量已过时 5 年以上）；Tor 仿真/测试床的真实性校准；非 WF 用途（流量相关性攻击、Tor 恶意软件检测）。

### 5.4 方法对比表

| 方法/数据集 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 合成 WF 数据集（AWF、DF、GoodEnough、BigEnough 等 27 个） | 目标可控、采集便宜、类均衡、便于复现实验设计 | 仅 web、简化用户模型、只抓热门页、无真实 base rate；易致 base rate fallacy | 以真实用户流量与自然 base rate 取代 |
| Cherubin et al. 2022（出口侧真实采集，全在线） | 首个真实、在线评估、贴近实际部署 | 不持久化数据与分类器，结果不可复现、方法难复用 | 持久化数据集 + 可复现方法论 |
| GTT23（本文） | 真实、量大（大一个数量级）、受控发布、伦理设计完备 | 标签不可逆、出口侧视角、无绝对时间戳、域名级稀疏 | — |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

本文无分类器实验，评估由三部分组成：(a) GTT23 的描述性统计分析（端口、电路长度、域名频次、类内变异）；(b) 28 个 2008–2025 年 WF 数据集的综述与缺陷归纳（Table 2 为节选、Table 3 为全表，见 Appendix B）；(c) 与 BigEnough、GoodEnough 的统计对照——为统计严谨，只取 ≥1,000 cell 的 trace，并在其中只保留 ≥30 条 trace 的域名（Fig. 6）。

### 6.2 数据集

- GTT23：2023 年 13 周、8 台出口中继（Calyx Institute 托管，两台同构机器，各 2×Intel Xeon E5-2695 v2 12 核、共 48 超线程，1 Gbit/s 对称不限量链路）；第 1/7/13 周为高量期、其余 10 周为低量期；13,900,621 条电路（高量期 10,557,898、低量期 3,342,723），1,142,115 个域名、68 个端口；受控发布。
- BigEnough（Mathews et al. 2023 S&P，Open PageRank 榜单，950 类 ×20 条，3.8×10⁴）与 GoodEnough（Pulls 2020，Alexa 首页+随机子页，500 类 ×20 条，2×10⁴）：两者每站至少 10 页，是综述中网站多样性最高的合成数据集代表。

### 6.3 Baseline

本文不以分类器为 baseline，而是以**既有数据集**为对照对象；文中另引用了三个下游使用 GTT23 的结果作为外部参照：Retracer（WPES 2023）与 CellShift（NDSS 2026）表明真实设置下 WF 准确率远低于合成数据集的暗示；Deng et al.（Tsinghua Science and Technology 2025）在监控集检测任务上发现 Var-CNN 准确率高于 DF。

### 6.4 评价指标

电路数/域名数/端口数、每电路 cell 数（中位数、分位数）、每域名电路数（幂律参数）、变异系数 CV、离散系数 CD、域名出现频率（base rate）、每域中位电路长度、非 web 端口占比。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文（GTT23） | 最优对比 | 提升/差异 | 说明 |
|---|---|---:|---:|---:|---|
| 真实性对照 | 域名中位电路长度顶到 5,000 cell 采集上限的比例 | 32% | GoodEnough 约 70% | — | 合成数据 trace 明显偏长（§4.2.2, Fig. 6） |
| base rate 对照 | 中位域名出现频率 | 5×10⁻⁴ | BigEnough 1×10⁻²；GoodEnough 4×10⁻³ | 高 1–2 个数量级 | 合成数据高估常见站点频率（§4.2.4） |
| 类内方差 | 各域 trace 长度 CV 分布 | 各百分位均更高 | BigEnough/GoodEnough 更低 | — | 真实流量更难分类（§4.2.3, Fig. 6） |
| 规模 | trace 数 | 1.4×10⁷（13,900,621） | AWF CW900 2.3×10⁶ | ≥1 个数量级 | 显著大于除 AWF 外的所有数据集（§4.1, Table 2） |
| 端口分布 | 首连接使用 80/8080/443 的电路占比 | 96%（13,356,305） | — | — | 其余大多为 43/4321（WhoIs/Remote WhoIs）|
| 电路长度 | 全部电路中位 cell 数 | 25（≤10.5 KB 应用载荷） | — | — | 与 HTTP Archive ">90% 页面 >450 KB" 对照，说明多数电路未承载完整页面（§3.2, Table 1, Fig. 3） |
| 域名集中度 | 仅 1 条电路的域名数 | 908,422（80%） | — | — | 幂律拟合 shape=0.023, loc=0.769, scale=1,495,234（§3.2, Fig. 4） |
| 测量规模 | 13 周电路/日均电路 | 13,900,621；高量期日均 502,757、低量期日均 47,753 | — | — | weeks 1/7/13 为高量期（§3.1, Fig. 1） |

### 6.6 优势最明显的场景

需要**真实 base rate 与真实类内多样性**的评估：开放世界攻击的 precision/FPR 估计、Tik-Tok 式评估陷阱的规避、WF 防御在真实流量上的有效性检验、以及训练时补充"背景类"负样本。作者特别强调：**测试**阶段使用真实踪迹比训练阶段更重要。

### 6.7 局限性

见 §4.6；作者明确承认的两点是：标签不可逆哈希限制与带标签数据集合成；以及需要针对真实踪迹专门设计与调优的新 WF 分类技术（未来工作）。

---

## 7. 学习与应用

### 7.1 是否开源？

GTT23 非公开下载：自 2024 年起向研究者**按需申请**、TRSB 建议的受控发布方式（§1、§5、Appendix A.5）；数据集 DOI 为 10.5281/zenodo.10620520（文中 ref [27]）。论文本身未提供代码仓库。

### 7.2 复现关键步骤

1. 与所在机构 IRB 与 Tor Research Safety Board 沟通，明确数据最小化、范围与发布机制（本文：受控发布 + "No Objections"）。
2. 给 Tor 中继打补丁：非出口电路剔除、按区间概率采样（80%/98% 拒绝）、元数据记录（day/domain/最短私有后缀/port/cells）、H(·) 编码。
3. 部署出口中继族（relay family）被动运行，测量期固定 salt、结束后销毁；记录经控制接口导出、压缩、公钥加密后落盘，私钥离线。
4. 汇总为数据集；用幂律拟合、CV/CD、base rate 等统计做数据集画像。
5. 对照评估：按 Year/Activity/User model/Software/Size/Availability/Attacks 维度综述既有数据集，并对可比数据集做逐域统计对照。

### 7.3 关键超参数、预处理和训练细节

| 项目 | 取值 |
|---|---|
| 测量时长 | 13 周（2023 年）；第 1/7/13 周为高量期，其余 10 周为低量期 |
| 采样拒绝率 | 高量期 80%、低量期 98% 的出口型电路被拒 |
| 中继规模 | 8 台出口中继（两台同构机器各 4 台） |
| 硬件 | 每机 2×Intel Xeon E5-2695 v2（共 48 超线程）、1 Gbit/s 对称不限量链路 |
| 元数据字段 | day / domain=H(D) / shortest_private_suffix=H(S) / port / cells 4 元组 (time, direction, cell command, relay command) |
| 编码 | H(x)=base64encode(sha256(x‖salt))，salt 测量后销毁 |
| 对照统计口径 | 仅 ≥1,000 cell 的 trace，且仅 ≥30 条 trace 的域名 |

### 7.4 能否迁移到其他任务？

（L3 迁移价值分析）

| 迁移方向 | 可迁移内容 | 迁移难度 | 说明 |
|---|---|---|---|
| 其他匿名/代理网络的真实踪迹采集 | "特权观测点 + 概率采样 + 不可逆标签"方法论 | 中 | 前提是存在类似 FPDN 的标签泄漏机制（如代理首请求域）；VPN 无逐电路隔离机制，需重新设计打标 |
| 流量分类数据集的可信度审计 | 7 维数据集综述模板 + 与真实数据的逐域统计对照法 | 低 | 可直接复用到加密流量分类数据集（如 ISCXVPN2016/USTC-TFC2016 的 base rate 与用户模型审查） |
| WF 攻击/防御评测协议 | 强调"测试必须用真实踪迹"、base-rate 敏感的指标配置 | 低 | 对本课题组的 WF 论文实验设计有直接约束价值 |
| 训练范式 | 不可逆标签下用自监督预训练 + 少样本微调 | 中 | 作者在 §5 明确提出；与表征预训练方向衔接 |
| 仿真/testbed 校准 | 用真实踪迹的时序与模式提升 Shadow 类仿真真实性 | 中 | 论文 §5 提出（refs [22,23]） |

### 7.5 对我的研究有什么启发？

1. **评测协议优先于模型**：GTT23 表明 WF 结论对 base rate 与类内方差高度敏感；做 WF/加密流量实验时应显式报告 base rate 与 FPR@低 FPR 的 precision。
2. **数据集缺陷是可发表的贡献**：把"数据集可信度审计"作为独立研究点（本文 28 数据集综述即核心贡献之一）。
3. **标签不可逆是可用约束**：哈希标签破坏了跨数据集合成，却不妨碍自监督预训练——这是一个把隐私约束转成方法创新点的范例。
4. **真实数据是防御评估的试金石**：防御（padding 等）在合成数据上常被高估，真实数据可暴露其代价与收益的真实权衡。

---

## 8. 总结

### 8.1 核心思想

> 出口中继看得到首流 DNS，于是真实 WF 数据可被合法、规模化地采集。

### 8.2 速记版 Pipeline

1. 与 IRB/TRSB 协商，确定安全边界与受控发布；
2. 给 Tor 中继打补丁：剔除非出口电路、80%/98% 概率采样、记录电路元数据、H(·) 编码域名；
3. 8 台出口中继被动运行 13 周，记录经压缩+公钥加密落盘（salt 事后销毁、私钥离线）；
4. 得到 GTT23：13,900,621 条电路 / 1,142,115 个域名 / 68 个端口，只有 25 cell 中位长度、80% 域名仅 1 条电路；
5. 综述 28 个既有数据集并与 BigEnough/GoodEnough 对照，证明合成数据在长度、方差、base rate 三方面失真。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]]
- [[anonymous-traffic-identification]]
- [[encrypted-traffic-analysis]]

### 9.2 相关方法

- 无。本文为测量/数据集工作，白名单中的 8 个方法页（contrastive-learning / convolutional-network / graph-neural-network / multi-modal-fusion / pre-training-finetuning / self-supervised-learning / state-space-model / transformer）均不匹配；论文 §5 提到未来可用自监督预训练应对哈希标签，但本文未使用任何学习型方法。

### 9.3 相关任务

- [[website-fingerprinting]]

### 9.4 可更新的综述页面

- [[survey-website-fingerprinting]]

### 9.5 可加入的对比表

- [[dataset-comparison-table]]（GTT23 是首个真实 Tor 踪迹数据集，应作为"真实 vs 合成"维度的核心条目；其 28 数据集综述（Table 3）可直接为该表补全 Year/Activity/User model/Software/Size/Availability 列）

**相关论文（知识库内）**：[[2022-USENIX-Online_Website_Fingerprinting__Evaluating_Website_Fingerprinting_Attacks_on_Tor_in_the_Real_World]]（本文方法论的直接前身）、[[2026-NDSS-CELLSHIFT__RTT-Aware_Trace_Transduction_for_Real-World_Website_Fingerprinting]]、[[2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild]]、[[2023-S&P-SoK__A_Critical_Evaluation_of_Efficient_Website_Fingerprinting_Defenses]]（BigEnough）、[[2023-CCS-Realistic_Website_Fingerprinting_by_Augmenting_Network_Traces]]、[[2023-USENIX-Subverting_Website_Fingerprinting_Defenses_with_Robust_Traffic_Representation]]、[[2024-USENIX-Stop__Don't_Click_Here_Anymore__Boosting_Website_Fingerprinting_By_Considering_Sets_of_Subpages]]、[[2024-CCS-Towards_fine-grained_webpage_fingerprinting_at_scale]]、[[2025-S&P-Countmamba__A_Generalized_Website_Fingerprinting_Attack_via_Coarse-Grained_Representation_and_Fine-Grained_Prediction]]、[[2025-CCS-Swallow__A_Transfer-Robust_Website_Fingerprinting_Attack_via_Consistent_Feature_Learning]]、[[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]]

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| GTT23 唯一使用真实用户流量 + 自然 base rate | 13 周 / 8 出口中继 / 13,900,621 条电路 / 1,142,115 域名 | §1、§3.1 |
| 电路普遍极短 | 全集中位 25 cell（≤10.5 KB 载荷）；仅 32% 域名中位长度达 5,000 cell | §3.2, Fig. 3；§4.2.2, Fig. 6 |
| 域名访问呈强长尾 | 幂律 shape=0.023, loc=0.769, scale=1,495,234；80%（908,422）域名仅 1 条电路 | §3.2, Fig. 4 |
| 合成数据集 trace 偏长 | GoodEnough 约 70% 域名中位 5,000 cell vs GTT23 32% | §4.2.2, Fig. 6 |
| 合成数据集 base rate 失真 | 中位域名频率 5×10⁻⁴ vs 1×10⁻² / 4×10⁻³ | §4.2.4, Fig. 6 |
| 真实流量类内方差更高 | CV 在几乎所有百分位高于两合成数据集 | §4.2.3, Fig. 6 |
| 规模大一个数量级 | 1.4×10⁷ vs AWF CW900 2.3×10⁶ | §4.1, Table 2 |
| 合成数据集四类系统性缺陷 | 仅 web / 简化用户模型与静态工具 / 只取热门页 / 无知情 base rate | §4.1、Appendix B |
| 测量安全与合规 | IRB 非人类受试；TRSB "No Objections"；受控发布 | §2.3、Appendix A.1/A.5 |
| 采样提供合理否认 | 高量期 80%/低量期 98% 拒绝率 | §2.2.1、Appendix A.1 |
| 标签不可逆 | H(x)=base64encode(sha256(x‖salt))，salt 销毁 | §2.2.2, Eq. 1、Appendix A.1 |
| 下游验证趋势 | Retracer / CellShift：真实设置下 WF 准确率远低于合成数据的暗示；Deng et al.：Var-CNN > DF | §5 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-PAM-A_Measurement_of_Genuine_Tor_Traces_for_Realistic_Website_Fingerprinting.pdf
- MinerU Markdown：02-parsed-markdown/2026-PAM-A_Measurement_of_Genuine_Tor_Traces_for_Realistic_Website_Fingerprinting.md

---

## 12. 后续问题

- GTT23 的申请流程与使用条款细节（TRSB 受控发布）解析稿未给出入口，需查 ref [27] 的 Zenodo 页面。
- 论文为 PAM 2026 会议论文的 full version；会议版与本文（含 Appendix A/Table 1/Listing 1）的差异未逐一核对。
- 出口侧与客户端侧的差异修正由 CellShift/Retracer 系列完成，本笔记未展开其量化结论，待对应笔记（[[2026-NDSS-CELLSHIFT__RTT-Aware_Trace_Transduction_for_Real-World_Website_Fingerprinting]]）交叉阅读。
- "非同质 base rate 下的 precision/FPR 评测协议"是否有现成标准（如 Wang 2020 高精度开放世界论文）值得单独整理为方法页。
- 可否用 GTT23 的统计特征（幂律参数、CV 分布）作为合成数据集生成的校准目标——作者未做，是可研究的空白。

---

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

WF 研究长期依赖合成数据，而合成数据已被反复批评为不真实——这是一个"证据基础本身不可信"的张力。作者用 28 个数据集的系统综述把这一张力坐实为四类系统性缺陷，随后指出唯一的真实数据尝试（Cherubin et al.）因全在线设计而不可复现，形成"有需求、有先例、但无可用资产"的转折点。本文用一条经 IRB/TRSB 审核的出口中继测量方法补齐该资产：GTT23。最后用与两个最新合成数据集的统计对照（长度、方差、base rate）把"合成数据失真"从定性指控升级为定量证据，落点在"未来 WF 评估必须建立在真实踪迹之上"。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 提出"首个真实 Tor 踪迹数据集"的定位与三大卖点（更真实、大一个数量级、可复现） | 价值宣言 | "larger than any existing WF dataset by at least an order of magnitude" |
| Introduction | 建立"WF 需要带标数据 → 标签只在出口侧可得 → 学术界却全用合成数据"的落差 | 张力铺设 | 指出唯一真实数据工作不可复现 |
| Methodology | 把采集方案写成"可被伦理审查通过的工程流程" | 可信度构建 | FPDN 打标机制 + 采样合理否认 |
| Measurement and Analysis | 用描述统计建立数据的"质感"（短、长尾、高方差） | 事实奠基 | 中位 25 cell 的意外发现 |
| Evaluation | 28 数据集综述 + 与 BigEnough/GoodEnough 逐域对照 | 证伪合成数据 | 70% vs 32%、5×10⁻⁴ vs 1×10⁻² |
| Appendix A（Ethics） | 前置消解"做这种测量是否合规"的质疑 | 防御性论证 | TRSB "No Objections" + 受控发布 |
| Conclusion and Future Work | 承认标签不可逆的代价并把它转成自监督预训练的机会 | 收束与延伸 | "测试比训练更重要"的论断 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 评估不足 | 27/28 数据集为合成，无法支撑真实世界结论 | 系统性综述 + 四类缺陷归纳 | §1、§4.1、Table 3 |
| 矛盾证据 | 合成数据导致 base rate fallacy 等 ML 评估陷阱 | 引既有批评 + 自己的量化对照 | §1、§4.2.4 |
| 场景缺失 | 真实用户的非 web 行为、长尾域名、自然访问频率缺席 | 与 2018 年隐私保护测量（>20% 流不在 Alexa Top 1M）互证 | §4.2.1 |
| 可复现性缺陷 | Cherubin et al. 全在线、不落盘 | 单点批评 + 后继工作仍用合成数据的事实 | §1、§2.1 |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 数据画像（Fig. 1–5） | 建立"真实流量长什么样"的基线认知（短、长尾、高方差） | 为后续"合成数据不像它"提供参照系 |
| 数据集综述（Table 2/3） | 横向证伪：缺陷是全生态的、不是个别数据集的问题 | 把个案批评升级为领域级论断 |
| 对照实验（Fig. 6） | 纵向证伪：即使最先进的合成数据集（BigEnough/GoodEnough）也在三个核心特征上失真 | 直接支撑结论"GTT23 更真实" |
| 外部证据旁引 | 引用 Retracer/CellShift 的下游结果说明真实数据已改变领域结论 | 证明数据集的实际影响力 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 先立"WF 危险且需要带标数据"，再一击指出"几乎所有先前工作都用合成数据" | 用"领域共同前提 + 一个被忽视的事实"开场，制造落差 |
| Gap 提出方式 | 不靠单点批评，而用 28 个数据集的系统综述量化缺陷 | 把 gap 做成"清单式证据表"，让审稿人难以反驳 |
| 方法论证逻辑 | 安全/伦理不是附录装饰，而是方法论的一部分（采样率、salt 销毁、受控发布都被写成设计要点） | 敏感数据类工作应把伦理设计提升为方法贡献 |
| 实验组织逻辑 | 先自证（数据画像）→ 再横向证伪（综述）→ 再纵向证伪（对照） | "自证—横向—纵向"三段式评估结构 |
| 局限性讨论方式 | 主动承认标签不可逆，并立刻给出"自监督预训练"的补救路径 | 局限 + 一份可执行的对策，而非只罗列缺点 |
| 最值得借鉴的一句话/一段结构 | "It represents real Tor user behavior…larger…by at least an order of magnitude"——把贡献压成可核验的三段式宣言 | 数据集类论文的一句话定位模板：真实性 + 规模 + 可复现性 |

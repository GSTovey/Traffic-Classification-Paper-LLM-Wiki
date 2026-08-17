---
type: paper
title_original: "FP-Rainbow: Fingerprint-Based Browser Configuration Identification"
title_cn: "FP-Rainbow: 基于指纹的浏览器配置识别"
authors: ["Maxime Huyghe", "Walter Rudametkin", "Clément Quinton"]
year: 2025
venue: "WWW 2025"
doi: "10.1145/3696410.3714699"
url: "https://doi.org/10.1145/3696410.3714699"
pdf: "00-inbox/Aug_inbox/2025-WWW-FP-Rainbow__Fingerprint-Based_Browser_Configuration_Identification.pdf"
mineru_md: "02-parsed-markdown/2025-WWW-FP-Rainbow__Fingerprint-Based_Browser_Configuration_Identification.md"
status: processed
reading_level: L3
research_area: ["web privacy", "browser fingerprinting", "online tracking", "configuration space exploration", "BOM enumeration"]
task: ["browser configuration identification", "browser fingerprint analysis"]
method: ["BOM enumeration", "JavaScript Template Attacks", "attribute stability metric", "subset comparison", "differential fingerprint analysis"]
dataset: ["self-collected browser fingerprint dataset (61,559 fingerprints, 18 Chromium versions × headless/headful × 1,748 switches)"]
code: unknown
relevance: medium
created: "2026-08-17"
updated: "2026-08-17"
---

# FP-Rainbow: Fingerprint-Based Browser Configuration Identification

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | FP-Rainbow: Fingerprint-Based Browser Configuration Identification |
| 中文标题 | FP-Rainbow: 基于指纹的浏览器配置识别 |
| 作者 | Maxime Huyghe（Univ. Lille / CNRS / Inria / CRIStAL）、Walter Rudametkin（Univ. Rennes / IRISA / IUF）、Clément Quinton（Univ. Lille / CNRS / Inria / CRIStAL，通讯） |
| 年份 | 2025 |
| 会议/期刊 | WWW 2025（ACM Web Conference 2025，2025-04-28~05-02，澳大利亚悉尼），11 页 |
| 研究方向 | Web 隐私、浏览器指纹、在线跟踪、浏览器配置空间探索 |
| 任务类型 | 从浏览器指纹中（重新）识别浏览器启用的配置参数（开关 switch） |
| 方法关键词 | BOM 枚举（FingerprintJS + JavaScript Template Attacks）、差分指纹分析、属性稳定性度量 ω_a、受影响属性子集比对 |
| 数据集 | 自建浏览器指纹数据集：1,748 个开关 × 18 个 Chromium 版本 × Headless/Headful 双模式，共 61,559 个指纹（每个指纹 12,334~16,473 个属性） |
| 是否开源 | 论文未提及代码仓库（unknown）；实验数据公开可获取 |
| PDF | 00-inbox/Aug_inbox/2025-WWW-FP-Rainbow__Fingerprint-Based_Browser_Configuration_Identification.pdf |
| MinerU Markdown | 02-parsed-markdown/2025-WWW-FP-Rainbow__Fingerprint-Based_Browser_Configuration_Identification.md |

---

## 1. 一句话总结

>

本文提出 FP-Rainbow，通过系统性地枚举 Chromium 浏览器的 1,748 个配置开关对 BOM（浏览器对象模型）的差分影响，构建属性稳定性知识库，从而能从未知指纹中以平均 84.36%（单开关）/ 78.15%（多开关）的准确率反推出浏览器启用的配置参数。

---

## 2. 摘要翻译

### 2.1 摘要原文

> Browser fingerprinting is a tracking technique that collects attributes and calls functions from the browser's APIs. Unlike cookies, browser fingerprints are difficult to evade or delete, raising significant privacy concerns for users as they can be used to re-identify individuals over browsing sessions without their consent. Yet, there has been limited research on the impact of browser configuration settings on these fingerprints.
>
> This paper introduces FP-Rainbow, a novel approach to systematically explore and map the configuration space of Chromium based web browsers aiming to identify the impact of configuration parameters on browser fingerprints and their changes over time. We explore 1,748 configuration parameters (switches) and identify their impact on the browser's BOM (Browser Object Model). By collecting and analyzing over 61,000 fingerprints from 18 versions of Chromium, our study reveals that 32 to 56 of these configuration parameters (depending on versions), such as disable-3d-apis or disable-notifications, influence the fingerprint of a web browser.
>
> FP-Rainbow also proves efficient in identifying browser configuration parameters from unknown fingerprints, achieving an average successful identification rate of 84% when considering a single configuration parameter and 78% when multiple parameters are involved, across all evaluated browser versions. These findings emphasize the importance of measuring the impact of configuration parameters on browsers to develop safer and more privacy-friendly web browsers.

### 2.2 摘要中文翻译

> 浏览器指纹是一种从浏览器 API 收集属性并调用函数的跟踪技术。与 Cookie 不同，浏览器指纹难以规避或删除，对用户构成显著的隐私担忧——它们可在未经用户同意的情况下跨浏览会话重新识别个体。然而，目前关于浏览器配置设置对这些指纹影响的研究十分有限。
>
> 本文提出 FP-Rainbow，一种系统性地探索和映射 Chromium 系浏览器配置空间的新方法，旨在识别配置参数对浏览器指纹的影响及其随时间的变化。我们探索了 1,748 个配置参数（开关），并识别它们对浏览器 BOM（浏览器对象模型）的影响。通过收集和分析来自 18 个 Chromium 版本的 61,000 余个指纹，我们的研究揭示其中 32 到 56 个配置参数（视版本而定），如 disable-3d-apis 或 disable-notifications，会影响浏览器指纹。
>
> FP-Rainbow 还证明了从未知指纹识别浏览器配置参数的有效性：在所有评估的浏览器版本上，仅考虑单个配置参数时平均识别成功率为 84%，涉及多个参数时为 78%。这些发现强调了测量配置参数对浏览器影响的重要性，以便开发更安全、更注重隐私的浏览器。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 浏览器指纹是难以规避/删除的跟踪手段，已有多项研究（Acar et al., Englehardt et al.）证明其被广泛用于跨站用户重识别。
- 但**几乎没有工作系统研究"浏览器配置设置"对指纹的影响**：浏览器从 `window` 对象出发可枚举出 1.2 万~1.6 万个暴露的属性/对象/方法（远超传统指纹算法使用的几十个属性），配置开关（如禁用某 API）会以副作用形式改变 BOM，从而泄漏可被利用的信息。
- 这类信息对双方都有价值：开发者可用它复现客户端环境、定位 bug；攻击者可用它识别存在已知安全问题（如不安全/实验性设置）的配置，或提高指纹唯一性以改进跟踪。
- 作者此前工作（SPLC 2024 [13]）虽按配置生成指纹，但未探索配置参数与指纹的对应关系。

### 3.2 现有方法的痛点和不足

| 痛点 | 说明 |
|---|---|
| 传统指纹属性集过小 | 主流指纹算法只用几十个属性（UA、语言、分辨率、时区、插件、canvas、字体、GPU/CPU 等），未覆盖 BOM 暴露的海量属性 |
| 配置副作用被忽视 | 用户个性化配置（占比可观，如欧洲 36% 用户为阻止 Cookie 修改过浏览器设置）会改变 BOM/JS API 暴露面，但无人系统研究这些副作用 |
| 反指纹工具不可持续 | Laperdrix 的随机化、Azad 的伪装测试等反指纹方案会破坏用户体验、可被识别且难以长期维护 |
| 配置空间巨大无法穷举组合 | 1,748 个开关的任意组合在计算上不可行，需要设计"线性逐开关"的数据集构建策略（其可行性依赖开关影响属性之间的低碰撞性） |

### 3.3 论文的研究假设或核心直觉

- **核心直觉**：配置开关对 BOM 的副作用是"可检测的指纹"——大部分开关不影响 BOM，少数（32~56 个）会影响，且每个开关影响的属性集合相对独立（碰撞少），因此可以逐开关线性收集数据、通过属性子集比对反推配置。
- **可验证假设**：用单台设备生成的数据集（switch→受影响属性 的映射）可跨设备用于识别其他环境中的未知指纹（RQ3）。

### 3.4 问题发现路径

> 追溯作者如何从**现象/痛点**一步步转化为**可研究的科学问题**。

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 浏览器从 window 对象出发可枚举出 1.2 万~1.6 万个 BOM 对象/属性/方法，远超指纹算法实际使用的属性数 | §1 |
| 痛点提炼 | 用户配置开关会改变 BOM 暴露面（副作用泄漏），但无人系统测量；反指纹工具无法持续维护 | §1、§2 |
| 问题转化 | 转化为可测量问题：哪些配置参数影响 BOM？如何从指纹反推配置？数据集能否跨设备复用？→ 形式化为 RQ1/RQ2/RQ3 | §4.1 |
| 文献定位 | 配置空间探索在多领域成熟（Linux 内核、JVM、视频编码，Pereira 综述），但从未应用于浏览器指纹场景；浏览器指纹研究聚焦"属性→重识别"，未聚焦"配置→BOM 影响" | §2 |

### 3.5 科学假设形成

> 论文提出了什么**可验证的科学假设**？该假设如何从 3.4 的问题推导而来？

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 少数配置开关（32~56 个）会以低碰撞方式影响 BOM，可据此从未知指纹反推配置 | BOM 枚举规模巨大 + 差分分析直觉（§3.1） | 1,748 开关 × 18 版本 × 双模式全量实验（§5.1） |
| 辅助假设 A | 单设备数据集可跨设备识别未知指纹 | 设备差异只改变少量属性，开关影响的属性子集相对稳定（§3.2 稳定性分析） | 服务器建库 + 笔记本跨设备识别（RQ3，§5.3） |
| 辅助假设 B | 可基于属性稳定性度量（ω_a）选出最小指纹子集 | 属性被越少开关影响越稳定，识别越可靠（§3.2） | 讨论节给出的最小指纹选择方法（§5.4） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | 每个版本 32~56 个开关影响 BOM；单开关平均识别率 84.36% | §5.1、§5.2 |
| 辅助假设 A | 部分支撑 | 跨设备识别率 77.54%，仅比同设备 78.15% 低 0.61 个百分点；但老版本（113/114）存在技术问题未列入 | §5.3 |
| 辅助假设 B | 支撑（方法层面） | 属性稳定性公式 (2)/(3) 用于属性排序与阈值选择 | §5.4 |

---

## 4. 方法设计

### 4.1 方法整体流程

FP-Rainbow 采用三步流程（论文 Figure 1）：

1. **指纹采集**：对每个浏览器版本、每个配置开关（在 Headless 与 Headful 双模式下）各执行一次浏览器，用扩展后的 FingerprintJS + JavaScript Template Attacks 从 `window` 对象出发枚举 BOM 并采集约 1.5 万属性/指纹；每个配置采集两次以剔除不稳定属性。
2. **指纹分析（差分）**：将新指纹 FP_new 与同版本的默认配置参考指纹 FP_ref 逐属性比较，判断每个属性属于"相同/值不同/新增/删除"四类，得到每个开关影响的属性集合（added/changed/removed），并计算属性稳定性 ω_a。
3. **配置识别**：给定未知指纹 FP_unk，只提取"已知被某开关影响的属性子集"与之比对，按 added/changed/removed 三情形计数归一化，判定该开关是否被启用。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1: 指纹采集 | 1,748 个开关 × 18 版本 × Headless/Headful；Puppeteer + Docker | 逐开关启动 Chromium（每线程 1~4 版本并发），浏览器访问自建指纹 Web 服务器，枚举 BOM 采集指纹（JSON + UUID 存库）；每个配置连续采集两次，两次间变化的属性被剔除 | 61,559 个指纹（每指纹 12,334~16,473 属性）；每版本一个默认参考指纹 FP_ref | 构建"开关→指纹"原始数据集 |
| Step 2: 差分分析 | 全部指纹 + FP_ref | 逐属性比较 FP_new 与 FP_ref，判定相同/Changed/Added/Removed；用公式 (2)(3) 计算每个属性的稳定性 | "开关→受影响属性子集"知识库 + 属性稳定性 ω_a | 构建识别所需的映射知识库；评估属性可靠性 |
| Step 3: 配置识别 | 未知指纹 FP_unk + 知识库 | 对每个候选开关，仅取 FP_unk 中该开关 impactedSet 内的属性，按公式 (5) 归一化匹配得分；FingerprintJS 场景用简单差分 | 每个开关的启用判定（匹配/不匹配） | 从指纹反推配置参数 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| BOM 枚举器 | 从 window 对象递归枚举全部对象/属性/方法并取值 | 浏览器页面上下文 | 12,334~16,473 个属性-值对（含 canvas PNG、字符串、数值） | 基于 FingerprintJS + JavaScript Template Attacks（Schwarz et al. 2019）扩展；FP 采集基础 |
| 指纹采集器 | 管理浏览器启动、开关注入、指纹存储 | 开关列表、浏览器版本 | JSON 指纹文件（UUID 标识） | 产出 Step 1 数据集；数据库被所有 Docker 容器共享 |
| 差分分析器 | 比较 FP_new 与 FP_ref，生成受影响集合 | FP_new、FP_ref | impactedSet / impactedSubset | 为识别器提供知识库 |
| 稳定性度量器 | 公式 (2)(3) 计算 ω_a | 各版本受影响统计 | 属性稳定性评分 | 支持最小指纹选择与属性加权 |
| 配置识别器 | 公式 (4)(5) 子集比对判定开关启用状态 | FP_unk + 知识库 | 开关启用判定 | 面向 RQ2/RQ3 的输出模块 |

### 4.4 公式、算法和机制解释

- **受影响判定（公式 1）**：`Impacted_{a_cp,v} = 1` 当且仅当属性 a 在配置 cp、版本 v 下的取值与默认配置不同（0 否则）。Changed/Added/Removed 三种情形统一视为"受影响"。
- **稳定性度量（公式 2、3）**：`Stability_{a,v} = 1 - (Σ_{cp∈CP_v} Impacted_{a_cp,v}) / |CP_v|`，即属性 a 在版本 v 中被越多开关影响越不稳定；跨版本取平均得到 `ω_a = Σ_v Stability_{a,v} / |V|`。ω_a ∈ [0,1]，越接近 1 表示该属性仅被极少开关影响、越稳定可靠。
- **识别得分（公式 4、5）**：对每个候选开关，取其受影响属性子集 impactedSubset_v，对 FP_unk 逐属性判定 Add/Chg/Rm 三类（Add：FP_ref 中无而 impactedSubset 与 FP_unk 中均有；Chg：值在 FP_ref 与 impactedSubset 间不同但在 impactedSubset 与 FP_unk 间相同；Rm：FP_ref 中有但 impactedSubset 与 FP_unk 中均无），三类计数求和后除以子集大小，得 0~1 的匹配得分。
- **Chg 运算符的数据类型适配**：数值用归一化绝对差；字符串用 Levenshtein 距离；PNG 图像（canvas）用逐像素 RGBA 绝对差求和后归一化为数值。
- **多开关场景**：不穷举组合（1,748 个开关的组合不可行），而是按比例随机采样（1/4、1/2、3/4、全部开关各生成若干指纹）评估；可行性依赖于"开关碰撞少、相互独立"的经验观察（§5.1：多数开关影响的属性不重叠，除 length 类属性等少数例外）。

### 4.5 方法优势

- **系统性**：首次对 1,748 个 Chromium 开关 × 18 版本 × 双模式做全量 BOM 影响测量，构建迄今最完整的"配置→BOM 影响"映射。
- **轻量识别**：只比较每个开关的受影响属性子集（远小于整个指纹），避免无关属性污染比对，天然支持多开关与跨环境场景。
- **跨设备可迁移**：单设备数据集即可在异质设备上以相近精度识别（77.54% vs 78.15%），降低数据采集成本（RQ3）。
- **可解释、可落地**：ω_a 稳定性度量可支持"最小指纹"选择，为浏览器开发者提供副作用检查、为隐私工具提供配置识别能力（如检测 bot、识别不安全配置）。

### 4.6 方法不足

- **识别率上限受开关结构限制**：等价开关（disable-3d-apis ≡ disable-webgl，源码确认完全一致）无法区分；子集开关（disable-speech-synthesis-api ⊂ disable-speech-api）只能靠额外子集判定。
- **噪声与不稳定属性**：存在两次采集间不稳定、或被配置参数以外因素影响的属性，会污染识别；需人工逐属性分析或降权。
- **外部效度受限**：数据集仅在 Docker 环境的 Headless/Headful Chromium 上生成，未覆盖真实用户场景的扩展/插件、固件、用户设置等因素（作者列为未来工作）。
- **版本漂移**：Chrome 128~130 版本受影响开关数骤增（53~56 个），识别率反而下降（64%~68%），说明浏览器演进会引入新的副作用，知识库需要持续更新。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

- 传统浏览器指纹研究（Laperdrix、Acar、Englehardt 等）关注"属性→重识别个体"：用少量高熵属性构建唯一标识。
- 反指纹研究（随机化、伪装、扫描器）关注"如何对抗指纹"。
- FP-Rainbow 关注**"配置→BOM 影响"的可逆映射**：方向相反（从指纹反推配置而非个体），且首次把配置空间探索（软件配置工程领域方法论）引入浏览器指纹场景。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 大规模配置×指纹数据集 | 1,748 开关 × 18 版本 × 双模式 = 61,559 指纹（每指纹 1.2 万+属性），公开可获取 | 高 | 是（方法论可迁移到 Firefox/Safari 或其他软件系统） |
| 配置→BOM 影响知识库 | 识别出每版本 32~56 个影响 BOM 的开关，并记录 added/changed/removed 属性明细及版本演化 | 高 | 是 |
| 属性稳定性度量 ω_a | 量化属性跨版本、跨开关的稳定性，支撑最小指纹选择 | 中 | 是（通用度量，可复用于其他指纹场景） |
| 子集比对识别方法 | 只比较受影响子集而非全指纹，支持多开关与跨设备识别 | 中 | 是 |
| 单设备数据集跨设备复用 | RQ3 实验证明单设备建库可迁移使用 | 中 | 是 |

### 5.3 适用场景

- **攻击侧**：识别配置存在已知安全问题的浏览器（如实验性/不安全开关），用于定向攻击面分析；提高指纹唯一性改进跟踪。
- **防御侧**：浏览器开发者检测新功能/开关对 BOM 的副作用，避免引入可被指纹化的暴露面；反指纹/反 bot 工具设计（Headless 与 Headful 的差异可用于 bot 检测）。
- **工程侧**：开发者远程复现用户环境（从指纹反推配置）以定位 bug。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 传统指纹算法（FingerprintJS 等） | 属性少、快、重识别率高 | 只覆盖几十个属性，不感知配置 | 扩展为全 BOM 枚举（1.2 万+ 属性），并用其做配置识别（简单差分即可） |
| JavaScript Template Attacks（Schwarz et al.） | 自动推断主机信息、BOM 枚举 | 未关联配置参数 | 作为 BOM 枚举基础组件，配对 FingerprintJS 与差分分析 |
| 反指纹工具（随机化/伪装） | 降低指纹唯一性 | 破坏体验、可被识别、难维护 | 提供配置副作用测量，可量化哪些开关需要被随机化 |
| 配置空间探索（Linux 内核/JVM/视频编码） | 成熟的采样与预测方法 | 未应用于浏览器指纹 | 首次将配置探索方法论引入浏览器 BOM 影响测量 |
| 作者前作（SPLC 2024） | 按配置生成指纹 | 未探索配置与指纹的对应关系 | 补上"配置→BOM 影响"映射与识别方法 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **硬件**：数据集服务器 2× Intel Xeon Gold 5118 + 188GB RAM，Rocky Linux（内核 4.18）；未知指纹生成笔记本 Intel i7-1185G7 + 64GB RAM，Arch Linux（内核 6.11）。
- **环境**：全部组件 Docker/Docker Compose 容器化（浏览器、数据库、分析工具、Web 服务器各一容器，每容器独立 Puppeteer 实例，共享同一数据库），保证可复现。
- **实验流程**：指纹从数据库取开关配置 → UUID 入库 → 浏览器访问自建指纹服务器采集 → 剔除不稳定属性（连续两次采集的变化属性）→ 超时/崩溃标记（超时每版本 3 次；崩溃 headless 23~144 次/版本、headful 22~38 次/版本）→ 全部配置约 5 小时完成。
- **RQ 结构**：RQ1 开关对 BOM 的影响；RQ2 未知指纹的配置识别（基线单开关 + 多开关）；RQ3 单设备数据集跨设备复用。

### 6.2 数据集

- 18 个 Chromium 版本（Chrome 113.0.5672.63 ~ 130.0.6710.0，覆盖约 18 个月）× Headless/Headful 双模式 = 36 个浏览器实例。
- 共测试 1,748 个开关（平均 headless 成功执行约 1,710 个、headful 约 1,714 个，成功执行的开关随版本存在差异）。
- 61,559 个指纹，每指纹 12,334（HeadlessChrome-113 最小值）~16,473（Chrome-130 最大值）个属性。
- 多开关实验：每版本 31 个指纹（10 个用 1/4 开关、10 个用 1/2、10 个用 3/4、1 个用全部），另含 1,116 个随机采样配置（贡献 3）。
- 数据与来自 Windows/Debian 平台及额外硬件的补充数据公开可获取（论文脚注 7、8，URL 未在解析文本中体现）。

### 6.3 Baseline

- **识别方法双轨**：BOM 枚举指纹（公式 5 子集比对）与 FingerprintJS 指纹（简单差分），二者互为对照，无外部第三方基线（该问题本身无既有方法）。

### 6.4 评价指标

- 识别率（Identified switches 占比，%）；误识别（False Positive）与未识别（False Negative）百分比；受影响属性数（min/max/average）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---|---:|---:|---:|---|
| RQ1 全版本 | 影响 BOM 的开关数 | 32~56（视版本） | — | — | Headful 40~56 个；Headless 32~41 个；影响 FingerprintJS 的为 12~32 个 |
| RQ1 最大影响开关 | 受影响属性数 | disable-3d-apis / disable-webgl / disable-software-rasterizer 各约 2,220~2,269 个属性 | — | — | enable-webgl-image-chromium 最高 2,269 个 |
| RQ1 属性碰撞 | 被多个开关影响的属性 | window._length 被约 22 个开关影响；window.wgl_length 约 8 个 | — | — | 碰撞少是线性建库可行性的前提 |
| RQ2 单开关基线 | 平均识别率 | 84.36% | — | — | 各版本 64.29%~89.36%；128~130 版本因开关数激增识别率降至 64~68% |
| RQ2 多开关（Server） | 平均识别率 | 78.15% | — | — | 31 指纹/版本；错误识别（FP）2.9%~7.8% |
| RQ3 跨设备（Laptop） | 平均识别率 | 77.54% | — | — | 与 Server 78.15% 相差 0.61pp；老版本 113/114 因技术问题未列出 |
| 等价开关 | 识别结果 | disable-3d-apis ≡ disable-webgl | — | — | 源码验证完全一致，无法区分；disable-speech-synthesis-api ⊂ disable-speech-api 为子集关系 |
| 开关-版本覆盖率 | 受影响版本数 | disable-notifications / disable-file-system / disable-remote-playback-api 等 12 个开关在所有 36 个浏览器上均生效 | — | — | 部分开关仅影响特定模式（如 headless 模式专有开关） |

### 6.6 优势最明显的场景

- **单开关识别**：旧版本（Chrome 113~127）单开关识别率达 87.5%~89.4%，接近天花板；受影响属性规模大的开关（如 disable-3d-apis 影响 2,200+ 属性）识别几乎必然成功。
- **跨设备迁移**：大多数版本上笔记本识别率与服务器几乎一致（如 Chrome-120 为 81.8% vs 82.0%），验证了单设备建库的可行性。

### 6.7 局限性

- 新版本（128~130）开关影响面增大导致识别率下降（最低 64.29%），知识库时效性受限。
- 等价/子集开关结构导致部分开关不可区分或需额外推断。
- 属性噪声（两次采集不稳定、非配置因素影响）需人工清理。
- 实验仅在 Docker 内 Chromium 上进行，未覆盖真实用户的插件、扩展、固件、用户设置；仅测 Linux 平台（补充数据含 Windows/Debian 但未纳入本文分析）。

---

## 7. 学习与应用

### 7.1 是否开源？

- **代码**：论文未提及代码仓库（unknown）。
- **数据**：公开可获取（论文脚注 7、8 提供链接；解析文本中未包含脚注 URL，数据含 Windows/Debian 平台与额外硬件的补充采集）。

### 7.2 复现关键步骤

1. 用 Docker Compose 搭建 Chromium（Puppeteer）+ 数据库 + 分析工具 + 自建指纹 Web 服务器四容器环境。
2. 从 peter.sh 博客抓取 Chromium 官方开关清单（1,748 个），逐开关（含默认配置对照）在 Headless/Headful 双模式下启动浏览器，采集 BOM 枚举指纹（FingerprintJS + JavaScript Template Attacks），每个配置采集两次并剔除不稳定属性。
3. 差分分析：FP_new 与 FP_ref 逐属性比对，按相同/Changed/Added/Removed 归类，生成每开关受影响子集，计算 ω_a 稳定性。
4. 对未知指纹，按公式 (5) 对每个候选开关做子集匹配，输出开关启用判定；多开关场景按 1/4、1/2、3/4、全部比例随机采样指纹评估。

### 7.3 关键超参数、预处理和训练细节

- 无模型训练（纯差分/比对方法）；识别判定依赖公式 (5) 的归一化阈值（论文未明确给出具体阈值，标注"未知"待查原文）。
- 预处理：剔除 URL、测试计时、网络类型等测试站点特有属性；双次采集剔除不稳定属性；Chg 比较按类型适配（数值归一化绝对差 / 字符串 Levenshtein / PNG 逐像素绝对差）。
- 资源：全量采集约 5 小时（每线程最多 4 版本并发）；每版本约 1,710~1,714 个开关成功执行，超时每版本约 3 次。
- 识别指纹生成方式：指纹先做稳定性过滤（连续两次采集），再按公式 (5) 与知识库比对。

### 7.4 能否迁移到其他任务？

- **浏览器生态**：方法可迁移到 Firefox、Safari 等（作者明确 FP-Rainbow 可扩展至 flags 等其他配置类型）；可用于反 bot 检测（Headless/Headful 差异）与浏览器开发副作用检测。
- **软件配置工程**：差分采集 + 稳定性度量 + 子集识别 的范式可迁移到任意"配置→可观测输出"映射系统（如物联网设备固件识别、虚拟化环境检测）。
- **流量指纹领域（本知识库语境）**：思想可类比——"少数特征子集承载大部分区分信息"的结论与 WF 中特征选择/最小指纹思路相通，但信号源完全不同（BOM 属性 vs 网络流量），不宜直接套用方法。

### 7.5 对我的研究有什么启发？

- 差分对比 + 稳定性筛选是构造"可解释识别器"的低成本范式：无需训练，先建"变化→原因"映射库，再反向检索。
- 单设备建库、跨设备迁移的实验设计（RQ3）值得借鉴——类似的"训练/采集分布漂移"问题在流量识别（跨网络/跨版本）中同样关键。
- 版本漂移导致识别率下降（128~130）提示：任何指纹类识别方法都需要刻画"知识时效性"，并建立持续更新机制。

---

## 8. 总结

### 8.1 核心思想

> 配置开关的 BOM 副作用即指纹，可反查识别。

### 8.2 速记版 Pipeline

1. 逐开关逐版本采集 BOM 全枚举指纹（双模式、双采集去噪）。
2. 与默认参考指纹差分，构建"开关→受影响属性子集"知识库。
3. 计算属性稳定性 ω_a，筛出可靠属性。
4. 未知指纹仅比对候选开关的受影响子集，归一化打分判定。
5. 验证单设备数据集跨设备可复用（84.36% / 78.15% / 77.54%）。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]] —— 注意：本文属于**浏览器端指纹**（信号源为浏览器 API/BOM 属性），与知识库中流量侧信道 WF（信号源为网络流量）是同一主题下的不同信号源分支，仅概念相关、方法不通用。

（其余概念页如 encrypted-traffic-analysis、traffic-classification 等均为网络流量域，与本文无关，不链接。）

### 9.2 相关方法

- 无合适页面：本库方法页（transformer、graph-neural-network 等）均为流量/深度学习域，本文方法（BOM 枚举、差分比对、稳定性度量）不在允许列表中，不链接。

### 9.3 相关任务

- [[website-fingerprinting]] —— 任务层面相关但信号源不同：本文任务为"从浏览器指纹识别配置参数"，是浏览器指纹任务的逆任务，与流量 WF 任务无直接重叠。

### 9.4 可更新的综述页面

- [[survey-website-fingerprinting]] —— 若综述覆盖浏览器端指纹（而非仅流量 WF），本文可作为"配置指纹"分支的引用材料；否则仅作主题关联。

### 9.5 可加入的对比表

- 无合适页面：[[dataset-comparison-table]] 收录流量数据集，本文为浏览器指纹数据集，不适用；[[open-source-registry]] 为代码资源登记，本文代码状态 unknown，暂不加入。

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 1,748 个开关中仅 32~56 个影响 BOM（视版本与模式） | 摘要；Table 1/Table 2 | §Abstract、§5.1 |
| 数据集规模：61,559 指纹，每指纹 12,334~16,473 属性 | 摘要；贡献 1；Table 1 | §Abstract、§1、§5.1 |
| 单开关平均识别率 84.36%、多开关 78.15%（Server）/ 77.54%（Laptop） | 摘要（84%/78%）；Table 2 | §Abstract、§5.2、§5.3 |
| disable-3d-apis 与 disable-webgl 源码验证为等价开关 | §5.2.1，验证后确认（源码脚注 10） | §5.2 |
| window._length 被约 22 个开关影响、window.wgl_length 约 8 个 | §5.1 | §5.1 |
| 识别采用子集比对而非全指纹比对，避免污染 | §3.3 | §3.3 |
| 跨设备识别率仅下降 0.61pp（77.54% vs 78.15%） | §5.3 | §5.3 |
| Chrome 128~130 开关影响数激增（53/54/56）、识别率降至 64~68% | Table 2 | §5.2、§6.7 |
| 数据公开可获取（含 Windows/Debian 补充数据），代码未提及 | §5 开篇脚注 7、8（URL 未在解析文本中） | §5 |
| 全量采集约 5 小时；每版本超时约 3 次、崩溃 22~144 次 | §4.3.1 | §4.3 |

---

## 11. 原始资料链接

- PDF：00-inbox/Aug_inbox/2025-WWW-FP-Rainbow__Fingerprint-Based_Browser_Configuration_Identification.pdf
- MinerU Markdown：02-parsed-markdown/2025-WWW-FP-Rainbow__Fingerprint-Based_Browser_Configuration_Identification.md

---

## 12. 后续问题

- 公式 (5) 的匹配得分判定阈值是多少？论文未在解析文本中给出明确阈值，需查原文/代码。
- 等价开关（disable-3d-apis / disable-webgl）在真实跟踪场景中如何被利用？作者未展开攻击场景的定量评估。
- "最小指纹"的选择阈值如何与识别率/性能权衡定量关联（§5.4 仅定性）？
- 补充数据（Windows/Debian 平台、其他硬件）与本文 Linux 数据的对比结果是什么？论文未纳入分析。
- 扩展到 flags/用户设置/扩展/插件后的识别率预期如何（作者列为未来工作）？

---

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

> 从"浏览器指纹难以删除、隐私风险显著"的既有共识切入，指出一个被忽视的盲区——用户配置（开关）会以副作用形式改变浏览器暴露的 BOM 属性面，却从未被系统测量。作者以"软件配置工程"的方法论（逐开关差分采集）补上这一空白，构建了大规模"配置→BOM 影响"知识库，并顺势完成叙事反转：不仅"配置影响指纹"可被测量，而且**"指纹反查配置"** 也可行（84.36% 识别率），最终落到"测量配置影响以构建更安全的浏览器"的防御性结论。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 摘要式承诺 | 抛出现象（配置→指纹影响未研究）+ 结果（84%/78% 识别率） | 无 |
| Introduction | 问题搭建 | 从用户个性化设置（36% 改设置）到 BOM 泄漏到攻击价值，给出 4 条贡献 | 把"配置副作用"从开发问题升格为隐私/安全问题 |
| Related Work | 定位空白 | 三线并进：指纹技术/反指纹工具/配置探索（跨领域），指出"配置探索从未应用于浏览器指纹" | 用 Pereira 综述证明方法论成熟、场景空白 |
| Method | 机制展开 | 三步流程 + 稳定性度量 + 子集比对识别 | 公式 (2)(3) 稳定性度量是方法的核心枢纽 |
| Experiments | 证据链 | RQ1 影响测量 → RQ2 单开关/多开关识别 → RQ3 跨设备迁移 | Chrome 128~130 识别率下降作为诚实的版本漂移证据 |
| Discussion | 延伸与自我批判 | 最小指纹方法 + 等价/子集开关 + 局限 | 识别率上限由开关结构决定而非方法缺陷 |
| Conclusion | 收束 | 影响攻击面 → 用户与开发者都应关注 → 未来扩展 | 无 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 场景缺失 | 配置空间探索在 Linux 内核/JVM/视频编码等领域成熟，却无人应用于浏览器指纹 | 文献对比（Pereira 综述 + 多领域例证） | §2 |
| 评估不足 | 现有指纹研究只覆盖几十个属性，未覆盖 BOM 暴露的 1.2 万+ 属性及配置影响 | 直接测量数据（BOM 枚举规模） | §1、§3.1 |
| 性能瓶颈 | 反指纹工具可被识别、难维护、破坏体验 | 相关工作批评（Azad et al. 检测到伪装工具） | §2 |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 主实验（RQ1 影响测量） | 全量穷举 1,748 开关，给出"只有 32~56 个开关起作用"的精确数字 | 证明配置副作用客观存在且可枚举，是知识库的原料 |
| 识别实验（RQ2） | 单开关基线（84.36%）→ 多开关（78.15%），逐步逼近真实场景 | 证明知识库可反向使用，完成叙事反转 |
| 跨设备实验（RQ3） | 换一台笔记本重复多开关实验，仅下降 0.61pp | 证明方法可落地（单设备建库），回应实用性质疑 |
| 案例/细描 | disable-databases 开关的 BOM 变化示例（Appendix Figure 2）、等价/子集开关分析 | 以具体例子增强可信度，同时诚实暴露识别上限 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 从宏观隐私背景（指纹难以删除）快速聚焦到"配置影响未研究"的具体缺口 | 用"大问题→被忽视的小切口"两步收窄 |
| Gap 提出方式 | 跨领域类比（配置探索在别的领域成熟）证明方法论可行性 + 断言本场景无人做过 | "方法论已成熟但场景空白"的论证模板 |
| 方法论证逻辑 | 三步流程对应 RQ 结构，公式少而精（受影响判定 → 稳定性 → 识别得分），每步都有明确输入输出 | 用"测量→建库→反向检索"的对称结构组织方法章 |
| 实验组织逻辑 | RQ1→RQ2→RQ3 层层递进（影响→识别→迁移），每个 RQ 一节，Table 2 一张大表贯穿 | 一张主表承载多 RQ 数据，叙事连续性强 |
| 局限性讨论方式 | 把等价/子集开关等"失败案例"放在结果节正面讨论（诚实展示上限），局限单列 | 主动披露失败模式而非留待审稿人发现 |
| 最值得借鉴的一句话/一段结构 | 贡献 3 的"1,116 个随机采样配置证明单设备数据集可跨设备识别"——用规模数字压缩工作量与结论 | 用"数据集规模 + 关键实验 + 结论"三件套写贡献 |

**MinerU 解析质量问题（本笔记引用时已做修正）**：解析文本存在明显的标记污染——所有章节标题被嵌入 `<sub>`/`<sup>` 标签（如 `Ab<sub>s</sub>t<sub>rac</sub>t`、`I<sub>n</sub>t<sub>ro</sub>d<sub>uc</sub>ti<sub>on</sub>`）；公式 (1)~(5) 大量出现乱码占位符（`��`、`�`、`�������` 等），符号无法还原，本笔记按语义重述公式；Table 2 表头文字被打散（如 "fin er r i n t"），部分单元格数据可能受噪声影响，引用时以 Table 1/Table 3 交叉核对；脚注 7、8 的 URL 缺失。

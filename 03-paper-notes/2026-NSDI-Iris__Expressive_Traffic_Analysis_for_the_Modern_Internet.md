---
type: paper
title_original: "Iris: Expressive Traffic Analysis for the Modern Internet"
title_cn: "Iris：面向现代互联网的高表达力流量分析框架"
authors: [Thea Rossman, Diana Qing, Gerry Wan, Zakir Durumeric]
year: 2026
venue: "USENIX NSDI 2026"
doi: "unknown"
url: "https://www.usenix.org/conference/nsdi26/presentation/rossman"
pdf: "00-inbox/PDFs/2026-NSDI-Iris__Expressive_Traffic_Analysis_for_the_Modern_Internet.pdf"
mineru_md: "02-parsed-markdown/2026-NSDI-Iris__Expressive_Traffic_Analysis_for_the_Modern_Internet.md"
status: deep-analyzed
reading_level: L3
research_area: [encrypted-traffic-analysis, censorship-circumvention]
task: [tunnel-detection]
method: ["Rust subscription compiler", "match-action pipeline", "DPDK zero-copy runtime"]
dataset: ["Stanford campus mirror traffic", "70万标注样本"]
code: "https://github.com/stanford-esrg/iris（Apache 2.0）"
relevance: medium
created: "2026-09-19"
updated: "2026-10-10"
---

# Iris: Expressive Traffic Analysis for the Modern Internet

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Iris: Expressive Traffic Analysis for the Modern Internet |
| 中文标题 | Iris：面向现代互联网的高表达力流量分析框架 |
| 作者 | Thea Rossman, Diana Qing, Gerry Wan, Zakir Durumeric（Stanford University） |
| 年份 | 2026 |
| 会议/期刊 | USENIX NSDI 2026（第 23 届，May 4–6, 2026, Renton, WA；ISBN 978-1-939133-54-0） |
| 研究方向 | encrypted-traffic-analysis / censorship-circumvention（流量分析系统与框架） |
| 任务类型 | tunnel-detection（框架支撑的案例研究，含 OpenVPN 指纹识别、恶意域名解析、视频分辨率推断） |
| 方法关键词 | 编译器式流量分析（Rust 代码生成）、subscription 抽象、match-action pipeline、跨订阅去重、状态机、DPDK 零拷贝 |
| 数据集 | 无公开数据集；案例研究使用斯坦福校园网镜像流量（95–120 Gbps）及前作训练数据（70 万标注样本） |
| 是否开源 | 是，https://github.com/stanford-esrg/iris（Apache 2.0） |
| PDF | 00-inbox/PDFs/2026-NSDI-Iris__Expressive_Traffic_Analysis_for_the_Modern_Internet.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-NSDI-Iris__Expressive_Traffic_Analysis_for_the_Modern_Internet.md |

---

## 1. 一句话总结

> 把流量分析应用编译化：用户在 Rust 中定义 subscription（数据类型/过滤器/回调），Iris 编译器将多个订阅融合去重为单条 match-action 流水线，在 12 核上并发跑数百个订阅并达到 100 Gbps 零丢包。

---

## 2. 摘要翻译

### 2.1 摘要原文

> "In this work, we investigate the needs of modern traffic analysis, and we introduce Iris, a framework for efficiently building complex, high-performance traffic analysis applications. Iris's key contribution is a compiler that transforms user-defined traffic filters, stream transformations, and computation written in Rust into an optimized processing pipeline. The Iris compiler eliminates redundant logic across analysis tasks to generate a unified runtime that minimizes aggregate work, allowing it to scale to hundreds of concurrent workloads. Rather than restricting users to a domain-specific query language, Iris provides a flexible development environment by exposing connection- and application-layer semantics as Rust data types to user-defined functions. We show that Iris can execute hundreds of analysis tasks concurrently at 100 Gbps+ on a single commodity server, and we demonstrate its flexibility through three use cases drawn from prior work."（解析稿 Abstract 原文）

### 2.2 摘要中文翻译

本文研究现代流量分析的实际需求，并提出 Iris——一个用于高效构建复杂、高性能流量分析应用的框架。Iris 的核心贡献是一个**编译器**：它把用户用 Rust 编写的流量过滤器、流（stream）变换与计算，转换为经过优化的处理流水线；编译器跨分析任务**消除冗余逻辑**，生成统一运行时以最小化总工作量，从而支撑数百个并发负载。Iris 不把用户限制在某种领域专用查询语言中，而是把连接层与应用层语义以 Rust 数据类型的形式暴露给用户自定义函数。作者展示了 Iris 可在单台商用服务器上以 100 Gbps+ 并发执行数百个分析任务，并通过三个来自既有工作的用例验证其灵活性。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

被动流量分析是理解互联网行为、安全与性能的主要手段，但现有工具在**表达力与性能之间**存在根本权衡：Zeek 能表达复杂分析（重组的流、应用层会话）但性能不足（已有估计：处理 100 Gbps 流量按完美扩展也需 100+ CPU 核）；高性能框架（Retina 等）只能跑单个订阅或较固定的分析。结果大量研究者直接基于 DPDK 等底层包处理库自建流水线（文献综述中生产网部署的 32 篇里有 65% 如此），重复开发、难以复用。

### 3.2 现有方法的痛点和不足

| 工具 | 优点 | 不足 |
|---|---|---|
| Zeek | 丰富协议解析、连接/流事件、Turing 完备 DSL；输出结构化数据而非仅告警 | 性能受限，100 Gbps 需要上百核（按已有估计） |
| Retina | 单订阅可在商用硬件上跑 100 Gbps+ | 限制为单订阅，无跨任务共享/优化 |
| 直接基于 DPDK 自建流水线 | 性能可控 | 开发成本高、逻辑重复（文献综述中 32 个生产部署有 21 个这么做） |

（§1、§2、§3）

### 3.3 论文的研究假设或核心直觉

核心直觉：**尽管分析任务千差万别，它们对数据的操作高度相似**（同样的连接跟踪、同样的协议解析、同样的过滤前缀）。因此可以把"流量分析"建模为**编译期优化问题**——把每个订阅分解为增量处理块，再在编译期统一与去重，生成一条专用运行时（§1、§4）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 大量研究者不用现成框架，而直接基于 DPDK 等自建连接分析流水线 | §1、§3.1（综述：32 个生产部署中 21 个自建） |
| 痛点提炼 | 表达力与性能的权衡使复杂分析无法在生产网（100 Gbps+）规模上运行 | §1、§3 |
| 问题转化 | 把"如何同时兼得表达力与性能"转化为"如何在编译期跨任务融合与去重" | §4、§5 |
| 文献定位 | 已有框架或限制单订阅（Retina）、或牺牲性能（Zeek）；无系统支持多订阅 100 Gbps+ | §2、§6.2 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 跨订阅的公共逻辑可在编译期融合去重，使运行时开销随订阅数**次线性**增长 | §1、§5 推断 | 多订阅扩展实验（128/256 订阅）与内存表 |
| 辅助假设 1 | 以 Rust 数据类型暴露连接/应用层语义，可同时满足扩展性（R1）与低开发开销（R2） | §3 需求分析 | 三个案例研究的代码行数（161–227 LOC） |
| 辅助假设 2 | 生成式（代码生成）方案不会引入显著额外开销 | §5.2、§6.1 推断 | 与 Retina 的单订阅对比（+5.52–9.89%） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | 128 个 IP 子网订阅仅 8.2% 吞吐损失（对比朴素 Retina 5.41 Gbps）；组合应用 12 核 100 Gbps（<1% 丢包） | §6.2、§6.3 |
| 辅助假设 1 | 支撑 | 三个案例分别 227 / 194 / 161 行代码，均 <250 LOC | §6.3 |
| 辅助假设 2 | 支撑 | 单订阅比 Retina 平均高 5.52–9.89%，两者 6 核零丢包；编译时间主要由 Rust release 优化占据（30 s / debug 2.5 s，Iris 逻辑 <50 ms） | §6.1、§6.5 |

---

## 4. 方法设计

### 4.1 方法整体流程

Iris 把流量分析应用建模为一组 **subscription**：每个 subscription 由三部分组成——**数据类型**（用户用 Rust struct 定义、构建在 Iris 原语之上）、**过滤器**（谓词）、**回调**（用户函数）。框架内部以"每连接协议状态机"为核心 IR：数据类型的构造/更新、过滤与回调都挂在状态与状态转移上；编译器把全部订阅编译为一条统一的 match-action 流水线（§4、§5）。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 定义订阅 | 用户 Rust 代码 | 定义数据类型（构造/更新函数）、过滤器谓词、回调 | 若干 subscription | 声明分析任务 |
| Step 2 构建状态机 | 每个 subscription | 抽取其数据类型/过滤器/回调，翻译为每连接状态机 + 附着的 "action" | 每订阅 IR | 把声明式接口映射到执行模型 |
| Step 3 构建 match-action 流水线 | 每订阅 IR | 对每个连接状态构建 action tree：按过滤前缀分支、叶节点放动作 | 每订阅 action tree | 把过滤与计算组织成匹配结构 |
| Step 4 融合 action tree | 全部订阅的 action tree | 合并为全局按状态的 action tree，统一共享过滤前缀与计算，删冗余节点、且尽可能重排谓词 | 全局 action tree | 跨任务去重（核心优化） |
| Step 5 生成代码 | 全局 action tree | 生成 Rust 源码（专用 match-action 连接处理流水线），交由 Rust 编译器做指令级优化与类型安全 | 可执行运行时 | 落到高性能实现 |
| Step 6 运行 | 镜像流量（95–120 Gbps） | 状态机按包推进、执行动作（一次性动作与流式动作） | 分析结果 | 生产环境运行 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Subscription 接口 | 用户定义数据类型/过滤器/回调 | Rust 代码 | 订阅声明 | 编译器输入 |
| 状态机层 | 每连接按协议推进（如 TCP、HTTP 状态机；每连接可有多个状态机） | 包流 | 状态与状态转移事件 | 挂载数据类型与回调 |
| 原语数据类型（Table 1） | 暴露状态转移作为用户逻辑钩子与基础类型 | 连接状态推进 | 原语（如首包、L4 连接状态等） | 用户自定义类型的构建基块 |
| Match-action 编译器 | 四步编译 + 跨订阅融合去重 | 订阅集合 | Rust 运行时源码 | 框架核心贡献 |
| 运行时 | 执行 action（一次性动作 / 流式动作）、连接跟踪、重组、解析 | 包 | 事件与数据 | 基于 Retina 的低层原语 |
| 低层原语（from Retina） | DPDK 集成、连接跟踪、轻量 TCP 重组、协议解析、NIC 硬件过滤、连接超时 | 原始包 | 高层抽象所需的底层能力 | 被运行时复用 |

**注**：Iris 从 Retina 借用若干通用原语的高性能实现（协议解析器、轻量 TCP 重组、DPDK 集成、NIC 硬件过滤、连接超时机制），这也是其单订阅性能与 Retina 同档的原因（§5.3）。

### 4.4 公式、算法和机制解释

本文为系统论文，无损失函数式；核心机制是编译期优化：

- **状态机 IR**：Iris 为每个连接维护所需的多个协议状态机（如 TCP 与 HTTP）；单个状态机内连接处于至多一个状态且顺序严格，但跨状态机无顺序保证。每个状态转移（含自环）都作为用户逻辑与基础数据类型的钩子（§4.1、Table 1）。
- **Action tree 与 match-action**：每个连接状态的过滤前缀构成分支，动作挂在叶节点；运行时据此决定"是否继续处理该连接、以及如何处理"（§5.1 步骤 2）。
- **跨订阅融合（核心优化）**：合并各订阅的 action tree，统一共享过滤前缀与计算、删冗余节点、尽可能重排谓词；文中以视频分辨率与 DNS 记录两个订阅共享同一过滤前缀为例说明该机制如何显著降低增加订阅的开销（§5.2、Fig.3）。
- **两类动作**：一次性动作（在某个状态转移内调用一次，如 `dns_record`）与流式动作（跨时间步持续执行）（§5.3）。
- **"取消订阅"语义**：回调可在条件满足后不再接收该连接（如 OpenVPN 指纹在收到前 150 个包后即 unsubscribe），使运行时能及时清理长连接状态（§6.3）。

### 4.5 方法优势

- 同时兼得表达力与性能：用户可写任意 Rust 逻辑，同时保持 100 Gbps 级性能。
- **次线性扩展**：订阅数增加时共享逻辑被去重，128 个订阅仅 8.2% 吞吐损失。
- 低开发开销：三个真实案例 161–227 LOC，而原实现（如 traffic refinery）为 5,708 行 Go。
- 通用性：同一框架内可同时运行解析、流式特征、机器学习推断等异构订阅。

### 4.6 方法不足

- 需要 DPDK 兼容 NIC 的商用服务器；移动/端侧或非 DPDK 环境不适用（§6.1、§6）。
- 代码生成带来编译时间：随订阅数量与复杂度增长（release 30 s / debug 2.5 s；主要由 Rust release 优化占据）（§6.5）。
- 内存随连接表增长（长连接跟踪与重组占主导；组合应用 PSS 5.0 GB + DPDK 3.5 GB）（§6.4、Table 2）。
- 需要用户具备 Rust 能力；论文以 R2（开发开销）为目标之一，但未给出与 Zeek DSL 的量化学习成本对比。
- §6.3 自述实现"three use cases"，而组合实验处写 "all four use cases"，存在计数不一致（见 §10）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

- **与 Zeek**：Zeek 提供 DSL 与丰富解析但性能受限；Iris 用 Rust 类型系统替代 DSL，并把优化留给编译器。
- **与 Retina**：Retina 是单订阅且"一个应用一条流水线"；Iris 保留 Retina 的底层原语（并借鉴其实现），但在其上加**跨订阅编译期融合**这一层。
- **与直接基于 DPDK 自建**：Iris 把连接跟踪、重组、解析等公共部分固化为框架原语，用户只写业务逻辑。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 编译式流量分析 | 把订阅集合编译为单条去重后的 match-action 流水线 | 高 | 是（任何多任务流处理系统） |
| Rust 原语化接口 | 连接/应用层语义以 Rust 类型 + 回调暴露，代替 DSL | 高 | 是（框架设计范式） |
| 跨订阅融合 | 统一过滤前缀、去重计算、谓词重排 | 高 | 是（复杂事件处理/查询优化同源） |
| "取消订阅"语义 | 回调可在满足条件后停止接收连接 | 中 | 是（长连接测量的资源管理） |
| 案例驱动需求分析 | 系统化 71 篇论文得出 R1/R2/R3 | 中 | 是（系统论文的需求论证方法） |

### 5.3 适用场景

适合：需要在生产网（100 Gbps 级）长期并发运行多个连接/会话级分析任务的研究与运营团队（安全测量、反审查研究、QoE 监测）；已有 DPDK 测试床的课题组。不适合：无 DPDK 环境的端侧分析、只需离线小规模分析的场景（部署成本不划算）、以及不熟悉 Rust 的团队（虽有 R2 目标但门槛仍在）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| Zeek | 丰富协议解析、结构化输出、成熟生态 | 100 Gbps 需上百核（已有估计）；性能受限 | 编译式去重 + Rust 代码生成 |
| Retina | 单订阅 100 Gbps+；提供可复用原语 | 无多订阅支持 | 跨订阅融合，128 订阅仅 8.2% 损失 |
| 朴素多订阅改造（作者对 Retina 的改造） | 保留核心框架设施 | 每订阅重复过滤与数据构造、动态分发、按 ID 追踪 | 128 订阅时 5.41 Gbps vs Iris 77 Gbps |
| DPDK 自建流水线 | 性能与灵活性完全可控 | 开发成本高（traffic refinery 5,708 行 Go） | 同功能 161 行（视频分辨率案例） |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

测试床：双路 Xeon Gold 6248R（24 核 @3GHz）、384 GB DDR4-2933 ECC、两张 100 GbE Mellanox ConnectX-5；接收斯坦福大学网络镜像流量，在高峰期实验，观测 95–120 Gbps。核心指标为 **ZLT（zero-loss throughput，零丢包吞吐）**：通过逐级降低采样率直到丢包 <1% 来测量（§6.1）。

### 6.2 数据集

无自有数据集。使用：(a) 校园网镜像流量（95–120 Gbps，峰值时段，每次实验运行 1 小时或 5 分钟）；(b) 前作视频分辨率研究的 70 万条标注样本用于训练随机森林（§6.3）；(c) Abuse.ch 恶意域名列表用于 HTTP 订阅实验（§6.2）。

### 6.3 Baseline

- **Retina**：单订阅对比基准（单订阅 100 Gbps+，且 Iris 复用其原语）。
- **朴素多订阅改造的 Retina**：作者修改 Retina 以支持多订阅但**不做根本性重构**，作为"朴素方案"基准；该实现共享包处理/连接管理/重组/协议识别，但每订阅重复过滤与数据构造、用 vector + 动态分发存储不同类型、按标识符追踪订阅（§6.2）。
- **Zeek（间接）**：论文引用 Wan 等对 Zeek/Suricata/Snort 的基准，指出单 TLS 连接订阅下 Retina 每核吞吐是它们的 5–100 倍（§6.1）。

### 6.4 评价指标

ZLT（零丢包吞吐，丢包 <1% 约束下可处理的最大流量）、吞吐下降比例、并发订阅数、峰值内存（PSS + DPDK Mempool）、编译时间、代码行数（LOC）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| 单订阅（TLS 握手 / 连接特征） | 相对吞吐 | Iris 高 5.52–9.89% | Retina | — | 两者均 6 核零丢包；各跑 5 分钟（§6.1） |
| 128 个 IP 子网连接订阅 | 吞吐损失 | 8.2% 损失；77 Gbps | 朴素 Retina 5.41 Gbps | — | 订阅数 8→128（§6.2、Fig.4a） |
| 256 个 HTTP 恶意域名订阅 | 吞吐下降 | 6.3% 下降（仅 2 核） | 朴素 Retina 下降 93.1%，仅 4.5 Gbps | — | Abuse.ch 域名列表（§6.2、Fig.4b） |
| 案例 1：安全实践测量（DeKoven 2019 复刻） | LOC / 吞吐 | 227 行；100+ Gbps（6 核） | 原系统 4–6 Gbps | — | 订阅 HTTP/TLS/QUIC/DNS/匿名五元组（§6.3） |
| 案例 2：OpenVPN 指纹（Xue 2022 复刻） | LOC / ZLT | 194 行；100 Gbps ZLT（6 核） | 原实现采样 1/8 流（20 Gbps）离线分析 | — | 回调在前 150 包后 unsubscribe（§6.3） |
| 案例 3：视频分辨率推断 | LOC / ZLT | 161 行；100 Gbps ZLT（10 核） | 原固定功能工具（traffic refinery 早期版，5,708 行 Go） | — | RF 用 70 万样本训练；推断约 150K cycles，约 300 次/秒（§6.3） |
| 组合应用 | ZLT | 100 Gbps（12 核，<1% 丢包） | — | — | 论文称"all four use cases"（§6.3） |
| 内存占用（Table 2） | 峰值 PSS / DPDK Mempool | 组合 5.0 GB / 3.5 GB | 单案例：3.9/2.2（安全实践）、2.5/1.0（OpenVPN）、3.5/1.5（视频） | — | 连接跟踪与重组占主导；组合时共享数据使内存次线性增长（§6.4） |
| 编译时间 | release / debug | 组合应用 30 s / 2.5 s（Iris 逻辑 <50 ms） | — | — | 时间主要花在 Rust release 优化（§6.5） |

### 6.6 优势最明显的场景

- **多订阅并发**：这是与 Retina/Zeek 差距最大的维度（128 订阅 77 Gbps vs 5.41 Gbps）。
- **长期生产网测量**：1 小时级别的内存与零丢包表现支撑长时运行（Table 2、§6.3）。

### 6.7 局限性

- 依赖 DPDK 与特定 NIC（Mellanox ConnectX-5）；未评估其他硬件。
- 编译时间随订阅规模增长（虽主要来自 Rust 优化）。
- 未在非校园网环境（如运营商级 400 Gbps）验证；实验速率为镜像流量上限 95–120 Gbps。
- §6.3 计数的"three use cases"与组合实验的 "all four use cases" 不一致，需核对原文。

---

## 7. 学习与应用

### 7.1 是否开源？

是。Apache 2.0，https://github.com/stanford-esrg/iris（§1）。

### 7.2 复现关键步骤

1. 准备 DPDK 兼容 NIC 的服务器与镜像流量源（论文用双 Xeon Gold 6248R + 2×100 GbE ConnectX-5）。
2. 用 Iris 的 subscription 接口（Rust）定义数据类型、过滤器与回调；例如复刻 OpenVPN 指纹：对 TCP/UDP 连接生成两类指纹（包长特征、payload 前缀 OpCode），在收到前 150 包后 unsubscribe。
3. 编译：Iris 依次构建每订阅状态机 → 每订阅 action tree → 融合全局 action tree → 生成 Rust 代码。
4. 用 ZLT 方法评估：逐步降低流采样率直到丢包 <1%，记录可处理吞吐。

### 7.3 关键超参数、预处理和训练细节

无模型训练（视频分辨率案例使用前作数据训练随机森林，取 top-10 特征、70 万标注样本）。系统关键参数：每订阅的数据类型/过滤/回调定义、谓词顺序（编译器会尽可能重排）、连接超时机制（来自 Retina 原语）、回调中的 unsubscribe 条件（如 150 包）。

### 7.4 能否迁移到其他任务？

- **编译期融合**思路可迁移到任何"多任务共享前缀过滤/解析"的系统（如 IDS 规则集、可编程交换机多租户）。
- **状态机 + 用户回调**的接口范式可迁移到其他流式分析框架设计。
- **ZLT 评测协议**可直接用于比较流量分析系统的实际可用吞吐。

### 7.5 对我的研究有什么启发？

1. 若研究涉及多个流量分析任务并行（如同时做指纹与异常检测），应把"共享前缀/解析只做一次"作为一等设计目标，而不是各任务各写一份。
2. 论文给出的评估协议（ZLT + PSS/DPDK 内存 + 编译时间 + LOC 开发成本）是系统类工作较完整的评价组合，可作为实验设计的模板。
3. 反审查方向：Iris 的订阅模型使"对同一流量同时跑多种指纹/防御评估"成为常规操作，降低了反审查测量实验的工程成本。

---

## 8. 总结

### 8.1 核心思想

> 把多任务流量分析当作编译期优化问题。

### 8.2 速记版 Pipeline

1. 用户以 Rust 定义 subscription（数据类型 + 过滤器 + 回调）。
2. 编译器为每订阅构建状态机与 action tree。
3. 融合所有 action tree：共享前缀、去重计算、删冗余、重排谓词。
4. 生成 Rust 代码并由 Rust 编译器做底层优化。
5. 运行时在 DPDK + 镜像流量上以 100 Gbps 级执行数百订阅。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[encrypted-traffic-analysis]]
- [[censorship-circumvention]]
- [[tunnel-detection]]
- [[traffic-classification]]

### 9.2 相关方法

- [[pre-training-finetuning]]

### 9.3 相关任务

- [[tunnel-detection]]
- [[encrypted-traffic-detection]]

### 9.4 可更新的综述页面

- [[survey-encrypted-traffic-analysis]]

### 9.5 可加入的对比表

- [[open-source-registry]]
- [[method-comparison-table]]

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 核心贡献是编译器：Rust 过滤/变换/计算 → 优化流水线 | 摘要 | Abstract |
| 文献综述系统化 71 篇论文，导出 R1/R2/R3 需求 | 需求分析 | §3 |
| 71 篇中 32 篇生产部署，其中 65%（21）基于包级开发套件自建；10 篇用 Zeek | 综述统计 | §3.1 |
| 状态机 IR 与 Table 1 原语数据类型 | 接口设计 | §4.1、Table 1 |
| 四步编译：状态机 → match-action → 融合 action tree → 生成 Rust 代码 | 编译流程 | §5.1、Fig.1 |
| 从 Retina 借用解析器、轻量 TCP 重组、DPDK 集成、NIC 硬件过滤、连接超时 | 实现说明 | §5.3 |
| 单订阅比 Retina 高 5.52–9.89%，均 6 核零丢包 | 单订阅对比 | §6.1 |
| 128 个 IP 子网订阅 8.2% 吞吐损失，77 Gbps vs 朴素 Retina 5.41 Gbps | 多订阅扩展 | §6.2、Fig.4a |
| 256 个 HTTP 订阅：Iris 6.3% 下降（2 核），朴素 Retina 下降 93.1%（4.5 Gbps） | 多订阅扩展 | §6.2、Fig.4b |
| 三案例代码量 227 / 194 / 161 行，均达 100 Gbps 级 | 案例研究 | §6.3、Fig.5 |
| 组合应用 12 核 100 Gbps、<1% 丢包 | 组合实验 | §6.3 |
| 内存：组合 PSS 5.0 GB + DPDK 3.5 GB，连接跟踪与重组主导 | 内存评估 | §6.4、Table 2 |
| 编译：release 30 s、debug 2.5 s，Iris 逻辑 <50 ms | 编译时间 | §6.5 |
| 测试床与 ZLT 指标定义 | 评测设置 | §6.1 |
| 开源许可与仓库 | 引言 | §1 |

> ⚠️ MinerU 解析问题：Table 1 以图片形式给出（解析稿仅保留 caption），原语状态转移的具体列表需查 PDF；Fig.4/Fig.5 为图片，扩展曲线数值以正文文字为准。§6.3 自述 "three use cases" 而组合实验处写 "all four use cases"，属论文内部计数不一致（已在 §6.7 标注）。

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-NSDI-Iris__Expressive_Traffic_Analysis_for_the_Modern_Internet.pdf
- MinerU Markdown：02-parsed-markdown/2026-NSDI-Iris__Expressive_Traffic_Analysis_for_the_Modern_Internet.md

---

## 12. 后续问题

- "all four use cases" 中的第四个用例是什么？（§6.3 只详述三个）
- 在 400 Gbps 或非 DPDK 加速环境下，编译期融合的收益是否保持？（论文未测）
- 谓词重排的搜索策略与最坏情况开销？（§5.1 提到"尽可能重排"，未给算法细节）
- 与库内 [[2024-USENIX-OpenVPN_is_Open_to_VPN_Fingerprinting]] 的原实现相比，Iris 复刻版在**指纹准确率**上是否一致？（论文只报吞吐，未报准确率对比）
- 能否把 Iris 用于网站指纹/流量分类的**多模型并发在线评测**？（框架能力可行，论文未涉及，属推断）

---

## 13. 写作叙事与故事线分析

Iris 从“复杂分析需要 Zeek 的表达力、生产线速需要 Retina/DPDK 性能”的张力出发，把跨任务公共逻辑提升为编译期融合问题。方法按 subscription、状态机 IR、去重 match-action 管线和零拷贝运行时递进，实验再由单订阅、并发扩展、案例和代码量证明表达力与性能可兼得。可迁移写法是先用真实部署统计证明重复造轮子，再用统一中间表示把多任务共享变成可测量收益。

## 14. 深度分析证据边界与知识层联动建议

- 本次将已有方法、实验、局限和案例证据正式升级为 L3；100 Gbps、订阅数、丢包率和代码量应以 PDF 原图/表核对。
- 可向 `05-methods/` 的流量分析系统与 `06-tasks/traffic-classification.md` 增加 Iris 框架证据；本次未修改共享页面。

---
type: "paper"
title_original: "Toward Unified Network Traffic Monitoring Using SIR"
title_cn: "基于 SIR 的统一网络流量监测"
authors: ["Anthony Dario", "Chris Misa", "Zena M. Ariola"]
year: 2026
venue: "FMANO (SIGCOMM workshop)"
source_version: "第三届 Formal Methods Aided Network Operation（FMANO ’26，SIGCOMM 附属工作坊）。Crossref 容器记录为 SIGCOMM 2026 会议论文集，论文首页引文明确标记工作坊。"
doi: "10.1145/3789240.3822355"
url: "https://doi.org/10.1145/3789240.3822355"
pdf: "00-inbox/PDFs/2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR.pdf"
mineru_md: "02-parsed-markdown/2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR.md"
status: "processed"
reading_level: "L3"
deep_analysis_reviewed: "2026-11-18"
research_area: ["网络遥测", "流式监测", "形式化方法"]
task: ["包流查询编译", "资源估计"]
method: ["SCRA", "KSCRA", "数据流 DAG"]
dataset: ["五个示例查询"]
code: "https://github.com/AnthonyDario/SIR"
relevance: "medium"
created: "2026-11-18"
updated: "2026-11-18"
metadata_source: "Crossref + PDF title page (workshop track)"
source_sha256: "c66450b3789afd0a97acc78b70eb95c6040a58e016940d62c237c9dbd531a987"
internal_citation_count: 0
citation_impact: 0.8
composite_weight: 0.52
citation_count_scope: "verified DOI or normalized complete titles in vault References; lower bound"
citation_count_verified: "2026-11-18"
---

# Toward Unified Network Traffic Monitoring Using SIR

## 0. 论文基础信息

| 项目 | 内容 |
| --- | --- |
| 原文标题 | Toward Unified Network Traffic Monitoring Using SIR |
| 中文标题 | 基于 SIR 的统一网络流量监测 |
| 作者 | Anthony Dario、Chris Misa、Zena M. Ariola |
| 年份 | 2026 |
| 会议/期刊及版本 | 第三届 Formal Methods Aided Network Operation（FMANO ’26，SIGCOMM 附属工作坊）。Crossref 容器记录为 SIGCOMM 2026 会议论文集，论文首页引文明确标记工作坊。 |
| DOI | 10.1145/3789240.3822355 |
| 题录来源 | Crossref + PDF title page (workshop track) |
| 研究方向 | 网络遥测、流式监测、形式化方法 |
| 任务类型 | 包流查询编译、资源估计 |
| 方法关键词 | SCRA、KSCRA、数据流 DAG |
| 数据集 | 五个示例查询 |
| 开源状态 | 作者仓库提供 SIR 参考实现。论文展示查询编译和解释执行的原型。 |
| PDF | [[00-inbox/PDFs/2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR.pdf]] |
| MinerU Markdown | [[02-parsed-markdown/2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR.md]] |

题录核验见 [出版记录](https://doi.org/10.1145/3789240.3822355)。

## 1. 一句话总结

SIR 用具有状态和寄存器的有键自动机 DAG 统一表示模式计算和指标查询，并从中估计资源需求。

## 2. 摘要翻译

### 2.1 摘要原文

见 [[00-inbox/PDFs/2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR.pdf]] 第 1 页 Abstract。

### 2.2 摘要中文翻译

面向不同平台的现有查询语言支持的能力有别，有的擅长计数，有的擅长识别跨包模式。SIR 用流式中间表示连接这些语言。作者建立三个查询语言到 SIR 的编译器，并利用实例解释如何估算实现资源。

## 3. 方法动机

高速监测同时需要包间模式和指标，若语言直接绑定设备，语义覆盖和资源分配都受到限制。统一中间表示可以显式描述计算和状态的代价（§1–3）。

### 3.4 问题发现路径

| 阶段 | 分析 | 出处 |
| --- | --- | --- |
| 现象观察 | 不同查询语言在窗口聚合、状态匹配与嵌套统计上各有强项。 | §1–2 |
| 提炼困难 | 查询语义与平台能力绑在一起，难以从代码行数判断部署成本。 | §2、§5 |
| 转换问题 | 能否在统一语义中表达已有查询，并从状态结构核算资源？ | §3–5 |
| 文献对照 | 以 Sonata、FLM、NetQRE 的代表查询作为前端及对照。 | §4.1–4.3 |

### 3.5 科学假设形成

有限控制状态、寄存器和数据流组合足以表达三种语言的一组代表查询。编译产物会显式暴露节点、转移和寄存器规模，作为异构部署分析输入。

## 4. 方法设计

### 4.1 输入、处理与输出

| 步骤 | 输入 | 处理 | 输出 |
| --- | --- | --- | --- |
| 编译 | Sonata、FLM、NetQRE 查询 | 把窗口、值比较和嵌套查询映射到键控寄存器自动机 | SIR 数据流 DAG |
| 执行 | 包事件流及节点状态 | 每个键维护对应状态和寄存器，通过 DAG 流转输出 | 模式匹配或指标流 |
| 估算资源 | 自动机和连边结构 | 统计节点、状态、寄存器和转移，结合目标平台的对象及键规模推断代价 | 部署决策所需的资源描述 |

### 4.2 机制与条件

符号 cost-register automaton 将匹配状态和定量计算放入同一个模型。KSCRA 在键上独立维护实例，DAG 表达模块之间的数据依赖。各输入流内部有序，跨流的相对到达顺序需要部署层给出语义（§3.1–3.4）。

### 4.3 机制拆解与可检验条件

**逐元素语义。** SCRA 用控制状态 $Q$、寄存器集合 $X$、初始配置 $I$、输出函数 $F$ 和转移集合 $\Delta$ 定义处理。当前元素满足守卫时，应用寄存器赋值并改变控制状态。若抵达允许输出的状态，再对新寄存器值求输出。KSCRA 按键保留各自状态。DAG 边指定数据依赖，输入标签区分上游来源（§3.1–3.3，原 PDF 第 3–4 页）。单个逻辑自动机状态有限，很多并发键仍会增加物理内存。

**三类前端差异。** Sonata 的时间窗由独立的结束标记流触发，窗口输出时重置聚合。FLM 的跨包值比较需要保留相关字段绑定。NetQRE 的嵌套查询可在数据流上把多个子查询输出组合。多输入流只保证各自内部有序，窗口边界和共同前缀必须在实现中有明确语义（§4.1–4.3，PDF 第 4–5 页）。

## 5. 与其他方法对比

Sonata 的示例多使用较多、较简单的节点，NetQRE 偏向较少且复杂的节点，FLM 缺少部分定量查询。比较对象是语义表达与状态规模。

### 5.2 方法对比与可归因性

| 方案或观测层 | 区分点 | 评估条件 |
| --- | --- | --- |
| Sonata | 键控时间窗内的流式聚合 | 关闭标记、每键重置和迟到语义 |
| FLM | 流模式及字段绑定 | 有限状态、绑定值及转移冲突 |
| NetQRE | 嵌套定量查询 | 子查询共享前缀和输出组合 |

## 6. 实验表现与局限性

### 6.1 设置、数据与对照

把三种语言的代表查询编译成 SIR，用参考解释器检查，对五个示例查询统计节点、状态、寄存器和转移资源。

- 基线　Sonata、FLM 和 NetQRE 的原生查询表示与各自可表达的查询。
- 指标　查询表达覆盖、源查询长度、KSCRA 数以及状态、寄存器和转移规模。

### 6.2 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 对照 | 差异 | 原文定位 |
| --- | --- | --- | --- | --- | --- |
| Heavy Hitter 查询 | 自动机数 / 寄存器 | Sonata 6 / 13 | NetQRE 9 / 16 | 依前端和查询而异 | §5 表 1，资源计数 |
| 5 个示例查询 | 编译及资源分析 | 三种语言的代表查询可映射，给出结构资源计数 | 不同源语言的查询表示 | — | §4–5 表 1，见原 PDF 第 6 页 |

### 6.4 关键对照、反例与证据边界

| 证据 | 原文复核结果 | 定位 |
| --- | --- | --- |
| Super Spreader | NetQRE 与 Sonata 分别为 7 与 8 个 KSCRA、33 与 22 个转移。 | PDF 第 6 页表 1 |
| Heavy Hitter | Sonata 6 个 KSCRA、13 个寄存器，NetQRE 9 个 KSCRA、16 个寄存器。 | PDF 第 6 页表 1 |
| 资源解释 | 表 1 统计编译结构。部署还需要测并发键规模、键的有效期和平台状态限制。 | §5–6 |

### 6.7 局限性

平台资源界取决于键数、值域、布局及实际并发流。本论文的计数是静态表达规模，硬件吞吐与上界的紧致程度需实测。MinerU 在正文、公式和表格中产生异常上/下标与替换字符，改用第二种 MinerU 模型复核仍出现类似问题。笔记采用 PDF 文本层和原表定位。

## 7. 学习与应用

### 7.1 开源状态

作者仓库提供 SIR 参考实现。论文展示查询编译和解释执行的原型。

[作者公开仓库或产物](https://github.com/AnthonyDario/SIR)。

### 7.2 复核要点

用作者解释器核对示例的状态和输出，在无害流量的固定输入上确认窗口及多输入顺序语义，再将状态数映射到实际资源预算。

### 7.3 可迁移的研究问题

适合用于表达因果窗口、按键状态和计数器预算。可以把研究原型的流级特征状态与告警逻辑明确到同一语义层。

### 7.4 独立复核与迁移设计

在参考解释器中用同一组普通测量事件检查源语言与 SIR 输出，并覆盖空窗口、跨流交错和迟到。将同一份转换结构映射到目标平台后另测吞吐。与 COSINT 成本对照时，记录窗口关闭、实际数据到达、编码及匹配分别在什么时候发生。

## 8. 总结

统一查询语义并显式计量状态资源。

编译 → 执行 → 估算资源。

## 9. Obsidian 知识链接

- 概念　[[04-concepts/network-telemetry]]。
- 方法　[[05-methods/streaming-telemetry-sketch]]。
- 任务　[[06-tasks/network-traffic-measurement]]。
- 对比与相邻资料　[[method-comparison-table]]。

- 补充对照　[[03-paper-notes/2026-COSINT-北邮时金桥|COSINT 汇报]]。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
| --- | --- | --- |
| 三类查询语言可通过一类中间表示表达部分查询 | 编译器、参考解释器与结构计数 | §4–5，PDF 第 6 页表 1 |

## 11. 原始资料链接

- PDF　[[00-inbox/PDFs/2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR.pdf]]
- MinerU Markdown　[[02-parsed-markdown/2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR.md]]
- MinerU 原始归档　[[01-mineru-output/2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR/full.md]]

- PDF 文本层复核　[[01-mineru-output/2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR/pdf-text-review.md|逐页文本]]

## 12. 后续问题

优先检验 §6.7 的主要限制，按 §7.2 记录数据、观测和指标条件。

## 13. 写作叙事与故事线分析

先说明语言对硬件的绑定为何影响覆盖，再用统一语义展开各前端的代表功能，最后以资源向量比较编译结果。

### 13.2 证据组织与写作借鉴

先把语言差异写成可检查的状态行为，再用每个前端的一个代表机制说明如何统一表达。资源表提供工程比较的输入，部署收益由后续平台实测回答。

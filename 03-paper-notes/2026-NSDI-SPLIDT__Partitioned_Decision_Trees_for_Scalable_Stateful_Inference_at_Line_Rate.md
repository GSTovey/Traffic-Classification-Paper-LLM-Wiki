---
type: paper
title_original: "SPLIDT: Partitioned Decision Trees for Scalable Stateful Inference at Line Rate"
title_cn: "SPLIDT：面向线速可扩展有状态推理的分区决策树"
authors: [Murayyiam Parvez, Annus Zulfiqar, Roman Beltiukov, Shir Landau Feibish, Walter Willinger, Arpit Gupta, Muhammad Shahbaz]
year: 2026
venue: "USENIX NSDI 2026"
doi: unknown
url: "https://www.usenix.org/conference/nsdi26/presentation/parvez"
pdf: "00-inbox/PDFs/2026-NSDI-SPLIDT__Partitioned_Decision_Trees_for_Scalable_Stateful_Inference_at_Line_Rate.pdf"
mineru_md: "02-parsed-markdown/2026-NSDI-SPLIDT__Partitioned_Decision_Trees_for_Scalable_Stateful_Inference_at_Line_Rate.md"
status: deep-analyzed
reading_level: L3
research_area: ["in-network machine learning", "programmable data plane", "stateful traffic inference"]
task: ["network traffic classification", "intrusion detection"]
method: ["partitioned decision trees", "Bayesian design-space exploration", "recirculation-based feature reuse"]
dataset: ["CIC-IoMT2024", "CIC-IoT2023-a", "ISCX-VPN2016", "CampusTraffic", "CIC-IDS2017", "CIC-IDS2018", "UNSW-NB15"]
code: "https://github.com/SpliDT-Decision-Trees/SpliDT-Artifact-NSDI26"
relevance: high
created: "2026-09-29"
updated: "2026-10-10"
---

# THE ADVANCED COMPUTING SYSTEMS ASSOCIATION

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | THE ADVANCED COMPUTING SYSTEMS ASSOCIATION |
| 年份 | 2026 |
| 会议/期刊 | NSDI |
| PDF | [[2026-NSDI-SPLIDT__Partitioned_Decision_Trees_for_Scalable_Stateful_Inference_at_Line_Rate.pdf]] |
| MinerU Markdown | [[2026-NSDI-SPLIDT__Partitioned_Decision_Trees_for_Scalable_Stateful_Inference_at_Line_Rate.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
Machine learning (ML) is increasingly being deployed in programmable data planes (switches and SmartNICs) to enable real-time traffic analysis, security monitoring, and innetwork decision-making. Decision trees (DTs) are particu larly well-suited for these tasks due to their interpretability and compatibility with data-plane architectures, i.e., match action tables (MATs). However, existing in-network DT im plementations are constrained by the need to compute all input features upfront, forcing models to rely on a small, fixed set of features per flow. This significantly limits model accuracy and scalability under stringent hardware resource constraints. We present SPLIDT, a system that rethinks DT deployment in the data plane by enabling partitioned inference over sliding windows of packets. SPLIDT introduces two key innovations: (1) it groups individual subtrees of a DT into partitions and allows each subtree to have its own feature set, and (2) it lever ages an in-band control channel (via recirculation) to reuse data-plane resources (both stateful registers and match keys) across partitions at line rate. These insights allow SPLIDT to scale the number of stateful features a model can use with out exceeding hardware limits. To support this architecture, SPLIDT incorporates a custom training and design-space exploration (DSE) framework that jointly optimizes feature allocation, tree partitioning, and DT model depth. Evaluation across multiple real-world datasets shows that SPLIDT achieves higher accuracy while supporting up to 5 more stateful features than prior approaches (e.g., NetBeacon and Leo). It maintains the same low time-to-detection (TTD) as these systems, while scaling to millions of flows with minimal recirculation overhead ( 0.05%).

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
- 主题线索：encrypted traffic, malicious traffic, anomaly, tor, adversarial, traffic classification。
- 摘要证据：Machine learning (ML) is increasingly being deployed in programmable data planes (switches and SmartNICs) to enable real-time traffic analysis, security monitoring, and innetwork decision-making. Decision trees (DTs) are particu larly well-suited for these tasks due to their interpretability and compatibility with data-plane architectures, i.e., match action tables (MATs). However, existing in-network DT im plementations are constrained by the need to compute all input features upfront, forcing models to rely on a small, fixed set of features per flow. This significantly limits model accuracy and scalability under stringent hardware resource constraints. We present SPLIDT, a system that rethinks DT deployment in the data plane by enabling partitioned inference over sliding windows of packets. SPLIDT introduces two key innovations: (1) it groups individual subtrees of a DT into partitions and allows each subtree to have its own feature set, and (2) it lever ages an in-band control channel (via recirculation) to reuse data-plane resources (both stateful registers and match keys) across partitions at line rate. These insights allow SPLIDT to scale the number of stateful features a model can use with out exceeding hardware limits. To support this architecture, SPLIDT incorporates a custom training and design-space exploration (DSE) framework that jointly optimizes feature allocation, tree partitioning, and DT model depth. Evaluation across multiple real-world datasets shows that SPLIDT achieves higher accuracy while supporting up to 5 more stateful features than prior approaches (e.g., NetBeacon and Leo). It maintains the same low time-to-detection (TTD) as these systems, while scaling to millions of flows with minimal recirculation overhead ( 0.05%).

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


## 深度分析（并行深度分析更新 2026-09-29）

### 方法、实验与证据
SPLIDT以分区决策树将有状态特征推理映射到可编程交换机，使用HyperMapper多目标搜索F1/资源配置；Tofino1实测，支持D1–D7数据集。固定等大小窗口和可信数据中心威胁模型是主要边界，提供artifact实现线索。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。

---

## 8. L3 深度方法分析补充

### 8.1 方法动机与问题定义

现有可编程数据面决策树需要在推理前一次性计算所有输入特征，寄存器和 TCAM 资源因此限制了每流状态特征数；静态 top-k 特征又会牺牲准确率。SPLIDT 的问题是：能否把一棵决策树拆成按包窗口执行的子树，让不同子树使用不同特征，并通过 recirculation 复用同一组硬件状态，从而同时扩大特征覆盖、保持线速和支持百万级流。

### 8.2 方法流程

| 步骤 | 输入 | 处理 | 输出 |
|---|---|---|---|
| 1. 数据窗口化 | 带标签的五元组流量 | 修改 CICFlowMeter，在每个 per-flow 窗口输出中间统计并重置状态 | 多窗口特征样本 |
| 2. 分区训练 | 数据集、树深 D、分区数、每子树特征数 k | 第一分区训练子树；按叶节点到达样本递归训练后续分区 | 分区决策树 |
| 3. 设计空间搜索 | 资源约束与目标 | HyperMapper Bayesian Optimization 联合搜索 D、partition、k、特征分配和可支持流数，过滤 TCAM/recirculation 不可行配置 | Pareto 模型 |
| 4. 规则生成 | 每个子树 | Range Marking 将特征范围编码为非重叠 TCAM 标记，并生成按 subtree ID 匹配的模型规则 | P4/MAT 规则 |
| 5. 线速推理 | 流包与 SID | 当前窗口只收集当前子树需要的特征；分区结束后预测下一 SID，recirculation 清理/复用寄存器 | 最终类别与 TTD |

### 8.3 核心机制与对比

- **分区特征分配**突破每棵树固定 top-k 特征：不同子树可查看不同窗口与不同特征集合，但每个窗口只占用 k 个寄存器。
- **SID 与 recirculation**把交换机 pipeline 变成时间共享机器，复用 match keys 和 stateful registers；recirculation 只在分区转换时触发，而非每个包都触发。
- **定制训练/DSE**把模型准确率、TCAM、寄存器、可支持流数和回流带宽放入同一搜索目标，区别于只做规则压缩的 Leo/NetBeacon。

### 8.4 实验与关键结果

评估在七个真实网络安全/流量数据集 D1–D7 上进行：CIC-IoMT2024、CIC-IoT2023-a、ISCX-VPN2016、CampusTraffic、CIC-IDS2017、CIC-IDS2018、UNSW-NB15；基线为 Leo 和 NetBeacon。测试床是两台 64 核服务器、Wedge 100-32X Tofino1（6.4 Mbit TCAM/12 stages），MoonGen 生成流量；另用 Webserver/Hadoop 两种数据中心负载测回流。

| 结果 | 证据 |
|---|---|
| 端到端 Pareto | 七个数据集均形成比 Leo/NetBeacon 更高的 F1–流数前沿 | §5.2, Fig. 6, Table 3 |
| 特征扩展 | 在 128-bit 寄存器预算中最多支持 30 个不同 32-bit 特征 | §5.2, Fig. 12 |
| 反馈与时延 | recirculation 保持在 100 Gbps resubmission buffer 内；TTD 与两基线相当，D3 F1 比 NetBeacon/Leo 高 9%/16% | §5.2–5.3, Fig. 8/11 |
| 离线搜索 | 所有数据集约 150 次 BO 迭代达到峰值；平均每数据集完整搜索 3.8 小时 | §5.2, Fig. 7, Table 4 |
| 低精度扩展 | 16-bit/8-bit 特征平均准确率下降约 7%/14%，但支持流数可增至 2M/4M，仍优于基线 Pareto | §5.3, Fig. 13 |

### 8.5 局限、复现与证据边界

SPLIDT 假设可信数据中心：交换机安全、包头不被对手伪造、攻击者无硬件访问；固定 per-flow 等大小窗口避免了不等窗口组合的指数搜索，但未证明在所有流量模式下最优。离线 BO 训练成本高，特征位宽降低会损失准确率，recirculation 仍受交换机回流带宽约束。复现需要 Python/Scikit-Learn/TensorFlow、HyperMapper、P4/BF-SDE v9.11、Tofino1、CICFlowMeter 改版、七个数据集和 artifact；官方 artifact 已在 frontmatter 记录。

### 8.6 写作叙事与知识层建议

论文从“固定特征集导致准确率/扩展性冲突”出发，依次给出分区推理、时间复用和 BO 搜索，再用 Pareto、硬件资源、TTD 和位宽消融闭环。可向 `05-methods/` 的 programmable data-plane inference 与 `06-tasks/traffic-classification.md` 增加分区决策树证据；本次未修改共享页面。

## 历史自动入库段落说明

- 本笔记前部的自动入库、摘要级或待核验段落是入库时的历史快照，按规范保留以避免删除原始记录。
- 本次新增的深度分析段落、证据记录和局限说明优先；历史段落中的“待深读/待核验”状态不代表当前分析尚未完成。

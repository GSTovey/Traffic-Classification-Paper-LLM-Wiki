---
type: research-front
question: "在代理封装和观测条件变化下，Tor-over-Proxy 能否稳定实现低误报检测？"
status: diverging
problem_state: under_test
evidence_state: partial
created: "2026-10-22"
last_updated: "2026-10-22"
last_reviewed: "2026-10-22"
related_concepts:
  - "[[tunnel-detection]]"
  - "[[anonymous-traffic-identification]]"
  - "[[encrypted-traffic-analysis]]"
related_methods:
  - "[[factorized-detection]]"
---

# Tor-over-Proxy 低误报检测的可识别条件

## 问题定义

在客户端到代理的外层观测中，区分 Tor-over-Proxy、同代理 Pure Proxy、Direct Tor 和普通背景流量。重点不是单一模型的最高分，而是明确观测点、负类构成、分布变化和低误报工作点后，哪些 Tor 行为仍可识别。

## 现有解释与共同前提

| 解释 | 代表证据 | 共同前提 | 当前状态 |
|---|---|---|---|
| 代理封装后仍保留阶段交互和 burst-response 行为 | [[2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions]]、[[2025-NDSS-The_Discriminative_Power_of_Cross-layer_RTTs_in_Fingerprinting_Proxy_Traffic]] | 观测点能够看到足够长的双向或跨层时序 | 部分支持 |
| 代理或隧道的外层指纹可以支持检测，但不等于内层 Tor 识别 | [[2024-USENIX-Fingerprinting_Obfuscated_Proxy_Traffic_with_Encapsulated_TLS_Handshakes]]、[[2024-TON-Website_Fingerprinting_on_Encrypted_Proxies__A_Flow-Context-Aware_Approach_and_Countermeasures]] | 外层代理特征与内层语义没有被混为一个标签 | 待条件化比较 |
| 低误报性能取决于困难负类和背景组成 | [[2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions]] | Pure Proxy、Direct Tor 和异质背景必须分开评估 | 部分支持 |

## 支持证据与反证

| 方向 | 证据 | 结论边界 |
|---|---|---|
| 支持 | NestTor 在域名/capture 隔离确认集上报告 99.45% macro-F1，在 later 数据上为 88.50% | 支持完整双向流条件下的行为可识别性，不支持单向或任意分段鲁棒性 |
| 支持 | NestTor 的匹配结构实验支持独立 Gate/Inner 对该复合标签的条件分解 | 只支持该任务、表示和树预算条件 |
| 反证/边界 | NestTor 在 512B 重分段下为 71.45%，later 与异质背景的误报也明显不同 | 说明包边界和背景分布会改变可识别性 |
| 相邻证据 | 代理指纹和加密代理网站指纹论文可在外层检测代理或网站行为 | 外层代理可识别不等于内层 Tor 可识别，需统一标签和观测条件后比较 |

## 未解决原因

- 观测条件：完整双向流与单向/早期观测的证据不一致。
- 表示层：阶段行为、跨层 RTT、封装 TLS 和网站行为可能捕获不同层级信号。
- 决策层：平面分类与 `ProxyPresent ∧ TorInside` 的条件分解尚未在统一协议下充分比较。
- 评估层：低误报工作点、背景比例、later、代理留出和重分段常被分开报告，难以直接比较。

## 候选科学问题与可证伪假设

| ID | 候选问题 | 机制假设 | 反证条件 | 当前排序 |
|---|---|---|---|---|
| TOP-Q1 | 代理条件分解是否在包装器留出和固定 FPR 下仍有独立收益？ | 同一表示与模型预算下，Gate/Inner 的条件边界能减少 Pure Proxy 与 Direct Tor 的混淆 | 平面模型在包装器留出和固定 FPR 下稳定不劣，或收益只来自更多参数 | 优先 |
| TOP-Q2 | 包边界变化是否是低误报退化的主要机制？ | 重分段、丢包和延迟会选择性破坏阶段/burst 证据，可靠性状态可解释退化 | 退化与包边界无关，或可靠性变量不能解释跨条件差异 | 次优先 |
| TOP-Q3 | 目标 Pure Proxy 负类是否足以支持代理留出校准？ | 目标负类分数尾部可为内层阈值提供有用的条件化校准 | 校准只改变阈值位置，不能改善未知背景或跨代理排序 | 观察 |

## 统一验证方案

- 数据划分：按域名、capture、代理协议、时间窗口和背景来源分别留出；禁止逐包随机划分。
- 对照组：Flat classifier、Shared multi-task、Independent Gate/Inner、仅外层代理检测、仅内层 Tor 检测。
- 变量：观测方向、包边界、延迟、丢包、代理留出、later 时间窗口、背景构成和目标负类可用性。
- 指标：固定 FPR 下 TPR/Recall、macro-F1、每类 FPR、AUPRC、检测延迟和观察预算。
- 失败判据：若 TOP-Q1 在包装器留出和固定 FPR 下没有独立收益，则放弃“条件分解是必要机制”的表述；若 TOP-Q2 的可靠性变量不能解释退化，则不引入可靠性模块；若 TOP-Q3 只改善已知代理而不改善未知背景，则限定为代理内负类校准。

## 当前决策

当前仅将 TOP-Q1 作为优先验证问题，TOP-Q2 和 TOP-Q3 保持候选状态。上述判断来自本地论文笔记和 NestTor 已登记证据，尚未构成新的实验结论。

## 相关证据账本

- [[claims-index]]：NEST-01–04
- [[contradictions]]：浅层/深度比较和低误报工作点的条件边界
- `09-claims/evidence-ledger.jsonl`：EV-NEST-01–04

## 2026-11-17　2026-COSINT-北邮时金桥 学术报告线索

| 时间 | 新线索 | 方向 | 证据严格度 | 候选问题 |
|---|---|---|---|---|
| 2026-11-17 | [[03-paper-notes/2026-COSINT-北邮时金桥|2026-COSINT-北邮时金桥]]，DHOR 第 18–31 页 | 相邻任务，中性 | 报告展示，原表已定位，完整配置待核 | 局部混淆邻域是否解释同代理 Pure 高分尾部？ |
| 2026-11-17 | 同报告，DHBCorr 第 45、51 页 | 跨点关联，相邻机制 | 报告展示，双侧候选竞争 | 真实匹配与困难负例的相对间距能否作为离线诊断？ |

DHOR 的类别目标、DHBCorr 的双点匹配及单流代理内 Tor 存在性各有对应条件。本次新增线索为 `pending_review`。可在固定表示下比较源阈值与邻域判定，并在相同召回/覆盖率下检验收益。该候选记录供后续研究使用，前沿状态与既有 TOP-Q 决策按原记录保留。


## 2026-11-18　待审核的新增证据链

| 年份 | 论文 | 方向 | 关联及适用条件 | 证据位置 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 2026 | [[03-paper-notes/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection\|HAD]] | 相邻机制 | 良性参考在 FAR 发生变化；汇报的 DHOR 贡献仍需低基率下校准证据 | §VII-C 表 XII，COSINT 第 18–31 页 | EV-20261118-HAD-DRIFT · pending_review |
| 2026 | [[03-paper-notes/2026-S&P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency\|SaTor]] | 观察条件 | 底层路由改变 Tor 的 RTT 分布；仅作为不同链路条件的评估变量 | §5.4/5.7，COSINT 第 46–51 页 | EV-20261118-SAT-RTT · pending_review |
| 2025 | [[03-paper-notes/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC\|Nepco]] | 工程对照 | 要分别记录前缀等待、决策服务时间与完成流数量 | §V-C 表 IV，COSINT 第 49–50 页 | EV-20261118-NEPCO-COST · pending_review |

### 2026-11-18　补充对照的观察口径

[[03-paper-notes/2026-S&P-CenRL__A_Framework_for_Performing_Intelligent_Censorship_Measurements|CenRL]] 的预算相同但候选范围不同，提供难例抽样与固定评估队列应分开的例子。[[03-paper-notes/2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR|SIR]] 的多输入流顺序和窗口标记表明，报告实际检测时延时需给出观测截止、晚到处理及超时弃权的定义。两项研究均为相邻方法，具体对应见 [[03-paper-notes/2026-COSINT-北邮时金桥|COSINT 汇报]] 第 14 节。

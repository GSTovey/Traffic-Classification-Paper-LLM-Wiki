---
type: method
name: factorized-detection
created: "2026-10-21"
updated: "2026-10-21"
---

# 分解式检测（Factorized Detection）

## 1. 定义

当目标标签由多个语义条件联合定义时，分别构建条件判别器，再按任务的逻辑规则组合决策。NestTor 的具体形式是“外层代理存在 AND 代理内部存在 Tor”。这是一种条件监督与决策结构，不要求使用某一种深度网络。

## 2. 输入、处理与输出

| 环节 | 输入 | 处理 | 输出 |
|---|---|---|---|
| 行为表示 | 完整双向 TCP 流的方向、payload 长度、相对 IAT | 62 维全局行为与 37 维相对阶段统计 | 99 维向量 |
| 代理条件 | 四类样本 | ToP + Pure Proxy 对 Ordinary + Direct Tor，独立 HGB | 代理得分 Q |
| 内层条件 | 代理域样本 | ToP 对 Pure Proxy，另一个独立 HGB | 内层 Tor 得分 T |
| 决策组合 | 得分与冻结阈值 | 两项均通过才输出阳性 | ToP / Non-ToP |

两个模型独立训练，不共享参数或联合损失。内层模型的训练域是代理流量；不能将其不加门控地当作适用于所有连接的通用 Tor 检测器。

## 3. 核心机制与适用前提

$$\widehat y(x)=\mathbb I[q(x)\ge\tau_Q]\land\mathbb I[t(x)\ge\tau_T].$$

AND 来自目标语义，而不是随意增加模型级联。Pure Proxy 与 Direct Tor 分别隔离两个条件，因此必须保留为困难负类。逻辑组合本身不保证优于平面分类器；收益需要在同数据、同表示、同模型预算下检验，误差也不能假定独立。

负类校准可用独立目标 Pure Proxy 参考集的经验上分位数选择内层阈值；它不使用目标 ToP 标签，但仍然访问了目标域负类，不能称为完全无目标数据的零样本迁移。

## 4. 现有证据

| 论文 | 对照 | 结果 | 可支持的结论 |
|---|---|---|---|
| [[03-paper-notes/2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions|NestTor (TNSM 2026)]]，TNSM 2026 | 同 99 维、RF、总 400 棵树；独立 Gate/Inner 各 200 棵 | 独立合取 94.12%；平面 86.67%；共享多任务 88.11% | 该 ToP 协议下独立条件边界有贡献，§V-E2、Fig. 6 |
| 同上 | 同表示和 HGB 家族 | 分解 99.45%；Flat HGB 87.64% | 补充同家族结构对照，不冒充等总树数 RF 实验 |

## 5. 优势、局限与工程问题

- 可定位错误来自外层条件还是内层判别，便于校准与分布漂移诊断。
- 对照任务必须与最终复合标签一致；共享门控的内层比较不等于原生端到端比较。
- 门控漏检会直接损失最终召回；包边界或采集环境变化可能改变两个条件得分。
- NestTor 使用完整流。模型推理吞吐和包含 PCAP 解析、特征构建的系统吞吐必须分开报告。
- 可迁移至其他复合标签是方法设计启发，现有证据尚未证明所有嵌套协议、单向流或 UDP/QUIC 场景。

## 6. 知识链接

[[04-concepts/tunnel-detection|tunnel-detection]]、[[anonymous-traffic-identification]]、[[04-concepts/traffic-classification|traffic-classification]]、[[traffic-representation-learning]]、[[representation-vs-shallow]]。

## 7. 审计补充：机制边界与证据状态

### 7.1 成立前提

- 复合标签确实由两个需要分别判断的语义条件构成。
- 困难负类能分别代表“仅有外层代理”和“仅有内层 Tor”的反事实条件。
- 训练、阈值和评估划分不共享会泄漏标签的域名、capture 或环境标识。

### 7.2 失效条件

- 观测不完整、包边界被重分段或背景分布发生变化时，两个条件的分数可能同时失真。
- AND 规则不保证误差独立，也不保证在未知背景上自动达到目标 FPR。
- 目标 Pure Proxy 参考集只能支持条件化负类校准，不能替代未知背景验证。

### 7.3 兼容性与迁移边界

| 机制 | 关系 | 证据 | 未知点 |
|---|---|---|---|
| 阶段行为表示 | 可与条件分解配合 | NestTor §IV、§V | 单向流和 UDP/QUIC 尚未验证 |
| 跨层 RTT 指纹 | 可作为外层代理证据对照 | [[2025-NDSS-The_Discriminative_Power_of_Cross-layer_RTTs_in_Fingerprinting_Proxy_Traffic]] | 是否能稳定支持内层 Tor 判别未知 |
| 封装 TLS 指纹 | 可作为外层代理检测对照 | [[2024-USENIX-Fingerprinting_Obfuscated_Proxy_Traffic_with_Encapsulated_TLS_Handshakes]] | 与 ToP 语义分解的关系未知 |

### 7.4 证据状态

| 结论 | 来源定位 | 证据类型 | 条件 | 状态 |
|---|---|---|---|---|
| 独立 Gate/Inner 在 NestTor 匹配结构下有收益 | §V-E2、Fig. 6 | ablation | 99 维、RF、总 400 棵树、完整双向流 | verified |
| 条件分解可迁移到所有嵌套协议 | 无 | — | 尚无统一跨协议实验 | pending_review |


## 2026-11-18　新论文证据

| 论文或报告 | 关联与适用条件 |
| --- | --- |
| [[03-paper-notes/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection\|HAD]] | 原 IDS 后可接独立分数补判，任务为异常筛查；两特征视角的分区与 NestTor 的复合语义标签分解各有不同前提。 |

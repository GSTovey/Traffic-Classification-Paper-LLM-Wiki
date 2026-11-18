---
type: method
name: streaming-telemetry-sketch
created: "2026-11-18"
updated: "2026-11-18"
---

# 流量遥测的有界摘要

Sketch 把大量事件合并到有限状态中，由后续查询恢复计数、分布特征或协方差结构。表示形式由要估计的对象决定。

| 方法 | 写入时维护的状态 | 查询与输出 | 成立前提和失败条件 |
|---|---|---|---|
| [[2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures|PS-ML]] | 既有多行共享计数器 | 读取多行及原估值，用分桶回归纠正流大小 | 要能读取计数行且源域有真实计数。计数器碰撞饱和会减少可恢复信号。 |
| [[2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks|SEDMS]] | 每设备固定行数的矩阵 sketch | 用谱和稀疏选择输出遥测指标，比较协方差近似后决定更新 | 设备身份和关键协方差方向可观测。工作负载变化可能同时改变相对重要性和下游阈值。 |
| [[2025-NDSS-SketchFeature__High-Quality_Per-Flow_Feature_Extractor_Towards_Security-Aware_Data_Plane|SketchFeature]] | 记录数据包观测的虚拟 sketch | 恢复逐流分布特征并判断解码有效性 | 量化、内存预算和流并发控制误差，最终分类性能需独立测。 |
| [[2026-INFOCOM-MonPlan__Taming_Network_Measurement_with_Accurate_and_Resource-Efficient_Sketch-INT_Co-Design|MonPlan]] | Sketch 与带内遥测协同 | 结合不同测量路径完成流量估计 | 部署条件取决于采集拓扑和遥测预算。 |

[[2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR|SIR]] 用明确的自动机状态、寄存器和 DAG 描述查询资源，可用作状态开销的对照。记账时同时报告写入吞吐、状态大小、读次数、每次查询耗时、后端推理及最终结果覆盖率。

与 [[03-paper-notes/2026-COSINT-北邮时金桥|COSINT 汇报]] 的码长比较时，明确压缩对象。PS-ML 压缩网络计数，SEDMS 压缩历史快照，DHBCorr 压缩表示以缩短后续距离计算。同等内存或位宽下先测表示误差，再测下游性能和完成量。

相关：[[04-concepts/network-telemetry|网络流式遥测]]、[[06-tasks/network-traffic-measurement|网络流量测量]]。

## 2026-11-18　深读证据补充

| 新增论文 | 联动点 | 证据口径与可迁移结论 |
| --- | --- | --- |
| [[03-paper-notes/2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR\|SIR]] | 结构性资源预算 | 当查询由多输入和多键构成时，同时保留逻辑寄存器规模、每键实例状态、队列容量及窗口协同成本。 |

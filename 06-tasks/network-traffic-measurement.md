---
type: task
name: network-traffic-measurement
created: "2026-11-18"
updated: "2026-11-18"
---

# 网络流量测量

在给定观测点、资源上限和时间窗内，从网络事件估计业务量、链路时延、可达性或遥测指标，再供管理或检测使用。首先确定测量单位、真值、观测分母与决策时可以看到的数据。

| 子任务 | 输入 → 输出 | 对照与指标 | 代表工作 |
|---|---|---|---|
| 流大小估计 | 已有数据面计数 → 流包数 | AAE、重流召回、写入和查询代价 | [[2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures|PS-ML]] |
| 遥测指标选择 | 包级指标快照 → 逐设备指标子集 | 固定/动态对照、选择比例、下游质量和吞吐 | [[2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks|SEDMS]] |
| 查询与编译 | 输入事件、规则和窗口 → 指标流 | 语义一致、状态/寄存器、平台实测 | [[2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR|SIR]] |
| 可达性监测 | 主动连通性观测 → 站点阻断及变化 | 同候选和预算的发现曲线，记录漏覆盖 | [[2026-S&P-CenRL__A_Framework_for_Performing_Intelligent_Censorship_Measurements|CenRL]] |
| 匿名网络性能 | 中继/电路与链路观测 → RTT 分布 | 测量与仿真分别报告，按拓扑及路由条件对照 | [[2026-S&P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency|SaTor]] |
| 矩阵恢复 | 部分聚合 OD 快照 → 缺失值、预测、异常时段 | 只对缺失位置计算误差，拓扑及时间留出 | [[2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models|MPA-LLM]] |

流量分析原型还需计入等待前缀、流表内存、拥塞时的完成率和采样漏失。对同一流的多次评分，应从首次可见事件计时。对存在相关性的流和主体，按时间、采集批次及设备汇总误差。资源核查参考 [[04-concepts/network-telemetry|网络流式遥测]] 和 [[05-methods/streaming-telemetry-sketch|流量遥测的有界摘要]]。

## 2026-11-18　深读证据补充

| 新增论文 | 联动点 | 证据口径与可迁移结论 |
| --- | --- | --- |
| [[03-paper-notes/2026-S&P-CenRL__A_Framework_for_Performing_Intelligent_Censorship_Measurements\|CenRL]] | 主动测量 | 比较调度时固定候选池和预算。目标定义包括发现新阻断、持续阻断和解除阻断。 |
| [[03-paper-notes/2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR\|SIR]] | 窗口化流查询 | 在固定测试流上校验输出及窗口时刻后，再核算状态容量、活跃键和实际设备时延。 |
| [[03-paper-notes/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models\|MPA-LLM]] | 缺失矩阵研究 | 插补的随机缺失和预测的连续未来掩码分别报告，与已存在的 ARI-LLM 使用同掩码对照。 |

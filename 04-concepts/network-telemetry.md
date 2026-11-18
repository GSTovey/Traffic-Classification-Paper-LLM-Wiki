---
type: concept
name: network-telemetry
created: "2026-11-18"
updated: "2026-11-18"
---

# 网络流式遥测

遥测从包事件、流状态或设备计数中提取可查询的观测量。工作负载与下游任务共同决定哪些字段需要读取、哪些状态需要保留，以及何时上报。

| 表示单位 | 保留了什么 | 主要误差或代价 | 代表工作 |
|---|---|---|---|
| 包事件与有键状态 | 顺序、匹配状态、窗口内计数 | 关联键的规模、状态生命周期与设备资源 | [[2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR|SIR]] |
| 设备的遥测指标快照 | 指标之间的主要协方差及其变化 | 摘要秩、设备数及指标上报比例 | [[2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks|SEDMS]] |
| 流键及共享计数器 | 流大小及计数行间的分歧 | 哈希碰撞、读放大和查询成本 | [[2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures|PS-ML]] |
| 短包前缀 | 已可见的协议字段和局部包序列 | 包收集、排队、每秒新流与评分覆盖 | [[2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC|Nepco]] |
| 活动站点或中继对 | 可达性及链路 RTT | 测量选点、候选范围和实测外推 | [[2026-S&P-CenRL__A_Framework_for_Performing_Intelligent_Censorship_Measurements|CenRL]]、[[2026-S&P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency|SaTor]] |
| 源目的对×时间 | 聚合业务量与矩阵统计 | 稀疏采样、拓扑差异与标签代理 | [[2026-INFOCOM-ARI-LLM__Autoregressive_Imputation_for_Network_Traffic_Matrix_via_Large_Language_Models|ARI-LLM]]、[[2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models|MPA-LLM]] |

用同一时钟统计首次观测、状态就绪、判定和上报的时间。按包、流、快照、流对和矩阵条目报告吞吐时，分别写清分母和完成量。遥测摘要对原量的近似误差与下游任务的错误应分开验证。

相关页面：[[06-tasks/network-traffic-measurement|网络流量测量任务]]、[[05-methods/streaming-telemetry-sketch|流量遥测的有界摘要]]、[[2025-NDSS-SketchFeature__High-Quality_Per-Flow_Feature_Extractor_Towards_Security-Aware_Data_Plane|SketchFeature]]。

## 2026-11-18　深读证据补充

| 新增论文 | 联动点 | 证据口径与可迁移结论 |
| --- | --- | --- |
| [[03-paper-notes/2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR\|SIR]] | 计数与窗口 | 寄存器计数是静态结构，资源还与活跃键、计时方式和平台有关。跨输入只保证各流内部有序。 |
| [[03-paper-notes/2026-S&P-CenRL__A_Framework_for_Performing_Intelligent_Censorship_Measurements\|CenRL]] | 主动测量预算 | 反馈影响选择哪些网站被观察，应把固定队列的总体估计与主动发现曲线分开。 |
| [[03-paper-notes/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models\|MPA-LLM]] | 聚合矩阵与逐流观察 | OD 时间窗口与单流标签是不同观测单位。按可见比例、模型成本与异常标签来源度量矩阵重构。 |

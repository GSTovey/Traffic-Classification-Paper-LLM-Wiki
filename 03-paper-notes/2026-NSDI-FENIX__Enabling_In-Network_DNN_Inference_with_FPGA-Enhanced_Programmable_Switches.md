---
type: paper
title_original: "FENIX: Enabling In-Network DNN Inference with FPGA-Enhanced Programmable Switches"
title_cn: "FENIX：基于 FPGA 增强可编程交换机的网络内 DNN 推理"
authors: [Xiangyu Gao, Tong Li, Yinchao Zhang, Ziqiang Wang, Xiangsheng Zeng, Su Yao, Ke Xu]
year: 2026
venue: "USENIX NSDI 2026"
doi: unknown
url: "https://www.usenix.org/conference/nsdi26/presentation/gao"
pdf: "00-inbox/PDFs/2026-NSDI-FENIX__Enabling_In-Network_DNN_Inference_with_FPGA-Enhanced_Programmable_Switches.pdf"
mineru_md: "02-parsed-markdown/2026-NSDI-FENIX__Enabling_In-Network_DNN_Inference_with_FPGA-Enhanced_Programmable_Switches.md"
status: deep-analyzed
reading_level: L3
research_area: ["in-network machine learning", "programmable data plane", "traffic analysis"]
task: ["encrypted traffic classification", "malware traffic detection"]
method: ["switch feature extraction", "probabilistic token bucket", "FPGA DNN inference"]
dataset: ["ISCXVPN2016", "USTC-TFC"]
code: unknown
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
| PDF | [[2026-NSDI-FENIX__Enabling_In-Network_DNN_Inference_with_FPGA-Enhanced_Programmable_Switches.pdf]] |
| MinerU Markdown | [[2026-NSDI-FENIX__Enabling_In-Network_DNN_Inference_with_FPGA-Enhanced_Programmable_Switches.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
Machine learning (ML) is increasingly used in network data planes for advanced traffic analysis, but existing solutions (such as FlowLens, N3IC, BoS) still struggle to simultaneously achieve low latency, high throughput, and high accu racy. To address these challenges, we present FENIX, a hybrid in-network ML system that performs feature extraction on programmable switch ASICs and deep neural network inference on FPGAs. FENIX introduces a Data Engine that leverages a probabilistic token bucket algorithm to control the sending rate of feature streams, effectively addressing the throughput gap between programmable switch ASICs and FPGAs. In addition, FENIX designs a Model Engine to enable high-accuracy deep neural network inference in the network, overcoming the difficulty of deploying complex models on resource-constrained switch chips. We implement FENIX on a programmable switch platform that integrates a Tofino ASIC and a ZU19EG FPGA directly, and evaluate it on real-world network traffic datasets. Our results show that FENIX achieves microsecond-level inference latency and multi-terabit throughput with low hardware overhead, and delivers over 90% accuracy on mainstream network traffic classification tasks, outperforming the state of the art.

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
- 主题线索：website fingerprint, encrypted traffic, malicious traffic, anomaly, tor, graph neural, transformer, covert, traffic classification。
- 摘要证据：Machine learning (ML) is increasingly used in network data planes for advanced traffic analysis, but existing solutions (such as FlowLens, N3IC, BoS) still struggle to simultaneously achieve low latency, high throughput, and high accu racy. To address these challenges, we present FENIX, a hybrid in-network ML system that performs feature extraction on programmable switch ASICs and deep neural network inference on FPGAs. FENIX introduces a Data Engine that leverages a probabilistic token bucket algorithm to control the sending rate of feature streams, effectively addressing the throughput gap between programmable switch ASICs and FPGAs. In addition, FENIX designs a Model Engine to enable high-accuracy deep neural network inference in the network, overcoming the difficulty of deploying complex models on resource-constrained switch chips. We implement FENIX on a programmable switch platform that integrates a Tofino ASIC and a ZU19EG FPGA directly, and evaluate it on real-world network traffic datasets. Our results show that FENIX achieves microsecond-level inference latency and multi-terabit throughput with low hardware overhead, and delivers over 90% accuracy on mainstream network traffic classification tasks, outperforming the state of the art.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
Figure 9 presents a photograph of the hardware prototype, with the primary components highlighted as follows: 1 Tofino 2 switch chip [31]: Featuring 20 MAU stages, 200 Mbits of SRAM, and 10.3 Mbits of TCAM per pipeline. We configured this chip to efficiently implement our Data Engine modules while balancing resource utilization across pipeline stages. Multiple 100 Gbps port channels were designed to connect the Tofino chip to the FPGA, enabling high-bandwidth data exchange. ![](images/a2fa7448146753128924bc4ba9b994dbf0195e3114febfd7fb47a5452700d388.jpg) Figure 9: Hardware Platform of FENIX: The FPGA-Enhanced Programmable Switch Implementation. 2 Xilinx ZU19EG FPGA chip [1]: Integrates approximately 80 Mbits of on-chip memory and 1,143,450 logic elements. The FPGA resources were partitioned to accommodate the Model Engine’s Vector I/O Processor and Neural Computing Array, while maintaining timing closure at high clock frequencies. The FPGA is directly connected to the Tofino chip through high-speed port channels, enabling low-latency communication. 3 Control plane CPU: Programmed to manage the Tofino chip, responsible for configuration, monitoring, and prob ability model adjustments. 4 Four front-panel FPGA ports: Designed with con figurable transceivers to operate in either 10G or 25G modes for external communication. The design process required careful signal integrity analysis and impedance matching. 5 BMC module: Customized for hardware status monitor ing and remote management of the platform, including thermal management for high-performance components. Experimental Software. Our development process encompassed multiple hardware and software platforms, requiring the integration of a diverse set of technologies and toolchains. For the Tofino chip, we used SDE version

### 局限与复现
![](images/7d78178aca5115456a1109ecf2a085fe9813612bd2b0f9362cfbd50029a26881.jpg) Figure 7: Mechanism of Buffer Manager.

### 开源与证据等级
- 代码线索：未检测到明确 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


## 深度分析（并行深度分析更新 2026-09-29）

### 方法、实验与证据
FENIX将P4可编程交换机特征提取与FPGA增强推理结合，面向加密流量分类和恶意流量检测。原文评估含9类方案，流级macro-F1报告0.890；需以表格核验其余数据集与吞吐/资源数值。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。

---

## 8. L3 深度方法分析补充

### 8.1 方法动机与问题定义

FENIX 处理的是网络内机器学习的三重约束：交换机 ASIC 能线速处理却难以承载复杂 DNN，FPGA 能运行 CNN/RNN 却与交换机之间存在带宽和同步鸿沟，控制面 CPU 方案又带来毫秒级往返。论文的问题是如何把流/包特征提取留在交换机、把高精度 DNN 推理放到 FPGA，同时保持低时延和高吞吐。

### 8.2 方法流程

| 步骤 | 输入 | 处理 | 输出 |
|---|---|---|---|
| 1. 流跟踪 | 到达包与五元组 | ASIC Flow Tracker 维护流哈希、持续时间和包计数；未分类包先走轻量树 | 流状态/初步决策 |
| 2. 特征控制 | 流特征和全局流量统计 | Data Engine 的概率 token bucket 根据流等待时间、已发送包数、活跃流数和总包率决定是否发送特征 | 受控特征流 |
| 3. 交换机到 FPGA | 特征向量、流标识 | Vector I/O Processor 以高带宽端口传输并缓存流 ID | FPGA 输入队列 |
| 4. DNN 推理 | CNN/RNN 特征向量 | FPGA Neural Computing Array 并行执行定点量化模型 | 分类结果 |
| 5. 回写与转发 | 结果和流 ID | 结果回送 ASIC；Flow Tracker 将分类状态用于后续包转发/检测 | 流/包级标签 |

### 8.3 核心设计与对比

- **Data Engine** 将流跟踪、概率速率控制和缓冲分开，解决 ASIC 线速与 FPGA 可接收速率不匹配；概率 token bucket 不为每个流分配物理队列，而是按时间窗口动态抽样。
- **Model Engine** 将流 ID 缓存、向量 I/O 和 DNN 阵列组合，支持 CNN/RNN 的较高精度模型，避免交换机内二值化或极小树模型带来的准确率损失。
- **硬件分工**是本文与 FlowLens（控制面 CPU）、Leo/NetBeacon（ASIC 决策树）、BoS（ASIC 二值 RNN）及 N3IC（SmartNIC）的本质区别：FENIX 把复杂推理放在 FPGA，同时让 ASIC 继续承担特征提取和线速转发。

### 8.4 实验与关键结果

数据集为 ISCXVPN2016（29,295 训练流/7,328 测试流，7 类）和 USTC-TFC（101,789/25,455 流，12 类）。指标以 FlowLens 的 flow-level macro-F1 和其余方案的 packet-level macro-F1 为主，并报告 Precision/Recall、硬件资源、吞吐可扩展性和推理时延。

| 结果 | 证据 |
|---|---|
| 加密流量 flow-level macro-F1 | FENIX F-CNN 0.890，F-RNN 0.912；FlowLens 0.870 | §7.2, Table 2 |
| USTC-TFC 恶意流量 packet-level macro-F1 | FENIX P-CNN 0.907、P-RNN 0.901；NetBeacon 0.670、Leo 0.741、BoS 0.814、N3IC 0.858 | §7.2, Table 2 |
| ASIC 资源 | SRAM 12.9%、TCAM 4.4%、Bus 3.5%、9 stages | §7.3, Table 3 |
| FPGA 资源 | CNN 总体 LUT/FF/BRAM/DSP 为 38.4%/33.8%/7.1%/8.1%；RNN 为 25.6%/31.2%/6.3%/4.6% | §7.3, Table 4 |
| 推理时延 | FPGA 推理约 1.2 μs；外部传输约 1–3 μs；FlowLens 传输/推理为毫秒级 | §7.5, Fig. 11 |
| 扩展性 | 流量规模扩大到仿真 Tbps 级时，macro-F1 最大约下降 13.2% | §7.4, Fig. 10 |

### 8.5 局限、复现与证据边界

FPGA 模型层参数和特征维度在综合时固定，更新 DNN 通常需要重新综合；当前主要支持常见 CNN/RNN，跨硬件迁移仍需专家集成。高吞吐扩展部分使用重新打包时间戳的合成 trace 和经过测试床校准的模拟器，不能等同于真实 Tbps 线上部署。复现需要 Tofino 2、Xilinx ZU19EG、SDE/FPGA 工具链、ISCXVPN2016/USTC-TFC、定点模型和 token bucket 配置；解析稿中的个别硬件细节和完整代码状态需回看官方 PDF/仓库。

### 8.6 写作叙事与知识层建议

论文按“设备错配→Data Engine/Model Engine 分工→准确率/资源/扩展性/时延验证”组织，适合用硬件瓶颈驱动系统设计。可向 `05-methods/` 的 in-network inference 或 `06-tasks/traffic-classification.md` 记录交换机特征提取与 FPGA 推理路线；本次未修改共享页面。

## 历史自动入库段落说明

- 本笔记前部的自动入库、摘要级或待核验段落是入库时的历史快照，按规范保留以避免删除原始记录。
- 本次新增的深度分析段落、证据记录和局限说明优先；历史段落中的“待深读/待核验”状态不代表当前分析尚未完成。

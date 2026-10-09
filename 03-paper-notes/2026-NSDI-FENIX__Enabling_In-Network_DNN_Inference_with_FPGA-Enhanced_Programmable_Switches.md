---
type: paper
title_original: "THE ADVANCED COMPUTING SYSTEMS ASSOCIATION"
title_cn: ""
authors: []
year: 2026
venue: NSDI
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-NSDI-FENIX__Enabling_In-Network_DNN_Inference_with_FPGA-Enhanced_Programmable_Switches.pdf"
mineru_md: "02-parsed-markdown/2026-NSDI-FENIX__Enabling_In-Network_DNN_Inference_with_FPGA-Enhanced_Programmable_Switches.md"
status: processed
reading_level: L2
research_area: []
task: []
method: []
dataset: []
code: unknown
relevance: medium
created: "2026-09-29"
updated: "2026-09-29"
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

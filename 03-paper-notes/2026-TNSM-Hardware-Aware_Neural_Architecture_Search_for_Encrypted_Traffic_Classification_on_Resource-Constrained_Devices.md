---
type: paper
title_original: "Hardware-Aware Neural Architecture Search for Encrypted Traffic Classification on Resource-Constrained Devices"
title_cn: "面向资源受限设备的加密流量分类硬件感知神经架构搜索"
authors: ["Adel Chehade", "Edoardo Ragusa", "Paolo Gastaldo", "Rodolfo Zunino"]
year: 2026
venue: "IEEE TNSM 2026"
doi: "10.1109/tnsm.2026.3666676"
url: "https://doi.org/10.1109/tnsm.2026.3666676"
pdf: "00-inbox/PDFs/2026-TNSM-Hardware-Aware_Neural_Architecture_Search_for_Encrypted_Traffic_Classification_on_Resource-Constrained_Devices.pdf"
mineru_md: "02-parsed-markdown/2026-TNSM-Hardware-Aware_Neural_Architecture_Search_for_Encrypted_Traffic_Classification_on_Resource-Constrained_Devices.md"
status: processed
reading_level: L2
research_area: ["encrypted-traffic-analysis", "traffic-classification", "resource-constrained IoT/edge devices"]
task: ["encrypted-traffic-detection", "traffic-classification", "app-fingerprinting"]
method: ["convolutional-network", "neural architecture search", "INT8 quantization"]
dataset: ["ISCX VPN-nonVPN", "USTC-TFC2016", "QUIC NetFlow"]
code: "https://github.com/SEAlab-unige/ProtectIT"
relevance: medium
created: "2026-09-19"
updated: "2026-09-19"
---

# Hardware-Aware Neural Architecture Search for Encrypted Traffic Classification on Resource-Constrained Devices

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Hardware-Aware Neural Architecture Search for Encrypted Traffic Classification on Resource-Constrained Devices |
| 中文标题 | 面向资源受限设备的加密流量分类硬件感知神经架构搜索 |
| 作者 | Adel Chehade、Edoardo Ragusa、Paolo Gastaldo、Rodolfo Zunino（热那亚大学 DITEN，SEAlab） |
| 年份 | 2026 |
| 会议/期刊 | IEEE TNSM 2026（IEEE Transactions on Network and Service Management） |
| 研究方向 | 加密流量分类；IoT/边缘端资源受限设备上的硬件感知 NAS |
| 任务类型 | 会话级加密流量分类：VPN/非 VPN 识别、VPN 差分、VPN 类型、非 VPN 类型、流量类别、应用识别（App-ID） |
| 方法关键词 | HW-NAS（进化算法 + 硬件约束）、1D-CNN、header 级预处理消融、会话长度缩减、INT8 量化（PTQ/QAT）、STM32Cube.AI 部署 |
| 数据集 | ISCX VPN-nonVPN（主基准，约 30 GB，11 类）、USTC-TFC2016（约 4 GB，20 类）、QUIC NetFlow（约 120 GB，5 类） |
| 是否开源 | 是：https://github.com/SEAlab-unige/ProtectIT（解析稿写作 "…/ProtectIT Unige"，末尾 "Unige" 为解析噪声，已按 PDF 与仓库名还原） |
| PDF | 00-inbox/PDFs/2026-TNSM-Hardware-Aware_Neural_Architecture_Search_for_Encrypted_Traffic_Classification_on_Resource-Constrained_Devices.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-TNSM-Hardware-Aware_Neural_Architecture_Search_for_Encrypted_Traffic_Classification_on_Resource-Constrained_Devices.md |

---

## 1. 一句话总结

> 用带参数/张量/FLOPs 三重硬约束的进化式 HW-NAS，在 ISCX VPN-nonVPN 上搜出一个仅 88.26K 参数、10.08M FLOPs 的 1D-CNN，精度 96.60% 的同时把参数量与算力相对 SOTA 最多压缩 444×/312×，并能 INT8 量化后跑在 Cortex-M4/M7 上做实时会话级分类。

---

## 2. 摘要翻译

### 2.1 摘要原文

> "This paper presents a hardware-efficient deep neural network (DNN), optimized through hardware-aware neural architecture search (HW-NAS); the DNN supports the classification of session-level encrypted traffic on resource-constrained Internet of Things (IoT) and edge devices. Thanks to HW-NAS, a 1D convolutional neural network (CNN) is tailored on the ISCX VPN-nonVPN dataset to meet strict memory and computational limits while achieving robust performance. The optimized model attains an accuracy of 96.60% with just 88.26K parameters, 10.08M floating-point operations (FLOPs), and a maximum tensor size of 20.12K. Compared to state-of-the-art (SOTA) models, it achieves reductions of up to 444-fold, 312-fold, and 15-fold in these metrics, respectively ... A reduction in the length of sessions of up to 75% yields significant improvements in efficiency, while maintaining high accuracy with only a negligible drop of 1-2%. However, ... improper settings or aggressive reductions can bring about a 7% reduction in overall accuracy. The quantized architecture was deployed on STM32 microcontrollers and evaluated across input sizes ..."

### 2.2 摘要中文翻译

本文提出一个通过硬件感知神经架构搜索（HW-NAS）优化的硬件高效深度神经网络（DNN），用于在资源受限的物联网（IoT）与边缘设备上做会话级加密流量分类。借助 HW-NAS，作者在 ISCX VPN-nonVPN 数据集上定制了一个 1D 卷积神经网络（CNN），在满足严格内存与算力限制的同时保持稳健性能。优化后的模型达到 96.60% 精度，仅需 88.26K 参数、10.08M 浮点运算（FLOPs）与 20.12K 的最大张量尺寸；相比 SOTA 模型，这三项指标最多分别降低 444 倍、312 倍与 15 倍。模型还展现出多任务通用性：在多个 VPN 与流量分类（TC）任务上最高达 99.86%；并泛化到外部基准，在 USTC-TFC 与 QUIC NetFlow 上最高 99.98%。此外，深入的 header 级预处理策略研究确认，模型在广泛配置下（包括隐私要求更严苛的场景）均能保持显著性能。类似地，把会话长度最多缩短 75% 能显著提升效率，而精度只有 1–2% 的轻微下降；但作者也强调谨慎选择预处理与会话长度仍然重要——不当设置或过度缩减会导致整体精度下降多达 7%。量化后的架构部署在 STM32 微控制器上并按输入长度评估，结果确认短会话带来的效率收益可转化为实际可用的低延迟嵌入式推理。

---

## 3. 方法动机

### 3.1 现实问题

- 加密流量已占互联网数据量约 96%（§I，引 [4]），DPI 与端口分类基本失效；同时海量数据若集中到云端处理会带来传输时延、网络负载与额外功耗（§I）。
- 理想方案是在边缘设备上就地做流监控/分类，但 IoT 与边缘平台的内存（Flash/RAM）、算力与功耗预算极其有限，现有高精度 DNN 模型（动辄百万级参数、数百 M FLOPs）无法直接落上去。

### 3.2 已有方法的局限

| 已有路线 | 代表工作 | 局限（本文观点） |
|---|---|---|
| 端口 / DPI | 传统方法 | 加密与混淆流量下失效；DPI 还是资源密集型的 |
| 经典 ML（RF/k-NN/DT） | [26] [31] [32] [33] | 依赖人工特征且需频繁重训；精度上限有限 |
| 会话级 DNN | 1D/2D-CNN [11]、图像化 CNN [34]、CNN+SAE [35]、ICLSTM [24] | 精度高（>98%）但计算开销大；注意力机制进一步增加开销与扩展性问题 |
| 包级 / 混合级 DNN | Deep Packet [6]、CapsNet [23]、CBS [5] | 包级需大数据量与长训练时间；CBS 参数 138.45M，明确只适合离线、无法实时 |
| NAS 用于 ETC | AutoML4ETC [8]、[47] [48] | 未针对 IoT 严格约束设计；[48] 只测了单一输入长度，未考察输入数据变化对效率与性能的影响 |

### 3.3 核心动机

把硬件约束（参数量、峰值中间张量、FLOPs）在**架构搜索阶段**就显式建模（而非事后压缩或手工调参），在会话级加密流量分类这一场景下同时满足"精度可用"与"可部署到 MCU"两个要求。作者称这是首个在严格 IoT 兼容约束下为 TC 设计硬件高效深度网络的工作（§I 贡献点 1）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 观察 | 加密流量占比升至 96%，传统方法失效；边缘设备算力/内存受限 | §I, [4] |
| 缺口 | 现有 ETC 深度模型普遍以精度为唯一目标，参数/FLOPs/张量三项均超标 | §I 贡献点 1；§II 相关工作综述 |
| 假设 | 若在搜索期显式约束三项硬件指标，可找到精度损失可接受、但资源占用低一个数量级的架构 | §III（HW-NAS 形式化）、§IV-B |
| 验证 | 在 ISCX 上按 Nucleo-F401RE 资源上限设定阈值做 100 代进化搜索 | §V-C, Table IV |
| 结论 | 搜出的模型精度 96.60%，三项指标降幅最高 444×/312×/15×，且是唯一同时满足 STM32F7 与 F401RE 约束的会话级模型 | §VI-A/B, Fig. 2 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| H1 | 硬件约束前置于搜索（而非事后压缩）能得到精度-效率更优的折中 | MnasNet [21] / ProxylessNAS [22] / MCUNet [42] 的经验 | 与 session 级 SOTA 在 5 项指标上对比（Fig. 2） |
| H2 | 会话级 1D-CNN 可在严格约束下兼具精度与效率，优于 RNN/Transformer 路线 | 1D-CNN 权值共享与局部连接；RNN 逐步处理开销大，Transformer 内存/算力需求不实际（§IV-C） | HW-NAS 搜索结果 + 多任务/跨数据集评估 |
| H3 | 输入长度与 header 预处理可进一步换取效率，且精度损失可控 | 加密流量的判别信息更多在 header/结构而非 payload | Table IX（24 种预处理）、Table X / Fig. 5（8 种输入长度） |
| H4 | INT8 量化（尤其 QAT）能在 MCU 上保住精度 | 量化是可部署性的必要一步 | Fig. 6（Float32 vs PTQ vs QAT）、§VIII |

**假设验证结果**：H1 成立——本文模型是 Fig. 2 中唯一同时满足 STM32F7 与 F401RE 约束者，且精度仅比最重型 SOTA 低约 2–3 个点；H2 成立——在多任务与跨数据集上均优于多数会话级基线；H3 部分成立——常规策略 784→196 B 只掉 1–2%，但过度 zeroing 的策略（如 Strat. 24）掉 7.51%，UDP padding 可缓解；H4 成立——QAT 在所有输入长度上距 Float32 仅 0.1–0.3%，PTQ 有稳定但适度的精度退化（§VI-A/B、§VII-A/B、§VIII-B）。

---

## 4. 方法设计

### 4.1 整体框架

三阶段流水线（§IV）：(1) **预处理**——会话抽取、清洗（去 MAC、匿名化 IP）、过滤无载荷包、会话归一化到 784 字节、字节值缩放到 [0,1]；(2) **HW-NAS 搜索**——进化算法在带硬件约束的搜索空间中迭代；(3) **模型选择与测试**——挑出验证精度最高的架构，在 6 个分类任务 + 2 个外部数据集 + 2 块 MCU 上做完整评测。

### 4.2 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| 1. 会话抽取 | 原始 pcap | 按（源/目的 IP、端口、协议）切分为双向有序包序列 | 会话（raw bytes） | 定义分类粒度 |
| 2. 数据清洗 | 会话 | 去除数据链路层（含 MAC）信息、匿名化 IP | 清洗后会话 | 防止模型记忆 session 特有特征（防过拟合） |
| 3. 过滤 | 会话 | 丢弃无载荷包（SYN/ACK/FIN 等）与无关 DNS 段 | 有效包序列 | 降噪 |
| 4. 归一化 | 变长会话 | 长截断、短补零，统一到 784 字节（沿用 [11][27]） | 定长 784 B 向量 | 统一模型输入 |
| 5. 缩放 | 字节值 | 每字节归一化到 [0,1] | 模型输入张量 | 训练稳定性 |
| 6. HW-NAS 搜索 | 训练集 / 验证集 | 进化算法：变异生成子代 → 硬件约束检查 → 训练 → 按验证精度选新父代；100 代 × 10 子代 | 最佳架构 | 在资源约束下寻优 |
| 7. 多任务重训 | ISCX 各任务切片 | 用同一架构在 6 个任务上重训（10 次独立运行，报告标准差） | 各任务精度/F1 | 验证通用性 |
| 8. 量化与部署 | 最佳架构 | PTQ / QAT 转 INT8，经 STM32Cube.AI 生成 C 代码，在 F746G/F401RE 上测时延与能耗 | 嵌入式推理指标 | 验证可部署性 |

### 4.3 关键模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 进化搜索器 | 种群式架构搜索：父代经 2 次随机变异（插入块 / 删除块 / 改块内超参）产生子代；不合格者继续变异直到凑够可分子代 | 初始架构 a₀、约束集 H | 每代的 10 个候选架构 | 驱动整个搜索循环（Algorithm 1） |
| 硬件约束检查 | 以 F_Th=120K 参数、R_Th=22K 张量、Flops_Th=11M 为阈值过滤子代 | 候选架构、硬件指标估计 | 通过 / 拒绝 | 约 37.5% 子代被拒（平均需生成 16 个才得 10 个可分子代，§V-C） |
| 深度约束 | 限制块数量上限为 5，防止架构过度复杂 | 候选架构 | 合法架构 | 与约束检查共同约束搜索空间 |
| 1D-CNN 块 | 每个卷积层由 kernel size / filters / padding / stride 定义，后接 BN、ReLU、pooling（max/avg，size 2–3）、dropout（0.1–0.5） | 会话字节序列 | 特征图 | 搜索空间的基本单元；搜索范围：filters 16–140、kernel 3–7、stride 1–6 |
| GAP + Dense | 全局平均池化聚合特征后接全连接 + softmax | 特征图 | 类别概率 | 最终分类头 |
| 量化/部署链 | TensorFlow Lite INT8（PTQ/QAT）→ STM32Cube.AI → C 代码 | Float32 模型 | MCU 可执行模型 | 部署阶段使用；QAT 通过模拟 INT8 算术微调以弥补量化损失 |

### 4.4 目标函数

HW-NAS 的形式化（式 2）：

- 最大化验证精度 `Accuracy_val(w*(a), a)`；
- 约束：`w*(a) = argmin_w L_train(w, a)`、`|P(a)| < F_Th`（参数量 < 120K）、`|T(a)| < R_Th`（峰值张量 < 22K）、`Flops(a) < Flops_Th`（< 11M）。

阈值来源：以 Nucleo-F401RE（512 KB Flash / 96 KB RAM / 84 MHz）为基准，float32 假设下 120K 参数 ≈ 480 KB Flash、22K 张量 ≈ 88 KB RAM；11M FLOPs 基于 84 MHz 时钟理论上界，对应推理上界约 130 ms（不含访存开销），落在边缘分析类任务可容忍的 100–250 ms 区间（§V-C，引 [49]）。

### 4.5 搜索配置

- 100 代 × 每代 10 个可分子代；最多深度 5 块；每个子代由父代经 2 次随机变异得到。
- 验证集为训练数据的 20% 留出；训练最多 100 epoch，初始学习率 1e-3，batch 128，验证损失平台触发降学习率，早停；多起点训练 3 次取最佳验证精度。
- 搜索在 NVIDIA 2080 Ti 上完成，数据预处理用 Scapy，框架为 Keras/TensorFlow。
- 收敛：Fig. 1 显示 G0/G1/G6/G12/G28/G57 出现过新最优，G57 之后不再提升，说明在硬件约束下搜索早收敛。

### 4.6 最终架构

Table V：Conv1D(129 滤波器, k=7, s=5, valid) → Conv1D(110, k=4, s=2, valid) → AvgPool1D(k=3, s=2) → Conv1D(38, k=7, s=2, valid) → MaxPool1D(k=2, s=2) → GAP → Dense(11) + Softmax。滤波器数逐层递减（129→110→38），兼顾特征提取与计算成本；浅层大感受野、深层抓细粒度。总参数 88.26K、最大张量 20.12K、10.08M FLOPs。

> ⚠️ MinerU 解析问题：Table XI 的多行合并单元格被解析为同一单元格内多行文本（如 "31.43 ms (784 B)19.45 ms (484 B)" 挤在一格），引用时需按下标平台对应关系拆分；§I 首段前几句在解析稿中缺失（首个可见句为 "often cannot handle effectively [1]."），Introduction 开头不完整。

---

## 5. 与其他方法对比

### 5.1 与基线/相关工作对比

| 方法 | 输入粒度 | 精度 | 参数量 | 是否可部署到 MCU |
|---|---|---|---|---|
| 本文（Prop.） | Session | 96.60%（F1 96.63%） | 0.09M | ✓✓（F746G + F401RE） |
| [12] CenTime | Session | >99% | 2.06M | × |
| [14] 通道注意力+可变形卷积 | Session | >99% | 1.24M | × |
| [24] ICLSTM | Session | 98.10% | 39.12M | × |
| [11] 1D-CNN | Session | 86.60%（F1） | 5.83M | × |
| [5] CBS | Hybrid | 99.70% | 138.45M | ×（且明确为离线设计） |
| [23] CapsNet | Session-Packets | 99.10% | 6.80M | × |
| [6] Deep Packet | Packets | 98.00%（F1） | 3.55M | × |
| [18] Attention-LSTM | Flows | 91.20% | 1.35M | × |
| [46] NAS 流量模型（USTC） | Flows | 99.99% | 0.07M | 参数量可比，但 FLOPs 19.63M ≈ 本文 1.95 倍 |

（数据来源：§VI-B Fig. 2/Fig. 3 正文描述、Table VI、Table VII；Fig. 中数值无法直接从解析稿读取，仅采用正文明确出现的数字。）

### 5.2 创新点

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 约束前置的 HW-NAS for ETC | 把参数/张量/FLOPs 三阈值写进搜索约束（式 2），在 ISCX 上直接搜硬件友好架构 | 高（作者称首个面向严格 IoT 约束的 TC 硬件高效网络） | 可迁移：同一套约束定义可套用到其他流量分析任务 |
| 系统级 header 预处理消融 | 24 种预处理策略组合（eth 去层、MAC/IP 匿名 vs 置零、端口置零、UDP padding）对同一 NAS 模型做全因子评测 | 高（给出可操作的隐私-精度权衡指南） | 可迁移：任何按字节输入的流量模型都能复用该评测矩阵 |
| 会话长度-效率-精度曲线 | 784→196 B 八档输入下同时报告精度与 FLOPs/张量，并给出"最优工作点"（324/484 B） | 中 | 可迁移 |
| INT8 部署实测 | PTQ vs QAT 对比 + 1000 次推理实测时延/能耗（含 idle/active 功耗分离） | 中（同类工作少有报实测部署数据） | 可迁移：部署测量协议可复用 |

### 5.3 与已有方法的本质差异

- 与 AutoML4ETC [8] 等 NAS for ETC 工作：它们不设严格 IoT 约束；本文将约束阈值对齐到具体 MCU（Nucleo-F401RE）的 Flash/RAM/主频。
- 与 [48]（同组前作，MCU 会话级推理）：[48] 只在 784 B 单一输入长度上报告，未考察输入长度变化带来的精度-效率权衡；本文系统扫描 8 档输入长度。
- 与 MCUNet 等 MCU-NAS 通用框架：本文把领域特性（加密流量 header 敏感性、会话级粒度）一并纳入评测。

### 5.4 优缺点

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 会话级高精度 DNN（[12][14][24][5]） | 精度 98–99.7% | 参数量 1.24M–138.45M、FLOPs 最高 3152M；无法部署到 MCU | 用 HW-NAS 换得可部署性，精度代价约 2–3 个点 |
| 包级模型（[6][51]） | 细粒度、可逐包预测 | 需更大训练量、推理频率高，累计开销大 | 会话级单次推理，累计开销更低 |
| 传统 ML（RF [32]） | 可在交换机内线速推理 | 依赖人工特征、需频繁重训；部署于高端交换硬件，非低功耗设备 | 目标 <1 W 功耗平台，扩展到 MCU 类设备 |
| 本文 | 88.26K 参数 / 10.08M FLOPs / 20.12K 张量；多任务与跨数据集稳定；INT8 后 MCU 实时 | 主任务精度低于重型 SOTA（96.60% vs >99%）；App-ID 上 94.18% 明显低于 CBS（99.67%） | — |

---

## 6. 实验表现与优势

### 6.1 实验设置

- **主基准**：ISCX VPN-nonVPN 2016（约 30 GB，11 类；Chat 25.98%、Email 12.78%、Streaming 4.52%、File Transfer 5.22%、VoIP 50.39%、P2P 1.11%，Table I）。
- **任务**：VPN-NonVPN（11 类）、VPN-Diff（2）、VPN-Type（6）、NonVPN-Type（5）、Traffic-Cat（6）、App-ID（15）（Table II）。
- **外部泛化基准**：USTC-TFC2016（20 类，Benign 405,517 样本占 81.0%、Malware 95,334 占 19.0%）、QUIC NetFlow（5 类：Chat 14,528 占 8.6%、Voice Call 61,311 占 36.3%、File Transfer 5,045 占 3.0%、Video Streaming 49,056 占 29.1%、Music Streaming 36,466 占 21.6%）。
- **部署平台**：STM32F746G-DISCO（Cortex-M7，1 MB Flash / 340 KB RAM / 216 MHz）与 Nucleo-F401RE（Cortex-M4，512 KB Flash / 96 KB RAM / 84 MHz），均为 5 V 供电（Table IV）。
- **评测协议**：重训实验 10 次独立运行报告样本标准差；嵌入式推理 1000 次平均；功耗用 USB 功率计在 idle/active 两阶段测量。

### 6.2 主任务结果（VPN-NonVPN）

- 本文：**96.60% 精度 / 96.63% F1**，88.26K 参数 / 10.08M FLOPs / 20.12K 最大张量。
- 对比中精度更高的模型代价显著：[12] 与 [14] 精度与 F1 均 >99%，但参数分别为 2.06M、1.24M（本文的 22 倍以内），FLOPs 3152.27M 与 28.96M（最多 312 倍与 2.9 倍）；[50] 最大张量 313.60K（本文的 15 倍以上）。
- [24]（ICLSTM）98.10% 精度，但三项硬件指标分别是本文的 435×/24.9×/7.5×；[35] 98.00% 精度对应 68×/4×/1.25×。
- 结论：本文是 Fig. 2 中唯一同时满足 STM32F7 与 F401RE 双约束的会话级模型。

### 6.3 多任务与 App-ID

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升/说明 |
|---|---|---|---|---|
| VPN-Diff | 精度 | 99.86 ± 0.08% | [24] 100% | 与 [24] 持平级，超过 [5] 99.82%；本文资源占用低 3 个数量级 |
| VPN-Type | 精度 | 99.14 ± 0.17% | [5] 99.38%（Hybrid） | 优于 [18] 94.80%/92.90% 与 [11] 98.30% |
| NonVPN-Type | 精度 | 94.04 ± 0.70% | [5] 99.45%（Hybrid） | 优于 [18] 89.30%/85.10% 与 [11] 81.70% |
| Traffic-Cat | 精度 | 96.74 ± 0.57% | [24] 98.20% | 该任务仅 [24] 做了对比；本文以 0.09M 参数 vs 39.12M 达成 |
| App-ID | 精度 / F1 | 94.18 ± 0.54% / 94.42 ± 0.51% | [5] 99.67% / 99.51% | 本文为会话级最优可用方案；[5] 为离线设计 |
| USTC-TFC2016 | 精度 / F1 | 99.73% / 99.73% | [10] 99.84%（18.11M 参数） | 会话级基线的张量/参数均超 MCU 约束；[46] 99.99% 但 FLOPs 19.63M |
| QUIC NetFlow | 精度 / F1 | 99.98 ± 0.01% / 99.98 ± 0.01% | CNN+RF [28] 99.00% | 比特征类方法（DWT-TC 93.70、STFT-TC 95.50、RF 95.30）高 4–6 个点 |

（数据来源：Table VI / Table VII / Table VIII 及 §VI-C/D/E 正文。）

### 6.4 预处理与输入长度消融

- **24 种预处理策略**（Table IX）：最好为 Strat. 2（去 eth 层 + IP 匿名，96.59%，即搜索时配置）；Strat. 6（IP 置零）95.38%、Strat. 7（IP 置零 + 端口置零 + UDP padding）95.12%，说明模型对 IP/端口无过拟合；最差为 Strat. 24（MAC+IP+端口全部置零）89.08%，**较最优下降 7.51%**；Strat. 22（同 24 但无端口置零）92.25%（−4.34%）；Strat. 23/21（带 UDP padding）分别为 95.24%/94.30%，说明 **UDP padding 能部分抵消大范围置零带来的损失**。
- **去 eth 层 vs MAC 置零**：Strat. 8（完全去 eth 层）95.00% 优于 Strat. 24（置零 MAC）89.08%——完全移除比部分掩码更能保持结构一致性。
- **输入长度**（Table X / Fig. 5）：784→196 B 时 FLOPs 由 10.08M 降至 2.24M、最大张量由 20.12K 降至 4.90K，参数量恒为 88.26K；多数策略（1/2/3/5/6/7）在 196 B 仅掉 1–2%；过度置零策略（4、8）降幅可达 4%。

### 6.5 嵌入式部署

- INT8 量化：PTQ 有稳定但适度的精度退化；QAT 恢复大部分损失并显著降低运行间方差，在所有输入长度上距 Float32 基线仅 0.1–0.3%。
- 推理功耗：两板 active 平均电流 0.05 A @ 5 V → **0.25 W**；idle 电流 F401RE 0.02 A（0.10 W）、F746G 0.23 A（1.15 W）。能量按 E = P·t 以 active 功率计算。
- 时延与能耗：**784 B 下 Cortex-M4 115.4 ms / 28.85 mJ，Cortex-M7 31.43 ms / 7.86 mJ**；F401RE 在 ≤400 B 时延低于 60 ms；M7 全区间 8–31 ms；能量随时延线性变化。
- 工作点建议：324–484 B 兼顾 >95% INT8 精度、M4 时延 <72 ms、M7 <20 ms，能耗分别低于 18 mJ 与 5 mJ。
- 与已有部署对比（Table XI）：[48] 同平台但只测 784 B 单点；FENXI [2] 用 ~30 W PCIe TPU 得 10–30 ms；[32] 在 Intel Tofino 上做到 <1 μs 但依赖高端交换硬件与 P4 特征管线限制。

### 6.6 优势总结

1. 三项硬件指标的压缩幅度（444×/312×/15×）在会话级 ETC 中具有明显领先性，且是唯一双 MCU 兼容的会话级模型。
2. 同一架构跨 6 任务 + 2 外部数据集泛化，说明搜索得到的结构不是任务特化的。
3. 首次系统给出"预处理策略 × 输入长度 × 量化"三维的可部署性权衡曲线，工程可用性强。
4. 提供开源实现（ProtectIT）与实测部署数据，可复现性较好。

### 6.7 局限

- 主任务精度（96.60%）低于重型 SOTA（>99%），在精度敏感场景下仍有差距。
- App-ID 精度 94.18% 明显落后 CBS 的 99.67%（尽管后者不可实时部署）。
- 量化仅在 NVIDIA 2080 Ti 上做搜索，未讨论搜索成本（100 代 × 10 子代 × 多起点训练）的绝对算力开销。
- 论文自述未来工作包括联邦学习、入侵/异常检测扩展与对抗鲁棒性，说明当前版本未覆盖这些维度（§IX）。

---

## 7. 学习与应用

### 7.1 可复用经验

1. **硬件约束写进搜索目标**比事后压缩更能保住精度——本文用三个直接对应部署瓶颈的量（Flash 容量→参数量、RAM→峰值张量、主频→FLOPs）定义阈值，阈值可直接由目标芯片规格换算。
2. **阈值来源要可追溯**：F_Th/R_Th 由 Nucleo-F401RE 的 512 KB/96 KB 在 float32 下反推，Flops_Th 由 84 MHz 反推约 130 ms 上界——这种"从芯片到约束"的换算链条值得照搬到自己的项目。
3. **预处理消融的结论具有普适性**：IP/端口信息对加密流量判别贡献有限（置零只掉约 1 个点），但"部分掩码"比"完全移除"更伤模型（Strat. 24 vs Strat. 8），说明输入处理要么保留原值、要么整段删掉，避免制造不一致的结构。
4. **UDP padding 是一个廉价的对齐技巧**：把 UDP 段补齐到与 TCP 段一致，能显著缓解置零/缩长度的精度损失。
5. **量化用 QAT 而非 PTQ**：代价很小但能把与 Float32 的差距压到 0.1–0.3%，并降低多次运行的方差。

### 7.2 可迁移到其他任务

1. 本套"约束前置 NAS + 输入长度扫描 + 量化部署"流程可直接迁移到 IoT 入侵检测、异常流量检测（论文 §IX 已列为未来方向）。
2. 预处理策略矩阵（24 组合 = eth 层处理 × MAC 处理 × IP 处理 × 端口处理 × UDP padding）是一种通用的隐私-精度评测设计，可用于任何以原始字节为输入的流量模型。
3. 部署测量协议（1000 次推理平均 + idle/active 功率分离 + E=P·t）可复用于其他边缘模型论文的实证部分。

### 7.3 对我研究的启发

- 若做加密流量分类的轻量化工作，可用本文的对比表（Table VI/VII）作为 SOTA 资源基线，其"参数/张量/FLOPs"三列已被统一到 float32 口径，横向可比性好。
- "会话级 vs 包级"的取舍需要按部署形态判断：包级精度高但推理频率高，累计开销大；会话级单次推理更适合网关-MCU 的分工架构（网关聚合、MCU 分类）。
- 若关心隐私合规场景（如 IP 不可见），Strat. 7/23 这类"置零 + padding"的组合可作为设计起点。

### 7.4 工程落地注意点

- MCU 侧只负责分类，抓包/会话聚合/缓冲由上游网关或嵌入式 Linux 板承担（§VIII-A），部署时必须按这个分工设计系统。
- 目标约束按**最弱设备**设定（Nucleo-F401RE），这样搜出的模型对更强平台天然兼容。
- 输入长度是运行时可直接调的旋钮：324/484 B 是论文推荐的精度-时延折中点。

### 7.5 可追问的问题

- HW-NAS 搜索本身的算力/时间成本是多少？论文未给出（只说明用单张 2080 Ti）。
- 数据集类别极度不均衡（VoIP 占 50.39%、P2P 仅 1.11%），是否做了重采样/类权重处理？解析稿未明确。
- 在分布漂移（新协议、新应用）下 MCU 端模型的重训/更新机制如何设计？

---

## 8. 总结

### 8.1 一句话

> 约束前置的进化式 HW-NAS 搜出 88.26K 参数的 1D-CNN，让加密流量分类在 Cortex-M4 上实时可跑。

### 8.2 速记版 Pipeline

1. 原始 pcap → 切分为会话 → 去 MAC/匿名 IP → 过滤无载荷包 → 归一化 784 B → 字节缩放 [0,1]。
2. 进化算法搜索：父代变异出子代 → 硬件约束过滤（<120K 参数、<22K 张量、<11M FLOPs）→ 训练 → 选新父代，共 100 代 × 10 子代。
3. 得最佳架构：Conv1D(129,k7,s5)→Conv1D(110,k4,s2)→AvgPool→Conv1D(38,k7,s2)→MaxPool→GAP→Dense(11)。
4. 同一架构跨 6 个分类任务重训 + USTC/QUIC 跨数据集验证 + 24 种预处理与 8 档输入长度消融。
5. INT8 QAT 量化 → STM32Cube.AI 生成 C 代码 → F746G/F401RE 实测：784 B 下 115.4 ms/28.85 mJ（M4）、31.43 ms/7.86 mJ（M7）。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[encrypted-traffic-analysis]] — 本文所属问题域；加密流量分类在资源受限设备上的落地
- [[traffic-classification]] — 会话级分类这一粒度选择是全文的核心设定

### 9.2 相关任务

- [[encrypted-traffic-detection]] — VPN/非 VPN 识别（VPN-Diff）与加密流量多分类
- [[app-fingerprinting]] — App-ID（15 类应用识别）实验

### 9.3 相关方法

- [[convolutional-network]] — 搜索空间以 1D-CNN 为基元，最终架构为纯卷积 + GAP
- [[pre-training-finetuning]] — 最佳架构在多个任务上重训的迁移范式（弱关联）

### 9.4 相关调研

- [[survey-encrypted-traffic-analysis]] — 相关工作覆盖传统 ML / DNN / NAS 三条路线的 ETC 综述

### 9.5 对比表与索引

- [[method-comparison-table]] — 本文提出 HW-NAS 驱动的轻量 ETC 方法，且给出参数/张量/FLOPs 三维对比
- [[open-source-registry]] — 代码开源：https://github.com/SEAlab-unige/ProtectIT

### 9.6 引用到的库内论文

- [[2022-TBD-Identification_of_Encrypted_Traffic_Through_Attention_Mechanism_Based_Long_Short_Term_Memory]] — 参考文献 [18]（Yao et al.，Attention-LSTM），在 Table VI/VII 中作为 flow 级基线出现

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 优化模型达到 96.60% 精度，仅 88.26K 参数 / 10.08M FLOPs / 20.12K 最大张量 | 摘要；§VI-A | Abstract; §VI-A |
| 相对 SOTA 三项指标最多降低 444× / 312× / 15× | §I 贡献点 3；§VI-B | §I, §VI-B |
| 硬件阈值设定：F_Th=120K 参数、R_Th=22K 张量、Flops_Th=11M（对齐 Nucleo-F401RE） | §V-C | §V-C, Table IV |
| HW-NAS 配置：100 代 × 10 子代，平均需生成 16 个子代才得 10 个可分子代，最大深度 5，G57 后收敛 | §V-C；Fig. 1 | §V-C, Fig. 1 |
| 24 种预处理中最佳 Strat. 2 = 96.59%，最差 Strat. 24 = 89.08%（下降 7.51%） | §VII-A | Table IX |
| 输入 784→196 B：FLOPs 10.08M→2.24M、张量 20.12K→4.90K，参数量不变 | §VII-B | Table X |
| QAT 距 Float32 仅 0.1–0.3%，PTQ 有稳定适度退化 | §VIII-B | Fig. 6 |
| 784 B 部署实测：M4 115.4 ms / 28.85 mJ；M7 31.43 ms / 7.86 mJ；active 功率 0.25 W | §VIII-B | §VIII-B, Fig. 7 |
| 多任务精度：VPN-Diff 99.86%、VPN-Type 99.14%、NonVPN-Type 94.04%、Traffic-Cat 96.74%、App-ID 94.18% | §VI-C, §VI-D | Table VI, Table VII |
| 跨数据集：USTC-TFC2016 99.73%、QUIC NetFlow 99.98% | §VI-E | §VI-E, Table VIII |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-TNSM-Hardware-Aware_Neural_Architecture_Search_for_Encrypted_Traffic_Classification_on_Resource-Constrained_Devices.pdf
- MinerU Markdown：02-parsed-markdown/2026-TNSM-Hardware-Aware_Neural_Architecture_Search_for_Encrypted_Traffic_Classification_on_Resource-Constrained_Devices.md
- 代码仓库（论文 §I 贡献点给出）：https://github.com/SEAlab-unige/ProtectIT
- DOI：https://doi.org/10.1109/tnsm.2026.3666676

---

## 12. 后续问题

1. 搜索阶段的总计算开销（GPU 小时数）未报告，难以评估 HW-NAS 相对手工设计的成本收益。
2. 作者另有 arXiv 预印本编号 2506.11319（同组 [48] 为 arXiv:2506.10851），本篇以 IEEE TNSM 正式版为准，正文未提及预印本关系。
3. 论文未说明 ISCX 类别不均衡（VoIP 50.39%）是否做了采样或加权处理，需查代码仓库或原文附录确认。
4. Table XI 中 [48] 与本文在相同平台上报出完全一致的时延数值（31.43 ms / 115.40 ms, 784 B），两者关系（同架构不同输入扫描）值得进一步核对。
5. INT8 部署只报了时延/能耗，未报 MCU 端 INT8 精度与 float32 的对照数值（仅 Fig. 6 曲线描述），若引用需谨慎。

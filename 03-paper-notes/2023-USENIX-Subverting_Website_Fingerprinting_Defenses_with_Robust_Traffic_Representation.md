---
type: paper
title_original: "Subverting Website Fingerprinting Defenses with Robust Traffic Representation"
title_cn: "以鲁棒流量表示颠覆网站指纹防御"
authors:
  - Meng Shen
  - Kexin Ji
  - Zhenbo Gao
  - Qi Li
  - Liehuang Zhu
  - Ke Xu
year: 2023
venue: "USENIX Security 2023"
doi: ""
url: ""
pdf: "00-inbox/PDFs/2023-USENIX-Subverting_Website_Fingerprinting_Defenses_with_Robust_Traffic_Representation.pdf"
mineru_md: "02-parsed-markdown/2023-USENIX-Subverting_Website_Fingerprinting_Defenses_with_Robust_Traffic_Representation.md"
status: processed
reading_level: L2
research_area:
  - website-fingerprinting
  - traffic-analysis
  - adversarial-robustness
task:
  - website-fingerprinting
method:
  - CNN
  - adversarial-training
dataset: []
code: "https://github.com/robust-fingerprinting/RF"
relevance: high
created: "2026-05-27"
updated: "2026-05-29"
---

# Subverting Website Fingerprinting Defenses with Robust Traffic Representation

## 0. 元信息

| 项目 | 内容 |
|---|---|
| 标题 | Subverting Website Fingerprinting Defenses with Robust Traffic Representation |
| 作者 | Meng Shen, Kexin Ji, Zhenbo Gao, Qi Li, Liehuang Zhu, Ke Xu |
| 机构 | 北京理工大学（网络空间科学技术学院、计算机学院）、清华大学（网络科学与网络安全研究所、计算机科学与技术系） |
| 会议 | USENIX Security 2023 |
| 日期 | 2023 年 8 月 9-11 日 |
| 代码 | https://github.com/robust-fingerprinting/RF |

## 1. 研究动机

Tor 匿名网络每天约有两百万活跃用户用于保护隐私，但其面临 website fingerprinting (WF) 攻击的威胁。攻击者通过分析加密连接的侧信道信息（如包大小、方向、包间时延）来推断用户访问的网站。

近年来已有多种防御方案（如 WTF-PAD、Front、Walkie-Talkie、TrafficSliver、RegulaTor、Blanket）被提出，其策略包括延迟发送、注入 dummy packets、多路径分流等。然而，现有的 state-of-the-art (SOTA) WF 攻击在面对不同防御时效果大幅下降：DF 和 Var-CNN 在 Front 下准确率降至 75% 以下，在 TrafficSliver 下低于 60%；Tik-Tok 和 Var-CNN 在网络带宽变化时准确率也显著降低。

**核心问题**：现有 traffic representation 方案（粗粒度统计特征或细粒度逐包特征序列）在不同防御策略下均会受到严重干扰，导致攻击鲁棒性不足。

## 2. 核心贡献

1. **提出 Robust Fingerprinting (RF) 攻击**：一种在多种防御策略下均能保持高准确率的鲁棒 WF 攻击方法。
2. **设计 Traffic Aggregation Matrix (TAM)**：一种新的 traffic representation 方法，通过在固定时间窗口内聚合出入方向的包数量来捕获鲁棒特征，能够同时抵抗 packet padding 和 packet delaying 防御。
3. **基于 CNN 的分类器**：利用 2D 和 1D convolutional blocks 从 TAM 中自动学习区分性特征，使用 Global Average Pooling (GAP) 替代全连接层以减少过拟合。
4. **提出针对 RF 的反制措施**：基于 Class Activation Mapping (CAM) 识别关键特征区域，通过 packet padding 和 delaying 实现 traffic morphing 防御。
5. **全面的实验评估**：在 closed-world 和 open-world 场景下与 7 种 SOTA 攻击在 9 种防御下进行了系统比较。

## 3. 方法动机：为什么现有防御会失败？

### 3.1 现有防御策略概览

WF 防御可分为两大类策略：
- **Disturbing traffic**：通过注入 dummy packets 或延迟真实包来破坏流量模式。代表方案包括 WTF-PAD（zero-delay adaptive padding，63% 带宽开销）、Front（Rayleigh 分布注入 dummy packets，103% 带宽开销）、Walkie-Talkie（半双工模式 + decoy page 合并，31% 带宽 + 34% 时间开销）、RegulaTor（规范化为连续衰减的 packet surges，77% 带宽 + 5% 时间开销）、Blanket（白盒 adversarial perturbation，85% 或 47% 带宽开销）
- **Splitting traffic**：将流量分割到多条路径以破坏原始指纹。代表方案 TrafficSliver（零带宽/时间开销，但需重构 Tor 网络）

### 3.2 为什么现有 WF 攻击在防御下失效？

现有攻击的 traffic representation 有两类，各有致命弱点：

**粗粒度统计特征**（k-NN、k-FP、CUMUL 使用）：
- 信息泄露分析显示，这些特征在不同防御间变化剧烈（Figure 2），在 WTF-PAD 下信息泄露量从 undefended 的 3.0 降至 2.0，Front 下降至 1.0，Walkie-Talkie 下仅 0.5
- 原因：dummy packet padding 直接改变了 trace 的统计摘要（如均值、方差、分位数），这些全局统计量对扰动极为敏感
- 实验验证：k-NN、k-FP、CUMUL 在 WTF-PAD 下准确率分别降至 40.94%、68.33%、59.80%，在 Front 下更降至 4.37%、52.66%、30.61%

**细粒度逐包特征序列**（DF 的 packet direction、Tik-Tok 的 timing with direction）：
- 这些特征同样受到 dummy packet padding 和 packet delaying 的显著影响，因为 padding 的随机性和 delaying 导致包序列模式发生剧烈变化
- 信息泄露分析证实：packet direction 在所有防御下泄露量仅 0.5，timing with direction 同样仅 0.5
- 实验验证：DF 在 Front 下降至 76.85%，TrafficSliver-BWR 下降至 19.99%；Tik-Tok 在 RegulaTor 下降至 47.07%

**关键原因总结**：粗粒度特征过度聚合丢失了局部模式，细粒度特征过度精确容易被扰动破坏。两者都无法在防御扰动下保持稳定的信息泄露。

### 3.3 核心洞察：packet-per-second 的鲁棒性

信息泄露分析揭示了一个关键发现：**Packet-per-second（每秒包数量）** 在 undefended、WTF-PAD 和 Front trace 上的信息泄露量几乎一致（均为 1.0）。这一发现的直觉解释：

- **对 packet padding 的鲁棒性**：padding 增加的 dummy packets 被分散到多个时间窗口中，每个窗口内的包数量变化被"稀释"，不会产生剧烈波动。多个时间窗口可以容纳总包数的变化，影响被分散
- **对 packet delaying 的鲁棒性**：由于用户体验考虑，防御引入的延迟通常有界（如 Front 报告 <35% 时间开销）。中等程度的延迟不会改变包落入的时间窗口——一个被延迟的包很可能仍然落在同一个时间槽内。时间窗口的统计聚合特性使其对时序扰动具有天然容忍度
- **对 traffic splitting 的鲁棒性**：即使流量被分割，攻击者获得的那部分流量在每个时间窗口内的包数量模式仍然保留了部分网站指纹信息

这一洞察直接指导了 TAM 的设计：**在固定时间窗口内聚合出入方向的包数量，既保留了足够的区分性信息，又能天然抵抗 padding 和 moderate delaying 扰动**。

### 3.4 威胁模型

- **攻击者类型**：本地、被动攻击者（local and passive attacker）
- **能力范围**：只能嗅探和记录客户端与 Tor guard node 之间连接的数据包，不能修改、延迟、丢弃或解密数据包
- **潜在攻击者**：客户端本地网络的窃听者、Internet Service Provider (ISP)、位于客户端和 guard node 之间的 Autonomous System (AS)
- **攻击假设**：攻击者事先知道受害者部署的具体防御方案，能够获取目标防御生成的 traffic traces 进行 adversarial training（second-mover advantage）
- **评估场景**：
  - **Closed-world**：客户端仅访问已知的 monitored websites 集合
  - **Open-world**：客户端同时访问 monitored 和大量 unmonitored websites

## 4. 方法设计：Robust Fingerprinting 的完整技术方案

### 4.1 信息泄露分析框架

作者采用 Li et al. (2018 CCS) 提出的 information leakage 指标进行系统化特征评估：

$$I(F;C) = H(C) - H(C|F)$$

其中 $C$ 为 monitored websites 集合，$F$ 为特定 representation 的特征集，$H(\cdot)$ 为熵。$I(F;C)$ 越大，表示该特征对网站分类的贡献越大。

**实验设置**：随机选取 95 个 monitored websites 各 100 条 undefended traces，并生成对应的 WTF-PAD、Front、Walkie-Talkie defended traces，量化分析 9 类特征集的信息泄露量。

**关键发现**（Figure 2）：

| 特征类型 | Undefended | WTF-PAD | Front | Walkie-Talkie |
|---|---|---|---|---|
| k-NN 统计特征 | 3.0 | 2.0 | 1.0 | 0.5 |
| k-FP 统计特征 | 3.0 | 2.5 | 1.0 | 0.5 |
| CUMUL 统计特征 | 3.0 | 2.0 | 1.0 | 0.5 |
| Packet Direction | 0.5 | 0.5 | 0.5 | 0.5 |
| Timing with Direction | 0.5 | 0.5 | 0.5 | 0.5 |
| Inter-arrival Time | 1.0 | 1.0 | 1.0 | 1.0 |
| Concentration | 1.0 | 1.0 | 1.0 | 1.0 |
| Burst | 1.0 | 1.0 | 1.0 | 1.0 |
| **Packet-per-Second** | **1.0** | **1.0** | **1.0** | 1.0 |

粗粒度统计特征在 undefended 下信息量最高（3.0），但在防御下急剧下降；细粒度逐包特征在所有场景下信息量都较低（0.5）且不变；**Packet-per-Second 在 undefended 和 WTF-PAD/Front defended 下保持相同的泄露量（1.0）**，这是唯一在 padding 类防御下信息不衰减的特征。

### 4.2 Traffic Aggregation Matrix (TAM) 的设计与构建

**数学定义**：给定 trace $F = (f_1, f_2, ..., f_l)$，其中 $f_k = \langle t_k, d_k \rangle$ 为第 $k$ 个包的时间戳和方向（$d_k = 1$ 为 outgoing，$d_k = -1$ 为 incoming）。TAM 为矩阵 $M \in \mathbb{R}^{2 \times N}$，其中 $N = T/s$，$T$ 为最大加载时间，$s$ 为时间槽长度。

元素 $m_{ij}$ 的计算：
$$m_{ij} = |\{f_k \in F : (j-1) \cdot s < t_k \leq j \cdot s, \text{direction}(f_k) = i\}|$$

**构建算法**（Algorithm 1）：
1. 初始化 $2 \times N$ 的零矩阵 $M$
2. 遍历 trace 中的每个 packet $f_k = \langle t_k, d_k \rangle$
3. 计算列索引 $j = \lceil t_k / s \rceil$
4. 若 $j \leq N$，根据方向 $d_k < 0$ 确定行索引 $i$（incoming=1, outgoing=2）
5. 更新 $m_{ij} \gets m_{ij} + 1$

**TAM 的中间粒度优势**：TAM 捕获的是 packet-per-time-slot 级别的特征，位于粗粒度统计特征和细粒度逐包特征之间的"甜蜜点"：
- 比统计特征更精细：保留了时间维度上的流量波动模式
- 比逐包序列更鲁棒：时间窗口聚合天然容忍窗口内的小扰动
- Tik-Tok 用精确时间戳，Var-CNN 用 inter-packet time，这些都"过度详细"（overly detailed），容易被扰动破坏

**对不同防御策略的鲁棒性机制**：
- **Packet padding（WTF-PAD、Front）**：dummy packets 被分散到多个时间窗口中，每个窗口的包数量变化被稀释。例如，注入 100 个 dummy packets 分散到 80 秒的加载时间中，每个 44ms 窗口平均仅增加约 0.055 个包
- **Packet delaying（Walkie-Talkie、RegulaTor）**：由于用户体验约束，延迟通常 bounded（Front <35% 时间开销，Walkie-Talkie 34% 时间开销）。中等延迟不改变包落入的时间窗口；即使改变，也仅影响相邻窗口
- **Traffic splitting（TrafficSliver）**：攻击者只能获得部分流量，但每个时间窗口内的包数量模式仍然保留了部分指纹信息

**超参数选择**（通过 extended candidate search 调优）：
- Maximum Length $L = 5000$（公平比较需要）
- Maximum Load Time $T = 80s$（超过 80s 后 accuracy 增长趋于平缓）
- Time Slot $s = 44ms$（过小导致 TAM 稀疏，过大导致信息丢失；44ms 在 accuracy 和空间开销间取得平衡）
- 最终 TAM 维度：$2 \times 1818$（$80/0.044 \approx 1818$）

### 4.3 鲁棒性量化验证：Intra-class Distance

使用 Maximum Mean Discrepancy (MMD) 衡量原始 trace $F$ 和防御后 trace $F'$ 之间的分布差异：

$$MMD(X^s, X^t) = \left\| \frac{1}{n} \sum_{i=1}^{n} \phi(x_i^s) - \frac{1}{m} \sum_{i=1}^{m} \phi(x_i^t) \right\|_{\mathcal{H}}$$

其中 $\phi(\cdot)$ 将数据映射到 Reproducing Kernel Hilbert Space (RKHS)，使用 5 个 Gaussian kernels 的 Kernel Trick 计算。Intra-class distance 定义为：

$$D_{intra}(F, F') = \frac{1}{|C|} \sum_{c=1}^{|C|} MMD(F_c, F'_c)$$

**关键实验结果**（Figure 4）：

Packet padding 实验（固定 time overhead=10%，变化 bandwidth overhead）：
- TAM 的 intra-class distance 在 bandwidth overhead 从 20% 增至 800% 时几乎不变（约 0.2）
- Packet direction 从 0.1 增至 0.8，timing with direction 从 0.1 增至 0.6
- 在 real-world defenses（WTF-PAD、Front）下 TAM 的距离同样远小于其他两种表示

Packet delaying 实验（固定 bandwidth overhead=30%，变化 time overhead）：
- 在 moderate time overhead（<15%）下，TAM 达到最短的 intra-class distance（约 0.05-0.15）
- 当 time overhead 超过 20% 后 TAM 的距离开始增长，但此时用户体验已严重受损
- 即使不使用时间信息，packet direction 在 WTF-PAD 下的 intra-class distance 也随 time overhead 增加而增加（高延迟导致 burst 间出现大时间间隙，使 WTF-PAD 能扰动更多模式）

**结论**：TAM 是比 packet direction 和 timing with direction 更鲁棒的 traffic representation，能容忍大带宽开销和中等时间开销。

### 4.4 CNN 分类器架构详解

RF 的 CNN 分类器将 TAM 视为"图像"输入，包含三个核心组件：

**2D Convolutional Blocks**（2 个）：
- 第一个 block：32 通道，kernel size $3 \times 6$，stride 1，padding 1；后接 BatchNorm、ReLU、$1 \times 3$ max pooling、dropout 0.1
- 第二个 block：64 通道，kernel size $3 \times 6$，stride 1，padding 1；后接 BatchNorm、ReLU、$2 \times 2$ max pooling、dropout 0.1
- 功能：提取 TAM 的局部空间特征。同一列的两个元素代表同一时间槽内 incoming 和 outgoing 包的数量，反映客户端-服务器交互；同一行相邻元素代表相同方向在连续时间槽的包数量，反映流量 burst 的波动

**Reshape 操作**：2D blocks 输出的 64 通道 feature maps 被 reshape 为 32 通道的 1D 向量，尺寸翻倍，使更深的网络能提取更高层特征

**1D Convolutional Blocks**（2 个）：
- 第三个 block：128 通道，kernel size 3；后接 BatchNorm、ReLU、$1 \times 3$ max pooling、dropout 0.3
- 第四个 block：256 通道，kernel size 3；后接 BatchNorm、ReLU、$1 \times 3$ max pooling、dropout 0.3
- 功能：提取更高层的抽象特征

**Global Average Pooling (GAP) 层**：
- 替代全连接层，直接计算每个 feature map 的平均值，后接 softmax 得到各网站的概率
- 优势：(1) 不引入额外参数，缓解过拟合；(2) 可接受不同长度的输入（调整 $N$ 无需改变网络架构）
- 损失函数：Cross-Entropy；优化器：Adam（learning rate 0.0005，weight decay 0.001，batch size 200）

**Ablation Study**（Appendix C）：
- $\text{RF}_{vari}$（DF 的 CNN + TAM 作为输入）在防御下比 DF 提升显著：WTF-PAD +4%、Front +14%、RegulaTor +42%、Walkie-Talkie +18%、BD +74%、BWR +55%
- RF（本文 CNN + TAM）比 $\text{RF}_{vari}$ 再提升 1%-5%
- 结论：**TAM 是 RF 鲁棒性的关键贡献者**，CNN 架构提供了边际增益

## 5. 与其他方法的对比分析

### 5.1 RF 与现有 WF 攻击的本质区别

| 维度 | k-NN/k-FP/CUMUL | DF | Tik-Tok | Var-CNN | **RF** |
|---|---|---|---|---|---|
| 特征类型 | 手工统计特征 | Packet direction | Direction × Time | Direction + IPT + Metadata | **TAM（packet-per-slot）** |
| 粒度 | 粗粒度（trace 级） | 细粒度（逐包） | 细粒度（逐包） | 细粒度（逐包） | **中间粒度（per-slot）** |
| 分类器 | SVM/k-NN/RF | CNN | CNN | ResNet ensemble | **2D+1D CNN** |
| 对 padding 鲁棒性 | 极差 | 中等 | 较好 | 较好 | **最优** |
| 对 delaying 鲁棒性 | 极差 | 差 | 中等 | 中等 | **最优** |
| 对 splitting 鲁棒性 | 差 | 极差 | 较好 | 中等 | **最优** |

**关键差异**：
- **vs DF**：DF 仅用 packet direction（1D 序列），在 Front 下降至 76.85%，TrafficSliver-BWR 下降至 19.99%。RF 的 TAM 聚合了时间窗口内的包数量，在 Front 下保持 93.34%，BWR 下保持 79.68%
- **vs Tik-Tok**：Tik-Tok 用 direction × raw time，在 RegulaTor 下降至 47.07%（因 traffic regularization 直接破坏时序模式）。RF 的时间窗口聚合对 regularization 有更强容忍度，保持 67.43%
- **vs Var-CNN**：Var-CNN 使用 inter-packet time，在 Front 下降至 79.24%（因 dummy packets 改变了 inter-packet intervals）。RF 不依赖精确的包间时延，保持 93.34%

### 5.2 RF 击败了哪些防御？

**完全击败**（accuracy 仅下降 <3%）：
- WTF-PAD：RF 96.58%（undefended 98.83%，仅降 2.25%）
- Blanket-I：RF 98.57%（几乎无损）
- Blanket-ID：RF 98.62%（几乎无损）

**大幅击败**（accuracy 下降 5-10%）：
- Front：RF 93.34%（降 5.49%），而 DF 降至 76.85%（降 21.55%）
- Walkie-Talkie：RF 93.87%（降 4.96%），而 DF 降至 71.02%（降 27.38%）

**有效击败**（accuracy 下降 10-25%）：
- TrafficSliver-BD：RF 95.70%（降 3.13%）
- TrafficSliver-BWR：RF 79.68%（降 19.15%），但仍比次优攻击（Tik-Tok 57.63%）高 22.05%

**部分有效**（accuracy 下降 >30%）：
- RegulaTor：RF 67.43%（降 31.40%），但仍比次优攻击（Var-CNN 47.68%）高 19.75%
- Tamaraw：RF 8.54%（所有攻击均被击败，因 Tamaraw 以极高开销规范化流量）

### 5.3 为什么 RF 对 RegulaTor 效果相对有限？

RegulaTor 将流量规范化为"连续衰减的 packet surges"，这本质上改变了流量的 burst 结构——而 TAM 正是通过捕获 burst 模式来区分网站的。RegulaTor 的 77% 带宽 + 5% 时间开销虽然 moderate，但其 traffic regularization 策略直接攻击了 TAM 所依赖的时间窗口包数量模式。这说明 **traffic regularization 是 WF 防御的一个有前景方向**，因为它从根本上改变了流量的统计特性而非仅仅添加噪声。

## 6. 实验表现：具体数据与关键发现

### 6.1 Closed-world 完整数据（Full Knowledge）

| 攻击 | Undefended | WTF-PAD | Front | RegulaTor | Tamaraw | Blanket-I | Blanket-ID | Walkie-Talkie | BD | BWR |
|---|---|---|---|---|---|---|---|---|---|---|
| k-NN | 93.64 | 40.94 | 4.37 | 5.11 | 4.56 | - | - | 26.11 | 27.06 | 4.47 |
| k-FP | 94.45 | 68.33 | 52.66 | 49.27 | 7.88 | - | - | 39.81 | 77.39 | 36.35 |
| CUMUL | 95.11 | 59.80 | 30.61 | 18.60 | 8.18 | - | - | 24.48 | 19.39 | 9.06 |
| AWF | 94.32 | 52.67 | 17.28 | 13.11 | 7.06 | - | - | 29.61 | 11.70 | 4.99 |
| DF | 98.40 | 90.85 | 76.85 | 20.96 | 6.89 | 97.94 | 98.00 | 71.02 | 20.69 | 19.99 |
| Tik-Tok | 98.45 | 93.80 | 84.79 | 47.07 | 6.94 | 98.15 | 98.13 | 72.85 | 92.74 | 57.63 |
| Var-CNN | 98.87 | 94.70 | 79.24 | 47.68 | 3.13 | 98.50 | 98.49 | 87.53 | 95.50 | 31.09 |
| **RF** | **98.83** | **96.58** | **93.34** | **67.43** | **8.54** | **98.57** | **98.62** | **93.87** | **95.70** | **79.68** |

### 6.2 RF 相对最佳已有攻击的提升

| 防御 | 次优攻击（准确率） | RF（准确率） | **绝对提升** |
|---|---|---|---|
| WTF-PAD | Var-CNN (94.70%) | 96.58% | **+1.88%** |
| Front | Tik-Tok (84.79%) | 93.34% | **+8.55%** |
| RegulaTor | Var-CNN (47.68%) | 67.43% | **+19.75%** |
| Walkie-Talkie | Var-CNN (87.53%) | 93.87% | **+6.34%** |
| Blanket-I | Var-CNN (98.50%) | 98.57% | +0.07% |
| Blanket-ID | Var-CNN (98.49%) | 98.62% | +0.13% |
| BD | Var-CNN (95.50%) | 95.70% | +0.20% |
| BWR | Tik-Tok (57.63%) | 79.68% | **+22.05%** |

**平均提升 8.9%**（over Tik-Tok under nine defenses）。

### 6.3 Partial Knowledge 评估（WTF-PAD 不同分布参数）

| 攻击 | norm | beta | gamma | pareto | weibull | 跨分布波动 |
|---|---|---|---|---|---|---|
| DF | 92.25 | 82.26 | 85.01 | 89.12 | 78.58 | 13.67 |
| Tik-Tok | 94.20 | 92.02 | 92.33 | 93.39 | 90.92 | 3.28 |
| Var-CNN | 94.91 | 88.64 | 89.81 | 92.58 | 85.67 | 9.24 |
| **RF** | **97.51** | **97.42** | **96.39** | **96.87** | **96.98** | **1.12** |

RF 在所有分布下均保持 96% 以上，跨分布波动仅 1.12%，远小于 DF（13.67%）和 Var-CNN（9.24%）。Weibull 分布（右偏分布，可采样更短的 inter-arrival time，使 WTF-PAD 注入更多 dummy packets）对 DF 和 Var-CNN 影响最大，但对 RF 几乎无影响。

### 6.4 网络条件变化下的评估

| 攻击 | 快速加载-undefended | 快速加载-WTF-PAD | 快速加载-Front | 慢速加载-undefended | 慢速加载-WTF-PAD | 慢速加载-Front |
|---|---|---|---|---|---|---|
| DF | 95.06 | 87.68 | 75.18 | 86.48 | 64.71 | 51.75 |
| Tik-Tok | 94.72 | 86.69 | 70.96 | 83.32 | 62.12 | 43.48 |
| Var-CNN | 95.47 | 91.18 | 75.72 | 83.81 | 66.33 | 45.51 |
| **RF** | **96.77** | **94.62** | **90.49** | 81.62 | **70.62** | **64.08** |

关键发现：
- RF 在所有 defended datasets 上保持最高准确率
- 慢速加载-Front 下 RF（64.08%）比次优 Var-CNN（45.51%）高 18.57%
- DF 在慢速 undefended trace 上表现最好（86.48%），说明时间特征受网络变化影响更大，但 TAM 的时间窗口聚合比精确时间戳更鲁棒

### 6.5 Open-world 评估

RF 的 precision-recall 曲线在所有 7 种防御下完全覆盖其他 SOTA 攻击的曲线。特别在高 recall 设置下：
- **Front**：当 recall=1.0 时，RF precision 约 0.6，Tik-Tok/Var-CNN 降至 0.5，DF 降至 0.45
- **Walkie-Talkie**：当 recall=1.0 时，RF precision 约 0.8，其他攻击降至 0.3-0.5
- **RegulaTor**：当 recall=1.0 时，RF precision 约 0.6，其他攻击降至 0.2-0.3
- **TrafficSliver-BWR**：当 recall=1.0 时，RF precision 约 0.5，其他攻击降至 0.0-0.4

### 6.6 TAM 变体实验

| 变体 | Undefended | WTF-PAD | Front | RegulaTor | Walkie-Talkie | BD | BWR |
|---|---|---|---|---|---|---|---|
| RF（标准） | 98.83 | 96.58 | 93.34 | 67.43 | 93.87 | 95.70 | 79.68 |
| RF_inf（无长度限制） | 98.80 | 97.11 | 94.83 | 69.24 | 94.45 | 95.64 | 79.60 |
| RF_overlap（25%重叠） | 98.78 | 96.86 | 93.70 | 66.11 | 92.49 | 94.82 | 78.04 |

- 移除长度限制（$\text{RF}_{inf}$）可进一步提升对 disturbing traffic defenses 的准确率（考虑更多包）
- 重叠时间槽（$\text{RF}_{overlap}$）无明显改善，说明 44ms 的时间槽已足够小，重叠无法提供更多有价值特征

## 7. 反制措施：针对 RF 的防御方案

### 7.1 防御设计

作者提出了一种基于 traffic morphing 的防御方案，核心思想是学习其他网站的关键特征区域，将当前网站的流量伪装成其他网站的模式。

**Step 1：Informative Regions Extraction**（Algorithm 2）：
- 利用 Class Activation Mapping (CAM) 计算 TAM 各元素对分类的重要性分数 $IS$
- 提取超过阈值 $\tau$ 的连续区域作为 informative regions
- 每个 informative region $p = [p_1, p_2, ..., p_l]$ 表示在连续时间槽内应发送的包数量序列

**Step 2：Traffic Morphing**（Algorithm 3）：
- 随机选择一个目标类别 $c' \neq c$，将其 informative regions 作为伪装目标
- 对每个时间窗口，将当前包数 $p_q$ 向目标 $p_{tar}$ 靠拢：
  - 若 $p_q \in [\lceil(1-\delta_{min}) \cdot p_{tar}\rceil, \lceil(1+\delta_{max}) \cdot p_{tar}\rceil]$，直接发送
  - 若 $p_q > \top$，延迟多余包到后续时间窗口
  - 若 $p_q < \bot$，注入 dummy packets 补足
- 参数设置：$\delta_{max}=0.3$，$\delta_{min}=0.2$

**开销控制**：
- 当目标 informative region 要求发送大量数据但当前负载较低时，不完全匹配，而是在空闲时间槽中均匀发送少量随机包（从 $[1, U]$ 中均匀采样），平衡延迟和带宽开销

### 7.2 防御效果对比

| 防御方案 | 带宽开销 | 时间开销 | RF 准确率 | Var-CNN 准确率 |
|---|---|---|---|---|
| TrafficSliver-BD | 0% | 0% | 95.70% | 95.50% |
| TrafficSliver-BWR | 0% | 0% | 79.68% | 31.09% |
| Window-filling | 45% | 0% | 98.64% | 97.47% |
| WTF-PAD | 63% | 0% | 96.58% | 94.70% |
| Front | 103% | 0% | 93.34% | 79.24% |
| Walkie-Talkie | 31% | 34% | 93.87% | 87.53% |
| RBB | 43% | 14% | 97.63% | 86.35% |
| Blanket-ID | 47% | 23% | 98.62% | 98.49% |
| RegulaTor | 77% | 5% | 67.43% | 47.68% |
| **本文防御** | **73%** | **14%** | **52.59%** | **27.65%** |

本文防御是所有方案中对 RF 和 Var-CNN 防御效果最好的，分别将准确率降至 52.59% 和 27.65%。与 RegulaTor 相比，本文防御在 RF 上低 15%，在 Var-CNN 上低 20%，且带宽开销更低（73% vs 77%）。

## 8. 学习与应用

### 8.1 WF 攻防军备竞赛的核心教训

**教训一：扰动不足以对抗自适应攻击者**

现有防御的根本问题在于它们只在流量表面添加"噪声"（dummy packets、延迟），而没有改变流量的底层统计结构。RF 通过 TAM 捕获的 packet-per-time-slot 特征正好利用了这一点：噪声被时间窗口聚合所吸收，而底层的流量模式（burst 结构、方向分布）仍然保留。

这意味着 WF 防御需要从"添加噪声"转向"改变结构"。RegulaTor 的 traffic regularization 策略（将流量规范化为统一的衰减模式）是唯一对 RF 造成显著威胁的防御（将准确率降至 67.43%），因为它从根本上改变了流量的统计特性。

**教训二：中间粒度表示是对抗鲁棒性的关键**

论文揭示了一个深刻的设计原则：在粗粒度和细粒度之间存在一个"鲁棒性甜蜜点"。
- 粗粒度（统计特征）：信息丰富但极易被扰动破坏
- 细粒度（逐包序列）：精确但过度敏感
- 中间粒度（per-time-slot 聚合）：信息量足够且天然容忍扰动

这一原则可推广到其他 traffic analysis 任务：在设计对抗鲁棒的特征表示时，应寻找对预期扰动具有天然不变性的聚合级别。

**教训三：信息泄露分析是特征设计的定量基础**

传统 WF 攻击的特征选择依赖经验（"包方向很重要"、"时间戳有用"），而本文通过 information leakage 分析定量证明了 packet-per-second 在防御下的信息保持能力。这种数据驱动的特征选择方法比直觉更有说服力，应成为鲁棒系统设计的标准流程。

### 8.2 本质上难以防御的流量特征

RF 的成功揭示了以下流量特征在当前防御策略下本质上难以消除：

1. **时间窗口内的包数量统计**：padding 增加的包被分散到多个窗口中稀释，moderate delaying 不改变包落入的窗口。要有效干扰此特征，需要大幅改变每个窗口的包数量，但这会带来极高的带宽或时间开销

2. **流量 burst 的宏观结构**：网站加载过程中的 burst 模式（大量包在短时间内传输）反映了页面资源的加载顺序和大小，这是由 HTTP 协议和浏览器行为决定的，很难通过流量层面的扰动完全消除

3. **客户端-服务器交互模式**：同一时间槽内 incoming 和 outgoing 包的数量关系反映了请求-响应的交互模式，这是网站结构的固有特征

### 8.3 对未来研究的启示

**对防御研究者**：
- Traffic regularization（如 RegulaTor）是有前景的方向，因为它改变流量结构而非添加噪声
- 作者提出的 CAM-based traffic morphing 随机选择目标类别和 informative regions，可通过先验知识（如估计的发送速率）优化选择过程
- 不引入时间开销的情况下有效降低 RF 准确率仍是开放问题

**对攻击研究者**：
- 移除 TAM 的 maximum length 限制可进一步提升准确率（$\text{RF}_{inf}$ 实验验证）
- TAM 的设计可推广到其他匿名网络（如 I2P、VPN）的流量分析
- 网络条件变化（特别是 guard node 和 client 同时变化）需要更多真实 trace 评估

**对系统设计者**：
- WF 防御的真实部署（而非仿真）是评估的关键缺失环节
- 防御方案需要在 overhead 和 effectiveness 之间取得更好的平衡

## 9. 方法论亮点

1. **信息论驱动的特征设计**：通过 information leakage 分析系统评估各类特征在不同防御下的鲁棒性，而非凭直觉选择特征
2. **中间粒度的 traffic representation**：TAM 在粗粒度统计特征和细粒度逐包特征之间找到了平衡点（packet-per-time-slot），既有足够的信息量又能容忍扰动
3. **矩阵化表示与图像类比**：将 TAM 视为"图像"输入 CNN，充分利用 2D 卷积在空间特征提取上的优势
4. **GAP 替代全连接层**：减少参数量、缓解过拟合，且能接受不同长度的输入

## 10. 关键术语表

| 术语 | 说明 |
|---|---|
| Website Fingerprinting (WF) | 通过分析加密流量的侧信道信息推断用户访问网站的被动攻击 |
| Traffic Aggregation Matrix (TAM) | 本文提出的 traffic representation，以 2×N 矩阵形式聚合时间窗口内出入方向的包数量 |
| Robust Fingerprinting (RF) | 本文提出的鲁棒 WF 攻击方法 |
| Global Average Pooling (GAP) | 替代全连接层的池化方法，计算每个 feature map 的平均值 |
| Class Activation Mapping (CAM) | 用于识别 TAM 中对分类贡献最大的区域 |
| Information Leakage | 衡量特征关于网站标签泄露的信息量，$I(F;C) = H(C) - H(C|F)$ |
| Maximum Mean Discrepancy (MMD) | 衡量两个数据集分布差异的核方法 |
| Intra-class Distance | 同一网站的原始 trace 和防御后 trace 之间的表示距离 |
| Packet Padding | 注入 dummy packets 的防御策略 |
| Packet Delaying | 延迟真实数据包发送时间的防御策略 |
| Traffic Splitting | 将流量分散到多条路径的防御策略 |

## 11. 与其他工作的关系

### 11.1 攻击方法谱系

| 方法 | 年份/会议 | 特征 | 分类器 | 对防御的鲁棒性 |
|---|---|---|---|---|
| k-NN | 2014 USENIX | 手工统计特征 | k-NN | 极差 |
| CUMUL | 2016 NDSS | 累积表示 | SVM | 极差 |
| k-FP | 2016 USENIX | 统计特征集 | RF + k-NN | 差 |
| AWF | 2018 NDSS | Packet direction | DNN | 差 |
| DF | 2018 CCS | Packet direction | CNN | 中等（对 padding 有效，对 splitting 无效） |
| TF | 2019 CCS | Packet direction | Triplet Network | 未评估防御 |
| Var-CNN | 2019 PoPETs | Direction + IPT + Metadata | ResNet ensemble | 较好（但对 Front/RegulaTor 不足） |
| Tik-Tok | 2020 PoPETs | Direction × Raw Time | CNN | 较好（但对 RegulaTor 不足） |
| **RF** | **2023 USENIX** | **TAM（packet-per-slot）** | **2D+1D CNN** | **最优** |

### 11.2 继承与改进

- **继承 DF 的 CNN 架构**：RF 的 1D convolutional blocks 结构与 DF 类似，但增加了 2D blocks 处理 TAM 的二维结构
- **继承 Tik-Tok 的时序信息利用**：Tik-Tok 首次证明了 packet timing 对 WF 的价值，但用 direction × raw time 过于精确；RF 用时间窗口聚合替代，保持时序信息的同时提高鲁棒性
- **继承 information leakage 分析框架**（Li et al., 2018 CCS）：该框架原本用于衡量防御的信息泄露程度，RF 将其用于特征选择，证明了 packet-per-second 的鲁棒性
- **改进 TAM 的设计**：解决了 DF 仅用方向信息（丢失时序）和 Tik-Tok 用精确时间戳（过于敏感）的两个极端问题

### 11.3 防御方案覆盖

本文评估的防御覆盖了所有主要策略类别：
- **Adaptive padding**：WTF-PAD（2016 ESORICS）
- **Trace randomization**：Front（2020 USENIX）
- **Half-duplex + decoy**：Walkie-Talkie（2017 USENIX）
- **Traffic regularization**：RegulaTor（2022 PoPETs）、Tamaraw（2014 CCS）
- **Adversarial perturbation**：Blanket（2021 USENIX）
- **Traffic splitting**：TrafficSliver（2020 CCS）
- **CAM-based perturbation**：RBB（2018 WNYISPW）

### 11.4 与对抗鲁棒性研究的关系

论文 Section 2.2 指出了 WF 场景与计算机视觉对抗鲁棒性的根本差异：
- 在 CV 中，对抗扰动需要对人"不可感知"，限制了扰动幅度
- 在 WF 中，防御者可以施加大得多的扰动（dummy packets 不需要"不可感知"），且扰动空间远大于 CV
- 因此，adversarial training、gradient masking、region-based classification 等 CV 中有效的防御策略在 WF 中效果有限
- RF 的 approach（提取对扰动不变的特征）比直接增强模型鲁棒性更有效

## 12. 个人思考与启发

1. TAM 的设计思想可以推广到其他 traffic analysis 任务：在粗粒度和细粒度表示之间寻找对扰动鲁棒的中间粒度
2. 信息泄露分析作为特征选择的定量工具，比经验性的特征工程更有说服力
3. RF 对 RegulaTor 的攻击效果相对有限（67.43%），说明流量正则化（traffic regularization）仍是 WF 防御的有效方向
4. CAM-based 防御思路新颖，但目标类别的随机选择可能不是最优策略，可考虑基于相似度的最优匹配
5. 开放问题：如何在不引入时间开销的情况下有效降低 RF 的准确率

## 13. 参考价值

**对 traffic classification 研究者**：TAM 的设计方法论（信息泄露分析 -> 中间粒度表示 -> CNN 自动特征提取）可迁移到加密流量分类场景。

**对隐私保护研究者**：RF 揭示了现有防御的根本脆弱性——仅依赖特定形式的扰动（padding/delaying/splitting）不足以对抗自适应攻击者，需要从根本上改变流量的统计特性。

**对对抗鲁棒性研究者**：WF 场景下的对抗鲁棒性与计算机视觉不同，防御者可以施加更大规模的扰动且无需对人"不可感知"，因此传统的 adversarial training、gradient masking 等策略效果有限。

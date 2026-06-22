---
type: paper
title_original: "COUNTMAMBA: A Generalized Website Fingerprinting Attack via Coarse-Grained Representation and Fine-Grained Prediction"
title_cn: "COUNTMAMBA：基于粗粒度表示与细粒度预测的通用网站指纹攻击"
authors: [Xianwen Deng, Ruijie Zhao, Yanhao Wang, Mingwei Zhan, Zhi Xue, Yijun Wang]
year: 2025
venue: "IEEE S&P 2025"
doi: "unknown"
url: "unknown"
pdf: "00-inbox/PDFs/2025-S&P-Countmamba__A_Generalized_Website_Fingerprinting_Attack_via_Coarse-Grained_Representation_and_Fine-Grained_Prediction.pdf"
mineru_md: "02-parsed-markdown/2025-S&P-Countmamba__A_Generalized_Website_Fingerprinting_Attack_via_Coarse-Grained_Representation_and_Fine-Grained_Prediction.md"
status: processed
reading_level: L3
research_area: [website-fingerprinting, encrypted-traffic-analysis]
task: [robust-website-fingerprinting, early-stage-attack, multi-tab-attack, tor-traffic-analysis]
method: [state-space-model, coarse-grained-representation, causal-convolution, windowed-traffic-counting-matrix]
dataset: [DFset, ARESset, TMWFset, k-NNset, Walkie-Talkie]
code: "https://github.com/SJTUdxw/CountMamba-WF"
relevance: high
created: "2026-06-21"
updated: "2026-06-21"
---

# COUNTMAMBA: A Generalized Website Fingerprinting Attack via Coarse-Grained Representation and Fine-Grained Prediction

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | COUNTMAMBA: A Generalized Website Fingerprinting Attack via Coarse-Grained Representation and Fine-Grained Prediction |
| 中文标题 | COUNTMAMBA：基于粗粒度表示与细粒度预测的通用网站指纹攻击 |
| 作者 | Xianwen Deng, Ruijie Zhao, Yanhao Wang, Mingwei Zhan, Zhi Xue, Yijun Wang |
| 机构 | 上海交通大学网络空间安全学院, 东南大学网络空间安全学院 |
| 年份 | 2025 |
| 会议/期刊 | IEEE S&P 2025 |
| 研究方向 | [[website-fingerprinting]], [[encrypted-traffic-analysis]] |
| 任务类型 | 鲁棒WF攻击, 早期阶段攻击, 多标签WF攻击 |
| 方法关键词 | [[state-space-model]], 粗粒度表示, 因果CNN, [[traffic-representation-learning]] |
| 数据集 | DFset, ARESset, TMWFset, k-NNset, Walkie-Talkie |
| 是否开源 | 是 — https://github.com/SJTUdxw/CountMamba-WF |
| PDF | `00-inbox/PDFs/2025-S&P-Countmamba__A_Generalized_Website_Fingerprinting_Attack_via_Coarse-Grained_Representation_and_Fine-Grained_Prediction.pdf` |
| MinerU Markdown | `02-parsed-markdown/2025-S&P-Countmamba__A_Generalized_Website_Fingerprinting_Attack_via_Coarse-Grained_Representation_and_Fine-Grained_Prediction.md` |

---

## 1. 一句话总结

> 提出COUNTMAMBA框架，通过Windowed Traffic Counting Matrix (WTCM) 构建粗粒度流量表示以抵抗防御扰动，结合State-Space-Oriented (SSO) 分类器实现因果性与迭代性的细粒度增量预测，在鲁棒攻击（RegulaTor下F1=96.62%，比RF提升28.89%）、早期阶段攻击（20%加载率F1=58.68%，比Holmes提升5%）和多标签攻击（MAP@2=91.89%，比ARES提升约4%）三种场景下均达到SOTA。

---

## 2. 摘要翻译

### 2.1 摘要原文

Tor is the leading low-latency anonymous communication network, widely used to protect users' privacy through mechanisms such as random relay selection. However, despite these defenses, Tor traffic remains susceptible to website fingerprinting (WF) attacks, where attackers analyze side-channel information (e.g., packet size, direction, inter-packet timing) to infer visited websites. Although WF attacks have shown high success rates in controlled settings, they rely on complete, unperturbed traffic, making them vulnerable to real-world defense mechanisms. Traditional WF approaches, which typically employ Machine Learning (ML) or Deep Learning (DL) to classify packet sequences as a single-label prediction, struggle to generalize in practical scenarios, especially under defenses that alter packet patterns or in environments requiring multilabel, early-stage analysis.

In this work, we introduce COUNTMAMBA, a robust and adaptable WF attack framework designed to address the challenges posed by real-world defenses, early-stage traffic analysis, and multi-tab browsing. COUNTMAMBA employs a Windowed Traffic Counting Matrix (WTCM) to create resilient, coarse-grained traffic representations by aggregating packet events within fixed time intervals, allowing it to withstand moderate perturbations from defenses. Additionally, a state-space-oriented (SSO) classifier incrementally generates fine-grained predictions from partial traffic data, maintaining high attack accuracy while enabling early-stage and multi-tab attack capabilities. Extensive experiments demonstrate that COUNTMAMBA outperforms state-of-the-art WF attacks across robust, early-stage, and multi-tab scenarios.

### 2.2 摘要中文翻译

Tor是领先的低延迟匿名通信网络，通过随机中继选择等机制广泛用于保护用户隐私。然而，尽管有这些防御措施，Tor流量仍然容易受到网站指纹(WF)攻击，攻击者通过分析侧信道信息（如数据包大小、方向、包间时序）来推断用户访问的网站。尽管WF攻击在受控环境中表现出很高的成功率，但它们依赖完整、未受干扰的流量，使其容易受到现实世界防御机制的影响。传统WF方法通常使用机器学习(ML)或深度学习(DL)将数据包序列作为单标签预测进行分类，在实际场景中泛化能力不足，尤其是在改变数据包模式的防御下或需要多标签、早期阶段分析的环境中。

本文提出COUNTMAMBA，一个鲁棒且适应性强的WF攻击框架，旨在应对现实世界防御、早期阶段流量分析和多标签浏览带来的挑战。COUNTMAMBA使用窗口化流量计数矩阵(WTCM)通过在固定时间间隔内聚合数据包事件来创建具有弹性的粗粒度流量表示，使其能够承受防御带来的中等扰动。此外，面向状态空间(SSO)的分类器从部分流量数据增量生成细粒度预测，在保持高攻击准确性的同时实现早期阶段和多标签攻击能力。大量实验证明COUNTMAMBA在鲁棒、早期阶段和多标签场景下均优于最先进的WF攻击。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

现有WF攻击存在一个根本性矛盾：**细粒度表示 + 粗粒度预测**的传统范式限制了泛化能力。细粒度的逐包特征（如包方向序列、时序序列）极易被防御机制破坏；粗粒度的单次分类预测依赖完整流量，无法支持早期阶段攻击和多标签攻击。作者提出反转这一范式：使用**粗粒度表示 + 细粒度预测**。

### 3.2 现有方法的痛点和不足

| 痛点 | 具体表现 | 受影响的方法 |
|---|---|---|
| 对防御不鲁棒 | 细粒度方向/时序序列被dummy packet和packet delay严重破坏 | AWF, DF, TF, Var-CNN |
| 无法早期阶段攻击 | 依赖完整流量产生单一分类结果，无法从部分流量推断 | 大部分DL方法 |
| 无法多标签攻击 | 设计为单标签分类，无法处理多标签浏览 | AWF, DF, Tik-Tok, Var-CNN |
| 专用方法互不兼容 | 鲁棒攻击(RF)、早期阶段(Holmes)、多标签(ARES/TMWF)各自为战，无法同时解决 | RF, Holmes, ARES, TMWF |
| RF对RegulaTor效果差 | TAM仅计数包数，RegulaTor通过包延迟+dummy packet破坏计数模式 | RF (F1降至67.73%) |
| Holmes效率低 | 每次攻击需完整特征构建和前向传播，不适用于迭代式早期攻击 | Holmes |

### 3.3 论文的研究假设或核心直觉

核心直觉包含三个层面：

1. **粗粒度表示更鲁棒**：基于时间窗口的计数特征（而非逐包序列）能承受dummy packet插入和packet delay带来的扰动，因为真实包通常仍在同一时间窗口内
2. **相关cell依赖性是关键特征**：Tor cell与TLS record之间的映射关系（一个TLS record包含多个512字节cell）构成网站特有的cell模式，现有防御未破坏这一模式
3. **SSM天然适合增量预测**：状态空间模型具有因果性（输出仅依赖当前和过去输入）和迭代性（保持中间状态），无需重新计算即可逐步更新预测

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | WF攻击在受控环境准确率>95%，但在防御/早期/多标签场景下大幅退化；现有专用方法只能解决单一场景 | §I, Table 1 |
| 痛点提炼 | "细粒度表示 + 粗粒度预测"的传统范式是根本瓶颈：细粒度特征易被防御破坏，粗粒度预测依赖完整流量 | §I (Figure 1对比) |
| 问题转化 | 从"如何设计更好的单场景攻击"转化为"如何设计一个统一框架同时解决鲁棒性、早期阶段和多标签三个挑战" | §I |
| 文献定位 | 位于WF攻击从专用方法向通用方法演进的关键节点。RF(鲁棒)、Holmes(早期)、ARES/TMWF(多标签)各自为战，无统一方案 | Table 1, §II |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 粗粒度（时间窗口计数）表示比细粒度（逐包序列）表示更能抵抗防御扰动，同时保留足够区分信息 | 经验研究[19]证明每秒包数特征可承受中等扰动 | Table 4（鲁棒攻击实验） |
| 辅助假设1 | Tor cell间依赖关系是被现有WF攻击忽视的关键特征，且现有防御未破坏此模式 | Tor数据传输层分析（Figure 3）：TLS record → 多个512B cell | Table 10（消融实验） |
| 辅助假设2 | SSM的因果性和迭代性使其天然适合早期阶段增量预测，优于CNN/Transformer | CNN/Transformer不满足因果性或迭代性（Table 13） | Table 6, 7（早期阶段实验） |

**假设验证结果：**

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 强支撑 | RegulaTor下COUNTMAMBA F1=96.62% vs RF=67.73%（+28.89%） | Table 4 |
| 辅助假设1 | 强支撑 | TAM(无cell依赖)加载率50%时F1=13.10%；WTCM(有cell依赖)=60.40%（+47.3%） | Table 10 |
| 辅助假设2 | 强支撑 | 置信度阈值0.4时，COUNTMAMBA加载率41.51%即达97.43%准确率；Holmes需59.93%加载率达97.28% | Table 6, 7 |

---

## 4. 方法设计

### 4.1 方法整体流程

```
输入: Tor流量trace F = (f1, f2, ..., fL), 每个fk = <tk, lk>
  ↓
Step 1: WTCM构建（粗粒度表示）
  - 将trace按时间窗口w切分
  - 计算每个窗口内不同cell数和方向的TLS record计数
  - 计算窗口内cluster数和窗口间gap
  - 对数平滑变换
  ↓
Step 2: 因果CNN（局部特征建模）
  - 多层因果卷积，每层仅使用当前和过去输入
  - 内存组件保留前k-1个输入以支持迭代推理
  ↓
Step 3: SSM（全局序列建模 + 增量预测）
  - 位置编码嵌入
  - 状态空间模型迭代处理序列
  - 训练时使用卷积形式并行化
  - 推理时使用递归形式线性时间
  ↓
Step 4: 预测输出
  - 鲁棒攻击: AVGPool → FC → 单标签分类
  - 早期阶段: 每个时间步FC → 置信度阈值判断
  - 多标签: 二元交叉熵 → 多标签分类
  ↓
输出: 网站分类结果
```

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| WTCM构建 | Trace F = <tk, lk> | 按时间窗口w切分，统计方向+cell数+cluster+gap | 矩阵 M ∈ R^(2C+2)×N | 粗粒度鲁棒表示 |
| 对数平滑 | 矩阵 M | M = log(1+M) | 平滑后的M | 缓解数值不稳定 |
| 因果CNN | M序列 | L层因果卷积(核大小k)，带内存组件 | 特征序列 M^(L) | 局部模式提取 |
| 位置编码 | M^(L) | 加入位置嵌入 E_pos | X = M^(L) + E_pos | 注入位置信息 |
| SSM处理 | X序列 | h_t = A_bar·h_{t-1} + B_bar·x_t; y_t = C·h_t | 输出序列 Y | 全局序列建模 |
| 单标签预测 | Y序列 | AVGPool → FC → Softmax | 网站标签 | 鲁棒攻击 |
| 早期阶段预测 | y_1...y_t | AVGPool([y_1,...,y_t]) → FC → 置信度检查 | 网站标签或继续等待 | 增量预测 |
| 多标签预测 | Y + Y_t | BCE(粗粒度) + ΣBCE(细粒度) | 多个网站标签 | 多标签攻击 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| WTCM | 粗粒度流量表示 | Tor trace | (2C+2)×N矩阵 | 下游CNN的输入 |
| 因果CNN (含内存) | 局部特征提取 | WTCM序列 | 特征序列 | SSM的输入 |
| SSO Block | 全局建模+增量预测 | 特征序列 | 类别相关特征 | 输出到预测层 |
| 预测头 | 分类输出 | SSM输出 | 网站标签 | 支持三种攻击模式 |

### 4.4 公式、算法和机制解释

**1. WTCM构建（Algorithm 1）**

对每条TLS record f_k = <t_k, l_k>：
- 方向 d_k = sign(l_k)
- Cell数 c_k = min(floor(|l_k|/512), C)
- 列索引 j = min(floor(t_k/w) + 1, N)（对应时间窗口）
- 行索引 i = 2×c_k + (d_k > 0 ? 1 : 2)（方向+cell数组合）
- M[i,j] += 1
- 额外特征：窗口内cluster数（基于时间间隔阈值）和窗口间gap

对数平滑：M = log(1 + M)

**2. SSM核心公式**

离散化状态空间模型：
$$h_t = \bar{A} h_{t-1} + \bar{B} x_t$$
$$y_t = C h_t$$

其中 $\bar{A} = \exp(\Delta A)$, $\bar{B} = (\Delta A)^{-1}(\exp(\Delta A) - I) \cdot \Delta B$（零阶保持离散化）

卷积形式（训练并行化）：
$$\bar{K} = (C\bar{B}, C\bar{A}\bar{B}, ..., C\bar{A}^{N-1}\bar{B})$$
$$y = x * \bar{K}$$

**3. 早期阶段预测（Algorithm 2）**

每个时间窗口间隔w执行：
1. 计算当前窗口WTCM特征
2. 因果CNN前向传播（利用内存，仅处理新数据）
3. SSM更新（利用隐藏状态，仅处理新数据）
4. AVGPool聚合所有已有预测 → FC → Softmax
5. 若 max(q_t^early) >= 阈值τ，则输出结果；否则等待下一窗口

**4. 多标签损失**

$$\mathcal{L}_{coarse} = BCE(\hat{Y}, Y_{true})$$
$$\mathcal{L}_{fine} = \sum_{t=1}^{N} BCE(\hat{Y}_t, Y_{true}^t)$$

### 4.5 方法优势

1. **统一框架**：一个模型同时支持鲁棒、早期阶段、多标签三种攻击场景
2. **粗粒度表示抗扰动**：时间窗口计数对dummy packet和packet delay具有天然鲁棒性
3. **cell依赖性特征**：捕获TLS record中Tor cell的依赖关系，现有防御未破坏此模式
4. **因果性+迭代性**：SSM仅需保留一个中间状态h_t即可增量推理，无需重新计算
5. **动态置信度阈值**：可灵活平衡加载率与准确率

### 4.6 方法不足

1. **对Tamaraw无效**：Tamaraw通过固定包长和发送速率消除cell模式，F1仅11.29%（虽然Tamaraw开销过高不实用）
2. **时间窗口长度固定**：44ms的固定窗口长度可能不是所有场景的最优选择
3. **最大加载时间限制**：超过320s后性能下降（特征复杂度增加但信息不增加）
4. **未考虑主动攻击者**：仅针对被动窃听者，未讨论主动攻击场景
5. **多标签场景缺少细粒度标签**：ARESset无细粒度标签，无法评估细粒度预测在大规模数据上的效果

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

传统WF范式：**细粒度表示（逐包方向/时序序列）→ 粗粒度预测（单一分类结果）**

COUNTMAMBA范式：**粗粒度表示（时间窗口计数矩阵）→ 细粒度预测（每个时间窗口的增量分类）**

这一反转带来双重优势：粗粒度表示对防御鲁棒，细粒度预测支持早期阶段和多标签攻击。

与RF的区别：RF使用TAM（Traffic Aggregating Matrix）仅计数每秒进出包数；COUNTMAMBA的WTCM额外捕获cell依赖关系和时序分布特征。

与Holmes的区别：Holmes使用embedding空间中的聚类中心和信任半径；COUNTMAMBA使用SSM的增量预测+置信度阈值，迭代效率更高（无需完整前向传播）。

与ARES/TMWF的区别：ARES/TMWF基于[[transformer]]，不满足因果性和迭代性；COUNTMAMBA基于[[state-space-model]]，天然支持增量推理。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 粗粒度表示+细粒度预测范式 | 反转传统WF的"细粒度表示+粗粒度预测"范式 | 高 | 是 — 适用于其他时序分类任务 |
| WTCM | 窗口化计数矩阵，整合方向、cell依赖、时序分布 | 高 | 是 — 适用于加密流量表示 |
| SSO分类器 | 因果CNN+SSM，满足因果性和迭代性 | 高 | 是 — 适用于增量时序分类 |
| cell依赖性特征 | 利用Tor cell与TLS record的映射关系作为区分特征 | 中 | 部分 — 依赖Tor协议特性 |
| 统一三场景框架 | 一个模型同时支持鲁棒/早期/多标签攻击 | 高 | 是 — 统一框架思想通用 |

### 5.3 适用场景

- Tor网络上的网站指纹攻击
- 有WF防御（dummy packet、packet delay、流量分割）的场景
- 需要早期阶段识别的实时监控场景
- 多标签浏览环境下的网站识别
- 被动窃听者模型

### 5.4 方法对比表

| 方法 | 表示粒度 | 预测粒度 | 鲁棒性 | 早期阶段 | 多标签 | RegulaTor F1 | 20%加载F1 | MAP@2 |
|---|---|---|---|---|---|---|---|---|
| k-FP | 统计特征 | 粗 | 差 | 差 | × | 47.71% | 2.71% | - |
| CUMUL | 累积表示 | 粗 | 差 | 差 | × | 49.16% | 7.28% | - |
| AWF | 方向序列 | 粗 | 差 | 差 | × | 11.82% | 10.74% | 15.66% |
| DF | 方向序列 | 粗 | 中 | 差 | × | 22.36% | 16.35% | 63.01% |
| Tik-Tok | 方向+时序 | 粗 | 中 | 差 | × | 51.90% | 14.65% | 70.47% |
| Var-CNN | 方向+时序 | 粗 | 中 | 差 | × | 62.87% | 17.30% | 72.94% |
| RF | 包数计数(TAM) | 粗 | 较好 | 中 | × | 67.73% | 28.87% | 64.66% |
| Holmes | 时序分布 | 粗 | 中 | 好 | × | - | 53.30% | - |
| TMWF | 方向序列 | 粗 | 中 | 差 | √ | 23.10% | 11.08% | 78.24% |
| ARES | 方向序列 | 粗 | 中 | 差 | √ | 27.44% | 12.94% | 81.74% |
| **COUNTMAMBA** | **WTCM** | **细** | **强** | **强** | **√** | **96.62%** | **58.68%** | **87.33%** |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **实现**：PyTorch 2.1.2, Python 3.10.5, 约2000行代码
- **硬件**：单块NVIDIA GeForce RTX 4090
- **数据划分**：训练:验证:测试 = 8:1:1
- **开放世界**：未监控网站视为额外类别

### 6.2 数据集

| 数据集 | 类型 | 规模 | 用途 |
|---|---|---|---|
| DFset | 单标签 | 95网站×1000 traces(闭世界) + 40000网站(开世界) | 鲁棒攻击、早期阶段攻击 |
| ARESset | 多标签 | 大规模多标签Tor浏览数据 | 多标签攻击 |
| TMWFset | 多标签(合成) | TBB + Chrome两个子集 | 细粒度预测评估 |
| k-NNset | 单标签 | - | 额外单标签验证 |
| Walkie-Talkie | 单标签 | - | 额外单标签验证 |

### 6.3 Baseline

11个SOTA方法：k-FP, CUMUL, AWF, DF, TF, TMWF, Tik-Tok, Var-CNN, RF, Holmes, ARES

防御机制：WTF-PAD, FRONT, RegulaTor, Tamaraw, TrafficSliver (Round Robin / By Direction / BWR)

### 6.4 评价指标

- **单标签**：Accuracy (AC), Precision (PR), Recall (RC), F1 (macro average)
- **多标签**：P@K, MAP@K

### 6.5 关键实验结果

**Table 4 — 鲁棒攻击（F1, %）：**

| 防御 | 无防御 | RB | BD | BWR | WTF-PAD | FRONT | RegulaTor | Tamaraw |
|---|---|---|---|---|---|---|---|---|
| RF | 98.67 | 99.17 | 95.72 | 77.36 | 97.41 | 95.84 | 67.73 | 6.34 |
| **COUNTMAMBA** | **99.20** | **99.66** | **98.36** | **80.28** | **98.56** | **99.00** | **96.62** | 11.29 |
| 提升 | +0.53 | +0.49 | +2.64 | +2.92 | +1.15 | +3.16 | **+28.89** | +4.95 |

**Table 7 — 早期阶段攻击（实际场景）：**

| 方法 | 延迟 | 加载率 | 准确率 |
|---|---|---|---|
| Holmes | 16.68s | 59.93% | 97.28% |
| RF | 10.36s | 44.83% | 77.77% |
| **COUNTMAMBA** | **8.86s** | **41.51%** | **97.43%** |

**Table 8 — 多标签攻击（闭世界MAP@K）：**

| 标签数 | ARES | TMWF | COUNTMAMBA | 提升(vs ARES) |
|---|---|---|---|---|
| 2-tab MAP@2 | 87.07 | 83.20 | **91.89** | +4.82 |
| 3-tab MAP@3 | 83.49 | 73.87 | **87.76** | +4.27 |
| 4-tab MAP@4 | 83.32 | 72.52 | **87.41** | +4.09 |
| 5-tab MAP@5 | 78.94 | 70.83 | **81.46** | +2.52 |

**Table 9 — 多标签细粒度预测（TMWFset）：**

| 数据集 | COUNTMAMBA P@2(粗粒度) | COUNTMAMBA Acc(细粒度) |
|---|---|---|
| TBB | 87.60% | 93.47% |
| Chrome | 83.70% | 94.77% |

**Table 10 — 消融实验（RegulaTor防御, 10%标注流量）：**

| 表示 | cell依赖 | 时序分布 | 对数变换 | 50%加载F1 | 80%加载F1 |
|---|---|---|---|---|---|
| TAM | × | × | × | 13.10% | 25.22% |
| WTCM | √ | × | × | 55.24% | 70.82% |
| WTCM | √ | √ | × | 57.72% | 72.83% |
| WTCM | √ | √ | √ | 60.40% | 75.82% |

### 6.6 优势最明显的场景

1. **RegulaTor防御下**：F1提升28.89%（96.62% vs 67.73%），因为WTCM的cell依赖性特征未被RegulaTor破坏
2. **早期阶段攻击**：20%加载率F1=58.68%，比Holmes提升5%；且延迟仅8.86s（Holmes需16.68s）
3. **多标签攻击**：MAP@2=91.89%，比ARES提升约4%，且提供细粒度预测（访问序列和频率）

### 6.7 局限性

1. Tamaraw（固定包长/速率）可有效反制，但该防御开销过大不实用
2. 最大加载时间超过320s后性能下降
3. 时间窗口长度(44ms)为固定超参数，未做自适应调整
4. 仅评估被动攻击者，未考虑主动攻击
5. ARESset缺少细粒度标签，多标签细粒度评估仅在合成数据集上进行

---

## 7. 学习与应用

### 7.1 是否开源？

是 — https://github.com/SJTUdxw/CountMamba-WF

### 7.2 复现关键步骤

1. 数据预处理：从pcap提取TLS record trace，每条record包含时间戳和长度（正负编码方向）
2. WTCM构建：实现Algorithm 1，设置w=44ms, C=3, N=T/w；注意cell数计算 floor(|l_k|/512) 和对数平滑
3. 因果CNN实现：多层因果卷积+内存组件，内存保留前k-1个输入用于推理时增量计算
4. SSM实现：使用零阶保持离散化(公式21-22)，训练时用卷积形式(公式6-7)，推理时用递归形式(公式4-5)
5. 三种预测模式实现：单标签(AVGPool→FC)、早期阶段(增量AVGPool→置信度检查)、多标签(BCE损失)
6. 训练：AdamW优化器, lr=2e-3, weight_decay=0.05, batch_size=200, epochs=100

### 7.3 关键超参数、预处理和训练细节

| 超参数 | 单标签值 | 多标签值 | 说明 |
|---|---|---|---|
| 最大加载时间 | 120s | 320s | 超过则截断 |
| 最大trace长度 | 5,000 | 10,000 | TLS record数 |
| 时间窗口长度 | 44ms | 44ms | 跟随TAM设定 |
| 最大cell数C | 3 | 3 | 受Ethernet MSS限制 |
| 嵌入维度 | 256 | 256 | SSM隐藏维度 |
| 模型深度 | 3 | 3 | 因果CNN+SSM层数 |
| Drop Path Rate | 0.2 | 0.2 | 正则化 |
| 学习率 | 2e-3 | 2e-3 | AdamW |
| Weight Decay | 0.05 | 0.05 | AdamW |
| Batch Size | 200 | 200 | - |
| 训练轮数 | 100 | 100 | - |

### 7.4 能否迁移到其他任务？

**高迁移潜力：**
- **粗粒度表示+细粒度预测范式**：可迁移到任何需要鲁棒+增量预测的时序分类任务
- **WTCM表示方法**：可迁移到其他加密流量分析任务（如恶意流量检测、应用识别）
- **SSO分类器架构**：因果CNN+SSM的组合可迁移到任何需要因果性+迭代性的序列建模任务
- **置信度阈值的早期停止机制**：通用的增量预测停止策略

**部分迁移：**
- cell依赖性特征依赖Tor协议特性，不直接适用于非Tor流量

### 7.5 对我的研究有什么启发？

1. **表示粒度与预测粒度的解耦**：传统方法往往假设表示和预测的粒度应该一致，本文证明反转二者的粒度可以同时获得鲁棒性和灵活性
2. **SSM在流量分析中的应用**：[[state-space-model]] 的因果性和迭代性使其天然适合流式/增量流量分析场景，相比[[transformer]]有推理效率优势
3. **时间窗口计数作为鲁棒特征**：简单的计数特征在对抗防御时比复杂的逐包特征更有效，"简单但鲁棒"的设计哲学值得借鉴
4. **cell依赖性作为新特征维度**：Tor协议栈各层之间的映射关系是被忽视的特征来源，启发我们关注协议内部结构特征

---

## 8. 总结

### 8.1 核心思想

> 粗粒度表示抗扰动，细粒度预测增量推。

### 8.2 速记版 Pipeline

1. Tor trace → WTCM（时间窗口计数矩阵，含cell依赖和时序特征）
2. WTCM → 因果CNN（局部模式提取，带内存支持迭代）
3. 因果CNN → SSM（全局建模，因果+迭代，增量预测）
4. 鲁棒攻击：AVGPool全序列 → 分类
5. 早期阶段：每个时间步增量预测 → 置信度阈值判断
6. 多标签：粗粒度+BCE细粒度 → 多标签分类

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]] — 网站指纹识别技术
- [[encrypted-traffic-analysis]] — 加密流量分析
- [[traffic-representation-learning]] — 流量表示学习

### 9.2 相关方法

- [[state-space-model]] — 状态空间模型（S4/Mamba），本文SSO分类器的核心
- [[transformer]] — Transformer模型，ARES和TMWF使用的基础架构，本文作为对比
- [[survey-website-fingerprinting]] — WF综述

### 9.3 相关任务

- [[website-fingerprinting]] — 鲁棒WF攻击、早期阶段WF攻击、多标签WF攻击
- Tor流量分析
- 匿名通信流量识别

### 9.4 可更新的综述页面

- [[survey-website-fingerprinting]] — 可加入COUNTMAMBA作为通用WF攻击的代表
- [[encrypted-traffic-analysis]] — 可加入SSM在流量分析中的应用案例

### 9.5 可加入的对比表

- [[website-fingerprinting]] 中的WF攻击对比表：加入COUNTMAMBA的三场景SOTA数据
- [[state-space-model]] 中的SSM应用场景表：加入WF攻击场景

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 传统WF范式"细粒度表示+粗粒度预测"限制泛化 | Figure 1对比分析 | §I |
| 时间窗口计数比逐包序列更抗防御扰动 | 经验研究引用[19] + 本文Table 4验证 | §4.1, §6.2 |
| cell依赖性是关键区分特征 | Table 10消融：TAM vs WTCM F1差距47.3% | §7 |
| SSM满足因果性和迭代性 | Table 13模型对比分析 | Appendix E |
| RegulaTor下COUNTMAMBA F1=96.62%，RF=67.73% | Table 4 | §6.2 |
| BWR防御下F1=80.28%，比RF提升2.92% | Table 4 | §6.2 |
| 20%加载率F1=58.68%，比Holmes提升5% | Table 5 | §6.3 |
| 置信度0.4时41.51%加载率达97.43%准确率 | Table 6 | §6.3 |
| 延迟8.86s vs Holmes 16.68s | Table 7 | §6.3 |
| 多标签MAP@2=91.89%，比ARES提升约4% | Table 8 | §6.4 |
| 细粒度预测准确率93.47%(TBB)和94.77%(Chrome) | Table 9 | §6.4 |
| cell依赖性消融：TAM 13.10% vs WTCM 60.40%（50%加载） | Table 10 | §7 |
| 因果CNN+SSM是唯一同时满足因果性和迭代性的架构 | Table 13 | Appendix E |
| Tamaraw可反制COUNTMAMBA但开销过大(182%时间+269%带宽) | Table 3, Table 4 | §6.2 |
| 2023年新数据集上COUNTMAMBA仍显著优于其他方法 | Table 14 | Appendix G |

---

## 11. 原始资料链接

- PDF: `00-inbox/PDFs/2025-S&P-Countmamba__A_Generalized_Website_Fingerprinting_Attack_via_Coarse-Grained_Representation_and_Fine-Grained_Prediction.pdf`
- MinerU Markdown: `02-parsed-markdown/2025-S&P-Countmamba__A_Generalized_Website_Fingerprinting_Attack_via_Coarse-Grained_Representation_and_Fine-Grained_Prediction.md`
- 代码: https://github.com/SJTUdxw/CountMamba-WF

---

## 12. 后续问题

1. 如何设计自适应时间窗口长度？固定44ms是否对所有网站最优？
2. cell依赖性特征在非Tor加密流量（如HTTPS直接连接）中是否存在类似模式？
3. SSM与[[transformer]]的混合架构能否进一步提升性能？
4. 针对cell依赖性特征，能否设计低开销的防御机制？（论文§7提出利用Grad-CAM定位关键区域+固定长度padding的思路）
5. 在更长时间尺度（>320s）的场景下，如何改进WTCM的设计？
6. 多标签场景下细粒度预测（访问序列和频率）的实际隐私威胁有多大？

---

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

从现有WF攻击"细粒度表示+粗粒度预测"范式的根本矛盾出发：细粒度特征易被防御破坏，粗粒度预测依赖完整流量无法支持早期/多标签场景。作者提出反转这一范式——用粗粒度的WTCM表示抵抗防御扰动，用细粒度的SSO分类器实现增量预测。通过引入被忽视的Tor cell依赖性特征和状态空间模型的因果性/迭代性，在三个场景下同时达到SOTA，证明"通用攻击"优于"专用攻击"。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 提出"通用WF攻击"的愿景 | 定义问题和贡献 | "Unlike prior WF methods, COUNTMAMBA iteratively updates predictions" |
| Introduction | 从传统范式的矛盾出发，建立三场景统一攻击的必要性 | 问题定位+动机建立 | Figure 1的传统vs COUNTMAMBA对比 |
| Related Work | 梳理ML/DL WF攻击和防御，定位"无通用方案"的空白 | 文献定位 | Table 1展示专用方法各自为战 |
| Threat Model | 定义被动攻击者+防御+多标签+早期阶段的现实威胁模型 | 场景设定 | 三因素威胁模型 |
| §4 WTCM | 从鲁棒性论证到cell依赖性发现，再到WTCM设计 | 核心创新1 | Figure 3的协议栈分析揭示cell依赖性 |
| §5 SSO | 从因果性/迭代性需求出发，选择因果CNN+SSM | 核心创新2 | Table 13的模型对比分析 |
| §6 Experiments | 三场景逐步验证：鲁棒→早期→多标签 | 全面验证 | Table 4(RegulaTor +28.89%)是最大亮点 |
| §7 Discussion | 消融归因+参数分析+防御建议 | 深入理解 | Table 10消融证明cell依赖性是关键 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 范式Gap | 细粒度表示+粗粒度预测的传统范式限制泛化 | 矛盾分析(Figure 1) | §I |
| 场景Gap | 无统一方案同时解决鲁棒/早期/多标签 | Table 1的专用方法对比 | §I, Table 1 |
| 特征Gap | 现有方法忽视Tor cell依赖性 | 协议栈分析(Figure 3) | §4.2 |
| 模型Gap | CNN/Transformer不满足因果性和迭代性 | Table 13的模型对比 | Appendix E |
| 联合场景Gap | 专用方法在联合场景（如防御+早期）下失效 | Appendix D实验 | Appendix D |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 鲁棒攻击(Table 4) | 证明粗粒度表示的抗扰动能力 | 验证核心假设1 |
| 早期阶段(Table 5-7) | 证明SSO分类器的增量预测能力 | 验证核心假设3 |
| 多标签(Table 8-9) | 证明细粒度预测的多标签能力 | 验证统一框架 |
| 消融(Table 10) | 归因cell依赖性为关键特征 | 验证辅助假设1 |
| 参数敏感性(Figure 8) | 展示超参数的影响范围 | 工程指导 |
| 联合场景(Appendix D) | 证明通用方法优于专用方法在联合场景 | 核心论点支撑 |
| 新数据集(Appendix G) | 证明方法的时效性 | 泛化验证 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 从传统范式的矛盾（细粒度表示+粗粒度预测）出发 | "反转范式"的开篇策略 |
| Gap提出方式 | Table 1展示专用方法各自为战，联合场景无解 | 表格式Gap声明+联合场景论证 |
| 方法论证逻辑 | 先论证粗粒度的鲁棒性(§4.1)→发现cell依赖性(§4.2)→设计WTCM(§4.3)；先分析模型需求(§5.1)→选择SSM(§5.2) | 从需求分析到设计选择的递进逻辑 |
| 实验组织逻辑 | 鲁棒→早期→多标签→消融→参数→联合→新数据集，逐步验证每个假设 | 每个实验对应一个假设/质疑 |
| 局限性讨论方式 | §7 Discussion中的Countermeasure主动讨论如何防御本方法 | 展示安全研究的攻防思维 |
| 最值得借鉴的一句话/一段结构 | Figure 1的两张流程图对比：传统"细粒度→粗粒度" vs COUNTMAMBA"粗粒度→细粒度" | 可视化对比是传达范式反转的最有效方式 |

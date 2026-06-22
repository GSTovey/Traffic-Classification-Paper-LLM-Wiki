---
type: paper
title_original: "DEMUX: Boundary-Aware Multi-Scale Traffic Demixing for Multi-Tab Website Fingerprinting"
title_cn: "DEMUX：面向多标签网站指纹的边界感知多尺度流量解混框架"
authors: [Yali Yuan, Yaosheng Liu, Qianqi Niu, Guang Cheng]
year: 2026
venue: "arXiv 2026"
doi: "unknown"
url: "https://arxiv.org/abs/2606"
pdf: "00-inbox/PDFs/2026-arXiv-DEMUX__Boundary-Aware_Multi-Scale_Traffic_Demixing_for_Multi-Tab_Website_Fingerprinting.md"
mineru_md: "02-parsed-markdown/2026-arXiv-DEMUX__Boundary-Aware_Multi-Scale_Traffic_Demixing_for_Multi-Tab_Website_Fingerprinting.md"
status: processed
reading_level: L2
research_area: [website-fingerprinting, encrypted-traffic-analysis, tor-traffic-analysis]
task: [multi-tab-website-fingerprinting, traffic-demixing, multi-label-classification]
method: [overlapping-window-partitioning, multi-scale-cnn, rotary-positional-embedding, transformer-encoder]
dataset: [ARES-closed-world, ARES-open-world, WTF-PAD, FRONT, TrafficSliver]
code: "unknown"
relevance: medium
created: "2026-06-21"
updated: "2026-06-21"
---

# 2026-arXiv DEMUX

## §0 基础信息

| 属性 | 值 |
|------|-----|
| 论文全称 | DEMUX: Boundary-Aware Multi-Scale Traffic Demixing for Multi-Tab Website Fingerprinting |
| 作者 | Yali Yuan, Yaosheng Liu, Qianqi Niu, Guang Cheng |
| 机构 | Southeast University（东南大学） |
| 年份/会议 | 2026 / arXiv |
| 关键词 | website fingerprinting, multi-tab, traffic demixing, overlapping window, multi-scale CNN, RoPE, Transformer |

## §1 一句话总结

提出 DEMUX，一种面向多标签网站指纹攻击的边界感知多尺度流量解混框架，通过重叠窗口边界保留聚合模块（BM）保持突发边界信号完整性、多尺度并行 CNN（MSP-CNN）捕获异构时序模式、两阶段 RoPE 增强 Transformer 实现分散片段的相对时序关联，在封闭世界 5-tab 设置下 P@5 达 0.943、MAP@5 达 0.961，超越最强基线 ARES'25 分别 9.2 和 6.2 个百分点。

## §2 摘要翻译

**原文摘要:**
Website fingerprinting (WF) attacks infer the websites visited by users from encrypted traffic in anonymous networks such as Tor. Existing deep learning methods achieve high accuracy under the single-tab assumption but degrade substantially when users open multiple tabs concurrently, producing interleaved traffic that transforms WF into an implicit demixing problem. We identify three structural requirements for effective multi-tab demixing, namely signal integrity at segment boundaries, multi-scale local modeling, and relative temporal association of dispersed fragments, and show that no prior method satisfies all three simultaneously. We propose DEMUX, a designed framework that addresses these requirements through three tightly coupled components. A Boundary Preserving Aggregation Module employs overlapping window partitioning with joint packet-level and burst-level feature extraction. A Multi-Scale Parallel CNN captures heterogeneous temporal patterns via parallel branches. A two-stage Transformer encoder with Rotary Positional Embedding enables robust cross-window fragment association. The Boundary Preserving Aggregation Module additionally serves as a plug-and-play preprocessor that consistently improves existing baselines without architectural modification. Extensive experiments across closed-world, open-world, defense-augmented, dynamic-tab, and cross-configuration settings demonstrate that DEMUX achieves state-of-the-art performance.

**中文翻译:**
网站指纹（WF）攻击通过匿名网络（如 Tor）中的加密流量推断用户访问的网站。现有深度学习方法在单标签假设下取得高精度，但当用户同时打开多个标签页时性能显著下降，产生的交织流量将 WF 转变为隐式解混问题。我们识别出有效多标签解混的三个结构性要求——分段边界处的信号完整性、多尺度局部建模和分散片段的相对时序关联——并证明现有方法无法同时满足这三个要求。我们提出 DEMUX，一个通过三个紧密耦合组件满足这些要求的设计框架。边界保留聚合模块采用重叠窗口划分联合包级和突发级特征提取。多尺度并行 CNN 通过并行分支捕获异构时序模式。带旋转位置编码的两阶段 Transformer 编码器实现稳健的跨窗口片段关联。边界保留聚合模块还可作为即插即用预处理器，在不修改架构的情况下持续改进现有基线。在封闭世界、开放世界、防御增强、动态标签和跨配置设置下的大量实验表明 DEMUX 达到了最先进的性能。

## §3 方法动机

**痛点:**
- 现有多标签 WF 方法继承自单标签 DF 架构，使用固定不重叠窗口分割，系统性地在相邻窗口间碎片化突发边界转换信号
- 单尺度 CNN 骨干无法同时捕获细粒度突发模式和粗粒度周期性加载节律
- 绝对位置编码将位置索引绑定到叠加混合物而非单个源，在不同标签组合下结构上不适合跨窗口片段关联
- 现有方法（包括最强基线 ARES'25）均无法同时满足上述三个结构性要求

**核心直觉:**
- 多标签 WF 本质上是隐式流量解混问题（implicit traffic demixing），而非单标签分类的简单扩展
- 突发边界（burst boundary）是区分并发源的最具判别力的跨源切换信号
- 不同网站的流量片段在混合轨迹中以异构时间尺度共存，需要多尺度感受野
- 同一网站的指纹证据分散在整个流量中，相对位置关系比绝对位置更有意义

### §3.4 问题发现路径

| 步骤 | 现象观察 | 科学问题推导 | 证据来源 |
|------|---------|-------------|---------|
| 1 | 现有深度学习 WF 方法在单标签下精度超 90%，但多标签下显著退化 | 多标签场景是否构成根本不同的问题结构？ | Abstract: "degrade substantially when users open multiple tabs concurrently" |
| 2 | ARES'25 使用固定不重叠窗口（W=20ms, stride=W），突发边界被分割到相邻窗口 | 固定分割是否系统性破坏最具判别力的边界信号？ | §IV-B: "systematically fragments these transitions across adjacent windows" |
| 3 | 现有方法均使用单尺度 CNN（DF 架构），小核捕获突发模式但对噪声敏感，大核平滑过度 | 单核 CNN 是否无法处理多标签流量的多尺度时序多样性？ | §I: "single-scale CNN backbones cannot accommodate" |
| 4 | Transformer 方法使用绝对/可学习位置编码，但混合流量中片段位置由不可预测的交织决定 | 绝对位置编码是否在结构上不适合解混问题？ | §I: "Absolute positional encodings tie position indices to the superimposed mixture" |
| 5 | 综合以上三个结构性缺陷，提出 R1-R3 三个要求 | 是否存在一个框架能同时满足 R1-R3？ | §I 贡献声明 |

### §3.5 科学假设形成

| 假设类型 | 假设内容 | 验证方式 | 验证结果 |
|---------|---------|---------|---------|
| **核心假设** | 重叠窗口分割 + 多尺度 CNN + RoPE Transformer 的三组件协同设计能有效解决多标签解混 | 完整模型 vs 各组件消融 | Table VII: 完整模型 P@5=0.951，去除 Transformer 暴跌至 0.574 |
| **辅助假设 1** | 重叠窗口保留突发边界信号，对现有方法有即插即用改进效果 | 将 BM 集成到 DF/TMWF/ARES'25 | Figure 5: DF AUC 从 0.780 提升至 0.901，ARES'25 P@5 从 0.869 提升至 0.900 |
| **辅助假设 2** | 多尺度并行 CNN 优于任何单一核大小 | 单核消融实验 | Table VII: 单核 P@5 范围 0.919-0.926，完整 MSP-CNN P@5=0.951 |
| **辅助假设 3** | RoPE 的相对位置编码优于绝对位置编码 | 四种位置编码对比 | Table VI: RoPE AUC=0.998/P@5=0.951 vs Sinusoidal 0.996/0.936 vs Learnable 0.996/0.934 |
| **辅助假设 4** | DEMUX 的优势随标签数量增加而扩大 | 2-tab 到 5-tab 性能对比 | Table II: 与 ARES'25 的 P@5 差距从 2.6pp（2-tab）扩大到 9.2pp（5-tab） |

## §4 方法设计

**整体流程:**
```
输入: 加密流量轨迹 T = {(d_i, t_i)}_{i=1}^N

Stage 1: 边界保留聚合模块 (BM)
  T → 重叠窗口划分 (W=20ms, Δ=10ms, 50% overlap)
  → 每窗口提取包级特征 p_k (方向序列) + 突发级特征 b_k (突发数/均值/方差/间隔)
  → 拼接为 x_k = [p_k; b_k] ∈ R^C
  → 输出序列 X ∈ R^{L×C}

Stage 2: 多尺度并行 CNN (MSP-CNN)
  X → Branch 1 (k=3): 细粒度突发模式
    → Branch 2 (k=5): 中间尺度结构
    → Branch 3 (k=7): 粗粒度周期行为
  → 各分支 RCB 残差卷积块
  → 通道拼接 H^cat ∈ R^{L'×3d_c}
  → 逐点卷积融合压缩 H ∈ R^{L'×d}

Stage 3: 全局关联模块 (GA)
  H → Stage 1 Transformer (L_1=2层, RoPE 位置编码)
    → 逐点投影扩展 (d=256 → d'=384)
    → Stage 2 Transformer (L_2=2层, 标准编码)
  → 上投影池化 (384→1024) + 均值池化
  → MLP 分类头 + sigmoid
  → 多标签预测 ŷ ∈ [0,1]^M

训练: 端到端二元交叉熵损失
```

**核心模块:**

1. **边界保留聚合模块 (BM)**:
   - 重叠窗口划分：长度 W=20ms，步长 Δ=10ms，50% 重叠率，每个点被 r=2 个连续窗口覆盖
   - 窗口数公式：L = floor((T-W)/Δ) + 1
   - 包级特征 p_k：窗口内包方向序列 {+1, -1}
   - 突发级特征 b_k：突发计数、平均突发大小、突发大小方差、平均突发间隔
   - 拼接为统一窗口特征向量 x_k ∈ R^C, C = C_p + C_b = 8
   - 即插即用：可替换任何依赖时序或突发特征的 WF 管道的聚合阶段

2. **多尺度并行 CNN (MSP-CNN)**:
   - B=3 个独立卷积分支，核大小 k_i ∈ {3, 5, 7}
   - 每分支由堆叠的残差 1D 卷积块 (RCB) 组成：RCB_k(z) = BN(σ(Conv_k(z))) + z
   - 通道递进：8→32→64→128→256，池化 kernel/stride = 8/4 × 4 阶段
   - 三分支输出拼接 H^cat ∈ R^{L'×768}
   - 逐点卷积 (1×1 Conv) 融合压缩：768→256

3. **全局关联模块 (GA)**:
   - Stage 1: 2 层 Transformer 编码器，8 头，维度 256，FFN 维度 1024
   - RoPE 位置编码：注意力分数仅依赖相对位移 (m-n)，θ_j = 10000^{-2j/d}
   - 逐点投影扩展：256→384
   - Stage 2: 2 层标准 Transformer 编码器，8 头，维度 384，FFN 维度 1536
   - 分类头：上投影 (384→1024) + 均值池化 + MLP + sigmoid

**优缺点:**
- (+) 首个从解混视角设计的多标签 WF 框架，三组件分别对应三个结构性要求
- (+) BM 即插即用，对 DF/TMWF/ARES'25 均有显著改进
- (+) 随标签数增加优势扩大，说明架构设计与问题结构对齐
- (+) 在防御场景（TrafficSliver）下表现稳健
- (+) 收敛快：epoch 40 已超越所有基线
- (-) 被动威胁模型，未考虑主动攻击者
- (-) 防御评估仅限 2-tab 合成数据集
- (-) 未开源代码（截至论文发表时）

### §4.4 公式、算法和机制解释

#### 4.4.1 重叠窗口划分机制

**窗口覆盖保证**（论文 Eq.1）: 给定轨迹总时长 T，窗口长度 W 和步长 Δ < W，窗口数为：

$$L = \left\lfloor \frac{T - W}{\Delta} \right\rfloor + 1$$

**重叠保证**: 由于 Δ < W，轨迹中每个点被 r = ceil(W/Δ) 个连续窗口覆盖。在实现中 W=20ms、Δ=10ms，r=2。这意味着每个突发边界在至少一个窗口中被完整包含，且两侧有足够上下文。

**物理解释**: 固定不重叠分割（stride=W）的问题在于突发边界可能恰好落在窗口边缘，被分割为两个上下文孤立的半段。重叠分割通过确保每个边界点在某个窗口内部被完整捕获来解决这个问题。这类似于图像处理中重叠 patch 策略保留边缘信息的思想。

#### 4.4.2 多尺度并行卷积的残差块

**残差卷积块**（论文 Eq.5）:

$$\text{RCB}_k(\mathbf{z}) = \text{BN}(\sigma(\text{Conv}_k(\mathbf{z}))) + \mathbf{z}$$

其中 Conv_k 是核大小为 k 的 1D 卷积，σ 是激活函数，BN 是批归一化。残差连接使每个分支能选择性地放大尺度特定模式，而不冗余地重新学习共享的低级统计量。

**多尺度融合**（论文 Eq.6-7）: 三分支输出沿通道维度拼接后通过逐点卷积压缩：

$$\mathbf{H}^{\text{cat}} = [\mathbf{H}_1 \| \mathbf{H}_2 \| \mathbf{H}_3] \in \mathbb{R}^{L' \times 3d_c}$$

$$\mathbf{H} = \text{PWConv}(\mathbf{H}^{\text{cat}}) \in \mathbb{R}^{L' \times d}$$

逐点卷积（1×1 卷积）仅在通道维度操作，执行跨尺度特征交互和降维（768→256），不改变时序结构。

#### 4.4.3 旋转位置编码 (RoPE)

**核心机制**（论文 Eq.11-12）: 对位置 m 的第 j 个二维子空间，旋转角度为 mθ_j，其中 θ_j = 10000^{-2j/d}：

$$\tilde{\mathbf{Q}}^{(\ell)} = \text{RoPE}(\mathbf{Q}^{(\ell)}), \quad \tilde{\mathbf{K}}^{(\ell)} = \text{RoPE}(\mathbf{K}^{(\ell)})$$

**关键性质**: 结果注意力分数仅依赖相对位移：

$$\langle \tilde{\mathbf{Q}}_m^{(\ell)}, \tilde{\mathbf{K}}_n^{(\ell)} \rangle = f(m-n)$$

**物理解释**: 在多标签流量中，同一网站的片段位置由不可预测的交织决定，绝对位置索引不可靠。RoPE 使注意力分数反映窗口间的相对时序距离，使模型能跨混合轨迹关联来自同一网站的片段，无论其绝对位置如何。这直接解决 R3 要求。

#### 4.4.4 两阶段 Transformer 设计

**Stage 1**（位置对齐）: L_1=2 层 Transformer + RoPE，建立相对位置对齐。FFN 隐藏维度 4d=1024。

**跨阶段投影**: 逐点投影扩展 d→d'（256→384），增加每 token 表示容量，同时不扰动 Stage 1 编码的相对位置结构。

**Stage 2**（精化编码）: L_2=2 层标准 Transformer（无 RoPE），在扩展特征空间中精化全局关联表示。FFN 隐藏维度 4d'=1536。

**设计理由**: 两阶段解耦使每个阶段专注于各自的职责——Stage 1 建立位置关系，Stage 2 精化语义表示。跨阶段投影作为轻量级瓶颈，防止两个阶段的功能纠缠。

## §5 与其他方法对比

**创新点:**
- 首次将多标签 WF 明确形式化为隐式流量解混问题，识别三个结构性要求 R1-R3
- BM 即插即用模块，可替换任何 WF 管道的聚合阶段
- 多尺度并行 CNN 替代单尺度 DF 骨干
- RoPE 首次引入 WF 领域解决相对位置编码问题

**与 baseline 对比:**

| 方法 | 类型 | 边界保留 | 多尺度建模 | 位置编码 | 多标签原生 |
|------|------|---------|-----------|---------|-----------|
| DF | CNN | 无（固定分割） | 单尺度 | N/A | 否（sigmoid 适配） |
| TMWF | CNN+Transformer | 无 | 单尺度 | 绝对 | 是 |
| ARES'23 | Transformer | 无 | 单尺度 | 可学习 | 是 |
| ARES'25 | Transformer | 无（固定不重叠） | 单窗口多级 | 可学习 | 是 |
| BAPM | Attention | 块划分 | 单尺度 | 绝对 | 是 |
| DEMUX | CNN+Transformer | 重叠窗口 | 多尺度并行 | RoPE 相对 | 是 |

**与 ARES'25 的关键区别:**
- ARES'25 的 Multi-Level Traffic Aggregation 在每个窗口内提取包级+突发级特征，但使用固定不重叠分割
- DEMUX 的 BM 继承了多级特征设计，但将固定分割替换为重叠分割，保留边界信号
- ARES'25 使用可学习位置编码，DEMUX 使用 RoPE 相对位置编码

## §6 实验表现

**数据集:**
- 封闭世界: Alexa Top-100 网站，2-5 tab，每配置 58,000 条轨迹
- 开放世界: 每条 N-tab 轨迹含 N-1 个监控站 + 1 个非监控站（Alexa Top-20,000），每配置 64,000 条轨迹
- 防御: 2-tab 合成数据集，三种防御——WTF-PAD、Front、TrafficSliver
- 动态标签: 混合训练集 60,000 条（2-5 tab 各 15,000），分别评估每个固定标签测试集

**评估指标:**
- AUC: 一对多 ROC 曲线下面积，阈值无关
- P@K: Top-K 预测中正确网站的比例
- MAP@K: 累积前缀精度的均值

**关键结果:**

封闭世界（Table II）:

| 方法 | 2-tab P@2 | 3-tab P@3 | 4-tab P@4 | 5-tab P@5 | 5-tab MAP@5 |
|------|----------|----------|----------|----------|------------|
| ARES'25 | 0.900 | 0.864 | 0.887 | 0.851 | 0.899 |
| DEMUX | 0.926 | 0.917 | 0.931 | 0.943 | 0.961 |
| 差距 | +2.6pp | +5.3pp | +4.4pp | +9.2pp | +6.2pp |

开放世界（Table III）:

| 方法 | 2-tab P@2 | 5-tab P@5 | 5-tab MAP@5 | 5-tab AUC |
|------|----------|----------|------------|----------|
| ARES'25 | 0.879 | 0.869 | 0.911 | 0.988 |
| DEMUX | 0.913 | 0.951 | 0.966 | 0.998 |
| 差距 | +3.4pp | +8.2pp | +5.5pp | +1.0pp |

防御鲁棒性（Table IV, 2-tab）:

| 防御 | 最佳 P@2 | DEMUX P@2 | 次佳 P@2 | DEMUX 优势 |
|------|---------|----------|---------|-----------|
| WTF-PAD | 0.959 (DEMUX) | 0.959 | 0.951 (ARES'25) | +0.8pp |
| Front | 0.962 (DEMUX) | 0.962 | 0.949 (ARES'25) | +1.3pp |
| TrafficSliver | 0.940 (DEMUX) | 0.940 | 0.915 (ARES'25) | +2.5pp |

### §6 消融实验分析

#### 6.1 三组件消融（Table VII, 开放世界 5-tab）

| 变体 | BM | MSP-CNN | GA | P@5 | MAP@5 | 与完整模型差距 |
|------|-----|---------|-----|-----|-------|-------------|
| 完整 DEMUX | √ | √ | √ | 0.951 | 0.966 | — |
| w/o BM | × | √ | √ | 0.876 | 0.907 | -7.5pp / -5.9pp |
| kernel=3 only | √ | × | √ | 0.924 | 0.946 | -2.7pp / -2.0pp |
| kernel=5 only | √ | × | √ | 0.926 | 0.949 | -2.5pp / -1.7pp |
| kernel=7 only | √ | × | √ | 0.919 | 0.943 | -3.2pp / -2.3pp |
| w/o Transformer | √ | √ | × | 0.574 | 0.745 | -37.7pp / -22.1pp |

**关键发现:**
- 移除 Transformer 造成最大退化（P@5 -37.7pp），证明全局关联是多标签解混最关键的能力
- 移除 BM 造成显著退化（P@5 -7.5pp），证明边界保留对解混至关重要
- 三种单核变体性能相近（0.919-0.926），均低于完整 MSP-CNN，证明多尺度设计的必要性
- 三个组件互补：BM 解决 R1，MSP-CNN 解决 R2，Transformer 解决 R3

#### 6.2 位置编码对比（Table VI, 开放世界 5-tab）

| 位置编码 | AUC | P@5 | MAP@5 |
|---------|-----|-----|-------|
| 无 | 0.996 | 0.937 | 0.956 |
| Sinusoidal | 0.996 | 0.936 | 0.955 |
| 可学习 | 0.996 | 0.934 | 0.954 |
| RoPE (DEMUX) | 0.998 | 0.951 | 0.966 |

**关键发现:**
- 无位置编码已具竞争力（AUC=0.996），说明多尺度前端已编码大量局部顺序信息
- 绝对编码（Sinusoidal/可学习）略差于无编码，因绝对位置索引与重叠分割和动态标签组合的变异性不匹配
- RoPE 最优，因其相对位置偏移自然适配跨窗口片段关联需求

#### 6.3 聚合策略对比（Table V, 开放世界 5-tab）

| 聚合策略 | AUC | P@5 | MAP@5 |
|---------|-----|-----|-------|
| 展平 (Flatten) | 0.944 | 0.888 | 0.929 |
| 均值池化 | 0.980 | 0.939 | 0.957 |
| 上投影+均值 (DEMUX) | 0.985 | 0.951 | 0.966 |

#### 6.4 BM 即插即用效果（开放世界 5-tab）

| 基线 | 原始 AUC | +BM AUC | 原始 P@5 | +BM P@5 |
|------|---------|---------|---------|---------|
| DF | 0.780 | 0.901 | 0.315 | 0.545 |
| TMWF | 0.905 | 0.972 | 0.542 | 0.771 |
| ARES'25 | 0.988 | 0.998 | 0.869 | 0.900 |

**关键发现:** BM 对所有基线均有显著改进，改进幅度与基线能力成反比（DF +12.1pp AUC vs ARES'25 +1.0pp），说明 BM 的边界保留效应对较弱基线更关键。

#### 6.5 收敛行为

- 两阶段收敛：epoch 0-40 快速上升（局部模块学习突发模式），epoch 40-260 缓慢精化（Transformer 精化长程依赖）
- Epoch 40 已超越所有基线（AUC=0.989, P@5=0.875），适合计算受限部署
- 饱和于 epoch 120 附近，最终收敛于 epoch 260

## §7 学习与应用

**开源情况:**
- 代码未开源（截至论文发表时）

**可复现性:**
- 数据集来自 ARES'23/ARES'25 公开基准
- 防御数据集使用 TMWF 提供的合成代码构建
- 训练超参数完整列出（Table I）
- 基线使用统一预处理和训练管道重新实现

**迁移价值:**
- BM 即插即用模块可直接应用于任何依赖时序或突发特征的 WF 管道
- 多尺度并行 CNN 设计可推广到其他需要多尺度时序建模的流量分析任务
- RoPE 在 WF 领域的首次引入为后续工作提供了位置编码选择参考
- 解混视角（demixing perspective）为多标签流量分析提供了新的问题框架

## §8 总结

**核心思想:** 将多标签网站指纹从"更难的单标签分类"重新定义为"隐式流量解混"问题，识别三个结构性要求（边界信号完整性 R1、多尺度局部建模 R2、相对时序关联 R3），并通过重叠窗口 BM + 多尺度 MSP-CNN + RoPE Transformer 三组件协同设计满足所有要求。

**快速 Pipeline:**
```
加密流量轨迹
  → 重叠窗口划分 (W=20ms, Δ=10ms)
  → 每窗口: 包级特征 + 突发级特征 → 拼接
  → MSP-CNN: 3 并行分支 (k=3,5,7) + 残差卷积
  → 逐点卷积融合 (768→256)
  → Stage 1 Transformer (RoPE, 2 层) → 投影扩展 (256→384)
  → Stage 2 Transformer (标准, 2 层)
  → 上投影池化 (384→1024) + 均值池化
  → MLP 分类头 + sigmoid → 多标签预测
```

## §9 知识链接

- [[website-fingerprinting]] — 网站指纹攻击与防御
- [[encrypted-traffic-analysis]] — 加密流量分析
- [[survey-website-fingerprinting]] — 网站指纹综述
- [[traffic-representation-learning]] — 流量表示学习
- deep-fingerprinting — DF 架构及其变体
- multi-tab-wf — 多标签网站指纹
- tor-traffic-analysis — Tor 流量分析

## §10 证据记录

| 关键声明 | 证据 | 可信度 |
|---------|------|--------|
| DEMUX 在封闭世界 5-tab 下 P@5=0.943，超越 ARES'25 9.2pp | Table II 数据 | 高 |
| DEMUX 在开放世界 5-tab 下 P@5=0.951 | Table III 数据 | 高 |
| BM 对 DF/TMWF/ARES'25 均有即插即用改进 | Figure 5 数据 | 高 |
| 移除 Transformer 导致 P@5 暴跌至 0.574 | Table VII 消融 | 高 |
| RoPE 优于其他三种位置编码 | Table VI 对比 | 高 |
| 性能优势随标签数增加而扩大 | Table II 2-5tab 趋势 | 高 |
| TrafficSliver 下 DEMUX P@2=0.940，超越次佳 2.5pp | Table IV 数据 | 高 |

## §11 原始资料链接

- PDF: `00-inbox/PDFs/2026-arXiv-DEMUX__Boundary-Aware_Multi-Scale_Traffic_Demixing_for_Multi-Tab_Website_Fingerprinting.pdf`
- MinerU MD: `02-parsed-markdown/2026-arXiv-DEMUX__Boundary-Aware_Multi-Scale_Traffic_Demixing_for_Multi-Tab_Website_Fingerprinting.md`

## §12 后续问题

1. BM 的重叠比例（当前 50%）是否是最优？更大重叠是否带来更多改进，还是收益递减？
2. 在主动攻击者模型下（可注入探测包或操纵时序），DEMUX 的解混能力是否仍有效？
3. 防御评估仅限 2-tab 合成数据集，在更高标签数的防御场景下表现如何？
4. RoPE 的 base（当前 10000）对不同标签数设置是否需要调整？
5. 解混视角是否可推广到其他流量分析场景（如加密流量分类中的多应用并发）？
6. BM 与其他流量表示方法（如 TAM 矩阵、burst 序列）的组合效果如何？
7. 两阶段 Transformer 的 Stage 1/Stage 2 层数比（当前 2:2）是否最优？

---
type: paper
title_original: "Robust Multi-tab Website Fingerprinting Attacks in the Wild"
title_cn: "野外环境中鲁棒的多标签网站指纹攻击"
authors: [Xinhao Deng, Qilei Yin, Zhuotao Liu, Xiyuan Zhao, Qi Li, Mingwei Xu, Ke Xu, Jianping Wu]
year: 2023
venue: "S&P"
doi: "unknown"
url: "unknown"
pdf: "00-inbox/PDFs/2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild.pdf"
mineru_md: "02-parsed-markdown/2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild.md"
status: processed
reading_level: L2
research_area: [website-fingerprinting, encrypted-traffic-analysis]
task: [multi-tab-website-fingerprinting, tor-traffic-analysis]
method: [transformer, multi-label-classification, sliding-window]
dataset: [500K-multi-tab-sessions, tor-browsing-dataset]
code: "unknown"
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

## §0 基础信息

| 项目 | 内容 |
|------|------|
| 论文全称 | Robust Multi-tab Website Fingerprinting Attacks in the Wild |
| 作者 | Xinhao Deng, Qilei Yin, Zhuotao Liu, Xiyuan Zhao, Qi Li, Mingwei Xu, Ke Xu, Jianping Wu |
| 机构 | 清华大学, 中关村实验室 |
| 发表时间 | 2023 |
| 会议 | IEEE S&P 2023 |

## §1 一句话总结

提出ARES框架，将多标签网站指纹攻击建模为多标签分类问题，利用基于Transformer的Trans-WF模型从多个短流量段中提取局部模式，在50万+多标签Tor浏览会话上实现最佳F1分数0.907，即使打开5个标签页仍能达到0.805 F1分数。

## §2 摘要翻译

**原始摘要：**
Website fingerprinting enables an eavesdropper to determine which websites a user is visiting over an encrypted connection. State-of-the-art website fingerprinting (WF) attacks have demonstrated effectiveness even against Tor-protected network traffic. However, existing WF attacks have critical limitations on accurately identifying websites in multi-tab browsing sessions, where the holistic pattern of individual websites is no longer preserved, and the number of tabs opened by a client is unknown a priori. In this paper, we propose ARES, a novel WF framework natively designed for multi-tab WF attacks. ARES formulates the multi-tab attack as a multi-label classification problem and solves it using a multi-classifier framework. Each classifier, designed based on a novel transformer model, identifies a specific website using its local patterns extracted from multiple traffic segments. We implement a prototype of ARES and extensively evaluate its effectiveness using our large-scale dataset collected over multiple months (by far the largest multi-tab WF dataset studied in academic papers.) The experimental results illustrate that ARES effectively achieves the multi-tab WF attack with the best F1-score of 0.907. Further, ARES remains robust even against various WF defenses.

**中文翻译：**
网站指纹识别使窃听者能够确定用户通过加密连接访问哪些网站。最先进的网站指纹攻击已被证明对Tor保护的网络流量也有效。然而，现有WF攻击在准确识别多标签浏览会话中的网站方面存在关键限制，其中单个网站的整体模式不再保留，且客户端打开的标签数量是未知的。本文提出ARES，一种专为多标签WF攻击设计的新颖框架。ARES将多标签攻击建模为多标签分类问题，并使用多分类器框架解决。每个分类器基于新颖的Transformer模型设计，使用从多个流量段中提取的局部模式识别特定网站。作者实现了ARES原型，并使用数月收集的大规模数据集（迄今为止学术论文中研究的最大多标签WF数据集）广泛评估其有效性。实验结果表明ARES有效地实现了多标签WF攻击，最佳F1分数为0.907。此外，ARES即使面对各种WF防御也保持鲁棒性。

## §3 方法动机

### §3.1 痛点问题
- 现有WF攻击假设单标签浏览，不适用于实际多标签场景
- 多标签浏览会话中，单个网站的整体流量模式被破坏
- 现有方法需要预先知道打开的标签数量
- 现有方法对WF防御机制不鲁棒

### §3.2 核心直觉
- 即使整体模式被破坏，仍可从多个短流量段中提取局部模式
- 网站的HTML元素与局部流量模式相关
- 可以将多标签攻击建模为多标签分类问题

### §3.3 方法动机
- 需要不依赖标签数量的通用多标签WF攻击方法
- Transformer模型可以捕获局部模式之间的相关性
- 多分类器框架可以并行训练和更新

### §3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 现有WF攻击在多标签场景下性能急剧下降；Juarez et al. [9] 证明传统攻击在多标签浏览中失效 | §I, [9] |
| 痛点提炼 | (1) 现有多标签方法需要预先知道标签数量（如MWF固定2标签）；(2) 对WF防御不鲁棒；(3) 标签数越多性能越差——干净流量块越难提取 | §I, Table I |
| 问题转化 | 从"如何分割干净流量块"转化为"如何从混合流量中直接提取局部模式"——从信号分离范式转为多标签分类范式 | §I, §IV-A |
| 文献定位 | 位于WF攻击从单标签到多标签的演进前沿。MWF/CWF/BAPM 均需标签数量先验知识，ARES 首次实现标签数量无关的通用多标签攻击 | Table I |

### §3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 网站的局部流量模式（与HTML元素相关）即使在多标签混合和防御干扰下仍可提取，且可通过自注意力机制建模局部模式间的相关性 | (1) CNN的平移不变性能定位任意位置的局部模式；(2) 自注意力机制能捕获序列内部依赖关系 | 闭世界多标签实验（Table II）、开世界实验（Table III） |
| 辅助假设 1 | Top-m Attention 能过滤噪声（来自其他网站和防御的干扰），比 vanilla attention 更鲁棒 | 噪声流量与目标网站的注意力权重较低，Top-m 选择可过滤 | 防御场景实验（Table IV） |
| 辅助假设 2 | 多分类器框架（one-vs-all）比单一多分类模型更适合动态标签数量场景 | 每个分类器仅判断"是否访问了某网站"，不依赖标签总数 | 动态设置实验（Table V, VI） |

**假设验证结果：**

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 强支撑 | 2标签 F1=0.907，5标签 F1=0.805，比基线提升260.4% | Table II |
| 辅助假设 1 | 支撑 | WTF-PAD下 ARES AUC=0.843，比DF提升19.7% | Table IV |
| 辅助假设 2 | 支撑 | 动态标签设置下 ARES AUC=0.738，比基线平均提升17.1% | Table V |

## §4 方法设计

**整体流程：**

```
输入: 多标签Tor浏览会话（方向序列）
  ↓
Step 1: 方向序列提取
  - 出站包: +1
  - 入站包: -1
  ↓
Step 2: 流量分割（Traffic Division）
  - 使用多个滑动窗口（不同起始位置）
  - 将方向序列分割为多个流量段
  - 保留局部模式的完整性
  ↓
Step 3: 局部模式提取（Local Profiling）
  - 基于CNN的局部特征提取器
  - 多个Conv1d + BatchNorm + ReLU块
  - 残差连接防止梯度消失
  - Dropout防止过拟合
  - MaxPooling保留最具代表性的特征
  ↓
Step 4: 网站识别（Website Identification）
  - 改进的自注意力机制
  - 计算局部特征之间的相关性
  - 每个Trans-WF识别一个特定网站
  ↓
Step 5: 多标签分类
  - N个Trans-WF并行运行（N=监控网站数）
  - Softmax层整合结果
  - 基于阈值输出标签集
  ↓
输出: 访问的网站标签集
```

### §4.4 关键公式推导

**1. 流量分割公式**

给定方向序列 $\mathbf{d}$ 长度为 $l$，使用 $n$ 个滑动窗口（窗口大小 $w$，第 $i$ 个窗口起始位置为 $i$）：

$$S = \{W_1, \dots, W_n\}, \quad W_i = \{\mathbf{d}[i + jw : i + jw + w]\}, \forall j \in [0, \lfloor l/w \rfloor - 1]$$

序列被复制拼接以确保循环分割，所有段长度相同。

**2. Top-m Attention 公式**

$$\text{Attention}^{Top-m}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}(\Gamma(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d}}))\mathbf{V}$$

其中 $\Gamma(\cdot)$ 是逐行 Top-m 选择操作：

$$[\Gamma(A)]_{ij} = \begin{cases} A_{ij}, & A_{ij} \text{ is the top-}m \text{ largest elements in row } j \\ \epsilon, & \text{otherwise} \end{cases}$$

Top-m 选择过滤掉来自其他网站和防御的噪声干扰（噪声的注意力权重较低）。

**3. Multi-head Top-m Attention**

$$head_i = \text{Attention}^{Top-m}(\mathbf{Q}\mathbf{W}_i^Q, \mathbf{K}\mathbf{W}_i^K, \mathbf{V}\mathbf{W}_i^V)$$

$$\Lambda(\mathbf{X}) = \text{Concat}(head_1, \dots, head_h)\mathbf{W}^O$$

其中 $\mathbf{W}_i^Q, \mathbf{W}_i^K, \mathbf{W}_i^V \in \mathbb{R}^{d \times d_h}$，$d_h = d/h$。

**4. 网站识别公式**

$$\Phi(\mathbf{X}) = \text{MLP}(\text{LN}(\mathbf{X} + \text{Dropout}(\Lambda(\mathbf{X}))))$$

$$\text{LN}(\mathbf{X}) = \frac{\mathbf{g}}{\sqrt{\sigma^2 + \epsilon}} \odot (\mathbf{X} - \mu) + \mathbf{b}$$

其中 LN 是 Layer Normalization，$g, b$ 是增益和偏置参数。

**5. 多标签评估公式**

$$\text{P@k} = \frac{1}{k} \sum_{l \in r_k(\hat{y})} \mathbf{y}_l, \quad \text{MAP@k} = \frac{\sum_{i=1}^{k} P@i}{k}$$

其中 $r_k(\hat{y})$ 是预测概率 top-k 的网站集合。

**优势：**
- 不依赖标签数量，适用于动态多标签场景
- 对WF防御鲁棒
- 可并行训练和更新分类器
- 局部模式提取对噪声具有鲁棒性

**局限：**
- 需要大量训练数据
- 计算复杂度较高
- 论文未明确说明在极端防御下的性能

## §5 与其他方法对比

**创新点：**
1. 首次将多标签WF攻击建模为多标签分类问题
2. 设计基于Transformer的Trans-WF模型提取局部模式
3. 使用多分类器框架，不依赖标签数量
4. 构建最大的多标签WF数据集（50万+实例）

### §5.1 本质区别

现有方法（MWF/CWF/BAPM）采用"分割→清洗→分类"范式：先将混合流量分割为干净块，再对每个块分类。这要求预先知道标签数量。ARES 采用"局部模式提取→相关性建模→多标签分类"范式：从多个短流量段中提取局部模式，通过自注意力建模模式间相关性，以 one-vs-all 框架实现标签数量无关的多标签分类。

### §5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 多标签分类建模 | 首次将多标签WF攻击建模为多标签分类问题，one-vs-all框架 | 高 | 是 — 适用于任何多标签序列分类 |
| Trans-WF 模型 | Transformer + CNN 的混合架构，CNN提取局部模式，Transformer建模相关性 | 高 | 是 — 局部模式+全局相关性范式通用 |
| Top-m Attention | 改进的自注意力机制，过滤噪声干扰 | 高 | 是 — 适用于含噪声的序列分析 |
| 滑动窗口分割 | 多个不同起始位置的滑动窗口保留局部模式完整性 | 中 | 是 — 序列分析通用技术 |
| 大规模数据集 | 50万+多标签Tor浏览会话，考虑多种真实世界复杂性 | 中 | 数据集公开可用 |

### §5.4 方法对比表

| 方法 | 多标签 | 通用性 | 鲁棒性 | 实用性 | 2标签F1 | 5标签F1 | WTF-PAD AUC |
|---|---|---|---|---|---|---|---|
| CUMUL | × | × | × | × | 0.315 | 0.158 | - |
| k-FP | × | × | × | × | 0.633 | 0.423 | - |
| AWF | × | × | × | × | 0.419 | 0.210 | 0.583 |
| DF | × | × | √ | × | 0.710 | 0.529 | 0.704 |
| Tik-tok | × | × | √ | × | 0.701 | 0.288 | 0.712 |
| MWF | √ | × | × | × | 0.170 | 0.095 | - |
| CWF | √ | × | × | × | 0.304 | 0.224 | 0.575 |
| BAPM | √ | × | × | × | 0.731 | 0.498 | - |
| **ARES** | **√** | **√** | **√** | **√** | **0.907** | **0.805** | **0.843** |

## §6 实验表现

**数据集：**
- 50万+多标签Tor浏览会话
- 收集时间: 2021年5月-2022年11月
- 考虑多种真实世界复杂性:
  - 多个Tor版本共存
  - 访问子页面（不仅是主页）
  - 不同流量收集位置
  - 真实Tor用户流量

**评估指标：**
- F1分数
- 准确率 (Accuracy)
- 精确率 (Precision)
- 召回率 (Recall)

### §6.5 关键实验结果

**闭世界单标签评估（Table II）：**

| 方法 | 2标签 F1 | 3标签 F1 | 4标签 F1 | 5标签 F1 |
|---|---|---|---|---|
| CUMUL | 0.315 | 0.215 | 0.196 | 0.158 |
| k-FP | 0.633 | 0.567 | 0.519 | 0.423 |
| AWF | 0.419 | 0.287 | 0.219 | 0.210 |
| DF | 0.710 | 0.688 | 0.596 | 0.529 |
| Tik-tok | 0.701 | 0.452 | 0.349 | 0.288 |
| BAPM | 0.731 | 0.649 | 0.615 | 0.498 |
| **ARES** | **0.907** | **0.905** | **0.894** | **0.805** |

**防御场景评估（Table IV, 2标签）：**

| 防御 | ARES AUC | DF AUC | Tik-tok AUC | ARES提升 |
|---|---|---|---|---|
| Random | 0.881 | 0.743 | 0.768 | +14.7% |
| WTF-PAD | 0.843 | 0.704 | 0.712 | +19.7% |
| Front | 0.761 | 0.592 | 0.628 | +21.1% |
| Tamaraw | 0.613 | 0.542 | 0.548 | +11.9% |

**真实用户评估（Figure 13）：**
- ARES Precision: 0.795, AUC: 0.78
- 最佳基线（BAPM）Precision: 0.70, AUC: 0.65

### §6.6 消融实验分析

**1. 标签数量消融（Table II）**

| 标签数 | ARES F1 | 最佳基线 F1 | ARES提升 |
|--------|---------|------------|----------|
| 2 | 0.907 | 0.731 (BAPM) | +24.1% |
| 3 | 0.905 | 0.688 (DF) | +31.5% |
| 4 | 0.894 | 0.615 (BAPM) | +45.4% |
| 5 | 0.805 | 0.529 (DF) | +52.2% |

**关键发现**：标签数越多，ARES 的优势越明显（从 24.1% 提升到 52.2%），因为现有方法在多标签下干净块更难提取，而 ARES 的局部模式方法不受影响。

**2. Top-m Attention 消融**

Top-m Attention 是 ARES 鲁棒性的关键：
- Vanilla Attention：所有注意力权重参与计算，噪声干扰大
- Top-m Attention：仅保留 top-m 权重，过滤噪声
- 在防御场景下，Top-m 的优势尤为显著（WTF-PAD AUC 0.843 vs 约 0.75 估计值）

**3. 滑动窗口数量消融**

多滑动窗口确保局部模式完整性：
- 单窗口：可能切断某些局部模式
- 多窗口（不同起始位置）：即使一个窗口切断模式，其他窗口可能捕获完整模式
- 论文通过 Figure 3 可视化说明了这一机制

**4. 动态设置消融（Table V, VI）**

| 设置 | ARES AUC | 最佳基线 AUC | 提升 |
|------|----------|-------------|------|
| 动态标签数 | 0.738 | 0.661 (Tik-tok) | +11.6% |
| 动态防御 | 0.708 | 0.591 (Tik-tok) | +19.8% |
| 跨标签训练/测试 | 0.713-0.855 | - | 训练/测试标签数不同时性能下降<5% |

**关键发现**：ARES 在动态设置下仍保持有效性，证明 one-vs-all 框架的通用性。

## §7 学习与应用

**开源情况：**
- 论文提到发布大规模多标签数据集，但未明确说明是否开源代码

### §7.2 复现关键步骤

1. 收集多标签Tor浏览流量数据（方向序列 +1/-1）
2. 实现滑动窗口分割模块：多个不同起始位置的窗口，大小 $w$
3. 实现CNN局部特征提取器：L个Block，每Block含2层Conv1d + BN + ReLU + MaxPooling + 残差连接
4. 实现Multi-head Top-m Attention：替换vanilla attention为Top-m选择
5. 构建one-vs-all框架：N个Trans-WF并行，每个识别一个网站
6. 训练：每个Trans-WF独立训练，使用binary cross-entropy损失
7. 排序输出：对所有Trans-WF的输出排序，基于阈值确定标签集

### §7.3 关键超参数

| 超参数 | 值 | 说明 |
|--------|-----|------|
| 滑动窗口大小 $w$ | 见Table VII | 流量段长度 |
| 滑动窗口数量 $n$ | 见Table VII | 不同起始位置的窗口数 |
| CNN Block数 $L$ | - | 局部特征提取深度 |
| Top-m | - | 保留的top注意力权重数 |
| 注意力头数 $h$ | - | Multi-head数量 |
| 阈值 | 验证集调优 | 控制多标签分类的灵敏度 |
| 训练时间 | ~30分钟/Trans-WF | NVIDIA RTX 2080Ti |
| 代码量 | ~1500行 | PyTorch实现 |

### §7.5 研究启发

1. **局部模式 > 整体模式**：在多标签/噪声场景下，从短段提取局部模式比试图恢复整体模式更有效
2. **one-vs-all 框架适合动态类别数**：每个分类器独立判断"是否存在"，不依赖类别总数
3. **Top-m Attention 是噪声过滤的有效机制**：在含噪声的序列分析中，仅保留最强的相关性信号
4. **概念漂移需要定期更新**：建议每月重训练一次（30天后性能下降14.9%）
5. **真实世界复杂性不可忽视**：多Tor版本、子页面浏览、不同观测点都会影响性能

## §8 总结

**核心思想：** 将多标签网站指纹攻击建模为多标签分类问题，利用基于Transformer的Trans-WF模型从多个短流量段中提取局部模式，实现不依赖标签数量的鲁棒攻击。

**快速流程：**
```
多标签Tor浏览会话 → 方向序列提取
    ↓
滑动窗口分割 → CNN局部特征提取 → Transformer自注意力
    ↓
N个Trans-WF并行 → Softmax整合 → 多标签分类结果
```

## §9 知识链接

### 跨论文关联

- [[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]] — DF 是 ARES 的重要基线之一，ARES 在多标签场景下显著优于 DF（2标签 F1 0.907 vs 0.710）
- [[2024-CCS-Robust_and_reliable_early-stage_website_fingerprinting_via_spatial-temporal_features_analysis]] — CCS 2024 WF 工作，与 ARES 同属鲁棒WF攻击方向
- [[2024-CCS-Towards_fine-grained_webpage_fingerprinting_at_scale]] — CCS 2024 细粒度WF，与 ARES 的大规模评估形成呼应

- [[website-fingerprinting]] - 网站指纹识别技术
- [[encrypted-traffic-analysis]] - 加密流量分析方法
- [[transformer]] - Transformer模型
- multi-label-classification - 多标签分类方法
- tor-traffic-analysis - Tor流量分析
- sliding-window - 滑动窗口方法
- local-pattern-extraction - 局部模式提取
- privacy-preservation - 隐私保护研究

## §10 证据记录

| 编号 | 声明 | 证据 | 位置 |
|---|---|---|---|
| E1 | ARES 2标签 F1=0.907，比最佳基线BAPM提升24.1% | Table II | 闭世界实验 |
| E2 | ARES 5标签 F1=0.805，比基线平均提升260.4% | Table II | 多标签实验 |
| E3 | WTF-PAD下 ARES AUC=0.843，比DF提升19.7% | Table IV | 防御实验 |
| E4 | Front下 ARES AUC=0.761，比Tik-tok提升21.1% | Table IV | 防御实验 |
| E5 | 动态标签设置 ARES AUC=0.738，提升17.1% | Table V | 动态设置 |
| E6 | 动态防御设置 ARES AUC=0.708，提升27.3% | Table V | 动态设置 |
| E7 | 跨标签训练/测试性能下降<5% | Table VI | 泛化能力 |
| E8 | 概念漂移：30天后性能下降14.9%，60天后AUC=0.672 | Figure 8 | 时效性 |
| E9 | 真实用户流量 Precision=0.795 | Figure 13 | 实用性验证 |
| E10 | 多Tor版本场景 MAP@2=0.692 | Figure 10 | 真实世界复杂性 |
| E11 | 子页面浏览 AUC=0.731, Precision=0.854 | Figure 11 | 真实世界复杂性 |
| E12 | 不同观测点 MAP@2=0.708 | Figure 12 | 真实世界复杂性 |
| E13 | ARES每增加一个标签F1下降约3.8% | Table II | 可扩展性分析 |
| E14 | ARES训练时间约30分钟/Trans-WF (RTX 2080Ti) | §VI | 计算开销 |
| E15 | 50万+多标签Tor浏览会话数据集 | §V-A | 数据规模 |

## §11 原始资料链接

- PDF: `00-inbox/PDFs/2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild.pdf`
- MinerU MD: `02-parsed-markdown/2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild.md`

## §12 后续问题

1. 滑动窗口大小和数量如何自动优化？
2. 对于更多标签页（如10+）的场景，方法的可扩展性如何？
3. 是否可以结合半监督学习减少训练数据需求？
4. 对于新型WF防御机制的效果如何？
5. 如何设计更有效的防御机制对抗此类攻击？

## §13 写作叙事与故事线分析

### §13.1 主线故事线

1. **问题定位**：现有WF攻击假设单标签浏览，不适用于实际多标签场景；现有多标签方法需要预先知道标签数量且对防御不鲁棒
2. **核心洞察**：即使整体模式被破坏，网站的局部流量模式（与HTML元素相关）仍可从多个短流量段中提取
3. **方法设计**：ARES 将多标签攻击建模为多标签分类问题，one-vs-all 框架 + Trans-WF（CNN局部特征 + Transformer全局相关性）
4. **大规模验证**：50万+数据集，考虑多种真实世界复杂性
5. **结论**：ARES 在准确性、通用性、鲁棒性、实用性四个维度全面超越现有方法

### §13.2 章节叙事功能

| 章节 | 叙事功能 | 关键转折点 |
|------|----------|-----------|
| §I Introduction | 从单标签假设的不现实性出发，指出多标签WF的三个关键限制 | "Most existing multi-tab WF attacks share a similar design architecture" |
| §II Background | 建立WF攻击/防御和多分类/多标签分类的背景知识 | 区分Multi-Class和Multi-Label |
| §III Threat Model | 定义更现实的威胁模型，Table I展示ARES的优势 | 四维对比表 |
| §IV Design | 详细展开ARES的三个模块 | Top-m Attention公式是技术深度的关键体现 |
| §V Evaluation | 多维度大规模实验验证 | Table II（F1=0.907）是全文高潮 |
| §VI Discussion | 讨论极端多标签、训练优化、对抗防御 | 诚实面对局限 |

### §13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 |
|----------|----------|----------|
| 场景Gap | 现有方法假设单标签浏览 | Juarez et al. [9]的实证研究 |
| 方法Gap | 现有多标签方法需要标签数量先验知识 | Table I的四维对比 |
| 鲁棒性Gap | 现有方法对WF防御不鲁棒 | Table IV的防御实验 |
| 实用性Gap | 现有方法未考虑真实世界复杂性 | §V-H的多维度复杂性实验 |

### §13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|----------|----------|-------------|
| 闭世界多标签（Table II） | 证明核心方法的有效性 | 直接验证假设 |
| 开世界（Table III） | 证明方法在未知网站集下的泛化 | 应对"闭世界不现实"批评 |
| 防御场景（Table IV） | 证明Top-m Attention的鲁棒性 | 关键差异化优势 |
| 动态设置（Table V, VI） | 证明one-vs-all框架的通用性 | 应对"需要先验知识"批评 |
| 概念漂移（Figure 8） | 评估方法的时效性 | 实用性考量 |
| 真实用户（Figure 13） | 证明方法在真实流量上的有效性 | 最终实用性验证 |

### §13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|------|----------|-----------------|
| 问题定义 | Table I四维对比，清晰展示所有现有方法的不足 | 表格式Gap声明比文字更直观 |
| 方法设计 | 从问题建模（多标签分类）到架构设计（one-vs-all）到核心模型（Trans-WF）逐步展开 | 先建立问题形式化，再展开技术细节 |
| 实验组织 | 从闭世界→开世界→防御→动态→概念漂移→真实用户，逐步推向真实场景 | 每个实验对应一个质疑 |
| 局限性处理 | §VI Discussion 主动讨论极端多标签、训练优化、对抗防御 | 提前回应审稿人质疑 |
| 数据集贡献 | 强调50万+数据集是"by far the largest" | 数据集本身是重要贡献 |

---
type: paper
title_original: "Towards Fine-Grained Webpage Fingerprinting at Scale"
title_cn: "面向大规模细粒度网页指纹攻击"
authors:
  - Xiyuan Zhao
  - Xinhao Deng
  - Qi Li
  - Yunpeng Liu
  - Zhuotao Liu
  - Kun Sun
  - Ke Xu
year: 2024
venue: "CCS"
doi: "10.1145/3658644.3690211"
url: ""
pdf: "00-inbox/PDFs/2024-CCS-Towards_fine-grained_webpage_fingerprinting_at_scale.pdf"
mineru_md: "02-parsed-markdown/2024-CCS-Towards_fine-grained_webpage_fingerprinting_at_scale.md"
status: processed
reading_level: L2
research_area:
  - website-fingerprinting
  - traffic-classification
  - privacy-attack
task:
  - webpage-fingerprinting
  - multi-tab-identification
  - fine-grained-traffic-classification
method:
  - metric-learning
  - multi-label-classification
  - data-augmentation
  - proxy-based-loss
  - sample-based-loss
  - k-NN-classifier
dataset:
  - Alexa-1000-webpages
  - unmonitored-9000-webpages
code: "https://github.com/OscarWPF/Oscar"
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

# Oscar: 面向大规模细粒度网页指纹攻击

## 0. 基础信息

| 字段 | 内容 |
|------|------|
| 论文全称 | Towards Fine-Grained Webpage Fingerprinting at Scale |
| 作者 | Xiyuan Zhao, Xinhao Deng, Qi Li, Yunpeng Liu, Zhuotao Liu, Kun Sun, Ke Xu |
| 机构 | 清华大学 INSC & BNRist; 中关村实验室; George Mason University |
| 发表年份 | 2024 |
| 会议/期刊 | CCS 2024 |
| 关键词 | Webpage Fingerprinting, Tor, Privacy, Multi-label Metric Learning, Data Augmentation |
| 代码 | https://github.com/OscarWPF/Oscar |

## 1. 一句话总结

提出 Oscar，一种基于多标签度量学习的大规模细粒度网页指纹攻击框架，能够在多标签（多 tab）场景下从混淆流量中识别不同网页，包括同一网站的不同子页面，Recall@5 相比现有攻击平均提升 88.6%，首次将监控网页规模扩展到 1000 个。

## 2. 摘要翻译

**原文：**
Website Fingerprinting (WF) attacks can effectively identify the websites visited by Tor clients via analyzing encrypted traffic patterns. Existing attacks focus on identifying different websites, but their accuracy dramatically decreases when applied to identify fine-grained webpages, especially when distinguishing among different subpages of the same website. WebPage Fingerprinting (WPF) attacks face the challenges of highly similar traffic patterns and a much larger scale of webpages. Furthermore, clients often visit multiple webpages concurrently, increasing the difficulty of extracting the traffic patterns of each webpage from the obfuscated traffic. In this paper, we propose Oscar, a WPF attack based on multi-label metric learning that identifies different webpages from obfuscated traffic by transforming the feature space. Oscar can extract the subtle differences among various webpages, even those with similar traffic patterns. In particular, Oscar combines proxy-based and sample-based metric learning losses to extract webpage features from obfuscated traffic and identify multiple webpages. We prototype Oscar and evaluate its performance using traffic collected from 1,000 monitored webpages and over 9,000 unmonitored webpages in the real world. Oscar demonstrates an 88.6% improvement in the multi-label metric Recall@5 compared to the state-of-the-art attacks.

**中文翻译：**
网站指纹（WF）攻击可以通过分析加密流量模式有效识别 Tor 客户端访问的网站。现有攻击专注于识别不同网站，但当应用于识别细粒度网页时，其准确率急剧下降，特别是区分同一网站的不同子页面时。网页指纹（WPF）攻击面临高度相似的流量模式和更大规模网页的挑战。此外，客户端经常同时访问多个网页，增加了从混淆流量中提取每个网页流量模式的难度。本文提出 Oscar，一种基于多标签度量学习的 WPF 攻击，通过变换特征空间从混淆流量中识别不同网页。Oscar 可以提取各种网页之间的细微差异，即使是流量模式相似的网页。具体而言，Oscar 结合基于代理和基于样本的度量学习损失，从混淆流量中提取网页特征并识别多个网页。我们原型化了 Oscar 并使用从 1000 个监控网页和超过 9000 个非监控网页收集的真实流量评估其性能。Oscar 在多标签度量 Recall@5 上相比现有攻击平均提升 88.6%。

## 3. 方法动机（Motivation）

### 3.1 问题背景与痛点

- **网站指纹 vs 网页指纹**：现有 WF 攻击专注于识别不同网站，但当应用于细粒度网页识别时性能急剧下降
- **高相似性挑战**：同一网站的不同网页共享相似布局，导致流量模式高度相似，难以在原始特征空间中区分
- **多标签（多 tab）场景**：客户端通常同时访问多个网页，导致流量混淆，提取单个网页的模式更加困难
- **大规模网页监控**：网页规模约为网站的 50 倍，现有方法难以扩展到数千个监控网页
- **类崩溃问题**：在多标签场景下，基于度量学习的方法容易出现类崩溃（所有网页流量聚集到一点）

### 3.2 核心直觉

- **细微差异存在**：即使同一网站的不同网页共享相似布局，其内容和资源仍存在差异，导致局部流量模式的细微变化
- **度量学习变换**：通过度量学习变换特征空间，可以将不同网页的流量分离，在新特征空间中提取细微差异
- **多标签度量学习**：结合基于代理和基于样本的损失，解决多标签场景下的类崩溃问题

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|------|------|----------|
| 现象观察 | 现有 WF 攻击（DF 98% 准确率）应用于网页识别时性能急剧下降；同一网站不同子页面流量模式高度相似 | §1, §2.1 |
| 痛点提炼 | (1) 网页流量相似性高，原始特征空间难以区分；(2) 多标签（多 tab）场景导致流量混淆；(3) 网页规模约为网站 50 倍，现有方法难以扩展；(4) 度量学习在多标签下出现类崩溃 | §1, §2.2 |
| 问题转化 | 能否通过变换特征空间提取网页间细微差异，并在多标签场景下避免类崩溃？ | §4 System Overview |
| 文献定位 | 现有 WPF 攻击（FineWP/BurNet/GAP-WF）仅支持单标签；多标签 WF 攻击（ARES/TMWF）仅针对网站级别 | §2.1, Table 1 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|------|----------|----------|----------|
| 核心假设 | 多标签度量学习（代理+样本损失）能变换特征空间，分离相似网页流量 | 同一网站不同网页内容/资源存在差异 → 局部流量模式不同 | 闭世界实验（§6.2），Recall@5=0.4899 |
| 辅助假设1 | 样本间+样本内数据增强能适应多标签流量多样性 | 多 tab 流量因不同网页组合和动态包序而高度多样 | 消融实验（§6.5），DA+FT+W1 vs FT+W1 |
| 辅助假设2 | 代理损失聚合同类 + 样本损失分离异类可解决类崩溃 | 传统度量学习在多标签下正样本暴增导致类崩溃 | 消融实验（§6.5），combined vs proxy-only vs sample-only |

**假设验证结果：**

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|------|-----------|-------------|------|
| 核心假设 | 支撑 | Recall@5=0.4899 vs 最佳 baseline TMWF=0.3951（+24.0%） | §6.2, Table 4 |
| 辅助假设1 | 支撑 | DA+FT+W1 Recall@5=0.4899 vs FT+W1=0.4511（+8.6%） | §6.5, Table 6 |
| 辅助假设2 | 支撑 | Combined Recall@5=0.4899 vs proxy-only=0.3066 vs sample-only=0.0063 | §6.5, Table 6 |

## 4. 方法设计（Method Design）

### 4.1 整体流程

```
原始 PCAP → Flow 分割 → 方向序列 ds + 时间序列 ts → 数据增强（样本间+样本内）
  → DF-based 特征变换模型 → 代理损失 + 样本损失 → 变换后特征空间
  → 双 k-NN 分类器（代理-样本 + 样本-样本）→ 多标签网页识别
```

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|------|------|----------|------|------|
| Step 1 | 原始 PCAP | 分割 flow，提取方向序列 ds（+1/-1）和时间序列 ts（相对首包间隔） | 样本 x ∈ R^(d_i×2) | 特征提取 |
| Step 2 | 两个样本 (x_i, x_j) | 按时间戳归并两个样本的包序列，标签取并集 y_g = y_i ∪ y_j | 增强样本（样本间） | 适应不同网页组合 |
| Step 3 | 单个样本 x_i | 提取 burst 序列，按交换比率 m_e=5% 随机采样 burst，交换相邻 burst | 增强样本（样本内） | 适应动态包序 |
| Step 4 | 原始+增强样本 | DF-based 模型：4×(1D Conv Block) → Linear → d_o=512 维嵌入 | 变换后特征 | 特征变换 |
| Step 5 | 嵌入特征 + 代理 | 代理损失：正对(cos_sim→1) + 负对(cos_sim < margin→0) | L_proxy | 聚合同类 |
| Step 6 | 嵌入特征 + 样本对 | 样本损失：筛选无重叠标签的样本对，cos_sim > margin 则惩罚 | L_sample | 分离异类 |
| Step 7 | 代理+样本损失 | Loss = L_proxy + β × L_sample (β=4.5) | 总损失 | 训练模型 |
| Step 8 | 测试样本 | 代理 k-NN（b=40 近邻代理）+ 样本 k-NN（b=40 近邻样本），score = score_proxy + θ × score_sample (θ=2) | 多标签预测 | 网页识别 |

### 4.3 模型结构与系统模块

**DF-based 特征变换模型**：

| 层 | 类型 | 参数 | 输出维度 |
|----|------|------|----------|
| Conv Block 1-4 | 1D Conv + BN + ReLU × 2 + MaxPool | kernel 3 | 逐步压缩 |
| Linear | 全连接层 | - | d_o=512 维嵌入 |

**关键设计选择**：
- **DF 架构**：选择 DF 因其在 WF 攻击中达到 98% 准确率，且 CNN 的平移不变性对多标签场景中特征片段位置动态变化很重要
- **替换全连接层**：将 DF 原始的分类全连接层替换为线性层，输出 512 维嵌入
- **代理动态更新**：代理随模型参数一起通过 optimizer 更新，位置不断优化

**数据增强模块**：

| 操作 | 输入 | 算法 | 输出 |
|------|------|------|------|
| 样本间增强 | 两个样本 (ds_i, ts_i), (ds_j, ts_j) | 双指针按时间戳归并包序列，标签取并集 | 新组合样本 |
| 样本内增强 | 单个样本 ds_i | 提取 burst → 按 m_e=5% 采样 → 交换相邻 burst | 包序变化样本 |

### 4.4 公式推导与机制解释

**代理损失（公式 1-4）**：

正 proxy-sample 对（y_ij=1）：
$$L_{pos\_proxy}(x_i, p_j) = 1 - \cos\_sim(x_i, p_j)$$
- **直觉**：样本应靠近其关联代理，cos_sim 趋近 1

负 proxy-sample 对（y_ij=0）：
$$L_{neg\_proxy}(x_i, p_j) = \max(\cos\_sim(x_i, p_j) - margin, 0)$$
- **margin=0.1**：低于 margin 的负对不贡献损失，防止过拟合

总代理损失：
$$L_{proxy} = \frac{L_{all\_pos\_proxy}}{\Theta_{pos\_proxy}} + \frac{L_{all\_neg\_proxy}}{\Theta_{neg\_proxy}}$$
- **除以对数**：避免正负样本数量不平衡

**样本损失（公式 5-7）**：

样本挖掘：筛选 |y_i| > 1 的样本，找 y_i · y_j = 0 的无重叠标签对
$$L_{ir\_sample}(x_i, x_j) = \max(\cos\_sim(x_i, x_j) - margin, 0)$$
$$L_{sample} = \frac{L_{all\_ir\_sample}}{\Theta_{ir\_sample}}$$
- **关键**：仅分离无重叠标签的样本对，大幅减少配对数量

**总损失（公式 8）**：
$$Loss = L_{proxy} + \beta \times L_{sample}$$
- **β=4.5**：赋予样本损失更大权重，增强多标签场景下的分离效果

**k-NN 分类（公式 9-13）**：

代理 k-NN：
$$score\_proxy_j = \frac{1}{\cos\_dis(x_{target}, p_j)}, \quad p_j \in R_{proxy}$$

样本 k-NN：
$$score\_sample_j = \sum_{x_i \in R_{sample} \wedge y_{ij}=1} \frac{1}{\cos\_dis(x_{target}, x_i)}$$

总分：
$$score_j = score\_proxy_j + \theta \times score\_sample_j$$
- **θ=2**：样本分数权重更高，考虑多标签流量多样性
- **阈值 τ=0.3**：高于阈值的标签输出为预测结果

### 4.4 优缺点

**优势：**
- 首次实现多标签（多 tab）场景下的大规模细粒度网页指纹
- 多标签度量学习有效解决类崩溃问题
- 样本间和样本内增强提高泛化能力
- 双 k-NN 分类器提高识别准确性
- 首次收集多标签网页流量数据集

**局限：**
- 仍需大量监控网页的训练数据
- 在极大规模网页（如数万）下性能可能下降
- 依赖于网页间存在细微差异的假设

## 5. 与其他方法对比（Comparison）

### 5.1 与主流方法的本质区别

| 维度 | k-FP/DF (WF) | TF (度量学习) | ARES (多标签 WF) | Oscar |
|------|-------------|--------------|-----------------|-------|
| 识别目标 | 网站级别 | 网站级别 | 网站级别 | 网页级别 |
| 多标签支持 | 否 | 否（类崩溃） | 是（固定 tab 数） | 是（动态 tab 数） |
| 损失函数 | 交叉熵 | Triplet Loss | 交叉熵（多头） | 代理+样本度量学习 |
| 数据增强 | 无/单标签 | 单标签 | 无 | 多标签专用（样本间+样本内） |
| 分类器 | softmax | k-NN | 多头投票 | 双 k-NN（代理+样本） |
| 规模 | ~100 网站 | ~100 网站 | ~95 网站 | 1000 网页 |

### 5.2 Baseline 详细对比

| 方法 | 类型 | 特征 | 优势 | 劣势 vs Oscar |
|------|------|------|------|---------------|
| k-FP | RF | 175 手工特征 | 可解释性强 | 多标签下 Recall@5 仅 0.2331 |
| DF | CNN | 方向序列 | 抗 WTF-PAD | 交叉熵损失无法提取网页细微差异 |
| Tik-Tok | CNN | 方向+时间戳 | 利用时间信息 | 单标签设计，多标签下 Recall@5=0.3313 |
| NetCLR | CNN | 自监督对比 | 动态网络适应 | 单标签预训练与多标签存在 gap |
| BAPM | Attention | 多头注意力 | 多标签（固定 tab） | 固定 5 头，Recall@5=0.2106 |
| TMWF | DETR | 目标检测 | 多标签（动态 tab） | Recall@5=0.3951，无法计算 AP@5 |
| FineWP/GAP-WF | CNN/GNN | 包级别/流级别 | 细粒度特征 | 仅支持单标签，无法处理多 tab 混淆 |
| ARES | Transformer | 多头注意力 | 多标签鲁棒 | 每网站单独分类器，1000 网页不可行 |

**排除的方法**：
- **TF**：单标签样本挖掘，多标签下类崩溃
- **MWF**：仅能识别多标签下第一个网页
- **ARES**：每网站构建独立 Transformer 分类器，计算开销大，无法扩展到 1000 网页

### 5.4 方法对比表

| 方法 | Recall@5 (CW) | AP@5 (CW) | Recall@5 (OW) | 多标签 | 大规模 |
|------|--------------|-----------|--------------|--------|--------|
| k-FP | 0.2331 | - | ~0.25 | 否 | 否 |
| NetCLR | 0.1809 | - | ~0.18 | 否 | 否 |
| DF | 0.3354 | - | ~0.32 | 否 | 否 |
| Tik-Tok | 0.3313 | - | ~0.47 | 否 | 否 |
| BAPM | 0.2106 | - | N/A | 是 | 否 |
| TMWF | 0.3951 | - | N/A | 是 | 否 |
| **Oscar** | **0.4899** | **0.7344** | **~0.48** | **是** | **是** |

**特征变换效果**：1000 网页的流量特征相似度平均降低 52.92%

## 6. 实验表现（Experiments）

### 6.1 数据集

| 数据集 | 描述 | 规模 |
|--------|------|------|
| 监控网页 | 1000 个监控网页 | 1,000 |
| 非监控网页 | 超过 9000 个非监控网页 | 9,000+ |
| 闭世界设置 | 仅监控网页 | - |
| 开放世界设置 | 监控+非监控网页 | - |

**数据集特点**：首个针对每个网页作为独立类别的多标签网页流量数据集，同时访问的网页数量动态变化。

### 6.2 Baseline 方法

- **WF 攻击**：k-FP, DF, Tik-Tok, TF, MWF, BAPM, NetCLR, TMWF, ARES
- **WPF 攻击**：FineWP, BurNet, GAP-WF

### 6.3 评估指标

- Recall@5（多标签度量）
- Precision
- Recall
- F1-score

### 6.4 关键结果

**闭世界设置（1000 监控网页）：**

| 方法 | Recall@5 | vs Oscar |
|------|----------|----------|
| k-FP | 0.2331 | -110.2% |
| NetCLR | 0.1809 | -170.8% |
| DF | 0.3354 | -46.1% |
| Tik-Tok | 0.3313 | -47.9% |
| BAPM | 0.2106 | -132.6% |
| TMWF | 0.3951 | -24.0% |
| **Oscar** | **0.4899** | - |

- Oscar Recall@30 >0.73, AP@5 >0.73，最佳 baseline 约 0.52

**开放世界设置（1000 监控 + 9236 非监控网页）：**
- Oscar Recall@30 约 0.70, AP@5 >0.67
- 平均提升 Recall@30 63.5%, AP@5 72.0%
- 轻微性能下降因非监控网页流量模式多样

**可扩展性（700→1000 网页）：**
- Oscar Recall@5 仅下降 2.76%（0.503→0.4899）
- Oscar AP@5 仅下降 4.41%（0.768→0.734）
- 所有规模下 AP@5 均保持 >0.71

### 6.5 消融实验

| 配置 | CW Recall@5 | CW AP@5 | OW Recall@5 | OW AP@5 |
|------|-------------|---------|-------------|---------|
| 仅 W1（原始特征+k-NN） | 0.0155 | 0.0189 | 0.0238 | 0.0234 |
| FT(combined)+W1 | 0.4511 | 0.6749 | 0.4206 | 0.6272 |
| DA+FT(proxy-only)+W1 | 0.3066 | 0.4450 | 0.2996 | 0.4340 |
| DA+FT(sample-only)+W1 | 0.0063 | 0.0070 | 0.0413 | 0.0826 |
| DA+FT(combined)+W1 (Oscar) | **0.4899** | **0.7344** | **0.4527** | **0.6766** |

**关键发现：**
- 特征变换贡献最大：原始特征 Recall@5=0.0155 → FT(combined) 0.4511（+2810%）
- 数据增强进一步提升：FT 0.4511 → DA+FT 0.4899（+8.6%）
- 代理损失单独 Recall@5=0.3066，样本损失单独仅 0.0063
- 但样本损失与代理损失结合后显著提升（0.3066 → 0.4899），证明分离异类流量的重要性
- 样本损失单独无效因其只能分离不能聚合同类

### 6.6 超参数分析

**损失权重 β**：
- β=0（仅代理损失）→ β=4.5（最优）→ β 更大
- Recall@30 和 AP@5 波动 <0.015，性能稳定
- 较大 β（样本损失权重更高）效果更好，证明多标签下分离异类的重要性

**邻居数量 b**：
- b=10→40→100，Recall@30 轻微上升，AP@5 轻微下降
- 两者均在 0.71-0.77 窄范围内
- 选择 b=40 作为平衡点

## 7. 学习与应用（Learning & Application）

### 7.1 开源情况

- **代码**：https://github.com/OscarWPF/Oscar
- **数据集**：作者发布了首个多标签网页流量数据集
- **可复现性**：提供了完整的代码和数据集

### 7.2 复现关键步骤

1. **数据收集**：115 网站 × 10 子页面 = 1000 监控网页，每组合 10 样本，81,284 样本
2. **开放世界数据**：9,236 非监控网页，每组合 1 样本
3. **特征提取**：方向序列 ds（+1/-1）+ 时间序列 ts，输入维度 d_i=10,000
4. **数据增强**：样本间（双指针时间归并）+ 样本内（burst 交换 m_e=5%）
5. **特征变换**：DF-based 模型，d_o=512 维嵌入
6. **训练**：Loss = L_proxy + 4.5 × L_sample，margin=0.1
7. **识别**：双 k-NN（b=40），score = score_proxy + 2 × score_sample，阈值 τ=0.3

**关键超参数**：d_i=10,000, m_e=5%, margin=0.1, β=4.5, d_o=512, b=40, θ=2, τ=0.3

### 7.3 实际应用场景

- **网页监控**：细粒度监控用户访问的具体子页面（1000+ 网页规模）
- **隐私评估**：评估网页级别隐私保护的有效性，揭示 WF 攻击可深入到子页面级别
- **内容过滤**：基于网页内容的细粒度过滤，区分同一网站不同内容页面
- **多标签流量分析**：处理用户同时打开多个标签页的真实浏览场景
- **Tor 隐私审计**：评估 Tor 匿名性在细粒度网页级别是否足够

### 7.5 对研究的启发

1. **多标签度量学习**：代理损失聚合同类 + 样本损失分离异类的组合策略，可迁移至其他多标签分类任务
2. **类崩溃问题**：传统度量学习在多标签下失效，需要专门设计损失函数
3. **数据增强设计**：应根据流量特性（多标签的组合多样性和包序动态性）设计专用增强
4. **双分类器结合**：代理 k-NN（稳定表征）+ 样本 k-NN（多样本多样性）互补
5. **大规模可扩展性**：k-NN 分类器天然支持大规模类别，无需为每个类别构建独立分类器
6. **网页 vs 网站粒度**：WF 攻击可从网站级深入到网页级，隐私威胁更严重

## 8. 总结（Summary）

### 8.1 核心思想

Oscar 的核心思想是通过多标签度量学习变换特征空间，从混淆的多标签流量中提取不同网页的细微差异。样本间和样本内数据增强提高泛化能力，代理损失和样本损失结合解决类崩溃问题，双 k-NN 分类器实现准确的多标签网页识别。

### 8.2 快速流程图

```
输入：多标签流量样本（多 tab 同时访问）
  ↓
数据增强（样本间组合 + 样本内交换）
  ↓
特征变换（多标签度量学习：代理损失 + 样本损失）
  ↓
网页识别（双 k-NN 分类器：代理-样本 + 样本-样本距离）
  ↓
输出：识别的网页标签（多标签）
```

## 9. 知识链接（Knowledge Links）

- [[website-fingerprinting]]：本文的背景任务，Oscar 是其细粒度扩展
- [[traffic-classification]]：更广泛的任务类别
- [[contrastive-learning]]：度量学习与对比学习密切相关
- [[encrypted-traffic-analysis]]：加密流量分析的应用
- [[few-shot-traffic-learning]]：度量学习在少样本场景中的应用

## 10. 证据记录（Evidence）

| 声明 | 证据 | 来源 |
|------|------|------|
| Recall@5 平均提升 88.6% | 闭世界 1000 网页，与 6 种攻击对比 | §6.2, Table 4 |
| Recall@5=0.4899 | 闭世界，vs TMWF 0.3951, DF 0.3354 | §6.2, Table 4 |
| AP@5=0.7344 | 闭世界，远超其他方法约 0.52 | §6.2, Figure 8 |
| 开放世界 Recall@5 提升 76.7% | 1000 监控 + 9236 非监控网页 | §6.3, Figure 9 |
| 特征相似度降低 52.92% | 1000 网页特征变换前后对比 | §4 System Overview |
| 网页规模约为网站 50 倍 | 文献引用 siteefy.com | §1 |
| 首个多标签网页流量数据集 | 1000 监控 + 9236 非监控，动态标签数 | §6.1, Table 3 |
| 消融：仅特征变换提升 2810% | 原始 Recall@5=0.0155 → FT=0.4511 | §6.5, Table 6 |
| 消融：数据增强额外提升 8.6% | FT=0.4511 → DA+FT=0.4899 | §6.5, Table 6 |
| 消融：样本损失单独无效 | sample-only Recall@5=0.0063 | §6.5, Table 6 |
| 消融：combined 最优 | proxy-only 0.3066 → combined 0.4899 | §6.5, Table 6 |
| 可扩展性：700→1000 网页仅降 2.76% | Recall@5 0.503→0.4899 | §6.4, Figure 10 |
| 多标签下编辑距离随 tab 数增加 | 1 tab=3600, 5 tab=5800 | §5.1, Figure 5(a) |
| 超参数不敏感 | β 和 b 变化下波动 <0.015 | §6.6, Figure 11 |

## 11. 原始资料链接（Source Links）

- **PDF**：`00-inbox/PDFs/2024-CCS-Towards_fine-grained_webpage_fingerprinting_at_scale.pdf`
- **MinerU MD**：`02-parsed-markdown/2024-CCS-Towards_fine-grained_webpage_fingerprinting_at_scale.md`

## 12. 后续问题（Open Questions）

1. **更大规模网页**：在数万甚至数十万监控网页下，Oscar 的可扩展性如何？
2. **动态网页**：对于动态生成内容的网页（如社交媒体 feed），识别准确性如何？
3. **防御机制**：是否存在针对 Oscar 的有效防御方法？
4. **实时识别**：Oscar 的计算复杂度是否满足实时识别需求？
5. **跨网站泛化**：在未见过的网站上，Oscar 的泛化能力如何？

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

从现有 WF 攻击仅关注网站级别且在网页识别上性能急剧下降出发，指出网页指纹面临三大挑战（高相似性、多标签混淆、大规模），提出基于多标签度量学习的 Oscar 框架，通过代理+样本损失变换特征空间，首次实现 1000 网页规模的多标签网页指纹攻击。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|------|----------|----------|----------|
| Abstract | 概述问题-方法-结果 | 全文缩影 | "Recall@5 平均提升 88.6%" |
| §1 Introduction | 建立 WF→WPF 的升级需求 | 问题动机 | 网页流量高相似性 + 多标签 + 大规模三挑战 |
| §2 Background | 定义 WF/WPF/度量学习 | 技术基础 | Table 1 现有方法能力矩阵 |
| §3 Threat Model | 定义攻击者能力和场景 | 约束条件 | 多标签 + 大规模 + 闭/开放世界 |
| §4 System Overview | 展示特征变换效果 | 方法骨架 | 特征相似度降低 52.92% |
| §5 Design | 详细设计三大模块 | 核心贡献 | 代理+样本损失解决类崩溃 |
| §6 Evaluation | 多维度实验验证 | 性能验证 | 消融实验证明各组件贡献 |
| §7 Discussion | 讨论大规模/防御/概念漂移 | 平衡性 | 可扩展性分析 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|----------|----------|----------|------|
| 性能瓶颈 | DF 98% 网站准确率 → 网页识别急剧下降 | 量化对比 | §1 |
| 场景缺失 | 无多标签网页指纹攻击 | Table 1 能力矩阵 | §2.1 |
| 技术缺陷 | 度量学习在多标签下类崩溃 | TF/NetCLR 分析 | §2.2 |
| 规模限制 | 现有攻击仅评估 ~100 网站 | 文献分析 | §1 |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|----------|----------|-------------|
| §6.2 闭世界 | 证明多标签网页识别能力 | 核心能力验证 |
| §6.3 开放世界 | 证明区分监控/非监控能力 | 实用性验证 |
| §6.4 规模实验 | 证明 700→1000 网页可扩展性 | 大规模目标验证 |
| §6.5 消融 | 证明三大模块 + 双损失的贡献 | 方法有效性归因 |
| §6.6 超参数 | 证明参数不敏感 | 鲁棒性验证 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|------|----------|------------------|
| 开篇方式 | 从现有方法的能力矩阵（Table 1）出发 | 用对比表建立 Gap |
| Gap 提出方式 | 三维度递进：高相似性→多标签混淆→大规模 | 挑战层层递进 |
| 方法论证逻辑 | 观察（52.92% 相似度降低）→ 设计 → 验证 | 用数据驱动设计决策 |
| 实验组织逻辑 | 闭世界→开放世界→规模→消融→超参数 | 层层递进验证 |
| 最值得借鉴的一句话结构 | "the similarity of traffic features across different webpages decreases by an average of 52.92% after feature transformation" | 用量化数据证明方法有效性 |

## 14. 跨论文链接（Cross-Paper Links）

- [[2024-CCS-Robust_and_reliable_early-stage_website_fingerprinting_attacks_via_spatial-temporal_distribution_analysis]]：同为 CCS 2024 的 WF 攻击，Holmes 关注早期阶段识别，Oscar 关注细粒度网页识别；两者都使用对比学习/度量学习变换特征空间
- [[2025-AAAI-MIETT__Multi-Instance_Encrypted_Traffic_Transformer_for_Encrypted_Traffic_Classification]]：MIETT 使用 Transformer + 多实例学习，Oscar 使用 CNN + 度量学习；两者都关注流量的层次结构
- [[2026-NDSS-A_Hard-Label_Black-Box_Evasion_Attack_against_ML-based_Malicious_Traffic_Detection_Systems]]：NetMasquerade 是逃逸攻击，Oscar 是 WF 攻击；两者都关注 ML 流量分析系统的实际部署
- **方法关联**：Oscar 的多标签度量学习 → Holmes 的监督对比学习 → MIETT 的 Flow Contrastive Learning，三种方法都通过变换特征空间提升分类性能
- **任务关联**：Oscar（网页级 WPF）+ Holmes（早期 WF）共同推进 WF 攻击的实用性；Oscar 首次将 WF 从网站级扩展到网页级

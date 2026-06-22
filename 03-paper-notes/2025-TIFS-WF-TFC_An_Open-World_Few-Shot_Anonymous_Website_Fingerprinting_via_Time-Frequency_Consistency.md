---
type: paper
title_original: "WF-TFC: An Open-World Few-Shot Anonymous Website Fingerprinting via Time-Frequency Consistency"
title_cn: "WF-TFC：基于时频一致性的开放世界少样本匿名网站指纹攻击"
authors:
  - Xiaolan Zhu
  - Junfeng Wang
  - Wenhan Ge
  - Yizhao Huang
  - Tingting Lu
year: 2025
venue: "IEEE TIFS 2025"
doi: "10.1109/TIFS.2025.3581092"
url: "https://doi.org/10.1109/TIFS.2025.3581092"
pdf: "00-inbox/PDFs/2025-TIFS-WF-TFC_An_Open-World_Few-Shot_Anonymous_Website_Fingerprinting_via_Time-Frequency_Consistency.pdf"
mineru_md: "02-parsed-markdown/2025-TIFS-WF-TFC_An_Open-World_Few-Shot_Anonymous_Website_Fingerprinting_via_Time-Frequency_Consistency.md"
status: processed
reading_level: L2
relevance: medium
dataset:
  - "AWF Dataset (2016, TBB 6.5): AWF100, AWF200, AWF200_gaps, AWF10K-200K"
  - "DS-19 Dataset (2019, TB 8.5a7): 100 monitored + 1000 unmonitored"
  - "Drift90/Drift5000 + authors' newly captured dataset"
code: null
research_area: ["网站指纹", "加密流量分析", "少样本学习"]
task: ["开放世界匿名网站指纹识别", "少样本WF攻击"]
method: ["自监督对比学习", "时频一致性", "DF骨干网络", "FFT频域增强"]
created: "2026-06-21"
updated: "2026-06-21"
---

# WF-TFC: An Open-World Few-Shot Anonymous Website Fingerprinting via Time-Frequency Consistency

## 0. 论文基础信息（表格）

| 项目 | 内容 |
|------|------|
| 论文标题 | WF-TFC: An Open-World Few-Shot Anonymous Website Fingerprinting via Time-Frequency Consistency |
| 作者 | Xiaolan Zhu, Junfeng Wang, Wenhan Ge, Yizhao Huang, Tingting Lu |
| 机构 | 四川大学（国家综合视觉基础科学重点实验室 + 计算机科学学院） |
| 期刊 | IEEE Transactions on Information Forensics and Security (TIFS) 2025 |
| 发表时间 | 2025年6月18日（online），2025年6月26日（current version） |
| DOI | 10.1109/TIFS.2025.3581092 |
| 关键词 | Website fingerprinting, self-supervised contrastive learning, time-frequency consistency, few-shot learning |
| 基金 | 国家自然科学基金 U24B20147 / U2133208；四川省重大科技专项 2024ZHCG0195 / 2024ZDZX0044 / 2024ZYD0269 |

## 1. 一句话总结

**WF-TFC** 是一种面向开放世界少样本场景的匿名网站指纹攻击方法，通过自监督对比学习在预训练阶段对齐时域和频域表征于潜在时频空间中，仅需每网站 5 条 trace 即可在预训练 6 周后的流量上达到 92.62% 准确率（超越 NetCLR 2.12%），在相似但互斥数据集的开放世界场景中 F1 达 87.20%（超越 SOTA 6.12%）。

## 2. 摘要翻译

**原文（摘要核心）：**
While Tor provides strong anonymity, it also facilitates the concealment of malicious activities. As an effective anti-anonymity technique, Website Fingerprinting (WF) enables the inference of which websites a user is visiting. SOTA methods require a large number of labeled traffic and suffer from concept drift due to the dynamic nature of website content and network conditions. This paper presents WF-TFC, an open-world few-shot anonymous WF model via self-supervised contrastive learning and time-frequency consistency. It aligns time- and frequency-based representations in the latent time-frequency space, enhancing the sustained effectiveness of inherent patterns across various websites. With only 5 traces per website, WF-TFC achieves 92.62% accuracy on traces collected six weeks after pre-training, exceeding NetCLR by 2.12%.

**中文翻译：**
Tor 提供强匿名性的同时也被恶意攻击者滥用。网站指纹（WF）作为一种有效的反匿名技术，能推断用户访问的网站。现有 SOTA 方法需要大量标记流量，且因网站内容和网络条件的动态性而面临概念漂移问题。本文提出 WF-TFC，一种基于自监督对比学习和时频一致性的开放世界少样本匿名 WF 模型。它在潜在时频空间中对齐时域和频域表征，增强跨网站固有模式的持续有效性。仅需每网站 5 条 trace，WF-TFC 在预训练 6 周后采集的流量上达到 92.62% 准确率，超越 NetCLR 2.12%。

## 3. 方法动机（为什么提出、现有痛点、核心直觉）

### 现有痛点

1. **概念漂移问题严重**：网站内容和网络条件动态变化导致同一网站的流量分布随时间显著变化。Juarez et al. 发现 KNN 分类器准确率在 10 天内从 80% 降至 30%；Rimmer et al. 观察到 SDAE 分类器在 28 天内从 95% 降至 81%。
2. **大量标注数据需求**：现有深度学习 WF 方法需要大量标记流量和频繁重训练。收集 50 万条 trace 需要单终端资源对抗者 250 天。
3. **i.i.d. 假设不成立**：训练和测试数据独立同分布的假设在开放世界的长期时空动态中不成立。不同 TBB 版本可降低准确率超过 50%，不同配置和网络位置引入高达 11.7% 和近 60% 的变化。
4. **现有少样本方法的局限**：已有少样本 WF 研究（TF、TLFA、NetCLR）仅考虑时域分析，缺乏更有效的预训练策略，导致分类性能次优。

### 核心直觉

- **时域分析**捕捉流量的瞬时变化和局部特征（包发送频率、时序、延迟），与特定网站活动模式密切相关。
- **频域分析**揭示流量中不可直接观测的行为（周期性、突发性、频谱特性），提供互补的全局视角。
- **时频一致性**：同一原始 trace 经时域编码器和频域编码器后产生的嵌入应在潜在空间中更接近，这种跨域对齐能增强模型学习联合表征的能力，提升在未见网络条件下的泛化性。
- 自监督对比学习可在无标签条件下从大量历史 trace 中学习鲁棒表征，减少对大量标注数据的依赖。

### 为什么提出 WF-TFC

已有少样本 WF 方法（如 NetCLR）仅在时域进行数据增强和对比学习预训练，未利用频域信息。信号处理理论表明时域和频域提供互补视角，将两者对齐应能捕获更鲁棒的固有流量模式，从而在开放世界的少样本场景中实现更好的知识迁移和数据兼容性。

## 4. 方法设计（整体流程、详细 Pipeline）

### 整体流程

WF-TFC 包含两个阶段：**任务无关预训练**（task-agnostic pre-training）和**任务特定微调**（task-specific fine-tuning）。预训练阶段通过自监督学习在无标签数据上学习鲁棒的通用表征；微调阶段用少量标记 trace 将预训练模型适配到特定少样本下游任务。

### 详细 Pipeline 表格

| 阶段 | 操作 | 详细说明 |
|------|------|----------|
| 输入表示 | packet direction 序列 | outgoing = +1, incoming = -1；截断/填充至固定长度 5000 |
| 骨干网络 | DF 网络 | 沿用 Sirinam et al. 2018 的 Deep Fingerprinting 架构 |
| **预训练阶段** | | |
| 时域增强 | Burst 级修改 | 提取 burst 序列，按概率增减 incoming/outgoing burst 大小（Algorithm 1） |
| 频域增强 | FFT + 频率分量扰动 | FFT 计算幅度谱 -> 对数变换 -> 随机移除或增加频率分量（Algorithm 2） |
| 时域编码器 G_T | DF 网络提取时域嵌入 | 原始 trace 和增强 trace 各产生高维表征 h_i^T |
| 频域编码器 G_F | DF 网络提取频域嵌入 | 频域表示和增强频域表示各产生高维表征 h_i^F |
| 时域投影器 R_T | 全连接层降维 | 将 h_i^T 映射到低维空间 z_i^T |
| 频域投影器 R_F | 全连接层降维 | 将 h_i^F 映射到低维空间 z_i^F |
| 对比损失 L_T | 时域对比损失 | 正对：(x_i^T, ~x_i^T)；负对：(x_i^T, x_j^T) |
| 对比损失 L_F | 频域对比损失 | 正对：(x_i^F, ~x_i^F)；负对：(x_i^F, x_j^F) |
| 一致性损失 L_C | 时频一致性损失 | 正对：(z_i^T, z_i^F)；负对：(z_i^T, z_j^F) |
| 总损失 | L_i = lambda(L_T + L_F) + (1-lambda)L_C | lambda=0.8 控制时频损失与一致性损失的相对重要性 |
| **微调阶段** | | |
| 投影层替换 | 替换为两层全连接层 | 最后一层输出每个网站的概率 |
| 训练/验证/测试 | N={1,2,5,10,15,20} trace/网站 | 验证集 20 条，测试集 50 条；五次随机测试取均值 |

### 关键公式解释

**1. 时域对比损失 (Eq. 2)**

$$L_{T,i} = -\log \frac{\exp(\text{sim}(z_i^T, \tilde{z}_i^T)/\tau)}{\sum_{x_j \in D^{pre}} \mathbb{1}_{[i \neq j]} \exp(\text{sim}(z_i^T, R_T(G_T(x_j^T)))/\tau)}$$

使用余弦相似度，温度参数 tau=0.5 控制相似度分布的锐度。正对是同一 trace 的原始和增强版本，负对是 batch 内其他样本。

**2. 时频一致性损失 (Eq. 13)**

$$L_{C,i} = -\log \frac{\exp(\text{sim}(z_i^T, z_i^F)/\tau)}{\sum_{x_j \in D^{pre}} \mathbb{1}_{[i \neq j]} \exp(\text{sim}(z_i^T, R_F(G_F(x_j^F)))/\tau)}$$

将同一原始 trace 的时域嵌入 z_i^T 和频域嵌入 z_i^F 作为正对拉近，与其他样本的频域嵌入作为负对推远。不考虑增强版本之间的对齐（~z_i^T 和 ~z_i^F），因为增强后跨域一致性可能不被保持。

**3. 频域变换 (Eq. 3-11)**

通过 FFT 将时域信号变换为频域，取模后取前半部分（DFT 对称性），再做对数变换 L_ik = ln(p_ik + 1) / C 确保数值稳定性。

### 关键设计决策

- **Burst 级增强 vs 包级增强**：基于用户-服务器交互特性，incoming 流量（服务器响应）远多于 outgoing（用户请求），且两者均动态变化。通过修改 burst 大小模拟不同网络条件下的流量变化。
- **频域增强策略**：随机移除或增加频率分量，模拟不同网络环境下流量周期性和突发性的变化。
- **不增强版本的跨域对齐**：增强可能破坏时频一致性，因此 L_C 仅对齐原始 trace 的时频嵌入。
- **lambda=0.8**：时域和频域对比损失权重之和为 0.8，一致性损失为 0.2，说明域内对比学习是主导目标。

### 优势

1. **首次在 WF 中引入频域分析和时频一致性**，为少样本 WF 提供了新的表征学习范式。
2. **无标签预训练**：任务无关预训练不需要任何标注数据，仅需少量标注数据进行微调。
3. **对概念漂移的鲁棒性**：时频一致性作为一种不变性约束，桥接了预训练数据和微调数据之间的分布差异。
4. **在极端少样本场景（1-shot、2-shot）下仍具竞争力**。

### 不足

1. **频域编码器单独使用时性能较差**（5-shot: 53.02% vs 时域 91.63%），说明频域特征单独不足以支撑 WF 任务，必须与时域结合。
2. **对重防御（TAMARAW）效果有限**：20-shot 仅达 11.33%，虽优于基线但仍远低于实用水平。
3. **预训练仍需大量无标签流量**（AWF100，每网站 2500 条），获取成本仍然较高。
4. **在 1-shot 场景下频率域优势不明显**：单条 trace 可能无法捕获足够的时序信息，频域特征贡献有限。
5. **在更现实的数据集（Drift90/Drift5000 + 新采集数据）上性能下降明显**：10-shot F1 从 ~97% 降至 ~82-89%，说明对预训练数据分布的依赖仍然较大。

## 5. 实验设计

### 数据集表格

| 数据集 | 采集时间 | TBB 版本 | 规模 | 用途 |
|--------|----------|----------|------|------|
| AWF100 | 2016 | TBB 6.5 | 100 网站 x 2500 trace | 预训练 |
| AWF200-AWF100 | 2016 | TBB 6.5 | 100 网站 | 闭世界微调（相似分布） |
| AWF200_gaps | 2016+3d/10d/2w/4w/6w | TBB 6.5 | 200 网站 | 概念漂移评估 |
| DS-19_cw | 2019 | TB 8.5a7 | 100 网站 x 100 trace | 闭世界微调（不同分布） |
| DS-19_ow | 2019 | TB 8.5a7 | 1000 非监控网站 | 开放世界 |
| DS-19_WTF-PAD/FRONT/TAMARAW | 2019 | TB 8.5a7 | 带防御数据集 | 防御鲁棒性评估 |
| AWF10K-200K | 2016 | TBB 6.5 | 10K-200K 非监控网站 | 大规模开放世界 |
| Drift90/Drift5000 | 2021+ | 多版本 | 93 监控 + 5000 非监控 | 现实场景评估 |
| 新采集数据 | 2024+ | 最新 | 20 监控 + 1600 非监控 | 现实场景评估 |

### 基线方法

| 方法 | 类型 | 关键特点 |
|------|------|----------|
| k-FP | 手工特征 | Random Forest + KNN |
| AWF | 深度学习 | SDAE |
| DF | 深度学习 | CNN（全监督） |
| WF-Transformer | 深度学习 | Transformer 时序特征 |
| TF | 少样本 | Triplet Network + N-shot |
| Var-CNN | 少样本 | ResNet-18 + 手工特征 |
| TLFA | 少样本 | 大量标记数据预训练 + 微调 |
| NetCLR | 少样本 | 网络 trace 增强 + 对比学习（SOTA） |

### 评估指标

- **闭世界**：Accuracy（正确分类监控网站的比例）
- **开放世界**：F1 score（precision 和 recall 的调和均值）

## 6. 核心结果

### 闭世界结果

| 场景 | N-shot | WF-TFC | NetCLR (SOTA) | DF (全监督) | 提升 |
|------|--------|--------|---------------|-------------|------|
| 相似互斥数据集 | 5 | 95.02% | 90.45% | 74.98% | +4.57% |
| 相似互斥数据集 | 10 | 97.10% | 95.43% | 85.46% | +1.67% |
| 不同分布数据集 | 5 | 90.77% | 87.57% | 74.03% | +3.20% |
| 不同分布数据集 | 20 | 96.06% | 94.88% | 93.00% | +1.18% |

### 概念漂移结果（5-shot，6 周间隔）

| 方法 | 3 天 | 6 周 | 下降幅度 |
|------|------|------|----------|
| WF-TFC | 95.86% | 92.62% | -3.24% |
| NetCLR | 93.31% | 89.11% | -4.20% |
| TLFA | 95.91% | 90.50% | -5.41% |
| DF | 67.25% | 61.70% | -5.55% |

### 开放世界结果（相似互斥数据集）

| 调优方向 | N-shot | WF-TFC | NetCLR | DF | 提升 |
|----------|--------|--------|--------|-----|------|
| Precision | 5 | 81.54% F1 | 36.43% F1 | 63.32% F1 | +18.22% vs DF |
| Precision | 10 | 89.77% F1 | 74.38% F1 | 81.97% F1 | +7.80% |
| Recall | 5 | 87.20% F1 | 81.08% F1 | 74.80% F1 | +6.12% |

### 开放世界结果（分布偏移数据集，DS-19）

| 调优方向 | N-shot | WF-TFC | NetCLR | TF | 提升 |
|----------|--------|--------|--------|-----|------|
| Precision | 5 | 84.62% F1 | 46.32% F1 | 82.43% F1 | +2.19% vs TF |
| Recall | 5 | 96.81% F1 | 90.64% F1 | 82.43% F1 | +6.17% vs NetCLR |

### 防御鲁棒性（10-shot）

| 防御 | WF-TFC | NetCLR | DF |
|------|--------|--------|-----|
| WTF-PAD | 81.06% | 70.40% | 67.88% |
| FRONT | 17.76% | 10.30% | 13.66% |
| TAMARAW | 9.64% | 9.53% | 7.40% |

### 消融实验结果（闭世界，AWF200-AWF100）

| 模型变体 | 5-shot | 10-shot |
|----------|--------|---------|
| 仅时域（去掉 L_F 和 L_C） | 70.61% | 91.63% |
| 仅频域（去掉 L_T 和 L_C） | 43.99% | 53.02% |
| 无一致性（去掉 L_C） | 73.84% | 93.36% |
| 无 incoming 增强 | 93.00% | 96.31% |
| 无 outgoing 增强 | 91.00% | 95.13% |
| WF-TFC（完整） | **95.02%** | **97.10%** |

## 7. 论文贡献点

1. **首次在 WF 中引入频域分析和时频一致性预训练**：在潜在时频空间中对齐时域和频域表征，增强跨网站固有模式的泛化性。
2. **设计了面向网络流量的时频域数据增强策略**：burst 级时域增强和 FFT 频率分量扰动，模拟动态网站内容和多样网络环境的变化。
3. **在闭世界和开放世界场景中进行了广泛实验**，包括更挑战性的 1-shot 和 2-shot 设置，验证了 WF-TFC 在少样本场景下的有效性。

## 8. 局限性与未来方向

### 局限性

1. **频域编码器单独效果差**：5-shot 仅 53.02%，说明频域特征在 WF 中的信息量有限，需依赖时域互补。
2. **对重防御（TAMARAW）效果有限**：TAMARAW 以高带宽开销为代价提供强防御，WF-TFC 仅略有改善。
3. **现实场景性能下降**：在 Drift90/Drift5000 和新采集数据集上，F1 从 ~97% 降至 ~82-89%，反映对预训练分布的依赖。
4. **预训练数据需求仍然较大**：每网站 2500 条无标签 trace，获取成本高。

### 未来方向

论文指出将专注于解决更现实的 WF 识别挑战，在有限标记流量下增强模型在动态演进网络中的鲁棒性。

## 9. 关键技术细节

### 超参数表

| 超参数 | 预训练 | 微调 |
|--------|--------|------|
| 学习率 | 5e-4 | 5e-4 |
| Epochs | 100 | 100 |
| Batch size | 128 | 16 |
| 优化器 | Adam + Cosine Scheduler | Adam |
| 嵌入维度 | 512 | 512 |
| 输出维度 | 128 | 网站数量 |
| Dropout | - | 0.9 |
| lambda | 0.8 | - |
| tau | 0.5 | - |

### 时域增强参数

| 参数 | 含义 | 值 |
|------|------|-----|
| r_inc,in | incoming burst 增大比率 | 1.0 |
| r_dec,in | incoming burst 减小比率 | 0.5 |
| r_inc,out | outgoing burst 增大比率 | 1.0 |
| r_dec,out | outgoing burst 减小比率 | 0.5 |
| th_in | incoming burst 最小阈值 | 10 |
| th_out | outgoing burst 最小阈值 | 2 |

### 频域增强参数

| 参数 | 含义 | 值 |
|------|------|-----|
| r_remove | 移除频率分量比率 | 0.1 |
| r_add | 增加频率分量比率 | 0.1 |

## 10. 与其他方法的关系

### 在 WF 方法谱系中的位置

| 方法 | 年份 | 特点 | 少样本能力 |
|------|------|------|------------|
| k-FP | 2015 | 手工特征 + RF + KNN | 无 |
| AWF | 2017 | SDAE | 无 |
| DF | 2018 | CNN 全监督 | 无 |
| TF | 2019 | Triplet Network + N-shot | 有 |
| Var-CNN | 2019 | ResNet-18 + 手工特征 | 有 |
| TLFA | 2021 | 大量标注数据预训练 | 有 |
| WF-Transformer | 2024 | Transformer | 无 |
| NetCLR | 2023 | 网络增强 + 对比学习 | 有（SOTA） |
| **WF-TFC** | **2025** | **时频一致性 + 对比学习** | **有（新 SOTA）** |

### 与 NetCLR 的对比

- **共同点**：都使用 DF 作为骨干网络，都采用自监督对比学习预训练。
- **关键差异**：WF-TFC 引入频域编码器和时频一致性对齐，NetCLR 仅在时域进行增强和对比学习。
- **性能差异**：在各场景下 WF-TFC 一致性超越 NetCLR，尤其在分布偏移和极端少样本场景下优势更大。

## 11. 对本研究领域的启示

1. **频域分析在 WF 中的价值被验证**：尽管频域编码器单独效果有限，但与时域结合并通过一致性对齐后，显著提升了表征质量。这为 [[website-fingerprinting]] 领域提供了新的特征工程思路。
2. **时频一致性作为一种通用预训练范式**：对齐不同域的表征以增强泛化性的思路，可能适用于 [[encrypted-traffic-analysis]] 的其他任务。
3. **少样本场景下的 WF 仍具挑战性**：特别是在分布偏移和现实场景下，性能仍有较大提升空间，这是 [[few-shot-traffic-learning]] 的重要研究方向。
4. **概念漂移是 WF 的核心难题**：WF-TFC 通过预训练-微调范式部分缓解了这一问题，但完全解决仍需更鲁棒的表征学习方法。

## 12. 关键引用

| 引用 | 关键点 |
|------|--------|
| Sirinam et al. 2018 (DF) | 提出 DF CNN 架构，WF-TFC 作为骨干网络 |
| Sirinam et al. 2019 (TF) | 提出基于 Triplet Network 的 N-shot WF |
| Bahramali et al. 2023 (NetCLR) | 提出网络 trace 增强 + 对比学习，WF-TFC 的主要基线 |
| Chen et al. 2021 (TLFA) | 大量标注数据预训练 + 微调的少样本 WF |
| Fu et al. 2021 (Whisper) | 频域分析用于恶意流量检测（与本文频域思路相关） |
| Zhou et al. 2024 (WF-Transformer) | Transformer 用于 WF 时序特征提取 |

---

**相关知识节点**：[[website-fingerprinting]] | [[few-shot-traffic-learning]] | [[encrypted-traffic-analysis]] | [[survey-website-fingerprinting]]

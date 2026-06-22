---
type: paper
title_original: "Few-Shot Website Fingerprinting With Distribution Calibration"
title_cn: "基于分布校准的小样本网站指纹攻击"
authors: ["Chenxiang Luo", "Wenyi Tang", "Qixu Wang", "Danyang Zheng"]
year: 2025
venue: "IEEE TDSC 2025"
doi: "10.1109/TDSC.2024.3411014"
pdf: ""
mineru_md: "02-parsed-markdown/2025-TDSC-Few-Shot_Website_Fingerprinting_With_Distribution_Calibration.md"
status: processed
reading_level: L2
research_area: ["network privacy", "website fingerprinting", "encrypted traffic analysis"]
task: ["website fingerprinting", "few-shot learning", "cross-domain transfer"]
method: ["distribution calibration", "SE Block", "Circle Loss", "Gaussian distribution sampling"]
dataset: ["AWF", "DF-95", "DS-14", "DF-19"]
code: "https://github.com/chenxiang3luo/DCWF"
relevance: medium
created: "2026-06-21"
updated: "2026-06-21"
---

# Few-Shot Website Fingerprinting With Distribution Calibration

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Few-Shot Website Fingerprinting With Distribution Calibration |
| 中文标题 | 基于分布校准的小样本网站指纹攻击 |
| 作者 | Chenxiang Luo (四川大学), Wenyi Tang (四川大学, 通讯作者), Qixu Wang (四川大学), Danyang Zheng (西南交通大学) |
| 年份 | 2025 (IEEE TDSC, 2024-06-07 发表, 2025-01-16 当前版本) |
| 会议/期刊 | IEEE Transactions on Dependable and Secure Computing (TDSC) 2025 |
| 研究方向 | 网络隐私、网站指纹攻击、Tor 匿名通信 |
| 任务类型 | 跨域小样本网站指纹攻击：利用历史标注数据预训练模型，少量目标域数据微调 |
| 方法关键词 | Distribution Calibration, SE Block, Circle Loss, Gaussian Sampling, Two-stage Calibration |
| 数据集 | AWF, DF-95, DS-14, DF-19 |
| 是否开源 | 是 https://github.com/chenxiang3luo/DCWF |
| DOI | 10.1109/TDSC.2024.3411014 |

## 1. 一句话总结

> 提出 DCWF (Distribution Calibrated Website Fingerprinting) 方法，通过两阶段分布校准过程（SE Block 学习目标域信息分布 + 基于源域相似类别的高斯采样校准特征分布）和定制 Circle Loss 网络，同时解决跨域和有偏分布两个问题，在 1-shot 设置下即可达到约 85% 准确率，闭世界和开世界场景下均优于 SOTA。

## 2. 摘要翻译

### 2.1 摘要原文

Website Fingerprinting (WF) aims to identify users' visited websites from encrypted traffic traces, disabling the anonymity of encrypted communication like the Tor network. It is practical to use historically labeled (source) data, e.g., public datasets, to pre-train a WF model, and then collect few incoming (target) data to re-train this model within a low cost. Unfortunately, there is always a considerable difference of latent feature distributions between the source and target data (i.e., the cross-domain problem) and an inevitable bias of feature distribution caused by a limited volume of target data (i.e., the biased distribution problem). Although current Few-Shot Learning-based WF (FSWF) methods achieve satisfactory performance on the efficient establishment, they lack cross-domain transferability, and meanwhile, are unable to alleviate the distribution bias. In this paper, we first systematically analyze the cross-domain problem among different domains of traffics, revealing the ubiquity and dominant factors of it. To mitigate the cross-domain and biased distribution problems, we propose a Distribution Calibrated Website Fingerprinting (DCWF) method that incorporates a two-stage distribution calibration process and a tailored circle network. In the two-stage calibration process, we first devise a re-modeling mechanism capturing the information distribution of the target domain to extract representative features, and then design a calibration process to adjust the biased distribution of the target domain. Subsequently, a tailored circle network is proposed to reduce the noise caused by the calibration process. Finally, extensive experiments are conducted and the results demonstrate the superiority of our DCWF over comparisons under both close-world and open-world settings.

### 2.2 摘要中文翻译

网站指纹 (WF) 旨在从加密流量轨迹中识别用户访问的网站，破坏 Tor 网络等加密通信的匿名性。实际应用中，使用历史标注（源域）数据（如公开数据集）预训练 WF 模型，然后收集少量目标域数据进行重训练，是一种低成本方案。然而，源域与目标域之间的潜在特征分布始终存在显著差异（即跨域问题），且有限目标数据导致特征分布不可避免的偏差（即有偏分布问题）。尽管现有基于小样本学习的 WF (FSWF) 方法在高效建模方面表现良好，但缺乏跨域迁移能力，且无法缓解分布偏差。本文首先系统分析了不同流量域之间的跨域问题，揭示其普遍性和主导因素。为缓解跨域和有偏分布问题，我们提出 DCWF 方法，包含两阶段分布校准过程和定制 Circle Loss 网络。第一阶段设计重建机制捕获目标域信息分布以提取代表性特征，第二阶段设计校准过程调整目标域的有偏分布。随后提出定制 Circle Loss 网络以减少校准过程引入的噪声。大量实验表明 DCWF 在闭世界和开世界设置下均优于对比方法。

## 3. 方法动机

### 3.1 跨域问题与有偏分布问题

**核心问题**：在实际 WF 攻击场景中，攻击者使用历史数据（源域）预训练模型，再用少量目标域数据微调。这导致两个根本性问题：

1. **跨域问题 (Cross-domain Problem)**：源域和目标域的特征分布不同，原因包括时间间隔、TBB 版本差异、网站类别不重叠、网络位置不同
2. **有偏分布问题 (Biased Distribution Problem)**：目标域数据量过少，无法准确代表真实分布，导致分类器过拟合

### 3.2 现有方法的失败模式

| 方法 | 核心弱点 |
|---|---|
| TF (Triplet Fingerprinting) | 使用三元组损失和 KNN 分类器，无跨域迁移能力 |
| WFBDC | 利用 BDC 计算特征，忽略跨域问题，特征提取器缺乏迁移性 |
| TLFA | 需要大量辅助数据（576x2500 traces），小样本下性能差 |
| MBL | 元学习方法，小样本下准确率低于 50% |
| 对抗域适应 [22] | 需要额外源数据集，每次遇到新目标域需重新训练特征提取器 |

### 3.3 跨域问题的四个主导因素

本文首次系统分析了 WF 中的跨域问题，识别出四个主导因素：

| 因素 | 描述 | 域相似度证据 |
|---|---|---|
| **时间间隔 (Time Gap)** | 训练与测试数据收集时间间隔越大，域相似度越低 | AWF200_3d: 0.800 → AWF200_4w: 0.633 |
| **TBB 版本 (TBB Version)** | 不同 TBB 版本导致流量模式变化 | AWF200 vs DS-14 (v6.5 vs v3.5.1): 0.326 |
| **网站重叠 (Websites Overlap)** | 源域与目标域网站类别越不重叠，跨域问题越严重 | AWF200 vs AWF100: 0.556 → AWF500 vs AWF100: 0.400 |
| **网络位置 (Network Locations)** | 不同网络位置的流量模式差异显著 | AWF200 vs DF-95 (同版本): 0.249 |

## 4. 方法设计

### 4.1 整体流程

```
源数据 → 预训练特征提取器 → 跨域场景
                                ↓
目标数据 → 阶段1: SE Block 学习目标域信息分布 → 阶段2: 特征分布校准 → Circle Loss 网络 → 分类器
```

### 4.2 方法组成

| 模块 | 功能 | 技术细节 |
|---|---|---|
| **SE Block** | 捕获目标域信息分布 | 通过 Squeeze (全局平均池化) 和 Excitation (瓶颈全连接层) 获取通道权重 |
| **大卷积核 + 瓶颈结构** | 减少背景噪声影响 | 深度可分离卷积，kernel size 31x1，捕获全局信息 |
| **阶段1: 域分布学习** | 微调 SE Block 通道权重 | 仅微调 SE Block 参数，冻结其他层，学习率 α，batch size 32 |
| **阶段2: 特征分布校准** | 校准目标域有偏分布 | 从源域选择 top-k 相似类别，用其协方差校准目标域分布，高斯采样生成特征 |
| **Circle Loss** | 提高特征空间可分离性 | 动态调整梯度权重，决策边界为圆弧，m=0.25, γ=64 |
| **Circle Network** | 减少校准引入的噪声 | 使特征分布更聚合，提升开世界鲁棒性 |

### 4.3 两阶段分布校准详细流程

**阶段 1: 域分布学习**
- 输入: 源域 D_S, 目标域 D_T, 特征提取器 f_θ, SE Block θ_C
- 操作: 用目标域数据微调 SE Block 参数，学习目标域的通道权重（信息分布）
- 更新公式: θ_C(t+1) = θ_C(t) - α/m * Σ∇L_CE(f(θ, θ_clf; x), y)

**阶段 2: 特征分布校准**
- 假设: 特征分布服从高斯分布（因 Batch Normalization）
- 步骤:
  1. 计算源域各类别质心向量 μ_c 和协方差矩阵 Σ_c
  2. 用余弦距离选择与目标域样本最相似的 top-k 源域类别
  3. 校准协方差: Σ' = (Σ_{i∈S_N} Σ_c) / k + α
  4. 从校准后的高斯分布 N(μ, Σ') 采样 512 个特征向量/类
  5. 用采样特征 + 原始支撑集特征训练分类器

### 4.4 关键假设

| 假设 | 内容 | 依据 |
|---|---|---|
| 高斯分布假设 | 特征分布服从高斯分布 | Batch Normalization 产生稳定的高斯分布 |
| 协方差相似性假设 | 同类网站的协方差相似 | 验证: 校准后性能提升 |
| 信息分布假设 | SE Block 通道权重可代表域信息分布 | 实验证据: 低层通道权重跨类别相似，高层类别特异 |

## 5. 实验设置

### 5.1 数据集

| 数据集 | 收集年份 | TBB 版本 | 网站数 | 用途 |
|---|---|---|---|---|
| AWF | 2017 | 6.5 | 1200 (monitored) + 400,000 (unmonitored) | 源域 / 跨域分析 |
| DF-95 | 2016 | 6.X | 100 + 9000 | 目标域 |
| DS-14 | 2014 | 3.5.1 | 100 + 9000 | 目标域 |
| DF-19 | 2019 | 8.5a7 | 100 + 9000 | 目标域 |

### 5.2 数据表示

- 每条 trace 转换为方向序列: 出站 +1, 入站 -1
- 固定长度 5000 包，不足补零
- 输入维度: [n × 5000]

### 5.3 域相似度度量

- 使用 Earth Mover's Distance (EMD) 度量域间距离
- 相似度定义: sim(S, T) = exp(-γ * EMD(S, T)), γ=0.1
- 特征提取器: Var-CNN (GAP 层输出)

### 5.4 实验设置

- 特征提取器预训练源域: AWF775 (25 traces/website)
- 目标域: AWF100, AWF200_δ, DS-14, DS-19, DF-95
- N-way-K-shot 任务: N=100, K={1,5,10,15,20}
- 评估指标: 闭世界 = Accuracy/TPR/FPR; 开世界 = AUC
- 实现: PyTorch 1.12, NVIDIA RTX 4090

### 5.5 Baseline 方法

| 方法 | 特征提取器 | 损失函数 | 分类器 |
|---|---|---|---|
| TF | DF backbone | Triplet | KNN |
| WFBDC | DF backbone | Multi-similarity | Linear |
| TLFA | 大规模辅助数据 | Cross-entropy | SVM |
| MBL | Meta-learning | Cross-entropy | - |

## 6. 实验结果

### 6.1 闭世界: 网站不重叠 (Disjoint Websites)

| 方法 | 1-shot | 5-shot | 10-shot | 15-shot | 20-shot |
|---|---|---|---|---|---|
| TLFA | 51% | 78% | 85% | 88% | 85% |
| MBL | 46% | 66% | 73% | 76% | 78% |
| WFBDC | 71% | 90% | 93% | 95% | 96% |
| TF | 73% | 88% | 91% | 92% | 93% |
| **DCWF** | **86%** | **96%** | **97%** | **98%** | **98%** |

**关键发现**: DCWF 在 1-shot 下比最佳 baseline (WFBDC) 高 15%。

### 6.2 闭世界: 时间间隔

| 时间间隔 | DCWF 1-shot | DCWF 20-shot | WFBDC 1-shot | WFBDC 20-shot |
|---|---|---|---|---|
| 3天 | 83% | 98% | 70% | 96% |
| 10天 | 82% | 98% | 67% | 96% |
| 2周 | 80% | 98% | 67% | 96% |
| 4周 | 75% | 96% | 62% | 93% |
| 6周 | 73% | 95% | 63% | 93% |

### 6.3 闭世界: 完整跨域场景

| 目标域 | 方法 | 1-shot | 10-shot | 20-shot |
|---|---|---|---|---|
| DS-14 | DCWF | 71.8% | 88.4% | 89.0% |
| DS-14 | WFBDC | 63.1% | 86.9% | 87.9% |
| DS-19 | DCWF | 71.5% | 91.9% | 94.0% |
| DS-19 | WFBDC | 59.0% | 91.1% | 93.4% |
| DF-95 | DCWF | 54.9% | 88.8% | 92.4% |
| DF-95 | WFBDC | 45.0% | 85.4% | 90.4% |

### 6.4 开世界场景 (AUC)

| 目标域 | 方法 | 5-shot | 10-shot | 20-shot |
|---|---|---|---|---|
| AWF100 | DCWF | 0.95 | 0.96 | 0.96 |
| DS-19 | DCWF | 0.97 | 0.98 | 0.98 |
| DF-95 | DCWF | 0.90 | 0.93 | 0.95 |

**关键发现**: 未监控网站数量增加 (9k→400k) 对 AUC 影响极小。

### 6.5 防御场景

| 防御 | 方法 | 1-shot | 10-shot | 20-shot |
|---|---|---|---|---|
| WTF-PAD | DCWF | 37.4% | 75.1% | 79.9% |
| WTF-PAD | WFBDC | 32.1% | 70.6% | 78.5% |
| FRONT | DCWF | 22.5% | 59.5% | 67.9% |
| FRONT | WFBDC | 17.3% | 45.9% | 56.6% |

### 6.6 消融实验

| 方法 | 1-shot Acc | 20-shot Acc | 1-shot TPR |
|---|---|---|---|
| w/o all (无校准) | 83.1% | 97.6% | 83.3% |
| w/o calibration (仅阶段1) | 83.5% | 97.8% | 84.0% |
| **DCWF (完整)** | **86.2%** | **98.0%** | **86.7%** |

**关键发现**: 校准过程在小样本时效果更显著 (1-shot 提升 2.7% TPR)，样本量增加后差距缩小。

### 6.7 损失函数对比

| 损失函数 | 1-shot | 20-shot |
|---|---|---|
| Triplet | 70.3% | 93.5% |
| BDC | 79.8% | 96.5% |
| **Circle** | **85.2%** | **97.9%** |

## 7. 结果分析

### 7.1 核心发现

1. **跨域问题的普遍性**: EMD 分析表明 WF 中跨域问题普遍存在，且受时间间隔、TBB 版本、网站重叠、网络位置四个因素主导
2. **1-shot 的有效性**: DCWF 在 1-shot 设置下即达到约 86% 准确率，比最佳 baseline 高约 15%
3. **网站重叠的反直觉发现**: 对于使用线性分类器的方法（DCWF, WFBDC），网站重叠率增加反而降低性能（噪声效应），仅 100% 重叠时恢复
4. **开世界鲁棒性**: 未监控网站数量从 9k 增加到 400k 对 AUC 几乎无影响
5. **防御鲁棒性**: DCWF 在 FRONT 防御下仍优于 baseline，20-shot 达 67.9% (baseline: 56.6%)

### 7.2 方法优势分析

| 优势 | 说明 |
|---|---|
| 一次性预训练 | 特征提取器只需预训练一次，可迁移至多个目标域 |
| 低标注需求 | 每类仅需 1 个标注样本即可达到 85%+ 准确率 |
| 防御鲁棒性 | Circle Loss 提高特征空间可分离性，对抗防御更有效 |
| 跨域迁移 | 两阶段校准分别处理跨域和有偏分布问题 |

## 8. 贡献与局限

### 8.1 主要贡献

1. **首次系统分析 WF 跨域问题**: 揭示四个主导因素（时间间隔、TBB 版本、网站重叠、网络位置）
2. **两阶段分布校准**: 阶段1 通过 SE Block 学习目标域信息分布提取代表性特征；阶段2 利用源域相似类别校准有偏分布
3. **Circle Loss 网络**: 提高特征空间可分离性，减少校准过程引入的噪声
4. **广泛实验验证**: 在闭世界、开世界、防御场景下均优于 SOTA

### 8.2 局限性

1. **公共数据集限制**: 无法独立控制每个变量（如 TBB 版本和网络位置无法单独评估）
2. **简化假设**: 假设用户按顺序使用 Tor 单标签浏览，现实中很少见
3. **高斯分布假设**: 特征分布可能不严格服从高斯分布，但因 BN 的存在使其较为合理
4. **单一源域**: 仅使用单一源域预训练，未探索多源域场景

## 9. 技术细节

### 9.1 SE Block 结构

| 操作 | 公式 | 说明 |
|---|---|---|
| Squeeze | G_c = 1/W * Σ x_c(i) | 全局平均池化，压缩空间维度 |
| Excitation | S = σ(W_2 * ReLU(W_1 * G)) | 瓶颈结构 (r=2)，学习通道权重 |
| Scale | x̃_c = s_c * x_c | 通道级缩放 |

**关键观察**: 低层通道权重跨类别相似（域级信息），高层通道权重类别特异。

### 9.2 Circle Loss 决策边界

决策边界为圆弧: (s_n - 0)^2 + (s_p - 1)^2 = 2m^2, m=0.25

与传统损失函数的区别:
- Triplet/Softmax: 对每个相似度分数施加等强度惩罚
- Circle Loss: 动态调整梯度权重，偏离最优值的分数获得更大梯度

### 9.3 特征分布校准算法

```
输入: 源域 D_S, 目标域 D_T, 特征提取器 θ, SE Block θ_C, 分类器 θ_clf, k, T
1. 微调 SE Block θ_C (T 次迭代)
2. 计算源域各类别质心 μ_c 和协方差 Σ_c
3. 对每个目标域样本 x_s:
   a. 提取特征 x̃_s = f_θ(x_s)
   b. 用余弦距离选择 top-k 相似源域类别 S_N
   c. 校准协方差: Σ' = (Σ_{i∈S_N} Σ_c)/k + α
   d. 从 N(μ=x̃_s, Σ') 采样 512 个特征
4. 用采样特征 + 支撑集特征训练分类器
```

## 10. 与其他 FSWF 方法的对比

| 方法 | 年份 | 跨域处理 | 有偏分布处理 | 特征提取器迁移性 | 预训练数据需求 |
|---|---|---|---|---|---|
| TF | 2019 | 无 | 无 | 需重新训练 | AWF775 |
| WFBDC | 2022 | 无 | BDC 部分缓解 | 需重新训练 | AWF775 |
| TLFA | 2021 | 无 | 数据增强 | 需重新训练 | 576x2500 traces |
| MBL | 2022 | 无 | 元学习 | 需重新训练 | AWF775 |
| 对抗域适应 [22] | 2021 | 对抗训练 | 无 | 每次新域需重训 | 额外源数据集 |
| **DCWF** | 2025 | SE Block 通道权重 | 高斯采样校准 | **一次预训练，多次迁移** | AWF775 |

## 11. 开放问题

1. **多标签浏览**: 现实中用户常多标签同时浏览，如何处理叠加的流量模式？
2. **独立变量控制**: 需要专门收集数据集以独立评估每个跨域因素的影响
3. **更强域适应方法**: 论文提到计划利用 domain adaptation 和 GANs 进一步解决跨域问题
4. **WF 防御进化**: FRONT 防御下 DCWF 仅达 67.9%，面对更强防御（如 Surakav, RegulaTor）的表现未知
5. **实时攻击**: 未讨论在线实时场景下的适用性

## 12. 结论

本文首次系统分析了 WF 中的跨域问题，识别出四个主导因素（时间间隔、TBB 版本、网站重叠、网络位置），并提出 DCWF 方法通过两阶段分布校准和 Circle Loss 网络同时解决跨域和有偏分布问题。实验表明 DCWF 在 1-shot 下即可达到约 86% 准确率（比 SOTA 高约 15%），在闭世界、开世界和防御场景下均表现优越。

**与 [[website-fingerprinting]] 领域的关联**: 本文从跨域迁移角度推进了 WF 攻击研究，特别是在数据稀缺场景下的实用性。

**与 [[few-shot-traffic-learning]] 的关联**: DCWF 展示了小样本学习在流量分析中的有效性，特别是在跨域场景下的分布校准方法。

**与 [[encrypted-traffic-analysis]] 的关联**: 本文关注 Tor 加密流量的分析，属于加密流量分析的一个重要子领域。

**与 [[survey-website-fingerprinting]] 的关联**: 本文的跨域分析和四个主导因素的发现可作为 WF 领域综述的重要参考。

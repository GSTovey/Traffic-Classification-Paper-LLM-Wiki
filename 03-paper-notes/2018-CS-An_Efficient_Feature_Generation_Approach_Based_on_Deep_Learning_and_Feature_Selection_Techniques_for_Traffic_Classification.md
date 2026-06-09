---
type: paper
title_original: "An Efficient Feature Generation Approach Based on Deep Learning and Feature Selection Techniques for Traffic Classification"
title_cn: "基于深度学习和特征选择技术的高效特征生成方法用于流量分类"
authors:
  - Hongtao Shi
  - Hongping Li
  - Dan Zhang
  - Chaqiu Cheng
  - Xuanxuan Cao
year: 2018
venue: "Computer Science (Elsevier)"
doi: ""
url: ""
pdf: "00-inbox/PDFs/2018-CS-An_Efficient_Feature_Generation_Approach_Based_on_Deep_Learning_and_Feature_Selection_Techniques_for_Traffic_Classification.pdf"
mineru_md: "02-parsed-markdown/2018-CS-An_Efficient_Feature_Generation_Approach_Based_on_Deep_Learning_and_Feature_Selection_Techniques_for_Traffic_Classification.md"
status: processed
reading_level: L2
dataset:
  - unknown
code: "unknown"
relevance: high
research_area: ["流量分类", "特征工程", "特征选择", "深度学习"]
task: ["流量分类", "特征优化"]
method: ["DBN", "symmetric uncertainty", "feature generation", "dimensionality reduction"]
created: "2026-05-27"
updated: "2026-05-29"
---

# 0. 基础信息

- **标题**: An Efficient Feature Generation Approach Based on Deep Learning and Feature Selection Techniques for Traffic Classification
- **作者**: Hongtao Shi (青岛农业大学网络管理中心), Hongping Li (中国海洋大学信息科学与工程学院), Dan Zhang, Chaqiu Cheng, Xuanxuan Cao
- **单位**: Qingdao Agricultural University; Ocean University of China
- **发表时间**: 2018年1月 (Available online 10 January 2018)
- **期刊/会议**: Computer Science (Elsevier)
- **关键词**: Feature Selection, Deep Learning, Multi-class Imbalance, Concept Drift, Machine Learning, Traffic Classification
- **论文类型**: 期刊论文

# 1. 一句话总结

提出 EFOA (Efficient Feature Optimization Approach)，通过三阶段流程（symmetric uncertainty 去除无关特征、DBN-based RFGM 生成鲁棒特征、WSU 去除冗余特征并处理多类不平衡）为 traffic classification 提供最优且鲁棒的特征集，同时应对 feature redundancy、multi-class imbalance 和 concept drift 三大挑战。

# 2. 摘要翻译

近年来，大量研究致力于将 Machine Learning (ML) 技术应用于 flow statistical features 进行 traffic classification。然而，由于 flow statistical features 的高维冗余、流量数量的类别不平衡以及 Internet traffic 的 concept drift，ML 技术的分类性能严重下降。为全面解决这些问题，本文提出一种基于 deep learning 和 Feature Selection (FS) 技术的新 feature optimization 方法，为 traffic classification 提供最优且鲁棒的 features。首先，利用 symmetric uncertainty 去除网络流量数据集中的 irrelevant features；然后，将这些 relevant features 输入基于 deep learning 的 feature generation model 进行 dimensionality reduction 和 feature generation；最后，利用 Weighted Symmetric Uncertainty (WSU) 通过去除 redundant features 来选择最优 features。基于真实流量轨迹的实验结果表明，该方法不仅能有效降低 feature space 的维度，还能克服 multi-class imbalance 和 concept drift 对 ML 技术的负面影响。与已有方法相比，该方法取得了最佳的分类性能和较高的运行时性能。

# 3. 动机与问题定义

## 3.1 核心问题

论文要解决 traffic classification 中的三个关键挑战：

1. **Feature redundancy**: flow statistical features 维度高、冗余严重，会降低 ML 分类器的准确率和效率。
2. **Multi-class imbalance**: 流量数据中多数类（如 WWW）远多于少数类（如 P2P、MULTIMEDIA），导致 ML 算法对少数类的 recall 很低。
3. **Concept drift**: 由于网络技术和用户活动的变化，Internet traffic 及其类别分布随时间动态变化，ML 分类器需要不断更新。

## 3.2 现有方法的不足

- **FS 方法**: 能去除 irrelevant/redundant features，但大多忽视了 multi-class imbalance 和 concept drift；无法捕捉 features 间的复杂依赖关系。
- **Resampling/Cost-sensitive 方法**: 能处理 multi-class imbalance，但会改变原始数据分布或难以获取精确的误分类代价；在高维 feature space 下效果差；无法处理 feature redundancy 和 concept drift。
- **Concept drift 检测方法**: 能通过持续更新分类器保持准确率，但原始 features 中的 irrelevant/redundant features 会降低分类器性能，且更新分类器增加了计算成本。

## 3.3 论文的核心论点

三个问题之间存在强交互关系：feature redundancy 会加剧 multi-class imbalance 和 concept drift 的影响。因此，通过 feature optimization 可以综合解决这三个问题。选择与少数类相关的 features 可以缓解 multi-class imbalance（且不改变原始类别分布），鲁棒稳定的 features 可以有效应对 concept drift。

# 4. 方法设计

## 4.1 整体架构

EFOA 包含三个阶段，形成一个 feature optimization 流水线：

```
Original Features (248维)
    --> Phase 1: Relevance Analysis (symmetric uncertainty)
        --> Relevant Features (去除无关特征)
            --> Phase 2: Feature Generation (DBN-based RFGM)
                --> Robust Features (降维 + 捕捉特征间依赖)
                    --> Phase 3: Redundancy Analysis (WSU)
                        --> Optimal Features (去除冗余，偏向少数类)
```

## 4.2 Phase 1: Relevance Analysis

- 使用 **symmetric uncertainty (SU)** 衡量每个 feature 与 class 之间的 feature-class correlation。
- SU 基于 information entropy，能捕捉非线性相关性，且对取值数量多的变量无偏。
- 公式：SU(V1, V2) = 2 * [IG(V1|V2) / (H(V1) + H(V2))]
- 保留 SU(feature, class) > 0 的所有 features（包括高度相关和弱相关），去除无关特征。

## 4.3 Phase 2: Feature Generation (RFGM)

**核心组件**: Robust Feature Generation Model (RFGM)，基于 Deep Belief Networks (DBNs) 构建。

**架构**:
- 全连接的 directed belief nets：输入层 h^0（D 个 units，D = relevant features 数量），N 个 hidden layers h^1, h^2, ..., h^N，顶部 label layer（C 个 units = 类别数）。
- 第一层使用 **Gaussian-Bernoulli RBM**（输入服从标准正态分布）。
- 更深层使用 **Bernoulli-Bernoulli RBM**。

**训练过程（两阶段）**:
1. **无监督学习 (Unsupervised learning)**: samples 先经 mean-variation 标准化，然后逐层从底部到顶部构建 deep architecture。每一层的参数空间 w^k 通过 Contrastive Divergence (CD) 方法训练。
2. **有监督学习 (Supervised learning / Fine-tuning)**: 使用 samples 及其 class labels，通过 gradient-descent algorithm 和 exponential cost function 对整个 RFGM 的权重空间 W 进行精调。

**特征生成**: 训练完成后，输入 sample 向量 f，返回最后一个 hidden layer 的 hidden units activation values 作为 discriminative features（公式 11）。

**关键特性**: 生成的 features 是通过提取所有 features 之间的交互作用得到的，因此非常稳定和鲁棒。

## 4.4 Phase 3: Redundancy Analysis (WSU)

- 使用 **Weighted Symmetric Uncertainty (WSU)** 衡量每个 feature 的 discriminative power。
- WSU 基于 weighted entropy，权重 w_i = 1 - n_i/N，其中 n_i 是分配到第 i 个值的样本数，N 是总样本数。
- 少数类的权重更大，因此 WSU 能有效处理 multi-class imbalance。
- **冗余去除过程** (Algorithm 1):
  1. 计算所有 features 的 SU(Fi, C)，按降序排列。
  2. 选择 predominant feature Fp。
  3. 移除所有满足 SU_w(Fp, Fq) >= SU_w(Fq, C) 的 feature Fq（即与 predominant feature 的相关性大于与 class 的相关性的 feature 被视为冗余）。
  4. 迭代直到无更多 predominant features。
  5. 输出 optimal features subset。

## 4.5 RFGM 结构选择

- 实验探索了不同深度的 RFGM（从 3 层到 10 层 hidden layers）。
- 最佳结构为 **4 层**（含 hidden layers），此时 flow OA 和 byte OA 均最高。
- 超过 4 层后，gradient-descent 算法难以达到最优解，预测错误率增加。
- 训练时间随 hidden units 数量单调递增。

# 5. 实验设置

## 5.1 数据集

| 数据集 | 来源 | 采集时间 | 特征数 | 类别数 | 说明 |
|--------|------|---------|--------|--------|------|
| Cambridge | University of Cambridge | 2003年8月 | 248 | 10 | 10个独立数据集，24小时内不同时间段采集；用 tcptrace 从 transport layer header 提取；WWW 流量显著多于其他类，典型的 multi-class imbalanced |
| UNIBS | University of Brescia | 2009年9-10月 | 96 | 6 | 两个数据集 (UNIBS01/02)；从每个 flow 的前 6 个 packets 提取特征 |

Cambridge 10 类: WWW, MAIL, FTP-CONTROL, FTP-PASV, ATTACK, P2P, DATABASE, FTP-DATA, MULTIMEDIA, SERVICES

UNIBS 6 类: WWW, P2P, CHAT, MAIL, SSH, OTHER

## 5.2 评估指标

- **Flow OA (Overall Accuracy)**: 正确分类的 flow 数占总 flow 数的比例。
- **Byte OA**: 正确分类的 bytes 数占总 bytes 数的比例。
- **Flow g-mean**: 所有类别 recall 的几何均值，衡量对各类别（包括少数类）的分类均衡性。
- **Byte g-mean**: 基于 byte 级别的 g-mean。
- **F-measure**: precision 和 recall 的调和平均。

所有指标均从 flow 和 byte 两个维度计算。

## 5.3 对比方法

1. **WSU_AUC** (Zhang et al., 2012): hybrid FS 方法，WSU 选初始特征 + AUC 评估最优特征。
2. **GOA** (Fahad et al., 2014): 使用 5 种 FS 算法 + SFS 搜索最优特征子集。
3. **MROS** (Liu & Liu, 2014): random over-sampling 模型。
4. **MRUS** (Liu & Liu, 2014): random under-sampling 模型。
5. **COST** (Liu & Liu, 2014): 基于 MetaCost 的 cost-sensitive learning。
6. **PCDD** (Wang et al., 2013): per concept drift detection 方法。

## 5.4 分类器

- 主要使用 **C4.5 Decision Trees**（实验证明 C4.5 在 multi-class imbalanced 数据上比 SVM 和 NBK 更稳定）。
- SVM 偏向多数类和大流量（elephant flows），NBK 性能最差。

# 6. 实验结果

## 6.1 Cambridge 数据集上的分类性能

**EFOA + C4.5 的整体性能**:

| 指标 | 均值 +/- 标准差 |
|------|----------------|
| Flow OA | 0.978 +/- 0.009 |
| Byte OA | 0.887 +/- 0.098 |
| Flow g-mean | 0.601 +/- 0.134 |
| Byte g-mean | 0.391 +/- 0.266 |

**与原始特征对比**: EFOA 输出的特征比原始特征表现更好，flow g-mean 提升约 7.1%，byte g-mean 提升约 5.3%。P2P 等少数类的 F-measure 显著提升。

**各阶段贡献分析 (Table 6)**:

| 配置 | Flow OA | Byte OA | Flow g-mean | Byte g-mean |
|------|---------|---------|-------------|-------------|
| EFOA (完整) | 0.978 | 0.887 | **0.601** | 0.391 |
| 去掉第一阶段 | 0.976 | 0.872 | 0.562 | **0.423** |
| 去掉第二阶段 | **0.980** | 0.871 | 0.545 | 0.352 |
| 去掉第三阶段 | 0.971 | 0.819 | 0.524 | 0.366 |

- 完整 EFOA 取得最佳 byte OA 和 flow g-mean。
- 去掉第二阶段时 flow OA 最高（因 RFGM 偏向少数类区分，略微降低整体 OA）。
- 去掉第三阶段性能最差，证明 WSU 阶段的有效性。

**与 DBNs 直接分类对比**: EFOA + C4.5 在四个指标上均优于直接使用 DBNs。DBNs 未去除 irrelevant features 且未处理 multi-class imbalance，导致 byte OA、flow g-mean 和 byte g-mean 很差。

## 6.2 与已有方法对比 (Cambridge)

**与 FS 方法对比 (Table 7)**:

| 方法 | Flow OA | Byte OA | Flow g-mean | Byte g-mean |
|------|---------|---------|-------------|-------------|
| EFOA | 0.978 | **0.887** | **0.601** | **0.391** |
| WSU_AUC | **0.980** | 0.838 | 0.501 | 0.237 |
| GOA | 0.979 | 0.832 | 0.484 | 0.230 |

EFOA 在 byte OA、flow g-mean 和 byte g-mean 上均显著优于 WSU_AUC 和 GOA，flow OA 略低。

**与 Resampling/Cost-sensitive 方法对比 (Table 10)**:

| 方法 | Flow OA | Byte OA | Flow g-mean | Byte g-mean |
|------|---------|---------|-------------|-------------|
| EFOA | **0.978** | **0.887** | **0.601** | 0.391 |
| MROS | 0.970 | 0.831 | 0.559 | **0.438** |
| MRUS | 0.963 | 0.874 | 0.570 | 0.424 |
| COST | 0.958 | 0.860 | 0.545 | 0.407 |

EFOA 在 flow OA、byte OA 和 flow g-mean 上最优，但 byte g-mean 相对较低（因未充分考虑 byte 信息）。

**与 PCDD 对比 (Table 13)**:

| 方法 | Flow OA | Byte OA | Flow g-mean | Byte g-mean |
|------|---------|---------|-------------|-------------|
| EFOA | **0.978** | **0.887** | **0.601** | 0.391 |
| PCDD | 0.967 | 0.748 | 0.578 | **0.525** |

EFOA 的 byte g-mean 显著低于 PCDD，但其他指标均优于 PCDD。随 flow instances 增加（>210,000），PCDD 的 flow OA 开始低于 EFOA，说明 EFOA 在应对 concept drift 方面更持久。

## 6.3 UNIBS 数据集上的验证 (Table 16)

| 方法 | Flow OA | Byte OA | Flow g-mean | Byte g-mean |
|------|---------|---------|-------------|-------------|
| EFOA | **0.953** | **0.949** | **0.587** | 0.517 |
| WSU_AUC | 0.921 | 0.895 | 0.549 | 0.497 |
| GOA | 0.934 | 0.918 | 0.511 | 0.483 |
| MROS | 0.917 | 0.921 | 0.581 | 0.541 |
| MRUS | 0.908 | 0.917 | 0.579 | 0.539 |
| COST | 0.911 | 0.911 | 0.577 | 0.535 |
| PCDD | 0.937 | 0.931 | 0.537 | 0.531 |

EFOA 在 UNIBS 上取得最佳 flow OA、byte OA 和 flow g-mean，进一步验证了方法的鲁棒性。UNIBS 数据（2009年）与 Cambridge 数据（2003年）在流量特征和类别分布上有显著差异，证明 EFOA 对数据变化的鲁棒性。

## 6.4 运行时性能

- **Preprocessing**: EFOA 耗时最多（约 470s），因需训练 DBN；GOA 次之（约 680s）；data-level 和 algorithm-level 方法耗时很少。
- **Training**: EFOA、WSU_AUC、GOA 训练时间较少（因特征维度低）；MROS 训练时间最长（因过采样增加了样本数）。
- **Classifying**: PCDD 最慢（约 40s，因持续更新分类器）；EFOA 约 2s；WSU_AUC 和 GOA 最快（约 1s）。

由于 classifying 是在线过程，其效率对实时 traffic classification 至关重要。EFOA 的分类效率优于 PCDD，与 data-level/algorithm-level 方法相当。

# 7. 方法优劣势分析

## 7.1 优势

1. **综合解决三大问题**: 首次通过 feature optimization 同时处理 feature redundancy、multi-class imbalance 和 concept drift。
2. **Deep learning 的优势**: RFGM 能捕捉 features 之间的复杂依赖关系，生成比传统 FS 方法更具 discriminative 和 robust 的 features。
3. **不改变原始数据分布**: 与 resampling 方法不同，EFOA 不修改原始数据，因此不会引入额外偏差。
4. **与 ML 分类器无关**: 生成的 features 可与多种 ML 分类器配合使用。
5. **有效降维**: 从原始 248/96 维特征降至更低维度，提高后续训练和分类效率。

## 7.2 劣势

1. **Byte g-mean 偏低**: 未充分考虑 byte 信息，导致在含有大流量的少数类（byte-level）上表现不如 PCDD 和 resampling 方法。
2. **Preprocessing 耗时长**: DBN 的训练和精调需要大量时间（约 470s），不适合需要频繁更新的场景。
3. **RFGM 结构依赖经验**: hidden layers 的数量和 units 数量通过经验或直觉设定，缺乏自动化结构搜索。
4. **少数类表现不稳定**: 对 ATTACK、MULTIMEDIA 等极少数类的 F-measure 标准差较大（如 ATTACK 的 flow F-measure: 0.456 +/- 0.312）。

# 8. 学习与应用

## 8.1 关键创新点

1. 将 deep learning（DBN）用于 feature generation 而非直接分类，是一个有启发性的思路：利用 deep learning 的特征抽象能力，而非其分类能力。
2. 三阶段流水线设计（相关性分析 - 特征生成 - 冗余分析）的思路可以推广到其他领域的 feature optimization 问题。
3. WSU 通过加权 entropy 实现对少数类特征的偏好选择，是一种不改变数据分布而处理 class imbalance 的有效方式。

## 8.2 可借鉴之处

- **特征优化 vs 数据增强**: 在 class imbalance 问题上，通过特征优化（而非数据层面的 resampling）来提升少数类识别率，避免了引入噪声或丢失信息的风险。
- **对称不确定性 (SU)**: 作为一种基于信息论的 correlation measure，SU 适合处理非线性关系和非数值特征，可作为特征选择的通用工具。
- **概念漂移的特征层面解决方案**: 不通过频繁更新分类器，而是通过生成鲁棒特征来应对 concept drift，是一个值得探索的方向。

## 8.3 局限性与改进方向

- byte g-mean 的不足可以通过在 WSU 中引入 byte-level 的权重来改进。
- RFGM 结构可以使用 NAS (Neural Architecture Search) 等自动化方法来优化。
- 可以探索更高效的 deep learning 架构（如 autoencoder）替代 DBN 以降低 preprocessing 时间。

# 9. 总结

本文提出 EFOA 方法，通过三阶段 feature optimization（symmetric uncertainty 相关性分析、DBN-based RFGM 特征生成、WSU 冗余分析）综合解决 traffic classification 中的 feature redundancy、multi-class imbalance 和 concept drift 三大问题。在 Cambridge 和 UNIBS 两个真实数据集上的实验表明，EFOA 在 flow OA、byte OA 和 flow g-mean 上优于 6 种已有方法，但 byte g-mean 相对较低。EFOA 的 preprocessing 耗时较长，但训练和分类效率较高，适合实时 traffic classification 场景。

# 10. 知识链接

## 10.1 相关论文

- **WSU_AUC** (Zhang et al., 2012): WSU + AUC 的 hybrid FS 方法，是 EFOA 的直接对比基线。
- **GOA** (Fahad et al., 2014): 多准则融合的稳定特征选择方法。
- **PCDD** (Wang et al., 2013): per concept drift detection 方法，是 concept drift 处理的对比基线。
- **SMOTE** (Chawla et al., 2002): 经典的过采样方法。
- **DBN** (Hinton et al., 2006): Deep Belief Networks 的奠基工作，是 RFGM 的理论基础。

## 10.2 核心概念关联

- **Feature Selection** 与 **Feature Generation** 的区别: FS 从原始特征中选择子集，FG 通过变换生成新特征。
- **DBN** 与 **RBM**: DBN 由多层 RBM 堆叠而成，RFGM 使用 Gaussian-Bernoulli RBM（首层）和 Bernoulli-Bernoulli RBM（深层）。
- **Symmetric Uncertainty** vs **Information Gain**: SU 是 IG 的归一化版本，消除了 IG 对取值多的变量的偏好。
- **Weighted Entropy**: 在 entropy 计算中引入类别权重，使少数类获得更大权重，是处理 class imbalance 的信息论方法。

# 11. 证据记录

## 11.1 关键实验数据

- **RFGM 最佳结构**: 4 层 hidden layers（226-200-200-200-20），flow OA 达 0.98，byte OA 达 0.89。
- **EFOA vs 原始特征**: flow g-mean 从 0.53 提升至 0.60（+7.1%），byte g-mean 从 0.34 提升至 0.39（+5.3%）。
- **EFOA vs WSU_AUC**: flow g-mean 0.601 vs 0.501，byte OA 0.887 vs 0.838。
- **EFOA vs PCDD**: flow OA 0.978 vs 0.967；当 flow instances > 210,000 时 EFOA 的 flow OA 开始超过 PCDD。
- **UNIBS 验证**: EFOA flow OA 0.953，优于所有对比方法。

## 11.2 关键发现

- C4.5 在 multi-class imbalanced 数据上比 SVM 和 NBK 更稳定（flow g-mean 最高: 0.601）。
- SVM 偏向多数类和 elephant flows（flow OA 最高但 flow g-mean 最低）。
- EFOA 的 byte g-mean 低于 PCDD 和 resampling 方法，说明其在 byte-level 少数类识别上存在不足。
- 各阶段中，第三阶段（WSU 冗余分析）对分类性能贡献最大（去掉后性能最差）。

# 12. 原始资料链接

- **论文原文**: Elsevier (2018)
- **Cambridge 数据集**: University of Cambridge Computer Laboratory (RR-05-13)
- **UNIBS 数据集**: University of Brescia Telecommunication Networks Group
- **工具**: tcptrace (http://www.tcptrace.org/), Weka (http://www.cs.waikato.ac.nz/ml/weka/)

# 13. 后续问题

1. 如何在 feature optimization 中同时考虑 byte-level 信息以提升 byte g-mean？
2. RFGM 的结构能否通过自动化方法（如 NAS）优化，而非依赖经验设定？
3. 能否用更高效的 deep learning 架构（如 autoencoder、VAE）替代 DBN 来降低 preprocessing 时间？
4. EFOA 生成的鲁棒特征在更长时间跨度（如数月甚至数年）的 concept drift 下是否仍然有效？
5. WSU 的权重设计（w_i = 1 - n_i/N）是否是最优的？是否有更好的加权策略来平衡各类别的特征选择？
6. 该方法能否扩展到 encrypted traffic classification（特征来源不同，但 feature optimization 的思路可能适用）？
7. EFOA 在线上的 feature generation 过程（公式 11）的计算复杂度是多少？在高速网络环境下是否可行？

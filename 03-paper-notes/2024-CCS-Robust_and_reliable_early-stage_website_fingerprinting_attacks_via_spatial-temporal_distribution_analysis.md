---
type: paper
title_original: "Robust and Reliable Early-Stage Website Fingerprinting Attacks via Spatial-Temporal Distribution Analysis"
title_cn: "基于时空分布分析的鲁棒可靠早期网站指纹攻击"
authors:
  - Xinhao Deng
  - Qi Li
  - Ke Xu
year: 2024
venue: "CCS"
doi: "10.1145/3658644.3670272"
url: ""
pdf: "00-inbox/PDFs/2024-CCS-Robust_and_reliable_early-stage_website_fingerprinting_attacks_via_spatial-temporal_distribution_analysis.pdf"
mineru_md: "02-parsed-markdown/2024-CCS-Robust_and_reliable_early-stage_website_fingerprinting_attacks_via_spatial-temporal_distribution_analysis.md"
status: processed
reading_level: L2
research_area: ["网站指纹识别", "流量分类", "隐私攻击"]
task: ["网站指纹识别", "早期流量识别", "暗网检测"]
method: ["supervised-contrastive-learning", "adaptive-data-augmentation", "spatial-temporal-distribution-analysis", "feature-attribution", "SHAP"]
dataset:
  - Alexa-top-10k
  - dark-web-80
  - WTF-PAD
  - Walkie-Talkie
  - FRONT
  - RegulaTor
code: "https://github.com/HolmesWF/Holmes"
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

# Holmes: 基于时空分布分析的鲁棒可靠早期网站指纹攻击

## 0. 基础信息

| 字段 | 内容 |
|------|------|
| 论文全称 | Robust and Reliable Early-Stage Website Fingerprinting Attacks via Spatial-Temporal Distribution Analysis |
| 作者 | Xinhao Deng, Qi Li, Ke Xu |
| 机构 | 清华大学 INSC & BNRist; 中关村实验室 |
| 发表年份 | 2024 |
| 会议/期刊 | CCS 2024 |
| 关键词 | Tor, Website Fingerprinting, Spatial-Temporal Analysis, Contrastive Learning, Early-Stage Attack |
| 代码 | https://github.com/HolmesWF/Holmes |

## 1. 一句话总结

提出 Holmes，一种基于时空分布分析和监督对比学习的早期网站指纹攻击方法，能够在页面加载仅完成约 21.71% 时即可准确识别 Tor 用户访问的网站，F1-score 相比现有 DL-based WF 攻击平均提升 169.18%，且在多种防御机制下保持鲁棒性。

## 2. 摘要翻译

**原文：**
Website Fingerprinting (WF) attacks identify the websites visited by users by performing traffic analysis, compromising user privacy. Particularly, DL-based WF attacks demonstrate impressive attack performance. However, the effectiveness of DL-based WF attacks relies on the collected complete and pure traffic during the page loading, which impacts the practicality of these attacks. The WF performance is rather low under dynamic network conditions and various WF defenses, particularly when the analyzed traffic is only a small part of the complete traffic. In this paper, we propose Holmes, a robust and reliable early-stage WF attack. Holmes utilizes temporal and spatial distribution analysis of website traffic to effectively identify websites in the early stages of page loading. Specifically, Holmes develops adaptive data augmentation based on the temporal distribution of website traffic and utilizes a supervised contrastive learning method to extract the correlations between the early-stage traffic and the pre-collected complete traffic. Holmes accurately identifies traffic in the early stages of page loading by computing the correlation of the traffic with the spatial distribution information, which ensures robust and reliable detection according to early-stage traffic. We extensively evaluate Holmes using six datasets. Compared to nine existing DL-based WF attacks, Holmes improves the F1-score of identifying early-stage traffic by an average of 169.18%. Furthermore, we replay the traffic of visiting real-world dark web websites. Holmes successfully identifies dark web websites when the ratio of page loading on average is only 21.71%, with an average precision improvement of 169.36% over the existing WF attacks.

**中文翻译：**
网站指纹（WF）攻击通过流量分析识别用户访问的网站，危害用户隐私。特别是基于深度学习的 WF 攻击展示了出色的攻击性能。然而，DL-based WF 攻击的有效性依赖于页面加载期间收集的完整且纯净的流量，这影响了这些攻击的实际可用性。在动态网络条件和各种 WF 防御下，WF 性能相当低，特别是当分析的流量仅是完整流量的一小部分时。本文提出 Holmes，一种鲁棒可靠的早期 WF 攻击。Holmes 利用网站流量的时空分布分析，在页面加载早期阶段有效地识别网站。具体而言，Holmes 基于网站流量的时间分布开发自适应数据增强，并利用监督对比学习方法提取早期阶段流量与预收集完整流量之间的相关性。Holmes 通过计算流量与空间分布信息的相关性，准确识别页面加载早期阶段的流量，确保基于早期阶段流量的鲁棒可靠检测。我们在六个数据集上广泛评估了 Holmes。与九种现有 DL-based WF 攻击相比，Holmes 在识别早期阶段流量的 F1-score 上平均提升 169.18%。此外，我们重放了访问真实暗网网站的流量。Holmes 在页面加载比例平均仅为 21.71% 时成功识别暗网网站，平均精度提升 169.36%。

## 3. 方法动机（Motivation）

### 3.1 问题背景与痛点

- **Tor 隐私保护的脆弱性**：Tor 是最流行的匿名通信系统，但容易受到 WF 攻击，现有 DL-based WF 攻击准确率超过 95%
- **完整流量收集的不现实性**：现有 WF 攻击依赖页面加载期间收集的完整且纯净的流量，但在实际场景中：
  - 不同网站页面加载时间和数据包数量差异巨大（5.04% 的网站加载时间超过 120 秒或数据包超过 5000）
  - 动态网络条件（不同路径、带宽、延迟）导致同一网站的流量模式变化
  - WF 防御（填充虚假包、延迟包、分裂流量）严重影响攻击效果
  - 现有攻击（如 DF）在某些网站上最低精度仅 54.11%
- **早期流量识别的挑战**：
  - 早期阶段流量包含的网站信息更少，在动态网络条件下更容易误识别
  - 防御机制对早期阶段流量的影响更大
  - 不同网站的页面加载速度差异大，难以统一设置

### 3.2 核心直觉

- **时空分布相关性**：同一网站的早期阶段流量和完整流量之间存在强烈的时空分布相关性，因为它们包含相同的网站信息（如网站内容和元素的部分）
- **时间分布**：通过特征归因方法（SHAP）分析网站流量的时间分布，发现所有网站的早期阶段流量与完整流量共享相似且充足的网站信息
- **空间分布**：在嵌入空间中，同一网站的流量点聚集在一起，可以通过计算未知流量与各网站的相关性进行识别

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|------|------|----------|
| 现象观察 | 现有 DL-based WF 攻击（如 DF）在动态网络条件和防御下性能大幅下降，某些网站最低精度仅 54.11%；5.04% 的网站加载时间超过 120 秒或数据包超过 5000，固定收集设置无法覆盖所有网站 | §2.2, Figure 2 |
| 痛点提炼 | 完整流量收集不现实：(1) 不同网站加载时间差异巨大；(2) 动态网络条件导致流量模式变化；(3) 防御机制（填充、延迟、分裂）严重影响攻击效果；(4) 固定设置导致部分网站被误识别或漏识别 | §2.2, §1 |
| 问题转化 | 能否在页面加载早期阶段（仅部分流量）就准确识别网站？核心挑战：早期流量信息不足、网络动态干扰、防御影响 | §2.2 |
| 文献定位 | 现有 WF 攻击（DF、ARES、Tik-Tok 等）均依赖完整流量；早期流量分析仅应用于非加密场景；尚无针对 Tor 流量的早期阶段 WF 攻击 | §8 Related Work |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|------|----------|----------|----------|
| 核心假设 | 同一网站的早期阶段流量与完整流量在嵌入空间中具有强相关性，可通过监督对比学习提取 | SHAP 分析显示早期流量包含充足网站信息（Figure 4） | 闭世界实验（§6.2），40% 加载时 Accuracy 达 90.65% |
| 辅助假设1 | 基于网站时间分布的自适应数据增强比随机增强更有效 | 不同网站的有效加载范围不同，随机增强可能生成信息不足的样本 | 与增强 baseline 对比（§6.7），Holmes 提升 255.78% |
| 辅助假设2 | 嵌入空间中的空间分布（质心+半径）可实现可靠的置信度判断 | 不同网站在嵌入空间中形成非重叠球体 | 开放世界实验（§6.3），r-precision 达 94.96% |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|------|-----------|-------------|------|
| 核心假设 | 支撑 | 40% 加载时 Holmes Accuracy 90.65%，最佳 baseline（RF）仅 71.08% | §6.2, Table 2 |
| 辅助假设1 | 支撑 | 20% 加载时 Holmes 比增强 baseline 准确率提升 255.78% | §6.7, Figure 12 |
| 辅助假设2 | 支撑 | 开放世界 40% 加载时 r-precision 94.96%，远超 baselines | §6.3, Figure 9 |

## 4. 方法设计（Method Design）

### 4.1 整体流程

```
早期阶段流量 → 自适应数据增强 → 监督对比学习 → 空间分布分析 → 网站识别
                (时间分布)        (嵌入空间)      (相关性计算)    (置信度判断)
```

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|------|------|----------|------|------|
| Step 1 | 完整流量数据 | 使用 RF 攻击作为目标模型，对每个网站随机选择 10 条流量，计算 SHAP 特征归因 | 每个网站的特征重要性分布 | 时间分布分析 |
| Step 2 | 特征重要性分布 | 聚合同一网站多条流量的 SHAP 值，生成累积分布，根据参数 μ=0.3 和 λ=0.6 计算每个网站的有效加载范围 [s_i, t_i] | 网站级有效加载范围 | 自适应增强基础 |
| Step 3 | 完整流量 + 有效加载范围 | 对每条流量随机采样 l ~ Uniform[s_i, t_i]，掩码从 l 到 100% 的尾部流量，每条流量增强 α=2 次 | 生成的早期阶段流量 | 数据增强 |
| Step 4 | 增强流量 + 原始流量 | 提取 TAF 特征（ρ=2000 个时间窗口，θ=80ms），每个窗口计算 6 维统计特征（入/出包数、入/出 burst 数、平均 burst 大小） | 原始特征向量 x | 特征提取 |
| Step 5 | 原始特征向量 | CNN Encoder（2×2D Conv Block → 2D Pool → 4×1D Conv Block → Adaptive Pool）生成 η=128 维嵌入 | 嵌入向量 z = Enc(x) | 特征变换 |
| Step 6 | 嵌入向量 + 标签 | 使用 SCL 损失训练 Encoder，γ=0.1 | 训练好的 Encoder | 监督对比学习 |
| Step 7 | 各网站嵌入向量 | 计算质心 c_w = Mean(z^w)，使用 MAD 计算半径 r_w，检查并调整重叠球体 | 质心 c 和半径 r | 空间分布建模 |
| Step 8 | 未知早期阶段流量 | 每 τ=120ms 投影到嵌入空间，计算与各网站质心的余弦距离 d，若 d ≤ r_w 则识别成功 | 识别结果或拒绝 | 自适应识别 |

### 4.3 模型结构与系统模块

**Encoder 架构（Figure 7）**：

| 层 | 类型 | 参数 | 输出维度 |
|----|------|------|----------|
| Conv Block 1 | 2D Conv + BN + ReLU × 2 + MaxPool | kernel 3×3 | 通道数翻倍 |
| Conv Block 2 | 2D Conv + BN + ReLU × 2 + MaxPool | kernel 3×3 | 通道数翻倍 |
| 2D Pool | 方向维度聚合 | - | 2D → 1D |
| Conv Block 3-6 | 1D Conv + BN + ReLU × 2 + MaxPool × 4 | kernel 3 | 逐步压缩 |
| Adaptive Pool | 自适应平均池化 | - | 固定 η=128 维 |
| Dropout | 多层 dropout | p=0.5 | 防止过拟合 |

**关键设计选择**：
- **残差连接（Residual Connection）**：从低层到高层的 skip connection，缓解梯度消失问题
- **更深更宽的网络**：相比 RF 和 DF 使用更多通道和更深架构，增强特征提取能力
- **余弦相似度**：使用 1 - cosine_similarity 计算距离，便于矩阵运算加速批量计算

### 4.4 公式推导与机制解释

**SHAP 特征归因（公式 1）**：

SHAP 基于 Shapley 值计算每个特征的边际贡献：

$$\phi_i = \sum_{S \subseteq U \setminus \{f_i\}} \frac{|S|! \cdot (n - |S| - 1)!}{n!} \cdot (O(S \cup \{f_i\}) - O(S))$$

- **直觉**：对于特征 f_i，遍历所有不包含 f_i 的子集 S，计算加入 f_i 后模型输出的变化量
- **权重**：子集大小的组合数保证了公平性——大子集和小组合集的贡献被平衡
- **近似计算**：由于精确计算复杂度为 O(2^n)，使用 DeepLIFT 算法进行近似加速
- **应用**：将流量分为 ρ=2000 个时间窗口，每个窗口的入/出包数作为特征，计算每个窗口的重要性

**自适应数据增强（公式 2）**：

$$l \sim \text{Uniform}[s_i, t_i]$$

- **有效加载范围 [s_i, t_i]**：通过 SHAP 累积分布的 μ=0.3（下界）和 λ=0.6（上界）确定
- **含义**：当页面加载比例达到 s_i 时，流量已包含足够网站信息；超过 t_i 后信息增量递减
- **掩码策略**：从随机采样的位置 l 开始掩码到完整加载，生成的早期流量保证在有效范围内

**监督对比学习损失（公式 4）**：

$$\mathcal{L}_i = -\frac{1}{|P(i)|} \sum_{p \in P(i)} \log \frac{\exp(z_i \cdot z_p / \gamma)}{\sum_{n \in N(i)} \exp(z_i \cdot z_n / \gamma)}$$

- **P(i)**：锚点 x_i 的正样本集合（同一网站的所有流量，包括不同加载阶段）
- **N(i)**：负样本集合（不同网站的流量）
- **温度 γ=0.1**：较小的温度使模型更关注难负样本，增强区分能力
- **核心作用**：同时学习两种相关性——(1) 同一网站不同加载阶段的流量相关性；(2) 同一网站在不同网络条件下的流量相关性

**MAD 半径计算（Algorithm 1）**：

$$r_w = \text{Median}\{|d_i^w - M^w|\}$$

- **M^w**：所有流量到质心距离的中位数
- **r_w**：距离偏差的中位数（MAD），比标准差更鲁棒
- **球体重叠调整**：若两网站球体重叠（概率 0.01%），按比例缩小半径：r_i = r_i - (r_i/(r_i+r_j))·(r_i+r_j-d)

**早期网站识别（Algorithm 2）**：

$$d = 1 - \text{cosine\_similarity}(c_w, z)$$

- **识别条件**：d ≤ r_w 时成功识别，否则继续收集
- **概念漂移检测**：设置阈值 ε=0.01，若 min(d - r_w) < ε 则识别为概念漂移样本
- **最大收集时间 σ=80s**：超过后触发开放世界判断

### 4.3 关键公式

- 特征归因：使用 SHAP 值量化每个时间步的特征重要性
- 对比学习损失：监督对比学习损失函数，拉近同一网站的流量，推远不同网站的流量
- 相关性计算：基于嵌入空间中的距离计算流量与网站的相关性

### 4.4 优缺点

**优势：**
- 首个鲁棒可靠的早期阶段 WF 攻击
- 自适应数据增强：根据网站独特的时间分布生成早期阶段流量
- 监督对比学习：有效提取早期阶段和完整流量之间的相关性
- 空间分布分析：准确识别早期阶段流量
- 拒绝机制：避免低置信度的误识别

**局限：**
- 仍需预收集完整流量作为参考
- 在极端防御下性能可能下降
- 依赖于早期阶段流量与完整流量的相关性假设

## 5. 与其他方法对比（Comparison）

### 5.1 与主流方法的本质区别

| 维度 | DF/RF (SOTA WF) | ARES (多标签) | NetCLR (对比学习) | Holmes |
|------|-----------------|---------------|-------------------|--------|
| 攻击时机 | 完整加载后 | 完整加载后 | 完整加载后 | 早期阶段（20-60%） |
| 数据增强 | 无或随机 | 无 | 自监督增强 | 网站自适应（SHAP） |
| 特征学习 | 交叉熵分类 | 多头注意力分类 | 自监督对比学习 | 监督对比学习 |
| 流量收集 | 固定 120s/5000 包 | 固定设置 | 固定设置 | 自适应（动态停止） |
| 鲁棒性机制 | TAM 特征 | Transformer | 数据增强 | 时空分布+SCL |
| 识别置信度 | softmax 概率 | 多头投票 | 聚类距离 | 球体半径拒绝 |

### 5.2 Baseline 详细对比

| 方法 | 类型 | 特征 | 优势 | 劣势 vs Holmes |
|------|------|------|------|----------------|
| AWF | CNN | 包方向序列 | 首个 DL-based WF | 固定输入长度，早期阶段性能差 |
| DF | CNN | 改进 CNN | 可抵御 WTF-PAD | 依赖完整流量，P@min 仅 54.11% |
| Tik-Tok | CNN | 方向+时间戳 | 利用时间信息 | 早期阶段时间信息不足 |
| Var-CNN | ResNet | 膨胀卷积 | 数据高效 | 固定设置，不适应动态网络 |
| TF | Triplet | N-shot 学习 | 少样本学习 | 度量学习未考虑多阶段相关性 |
| RF | CNN | TAM 矩阵 | 防御鲁棒 | P@min 仅 66.87% |
| NetCLR | CNN | 自监督对比 | 动态网络适应 | 仅单标签对比，未建模跨阶段相关性 |
| ARES | Transformer | 多头注意力 | 多标签攻击 | 无法确保所有网站可靠识别 |
| TMWF | DETR | 目标检测 | 多标签检测 | 计算开销大，早期阶段性能差 |

### 5.4 方法对比表

| 方法 | 40%加载 Accuracy | WTF-PAD 40% Accuracy | P@min (完整) | 暗网 Precision | 延迟 |
|------|-----------------|---------------------|-------------|---------------|------|
| RF | 71.08% | ~45% | 66.87% | 84.99% | 162.21s |
| Var-CNN | 47.52% | ~25% | 0% | 67.31% | 162.21s |
| ARES | 43.28% | ~20% | 54.30% | 52.09% | 236.58s |
| DF | 32.96% | ~25% | 54.11% | 33.68% | 162.21s |
| Holmes | 90.65% | 82.03% | 82.11% | 85.19% | 45.25s |

## 6. 实验表现（Experiments）

### 6.1 数据集

| 数据集 | 描述 | 规模 |
|--------|------|------|
| Alexa-top | Alexa-top 10k 网站 | 10,000 网站 |
| Dark Web | 暗网网站（Tor onion services） | 80 网站 |
| WTF-PAD 防御数据集 | 轻量级填充防御 | - |
| Walkie-Talkie 防御数据集 | 流量分裂防御 | - |
| FRONT 防御数据集 | 前台流量防御 | - |
| RegulaTor 防御数据集 | 规则化防御 | - |

### 6.2 Baseline 方法

- DF（Deep Fingerprint）
- ARES（多标签攻击）
- Tik-Tok
- TF（Triplet Fingerprint）
- NetCLR
- 等其他 9 种 DL-based WF 攻击

### 6.3 评估指标

- F1-score
- Precision
- Recall
- Page Loading Ratio（页面加载比例）

### 6.4 关键结果

**早期阶段流量识别：**
- F1-score 平均提升 169.18%（与 9 种现有方法对比）
- 在页面加载比例平均为 21.71% 时即可成功识别

**暗网网站识别：**
- 80 个真实暗网网站，精度达 85.19%
- 平均页面加载比例仅 21.71%
- 精度平均提升 169.36%

**防御鲁棒性：**
- 在 WTF-PAD、Walkie-Talkie、FRONT、RegulaTor 等防御下保持高性能
- 现有方法在防御下性能大幅下降，Holmes 保持稳定

**自适应流量收集：**
- Holmes 自动停止流量收集当获得足够网站信息
- 不同网站的收集时间不同，适应性强

### 6.5 可靠性评估（P@min）

使用 WTF-PAD 防御数据集（已部署于 Tor 网络），以所有网站中最低精度 P@min 衡量可靠性：

| 页面加载比例 | Holmes | RF | Tik-tok | ARES | DF | Var-CNN | NetCLR | TMWF | AWF | TF |
|---|---|---|---|---|---|---|---|---|---|---|
| 60% | **70.25%** | - | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |
| 80% | 最佳 | 平均提升 299.43% | - | - | - | - | - | - | - | - |
| 100% | **82.11%** | 66.87% | 64.46% | 54.30% | 54.11% | - | - | - | - | - |

**关键发现：**
- 60% 加载时，Holmes P@min=70.25%，所有 baseline 均为 0%（存在完全无法识别的网站）
- 100% 加载时，声称鲁棒的攻击（RF/Tik-tok/ARES/DF）平均精度 >91%，但 P@min 仅 54-67%
- Holmes 100% 加载 P@min=82.11%，相比 RF 提升 22.8%，相比 DF 提升 51.7%
- 多标签攻击 ARES/TMWF 在混淆流量下无法保证可靠识别

**可靠性来源：**
1. 网站自适应数据增强确保所有网站的早期流量包含充足信息
2. SCL 有效分离不同网站流量，减少相似网站误分类
3. 空间分布（质心+半径）通过置信度判断增强识别可靠性

### 6.6 真实世界评估（暗网流量）

使用 80 个真实暗网网站（2023 年 8 月和 2024 年 4 月采集），20 台服务器部署在 3 个国家：

| 方法 | 延迟 | 加载比例 | 精度 |
|------|------|----------|------|
| TF | 162.44s | 73.67% | 17.14% |
| AWF | 100.91s | 47.15% | 10.18% |
| TMWF | 236.58s | 97.58% | 47.21% |
| Tik-tok | 162.21s | 73.63% | 63.19% |
| DF | 162.21s | 73.63% | 33.68% |
| NetCLR | 162.20s | 73.61% | 28.45% |
| ARES | 236.58s | 97.58% | 52.09% |
| Var-CNN | 162.21s | 73.63% | 67.31% |
| RF | 162.21s | 73.63% | 84.99% |
| RF_30%（优化版） | 52.44s | 25.07% | 83.70% |
| **Holmes** | **45.25s** | **21.71%** | **85.19%** |

**关键发现：**
- Holmes 延迟仅 45.25s，比 baseline 平均降低 66.33%
- Holmes 加载比例仅 21.71%，比 baseline 平均降低 66.38%
- Holmes 精度 85.19%，比 baseline 平均提升 169.36%
- 即使 RF 缩短输入长度至 30%（RF_30%），精度仍低于 Holmes（83.70% vs 85.19%），且延迟更高（52.44s vs 45.25s）
- 暗网网站使用 onion 服务，需要更多 Tor 中继，加载延迟更高

## 7. 学习与应用（Learning & Application）

### 7.1 开源情况

- **代码**：https://github.com/HolmesWF/Holmes
- **可复现性**：作者提供了完整的代码和数据集

### 7.2 复现关键步骤

1. **数据准备**：使用 Alexa-top 95 网站闭世界数据集（每网站 >1000 traces）+ 40,000 非监控网站开放世界数据集
2. **SHAP 分析**：选择 RF 攻击作为目标模型，每网站随机 10 条流量，计算 2000 个时间窗口的特征重要性
3. **有效加载范围计算**：参数 μ=0.3（下界）、λ=0.6（上界），生成每网站的 [s_i, t_i]
4. **数据增强**：每条流量增强 α=2 次，从 Uniform[s_i, t_i] 采样掩码起点
5. **特征提取**：TAF 特征（ρ=2000 窗口，θ=80ms），每窗口 6 维统计特征
6. **SCL 训练**：CNN Encoder（2×2D Conv Block → 2D Pool → 4×1D Conv Block → Adaptive Pool），η=128 维嵌入，γ=0.1 温度
7. **空间分布建模**：计算质心 c_w = Mean(z^w)，MAD 半径 r_w，检查球体重叠
8. **识别**：每 τ=120ms 投影到嵌入空间，余弦距离 d ≤ r_w 则识别成功

**关键超参数**：μ=0.3, λ=0.6, α=2, ρ=2000, θ=80ms, η=128, γ=0.1, τ=120ms, σ=80s, ε=0.01

### 7.3 实际应用场景

- **暗网犯罪检测**：在页面加载早期即可识别暗网网站，支持实时监控，延迟仅 45.25s
- **Tor 流量分析**：对 Tor 匿名通信的流量分析，可部署于 ISP/AS 级别
- **隐私保护评估**：评估 WF 防御（WTF-PAD、Walkie-Talkie、Front、TrafficSliver）的有效性
- **多标签攻击增强**：可替换 ARES 中的 Trans-WF 模型，增强多标签场景下的早期识别
- **概念漂移检测**：开放世界设置下自动检测网站内容变化，仅需更新质心和半径

### 7.5 对研究的启发

1. **时空分布相关性**：同一网站不同加载阶段的流量共享网站信息，这一发现可迁移至其他早期流量分析任务
2. **SHAP 用于流量分析**：特征归因方法可量化加密流量中各时间步的信息含量，为自适应收集提供依据
3. **SCL vs 自监督对比学习**：监督对比学习能同时学习同一网站不同阶段和不同网络条件下的两种相关性，优于自监督方法
4. **MAD 半径估计**：比标准差更鲁棒的分布估计方法，适用于对抗环境下的置信度判断
5. **拒绝机制设计**：低置信度拒绝 + 自适应继续收集的范式，可应用于其他需要可靠识别的场景
6. **球体重叠调整**：嵌入空间中网站球体的非重叠约束，为多类别的度量学习提供新思路

## 8. 总结（Summary）

### 8.1 核心思想

Holmes 的核心思想是利用同一网站早期阶段流量与完整流量之间的时空分布相关性，通过监督对比学习在嵌入空间中提取这种相关性，实现早期阶段的网站识别。自适应数据增强确保早期阶段流量包含充足网站信息，空间分布分析实现准确识别，拒绝机制避免误识别。

### 8.2 快速流程图

```
输入：早期阶段流量（页面加载部分完成）
  ↓
自适应数据增强（基于网站时间分布）
  ↓
监督对比学习（提取时空分布相关性）
  ↓
空间分布分析（计算与各网站的相关性）
  ↓
置信度判断（高置信度识别 or 拒绝继续收集）
  ↓
输出：识别的网站 or 继续收集更多流量
```

## 9. 知识链接（Knowledge Links）

- [[website-fingerprinting]]：本文的核心任务，通过流量分析识别用户访问的网站
- [[traffic-classification]]：更广泛的任务类别，网站指纹是其子任务
- [[contrastive-learning]]：本文采用监督对比学习方法提取流量相关性
- [[encrypted-traffic-analysis]]：加密流量分析的背景，WF 是其重要应用
- [[transformer]]：虽然本文未使用 Transformer，但对比学习方法在 Transformer 中有广泛应用

## 10. 证据记录（Evidence）

| 声明 | 证据 | 来源 |
|------|------|------|
| Holmes F1-score 平均提升 169.18% | 与 9 种 DL-based WF 攻击对比，20%-60% 加载 | §6.2, Table 2 |
| 40% 加载时 Accuracy 90.65% | 闭世界 95 网站，比 RF(71.08%) 提升 27.5% | §6.2, Figure 8 |
| 20% 加载时 F1 提升 330.43% | Holmes 53.45% vs baseline 平均 ~12% | §6.2, Table 2 |
| 开放世界 40% 加载 r-precision 94.96% | 95 监控 + 40,000 非监控网站 | §6.3, Figure 9 |
| 暗网识别精度 85.19% | 80 个真实暗网网站，2023-2024 采集 | §6.6, Table 3 |
| 暗网加载比例仅 21.71% | 比 baseline 平均 73.63% 降低 70.5% | §6.6, Table 3 |
| 暗网延迟仅 45.25s | 比 baseline 平均 162s 降低 72.0% | §6.6, Table 3 |
| P@min 100% 加载 82.11% | RF 66.87%, DF 54.11%, ARES 54.30% | §6.5, Figure 11 |
| P@min 60% 加载 70.25% | 所有 baseline 均为 0% | §6.5, Figure 11 |
| WTF-PAD 下 40% 加载 Accuracy 82.03% | 所有 baseline 均低于 45% | §6.4, Figure 10(a) |
| TrafficSliver 下 30% 加载提升 711.28% | 流量分裂防御，Holmes 保持鲁棒 | §6.4, Figure 10(d) |
| 增强 baseline 对比 20% 加载提升 255.78% | 随机掩码增强 vs 网站自适应增强 | §6.7, Figure 12 |
| 5.04% 网站加载超 120 秒或包超 5000 | Alexa-top 10k 网站统计分析 | §2.2, Figure 2 |
| 58.17% 网站加载 <60 秒或 <2500 包 | 固定设置导致过度收集噪声 | §2.2, Figure 2 |
| 球体重叠概率 0.01% | 嵌入空间中网站分布分析 | §5.2, Algorithm 1 |

## 11. 原始资料链接（Source Links）

- **PDF**：`00-inbox/PDFs/2024-CCS-Robust_and_reliable_early-stage_website_fingerprinting_attacks_via_spatial-temporal_distribution_analysis.pdf`
- **MinerU MD**：`02-parsed-markdown/2024-CCS-Robust_and_reliable_early-stage_website_fingerprinting_attacks_via_spatial-temporal_distribution_analysis.md`

## 12. 后续问题（Open Questions）

1. **极端防御场景**：在更激进的 WF 防御下，Holmes 的性能如何？是否存在防御可以完全规避 Holmes？
2. **开放世界扩展**：在完全开放的世界场景中（未知网站数量极多），Holmes 的可扩展性如何？
3. **多标签浏览**：在多标签同时浏览的场景下，早期阶段流量的识别准确性如何？
4. **实时部署**：Holmes 的计算复杂度和延迟是否满足实时部署需求？
5. **隐私防御设计**：基于 Holmes 的发现，如何设计更有效的 WF 防御机制？

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

从现有 DL-based WF 攻击依赖完整流量收集的不现实性出发，观察到早期流量与完整流量共享时空分布相关性，提出基于 SHAP 时间分布分析 + SCL 空间分布分析的三步方法，实现首个鲁棒可靠的早期阶段 WF 攻击。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|------|----------|----------|----------|
| Abstract | 概述问题-方法-结果 | 全文缩影 | "F1-score 平均提升 169.18%" |
| §1 Introduction | 建立完整流量收集的不现实性 | 问题动机 | 5.04% 网站加载超 120 秒 + DF 最低精度 54.11% |
| §2 Background | 形式化问题定义 + 三大目标 | 问题框架 | 可靠性/自适应性/鲁棒性三目标 |
| §3 Threat Model | 定义攻击者能力和场景 | 约束条件 | 本地被动攻击者 + 闭/开放世界 |
| §4 Design | 展示关键观察 + 三模块概述 | 方法骨架 | SHAP 可视化发现早期流量信息充足 |
| §5 Design Details | 详细设计三大模块 | 核心贡献 | SHAP→自适应增强→SCL→MAD→识别 |
| §6 Evaluation | 六数据集全面评估 | 性能验证 | 暗网 85.19% @ 21.71% 加载 |
| §7 Discussion | 讨论局限和对策 | 平衡性 | 概念漂移/多标签/防御对策 |
| §8 Related Work | 定位本文在技术谱系中 | 差异化 | 首个 Tor 流量早期阶段分析 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|----------|----------|----------|------|
| 性能瓶颈 | DF 最低精度仅 54.11%，ARES 最低 42.86% | 量化对比 + 网站级分析 | §2.2, Figure 2 |
| 场景缺失 | 无早期阶段 Tor 流量 WF 攻击 | 文献综述 + 现有方法分析 | §8 Related Work |
| 实用性缺陷 | 固定收集设置无法覆盖所有网站 | 5.04% 网站加载超 120 秒 | §2.2, Figure 2 |
| 防御脆弱性 | 现有攻击在防御下性能大幅下降 | WTF-PAD 下 DF 精度下降 | §2.1 |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|----------|----------|-------------|
| §6.2 闭世界 | 证明早期阶段识别能力 | 核心能力验证 |
| §6.3 开放世界 | 证明区分监控/非监控能力 | 实用性验证 |
| §6.4 鲁棒性 | 证明四种防御下保持高性能 | 鲁棒性目标验证 |
| §6.5 可靠性（P@min） | 证明所有网站均可可靠识别 | 可靠性目标验证 |
| §6.6 真实世界 | 暗网流量实际部署验证 | 实用性最终验证 |
| §6.7 增强 baseline | 排除数据增强本身的贡献 | 方法有效性归因 |
| §6.8 参数分析 | 证明参数不敏感 | 易用性验证 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|------|----------|------------------|
| 开篇方式 | 从现有方法的性能数据出发（95% 准确率 → 54.11% 最低精度） | 用量化数据反差建立问题 |
| Gap 提出方式 | 三层递进：不现实→不鲁棒→不可靠 | 从实用性到性能的多维度 Gap |
| 方法论证逻辑 | 观察→假设→验证的科学方法 | SHAP 可视化作为核心观察证据 |
| 实验组织逻辑 | 闭世界→开放世界→鲁棒性→可靠性→真实世界 | 层层递进，从理想到实际 |
| 最值得借鉴的一句话结构 | "the lowest precision of fingerprinting is only less than 55%" | 用极端数据点制造紧迫感 |

## 14. 跨论文链接（Cross-Paper Links）

- [[2024-CCS-Towards_fine-grained_webpage_fingerprinting_at_scale]]：同为 CCS 2024 的 WF 攻击，Oscar 关注细粒度网页识别，Holmes 关注早期阶段识别；两者都使用度量学习/对比学习变换特征空间
- [[2025-AAAI-MIETT__Multi-Instance_Encrypted_Traffic_Transformer_for_Encrypted_Traffic_Classification]]：MIETT 使用 Transformer + 多实例学习进行加密流量分类，Holmes 使用 CNN + 对比学习；两者都关注流量的层次结构（packet→flow）
- [[2026-NDSS-A_Hard-Label_Black-Box_Evasion_Attack_against_ML-based_Malicious_Traffic_Detection_Systems]]：NetMasquerade 是逃逸攻击（攻击者视角），Holmes 是 WF 攻击（监控者视角）；两者都关注 ML 流量分析系统的鲁棒性
- **方法关联**：Holmes 的 SCL 对比学习 → MIETT 的 FCL 对比学习 → Oscar 的度量学习，三种方法都通过变换特征空间提升分类性能
- **任务关联**：Holmes（早期 WF）+ Oscar（细粒度 WPF）共同推进 WF 攻击的实用性；NetMasquerade 从攻击者角度揭示 ML 检测系统的脆弱性

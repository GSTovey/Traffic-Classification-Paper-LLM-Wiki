---
type: paper
title_original: "Toward Robust Multi-Tab Website Fingerprinting"
title_cn: "面向鲁棒多标签页网站指纹攻击"
authors: ["Xinhao Deng", "Xiyuan Zhao", "Qilei Yin", "Zhuotao Liu", "Qi Li", "Mingwei Xu", "Ke Xu", "Jianping Wu"]
year: 2026
venue: "IEEE/ACM TON 2026"
doi: "10.1109/TON.2026.3666721"
url: unknown
pdf: ""
mineru_md: "02-parsed-markdown/2026-TON-Toward_Robust_Multi-Tab_Website_Fingerprinting.md"
status: processed
reading_level: L2
relevance: medium
research_area: ["website fingerprinting", "encrypted traffic analysis", "multi-tab attack", "deep learning"]
task: ["website fingerprinting", "multi-label classification", "multi-tab attack", "defense robustness"]
method: ["Transformer", "multi-head top-m attention", "multi-level traffic aggregation", "one-vs-all framework", "CNN local profiling"]
dataset: ["closed-world multi-tab (230K+, Alexa Top 100)", "open-world multi-tab (250K+)", "WTF-PAD / Front / RegulaTor / Random defense datasets", "dynamic settings (100K+)"]
code: unknown
created: "2026-06-21"
updated: "2026-06-21"
---

# Toward Robust Multi-Tab Website Fingerprinting

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Toward Robust Multi-Tab Website Fingerprinting |
| 中文标题 | 面向鲁棒多标签页网站指纹攻击 |
| 作者 | Xinhao Deng, Xiyuan Zhao, Qilei Yin, Zhuotao Liu (Senior), Qi Li (Senior, 通讯), Mingwei Xu (Senior), Ke Xu (Fellow), Jianping Wu (Fellow) — 清华大学; Qilei Yin — 中关村实验室 |
| 年份 | 2026 |
| 会议/期刊 | IEEE/ACM Transactions on Networking (TON) 2026 |
| DOI | 10.1109/TON.2026.3666721 |
| 前序会议版 | IEEE S&P 2023 [DOI: 10.1109/SP46215.2023.10179464] |
| 研究方向 | [[website-fingerprinting]]、[[encrypted-traffic-analysis]]、多标签页攻击 |
| 任务类型 | [[website-fingerprinting]]、多标签分类、开放世界识别、防御对抗 |
| 方法关键词 | ARES 框架、Trans-WF 模型、多级流量聚合（packet-level + burst-level）、CNN 局部模式提取、多头 Top-m 自注意力机制、One-vs-All 多标签分类、Droppath 正则化 |
| 数据集 | 闭世界多标签页（230K+ 实例，Alexa Top 100）、开放世界多标签页（250K+）、四种防御数据集（Random / WTF-PAD / Front / RegulaTor，各 50K+）、动态设置（100K+）、不同重叠率（30K+） |
| 是否开源 | 否（论文提及 1500+ 行 PyTorch 代码但未公开链接） |
| PDF | - |
| MinerU Markdown | `02-parsed-markdown/2026-TON-Toward_Robust_Multi-Tab_Website_Fingerprinting.md` |

---

## 1. 一句话总结

> ARES 将多标签页网站指纹攻击建模为多标签分类问题，通过 One-vs-All 框架 + Trans-WF 模型（多级流量聚合 + CNN 局部模式提取 + 多头 Top-m 自注意力）实现无需预知标签页数量的鲁棒攻击，在 5 标签页闭世界场景 MAP@5=0.909（超最优基线 55%），在 WTF-PAD 防御下平均提升 112.74%。

---

## 2. 摘要翻译

### 2.1 摘要原文

Website fingerprinting enables an eavesdropper to determine which websites a user is visiting over an encrypted connection. State-of-the-art website fingerprinting (WF) attacks have demonstrated effectiveness even against Tor-protected network traffic. However, existing WF attacks have critical limitations on accurately identifying websites in multi-tab browsing sessions, where the holistic pattern of individual websites is no longer preserved, and the number of tabs opened by a client is unknown a priori. In this paper, we propose ARES, a novel WF framework natively designed for multi-tab WF attacks. ARES formulates the multi-tab attack as a multi-label classification problem and solves it using the novel Transformer-based models. Specifically, ARES extracts local patterns based on multi-level traffic aggregation features and utilizes the improved self-attention mechanism to analyze the correlations between these local patterns, effectively identifying websites. We implement a prototype of ARES and extensively evaluate its effectiveness using our large-scale datasets collected over multiple months. The experimental results illustrate that ARES achieves optimal performance in several realistic scenarios. Further, ARES remains robust even against various WF defenses.

### 2.2 摘要中文翻译

网站指纹攻击使窃听者能够通过加密连接确定用户正在访问哪些网站。最先进的 WF 攻击已被证明对 Tor 保护的网络流量同样有效。然而，现有 WF 攻击在准确识别多标签页浏览会话中的网站方面存在关键限制——此时单个网站的整体流量模式不再保留，且客户端打开的标签页数量事先未知。本文提出 ARES，一个专为多标签页 WF 攻击设计的新框架。ARES 将多标签页攻击建模为多标签分类问题，并使用新型 Transformer 模型求解。具体而言，ARES 基于多级流量聚合特征提取局部模式，并利用改进的自注意力机制分析这些局部模式之间的关联，从而有效识别网站。我们实现了 ARES 原型，并使用跨越多个月采集的大规模数据集进行了广泛评估。实验结果表明 ARES 在多种现实场景中达到最优性能，并对各种 WF 防御保持鲁棒性。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

现有 WF 攻击普遍假设客户端在一个浏览会话中只访问单个网页（single-page assumption），但现实中用户经常同时打开多个浏览器标签页。多标签页浏览会导致不同网站的流量模式混合，使传统 WF 攻击性能急剧下降。

### 3.2 现有方法的痛点和不足

| 痛点 | 具体表现 | 影响 |
|---|---|---|
| C1: 需预知标签页数量 | 现有多标签页方法（如 [12]）需固定标签页数训练，模型不泛化到其他标签页数 | 实际部署不可行，用户标签页数动态未知 |
| C2: 对防御不鲁棒 | 轻量级防御（WTF-PAD）即可大幅降低现有多标签页攻击效果 | 现实 Tor 网络已部署防御 |
| C3: 标签页增多性能下降 | 依赖干净流量分块，标签页越多越难提取干净分块 | 方法可扩展性差 |
| C4: 需要最大标签页数先验知识 | BAPM [16]、TMWF [17] 等最新方法仍需预知最大标签页数 | 限制实际应用场景 |

### 3.3 论文的研究假设或核心直觉

**核心直觉**：虽然多标签页浏览会话中网站的整体流量模式被破坏，但**多个短流量段中仍可提取网站的局部模式**。通过分析这些局部模式之间的关联性，仍可构建鲁棒的网站签名。

**关键洞察**（互信息分析）：传统顺序特征（包方向/时间戳序列）的互信息随标签页数增加急剧下降，但基于分段的聚合特征（packet-level + burst-level）保持更高互信息，多级聚合特征信息保留最优。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 现有多标签页 WF 攻击在动态标签页数和防御场景下性能大幅下降 | §I, Table II-IV |
| 痛点提炼 | 三个关键缺陷：(i) 需预知标签页数；(ii) 对防御脆弱；(iii) 标签页增多性能下降 | §I |
| 问题转化 | 将多标签页攻击从"先分块再分类"转化为"多标签分类"问题 | §IV-A |
| 文献定位 | 现有方法（BAPM, TMWF, RF, Tik-Tok 等）均无法同时解决上述三个问题 | §VII |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 多标签页场景中局部流量模式仍然可提取且具有区分性 | 互信息分析（Fig. 3）显示聚合特征信息保留优于顺序特征 | 消融实验（Table VIII, IX） |
| 辅助假设 1 | Top-m 注意力可过滤噪声包干扰，比全连接注意力更鲁棒 | 目标网站流量与其他网站/防御噪声的相关性低于自身 | 防御实验（Table IV） |
| 辅助假设 2 | One-vs-All 多标签框架无需预知标签页数即可工作 | 每个分类器独立判断特定网站是否存在 | 动态设置实验（Table V） |
| 辅助假设 3 | 参数共享的单 Trans-WF + 多线性头比独立分类器更高效 | 会议版 [1] 使用独立分类器，期刊版共享骨干降低训练成本 | 延迟分析（Fig. 10） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | 移除流量聚合模块后 MAP@2 从 0.903 降至 0.828（-8.31%） | Table VIII |
| 辅助假设 1 | 支撑 | WTF-PAD 下 ARES MAP@2=0.893 vs TMWF 0.641（+39.3%） | Table IV |
| 辅助假设 2 | 支撑 | 动态标签页设置 AUC=0.945 vs 所有基线 <0.85 | Table V |
| 辅助假设 3 | 支撑 | 推理延迟 5.08-5.86ms，受监控网站数影响小 | Fig. 10 |

---

## 4. 方法设计

### 4.1 方法整体流程

ARES 采用 One-vs-All 多标签分类框架：一个共享的 Trans-WF 骨干模型 + N 个线性层头（N = 监控网站数）。每个头预测特定监控网站存在于混淆流量中的概率，通过阈值判定输出完整标签集。Trans-WF 由三个模块组成：多级流量聚合、局部模式提取、网站识别。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1: 流量分段 | 混淆流量 | 按固定时间间隔 t（默认 20ms）分段 | 多个子段 | 隔离局部模式，减少全局噪声 |
| Step 2: 多级流量聚合 | 每个子段 | 分别提取入/出方向的 packet-level（包数 + 平均包间隔）和 burst-level（burst 数 + 平均 burst 大小）特征 | 8 维特征向量/段 | 捕获细粒度时间 + 粗粒度传输模式 |
| Step 3: 特征拼接 | 所有子段特征 | 拼接为固定维度输入（默认 8000 维） | 特征矩阵 | 作为 Trans-WF 输入 |
| Step 4: CNN 局部模式提取 | 特征矩阵 | L 个 Conv1d+BN+ReLU+残差连接+MaxPool+Dropout 块 | 局部模式向量 | 利用 CNN 平移不变性提取位置无关模式 |
| Step 5: 多头 Top-m 自注意力 | 局部模式向量 | 并行 h 个 Top-m 注意力头（默认 h=2, m=20） | 关联性表示 | 分析局部模式间关联，过滤噪声 |
| Step 6: 网站判定 | 关联性表示 | LayerNorm + MLP + 残差连接 | 每个监控网站的存在概率 | 输出二值预测 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 多级流量聚合 | 从混淆流量提取 packet + burst 聚合特征 | 原始流量 | 特征矩阵 | 为 CNN 提供输入 |
| CNN 局部模式提取 | 利用平移不变性提取位置无关的局部模式 | 特征矩阵 | 局部模式向量 | 为注意力层提供输入 |
| 多头 Top-m 自注意力 | 分析局部模式关联性，过滤噪声 | 局部模式向量 | 关联性表示 | 核心识别模块 |
| One-vs-All 线性头 | 每个监控网站独立预测存在概率 | 关联性表示 | N 个概率值 | 阈值判定输出标签集 |
| Droppath | 训练时随机跳过残差连接 | 训练过程 | 正则化效果 | 缓解过拟合 |

### 4.4 公式、算法和机制解释

**互信息分析（特征选择依据）**：

$$
I(F; C) = H(C) - H(C|F)
$$

用于量化不同特征类型包含的网站信息量。结果表明多级聚合特征在所有标签页数下互信息最高。

**Top-m 注意力（核心创新）**：

$$
\text{Attention}^{Top-m}(Q, K, V) = \text{softmax}\left(\Gamma\left(\frac{QK^T}{\sqrt{d}}\right)\right) V
$$

其中 Gamma 为行级 Top-m 选择操作：保留每行最大 m 个元素，其余替换为极小常数 epsilon。这过滤了与目标网站无关的噪声特征，提升鲁棒性。

**One-vs-All 判定**：

每个监控网站 i 由独立线性头预测概率 p_i，通过预设阈值（默认 0.5）判定该网站是否被访问。无需预知标签页数量。

### 4.5 方法优势

1. **无需预知标签页数**：One-vs-All 框架将多标签页攻击转化为多个独立二分类，标签页数动态变化不影响架构
2. **局部模式鲁棒性**：CNN 平移不变性 + 多级聚合特征在混淆流量中仍可提取有效模式
3. **噪声过滤**：Top-m 注意力机制相比全连接注意力有效过滤防御噪声和无关网站流量
4. **增量扩展**：新增监控网站只需训练新的线性头，共享骨干固定
5. **低推理延迟**：5-6ms/batch（RTX 4090），适合实时部署

### 4.6 方法不足

1. **监控网站数受限**：当前仅评估 100 个监控网站，极端多标签（数万到数百万网站）未解决
2. **训练成本较高**：单个 Trans-WF 训练约 60 分钟（RTX 2080Ti）
3. **未公开代码**：1500+ 行 PyTorch 代码未开源
4. **RegulaTor 防御下性能下降**：MAP@2=0.773，虽优于基线但绝对值不高
5. **输入维度敏感**：d=2000 时 MAP@2 仅 0.852，需足够输入维度（>=8000）
6. **未考虑极端多标签场景**：标签树架构（XMLC）在讨论中提及但未实现

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 维度 | 传统多标签页 WF（BAPM, TMWF） | ARES |
|---|---|---|
| 问题建模 | 先分块再分类（需预知标签页数） | 多标签分类（无需预知标签页数） |
| 分类器架构 | 独立端到端模型 | One-vs-All + 共享 Trans-WF + 多线性头 |
| 注意力机制 | 标准 Transformer 注意力 | Top-m 注意力（过滤噪声） |
| 特征提取 | 原始流量序列 | 多级聚合特征（packet + burst） |
| 防御鲁棒性 | 弱（WTF-PAD 下显著下降） | 强（WTF-PAD MAP@2=0.893） |

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 多标签页建模为多标签分类 | One-vs-All 框架，每网站独立预测存在概率 | 高 | 是（任何多实例识别任务） |
| Trans-WF 模型 | CNN 局部模式 + 多头 Top-m 注意力 | 高 | 部分（Top-m 注意力通用） |
| 多级流量聚合 | packet-level + burst-level 分段统计特征 | 中 | 是（[[traffic-classification]] 特征工程） |
| 参数共享 + 多头结构 | 单骨干 + N 线性头替代 N 独立分类器 | 中 | 是（大规模分类任务） |

### 5.3 适用场景

- Tor 匿名网络中的多标签页网站监控
- 未知标签页数量的动态浏览会话
- 存在轻量级防御（WTF-PAD, Front）的对抗场景
- 需要增量扩展监控网站集的长期部署

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| BAPM (ACACS 2021) | Block attention 提取多标签页模式 | 需预知最大标签页数，防御下性能差 | One-vs-All 消除标签页数依赖 |
| TMWF (CCS 2023) | Transformer 端到端多标签页攻击 | 需预知最大标签页数，WTF-PAD 下 MAP@2=0.641 | Top-m 注意力过滤噪声 |
| RF (USENIX 2023) | 聚合特征鲁棒 | 仅单标签页，自适应池化层混合多网站信息 | 多级聚合 + One-vs-All |
| Tik-Tok (PET 2020) | 时间间隔特征鲁棒 | 仅单标签页 | 分段聚合保留局部时间信息 |
| Var-CNN (PET 2019) | 深度学习自动特征 | 仅单标签页 | One-vs-All 多标签扩展 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

七个实验维度：
- **闭世界多标签页**：2-5 标签页，Alexa Top 100 监控网站
- **开放世界多标签页**：2-5 标签页，非监控网站来自 Alexa Top 20K
- **防御对抗**：Random / WTF-PAD / Front / RegulaTor（2 标签页）
- **动态设置**：动态标签页数 / 动态防御类型
- **重叠率**：10%-50% 流量重叠
- **泛化性**：训练/测试标签页数不匹配
- **参数分析**：时间间隔 t、输入维度 d、Top-m 参数 m、注意力层数 n

### 6.2 数据集

| 数据集 | 规模 | 标签页数 | 防御 | 采集时间 |
|---|---|---|---|---|
| 闭世界多标签页 | 230K+ 实例 | 2-5 | 无 | 2021.5-2021.12 + 2022.6-2022.11 |
| 开放世界多标签页 | 250K+ 实例 | 2-5 | 无 | 同上 |
| Random 防御 | 50K+ 实例 | 2 | Random padding | - |
| WTF-PAD 防御 | 50K+ 实例 | 2 | WTF-PAD | - |
| Front 防御 | 50K+ 实例 | 2 | Front | - |
| RegulaTor 防御 | 50K+ 实例 | 2 | RegulaTor | - |
| 动态设置 | 100K+ 实例 | 混合 | 混合 | - |
| 重叠率数据集 | 30K+ 实例 | 2 | 无（合成） | - |

数据采集工具：基于 Tor Browser + Selenium 的自动化工具，部署在 40 个不同区域云服务器上。

### 6.3 Baseline

| 方法 | 类型 | 特点 |
|---|---|---|
| Var-CNN | 单标签页 DL | 深度学习自动特征 |
| NetCLR | 单标签页 DL | 数据增强 + 对比学习 |
| DF | 单标签页 DL（抗防御） | 复杂 CNN |
| Tik-Tok | 单标签页（抗防御） | 时间间隔特征 |
| RF | 单标签页（抗防御） | 聚合特征 |
| BAPM | 多标签页 | Block attention |
| TMWF | 多标签页 | Transformer |

### 6.4 评价指标

AUC、P@k（Top-k 精确率）、MAP@k（Top-k 平均精确率均值）、Precision、Recall。

### 6.5 关键实验结果

**闭世界多标签页（Table II）**：

| 设置 | ARES MAP@k | 最优基线 MAP@k | 提升 |
|---|---:|---:|---:|
| 2-tab | 0.938 | 0.788 (TMWF) | +19.0% |
| 3-tab | 0.916 | 0.720 (TMWF) | +27.2% |
| 4-tab | 0.922 | 0.685 (TMWF) | +34.6% |
| 5-tab | 0.909 | 0.586 (TMWF) | +55.1% |

**防御对抗（Table IV，2-tab）**：

| 防御 | ARES MAP@2 | 最优基线 MAP@2 | 提升 |
|---|---:|---:|---:|
| Random | 0.925 | 0.730 (TMWF) | +26.7% |
| WTF-PAD | 0.893 | 0.679 (Var-CNN) | +31.5% |
| Front | 0.900 | 0.678 (TMWF) | +32.7% |
| RegulaTor | 0.773 | 0.477 (TMWF) | +62.1% |

WTF-PAD 下平均 P@2 提升 112.74%，MAP@2 提升 89.73%。

**动态设置（Table V）**：

| 设置 | ARES AUC | ARES MAP | 最优基线 MAP |
|---|---:|---:|---:|
| 动态标签页 | 0.945 | 0.707 (MAP@5) | 0.467 (Var-CNN) |
| 动态防御 | 0.987 | 0.864 (MAP@2) | 0.501 (TMWF) |

**泛化性（Table VII）**：训练/测试标签页数不匹配时，ARES 平均 AUC 提升 14-17%。

**重叠率（Table VI）**：50% 重叠率下 ARES MAP@2=0.914，所有基线 <0.86。

### 6.6 优势最明显的场景

- **高标签页数**（5-tab）：MAP@5 提升 55.1%，优势随标签页数增加而扩大
- **RegulaTor 防御**：MAP@2 提升 62.1%，在最强防御下优势最显著
- **动态设置**：MAP@5 提升 51.4%，无需预知标签页数/防御类型的架构优势
- **高重叠率**（50%）：MAP@2=0.914，局部模式提取在高混淆下仍有效

### 6.7 局限性

1. 极端多标签（XMLC，数万以上网站）未解决，标签树架构未实现
2. 训练成本较高（60min/模型，RTX 2080Ti）
3. 代码未开源
4. RegulaTor 防御下绝对性能 0.773 仍有提升空间
5. 输入维度需 >=8000 才能达到最佳性能
6. 未评估更强防御（Surakav, Shadow 等）

---

## 7. 学习与应用

### 7.1 是否开源？

否。论文提及 1500+ 行 PyTorch 代码但未提供公开链接。

### 7.2 复现关键步骤

1. 部署 40 个云服务器 + Tor Browser + Selenium 自动化采集
2. 流量预处理：按 20ms 时间间隔分段 → 提取 packet-level（包数 + 平均包间隔）和 burst-level（burst 数 + 平均 burst 大小）特征 → 拼接为 8000 维输入
3. 模型训练：Trans-WF（4 块 CNN + 2 头 Top-m-20 注意力）+ 100 个线性头
4. 推理：每个头输出概率 → 阈值 0.5 判定 → 输出标签集
5. 评估：AUC / P@k / MAP@k

### 7.3 关键超参数、预处理和训练细节

| 参数 | 默认值 | 敏感性 | 说明 |
|---|---|---|---|
| 时间间隔 t | 20ms | 低（10-50ms 内 MAP@2 变化 <3%） | 流量分段间隔 |
| 输入维度 d | 8000 | 中（2000 时性能降 6%） | 过小则信息不足 |
| Top-m 参数 m | 20 | 低（5-25 变化 <1%） | 注意力中保留的 top 元素数 |
| 注意力层数 n | 4 | 低（1-5 变化 <2%） | Transformer 层数 |
| 注意力头数 h | 2 | - | 多头注意力头数 |
| CNN 块数 L | 4 | - | 局部模式提取层数 |
| 卷积核大小 | 7 | - | Conv1d 核大小 |
| 池化大小 | 8 | - | MaxPool 大小 |
| 输出维度 | 256 | - | 局部模式维度 |
| 判定阈值 | 0.5 | 中 | 越高精确率越高、召回率越低 |

### 7.4 能否迁移到其他任务？

**高度可迁移的概念**：
- **One-vs-All 多标签分类框架**：可迁移到任何需要识别多个同时存在目标的加密流量分析任务（如多应用识别）
- **Top-m 注意力机制**：通用的噪声过滤注意力，可迁移到任何 Transformer 架构中对抗噪声输入
- **多级流量聚合特征**：packet-level + burst-level 的分段统计特征可用于 [[traffic-classification]] 任务

**需注意**：
- Trans-WF 的具体架构（CNN 块数、注意力头数等）需要针对新任务调优
- 互信息分析方法可复用于评估不同特征类型的区分能力

### 7.5 对我的研究有什么启发？

1. **多标签页问题建模**：将多标签页 WF 转化为多标签分类的思路可推广到其他"多实例混合"场景（如多应用同时运行的流量分类）
2. **Top-m 注意力**：噪声过滤的注意力机制对 [[encrypted-traffic-analysis]] 中的鲁棒性问题有通用价值
3. **局部模式提取**：CNN 平移不变性在混淆流量中提取局部模式的思路，与 [[traffic-classification]] 中的分段特征工程方法论相通
4. **与 [[survey-website-fingerprinting]] 的关联**：ARES 是多标签页 WF 方向的重要进展，期刊版相比会议版 [1] 增加了参数共享、延迟分析、增量扩展等评估

---

## 8. 总结

### 8.1 核心思想

> One-vs-All 多标签分类 + Trans-WF（多级聚合 + CNN 局部模式 + Top-m 注意力）实现无需预知标签页数的鲁棒多标签页网站指纹攻击。

### 8.2 速记版 Pipeline

1. 流量分段：20ms 间隔分段 → 8 维聚合特征/段（packet count/interval + burst count/size x 入/出方向）
2. CNN 局部模式提取：4 块 Conv1d+BN+残差+MaxPool → 256 维局部模式
3. Top-m 注意力：2 头 Top-20 注意力分析局部模式关联性
4. One-vs-All 判定：100 个线性头独立预测 → 阈值 0.5 → 输出标签集

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]]
- [[encrypted-traffic-analysis]]
- [[traffic-classification]]

### 9.2 相关方法

- [[survey-website-fingerprinting]]

### 9.3 相关任务

- [[website-fingerprinting]] — 多标签页变体
- 多标签分类
- 鲁棒性攻击与防御对抗

### 9.4 可更新的综述页面

- [[survey-website-fingerprinting]] — 多标签页 WF 攻击进展（期刊版 ARES）

### 9.5 可加入的对比表

- 多标签页 WF 方法对比表（标签页数依赖性、防御鲁棒性、泛化性）
- WF 攻击方法在不同防御下的鲁棒性对比表

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| ARES 5-tab MAP@5=0.909 | Table II: ARES MAP@5=0.909 vs TMWF 0.586 | §V-B |
| WTF-PAD 下平均提升 112.74% | Table IV: ARES P@2=0.846 vs 基线平均 ~0.4 | §V-D |
| 互信息分析：聚合特征优于顺序特征 | Fig. 3: 5-tab 时 packet sequence ~0.5 vs multi-level ~2.0 | §IV-B |
| 消融：移除 CNN 模块 MAP@2 降 21.82% | Table VIII: 无 CNN 0.706 vs 完整 0.903 | §V-I |
| 动态标签页 AUC=0.945 | Table V: ARES AUC 0.945 vs 基线 <0.85 | §V-E |
| 增量扩展性能稳定 | 96→100 网站 P@2: 0.877-0.889 | §V-E |
| 推理延迟 5-6ms | Fig. 10: 20 网站 5.08ms, 100 网站 5.86ms | §V-J |
| 参数敏感性低 | Fig. 9: t/m/n 变化下 MAP@2 变化 <3% | §V-H |
| RegulaTor 下仍有优势 | Table IV: ARES 0.773 vs TMWF 0.477 | §V-D |

---

## 11. 原始资料链接

- PDF：-
- MinerU Markdown：`02-parsed-markdown/2026-TON-Toward_Robust_Multi-Tab_Website_Fingerprinting.md`
- 前序会议版：IEEE S&P 2023 [DOI: 10.1109/SP46215.2023.10179464]

---

## 12. 后续问题

- 标签树架构（XMLC）能否有效扩展到数万监控网站的场景？
- 更强防御（Surakav, Shadow, Real-time defense）下 ARES 的鲁棒性如何？
- Top-m 注意力中 m 的自适应选择能否进一步提升性能？
- 将 ARES 的 One-vs-All 框架与其他特征提取方法（如 RF 的聚合特征）结合效果如何？
- 与 Oscar (CCS 2024) 等同时期多标签页方法的技术路线对比如何？
- ARES 在非 Tor 加密代理（如 Shadowsocks/V2Ray）场景下的泛化性？

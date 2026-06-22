---
type: paper
title_original: "PrismWF: A Multi-Granularity Patch-Based Transformer for Robust Website Fingerprinting Attack"
title_cn: "PrismWF：面向鲁棒网站指纹攻击的多粒度 Patch-Based Transformer"
authors:
  - Yuhao Pan
  - Wenchao Xu
  - Fushuo Huo
  - Haozhao Wang
  - Xiucheng Wang
  - Nan Cheng
year: 2026
venue: "arXiv 2026"
doi: unknown
url: unknown
pdf: ""
mineru_md: "02-parsed-markdown/2026-arXiv-PrismWF__A_Multi-Granularity_Patch-Based_Transformer_for_Robust_Website_Fingerprinting_Attack.md"
status: processed
reading_level: L2
relevance: medium
dataset:
  - "ARES multi-tab datasets: 100 monitored sites, 2/3/4/5-tab subsets, 58,000+ instances/subset (closed-world)"
  - "Open-world: 64,000 instances/subset (100 monitored + unmonitored)"
code: unknown
research_area: ["网站指纹", "流量分析", "多标签分类", "隐私与匿名"]
task: ["多标签网站指纹攻击", "Tor 流量分析", "多 Tab 混合流量识别"]
method: ["Transformer", "Multi-Granularity Attention", "CNN", "Router Token"]
created: "2026-06-21"
updated: "2026-06-21"
---

# PrismWF: A Multi-Granularity Patch-Based Transformer for Robust Website Fingerprinting Attack

## 0. 基础信息

| 项目 | 内容 |
|------|------|
| 论文标题 | PrismWF: A Multi-Granularity Patch-Based Transformer for Robust Website Fingerprinting Attack |
| 作者 | Yuhao Pan, Wenchao Xu, Fushuo Huo, Haozhao Wang, Xiucheng Wang, Nan Cheng |
| 机构 | HKUST (通讯); Xidian University; Southeast University; Huazhong University of Science and Technology |
| 会议/期刊 | arXiv 2026 (preprint) |
| 发表状态 | preprint |
| 关键词 | Tor; Website Fingerprinting; Multi-Tab Attack; Multi-Granularity; Transformer; Router Token |
| 数据集 | ARES multi-tab datasets (100 sites, 2/3/4/5-tab), closed-world 58,000+ instances/subset, open-world 64,000 instances/subset |
| 代码仓库 | 未开源 |
| Confidence | medium |
| 晋升状态 | 未晋升 |

---

## 1. 一句话总结

> 提出 PrismWF，一种多粒度 Patch-Based Transformer，通过多分支 CNN 提取不同时间粒度的流量特征，并设计 Router Token 引导的三层注意力机制（跨粒度交互、粒度内交互、Router 交互），在多 Tab 混合流量场景下实现 SOTA 的网站指纹攻击性能，5-tab 闭世界 MAP@5 达 91.63%。

---

## 2. 核心贡献

### 2.1 贡献列表

1. **提出 PrismWF**：面向多 Tab 混合流量的鲁棒 WF 攻击模型，显式建模并发多 Tab 浏览导致的流量混合问题。
2. **Multi-Granularity Attention Block**：基于 Transformer 的新架构，包含三层交互机制——跨粒度（粗到细）交互、粒度内 Patch 交互、Router Token 引导的双层融合，有效缓解流量混合导致的性能退化。
3. **Router Token 机制**：为每个时间粒度引入可学习的 Router Token 作为语义代理，聚合粒度级全局信息并进行跨粒度融合，最终拼接所有 Router Token 进行网站识别。
4. **大规模实验验证**：在闭世界、开放世界、混合 Tab、多种 WF 防御场景下均达到 SOTA。

### 2.2 与领域已有工作的关键区别

| 已有工作 | 差异点 | 位置 |
|---|---|---|
| BAPM (Guan et al., 2021) | BAPM 使用 Block 级建模 + 自注意力融合，PrismWF 使用多粒度 CNN + Router Token 层次化融合 | §II-A |
| TMWF (Jin et al., 2023) | TMWF 使用 DETR 风格 Transformer 编解码器，PrismWF 使用多粒度注意力块 + Router Token，无解码器 | §II-A |
| ARES (Deng et al., 2023/2026) | ARES 使用 MTAF 表示 + Top-K 稀疏注意力，PrismWF 使用 6 维时间槽表示 + 多粒度交互机制 | §II-A, §II-C |
| CountMamba (Deng et al., 2025) | CountMamba 使用 Mamba SSM，PrismWF 使用 Transformer + Router Token，在 RegulaTor 防御下更鲁棒 | §II-A, §V-D |
| DF (Sirinam et al., 2018) | DF 为单 Tab 设计，PrismWF 显式处理多 Tab 混合流量 | §II-A |

---

## 3. 研究连接

### 3.1 相关概念

- [[website-fingerprinting]]
- [[encrypted-traffic-analysis]]

### 3.2 相关方法

- [[transformer]]

### 3.3 相关任务

- [[website-fingerprinting]] (多标签变体)

### 3.4 基于哪些已有论文

- [[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]] — DF 作为特征提取 backbone 的灵感来源
- [[survey-website-fingerprinting]] — WF 领域综述参考

### 3.5 与已有 Claims 的关系

| 已有 Claim | 本论文的关系 | 位置 |
|---|---|---|
| DF CNN 特征提取器是 WF 的标准 backbone | 扩展：PrismWF 的多分支 CNN 受 DF ConvBlock 启发，但扩展为多粒度 | §IV-C |
| Transformer 在流量分析中有效 | 扩展：引入 Router Token 和多粒度注意力块改进标准 Transformer | §IV-D |

---

## 4. 关键发现与证据

### 4.1 主要实验结果

**闭世界 2-tab (Table II):**

| 指标 | PrismWF | ARES | CountMamba | TMWF | BAPM |
|------|---------|------|------------|------|------|
| P@2 | **89.46%** | 87.78% | 87.33% | 78.24% | 57.22% |
| MAP@2 | **93.10%** | 92.00% | 91.89% | 83.20% | 66.38% |

**闭世界 5-tab (Table II):**

| 指标 | PrismWF | ARES | CountMamba | TMWF | BAPM |
|------|---------|------|------------|------|------|
| P@5 | **87.54%** | 83.27% | 73.89% | 64.00% | 34.67% |
| MAP@5 | **91.63%** | 88.38% | 81.46% | 70.83% | 42.88% |

**开放世界 5-tab (Table II):**

| 指标 | PrismWF | ARES | CountMamba | TMWF | BAPM |
|------|---------|------|------------|------|------|
| P@5 | **88.52%** | 84.11% | 75.60% | 64.21% | 35.65% |
| MAP@5 | **92.33%** | 89.11% | 83.09% | 71.06% | 44.38% |

**混合 Tab 训练 - 5-tab 测试 (Table III):**

| 指标 | PrismWF | ARES | CountMamba | TMWF |
|------|---------|------|------------|------|
| P@5 | **68.12%** | 63.99% | 54.63% | 38.56% |
| MAP@5 | **79.87%** | 77.05% | 69.50% | 50.93% |

**5-tab + 防御 (Table V):**

| 防御 | P@5 (PrismWF) | P@5 (ARES) | P@5 (CountMamba) |
|------|---------------|------------|------------------|
| WTF-PAD | **77.94%** | 73.89% | 59.86% |
| Front | **83.92%** | 78.00% | 65.48% |
| RegulaTor | **53.49%** | 52.62% | 5.69% |

### 4.2 关键发现

1. **Tab 数增加时性能退化可控**：PrismWF 从 2-tab 到 5-tab P@K 仅下降约 2%，而 ARES 下降约 4.5%，CountMamba 下降约 13.4%。
2. **RegulaTor 防御下 CountMamba 崩溃**：P@2/MAP@2 均降至约 2.7%，因其因果 CNN 和 SSM 对 burst 级扰动敏感；PrismWF 保持 72.18%/78.29%。
3. **混合 Tab 训练有效**：PrismWF 在 mixed-tab 训练 + 任意 Tab 测试下仍领先所有 baseline，证明多粒度表示对异构混合条件的鲁棒性。
4. **Packet Count 是最具区分力的特征**：消融实验中单特征 MAP@2 最高（92.23%），但融合全部 6 维特征达到最优（93.10%）。
5. **Router 交互与跨粒度交互互补且不可或缺**：去除两者后 P@5 在 RegulaTor 下下降 10.23%。

---

## 5. 质量与信心评估

### 5.1 当前状态

| 维度 | 状态 | 备注 |
|------|------|------|
| 实验完整性 | 完整 | 闭/开放世界、混合 Tab、3 种防御、消融实验 |
| 写作完整性 | 完整 | 7 节结构清晰，Algorithm 伪代码完整 |
| 方法创新性 | 中 | 多粒度 + Router Token 有新意，但核心组件（CNN、MHA）为已有技术组合 |
| 实验说服力 | 强 | 在多种场景下一致优于 SOTA，消融实验充分 |
| 与已有工作的区分度 | 明确 | 明确对比 10 个 baseline，覆盖传统和深度学习方法 |

### 5.2 需要改进的地方

1. **代码未开源**：无法复现，降低可信度。
2. **仅使用 ARES 数据集**：未在独立数据集上验证泛化性。
3. **防御评估仅用模拟器**：未在真实 Tor 网络部署的防御中评估（论文自身承认此局限）。
4. **100 个监控网站规模有限**：大规模监控场景（数百/数千网站）下的表现未知。

### 5.3 是否可以考虑提交/晋升？

> [x] 方法论完整
> [x] 实验覆盖足够
> [x] 写作达到可读标准
> [x] 与已有工作区分度明确
> [x] 局限性已诚实讨论
> [ ] 代码已开源

---

## 6. 开放问题与后续计划

### 6.1 本文遗留的问题

- 大规模监控集（数百至数千网站）下的可扩展性未知。
- 现有 WF 防御主要为单 Tab 设计，缺乏针对多 Tab 场景的专用防御。
- 模拟防御与真实部署间存在差距。

### 6.2 下一步研究方向

- 结合网站间结构关系（用户浏览偏好、共访问模式）提升大规模可扩展性。
- 设计面向多 Tab 场景的专用 WF 防御机制。
- 在真实 Tor 网络部署中评估攻击与防御。

### 6.3 与我的研究主线的关系

> 本文属于 [[website-fingerprinting]] 领域的多 Tab 攻击方向，与 [[encrypted-traffic-analysis]] 中的多标签分类问题相关。对 Transformer 在流量分析中的应用提供了新思路。

---

## 7. [深度分析] 方法设计详解

### 7.1 方法整体流程

1. **鲁棒流量表示**：将原始流量 trace 按固定时间槽（20ms）离散化，提取 6 维特征矩阵 M。
2. **多粒度特征提取**：4 个并行 CNN 分支（kernel sizes [15, 11, 7, 5]），每个分支 3 个 ConvBlock，提取不同时间粒度的 Patch Token。
3. **Multi-Granularity Attention Block**（堆叠 3 层）：
   - 跨粒度交互（粗到细 Cross-Attention）
   - 粒度内交互（Patch 局部自注意力 + Router 全局交叉注意力）
   - Router 交互（全局 Router 自注意力）
4. **网站识别**：拼接所有粒度的 Router Token，线性分类器输出。

### 7.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|------|------|----------|------|------|
| 鲁棒表示 | 原始 trace x | 按 Δt=20ms 分槽，提取 6 维特征 | M ∈ R^{6×L} | 结构化流量表示 |
| 多粒度提取 | M | 4 分支 CNN (k=[15,11,7,5])，各 3 ConvBlock | F_i ∈ R^{d×N_i}, u_i ∈ R^{N_i×d} | 多分辨率 Patch Token |
| Router 注入 | u_i | 追加可学习 Router Token | u~_i ∈ R^{(N_i+1)×d} | 语义代理 |
| 跨粒度交互 | 粗粒度 u_c, 细粒度 u_f | 局部 Cross-Attention (窗口 w=3) | u'_c | 粗到细信息补充 |
| 粒度内交互 | u'_i, v'_i | Patch 局部自注意力 + Router 全局交叉注意力 | u_loc_i, v_glob_i | 局部时序 + 全局语义 |
| Router 交互 | 所有 Router Token | 全局自注意力 | R' | 跨粒度语义融合 |
| 网站识别 | 所有 Router Token | 拼接 + 线性投影 | logits o | 多标签分类 |

### 7.3 模型模块表格

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|------|------|------|------|----------------|
| Robust Trace Representation | 流量离散化+特征提取 | 原始 trace | M ∈ R^{6×L} | 后续所有模块的输入 |
| Multi-Branch CNN | 多粒度特征提取 | M | u_i ∈ R^{N_i×d} | 喂入 Multi-Granularity Attention Block |
| Router Token | 粒度级语义聚合 | 初始化为可学习向量 | v_i ∈ R^{1×d} | 与 Patch Token 交互，最终用于分类 |
| Inter-Granularity Interaction | 粗到细信息补充 | 粗/细粒度 Patch Token | 更新的粗粒度表示 | 仅 Patch Token 参与 |
| Intra-Granularity Interaction | 粒度内时序建模 | Patch + Router Token | 局部+全局表示 | 双分支：Patch 局部 + Router 全局 |
| Inter-Granularity Router Interaction | 跨粒度语义融合 | 所有 Router Token | 融合后 Router Token | 全局自注意力 |
| Website Identification | 分类输出 | 拼接的 Router Token | logits | 支持单/多 Tab |

### 7.4 公式、算法和机制解释

**1. 鲁棒流量表示 (Eq. 2)**

$$\mathbf{M} = \phi(\mathbf{x}) \in \mathbb{R}^{6 \times L}$$

将原始 trace x = {f_1, ..., f_N}（f_i = <d_i, t_i>）按时间槽 Δt 离散化。每个时间槽提取 6 维特征：
- Packet-level 统计（4 维）：入/出方向包计数、出→入/入→出方向转换计数
- 时间间隔特征（2 维）：出→入/入→出转换的平均时间间隔

**2. 多粒度 CNN 特征提取 (Eq. 3-4)**

$$\mathbf{F}_i = \mathrm{CNN}_i(\mathbf{M}) \in \mathbb{R}^{d \times N_i}$$

4 个并行分支（kernel sizes [15, 11, 7, 5]），每个含 3 个 ConvBlock（Conv1D + BN + ReLU + MaxPool + Dropout）。不同 kernel size 产生不同数量的 Patch Token N_i，对应不同时间粒度。

**3. Router Token 注入 (Eq. 5-6)**

$$\tilde{\mathbf{u}}_i = [\mathbf{u}_i; \mathbf{v}_i] \in \mathbb{R}^{(N_i+1) \times d}$$

为每个粒度引入可学习 Router Token v_i，追加到 Patch Token 序列末尾，作为粒度级语义代理。

**4. 跨粒度交互 — 粗到细 Cross-Attention (Eq. 7-9)**

$$c_n = \left\lfloor (n + 0.5) \frac{N_f}{N_c} \right\rfloor$$

粗粒度 Patch Token 作为 Query，对齐到细粒度序列的局部窗口（窗口大小 w），进行局部多头交叉注意力。偏移 +0.5 使粗粒度 Token 对齐到对应细粒度区域的时间中心。

**5. 粒度内交互 — 双分支 (Eq. 10-11)**

- Patch 局部自注意力：MHA_local(u'_i, u'_i, u'_i) 捕获短程时序依赖
- Router 全局交叉注意力：MHCA(v'_i, u_loc_i, u_loc_i) 聚合全局语义

**6. Router 交互 — 全局自注意力 (Eq. 13-15)**

$$\mathbf{R}' = \mathrm{MHA}_{\mathrm{global}}(\mathbf{R}, \mathbf{R}, \mathbf{R})$$

所有 Router Token 拼接后进行全局自注意力，更新后的 Router Token 回写到对应粒度。

**7. 分类损失 (Eq. 16)**

$$\mathcal{L} = \begin{cases} \mathrm{CE}(\mathbf{o}, y) & \text{single-tab} \\ \mathrm{BCEWithLogits}(\mathbf{o}, \mathbf{y}) & \text{multi-tab} \end{cases}$$

单 Tab 用交叉熵，多 Tab 用带 Logits 的二元交叉熵（multi-hot 标签）。

---

## 8. [深度分析] 实验详细分析

### 8.1 实验设计和设置

- **硬件**：NVIDIA A800-SXM4-80GB GPU
- **软件**：Python 3.10.19 + PyTorch 2.1.2，代码量 2000+ 行
- **训练策略**：单 Tab 50 epochs，多 Tab 80 epochs
- **评估指标**：P@K（Top-K 精度）、MAP@K（Top-K 平均精度均值）

### 8.2 数据集详情

| 数据集 | 说明 |
|--------|------|
| ARES 2-tab | 100 monitored sites, 58,000+ instances (closed-world), 64,000 (open-world) |
| ARES 3-tab | 同上 |
| ARES 4-tab | 同上 |
| ARES 5-tab | 同上 |
| Mixed-tab | 从每个子数据集随机采样 30% 合并训练 |

### 8.3 Baseline 选择理由

| Baseline | 类型 | 选择理由 |
|----------|------|----------|
| AWF, DF, Var-CNN, TikTok, RF | 单 Tab 攻击 | 经典 DL 方法，适配多 Tab 后作为基线 |
| Holmes | 单 Tab 攻击 | 基于时空分布分析的早期阶段 WF |
| BAPM | 多 Tab 攻击 | 首个 DL 多 Tab WF（Block 注意力） |
| TMWF | 多 Tab 攻击 | DETR 风格 Transformer 多 Tab WF |
| ARES | 多 Tab 攻击 | 当前 SOTA 多 Tab WF（MTAF + Top-K 注意力） |
| CountMamba | 多 Tab 攻击 | 最新 SSM 方法（Mamba）用于多 Tab WF |

### 8.4 消融实验

**特征表示消融 (Fig. 5):**

| 特征配置 | 2-tab MAP@2 | 5-tab MAP@5 |
|----------|-------------|-------------|
| Whole (6维融合) | **93.10%** | **91.63%** |
| Packet Count only | 92.23% | 89.24% |
| Transition Count only | 86.21% | 73.18% |
| Time Interval only | 84.32% | 73.06% |

**超参数消融:**
- 最大加载时间：160s 最优（P@2=89.46%），80s→160s 提升显著，160s→240s 边际递减
- 时间槽间隔：20ms 最优（P@2=89.46%），更小间隔产生更长序列但精度略有下降
- Block 数量：5 blocks 最优（P@2=90.03%），3 blocks 为默认（P@2=89.46%，平衡性能与效率）

**架构消融 (Table VI, 5-tab 场景):**

| 变体 | WTF-PAD P@5 | Front P@5 | RegulaTor P@5 |
|------|-------------|-----------|---------------|
| w/o RI + GI | 69.24% | 76.49% | 43.26% |
| w/o RI | 75.80% | 80.60% | 50.89% |
| Single-G | 73.89% | 79.41% | 48.89% |
| **Full** | **77.94%** | **83.92%** | **53.49%** |

### 8.5 关键发现与可视化

- 性能随 Tab 数增加下降缓慢：PrismWF 2-tab→5-tab P@K 仅降约 2%，远优于其他方法。
- CountMamba 在 RegulaTor 下完全失效（~2.7%），因 burst 级扰动破坏其因果结构。
- 多粒度设计的关键贡献：Single-G 变体在 RegulaTor 下 P@5 下降 4.60%。

### 8.6 局限性与失败案例

1. **规模限制**：仅评估 100 个监控网站，大规模场景未知。
2. **模拟防御**：未在真实 Tor 部署的防御中评估。
3. **RegulaTor 仍有挑战**：P@5=53.49%，表明 burst 级防御对本方法仍有一定效果。
4. **代码未开源**：可复现性存疑。

---

## 9. 证据记录

| 编号 | 证据内容 | 出处位置 | 备注 |
|------|----------|----------|------|
| E1 | PrismWF 闭世界 2-tab P@2=89.46%, MAP@2=93.10% | Table II | SOTA，超 ARES 1.68%/1.10% |
| E2 | PrismWF 闭世界 5-tab P@5=87.54%, MAP@5=91.63% | Table II | SOTA，超 ARES 4.27%/3.25% |
| E3 | PrismWF 开放世界 5-tab P@5=88.52%, MAP@5=92.33% | Table II | 优于闭世界，说明 unmonitored 类处理良好 |
| E4 | 混合 Tab 训练 5-tab 测试 P@5=68.12%, MAP@5=79.87% | Table III | 最具现实意义的设置 |
| E5 | 5-tab + WTF-PAD: P@5=77.94% | Table V | 超 ARES 4.05% |
| E6 | 5-tab + Front: P@5=83.92% | Table V | 超 ARES 5.92% |
| E7 | 5-tab + RegulaTor: P@5=53.49% | Table V | 超 ARES 0.87%，CountMamba 仅 5.69% |
| E8 | 2-tab + RegulaTor: PrismWF P@2=72.18%, CountMamba ~2.7% | Table IV | CountMamba 在 RegulaTor 下崩溃 |
| E9 | Packet Count 单特征 MAP@2=92.23% | Fig. 5 | 最具区分力的特征 |
| E10 | 去除 RI+GI 后 RegulaTor P@5 下降 10.23% | Table VI | 多粒度+Router 交互不可或缺 |
| E11 | 最大加载时间 160s 达最优，240s 边际递减 | Fig. 4a | |
| E12 | 时间槽间隔 20ms 最优 | Fig. 4b | |
| E13 | 5 blocks 最优 P@2=90.03%，3 blocks 默认 P@2=89.46% | Fig. 4c | 平衡性能与效率 |

---

## 10. 原始资料链接

- PDF：
- MinerU Markdown：`02-parsed-markdown/2026-arXiv-PrismWF__A_Multi-Granularity_Patch-Based_Transformer_for_Robust_Website_Fingerprinting_Attack.md`
- 代码仓库：未开源
- 补充材料：

---

## 11. 研究动机链分析

### 11.1 问题发现路径

| 阶段 | 内容 | 证据来源 |
|------|------|----------|
| 现象观察 | 现有 WF 攻击主要为单 Tab 设计，假设用户一次只访问一个网站 | §1 |
| 痛点提炼 | (1) 真实场景中多 Tab 并发浏览导致流量混合，单 Tab 模型性能严重退化；(2) 已有多 Tab 方法缺乏鲁棒的流量表示设计或未充分考虑混合流量特性；(3) 部分方法需要知道并发网站数量（不现实假设） | §1 第三段 |
| 问题转化 | 从"单 Tab 网站识别"转化为"多 Tab 混合流量下的多标签网站识别"——核心科学问题：如何在混合流量中隔离各网站的指纹模式？ | §1 |
| 文献定位 | 位于 WF 攻击从单 Tab 向多 Tab 演进的前沿。BAPM (2021) → TMWF (2023) → ARES (2023/2026) → CountMamba (2025) → PrismWF (2026)，每次迭代引入新的特征表示或模型架构 | §II-A |

### 11.2 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|------|----------|----------|----------|
| 核心假设 | 多粒度特征提取 + Router Token 引导的层次化注意力机制能有效建模混合流量中的跨网站交互模式 | (1) 不同网站的流量模式在不同时间尺度上具有不同的可区分性；(2) 粗粒度特征提供全局上下文，细粒度特征保留细节；(3) Router Token 可作为粒度级语义代理进行跨粒度融合 | Table II 全场景 SOTA |
| 辅助假设 1 | 6 维时间槽表示比纯方向序列或全局统计特征更鲁棒 | TAM 表示的成功经验（Shen et al., 2023）；时间槽级特征可捕获局部时序动态 | Fig. 5 消融实验 |
| 辅助假设 2 | 粗到细的跨粒度交互比全局注意力更适合混合流量 | 混合流量中不同网站主导不同时间片段，粗粒度提供上下文定位，细粒度提供细节 | Table VI 去除 GI 后性能下降 |

假设验证结果：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|------|-----------|-------------|------|
| 核心假设 | 强支撑 | 闭/开放世界、混合 Tab、防御场景全 SOTA | Table II-V |
| 辅助假设 1 | 支撑 | 6 维融合 > 任意单特征；比 DF 方向序列表示更鲁棒 | Fig. 5 |
| 辅助假设 2 | 支撑 | 去除 GI 后 RegulaTor P@5 下降 10.23% | Table VI |

---

## 12. 全文叙事分析

### 12.1 主线故事线

1. **背景铺垫**：Tor 匿名网络中的 WF 攻击已从传统 ML 演进到深度学习，单 Tab 场景准确率接近饱和。
2. **转折引入**：真实浏览中用户同时打开多个 Tab，导致流量混合，单 Tab 模型性能严重退化。
3. **核心主张**：提出多粒度 Patch-Based Transformer，通过多分支 CNN 提取不同时间尺度特征，用 Router Token 引导的三层注意力机制进行层次化信息融合。
4. **关键结果**：在闭世界/开放世界/混合 Tab/多种防御场景下均达到 SOTA，5-tab 性能退化可控。
5. **启示与呼吁**：WF 防御需要为多 Tab 场景重新设计，当前防御在多 Tab 设置下效果有限。

### 12.2 章节叙事功能表

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|------|----------|------------|------------|
| §I Introduction | 问题导入 + 动机 + 贡献 | 从单 Tab 局限性切入多 Tab 问题 | "single-tab attack models are inherently limited" |
| §II Related Work | 文献定位 | 建立"已有方法不够好"的铺垫 | 区分单 Tab/多 Tab/防御三线并行 |
| §III Threat Model | 研究边界 | 明确多 Tab、被动攻击者、闭/开放世界假设 | 引入 mixed-tab 现实假设 |
| §IV Methodology | 方法详解 | 四个组件逐步展开：表示→提取→注意力→分类 | Router Token 机制的引入 |
| §V Experiments | 核心论证 | 多维度实验：Tab 数、防御、消融 | Table II 5-tab 结果，Table V RegulaTor 结果 |
| §VI Discussion | 局限性 + 未来方向 | 诚实讨论三大局限 | 承认模拟防御的差距 |
| §VII Conclusion | 总结 | 回扣多 Tab + 多粒度主题 | |

### 12.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|----------|----------|----------|------|
| 应用 Gap | 真实场景多 Tab 浏览导致流量混合，单 Tab 模型失效 | 直接陈述 + 引用 prior work 的实验结果 | §1 第三段 |
| 方法论 Gap | 已有多 Tab 方法缺乏鲁棒表示或未考虑混合特性 | 逐条列举 BAPM/TMWF/ARES 的局限 | §1 第三段 |
| 假设 Gap | 部分方法需要知道并发网站数量（不现实） | 直接指出该假设的不合理性 | §1 第三段 |

### 12.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|----------|----------|-------------|
| 闭世界多 Tab (§V-B) | 建立基线优越性 | 证明在标准设置下 SOTA |
| 开放世界 (§V-B.2) | 应对"闭世界不现实"的批评 | 证明对 unmonitored 类的鲁棒性 |
| 混合 Tab (§V-C) | 最具现实意义的验证 | 证明未知 Tab 数时仍有效 |
| 防御场景 (§V-D) | 鲁棒性验证 | 证明在流量混淆下仍有效 |
| 消融实验 (§V-E) | 建立因果关系 | 证明每个组件的贡献 |

### 12.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|------|----------|-----------------|
| 多粒度设计论证 | 从"不同时间尺度有不同信息"出发，用 CNN kernel size 变化实现多粒度 | "数据 X 在不同尺度 Y 上有不同的可区分性"——用多分支架构显式建模多尺度 |
| Router Token 设计 | 借鉴 DETR 的 Object Query 思想，但改为粒度级语义代理 | "为每个子问题引入一个可学习的代理 Token"——用 Token 聚合子问题的全局信息 |
| 实验递进结构 | 标准→挑战（Tab 增加）→更挑战（混合 Tab）→最强挑战（+防御） | 从理想条件逐步推向真实场景 |
| 消融实验设计 | 组件消融（RI/GI/Single-G）+ 特征消融 + 超参数消融 | 三维消融覆盖：架构组件、输入特征、超参数 |

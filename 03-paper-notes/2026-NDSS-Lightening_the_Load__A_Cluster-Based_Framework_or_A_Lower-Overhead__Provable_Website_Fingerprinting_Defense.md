---
type: paper
title_original: "Lightening the Load: A Cluster-Based Framework for A Lower-Overhead, Provable Website Fingerprinting Defense"
title_cn: "减负：基于聚类的低开销可证明网站指纹防御框架"
authors: ["Khashayar Khajavi", "Tao Wang"]
year: 2026
venue: "NDSS 2026"
doi: "10.14722/ndss.2026.241760"
url: "https://www.ndss-symposium.org/ndss2026/"
pdf: ""
mineru_md: "02-parsed-markdown/2026-NDSS-Lightening_the_Load__A_Cluster-Based_Framework_or_A_Lower-Overhead__Provable_Website_Fingerprinting_Defense.md"
status: processed
reading_level: L3
relevance: high
research_area: ["network privacy", "website fingerprinting", "Tor anonymity", "traffic analysis"]
task: ["website fingerprinting defense", "adaptive padding", "provable security"]
method: ["pattern-level clustering", "k-anonymity", "l-diversity", "early time-series classification", "global-to-local regularization"]
dataset: ["Sirinam et al. (95 sites, 1000 traces/site)", "AWF (100 sites, 2500 traces/site)", "Overdorf et al. onion service (100 sites)"]
code: "https://github.com/khashayarkhaj/Adaptive-Tamaraw"
related_papers: []
kb_read_only: true
promoted_to: ""
created: "2026-06-21"
updated: "2026-06-21"
---

# Lightening the Load: A Cluster-Based Framework for A Lower-Overhead, Provable Website Fingerprinting Defense

> **个人论文笔记** — 本笔记严格隔离于主知识库。
> `kb_read_only: true`：本笔记可链接到主知识库页面，但不会触发主知识库的任何更新。
> 如需晋升至主知识库，须满足 `publication_status: published/accepted` + `my_confidence: high` + 用户主动要求。

---

## 0. 基础信息

| 字段 | 内容 |
|---|---|
| 标题 | Lightening the Load: A Cluster-Based Framework for A Lower-Overhead, Provable Website Fingerprinting Defense |
| 作者 | Khashayar Khajavi, Tao Wang (Simon Fraser University) |
| 年份 | 2026 |
| 目标/发表 venue | NDSS 2026 (Network and Distributed System Security Symposium) |
| 发表状态 | published |
| DOI | 10.14722/ndss.2026.241760 |
| 关键词 | website fingerprinting defense, adaptive regularization, k-anonymity, l-diversity, provable security, Tamaraw, clustering, early time-series classification |
| 数据集 | Sirinam et al. (95 sites x 1000 traces), AWF top 100 (100 sites x 2500 traces), Overdorf et al. onion service (100 sites) |
| 代码仓库 | https://github.com/khashayarkhaj/Adaptive-Tamaraw |
| 研究方向 | [[website-fingerprinting-defense]], [[website-fingerprinting]], [[encrypted-traffic-analysis]] |
| Confidence | high |
| 晋升状态 | 未晋升 |

---

## 1. 一句话总结

> 提出 Adaptive Tamaraw，一种基于 global-to-local 策略的自适应 WF 防御框架：先以全局保守参数保护早期流量，再通过模式级聚类构建 (k,l)-多样性匿名集、结合 ECDIRE 早期时序分类器检测匿名集并切换至轻量局部参数；在保留 Tamaraw 信息论安全保证的同时，将总开销最高降低 99 个百分点，高隐私模式下将攻击者准确率压至 30% 以下。

---

## 2. 核心贡献

### 2.1 贡献列表

1. **统一设计框架**：提出首个同时融合正则化防御（固定速率填充）和超序列防御（匿名集分组）优势的自适应 WF 防御框架，实现全局到局部的参数切换
2. **形式化安全分析**：推导 weighted delta-non-injectivity 的全局定理，证明自适应切换后攻击者平均成功概率仍受信息论上界约束，上界由匿名集大小和多样性决定
3. **Adaptive Tamaraw 实例化**：在 Tamaraw 基础上引入模式级聚类（改进 CAST 算法）、(k,l)-多样性匿名集生成（Algorithm 1）、Holmes + kFP 两级早期分类器
4. **灵活的隐私-效率权衡**：通过调节 k 值，高隐私模式（k 大）将攻击者准确率压至 30% 以下，高效率模式（k 小）将总开销降低最高 99 个百分点
5. **Out-of-training 泛化**：首次证明匿名集防御可泛化至训练集外的未见网页，突破超序列方法仅限训练集内网页的限制

### 2.2 与领域已有工作的关键区别

| 已有工作 | 差异点 | 位置 |
|---|---|---|
| Tamaraw (Cai et al., CCS 2014) | Tamaraw 使用全局固定参数，Adaptive Tamaraw 根据聚类动态切换参数，保留信息论保证的同时大幅降低开销 | §V-B |
| Palette (Shen et al., IEEE S&P 2024) | Palette 在网页级聚类并构建超序列，仅保护训练集内网页；本文在模式级聚类，泛化到 out-of-training 网页 | §V-D |
| Super-Sequence (Wang et al., USENIX 2014) | 超序列方法仅保护训练集内网页；本文通过正则化基础 + 动态聚类实现对任意网页的保护 | §II-B2 |
| Walkie-Talkie (Wang & Goldberg, USENIX 2017) | Walkie-Talkie 需要预先知道完整流量轨迹，且随机化版本失去对抗性上界；本文不需要预先知道轨迹 | §II-B2 |

---

## 3. 研究连接（Research Connection）

### 3.1 相关概念

- [[website-fingerprinting-defense]] — 本文核心研究领域，提出一种兼具可证明安全性和实用效率的新型防御方案
- [[website-fingerprinting]] — 本文所对抗的攻击类型，包括 DF、Tik-Tok、RF、LASERBEAK 等现代深度学习攻击
- [[encrypted-traffic-analysis]] — 流量分析的上位概念，WF 防御是其重要研究方向
- [[survey-website-fingerprinting]] — WF 领域综述，本文 Table I 提供了防御方法的综合对比

### 3.2 相关方法

- [[k-anonymity]] — 匿名集构造的核心隐私模型，每个匿名集包含至少 k 个不同流量模式
- [[l-diversity]] — 确保匿名集内模式来自至少 l 个不同网页，防止标签同质化
- [[CAST-clustering]] — 改进的 Cluster Affinity Search Technique，用于网页内模式检测
- [[ECDIRE]] — 早期时序分类框架，用于在安全时间点从全局参数切换到局部参数
- [[Holmes]] — 空间-时间 CNN 编码器，用于早期网页级预测
- [[k-fingerprinting]] — 轻量随机森林分类器，用于细粒度模式预测

### 3.3 相关任务

- [[website-fingerprinting-defense]] — WF 防御的设计与评估

### 3.4 基于哪些已有论文

- Tamaraw (Cai et al., CCS 2014) — 本文的基线防御，提供信息论安全保证，Adaptive Tamaraw 在其基础上改进
- Palette (Shen et al., IEEE S&P 2024) — 提供 k-匿名聚类算法的基础，本文进行模式级和多样性距离度量的改进
- ECDIRE (Mori et al., DMKD 2017) — 早期时序分类框架，本文适配用于 WF 场景的匿名集检测
- Holmes (Deng et al., CCS 2024) — 空间-时间 CNN，用于早期网页预测
- RF (Shen et al., USENIX 2023) — 当前最强 WF 攻击之一，用于评估防御效果

### 3.5 与已有 Claims 的关系

| 已有 Claim | 本论文的关系 | 位置 |
|---|---|---|
| 无形式化保证的防御总被更强攻击打破 (Table I) | 支撑 — 本文保留 Tamaraw 的信息论保证作为理论基础 | §II-B, §VI-D |
| 超序列方法仅限训练集内网页 (Wang et al., 2014; Palette) | 反驳 — 本文通过正则化基础 + 动态聚类实现 out-of-training 泛化 | §VI-C |
| 固定速率正则化导致过高开销 (Tamaraw 原文) | 改进 — 自适应参数切换将开销降低最高 99 个百分点 | §VI-B |
| WF 防御缺乏可证明安全性 (大多数经验性防御) | 弥补 — 提供 Theorem V.1 全局非均匀加权 delta-non-injectivity 证明 | §V-F, Appendix E |

---

## 4. 关键发现与证据

### 4.1 主要实验结果

**表 III：静态 Tamaraw vs Adaptive Tamaraw 平均开销对比（in-training）**

| 数据集 | L | Tamaraw BW | Tamaraw Time | AT(k=2) BW | AT(k=2) Time | AT(k=7) BW | AT(k=7) Time | AT(k=30) BW | AT(k=30) Time |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Sirinam et al. | 100 | 158% | 83% | 136% (-22) | 68% (-15) | 144% (-14) | 74% (-9) | 157% (+1) | 77% (-6) |
| Sirinam et al. | 500 | 198% | 98% | 176% (-22) | 86% (-12) | 184% (-14) | 86% (-11) | 196% (-2) | 87% (-11) |
| Sirinam et al. | 1000 | 258% | 199% | 223% (-35) | 135% (-64) | 235% (-23) | 144% (-55) | 248% (-10) | 150% (-49) |
| AWF | 100 | 151% | 153% | 100% (-51) | 111% (-42) | 109% (-42) | 123% (-30) | 125% (-26) | 135% (-18) |
| AWF | 500 | 157% | 183% | 122% (-35) | 147% (-36) | 132% (-25) | 155% (-28) | 141% (-16) | 172% (-6) |
| AWF | 1000 | 182% | 207% | 145% (-37) | 154% (-53) | 157% (-25) | 162% (-45) | 169% (-13) | 182% (-25) |

**表 IV：固定时间开销约束下的最小带宽开销（Sirinam et al. 数据集）**

| 方法 | <10% Time | <45% Time | <125% Time | <250% Time | AUC |
|---|---:|---:|---:|---:|---:|
| Tamaraw | 279% | 124% | 83% | 66% | 82% |
| Adaptive Tamaraw (out-of-training) | 277% (-2) | 119% (-5) | 80% (-3) | 64% (-2) | 79% (-3) |
| Adaptive Tamaraw (in-training) | 227% (-52) | 110% (-14) | 72% (-11) | 61% (-5) | 68% (-14) |

**表 V：理论安全上界 vs 实际 WF 攻击准确率（k=7, L=100）**

| rho_out | rho_in | 理论上界 | kFP | Tik-Tok | RF | LASERBEAK |
|---:|---:|---:|---:|---:|---:|---:|
| 0.012 | 0.030 | 41% | 31% | 20% | 39% | 31% |
| 0.009 | 0.010 | 43% | 33% | 21% | 38% | 32% |
| 0.010 | 0.020 | 42% | 31% | 22% | 40% | 30% |
| 0.030 | 0.120 | 35% | 20% | 15% | 33% | 23% |

**表 VI：Out-of-training 开销对比（Normal vs Onion 网站）**

| 网站类型 | 方法 | <20% Time | <45% Time | <125% Time | <200% Time |
|---|---|---:|---:|---:|---:|
| Normal | Tamaraw | 168% | 124% | 83% | 67% |
| Normal | Adaptive | 166% (-2) | 119% (-5) | 80% (-3) | 67% (0) |
| Onion | Tamaraw | 195% | 120% | 78% | 66% |
| Onion | Adaptive | 187% (-8) | 116% (-4) | 77% (-1) | 65% (-1) |

### 4.2 消融实验

**表 VII：CAST 算法改进效果**

| 变体 | 平均聚类大小 | 小聚类比例 | 最大/最小比 |
|---|---:|---:|---:|
| Baseline (Raw) | 13 | 81.9% | 200 |
| + Dynamic Threshold | 70 | 64.3% | 633 |
| + Cleaning Step | 74 | 13.6% | 27.7 |
| + Post Processing | 200 | 0.2% | 3.83 |

**表 VIII：alpha 敏感性分析**

| 指标 | alpha=0.6 | alpha=0.7 | alpha=0.8 | alpha=0.9 | alpha=1.0 |
|---|---:|---:|---:|---:|---:|
| 开销改进 | -34% | -32% | -27% | -25% | -15% |
| tau_s 攻击者准确率 | 41% | 39% | 38% | 36% | 34% |

**表 IX：网页级 vs 模式级聚类总开销对比**

| 粒度 | k=2 | k=7 | k=30 |
|---|---:|---:|---:|
| Website Level | 219% | 229% | 243% |
| Pattern Level | 205% | 217% | 235% |

**表 X：计算与资源开销**

| 指标 | 数值 |
|---|---|
| Holmes 模型大小 | 8.21 MB |
| kFP 模型大小（每个实例） | 0.41 MB |
| 总推理延迟（每次决策） | 1.84 ms |
| 每站点平均安全时间戳数 | 4.09 |

---

## 5. 方法细节

### 5.1 整体架构：Global-to-Local 策略

防御分为三个阶段：

1. **Intra-Webpage Pattern Detection（网页内模式检测）**：使用改进 CAST 算法对每个网页的流量轨迹进行聚类，提取反复出现的流量模式
2. **Anonymity Set Generation（匿名集生成）**：将不同网页的模式聚类为满足 k-anonymity 和 l-diversity 的匿名集，为每个集合预计算轻量局部参数
3. **Early Anonymity Set Detection（早期匿名集检测）**：使用 Holmes + kFP 两级分类器在安全时间点从全局参数切换到局部参数

### 5.2 改进 CAST 算法（四项修改）

| 修改 | 目的 |
|---|---|
| Local Scaling（自适应 sigma） | 使用 K 近邻距离替代全局 sigma，适应不同数据密度 |
| Cleaning Step | 每个点重新分配到亲和力最高的聚类，消除错误归属 |
| Post Processing | 基于扩展比 phi 合并最小聚类，限制聚类数量 |
| Dynamic Affinity Threshold | 使用全局平均相似度作为自适应阈值，避免手动调参 |

### 5.3 匿名集生成（Algorithm 1）

- **模式级聚类**：在 intra-webpage cluster（模式）而非网页级进行聚类，产生更均匀的分组
- **多样性感知距离度量**：定义 d(C,p) 为合并候选模式 p 后在所有 (p_in, p_out) 配置上的平均攻击者准确率，隐式增强 l-diversy
- **贪婪策略**：每次选择最小化 d(C,p) 的候选模式加入当前匿名集

### 5.4 早期匿名集检测（ECDIRE 适配）

- **Stage A — Holmes**：空间-时间 CNN 编码器，监督对比学习，预测最可能的网页 w
- **Stage B — kFP**：每个 (网页, 时间戳) 对训练一个轻量随机森林，识别细粒度模式 p
- **安全时间点 tau_S**：对每个匿名集 S，计算最早可达到 alpha * A_S^full 准确率的时间点
- **单次切换规则**：每个匿名集绑定唯一安全时间点，避免时序侧信道

### 5.5 安全定理

**Theorem V.1**：设 S 为匿名集集合，delta = 1 / E_{S_i} [A_bar(S_i; p_in, p_out)]，则 Adaptive Tamaraw 是非均匀加权 delta-non-injective 的，攻击者平均成功概率 Pr[success] <= 1/delta。

核心洞察：切换机制本身确实会泄露匿名集身份（95.64% 准确率），但匿名集内的 k-anonymity 和 l-diversity 仍然足以约束攻击者成功率。

---

## 6. 实验设计

### 6.1 数据集

| 数据集 | 规模 | 来源 | 用途 |
|---|---|---|---|
| Sirinam et al. | 95 sites x 1000 traces | Tor 真实连接 | 主要评估（in-training + out-of-training） |
| AWF | 100 sites x 2500 traces | Tor 真实连接 | 大规模 in-training 评估 |
| Overdorf et al. onion | 100 sites | Tor onion 服务 | Out-of-training 泛化验证 |

### 6.2 参数配置

- L（长度桶参数）：{100, 500, 1000}
- rho_in 搜索范围：[0.001, 0.006]
- rho_out 搜索范围：[0.005, 0.21]
- Pareto 最优配置数：Sirinam 33 个，AWF 40 个
- k（匿名集大小）：2 到 30
- alpha（ECDIRE 置信阈值）：0.9
- TAM 时间槽：80ms

### 6.3 评估场景

1. **In-training**：训练集和测试集来自同一组网页（8:1:1 分割）
2. **Out-of-training**：训练集和测试集来自完全不同的网页（50/50 分割）
3. **Onion service 泛化**：用 Sirinam 数据集训练，在 onion 服务流量上测试

---

## 7. 局限性与未来方向

### 7.1 当前局限

| 局限 | 说明 |
|---|---|
| 切换时序泄露 | 切换机制泄露匿名集身份（95.64% 准确率），虽然安全定理已考虑此泄露 |
| k 增大时开销优势减弱 | 大 k 匿名集包含更多异构模式，自适应参数的局部优势被稀释 |
| 依赖预训练数据集 | 匿名集构建和分类器训练需要离线阶段的标注数据 |
| 非切换轨迹（9%） | 约 9% 的轨迹被分配到错误匿名集，10% 未触发切换而使用全局参数 |

### 7.2 未来方向

- 更先进的表示学习增强模式检测
- 新型聚类算法优化匿名集生成
- 作为 Tor Pluggable Transport（WFDefProxy 框架）的实际部署
- 推理延迟 <2ms，适合 Tor Browser 集成

---

## 8. 方法论评估

### 8.1 实验严谨性

| 维度 | 评分 | 说明 |
|---|---|---|
| 数据集多样性 | 高 | 三个独立数据集，涵盖标准网页和 onion 服务 |
| 对比公平性 | 高 | 与原始 Tamaraw 在相同配置下对比，使用 Pareto 最优参数 |
| 消融实验 | 完整 | CAST 改进、alpha 敏感性、模式级 vs 网页级聚类均有消融 |
| 理论-实验一致性 | 高 | Table V 显示所有攻击者准确率均低于理论上界 |

### 8.2 复现性

| 维度 | 状态 |
|---|---|
| 代码开源 | 是（GitHub） |
| 数据集公开 | 是（Sirinam, AWF 均为公开数据集） |
| 超参数完整 | 是（Table II） |
| 计算资源明确 | 是（AMD EPYC 9454 + NVIDIA H100） |

---

## 9. 引用建议

### 9.1 适用场景

- 设计兼具可证明安全性和实用效率的 WF 防御
- WF 防御中的自适应参数选择
- 匿名集构造中的 k-anonymity 和 l-diversy 应用
- WF 防御的 out-of-training 泛化问题

### 9.2 关键引用

| 场景 | 引用 |
|---|---|
| 框架设计 | Khajavi & Wang, NDSS 2026, Section V |
| 安全定理 | Khajavi & Wang, NDSS 2026, Theorem V.1 / Appendix E |
| 实验对比 | Khajavi & Wang, NDSS 2026, Table III, V |

---

## 10. 与其他笔记的关联

### 10.1 本领域相关论文

| 论文 | 关系 |
|---|---|
| CELLSHIFT (NDSS 2026) | 同期 WF 研究，CELLSHIFT 关注攻击侧数据增强，本文关注防御侧自适应 |
| Cease at the Ultimate Goodness (NDSS 2026) | 同期 WF 防御研究，可对比方法论 |
| Tamaraw (CCS 2014) | 本文的基线防御和理论基础 |
| Palette (IEEE S&P 2024) | 本文的聚类算法基础来源 |

### 10.2 知识图谱位置

```
encrypted-traffic-analysis
  └── website-fingerprinting
        ├── website-fingerprinting-defense
        │     ├── regularization-based: Tamaraw → Adaptive Tamaraw (本文)
        │     ├── supersequence-based: Super-Sequence, Palette
        │     └── hybrid: 本文框架
        └── website-fingerprinting-attack
              ├── DF, Tik-Tok, RF, LASERBEAK (本文评估对象)
              └── CELLSHIFT (数据增强)
```

---

## 11. 关键公式与定义

### 11.1 核心定义

**Weighted Pre-image Size (Eq. 1)**：
delta_tilde(f') = |D^{-1}(f')| / max_w |D_w^{-1}(f')|

衡量每个被合并输入对应的多数网页占比倒数。delta_tilde = 1 表示完美信息攻击者总能猜对。

**Non-Uniformly Weighted delta-Non-Injectivity**：
E_{f'} [1/delta_tilde(f')] <= 1/delta

攻击者平均成功概率受 delta 约束。

### 11.2 关键定理

**Theorem V.1 (Global Non-Uniformly Weighted delta-Non-Injectivity)**：
1/delta = E_{S_i ~ S} [A_bar(S_i; p_in, p_out)]
Pr[success] <= 1/delta

安全上界由匿名集上的平均攻击者成功率决定。

---

## 12. 开放问题

1. 切换时序泄露是否可通过随机化切换时间点缓解？（论文提到单次切换规则关闭了时序侧信道，但匿名集身份仍可推断）
2. 模式级聚类在更大规模网页集（如 1000+ 站点）上的可扩展性如何？
3. 与最新 Transformer-based WF 攻击（如 WF-Transformer）的对抗效果如何？
4. 在 Tor 真实网络部署中，网络抖动和拥塞对早期分类器精度的影响？
5. 是否可将框架实例化为其他正则化防御（如 RegulaTor）而非仅 Tamaraw？

---

## 13. 阅读备注

### 13.1 阅读笔记

- 本文的核心创新在于将正则化防御的"普适性"和超序列防御的"可证明安全性"统一到一个框架中，同时解决了超序列方法仅限训练集内网页的限制
- Table I 是领域内非常有价值的防御方法综合对比表，清晰展示了"低开销 vs 可证明安全性"的二元困境
- 模式级聚类是关键设计洞察：同一网页可产生多种流量模式（CDN、广告、本地化），传统网页级聚类忽略了这一多样性
- 安全定理的证明思路清晰：切换泄露已被纳入安全模型，匿名集内的 k,l-多样性是安全性的真正来源
- 实验结果中 RF (Robust Fingerprinting) 是最接近理论上界的攻击，说明 RF 的 2xN TAM 表示与本文的 TAM 表示有相似的信息捕获能力

### 13.2 待验证

- Table V 中 rho_out=0.030, rho_in=0.120 配置下理论上界为 35%，实际攻击最高为 33%（RF），差距较小，需确认是否为配置特例
- Out-of-training 场景下理论上界（31%）低于 in-training（45%），论文给出的解释（退化为原始 Tamaraw 行为）是否充分

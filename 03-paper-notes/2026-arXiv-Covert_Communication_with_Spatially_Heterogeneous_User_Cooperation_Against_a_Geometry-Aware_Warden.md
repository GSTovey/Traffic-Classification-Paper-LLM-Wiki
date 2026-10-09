---
type: paper
title_original: "Covert Communication with Spatially Heterogeneous User Cooperation Against a Geometry-Aware Warden"
title_cn: "面向几何感知典狱长的空间异构用户协作隐蔽通信"
authors: ["Hyeonsik Yeom", "Jinyoung Lee"]
year: 2026
venue: "arXiv 2026"
doi: "unknown"
url: "https://arxiv.org/abs/2608.10446"
pdf: "00-inbox/PDFs/2026-arXiv-Covert_Communication_with_Spatially_Heterogeneous_User_Cooperation_Against_a_Geometry-Aware_Warden.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-Covert_Communication_with_Spatially_Heterogeneous_User_Cooperation_Against_a_Geometry-Aware_Warden.md"
status: processed
reading_level: L1
research_area: []
task: []
method: []
dataset: []
code: "unknown"
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

# Covert Communication with Spatially Heterogeneous User Cooperation Against a Geometry-Aware Warden

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Covert Communication with Spatially Heterogeneous User Cooperation Against a Geometry-Aware Warden |
| 中文标题 | 面向几何感知典狱长的空间异构用户协作隐蔽通信 |
| 作者 | Hyeonsik Yeom, Jinyoung Lee（解析稿未给出所属单位） |
| 年份 | 2026 |
| 会议/期刊 | arXiv 预印本（arXiv 2026；arXiv ID 2608.10446） |
| 研究方向 | 无线物理层安全（PLS）/ 隐蔽通信（covert communication）。KB 白名单无对应 slug（非流量分析主题），故 `research_area` / `task` / `method` 留空 |
| 任务类型 | 理论建模 + 优化算法：多个空间分布的非隐蔽用户协作干扰，掩护 Alice 向 Bob 的隐蔽传输不被 Willie 检测 |
| 方法关键词 | on–off 用户激活、大尺度衰落空间异构、检测错误概率（DEP）闭式近似、inclusion probability、piecewise search（复杂度 O(M log M)） |
| 数据集 | 无数据集；仿真采用 3GPP TR 25.996 Urban Macrocell 路损模型（PL(dB)=34.5+35log₁₀(d)） |
| 是否开源 | 未提及，`code` 记为 unknown |
| PDF | 00-inbox/PDFs/2026-arXiv-Covert_Communication_with_Spatially_Heterogeneous_User_Cooperation_Against_a_Geometry-Aware_Warden.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-arXiv-Covert_Communication_with_Spatially_Heterogeneous_User_Cooperation_Against_a_Geometry-Aware_Warden.md |

> ⚠️ MinerU 解析问题：式 (16) 附近的排序方向表述自相矛盾——正文称按比值升序（ascending order）排序，却给出 `r_{m_i} ≥ r_{m_j} for i ≥ j` 的降序条件；附录 A/伪代码又回到升序口径，无法判断是原文笔误还是解析偏差。

## 1. 一句话总结

> 把每个协作用户到典狱长 Willie 的**个体**大尺度衰落系数同时用于用户激活与检测分析：推导出 on–off 激活结构、DEP 闭式近似、最小协作用户数 K_min 与激活阈值，并将原始 M+1 维功率控制问题降为一维分段搜索（O(M log M)）；数值上比"仅看 Bob 侧信道"的基线用更少协作用户达到同样隐蔽性。

## 2. 摘要翻译

### 2.1 摘要原文

"This paper investigates covert communication in which a single covert user is assisted by multiple spatially distributed non-covert users against a geometry-aware warden. Unlike prior works based on receiver-centric activation, homogeneous channels, or averaged geometry, the proposed framework retains the individual user-to-warden large-scale fading coefficients in both cooperative user activation and the warden's detection analysis. Under the adopted analytical formulation for large-scale user deployments, we establish an on–off activation structure that balances the interference caused at Bob and the interference effectiveness at warden. ... The analysis shows that greater warden-side spatial dispersion can reduce the required cooperative users, whereas a larger average user-to-warden distance increases it. Numerical results validate the analysis and show that finite-sample detection approaches the large-sample benchmark, while imperfect user-to-Bob channel estimation mainly reduces the achievable rate through activation errors."（Abstract 节选）

### 2.2 摘要中文翻译

本文研究单一隐蔽用户（Alice）在多个空间分布的非隐蔽用户协助下、对抗几何感知典狱长（Willie）的隐蔽通信。与以往基于接收端中心式激活、同构信道或平均化几何的模型不同，本框架在协作用户激活与 Willie 检测分析中都保留**逐用户**的 user-to-warden 大尺度衰落系数。在大规模用户部署解析模型下，建立了兼顾 Bob 侧干扰代价与 Willie 侧干扰有效性的 on–off 激活结构；据此推导检测错误概率（DEP）的闭式近似、最小化 DEP 的检测阈值，以及满足隐蔽约束所需的最少协作用户数；并把原高维功率控制问题降为一维分段搜索、给出不依赖分辨率的低复杂度算法。分析表明：Willie 侧空间离散度越大，所需协作用户越少；平均 user-to-Willie 距离越大，所需协作用户越多。数值结果验证了分析，并显示有限样本检测趋近大样本基准，而不完美的 user-to-Bob 信道估计主要通过激活错误降低可达速率。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

既有协作隐蔽通信方案（[29]–[32]）要么只按 user-to-Bob 瞬时信道确定激活用户（接收端中心式），要么将所有用户的信道方差替换为公共平均值（均匀/平均几何）。但"对 Bob 造成相近干扰的用户，对 Willie 的干扰可能差异巨大"（§I），因此旧设计会选到无效用户、误估 Willie 的聚合干扰统计，进而高估所需协作用户数（Motivation 段、贡献 4）。

### 3.2 现有方法的痛点和不足

- 接收端中心式激活忽略 Willie 侧几何，可能激活对隐蔽性无益的用户（§I）。
- 均匀/平均几何分析丢失个体空间特征，导致 DEP 与最少协作用户数估计不准（§I、§IV-C 中 Corollary 2 偏大）。
- 原问题有 M+1 个优化变量、目标函数含分数式 SINR、约束是统计型（Willie 先优化自身阈值），直接搜索不可行（§II-C）。

### 3.3 论文的研究假设或核心直觉

隐蔽性取决于"Alice 引起的接收能量偏移 Δ"与"协作干扰不确定性 Σ_K"之间的平衡（§I 贡献 4、§IV）：把 Willie 侧空间异构当作设计要素而非部署细节，就能用更少的用户产生更大的干扰不确定性。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 既有协作方案或忽略 Willie 侧几何，或用平均参数抹平个体差异 | §I |
| 痛点提炼 | 错误估计 K_min 会多激活用户、抬高 Bob 侧干扰、压低隐蔽速率 | §I、§II-C |
| 问题转化 | 用激活度量 r_m=\|h_{m,b}\|²/λ_{m,w} 把 M 维功率问题降为 on–off + 阈值τ | §III Prop.1 |
| 求解与验证 | 推导 DEP 闭式 → K_min → 一维分段搜索；数值与 3GPP 模型验证 | §IV–§VI |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 最优协作功率谱是 on–off 结构（K 个用户满功率，其余静默） | KKT 条件（App. A） | Prop.1 及其证明 |
| 辅助假设 | Willie 侧空间离散度越大所需 K_min 越少；平均距离越大 K_min 越多 | Cor.1/Cor.2 的缩放律（§IV） | Fig. 4(b)(c) |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | KKT 解在边界情形吸收后即 on–off 结构；数值 DEP 曲线与 Lemma 2/3 的理论极小点吻合 | App. A、Fig. 2 |
| 辅助假设 | 支撑 | σ_d 增大 ⇒ K_min 下降；μ_d 增大 ⇒ K_min 上升；均匀近似（Cor. 2）明显高估 K_min | Fig. 4(a)–(c) |

## 4. 方法设计

### 4.1 方法整体流程

系统含 Alice（隐蔽用户）、M 个非隐蔽用户、Bob（基站）与 Willie。非隐蔽用户本用正交载波 f_m 正常通信；被选中的协作用户在 Alice 的载波 f_a 上发干扰。流程：① 用激活度量 r_m 选出 K 个协作用户（on–off）；② 推导 Willie 能量检测器的 DEP 闭式近似；③ 由隐蔽约束反解 K_min 与激活阈值 τ；④ 对 P_a 做一维分段搜索最大化隐蔽速率。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| 用户激活 | r_m=\|h_{m,b}\|²/λ_{m,w}（信道 + Willie 侧大尺度衰落） | Prop.1：r_m ≤ τ 者以 P_max 发干扰，其余静默 | 协作用户集 S（K=\|S\|） | 把 M 维功率谱降为单一阈值 τ |
| 检测分析 | 被选用户的 λ_{m,w} | Lemma 1 闭式逼近 DEP（含一/二阶 inclusion probability π_m^(K)、π_{m,n}^(K)）；Lemma 2 得 γ*=Ξ_K+σ_w²；Lemma 3 得 ζ_min | DEP 闭式表达 | 支撑隐蔽约束的解析求解 |
| 约束反解 | ζ_min ≥ 1−ε | Theorem 1：K_min = min{K: Σ_K ≥ c_εΔ²}；Cor.1/2 给均匀与同构特例闭式 | K_min 与阈值 τ（Theorem 2） | 决定最少协作用户 |
| 功率优化 | P_a | Algorithm 1：对每个 K̄ 取候选功率 P_K̄=min(P_max, √Σ_K̄/(√c_ε λ_{a,w})) 比较速率 | P_a*、K*、τ* | 复杂度 O(M log M)，避免网格分辨率误差 |

### 4.3 模型结构或系统模块

无学习模型。信道为 Rayleigh 衰落（式 (1)），大尺度衰落 λ_{x,y}=β₀d^{-α}；Bob 通过用户秘密正交导频估计 user-to-Bob 信道（式 (2)），Willie 无法获得；Willie 用能量检测统计量 T_w（式 (7)，有限 N 下服从 χ²_{2N}/(2N) 缩放）。

### 4.4 公式、算法和机制解释

- DEP 定义：ζ ≜ P_FA(γ) + P_MD(γ)（等先验），隐蔽约束为 ζ_min ≥ 1−ε（式 (5)）。
- 关键中间量：Δ = P_aλ_{a,w}（Alice 的能量偏移）、Ξ_K（聚合干扰均值）、Σ_K（聚合干扰方差，含 inclusion probability 修正，式 (19)）。
- K_min 条件 Σ_K ≥ c_εΔ²，其中 c_ε = (1/ε² − 8 + 16ε²)/(2π)（式 (24)）；均匀近似下 K_min^uni ≈ ⌈c_εP_a²λ_{a,w}²/(P_max²(E+V))⌉（式 (32)），说明 K_min 随 Willie 侧二阶统计量 E+V 下降、随 P_aλ_{a,w} 平方增长、随约束收紧按 ε⁻² 增长。

### 4.5 方法优势

- 保留个体 Willie 侧几何，选出"对 Bob 干扰便宜、对 Willie 干扰有效"的用户（§V-B）。
- 无需网格搜索：直接评估解析边界候选 P_K̄，复杂度 O(M log M)（对比网格 O(N_pM)）；Table I 中相比 N_p=10⁴ 网格获 5.70%–6.22% 速率增益。
- 结论可解释：K_min 随 Willie 侧空间离散度增大而减少、随平均 user-to-Willie 距离增大而增多；给出部署建议（用户尽量靠近 Willie 且保持高离散度）。

### 4.6 方法不足

- 纯理论/仿真工作，无实测或数据集验证（§VI 全部为仿真）。
- 依赖大 M 渐近与 Gamma/正态近似（App. A、B），有限 N 只以数值方式补充（Fig. 3）。
- 不完备信道估计使实际干扰增大（激活错误），只降速率（Fig. 5(d)(e)）；多个 Willie、移动场景与 ISAC 留给未来工作（§VII）。

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

与接收端中心式激活（[29]–[32]，只看 user-to-Bob 信道）相比，本文激活度量 r_m 同时含 λ_{m,w}，即把 Willie 侧几何写进选择规则；与均匀/平均几何分析相比，本文在 DEP 中保留逐用户 inclusion probability。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 空间异构感知的 on–off 激活 | 激活度量 r_m=\|h_{m,b}\|²/λ_{m,w}，兼顾 Bob 干扰与 Willie 侧有效性 | 高 | 是（任何"选辅助节点"问题） |
| 含选择偏差的 DEP 统计刻画 | 用 inclusion probability 处理有序统计导致的选择偏差 | 中 | 是（抽样/选择偏差建模） |
| 一维分段搜索算法 | 原 M+1 维问题 → O(M log M)，避免分辨率误差 | 中 | 是（分段结构优化范式） |

### 5.3 适用场景

大规模 IoT 类无线网络（M≫1、节点慢移动、相干时间足够长）中，隐藏单个用户向基站的传输不被第三方能量检测器发现；不涉及网络层流量分析。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 接收端中心式激活 [29]–[32] | 实现简单 | 忽略 Willie 侧几何，可能选到无效用户 | 激活度量加入 λ_{m,w} |
| 均匀/平均几何分析 [30]、[31] | 闭式简洁 | 抹平个体差异，高估 K_min | 保留个体 λ_{m,w} 与选择偏差 |
| 网格搜索引擎 | 通用 | O(N_pM) 且依赖分辨率、可能错过解析边界 | 直接评估解析候选 P_K̄ |

## 6. 实验表现与优势

### 6.1 实验设计和设置

仿真区域 1000 m × 1000 m；Willie 位于 (500,500)、Bob 位于 (100,100)、Alice 位于 (832.3,832.3)（d_{a,w}≈470 m、d_{a,b}≈1035.7 m，构成对 Alice 不利的链路）；α=3.5、β₀=10^{−3.45}、P_max=200 mW (23 dBm)、σ_b²=σ_w²=−102 dBm；用户随机分布以体现一般化拓扑。

### 6.2 数据集

无数据集（见 §0）。

### 6.3 Baseline

Bob-only baseline：只按 user-to-Bob 瞬时信道增益选协作用户（[30]–[32] 的做法）；另有均匀有限总体近似（Cor. 1）与网格搜索（N_p=10⁴）作对比。

### 6.4 评价指标

DEP ζ(γ) 与其最小值 ζ_min；最少协作用户数 K_min；优化后的隐蔽速率 R*；相对网格搜索的速率增益 (R*−R_Grid*)/R_Grid*。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---|---|---|---|
| 优化对比（仿真，N_p=10⁴ 网格） | Rate gain | M=500/1000/2000 分别 5.70%/5.94%/6.22% | 网格搜索 | — | P_a*/P_max 0.336/0.407/0.486 vs 网格 0.319/0.386/0.458（Table I） |
| 协作用户数（vs Bob-only 基线） | K* | 更少 | Bob-only 基线 | — | 约束越严差距越明显（Fig. 5(a)(b)） |
| 隐蔽速率 | R* | 更高 | Bob-only 基线 | — | Fig. 5(c) |
| 空间分布影响 | K_min | σ_d↑ ⇒ K_min↓；μ_d↑ ⇒ K_min↑ | — | — | M=500、P_a=140 mW、1−ε=0.97（Fig. 4(b)(c)） |
| 有限样本检测 | ζ_{N,min} | N=10/30/100 逐渐逼近大 N 基准 | — | — | Fig. 3(a)(b) |

### 6.6 优势最明显的场景

隐蔽约束很强（1−ε 接近 1）时，本文设计相对 Bob-only 基线的 K* 与速率优势最大（§V-B 末）。

### 6.7 局限性

见 §4.6；另 Corollary 2（同构假设）明显高估 K_min，说明平均几何类分析在异构部署下不可靠（Fig. 4(a)）。

## 7. 学习与应用

### 7.1 是否开源？

未提及代码仓库，`code: unknown`。

### 7.2 复现关键步骤

1. 生成 1000×1000 m 随机拓扑与 Rayleigh 信道（3GPP TR 25.996 路损）。
2. 计算激活度量 r_m 并升序排序，按 Theorem 1 求 K_min、按 Theorem 2 设 τ。
3. 运行 Algorithm 1 遍历 K̄=0..M 的解析候选功率，取速率最大者。
4. 对 Willie 阈值 γ 做数值最小化，与 Lemma 2/3 的闭式结果对照验证。

### 7.3 关键超参数、预处理和训练细节

α=3.5、P_max=200 mW、σ²=−102 dBm、M=300–2000、K=50–150、ρ_e∈[0,1] 信道估计误差、ε 由 1−ε=0.97 等设定。

### 7.4 能否迁移到其他任务？

与流量分析无直接关系（推断）。可借鉴的是方法论：**把"被选择对象的对手侧统计差异"写进选择准则**，以及用 inclusion probability 修正选择偏差——在流量分析中对应"选样本/选特征时对手侧(检测器)信息的利用"，但论文本身未涉及该领域。

### 7.5 对我的研究有什么启发？

弱启发：论文"仅按己方代价选节点会次优"的论证与"检测器视角信息应参与攻击/防御设计"的一般原则同构（推断），可作为跨领域类比论据，但不能直接支撑流量分析结论。

## 8. 总结

### 8.1 核心思想

> 把每个协作用户的 Willie 侧个体几何写进激活规则与检测分析，隐蔽性由"Alice 能量偏移 vs 聚合干扰不确定性"的平衡决定。

### 8.2 速记版 Pipeline

1. 计算激活度量 r_m=\|h_{m,b}\|²/λ_{m,w}，升序排序。
2. on–off 激活：r_m ≤ τ 的用户满功率发干扰。
3. 用 Lemma 1–3 的闭式 DEP 与 Theorem 1 反解 K_min、Theorem 2 定 τ。
4. 对每个候选 K̄ 取解析边界功率，一维分段搜索得 P_a*。
5. 输出 (P_a*, K*, τ*) 并由 Bob 广播控制参数。

## 9. Obsidian 知识链接

### 9.1 相关概念

- KB 概念白名单（website-fingerprinting、encrypted-traffic-analysis、tunnel-detection 等）均不覆盖物理层无线隐蔽通信，故本节不建立链接，避免发明页面名。

### 9.2 相关方法

- 方法白名单（transformer、graph-neural-network、contrastive-learning 等）均不适用：本文是统计建模 + KKT/分段优化，无机器学习组件。

### 9.3 相关任务

- 无对应任务页（KB 任务白名单全部为流量侧任务）。

### 9.4 可更新的综述页面

- 无。本文不属于 KB 任何综述（加密流量分析 / WF / 恶意检测）的主题范围。

### 9.5 可加入的对比表

- 不适用：论文未提出可用于 `method-comparison-table` 的流量分析新方法，也未使用或发布数据集；无开源代码可入 `open-source-registry`。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 最优协作功率谱为 on–off 结构（选中者满功率、其余静默） | KKT 求解，边界情形并入激活集 | Prop.1、App. A 式 (50) |
| 最小协作用户数由 Σ_K ≥ c_εΔ² 决定，c_ε=(1/ε²−8+16ε²)/(2π) | 由 ζ_min 闭式反解 | Thm.1 式 (24) |
| 分段搜索复杂度 O(M log M)，优于网格 O(N_pM)，速率增益 5.70%–6.22% | 复杂度推导 + N_p=10⁴ 对比实验（M=500/1000/2000） | §V-B、Table I |
| Willie 侧空间离散度越大 K_min 越少、平均距离越大 K_min 越多 | 缩放律 K_min^uni≈⌈c_εP_a²λ_{a,w}²/(P_max²(E+V))⌉ 与仿真 | 式 (32)、Fig. 4(b)(c) |
| 信道估计误差不改变 Willie 侧 DEP，主要通过激活错误降低速率 | 误差模型下 ĥ 统计分布不变；Fig. 5(d) 重合、5(e) 下降 | §V-B、Fig. 5(d)(e) |

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-arXiv-Covert_Communication_with_Spatially_Heterogeneous_User_Cooperation_Against_a_Geometry-Aware_Warden.pdf
- MinerU Markdown：02-parsed-markdown/2026-arXiv-Covert_Communication_with_Spatially_Heterogeneous_User_Cooperation_Against_a_Geometry-Aware_Warden.md

## 12. 后续问题

- 暂未整理

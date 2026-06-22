---
type: paper
title_original: "Minipatch: Undermining DNN-Based Website Fingerprinting With Adversarial Patches"
title_cn: "Minipatch：利用对抗补丁破坏基于DNN的网站指纹攻击"
authors: ["Ding Li", "Yuefei Zhu", "Minghao Chen", "Jue Wang"]
year: 2022
venue: "IEEE TIFS 2022"
doi: "10.1109/TIFS.2022.3186743"
url: "https://ieeexplore.ieee.org/document/9815943"
pdf: "00-inbox/PDFs/2022-TIFS-Minipatch__Undermining_DNN-Based_Website_Fingerprinting_With_Adversarial_Patches.pdf"
mineru_md: "02-parsed-markdown/2022-TIFS-Minipatch__Undermining_DNN-Based_Website_Fingerprinting_With_Adversarial_Patches.md"
status: processed
reading_level: L2
research_area: ["website fingerprinting", "adversarial machine learning", "traffic analysis", "privacy"]
task: ["website fingerprinting defense", "adversarial perturbation", "real-time traffic perturbation"]
method: ["adversarial patches", "dual annealing", "black-box optimization", "adaptive bound tuning"]
dataset: ["Sirinam (95 sites)", "Rimmer100", "Rimmer200", "Rimmer500", "Rimmer900", "Rimmer+T (concept drift)"]
code: "https://github.com/website-fingerprinting/minipatch"
relevance: medium
created: "2026-06-21"
updated: "2026-06-21"
---

# Minipatch: Undermining DNN-Based Website Fingerprinting With Adversarial Patches

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Minipatch: Undermining DNN-Based Website Fingerprinting With Adversarial Patches |
| 中文标题 | Minipatch：利用对抗补丁破坏基于DNN的网站指纹攻击 |
| 作者 | Ding Li, Yuefei Zhu (通讯作者), Minghao Chen, Jue Wang |
| 机构 | 数学工程与先进计算国家重点实验室，郑州，中国 |
| 会议/期刊 | IEEE Transactions on Information Forensics and Security (TIFS), 2022 |
| 发表时间 | 2022 年 6 月 27 日 |
| DOI | 10.1109/TIFS.2022.3186743 |
| 关键词 | Traffic analysis, deep neural networks, adversarial machine learning, adversarial example |
| 研究方向 | [[website-fingerprinting]] 防御、[[encrypted-traffic-analysis]]、对抗机器学习 |
| 任务类型 | 利用对抗补丁防御 DNN-based [[website-fingerprinting]] 攻击 |
| 方法关键词 | adversarial patches, dual annealing (DA), black-box optimization, adaptive bound tuning |
| 数据集 | Sirinam (95 sites, 800/100/100 split); Rimmer100/200/500/900; Rimmer+T (concept drift, 3/10/28/42/56 days) |
| 是否开源 | 是（https://github.com/website-fingerprinting/minipatch） |
| Confidence | medium |
| 晋升状态 | 未晋升 |

---

## 1. 一句话总结

> 提出 Minipatch，一种基于对抗补丁的 [[website-fingerprinting-defense]] 方案，通过向网络流量中注入极少的 dummy packets（<5% 带宽开销），在黑盒设定下实现超过 97% 的 DNN 分类器逃逸率，显著优于已有对抗防御方案。

---

## 2. 核心贡献

### 2.1 贡献列表

1. **自适应补丁注入技术**：提出将对抗补丁注入同方向 burst 尾部的策略，使扰动能适应同一网站不同 trace 的变化，支持实时流量注入，不引入新 burst、不增加额外 RTT
2. **黑盒对抗补丁生成算法**：定义最小化正确分类概率的优化问题，采用 Dual Annealing (DA) 元启发式算法求解，仅需目标模型的概率标签输出，无需梯度或模型结构信息
3. **自适应带宽开销调优策略**：将二叉搜索泛化为寻找最优补丁长度约束的问题，在成功率和带宽开销之间找到最优平衡
4. **全面的实验评估**：在多种挑战性设置下评估 Minipatch，包括单向客户端扰动、概念漂移鲁棒性、跨模型迁移性，以及频率分析和对抗训练等反制措施的分析

### 2.2 与领域已有工作的关键区别

| 已有工作 | 差异点 | 位置 |
|---|---|---|
| Mockingbird [19] | Mockingbird 是 burst-oriented（需完整 trace），Minipatch 是 packet-oriented（支持实时注入）；Mockingbird 带宽开销 >50%，Minipatch <5% | §II-C, §IV-B.7 |
| Blind [21] | Blind 需要白盒访问（计算 loss gradient），Minipatch 仅需黑盒反馈；Blind 在 11% 开销下成功率 91%，Minipatch 在 5% 开销下 >97% | §II-C, §IV-B.7 |
| Dolos [23] | Dolos 在 DNN 特征空间操作（白盒），且在固定位置注入（不可自适应）；Dolos 带宽开销 30%，Minipatch <5% | §II-C, §IV-B.7 |
| AWA [22] | AWA 是 GAN-based，需要完整 burst sequence（非实时）；AWA 带宽开销 22.3%，Minipatch <5% | §II-C, §IV-B.7 |

---

## 3. 研究连接

### 3.1 相关概念

- [[website-fingerprinting]]
- [[website-fingerprinting-defense]]
- [[encrypted-traffic-analysis]]

### 3.2 相关方法

- [[convolutional-network]]（作为被攻击的目标模型）
- 对抗补丁（adversarial patches）— 将计算机视觉中的对抗补丁概念迁移到网络流量领域
- Dual Annealing — 基于广义模拟退火 (GSA) 的全局优化算法

### 3.3 相关任务

- [[website-fingerprinting-defense]]

### 3.4 基于哪些已有论文

- [[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]] (DF 攻击)
- [[survey-website-fingerprinting]] (领域综述)

### 3.5 与已有 Claims 的关系

| 已有 Claim | 本论文的关系 | 位置 |
|---|---|---|
| DNN-based WF 攻击可达 98%+ 准确率 | 挑战 — 证明 DNN-based WF 可被极少 dummy packets 破坏 | §I, §IV |
| 对抗扰动可用于 WF 防御 | 扩展 — 首次将 adversarial patches（非全局扰动）应用于 WF 防御 | §I, §III |
| 现有 WF 防御带宽开销过高（>20%） | 挑战 — 证明 <5% 开销即可有效防御 | §IV-B.7 |

---

## 4. 关键发现与证据

### 4.1 主要实验结果

| 任务/数据集 | 指标 | Minipatch | 最优 Baseline | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| Sirinam / DF | 成功率 (SR) | 99.4% | 98.4% (Mockingbird) | +1.0% | Minipatch 带宽开销仅 5.7%，Mockingbird 为 54.7% |
| Sirinam / AWF | 成功率 (SR) | 99.8% | 99.7% (Mockingbird) | +0.1% | 带宽开销 3.2% vs 54.7% |
| Sirinam / Var-CNN | 成功率 (SR) | 99.3% | 99.1% (Mockingbird) | +0.2% | 带宽开销 4.8% vs 54.7% |
| Rimmer100 / DF | 成功率 (SR) | 99.1% | 97.8% (Mockingbird) | +1.3% | 带宽开销 4.9% vs 56.2% |
| Sirinam / DF (outgoing) | 成功率 (SR) | 97.8% | — | — | 仅客户端注入，带宽开销 5.3% |
| Sirinam / DF (concept drift, 6w) | 成功率 (SR) | 99.0% | — | — | 补丁在 6 周后仍有效 |

### 4.2 关键发现

1. **Var-CNN 比 DF 更脆弱**：尽管 Var-CNN 结构更复杂（20 层 Conv vs 8 层）、准确率更高（99.7% vs 98.1%），但其对抗补丁成功率更高。结论：更复杂的 DNN 模型不一定具有更好的对抗鲁棒性
2. **出站方向特征权重更大**：outgoing mode（仅注入出站包）接近 duplex mode 性能（97.8% vs 99.1%），而 incoming mode 仅 82.3% 且带宽开销 >13%。说明 DNN 对出站包特征赋予更大权重
3. **概念漂移反而增强防御效果**：网站内容变化本质上也是一种扰动，与对抗补丁叠加后将 trace 推离原始位置，因此 Minipatch 在 6 周后仍保持 99% 成功率
4. **DF 生成的补丁迁移性最好**：DF 生成的补丁对 AWF 和 Var-CNN 的迁移成功率分别为 89.7% 和 91.1%，适合作为白盒模型生成通用补丁
5. **少于 10 次查询即可有效防御 AWF**：DA 算法的计算效率优于群体进化算法，仅需几百次查询即可为几乎所有网站提供高效保护
6. **对抗训练后可完全恢复防御效果**：攻击者进行对抗训练后 Minipatch 成功率降至 25.9%，但使用重训练模型重新生成补丁后恢复至 98.9%

---

## 5. 质量与信心评估

### 5.1 当前状态

| 维度 | 状态 | 备注 |
|---|---|---|
| 实验完整性 | 完整 | 覆盖 3 个 DNN 模型、6 个数据集、多种挑战性设置 |
| 写作完整性 | 完整 | 结构清晰，算法伪代码完整 |
| 方法创新性 | 中 | 将 CV 领域的 adversarial patches 迁移到 WF 领域，创新在于自适应注入和黑盒优化 |
| 实验说服力 | 强 | 对比实验全面，带宽开销定义更严格（使用 min(mx,n)）仍优于基线 |
| 与已有工作的区分度 | 明确 | 与 Mockingbird/Blind/Dolos/AWA 有明确的对比和区分 |

### 5.2 需要改进的地方

1. **需要知道用户访问的网站**：防御者需预先知道用户访问哪个网站才能生成对应补丁，这在实际部署中是一个限制
2. **仅处理方向序列特征**：无法防御使用包时间信息的 WF 攻击（如 Tik-Tok）
3. **仅考虑非定向扰动**：未探索定向扰动（将所有网站伪装为特定网站）的可行性
4. **频率分析在 >32 样本时可检测**：当攻击者收集足够多同一网站的保护 trace 时，可通过重叠率分析检测 Minipatch 的存在

### 5.3 是否可以考虑提交/晋升？

> [x] 方法论完整
> [x] 实验覆盖足够
> [x] 写作达到可读标准
> [x] 与已有工作区分度明确
> [x] 局限性已诚实讨论

---

## 6. 开放问题与后续计划

### 6.1 本文遗留的问题

- 如何减少对已知网站的依赖，提高对抗补丁的通用性？
- 如何将防御扩展到使用包时间特征的 WF 攻击？
- 如何实现定向扰动（将访问伪装为特定网站）？
- 非 DNN 流量分析技术（基于统计特征）如何与本方法结合？

### 6.2 下一步研究方向

- 设计包含方向和时间两个维度的联合优化补丁
- 探索通用对抗补丁（不依赖特定网站）的生成方法
- 研究对抗训练与补丁生成的对抗博弈均衡

### 6.3 与我的研究主线的关系

> 本文属于 [[website-fingerprinting-defense]] 方向，提供了基于对抗机器学习的轻量级防御范式。其黑盒优化方法和低带宽开销的特性对实际部署有参考价值，可作为 WF 攻防研究中的重要 baseline。

---

## 7. 方法设计详解

### 7.1 方法整体流程

Minipatch 由三个核心组件组成：

1. **补丁注入函数 (Patch Injection)**：将对抗补丁注入到网络流量 trace 的同方向 burst 尾部
2. **补丁生成 (Patch Generation)**：使用 Dual Annealing 算法在黑盒设定下求解优化问题
3. **开销调优 (Overhead Tuning)**：通过扭曲二叉搜索找到最优的补丁数量和长度约束

### 7.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| 1. 流量采集 | 用户 Tor 连接 | 采集网站 trace，编码为方向序列 (+1/-1) | 方向序列 x | 输入表示 |
| 2. 预训练目标模型 | 方向序列数据集 | 训练 AWF/DF/Var-CNN | DNN 分类器 f | 黑盒目标 |
| 3. 正确分类样本筛选 | 测试集 + 分类器 f | 选出 f 正确分类的 trace 集合 X_w^f | X_w^f | 补丁生成的训练集 |
| 4. 自适应开销调优 | X_w^f, 初始约束 (M_α=8, M_β=64) | 扭曲二叉搜索，逐步缩小约束 | 最优约束 <M_α, M_β> | 最小化带宽开销 |
| 5. 补丁生成 (DA) | X_w^f, 分类器 f, 约束 | Dual Annealing 优化，最小化正确分类概率 | 对抗补丁向量 δ_w | 核心扰动 |
| 6. 实时注入 | 实时流量 trace x, 补丁 δ_w | 注入到同方向 burst 尾部 | 扰动后 trace x' | 实时防御 |

### 7.3 核心算法模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Patch Injection (Algorithm 1) | 将补丁注入 trace 的同方向 burst 尾部 | 网站 trace x, 扰动向量 δ | 扰动后 trace x' | 被 Patch Generation 调用 |
| Patch Generation (Algorithm 2) | DA 优化求解对抗补丁 | X_w^f, 分类器 f, 约束参数 | 最优扰动 δ_w | 调用 Injection 计算能量 |
| Adaptive Tuning (Algorithm 3) | 二叉搜索找最优约束 | X_w^f, f, 初始约束 | 最优 δ_w | 调用 Patch Generation |

### 7.4 公式、算法和机制解释

**优化问题定义 (Eq. 7)**

网站级别的对抗补丁优化问题：
```
δ_w = argmin_δ  (1/|X_w^f|) Σ_{x ∈ X_w^f} f_w(Φ[x, δ])
```
其中 f_w(x) 是分类器对网站 w 的置信概率，Φ[x, δ] 是补丁注入函数。约束条件：
- 1 ≤ α ≤ M_α（补丁数量上界）
- 0 ≤ p_i ≤ N（注入位置范围）
- -M_β ≤ β_i ≤ M_β（补丁长度上界）

**成功判据 (Eq. 8)**
```
Σ 1[f(Φ[x, δ]) ≠ f(x)] ≥ |X_w^f| × τ
```
τ = 1 表示要求所有正确分类的 trace 都被逃逸。

**Dual Annealing 能量函数**

候选解 δ 的能量 E 定义为 Eq. 7 的优化目标（所有 trace 的平均正确分类概率）。温度衰减：
```
T(t) = T_0 × (2^(q_v-1) - 1) / ((t+1)^(q_v-1) - 1)
```
接受准则使用广义 Metropolis 准则 (Eq. 10)，参数 T_0=5230, q_v=2.62, q_a=-10^3。

**自适应开销调优 (Eq. 11)**

最优扰动定义为最高扰动效率：
```
δ_w = argmax_δ  [Σ 1[f(Φ[x,δ]) ≠ f(x)]] / [Σ |β_i|]
```
即在满足成功阈值的解中，选择成功率/总注入包数最高的解。

**带宽开销定义 (Eq. 13)**
```
BWO = [Σ_x Σ_{<p,β> ∈ δ_x} |β|] / [Σ_x min(m_x, n)]
```
使用 min(m_x, n) 而非 m_x 或 n，定义更严格。

---

## 8. 实验详细分析

### 8.1 实验设计和设置

- **目标模型**：AWF（3 Conv, 147k 参数）、DF（8 Conv, 3,979k 参数）、Var-CNN（20 Conv/ResNet-18, 3,893k 参数）
- **输入表示**：方向序列 +1/-1，固定长度 5000（截断/零填充）
- **Minipatch 参数**：初始约束 M_α=8, M_β=64；DA 参数 T_0=5230, q_v=2.62, q_a=-10^3, τ=1, M_t=30
- **评估指标**：成功率 SR（归一化）= 分类器被逃逸的 trace 比例；带宽开销 BWO

### 8.2 数据集详情

| 数据集 | 网站数 | 训练/验证/测试 | 说明 |
|---|---|---|---|
| Sirinam | 95 | 800 / 100 / 100 | Sirinam et al. 公开数据集 |
| Rimmer100 | 100 | 2250 / 125 / 125 | Rimmer et al. 数据集 |
| Rimmer200 | 200 | 2250 / 125 / 125 | 同上，更多网站 |
| Rimmer500 | 500 | 2250 / 125 / 125 | 同上 |
| Rimmer900 | 900 | 2250 / 125 / 125 | 同上 |
| Rimmer+T | 200 | — / — / 100×5 | 概念漂移数据集（3/10/28/42/56 天后重新采集） |

### 8.3 Baseline 选择理由

| Baseline | 类型 | 选择理由 |
|---|---|---|
| Mockingbird [19] | 模仿型 (mimicking) | 首个将对抗样本用于 WF 防御的工作，高成功率但高开销 |
| Blind [21] | 盲扰动 (blind perturbation) | 首个实现实时流量扰动的对抗防御，但需白盒访问 |
| AWA [22] | GAN-based | 网站级通用扰动，开销合理 |
| Dolos [23] | 补丁型 (patch-based) | 最接近本文方法，使用对抗补丁但需白盒且固定位置注入 |

### 8.4 消融实验

本文未设置传统消融实验，但通过以下变量分析实现了类似效果：

| 变量 | 分析内容 | 结论 |
|---|---|---|
| 补丁数量和长度约束 (M_α × M_β) | 4 组约束 (8/32/128/512 packets) | 更大约束 → 更高成功率，但实际注入包数远小于约束上界 |
| 监控网站数量 | Rimmer100/200/500/900 | 更多网站 → 更容易生成扰动（特征空间更密集） |
| 补丁方向 | duplex / outgoing / incoming | outgoing ≈ duplex >> incoming |
| 查询数量 | 10/100/1000/10000 次查询 | 1000 次后收敛，10 次即可有效防御 AWF |
| 概念漂移时间 | 3/10/28/42/56 天 | 成功率始终 >96%，6 周后仍 99% |
| 跨模型迁移 | 所有模型对组合 | DF 生成的补丁迁移性最好（89.7%-91.1%） |

### 8.5 Case Study / 可视化分析

- **Figure 1**：展示 Minipatch 扰动成功逃逸三种 DNN 攻击的示例，显示原始 trace 和注入补丁后 trace 的方向序列对比
- **Figure 5**：成功率 vs 监控网站数量，Rimmer900 在 32 packets 约束下达到 68% 成功率（Rimmer100 仅 31.5%）
- **Figure 8**：概念漂移实验，DNN 准确率随时间下降，但 Minipatch 成功率保持高位
- **Figure 9**：热力图展示跨模型迁移性，DF→(AWF, Var-CNN) 迁移率最高
- **Figure 10**：重叠率分析，<20 样本时 patch overlap rate 与 trace overlap rate 接近，难以检测

### 8.6 局限性与失败案例

1. **需要预知用户访问的网站**：无法在不知道目标网站的情况下生成补丁
2. **无法防御时间特征攻击**：对使用包间时间间隔的 WF 攻击无效
3. **频率分析可检测**：收集 >32 个同一网站的保护 trace 后可通过重叠率检测
4. **对抗训练降低效果**：攻击者使用对抗训练后，原始补丁成功率降至 25.9%（但可重新生成恢复）

---

## 9. 反制措施与部署分析

### 9.1 频率分析

攻击者观察同一用户的多次访问，通过 patch overlap rate (OR_P) 检测补丁存在。实验表明：
- <20 个样本：OR_P 与 trace overlap rate (OR_T ≈ 86%) 接近，难以区分
- >32 个样本：OR_P 显著高于 OR_T，可被检测
- 实际中用户对同一网站的访问次数有限，且误分类进一步降低检测可行性

### 9.2 对抗训练

攻击者收集保护后的 trace 进行对抗训练：
- 对抗训练后 DF 模型准确率 98.0%，Minipatch 成功率降至 25.9%
- 但使用重训练模型重新生成补丁后，成功率恢复至 98.9%
- 启示：需要设计更新机制指导部署中的补丁生成

### 9.3 双重更新机制

- **部分更新**：定期为每个网站生成多个新补丁向量，随机选择一个应用于实时流量（每网站约 6 秒）
- **完整更新**：更长周期内重新执行自适应开销调优，假设目标分类器已被对抗训练

### 9.4 部署可行性

- **端到端协作**：客户端和 Tor 入口节点协作（或仅客户端 outgoing mode）
- **时间开销**：TO < BWO < 5%，用户几乎无感知
- **预计算**：补丁可预先计算，运行时无额外计算开销
- **注入方式**：修改浏览器通信为半双工模式，或放宽位置约束尽早注入

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| <5% 带宽开销可实现 >97% WF 防御成功率 | Table III, Table IV | §IV-B.1, §IV-B.7 |
| Var-CNN 比 DF 更脆弱（尽管更复杂） | Table III: Var-CNN SR 99.3% vs DF SR 99.4% @Sirinam, 但 Var-CNN BWO 更低 | §IV-B.1 |
| 出站方向特征权重更大 | outgoing SR 97.8% vs incoming SR 82.3% | §IV-B.3 |
| 概念漂移增强防御效果 | Figure 8: 6 周后 SR 仍 99% | §IV-B.5 |
| DF 生成的补丁迁移性最好 | Figure 9: DF→AWF 89.7%, DF→Var-CNN 91.1% | §IV-B.6 |
| 对抗训练后重新生成可恢复效果 | SR 25.9% → 98.9% | §V-A.2 |
| <10 次查询即可有效防御 AWF | Figure 7: 10 queries → 94.2% SR | §IV-B.4 |
| 频率分析在 >32 样本时可检测 | Figure 10 | §V-A.1 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2022-TIFS-Minipatch__Undermining_DNN-Based_Website_Fingerprinting_With_Adversarial_Patches.pdf
- MinerU Markdown：02-parsed-markdown/2022-TIFS-Minipatch__Undermining_DNN-Based_Website_Fingerprinting_With_Adversarial_Patches.md
- 代码仓库：https://github.com/website-fingerprinting/minipatch
- 补充材料：无

---

## 12. 领域关联与定位

### 12.1 在 WF 攻防演进中的位置

```
传统 WF 攻击 (k-FP, CUMUL)
  → DNN-based WF 攻击 (AWF [2018], DF [2018], Var-CNN [2019])
    → 对抗防御探索
      → Mockingbird [2021]: mimicking, 白盒, >50% BWO
      → WF-GAN [2020]: GAN-based, burst-oriented, 90% SR
      → Blind [2021]: blind perturbation, 白盒, 11-25% BWO
      → AWA [2021]: GAN-based, 网站级, 22% BWO
      → Dolos [2021]: patch-based, 白盒, 30% BWO
      → **Minipatch [2022]**: patch-based, 黑盒, <5% BWO ← 本文
```

### 12.2 技术贡献的长期价值

- **黑盒优化范式**：证明了在仅访问概率标签的情况下，通过元启发式算法可以有效生成对抗扰动，降低了实际部署的门槛
- **低开销防御标杆**：<5% 带宽开销设定了 WF 防御的效率标杆，后续工作需要在此基础上进一步优化或提出新范式
- **补丁自适应性**：同方向 burst 尾部注入策略使补丁能适应同一网站的不同 trace，解决了 trace-oriented 方法的实时性问题

### 12.3 与后续工作的关联

- 本文证明了 outgoing-only 扰动接近 duplex 性能，为纯客户端防御提供了理论依据
- 概念漂移增强防御的发现为自适应防御系统设计提供了新思路
- 对抗训练与补丁重新生成的对抗博弈关系预示了 WF 攻防将持续演进

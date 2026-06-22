---
type: paper
title_original: "Reality Check for Tor Website Fingerprinting in the Open World"
title_cn: "Tor 网站指纹在开放世界中的现实检验"
authors:
  - Mohammadhamed Shadbeh
  - Khashayar Khajavi
  - Tao Wang
year: 2026
venue: "arXiv 2026"
doi: ""
url: "https://arxiv.org/abs/2605.xxxxx"
pdf: ""
mineru_md: "02-parsed-markdown/2026-arXiv-Reality_Check_for_Tor_Website_Fingerprinting_in_the_Open_World.md"
status: processed
reading_level: L2
dataset:
  - "Pre-Conflux: 103 monitored webpages, 103,369 monitored traces + 79,833 non-monitored traces"
  - "Post-Conflux: 112 monitored webpages, 530,257 monitored traces + 31,724 non-monitored traces"
  - "Total: 800,000+ traces"
code: "https://osf.io/9m8ea/"
relevance: medium
research_area: ["网站指纹", "Tor流量分析", "隐私与匿名"]
task: ["开放世界网站指纹", "Conflux流量分析", "Guard节点攻击"]
method: ["DF (CNN)", "RF (TAM)", "k-FP", "Tik-Tok", "Holmes"]
created: "2026-06-21"
updated: "2026-06-21"
---

# Reality Check for Tor Website Fingerprinting in the Open World

## 0. 论文基础信息（表格）

| 项目 | 内容 |
|------|------|
| 论文标题 | Reality Check for Tor Website Fingerprinting in the Open World |
| 作者 | Mohammadhamed Shadbeh, Khashayar Khajavi, Tao Wang |
| 机构 | Simon Fraser University |
| 会议/期刊 | arXiv 2026 (预印本) |
| 发表时间 | 2026 |
| 关键词 | Tor; website fingerprinting; open-world; Conflux; guard relay; traffic analysis |
| 数据集规模 | 800,000+ traces (103 + 112 monitored webpages) |
| 开源代码/数据 | https://osf.io/9m8ea/ |

## 1. 一句话总结

从 Tor Guard 节点视角出发，使用隐私保护方法收集真实非监控流量，首次证明 WF 攻击在真实 Tor 开放世界中仍然高度有效（DF 达到 π₁₀=0.956, recall=0.922），并首次系统评估 Conflux 流量分割机制下的 WF 可行性。

## 2. 摘要翻译（原文+中文）

**原文：**
Website fingerprinting (WF) attacks on Tor can infer user destinations from encrypted traffic metadata. However, their real-world effectiveness remains debated due to laboratory settings that fail to capture network fluctuations, evaluate noise, and create a representative open world. In this work, we re-examine WF from a guard-relay vantage point using a novel, privacy-preserving methodology that builds an open-world background from real, unlabeled Tor traffic paired with synthetic monitored traces. Using this methodology, we collect a large-scale dataset of over 800,000 traces. We then benchmark state-of-the-art WF attacks under a cross-network setting and show that WF remains highly effective against real Tor open-world traffic: the best-performing attack achieves 0.956 precision and 0.922 recall at a 9% base rate. We further present results that demonstrate robustness to small training sets, network jitter, and concept drift. Moreover, we show that timing-independent classifiers are significantly more robust to network variability than others. Finally, we provide the first systematic study of Tor's Conflux traffic-splitting, where we show that a guard node with a latency advantage can maintain high attack effectiveness even when traffic is split.

**中文翻译：**
针对 Tor 的 website fingerprinting (WF) 攻击可以从加密流量元数据中推断用户目的地。然而，由于实验室环境无法捕捉网络波动、评估噪声并创建具有代表性的开放世界，其现实有效性一直存在争议。在本研究中，我们从 guard relay 的视角重新审视 WF，采用一种新颖的隐私保护方法论，用真实、未标记的 Tor 流量配合合成监控流量构建开放世界背景。利用该方法论，我们收集了超过 800,000 条 trace 的大规模数据集。然后，我们在跨网络设置下基准测试最先进的 WF 攻击，结果表明 WF 对真实 Tor 开放世界流量仍然高度有效：最佳攻击在 9% 基础率下达到 0.956 precision 和 0.922 recall。我们进一步展示了对小训练集、网络抖动和概念漂移的鲁棒性。此外，我们表明不依赖时序的分类器对网络变异性的鲁棒性显著优于其他分类器。最后，我们首次系统研究了 Tor 的 Conflux 流量分割机制，证明具有延迟优势的 guard 节点即使在流量被分割的情况下仍能保持高攻击有效性。

## 3. 方法动机（为什么提出、现有痛点、核心直觉）

### 现有痛点

1. **实验室与现实差距**：现有 WF 评估依赖实验室条件（稳定客户端设置、一致网络条件、清晰页面加载边界、无背景活动），无法反映真实 Tor 使用场景。
2. **Cherubin 设置的局限**：Cherubin et al. (USENIX Security 2022) 的研究虽使用真实非监控流量，但在 exit 节点收集监控流量导致只能获得 domain 级标签（而非 page 级），且 exit-to-guard 训练-测试不匹配导致性能下降。
3. **开放世界评估不充分**：大多数研究使用合成非监控流量，无法捕捉真实 Tor 开放世界的复杂性（真实流行度分布、浏览模式、动态内容）。
4. **Conflux 影响未知**：Tor 的 Conflux 流量分割机制对 WF 攻击的影响从未被系统评估。

### 核心直觉

- Guard 节点是特别危险的攻击位置：它可以看到客户端 IP 地址、观察长期流量模式、利用流隔离机制去复用并发页面加载。
- 使用合成监控流量（page 级标签）+ 真实非监控流量的组合方法论，既保留了标签精度，又捕捉了真实开放世界的复杂性。
- 训练和测试都在 guard 节点视角收集，消除了 Cherubin 设置中的 vantage point 不匹配问题。

### 为什么提出本方法

- Cherubin 设置强制攻击者在 exit 节点训练是不必要的限制：实际攻击者可以选择最优训练策略。
- 使用 exit 收集的监控流量训练、guard 收集的测试流量评估，引入了 relay 效应导致的特征失真。
- 需要一种更准确反映真实攻击者能力的方法论，同时保持隐私保护。

## 4. 方法设计（整体流程、详细 Pipeline 表格、模型模块表格、公式解释、优势、不足）

### 整体流程

1. **数据采集**：在 Canada/Australia/UK 部署受控客户端，在 Canada 部署 guard relay
2. **监控流量采集**：受控客户端通过自动化 Tor Browser 访问目标网页，round-robin 调度
3. **非监控流量采集**：guard relay 记录非受控客户端的真实流量（仅元数据）
4. **数据清洗**：多步骤清洗管道提取高质量 trace
5. **模型训练与评估**：跨网络条件下基准测试 5 种 WF 攻击

### 详细 Pipeline 表格

| 阶段 | 操作 | 详细说明 |
|------|------|----------|
| Guard 插桩 | ≈300 LoC 补丁 | 记录 per-cell 元数据：circuit/channel ID、高精度时间戳、方向性 |
| 客户端插桩 | ≈200 LoC 补丁 | 记录 first-party domain、请求时间戳、目标 domain、circuit ID |
| 监控流量收集 | 自动化浏览器 | 使用 Tampermonkey（非 Selenium），每个客户端访问每个网页 ≥200 次 |
| 非监控流量收集 | Guard 被动记录 | 仅记录隐私保护的 per-cell 元数据，不记录 IP 或目的地 |
| Spam 过滤 | Channel 级规则 | 创建 >10,000 circuits 的 channel 标记为 spam |
| 握手验证 | Cell 序列检查 | Pre-Conflux: [+1,-1,+1]; Post-Conflux: [+1,-1,+1,-1,+1] |
| 小电路过滤 | Cell 数阈值 | 移除 <200 cells 的电路 |
| 头部修剪 | 握手移除 | Pre-Conflux: 移除前 2 个 cells; Post-Conflux: 移除前 5 个 cells |
| 尾部修剪 | 4 阶段处理 | Teardown 移除 + Gap-based pruning + Duration capping + Length truncation (5000 cells) |

### 被评估的 WF 攻击模型

| 模型 | 年份 | 分类器 | 特征类型 | 关键特点 |
|------|------|--------|----------|----------|
| k-FP | 2016 | Random Forest | 手工特征 (175维) | 叶节点特征 + k-NN |
| DF | 2018 | 1D CNN | Packet direction 序列 | 仅使用方向信息，不含时序 |
| Tik-Tok | 2019 | 1D CNN | Direction + Timing | 在 DF 基础上加入时序信息 |
| RF | 2023 | 2D CNN | Traffic Aggregation Matrix (TAM) | 时序聚合矩阵表示 |
| Holmes | 2024 | Dual-Branch CNN | Temporal + TAF | 对比学习，专为早期检测设计 |

### 关键公式

**r-precision (开放世界评估核心指标):**

$$\pi_r = \frac{TPR}{TPR + WPR + r \cdot FPR}$$

其中 $r$ 是非监控与监控流量的实际比率，$WPR$ 是 wrong positive rate（被预测为监控类但分配到错误监控类），$FPR$ 是 false positive rate。r-precision 明确考虑了基础率谬误。

**F₁ 得分:**

$$F_1 = 2 \cdot \frac{\pi_r \cdot TPR}{\pi_r + TPR}$$

综合 r-precision 和 recall 的调和平均。

### 数据集总结

| 数据集 | 类别数 | 监控流量 (Normal) | 监控流量 (Latency) | 监控流量 (Client) | 非监控流量 |
|--------|--------|-------------------|--------------------|--------------------|------------|
| Pre-Conflux | 103 | 103,369 | - | - | 79,833 |
| Post-Conflux | 112 | 158,233 | 96,420 | 335,528 | 31,724 |

### 优势

1. **隐私保护方法论**：不记录 IP 地址或目的地，非监控流量完全匿名化
2. **真实开放世界背景**：使用真实 Tor 用户流量作为非监控集，比合成数据更真实
3. **Page 级标签精度**：监控流量使用合成方法获得精确的网页级标签
4. **跨网络评估**：使用不同地理位置的客户端（CA/AU/UK）进行训练-测试，模拟真实网络异质性
5. **大规模数据集**：800,000+ traces，远超现有研究
6. **首次 Conflux 评估**：首次系统研究 Conflux 对 WF 的影响

### 不足

1. **合成监控流量**：虽然方法论合理，但合成流量可能无法完全代表真实用户的浏览行为（如动态页面、cookie、个性化）
2. **Guard 视角局限**：仅评估 guard 攻击者，未与其他 vantage point（如 ISP）直接对比
3. **Conflux 评估有限**：仅评估默认 LowRTT 调度策略，未探索其他调度算法
4. **监控网页选择偏差**：选择 Tranco 排名 10,000 以外的网站，可能不具代表性
5. **非监控流量标签噪声**：无法排除非监控流量中恰好访问监控网页的情况

## 5. 与其他方法对比（本质区别、创新点表格、适用场景、方法对比表）

### 本质区别

与 Cherubin et al. (USENIX Security 2022) 的核心区别在于训练策略：Cherubin 设置在 exit 节点收集监控流量用于训练（仅 domain 级标签），而本工作使用合成监控流量在 guard 节点训练（page 级标签）。本工作的非监控流量同样使用真实 Tor 流量，保持了开放世界的真实性。

### 实验设置对比表

| 设置 | Standard (实验室) | Cherubin | 本工作 (Ours) |
|------|-------------------|----------|---------------|
| **训练集 - 监控流量** | 合成 | 真实 (exit) | 合成 |
| **训练集 - 非监控流量** | 合成 | 真实 (exit) | 真实 (guard) |
| **训练集 - 视角** | Client | Exit | Guard |
| **训练集 - 标签** | Webpages | Domains | Webpages |
| **测试集 - 监控流量** | 合成 | 合成 | 合成 |
| **测试集 - 非监控流量** | 合成 | 真实 (guard) | 真实 (guard) |
| **测试集 - 视角** | Client | Guard | Guard |
| **测试集 - 标签** | Webpages | Domains* | Webpages |

### 创新点表格

| 创新点 | 说明 |
|--------|------|
| 隐私保护的 Guard 攻击方法论 | 不记录 IP/目的地，使用临时标识符和严格清洗 |
| 首次 Guard 视角 WF 评估 | 分析 Guard 作为攻击者的独特优势（控制数据移除、circuit 去复用） |
| 真实 Tor 开放世界数据集 | 800,000+ traces，包含真实非监控流量 |
| 首次 Conflux WF 系统评估 | 评估流量分割对 guard 攻击者的影响 |
| 跨网络评估框架 | CA/AU/UK 三地客户端，评估网络异质性影响 |
| 强大 Guard 模拟 | 通过 RTT 操纵模拟具有延迟优势的 guard 节点 |

### 适用场景

| 方法 | 最佳适用场景 | 局限场景 |
|------|-------------|----------|
| DF | 跨网络条件、真实开放世界 | 早期检测（需 90% 数据） |
| RF | 概念漂移、Conflux 非 FS traces | 跨网络条件（时序敏感） |
| Tik-Tok | 中等网络变异 | 大延迟差异 |
| k-FP | 概念漂移初期 | 跨网络、Conflux |
| Holmes | 理论设计用于早期检测 | 跨网络条件完全失效 |

## 6. 实验表现（实验设置、数据集、Baseline、指标、关键结果表格、优势场景、局限性）

### 实验设置

- **硬件**：Guard relay: OVH 服务器 (Intel Xeon E3-1245v2, 32GB RAM, 100Mbps); 客户端: Intel i7-6700 (CA), DigitalOcean 2vCPU (UK/AU)
- **网络延迟**：CA→Guard ≈68ms, AU→Guard ≈223ms, UK→Guard ≈79ms
- **评估模式**：Cross-network (Train: AU, Test: CA) 和 Pooled (Train & Test: Both)
- **指标**：π₁, π₁₀, Recall (TPR), F₁ (基于 π₁₀)
- **操作点选择**：最大化 F₁ 得分的决策阈值
- **FPR 基线**：0.5%（用于固定 FPR 比较）

### 关键结果表格

**Pre-Conflux 开放世界评估（表3）:**

| 分类器 | Baseline π₁₀ | Cross-Network π₁₀ | Cross-Network R | Cross-Network F₁ | Pooled π₁₀ | Pooled R | Pooled F₁ |
|--------|-------------|-------------------|-----------------|-------------------|-------------|----------|-----------|
| k-FP | 0.861 | 0.717 | 0.307 | 0.430 | 0.970 | 0.915 | 0.942 |
| **DF** | **0.951** | **0.956** | **0.922** | **0.939** | **0.979** | **0.966** | **0.973** |
| Tik-Tok | 0.947 | 0.901 | 0.844 | 0.872 | 0.980 | 0.948 | 0.964 |
| RF | 0.969 | 0.089 | 0.031 | 0.046 | 0.980 | 0.968 | 0.974 |
| Holmes | 0.970 | 0.176 | 0.004 | 0.009 | 0.950 | 0.956 | 0.953 |

**Conflux 单 leg 评估（表6）:**

| 分类器 | Train AU π₁₀ | Train AU R | Train AU F₁ | Train UK π₁₀ | Train UK R | Train UK F₁ |
|--------|-------------|------------|-------------|--------------|------------|-------------|
| k-FP | 0.130 | 0.090 | 0.107 | 0.387 | 0.228 | 0.287 |
| DF | 0.558 | 0.287 | 0.379 | 0.616 | 0.285 | 0.389 |
| Tik-Tok | 0.399 | 0.237 | 0.297 | 0.563 | 0.369 | 0.446 |
| RF | 0.009 | 0.002 | 0.003 | 0.537 | 0.557 | 0.547 |
| Holmes | 0.018 | 0.011 | 0.013 | 0.378 | 0.346 | 0.361 |

**概念漂移评估（表5 - UK客户端，纵向研究）:**

| 分类器 | Month 0 F₁ | Month 2 F₁ | Month 6 F₁ | 6个月衰减 |
|--------|-----------|-----------|-----------|----------|
| k-FP | 0.926 | 0.761 | 0.547 | -0.379 |
| DF | 0.967 | 0.854 | 0.685 | -0.282 |
| Tik-Tok | 0.956 | 0.827 | 0.653 | -0.303 |
| **RF** | **0.972** | **0.907** | **0.754** | **-0.218** |
| Holmes | 0.966 | 0.740 | 0.622 | -0.344 |

**强大 Guard 模拟（Conflux + RTT优势）:**

| Added RTT | FS Fraction | DF TPR | RF TPR |
|-----------|------------|--------|--------|
| 0 ms | ~45% | 0.189 | ~0.200 |
| 32 ms | ~60% | ~0.380 | ~0.380 |
| 64 ms | ~70% | ~0.500 | ~0.500 |
| 128 ms | ~85% | 0.736 | 0.881 |
| 256 ms | ~92% | ~0.850 | ~0.850 |
| 512 ms | ~96% | ~0.880 | ~0.880 |

### 优势场景

1. **DF 在跨网络条件下表现最佳**：仅依赖方向序列，对时序变化鲁棒
2. **RF 在概念漂移下最稳定**：6 个月后仍保持 0.754 F₁
3. **DF 在小训练集下高效**：70 traces/page 即可达到 0.90 TPR
4. **非监控训练数据越多越好**：从 1,000 到 20,000 traces，FPR 从 0.008 降至 0.002

### 局限性

1. **RF/Holmes 跨网络失效**：时序依赖特征对网络延迟差异极度敏感
2. **Conflux 显著降低攻击效果**：单 leg 观察下 F₁ 从 0.939 降至 0.379 (DF)
3. **早期检测困难**：跨网络条件下，DF 需要 90% 数据才能达到 0.8 TPR
4. **概念漂移持续影响**：6 个月后所有方法 F₁ 下降 0.2-0.4

## 7. 核心贡献与创新

### 贡献总结

| 贡献 | 说明 |
|------|------|
| 隐私保护方法论 | Guard 视角 + 临时标识符 + 严格清洗，首次实现真实开放世界数据采集 |
| Guard 攻击者分析 | 首次分析 Guard 的独特攻击优势：控制数据移除、circuit 去复用、流隔离利用 |
| 真实开放世界验证 | 首次证明 WF 在真实 Tor 流量中仍然高度有效（DF: π₁₀=0.956, R=0.922） |
| Conflux 系统评估 | 首次评估 Conflux 对 WF 的影响，以及强大 Guard 的攻击恢复能力 |
| 数据集开源 | 800,000+ traces 数据集公开发布 |

### 方法论改进对比

| 维度 | Cherubin 设置 | 本工作设置 | 改进 |
|------|--------------|-----------|------|
| 训练监控标签 | Domain 级 | Page 级 | 更精确的分类目标 |
| 训练-测试 vantage | Exit→Guard | Guard→Guard | 消除特征失真 |
| 非监控流量来源 | 真实 (exit) | 真实 (guard) | 同样真实 |
| 数据规模 | 中等 | 800,000+ | 大幅扩展 |
| Conflux 评估 | 无 | 首次系统评估 | 新增维度 |

## 8. 对 encrypted-traffic-analysis 领域的启示

### 关键发现

1. **WF 威胁仍然真实**：即使在真实 Tor 开放世界中，现代 WF 攻击仍然高度有效，反驳了"WF 在实际部署中无效"的观点。
2. **时序无关特征更鲁棒**：DF（仅使用方向序列）在跨网络条件下显著优于 RF/Holmes（依赖时序特征），说明方向序列是更可靠的 WF 特征。
3. **Conflux 不是银弹**：虽然 Conflux 降低了 guard 攻击者的效果，但具有延迟优势的 guard 仍能恢复大部分攻击能力。
4. **训练策略决定成败**：使用合成监控流量 + 真实非监控流量的训练策略比 Cherubin 的 exit 训练策略更有效。
5. **Guard 是高风险位置**：Guard 节点的持久性、流隔离可见性使其成为特别危险的攻击者。

### 防御启示

- 仅依赖流量分割（如 Conflux）不足以防御 WF 攻击
- 需要更根本的防御机制来模糊流量模式
- 时序混淆防御可能比流量分割更有效（针对时序依赖攻击）

## 9. 关联知识（与已读论文的关系、领域定位）

### 与 [[website-fingerprinting]] 领域的关系

- **延续 DF 系列**：直接使用 Sirinam et al. (CCS 2018) 的 Deep Fingerprinting 作为主要评估对象，验证其在真实场景中的有效性
- **回应 Cherubin 质疑**：反驳 Cherubin et al. (USENIX Security 2022) 关于"WF 在实际中无效"的结论，通过改进方法论证明 WF 仍然有效
- **扩展 Wang 的评估框架**：使用 Tao Wang (S&P 2020) 的 r-precision 指标进行开放世界评估

### 与 [[encrypted-traffic-analysis]] 领域的关系

- **元数据分析范例**：仅使用 packet direction 和 timing 元数据（不需 payload），展示加密流量分析的可行性
- **跨网络泛化挑战**：揭示了流量分析模型在不同网络条件下泛化的困难，特别是时序依赖方法

### 与 [[survey-website-fingerprinting]] 的关系

- **填补 Conflux 空白**：首次系统评估 Tor Conflux 对 WF 的影响，填补了 survey 中未覆盖的领域
- **方法论标准化**：提出了一种可复现的隐私保护评估方法论，可作为未来 WF 研究的标准

### 被引用/引用的关键论文

| 论文 | 关系 | 说明 |
|------|------|------|
| Sirinam et al. (CCS 2018) - DF | 直接使用 | 本文主要评估的 WF 攻击 |
| Cherubin et al. (USENIX Security 2022) | 对比/反驳 | 本文方法论的核心对比对象 |
| Shen et al. (USENIX Security 2023) - RF | 直接使用 | 评估的 WF 攻击，在概念漂移下表现最佳 |
| Deng et al. (CCS 2024) - Holmes | 直接使用 | 评估的早期检测 WF 攻击 |
| Wang (S&P 2020) | 方法论基础 | r-precision 评估指标 |
| Tor Proposal 329 - Conflux | 研究对象 | 首次系统评估其对 WF 的影响 |

## 10. 开放问题与未来方向

### 未解决问题

1. **真实监控流量评估**：合成监控流量与真实用户浏览的差异程度未知
2. **动态页面影响**：现代网站的动态内容（JS 渲染、实时更新）对 WF 的影响未评估
3. **Conflux 调度优化**：是否存在能防御 WF 的 Conflux 调度算法？
4. **多 tab 场景**：虽然 Guard 可以去复用，但真实多 tab 浏览的复杂交互未充分评估
5. **Bridge 节点影响**：未探索 bridge 节点作为攻击位置的可行性

### 未来研究方向

1. **Conflux 调度防御设计**：设计抗 WF 的 Conflux 调度算法（如随机化调度）
2. **真实监控流量对比**：比较合成 vs 真实监控流量的分类难度差异
3. **时序鲁棒 WF**：开发对网络延迟不敏感的 WF 特征表示
4. **持续学习应对概念漂移**：开发能自适应网页变化的 WF 模型
5. **多视角攻击融合**：结合 Guard 和 ISP 视角的联合攻击

## 11. 批判性评价

### 优点

1. **方法论严谨**：隐私保护设计周全，数据清洗流程详尽且可复现
2. **实验规模大**：800,000+ traces，三地客户端，首次 Conflux 评估
3. **结果有说服力**：跨网络条件下 DF 仍然有效，直接反驳了 WF 无效论
4. **开源数据集**：促进领域可复现性和后续研究
5. **伦理考量充分**：详细的伦理分析、利益相关者讨论、缓解措施

### 缺点

1. **监控网页选择**：Tranco 10,000 以外的网站可能不具代表性，敏感网站可能排名更高
2. **合成流量局限**：虽然论证了合理性，但无法证明合成流量与真实用户行为等价
3. **Conflux 评估有限**：仅评估 LowRTT 策略，未探索其他调度算法或防御增强
4. **未与 ISP 攻击者直接对比**：Guard 和 ISP 视角的差异未在相同条件下量化比较
5. **概念漂移评估时间跨度有限**：仅 6 个月，长期漂移影响未知

### 结论可靠性

总体结论可靠：WF 在真实 Tor 开放世界中仍然有效。但 Conflux 作为防御机制的有效性评估可能过于乐观——仅评估了默认配置，未探索防御增强选项。Guard 强大攻击者的结果展示了理论上限，实际中达到 128ms RTT 优势的可行性需要进一步验证。

## 12. 关键引用

### 必读引用

| 引用 | 重要性 | 说明 |
|------|--------|------|
| Sirinam et al. (CCS 2018) | 核心 | Deep Fingerprinting 原始论文 |
| Cherubin et al. (USENIX Security 2022) | 核心 | 被反驳的 WF 现实性评估 |
| Wang (S&P 2020) | 方法论 | r-precision 开放世界评估框架 |
| Tor Proposal 329 | 背景 | Conflux 流量分割协议规范 |
| Hayes & Danezis (USENIX Security 2016) | 基础 | k-Fingerprinting 方法 |
| Shen et al. (USENIX Security 2023) | 对比 | Robust Fingerprinting 方法 |
| Deng et al. (CCS 2024) | 对比 | Holmes 早期检测方法 |
| Juarez et al. (CCS 2014) | 基础 | WF 评估批评性分析 |

### 方法论参考

| 引用 | 用途 |
|------|------|
| Wang & Goldberg (PoPETs 2016) | 现实 WF 攻击讨论 |
| Jansen et al. (WPES 2023) | WF 重新定位研究 |
| Rimmer et al. (NDSS 2018) | 自动化 WF 深度学习 |

### 工具与数据

| 资源 | 链接 | 说明 |
|------|------|------|
| 数据集 | https://osf.io/9m8ea/ | 800,000+ traces 数据集 |
| Tranco List | https://tranco-list.eu/ | 网站排名数据源 |

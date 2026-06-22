---
type: paper
title_original: "WFDefProxy: Real World Implementation and Evaluation of Website Fingerprinting Defenses"
title_cn: "WFDefProxy：Website Fingerprinting 防御的真实世界实现与评估"
authors: ["Jiajun Gong", "Wuqi Zhang", "Charles Zhang", "Tao Wang"]
year: 2024
venue: "IEEE TIFS 2024"
doi: "10.1109/TIFS.2023.3327662"
url: unknown
pdf: unknown
mineru_md: "02-parsed-markdown/2024-TIFS-WFDefProxy__Real_World_Implementation_and_Evaluation_of_Website_Fingerprinting_Defenses.md"
status: processed
reading_level: L2
research_area: ["website fingerprinting", "traffic analysis", "anonymity network", "defense evaluation"]
task: ["WF defense implementation", "simulation vs implementation comparison", "defense benchmarking"]
method: ["pluggable transport proxy", "state machine defense control", "soft stop condition", "empirical Tor evaluation"]
dataset: ["Tranco top-100 websites", "defended/undefended Tor traces (100x100 closed-world)", "open-world 90000 non-monitored traces"]
code: "https://github.com/websitefingerprinting/wfdef"
relevance: medium
created: "2026-06-21"
updated: "2026-06-21"
---

# WFDefProxy: Real World Implementation and Evaluation of Website Fingerprinting Defenses

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | WFDefProxy: Real World Implementation and Evaluation of Website Fingerprinting Defenses |
| 中文标题 | WFDefProxy：Website Fingerprinting 防御的真实世界实现与评估 |
| 作者 | Jiajun Gong, Wuqi Zhang, Charles Zhang, Tao Wang |
| 年份 | 2024（发表于 2023-10-25，TIFS current version 2023-12-07） |
| 会议/期刊 | IEEE Transactions on Information Forensics and Security (TIFS) 2024 |
| 研究方向 | [[website-fingerprinting]] 防御实现与评估、[[encrypted-traffic-analysis]] |
| 任务类型 | WF 防御平台搭建、simulation vs implementation 对比评估 |
| 方法关键词 | pluggable transport, obfs4proxy 扩展, state machine, soft stop condition, optimistic/pessimistic simulation strategy |
| 数据集 | Tranco top-100 网站, 100x100 closed-world traces, 90000 open-world non-monitored traces, 多时间段重复采集 |
| 是否开源 | 是（https://github.com/websitefingerprinting/wfdef + WFCrawler） |

## 1. 一句话总结

> 本文构建了 WFDefProxy——首个基于 Tor pluggable transport 的通用 [[website-fingerprinting-defense]] 实现平台，实现了 FRONT、Tamaraw、RegulaTor、Random-WT 四种防御，并通过真实 Tor 网络实验系统性地揭示了模拟评估的不准确性：Tamaraw 时间开销被低估 22% 或高估 24%，RegulaTor 时间开销被低估 30-40%，网络拥塞是模拟无法捕捉的关键误差来源。

## 2. 摘要翻译

### 2.1 摘要原文

Tor, an onion-routing anonymity network, can be attacked by Website Fingerprinting (WF), which de-anonymizes encrypted web browsing traffic by analyzing its unique sequence characteristics. Although many defenses have been proposed, few have been implemented and tested in the real world; most state-of-the-art defenses were only simulated. Simulations fail to capture the real performance of these defenses as they make simplifying assumptions about the protocol stack and network conditions. To allow WF defenses to be analyzed as real implementations, we create WFDefProxy, the first general platform for WF defense implementation on Tor as pluggable transports. We implement three state-of-the-art WF defenses: FRONT, Tamaraw, and RegulaTor. We evaluate each defense extensively by directly collecting defended datasets under WFDefProxy. Our results show that simulation can be inaccurate in many cases. Specifically, Tamaraw's time overhead was underestimated by 22% in one setting and overestimated by 24% in another. RegulaTor's time overhead was underestimated by 30-40%. We find that a major source of simulation inaccuracy is that they cannot incorporate how packets depend on each other. We also find that adverse network conditions (which are ignored in simulation), especially congestion, can affect the evaluated overhead of defenses. These results show that it is important to evaluate defenses as implementations instead of only simulations to avoid errors in evaluation.

### 2.2 摘要中文翻译

Tor 作为一种洋葱路由匿名网络，可被 Website Fingerprinting (WF) 攻击——通过分析加密 Web 浏览流量的独特序列特征来去匿名化用户。尽管已有多种防御方案被提出，但很少有方案在真实环境中实现和测试；大多数 SOTA 防御仅通过模拟评估。模拟无法捕捉这些防御的真实性能，因为它们对协议栈和网络条件做了简化假设。为使 WF 防御能以真实实现的方式被分析，我们创建了 WFDefProxy——首个在 Tor 上以 pluggable transport 形式实现 WF 防御的通用平台。我们实现了三种 SOTA 防御：FRONT、Tamaraw 和 RegulaTor，并通过 WFDefProxy 直接采集受防御保护的数据集进行广泛评估。结果表明，模拟在多种情况下存在不准确性：Tamaraw 的时间开销在一种设置下被低估 22%，在另一种设置下被高估 24%；RegulaTor 的时间开销被低估 30-40%。我们发现模拟不准确的一个主要来源是无法纳入数据包之间的依赖关系。此外，模拟中被忽略的不利网络条件（尤其是拥塞）也会影响防御的评估开销。这些结果表明，仅依靠模拟来评估防御是不够的，必须结合真实实现来避免评估误差。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

**WF 防御评估的根本缺陷**：绝大多数 [[website-fingerprinting-defense]] 仅通过模拟（simulation）进行评估，即在采集的未防御流量上按理论效果注入假包或延迟真实包。这种做法存在三个系统性问题：

1. **忽略实现挑战**：模拟忽略了实际部署中的工程复杂性。防御的鲁棒性可能依赖于在真实场景中难以满足的假设。
2. **简化包依赖关系**：模拟中对数据包之间的依赖关系做了过度简化。例如，出站包的延迟模拟可能无法准确反映其与触发的入站包之间的交互。
3. **忽略网络协议与拥塞交互**：模拟无法捕捉网络协议和网络拥塞之间的交互效应，而不同网络条件对 WF 防御的影响几乎没有被研究。

**现有框架的局限**：

| 框架 | 局限性 |
|---|---|
| WFPadTools | 无数据加密，已停止维护，只实现了 WTF-PAD |
| Basket2 | 缺乏防御启停控制机制，以 burst 为粒度而非 page load，简化了 Tamaraw 协议 |
| Circuit Padding Framework (CPF) | 不支持延迟类防御（如 Tamaraw、RegulaTor），缺少仅在加载开始时触发 padding 的机制 |

### 3.2 核心研究问题

- **RQ1 (Evaluation)**：模拟对防御评估是否有用？模拟与真实实现的结果差异有多大？
- **RQ2 (Parametrization)**：模拟能否确定最优防御参数？模拟是否正确刻画了参数变化对防御的影响？
- **RQ3 (Network conditions)**：模拟无法研究的不利网络条件（如低带宽）如何影响真实实现？

## 4. 方法设计

### 4.1 WFDefProxy 平台架构

WFDefProxy 基于 obfs4proxy（广泛使用的 Tor pluggable transport 代理）扩展构建，核心设计：

- **通用防御类**：所有防御通过继承通用类实现，覆写 `Read` 和 `Write` 函数分别处理上下行数据。Tamaraw 实现仅约 400 行代码。
- **状态机控制**：设计状态机系统控制防御的启动和停止，支持多种防御状态（图 3 展示了 Tamaraw 客户端的四状态有限状态机：Stop → Ready → Start → Padding）。
- **信号包机制**：定义信号包（signal packet）便于双方同步启停 padding。
- **加密层**：在 Tor 加密之上添加另一层加密（obfs4proxy 加密模块），使攻击者无法区分真实包和假包。
- **帧头开销**：每个 WFDefProxy 帧增加 5 字节头部 + 16 字节加密认证标签，约 4% 额外数据开销，帧封装仅需 0.002 ms。

### 4.2 Soft Stop Condition（软停止条件）

网络层防御在真实环境中无法精确知道页面何时加载完毕。WFDefProxy 的解决方案：

- 观察真实包的吞吐量，在 4 秒时间窗口内若出站包不超过 1 个，则判定页面加载完成
- 4 秒窗口的选择依据：98.8% 的未防御数据集中连续出站包间隔 < 1 秒
- 实验中 96% 的 FRONT trace 重启事件不超过 1 次（76% 为零重启）

### 4.3 四种防御实现

| 防御 | 类型 | 核心机制 | 关键参数 |
|---|---|---|---|
| **Tamaraw** | 规则化（Regularized） | 固定间隔发送包（客户端 ρ_out ms，代理端 ρ_in ms），加载结束后继续填充至 trace 长度为 L 的倍数 | ρ_out=14, ρ_in=4, L=100 |
| **FRONT** | 非规则化（Non-regularized） | 不延迟真实包，仅在 trace 前端注入随机假包，时间戳采样自 Rayleigh 分布 | N=10000, α=0.5, W_min=1, W_max=14 |
| **RegulaTor** | 规则化（Regularized） | 以指数衰减速率发送 burst，支持 impatient packet 机制降低延迟 | R=277, D=0.940, T=3.55, N=3550, U=3.95, C=1.77 |
| **Random-WT** | 规则化（Regularized） | Walkie-Talkie 的简化版，在真实 burst 上添加 padding 并随机插入假 burst，WFDefProxy 通过状态机实现半双工 | N_out^real=4, N_in^real=45, p_fake=0.4 |

## 5. 实验设计

### 5.1 部署环境

| 组件 | 配置 |
|---|---|
| 合作代理（Bridge） | Microsoft Azure 服务器，1 CPU (2.3 GHz), 2 GB RAM, Debian 9.11, Tor 0.4.4.5 |
| 客户端 | 大学服务器，128 CPU cores, 500 GB RAM, 1 Gbps 总带宽, Ubuntu 18.04.4 LTS |
| 浏览器 | Tor Browser 10.0.15，每次访问使用全新 Bundle 副本 |
| 并行采集 | 8-12 Docker 容器，每个页面最多 70 秒加载时间，加载后等待 5 秒 |

### 5.2 数据集

- **网站列表**：Tranco top-100（2022-01-21 生成），去除不可访问和重复 URL
- **采集规模**：每个监控页面至少 100 个实例，闭世界 100x100 traces
- **开世界**：额外采集 90,000 条非监控 trace（2022 年 7 月）
- **时间一致性**：每个受防御数据集与 4 天内采集的未防御数据集对比
- **采集耗时**：约 4 个月

### 5.3 攻击方法

| 攻击 | 分类器 | 特点 |
|---|---|---|
| kFP | Random Forests + kNN | 高精度但低 TPR |
| CUMUL | SVM + cumulative representation | 低 FPR 但高 FPR 导致低 precision |
| DF | CNN | 深度学习攻击 |
| Tik-Tok | CNN | 利用包时序信息，总体表现最强 |

评估设置：10-fold cross-validation，输入长度 20,000，训练 30 epochs。

### 5.4 模拟策略

| 策略 | 假设 | 使用者 |
|---|---|---|
| **乐观策略（Optimistic）** | 每个包与其他包信息独立，各方向包分配到原始时间戳之后最近的时隙 | RegulaTor 原论文 |
| **悲观策略（Pessimistic）** | 每个包依赖所有先前两个方向的包，包分配到所有先前包之后最近的时隙 | Tamaraw 原论文 |

## 6. 核心结果

### 6.1 RQ1：模拟 vs 实现——开销对比

| 防御 | 数据开销 Sim. (%) | 数据开销 Imp. (%) | 时间开销 Sim. (%) | 时间开销 Imp. (%) | 误差方向 |
|---|---|---|---|---|---|
| Tamaraw | 107 | 114 | 41 | 61 | 时间开销低估 20% |
| FRONT | 72 | 81 | 0 | 1 | 基本准确 |
| RegulaTor | 36 | 58 | 32 | 62 | 时间开销低估 30% |
| Random-WT | 88 | 82 | 59 | 37 | 时间开销高估 22% |

### 6.2 RQ1：模拟策略对开销的影响

| 防御 | 策略 | 数据开销 (%) | 时间开销 (%) |
|---|---|---|---|
| Tamaraw | 乐观 | 90 | 29 |
| Tamaraw | 悲观* | 107 | 41 |
| Tamaraw | 实现 | 114 | 61 |
| RegulaTor | 乐观* | 36 | 32 |
| RegulaTor | 悲观 | 47 | 32 |
| RegulaTor | 实现 | 58 | 62 |

**关键发现**：即使悲观策略也低估了开销。Tamaraw 的悲观模拟低估时间开销 22%（ρ_in=4, ρ_out=10），高估 24%（ρ_in=6, ρ_out=26）。RegulaTor 两种策略给出相同的时间开销，因为 impatient packet 机制打破了包依赖关系。

### 6.3 RQ1：攻击准确率对比

| 防御 | 设置 | kFP (%) | CUMUL (%) | DF (%) | Tik-Tok (%) |
|---|---|---|---|---|---|
| Tamaraw | Sim. | 2.19 | 17.63 | 17.11 | 16.61 |
| Tamaraw | Imp. | 6.43 | 9.73 | 10.20 | 17.85 |
| FRONT | Sim. | 25.86 | 20.22 | 60.17 | 72.16 |
| FRONT | Imp. | 30.82 | 19.94 | 55.95 | 68.52 |
| RegulaTor | Sim. | 48.73 | 24.13 | 29.01 | 43.43 |
| RegulaTor | Imp. | 42.76 | 30.06 | 55.62 | 55.88 |
| Random-WT | Sim. | 68.56 | 69.89 | 93.65 | 95.69 |
| Random-WT | Imp. | 62.88 | 67.30 | 91.55 | 92.87 |

**关键发现**：RegulaTor 的攻击准确率在实现中显著高于模拟——DF 从 29% 飙升至 56%，Tik-Tok 从 43% 升至 56%。根本原因是 RegulaTor 的 "surge 特征" 在真实 trace 中与模拟差异巨大：

| 设置 | 平均 surge 数 | surge 数方差 | RF 仅用 surge 特征准确率 (%) |
|---|---|---|---|
| 模拟 | 3.28 | 1.98 | 12.90 |
| 实现 | 5.48 | 3.93 | 33.20 |

### 6.4 RQ2：参数化分析

**Tamaraw**：模拟预测增大 ρ_out 会增加时间开销，但实现结果相反——当 ρ_in=4ms 时，ρ_out 从 14ms 增至 26ms，时间开销从 60% 降至 47%。原因是小 ρ_out 增加数据开销进而引发拥塞，而模拟无法捕捉此效应。

**FRONT**：模拟在参数化方面较为准确。W_max 从 6 增至 30 秒时，数据开销从 82% 降至 60%（模拟从 77% 降至 54%），Tik-Tok 准确率差异在 4% 以内。

**RegulaTor**：原始论文报告 Light/Heavy 时间开销分别为 8.9%/6.6%，但本研究实现结果为 78%/62%。差异部分来源于网页流量增长（本研究平均每 trace 7903 cells vs 原研究 2101 cells）和不同的采集方法。

### 6.5 RQ3：网络带宽影响

| 防御 | 设置 | 大学 1Gbps 时间开销 (%) | Azure 2Gbps 时间开销 (%) | 差异 |
|---|---|---|---|---|
| Tamaraw | ρ_out=10 | 60 | 45 | -15% |
| Tamaraw | ρ_out=14 | 60 | 42 | -18% |
| RegulaTor | Light | 78 | 51 | -27% |
| RegulaTor | Heavy | 62 | 41 | -21% |

**FRONT 在低带宽下的表现**：当带宽限制为 1 Mbps 时，FRONT 也产生了显著时间开销——N=2000 时 6%，N=20000 时 16%。这证实了即使设计为零延迟的防御，在带宽受限时也会因拥塞产生延迟。

## 7. 开世界评估

| 防御 | DF TPR (%) | DF FPR (%) | DF π_10 (%) | Tik-Tok TPR (%) | Tik-Tok FPR (%) | Tik-Tok π_10 (%) |
|---|---|---|---|---|---|---|
| Undefended | 96.97 | 0.32 | 75.49 | 96.35 | 0.27 | 78.00 |
| Tamaraw | 14.50 | 0.07 | 14.51 | 7.81 | 0.04 | 14.40 |
| FRONT | 48.86 | 1.98 | 19.62 | 55.36 | 1.83 | 23.35 |

Tamaraw 在开世界场景中对所有攻击仍然有效（最佳攻击 DF 仅 15% TPR）。FRONT 对 kFP 和 CUMUL 接近 Tamaraw 的效果（TPR < 8%），但 Tik-Tok 仍有 55% TPR。

## 8. 实现一致性验证

在 2021 年 5 月和 2022 年 7 月两个时间点重复采集开世界数据集，验证防御性能的可重复性。DF 在两个时间段对 Tamaraw 和 FRONT 的保护率表现相似，证实了 WFDefProxy 实现的稳定性。

## 9. 何时应避免使用模拟？

论文总结了模拟不可靠的四类场景：

1. **规则化防御的开销评估**：乐观/悲观假设都会扭曲开销评估，悲观 Tamaraw 最差情况下低估时间开销 22%、数据开销 14%
2. **高延迟防御**：更频繁引发拥塞和重传等网络事件，模拟无法捕捉
3. **时间敏感防御**：如 RegulaTor 和 CS-BuFLO 动态调整发送速率，对时间因素高度敏感，RegulaTor 时间开销被低估一半
4. **页面加载结束敏感防御**：如 Tamaraw，真实环境中识别页面加载结束是难题

## 10. 关键贡献总结

| 贡献 | 说明 |
|---|---|
| WFDefProxy 平台 | 首个通用 WF 防御实现平台，支持所有已知网络层防御，基于 obfs4proxy 扩展 |
| 四种防御首次完整实现 | FRONT、Tamaraw、RegulaTor、Random-WT 的首次真实 Tor 部署 |
| 模拟不准确性系统性量化 | 首次系统比较乐观/悲观模拟策略，揭示包依赖和拥塞是主要误差来源 |
| 网络条件影响首次评估 | 首次评估带宽对 WF 防御开销和效果的影响 |
| Random-WT 评估 | 首次评估 Random-WT，发现其几乎没有防御效果 |

## 11. 局限性

- **信任模型限制**：WFDefProxy 作为 pluggable transport 部署，bridge 是可信方；但现实中 bridge 可能是 WF 攻击者，理想应在 middle node 部署（需 Tor 协议变更）
- **网站列表局限**：仅使用 Tranco top-100，可能不代表不同浏览偏好用户的真实防御性能
- **单一 bridge**：仅使用一个私有 bridge 作为合作代理，未测试多 bridge 场景
- **参数与网络条件未联合优化**：将参数化和网络条件作为独立问题研究，现实中最优参数可能依赖网络条件
- **仅闭世界为主**：为减少数据采集时间和对 Tor 网络的影响，主要在闭世界场景评估

## 12. 对后续研究的启示

### 12.1 方法论启示

- **WF 防御必须结合实现评估**：仅靠模拟无法给出可靠的开销和效果评估，尤其是规则化防御
- **包依赖关系是模拟的根本瓶颈**：乐观和悲观策略都无法准确建模真实包间依赖
- **拥塞效应不可忽视**：数据开销和时间开销在模拟中被假设为独立，但真实环境中高数据开销会引发拥塞进而增加时间开销

### 12.2 与 [[survey-website-fingerprinting]] 的关联

本文填补了 [[website-fingerprinting]] 领域长期缺乏的 defense implementation 评估空白。此前 WF 防御研究主要依赖模拟，本文证明这种做法在多种场景下会产生误导性结论。这对 [[website-fingerprinting-defense]] 的未来研究具有重要的方法论指导意义。

### 12.3 对防御设计的启示

- FRONT 作为零延迟防御，在高带宽下模拟较准确，但在低带宽下仍可能因拥塞产生时间开销
- RegulaTor 的 surge 特征在真实环境中泄露的信息远超模拟预期，设计时需考虑更细粒度的特征泄露
- Random-WT 的无效性说明简化版 Walkie-Talkie 在面对现代攻击时已不再有效

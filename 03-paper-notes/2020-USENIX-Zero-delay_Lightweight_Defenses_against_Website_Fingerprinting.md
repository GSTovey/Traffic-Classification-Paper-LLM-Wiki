---
type: paper
title_original: "Zero-delay Lightweight Defenses against Website Fingerprinting"
title_cn: "零延迟轻量级网站指纹防御"
authors:
  - Jiajun Gong
  - Tao Wang
year: 2020
venue: "USENIX Security 2020"
doi: unknown
url: "https://www.usenix.org/conference/usenixsecurity20/presentation/gong"
pdf: "00-inbox/PDFs/2020-USENIX-Zero-delay_Lightweight_Defenses_against_Website_Fingerprinting.pdf"
mineru_md: "02-parsed-markdown/2020-USENIX-Zero-delay_Lightweight_Defenses_against_Website_Fingerprinting.md"
status: processed
reading_level: L3
research_area:
  - website-fingerprinting
  - website-fingerprinting-defense
  - encrypted-traffic-analysis
  - anonymity-network
  - privacy-preserving
task:
  - website-fingerprinting-defense
  - Tor-traffic-protection
  - traffic-padding
method:
  - front-obfuscation
  - trace-gluing
  - rayleigh-distribution-padding
  - split-decision-attack
  - CDSB-split-finding
dataset:
  - "DS-19: Alexa top 100 + 10000 non-monitored (2019)"
  - "DS-14: Wang 2014 dataset (9000 monitored + 9000 non-monitored)"
code: "https://github.com/websitefingerprinting/WebsiteFingerprinting/"
relevance: high
related_papers:
  - "2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning"
  - "2020-CCS-TrafficSliver-Fighting_Website_Fingerprinting_Attacks_with_Traffic_Splitting"
  - "2024-S&P-Real-Time_Website_Fingerprinting_Defense_via_Traffic_Cluster_Anonymization"
created: "2026-06-21"
updated: "2026-06-21"
---

# Zero-delay Lightweight Defenses against Website Fingerprinting

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Zero-delay Lightweight Defenses against Website Fingerprinting |
| 中文标题 | 零延迟轻量级网站指纹防御 |
| 作者 | Jiajun Gong, Tao Wang |
| 机构 | Hong Kong University of Science and Technology |
| 会议/期刊 | USENIX Security 2020 |
| 发表时间 | 2020年8月 |
| 研究方向 | [[website-fingerprinting-defense]]、[[encrypted-traffic-analysis]]、匿名网络隐私保护 |
| 任务类型 | [[website-fingerprinting-defense]]、Tor 流量保护、流量填充 |
| 方法关键词 | FRONT（前部随机混淆）、GLUE（流量粘合）、Rayleigh 分布填充、trace-to-trace 随机化、CDSB 分割框架 |
| 数据集 | DS-19（Alexa top 100 各 100 次 + 10000 非监控页面，2019 年）；DS-14（Wang 2014 数据集，9000 监控 + 9000 非监控） |
| 是否开源 | 是（https://github.com/websitefingerprinting/WebsiteFingerprinting/） |
| PDF | `00-inbox/PDFs/2020-USENIX-Zero-delay_Lightweight_Defenses_against_Website_Fingerprinting.pdf` |
| MinerU Markdown | `02-parsed-markdown/2020-USENIX-Zero-delay_Lightweight_Defenses_against_Website_Fingerprinting.md` |

---

## 1. 一句话总结

> FRONT 通过 Rayleigh 分布在 trace 前部注入随机数量的虚拟包来混淆攻击者最依赖的特征丰富区域，GLUE 通过在相邻 trace 间隙注入"粘合流量"将多个独立 trace 融合为长连续 trace 迫使攻击者解决困难的分割问题，两者均实现零延迟、低开销，在 33% 数据开销下 FRONT 优于 WTF-PAD，GLUE 在 22%-44% 开销下可将最佳 WF 攻击的 TPR 和 precision 降至个位数。

---

## 2. 摘要翻译

### 2.1 摘要原文

Website Fingerprinting (WF) attacks threaten user privacy on anonymity networks because they can be used by network surveillants to identify the webpage being visited by extracting features from network traffic. A number of defenses have been put forward to mitigate the threat of WF, but they are flawed: some have been defeated by stronger WF attacks, some are too expensive in overhead, while others are impractical to deploy.

In this work, we propose two novel zero-delay lightweight defenses, FRONT and GLUE. We find that WF attacks rely on the feature-rich trace front, so FRONT focuses on obfuscating the trace front with dummy packets. It also randomizes the number and distribution of dummy packets for trace-to-trace randomness to impede the attacker's learning process. GLUE adds dummy packets between separate traces so that they appear to the attacker as a long consecutive trace, rendering the attacker unable to find their start or end points, let alone classify them. Our experiments show that with 33% data overhead, FRONT outperforms the best known lightweight defense, WTF-PAD, which has a similar data overhead. With around 22%--44% data overhead, GLUE can lower the accuracy and precision of the best WF attacks to a degree comparable with the best heavyweight defenses. Both defenses have no latency overhead.

### 2.2 摘要中文翻译

网站指纹（WF）攻击威胁匿名网络上的用户隐私，因为网络监控者可以通过从网络流量中提取特征来识别用户正在访问的网页。已有多种防御方案被提出以缓解 WF 威胁，但均存在缺陷：部分已被更强的 WF 攻击攻破，部分开销过大，还有部分在实际部署中不可行。

本文提出两种新颖的零延迟轻量级防御方案 FRONT 和 GLUE。我们发现 WF 攻击依赖特征丰富的 trace 前部，因此 FRONT 专注于用虚拟包混淆 trace 前部，并随机化虚拟包的数量和分布以实现 trace-to-trace 随机性，从而阻碍攻击者的学习过程。GLUE 在不同 trace 之间添加虚拟包，使它们在攻击者看来呈现为一条长连续 trace，使攻击者无法找到其起止点，更不用说进行分类。实验表明，在 33% 数据开销下，FRONT 优于已知最佳轻量级防御 WTF-PAD（具有相似数据开销）。在约 22%-44% 数据开销下，GLUE 可将最佳 WF 攻击的准确率和精度降低到与最佳重量级防御相当的水平。两种防御均无延迟开销。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

WF 防御领域存在一个根本性的**三难困境**：安全性、低延迟、低开销无法同时满足。作者的核心观察是现有防御方案分为三类，各有致命缺陷：

**现有防御的系统性分类与失败原因**：

| 防御类别 | 代表方案 | 失败原因 |
|---|---|---|
| Obfuscation（混淆） | WTF-PAD, Traffic Morphing, HTTPOS | 已被 DF 等深度学习攻击攻破（DF 在 WTF-PAD 下 F1=0.70） |
| Confusion（混淆） | Decoy, Supersequence, Walkie-Talkie | 高开销或需额外基础设施（页面知识、半双工浏览器修改） |
| Regularization（规范化） | BuFLO, CS-BuFLO, Tamaraw | 极高延迟和带宽开销（Tamaraw: 78% 延迟 + 163% 带宽） |

**核心洞察**：
1. WF 攻击高度依赖 trace 的前几秒（"trace front"）——kNN 和 kFP 显式使用 trace front 信息进行分类
2. 所有已知 WF 攻击都假设每个待分类 trace 对应一个网页（singleton trace），当多个网页的 trace 无间隙连接时（-trace），攻击者必须先解决分割问题

### 3.2 现有方法的痛点和不足

| 现有方法 | 痛点 | 关键数据 | 本文解决方案 |
|---|---|---|---|
| WTF-PAD | 无法抵抗 DF 攻击；参数调优依赖数据集 | DF F1=0.70, kFP F1=0.61 | FRONT 用更简单方案在同开销下降低 DF F1 至 0.47 |
| Tamaraw | 延迟和带宽开销极高，影响用户体验 | 78% 延迟 + 163% 带宽开销 | FRONT/GLUE 零延迟 + 22%-48% 带宽 |
| Walkie-Talkie | 需修改浏览器为半双工模式，需页面大小知识 | 需要额外基础设施 | FRONT/GLUE 无需任何额外基础设施 |
| Supersequence | 需要页面大小知识，极高开销 | 需要额外基础设施 | FRONT/GLUE 无需任何额外基础设施 |
| BuFLO 系列 | 需要固定速率网络传输，修改网络栈 | 需要额外基础设施 | FRONT/GLUE 无需任何额外基础设施 |

### 3.3 论文的研究假设或核心直觉

**FRONT 的核心直觉**：
1. **Trace front 信息泄露假设**：WF 攻击的关键特征集中在 trace 的前几秒。证据：kNN [24] 和 kFP [7] 显式使用 trace front 进行分类。
2. **Trace-to-trace 随机性假设**：同一网页的不同 trace 如果在攻击者看来完全不同（总长度、包顺序、方向均随机），攻击者将无法学习到有意义的模式。

**GLUE 的核心直觉**：
3. **分割问题困难性假设**：当多个网页的 trace 无间隙连接时，已知 WF 攻击无法成功分类，即使经过适当训练 [10, 30]。分割决策（split decision）和分割查找（split finding）问题均未被有效解决。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 现有轻量级防御（WTF-PAD）已被 DF 攻破，重量级防御（Tamaraw）开销过大无法部署 | §1 Introduction, Table 1 |
| 痛点提炼 | 防御领域存在三难困境：安全性、零延迟、低开销无法兼得 | §2 Related Work |
| 问题转化 | 能否找到在零延迟、低开销约束下仍能抵抗最佳攻击的新防御范式？ | §4.1 FRONT Overview |
| 文献定位 | 已有工作关注混淆/规范化/混淆策略，但未系统利用 trace front 信息泄露和 -trace 分割困难性 | §2 Related Work |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| FRONT 核心假设 | 集中预算于 trace 前部比均匀分布更有效 | kNN/kFP 显式依赖 trace front [7, 24] | 实验：延迟 dummy packets 1-10 秒后 TPR 变化（Figure 4） |
| FRONT 随机性假设 | 随机化 dummy packet 数量和窗口大小可降低攻击者学习能力 | trace-to-trace 一致性帮助攻击者学习模式 | 实验：改变 beta 参数后 TPR 变化（Figure 5, 6） |
| GLUE 分割困难性假设 | -trace 分割问题（decision + finding）即使改进算法仍极难解决 | 已知攻击无法分类 -trace [10, 30] | 实验：改进 CDSB 框架后攻击性能（Figure 10, 11） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| FRONT 核心假设 | 支撑 | 延迟 10 秒后 kFP TPR 从 34% 升至 62%，DF TPR 从 59% 升至 71% | §5.4, Figure 4 |
| FRONT 随机性假设 | 支撑 | beta 从 0 增至 1 时，CUMUL/kFP TPR 显著上升 | §5.5, Figure 5-6 |
| GLUE 分割困难性假设 | 支撑 | 即使告知攻击者 l 值，l=16 时所有攻击 TPR < 5%；需要 split decision 时 precision < 1% | §7.2-7.3, Figure 10-11 |

---

## 4. 方法设计

### 4.1 方法整体流程

本文提出两个独立但互补的防御方案：

**FRONT（Front Randomized Obfuscation of Network Traffic）**：
1. 采样虚拟包数量 n_c, n_s（从离散均匀分布 U(1, N_c), U(1, N_s)）
2. 采样填充窗口大小 w_c, w_s（从均匀分布 U(W_min, W_max)）
3. 从 Rayleigh 分布 f(t; w) 采样时间戳，生成虚拟包调度时间表
4. 真实包零延迟发送，虚拟包按时间表发送

**GLUE**：
1. Front Mode：首次加载网页时执行 FRONT 防御，同时采样包间隔时间分布 I
2. Glue Mode：网页加载完成后，客户端和代理互发虚拟包模拟新网页访问，持续至 d_max 或用户发起新请求
3. Back Mode：用户实际加载新网页时，不添加虚拟包，但继续采样间隔时间
4. 循环：Glue Mode ↔ Back Mode 直到用户停留时间超过 d_max

### 4.2 详细 Pipeline

**FRONT Pipeline**：

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| 采样虚拟包数量 | 参数 N_c, N_s | n_c ← U(1, N_c), n_s ← U(1, N_s) | 每条 trace 的虚拟包预算 | 确保 trace-to-trace 随机性 |
| 采样填充窗口 | 参数 W_min, W_max | w_c ← U(W_min, W_max), w_s ← U(W_min, W_max) | 填充窗口大小 | 控制虚拟包集中区域 |
| 生成时间表 | n_c, n_s, w_c, w_s | 从 Rayleigh 分布 f(t; w) 采样 n_c + n_s 个时间戳 | 虚拟包发送时间表 | 集中虚拟包于 trace 前部 |
| 调度发送 | 真实包 + 时间表 | 真实包零延迟发送，虚拟包按时间表发送 | 防御后的 trace | 混淆 trace front 特征 |

**GLUE Pipeline**：

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Front Mode | 网页加载请求 | 执行 FRONT 防御 + 采样间隔分布 I | FRONT 防御的 trace + 分布 I | 保护第一个 trace |
| 等待 t_delta | 分布 I | t_delta ← U(I_20, I_80) | 短暂等待时间 | 模拟自然的请求间隔 |
| Glue Mode | 客户端停留中 | 客户端和代理互发虚拟包，模拟新网页加载 | 粘合 trace | 隐藏真实 trace 间隙 |
| Back Mode | 用户发起新请求 | 零虚拟包，仅采样间隔时间 | 新 trace（无额外保护） | 实际网页加载 |
| 终止条件 | 停留时间 > d_max | 返回 Front Mode | -trace 结束 | 控制开销 |

### 4.3 模型模块表格

**FRONT 参数与变量**：

| 类型 | 符号 | 含义 | 取值/分布 |
|---|---|---|---|
| 参数 | N_c | 客户端填充预算上限 | FT-1: 1700, FT-2: 2500 |
| 参数 | N_s | 代理填充预算上限 | FT-1: 1700, FT-2: 2500 |
| 参数 | W_min | 最小填充窗口 | 1s |
| 参数 | W_max | 最大填充窗口 | 14s |
| 变量 | n_c | 实际出站虚拟包数 | U(1, N_c) |
| 变量 | n_s | 实际入站虚拟包数 | U(1, N_s) |
| 变量 | w_c | 客户端填充窗口 | U(W_min, W_max) |
| 变量 | w_s | 代理填充窗口 | U(W_min, W_max) |

**GLUE 状态机**：

| 状态 | 触发条件 | 行为 | 下一状态 |
|---|---|---|---|
| Front Mode | 初始/用户访问网页 | 执行 FRONT + 采样分布 I | 等待 t_delta → Glue Mode |
| Glue Mode | t_delta 超时 | 客户端和代理互发虚拟包（模拟网页加载） | 用户点击 → Back Mode；超时 → Front Mode |
| Back Mode | 用户发起新请求 | 零虚拟包，采样间隔时间 | t_delta 超时 → Glue Mode |

### 4.4 公式、算法和机制解释

**Rayleigh 分布 PDF**：

$$
f(t; w) = \begin{cases} \frac{t}{w^2} e^{-t^2/2w^2} & t \geq 0 \\ 0 & t < 0 \end{cases}
$$

其中 w 是填充窗口大小。该分布在 t = w 处达到峰值，40% 的虚拟包集中在 [0, w] 区间内：

$$
\int_0^w \frac{t}{w^2} e^{-t^2/2w^2} dt \approx 0.40
$$

**设计含义**：Rayleigh 分布自然地将虚拟包集中于 trace 开头（前 40%），与 FRONT 的"混淆 trace front"直觉一致。分布的长尾特性确保部分虚拟包散布于 trace 中后部，增加随机性。

**FRONT 数据开销**：

$$
O(\text{FRONT}) = \frac{\bar{U}(1, N_s) + \bar{U}(1, N_c)}{|P|} \approx \frac{(N_s + N_c)/2 + 1}{|P|}
$$

均值为 (N_s + N_c)/2 + 1 个虚拟包。

**GLUE 数据开销**：

$$
O(\text{GLUE}) = \underbrace{\frac{N_s + N_c + 2}{2\ell b d_P}}_{\text{FRONT 噪声}} + \underbrace{\frac{(\ell-1) d_G}{\ell d_P}}_{\text{粘合 trace}} + \underbrace{\frac{d_L}{\ell d_P}}_{\text{尾部}}
$$

其中 l 为粘合的 trace 数量，d_P 为平均页面加载时间，d_G 为平均停留时间，d_L 为尾部平均时间，b 为包速率。

**CDSB 分割查找算法（Algorithm 1: Score Decoding）**：

```
输入：出站包位置和得分列表，邻域参数 r，分割数 n
输出：预测分割点集合 L
1: L ← {}
2: for i = 1 to n do
3:   找到得分最高的包 p，加入 L
4:   p.score ← -∞
5:   for 每个其他包 q do
6:     if |q.loc - p.loc| < r then
7:       q.score ← -∞
8:     end if
9:   end for
10: end for
11: return L
```

**机制**：每轮选择得分最高的包作为分割点，然后将其邻域内的包得分置为负无穷，避免选择相邻包作为多个分割点。邻域参数 r = 40。

---

## 5. 关键发现与证据

### 5.1 主要实验结果

**FRONT 防御效果（DS-19 数据集，open-world，r=10）**：

| 防御 | 数据开销 | kNN F1 | CUMUL F1 | kFP F1 | DF F1 |
|---|---:|---:|---:|---:|---:|
| 无防御 | 0% | 0.86 | 0.76 | 0.93 | 0.94 |
| Tamaraw | 163% | 0.028 | 0.052 | 0.038 | 0.11 |
| WTF-PAD | 33% | 0.16 | 0.28 | 0.61 | 0.70 |
| FT-1 (FRONT) | 33% | 0.048 | 0.18 | 0.54 | 0.47 |
| FT-2 (FRONT) | 49% | 0.016 | 0.13 | 0.46 | 0.40 |

**GLUE 防御效果（l=8, 无 split decision, FRONT 噪声）**：

| 攻击 | TPR | Precision |
|---|---:|---:|
| kNN | ~8% | ~4% |
| CUMUL | ~15% | ~3% |
| kFP | ~8% | ~4% |
| DF | ~25% | ~2% |

**GLUE 防御效果（l=16, 有 split decision）**：

| 攻击 | TPR | Precision |
|---|---:|---:|
| kNN | ~0.1% | ~0.1% |
| CUMUL | ~1% | ~0.05% |
| kFP | ~0.1% | ~0.05% |
| DF | ~0.5% | ~0.02% |

### 5.2 关键发现

1. **FRONT 在同等开销下全面优于 WTF-PAD**：FT-1（33% 开销）vs WTF-PAD（33% 开销），FRONT 对所有四种攻击的 F1 均更低，尤其对 DF 的 F1 从 0.70 降至 0.47（降低 33%）。

2. **Trace front 是 WF 攻击的关键信息源**：延迟 dummy packets 10 秒后，kFP TPR 从 34% 升至 62%（近乎翻倍），DF TPR 从 59% 升至 71%。这证实了 FRONT 的核心直觉。

3. **Trace-to-trace 随机性是 FRONT 成功的关键**：当 beta 从 0（最大随机化）增至 1（固定数量）时，CUMUL TPR 从 ~60% 升至 ~90%，kFP TPR 从 ~35% 升至 ~55%。随机化同时降低了数据开销（beta=1 时开销翻倍）。

4. **GLUE 的防御效果随 l 增大急剧增强**：l=2 时 DF TPR 仍有 54%，l=16 时所有攻击 TPR < 5%（无 split decision）或 < 1%（有 split decision）。

5. **FRONT 的信息泄露分析**：WeFDE 分析显示 FRONT 下无特征泄露超过 2.3 bits（FT-1）或 2.0 bits（FT-2），而无防御时最高 3.6 bits，WTF-PAD 最高 3.5 bits。

6. **FRONT 对大网页防御效果较弱**：kFP 在最大四分位网页组（G4）上 recall 为 54%，远高于其他三组（24%-35%），说明大网页的特征更难被混淆。

---

## 6. 质量与信心评估

### 6.1 当前状态

| 维度 | 状态 | 备注 |
|---|---|---|
| 实验完整性 | 完整 | 两个数据集、四种攻击、三种防御对比、信息泄露分析、消融实验 |
| 写作完整性 | 完整 | 结构清晰，动机明确，实验充分 |
| 方法创新性 | 高 | FRONT 的 trace front 混淆和 GLUE 的 -trace 粘合均为新颖思路 |
| 实验说服力 | 强 | 开放世界场景、多种攻击、信息泄露分析（WeFDE）多角度验证 |
| 与已有工作的区分度 | 明确 | Table 1 清晰对比所有防御的开销和安全性 |

### 6.2 需要改进的地方

1. **GLUE 的实际部署可行性**：需要 Tor 目录服务器维护粘合 trace 数据库，增加了基础设施依赖（虽然作者论证了开销可控）。
2. **FRONT 对大网页的防御不足**：G4 组（最大网页）的 recall 仍达 54%，说明当前参数设置对大网页不够充分。
3. **GLUE 的开销依赖用户行为**：d_G 和 d_L 的不同设置导致开销从 3% 到 53% 不等，实际部署中难以预测。

### 6.3 是否可以考虑提交/晋升？

- [x] 方法论完整
- [x] 实验覆盖足够
- [x] 写作达到可读标准
- [x] 与已有工作区分度明确
- [x] 局限性已诚实讨论

---

## 7. [深度分析] 方法设计详解

### 7.1 方法整体流程

FRONT 和 GLUE 是两个独立但可组合的防御方案，共享"零延迟、轻量级"的设计哲学：

**FRONT 的设计逻辑链**：
1. 观察：WF 攻击依赖 trace front → 2. 策略：集中预算混淆 trace front → 3. 实现：Rayleigh 分布自然集中于前部 → 4. 强化：随机化预算和窗口实现 trace-to-trace 差异 → 5. 效果：攻击者无法学习稳定的网页模式

**GLUE 的设计逻辑链**：
1. 观察：WF 攻击假设 singleton trace → 2. 策略：将多个 trace 粘合为 -trace → 3. 挑战：攻击者需解决 split decision + split finding → 4. 验证：改进 CDSB 框架后问题仍极难 → 5. 效果：即使最优攻击也无法有效分割

### 7.2 详细 Pipeline

**FRONT 三步流程**：

| 步骤 | 操作 | 数学描述 | 设计意图 |
|---|---|---|---|
| Step 1: 采样虚拟包数量 | 客户端和代理分别采样 | n_c ← U(1, N_c), n_s ← U(1, N_s) | 每条 trace 的虚拟包数量不同，阻止攻击者学习固定模式 |
| Step 2: 采样填充窗口 | 客户端和代理分别采样窗口大小 | w_c ← U(W_min, W_max), w_s ← U(W_min, W_max) | 窗口大小随机化，虚拟包集中区域随 trace 变化 |
| Step 3: 生成时间表并发送 | 从 Rayleigh 分布采样时间戳 | t_i ~ Rayleigh(w); 真实包零延迟 | 虚拟包集中于 trace 前部（40% 在 [0,w]），混淆关键特征 |

**GLUE 状态机详细流程**：

| 状态 | 输入 | 操作 | 输出 | 转换条件 |
|---|---|---|---|---|
| Front Mode | 用户访问网页 | (1) 执行 FRONT 防御 (2) 采样间隔分布 I (3) t_delta ← U(I_20, I_80) | FRONT 保护的 trace + 分布 I | 网页加载完成 → 等待 t_delta → Glue Mode |
| Glue Mode | t_delta 超时 | 客户端和代理从粘合 trace 数据库中选择一条，按其时间表互发虚拟包 | 粘合 trace（看起来像新网页加载） | 用户点击 → Back Mode；超时 d_max → Front Mode |
| Back Mode | 用户发起新请求 | (1) 零虚拟包 (2) 采样间隔时间 | 真实 trace（无额外保护） | 网页加载完成 → 等待 t_delta → Glue Mode |

### 7.3 模型结构或系统模块

**FRONT 系统模块**：

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 随机采样器 | 采样虚拟包数量和窗口大小 | 参数 N_c, N_s, W_min, W_max | n_c, n_s, w_c, w_s | 输出传递给时间表生成器 |
| 时间表生成器 | 从 Rayleigh 分布生成虚拟包时间戳 | n_c, n_s, w_c, w_s | 虚拟包发送时间表 | 输出传递给包调度器 |
| 包调度器 | 按时间表发送虚拟包，真实包零延迟 | 真实包流 + 时间表 | 防御后的包流 | 接收来自时间表生成器的指令 |

**GLUE 系统模块**：

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 状态控制器 | 管理 Front/Glue/Back 模式切换 | 用户行为信号 + 定时器 | 状态指令 | 控制其他所有模块 |
| FRONT 防御器 | 在 Front Mode 下执行 FRONT 防御 | 网页加载请求 | FRONT 保护的 trace | 仅在 Front Mode 激活 |
| 间隔采样器 | 采样包间隔时间分布 | 入站/出站包时间戳 | 分布 I + t_delta | 输出传递给状态控制器和粘合器 |
| 粘合器 | 在 Glue Mode 下生成粘合 trace | 粘合 trace 数据库 + 状态指令 | 虚拟包流 | 仅在 Glue Mode 激活 |

### 7.4 公式、算法和机制解释

**Rayleigh 分布的性质与 FRONT 的关系**：

Rayleigh 分布是二维正态分布的径向分量，其 PDF 在 t=0 处为 0，在 t=w 处达到峰值，之后以指数速率衰减。这意味着：
- 虚拟包不会在 trace 最开始（t=0）就密集出现，避免产生异常的包突发
- 虚拟包集中在 [0, w] 区间（约 40%），与 trace front 的时间范围匹配
- 长尾特性确保部分虚拟包散布于 trace 中后部，增加整体随机性

**为什么选择 Rayleigh 而非其他分布**：
- 均匀分布：虚拟包均匀散布，无法集中于 trace front
- 指数分布：峰值在 t=0，会导致 trace 最开始的包突发
- 正态分布：需要截断处理负值，且峰值位置不自然

**GLUE 的 t_delta 采样策略**：

$$
t_\Delta \in U(I_{20}, I_{80})
$$

其中 I_20 和 I_80 是入站-出站包间隔时间分布的 20 和 80 百分位数。选择这个范围的原因：
- 如果 t_delta 太小（< I_20），粘合 trace 的起始会显得不自然
- 如果 t_delta 太大（> I_80），会产生明显的间隙，被攻击者利用
- 在 [I_20, I_80] 范围内，t_delta 模拟了自然的"客户端收到数据后发送请求"的时间间隔

---

## 8. [深度分析] 实验详细分析

### 8.1 实验设计和设置

**数据集**：
- DS-19（2019年2-4月采集）：Alexa top 100 网站各 100 次 + 10000 非监控网页，使用 Tor Browser 8.5a7
- DS-14（Wang 2014 数据集）：9000 监控 + 9000 非监控网页，平均包数 2163（DS-19 为 4444）

**攻击者**：kNN [24], CUMUL [16], kFP [7], DF [20]——均为当时最先进的 WF 攻击

**评估场景**：开放世界（open-world），r=10（每访问 1 个监控网页对应 10 个非监控网页），10-fold 交叉验证

**评估指标**：TPR（真正率）、Precision（精度）、F1（F1 分数）

**防御参数设置**：

| 防御 | 参数 | 数据开销 | 延迟开销 |
|---|---|---:|---:|
| 无防御 | - | 0% | 0% |
| Tamaraw | rho_out=0.04, rho_in=0.012, L=50 | 163% | 78% |
| WTF-PAD | Normal rcv | 33% | 0% |
| FT-1 (FRONT) | N_s=N_c=1700, W_min=1s, W_max=14s | 33% | 0% |
| FT-2 (FRONT) | N_s=N_c=2500, W_min=1s, W_max=14s | 49% | 0% |

### 8.2 数据集详情

| 数据集 | 采集时间 | 监控网页数 | 非监控网页数 | 平均包数 | Tor 版本 |
|---|---|---:|---:|---:|---|
| DS-19 | 2019年2-4月 | 100 x 100 | 10000 | 4444 | Tor 0.4.0.1-alpha |
| DS-14 | 2014年 | 9000 | 9000 | 2163 | - |

**网页大小分布**（DS-19）：
- G1（最小四分位）：最多 2039 包
- G2：最多 4368 包
- G3：最多 6611 包
- G4（最大四分位）：最多 28199 包

### 8.3 Baseline 选择理由

| Baseline | 选择理由 | 类别 |
|---|---|---|
| WTF-PAD | 唯一共享"零延迟、轻量级"特性的现有防御，是 FRONT 的直接竞争对手 | Obfuscation |
| Tamaraw | 重量级防御的代表，提供安全性上限参考 | Regularization |
| kNN [24] | 设计用于攻破防御的攻击，自动降低无效特征权重 | WF Attack |
| CUMUL [16] | 高效的 SVM 攻击，计算时间优秀 | WF Attack |
| kFP [7] | 高精度的随机森林+kNN 攻击 | WF Attack |
| DF [20] | 深度学习攻击，首个攻破 WTF-PAD 的方法 | WF Attack |

### 8.4 消融实验

**FRONT 消融实验**：

| 消融维度 | 实验设置 | 关键发现 |
|---|---|---|
| Trace front 重要性 | 延迟 dummy packets 0-10 秒 | 延迟 10 秒后 kFP TPR 从 34% 升至 62%，证实 trace front 是关键信息源 |
| 虚拟包数量随机性 | beta 从 0 到 1 控制随机化程度 | beta=0.8 时 CUMUL TPR 从 ~60% 升至 ~65%，beta=1 时升至 ~65% |
| 填充窗口随机性 | beta 从 0 到 1 控制窗口大小范围 | beta=1 时 CUMUL TPR 从 ~60% 升至 ~90%，DF TPR 从 ~25% 升至 ~60% |
| 数据开销影响 | N_s + N_c 从 0 到 7200 | 25% 开销时 kFP TPR 已低于 50%，70% 开销时 F1 降至 38% |
| 填充预算比例 | alpha = N_c/(N_c+N_s) 从 0 到 1 | 最优 alpha 约为 0.25-0.5，即 N_s 应等于或略小于 N_c |
| 填充窗口大小 | W_max 从 14s 到 36s | W_max 过大会导致虚拟包被丢弃（长尾效应），对小网页尤其不利 |

**GLUE 消融实验**：

| 消融维度 | 实验设置 | 关键发现 |
|---|---|---|
| FRONT 噪声贡献 | 有/无 FRONT 噪声对比 | 无 FRONT 噪声时第一个 trace 的 TPR 为 40%-80%，有 FRONT 噪声时降至 20%-60% |
| l 值影响 | l 从 2 到 16 | l=2 时 DF TPR=54%，l=16 时所有攻击 TPR < 5% |
| Split decision 影响 | 有/无 split decision | 有 split decision 时攻击性能进一步下降，l=16 时 precision < 1% |

### 8.5 Case Study / 可视化分析

**信息泄露分析（WeFDE）**：
- 使用 WeFDE 工具分析 3043 个特征的信息泄露
- FRONT 在大多数特征类别上泄露更少，尤其在 Pkt. Count、Time、NGRAM、Pkt. Distribution 和 CUMUL 类别
- WTF-PAD 在 Interval-I、II、III 类别上优于 FRONT（因为 WTF-PAD 基于时间混淆）

**FRONT vs WTF-PAD 预算分配对比**：
- WTF-PAD：24% 预算在前 1/4，49% 在前 1/2（均匀分布）
- FRONT：40% 预算在前 1/4，69% 在前 1/2（集中于 trace front）

**Trace-to-trace 随机性对比**：
- FRONT：虚拟包数量的变异系数中位数 42%
- WTF-PAD：虚拟包数量的变异系数中位数 36%

### 8.6 局限性与失败案例

| 局限性 | 具体表现 | 影响 |
|---|---|---|
| FRONT 对大网页防御不足 | G4 组（最大网页）kFP recall 54%，远高于其他组 | 大网页的特征更丰富，需要更多预算 |
| GLUE 开销依赖用户行为 | d_G=2.5s 时开销 3%-13%，d_G=10s 时开销 35%-53% | 实际部署中难以预测和控制开销 |
| GLUE 需要额外基础设施 | 需要 Tor 目录服务器维护粘合 trace 数据库 | 增加了部署复杂性 |
| FRONT 对网络条件敏感 | 作者承认在差网络条件下 FRONT 可能表现不佳 | 未实验验证 |
| GLUE 的粘合 trace 可被识别 | 作者允许攻击者知道整个数据库，但未证明不可能识别粘合 trace | 开放问题 |

---

## 9. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| WF 攻击依赖 trace front | kNN [24] 和 kFP [7] 显式使用 trace front 特征 | §4.1 |
| FRONT 在同等开销下优于 WTF-PAD | FT-1 F1 均低于 WTF-PAD（Table 4） | §5.2 |
| Trace front 是关键信息源 | 延迟 10 秒后 kFP TPR 从 34% 升至 62% | §5.4, Figure 4 |
| Trace-to-trace 随机性重要 | beta 从 0 到 1 时 CUMUL TPR 从 ~60% 升至 ~90% | §5.5, Figure 5-6 |
| FRONT 信息泄露更少 | WeFDE 分析：FRONT 最高泄露 2.3 bits，无防御 3.6 bits | §5.3, Figure 3 |
| GLUE 在 l=16 时使所有攻击失效 | TPR < 5%（无 split decision），precision < 1%（有 split decision） | §7.2-7.3, Figure 10-11 |
| FRONT 噪声对 GLUE 第一个 trace 必要 | 无 FRONT 噪声时第一个 trace TPR 40%-80%，有 FRONT 噪声时 20%-60% | §7.6, Figure 13 |
| GLUE 开销随 l 增大而降低 | FRONT 噪声和尾部开销被 l 个 trace 分摊 | §7.5, Equation 1 |
| 大网页更难防御 | G4 组 kFP recall 54%，G1-G3 组 24%-35% | §5.2 |
| DS-19 上攻击性能普遍高于 DS-14 | 更大的网页（DS-19 平均 4444 包 vs DS-14 平均 2163 包）更容易识别 | §5.2 |

---

## 10. 原始资料链接

- PDF：`00-inbox/PDFs/2020-USENIX-Zero-delay_Lightweight_Defenses_against_Website_Fingerprinting.pdf`
- MinerU Markdown：`02-parsed-markdown/2020-USENIX-Zero-delay_Lightweight_Defenses_against_Website_Fingerprinting.md`
- 代码仓库：https://github.com/websitefingerprinting/WebsiteFingerprinting/
- 补充材料：Appendix A（FRONT 参数设置）、Appendix B（Split Decision 特征）、Appendix C（Score Decoding 算法）、Appendix D（信息泄露详细结果）、Appendix E（无防御 -trace 评估）

---

## 11. 与领域已有工作的关系

### 11.1 攻击-防御演化链

| 攻击 | 年份 | 特点 | 被谁攻破/防御 |
|---|---|---|---|
| kNN [24] | 2014 | 自动学习特征权重，设计用于攻破防御 | FRONT 显著降低其性能 |
| CUMUL [16] | 2016 | SVM + cumulative representation | FRONT/GLUE 均有效 |
| kFP [7] | 2016 | 随机森林 + kNN，高精度 | FRONT 降低其 F1 至 0.46 |
| DF [20] | 2018 | CNN，首个攻破 WTF-PAD | FRONT 将其 F1 从 0.70 降至 0.47 |

### 11.2 防御方案对比

| 防御 | 年份 | 类别 | 延迟 | 数据开销 | 被攻破？ | 本文关系 |
|---|---|---|---|---|---|---|
| WTF-PAD | 2016 | Obfuscation | 0% | 33% | 是（DF） | FRONT 直接超越 |
| Tamaraw | 2014 | Regularization | 78% | 163% | 否 | 安全性上限参考 |
| Walkie-Talkie | 2017 | Confusion | Medium | Low | 否 | 需额外基础设施 |
| FRONT | 2020 | Obfuscation | 0% | 33%-49% | 否 | 本文贡献 |
| GLUE | 2020 | 新类别 | 0% | 22%-53% | 否 | 本文贡献 |

### 11.3 后续工作影响

本文提出的 FRONT 和 GLUE 为后续 WF 防御研究提供了重要基准：
- FRONT 的"trace front 混淆"思路影响了后续防御设计
- GLUE 的"-trace 粘合"思路开创了新的防御范式
- CDSB 分割框架为后续分割攻击研究提供了改进基线

---

## 12. 开放问题与后续计划

### 12.1 本文遗留的问题

1. **GLUE 粘合 trace 的可识别性**：作者允许攻击者知道整个数据库，但未证明不可能识别粘合 trace。"we leave the question open as future work"（§8）
2. **FRONT 对差网络条件的适应性**："making FRONT automatically self-adjusting to poor network conditions is a potential future direction"（§8）
3. **GLUE 的"实时生成"方案**：客户端能否"on the fly"生成看起来像真实网页流量的粘合 trace，以消除数据库依赖？
4. **理论安全性保证**：本文未设计能"guarantee future success"的防御，split decision 和 finding 的困难性未被理论证明。

### 12.2 下一步研究方向

1. 自适应 FRONT：根据网络条件和网页大小动态调整参数
2. GLUE 的实时粘合 trace 生成：消除对目录服务器的依赖
3. FRONT + GLUE 的联合优化：探索两种防御的最优组合策略
4. Split 问题的理论分析：证明 split decision 和 finding 的计算复杂度

### 12.3 与研究主线的关系

本文在 [[website-fingerprinting-defense]] 领域具有重要地位：
- 是零延迟轻量级防御的代表作，与 WTF-PAD 共享设计哲学但性能更优
- GLUE 开创了利用 -trace 分割困难性的新防御范式
- 为后续防御方案（如 TrafficSliver、Palette）提供了重要的对比基线

---

## 13. 关联图谱

### 13.1 Wikilinks

- [[website-fingerprinting]]：本文研究的核心问题
- [[website-fingerprinting-defense]]：本文提出的 FRONT 和 GLUE 均属此类
- [[encrypted-traffic-analysis]]：WF 攻击是加密流量分析的特例
- [[survey-website-fingerprinting]]：本文 Table 1 系统对比了所有 WF 防御
- [[tunnel-detection]]：WF 攻击针对 Tor 隧道流量

### 13.2 相关论文

| 论文 | 关系 | 说明 |
|---|---|---|
| Deep Fingerprinting (CCS 2018) | 攻击者 | DF 是首个攻破 WTF-PAD 的攻击，本文 FRONT 专门针对 DF |
| WTF-PAD (ESORICS 2016) | 直接竞争 | FRONT 在同等开销下全面优于 WTF-PAD |
| Tamaraw (CCS 2014) | 安全性参考 | 重量级防御的代表，提供安全性上限 |
| kNN (USENIX 2014) | 攻击者 | 依赖 trace front 的攻击，FRONT 特别有效 |
| kFP (USENIX 2016) | 攻击者 | 最精确的攻击，FRONT 将其 F1 降至 0.46 |
| TrafficSliver (CCS 2020) | 同期工作 | 同为 2020 年 WF 防御，采用流量分割策略 |
| Palette (S&P 2024) | 后续工作 | 基于流量聚类匿名化的防御，引用本文 FRONT |

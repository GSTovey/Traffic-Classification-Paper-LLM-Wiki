---
type: paper
title_original: "Time-Hopping Covert Communication With Random Slots and Dispersed Energy"
title_cn: "随机时隙与能量分散的时间跳变隐蔽通信"
authors: [Kun Lu, Zhe Song, Shuai Wang, Tingting Li, Gaofeng Pan, Heng Liu, George Karagiannidis]
year: 2026
venue: "IEEE TIFS 2026"
doi: "unknown"
url: "unknown"
pdf: "00-inbox/PDFs/2026-TIFS-Time-Hopping_Covert_Communication_With_Random_Slots_and_Dispersed_Energy.pdf"
mineru_md: "02-parsed-markdown/2026-TIFS-Time-Hopping_Covert_Communication_With_Random_Slots_and_Dispersed_Energy.md"
status: processed
reading_level: L2
research_area: []
task: []
method: []
dataset: []
code: unknown
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

# Time-Hopping Covert Communication With Random Slots and Dispersed Energy

> 说明：本篇属**物理层隐蔽通信（covert communication / LPD）**方向，与 kb_reference C 节白名单（加密流量分析/网站指纹/恶意流量检测等）无交集。为避免编造 slug，`research_area`/`task`/`method`/`dataset` 四个 frontmatter 字段留空，§9 仅给出适用范围说明。DOI 在解析稿全文中未出现（已逐段检索 "10.1109"、"DOI"、"doi.org"），故填 unknown。

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Time-Hopping Covert Communication With Random Slots and Dispersed Energy |
| 中文标题 | 随机时隙与能量分散的时间跳变隐蔽通信 |
| 作者 | Kun Lu, Zhe Song, Shuai Wang, Tingting Li, Gaofeng Pan, Heng Liu, George Karagiannidis |
| 年份 | 2026 |
| 会议/期刊 | IEEE TIFS（IEEE Transactions on Information Forensics and Security） |
| 研究方向 | 物理层隐蔽通信（covert communication），不在本库白名单范围 |
| 任务类型 | 隐蔽性建模与分析（理论推导 + 行为级仿真） |
| 方法关键词 | random time-hopping、energy dispersion、KL divergence、likelihood ratio test、finite blocklength、covert throughput |
| 数据集 | 无（纯数值仿真，无公开数据集） |
| 是否开源 | 解析稿未给出代码链接 → unknown |
| PDF | 00-inbox/PDFs/2026-TIFS-Time-Hopping_Covert_Communication_With_Random_Slots_and_Dispersed_Energy.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-TIFS-Time-Hopping_Covert_Communication_With_Random_Slots_and_Dispersed_Energy.md |

> ⚠️ MinerU 解析问题：全文 fi 连字丢失（"dificult"/"efort" 等）；部分公式编号标签被污染（如出现 `\tag{（}\tag{29}` 一类的半角/全角混排）；Fig. 3 的行为仿真伪代码在解析稿中只剩图注，算法步骤以正文 (1)–(4) 列表形式保留。

---

## 1. 一句话总结

> ED-RTH：让 Alice 在 T 个时隙里随机挑 K 个、把原本单时隙的能量均摊到 K 个时隙重复发送 n 符号消息，从信息论上证明 K 增大可单调提升 Willie 的检测错误概率下界（KL 散度给出），且在固定总功率下隐蔽吞吐与 K 无关、在固定隐蔽约束下随 K 提升。

---

## 2. 摘要翻译

### 2.1 摘要原文

> The growth of communication technologies has led to a corresponding increase in the need for information security. The use of covert communication techniques has the potential to significantly reduce the likelihood of the transmitted signal being intercepted by unintended receivers, thereby significantly increasing the security of the information. In this paper, we propose an energy-dispersed random time-hopping (ED-RTH) covert communication scheme. Building on existing time uncertainty schemes, this scheme further enhances time uncertainty through random time-hopping, while dispersing signal energy to achieve stronger covertness. We present a model for analyzing the covertness of the ED-RTH scheme. Given the complexity of the likelihood ratio distribution, the Kullback-Leibler (KL) divergence is used to analyze the lower bound of Willie's detection error probability. Through constructing behavioral-level simulations for validation, we investigated the impact of the number of dispersed time slots K on both Willie's detection error probability and the system's covert throughput. Finally we compared the proposed ED-RTH scheme with existing time uncertainty scheme, and the results demonstrate that the ED-RTH scheme achieves significantly enhanced covertness.

### 2.2 摘要中文翻译

通信技术的发展带来了对信息安全需求的同步增长。隐蔽通信技术能够显著降低所发送信号被非预期接收者截获的可能性，从而大幅提升信息安全性。本文提出**能量分散的随机时间跳变（ED-RTH）隐蔽通信方案**：在既有"时间不确定性"方案的基础上，通过随机时间跳变进一步增强时间不确定性，同时分散信号能量以获得更强的隐蔽性。作者给出了 ED-RTH 方案的隐蔽性分析模型；由于似然比分布过于复杂，改用 KL 散度（Kullback-Leibler divergence）分析 Willie 检测错误概率的下界。通过构建行为级仿真进行验证，研究了分散时隙数 K 对 Willie 检测错误概率与系统隐蔽吞吐的双重影响。最后将所提 ED-RTH 方案与既有时间不确定性方案对比，结果表明 ED-RTH 方案实现了显著增强的隐蔽性。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

隐蔽通信（covert communication）的目标不是"内容不被破解"，而是"通信行为本身不被发现"。经典起点是 Wyner 1975 的囚徒问题（Prisoner's Problem）与 Bash 等 2013 年从信息论角度提出的隐蔽通信容量平方根律（SRL：码长 n 的码块只能隐蔽传输 O(√n) 比特）。作者所在的无线通信社区随后开始利用系统固有不确定性（噪声不确定性、信道不确定性、传输时间不确定性）来降低 Willie 的检测能力。本文聚焦**时间不确定性**这一支，认为已有工作只考虑了"单时隙选择"或"每符号功率固定"的设定，**遗漏了"把能量分散到多个时隙"这一自由度**（§II-B）。

### 3.2 现有方法的痛点和不足

- 传统确定时间方案（certain time，即 T=1、K=1）：能量集中在单时隙，Willie 很容易把接收信号与纯噪声区分开（§IV-C）。
- 单时隙随机选择方案（single-slot selection，T>1、K=1）：增加了时间不确定性，但一旦选中某时隙，该时隙的功率仍然很高，可区分度依然明显。
- 已有分析手段受限：ED-RTH 的似然比分布涉及 $C_T^K$ 项求和，难以直接解析求 Willie 的检测错误概率，需要新的分析工具（→ 引入 KL 散度下界）。

### 3.3 论文的研究假设或核心直觉

核心直觉：**在总能量恒定的前提下，把能量摊薄到 K 个随机时隙，可以同时获得"时间不确定性"和"功率不确定性"双重收益**；而 Willie 虽然知道 Alice 的发射功率与"随机均匀选 K 个时隙"这一策略，却不知道具体是哪 K 个时隙（共 $C_T^K$ 种等概率组合），因此其最优似然比检验（LRT）的性能会随 K 增大而退化。作者还假设 $P_a^* < \sigma_w^2/2$ 以维持期望的检测错误概率水平，并令 Alice 的发射先验概率 ρ = 0.5 以最大化 Willie 的检测错误概率。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 单时隙或固定功率的时间不确定性方案，其可获得的隐蔽性提升有限 | §I（对 Bash et al. [28] 等工作的综述）、§II-B |
| 痛点提炼 | Willie 只要观测各时隙功率就能区分"发送/未发送"；单时隙方案下信号与噪声差异明显 | §IV-C 对 Fig. 10 的解释 |
| 问题转化 | 把"如何进一步增强时间不确定性"转化为"分散时隙数 K 如何影响 Willie 检测错误概率下界与隐蔽吞吐"的可分析问题 | §I 贡献陈述、§III |
| 文献定位 | 时间不确定性方向已有工作，但"多时隙能量分散"这一自由度未被分析，属被忽视的空白 | §II-B "failed to consider the possibility of dispersing energy across multiple time slots" |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 固定总功率 P 与总时隙数 T 下，增大 K 会降低 KL 散度 D(P0‖P1)，即提升隐蔽性 | §III-A、式(25)(26) | 理论推导 + 行为级仿真（Fig. 4/Fig. 5） |
| 辅助假设 1 | 当 K = T 时，LRT 退化为能量检测，两者检测错误概率收敛一致 | §III-A 式(16)(17) | 仿真（Fig. 7） |
| 辅助假设 2 | 固定 Pa* 时隐蔽吞吐与 K 无关；固定隐蔽约束时吞吐随 K 提升 | §III-B 式(33) | 仿真（Fig. 9(a)） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 增大 K 提升隐蔽性 | 支撑 | KL 散度随 K 单调下降；ξ 随 K 单调上升并趋于饱和 | §IV-B, Fig. 4/Fig. 5 |
| K=T 时 LRT ≡ 能量检测 | 支撑 | 两条曲线在 K=T 处完全收敛 | §IV-B, Fig. 7 |
| 吞吐与 K 的关系 | 支撑 | η 在固定 Pa* 下与 K 无关；固定 ε 下随 K 上升 | §IV-B, Fig. 9(a) |

---

## 4. 方法设计

### 4.1 方法整体流程

三节点模型（Alice→Bob，Willie 监听），AWGN 信道。Alice 把时间轴划分为若干个长度 T 时隙的窗口，每个时隙含 n 个符号周期；以先验概率 ρ=0.5 决定是否发送；发送时随机选 K 个时隙（$C_T^K$ 种等概率组合），把 n 符号消息在 K 个时隙上重复，原单时隙能量在 K 个时隙间均分。Willie 在 nT 个信道使用上做二元假设检验（H0 无发送 / H1 有发送），可用最优 LRT 或次优能量检测。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 生成信号 | 先验 ρ=1/2 | 以 1/2 概率全零；以 1/2 概率从 T 个时隙随机选 K 个，填入平均功率 Pa 的 nK 个符号 | 长度 nT 的发送向量 | 引入时间+功率双重不确定性 |
| Step 2 过信道 | 发送向量 | 叠加 Willie 端 Gaussian 白噪声 N(0, σw²) | Willie 观测向量 y_w | 模拟监听信道 |
| Step 3 Willie 检测 | y_w | 计算似然比并与最优阈值 τLRT 比较；或做能量检测并与 τED 比较 | 判决 D0/D1 | 得到虚警概率 α 与漏检概率 β |
| Step 4 重复统计 | 多次重复 | 与真实发送状态比对，统计 α、β | 检测错误概率 ξ | 隐蔽性度量 |
| Step 5 吞吐分析 | Bob 端接收 | K 时隙相干合并后按有限码长公式解码 | 隐蔽吞吐 η | 有效性度量 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Alice 发射端 | 随机时隙选择 + 能量均分 + 消息重复 | 消息比特、参数 T/K/n | 发送信号 x[i] | 决定 K、Pa = Pa*/K |
| Bob 接收端 | K 时隙相干合并后解码 | 接收信号 | 解码结果与误码率 δ | 决定吞吐 η |
| Willie 检测端（最优） | 最优似然比检验 LRT | y_w、已知的 Pa 与选择策略 | 判决与 ξ | 复杂度高，需遍历 C_T^K 项 |
| Willie 检测端（次优） | 能量检测 | 全部 T 时隙总能量 | 判决与 ξ | 与 K 无关；K=T 时与 LRT 等价 |
| KL 散度分析模块 | 以 KL 散度给出 ξ 的下界 | 分布 P0、P1 | ξ_LB(K) | 为系统设计提供更严格的约束 |

### 4.4 公式、算法和机制解释

- **发送功率关系**：$P_a = P_a^*/K$，$P = nP_a^* = nKP_a$；其中 $P_a^*$ 为 K=1 时的每符号平均功率，假设 $P_a^* < \sigma_w^2/2$（§II-B）。
- **LRT 统计量**（式 15）：$\Lambda(y_w) = \frac{1}{C_T^K}(\frac{\sigma_w^2}{\sigma_w^2+P_a})^{nK/2}\sum_{j=1}^{C_T^K} I_j$，其中 $I_j$ 是第 j 种时隙组合下的能量指数项。K=T 时（式 16–17）LRT 化简为"平均能量与阈值比较"，与能量检测等价。
- **KL 散度近似**（式 25，附录 B 在 $T\to\infty$ 下推导）：
  $\mathcal{D}(K) \approx \frac{n\gamma_w^{*2}}{4T}\exp\left(-\frac{n\gamma_w^*}{2}(1-\frac{1}{K})\right)$，其中 $\gamma_w^* = P/(n\sigma_w^2) = P_a^*/\sigma_w^2$。
- **检测错误概率下界**（式 26）：$\xi_{LB}(K) = 1-\sqrt{\mathcal{D}(K)/2} \approx 1 - A\exp(-B(1-1/K))$，$A=\sqrt{n\gamma_w^{*2}/8T}$，$B=n\gamma_w^*/4$。随 K 单调递增但增幅按 $1/K$ 衰减（呈 $1/K^2$ 的一阶增量量级），因此 K 大到一定程度后收益边际化。
- **隐蔽吞吐**（式 31–33）：$\eta = N R (1-\delta)$，解码错误概率 $\delta$ 由有限码长 Q 函数给出（$\gamma_b = P_a/\sigma_b^2$）。相干合并后 $\gamma_{b-c} = P_aK^2/(\sigma_b^2K) = P_a^*/\sigma_b^2$，故**固定 Pa* 时 η 与 K 无关**；但由于 K 增大提升了隐蔽性、从而放宽了功率约束，**在固定隐蔽约束 ε 下 η 随 K 增大**。
- **K 的代价**：K 增大降低每符号 SNR，需要 Bob 做跨时隙相干合并（论文假设完美合并，实际存在同步误差导致的合并 SNR 损失），对接收机复杂度提出更高要求（§III-B/§IV-B）。
- **衰落信道讨论**（§III-C，定性）：衰落引入信道不确定性，Willie 因缺乏瞬时 CSI 只能用次优能量检测，隐蔽性反而增强；若跳变间隔大于信道相干时间，能量分散还能缓解深衰落影响。

### 4.5 方法优势

- 在两个自由度上同时施压：时间不确定性（选哪 K 个时隙）+ 功率不确定性（每符号功率降为 Pa*/K）。
- 给出了闭式的隐蔽性下界表达式（式 25/26），可直接用于系统参数设计；相比 LRT 数值解，KL 下界更严格（Fig. 6 显示同样隐蔽约束下对功率的限制更强）。
- 分析结论对工程选参有直接指导：K 的收益饱和点、编码率与隐蔽约束的匹配关系（隐蔽约束越严，最优编码率越低）。

### 4.6 方法不足

- 假设 Bob 能**完美相干合并** K 个时隙，忽略了同步误差带来的合并损失与接收机复杂度（作者承认这是"可达上界"式的假设）。
- 衰落信道只给定性讨论，没有闭式结果或仿真验证（§III-C）。
- 隐蔽吞吐分析基于有限码长近似，且未考虑实际信道编码方案。
- 全部结果来自数值/行为级仿真，无实测或硬件验证。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 维度 | 传统确定时间（T=1,K=1） | 单时隙选择（T>1,K=1） | RSS 方案 | ED-RTH（本文） |
|---|---|---|---|---|
| 时间不确定性 | 无 | 有（选哪个时隙） | 有（随机时隙） | 有（随机选 K 个） |
| 功率不确定性 | 无 | 无 | 无 | 有（能量均分到 K 时隙） |
| 每符号功率 | Pa* | Pa* | — | Pa*/K |
| 接收机复杂度 | 低 | 低 | 中 | 高（需 K 时隙相干合并） |

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 能量分散随机时间跳变机制 | K 个随机时隙 + 能量均分（式 15） | 高 | 是（任何时隙化传输体制） |
| KL 散度下界分析框架 | 式 (25)(26)，闭式给出 ξ 下界及 A、B 系数 | 高 | 是（可复用于其他隐蔽方案分析） |
| 隐蔽吞吐—K—编码率三者关系 | 式 (33) + Fig. 9 的编码率选择结论 | 中 | 是 |
| 衰落信道定性推广 | §III-C 的两点论证 | 低 | — |

### 5.3 适用场景

适用于**无线场景下"通信行为本身不可被发现"**的需求：军事通信、需要隐藏活动的传感器/物联网上行、以及任何以 Willie 式被动监听者为威胁模型的链路。不适用于：有线/互联网流量场景（本库关注的对象），也不适用于对抗主动干扰或中间人的场景。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 传统确定时间（T=1,K=1） | 收发简单 | 隐蔽性最低，信号与噪声差异显著 | ED-RTH 显著提升 ξ（Fig. 10） |
| 单时隙选择 [28] | 引入时间不确定性 | 选中时隙功率仍高，可区分度大 | 能量分散进一步压低每符号功率 |
| RSS [30] | 同类时间不确定方案 | 相同发送窗下总信道使用数固定，隐蔽性受限 | 在相同 1536 符号周期窗口下 ED-RTH 更优（Fig. 12） |
| 能量检测（Willie 次优） | 无需组合遍历，复杂度低 | K 较小时性能远差于 LRT；K=T 时趋同 | 论文用其作为对照下界（Fig. 7） |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

采用"行为级仿真"（behavioral-level simulation）：完整模拟 Alice 生成信号→叠噪→Willie 判决→统计的闭环流程（§IV-A 的 (1)–(4) 步，配 Fig. 3）。仿真参数：Willie 与 Bob 端噪声功率 σw² = σb² = 1；依据 AES-128 标准取每时隙信道使用数 n = 128；为兼顾解析清晰度与仿真复杂度取 T = 12；ρ = 0.5。

### 6.2 数据集

无公开数据集；全部为蒙特卡洛/数值仿真。Table I 给出完整记号表（T、K、n、N、D、R、Pa、Pa*、P、ξ、ε、δ、η 等）。

### 6.3 Baseline

传统确定时间方案（对应 T=1、K=1）、单时隙选择方案 [28]（T>1、K=1）、RSS 方案 [30]、以及 Willie 侧的能量检测（作为 LRT 的对照）。

### 6.4 评价指标

Willie 的检测错误概率 ξ（隐蔽性）、Alice 最大总发射功率 P（在 ξ ≥ 1−ε 约束下）、隐蔽吞吐 η、KL 散度 D(P0‖P1)。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| KL 散度 vs K（Fig. 4） | D(P0‖P1) | 随 K 单调下降并饱和 | K=1 基线 | — | 固定 P、T 下能量分散有效 |
| 检测错误概率 vs K（Fig. 5） | ξ | 随 K 单调上升 | — | — | LRT 仿真与 KL 下界趋势几乎重合 |
| 功率约束 vs ε（Fig. 6） | 允许的 P | KL 下界给出的约束更严 | LRT 数值解 | — | 用 KL 做设计更保守安全 |
| LRT vs 能量检测（Fig. 7） | ξ | K 小时 LRT 明显更优 | 能量检测 | — | K=T 时两者完全收敛 |
| ξ vs 每时隙符号数 n（Fig. 8） | ξ | 随 n 单调上升 | — | — | 固定总能量下 n 增大摊薄每符号功率 |
| 隐蔽吞吐 vs K（Fig. 9a） | η | 随 K 增大 | — | — | T=12、R=1/32 |
| 吞吐 vs ε 与编码率（Fig. 9b） | η | 高编码率上限更高 | — | — | 隐蔽约束严时低编码率反而更优 |
| 三方案对比（Fig. 10） | ξ vs P | ED-RTH 最优 | 单时隙选择 > 确定时间 | — | T=12；功率越大优势越明显 |
| ED-RTH vs RSS（Fig. 12） | ξ vs 总信道使用数 | ED-RTH 更优 | RSS | — | 相同发送窗 1536 符号周期 |

### 6.6 优势最明显的场景

**高发射功率区间**：Alice 总功率 P 越大，ED-RTH 相对单时隙选择与确定时间方案的优势越明显（Fig. 10）——因为单时隙方案的信号与噪声差异随功率线性放大，而分散策略把这个差异摊薄到 K 个时隙上。此外在"相同发送窗口、相同总信道使用数"的公平比较下（ED-RTH K=3、n=128 → nK=384；RSS T'=4、n'=384），ED-RTH 仍给出更高的 ξ（Fig. 12）。

### 6.7 局限性

- 全部结论建立在 AWGN + 完美相干合并的假设上，实际同步误差会削弱吞吐收益。
- 论文明确承认：K 增大到一定程度后隐蔽性收益边际化，而接收机复杂度"substantially"上升——即存在一个工程上的最优 K。
- 无实测验证，且衰落信道只有定性讨论。
- 论文未给出与"噪声不确定性""信道不确定性"等其他不确定性维度的联合分析。

---

## 7. 学习与应用

### 7.1 是否开源？

解析稿未见代码或仿真脚本链接，code: unknown。

### 7.2 复现关键步骤

1. 设定 T、K、n、σw²、σb²、Pa*（论文取 T=12、n=128、σw²=σb²=1）；
2. 按 ρ=0.5 采样发送状态；发送时均匀随机选 K 个时隙，每时隙填平均功率 Pa = Pa*/K 的 Gaussian 符号，其余时隙置零；
3. 叠加以 σw² 为方差的 Gaussian 噪声，形成 Willie 的长度 nT 观测；
4. Willie 侧实现式 (15) 的 LRT（遍历 $C_T^K$ 项）与能量检测，扫描阈值得到最优判决门限对应的 ξ；
5. 用 Monte Carlo 计算式 (24) 的 Γ(K) 以数值求解 KL 散度，对比式 (26) 的解析下界；
6. 在 Bob 侧按式 (32)(33) 计算有限码长解码错误概率与吞吐。

### 7.3 关键超参数、预处理和训练细节

| 参数 | 取值 | 说明 |
|---|---|---|
| T | 12 | 总时隙数（多数场景） |
| K | 1…T | 分散时隙数（扫描变量） |
| n | 128 | 每时隙信道使用数，依据 AES-128 |
| σw² = σb² | 1 | Willie 与 Bob 端噪声功率 |
| ρ | 0.5 | Alice 发送先验概率（最大化 Willie 的 ξ） |
| Pa* | 扫描变量（如 Fig. 5/Fig. 12 中 0.2） | K=1 时的每符号平均功率，假设 < σw²/2 |
| 发送窗口（与 RSS 对比时） | 1536 符号周期 | Fig. 12 的公平比较设定 |

### 7.4 能否迁移到其他任务？

可迁移的是**分析工具**而非方案本身：（i）用 KL 散度给出"检测错误概率下界"的做法，可迁移到任何"监听者做二元假设检验"的场景（例如流量分析中的 padding/掩护流量对抗评估——把 Willie 换成流量分类器，把 KL 换成可区分性度量）；（ii）"能量/信息摊薄以降低可区分度"的直觉，与流量侧的分片、填充、时延抖动等对策在思想上是同源的，可作为跨层类比素材。

### 7.5 对我的研究有什么启发？

- 论文对"KL 下界比数值最优解更严格"的强调（Fig. 6），提示在流量侧评估中也可以用更保守的解析下界来替代经验性指标，从而给出可证明的防御/攻击上界。
- "增大 K 的收益按 1/K 衰减"这一饱和现象，与流量侧"增大 padding 比例带来的防御收益递减"是同一类边际效应，可作为综述里的跨领域类比。
- 与本库主线（加密流量分类、WF）关联度低，不建议在流量分析综述中进行实质引用，最多作为"隐蔽信道 / LPD"的物理层对照提及。

---

## 8. 总结

### 8.1 核心思想

> 随机选 K 个时隙、能量均摊，以 K 换隐蔽性。

### 8.2 速记版 Pipeline

1. 时间轴切成 T 个时隙，每时隙 n 个信道使用；
2. Alice 以 ρ=0.5 决定发送与否；发送时随机选 K 个时隙；
3. 把单时隙能量均分到 K 个时隙，每符号功率 Pa = Pa*/K；
4. Willie 在 nT 个观测上用 LRT（或能量检测）判决发送与否；
5. 用 KL 散度给出 ξ 的闭式下界 ξ_LB(K) ≈ 1 − A·exp(−B(1−1/K))；
6. Bob 相干合并 K 时隙后解码，按 η = N·R·(1−δ) 计算隐蔽吞吐；
7. 结论：K↑ → ξ↑（饱和）；固定 ε 下 K↑ → η↑。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- 不适用：kb_reference C 节概念页（anomaly-detection / encrypted-traffic-analysis / malicious-traffic-detection / website-fingerprinting 等）均面向流量分析任务，与本文的物理层隐蔽通信无实质关联，故不建立 wikilink，避免污染概念图谱。

### 9.2 相关方法

- 不适用：方法页（transformer / state-space-model / contrastive-learning / multi-modal-fusion 等）无一覆盖 wireless covert communication 或 KL-divergence-based detection analysis。本文使用的方法要素（LRT、能量检测、有限码长 Q 函数、Monte Carlo）不属白名单范围。

### 9.3 相关任务

- 不适用：任务页（traffic-classification / website-fingerprinting / tunnel-detection 等）与本文的"隐蔽传输"任务无交集。

### 9.4 可更新的综述页面

- 不适用：现有五篇综述（survey-encrypted-traffic-analysis / survey-few-shot-learning / survey-malicious-traffic-detection / survey-traffic-foundation-model / survey-website-fingerprinting）均无"物理层隐蔽通信"章节，暂无自然落点。若后续建立"隐蔽信道 / 反检测通信"综述，本文可作为无线侧代表工作入库。

### 9.5 可加入的对比表

- 暂不加入：`method-comparison-table`（面向加密流量分类方法）、`dataset-comparison-table`（本文无数据集）、`open-source-registry`（本文无开源代码），三者均不适用。

### 9.6 引用的已有论文笔记

- 无：解析稿参考文献列表中未出现 kb_reference A 表内的任何论文。

---

## 10. 证据记录

| 结论 | 证据位置 | 原文关键数字 |
|---|---|---|
| ED-RTH 的能量分散机制 | §II-B | Pa = Pa*/K，P = nPa* = nKPa，K ∈ [1, T] |
| 隐蔽性假设 | §II-B | 假设 Pa* < σw²/2；ρ 取 0.5 |
| KL 散度闭式 | §III-A 式 (25) | D(K) ≈ (nγw*²/4T)·exp(−(nγw*/2)(1−1/K)) |
| 检测错误概率下界 | §III-A 式 (26) | ξ_LB(K) ≈ 1 − A·exp(−B(1−1/K))，A = √(nγw*²/8T)，B = nγw*/4 |
| K=T 时 LRT 等价能量检测 | §III-A 式 (16)(17) + §IV-B | "when K = T LRT is equivalent to energy detection" |
| 吞吐与 K 的关系 | §III-B 式 (33) | 固定 Pa* 时 η 与 K 无关；固定隐蔽约束下 η 随 K 提升 |
| 仿真参数 | §IV-A | σw² = σb² = 1，n = 128（AES-128），T = 12，ρ = 1/2 |
| 与 RSS 对比的公平设定 | §IV-C | 发送窗 1536 符号周期；ED-RTH K=3、n=128 → nK=384 = RSS 的 n' |
| 编码率与隐蔽约束的权衡 | §IV-C | 隐蔽约束越严，最优编码率越低 |
| 衰落信道的定性结论 | §III-C | Willie 缺瞬时 CSI 只能用次优能量检测，隐蔽性增强 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-TIFS-Time-Hopping_Covert_Communication_With_Random_Slots_and_Dispersed_Energy.pdf
- MinerU Markdown：02-parsed-markdown/2026-TIFS-Time-Hopping_Covert_Communication_With_Random_Slots_and_Dispersed_Energy.md

---

## 12. 后续问题

1. 解析稿中**没有出现 DOI**（已检索 "10.1109"、"DOI"、"doi.org" 均无命中），需要主代理从出版方页面补登。
2. 该论文与本库主线（加密流量分类/WF/恶意流量检测）无方法论交集，建议在知识层聚合时归入"边缘方向"，不参与 research_fronts 的加权。
3. 若后续要建立"跨层隐蔽通信"综述，本文可与会话级隐蔽信道工作（如 QUIC 隐蔽信道类论文）放在同一章节，但需明确二者威胁模型不同（物理层 Willie vs 网络层检测器）。

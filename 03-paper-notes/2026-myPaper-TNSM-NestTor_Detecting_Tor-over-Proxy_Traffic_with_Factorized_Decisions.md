---
type: paper
title_original: "NESTTOR: Detecting Tor-over-Proxy Traffic with Factorized Decisions"
title_cn: "NestTor：通过分解式决策检测 Tor-over-Proxy 流量"
authors:
  - Chenxin Zhou
  - Cheng Huang
  - Qiang Zhang
  - Qiliang Xie
  - Zeqing Li
year: 2026
venue: "IEEE Transactions on Network and Service Management (TNSM)"
publication_status: published
doi: "10.1109/TNSM.2026.3743261"
url: "https://ieeexplore.ieee.org/document/11735245"
pdf: "00-inbox/PDFs/2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions.pdf"
pdf_version: "submission-system-export-20261010; 4 cover pages + 15 manuscript pages"
mineru_md: "02-parsed-markdown/2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions.md"
status: deep-analyzed
reading_level: L3
research_area: [encrypted-traffic-analysis, anonymous-traffic-identification, tunnel-detection]
task: [tor-over-proxy-detection, traffic-classification]
method: [factorized-detection, stage-based-flow-features, histogram-gradient-boosting, negative-only-calibration]
dataset: [NestTor-Benchmark]
code: "https://github.com/GSTovey/NestTor"
code_status: "public-repository; implementation and dataset coverage assessed separately"
relevance: high
is_my_paper: true
metadata_source: crossref
metadata_verified: "2026-10-21"
venue_factor: 0.65
time_factor: 1.0
citation_impact: 0.8
internal_citation_count: 0
composite_weight: 0.52
weight_rule: "AGENTS.md §11: TNSM 未列入 Tier 2，按其他期刊 0.65，不自行调整规则"
created: "2026-10-21"
updated: "2026-10-21"
---

# NESTTOR: Detecting Tor-over-Proxy Traffic with Factorized Decisions

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | NESTTOR: Detecting Tor-over-Proxy Traffic with Factorized Decisions |
| 中文标题 | NestTor：通过分解式决策检测 Tor-over-Proxy 流量 |
| 作者 | Chenxin Zhou, Cheng Huang, Qiang Zhang, Qiliang Xie, Zeqing Li |
| 年份、期刊 | 2026，IEEE TNSM；发表状态经作者与 CrossRef 记录核对 |
| DOI | [10.1109/TNSM.2026.3743261](https://doi.org/10.1109/TNSM.2026.3743261) |
| 卷期、正式页码 | unknown；CrossRef 当前 page 为占位值 `1-1`，不作为正式页码 |
| 研究方向 | 被动加密流量分析、匿名流量识别、代理内部 Tor 检测 |
| 任务类型 | 完整双向 TCP 流的 ToP / Non-ToP 二分类 |
| 方法关键词 | 语义条件分解、相对阶段统计、独立 HGB、AND、负样本阈值校准 |
| 数据集 | 349,891 条去重双向流，1,663 个域名，四种代理、四类语义 |
| 公开资料 | [项目仓库](https://github.com/GSTovey/NestTor)；仓库公开不等于全量数据与终版实验配置均已发布 |
| PDF | [[00-inbox/PDFs/2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions.pdf]] |
| MinerU Markdown | [[02-parsed-markdown/2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions.md]] |

**资料版本**：本地 PDF 是投稿系统导出件，前四页为系统封面，正文从 PDF 第 5 页开始；不是出版社排版 PDF。分析以其正文及作者固定终版源码 `NestTor_TNSM/writing/latex/` 为依据。下文页码采用正文页码，图表编号采用 PDF 印刷编号。

**解析质量**：MinerU 成功解析 19 页；摘要、公式、表格和参考文献均已抽查。部分公式出现字符间空格，双栏图表在 Markdown 中有前后移位，系统封面问答不是论文正文。公式和计数已对照 LaTeX；Fig. 5 的自动提取图片仅含 (b) Native End-to-End 面板。

## 1. 一句话总结

NestTor 将“存在外层代理”和“代理内存在 Tor”拆成两个独立决策，用完整双向流的方向、长度和相对时序统计完成 ToP 检测，并通过严格划分和分布迁移实验刻画其有效性及边界。

## 2. 摘要翻译

### 2.1 摘要原文

Tor users can place an encrypted proxy between the client and the Tor network to conceal the exposed entry connection. This additional layer also transforms the Tor byte stream through protocol framing, buffering, and TCP segmentation before an observer sees the outer client-to-proxy flow. The transformation breaks stable packet-to-cell alignment and raises two questions. We ask which Tor behaviors remain observable across different proxies and how a detector should combine the presence of an outer proxy with the presence of Tor traffic. Existing datasets primarily study Tor and proxy traffic as separate targets and provide limited support for answering these questions under a unified evaluation protocol. We propose NESTTOR, which trains a proxy gate and a proxy-conditioned Tor detector separately and combines their decisions with an AND rule. Its stage-based features capture relative connection evolution without reconstructing Tor cells. We construct a longitudinal benchmark of 349,891 bidirectional TCP flows that distinguishes Tor-over-Proxy (ToP), Pure Proxy, Direct Tor, and Ordinary traffic across four proxy protocols, 1,663 domains, and approximately 18 months. NESTTOR achieves 99.45% macro-F1 on confirmatory data from unseen domains and 88.50% on later captures.

### 2.2 摘要中文翻译

Tor 用户可以在客户端与 Tor 网络之间加入加密代理，隐藏原本暴露的入口连接。这一额外层也会通过协议分帧、缓冲和 TCP 分段变换 Tor 字节流，使观察者只能看到客户端到代理的外层流量。该变换破坏了数据包与 Tor cell 的稳定对应关系，并带来两个问题：哪些 Tor 行为在不同代理之后仍然可见，以及检测器应如何结合外层代理存在与 Tor 流量存在的证据。现有数据集主要将 Tor 和代理流量作为独立目标研究，难以在统一评估协议下回答这些问题。本文提出 NestTor，分别训练代理门控和以代理为条件的 Tor 检测器，并通过 AND 规则组合二者的决策。基于阶段的特征不重构 Tor cell，而是描述连接相对生命周期中的行为演化。作者构建包含 349,891 条双向 TCP 流的纵向基准，区分 ToP、Pure Proxy、Direct Tor 和 Ordinary，覆盖四种代理协议、1,663 个域名及约 18 个月。NestTor 在未见域名确认数据上达到 99.45% macro-F1，在后续采集数据上达到 88.50%。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

代理隐藏了直连 Tor 的外观，但“识别代理”不能说明代理内部运行 Tor，“识别 Tor 行为”也不能排除 Direct Tor。目标标签本身是两个条件的合取，输入却只有客户端至代理这一跳的加密双向流。作者将任务语义、可观测信号与分类结构对应起来。依据：§I、§III-A。

### 3.2 现有方法的痛点和不足

- **观察对象发生变换**：代理分帧、缓冲和网络分段破坏 cell 与外层 packet 的一一关系，固定 cell 尺度不再可靠。§III-B。
- **任务标签容易混淆**：Pure Proxy 与 Direct Tor 分别满足一个条件，是检验 ToP 检测的必要困难负类。§III-A。
- **评估容易混入来源捷径**：地址、端口、域名及采集标识会与类别相关，需要在模型输入与划分层面同时控制。§V-A。

### 3.3 论文的研究假设或核心直觉

跨代理可能保留交互顺序、阶段演化和 burst-response 耦合；将代理与内层 Tor 分别监督，可以减少平面二分类依赖单一条件的错误。前者通过协议统计审计检验，后者通过固定表示和预算的结构对照检验。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | ToP 的客户端外发流量不再直接呈现 Tor 入口连接 | §I、Fig. 1 |
| 痛点提炼 | 固定 cell 尺度遭到变换；代理存在与 Tor 存在不能互相替代 | §III-A/B |
| 问题转化 | 在单条外层双向流上，识别哪些行为保留，并联合估计两个条件 | §III、§IV |
| 文献定位 | 隧道、代理、Tor 及特定嵌套配置已有研究；本文补充四代理、四类和统一泄漏控制 | §II；不解读为首次研究所有嵌套检测 |

### 3.5 科学假设形成

| 假设 | 推导依据 | 验证方式 | 结果 |
|---|---|---|---|
| 跨代理保留较高层交互行为 | 外层变换不必完全消除交互顺序与生命周期 | 147 候选统计的跨代理审计 | 31 项通过：20 早期方向交互、7 多尺度动力学、4 burst-response；soft cell lattice 为 0，§VI-RQ1 |
| 语义分解带来独立于特征容量的收益 | ToP = 代理存在 AND 代理内部 Tor | 相同 99 维输入、RF 实现和总 400 棵树预算 | Gate + Inner 94.12%，Shared Multi-task 88.11%，§VI-RQ3 |
| Pure Proxy 可用于缺少目标 ToP 标注时的校准 | 目标负类得分可估计上尾阈值 | leave-one-proxy-out + 独立负类参考集 | 收益依代理而变；Trojan 校准后下降，Table IV |

## 4. 方法设计

### 4.1 方法整体流程

![[10-outputs/key-figures/images/2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decis__Fig__3__728c238898455058.jpg]]

Fig. 3 为完整框架：双向流预处理 → 99 维阶段行为表示 → 独立代理门控与条件 Tor 检测器 → 固定阈值 AND；可选负类校准与已知环境选门在评估前完成。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| 1. 流构建 | PCAP | 重建完整双向 TCP 流、payload 序列去重、每 capture 最多 5 流 | 单流包序列 | 统一样本单位与来源控制 |
| 2. 标识排除 | 方向、TCP payload 长度、相对 IAT | 不向模型输入地址、端口、域名、绝对时间、来源 ID、代理标签、SNI、握手哈希或 payload 内容 | $(d_i,\ell_i,\Delta t_i)$ | 控制捷径 |
| 3. 基础表示 | 完整单流序列 | 汇总体量、分布、长度、时序、方向游程、burst 与反向响应 | 62 维 base | 描述全局行为 |
| 4. 相对阶段 | payload 包索引 | 按相对包位置三等分，统计阶段内行为及选定早晚差分 | 37 维 dynamics；拼接为 99 维 | 描述连接演化 |
| 5. 代理门控 | 99 维表示 | ToP + Pure Proxy 对 Ordinary + Direct Tor，独立 HGB | $q(x)$ | 判断外层代理 |
| 6. 内层检测 | 代理流量的表示 | ToP 对 Pure Proxy，另一个独立 HGB | $t(x)$ | 区分代理内是否有 Tor |
| 7. 校准与决策 | 两个得分、冻结阈值 | 可先用独立 Pure Proxy 参考校准内层阈值；两个条件同时通过才判 ToP | ToP / Non-ToP | 对应复合标签 |

### 4.3 模型结构或系统模块

| 模块 | 输入/输出 | 与其他模块关系 |
|---|---|---|
| Stage representation | 完整双向流 → 99 维 | 主方法固定表示，无须重构 cell |
| Gate $Q$ | 99 维 → 代理得分 | 与内层模型不共享编码器、参数或联合损失 |
| Inner $T$ | 主方法 99 维，Residual 变体 97 维 → 条件 Tor 得分 | 监督训练仅使用 ToP 与 Pure Proxy |
| Negative-only calibration | 独立目标 Pure Proxy 参考得分 → 内层阈值 | 不使用目标 ToP 标签，不重训分类器 |
| Environment selector | 独立 800 条无标签流窗口 → 已知环境对应门控 | 可选扩展；仅验证两个已知采集环境，内层模型不变 |

### 4.4 公式、算法和机制解释

单流观察量与任务定义为：

$$x=\{(d_i,\ell_i,\Delta t_i)\}_{i=1}^{n},\qquad y(x)=s_P(x)\land s_T(x).$$

这里 $s_P$ 表示外层代理存在，$s_T$ 表示 Tor 存在。Pure Proxy 为 $(1,0)$，Direct Tor 为 $(0,1)$，Ordinary 为 $(0,0)$，ToP 为 $(1,1)$。这是标签定义，不是把能访问到的真实条件直接作为模型输入。

相对位置与表示为：

$$u_i=\frac{i-1}{\max(n-1,1)},\qquad \phi_{stage}=[\phi_{base}^{62},\phi_{dyn}^{37}]\in\mathbb R^{99}.$$

按 $[0,1/3)$、$[1/3,2/3)$、$[2/3,1]$ 分早、中、晚阶段。该坐标依据包索引，不是协议状态，也不是在线 1-RTT 前缀。

最终规则为：

$$\widehat y(x)=\mathbb I[q(x)\ge\tau_Q]\land\mathbb I[t(x)\ge\tau_T].$$

原确认规则包含按代理校准的内层阈值；统一阈值对照对所有流使用 $\tau_Q=0.485,\tau_T=0.225$。二者结果分别是 99.45% 与 99.41% macro-F1，不混用。

负类校准采用：

$$\tau_T^{(u)}=\operatorname{next}_{+}\!\left(\operatorname{Quantile}^{higher}_{0.99}\{t(x):x\in\mathcal R^-_u\}\right).$$

`higher` 为经验上分位数规则，`next+` 将阈值移到该分位数之后的下一个可表示浮点数。它控制参考集上的经验误报，不保证未知背景分布上的同等 FPR。依据：§IV-C、Appendix B。

**两种候选统计口径**：机制审计跨四代理保留 31/147；检测变体在每个训练折内重新选择，确认配置仅用 SS/Trojan/VMess 选出 35 项，与 62 维 base 拼成 97 维。31 与 35 分属不同用途，不能互换。

### 4.5 方法优势

语义条件与模型监督明确对应；不依赖解密和终端标识；可将错误定位为代理门控失败或代理内 Tor 判别失败。相同 RF 表示和总树数的结构对照支持独立边界的收益。依据：§IV、§VI-RQ3。

### 4.6 方法不足

依赖完整双向流与包边界统计；重分段和环境漂移会同时影响门控与内层模型；校准需要独立负类参考，环境选门需要已知环境及独立窗口。没有据此证明单向、不完整观测或任意未知代理均可检测。

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

外层代理指纹回答“是否有代理”，网站指纹回答“访问哪个网站”，而本研究回答“外层代理中是否承载 Tor”。方法的重点在复合目标的条件分解，不是增加新的字节语义编码器。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 任务语义与分解决策对应 | 两个独立监督问题经 AND 合成 ToP | 高；有等表示、等 RF 树预算对照 | 可作为复合标签设计思路，迁移效果需验证 |
| 外层变换后的行为表示 | 62 维 base + 37 维相对阶段，不恢复 cell | 中；阶段在特征消融中增益小于 base | 可迁移相对阶段思想 |
| 纵向与标签受限评估 | 四类、域/capture 隔离、代理留出、负类校准、later/background | 高；构成系统适用边界证据 | 可迁移评估协议 |

### 5.3 适用场景

客户端出口或本地网关上的完整双向 TCP 流离线筛查、测量和取证。输入不要求代理配合或主动探测；在线首包阻断、流尚未结束时的服务延迟不是已验证能力。

### 5.4 方法对比表

| 方法 | 输入与任务 | NestTor 文中的对照含义 |
|---|---|---|
| FS-Net | 有向包长序列、Bi-RNN | 共用门控时 99.50%，与 NestTor 差值区间跨零；原生端到端 87.46% |
| ET-BERT | 去标识头部后的 bigram 字节表示 | 原生端到端 72.85%；共用门控下比较的是内层判别 |
| YaTC | 流量图像、MAE/ViT | 原生端到端 84.17% |
| NetMamba | 原始接口的 byte allocation + stride | 原生端到端 84.72%；512B 重分段优于 NestTor |
| TrafficFormer | 去地址/端口的 bigram tokens | 原生端到端 73.82% |
| Flat RF / Shared Multi-task | 与分解结构相同 99 维表示和 400 棵树总预算 | 用于归因决策结构，不等同于外部模型性能比较 |

## 6. 实验表现与优势

### 6.1 实验设计和设置

先按域名、再按 capture 划分，训练、验证和评估不共享域名或 capture。模型输入剔除标识字段；每 capture 最多保留 5 流；模型、阈值和分析规则在确认评估前冻结。确认集来自同一采集环境的 125 个新域名。

VLESS 不参与监督拟合和源域阈值选择，但独立 Pure Proxy 子集用于目标负类校准；四代理机制审计与训练折内特征选择必须分开解释。随机包扰动使用五个种子，属于扰动重复，不代表主模型经过五个独立训练种子。依据：§V-A/E/F、Appendix A/B。

### 6.2 数据集

| 口径 | 规模与构成 | 解释 |
|---|---|---|
| 完整 NestTor Benchmark | 349,891 流；86,889 ToP、39,516 Pure Proxy、191,769 Ordinary、31,717 Direct Tor | 四类总和一致；1,663 域名；2025-01 至 2026-07，约 18 个月 |
| 四种 ToP 代理 | SS 27,915；Trojan 23,598；VMess 15,714；VLESS 19,662 | 总和 86,889 |
| 来源组 | Earlier 221,216；Current 47,752；Later 80,923 | 总和 349,891；Earlier 没有 Pure Proxy 和 VLESS |
| 冻结确认集 | 2,300：900 ToP、1,000 Pure Proxy、150 Ordinary、250 Direct Tor | 125 新域名；类别比例为评估设计，不是部署基准率 |
| later 评估集 | 23,374 流 | 是 Later 来源组中的评估口径，不等于整个 80,923 流来源池 |
| 异质背景 | 11,131 流 | HTTPS、批量传输、I2P/JonDonym、视频、CDN、VPN |
| 环境路由子集 | Earlier 1,000；Current 800 | Earlier 子集来自 2025-06/07，不等于含 2025-01 数据的全部历史池 |

Earlier 的“2025 年 6–7 月”名称是包含更早公开数据的归并报告标签，不把归并标签当作所有样本真实采集日期。全量数据可获取范围须与仓库数据说明分别核对。

### 6.3 Baseline

外部方法为 FS-Net、ET-BERT、YaTC、NetMamba、TrafficFormer；受控结构包括 Flat Binary、Inner Only、Gate Only、Shared Multi-task、Independent Gate + Inner，并有同表示 Flat HGB。共用门控实验与原生端到端实验使用不同问题定义，结果分别记录。

### 6.4 评价指标

主指标为 ToP 与 Non-ToP 两类 F1 的算术平均 macro-F1；ToP 报 TPR，负类分别报 FPR。确认集支持域内新域名迁移，later 使用按域名 bootstrap 的置信区间；异质背景的 PR-AUC 使用 ToP/背景等总权重，不能直接作为实际低基准率 precision。

### 6.5 关键实验结果

| 任务/设置 | 指标 | 本文方法 | 对照 | 解释与位置 |
|---|---|---:|---:|---|
| 原确认规则 | macro-F1 / TPR / Pure Proxy FPR | 99.45 / 99.33 / 0.60% | TP/FN=894/6，FP/TN=6/1,394 | Table III/X；按代理内层阈值 |
| 统一阈值 | macro-F1 / Pure Proxy FPR | 99.41 / 0.70% | 比原规则多 1 个 Pure Proxy FP | Table III/X；固定 0.485/0.225 |
| 共用门控 | macro-F1 | 99.45% | FS-Net 99.50% | Fig. 5(a)；差值 95% CI [-0.36,0.46]，不支持显著优于 FS-Net |
| 原生端到端 | macro-F1 | 99.45% | 最强外部 FS-Net 87.46% | Fig. 5(b)，+11.99 个百分点 |
| RF 结构归因 | macro-F1 | Independent 94.12% | Shared 88.11%；Flat 86.67% | 同 99 维、总 400 棵树，Fig. 6 |
| HGB 结构对照 | macro-F1 | 分解 99.45% | Flat HGB 87.64% | 同分类器家族与表示；不冒充 RF 等总预算实验 |
| 特征消融 | macro-F1 | Base + Stage 99.25% | Coarse 97.00；Base 99.15；Residual 99.45；去粗统计 99.18% | Fig. 7；独立诊断模型，不替换主确认结果 |
| 512B 重分段 | macro-F1 | 71.45% | NetMamba 83.56% | Fig. 8；Direct Tor FPR 升至 86.4% |
| 50% padding / 50±10 ms delay / 3% loss | macro-F1 | 96.65 / 98.45 / 99.25% | 该组变换中 NestTor 最高 | Fig. 8；五个扰动种子算术平均 |
| later 23,374 流 | macro-F1 | 88.50% [87.85,89.15] | FS-Net 57.49% | Table V；TPR 86.50%，Pure Proxy FPR 5.44% |
| 异质背景固定 AND | FPR / ToP TPR | 3.14 / 99.33% | 350/11,131 背景误报 | Table VI；ToP TPR 来自 900 条确认正类参考 |
| 已知两环境选门 | 等权平均 macro-F1 | 95.77% | Current gate 54.97% | Table VII；不代表未见环境自动适应 |

代理留出与校准的 macro-F1（Table IV）：

| 表示/设置 | Shadowsocks | Trojan | VMess | VLESS |
|---|---:|---:|---:|---:|
| Stage，无目标校准 | 71.77 | 97.81 | 85.12 | 97.60 |
| Residual，无目标校准 | 90.37 | 97.24 | 92.35 | 98.45 |
| Residual + 负类校准 | 97.77 | 93.60 | 94.15 | 99.45 |

异质背景的另外三个点使用连续分数 $s(x)=q(x)t(x)$ 事后扫阈值：FPR 0.99/0.10/0.01% 时 TPR 94.44/86.22/72.33%。这些是描述性工作点，不能说原冻结 AND 自动实现了这些误报率。等总权重 PR-AUC=0.9812。

### 6.6 优势最明显的场景

完整双向流、四类困难负样本齐备、域名/capture 隔离的新域名确认，以及 later 采集集上的整体检测性能。结构对照明确支持分别学习条件边界；共用门控下与 FS-Net 的内层识别能力没有统计上可分辨的差异。

### 6.7 局限性

- 512B 重分段导致明显失效，特别是 Direct Tor 门控误报；“不依赖 cell 对齐”不等于“对任意重分段不敏感”。
- later 比确认集下降 10.95 个百分点，四代理的主导错误来源不同。
- 完整流输入，16/32/64/128/256 包前缀均更弱；不能据模型推理耗时推断早期检测。
- 在预构造特征上，四 CPU 线程 batch=1 平均/P95 推理为 3.44/3.52 ms，batch=64 为 18,031 流/秒；包括解析和特征构建的离线流程是 2,500 流/156 秒，即 16.0 流/秒。95.7% 时间花在前处理，模型吞吐不等于系统吞吐。
- 环境路由仅在两个已知环境验证；负类校准只修正得分位置/尺度，不能恢复排序信息或消除未知背景差异。

## 7. 学习与应用

### 7.1 是否开源？

[GSTovey/NestTor](https://github.com/GSTovey/NestTor) 已核验为公开仓库。论文、框架图、数据说明与实现文件分开核验；没有用旧项目仓库代替本论文代码。当前数据说明明确公开的是 650 流处理后兼容性样例，含 99 维特征与对齐序列，但没有 Pure Proxy，既不是完整开发集也不是确认集。全量 349,891 流与终版实验的复现仍需对应固定 manifest 和完整配置。

### 7.2 复现关键步骤

1. 核对原始 PCAP、类别/域名/capture manifest 及去重后的四类计数，区分来源池与各评估子集。
2. 在划分前确定域名/capture 分组规则；模型表示只保留方向、TCP payload 长度、相对 IAT，校验 62+37=99。
3. 独立训练代理 HGB 与条件 Tor HGB，分别选择源域阈值；目标代理只用独立 Pure Proxy 参考校准。
4. 固定模型、阈值、候选选择和评估规则后执行确认评估，再分别报告 later、异质背景和五种子扰动结果。

本次仅入库与核对已发表证据，未运行或重建实验。需要的原始 manifest、训练配置或全量数据若不在发布资料中，记为未公开/待作者提供。

### 7.3 关键超参数、预处理和训练细节

| 配置 | 已核验值 | 依据 |
|---|---|---|
| Gate HGB | 99 维；learning_rate=0.03；max_leaf_nodes=7；L2=3 | Appendix B |
| Inner HGB | Stage 99 维 / Residual 97 维；learning_rate=0.07；max_leaf_nodes=7；L2=1 | Appendix B |
| RF 结构消融 | 总 400 棵树；独立 Gate/Inner 各 200；其余结构各 400 | §V-E2 |
| 负类校准 | alpha=0.01；higher 99% 分位数后取下一浮点数 | Appendix B |
| 候选审计 | 前 128 个 payload 包；147 候选；AUC 严格 >0.58；泄漏偏差 <0.05；100,000 次置换校正 | §III-C、Appendix A |
| 环境画像 | 独立无标签 800 流窗口 | §IV-D、§V-F4 |
| 其他训练配置 | 以上不是完整配置清单；正文未完整展开的参数不补造 | 发布实现、manifest 需逐项核对 |

### 7.4 能否迁移到其他任务？

**合理推断**：可将“外层载体存在 AND 内层目标存在”的条件设计迁移至其他嵌套服务识别，也可迁移相对生命周期表示。论文没有证明单向观测、UDP/QUIC 封装、其他匿名网络或持续未知类识别的有效性。

### 7.5 对我的研究有什么启发？

用困难负类分离“只识别外壳”和“真正识别内层”的能力；用共享门控与原生端到端两种协议定位收益来源；将包边界与时间/环境漂移作为独立问题，不把受控高分当作部署保证。

## 8. 总结

### 8.1 核心思想

> 分别判断代理与 Tor，取合取。

### 8.2 速记版 Pipeline

1. 完整双向流 → 方向/长度/相对时间。
2. 62 维全局行为 + 37 维相对阶段。
3. 独立代理门控与代理条件 Tor HGB。
4. 按已冻结规则校准并执行 AND。
5. 分开报告域内确认、later、开放背景与扰动。

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[encrypted-traffic-analysis]]、[[04-concepts/traffic-classification|traffic-classification]]、[[anonymous-traffic-identification]]、[[04-concepts/tunnel-detection|tunnel-detection]]、[[traffic-representation-learning]]。

### 9.2 相关方法

- [[factorized-detection]]：复合语义条件分解；HGB 与 RF 对照。

### 9.3 相关任务

- [[06-tasks/tunnel-detection]]、[[06-tasks/traffic-classification]]、[[encrypted-traffic-detection]]。

### 9.4 可更新的综述页面

- [[survey-encrypted-traffic-analysis]]；[[representation-vs-shallow]] 的任务条件化证据。

### 9.5 可加入的对比表

- [[method-comparison-table]]、[[dataset-comparison-table]]、[[open-source-registry]]、[[motivation-pattern-comparison]]、[[narrative-pattern-comparison]]。
- 相关主库论文：[[2019-INFOCOM-FS-Net__A_Flow_Sequence_Network_For_Encrypted_Traffic_Classification]]、[[2022-WWW-ET-BERT__A_Contextualized_Datagram_Representation_with_Pre-training_Transformers_for_Encrypted_Traffic_Classification]]、[[2023-AAAI-Yet_Another_Traffic_Classifier_a_Masked_Autoencoder_Based_Traffic_Transformer_With_Multi-level_Flow_Representation]]、[[2024-ICNP-NetMamba__Efficient_Network_Traffic_Classification_via_Pre-training_Unidirectional_Mamba]]、[[2025-S&P-TrafficFormer_An_Efficient_Pre-trained_Model_for_Traffic_Data]]。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 目标为代理存在与 Tor 存在的合取 | 四类语义定义、单观察点限制 | §III-A，正文 p.3 |
| 99 维主表示、97 维 Residual 变体 | 62+37 与训练折内选取 35 候选 | §IV-A，Appendix B |
| 两模型独立训练后 AND | 不共享参数或联合损失 | §IV-B |
| 2,300 条确认集和原/统一阈值结果 | 900/1,000/150/250；894 TP，原规则 6 FP | Table III、Table X |
| 共享门控与原生端到端必须分开 | FS-Net 分别为 99.50% 与 87.46% | Fig. 5、§VI-RQ2 |
| 结构收益经过匹配控制 | 99 维、RF、总 400 棵树 | §V-E2、Fig. 6 |
| 后续采集仍有优势但退化 | 23,374 流；88.50% [87.85,89.15] | Table V、§VI-RQ4 |
| 重分段构成显著边界 | 512B 下 71.45%，Direct Tor FPR 86.4% | Fig. 8、§VI-RQ3 |
| 低误报率工作点不是冻结 AND 的同一规则 | 固定 AND 与乘积分数扫阈值分开 | Table VI、§VI-RQ4 |
| 来源池不能替换子集口径 | Earlier/Current/Later 与环境比较子集分开 | Appendix D、Table IX |
| 发表元数据真实可核验 | CrossRef DOI、作者顺序、期刊、年份；页码占位 | [CrossRef API](https://api.crossref.org/works/10.1109/TNSM.2026.3743261)，2026-10-21 |

## 11. 原始资料链接

- PDF：[[00-inbox/PDFs/2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions.pdf]]。
- MinerU Markdown：[[02-parsed-markdown/2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions.md]]。
- 机器解析原始资源：`01-mineru-output/2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions/`。
- 正式论文：[IEEE Xplore](https://ieeexplore.ieee.org/document/11735245)；[DOI](https://doi.org/10.1109/TNSM.2026.3743261)。
- 公开项目：[GSTovey/NestTor](https://github.com/GSTovey/NestTor)。

## 12. 后续问题

- 在单向或不完整观测下，哪些条件证据仍可估计？这是后续问题，不是本文能力。
- 能否减少重分段对 burst、相对阶段和门控边界的影响，同时保持统一背景低 FPR？
- 未知采集环境下能否可靠拒绝环境路由，而不依赖已有两环境闭集？
- 在真实低 ToP 占比下，如何利用独立背景数据选择并验证工作点？

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

代理既隐藏 Tor 的直接入口，也改变可见流量的结构，使“看见代理”与“看见 Tor”不再等价。论文先定义四类语义，接着从外层变换推导可观察行为，再用两个独立边界对应两个条件。实验依次回答信号是否存在、检测是否有效、设计为何有效以及跨分布能保留多少能力。高确认分数与重分段、later 退化共同闭合适用范围。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 关键转折点 |
|---|---|---|
| Abstract / I | 将代理封装引入的观察变化变成两个可回答问题 | 从协议外观转向复合标签 |
| II | 对齐隧道、代理、Tor、表示与评估风险 | 现有任务并非同一个目标 |
| III | 定义观察点、四类语义与可观测假设 | 解释为什么不恢复 cell |
| IV | 表示、独立边界、AND、受限标签校准 | 每个模块对应一个问题 |
| V | 固定数据、划分、标签权限和比较协议 | 共用门控不冒充端到端比较 |
| VI | 四 RQ 逐层验证并定位失败 | 从确认高分转向跨分布边界 |
| VII / Appendix | 收束贡献，补全计数、配置和控制 | 子集、阈值、来源池相互可追溯 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 观察条件缺口 | 外层 packet 与内层 cell 不稳定对应 | 协议变换分析 + 候选审计 | §III、RQ1 |
| 目标与结构不匹配 | 平面目标可能混淆两个条件 | 四类语义 + 匹配结构对照 | §III-A、RQ3 |
| 评估证据不足 | 单环境或单类负样本不足以说明部署 | 严格划分、later、背景与扰动分开报告 | §V、RQ4 |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线关系 |
|---|---|---|
| 协议审计 | 先证明可见信号存在 | 避免凭模型高分猜机制 |
| 确认与端到端 | 分开检验条件判别与完整系统 | 直接回应两个条件 |
| 结构与特征消融 | 分离决策结构、base 和阶段表示的增益 | 避免把所有收益归给单个模块 |
| 逐流例证 | 解释平面模型修正与分解模型自身错误 | 让门控/内层语义可检查 |
| 迁移与扰动 | 暴露包边界和采集条件依赖 | 使结论随协议与观测条件收束 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移模式 |
|---|---|---|
| 开篇 | 从通信路径变化起笔 | 先说明观察对象为何改变 |
| Gap | 信号、目标、评估三层问题 | 让每个缺口有对应证据 |
| 方法 | 条件定义直接导出模块与决策 | 不以模块堆叠代替机制 |
| 实验 | RQ1–RQ4 从存在性到适用边界 | 每一组实验只承担清晰论证职责 |
| 局限 | 用失败条件、误报类别和开销构成描述边界 | 以具体测量取代泛化式自我辩护 |
| 值得借鉴的结构 | 语义定义 → 观察变换 → 条件分解 → 受控验证 | 适合嵌套目标检测的写作组织 |

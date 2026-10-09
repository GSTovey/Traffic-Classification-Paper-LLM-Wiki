---
type: paper
title_original: "Comparative Analysis of Deep Learning Models for Real-World ISP Network Traffic Forecasting"
title_cn: "面向真实 ISP 网络流量预测的深度学习模型对比分析"
authors: ["Josef Koumar", "Timotej Smoleň", "Kamil Jeřábek", "Tomáš Cejka"]
year: 2026
venue: "IEEE TNSM 2026"
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-TNSM-Comparative_Analysis_of_Deep_Learning_Models_for_Real-World_ISP_Network_Traffic_Forecasting.pdf"
mineru_md: "02-parsed-markdown/2026-TNSM-Comparative_Analysis_of_Deep_Learning_Models_for_Real-World_ISP_Network_Traffic_Forecasting.md"
status: processed
reading_level: L2
research_area: ["anomaly-detection", "network traffic forecasting", "time series analysis"]
task: ["anomaly-detection", "traffic forecasting"]
method: ["GRU", "LSTM", "GRU-FCN", "LSTM-FCN", "ResNet", "InceptionTime", "RCLSTM"]
dataset: ["CESNET-TimeSeries24"]
code: "https://github.com/koumajos/isp-forecasting-benchmark"
relevance: medium
created: "2026-09-19"
updated: "2026-09-19"
---

# Comparative Analysis of Deep Learning Models for Real-World ISP Network Traffic Forecasting

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Comparative Analysis of Deep Learning Models for Real-World ISP Network Traffic Forecasting |
| 中文标题 | 面向真实 ISP 网络流量预测的深度学习模型对比分析 |
| 作者 | Josef Koumar（捷克技术大学 FIT / CESNET）、Timotej Smoleň（捷克技术大学 FIT）、Kamil Jeřábek（布尔诺理工大学 FIT）、Tomáš Cejka（捷克技术大学 FIT / CESNET，通讯作者 koumajos@fit.cvut.cz） |
| 年份 | 2026 |
| 会议/期刊 | IEEE TNSM 2026（IEEE Transactions on Network and Service Management；解析稿未标注卷期与 DOI） |
| 研究方向 | 真实 ISP 网络流量预测（time-series forecasting）、时序基准评测；服务于资源规划与异常检测 |
| 任务类型 | 单变量多步流量预测：在 institution / subnet / IP 三个聚合粒度、18 个指标上预测下一值 |
| 方法关键词 | 滑动窗口、MinMax 归一化、缺失值零填充、Adam + MSELoss、超参搜索；GRU / LSTM / GRU-FCN / LSTM-FCN / ResNet / InceptionTime / RCLSTM |
| 数据集 | CESNET-TimeSeries24（真实 ISP 网络 CESNET3，283 家机构、548 个子网、>270,000 个 IP，40 周，2023-10 至 2024-07，10 min/1 h/1 day 三种聚合间隔；本文用 1 小时序列） |
| 是否开源 | 是（论文正文注明代码与实验发布在 GitHub，见 §7.1） |
| PDF | 00-inbox/PDFs/2026-TNSM-Comparative_Analysis_of_Deep_Learning_Models_for_Real-World_ISP_Network_Traffic_Forecasting.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-TNSM-Comparative_Analysis_of_Deep_Learning_Models_for_Real-World_ISP_Network_Traffic_Forecasting.md |

---

## 1. 一句话总结

> 在真实 ISP 数据集 CESNET-TimeSeries24 上把 7 种深度模型与均值基线做标准化对比：简单循环网络（GRU/LSTM）总体最优、GRU-FCN 精度-效率折中最好，InceptionTime/ResNet 与长预测窗明显吃亏，聚合粒度越细（IP 级）越难预测。

---

## 2. 摘要翻译

### 2.1 摘要原文

> "Accurate network traffic forecasting is essential for Internet Service Providers (ISP) to optimize resources, enhance user experience, and mitigate anomalies. This study evaluates state-of-the-art deep learning models on CESNET-TimeSeries24, a recently published, comprehensive real-world network traffic dataset from the ISP network CESNET3 spanning multivariate time series over 40 weeks. Our findings highlight the balance between prediction accuracy and computational efficiency across different levels of network granularity. Additionally, this work establishes a reproducible methodology that facilitates direct comparison of existing approaches, explores their strengths and weaknesses, and provides a benchmark for future studies using this dataset."

### 2.2 摘要中文翻译

准确的网络流量预测对 ISP 优化资源、提升用户体验与缓解异常至关重要。本研究在 CESNET-TimeSeries24 上评测了当前最先进的深度学习模型——该数据集是近期发布的、来自 ISP 网络 CESNET3 的综合真实流量数据集，覆盖 40 周的多变量时间序列。我们的发现揭示了在不同网络聚合粒度下预测精度与计算效率之间的权衡。此外，本工作建立了一套可复现的方法学，便于对既有方法做直接比较，剖析其优缺点，并为后续使用该数据集的研究提供基准。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

实时监控不足以主动管理网络资源，ISP 需要预测流量走势以提前分配带宽、扩容与规避拥塞（§1）。但"网络流量预测方法究竟谁更好"这一判断长期不可靠：该领域缺乏长期真实数据集，多数工作要么用非为预测设计的公开数据（如 MAWI 每天仅 15 分钟），要么用不公开或合成数据（§2）。作者以 CESNET-TimeSeries24 这一新发布的真实 ISP 数据集为统一基础，做可复现的横向对比。

### 3.2 现有方法的痛点和不足

| 痛点 | 具体表现 | 证据 |
|---|---|---|
| 数据集不统一 | 各工作各用各的数据集，方法难以比较；许多数据并非为预测评测设计（WIDE/MAWI 每天 15 分钟）、不公开或为合成数据 | §2 |
| 统计模型的局限 | ARIMA/SARIMA/ETS/HMM 假设线性与平稳，对高峰时段的非线性、高频波动建模能力不足 | §1、§2 |
| 合成数据造成"虚假进步" | 在合成数据上评估新方法会制造并不存在的进展错觉（引 Wu et al.） | §1 |
| 深度模型膨胀但缺乏统一评测 | LSTM/GRU→FCN 混合→ResNet/InceptionTime→Transformer 变体层出不穷，却缺少可比评测 | §2 |

### 3.3 论文的研究假设或核心直觉

- 真实 ISP 流量的可预测性随聚合粒度与指标类型而系统性变化：聚合越粗（机构级）、越偏"量"的指标（flows/packets/bytes）越可预测；越细（IP 级）、越偏"比例"的指标（TCP/UDP 比、方向比）越难。
- 缺失值（以 0 填充）比例是精度的主要破坏因素。
- 更强的模型/更长的窗口未必更好（引 Zeng et al.："简单线性模型可胜过 Transformer"），需要在真实数据上实测检验。
- 预测窗越长，误差累积越严重。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | ISP 业务多样、流量波动加剧，实时监控不足以前瞻性调度；DL 方法数量激增但缺乏可比评测 | §1 |
| 痛点提炼 | 缺少长期真实数据集与统一方法学，导致评估不可复现、性能结论不可信 | §2 |
| 问题转化 | 把"哪种 DL 模型适合真实 ISP 流量预测"转化为四个可回答的研究问题（RQ1 性能 / RQ2 窗口影响 / RQ3 聚合粒度影响 / RQ4 指标影响） | §1, RQ1-RQ4 |
| 文献定位 | 统计方法→RNN→FCN 混合→ResNet/InceptionTime→Transformer 演进链条清晰，但评测基础薄弱；CESNET-TimeSeries24 首次提供大规模真实 ISP 时序 | §2 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 在真实 ISP 数据上，模型精度主要由聚合粒度与指标可预测性决定，而非模型复杂度 | §2 文献综述 + RQ1/RQ3 | 1,318,320 个模型的大规模对比实验 |
| 辅助假设 1 | 训练/预测窗口越大精度越高 | 常规时序直觉 | 5 组窗口组合（24/168/744 × 1/168/24） |
| 辅助假设 2 | 更复杂的架构（InceptionTime/ResNet）应优于简单 RNN | 图像/时序分类领域的成功经验 | 相同数据与调参流程下的横向比较 |

**假设验证结果**：

| 假设 | 支撑/部分支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 粒度/指标决定精度 | 支撑 | 机构级整体 Harmonic 0.152 → 子网 0.190 → IP 级 0.300（均值基线同趋势）；缺失率与 R² 在 IP 级负相关 −0.69 | §6.1, Table 6, §6.1 末段 |
| 窗口越大越好 | 反驳 | 小训练窗（≤168）精度最高，训练窗增大反而下降；预测窗 1 明显优于 24/168 | §7 RQ2, Table 4-6 |
| 更复杂模型更优 | 反驳 | InceptionTime 全面最差（Harmonic 总体均值 0.46035，GRU 0.14838）、ResNet 次差（0.17115） | §6.1, Table 6 |

---

## 4. 方法设计

### 4.1 方法整体流程

方法学遵循数据集推荐用法（§5）：取数据集的 institutions / institution subnets / IP sample 三个部分，统一用 1 小时聚合；对每条时间序列指标单独建模（单变量）；预处理依次为"缺失值填 0 → 仅用训练集拟合 MinMax → 滑动窗口切分"；再在每个（模型 × 窗口组合 × 指标 × 时间序列）组合上训练并评测，最后按数据集部分与总体做宏平均汇总。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 缺失值处理 | 原始时间序列 | 缺失值填 0（表示无传输流量），并统计缺失比例 | 连续序列 | 让 DL 模型可直接处理；同时把"高缺失率"作为分析变量 |
| Step 2 划分 | 全序列 | 前 35%（14 周）训练、随后 5%（2 周）验证、剩余 24 周测试；测试期不重训 | 三段时间序列 | 避免迭代式方法（如 SARIMA）的评测优势 |
| Step 3 归一化 | 训练/验证/测试段 | 仅在训练集上拟合 MinMax，再变换三段 | 归一化序列 | 防止信息泄漏 |
| Step 4 滑窗构造 | 归一化序列 | 训练窗 L ∈ {24,168,744} × 预测窗 H ∈ {1,24,168}（共 5 组合），窗口按 H 前移，生成重叠样本 | (输入窗, 目标窗) 对 | 学习时序依赖并覆盖长短视界 |
| Step 5 训练与调参 | 样本 | Adam + MSELoss；对 RNN 层数、隐层大小、batch、学习率、epoch 做网格搜索（先以各部分随机 50 条序列的均值定超参） | 训练好的模型 | 保证各模型在可比条件下对比 |
| Step 6 评测汇总 | 测试集预测 | 计算 RMSE、R²、Harmonic-Score，按模型×窗口×粒度做宏平均 | 结果表 | 回答 RQ1-RQ4 |

### 4.3 模型结构或系统模块

| 模型 | 功能/结构要点 | 输入输出 | 与其他模块关系 |
|---|---|---|---|
| Mean 基线 | 用训练窗均值作为预测窗每个点的预测 | 序列 → 常数预测 | 最低性能门槛参照 |
| GRU / LSTM | 1 层 RNN，隐层 100，batch 16，lr 0.01，100 epochs | 窗口 → 未来值 | 简单循环基线 |
| GRU-FCN / LSTM-FCN | RNN + 全卷积（FCN）混合；LSTM-FCN 三层 CNN 尺寸 128-256-128，GRU-FCN 为 64-128-64 | 窗口 → 未来值 | 检验卷积增强的收益 |
| InceptionTime | 多尺度卷积网络（标准预定义结构），batch 128，lr 0.001，20 epochs | 窗口 → 未来值 | 图像/时序分类架构迁移代表 |
| ResNet | 残差网络（标准结构），batch 128，lr 0.01，20 epochs | 窗口 → 未来值 | 深层网络迁移代表 |
| RCLSTM | 随机连接 LSTM，隐层 300，batch 32，100 epochs；超参取自原论文 | 窗口 → 未来值 | 轻量化循环变体代表 |

### 4.4 公式、算法和机制解释

- RMSE（Eq. 1）：√(1/N · Σ(y_i − ŷ_i)²)，0→∞，越小越好，对单个大误差敏感。
- R²（Eq. 2）：1 − Σ(y−ŷ)² / (Σ(y−μ_y)² + ε)，−∞→1，越大越好，反映趋势拟合程度。
- Harmonic-Score（Eq. 3）：2·RMSE·|R²−1| / (RMSE + |R²−1|)。由于两者量纲不同，先把 RMSE 上截到 11、R² 下截到 −10（覆盖结果分布的中心 95% 以抑制离群点），再用调和平均强调"两个指标同时好"的模型。
- 归一化与滑窗：MinMax 只在训练集拟合；窗口按预测窗长度前移，形成重叠样本以增加训练样本多样性（Fig. 2）。

### 4.5 方法优势

- 首个在 CESNET-TimeSeries24 上的系统性基准，规模大（1,318,320 个最终模型）、流程可复现、代码与结果公开。
- 覆盖 3 个聚合粒度 × 18 个指标 × 5 组窗口 × 8 个模型，给出多维度证据而非单一榜单。
- 用 Mean 基线暴露"简单方法也能在 R² 上胜过深度模型"这一反直觉现象（Table 5 总体均值：Mean 0.0173，所有 DL 模型为负）。

### 4.6 方法不足

- 只做单变量建模（每个指标单独建模），未评估多变量模型；作者把"单变量 vs 多变量"列为开放问题（§8）。
- 缺失值一律填 0，虽便于检测中断，但会引入偏差（§5.1、§8）。
- 每个序列单独训练模型，计算与运维成本极高（1.3M 模型），实际部署不可行（§8 挑战 1）。
- 论文聚焦 7 个模型，Transformer 系（Informer/Autoformer/ETSformer）只在相关工作讨论、未纳入评测（§2）。
- 评测用 1 小时聚合与单步/多步预测，未涉及跨时间漂移（仅以 24 周测试集间接体现）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

本文是基准对比研究而非新方法：它不提出新架构，而是把统计方法→RNN→FCN 混合→ResNet/InceptionTime→Transformer 这条演进链中的代表模型放在同一真实数据集、同一预处理与调参流程下比较。与既有评测（多为各自数据集、各自预处理）相比，其区别在"统一真实数据 + 统一方法学 + 公开代码"。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 真实 ISP 大规模基准 | 1,318,320 个模型覆盖 3 粒度 × 18 指标 × 5 窗口 | 高 | 是（可迁移到其他 ISP/时序数据集） |
| 组合指标 Harmonic-Score | 调和平均 + 截断，兼顾 RMSE 与 R² 且抑制离群 | 中 | 是（任何双指标评测都可借鉴） |
| 缺失率-精度定量结论 | IP 级缺失率与 R² 负相关 −0.69 | 中 | 是（作为数据质量筛选依据） |
| 效率测量口径 | 归一化的训练/预测时间（每 100 数据点，秒） | 中 | 是（部署可行性评估模板） |

### 5.3 适用场景

适合 ISP/运营商侧的中长期容量规划与资源调度：机构级、量类指标（flows/packets/bytes）用 GRU 或 GRU-FCN 即可；对频繁重训或算力受限场景选 GRU-FCN；对 IP 级细粒度预测，论文提示需要更强的预处理或专门架构，现有模型普遍失效（R² 为负）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文结论 |
|---|---|---|---|
| GRU / LSTM | 精度最好、跨预测窗最稳定 | 训练较慢（4.2-5.3 s/100 点） | 总体宏平均最佳（GRU Harmonic 0.14838） |
| GRU-FCN | 训练/预测最快（1.196/0.065 s per 100 点），机构级最优 | IP 级长预测窗场景明显掉分（744/168 达 0.22075） | 精度-效率折中最佳 |
| LSTM-FCN | 子网级精度最佳 | 效率逊于 GRU-FCN | 可用但不占优 |
| InceptionTime | 多尺度特征 | 全部指标最差、长窗崩溃（R² 低至 −9.22） | 不推荐用于流量预测 |
| ResNet | 残差训练稳定 | 精度次差、训练最耗时之一 | 不推荐 |
| RCLSTM | 参数量少的轻量循环 | 训练最慢（最高 16.287 s/100 点） | 单步 R² 有亮点，总体一般 |
| Mean 基线 | 极简、R² 最高（总体 0.0173） | 无季节性建模能力 | 深度模型的 R² 全体为负，被基线"打脸" |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- 数据：CESNET-TimeSeries24 的 1 小时聚合序列；建模 18 个指标，共 1,831 条时间序列（283 机构 + 548 子网 + 1000 IP）。
- 规模：8 个模型（含均值基线）× 5 组窗口 × 18 指标 × 1,831 序列 = 1,318,320 个最终模型（§6.1）。
- 训练环境：MetaCentrum（NGI/EGI）统一机型，每次运行 4 个独占 CPU（§6.2）。
- 重复性：主对比为单次大规模网格；最终超参由各部分随机 50 条序列的平均表现确定（§5.3）。
- 论文正文详报 Number of bytes（传输数据量）指标，其余指标在 GitHub 补充材料。

### 6.2 数据集

| 数据集 | 规模/结构 | 时间跨度 | 备注 |
|---|---|---|---|
| CESNET-TimeSeries24 | 283 机构、548 机构子网、>270,000 IP；18 个指标；10 min/1 h/1 day 三种聚合 | 40 周（2023-10 至 2024-07） | 本文使用 1 小时聚合、全部 18 指标；由同课题组 [7] 发布 |

指标含 n_flows、n_packets、n_bytes、n_dest_ip、n_dest_ports、n_dest_asn、tcp_udp_ratio_packets/bytes、dir_ratio_packets/bytes、avg_duration、avg_ttl（Table 1）。

### 6.3 Baseline

本文的"基线"即被比较的 7 个深度模型本身，外加一个非学习 Mean 基线（训练窗均值外推）。未与统计方法（ARIMA/SARIMA/ETS）实测对比，仅在相关工作讨论其局限。

### 6.4 评价指标

RMSE（Eq. 1）、R²（Eq. 2）、Harmonic-Score（Eq. 3，RMSE 截断 11、R² 截断 −10 后取调和平均）；效率侧报告归一化到每 100 数据点的训练与预测时间（秒，Table 7）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| 全粒度总体（Number of bytes） | Harmonic 总均值（越低越好） | GRU 0.14838 | InceptionTime 0.46035 / Mean 0.21408 | GRU 比 InceptionTime 低 0.312 | LSTM 0.14875、LSTM-FCN 0.1501、GRU-FCN 0.15245（Table 6） |
| 全粒度总体 | RMSE 总均值 | GRU 0.1696 | Mean 0.5179 / InceptionTime 0.332 | 比 Mean 低 0.348 | LSTM 0.1701、LSTM-FCN 0.1707（Table 4） |
| 全粒度总体 | R² 总均值 | Mean 0.0173（唯一为正） | GRU −0.2887 | — | 全部 DL 模型 R² 为负（Table 5） |
| 三个粒度分层 | Harmonic 均值 | 机构 0.135-0.152 | 子网 0.170-0.190、IP 级 0.130-0.300 | — | 越细粒度越难（Table 6） |
| 训练/预测效率 | 秒/100 数据点 | GRU-FCN 1.196 / 0.065（机构） | RCLSTM 11.371-16.287 / 0.286-0.303 | 训练快约 9-14 倍 | GRU 4.249、LSTM 5.327、ResNet 6.369（Table 7） |
| 缺失率相关性 | 皮尔逊相关 | IP 级 −0.69（缺失比例 vs R²） | — | — | 机构级缺失最少、精度最高（§6.1） |

### 6.6 优势最明显的场景

- GRU/LSTM：所有设置下预测稳定性最好（跨预测窗退化最小），适合作为 ISP 侧默认模型。
- GRU-FCN：训练与推理都最快，适合需频繁重训或算力受限的部署（§6.2、Table 7）。
- 机构级 + 量类指标（n_flows/n_packets/n_bytes）：季节性明显，模型普遍学得动（§6.1 末段）。

### 6.7 局限性

- 论文坦言"没有任何模型在所有设置下都最优"（RQ1）；精度对实验条件高度敏感。
- R² 为负说明多数 DL 模型在细粒度/多步预测上并不比均值基线更会把握趋势；作者解释为数据缺乏强季节性、离群多（RQ2 讨论）。
- 单变量逐序列建模在真实运维中不可扩展（§8 挑战 1、2）。
- 未测跨时间漂移、未纳入 Transformer 实测、未与统计基线对比。

---

## 7. 学习与应用

### 7.1 是否开源？

是。论文正文明确写出模型与实验源码发布在 GitHub（脚注 2/4）。解析稿在转换过程中丢失了脚注 URL，经从 PDF 抽取正文确认仓库地址为 `https://github.com/koumajos/isp-forecasting-benchmark`（已填入 frontmatter 的 `code`）。所有结果与补充分析亦在该仓库。

### 7.2 复现关键步骤

1. 下载 CESNET-TimeSeries24（10 分钟原始聚合），构造 1 小时序列，选定 18 个指标与三个数据集部分。
2. 缺失值填 0，按 35%/5%/60%（14/2/24 周）切分；仅用训练段拟合 MinMax。
3. 按 (24,1)、(168,1)、(168,24)、(744,1)、(744,168) 五组窗口做滑动切分。
4. 对每个模型跑超参搜索（RNN 层数 1-5、隐层 20-200、batch、lr、epoch），再用 Table 3 的最终超参全量训练与测试。
5. 按 Table 4-7 口径汇总 RMSE / R² / Harmonic-Score 与训练/预测时间，复核粒度与指标分层结论。

### 7.3 关键超参数、预处理和训练细节

最终超参（Table 3）：GRU/LSTM/LSTM-FCN 均为 1 层、隐层 100、batch 16、lr 0.01、100 epochs；GRU-FCN 为 4 层、隐层 20、batch 16、lr 0.01、20 epochs（CNN 三层 64-128-64）；InceptionTime/ResNet 用官方结构，batch 128，lr 0.001/0.01，20 epochs；RCLSTM 1 层隐层 300、batch 32、100 epochs。归一化 MinMax、损失 MSELoss、优化器 Adam。多数模型最终只用 1 层 RNN——作者指出这与 Zeng et al. "简单模型可胜 Transformer" 的结论一致（§5.3）。

### 7.4 能否迁移到其他任务？

- 评测方法学（真实数据 + 统一预处理 + 统一调参 + 效率测量 + 组合指标）可直接迁移到任何时序预测基准研究。
- Harmonic-Score 的构造（量纲对齐 + 截断 + 调和平均）可作为多指标评审模板。
- 结论层面："机构/聚合级可预测、IP 级不可预测、缺失率是头号杀手"可迁移到任何细粒度网络遥测（如 per-device 流量、加密流量速率预测）的数据质量评估。

### 7.5 对我的研究有什么启发？

- 加密流量分析领域同样面临"数据集不一致导致结果不可比"的问题；本文的"统一真实数据 + 公开代码 + 覆盖多维度变量"的基准套路是可借鉴的对抗性证据生产模式。
- Mean 基线在 R² 上压倒全部深度模型，提醒在流量类任务中必须报告强基线（与加密流量领域的"浅层模型优于深度表征"结论同构）。
- 缺失率与精度的定量相关（−0.69）提示：在细粒度流量任务里，数据质量指标（缺失率）应作为实验设计的显式控制变量。

---

## 8. 总结

### 8.1 核心思想

> 真实 ISP 数据上，简单循环模型胜过复杂架构。

### 8.2 速记版 Pipeline

1. 取 CESNET-TimeSeries24 的机构/子网/IP 三部分，按 1 小时聚合、逐指标单变量建模。
2. 缺失值填 0，35%/5%/60% 划分，仅训练集拟合 MinMax。
3. 以 24/168/744 训练窗与 1/24/168 预测窗组合做滑动切分。
4. 统一调参后训练 GRU/LSTM/GRU-FCN/LSTM-FCN/ResNet/InceptionTime/RCLSTM 与 Mean 基线。
5. 用 RMSE、R²、Harmonic-Score 与训练/预测时间按粒度与指标汇总，得出 GRU 总体最优、GRU-FCN 折中最佳。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[anomaly-detection]]：流量预测被明确用于异常缓解与资源规划，是该任务的支撑性时序技术。

### 9.2 相关方法

- [[transformer]]：论文在相关工作讨论了 Transformer 系预测模型（Informer/Autoformer/ETSformer）并引用了"简单线性模型可胜 Transformer"的结论，但未将其纳入实测。

### 9.3 相关任务

- [[anomaly-detection]]：本文预测服务的目标场景之一（作者把异常检测列为后续方向）。

### 9.4 可更新的综述页面

- 现有综述页（加密流量分析 / 小样本 / 恶意流量 / 流量基座模型 / WF）均不覆盖"网络流量预测"，暂不更新。

### 9.5 可加入的对比表

- [[dataset-comparison-table]]：论文系统使用并推广了 CESNET-TimeSeries24 这一真实 ISP 时序数据集，可作为细粒度、长时间跨度的数据集条目。
- [[open-source-registry]]：代码与全部实验结果开源。

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 规模：8 模型 × 5 窗口 × 18 指标 × 1,831 序列 = 1,318,320 个模型 | 实验设置 | §6.1 |
| GRU 总体宏平均最准（Harmonic 0.14838），InceptionTime 最差（0.46035） | 全粒度汇总 | §6.1, Table 6 |
| 全部深度模型的 R² 总均值为负，Mean 基线（0.0173）反而最优 | R² 汇总 | §6.1, Table 5 |
| 训练窗越大精度越低、预测窗越长误差累积越重 | RQ2 结论 | §7 RQ2, Table 4-6 |
| IP 级缺失比例与 R² 相关系数 −0.69；机构级最准、IP 级最差 | 粒度分析 | §6.1, Table 6 |
| GRU-FCN 训练/预测最快（1.196 s / 0.065 s per 100 点，机构级），RCLSTM 最慢（最高 16.287 s） | 效率测量 | §6.2, Table 7 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-TNSM-Comparative_Analysis_of_Deep_Learning_Models_for_Real-World_ISP_Network_Traffic_Forecasting.pdf
- MinerU Markdown：02-parsed-markdown/2026-TNSM-Comparative_Analysis_of_Deep_Learning_Models_for_Real-World_ISP_Network_Traffic_Forecasting.md

---

## 12. 后续问题

- 解析稿未给出 DOI、卷期与 arXiv 编号；正式出版信息待补（任务分配记录的 arXiv 2503.17410 为预印本编号，未写入 frontmatter）。
- 解析稿在缺引文编号处出现 `missing values [?]`，且脚注中的 GitHub 地址丢失，已从 PDF 抽取补齐；后续若做引用统计需回查 PDF。
- 未评测 Transformer 系与统计基线（ARIMA/SARIMA），"简单模型胜出"的结论在更广模型谱系上的稳健性未知。
- 与该知识库的加密流量任务交叉点：能否把该基准方法学照搬到加密流量的速率/流量预测（如隧道流量时序）尚待验证。

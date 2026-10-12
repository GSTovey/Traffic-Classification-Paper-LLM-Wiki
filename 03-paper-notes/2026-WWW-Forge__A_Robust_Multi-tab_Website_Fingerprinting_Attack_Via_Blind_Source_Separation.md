---
type: paper
title_original: "Forge: A Robust Multi-tab Website Fingerprinting Attack Via Blind Source Separation"
title_cn: "Forge：基于盲源分离的鲁棒多标签页网站指纹攻击"
authors: ["Yitan Huang", "Wei Qiao", "Ding Wang", "Meng Shen", "Di Zhao", "Linxu Li", "Susu Cui", "Bo Jiang", "Zhigang Lu", "Baoxu Liu"]
year: 2026
venue: "ACM Web Conference 2026 (WWW'26)"
doi: unknown
url: "https://doi.org/10.1145/3774904.3792410"
pdf: "00-inbox/PDFs/2026-WWW-Forge__A_Robust_Multi-tab_Website_Fingerprinting_Attack_Via_Blind_Source_Separation.pdf"
mineru_md: "02-parsed-markdown/2026-WWW-Forge__A_Robust_Multi-tab_Website_Fingerprinting_Attack_Via_Blind_Source_Separation.md"
status: deep-analyzed
reading_level: L3
research_area: ["website-fingerprinting", "encrypted-traffic-analysis", "Tor traffic analysis"]
task: ["multi-tab website fingerprinting", "open-world WF", "defense/noise robustness"]
method: ["blind source separation", "time-delay embedding", "iterative correction network", "dual-domain attention"]
dataset: ["WFLib closed/open-world", "defense-enabled WFLib", "dynamic tab/defense mixtures", "synthetic packet-loss/jitter/reordering"]
code: "https://github.com/Carm3nc1ta/FORGE"
relevance: medium
created: "2026-09-29"
updated: "2026-10-10"
---

# Forge: A Robust Multi-tab Website Fingerprinting Attack Via Blind Source Separation

> **L3 深度分析笔记**：基于正文 §1–§6、Tables 1–6、Figures 1–10、附录数据集/噪声/参数与开源说明交叉核对。论文的“未知标签数”是方法设计目标；在具体训练和评测中仍需按数据集与动态混合方式解释，不能把所有结果理解为完全无先验的开放世界识别。

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Forge: A Robust Multi-tab Website Fingerprinting Attack Via Blind Source Separation |
| 中文标题 | Forge：基于盲源分离的鲁棒多标签页网站指纹攻击 |
| 作者 | Yitan Huang、Wei Qiao、Ding Wang、Meng Shen、Di Zhao、Linxu Li、Susu Cui、Bo Jiang、Zhigang Lu、Baoxu Liu |
| 年份 | 2026 |
| 会议/期刊 | ACM Web Conference 2026 (WWW'26) |
| 研究方向 | 多标签页网站指纹、Tor 加密流量分析、WF 防御鲁棒性 |
| 任务类型 | 多标签页多标签识别、开放世界 WF、未知标签页数、噪声/防御环境识别 |
| 方法关键词 | Takens 时间延迟嵌入、8 通道虚拟观测、BSS 深度展开、Iterative Correction Module、Dual-Domain Consistency Attention |
| 数据与规模 | WFLib 闭世界/开放世界、多种防御数据、动态标签页/防御混合、0.1%–10% 丢包/抖动/乱序噪声 |
| 是否开源 | 是：https://github.com/Carm3nc1ta/FORGE |
| DOI | 10.1145/3774904.3792410 |
| PDF | 00-inbox/PDFs/2026-WWW-Forge__A_Robust_Multi-tab_Website_Fingerprinting_Attack_Via_Blind_Source_Separation.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-WWW-Forge__A_Robust_Multi-tab_Website_Fingerprinting_Attack_Via_Blind_Source_Separation.md |

## 1. 一句话总结
> Forge 将多标签页 WF 从“直接多标签分类”重构为“先盲源分离、后网站识别”：在闭世界 2–5 tab、开放世界、防御、动态和噪声场景中，分别用时延嵌入构造虚拟观测、BSS solver 分离混合源、DDCA 识别网站。

## 2. 摘要原文

While Tor’s strong anonymity shields users’ privacy, it also enables malicious activities, motivating attacks that bypass its protections. Website Fingerprinting (WF) has emerged as a primary threat in this domain. However, existing WF methods struggle with realistic multi-tab browsing scenarios, often relying on prior knowledge of the number of open tabs and lacking robustness against network noise and defenses. To address these challenges, we propose Forge, a robust WF attack framework inspired by the classic cocktail party problem. Forge reframes multi-tab WF as Blind Source Separation, decomposing mixed traffic into individual signals without requiring a predefined number of concurrent tabs. A robust website identifier then classifies separated components using dual-domain attention across time and frequency. Across WFLib open-world, defense-enabled and dynamic datasets, Forge improves MAP over the state-of-the-art average by 78.6% in the challenging multi-tab open-world setting.

## 3. 方法分析

### 3.1 研究问题与核心假设

Forge 针对三个现实缺口：混合流量导致单站点特征交织；大多数多标签模型假设已知 tab 数；防御注入、时序噪声和动态场景使直接组合分类失稳。作者的核心假设是：多标签 WF 更接近信号处理的 cocktail-party/BSS 问题，先把混合流量拆成潜在网站流，再对每个分量识别，比直接记忆标签组合更可泛化。

### 3.2 输入—处理—输出

| 步骤 | 输入 | 具体操作 | 输出 |
|---|---|---|---|
| Traffic Channel Construction | 单一 Tor 混合 packet direction/timestamp 序列 | 在窗口 τ 内统计上/下行包数、方向内时间间隔、上/下行 burst 数和平均 burst 长度，形成 8 维状态向量 | 8×T 虚拟多通道状态序列 |
| BSS Solver | 虚拟观测 V | 由 L 个 Iterative Correction Module 组成的深度展开网络，残差卷积/归一化/非线性/池化逐级修正混合源 | 多个分离的 website-like stream |
| Website Identifier | 分离分量 | Transformer 编码器 + 时间/频率双域一致性注意力（DDCA）融合序列依赖与 FFT magnitude 特征 | 每个分量的网站概率/标签 |
| Multi-label aggregation | 分离结果与标签 | 对有效分量汇总网站集合；动态场景不要求预先给出真实 tab 数 | 监控网站集合和置信度 |

### 3.3 方法优势与不足

- **优势**：把 tab 数未知转化为源分离问题；DDCA 用频域残留抵消时域 padding/插包干扰；在防御、噪声和 tab-count mismatch 下保持较高 AUC/MAP。
- **不足**：BSS 在单观测下本质欠定，8 个虚拟通道依赖 Takens 嵌入和手工统计；分离结果未提供独立的物理可验证源；开放世界把未监控网站合成单类标签，不能说明细粒度未知站点识别；防御和噪声主要是 WFLib/作者模拟分布。

## 4. 实验表现

### 4.1 数据集与基线

- WFLib 闭世界：Alexa Top 100，2–5 tab；开放世界：100 个 monitored sites 加 Alexa 101–20,000 的 unmonitored pool，未监控站点合并为一类。
- 防御集：WTF-PAD、Front、Walkie-Talkie、TrafficSliver，以及作者从 2-tab 闭世界构造的 Random、RegularTor-Light/Heavy。
- 动态集：40% 2-tab、30% 3-tab、20% 4-tab、10% 5-tab 的 tab-count 混合；另有 WTF-PAD/Front defense 混合。
- 噪声集：对 2-tab 流量注入 0.1%、0.5%、1%、2%、5%、10% 的丢包、时间抖动和局部乱序。
- 七个基线：AWF、DF、Tik-Tok、RF、BAPM、ARES、TMWF；单标签方法按作者附录改造成多标签分类。

### 4.2 关键结果

| 场景 | Forge 结果 | 证据 |
|---|---|---|
| 闭世界 2/3/4/5-tab | F1=0.8124/0.7871/0.7900/0.7666 | Table 2 |
| 开放世界 2-tab | MAP@5=0.8782，较其他方法平均 +35.9% | Table 3 |
| 开放世界 5-tab | MAP@5=0.8181，较平均 +78.6%；AUC≈0.98 | Table 3, Fig. 6 |
| 防御 Random/Front/WTF-PAD | AUC=0.9848/0.9996/0.9998 | Table 4 |
| RegularTor-Light/Heavy | AUC=0.9486/0.9357，MAP@k 仍高于基线 | Table 4 |
| 动态 tab-count / defense | AUC=0.9848/0.9986 | Table 5 |
| 噪声 | 10% 噪声下 AUC 仍 >0.9 | §5.6, Fig. 9 |
| 消融 | 移除 BSS solver，MAP@2 从 0.8640 降至 0.4114（约 −52.4%）；移除时延嵌入降至 0.7889；移除 DDCA 降至 0.8034 | Table 6 |

### 4.3 评价指标与解释

多标签结果使用 AUC、P@K、MAP@K 以及 Precision/Recall/F1。论文强调在高 tab 数下 F1 比单看 precision 更能反映漏检；开放世界将未监控站点合并为一个未知类，因此开放世界 AUC/MAP 不能解释为识别每个未监控网站的细粒度能力。

## 5. 局限性与复现建议

- BSS 的输入只有一条混合观测；8 个虚拟通道来自手工方向/时间/burst 特征，Takens 嵌入并不能在所有混合过程下保证真实源的唯一可辨识性。
- 训练和评测仍使用 WFLib 的 monitored-site 标签组合；“不预设 tab 数”主要在动态混合和分离模块层面体现，不等于完全无训练先验。
- defense/noise 结果依赖 WFLib 防御与附录模拟器；10% 丢包/抖动/乱序之外的真实 ISP 队列、Tor 路径变化、长期概念漂移未测。
- 论文报告了单次数据集结果、固定网络结构与参数敏感性，未提供跨随机种子置信区间或跨地域外部验证。
- 复现需获取 WFLib、作者 GitHub、PyTorch 2.4.1/Python 3.10.5，按附录固定窗口、序列长度、随机种子和噪声操作顺序（loss→jitter→reordering）。

## 6. 知识链接
- [[website-fingerprinting]]
- [[encrypted-traffic-analysis]]
- [[traffic-classification]]

## 7. 证据状态
- 正文证据已核对至 §1–§6、Tables 2–6、Figures 4–10 与附录 B/F。
- DOI 为 10.1145/3774904.3792410；代码仓库为 https://github.com/Carm3nc1ta/FORGE。
- MinerU 存在小标题 small-caps 碎裂和个别表格实体丢失；关键数值以正文表格抄录，未监控站点合并为一类的口径已单独标注。



## 8. 详细方法与机制

### 8.1 Time-Delay Embedding

原始观测是带方向和时间戳的单流序列，BSS 经典条件却需要多观测通道。Forge 在长度 τ 的历史窗口中计算八个统计量：上行包数、下行包数、上行相邻时间间隔总和、下行相邻时间间隔总和、上行 burst 数、下行 burst 数、上行平均 burst 长度和下行平均 burst 长度。沿时间滑窗堆叠后得到 8×T 的虚拟观测矩阵 V。该步骤保留方向和局部时间结构，但其“虚拟独立通道”是特征构造而非真实传感器。

### 8.2 BSS Solver

Solver 将经典迭代 BSS 写成 L 个级联 Iterative Correction Module。第 l 个模块对当前估计 H^(l) 做 Conv1d+BatchNorm+ReLU 的残差特征提取，再用第二组卷积合成修正 ΔH，执行 H^(l+1)=PostProcess(H^(l)+ΔH)，并通过池化/Dropout 逐级扩大感受野。最终输出多个潜在源流，不需要把真实 tab 数作为输入参数。

### 8.3 Dual-Domain Consistency Attention

Website Identifier 给每个分离流加入可学习位置嵌入，Transformer 编码器的 DDCA 同时处理时间和频率视图：时间分支用 self-attention 捕获序列依赖；频率分支对信号做 FFT，只保留 magnitude spectrum，以减弱时移/抖动；两支通过门控残差（论文默认门控参数约 0.1）融合。其设计假设是 padding/插包主要破坏时域，而频域仍残留站点加载节奏。

### 8.4 训练与推理

所有基线改为多标签分类并使用统一数据分割。Forge 的输出经过每个分离分量的网站识别后汇总为网站集合。动态数据中 tab 数按 40/30/20/10% 混合；开放世界把 unmonitored pool 合并为单一未知类；论文没有将未知站点进一步细分。

## 9. 学习与应用

### 9.1 是否开源？

作者提供 GitHub 仓库 https://github.com/Carm3nc1ta/FORGE。复现还需要 WFLib 数据、附录中防御/噪声生成脚本和相同版本的 PyTorch/Python；代码可用不等于 WFLib 所有数据都能无条件再分发。

### 9.2 复现关键步骤

1. 准备 WFLib 2–5 tab 闭世界、开放世界和防御数据，保留 packet direction/timestamp。
2. 固定时间窗口 τ、8 维状态特征、序列长度和 PyTorch 版本，生成 8×T 虚拟观测。
3. 训练级联 ICM BSS solver 与 DDCA identifier，按附录固定随机种子、噪声操作顺序和防御参数。
4. 分别报告 closed/open-world AUC、P@K、MAP@K、Precision/Recall/F1，不能用单一 F1 替换所有指标。
5. 在未知 tab-count、未知 defense 和 0.1%–10% 噪声下重复评估，记录每一模块消融。

### 9.3 能否迁移到其他任务？

“先分离、后识别”可以迁移到混合会话流、应用复用隧道或多设备共享链路，但前提是能从单观测构造有用的虚拟通道，且源流在统计上有可分性。DDCA 的时频交叉验证可用于其他具有 padding/节奏扰动的加密流量分类；BSS 输出的源数与网站标签不应直接当作真实用户 tab 数。

### 9.4 对我的研究有什么启发？

Forge 的主要方法论价值是把多标签流量任务拆成“结构恢复”和“语义识别”两个阶段，并用消融证明 BSS solver 是主要增益来源（去掉后 MAP@2 约降 52.4%）。对现有 WF 研究，需同时报告 tab-count mismatch、开放世界未知类、defense/noise 和源分离误差，而不是只在理想闭世界单一 tab 上比较分类器。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 将多标签 WF 重构为 BSS，不要求预先知道 tab 数 | cocktail-party 动机与贡献 | §1, §3 |
| 8 个虚拟通道来自方向、时间间隔和 burst 统计 | Time-Delay Embedding | §4.1 |
| BSS Solver 由级联 ICM 进行残差迭代修正 | ICM update 公式与架构 | §4.2 |
| DDCA 联合时间 self-attention 与 FFT magnitude 频域注意力 | Dual-Domain Consistency Attention | §4.3, Fig. 3 |
| 2–5 tab 闭世界 F1 分别为 0.8124/0.7871/0.7900/0.7666 | closed-world Table 2 | §5.2, Table 2 |
| 开放世界 5-tab MAP@5=0.8181，较其他方法平均 +78.6% | open-world Table 3 | §5.3, Table 3 |
| Random/Front/WTF-PAD AUC=0.9848/0.9996/0.9998 | defense Table 4 | §5.4, Table 4 |
| 动态 tab-count/defense AUC=0.9848/0.9986 | dynamic Table 5 | §5.5, Table 5 |
| 10% 丢包/抖动/乱序下 AUC 仍 >0.9 | noise curve | §5.6, Fig. 9 |
| 去掉 BSS solver，MAP@2 0.8640→0.4114；去掉 DDCA 0.8640→0.8034 | ablation Table 6 | §5.7, Table 6 |
| 代码开源于 GitHub | Availability | §1 |

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-WWW-Forge__A_Robust_Multi-tab_Website_Fingerprinting_Attack_Via_Blind_Source_Separation.pdf
- MinerU Markdown：02-parsed-markdown/2026-WWW-Forge__A_Robust_Multi-tab_Website_Fingerprinting_Attack_Via_Blind_Source_Separation.md
- DOI：https://doi.org/10.1145/3774904.3792410
- 代码：https://github.com/Carm3nc1ta/FORGE

## 12. 后续问题

1. 8 个虚拟通道在不同站点组合和真实 Tor 路径下是否满足 BSS 的独立性/可分性要求？
2. 开放世界把所有 unmonitored 网站合并为一类，若改为未知站点逐站拒识，Forge 的 FPR/召回会如何变化？
3. DDCA 对频域 magnitude 的增益来自哪些防御类型，是否在非 padding 的流量整形下仍成立？
4. BSS 输出分量是否能被稳定映射到真实 tab，还是只作为分类中间表征？
5. 模型是否跨日期、浏览器、Tor circuit 和网站内容更新保持性能，概念漂移下是否需要再训练？

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

论文先指出多标签 WF 仍把混合流量当成一个多标签分类样本，导致 tab 数先验和组合记忆依赖；防御和网络噪声进一步让这种做法失稳。作者用 cocktail-party 类比完成转折：真实问题应先拆分混合信号，再识别每个源。Forge 因此用 Takens 时延嵌入把单观测升成虚拟多通道，用深度展开 BSS solver 逐步分离，再用 DDCA 在时域和频域交叉验证站点指纹。实验按闭世界→开放世界→防御→动态→噪声→消融递进，把“能分离、能泛化、能抗扰动”的叙事逐层兑现，并用去掉 BSS 的大幅退化作为结构性证据。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 角色 | 关键转折 |
|---|---|---|---|
| Introduction | 建立多标签混合、tab 先验和噪声三重矛盾 | 问题框定 | 从分类转向分离 |
| Related Work | 对比单 tab、多 tab、WF defenses | 定位差异 | 现有方法共享直接分类范式 |
| Threat Model/Motivation | 给出被动本地 adversary 与 cocktail-party 类比 | 直觉桥接 | 混合网站流=多源信号 |
| Forge Design | 依次介绍虚拟通道、BSS、DDCA | 方法主体 | separate-then-identify |
| Evaluation | 六个 RQ 从准确性到噪声和消融 | 证据递进 | BSS 去除造成最大损失 |
| Conclusion | 回到未知 tab 和防御鲁棒性 | 收束 | 方法价值来自问题重构 |

### 13.3 Gap 展开方式

| Gap | 具体内容 | 论证方式 |
|---|---|---|
| 任务范式 | 多 tab 被当成直接多标签分类 | cocktail-party/BSS 重构 |
| 先验依赖 | 已知 tab 数不现实 | BSS 输出源数与动态混合 |
| 防御鲁棒 | 时域 padding 破坏时序特征 | DDCA 频域 magnitude 交叉验证 |
| 评估真实性 | 理想闭世界掩盖部署困难 | WFLib open/defense/dynamic/noise 组合 |

### 13.4 实验叙事方式

| 环节 | 作用 |
|---|---|
| Closed-world | 建立基本多 tab 性能和 tab 数扩展趋势 |
| Open-world | 测未知站点拒识与长尾组合 |
| Defenses | 验证频域残留是否提供抗 padding 能力 |
| Dynamic | 验证训练/测试 tab 数和 defense 不一致 |
| Noise | 将真实网络伪影转成可控强度曲线 |
| Ablation | 证明 BSS、时延嵌入、DDCA 各自贡献 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移写法 |
|---|---|---|
| 类比 | 用 cocktail-party 把抽象混合问题变成直觉 | 用一个物理类比引出问题重构，但随后给出形式化映射 |
| 模块顺序 | 按“观测构造→分离→识别”叙述 | 让 pipeline 顺序与论文贡献顺序一致 |
| 结果分级 | 将基础准确性、抗防御、动态和噪声分开 | 每个部署风险对应一个独立 RQ |
| 局限表达 | 通过未知类合并、BSS 欠定等边界控制外推 | 说明指标高的条件与未覆盖的真实变量 |

## 14. 证据边界与复现清单

1. **BSS 可辨识性**：单混合流通过 8 个统计通道后并不自动满足独立源条件；论文结果证明的是模型在 WFLib 分布上的识别性能，不是一般 BSS 唯一分解定理。
2. **未知 tab 数口径**：Forge 不把 tab 数作为分离器输入，但训练、标签空间和动态混合集仍来自预先定义的 monitored sites/组合；不能写成无任何先验的通用开放世界攻击。
3. **开放世界口径**：所有未监控网站被合并为共同标签，AUC/MAP 反映 monitored-vs-unknown 与集合预测，不反映未知站点逐站识别。
4. **鲁棒性口径**：Random/Front/WTF-PAD/RegularTor、0.1%–10% 噪声均为 WFLib 或作者模拟配置；未覆盖所有真实 Tor relay、浏览器版本、拥塞和概念漂移。
5. **指标口径**：闭世界表格的 F1、开放世界的 MAP@K/AUC、动态的 AUC 和防御的 MAP@K 不能横向当作同一性能指标。
6. **复现**：需固定 WFLib 版本、PyTorch 2.4.1/Python 3.10.5、窗口 τ、序列长度默认约 8000、随机种子以及 loss→jitter→reordering 噪声顺序；代码仓库与数据许可需分别核对。

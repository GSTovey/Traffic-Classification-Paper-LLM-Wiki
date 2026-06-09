---
type: paper
title_original: "Causality Correlation and Context Learning Aided Robust Lightweight Multi-Tab Website Fingerprinting Over Encrypted Tunnel"
title_cn: "因果关联与上下文学习辅助的鲁棒轻量级多标签加密隧道网站指纹识别"
authors:
  - Siyang Chen
  - Shuangwu Chen
  - Huasen He
  - Xiaofeng Jiang
  - Jian Yang
  - Siyu Cheng
year: 2024
venue: "INFOCOM 2024"
doi: ""
url: ""
pdf: "00-inbox/PDFs/2024-INFOCOM-Causality_Correlation_and_Context_Learning_Aided_Robust_Lightweight_Multi-Tab_Website_Fingerprinting_Over_Encrypted_Tunnel.pdf"
mineru_md: "02-parsed-markdown/2024-INFOCOM-Causality_Correlation_and_Context_Learning_Aided_Robust_Lightweight_Multi-Tab_Website_Fingerprinting_Over_Encrypted_Tunnel.md"
status: processed
reading_level: L2
research_area: ["网站指纹识别", "多标签", "加密流量", "鲁棒性"]
task: ["网站指纹识别"]
method: ["causality-learning", "context-learning", "random-forest"]
dataset: []
code: "https://github.com/chenxiailian/robustweb"
relevance: high
created: "2026-05-27"
updated: "2026-05-29"
---

# 0. 元信息

| 字段 | 内容 |
|------|------|
| 论文标题 | Causality Correlation and Context Learning Aided Robust Lightweight Multi-Tab Website Fingerprinting Over Encrypted Tunnel |
| 作者 | Siyang Chen, Shuangwu Chen, Huasen He, Xiaofeng Jiang, Jian Yang, Siyu Cheng |
| 机构 | 中国科学技术大学；合肥综合性国家科学中心人工智能研究院 |
| 会议/期刊 | IEEE INFOCOM 2024 |
| 关键词 | website fingerprinting, multi-tab, causality correlation, context learning, encrypted tunnel, robustness |
| 代码/数据 | https://github.com/chenxiailian/robustweb |

# 1. 研究动机与问题定义

## 1.1 研究背景

用户越来越多地使用 Tor、VPN、SSH、V2ray 等隐私增强技术来加密传输内容并隐藏通信关系。然而，被动窃听者仍可通过 encrypted tunnel 中的侧信道信息（packet size、time、directions）实施 website fingerprinting (WF) 攻击，推断用户访问的具体网站。

## 1.2 核心问题

现有 WF 方法在真实 multi-tab 浏览场景中面临以下关键挑战：

- **C1 - Transmission Concealment**：由于通过加密代理中继连接，目标 IP 固定为代理地址，不同网站的流量封装在同一 flow 中，无法通过 IP 或 packet inspection 区分。
- **C2 - Open-World Noise**：用户可能访问监控列表之外的网站，这些未知网站的流量对 WF 模型构成干扰，可能被误分类为已知网站。
- **C3 - Dynamic Network Conditions**：网络拥塞、CDN 差异路径等导致 packet loss、duplication 和 disorder，破坏从静态训练集学到的固定序列模式。
- **C4 - Multi-tab Websites Concurrency**：多标签并发访问使不同网站的 packet sequence 交织重叠，且标签数量动态变化，无法预先确定。

## 1.3 研究目标

开发一种轻量级且鲁棒的 WF 模型 RobustWF，能够适应不确定数量的并发标签和动态网络环境变化。

# 2. 核心思想与方法概述

RobustWF 的核心思想基于两个关键观察：

1. **Causality 关系**：用户请求与网站响应之间存在因果关系，浏览器通过独立 session 请求不同资源，同一 session 中的交互 packets 可形成 causality chain。
2. **Context 依赖**：完整网页由多个资源组成，不同 causality chain 之间存在上下文依赖关系，整体结构比细节更稳定。

RobustWF 采用六步流水线架构：(1) RF-labeling → (2) Packet Size Filtering → (3) Causality Correlation → (4) Causality Chains Construction → (5) Context Learning → (6) Website Recognition。

# 3. 方法详解

## 3.1 RF-labeling（随机森林初步标注）

利用 Random Forest 对 packet sequence 进行粗粒度网站标注。以 packet size 频率分布 $F = [f_1, f_2, \cdots, f_K]$ 作为特征，随机选取 H 个特征和 I 个样本构建决策树，重复 Q 次形成随机森林。决策树输出的 top-ranking labels $\tilde{Y}$ 作为候选网站。该步骤无需预先知道标签数量。

## 3.2 Packet Size Filtering（包大小过滤）

定义两个指标评估 packet size 对目标网站的指示性：

- **Frequency** $Fre_m^{s_i}$：该包大小在目标网站所有训练样本中的出现频率
- **Confidence** $Con_m^{s_i}$：包含该包大小的训练样本比例

保留低频率（排除 MTU、ACK 等通用包）且高 confidence（具有代表性）的包大小，构建 screen list $S_m$，过滤掉与目标网站无关的 packets。

## 3.3 Causality Correlation（因果关联）

使用 Average Causal Effect (ACE) 衡量包大小之间的因果关联：

$$ACE(s_i, s_j) = P(s_j|s_i) - P(s_k|s_i, k \neq j)$$

在关联窗口 W 内，若 ACE 超过阈值 $\theta$，则建立因果关联模板 $\langle s_i, s_j \rangle$（$s_i$ 为因，$s_j$ 为果）。仅作为因而不作为果的包大小被视为 root cause。

## 3.4 Causality Chains Construction（因果链构建）

给定因果关联模板 $T_m$，将子序列 $P_m$ 解耦为一系列 causality chains：

1. 对每个 root cause，在 $P_m$ 中找到对应 packets
2. 根据模板寻找关联结果
3. 在关联窗口内将关联 packet 追加到链中
4. 递归执行直至链终止

最终得到因果链列表 $C(P_m) = [c_1, c_2, \ldots, c_L]$，每条链代表目标网站一个 session 的建立、传输和终止过程。短链可被移除。

## 3.5 Context Learning（上下文学习）

使用 Transformer 捕获 causality chains 之间的依赖关系：

- **归一化**：用固定参数 w 和 v 对变长因果链进行裁剪/填充，得到矩阵 $E \in \mathbb{R}^{w \times v}$
- **嵌入**：引入额外的 $x_{class}$ 向量拼接于链矩阵前，加上 position embedding $E_{pos}$
- **Transformer 编码**：h 层堆叠编码器，每层包含 Multi-head Self-Attention (MSA) 和 MLP，配合 Layer Normalization 和 Residual Connection
- **输出**：$Z_h^0$（更新后的 $x_{class}$）学习到因果链间的上下文依赖

**鲁棒性来源**：off-chain packet 的 loss/duplication/disorder 不影响因果链构建；on-chain packet 的 duplication 仅增加冗余链不改变模式；on-chain packet 的 loss/disorder 使部分链缺失，但 context learning 依赖整体结构而非单条链。

## 3.6 Website Recognition（网站识别）

对每个 RF 给出的候选标签 m，将其因果链列表输入 Transformer 获得特征向量 $Z_h^0$，通过 MLP 进行细粒度识别：

$$\hat{y} = MLP(Z_h^0)$$

若 $\hat{y}_m = 1$ 则确认访问了网站 m。整个模型为统一的集成模型，无需为每个网站或每种标签数量训练单独模型。

# 4. 实验设置

## 4.1 数据集

| 数据集 | 描述 | 规模 |
|--------|------|------|
| SSH70 | SSH 加密隧道，2000 网站中筛选 70 个 | 70 网站 |
| OpenVPN40 | 自建 OpenVPN 隧道，Alexa 中国 Top 40 域名 | 40 网站，每站 100 次 |
| Monkey500 | 移动网站流量，500 网站 | 500 网站，每站 50 实例 |

## 4.2 Baseline 方法

| 方法 | 特征/模型 | 特点 |
|------|-----------|------|
| CUMUL (Multi-CUMUL) | 104 统计特征 + SVM | 经典单标签方法改造 |
| APPscanner (Multi-APPscanner) | 54 统计特征 + RF | 上下游及双向流量统计 |
| DF (Multi-DF) | CNN 深度学习 | 自动学习序列特征 |
| BAPM | CNN + Attention | 块注意力 profiling，固定标签数 |
| ARES | 每网站独立 Transformer | 动态标签数，但模型数量随网站增长 |

## 4.3 评估指标

- **单标签**：Accuracy, Macro-Precision, Macro-Recall, Macro-F1 Score
- **多标签**：Accuracy, Jaccard score（衡量预测结果与真实结果的相似度）

# 5. 实验结果与分析

## 5.1 Closed-World 单标签场景

RobustWF 在三个数据集上的 F1-Score 均最优：SSH70 为 0.919，OpenVPN40 为 0.981，Monkey100 为 0.981。DF 表现也较好，说明 CNN 能有效捕捉序列依赖。APPscanner 和 CUMUL 在不同数据集上波动较大，表明统计特征难以泛化到不同加密隧道。

## 5.2 Open-World 单标签场景

加入 400 个未知网站作为 open-world noise 后，RobustWF 的 Precision/Recall/F1 均达到 98.1%，性能几乎不变。而其他方法 F1 显著下降（DF 从 0.944 降至 0.866，ARES 从 0.824 降至 0.728），因为它们可能将 open-world noise 误分类为已知网站。RobustWF 通过 RF-labeling 与 context learning 结果的一致性评估来减少误识别。

## 5.3 动态重叠比例（2-tab）

在 0%-50% 重叠比例下，RobustWF 在两个 tab 上的准确率均超过 85%，显著优于 baselines。第 1 个 tab 的准确率高于第 2 个 tab，因为 flow 头部对 WF 更关键。基于序列特征的方法（RobustWF、BAPM、ARES、Multi-DF）随重叠增加性能下降，而基于统计特征的方法（Multi-CUMUL、Multi-APPscanner）几乎不受影响。

## 5.4 动态标签数量（2-5 tab + dynamic）

RobustWF 在所有标签数量（包括动态变化）上 Jaccard score 均最优。2-tab 时为 0.71，5-tab 时降至 0.47，dynamic-tab 为 0.57。通过结合统计特征（RF-labeling）和序列特征（Transformer）的一致性评估来降低 false positives。

## 5.5 鲁棒性：动态网络条件

在 packet loss/duplication/disorder 比例从 10% 到 50% 的实验中：
- **Packet loss**：RobustWF 在 loss ratio 达 12% 前 Jaccard score 保持在 0.5 以上，最大降幅不超过 7%（0%-15% 范围内）
- **Packet duplication**：RobustWF 在 duplication ratio 达 15% 时仍保持 0.6 的 Jaccard score，表现最稳定
- **Packet disorder**：RobustWF 从 0.58 降至 0.53（disorder ratio 15%），降幅最小

ARES 在 loss 和 duplication 下性能显著下降，因其为每个网站训练独立二分类器，packet 扰动同时影响所有分类器。Multi-APPscanner 基于统计特征，几乎不受影响。

## 5.6 监控网站数量的影响

随着监控网站从 100 增至 500，所有方法 Jaccard score 均下降。RobustWF 从 0.70 降至 0.61，始终保持最优。ARES 训练时间成本显著高于其他方法（每网站一个模型），而 RobustWF 使用统一集成模型，时间成本可接受。

# 6. 与现有工作的对比

论文 Table III 系统对比了各方法对 C1-C4 挑战的应对能力：

| 能力 | 传统方法 | BAPM | ARES | **RobustWF** |
|------|----------|------|------|-----------|
| C1 Transmission Concealment | 部分支持 | 支持 | 支持 | 支持 |
| C2 Open-World Noise | 部分支持 | 支持 | 支持 | 支持 |
| C3 Packet Loss | 多数不支持 | 不支持 | 不支持 | **支持** |
| C3 Packet Duplication | 不支持 | 不支持 | 不支持 | **支持** |
| C3 Packet Disorder | 不支持 | 不支持 | 不支持 | **支持** |
| C4 Multi-tab | 不支持/固定标签数 | 固定标签数 | 动态标签数 | **动态标签数** |

RobustWF 是唯一同时应对所有四个挑战的方法。

# 7. 主要贡献

1. 提出 **causality correlation 机制**，将交织的多网站 packets 解耦为 causality chains，缓解混合流量的信息混淆
2. 设计 **context learning 方法**，聚合因果链间的上下文关联，捕获目标网站的整体结构，增强对 packet loss/duplication/disorder 的鲁棒性
3. 构建 **轻量级统一模型**，无需为每个网站或每种标签数量训练独立模型，适应动态变化
4. 在三个加密流量数据集上验证了 RobustWF 相比 SOTA 方法在准确率（提升 14%）和鲁棒性上的优势

# 8. 局限性与未来方向

论文在 Conclusion 中指出，未来工作将关注当各种 **traffic defense measures**（流量防御措施）被应用时模型的改进。论文未深入讨论：
- 对抗 WF 防御（如 traffic morphing、padding）的鲁棒性
- TLS 1.3 等新协议的影响
- 实时部署的计算效率和延迟

# 9. 关键公式总结

| 公式 | 含义 |
|------|------|
| Eq.(1) Frequency & Confidence | 评估 packet size 对目标网站的指示性 |
| Eq.(2) ACE | 衡量包大小间的 Average Causal Effect |
| Eq.(3) 条件概率估计 | 基于共现频率估计因果概率 |
| Eq.(4) Transformer 输入 | 因果链矩阵 + 位置嵌入 |
| Eq.(5) 编码器层 | MSA + MLP + LayerNorm + Residual |
| Eq.(6) 网站识别 | MLP 对融合特征进行分类 |

# 10. 关键技术细节

- **特征选择**：仅使用 packet size 和 direction（受 C1 约束），不依赖 IP、port、domain name
- **关联窗口 W**：定义因果关联的最大距离，窗口外的包被认为无关
- **随机森林的作用**：不仅用于初步标注，还通过无需预知标签数量的特性解决了 C4 中标签数量不确定的问题
- **Transformer 的 $x_{class}$**：随机初始化且无语义，公平聚合所有链的特征，提供网站整体结构的综合表示
- **双重一致性验证**：RF-labeling（统计特征）与 Transformer（序列特征）的结果一致性评估，有效降低 open-world noise 的误识别

# 11. 相关工作脉络

| 阶段 | 代表方法 | 特点 |
|------|----------|------|
| 传统统计特征 | CUMUL, APPscanner, k-fingerprinting | 手工特征提取，效率低 |
| 深度学习 | DF (CNN), SDAE, LSTM, Var-CNN | 自动特征学习，但单标签假设 |
| 多标签-流量分割 | Wang et al., Xu et al. | 找分离点，仅识别首个标签 |
| 多标签-分块分类 | Cui et al., BAPM | 分段/分块投票，需预知标签数 |
| 多标签-独立模型 | ARES | 每网站独立 Transformer，计算开销大 |
| **RobustWF** | 本文方法 | 统一模型 + causality + context，鲁棒且轻量 |

# 12. 个人评价与启发

- **方法创新性**：将因果推断（causality）思想引入 WF 领域，通过 request-response 的因果关系解耦混合流量，思路新颖且符合浏览器加载网页的实际机制
- **鲁棒性设计**：利用整体结构（context）而非细节特征进行识别，天然抵抗 packet 级别的扰动，设计哲学值得借鉴
- **实用性**：统一模型避免了为每个网站/标签组合训练独立模型的工程负担，更适合真实部署
- **可扩展性思考**：该方法依赖 packet size 分布的稳定性，若网站采用 traffic morphing 或动态内容变化，packet size 的区分度可能下降
- **对后续研究的启发**：causality chain 的构建方式可推广到其他需要从混合流中解耦子流的场景，如 encrypted traffic 中的应用识别

---
type: paper
title_original: "LotBoNC: Novel Botnet Traffic Classification under Long-tailed Distributions"
title_cn: "LotBoNC：长尾分布下的新型僵尸网络流量分类"
authors: ["Huancheng Hu", "Ziyun Li", "Christian Doerr"]
year: 2026
venue: "ACM AsiaCCS 2026"
doi: "10.1145/3779208.3785276"
url: "https://doi.org/10.1145/3779208.3785276"
pdf: "00-inbox/PDFs/2026-AsiaCCS-LotBoNC__Novel_Botnet_Traffic_Classification_under_Long-tailed_Distributions.pdf"
mineru_md: "02-parsed-markdown/2026-AsiaCCS-LotBoNC__Novel_Botnet_Traffic_Classification_under_Long-tailed_Distributions.md"
status: processed
reading_level: L2
research_area: ["malicious-traffic-detection", "encrypted-traffic-analysis", "traffic-classification", "traffic-representation-learning"]
task: ["malicious-traffic-detection", "traffic-classification"]
method: ["contrastive-learning", "self-supervised-learning", "pre-training-finetuning"]
dataset: ["IoT-23", "ISCX-Bot-2014 (ISCX-2014)", "CTU-13", "CTU-MALWARE-CAPTURE", "VNAT", "ISCX-VPN-2016", "Ton-IoT"]
code: "https://github.com/watsonhuhpi/LotBoNC"
relevance: high
created: "2026-09-19"
updated: "2026-09-19"
---

# LotBoNC: Novel Botnet Traffic Classification under Long-tailed Distributions

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | LotBoNC: Novel Botnet Traffic Classification under Long-tailed Distributions |
| 中文标题 | LotBoNC：长尾分布下的新型僵尸网络流量分类 |
| 作者 | Huancheng Hu（Hasso Plattner Institute & University of Potsdam）、Ziyun Li（KTH Royal Institute of Technology）、Christian Doerr（Hasso Plattner Institute & University of Potsdam） |
| 年份 | 2026 |
| 会议/期刊 | ACM Asia Conference on Computer and Communications Security (AsiaCCS 2026), June 1–5, 2026, Bangalore, India |
| 研究方向 | 加密恶意流量分类；开世界新类发现（NCD）；长尾学习 |
| 任务类型 | 已知僵尸网络多分类 + 未标注流量中新僵尸网络家族发现（open-world, long-tailed） |
| 方法关键词 | burst 级 2-byte bigram tokenization、masked token 预训练 + InfoNCE 对比预训练（仅 dropout 增强）、熵正则化最优传输（Sinkhorn-Knopp）伪标签、EM 式原型/先验动量更新、原型损失 + 实例对比损失 + 监督对比损失 |
| 数据集 | 预训练：CTU-MALWARE-CAPTURE、VNAT、ISCX-VPN-2016、Ton-IoT；评估：IoT-23、ISCX-Bot-2014 (ISCX-2014)、CTU-13 |
| 是否开源 | 是：https://github.com/watsonhuhpi/LotBoNC（`§1` 正文给出；解析稿该 URL 因换行被拆为 "watsonhu hpi"） |
| PDF | 00-inbox/PDFs/2026-AsiaCCS-LotBoNC__Novel_Botnet_Traffic_Classification_under_Long-tailed_Distributions.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-AsiaCCS-LotBoNC__Novel_Botnet_Traffic_Classification_under_Long-tailed_Distributions.md |

---

## 1. 一句话总结

> 面向"未标注流量长尾 + 新僵尸网络家族稀疏出现"的开世界场景，用自监督预训练 + 熵正则化最优传输伪标签 + EM 式原型/先验迭代，在三个僵尸网络数据集上将稀有新类发现准确率最高提升 19.4 个百分点。

---

## 2. 摘要翻译

### 2.1 摘要原文

Botnets are a persistent cyber threat, leveraging global infrastructures to launch large-scale attacks. Yet, most existing classification methods are evaluated under balanced and closed-set assumptions, which fail to capture real-world conditions. In practice, botnet traffic is both long-tailed and open-world: unknown variants continually emerge, and rare threats are buried under dominant traffic, often evading detection. To reflect real-world conditions, we define a deployment-oriented setting where unlabeled traffic follows a long-tailed distribution, with dominant known classes in the head and rare novel botnet variants in the tail. We propose LotBoNC, a unified framework for encrypted traffic classification under long-tailed open-world conditions. LotBoNC first performs self-supervised pre-training to learn transferable representations, then applies entropy-regularized optimal transport to assign pseudo-labels aligned with estimated class priors. An EM-style loop iteratively refines prototypes and priors, improving class separation between frequent and rare categories. We evaluate LotBoNC on three public encrypted traffic datasets with diverse long-tailed scenarios. LotBoNC consistently outperforms prior state-of-the-art methods and accurately classifies known botnets and discovers unseen botnet variants in diverse, imbalanced open-world scenarios.

### 2.2 摘要中文翻译

僵尸网络是持续存在的网络威胁，借助全球基础设施发起大规模攻击。然而，现有大多数分类方法都在平衡、闭集假设下评估，无法反映真实条件。实践中僵尸网络流量同时具有长尾与开世界特性：未知变种不断出现，稀有威胁被主流流量淹没、难以被检测。为反映真实条件，本文定义了一个面向部署的设置：未标注流量服从长尾分布，头部是占主导的已知类别，尾部是稀有的新僵尸网络变种。我们提出 LotBoNC——一个面向长尾开世界条件的加密流量分类统一框架。LotBoNC 首先做自监督预训练以学习可迁移表征，然后用熵正则化最优传输分配与估计类别先验对齐的伪标签；EM 式循环迭代精化原型与先验，改善频繁类与稀有类的可分性。我们在三个公开加密流量数据集上以多种长尾场景评估 LotBoNC，其在多样、不平衡的开世界场景中持续优于先前 SOTA，既能准确分类已知僵尸网络、又能发现未见过变种。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 真实部署中僵尸网络流量有**两个叠加特性**：未见变种持续涌现（开世界）、类别频率高度不平衡（长尾）；网络流中混杂良性流、已知僵尸网络与稀有未知家族（`§1`, Figure 1）。
- 这种结构带来两个耦合挑战：(i) 无监督情况下未知类难以检测；(ii) 长尾分布使模型偏向头部类，稀有未知僵尸网络被误判为已知恶意类甚至良性流量（`§1`）。

### 3.2 现有方法的痛点和不足

- 现有加密流量分类方法（含 ET-BERT、NetMamba 等）假设**所有类别预先已知、标签充分**，在闭集/平衡类设置下评估（`§1`、`§3`）。
- 已有新类发现（NCD）工作（如 RoNeTC）**未考虑类别不平衡**，无法应对真实网络的极端长尾（`§1`、`§2.2`）。
- 半监督/伪标签方法在噪声预测下脆弱，往往**放大对多数类的偏置**；重加权/过采样等长尾方法又假设标签完整可得（`§3`）。

### 3.3 论文的研究假设或核心直觉

核心直觉：若把伪标签分配建模为**带类别先验约束的最优传输问题**（而不是逐样本 argmax 或阈值化），伪标签就会按估计的类先验成比例分配，从而天然抵抗长尾塌缩；再用 EM 式循环不断精化原型与先验，即可在持续改进已知类分类的同时把尾部新类"分离"出来（`§4.4`、`§4.5`）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 真实网络流中已知僵尸网络（Mirai、Mozi、Gafgyt 等）占据绝大多数已标注流量，新家族稀疏且无标注，埋没在尾部 | §1, Figure 1 |
| 痛点提炼 | 闭集/平衡假设下的分类器把稀有未知僵尸网络误判为已知恶意类或良性流量，直接漏检 | §1 |
| 问题转化 | 形式化为"标注集平衡、仅未标注集长尾"的联合已知/未知类学习（NCD + long-tail）问题，并给出可量化的长尾构造参数 γ | §1, §4.1, §5.1 |
| 文献定位 | NCD、长尾学习、开集识别各自有进展，但没有工作同时满足"加密 + 无标签 + 长尾 + 多类发现"，属被忽视的交叉空白 | §2.2, §2.3, §3 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 与估计类先验对齐的熵正则化 OT 伪标签（E-step）+ 原型与先验的动量精化（M-step）能在长尾开世界设置下同时保持已知类精度与尾部新类发现能力 | §4.4–§4.5（OT 的边际约束防止塌向头部类） | 三数据集 × γ∈{1,5,10} 实验（Table 2） |
| 辅助假设 | 自监督预训练（masked token + dropout 增强对比）是长尾新类发现的关键；无预训练时尾部性能显著下降 | §4.3（多源预训练提供可迁移表征）；§5.7.2 | 预训练消融（Table 5） |
| 辅助假设 | 仅用 encoder dropout 作为增强（不做输入级扰动）即可保证尾部类结构不被破坏 | §4.2（尾部类样本稀有且结构脆弱） | dropout 消融（Table 6） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | IoT-23 在 γ=10 时 unlabelled-aware 60.01 vs 最强基线 RoNeTC 45.30；三项指标总体领先（Overall 96.93） | §5.5, Table 2 |
| 预训练必要性 | 支撑 | unlabelled-agnostic：IoT-23 w/ 88.20 vs w/o 74.21（γ=1）、56.05 vs 47.82（γ=10） | §5.7.2, Table 5 |
| dropout 增强 | 支撑 | IoT-23 整体准确率 p=0 时 58.2/61.3/63.5，p=0.10 时 89.9/91.3/92.9，p=0.50 回落至 70.1/71.5/72.3（γ=1/5/10） | §5.7.5, Table 6 |

---

## 4. 方法设计

### 4.1 方法整体流程

LotBoNC = **自监督预训练**（burst 级 masked token 重建 + InfoNCE 对比，多源数据）→ **EM 式长尾新类发现**：E-step 用熵正则化最优传输在类别先验约束下给未标注样本分配软伪标签；M-step 用原型损失训练并动量更新原型与类先验；每步同时叠加实例级对比损失（未标注）与监督对比损失（已标注）。训练目标 `L_overall = L_ins + λ_proto·L_proto + λ_sup·L_sup`（`§4.7`, Eq. 13, Algorithm 1）。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 分词 | 原始会话流量 | 按"同一 TCP/UDP 流内、时间连续、同方向"的包序列切分为 burst；去除低层协议头，拼接剩余 payload，切为固定 2-byte bigram token，加 [CLS]/[SEP]/[MASK]/[PAD] | token 序列 X=[x1..xT] | burst 级结构近似应用层边界，比原始包序列更结构化（`§4.2`） |
| Step 2 预训练 | 四数据集 token 序列（每包取以太网层后 64 字节） | masked token 交叉熵重建（Eq. 1）+ 两次独立 dropout 前向得到正对的 InfoNCE 对比（Eq. 2） | 预训练编码器 f_θ | 学习可迁移的上下文表征（`§4.3`） |
| Step 3 E-step | 未标注批次 + 估计先验 r | softmax 预测 P → K=exp(−logP/η)，Sinkhorn-Knopp 迭代求 α、β，得伪标签矩阵 A（Eq. 3–5） | 软伪标签 A | 按类先验比例分配伪标签，抵抗长尾塌缩（`§4.4`） |
| Step 4 M-step | A、未标注/已标注批次 | 原型损失 L_proto（含 −log p_k 先验修正项，Eq. 6）；动量更新类先验 r 与原型 c_k（Eq. 7–9） | 更新后的 θ、原型、先验 | 精化类结构与先验估计（`§4.5`） |
| Step 5 表征改善 | 未标注/已标注数据 | 未标注：dropout 双视图 InfoNCE（Eq. 10–11）；已标注：监督对比损失 L_sup（Eq. 12） | 实例级可判别表征 | 保持实例级判别力、提升类内紧致度（`§4.6`） |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 分词器（burst + 2-byte bigram） | 把加密会话转为 token 序列 | 原始 pcap 流 | token 序列 | 供预训练与微调共用（`§4.2`） |
| Masked token 预训练头 | 重建被掩 token | 损坏序列 x̃ | 各位置 token 分布 | 预训练阶段与对比目标联合（`§4.3.1`） |
| InfoNCE 对比头 | 对齐同一实例两个 dropout 视图 | 视图对 (h, h′) | 对比损失 | 预训练（Eq. 2）与微调（Eq. 10）两处复用 |
| OT 伪标签模块（E-step） | 先验约束下分配软伪标签 | P、先验 r、均匀 w | 传输矩阵 A | 输出供 M-step 使用（`§4.4`） |
| 原型/先验记忆（M-step） | 动量维护每类原型 c_k 与先验 r_k | 置信分配样本 | 更新后的 c_k、r_k | 同时反过来约束下一轮 E-step 的 r（`§4.5`） |

> 解析稿未给出编码器网络的具体层数/维度（如是否为标准 Transformer 骨干），只给出 f_θ 的抽象记号；token 设定（[CLS]/[SEP]/[MASK]）与引用 [12, 37]（BERT/ET-BERT）表明其为 BERT 式掩码建模范式。

### 4.4 公式、算法和机制解释

- **E-step（Eq. 3）**：min_{A∈Π(r,w)} ⟨A, −log P⟩ − ηH(A)，其中 Π(r,w) 约束列和 = 类先验 r、行和 = 样本分布 w；η 控制熵正则强度。用 Sinkhorn-Knopp 迭代（Algorithm 1 第 8–13 行）求解 A = diag(α)·K·diag(β)，K = exp(−log P/η)。
- **M-step（Eq. 6）**：L_proto = −Σ_i Σ_k A_ik [log softmax(v_iᵀc_k) − log p_k]，减 log p_k 是**先验修正项**，惩罚对高频类的过度自信；Appendix A.1 给出从 EM 下界（Jensen 不等式）到该损失的完整推导（Eq. 15–23）。
- **先验/原型动量更新（Eq. 7–9）**：先验 r_k ← μr_k + (1−μ)z_k，z_k 为预测类计数占比；原型 c_k ← μc_k + (1−μ)·（置信分配样本嵌入均值）。每 epoch 更新一次。
- **聚合熵正则的直觉**：OT 的边际约束让伪标签"按先验配额"分配，避免 argmax 式伪标签全部倒向头部类（`§4.4`）。

### 4.5 方法优势

- 首次把"标注平衡 + 未标注长尾"的部署式设置形式化，并把 NCD 与长尾/开世界结合到加密流量（`§1`，三点贡献）。
- OT + 先验对齐从机制上抑制伪标签塌缩，是相对 RoNeTC 等开集方法的核心差异（`§5.5`, Table 2）。
- 仅用 dropout 增强，避免输入级扰动破坏尾部类结构（`§4.2`, `§5.7.5`）。
- 代码开源（`§1`）。

### 4.6 方法不足

- 需要预先知道未标注集的**类别总数 K**（含未知类），真实部署中未知家族数量本身未知（`§4.1`、`§5.6` 中 K 由实验设定；论文未讨论 K 估计误差的影响）。
- 依赖估计先验，先验估计不准时 OT 分配会系统性偏移（论文用动量更新缓解，但未给先验误差敏感性实验）。
- 训练流程含预训练 + EM 循环 + 三个损失项，超参（λ_proto、λ_sup、μ、η）较多。
- 未讨论对加密协议版本/时间漂移的鲁棒性。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

主流加密流量分类（ET-BERT、NetMamba、DeepTraffic 等）是**闭集监督分类**：只优化已知类判别边界，未标注数据不参与或仅做简单伪标签；开集方法（RoNeTC）能识别"未知"，但不建模未知类的**结构**，也不处理长尾。LotBoNC 的差别在于：把未标注数据的伪标签分配显式建模为先验约束下的最优传输，并用 EM 循环同时更新原型与先验，从而在长尾下**发现并分离多个新类**（`§2.2`–`§2.3`, `§4.4`–`§4.5`）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 部署式长尾开世界设置 | 标注集平衡、未标注集按 γ=n_k/n_u 长尾（γ∈{1,5,10}），未知类只出现在尾部 | 高 | 是（任意"标注少 + 未知多"的流量分析场景） |
| 熵正则化 OT 伪标签（E-step） | 用类先验 r 作为列边际约束分配伪标签，防头部类塌缩 | 高 | 是（半监督/新类发现通用组件） |
| EM 式原型 + 先验动量精化 | 每 epoch 更新 c_k、r_k，形成闭环 | 中 | 是 |
| 仅 dropout 的对比增强 | 不做输入级扰动，保护稀有尾部类结构 | 中 | 是（长尾/脆弱样本场景） |
| 多源预训练（4 数据集） | CTU-MALWARE-CAPTURE + VNAT + ISCX-VPN-2016 + Ton-IoT | 中 | 是 |

### 5.3 适用场景

- 安全运营中心/CERT 场景：已有部分标注的已知僵尸网络家族，需要从每天涌入的未标注流量中发现新的、罕见的家族（`§6` 明确限定在合规环境部署）。
- 数据集层面适合"已知类样本充足、未知类极稀有"的监控环境。
- 不适合：完全无标注的纯聚类场景、类别数未知且无法估计的场景。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 1DCNN / LSTM-Att / TSCRNN | 端到端、实现简单 | 无预训练、无未知类机制；长尾下 unlabelled 指标 <31% | 引入预训练 + OT 伪标签 |
| DeepTraffic | 图像化表征、对恶意样本有效 | 闭集分类，长尾未知类下 unlabelled-aware 仅 21.57–65.03 | 同上 |
| ET-BERT | 掩码预训练 + 强少样本迁移 | 无未知类发现机制；γ=10 时 unlabelled-agnostic 仅 19.24（IoT-23） | 在预训练之上叠加 OT/原型 EM |
| NetMamba | 线性时间序列建模、时延低 | 已知类精度高（99.34）但新类发现弱（γ=10 UA 32.93） | 同上 |
| RoNeTC（最强基线） | 开集导向、多视图包表征 + 不确定性估计 | 长尾下退化严重（γ=10 UA 45.30/38.14/42.91） | 用先验约束 OT 显式建模尾部新类结构 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- 每个数据集构造两个不相交划分：标注集只含已知家族且类平衡（分层采样）；未标注集含已知 + 未知家族，且**只在未标注集上施加长尾**（隔离不平衡效应）（`§5`, `§5.1`）。
- 长尾构造：类样本数 n_i = max(n_min, ⌊n_max·γ^{i−1}⌋)，γ = n_k/n_u ∈ {1, 5, 10}（指数衰减）；另用 LDAM 式 step-decreasing 分布做形状消融（`§5.1`, `§5.7.1`）。
- 另设标注类数/未标注类数比 ρ = C_L/C_U ∈ {0.5, 1, 2} 实验（`§5.6`）。
- 结果取 5 个随机种子平均（`§5.4`）。
- 评测指标（`§5.4`）：Overall（全部样本）、Labelled（已知类）、Unlabelled-Aware（假定新类与已知类已理想分离，测聚类-类对齐，匈牙利算法）、Unlabelled-Agnostic（不做该假定，对全部未标注样本聚类评估）。

### 6.2 数据集

- 预训练：CTU-MALWARE-CAPTURE（3.25×10^8 flows）、VNAT（3.17×10^6）、ISCX-VPN-2016（2.80×10^6）、Ton-IoT（2.0×10^5）（Table 1）。
- 训练/评估：IoT-23（20 种恶意类型 + 3 条良性参考，>30GB）、ISCX-2014（10 天企业流量、7 个僵尸网络家族、50.0M flows）、CTU-13（13 个僵尸网络活动、147.3M 包 ≈ 1.3M 标注 flows）（`§5.1`）。
- 预处理：重建双向流、丢弃非 IP 控制流量、仅保留 ≥5 包的 TCP/UDP 记录（`§5.1`）。
- > ⚠️ MinerU 解析问题：Table 1 的 fine-tuning 列 flow 数与正文描述不一致（表内 IoT-23 3.25×10^6 / ISCX-Bot-2014 3.17×10^5 / CTU-13 2.80×10^6 与 pre-training 行的 CTU-MAL-CAP、VNAT、ISCX-VPN-2016 数量呈"错位重复"形态），引用时以正文描述为准。

### 6.3 Baseline

1DCNN、LSTM-Att、TSCRNN、DeepTraffic、ET-BERT、NetMamba、RoNeTC（开集导向的多视图包表征 + 不确定性估计），共 7 个（`§5.2`）。

### 6.4 评价指标

Overall / Labelled / Unlabelled-Aware / Unlabelled-Agnostic 四项准确率（%），均值为 5 seed 平均（`§5.4`, Eq. 14；ACC 用匈牙利算法做最优一对一匹配）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| IoT-23, γ=1 | Overall | 94.48 | 91.34 (RoNeTC) | +3.14 | Table 2 |
| IoT-23, γ=1 | Unlabelled-Aware | 90.42 | 86.50 (RoNeTC) | +3.92 | Table 2 |
| IoT-23, γ=10 | Unlabelled-Aware | 60.01 | 45.30 (RoNeTC) | +14.71 | 与贡献声称的 +14.7 一致 |
| ISCX-2014, γ=10 | Unlabelled-Aware | 57.55 | 38.14 (RoNeTC) | +19.41 | 贡献声称的最高 +19.4 |
| CTU-13, γ=10 | Unlabelled-Aware | 60.15 | 42.91 (RoNeTC) | +17.24 | 贡献声称的 +17.2 |
| IoT-23, γ=10 | Overall / Labelled | 96.93 / 99.93 | 94.66 (RoNeTC) / 99.65 | +2.27 / +0.28 | Table 2 |
| IoT-23, ρ=0.5 | Overall / UA | 83.56 / 75.73 | — | — | ρ 实验，Table 3 |
| IoT-23, ρ=2 | Overall / UA | 94.41 / 92.59 | — | — | 标注类越多、潜空间越结构化 |

注：γ=1（平衡）时 LotBoNC 的 Unlabelled-Agnostic 指标（88.20）低于 RoNeTC（91.45），论文将其归因于指标假设差异，并强调随着不平衡加剧优势扩大（`§5.5`）。

### 6.6 优势最明显的场景

- **极端长尾 + 新类发现**：γ=10 时 unlabelled-aware 全面领先（+14.7 ~ +19.4），基线"腰斩"（45.30/38.14/42.91）而 LotBoNC 保持 57–60（`§5.5`, Table 2）。
- 类别分布恢复：γ∈{1,5,10} 下 LotBoNC 的类级预测分布明显比 DeepTraffic 更贴近真实长尾（`§5.5`, Figure 7）。
- ρ=0.5（每 2 个未标注类仅 1 个标注类）时标注子集准确率仍 >98.5（`§5.6`）。
- t-SNE 上头部类与尾部类边界比 DeepTraffic 更清晰（`§5.5`, Figure 6）。

### 6.7 局限性

- Unlabelled-Agnostic 指标在 γ=1 时未超过 RoNeTC（88.20 vs 91.45），"理想分离假定"与实际聚类质量存在差距（`§5.5`）。
- 消融部分数据存在内部不一致（见 §12 与 JSON `mineru_issues`）：`§5.7.2` 正文引用的"w/o pre-train"数值与 Table 5 不一致；Table 4/5/6 的绝对数值与 Table 2 不同量级（如表 4 IoT-23 γ=1 Overall 89.88 vs Table 2 的 94.48），论文未说明口径差异。
- `§5.3` 称预训练"排除加密 payload 内容"，与 `§4.2` 的 payload bigram 分词相互矛盾（见 §12）。

---

## 7. 学习与应用

### 7.1 是否开源？

是。`§1` 给出 Source code: https://github.com/watsonhuhpi/LotBoNC；`§6` 称将在发表后发布相关代码与脚本（解析稿中该 URL 被换行拆成 "watsonhu / hpi"）。

### 7.2 复现关键步骤

1. 按 burst 定义切分流：同 TCP/UDP 流内、时间连续、同方向的包构成 burst；去头后拼接 payload，切 2-byte bigram token（含 [CLS]/[SEP]/[MASK]/[PAD]）。
2. 在四个预训练集上训练 masked token + InfoNCE（每包截断为以太网层后 64 字节；Adam，lr 1e-5，batch 64，580,000 步，线性衰减 + warmup 0.1）。
3. 构造长尾划分：标注集类平衡采样；未标注集按 n_i = max(n_min, ⌊n_max·γ^{i−1}⌋) 生成，γ∈{1,5,10}。
4. 微调：lr 2e-5、weight decay 1e-4、τ=0.5、dropout 0.1、batch 32；跑 EM 循环（Sinkhorn 求 A → 原型损失 + 对比损失反传 → 每 epoch 动量更新 r_k、c_k）。
5. 评测四项准确率，5 seed 取均值。

### 7.3 关键超参数、预处理和训练细节

- 预训练：每包 64 字节；lr 1e-5；batch 64；580,000 步；warmup ratio 0.1；线性衰减（`§5.3`）。
- 微调：lr 2e-5；weight decay 1e-4；温度 τ=0.5；dropout 0.1；batch 32（`§5.3`）。
- 损失权重：λ_proto=0.7 在所有指标上最优（扫 {0.1,0.3,0.5,0.7,1.0}，`§5.7.3`, Figure 8）；dropout p=0.10 最优（扫 {0, 0.05, 0.10, 0.50}，`§5.7.5`, Table 6）。
- > ⚠️ MinerU 解析问题：`§5.7.2` 正文的部分数值（如 60.21→75.73、52.18→68.27、58.34→72.86 与 77.82→92.59 等）与 Table 5 实际数值（88.20/74.21 等）对不上，疑似正文引用了另一版本表格；引用请以 Table 5 为准。

### 7.4 能否迁移到其他任务？

- **OT + 先验约束的伪标签分配**是通用半监督组件，可迁移到任意"已知类标注充分、未知类稀有"的流量分析任务（如恶意软件家族发现、IoT 设备类型发现）。
- 仅 dropout 增强的对比学习适合样本结构脆弱/稀有的场景（尾部类、少样本类）。
- burst 级 2-byte bigram tokenization 可直接复用到其他加密流量表征工作。
- EM 式原型/先验循环与具体的编码器解耦，可套在任何骨干网络上。

### 7.5 对我的研究有什么启发？

- 长尾 + 开世界的评测协议（只对未标注集施加长尾、标注集保持平衡）值得在恶意流量检测评测中直接借用，比常规"整体长尾"更能隔离不平衡因素。
- "四项指标"（Overall/Labelled/UA/UAA）把已知类精度与新类发现质量分开度量，可作为长尾/开集工作的评测模板。
- OT 伪标签的边际约束思路可解释为"用先验配额防塌缩"，比 class-balanced loss 更显式；可作为对抗标签噪声/分布漂移的手段。

---

## 8. 总结

### 8.1 核心思想

> 用先验约束的最优传输伪标签 + EM 原型精化，在长尾开世界中同时分类已知与发现新僵尸网络。

### 8.2 速记版 Pipeline

1. burst 切分 → 去协议头 → 2-byte bigram token。
2. 四数据集多源预训练：masked token 重建 + dropout 视图 InfoNCE。
3. 构造"标注平衡 + 未标注长尾（γ）"划分。
4. E-step：Sinkhorn-Knopp 解熵正则 OT，得先验对齐的软伪标签 A。
5. M-step：L_proto（含先验修正）+ L_ins + λ_sup·L_sup 反传；每 epoch 动量更新原型 c_k 与先验 r_k；循环至收敛。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[malicious-traffic-detection]]
- [[encrypted-traffic-analysis]]
- [[traffic-classification]]
- [[traffic-representation-learning]]

### 9.2 相关方法

- [[contrastive-learning]]
- [[self-supervised-learning]]
- [[pre-training-finetuning]]

### 9.3 相关任务

- [[malicious-traffic-detection]]
- [[traffic-classification]]

### 9.4 可更新的综述页面

- [[survey-malicious-traffic-detection]]
- [[survey-encrypted-traffic-analysis]]

### 9.5 可加入的对比表

- [[method-comparison-table]]（提出新框架 LotBoNC，可作为长尾/开世界方法的对比行）
- [[open-source-registry]]（代码开源 https://github.com/watsonhuhpi/LotBoNC）
- [[dataset-comparison-table]]（给出 IoT-23 / ISCX-2014 / CTU-13 的长尾改造用法与流数统计）

### 9.6 相关论文笔记（KB 已有）

- [[2022-WWW-ET-BERT__A_Contextualized_Datagram_Representation_with_Pre-training_Transformers_for_Encrypted_Traffic_Classification]]（基线之一，ref [37]）
- [[2024-ICNP-NetMamba__Efficient_Network_Traffic_Classification_via_Pre-training_Unidirectional_Mamba]]（基线之一，ref [61]）
- [[2023-AAAI-Yet_Another_Traffic_Classifier_a_Masked_Autoencoder_Based_Traffic_Transformer_With_Multi-level_Flow_Representation]]（burst 级 tokenization 的设计参照，ref [72]）
- [[2025-S&P-TrafficFormer_An_Efficient_Pre-trained_Model_for_Traffic_Data]]（预训练流量模型引用，ref [74]）
- [[2022-TBD-Identification_of_Encrypted_Traffic_Through_Attention_Mechanism_Based_Long_Short_Term_Memory]]（LSTM-Att 基线，ref [70]）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 长尾 + 开世界是真实僵尸网络流量的常态：少数家族占主导、新变种稀疏无标注 | 问题定义与 Figure 1 图示（Mirai/Mozi/Gafgyt 头部 vs 尾部新家族） | §1 |
| 只对未标注集施加长尾可隔离不平衡效应，标注集保持类平衡 | 实验设计说明（"impose a long-tailed distribution only on the unlabelled portion"） | §5 |
| LotBoNC 在 γ=10 下 unlabelled-aware 领先最强基线 14.7~19.4 点 | Table 2（60.01/57.55/60.15 vs 45.30/38.14/42.91） | §5.5 |
| γ=1 时 unlabelled-agnostic 指标未超过 RoNeTC（88.20 vs 91.45） | Table 2 与正文自述 | §5.5 |
| 预训练是长尾新类发现的必要条件 | Table 5（IoT-23 88.20/74.21→56.05/47.82 等） | §5.7.2 |
| 移除监督对比损失 L_sup 造成最大退化（γ=5 时 UA 74.0→28.0） | Figure 9 消融描述 | §5.7.4 |
| 适度 dropout（0.10）是必需的，p=0 与 p=0.50 均崩溃 | Table 6（89.9/91.3/92.9 at p=0.10 vs 58.2/61.3/63.5 at p=0） | §5.7.5 |
| λ_proto=0.7 在所有指标最优 | Figure 8 与正文（0.1→0.7 时 UA 73.8→79.5，UAA 71.0→76.5） | §5.7.3 |
| ρ=0.5 时标注子集准确率仍 >98.5 | Table 3 | §5.6 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-AsiaCCS-LotBoNC__Novel_Botnet_Traffic_Classification_under_Long-tailed_Distributions.pdf
- MinerU Markdown：02-parsed-markdown/2026-AsiaCCS-LotBoNC__Novel_Botnet_Traffic_Classification_under_Long-tailed_Distributions.md

---

## 12. 后续问题

- Table 2 与 Table 4/5/6 的绝对数值口径不一致（如 IoT-23 γ=1 Overall：Table 2 = 94.48 vs Table 4 = 89.88 vs Table 5 w/ pretrain 行 88.20），论文未解释；需要核对 PDF 原表确认是否 Model 版本/超参不同（本文沿用解析稿数值，引用时标注口径）。
- `§5.7.2` 正文数值与 Table 5 不符（正文 60.21→75.73 等 vs 表内 88.20 等），疑似论文自身笔误或跨表引用错误，需查 PDF 原文。
- `§5.3` 称预训练"排除加密 payload 内容（they are irrelevant）"，但 `§4.2` 明确对去头后的 payload 做 2-byte bigram 分词——两处表述矛盾，需确认 payload 是否真正参与建模（若参与，则该文本身构成"payload 仍有可学习性"的证据）。
- 类别总数 K（含未知类数）在真实部署中如何确定？论文未给出 K 的敏感性实验或估计方法。
- Unlabelled-Agnostic 在平衡场景未超过 RoNeTC 的原因，论文仅定性解释，缺少可分性/校准角度的分析。

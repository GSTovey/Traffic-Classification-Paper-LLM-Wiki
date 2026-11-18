---
type: comparison
name: narrative-pattern-comparison
created: "2026-06-01"
updated: "2026-10-21"
---

# 叙事模式横向对比表

> 本表横向比较知识库中不同论文的**故事线**、**章节闭环方式**、**实验叙事方式**和**写作风格**，用于：
> 1. 学习顶会论文的叙事技巧
> 2. 为自己的论文写作选择合适的叙事模式
> 3. 识别不同方向/venue 的写作偏好

---

## 1. 叙事模式总览

| 论文 | 年份 | 方向 | 叙事模式 | 开篇方式 | 主线一句话 | 章节数 |
|---|---:|---|---|---|---|---:|
| Flowprint | 2020 | 移动应用指纹 | 首次型 + 填补型 | 应用开头 | 移动加密流量中目的地的时间相关性可构成指纹，首次实现无监督已知识别+未知检测 | 8 |
| Deep Fingerprinting | 2018 | 网站指纹攻击 | 跨域迁移 + 军备竞赛叙事 | 矛盾开头 | Tor 的隐私保护并非安全的——专为 WF 设计的深层 CNN 可突破 WTF-PAD 防御 | 8 |
| ET-BERT | 2022 | 加密流量分类 | 首次型 + 填补型 | 定义开头 | NLP 的 BERT 范式可系统迁移到加密流量分析，密码非完美随机是其理论基础 | 7 |
| ASNet | 2025 | 加密流量分类 | 填补型 + 问题分解型 | 问题开头 | BERT 的 word sense 在流量数据中被破坏 + 隐式分类导致特征区分度不足，需从 word-level 和 packet-level 双层解决 | 7 |
| TrafficGPT | 2024 | 流量分类与生成 | 填补型 + 统一型 | 挑战开头 | 线性注意力 GPT 突破 512 token 限制，可逆 tokenization 实现 pcap 完整重建，同时支持分类和生成 | 6 |
| Multi-ARCL | 2025 | 加密流量分类（持续学习） | 首次型 + 现象驱动型 | 数据开头 | 静默应用（已下架应用）加速模型衰减，需自适应 relay 持续学习框架实现选择性遗忘 | 7 |
| NetMamba | 2024 | 加密流量分类 | 首次型 + 填补型 | 问题开头 | 线性复杂度 SSM（Mamba）替代 Transformer 实现高效流量分类，stride 序列保留完整字节信息 | 7 |
| NetMamba+ | 2026 | 加密流量分类 | 填补型 + 统一型 | 问题开头 | Mamba + Flash Attention 双骨干 + 多模态表征 + 长尾感知微调，三重创新统一解决效率、表征和分布挑战 | 8 |
| TrafficMoE | 2026 | 加密流量分类 | 颠覆型 + 填补型 | 问题开头 | DFA（Disentangle-Filter-Aggregate）范式打破静态同质流水线，用稀疏 MoE 解耦 header/payload 异质建模 | 7 |
| STAR | 2025 | 网站指纹（零样本） | 首次型 + 跨域迁移型 | 矛盾开头 | HTTPS/ECH 加密隐私仍可被语义泄漏攻破——将 WF 重构为零样本跨模态检索问题，无需目标网站流量 | 7 |
| BiasSeeker (Bias in the Shadows) | 2026 | 加密流量分类（鲁棒性） | 颠覆型 + 评估驱动型 | 定义开头 | 预训练模型依赖 shortcut 特征泛化失败——首个模型无关、数据驱动的半自动 shortcut 检测框架 | 6 |
| [[03-paper-notes/2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions|NestTor (TNSM 2026)]] | 2026 | ToP 检测 | 语义分解 + 证据递进 + 条件边界 | 代理改变可见路径和可观察行为 | 先定义两个条件，再验证可见信号、检测、结构贡献与分布迁移 | 7（另含附录 A–E） |

> **叙事模式**：颠覆型 / 填补型 / 统一型 / 工程型 / 首次型
>
> **开篇方式**：数据开头 / 故事开头 / 矛盾开头 / 定义开头 / 应用开头

---

## 2. 章节叙事功能对比

### 2.1 Introduction 写法对比

| 论文 | 开篇钩子 | Gap 提出方式 | 段落结构 | 过渡到方法的方式 |
|---|---|---|---|---|
| Flowprint | 安全运维需求（管理员需要知道网络中哪些应用活跃） | 四象限定位（监督/无监督 × 明文/加密，发现空白象限） | 场景→挑战→现有方法→空白→方案概述→贡献 | 直接列出贡献点，引出方法名 |
| Deep Fingerprinting | Tor 的 WF 防御正在被实际部署（WTF-PAD/W-T） | 跨域论证：CV 的 DL 革命尚未发生在 WF 领域 | 威胁→防御→攻击现状→DL 潜力→方案→贡献 | "In this work, we present DF"——简明直入 |
| ET-BERT | 加密流量分类对网络安全至关重要但极具挑战 | 四代方法局限性枚举 + PERT 43.45% 数字冲击 | 问题重要性→四代方法演进→NLP 类比→方案→贡献 | 从 NLP 领域的 BERT 成功引入迁移思路 |
| ASNet | 加密流量分析中 BERT 直接处理字节会破坏语义完整性 | 两个核心问题的结构化分析：word-level（子词拆分破坏 word sense）+ packet-level（隐式分类特征区分度不足） | 问题重要性→两个核心问题→WSA 方案→CSS 方案→贡献 | 从 word-level 和 packet-level 两个语义层面分别引出对应解决方案 |
| TrafficGPT | 预训练模型在流量分析和生成中面临 token 长度限制 | 512 token 限制 + tokenization 不可逆两个具体挑战 | 问题重要性→预训练进展→两个挑战→线性注意力方案→贡献 | 从 NLP 的 GPT 成功引入自回归预训练思路 |
| Multi-ARCL | 应用市场频繁下架应用导致"静默应用"问题 | AppBrain 数据展示百万级应用/年下架 + 实验验证静默应用对模型的影响 | 现象观察→三个具体挑战（稳定性/可塑性/存储成本）→方案→贡献 | 从真实应用生态数据出发，用具体数字建立紧迫感 |
| NetMamba | 加密流量分类对网络安全至关重要但极具挑战 | 两大挑战结构化分析：效率（Transformer 二次复杂度）+ 表征（丢弃字节信息+保留偏差） | 问题重要性→两大挑战→Mamba 方案→表征方案→贡献 | 从 NLP/CV 的 Mamba 成功引入 SSM 迁移思路 |
| NetMamba+ | 加密流量分类三大挑战（效率+表征+长尾） | 在 NetMamba 基础上新增第三个挑战（长尾分布），形成三重创新结构 | 问题重要性→三大挑战→三重方案→贡献→在线系统 | 从 NetMamba 的局限性出发，自然引出升级需求 |
| TrafficMoE | 加密流量本质是异质的，但现有方法用同质流水线处理 | 三个关键因素分析：统一参数共享→噪声传播→静态融合 | 问题重要性→异质性分析→三个因素→DFA 范式→贡献 | 从"one-size-fits-all"的批判性视角出发，颠覆现有范式 |
| STAR | HTTPS/ECH 加密后传统标识符被隐藏，但流量仍泄漏语义信息 | 两个核心局限：流量漂移需频繁重训 + 无法处理未见网站 | 隐私背景→WF 现状→两个局限→跨模态检索方案→贡献 | 从隐私保护与语义泄漏的矛盾出发，建立研究紧迫性 |
| BiasSeeker | 预训练模型在 NTC 中存在 shortcut learning 问题 | 两类现有方法的局限：模型无关方法依赖专家知识 + 模型相关方法受限于特定架构 | 问题定义→两类现有方法→两个核心挑战→BiasSeeker 方案→贡献 | 从 shortcut learning 的定义出发，建立理论框架 |
| TrafficGPT | 预训练模型在流量分析和生成中面临 token 长度限制 | 512 token 限制 + tokenization 不可逆两个具体挑战 | 问题重要性→预训练进展→两个挑战→线性注意力方案→贡献 | 从 NLP 的 GPT 成功引入自回归预训练思路 |

### 2.2 方法论证逻辑对比

| 论文 | 论证方向 | 模块组织方式 | 公式呈现策略 | 图表配合方式 |
|---|---|---|---|---|
|  |  |  |  |  |

> **论证方向**：自底向上（从组件到系统） / 自顶向下（从目标到实现） / 类比迁移（从其他领域借鉴）
>
> **模块组织方式**：流水线式 / 分支汇合式 / 对比改进式

### 2.3 实验叙事方式对比

| 论文 | 实验组织逻辑 | 主实验叙事 | 消融实验策略 | 可视化/案例策略 |
|---|---|---|---|---|
| Flowprint | 场景驱动（识别→检测→跨平台→版本更新→浏览器→实时性） | 核心能力展示：已知 89.2% + 未知 93.5% precision | 无传统消融，通过 AMI 特征排名分析各特征贡献 | 流量聚类可视化 + 共享集群分析 |
| Deep Fingerprinting | 渐进增强驱动（无防御→WTF-PAD→W-T→开世界） | 对比碾压：98.3% 无防御 + 90.7% vs WTF-PAD | 架构消融：逐 Block 移除证明深度的必要性（Figure 7） | t-SNE 特征可视化 + 逐层激活分析 |
| ET-BERT | RQ 驱动（RQ1 分类性能→RQ2 预训练效果→RQ3 理论解释） | 对比碾压：ISCX +5.2%, Cross-Platform +5.4%, TLS1.3 +10.0% | 逐组件消融（MBM/SBP/Datagram2Token 各自贡献） | 密码随机性分析（理论可视化） + few-shot 分析 |
| ASNet | 任务覆盖驱动（7 个任务全面评估） | 无预训练 SOTA：5 个数据集 7 个任务全面领先 | WSA/CSS 模块消融 + prompt 设计分析 | word sense 可视化 + 语义空间分离可视化 + 可解释性分析 |
| TrafficGPT | 双任务驱动（分类 + 生成分别评估） | 分类 Macro F1 平均提升 2%；生成 JS 散度 0.1605（header）/ 0.2396（flow），F1≈0.5 判别 | token 长度扩展实验 + 注意力机制消融 | 生成流量 vs 真实流量对比可视化 |
| Multi-ARCL | 挑战驱动（三个挑战分别验证） | NJUPT2023 准确率提升 8.64%+；跨数据集泛化验证 | 静默应用影响分析 + 自适应 relay 机制消融 + 多模态融合分析 | 静默应用数量趋势图 + 稳定性-可塑性权衡曲线 |
| NetMamba | 渐进增强驱动（无防御→few-shot→分布偏移） | 6 数据集准确率 90%+，部分超 99%；推理速度提升 60 倍 | stride 长度/方向/位置嵌入消融 + 预训练策略对比 | 表征方案对比表 + 效率分析（吞吐量+GPU 内存）+ t-SNE 可视化 |
| NetMamba+ | 任务覆盖驱动（4 个分类任务 + OOD + 在线系统） | F1 最高提升 6.44%；推理吞吐量 1.7x；在线系统 261.87 Mb/s；OOD AUROC >94% | 多模态消融（byte/packet size/interval 各自贡献）+ LDA loss 消融 + Flash Attention vs vanilla Transformer | 多模态表征方案对比表 + 长尾分布分析 + OOD 检测 ROC 曲线 |
| TrafficMoE | 功能验证驱动（DFA 三组件逐一验证） | 6 数据集 SOTA | Disentangle/Filter/Aggregate 三组件消融 + 专家数量敏感性 + 不同 MoE 配置对比 | 专家利用率热力图 + 路由概率分布可视化 + 不确定性过滤效果对比 |
| STAR | 任务递进驱动（闭世界→少样本→开世界→语义对齐分析） | 1,600 未见网站 87.9% top-1；开世界 AUC 0.963；Tip-Adapter top-5 98.8% | 双编码器结构消融 + 对比学习损失消融 + 增强策略消融 + 对齐锚点分析 | 语义-流量对齐可视化 + 跨模态检索示例 + 混淆矩阵分析 |
| BiasSeeker | 数据驱动（19 数据集 × 3 任务全面诊断） | 揭示预训练模型依赖 TCP Timestamp 等 shortcut 特征 | shortcut 分类验证 + 特征遮蔽前后性能对比 + 不同检测阈值敏感性 | shortcut 特征分布热力图 + AMI 分布直方图 + 特征遮蔽前后 t-SNE 对比 |
| TrafficGPT | 双任务驱动（分类 + 生成分别评估） | 分类 Macro F1 平均提升 2%；生成 JS 散度 0.1605（header）/ 0.2396（flow），F1≈0.5 判别 | token 长度扩展实验 + 注意力机制消融 | 生成流量 vs 真实流量对比可视化 |

> **实验组织逻辑**：RQ 驱动 / 场景驱动 / 假设验证驱动 / 渐进增强驱动
>
> **消融实验策略**：逐模块剥离 / 按功能分组 / 超参数敏感性 / 架构变体对比

### 2.4 局限性与讨论对比

| 论文 | 局限性位置 | 讨论方式 | 承认范围 | 未来工作策略 |
|---|---|---|---|---|
|  |  |  |  |  |

> **讨论方式**：主动承认 / 条件限定 / 未来工作暗示 / 不讨论

---

## 3. 写作风格维度对比

| 论文 | 句子密度 | 技术细节密度 | 图表数量 | 参考文献数 | 总页数 | 一句话风格标签 |
|---|---|---|---:|---:|---:|---|
| ASNet | 适中 | 平衡 | 8 | 45 | 14 | 双层语义分解 + 无预训练 SOTA |
| TrafficGPT | 详细 | 直觉优先（少公式） | 5 | 50 | 12 | 突破长度限制的统一框架 |
| Multi-ARCL | 详细 | 平衡 | 6 | 38 | 14 | 现象驱动 + 三个挑战逐个击破 |
| NetMamba | 适中 | 平衡 | 7 | 35 | 12 | 首次 SSM 迁移 + 效率碾压 |
| NetMamba+ | 详细 | 平衡 | 9 | 40 | 14 | 三重创新统一框架 + 在线系统验证 |
| TrafficMoE | 适中 | 公式密集 | 6 | 38 | 13 | DFA 范式颠覆 + 异质性建模 |
| STAR | 详细 | 平衡 | 8 | 42 | 13 | 零样本跨模态检索 + 语义泄漏分析 |
| BiasSeeker | 详细 | 公式密集 | 5 | 55 | 12 | 数据驱动诊断 + 19 数据集全面验证 |

> **句子密度**：简洁（每段 ≤5 句） / 适中 / 详细（每段 >8 句）
>
> **技术细节密度**：直觉优先（少公式） / 平衡 / 公式密集

---

## 4. 按 Venue 的写作偏好

### 4.1 顶会（CCS / S&P / USENIX / NDSS / SIGCOMM）

| 写作特征 | 典型表现 | 代表论文 |
|---|---|---|
|  |  |  |

### 4.2 顶刊（TIFS / TDSC / TON / TSC）

| 写作特征 | 典型表现 | 代表论文 |
|---|---|---|
|  |  |  |

### 4.3 其他（KDD / NeurIPS / AAAI / arXiv）

| 写作特征 | 典型表现 | 代表论文 |
|---|---|---|
| 问题分解式论证 | 从多个维度系统分析问题，每个维度对应一个解决方案 | ASNet (TIFS 2025)：word-level + packet-level 双层分析 |
| 现象驱动叙事 | 从真实世界观察出发，用数据建立紧迫感 | Multi-ARCL (JPDC 2025)：AppBrain 百万级应用/年下架数据 |
| 统一框架叙事 | 将多个任务统一到一个框架中，强调通用性 | TrafficGPT (arXiv 2024)：分类+生成统一到 GPT 框架 |
| 范式颠覆叙事 | 批判现有范式并提出全新框架 | TrafficMoE (arXiv 2026)：DFA 范式打破"one-size-fits-all"静态流水线 |
| 零样本跨域迁移叙事 | 将传统问题重构为新范式，消除对标注数据的依赖 | STAR (INFOCOM 2026)：WF 重构为零样本跨模态检索，无需目标网站流量 |
| 数据驱动诊断叙事 | 从评估视角揭示系统性问题，提供工具化解决方案 | BiasSeeker (arXiv 2026)：模型无关的 shortcut 检测框架，19 数据集全面诊断 |

---

## 5. 可迁移写法提炼

> 基于横向比较，提炼最高价值的可迁移写作模式。

### 5.1 开篇模式库

| 模式 | 适用场景 | 典型范例 | 效果 |
|---|---|---|---|
|  |  |  |  |

### 5.2 Gap 展开模式库

| 模式 | 适用场景 | 典型范例 | 效果 |
|---|---|---|---|
|  |  |  |  |

### 5.3 实验叙事模式库

| 模式 | 适用场景 | 典型范例 | 效果 |
|---|---|---|---|
|  |  |  |  |

---

## 6. 对写作的启示

> 基于上述横向比较，提炼可直接用于论文写作的叙事建议。

1. **开篇要快速建立"为什么这篇论文值得读"**：Flowprint 用安全运维场景、DF 用防御部署的紧迫性、ET-BERT 用 PERT 43.45% 的数字冲击、Multi-ARCL 用百万级应用/年下架的现实数据——四种策略都有效，但安全会议偏好场景驱动，AI 会议偏好数据驱动
2. **Gap 展开不要只说"效果不好"，要定位到结构化空白**：Flowprint 的四象限图和 ET-BERT 的四代演进图都是极好的 Gap 可视化——建议在 Introduction 中用一张图把 Gap 讲清楚
3. **实验叙事要有"高潮"**：DF 的 Section 5.6（WTF-PAD 90.7%）是全文叙事的顶点——在递进式实验中，最关键的突破性结果应放在消融之后、开世界之前，让读者在积累了足够信任后看到最震撼的结果
4. **问题分解式叙事适合多维度创新**：ASNet 从 word-level 和 packet-level 两个层面分别分析问题并给出对应方案，这种"问题-方案"配对结构清晰且有说服力——适合有多个创新点的论文
5. **现象驱动叙事建立真实紧迫感**：Multi-ARCL 从 AppBrain 真实数据出发，用百万级应用/年下架的数字建立紧迫感，比纯学术 Gap 更有冲击力——适合解决实际部署问题的论文
6. **统一框架叙事扩大影响力**：TrafficGPT 将分类和生成统一到一个框架中，强调通用性——适合基础模型类论文，可同时吸引不同子方向的关注

## 2026-10-26 新入库动机与叙事候选（待审核）

| 论文 | venue/年份 | 动机模式 | 证据位置 |
|---|---|---|---|
| HF-Transformer: A Non-Pretrained Encrypted Network Traffic Classification Model Based on Packet Header Fields | INFOCOM 2026 | 性能/泛化改进 | 摘要/引言，待正文复核 |
| Synecdoche: Efficient and Accurate In-Network Traffic Classification via Direct Packet Sequential Pattern Matching | INFOCOM 2026 | 性能/泛化改进 | 摘要/引言，待正文复核 |
| A Unified Oversampling-Based Imbalance Processing Framework for Network Traffic Anomaly Detection | TDSC 2026 | 性能/泛化改进 | 摘要/引言，待正文复核 |
| Behavioral Evidence-Based Hierarchical Decision Refinement for Encrypted Malicious Traffic Classification in Decentralized Data Circulation | TDSC 2026 | 性能/泛化改进 | 摘要/引言，待正文复核 |
| Drift-Aware Adaptive Website Fingerprinting | TDSC 2026 | 性能/泛化改进 | 摘要/引言，待正文复核 |
| Fooling Multi-Tab Browsing: Few-Shot Website Fingerprinting Attacks and Lightweight Obfuscation Defenses | TDSC 2026 | 性能/泛化改进 | 摘要/引言，待正文复核 |
| GenETC: Dynamic Graph-enhanced Fine-tuning for Encrypted Traffic Classification | TDSC 2026 | 性能/泛化改进 | 摘要/引言，待正文复核 |
| Is the Data Really Noisy? Rethinking Traffic Filtering for Encrypted Traffic Classification | TDSC 2026 | 性能/泛化改进 | 摘要/引言，待正文复核 |
| QuicReflo: Exploiting Multi-Flow Redundancy for Restoration-Free Covert Communication Over QUIC | TDSC 2026 | 新攻击面或通信机制 | 摘要/引言，待正文复核 |
| RearView: Secure Two-Stage Malicious Traffic Identification with Dynamic Relationship Awareness | TDSC 2026 | 新攻击面或通信机制 | 摘要/引言，待正文复核 |
| TridentDNS: Detecting Diverse DNS Tunnels Via Multidimensional Features | TDSC 2026 | 新攻击面或通信机制 | 摘要/引言，待正文复核 |
| InvisiTunnel: Causality-Preserving Covert Communication over DoH through Request Substitution | TIFS 2026 | 新攻击面或通信机制 | 摘要/引言，待正文复核 |
| Two Heads Are Better Than One: Models-to-Model Learning for Encrypted Traffic Analysis | TIFS 2026 | 新攻击面或通信机制 | 摘要/引言，待正文复核 |
| Two Heads Are Not Better Than One: Continual Learning From Multiple Models for Encrypted Traffic Analysis | TIFS 2026 | 新攻击面或通信机制 | 摘要/引言，待正文复核 |
| Encrypted Network Traffic Classification Using Generative and Contrastive Self-Supervised Learning | TON 2026 | 性能/泛化改进 | 摘要/引言，待正文复核 |
| Fighting the Enemy Within: Traffic Semantics-Driven Framework Against Noisy Labels for Robust Traffic Classification | TON 2026 | 性能/泛化改进 | 摘要/引言，待正文复核 |
| KAN-Vis: Efficient and Lightweight Visual Technique for Network Traffic Classification Using Kolmogorov–Arnold Network | TON 2026 | 性能/泛化改进 | 摘要/引言，待正文复核 |
| Making the Best of Both Worlds: Universal Perturbations for Live Black-Box Evasion Against NIDS in Encrypted Traffic | TON 2026 | 新攻击面或通信机制 | 摘要/引言，待正文复核 |
| SRViT: A Robust Online Encrypted Traffic Classification Based on Vision Transformer | TON 2026 | 性能/泛化改进 | 摘要/引言，待正文复核 |
| When Pre-Training Meets Contrast Learning: Few-Shot Encrypted Traffic Classification With Novelty Detection | TON 2026 | 性能/泛化改进 | 摘要/引言，待正文复核 |


## 2026-11-18　L3 论文叙事案例

| 论文 | 开篇张力 | 论证与实验结构 |
| --- | --- | --- |
| [[03-paper-notes/2025-NIPS-Self-Supervised_Learning_of_Graph_Representations_for_Network_Intrusion_Detection\|GraphIDS]] | 分离训练和检测 → 联合重构 | 从分离训练与检测的错位提出共享重构目标。消融把可比较的两个因素定义为局部图与批内注意力，并用两类规模的数据展示它们的边际收益。部署讨论进一步拆开前向时间和整条观测链路。 |
| [[03-paper-notes/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC\|Nepco]] | 端侧代价 → 分解输入、算子与执行 | 先将表面上的通用性/效率冲突分解到前处理、架构与执行，再以局部性观测支持卷积选择。最后用同设备负载扫描和完成量验证端到端收益。 |
| [[03-paper-notes/2026-S&P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency\|SaTor]] | 电路时延与中继选择随机性 → 底层链路 | 从降低时延与保持中继随机性的矛盾提出底层链路选择。先校准仿真再扫部署覆盖，最后将时延收益和可见性分别讨论。 |
| [[03-paper-notes/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture\|CryptoFormer]] | 多币种明密文与行为混淆 → 两层表示 | 由明密文并存及多币种会话相似引出两级表示。主表对照总体效果，错误矩阵和消融定位信号来源，最后以训练时间讨论部署成本。 |
| [[03-paper-notes/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection\|HAD]] | 原 IDS 受变化影响 → 跨视角补充分数 | 论文先通过特征分区提出正常样本跨视角一致的假设，再用分层表示实现防御。独立防御、附加检测和时间漂移各用相应主结果，FAR 的恢复另列目标数据访问。 |
| [[03-paper-notes/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures\|PS-ML]] | 计数饱和与大流稀缺 → 查询侧专门化 | 从 RatioSketch 的按域失效和大流样本稀缺出发，以丰富查询信息和专用模型回应两种误差来源。按内存、时间和跨域报告，同时保留写入与查询的区别。 |
| [[03-paper-notes/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks\|SEDMS]] | 全量遥测负担和统计变化 → 摘要与更新 | 从全量遥测的内存/通信负担与固定子集的陈旧性出发，给出摘要与更新两项机制。实验分别检验判别性、保留比例、速度和分布变化。 |
| [[03-paper-notes/2026-ICML-Threat2Traffic__Multi-Agent_Environment_Synthesis_for_Malware_Traffic_Generation_from_Threat_Intelligence\|Threat2Traffic]] | 从行为覆盖缺口拆分采集失败 | 采集缺口引出条件证据与配置验证两类失败。正文依次交代阶段指标、源隔离对照、消融和产出，最后用失败样本厘清语料覆盖。 |
| [[03-paper-notes/2026-S&P-A_Context_Is_Worth_a_Thousand_Lies__Evading_Intrusion_Detectors_via_Intelligent_Context_Distortion\|Contorter]] | 检测依赖关系 → 区分图的语义与判定 | 论证先从强上下文为何有助检测转到它的可变性。节点级和图级结果分开呈现，切分、权限与标注范围的差异决定结论边界。 |
| [[03-paper-notes/2026-S&P-CenRL__A_Framework_for_Performing_Intelligent_Censorship_Measurements\|CenRL]] | 固定测量预算 → 按反馈选择 | 受控部分将固定预算和动态变化分开验证。真实部署同时改变站点选择范围和调度，写作时补上这一点，避免把全部收益归因于 UCB。 |
| [[03-paper-notes/2026-S&P-Descriptors_of_Exposure__Undermining_Tor_Anonymity_Through_Exploiting_Descriptor_Flood\|Descriptors of Exposure]] | 缓存计量偏差 → 进程/服务资源 | 论文从组件内存异常推导服务影响，夹杂实测与估计。可借鉴按组件、服务与网络层组织结果，再用审稿疑问核对中间推断。 |
| [[03-paper-notes/2026-FMANO-Toward_Unified_Network_Traffic_Monitoring_Using_SIR\|SIR]] | 多语言语义差异 → 统一状态 | 先把语言差异写成可检查的状态行为，再用每个前端的一个代表机制说明如何统一表达。资源表提供工程比较的输入，部署收益由后续平台实测回答。 |
| [[03-paper-notes/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models\|MPA-LLM]] | 共享模型受分辨率差异影响 → 阶段解耦 | 文章从多尺度重构过渡到多任务架构。主比较、去阶段消融、联合训练和跨拓扑是四个不同证据，不能用一个平均赢家概括。 |

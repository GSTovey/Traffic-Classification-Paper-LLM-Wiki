---
type: paper
title_original: "SkillWatermark: An Embedded Skill Watermark of Progressive Privacy Inference via Benign Prompts"
title_cn: "SkillWatermark：经良性提示词嵌入技能水印的渐进式隐私推断"
authors: [Yu Li, Liqi Zhuang, Dong Wei, Jiwen Luo, Hang Zhang, Meng Zhang, Xiaona Li, Weiqing Huang]
year: 2026
venue: "arXiv 2026"
doi: "unknown"
url: "https://arxiv.org/abs/2608.16026"
pdf: "00-inbox/PDFs/2026-arXiv-SkillWatermark__An_Embedded_Skill_Watermark_of_Progressive_Privacy_Inference_via_Benign_Prompts.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-SkillWatermark__An_Embedded_Skill_Watermark_of_Progressive_Privacy_Inference_via_Benign_Prompts.md"
status: processed
reading_level: L1
research_area: ["encrypted-traffic-analysis"]
task: []
method: []
dataset: ["ClawHub 技能市场全量爬取（65,699 个技能，14 个领域）", "自采集 Claude Code 流量样本（>7,000 条，Clash 代理模拟 VPN）"]
code: "unknown"
relevance: medium
created: "2026-09-19"
updated: "2026-09-19"
---

# SkillWatermark: An Embedded Skill Watermark of Progressive Privacy Inference via Benign Prompts

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | SkillWatermark: An Embedded Skill Watermark of Progressive Privacy Inference via Benign Prompts |
| 中文标题 | SkillWatermark：经良性提示词嵌入技能水印的渐进式隐私推断 |
| 作者 | Yu Li, Liqi Zhuang, Dong Wei, Jiwen Luo, Hang Zhang, Meng Zhang, Xiaona Li, Weiqing Huang（中科院信息工程研究所/中国科学院大学/CASIC 智能决策工程研究院） |
| 年份 | 2026 |
| 会议/期刊 | arXiv 2026（解析稿首页无会议页眉；IEEE 模板风格，未提及正式出版信息） |
| 研究方向 | 加密流量分析（LLM agent 流量的隐私推断/隐蔽信道） |
| 任务类型 | 被动流量隐私推断（prompt 关键词恢复），以隐蔽信道编码实现 |
| 方法关键词 | 技能水印（prompt 约束词）、多轮流量塑形、编码工具箱（包大小/方向/时序）、多级编码策略 |
| 数据集 | ClawHub 技能市场全量爬取（65,699 技能 / 14 领域，2026-06）；自采集 Claude Code 与 GLM 5.2 流量样本 >7,000 条 |
| 是否开源 | 未提及自有代码仓库（code=unknown）；实验提及 Clash 代理与 Whisper Leak 式采集脚本 |
| PDF | 00-inbox/PDFs/2026-arXiv-SkillWatermark__An_Embedded_Skill_Watermark_of_Progressive_Privacy_Inference_via_Benign_Prompts.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-arXiv-SkillWatermark__An_Embedded_Skill_Watermark_of_Progressive_Privacy_Inference_via_Benign_Prompts.md |

---

## 1. 一句话总结

> 在 agent 技能描述中插入良性 prompt 约束词（水印）主动塑形多轮加密流量，被动攻击者据此解码用户私密关键词，TPR 98.8%/FPR 8% 且通过 LLM 审计。

---

## 2. 摘要翻译

### 2.1 摘要原文

> "We observe that these skills generate specific traffic patterns during execution. In this paper, we design a pipeline that generates specific traffic patterns by inserting carefully designed skill descriptions, which we term skill watermarks, so that a passive network attacker can establish a covert channel to encode private information within observable traffic across multiple conversation turns... our modifications are benign in the sense that they do not directly exfiltrate any private data and do not execute any malicious instructions."（Abstract，节选）

### 2.2 摘要中文翻译

面向 LLM agent 的技能已在多个领域广泛部署，但我们观察到这些技能在执行时会产生特定流量模式。本文设计一条流水线：向技能描述中插入精心设计的文本（称为技能水印），使被动的网络攻击者能够在多轮会话的可观测流量中建立隐蔽信道、编码私密信息。具体而言，水印是插入原始技能描述中的 prompt 约束词，被嵌入多轮对话后由用户原始 prompt 中的关键信息触发，从而在流量中产生清晰可观测的编码；攻击者只需解码流量模式即可恢复被编码的信息。这些修改是"良性"的：不直接外传任何隐私数据，也不执行任何恶意指令。大量实验表明，水印产生高度一致且可区分的流量模式，且经改造的技能可通过现有 LLM 安全审计工具。该研究揭示"生成特定流量模式"可被利用为新的攻击面，并为后续安全加固提供关键洞察。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

技能生态（如 ClawHub，2026-06 已达 65,699 个技能）中超三分之一具备多轮能力，而技能的 prompt 描述本身会显著改变网络流量。已有 agent 流量隐私攻击（WHISPER LEAK、AGENTPRINT）依赖"采集流量→训练分类器"范式，只对数据集内出现过的 prompt 有效；用户 prompt 内容高度个性化、无界，一旦超出数据集即按开放世界问题被忽略（§I、§II-C）。

### 3.2 现有方法的痛点和不足

① 数据集依赖：prompt 空间无界，离线采集 + 分类无法覆盖；② 语言风格敏感：同一意图换风格后流量分布可差十倍以上，t-SNE 上两类完全重叠（§III-B, Figure 3）；③ 现有恶意技能检测（静态分析 + LLM 审计）只覆盖外传数据、提权、远程执行等已知类别，流量侧信道塑形不在其列（§II-B, Table I）；④ 依赖 DNS/SNI 可见性的方法在 VPN/加密下失效（§II-C）。

### 3.3 论文的研究假设或核心直觉

私密信息只藏在 prompt 的少数关键词中；只要攻击者维持一份"关注词字典"，并让技能在检测到这些词时产生可区分的流量模式，就能跨多轮会话逐步泄露 + 推断（§III-B、§IV-A）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 技能描述能显著改变流量（68% 已安装技能含塑形描述）；同一意图不同风格流量差 10× | §IV-B、Figure 3–4 |
| 痛点提炼 | 采集-训练-分类范式对无界 prompt 空间不可行；风格变化破坏可分性 | §III-B、§II-C |
| 问题转化 | 转为"如何设计良性 prompt 词主动塑形流量以编码信息" | §IV-A |
| 文献定位 | WHISPER LEAK/AGENTPRINT 最近邻但范式不同；恶意技能检测体系未覆盖该面 | §II-B–C |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | prompt 约束词可稳定控制包大小/时序，从而跨轮编码信息且不触发审计 | §IV-B | 14 领域一致性 + TPR/FPR + LLM 审计 |
| 辅助假设（如有） | 良性技能中已存在结构相似的描述，拼接后不显可疑 | §IV-B、Figure 4 | 100+ 技能改造后过审 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 流量可控且可解码 | 支撑 | T2+T3 判据 TPR 98.8%/FPR 8%；T2 92.5%/13% | Table III、§V-C |
| 改造后不被审计发现 | 支撑 | 全部改造技能通过 LLM 安全审计（被解释为个性化） | §V-D |

---

## 4. 方法设计

### 4.1 方法整体流程

攻击者向技能描述插入水印（prompt 约束词）并发布 → 用户使用该技能时，水印在检测到关注关键词后触发特定行为（简短回答/详细回答、本地 sleep、web 搜索等）→ 流量在包大小、方向、时序三个维度产生可区分模式 → 被动攻击者观测多轮会话并按字典解码 → 逐步推断用户意图与身份属性（§IV-A）。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | 良性技能描述 | 拼接良性约束词形成水印，保证语义合理 | 改造后的技能 | 建立隐蔽信道载体 |
| Step 2 | 用户 prompt | 技能检测关键词并触发 A/B 两种流量模式 | 每轮可区分的流量 | 编码 1 bit/轮 |
| Step 3 | 多轮会话 | N 轮 × 2 模式编码 → 2^N 个关键词可区分（N=4 时 16 个） | 会话级编码 | 提升信息容量 |
| Step 4 | 加密流量（含 VPN） | 观测包大小/方向/时序，按字典解码 | 关键词/意图 | 渐进式隐私推断 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 编码工具箱 | 三类可控维度（包大小：字符限制/模糊量词；时序：bash sleep、web 搜索延迟；方向：轮次边界） | 水印文本 | 可观测流量变化 | 方法核心 |
| 语言模板层 | 用既有良性描述拼装水印，降审计风险 | 水印意图 | 自然语言技能描述 | 与编码工具箱配对 |
| 多级编码策略 | 把单轮扩展为多轮，逐轮收窄范围 | 关键词字典 | N 轮编码方案 | 提升容量 |
| 解码端字典 | 攻击者预建关注词表 | 观测模式 | 关键词 | 攻击输出 |

### 4.4 公式、算法和机制解释

多级编码：设字典 K 个敏感词，每词分配长度 N 的二进制码字；第 i 轮若 prompt 含码字第 i 位为 1 的词则执行模式 A（简短回答 + sleep），否则模式 B（详细回答 + web 搜索）；攻击者对 N 轮流量逐轮分类后拼接比特，N=4 时可区分 2^4=16 个关键词（§IV-C）。时序维度需避开与包大小的冲突：显式/隐式的"思考"延迟会同时产生 token 流量，故改用 bash sleep 与 web 搜索（检索等待期无 token 输出）作为时序水印（§IV-B）。

### 4.5 方法优势

无需解密、不受 VPN 影响（仅用包大小/方向/时序）；不依赖流量采集与模型训练，免去对 prompt 数据集的依赖；水印由良性描述拼接而成，静态/LLM 审计均不告警；跨领域（14 领域）与跨模型（Claude Code、GLM 5.2）稳定（§IV-B、§V-A–D）。

### 4.6 方法不足

仅适用于可观测网络的在线模型（离线部署无效）；用户不用技能、仅单轮且 prompt 极短、或多会话并发（VPN 掩盖端口）时失效；未改造技能偶发相似流量会造成误报；实验为闭环采集，端到端信息恢复率尚待量化（§V-D、§VI 局限性）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

与 WHISPER LEAK/AGENTPRINT 等"采集-训练-分类"被动推断不同，本文是主动塑形（attack-shaped traffic）：由攻击者在技能中埋入编码规则，使流量本身携带结构化信号，从而摆脱训练集覆盖限制；与恶意技能攻击（外传、提权、远程执行、prompt 注入）不同，水印在外观上是良性个性化描述（§II-B–C、§IV-A）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 技能水印攻击面 | 首次揭示 prompt-流量关系可被主动利用 | 高 | 是（同类 agent 生态均适用） |
| 编码工具箱 | 包大小/时序/方向三维可控，含跨维度冲突分析 | 中-高 | 是（流量隐蔽信道设计） |
| 多级编码 + 探测策略 | N 轮 2^N 关键词区分，逐步收窄意图 | 中 | 是 |
| 审计规避设计 | 以良性描述拼装水印，过 LLM 审计 | 中-高 | 是（供应链攻击设计） |

### 5.3 适用场景

攻击者可向技能市场/仓库上传技能的供应链场景；受害者使用 agent（Claude Code、Cursor、Codex 等）多轮交互且流量可被 ISP/网关/中继观测；用户使用 Clash/V2Ray 等匿名代理时仍成立（§III-A）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| WHISPER LEAK / AGENTPRINT（采集+分类） | 被动、对已有流量有效 | 依赖训练集覆盖；风格变化即失效 | 主动塑形，不依赖数据集 |
| NETECHO（领域结构化文本重建） | 特定领域可重建文本 | 依赖领域结构化词表 | 仅需关注词字典 + 流量模式 |
| 既有恶意技能检测（静态/LLM 审计） | 覆盖外传/提权/注入等 | 不检测流量侧信道塑形 | 水印天然绕过此类审计 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

采集：在 Intel i7-13700H 笔记本上安装 Claude Code，用 Clash 代理模拟 VPN；改造 100+ 个真实技能（每领域下载量前 10），每技能设计贴合其功能的提问并嵌入身份/目标/需求信息；>7,000 条样本；另用 GLM 5.2 做跨模型对照，9 种 prompt 风格做跨风格对照（§V-A, Table II）。

### 6.2 数据集

ClawHub 全量技能爬取（65,699 个，按 14 领域分类，2026-06 时点）用于统计与技能改造；流量样本为自采集（>7,000 条）（§II-A、§V-A）。

### 6.3 Baseline

定性对照为未嵌水印的原始技能流量；相关方法对照为 WHISPER LEAK、AGENTPRINT、NETECHO（§II-C、§V-B）。

### 6.4 评价指标

流量一致性（Wasserstein 距离、DTW 距离，越小越稳定）；解码 TPR/FPR（水印数据集 vs 无水印数据集）；LLM 安全审计通过率（定性）（§V-B–D）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| 跨领域一致性（14 领域） | 一致性改善 | 第 2 轮起 11 个领域 >2× | 未嵌水印基线 | >2× | 第 3 轮起各技能流量结构高度相似 |
| 解码（T2） | TPR/FPR | 92.5% / 13% | — | — | 单轮判别力有限 |
| 解码（T2+T3） | TPR/FPR | 98.8% / 8% | — | — | 轮数增加 TPR 升、FPR 降 |
| 跨模型（Claude Code vs GLM 5.2） | 模式一致性 | 高度一致（GLM 流量更稀疏） | — | — | 模型 API 经 settings.local.json 切换 |
| 对抗 LLM 审计 | 通过率 | 全部通过（被解释为个性化服务） | — | — | 含尝试泄露隐式信息的样例 |

### 6.6 优势最明显的场景

用户使用多轮技能且流量经 VPN 加密：攻击者仅凭包大小/方向/时序即可判别每轮模式并解码；技能改造后仍通过审计，形成"良性外观 + 隐蔽信道"的组合（§V-D）。

### 6.7 局限性

离线模型、无技能场景、单轮短 prompt、并发会话（VPN 掩盖端口）均不适用；未改造技能的巧合流量带来假阳性；论文自述尚未量化端到端信息恢复准确率（§VI Limitations）。

---

## 7. 学习与应用

### 7.1 是否开源？

未提及自有代码或数据仓库（code=unknown）；采集脚本参照 Whisper Leak 的做法自行实现。

### 7.2 复现关键步骤

1. 爬取技能市场并按领域统计多轮技能占比与流量塑形描述占比（Figure 1、4）；
2. 从良性技能中挑选字符限制/模糊量词/sleep/web 搜索等约束词，拼装为 A/B 两种水印；
3. 在真实 agent（Claude Code + 代理）上按 14 领域 × 9 风格 × 多轮采集流量，用 Wasserstein/DTW 评估一致性；
4. 以 T2/T3 判据计算 TPR/FPR，并把改造后技能交给 LLM 审计工具做定性过审测试。

### 7.3 关键超参数、预处理和训练细节

无模型训练。关键设计参数：水印轮数 N（示例 N=4 → 16 个关键词）、字符限制选型（"at least x chars" 判别力最佳，"exactly/at most" 明显更差）、模糊量词四级（as-few/few/more/much）、时序水印形式（bash sleep 精确间隔、web 搜索引入等待）（§IV-B–C、Figure 5–8）。

### 7.4 能否迁移到其他任务？

可迁移点：① "以良性描述承载编码规则"的供应链思路可迁移到任何插件/技能生态（VS Code 扩展、浏览器插件、MCP 工具）；② 包大小/时序/方向三维编码与跨维度冲突分析（延迟塑形必然伴随 token 流量）对流量隐蔽信道设计普遍适用；③ 其"不训练分类器、直接模式判别"的解码方式对 WF 类研究是一个范式对照（以下为笔记作者的迁移分析，非论文原文主张）。

### 7.5 对我的研究有什么启发？

① LLM agent 流量正在成为独立攻击面，其"开放式 prompt 空间 + 固定技能管道"的组合与网站指纹的封闭站点集假设形成鲜明对比，值得在开放世界设定下系统评估；② 防御侧需要新的审计维度：检测"能跨轮产生模式化流量"的技能；③ 评估指标（Wasserstein/DTW 一致性 + TPR/FPR）可直接复用到流量塑形类防御评估。

---

## 8. 总结

### 8.1 核心思想

> 用良性提示词水印主动塑形 agent 流量以编码隐私。

### 8.2 速记版 Pipeline

1. 攻击者从良性技能描述中拼装水印（字符限制/模糊量词/sleep/web 搜索）；
2. 水印随技能分发，用户使用时被关键词触发，产生 A/B 两种流量模式；
3. 多轮扩展（N 轮 = 2^N 个关键词），包大小/时序/方向三维编码；
4. 被动攻击者观测加密流量（VPN 下亦然），按字典逐轮解码；
5. 跨 14 领域验证一致性，T2+T3 解码 TPR 98.8%/FPR 8%，且全部通过 LLM 审计。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[encrypted-traffic-analysis]]（攻击者仅用加密流量可观测的包大小/方向/时序做推断，属加密流量分析的新载体：LLM agent 流量）
- [[website-fingerprinting]]（论文明确将 WHISPER LEAK/AGENTPRINT 归为 WF/app fingerprinting 技术的迁移，并指出该范式在无界 prompt 空间下的失效）
- [[anonymous-traffic-identification]]（在用户使用 Clash/V2Ray 匿名代理、仅剩元数据可观测的设定下做身份/意图识别）

### 9.2 相关方法

- 库内无对应方法页：本文不训练模型，方法为水印编码工具箱与多级编码策略，白名单 8 个方法 slug 均不适用。
- [[2025-S&P-Countmamba__A_Generalized_Website_Fingerprinting_Attack_via_Coarse-Grained_Representation_and_Fine-Grained_Prediction]]（[13] 本文引用的 WF 攻击工作，用作"网站/应用流量模式近乎固定"的对照；非本文方法）
- [[2024-CCS-Robust_and_reliable_early-stage_website_fingerprinting_attacks_via_spatial-temporal_distribution_analysis]]（[29] 本文引用的早期 WF 攻击工作，作为其"本地被动敌手模型"的既有来源之一）

### 9.3 相关任务

- [[app-fingerprinting]]（本文与之对照的既有范式之一：AGENTPRINT 属 app fingerprinting 思路；论文用其作对照基线并指出局限）

### 9.4 可更新的综述页面

- [[survey-encrypted-traffic-analysis]]（LLM agent 交互流量可作为新的加密流量分析对象/攻击面章节）
- [[claims-index]]（可沉淀"WF 式采集-训练-分类范式在无界 prompt 空间失效"类证据；与 WF 相关 claims 存在潜在呼应，入库时需标注载体差异）

### 9.5 可加入的对比表

- [[motivation-pattern-comparison]]（其动机叙事——"数据集依赖范式失效→主动塑形新范式"——是一个可对比的 motivation 模式）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| ClawHub 技能 65,699 个（2026-06），多轮技能超 1/3（教育领域 >50%）；约 68% 已安装技能通过描述影响流量 | Figure 1、Figure 4(a)(b)、§IV-B | §II-A、§IV-B |
| 同一意图换语言风格后流量可差 10×；两类问题在 t-SNE 上从清晰分离变为完全重叠 | Figure 3、§III-B | §III-B |
| 解码性能：T2 判据 TPR 92.5%/FPR 13%；T2+T3 TPR 98.8%/FPR 8% | Table III、§V-C | §V-C |
| 跨领域一致性：第 2 轮起 11 个领域一致性改善 >2×，第 3 轮流量结构高度相似 | Figure 9 左、§V-B | §V-B |
| 编码维度可用性：包大小（"at least x chars" 最佳；exactly/at most 明显更差）、时序（bash sleep、web 搜索等待）、方向（轮次边界）；延迟塑形与包大小存在跨维度冲突 | Figure 5–8、§IV-B | §IV-B |
| 所有改造技能通过 LLM 安全审计，被解读为面向特定人群的个性化 | §V-D | §V-D |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-arXiv-SkillWatermark__An_Embedded_Skill_Watermark_of_Progressive_Privacy_Inference_via_Benign_Prompts.pdf
- MinerU Markdown：02-parsed-markdown/2026-arXiv-SkillWatermark__An_Embedded_Skill_Watermark_of_Progressive_Privacy_Inference_via_Benign_Prompts.md

---

## 12. 后续问题

- 暂未整理。

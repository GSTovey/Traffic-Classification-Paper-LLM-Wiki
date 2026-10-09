---
type: paper
title_original: "Practice Makes (Im)Perfect: A Look Back at Benchmarking Practices for Microarchitectural Side-Channel Attacks"
title_cn: "熟未必生巧：微架构侧信道攻击基准测试实践回顾"
authors: [Iliana Fayolle, Daniel De Almeida Braga, Antoine Geimer, Clémentine Maurice]
year: 2026
venue: "CCS 2026"
doi: "10.1145/3830454.3846555"
url: "https://arxiv.org/abs/2609.03893"
pdf: "00-inbox/PDFs/2026-arXiv-Practice_Makes_(Im)Perfect__A_Look_Back_at_Benchmarking_Practices_for_Microarchitectural_Side-Channel_Attacks.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-Practice_Makes_(Im)Perfect__A_Look_Back_at_Benchmarking_Practices_for_Microarchitectural_Side-Channel_Attacks.md"
status: processed
reading_level: L1
research_area: []
task: []
method: []
dataset: ["自建语料：83 篇微架构侧信道论文（2014–2024，CCS/NDSS/S&P/USENIX Security/ASPLOS/HPCA/ISCA/MICRO）"]
code: "https://github.com/Naeele/Practice_Makes_-Im-Perfect---Artifacts"
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

# Practice Makes (Im)Perfect: A Look Back at Benchmarking Practices for Microarchitectural Side-Channel Attacks

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Practice Makes (Im)Perfect: A Look Back at Benchmarking Practices for Microarchitectural Side-Channel Attacks |
| 中文标题 | 熟未必生巧：微架构侧信道攻击基准测试实践回顾 |
| 作者 | Iliana Fayolle, Daniel De Almeida Braga, Antoine Geimer, Clémentine Maurice（Univ. Lille/CNRS/Inria、Univ. Rennes/CNRS/IRISA） |
| 年份 | 2026 |
| 会议/期刊 | CCS '26（解析稿首页无会议页眉；DOI 10.1145/3830454.3846555 与 AVP-Inspect 同属 ACM 论文集 3830454，推断为 CCS '26 会议论文；原按分配登记为 arXiv 2026，聚合时已更正） |
| 研究方向 | 微架构侧信道与隐蔽信道攻击的评估方法学（元分析/综述，非流量分析主题） |
| 任务类型 | 系统文献综述 + 缺陷量化统计（无模型训练任务） |
| 方法关键词 | systematic review、codebook 标注、19 类基准测试缺陷分类、评估属性清单 |
| 数据集 | 自建语料：83 篇论文（2014–2024，8 个顶会），涉及 218 个攻击 |
| 是否开源 | 是，数据与脚本见 GitHub `Naeele/Practice_Makes_-Im-Perfect---Artifacts`（附录 A） |
| PDF | 00-inbox/PDFs/2026-arXiv-Practice_Makes_(Im)Perfect__A_Look_Back_at_Benchmarking_Practices_for_Microarchitectural_Side-Channel_Attacks.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-arXiv-Practice_Makes_(Im)Perfect__A_Look_Back_at_Benchmarking_Practices_for_Microarchitectural_Side-Channel_Attacks.md |

---

## 1. 一句话总结

> 系统审查 2014–2024 年 8 个顶会 83 篇微架构侧信道论文，归纳出 19 类基准测试缺陷（每篇平均 5.5 处），并给出面向作者/审稿人/社区的评估建议。

---

## 2. 摘要翻译

### 2.1 摘要原文

> "We survey 83 attack papers published in top-ranked security and architecture conferences from 2014 to 2024. From this corpus, we identify and define 19 recurrent benchmarking flaws that afect evaluation completeness, relevance, soundness, and reproducibility. These flaws include unfair or absent comparisons, missing code or materials, and the failure to evaluate the key attack properties. On average, each paper exhibits 5.5 such flaws..."（Abstract，节选）

### 2.2 摘要中文翻译

微架构侧信道研究近年高速膨胀，对严谨、有意义的基准测试的需求随之上升。早期攻击论文依赖间接代理指标（如隐蔽信道带宽、对朴素 AES/RSA 实现的密钥恢复），这些做法成为事实标准并被后续工作不断复制，有时甚至直接对比旧论文的原始数字。这些做法虽便于比较，但当前的基准测试未必能评估新原语的特定属性；更严重的是，微架构攻击对实验条件极度敏感，目标系统的微小变动即可显著改变结果，不当的评估实践因而损害可复现性，即使在顶会中也如此。本文系统调查 2014–2024 年顶会（安全与体系结构）发表的 83 篇攻击论文，识别并定义 19 类反复出现的基准测试缺陷，涉及评估的完整性、相关性、可靠性与可复现性，包括不公平或缺失的对比、缺失代码/材料、未评估关键攻击属性等。平均每篇论文有 5.5 处此类缺陷。基于发现，作者提出评估新攻击应关注的关键属性，并分析随时间变化的趋势以及安全与体系结构社区间的实践差异。

> ⚠️ MinerU 解析问题：标题被解析为 "Atacks"（应为 "Attacks"）；正文存在 fi/ff 连字丢失（diferent→different、afect→affect、of→off、efort→effort）。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

领域内长期缺少对"如何有意义地评估和比较微架构侧信道攻击"的反思（§1）：基准测试沿用历史做法（攻击 AES T-table、平方乘幂运算、最大化隐蔽信道带宽），而这些问题早已被修补，基准的意义存疑。

### 3.2 现有方法的痛点和不足

三个核心痛点（§1）：① 基准过时、与被评估原语的真实能力脱节；② 实现与实验条件各异，无法"apple-to-apple"比较（如带纠错与协议栈的隐蔽信道无法与 20% 错误率的裸比特信道对比）；③ 可复现性差——代码不可得或不可用，且论文常省略关键工程细节。

### 3.3 论文的研究假设或核心直觉

核心直觉：把"一个有意义的评估应当暴露哪些属性"形式化为一套属性清单与统一编码本，再对大规模语料逐篇标注，即可把"评估质量差"从主观印象转化为可量化、可跨年份/跨社区比较的统计事实（§3.1、§4）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 同一原语（如 Prime+Probe）报告数字跨度极大；"错误率"定义在不同论文中不一致（Edit 距离 vs Hamming 距离 vs 未说明） | §2 |
| 痛点提炼 | 原始带宽数字不可比、可复现性差，读者被误导，顶会亦未能识别此类问题 | §1、§2 |
| 问题转化 | 把工程问题提升为"如何评估新原语的关键属性"这一评估方法学问题 | §1 |
| 文献定位 | 既有工作未系统研究评估实践本身；本文以 83 篇语料做 meta-analysis 填补空白 | §3.1 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 顶会微架构侧信道论文普遍存在可归类、可量化的基准测试缺陷 | §1、推断 | 83 篇语料的系统编码与统计 |
| 辅助假设（如有） | 安全与体系结构社区、不同年份的实践存在可测差异 | §1 | 分组统计 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 缺陷普遍存在 | 支撑 | 平均每篇 5.5 处缺陷；语料内无一篇零缺陷；77 篇（92.8%）至少含 1 处 full 缺陷 | §6、§4 |
| 社区差异 | 支撑 | 文中报告了安全/架构会议间的实践差异与时间趋势 | §7 |

---

## 4. 方法设计

### 4.1 方法整体流程

设计结构化调查表与通用编码本（codebook）→ 筛选 2014–2024 年 8 个顶会论文得到 83 篇语料 → 逐篇标注评估要素（原语类型、评估目标、目标与平台、指标、对比、artifact 可得性）→ 归纳出 19 类缺陷（A 基准缺失 A1–A7、B 不当对比 B1–B4、C 信息缺失 C1–C8）→ 统计分布、趋势与社区差异 → 给出推荐清单（§3、§4、§7）。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | 8 个会议的论文池 | 按预设标准筛选 2014–2024 年微架构侧信道攻击论文 | 83 篇语料（含 218 个攻击） | 确定分析对象 |
| Step 2 | 83 篇论文全文 | 用编码本逐篇标注评估要素与缺陷（full/partial） | 结构化标注数据 | 把定性判断转为可统计变量 |
| Step 3 | 标注数据 | 统计缺陷出现率、每篇缺陷数、时间趋势、社区差异 | 缺陷分布与趋势结论 | 支撑 19 类缺陷的普遍性论断 |
| Step 4 | 统计分析结果 | 提炼关键评估属性与检查清单 | 面向作者/审稿人/社区的推荐 | 给出可操作改进建议 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 调查表/编码本 | 统一评估要素的词汇与判据 | 论文评估章节 | 逐篇编码记录 | 供 Step 2 使用 |
| 缺陷分类体系 | 19 类缺陷（A/B/C 三类） | 编码记录 | 缺陷标签 | 统计的基础 |
| 评估属性清单与推荐 | 定义"应当暴露的属性" | 统计分析 | 检查清单 | 最终产出 |

### 4.4 公式、算法和机制解释

本文为元分析，无新算法或公式。关键机制是把常见的评估争议（带宽可比性、错误率定义、ECC 是否声明、威胁模型是否匹配）转写为可核查的标注判据（§2、§4）。

### 4.5 方法优势

覆盖 10 年、8 个顶会的 83 篇语料，规模与代表性较强；缺陷分类可复用为审稿清单；数据与脚本公开，结论可复核（§1、附录 A）。

### 4.6 方法不足

语料限于 8 个会议与 2014–2024 年，结论外推到其他社区/年份需谨慎；标注依赖作者判断，存在主观性与评审偏差（文中自述局限，§3 末）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

不同于提出新攻击或新原语的常规论文，本文研究对象是"评估实践"本身；也不同于既有协议/实现层面 SoK，它不梳理攻击技术谱系，而是量化评估缺陷在顶会语料中的分布（§3）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 19 类基准测试缺陷分类 | 覆盖完整性/相关性/可靠性/可复现性四维度 | 高 | 是（可迁移到流量分析评估审查） |
| 大规模评估实践量化 | 83 篇语料、每篇 5.5 处缺陷、跨年份与社区趋势 | 高 | 是 |
| 评估属性清单与推荐 | 面向作者/审稿人/PC/社区的检查清单 | 中 | 是 |

### 5.3 适用场景

① 微架构侧信道论文的自我审查与审稿；② 任何"以旧基准数字做对比"的实验领域（本文特别指出分类式评估如 website/application fingerprinting 的细节缺失影响可复现性，§4 C5）；③ 构建领域评估规范时的方法论参考。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 常规攻击论文自定基准 | 灵活、贴合具体原语 | 不可比、常省略细节、遗留旧基准 | 给出统一属性清单与缺陷标签 |
| 既有 SoK/综述 | 系统整理技术谱系 | 不量化评估质量 | 以编码本对评估实践做统计 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

对 83 篇语料（2014–2024，安全：CCS/NDSS/S&P/USENIX Security；体系结构：ASPLOS/HPCA/ISCA/MICRO）逐篇标注并统计缺陷出现率、每篇缺陷数与趋势（§3、§6）。

### 6.2 数据集

自建语料共 83 篇论文、218 个攻击，其中侧信道 147 个（67.4%）、隐蔽信道 71 个（32.6%）；73 篇（88%）面向 CPU，65 篇（78.3%）使用 Intel 平台（§5、Fig. 5）。

### 6.3 Baseline

无机器学习 baseline；对照对象是"论文自述的评估实践"与本文提出的属性清单（元分析范式）。

### 6.4 评价指标

各类缺陷在语料中的出现比例、每篇论文平均缺陷数、full/partial 缺陷分布。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| 83 篇语料 | 平均缺陷数/篇 | 5.5 | — | — | 语料内无零缺陷论文 |
| 83 篇语料 | B1 不公平对比占比 | 67.3% | — | — | 多与旧论文原始数字直接比较 |
| 83 篇语料 | C3 无代码/材料占比 | 49.4% | — | — | 三种缺失形态 |
| 83 篇语料 | A6 单一平台评估占比 | 20.7% | — | — | 通常为单 CPU 型号 |
| 语料中 fingerprinting 攻击 | 攻击数 | 23 | — | — | 其中 9 个（39.1%）未指明受害者 |

### 6.6 优势最明显的场景

揭示"顶会论文同样普遍存在评估缺陷"这一系统性事实，并给出安全 vs 体系结构社区、不同年份的差异对比，为社区规范提供实证依据（§6、§7）。

### 6.7 局限性

语料选择与缺陷编码依赖人工判断；部分缺陷（如"评估是否充分"）带主观性；未覆盖 2024 年后论文与其他会议（文中自述，§3）。

---

## 7. 学习与应用

### 7.1 是否开源？

是：数据与脚本随附录 A 发布于 GitHub（`Naeele/Practice_Makes_-Im-Perfect---Artifacts`），并做 Software Heritage 存档。

### 7.2 复现关键步骤

1. 按论文的会议/年份/主题筛选标准重建 83 篇语料；
2. 使用其编码本与 19 类缺陷判据逐篇标注；
3. 复算缺陷出现率、每篇缺陷数与分组统计，核对结论。

### 7.3 关键超参数、预处理和训练细节

无（元分析）；关键"参数"是编码本的判据定义与 full/partial 缺陷的判定规则（§3、§4）。

### 7.4 能否迁移到其他任务？

可以：19 类缺陷中的多数（不公平对比、缺代码、错误率定义不清、单选数据集）在加密流量分类与 WF 论文中同样常见，可直接改写成流量分析领域的评估审查清单；"不要直接引用旧论文原始数字""声明指标定义""报告噪声鲁棒性"等建议对 WF/ETC 实验设计有直接约束意义（§7 推荐与 §4 C5 关于 fingerprinting 分类细节缺失的讨论）。

### 7.5 对我的研究有什么启发？

写流量分析实验章节时，应显式声明：错误率/精度的计算方式、ECC 或后处理是否包含、对比方法的运行环境是否一致、是否跨平台/跨时间验证、artifact 是否可获取——本文给出了现成的检查项模板。

---

## 8. 总结

### 8.1 核心思想

> 用缺陷清单量化审查侧信道基准测试实践。

### 8.2 速记版 Pipeline

1. 定编码本与筛选标准，得 83 篇语料（2014–2024、8 会）；
2. 逐篇标注评估要素与缺陷（full/partial）；
3. 归纳 19 类缺陷（A 基准缺失 / B 不当对比 / C 信息缺失）；
4. 统计出现率（B1 67.3%、C3 49.4%、A6 20.7% 等）与社区/年份差异；
5. 输出评估属性清单与面向作者/审稿人/社区的推荐。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]]（语料含 23 个 fingerprinting 类缓存攻击、占 20.5%，其分类细节缺失缺陷 C5 直接讨论 website/application fingerprinting）

### 9.2 相关方法

- 库内无对应方法页：本文无新 ML 方法，方法学贡献为编码本与缺陷分类体系。

### 9.3 相关任务

- 库内暂无直接对应的任务页（元分析不面向具体流量任务）；最近邻为 [[website-fingerprinting]]（仅作语料对象，非本文任务）。

### 9.4 可更新的综述页面

- [[claims-index]]（可沉淀"微架构侧信道/分类式攻击的评估缺陷普遍性"类证据条目；本文属跨领域证据，需标注主题限定）

### 9.5 可加入的对比表

- [[open-source-registry]]（本文在附录 A 公开数据与脚本，并做 Software Heritage 存档，可登记 artifact）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 83 篇语料、平均每篇 5.5 处缺陷、无零缺陷论文 | "average of 5.5 issues per paper" | §9（结论）/ §6 |
| 67.3% 论文存在不公平对比（与不同设置/硬件/威胁模型的原始数字比较） | "B1 Unfair comparisons to other work. 67.3%..." | §5.4 |
| 49.4% 论文不提供任何代码/材料 | "C3 No code/materials/artifact. 49.4%..." | §5.5 |
| 20.7% 论文仅在单一平台评估 | "A6 Evaluated on a single platform. 20.7%..." | §5.3 |
| 分类式评估（website/application fingerprinting）细节缺失损害可复现性；语料含 23 个 fingerprinting 攻击，39.1% 未指明受害者 | C5 讨论；Fig. 5 统计 | §4 C5 / §6 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-arXiv-Practice_Makes_(Im)Perfect__A_Look_Back_at_Benchmarking_Practices_for_Microarchitectural_Side-Channel_Attacks.pdf
- MinerU Markdown：02-parsed-markdown/2026-arXiv-Practice_Makes_(Im)Perfect__A_Look_Back_at_Benchmarking_Practices_for_Microarchitectural_Side-Channel_Attacks.md

---

## 12. 后续问题

- 暂未整理。

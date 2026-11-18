---
type: "paper"
title_original: "CenRL: A Framework for Performing Intelligent Censorship Measurements"
title_cn: "基于自适应采样的互联网审查测量框架"
authors: ["Hieu Le", "Armin Huremagic", "Kevin Wang", "Roya Ensafi", "Ram Sundara Raman"]
year: 2026
venue: "S&P"
source_version: "IEEE Symposium on Security and Privacy 2026 正式论文。"
doi: "10.1109/sp63933.2026.00098"
url: "https://doi.org/10.1109/sp63933.2026.00098"
pdf: "00-inbox/PDFs/2026-S&P-CenRL__A_Framework_for_Performing_Intelligent_Censorship_Measurements.pdf"
mineru_md: "02-parsed-markdown/2026-S&P-CenRL__A_Framework_for_Performing_Intelligent_Censorship_Measurements.md"
status: "processed"
reading_level: "L3"
deep_analysis_reviewed: "2026-11-18"
research_area: ["互联网审查测量", "主动网络测量"]
task: ["发现受阻内容", "追踪封锁变化"]
method: ["多臂赌博机", "UCB", "动态预算分配"]
dataset: ["Tranco Top-10K", "Citizen Lab Regional Test Lists", "GFWatch", "Censored Planet / Hyperquack", "RU 与 KZ 控制测量列表"]
code: "https://doi.org/10.5281/zenodo.17382167"
relevance: "medium"
created: "2026-11-18"
updated: "2026-11-18"
metadata_source: "Crossref"
source_sha256: "71679cf90442e3ce3bcf5334c745c63fb94cc23f9b86460df84bb208f356a1e6"
internal_citation_count: 0
citation_impact: 0.8
composite_weight: 0.8
citation_count_scope: "verified DOI or normalized complete titles in vault References; lower bound"
citation_count_verified: "2026-11-18"
---

# CenRL: A Framework for Performing Intelligent Censorship Measurements

## 0. 论文基础信息

| 项目 | 内容 |
| --- | --- |
| 原文标题 | CenRL: A Framework for Performing Intelligent Censorship Measurements |
| 中文标题 | 基于自适应采样的互联网审查测量框架 |
| 作者 | Hieu Le、Armin Huremagic、Kevin Wang、Roya Ensafi、Ram Sundara Raman |
| 年份 | 2026 |
| 会议/期刊及版本 | IEEE Symposium on Security and Privacy 2026 正式论文。 |
| DOI | 10.1109/sp63933.2026.00098 |
| 题录来源 | Crossref |
| 研究方向 | 互联网审查测量、主动网络测量 |
| 任务类型 | 发现受阻内容、追踪封锁变化 |
| 方法关键词 | 多臂赌博机、UCB、动态预算分配 |
| 数据集 | Tranco Top-10K；Citizen Lab Regional Test Lists；GFWatch；Censored Planet / Hyperquack；RU 与 KZ 控制测量列表 |
| 开源状态 | 论文首页标有 Artifact Evaluated/Available，随文给出 Zenodo artifact DOI。会议产物清单与 Zenodo 记录均已核对。引用时区分 10.1109/SP63933.2026.00098 论文 DOI 与产物 DOI。 |
| PDF | [[00-inbox/PDFs/2026-S&P-CenRL__A_Framework_for_Performing_Intelligent_Censorship_Measurements.pdf]] |
| MinerU Markdown | [[02-parsed-markdown/2026-S&P-CenRL__A_Framework_for_Performing_Intelligent_Censorship_Measurements.md]] |

题录核验见 [出版记录](https://doi.org/10.1109/sp63933.2026.00098)。

## 1. 一句话总结

CenRL 把有限的网站连通性测量次数分配给不同网站组，利用历史反馈发现更多封锁和更早发现变化。

## 2. 摘要翻译

### 2.1 摘要原文

见 [[00-inbox/PDFs/2026-S&P-CenRL__A_Framework_for_Performing_Intelligent_Censorship_Measurements.pdf]] 第 1 页 Abstract。

### 2.2 摘要中文翻译

主动测量的时间和资源有限，发现新变化通常依赖人工挑选目标。CenRL 用多臂赌博机在不同网站类别或属性组间分配测量。三地区的受控实验验证静态发现与动态响应，15 国远程观测点的实验检验有限测量预算下的效率。

## 3. 方法动机

排名优先和随机选点不随过去的测量反馈变化。网站类别、后缀、排名等属性有时共享阻断行为，因此可以在固定预算下利用这种相关性（§2–3）。

### 3.4 问题发现路径

| 阶段 | 分析 | 出处 |
| --- | --- | --- |
| 现象观察 | 测量次数有限，固定排序会集中在原本容易选中的网站。 | §1–2 |
| 提炼困难 | 站点组内阻断可能相关，且变化会削弱过去反馈。 | §3.1–3.3，§6.1 |
| 转换问题 | 同候选范围与测量预算下，在线反馈是否改善已知/新发生阻断的发现时间？ | §3.3–3.4，§5.1 |
| 文献对照 | 同一受控名单对照随机、排名和非学习规则，实际平台对照静态 Hyperquack。 | §5.1–5.2 |

### 3.5 科学假设形成

若站点分组具有可迁移的阻断相关性，早期反馈就能为后续测量提供信息。若少量规则或历史样本失去代表性，反馈带来的发现收益会减少。

## 4. 方法设计

### 4.1 输入、处理与输出

| 步骤 | 输入 | 处理 | 输出 |
| --- | --- | --- | --- |
| 定义测量范围 | 候选域名和属性 | 按类别、后缀、排名等建立候选组 | 可独立跟踪收益的组 |
| 分配测量 | 预算、先验和测量反馈 | 在探索与利用之间选择测量组，按是否观测到封锁或变化更新组收益 | 随时间调整的测量计划 |
| 比较发现效率 | 固定实验组和测量轮次 | 统计同预算发现量与达到指定覆盖所需测量次数 | 发现曲线和动态变化响应 |

### 4.2 机制与条件

§3.3 分别定义当前封锁与动态变化奖励。§3.4 以 UCB 为主要策略，附录比较 ε-greedy 和 Thompson Sampling。观察到的反馈受选点策略影响，分析环境总体封锁率应保留抽样框和独立验证。

### 4.3 机制拆解与可检验条件

**选择对象与反馈。** 给定网站集合 $I$，将某一属性划分下的站点组作为臂，例如类别、顶级域或实体。实际反馈是某观测点上当前测量是否出现阻断。基础奖励 $R_1$ 对命中计 1。动态奖励 $R_2$ 将新阻断、继续阻断和解除阻断分别计 1、3/4 和 1/2，按日窗口记录历史状态（§3.2–3.3，式 1–2）。目标函数决定何谓早发现，不能用日历时间替代固定预算下的测量步数。

**探索与适配。** UCB 把当前估计的组收益与随访问次数下降的探索项相加。新反馈用移动平均更新组收益。论文对照 ε-greedy 和 Thompson Sampling（§3.4、附录 C）。真实测量先用同观测点的历史记录选超参数，之后执行固定 2,000 次 HTTPS 测量。配置依赖站点的历史数据可用性（§5.2）。

## 5. 与其他方法对比

与 Tranco 随机、按排名和其他规则调度比较受控发现效率，与原始 Hyperquack 比较真实测量发现量。

### 5.2 方法对比与可归因性

| 方案或观测层 | 区分点 | 评估条件 |
| --- | --- | --- |
| Tranco 随机 / 排名 | 受控场景共用 Top–10K 和预算 | 比较反馈调度对发现曲线的贡献 |
| 原始 Hyperquack | 固定前 2,000 域作为输入 | 实际平台比较也包含候选范围差异 |
| CenRL Hyperquack | 从 Top–10K 自适应选测 2,000 次 | 检验实际发现量，测量视角单点 |

## 6. 实验表现与局限性

### 6.1 设置、数据与对照

使用 CN、RU、KZ 的已有阻断列表构造受控环境，按静态与动态设置区分。实际观测用 15 国观测点和 Tranco 候选范围，每点的可观察连接条件不同。

- 基线　Tranco Random、Rank Order、按类别/实体的规则调度、vanilla Hyperquack。
- 指标　同预算发现的站点数、达到目标覆盖的测量次数与随时间变化的响应。

### 6.2 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 对照 | 差异 | 原文定位 |
| --- | --- | --- | --- | --- | --- |
| 三地区受控实验 | 达到 75% 发现所需测量 | 相对测量数低于一半 | 论文中的既有测量策略 | — | 摘要及 §6.1，条件见各图 |
| KZ 受控动态事件第二天 | 找到前 100 个受阻站点的测量次数 | 158（均值） | Tranco Random 1,075 | 约 6.8 倍更少测量 | §6.1.2 图 5，单事件 |
| 15 国真实观测点 | 发现站点数 | 摘要约 2.5 倍，§6.2 报 2.75 倍 | 原始 Hyperquack | 聚合口径待核 | 摘要与正文各自记录，§6.2 图 9 |

### 6.4 关键对照、反例与证据边界

| 证据 | 原文复核结果 | 定位 |
| --- | --- | --- |
| 真实观测点示例 | 阿联酋观测点检出 568 个，静态对照 102 个。斯里兰卡观测点为 499 对 215。 | §6.2 图 9，站点数 |
| 聚合数字 | 摘要报平均约 2.5 倍，§6.2 正文报 2.75 倍。两处分别记录，引用聚合值前需核对汇总分母。 | 摘要、§6.2 |
| 实际对照的边界 | 双方测量次数相同，候选范围不同。每国只有一个观测点。 | §5.2 表 3 |

### 6.7 局限性

Tranco 样本范围和远端观测点制约外推。个别低阻断站点环境缺少足够反馈，文中存在持平或少发现的观测点。模拟阻断列表的覆盖也不同于现实总体。

## 7. 学习与应用

### 7.1 开源状态

论文首页标有 Artifact Evaluated/Available，随文给出 Zenodo artifact DOI。会议产物清单与 Zenodo 记录均已核对。引用时区分 10.1109/SP63933.2026.00098 论文 DOI 与产物 DOI。

[作者公开仓库或产物](https://doi.org/10.5281/zenodo.17382167)。

### 7.2 复核要点

先用论文提供的受控列表复核观测预算下的曲线，统一初始候选集合。比较列表覆盖缺失及静态/动态条件，记录低反馈组。

### 7.3 可迁移的研究问题

可用来组织防御研究的标注或测量优先级。区分自适应抽中的难例与固定评估队列，尤其要避免把抽样后的难例比率当部署基率。

### 7.4 独立复核与迁移设计

用由历史记录构成的固定测量矩阵比较同候选、同预算下的静态调度和 UCB。把按策略选择的难例用于诊断，另保留无策略选择的评估队列，用于估计总体基率或 FPR。对照 COSINT 的背景流评价时，明确难例选择机制和负类分母。

## 8. 总结

用测量反馈动态安排探测预算。

定义测量范围 → 分配测量 → 比较发现效率。

## 9. Obsidian 知识链接

- 概念　[[04-concepts/censorship-circumvention]]、[[04-concepts/network-telemetry]]。
- 任务　[[06-tasks/network-traffic-measurement]]。
- 对比与相邻资料　[[method-comparison-table]]。

- 补充对照　[[03-paper-notes/2026-COSINT-北邮时金桥|COSINT 汇报]]。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
| --- | --- | --- |
| 自适应调度在相同测量预算下改善覆盖 | 三地区受控发现曲线 | §6.1 图 2、5–7 |
| 效果依赖观测点和反馈密度 | 15 国远程测量结果存在例外 | §6.2 图 9 |

## 11. 原始资料链接

- PDF　[[00-inbox/PDFs/2026-S&P-CenRL__A_Framework_for_Performing_Intelligent_Censorship_Measurements.pdf]]
- MinerU Markdown　[[02-parsed-markdown/2026-S&P-CenRL__A_Framework_for_Performing_Intelligent_Censorship_Measurements.md]]
- MinerU 原始归档　[[01-mineru-output/2026-S&P-CenRL__A_Framework_for_Performing_Intelligent_Censorship_Measurements/full.md]]

## 12. 后续问题

优先检验 §6.7 的主要限制，按 §7.2 记录数据、观测和指标条件。

## 13. 写作叙事与故事线分析

先给测量预算和变化两个问题，再定义决定测哪里与未来如何调整的反馈，最后按受控与实测分别报告。

### 13.2 证据组织与写作借鉴

受控部分将固定预算和动态变化分开验证。真实部署同时改变站点选择范围和调度，写作时补上这一点，避免把全部收益归因于 UCB。

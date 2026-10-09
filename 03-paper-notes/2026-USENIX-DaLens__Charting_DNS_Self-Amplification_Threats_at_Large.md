---
type: paper
title_original: "THE ADVANCED COMPUTING SYSTEMS ASSOCIATION"
title_cn: ""
authors: []
year: 2026
venue: USENIX
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-USENIX-DaLens__Charting_DNS_Self-Amplification_Threats_at_Large.pdf"
mineru_md: "02-parsed-markdown/2026-USENIX-DaLens__Charting_DNS_Self-Amplification_Threats_at_Large.md"
status: processed
reading_level: L2
research_area: []
task: []
method: []
dataset: []
code: unknown
relevance: medium
created: "2026-09-29"
updated: "2026-09-29"
---

# THE ADVANCED COMPUTING SYSTEMS ASSOCIATION

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | THE ADVANCED COMPUTING SYSTEMS ASSOCIATION |
| 年份 | 2026 |
| 会议/期刊 | USENIX |
| PDF | [[2026-USENIX-DaLens__Charting_DNS_Self-Amplification_Threats_at_Large.pdf]] |
| MinerU Markdown | [[2026-USENIX-DaLens__Charting_DNS_Self-Amplification_Threats_at_Large.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
The emerging self-amplification attacks (SAAs) pose serious denial-of-service (DoS) risks to the Domain Name System (DNS). They can substantially amplify the interactions between recursive and authoritative servers, depleting resources at disproportionally small costs. Assessing the impact of such attacks on the global name resolution infrastructure is crucial for DNS operators to effectively triage threats and deploy defenses, yet this remains an uncharted and daunting territory. We have conducted the first large-scale measurement study of SAAs, leveraging a versatile framework, DaLens, which we designed and developed. The work consists of untangling the intricate Open DNS infrastructure to identify effective amplifiers and quantifying their amplification capabilities in a modular, scalable, and sound manner. Out of 307K persistent public resolvers, we find 29K unique resolver clusters that can be exploited in parallel for SAAs, and a significant number of them can still produce large amplification effects even though these vulnerabilities had already been disclosed in prior work.

## 3. 方法分析
- 输入：论文所研究的网络流量、协议、系统或安全数据（以全文为准）。
- 处理：论文提出的方法或分析流程（摘要级自动提取，待核验）。
- 输出：分类、检测、预测、攻击/防御或系统验证结果。

## 4. 实验表现
- 数据集：待从全文核验。
- Baseline：unknown。
- 指标与数值：不补造，待表格核验。

## 5. 局限性与复现建议
- 当前笔记完成自动入库和摘要级分析，未替代人工深读。
- 先核验数据来源、代码状态、划分和指标，再决定复现等级。

## 6. 知识链接
- [[traffic-classification]]
- [[encrypted-traffic-analysis]]

## 7. 证据状态
- MinerU：已完成；解析质量需人工抽查。
- Bib 元数据：待官方 API/论文首页核验。


## 深度分析（自动证据提取，需人工复核）

### 研究问题与证据
- 主题线索：dns, tor, adversarial, quic。
- 摘要证据：The emerging self-amplification attacks (SAAs) pose serious denial-of-service (DoS) risks to the Domain Name System (DNS). They can substantially amplify the interactions between recursive and authoritative servers, depleting resources at disproportionally small costs. Assessing the impact of such attacks on the global name resolution infrastructure is crucial for DNS operators to effectively triage threats and deploy defenses, yet this remains an uncharted and daunting territory. We have conducted the first large-scale measurement study of SAAs, leveraging a versatile framework, DaLens, which we designed and developed. The work consists of untangling the intricate Open DNS infrastructure to identify effective amplifiers and quantifying their amplification capabilities in a modular, scalable, and sound manner. Out of 307K persistent public resolvers, we find 29K unique resolver clusters that can be exploited in parallel for SAAs, and a significant number of them can still produce large amplification effects even though these vulnerabilities had already been disclosed in prior work.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。

## 深度分析（2026-09-29）

- reading_level: L3
- 研究定位：DNS自放大/大规模测量
- 方法机制：DaLens解析开放DNS基础设施，寻找递归—权威交互中的自放大器并量化放大能力；在307K持久公共解析器中发现29K可并行利用的解析器集群。
- 输入—处理—输出：输入开放DNS测量与依赖拓扑；输出可利用集群、放大倍数和风险排序。
- 证据边界：摘要提供规模结论；测量伦理、放大定义、时间窗口和已披露漏洞残留需正文核验。
- 联动标签：website-fingerprinting；DNS；anomaly-detection；traffic-security


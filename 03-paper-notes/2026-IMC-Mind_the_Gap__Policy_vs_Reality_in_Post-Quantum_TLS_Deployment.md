---
type: paper
title_original: "Mind the Gap: Policy vs Reality in Post-Quantum TLS Deployment"
title_cn: ""
authors: []
year: 2026
venue: IMC
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-IMC-Mind_the_Gap__Policy_vs_Reality_in_Post-Quantum_TLS_Deployment.pdf"
mineru_md: "02-parsed-markdown/2026-IMC-Mind_the_Gap__Policy_vs_Reality_in_Post-Quantum_TLS_Deployment.md"
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

# Mind the Gap: Policy vs Reality in Post-Quantum TLS Deployment

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Mind the Gap: Policy vs Reality in Post-Quantum TLS Deployment |
| 年份 | 2026 |
| 会议/期刊 | IMC |
| PDF | [[2026-IMC-Mind_the_Gap__Policy_vs_Reality_in_Post-Quantum_TLS_Deployment.pdf]] |
| MinerU Markdown | [[2026-IMC-Mind_the_Gap__Policy_vs_Reality_in_Post-Quantum_TLS_Deployment.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
论文未明确提取摘要。

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
- 摘要证据：Post-<sub>q</sub>uantum cr<sub>yp</sub>to<sub>g</sub>ra<sub>p</sub>h<sub>y</sub> (PQC) has evolved from a lon<sub>g</sub>-term <sub>p</sub>lannin<sub>g</sub> concern into an o<sub>p</sub>erational <sub>p</sub>riorit<sub>y</sub>. Followin<sub>g</sub> NIST’s standardization of PQC algorithms, governments and standards bodies <sub>p</sub>ublished transition roadma<sub>p</sub>s outlinin<sub>g</sub> mi<sub>g</sub>ration timelines<sub>,</sub> <sub>p</sub>riorit<sub>y</sub> sectors<sub>,</sub> and de<sub>p</sub>lo<sub>y</sub>ment strate<sub>g</sub>ies. However<sub>,</sub> our <sub>survey</sub> <sub>o</sub>f th<sub>ese</sub> <sub>po</sub>li<sub>c</sub>i<sub>es</sub> <sub>revea</sub>l<sub>s</sub> <sub>su</sub>b<sub>s</sub>t<sub>an</sub>ti<sub>a</sub>l di<sub>vergence</sub> i<sub>n</sub> t<sub>ec</sub>h<sub>n</sub>i<sub>ca</sub>l prescriptions and urgency. It remains unclear how widely PQC has b<sub>een a</sub>d<sub>op</sub>t<sub>e</sub>d i<sub>n prac</sub>ti<sub>ce an</sub>d h<sub>ow po</sub>li<sub>cy</sub> dif<sub>erences</sub> t<sub>rans</sub>l<sub>a</sub>t<sub>e</sub> i<sub>n</sub>t<sub>o</sub> <sub>o</sub>b<sub>serva</sub>bl<sub>e</sub> d<sub>ep</sub>l<sub>oymen</sub>t <sub>ou</sub>t<sub>comes.</sub> To <sub>q</sub>uantif<sub>y</sub> trends in <sub>p</sub>ublic-facin<sub>g p</sub>ost-<sub>q</sub>uantum TLS (PQ-TLS) ado<sub>p</sub>tion, we conduct three measurement rounds between Jul<sub>y</sub> 2025 <sub>a</sub>nd M<sub>a</sub>r<sub>c</sub>h 2026<sub>, cove</sub>rin<sub>g o</sub>n<sub>e</sub> milli<sub>o</sub>n <sub>pu</sub>bli<sub>c</sub> HTTPS <sub>e</sub>nd-<sub>po</sub>i<sub>n</sub>t<sub>s.</sub> A<sub>cross</sub> th<sub>ese roun</sub>d<sub>s, we es</sub>t<sub>a</sub>bli<sub>s</sub>h <sub>more</sub> th<sub>an</sub> t<sub>wo</sub> billi<sub>on</sub> TLS 1<sub>.</sub>3 h<s

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：未检测到明确 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


## 深度分析（并行深度分析更新 2026-09-29）

### 方法、实验与证据
论文以DomCop Top10M域名为目标，三轮（2025-07/11、2026-03）TLS1.3扫描并结合政策调查；成功定义为所有测点三轮均完成握手，684,494域（68.44%）满足。政策仅作上下文，不做因果估计。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。

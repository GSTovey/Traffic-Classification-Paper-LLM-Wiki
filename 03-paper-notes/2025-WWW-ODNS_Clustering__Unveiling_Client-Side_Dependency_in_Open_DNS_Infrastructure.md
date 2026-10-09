---
type: paper
title_original: "ODNS Clustering: Unveiling Client-Side Dependency in Open DNS Infrastructure"
title_cn: ""
authors: []
year: 2025
venue: WWW
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2025-WWW-ODNS_Clustering__Unveiling_Client-Side_Dependency_in_Open_DNS_Infrastructure.pdf"
mineru_md: "02-parsed-markdown/2025-WWW-ODNS_Clustering__Unveiling_Client-Side_Dependency_in_Open_DNS_Infrastructure.md"
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

# ODNS Clustering: Unveiling Client-Side Dependency in Open DNS Infrastructure

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | ODNS Clustering: Unveiling Client-Side Dependency in Open DNS Infrastructure |
| 年份 | 2025 |
| 会议/期刊 | WWW |
| PDF | [[2025-WWW-ODNS_Clustering__Unveiling_Client-Side_Dependency_in_Open_DNS_Infrastructure.pdf]] |
| MinerU Markdown | [[2025-WWW-ODNS_Clustering__Unveiling_Client-Side_Dependency_in_Open_DNS_Infrastructure.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
There are over a million open DNS servers in the wild. However, not all servers perform recursive queries directly. Instead, many DNS forwarders forward queries to upstream recursive servers or other DNS forwarders for name resolving on their behalf. The groups of open servers that have such dependencies on each other form ODNS Clusters. The dependencies can result in vulnerabilities; yet we have little knowledge of the ODNS cluster structure. In this work, we measure the inter-dependence of open DNS resolvers and find that 1.9 million open DNS servers form only 81,636 ODNS clusters. We further analyze the characteristics of the clustered ODNS structure. The key observations include biased cluster size distribution, discrepancy of ODNS infrastructures among countries, concentration in major public DNS server providers, and potential security and resilience risks due to the dependence.

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
- 主题线索：dns, tor, covert。
- 摘要证据：There are over a million open DNS servers in the wild. However, not all servers perform recursive queries directly. Instead, many DNS forwarders forward queries to upstream recursive servers or other DNS forwarders for name resolving on their behalf. The groups of open servers that have such dependencies on each other form ODNS Clusters. The dependencies can result in vulnerabilities; yet we have little knowledge of the ODNS cluster structure. In this work, we measure the inter-dependence of open DNS resolvers and find that 1.9 million open DNS servers form only 81,636 ODNS clusters. We further analyze the characteristics of the clustered ODNS structure. The key observations include biased cluster size distribution, discrepancy of ODNS infrastructures among countries, concentration in major public DNS server providers, and potential security and resilience risks due to the dependence.

### 方法机制
Results analysis: With the cache-snooping results, we classify all servers into the following types based on their behavior: • Caching forwarders: Servers have not cached current record is a caching forwarder (�2), indicating that this server is not an upstream resolver. Instead, it is a forwarder and has independent cache processing itself. • Proxies & Resolver: Servers have cached current record is a upstream resolver (�4) or non-caching proxy (�3). This signifies that the cache record passed through such servers when the DNS query was initially performed. While non-caching proxies [10] simply follow the status of the upstream resolver, such proxies are classified into the same category with upstream resolver. • New-trigger: In addition, if our cache snooping triggers a new DNS response from ADNS, we mark such server as a new-trigger.

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。

## 深度分析（2026-09-29）

- reading_level: L3
- 研究定位：开放DNS测量/依赖图
- 方法机制：将开放DNS递归器、转发器及其上游依赖构成ODNS clusters；测量显示约190万开放DNS服务器归属于81,636个集群，并分析规模分布、国家差异、公共DNS集中度与安全韧性风险。
- 输入—处理—输出：大规模DNS探测与依赖关系聚类；输出集群结构和风险画像。
- 证据边界：摘要给出服务器与集群规模；探测周期、去重规则、可复现实验细节、代码和置信区间需回看正文。
- 联动标签：website-fingerprinting；DNS；anomaly-detection；traffic-security


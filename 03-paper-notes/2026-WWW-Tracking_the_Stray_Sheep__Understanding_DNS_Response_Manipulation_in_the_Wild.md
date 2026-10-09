---
type: paper
title_original: "Tracking the Stray Sheep: Understanding DNS Response Manipulation in the Wild"
title_cn: ""
authors: []
year: 2026
venue: WWW
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-WWW-Tracking_the_Stray_Sheep__Understanding_DNS_Response_Manipulation_in_the_Wild.pdf"
mineru_md: "02-parsed-markdown/2026-WWW-Tracking_the_Stray_Sheep__Understanding_DNS_Response_Manipulation_in_the_Wild.md"
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

# Tracking the Stray Sheep: Understanding DNS Response Manipulation in the Wild

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Tracking the Stray Sheep: Understanding DNS Response Manipulation in the Wild |
| 年份 | 2026 |
| 会议/期刊 | WWW |
| PDF | [[2026-WWW-Tracking_the_Stray_Sheep__Understanding_DNS_Response_Manipulation_in_the_Wild.pdf]] |
| MinerU Markdown | [[2026-WWW-Tracking_the_Stray_Sheep__Understanding_DNS_Response_Manipulation_in_the_Wild.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
The Domain Name System (DNS) plays a crucial role in modern web applications; however, manipulations such as hijacking, tampering, and censorship can disrupt domain resolution, posing significant privacy and security risks. While such manipulations are prevalent across global DNS infrastructures, their scope and mechanisms remain poorly understood. Existing studies focus on country-level censorship or rely on authoritative data and passive trafic from selected domains, which prevents a comprehensive understanding. Moreover, the dynamic nature of modern DNS resolution, in which a single domain may resolve to thousands of edge servers, further complicates the detection of manipulated responses. In this work, we propose a novel approach for measuring DNS manipulations based on resolution path analysis. Our method leverages CNAME chains and attributes of intermediate nodes in the DNS resolution process to link dynamic resolution results, enabling accurate detection of manipulation in highly dynamic DNS environments. We conduct large-scale measurements for 2,283 popular domains across global open DNS infrastructures. Measurement re sults reveal critical insights into DNS manipulation, uncovering the strategies and preferences of malicious manipulation operators and demonstrating how specific domains are exploited. <sup>∗</sup>Corresponding author: Zhenyu Li. CCS Concepts • Networks → Network measurement.

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
- 主题线索：anomaly, dns, tor, covert。
- 摘要证据：The Domain Name System (DNS) plays a crucial role in modern web applications; however, manipulations such as hijacking, tampering, and censorship can disrupt domain resolution, posing significant privacy and security risks. While such manipulations are prevalent across global DNS infrastructures, their scope and mechanisms remain poorly understood. Existing studies focus on country-level censorship or rely on authoritative data and passive trafic from selected domains, which prevents a comprehensive understanding. Moreover, the dynamic nature of modern DNS resolution, in which a single domain may resolve to thousands of edge servers, further complicates the detection of manipulated responses. In this work, we propose a novel approach for measuring DNS manipulations based on resolution path analysis. Our method leverages CNAME chains and attributes of intermediate nodes in the DNS resolution process to link dynamic resolution results, enabling accurate detection of manipulation in highly dynamic DNS environments. We conduct large-scale measurements for 2,283 popular domains across global open DNS infrastructures. Measurement re sults reveal critical insights into DNS manipulation, uncovering the strategies and preferences of malicious manipulation operators and demonstrating how specific domains are exploited. <sup>∗</sup>Corresponding author: Zhenyu Li. CCS Concepts • Networks → Network measurement.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：未检测到明确 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。

## 深度分析（2026-09-29）

- reading_level: L3
- 研究定位：DNS响应操纵/路径分析
- 方法机制：通过CNAME链与中间节点属性建立解析路径关联，在全球开放DNS基础设施对2,283个热门域名进行大规模测量，以识别劫持、篡改和审查响应。
- 输入—处理—输出：输入多点DNS解析结果与CNAME/中间节点特征；输出操纵事件及其路径证据。
- 证据边界：需核验操纵标签、探测点覆盖、误报验证、国家级差异和伦理边界。
- 联动标签：website-fingerprinting；DNS；anomaly-detection；traffic-security


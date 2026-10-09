---
type: paper
title_original: "Unveiling the Underground Phishing Ecosystem: A 12-Year Longitudinal Study of Deep and Dark Web Forums"
title_cn: ""
authors: []
year: 2026
venue: WWW
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-WWW-Unveiling_the_Underground_Phishing_Ecosystem__A_12-Year_Longitudinal_Study_of_Deep_and_Dark_Web_Forums.pdf"
mineru_md: "02-parsed-markdown/2026-WWW-Unveiling_the_Underground_Phishing_Ecosystem__A_12-Year_Longitudinal_Study_of_Deep_and_Dark_Web_Forums.md"
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

# Unveiling the Underground Phishing Ecosystem: A 12-Year Longitudinal Study of Deep and Dark Web Forums

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Unveiling the Underground Phishing Ecosystem: A 12-Year Longitudinal Study of Deep and Dark Web Forums |
| 年份 | 2026 |
| 会议/期刊 | WWW |
| PDF | [[2026-WWW-Unveiling_the_Underground_Phishing_Ecosystem__A_12-Year_Longitudinal_Study_of_Deep_and_Dark_Web_Forums.pdf]] |
| MinerU Markdown | [[2026-WWW-Unveiling_the_Underground_Phishing_Ecosystem__A_12-Year_Longitudinal_Study_of_Deep_and_Dark_Web_Forums.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
Phishing is a threat in which attackers masquerade as legitimate entities to steal sensitive data. While understanding the phishing ecosystem is critical for developing efective countermeasures, prior research has largely studied phishing through post-attack data, with limited examination of the attacker’s perspective and how phishing campaigns are built. Critically, the Deep and Dark Web (D2Web) serves as the primary marketplace and knowledge-sharing platform where attackers acquire phishing tools (e.g., phishing kits), exchange techniques, and trade compromised credentials. Analyz ing D2Web forums therefore provides unique visibility into the supply chain of phishing attacks pre-deployment, enabling proac tive understanding of emerging threats and attack methodologies. This study addresses this gap through a comprehensive analysis of 394,034 posts (343,334 unique) collected from 13 D2Web forums spanning 2013 to 2025, from which 70,055 phishing-related posts are identified. We employ a LLM-based approach to eficiently ex tract key information, including phishing attack components (e.g., credentials, phishing pages, SMTP servers), targeted services (e.g., PayPal, Netflix), and component authors. This extracted data is mapped to a seven-stage attack scenario framework derived from empirical case studies. Our analysis reveals longitudinal trends in component availability, target service distribution, post type evolution, and the most active contributors annually, while characterizing pricing dynamics across diferent attack components. The results provide the first attacker-centric, macro-level longitudi nal analysis of the phishing ecosystem, ofering insights into how phishing infrastructure and markets have evolved over more than a decade. These findings contribute to a deeper understanding of the phishing supply chain and inform more efective detection and prevention strategies.

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
- 主题线索：tor, covert。
- 摘要证据：Phishing is a threat in which attackers masquerade as legitimate entities to steal sensitive data. While understanding the phishing ecosystem is critical for developing efective countermeasures, prior research has largely studied phishing through post-attack data, with limited examination of the attacker’s perspective and how phishing campaigns are built. Critically, the Deep and Dark Web (D2Web) serves as the primary marketplace and knowledge-sharing platform where attackers acquire phishing tools (e.g., phishing kits), exchange techniques, and trade compromised credentials. Analyz ing D2Web forums therefore provides unique visibility into the supply chain of phishing attacks pre-deployment, enabling proac tive understanding of emerging threats and attack methodologies. This study addresses this gap through a comprehensive analysis of 394,034 posts (343,334 unique) collected from 13 D2Web forums spanning 2013 to 2025, from which 70,055 phishing-related posts are identified. We employ a LLM-based approach to eficiently ex tract key information, including phishing attack components (e.g., credentials, phishing pages, SMTP servers), targeted services (e.g., PayPal, Netflix), and component authors. This extracted data is mapped to a seven-stage attack scenario framework derived from empirical case studies. Our analysis reveals longitudinal trends in component availability, target service distribution, post type evolution, and the most active contributors annually, while characterizing pricing dynamics across diferent attack components. The results provide the first attacker-centric, macro-level longitudi nal analysis of the phishing ecosystem, ofering insights into how phishing infrastructure and markets have evolved over more than a decade. These findings contribute to a 

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
- 研究定位：钓鱼生态/地下论坛测量
- 方法机制：对13个深暗网论坛2013–2025年394,034条帖子（343,334条去重）进行分析，LLM抽取钓鱼组件、目标服务和供应链关系，识别70,055条钓鱼相关帖子。
- 输入—处理—输出：输入论坛帖子；LLM信息抽取后构建组件、目标和时序生态分析。
- 证据边界：摘要给出数据规模；论坛可见性偏差、LLM标注准确率、伦理与可复现性需正文核验。
- 联动标签：website-fingerprinting；DNS；anomaly-detection；traffic-security


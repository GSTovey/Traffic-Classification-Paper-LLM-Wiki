---
type: paper
title_original: "THE ADVANCED COMPUTING SYSTEMS ASSOCIATION"
title_cn: ""
authors: []
year: 2026
venue: USENIX
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-USENIX-DNS_Cache_Poisoning_Like_it’s_2006.pdf"
mineru_md: "02-parsed-markdown/2026-USENIX-DNS_Cache_Poisoning_Like_it’s_2006.md"
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
| PDF | [[2026-USENIX-DNS_Cache_Poisoning_Like_it’s_2006.pdf]] |
| MinerU Markdown | [[2026-USENIX-DNS_Cache_Poisoning_Like_it’s_2006.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
The Domain Name System (DNS) underpins virtually all Internet services, making the integrity of DNS resolution crit ical to security and availability. We present a comprehensive study of a novel class of DNS cache poisoning attacks against BIND 9, the most widely deployed open-source DNS resolver. Our attack focuses on two key capabilities that set it apart from most prior work: (1) reliably predicting both critical challenge parameters – the UDP source port and TXID – whereas most existing attacks target only one; and (2) performing this pre diction entirely from the client side, without attacker-operated authoritative servers for attacker domains, which to our knowl edge is a first. We achieve this by exploiting weaknesses in BIND’s pseudo-random number generation, enabling highly reliable prediction even under realistic network conditions. In addition to the client-side-only techniques, we also develop server-side techniques which are needed in order to attack the older 9.18 branch of BIND 9. We evaluate our attacks and demonstrate practical success rates across multiple BIND 9 release branches and configurations. All vulnerabilities were responsibly disclosed to the Internet Systems Consortium (ISC) and the FreeBSD Project, leading to two patches and CVEs and acknowledgments.

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
- 主题线索：anomaly, dns, tor, adversarial, quic。
- 摘要证据：The Domain Name System (DNS) underpins virtually all Internet services, making the integrity of DNS resolution crit ical to security and availability. We present a comprehensive study of a novel class of DNS cache poisoning attacks against BIND 9, the most widely deployed open-source DNS resolver. Our attack focuses on two key capabilities that set it apart from most prior work: (1) reliably predicting both critical challenge parameters – the UDP source port and TXID – whereas most existing attacks target only one; and (2) performing this pre diction entirely from the client side, without attacker-operated authoritative servers for attacker domains, which to our knowl edge is a first. We achieve this by exploiting weaknesses in BIND’s pseudo-random number generation, enabling highly reliable prediction even under realistic network conditions. In addition to the client-side-only techniques, we also develop server-side techniques which are needed in order to attack the older 9.18 branch of BIND 9. We evaluate our attacks and demonstrate practical success rates across multiple BIND 9 release branches and configurations. All vulnerabilities were responsibly disclosed to the Internet Systems Consortium (ISC) and the FreeBSD Project, leading to two patches and CVEs and acknowledgments.

### 方法机制
Results. In our tests, the RRset variant succeeded in predicting the PRNG state in 10/10 of experiments and achieved a successful poisoning rate of 10/10 when using the third-party ANS and DRINK servers.

### 实验与结果
![](images/9d89a761aaaf379ac6b15b62ce156274c2ecdc70899cb5d19eb8e5aec3171964.jpg) Figure 3: Attack success rate vs. resolver load. Success Rate vs Load. Fig. 3 shows the cache poisoning success rate as a function of query load, ranging from 1 to 10,000 QPS. While most variants remained effective at moderate loads, several configurations exhibited performance degradation under high load. In particular, the RR-QMA variant against BIND 9.18.37 completely failed at 10,000 QPS. RR-QMA also showed reduced reliability on BIND 9.21.9 and 9.20.10 under load. In contrast, RRset-ANY maintained a success rate above 94% even at the highest tested load. Offset CDF. In our load experiments, we also measured the PRNG offset (i.e., PRNG steps) between the PRNG state right after it is observed by the attacker (obtained from the re-sync query, immediately before the poisoning query), and the PRNG state used to generate the UDP source port and TXID for the poisoning query. For each offset, the attacker needs to send a spoofed answer with source port and TXID corresponding to the PRNG state at the prescribed offset. Since the attacker’s goal is to cover as much probability space (in terms of offsets) as possible in the attack window, it follows that the ideal situation for the attacker is to have very few (ideally one) offsets that cover almost 100% of the probability space. Fig. 4 shows the cumulative distribution of this offset for various attack variants and query loads. ![](images/30a0e5ec07d46ec9b9c78fe45c439d42d2fa47703f781828d64315975f0984be.jpg) Figure 4: CDF of PRNG offset values per attack variant and load. Most attacks succeed with low offsets, even under heavy load. RR-QMA 9.18 @10K is not plotted since the attack fails 100% of the time. Note that RR-QMA 9.20 @1 graphically coinc

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。

## 深度分析（2026-09-29）

- reading_level: L3
- 研究定位：DNS缓存投毒/PRNG安全
- 方法机制：针对BIND 9利用Xoshiro128**状态恢复，同时预测UDP源端口与TXID；客户端侧变体无需攻击者自有权威服务器，另有针对9.18的服务端方法。
- 输入—处理—输出：输入可观测DNS响应或查询序列；恢复PRNG状态并构造少量伪造响应完成投毒。
- 证据边界：摘要称在多版本和现实网络条件下成功，并导致2个补丁/CVE；生产配置泛化、DNSSEC覆盖和完整成功率需核验。
- 联动标签：website-fingerprinting；DNS；anomaly-detection；traffic-security


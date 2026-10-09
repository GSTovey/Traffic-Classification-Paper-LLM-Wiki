---
type: paper
title_original: "Eclipse Atacks on Ethereum’s Peer-to-Peer Network"
title_cn: ""
authors: []
year: 2026
venue: WWW
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-WWW-Eclipse_Attacks_on_Ethereum’s_Peer-to-Peer_Network.pdf"
mineru_md: "02-parsed-markdown/2026-WWW-Eclipse_Attacks_on_Ethereum’s_Peer-to-Peer_Network.md"
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

# Eclipse Atacks on Ethereum’s Peer-to-Peer Network

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Eclipse Atacks on Ethereum’s Peer-to-Peer Network |
| 年份 | 2026 |
| 会议/期刊 | WWW |
| PDF | [[2026-WWW-Eclipse_Attacks_on_Ethereum’s_Peer-to-Peer_Network.pdf]] |
| MinerU Markdown | [[2026-WWW-Eclipse_Attacks_on_Ethereum’s_Peer-to-Peer_Network.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
Eclipse attacks isolate blockchain nodes by monopolizing their peer-to-peer connections. The attacks were extensively studied in Bitcoin (SP’15, SP’20, CCS’21, SP’23) and Monero (NDSS’25), but their practicality against Ethereum nodes remains underexplored, particularly in the post-Merge settings. We present the first end-to-end implementation of an eclipse attack targeting Ethereum (2.0 version) execution-layer nodes. Our attack exploits the bootstrapping and peer management logic of Ethereum to fully isolate a node upon restart. We introduce a multi stage strategy that majorly includes (i) poisoning the node’s discovery table via unsolicited messages, (ii) infiltrating Ethereum’s DNS-based peerlist by identifying and manipulating the oficial DNS crawler, and (iii) hijacking idle incoming connection slots across the network to block benign connections. Our DNS list poi soning is the first in the cryptocurrency context and requires only 28 IP addresses over 100 days. Slots hijacking raises outgoing redi rection success from 45% to 95%. We validate our approach through controlled experiments on Ethereum’s Sepolia testnet and broad measurements on the mainnet. Our findings demonstrate that over 80% of public nodes do not leave suficient idle capacity for effective slots occupation, highlighting the feasibility and severity of the threat. We further propose concrete countermeasures and responsibly disclosed all findings to Ethereum’s security team.

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
- 主题线索：dns, tor, adversarial。
- 摘要证据：Eclipse attacks isolate blockchain nodes by monopolizing their peer-to-peer connections. The attacks were extensively studied in Bitcoin (SP’15, SP’20, CCS’21, SP’23) and Monero (NDSS’25), but their practicality against Ethereum nodes remains underexplored, particularly in the post-Merge settings. We present the first end-to-end implementation of an eclipse attack targeting Ethereum (2.0 version) execution-layer nodes. Our attack exploits the bootstrapping and peer management logic of Ethereum to fully isolate a node upon restart. We introduce a multi stage strategy that majorly includes (i) poisoning the node’s discovery table via unsolicited messages, (ii) infiltrating Ethereum’s DNS-based peerlist by identifying and manipulating the oficial DNS crawler, and (iii) hijacking idle incoming connection slots across the network to block benign connections. Our DNS list poi soning is the first in the cryptocurrency context and requires only 28 IP addresses over 100 days. Slots hijacking raises outgoing redi rection success from 45% to 95%. We validate our approach through controlled experiments on Ethereum’s Sepolia testnet and broad measurements on the mainnet. Our findings demonstrate that over 80% of public nodes do not leave suficient idle capacity for effective slots occupation, highlighting the feasibility and severity of the threat. We further propose concrete countermeasures and responsibly disclosed all findings to Ethereum’s security team.

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
- 研究定位：Ethereum P2P/eclipse攻击
- 方法机制：首次端到端实现Ethereum执行层重启后隔离：通过未请求消息污染发现表、操纵官方DNS crawler peerlist、劫持空闲入站槽位；28个IP持续100天即可DNS列表投毒，槽位劫持将出站重定向成功率从45%升至95%。
- 输入—处理—输出：输入节点发现/连接状态与DNS peerlist；输出隔离节点及重定向攻击。
- 证据边界：摘要明确测试网与主网测量；部署版本、检测/缓解评估、长期可行性和伦理限制待核验。
- 联动标签：website-fingerprinting；DNS；anomaly-detection；traffic-security


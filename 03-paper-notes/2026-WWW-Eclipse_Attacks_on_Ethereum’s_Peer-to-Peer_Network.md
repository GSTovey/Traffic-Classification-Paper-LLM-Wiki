---
type: paper
title_original: "Eclipse Attacks on Ethereum’s Peer-to-Peer Network"
title_cn: "以太坊点对点网络的日蚀攻击"
authors: ["Ruisheng Shi", "Qin Wang", "Yuxuan Liang", "Lina Lan", "Zhuoyi Zheng", "Zijun Guo", "Chenfeng Wang"]
year: 2026
venue: "ACM Web Conference 2026 (WWW'26)"
doi: unknown
url: "https://doi.org/10.1145/3774904.3792231"
pdf: "00-inbox/PDFs/2026-WWW-Eclipse_Attacks_on_Ethereum’s_Peer-to-Peer_Network.pdf"
mineru_md: "02-parsed-markdown/2026-WWW-Eclipse_Attacks_on_Ethereum’s_Peer-to-Peer_Network.md"
status: deep-analyzed
reading_level: L3
research_area: ["Ethereum P2P security", "blockchain network measurement", "eclipse attacks"]
task: ["peer discovery analysis", "connection hijacking", "network-wide attack feasibility"]
method: ["Geth source analysis", "Sepolia controlled experiment", "mainnet active measurement", "DNS peerlist poisoning"]
dataset: ["Geth v1.14.3", "Sepolia testnet", "Ethereum mainnet public nodes", "2,000+ node slot scan"]
code: "unknown (attack details and pseudocode in paper Appendix F)"
relevance: medium
created: "2026-09-29"
updated: "2026-10-10"
---

# Eclipse Attacks on Ethereum’s Peer-to-Peer Network

> **L3 深度分析笔记**：基于正文 §1–§7、Tables 1–7、Appendix B–F、Ethics Considerations 与 responsible disclosure 内容交叉核对。该论文在 Sepolia 和受控自有节点上验证攻击链，并对主网做公开节点测量；不能把受控实验等同于对第三方节点的未授权攻击。

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Eclipse Attacks on Ethereum’s Peer-to-Peer Network |
| 中文标题 | 以太坊点对点网络的日蚀攻击 |
| 作者 | Ruisheng Shi、Qin Wang、Yuxuan Liang、Lina Lan、Zhuoyi Zheng、Zijun Guo、Chenfeng Wang |
| 年份 | 2026 |
| 会议/期刊 | ACM Web Conference 2026 (WWW'26) |
| 研究方向 | Ethereum execution-layer P2P 安全、peer discovery、eclipse attack |
| 任务类型 | 发现表/DNS peerlist 投毒、入/出站连接劫持、公开节点槽位测量 |
| 方法关键词 | Geth v1.14.3 源码分析、Discv4、17 K-bucket、devp2p crawler、Sepolia 控制实验、mainnet 公开测量 |
| 数据与范围 | Sepolia testnet、Ethereum mainnet 公共节点、2,000+ 节点空闲槽位扫描、Geth 版本更新历史 |
| 是否开源 | unknown；论文含 Appendix F 伪代码，未给代码仓库 |
| DOI | 10.1145/3774904.3792231 |
| PDF | 00-inbox/PDFs/2026-WWW-Eclipse_Attacks_on_Ethereum’s_Peer-to-Peer_Network.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-WWW-Eclipse_Attacks_on_Ethereum’s_Peer-to-Peer_Network.md |

## 1. 一句话总结
> 论文针对 Merge 后 Ethereum 执行层节点，组合发现表 DB 预填、官方 DNS peerlist 投毒、全网空闲入站槽位占用及目标重启后的入/出站连接劫持；Sepolia 实验中 50% DNS+DB 投毒配合槽位占用将出站劫持成功率提升至 95%，主网 40 次试验中 60% 在两天内完全占满入站连接。

## 2. 摘要原文
Eclipse attacks isolate blockchain nodes by monopolizing their peer-to-peer connections. The attacks were extensively studied in Bitcoin (SP’15, SP’20, CCS’21, SP’23) and Monero (NDSS’25), but their practicality against Ethereum nodes remains underexplored, particularly in the post-Merge settings. We present the first end-to-end implementation of an eclipse attack targeting Ethereum (2.0 version) execution-layer nodes. Our attack exploits the bootstrapping and peer management logic of Ethereum to fully isolate a node upon restart. We introduce a multi stage strategy that majorly includes (i) poisoning the node’s discovery table via unsolicited messages, (ii) infiltrating Ethereum’s DNS-based peerlist by identifying and manipulating the oficial DNS crawler, and (iii) hijacking idle incoming connection slots across the network to block benign connections. Our DNS list poi soning is the first in the cryptocurrency context and requires only 28 IP addresses over 100 days. Slots hijacking raises outgoing redi rection success from 45% to 95%. We validate our approach through controlled experiments on Ethereum’s Sepolia testnet and broad measurements on the mainnet. Our findings demonstrate that over 80% of public nodes do not leave suficient idle capacity for effective slots occupation, highlighting the feasibility and severity of the threat. We further propose concrete countermeasures and responsibly disclosed all findings to Ethereum’s security team.

## 3. 方法分析

### 3.1 系统前提

论文以 Geth v1.14.3 为主要分析对象。节点默认最多 16 个 outgoing、34 个 incoming 连接；发现表有 17 个 K-bucket、每桶最多 16 个节点，总容量 272。节点重启时从持久 DB 随机加载 30 个节点和 4 个 bootnodes，之后通过 Discv4 lookup 刷新；DNS peerlist 由 devp2p crawler 维护，每 5 小时 40 分钟运行一次，主网/测试网分别取 top 3000/250 节点。

### 3.2 五阶段攻击管线

| 阶段 | 操作 | 预期效果 |
|---|---|---|
| 1 DB pre-filling | 未请求 Ping 让攻击 ENR 进入 discovery table；保持 >5 分钟且通过 liveness 后写入 DB；多轮替换 | 重启时恶意节点成为早期 seed |
| 2 DNS list poisoning | 低 node ID、持续在线、监视 crawler、FindNode 返回自有 ENR、累积 score | 恶意 ENR 进入官方 top-N peerlist |
| 3 网络槽位占用 | 用攻击节点预占公共节点的空闲 incoming slots | 目标重启后无法连接诚实节点 |
| 4 出站劫持 | 重启后 swarm Ping 填表，利用 DNS/DB 偏置提高恶意 peer 选择 | 控制目标 outgoing 连接 |
| 5 入站劫持 | 重启同时大量连接目标，抢先占满 34 个 incoming slots | 完成执行层节点 eclipse |

### 3.3 核心假设与边界

攻击依赖三点：重启清空短期 discovery table 但保留 DB；DNS peerlist 是独立 bootstrap 来源；Ethereum 缺少主动连接驱逐，且 incoming 槽位固定。攻击不需要共识层控制或解密交易，只需让网络层 peer 选择被偏置。

## 4. 实验表现

### 4.1 关键设置与结果

| 实验 | 设置 | 结果 |
|---|---|---|
| Geth/P2P 分析 | Geth v1.14.3 源码和运行行为 | 17 bucket、272 table slots、16 outgoing/34 incoming |
| DB poisoning | Sepolia 自建节点，272 攻击节点，多轮 Ping/替换 | 首轮 24h 达约 95%；后续批次约 1h 重填近 100% |
| DNS poisoning | 受控 testbed；score 机制 | 10 次中 5 次有攻击节点进入表，1 次五节点均达 3 分；估算 25/50/75/100% 列表替换需 64/100/166/538 天 |
| 空闲槽位扫描 | >2,000 公共节点；Sepolia 1,268 DNS 节点 | >80% 节点空闲槽位≤10；Sepolia 321 个有空闲槽位；200 攻击节点两小时占用约 90% |
| 出站劫持 | 20 次/条件，DNS poison 0/25/50/75/100%，DB 50% | 50% DNS+DB：占槽位前 40%（8/20），占槽位后 95%（19/20） |
| 入站劫持 | Sepolia 30 次；mainnet 40 次 | Sepolia 30/30（100%，30s 内）；mainnet 24/40（60%，2 天内），18/40（45%）30s 内 |

论文不是机器学习 benchmark；对照是“有/无 DB poisoning”“槽位占用前/后”和不同 DNS filling rate。

## 5. 局限性与复现建议
- 攻击步骤 1–5 的实测主要在 Sepolia 和自建/受控节点上；mainnet 部分是公开节点槽位扫描与 40 次入站占用试验，不等于对所有主网节点可稳定完成完整 eclipse。
- DNS poisoning 的官方 crawler 未被直接攻击，论文用受控 testbed 估计 score 和完成时间；“28 IP/100 天”是作者场景和理想 score 假设下的资源估计。
- Geth v1.14.3 与 2025 年网络状态限定结论；客户端更新、DNS crawler 策略、IP admission 和连接驱逐改动可能改变可行性。
- Ethics 章节明确所有攻击步骤只在自有目标节点/受控环境进行，未对主网第三方节点实施未经授权的 DoS；复现只能在自有节点和测试网进行。
- 论文未提供完整公开代码仓库；Appendix F 伪代码足以理解流程，但不能替代依赖版本、节点配置和网络环境。

## 6. 知识链接
- 暂无与现有流量分析白名单直接对应的概念页；DNS/区块链 P2P 主题不新建空页。

## 7. 证据状态
- 正文证据已核对至 §1–§7、Tables 1–7、Appendix B–F、Ethics Considerations。
- DOI 为 10.1145/3774904.3792231；未找到作者公开攻击代码仓库，记为 unknown。
- 攻击性数值均保留 Sepolia、mainnet public-node measurement 或估计口径，不将其泛化为当前全网永久风险。



## 8. 详细方法与机制

### 8.1 Peerlist 和连接机制

Geth 把发现节点分为持久 DB 与重启即清空的 discovery table；后者 17 个 K-bucket、总容量 272，bucketIPLimit/tableIPLimit 限制同一 /24 的节点数。启动时先加载 DB/bootnodes，再通过 self/random lookup 填充；运行中既有 doRefresh 主动 lookup，也接受未请求 Ping 的被动插入。连接层上限为 16 outgoing 和 34 incoming。devp2p crawler 每 5 小时 40 分钟抓取节点，按 ENRResponse 成功加分、失败减半，聚合后选主网 3000、测试网 250 个 DNS peer。

### 8.2 DB pre-filling

攻击者从多个 ENR/IP 发送未请求 Ping，使节点把攻击记录放入 discovery table；记录持续在线、超过 5 分钟并通过 liveness 后被写入 DB。攻击者关闭第一批节点并启动下一批，重复多轮，让 DB 和高索引 bucket 中的恶意记录逐步替换诚实记录。目标第二次重启时，从 DB 加载的 30 个随机 seed 被恶意记录占据，再配合 272 节点 Ping/Neighbors 响应强化 table poisoning。

### 8.3 DNS list poisoning

攻击者通过低 node ID、持续在线和回应 crawler 的 ENRRequest/FindNode 提高 score；论文定位了官方 crawler，但为伦理原因仅在自建 testbed 模拟。score 机制给攻击者每次 crawl 更高增长，估计在理想稳定响应下需要 64–538 天将测试网 DNS 列替换 25–100%。

### 8.4 槽位占用与重启窗口

全网槽位占用利用多数公开节点空闲 incoming slots 很少这一事实。预先连接 200 个攻击节点到有空闲槽位的节点，使目标重启后对诚实 peer 的 outgoing dial 失败或超时，只能从被污染的 DB/DNS 集合选择恶意节点；同时用约 34/40 个不同 IP 抢占目标 incoming slots，完成双向连接控制。Geth 高频更新（Merge 后 32 个月 56 个版本，约每月 1.75 次）意味着重启窗口会重复出现。

## 9. 学习与应用

### 9.1 复现关键步骤

1. 仅在自有 Geth v1.14.3/本地 Sepolia 节点上构建 DB、DNS crawler 和连接槽位 testbed。
2. 记录 discovery table 17 bucket、DB 写入等待、/24 限制、16/34 连接上限和重启时间。
3. 复现单阶段 DB filling、受控 DNS score、available-slot measurement，再组合 outgoing/incoming hijack；每阶段先测成功率，不能直接执行完整公共网络攻击。
4. 固定 10 次 DB/出站实验、30 次 Sepolia/40 次 mainnet 论文口径，保存节点版本、IP 数、restart interval 和连接日志。
5. 对照论文 countermeasures 测试：限制同 IP DNS 节点、禁用 unsolicited insertion、启动期保留可信 peer、主动 eviction 和动态连接上限。

### 9.2 能否迁移到其他任务？

方法可迁移到依赖长期 peerlist、DNS bootstrap 和固定连接槽位的 P2P 系统，但攻击阶段必须按协议的发现表持久性、重启初始化和入/出站配额重新建模。其测量方法也可用于评估 Web3/P2P 网络的 peer diversity 与连接集中度；不能直接把以太坊的 IP 数和时间成本移植到 Bitcoin、Monero 或其他客户端。

### 9.3 与本库主题的关系

该论文不是加密流量分类任务；可迁移的只有测量层方法：把协议状态、连接来源和 bootstrap 依赖拆成可观测状态图，再用受控重启/连接事件验证风险。不要将其加入 website fingerprint 或 traffic-classification 方法对比表。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| Geth v1.14.3 的 DB/discovery table、17 K-bucket、272 容量 | P2P architecture analysis | §2.2 |
| 节点连接上限 16 outgoing/34 incoming | connection management | §2.3 |
| devp2p crawler 5h40m、score 和 top-N DNS list | DNS peerlist management | §2.4 |
| 五阶段 eclipse workflow | DB、DNS、slots、outgoing、incoming | §3.1 |
| DB 首轮 24h 约 95% filling，多轮约 1h 重填 | Table 1/Fig. 2 | §4.1 |
| DNS list poisoning 估计 25/50/75/100% 需 64/100/166/538 天 | Table 3 | §4.2 |
| >2,000 公共节点中 >80% 空闲槽位≤10；Sepolia 200 攻击节点占约 90% | slot scan | §4.3, Appendix E |
| 50% DNS+DB 后 outgoing hijack 8/20→19/20 | Table 4 | §4.4 |
| Sepolia incoming 30/30、mainnet 24/40 两天内成功 | Table 5 | §4.5 |
| Merge 后 56 个 Geth 版本、约 1.75/月重启窗口 | version discussion | §5.1 |
| 受控实验、无第三方 DoS、向 Ethereum security team 披露 | Ethics/disclosure | §Ethics Considerations |

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-WWW-Eclipse_Attacks_on_Ethereum’s_Peer-to-Peer_Network.pdf
- MinerU Markdown：02-parsed-markdown/2026-WWW-Eclipse_Attacks_on_Ethereum’s_Peer-to-Peer_Network.md
- DOI：https://doi.org/10.1145/3774904.3792231

## 12. 后续问题

1. Geth、Besu、Nethermind 等不同执行客户端的 DB/Discv4/DNS 逻辑差异是否会改变五阶段攻击链？
2. DNS crawler score、IP /24 限制和入站 slot 保护的补丁能否在不降低 peer diversity 的情况下阻断攻击？
3. 主网节点的真实重启与客户端升级节奏如何影响长期成功率，是否存在季节性或地域性差异？
4. 该攻击对 consensus-layer peers、validator liveness 和交易传播的实际影响需要隔离评估；本文主要证明网络层 eclipse 可行性。
5. 公开节点槽位扫描和受控攻击的边界如何标准化，才能在其他 P2P 网络开展可比的伦理测量？

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

论文从 Merge 后 Ethereum 的新运行条件切入：validator 长在线、静态 bootstrap、DNS discovery 和 execution client 的交易传播，使旧式 eclipse 风险重新出现。作者先拆解 Geth 的 DB、discovery table、DNS crawler 和连接上限，再把这些看似分散的弱点串成五阶段攻击链。实验顺序与攻击顺序一致：先证明 DB 能填、DNS 能污染、全网槽位确实稀缺，再证明这些条件叠加后出站成功率从 40% 升至 95%，最后以重启后的入站占满完成闭环。讨论用版本更新频率和 IP 资源估计说明攻击不是一次性 PoC，而是重复重启窗口下的系统性风险；伦理章节将证明范围限定在自有/受控节点。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 角色 | 关键转折 |
|---|---|---|---|
| Introduction | 将 Merge 后网络假设与旧 eclipse 文献连接 | 问题重启 | post-Merge 行为改变攻击面 |
| P2P dissection | 解释 DB、bucket、DNS crawler、connection cap | 系统锚定 | 多个独立 bootstrap/连接机制同时存在 |
| Attack design | 五阶段 workflow | 方法主体 | 重启成为攻击同步点 |
| Evaluation | 按步骤测 filling/poisoning/slots/hijack | 证据递进 | 50% DNS+DB+slots 组合达到 95% |
| Discussion/Countermeasures | 版本频率、IP 成本和防护建议 | 风险落地 | 重启窗口让攻击可重复 |
| Ethics/Conclusion | 限定受控实验和责任披露 | 外推边界 | 不把受控节点结果写成全网已被攻破 |

### 13.3 Gap 展开方式

| Gap | 具体内容 | 论证方式 |
|---|---|---|
| 时间缺口 | 现有 Ethereum eclipse 工作多早于 Merge | 以 Geth v1.14.3 post-Merge 重新测量 |
| bootstrap 缺口 | DB/discovery 与 DNS 是两个独立来源 | 先分别投毒再组合 |
| 连接缺口 | 仅控制 target 不足以阻断诚实 outgoing peers | network-wide available slot occupation |
| 可行性缺口 | 旧工作只给攻击概念/单阶段 | Sepolia + mainnet 公开测量和资源估计 |

### 13.4 实验叙事方式

| 环节 | 作用 |
|---|---|
| DB growth/filling | 证明持久记录可以积累 |
| DNS score/time | 量化外部 crawler 投毒成本 |
| Available slots | 证明全网诚实连接确有可占用余量 |
| Outgoing hijack | 连接 DB/DNS 和 slot occupation |
| Incoming hijack | 完成重启后双向连接闭合 |
| Version/IP discussion | 把一次实验转为长期风险评估 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移写法 |
|---|---|---|
| 系统分析 | 先画出状态持久性、bucket 和连接上限 | 先把协议状态机拆成可测变量 |
| 攻击叙述 | 每个阶段给出资源、时间、成功率 | 攻击论文按 prerequisite→trigger→impact 顺序写 |
| 现实验证 | 测试网做闭环，主网只做公开测量/部分占用 | 将“证明可行”和“测量现实性”分开 |
| 伦理边界 | 明确官方 crawler 不直接投毒、第三方节点不受影响 | 把实验权限和外推范围写进结果段落 |

## 14. 证据边界与复现清单

1. **版本边界**：结果针对 Geth v1.14.3 和 2025 年观测；客户端更新后 DB、DNS 和连接策略可能改变。
2. **实验边界**：完整五阶段闭环主要在 Sepolia/自有节点；mainnet 结果是公开节点槽位测量和受控入站占用，不等于未经授权的主网 eclipse。
3. **资源口径**：28 IP/100 天、304 IP 和 64–538 天 DNS list 完成时间分别对应不同攻击阶段/理想 score 假设，不能拼成一个无条件最低成本。
4. **指标边界**：slot availability、outgoing hijack success、incoming occupation success 衡量不同阶段；成功占满连接不自动等于能操纵区块共识或交易结果。
5. **复现伦理**：只在本地节点、私有网络或获授权测试网执行；不要向官方 crawler 或第三方节点发送投毒/DoS 流量。
6. **代码证据**：论文含 Appendix F 伪代码但未给公开攻击代码；复现需要自行实现和核对 Geth 版本，记为 unknown code 状态。

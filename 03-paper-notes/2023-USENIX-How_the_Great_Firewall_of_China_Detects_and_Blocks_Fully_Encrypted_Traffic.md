---
type: paper
title_original: "How the Great Firewall of China Detects and Blocks Fully Encrypted Traffic"
title_cn: "中国防火长城如何检测和阻断全加密流量"
authors: ["Mingshi Wu", "Jackson Sippe", "Danesh Sivakumar", "Jack Burg", "Peter Anderson", "Xiaokang Wang", "Kevin Bock", "Amir Houmansadr", "Dave Levin", "Eric Wustrow"]
year: 2023
venue: "USENIX Security 2023"
publication_status: published
doi: unknown
url: "https://www.usenix.org/conference/usenixsecurity23/presentation/wu-mingshi"
pdf: ""
mineru_md: "02-parsed-markdown/2023-USENIX-How_the_Great_Firewall_of_China_Detects_and_Blocks_Fully_Encrypted_Traffic.md"
status: deep-analyzed
reading_level: L3
research_area: ["censorship-circumvention", "encrypted-traffic-analysis", "tunnel-detection"]
task: ["tunnel-detection", "encrypted-traffic-detection", "censorship-evasion"]
method: ["heuristic-rules", "bit-popcount", "ascii-analysis", "protocol-fingerprinting", "probabilistic-blocking"]
dataset: ["CU-Boulder-Network-Tap", "Internet-Scan-10pct", "China-VPS-TencentCloud", "China-VPS-AlibabaCloud"]
code: "https://gfw.report/publications/usenixsecurity23/en"
my_confidence: high
relevance: high
related_papers: []
kb_read_only: true
promoted_to: ""
created: "2026-06-21"
updated: "2026-06-21"
---

# How the Great Firewall of China Detects and Blocks Fully Encrypted Traffic

> **L3 深度分析笔记** — 基于 MinerU 解析的全文进行深度方法论与实验分析。
> `kb_read_only: true`：本笔记可链接到主知识库页面，但不会触发主知识库的任何更新。

---

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | How the Great Firewall of China Detects and Blocks Fully Encrypted Traffic |
| 中文标题 | 中国防火长城如何检测和阻断全加密流量 |
| 作者 | Mingshi Wu (GFW Report), Jackson Sippe (CU Boulder), Danesh Sivakumar (UMD), Jack Burg (UMD), Peter Anderson (Independent), Xiaokang Wang (V2Ray), Kevin Bock (UMD), Amir Houmansadr (UMass Amherst), Dave Levin (UMD), Eric Wustrow (CU Boulder) |
| 年份 | 2023 |
| 会议/期刊 | USENIX Security 2023 (第32届USENIX安全研讨会) |
| 研究方向 | [[censorship-circumvention]], [[encrypted-traffic-analysis]], [[tunnel-detection]] |
| 任务类型 | 审查机制逆向分析、全加密流量检测规则推断、规避策略设计 |
| 方法关键词 | popcount熵检测、可打印ASCII豁免、协议指纹豁免、概率性阻断、残余审查 |
| 数据集 | CU Boulder 40Gbps网络Tap (17亿连接)、10% IPv4互联网扫描 (550万IP)、中国腾讯云/阿里云VPS |
| 是否开源 | 是 — https://gfw.report/publications/usenixsecurity23/en |
| PDF | — |
| MinerU Markdown | 02-parsed-markdown/2023-USENIX-How_the_Great_Firewall_of_China_Detects_and_Blocks_Fully_Encrypted_Traffic.md |

---

## 1. 一句话总结

> 本文通过大规模测量实验揭示了GFW在2021年11月部署的被动式全加密流量检测系统：GFW并非直接定义"全加密流量"，而是通过至少五组启发式豁免规则（popcount熵、可打印ASCII比例/位置/连续长度、TLS/HTTP协议指纹）排除非全加密流量，对未被豁免的流量以26.3%的概率进行阻断，仅覆盖26%的连接和特定数据中心IP段，误报率约0.6%。

---

## 2. 摘要翻译

### 2.1 摘要原文

One of the cornerstones in censorship circumvention is fully encrypted protocols, which encrypt every byte of the payload in an attempt to "look like nothing". In early November 2021, the Great Firewall of China (GFW) deployed a new censorship technique that passively detects—and subsequently blocks—fully encrypted traffic in real time. The GFW's new censorship capability affects a large set of popular censorship circumvention protocols, including but not limited to Shadowsocks, VMess, and Obfs4. Although China had long actively probed such protocols, this was the first report of purely passive detection, leading the anti-censorship community to ask how detection was possible.

In this paper, we measure and characterize the GFW's new system for censoring fully encrypted traffic. We find that, instead of directly defining what fully encrypted traffic is, the censor applies crude but efficient heuristics to exempt traffic that is unlikely to be fully encrypted traffic; it then blocks the remaining non-exempted traffic. These heuristics are based on the fingerprints of common protocols, the fraction of set bits, and the number, fraction, and position of printable ASCII characters. Our Internet scans reveal what traffic and which IP addresses the GFW inspects. We simulate the inferred GFW's detection algorithm on live traffic at a university network tap to evaluate its comprehensiveness and false positives. We show evidence that the rules we inferred have good coverage of what the GFW actually uses. We estimate that, if applied broadly, it could potentially block about 0.6% of normal Internet traffic as collateral damage.

Our understanding of the GFW's new censorship mechanism helps us derive several practical circumvention strategies. We responsibly disclosed our findings and suggestions to the developers of different anti-censorship tools, helping millions of users successfully evade this new form of blocking.

### 2.2 摘要中文翻译

审查规避的基石之一是全加密协议，它将载荷的每个字节都加密以试图"看起来像什么都没有"。2021年11月初，中国防火长城（GFW）部署了一种新的审查技术，能够被动检测并实时阻断全加密流量。GFW的新审查能力影响了大量流行的审查规避协议，包括但不限于Shadowsocks、VMess和Obfs4。虽然中国长期以来一直对此类协议进行主动探测，但这是首次报告纯被动检测，引发了反审查社区对检测原理的疑问。

在本文中，我们测量并表征了GFW审查全加密流量的新系统。我们发现，审查者并非直接定义什么是全加密流量，而是应用粗糙但高效的启发式规则来豁免不太可能是全加密流量的流量，然后阻断剩余的未被豁免的流量。这些启发式规则基于常见协议的指纹、置位比特比例，以及可打印ASCII字符的数量、比例和位置。我们的互联网扫描揭示了GFW检查的流量和IP地址。我们在大学网络Tap的实时流量上模拟推断出的GFW检测算法，以评估其全面性和误报率。我们提供的证据表明，我们推断的规则与GFW实际使用的规则有很好的覆盖度。我们估计，如果广泛应用，可能会阻断约0.6%的正常互联网流量作为附带损害。

我们对GFW新审查机制的理解帮助我们推导出多种实用的规避策略。我们负责任地向不同反审查工具的开发者披露了我们的发现和建议，帮助数百万用户成功规避了这种新形式的封锁。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

2021年11月6日，中国用户报告Shadowsocks和VMess服务器被封锁。这是GFW首次实现纯被动流量分析来实时阻断全加密代理流量，而此前（自2019年5月起）GFW需要被动分析+主动探测两步才能封锁Shadowsocks。由于全加密协议被设计为"看起来像什么都没有"，其被动检测原理对反审查社区是一个谜，因此作者需要逆向分析GFW的检测机制。

### 3.2 现有方法的痛点和不足

| 痛点 | 描述 | 位置 |
|---|---|---|
| 全加密协议的"不可检测"假设被打破 | 业界认为全加密流量无指纹可言，但GFW找到了替代检测路径 | §1 |
| 主动探测防御失效 | Shadowsocks等已部署抗探测设计（自2020年9月起有效），但新封锁完全基于被动分析 | §2.2 |
| 对GFW检测机制一无所知 | 反审查社区无法设计有效的规避策略，因为不了解检测规则 | §1 |
| 已有的被动分析研究停留在PoC阶段 | Wang et al. (2015)、Zhixin Wang (2017)等仅提出概念验证，未分析GFW实际部署的系统 | §2.1 |

### 3.3 论文的研究假设或核心直觉

GFW并非直接识别"全加密流量"（这在计算上很困难），而是采用排除法——通过启发式规则豁免"明显不是全加密"的流量，将剩余未被豁免的流量视为可疑并阻断。这种"反向定义"策略计算成本低、效率高，但天然存在误报。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 2021年11月6日起，中国用户报告Shadowsocks/VMess服务器被封锁；11月8日Outline使用量骤降 | §1, [10], [69] |
| 痛点提炼 | 这是首次纯被动检测全加密流量，此前的主动探测防御措施完全失效 | §1, §2.2 |
| 问题转化 | 从"为什么被封"的工程问题转化为"GFW如何在被动模式下区分全加密流量与正常流量"的科学问题 | §1 |
| 文献定位 | 已有被动分析研究（Wang 2015, Zhixin Wang 2017, Alice et al. 2020）仅关注概念验证或单一协议，未系统逆向GFW实际部署的检测规则 | §2.1 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | GFW使用基于排除法的启发式规则而非机器学习模型来检测全加密流量 | 全加密流量"看起来像随机"的特性可用简单统计量（比特比例、ASCII比例）区分 | 构造满足/违反各规则的探测载荷，观察GFW反应 |
| 辅助假设1 | GFW仅分析TCP连接的第一个数据包 | 全加密流量从第一个字节即加密，无需重组多包 | 分两包发送测试数据（第一包低熵+第二包高熵），观察是否阻断 |
| 辅助假设2 | GFW采用概率性阻断而非确定性阻断 | 可能为降低误报的附带损害和减少计算开销 | 对同一载荷重复25次连接，统计阻断概率 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 排除法启发式规则 | 支撑 | 发现5组豁免规则（Ex1-Ex5），未被豁免的流量被阻断 | §4 |
| 仅分析第一个数据包 | 支撑 | 第一包\x21（低熵）+第二包200字节随机数据，25次均未阻断 | §4.5 |
| 概率性阻断 | 支撑 | 109,489个被阻IP的连接次数分布符合几何分布，p=26.3% | §6.3 |

---

## 4. 方法设计

### 4.1 方法整体流程

本文采用"黑盒逆向"方法论：通过构造精心设计的测试载荷在中国境内和境外主机之间发送，观察GFW的反应（阻断/不阻断），逐步推断出检测规则。具体分为四个实验阶段：(1) 特征化实验——推断5条豁免规则；(2) 活跃探测关系分析——验证新系统与已有主动探测系统的关系；(3) 互联网扫描——确定GFW监控的IP范围和阻断策略；(4) 实时流量评估——在大学网络Tap上验证推断规则的误报率和覆盖率。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| 1. 探测构造 | 各种字节模式 | 生成256种单字节重复100次的模式、随机长度载荷、协议前缀等 | 测试载荷库 | 系统性覆盖各种字节统计特征 |
| 2. 发送并观察 | 测试载荷 + 中/美VPS对 | 从中国VPS发送载荷到美国sink服务器，每种载荷最多25次连接 | 阻断/未阻断标签 | 获取GFW对每种载荷的反应 |
| 3. 残余审查确认 | 被疑似阻断的3-tuple | 发送5个后续TCP连接（间隔1秒），若全部超时则确认阻断 | 确认的阻断事件 | 消除网络抖动等假阳性 |
| 4. 规则推断 | 阻断/未阻断标签集 | 分析哪些字节特征与阻断相关，归纳为规则 | Algorithm 1 (5条豁免规则) | 逆向GFW检测逻辑 |
| 5. 规则验证 | 推断规则 + CU Boulder Tap | 在17亿真实连接上模拟规则，统计被阻断比例 | 误报率(0.6%)、覆盖率 | 验证推断规则的全面性 |
| 6. GFW实测验证 | 442,928个6字节前缀 | 将Tap中会被规则阻断的连接前缀+随机数据发送过真实GFW | 仅1个前缀被豁免 | 确认推断规则与GFW实际规则高度吻合 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 探测生成器 | 生成满足特定约束的测试载荷 | 字节模式配置 | TCP连接+载荷数据 | -> GFW观测 |
| 残余审查检测器 | 通过后续连接确认阻断 | 3-tuple (client IP, server IP, server port) | 阻断/未阻断 | -> 规则推断 |
| 规则推断引擎 | 从阻断模式归纳豁免规则 | 阻断/未阻断标签集 | Algorithm 1 | -> Tap验证器 |
| Tap流量分析器 | 在真实流量上模拟推断规则 | 17亿连接的前6字节+端口号 | 被阻断连接统计、6字节前缀分布 | -> GFW实测验证 |
| 互联网扫描器 | 确定GFW监控的IP范围 | 550万IP地址 | 受影响AS/前缀分布 | -> 阻断策略分析 |

### 4.4 公式、算法和机制解释

**Algorithm 1 — GFW的5条豁免规则**：

GFW对从中国发出的TCP连接的第一个数据包(pkt)应用以下规则，若满足任一豁免条件则放行，否则阻断：

- **Ex1 (popcount熵豁免)**：`popcount(pkt) / len(pkt) <= 3.4` 或 `>= 4.6`。即平均每字节置位比特数偏离4.0（半数）超过0.6则豁免。随机/加密数据的popcount接近4.0，而正常协议（如TLS Client Hello仅1.56 bits/byte）偏离较大。

- **Ex2 (前6字节可打印豁免)**：pkt的前6字节全部在可打印ASCII范围[0x20, 0x7e]内则豁免。

- **Ex3 (50%以上可打印豁免)**：pkt中超过50%的字节在[0x20, 0x7e]范围内则豁免。

- **Ex4 (20字节连续可打印豁免)**：pkt中存在超过20个连续字节在[0x20, 0x7e]范围内则豁免。

- **Ex5 (协议指纹豁免)**：前3-6字节匹配TLS或HTTP协议指纹则豁免。TLS: `[\x16-\x17]\x03[\x00-\x09]`；HTTP: `GET `、`PUT `、`POST `、`HEAD `（大小写不敏感，空格必需）。

**概率性阻断机制**（§6.3）：每个连接有26.3%的概率被阻断，符合几何分布，说明每次连接的阻断决策相互独立。这可能出于两个原因：(1) 仅检查约1/4的连接以减少计算开销；(2) 降低对非代理连接的附带损害。一旦连接被判定阻断，残余审查机制会继续阻断相同3-tuple的后续连接120-180秒。

**残余审查机制**（§4.4）：阻断后，相同(client IP, server IP, server port)的后续TCP连接被持续丢弃120-180秒。但GFW似乎限制了同时进行的残余阻断数量——当同时阻断500个端口时，约40%的阻断仅持续10秒。

### 4.5 方法优势

1. **排除法逆向策略**：通过构造满足单一规则但违反其他规则的载荷，可以隔离每条规则的效果，逐步推断完整规则集。
2. **多层次验证**：推断规则 -> CU Boulder Tap模拟 -> 真实GFW实测，三层验证确保规则准确性。
3. **大规模真实流量评估**：17亿连接的数据规模使误报率估计具有统计可信度。
4. **概率性阻断的精确建模**：通过109,489个被阻IP的连接次数分布精确估计阻断概率为26.3%。

### 4.6 方法不足

1. **规则完备性不确定**：由于GFW的黑盒性质，推断的5条规则可能不是全部规则，可能存在未发现的规则（作者通过Tap验证实验间接证明覆盖率良好，但无法完全排除）。
2. **规则应用顺序未知**：无法确定5条规则的应用顺序，也无法确认是否存在规则组合逻辑（AND/OR）。
3. **时间稳定性**：规则可能随时间变化，作者在2023年2月重测确认规则仍然成立，但长期稳定性未知。
4. **地理局限性**：实验主要使用北京的VPS，不同城市/ISP的GFW部署可能存在差异（作者未观察到差异但样本有限）。
5. **仅覆盖IPv4**：互联网扫描仅针对IPv4，未涉及IPv6流量。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

本文的独特之处在于它不是提出一种新的检测方法，而是**逆向分析**审查者的检测方法。与已有研究的关键区别：

- **相对于Wang et al. (2015)**：Wang使用第一个包的长度和Shannon熵识别obfs4，是PoC级别。本文发现GFW实际使用的是更粗糙但更高效的popcount（比特计数）而非Shannon熵，且结合了ASCII字符分析和协议指纹豁免。
- **相对于Zhixin Wang (2017)的sssniff**：sssniff使用前3个包的Shannon熵。本文证明GFW仅分析第1个数据包，且使用popcount而非Shannon熵。
- **相对于Alice et al. (2020)**：Alice发现GFW使用第一个包的长度和熵来怀疑Shadowsocks，然后主动探测确认。本文发现2021年11月后GFW可纯被动阻断，且检测规则比Alice发现的更复杂（5条豁免规则而非单一熵阈值）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 发现GFW的"排除法"检测范式 | GFW不直接定义全加密流量，而是通过豁免规则排除正常流量 | 高 | 是 — 可用于分析其他国家的审查系统 |
| 推断5条具体豁免规则 | popcount、ASCII前缀/比例/连续长度、协议指纹 | 高 | 是 — 直接指导规避工具开发 |
| 揭示概率性阻断机制 | 26.3%的阻断概率，几何分布 | 中 | 是 — 为审查系统的工程权衡提供实证 |
| 揭示GFW与主动探测系统的关系 | 两系统并行工作，主动探测系统使用相同5条规则+额外长度规则 | 中 | 是 — 说明规避被动检测也会规避主动探测 |
| 大规模误报率评估 | 17亿连接上0.6%的误报率 | 高 | 是 — 为审查成本-收益分析提供量化依据 |

### 5.3 适用场景

- **审查规避工具开发**：直接利用推断的规则设计规避策略（如定制IV前缀、调整popcount）。
- **审查系统研究**：理解国家级审查系统的设计哲学（粗糙启发式 vs 精细机器学习）。
- **加密协议设计**：评估新协议是否容易被类似启发式规则检测。
- **互联网自由度测量**：量化审查的附带损害（0.6%误报率）和覆盖范围（26%连接、特定IP段）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| Shannon熵检测 (Wang 2015, sssniff 2017) | 理论上更精确 | 计算成本高，GFW实际未使用 | 发现GFW使用更粗糙但高效的popcount替代Shannon熵 |
| 被动流量分析+主动探测 (Alice et al. 2020) | 可确认代理身份 | 需要两步，有延迟 | 发现新系统纯被动即可阻断，无需主动探测 |
| 协议指纹匹配 (传统DPI) | 精确 | 仅适用于有固定指纹的协议 | 发现GFW用指纹作为"豁免"而非"匹配"，检测无指纹流量 |
| 机器学习分类器 | 可学习复杂模式 | 计算成本高、不可解释 | 发现GFW使用5条简单规则，计算成本极低 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

论文包含5组主要实验（Table 1）：

| 实验 | 时间跨度 | 中国Vantage Points | 美国Vantage Points | 目标 |
|---|---|---|---|---|
| 特征化实验 | 2021.11.6 - 2022.5.18 (6个月) | 3 (TC,BJ) + 1 (Ali,BJ) | 3 (DO,SFO) | 推断5条豁免规则 (§4) |
| 重测实验 | 2023.2.16 (1天) | 1 (TC,BJ) | 1 (DO,SFO) | 确认规则仍成立 (§4.1-4.3) |
| 活跃探测实验 | 2022.5.19 - 6.8 (3周) | 1 (TC,BJ) | 2 (DO,SFO) | 分析与主动探测系统的关系 (§5) |
| 互联网扫描 | 2022.5.12-13 (2天) | 9 (TC,BJ) | 1 (Scan,Univ) | 确定监控IP范围 (§6) |
| 实时流量评估 | 2022.7-9 (3个月) | 1 (TC,BJ) | 1 (DO,SFO) + 1 (Tap,Univ) | 评估误报率和覆盖率 (§7) |

### 6.2 数据集

| 数据集 | 规模 | 来源 | 特点 |
|---|---|---|---|
| CU Boulder Network Tap | 17亿连接 | 40Gbps校园网络Tap | 真实流量、极少代理流量、用于误报率评估 |
| 10% IPv4 Internet Scan | 550万可用IP (7M原始) | CU Boulder -> 9个北京VPS | 覆盖538个AS、用于确定GFW监控范围 |
| China VPS (TencentCloud) | 10台VPS, 北京AS45090 | 腾讯云 | 主要测量平台 |
| China VPS (AlibabaCloud) | 1台VPS, 北京AS37963 | 阿里云 | 交叉验证平台 |
| US Sink Servers (DigitalOcean) | 4台VPS, SFO AS14061 | DigitalOcean | 监听1-65535所有端口 |

### 6.3 Baseline

本文不与传统分类器比较，而是通过以下方式建立基线：
- **零载荷对照**：发送50字节`\x00`（不触发阻断），排除服务器自身阻断的可能性。
- **已知协议对照**：测试TLS、HTTP、SSH、SMTP、FTP、DNS等常见协议，确认它们被豁免。
- **几何分布拟合**：将阻断次数分布与几何分布(p=0.263)拟合，验证概率性阻断假设。

### 6.4 评价指标

| 指标 | 定义 | 用途 |
|---|---|---|
| 阻断/未阻断 | 5次后续连接全部超时=阻断 | 规则推断的基本信号 |
| 误报率 (FPR) | 在CU Boulder Tap上被模拟阻断的正常连接比例 | 评估附带损害 |
| 覆盖率 | 推断规则与GFW实际规则的一致性（通过实测验证） | 评估推断规则的完备性 |
| 阻断概率 | 被阻断IP的首次阻断前成功连接次数的几何分布参数 | 量化概率性阻断 |
| 受影响IP/AS比例 | 互联网扫描中被标记为受影响的IP和AS占比 | 量化GFW监控范围 |

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 结果 | 说明 |
|---|---|---|---|
| popcount豁免 (Ex1) | 阻断阈值 | 3.4 - 4.6 bits/byte | 256种单字节模式中40种被阻断，全部恰好4 bits set |
| ASCII前缀豁免 (Ex2) | 最小前缀长度 | 6字节 | n<6被阻断，n>=6不阻断 |
| ASCII比例豁免 (Ex3) | 阻断阈值 | 50% | >50%可打印ASCII不阻断 |
| 连续ASCII豁免 (Ex4) | 阻断阈值 | 20字节 | >20连续可打印字节不阻断 |
| TLS协议豁免 (Ex5) | 匹配模式 | `[\x16-\x17]\x03[\x00-\x09]` | 含MPTCP的Application Data情况 |
| HTTP协议豁免 (Ex5) | 匹配模式 | `GET `/`PUT `/`POST `/`HEAD ` | 大小写不敏感，空格必需 |
| 误报率 (FPR) | CU Boulder Tap | 0.6% (约970万/17亿连接) | 如广泛应用的附带损害估计 |
| 覆盖率验证 | 442,928个前缀过GFW | 仅1个前缀被豁免 | 推断规则与GFW实际规则高度吻合 |
| 监控范围 | 受影响IP比例 | 2% (550万IP中) | GFW相当保守 |
| 监控范围 | 受影响连接比例 | 26% | 仅针对特定数据中心IP段 |
| 阻断概率 | 几何分布参数p | 26.3% | 基于109,489个被阻IP |
| 残余审查时长 | 默认 | 120-180秒 | 500端口并发时降至约10秒 |
| UDP影响 | — | 不受影响 | 仅TCP被阻断 |
| 端口范围 | — | 1-65535全部可被阻断 | 使用非标准端口无法规避 |

### 6.6 优势最明显的场景

1. **推断GFW的"反向定义"检测范式**：这是首次揭示国家级审查系统使用排除法而非匹配法检测全加密流量。
2. **概率性阻断的精确量化**：26.3%的阻断概率和几何分布特性为理解审查系统的工程权衡提供了精确的实证。
3. **误报率的严格评估**：17亿连接的数据规模和"前缀过GFW"的验证方法使结论具有高可信度。

### 6.7 局限性

1. **规则完备性无法保证**：作者承认推断的规则可能不是全部，但通过Tap验证实验间接证明了良好覆盖率。
2. **规则应用顺序未知**：无法确定5条规则是并行应用还是有优先级。
3. **中文字符未被豁免**：UTF-8和GBK编码的中文字符均被阻断，但未深入分析原因。
4. **仅分析端口80的扫描结果**：互联网扫描仅针对TCP端口80，其他端口的覆盖情况可能不同。
5. **CU Boulder网络不代表性**：大学网络的流量模式可能与商业ISP不同，0.6%的误报率可能在其他网络中有差异。

---

## 7. 学习与应用

### 7.1 是否开源？

是。代码和数据发布在 https://gfw.report/publications/usenixsecurity23/en

### 7.2 复现关键步骤

1. 在中国境内租用VPS（推荐腾讯云北京），在美国租用sink服务器（监听1-65535端口）。
2. 使用测量工具发送各种构造的载荷（单字节重复、随机长度、协议前缀），每种载荷最多25次连接。
3. 通过残余审查确认阻断：发送5个后续TCP连接（间隔1秒），全部超时则确认阻断。
4. 分析阻断/未阻断标签，归纳豁免规则。
5. 在真实网络流量上模拟推断规则，评估误报率。

### 7.3 关键超参数、预处理和训练细节

| 参数 | 值 | 说明 |
|---|---|---|
| 最大连接次数 | 25 | 每种载荷最多发送25次以应对概率性阻断 |
| 确认连接数 | 5 | 残余审查确认需5次连续超时 |
| 确认连接间隔 | 1秒 | 后续确认连接之间的时间间隔 |
| 残余审查冷却期 | 180秒 | 不重复使用被阻断的3-tuple |
| 单字节重复模式长度 | 100字节 | popcount测试中每种模式的长度 |
| 随机字节测试长度 | 50字节 | popcount阈值测试的载荷长度 |
| popcount阻断范围 | 3.4 - 4.6 bits/byte | Ex1的阈值 |
| ASCII可打印范围 | 0x20 - 0x7e | Ex2-Ex4的可打印字节定义 |

### 7.4 能否迁移到其他任务？

- **审查系统逆向分析**：本文的"构造探测+观察反应+归纳规则"方法论可直接迁移到分析其他国家（如伊朗、俄罗斯）的审查系统。论文提到规避策略在伊朗也有效（§8.3）。
- **加密流量特征分析**：popcount作为粗略熵度量的方法可用于其他需要快速评估流量随机性的场景。
- **DPI系统测试**：残余审查确认方法可用于测试其他DPI系统的阻断行为。

### 7.5 对我的研究有什么启发？

1. **"反向定义"检测范式**：审查者可能不直接检测目标流量，而是排除非目标流量。这种思路对设计抗审查协议有重要启示——规避策略不需要让流量"看起来像"某种允许的协议，只需要满足豁免条件之一即可。
2. **简单规则的威力**：5条简单的启发式规则就能有效检测全加密流量，说明复杂度不是检测能力的必要条件。
3. **概率性阻断的设计智慧**：26.3%的阻断概率在计算成本和审查效果之间取得了平衡，这种工程权衡值得在其他安全系统设计中借鉴。
4. **与主动探测的关系**：被动检测和主动探测使用相同的规则集，说明规避被动检测会同时削弱主动探测能力，这对协议设计有重要指导意义。

---

## 8. 总结

### 8.1 核心思想

> GFW用排除法而非匹配法检测全加密流量。

### 8.2 速记版 Pipeline

1. GFW检查从中国发出的TCP连接的第一个数据包
2. 应用5条豁免规则：popcount偏离半数(Ex1)、前6字节可打印(Ex2)、>50%可打印(Ex3)、>20连续可打印(Ex4)、TLS/HTTP指纹(Ex5)
3. 满足任一规则则放行，否则以26.3%概率阻断
4. 阻断后残余审查相同3-tuple 120-180秒
5. 仅监控26%的连接和特定数据中心IP段

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[censorship-circumvention]] — 审查规避的核心任务域
- [[encrypted-traffic-analysis]] — 加密流量分析技术背景
- [[tunnel-detection]] — 隧道/代理检测的核心任务域

### 9.2 相关方法

- [[traffic-classification]] — 流量分类的通用框架
- [[survey-encrypted-traffic-analysis]] — 加密流量分析综述

### 9.3 相关任务

- [[tunnel-detection]] — 检测加密隧道/代理
- [[encrypted-traffic-analysis]] — 全加密流量的被动检测

### 9.4 可更新的综述页面

- [[survey-encrypted-traffic-analysis]] — 可加入"国家级审查系统检测方法"分类

### 9.5 可加入的对比表

- [[tunnel-detection]] — 可在"检测方法对比表"中加入GFW的启发式规则方法

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| GFW使用排除法而非匹配法检测全加密流量 | "the censor applies crude but efficient heuristics to exempt traffic that is unlikely to be fully encrypted traffic; it then blocks the remaining non-exempted traffic" | Abstract |
| popcount阻断范围为3.4-4.6 bits/byte | "All of the blocked patterns consist of bytes with exactly 4 (out of 8) bits that were 1" + 50字节随机数据实验确认阈值 | §4.1 |
| 前6字节可打印即可豁免 | "for n >= 6 where the first n bytes are ASCII printable characters, no blocking occurs" | §4.2 |
| 超过50%可打印即可豁免 | "blocking when the fraction of printable characters is less than or equal to half" | §4.2 |
| 超过20连续可打印字节即可豁免 | "with n <= 20, the connection was blocked. For n > 20, the connection was not blocked" | §4.2 |
| TLS和HTTP被显式豁免 | TLS: `[\x16-\x17]\x03[\x00-\x09]`; HTTP: `GET `等 | §4.3 |
| GFW仅分析第一个数据包 | 第一包\x21+第二包200字节随机数据，25次均未阻断 | §4.5 |
| 阻断概率为26.3%，符合几何分布 | 109,489个被阻IP的连接次数分布拟合几何分布p=0.263 | §6.3 |
| 仅2%的IP受监控 | "98% of them are unaffected by the GFW's blocking" | §6.2 |
| 仅26%的连接受监控 | "the GFW strategically only monitors 26% of connections" | §1 |
| 误报率约0.6% | "we observe on average that 0.6% of TCP connections from our tap would be blocked" | §7.2 |
| 推断规则与GFW实际规则高度吻合 | 442,928个前缀中仅1个被GFW豁免 | §7.2 |
| UDP不受影响 | "Sending a UDP datagram with a random payload cannot trigger the blocking" | §4.4 |
| 残余审查持续120-180秒 | "it continues to drop all subsequent TCP packets having the same 3-tuple for 120 or 180 seconds" | §4.4 |
| 活跃探测系统与新系统并行工作 | "in more than 99% of the tests, the GFW did not send any active probes to the server before blocking" | §5 |
| 主动探测系统使用相同5条规则+额外长度规则 | "the traffic exempted by any of the five rules discovered in Algorithm 1 will also not trigger the active probing system" | §5 |
| 中文字符不被豁免 | "All of these tests were blocked, suggesting that there is no exemption for Chinese characters" | §4.2 |
| 规则在2023年2月仍成立 | "On February 16, 2023, we reran our experiments and confirmed all detection rules still held" | §4 |

---

## 11. 原始资料链接

- PDF：—
- MinerU Markdown：`02-parsed-markdown/2023-USENIX-How_the_Great_Firewall_of_China_Detects_and_Blocks_Fully_Encrypted_Traffic.md`
- 代码仓库：https://gfw.report/publications/usenixsecurity23/en
- 补充材料：Appendix A（其他临时规避策略）包含在正文中

---

## 12. 后续问题

- GFW是否已更新规则以检测本文提出的规避策略（定制IV前缀、popcount调整）？论文截至2023年2月仍有效，但之后的情况未知。
- 如果GFW开始分析第二个数据包或重组多个数据包，现有规避策略是否仍然有效？
- 其他国家（如伊朗、俄罗斯）是否部署了类似的排除法检测系统？论文提到规避策略在伊朗有效，但未系统分析伊朗的检测机制。
- GFW的概率性阻断参数（26.3%）是否会随时间调整？是否与政治敏感时期相关？
- 基于机器学习的检测方法能否替代启发式规则？计算成本和误报率如何权衡？

---

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

本文从一个具体的"突发事件"出发——2021年11月GFW突然封锁了主流全加密代理工具——然后以"侦探式"的叙事逐步揭示GFW的检测机制。核心张力在于：全加密协议被设计为"看起来像什么都没有"，但GFW找到了一种巧妙的"反向定义"方法——不检测"什么是全加密"，而是排除"什么不是全加密"。最终，理解了检测机制后，作者推导出简单但有效的规避策略，并与开发者合作帮助数百万用户恢复访问。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 呈现核心发现：GFW用排除法检测全加密流量 | 设定全文基调 | "instead of directly defining what fully encrypted traffic is" |
| Introduction | 从突发事件切入，建立研究紧迫性 | 制造悬念：全加密流量如何被被动检测？ | "this was the first report of purely passive detection" |
| Background (§2) | 回顾流量混淆和主动探测的历史 | 提供技术上下文 | 从协议模仿到全加密的范式转变 |
| Methodology (§3) | 介绍黑盒逆向方法论 | 建立可信度 | 残余审查确认+概率性阻断的重复测试策略 |
| Characterization (§4) | 逐步推断5条豁免规则 | 核心技术贡献 | 每条规则的推断过程都是一个小型"破案"故事 |
| Active Probing (§5) | 分析新旧系统的关系 | 扩展贡献 | 两系统并行但共享规则集 |
| Blocking Strategies (§6) | 揭示GFW的工程权衡 | 深化理解 | 概率性阻断(26.3%)+选择性监控(26%连接) |
| Evaluation (§7) | 在真实流量上验证推断规则 | 确认可靠性 | 0.6%误报率+442,928前缀仅1个被豁免 |
| Circumvention (§8) | 推导并部署规避策略 | 实际影响 | 帮助数百万用户 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 场景缺失 | 全加密流量的被动检测此前未被观察到 | 突发事件报道 + 历史对比 | §1 |
| 机制未知 | 无人知道GFW如何检测"看起来像随机"的流量 | 黑盒逆向 + 逐步排除 | §4 |
| 评估不足 | 已有PoC研究未在真实审查系统上验证 | 大规模实证 + GFW实测 | §7 |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 特征化实验 (§4) | 逐步推断5条规则，每条规则一个独立"破案"故事 | 核心贡献，直接支撑"排除法"论点 |
| 活跃探测实验 (§5) | 分析新旧系统关系，扩展对GFW审查架构的理解 | 深化贡献，说明规避被动检测的额外收益 |
| 互联网扫描 (§6) | 揭示GFW的工程权衡（选择性监控+概率性阻断） | 解释为什么0.6%误报率可以接受 |
| 实时流量评估 (§7) | 在17亿连接上验证推断规则 | 确认贡献的可靠性 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 从具体突发事件切入（2021年11月封锁），制造研究紧迫性 | "事件驱动"型开篇，适用于安全/审查领域 |
| Gap 提出方式 | "The anti-censorship community to ask how detection was possible" — 社区困惑即Gap | 将社区未解之谜直接转化为研究问题 |
| 方法论证逻辑 | 黑盒逆向：构造探测 -> 观察反应 -> 归纳规则 -> 大规模验证 | "侦探式"论证，适用于逆向分析类研究 |
| 实验组织逻辑 | 每条规则独立验证 + 规则间交叉验证 + 真实流量总验证 | 逐条推断+整体验证的两层结构 |
| 局限性讨论方式 | 坦诚承认规则完备性不确定，但用Tap验证间接证明覆盖率 | "无法完全证明，但提供强证据"的务实态度 |
| 最值得借鉴的一句话/一段结构 | "instead of directly defining what fully encrypted traffic is, the censor applies crude but efficient heuristics to exempt traffic" — 一句话概括核心洞察 | 用"反向定义"的修辞手法突出方法论创新 |

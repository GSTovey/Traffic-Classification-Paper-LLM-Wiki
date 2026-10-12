---
type: paper
title_original: "DNS Cache Poisoning Like it’s 2006"
title_cn: "DNS 缓存投毒再现：回到 2006"
authors: ["Omer Ben-Simhon", "Amit Klein"]
year: 2026
venue: "USENIX Security 2026"
doi: unknown
url: "https://www.usenix.org/conference/usenixsecurity26/presentation/ben-simhon"
pdf: "00-inbox/PDFs/2026-USENIX-DNS_Cache_Poisoning_Like_it’s_2006.pdf"
mineru_md: "02-parsed-markdown/2026-USENIX-DNS_Cache_Poisoning_Like_it’s_2006.md"
status: deep-analyzed
reading_level: L3
research_area: ["DNS security", "cache poisoning", "PRNG state recovery"]
task: ["DNS cache poisoning", "resolver security evaluation"]
method: ["Xoshiro128** state recovery", "RRset/RRset-ANY", "RR-QMA", "GF(2) linear algebra"]
dataset: ["BIND 9.18/9.20/9.21 controlled testbeds", "FreeBSD 14.3", "open BIND 9.20 resolver safe test"]
code: "yes (Zenodo artifact stated in paper)"
relevance: high
created: "2026-09-29"
updated: "2026-10-10"
---

# DNS Cache Poisoning Like it’s 2006

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



## 深度分析（L3 补充，2026-10-09）

### 3. 研究问题、威胁模型与证据边界

#### 3.1 研究问题

论文检验的是：在 BIND 9 已同时随机化 TXID 和 UDP 源端口、部署 qname minimization、prefetch、DNS Cookies 和状态防火墙的现实条件下，离路径攻击者是否仍能以少量伪造响应恢复 PRNG 状态并完成缓存投毒。核心观察是 BIND 的 Xoshiro128** 同时驱动 TXID、UDP 源端口和 RRset 顺序，若能从 RRset 排列或 TXID 片段恢复内部状态，就可以同时预测两个关键匹配字段（§1、§3）。

#### 3.2 威胁模型

攻击者不能拦截 resolver–authoritative name server（ANS）链路，但可以向目标 resolver/forwarder 发起查询，并发送源地址伪造的 DNS 响应；攻击者的目标是先恢复目标线程的 PRNG 状态，再在真实 ANS 响应之前注入 Kaminsky 风格的 NS 委派和 glue。论文假设目标运行 BIND 9 默认配置、被攻击域通常没有 DNSSEC，并覆盖 9.18 resolver、9.20/9.21 resolver 及 forwarder，负载最高约 10,000 cache-miss QPS（§2）。

论文明确的证据边界是：实验主要使用作者自有默认配置 BIND 服务器和少量安全测试的开放 resolver；生产环境的非默认配置、DNSSEC、NAT 端口重写和更广泛 resolver 软件不在完整验证范围内（§1、§9）。

### 4. 方法机制

#### 4.1 PRNG 状态恢复

BIND 的 Xoshiro128** 状态是 128 位，输出由可逆的 `starstar(x)=9·rotl(5·x,7)` 变换得到。TXID 是输出低 16 位，UDP 源端口由输出映射到系统临时端口范围，RRset 随机排列使用同一输出驱动 Fisher–Yates shuffle（§3.1）。攻击流程分三步：

1. 从 RRset 排列或 TXID 观察中取得完整/部分 PRNG 输出；
2. 通过乘法逆元和旋转逆运算得到内部状态的若干比特；
3. 利用状态转移是 GF(2) 上的线性变换，将多次观测写成 128 位线性方程，使用 Gaussian elimination 恢复初始状态（§3.2、§3.5）。

RRset 变体从一个至少 23 条记录的排列恢复单个 32 位输出：比较 DNSSEC 顺序与返回顺序，得到 Fisher–Yates 的模方程，再用 CRT 求 `x mod lcm(1,…,N)`。论文指出 `N≥23` 时 lcm 超过 2^32，足以唯一恢复输出（§3.3）。TXID 变体从每个 16 位 TXID 提取 seed[0] 的低 9 位；20 个隔步观测共提供 180 个约束，用于恢复 128 位状态（§3.4–§3.5）。

#### 4.2 三种攻击变体

| 变体 | 适用版本/角色 | 观测来源 | 关键特征 | 证据 |
|---|---|---|---|---|
| RRset | BIND 9.20/9.21 resolver | 默认 `rrset-order random` 返回的大 RRset 排列 | 客户端侧；可用第三方大 RRset “living off the land” | §4.2.1 |
| RRset-ANY | BIND 9.20/9.21 resolver/forwarder | 一个 ANY 响应中多个已缓存 RRset 的连续排列 | 单响应原子地获得多个输出，负载下最稳健 | §4.2.1、§5.9 |
| RR-QMA | BIND 9.18/9.20/9.21 resolver | 攻击者 ANS 看到的连续 outbound query TXID | 服务端侧；使用 qname minimization 形成近原子查询批次；可处理 RRset 固定顺序 | §4.2.2–§4.3 |

同一固定客户端 IP–端口组合会被 SO_REUSEPORT 哈希到同一个 worker thread，从而锁定一个 PRNG 实例（§4.1）。9.18 的 listener/worker bucket 模型不同，因此论文在 Appendix B 单独调整 RR-QMA。

#### 4.3 投毒阶段与防御交互

恢复状态和端口范围后，攻击者先发同步查询，再发目标域名的触发查询，随后发送匹配预测的源端口/TXID、伪造源地址为合法 ANS 的响应。payload 采用 Kaminsky 风格的恶意 NS 委派与 glue，使后续解析和 prefetch 转向攻击者 ANS（§4.5、Fig. 2）。

论文分析了三类防御交互：qname minimization 会把相关查询排队并增强 TXID 观测的近原子性；DNS Cookies 在 BIND 的短期合规缓存过期窗口内会暂时被接受缺失 cookie 的响应；stateful firewall 不会阻断该方法所需的标准 DNS 查询/响应流，因为攻击不依赖 ICMP 或关闭端口等异常 side channel（§4.3、§4.6、§6）。这些是论文对默认/特定实现的实验结论，不应泛化为所有 DNS 实现的防御失效。

### 5. 实验设计、数据与结果

#### 5.1 环境

ANS 和非 resolver 机器使用 Azure Standard B2s（2 vCPU/4 GiB），目标 resolver 默认使用 Central US 的 Standard D4as v5（4 vCPU/16 GiB），系统为 Ubuntu 24.04.2/Linux 6.11；BIND 版本为 9.18.38、9.20.11、9.21.10，源码编译、默认配置、jemalloc，启用 qmin/prefetch。10,000 QPS 使用 D16ls v5（16 vCPU/32 GiB）。每个实验统一用 Python 攻击框架生成查询、监视结果和（在自有网络中）伪造响应；§5.2 与 §5.9 各 100 次，其他实验 10 次（§5.1）。

为绕过 Azure 禁止公网源地址伪造，作者把伪造发生在实验网络目的端，通过 iptables SNAT 重写自有入站包源地址；没有把伪造流量发到公网。开放 resolver 实验只比较预测的 TXID/端口与作者 ANS 日志，不实施真正投毒（§5.1、§5.6）。

#### 5.2 关键结果

| 实验 | 结果 | 证据与边界 |
|---|---:|---|
| 基线 RRset | BIND 9.20/9.21，UDP/TCP 均 100%（各 10 次） | Table 2；默认配置、自有 resolver |
| 基线 RRset-ANY | BIND 9.20/9.21，UDP/TCP 均 100%（各 10 次） | Table 2 |
| 基线 RR-QMA | 9.18 UDP 97%、TCP 92%；9.20 UDP 100%、TCP 99%；9.21 UDP 96%、TCP 97% | Table 2；各版本各 100 次 |
| FreeBSD | 三个版本/变体的预测值均 10/10；9.18 另发现 FreeBSD 特定漏洞 | §5.3；实际投毒受平台限制，主要比较预测值 |
| 非 prefetch | 10/10 成功 | §5.4；避免触发 prefetch 的条件 |
| DNS Cookies | cookie 合规缓存未过期时失败；60 s 过期后 RRset-ANY 10/10 成功 | §5.5；BIND 9.20/9.21 实现 |
| 开放 resolver 安全测试 | 5 个 BIND 9.20 中 4 个可用；3 个剩余 resolver 的模拟攻击均在 500 PRNG steps 内成功，83% 偏移在 0–3 | §5.6；仅预测验证，不实施投毒，样本极小 |
| 第三方 ANS/LotL | 10/10 恢复状态，10/10 成功投毒（自有目标 resolver） | §5.7；第三方 ANS 每台约 ≤1 query/s |
| BIND forwarder | RRset-ANY 的 PRNG 预测与缓存投毒均 10/10 | §5.8；Google Public DNS 上游、显式假设 cache miss |
| 高负载 | 1–10,000 cache-miss QPS；RRset-ANY 在 10,000 QPS 仍 >94%；RR-QMA 9.18.37 在 10,000 QPS 完全失败 | Fig. 3–4、§5.9；每个负载点 100 次 |

论文还报告多数成功样本只需偏移 0–3 的少量候选；在 10,000 QPS 下 RRset-ANY 仍保持高成功率，而 RR-QMA 对 9.18 的线程/bucket 代表域查找在高负载下退化（§5.9、§6）。

#### 5.3 局限性

1. 目标主要是自有、默认配置 BIND 9 服务器，开放 resolver 只有 5 个发现样本、4 个可用样本，不能估计互联网范围的漏洞比例。
2. 目标域无 DNSSEC；DNSSEC 验证开启、上游策略、非默认 `rrset-order`、自定义 worker/端口范围以及 NAT 端口改写的完整组合未系统覆盖。
3. 10,000 QPS 实验全部是 cache miss，作者将其视为比生产更苛刻的熵压力；它不等价于真实混合 cache-hit/miss 流量的部署成功率。
4. 投毒成功必须满足攻击者到 resolver 的 RTT 短于 resolver 到合法 ANS 的 RTT；跨网络路径、丢包和源地址过滤可能改变结果（§4.8）。
5. 论文在 patched BIND 发布前进行主体实验；随后 ISC 替换 PRNG 并弃用/移除 random RRset mode 的修复状态不能反推未打补丁系统的现实暴露比例。

### 6. 负责任披露与复现

论文报告 CVE-2025-40780（BIND PRNG）和 CVE-2025-24934（FreeBSD 漏洞）。ISC 在 BIND 9.18.41、9.20.15、9.21.14 中将 Xoshiro128** 替换为更安全的随机源；9.20.13/9.21.12 起文档澄清 RRset random 不保证均匀，9.21.14 移除 random 选项；FreeBSD 于 2025-10-22 发布补丁（§8、Disclosures）。

复现所需环境是受控 testbed：BIND resolver、攻击者客户端、攻击者/真实 ANS；论文称 Zenodo artifact 提供 RRset/RRset-ANY 客户端实现（C++20 + Python）、zone/config 和 README。复现应严格在自有或明确授权环境进行，先复现“预测但不投毒”的开放 resolver 流程，再验证自有 resolver 的受控缓存行为；不应把论文的公网安全测试过程直接外推为生产攻击步骤。

### 7. 总结

> 利用 BIND 共享弱 PRNG 同时预测 TXID、端口并少包投毒。

速记 Pipeline：固定线程观测 RRset/TXID → 逆变换与 GF(2) 线性方程恢复状态 → 推断端口范围 → 同步并触发目标查询 → 伪造 NS/glue 响应 → 在负载、Cookies、qmin 条件下评估。

### 8. 知识链接与同步边界

本笔记可与现有 DNS、anomaly-detection 和恶意流量安全主题交叉阅读；本次不自动创建新概念页、不修改 04–09 层共享表。漏洞编号和补丁状态按论文 Disclosures 记录，引用时需以 ISC/FreeBSD 官方公告再核验当前版本。

### 9. 本地证据记录

| 观点 | 原始资料位置 |
|---|---|
| Xoshiro128** 输出、RRset Fisher–Yates、TXID 低位恢复 | raw Markdown §3.1–§3.5 |
| RRset/RRset-ANY/RR-QMA 攻击流程 | raw Markdown §4.1–§4.5 |
| qmin、DNS Cookies、prefetch、RTT 交互 | raw Markdown §4.3–§4.8 |
| BIND 版本、Azure 环境、实验次数和安全测试边界 | raw Markdown §5.1、§5.6 |
| 基线、负载、开放 resolver 与 forwarder 结果 | raw Markdown §5.2–§5.9、Fig. 3–4、Table 2 |
| CVE、补丁和 artifact | raw Markdown §8–§9、Disclosures、Open Science |

---
## 8. L3 深度方法分析补充

### 8.1 方法动机与流程

论文针对 BIND 9 伪随机数生成弱点，目标是从客户端观测恢复同时决定 UDP 源端口和 DNS TXID 的 PRNG 状态；新颖之处是客户端侧变体无需攻击者自有权威 DNS，旧 9.18 分支另需服务端变体。流程为同步查询/观测输出、恢复 Xoshiro128** 状态、预测偏移、并行伪造响应并验证缓存结果。

### 8.2 实验与局限

实验覆盖 BIND 9.18/9.20/9.21 多版本和不同查询负载；RRset 变体在 10/10 实验中恢复状态并 10/10 投毒成功，RRset-ANY 在最高负载仍保持 94% 以上成功率。高负载下 RR-QMA 在 9.18.37 失效，说明成功率依赖版本、负载与攻击变体。论文已向 ISC/FreeBSD 披露并获得补丁/CVE；DNSSEC 覆盖、生产配置泛化和完整工具链需回看 PDF/披露信息。

### 8.3 写作叙事与知识层建议

论文把“2006 年级别的 DNS 投毒”与现代 BIND 部署联系起来，用 PRNG 状态恢复、客户端可达性和负载曲线逐步证明现实威胁。可向 DNS 安全专题记录；不计入 traffic-* 分类统计。本次未修改共享页面。

## 并行补充块说明

- 本笔记保留了两段同日并行追加的 L3 证据块。前一块是主方法/实验分析，后一块是补充性的流程与边界摘要；二者不是两次独立分析，引用时以主块的完整表格为准。

## 历史自动入库段落说明

- 本笔记前部的自动入库、摘要级或待核验段落是入库时的历史快照，按规范保留以避免删除原始记录。
- 本次新增的深度分析段落、证据记录和局限说明优先；历史段落中的“待深读/待核验”状态不代表当前分析尚未完成。

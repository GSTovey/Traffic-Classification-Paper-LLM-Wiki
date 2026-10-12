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
status: deep-analyzed
reading_level: L3
research_area: []
task: []
method: []
dataset: []
code: unknown
relevance: medium
created: "2026-09-29"
updated: "2026-10-10"
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


## 深度方法分析（2026-10-09）

> 依据本地 MinerU 原文 §1–§7、附录 A–B 追加。该论文是 Internet-wide DNS 测量研究；“潜在恶意/有害”来自异常响应和网页重定向证据，不等同于对服务器运营者的恶意归因。

### 1. 方法动机与问题边界

开放 DNS 地址不一定直接访问权威 DNS，很多服务器是 forwarder，把查询转发给上游 resolver 或另一个 forwarder。客户端只能看到入口服务器，无法知道这些服务器是否共享上游、缓存或 anycast PoP。论文定义 ODNS cluster 为存在直接或间接依赖的一组开放 DNS 服务器，目标是测量这种 client-side dependency、刻画集中化和发现风险。

现有方法依赖权威 DNS 查询日志或已知 public DNS 后端，难以看到 forwarder 之间的隐藏依赖。本文的关键假设是：若多个 ODNS 服务器最终依赖同一上游缓存，向同一 controlled ADNS 查询后，它们会返回相同的唯一 A 记录；不同依赖链在相同时间窗口内返回不同记录。由此可以通过 cache footprint 聚类，而无需知道上游地址。

### 2. 方法设计

#### 2.1 三阶段 ODNS clustering

1. **ODNS discovery**：用 ZMap 脚本向全部可路由 IPv4 地址发送新注册域名的 DNS A 查询；收到 NOERROR 且含 A 记录的 IP 记为开放 DNS。同步检查 transparent forwarders 作为额外观测点。
2. **ODNS labeling**：控制的 ADNS 为每个进入查询生成唯一 A 记录（示例 `0.0.0.1`、`0.0.0.2`）。该记录沿 forwarder 链返回并被上游缓存；随后对每个 ODNS 逐个发送相同查询，读到的唯一记录充当标签。
3. **ODNS clustering**：将共享同一 A 记录的服务器分到同一 cluster。服务器可以因 anycast 或多种 forwarding 策略属于多个 cluster。

该方法的输出是 cluster ID、成员服务器和隐含的依赖关系；它不直接恢复完整的转发路径，只能确定共享缓存/依赖的群组。

#### 2.2 公共 DNS、anycast 和多轮聚合

公共 DNS 的 anycast 地址后面有多个 PoP 和碎片化缓存，单轮测量可能把同一公共 resolver 的 forwarder 错分成多个 cluster。论文使用 5 个 controlled subdomain、每轮重复查询 5 次，再用不同轮次的 cluster overlap 聚合结果：若新轮 cluster 与当前 cluster 的重叠率达到阈值 $\alpha$，则合并；跨轮始终混合的服务器可归入稳定 cluster，属于不同 PoP 的长期稳定 cluster 则保留分开。附录算法 1 对 `C_now` 和 `C_new` 逐个计算 overlap rate 并合并。原文在 MinerU 末尾没有稳定抽取 $\alpha$ 的具体值，需回看 PDF/代码。

为了覆盖 anycast PoP，作者部署新加坡、美国、爱尔兰、乌克兰和巴西 5 个 controlled vantage points；另使用约 37 万个、覆盖 186 个地区的 transparent forwarders 作为补充 vantage points。其覆盖仍偏向透明 forwarder 实际指定的 public DNS。

#### 2.3 集群内服务器分类

对每个 cluster，先向随机服务器发送 controlled A 查询，让响应在转发链缓存；再对同 cluster 其他服务器做 cache snooping：

- 未缓存当前记录的服务器标记为 caching forwarder；
- 已缓存记录、或直接随上游状态变化的 non-caching proxy/上游 resolver 归入 Proxies & Resolver；
- cache snooping 触发 controlled ADNS 新响应的服务器标记为 new-trigger。

该分类依赖缓存观测，不能单独证明服务器的部署角色或完整链路深度。

### 3. 与其他测量方法的差异

| 方法 | 依赖信息 | 可见结构 | 主要限制 | 本文差异 |
|---|---|---|---|---|
| ADNS 日志/编码查询 | 权威 DNS 侧日志或预知 resolver | forwarder→resolver 局部关系 | 看不到 forwarder 间隐藏依赖 | 用 cache footprint 端到端标记 cluster |
| 已知公共 DNS 测量 | 后端地址/服务清单 | 特定 provider | 难覆盖未知 ODNS 和多层转发 | ZMap 全 IPv4 discovery + transparent forwarder |
| 单轮 cache snooping | 一次缓存响应 | 依赖瞬时状态 | anycast/碎片缓存导致误分簇 | 多轮 cluster aggregation + 多 PoP vantage |
| ODNS Clustering | controlled ADNS 唯一 A 记录 | 集群成员、规模、地域和缓存类型 | 不能证明完整路径或恶意归因 | 统一测量开放 DNS 依赖并分析风险 |

### 4. 实验表现、优势与限制

- 测量规模：发现超过 190 万开放 DNS 地址；其中 972,383 台完成完整测量，短期 IP churn（如 DHCP）被排除；成功响应服务器被分成 81,636 个 cluster。
- 规模分布：48,894 个 singleton cluster 覆盖去重后服务器的约 5%；207 个（0.25%）大于 1,000 成员的 cluster 覆盖 429,499 台服务器，占 44.1%；约 95% 开放 resolver 属于多成员 cluster。
- 地域差异：超过 95.5% 的 cluster 至少 99% 成员来自同一国家；中国 86%、韩国 88% 的开放 DNS 位于规模超过 100 的 cluster，德国和法国 singleton 更多，美国以中等规模 cluster 为主。
- 公共 DNS 集中化：前四个公共 DNS provider 的 cluster 覆盖超过 47% 开放 DNS；Google 268 个 cluster、覆盖率 27.99%，Cloudflare 228 个/9.76%，OpenDNS 46 个/5.33%，Yandex 118 个/4.24%。同一 anycast provider 的 cluster 规模不均衡，Google 最大 cluster 超过 23,000 成员。
- 异常响应：91,403 台服务器（9.3%）位于 7,346 个 cluster，对 controlled 查询返回非预期 A 记录；其中 87,753 台返回第三方 public IP，1,473 台返回 private IP，2,177 台返回 loopback。进一步 HTTP 访问中，65 个 cluster（影响 1,581 台 ODNS）重定向到与恶意、钓鱼或滥用 parked domain 相关的页面。
- 集群内角色：Proxies & Resolver 占检测 ODNS 的 61.7% 以上；131 个 cluster 的该比例超过 95%，大 cluster 中非缓存 proxy 更多，可能增加上游流量压力和 DDoS 暴露。

优势是首次在大规模开放 DNS 地址空间上用统一 cache label 测量 client-side 依赖，并把 anycast、地域、错误响应和角色组成放入同一 cluster 视角。局限是：成功测量服务器是 972,383 台而不是全部 190 万，短期 churn 被排除；5 个主动 vantage 和 37 万 transparent forwarder 对未被透明 forwarder 使用的上游覆盖不足；异常 A 记录可能来自管理员配置或服务故障，不能直接认定恶意；多轮聚合阈值、去重和 DNS 缓存 TTL 细节需要代码/附录复核。

### 5. 学习与复现

1. 注册 controlled ADNS 域名，准备多个 subdomain；记录每次响应唯一 A 记录、TTL 和时间窗口。
2. 用 ZMap 扫描可路由 IPv4，按 NOERROR+A 记录筛出 ODNS；同时收集透明 forwarder 列表并标注来源地区。
3. 在至少 5 个 vantage point 重复发送每个 controlled subdomain 的 A 查询，基于返回记录构造初始 cluster。
4. 按附录算法计算跨轮 overlap rate，合并碎片缓存 cluster，保留稳定 anycast PoP cluster。
5. 对 cluster 做 cache snooping 分类，统计 singleton/大 cluster、国家分布、public DNS provider、异常响应和 HTTP 重定向；将主动探测时间、churn 排除和扫描伦理记录在日志中。

论文给出 GitHub 线索 `f-555/ODNS_Clusting`，但当前本地资料未核验代码版本、完整扫描脚本和阈值；DNS 缓存 TTL、重试间隔、$\alpha$、去重规则和 raw scan 清单仍需复现时确认。

### 6. 总结

**核心思想：用缓存指纹测量开放 DNS 依赖。**

速记版 pipeline：

1. 扫描全网开放 DNS 并部署 controlled ADNS。
2. 用唯一 A 记录给转发链留下缓存标签。
3. 按共享标签聚类，多轮聚合处理 anycast 碎片缓存。
4. 分析 cluster 的规模、地域、公共 DNS 集中度和异常响应。
5. 对 cluster 内服务器做 cache snooping，区分缓存转发器和 proxy/resolver。

### 7. 知识层联动建议（不改共享表）

- 在 `05-methods/` 增加“DNS cache footprint clustering”方法条目，记录 discovery、controlled labeling、multi-round aggregation、cache snooping 四步。
- 在 `06-tasks/` 的 DNS/网络测量任务页记录 cluster-level 风险指标：依赖集中、anycast 不均衡、错误响应扩散和 proxy 上游压力。
- 在 `09-claims/` 中将“9.3% 异常响应”写成测量期内的响应异常率，保留可能是误配置或恶意行为的双重解释；本次未修改共享页。

### 8. 证据范围

直接证据为 `02-parsed-markdown/2025-WWW-ODNS_Clustering__Unveiling_Client-Side_Dependency_in_Open_DNS_Infrastructure.md` 的 §1–§7、附录 A–B、表 1–5；对应本地 PDF 已存在。本次未修改 PDF、MinerU 原文或共享对比表。

## 历史自动入库段落说明

- 本笔记前部的自动入库、摘要级或待核验段落是入库时的历史快照，按规范保留以避免删除原始记录。
- 本次新增的深度分析段落、证据记录和局限说明优先；历史段落中的“待深读/待核验”状态不代表当前分析尚未完成。

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

## 深度方法分析（2026-10-09）

> 本节依据本地 MinerU 原文 §1–§6、图 2–11、附录 B–E 整理。论文是主动 DNS 测量研究；manipulation 分类来自解析路径、目的 IP 和服务验证，不能据此直接归因某个 resolver 运营者的主观恶意。

### 1. 研究问题与测量边界

论文研究现代 CDN/多 edge DNS 下如何区分正常的多路径解析与 hijacking、censorship、redirect、cache/response tampering。传统只比对 IP、网页内容或跨 vantage point 的方法会把合法地理分流误报为异常，也可能漏掉只针对少数域名和 resolver 的 partial manipulation。目标是对任意热门域名构造 resolution-path graph，在不依赖 authoritative server 合作或被动流量的情况下识别结构离群路径，并观察操纵目的、链路改写、resolver 选择和域名偏好。

### 2. Resolution-path graph 与异常检测

- **路径采集**：从多个 vantage point 并发向每个 open recursive resolver 查询 NS、CNAME、A，递归直到终止的 A 记录，形成 `Domain → CNAME1 → … → CNAMEk → A`。
- **图建模**：D 节点表示原始域名，C 表示中间 CNAME，A 表示最终 IP；M 为元数据节点。D/C 关联 authoritative NS 和组织，A 关联 IP 的 ASN/组织，D–C–A 用有向边表达解析链，M 与对应节点双向连接。对同一域名所有 resolver 的路径合并为 (G=(V,E))，正常路径可通过共享 NS/组织/ASN 元数据相互连接，异常路径通常引入不相关 CNAME/A 或缺乏元数据连接。
- **Path Divergence**：路径 (P_a=(u_1,ldots,u_p))、(P_b=(v_1,ldots,v_q)) 的结构差异为平均双向最短路径 (rac1{pq}sum_{u\in P_a}sum_{v\in P_b}(d_G(u,v)+d_G(v,u)))，同一路径设为 0。终端附近改动因有向距离增大而得到更高差异。
- **加权 IQR 离群**：每条路径 (P_i) 的分数 (S_i=sum_jN_jD(P_i,P_j))，(N_j) 是共享 (P_j) 的 resolver 数。按 (N_i) 加权的 score 分布求 (Q_1,Q_3)，当 (S_i>Q_3+alpha(Q_3-Q_1)) 时标为潜在 manipulation；默认 (alpha=1.5)。该过程依赖“大多数路径正常且操纵占少数”的假设。

### 3. 规模、采样与验证

- **域名样本**：依据全球热门榜单选取主要 Web 类别，再扩展热门和语义前缀（如 m、mynet、login、mail、auth），共 2,283 个域名；单域最多可产生约 10K distinct paths。
- **Resolver 样本**：复现 ODNS clustering，得到 72,376 个 cluster；按 cluster 比例抽样，并保证大于 100 个成员的 cluster 至少抽 2 个 resolver，得到约 10,000 个 resolver，覆盖 120 个国家。测量 vantage 在马来西亚、美国、中国、芬兰四地。
- **方法验证**：以 www.baidu.com 手工标注 59 条正常路径（覆盖 99.2% normal resolvers）和 11 条 manipulated path（0.8%）。与依赖 HTTP/TLS 的 Iris-style 检查比较，本文方法只提取 1.15% 候选而 Iris-style 为 37.7%，F1 为 0.79。alpha 在 1.21–2.29 范围内保持同一 F1；alpha=0.45 时 F1=0.76，过大则增加 false negative。另用 4 个可明确归因的 ground-truth IP（Private、Abused、两类 Block）验证，检测率均为 2283/2283、219/219、308/308、417/417。

### 4. 全局测量结果

- **总量与分类**：以 domain–resolver pair 为 manipulation 单位，共观测 1,042,360 次，约占全部 probes 的 4.5%。按目的和服务把异常分为六类：Abuse（恶意活动 IP）、Redirect（第三方页面/广告/portal）、Error（过期域或默认页面）、Block（安全/国家级阻断页）、Private/Reserved、Invalid（无活跃服务）。Invalid 最多，其次 Private/Reserved 和 Block；Abuse/Redirect 数量较少但风险更高。
- **目的 IP 集中**：Abuse、Block、Redirect 几乎都集中到少于 100 个 IP；Abuse/Redirect 常集中到单个或极少数 IP，Block 目的 IP 较多，反映显式阻断基础设施。
- **链路改写**：Abuse、Redirect、Private 和 Invalid 多将链路缩短到约 2–3 hops，通过替换中间 CNAME 的 A 记录提前终止；Block 常添加额外 CNAME 使链路变长；Error 结构不稳定。缩短链是高风险 manipulation 的可操作检测信号，但单独不能证明恶意。
- **Resolver 行为**：约 26.4% resolver 只对部分域名进行 manipulation；Abuse/Redirect 几乎都呈 partial pattern。国家差异明显：印尼、俄罗斯多为 Block；墨西哥、西班牙少量域名被重定向到恶意 IP；孟加拉大量 resolver 转发至 Google Public DNS，实际本地递归较少。
- **域名偏好**：按域名数量归一化后，类别影响大于前缀。Porn/Bet 的阻断最突出；Abuse 更偏 Porn，Redirect 更偏 Government；`www` 前缀仍是 redirect 的常见目标。
- **案例**：一个 AbuseIPDB 报告的 abused IP 聚合 3,931 次 manipulation；中间 CNAME 操纵将平均链长从 2.3 缩到 2.1；16 个受影响 resolver 中 15 个只对部分域名操纵；493 个 partial domains 中 51.1% 是 Porn、9.5% 是 Bet。

### 5. 证据边界与解释

论文支持“全球 open DNS 中存在约 4.5% 的 domain–resolver manipulation 报告，且高风险目的高度集中、常缩短解析链并对域名选择性作用”。这些是测量期、样本域名和抽样 resolver 下的比例，不能外推成全球所有 DNS 查询的用户暴露率。Abuse/Redirect 的分类使用 AbuseIPDB、证书和网页/服务检查，仍可能混入误配置、服务故障或瞬态 CDN 变化；partial behavior 与国家分布显示选择性，但不等同于识别了操作者或法律意义上的攻击。

### 6. 局限与复现建议

- **覆盖与偏差**：仅约 10K resolver、2,283 热门域名和四个 cloud vantage；小 cluster、非热门服务、IPv6 resolver、不可访问网页均未覆盖。ODNS cluster 抽样依赖既有聚类和大于 100 的 cluster 阈值，可能过度代表公共/ISP 基础设施。
- **假设与阈值**：方法假设 manipulation 是少数路径，使用加权 IQR \alpha=1.5；高污染或多源 CDN 的域名可能使“多数正常”失效。Path Divergence 需要 Whois/IPInfo ASN/组织元数据和完整 NS/CNAME/A 链，缓存过期、超时与 DNSSEC 行为会影响可比性。
- **验证限制**：Baidu 手工标注和 4 个 ground-truth IP 能验证已知案例，不能形成全球真值集；Iris-style 失败部分源于 15% 域名没有 TLS/HTTP 服务，比较结果不等价于统一 oracle。
- **复现步骤**：先按附录 B/C 生成 2,283 域名和 ODNS cluster 分层的约 10K resolver；从四地并发采集 NS/CNAME/A，缓存 Whois/IPInfo 的 NS/ASN/组织信息；按图结构计算 pairwise Path Divergence、resolver-count 加权 score 与 IQR outlier，再以 AbuseIPDB、网页/证书和人工标注做六类归因。应同时保存测量日期、TTL、重试、超时、α 敏感性和每域/每国分母。论文提供代码与数据仓库 `github.com/f-555/Tracking-Stray-Sheep`（Zenodo DOI 10.5281/zenodo.18297300），复现前仍需核对版本和公开数据范围。

### 7. 方法定位

该方法的核心不是固定“正确 IP”列表，而是把 DNS 解析视为带元数据的图，利用多 resolver 的共享路径结构来容忍合法 CDN 动态，再用路径离群检测选择候选。它适合测量型 DNS 异常发现和后续人工归因；在少量 resolver、强 anycast、频繁 CDN 变更或高比例污染场景，应把结果视为候选而非终局判定。

### 8. 证据范围

直接证据来自本地 `02-parsed-markdown/2026-WWW-Tracking_the_Stray_Sheep__Understanding_DNS_Response_Manipulation_in_the_Wild.md` 的 §3–§6、图 2–11、附录 B–E。数量、阈值、案例和验证比率按正文/附录转写；伦理限制与“恶意”解释保留论文的测量边界。

## 历史自动入库段落说明

- 本笔记前部的自动入库、摘要级或待核验段落是入库时的历史快照，按规范保留以避免删除原始记录。
- 本次新增的深度分析段落、证据记录和局限说明优先；历史段落中的“待深读/待核验”状态不代表当前分析尚未完成。

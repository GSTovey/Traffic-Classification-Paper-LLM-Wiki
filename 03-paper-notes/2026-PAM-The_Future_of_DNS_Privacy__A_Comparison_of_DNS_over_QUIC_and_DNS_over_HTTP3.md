---
type: paper
title_original: "The Future of DNS Privacy: A Comparison of DNS over QUIC and DNS over HTTP/3"
title_cn: "DNS 隐私的未来：DNS over QUIC 与 DNS over HTTP/3 的大规模对比测量"
authors: [Philipp Bielefeld, Felix Hofmann, Stefen Sassalla, vasilis ververis, Vaibhav Bajpai]
year: 2026
venue: "PAM 2026"
doi: "unknown"
url: "unknown"
pdf: "00-inbox/PDFs/2026-PAM-The_Future_of_DNS_Privacy__A_Comparison_of_DNS_over_QUIC_and_DNS_over_HTTP3.pdf"
mineru_md: "02-parsed-markdown/2026-PAM-The_Future_of_DNS_Privacy__A_Comparison_of_DNS_over_QUIC_and_DNS_over_HTTP3.md"
status: processed
reading_level: L2
research_area: [encrypted-traffic-analysis]
task: []
method: []
dataset: [Tranco Top 1M]
code: "https://doi.org/10.5281/zenodo.17860118"
relevance: medium
created: "2026-09-19"
updated: "2026-09-19"
---

# The Future of DNS Privacy: A Comparison of DNS over QUIC and DNS over HTTP/3

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | The Future of DNS Privacy: A Comparison of DNS over QUIC and DNS over HTTP/3 |
| 中文标题 | DNS 隐私的未来：DNS over QUIC 与 DNS over HTTP/3 的大规模对比测量 |
| 作者 | Philipp Bielefeld, Felix Hofmann, Stefen Sassalla, vasilis ververis, Vaibhav Bajpai（Hasso Plattner Institute, University of Potsdam，德国） |
| 年份 | 2026 |
| 会议/期刊 | PAM 2026（Passive and Active Measurement） |
| 研究方向 | encrypted-traffic-analysis（加密 DNS 协议采用度与性能测量） |
| 任务类型 | 互联网测量：DoE resolver 发现、协议特性（session resumption / 0-RTT）支持、网页加载性能影响 |
| 方法关键词 | ZMap IPv4 扫描 + IPv6 Hitlist、RouteDNS 代理（DoQ/DoH/3 及回退）、WebDriver + BrowserMob Proxy（HAR 采集）、HAR 复杂度指标、CDF/相关性分析 |
| 数据集 | Tranco Top 1M（网站源）；自建权威 DNS 服务器采集数据；工件发布含数据集/源码/分析脚本（Zenodo 10.5281/zenodo.17860118） |
| 是否开源 | 是：作者声明 "We release our datasets, source code, and analysis scripts"，工件 DOI 见 `code` 字段（该 DOI 为工件 DOI，非论文 DOI） |
| PDF | 00-inbox/PDFs/2026-PAM-The_Future_of_DNS_Privacy__A_Comparison_of_DNS_over_QUIC_and_DNS_over_HTTP3.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-PAM-The_Future_of_DNS_Privacy__A_Comparison_of_DNS_over_QUIC_and_DNS_over_HTTP3.md |

> 注：解析稿中未出现论文自身的 DOI/URL（参考文献中的 DOI 均属他文），故 `doi`/`url` 填 `unknown`。Zenodo 条目 10.5281/zenodo.17860118 为作者工件（参考文献 [25]，2025 年提交），按规则记入 `code`。

---

## 1. 一句话总结

> 对 3000+ 个 DNS-over-Encryption resolver 做特性与延迟测量、并用百万级网站做端到端网页加载实验，结论是 DoQ 特性采用领先（93% session resumption、2/3 支持 0-RTT）但浏览器仍偏好 DoH/3，且加密 DNS 在低延迟环境下对网页加载的惩罚可忽略（≤1%）。

---

## 2. 摘要翻译

### 2.1 摘要原文

> This study presents a large-scale empirical analysis of DNSover-Encryption (DoE) protocols, focusing on the adoption, protocol feature support, and impact on webpage loading performance. We conducted measurements across over three thousand DoE resolvers, characterizing their support for features such as session resumption and 0-Round-trip Time (RTT) in DNS-over-QUIC (DoQ) and DNS-over-HTTP/3 (DoH/3). Despite broader feature adoption by DoQ, major browsers currently favor DoH/3. Our extensive latency measurements demonstrate that both protocols perform comparably, with DoQ slightly outperforming on average. Complementary experiments with the top one million websites show negligible overall page load time penalties when using DoQ or DoH/3 compared to traditional DNS-over-UDP (Do53), even under low-latency conditions. Further, our analysis explores the relationship between webpage complexity, quantified via metrics including number of objects, queried servers, and MIME type diversity, and the performance impact of DoE. We find no statistically significant correlation, indicating that DoEs performance efects are consistent across a range of website architectures. The study also addresses limitations in current client support for key protocol enhancements and validates efective 0-0-RTT resumption using proxy resolvers. Our findings alleviate prevalent concerns about DoE-induced performance degradation, supporting broader adoption of encrypted Domain Name System (DNS) protocols without sacrificing user experience. We release our datasets, source code, and analysis scripts to facilitate reproducibility and foster further research into encrypted DNS ecosystems.

> ⚠️ MinerU 解析问题：解析稿系统性丢失 ff/fi/ffi 连字（"trafic"、"efect"、"diferent"、"of" 应为 "off"），并有 "0-0-RTT" 之类重复碎片；正文引用时已还原为正常拼写。

### 2.2 摘要中文翻译

本文对 DNS-over-Encryption（DoE）协议做了大规模实证分析，关注其采用情况、协议特性支持以及对网页加载性能的影响。作者测量了三千多个 DoE resolver，刻画它们对 DNS-over-QUIC（DoQ）与 DNS-over-HTTP/3（DoH/3）中会话恢复（session resumption）与 0-RTT 等特性的支持。尽管 DoQ 的特性采用更广，主流浏览器当前仍偏好 DoH/3。大规模延迟测量表明两种协议性能相当，DoQ 平均略优。配合对前一百万个网站的补充实验显示，与传统的 DNS-over-UDP（Do53）相比，使用 DoQ 或 DoH/3 带来的整体页面加载时间惩罚可以忽略不计，即使在低延迟条件下也是如此。作者还分析了以对象数、被查询服务器数、MIME 类型多样性等指标量化的网页复杂度与 DoE 性能影响之间的关系，未发现统计学上显著的相关性，说明 DoE 的性能影响在各种网站架构下是一致的。研究还指出了当前客户端对关键协议增强支持的不足，并验证了通过代理 resolver 可有效使用 0-RTT 恢复。这些发现缓解了关于 DoE 引起性能退化的普遍担忧，支持在不牺牲用户体验的前提下更广泛地采用加密 DNS 协议。作者公开数据集、源码与分析脚本以支持可复现性。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 加密 DNS 要获得广泛采用，必须同时在隐私与性能上可接受；DoT 因性能顾虑采用受限（引 [27]），DoQ/DoH/3 基于 QUIC 声称降低开销。
- 已有研究多比较 DNS 层 RTT，但缺少把网络指标与实际用户体验（页面加载）联系起来的证据（§1）。
- 用户期望页面 2 秒内加载完成，而常访问站点会产生至少 20 次后台 DNS 查询——DNS 层延迟是否影响体验是一个可观测、可证伪的问题（§1）。

### 3.2 现有方法的痛点和不足

| 痛点 | 具体表现 | 解析稿依据 |
|---|---|---|
| 只测 RTT 不测体验 | 既有工作比较 DNS 与各协议的 RTT，缺乏对真实用户体验的验证 | §1 |
| 浏览器偏好与特性采用错位 | DoQ 特性支持更广，但主流浏览器更推荐 DoH/3 | 摘要、§1 贡献 2 |
| 客户端支持限制 | 客户端对关键协议增强（如 0-RTT）支持不足，阻碍特性落地 | 摘要、RQ1 结论 |
| 性能顾虑缺乏端到端证据 | 早期结论称 DoQ/DoH/3 响应时间比 Do53 长 200% 以上，但未落到页面加载层面 | §5.1（与既有结论对照） |

### 3.3 论文的研究假设或核心直觉

核心直觉：DNS 解析在浏览器中与其它任务高度并行，因此 DNS 层响应时间的增加未必传导为页面加载变慢。据此可提出三个可测问题（RQ1–RQ3）：特性支持率、页面加载惩罚、以及复杂度/类型对惩罚的调节作用。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | DoQ/DoH/3 标准化后采用情况不明；浏览器选择与协议特性优劣不一致；已有 RTT 结论彼此矛盾 | §1、§2.9 |
| 痛点提炼 | 若无法证明加密 DNS 不损害体验，部署方会以性能为由延缓采用 | §1 |
| 问题转化 | 把"性能顾虑"转化为三个可测的 RQ：特性支持率（RQ1）、页面加载惩罚（RQ2）、复杂度依赖（RQ3） | §1、§6 |
| 文献定位 | 既有工作停留在 DNS 层指标；本文补上"用户可感知性能"这一环，并给出可复现的测量管线 | §1、§2.9 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | DoQ 与 DoH/3 相对 Do53 的性能惩罚在端到端页面加载层面可忽略 | §1（推断）| 1M 网站 × 3 协议的浏览器实验（§5.1） |
| 辅助假设 1 | 网站复杂度（对象数、服务器数、MIME 类型）会调节 DoE 的性能惩罚 | §1 RQ3 | HAR 指标与惩罚值的相关性热力图（§5.2） |
| 辅助假设 2 | 0-RTT 与会话恢复能弥补 QUIC 类协议相对 Do53 的额外往返 | §4（Do53 1 RTT vs DoQ/DoH3 3 RTT） | resolver 特性统计 + resolve time CDF（§4、Fig. 9） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑（低延迟条件下） | 各协议平均加载时间差在总加载时间的 1% 以内；DoQ/DoH/3 甚至略快于 Do53（出现负惩罚） | §5.1、Fig. 12 |
| 辅助假设 1 | 反驳 | 复杂度特征与惩罚的相关性弱（≤0.45），无显著相关；但与总加载时间正相关 | §5.2、Fig. 13 |
| 辅助假设 2 | 部分支撑 | 支持 0-RTT 的 resolver 平均延迟更低，但在本测量点（光纤）最快响应并不快于无 0-RTT 的；DoH/3 无 0-RTT 支持 | §4、Fig. 9 |

---

## 4. 方法设计

### 4.1 方法整体流程

三套实验：(a) DNS 性能实验——ZMap 扫 IPv4:53 + IPv6 Hitlist，发现 resolver，用 RouteDNS 代理测 DoQ/DoH/3 支持、RTT、会话恢复与 0-RTT；(b) 网页性能实验——用 WebDriver 把浏览器 DNS 指向本地代理（固定使用 resolver64.dns4all.eu），对 Tranco Top 1M 逐协议做 warm-up + 测量两轮导航，采集浏览器性能指标；(c) 网页复杂度实验——BrowserMob Proxy 采 HAR，提取对象数、被查询服务器数、MIME 类型等，与性能惩罚做相关性分析。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 resolver 发现 | IPv4 地址空间 / IPv6 Hitlist | ZMap 扫 UDP/53 请求 www.google.com 的 A 记录（借缓存提高命中）；过滤私网/保留段与被滥用上报段 | resolver 候选列表 | 大规模 DoE resolver 普查（§3.2） |
| Step 2 特性测量 | resolver 列表 | RouteDNS 代理配置 DoQ/DoH/3（含回退），ping 验活，查询探测协议支持、预热缓存、测 RTT/会话恢复/0-RTT | 数据库记录（含元数据） | 回答 RQ1（§3.3） |
| Step 3 权威侧观测 | 自建 bind9 权威服务器（德/奥，按协议分容器，DoT/DoH/2） | 记录进入的查询，识别重放/异常（DNS zombies） | 递归行为统计 | §3.11 递归解析行为 |
| Step 4 网页性能 | Tranco 域名 + 选定 resolver | 启动代理与脚本 → WebDriver 指向本地代理 → warm-up 成功后再测量 → 记录浏览器指标 | 每协议数百万次测量 | 回答 RQ2（§3.4） |
| Step 5 复杂度测量 | 网站列表 | 并行 Python 实例，每站一次查询，BrowserMob Proxy 采 HAR + 截图，抽取对象数/MIME/服务器数 | 复杂度指标表 | 回答 RQ3（§3.5） |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 自建权威 DNS（bind9 + Docker） | 提供按协议隔离的权威解析与日志 | 上游递归查询 | 查询日志/A 记录 | 支撑递归行为观测（Fig. 5） |
| ZMap 扫描器 | IPv4 resolver 发现 | IPv4 地址空间 | 活跃 resolver | 与 IPv6 Hitlist 合并 |
| RouteDNS 代理 | 协议适配与回退（DoQ/DoH/3） | 客户端查询 | 各协议上游查询 | 浏览器实验的统一入口 |
| WebDriver + 浏览器 | 采集页面性能指标 | URL | FCP/onLoad 等指标 | 产出 RQ2 数据 |
| BrowserMob Proxy | HAR 采集 | 页面加载流量 | HAR + 截图 | 产出复杂度指标 |

### 4.4 公式、算法和机制解释

- DNS 加载时间：`T_DNS = domainLookupEnd − domainLookupStart`；网站加载时间：`T_Load = loadEventEnd − fetchStart`；另测 FCP（首内容绘制）作为用户体验代理指标。
- 往返效率论证：Do53 只需 1 个 RTT，DoQ/DoH/3 初始需 3 个 RTT；会话恢复与 0-RTT 可让二者达到 Do53 的往返效率（§4）。
- 相关性分析：对复杂度特征与性能惩罚计算相关系数并绘制热力图，判定"弱相关（≤0.45）"。
- 过滤链：移除有错误的测量 → 排除 loadEventEnd 为 0 而 FCP 非 0 的实例 → 只用测量请求 → 保留三协议都成功的网站 → 46,440 域名（自初始 455,677 收缩）。

### 4.5 方法优势

- 三个互补测量维度（协议特性 / 端到端体验 / 复杂度调节），把 DNS 层指标与用户体验打通。
- 用受控自建权威服务器 + 固定 resolver 控制变量，降低距离与基础设施差异的混杂。
- 数据、源码与分析脚本全部公开（Zenodo），可复现。
- 覆盖 IPv4 与 IPv6 resolver 发现，并给出 70+ 国家与 AS 级分布。

### 4.6 方法不足

- 测量点单一（柏林、光纤低延迟），作者自陈结论可能不适用于高延迟/丢包环境。
- 网页性能实验关闭了 0-RTT 与会话恢复，也未考虑 DNS 缓存，低估了最优配置下的体验。
- DoH/3 的 0-RTT 支持因 stub resolver 限制无法充分评估。
- 解析稿未给出论文 DOI/URL，仅见工件 DOI（见 §0 注）。
- 关键统计口径在原文中不一致（见 §6.2 "572,367 vs 572,345" 与 §6.7）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 维度 | 既有 DoE 性能研究 | 本文 |
|---|---|---|
| 层的选择 | DNS 层 RTT / 查询时间 | 端到端网页加载（FCP / onLoad）+ DNS 层双测 |
| 规模 | 数百至数千 resolver | 3000+ resolver 特性测量 + 1M 网站加载实验 |
| 复杂度建模 | 通常不建模 | 用 HAR 指标量化对象数/服务器数/MIME 并做相关分析 |
| 客户端支持 | 少涉及 | 明确指出客户端 0-RTT 支持是瓶颈，并用代理 resolver 验证 |

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 端到端 DoE 影响评估 | 把 DoE 性能影响下沉到浏览器加载指标 | 高 | 是（任何传输层改造的体验评估） |
| 大规模 resolver 特性普查 | 3000+ resolver 的会话恢复/0-RTT 支持统计 | 高 | 是（协议部署度测量范式） |
| 复杂度-性能相关性分析 | 证明网站架构不调节 DoE 惩罚 | 中 | 是 |
| 0-RTT 代理验证 | 借代理 resolver 绕过客户端限制验证 0-RTT | 中 | 是 |
| 递归侧异常观测 | 22% 查询被重放（DNS zombies，集中在中国 AS）、142 例返回 0.0.0.0 | 中 | 是（DNS 生态健康度测量） |

### 5.3 适用场景

浏览器厂商与 resolver 运营方评估加密 DNS 部署代价；隐私监管/政策讨论中用于反驳"加密 DNS 拖慢上网"的论点；测量方法论可迁移到其它传输协议升级（如 QUIC/HTTP/3 在 Web 场景的收益评估）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| Do53（DNS over UDP） | 最快（中位 33 ms）、单 RTT | 明文，可被监听/篡改 | 用 DoQ/DoH/3 加密，并证明体验代价可忽略 |
| DoT（DNS over TLS） | 部署早、明文端口明确 | 性能顾虑导致采用受限（引 [27]） | 本文作为对照协议之一（延迟中位约 60 ms） |
| DoH/2 | 复用 HTTPS 生态 | 依赖 TCP/HTTP 层，往返多 | 作为对照协议之一（特性支持最少、被 AdGuard 离群值主导） |
| DoQ | 特性支持最全（93% 会话恢复、约 2/3 支持 0-RTT），延迟平均略优 | 浏览器偏好度低于 DoH/3；长尾慢 resolver 较多 | 指出浏览器选择与协议能力的错位 |
| DoH/3 | 加载时间更稳定（中位/平均表现更好） | 无 0-RTT；391/401 resolver 测量失败，可靠性差 | 指出其优化空间与实验性部署比例高的可能原因 |
| oDoH | 进一步隐藏客户端身份（代理 + HPKE） | 额外一跳，本文未测其性能 | 作为背景（§2.6），指出未来方向 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

三类实验：(1) DNS 性能——从柏林单一测量点，跨 5 个 DoE 协议做扫描、探测与延迟测量（28,792 次成功 DoE 查询）；(2) 网页性能——2024-10-22 至 10-31，三种 stub resolver 实例，固定使用 resolver64.dns4all.eu 保证距离一致，对每协议 719,281 个网站做 warm-up + 测量导航；(3) 复杂度——并行抓 HAR，提取对象数、被查询服务器、MIME 类型等，并与惩罚做相关分析。测试协议组合含 DoH/1.1、DoH/2、DoH/3、DoT、DoQ、Do53。伦理方面使用 MassDNS 滥用上报列表过滤扫描目标（§3.6）。

### 6.2 数据集

| 数据集/来源 | 规模 | 用途 |
|---|---|---|
| resolver 发现集 | IPv4 ZMap 扫描 + IPv6 Hitlist；观察分布于 70+ 国家；DoQ/DoH/2 覆盖数百 AS，DoH/3 与 DoT 集中在少数 AS（如 AdGuard） | 特性与延迟测量（§3.2、§3.7） |
| 网页实验集 | 每协议探测 719,281 个网站；成功加载 1,869,105 次；过滤后 46,440 域名（自初始 455,677 收缩） | RQ2 端到端性能 |
| 复杂度统计 | 中位网页 1.2 MB / 42 个资源 / 7 个服务器 / 7 次 DNS 解析（其中 5 次为域外）；中位加载约 0.9 s | RQ3 |
| 自建权威日志 | 75,299 条带标记查询 | 递归行为观测 |
| 公开工件 | Zenodo 10.5281/zenodo.17860118（数据集/源码/脚本） | 可复现性 |

> ⚠️ 原文内部数字不一致（如实并列）：§5.1 写复杂度测量成功加载 "572,367 websites"，§5.2 写 "only 572,345 of these websites were accessible"；两处相差 22 个网站，解析稿未给出解释。

### 6.3 Baseline

对照协议包含 Do53（UDP）、DoT、DoH/1.1、DoH/2、DoQ、DoH/3。网页加载层面以 Do53 作为基准计算 performance penalty；另与传统结论（DoQ/DoH/3 响应时间比 Do53 长 200%+）作对照（§5.1）。

### 6.4 评价指标

中位/最快/最慢响应时间（ms）、请求成功与失败数、会话恢复数与 0-RTT 支持数、T_DNS 与 T_Load、FCP、95 分位区间、复杂度特征与惩罚的相关系数、TLS 版本与密码套件分布。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法（DoQ / DoH3） | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| 会话恢复支持 | 数量/比例 | DoQ 1039/1112（≈93%）；DoH/3 131/202（65%） | — | — | 贡献 1、§4、Table 1 |
| 0-RTT 支持 | 数量 | DoQ 733（约 2/3）；DoH/3 0 | — | — | DoH/3 无 0-RTT（Table 1） |
| 中位响应时间 | ms | DoQ 88（第三轮 71）；DoH/3 883（第三轮 2000） | UDP 33（第三轮 32） | — | DoH/3 受 AdGuard 离群值影响 |
| 最快响应 | ms | DoQ 37；DoH/3 55 | UDP 5 | — | UDP 优势或来自 resolver 就近 |
| 可靠性 | 失败数 | DoH/3：391 失败 / 401（原文表述为 "391 out of 401 resolvers failing measurements"） | DoQ 3；UDP 3 | — | 与回退机制无关 |
| 端到端页面加载 | 相对惩罚 | ≤1% 总加载时间（DoQ/DoH3 对 Do53） | — | 负惩罚（略快） | §5.1、Fig. 12 |
| 复杂度相关性 | 相关系数 | ≤0.45（弱相关） | — | 不显著 | §5.2、Fig. 13；与总加载时间正相关 |
| 批量测量规模 | 网站/加载 | 每协议 719,281 网站；1,869,105 次成功加载；终集 46,440 域名 | — | — | §5.1 |
| 递归行为 | 重放比例 | 75,299 条标记查询中约 22% 被重放（最长延迟数周） | — | — | 集中于中国 AS；142 例返回 0.0.0.0 |
| TLS 安全属性 | 版本/套件 | 99% 偏好 TLS 1.3；AES-128-GCM-SHA256 >90% | — | — | 未见弱配置（§3.10） |

### 6.6 优势最明显的场景

在低延迟（光纤）环境下推动加密 DNS 部署的政策与工程论证：本文给出的端到端证据表明，加密 DNS 的体验代价可忽略，从而削弱"隐私换性能"的反对理由。

### 6.7 局限性

作者自陈：高延迟/丢包环境下结论可能不同；网页实验未启用 0-RTT/会话恢复与 DNS 缓存，可能低估最优配置；DoH/3 的 0-RTT 支持无法充分评估。笔记补充：单一测量点（柏林）限制外推；DoH/3 结果被 AdGuard resolver 主导（约占数据集 85%），协议间比较受运营方差异混淆；两处网站计数不一致（见 §6.2 警示）。

---

## 7. 学习与应用

### 7.1 是否开源？

是。作者声明公开数据集、源码与分析脚本，工件 DOI 为 `10.5281/zenodo.17860118`（已记入 `code` 字段；该 DOI 属工件而非论文本身，故未写入 `doi`）。

### 7.2 复现关键步骤

1. 用 ZMap 扫 IPv4:53（请求 www.google.com A 记录）+ IPv6 Hitlist 获取 resolver 列表，剔除私网/保留段与滥用上报段。
2. 部署 RouteDNS 代理为 DoQ/DoH/3（含回退）配置，探测协议支持；预热缓存后测 RTT、会话恢复与 0-RTT。
3. 自建 bind9 权威服务器（德/奥，按协议分 Docker 容器）用于观测递归与重放行为。
4. 用 WebDriver 把浏览器 DNS 指向固定 resolver 的本地代理，对 Tranco 域名做 warm-up + 测量两轮，记录 FCP/onLoad 等指标。
5. 用 BrowserMob Proxy 采 HAR + 截图，抽复杂度指标，计算与性能惩罚的相关系数。

### 7.3 关键超参数、预处理和训练细节

固定 resolver：resolver64.dns4all.eu（排名 53，稳定性优先；排名 1 的 2f07i9strpu.dns.controld.com 在大规模实验中出现频繁超时）；网页实验关闭 0-RTT 与会话恢复；过滤链见 §4.4；MIME 分析只保留出现 >100 次的 82 种类型并分析前 40 种；相关性判定阈值 0.45。

### 7.4 能否迁移到其他任务？

- **测量范式**：三层结构（协议特性普查 → 端到端体验 → 复杂度调节）可迁移到任何"协议升级是否伤害用户体验"的评估（HTTP/2→3、TCP→QUIC、加密化改造）。
- **陷阱规避**：单一 resolver 固定化 + 距离控制 + 多协议同集网站过滤，是可复用的控制变量方案。
- **安全侧启示**：解析稿给出的 resolver 生态异常（22% 重放、0.0.0.0 响应、加密递归到权威端点（RFC 9539）零采用）可作为 DNS 供应链安全研究的入口。
- **对流量分析的意义**：加密 DNS 的普及与特性差异（如 0-RTT、会话恢复）会改变加密流量的可观测结构，是流量分类/指纹识别研究需要跟踪的底层变化。

### 7.5 对我的研究有什么启发？

- 论文把"隐私 vs 性能"的对立转化为可证伪的测量问题，并得到"惩罚可忽略"的结论——这是用端到端指标纠正社区直觉的范例。
- 需要警惕两个方法论陷阱：(a) 用单一 resolver 代表协议（AdGuard 主导了 DoH/3 结果）；(b) 用"最差站点"放大均值（DoQ 的 onLoad 尖峰来自少数离群站点）。
- 论文提及客户端 0-RTT 支持不足这一"落地瓶颈"，提示协议设计的收益常受客户端实现限制，评测应分层（协议能力 / 客户端能力 / 生态采用）。

---

## 8. 总结

### 8.1 核心思想

> 加密 DNS 的 DNS 层代价真实存在，但传导不到用户感知的页面加载。

### 8.2 速记版 Pipeline

1. ZMap + IPv6 Hitlist 发现 3000+ DoE resolver，测协议支持、会话恢复与 0-RTT。
2. 从柏林单点测 RTT：DoQ 中位 88 ms 明显优于 DoH/3 的 883 ms，UDP 33 ms 最快。
3. 固定 resolver64.dns4all.eu，对 Tranco Top 1M 每协议探测 719,281 个网站，记录浏览器加载指标。
4. 过滤到 46,440 个三协议皆成功的域名后比较：平均加载差异 ≤1%，DoQ/DoH3 甚至略快于 Do53。
5. 用 HAR 复杂度指标做相关分析：与性能惩罚无显著相关（≤0.45），但与总加载时间正相关。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[encrypted-traffic-analysis]] — 加密 DNS 的采用度与性能测量，是加密流量生态的底层观测视角

### 9.2 相关方法

（无直接对应页：本文为互联网测量工作，不使用 kb 方法白名单中的任何方法范式。）

### 9.3 相关任务

（无直接对应页：任务白名单以分类/检测类任务为主，本文不涉及。）

### 9.4 可更新的综述页面

- [[survey-encrypted-traffic-analysis]] — 可增补"加密 DNS（DoQ/DoH3）协议特性采用度与端到端性能"的背景数据

### 9.5 可加入的对比表

（不适用：本文未提出分类方法或新数据集供横向对比。）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| DoQ 会话恢复支持 1039/1112（≈93%）；DoH/3 为 131/202（65%） | Table 1 | §4、Table 1 |
| DoQ 0-RTT 支持 733 个；DoH/3 为 0 | Table 1 | §4 |
| 中位响应时间：DoQ 88 ms（第三轮 71），DoH/3 883 ms（第三轮 2000），UDP 33 ms（第三轮 32） | Table 1 | §4、Table 1 |
| 最快响应：UDP 5 ms、DoQ 37 ms、DoH/3 55 ms | Table 1 + §4 正文 | §4 |
| DoH/3 可靠性最差：391 失败 / 401（原文表述），与回退机制无关 | Table 1 及正文 | §4 |
| 端到端页面加载差异在总加载时间 1% 以内，DoQ/DoH/3 甚至出现负惩罚 | Fig. 12 | §5.1 |
| 复杂度（对象数/服务器数/MIME）与性能惩罚弱相关（≤0.45），但与总加载时间正相关 | Fig. 13、Fig. 14 | §5.2 |
| 规模：每协议 719,281 网站；1,869,105 次成功加载；终集 46,440 域名（自 455,677） | 测量规模陈述 | §5.1 |
| 中位网页：1.2 MB / 42 资源 / 7 服务器 / 7 次 DNS 解析（5 次域外），中位加载约 0.9 s | 复杂度统计 | §5.2 |
| 网站计数不一致：§5.1 为 572,367，§5.2 为 572,345 | 两处原文并列 | §5.1、§5.2 |
| 28,792 次成功 DoE 查询；DoT 平均延迟最低（中位约 60 ms）；AdGuard/Control D 子集内协议中位 115–123 ms | Fig. 8 及相关正文 | §3.8 |
| 递归行为：75,299 条标记查询中约 22% 被重放（集中于中国 AS）；142 例返回 0.0.0.0；无 resolver 使用加密递归到权威（RFC 9539） | 权威侧日志分析 | §3.11 |
| TLS：99% 偏好 TLS 1.3，AES-128-GCM-SHA256 占 >90%，未见弱配置 | 安全属性统计 | §3.10 |
| resolver 分布于 70+ 国家；DoH/3 与 DoT 集中于少数 AS（如 AdGuard） | 地理/AS 分布分析 | §3.7 |
| 论文自身 DOI/URL 未出现在解析稿中；仅见工件 DOI 10.5281/zenodo.17860118 | 参考文献 [25] 与正文发布声明 | §0 注、§7.1 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-PAM-The_Future_of_DNS_Privacy__A_Comparison_of_DNS_over_QUIC_and_DNS_over_HTTP3.pdf
- MinerU Markdown：02-parsed-markdown/2026-PAM-The_Future_of_DNS_Privacy__A_Comparison_of_DNS_over_QUIC_and_DNS_over_HTTP3.md

---

## 12. 后续问题

- 高延迟/有丢包环境（移动网络、跨洲链路）下结论是否仍成立？作者自陈未覆盖。
- 若启用 0-RTT、会话恢复与 DNS 缓存，DoQ 相对 DoH/3 的优势会扩大到什么程度？
- DoH/3 结果被 AdGuard resolver 主导（约占 85%），若剔除后协议排序是否反转（原文提到剔除后近半 DoH/3 resolver 与 DoQ 持平）？
- RFC 9539（加密的递归到权威）零采用的原因是什么——性能、运维复杂度还是生态激励？
- 22% 查询重放（"DNS zombies"）的成因与安全影响需专门研究，本文仅作观测。
- 该测量方法可迁移到 ECH、DoH 到应用层网关等后续隐私增强技术的体验评估。

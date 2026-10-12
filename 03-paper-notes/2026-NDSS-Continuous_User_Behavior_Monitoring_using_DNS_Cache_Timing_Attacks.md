---
type: paper
title_original: "Continuous User Behavior Monitoring using DNS Cache Timing Attacks"
title_cn: "基于 DNS 缓存计时攻击的持续用户行为监控"
authors: [Hannes Weissteiner, Roland Czerny, Simone Franza, Stefan Gast, Johanna Ullrich, Daniel Gruss]
year: 2026
venue: "NDSS 2026"
doi: "10.14722/ndss.2026.242287"
url: "https://doi.org/10.14722/ndss.2026.242287"
pdf: "00-inbox/PDFs/2026-NDSS-Continuous_User_Behavior_Monitoring_using_DNS_Cache_Timing_Attacks.pdf"
mineru_md: "02-parsed-markdown/2026-NDSS-Continuous_User_Behavior_Monitoring_using_DNS_Cache_Timing_Attacks.md"
status: deep-analyzed
reading_level: L3
research_area: ["DNS cache side channel", "privacy leakage", "network security"]
task: ["continuous user behavior monitoring", "timing side-channel measurement"]
method: ["Evict+Reload", "DNS cache eviction", "scriptless browser timing"]
dataset: ["103-domain open-world list", "10-domain browser evaluation"]
code: "unknown"
relevance: low
created: "2026-09-19"
updated: "2026-10-10"
---

# Continuous User Behavior Monitoring using DNS Cache Timing Attacks

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Continuous User Behavior Monitoring using DNS Cache Timing Attacks |
| 中文标题 | 基于 DNS 缓存计时攻击的持续用户行为监控 |
| 作者 | Hannes Weissteiner, Roland Czerny, Simone Franza, Stefan Gast, Johanna Ullrich, Daniel Gruss(格拉茨工业大学 + 维也纳大学) |
| 年份 | 2026 |
| 会议/期刊 | NDSS 2026 |
| 研究方向 | 无白名单概念页对应(本地 DNS 缓存侧信道 / 用户行为监控;论文明确声明**不属于** website fingerprinting) |
| 任务类型 | 无白名单任务页对应(非流量分类/指纹识别任务,而是缓存侧信道测量) |
| 方法关键词 | Evict+Reload、DNS cache eviction primitives、timing side channel、CORS preflight、CSS font fallback(scriptless) |
| 数据集 | 103 个网站(Alexa Top 100 + 若干自有域)的开放世界测量;10 网站 JS 端到端评测 |
| 是否开源 | 解析稿未提及代码/artifact 发布 |
| PDF | 00-inbox/PDFs/2026-NDSS-Continuous_User_Behavior_Monitoring_using_DNS_Cache_Timing_Attacks.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-NDSS-Continuous_User_Behavior_Monitoring_using_DNS_Cache_Timing_Attacks.md |

---

## 1. 一句话总结

> 用 4 种免特权 DNS 缓存驱逐原语 + 3 种跨环境测量原语做 Evict+Reload,从 VM/JS/纯 HTML 持续监控受害者访问了哪些网站。

---

## 2. 摘要翻译

### 2.1 摘要原文

> "The Domain Name System (DNS) is a core component of the Internet. ... Prior work showed that DNS caches can be exploited via timing attacks to test whether a user has visited a specific website recently but lacked eviction capabilities, i.e., could not monitor when precisely a user accessed a website; others focused on DNS caches in routers. All prior attacks required some form of code execution (e.g., native code, Java, or JavaScript) on the victim's system, which is also not always possible. We introduce DMT, a novel Evict+Reload attack to continuously monitor a victim's Internet accesses through the local, system-wide DNS cache. ... In an end-to-end cross-VM attack, we can detect website visits from a list of 103 websites (in an open-world scenario) reliably with an F score of 92.48 % within less than one second. In our JavaScript-based attack, we achieve F1 scores of 82.86 % and 78.89 % for detecting accesses to 10 websites, with and without DNSSEC, respectively."(节选自 Abstract)

### 2.2 摘要中文翻译

DNS 是互联网核心组件,客户端通过查询 DNS 服务器把域名解析为 IP;本地 DNS 缓存缓解了解析时延。已有工作表明 DNS 缓存可被计时攻击利用来测试用户"最近是否访问过某网站",但缺乏**驱逐(eviction)能力**——即无法精确监控用户"何时"访问了网站;另一些工作则聚焦路由器中的 DNS 缓存。所有先前的攻击都要求受害者系统上能执行某种代码(原生代码、Java 或 JavaScript),而这并不总是可行。本文提出 DMT:一种针对本地**系统级** DNS 缓存的 Evict+Reload 攻击,可持续监控受害者的上网行为。其基础是可靠的 DNS 缓存驱逐——论文给出 4 种驱逐技术,覆盖非特权/沙箱原生代码、跨 VM 虚拟化、以及浏览器场景(带 JS 的网站与利用字体串行加载的**无脚本**攻击)。该攻击在默认配置、启用 DNS-over-TLS、启用 DNSSEC 以及使用非默认 DNS 转发器时均有效。跨所有上下文,最快驱逐原语的平均驱逐时间为 77.267 ms;100 个域的测量时间在最好情形(跨 VM)平均 685.86 ms,最差情形(JS 攻击)平均 14.710 s。因此在 5 分钟粒度下攻击盲区最好小于 0.26%、最差 4.92%,攻击可靠。跨 VM 端到端攻击可在 1 秒内以 F1 92.48% 从 103 个网站(开放世界)中检测访问;基于 JS 的攻击对 10 个网站的 F1 分别为 82.86%(有 DNSSEC)与 78.89%(无 DNSSEC)。作者认为 DMT 泄露的信息可用于勒索与诈骗活动,或用于投放针对受害者 EDR 方案定制的攻击载荷。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法?

缓存天然引入侧信道[78]:DNS 缓存把"最近解析过的域名"保存在本地,命中与未命中之间存在显著时延差。2003 年的 Felten & Schneider 便已指出本地 DNS 缓存的信息泄露,但他们只做了单次、破坏性测量的有限实验;Grangeia 总结过三种测量网络 DNS 缓存状态的方法(Klein & Pinkas 用 DNS 记录组合跨浏览器追踪用户;Bushart & Rossow 则只依赖 DoT/DoH 加密 DNS 流量做被动指纹)。作者认为这类工作缺少**持续监控能力**(§I、§II-B)。

### 3.2 现有方法的痛点和不足

- **缺驱逐能力**:读取缓存是破坏性操作(读一次就把目标域名放进缓存),没有可靠的驱逐原语就无法做 Evict+Reload,也就无法把时间分辨率压到 TTL 之下(§I);
- **目标错位**:并发工作 Moav et al.(DNS FLaRE,USENIX Security 2025)攻击**路由器**的 DNS 转发器,可覆盖 IoT 设备;本文攻击**本地系统级**缓存,二者正交(§II-C);
- **前提过强**:先前攻击都要受害端能执行代码(原生/Java/JS),而禁用 JS 或沙箱环境会阻断这些路径(Abstract, §I);
- **resolvectl 不可用**:resolved 中冲刷缓存虽是非特权操作,但 `resolvectl` 接口在 VM、应用沙箱与浏览器中都不可用,必须另找驱逐手段(§I、§IV-A)。

### 3.3 论文的研究假设或核心直觉

核心直觉:只要缓存存在,命中/未命中的时延差就存在,而**驱逐可以完全依赖解析器自身的合法行为**(填满缓存、大响应、错误回退),不需要任何特权接口或其自身漏洞。由此把"监控用户行为"归约为"周期性驱逐 + 单次计时测量"(§IV, Figure 1)。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 命中与未命中解析时延长差显著(原生代码下 DNSSEC 场景平均偏差 20.663 ms,无 DNSSEC 6.701 ms) | §V-D, Table I |
| 痛点提炼 | 读取是破坏性的,不驱逐就只能"测一次",无法做持续监控 | §I |
| 问题转化 | 把任务形式化为"在受限执行上下文(VM/JS/无 JS 浏览器)中构造可靠缓存驱逐 → 恢复 Evict+Reload 循环" | §IV |
| 文献定位 | 本地 DNS 缓存的持续监控此前无工作;路由器场景有并发工作;浏览器缓存侧信道研究充分但 DNS 缓存被忽视 | §II, §II-C |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 存在不依赖特权接口、可在 VM/浏览器上下文中触发的 DNS 缓存驱逐原语,使本地 DNS 缓存的 Evict+Reload 循环可行 | §IV(4 种原语的设计) | 实验:跨 VM 端到端、JS 端到端、无脚本端到端 |
| 辅助假设 | DNSSEC/DoT/VPN 这类"传输层保护"不会缓解该侧信道,反而因时延增大而提升可靠性 | §IX 的论证(保护的是传输中的数据,而非本地缓存) | Table I / Table V 的有无 DNSSEC 对比 |

**假设验证结果**:

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 驱逐原语可行 | 支撑 | 4 种原语:直接冲刷 10.987 ms、大量请求 5.109 s、大响应 1.387 s、错误回退 79.1 ms–5 s | Table III |
| 持续监控可行 | 支撑 | 5 分钟粒度盲区 0.26%(最好)–4.92%(最差);每分钟可探测并驱逐 3 次 | §I, Abstract |
| 端到端可靠 | 支撑 | 跨 VM 开放世界 103 域 F1 92.48%(TP 22999 / FN 3502 / FP 240 / TN 314498) | Table IV |
| 加密/DNSSEC 无助 | 支撑 | 无 JS 纯 HTML 场景仍达 87.5% 可靠性;DNSSEC 使 FN 从 24.192% 降到 13.641%(F1 78.89%→82.86%) | Table I, Table V |

---

## 4. 方法设计

### 4.1 方法整体流程

DMT 循环 = **驱逐 → 测量 → 判决**:攻击者周期性用驱逐原语清空本地系统级 DNS 缓存(同时也要绕过浏览器私有 DNS 缓存),随后对目标域名做**一次**计时测量——命中(缓存中已有,说明受害者最近访问过)耗时短,未命中则需走 DNS 网络往返,耗时长。以阈值判决每次测量为 hit/miss,并以滑动窗口(如最近 10 次测量的中位数 + 网站特定偏移)平滑网络抖动(§VII)。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 起手 | 恶意网页或 VM 内进程 | 部署自建 DNS 服务器 + Web 服务器,离线阶段标定每个目标域的 hit/miss 直方图 | 每域阈值 | 建立判决基准(§VII) |
| Step 2 驱逐系统缓存 | 目标域列表 | 选用 4 种原语之一(Table III):`resolvectl flush-caches`(仅 shell)/ 大量随机长 TTL 请求填满缓存 / 大响应打洞 / 触发 resolved 的错误回退冲刷 | 空的系统 DNS 缓存 | 恢复可测量的初始状态 |
| Step 3 绕过浏览器缓存 | 1000 个攻击者控制的域 | 用长 TTL 条目填满浏览器私有 DNS 缓存(Chromium 1000 条 / Firefox 800 条) | 后续真实解析被推到系统缓存 | 使浏览器场景仍能观测系统级缓存 |
| Step 4 测量 | 目标域 | 原生:`socket.gethostbyname`;JS:`fetch`(CORS 预检在下载内容前终止,噪声更小);无脚本:两个 attacker 侧请求夹住目标请求,在服务器端测时差 | 一次耗时样本 | 单次测量判定 hit/miss |
| Step 5 判决 | 耗时样本 | 与该域阈值比较(阈值来自 10 次测量中位数 + 网站特定偏移) | 该域是否被访问 | 输出行为信号 |
| Step 6 循环 | — | 重复 Step 2–5;实测每分钟可探测并驱逐约 3 次 | 连续行为时间线 | 达到 5 分钟粒度下 ≤4.92% 盲区 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 驱逐原语集(4 种) | 在无特权/沙箱环境下清空系统 DNS 缓存 | 目标解析器状态 | 空缓存 | 与测量原语交替执行,决定时间分辨率 |
| 测量原语集(3 种) | 从原生 / JS / 无脚本 HTML 三种上下文观测解析时延 | 目标域名 | 时延样本 | 决定适用攻击面(是否需要代码执行) |
| 浏览器缓存绕过 | 把浏览器私有缓存挤出,强制走系统缓存 | 1000 个攻击者域 | 系统缓存访问 | 是浏览器场景的前置步骤 |
| 自建 DNS 服务器 | 控制应答(大响应、错误、超时回退) | 查询 | 受控响应 | 支撑"大响应"与"错误回退"两种驱逐原语 |
| 阈值判决器 | 抗网络抖动的 hit/miss 判定 | 每域 10 次测量窗口 | 访问判定 | 输出层;决定 F1 |

### 4.4 公式、算法和机制解释

- **驱逐为何不需要特权**:resolved 中 `resolvectl flush-caches` 本身是非特权操作,但接口在 VM/沙箱/浏览器中不可用;论文因此构造三种"靠合法行为"的替代——填满缓存(依赖固定容量,如 systemd-resolved 4096 条、macOS ≈2000 条)、大响应打洞(依赖公共 DNS 允许的最大应答记录数,Table II:Google 248 / Cloudflare 87 / OpenDNS 83 / Quad9 72 / Yandex 4089 / Verisign 250)、错误回退(利用 resolved 在 SERVFAIL 后切到 fallback DNS 并冲刷缓存,79.8 ms;不支持 EDE 时需等 5 s 超时;systemd ≥256 支持 EDE 错误码后不再切换,该原语失效)。
- **无脚本测量的机制**:不能调用 `performance.now()`,于是用两个 attacker 侧请求**夹住**目标资源请求,在服务器端测量二者到达时差,从而得到目标请求的加载时延(利用浏览器对资源的串行加载)。
- **为什么 CORS 反而帮忙**:浏览器场景下严格 CORS 使预检提前终止请求、不下载内容,减少噪声,使测量更干净(§I)。
- **为什么 DNSSEC 提升攻击效果**:DNSSEC 加大了未命中的解析时延,从而扩大 hit/miss 差距;但 DNSSEC 的正确性并不受影响——攻击读的是**本地缓存状态**,而非传输中的数据。

### 4.5 方法优势

1. **不需要特权**:4 种原语中有 3 种在全部上下文可用(Table III 的 RCE/JS/HTML 三列);
2. **不需要 JS**:纯 HTML + CSS 字体回退即可攻击,覆盖"关掉 JS 的谨慎用户";
3. **跨应用/跨 VM**:同一台主机上任意应用解析过的域名都会进入系统级缓存,可观测面大;
4. **加密无缓解**:DoT/DNSSEC/VPN 均不影响,甚至因时延增大而更准;
5. **时间分辨率高**:每分钟 3 次探测,5 分钟粒度盲区 ≤4.92%。

### 4.6 方法不足

- 依赖具体解析器行为(错误回退原语绑定 systemd-resolved;systemd ≥256 后该原语失效);
- Windows 11 上未找到可用的免 shell 驱逐策略(缓存可达 16 万条、无固定容量);
- macOS 上可驱逐但**不完全可靠**(闭源,存在残留命中);
- 浏览器场景需先绕过浏览器私有 DNS 缓存,且 network state partitioning 会降低准确率;
- 论文自述:防御只能"彻底关闭 DNS 缓存",代价是显著的性能损失与更多的上游信任(§IX)。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

与**网站指纹(WF)**的本质区别:WF 依赖传输内容/长度/方向等网站特征;DMT 只做**一次计时测量**判断"某个具体域名是否在本地缓存中",不依赖传输内容、也不依赖网站特征,因此论文明确声明"DMT does not qualify as a fingerprinting attack",且网站内容变化不影响其可靠性(§I)。与**路由器 DNS 缓存攻击**(Moav et al. / DNS FLaRE)的区别:攻击点不同(本地系统缓存 vs 路由器转发器),本文能攻击到 VM 内部视角、对端到端时延更小、测量更可靠,但不能像路由器场景那样攻击 IoT 设备(§II-C)。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 4 种缓存驱逐原语 | 免特权/跨 VM/JS/无脚本均可触发(Table III) | 高 | 是(适用于其他有固定容量缓存或错误回退机制的解析器) |
| 无脚本测量 | CSS 字体串行加载 + 服务器侧夹逼计时 | 高 | 是(可迁移到任何需要"无 JS 计时"的侧信道) |
| 浏览器 DNS 缓存绕过 | 1000 条长 TTL 攻击者域挤出私有缓存 | 中 | 是 |
| 持续监控循环 | 驱逐 + 单次测量的高分辨率行为时间线 | 高 | 是(把一次性泄漏升级为持续监控是本文的核心叙事) |
| 网络状态分区下的可行性论证 | 证明 partition 后仍可观测系统级缓存 | 中 | 是 |

### 5.3 适用场景

- 受害端为 Linux(systemd-resolved)且攻击者能投放网页(JS 或无 JS 均可)或运行 VM 内代码;
- 隐私敏感目标(使用 VPN/DNSSEC 的用户)仍是有效目标——这些防护不覆盖本地缓存;
- 可用于识别用户使用的具体应用(附录 D 演示了 VSCode 活动与 Copilot 使用检测)。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| Felten & Schneider 2003 经典 DNS 缓存计时 | 首次指出本地 DNS 缓存泄露 | 仅单次、破坏性测量,无驱逐 | 给出可重复的驱逐 + 持续监控 |
| Klein & Pinkas(缓存中做标记追踪) | 可跨浏览器识别用户 | 需主动注入 DNS 记录 | 无需注入,仅观测既有缓存状态 |
| Bushart & Rossow(加密 DNS 被动指纹) | 被动、覆盖 DoT/DoH | 只做分类而非"具体域名是否被访问" | 单域名判定的高精度测量 |
| Moav et al. DNS FLaRE(并发,路由器缓存) | 可覆盖 IoT 设备 | 目标为路由器,需触发上游解析;时延大 | 本地缓存时延更小、测量更可靠(判定正交互补) |
| WF 攻击(如 DF/Var-CNN) | 成熟的特征学习路线 | 依赖内容/长度等网站特征,内容变化影响可靠性 | DMT 不做指纹,内容无关 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **跨 VM 端到端**:宿主(Ubuntu 24.04 LTS,systemd-resolved 255.4-1ubuntu8.8,DNSSEC 关闭)为受害者,libvirt/Debian 12 VM 内跑非特权原生代码为攻击者;
- **JS 端到端**:受害者 Ubuntu 24.04.2 LTS + Chromium 139.0.7258.5(Playwright 注入),攻击者部署自建 DNS 服务器与恶意网站;网络未隔离(存在真实噪声);
- **测量对比**:原生 / JS / JS 50 Mbit/s / JS 300 Mbit/s / 无脚本五种上下文 × DNSSEC 开/关;
- 采样量:每场景 2 万次以上测量(Table I 脚注)。

### 6.2 数据集

| 数据集 | 规模/内容 | 用途 |
|---|---|---|
| 开放世界域列表 | 103 个域(Alexa Top 100 + snee.la 等少量自有域) | 跨 VM 端到端评测 |
| JS 端到端集合 | 10 个网站(amazon / pornhub / reddit / wikipedia 等) | 有无 DNSSEC 的 F1 对比 |
| 3313 个 20 s 时间片 | 连续监控总时长约 18.4 小时 | 持续监控可靠性统计 |

### 6.3 Baseline

消融/对照对象为:官方冲刷命令 `resolvectl flush-caches`(作为"最可靠驱逐"的上界参照)、有无 DNSSEC、不同网络带宽(50 / 300 Mbit/s)、以及有无脚本(JS vs 纯 HTML)。

### 6.4 评价指标

命中/未命中的时延偏差与标准差、误报率(false negatives per measurement)、F1、TP/FN/FP/TN、端到端测量耗时、以及 5 分钟粒度下的盲区比例(blind spot)。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| 测量原语(facebook.com) | 平均时延偏差 | 原生 +DNSSEC 20.663 ms / 无 6.701 ms | JS +DNSSEC 20.356 ms / 无 8.942 ms | — | 原生误报率最低 0.000% / 0.006% |
| 测量原语 | 误报率(FN) | JS +DNSSEC 13.641% | 无脚本 +DNSSEC 12.494%;JS 无 DNSSEC 24.192% | DNSSEC 使 FN 近乎减半 | Table I |
| 跨 VM 端到端(103 域) | F1 | 92.48% | — | — | TP 22999 / FN 3502 / FP 240 / TN 314498;平均 539.78 ms 测完 103 域(10 线程) |
| JS 端到端(10 域) | 宏平均 F1 | 有 DNSSEC 82.86% | 无 DNSSEC 78.89% | +3.97pp | reddit.com 提升最大:86.49%→97.78% |
| 持续监控粒度 | 盲区 | 0.26%(最好) | 4.92%(最差) | — | 5 分钟粒度 |
| 驱逐原语速度 | 驱逐耗时 | 直接冲刷 10.987 ms | 大响应 1.387 s;大量请求 5.109 s | 错误回退 79.1 ms–5 s | Table III |

> ⚠️ MinerU 解析问题:论文 Abstract 与 Table V 报告 JS 端到端 F1 为 82.86%(有 DNSSEC)/78.89%(无 DNSSEC),而 Conclusion(§X)写作 "F1 scores of 95.94 % and 84.93 %";两处数值不一致,疑为结论段笔误或指代另一组(300 Mbit/s)实验,引用时以 Table V 为准并注明分歧。

### 6.6 优势最明显的场景

**原生代码跨 VM 场景**:攻击者只在一个普通 VM 内运行非特权代码,即可在 1 秒内以 F1 92.48% 从 103 个开放世界域名中判定宿主访问了哪些站;本场景下平均驱逐仅 77.267 ms(最快原语),整轮盲区最小(0.26%)。此外,**慢速网络**反而更有利——hit/miss 时延差被拉大。

### 6.7 局限性

- 依赖解析器具体行为:错误回退原语在 systemd ≥256(支持 EDE)后失效;Ubuntu 24.04 LTS 等仍出厂 systemd 255 及以下,因此当前脆弱;
- Windows 11 无可用免 shell 驱逐策略(缓存可增长到 16 万条且无固定容量),仅在原理上仍存在计时差;
- macOS 可驱逐但不完全可靠(≈2000 条,闭源);
- 浏览器场景需要绕过浏览器私有 DNS 缓存,且 network state partitioning 会降低准确率;
- 有 DNS 缓存的上游共享解析器(路由器/ISP)自身也是攻击面,但本文不覆盖该路径。

---

## 7. 学习与应用

### 7.1 是否开源？

解析稿未提及代码或 artifact 发布,亦未见仓库链接。可复现性依赖论文对原语的文字描述(自建 DNS 服务器、Chromium+Playwright、libvirt VM)。

### 7.2 复现关键步骤

1. 搭建受害者主机(Linux + systemd-resolved)与攻击者 VM(libvirt,Debian 12),VM 内跑非特权原生代码;
2. 部署自建 DNS 服务器:用于控制应答大小、返回 SERVFAIL/超时以触发错误回退驱逐;
3. 离线标定每个目标域的 hit/miss 时延直方图与判决阈值;
4. 循环执行"驱逐(选一种原语)→ 对每个域做一次计时测量 → 判决",统计 F1 与盲区。

### 7.3 关键超参数、预处理和训练细节

- 驱逐原语选择:速度与可用性权衡(直接冲刷最快但需 shell;大量请求最慢但全上下文可用);
- 判决窗口:每域保留最近 10 次命中测量的中位数,加网站特定偏移作为阈值(§VII);
- 浏览器缓存绕过:填 1000 条(Chromium)/800 条(Firefox)攻击者控制的长 TTL 域;
- 时间分辨率:每分钟可完成约 3 次"驱逐 + 测量"。

### 7.4 能否迁移到其他任务？

可迁移性主要在**方法学**层面:(1) "把一次性侧信道泄漏升级为持续监控循环"的范式,依赖的是可靠的驱逐原语——该思路可移植到任何有固定容量/替换策略的缓存(CPU cache、CDN cache、DNS over HTTPS 连接池等);(2) 无脚本计时(服务器侧夹逼)可迁移到任何"禁 JS 环境下的时延探测";(3) 判决侧"滑动窗口 + 每目标阈值标定"是抗噪计时的通用做法。

### 7.5 对我的研究有什么启发？

1. **与 WF 的边界值得在综述中写清**:DMT 说明"访问了哪个域名"这一信号可以完全绕开内容/长度特征,只用本地缓存状态获得;它不构成 WF,但构成同一隐私威胁模型下的补充路径——WF 综述的"威胁模型分类"小节可据此增加"本地状态侧信道"一类;
2. **防御讨论的教训**:DNSSEC/DoT/VPN 都是"传输层保护",对本地状态侧信道零作用,甚至因时延增大而放大信号。这提醒我们在评估 WF 防御时,应区分"保护传输"与"保护本地可观测状态";
3. **盲区量化**是评价持续监控类攻击的好指标(比单次准确率更贴近真实威胁),值得在实验设计中借用。

---

## 8. 总结

### 8.1 核心思想

> 靠合法缓存行为驱逐 DNS 缓存,把一次性泄漏变成持续监控。

### 8.2 速记版 Pipeline

1. 目标:本地系统级 DNS 缓存(systemd-resolved);
2. 驱逐:4 种原语(直接冲刷 / 大量请求 / 大响应 / 错误回退),覆盖原生、VM、JS、无 JS;
3. 绕缓存:填满浏览器私有 DNS 缓存(1000 / 800 条)使解析下沉到系统缓存;
4. 测量:原生 `gethostbyname` / JS `fetch`(CORS 预检降噪)/ 无脚本 CSS 字体串行加载夹逼计时;
5. 判决:每域滑动窗口中位数 + 偏移作阈值,循环实现每分钟 3 次探测,5 分钟盲区 ≤4.92%。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]]:论文把 WF 作为对照系(§I、§II-B 大量比较),同时**明确声明 DMT 本身不属于 fingerprinting**(不依赖内容/网站特征),故此处仅为"相关工作概念",聚合时不应把本文计入 WF 攻击统计。

### 9.2 相关方法

- 白名单方法页均为机器学习方法(contrastive-learning / transformer 等),本文为缓存侧信道测量与驱逐原语设计,无对应,故不链接。

### 9.3 相关任务

- 白名单任务页(anomaly-detection / app-fingerprinting / encrypted-traffic-detection / malicious-traffic-detection / traffic-classification / traffic-representation / tunnel-detection / website-fingerprinting)均不对应本文的"缓存计时测量"任务,故不链接。

### 9.4 可更新的综述页面

- [[survey-website-fingerprinting]]:可在其"威胁模型 / 非 WF 的替代监控路径"部分补一条:本地 DNS 缓存侧信道可在不依赖网站特征的前提下判定具体域名访问(F1 92.48%,103 域开放世界),且 DNSSEC/DoT/VPN 不缓解。

### 9.5 可加入的对比表

- 无(本文未提出可对比的流量分析方法,也不涉及新数据集发布或开源代码)

### 9.6 相关论文笔记(KB 已有)

- [[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]](参考文献 [91],作为 WF 攻击代表作被引)
- [[2023-CCS-Realistic_Website_Fingerprinting_by_Augmenting_Network_Traces]](参考文献 [9],Bahramali et al.)
- [[2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild]](参考文献 [22],Deng et al.)
- [[2023-CCS-Transformer-based_Model_for_Multi-tab_Website_Fingerprinting_Attack]](参考文献 [44],Jin et al.)

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 论文明确声明 DMT **不是**指纹攻击(不依赖传输内容/网站特征) | "DMT does not qualify as a fingerprinting attack. Changes to the target website's content do not affect the attack's reliability." | §I |
| 4 种驱逐原语覆盖全部上下文,3 种在 RCE/JS/HTML 均可用 | Table III:Direct Flushing(仅 RCE,10.987 ms)/ Many Requests(5.109 s)/ Large Response(1.387 s)/ Error-Based(79.1 ms–5 s) | §IV, Table III |
| DNSSEC 提升攻击可靠性,而非缓解 | FN 从 24.192%(无 DNSSEC)降至 13.641%(有 DNSSEC);端到端 F1 78.89%→82.86% | Table I, Table V |
| 跨 VM 开放世界攻击在 1 秒内达到 F1 92.48% | TP 22999 / FN 3502 / FP 240 / TN 314498;103 域平均 539.78 ms(10 线程) | Table IV |
| 无 JS 场景同样可行,可靠性最高 87.5% | 利用 CSS 字体串行加载,两端夹逼计时 | Abstract, §V |
| 浏览器私有 DNS 缓存可被挤占绕过 | Chromium 1000 条 / Firefox 800 条默认容量 | §VI-E |
| 公共 DNS 的最大应答记录数差异很大(72–4089) | Google 248 / Cloudflare 87 / OpenDNS 83 / Quad9 72 / Yandex 4089 / Verisign 250 | Table II |
| 5 分钟粒度盲区 0.26%–4.92% | 论文给出的最好/最差情形 | Abstract, §X |
| 四个厂商均确认问题但未实施缓解 | systemd 2025-10-11、Chromium/Mozilla 2025-10-15、Apple 2025-11-18 | §IX(Responsible Disclosure) |
| Windows 11 无可用免 shell 驱逐策略,但仍有时延差 | 缓存报告可达 160 000 条、无固定容量 | §IV-C |

---

## 11. 原始资料链接

- PDF:00-inbox/PDFs/2026-NDSS-Continuous_User_Behavior_Monitoring_using_DNS_Cache_Timing_Attacks.pdf
- MinerU Markdown:02-parsed-markdown/2026-NDSS-Continuous_User_Behavior_Monitoring_using_DNS_Cache_Timing_Attacks.md

---

## 12. 后续问题

- Abstract/Table V(82.86% / 78.89%)与 Conclusion(95.94% / 84.93%)的 JS F1 数值分歧需对照原文 PDF 核实;
- 论文未给出代码/artifact,驱逐原语的工程细节(自建 DNS 服务器实现、阈值标定脚本)无法直接复用;
- "每分钟 3 次探测"与"5 分钟盲区 ≤4.92%"之间的推导关系(单次迭代耗时分布)未在解析稿中展开;
- 与 KB 主题的关系:本文不属 WF/流量分类,但为 WF 综述的"威胁模型"小节提供了新类别,聚合时建议按"相邻威胁模型"处理而非计入 WF 攻击;
- 若后续要复现,需先确认目标环境 systemd 版本(<256 才有错误回退原语)。

---

## 13. 写作叙事与故事线分析

> 本文为 NDSS 2026（CCF A）论文，补充方法论与叙事分析。

### 13.1 论文主线故事线

论文先从 DNS 缓存命中与未命中之间稳定的时延差出发，指出已有工作只能做破坏性、低时间分辨率的单次判断。关键转折是把“无法驱逐”转化为一个可工程化的系统问题，并设计覆盖原生代码、跨 VM、JavaScript 与无脚本浏览器的四类驱逐原语。随后，测量微基准先证明缓存状态可分离，跨 VM 与浏览器端到端实验再证明持续监控可行。最后，论文把 DNSSEC、DoT、VPN、浏览器缓存和不同解析器行为纳入讨论，收束到“传输层加密不等于本地缓存隐私”的结论。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 问题、四类原语与端到端数字结果的压缩预告 | 让读者先看到威胁可行性与量级 | “continuous monitoring”与 103 域 F1 结果同时出现 |
| Introduction | 从 DNS 普及和缓存侧信道引出持续监控缺口 | 定义“读缓存会破坏缓存”这一核心矛盾 | 将一次性 timing test 提升为 Evict+Reload 循环 |
| Concurrent Work / Background | 区分本地系统缓存、路由器转发器和 WF | 划定攻击对象与相关工作边界 | 明确 DMT 不依赖网站内容，不能直接归为 WF |
| Threat Model / Overview | 把攻击者能力、目标缓存和测量循环具体化 | 使问题可验证、可复现 | “驱逐→测量→判决”成为全文统一抽象 |
| Measurement | 先验证命中/未命中时延差，再处理 JS、无脚本和网络噪声 | 建立侧信道存在性与可分性证据 | DNSSEC 增大时延差，反而提高可测性 |
| Eviction | 系统化比较四种驱逐原语及其环境依赖 | 回答“如何持续测量”这一方法核心 | 大响应与错误回退把无特权场景纳入 |
| End-to-end | 用开放世界跨 VM 与浏览器实验验证实用性 | 从微基准过渡到真实行为监控 | F1、盲区和每轮耗时共同量化部署价值 |
| Discussion / Conclusion | 讨论解析器版本、浏览器分区和防御代价 | 收回威胁边界并给出缓解方向 | 关闭缓存有效但会牺牲性能与上游信任 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 能力缺口 | 既有 DNS cache timing 只能判断“最近是否访问”，缺少可靠驱逐，无法持续监控 | 机制缺陷 + 时间分辨率后果 | §I, §IV-B |
| 执行环境缺口 | 既有方案依赖原生代码、Java 或 JavaScript，沙箱和禁脚本环境覆盖不足 | 场景缺失 + 攻击面比较 | §I, §IV-C |
| 防护边界缺口 | DoT、DNSSEC 与 VPN 保护传输或上游路径，却不覆盖本地系统缓存 | 防护对象错位 | §II-C, §VIII, §IX |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 时延测量微基准 | 先建立 cached/uncached 可分离性，并量化网络噪声 | 证明侧信道存在且可观测 |
| 驱逐原语比较 | 对比速度、适用上下文与解析器依赖 | 证明持续测量的工程支点 |
| 跨 VM 开放世界主实验 | 103 域、F1、测量时间和盲区联合报告 | 直接回答“能否持续监控” |
| JS / 无脚本 / DNSSEC 泛化实验 | 改变执行权限、脚本能力与传输配置 | 证明结论不局限于单一环境 |
| 限制与负面结果 | 报告 systemd ≥256、Windows、macOS 和浏览器分区限制 | 把适用边界写进主线，而不是只报告最佳数字 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 用日常基础设施（DNS）和隐私后果快速落到一个可观测时延差 | “普遍组件→具体侧信道→可验证缺口”三步收窄问题 |
| Gap 提出方式 | 把“读取会破坏状态”写成持续监控无法成立的因果瓶颈 | 用一个机制级矛盾承载研究空白，避免只罗列相关工作 |
| 方法论证逻辑 | 先建立测量基线，再逐个解释驱逐原语的环境与代价 | 每个系统组件先回答“为什么需要”，再说明“怎样实现” |
| 实验组织逻辑 | 微基准→驱逐比较→端到端→跨环境鲁棒性 | 从可分性、可执行性到可部署性逐级推进 |
| 局限性讨论方式 | 明确列出失效系统版本、浏览器缓存和噪声来源 | 把环境依赖与负面结果写成可复现的边界条件 |
| 最值得借鉴的结构 | “测量是破坏性的，因此需要驱逐；驱逐后才能提高时间分辨率” | 用一条短因果链把动机、机制和指标串成闭环 |

## 14. 深度分析证据边界与知识层联动建议

- 本次深度分析直接依据 `02-parsed-markdown/2026-NDSS-Continuous_User_Behavior_Monitoring_using_DNS_Cache_Timing_Attacks.md` 的 §§I–X、Tables I–V 和 Appendix；原始 PDF 与解析稿均已保留。结论段的 JS F1 数值与 Abstract/Table V 不一致，笔记以 Table V 为主，并保留该冲突供 PDF 复核。
- 可向 `07-surveys/survey-website-fingerprinting.md` 提交一条“本地 DNS 缓存侧信道”相邻威胁模型记录，但应标注为非 WF、非流量分类方法，不计入 WF 攻击方法统计。
- 当前未修改 `04-concepts/`、`05-methods/`、`06-tasks/`、`07-surveys/` 或 `08-comparisons/` 共享页面；上述联动仅作为后续总审计建议。

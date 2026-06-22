---
type: paper
title_original: "LZR: Identifying Unexpected Internet Services"
title_cn: "LZR：识别非预期互联网服务"
authors: ["Liz Izhikevich", "Renata Teixeira", "Zakir Durumeric"]
year: 2021
venue: "USENIX Security 2021"
doi: unknown
url: "https://www.usenix.org/conference/usenixsecurity21/presentation/izhikevich"
pdf: "00-inbox/PDFs/2021-USENIX-LZR__Identifying_Unexpected_Internet_Services.md"
mineru_md: "02-parsed-markdown/2021-USENIX-LZR__Identifying_Unexpected_Internet_Services.md"
status: processed
reading_level: L3
research_area: ["internet-wide scanning", "service discovery", "network measurement", "middlebox detection"]
task: ["service identification", "port scanning optimization", "unexpected service detection"]
method: ["TCP state inference", "protocol fingerprinting", "greedy handshake ordering", "middlebox behavior analysis"]
dataset: ["1% IPv4 random sample", "0.1% IPv4 all-ports scan", "100% IPv4 scan (June 2020)"]
code: "https://github.com/stanford-esrg/lzr"
relevance: high
created: "2026-06-21"
updated: "2026-06-21"
---

# LZR: Identifying Unexpected Internet Services

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | LZR: Identifying Unexpected Internet Services |
| 中文标题 | LZR：识别非预期互联网服务 |
| 作者 | Liz Izhikevich (Stanford), Renata Teixeira (Inria), Zakir Durumeric (Stanford) |
| 年份 | 2021 |
| 会议/期刊 | 30th USENIX Security Symposium |
| 研究方向 | 全网扫描、服务发现、中间件行为分析、[[tunnel-detection]] |
| 任务类型 | 识别非预期端口上的互联网服务，过滤伪服务，加速应用层扫描 |
| 方法关键词 | TCP 状态推断、协议指纹识别、贪婪握手排序、中间件保护行为分类 |
| 数据集 | 1% IPv4 随机样本（37 IANA 端口 + 2000 随机端口）、0.1% IPv4 全端口扫描、100% IPv4 扫描（2020 年 6 月） |
| 是否开源 | 是（Apache 2.0） |
| PDF | 00-inbox/PDFs/2021-USENIX-LZR__Identifying_Unexpected_Internet_Services.md |
| MinerU Markdown | 02-parsed-markdown/2021-USENIX-LZR__Identifying_Unexpected_Internet_Services.md |

## 1. 一句话总结

> 通过对 IPv4 全网的系统性测量，揭示协议部署远比预期分散（仅 3% HTTP 和 6% TLS 在其 IANA 指定端口上），中间件和防火墙导致大量 SYN-ACK 伪服务，并提出 LZR 系统以 5 次握手识别 99% 可识别的非预期服务，在 MongoDB 端口上实现 55 倍扫描加速。

## 2. 摘要翻译

### 2.1 摘要原文

Internet-wide scanning is a commonly used research technique that has helped uncover real-world attacks, find cryptographic weaknesses, and understand both operator and miscreant behavior. Studies that employ scanning have largely assumed that services are hosted on their IANA-assigned ports, overlooking the study of services on unusual ports. In this work, we investigate where Internet services are deployed in practice and evaluate the security posture of services on unexpected ports. We show protocol deployment is more diffuse than previously believed and that protocols run on many additional ports beyond their primary IANA-assigned port. For example, only 3% of HTTP and 6% of TLS services run on ports 80 and 443, respectively. Services on non-standard ports are more likely to be insecure, which results in studies dramatically underestimating the security posture of Internet hosts. Building on our observations, we introduce LZR ("Laser"), a system that identifies 99% of identifiable unexpected services in five handshakes and dramatically reduces the time needed to perform application-layer scans on ports with few responsive expected services (e.g., 5500% speedup on 27017/MongoDB). We conclude with recommendations for future studies.

### 2.2 摘要中文翻译

全网扫描是一种常用的研究技术，已帮助发现现实世界的攻击、密码学弱点以及理解运营商和恶意行为者的行为。采用扫描的研究大多假设服务运行在其 IANA 指定的端口上，忽略了对非预期端口上服务的研究。在本文中，我们调查了互联网服务在实践中的部署位置，并评估了非预期端口上服务的安全态势。我们发现协议部署比先前认为的更加分散，协议运行在其主要 IANA 指定端口之外的许多额外端口上。例如，仅 3% 的 HTTP 和 6% 的 TLS 服务分别运行在端口 80 和 443 上。非标准端口上的服务更可能是不安全的，这导致研究严重低估了互联网主机的安全态势。基于我们的观察，我们引入了 LZR（"Laser"），一个能在五次握手中识别 99% 可识别非预期服务的系统，并大幅减少了在预期服务较少的端口上执行应用层扫描所需的时间（例如在 27017/MongoDB 上实现 5500% 的加速）。我们最后给出了对未来研究的建议。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？（三大核心问题）

本文的动机源于全网扫描研究中长期存在但未被系统审视的三个核心问题：

**问题 1 — L4 与 L7 存活率的巨大差距**：过去 300+ 篇使用全网扫描的研究发现，大量响应 SYN 扫描的主机从未完成应用层握手（如 [24, 26, 36, 51, 67]），但从未系统调查原因。这一差距从 14%（端口 80）到 96%（端口 102）不等，严重影响扫描结果的准确性。

**问题 2 — 协议部署的分散性被低估**：现有研究假设服务运行在 IANA 指定端口上（如 HTTPS 在 443），但实际上仅 3% 的 HTTP 在端口 80，6% 的 TLS 在端口 443。达到 90% TLS 覆盖率需要扫描 4 万个端口。这种分散性意味着大量服务和安全问题被系统性遗漏。

**问题 3 — 非预期端口服务的安全隐患被忽视**：IoT 设备频繁在非标准端口上托管不安全服务（如弱 TLS 证书、非公钥 SSH 认证），但现有安全研究仅关注标准端口，导致对互联网安全态势的严重低估。

### 3.2 现有方法的痛点和不足

| 现有方法/问题 | 痛点 | 影响范围 |
|---|---|---|
| 两阶段扫描（ZMap + ZGrab） | SYN-ACK 不能指示 L7 服务存在，40% 的 SYN-ACK 主机不确认数据 | 所有使用 ZMap 的研究（300+ 篇） |
| 仅扫描 IANA 指定端口 | 97% HTTP 和 93% TLS 不在指定端口上 | TLS/SSH/Web PKI 安全研究 |
| 忽略中间件行为 | 零窗口 DDoS 保护、连接回避、动态阻断等行为被误认为"无服务" | 端口扫描结果准确性 |
| 缺少非预期服务识别 | 30 个协议扫描器逐一尝试过于侵入且缓慢 | 大规模非预期服务发现 |
| 安全评估仅限标准端口 | 非标准端口 TLS 证书已知私钥概率高 1.17 倍，SSH 非公钥认证概率高 15% | IoT 安全、密码学弱点研究 |

### 3.3 论文的研究假设或核心直觉

**核心假设 1**：大量 SYN-ACK 响应不对应真实 L7 服务，而是中间件和防火墙的保护行为所致，可通过 TCP 状态推断进行分类和过滤。

**核心假设 2**：协议在其 IANA 指定端口之外广泛部署，非预期端口上的服务可通过少量精心排序的握手高效识别。

**核心假设 3**：非预期端口上的服务具有更弱的安全态势（更多 IoT 设备、更弱的 TLS/SSH 配置），对安全研究具有重要意义。

**研究问题**：
- RQ1：L4 响应（SYN-ACK）与 L7 存活之间差距的原因是什么？
- RQ2：互联网协议在实践中的部署分布如何？
- RQ3：非预期端口上的服务安全态势如何？
- RQ4：如何高效识别非预期服务？

## 4. 方法设计

### 4.1 方法整体流程

1. **L4 vs L7 存活分析**：在 37 个 IANA 端口上对 1% IPv4 样本进行两阶段扫描，量化 SYN-ACK 与 L7 握手完成之间的差距
2. **TCP 状态推断**：开发基于 RFC 793 的修改版 TCP 状态机，引入"接受数据"和"确认数据"两个新状态，系统分类 5 种中间件保护行为
3. **非预期服务发现**：在 55 个端口上使用 30 个 ZGrab 协议扫描器，识别运行非预期协议的服务
4. **协议部署长尾分析**：对 10 个流行协议在全部 65,535 端口上进行 0.1% IPv4 扫描，量化协议覆盖所需的端口数
5. **LZR 系统设计与实现**：基于上述发现设计高效的非预期服务识别系统
6. **全面评估**：在 100% IPv4 扫描上评估 LZR 的准确性和性能

### 4.2 详细 Pipeline（表格形式）

| 步骤 | 描述 | 技术细节 |
|---|---|---|
| 1. 两阶段扫描 | ZMap 发送 SYN，ZGrab 完成 L7 握手 | 37 个 IANA 端口，1% IPv4 随机样本，2019 年 11 月 12-14 日 |
| 2. 连接回避检测 | 从两个 IP 地址连接同一主机 | 70% 的"消失"主机对新 IP 有响应，证实为连接回避而非网络故障 |
| 3. TCP 状态推断 | 发送 "\n\n" 并观察服务器响应 | Algorithm 1：发送 SYN → 检查窗口大小 → 发送数据 → 等待 ACK/RST/超时 → 返回状态 |
| 4. 零窗口 DDoS 检测 | 检查 SYN-ACK 窗口大小 | 99.94% 的零窗口主机永远不会增大窗口；99% 在所有端口上表现一致 |
| 5. 连接中断检测 | 观察 SYN-ACK 重传 | 平均 7.8 次 SYN-ACK 重传，ISP 保护消费设备的行为 |
| 6. 连接重置检测 | 观察三路握手后的 RST | 73% 热门端口、34% 冷门端口的不确认数据主机在握手后重置 |
| 7. 动态阻断检测 | 从两个 IP 同时尝试 L7 握手 | 98% 的不响应主机对新 IP 有响应，确认为动态阻断 |
| 8. 数据确认防火墙过滤 | 检查 5 个随机临时端口 | F5 Big-IP 防火墙在几乎所有端口上响应，过滤 99.9% |
| 9. 非预期服务识别 | 在 55 个端口上尝试 30 个协议握手 | 先尝试预期协议，失败后逐一尝试其他协议 |
| 10. 协议覆盖分析 | 10 个协议 × 65,535 端口 | 0.1% IPv4 扫描，计算累积覆盖率 |
| 11. LZR 实现 | 3,500 行 Go 代码 | 使用 libpcap 发送/接收原始以太网帧，无需完整 TCP/IP 栈 |
| 12. 全网评估 | 100% IPv4 扫描 | 2020 年 6 月，比较 LZR 与 ZGrab 的准确性和性能 |

### 4.2.1 TCP 状态推断模型（Figure 2）

论文基于 RFC 793 设计了修改版的客户端视角 TCP 状态机：

| 状态 | 含义 | 检测方法 |
|---|---|---|
| LISTEN | 服务器监听 | - |
| SYN RECEIVED | 服务器发送 SYN-ACK | ZMap 探测 |
| ESTABLISHED | 三路握手完成 | 客户端发送 ACK |
| **ACCEPTS DATA** | 服务器窗口 > 0，可接收数据 | 检查 SYN-ACK 窗口大小 |
| **ACKNOWLEDGES DATA** | 服务器确认接收数据 | 发送 "\n\n"，等待 ACK |

**关键创新**：引入 ACCEPTS DATA 和 ACKNOWLEDGES DATA 两个新状态，因为 ESTABLISHED 状态不保证能交换数据（零窗口情况）。

### 4.2.2 五种中间件保护行为分类（Table 3b, Figure 4）

| 保护行为 | 机制 | 占比（热门端口） | 占比（冷门端口） | 网络粒度 | 代表案例 |
|---|---|---|---|---|---|
| **连接回避 (Connection Shunning)** | 首次扫描后封锁源 IP | 1.6% | 5% | 40% /32（主机级），10% > /24 | Alestra Net (/20, ASN 11172) |
| **零窗口 DDoS 保护** | SYN-ACK 窗口为 0，永不增大 | 13% | 26% | 90% > /24（网络级） | Florida DMS (ASN 8103, 16% 全网零窗口) |
| **连接中断 (Mid-Handshake Drop)** | 发 SYN-ACK 后不完成握手 | 2% | - | ISP 级 | CenturyLink, Frontier, MCI (端口 4567)；KT, Axtel (端口 7547) |
| **连接重置 (Reset Connection)** | 握手完成后立即 RST | 73% | 34% | 主机级为主 | DenyHosts, Cisco IOS 威胁检测；KT, Vodafone AU, OVH, Akamai |
| **动态阻断 (Dynamic Blocking)** | 握手后不确认数据并封锁 | 10% | 18% | 网络级 | 中国 GFW [18]；Coming ABCDE HK (ASN 133201, 48%) |

### 4.3 LZR 系统架构（Section 5）

| 模块 | 功能 | 输入 | 输出 |
|---|---|---|---|
| SYN-ACK 过滤器 | 过滤零窗口和不确认数据的主机 | ZMap SYN-ACK 流 | 有效主机列表 |
| ACK+数据发送器 | 在 ACK 中携带协议握手数据 | 有效主机 + 协议握手模板 | 主机响应数据 |
| 协议指纹引擎 | 匹配服务器响应与已知协议签名 | 服务器响应数据 | 协议标识 / 未知 |
| 连接管理器 | 管理 TCP 连接状态和重传 | 连接事件 | 连接决策（继续/放弃/重试） |
| 临时端口过滤器 | 检测全端口响应的防火墙 | 随机临时端口 SYN-ACK | 过滤标志 |

**LZR 扫描算法（Figure 12）**：
1. 接收 ZMap 的 SYN-ACK 流或 (IP, port) 列表
2. 过滤零窗口主机
3. 发送 ACK + 预期协议握手数据
4. 如果收到数据 → 指纹识别并关闭连接
5. 如果主机不确认数据 → 标记为无服务，不再尝试
6. 如果确认但无响应 → 关闭连接，发送下一个握手
7. 重复直到识别协议或用尽握手

**关键设计决策**：
- 使用 libpcap 而非 OS TCP/IP 栈，允许单个 socket 扫描全网
- 仅需单个包即可指纹识别服务，无需完整 TCP 栈
- "fail-fast" 策略：快速过滤不确认数据的主机
- "fingerprint everything" 策略：监听服务器主动发送的数据

### 4.4 协议发现优化（Section 4）

**最优握手顺序（Table 2）**：

| 排序 | IANA 端口 | 增量覆盖 | 临时端口 | 增量覆盖 |
|---|---|---|---|---|
| 1 | wait（等待服务器先发） | 51.3% | wait | 66.3% |
| 2 | TLS Client Hello | 29.0% | HTTP GET | 17.1% |
| 3 | HTTP GET | 13.6% | TLS Client Hello | 15.9% |
| 4 | DNS | 3.4% | Oracle DB | 0.23% |
| 5 | PPTP | 1.8% | PPTP | 0.14% |

**关键发现**：
- 5 次握手可识别 99% 的可识别非预期服务
- 8/30 个协议是"服务器优先"（POP3, IMAP, MySQL, FTP, VNC, SSH, Telnet, SMTP）
- 16/30 个协议在收到 HTTP GET 或 TLS Client Hello 后会响应可指纹数据
- 75% 的二进制协议（MQTT, Postgres, PPTP 等）不响应错误握手

### 4.5 方法优势

1. **系统性**：首次系统调查 L4-L7 存活差距的原因，覆盖 37 个 IANA 端口和 2000 个随机端口
2. **实用性**：LZR 开源（Apache 2.0），可直接集成到 ZMap/ZGrab 工作流
3. **高效性**：单包识别 88% 可识别服务，5 次握手识别 99%，MongoDB 端口 55 倍加速
4. **全面性**：同时识别预期和非预期服务，比 ZGrab 多发现 31% 的服务
5. **方法论贡献**：TCP 状态推断框架可推广到其他网络测量场景

### 4.6 方法不足

1. **协议覆盖偏差**：30 个 ZGrab 扫描器偏向 ASCII 协议，二进制协议（如 MQTT, Postgres）可能被低估
2. **握手参数敏感性**：L7 过滤（如 PPTP Magic Cookie、TLS 密码套件）可能导致服务遗漏
3. **连续握手影响**：发送错误握手可能导致 17-30% 的后续握手失败（类似 Cisco Login Block）
4. **扫描侵入性**：100% IPv4 扫描收到 7 个组织投诉，大规模使用需谨慎
5. **时间局限**：数据采集于 2019-2020 年，协议部署格局可能已变化
6. **端口选择偏差**：37 个 IANA 端口基于 ZGrab 可用性选择，可能不完全代表所有服务

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 对比维度 | 传统两阶段扫描 | LZR 方法 |
|---|---|---|
| 服务发现假设 | SYN-ACK = 服务存在 | SYN-ACK ≠ 服务存在，需进一步验证 |
| 端口覆盖 | 仅 IANA 指定端口 | 所有端口，重点关注非预期部署 |
| 伪服务处理 | 未区分真实服务和中间件响应 | 系统分类 5 种中间件行为并过滤 |
| 协议识别 | 仅尝试预期协议 | 30 个协议扫描器 + 交叉指纹 |
| 性能优化 | 无专门优化 | "fail-fast" + "fingerprint everything" |
| 输出 | 仅预期协议主机 | 预期 + 非预期协议主机 |

### 5.2 创新点分析（表格形式）

| 创新点 | 说明 |
|---|---|
| TCP 状态推断框架 | 引入 ACCEPTS DATA 和 ACKNOWLEDGES DATA 两个新状态，系统分类 L4-L7 差距原因 |
| 中间件行为分类 | 首次系统量化 5 种中间件保护行为的部署规模和网络粒度 |
| 协议部署长尾分析 | 首次在 65,535 端口上量化 10 个协议的覆盖分布 |
| 最优握手排序 | 贪婪算法计算 5 次握手覆盖 99% 可识别非预期服务 |
| LZR 系统 | 单包指纹 + fail-fast 过滤，实现 55 倍扫描加速 |
| 数据确认防火墙过滤 | 通过 5 个随机临时端口检测 F5 Big-IP 类防火墙（99.9% 过滤率） |

### 5.3 与相关工作的定位对比

| 工作 | 研究问题 | 方法 | 本文区别 |
|---|---|---|---|
| ZMap [26] | 快速全网扫描 | 无状态 SYN 扫描 | LZR 解决 ZMap 无法完成 L7 握手的问题 |
| ZGrab [21] | 应用层握手 | 有状态 L7 扫描 | LZR 比 ZGrab 快 1.9-55 倍 |
| Degreaser [8] | 识别 tarpits | 单一行为检测 | LZR 系统分类 5 种行为 |
| Bano et al. [12] | 主机存活 | 端口相关性分析 | LZR 深入分析 L4-L7 差距原因 |
| Clayton et al. [18] | GFW 动态阻断 | 单一行为观察 | LZR 量化动态阻断的全球部署规模 |

### 5.4 LZR 性能对比（Table 4 摘选）

| 端口 | 协议 | SYN-ACK | ACKs Data | LZR 预期 | LZR 非预期 | ZMap/LZR 加速 | Offline LZR 加速 |
|---|---|---|---|---|---|---|---|
| 80 | HTTP | 62.6M | 55M | 54.66M | 238K (18 协议) | 3.3x | 4.1x |
| 443 | TLS | 51.8M | 45M | 43.7M | 1.3M (16 协议) | 4.7x | 4.1x |
| 27017 | MongoDB | 2.4M | 505K | 73.3K | 23K (14 协议) | 1.6x | **55x** |
| 62220 | HTTP | 2.6M | 628K | 38K | 23K (12 协议) | 2.7x | 25.3x |
| 5672 | AMQP | 3.5M | 1.4M | 123K | 260K (11 协议) | 1.9x | 11.4x |

**关键发现**：
- LZR 发现的非预期服务数量可超过预期服务（如 5672/AMQP 上 260K > 123K）
- 在低命中率端口（如 27017/MongoDB），LZR 加速效果最显著（55 倍）
- LZR 与 ZGrab 的 KS 检验 p > 0.05，确认两者发现的服务无统计显著差异

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **扫描规模**：1% IPv4（端口实验）、0.1% IPv4（全端口实验）、100% IPv4（LZR 评估，2020 年 6 月）
- **端口选择**：37 个 IANA 端口（有 ZGrab 扫描器）+ 2000 个随机端口 + 5 个临时端口
- **协议扫描器**：30 个 ZGrab 实现的唯一协议
- **评估指标**：服务发现数量、扫描速度（CPU 周期/秒）、带宽节省、KS 检验
- **伦理考虑**：遵循 Durumeric et al. [26] 最佳实践，排除曾请求移除的网络

### 6.2 协议部署分布（Section 3.2）

| 协议 | IANA 端口占比 | 达到 90% 覆盖需扫描端口数 | 是否出现在所有端口 |
|---|---|---|---|
| HTTP | 3.0% (端口 80) | 25,000 | 是 |
| TLS | 6.4% (端口 443) | 40,000 | 是 |
| SSH | 大量在非标准端口 | - | 否 |
| Telnet | 5.5% (端口 23) | - | 否 |
| AMQP | 83.1% (端口 5672) | 2 | 否 |
| FTP | 大量在非标准端口 | - | 否 |

**Telnet 端口分布（Table 1）**：

| 端口 | 主机数 | 最大 AS | 该 AS 占比 |
|---|---|---|---|
| 23 | 2,606 | Telecom Argentina (10318) | 8.7% |
| 5523 | 521 | Claro S.A (28573) | 87% |
| 9002 | 396 | Fastweb Italia (12874) | 4% |
| 6002 | 232 | Fastweb Italia (12874) | 6% |
| 8000 | 158 | Powercomm KR (17858) | 89% |

### 6.3 非预期服务安全态势（Section 3.3）

| 安全维度 | 标准端口 | 非预期端口 | 差异 |
|---|---|---|---|
| TLS 已知私钥证书 | 基准 | 高 1.17 倍 | 非预期端口 TLS 更不安全 |
| SSH 非公钥认证 | 基准 | 高 15% | 更多密码/主机认证 |
| SSH 仅公钥认证 | 26% | 11% | 低 2.4 倍 |
| IoT 设备 TLS | 基准 | 高 5 倍 | 50% 非预期端口 TLS 属于 IoT |
| IoT 设备 SSH | 基准 | 高 2 倍 | 更多 Dropbear/Cisco/Huawei |
| 登录页面比例 | 端口 80 基准 | 8080 高 2.4 倍 | 更多暴露的管理界面 |

**IoT 设备分布示例**：
- 8000/TLS：35% 为韩国 KT 的 icctv 监控摄像头
- 80/TLS：38% 为华为网络设备，分布在 1% 国际网络中
- 8443/TLS：5% 为韩国网络的 Android TV，20%+ 为路由器
- 49152：12 倍于端口 80 的 TCP/UPnP 设备（拉丁美洲和亚洲电信）

### 6.4 中间件保护效果评估（Section 2.8）

| 保护行为 | 部署 AS 占比 | 扫描减速效果 | 多 IP 绕过可行性 |
|---|---|---|---|
| 连接重置 | 34% | 可忽略（~100ms） | 不适用（握手后行为） |
| 连接回避 | 6% | 与动态阻断相同 | 可绕过（多源 IP） |
| 动态阻断 | 6% | 最高 55 倍（MongoDB） | 可绕过（多源 IP） |
| 零窗口 | 2% | 中等（最终超时） | 容易过滤 |
| 连接中断 | ISP 级 | 中等 | 不适用 |

### 6.5 LZR 扫描速度与带宽节省

**速度提升（100% IPv4 扫描）**：

| 配置 | 80/HTTP | 443/TLS | 27017/Mongo | 62220/HTTP |
|---|---|---|---|---|
| ZMap/LZR vs ZGrab | 3.3x | 4.7x | 1.6x | 2.7x |
| Offline ZMap/LZR vs ZGrab | 4.1x | 4.1x | **55x** | 25.3x |
| Offline ZMap/LZR+ZGrab vs ZGrab | 1.1x | 1.1x | 7x | 5.4x |

**带宽节省**：

| 配置 | 80/HTTP | 443/TLS | 27017/Mongo | 62220/HTTP |
|---|---|---|---|---|
| ZMap/LZR | 60% | 75% | 66% | 68% |
| Offline ZMap/LZR | 49% | 60% | 87% | 85% |

### 6.6 优势最明显的场景

- **低命中率端口**：27017/MongoDB 上 21% 的 SYN-ACK 主机确认数据，LZR 实现 55 倍加速
- **非预期服务发现**：单次 HTTP 握手识别 88% 可识别服务，发现 12+ 个额外协议
- **中间件过滤**：40% 的路由 AS 包含至少一种中间件保护，LZR 可高效过滤
- **IoT 安全评估**：非预期端口上 50% TLS 属于 IoT 设备，证书安全显著更差

### 6.7 局限性

1. **二进制协议覆盖不足**：75% 二进制协议不响应错误握手，需专门扫描器
2. **握手参数敏感性**：PPTP Magic Cookie 错误导致 67.1% 无响应，TLS 密码套件不匹配导致 2.65% 无响应
3. **连续握手退化**：发送错误握手后 17-30% 后续握手失败，需等待 5 秒-2 分钟恢复
4. **大规模扫描投诉**：100% IPv4 扫描收到 7 个组织投诉
5. **数据确认防火墙误报**：F5 Big-IP 类防火墙在几乎所有端口响应，需额外过滤步骤

## 7. 学习与应用

### 7.1 是否开源？

是。LZR 以 Apache 2.0 许可证发布：
- 代码仓库：https://github.com/stanford-esrg/lzr
- 指纹签名：https://github.com/stanford-esrg/lzr/tree/master/handshakes
- 语言：Go（3,500 行）
- 依赖：libpcap（原始以太网帧收发）

### 7.2 复现关键步骤

1. **环境准备**：安装 Go 和 libpcap，配置 iptables 规则防止内核发送 RST
2. **ZMap 扫描**：使用 ZMap 进行 SYN 扫描获取 SYN-ACK 流
3. **LZR 运行**：`lzr -handshakes <protocol_list>` 接收 ZMap 输出或直接指定 IP/port 列表
4. **协议选择**：根据目标选择握手协议（推荐：wait → TLS → HTTP → DNS → PPTP）
5. **结果分析**：LZR 输出协议标识和过滤结果

### 7.3 关键超参数和配置

| 参数 | 值/说明 |
|---|---|
| 临时端口过滤数量 | 用户指定的随机临时端口数（用于检测全端口防火墙） |
| 最大重传次数 | PUSH 标志重传次数（RFC 793 建议 8 次，超时 100 秒） |
| 协议握手列表 | 按优先级排序的协议列表（影响覆盖速度） |
| 扫描速率 | 受 ZMap 发送速率限制（默认 50K pps） |
| 并发 Go routine 数 | 内部小池，CPU 密集型（指纹匹配为主要瓶颈） |

### 7.4 关键 Lessons Learned

**关于全网扫描**：
- SYN-ACK 不等于服务存在，40% 的 SYN-ACK 主机不确认数据
- 两阶段扫描（ZMap + ZGrab）引入系统性偏差，中间件保护是主要原因
- 仅扫描 IANA 指定端口会遗漏 90%+ 的协议部署

**关于协议部署**：
- 协议部署极度分散，HTTP 和 TLS 出现在所有 65,535 个端口上
- 达到 90% HTTP 覆盖率需要扫描 25,000 个端口，90% TLS 需要 40,000 个
- "最流行端口"因协议而异，不能简单使用全局最流行端口列表

**关于非预期服务安全**：
- IoT 设备是非预期服务的主要来源，安全态势显著更差
- 非预期端口 TLS 证书已知私钥概率高 1.17 倍
- 非预期端口 SSH 更可能使用弱认证方法（密码、主机认证）
- 超过一半非预期端口托管登录页面，暴露更多攻击面

**关于扫描优化**：
- 5 次握手可覆盖 99% 可识别非预期服务
- 等待服务器先发（"listen more"）是最高效的第一步
- 使用 PUSH 标志重传可额外发现 0.18% 的主机

### 7.5 能否迁移到其他任务？

- **[[censorship-circumvention]]**：LZR 的中间件行为分类可用于识别审查设备和策略
- **[[tunnel-detection]]**：非预期协议识别方法可用于检测隧道和代理服务
- **IoT 安全评估**：非预期端口扫描可系统发现暴露的 IoT 设备
- **Botnet 追踪**：Telnet 部署长尾分析表明 botnet 攻击面比先前估计大 15 倍
- **密码学弱点研究**：扩展到非标准端口可发现更多弱密钥和证书
- **Web PKI 研究**：非预期端口 TLS 证书分析可补充现有 HTTPS 研究

### 7.6 开放问题与未来研究方向

1. **端口选择策略**：如何高效选择值得扫描的端口子集？仅使用最流行端口不充分
2. **二进制协议覆盖**：如何高效识别不响应错误握手的二进制协议？
3. **协议部署动态性**：协议部署分布如何随时间变化？
4. **中间件演化**：中间件保护行为是否在增加？新的保护机制？
5. **QUIC/HTTP3**：UDP 基础的协议部署是否也存在类似的分散性？
6. **IPv6 服务部署**：IPv6 地址空间的协议部署分布如何？

### 7.7 对我的研究有什么启发？

1. **[[traffic-classification]] 研究**：仅关注标准端口会遗漏大量服务，分类器训练数据应包含非标准端口流量
2. **[[encrypted-traffic-analysis]] 研究**：93% TLS 不在端口 443 上，TLS 分析应覆盖全端口
3. **[[survey-encrypted-traffic-analysis]] 综述**：应强调端口选择偏差对研究结论的影响
4. **[[survey-malicious-traffic-detection]] 综述**：恶意流量可能隐藏在非标准端口上
5. **数据集构建**：构建流量数据集时应考虑非预期端口的协议分布
6. **中间件意识**：网络测量研究需考虑中间件对扫描结果的影响

## 8. 总结

### 8.1 核心思想（不超过20字）

协议部署极度分散，中间件导致伪服务，LZR 高效识别非预期服务。

### 8.2 速记版 Pipeline（3-5步）

1. 两阶段扫描揭示 L4-L7 存活差距（28% 主机不确认数据）
2. 系统分类 5 种中间件保护行为（连接回避、零窗口、连接中断、重置、动态阻断）
3. 30 个协议扫描器揭示协议部署极度分散（3% HTTP 在端口 80）
4. 贪婪算法计算最优 5 次握手顺序（覆盖 99% 可识别服务）
5. LZR 实现 fail-fast 过滤 + fingerprint-everything 识别（55 倍加速）

## 9. Obsidian 知识链接

### 9.1 相关概念

- Internet-wide Scanning - 全网扫描
- IANA Port Assignment - IANA 端口分配
- Middlebox Behavior - 中间件行为
- TCP State Machine - TCP 状态机
- Connection Shunning - 连接回避
- Zero Window DDoS Protection - 零窗口 DDoS 保护
- Dynamic Blocking - 动态阻断
- Protocol Fingerprinting - 协议指纹识别
- Service Discovery - 服务发现

### 9.2 相关方法

- ZMap - 无状态全网 SYN 扫描器
- ZGrab - 有状态应用层握手扫描器
- Masscan - 另一个全网扫描工具
- libpcap - 原始网络帧收发库
- TCP State Inference - TCP 状态推断

### 9.3 相关任务

- [[traffic-classification]] - 流量分类
- [[encrypted-traffic-analysis]] - 加密流量分析
- [[tunnel-detection]] - 隧道检测
- [[censorship-circumvention]] - 审查规避
- IoT Security Assessment - IoT 安全评估
- Botnet Tracking - 僵尸网络追踪
- Certificate Transparency - 证书透明度

### 9.4 可更新的综述页面

- [[survey-encrypted-traffic-analysis]] - 加密流量分析综述
- [[survey-malicious-traffic-detection]] - 恶意流量检测综述
- Internet Scanning Methodology Survey - 全网扫描方法综述

### 9.5 可加入的对比表

- Internet Scanning Tools Comparison (ZMap vs Masscan vs LZR)
- Middlebox Protection Behaviors Taxonomy
- Protocol Deployment Distribution Across Ports
- Non-standard Port Security Posture Metrics

## 10. 证据记录（表格形式）

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E1 | L4-L7 差距 | 37 个端口上平均 96% 的服务不完成 L7 握手 | Section 2.1, Figure 1 |
| E2 | L4-L7 差距 | 端口 80 上 14% 不完成 L7 握手，端口 102 上 96% | Section 2.1, Figure 1 |
| E3 | 连接回避 | 70% 的"消失"主机对新 IP 有响应，确认为连接回避 | Section 2.2 |
| E4 | 连接回避 | 40% 的回避网络是 /32（主机级），10% > /24（网络级） | Section 2.2, Figure 4 |
| E5 | 零窗口 | 99.94% 零窗口主机永不增大窗口，99% 在所有端口一致 | Section 2.4 |
| E6 | 零窗口 | 90% 零窗口主机在网络 > /24 上部署 | Section 2.4, Figure 4 |
| E7 | 零窗口 | Florida DMS (ASN 8103) 贡献 16% 全网零窗口 | Section 2.4 |
| E8 | 连接中断 | ISP 保护消费设备：CenturyLink, Frontier, MCI 在端口 4567 | Section 2.5 |
| E9 | 连接重置 | 73% 热门端口、34% 冷门端口的不确认数据主机在握手后重置 | Section 2.6, Figure 3b |
| E10 | 连接重置 | KT, Vodafone AU, OVH, Akamai 占 40%+ 重置主机 | Section 2.6 |
| E11 | 动态阻断 | 98% 不响应主机对新 IP 有响应，确认为动态阻断 | Section 2.7 |
| E12 | 中间件总结 | 16% 热门端口、40% 冷门端口的不确认数据主机是中间件伪服务 | Section 2.8 |
| E13 | 中间件总结 | 40% 路由 AS 包含至少一种中间件保护 | Section 2.8 |
| E14 | 协议部署 | 仅 3% HTTP 在端口 80，6% TLS 在端口 443 | Section 3.2, Figure 9 |
| E15 | 协议部署 | 达到 90% HTTP 覆盖需扫描 25,000 端口 | Section 3.2, Figure 9 |
| E16 | 协议部署 | 达到 90% TLS 覆盖需扫描 40,000 端口 | Section 3.2 |
| E17 | 协议部署 | 83.1% AMQP 在端口 5672 | Section 3.2, Figure 9 |
| E18 | 协议部署 | 5.5% Telnet 在端口 23，攻击面比先前估计大 15 倍 | Section 3.2, Table 1 |
| E19 | 非预期服务 | 65% 非预期服务是 HTTP，30% 是 TLS | Section 3.2, Figure 7 |
| E20 | 非预期服务 | 50% 非预期端口 TLS 属于 IoT 设备 | Section 3.3 |
| E21 | 非预期服务 | 非预期端口 TLS 已知私钥概率高 1.17 倍 | Section 3.3 |
| E22 | 非预期服务 | 非预期端口 SSH 非公钥认证概率高 15% | Section 3.3 |
| E23 | 非预期服务 | 8000/TLS 35% 为韩国 icctv 监控摄像头 | Section 3.3 |
| E24 | 非预期服务 | 80/TLS 38% 为华为网络设备 | Section 3.3 |
| E25 | 非预期服务 | 50%+ 非预期端口托管登录页面 | Section 3.3 |
| E26 | 非预期服务 | 8080/HTTP 登录页面比例比端口 80 高 2.4 倍 | Section 3.3 |
| E27 | 协议发现 | 5 次握手覆盖 99% 可识别非预期服务 | Section 4.1, Table 2 |
| E28 | 协议发现 | 8/30 协议是"服务器优先" | Section 4.1 |
| E29 | 协议发现 | 16/30 协议响应 HTTP GET 或 TLS Client Hello | Section 4.1, Figure 10 |
| E30 | 协议发现 | 75% 二进制协议不响应错误握手 | Section 4.1 |
| E31 | 握手参数 | PPTP 错误 Magic Cookie 导致 67.1% 无响应 | Section 4.2, Table 3 |
| E32 | 握手参数 | TLS 不兼容密码套件导致 2.65% 关闭连接 | Section 4.2, Table 3 |
| E33 | 连续握手 | 错误握手导致 17-30% 后续握手失败 | Section 4.3, Figure 11 |
| E34 | 连续握手 | 75% 失败主机 5 秒内恢复，99% 2 分钟内恢复 | Section 4.3 |
| E35 | LZR 性能 | MongoDB 端口 55 倍加速（Offline ZMap + LZR） | Table 4 |
| E36 | LZR 性能 | TLS 端口 4.7 倍加速（ZMap/LZR vs ZGrab） | Table 4 |
| E37 | LZR 准确性 | KS 检验 p > 0.05，LZR 与 ZGrab 发现服务无显著差异 | Section 5.3 |
| E38 | LZR 发现 | 单次 HTTP 握手识别 88% 可识别服务 | Section 5.3 |
| E39 | LZR 发现 | 5672/AMQP 上非预期服务 260K > 预期服务 123K | Table 4 |
| E40 | F5 防火墙 | 5 个 AS（加拿大政府）贡献 77% 全端口响应主机 | Section 3.1 |
| E41 | F5 防火墙 | 5 个随机临时端口过滤 99.9% 全端口防火墙主机 | Section 3.1 |
| E42 | 扫描投诉 | 100% IPv4 扫描收到 7 个组织投诉 | Section 5.3 |

## 11. 原始资料链接

- 论文发表于 30th USENIX Security Symposium, August 11-13, 2021
- 作者单位：
  - Liz Izhikevich, Zakir Durumeric: Stanford University
  - Renata Teixeira: Inria, Paris
- 开源工具：https://github.com/stanford-esrg/lzr（Apache 2.0 许可证）
- 相关工具：ZMap (https://zmap.io/), ZGrab (https://github.com/zmap/zgrab2), Masscan (https://github.com/robertdavidgraham/masscan)
- 数据来源：Censys (https://censys.io/)

## 12. 后续问题

1. **IPv6 部署**：IPv6 地址空间的协议部署分布是否与 IPv4 类似？中间件保护行为是否相同？
2. **QUIC/HTTP3**：UDP 基础的协议是否也存在类似的端口分散性？
3. **协议部署动态性**：COVID-19 期间远程办公增加是否改变了协议部署分布？
4. **中间件演化**：新的中间件保护机制（如 eBPF 基础防火墙）是否改变了扫描格局？
5. **LZR 与 Censys/Shodan 集成**：LZR 的发现如何补充现有互联网测绘平台？
6. **非预期服务安全影响**：非预期端口上的弱安全配置是否已被实际攻击利用？
7. **端口选择优化**：如何基于轻量级子采样扫描预测最值得扫描的端口？
8. **二进制协议识别**：如何高效识别不响应错误握手的二进制协议（如 MQTT, Postgres）？
9. **IoT 安全干预**：非预期端口上的 IoT 设备安全问题如何通过协调披露解决？
10. **扫描伦理**：如何在全网扫描的科学价值和对网络运营商的影响之间取得平衡？

## 13. 与知识库的关联

### 与 [[encrypted-traffic-analysis]] 的关联

LZR 揭示 93% TLS 服务不在端口 443 上，这对加密流量分析研究具有重要启示：
- 现有 TLS 流量分析研究仅关注标准端口，遗漏了绝大多数 TLS 部署
- 非标准端口 TLS 更可能属于 IoT 设备，具有不同的流量特征
- 构建 TLS 流量数据集时应考虑全端口采样

### 与 [[traffic-classification]] 的关联

协议部署的极度分散性对流量分类器训练和评估有直接影响：
- 仅基于标准端口流量训练的分类器可能无法泛化到非标准端口
- 非预期端口上的服务可能有不同的流量模式（如 IoT 设备的 TLS）
- 流量分类基准数据集应包含非标准端口流量

### 与 [[tunnel-detection]] 的关联

LZR 的非预期服务发现方法可应用于隧道检测：
- 隧道服务通常运行在非标准端口上以规避检测
- LZR 的协议指纹识别方法可用于识别隧道协议
- 中间件保护行为的分类有助于区分隧道流量和中间件伪服务

### 与 [[censorship-circumvention]] 的关联

LZR 的中间件行为分类直接关联审查规避研究：
- 连接回避和动态阻断是审查设备的常见行为
- 零窗口 DDoS 保护可能被滥用于审查
- 理解中间件行为有助于设计更有效的规避策略

### 与 [[survey-encrypted-traffic-analysis]] 和 [[survey-malicious-traffic-detection]] 的关联

本文的发现对相关综述研究有重要参考价值：
- 端口选择偏差是现有研究的系统性问题，综述应强调这一局限
- 非预期端口上的安全问题（弱 TLS、弱 SSH）应纳入恶意流量检测综述
- IoT 设备在非标准端口上的广泛部署是新兴研究方向

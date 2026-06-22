---
type: paper
title_original: "Censorship Evasion with Unidentified Protocol Generation"
title_cn: "基于未识别协议生成的审查规避"
authors: ["Ryan Wails", "Rob Jansen", "Aaron Johnson", "Micah Sherr"]
year: 2025
venue: "USENIX Security 2025"
doi: unknown
url: "https://www.usenix.org/conference/usenixsecurity25/presentation/wails"
pdf: unknown
mineru_md: "02-parsed-markdown/2025-USENIX-Censorship_Evasion_with_Unidentified_Protocol_Generation.md"
status: processed
reading_level: L3
research_area: ["censorship circumvention", "encrypted protocol generation", "traffic analysis resistance"]
task: ["protocol generation", "censorship evasion", "collateral damage maximization"]
method: ["protocol parameter sampling", "programmable protocol system", "ML-based security evaluation", "distributed simulation"]
dataset: ["custom UPGen traffic traces", "WIDE MAWI", "Tor Shadow simulation"]
code: "https://github.com/unblockable/upgen"
relevance: high
created: "2026-06-21"
updated: "2026-06-21"
---

# Censorship Evasion with Unidentified Protocol Generation

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Censorship Evasion with Unidentified Protocol Generation |
| 中文标题 | 基于未识别协议生成的审查规避 |
| 作者 | Ryan Wails (NRL & Georgetown), Rob Jansen (NRL), Aaron Johnson (NRL), Micah Sherr (Georgetown) |
| 年份 | 2025 |
| 会议/期刊 | USENIX Security 2025 |
| 研究方向 | 审查规避、加密协议生成、流量分析抵抗 |
| 任务类型 | 自动生成大量结构化加密协议以规避国家级审查，同时最大化附带损害 |
| 方法关键词 | protocol parameter sampling, programmable protocol system (Proteus), ML-based security evaluation, Shadow distributed simulation |
| 数据集 | 自建 UPGen 流量 traces（每协议 1000 条）、WIDE MAWI 骨干网流量、Tor Shadow 仿真数据 |
| 是否开源 | 是（UPGen 生成器 + 扩展版 Proteus + 流量生成器 + PSF 文件，Zenodo: 10.5281/zenodo.15491977） |
| PDF | 00-inbox/PDFs/2025-USENIX-Censorship_Evasion_with_Unidentified_Protocol_Generation.pdf |
| MinerU Markdown | 02-parsed-markdown/2025-USENIX-Censorship_Evasion_with_Unidentified_Protocol_Generation.md |

## 1. 一句话总结

> 提出 UPGen 系统，通过概率采样从 27 种真实加密协议的共性特征中自动生成 4.2 x 10^22 种结构化加密协议，使审查者在尝试封锁时必然造成大规模附带损害（OOD FPR 接近 100%），且性能优于或持平 Obfs4 等主流规避协议。

## 2. 摘要翻译

### 2.1 摘要原文

We present the design and implementation of a novel approach to internet censorship evasion called Unidentified Protocol Generation (UPGen). UPGen automatically generates novel protocols for encrypted communication that are not easily recognizable as being UPGen protocols, but instead as some benign encrypted protocol unknown to the adversary. UPGen protocols are to be used to relay traffic to censored destinations via proxies, where each proxy can run a different UPGen-generated protocol. An adversary attempting to block at the protocol level but unable to identify UPGen protocols could cause significant collateral damage if it attempted to block all unidentified protocols. We conduct a security evaluation of UPGen employing state-of-the-art machine learning classifiers and find that it is infeasible to block UPGen protocols without also blocking existing encrypted protocols. We conduct small- and large-scale performance evaluations and find that UPGen protocols meet or exceed the performance of other common censorship evasion protocols.

### 2.2 摘要中文翻译

我们提出了一种名为"未识别协议生成"（UPGen）的互联网审查规避新方法的设计与实现。UPGen 自动生成用于加密通信的新型协议，这些协议不易被识别为 UPGen 协议，而是看起来像某种审查者未知的良性加密协议。UPGen 协议通过代理将流量中继到被审查的目的地，每个代理可以运行不同的 UPGen 生成协议。试图在协议级别进行封锁但无法识别 UPGen 协议的审查者，如果试图封锁所有未识别协议，将造成严重的附带损害。我们使用最先进的机器学习分类器对 UPGen 进行安全评估，发现封锁 UPGen 协议而不同时封锁现有加密协议是不可行的。我们进行了小规模和大规模性能评估，发现 UPGen 协议达到或超过了其他常见审查规避协议的性能。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？（三大核心洞察）

本文的方法动机源于对审查规避领域三个关键观察的综合：

**洞察 1 — 加密协议的结构化特征普遍存在**：虽然加密可以隐藏协议元数据，但典型的加密协议都展现出协议结构和未加密字段（如问候字符串、版本号、消息类型）。这意味着完全随机化（如 FEP）反而成为了一个可检测的指纹。

**洞察 2 — 加密协议的生态极其多样化**：加密协议不仅包括 TLS、SSH 等知名协议，还包括加密货币（Lightning、RLPx）、IoT（MQTT、OSCORE）、文件存储（msgr2）、视频游戏（GameNetworkingSockets）、键盘预测等众多不太知名的协议。审查者不可能了解所有这些协议。

**洞察 3 — 协议级封锁的附带损害杠杆**：部署协议特定分类器的审查者通常可以破坏无法适应或使用未被封锁的回退协议的规避工具。但如果规避工具使用的是大量"看似合理但无法关联"的加密协议，审查者要么为每个协议开发分类器（不可行），要么冒着封锁大量良性流量的风险。

### 3.2 现有方法的痛点和不足

| 现有方法/问题 | 痛点 | 影响范围 |
|---|---|---|
| 全加密协议 (FEP) | 完全随机化的字节流本身成为可检测指纹，已被 GFW 实际封锁 [86] | Obfs4, ScrambleSuit, Shadowsocks, Lantern, VMess |
| 协议隧道 | 隧道协议层之间的一致性可被利用 [7,18,29,44,87]，或依赖不切实际的用户模型且性能差 [80] | Facet, DeltaShaper, CovertCast |
| TLS 伪装 | TLS 参数（Client Hello 内容）可被用于识别特定配置 [26]；ESNI/ECH 被部分审查者封锁 [11]；需要持续重新配置 | HTTPT, domain fronting, V2Ray |
| 协议模仿 | 精确模仿协议极其困难，微小差异可被利用 [35] | StegoTorus, SkypeMorph, CensorSpoofer |
| 可编程规避框架 | 缺乏如何配置有效协议的指导 | Marionette, Proteus, WATER |

### 3.3 论文的研究假设或核心直觉

**核心假设 1**：自动生成的协议空间足够大（4.2 x 10^22 种），使得为每个协议单独建立指纹是不可行的。

**核心假设 2**：生成的协议在结构特征上与真实加密协议足够相似，使得区分 UPGen 与未知良性协议的分类器必然产生高误报率（附带损害）。

**核心假设 3**：每个代理使用不同协议的设计确保了单个协议被发现和封锁只影响一个代理，不会使整个代理网络不可访问。

**核心假设 4**：审查者倾向于使用 blocklist（封锁列表）而非 allowlist（白名单），因为白名单会导致更大的附带损害——UPGen 正是利用了这一偏好。

## 4. 方法设计

### 4.1 方法整体流程

1. **协议调研**：研究 27 种真实世界加密协议（21 种开放设计），提取共性特征
2. **协议生成器设计**：基于观察到的模式设计概率采样算法，生成协议规范文件 (PSF)
3. **Proteus 扩展**：扩展 Proteus 可编程协议系统以支持密钥交换、随机加密、前向保密等特性
4. **安全评估**：使用 ML 分类器（Deep Fingerprinting、Decision Tree、Random Forest、nPrintML）评估可区分性
5. **DPI 工具分析**：使用 Zeek、libprotoident、nDPI 分析未识别协议的真实世界比例
6. **性能评估**：实验室基准测试 + Tor Shadow 大规模分布式仿真
7. **真实世界部署**：在中国进行小规模实际部署测试

### 4.2 详细 Pipeline（表格形式）

| 步骤 | 描述 | 技术细节 |
|---|---|---|
| 1. 协议调研 | 分析 27 种加密协议的共性模式 | Table 8: 21 种开放设计的协议，涵盖 TLS、SSH、CurveZMQ、Noise、secio、MQTT、QUIC 等 |
| 2. 参数采样 | Algorithm 1: 16 个参数的独立概率采样 | 安全参数、加密密码、类型字段、长度字段、版本字段、nonce 字段、填充长度字段、额外字段、保留字段、证书、密钥编码、问候字符串、握手模式、子协议模式、字段顺序、长度独立写入 |
| 3. PSF 生成 | 将采样参数确定性地转换为 Proteus 协议规范文件 | 使用 Proteus 协议语法生成 @SEGMENT.FORMATS, @SEGMENT.SEMANTICS, @SEGMENT.SEQUENCE, @SEGMENT.CRYPTO |
| 4. 流量收集 | 为每种协议收集流量 traces | 9000 行 C++/Rust/Python 自定义流量生成软件；客户端先发 1kB，服务器回 10kB，然后 256B/10kB 交替；tcpdump 抓包，tshark 过滤 |
| 5. ML 安全评估 | 训练分类器区分 UPGen 与良性协议流量 | 4 种分类器 x 5 种 OOD 良性协议 = 20 组实验；每组含 in-distribution 和 OOD 测试 |
| 6. DPI 分析 | 使用 3 种 DPI 工具分析协议识别率 | Zeek + libprotoident + nDPI；在自建数据集和 WIDE MAWI 数据集上测试 |
| 7. 性能基准 | 实验室延迟、吞吐量、可扩展性测试 | 3 台 28 核 Xeon 服务器，10Gbps 直连；对比 Dummy、Obfs4、TLS、UPGen (best/avg/worst) |
| 8. Tor 仿真 | Shadow 离散事件分布式系统仿真 | 20% 规模 Tor 网络：1527 节点，1755 流量生成器，950K 电路/10min，150K 用户等效 |
| 9. OpenGFW 测试 | 模拟 GFW 的全加密流量检测规则 | 1000 个 UPGen PSF + 1000 个 Obfs4 配置通过 OpenGFW FET 分析器 |
| 10. 真实部署 | 在中国实际部署测试 | 北京、广州、上海的 VM 客户端连接北美代理，持续两周，每 30 分钟 5 次传输 |

### 4.3 Generator 参数空间详解（Algorithm 1）

| 参数 | 选项数 | 熵 (bits) | 描述 |
|---|---|---|---|
| SECPARAM() | 2 | 1.0 | 安全参数：128 或 256 位 |
| CIPHER(s) | 3 | 0.5 | AES-128-GCM, AES-256-GCM, ChaCha20-Poly1305 |
| TYPEFIELD() | 25 | 2.7 | 消息类型字段：明文或加密，集合大小 x 起始值 |
| LENGTHFIELD() | 2 | 0.81 | 长度字段：明文，2 种字节长度 |
| VERSIONFIELD() | 36 | 4.1 | 版本字段：明文或加密，36 种组合 |
| NONCEFIELD(s) | 3 | 1.0 | Nonce 字段：明文，长度为安全参数 |
| PADLENGTHFIELD(c,l) | 2 | 0.25 | 填充长度字段：加密，仅块密码时出现 |
| EXTRAFIELD(t,v) | 9 | 2.4 | 额外字段：加密，类型或版本加密时出现 |
| RESERVEDFIELD() | 5 | 1.1 | 保留字段：加密，仅握手阶段 |
| CERTIFICATE() | 2048 | 6.5 | 证书字段：加密，2048 种长度 |
| KEYENCODING() | 3 | 1.6 | 密钥编码：DER、PEM 或原始字节 |
| GREETINGSTRING() | 3 | 1.1 | 问候字符串：由 RNN 生成（训练于 GitHub 仓库名） |
| HANDSHAKE() | 8 | 3.0 | 握手模式：0-RTT, 1-RTT, 1.5-RTT 共 8 种 |
| SUBPROTOCOL(h) | 4.0 x 10^9 | 8.3 | 子协议模式：0/1/2 次消息交换，每次 252 种大小 |
| FIELDORDER() | 12 | 3.6 | 字段顺序：明文/加密字段各自随机排列 |
| LENGTHALONE(f) | 2 | 0.48 | 长度字段是否独立写入（可能独占 TCP 包） |
| **总计** | **4.2 x 10^22** | **38.4** | - |

### 4.4 协议三阶段设计模式

所有 UPGen 协议遵循统一的三阶段设计：

**Greeting 阶段**（可选）：双方交换 ASCII 可打印的固定长度问候字符串。由 RNN 训练于 GitHub 仓库名称生成。

**Handshake 阶段**：执行（或看起来执行）连接设置功能，如密钥交换。临时密钥使用 Curve25519 进行 Diffie-Hellman 交换，提供前向保密。静态密钥仅用于外观，不用于加密或认证。

**Data 阶段**：应用数据在客户端和服务器之间传输。消息布局为：未加密字段 → 加密字段 → payload（始终最后）。

### 4.5 模型结构或系统模块（表格形式）

| 模块 | 功能 | 输入 | 输出 |
|---|---|---|---|
| Generator | 概率采样生成协议规范 | 随机性 | Protocol Specification File (PSF) |
| Proxy Provisioner | 为每个代理配置 PSF 和长期对称密钥 | PSF, 密钥 | 配置好的代理 |
| Proxy Distributor | 向客户端分发代理信息 | 代理地址、PSF、密钥 | 客户端配置 |
| Programmable Protocol Engine (Proteus) | 执行 PSF 定义的协议 | PSF, 网络连接 | 加密通信通道 |
| Traffic Generator (tgen) | 模拟应用行为产生测试流量 | 流量模型 | pcap 文件 |

### 4.6 方法优势

1. **协议空间巨大**：4.2 x 10^22 种协议远超可枚举范围，即使排除子协议模式也有 10^13+ 种
2. **无需模仿**：不模仿任何特定协议，避免了协议模仿的精确性难题 [35]
3. **独立部署**：每个代理使用不同协议，单点暴露不影响全局
4. **可维护性**：无需与外部系统保持同步；生成器可独立更新以适应新的审查技术
5. **前向保密**：使用临时密钥交换，即使长期密钥泄露也不影响历史通信安全
6. **结构化设计**：包含真实的协议结构元素（类型字段、版本号、nonce 等），与完全随机化形成对比

### 4.7 方法不足

1. **无流量整形**：不进行流量整形/填充，无法隐藏隧道流量的可检测模式 [29,81,87]
2. **不抗主动攻击**：主动审查者可以丢弃、注入或修改数据包；修改的加密数据只会导致连接关闭（不像 TLS 使用 Alert 消息）
3. **不支持多路复用**：每个 UPGen 连接仅支持隧道一个 TCP 连接，无直接多路复用支持
4. **依赖未被封锁的代理**：需要将代理信息安全分发给客户端，这是所有审查规避系统面临的共同挑战
5. **仅支持 TCP**：系统设计仅支持代理 TCP 连接
6. **问候字符串的 RNN 生成**：使用 GitHub 仓库名训练的 RNN 生成问候字符串，其真实性和多样性有待验证

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 对比维度 | 全加密协议 (FEP) | TLS 伪装 | 协议模仿 | UPGen |
|---|---|---|---|---|
| 核心策略 | 完全随机化，隐藏所有元数据 | 利用 TLS 的普遍性 | 精确模仿特定协议 | 生成大量"看似合理"的新协议 |
| 指纹风险 | 随机化本身成为指纹 [86] | TLS 参数可被识别 [26] | 微小差异可被利用 [35] | 与未知良性协议不可区分 |
| 维护成本 | 低 | 高（需跟踪 TLS 变化） | 高（需跟踪目标协议变化） | 低（无需与外部系统同步） |
| 单点失败 | 全局影响 | 全局影响 | 全局影响 | 仅影响单个代理 |
| 附带损害 | 低（可被针对性封锁） | 中（TLS 太普遍） | 低（可被识别） | 高（封锁需牺牲大量良性协议） |

### 5.2 创新点分析（表格形式）

| 创新点 | 说明 |
|---|---|
| 协议空间生成 | 首次系统化地从真实协议共性中提取参数空间，生成 4.2 x 10^22 种结构化加密协议 |
| 安全性论证框架 | 形式化定义安全目标：U（生成空间）与 P\Q（未知良性协议）不可区分 |
| 附带损害量化 | 通过 OOD 实验量化审查者封锁 UPGen 所需付出的附带损害代价 |
| DPI 工具覆盖分析 | 使用 3 种 DPI 工具分析真实世界流量中未识别协议的比例，证明白名单不可行 |
| OpenGFW 实验 | 首次在模拟 GFW 环境中测试自动生成协议对全加密流量检测规则的抵抗力 |
| Proteus 扩展 | 扩展 Proteus 支持密钥交换、随机加密、前向保密等完整协议特性 |

### 5.3 适用场景

- Tor 桥接部署：Tor Project 作为 Generator 和 Provisioner，第三方运行代理
- VPN 提供商：提供商运行所有角色，通过软件分发渠道分发配置
- 个人部署：个人运行代理并承担所有角色
- 高审查环境：需要最大化审查者附带损害的场景

### 5.4 与 Obfs4 的详细对比

| 对比维度 | Obfs4 | UPGen |
|---|---|---|
| 协议数量 | 1 种固定协议 | 4.2 x 10^22 种可生成协议 |
| 设计理念 | 完全随机化（FEP） | 结构化加密（模拟真实协议特征） |
| ML 分类器抵抗 | DF 可在 3/4 OOD 场景中识别，OOD FPR 接近 0% | 所有分类器在所有场景中 OOD FPR 接近 100% |
| DPI 识别 | 3 种工具均标记为 Unknown（无误识别） | 3 种工具均标记为 Unknown（7% 被 libprotoident 误识别为 RTMP） |
| OpenGFW 抵抗 | 0.4% 成功穿越（随机 printable 字符概率） | 56.2% 成功穿越（结构化特征降低熵值） |
| 延迟 (TTFB) | 212 ms | 252-677 ms（取决于握手轮次） |
| 吞吐量 | 4.65 Gbit/s/core | 3.70-4.25 Gbit/s/core |
| 内存使用 | 5.96 GiB (50K sockets) | 2.25-2.88 GiB (50K sockets) |
| 连接成功率 | 低于 50K（goptlib 连接错误） | 达到 50,000（全部成功） |
| 模块化组合 | 无 | DF + Random Forest 的逻辑与组合无法对 UPGen 实现完美分类（对比 Obfs4 可以） |

## 6. 实验表现与优势

### 6.1 实验设计和设置

**安全评估实验**：
- 7 种良性加密协议：TLS 1.2, TLS 1.3, SSH 2.0, CurveZMQ, Noise, secio, Obfs4
- UPGen：1000 个 PSF（in-distribution，每协议 5 条 trace）+ 2500 个 PSF（OOD，每协议 2 条 trace）
- 4 种分类器：Deep Fingerprinting (DF), Decision Tree, Random Forest, nPrintML
- 2 种特征表示：包长度序列（30 包）、nPrint 位序列（30 包 x 280 位）
- 5 种 OOD 良性协议选择：CurveZMQ, Noise, secio, SSH, TLS

**性能评估实验**：
- 硬件：3 台 28 核 Intel Xeon E5-2697, 256GB RAM, 10Gbps 直连
- 协议：Dummy（无加密基线）, Obfs4, TLS 1.3, UPGen (best/avg/worst)
- 指标：延迟（TTFB）、单核吞吐量、可扩展性（50K sockets 内存）

**Tor 仿真实验**：
- 20 个 20% 规模 Tor 网络，Shadow 离散事件仿真
- 1527 Tor 节点，1755 流量生成器，950K 电路/10min，150K 用户等效
- 4 种代理协议变体，每种 20 次仿真

### 6.2 数据集

| 数据集 | 规模 | 协议 | 用途 |
|---|---|---|---|
| UPGen in-distribution | 1000 PSF x 5 traces = 5000 | UPGen | ML 训练和 in-distribution 测试 |
| UPGen OOD | 2500 PSF x 2 traces = 5000 | UPGen | OOD 测试 |
| 良性协议 traces | 每协议 1000 traces | TLS 1.2, TLS 1.3, SSH, CurveZMQ, Noise, secio | ML 训练和测试 |
| Obfs4 traces | 1000 traces | Obfs4 | 对比实验 |
| WIDE MAWI | 205,127-305,513 TCP 流 | 真实世界混合 | DPI 工具未识别率分析 |
| Tor Shadow | 20 网络 x 20 次仿真 | Tor + 代理协议 | 大规模性能评估 |

### 6.3 Baseline

- **Dummy 协议**：无加密的数据转发，代表性能上限
- **Obfs4**：主流全加密审查规避协议，代表 FEP 的安全性和性能基线
- **TLS 1.3**：最广泛部署的加密协议，代表优化良好的加密性能

### 6.4 评价指标

**安全评估指标**：
- In-distribution TPR：审查者在训练过的 UPGen 协议上的检测率
- In-distribution FPR：审查者对训练集内良性协议的误封率
- OOD TPR：审查者对未训练过的 UPGen 协议的检测率
- OOD FPR：审查者对训练集外良性协议的误封率（**关键指标**）

**性能评估指标**：
- 延迟 (TTFB)：从发起连接到收到第一个 payload 字节的时间
- 吞吐量 (Gbit/s/core)：单核每秒发送和接收的字节总和
- 可扩展性：50K 并发连接下的内存使用和连接成功率

### 6.5 关键实验结果（表格形式）

**Table 3: ML 分类器对 UPGen 的 OOD 性能（核心安全结果）**

| OOD 良性协议 | 分类器 | In-dist TPR | In-dist FPR | OOD TPR | OOD FPR |
|---|---|---|---|---|---|
| CurveZMQ | DF | 1.00 | 0.00 | 0.25 | **1.00** |
| CurveZMQ | Decision Tree | 1.00 | 0.00 | 0.93 | **1.00** |
| CurveZMQ | Random Forest | 1.00 | 0.00 | 0.81 | **1.00** |
| CurveZMQ | nPrintML | 1.00 | 0.00 | 1.00 | **1.00** |
| secio | DF | 0.99 | 0.05 | 0.04 | **0.90** |
| secio | Decision Tree | 1.00 | 0.00 | 0.94 | **0.89** |
| secio | Random Forest | 1.00 | 0.00 | 0.36 | **1.00** |
| secio | nPrintML | 1.00 | 0.00 | 1.00 | **1.00** |
| SSH | DF | 0.99 | 0.00 | 0.20 | **0.41** |
| SSH | Decision Tree | 1.00 | 0.00 | 0.97 | **1.00** |
| SSH | Random Forest | 1.00 | 0.00 | 1.00 | **1.00** |
| SSH | nPrintML | 1.00 | 0.00 | 1.00 | **1.00** |
| TLS | DF | 1.00 | 0.00 | 0.00 | **1.00** |
| TLS | Decision Tree | 1.00 | 0.00 | 0.20 | **1.00** |
| TLS | Random Forest | 1.00 | 0.00 | 0.79 | **1.00** |
| TLS | nPrintML | 1.00 | 0.00 | 1.00 | **1.00** |
| Noise (验证) | DF | 0.99 | 0.00 | 0.01 | **1.00** |
| Noise (验证) | Decision Tree | 1.00 | 0.00 | 0.99 | **1.00** |
| Noise (验证) | Random Forest | 1.00 | 0.00 | 0.78 | **1.00** |
| Noise (验证) | nPrintML | 1.00 | 0.00 | 1.00 | **1.00** |

**关键发现**：所有分类器在所有 OOD 场景中 FPR 接近 100%（唯一例外：SSH+DF 组合 FPR=0.41，但此时 TPR 仅 0.20）。这意味着审查者封锁 UPGen 时必然封锁几乎所有良性加密协议。

**Table 4: ML 分类器对 Obfs4 的 OOD 性能（对比）**

| OOD 良性协议 | 分类器 | In-dist TPR | In-dist FPR | OOD FPR |
|---|---|---|---|---|
| CurveZMQ | DF | 1.00 | 0.00 | **0.00** |
| secio | DF | 1.00 | 0.00 | **0.00** |
| SSH | DF | 1.00 | 0.00 | **0.00** |
| TLS | DF | 1.00 | 0.00 | **1.00** |
| 多数组合 | Decision Tree | 0.99 | 0.00 | **0.00-0.20** |

**关键发现**：Obfs4 的 OOD FPR 显著低于 UPGen。DF 和 Random Forest 的逻辑与组合可实现 Obfs4 的完美 TPR 和 FPR（但对 UPGen 不行）。

**Table 5: DPI 工具协议识别率**

| 协议 | libprotoident K | libprotoident M | libprotoident U | nDPI K | nDPI M | nDPI U | Zeek K | Zeek M | Zeek U |
|---|---|---|---|---|---|---|---|---|---|
| CurveZMQ | 0 | 0 | 1.0 | 1.0 | 0 | 0 | 0 | 0 | 1.0 |
| Noise | 0 | 0 | 1.0 | 0 | 0 | 1.0 | 0 | 0 | 1.0 |
| Obfs4 | 0 | 0 | 1.0 | 0 | 0 | 1.0 | 0 | 0 | 1.0 |
| secio | 0 | 0 | 1.0 | 0 | 0 | 1.0 | 0 | 0 | 1.0 |
| SSH | 1.0 | 0 | 0 | 1.0 | 0 | 0 | 1.0 | 0 | 0 |
| TLS | 1.0 | 0 | 0 | 1.0 | 0 | 0 | 1.0 | 0 | 0 |
| UPGen | 0 | 0.07 | **0.93** | 0 | 0 | **1.0** | 0 | 0 | **1.0** |

K=已知, M=误识别, U=未识别。UPGen 的 93-100% 流量被 DPI 工具标记为未识别。

**Table 7: 性能基准结果**

| 代理协议 | 延迟 TTFB (ms) | 吞吐量 (Gbit/s/core) | 最大连接数 | 内存 (GiB) |
|---|---|---|---|---|
| Dummy | 211 | 18.4 | 43,248 | 0.61 |
| Obfs4 | 212 | 4.65 | 47,826 | 5.96 |
| TLS | 313 | 9.42 | 49,990 | 12.4 |
| UPGen best | 252 | 4.25 | 50,000 | 2.25 |
| UPGen avg | 420 +/- 50 | 4.0 +/- 0.2 | 50,000 | 2.63 +/- 0.02 |
| UPGen worst | 677 | 3.70 | 50,000 | 2.88 |

**关键发现**：UPGen 延迟与 Obfs4 相当（best 模式），吞吐量略低于 Obfs4 但仍在 Gbit/s 级别，内存使用显著低于 Obfs4（约一半）和 TLS（约五分之一），且是唯一成功维持全部 50,000 连接的协议。

**OpenGFW 实验结果**：
- UPGen：562/1000 (56.2%) 协议成功穿越 OpenGFW 的全加密流量检测
- Obfs4：4/1000 (0.4%) 配置成功穿越

**WIDE MAWI DPI 分析**：
- libprotoident：约 4% 流量未识别
- nDPI：67% 流量未识别
- Zeek：90% 流量未识别
- 结论：白名单策略至少会产生 4% 的误封率（远超文献 [81,87] 提出的 0.6% 上限）

### 6.6 优势最明显的场景

- **ML 分类器抵抗**：OOD FPR 接近 100% 是所有实验的一致结果，表明 UPGen 在协议层面几乎不可区分于良性加密流量
- **OpenGFW 抵抗**：56.2% 的穿越率（vs Obfs4 的 0.4%）表明结构化设计对基于熵的检测有天然抵抗力
- **内存效率**：UPGen 使用 Proteus 运行时解释器，内存效率显著优于基于 goptlib 的 Obfs4/Dummy
- **连接可靠性**：UPGen 是唯一在 50K 连接测试中无连接错误的协议
- **模块化安全**：每个代理独立协议，单点暴露不影响全局网络

### 6.7 局限性

1. **流量整形缺失**：不进行流量整形，无法隐藏隧道流量模式
2. **主动攻击脆弱性**：对主动审查者（丢包、注入、修改）无特殊防护
3. **单连接限制**：每个 UPGen 连接仅支持一个 TCP 隧道
4. **代理分发依赖**：依赖安全的代理分发渠道
5. **应用行为固定**：安全评估使用固定应用行为（1kB→10kB→256B/10kB 交替），可能不反映真实多样性
6. **Noise 协议验证的局限**：虽然 Noise 未参与设计迭代，但其协议族可能与参与设计的协议有相似特征

## 7. 学习与应用

### 7.1 是否开源？

是。四个研究工件在 Zenodo 公开（10.5281/zenodo.15491977）：
1. UPGen 生成器组件：https://github.com/unblockable/upgen
2. 扩展版 Proteus (v0.2.0)：https://github.com/unblockable/proteus
3. 加密流量生成器
4. 实验用 PSF 文件

### 7.2 复现关键步骤

1. **协议生成**：运行 UPGen Generator，输入随机性，输出 PSF 文件
2. **Proteus 配置**：使用扩展版 Proteus 加载 PSF，配置客户端和代理
3. **流量收集**：使用自定义 C++/Rust/Python 流量生成软件，固定应用行为，tcpdump 抓包
4. **ML 评估**：
   - 特征提取：包长度序列（30 包，方向标记）或 nPrint 位序列（30 包 x 280 位）
   - 数据划分：500 良性训练 + 4 x 1000 UPGen 训练；500 良性 ID 测试 + 1000 OOD 良性测试 + 1000 UPGen ID 测试 + 5000 UPGen OOD 测试
   - 分类器训练：DF (CNN), Decision Tree, Random Forest, nPrintML (AutoGluon)
5. **性能测试**：tgen 流量生成 + netem 延迟注入 + dstat 资源监控

### 7.3 关键超参数、预处理和训练细节

| 参数 | 值/说明 |
|---|---|
| 包长度序列长度 | 30 包（遵循 Wang et al. [82]） |
| nPrint 位序列 | 30 包 x 280 位/包 |
| 每协议训练 traces | 良性: 500; UPGen: 4 x 1000 PSF |
| 每协议测试 traces | 良性 ID: 500; 良性 OOD: 1000; UPGen ID: 1000 PSF; UPGen OOD: 2500 PSF x 2 |
| DF 模型 | Sirinam et al. [70] 的 Deep Fingerprinting CNN |
| nPrintML | AutoGluon 自动选择最优分类器/集成 |
| 实验网络配置 | MTU 1500, 关闭 TSO/GSO, 禁用 IPv6 |
| 延迟注入 | netem 25ms 双向（客户端-代理 + 代理-服务器），总 RTT 100ms |
| Tor 仿真规模 | 20% 公共 Tor 网络，1527 节点，150K 用户等效 |

### 7.4 关键 Lessons Learned

1. **结构化优于随机化**：FEP 的完全随机化已被证明可被检测 [86]，而 UPGen 的结构化设计使其与良性协议不可区分
2. **附带损害是审查者的阿喀琉斯之踵**：审查者不愿封锁无法识别的流量（WIDE 数据显示至少 4% 的良性流量无法被 DPI 工具识别）
3. **协议多样性是关键安全属性**：4.2 x 10^22 的协议空间使得逐一封锁不可行
4. **OOD 泛化是审查者分类器的根本挑战**：分类器在训练分布内表现完美，但对 OOD 协议完全失败
5. **性能不应是瓶颈**：自动生成的协议可以达到与手工设计协议相当的性能
6. **每个代理独立协议是关键架构决策**：单点暴露不影响全局，大幅提高了系统的韧性

### 7.5 能否迁移到其他任务？

- **协议模糊测试**：Generator 的参数采样方法可用于网络协议的模糊测试
- **流量分类鲁棒性评估**：UPGen 生成的多样化协议可用于评估流量分类器的泛化能力
- **网络入侵检测**：DPI 工具的未识别率分析方法可用于评估 IDS 的覆盖盲区
- **隐私保护通信**：协议生成技术可用于设计难以被识别的隐私保护通信协议
- **IoT 安全**：参数化协议生成方法可用于 IoT 设备的通信协议安全分析

### 7.6 开放问题与未来研究方向

1. **流量整形整合**：如何在 UPGen 框架中整合流量整形以隐藏隧道模式？
2. **主动攻击防护**：如何增强协议以抵抗主动探测和篡改？
3. **多路复用支持**：如何在不牺牲安全性的前提下支持多连接复用？
4. **代理分发机制**：如何安全地分发代理信息到审查区域内？
5. **自适应生成**：如何根据审查者的行为动态调整协议生成策略？
6. **QUIC/UDP 支持**：当前仅支持 TCP，是否可以扩展到 UDP/QUIC？
7. **协议质量评估**：如何自动评估生成协议的"合理性"以提高穿越率？

### 7.7 对我的研究有什么启发？

1. **协议级特征的重要性**：UPGen 证明了协议结构特征（字段类型、位置、顺序）比 payload 内容更重要——这对 [[traffic-classification]] 研究有直接启示
2. **OOD 泛化是核心挑战**：分类器对训练分布外协议的失败是系统性的，这与 [[encrypted-traffic-analysis]] 中的泛化问题一致
3. **附带损害量化方法**：UPGen 的 OOD FPR 分析框架可用于评估任何封锁/检测策略的实际代价
4. **结构化 vs 随机化的权衡**：FEP 的随机化策略已被证明失败，结构化设计提供了新的思路
5. **DPI 工具的覆盖盲区**：WIDE 数据集分析表明大量真实流量无法被现有 DPI 工具识别，这对 [[tunnel-detection]] 研究有重要参考价值
6. **可编程协议系统的价值**：Proteus 等 PPS 的灵活性为快速迭代和适应性部署提供了基础设施

## 8. 总结

### 8.1 核心思想（不超过20字）

自动生成大量结构化加密协议，使审查封锁必然造成不可接受的附带损害。

### 8.2 速记版 Pipeline（3-5步）

1. 调研 27 种真实加密协议，提取 16 维参数空间
2. 概率采样生成 4.2 x 10^22 种 PSF，每个代理独立协议
3. ML 安全评估证明 OOD FPR 接近 100%（封锁不可行）
4. 性能评估证明达到/超过 Obfs4 水平
5. OpenGFW + 中国真实部署验证实际可行性

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[censorship-circumvention]] - 审查规避
- [[encrypted-traffic-analysis]] - 加密流量分析
- [[tunnel-detection]] - 隧道检测
- [[traffic-classification]] - 流量分类
- Fully Encrypted Protocol (FEP) - 全加密协议
- Collateral Damage - 附带损害
- Programmable Protocol System (PPS) - 可编程协议系统
- Out-of-Distribution Generalization - 分布外泛化

### 9.2 相关方法

- Proteus - 可编程审查规避协议系统
- Obfs4 - 全加密审查规避协议
- Deep Fingerprinting (DF) - 深度指纹 CNN 分类器
- nPrintML / AutoGluon - 自动化流量分析模型
- Shadow - 离散事件分布式系统仿真器
- OpenGFW - 开源 GFW 模拟系统

### 9.3 相关任务

- Censorship Evasion Protocol Design - 审查规避协议设计
- Traffic Analysis Resistance - 流量分析抵抗
- Protocol Fingerprinting - 协议指纹识别
- Network Censorship Measurement - 网络审查测量

### 9.4 可更新的综述页面

- [[survey-encrypted-traffic-analysis]] - 加密流量分析综述
- Censorship Circumvention Protocol Comparison
- DPI Tool Coverage Analysis

### 9.5 可加入的对比表

- Censorship Evasion Protocol Comparison (FEP vs Mimicry vs UPGen)
- DPI Tool Protocol Recognition Rates
- ML Classifier OOD Performance Comparison

## 10. 证据记录（表格形式）

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E1 | 协议空间 | UPGen 可生成 4.2 x 10^22 种不同协议，总熵 38.4 bits | Table 1 |
| E2 | 协议空间 | 排除子协议模式后仍有 10^13+ 种协议 | Section 4.2 |
| E3 | ML 安全 | 所有分类器在所有 OOD 场景中 FPR 接近 100% | Table 3 |
| E4 | ML 安全 | SSH+DF 是唯一 OOD FPR < 89% 的组合，但 TPR 仅 0.20 | Table 3 |
| E5 | ML 安全 | Obfs4 可被 DF+Random Forest 逻辑与组合完美分类 | Section 4.3.3 |
| E6 | DPI 分析 | UPGen 93-100% 流量被 DPI 工具标记为未识别 | Table 5 |
| E7 | DPI 分析 | libprotoident 将 7% UPGen 流量误识别为 RTMP | Table 5 |
| E8 | DPI 分析 | WIDE 数据集中 Zeek 未识别 90%，nDPI 未识别 67% | Section 4.4 |
| E9 | DPI 分析 | libprotoident 未识别约 4% WIDE 流量 | Table 6 |
| E10 | DPI 分析 | 白名单策略至少产生 4% 误封率（远超 0.6% 上限） | Section 4.4 |
| E11 | 性能 | UPGen best 延迟 252ms，优于 TLS 的 313ms | Table 7 |
| E12 | 性能 | UPGen 吞吐量 3.70-4.25 Gbit/s/core | Table 7 |
| E13 | 性能 | UPGen 内存 2.25-2.88 GiB，约为 Obfs4 的一半 | Table 7 |
| E14 | 性能 | UPGen 是唯一成功维持全部 50,000 连接的协议 | Table 7 |
| E15 | 性能 | Tor Shadow 仿真显示 4 种代理协议变体性能无显著差异 | Figure 4 |
| E16 | OpenGFW | 56.2% UPGen 协议成功穿越 OpenGFW FET 分析器 | Section 6 |
| E17 | OpenGFW | 仅 0.4% Obfs4 配置成功穿越 OpenGFW | Section 6 |
| E18 | OpenGFW | 问候字符串协议（25% 概率生成）全部通过 OpenGFW | Section 6 |
| E19 | 真实部署 | 中国两周部署测试中 Obfs4 和 UPGen 均未被封锁 | Section 6 |
| E20 | 设计基础 | 分析了 27 种真实加密协议（21 种开放设计） | Section 2.4, Table 8 |
| E21 | 密码学 | 使用 ChaCha20-Poly1305 实际加密，Curve25519 密钥交换 | Section 2.4 |
| E22 | 密码学 | 长期对称密钥 + 临时密钥 + KDF 提供前向保密 | Section 4.1 |
| E23 | 威胁模型 | 安全目标：U 与 P\Q 不可区分，其中 P 是所有良性协议，Q 是已知子集 | Section 2.1 |
| E24 | 威胁模型 | 设计针对被动审查者；对主动扫描提供部分保护 | Section 2.1 |
| E25 | 实现 | Generator: ~2000 行 Python 3；Proteus 扩展: ~1000 行 Rust | Section 3 |
| E26 | 实现 | 流量生成软件: ~9000 行 C++/Rust/Python | Section 4.3.1 |
| E27 | 数据收集 | 每协议 1000 traces；UPGen: 1000 PSF x 5 + 2500 PSF x 2 | Section 4.3.1 |

## 11. 原始资料链接

- 论文发表于 USENIX Security 2025，2025 年 8 月 13-15 日，西雅图
- 作者单位：
  - Ryan Wails: U.S. Naval Research Laboratory & Georgetown University
  - Rob Jansen, Aaron Johnson: U.S. Naval Research Laboratory
  - Micah Sherr: Georgetown University
- 开源代码：
  - UPGen 生成器：https://github.com/unblockable/upgen
  - 扩展版 Proteus v0.2.0：https://github.com/unblockable/proteus
  - Zenodo 全部工件：https://doi.org/10.5281/zenodo.15491977
- 资助：Office of Naval Research (ONR), DARPA (FA8750-19-C-0500), Georgetown University

## 12. 后续问题

1. **对抗自适应审查者**：如果审查者也使用 ML 来学习 UPGen 的分布特征，安全性如何变化？
2. **协议质量优化**：如何提高生成协议的 OpenGFW 穿越率（从 56.2% 提升到更高）？
3. **与流量整形的结合**：UPGen + 流量整形的组合能否同时解决协议级和流量模式级的检测？
4. **大规模部署挑战**：在 Tor 网络中大规模部署 UPGen 需要解决哪些工程和协调问题？
5. **主动探测防护**：如何增强 UPGen 协议以抵抗主动探测（当前设计仅针对被动审查者）？
6. **协议更新策略**：当部分协议被封锁时，最优的协议更新和分发策略是什么？
7. **与其他规避技术的组合**：UPGen 是否可以与 Snowflake、meek 等其他规避技术互补？

## 13. 与研究组方向的关联

本文与 [[traffic-classification]] 和 [[encrypted-traffic-analysis]] 研究方向的关联：

1. **对流量分类器的挑战**：UPGen 生成的 4.2 x 10^22 种协议构成了对现有流量分类器的极端压力测试——分类器必须对训练分布外的协议保持泛化能力
2. **OOD 泛化的核心问题**：UPGen 的安全论证本质上依赖于分类器的 OOD 泛化失败，这与流量分类领域的泛化挑战一致
3. **协议指纹识别**：UPGen 的参数空间分析（Table 1）揭示了哪些协议特征具有最高的区分度（子协议模式 8.3 bits，证书 6.5 bits），对协议指纹识别研究有参考价值
4. **DPI 工具的局限性**：WIDE 数据集分析表明现有 DPI 工具存在大量覆盖盲区，这对 [[tunnel-detection]] 和恶意流量检测研究有重要启示
5. **审查与反审查的军备竞赛**：UPGen 代表了审查规避领域从"模仿已知协议"到"生成未知协议"的范式转变，可能推动审查技术的相应演进

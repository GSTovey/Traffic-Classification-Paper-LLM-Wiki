---
type: paper
title_original: "Crypto Wars in Secure Messaging: Covert Channels in Signal Despite Leaked Keys"
title_cn: "安全通信中的加密战争：密钥泄露下的 Signal 隐蔽信道"
authors: [Rosario Giustolisi, Gabriele Lenzini, Chuanwei Lin, Mohammadamin Rakeei, Andy Rupp]
year: 2026
venue: "USENIX Security 2026"
doi: "unknown"
url: "https://www.usenix.org/conference/usenixsecurity26/presentation/giustolisi"
pdf: "00-inbox/PDFs/2026-USENIX-Crypto_Wars_in_Secure_Messaging__Covert_Channels_in_Signal_Despite_Leaked_Keys.pdf"
mineru_md: "02-parsed-markdown/2026-USENIX-Crypto_Wars_in_Secure_Messaging__Covert_Channels_in_Signal_Despite_Leaked_Keys.md"
status: deep-analyzed
reading_level: L3
research_area: ["censorship-circumvention", "secure messaging", "anamorphic encryption"]
task: ["covert-channel construction", "key-disclosure resilience", "protocol performance evaluation"]
method: ["DH-ratchet embedding", "MAC-tag embedding", "transcript indistinguishability", "transcript binding"]
dataset: ["Signal-Android implementation", "libSignal Rust/Java/Kotlin implementation", "Android 14 device and emulator benchmarks"]
code: "https://doi.org/10.5281/zenodo.20425141"
relevance: medium
created: "2026-09-19"
updated: "2026-10-10"
---

## 0. 论文基础信息

> **L3 深度分析笔记**：基于正文 §1–§7、Table 1、Table 3、算法 1–10、Ethical Considerations 与 Open Science 章节交叉核对。安全结论是条件性的：每条信道只在对应的密钥披露模式、double key 假设和密码学安全假设下成立。

| 项目 | 内容 |
|---|---|
| 标题（原文） | Crypto Wars in Secure Messaging: Covert Channels in Signal Despite Leaked Keys |
| 标题（中文） | 安全通信中的加密战争：密钥泄露下的 Signal 隐蔽信道 |
| 作者 | Rosario Giustolisi, Gabriele Lenzini, Chuanwei Lin, Mohammadamin Rakeei, Andy Rupp |
| 单位 | IT University of Copenhagen（Giustolisi）；University of Luxembourg（Lenzini、Lin、Rakeei、Rupp）；Karlsruhe Institute of Technology（Lin）；KASTEL Security Research Labs（Rupp） |
| 发表年份 | 2026 |
| 发表会议 | USENIX Security 2026（第 35 届 USENIX Security Symposium，2026-08-12~14，Baltimore） |
| 论文类型 | 密码协议构造 + 真实实现与性能评测（anamorphic encryption 在 Signal Double Ratchet 上的落地） |
| 研究领域 | 抗审查/隐蔽通信（censorship-circumvention）；密钥泄露与合法访问（lawful access）威胁下的可否认/隐蔽通信 |
| 代码 / artifact | Zenodo software artifact：https://doi.org/10.5281/zenodo.20425141 ；完整版见 Cryptology ePrint Archive 2025/2172（非 arXiv，故不入 arxiv_id） |
| 数据集 | 无（实验对象为官方 Signal-Android 客户端与 libSignal 库） |
| DOI | unknown（解析稿未给出论文 DOI；Zenodo 为 artifact DOI，非论文 DOI） |
| PDF | 00-inbox/PDFs/2026-USENIX-Crypto_Wars_in_Secure_Messaging__Covert_Channels_in_Signal_Despite_Leaked_Keys.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-USENIX-Crypto_Wars_in_Secure_Messaging__Covert_Channels_in_Signal_Despite_Leaked_Keys.md |

> ⚠️ MinerU 解析问题：算法块（Algorithm 1-10）以 `<div class="mineru-algorithm">` 包裹，出现 HTML 实体、下标碎裂（`mac_{key}`、`$\mathsf{...}$` 混排）与步骤编号错位；部分节标题/术语为 small-caps 字体，解析稿中出现 `I<sub>n</sub>t<sub>ro</sub>d<sub>uc</sub>ti<sub>on</sub>` 型下标碎片（引用时已还原为正常文字）；Table 3 的列标题跨行合并，需结合正文与图 4/5 交叉核对。

## 1. 一句话总结

论文把 anamorphic encryption 首次落地到已部署的 E2EE 协议中：在 Signal 的 Double Ratchet 上构造两条隐蔽信道——把隐蔽消息嵌入非对称 ratchet 的 DH 公钥（需额外 double key，可抵抗全部状态泄露）或嵌入对称 ratchet 的 MAC 认证标签（无需预共享密钥，在仅泄露 root key 或 DH 私钥之一时可抵抗），分别以每次 ratchet 步进 32 bit、每条消息 64 bit 的速率隐蔽传输。

## 2. 摘要翻译

### 2.1 摘要原文（节选）

> End-to-end encryption (E2EE) is the foundation of modern secure messaging, with the Signal protocol as the de facto standard... At the same time, the deployment of E2EE has led to growing pressure from authorities to decrypt user traffic under law enforcement. This raises a critical question: if an adversary can routinely decrypt Signal messages (for example via a mandated access or a leaked key), can users still communicate securely and covertly? We address this question through the lens of anamorphic encryption... We design two constructions that embed covert channels into the existing Signal Double Ratchet protocol. Concretely, we show how to embed covert messages (i) into Diffie-Hellman keys used in the asymmetric ratchet, or (ii) into authentication tags produced in the symmetric ratchet... We formalize security in threat models that capture adversaries with decryption capabilities granted through lawful access mechanisms, and prove that the resulting protocol transcripts are indistinguishable from those of standard Signal. We implement our constructions in the official Signal library and Android client, and show that they incur low overhead and are practical in real-world settings.

### 2.2 摘要中文翻译

端到端加密（E2EE）是现代安全通信的基石，而 Signal 协议已是 Signal、WhatsApp、Facebook Messenger、Google Messages 等应用的事实标准。与此同时，E2EE 的部署招致当局越来越大的压力，要求在执法名义下解密用户流量。这引出一个关键问题：如果敌手（例如通过强制访问机制或泄露的密钥）能够常规性地解密 Signal 消息，用户是否仍能安全且隐蔽地通信？我们从 anamorphic encryption（变形加密）的视角回答该问题——它允许在看似正常的密文中传递隐藏消息，即便面对能解密这些密文的敌手。我们设计了两种构造，把隐蔽信道嵌入既有的 Signal Double Ratchet 协议：(i) 把隐蔽消息嵌入非对称 ratchet 使用的 Diffie-Hellman 密钥中；(ii) 把隐蔽消息嵌入对称 ratchet 产生的认证标签（MAC）中。我们的技术兼容既有的 Signal 类部署，且无需服务提供商做任何改动。我们在刻画"经合法访问机制获得解密能力的敌手"的威胁模型下形式化安全，并证明所得协议转录与标准 Signal 不可区分。我们在官方 Signal 库与 Android 客户端中实现了两种构造，显示其开销低、在真实环境中可行。结果表明：即便常规 E2EE 保障已被削弱，隐蔽通信信道仍可存续。

## 3. 方法动机

1. **E2EE 面临的政治压力**：欧盟、英国、瑞典、澳大利亚的提案要求提供商通过密钥托管、客户端扫描或其他技术手段实现解密；Signal 表示宁愿退出某些市场。对记者与线人、活动人士、律师与客户、家暴受害者等群体，"若敌手能解密你的消息，是否还有任何可以私密传递的内容"成为实际问题。
2. **anamorphic encryption 与封面媒介隐写的区别**：隐写（steganography）依赖可用的封面分布（图像/音频），在净化、过滤、审查环境下封面可得性与鲁棒性会成为瓶颈；anamorphic encryption 在密码协议内部运作，敌手可以解密公开通信并检查协议值，因此隐蔽信道必须在**密码学检查**下依然不可见。
3. **既有理论未落地**：anamorphic encryption 理论已有大量工作，但此前**没有任何实现在广泛部署的消息协议内部落地**。
4. **Signal 带来的协议特定挑战**：Signal 不是一次加密调用——Double Ratchet 随时间演化状态、混合非对称与对称步骤、且在丢包与乱序下仍须正确；协议消息同时携带 DH 公钥、密文、认证标签等多种密码值，隐蔽信道必须融入**整个转录**而非单个原语。此外不同监控机制揭示的密钥材料子集不同，需要匹配不同披露模式的构造。

### 3.5 科学假设形成

| 假设 | 具体内容 | 验证方式 | 结果 |
|---|---|---|---|
| H1 | Double Ratchet 中的 DH 公钥可以承载隐蔽消息，同时对掌握普通解密所需状态但没有 double key 的敌手保持标准分布 | fakeKeygen/aDec 构造、PRF 混合证明与 Signal 实现 | 支持：DH-based Sym-DH/Asym-DH 在 full-state disclosure 下实现转录不可区分；前提是 double key 未泄露 |
| H2 | MAC key 由 root key 与 DH 输出共同派生，因此只泄露其中一侧时，MAC 标签可承载隐蔽消息且无需预共享密钥 | Sym-MAC 的部分披露模型、MAC 伪随机性证明 | 支持：root key 或 DH 私钥二选一泄露时可保持隐蔽；同时泄露或泄露 mac key 即失效 |
| H3 | transcript binding 可把被动不可区分性提升到面对注入/重放/修改的 CCA-style 保证 | 额外 carrier + 第 ℓ+1 个 PRF transcript tag 的构造与安全论证 | 条件支持：依赖 PRF/MAC 安全和未泄露的下一步 mac key；完整形式化证明在 full version |
| H4 | 这些构造可在官方 Signal 客户端中以可接受开销运行 | Signal-Android/libSignal 实现、真实设备/模拟器 Table 3 | 支持但有权衡：Sym-MAC 接近基线；优化 DH 约 7× 解密开销；基础 DH 16-bit 需数百毫秒 |

## 4. 方法设计

### 4.1 威胁模型：两类密钥披露（§1.2, §3）

| 披露模式 | 敌手掌握 | 对应用户场景 | 本文对应构造 |
|---|---|---|---|
| 全部状态披露（full state disclosure） | 完整 Double Ratchet 状态：root key、DH 私钥、chain keys、派生的消息密钥 | 大范围密钥披露立法、设备取证、法院命令强制交出设备凭证 | **DH-based channel**（前提是双方另行建立了未通过同一监控机制获得的 double key） |
| 部分状态披露（partial state disclosure） | 只拿到 root key 材料**或**只拿到后续 ratchet 步骤的临时 DH 私钥（而非两者） | 法律框架只授权访问消息内容、取证工具只能提取部分密钥、记录全部临时值成本过高、备份不完整 | **MAC-based channel**（不需任何预共享 double key） |

- **double key 的建立**：对称变体需双方事先共享 double key（可面对面交换口令/QR/NFC、由监控发生前的共同历史派生、或其他信道一次性引导）；非对称变体只需接收方持有 double secret key 并**公开发布**对应的 double 公钥（如记者在个人网站发布），任何发送方即可在无事先协调下发起隐蔽通信。
- **范围与非目标**：不保护元数据（通信关系、时序、频率）；基础构造针对对消息投递被动的监控，transcript-binding 变体针对可注入/重放/修改/重排的主动敌手；不解决破坏端点的主动 MITM。
- **隐蔽带宽**：优化后的 DH 信道每 ratchet 步进 32 bit，MAC 信道每条消息 64 bit——足以传短敏感内容（标识符、坐标、状态标志）或引导一条独立安全信道，不足以大批量传输。

### 4.2 两条构造（§1.1, §4, §5）

| 构造 | 承载位置 | 隐蔽容量 | double key | 抵抗的披露模式 |
|---|---|---|---|---|
| DH-based（对称变体，Sym-DH） | 非对称 ratchet 中生成的 DH 公钥 | 每次 DH ratchet 步进 32 bit（经查表优化） | 需双方预共享 double key | 全部状态披露（只要 double key 未被同一机制获取） |
| DH-based（非对称变体，Asym-DH） | 同上 | 同上 | 仅接收方持 double secret key，公钥可公开 | 同上，且发送方无需事先协调 |
| MAC-based（Sym-MAC） | 对称 ratchet 产生的 MAC 认证标签 | 每条消息最多 MAC 长度（实现中为 64 bit） | 不需要 | 部分状态披露（root key 与 DH 私钥只泄露其一，MAC key 仍不可导出） |

- **DH-based 的核心性质**：产生的公钥即便对"已掌握足以解密普通消息的 Double Ratchet 秘密"的敌手也**计算不可区分**于诚实生成的公钥；隐蔽接收方用 double key 恢复隐蔽消息。
- **MAC-based 的核心洞察**：Signal 的每条消息 MAC key 由 root key 与 DH 输出**共同**派生；敌手只掌握其中一侧时 MAC key 不可导出，因此认证标签可安全承载隐蔽消息，且无需预共享密钥。
- **安全形式化**：以"转录不可区分性"（transcript indistinguishability）定义 anamorphic 安全——掌握被披露密钥材料的敌手无法区分 anamorphic 执行与标准 Signal 执行；两条构造均证明满足该定义。进一步加入 **transcript binding** 得到 IND-CCA2 式安全（第 ℓ+1 个标签用 PRF(mac_key_{ℓ+1}, 转录值) 计算，敌手须伪造新 PRF 输出才可能通过验证），以抵抗主动敌手。

### 4.3 工程优化

- **X25519 + Edwards-Montgomery 映射**：DH 信道在 X25519 上实例化；朴素提取需在消息空间做穷举搜索，很快变得不可行。
- **查找表优化**：用"一次群运算 + 一次查表"替代在线穷举搜索，使 32-bit 隐蔽消息/ratchet 步进变得实用。查表在 Intel Xeon Gold 6248R（3 GHz、96 核、800 GB RAM）上离线生成：16-bit 表几秒生成、占 2.3 MB；32-bit 表约 50 分钟生成、占 144 GB。表只需算一次，且实现支持**远程查表服务**，客户端可不本地存储。
- **实现**：以 Rust、Java、Kotlin 在官方 Signal 应用与 libSignal（官方客户端使用的平台无关库，主要为 Rust）中实现原型；PRF 在 Sym-DH 与 Asym-DH 中用 HMAC-SHA256 实例化。
- **时序侧信道**：论文额外测量接收方 round-trip 延迟（从收到消息到发出投递回执），因该延迟可能向服务器泄露"消息是否 anamorphic"；缓解手段包括固定延迟发送回执，以及发送方以长于最坏情况 RTT 的间隔发送（真实设备约 1600 ms、模拟器约 1000 ms）。

### 4.4 证据分层与安全边界

- **形式化层**：论文给出 anamorphic security 定义，把 anamorphic target component 与 standard target component 的区分优势限制为可忽略量；DH target 是 ratchet public key，MAC target 是认证标签。transcript-binding 变体提供 CCA-style 目标，但全文证明细节在 ePrint full version。
- **构造层**：DH 信道的前提是双 key 未被同一访问机制获取；Sym-DH 需 out-of-band PSK，Asym-DH 把接收方 double public key 公开。MAC 信道无需 double key，但只容忍 root key 或 DH 私钥一侧泄露。
- **实现层**：官方 Signal-Android 和 libSignal 只验证功能和性能，不等于真实 Signal 服务部署或所有平台实现均已具备安全 API。
- **观测层**：论文测量加密/解密/回执时延，不能由此证明在所有网络条件下统计不可检测，也不能推出隐蔽信道提供元数据保护或前向保密。

## 5. 与其他方法对比

| 维度 | 本文（协议内 anamorphic 信道） | 封面媒介隐写（cover-media steganography） | 可否认加密 / 可否认消息层（如 Wink） |
|---|---|---|---|
| 载体 | Signal Double Ratchet 协议内部值（DH 公钥、MAC 标签） | 图像/音频/文本等外部封面对象 | 随机数（盐、IV）等应用线格式内字段 |
| 是否需封面分布 | 否 | 是（净化/过滤下封面可得性与鲁棒性是瓶颈） | 否 |
| 敌手能力 | 可解密公开消息、检查协议值（含全部状态披露） | 通常只观察信道 | 部分设备被攻陷/强制披露 |
| 需预共享秘密 | DH 变体需要 double key；MAC 变体不需要 | 通常需要共享密钥 | 需要 |
| 带宽 | 32 bit/ratchet 步进 或 64 bit/消息 | 视封面容量，通常较高 | 受随机数字段长度限制 |
| 落地证据 | 官方 Signal 库/Android 客户端实测（本文） | 多为实验室评测 | TrustZone 实现 |

论文未与本库的流量分类方法构成直接可比关系（本文关注协议内部隐蔽信道，而非流量侧的识别与分类），故不做跨域对比。

## 6. 实验表现与优势

### 6.1 实验环境（§6）

| 项 | 设置 |
|---|---|
| 真实设备 | Android 14，Qualcomm Snapdragon 888，8 GB RAM |
| 模拟器 | Android Studio 模拟器，宿主为 2023 MacBook Pro（M2 Pro，16 GB RAM） |
| 查表生成 | Intel Xeon Gold 6248R 3 GHz，96 核，800 GB RAM |
| 实现范围 | 官方 Signal-Android 客户端 + libSignal（Rust/Java/Kotlin）；无服务器改动 |

### 6.2 性能结果（Table 3，单位 ms）

| 环境 | 构造 | 隐蔽长度 | 解密 Avg | 解密 Worst | Round-trip Avg | Round-trip Worst | libSignal 解密 Avg |
|---|---|---|---|---|---|---|---|
| 真实设备 | Original（无隐蔽内容） | — | 1.56 | — | 20.5 | — | 1.42 |
| 真实设备 | Base (A)Sym-DH | 16-bit | 822.8 | 1622.2 | 841.48 | 1673.28 | 811.34 |
| 真实设备 | Sym-MAC | 64-bit | 1.57 | — | 20.6 | — | 1.40 |
| 模拟器 | Original | — | 1.50 | — | 120.10 | — | 1.11 |
| 模拟器 | Base (A)Sym-DH | 16-bit | 438.2 | 888.2 | 567.3 | 1010.2 | 440.3 |
| 模拟器 | Optimized (A)Sym-DH | 16-bit | 7.01 | 14.12 | 149.96 | 150.14 | 5.77 |
| 模拟器 | Optimized (A)Sym-DH | 32-bit | 7.22 | 65.10 | 150.32 | 200.18 | 5.43 |
| 模拟器 | Sym-MAC | 64-bit | 1.51 | — | 120.15 | — | 1.12 |

> ⚠️ MinerU 解析问题：Table 3 的表头跨列合并（Signal-Android 与 libSignal 分块）在解析稿中以嵌套 `<td>` 呈现，列归属需按正文 §6 核对；单位（ms）取自表标题。

### 6.3 结论要点

- **加密耗时不受影响**：真实设备上原版 Signal 加密约 1.53 ms，各 anamorphic 构造加密时间几乎相同，与隐蔽消息长度无关。
- **解密耗时取决于构造**：优化后的 (A)Sym-DH 避免在线穷举离散对数搜索，**仅约 7× 解密开销**，且用户可见的 round-trip 时间接近基线；基础 (A)Sym-DH 因需多次标量乘法搜索至多 16 bit，显著慢于原版，仅适合无法维护查找表的场景。
- **Sym-MAC 最高效**（加解密与 round-trip 均接近基线）但支持的威胁模型最弱；优化 (A)Sym-DH 支持的威胁模型最强，性能与原始 Signal 同数量级。
- 论文自述这是**anamorphic encryption 在已部署 E2EE 协议中的首个实用实例**（"the first practical instantiation of anamorphic encryption within a deployed E2EE protocol"）。

### 6.4 实验设置、指标与局限

- **实现**：Rust、Java、Kotlin 改造官方 Signal-Android 与平台无关的 libSignal；PRF 在 Sym-DH/Asym-DH 中用 HMAC-SHA256。
- **设备**：Android 14、Snapdragon 888、8 GB RAM；Android Studio 模拟器（2023 MacBook Pro M2 Pro、16 GB RAM）；查表在 Xeon Gold 6248R（96 核、800 GB RAM）生成。
- **变量**：构造类型（Original/Base/Optimized (A)Sym-DH/Sym-MAC）、隐蔽长度（16/32/64 bit）、Signal-Android 与 libSignal、真实设备与模拟器。
- **指标**：加密平均耗时、解密平均/最坏耗时、Signal-Android round-trip 平均/最坏耗时、查表构建时间/空间；论文没有用户研究、真实 Signal 服务器测试或跨硬件统计置信区间。
- **性能边界**：32-bit 查表约 144 GB；基础 DH 的在线离散对数搜索在真实设备约 822.8 ms 平均、1,622.2 ms 最坏；优化 DH 在模拟器 32-bit 平均 7.22 ms 但最坏 65.10 ms。Sym-MAC 只在部分披露模型下安全。
- **安全边界**：双 key 暴露后可用 transcript 重算过去隐蔽内容；不保护通信关系、时序、频率；不处理主动 MITM 破坏端点认证；基础构造的主动安全需 transcript binding 版本。

## 7. 学习与应用

- **对审查规避/抗监控研究**：本文为"即便密钥被强制披露，仍可保留隐蔽通信能力"提供了具体设计范式。对高风险用户（记者、活动人士）有直接应用价值，尤其是 MAC 变体不需要任何预共享秘密即可工作。
- **对流量分析研究**：隐蔽内容完全承载于协议内部密码值（DH 公钥、MAC 标签），包层长度/时序几乎无变化——除非利用 round-trip 解密延迟这类**侧信道**。这提示：面对"协议内隐蔽信道"，流量侧检测（包长/时序/频率）能力有限，检测方需要考虑**终端侧时序侧信道**与统计检验。该论点可作为"加密流量分析的检测边界"类讨论的证据。
- **对协议设计者**：论文揭示了 Double Ratchet 的"密钥派生分离性"（root key 与 DH 输出共同派生 MAC key）本身的隐蔽信道潜力；抗 anamorphic 的设计（ARE）成为自然的后续方向。
- **可迁移技巧**：(1) 用 double key 让隐蔽接收方可解码而公开解码方不可判别；(2) 用"一次群运算 + 查表"把指数级搜索降为常数开销；(3) 用 transcript binding（对整段转录做 PRF）把被动不可区分性升级为抗主动敌手的 IND-CCA2 式安全。

## 8. 总结

论文针对 E2EE 面临"合法访问/密钥泄露"的政治压力这一现实背景，把 anamorphic encryption 首次落地到已部署的 Signal Double Ratchet 中。两条构造分别把隐蔽消息嵌入 (i) 非对称 ratchet 的 DH 公钥（分对称与非对称 double-key 变体，可抵抗全部状态披露）与 (ii) 对称 ratchet 的 MAC 认证标签（无需预共享密钥，只要 root key 与 DH 私钥不同时泄露即可）。论文以转录不可区分性形式化安全并证明，进一步用 transcript binding 达到 IND-CCA2 式抗主动敌手安全。在官方 Signal 库与 Android 客户端上的实测显示：优化后 DH 信道约 7× 解密开销（模拟器 16-bit 7.01 ms / 32-bit 7.22 ms），MAC 信道开销可忽略（1.51 ms，64 bit/消息），加密耗时不受影响。

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[censorship-circumvention]] — 本文属于抗监控/抗审查的密码学路线（anamorphic encryption 作为"自我抗审查"性质的一种实现）。

### 9.2 相关方法

- 本库方法白名单（transformer / cnn / gcn / contrastive-learning / few-shot-learning / metric-learning / autoencoder / llm）均为机器学习方法，与本文的密码协议构造方法无对应，故不链接。

### 9.3 相关任务

- 本库任务白名单（website-fingerprinting / encrypted-traffic-classification / malicious-traffic-detection 等）针对流量分析任务，本文属于隐蔽信道构造，无对应任务页，故不链接。

### 9.4 相关综述

- 白名单综述页（`survey-encrypted-traffic-analysis`、`survey-few-shot-learning`、`survey-malicious-traffic-detection`、`survey-traffic-foundation-model`、`survey-website-fingerprinting`）均聚焦流量分析方法与任务，不覆盖 anamorphic encryption/隐蔽信道，故本节不链接。

### 9.5 对比表

- `method-comparison-table`：本文提出的是密码学隐蔽信道构造而非机器学习方法，与该表覆盖范围不符，故不链接。
- `dataset-comparison-table`：本文未使用或发布公开数据集，故不链接。
- `open-source-registry`：本文提供 Zenodo artifact（官方 Signal 库改造实现），但该登记页面向流量分析工具，不在其覆盖范围，故不链接。

### 9.6 相关研究前沿

- 本库 6 条研究前沿（`multimodal-fusion-strategy`、`payload-learnability`、`pretraining-necessity`、`representation-vs-shallow`、`tokenization-optimal`、`wf-attack-defense-limit`）均围绕加密流量分析，与本文主题无对应，故不链接。

### 9.7 相关论文笔记

- 本论文参考文献中未出现 kb_reference A 表内的 171 篇论文，故不建立论文间 wikilink。

## 10. 证据记录

| 编号 | 论断 | 证据位置 |
|---|---|---|
| E1 | 两条构造：DH 公钥信道（非对称 ratchet）与 MAC 标签信道（对称 ratchet） | 摘要;§1.1 |
| E2 | DH 信道产生的公钥对"已掌握解密所需 Double Ratchet 秘密"的敌手仍计算不可区分；需额外 double key（对称变体预共享，非对称变体仅接收方持私钥并公开公钥） | §1.1, §1.2, §4 |
| E3 | MAC 信道无需预共享密钥；只要敌手不能同时掌握 root key 与 DH 私钥，MAC key 即不可导出 | §1.2, §5 |
| E4 | 隐蔽带宽：优化 DH 信道 32 bit/ratchet 步进；MAC 信道 64 bit/消息（受 MAC 长度限制） | §1.2 Covert bandwidth;§1.1 |
| E5 | 查找表：16-bit 表几秒生成、2.3 MB；32-bit 表约 50 分钟、144 GB；在 Xeon Gold 6248R（96 核/800 GB）上生成；支持远程查表 | §6 |
| E6 | 性能（真实设备）：Original 解密 1.56 ms / round-trip 20.5 ms；Base (A)Sym-DH 16-bit 解密 822.8 ms（worst 1622.2）；Sym-MAC 64-bit 解密 1.57 ms | §6, Table 3 |
| E7 | 性能（模拟器）：Optimized (A)Sym-DH 16-bit 7.01/14.12 ms；32-bit 7.22/65.10 ms；Sym-MAC 1.51 ms；优化后"仅约 7× 解密开销" | §6, Table 3 |
| E8 | 加密耗时不随隐蔽内容变化（真实设备基线约 1.53 ms）；round-trip 仅在基础 (A)Sym-DH 下显著升高 | §6 |
| E9 | transcript binding：第 ℓ+1 个标签为 PRF(mac_key_{ℓ+1}, T)，达到抗主动敌手的 IND-CCA2 式安全；ℓ 条 anamorphic 消息嵌在 ℓ+1 条正常 Signal 消息中 | §5, Algorithm 9/10 |
| E10 | 侧信道缓解：固定延迟发送回执；发送间隔需长于最坏 round-trip（真实设备约 1600 ms、模拟器约 1000 ms） | §6 |
| E11 | 局限性：隐蔽信道无前向保密（double key 暴露后可重算验证历史隐蔽内容）；不保护元数据；仅适合短消息 | §1.2, §7 |
| E12 | artifact 公开于 Zenodo 10.5281/zenodo.20425141；完整版为 ePrint 2025/2172 | §6 脚注/参考文献 [23][24] |

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-USENIX-Crypto_Wars_in_Secure_Messaging__Covert_Channels_in_Signal_Despite_Leaked_Keys.pdf
- MinerU Markdown：02-parsed-markdown/2026-USENIX-Crypto_Wars_in_Secure_Messaging__Covert_Channels_in_Signal_Despite_Leaked_Keys.md

## 12. 后续问题

1. 论文的转录不可区分性是计算意义上的；对**统计检测器**（如对 DH 公钥分布做检验）而言，其不可区分性需要多少样本才能被打破？解析稿未给出不可区分性的实验测量。
2. 32-bit 查找表 144 GB 且需一次性生成——论文提出远程查表服务，但该服务本身会成为新的可观测点/单点依赖，其安全性与可用性权衡未展开。
3. 隐蔽信道不提供前向保密；论文提到可用 KDF 链派生 per-message double key，但未实现或评估该方向的成本。
4. 时序侧信道仅通过固定延迟缓解；在延迟抖动较大的移动网络下，该缓解是否足以抵抗统计判别？
5. 若成为现实检测目标：流量分析方能否通过 round-trip 时序特征区分启用 anamorphic 信道的会话？这是本库（加密流量分析）与本文最直接的交汇点。

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

论文从“解密能力是否等于通信可控”这一政策问题出发：如果监管者或服务器拿到了足以解密普通 Signal 消息的密钥，用户是否仍能传递不被发现的信息？作者先指出外部封面隐写在净化和审查下不稳，再把 anamorphic encryption 的不可区分性嵌入 Signal Double Ratchet 的两个密码值。转折点是按披露状态拆构造：full-state 下用额外 double key 伪装 DH 公钥，partial-state 下利用 root key 与 DH 输出的派生分离承载 MAC 标签。证明负责回答“看不见”，transcript binding 负责回答“主动篡改也不能伪造”，实现和性能实验则回答“能否运行”。最后作者明确把低带宽、无前向保密、元数据暴露和查表成本写成部署边界。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract/Introduction | 将合法访问与用户隐蔽通信的冲突具体化 | 问题与意义 | “可解密”不等于“可检测” |
| Background/Related Work | 解释 Double Ratchet 与 anamorphic encryption 的接口 | 技术语境 | 从外部封面转向协议内部载体 |
| System Model | 按 full/partial disclosure 分配构造 | 威胁模型锚定 | 同一信道不能覆盖所有泄露模式 |
| DH Construction | 用 PRF+DH 公钥承载消息，随后加入 transcript binding | 强威胁模型方案 | Asym-DH 取消发送方预协调 |
| MAC Construction | 利用 MAC key 的派生分离，无需 PSK | 低成本方案 | 安全性换取部分泄露模型 |
| Performance | 将群运算/离散对数搜索转成实际设备时延 | 工程可行性 | 查表把 16/32-bit 降到约 7 ms 量级 |
| Discussion/Conclusion | 明确前向保密、元数据和 ARE 方向 | 边界收束 | 协议内隐蔽性是条件性质而非普遍保证 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 应用缺口 | anamorphic encryption 理论多，已部署 E2EE 落地少 | 选择 Signal Double Ratchet 作为真实协议承载 | §1, Related Work |
| 威胁缺口 | 密钥泄露不是单一模型，full 与 partial 暴露能力不同 | Table 1 对构造和泄露材料逐格区分 | §3.3 |
| 密码值缺口 | 公开 DH key 与认证标签都可能承载隐蔽内容，但安全条件不同 | DH/ MAC 两条独立证明路线 | §4–5 |
| 工程缺口 | 理论构造可能需要大规模离散对数搜索 | 查表优化、远程查询与时序测量 | §4.4, §6 |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 真实设备基线 | 给出普通 Signal 加解密与 round-trip 参照 | 让开销结论可比较 |
| Base DH | 展示在线离散对数搜索的实际代价 | 证明朴素构造不适合部署 |
| Optimized DH | 展示查表对 16/32-bit 的加速 | 支撑强威胁模型下的可行性 |
| Sym-MAC | 验证 64-bit 隐蔽标签接近基线 | 支撑弱泄露模型的低成本方案 |
| 时序讨论 | 将解密开销转化为可能的检测侧信道 | 提醒“不可区分”需要实现和调度边界 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 问题入口 | 用政策场景而非单一算法缺陷提出问题 | 先明确敌手新增能力，再问安全性是否仍有残余 |
| 构造组织 | 同一协议内按威胁模型拆成两条构造 | 将不同泄露边界写成独立设计选择 |
| 证明与实现 | 先给不可区分性，再给查表、设备和时延数据 | 把“安全成立”和“可运行”分别证成 |
| 局限表达 | 主动写明 double key 暴露、元数据、带宽和前向保密 | 对隐蔽通信结论同时给出可检测侧信道边界 |

## 14. 证据边界与复现清单

1. **安全证明边界**：DH/MAC 的不可区分性在给定 key-disclosure、PRF/MAC 假设和 double key 条件下成立；不要把它表述为任意密钥泄露或任意主动 MITM 下的普遍安全。
2. **主动安全边界**：基础构造针对被动敌手；transcript-binding 版本需要额外 carrier 和最后一个 PRF tag，完整游戏证明在 ePrint full version。
3. **工程证据**：官方客户端和 libSignal 的实验只说明测量设备/版本上的功能与开销；144 GB 查表、远程查表服务和固定回执策略会引入部署依赖。
4. **检测边界**：论文没有对大样本统计检测器、流量侧分类器或真实监管部署做评估；“转录不可区分”不能替代对时序、元数据和实现泄漏的实测。
5. **可复现材料**：Zenodo 10.5281/zenodo.20425141 与 Signal/libSignal 版本、Table 3 硬件、查表参数和构造 bit-rate 必须一起记录；论文 artifact 是复现实验用代码，不应当表述为面向终端用户的 drop-in covert messenger。

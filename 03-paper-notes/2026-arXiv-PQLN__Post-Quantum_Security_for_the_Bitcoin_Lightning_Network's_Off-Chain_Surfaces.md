---
type: paper
title_original: "PQLN: Post-Quantum Security for the Bitcoin Lightning Network's Off-Chain Surfaces"
title_cn: "PQLN：比特币闪电网络链下表面的后量子安全"
authors: ["Ahmet Kurt", "Abdul-Salem Beibitkhan", "Yacoub Hanna", "Abdullah Aydeger"]
year: 2026
venue: "arXiv 2026"
doi: "unknown"
url: "https://arxiv.org/abs/2609.13781"
pdf: "00-inbox/PDFs/2026-arXiv-PQLN__Post-Quantum_Security_for_the_Bitcoin_Lightning_Network's_Off-Chain_Surfaces.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-PQLN__Post-Quantum_Security_for_the_Bitcoin_Lightning_Network's_Off-Chain_Surfaces.md"
status: processed
reading_level: L1
research_area: []
task: []
method: []
dataset: []
code: "unknown"
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

# PQLN: Post-Quantum Security for the Bitcoin Lightning Network's Off-Chain Surfaces

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | PQLN: Post-Quantum Security for the Bitcoin Lightning Network's Off-Chain Surfaces |
| 中文标题 | PQLN：比特币闪电网络链下表面的后量子安全 |
| 作者 | Ahmet Kurt, Abdul-Salem Beibitkhan, Yacoub Hanna, Abdullah Aydeger（解析稿未含单位信息） |
| 年份 | 2026 |
| 会议/期刊 | arXiv 预印本（arXiv 2026；arXiv ID 2609.13781） |
| 研究方向 | 加密货币协议安全 / 后量子密码迁移（Lightning Network off-chain 协议层）。**超出 KB 白名单范围**（无区块链/密码协议类 slug），故 `research_area` / `task` / `method` 留空，§9 不建立链接 |
| 任务类型 | 系统设计与实现：为闪电网络五类链下表面（gossip、传输握手、invoice、onion、offer）做混合后量子加固，并在 rust-lightning 上实现与评估 |
| 方法关键词 | 混合保守扩展（hybrid conservative extension）、ML-DSA-44 / ML-KEM-768、FN-DSA 对照、TOFU 公钥 pin、签名分块、密文列表、BOLT 1 TLV 奇数类型兼容 |
| 数据集 | 无公开数据集；评估在 Bitcoin Core v31.1 regtest 与真实 Lightning 节点上完成 |
| 是否开源 | 论文称代码公开于 GitHub（以脚注 4 形式出现），但解析稿中无 URL，`code` 记为 unknown |
| PDF | 00-inbox/PDFs/2026-arXiv-PQLN__Post-Quantum_Security_for_the_Bitcoin_Lightning_Network's_Off-Chain_Surfaces.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-arXiv-PQLN__Post-Quantum_Security_for_the_Bitcoin_Lightning_Network's_Off-Chain_Surfaces.md |

> ⚠️ MinerU 解析问题：§I 首句被截断且 small-cap 首字母被拆为上标（"P UBLIC-KEY cryptography in use today rests on the" 后直接跳到 Shor 算法），句子成分缺失；引用该句时需回查 PDF。

## 1. 一句话总结

> PQLN 用"经典机制原样保留 + ML-DSA/ML-KEM 并置"的混合方案保护闪电网络全部链下表面（gossip 公钥分发、混合握手、invoice 签名、offer 承诺密钥、混合 onion），靠签名分块（639 B 字段）与 20 槽密文列表塞进既有消息格式；rust-lightning 实现中新增密码操作 ≤0.33 ms、每跳延迟 <60 ms，代价是 gossip 膨胀约 10×（FN-DSA 约 4×），12 个互操作场景全部通过。

## 2. 摘要翻译

### 2.1 摘要原文

"A cryptographically relevant quantum computer will break the elliptic-curve cryptography behind Bitcoin and its Lightning Network, the most widely used payment channel network. Even a post-quantum consensus upgrade of Bitcoin would not cover Lightning's off-chain surfaces, so its gossip, peer transport, invoices, payment onions, and offers need separate protection. An adversary can already record Lightning's encrypted traffic today and decrypt it once such a computer exists. Lightning can therefore move to post-quantum cryptography now, without waiting for Bitcoin, and stop such harvest-now-decrypt-later attacks along with node impersonation, invoice forgery, and payment deanonymization. In this paper, we propose PQLN, a hybrid post-quantum extension of Lightning that protects all of these surfaces with the lattice-based standards ML-DSA and ML-KEM. ... Our evaluation with real Lightning nodes shows that PQLN nodes interoperate with unmodified nodes. The added cryptographic operations take at most 0.33 milliseconds, and the main cost is communication, since gossip data grows about tenfold with ML-DSA and about fourfold with the smaller Falcon. To our knowledge, PQLN is the first post-quantum design, implementation, and evaluation for Lightning."（Abstract）

### 2.2 摘要中文翻译

一台密码学相关量子计算机将攻破比特币及其（使用最广的）支付通道网络闪电网络所依赖的椭圆曲线密码。即使比特币完成后量子共识升级，也覆盖不到闪电网络的链下表面，因此其 gossip、对等传输、invoice、支付 onion 与 offer 需要单独保护。攻击者今天就可以录下闪电网络的加密流量，等量子计算机出现后再解密。因此闪电网络可以不等比特币，现在就迁移到后量子密码，以阻止此类"先收集后解密"攻击，以及节点冒充、invoice 伪造与支付去匿名化。本文提出 PQLN——闪电网络的混合后量子扩展，用基于格的 ML-DSA 与 ML-KEM 保护上述全部表面：经 gossip 分发后量子节点身份、混合化传输握手、为 invoice 加入后量子签名、在 offer 中承诺后量子密钥、使支付 onion 混合化。由于后量子材料远大于椭圆曲线对应物，作者提出若干把它们放进闪电网络既有消息格式与大小限制的技术。论文对量子对手做了安全性分析，并在主流实现 rust-lightning 中完成实现；真实节点评估显示 PQLN 节点可与未修改节点互操作，新增密码操作至多 0.33 毫秒，主要成本在通信——gossip 数据随 ML-DSA 增长约 10 倍、随更小的 Falcon 约 4 倍。据作者所知，PQLN 是闪电网络首个后量子设计、实现与评估。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

比特币约 690 万 BTC 存放在已暴露公钥的 output 中，但基座层替换密码需共识升级且现有 PQ 提案仍处早期（§I）；闪电网络的协议栈同样全面暴露于 Shor 算法（ECDSA 认证 gossip、ECDH 派生对等连接密钥、ECDSA/Schnorr 签支付请求、每跳一个 ECDH 秘密构造 onion），而此前唯一的闪电网络量子威胁分析止步于论坛讨论、没有设计（§I、§II）。

### 3.2 现有方法的痛点和不足

- 比特币基座层迁移工作（commit-delay-reveal、BIP 360、hash-based 签名等）都停留在基座层，不触碰闪电网络（§II，Table I）。
- TLS 1.3 混合组、OpenSSH、Signal、Noise-KEM 替换等已部署迁移实践均不针对闪电网络/支付通道网络（§II）。
- PQ onion 路由工作（HybridOR、Outfox）面向 Tor 固定长度电路，不适配闪电网络定长 1300 B onion + 可变跳数（§II）。
- PQ adaptor signature 方案要在比特币能验证其签名后才能保护通道内资金，而今天不能；PQLN 保护的是基座升级碰不到的链下表面（§II）。

### 3.3 论文的研究假设或核心直觉

闪电网络的链下表面完全活在节点间消息里，因此**仅靠软件升级**即可完成后量子迁移，无需等待比特币共识变化；同时 BOLT 1 "it's ok to be odd"（未知奇数 TLV 可跳过）等扩展性规则使新旧节点能共存（§I、§III-A、§IV）。两个硬约束决定设计边界：不能改比特币共识规则（资金相关 secp256k1 密钥不动）、网络不能一次升级完（必须与 vanilla 节点互操作）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 量子威胁（Willow 逻辑量子比特、破解 256-bit ECC 资源估计下降）+ 先收集后解密策略 | §I，引 [1]–[6] |
| 痛点提炼 | 基座层 PQ 升级覆盖不到闪电网络链下表面，而链下表面同样 Shor-vulnerable | §I、Table II |
| 问题转化 | 把"如何在不动比特币、且与旧节点互操作的前提下加固五类链下表面"分解为密钥分发、握手、invoice、onion、offer 五个子问题 | §IV |
| 工程落地 | 在 rust-lightning 上实现并用真实节点评估开销、延迟与互操作 | §VI |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 混合 PQ 材料（体积远大于 ECC）可塞进闪电网络硬性大小限制并保持与 vanilla 节点互操作 | BOLT 1/9/11 扩展性规则（§III-A） | 12 个互操作场景 + 消息体积/请求长度测量（Table V、Fig. 7） |
| 辅助假设 | 新增计算开销相对网络延迟可忽略，主要成本是通信 | 每秒级/毫秒级操作对比 | Table III 计时 + Table IV 端到端延迟 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑（有边界） | 12/12 场景通过；仅 ML-DSA-44 的支付请求全部低于解析上限，ML-DSA-87 gossip 记录超 8192 B 中继预算需翻倍 | Table V、§VI-C、Fig. 7(a) |
| 辅助假设 | 支撑 | 最贵操作 ML-DSA-44 签名平均 0.33 ms（约 ECDSA 13×）；典型链路每跳 <60 ms；gossip 下载 10.2× | Table III、Table IV、§VI-D |

## 4. 方法设计

### 4.1 方法整体流程

采用混合保守扩展：经典机制全部保留，ML-DSA/ML-KEM 并置（§IV）。逐表面处理（Table II）：① gossip（BOLT 7）承载 PQ 节点密钥并 TOFU pin；② 传输（BOLT 8）在专用端口跑混合 Noise_XK 握手，不做带内协商；③ invoice（BOLT 11）加 PQ 签名；④ offer（BOLT 12）在 metadata 中承诺每 offer 一把签名密钥；⑤ onion（BOLT 4）保持 1300 B 包不变、密文放在旁边的定长列表中。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| PQ 密钥生成 | 32/64 字节种子 | 按两个 hardened BIP 32 索引从种子派生 ML-DSA 与 ML-KEM 密钥 | 节点 PQ 身份 | 无证书基础设施的密钥来源（§IV-A） |
| 密钥分发 | node_announcement | 加入 TLV 27（pk）、29（ek）、31（签名；ECDSA 覆盖整条消息防降级），首见即 pin；中继预算 1024→8192 B | 全网可验的 PQ 公钥 | 把 gossip 变成密钥分发信道（§IV-B） |
| 混合握手 | BOLT 8 连接 | 专用端口 + 两次 ML-KEM 封装，无带内协商；对照 pin/offer 承诺密钥检查降级 | 与经典字节兼容的混合会话 | 抗节点冒充与录制解密（§IV-C） |
| invoice/offer | BOLT 11/12 | 2420 B 签名按 639 B/字段分块（3 字段装 pk、4 字段装签名）；offer metadata 内嵌每 offer ML-DSA 密钥（seed=HMAC(对称 offer 密钥, nonce)） | 可验证的 PQ 支付请求 | 抗 invoice 伪造（§IV-D/E） |
| onion | update_add_htlc | 1300 B onion 不动，密文列表放奇数 TLV 字段；固定 20 槽共 21,770 B（空槽用 FIPS-203 编码的 dummy 填充），blinded 尾部再 10 槽 +10,890 B | 混合多跳支付 | 抗支付去匿名化（§IV-F） |
| feature 协商 | BOLT 9 特征位 | require_post_quantum_payments / require_post_quantum_inbound / build_post_quantum_blinded_paths | 新旧节点能力对齐 | 允许拒绝经典路由而不破坏互操作（§IV-F） |

### 4.3 模型结构或系统模块

无学习模型。系统模块：rust-lightning fork（单一 Cargo feature `post-quantum`）+ fips204 v0.4.6 / fips203 v0.4.3 crate；变体支持构建时选择参数集并用 fn-dsa v0.4.0 替换 ML-DSA（512/1024 度）；评估含 pq-ldk-sample 示例与 Bitcoin Core v31.1 regtest。

### 4.4 公式、算法和机制解释

- 混合签名合并（式 (1)）：s* = H(τ ∥ s_c ∥ K)，把经典签名与 PQ 签名绑进同一承诺，防降级剥离。
- 安全性归约（Prop. 1–5）：五类表面的保证分别归约到 ML-DSA 的 EUF-CMA 与 ML-KEM 的 IND-CCA。
- 大小适配：ML-DSA-44 签名 2420 B、公钥 1312 B；ML-KEM-768 ek 1184 B、密文 1088 B；单条 ML-KEM 密文几乎填满 1300 B onion 载荷且每跳一个，因此采用"包不动、密文并列"的定长列表设计。

### 4.5 方法优势

- 全链下、零比特币改动：资金仍由 secp256k1 保护，但五类链下表面立即获得 PQ 保护，不等基座层迁移（§I）。
- 向后兼容：vanilla 节点跳过奇数 TLV 类型即可共存，12/12 互操作场景通过（Table V）。
- 工程开销低：最贵操作 0.33 ms（ML-DSA-44 签名），典型链路每跳 <60 ms（Table III、§VI-D）。
- 若换 FN-DSA-512，gossip 成本从 10× 降到约 4×（§VI-D）。

### 4.6 方法不足

见 §6.7（局限一节）：TOFU 可被"量子计算机出现后才首次见面的对手"利用、尚无 pin 轮换；部分签名仍为经典（未宣告 BOLT 11 payee 的 invoice、invoice_request 及 refund 响应）；phantom payments 仍为经典；TLV 类型/标签/特征位均为实验性待 BOLT 流程分配；仅测 rust-lightning。

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

与比特币基座层迁移（需共识升级）不同，PQLN 只改链下消息层，纯软件升级；与 TLS/SSH/Signal 的 PQ 迁移实践不同，PQLN 面向的是无证书基础设施、消息尺寸硬约束（639 B invoice 字段、1300 B onion、65,535 B 消息上限、8192 B 中继预算）且必须与旧节点互操作的支付通道网络；与 Outfox（每跳一个 KEM 密文、只适合定长路由）不同，PQLN 保持 onion 不变、密文并列承载。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 首个闪电网络 PQ 设计+实现+评估 | 五类链下表面全覆盖，rust-lightning 实现与真实节点评估 | 高 | 是（其他支付通道网络） |
| gossip 即密钥分发 + TOFU pin | 借用现成 gossip 承载 PQ 密钥，靠 pin/offer 承诺抗降级 | 高 | 是（无 PKI 的 P2P 协议） |
| 尺寸适配手法 | 639 B 字段签名分块；1300 B onion 旁的定长 20 槽密文列表（dummy 用 FIPS-203 编码） | 中 | 是（大 PQ 材料塞进定长格式的通用工程范式） |
| 参数集系统对比 | ML-DSA 各档 + FN-DSA-512/1024，15 种配对的体积/延迟/请求长度比较 | 中 | 是（PQ 迁移的参数选择方法） |

### 5.3 适用场景

闪电网络节点软件升级（尤其希望立即防"先收集后解密"的运营方）；同样适用于其他无 PKI、有严格消息尺寸限制的 P2P 协议的后量子迁移设计。不适用于需要改比特币交易/共识语义的场景（本文明确不改）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 比特币基座层 PQ 提案 [11][16]–[18] | 保护资金 | 不覆盖链下表面；需共识升级 | 只改链下消息、无共识变更 |
| PQ 传输（TLS/SSH/Signal）[19]–[22] | 已部署 | 不针对闪电网络 | 混合 Noise_XK+BOLT 8 字节兼容 |
| PQ onion 路由（HybridOR/Outfox）[23][24] | 抗量子 onion | 只适合定长电路 | 定长 1300 B onion 不动 + 并列密文表 |
| PQ adaptor 签名 [25][26] | 保护通道资金 | 依赖比特币可验证其签名（今天不行） | 覆盖基座升级碰不到的表面 |
| 论坛分析 [13] | 提出威胁 | 无设计、无实现 | 首个完整设计+实现+评估 |

## 6. 实验表现与优势

### 6.1 实验设计和设置

rust-lightning 主分支 commit 384e0d6（2026-08）fork：约 11,000 行、52 个文件，全部置于 Cargo feature `post-quantum` 之下；关闭该 feature 时通过上游全量测试，开启时额外通过 99 个新测试（其中 36 个覆盖 §V 的攻击与拒绝路径），15 种参数配对下同样通过。硬件：16 核 Threadripper PRO 3955WX / 64 GB / Ubuntu 26.04；真实节点评估 + Bitcoin Core v31.1 regtest。

### 6.2 数据集

无数据集。评估对象为自建的真实 Lightning 节点组合（V/Q 混合）与生成的支付请求、gossip 记录。

### 6.3 Baseline

vanilla（未修改 rust-lightning）构建作为全部对比的基线；参数集维度对照 ML-DSA-44/65/87 与 FN-DSA-512/1024。

### 6.4 评价指标

① 计算开销（新增密码操作执行时间）；② 支付延迟（在付款方测的端到端时延）；③ 通信开销（消息级与网络级体积增长）；④ 互操作性（PQ 与 vanilla 节点能否任意组合共存交易）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---|---|---|---|
| 密码操作 | 耗时 | ML-DSA-44 签 327.0 µs（0.33 ms）/ 验 103.4 µs / 生成 131.4 µs | ECDSA 25.7/33.8/19.3 µs | 签名约 13× | 标准差大来自拒绝采样；ML-DSA-87 签 0.64 ms |
| 握手/onion | 附加耗时 | 握手 +180 µs（发起方）/+130 µs（响应方）；onion +55 µs/跳（发送端）、+74 µs/跳 | — | — | BOLT 12 payee 每 invoice 约 460 µs |
| 支付延迟（循环/50 ms+10 Mbit/50 ms+1 Mbit） | 端到端 ms | 1 跳 98/252/438；2 跳 193/456/818；3 跳 306/768/1213 | vanilla 113/228/278、207/418/465、297/608/651 | 典型链路 <60 ms/跳 | Table IV |
| 消息体积 | 字节增幅 | node_announcement +4928 B；channel_update +2424 B；握手 +2272/+1088 B；onion 密文表 +21,770 B；blinded 尾 +10,890 B | — | — | ML-DSA-87 记录超 8192 B 中继预算（变体翻倍）；FN-DSA-512 仅 +2759/+670 B |
| 支付请求长度 | 字符 | 发票 ~400→4286（仅签名）→6396（含 pk）；offer 416→2528→4332；refund 531→2323 | QR 上限 4296、解析上限 7089 | — | 仅 ML-DSA-44 全部请求可用、其"仅签名"发票能进 QR（余 10 字符） |
| gossip 成本 | 每通道字节 | 下载 8111 / 存储 9687（vanilla 799/1102），10.2×/8.8× | — | — | 两条 channel_update 签名记录占 4848 B；33,000 通道 ≈270 MB 下载/320 MB 图文件（FN-DSA-512 → 115/160 MB） |
| 互操作 | 场景通过数 | 12/12（S1–S12） | — | — | S11 vanilla 发送方在异步支付上 fail-closed |

### 6.6 优势最明显的场景

PQ 节点之间一至两跳的完整功能场景（S2/S3/S5/S10）：五类受保护表面全部生效，且延迟增加在典型链路下 <60 ms/跳；若网络以 FN-DSA-512 运行，gossip 成本可压到约 4×。

### 6.7 局限性

见 §4.6；作者列出的局限（§VII）：TOFU 信任模型（晚加入者可 pin 到对手密钥）、无 pin 轮换（给出两个未来方向：用旧 pin 密钥签 node_announcement 轮换、或如 Taproot 承诺脚本树般由资金密钥承诺 PQ 密钥）；部分签名仍经典（无 trusted key 的验证方）；phantom payments 仍经典；TLV/标签/特征位为实验性；仅覆盖 rust-lightning。

## 7. 学习与应用

### 7.1 是否开源？

论文称代码公开（正文以脚注 4 指向 GitHub 仓库），但解析稿中无 URL，无法登记，`code: unknown`。

### 7.2 复现关键步骤

1. fork rust-lightning（commit 384e0d6），启用 Cargo feature `post-quantum`（ML-DSA-44/ML-KEM-768 默认）。
2. 实现五个表面：gossip TLV 27/29/31 + TOFU pin、BOLT 8 混合握手（专用端口）、BOLT 11 签名分块、BOLT 12 metadata 承诺密钥、onion 密文列表与 blinded 尾部。
3. 提高 gossip 中继预算至 8192 B；实现三个 feature 位。
4. 用 Bitcoin Core v31.1 regtest 起真实节点，跑 S1–S12 互操作场景与攻击测试（36 个）。

### 7.3 关键超参数、预处理和训练细节

无训练。关键参数：ML-DSA-44（pk 1312 B / sig 2420 B）、ML-KEM-768（ek 1184 B / ct 1088 B）；onion 密文列表固定 20 槽 = 21,770 B、blinded 尾 10 槽 = +10,890 B；invoice 字段上限 639 B；onion 载荷 1300 B；消息上限 65,535 B；中继预算 1024→8192 B。

### 7.4 能否迁移到其他任务？

与网络流量分析无直接关系。可迁移的是方法论：**"后量子迁移=体积约束下的格式适配问题"**——把大体积 PQ 材料塞进定长字段、用 dummy 填充隐藏真实槽位使用（可类比流量分析中的掩蔽/填充设计），以及"新旧协议共存期靠可选字段跳过"的兼容策略，可类比加密流量分类面对协议版本演进（如 PQC 时代 TLS 握手形态变化）时的特征漂移问题（推断，非论文主张）。

### 7.5 对我的研究有什么启发？

弱启发：本批另有 2026-NDSS-Looma（PQC 认证架构）与 2026-arXiv-The_Colossus_with_Feet_of_Clay（PQC 演进对加密流量分类器的影响）等论文；PQLN 提供的"协议升级期新旧共存、报文格式可加不可改"视角，可作为讨论"加密流量分类器在协议演进下的鲁棒性"的协议层背景（推断，非论文主张，§9 不建立链接）。

## 8. 总结

### 8.1 核心思想

> 闪电网络链下表面可先于比特币完成 PQ 迁移：混合保守扩展 + TOFU pin + 尺寸适配（签名分块、密文并列），软件升级即可，无需共识变更。

### 8.2 速记版 Pipeline

1. 从种子按两个 hardened BIP 32 索引派生 ML-DSA/ML-KEM 节点密钥。
2. 在 node_announcement 里带 TLV 27/29/31 宣告公钥，首见即 pin；中继预算提到 8192 B。
3. BOLT 8 专用端口跑混合 Noise_XK 握手（两次 ML-KEM 封装），无带内协商。
4. invoice 分块塞 ML-DSA 签名；offer metadata 承诺每 offer 密钥；onion 保持 1300 B、密文放 20 槽并列列表。
5. vanilla 节点跳过未知奇数 TLV 照常工作；12 类互操作场景全部通过，gossip 代价约 10×。

## 9. Obsidian 知识链接

### 9.1 相关概念

- KB 概念白名单（website-fingerprinting、encrypted-traffic-analysis、censorship-circumvention 等）均为流量分析概念，不覆盖区块链/支付通道协议安全，故本节不建立链接，避免发明页面名。

### 9.2 相关方法

- 方法白名单（transformer、pre-training-finetuning 等）均为流量分析建模方法，本文为密码协议工程，无对应页，不建立链接。

### 9.3 相关任务

- 无对应任务页（KB 任务白名单全部为流量侧任务）。

### 9.4 可更新的综述页面

- 无。本文不属于 KB 任何综述（加密流量分析 / WF / 恶意检测 / 基础模型）的主题范围。

### 9.5 可加入的对比表

- 不适用：论文未提出流量分析方法/数据集，也无流量侧实验。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 链下五类表面可在不改比特币的前提下获得 PQ 保护，且与 vanilla 节点互操作 | 12 个互操作场景（含混合 V-Q、Q-V-Q）全部通过 | Table V、§VI-E |
| 新增密码操作开销可忽略：最贵为 ML-DSA-44 签名 0.33 ms（约 ECDSA 13×），典型链路每跳 <60 ms | Rust 计时（15 种配对）与端到端延迟测量 | Table III、Table IV |
| 主要成本是通信：gossip 下载 10.2×、存储 8.8×（ML-DSA-44），换 FN-DSA-512 约 4× | 每通道 8111/9687 B vs vanilla 799/1102 B；33,000 通道 ≈270/320 MB | §VI-D、Fig. 7(c) |
| 尺寸适配手法（639 B 分块签名、1300 B onion 旁 20 槽密文列表 + FIPS-203 dummy）决定参数可用性：仅 ML-DSA-44 全部支付请求低于解析上限 | 请求长度测量 vs QR 4296 / 解析 7089 限制 | §VI-C、Fig. 7(b) |
| 设计被迫做的取舍：channel_announcement 保持经典（故 growth 10× 而非 Osuntokun 估计的 29×）；TOFU + 部分经典签名 + phantom 支付未覆盖 | 设计选择说明与局限一节 | §VI-D、§VII |

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-arXiv-PQLN__Post-Quantum_Security_for_the_Bitcoin_Lightning_Network's_Off-Chain_Surfaces.pdf
- MinerU Markdown：02-parsed-markdown/2026-arXiv-PQLN__Post-Quantum_Security_for_the_Bitcoin_Lightning_Network's_Off-Chain_Surfaces.md

## 12. 后续问题

- 暂未整理

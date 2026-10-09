---
type: paper
title_original: "Hop: A Modern Transport and Remote Access Protocol"
title_cn: "Hop：一种现代传输与远程访问协议"
authors: [Paul Flammarion, George Hosono, Wilson Nguyen, Laura Bauman, Daniel Rebelsky, Gerry Wan, David Adrian, Zakir Durumeric]
year: 2026
venue: "USENIX Security 2026"
doi: "unknown"
url: "https://www.usenix.org/conference/usenixsecurity26/presentation/flammarion"
pdf: "00-inbox/PDFs/2026-USENIX-Hop__A_Modern_Transport_and_Remote_Access_Protocol.pdf"
mineru_md: "02-parsed-markdown/2026-USENIX-Hop__A_Modern_Transport_and_Remote_Access_Protocol.md"
status: processed
reading_level: L2
research_area: []
task: []
method: []
dataset: []
code: "https://doi.org/10.5281/zenodo.17953397"
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 标题（原文） | Hop: A Modern Transport and Remote Access Protocol |
| 标题（中文） | Hop：一种现代传输与远程访问协议 |
| 作者 | Paul Flammarion, George Hosono, Wilson Nguyen, Laura Bauman, Daniel Rebelsky, Gerry Wan, David Adrian, Zakir Durumeric |
| 单位 | Stanford University；Georgia Institute of Technology（George Hosono）；Independent（David Adrian） |
| 发表年份 | 2026 |
| 发表会议 | USENIX Security 2026（第 35 届 USENIX Security Symposium，2026-08-12~14，Baltimore） |
| 论文类型 | 协议设计 + 参考实现 + 性能评测（clean-slate 远程访问协议） |
| 研究领域 | 安全协议设计（传输层 + 远程访问）；不属于本库流量分析 main line 的 research_area 白名单范围 |
| 参考实现 | Go，约 18K LoC，由 cloc 统计：Transport 6k / Tubes 2k / Remote Access 5k / Tests 5k；对比 OpenSSH 约 130K LoC（C） |
| 数据集 | 无公开数据集；评测含 Mininet 仿真与 DigitalOcean 三地云服务器真实网络实验 |
| DOI | unknown（解析稿未给出论文 DOI；Zenodo 为 artifact DOI，非论文 DOI） |
| artifact | https://doi.org/10.5281/zenodo.17953397 （源码、Mininet 脚本、测量脚本、绘图脚本与文档） |
| PDF | 00-inbox/PDFs/2026-USENIX-Hop__A_Modern_Transport_and_Remote_Access_Protocol.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-USENIX-Hop__A_Modern_Transport_and_Remote_Access_Protocol.md |

> ⚠️ MinerU 解析问题：正文夹杂小型连字/脚注碎片（如 "refilationship"、"fi1400 byte"、"a contrario" 前的残留 `fi`），系 `fi`/`fl` 连字解析错误；节标题出现下标碎片形式；图（Figure 1-9）仅保留图片路径未提取内容；握手流程图中彩色标注（蓝/绿字段）信息在解析稿中丢失，只能从正文文字推断。

## 1. 一句话总结

Hop 是一个 clean-slate 设计的远程访问协议：以 Noise 握手 + Cyclist/Keccak duplex + ML-KEM 的三层结构（Transport / Tubes / Remote Access）替代 SSH，实现 5-6 个 RTT 的会话建立（SSH 需 12 个）、ACME 式自动证书签发、被绑定到"谁/做什么/何时/对谁"的单次授权委派，以及基于 UDP 的漫游支持。

## 2. 摘要翻译

### 2.1 摘要原文（节选）

> Since SSH's standardization nearly 20 years ago, real-world requirements for a remote access protocol and our understanding of how to build secure cryptographic network protocols have both evolved significantly. In this work, we introduce Hop, a transport and remote access protocol designed to support today's needs. Building on modern cryptographic advances, Hop reduces SSH protocol complexity and overhead while simultaneously addressing many of SSH's shortcomings through a cryptographically-mediated delegation scheme, native host identification based on lessons from TLS and ACME, client authentication for modern enterprise environments, and support for client roaming and intermittent connectivity.

### 2.2 摘要中文翻译

自 SSH 标准化近二十年以来，远程访问协议的现实需求与我们对"如何构建安全的密码网络协议"的理解都发生了显著变化。本文提出 Hop——一个面向当今需求的传输与远程访问协议。基于现代密码学进展，Hop 降低了 SSH 的协议复杂度与开销，同时通过以下机制弥补 SSH 的诸多缺陷：密码学中介的委派方案（cryptographically-mediated delegation）、借鉴 TLS 与 ACME 经验的服务器身份识别、面向现代企业环境的客户端认证，以及对客户端漫游与间歇性连接的支持。我们给出了现代远程访问协议的具体设计需求，描述了所提出的协议，并对其性能进行了评测。我们希望这项工作能推动关于"未来现代远程访问协议应当是什么样"的讨论。

## 3. 方法动机

1. **SSH 的既有缺陷**：存在降级攻击（Bäumer et al. 2023，SSH 未保护完整握手转录）与隐私泄露（协议作为"给定公钥是否被服务器接受"的预言机）；服务器认证依赖 TOFU（trust-on-first-use），Gutmann 的研究显示用户会盲目接受服务器密钥，SSH 作者 Tatu Ylönen 亦公开呼吁重新设计主机认证。
2. **实现层面的问题**：事实标准 OpenSSH 体量庞大且已偏离 SSH-2 规范（IETF 于 2024 年重启 SSH 工作组以弥合差异）；Dropbear 等轻量实现漏洞频发。Mosh、Guardian Agent、SSH-over-QUIC（SSH3）等改良方案均未被广泛采用。
3. **现代密码学提供了更简的构建方式**：WireGuard 证明社区愿意采纳全新协议设计；Noise 框架提供形式化验证的握手模式；Cyclist/Keccak duplex 可用单一置换实现全部对称密码学；ML-KEM 已由 NIST 标准化用于抗量子密钥建立。
4. **企业需求变化**：需要与既有 out-of-band 信任关系（SSO/OAuth/FIDO2）结合的客户端认证，以及受控的凭证委派（SSH 的 ssh-agent forwarding 允许被委派方的 root 无确认地冒充用户，是横向移动的常见跳板）。
5. **作者据此系统化出 8 条设计需求**（见 §4.1），并主张 clean-slate 重构而非继续打补丁。

## 4. 方法设计

### 4.1 八条设计需求（§2）

| 需求 | 内容要点 |
|---|---|
| R1 简单密码学协议 | 握手须抗降级、保证握手完整性、会话唯一性与抗重放；固定版本化原语集、无带内协商，不支持即显式失败 |
| R2 可信主机标识 | 首次连接即可验证服务器身份，验证失败必须导致认证失败；须抵抗主动网络敌手，且在发起方长期认证密钥被攻陷（KCI）时仍成立 |
| R3 可扩展客户端验证 | 原生支持利用既有 out-of-band 信任关系的客户端认证；长期身份被攻陷或委派权限被滥用时认证失败 |
| R4 隐私与机密性 | 服务器不得成为主动敌手的预言机；对被动观察者隐藏 SNI；对未知/未认证服务器保证客户端身份隐藏与前向保密 |
| R5 安全凭证委派 | 委派凭证绑定到特定用户、动作、目标与有效期，且不可超出授权范围复用；在被委派主机被攻陷时仍成立 |
| R6 不可靠流量上的安全传输 | 防止未认证敌手使服务器发出大于触发请求的响应（放大）；漫游与间歇连接不得导致会话劫持 |
| R7 受限环境支持 | 无复杂解析/验证逻辑；凭证走固定确定性验证路径且有界大小 |
| R8 抗量子安全 | 抵抗"先记录后解密"的量子敌手；长期认证密钥被攻陷不得追溯性破坏机密性 |

### 4.2 三层架构

| 层 | 职责 | 关键机制 |
|---|---|---|
| Hop Transport | 轻量密码传输层（UDP 之上） | Noise XX（discoverable）/ PQNoise IK 改造（hidden）；Cyclist+Keccak duplex；ML-KEM 做临时密钥交换、静态 DH 做认证；轻量 Hop Certs |
| Hop Tubes | 可靠/尽力而为连接复用层 | "tube" 多路复用；Tube ID 奇偶分配（客户端奇、服务器偶）；单 RTT 创建、四路 FIN-ACK 关闭；NewReno 类拥塞控制 |
| Hop Remote Access | 远程访问应用层 | 远程 shell、命令执行、本地/远程端口转发（+ UDP 端口转发走 best-effort tube）；Authorization Grant 委派协议 |

### 4.3 握手设计

- **Discoverable Mode**：在 Noise XX 前额外增加一个 RTT（受 PQNoise 启发），流程为 `→ ekem；← Encaps(ekem), cookie；→ e, ekem, cookie；← e, ee, s, es；→ s, se`。额外 RTT 用于防 DoS 放大并实现抗量子前向保密；cookie 为认证加密块（以客户端 ML-KEM 临时公钥、IP、端口为关联数据），服务器可定期轮换解密密钥（如每两分钟），从而在客户端认证前保持**无状态**；Server Hello 大小与 Client Hello 相等以抑制放大（R6）。
- **Hidden Mode**：基于 PQNoise IK 改造（认证仍用 DH 静态密钥），**单 RTT**完成；要求客户端事先经 out-of-band 获得服务器静态 ML-KEM 封装密钥；服务器对不知晓其密钥的客户端不作响应，从而对扫描器与未认证探测**完全隐身**（R4）。
- **握手失败处理**：除拒绝/超时/错误外握手无分支；失败或丢包时双方丢弃状态并保持沉默；证书验证失败时双方仍完成握手，但拒绝方立即发送加密的 Connection Close（防 UDP 伪造）。
- **关键派生**：duplex 对象吸收传输参数、KEM 密钥与其共享秘密、DH 结果，并挤出 MAC 附加到每条消息以保证完整性与转录一致性；握手后使用标准 AEAD 记录构造。

### 4.4 证书与身份

- **Hop Certs**：自定义轻量证书结构，每字段只支持单一算法/方案以简化解析；每证书至多一个父证书（保证链为线性），路径长度固定为 3（leaf / intermediate / root）；证书大小保证所有握手认证消息 **≤ 1400 字节 MTU**，无需跨 L4 分片重组。
- **自动签发（ACME 式）**：三阶段——Registration / Identifier Validation / Certificate Issuance；CA 向申请者发送 **256-bit challenge** 字符串与 Hop 客户端 KEM 密钥，申请者在其域名上建立 Hop 服务器并为 CA 的 KEM 密钥创建特殊授权 grant，CA 以 hidden mode 连接并验证 challenge 回显。
- **客户端认证**：所有 Hop 握手都强制客户端认证（区别于 TLS/QUIC）；支持三类客户端证书——CA 签发的短期证书、自签发证书（类似 SSH 公钥，另支持 authorized_keys 文件）、临时客户端证书（供委派使用）。

### 4.5 授权委派（Authorization Grant）

三方模型：**Principal**（信任机器上的 Hop 客户端，持长期凭证）→ **Delegate**（半信任机器上的客户端）→ **Target**（被访问的 Hop 服务器）。意图（intent）明确四要素：**who**（请求授权的 Delegate 身份）、**what**（可执行的单个动作）、**when**（授权时间窗）、**to whom**（Target 身份）。流程：Delegate 发 Intent Request（含动作描述与临时客户端证书）→ Principal 请求用户显式确认（对话框）→ Principal 经 Delegate 代理与 Target 握手 → 发 Intent Communication → Target 若批准则在内存映射中创建授权 grant 并回 Intent Confirmation → Principal 转达 → Delegate 以自己的身份与 Target 建立 Hop 会话执行动作 → 会话建立后 Target 立即移除该 grant。**授权不可转移、限时、单次使用**，且可扩展为多跳委派链（Delegate 再接 Target 时 Target 本身可作为新的 delegate 向原 Principal 发起意图请求），从而限制横向移动（R5）。

### 4.6 Tubes 的传输机制

- **Tube 创建**：单 RTT，REQ 位 = 1 且 Frame Number = 0（消除序列号同步需求）；Tube ID 与 tube type 由发起方**不可协商**指定，响应方仅回 RESP 表示接受。
- **关闭**：四路 FIN-ACK/FIN-ACK；已发送 FIN 后仍会对来的 tube 帧回带 FIN 标志的确认；Tube ID 在关闭后需保留 **4×RTT** 才可复用。
- **可靠传输**：重复 ACK 检测丢包 + RTO 兜底；**重排序阈值设为 10**（高于 TCP 的 3，因 Hop 的帧号加密使网络设备无法观察重排）；RTT 用 EWMA 平滑（新样本权重 1/8），RTO = **9/8 倍平滑 RTT**，连续超时指数退避，RTO > 10 秒则从重传列表移除。
- **拥塞控制**：类 TCP NewReno（慢启动 / AIMD / 快速恢复）；窗口以**帧数**而非字节计，最小 10 帧、最大 1000 帧；丢包时窗口降为当前值的 **25%**（非 TCP 的 50%，以避免利用率过低）；不做 pacing，作者称这是当前实现的性能局限、与安全协议本身独立。

## 5. 与其他方法对比

| 维度 | Hop | SSH（OpenSSH） | Mosh | SSH3（SSH over QUIC/HTTP3） |
|---|---|---|---|---|
| 传输层 | UDP（自带可靠/拥塞/漫游） | TCP | SSH 认证后切到 UDP | QUIC |
| 会话建立往返 | 5（Hidden）/ 6（Discoverable）RTT | 12 RTT | 依赖 SSH | 论文未并列对比 |
| 主机认证 | 内建 ACME 式自动签发证书 + 固定三层链 | TOFU 为主 | 沿用 SSH | 沿用 SSH 身份模型 |
| 委派 | Authorization Grant（绑定 who/what/when/to whom、单次使用） | ssh-agent forwarding（被委派方 root 可任意冒充） | 同 SSH | 同 SSH |
| 抗量子 | ML-KEM 做临时密钥建立（抗"先记录后解密"） | 无原生 PQC | 无 | 依赖 QUIC 栈 |
| 实现规模 | 18K LoC Go | 约 130K LoC C | — | — |
| 落地状态 | 参考实现（未公开部署） | 事实标准 | 部分采用 | 未广泛采用 |

## 6. 实验表现与优势

### 6.1 实验设置

| 项 | 设置 |
|---|---|
| 真实网络 | 三台云服务器（US / Europe / Asia），客户端位于 US 经 WiFi 连接（DigitalOcean 基础设施） |
| SSH 密码套件 | ChaCha20-Poly1305（避免硬件加速干扰对比） |
| 会话建立 | 每台主机 300 次会话建立，两协议交替进行；测量"Time to Shell"（非交互式 shell + 执行首条命令） |
| 仿真 | Mininet 连接两主机与一路由器，瓶颈链路 100 Mb/s、10 ms 延迟、无抖动、无丢包；传输 1 GB 随机数据 |
| 吞吐 | 真实网络用 rsync 上传 10 MB / 100 MB / 1 GB 文件，每种至少重复 50 次、跨 3 天 |
| 按键延迟 | 已建立会话上进行，按键间隔 150 ms；沿用 SSH3 评测方法，在 Vim 中用 Typometer 记录 |
| RTT 参考 | US = 69 ms，Europe = 144 ms，Asia = 186 ms（Fig. 6 说明） |

### 6.2 主要结果

| 指标 | Hop | SSH | 说明/证据 |
|---|---|---|---|
| 会话建立往返数 | 5（Hop-H）/ 6（Hop-D）RTT | 12 RTT | Fig. 6；Hop 连接时间波动更小（更稳定） |
| 吞吐（真实网络，rsync） | 与 SSH NewReno 相当，尤其小文件 | TCP CUBIC 在各地区与文件大小上吞吐最高 | Fig. 8；Hop 在大文件上因无 pacing 出现突发丢包、线性增长较慢 |
| 吞吐（Mininet 仿真） | 与 SSH NewReno 相近；**带宽变化时低约 40%** | NewReno 表现稳定 | §8.2, Fig. 7 |
| 按键延迟 | 分布更紧、更接近真实 RTT | 分布更分散 | Fig. 9；得益于 UDP（无 Nagle、无队头阻塞）与轻量成帧 |
| 实现规模 | 18K LoC Go | 约 130K LoC C | §7 开篇 |

> ⚠️ MinerU 解析问题：Figure 6-9 均为图片（未提取数值），上述定量结论以正文文字描述与图注为据，具体分位数未能从解析稿读取。

### 6.3 优势

- 以"减少往返 + 固定原语集 + 简化证书"换取更小的攻击面与更易审计的实现（18K vs 130K LoC）；
- 唯一在协议层原生解决"首次连接即可信"（ACME 式签发）与"受限委派"（Authorization Grant）两项 SSH 长期痛点的设计之一；
- 抗量子前向保密（ML-KEM 临时密钥建立）与对量子"先记录后解密"的防御被显式纳入设计需求（R8）；
- 服务器隐身模式（Hidden Mode）对扫描器完全不作响应，显著降低被探测/滥用面；
- 作者明确不追求性能超越 SSH（OpenSSH 是高度优化的 C 实现），而重在证明功能完备与工程可行。

## 7. 学习与应用

- **对协议设计研究**：Hop 展示了"用单一 duplex 置换实现全部对称密码学 + 版本化而非带内协商"的设计范式如何同时降低代码量、内存占用与降级攻击面；这一思路可迁移到 IoT、嵌入式等受限环境的协议设计。
- **对流量分析研究（间接价值）**：Hop 的流量特征与 SSH 显著不同——UDP 承载、无 Nagle、帧号加密、连接 ID 与 IP/port 解耦（支持漫游）。这对**协议识别/流量分类**意味着：(1) 基于包长/时序的 SSH 指纹可能无法直接迁移到 Hop；(2) 加密帧号使网络中间设备失去重排可见性，与传统 TCP 类协议的可观测性假设不同。可作为"新型协议对既有流量分类器的挑战"的案例。
- **对流量伪装/抗审查（间接）**：Hidden Mode 的"先验共享 KEM 密钥 + 单 RTT"设计使服务器对扫描器不可见，与抗审查领域的"主动探测防御"目标一致，可作为主动探测抵抗设计的参考案例。
- **可迁移机制**：(1) cookie 中编码完整 duplex 状态以实现客户端认证前无状态服务器；(2) 证书链长度固定为 3 且消息 ≤1400 字节以规避分片重组；(3) 委派授权绑定 who/what/when/to whom 并单次使用。
- **对本库主线**：论文不涉及流量分类/指纹识别/检测任务，方法学关联弱（relevance: low），主要价值在于协议层新流量形态对流量分析研究的潜在挑战。

## 8. 总结

Hop 是对 SSH 的 clean-slate 重新设计：以 Noise 握手（Discoverable/XX 加一 RTT；Hidden/PQNoise IK 单 RTT）+ Cyclist/Keccak duplex + ML-KEM 构成轻量传输层，其上是多路复用的 Hop Tubes（NewReno 类拥塞控制、以帧计数、25% 乘性减窗），最上是提供远程 shell 与端口转发的 Remote Access 层。它用 ACME 式自动证书签发消灭 TOFU，用 Authorization Grant 实现绑定 who/what/when/to whom 的单次委派，并以 UDP 支持漫游与间歇连接。评测显示会话建立 5-6 RTT（SSH 12 RTT）、吞吐与 SSH NewReno 相当（带宽变化时低约 40%）、按键延迟更低更稳定。

## 9. Obsidian 知识链接

### 9.1 相关概念

- 白名单概念页（`censorship-circumvention`、`website-fingerprinting`、`encrypted-traffic-analysis`、`traffic-classification`、`tunnel-detection` 等）均以流量分析/审查规避的测量与识别为主题，不覆盖"远程访问协议设计"，故本节不链接。

### 9.2 相关方法

- 白名单方法页均为机器学习方法（transformer、cnn、gcn 等），与本论文的密码协议设计方法无对应，故不链接。

### 9.3 相关任务

- 白名单任务页（`website-fingerprinting`、`encrypted-traffic-classification`、`malicious-traffic-detection` 等）不涵盖远程访问协议，故不链接。

### 9.4 相关综述

- 白名单综述页（`survey-encrypted-traffic-analysis`、`survey-few-shot-learning`、`survey-malicious-traffic-detection`、`survey-traffic-foundation-model`、`survey-website-fingerprinting`）均以流量分析为目标，与本论文主题不符，故不链接。

### 9.5 对比表

- `method-comparison-table` / `dataset-comparison-table`：本文未提出机器学习方法、未使用或发布数据集，故不链接。
- `open-source-registry`：论文在 Open Science 节公开了源码、Mininet 脚本、测量脚本等 artifact（Zenodo 10.5281/zenodo.17953397），但该登记页面向流量分析工具，Hop 作为传输/远程访问协议实现不在其覆盖范围，故不链接。

### 9.6 相关研究前沿

- 本库 6 条研究前沿（`multimodal-fusion-strategy`、`payload-learnability`、`pretraining-necessity`、`representation-vs-shallow`、`tokenization-optimal`、`wf-attack-defense-limit`）均围绕加密流量分析，与本论文无对应，故不链接。

### 9.7 相关论文笔记

- 本论文参考文献中未出现 kb_reference A 表内的 171 篇论文，故不建立论文间 wikilink。

## 10. 证据记录

| 编号 | 论断 | 证据位置 |
|---|---|---|
| E1 | 三层架构：Hop Transport / Hop Tubes / Hop Remote Access；18K LoC Go（6k/2k/5k/5k）对比 OpenSSH 130K LoC C | §4, §7 开篇 |
| E2 | 系统化 8 条设计需求（R1-R8），并在 §8.1 逐条论证满足情况 | §2, §8.1 |
| E3 | Discoverable Mode = Noise XX 加一个额外 RTT（防 DoS 放大 + PQ 前向保密）；Hidden Mode = PQNoise IK 改造，单 RTT | §5.1-§5.3, Fig. 2 |
| E4 | 会话建立：Hop-H 5 RTT、Hop-D 6 RTT vs SSH 12 RTT；每主机 300 次测量；RTT US 69 ms / EU 144 ms / Asia 186 ms | §8.2, Fig. 6 |
| E5 | 吞吐：与 SSH NewReno 相当；Mininet（100 Mb/s、10 ms、无抖动丢包）下带宽变化时低约 40%；rsync 10 MB/100 MB/1 GB 各 ≥50 次跨 3 天 | §8.2, Fig. 7-8 |
| E6 | 按键延迟分布更紧、更接近真实 RTT；Vim + Typometer，150 ms 按键间隔，沿用 SSH3 方法 | §8.2, Fig. 9 |
| E7 | Hop Certs：每字段单一算法、至多一个父证书、路径固定 3 层（leaf/intermediate/root）、消息 ≤1400 字节 MTU | §5.6 |
| E8 | ACME 式签发三阶段（Registration / Identifier Validation / Certificate Issuance），256-bit challenge；客户端认证支持 CA 签发/自签发/临时三类证书 | §5.6.1-§5.6.2 |
| E9 | Authorization Grant：Principal/Delegate/Target 三方；intent = who/what/when/to whom；单次使用、限时、不可转移、可多跳链式 | §7.2-§7.3, Fig. 4-5 |
| E10 | Congestion control：NewReno 类；窗口以帧计（10-1000）；丢包降至 25%；重排序阈值 10；RTO = 9/8 平滑 RTT；无 pacing | §6.3 |
| E11 | 密码学：Cyclist（Keccak 置换）duplex 承担全部对称操作；ML-KEM 做临时 KEM；静态 DH（x25519 类）做认证；版本化替代带内协商 | §5.1, §5.5 |
| E12 | artifact 公开于 Zenodo，含源码、仿真/测量/绘图脚本与文档 | Open Science |

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-USENIX-Hop__A_Modern_Transport_and_Remote_Access_Protocol.pdf
- MinerU Markdown：02-parsed-markdown/2026-USENIX-Hop__A_Modern_Transport_and_Remote_Access_Protocol.md

## 12. 后续问题

1. 论文的性能结论基于 Go 参考实现且不做 pacing；若加入 pacing 与可插拔拥塞控制，带宽变化时 ~40% 的吞吐差距能否消除？
2. Hop 的 UDP 承载与加密帧号使其流量特征区别于 SSH——现有 SSH 协议识别/流量分类方法能否识别 Hop？需要哪些新特征？
3. Authorization Grant 的"内存映射 + 会话建立后即刻移除"在 Target 重启或进程崩溃时的行为如何？是否存在授权重放窗口？
4. Hidden Mode 依赖 out-of-band 分发服务器静态 ML-KEM 封装密钥；在密钥轮换与多主机配置（服务器需遍历 host 匹配静态密钥）下的可扩展性如何？
5. 论文未做形式化验证（仅称基于形式化验证过的 Noise 模式）；Hop 的握手组合（Noise + 额外 RTT + cookie）是否已由形式化工具覆盖？

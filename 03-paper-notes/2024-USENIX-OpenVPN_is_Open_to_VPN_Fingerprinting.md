---
type: paper
title_original: "OpenVPN is Open to VPN Fingerprinting"
title_cn: "OpenVPN 容易受到 VPN 指纹识别攻击"
authors:
  - Diwen Xue
  - Reethika Ramesh
  - Arham Jain
  - Michalis Kallitsis
  - J. Alex Halderman
  - Jedidiah R. Crandall
  - Roya Ensafi
year: 2022
venue: USENIX Security
doi: unknown
url: https://www.usenix.org/conference/usenixsecurity22/presentation/xue-diwen
pdf: "../00-inbox/PDFs/2024-USENIX-OpenVPN_is_Open_to_VPN_Fingerprinting.pdf"
mineru_md: "../02-parsed-markdown/2024-USENIX-OpenVPN_is_Open_to_VPN_Fingerprinting.md"
status: processed
reading_level: L2
research_area:
  - VPN 流量检测
  - 网络审查对抗
  - 流量指纹识别
task:
  - VPN 流量识别
  - 流量指纹识别
  - 活跃探测
method:
  - Opcode 指纹识别
  - ACK 指纹识别
  - 活跃服务器探测
  - 两阶段检测框架（Filter + Prober）
dataset:
  - ISP Dataset（Merit Network, 1M 用户）
  - VPN Dataset（20 商业 VPN 提供商）
  - ZMap Set（13M+ 端点）
  - Censys Set（180,858 OpenVPN 端点）
code: unknown
relevance: high
created: 2026-06-09
updated: 2026-06-09
---

# OpenVPN is Open to VPN Fingerprinting

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | OpenVPN is Open to VPN Fingerprinting |
| 中文标题 | OpenVPN 容易受到 VPN 指纹识别攻击 |
| 作者 | Diwen Xue, Reethika Ramesh, Arham Jain, Michalis Kallitsis, J. Alex Halderman, Jedidiah R. Crandall, Roya Ensafi |
| 年份 | 2022 |
| 会议/期刊 | USENIX Security |
| 研究方向 | VPN 流量检测 / 网络审查对抗 |
| 任务类型 | VPN 流量识别、流量指纹识别、活跃探测 |
| 方法关键词 | Opcode 指纹、ACK 指纹、活跃探测、两阶段框架、被动过滤 + 主动探测 |
| 数据集 | Merit Network ISP 数据（1M 用户）、20 商业 VPN、ZMap 13M+ 端点、Censys 180K OpenVPN 端点 |
| 是否开源 | 否 |
| PDF | `00-inbox/PDFs/2024-USENIX-OpenVPN_is_Open_to_VPN_Fingerprinting.pdf` |
| MinerU Markdown | `02-parsed-markdown/2024-USENIX-OpenVPN_is_Open_to_VPN_Fingerprinting.md` |

---

## 1. 一句话总结

> 通过被动过滤（Opcode + ACK 指纹）和主动探测的两阶段框架，在真实 ISP 网络中以极低误报率识别超过 85% 的 OpenVPN 流量，包括大多数"混淆"VPN 服务。

---

## 2. 摘要翻译

### 2.1 摘要原文

VPN adoption has seen steady growth over the past decade due to increased public awareness of privacy and surveillance threats. In response, certain governments are attempting to restrict VPN access by identifying connections using "dual use" DPI technology. To investigate the potential for VPN blocking, we develop mechanisms for accurately fingerprinting connections using OpenVPN, the most popular protocol for commercial VPN services. We identify three fingerprints based on protocol features such as byte pattern, packet size, and server response. Playing the role of an attacker who controls the network, we design a two-phase framework that performs passive fingerprinting and active probing in sequence. We evaluate our framework in partnership with a million-user ISP and find that we identify over 85% of OpenVPN flows with only negligible false positives, suggesting that OpenVPN-based services can be effectively blocked with little collateral damage. Although some commercial VPNs implement countermeasures to avoid detection, our framework successfully identified connections to 34 out of 41 "obfuscated" VPN configurations.

### 2.2 摘要中文翻译

过去十年间，随着公众对隐私和监控威胁意识的增强，VPN 的采用率稳步增长。作为回应，某些政府试图通过"两用"DPI 技术识别连接来限制 VPN 访问。为调查 VPN 封锁的潜力，我们开发了准确指纹识别 OpenVPN 连接的机制——OpenVPN 是商业 VPN 服务最常用的协议。我们基于字节模式、数据包大小和服务器响应等协议特征识别出三种指纹。我们以控制网络的攻击者角色设计了一个两阶段框架，依次执行被动指纹识别和活跃探测。我们与一家百万用户 ISP 合作评估该框架，发现能识别超过 85% 的 OpenVPN 流量且误报率可忽略不计，表明基于 OpenVPN 的服务可以被有效封锁且附带损害极小。尽管一些商业 VPN 实施了反检测措施，我们的框架仍成功识别了 41 个"混淆"VPN 配置中的 34 个。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 多国政府（中国、俄罗斯、印度）和 ISP 正在积极封锁/限速 VPN
- 现有 ML 方法在真实网络环境中因低基数问题导致误报率过高
- 缺乏从 ISP/审查者视角评估 OpenVPN 可指纹性的实证研究

### 3.2 现有方法的痛点和不足

- ML 方法在平衡数据集上表现好，但真实网络中 VPN 流量基数极低，误报率不可接受
- 现有 DPI 工具仅做静态 opcode 匹配，无法应对 XOR 混淆
- 商业 VPN 的"混淆"服务声称不可检测，但缺乏系统性验证
- 没有在真实 ISP 网络中进行大规模评估的工作

### 3.3 论文的研究假设或核心直觉

OpenVPN 的协议特征（opcode 序列、ACK 模式、服务器响应行为）即使经过混淆处理仍可被指纹识别，且在 ISP 规模下可实现极低误报率。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 多国政府和 ISP 积极封锁 VPN，商业 VPN 纷纷推出"混淆"服务 | §1 |
| 痛点提炼 | 缺乏从攻击者视角在真实网络中评估 VPN 可指纹性的研究 | §2, §3 |
| 问题转化 | ISP/审查者能否在大规模、低误报率下识别 OpenVPN 流量？ | §3 |
| 文献定位 | 该问题在已有文献中被部分解决（ML 方法）但缺乏实际可行性验证 | §2 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | OpenVPN 的协议级特征可通过被动+主动方式在 ISP 规模下被可靠识别 | 协议分析 + GFW 架构启发 | 真实 ISP 部署实验 |
| 辅助假设 | 商业 VPN 的混淆方案不足以抵御协议级指纹识别 | 混淆方案多基于简单 XOR/隧道 | 41 个混淆配置测试 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | 85% vanilla OpenVPN 被识别，误报率 < 0.0039% | §9 |
| 辅助假设 | 支撑 | 34/41 混淆配置被成功识别 | §9.1 |

---

## 4. 方法设计

### 4.1 方法整体流程

两阶段框架：(1) Filter 被动过滤——在 ISP 网络中实时分析流量，基于 Opcode 和 ACK 指纹标记可疑流；(2) Prober 主动探测——向可疑目标发送精心设计的探测包，利用协议行为差异确认 OpenVPN 服务器。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | 原始网络流量 | Opcode 指纹：分析前 N 包的 opcode 字节数种类和序列模式 | 可疑流标记 | 被动检测 OpenVPN 握手 |
| Step 2 | 原始网络流量 | ACK 指纹：统计每 10 包 bin 中 ACK 大小包的数量分布 | 可疑流标记 | 检测隧道/加密混淆 |
| Step 3 | Filter 输出的 IP:Port | 发送 Base Probe 1（完整 Client Reset）和 Base Probe 2（截断 1 字节） | 服务器响应时间差异 | 利用 OpenVPN 包重组行为 |
| Step 4 | 候选端点 | 发送 RST 阈值探测（2000 随机字节）和协议探测（HTTP/TLS/SSH） | 确认/排除 | 降低误报 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Filter (Zeek) | 被动指纹识别 | 原始流量镜像 | 可疑 IP:Port 列表 | 传给 Prober |
| Prober (Nim) | 主动探测确认 | IP:Port 列表 | 确认的 OpenVPN 端点 | 接收 Filter 输出 |
| PF_RING | 高速包处理 | 网络接口镜像 | 零拷贝包流 | 供 Filter 处理 |

### 4.4 公式、算法和机制解释

- **Opcode 指纹**：观察前 N 包的 opcode 字段，检查 (1) 不同 opcode 种类数是否在 4-10 之间；(2) Client Reset 和 Server Reset 仅出现在握手初期。对 XOR 混淆有效因为 XOR patch 不反转首字节。
- **ACK 指纹**：将包分为 10 包 bin，统计每 bin 中与首个 ACK 包同大小的包数。OpenVPN 特征：早期 bin 高 ACK 计数，后期 bin 低 ACK 计数。
- **主动探测**：Base Probe 1（16 字节完整 Client Reset）触发立即关闭；Base Probe 2（15 字节截断）触发长等待后关闭。时间差可区分 OpenVPN。
- **RST 阈值**：OpenVPN 服务器的 RST 阈值集中在 1550-1660 字节（对应 MTU 配置），97%+ 随机端点阈值 < 500 或 > 4000。

### 4.5 方法优势

- 仅检查前 100 个数据包即可完成检测（中位延迟 7.9 秒）
- 误报率极低（< 0.0039%），比 ML 方法低三个数量级
- 可应对 XOR 混淆和大多数隧道混淆
- 在单服务器上每天处理 15TB / 20 亿流

### 4.6 方法不足

- 无法有效检测 UDP 模式下的 OpenVPN（缺少长度字段）
- obfs4、VMess 等带随机填充的混淆可逃避检测
- 活跃探测对 behind-IDS 的服务器无效
- 仅针对 OpenVPN，需额外工作扩展到 WireGuard 等

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

本文从**实际攻击者（ISP/审查者）的视角**出发，不仅识别指纹漏洞，还在真实 ISP 网络中验证实际可行性。与 ML 方法相比，本文的方法在低基数真实流量中表现更优（误报率低三个数量级）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| Opcode 动态指纹 | 不要求精确匹配，仅检查 opcode 种类数变化 | 高 | 是（可扩展到其他协议） |
| ACK 指纹 | 利用 OpenVPN 协议层 ACK 的独特模式 | 高 | 是（类似模式的协议） |
| 主动探测（利用包重组行为） | 通过截断包触发不同代码路径的响应时间差 | 高 | 是（TCP 协议通用） |
| 真实 ISP 部署评估 | 与百万用户 ISP 合作的 8 天评估 | 高 | 否（需 ISP 合作） |
| 混淆 VPN 系统性评估 | 测试 41 个混淆配置 | 中 | 否 |

### 5.3 适用场景

- ISP 级别的 VPN 流量检测和限速
- 国家级审查者封锁 VPN 服务
- VPN 提供商评估自身混淆方案的安全性

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| ML 分类器 | 可自动学习特征 | 真实网络误报率高（1.4%-5.5%） | 误报率 < 0.0039% |
| 静态 DPI（nDPI 等） | 实时处理 | 仅匹配已知模式，易被混淆绕过 | 动态 opcode + ACK 双指纹 |
| 基于 IP 封锁 | 简单直接 | VPN IP 频繁更换 | 协议级检测不依赖 IP |
| 流量时序分析 | 不依赖载荷 | 精度不足 | 结合协议语义和活跃探测 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

在 Merit Network（服务 100 万用户的中型区域 ISP）内部署 Filter 和 Prober。Filter 部署在监控站（16 核服务器，20Gbps 镜像接口），使用 PF_RING 零拷贝 + Zeek 集群（15 workers）。Prober 部署在两台专用测量机上。采样率 12.5%（基于 IP 对），丢包率 < 3%。

### 6.2 数据集

- ISP Dataset：2021 年 7 月 28 日 45 分钟流量快照（1/30 采样），461GB，221,534 流
- VPN Dataset：20 商业 VPN + 2 自建 OpenVPN，2,200 traces
- ZMap Set：全 IPv4 65,535 端口扫描，13M+ 端点
- Censys Set：180,858 已知 OpenVPN 端点
- 评估控制流量：80 商业 VPN 提供商，81 配置（40 vanilla + 41 混淆）

### 6.3 Baseline

- ML 方法（Bagui et al., Fu et al., Miller et al.）的误报率：1.4%-5.5%

### 6.4 评价指标

- Recall（识别率）
- Precision / False Positive Rate（误报率）
- 处理吞吐量（TB/天，流/天）

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| Vanilla OpenVPN (40 configs) | Recall | 85.90% (1718/2000) | - | - | 39/40 配置被识别 |
| Obfuscated OpenVPN (41 configs) | Recall | 72.67% (1468/2020) | - | - | 34/41 配置被识别 |
| Overall (ISP traffic) | FPR | < 0.0039% | 1.4%-5.5% (ML) | 低 3 个数量级 | 8 天评估，3638 flagged 流 |
| 日处理量 | 吞吐量 | 15 TB / 20 亿流 | - | - | 单服务器 |

### 6.6 优势最明显的场景

- Vanilla OpenVPN TCP 连接：识别率最高
- XOR 混淆的 VPN 服务：Opcode 指纹仍然有效
- 缺乏随机填充的隧道混淆（Stunnel, SSH, obfs3）：ACK 指纹有效

### 6.7 局限性

- UDP 模式 OpenVPN 无法通过活跃探测确认
- obfs4 和 VMess 等带随机填充的混淆可逃逸
- Behind-IDS 的服务器阻止活跃探测
- /29 子网探测范围限制可能遗漏远端服务器

---

## 7. 学习与应用

### 7.1 是否开源？

否

### 7.2 复现关键步骤

1. 使用 Zeek 实现 Opcode 和 ACK 指纹过滤器
2. 使用 Nim 实现 Prober（发送各种探测包并测量响应时间）
3. 使用 PF_RING 进行高速包处理
4. 在 ISP 网络中部署 Filter 进行流量镜像分析
5. 配置 Prober 异步批量探测

### 7.3 关键超参数、预处理和训练细节

- 观察窗口 N = 100 包
- ACK bin 大小 = 10 包
- ACK 阈值：Bin[1] 在 1-3，Bin[2] 在 2-5，Bin[3-5] <= 5，Bin[6+] <= 1
- 探测频率：每日批量
- 采样率：12.5%（基于 IP 对）

### 7.4 能否迁移到其他任务？

- Opcode 动态指纹思路可扩展到其他基于 opcode 的协议
- ACK 指纹方法可应用于有类似确认机制的协议
- 包重组行为探测可通用化为 TCP 协议的指纹识别手段
- 两阶段框架（被动+主动）可作为通用 VPN/代理检测架构

### 7.5 对我的研究有什么启发？

- 从攻击者视角评估协议安全性比单纯识别漏洞更有说服力
- 协议级指纹比 ML 特征更稳定、更可解释
- "混淆"不等于"不可检测"——大多数商业混淆方案过于简单
- 真实网络评估（ISP 合作）是验证检测系统可行性的关键

---

## 8. 总结

### 8.1 核心思想

> OpenVPN 协议级特征可通过被动+主动两阶段框架在 ISP 规模下可靠识别。

### 8.2 速记版 Pipeline

1. Filter 被动分析前 100 包的 Opcode 序列和 ACK 分布
2. 标记可疑流的 IP:Port
3. Prober 发送精心设计的探测包（完整/截断 Client Reset）
4. 利用 OpenVPN 包重组行为的响应时间差异确认
5. RST 阈值探测进一步排除误报

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- VPN 流量检测
- 深度包检测（DPI）
- 流量指纹识别
- 活跃探测
- 网络审查

### 9.2 相关方法

- Opcode 指纹识别
- ACK 指纹识别
- 两阶段检测框架
- OpenVPN XOR 混淆

### 9.3 相关任务

- 加密流量分类
- 协议识别
- 审查对抗

### 9.4 可更新的综述页面

- VPN 流量检测综述
- 加密协议指纹识别方法对比

### 9.5 可加入的对比表

- VPN 混淆方案效果对比
- 加密流量检测方法对比

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 85.90% vanilla OpenVPN 被识别 | 1718/2000 控制流，39/40 配置 | §9.1 |
| 72.67% 混淆 OpenVPN 被识别 | 1468/2020 控制流，34/41 配置 | §9.1 |
| 误报率 < 0.0039% | 3638 flagged 流中 3245 有证据支持 | §9.2 |
| 4/5 头部 VPN 使用 XOR 混淆 | 分析 top5 VPN 提供商的混淆实现 | §9.1 |
| obfs4/VMess 可逃逸检测 | 随机填充破坏 ACK 指纹 | §9.1 |
| OpenVPN 服务器 RST 阈值 1550-1660 | ZMap 和 Censys 数据集分析 | §6.3 |

---

## 11. 原始资料链接

- PDF：`00-inbox/PDFs/2024-USENIX-OpenVPN_is_Open_to_VPN_Fingerprinting.pdf`
- MinerU Markdown：`02-parsed-markdown/2024-USENIX-OpenVPN_is_Open_to_VPN_Fingerprinting.md`

---

## 12. 后续问题

- WireGuard 和 IPSec 等其他 VPN 协议的可指纹性如何？
- 商业 VPN 采用 Pluggable Transports 等标准化混淆后效果如何？
- 审查者是否会实际部署此类两阶段检测系统？
- 如何设计既高效又抗指纹的 VPN 混淆方案？

---

## 13. 写作叙事与故事线分析

> 仅对 CCF A/B 级或用户指定深度分析的论文填写本节。

### 13.1 论文主线故事线

论文从全球 VPN 封锁趋势出发，指出 OpenVPN 作为最流行商业 VPN 协议面临 DPI 检测威胁。作者设计了受 GFW 启发的两阶段检测框架，在真实 ISP 中验证了 OpenVPN（包括大多数"混淆"服务）的可指纹性，并警告用户不应期望 VPN 使用不可观测。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 概述威胁和核心发现 | 全文缩影 | - |
| Introduction | 从全球 VPN 封锁趋势引入 | 问题背景 | 混淆 VPN 声称不可检测 |
| Background | OpenVPN 协议和已有检测方法 | 技术铺垫 | 现有方法缺乏实际验证 |
| Challenges | 指出真实世界检测的挑战 | 问题定位 | ML 方法在低基数下不可行 |
| Fingerprinting Features | 三种指纹识别方法 | 核心贡献 | Opcode + ACK + 活跃探测 |
| Fine-tuning | 参数优化和阈值确定 | 工程支撑 | 100 包窗口平衡速度和精度 |
| Evaluation | 真实 ISP 部署评估 | 关键证据 | 85% 识别率 + 0.0039% 误报 |
| Discussion | 威胁模型和缓解措施 | 影响讨论 | 混淆 VPN 的虚假安全感 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 评估不足 | ML 方法未在真实网络低基数场景下验证 | 矛盾证据（平衡数据集 vs 真实流量） | §3 |
| 场景缺失 | 商业混淆 VPN 缺乏系统性安全评估 | 声称 vs 实际的矛盾 | §2, §9.1 |
| 理论缺陷 | 混淆方案设计过于简单 | XOR patch 不反转首字节的漏洞 | §6.1 |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 控制流评估 | 量化检测能力 | 证明方法有效性 |
| 全流量评估 | 量化误报率 | 证明实际可行性 |
| 混淆 VPN 评估 | 揭示安全虚假感 | 强化威胁警告 |
| 参数敏感性分析 | 验证鲁棒性 | 支撑工程决策 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 从全球 VPN 封锁政策趋势切入 | 政策/社会背景驱动的安全研究 |
| Gap 提出方式 | 对比学术方法与实际攻击者约束 | 从攻击者可行性角度定位 Gap |
| 方法论证逻辑 | 受 GFW 启发设计 -> 逐步优化参数 | 借鉴真实系统架构设计攻击 |
| 实验组织逻辑 | 控制实验 -> 全流量评估 -> 手动验证 | 层层递进的可信度验证 |
| 局限性讨论方式 | 区分短期缓解和长期防御 | 实用主义的攻防讨论 |
---
type: paper
title_original: "Off-Path Network Traffic Manipulation via Revitalized ICMP Redirect Attacks"
title_cn: "通过复兴ICMP重定向攻击实现路径外网络流量操纵"
authors: [Xuewei Feng, Qi Li, Kun Sun, Zhiyun Qian, Gang Zhao, Xiaohui Kuang, Chuanpu Fu, Ke Xu]
year: 2022
venue: "USENIX Security"
doi: "unknown"
url: "https://www.usenix.org/conference/usenixsecurity22/presentation/feng"
pdf: "00-inbox/PDFs/2022-USENIX-off-path_network_traffic_manipulation_via_revitalized_ICMP_redirect_attacks.pdf"
mineru_md: "02-parsed-markdown/2022-USENIX-off-path_network_traffic_manipulation_via_revitalized_ICMP_redirect_attacks.md"
status: processed
reading_level: L2
research_area: [malicious-traffic-detection, network-security]
task: [attack-detection, network-manipulation]
method: [icmp-attack, protocol-analysis, vulnerability-analysis]
dataset: [internet-measurement, website-survey]
code: "unknown"
relevance: medium
created: "2026-06-03"
updated: "2026-06-03"
---

## §0 基础信息

| 项目 | 内容 |
|------|------|
| 论文全称 | Off-Path Network Traffic Manipulation via Revitalized ICMP Redirect Attacks |
| 作者 | Xuewei Feng, Qi Li, Kun Sun, Zhiyun Qian, Gang Zhao, Xiaohui Kuang, Chuanpu Fu, Ke Xu |
| 机构 | 清华大学, George Mason University, UC Riverside, 北京邮电大学 |
| 发表时间 | 2022 |
| 会议 | USENIX Security Symposium 2022 |
| URL | https://www.usenix.org/conference/usenixsecurity22/presentation/feng |

## §1 一句话总结

揭示ICMP重定向机制与无状态协议之间的根本性安全漏洞，证明路径外攻击者可以利用伪造的ICMP重定向消息在广域网上实施DoS攻击和中间人攻击，影响超过43,000个网站、54,470个DNS解析器和186个Tor节点。

## §2 摘要翻译

**原始摘要：**
ICMP redirect is a mechanism that allows an end host to dynamically update its routing decisions for particular destinations. Previous studies show that ICMP redirect may be exploited by attackers to manipulate the routing of victim traffic. However, it is widely believed that ICMP redirect attacks are not a real-world threat since they can only occur under specific network topologies (e.g., LAN). In this paper, we conduct a systematic study on the legitimacy check mechanism of ICMP and uncover a fundamental gap between the check mechanism and stateless protocols, resulting in a wide range of vulnerabilities. In particular, we find that off-path attackers can utilize a suite of stateless protocols (e.g., UDP, ICMP, GRE, IPIP and SIT) to easily craft evasive ICMP error messages, thus revitalizing ICMP redirect attacks to cause serious damage in the real world, particularly, on the wide-area network. First, we show that off-path attackers can conduct a stealthy DoS attack by tricking various public servers on the Internet into mis-redirecting their traffic into black holes with a single forged ICMP redirect message. For example, we reveal that more than 43K popular websites on the Internet are vulnerable to this DoS attack. In addition, we identify 54.47K open DNS resolvers and 186 Tor nodes on the Internet are vulnerable as well. Second, we show that, by leveraging ICMP redirect attacks against NATed networks, off-path attackers in the same NATed network can perform a man-in-the-middle (MITM) attack to intercept the victim traffic. Finally, we develop countermeasures to throttle these attacks.

**中文翻译：**
ICMP重定向是一种允许终端主机动态更新特定目的地路由决策的机制。先前研究表明ICMP重定向可能被攻击者利用来操纵受害者流量的路由。然而，人们普遍认为ICMP重定向攻击不是现实世界的威胁，因为它们只能在特定网络拓扑（如局域网）下发生。本文对ICMP的合法性检查机制进行了系统研究，发现了检查机制与无状态协议之间的根本性差距，导致广泛存在的漏洞。特别是，作者发现路径外攻击者可以利用一系列无状态协议（如UDP、ICMP、GRE、IPIP和SIT）轻松伪造逃避检测的ICMP错误消息，从而复兴ICMP重定向攻击，在现实世界中造成严重损害，尤其是在广域网上。首先，作者证明路径外攻击者可以通过单个伪造的ICMP重定向消息诱骗互联网上的公共服务器将其流量错误重定向到黑洞，实施隐蔽的DoS攻击。例如，作者发现互联网上超过43,000个流行网站容易受到此DoS攻击。此外，作者还发现54,470个开放DNS解析器和186个Tor节点也容易受到攻击。其次，作者证明通过利用针对NAT网络的ICMP重定向攻击，同一NAT网络中的路径外攻击者可以执行中间人攻击来拦截受害者流量。最后，作者开发了对策来遏制这些攻击。

## §3 方法动机

**痛点问题：**
- 传统观点认为ICMP重定向攻击仅在局域网等特定网络拓扑下可行
- 现有ICMP合法性检查机制与无状态协议之间存在根本性差距
- 广域网上的ICMP重定向攻击可行性未被充分研究

**核心直觉：**
- 无状态协议（UDP、ICMP、GRE等）无法记住先前发送的数据
- 攻击者可以诱骗受害者建立可预测的UDP套接字
- 伪造的ICMP重定向消息可以嵌入已知的UDP数据来逃避检查

**方法动机：**
- ICMP重定向机制在现代操作系统中默认启用
- 无状态协议的内存less特性使得合法性检查存在漏洞
- 广域网上存在大量未过滤伪造ICMP消息的自治系统

## §4 方法设计

**攻击流程：**

```
攻击者视角：
Step 1: 探测受害者开放的UDP端口（NTP、SNMP、DHCP、DNS、TFTP等）
  ↓
Step 2: 诱骗受害者建立到远程目的地的可预测UDP套接字
  ↓
Step 3: 伪造ICMP重定向消息
  - 源IP: 受害者网关IP
  - 目标IP: 受害者IP
  - Type=5 (重定向)
  - 嵌入已知UDP套接字数据（至少28字节）
  ↓
Step 4: 发送伪造消息到受害者
  ↓
Step 5: 受害者验证通过，更新路由表
  ↓
Step 6: 受害者后续流量被重定向到攻击者指定位置

攻击类型：
1. DoS攻击: 重定向到黑洞（禁用转发的主机）
2. MITM攻击: 重定向到攻击者控制的主机
```

**关键漏洞：**
- ICMP合法性检查机制与无状态协议不匹配
- Linux 2.6.20+、FreeBSD 8.2+、Android 4.3+、Mac OS 10.11+受影响
- 超过5,100个AS未实施有效的入口过滤

**攻击效果：**
- 单个伪造ICMP重定向消息即可实施DoS攻击
- 可影响网站、DNS解析器、Tor节点等多种服务
- NAT网络内可实施中间人攻击

**优势：**
- 攻击简单，仅需单个伪造消息
- 影响范围广，覆盖多种操作系统和服务
- 可在广域网上实施，不受网络拓扑限制

**局限：**
- 需要IP地址欺骗能力（约1/4的AS允许）
- 需要受害者使用无状态协议
- 需要受害者未禁用ICMP重定向机制

## §5 与其他方法对比

**创新点：**
1. 首次发现ICMP合法性检查机制与无状态协议之间的根本性差距
2. 证明ICMP重定向攻击可在广域网上实施，打破"仅限局域网"的传统认知
3. 系统性测量互联网上易受攻击的网站、DNS解析器和Tor节点
4. 开发并评估防御对策

**与基线对比：**
- 对比方法:
  - 传统ICMP重定向攻击（仅限局域网）
  - 基于UDP的ICMP攻击（Linux 2.6.20前有效）
  - 基于ICMP echo的攻击（Kulas, 2007）
- 改进点:
  - 适用范围: 从局域网扩展到广域网
  - 攻击效果: 影响更多操作系统版本
  - 防御难度: 利用协议设计漏洞，难以完全防御

## §6 实验表现

**测量数据：**
- 互联网测量: 超过5,100个AS未实施入口过滤
- 网站调查: 43,000+流行网站易受DoS攻击
- DNS解析器: 54,470个开放DNS解析器易受攻击
- Tor节点: 186个Tor中继节点易受攻击

**实验结果：**
- ICMP重定向消息可在互联网上跨AS转发
- 跨大洲转发成功率高（见Table 1）
- DoS攻击可在单消息内完成
- MITM攻击可在NAT网络内实施

**受影响系统：**
- Linux 2.6.20及更高版本
- FreeBSD 8.2及更高版本
- Android 4.3及更高版本
- Mac OS 10.11及更高版本

**防御对策评估：**
- 网络设置更改: 阻止伪造的ICMP重定向消息
- 协议更改: 在UDP中嵌入秘密进行认证
- 严格区分无状态和有状态协议，禁用无状态协议的ICMP重定向

## §7 学习与应用

**开源情况：**
- 论文未明确说明是否开源代码

**复现要点：**
- 需要IP地址欺骗能力
- 需要探测受害者开放的UDP端口
- 需要构造符合格式的伪造ICMP重定向消息
- 需要验证受害者操作系统版本

**迁移价值：**
- 漏洞分析方法可应用于其他协议安全性研究
- 测量方法可用于互联网安全态势评估
- 防御对策可指导网络安全部署

## §8 总结

**核心思想：** 发现ICMP合法性检查机制与无状态协议之间的根本性差距，复兴ICMP重定向攻击，证明其可在广域网上实施DoS和MITM攻击。

**快速流程：**
```
漏洞发现 → ICMP检查机制与无状态协议不匹配
    ↓
攻击设计 → 伪造ICMP重定向消息嵌入已知UDP数据
    ↓
互联网测量 → 43K网站、54K DNS、186 Tor节点易受攻击
    ↓
攻击验证 → DoS攻击 + MITM攻击
    ↓
防御对策 → 网络过滤 + 协议改进 + 状态区分
```

## §9 知识链接

- [[malicious-traffic-detection]] - 恶意流量检测技术
- [[network-security]] - 网络安全基础
- [[protocol-analysis]] - 协议安全分析
- [[attack-detection]] - 攻击检测方法
- [[vulnerability-analysis]] - 漏洞分析方法
- [[internet-measurement]] - 互联网测量技术
- [[dos-attack]] - DoS攻击与防御
- [[man-in-the-middle]] - 中间人攻击

## §10 证据记录

| 声明 | 证据 | 证据强度 |
|------|------|----------|
| ICMP检查机制与无状态协议存在根本性差距 | Linux源码分析（Fig 3） | 强（代码分析） |
| 43,000+网站易受DoS攻击 | 互联网测量数据 | 强（实测数据） |
| 54,470个DNS解析器易受攻击 | 互联网扫描结果 | 强（实测数据） |
| ICMP重定向消息可在互联网上转发 | 跨AS测量实验（Table 1） | 强（实验数据） |
| 受影响操作系统版本广泛 | 系统版本测试 | 强（实验验证） |

## §11 原始资料链接

- PDF: `00-inbox/PDFs/2022-USENIX-off-path_network_traffic_manipulation_via_revitalized_ICMP_redirect_attacks.pdf`
- MinerU MD: `02-parsed-markdown/2022-USENIX-off-path_network_traffic_manipulation_via_revitalized_ICMP_redirect_attacks.md`

## §12 后续问题

1. 如何在不破坏ICMP重定向机制正常功能的情况下防御此类攻击？
2. 无状态协议的安全性如何系统性提升？
3. 该攻击对现代云环境和CDN网络的影响如何？
4. IPv6环境下是否存在类似的漏洞？
5. 如何设计更安全的路由更新机制？

---
type: paper
title_original: "Detection of Encrypted Tunnels across Network Boundaries"
title_cn: "跨网络边界加密隧道检测"
authors: ["Maurizio Dusi", "Manuel Crotti", "Francesco Gringoli", "Luca Salgarelli"]
year: 2008
venue: "IEEE ICC 2008"
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2008-ICC-Detection_of_Encrypted_Tunnels_Across_Network_Boundaries.pdf"
mineru_md: "02-parsed-markdown/2008-ICC-Detection_of_Encrypted_Tunnels_Across_Network_Boundaries.md"
status: processed
reading_level: L2
research_area: ["network security", "traffic classification", "encrypted traffic analysis"]
task: ["tunnel detection", "traffic classification", "anomaly detection"]
method: ["statistical fingerprinting", "naive Bayes", "histogram density estimation", "Parzen kernel method", "anomaly score"]
dataset: ["campus network traffic traces"]
code: unknown
relevance: medium
created: "2026-05-27"
updated: "2026-05-27"
---

# Detection of Encrypted Tunnels across Network Boundaries

## 0. 论文基础信息

| 项目              | 内容                                                                                                   |
| --------------- | ---------------------------------------------------------------------------------------------------- |
| 原文标题            | Detection of Encrypted Tunnels across Network Boundaries                                             |
| 中文标题            | 跨网络边界加密隧道检测                                                                                          |
| 作者              | Maurizio Dusi, Manuel Crotti, Francesco Gringoli, Luca Salgarelli                                    |
| 年份              | 2008                                                                                                 |
| 会议/期刊           | IEEE International Conference on Communications (ICC 2008)                                           |
| 研究方向            | 网络安全、加密流量分类                                                                                          |
| 任务类型            | 加密 SSH 隧道中的 protocol tunneling 检测                                                                    |
| 方法关键词           | statistical fingerprinting, naive Bayes, histogram density estimation, anomaly score, shifted window |
| 数据集             | 校园网络真实流量（约4000个合法SSH会话 + 约12000个评估会话）                                                                |
| 是否开源            | 否                                                                                                    |
| PDF             | 00-inbox/PDFs/2008-ICC-Detection_of_Encrypted_Tunnels_Across_Network_Boundaries.pdf                  |
| MinerU Markdown | 02-parsed-markdown/2008-ICC-Detection_of_Encrypted_Tunnels_Across_Network_Boundaries.md              |

## 1. 一句话总结

> 通过统计协议指纹（packet size + inter-arrival time 的直方图密度估计）检测加密 SSH 隧道中的非合法 tunneling 流量，合法 SSH/SCP 识别率超过 98%，隧道阻断率接近 90%。

## 2. 摘要翻译

### 2.1 摘要原文

The use of covert application-layer tunnels to bypass security gateways has become quite popular in recent years. By encapsulating blocked or controlled protocols such as peer-to-peer, chat and e-mail into others allowed by the security policies, such as HTTP, SSH or even DNS, both legitimate and malicious users can effectively neutralize many security restrictions enforced at the network edge. Traditional firewalling techniques, based on Application Layer Gateways and even pattern-matching mechanisms are becoming practically useless as tunneling tools grow more sophisticated.

In this paper we propose an effective solution to this problem based on a statistical traffic classification technique. Our mechanism relies on the creation of a statistical fingerprint of legitimate usage of a given protocol, such as regular remote interactive logins or secure copying activities. Such fingerprint can then be used to detect with high accuracy non-legitimate sessions, i.e., sessions that tunnel other protocols. Results from experiments conducted on a live network suggest that the technique can be very effective, even when the application layer protocol used as a tunnel is encrypted, such as in the case of SSH.

### 2.2 摘要中文翻译

近年来，利用隐蔽的应用层隧道（covert application-layer tunnel）绕过安全网关的做法日益普遍。用户可以将被封锁或受控的协议（如 P2P、聊天、邮件）封装到安全策略允许的协议（如 HTTP、SSH 或 DNS）中，从而有效规避网络边界的安全限制。传统的防火墙技术（基于 ALG 和模式匹配机制）在隧道工具日益复杂的情况下几乎失效。

本文提出一种基于统计流量分类技术的有效解决方案。该机制通过为协议的合法使用（如远程交互登录或安全文件拷贝）建立统计指纹（statistical fingerprint），然后利用该指纹高精度地检测非合法会话（即隧道其他协议的会话）。在真实网络上的实验表明，该技术非常有效，即使隧道使用的应用层协议是加密的（如 SSH）。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- SSH 隧道可以将任意 TCP 流量加密封装，使得基于 payload 的 DPI（Deep Payload Inspection）方法完全失效
- 网络管理员面临两难困境：允许 SSH 则失去对 tunneling 的控制，完全封锁 SSH 则影响合法远程登录和文件传输需求
- 作者此前已经在 HTTP 隧道检测方面取得成果（ICC 2007），希望将统计方法扩展到加密 SSH 隧道场景

### 3.2 现有方法的痛点和不足

| 现有方法 | 痛点 |
|---|---|
| Deep Payload Inspection (DPI) | 对加密流量完全无效；无法为 tunneling 流量构建有效的正则表达式 |
| Application Layer Gateway (ALG) | 被 SSH 加密欺骗，无法检查 payload 内容 |
| 基于端口的防火墙规则 | SSH tunneling 使用同一端口（22），无法区分合法和隧道流量 |
| 已有的统计分类方法（hierarchical clustering, Nearest Neighbor, Bayesian 等） | 尚未被用于检测 tunneling 流量以加强网络边界策略 |

### 3.3 论文的研究假设或核心直觉

- **核心假设**：即使流量被加密，IP 层的统计特征（packet size 和 inter-arrival time）仍然足以推断产生流量的应用协议类型
- **关键直觉**：合法 SSH 使用（远程交互登录、安全文件拷贝）具有可区分的统计行为模式，与通过 SSH 隧道传输其他协议（如 P2P、SMTP、POP3、Chat）的行为显著不同
- 加密只隐藏了 payload 内容，但无法隐藏流量的统计行为特征

## 4. 方法设计

### 4.1 方法整体流程

1. **训练阶段**：收集合法 SSH/SCP 流量，提取 packet size 和 inter-arrival time 特征，通过直方图方法建立协议指纹（protocol fingerprint）
2. **平滑处理**：对直方图进行 Gaussian filtering（Parzen method），消除离散分布的边界效应
3. **检测阶段**：对新到达的流计算 anomaly score，与阈值 T 比较，判断是否为合法 SSH 流量或 tunneling 流量
4. **SSH 特殊处理**：使用 shifted window 跳过 SSH 认证阶段的包，只对数据交换阶段的包计算 anomaly score

### 4.2 详细 Pipeline（表格形式）

| 步骤 | 描述 | 技术细节 |
|---|---|---|
| 1. 数据采集 | 在校园网边界路由器上用 Tcpdump 抓包 | 只采集携带 TCP payload 的包，丢弃无 payload 包 |
| 2. 特征提取 | 从每个流中提取 packet size s 和 inter-arrival time delta_t | s 在 [40, 1500] bytes 范围内离散取值；delta_t 在对数量化后从 10^-7 到 10^3 秒 |
| 3. 模式表示 | 将每个流表示为 2 x r 矩阵 | x = (s_1,...,s_r; delta_t_1,...,delta_t_r)，r 为流中的包数减1 |
| 4. 指纹构建 | 用直方图方法对合法流量做非参数密度估计 | 1461 x 1001 的矩阵，假设连续 (s, delta_t) 对独立 |
| 5. 高斯平滑 | 对直方图应用 Gaussian kernel 平滑 | 解决直方图的不连续性问题，处理噪声（如 RTT 变化） |
| 6. 异常评分 | 计算待分类流相对于指纹的 anomaly score | 公式：S = sum(epsilon / p(x_i|w_1)) / min(r, L) |
| 7. 分类决策 | anomaly score < T 则判定为合法，否则判定为 tunneling | 最优 T = 3/8，窗口 [6, 13] |

### 4.3 模型结构或系统模块（表格形式）

| 模块 | 功能 | 输入 | 输出 |
|---|---|---|---|
| 训练集采集器 | 收集合法 SSH/SCP 会话 | 校园网边界流量 | 标注的合法流量集合 |
| 特征提取器 | 从 TCP 流中提取 (s, delta_t) 序列 | 原始 IP 包 | 模式向量 x |
| 指纹生成器 | 用直方图 + Gaussian 平滑构建协议指纹 | 训练集模式向量 | 指纹矩阵 M（分为 M_client 和 M_server） |
| SSH 认证过滤器 | 识别并跳过 SSH 认证阶段的包 | SSH 流 | shifted window 起始位置 n_0 |
| 异常评分计算 | 逐包计算流的 anomaly score | 流模式 + 指纹 | anomaly score S |
| 分类决策器 | 根据阈值 T 判定合法/隧道 | anomaly score + T | 分类结果（合法 / UNKNOWN） |

### 4.4 公式、算法和机制解释

**直方图密度估计**：

$$\hat{p}(\vec{x}) = \frac{n_j}{\sum_{j \in N} n_j \cdot dV}$$

其中 n_j 为落入当前单元格的样本数，dV 为单元格体积，N 为所有单元格。矩阵大小为 1461 x 1001（对应 packet size 的 1461 个可能值和 delta_t 量化的 1001 个区间）。

**Anomaly Score 计算**：

$$S(\vec{x} | \omega_1) = \sum_{i=1}^{\min(r,L)} \frac{\varepsilon}{p(x_i | \omega_1) \cdot \min(r, L)}$$

其中 p(x_i|omega_1) = max(epsilon, M_1(s_i, delta_t_i))，epsilon = 10^-12。S 取值范围 [0, 1]。每个 (s, delta_t) 对的贡献在 [0, 1/min(r,L)] 范围内。

**分类决策规则**：

$$\vec{x} \in \begin{cases} \omega_1 & \text{if } S(\vec{x}|\omega_1) < T \\ \text{UNKNOWN} & \text{otherwise} \end{cases}$$

**Shifted Window（针对 SSH）**：

$$S_{[n_0 \rightarrow n]}(\vec{x}|\omega_1) = \sum_{i=n_0}^{n} \frac{\varepsilon}{p(x_i|\omega_1) \cdot (n - n_0)}$$

n_0 设为 SSH MSG NEWKEYS 消息之后的第 3 个 F_client 包（假设使用 public-key 两轮认证）。

**关键机制解释**：
- **独立性假设**：假设连续的 (s, delta_t) 对之间相互独立，将 N^r 的复杂度降为 r*N，极大降低了计算复杂度，同时实验效果优异
- **最大模式长度 L**：限制观察的包数，不需要等到流结束即可做出分类判断
- **epsilon 保底**：防止某对落在零值单元格导致分数趋近无穷

### 4.5 方法优势

1. **对加密流量有效**：仅依赖 IP 层统计特征，无需 payload 内容
2. **低误报率**：可配置阈值以达到任意预设的 false-positive 目标（本文设定 <1%）
3. **实时性**：仅需观察前 L+1 个包即可做出判断，无需等待流结束
4. **计算简单**：独立性假设将复杂度大幅降低，直方图查表操作高效
5. **可扩展**：已验证可用于 HTTP 隧道（前作）和 SSH 隧道，理论上适用于任何加密隧道协议

### 4.6 方法不足

1. **n_0 需要预设**：必须假设统一的 SSH 认证方式（如 public-key 两轮认证），认证错误会被误判
2. **无法识别被隧道的具体协议**：只能判断是否存在 tunneling，不能区分隧道中传输的是 POP3、HTTP 还是 SMTP
3. **静态 shifted window**：无法应对先交换若干合法包再开启隧道的攻击
4. **训练集依赖**：需要收集大量纯净的合法 SSH 流量，训练集质量直接影响指纹质量
5. **单一协议假设**：只建模了合法 SSH 使用的"一类"行为，未考虑多种合法使用模式的差异

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 对比维度 | DPI / Pattern Matching | 本文方法 (Tunnel Hunter) |
|---|---|---|
| 分析层面 | 应用层 payload | IP 层统计特征 |
| 对加密流量 | 完全无效 | 有效 |
| 分类原理 | 确定性模式匹配 | 统计模式识别 |
| 需要 payload | 是 | 否 |
| 实时性 | 高 | 高（前 L+1 包即可判断） |

与已有统计分类方法（hierarchical clustering, Nearest Neighbor, Bayesian 等）的本质区别在于：本文聚焦于 **tunneling 检测** 而非通用协议分类，通过建立单一合法类别的指纹来检测偏离行为（anomaly detection 思路）。

### 5.2 创新点分析（表格形式）

| 创新点 | 说明 |
|---|---|
| Protocol Fingerprint 概念 | 用合法协议使用行为的统计指纹来检测异常（tunneling），无需建模所有可能的隧道协议 |
| SSH shifted window 机制 | 跳过 SSH 认证阶段，只对数据交换阶段的包进行分类，解决了 SSH 认证过程干扰分类的问题 |
| 加密隧道检测的可行性验证 | 首次在真实网络上验证统计方法可有效检测加密 SSH 隧道中的 tunneling |
| 从 HTTP 到 SSH 的扩展 | 在前作 HTTP 隧道检测基础上，证明了方法对加密隧道的通用性 |

### 5.3 适用场景

- 企业网络安全策略执行：允许 SSH 远程登录和文件传输，但阻止通过 SSH 隧道传输 P2P、邮件、聊天等协议
- 检测受控网络中的恶意 tunneling（如被攻陷的内网主机通过 SSH 隧道外传数据）
- 补充现有 ALG 的不足，增强对加密 tunneling 的检测能力

### 5.4 方法对比表

| 方法 | 是否处理加密流量 | 是否针对 tunneling | 分类基础 | 误报率控制 |
|---|---|---|---|---|
| DPI (Bro, Snort) | 否 | 否 | payload pattern | 不适用 |
| Hierarchical Clustering | 是（理论上） | 否 | 流统计特征 | 未报告 |
| Nearest Neighbor / LDA | 是（理论上） | 否 | 流统计特征 | 未报告 |
| Levine et al. (cross-correlation) | 是 | 否（针对网站指纹） | 包长度/时间 profile | 未报告 |
| Wright et al. | 是 | 部分（IPSec隧道流数量推断） | 流统计特征 | 未报告 |
| **Tunnel Hunter (本文)** | **是** | **是** | **packet size + inter-arrival time 指纹** | **<1% FP** |

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **网络环境**：校园网 100Base-TX 链路，连接边界路由器与 Internet，约 1000 用户
- **训练阶段**：三周内收集约 4000 个合法 SSH/SCP 会话，用于构建指纹
- **评估阶段**：另外收集约 12660 个会话（合法 + 隧道）
- **SSH 隧道设置**：使用 OpenSSH tunnel 工具，一端在校园网 Mac OS X 工作站，另一端在多个远程服务器
- **P2P 隧道**：额外设置 Linux 网关将 P2P 流量封装进 SSH 隧道，使用 Iptables 进行 masquerading
- **合法流量采集**：来自多个操作系统（Mac OS X, Linux, Windows），连接到多个不同网络位置（意大利罗马、特伦托、美国犹他州、家庭 DSL）
- **SSH 配置约束**：public-key 认证、启用公钥验证、禁用压缩

### 6.2 数据集

| 数据集 | 会话数 | 用途 |
|---|---|---|
| 合法 SSH 交互会话 | ~600（评估集） | 正样本 |
| 合法 SCP 批量传输会话 | ~1700（评估集） | 正样本 |
| POP3 over SSH | 2360 | 负样本（隧道） |
| SMTP over SSH | 4300 | 负样本（隧道） |
| Chat over SSH | 2100 | 负样本（隧道） |
| P2P (BitTorrent) over SSH | 1600 | 负样本（隧道） |
| 训练集总计 | ~4000 | 指纹构建 |

### 6.3 Baseline

论文未设置显式的 baseline 对比方法，主要是因为此前没有已发表的针对加密 SSH 隧道 tunneling 检测的统计方法。作者将合法 SSH/SCP 流量作为正样本基线，验证 tunneling 流量可以被有效区分。

### 6.4 评价指标

- **Hit ratio（命中率）**：正确分类的会话比例
  - 对合法 SSH/SCP：正确识别为合法的比例（越高越好，即低 false-positive）
  - 对 tunneling 流量：正确检测为隧道的比例（即 blocking rate / true-positive rate）
- **False-positive rate**：合法流量被误判为隧道的比例，设定目标 <1%

### 6.5 关键实验结果（表格形式）

| 协议类型 | Hit Ratio | 会话数 | 含义 |
|---|---|---|---|
| SSH（合法交互） | 98.95% | 600 | 仅 1.05% 误报 |
| SCP（合法文件传输） | 99.69% | 1700 | 仅 0.31% 误报 |
| POP3 over SSH | 87.89% | 2360 | 87.89% 被正确检测为隧道 |
| SMTP over SSH | 99.93% | 4300 | 几乎全部被检测为隧道 |
| Chat over SSH | 88.31% | 2100 | 88.31% 被正确检测为隧道 |
| P2P over SSH | 88.77% | 1600 | 88.77% 被正确检测为隧道 |

**最优参数**：T = 3/8，窗口 [6, 13]，仅使用 F_client 方向

### 6.6 优势最明显的场景

- **SMTP over SSH**：检测率高达 99.93%，因为 SMTP 的流量模式与 SSH/SCP 差异最大
- **合法 SSH/SCP 保护**：超过 98% 的合法流量不被误判，满足企业网络管理需求
- 在控制 false-positive <1% 的前提下，各类 tunneling 的最差检测率也接近 90%

### 6.7 局限性

1. **POP3 和 Chat 隧道检测率相对较低**（~88%）：这些协议的流量模式可能与 SSH/SCP 有部分重叠
2. **n_0 预设限制**：假设统一的 public-key 两轮认证，不支持密码认证或其他认证方式
3. **无法识别具体隧道协议**：只做二分类（合法 vs 隧道），不能告诉你隧道里跑的是什么
4. **静态窗口**：无法应对"先正常通信再开隧道"的对抗策略
5. **训练集采集周期长**：需要三周时间收集足够多的合法流量
6. **环境依赖**：不同网络环境的最优参数可能不同，需要重新调优

## 7. 学习与应用

### 7.1 是否开源？

否。论文未提供代码或开源实现。

### 7.2 复现关键步骤

1. **采集合法 SSH/SCP 训练流量**：在网络边界用 Tcpdump 抓包，需确保无 tunneling 流量混入
2. **特征提取**：从每个 TCP 流中提取 (packet_size, inter_arrival_time) 序列，丢弃无 TCP payload 的包
3. **识别 SSH 认证阶段**：寻找 SSH MSG NEWKEYS 消息，标记认证结束位置
4. **构建指纹矩阵**：对合法流量的 (s, delta_t) 对建直方图（1461 x 1001），应用 Gaussian 平滑
5. **设置参数**：n_0（认证结束后的偏移）、T（异常阈值）、L（最大观察包数）
6. **分类**：对新流从 n_0 开始逐包计算 anomaly score，与 T 比较

### 7.3 关键超参数、预处理和训练细节

| 参数 | 值/说明 |
|---|---|
| Threshold T | 3/8（允许 3/8 的包落在零值区域） |
| Shifted window 起始 n_0 | SSH MSG NEWKEYS 后第 3 个 F_client 包 |
| 观察窗口 | [6, 13]（第 6 到第 13 对） |
| 最大模式长度 L | 论文未明确说明具体值 |
| epsilon | 10^-12（防止除零） |
| delta_t 量化 | 对数量化，10^-7 到 10^3 秒，步长 10^-2 |
| packet size 范围 | [40, 1500] bytes（以太网） |
| 独立性假设 | 连续 (s, delta_t) 对之间独立 |
| 认证方式 | public-key（两轮 round-trip） |
| 压缩 | 禁用 |

### 7.4 能否迁移到其他任务？

- **HTTP 隧道检测**：作者前作已验证可行（ICC 2007），方法可直接迁移
- **DNS 隧道检测**：理论上可行，但 DNS 隧道吞吐量低，训练数据可能不足
- **其他加密协议的异常检测**：如 HTTPS 中的异常行为、VPN 隧道中的协议检测，核心思路（统计指纹 + anomaly score）可迁移
- **恶意软件流量检测**：作者在结论中提到计划将此技术用于检测被攻陷机器的外传隧道流量
- **网站指纹识别**：与 Levine et al. 的工作思路相近，但应用目标不同

### 7.5 对我的研究有什么启发？

1. **加密不等于安全**：即使 payload 被加密，IP 层统计特征仍然泄露大量信息，这对隐私研究和安全研究都有启示
2. **异常检测范式**：只建模"正常"行为的 fingerprint，检测偏离者，是一种简洁有效的范式，适用于流量分类中的 open-set 问题
3. **特征工程的简洁性**：仅用 packet size 和 inter-arrival time 两个特征就能达到很好的效果，说明好的特征选择比复杂的模型更重要
4. **参数调优思路**：通过在验证集上固定 false-positive 目标来优化阈值，是实际部署中的实用方法
5. **Shifted window 的思想**：在序列数据中跳过无关段（如认证阶段），聚焦于有信息量的部分，可推广到其他序列分类任务

## 8. 总结

### 8.1 核心思想（不超过20字）

用合法SSH的统计指纹检测加密隧道中的异常流量。

### 8.2 速记版 Pipeline（3-5步）

1. 采集合法 SSH/SCP 流量，提取 (packet_size, inter_arrival_time) 序列
2. 用直方图 + Gaussian 平滑建立协议指纹 M（client 和 server 各一个）
3. 跳过 SSH 认证阶段（shifted window），从数据包开始计算 anomaly score
4. anomaly score < 阈值 T 判定为合法，否则判定为 tunneling
5. 通过验证集优化 T 和 n_0，使 false-positive < 1%

## 9. Obsidian 知识链接

### 9.1 相关概念

- Encrypted Traffic Classification - 加密流量分类
- Network Traffic Fingerprinting - 网络流量指纹
- Anomaly Detection - 异常检测
- Application Layer Gateway (ALG) - 应用层网关
- Deep Payload Inspection (DPI) - 深度包检测
- SSH Protocol - SSH 协议
- Protocol Tunneling - 协议隧道

### 9.2 相关方法

- Naive Bayes Classifier - 朴素贝叶斯分类器
- Histogram Density Estimation - 直方图密度估计
- Parzen Window / Kernel Density Estimation - Parzen 窗 / 核密度估计
- Statistical Pattern Recognition - 统计模式识别
- Cross-correlation Traffic Analysis - 互相关流量分析（Levine et al.）

### 9.3 相关任务

- SSH Tunnel Detection - SSH 隧道检测
- HTTP Tunnel Detection - HTTP 隧道检测
- Covert Channel Detection - 隐蔽信道检测
- Network Security Policy Enforcement - 网络安全策略执行
- Malware Traffic Detection - 恶意软件流量检测

### 9.4 可更新的综述页面

- [[survey-encrypted-traffic-analysis]]
- Network Tunneling Detection Methods
- Statistical Methods for Traffic Analysis

### 9.5 可加入的对比表

- Tunnel Detection Methods Comparison
- Encrypted Traffic Classification Methods

## 10. 证据记录（表格形式）

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E1 | 实验结果 | SSH 合法会话 hit ratio 98.95%（600会话） | Table I |
| E2 | 实验结果 | SCP 合法会话 hit ratio 99.69%（1700会话） | Table I |
| E3 | 实验结果 | POP3 over SSH 检测率 87.89%（2360会话） | Table I |
| E4 | 实验结果 | SMTP over SSH 检测率 99.93%（4300会话） | Table I |
| E5 | 实验结果 | Chat over SSH 检测率 88.31%（2100会话） | Table I |
| E6 | 实验结果 | P2P over SSH 检测率 88.77%（1600会话） | Table I |
| E7 | 参数设定 | 最优阈值 T=3/8，窗口 [6,13]，仅用 F_client | Section VI |
| E8 | 方法假设 | 假设连续 (s, delta_t) 对独立，复杂度从 N^r 降为 r*N | Section IV-C |
| E9 | 方法假设 | SSH 认证使用 public-key 两轮认证，n_0 设为 NEWKEYS 后第3包 | Section IV-E |
| E10 | 训练数据 | 三周内收集约4000个合法SSH会话用于指纹构建 | Section V |

## 11. 原始资料链接

- 论文发表于 IEEE ICC 2008
- 作者单位：DEA, Universita degli Studi di Brescia, Italy
- 前作：Detecting HTTP Tunnels with Statistical Mechanisms (ICC 2007)
- 相关工具：OpenSSH (http://www.openssh.org), Tcpdump (http://www.tcpdump.org)
- 项目资助：Italian MIUR, PRIN project RECIPE

## 12. 后续问题

1. **动态 shifted window**：如何自动检测 SSH 认证结束位置，而不是预设 n_0？论文提到这是 future work
2. **隧道协议识别**：能否在检测到 tunneling 的基础上进一步识别被隧道的具体协议？论文提到需要进一步研究
3. **对抗性攻击**：如果攻击者故意模仿合法 SSH 的统计特征（通过流量整形），该方法是否仍然有效？
4. **与其他加密协议的兼容性**：该方法在 TLS/HTTPS、WireGuard 等现代加密协议上的表现如何？
5. **深度学习方法对比**：与近年来基于 CNN/LSTM 的加密流量分类方法相比，这种传统统计方法的优劣如何？
6. **大规模部署可行性**：在高速网络（10Gbps+）上，该方法的计算开销是否可接受？
7. **隐私影响**：该技术的逆向应用（如网站指纹攻击）对用户隐私的影响如何？

---
type: paper
title_original: "HOLMES & WATSON: A Robust and Lightweight HTTPS Website Fingerprinting through HTTP Version Parallelism"
title_cn: "HOLMES & WATSON: 利用 HTTP 版本并行性的鲁棒轻量级 HTTPS 网站指纹识别"
authors: ["Yifei Cheng", "Yujia Zhu", "Baiyang Li", "Peishuai Sun", "Yong Ding", "Xinhao Deng", "Qingyun Liu"]
year: 2025
venue: "WWW 2025"
doi: "10.1145/3696410.3714578"
url: "https://doi.org/10.1145/3696410.3714578"
pdf: "00-inbox/Aug_inbox/2025-WWW-HOLMES&WATSON__A_Robust_and_Lightweight_HTTPS_Website_Fingerprinting_through_HTTP_Version_Parallelism.pdf"
mineru_md: "02-parsed-markdown/2025-WWW-HOLMES&WATSON__A_Robust_and_Lightweight_HTTPS_Website_Fingerprinting_through_HTTP_Version_Parallelism.md"
status: processed
reading_level: L3
research_area: ["network privacy", "HTTPS website fingerprinting", "application-layer features", "HTTP version parallelism"]
task: ["website fingerprinting", "encrypted traffic analysis", "traffic classification"]
method: ["HTTP version inference", "protocol state machine", "H123 fingerprint", "lazy learning", "k-NN", "Wasserstein distance", "LCSS distance", "Gini coefficient"]
dataset: ["self-collected HTTPS dataset (1.5TB+, 220k samples, 80k websites, 12 scenarios)"]
code: "https://github.com/2654400439/H123-Website-Fingerprinting"
relevance: high
created: "2026-08-17"
updated: "2026-08-17"
---

# HOLMES & WATSON: A Robust and Lightweight HTTPS Website Fingerprinting through HTTP Version Parallelism

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | HOLMES & WATSON: A Robust and Lightweight HTTPS Website Fingerprinting through HTTP Version Parallelism |
| 中文标题 | HOLMES & WATSON: 利用 HTTP 版本并行性的鲁棒轻量级 HTTPS 网站指纹识别 |
| 作者 | Yifei Cheng、Yujia Zhu（通讯）、Baiyang Li、Peishuai Sun、Yong Ding、Qingyun Liu（中科院信工所/国科大网安学院）、Xinhao Deng（清华大学网研院） |
| 年份 | 2025 |
| 会议/期刊 | WWW 2025（ACM Web Conference 2025，2025-04-28~05-02，澳大利亚悉尼），15 页 |
| 研究方向 | HTTPS 网站指纹攻击、应用层特征、协议版本并行性、轻量级分类 |
| 任务类型 | 对真实 HTTPS 流量的网站指纹识别攻击（closed-world + open-world） |
| 方法关键词 | HTTP version parallelism, H123 fingerprint, 协议状态机, lazy learning, Wasserstein 距离, LCSS, Gini 系数 |
| 数据集 | 自建 1.5TB+ HTTPS 流量数据集：220,000 样本、80,000 网站、12 个实验场景（2024-07~09，10 台 AWS 服务器采集） |
| 是否开源 | 是（代码 GitHub: 2654400439/H123-Website-Fingerprinting；数据集公开） |
| PDF | 00-inbox/Aug_inbox/2025-WWW-HOLMES&WATSON__A_Robust_and_Lightweight_HTTPS_Website_Fingerprinting_through_HTTP_Version_Parallelism.pdf |
| MinerU Markdown | 02-parsed-markdown/2025-WWW-HOLMES&WATSON__A_Robust_and_Lightweight_HTTPS_Website_Fingerprinting_through_HTTP_Version_Parallelism.md |

---

## 1. 一句话总结

> 发现并利用"HTTP 版本并行性"这一应用层信号（仅 HTTP/2 资源数量一项就泄露 4.28 bit 信息、超过 98% 已知特征）：HOLMES 免解密提取 H123 指纹（各连接 HTTP 版本 × 资源数量矩阵），WATSON 用 Wasserstein + LCSS 混合距离的惰性学习分类，每网站仅 1 个参考样本即在真实 HTTPS 场景下平均达 87.7% 准确率，较 SOTA 提升超 15%，并对网络条件变化与概念漂移鲁棒。

---

## 2. 摘要翻译

### 2.1 摘要原文

Website Fingerprinting (WF) is a traffic analysis technique that aims to identify websites visited by users through the analysis of encrypted traffic patterns. Existing approaches often exhibit limited robustness against network variability and concept drift, resulting in significant performance degradation under real-world HTTPS conditions. Moreover, these methods typically require large-scale training datasets and substantial computational resources, which further increases the complexity of deployment. In this paper, we propose HOLMES, a novel approach that exploits HTTP version parallelism to extract enhanced application-layer features. These features, including the number of web resources transmitting in various HTTP versions, expose up to 4.28 bits of information—surpassing 98% of previously reported features and demonstrate increased stability across varying network conditions. Complementary to this, we introduce WATSON, a lightweight classification method based on lazy learning, which substantially reduces the dependency on large training datasets. To further enhance the identification accuracy, we incorporate two fingerprint-specific distance metrics that ensure high intra-class similarity. Our experimental evaluation demonstrates that HOLMES & WATSON significantly enhance both robustness and efficiency, achieving an average accuracy of 87.7% with only a single sample per website, marking an improvement of over 15% compared to state-of-the-art methods.

### 2.2 摘要中文翻译

网站指纹（WF）是一种通过分析加密流量模式来识别用户访问网站的技术。现有方法对网络条件变化与概念漂移的鲁棒性有限，在真实 HTTPS 环境下性能显著下降；此外，这些方法通常需要大规模训练数据集和大量计算资源，进一步增加了部署复杂度。本文提出 HOLMES：利用 HTTP 版本并行性提取增强的应用层特征。这些特征（包括以不同 HTTP 版本传输的 Web 资源数量）最多泄露 4.28 bit 信息，超过 98% 的已报道特征，并且在多变网络条件下表现出更高的稳定性。与之配套，本文提出 WATSON——基于惰性学习（lazy learning）的轻量级分类方法，大幅降低对大规模训练数据的依赖。为提升识别精度，我们引入两种面向指纹的距离度量以保证类内相似度。实验表明，HOLMES & WATSON 显著提升了鲁棒性与效率：每网站仅需 1 个样本即达到平均 87.7% 的准确率，比现有最先进方法提升超过 15%。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 现有 WF 研究集中在 Tor 匿名网络，HTTPS 场景研究相对少且假设不现实：稳定网络条件、无概念漂移、大量标注数据，均与真实 HTTPS 流量不符（§1）。
- Juarez 等人的工作表明概念漂移使 WF 精度大幅下降；本文复现实验显示网络条件变化下准确率下降约 20%（§4.4）。
- 典型 WF 分类器训练需 10 天以上的数据采集（引用 Triplet Fingerprinting [71]），部署成本高（§1）。
- 作者认为根源在**特征提取层**：现有方法多用传输层特征（包方向序列、包间延迟），远离网站资源的真实特征，易受网络条件影响且稀疏碎片化，需要复杂模型和大数据（§1、Figure 1）。
- 观察到现代 Web 生态的**HTTP 版本并行性**：多个 HTTP 版本（1.1/2/3）无需强制升级而并存，网站自行选择，形成各网站不同的模式（§2.1），且 80%+ 网站并行使用 ≥2 个版本（附录 B 测量）。

### 3.2 现有方法的痛点和不足

| 痛点 | 具体表现 | 论文依据 |
|---|---|---|
| 对网络条件变化鲁棒性差 | 跨网络训练/测试时精度下降明显（带宽变化影响 > 丢包变化） | §4.4, Figure 5 |
| 对概念漂移鲁棒性差 | 网站内容更新 30 天后 k-FP+ 从 98% 掉到 72% | §4.4, Figure 6(b) |
| 依赖大规模标注数据 | 需 >10 天采集；少样本下深度方法精度崩（DF 在 N=1 时仅 16.7%~38.6%） | §1, Table 2 |
| 特征层选择不当 | 传输层特征（方向/时序）易受网络干扰，稀疏且需复杂模型 | §1, Figure 1 |

### 3.3 论文的研究假设或核心直觉

- 核心直觉：**内容加密不改变 HTTP 请求-响应模式**，HTTP 版本与资源数量可从流量元数据中推断（§3.1）；而 HTTP 版本并行性是现代互联网"不可避免、普遍存在、有区分度"的现象（§2.1 三性论证）。
- 应用层资源数量类特征与网络条件解耦（不依赖加载时间/丢包），因而跨网络稳定；与资源"大小"解耦（不依赖内容更新），因而抗概念漂移（§4.4）。
- 惰性学习（距离度量）使攻击可在极少数样本（N=1）下启动，且无需预训练模型。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | HTTPS 时代网站普遍同时使用 HTTP/1.1、2、3，版本组合模式各异；前 10 万网站中近 80% 存在版本并行 | 附录 B 测量（Figure 9） |
| 痛点提炼 | 传输层特征在真实 HTTPS 网络条件下精度大降（-20%），且数据采集成本高（>10 天） | §1、§4.4 |
| 问题转化 | 能否把特征提取层上移到"加密仍掩盖不了"的应用层元数据（HTTP 版本 + 资源数量）？ | §3.1 协议分析 |
| 文献定位 | 早期 WF（Hintz 等）用过资源数量/大小，但被传输层方法取代；协议语义推断类工作（[3, 25, 42, 55, 83, 87]）未聚焦版本并行性的隐私含义 | 附录 A |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | HTTP 版本并行性驱动的应用层特征（版本+资源数量）信息量高且跨网络稳定 | 信息量测量（4.28 bit，超 98% 特征）+ 变异系数稳定性测量（Figure 2） | 实验（§4.2-4.4） |
| 辅助假设 1 | 惰性学习 + 指纹专用距离度量可在 N=1 下有效攻击 | 距离度量直接比较无需训练 | 少样本实验（Table 2） |
| 辅助假设 2 | 资源数量/版本特征不受网站内容更新影响，抗概念漂移 | H123 不含资源大小信息 | 时间漂移实验（Figure 6） |
| 辅助假设 3 | 应用层资源特征与网络条件解耦，跨网络鲁棒 | 特征不依赖加载时间 | 跨网络实验（Figure 5） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | HTTP/2 资源数量泄露 4.28 bit；N=1 平均 87.7% vs 最优对比 IP-WF 70.5% | Figure 2, Table 2 |
| 辅助假设 1 | 支撑 | N=1 时 87.7%，N=30 时 98.6%（接近 k-FP+ 99.3%） | Table 2 |
| 辅助假设 2 | 支撑 | 30 天漂移后 H&W 88% vs k-FP+ 72%（N=10） | Figure 6(b) |
| 辅助假设 3 | 支撑 | 跨网络（unconstrained→slow 等）H&W 表现优于现有方法 | Figure 5 |

---

## 4. 方法设计

### 4.1 方法整体流程

两个组件：

1. **HOLMES（特征提取）**：在五元组划分的流量流（flow）粒度上，通过协议分析（状态机）免解密推断每条连接的 HTTP 版本与资源数量，生成 H123 指纹（3×L 矩阵：行 = HTTP/1.1/2/3，列 = 连接序列，值为该连接内对应版本的资源数量）。
2. **WATSON（分类）**：惰性学习（lazy learning）：closed-world 用最近邻（NN）；open-world 用 KNN + Gini 系数阈值判断是否属于监控集；距离 = 0.5×Wasserstein + 0.5×LCSS；预测时先用资源总数带通滤波（±20%）预筛参考样本。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 流划分 | 原始 pcap | 按五元组 <源 IP、源端口、目的 IP、目的端口、协议> 划分流量流 | 每条连接的包序列 | 平衡包级效率与会话级信息量（§3） |
| Step 2 HTTP 阶段定位 | 流内包序列 | HTTP 阶段起点 = 首个出方向 TLS "application data" 包（HTTP/3 为首个短头 QUIC 包） | 定位后的包序列 | 避开握手阶段混淆（§3.1） |
| Step 3 版本推断 | HTTP 阶段前两个包 | HTTP/3：是否用 QUIC（UDP）；HTTP/1：前两包为"出+入"（顺序请求/响应）；HTTP/2：前两包均为"出"（preface 包） | 每条连接的 HTTP 版本（1/2/3） | 版本是 H123 指纹的行索引（§3.1.1） |
| Step 4 资源数量推断 | HTTP 阶段出方向包 | 协议状态机统计"出方向请求"数量；过滤控制包（HTTP/2 <40 字节、HTTP/3 <120 字节；初始 setting 包不计） | 每条连接的资源数量 R_i | 资源数量是 H123 指纹的值（§3.1.2） |
| Step 5 构建 H123 | 版本 + 资源数量序列 | F ∈ R^(3×L)：F[v,i] = R_i（若连接 i 用版本 v），否则 0；L=50 | H123 指纹 | 网站判别性表示 |
| Step 6 参考集预筛 | 查询指纹 + 参考集 | 仅保留资源总量在查询样本 ±20% 内的参考样本 | 缩小候选集 | 减少约 85% 距离计算（§3.2.1） |
| Step 7 距离度量 | 查询指纹 + 候选 | Wasserstein 距离（对每个 HTTP 版本行排序后算 CDF 距离，三行平均归一化）+ LCSS 距离（相似阈值 ε=0.24）按 0.5/0.5 加权 | 混合距离 | 处理排列/聚合/错位三类类内变异（§3.2.2） |
| Step 8 分类决策 | 混合距离 | closed-world：NN；open-world：KNN（取 2N 最近）+ Gini 系数阈值判定监控集归属 | 网站类别 / 监控集判定 | 攻击输出 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| HOLMES 协议状态机 | 免解密推断资源数量 | 出方向包事件（get_pkt/get_s_pkt/get_l_pkt/EOF） | 资源计数（Counter） | 状态：Idle/Request/Standby/Preface/Settings/End（附录 C, Figure 10） |
| H123 指纹 | 网站判别表示 | 每条连接的 (HTTP 版本, 资源数量) | 3×L 矩阵（L=50） | 是 WATSON 的全部输入 |
| 带通预筛 | 加速惰性学习 | 查询指纹 + 参考集 | 候选子集 | 资源总量 ±20%，比较量减少约 85% |
| Wasserstein 距离 | 分布级差异度量 | 两个 H123 指纹 | 归一化距离 | 按行排序后取 CDF 差（附录 E, Algorithm 1） |
| LCSS 距离 | 子序列局部相似度 | 两个 H123 指纹（无版本标注的资源序列） | 归一化距离 | 相似阈值 ε=0.24（附录 E, Algorithm 2） |
| NN / KNN+Gini | 分类决策 | 加权混合距离 | 类别 / 是否监控集 | closed-world 用 NN；open-world 用 2N 邻居距离的 Gini 系数阈值 |

### 4.4 公式、算法和机制解释

- **H123 指纹**（式 1）：F[v,i] = R_i（若 HTTP_i = v），否则 0；v ∈ {1,2,3}。矩阵 F ∈ R^(3×x)，x 为连接数（截断至 L=50）。
- **Wasserstein 距离**（式 2）：W(P,Q) = inf_{γ∈Γ(P,Q)} ∫|x−y|dγ(x,y)。实现：对每一行（版本）数值排序后计算累积分布函数（CDF）距离之和并归一化（1D 离散情形等价于 CDF 距离，引用 [59]）。
- **LCSS 距离**：相似阈值 ε·max(a,b) 内视为匹配（|F1[i−1]−F2[j−1]| ≤ ε·max(...)），返回 1 − (LCSS 匹配数之和 / sum(F1))。
- **Open-world 判定（Gini 系数）**：取 2N 个最近参考样本（N=每类参考样本数）。若查询样本属于已知类，期望 N 个同类别样本距离远小、N 个异类样本距离大 → 距离分布不均 → Gini 系数低；反之未知类距离均匀 → Gini 高。设定阈值区分（§3.2.3）。
- **超参数**：最大指纹长度 L=50、LCSS 阈值 ε=0.24、两距离权重各 0.5（附录 G 用补充数据独立调优，避免测试集泄漏，§4.2.1）。

### 4.5 方法优势

1. **免训练**：惰性学习无需参数化模型训练，训练时间开销为 0（Table 2 Time Overhead 列 H&W 为 "-"），可灵活增删监控网站（§4.3 Experiment 3）。
2. **极致少样本**：N=1（每站访问 1 次，bootstrap 20 小时）即达平均 87.7%（§4.3）。
3. **跨网络鲁棒**：应用层资源特征与网络条件解耦，跨网络矩阵中对角线与非对角线均优于现有方法（§4.4）。
4. **抗概念漂移**：H123 用版本与资源数量而非资源大小，内容更新（如广告更换）影响小（§4.4）。
5. **效率**：带通预筛减少约 85% 比较；预测吞吐 ≥2000 网站/秒（§4.3 Experiment 3）。

### 4.6 方法不足

1. **跨浏览器失效**：Chrome↔Firefox 交叉测试精度跌至 ~5%（N=1）/6.8%（N=10）——不同浏览器对资源处理差异导致 H123 序列差异（附录 H，Table 7）。
2. **跨版本下降**：同浏览器跨版本测试精度下降约 20%（Chrome 88.4%→62.2%，N=1）（Table 7）。
3. **依赖资源稳定性**：网站资源重大变化需周期性更新数据（§5 Limitations）。
4. **填充防御未知时失效**：攻击者不知防御时（无先验知识），所有方法（含 H&W）均跌至 ~6%（Table 8）。
5. **open-world 精度随负样本量下降**：8 万未监控网站时 N=10 的 precision 70.2%、recall 81.0%（§4.5 Experiment 2）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 对比维度 | 传输层方法（DF/TF/RF/k-FP） | IP-WF | H&W（本文） |
|---|---|---|---|
| 特征层 | 传输层（包方向/时序/长度） | IP 地址 + 熵匹配 | 应用层（HTTP 版本 × 资源数量） |
| 学习范式 | 急切学习（深度/统计模型训练） | 指纹库匹配 | 惰性学习（距离度量） |
| 数据需求 | 大（N≥10 起步，通常更多） | 中 | 极小（N=1 可用） |
| 网络鲁棒性 | 差（时序类特征强相关加载时间） | 最稳定但精度平庸 | 好（资源数量与网络解耦） |
| 抗概念漂移 | 差 | 中 | 好（不含资源大小） |

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 首次识别 HTTP 版本并行性的隐私风险 | 测量前 10 万网站：80%+ 并行、近半数三版本共存；单特征 4.28 bit 信息量 | 高 | 是（TLS 1.2/1.3、IPv4/IPv6 并行亦可类比，§5） |
| H123 指纹 + 协议状态机 | 免解密推断每连接的版本与资源数量，3×L 矩阵编码 | 高 | 是（任意加密 Web 流量） |
| 指纹专用混合距离 | Wasserstein（抗排列/聚合）+ LCSS（抗错位）互补，加权 0.5/0.5 | 中 | 是（序列型指纹通用） |
| Gini 系数开放世界判定 | 用 2N 邻居距离分布的不均匀度判断监控集归属 | 中 | 是 |
| 1.5TB 真实 HTTPS 数据集 | 首个含困难网络条件/多浏览器/现实监控集的 HTTPS WF 数据集（12 场景） | 高 | 是（社区资产） |

### 5.3 适用场景

- 网络审查者（censor）对 HTTPS 网站进行大规模监控（open-world 场景直接用 CW-censorship 集模拟，§4.5）。
- 少量样本即可启动攻击的快速部署场景（N=1，bootstrap 仅 20 小时）。
- 需要频繁更新监控网站列表的动态场景（惰性学习即插即用）。
- 注意：仅适用于**单浏览器环境**或已知浏览器场景；跨浏览器/跨版本场景目前不可用。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| k-FP（150 特征 + 随机森林） | 精度高（大数据下 95.9%+） | 特征与加载时间强相关、跨网络最差、需训练 | 用应用层资源特征替代时序统计特征 |
| DF（CNN） | 无防御下精度高 | N=1 时仅 16.7%~38.6%、训练 254s、需大数据 | 惰性学习免训练、N=1 可用 |
| TF（三元组指纹） | 少样本较好（N=1 57.3%） | 预训练成本 205.9s、跨网络一般 | 免训练 + 跨网络更好 |
| IP-WF | 跨网络最稳定、open-world 二分类强 | 精度平庸（N=1 70.5%）、依赖 IP 解析、censorship 集优势靠 IP 独特性 | 精度更高（N=1 87.7%）且不依赖 IP |
| H&W | 免训练、N=1 高效、跨网络/漂移鲁棒、≥2000 网站/秒 | 跨浏览器失效、依赖资源稳定性、无先验防御时失效 | — |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- 数据集构建：Selenium v4.15.2 + Chrome v126（浏览器数据集另含 Firefox v129、Chrome-legacy v104），tcpdump 抓包，10 台 AWS 北美服务器，2024-07~09；开放世界每站 1 次，其余场景每站 50 次取 40 个有效样本；轮询访问方式（round-robin）；排除加载失败/CAPTCHA/无意义内容/<50 包网站。
- 对比方法用作者发布代码实现并针对少样本微调（超参搜索 + early stopping）；k-FP+（启用包长）、DF+（包长映射进序列）、IP-WF（理想版用浏览器日志 IP 估计上限）。
- k 折交叉验证消除随机误差。
- 硬件：Ubuntu 23.10，NVIDIA A100 80GB，Intel Xeon 2.9GHz，128GB RAM。

### 6.2 数据集

| 场景 | 内容 | 规模 |
|---|---|---|
| CW-popular | Tranco 前 1600 网站 | 64,000 样本（40/站） |
| CW-random | Tranco 前 1 万中随机 320 站 | 12,800 |
| CW-censorship | Citizenlab 列表 320 站 | 12,800 |
| Bandwidth ×3 | unconstrained / starlink-like / slow（Chrome 节流模拟） | 各 8,000 |
| Browser ×3 | chrome / chrome-legacy / firefox | 各 8,000 |
| Time-Drift ×2 | 18 天 / 30 天间隔重采 | 各 8,000 |
| OW | Tranco 前 8 万未采集网站 | 80,000（各 1 次） |

网络条件参数：unconstrained（>500Mbps/上下行，<10ms 延迟，<1% 丢包）；starlink-like（8/70Mbps，50ms，6%）；slow（300kbps/800kbps，350ms，3%）。

### 6.3 Baseline

- k-FP、DF、TF（Triplet Fingerprinting）、RF（Robust Traffic Representation, USENIX Sec'23）、IP-WF，及增强版 k-FP+、DF+、IP-WF(ideal)。

### 6.4 评价指标

- Closed-world：Accuracy。
- Open-world：二分类视角（监控 vs 未监控）的 Precision、Recall、F1（binary F1 区分能力、micro F1 具体网站识别），论文称比 TPR/FPR 更抗类别不平衡。

### 6.5 关键实验结果

**Closed-world 少样本（Table 2 关键格）**：

| 方法 | N=1 pop./rand./cens. | N=30 pop./rand./cens. | 训练时间 | 预测吞吐 |
|---|---:|---:|---:|---:|
| k-FP | 40.1/50.3/58.3 | 90.6/94.9/95.9 | 10.9s | >5k/秒 |
| DF | 16.7/38.6/29.0 | 98.0/99.0/98.6 | 254.4s | 3,765/秒 |
| k-FP+ | 64.1/69.4/76.5 | 99.1/99.5/99.4 | 16.3s | >5k/秒 |
| IP-WF | 65.2/64.9/81.4 | 73.4/74.9/90.2 | 50.1s | 4,023/秒 |
| IP-WF (ideal) | 79.5/79.3/85.2 | 93.9/96.2/95.0 | 50.1s | 3,819/秒 |
| **WATSON** | **85.3/90.4/87.3** | 98.7/99.5/97.6 | 0（免训练） | 2,068/秒 |

- N=1 平均 87.7%（三组监控集平均）vs 最优现有方法 IP-WF 70.5%，提升 >15%。
- N=30 时 k-FP+ 最高 99.3%，H&W 仍达 98.6%（论文称其非为此设计）。
- 距离度量消融（N=1 popular）：Cosine 42.4%、Edit 73.9%、Wasserstein 80.1%、LCSS 78.8%、WATSON（组合）85.3%——组合带来约 +3%。

**跨网络（Figure 5，N=10）**：H&W 对角线与非对角线均优于现有方法；k-FP+ 与 RF 因特征与加载时间强相关而下降最严重；带宽变化（unconstrained↔slow）比丢包变化（unconstrained↔starlink）影响更大；IP-WF 最稳定但精度平庸。

**概念漂移（Figure 6(b)）**：30 天后（N=10）k-FP+ 从 98% 降至 72%，H&W 保持 88%；N=1 + 30 天时 H&W 仍约 80%。增加训练样本（N=1→10）不能缓解漂移。

**Open-world（Table 3）**：

| 方法 | N=1 binary/micro | N=10 binary/micro |
|---|---:|---:|
| k-FP+ | 79.3/77.9 | 92.8/95.8 |
| DF+ | 46.0/43.1 | 93.9/95.1 |
| IP-WF | 88.1/84.7 | 91.2/90.1 |
| **H&W** | **84.7/85.9** | 92.1/94.2 |

- 8 万未监控网站规模（N=10）：precision 70.2%、recall 81.0%；未监控样本增多主要损害 precision（更多负样本被误判为正），recall 不变。

**案例研究（Table 4/7/8）**：
- 资源数量/连接数量处于 (Q2,Q3] 区间的网站更易受攻击；HTTP 版本多样性（版本序列 Shannon 熵）越高越易受攻击（版本多样性 N=10 时 96.2%→99.2% 随四分位上升）。
- 浏览器：Chrome 88.4%（N=1）、98.6%（N=10）；Firefox 83.6%/98.0%；跨版本下降约 20%；跨浏览器几乎失效（4.9%~6.8%）。
- 填充防御（每包填充到最大长度）：攻击者已知防御时 H&W 95.5%（N=10，较无防御仅降约 3%）；攻击者不知防御时全部方法失效（H&W 6.9%）。

### 6.6 优势最明显的场景

- **每网站单样本（N=1）**：87.7% 平均精度，bootstrap 仅 20 小时，比第二名 IP-WF(ideal) 高约 8 个百分点。
- **概念漂移 30 天**：88% vs k-FP+ 72%（N=10），优势 16 个百分点。
- **跨网络条件**：所有交叉组合下优于现有方法。
- **开放世界少样本**：N=1 micro F1 85.9%，高于 k-FP+（77.9%）与 DF+（43.1%）。

### 6.7 局限性

1. 跨浏览器/跨版本不鲁棒（跨浏览器 ~5-7%，跨版本降 20%）——协议处理差异导致资源序列不同（附录 H）。
2. 依赖网站资源稳定性，重大内容变化需更新数据与参考集（§5）。
3. 对填充类防御仅在"攻击者已知防御"时鲁棒；未知防御时失效（Table 8）。
4. 仅验证主流浏览器（Chrome/Firefox/Edge 因同内核被排除）（§4.2.1、附录 H）。
5. 仅攻击主页（homepage），多页/子页场景未覆盖（§2.2，引用 Mitseva 等的框架为未来方向）。
6. 实验限于 2024-07~09 时段采集的数据，其结果具有时点性。

---

## 7. 学习与应用

### 7.1 是否开源？

是。代码仓库：https://github.com/2654400439/H123-Website-Fingerprinting（论文引用 [14]）；数据集公开（>1.5TB，论文脚注 1）。

### 7.2 复现关键步骤

1. 采集：Selenium + Chrome v126 + tcpdump，10 台 AWS 服务器轮询访问；每站 40 有效样本。
2. 划分流：五元组。
3. HOLMES：定位 HTTP 阶段起点（首个出方向 TLS application data / 短头 QUIC 包）→ 前两包方向判版本 → 协议状态机计资源数（过滤 <40B（HTTP/2）/ <120B（HTTP/3）控制包）。
4. 构建 3×L H123 指纹（L=50）。
5. WATSON：±20% 带通预筛 → Wasserstein（按行排序 CDF 距离）与 LCSS（ε=0.24）各 0.5 加权 → NN（closed-world）/ KNN+Gini（open-world）。

### 7.3 关键超参数、预处理和训练细节

| 参数 | 值 | 说明 |
|---|---|---|
| 指纹最大长度 L | 50 | 截断过长指纹（附录 G, Fig 13a） |
| LCSS 相似阈值 ε | 0.24 | 容忍资源数量波动（Fig 13b） |
| 距离权重 w | 0.5（Wasserstein）/ 0.5（LCSS） | 互补组合（Fig 13c） |
| 带通预筛范围 | ±20% 资源总量 | 比较量减少约 85% |
| open-world 邻居数 | 2N（N=每类参考数） | 配 Gini 系数阈值 |
| 超参调优数据 | 半年前采集的 400 站 ×40 样本补充数据 | 独立于测试集，避免泄漏 |

### 7.4 能否迁移到其他任务？

- **协议层类比**：TLS 1.2/1.3 并存、IPv4/IPv6 并存等"版本/协议并行性"可产生同类侧信道（§5 作者展望）。
- **代理流量指纹**：QUIC/HTTP/3 流量分类可直接复用 HOLMES 状态机思路。
- **跨任务限制**：依赖浏览器 API 处理资源的方式，跨浏览器场景需先做浏览器识别（作者建议 JA4，附录 H）或混合多浏览器训练样本。

### 7.5 对我的研究有什么启发？

1. **特征层的选择决定鲁棒性上限**：传输层特征天然受网络条件与概念漂移影响；"加密掩盖不了的应用层元数据"是更稳的信号——与流量表示学习文献的"高层语义特征"思路呼应。
2. **测量先行**：论文先用前 10 万网站测量（80% 并行、4.28 bit）再设计方法，"现象测量 → 信息量论证 → 方法落地"的顺序很有说服力。
3. **惰性学习的攻击价值**：距离度量 + 免训练在少样本/快速部署场景碾压深度模型，深度方法不是唯一答案。
4. **数据集是重大贡献**：12 场景 1.5TB 真实 HTTPS 数据集本身就是社区资产，可作为基准（对比 WFCAT 等自建 Tor 数据集的评估可复现性问题）。
5. 注意其跨浏览器脆弱性：若研究防御方视角，"浏览器差异导致的指纹不稳定"本身可能是设计跨浏览器防御的切入点。

---

## 8. 总结

### 8.1 核心思想

> 应用层 HTTP 版本并行性特征 + 惰性学习，少样本鲁棒 HTTPS 指纹。

### 8.2 速记版 Pipeline

1. 五元组分流，定位 HTTP 阶段（首个出方向 application data/QUIC 包）
2. 状态机推断每连接 HTTP 版本与资源数量
3. 构造 3×L H123 指纹（L=50）
4. ±20% 带通预筛 + Wasserstein/LCSS 混合距离
5. NN（closed）/ KNN+Gini（open）分类，N=1 达 87.7%

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]] - 网站指纹识别（HTTPS 场景）
- [[encrypted-traffic-analysis]] - 加密流量分析
- [[traffic-representation-learning]] - 流量表示学习（H123 指纹属于应用层表示）
- [[traffic-classification]] - 流量分类（协议语义推断角度）

### 9.2 相关方法

- 本文方法为惰性学习（lazy learning）+ 距离度量，可用页面中无直接对应方法页面（相关但非页面主题：无）。

### 9.3 相关任务

- [[website-fingerprinting]] - WF 攻击（closed-world / open-world）
- [[traffic-classification]] - 加密流量分类任务

### 9.4 可更新的综述页面

- [[survey-website-fingerprinting]] - 网站指纹综述（可补充应用层特征 + HTTPS 真实场景评估）
- [[survey-encrypted-traffic-analysis]] - 加密流量分析综述

### 9.5 可加入的对比表

- [[method-comparison-table]] - WF 攻击方法对比（传输层 vs 应用层）
- [[dataset-comparison-table]] - 本文 1.5TB 12 场景 HTTPS 数据集可入数据集对比表
- [[open-source-registry]] - 代码与数据集均公开

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| HTTP/2 资源数量泄露 4.28 bit，超 98% 已知特征（3043 维特征集对照，300 监控网站） | Figure 2(b) | §1 |
| 前 10 万网站近 80% 存在 HTTP 版本并行，近半数三版本共存 | Figure 9 / 附录 B | §2.1 |
| N=1 平均 87.7%（三监控集），最优现有 IP-WF 70.5% | Table 2 | §4.3 |
| N=30 时 H&W 98.6% vs k-FP+ 99.3% | Table 2 | §4.3 |
| 网络条件变化导致约 20% 精度下降（现有方法） | §4.4（复现） | §1 / §4.4 |
| 30 天概念漂移：H&W 88% vs k-FP+ 72%（N=10） | Figure 6(b) | §4.4 |
| 距离度量消融：Cosine 42.4 / Edit 73.9 / Wasserstein 80.1 / LCSS 78.8 / WATSON 85.3 | Table 2 | §4.3 Experiment 4 |
| 带通预筛减少约 85% 比较 | §3.2.1 | §3.2.1 |
| 开放世界 N=10：binary F1 92.1、micro F1 94.2；8 万未监控时 precision 70.2% / recall 81.0% | Table 3, Figure 7(a) | §4.5 |
| 跨浏览器失效（4.9%~6.8%）；跨版本降约 20% | Table 7 | 附录 H |
| 填充防御已知时 95.5%（N=10），未知时 6.9% | Table 8 | 附录 H.2 |
| 预测吞吐 ≥2000 网站/秒；H&W 训练开销为 0 | Table 2 Time Overhead | §4.3 Experiment 3 |

---

## 11. 原始资料链接

- PDF：00-inbox/Aug_inbox/2025-WWW-HOLMES&WATSON__A_Robust_and_Lightweight_HTTPS_Website_Fingerprinting_through_HTTP_Version_Parallelism.pdf
- MinerU Markdown：02-parsed-markdown/2025-WWW-HOLMES&WATSON__A_Robust_and_Lightweight_HTTPS_Website_Fingerprinting_through_HTTP_Version_Parallelism.md
- DOI：10.1145/3696410.3714578
- 代码：https://github.com/2654400439/H123-Website-Fingerprinting
- 资助：中科院信工所 Scaling Program（E3Z0191101、E3Z0041101）

**解析质量问题（有，轻微）**：
1. Table 2 为 15 列宽表，解析后在单行内压缩，列头（N=1~30 的 pop./rand./cens. 分块）与数据行对齐可读，但 Bootstrap Time 脚注与 Time Overhead 列需对照原文理解。
2. 附录 D 的 H123 指纹示例以代码块呈现，部分行被省略号截断（如第 10 个示例的 h3 行），不影响正文信息。
3. 公式 (1)(2) 与算法伪代码解析正常；个别引用编号（如 [14] 为代码仓库）正常。

---

## 12. 后续问题

- 跨浏览器失效的根本原因（资源处理差异）能否被建模修正？JA4 浏览器识别 + H&W 的组合效果未实验。
- 版本并行性随时间推移（HTTP/3 普及）会增强攻击面（作者预测）——防御方应如何应对"应用层资源数量"这一侧信道？
- 填充防御"未知防御"时所有方法失效——这是否意味着攻击者对防御的先验知识仍是决定性因素？
- H123 指纹对多标签浏览、子页面浏览的扩展（论文仅主页）。
- 状态机资源推断在边缘场景（POST 拆包、极端控制帧序列）的准确率未单独量化。

---

## 13. 写作叙事与故事线分析

> 仅对 CCF A/B 级或用户指定深度分析的论文填写本节。

### 13.1 论文主线故事线

论文从"HTTPS 已普及、但现有 WF 攻击在真实 HTTPS 场景下不可用"这一矛盾出发：传输层特征在多变网络与概念漂移下大幅失效，且训练成本高昂。转折发生在作者把目光从传输层上移到应用层——发现并测量了"HTTP 版本并行性"这一被忽视的普遍现象（80% 网站、4.28 bit 信息量、跨网络稳定），由此提出 HOLMES 免解密提取 H123 指纹，配套 WATSON 惰性学习分类器把数据需求压缩到每站 1 个样本。实验用 12 场景 1.5TB 自建数据集证明其在少样本、跨网络、概念漂移三方面全面胜出，并坦诚跨浏览器失效等局限。主线是"旧范式（传输层+大模型）在真实场景崩塌 → 新信号源（应用层版本并行性）被发现与量化 → 轻量级新范式全面验证"。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 立题 + 量化卖点 | "4.28 bit 超 98% 特征 + N=1 87.7% +15%"三个数字一次给足 | 应用层特征替代传输层 |
| Introduction | 双线铺垫 | 先批现有假设不现实（-20%、10 天采集），再引出版本并行性测量 | 图 2 三连图（现象/信息量/稳定性）完成说服 |
| Background & Motivation | 理论立基 | "不可避免、普遍存在、有区分度"三性论证版本并行性 | 80% 并行测量数据 |
| Method | 双组件展开 | HOLMES（协议分析+状态机）与 WATSON（惰性学习+双距离）各自独立成节 | 距离度量针对三类类内变异的设计动机 |
| Experiments | 分层证明 | 少样本→跨网络→漂移→开放世界→案例研究，每节一个结论 | 案例研究把威胁推向"版本多样性越高越危险" |
| Limitations & Discussion | 诚实收束 | 承认跨浏览器失败，但把协议并行性推广到 TLS/IPv4-6 展望 | "威胁随版本并行性增长"的远期断言 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 场景缺失 | HTTPS 真实场景（网络变化/漂移/少样本/现实监控集）缺乏系统评估 | 复现实验（-20%）+ 引用 Juarez 等 | §1, §4.4 |
| 性能瓶颈 | 少样本下深度方法崩溃（DF N=1 仅 16.7%） | 实验数据 | Table 2 |
| 理论缺陷 | 传输层特征远离网站资源真实特征、稀疏碎片化 | 协议栈分层论证（Figure 1 五类方法对比） | §1 |
| 场景缺失（新信号） | HTTP 版本并行性此前仅在 IETF 邮件列表被讨论，未从隐私角度研究 | 测量数据 + 文献定位 | §2.1 |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 主实验（closed-world 少样本矩阵 6 方法 × 5 N 值 × 3 监控集） | 对比碾压 + 少样本叙事：N=1 起跑即领先 | 直接支撑"轻量级"主张 |
| 距离度量消融 | 归因：Cosine/Edit 被双距离碾压，组合 +3% | 证明 WATSON 设计非偶然 |
| 鲁棒性实验（跨网络 + 概念漂移） | 渐进证明：先网络、后时间两个维度 | 支撑"应用层特征解耦"核心直觉 |
| 开放世界实验 | 场景完整性：从理想闭世界走向现实 | 服务"审查者可用"的叙事 |
| 案例研究（网站特征/浏览器/防御） | 深描：谁最脆弱、什么条件下失效 | 诚实边界 + 未来威胁放大 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 从"隐私技术升级（DoH/ECH）削弱旧侧信道，但 WF 仍威胁"的现实矛盾切入 | 先用生态变迁（加密普及）设定语境再立题 |
| Gap 提出方式 | "测量先行"：先给现象图（版本并行）、信息量（4.28 bit）、稳定性（变异系数）三连证据，再提方法 | 用测量数据而非文献引用定义 gap |
| 方法论证逻辑 | 双组件命名化（HOLMES/WATSON）+ 协议分析逐步推导（版本推断→资源推断→指纹→距离） | 可读的组件人格化 + 可复现的状态机细节进附录 |
| 实验组织逻辑 | 按"少样本 → 网络 → 时间 → 开放世界 → 深描"的威胁递增序组织，每节有 Takeaway 式结论 | 每小节收尾给一句结论句 |
| 局限性讨论方式 | 单独设 Limitations 节 + 附录深挖（Table 7/8），把最大软肋（跨浏览器）放附录但正文明说 | 软肋不藏，反而用同条件对比（k-FP+ 同样 6.5%）降低伤害 |
| 最值得借鉴的一句话/一段结构 | "We are the first to identify and analyze the privacy risks posed by application-layer features under the context of modern HTTP version parallelism…"（§1 贡献 1）——贡献句同时给出"首创性 + 现象 + 机制" | 贡献点 = 首创声明 + 新现象 + 实现机制的三合一句式 |

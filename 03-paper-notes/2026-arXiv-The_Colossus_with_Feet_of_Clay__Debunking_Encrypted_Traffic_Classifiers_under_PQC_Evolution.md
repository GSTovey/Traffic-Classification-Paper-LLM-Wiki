---
type: paper
title_original: "The Colossus with Feet of Clay: Debunking Encrypted Traffic Classifiers under PQC Evolution"
title_cn: "泥足巨人：PQC 演进下加密流量分类器的实证祛魅"
authors: [Bingzhen Li, Lingjia Meng, Runhan Song, Chuanzhou Pan, Tongjun Pu, Ziqiang Ma, Yupeng Jiang, Lei Cui, Zhiyu Hao]
year: 2026
venue: "arXiv 2026"
doi: unknown
url: "https://arxiv.org/abs/2608.22683"
pdf: "00-inbox/PDFs/2026-arXiv-The_Colossus_with_Feet_of_Clay__Debunking_Encrypted_Traffic_Classifiers_under_PQC_Evolution.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-The_Colossus_with_Feet_of_Clay__Debunking_Encrypted_Traffic_Classifiers_under_PQC_Evolution.md"
status: processed
reading_level: L2
research_area: [encrypted-traffic-analysis, website-fingerprinting]
task: [website-fingerprinting, traffic-classification]
method: [convolutional-network, transformer, pre-training-finetuning, self-supervised-learning]
dataset: [Non-PQC Website Dataset, PQC Website Dataset, Tranco]
code: "http://anonymous.4open.science/r/PQ-WF-Eval"
relevance: high
created: "2026-09-19"
updated: "2026-09-19"
---

# The Colossus with Feet of Clay: Debunking Encrypted Traffic Classifiers under PQC Evolution

> ⚠️ MinerU 解析问题：解析稿中 ff/fi 连字系统性丢失（trafic→traffic、ofers→offers、efects→effects、diferent→different），正文引用时已还原为正常英文；节标题为 small-caps 字体导致大量下标碎片（如 `I<sub>ntroduction</sub>`），引用时同样已还原。

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | The Colossus with Feet of Clay: Debunking Encrypted Traffic Classifiers under PQC Evolution |
| 中文标题 | 泥足巨人：PQC 演进下加密流量分类器的实证祛魅 |
| 作者 | Bingzhen Li, Lingjia Meng, Runhan Song, Chuanzhou Pan, Tongjun Pu, Ziqiang Ma, Yupeng Jiang, Lei Cui, Zhiyu Hao（Beihang University / Zhongguancun Laboratory / Ningxia University） |
| 年份 | 2026 |
| 会议/期刊 | arXiv 预印本（venue 记为 arXiv 2026） |
| 研究方向 | encrypted-traffic-analysis；website-fingerprinting |
| 任务类型 | 封闭世界 HTTPS 网页指纹（website-fingerprinting）；加密流量分类可靠性评估 |
| 方法关键词 | protocol drift；Hybrid-PQC（X25519MLKEM768）；CUMUL / DF / Tik-Tok / ET-BERT / YaTC 五分类器受控评测；跨域迁移（N-P / P-N）；部署比例梯度 α |
| 数据集 | 自建 Non-PQC Website Dataset 与 PQC Website Dataset（195 个 Tranco 网站配对采集，每站 120 次完整访问）；测量样本来自 2,060 个 Tranco 网站 |
| 是否开源 | 有匿名代码仓库 http://anonymous.4open.science/r/PQ-WF-Eval（解析稿未见正式 GitHub 地址） |
| PDF | 00-inbox/PDFs/2026-arXiv-The_Colossus_with_Feet_of_Clay__Debunking_Encrypted_Traffic_Classifiers_under_PQC_Evolution.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-arXiv-The_Colossus_with_Feet_of_Clay__Debunking_Encrypted_Traffic_Classifiers_under_PQC_Evolution.md |

---

## 1. 一句话总结

> 在受控配对基准上证明：TLS 1.3 混合后量子密钥建立（X25519MLKEM768）不会消除 WF 可学习性，但会系统性摧毁分类器的跨密码域可靠性，匹配域精度无法预测部署可靠性。

---

## 2. 摘要翻译

### 2.1 摘要原文

> Encrypted traffic classifiers often achieve high accuracy under matched training and testing conditions, implicitly assuming that deployment traffic follows the training distribution. TLS migration toward post-quantum cryptography (PQC) challenges this assumption because hybrid key establishment can reshape observable traffic without changing application labels. We frame this change as PQC-induced protocol drift and study its effects through closed-world HTTPS website fingerprinting using the deployed TLS 1.3 Hybrid-PQC group X25519MLKEM768. We build a controlled, PQC-aware benchmark pairing Traditional (Non-PQC) and Hybrid-PQC traffic, then evaluate five representative classifiers and side-channel representations under matched-domain, cross-domain, and deployment-ratio settings. Collectively, the experiments show that PQC evolution does not remove learnable website information. Instead, it changes how that information appears in traffic, causing classifiers and feature combinations that perform well in-domain to lose reliability across cryptographic domains. By exposing the fragility of matched-domain evaluation, we offer strategic guidance, identify cross-domain robustness as a research priority, and recommend protocol-aware practices for dependable real-world encrypted traffic classification. The code is available at http://anonymous.4open.science/r/PQ-WF-Eval.

（说明：原文中 "traffic/offers/effects/different" 等词的 ff/fi 连字在解析稿中丢失，以上为还原后的节选。）

### 2.2 摘要中文翻译

加密流量分类器在训练与测试条件匹配时往往能取得高精度，这隐含地假定部署流量服从训练分布。TLS 向后量子密码（PQC）的迁移挑战了这一假设：混合密钥建立在应用标签不变的前提下也能重塑可观测流量。作者把这种变化定义为「PQC 引发的协议漂移（PQC-induced protocol drift）」，并以封闭世界 HTTPS 网页指纹为场景、采用已实际部署的 TLS 1.3 混合组 X25519MLKEM768 展开研究。论文构建了一个受控的 PQC 感知基准，配对采集传统（Non-PQC）与混合 PQC 流量，随后在匹配域、跨域与部署比例三类设置下评测五种代表性分类器及侧信道表征。实验整体表明：PQC 演进并不会移除可学习的网站信息，而是改变了这些信息在流量中的呈现方式，使得域内表现良好的分类器与特征组合在跨密码域时失去可靠性。通过揭示匹配域评估的脆弱性，作者给出了策略性建议，将跨域鲁棒性确立为研究优先项，并推荐了面向协议演进的评估实践，以支撑真实环境中可靠的加密流量分类。代码见 http://anonymous.4open.science/r/PQ-WF-Eval。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- TLS 1.3 正在向后量子密码迁移：浏览器/TLS 栈已默认启用混合组 X25519MLKEM768（§II-A），其 KeyShare 从 32 B 膨胀到 1216 B（客户端）/1120 B（服务端）（Table II）。密钥建立材料变大后，ClientHello/ServerHello 会跨 TLS record 与 TCP segment 边界切分，改变包长、包数、突发结构和握手时序。
- 这些变化不改变应用标签，却改变了分类器赖以工作的可观测特征——即「协议漂移」。既有漂移研究主要关注时间、观测点、客户端、应用、数据管线等来源（Table I），几乎没有把「协议栈自身的演进」作为独立变量隔离研究（§II-C）。
- 于是需要一套受控基准来回答：PQC 迁移到底有没有削弱加密流量分类？削弱到什么程度？哪类表征最受伤？

### 3.2 现有方法的痛点和不足

| 现有痛点 | 具体表现 | 位置 |
|---|---|---|
| 匹配域评测的隐含假设 | 同类论文普遍在训练/测试同分布的设定下报告高精度，默认部署流量服从训练分布 | §I、§V-A |
| 漂移源未隔离 | 时间/网络/客户端/应用/管线漂移常被混在一起，协议栈演进的独立效应未被量化 | §II-C、Table I |
| 缺乏配对数据 | 真实互联网中 Non-PQC 与 Hybrid-PQC 流量混杂且不可控，无法做干净的因果对比 | §IV-B（作者用浏览器开关构造配对数据） |
| 部署是渐进的 | 现实中 Hybrid-PQC 占比会从 0% 逐步爬升，端点对比（0% vs 100%）无法刻画中间地带 | §IV-C |

### 3.3 论文的研究假设或核心直觉

核心直觉：**PQC 造成的不是「信息消失」，而是「信息搬移」**——网站身份信息仍然存在于流量中（域内训练仍可学到），但它在包长分布、TCP 分段方式、字节对齐中的呈现位置发生了偏移，因此跨域使用旧模型时会失配。作者据此提出三条可检验假设（§III-C）：H1 包长漂移、H2 方向与时序漂移、H3 预训练字节级表征的鲁棒性。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 实测 2,060 个 Tranco 网站发现 50.3% 已协商 Hybrid-PQC TLS 1.3、38.6% 为传统 TLS 1.3；混合组 X25519MLKEM768 的 KeyShare 达 1216/1120 B，远超 X25519 的 32 B | §IV-A、Fig.4、Table II |
| 痛点提炼 | 密钥材料膨胀会经 TLS record 构造与 TCP 分段传播，改变包长序列、方向序列、IAT 与字节级对齐——这些恰是现有分类器的原生输入 | §III-B |
| 问题转化 | 把「PQC 迁移是否让分类器失效」转化为可度量的科学问题：在保持标签空间、访问流程、观测点、客户端、采集管线不变的前提下，仅改变密码配置，测量跨域迁移退化 | §V-A（威胁模型与评测范围）、Table I |
| 文献定位 | 漂移研究中「协议栈演进」这一维度被系统性忽视；既有工作只做端点对比或单一时间点对比，缺少部署比例梯度与特征归因 | §II-C、§IV-C |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 H1：Packet-Length Drift | 依赖包长序列及其派生统计（CUMUL 曲线、矩）的模型，在 Non-PQC 训练、PQC 测试时会显著退化 | §III-B（KEM 载荷膨胀直接改变包长） | RQ2/RQ4 实验（N-P 迁移、五种输入表征消融） |
| 辅助假设 H2：Directional and Temporal Drift | 方向/时序特征（含 IAT）也会因额外分段、ACK、握手时长变化而退化，高时延或资源受限路径更明显 | §III-B（分段与时序传播） | RQ2（DF/Tik-Tok 的 N-P 迁移） |
| 辅助假设 H3：预训练字节级表征更鲁棒 | ET-BERT/YaTC 可捕获可复用的字节级结构，跨域退化应小于纯 L/D/T 模型，但固定输入窗口会限制其优势 | §III-B（字节级对齐偏移） | RQ1–RQ3（ET-BERT/YaTC 的 N-N/N-P/P-N 对比） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| H1 | 部分支撑 | 五种输入表征（D/L/T/DL/DLT）在 N-N→N-P 全部单调退化；但包长 L 在 N-P 下仍是最强单特征（0.4310 vs D 0.3728、T 0.3766），说明「包长信号被侵蚀但未消失」 | §V-F、Fig.6、Fig.7 |
| H2 | 部分支撑 | 方向与 DLT 组合在全部设置下都无增益：DLT 从未超过 DL（N-N 0.7983 vs 0.8026；N-P 0.3899 vs 0.4186）；但 DF/Tik-Tok 的退化幅度小于 CUMUL，时序效应未单独占主导 | §V-F |
| H3 | 部分支撑 | ET-BERT 在 N-P 下保持最高精度 0.6255（仍远低于其 N-N 的 0.9316），符合「部分鲁棒」；YaTC 则 N-N 1.0000 → N-P 0.3582，匹配域表现完全不能预测跨域表现 | §V-D、Table IV、Table V |

---

## 4. 方法设计

### 4.1 方法整体流程

论文本体不是新算法，而是一套「PQC 感知评测方法与基准」，分三个阶段（§IV）：

1. **部署测量**：对 2,060 个 Tranco 网站抓包，用 Algorithm 1 从 ServerHello 的 key_share 组提取密钥建立方式分布（码点 29 = X25519；4588 = X25519MLKEM768）。
2. **配对数据采集**：对支持该混合组的 Top 200 候选网站，用 Firefox 开关 `security.tls.enable_kyber` 分别产生 Hybrid-PQC 与 Non-PQC 流量，每个网站在每种配置下采集 120 次完整页面加载。
3. **评测**：构造六档部署比例测试集（α ∈ {0%, 20%, 40%, 60%, 80%, 100%}），对五种代表性分类器在匹配域（N-N / P-P）、双向跨域（N-P / P-N）、部署比例（N-M2…N-M8）与特征消融（RQ4）四类设置下评测。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 测量 | 2,060 个 Tranco 网站（base 域 + www 变体）的抓包 | Algorithm 1：识别含 ClientHello+ServerHello 的 TLS 会话，比对 SNI，统计 ServerHello key_share 组分布 | 密钥建立方式分布（Fig.4） | 确认 Hybrid-PQC 已是最大类（50.3%），选定 X25519MLKEM768 为研究对象 |
| Step 2 配对采集 | Top 200 支持混合组的网站 | Firefox 切换 `security.tls.enable_kyber`，每站每配置 120 次完整访问 | Non-PQC / PQC 两套配对抓包 | 保持标签、客户端、观测点、缓存状态不变，只变密码配置 |
| Step 3 数据校验与切分 | 配对抓包 | 重新运行 Algorithm 1 验证保留样本的 ServerHello 组（PQC 全为 4588、Non-PQC 全为 29）；按完整访问（visit）而非单条 TCP 流切分 80/10/10 | 195 个共享标签的两套数据集 | 防止同一次访问的流量跨训练/测试泄漏 |
| Step 4 比例测试集 | 两套测试分区 | 按 α 定义混合样本，α ∈ {0%, 20%, 40%, 60%, 80%, 100%}，对全部 195 个标签施加同一 α | 六个部署比例测试集（0% = N-N，100% = N-P） | 隔离「测试域组成变化」这一单一变量 |
| Step 5 分类器评测 | 六档测试集 × 五种分类器 | 每个分类器保留原生预处理；每站 80 训练 / 10 验证 / 10 测试；报告 accuracy / precision / recall / F1 | RQ1–RQ4 结果 | 回答匹配域可学性、双向迁移、比例敏感性、特征贡献 |

> 数据校验细节：共有 4 个候选网站因网络与采集失败无法在两种配置下都取得有效抓包，最终保留 195 个共享标签（§IV-B）。

### 4.3 模型结构或系统模块

论文不新增模型，评测对象是三类表征范式的五个代表（Table III）：

| 模块（分类器） | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| CUMUL | 聚合统计分类器（SVM + 手工艺特征） | 统计特征 + 采样的累计流量曲线 | 195 类标签 | 代表「聚合统计表征」，对流量总量与累计传输轮廓敏感 |
| DF | 1D 卷积网络 | 方向编码的包序列 | 同上 | 代表「包序列表征」，对局部序列模式与位置对齐敏感 |
| Tik-Tok | 含时序的深度序列模型 | 包长 + 方向 + IAT | 同上 | 在 DF 基础上引入时序，检验联合序列/时序变化的影响 |
| ET-BERT | 预训练 Transformer | 匿名化 datagram 字节（前 5 个包，每包 128 B） | 同上 | 代表「预训练字节级表征」；固定输入窗口可能截断扩张后的握手 |
| YaTC | 预训练掩码自编码器（MAE） | 匿名化多层级流表征（前 5 个包，每包 80 B 头 + 240 B 载荷） | 同上 | 同上；字节范围偏移可能改变其窗口内容 |

### 4.4 公式、算法和机制解释

- **表征 4 元组**（Eq.2）：$X = (L, D, T, P)$，其中 $L$ 为包长序列、$D$ 为方向序列、$T$ 为时间戳/到达间隔、$P$ 为泛化字节级表征（可含匿名化网络/传输头、TLS 握手字节、加密应用记录，但不含明文应用内容）。CUMUL/DF/Tik-Tok 主要消费 $(L,D,T)$ 的组合，ET-BERT/YaTC 消费 $P$。
- **混合共享密钥**（Eq.1）：$SS_{\text{hybrid}} = SS_{\text{MLKEM}} \parallel SS_{\text{X25519}}$，拼接后 64 字节交予 TLS 1.3 key schedule。
- **部署比例**（Eq.3）：$\alpha = \frac{N_{\mathrm{Hybrid\text{-}PQC}}}{N_{\mathrm{Non\text{-}PQC}} + N_{\mathrm{Hybrid\text{-}PQC}}}$；对每个网站施加同一 α，避免类别级部署偏斜污染分类器性能。
- **机制链条**：ML-KEM-768 封装密钥（客户端 1184 B）+ X25519（32 B）= 1216 B，服务端密文 1088 B + 32 B = 1120 B → ClientHello/ServerHello 变大 → 超过 TCP MSS 时被拆成多段 → 可观测包数、包长序列、突发边界、握手时长与字节对齐随之改变 → 直接冲击上表五类原生输入。

### 4.5 方法优势

- **因果干净**：通过浏览器开关在「同一网站、同一客户端、同一观测点、同一采集脚本」下配对采集，只让密码配置变化，并把时间漂移用交替采集压制（Table I）。
- **表征覆盖全面**：五个分类器横跨聚合统计、包序列、预训练字节级三类范式与 $(L,D,T,P)$ 四个特征维度，避免单一模型的结论偏差。
- **评测维度成体系**：匹配域（RQ1）、双向迁移（RQ2）、部署比例梯度（RQ3）、特征归因（RQ4），后者用「固定 DF 架构只换输入表征」的方式把差异归因到输入组成而非模型容量。
- **可操作的政策含义**：给出「匹配域精度必须配跨域测试」「数据集应反映当代密码部署」两条评估规范建议（§VII）。

### 4.6 方法不足（作者自述 + 范围限制）

- 仅封闭世界、仅 195 个标签、单一观测点、单一客户端平台；不含 Tor/VPN 隧道、主动攻击与开放世界（§V-A）。
- 只研究 Hybrid-PQC 密钥建立，纯 PQC（MLKEM768）只在协议层做了对比（Table II），未做实证；后量子认证（ML-DSA/Falcon 证书链）可能引入更大且方向不定的漂移，作者将其列为未来工作（§VI-A）。
- 时序漂移的量级是环境依赖的（取决于硬件加速、带宽、路径），不能外推到所有部署（§III-B）。
- 未做对抗自适应实验：攻击者重新采集 Hybrid-PQC 数据并重训后是否完全恢复，论文只给出方向性论断（§VI-C）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

- 与 SoK 式工作（Wickramasinghe et al. 等）的区别：后者揭示输入、清洗与采样粒度对结论的影响；本文把「协议栈演进」单列为独立漂移源，并用配对数据把其他漂移源钉死。
- 与既有漂移工作（跨时间/跨观测点/跨客户端）的区别：本文的漂移由协议机制确定性触发（KEM 载荷膨胀），而非外部环境波动，因此可控、可复现。
- 与「WF 攻击方法」论文的区别：本文不追求更高的攻击精度，而是给现有攻击范式做「可靠性压力测试」，并输出评估方法论。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| protocol drift 概念与分类法 | 把漂移源细分为时间/网络/客户端/应用/管线/协议六类，明确协议漂移的独立性 | 高 | 是（QUIC/HTTP3、ECH、TLS 扩展演进同样适用） |
| PQC 感知配对基准 | 用浏览器开关构造 195 站配对的 Non-PQC / Hybrid-PQC 数据集，visit 级 80/10/10 切分 | 高 | 是（可为任意协议变量做配对评测集） |
| 双向跨域迁移评测 | N-P 与 P-N 同时测，发现方向非对称是核心现象 | 高 | 是（所有跨域/分布漂移研究可复用） |
| 部署比例梯度 | α ∈ {0,20,40,60,80,100}%，覆盖渐进迁移过程 | 中 | 是（适用于任何渐进部署场景） |
| 受控特征归因 | 固定 DF 架构，只切换 D/L/T/DL/DLT 输入 | 中 | 是（特征贡献的标准做法） |

### 5.3 适用场景

- 加密流量分类研究者在报告「高精度」结论前，用同类基准做跨密码域稳健性自查；
- 部署方评估「浏览器默认开启 PQC 后，现有流量分类/安全检测模型是否需要重训」；
- 协议测量研究者量化协议变更（如后量子认证、QUIC 迁移）对流量侧信道的影响。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点（评测视角） |
|---|---|---|---|
| CUMUL（SVM + 统计/累计曲线） | 轻量、可解释、域内精度尚可（N-N 0.7731） | 对总量与累计轮廓强依赖，跨域退化最严重（N-P 仅 0.1919） | 揭示聚合表征在协议漂移下最先失效 |
| DF（1D-CNN） | 端到端学局部序列模式，域内 0.5855 | 位置对齐敏感，N-P 退化到 0.3728 | 作为 RQ4 的受控骨架，用于特征归因 |
| Tik-Tok（长度+方向+IAT） | 显式建模时序 | 加入时序未带来跨域优势（N-P 0.3873） | 证明时序特征不能补偿协议漂移 |
| ET-BERT（预训练 Transformer） | 域内 0.9316，N-P 下最稳（0.6255） | 跨域仍大幅下降；固定前 5 包窗口会截断膨胀后的握手 | 说明预训练只带来「部分」鲁棒性 |
| YaTC（MAE 预训练） | 域内近乎完美（N-N 1.0000） | N-P 崩塌至 0.3582，匹配域表现最不能预测跨域表现 | 揭示「高域内精度 = 高可靠性」的评估陷阱 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

威胁模型为客户端附近的被动观测者，只见单个 HTTPS 站点的加密包迹，不做解密/篡改/注入；封闭世界 195 类；每类 80/10/10（训练/验证/测试）访问级切分；out-of-band DNS 与解密信息（证书、Host 头、URL）对全部分类器禁用（§V-A、§V-B2）。

### 6.2 数据集

| 数据集 | 来源 | 规模 | 说明 |
|---|---|---|---|
| 部署测量样本 | Tranco 排名（base + www 变体） | 2,060 个网站 | 50.3% Hybrid-PQC TLS 1.3、38.6% 传统 TLS 1.3、9.8% TLS 1.2、1.3% 无响应（§IV-A） |
| Non-PQC Website Dataset | Top 200 候选（195 有效）× Firefox 关闭 kyber | 每站 120 次完整访问 | 全部样本 ServerHello 码点 29（X25519）（§IV-B） |
| PQC Website Dataset | 同上 × Firefox 开启 kyber | 每站 120 次完整访问 | 全部样本 ServerHello 码点 4588（X25519MLKEM768）（§IV-B） |
| 部署比例测试集 | 两套测试分区按 α 混合 | α ∈ {0%,20%,40%,60%,80%,100%} | 对全部 195 标签统一 α，防类别级偏斜（§IV-C） |

### 6.3 Baseline

每个分类器主要与**自身的匹配域基线**对照（作者刻意避免跨模型绝对排名，因输入异构：§V-B2）。域内基线：YaTC 1.0000、ET-BERT 0.9316、CUMUL 0.7731、DF 0.5855、Tik-Tok 0.5679（Table IV，N-N）。

### 6.4 评价指标

accuracy、precision、recall、F1 score（每类均值聚合为 macro 形式报告）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法（关键设定） | 最优对比方法 | 提升/落差 | 说明 |
|---|---|---:|---:|---:|---|
| RQ1 匹配域 P-P vs N-N | Accuracy | YaTC 0.9991 (P-P) / 1.0000 (N-N) | ET-BERT 0.9332 / 0.9316 | 五种分类器 N-N 与 P-P 差距均很小 | Hybrid-PQC 域内仍完全可学（Table IV） |
| RQ2 N-P（Non-PQC 训练 → PQC 测试） | Accuracy | ET-BERT 0.6255（最佳） | YaTC 0.3582；CUMUL 0.1919 | ET-BERT 仍比自身 N-N 低 0.3061 | 全部五类跨域退化（Table V） |
| RQ2 P-N（PQC 训练 → Non-PQC 测试） | Accuracy | YaTC 0.9709 | ET-BERT 0.6043；DF 0.4923 | YaTC 逼近其 P-P 基线 0.9991 | 迁移方向非对称，四类 P-N 优于 N-P，ET-BERT 例外 |
| RQ3 部署比例 | Accuracy | ET-BERT 单调 0.9316→0.6255 | YaTC 非单调：1.0000→0.6166(N-M4)→0.7252(N-M8)→0.3582(N-P) | — | 无分类器能在全 α 区间保住 Non-PQC 基线（Fig.5） |
| RQ4 特征归因（固定 DF） | Accuracy | L（仅包长）0.7944→0.4310 | DL 0.8026→0.4186；DLT 0.7983→0.3899；D 0.5855→0.3728；T 0.5560→0.3766 | L 对 D 的优势从 0.2089 收窄到 0.0582 | 包长是最强单特征；方向无增益；加时序无增益（Fig.6/Fig.7） |

### 6.6 优势最明显的场景

本文是「诊断型」论文，最有价值的产出是负面结论的可量化证据：**匹配域精度高 ≠ 部署可靠**。最典型的失配是 YaTC——N-N 1.0000 的完美分类器在 N-P 只剩 0.3582（低于 DF 同设置的 0.3728 之外的四类），说明预训练模型对匹配域的高度拟合可能掩盖协议域迁移风险；相反 ET-BERT 域内精度略低（0.9316）却在 N-P 下最稳（0.6255），是「鲁棒性—精度」权衡的正面案例。

### 6.7 局限性

- 封闭世界 195 类、单观测点、单客户端；不含开放世界与隧道场景（§V-A）。
- 仅覆盖 Hybrid-PQC 密钥建立这一种协议变化；纯 PQC 与后量子认证未实证（§VI-A）。
- 未做「攻击者重采集重训练」的自适应闭环实验，因此「漂移可被重训抹平」只是推断（§VI-C）。
- 时序漂移依赖硬件与网络条件，实验结论的时序部分不能直接外推（§III-B）。

---

## 7. 学习与应用

### 7.1 是否开源？

论文摘要给出匿名代码仓库 http://anonymous.4open.science/r/PQ-WF-Eval（投稿期匿名 artifact）；解析稿未给出正式 GitHub 地址或数据发布方式 → 数据集公开性未提及。

### 7.2 复现关键步骤

1. 用抓包工具对目标网站集合执行密钥建立测量（对应 Algorithm 1），以 ServerHello 的 key_share 组判定密码域，而不是以「浏览器是否开启开关」判定。
2. 用 Firefox 的 `security.tls.enable_kyber` 开关在同一环境交替采集 Hybrid-PQC / Non-PQC 流量，每站每配置 120 次完整访问，按**访问**（而非单条 TCP 流）切分 80/10/10。
3. 按 α 构造六档测试集，先跑 N-N/P-P 匹配域基线，再跑 N-P/P-N 双向迁移，最后做固定架构的特征消融（D/L/T/DL/DLT）。

### 7.3 关键超参数、预处理和训练细节

- 各分类器保留**原生**预处理：ET-BERT 前 5 包 × 128 B；YaTC 前 5 包 ×（80 B 头 + 240 B 载荷）；DF 方向编码；Tik-Tok 长度+方向+IAT；CUMUL 统计特征 + 采样累计曲线（Table III）。
- 切分比例 80/10/10（每站），六档 α 对全部 195 类统一取值（§V-B2、§IV-C）。
- 论文未报告学习率、批大小、训练轮数等训练超参（解析稿未明确）。

### 7.4 能否迁移到其他任务？

高度可迁移的是**方法论**：配对协议域基准 + 双向迁移 + 部署比例梯度 + 固定架构特征归因，可直接搬到 QUIC/HTTP3 迁移、ECH 上线、后量子认证证书链变化等场景；也可迁移到恶意流量检测与隧道识别——任何「标签不变但协议实现改变」的部署都需要同款压力测试。

### 7.5 对我的研究有什么启发？

- 评估协议应把「跨域双向迁移」列为标准报告项，而不是只报同分布精度；跨域设置下要同时报告 N-P 与 P-N，因为方向非对称普遍存在。
- 特征消融要固定模型架构（本文用 DF 作骨架），否则无法区分「表征贡献」与「模型容量贡献」。
- 数据切分粒度（visit 级 vs 流级）是复现性关键，且要在论文中显式声明。
- 「预训练 = 更鲁棒」是可疑的默认假设：本文的 YaTC 反例值得在综述中作为预训练必要性的反证素材（需注明其固定窗口限制）。

---

## 8. 总结

### 8.1 核心思想

> PQC 漂移不消灭信息，只摧毁跨域可靠性。

### 8.2 速记版 Pipeline

1. 抓包测量 2,060 个 Tranco 网站的密钥建立方式，确认 Hybrid-PQC 已成主流（50.3%）。
2. 用浏览器 kyber 开关为 195 个共享标签配对采集 Non-PQC / Hybrid-PQC 流量（各 120 次访问）。
3. 按 α ∈ {0…100%} 构造六档部署比例测试集，统一 80/10/10 访问级切分。
4. 评测 CUMUL / DF / Tik-Tok / ET-BERT / YaTC 五分类器：匹配域（RQ1）、双向跨域（RQ2）、比例梯度（RQ3）、固定 DF 特征消融（RQ4）。
5. 结论：域内可学性保留、跨域普遍退化、迁移方向非对称、包长是最强但不充分的单特征。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[encrypted-traffic-analysis]]
- [[website-fingerprinting]]
- [[traffic-classification]]
- [[traffic-representation-learning]]
- [[2025-S&P-SoK_Decoding_the_Enigma_of_Encrypted_Network_Traffic_Classifiers]]（SoK：本文引用的 [1]，漂移与评测陷阱的直接前作）
- [[2025-SIGCOMM-The_Sweet_Danger_of_Sugar_Debunking_Representation_Learning_for_Encrypted_Traffic_Classification]]（Sweet Danger：本文引用的 [2]，表征学习有效性的争议来源）

### 9.2 相关方法

- [[convolutional-network]]
- [[transformer]]
- [[pre-training-finetuning]]
- [[self-supervised-learning]]
- [[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]]（DF：本文评测的五分类器之一，兼作 RQ4 受控骨架）
- [[2022-WWW-ET-BERT__A_Contextualized_Datagram_Representation_with_Pre-training_Transformers_for_Encrypted_Traffic_Classification]]（ET-BERT：本文评测中 N-P 最稳的模型）
- [[2023-AAAI-Yet_Another_Traffic_Classifier_a_Masked_Autoencoder_Based_Traffic_Transformer_With_Multi-level_Flow_Representation]]（YaTC：本文评测中匹配域最强、跨域崩塌最明显的模型）
- [[2025-S&P-TrafficFormer_An_Efficient_Pre-trained_Model_for_Traffic_Data]]（同类预训练范式，本文引作预训练字节级表征的代表之一 [45]）
- [[2024-ICNP-NetMamba__Efficient_Network_Traffic_Classification_via_Pre-training_Unidirectional_Mamba]]（预训练流量模型邻域工作，本文引用 [44]）

### 9.3 相关任务

- [[website-fingerprinting]]
- [[traffic-classification]]
- [[encrypted-traffic-detection]]

### 9.4 可更新的综述页面

- [[survey-encrypted-traffic-analysis]]
- [[survey-website-fingerprinting]]
- [[survey-traffic-foundation-model]]（预训练模型跨域鲁棒性证据）
- [[contradictions]]（「预训练是否带来跨域鲁棒性」存在正反证据：ET-BERT 部分鲁棒 vs YaTC 崩塌）

### 9.5 可加入的对比表

- [[method-comparison-table]]（五种表征范式在同一受控基准下的跨域表现对比）
- [[dataset-comparison-table]]（Non-PQC / PQC Website Dataset 是新的配对协议域数据集）
- [[open-source-registry]]（匿名 artifact：http://anonymous.4open.science/r/PQ-WF-Eval）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| Hybrid-PQC 已是 Tranco 主流：50.3% 混合 PQC TLS 1.3、38.6% 传统 TLS 1.3、9.8% TLS 1.2、1.3% 无响应 | Fig.4 及正文统计 | §IV-A, Fig.4 |
| 混合组使 KeyShare 从 32 B 膨胀到 1216 B（客户端）/ 1120 B（服务端） | Table II | §III-A, Table II |
| 匹配域下 PQC 不降低可学性（五分类器 N-N 与 P-P 差距很小） | Table IV；如 YaTC 1.0000→0.9991、ET-BERT 0.9316→0.9332 | §V-C, Table IV |
| 跨域普遍退化且方向非对称：YaTC N-P 0.3582 vs P-N 0.9709；ET-BERT 是唯一 N-P 高于 P-N 的例外（0.6255 vs 0.6043） | Table V | §V-D, Table V |
| 部署比例升高整体降低精度且无分类器保住 Non-PQC 基线；YaTC 非单调（N-M4 0.6166 → N-M8 0.7252） | Fig.5 及正文 | §V-E, Fig.5 |
| 包长是最强单特征但优势被漂移侵蚀（对 D 的优势 0.2089 → 0.0582）；DLT 从不优于 DL，方向/时序无补偿作用 | Fig.6/Fig.7 及正文 | §V-F |
| 漂移源于信息「呈现方式」变化而非信息消失；作者据此建议协议配置作为显式评估维度 | 讨论与结论 | §VI-C, §VII |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-arXiv-The_Colossus_with_Feet_of_Clay__Debunking_Encrypted_Traffic_Classifiers_under_PQC_Evolution.pdf
- MinerU Markdown：02-parsed-markdown/2026-arXiv-The_Colossus_with_Feet_of_Clay__Debunking_Encrypted_Traffic_Classifiers_under_PQC_Evolution.md

---

## 12. 后续问题

- 攻击者在 Hybrid-PQC 域重新采集数据并重训后，能否恢复 Non-PQC 基线？论文只给出方向性论断（§VI-C），需要实证。
- 后量子认证（ML-DSA/Falcon 证书链）引入的漂移方向与幅度是否与密钥建立漂移一致？作者列为 §VI-A 未来工作。
- 纯 PQC（MLKEM768，码点仅协议层对比）实证缺失：KeyShare 比混合组小 32 B，但握手流程差异可能带来不同模式。
- 开放世界与隧道（Tor/VPN）场景下的结论是否保持？当前评测范围明确排除。
- 该匿名 artifact 是否已转为正式开源仓库（含数据集）？解析稿未提及，需后续核查。

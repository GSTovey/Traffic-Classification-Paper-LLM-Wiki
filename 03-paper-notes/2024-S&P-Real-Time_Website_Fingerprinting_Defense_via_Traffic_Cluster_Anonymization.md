---
type: paper
title_original: "Real-Time Website Fingerprinting Defense via Traffic Cluster Anonymization"
title_cn: "基于流量聚类匿名化的实时 Website Fingerprinting 防御"
authors: ["Meng Shen", "Kexin Ji", "Jinhe Wu", "Qi Li", "Xiangdong Kong", "Ke Xu", "Liehuang Zhu"]
year: 2024
venue: "IEEE Symposium on Security and Privacy (S&P) 2024"
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2024-S&P-Real-Time_Website_Fingerprinting_Defense_via_Traffic_Cluster_Anonymization.pdf"
mineru_md: "02-parsed-markdown/2024-S&P-Real-Time_Website_Fingerprinting_Defense_via_Traffic_Cluster_Anonymization.md"
status: processed
reading_level: L2
research_area: ["anonymity network", "traffic analysis", "website fingerprinting", "privacy defense"]
task: ["WF defense", "traffic anonymization", "Tor traffic protection"]
method: ["traffic cluster anonymization", "k-anonymity", "Traffic Aggregation Matrix (TAM)", "super-matrix refinement", "trace regularization", "anonymity set generation"]
dataset: ["public WF dataset (95 websites, 1000 traces each)", "Tranco top-100 websites collected in real Tor network"]
code: "https://github.com/kxdkxd/Palette"
relevance: high
created: "2026-05-27"
updated: "2026-05-27"
---

# Real-Time Website Fingerprinting Defense via Traffic Cluster Anonymization

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Real-Time Website Fingerprinting Defense via Traffic Cluster Anonymization |
| 中文标题 | 基于流量聚类匿名化的实时 Website Fingerprinting 防御 |
| 作者 | Meng Shen, Kexin Ji, Jinhe Wu, Qi Li, Xiangdong Kong, Ke Xu, Liehuang Zhu |
| 年份 | 2024 |
| 会议/期刊 | IEEE Symposium on Security and Privacy (S&P) 2024 |
| 研究方向 | 匿名网络、流量分析、website fingerprinting 防御 |
| 任务类型 | 防御 Tor 网络中的 website fingerprinting (WF) 攻击 |
| 方法关键词 | traffic cluster anonymization, k-anonymity, Traffic Aggregation Matrix (TAM), super-matrix, trace regularization, anonymity set |
| 数据集 | 公开 WF 数据集（95 个网站各 1000 条 trace）+ 真实 Tor 网络中采集的 Tranco top-100 网站 |
| 是否开源 | 是（https://github.com/kxdkxd/Palette） |
| PDF | 00-inbox/PDFs/2024-S&P-Real-Time_Website_Fingerprinting_Defense_via_Traffic_Cluster_Anonymization.pdf |
| MinerU Markdown | 02-parsed-markdown/2024-S&P-Real-Time_Website_Fingerprinting_Defense_via_Traffic_Cluster_Anonymization.md |

## 1. 一句话总结

> Palette 通过将流量模式相似的网站聚类为 anonymity set 并将其统一为 super-matrix 规定的流量模式，实现了对 Tor 实时流量的 website fingerprinting 防御，在可接受开销下将 SOTA WF 攻击准确率平均降低 73.60%，优于现有防御方案 33.50%-43.47%。

## 2. 摘要翻译

### 2.1 摘要原文

Website Fingerprinting (WF) attacks significantly threaten user privacy in anonymity networks such as Tor. While numerous defenses have been proposed, they are unable to efficiently defend against recent deep learning based WF attacks. In this paper, we propose Palette, a novel and practical WF defense that utilizes traffic cluster anonymization to protect live Tor traffic. By clustering websites with high similarity in traffic patterns and regulating them into a well-designed uniform pattern for a cluster (i.e., a group of similar websites), Palette prevents attackers from distinguishing between these similar websites within the cluster and further provides a strong anonymity guarantee. Comprehensive evaluations with public real-world datasets show that Palette is superior to the existing defenses, greatly reducing the accuracy of the state-of-the-art (SOTA) WF attacks with acceptable overheads. Furthermore, we implement Palette as a Pluggable Transport in the Tor network. The experiment results demonstrate that, on average, Palette effectively reduces the accuracy of the SOTA WF attacks by 73.60%, which improves the existing defenses by 33.50%-43.47%.

### 2.2 摘要中文翻译

Website Fingerprinting (WF) 攻击严重威胁 Tor 等匿名网络中用户的隐私。虽然已有多种防御方案被提出，但它们无法有效抵御基于深度学习的最新 WF 攻击。本文提出 Palette，一种基于 traffic cluster anonymization 的新型实用 WF 防御方案，用于保护 Tor 实时流量。Palette 将流量模式高度相似的网站聚类，并将其调节为精心设计的统一模式（即一组相似网站的 uniform pattern），从而阻止攻击者在同一聚类内区分不同网站，提供强匿名性保证。基于公开真实数据集的全面评估表明，Palette 优于现有防御方案，在可接受开销下大幅降低 SOTA WF 攻击的准确率。此外，我们将 Palette 实现为 Tor 网络的 Pluggable Transport。实验结果表明，Palette 平均将 SOTA WF 攻击准确率降低 73.60%，比现有防御方案提升 33.50%-43.47%。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

WF 防御领域存在一个根本性的困境：**安全性与实用性之间的矛盾**。现有的防御方案无法同时满足四个关键需求——抵抗 adversarial training、适应实时流量、掩盖 informative features、开销适中（见 Table 1）。具体而言：

**实时防御的紧迫性**：Tor 是全球数百万用户依赖的匿名通信服务，WF 攻击使得本地窃听者（ISP、AS、恶意 guard node）可以通过流量侧信道推断用户访问的网站。深度学习的兴起使 WF 攻击准确率飙升至 98% 以上（DF/Tik-Tok/Var-CNN/RF 在 undefended 流量上均超 94%），急需可实际部署的防御方案。

**现有防御的系统性失败**：
- **Obfuscation 类的致命弱点**：WTF-PAD 和 FRONT 虽然零延迟且开销适中，但由于 Tor 上部署的防御是公开的，攻击者可以用防御后的流量进行 adversarial training。实验表明，WTF-PAD 在 adversarial training 下被 DF/Tik-Tok/Var-CNN/RF 击穿（准确率 90.85%-96.64%），FRONT 也被 RF 以 93.92% 准确率攻破。BLANKET 虽利用对抗扰动，但假设扰动对攻击者未知（agnostic），低估了 Tor 场景中攻击者的能力。
- **高安全性防御的不可行性**：BuFLO 家族（Tamaraw bandwidth overhead 121%, time overhead 43%）和 Supersequence（88% BOH, 91% TOH）能将攻击准确率降至 30% 以下，但过高的开销会影响 Tor 节点的内存稳定性，无法广泛部署。
- **中等开销防御的信息泄露**：RegulaTor 只关注粗粒度的 packet surges 特征，忽略了其他 informative features（如 Pkt. per Second 信息泄露 1.401 bit，甚至高于 undefended 的 1.347 bit），导致 RF 攻击准确率仍达 53.11%。Surakav 使用 GAN 生成模式，但 Interval-II 和 Interval-III 特征泄露也超过 undefended 水平。

**核心挑战**：需要一种新的防御范式，既能从信息论角度全面掩盖 informative features，又能以中等开销适配实时流量。

### 3.2 现有方法的痛点和不足

| 现有方法 | 痛点 | 关键数据 |
|---|---|---|
| Obfuscation 类（WTF-PAD, FRONT, BLANKET） | 无法抵抗 adversarial training，攻击者可用防御后的流量重新训练分类器 | WTF-PAD 被 RF 击穿至 96.64%；FRONT 被 RF 击穿至 93.92% |
| BuFLO 家族（Tamaraw, CS-BuFLO） | 开销极高，影响 Tor 网络性能和节点稳定性 | Tamaraw: 121% BOH + 43% TOH；real-world 中更达 135% BOH + 78% TOH |
| Supersequence, Glove | 可证明安全性但开销过大，无法实际部署 | Supersequence: 88% BOH + 91% TOH |
| Walkie-Talkie | 只考虑 burst 特征，需修改浏览器为半双工模式，且易被 timing 特征攻击 | 对 timing-based 攻击（如 Tik-Tok）防御失效 |
| RegulaTor | 只调节粗粒度 packet surges，泄露 informative features | Pkt. per Second 泄露 1.401 bit（> undefended 1.347 bit）；RF 准确率 53.11% |
| Surakav | GAN 生成模式对最新 RF 攻击效果不佳，Interval-II/III 泄露超 undefended | RF 准确率 79.94%；Interval-II 泄露 0.383 bit（> undefended 0.262 bit） |
| TrafficSliver, HyWF, CoMPS | 拆分流量方案，无法防御观察完整流量的本地攻击者 | 只保护单一路径，本地攻击者可观察完整流量 |

### 3.3 Traffic Cluster Anonymization 的核心直觉

**关键洞察**：之前所有 regularization 类防御要么对所有网站使用同一个固定模式（如 Tamaraw），要么为每个网站随机选择模式（如 Surakav），都没有利用**网站间的相似性**。Palette 的核心创新在于观察到：流量模式相似的网站可以被聚类为一个 anonymity set，并统一调节为一个与这些网站流量分布高度相关的 uniform pattern（super-matrix），从而以较低开销实现 k-anonymity。

**为什么这种策略有效**：
1. **相似性降低对齐开销**：因为 super-matrix 是基于 anonymity set 内网站的流量特征构建的，所以实时流量更容易对齐到 super-matrix，需要的 padding 和 delay 更少
2. **k-anonymity 提供理论保证**：每个 anonymity set 至少包含 k 个网站，攻击者最多只能以 1/k 的概率猜测目标网站（理想情况下攻击准确率接近 1/k）
3. **TAM 表示的全面性**：使用 Traffic Aggregation Matrix（2xN 矩阵）聚合包方向、数量和时间信息，比 burst sequence 和 packet surges 更 informative，能覆盖更多 feature category

**受 k-anonymity 技术启发**：每个 anonymity set 包含至少 k 个网站，攻击者最多只能以 1/k 的概率猜测目标网站。实验中 k=30 时，95 个网站被分为 3 个 anonymity set，每个 set 约 30 个网站。

## 4. 方法设计

### 4.1 方法整体流程

Palette 的防御框架分为三个阶段，对应 Figure 2 的三个模块：

**阶段一：Anonymity Set Generation（离线）**
1. 将流量 trace 转换为 TAM 表示（2xN 矩阵，T=80s, s=80ms, N=1000）
2. 基于 super-matrix 间的欧氏距离，迭代将网站聚类为 anonymity set（每个至少 k 个网站）
3. 为每个 anonymity set 构建初始 super-matrix（取各时间槽的最大值，覆盖所有 trace）

**阶段二：Super-Matrix Refinement（离线）**
1. Super-Matrix Shrinking：通过梯度下降优化参数 w 和 b，缩小各时间槽的数值，降低 bandwidth overhead
2. Super-Matrix Sampling：估计 PMF（时间槽概率分布），按概率采样时间槽直到累积概率达阈值 alpha，进一步降低密度

**阶段三：Trace Regularization（在线）**
1. 根据 refined super-matrix 每个时间槽的值决定发包或缓冲
2. Early Sending：缓冲区拥塞时提前发送，防止 packet delay 过大
3. Tail Padding：检测页面加载完成（缓冲区连续空闲），停止填充 dummy packets

**关键设计哲学**：前两个阶段是离线的（在 Tor directory server 上完成），第三个阶段是在线的（在客户端和 middle node 上实时执行）。这种分离设计使得在线处理开销极低，而离线计算可以充分利用历史流量数据。

### 4.2 详细 Pipeline（表格形式）

| 步骤 | 描述 | 技术细节 | 阶段 |
|---|---|---|---|
| 1. TAM 构建 | 将最大加载时间 T 分为 N 个时间槽，统计每个槽的出/入包数 | T=80s, s=80ms, N=1000；矩阵 M ∈ R^(2xN)，M_ij 表示第 j 个时间槽内方向 i 的包数 | 离线 |
| 2. 网站聚类 | 迭代构建至少包含 k 个高相似网站的 anonymity set | Algorithm 1：先选最远网站初始化新 set，再反复添加最近网站；距离 = super-matrix 间的欧氏距离 | 离线 |
| 3. Super-Matrix 构建 | 对每个 anonymity set，取所有 trace 在各时间槽的最大值 | M^S_ij = max{M_ij | M ∈ S}，确保覆盖所有 trace（cover rate > 95%） | 离线 |
| 4. Super-Matrix Shrinking | 用 sigmoid(w)*M - tau*sigmoid(b) 缩小各时间槽的值 | 梯度下降优化 w 和 b；损失函数 L 的 lambda=0.5 平衡 BOH 和 TOH；tau=10 控制调整范围 | 离线 |
| 5. Super-Matrix Sampling | 估计 PMF，按概率采样时间槽直到累积概率达阈值 alpha | PMF 估计每个时间槽出现包的概率；alpha=0.16；保留采样时间槽的值，其余置零，再均匀扩散到后续空槽 | 离线 |
| 6. 在线 Trace Regularization | 根据 refined super-matrix 每个时间槽的值决定发包或缓冲 | client 和 middle node 分别缓冲出/入包，下一时间槽按 Mr 值发送；real > matrix 时缓冲，real < matrix 时填充 | 在线 |
| 7. Early Sending | 缓冲区包数超过下一 u 个时间槽的 Ms 值之和时，按 Ms 发送 | u 从 [0, U) 均匀采样，U=20；切换到 Ms（比 Mr 有更高 volume）以缓解拥塞 | 在线 |
| 8. Tail Padding | 当前时间槽索引是 B 的倍数且缓冲区为空时，停止填充 | B=45；假设页面加载完成，直到有新 real packets 再恢复；比 Tamaraw 更实用（不需要知道精确加载完成时间） | 在线 |

### 4.2.1 TAM 表示的深层分析

TAM（Traffic Aggregation Matrix）是 Palette 的基础表示，其设计解决了传统表示的两个根本矛盾：

**Packet Sequence 的困境**：BuFLO/Glove/Supersequence 使用 per-packet 表示（为每个包指定精确的时间戳和方向），虽然可以提供可证明安全性，但这种过细粒度的表示与实时流量的动态性（网络抖动、包间依赖）严重不匹配，导致极高的 padding 和 delay 开销。

**高级表示的信息损失**：Walkie-Talkie 使用 burst sequence（连续同方向包的数量），RegulaTor 使用 packet surges（短时间内的大量包），Surakav 也使用 burst sequence。这些表示虽然降低了开销，但不可避免地丢失了信息。论文 Table 13 的信息泄露分析证实了这一点：RegulaTor 的 Pkt. per Second 泄露 1.401 bit（甚至高于 undefended 的 1.347 bit），Surakav 的 Interval-II/III 泄露也超过 undefended 水平。

**TAM 的折中优势**：TAM 将时间分为 80ms 的时间槽，统计每个槽的出/入包数，形成 2x1000 矩阵。这种表示：
- 保留了时间维度信息（比 burst sequence 更 informative）
- 聚合了包级别细节（比 packet sequence 更平滑，更容易与实时流量对齐）
- 95% 的 trace 中超过 700 个 outgoing slots 和 600 个 incoming slots 为空，说明 TAM 是稀疏的，可以通过 sampling 进一步优化

### 4.3 模型结构或系统模块（表格形式）

| 模块 | 功能 | 输入 | 输出 | 运行位置 |
|---|---|---|---|---|
| TAM 特征提取器 | 将流量 trace 转换为 TAM 矩阵 | 原始 trace（时间戳+方向序列） | 2xN TAM 矩阵 | Tor directory server |
| Anonymity Set Generator | 聚类相似网站，构建 anonymity set 和初始 super-matrix | 各网站的 TAM traces | anonymity sets + super-matrices | Tor directory server |
| Super-Matrix Refiner | 通过 shrinking 和 sampling 优化 super-matrix | 初始 super-matrix + 历史 traces | refined super-matrix Mr | Tor directory server |
| PMF Estimator | 估计每个 anonymity set 的时间槽概率分布 | anonymity set 的 traces | PMF p(x) | Tor directory server |
| Trace Regularizer | 在线调节实时流量 | 实时 trace + refined super-matrix | defended trace f' | Client + Middle node |
| Early Sending 模块 | 缓冲区拥塞时提前发送 | 缓冲区状态 + Ms | 发包决策 | Client + Middle node |
| Tail Padding 模块 | 检测页面加载完成，停止填充 | 缓冲区状态 + 参数 B | 是否继续填充 | Client + Middle node |

**系统部署架构**：Palette 的离线模块运行在 Tor directory server 上，训练完成后将 super-matrix、PMF 和 anonymity set mapping 分发给客户端。客户端下载后在本地缓存，每 5 天更新一次。在线模块（Trace Regularization）在客户端和 Tor middle node 之间协同工作：客户端负责 outgoing packets 的调节，middle node 负责 incoming packets 的调节。

### 4.4 公式、算法和机制解释

**Super-Matrix 定义**：

$$\mathbf{M}^{\mathcal{S}}_{ij} = \max\{M_{ij} \mid M \in \mathcal{S}\}$$

取 anonymity set 内所有 trace 在每个时间槽的最大值，确保覆盖所有 trace。这是后续所有操作的基础——只有覆盖了所有 trace，才能保证 anonymity set 内的网站可以被统一调节为相同模式。

**Super-Matrix Shrinking**：

$$\mathbf{M}^s = \max(\sigma(w) \cdot \mathbf{M}, \tau) - \tau\sigma(b)$$

其中 sigma 是 sigmoid 函数（将 w 和 b 限制在 [0,1]），tau=10 控制调整范围。这个公式的直觉是：sigma(w) 对整个 super-matrix 进行粗粒度缩放（乘性调整），sigma(b) 进行细粒度偏移（加性调整），max(., tau) 确保值不低于阈值 tau。通过梯度下降训练 w 和 b。

**Loss Function**：

$$\mathcal{L} = \mathbb{E}_{c \sim \mathcal{A}} \mathbb{E}_{M \sim \mathcal{S}_c} \sum_{i=1}^{2} \sum_{j=1}^{N} \max(\mathbf{M}^s_{ij} \mathbb{I}_{(M_{ij}>0)} - M_{ij}, \tau_{high}) - \lambda \mathbb{E}_{c \sim \mathcal{A}} \mathbb{E}_{M \sim \mathcal{S}_c} \sum_{i=1}^{2} \sum_{j=1}^{N} \min(\mathbf{M}^s_{ij} \mathbb{I}_{(M_{ij}>0)} - M_{ij}, \tau_{low})$$

其中 lambda=0.5 平衡 bandwidth 和 time overhead。损失函数的设计体现了两个目标的权衡：
- 第一项（max 部分）惩罚 shrunk super-matrix 值低于实际 trace 的情况（需要 padding dummy packets -> bandwidth overhead）
- 第二项（min 部分，带负号）奖励 shrunk super-matrix 值接近实际 trace 的情况（减少 delay -> time overhead）
- tau_high 和 tau_low 设定无惩罚的容忍范围，允许少量的 padding/delay 不计入损失

**PMF 估计**：

$$\hat{p}(x)_i = \frac{\sum_{c \sim \mathcal{A}} \sum_{M \sim \mathcal{S}_c} \mathbb{I}_{(M_{ix}>0)}}{\sum_{c \sim \mathcal{A}} \sum_{M \sim \mathcal{S}_c} \sum_{j=1}^{N} \mathbb{I}_{(M_{ij}>0)}}$$

估计每个 anonymity set 中出/入包在各时间槽出现的概率。PMF 呈右偏分布：包更可能在页面加载的前几秒发送，后续时间槽概率很低。这解释了为什么 95% 的 trace 中超过 700 个 outgoing slots 和 600 个 incoming slots 为空。

**Early Sending 判定**：

$$m_{ij} = \begin{cases} \mathbf{M}^s_{ij}, & b_i \geq b_{ij}^{\max} \\ \mathbf{M}^r_{ij}, & b_i < b_{ij}^{\max} \end{cases}$$

其中 $b_{ij}^{\max} = \sum_{k=0}^{u} \mathbf{M}^s_{i(j+k)}$，u 从 [0, U) 均匀采样。Early Sending 的核心思想是：当缓冲区积压的包数超过未来 u 个时间槽的 Ms 容量之和时，切换到 volume 更高的 Ms 进行发送，防止 packet delay 过大。u 的随机采样增加了不确定性，使攻击者更难推断具体的发送模式。

**Cover Rate**：

$$\text{CoverRate}(i) = \frac{1}{|\mathcal{A}|} \sum_{c \sim \mathcal{A}} \frac{\sum_{j=1}^{N} \mathbb{I}_{(\mathbf{M}_{ij} \geq \mathbf{M}^{\mathcal{S}_c}_{ij})}}{|N|}$$

衡量 super-matrix 对 anonymity set 内 trace 的覆盖程度。实验中所有 set 的 incoming 和 outgoing cover rate 均超过 95%（Figure 4(b)），证明 super-matrix 可泛化到未见 trace。

**关键机制解释**：
- **TAM 表示**：相比 packet sequence（过细粒度）和 burst sequence（信息损失大），TAM 在粒度和信息保留之间取得平衡。95% trace 中 700+ outgoing slots 和 600+ incoming slots 为空，说明 TAM 是稀疏的，可通过 sampling 优化
- **网站聚类**：Algorithm 1 保证每个 anonymity set 至少 k 个网站且内部高相似。15/19 个 anonymity set 的 intra-class distance 小于 inter-class distance 的 25th percentile（Figure 4(a)）
- **Shrinking + Sampling**：两步 refinement 策略先缩小数值再降低密度，从 3188% bandwidth overhead（无 refinement）降至 84%。消融实验（Table 14）显示去掉 shrinking 后 BOH 升至 490%，去掉 sampling 后 BOH 升至 770%
- **Early Sending + Tail Padding**：解决实时流量与预定义模式不匹配的问题。去掉 early sending 后 TOH 从 9% 升至 17%，去掉 tail padding 后 BOH 从 84% 升至 282%（Table 14）

### 4.5 方法优势

1. **唯一同时满足四个条件的防御**：在 Table 1 中，Palette 是唯一同时满足抵抗 AdvTrain、适应实时流量、掩盖 informative features、开销适中（BOH<100%, TOH<50%）四个条件的防御方案
2. **开销可控且可调**：bandwidth overhead 84%, time overhead 9%（closed-world simulation），与 RegulaTor（80%, 5%）和 Surakav（80%, 6%）相当，但防御效果显著更好。通过调节 k/alpha/B/U 参数可以灵活平衡开销和防御效果
3. **信息泄露最少**：基于 WeFDE 框架的信息泄露分析表明，Palette 在所有 14 个 feature category 中都将泄露控制在较低水平（Table 13），没有出现 FRONT/RegulaTor/Surakav 那样的特定 feature category 泄露超过 undefended 的情况
4. **实际可部署**：已实现为 Pluggable Transport（开源代码 https://github.com/kxdkxd/Palette），在真实 Tor 网络中验证。训练开销低（generation 约 112s, refinement 约 148s），存储开销小（k=5 时仅 228KB），通信开销极低（1000 万客户端每 5 天更新仅 0.66%）
5. **自适应流量变化**：early sending 和 tail padding 机制使其能适应实时流量的动态性。在网络带宽波动（80-160 Mbps）和不同浏览器（Tor/Chrome）条件下均表现稳健
6. **理论保证**：k-anonymity 提供了可量化的匿名性保证，每个 anonymity set 至少 k 个网站，攻击者最多以 1/k 概率猜测

### 4.6 方法不足

1. **依赖网站列表**：需要预先知道可能访问的网站以构建 anonymity set，Tranco 列表可能不反映真实 Tor 用户的访问偏好。论文承认这是伦理和技术双重挑战
2. **匿名集分配单一**：每个网站只分配到一个 anonymity set，adaptive attacker 可先识别 set 再在 set 内分类。两阶段 adaptive attack 最高准确率 36.92%（RF），虽然仍较低，但比 AdvTrain 的 36.43% 略有提升
3. **参数调优复杂**：k, alpha, B, U, s 等参数需要根据网络条件调优。论文建议调优顺序：先确定 k（匿名度），再调 U 和 B（开销平衡），最后调 s 和 alpha（进一步优化开销）
4. **页面加载时间限制**：TAM 默认 T=80s，超长加载时间的网站可能不完整。但这是 WF 研究的普遍假设
5. **Real-world 开销增加**：real-world 中 time overhead 从仿真 9% 增至 24%，主要因为 incoming/outgoing packets 的依赖关系在仿真中难以完全模拟
6. **长期性能衰减**：5 天后 RF 准确率从 53.28% 降至 48.98%（bandwidth overhead 从 73% 略增至 75%），但更长时间跨度的稳定性需进一步验证

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 对比维度 | Obfuscation 类（WTF-PAD, FRONT） | Regularization 类（RegulaTor, Surakav） | Palette |
|---|---|---|---|
| 防御策略 | 随机化包发送（adversarial perturbation） | 将流量调节为预定义模式（固定或随机） | 将相似网站聚类后调节为统一模式（基于相似性） |
| 抵抗 AdvTrain | 否（攻击者可重新训练） | 否（Surakav, RegulaTor 泄露 features） | 是（RF 准确率仅 36.43%） |
| 适应实时流量 | 是（零延迟） | 是（动态调整） | 是（early sending + tail padding） |
| 掩盖 Informative Features | 否（FRONT 的 Pkt. per Second 泄露 1.197 bit） | 否（RegulaTor 的 Pkt. per Second 泄露 1.401 bit） | 是（所有 category 泄露均低于 1.1 bit） |
| 开销适中 | 是（WTF-PAD 61% BOH, FRONT 80% BOH） | 是（RegulaTor 80% BOH, Surakav 80% BOH） | 是（84% BOH, 9% TOH） |
| Trace 表示 | Packet Sequence | Burst Sequence / Packet Surges | Traffic Aggregation Matrix |

**Palette 的核心创新在于利用网站间相似性（而非固定或随机模式）构建 uniform pattern**。这一设计哲学的根本差异体现在：
- Tamaraw 对所有网站使用同一个固定模式 -> 高 overhead（121% BOH）
- Surakav 从随机类别生成参考模式 -> 容易 mismatch -> 泄露 features（RF 79.94%）
- RegulaTor 只关注 packet surges -> 忽略其他 features -> 泄露（RF 53.11%）
- Palette 利用网站相似性构建 super-matrix -> 与实际流量高度相关 -> 低 overhead + 低信息泄露

### 5.2 与各方法的详细对比

**vs. WTF-PAD/FRONT（Obfuscation 类）**：
- 这些防御的核心假设是：随机化包发送可以隐藏特征。但 Tor 上的防御是公开的，攻击者可以用防御后的流量进行 adversarial training
- WTF-PAD 被 DF/Tik-Tok/Var-CNN/RF 以 90%-96% 准确率击穿；FRONT 被 RF 以 93.92% 准确率击穿
- Palette 通过 k-anonymity 提供理论保证，即使攻击者知道防御细节也无法区分同一 anonymity set 内的网站

**vs. Tamaraw/Supersequence（高安全性 Regularization）**：
- 这些防御可以将攻击准确率降至 10%-30%，但 bandwidth overhead 88%-121%, time overhead 43%-91%
- Palette 在 closed-world 中将 RF 降至 36.43%（vs. Tamaraw 10.23%），但 overhead 仅 84% BOH + 9% TOH（vs. Tamaraw 121% BOH + 43% TOH）
- 在 real-world 中，Tamaraw 的 time overhead 更达 78%，Palette 仅 24%

**vs. RegulaTor**：
- RegulaTor 只关注 packet surges 的粗粒度特征，忽略其他 informative features。Table 13 显示其 Pkt. per Second 泄露 1.401 bit（甚至高于 undefended 的 1.347 bit）
- Palette 使用 TAM 全面覆盖多维信息，所有 feature category 泄露均低于 1.1 bit
- Closed-world: Palette 将 RF 从 53.11% 降至 36.43%（降低 16.68%）
- Real-world: RegulaTor 的 time overhead 高达 112%，Palette 仅 24%

**vs. Surakav**：
- Surakav 使用 GAN 生成随机模式，但生成的模式与实际流量容易 mismatch
- Table 13 显示 Surakav 的 Interval-II/III 泄露超过 undefended 水平
- Closed-world: Palette 将 RF 从 79.94% 降至 36.43%（降低 43.51%）
- Real-world: Palette 将 DF/Tik-Tok/Var-CNN 降至 15% 以下，Surakav 仍在 29%-60%

**vs. Walkie-Talkie**：
- Walkie-Talkie 只考虑 burst 特征，需要修改浏览器为半双工模式，且易被 timing 特征攻击（如 Tik-Tok）
- Palette 使用 TAM 全面覆盖包方向、数量和时间信息，无需修改浏览器

**vs. TrafficSliver/HyWF/CoMPS（流量拆分）**：
- 这些方案将流量拆分到多个路径，不引入时间和带宽开销
- 但只能防御观察单一路径的攻击者，本地攻击者（同一网络）可观察完整流量
- Palette 防御的是本地攻击者（ISP、AS、guard node），这是 WF 的标准威胁模型

### 5.3 创新点分析（表格形式）

| 创新点 | 说明 | 实验证据 |
|---|---|---|
| Traffic Cluster Anonymization | 受 k-anonymity 启发，将相似网站聚类为 anonymity set，实现类内不可区分 | T-SNE 可视化（Figure 15）显示同一 anonymity set 内的网站在特征空间中高度聚集 |
| TAM 作为 trace 表示 | 使用 TAM（2xN 矩阵）聚合多维信息，比 burst sequence 和 packet surges 更 informative | 所有 feature category 泄露均低于 1.1 bit，无单项泄露超过 undefended |
| Super-Matrix Refinement | Shrinking + Sampling 两步策略将初始 super-matrix 的极高开销降至可接受水平 | 从 3188% BOH（无 refinement）降至 84%；消融实验证明各组件贡献 |
| Early Sending + Tail Padding | 解决实时流量与预定义模式不匹配的问题，分别处理拥塞和空闲 | 去掉 early sending 后 TOH 升至 17%；去掉 tail padding 后 BOH 升至 282% |
| 信息泄露分析 | 使用 WeFDE 框架从信息论角度证明 Palette 泄露最少信息 | Top-500 features 平均泄露最低，且无单项泄露异常 |

### 5.4 适用场景

- **Tor 用户的实时浏览保护**：Palette 可作为 Pluggable Transport 部署在 Tor 网络中，已验证可行性
- **对抗 advanced WF 攻击者**：特别是使用 adversarial training 和深度学习的攻击者（RF/Tik-Tok/Var-CNN）
- **需要平衡安全性和性能的场景**：bandwidth/time overhead 可通过参数灵活调节（k 从 5 到 95）
- **不适合的场景**：需要可证明安全性的场景（Tamaraw/Supersequence 更合适）；multi-tab 浏览场景（论文假设单页面）

### 5.5 方法对比表

| 方法 | Trace 表示 | 抵抗 AdvTrain | 适应实时流量 | 掩盖 Features | 开销适中 | RF 准确率(CW) | RF 准确率(RW) | BOH | TOH |
|---|---|---|---|---|---|---|---|---|---|
| WTF-PAD | Packet Seq | 否 | 是 | 否 | 是 | 96.64% | - | 61% | 0% |
| FRONT | Packet Seq | 否 | 是 | 否 | 是 | 93.92% | 90.45% | 80%/99% | 0% |
| Supersequence | Packet Seq | 是 | 否 | 是 | 否 | 26.51% | - | 88% | 91% |
| Tamaraw | Packet Seq | 是 | 否 | 是 | 否 | 10.23% | 22.51% | 121%/135% | 43%/78% |
| Surakav | Burst Seq | 否 | 是 | 否 | 是 | 79.94% | 75.08% | 80%/81% | 6%/14% |
| RegulaTor | Pkt Surges | 否 | 是 | 否 | 是 | 53.11% | 66.67% | 80%/70% | 5%/112% |
| **Palette** | **Traffic Matrix** | **是** | **是** | **是** | **是** | **36.43%** | **53.28%** | **84%/80%** | **9%/24%** |

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **数据集**：公开 WF 数据集（95 个网站各 1000 条 trace 的 closed-world + 40716 个网站的 open-world）
- **WF 攻击**：6 种 SOTA 攻击（CUMUL, k-FP, DF, Tik-Tok, Var-CNN, RF），包含传统 ML 和深度学习方法
- **WF 防御**：6 种对比防御（Supersequence, Tamaraw, WTF-PAD, FRONT, Surakav, RegulaTor）
- **训练/验证/测试**：8:1:1 比例划分
- **真实 Tor 网络**：使用 WFDefProxy 框架实现为 Pluggable Transport，在真实 Tor 网络中采集数据
- **服务器配置**：Intel Core i7 3.4 GHz, 32GB 内存, 10GB GPU

### 6.2 数据集

| 数据集 | 网站数 | Trace 数 | 用途 |
|---|---|---|---|
| Closed-world | 95 | 每站 1000 | WF 防御评估 |
| Open-world | 40,716 | 每站 1 | 模拟真实 Tor 用户访问 |
| Real-world (Tranco) | 100 | 每站至少 100 | 真实 Tor 网络验证 |

### 6.3 Baseline

论文对比了 6 种代表性 WF 防御：
- **Obfuscation 类**：WTF-PAD, FRONT
- **Regularization 类**：Supersequence, Tamaraw, Surakav, RegulaTor

所有防御均使用作者提供的默认参数或论文中的推荐参数。

### 6.4 评价指标

- **Attack Accuracy（%）**：WF 攻击对 defended traffic 的分类准确率（越低越好）
- **Bandwidth Overhead (BOH, %)**：dummy packets 数与 real packets 数的比值
- **Time Overhead (TOH, %)**：最后一个 real packet 的延迟时间比
- **Information Leakage (Bit)**：基于 WeFDE 框架的信息泄露比特数
- **Precision-Recall Curve**：open-world 场景下的精确率-召回率曲线
- **TPR/FPR**：one-page setting 下的真正率和假正率

### 6.5 关键实验结果（表格形式）

**Closed-World 结果（Table 3，含 adversarial training）：**

| 防御 | BOH | TOH | k-FP | CUMUL | DF | Tik-Tok | Var-CNN | RF | 平均准确率 |
|---|---|---|---|---|---|---|---|---|---|
| Undefended | - | - | 94.54 | 94.81 | 98.23 | 98.45 | 98.83 | 98.40 | 97.21 |
| Supersequence | 88% | 91% | 27.28 | 24.71 | 29.09 | 29.18 | 17.89 | 26.51 | 25.78 |
| Tamaraw | 121% | 43% | 10.24 | 8.42 | 8.34 | 8.32 | 3.56 | 10.23 | 8.19 |
| WTF-PAD | 61% | 0% | 68.47 | 55.83 | 90.85 | 93.80 | 94.83 | 96.64 | 83.40 |
| FRONT | 80% | 0% | 52.34 | 23.22 | 76.10 | 84.79 | 80.97 | 93.92 | 68.56 |
| Surakav | 80% | 6% | 41.83 | 44.03 | 64.00 | 67.63 | 54.56 | 79.94 | 58.67 |
| RegulaTor | 80% | 5% | 39.17 | 16.30 | 20.41 | 29.06 | 40.51 | 53.11 | 33.09 |
| **Palette** | **84%** | **9%** | **29.39** | **10.96** | **20.27** | **24.73** | **22.79** | **36.43** | **24.10** |

Palette 的平均攻击准确率 24.10%，比 RegulaTor（33.09%）降低约 9 个百分点，比 Surakav（58.67%）降低约 34.5 个百分点。在所有 6 种攻击中，Palette 在 5 种上取得了最低准确率（k-FP/CUMUL/DF/Tik-Tok/Var-CNN），仅在 RF 上略高于 Tamaraw（36.43% vs 10.23%），但 Tamaraw 的开销是 Palette 的约 3 倍（121% BOH + 43% TOH vs 84% BOH + 9% TOH）。

**Real-World 结果（Table 6）：**

| 防御 | BOH | TOH | DF | Tik-Tok | Var-CNN | RF | 平均准确率 |
|---|---|---|---|---|---|---|---|
| Undefended | 0% | 0% | 91.80 | 93.20 | 94.40 | 98.20 | 94.40 |
| Tamaraw | 135% | 78% | 24.95 | 23.01 | 14.33 | 22.51 | 21.20 |
| FRONT | 99% | 0% | 55.19 | 57.19 | 54.23 | 90.45 | 64.27 |
| Surakav | 81% | 14% | 60.50 | 58.12 | 29.95 | 75.08 | 55.91 |
| RegulaTor | 70% | 112% | 62.42 | 56.16 | 31.95 | 66.67 | 54.30 |
| **Palette** | **80%** | **24%** | **13.97** | **11.35** | **4.58** | **53.28** | **20.80** |

Palette 在 real-world 中的平均准确率 20.80%，甚至低于 Tamaraw（21.20%），且 overhead 显著更低（80% BOH + 24% TOH vs 135% BOH + 78% TOH）。DF/Tik-Tok/Var-CNN 准确率均降至 15% 以下（13.97%/11.35%/4.58%），RF 准确率 53.28% 优于所有中等开销防御。

**关键发现**：

1. **AdvTrain vs. Non-AdvTrain 的差距**：Without adversarial training，所有防御都能将攻击准确率降至 16% 以下（Table 12）。这说明 adversarial training 是当前 WF 攻击的关键能力，防御评估必须考虑这一场景。

2. **信息泄露的不平衡性**：Table 13 显示 FRONT 虽然平均泄露低，但 Pkt. per Second 泄露 1.197 bit，Interval-II/III 甚至超过 undefended。RegulaTor 的 Pkt. per Second 泄露 1.401 bit（> undefended 1.347 bit）。这种不平衡泄露被 RF 利用，导致高攻击准确率。Palette 在所有 14 个 category 中都保持较低且均衡的泄露。

3. **Adaptive Attack 的韧性**：Table 9 显示两阶段 adaptive attack（先识别 anonymity set，再在 set 内分类）的最高准确率仅 36.92%（RF），比 AdvTrain 仅增加 0.49 个百分点。这证明同一 anonymity set 内的网站确实难以区分。

4. **Open-world 的强保护**：Figure 7 显示 Palette 将所有攻击的 recall 降至 0.1 以下（高 precision 时）。在 one-page setting（更难的 open-world 变体）中，Palette 在低 FPR（<0.1）范围内表现出最低的 TPR，优于所有中等开销防御。

5. **参数敏感性分析**：
   - k 从 5 增至 95：BOH 从 39% 增至 96%，RF 准确率从 70.70% 降至 25.49%（Table 5）
   - s 从 53ms 增至 160ms：BOH 降 46%，TOH 增 21%，RF 准确率从 38.55% 降至 28.62%（Figure 10）
   - alpha 从 0.1 增至 0.24：TOH 从 22% 降至 5%，BOH 从 60% 增至 123%（Figure 11）
   - B 和 U 的网格搜索（Figure 12）：B=45, U=20 为默认平衡点

### 6.6 优势最明显的场景

- **对抗 SOTA RF 攻击**：Palette 将 RF 准确率从 98.40% 降至 36.43%（closed-world），比次优的 RegulaTor 再降 16.68%。在 real-world 中降至 53.28%，优于所有中等开销防御（FRONT 90.45%, Surakav 75.08%, RegulaTor 66.67%）
- **Real-world 部署**：在真实 Tor 网络中，Palette 将 DF/Tik-Tok/Var-CNN 准确率降至 15% 以下（13.97%/11.35%/4.58%），这是中等开销防御中唯一能做到的方案
- **Open-world 场景**：precision-recall 曲线显示 Palette 将所有攻击的 recall 降至 0.1 以下（高 precision 时）。在 one-page setting 中，Palette 在低 FPR（<0.1）范围内 TPR 最低
- **对抗 adversarial training**：Palette 是唯一在 Table 1 中同时满足四个理想特性的防御。即使攻击者使用 adversarial training，RF 准确率也仅 36.43%
- **信息泄露控制**：Table 13 显示 Palette 在所有 14 个 feature category 中都保持较低泄露（最高 CUMUL 0.966 bit），无单项泄露超过 undefended
- **网络条件稳健性**：在不同带宽（80-160 Mbps）和不同浏览器（Tor/Chrome）条件下表现稳定（Table 7）

### 6.7 局限性

1. **网站列表依赖**：使用 Tranco 列表而非真实 Tor 用户访问列表，可能不反映真实场景。论文承认这是伦理和技术双重挑战——部署 exit node 可收集真实列表，但会泄露用户目的地
2. **单次访问假设**：假设用户一次只访问一个页面，不考虑 multi-tab 场景。虽然 multi-tab 攻击本身被认为困难，但实际用户行为是多标签的
3. **匿名集分配单一**：每个网站只属于一个 anonymity set，可被两阶段 adaptive attack 攻破（最高 36.92%）。论文建议将网站分配到多个 anonymity set 作为 future work
4. **参数调优复杂**：k, alpha, B, U, s 等参数需根据网络条件调优。论文建议的调优顺序：k -> U,B -> s,alpha
5. **时间开销真实世界增加**：real-world 中 time overhead 从仿真 9% 增至 24%，主要因为 incoming/outgoing packets 的依赖关系在仿真中难以完全模拟。RegulaTor 的增幅更大（5% -> 112%）
6. **性能随时间衰减**：5 天后 RF 准确率从 53.28% 降至 48.98%（bandwidth overhead 从 73% 略增至 75%），长期表现需进一步验证
7. **Without AdvTrain 优势不明显**：Table 12 显示 without adversarial training，所有防御都能将攻击准确率降至 16% 以下，Palette 的优势主要体现在 AdvTrain 场景

## 7. 学习与应用

### 7.1 是否开源？

是。Palette 的源代码在 https://github.com/kxdkxd/Palette 公开。论文还使用了 WFDefProxy 框架进行 real-world 部署评估。

### 7.2 复现关键步骤

1. **数据准备**：使用公开 WF 数据集（95 网站 x 1000 traces）或在 Tor 网络中采集 Tranco 列表网站（Tranco list 更新于 2023 年 2 月）
2. **TAM 构建**：将每个 trace 转换为 2x1000 的 TAM 矩阵（T=80s, s=80ms）
3. **网站聚类**：运行 Algorithm 1，设置 k=30，基于欧氏距离迭代构建 anonymity set
4. **Super-Matrix 构建**：对每个 anonymity set 取各时间槽最大值
5. **Super-Matrix Refinement**：训练 w 和 b 进行 shrinking，估计 PMF 进行 sampling（alpha=0.16）
6. **在线 Trace Regularization**：部署为 Pluggable Transport，在 real-time 根据 refined super-matrix 发包
7. **参数设置**：k=30, alpha=0.16, B=45, U=20, s=80ms

### 7.3 关键超参数、预处理和训练细节

| 参数 | 默认值 | 说明 | 敏感性 |
|---|---|---|---|
| k (anonymity set size) | 30 | 匿名集大小，越大匿名性越强但开销越高 | 高：k 从 5 到 95，BOH 增 57%，RF 准确率从 70.70% 降至 25.49% |
| alpha (sampling threshold) | 0.16 | 控制采样时间槽数量，越大采样越少 | 中：alpha 从 0.1 到 0.24，TOH 从 22% 降至 5%，BOH 从 60% 增至 123% |
| B (tail padding multiple) | 45 | 缓冲区为空时每 B 个时间槽检查是否停止填充 | 中：增大 B 增加 BOH 但提高匿名度 |
| U (early sending upper bound) | 20 | 控制提前发送的激进程度 | 中：降低 U 减少 TOH 但增加 BOH 且泄露 timing features |
| s (time slot) | 80ms | TAM 时间槽粒度 | 低：s 从 53ms 到 160ms，BOH 降 46%，TOH 增 21%，RF 从 38.55% 降至 28.62% |
| T (max load time) | 80s | 最大网站加载时间 | 低：需覆盖大多数网站的加载过程 |
| N (number of slots) | 1000 | 时间槽总数 T/s | 低：由 T 和 s 决定 |
| lambda (loss balance) | 0.5 | 平衡 bandwidth 和 time overhead | 低：0.5 为平衡点 |
| tau (shrinking threshold) | 10 | 控制 shrinking 调整范围 | 低 |

**调优策略**（论文 Section 8 建议）：先确定 k（匿名度），再调 U 和 B（开销平衡），最后调 s 和 alpha（进一步优化开销）。

### 7.4 实际部署可行性分析

**部署开销**：
- 训练开销：Anonymity set generation 约 112s，super-matrix refinement 约 75-149s（取决于 k），在标准服务器上可快速完成
- 存储开销：k=5 时仅 228KB，k=95 时仅 17KB。客户端和 middle node 只需存储各自方向的 super-matrix 和 PMF
- 通信开销：每 5 天更新一次，即使 1000 万客户端也仅占 0.66% 带宽（Figure 13）
- 在线处理开销：每个时间槽（80ms）仅需简单的数值比较和发包决策，计算开销极低

**部署方式**：
- Tor directory server 负责离线训练和数据分发
- 客户端在 Tor 启动时下载 super-matrix/PMF/mapping，本地缓存
- 实现为 Pluggable Transport（PT），无需修改 Tor 核心代码
- Client 和 middle node 协同工作：client 调节 outgoing packets，middle node 调节 incoming packets

**实际约束**：
- 需要 Tor middle node 的配合（部署 Palette PT）
- 需要定期更新 super-matrix 以适应网站流量模式变化
- Tranco 列表可能不反映真实 Tor 用户访问偏好，但目前没有更好的公开替代方案

### 7.5 能否迁移到其他任务？

- **其他匿名网络**：核心思路（聚类相似流量 + 统一模式）可迁移到 I2P、VPN 等匿名网络的流量保护
- **Traffic analysis 防御**：TAM 表示和 super-matrix refinement 的思路可用于其他流量分析防御场景
- **k-anonymity 在网络流量中的应用**：anonymity set generation 的方法可推广到其他需要流量匿名化的场景
- **隐私保护的流量调节**：early sending 和 tail padding 的实时调整策略可用于其他在线流量调节任务

### 7.6 对我的研究有什么启发？

1. **利用相似性降低开销**：将相似实体聚类后统一处理，比对所有实体使用固定模式更高效。这个思路可以推广到其他需要"统一化"处理的场景
2. **TAM 作为通用表示**：TAM 是一个 robust 的流量表示，已被 SOTA 攻击（RF）和防御（Palette）同时采用，说明它在粒度和信息保留之间取得了好的平衡
3. **信息泄露分析的重要性**：仅看攻击准确率不够——FRONT 和 Palette 的平均泄露相近，但 FRONT 的 Pkt. per Second 泄露 1.197 bit 导致被 RF 击穿。需要从信息论角度分析各 feature category 的泄露情况
4. **实时流量与预定义模式的匹配问题**：early sending 和 tail padding 是解决动态流量与静态模式不匹配的实用策略，这个思路可以用于其他在线流量调节任务
5. **对抗性评估**：防御评估必须考虑 adversarial training 和 adaptive attack，否则会高估防御效果。Table 12 显示 without AdvTrain 所有防御都能将准确率降至 16% 以下，但 with AdvTrain 差距巨大
6. **Meta-review 的启示**：S&P meta-review 指出 Palette 的改进主要体现在 AdvTrain 场景，real-world 部署中需要权衡攻击者能力与开销。这提醒我们防御设计需要明确目标威胁模型

## 8. 总结

### 8.1 核心思想（不超过20字）

聚类相似网站为匿名集，统一流量模式，实现低开销 WF 防御。

### 8.2 速记版 Pipeline（3-5步）

1. 用 TAM 表示流量 trace，将相似网站聚类为 anonymity set（至少 k 个）
2. 为每个 set 构建 super-matrix（取各时间槽最大值），再通过 shrinking 和 sampling 精炼
3. 在线根据 refined super-matrix 指导发包，配合 early sending 和 tail padding 实时调整
4. 结果：攻击者在同一 anonymity set 内无法区分网站，实现 k-anonymity 保护

## 9. Obsidian 知识链接

### 9.1 相关概念

- Website Fingerprinting (WF) - 网站指纹攻击
- Tor Anonymity Network - Tor 匿名网络
- k-Anonymity - k-匿名性
- Traffic Analysis - 流量分析
- Anonymity Set - 匿名集
- Pluggable Transport - Tor 可插拔传输
- Adversarial Training - 对抗训练

### 9.2 相关方法

- Traffic Aggregation Matrix (TAM) - 流量聚合矩阵
- Super-Matrix Refinement - 超矩阵精炼
- Trace Regularization - 流量正则化
- Information Leakage Measurement (WeFDE) - 信息泄露测量框架
- Gradient Descent for Traffic Shaping - 梯度下降优化流量整形

### 9.3 相关任务

- WF Defense - 网站指纹防御
- Tor Traffic Protection - Tor 流量保护
- Traffic Obfuscation - 流量混淆
- Network Privacy - 网络隐私

### 9.4 可更新的综述页面

- Website Fingerprinting Attacks and Defenses Survey
- Tor Privacy Enhancement Techniques
- Traffic Analysis Defense Methods

### 9.5 可加入的对比表

- WF Defense Methods Comparison
- Closed-World WF Attack Results
- Real-World WF Defense Evaluation

## 10. 证据记录（表格形式）

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E1 | 实验结果 | Palette closed-world 将 RF 攻击准确率降至 36.43%，比 RegulaTor 低 16.68% | Table 3 |
| E2 | 实验结果 | Palette closed-world 平均将 6 种攻击准确率降至 24.10%，开销 84% BOH + 9% TOH | Table 3 |
| E3 | 实验结果 | Real-world 中 Palette 将 DF/Tik-Tok/Var-CNN 准确率降至 15% 以下（13.97%/11.35%/4.58%） | Table 6 |
| E4 | 实验结果 | Real-world 中 RF 准确率 53.28%，优于所有中等开销防御（FRONT 90.45%, Surakav 75.08%, RegulaTor 66.67%） | Table 6 |
| E5 | 实验结果 | 信息泄露分析：Palette 在所有防御中 Top-500 features 平均泄露最少，且所有 14 个 feature category 泄露均低于 1.1 bit | Figure 9, Table 13 |
| E6 | 实验结果 | Adaptive attack 最高准确率仅 36.92%（RF），比 AdvTrain 仅增 0.49 个百分点 | Table 9 |
| E7 | 实验结果 | Open-world 中 Palette 将所有攻击 recall 降至 0.1 以下（高 precision 时） | Figure 7 |
| E8 | 实验结果 | Cover rate 超过 95%，证明 super-matrix 可泛化到未见 trace | Figure 4(b) |
| E9 | 实验结果 | k=4 时 anonymity set 平均包含至少 3 个网站类别，k=10 时 dominant category 比例不超过 30% | Appendix A, Figure 14 |
| E10 | 实验结果 | 5 天后 Palette 仍有效（RF 准确率 48.98%，bandwidth overhead 75%） | Section 6.6 |
| E11 | 实验结果 | 通信开销：每 5 天更新，1000 万客户端时仅 0.66% | Figure 13 |
| E12 | 参数分析 | k 从 5 增至 95，bandwidth 增 57%（39%->96%），RF 准确率从 70.70% 降至 25.49% | Table 5 |
| E13 | 参数分析 | alpha 从 0.1 增至 0.24，time overhead 从 22% 降至 5%，bandwidth overhead 从 60% 增至 123% | Figure 11 |
| E14 | 消融实验 | 去掉聚类后 RF 准确率从 36.43% 升至 41.52%（+5.09%） | Table 14 |
| E15 | 消融实验 | 去掉所有 refinement 后 bandwidth overhead 高达 3188% | Table 14 |
| E16 | 消融实验 | 去掉 shrinking 后 BOH 升至 490%，但 RF 准确率降至 26.72%（更安全但不可接受的开销） | Table 14 |
| E17 | 消融实验 | 去掉 sampling 后 BOH 升至 770%，RF 准确率升至 55.70%（sampling 引入随机噪声有防御效果） | Table 14 |
| E18 | 消融实验 | 去掉 early sending 后 TOH 从 9% 升至 17%，RF 准确率降至 32.19%（更安全但更高延迟） | Table 14 |
| E19 | 消融实验 | 去掉 tail padding 后 BOH 从 84% 升至 282%，RF 准确率降至 14.29%（更安全但极高带宽开销） | Table 14 |
| E20 | 对比分析 | Without adversarial training，所有防御都能将攻击准确率降至 16% 以下，Palette 优势主要体现在 AdvTrain 场景 | Table 12 |
| E21 | 对比分析 | FRONT 的 Pkt. per Second 泄露 1.197 bit，RegulaTor 泄露 1.401 bit（> undefended 1.347 bit），解释了它们被 RF 击穿的原因 | Table 13 |
| E22 | 对比分析 | Supersequence 和 Tamaraw 在 Time 和 Burst 等 category 泄露反而超过 undefended（因 padding 改变了统计特征） | Table 13 |
| E23 | 部署数据 | 训练开销：generation 约 112s，refinement 约 75-149s；存储 k=5 时 228KB，k=95 时 17KB | Table 8 |
| E24 | 部署数据 | 网络稳健性：带宽 80-160 Mbps 下 RF 准确率 47.74%-50.87%，Chrome 下 24.47%（更低 BOH 19%） | Table 7 |
| E25 | 理论分析 | 每个 anonymity set 至少 k 个网站，攻击者最多以 1/k 概率猜测目标网站（k-anonymity 保证） | Section 4 |
| E26 | 实验结果 | 15/19 个 anonymity set 的 intra-class distance 小于 inter-class distance 的 25th percentile | Figure 4(a) |
| E27 | Meta-review | S&P meta-review 确认 Palette 的"clever insight"——相似网站可统一调节为相同模式且低开销 | Appendix G |

## 11. 原始资料链接

- 论文发表于 IEEE S&P 2024
- 作者单位：北京理工大学网络空间安全学院（沈蒙、季珂鑫、吴锦鹤、孔祥东、祝烈煌），清华大学网络科学与网络空间研究院（李琦），清华大学计算机科学与技术系（徐恪）
- 开源代码：https://github.com/kxdkxd/Palette
- 使用的数据集：公开 WF 数据集（Sirinam et al., CCS 2018）和 Tranco 列表
- 关键引用：RF 攻击 [9]（Shen et al., USENIX Security 2023），RegulaTor [16]，Surakav [17]
- 项目资助：国家重点研发计划 2023YFB2703800，NSFC 62132011/62222201/U23A20304，北京新星计划 20220484174

## 12. 后续问题

1. **多 anonymity set 分配**：能否将一个网站分配到多个 anonymity set，使不同访问呈现不同模式，增加 adaptive attack 难度？
2. **更大规模网站聚类**：能否在 open-world 场景下进行更大规模的网站聚类，提高每个 set 内的相似性？
3. **长期性能稳定性**：Palette 的 super-matrix 和参数在更长时间跨度（数周/数月）后是否仍有效？
4. **Tor 用户真实访问列表**：如何在不侵犯 Tor 用户隐私的前提下收集更真实的网站列表用于 WF 研究？
5. **Multi-tab 场景**：Palette 在用户同时打开多个标签页时的表现如何？
6. **与其他防御的组合**：Palette 能否与流量拆分（TrafficSliver）等方案结合，进一步增强保护？
7. **动态 anonymity set 更新**：随着网站流量模式变化，能否动态更新 anonymity set 的划分？
8. **对更先进攻击的鲁棒性**：如果攻击者使用 TAM 的变体或其他更高级特征表示，Palette 是否仍然有效？

---
type: paper
title_original: "AdaDoHTool: A test-time adaptive framework for identifying DoH tunneling tools with unknown resolvers"
title_cn: "AdaDoHTool：面向未知解析器的 DoH 隧道工具识别的测试时自适应框架"
authors: [Yandu Yi, Xiaoyan Hu, Yang Miao, Guang Cheng, Ruidong Li, Hua Wu]
year: 2026
venue: "Journal of Computer Networks 2026"
doi: "10.1016/j.comnet.2026.112645"
url: "https://doi.org/10.1016/j.comnet.2026.112645"
pdf: "00-inbox/PDFs/2026-JCN-AdaDoHTool_A_test-time_adaptive_framework_for_identifying_DoH_tunneling_tools_with_unknown_resolvers.pdf"
mineru_md: "02-parsed-markdown/2026-JCN-AdaDoHTool_A_test-time_adaptive_framework_for_identifying_DoH_tunneling_tools_with_unknown_resolvers.md"
status: processed
reading_level: L2
research_area: [encrypted-traffic-analysis, tunnel-detection, traffic-classification]
task: [tunnel-detection, traffic-classification]
method: [convolutional-network, pre-training-finetuning]
dataset: ["CIRA-CIC-DoHBrw-2020", "DoH-Tunnel-Traffic-HKD"]
code: unknown
relevance: medium
created: "2026-09-19"
updated: "2026-09-19"
---

# AdaDoHTool: A test-time adaptive framework for identifying DoH tunneling tools with unknown resolvers

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | AdaDoHTool: A test-time adaptive framework for identifying DoH tunneling tools with unknown resolvers |
| 中文标题 | AdaDoHTool：面向未知解析器的 DoH 隧道工具识别的测试时自适应框架 |
| 作者 | Yandu Yi, Xiaoyan Hu, Yang Miao, Guang Cheng, Ruidong Li, Hua Wu（东南大学网络空间安全学院 / 紫金山实验室 / 金泽大学） |
| 年份 | 2026 |
| 会议/期刊 | Journal of Computer Networks 2026（Computer Networks, Elsevier） |
| 研究方向 | encrypted-traffic-analysis / tunnel-detection / traffic-classification |
| 任务类型 | DoH 隧道工具细粒度识别（tunneling tool identification）+ 未知 resolver 的跨域自适应 |
| 方法关键词 | test-time adaptation、Word2Vec (CBOW) embedding、TextCNN、KNN-aware loss、feature–label memory bank、KNN similarity-weighted voting |
| 数据集 | CIRA-CIC-DoHBrw-2020（扩充：新增 Qihoo-360 / DNSPod / OpenDNS / Mullvad 采集流量）、DoH-Tunnel-Traffic-HKD |
| 是否开源 | 未提及代码仓库；原文 "Data availability: Data will be made available on request" |
| PDF | 00-inbox/PDFs/2026-JCN-AdaDoHTool_A_test-time_adaptive_framework_for_identifying_DoH_tunneling_tools_with_unknown_resolvers.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-JCN-AdaDoHTool_A_test-time_adaptive_framework_for_identifying_DoH_tunneling_tools_with_unknown_resolvers.md |

> ⚠️ MinerU 解析问题：§I 第 2 段严重掉字——"First, it adopts KNN-aware repl h f f b l ll h model to preserve a more reliable neighborhood structure"，中间整段词句丢失，语义只能依据 §4.3 复原。
> ⚠️ MinerU 解析问题：§3 问题定义段数学符号丢失（"Let the input space be denoted as   and the label space as …，其中 � 表示 benign DoH traffic"），变量符号被替换为占位符。
> ⚠️ MinerU 解析问题：§2.1、§2.2、§5.3、§5.4.2 多处出现连续字母碎片（如 "Bannat Wala l [ ] ll d ffi f h bli l"、"We compute h f d f h h d l h ld l d from known classes"、"resolver-induced d b h f"），为解析掉字，引用时已按上下文还原。

---

## 1. 一句话总结

> 把 DoH 隧道工具识别重构成"跨 resolver 域的测试时自适应"问题：TLS 应用数据记录长度序列 → Word2Vec 词向量 → TextCNN + KNN-aware loss 预训练 → 特征-标签记忆库在线更新 + KNN 投票，未知 resolver 上 0% 标注平均 0.7125、10% 标注平均 0.8463。

---

## 2. 摘要翻译

### 2.1 摘要原文

> With the development of Domain Name System (DNS) encryption technologies, DNS over HTTPS (DoH) has emerged as a mainstream encrypted protocol. It enhances the security and privacy of traditional DNS while also providing malicious actors with a new covert channel for tunneling. Existing DoH tunneling traffic detection methods suffer significant performance degradation when encountering unknown recursive resolvers due to the diversity of resolver padding strategies and configuration differences, resulting in insufficient model generalization and adaptability. We propose AdaDoHTool, a test-time adaptive identification method for DoH tunneling tools targeting unknown recursive resolvers to address this issue. AdaDoHTool uses a word embedding matrix generated from unidirectional TLS application data record length sequences as input, applies a TextCNN model to extract deep feature representations, and incorporates a feature–label memory bank with an online update mechanism. Combined with a KNN classifier and a dedicated loss function, AdaDoHTool enhances feature transferability and target-domain adaptability. Experimental results show that under target domain conditions with no labeled data (0%) and with a small amount of labeled data (10%), AdaDoHTool achieves average accuracies of 0.71 and 0.85, respectively, improving upon other comparison methods by 7.41% and 25.62%, respectively. Moreover, the method maintains low memory consumption. Its inference time is only 30.5% of the fastest baseline model.

### 2.2 摘要中文翻译

> 随着 DNS 加密技术的发展，DNS over HTTPS（DoH）已成为主流的加密协议。它在增强传统 DNS 安全性与隐私性的同时，也为攻击者提供了新的隐蔽隧道信道。由于不同 resolver 的 padding 策略与配置差异，现有 DoH 隧道流量检测方法在遇到未知递归解析器时性能显著退化，模型泛化性与自适应能力不足。为此，本文提出 AdaDoHTool——一种面向未知递归解析器的、测试时自适应的 DoH 隧道工具识别方法。AdaDoHTool 以单向 TLS 应用数据记录长度序列生成的词嵌入矩阵为输入，用 TextCNN 提取深层特征表示，并引入带在线更新机制的特征–标签记忆库；结合 KNN 分类器与专用损失函数，提升了特征可迁移性与目标域自适应能力。实验结果显示：在目标域无标注（0%）与少量标注（10%）两种条件下，AdaDoHTool 平均准确率分别为 0.71 与 0.85，相比其他对比方法分别提升 7.41% 与 25.62%；同时内存占用低，推理时间仅为最快基线模型的 30.5%。

> ⚠️ 摘要中 "7.41%" 与 "25.62%" 两个提升幅度在正文表格中无法直接复算（§5.3 给出的是相对 WEDoHTool +17.51%、METC-Seq +13.95%、DAN +10.27% 口径），引用时需注意口径不一致。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

DoH 把 DNS 查询封装进 HTTPS，攻击者（如 Godlua 恶意软件）利用其建立 C&C 与数据外传的隐蔽隧道（§1）。已有 DoH/DoH 隧道检测工作多数假设训练与测试流量分布一致，忽略了 **递归解析器（recursive resolver）多样性** 带来的分布漂移：DoH 协议并未强制统一的 padding 策略，仅建议使用 EDNS(0) padding（RFC 7830 / RFC 8467），不同 resolver 的实现、部署位置与服务端配置会让同一隧道工具的流量模式发生变化（§1、§2.3）。

### 3.2 现有方法的痛点和不足

1. **未知 resolver 下性能骤降**：训练期未见的 resolver 会让模型的输入分布发生偏移，离线模型泛化不足（§1、§2.3）。
2. **离线训练范式缺乏在线更新能力**：新 resolver 出现时需要重新采集标注数据并从零重训，实时响应能力受限（§1）。
3. **既有 DoH 研究多为"隧道检测"而非"工具识别"**：粒度较粗，无法直接支撑对具体隧道工具的判别（§2.2 末段）。
4. **UDDA/DA 方法需要训练期接触目标域**：DAN/DSAN/DANN/CDANs 等分布匹配或对抗方法都要求在训练阶段获得目标域数据，而真实部署中未知 resolver 的流量只有在部署后才出现（§3 末段）。

### 3.3 论文的研究假设或核心直觉

核心直觉：**不更新骨干参数、只更新"决策参考集"，也能实现跨 resolver 自适应**。把源域样本的 feature–label 对放进一个记忆库；推理时用 KNN 相似度加权投票做预测，并把高置信度的目标域样本（连同伪标签）回填记忆库；记忆库随测试流渐进向目标域分布靠拢，从而在不改动 TextCNN 参数的前提下移动有效决策边界（§4.1、§4.4）。为使特征空间与 KNN 推理方式一致，还设计了 KNN-aware 损失 $L_{\mathrm{KNN}}$ 替代交叉熵，保持类内多样性并强化类间可分（§4.3）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | DoH 未强制 padding 策略；KDE 与 UMAP 显示不同 resolver 下 TLS 记录长度分布与相同工具（dnscat2）的特征聚类明显不同 | §5.2、Fig. 2、Fig. 5、Fig. 6 |
| 痛点提炼 | 训练期只见过部分 resolver 的模型，在 Qihoo-360/DNSPod 等未见 resolver 上准确率骤降；重新标注+重训的代价不可接受 | §1、§5.3（Exp. 5 全部方法掉至 0.55–0.65 区间） |
| 问题转化 | 把"DoH 隧道工具识别"形式化为跨域分类问题 $D_S \to D_T$（标签空间相同、联合分布不同），并要求测试时在线自适应 | §3 式 (1) |
| 文献定位 | 既有工作只在 Zhan et al. 等少数研究中把 resolver 类型当作实验变量，未作为核心问题；TTA 在计算机视觉已成熟但在加密流量分析中应用有限 | §2.2、§2.3 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 保持骨干冻结、用"高置信度样本在线更新的 feature–label 记忆库 + KNN 投票"即可在未知 resolver 上获得优于离线模型与参数更新式 TTA 的识别性能 | §4.3、§4.4（含推断：假设由 T3A/Tent 的局限自然导出） | 5 个 resolver 域的 leave-one-resolver-out 实验（Exp. 1–5）+ 4 组新增 resolver（Exp. 6–9） |
| 辅助假设 | 与 KNN 推理相匹配的 $L_{\mathrm{KNN}}$ 损失比交叉熵学到更可迁移的表示（保留类内多样性） | §4.3.1、Fig. 9 | 消融实验 w/o $L_{\mathrm{KNN}}$（Table 8） |
| 辅助假设 | 置信度阈值过滤可抑制伪标签噪声，使记忆库更新"既够快又够准" | §4.4.2、Algorithm 1 | 阈值敏感性分析（Fig. 8b）与 w/o confidence threshold 消融 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑（有保留） | 0% 标注平均 0.7125 高于 T3A 0.6863/Tent 0.6641 等；移除记忆库在线更新后跌至 0.5886（−17.39%）；Exp. 5（Qihoo-360 且 0%）0.5825 略低于 WEDoHTool 0.5888 | Table 4、Table 8、§5.3 |
| 辅助假设（$L_{\mathrm{KNN}}$） | 部分支撑 | 平均 0.7125 vs 交叉熵 0.7088，仅 +0.52%，且 Exp. 1/Exp. 5 交叉熵更好；但 Fig. 9 显示 $L_{\mathrm{KNN}}$ 的类间分离与类内结构更清晰 | Table 8、Fig. 9 |
| 辅助假设（置信阈值） | 支撑 | 去掉阈值后 0.7125 → 0.6214（−12.79%）；阈值 0.70–0.85 区间稳定，0.75 最优 | Table 8、Fig. 8b |

---

## 4. 方法设计

### 4.1 方法整体流程

AdaDoHTool 由三个模块组成（§4.1、Fig. 1）：(1) **词嵌入向量生成**——把单向流的 TLS 应用数据记录长度序列当"句子"、长度值当"词"，用 Word2Vec(CBOW) 得到嵌入矩阵；(2) **可迁移表示学习**——用 TextCNN + $L_{\mathrm{KNN}}$ 在源域训练，并把源域 feature–label 对灌入记忆库；(3) **记忆增强的测试时自适应**——KNN 从记忆库检索 top-k 近邻做相似度加权投票，并对高置信度目标样本在线回填记忆库（FIFO 淘汰），骨干参数全程冻结。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 采集与过滤 | pcap | 提取单向流；只保留源或目的 IP 命中指定公共 DoH resolver 的流 | 目标流集合 | 排除无关流量（§5.1） |
| Step 2 特征构造 | 流 | 解析 TLS 记录，仅保留应用数据记录，按时间序取长度序列；取前 15 个长度值，不足补零 | 定长长度序列（15） | 长度侧信道特征（§4.2.1、§5.1） |
| Step 3 词嵌入 | 长度序列 | 用 Word2Vec(CBOW) 把每个长度值映射为向量（embedding dim=64），整条序列构成嵌入矩阵 | 词嵌入矩阵 | 抗稀疏、捕获上下文依赖（§4.2.2） |
| Step 4 源域预训练 | 嵌入矩阵 + 源域标签 | TextCNN（窗口 3/4/5）在 $L_{\mathrm{KNN}}$ 下训练，同步把每个源的 feature–label 对写入记忆库 | 冻结骨干 + 初始记忆库 | 学可迁移表示（§4.3） |
| Step 5 测试时推理 | 目标样本 | KNN 检索记忆库 top-k，按余弦相似度加权投票并 softmax 得标签 | 预测标签 + 置信度 | 免参数更新的分类（§4.4.1、式 (8)） |
| Step 6 记忆库在线更新 | 高置信目标样本 | 若置信度 ≥ τ（0.75），把 (feature, 伪标签) 插入记忆库；超容量按 FIFO 淘汰最旧条目 | 更新后的记忆库 | 渐进对齐目标分布（§4.4.2、Algorithm 1） |
| Step 7（可选）少量标注微调 | 目标域少量标注样本 | 预训练 + 微调范式；微调样本同样按协议入记忆库 | 目标域敏感模型 | 10%/20% 标注设定（§4.4.2 末段） |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Word embedding 生成 | CBOW 架构，窗口 2m，最大化上下文预测目标词的对数概率（式 (2)(3)） | TLS 记录长度序列（15） | 64 维词嵌入矩阵 | 为 TextCNN 提供输入；不做图像化格式转换 |
| KNN-aware TextCNN 骨干 | 卷积窗口 3/4/5，每窗口 32 个滤波器（由记忆库内存估算 96 = 3×32 推断）；dropout 0.5 | 嵌入矩阵 | 96 维特征向量 $h_\theta(x)$ | 冻结于推理期；特征同时供 KNN 与记忆库使用 |
| $L_{\mathrm{KNN}}$ 损失 | 在 top-k 邻居上做相似度加权的类内对数似然（式 (4)–(7)），温度 τ'=0.1 | 源域 batch 的成对余弦相似度 | 训练梯度 | 替代交叉熵，保持类内多样性（§4.3.1） |
| 特征–标签记忆库 $M$ | 存 (feature, label/pseudo-label)，容量 30000，FIFO 淘汰 | 源域训练样本 + 高置信目标样本 | 检索库 | 桥接训练与测试；在线更新实现 TTA（§4.3.2、§4.4.2） |
| KNN 分类器 | top-k 近邻余弦相似度加权投票 + softmax（式 (8)） | 目标特征 + 记忆库 | 标签与置信度 | 决定是否触发记忆库写入（阈值 0.75） |

### 4.4 公式、算法和机制解释

- **跨域问题定义**（§3）：标签空间 $\mathcal{Y}=\{B,M_1,\dots,M_n\}$（B 为良性 DoH，$M_k$ 为第 k 个隧道工具）；源域 $D_S$ 有标注、目标域 $D_T$ 来自未见 resolver，联合分布不同；目标为 $F(x)=\arg\max_y P(y\mid x;\theta)$（式 (1)）。
- **$L_{\mathrm{KNN}}$**（式 (4)–(7)）：$-\frac{1}{n_s}\sum_i \log \frac{N_i}{D_i}$，其中 $N_i$、$D_i$ 为 top-k 邻居上以 $\exp(w_{ij}/\tau)$ 加权的"同类项 / 全部项"，$w_{ij}$ 为特征余弦相似度。直觉：把交叉熵的"类原型压缩"换成"邻域一致性"，保留类内多样性。
- **KNN 投票分类**（式 (8)）：$\eta_k(x_u)=\mathrm{softmax}\big(\sum_{j\in B_{(k,\theta,M)}(x_u)} w_{uj}\cdot \mathbf{1}\{y_j\}\big)$，即用近邻标签的相似度加权和做 softmax。
- **在线更新**（Algorithm 1）：逐样本推理 → 若置信度 $\rho_u\ge\tau$ 则 $M \leftarrow M\cup\{(h_\theta(x_u),\hat y_u)\}$；$|M|>C$ 时 FIFO 淘汰。内存开销 30000×(96×4+1×8) ≈ 0.01095 GB（§5.7）。
- **复杂度**（式 (9)–(11)）：单样本推理 $O(Cd + C\log K + K|\mathcal{Y}|)$，记忆库空间 $O(Cd)$，均随容量 C 线性增长；当 C 有界时可兼顾在线自适应与开销可控（§4.5）。

### 4.5 方法优势

1. **免重训**：骨干冻结，靠记忆库调整决策边界，避免了参数更新式 TTA 的模型漂移与额外算力（§2.3 末段）。
2. **粒度更细**：相比"是否隧道"的二分类，直接识别具体隧道工具（dns2tcp/dnscat2/iodine 等）（§2.2 末段）。
3. **样本级而非类原型级**：比 T3A 的类级伪原型更细粒度，能利用样本级目标信息（§5.3 讨论）。
4. **效率高**：推理 0.0054 ms/sample（最快基线的 30.5%），记忆库内存约 0.011 GB（Table 9、§5.7）。
5. **兼容半监督**：同一机制可插入少量目标域标注（10%/20%）进一步提升（§4.4.2 末段、Table 5）。

### 4.6 方法不足

1. **伪标签污染无根治手段**：置信阈值不能保证入库样本正确，可能随时间强化错误模式（§6 讨论）。
2. **极端分布漂移下失效**：Exp. 5（Qihoo-360，0% 标注）0% 设定下略低于不做自适应的 WEDoHTool，作者解释为高置信更新在证据不足时收益有限（§5.3）。
3. **特征可被规避**：所用 TLS 记录长度可被 padding 混淆或对抗扰动，作者将其列为未来工作（§6）。
4. **依赖前 15 个 TLS 应用数据记录**：更长的隧道会话或不同握手模式下的鲁棒性未讨论；短流需补零（§5.1）。
5. **需要目标域流量在线可得**：TTA 的前提是测试样本持续到达，冷启动阶段（记忆库仍以源域为主）性能最弱。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

主流方案是"离线监督训练统计特征/深度模型"（如 METC、WEDoHTool），把 resolver 差异当噪声；域自适应方案（DAN/DANN/CDANs/DSAN）需要在训练期访问目标域；参数更新式 TTA（Tent）会改模型参数。AdaDoHTool 的差异在于：**训练期不接触目标域、推理期不改参数**，只把目标域信息沉淀进一个可淘汰的特征-标签记忆库，靠 KNN 投票改变有效决策边界（§2.2 末段、§2.3）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 问题重构 | 首次（就作者所知）把"未知 resolver 下的 DoH 隧道工具识别"形式化为测试时自适应问题（§1、§3） | 高 | 是（任何存在部署期域漂移的流量任务） |
| 特征–标签记忆库 + 在线更新 | 样本级记忆库 + 置信阈值门控写入 + FIFO 淘汰，替代参数更新实现 TTA | 高 | 是（与骨干无关的通用包装） |
| KNN-aware 损失 | 用邻域一致性目标替代交叉熵，与 KNN 推理机制对齐 | 中 | 是（任何 KNN/检索式推理场景） |
| TLS 记录长度 + 词嵌入输入 | 沿用作者前作 WEDoHTool 的表示（TLS 应用数据记录长度 + Word2Vec），首次用于跨 resolver 场景 | 中 | 是（长度侧信道特征构造的通用做法） |
| 跨区域泛化实验设计 | 引入国产 resolver（Qihoo-360/DNSPod）与特殊配置 resolver（Mullvad ad-blocking），构造 9 组域迁移实验 | 中 | 是（评测协议） |

### 5.3 适用场景

- 部署环境中的 DoH resolver 集合与训练期不同（换用国产/企业自建/带过滤功能的 resolver）时的隧道工具识别（§5.1、§5.4.1）。
- 需要在线持续识别、且不便重训的边缘/网关侧检测（推理 0.0054 ms/样本、内存约 11 MB 量级，§5.7）。
- 训练期拿不到目标域流量、仅有少量标注（10%）甚至零标注的场景（Table 4、Table 5）。
- **不适用**：目标 resolver 分布与源域差异极端（如 Qihoo-360 在 0% 标注下）且完全没有任何可靠目标证据时，TTA 收益可能被伪标签噪声抵消（§5.3）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| WEDoHTool [6]（前作） | 词嵌入 + TextCNN/Transformer 两阶段，早期识别性能好 | 离线范式，假设训练/测试同分布 | 引入记忆库在线自适应 |
| METC-Seq [19] | CNN-BiGRU-Attention 混合结构 | 统计特征/离线训练，跨 resolver 泛化一般 | 以 TTA 处理分布漂移 |
| T3A [25] | 无需训练、类原型调整，Exp. 2/3 略优 | 类级伪原型在漂移大时不可靠，Exp. 1/4/5 落后 | 样本级记忆库 + 相似度加权投票 |
| Tent [24] | 熵最小化在线更新，思想简单 | 需更新参数，存在漂移/算力问题 | 冻结骨干，只更新记忆库 |
| DAN/DANN/CDANs/DSAN | 经典域自适应，10% 标注下 DAN 最强（0.7675） | 训练期需目标域数据 | 测试时自适应，AdaDoHTool 0.8463（+10.27% vs DAN） |
| **AdaDoHTool（本文）** | 0% 标注 0.7125、10% 标注 0.8463，均值为最高；推理最快（0.0054 ms） | Exp. 5/0% 略低于 WEDoHTool；伪标签污染风险 | — |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **域划分**（§5.1）：按 DoH 递归解析器划分 5 个域（AdGuard、Cloudflare、Google DNS、Quad9、Qihoo-360），每域 4 类（benign-DoH、dns2tcp、dnscat2、iodine）。
- **实验组**（Table 3）：Exp. 1–4 为 4 个国外 resolver 的 leave-one-resolver-out；Exp. 5 为"国外 resolver → 国产 Qihoo-360"的跨区域迁移；Exp. 6–9 追加 OpenDNS、DNSPod、Mullvad(ad-blocking)、以及"加入 Qihoo-360 后迁移至 DNSPod"（§5.4.1）。
- **标注比例**：0% / 10% / 20% 目标域标注三种设定（§5.1）。
- **数据划分**：每个 resolver 随机采样 5 次、每次用 3 个随机种子划分训练/测试，报告均值（§5.1）。
- **环境**：Ubuntu 22.04、i9-14900K、PyTorch-GPU 2.1.0、RTX 4090、32 GB 内存（§5.1）。
- **统计检验**：单边配对 Wilcoxon signed-rank 检验（Table 4 的 P-value 列）。
- **数据采集**（§5.1）：良性 DoH 用 Chrome + WebDriver 自动访问 Majestic Million top-200；恶意流量用两台主机模拟 C2 服务端/受控端，会话 5 min，不支持 DoH 的工具（dns2tcp）经 dnsproxy 转发；采集历时两周，良性每轮约 8 h、恶意每轮约 10 h。

### 6.2 数据集

| 数据集 | 内容 | 用途 |
|---|---|---|
| CIRA-CIC-DoHBrw-2020 | 4 个国外公共 DoH resolver（AdGuard、Cloudflare、Google DNS、Quad9）的 DoH 流量 | 主实验（Exp. 1–4）基线数据 |
| 自采集扩展流量 | 新增 Qihoo-360（国产）、DNSPod（国产）、OpenDNS、Mullvad（ad-blocking）四个 resolver 的良性/恶意 DoH 隧道流量 | Exp. 5（Qihoo-360 目标域）、Exp. 6–9 |
| DoH-Tunnel-Traffic-HKD | 补充更多 DoH 隧道工具流量（dnstt、tcpover-dns、tuns 等未见工具） | 开集识别实验（§5.4.2） |

样本均衡策略：每个公共 resolver 采样 3000 条良性 DoH 流，每个隧道工具采样 1000 条恶意流；不足者全保留（§5.1）。工具集合：dns2tcp、dnscat2、iodine（已知类）+ dnstt、tcpover-dns、tuns（开集未知类）。

### 6.3 Baseline

共 9 个基线（§5.1）：域自适应 DSAN、DSAN-AT、DAN、DANN、CDANs；测试时自适应 T3A、Tent；DoH 检测深度学习框架 METC（序列化变体 METC-Seq）；作者前作 WEDoHTool。0% 标注场景下比较 T3A/Tent/METC-Seq/WEDoHTool；10%/20% 场景下比较 DA 系 + METC-Seq + WEDoHTool（§5.3）。所有基线（DSAN-AT 除外）统一使用与 AdaDoHTool 相同的 TLS 记录长度嵌入输入，以保证差异来自模型/自适应机制（§5.1）。

### 6.4 评价指标

Accuracy（式 (12)）、Recall（式 (13)）、开集场景的 K-Acc（已知类准确率）、U-Rec（未知类召回）、FUR（已知类被误拒为未知的比例，式 (14)）、Macro-F1（式 (15)）；效率指标为单样本推理时延（ms）与记忆库内存占用（GB）（§5.1、§5.4.2、§5.7）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| Exp. 1–5，0% 标注 | Avg Acc | 0.7125 ± 0.0171 | T3A 0.6863 ± 0.0070 | +2.62 个百分点 | 全部基线中最高的平均值；Exp. 2/3 上 T3A 略高（Table 4，§5.3） |
| Exp. 1–5，10% 标注 | Avg Acc | 0.8463 | DAN 0.7675（DA 最强）、METC-Seq 0.7427、WEDoHTool 0.7202 | vs WEDoHTool +17.51%、vs METC-Seq +13.95%、vs DAN +10.27%（相对提升口径） | 全部 5 组实验均为最优；Exp. 5 从 0.5825 提升到 0.6944（Table 5） |
| Exp. 1–5，20% 标注 | Avg Acc | 0.8323 | WEDoHTool 0.7529、METC-Seq 0.7532、DAN 0.7578 | 比 10% 设定略降（非单调） | 作者解释：更多标注未必覆盖目标域分布边界（Table 5、§5.3） |
| Exp. 6–9 额外未知 resolver，0% 标注 | Acc | 0.7723 / 0.6095 / 0.7304 / 0.6892 | T3A 0.7737（Exp. 6）/ Tent 0.6049（Exp. 7） | Exp. 6 与 T3A 持平稍低，其余三组领先 | DNSPod 组（Exp. 7）所有方法均显著退化（Table 6） |
| Exp. 6–9，10% 标注 | Acc | 0.8958 / 0.7426 / 0.8143 / 0.7887 | 各组次优为 CDANs 0.8140（Exp.6）、METC-Seq 0.6621 等 | 四组全为最优 | 源域加入 Qihoo-360 后 DNSPod 从 0.6095→0.6892（0%）、0.7426→0.7887（10%）（Table 6、§5.4.1） |
| 开集（未见工具） | K-Acc / U-Rec / FUR / Macro-F1 | 0.9337 / 0.6253 / 0.0658 / 0.8429 | WEDoHTool 0.8975 / 0.6598 / 0.1010 / 0.8101 | K-Acc +3.62 个百分点、FUR 最低、Macro-F1 最高 | WEDoHTool/Tent 的 U-Rec 更高但 FUR 更差（更激进拒识）（Table 7） |
| 效率（推理/内存） | ms / GB | 0.0054 ms、0.01095 GB | T3A 0.0177 ms（最快基线） | 时延为最快基线的 30.5% | 记忆库容量 30000（Table 9、§5.7） |

消融（0% 标注，Table 8）补充：完整模型 0.7125；w/o $L_{\mathrm{KNN}}$ 0.7088（−0.52%）；w/o memory update 0.5886（−17.39%）；w/o confidence threshold 0.6214（−12.79%）；w/o replacement 0.6357（−10.78%）；LRU 替换 0.6836（−4.06%）——**在线更新机制贡献最大**。

### 6.6 优势最明显的场景

"有少量目标域标注（10%）+ 目标 resolver 与源域不完全同分布"的场景：平均 0.8463、四组新增 resolver 全为最优（§5.3、§5.4.1）。其次是跨区域迁移（国外 resolver → 国产 resolver）：通过把 Qihoo-360 加入源域，DNSPod 目标域性能显著回升，提示**源域多样性是缓解跨区域漂移的有效手段**（Exp. 7 vs Exp. 9）。效率方面，0.0054 ms/样本的推理时延使其适合在线部署（§5.7）。

### 6.7 局限性

- Exp. 5（Qihoo-360，0% 标注）0.5825 略低于 WEDoHTool 0.5888：分布漂移最强时，高置信度更新反而可能引入不可靠伪标签（§5.3）。
- 20% 标注并不总优于 10%（0.8323 vs 0.8463），说明标注量收益存在饱和甚至反向（§5.3）。
- 伪标签污染、对抗/混淆鲁棒性、记忆库更新策略均被作者列为未来工作（§6）。
- 数据未公开（"available on request"），复现依赖自采流量与工具配置。
- 摘要报告的 7.41%/25.62% 提升幅度与正文表格口径不一致（详见 §2 提示与 JSON ingest_notes）。

---

## 7. 学习与应用

### 7.1 是否开源？

解析稿未给出代码仓库；数据可用性声明为 "Data will be made available on request"（§Data availability）。因此 frontmatter 的 `code` 记为 unknown。

### 7.2 复现关键步骤

1. 按 §5.1 的采集协议：Chrome+WebDriver 访问 top-200 网站产生良性 DoH；两台主机 + dnsproxy 模拟各隧道工具（每会话 5 min），按 resolver 分别归类。
2. 提取单向流并按 resolver IP 过滤；解析 TLS 记录，取应用数据记录长度序列的前 15 项、不足补零（§4.2.1、§5.1）。
3. 训练 Word2Vec(CBOW) 得到 64 维长度嵌入（§4.2.2、Table 2）。
4. TextCNN（窗口 3/4/5）在 $L_{\mathrm{KNN}}$（温度 0.1）下训练 5001 steps，同步初始化 feature–label 记忆库（容量 30000）（§4.3、Table 2）。
5. 测试时逐样本 KNN 投票（0% 标注 k=25；10%/20% 标注 k=200），置信阈值 0.75 以上样本 FIFO 写入记忆库（§4.4、§5.5）。
6. 以 leave-one-resolver-out 及新增 resolver 组（Exp. 6–9）评测，报告均值与 Wilcoxon 检验（§5.1、§5.4.1）。

### 7.3 关键超参数、预处理和训练细节

Table 2：输入序列长度 15；嵌入维度 64；卷积窗口高 3/4/5；最大池化高 13/12/11；dropout 0.5；优化器 SGD；batch 32；学习率 0.01；温度 0.1；记忆库容量 30000；$N_{\text{STEPS}}$ 5001；β=0.75（论文未解释 β 的含义，解析稿未见定义）；损失函数 $L_{\mathrm{KNN}}$。敏感性结论（§5.5）：0% 标注用 k=25 更好（伪标签噪声主导时小邻域更稳），10%/20% 标注用 k=200 更好；置信阈值 0.70–0.85 稳健、0.75 最优；记忆库容量 30000 最优（过大反而保留过期/噪声样本）。

### 7.4 能否迁移到其他任务？

可迁移性较强：**"冻结骨干 + 特征-标签记忆库 + 置信门控在线更新 + KNN 投票"是与骨干和任务解耦的 TTA 包装器**，可直接套用到其他存在部署期域漂移的流量任务（如跨环境网站指纹、跨网络条件的恶意流量检测、跨代理的隧道识别）。KNN-aware 损失也适用于任何"检索式推理"的表征学习场景。需要注意：当目标域漂移极端且无任何可靠证据时（§5.3 Exp. 5），该范式需与噪声防御机制（§6 讨论的方向）配合使用。

### 7.5 对我的研究有什么启发？

1. **评测协议价值**：把"resolver 多样性"显式建模为域划分（leave-one-resolver-out + 跨区域 + 特殊配置 resolver），比"随机划分"更接近部署现实——这一评测设计可迁移到 WF/隧道检测等任务的环境漂移评测。
2. **记忆库 vs 参数更新**：本文的消融（−17.39%）表明在流量任务里"更新决策参考集"可能比"更新参数"更稳、更便宜，这为资源受限的在网检测提供了轻量自适应路径。
3. **相对提升口径陷阱**：摘要 7.41%/25.62% 与正文 17.51%/13.95%/10.27% 无法对齐，提醒写综述引用数字时必须以表格口径为准（已记入 ingest_notes）。
4. **与库内其他自适应工作对照**：本库已有测试时训练方向的工作（如 NetTTT，JiOT 2026）与面向 RTT 漂移的 trace transduction 工作（CellShift，NDSS 2026），本文的"无参数记忆库"路线可作为第三条技术路线的对照点。

---

## 8. 总结

### 8.1 核心思想

> 冻结骨干，用在线记忆库 + KNN 投票适应新 resolver。

### 8.2 速记版 Pipeline

1. 按 resolver 分域采集 DoH 流量，提取单向流并解析 TLS 应用数据记录长度序列（前 15 项）。
2. Word2Vec(CBOW) 生成长度词嵌入矩阵。
3. TextCNN + KNN-aware loss 在源域训练，初始化特征-标签记忆库。
4. 推理时 KNN 相似度加权投票；置信度 ≥0.75 的样本入记忆库（FIFO 淘汰）。
5. 可选：以少量目标域标注（10%/20%）微调并同样入库，进一步对齐目标分布。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[tunnel-detection]]
- [[encrypted-traffic-analysis]]
- [[traffic-classification]]
- [[traffic-representation-learning]]

### 9.2 相关方法

- [[convolutional-network]]
- [[pre-training-finetuning]]

### 9.3 相关任务

- [[tunnel-detection]]
- [[traffic-classification]]

### 9.4 可更新的综述页面

- [[survey-encrypted-traffic-analysis]]

### 9.5 可加入的对比表

- [[method-comparison-table]]（新增测试时自适应类的 DoH 隧道工具识别方法）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 不同 resolver 的 TLS 应用数据记录长度分布可区分（如 Cloudflare/Google DNS 峰在 30–40 与 100–110 字节，Qihoo-360 多峰于 30–60/100/160/290） | 五个 resolver 的长度分布统计 | §5.2、Fig. 5 |
| 同一隧道工具（dnscat2）在不同 resolver 下的特征形成 domain-specific 聚类并部分重叠，说明 resolver 配置改变工具行为模式 | UMAP 可视化 | §5.2、Fig. 6 |
| 0% 标注下 AdaDoHTool 平均 0.7125 高于 T3A 0.6863 / Tent 0.6641 / METC-Seq 0.6640 / WEDoHTool 0.6390（Wilcoxon 显著） | Table 4 统计对比 | §5.3、Table 4 |
| 10% 标注下平均 0.8463，相对 WEDoHTool +17.51%、METC-Seq +13.95%、DAN +10.27% | Table 5 | §5.3、Table 5 |
| 移除记忆库在线更新后 0.7125→0.5886（−17.39%），为最大降幅的消融项 | Table 8 消融 | §5.6、Table 8 |
| k 的最优取值随标注量反转：0% 用 k=25、10%/20% 用 k=200；置信阈值 0.75 最优 | 参数敏感性分析 | §5.5、Fig. 7、Fig. 8 |
| 开集场景 K-Acc 0.9337、FUR 0.0658、Macro-F1 0.8429 均为最优；WEDoHTool U-Rec 0.6598 略高但 FUR 更差 | 开集实验 | §5.4.2、Table 7 |
| 推理 0.0054 ms/样本（T3A 的 30.5%），记忆库内存 0.01095 GB | 效率测量 | §5.7、Table 9 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-JCN-AdaDoHTool_A_test-time_adaptive_framework_for_identifying_DoH_tunneling_tools_with_unknown_resolvers.pdf
- MinerU Markdown：02-parsed-markdown/2026-JCN-AdaDoHTool_A_test-time_adaptive_framework_for_identifying_DoH_tunneling_tools_with_unknown_resolvers.md

---

## 12. 后续问题

- 摘要的 7.41% / 25.62% 提升幅度对应哪个基线、哪种口径？需查原文摘要或补充材料确认。
- β=0.75（Table 2）在正文中未定义，可能是 $L_{\mathrm{KNN}}$ 的某个权重或平衡系数，需查原公式。
- 记忆库中的伪标签错误率随时间如何演化？论文只给出最终准确率，缺少污染率-轮次的动态分析。
- 目标域样本是否需要按时间顺序到达（流式）？若可离线获得目标域全部样本，按批量初始化记忆库是否会更好？
- 特征维度 96（由 30000×(96×4+1×8) 反推）与 Table 2 的 embedding dim 64 不同源，具体结构（3 窗口 × 32 滤波）需核对原文图 3。

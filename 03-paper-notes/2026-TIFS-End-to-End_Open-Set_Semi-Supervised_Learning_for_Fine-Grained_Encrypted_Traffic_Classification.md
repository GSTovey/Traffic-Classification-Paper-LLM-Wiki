---
type: paper
title_original: "End-to-End Open-Set Semi-Supervised Learning for Fine-Grained Encrypted Traffic Classification"
title_cn: "基于开放集半监督学习的端到端细粒度加密流量分类"
authors: ["Qian Yang", "Wenxuan He", "Minghao Chen", "Hongyu Du", "Sisi Shao", "Fei Wu", "Shangdong Liu", "Yimu Ji", "Kui Ren"]
year: 2026
venue: "IEEE Transactions on Information Forensics and Security (TIFS)"
doi: "10.1109/TIFS.2026.3653575"
url: unknown
pdf: "00-inbox/PDFs/2026-TIFS-End-to-End_Open-Set_Semi-Supervised_Learning_for_Fine-Grained_Encrypted_Traffic_Classification.pdf"
mineru_md: "02-parsed-markdown/2026-TIFS-End-to-End_Open-Set_Semi-Supervised_Learning_for_Fine-Grained_Encrypted_Traffic_Classification.md"
status: processed
reading_level: L2
research_area: ["encrypted traffic classification", "network security", "open-set recognition"]
task: ["open-set traffic classification", "unknown traffic detection", "unknown class clustering", "fine-grained classification"]
method: ["energy-based model", "vision transformer", "graph neural network", "TAGCN", "adaptive deep clustering", "dual-branch feature extraction", "Weibull distribution"]
dataset: ["USTC-TFC-2016", "CIC-IDS-2018", "ISCX-Tor-2016"]
code: unknown
relevance: high
created: "2026-05-27"
updated: "2026-05-27"
---

# End-to-End Open-Set Semi-Supervised Learning for Fine-Grained Encrypted Traffic Classification

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | End-to-End Open-Set Semi-Supervised Learning for Fine-Grained Encrypted Traffic Classification |
| 中文标题 | 基于开放集半监督学习的端到端细粒度加密流量分类 |
| 作者 | Qian Yang, Wenxuan He, Minghao Chen, Hongyu Du, Sisi Shao, Fei Wu, Shangdong Liu, Yimu Ji, Kui Ren |
| 年份 | 2026 |
| 会议/期刊 | IEEE Transactions on Information Forensics and Security (TIFS) |
| 研究方向 | 加密流量分类、开放集识别、网络安全 |
| 任务类型 | 开放世界场景下的加密流量细粒度分类，包括已知类分类、未知类检测与聚类 |
| 方法关键词 | energy-based model, dual-branch feature extraction, CViT (Convolution-enhanced ViT), TAGCN, adaptive deep clustering, Weibull distribution, end-to-end joint training |
| 数据集 | USTC-TFC-2016（20类，10恶意+10良性）、CIC-IDS-2018（7类，含多种攻击）、ISCX-Tor-2016（16类Tor应用） |
| 是否开源 | 否 |
| PDF | 00-inbox/PDFs/2026-TIFS-End-to-End_Open-Set_Semi-Supervised_Learning_for_Fine-Grained_Encrypted_Traffic_Classification.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-TIFS-End-to-End_Open-Set_Semi-Supervised_Learning_for_Fine-Grained_Encrypted_Traffic_Classification.md |

## 1. 一句话总结

> 提出 FEC-OSL 方法，通过双分支流特征提取（CViT + TAGCN）、基于能量模型的已知/未知类边界学习、以及自适应深度聚类，在开放世界场景下实现端到端的加密流量细粒度分类，在三个真实数据集上全面超越现有方法。

## 2. 摘要翻译

### 2.1 摘要原文

Encrypted traffic classification is crucial for enhancing network management, service quality, and security. However, real-world network environments are inherently open-world scenarios in which traffic not only consists of known classes but also includes the continuous emergence of unknown classes. Existing deep learning methods typically rely on the closed-world assumption, which significantly limits their classification performance when dealing with unknown traffic types. This limitation makes it challenging to accurately classify known traffic classes and effectively identify unknown ones. Although few studies have focused on open-world scenarios, these methods often use staged strategies and struggle to reliably detect unknown traffic or to estimate novel classes. To address these challenges, we propose an end-to-end Fine-grained Encrypted traffic Classification method based on Open-set Semi-supervised Learning, called FEC-OSL. This method comprises three mutually reinforcing core components. First, we design a dual-branch flow feature extraction module to capture detailed and discriminative flow features. Second, we introduce a novel energy-based perspective that leverages energy-boundary learning to distinguish known traffic from unknown traffic, enabling precise detection of known classes. Finally, an adaptive deep clustering approach integrates feature learning with clustering to achieve fine-grained classification of unknown flows. We conduct extensive experiments on three real-world datasets, and the results validate that our proposed method exhibits outstanding performance in handling both known and unknown encrypted traffic in open-world scenarios.

### 2.2 摘要中文翻译

加密流量分类对于提升网络管理效率、服务质量和安全性至关重要。然而，现实网络环境本质上是开放世界场景，流量不仅包含已知类别，还不断涌现出未知类别。现有的深度学习方法通常依赖封闭世界假设，这极大地限制了其在处理未知流量类型时的分类性能。虽然已有少数研究关注开放世界场景，但这些方法通常采用分阶段策略，难以可靠地检测未知流量或估计新类别。为解决这些挑战，我们提出了一种基于开放集半监督学习的端到端细粒度加密流量分类方法 FEC-OSL。该方法包含三个相互增强的核心组件：首先，设计双分支流特征提取模块以捕获详细且具有区分性的流特征；其次，引入基于能量模型的新视角，利用能量边界学习区分已知流量和未知流量，实现已知类的精确检测；最后，采用自适应深度聚类方法将特征学习与聚类集成，实现未知流的细粒度分类。在三个真实数据集上的大量实验验证了该方法在开放世界场景下处理已知和未知加密流量的出色性能。

## 3. 方法动机

### 3.1 什么是 Open-Set Classification？为什么它对加密流量至关重要？

**Open-set classification（开放集分类）** 与传统 closed-set classification（封闭集分类）的根本区别在于：封闭集假设测试样本的所有类别在训练阶段均已出现，模型只需在已知类别中做选择；而开放集假设测试阶段可能出现训练中从未见过的未知类别，模型必须同时完成"已知类分类"和"未知类识别"两个任务。

**封闭世界假设在真实网络中必然失败的原因**：
- **应用生态的动态性**：新的应用程序、协议版本和恶意软件变种不断涌现。据 Zscaler 2023 报告，约 85.9% 的网络威胁通过加密通道传输，攻击者持续更新工具和策略以规避检测
- **类别空间的开放性**：真实网络流量的类别空间是无限的。训练数据永远无法覆盖所有可能的流量类型。论文定义了三类数据集：已知类 $\mathcal{D}_k$（训练时有标签）、辅助未知类 $\mathcal{D}_{au}$（训练时无标签）、全新未知类 $\mathcal{D}_{nu}$（仅在测试时出现），三者的标签空间严格不相交
- **闭集模型的"虚假高置信度"问题**：softmax 分类器将所有输入强制归入预定义类别，即使面对从未见过的流量，也会给出看似确定的分类结果。论文通过可视化实验证实（Fig. 11a），softmax 的已知类和未知类置信度分数在 0.8-1.0 区间存在大量重叠，根本无法可靠区分

**Open-set 与 Semi-supervised Learning 结合的意义**：
- 半监督学习利用少量有标签数据和大量无标签数据进行训练，天然适合开放世界场景——因为未知流量在训练阶段就是"无标签"的
- 将开放集识别与半监督学习结合，使模型能够：(1) 利用无标签的辅助未知类数据学习能量边界，区分已知与未知；(2) 通过自适应深度聚类为未知流生成伪标签，实现细粒度分类；(3) 端到端联合训练让三个任务（分类、检测、聚类）相互增强
- 传统的多阶段方法（如 CVAE-EVT 先训练分类器，再用极值理论检测未知类）各阶段独立训练，存在错误传播；端到端方法让特征提取与分类/聚类同步优化，避免了这一问题

### 3.2 现有方法的痛点和不足

| 现有方法 | 痛点 |
|---|---|
| 基于 softmax 的闭集分类方法 | 依赖封闭世界假设，对未知类产生虚假高置信度预测，无法处理开放世界场景 |
| DPI / payload 分析 | 对加密流量完全无效，无法直接访问 packet payload |
| CVAE-EVT（多阶段检测框架） | 各阶段需分别训练，增加复杂度，存在阶段间错误传播 |
| ECNet（多视图特征+置信度机制） | 在高开放度场景下性能下降明显 |
| Trident 系列（AE/RNN/GNN） | 不同变体在不同数据集上表现不稳定，缺乏泛化能力 |
| 基于重建误差的方法 | 对重建误差敏感，整体 OSR 效果受限 |
| 基于分类器置信度的方法 | 高置信度的未知样本仍可能被误分类 |
| 手动/离线聚类方法 | 严重依赖专家知识，需要人工参数调优 |

### 3.3 论文的研究假设或核心直觉

- **核心假设**：开放世界加密流量分类需要同时解决三个子任务——已知类分类、未知类检测、未知类聚类，且这三个任务可以通过端到端联合训练相互增强
- **关键直觉 1**：基于能量模型（EBM）比 softmax 更能捕获已知类和未知类之间的全局分布差异，通过能量边界学习可以在能量空间中形成清晰的已知/未知分界
- **关键直觉 2**：字节级特征和流交互特征具有互补性——字节级特征关注细粒度的结构模式，交互特征关注通信行为模式，融合二者可获得更具区分性的表征
- **关键直觉 3**：将特征学习与聚类过程集成，通过迭代优化特征表征和伪标签分配，可以逐步揭示未知流中的细粒度类别

## 4. 方法设计

### 4.1 方法整体流程

1. **数据预处理**：将原始 pcap 数据分割为独立的 biflow，移除以太网头，匿名化 IP 地址和端口号
2. **双分支特征提取**：字节级分支（CViT）提取 header 和 payload 的字节矩阵特征；交互分支（TAGCN）提取流交互图特征；两分支特征融合
3. **能量模型分类**：将融合特征映射为能量值，已知类低能量、未知类高能量，用 Weibull 分布建模能量边界
4. **自适应深度聚类**：对未知流进行特征学习与聚类的迭代优化，逐步精细化伪标签
5. **端到端联合训练**：三个模块通过统一损失函数联合优化
6. **测试时增量更新**：识别可信的新未知流，合并到辅助未知集进行周期性重训练

### 4.2 详细 Pipeline（表格形式）

| 步骤 | 描述 | 技术细节 |
|---|---|---|
| 1. 数据预处理 | 将 pcap 分割为 biflow，匿名化处理 | 使用 Splitcap 工具，移除以太网头，匿名化 IP 和端口 |
| 2. 字节矩阵重塑 | 选取前 M=5 个包，header 和 payload 分别重塑为矩阵 | header 矩阵 x_h ∈ R^(M*m_h^r) x m_h^c，payload 矩阵 x_p ∈ R^(M*m_p^r) x m_p^c |
| 3. CViT 特征提取 | 对字节矩阵做 patch 划分，卷积提取局部特征，Transformer 编码全局特征 | P x P patches，卷积核 θ，L 层 Transformer encoder，全局池化得到 z_h 和 z_p |
| 4. 流交互图构建 | 以包为节点，burst 为连接依据构建图 | 7 维节点特征（方向、长度、时间戳、burst 包数/字节数、burst 间比率），intra-burst 和 inter-burst 边 |
| 5. TAGCN 图卷积 | 对流交互图做拓扑自适应图卷积 | K 阶多项式图滤波器，可学习系数 w，L' 层图卷积 |
| 6. 特征融合 | 字节特征 h_b 和交互特征 h_g 拼接 | h = [h_b, h_g]，形成综合流表征 |
| 7. 能量模型分类 | 用分类器 g(h) 映射到 C_k+1 logits，计算自由能量 E(h;g) | E(h;g) = -T * log(sum(exp(g_j(h)/T)))，与阈值 τ 比较 |
| 8. 自适应深度聚类 | CNN 精炼特征，初始化伪标签，迭代更新特征和聚类中心 | 动量更新公式 F_β(x)，最近聚类中心重分配伪标签 |
| 9. 联合训练 | 交替优化分类和聚类模块 | L_total = L_1 + L_2，L_1 含交叉熵和能量边界正则化 |
| 10. 测试时更新 | 识别可信新未知流，合并到辅助未知集 | Weibull 分布尾部（p<0.01）+ 特征距离 top 5% + 高密度聚类 |

### 4.3 模型结构或系统模块（表格形式）

| 模块 | 功能 | 输入 | 输出 |
|---|---|---|---|
| 字节级流特征提取（BFE） | 从原始字节数据中提取细粒度特征 | pcap 数据的 header 和 payload 字节矩阵 | 字节级特征 h_b = [z_h, z_p] |
| 流交互特征提取（FIE） | 从包交互模式中提取通信行为特征 | 流交互图 G = (V, E) | 图级特征 h_g |
| 能量模型分类模块 | 区分已知类和未知类流量 | 融合特征 h | 能量值 E(h;g) 和分类结果 |
| 自适应深度聚类模块 | 对未知流进行细粒度聚类 | 辅助未知流特征 | 伪标签和聚类结果 |
| 端到端训练框架 | 联合优化所有模块 | 所有训练数据 | 训练好的模型 M |

### 4.4 公式、算法和机制解释

**CViT 字节级特征提取**：

卷积操作提取局部特征：
$$c_{h,i} = \text{Conv}(\tilde{x}_{h,i}; \theta)$$

嵌入与位置编码：
$$z_h^{(0)} = [c_{h,1}E_{\text{emb}}; c_{h,2}E_{\text{emb}}; \dots; c_{h,N_p}E_{\text{emb}}] + E_{\text{pos}}$$

Transformer 编码器第 l 层：
$$\bar{z}_h^{(l)} = \text{MHA}(\text{LN}(z_h^{(l-1)})) + z_h^{(l-1)}$$
$$z_h^{(l)} = \text{FFN}(\text{LN}(\bar{z}_h^{(l)})) + \bar{z}_h^{(l)}$$

**TAGCN 图卷积**：

图滤波器定义（K 阶多项式）：
$$G_{d,f}^{(l')} = \sum_{k=1}^{K} w_{d,f,k}^{(l')} \mathcal{A}^k$$

节点特征更新：
$$h_{i,f}^{(l')} = \sum_{k=1}^{K} \sum_{d=1}^{D} w_{d,f,k}^{(l')} \mathcal{A}^k \hat{a}_d + b_f$$

**能量函数**：

自由能量（Helmholtz free energy）：
$$E(h) = -T \log \int_{y'} \exp(-E(h, y')/T)$$

与判别分类器的关联：
$$E(h; g) = -T \log\left(\sum_{j=1}^{C_k+1} \exp(g_{y_j}(h)/T)\right)$$

**总损失函数**：

$$\mathcal{L}_1 = \mathbb{E}_{(h,y) \sim \mathcal{H}^{\text{train}}}[-\log \mathcal{P}(y|h)] + \lambda \mathcal{L}_{\text{energy}}$$

能量边界正则化损失：
$$\mathcal{L}_{\text{energy}} = \mathbb{E}_{(h,y) \sim \mathcal{H}_k}(\max(0, E(h) - m_k))^2 + \mathbb{E}_{(h,y) \sim \mathcal{H}_{au}}(\max(0, m_{au} - E(h)))^2$$

聚类损失：
$$\mathcal{L}_2 = \mathbb{E}_{(x, \tilde{y}) \sim \mathcal{D}_{au}}[\text{CE}(g'(\psi_\theta(x), \tilde{y}))]$$

总损失：
$$\mathcal{L}_{\text{total}} = \mathcal{L}_1 + \mathcal{L}_2$$

**推理阶段分类规则**：

$$r = \begin{cases} \arg\min_{y \in \mathcal{Y}_k} E(h, y), & \text{if } -E(h; g) \geq \tau \\ U, & \text{otherwise} \end{cases}$$

**动量更新公式**：

$$F_\beta(x) \leftarrow \beta \cdot \frac{\psi_\theta(x_u)}{\|\psi_\theta(x)\|_2} + (1-\beta) \cdot F_\beta(x)$$

**伪标签重分配**：

$$\tilde{y}' = \arg\min_{\tilde{y} \in \{1, \dots, C_{au}\}} \|F_\beta(x) - c_{\tilde{y}}\|_2^2$$

**关键机制解释**：

- **能量边界学习**：通过 m_k 和 m_{au} 两个边界参数，强制已知类能量低于 m_k，辅助未知类能量高于 m_{au}，在能量空间中形成清晰分界
- **Weibull 分布建模**：用 Weibull 分布拟合已知类的负能量分布，通过分位数确定阈值 τ，实现自适应的已知/未知判定
- **端到端联合训练**：分类模块引导已知类特征趋向低能区、未知类特征趋向高能区；聚类模块细化伪标签，增强类内紧凑性；二者协同优化特征空间
- **增量更新机制**：测试时识别可信新未知流（Weibull 尾部 p<0.01 + 特征距离 top 5% + 高密度聚类），合并到辅助集进行周期性重训练

### 4.5 方法优势

1. **端到端统一框架**：三个模块（特征提取、能量分类、深度聚类）通过统一损失函数联合训练，避免了分阶段方法的错误传播问题
2. **双分支互补特征**：字节级特征（CViT）捕获细粒度结构模式，交互特征（TAGCN）捕获通信行为模式，二者互补提供更全面的流表征
3. **能量模型优于 softmax**：通过全局建模避免 softmax 对未知类的虚假高置信度预测，在已知/未知区分上表现更优
4. **自适应聚类未知类**：将特征学习与聚类集成，通过迭代优化逐步精细化未知流的类别划分
5. **概念漂移鲁棒性**：在概念漂移场景下仍能维持接近 90% 的 F1 score，表明方法具有良好的泛化能力
6. **高开放度场景稳健**：在已知/未知比为 4:16 的高开放度下，AUC 仍维持在 97.5%，远优于 baseline

### 4.6 关键机制深度分析

**能量模型 vs Softmax 的本质区别**：

Softmax 输出 $P(y|h) = \exp(g_y(h)/T) / \sum_j \exp(g_j(h)/T)$ 仅依赖 logits 的相对大小。如果一个未知样本的特征恰好使得某个已知类的 logit 值很高，softmax 会给出高置信度预测。论文的消融实验（Table IV）证实了这一点：将 EBM 替换为 softmax 后，已知/未知区分 AUC 从 99.13% 骤降至 89.65%。

EBM 的自由能量 $E(h;g) = -T \log(\sum_{j=1}^{C_k+1} \exp(g_{y_j}(h)/T))$ 是对所有类别的全局聚合。它不是在做"哪个类最像"的相对比较，而是在衡量"这个样本与整个已知类别体系的兼容程度"。未知样本即使在某个维度上与某已知类相似，由于其整体特征分布与已知类不匹配，能量值仍然会偏高。

**能量边界正则化的具体机制**：
- $m_k = -10$ 是已知类能量的上界：训练时强制已知类样本的能量 $E(h) < -10$
- $m_{au} = -5$ 是辅助未知类能量的下界：训练时强制辅助未知类样本的能量 $E(h) > -5$
- 两者之间形成宽度为 5 的"能量无人区"，任何落在该区域的样本都会被明确判定
- 论文通过网格搜索发现 $|m_{au} - m_k| \in [5, 7]$ 时 AUC 最优，最终选择 $m_k = -10, m_{au} = -5$

**Weibull 分布阈值选择**：
- 对已知类样本的负能量值 $-E(h;g)$ 拟合 Weibull 分布
- 取分布的分位数作为阈值 $\tau$：USTC-TFC 和 CIC-IDS 取 0.05 分位数，ISCX-Tor 取 0.1 分位数
- 分位数选择的敏感性分析（Fig. 12d）：0.1-0.5 分位数范围内 F1 和 AUC 均接近 100%，但 0.9 分位数时 F1 骤降至 42%、AUC 降至 65%，说明过高的阈值会将大量已知类误判为未知类

**自适应深度聚类的迭代优化过程**：
1. **初始化阶段**：用聚类算法（如 K-means）对辅助未知类特征分配初始伪标签 $\tilde{y}$
2. **特征精炼**：用 CNN 网络 $\psi_\theta(\cdot)$ 对 EBM 输出的特征进行二次精炼，消除 EBM 将未知流错误映射到第 $(C_k+1)$ 类带来的特征偏差
3. **伪标签训练**：用交叉熵损失 $\mathcal{L}_2$ 更新 $\psi_\theta$ 的参数
4. **动量更新样本库**：$F_\beta(x) \leftarrow \beta \cdot \psi_\theta(x)/\|\psi_\theta(x)\|_2 + (1-\beta) \cdot F_\beta(x)$，确保特征平滑过渡
5. **伪标签重分配**：根据更新后的特征，将每个样本重新分配到最近的聚类中心
6. **迭代重复**步骤 3-5，特征表征和伪标签逐步精细化

**端到端联合训练的协同效应**：
- 分类模块 $\mathcal{L}_1$ 引导已知类特征趋向低能区、未知类特征趋向高能区，减小已知类的类内方差
- 聚类模块 $\mathcal{L}_2$ 细化未知流的伪标签，增强未知类的类内紧凑性
- 两个模块共享双分支特征提取器，分类任务的学习信号帮助特征提取器捕获更具区分性的模式，聚类任务的学习信号帮助特征提取器发现未知流中的细粒度结构
- 交替优化而非同时优化，避免两个目标函数的梯度冲突

### 4.7 方法不足

1. **依赖前 30 个包**：字节级特征仅使用前 M=5 个包（每包取前若干字节），可能无法捕获后期阶段的攻击行为
2. **计算开销**：双分支特征提取和聚类过程引入额外计算开销，可能限制在低延迟或资源受限环境中的应用
3. **辅助未知类依赖**：训练需要辅助未知类数据，如果辅助未知类与测试中的新未知类差异过大，聚类效果可能下降
4. **固定维度限制**：字节矩阵和交互图使用固定维度，对于长度差异较大的流可能造成信息损失
5. **聚类数量敏感**：初始聚类数需设置为大于潜在真实未知类数，设置不当可能影响聚类效果
6. **批量大小和 epoch 选择**：使用 batch size 64 和 50 epochs，在大规模数据集上的训练效率有待验证

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 对比维度 | 传统闭集方法 | 多阶段 OSR 方法 | FEC-OSL (本文) |
|---|---|---|---|
| 世界假设 | 封闭世界 | 开放世界 | 开放世界 |
| 训练方式 | 端到端 | 多阶段分别训练 | 端到端联合训练 |
| 未知类处理 | 不支持 | 检测但不聚类 | 检测 + 聚类 |
| 分类器 | softmax | 各种（autoencoder/EVT 等） | 能量模型（EBM） |
| 特征提取 | 单一视角 | 通常单一视角 | 双分支（字节+交互） |
| 概念漂移适应 | 无 | 有限 | 增量更新机制 |

**与闭集方法的对比**：
- ET-BERT（闭集 SOTA）仅依赖 packet payload 的 Transformer 特征，在封闭集上 F1 达 98.43%，但完全不支持开放集场景。FEC-OSL 通过引入能量模型和聚类模块，在封闭集上 F1 达 99.59%（提升 1.16%），同时支持开放集分类
- GraphDApp 仅使用交互图特征（F1 82.43%），DeepPacket 仅使用 1D-CNN payload 特征（F1 91.20%），说明单一视角特征的局限性
- FlowPrint 作为半监督方法，利用无标签数据进行应用指纹提取，但不支持未知类检测

**与开放集方法的对比**：
- CVAE-EVT 采用"先训练 CVAE 学习已知类分布，再用 EVT 拟合尾部分布检测未知类"的两阶段策略。各阶段独立训练，存在特征不一致和错误传播问题。在高开放度（4:16）场景下 AUC 降至 ~79.5%
- ECNet 使用多视图特征和置信度机制检测未知类，但不支持未知类聚类（CVAE-EVT 也不支持）。在高开放度下 AUC 降至 ~85.5%
- Trident 系列（AE/RNN/GNN）是唯一支持未知类聚类的 baseline，但三种变体在不同数据集上表现差异大：Trident(RNN) 在 CIC-IDS-2018 上 F1 达 99.57%，但在 USTC-TFC-2016 上仅 89.64%；Trident(AE) 在 ISCX-Tor-2016 上 F1 仅 89.01%

**FEC-OSL 的综合优势**：三合一——同时具备开放集识别、端到端训练、未知类聚类能力，在所有数据集和所有开放度设置下均取得最优或接近最优的结果

### 5.2 创新点分析（表格形式）

| 创新点 | 说明 |
|---|---|
| 端到端开放集半监督学习框架 | 首次将特征提取、已知/未知分类、未知类聚类三个任务统一在端到端框架中，通过联合训练相互增强 |
| 双分支流特征提取模块 | CViT（卷积增强 ViT）提取字节级特征 + TAGCN 提取流交互特征，两个互补视角提供全面的流表征 |
| 能量模型用于已知/未知分类 | 引入能量边界学习，通过 Weibull 分布建模能量分布，比 softmax 更可靠地区分已知和未知类 |
| 自适应深度聚类 | 将特征学习与聚类集成，通过动量更新和伪标签重分配迭代优化未知流的细粒度分类 |
| 增量更新机制 | 测试时识别可信新未知流并合并到辅助集，增强模型对新兴未知流量的适应能力 |

### 5.3 适用场景

- 网络入侵检测系统（IDS）：在开放世界环境中同时检测已知攻击类型和新型未知攻击
- 恶意软件流量识别：识别已知恶意软件流量并发现新型恶意软件的加密通信
- 加密流量管理：对加密应用流量进行细粒度分类，支持 QoS 策略制定
- 安全威胁情报扩展：通过未知类聚类发现新型攻击模式，扩展攻击知识库
- 持续演进的网络安全监控：通过增量更新机制适应不断变化的网络威胁态势

### 5.4 方法对比表

| 方法 | 开放集 | 端到端 | 已知分类 | 未知检测 | 未知聚类 | 特征类型 | USTC-TFC AC |
|---|---|---|---|---|---|---|---|
| GraphDApp | 否 | 否 | 是 | 否 | 否 | 图（交互） | 87.89% |
| DeepPacket | 否 | 是 | 是 | 否 | 否 | 1D-CNN（payload） | 91.38% |
| PERT | 否 | 是 | 是 | 否 | 否 | Transformer（payload） | 95.90% |
| ET-BERT | 否 | 是 | 是 | 否 | 否 | Transformer（datagram） | 98.04% |
| Kitsune | 否 | 是 | 是 | 否 | 否 | Autoencoder（统计） | 86.75% |
| FlowPrint | 否 | 否 | 是 | 否 | 否 | 半监督（指纹） | 81.46% |
| CVAE-EVT | 是 | 否 | 是 | 是 | 否 | CVAE + EVT | 97.32% |
| ECNet | 是 | 否 | 是 | 是 | 否 | 多视图 + 置信度 | 98.21% |
| Trident (AE/RNN/GNN) | 是 | 否 | 是 | 是 | 是 | AE/RNN/GNN | 95.65/92.38/94.32% |
| **FEC-OSL (本文)** | **是** | **是** | **是** | **是** | **是** | **双分支（字节+交互）** | **99.60%** |

**将开放集 + 半监督 + 端到端三者结合的价值**：
- **纯开放集方法**（CVAE-EVT, ECNet）：能检测未知类，但不聚类，无法为安全分析师提供未知流量的结构化信息
- **纯半监督方法**（FlowPrint）：利用无标签数据，但不处理未知类，无法应对开放世界场景
- **纯端到端方法**（ET-BERT）：训练高效，但假设封闭世界，无法泛化到未知类
- **FEC-OSL 的三合一设计**：利用半监督学习的思想将无标签的辅助未知类纳入训练，通过能量模型实现开放集识别，通过端到端联合训练让三个模块协同优化。这使得模型在封闭集上也优于纯闭集方法（因为未知类的参与帮助模型学习了更具区分性的特征边界），在开放集上大幅领先纯开放集方法

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **实验环境**：Python 3.8.19, PyTorch 1.8.1, NVIDIA GeForce RTX 3090 GPU
- **优化器**：SGD
- **学习率**：双分支特征提取和已知/未知分类模块 0.0001，聚类模块 0.001
- **训练轮次**：50 epochs，batch size 64
- **封闭世界评估**：所有类已知，与 9 个 baseline 对比
- **开放集评估**：多种已知/未知类比例设置，评估 AUC、F1、AMI 三个指标
- **概念漂移评估**：重组 CIC-IDS-2018 训练/测试集，模拟真实漂移场景
- **消融实验**：分别移除 BFE、header、payload、FIE 模块，以及替换 EBM 为 softmax

### 6.2 数据集

| 数据集 | 类别数 | 类型 | 用途 |
|---|---|---|---|
| USTC-TFC-2016 | 20 | 10 恶意 + 10 良性 | 加密恶意流量分类 |
| CIC-IDS-2018 | 7 | 正常流量 + 6 类攻击（暴力破解、Botnet、DoS 等） | 入侵检测基准 |
| ISCX-Tor-2016 | 16 | Tor 加密应用流量（邮件、聊天、FTP 等） | Tor 流量分类 |

开放集评估中已知/未知类比例设置：
- USTC-TFC-2016: N_k:N_u = {16:4, 12:8, 8:12, 4:16}
- CIC-IDS-2018: N_k:N_u = {5:2, 4:3, 3:4, 2:5}
- ISCX-Tor-2016: N_k:N_u = {6:2, 4:4, 2:6}

### 6.3 Baseline

**封闭集方法**：
- 监督方法：GraphDApp（图神经网络）、DeepPacket（1D-CNN）、PERT（Transformer）、ET-BERT（预训练 Transformer）
- 无监督方法：Kitsune（autoencoder 集成）
- 半监督方法：FlowPrint（半监督指纹）

**开放集方法**：
- CVAE-EVT（条件 VAE + 极值理论，多阶段）
- ECNet（多视图特征 + 置信度机制）
- Trident（三种变体：AE、RNN、GNN，支持未知类聚类）

### 6.4 评价指标

- **封闭集**：Accuracy (AC), Precision (PR), Recall (RC), F1 score
- **已知/未知区分**：AUC (ROC 曲线下面积)
- **已知类分类**：F1 score
- **未知类聚类**：AMI (Adjusted Mutual Information)

### 6.5 关键实验结果（表格形式）

**封闭集分类结果（Table I）**：

| 方法 | USTC-TFC AC | USTC-TFC F1 | CIC-IDS AC | CIC-IDS F1 | ISCX-Tor AC | ISCX-Tor F1 |
|---|---|---|---|---|---|---|
| ET-BERT | 98.04% | 98.43% | 99.43% | 99.43% | 98.35% | 98.64% |
| ECNet | 98.21% | 97.18% | 98.12% | 98.45% | 98.10% | 98.09% |
| CVAE-EVT | 97.32% | 97.06% | 97.94% | 97.01% | 98.06% | 97.60% |
| Trident (RNN) | 92.38% | 89.64% | 99.93% | 99.57% | 99.38% | 97.02% |
| **FEC-OSL** | **99.60%** | **99.59%** | **99.86%** | **99.85%** | **99.75%** | **99.74%** |

**开放集结果（USTC-TFC-2016, 已知/未知比 16:4）**：

| 方法 | AUC | F1 (已知类) | AMI (未知类聚类) |
|---|---|---|---|
| CVAE-EVT | ~91% | - | 不支持 |
| ECNet | ~97% | - | 不支持 |
| Trident (AE) | ~93.5% | - | ~78.5% |
| **FEC-OSL** | **99.13%** | **99.00%** | **83.43%** |

**高开放度场景（USTC-TFC-2016, 4:16）**：

| 方法 | AUC |
|---|---|
| CVAE-EVT | ~79.5% |
| ECNet | ~85.5% |
| Trident 系列 | ~78-80% |
| **FEC-OSL** | **~97.5%** |

**概念漂移评估（CIC-IDS-2018-new）**：

| 指标 | 无漂移 (CIC-IDS-2018) | 有漂移 (CIC-IDS-2018-new) |
|---|---|---|
| AC | 99.86% | 91.00% |
| PR | 99.85% | 93.27% |
| RC | 99.86% | 90.74% |
| F1 | 99.85% | 89.96% |

**消融实验详细数据（Table III, 封闭集 USTC-TFC-2016）**：

| 配置 | AC | PR | RC | F1 | F1 变化 |
|---|---|---|---|---|---|
| FEC-OSL (完整) | 99.60% | 99.61% | 99.59% | 99.59% | - |
| w/o BFE | 97.71% | 97.90% | 97.84% | 97.79% | -1.80% |
| w/o header | 97.69% | 97.16% | 96.87% | 96.98% | -2.61% |
| w/o payload | 98.12% | 98.13% | 98.08% | 98.07% | -1.52% |
| w/o FIE | 97.14% | 97.42% | 97.33% | 97.30% | -2.29% |

**消融实验详细数据（Table IV, 开放集 USTC-TFC-2016, 16:4）**：

| 配置 | Kn/Unk AUC | Kn F1 | Unk AMI |
|---|---|---|---|
| FEC-OSL (完整) | 99.13% | 99.00% | 83.43% |
| w/o BFE | 86.42% | 91.11% | 73.39% |
| w/o header | 85.59% | 91.96% | 72.74% |
| w/o payload | 92.78% | 96.58% | 76.63% |
| w/o FIE | 80.35% | 90.72% | 71.59% |
| w/ Softmax | 89.65% | 96.48% | 77.82% |

**跨数据集开放集 AUC 趋势（已知/未知比变化时）**：

| 数据集 | 比例 | FEC-OSL | CVAE-EVT | ECNet | 最佳 Trident |
|---|---|---|---|---|---|
| USTC-TFC | 16:4 | 99.0% | 91.0% | 97.0% | 93.5% (AE) |
| USTC-TFC | 4:16 | 97.5% | 79.5% | 85.5% | 79.0% (RNN) |
| CIC-IDS | 5:2 | 98.0% | 91.0% | 95.0% | 96.0% (AE) |
| CIC-IDS | 2:5 | 94.0% | 83.0% | 90.0% | 90.0% (AE/RNN) |
| ISCX-Tor | 6:2 | 98.0% | 92.0% | 95.0% | 95.0% (RNN/GNN) |
| ISCX-Tor | 2:6 | 95.0% | 87.0% | 88.0% | 90.0% (RNN) |

### 6.6 优势最明显的场景

- **高开放度环境**：在已知/未知比为 4:16 的极端场景下，FEC-OSL 的 AUC 仍维持在 97.5%，而 baseline 方法普遍降至 80% 左右
- **封闭集分类**：在三个数据集上均取得最优 AC 和 F1，相比最强 baseline ET-BERT 分别提升 1.56%/0.43%/1.4%（AC）和 1.16%/0.42%/1.1%（F1）
- **未知类聚类**：AMI 在所有比例设置下均优于 Trident 系列，说明自适应深度聚类模块有效
- **概念漂移场景**：F1 仍接近 90%，表明方法具有良好的泛化能力
- **特征可解释性**：attention 热图显示模型能学习到不同流量类型的结构差异（如 Weibo 关注 TCP window size，Zeus 关注 TCP flags 和 SYN options）

### 6.7 局限性

1. **前期包依赖**：仅使用前 5 个包的字节特征，可能遗漏后期阶段的攻击行为特征
2. **计算开销**：双分支特征提取（CViT + TAGCN）和聚类迭代引入额外计算负担
3. **辅助未知类需求**：训练阶段需要辅助未知类数据，如果辅助类与测试新未知类分布差异大，效果可能下降
4. **概念漂移后性能下降**：从 99.85% 降至 89.96%（F1），说明对严重漂移仍有一定脆弱性
5. **聚类初始化依赖**：初始聚类数需预设为大于真实未知类数，不当设置可能影响效果
6. **数据集规模限制**：实验仅在三个中等规模数据集上验证，大规模真实网络环境中的表现有待验证

## 7. 学习与应用

### 7.1 是否开源？

否。论文未提供代码或开源实现。

### 7.2 复现关键步骤

1. **数据准备**：下载 USTC-TFC-2016、CIC-IDS-2018、ISCX-Tor-2016 数据集，使用 Splitcap 分割 biflow
2. **字节矩阵构建**：选取前 M=5 个包，header 重塑为 20x20 矩阵，payload 重塑为 40x40 矩阵
3. **流交互图构建**：以包为节点提取 7 维特征，基于 burst 阈值划分 burst，构建 intra-burst 和 inter-burst 边
4. **CViT 模型搭建**：Patch 划分 → 卷积层 → 位置嵌入 → L 层 Transformer encoder → 全局池化
5. **TAGCN 模型搭建**：K 阶多项式图滤波器，L' 层图卷积 + readout 层
6. **能量模型实现**：分类器 g(h) 输出 C_k+1 logits，计算自由能量 E(h;g)，用 Weibull 分布拟合确定阈值 τ
7. **聚类模块实现**：CNN 精炼特征，初始聚类分配伪标签，动量更新样本特征，最近聚类中心重分配伪标签
8. **联合训练**：L_total = L_1 + L_2，交替优化分类和聚类模块，50 epochs

### 7.3 关键超参数、预处理和训练细节

| 参数 | 值/说明 |
|---|---|
| 每流包数 M | 5 |
| header 矩阵维度 m_h^c | 20 |
| payload 矩阵维度 m_p^c | 40 |
| 流交互图节点数 N_v | 30 |
| 温度参数 T | 10（网格搜索 0.01-100） |
| 能量边界 m_k | -10 |
| 能量边界 m_{au} | -5 |
| 损失权重 λ | 0.1 |
| 动量系数 β | 论文未明确指定 |
| 能量阈值 τ | 数据集特定，通过 Weibull 分布分位数确定（USTC: 0.05, CIC-IDS: 0.05, ISCX-Tor: 0.1） |
| 优化器 | SGD |
| 学习率（特征提取+分类） | 0.0001 |
| 学习率（聚类） | 0.001 |
| 训练轮次 | 50 |
| 批量大小 | 64 |
| 类平衡采样 | 采用 class-balanced sampling 缓解类别不平衡 |
| Transformer 层数 L | 论文未明确指定 |
| TAGCN 层数 L' | 论文未明确指定 |
| 图滤波器阶数 K | 论文未明确指定 |

### 7.4 能否迁移到其他任务？

- **IoT 设备识别**：双分支特征提取（字节+交互）可迁移到 IoT 设备指纹识别任务
- **VPN 流量分类**：方法框架可直接应用于 VPN 加密流量的细粒度分类
- **Tor 流量分析**：已在 ISCX-Tor-2016 上验证，可扩展到更多 Tor 应用场景
- **恶意软件家族分类**：开放集框架适合处理不断出现的新型恶意软件家族
- **零日攻击检测**：能量模型的已知/未知区分能力可迁移到零日攻击发现场景
- **网站指纹攻击**：字节级特征提取思路可用于加密网站流量的指纹分析
- **其他序列分类任务**：双分支（局部特征 + 交互特征）的思路可推广到其他需要多视角特征的序列分类任务

### 7.5 开放集分类对真实网络部署的实际意义

**解决流量分类的"长尾问题"**：
- 真实网络中的流量分布遵循幂律分布：少数主流应用（如 YouTube、微信、Netflix）占据大部分流量，而大量小众应用和新兴攻击构成"长尾"
- 闭集方法只能识别训练集中出现过的头部应用，对长尾部分束手无策
- FEC-OSL 的开放集框架允许模型将长尾流量识别为"未知"，再通过自适应聚类发现其内在结构，逐步将高密度聚类提升为新的已知类
- 增量更新机制（测试时识别可信新未知流并合并到辅助集）实现了模型的持续演化，无需重新训练

**对网络安全运营的实际价值**：
- **未知威胁发现**：将未知流量自动聚类，安全分析师只需审查聚类结果而非逐条分析，大幅降低人工成本
- **攻击知识库扩展**：新发现的未知类聚类结果可直接纳入威胁情报库，支持后续的自动化检测
- **误报降低**：能量模型的全局建模能力减少了将未知类误判为已知攻击类的情况，降低了安全团队的无效告警

### 7.6 对我的研究有什么启发？

1. **开放世界范式**：真实网络环境本质上是开放世界，封闭世界假设是不切实际的，研究应考虑未知类的存在
2. **能量模型替代 softmax**：EBM 通过全局建模避免 softmax 的虚假高置信度问题，在开放集识别中是更可靠的分类器设计
3. **多视角特征互补**：字节级（细粒度结构）和交互级（通信行为）特征具有天然互补性，融合可获得更全面的流表征
4. **端到端联合训练**：多任务联合训练比多阶段分别训练更优，可避免错误传播并实现任务间相互增强
5. **增量学习思想**：测试时识别可信新未知流并合并到训练集的增量更新机制，是应对持续演进威胁的实用策略
6. **特征可解释性**：通过 attention 热图和 SHAP 值分析特征重要性，增强模型的可解释性和可信度
7. **概念漂移评估**：通过重组训练/测试集模拟真实漂移是评估模型鲁棒性的有效方法
8. **辅助未知类的设计思路**：训练时引入辅助未知类（无标签）参与能量边界学习，是一种利用"已知的未知"来泛化到"未知的未知"的巧妙策略

## 8. 总结

### 8.1 核心思想（不超过20字）

能量模型驱动的端到端开放集加密流量分类与未知类聚类。

### 8.2 速记版 Pipeline（3-5步）

1. 双分支特征提取：CViT 提取字节级特征 + TAGCN 提取流交互图特征，融合为综合表征
2. 能量模型分类：映射特征为能量值，Weibull 分布建模边界，区分已知类（低能量）和未知类（高能量）
3. 自适应深度聚类：对未知流迭代优化特征和伪标签，实现细粒度类别划分
4. 端到端联合训练：统一损失函数 L_total = L_1 + L_2，三个模块协同优化
5. 增量更新：测试时识别可信新未知流，合并到辅助集进行周期性重训练

## 9. Obsidian 知识链接

### 9.1 相关概念

- Encrypted Traffic Classification - 加密流量分类
- Open-Set Recognition (OSR) - 开放集识别
- Energy-Based Model (EBM) - 能量模型
- Semi-Supervised Learning - 半监督学习
- Concept Drift - 概念漂移
- Vision Transformer (ViT) - 视觉 Transformer
- Graph Neural Network (GNN) - 图神经网络
- Network Intrusion Detection - 网络入侵检测

### 9.2 相关方法

- CViT (Convolution-enhanced ViT) - 卷积增强视觉 Transformer
- TAGCN (Topology-Adaptive Graph Convolutional Network) - 拓扑自适应图卷积网络
- Weibull Distribution Modeling - Weibull 分布建模
- Adaptive Deep Clustering - 自适应深度聚类
- Flow Interaction Graph (FIG) - 流交互图
- Helmholtz Free Energy - Helmholtz 自由能量

### 9.3 相关任务

- Open-World Traffic Classification - 开放世界流量分类
- Unknown Traffic Detection - 未知流量检测
- Unknown Class Clustering - 未知类聚类
- Malware Traffic Classification - 恶意软件流量分类
- Zero-Day Attack Detection - 零日攻击检测
- Fine-Grained Traffic Classification - 细粒度流量分类

### 9.4 可更新的综述页面

- Encrypted Traffic Classification Survey
- Open-Set Recognition for Network Traffic
- Deep Learning for Traffic Analysis

### 9.5 可加入的对比表

- Open-Set Traffic Classification Methods Comparison
- Encrypted Traffic Classification Methods
- Energy-Based vs Softmax Classification

## 10. 证据记录（表格形式）

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E1 | 实验结果 | 封闭集 USTC-TFC-2016: AC=99.60%, F1=99.59%，超越 ET-BERT 1.56% AC | Table I |
| E2 | 实验结果 | 封闭集 CIC-IDS-2018: AC=99.86%, F1=99.85% | Table I |
| E3 | 实验结果 | 封闭集 ISCX-Tor-2016: AC=99.75%, F1=99.74% | Table I |
| E4 | 实验结果 | 开放集 USTC-TFC (16:4): AUC=99.13%, F1=99.00%, AMI=83.43% | Table IV |
| E5 | 实验结果 | 高开放度 USTC-TFC (4:16): AUC~97.5%，远超 baseline ~80% | Fig. 4(a) |
| E6 | 实验结果 | 概念漂移 CIC-IDS-2018-new: F1=89.96%，仍接近 90% | Fig. 10 |
| E7 | 消融实验 | 移除 FIE 后开放集 AUC 从 99.13% 降至 80.35%，交互特征最关键 | Table IV |
| E8 | 消融实验 | 移除 header 后开放集 AUC 从 99.13% 降至 85.59% | Table IV |
| E9 | 消融实验 | 替换 EBM 为 softmax 后 AUC 从 99.13% 降至 89.65% | Table IV |
| E10 | 可视化 | 训练后已知类形成紧凑聚类，未知类与已知类清晰分离 | Fig. 7 |
| E11 | 可解释性 | Weibo 关注 TCP window size，Zeus 关注 TCP flags 和 SYN options | Fig. 8 |
| E12 | 参数分析 | m_h^c=20, m_p^c=40, N_v=30, T=10, m_k=-10, m_{au}=-5 为最优配置 | Fig. 12-13 |
| E13 | 消融实验 | 移除 BFE 后封闭集 F1 从 99.59% 降至 97.79%（-1.80%），字节特征贡献显著 | Table III |
| E14 | 消融实验 | 移除 header 比移除 payload 影响更大（F1 -2.61% vs -1.52%），header 信息更关键 | Table III |
| E15 | 消融实验 | 移除 FIE 后封闭集 F1 从 99.59% 降至 97.30%（-2.29%），交互特征同样重要 | Table III |
| E16 | 消融实验 | 移除 FIE 后开放集 AMI 从 83.43% 降至 71.59%（-11.84%），交互特征对聚类最关键 | Table IV |
| E17 | 跨数据集 | CIC-IDS-2018 (2:5): FEC-OSL AUC=94.0% vs CVAE-EVT 83.0% vs ECNet 90.0% | Fig. 5(a) |
| E18 | 跨数据集 | ISCX-Tor-2016 (2:6): FEC-OSL AUC=95.0% vs CVAE-EVT 87.0% vs ECNet 88.0% | Fig. 6(a) |
| E19 | 参数分析 | 能量阈值分位数 0.9 时 F1 骤降至 42%，说明阈值选择对性能影响极大 | Fig. 12(d) |
| E20 | 参数分析 | 温度参数 T=100 时 AUC 降至 86.50%，T=10 为最优（99.50%） | Fig. 12(e) |
| E21 | 特征分析 | SHAP 分析：Weibo 依赖 direction-length 和 bytes in burst，Zeus 依赖 timestamp 和 direction-length | Fig. 9 |
| E22 | 行业数据 | 约 85.9% 的网络威胁通过加密通道传输（Zscaler 2023 报告） | Section I |

## 11. 原始资料链接

- 论文发表于 IEEE TIFS 2026，DOI: 10.1109/TIFS.2026.3653575
- 作者单位：南京邮电大学计算机科学学院（Qian Yang 等）、浙江大学区块链与数据安全国家重点实验室（Kui Ren）
- 资助项目：国家重点研发计划 (2023YFB2904000, 2023YFB2904004)、江苏省重点发展规划项目 (BE2023004-2)、未来网络科研基金 (FNSRFP-2021-YB-15)
- 数据集来源：USTC-TFC-2016（中国科学技术大学）、CIC-IDS-2018（加拿大网络安全研究所）、ISCX-Tor-2016
- 关键参考工具：Splitcap（biflow 分割）、OpenSSH、Wireshark

## 12. 后续问题

1. **变长流建模**：如何在不固定前 N 个包的情况下捕获流的完整特征？论文提到未来可能探索 variable-length 或 context-aware flow modeling
2. **轻量化设计**：如何降低双分支特征提取和聚类的计算开销以适应低延迟场景？论文提到探索 lightweight alternatives 或 approximation strategies
3. **测试时自适应**：论文计划探索 test-time training/adaptation 方法，使模型在测试阶段通过自适应学习动态调整参数
4. **对抗性攻击**：如果攻击者故意模仿已知类的统计和字节特征，能量模型是否仍能有效区分？
5. **更大规模验证**：在高速网络（10Gbps+）和更大规模数据集上的可扩展性如何？
6. **与其他 EBM 方法的对比**：能量模型在其他开放集流量分类框架中的通用性如何？
7. **辅助未知类选择策略**：如何更有效地选择辅助未知类，使其更好地代表测试中的新未知类？
8. **聚类数量自动确定**：能否自动确定未知类的真实聚类数，而非预设一个较大的初始值？
9. **实时部署可行性**：端到端框架在实际网络设备上的推理延迟和资源消耗如何？
10. **跨域泛化**：在一个网络环境中训练的模型能否直接部署到另一个不同特征的网络环境？

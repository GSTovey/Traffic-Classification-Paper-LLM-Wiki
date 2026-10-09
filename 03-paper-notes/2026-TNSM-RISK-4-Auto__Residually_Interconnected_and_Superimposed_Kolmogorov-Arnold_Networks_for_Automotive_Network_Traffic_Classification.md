---
type: paper
title_original: "RISK-4-AUTO: Residually Interconnected and Superimposed Kolmogorov-Arnold Networks for Automotive Network Traffic Classification"
title_cn: "RISK-4-AUTO：用于车载网络流量分类的残差互联叠加 Kolmogorov-Arnold 网络"
authors: ["Anurag Dutta", "Sangita Roy", "Rajat Subhra Chakraborty"]
year: 2026
venue: "IEEE TNSM 2026"
doi: "10.1109/tnsm.2025.3625404"
url: "https://doi.org/10.1109/tnsm.2025.3625404"
pdf: "00-inbox/PDFs/2026-TNSM-RISK-4-Auto__Residually_Interconnected_and_Superimposed_Kolmogorov-Arnold_Networks_for_Automotive_Network_Traffic_Classification.pdf"
mineru_md: "02-parsed-markdown/2026-TNSM-RISK-4-Auto__Residually_Interconnected_and_Superimposed_Kolmogorov-Arnold_Networks_for_Automotive_Network_Traffic_Classification.md"
status: processed
reading_level: L2
research_area: ["malicious-traffic-detection", "traffic-classification"]
task: ["malicious-traffic-detection", "traffic-classification"]
method: ["convolutional-network"]
dataset: ["HCRL-Car Hacking Dataset (HCRL-CHD)", "HCRL-CAN-FD", "HCRL-B-CAN"]
code: "https://github.com/Anurag-Dutta/RISK-4-Auto"
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

# RISK-4-AUTO: Residually Interconnected and Superimposed Kolmogorov-Arnold Networks for Automotive Network Traffic Classification

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | RISK-4-AUTO: Residually Interconnected and Superimposed Kolmogorov-Arnold Networks for Automotive Network Traffic Classification |
| 中文标题 | RISK-4-AUTO：用于车载网络流量分类的残差互联叠加 Kolmogorov-Arnold 网络 |
| 作者 | Anurag Dutta（IIT Kharagpur 计算机系在读硕士，IEEE Graduate Student Member）、Sangita Roy（Thapar Institute of Engineering and Technology 助理教授，IEEE Member）、Rajat Subhra Chakraborty（IIT Kharagpur 教授，IEEE Senior Member） |
| 年份 | 2026 |
| 会议/期刊 | IEEE Transactions on Network and Service Management (TNSM)；DOI 10.1109/tnsm.2025.3625404（由主代理分配给出，解析稿正文未印 DOI） |
| 研究方向 | 车载网络（CAN 总线）入侵检测/流量分类：以二维直方图（mini-FlowPic）+ KAN 混合网络做有监督多分类与单类二分类 |
| 任务类型 | （1）全类多分类：HCRL-CHD 5 类、CAN-FD 3 类、B-CAN 3 类；（2）聚焦单类检测：对每个恶意类别做"注入/正常"二分类（共 4+3+2 个二分类任务） |
| 方法关键词 | 四个模型：LIN-KAN、RES-KAN、RES-KAN^BN、RES-KAN^II；mini-FlowPic 64×64 灰度直方图（Algorithm 1 SessionPlotter）；Residual Block（Eq. 1）；KAN 层（B-spline 可训练激活，Eq. 2–5，grid-size=10 / spline-order=3 / noise-factor=1e-2）；MaxPool2D 2×2；Softmax 分类 |
| 数据集 | HCRL-Car Hacking Dataset（HCRL-CHD，5 类）、HCRL CAN with Flexible Data Rate（HCRL-CAN-FD，3 类）、HCRL Bus-type CAN（HCRL-B-CAN，3 类），均为 OBD 口直注采集的公开数据集 |
| 是否开源 | 开源：https://github.com/Anurag-Dutta/RISK-4-Auto（参考文献 [34]，论文称公开发布代码与部分 2D 直方图数据） |
| PDF | 00-inbox/PDFs/2026-TNSM-RISK-4-Auto__Residually_Interconnected_and_Superimposed_Kolmogorov-Arnold_Networks_for_Automotive_Network_Traffic_Classification.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-TNSM-RISK-4-Auto__Residually_Interconnected_and_Superimposed_Kolmogorov-Arnold_Networks_for_Automotive_Network_Traffic_Classification.md |

---

## 1. 一句话总结

> RISK-4-AUTO 把 CAN 帧序列画成 64×64 mini-FlowPic 直方图，用 4 个 ResNet+KAN 混合模型（LIN-KAN/RES-KAN/RES-KAN^BN/RES-KAN^II）做车载网络流量分类，全类准确率最高 0.9976/0.9992/0.9303（HCRL-CHD/CAN-FD/B-CAN），平均超 6 个 SOTA 1.0163%，聚焦二分类平均超 2.5535%。

---

## 2. 摘要翻译

### 2.1 摘要原文

In modern automobiles, a Controller Area Network (CAN) bus facilitates communication among all electronic control units for critical safety functions, including steering, braking, and fuel injection. However, due to the lack of security features, it may be vulnerable to malicious bus traffic-based attacks that cause the automobile to malfunction. Such malicious bus traffic can be the result of either external fabricated messages or direct injection through the on-board diagnostic port, highlighting the need for an effective intrusion detection system to efficiently identify suspicious network flows and potential intrusions. This work introduces Residually Interconnected and Superimposed Kolmogorov-Arnold Networks (RISK-4-AUTO), a set of four deep neural network architectures for intrusion detection targeting in-vehicle network traffic classification. RISK-4-AUTO models, when applied on three hexadecimally identifiable sequence-based open-source datasets (collected through direct injection in the on-board diagnostic port), outperform six state-of-the-art vehicular network intrusion detection systems (as per their accuracies) by 1.0163% for all-class classification and 2.5535% on focused (single-class) malicious flow detection. Additionally, RISK-4-AUTO enjoys a significantly lower overhead than existing state-of-the-art models, and is suitable for real-time deployment in resource-constrained automotive environments.

### 2.2 摘要中文翻译

在现代汽车中，控制器局域网（CAN）总线支撑所有电子控制单元（ECU）之间的通信，服务于转向、制动、燃油喷射等关键安全功能。然而由于协议缺乏安全机制，CAN 总线易受恶意总线流量攻击而令车辆发生故障。此类恶意流量既可能来自外部伪造报文，也可能来自通过车载诊断（OBD）口的直接注入，因此需要高效的入侵检测系统及时识别可疑流量与潜在入侵。本文提出 RISK-4-AUTO（Residually Interconnected and Superimposed Kolmogorov-Arnold Networks）——一组面向车载网络流量分类的四套深度神经网络架构。在三个以十六进制序列表示的公开数据集（均通过 OBD 口直接注入采集）上，RISK-4-AUTO 在全类分类上平均超越六个最先进车载入侵检测系统 1.0163%（按准确率），在聚焦（单类）恶意流量检测上超越 2.5535%。此外，RISK-4-AUTO 的开销显著低于现有最先进模型，适合在资源受限的车载环境中实时部署。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- CAN 总线按 ISO 11898 广播通信，**没有任何内建密码学机制**（无机密性与发送方认证），攻击者可通过 OBD 口注入伪造帧、或经远程信息处理单元（telematics）无线注入，导致转向/制动等关键功能失效（§I）。
- 现有车载 IDS 多为深网络（DCNN 的深层卷积）、或带注意力机制（CANIntelliIDS）、或多层协调（MTH-IDS），在**资源受限的车载硬件**上推理/内存开销大，且部分方法（RNN 类）依赖大规模标注数据，数据稀缺时性能退化（§I、§II、§III.A）。
- 时间序列→二维直方图（FlowPic / mini-FlowPic）能把"每个数据实例的信息增益"放大（同一会话的多帧压缩为一张图），且作者声称 KAN 的可训练激活函数（B-spline）在图像分类上比固定激活的 MLP 更具表达效率（§III.A–C、§IV.A"我们贡献"段）。

### 3.2 现有方法的痛点和不足

| 现有方法 | 痛点（论文表述） |
|---|---|
| RNN + 启发式（Tariq et al. [9]） | 奖励塑形复杂、设计不当会提高 FPR；训练 RNN 需大量标注数据，周期与成本高（§II） |
| CANTransfer（Conv-LSTM 迁移学习 [10]） | 精度依赖微调数据量，数据稀缺时性能退化（§II） |
| DCNN（Song et al. [3]） | 效果受标注数据量与质量影响大；卷积层深导致推理时间增加（§II） |
| CANIntelliIDS（CNN+注意力 GRU [11]） | 注意力机制带来推理期内存开销大（§II） |
| GIDS（GAN 增强 [12]） | 无约束生成可能产生不真实样本、训练不稳；合成样本致"死记硬背"式学习（§II） |
| MTH-IDS（三层云端+雾端+边缘 [23]） | 多层协调带来通信时延（§II） |
| LSTMIDS（LSTM 自编码器 [13]） | 论文承认其"据我们所知报告了迄今最好的分类性能"（约 99%），但其精度仍低于 RISK-4-AUTO（§II、§VI） |

### 3.3 论文的研究假设或核心直觉

核心直觉：**把 CAN 会话的（到达时间 × 帧大小）联合分布画成 64×64 灰度图后，类别差异变成"图像的纹理差异"**——正常流量稠密、均匀、周期性，注入流量稀疏或非均匀（突发尖峰）（§I、Fig. 1）；用少量残差卷积层 + KAN 层即可从这些图中分出正常/攻击类别，且模型足够轻，能部署在车载硬件上。作者同时假设 KAN 的"可训练激活"比固定激活 MLP 表达效率更高（§III.C、§IV.B 设计理由）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | CAN 无密码学保护；恶意帧可来自 OBD 直注或无线注入；正常流量与注入流量在"时间-大小"二维分布上形态不同 | §I、Fig. 1 |
| 痛点提炼 | 现有 IDS 依赖深网络/注意力/多级协调，开销大；RNN 类需大量数据 | §I、§II |
| 问题转化 | 把"车联网流量分类"转化为"直方图图像分类"，用 mini-FlowPic 表示 + 轻量 ResNet/KAN 分类器求解 | §III.A、§IV |
| 文献定位 | 现有文献"几乎只做全类分类，尚无工作报告每类攻击的类内检测"（作者称），本文补上聚焦单类检测 | §V.B、§VI.A |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 64×64 mini-FlowPic + ResNet-KAN 混合模型可在三个 HCRL 数据集上超越 6 个 SOTA IDS | §III.A、§IV.B | Tables IV–XV 全类与聚焦二分类对比 |
| 辅助假设 1 | 残差连接可缓解深层网络的梯度消失，提高直方图分类精度 | §III.B、Eq. 1 | Table XVI 消融（加 Residual Block 后 0.9192→0.9627） |
| 辅助假设 2 | KAN 可训练激活优于纯线性/MLP 层 | §III.C、Eq. 2–5 | Table XVI（KAN-Linear ×1→×2：0.9883→0.9887；叠加 Residual ×2 后 0.9966） |
| 辅助假设 3 | 四套模型覆盖"精度优先/轻量优先"两种部署需求 | §IV.B、Table XVI | TTTr/TTTe/模型大小对比（LIN-KAN 最轻、RES-KAN^II 最准） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑（论文自报） | 三数据集全类最高 0.9976/0.9992/0.9303；聚焦二分类多数类别达 1.0000 | §VI.A，Tables IV–XV |
| 辅助假设 1（残差） | 支撑 | 消融中 "Linear(×2) → Linear+Residual Block"：0.9192→0.9627 | §VI.B, Table XVI |
| 辅助假设 2（KAN） | 支撑（有限） | KAN-Linear(×1) 0.9883 → 加残差 0.9966；但再加第三层 KAN 反降至 0.9951 | §VI.B, Table XVI |
| 辅助假设 3（轻量） | 部分支撑 | LIN-KAN 训练 620.13 s（LSTMIDS 2016.48 s）、推理 8.46 s；但精度最高的 RES-KAN^II 训练 2438.17 s、推理 12.01 s，均**高于** LSTMIDS（2016.48/9.07 s） | §VI.A, Table IV |

---

## 4. 方法设计

### 4.1 方法整体流程

三阶段（Fig. 2）：(I) 从 ECU 捕获 CAN 会话（含 Timestamp、CAN ID（十六进制）、包数 n、n 个到达时间戳、n 个帧大小、以及标注用的 "Flag" 字段）；(II) 用 SessionPlotter（Algorithm 1）把到达时间与帧大小归一化后填入 (#MTU × #MTU) 二维直方图（本文 #MTU=64），得到灰度图并标注；(III) 用四个 KAN/ResNet 混合模型做有监督分类（多类或二分类）（§IV.A）。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 会话采集 | CAN 总线流量 | 采集单个会话的帧序列与 Flag 标注（正常/注入） | 五元特征 + Flag | 原始数据（OBD 直注数据集） |
| Step 2 归一化 | 到达时间序列 $T$、帧大小序列 $\Pi$（各 n 维） | $\tilde{T}_i=((T_i-T_0)/(T_{n-1}-T_0))\cdot$#MTU；$\tilde{\Pi}_i$ 同理（Algorithm 1 第 4–5 行） | 归一化向量 | 把异质量纲压到同一网格 |
| Step 3 直方图生成 | $\tilde{T},\tilde{\Pi}$ | 初始化 $H_{(\#MTU\times\#MTU)}\leftarrow\mathbf{0}$；对每帧 $H_{\lfloor\tilde{\Pi}_j\rfloor,\lfloor\tilde{T}_j\rfloor}\mathrel{+}=1$ | 64×64 灰度直方图（强度 0–255） | 时序→图像表示，放大单实例信息量 |
| Step 4 特征展平（LIN-KAN） | 64×64 图 | Flatten 为 4096 维向量，喂入 KAN 层（解析稿称"以每批 32 个特征"输入） | 分类 logits | 最轻量基线模型 |
| Step 5 残差特征提取（RES-KAN 系） | 64×64 图 | 两组 Residual Block + MaxPool2D(2×2)：第一组 $n_{in}$=1→$n_{out}$=5，第二组 5→25；RES-KAN^BN 额外加 BatchNorm2D；RES-KAN^II 再用两个 KAN 层做特征提取与映射 | 空间特征 | 提取时空特征并抑制梯度问题 |
| Step 6 分类 | 特征向量 | KAN 层 + Softmax 输出类别（五类场景）（§IV.B.1） | 类别概率 | 多类/二分类共用 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| SessionPlotter（Algorithm 1） | 时间×大小二维直方图生成 | 帧时间戳与大小序列 | 64×64 灰度图 | 所有模型的公共输入表示 |
| Residual Block 组（×2）+ MaxPool2D | 空间特征提取、降采样 | 直方图（单通道） | 5→25 通道特征图 | LIN-KAN 之后所有变体的公共主干 |
| BatchNorm2D（仅 RES-KAN^BN） | 缓解内部协变量偏移、改善梯度流 | 残差层输出 | 归一化特征 | 插入每个残差层后 |
| KAN 层（B-spline 可训练激活） | 非线性映射与分类 | 展平/特征向量 | logits | LIN-KAN 一层；RES-KAN^II 两层 |
| Softmax 输出层 | 类别分布 | KAN 输出 | 概率 | 训练用交叉熵 |

### 4.4 公式、算法和机制解释

- **残差块（Eq. 1）**：$\mathbf{x}\mapsto a[\mathbf{x}]+\mathbf{x}$，$a[\cdot]$ 为任意层的激活；作者引入残差的原因是直方图学习易受梯度消失影响（§III.B）。
- **MLP vs KAN（Eq. 2–3）**：MLP 近似 $y=\sum a[\Omega\cdot\mathbf{x}+\beta]$（固定激活 $a$）；KAN 依 Kolmogorov-Arnold 表示定理近似 $y=\sum\Phi[\sum\phi[\mathrm{x}]]$，其中 $\phi_{i,j}$ 是可训练的实值函数（B-spline）（§III.C）。
- **基函数（Eq. 4）**：$\phi_{i,j}[x_i]=\mu^{(b)}_{i,j}\cdot(x_i/(1+e^{-x_i}))+\mu^{(s)}_{i,j}\cdot\sum_k\lambda_{i,j,k}\mathcal{B}_k[x_i]$，即"生物项（Swish）+ spline 项（B-spline 系数 $\lambda$）"的加权和。
- **组合矩阵（Eq. 5）**：$\Phi_\ell$ 为 L×L 的层内映射矩阵，元素 $\phi_{\ell,i,j}$（§III.C）。
- **Algorithm 1（SessionPlotter）**：见 §4.2 Step 2–3；要点是**归一化用 min-max 形式的端点差**（$T_0$ 与 $T_{n-1}$），然后取整索引并累加计数。
- **KAN 超参**（§IV.B 末）：grid-size=10（网络复杂度）、spline-order=3（三次多项式 B-spline）、noise-factor=$10^{-2}$（正则化防过拟合）；随机初始化后用交叉验证更新，训练时留 10% 数据做验证。
- **模型参数选择理由**（§IV.B 末）：64×64 灰度图共 4096 特征；首层 $n_{out}$=5 对应"至多五类"的车载流量分类上限；5→25 保持扩容比 5；MaxPool 取 2×2 适合小尺寸图像。

### 4.5 方法优势

- **表示侧**：把一段会话压成一张 64×64 图，减少了对逐帧时序建模的依赖，且天然不受 CAN ID 之类的标识特征支配（论文强调数据集为"hexadecimally identifiable sequence-based"，分类依据是时间-大小形态）。
- **模型侧**：四个模型覆盖"精度优先"（RES-KAN^II/RES-KAN^BN）与"轻量优先"（LIN-KAN/RES-KAN）两类需求，便于按部署条件选型（§VI.B 末）。
- **任务侧**：除全类分类外，补充了**每个攻击类别的聚焦二分类**（此前文献未见报告，作者称），并给出 TTTr/TTTe 时间开销。
- **开源**：代码与部分处理后的 2D 直方图数据公开（[34]）。

### 4.6 方法不足

- **"低开销"结论与数据不完全一致**：摘要称"显著更低的开销"，但 Table IV 中精度最高的 RES-KAN^II 的 TTTr（2438.17 s）与 TTTe（12.01 s）均高于 LSTMIDS（2016.48 s / 9.07 s）；只有 LIN-KAN 一档真正轻量（620.13 s / 8.46 s）（§VI.A）。
- **最佳模型的训练/推理成本随结构增加而显著上升**，Table XVI 显示 RES-KAN^II 配置模型体积达 96623 kB（约 94 MB），加第三层 KAN 后达 503684 kB（约 492 MB）却精度下降。
- **数据层面**：三个数据集均来自 OBD 口**直接注入**（单一注入路径），论文自陈"不能泛化到完全未知的攻击"（§VII）。
- **未说明**：数据划分按会话级还是帧级（影响直方图是否泄漏）、重复次数与方差来源（Table XVI 给了 stdev 但总体表未给）、超参搜索范围。
- **对比基线均取自他人论文报告的数值**，未在统一环境下重跑；且部分基线的实现细节（如 CANIntelliIDS 的内存开销）仅作定性引用。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

现有车载 IDS 直接对 CAN 帧序列建模（RNN/Conv-LSTM 学时序、DCNN 把帧映射到时间×ID 二维图、注意力 GRU 抓显著片段、GAN 做数据增强）；RISK-4-AUTO 改走"**流量图像化 + KAN**"路线：用（到达时间，帧大小）直方图代替原始序列，用"可训练激活（B-spline）"代替固定激活的卷积/全连接堆叠，用残差连接控制深度，从而在同样甚至更少数据下提高精度（§III、§IV、§VI）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 车载场景的 mini-FlowPic 表示 | 64×64 时间-大小直方图用于 CAN 流量（沿用 FlowPic [25][26]、mini-FlowPic [27]） | 中（表示本身非首创，跨域迁移） | 是（任何帧序列总线/日志数据） |
| ResNet + KAN 混合架构 | 4 个变体：LIN-KAN/RES-KAN/RES-KAN^BN/RES-KAN^II | 中（KAN 在流量分类的早期应用） | 是（图像/直方图分类任务） |
| 聚焦单类检测 | 对每个攻击类别做注入/正常二分类（此前文献未见报告） | 中 | 是（其他 IDS 评估可增补该协议） |
| 开销报告口径 | 用 TTTr/TTTe/模型体积（kB）而非仅参数量报告开销 | 低-中 | 是（工程选型友好） |

### 5.3 适用场景

车载 CAN 总线（ISO 11898）实时入侵检测，部署点为车辆 ECU 侧（资源受限：论文实验硬件仅为 Intel i7-1065G7 + 2 GiB 显存的 MX330）；作者指出方法可扩展到 Automotive Ethernet、SPI、安全系统等其他车载网络（§VII）。适用前提是能获得带 Flag 标注的会话数据（本文数据集为 OBD 直注采集）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| LSTMIDS [13] | 仅在良性数据上训练自编码器，约 99% 准确率，迄今最强基线之一 | 精度仍低于 RISK-4-AUTO；训练时间长（CHD 2016.48 s） | RES-KAN^II 全类 0.9976 vs 0.9901（+0.75 pp） |
| GIDS [12] | GAN 增强提升抗噪与泛化 | 生成样本可能失真、训练不稳、易"背题" | 无需数据增强即达更高精度（CHD 0.9976 vs 0.9872） |
| CANIntelliIDS [11] | CNN+注意力 GRU，混合攻击场景 +10% | 注意力机制推理内存开销大 | 无注意力结构，参数量更小（RES-KAN 系） |
| DCNN [3] | 免手工特征、把帧映射为二维图 | 卷积层深、推理慢；依赖标注数据量 | 1–2 组残差卷积即可（LIN-KAN 甚至卷积为零） |
| CANTransfer [10] | 迁移学习降低数据需求 | 微调数据不足时精度退化 | 直接在直方图上训练，无需预训练迁移 |
| RNN+Heuristics [9] | 强化学习自适应阈值 | 奖励塑形复杂、FPR 风险、需大量数据 | 有监督图像分类替代奖励设计 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

PyTorch v2.4 实现；硬件 16 GB 内存、Intel Core i7-1065G7 @1.30 GHz、NVIDIA GeForce MX330（2 GiB 显存）；数据按 **80:10:10** 划分训练/测试/验证；报告 Accuracy/Precision/Recall/F1 与 TTTr（Time-to-Train）、TTTe（Time-to-Test）（§V.B、§VI.A）。代码与部分 2D 直方图数据已开源（[34]）。

### 6.2 数据集

| 数据集 | 类别/内容 | 规模（按 Table I–III 原文，印度计数法） | 说明 |
|---|---|---|---|
| HCRL-CHD [20] | 5 类：DoS、Fuzzy、Gear Spoofing、RPM Spoofing、Benign | 注入：5,87,521 / 4,91,847 / 5,97,252 / 6,54,897（≈587,521/491,847/597,252/654,897）；正常：30,78,250 / 33,47,013 / 38,45,890 / 39,66,805（≈3.08M/3.35M/3.85M/3.97M）；Benign 9,88,987（≈988,987） | Table I |
| HCRL-CAN-FD [21] | 3 类：Flooding、Fuzzy、Malfunction | 注入：9,88,241 / 5,06,506 / 1,35,726；正常：17,96,070 / 18,95,836 / 17,98,223 | Table II |
| HCRL-B-CAN [22] | 3 类：DDoS、Fuzzy、Benign | 注入：4,00,000 / 1,00,000；Benign/正常：25,10,262 | Table III |

三个数据集均以十六进制序列形式给出（含 Timestamp、CAN ID、包数、到达时间、帧大小与 Flag），据 HCRL 的采集说明均为 OBD 口直接注入（§V.A）。

### 6.3 Baseline

六个 SOTA IDS（按论文给出顺序）：LSTMIDS [13]、GIDS [12]、CANintelliIDS [11]、DCNN [3]、CANTransfer [10]、RNN+Heuristics [9]。聚焦二分类的对比对象分别是 SOTA-IDS [13]（HCRL-CHD 四类与 B-CAN 两类）与 SOTA-IDS [12]（CAN-FD 三类）（Tables VII–XV）。⚠️ 所有基线数值均引自原论文（论文未说明是否复现）。

### 6.4 评价指标

Accuracy、Precision、Recall、F1-Score（分类）；TTTr（秒）、TTTe（秒）（开销）；消融额外报告"模型体积（kB）"与准确率 stdev（Table XVI）。全类分类的"提升"按与最优 SOTA 的准确率差计。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文最好模型 | 最优对比方法 | 提升 | 说明 |
|---|---|---|---:|---:|---:|---|
| HCRL-CHD 全类（5 类） | Accuracy | 0.9976（RES-KAN^II；R/P/F1 = 0.9978） | LSTMIDS 0.9901 | +0.7576 pp（论文口径） | Table IV；LIN-KAN 0.9883、RES-KAN 0.9966、RES-KAN^BN 0.9917 |
| HCRL-CAN-FD 全类（3 类） | Accuracy | 0.9992（RES-KAN^BN 与 RES-KAN^II） | GIDS 0.9947 | +0.4523 pp | Table V；LIN-KAN 0.9928、RES-KAN 0.9986 |
| HCRL-B-CAN 全类（3 类） | Accuracy | 0.9303（RES-KAN^II） | LSTMIDS 0.9135 | +1.8398 pp | Table VI；LIN-KAN 0.9022、RES-KAN 0.9166、RES-KAN^BN 0.9202 |
| 三数据集全类平均 | Accuracy | — | — | 平均 +1.0163%（摘要/结论口径） | 由 0.7576/0.4523/1.8398 三点平均得 ≈1.0166 |
| HCRL-CHD 聚焦 DoS 二分类 | Accuracy | 1.0000（RES-KAN^BN、RES-KAN^II） | LSTMIDS 0.9796 | +2.04 pp | Table VII |
| HCRL-CHD 聚焦 Fuzzy 二分类 | Accuracy | 1.0000（RES-KAN、RES-KAN^BN、RES-KAN^II） | LSTMIDS 0.9806 | +1.94 pp | Table VIII |
| HCRL-CHD 聚焦 Gear 二分类 | Accuracy | 1.0000（RES-KAN 及之后） | LSTMIDS 0.9783 | +2.17 pp | Table IX |
| HCRL-CHD 聚焦 RPM 二分类 | Accuracy | 1.0000（RES-KAN^II） | LSTMIDS 0.9620 | +3.80 pp | Table X；RES-KAN^BN 0.9998 |
| HCRL-CAN-FD 聚焦 Flooding | Accuracy | 1.0000（RES-KAN 及之后） | GIDS 0.9892 | +1.08 pp | Table XI |
| HCRL-CAN-FD 聚焦 Fuzzy | Accuracy | 1.0000（LIN-KAN 即达 1.0000） | GIDS 0.9975 | +0.25 pp | Table XII |
| HCRL-CAN-FD 聚焦 Malfunction | Accuracy | 1.0000（LIN-KAN 即达 1.0000） | GIDS 0.9992 | +0.08 pp | Table XIII |
| HCRL-B-CAN 聚焦 DDoS | Accuracy | 1.0000（RES-KAN 及之后） | LSTMIDS 1.0000 | 持平（LIN-KAN 反而 0.9972） | Table XIV |
| HCRL-B-CAN 聚焦 Fuzzy | Accuracy | 1.0000（RES-KAN 及之后） | LSTMIDS 0.9985 | +0.15 pp | Table XV |
| 聚焦二分类平均 | Accuracy | — | — | 平均 +2.5535%（偏差 0.4596） | §VI.A 文字 |
| 消融（最优层配置） | Accuracy / TTTr / TTTe / 体积 | 0.9976(0.0008) / 2438.17 s / 12.01 s / 96623 kB | 配置 KAN-Linear(×2)+Residual(×2) | 再加 KAN(×3) 降至 0.9951(0.0011)，体积 503684 kB | Table XVI |

### 6.6 优势最明显的场景

- **B-CAN 数据集**：全类提升最大（+1.84 pp），说明在类别更少但分布更接近真实的拓扑数据集上直方图表示仍有效（Table VI）。
- **聚焦单类检测**：几乎所有恶意类别可达 1.0000 准确率（Tables VII–XV），论文据此强调"类内检测"协议的价值。
- **轻量部署档（LIN-KAN）**：CHD 上 TTTr 620.13 s、TTTe 8.46 s，为全部模型中最快，准确率 0.9883 仍接近 LSTMIDS（0.9901）（Table IV）。
- **残差带来的稳定提升**：消融显示从纯线性到"线性+残差"准确率 0.9192→0.9627（+4.35 pp），是最显著的结构性增益（Table XVI）。

### 6.7 局限性

- 实验硬件规模极小（2 GiB 显存），能否代表真实车规算力未讨论；训练时间随模型加深急剧上升（最高 3119.48 s）。
- 所有基线数值为引用值，未在统一环境下复现；不同 baseline 出自不同论文与实验设置，可比性受限。
- "显著更低开销"仅对 LIN-KAN/RES-KAN 成立；最强模型反而更慢（见 §4.6 与 §3.5 验证表）。
- 仅在 OBD 直注数据集上评测；论文自陈无法泛化到未见攻击类型（§VII）。
- 数据划分粒度（会话级 vs 帧级）未说明，直方图表示下同一会话的帧可能跨划分泄漏。
- Table XVI 存在一行 "Residual Block (×2) → Residual Block (×2) | Baseline Model" 无任何数值（原文如此），影响消融链的完整性。

---

## 7. 学习与应用

### 7.1 是否开源？

开源：https://github.com/Anurag-Dutta/RISK-4-Auto（参考文献 [34]），论文称发布代码与处理后的部分 2D 直方图数据，便于复现。

### 7.2 复现关键步骤

1. 取 HCRL-CHD / HCRL-CAN-FD / HCRL-B-CAN 逐会话数据（Timestamp、CAN ID、帧数、到达时间序列、帧大小序列、Flag）。
2. 按 Algorithm 1：对到达时间与帧大小做端点归一化（乘 #MTU=64）→ 取整 → 累加到 64×64 直方图 → 灰度强度 0–255。
3. 训练四个模型之一：LIN-KAN（Flatten 4096 → KAN → Softmax）；RES-KAN（两组 Residual+MaxPool2D，1→5→25 通道，再走 LIN-KAN 路径）；RES-KAN^BN（残差后加 BatchNorm2D）；RES-KAN^II（两个 KAN 层）。
4. KAN 超参：grid-size=10、spline-order=3、noise-factor=1e-2；留 10% 验证；交叉验证调参；Softmax + 交叉熵。
5. 80:10:10 划分；报告 Accuracy/Precision/Recall/F1 与 TTTr/TTTe/模型体积。

### 7.3 关键超参数、预处理和训练细节

- 表示：#MTU=64（mini-FlowPic 维度之一；原始 FlowPic 用 1500，mini-FlowPic 后续用 64/128/256）→ 4096 维。
- KAN：grid-size=10、spline-order=3、noise-factor=$10^{-2}$；激活 = Swish（生物项）+ B-spline（spline 项）加权和。
- 结构：残差组 1→5 与 5→25 通道；MaxPool2D 2×2；RES-KAN^BN 在每个残差层后加 BatchNorm2D。
- 训练/划分：PyTorch 2.4；80:10:10；论文未给出学习率、批大小、优化器与 epoch 数。
- 设备：i7-1065G7 @1.30 GHz + 16 GB 内存 + MX330 2 GiB。

### 7.4 能否迁移到其他任务？

- **表示层可直接迁移**：任何"帧序列 →（到达时间，大小）直方图"的场景（其他总线、IoT 报文、系统日志）都可套用 mini-FlowPic + Algorithm 1，且提供 64/128/256 三档分辨率取舍。
- **KAN 组件的迁移**：把 KAN 层接到现有 CNN 主干（如流量图像分类、恶意流量检测）上可做消融对照；但 Table XVI 显示 KAN 层数存在明显最优点（×2 最优，×3 精度降、体积暴涨 5.2 倍），迁移时需重新做层级扫描。
- **评估协议可迁移**：其"全类 + 每类聚焦二分类"的双层评估，适合作为 IDS 论文的补充协议；TTTr/TTTe/模型体积（kB）报告口径对工程选型友好。
- 注意：任务域是**明文 CAN 总线**，与 KB 主线的加密流量/WF 场景相距较远；方法对比时应说明域差异（CAN 无加密与载荷语义遮蔽问题）。

### 7.5 对我的研究有什么启发？

- **"序列→图像"表示的复用价值**：与 KB 中 FlowPic 系列一脉相承；若研究加密流量分类，可把该表示的"归一化 + 网格计数"当作轻量对照基线（但应警惕其信息损失）。
- **KAN 的工程定位**：本文把 KAN 当作"替代固定激活的最后一层/中间层"，并在消融中给出"层数过深反而更差"的证据，可作为 KAN 相关实验的起点参照。
- **评估补充**：聚焦单类检测（每类 vs 正常）在 WF/恶意检测中同样可用，能暴露"全类精度掩盖某类完全失效"的问题。
- **与 KB 的接口**：其表示直接来自 [[2019-INFOCOM-FlowPic__Encrypted_Internet_Traffic_Classification_is_as_Easy_as_Image_Recognition]]（本文引用 [26]），可与 KB 中其他使用图像化表示的工作（如 BTRFormer 的分块表示、MM4flow 的多模态）横向比较表示策略。
- **需要警惕**：论文的"低开销"叙述与表格数据存在张力（见 §4.6），引用其开销结论前应回到 Table IV/XVI 核对。

---

## 8. 总结

### 8.1 核心思想

> CAN 帧序列画成 64×64 直方图，用 ResNet+KAN 做分类。

### 8.2 速记版 Pipeline

1. 采集 CAN 会话（时间戳、CAN ID、包数、到达时间、帧大小、Flag）。
2. Algorithm 1 归一化 + 64×64 直方图计数（灰度 0–255）。
3. LIN-KAN：Flatten 4096 → KAN → Softmax；RES-KAN 系加两组 Residual+MaxPool2D（1→5→25）。
4. RES-KAN^BN 加 BatchNorm2D；RES-KAN^II 使用两个 KAN 层（最优）。
5. 80:10:10 训练；HCRL-CHD 全类 0.9976、CAN-FD 0.9992、B-CAN 0.9303；聚焦二分类多数达 1.0000。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[malicious-traffic-detection]]（车载总线入侵/注入检测属恶意流量检测的车载分支）
- [[traffic-classification]]（多类/二类流量分类任务）
- [[anomaly-detection]]（恶意注入帧的相对正常帧的偏离检测）

### 9.2 相关方法

- [[convolutional-network]]（残差卷积主干 Residual Block + MaxPool2D；KAN 层为其上的可训练激活替代）

### 9.3 相关任务

- [[malicious-traffic-detection]]
- [[traffic-classification]]

### 9.4 可更新的综述页面

- [[survey-malicious-traffic-detection]]（可作为"非加密、非 IP 网络（车载 CAN 总线）恶意流量检测"的扩展条目；KB 现有综述聚焦加密网络流量）

### 9.5 可加入的对比表

- [[open-source-registry]]（开源代码：https://github.com/Anurag-Dutta/RISK-4-Auto，含代码与部分 2D 直方图数据）
- [[method-comparison-table]]（新增"流量图像化 + KAN"方法条目：RISK-4-AUTO 四变体 vs LSTMIDS/GIDS/CANIntelliIDS/DCNN/CANTransfer/RNN+Heuristics）
- [[dataset-comparison-table]]（新增 HCRL-CHD / HCRL-CAN-FD / HCRL-B-CAN 三个车载 CAN 入侵检测数据集条目，KB 首次收录）

被本文引用的 KB 内论文笔记：

- [[2019-INFOCOM-FlowPic__Encrypted_Internet_Traffic_Classification_is_as_Easy_as_Image_Recognition]]（参考文献 [26]，本文 64×64 直方图表示的源头之一；另引其期刊版 [25] 与 mini-FlowPic [27]，后两者不在 KB 内）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 全类分类三数据集最高准确率 | HCRL-CHD 0.9976（RES-KAN^II）、CAN-FD 0.9992（RES-KAN^BN/^II）、B-CAN 0.9303（RES-KAN^II） | §VI.A, Tables IV–VI |
| 平均提升口径 | 全类 1.0163%、聚焦 2.5535%（偏差 0.4596）；分数据集 +0.7576/+0.4523/+1.8398 pp | Abstract、§VI.A |
| 聚焦二分类多数达 1.0000 | DoS/Fuzzy/Gear/RPM/Flooding/Fuzzy/Malfunction/DDoS/Fuzzy 各表 | Tables VII–XV |
| 轻量档与最强档开销 | LIN-KAN CHD TTTr 620.13 s / TTTe 8.46 s；RES-KAN^II 2438.17 s / 12.01 s（LSTMIDS 2016.48 s / 9.07 s） | Table IV |
| 消融链（层配置） | Linear(×1) 0.8914 → +Residual 0.9627 → KAN-Linear(×2)+Residual(×2) 0.9976；KAN(×3)+Residual(×2) 0.9951、模型 503684 kB | Table XVI |
| KAN 超参与设计理由 | grid-size=10、spline-order=3、noise-factor=1e-2；4096 特征；1→5→25 通道扩容比 5；MaxPool 2×2 | §IV.B 末 |
| 数据集统计与采集方式 | Table I–III 消息计数；三数据集均由 OBD 口直接注入采集 | §V.A, Tables I–III |
| 训练环境 | PyTorch 2.4、16 GB 内存、i7-1065G7 @1.30 GHz、MX330 2 GiB；80:10:10 划分 | §V.B、§VI.A |
| 开源 | https://github.com/Anurag-Dutta/RISK-4-Auto（代码 + 部分 2D 直方图数据） | §V.B、参考文献 [34] |
| 表示来源 | 沿用 FlowPic（#MTU=1500）与 mini-FlowPic（64/128/256），本文取 64×64 | §III.A |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-TNSM-RISK-4-Auto__Residually_Interconnected_and_Superimposed_Kolmogorov-Arnold_Networks_for_Automotive_Network_Traffic_Classification.pdf
- MinerU Markdown：02-parsed-markdown/2026-TNSM-RISK-4-Auto__Residually_Interconnected_and_Superimposed_Kolmogorov-Arnold_Networks_for_Automotive_Network_Traffic_Classification.md

---

## 12. 后续问题

- 数据划分按会话级还是帧级？直方图按会话生成，若划分在帧级则同一会话可同时出现在训练/测试集，需核查（论文未说明）。
- 训练细节缺失：学习率、批大小、优化器、epoch 数、是否数据增强均未报告。
- Table IV 的 TTTr/TTTe 对比显示"最强模型更慢"，与摘要"significantly lower overhead"的表述存在张力；引用开销结论时应指明具体变体。
- Table XVI 出现无数据的 "Baseline Model" 行，消融链在"Residual Block (×2)"处中断；此外 LIN-KAN 体积（2435 kB）到 RES-KAN^II（96623 kB）增长 40 倍，未在正文讨论。
- §I 的论文路线图写"Section V presents the supervised framework / Section VI describes the experimental setup"，但实际 §IV 为 PROPOSED SOLUTION、§V 为 EVALUATION METHODOLOGY、§VI 为 EXPERIMENTAL RESULTS（疑为原文笔误，路线图整体错位一节）。
- Tables I–III 使用印度计数法（如 5,87,521），引用数字时注意换算为 587,521。
- 基线数值全部来自各自原文（未统一复现），跨论文比较时应标注。
- MinerU 解析质量：表格结构完整、公式（Eq. 1–5）与 Algorithm 1 可读；个别处出现 small-caps 引起的碎片（如 "I<sub>n</sub>t<sub>ro</sub>d<sub>uc</sub>ti<sub>on</sub>"）与 "$n _ { \mathrm { i n p u t } }$" 类的空格化下标，不影响理解。

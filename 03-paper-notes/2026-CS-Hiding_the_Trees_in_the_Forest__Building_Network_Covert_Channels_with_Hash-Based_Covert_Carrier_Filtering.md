---
type: paper
title_original: "Hiding the Trees in the Forest: Building Network Covert Channels with Hash-Based Covert Carrier Filtering"
title_cn: "在森林中藏树：基于哈希隐蔽载体过滤的网络隐蔽信道构建"
authors: ["Zexiao Zou", "Zhiqiang Wang", "Baoxu Liu", "Yuyang Han", "Yan Zhang"]
year: 2026
venue: "Computer & Security 2026"
doi: unknown
url: unknown
pdf: ""
mineru_md: ""
status: processed
reading_level: L2
research_area: ["network-covert-channel", "traffic-analysis", "information-hiding"]
task: ["covert-channel-construction", "covert-channel-detection-resistance"]
method: ["hash-based-filtering", "SHA-256", "SVM", "Random-Forest", "XGBoost"]
dataset: ["office-web-browsing-traffic", "video-surveillance-traffic"]
code: unknown
relevance: medium
created: 2026-06-21
updated: 2026-06-21
---

# Hiding the Trees in the Forest: Building Network Covert Channels with Hash-Based Covert Carrier Filtering

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Hiding the Trees in the Forest: Building Network Covert Channels with Hash-Based Covert Carrier Filtering |
| 中文标题 | 在森林中藏树：基于哈希隐蔽载体过滤的网络隐蔽信道构建 |
| 作者 | Zexiao Zou, Zhiqiang Wang, Baoxu Liu, Yuyang Han, Yan Zhang |
| 年份 | 2026 |
| 会议/期刊 | Computer & Security 2026 |
| 研究方向 | 网络隐蔽信道、信息隐藏 |
| 任务类型 | 隐蔽信道构建、抗检测增强 |
| 方法关键词 | SHA-256哈希过滤、密钥控制载体选择、SVM/RF/XGBoost检测对抗 |
| 数据集 | 办公网Web浏览流量（100万TCP包）、视频监控流量（160万UDP包） |
| 是否开源 | 否（Data will be made available on request） |
| PDF | - |
| MinerU Markdown | - |

---

## 1. 一句话总结

> 提出基于SHA-256哈希的隐蔽载体过滤策略，通过密钥控制的伪随机载体子集选择，将网络隐蔽信道的安全性从依赖算法保密转移到依赖密钥安全，使ML检测器的AUC从1.0降至接近0.5。

---

## 2. 摘要翻译

### 2.1 摘要原文

As an effective anti-censorship mechanism, network covert channels can provide data privacy protection and ensure communication security. However, the covertness of existing network covert channels primarily depends on the secrecy of their covert algorithms. With the increasing depth of research in this field, the difficulty of breaking such algorithms has gradually decreased. Once the algorithm is exposed, the network covert channel can be easily detected by adversaries. To address this issue, this paper proposes a covert carrier filtering strategy based on the hash. In this strategy, a key-dependent filtering rule is introduced during the construction of the network covert channel, enabling the communicating parties to randomly and dynamically filter a sparse subset from the carrier set as the covert carrier set. This strategy not only enhances the randomness of carrier selection but also tightly couples the covertness of the network covert channel with the security of the key. We employ machine learning-based traffic analysis methods to experimentally validate the strategy in two types of network covert channels: network storage and timing covert channels. The experimental results demonstrate that the proposed strategy significantly improves the detection resistance of network covert channels. When the filter key size exceeds six bits, the impact on the detection effect of the classifier becomes quite significant. Furthermore, the processing delay for a single packet is less than 8 us, indicating the feasibility of deploying the proposed strategy in high-speed network environments.

### 2.2 摘要中文翻译

网络隐蔽信道作为一种有效的反审查机制，可以提供数据隐私保护并确保通信安全。然而，现有网络隐蔽信道的隐蔽性主要依赖于其隐蔽算法的保密性。随着该领域研究的深入，破解此类算法的难度逐渐降低。一旦算法暴露，网络隐蔽信道很容易被对手检测到。为解决此问题，本文提出了一种基于哈希的隐蔽载体过滤策略。在该策略中，在网络隐蔽信道的构建过程中引入了依赖密钥的过滤规则，使通信双方能够从载体集合中随机、动态地筛选出一个稀疏子集作为隐蔽载体集。该策略不仅增强了载体选择的随机性，还将网络隐蔽信道的隐蔽性与密钥的安全性紧密耦合。我们使用基于机器学习的流量分析方法，在网络存储隐蔽信道和网络时序隐蔽信道两种类型上进行了实验验证。实验结果表明，所提策略显著提高了网络隐蔽信道的抗检测能力。当过滤密钥长度超过6位时，对分类器检测效果的影响相当显著。此外，单个数据包的处理延迟小于8微秒，表明该策略在高速网络环境中部署的可行性。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

传统网络隐蔽信道的隐蔽性依赖于隐蔽算法的保密性。随着研究积累，这些算法被逐一枚举和破解的可能性越来越高。一旦算法暴露，对手可以轻易识别隐蔽载体，从而破坏隐蔽信道。作者希望通过引入密钥控制的载体过滤机制，将安全性从"算法保密"转移到"密钥安全"，从根本上改变对抗动态。

### 3.2 现有方法的痛点和不足

| 痛点 | 具体描述 | 证据来源 |
|---|---|---|
| 算法保密性脆弱 | 现有隐蔽信道的安全性主要依赖隐蔽算法的保密性，一旦算法被破解则信道暴露 | Abstract, §1.1 |
| 固定修改模式易检测 | 传统方法对固定载体集进行一致修改，产生稳定的统计异常模式，ML分类器可轻松学习 | §1.2, §5.3 |
| 加密不能解决可检测性 | 即使加密隐蔽数据，通信行为本身的异常流量模式仍可被检测 | §1.1 (引用Iv et al., 2022) |
| 存储信道字段已被枚举 | 研究者已大量枚举可利用的协议字段，基于规则的检测日趋成熟 | §4.1 Scenario 1 |
| 时序信道固定周期性易暴露 | 固定调制模式引入异常的统计规律性，易被时间序列分析工具检测 | §4.1 Scenario 2 |

### 3.3 论文的研究假设或核心直觉

核心直觉：网络隐蔽信道使用大量数据包作为载体，每个包的隐藏容量很小。如果能从大量可用包中伪随机地选择一个子集作为隐蔽载体，即使对手截获所有流量，也难以准确指出哪些包承载了隐蔽数据。将"在森林中藏一棵树"转变为"在森林中藏一片树林的子集"。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 网络隐蔽信道的研究日益成熟，隐蔽算法被枚举和破解的风险增加 | §1.1 |
| 痛点提炼 | 算法暴露后，固定载体修改模式产生一致的统计异常，ML检测器可轻松识别 | §1.2 |
| 问题转化 | 如何在算法公开的情况下仍保持隐蔽性？——将安全性从算法保密转移到密钥安全 | §1.2 |
| 文献定位 | 已有工作关注编码机制和载体类型优化，但未从根本上解决算法暴露后的安全性问题 | §2.3 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 基于密钥的伪随机载体子集选择可以将隐蔽性与密钥安全绑定，即使算法公开也能抵抗ML检测 | 信息论分析：I(D;K|C̃) ≈ H(K) | 实验：不同L值下ML分类器的AUC |
| 辅助假设1 | 哈希函数的输入敏感性和均匀分布性适合构建密钥依赖的过滤规则 | 密码学性质推导 | 实验：过滤比例r = 1/2^L |
| 辅助假设2 | 过滤策略引入的处理开销可接受（<8μs/包），不影响实际部署 | 算法复杂度分析 | 实验：Table 5处理时间测量 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | L=6时存储信道AUC从1.0降至0.73，时序信道AUC从0.99降至0.51 | §5.3.2 Fig.6, Fig.7 |
| 辅助假设1 | 支撑 | 过滤比例严格遵循r=1/2^L，输出均匀分布 | §4.2.2 |
| 辅助假设2 | 支撑 | 单包处理时间均<8μs（存储信道~6μs，时序信道~7.5μs） | §5.3.3 Table 5 |

---

## 4. 方法设计

### 4.1 方法整体流程

将传统网络隐蔽信道的构建流程扩展为七元组模型 Ω = <C, C̃, D, K, Γ, Φ, Ψ>，在载体选择和数据嵌入之间插入密钥控制的哈希过滤步骤。CS和CR使用相同的预共享密钥和SHA-256哈希函数，对每个候选包计算哈希值，仅选择哈希值满足过滤条件的包作为隐蔽载体。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1: 预共享密钥建立 | 安全通道 | CS&CR协商Input Key + Filter Key | 共享密钥K | 为过滤提供密钥控制 |
| Step 2: 哈希计算 | 数据包载荷cᵢ + Input Key | hᵢ = SHA-256(Input Key \|\| payload) | 256位哈希值hᵢ | 生成密钥依赖的伪随机值 |
| Step 3: 载体过滤 | 哈希值hᵢ + Filter Key | (hᵢ & (2^L - 1)) == Filter Key | 隐蔽载体子集C* | 伪随机选择约1/2^L的包 |
| Step 4: 数据嵌入 | 隐蔽载体 + 隐蔽数据 | 嵌入算法（DS字段/ID字段/IPD调制） | 修改后的隐蔽载体C̃ | 在选定载体中嵌入秘密信息 |
| Step 5: 同步提取 | 接收包 + 共享密钥 | CR执行相同的哈希计算和过滤，从匹配包中提取数据 | 隐蔽数据D | 无需带内同步即可恢复数据 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 密钥协商模块 | 建立和管理预共享密钥 | 安全通道/隐蔽信道本身 | K = {Input Key, Filter Key} | 为过滤模块提供密钥输入 |
| 哈希计算模块 | 对每个包计算密钥依赖的哈希值 | 包载荷 + Input Key | 256位哈希值 | 输出给过滤决策模块 |
| 过滤决策模块 | 基于Filter Key进行比特掩码比较 | 哈希值 + Filter Key | 是否为隐蔽载体（布尔值） | 决定哪些包进入嵌入/提取模块 |
| 嵌入模块(CS) | 在隐蔽载体中嵌入数据 | 隐蔽载体 + 隐蔽数据 | 修改后的包 | 仅对过滤命中的包执行 |
| 提取模块(CR) | 从隐蔽载体中提取数据 | 接收的隐蔽载体 | 隐蔽数据D | 仅对过滤命中的包执行 |

### 4.4 公式、算法和机制解释

**核心过滤公式**：

$$r = \frac{1}{2^L}$$

其中L为Filter Key的比特长度。过滤过程等价于参数为r的伯努利试验，候选包被选为隐蔽载体的概率独立且随机。

**信息论安全性分析**：

- 传统隐蔽信道安全性：H(D|C̃) — 依赖算法保密
- 引入过滤后安全性：H(D|C̃) = H(D|C̃,K) + I(D;K|C̃)
- 当Γ具有强伪随机性时：I(D;K|C̃) ≈ H(K)
- 即使算法暴露（H(D|C̃,K)=0），安全性仍由H(K)保障

**过滤规则的三个设计要求**：
1. 密钥依赖性：Γ对K敏感
2. 输出均匀性：C̃*在C̃中均匀分布
3. 计算效率：最小化每包处理时间

### 4.5 方法优势

1. **协议无关性**：作为独立安全原语，可应用于几乎所有类型的网络隐蔽信道（存储信道和时序信道均验证有效）
2. **Kerckhoffs原则合规**：安全依赖密钥而非算法保密，符合密码学设计原则
3. **低开销**：单包处理<8μs，适合高速网络部署
4. **灵活可控**：通过调整L值精细控制隐蔽性-容量权衡
5. **无需带内同步**：CS和CR基于相同的密钥和哈希函数独立计算，天然同步

### 4.6 方法不足

1. **容量代价**：过滤比例r=1/2^L意味着容量指数级下降，L=8时仅1/256的包可用（§5.3.4 Table 6）
2. **静态参数**：当前实现使用静态密钥和固定过滤比例，长期暴露下可能被统计分析破解（§6.2）
3. **载荷修改限制**：若隐蔽信道使用载荷字段作为嵌入载体，CS和CR计算的哈希值不一致，无法直接应用（§4.2.1末段）
4. **仅考虑被动对手**：威胁模型假设对手为被动warden，未考虑主动攻击场景（§4.1）
5. **数据集有限**：仅在办公网浏览和视频监控两种流量上验证，泛化性有待进一步验证（§6.1）

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

本文方法不设计新的编码机制，而是引入一个上游的密码学驱动的过滤层，决定是否对给定包应用隐蔽数据编码。这是一个编码无关的、更底层的载体管理机制，与现有的分布式隐蔽信道（如流量分散）本质不同——后者仍是对编码模式的复杂化变体，而本文是通过放弃大多数载体的修改机会，让大量未修改的包"稀释"微观异常。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 哈希载体过滤策略 | 将密钥控制的哈希过滤引入隐蔽信道构建，将安全性从算法转移到密钥 | 高 | 是（协议无关） |
| 信息论安全性证明 | 证明I(D;K|C̃) ≈ H(K)，量化过滤策略的安全增益 | 高 | 是 |
| 双密钥设计 | Input Key（参与哈希）+ Filter Key（过滤决策）的分离设计 | 中 | 是 |
| Bernoulli试验建模 | 将过滤过程建模为参数r=1/2^L的伯努利试验，简洁刻画统计特性 | 低 | 是 |

### 5.3 适用场景

1. 需要在算法公开前提下保持安全性的隐蔽通信场景
2. 可容忍容量下降换取更高隐蔽性的场景
3. 需要在高速网络中实时部署的场景（<8μs/包）
4. 存储隐蔽信道（IP头字段修改）和时序隐蔽信道（IPD调制）

### 5.4 方法对比表

| 方法 | 哈希角色 | 过滤功能 | 隐蔽性增强机制 | 灵活性 |
|---|---|---|---|---|
| 本文方法 | 作为协议无关的过滤规则 | 是 | 密钥控制伪随机子集选择 | L可调，密钥可更新 |
| LaSPsteg (Liu et al., 2018) | 动态生成SN值集合 | 是 | 特定于LTE-A RLC/MAC层 | 领域受限 |
| DYST (Wendzel et al., 2025) | 计算哈希值匹配隐蔽数据 | 是 | 完全被动，利用已有合法流量 | 固定匹配位数 |
| Hash Chains (Keller & Wendzel, 2021) | 哈希链作为计算工具 | 否 | 一次性密码的可否认性 | 特定于OTP |
| 区块链隐蔽信道 (Wang/Ma/Partala) | 哈希值作为隐蔽载体 | 否 | 利用区块链地址的伪随机性 | 受限于区块链协议 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **硬件**：12代Intel Core i5-12400 (2.50 GHz), 64 GB RAM, Windows 10
- **软件**：Python 3.9, Scapy, Scikit-learn, dpkt
- **两个场景**：网络存储隐蔽信道（DS/ID字段嵌入）+ 网络时序隐蔽信道（IPD调制）
- **三种分类器**：SVM, Random Forest, XGBoost（参数经预实验调优）
- **Filter Key长度L**：0-8，观察不同过滤强度的效果

### 6.2 数据集

| 数据集 | 类型 | 规模 | 流量特征 | 用途 |
|---|---|---|---|---|
| 办公网Web浏览流量 | TCP/IP | 1,000,000包 | HTTP/HTTPS请求响应，完整协议字段 | 存储隐蔽信道载体 |
| 视频监控流量 | UDP/IP | 1,600,000包 | 宏观稳定但微观有抖动 | 时序隐蔽信道载体 |

每个数据集均分为两半：正常流量集（训练基线）和隐蔽流量候选集（构造隐蔽信道）。

### 6.3 Baseline

- **无过滤策略（L=0）**：传统隐蔽信道，所有候选包均用作隐蔽载体
- **正常流量基线**：分类器在纯正常流量上的表现（AUC≈0.51-0.55）
- **仅过滤延迟**：引入过滤步骤但不嵌入数据，验证过滤本身不引入异常（AUC≈0.57）

### 6.4 评价指标

| 指标类别 | 指标名称 | 含义 |
|---|---|---|
| 隐蔽性 | TPR (真正率) | 正确识别隐蔽流量的比例 |
| 隐蔽性 | FPR (假正率) | 正常流量被误判为隐蔽的比例 |
| 隐蔽性 | AUC | ROC曲线下面积，理想值趋近0.5 |
| 通信性能 | U_cc (单位隐蔽容量) | 传输1比特隐蔽数据所需的隐蔽载体数 |
| 通信性能 | t_average (平均处理时间) | 单包额外处理延迟 |
| 鲁棒性 | ETR (有效传输率) | 接收的隐蔽比特/总隐蔽比特 |
| 鲁棒性 | BER (误码率) | 错误接收的隐蔽比特/总隐蔽比特 |

### 6.5 关键实验结果

**存储隐蔽信道（Fig. 6）**：

| Filter Key长度L | SVM AUC | DT AUC | XGBoost AUC | 单位隐蔽容量U_cc | 过滤比例r |
|---|---:|---:|---:|---:|---:|
| 0（无过滤） | 1.00 | 1.00 | 1.00 | 0.125 | 100% |
| 3 | 0.99 | 0.99 | 0.99 | 1 | 12.5% |
| 5 | 0.87 | 0.87 | 0.87 | 4 | 3.125% |
| 6 | 0.73 | 0.73 | 0.73 | 8 | 1.56% |
| 7 | 0.63 | 0.63 | 0.63 | 16 | 0.78% |
| 8 | 0.59 | 0.59 | 0.59 | 32 | 0.39% |

**时序隐蔽信道（Fig. 7）**：

| Filter Key长度L | SVM AUC | XGBoost AUC | DT AUC | 单位隐蔽容量U_cc |
|---|---:|---:|---:|---:|
| 0（无过滤） | 1.00 | 1.00 | 1.00 | 2 |
| 2 | 0.87 | 0.87 | 0.87 | 2 |
| 3 | 0.59 | 0.59 | 0.59 | 2 |
| 5 | 0.53 | 0.53 | 0.53 | 2 |
| 6 | 0.51 | 0.51 | 0.51 | 60 |

**关键发现**：当L>=6时，两种信道的分类器AUC均显著下降至接近随机猜测水平（0.5），证明策略有效。

**鲁棒性验证**：在丢包率1%-20%、乱序、延迟抖动条件下，L=0和L=6的ETR和BER无显著差异，过滤策略不引入额外鲁棒性损失。

**处理时间（Table 5）**：

| 信道类型 | 无策略嵌入 | 仅过滤 | L=1嵌入 | L=6嵌入 | L=8嵌入 |
|---|---:|---:|---:|---:|---:|
| 存储信道 | 4.1 μs | 4.11 μs | 6.48 μs | 5.78 μs | 5.75 μs |
| 时序信道 | 0.78 μs | 7.44 μs | 7.87 μs | 7.63 μs | 7.63 μs |

### 6.6 优势最明显的场景

1. **L=6-8的存储隐蔽信道**：AUC从1.0降至0.59-0.73，容量代价可接受（U_cc=8-32）
2. **L=5-6的时序隐蔽信道**：AUC从0.99降至0.51-0.53，且时序信道的U_cc不随L变化（始终为2），代价更小
3. **高速网络实时部署**：单包<8μs的处理开销几乎不影响吞吐

### 6.7 局限性

1. 容量-隐蔽性权衡：高L值下容量指数级下降（存储信道L=8时U_cc=32，即每32个隐蔽载体才能传1比特）
2. 仅验证了两种流量类型（办公网+监控），未覆盖IoT、工业控制等场景
3. 静态密钥和固定过滤比例，长期部署存在被统计分析风险
4. 对使用载荷字段作为嵌入载体的隐蔽信道不适用
5. 威胁模型仅考虑被动对手

---

## 7. 学习与应用

### 7.1 是否开源？

否。作者声明"Data will be made available on request"。

### 7.2 复现关键步骤

1. 使用Scapy捕获真实网络流量（TCP和UDP），分别作为存储和时序信道的载体
2. 实现SHA-256哈希过滤：对每个包计算Hash(Input Key || payload)，用Filter Key进行比特掩码比较
3. 在DS/ID字段嵌入8比特数据（存储信道）或通过IPD调制编码1比特（时序信道，base_interval=5ms）
4. 提取KDE/Cv/H/R(τ)特征（存储信道）或D/Reg/H/CCE特征（时序信道）
5. 训练SVM/RF/XGBoost分类器，比较不同L值下的AUC

### 7.3 关键超参数、预处理和训练细节

| 参数 | 值 | 说明 |
|---|---|---|
| 哈希函数 | SHA-256 | 256位输出，强碰撞抗性 |
| Filter Key长度L | 0-8 | 控制过滤比例r=1/2^L |
| Input Key | >=128位 | 推荐最小长度 |
| 时序信道base_interval | 5ms | IPD调制基准间隔 |
| 时间窗口 | 1000包 | 时序特征提取的滑动窗口 |
| 分类器参数 | 预实验调优 | 未详细说明具体参数 |

### 7.4 能否迁移到其他任务？

- **正向迁移**：该策略是协议无关的过滤原语，理论上可应用于任何基于包的隐蔽信道（DNS隐蔽信道、ICMP隐蔽信道等）
- **与[[tunnel-detection]]的关联**：过滤后的隐蔽流量统计特征趋近正常流量，可能使现有隧道检测方法失效
- **与[[encrypted-traffic-analysis]]的关联**：加密流量中的隐蔽信道检测是更具挑战性的场景，本文方法可能进一步增加检测难度
- **与[[anomaly-detection]]的关联**：稀释策略本质上是利用大量正常样本掩盖少量异常样本，对基于统计分布的异常检测构成挑战

### 7.5 对我的研究有什么启发？

1. **检测侧视角**：需要研究针对稀疏隐蔽载体的检测方法，不能仅依赖全局统计特征
2. **特征工程启示**：传统特征（KDE/Cv/H/自相关）在L>=6时失效，需要探索更细粒度的特征
3. **对抗性思维**：隐蔽信道研究和检测研究是猫鼠游戏，需要从对手角度思考检测策略的脆弱性
4. **容量-安全权衡**：这一思想可推广到其他安全增强场景

---

## 8. 总结

### 8.1 核心思想

> 密钥控制的哈希过滤实现伪随机载体稀疏化。

### 8.2 速记版 Pipeline

1. CS&CR预共享密钥K = {Input Key, Filter Key}
2. 对每个候选包计算h = SHA-256(Input Key || payload)
3. 若(h & (2^L-1)) == Filter Key，则选为隐蔽载体
4. CS在隐蔽载体中嵌入数据并发送
5. CR执行相同过滤和提取，无需带内同步

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[tunnel-detection]] — 本文过滤策略可能使基于统计特征的隧道检测方法失效
- [[encrypted-traffic-analysis]] — 加密流量中隐蔽信道的检测更具挑战
- [[anomaly-detection]] — 稀疏载体选择策略对抗基于分布的异常检测
- [[traffic-classification]] — 隐蔽信道流量与正常流量的分类边界模糊化

### 9.2 相关方法

- [[traffic-classification]] — 本文使用SVM/RF/XGBoost作为检测对手进行评估

### 9.3 相关任务

- [[tunnel-detection]] — 隐蔽信道检测是隧道检测的子任务
- [[anomaly-detection]] — 隐蔽流量本质上是异常流量的特殊形式

### 9.4 可更新的综述页面

- [[encrypted-traffic-analysis]] — 可将本文作为隐蔽信道抗检测策略的案例补充

### 9.5 可加入的对比表

- [[tunnel-detection]] — 隐蔽信道检测方法对比表

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 算法保密性是传统隐蔽信道的核心弱点 | "the covertness of existing network covert channels primarily depends on the secrecy of their covert algorithms" | Abstract |
| L=6是隐蔽性显著提升的阈值 | "When the filter key size exceeds six bits, the impact on the detection effect of the classifier becomes quite significant" | Abstract |
| 单包处理<8μs | "the processing delay for a single packet is less than 8 μs" | Abstract |
| 过滤比例严格遵循r=1/2^L | "r = 1/2^L" | §4.2.2 Eq.4 |
| 信息论安全性证明 | "I(D;K|C̃) ≈ H(K)" | §3.2 Eq.3 |
| 存储信道L=6时AUC=0.73 | Fig.6数据 | §5.3.2 |
| 时序信道L=5时AUC<0.6 | "When the L=5, the AUC of all three classifiers drops below 0.6" | §5.3.2 |
| 过滤策略不影响鲁棒性 | "no significant differences are observed in either ETR or BER before and after introducing the filtering strategy" | §5.3.1 |
| 载荷修改场景不适用 | "modifying the payload will cause the hash values calculated by the CS&CR to be inconsistent" | §4.2.1 |
| 静态参数是已知局限 | "Our implementation adopts a static key and a fixed filtering ratio" | §6.2 |

---

## 11. 原始资料链接

- PDF：-
- MinerU Markdown：-

---

## 12. 后续问题

1. 如何设计针对稀疏隐蔽载体的检测特征？传统全局统计特征在L>=6时失效
2. 自适应过滤比例（基于强化学习动态调整L）能否在保持隐蔽性的同时最大化容量？
3. 在加密流量（如TLS/QUIC）场景下，哈希过滤策略是否仍然有效？
4. 主动对手（可注入或修改流量的warden）能否通过操纵包载荷破坏CS&CR的哈希同步？
5. 该策略与现有隐蔽信道编码模式（PT1, PS1, PS3等）的具体组合效果如何？

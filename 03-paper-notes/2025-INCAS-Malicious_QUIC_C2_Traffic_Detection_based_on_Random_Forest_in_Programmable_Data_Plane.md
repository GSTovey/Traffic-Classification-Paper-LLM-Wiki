---
type: paper
title_original: "Malicious QUIC C2 Traffic Detection based on Random Forest in Programmable Data Plane"
title_cn: "基于可编程数据平面随机森林的恶意 QUIC C2 流量检测"
authors: ["Yuqin Hong", "Yi Bai", "Xiaoquan Zhang", "Lin Cui"]
year: 2025
venue: "ACM INCAS 2025 (CoNEXT Workshop)"
doi: "10.1145/3769699.3771588"
url: unknown
pdf: "00-inbox/PDFs/2025-INCAS-Malicious_QUIC_C2_Traffic_Detection_based_on_Random_Forest_in_Programmable_Data_Plane.pdf"
mineru_md: "02-parsed-markdown/2025-INCAS-Malicious_QUIC_C2_Traffic_Detection_based_on_Random_Forest_in_Programmable_Data_Plane.md"
status: processed
reading_level: L2
research_area: ["network security", "encrypted traffic analysis", "programmable data plane"]
task: ["C2 detection", "malicious traffic classification", "real-time inference"]
method: ["random forest", "decision tree", "in-band network telemetry (INT)", "P4 programmable switch", "match-action table"]
dataset: ["NetFlow-QUIC (Google)", "Merlin C2 synthetic traffic"]
code: unknown
relevance: medium
created: "2026-05-27"
updated: "2026-05-27"
---

# Malicious QUIC C2 Traffic Detection based on Random Forest in Programmable Data Plane

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Malicious QUIC C2 Traffic Detection based on Random Forest in Programmable Data Plane |
| 中文标题 | 基于可编程数据平面随机森林的恶意 QUIC C2 流量检测 |
| 作者 | Yuqin Hong, Yi Bai, Xiaoquan Zhang, Lin Cui |
| 年份 | 2025 |
| 会议/期刊 | ACM CoNEXT Workshop on In-Network Computing and AI for Distributed Systems (INCAS '25) |
| 研究方向 | 网络安全、加密流量分析、可编程数据平面 |
| 任务类型 | QUIC 协议中 C2 (Command-and-Control) 恶意流量的实时检测 |
| 方法关键词 | Random Forest, P4 programmable switch, in-band network telemetry (INT), match-action table, decision tree pruning |
| 数据集 | Google NetFlow-QUIC 公开数据集（良性流量）+ Merlin C2 框架合成的恶意流量 |
| 是否开源 | 否 |
| PDF | 00-inbox/PDFs/2025-INCAS-Malicious_QUIC_C2_Traffic_Detection_based_on_Random_Forest_in_Programmable_Data_Plane.pdf |
| MinerU Markdown | 02-parsed-markdown/2025-INCAS-Malicious_QUIC_C2_Traffic_Detection_based_on_Random_Forest_in_Programmable_Data_Plane.md |

## 1. 一句话总结

> 在 P4 可编程交换机上部署轻量级 Random Forest 分类器，结合 INT 内网遥测特征，在微秒级延迟下实现对加密 QUIC 流量中 C2 恶意流量的实时检测，服务器端准确率 99.83%，交换机端准确率 82.1%。

## 2. 摘要翻译

### 2.1 摘要原文

The widespread adoption of QUIC, an encrypted transport protocol, presents novel challenges for network security. Its underlying UDP-based connectionless design, full encryption, and multiplexed streams hinder traditional Deep Packet Inspection (DPI) and behavior-based detection methods. At the same time, Command-and-Control (C2) channels increasingly adopt QUIC to evade detection in advanced persistent threat (APT) attacks. This paper presents a real-time C2 detection framework built on programmable data planes and lightweight Random Forest classifiers. By embedding in-network telemetry (INT) metadata and compiling trained models into switch-executable rule tables, the proposed system enables near-source malicious flow detection at microsecond latency. We demonstrate the feasibility of deploying decision-tree-based inference within resource-constrained P4 switches, achieving 99.83% detection accuracy on server-based training and 82.1% on programmable hardware, with a 2–3 orders of magnitude reduction in inference latency. Our findings outline a novel design space for encrypted traffic inspection under performance and scalability constraints.

### 2.2 摘要中文翻译

QUIC 加密传输协议的广泛采用给网络安全带来了新挑战。其基于 UDP 的无连接设计、全加密和多路复用流机制阻碍了传统深度包检测 (DPI) 和基于行为的检测方法。与此同时，C2 (Command-and-Control) 通道越来越多地采用 QUIC 来规避高级持续性威胁 (APT) 攻击中的检测。本文提出一种基于可编程数据平面和轻量级 Random Forest 分类器的实时 C2 检测框架。通过嵌入 INT (In-band Network Telemetry) 元数据并将训练好的模型编译为交换机可执行的规则表，系统实现了近源微秒级延迟的恶意流检测。我们验证了在资源受限的 P4 交换机上部署基于决策树的推理的可行性，在服务器端训练达到 99.83% 的检测准确率，在可编程硬件上达到 82.1%，推理延迟降低了 2-3 个数量级。研究结果为性能和可扩展性约束下的加密流量检测开辟了新的设计空间。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- QUIC 协议加密了 payload 和大部分 header 字段，使得传统 DPI 方法（如 Snort、Suricata）完全失效
- C2 通道利用 QUIC 的加密会话和持久连接建立隐蔽通信隧道，传统基于 TCP 的流特征检测方法无法适用
- 深度学习方法虽然在加密流量分析中有前景，但计算复杂度高、内存占用大，不适合直接部署在资源受限的可编程数据平面设备上
- 需要一种轻量级、可解释的模型，能在交换机转发平面上以线速执行推理

### 3.2 现有方法的痛点和不足

| 现有方法 | 痛点 |
|---|---|
| DPI（Snort, Suricata） | 对 QUIC 加密流量完全无效，无法访问 payload |
| 基于流指纹的方法 | QUIC 的混淆流量结构导致准确率下降 |
| 深度学习方法（CNN/LSTM） | 计算复杂度高、内存占用大，不适合交换机部署 |
| 同态加密 (HE) | 性能开销大，不适用于实时加密流量检测 |
| 服务器端离线检测 | 引入额外延迟，无法实现近源实时检测 |

### 3.3 论文的研究假设或核心直觉

- **核心假设**：即使 QUIC 流量被全加密，通过 INT 注入的网络遥测元数据（逐跳延迟、丢包率、端口利用率等）仍能揭示 C2 流量的隐蔽行为模式
- **关键直觉**：C2 流量通常表现出周期性低频"心跳"信号和突发数据外泄的模式，这种不规则的 bursty 行为会导致包间到达时间和交换机处理延迟的波动，与正常的会话型良性 QUIC 流量有明显差异
- Random Forest 的决策树结构可以被编译为 P4 交换机的 match-action table，实现线速推理

## 4. 方法设计

### 4.1 方法整体流程

1. **数据采集**：良性流量来自 Google NetFlow-QUIC 数据集，恶意 C2 流量通过 Merlin C2 框架在虚拟环境中合成生成
2. **INT 增强**：P4 交换机注入遥测 header，采集队列深度、逐跳延迟、丢包等元数据，与流记录合并
3. **特征工程**：提取 13 个量化特征，涵盖延迟特征、流量统计和设备负载指标三个维度
4. **模型训练**：使用 scikit-learn 的 RandomForestClassifier 训练，Gini impurity 作为分裂准则
5. **模型嵌入**：对决策树剪枝、特征选择后，将模型编译为 P4 交换机的 match-action table
6. **交换机推理**：在可编程交换机上执行实时分类，实现微秒级延迟的近源检测

### 4.2 详细 Pipeline（表格形式）

| 步骤 | 描述 | 技术细节 |
|---|---|---|
| 1. 流量生成 | 良性流量从 Google NetFlow-QUIC 获取，恶意流量用 Merlin C2 合成 | Kali Linux 上搭建攻击者和受害者节点，QUIC 端口 443，Wireshark 抓包 |
| 2. INT 注入 | P4 交换机注入遥测 header | 采集 queue depth, hop-level latency, packet loss，用 timestamp 和 identifier 对齐合并 |
| 3. 数据清洗 | pcap 文件清洗转换为 csv | 去噪、去重，合并网络层设备指标和应用层流量行为 |
| 4. 特征提取 | 提取 13 个特征 | 3 个维度：delay-based、traffic statistics、device load indicators |
| 5. 特征展平 | 3D 时间序列张量 [T, N, d] 展平为 2D 矩阵 [T x N, d] | 时间切片保留时序模式 |
| 6. 模型训练 | 分层 80/20 训练测试集划分 | RandomForestClassifier, Gini impurity, 交叉验证防过拟合 |
| 7. 树剪枝 | 用 Gini importance 和互信息筛选特征 | 阈值 < 0.05 的低影响特征被丢弃 |
| 8. 表生成 | 特征值范围编码为 ternary match-action table | 叶子决策编码为输出动作，多数投票机制模拟 |
| 9. P4 编译 | 模型编译为 P4 match-action 范式 | 路径编码技术，规则复杂度从 O(2^D) 降至 O(L) |
| 10. 部署推理 | 交换机上实时分类 | 两个 pipeline stage：特征提取 + 路径编码分类 |

### 4.3 模型结构或系统模块（表格形式）

| 模块 | 功能 | 输入 | 输出 |
|---|---|---|---|
| 训练模块 (Training Module) | 收集良性和恶意 QUIC 流量，提取 INT 元数据，训练 Random Forest | 良性/恶意 QUIC 流量 | 训练好的分类器 |
| 模型嵌入模块 (Model Embedding Module) | 剪枝、优化、编译为交换机可执行 match-action table | 训练好的模型 | P4 match-action table |
| 流量分类模块 (Traffic Classification Module) | 在可编程交换机上执行实时分类和缓解 | 流元数据 | 分类结果（良性/C2） |

### 4.4 公式、算法和机制解释

**Random Forest 训练**：
- 使用 scikit-learn 的 RandomForestClassifier
- 分裂准则：Gini impurity [22]
- 特征采样：每个分裂点使用 sqrt(d) 个特征（d 为总特征数）
- 并行训练：使用 joblib 并行训练多棵树

**路径编码 (Path Encoding)**：
- 受 Planter [20] 启发，将决策树的根到叶子节点路径编码为唯一码（如 '00', '01'）
- 规则复杂度从 O(2^D) 降至 O(L)，其中 D 为树深度，L 为有效叶子节点数
- 每棵树的决策路径被编译为 match-action table 中的一条规则

**模型部署**：
- 每个交换机部署 5 棵决策树，在内存使用和检测准确率之间取得平衡
- 占用两个 pipeline stage：一个用于特征提取，一个用于路径编码和分类
- 通过并行 table lookup 模拟多数投票机制

**特征选择策略**：
- 结合 Gini importance 和 mutual information score 两种方法
- 丢弃重要性分数低于 0.05 的特征
- 延迟特征和端口利用率对分类贡献最大

**关键机制解释**：
- **INT 增强**：通过内网遥测获取加密流量中不可见的微秒级行为特征，弥补 payload 加密带来的信息损失
- **路径编码**：将决策树逻辑压缩为紧凑表示，使其能适配 P4 交换机有限的 match-action table 资源
- **时间切片展平**：保留时序模式的同时将 3D 张量降为 2D 矩阵，适配 Random Forest 输入格式

### 4.5 方法优势

1. **微秒级推理延迟**：交换机端推理延迟约 0.5 us，比服务器端（约 100 us）降低 2-3 个数量级
2. **无需 payload 检查**：依赖 INT 元数据和流统计特征，对加密流量有效
3. **近源检测**：检测逻辑嵌入转发平面，在流量进入网络时即完成分类
4. **轻量级模型**：Random Forest 可分解为独立决策树，适合资源受限的 P4 交换机部署
5. **可解释性**：决策树结构清晰，每个分类决策可追溯到具体的特征路径

### 4.6 方法不足

1. **交换机端准确率损失**：从服务器端 99.83% 降至交换机端 82.1%，下降幅度显著（约 17.7%）
2. **合成数据局限**：恶意流量由 Merlin C2 单一框架生成，代表性有限
3. **特征依赖 INT**：需要 P4 交换机支持 INT 注入，部署前提条件较高
4. **模型更新机制缺失**：论文未提出自动化的模型更新方案以适应演变的威胁行为
5. **单一 C2 工具**：仅使用 Merlin C2 进行实验，未验证对其他 C2 工具的泛化能力
6. **BMv2 仿真局限**：使用软件交换机模型 (BMv2) 进行延迟测量，不适用于精确的纳秒级性能基准测试

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 对比维度 | 传统 DPI | 本文方法 (IDRF) |
|---|---|---|
| 分析层面 | 应用层 payload | INT 元数据 + 流统计特征 |
| 对加密流量 | 完全无效 | 有效 |
| 部署位置 | 服务器端 | 可编程交换机数据平面 |
| 推理延迟 | 毫秒级（服务器处理） | 微秒级（线速匹配） |
| 模型类型 | 规则/签名匹配 | Random Forest 机器学习 |

与已有机器学习检测方法的本质区别在于：本文将模型部署在**可编程数据平面**（P4 交换机）而非服务器端，通过 INT 获取加密流量中的隐藏行为特征，并将决策树编译为 match-action table 实现线速推理。

### 5.2 创新点分析（表格形式）

| 创新点 | 说明 |
|---|---|
| IDRF 框架 | 提出 INT-enhanced Decision-tree Random Forest 框架，将 INT 元数据与 Random Forest 结合用于 QUIC C2 检测 |
| INT 特征工程 | 利用内网遥测注入微秒级延迟、丢包、端口利用率等特征，弥补加密流量 payload 信息的缺失 |
| 模型编译为 match-action table | 将训练好的 Random Forest 编译为 P4 交换机可执行的规则表，实现数据平面推理 |
| 路径编码技术 | 受 Planter 启发，将决策路径编码为紧凑表示，规则复杂度从 O(2^D) 降至 O(L) |
| 端到端系统验证 | 从服务器训练到交换机部署的完整流程验证，证明了在资源受限设备上实现实时加密流量检测的可行性 |

### 5.3 适用场景

- 企业网络中检测利用 QUIC 协议进行 C2 通信的 APT 攻击
- 需要近源实时检测的高性能网络环境（微秒级延迟要求）
- 加密流量无法使用传统 DPI 的场景
- 需要在网络基础设施层面（而非端点）部署安全检测的场景

### 5.4 方法对比表

| 方法 | 是否处理加密流量 | 部署位置 | 推理延迟 | 检测准确率 | 模型复杂度 |
|---|---|---|---|---|---|
| DPI (Snort, Suricata) | 否 | 服务器 | 毫秒级 | 不适用 | 低 |
| FP-RF (服务器端 RF) | 是 | 服务器 | 百微秒级 | 100% | 中 |
| FP-DT (服务器端 DT) | 是 | 服务器 | 百微秒级 | 98% | 低 |
| FP-KNN | 是 | 服务器 | 百微秒级 | 100% | 中 |
| FP-SVM | 是 | 服务器 | 百微秒级 | 75% | 中 |
| FP-AdaBoost | 是 | 服务器 | 百微秒级 | 75% | 中 |
| FP-MLP | 是 | 服务器 | 百微秒级 | 80% | 高 |
| **IDRF (本文)** | **是** | **P4 交换机** | **~0.5 us** | **82.1% (交换机) / 99.83% (服务器)** | **低** |

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **训练环境**：Windows Server 2019, Intel Xeon E5-2620 v3 (2.40GHz, 6 cores), 64GB RAM
- **网络仿真**：Ubuntu 20.04.6 LTS, Linux kernel 5.15.0, Mininet 2.2.2
- **交换机**：P4 Behavioral Model v2 (BMv2), P4_16 语言, V1Model 架构
- **C2 模拟**：Kali Linux 上搭建 Merlin C2 服务器，攻击者通过 QUIC (端口 443) 发起命令和文件传输
- **自动化**：Wireshark 抓包 + Pexpect 自动化脚本
- **模型训练**：Python + scikit-learn, 固定随机种子保证可复现性

### 6.2 数据集

| 数据集 | 来源 | 用途 |
|---|---|---|
| 良性 QUIC 流量 | Google NetFlow-QUIC 公开数据集 | 正样本 |
| 恶意 C2 流量 | Merlin C2 框架在虚拟环境合成 | 负样本 |
| INT 元数据 | P4 交换机注入 | 特征增强 |

### 6.3 Baseline

论文与 6 种传统机器学习模型进行了对比，均使用相同特征但不包含 INT 增强：

| Baseline | 说明 |
|---|---|
| FP-RF | 标准 Random Forest（无 INT） |
| FP-DT | 单决策树（无 INT） |
| FP-KNN | K-Nearest Neighbor（无 INT） |
| FP-SVM | Support Vector Machine（无 INT） |
| FP-MLP | Multilayer Perceptron（无 INT） |
| FP-AdaBoost | AdaBoost 集成方法（无 INT） |

### 6.4 评价指标

- **Accuracy（准确率）**：正确分类的样本比例
- **Precision（精确率）**：预测为 C2 的样本中真正 C2 的比例
- **Recall（召回率）**：实际 C2 样本中被正确检测的比例
- **F1 Score**：精确率和召回率的调和平均
- **Inference Latency（推理延迟）**：从输入特征到输出分类结果的时间

### 6.5 关键实验结果（表格形式）

**服务器端性能对比（有 INT 增强）**：

| 模型 | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|
| FP-RF (无 INT) | 100% | 100% | 100% | 100% |
| IDRF (有 INT) | 100% | 100% | 100% | 100% |
| FP-DT (无 INT) | 98% | 97% | 96% | 95% |
| IDRF (有 INT) | 99% | 98% | 97% | 94% |
| FP-KNN (无 INT) | 100% | 100% | 100% | 100% |
| IDRF (有 INT) | 100% | 100% | 100% | 100% |
| FP-SVM (无 INT) | 75% | 85% | 80% | 75% |
| IDRF (有 INT) | 98% | 98% | 98% | 92% |
| FP-AdaBoost (无 INT) | 75% | 80% | 75% | 75% |
| IDRF (有 INT) | 98% | 75% | 75% | 75% |
| FP-MLP (无 INT) | 80% | 85% | 85% | 85% |
| IDRF (有 INT) | 99% | 99% | 99% | 78% |

**IDRF 服务器端综合性能**：Accuracy 99.83%, F1 Score 99.75%

**交换机端性能**：

| 配置 | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|
| 有 INT | 82.1% | 82.18% | 82.1% | 81.9% |
| 无 INT | 9.6% | 9.9% | 13.9% | 12.1% |

**INT 影响**：加入 INT 特征后，交换机端准确率从 9.6% 大幅提升至 82.1%

**模型架构对比（交换机端）**：

| 模型 | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|
| Random Forest | 82.1% | 82.18% | 82.1% | 81.9% |
| Decision Tree | 80.94% | 80.66% | 80.94% | 80.84% |

Random Forest 比单决策树准确率高约 4.7%

**推理延迟对比**：

| 部署方式 | 延迟 |
|---|---|
| 可编程交换机 | ~0.5 us |
| 远程服务器 | ~100 us |

### 6.6 优势最明显的场景

- **INT 特征增益显著**：无 INT 时交换机端准确率仅 9.6%，有 INT 后提升至 82.1%，说明 INT 对加密流量检测至关重要
- **SVM/AdaBoost 替代场景**：对于 SVM 和 AdaBoost 等模型，IDRF 的优势最为明显（从 75% 提升至 98%）
- **延迟优势**：推理延迟降低 2-3 个数量级，适合高速网络的实时检测需求

### 6.7 局限性

1. **服务器端 vs 交换机端性能差距大**：准确率从 99.83% 降至 82.1%，下降约 17.7 个百分点
2. **合成数据**：恶意流量仅由 Merlin C2 生成，缺乏真实世界的 APT 攻击流量
3. **INT 依赖**：无 INT 特征时交换机端准确率仅 9.6%，说明方法强依赖 INT 基础设施
4. **单一 C2 工具**：未验证对 Cobalt Strike、Metasploit 等其他 C2 工具的泛化能力
5. **BMv2 限制**：软件交换机模型不等于真实硬件，实际 ASIC 交换机的性能可能有差异
6. **缺乏对抗性评估**：未考虑攻击者主动规避检测的场景

## 7. 学习与应用

### 7.1 是否开源？

否。论文未提供代码或开源实现。

### 7.2 复现关键步骤

1. **搭建网络仿真环境**：Ubuntu 20.04 + Mininet 2.2.2 + P4 BMv2
2. **生成良性流量**：从 Google Drive 下载 NetFlow-QUIC 数据集
3. **生成恶意流量**：在 Kali Linux 上部署 Merlin C2 服务器，用 Pexpect 自动化攻击交互
4. **INT 注入**：配置 P4 交换机注入 INT header，采集延迟、丢包、利用率元数据
5. **特征提取**：清洗 pcap 文件，提取 13 个特征，转换为 csv 格式
6. **模型训练**：使用 scikit-learn RandomForestClassifier，80/20 分层划分，网格搜索调参
7. **模型剪枝**：用 Gini importance 和互信息筛选特征，阈值 0.05
8. **P4 编译**：将决策树编译为 match-action table，使用路径编码技术
9. **交换机部署**：在 BMv2 上部署 P4 程序，注入测试流量验证

### 7.3 关键超参数、预处理和训练细节

| 参数 | 值/说明 |
|---|---|
| 分类器 | RandomForestClassifier (scikit-learn) |
| 分裂准则 | Gini impurity |
| 特征采样 | sqrt(d) 个特征（d 为总特征数） |
| 数据划分 | 分层 80/20 train-test split |
| 交叉验证 | 使用，防过拟合 |
| 特征选择阈值 | Gini importance / mutual information < 0.05 |
| 部署树数量 | 每交换机 5 棵决策树 |
| Pipeline stage | 2 个（特征提取 + 路径编码分类） |
| 特征数量 | 13 个（3 个维度） |
| 展平方式 | 3D [T, N, d] -> 2D [T x N, d] 时间切片 |
| P4 语言版本 | P4_16 |
| 目标架构 | V1Model |

### 7.4 能否迁移到其他任务？

- **其他加密协议检测**：方法思路（INT + 轻量级 ML + 数据平面部署）可迁移到 TLS/HTTPS、DNS-over-HTTPS 等加密协议的异常检测
- **其他 C2 工具检测**：需要扩展训练数据，但框架结构不变
- **DDoS 检测**：Random Forest 已广泛用于 DDoS 检测，可考虑将模型编译到交换机上
- **Heavy hitter 检测**：作者团队之前有 pHeavy [15] 的工作，可结合 INT 特征进一步优化
- **其他可编程硬件**：方法不限于 P4 交换机，可扩展到 SmartNIC、FPGA 等可编程硬件平台

### 7.5 对我的研究有什么启发？

1. **INT 作为加密流量的"透视镜"**：即使 payload 全加密，INT 注入的网络层元数据（延迟、丢包、利用率）仍能提供有价值的分类信号
2. **模型-硬件协同设计**：不是先训练模型再部署，而是从一开始就考虑硬件约束（match-action table），选择 Random Forest 这种可分解的模型
3. **路径编码思路**：将决策树逻辑压缩为 match-action table 的路径编码技术，规则复杂度优化的思路值得借鉴
4. **近源检测范式**：在转发平面完成检测，避免将流量牵引到服务器的额外延迟，适合高性能网络
5. **特征重要性分析**：延迟特征和端口利用率对 C2 检测贡献最大，说明 C2 流量的时间行为模式是关键区分信号
6. **性能与准确率的权衡**：交换机端 82.1% vs 服务器端 99.83% 的差距表明，资源受限环境下的模型压缩仍需进一步研究

## 8. 总结

### 8.1 核心思想（不超过20字）

在 P4 交换机上用 Random Forest + INT 实时检测加密 QUIC C2 流量。

### 8.2 速记版 Pipeline（3-5步）

1. 采集良性/恶意 QUIC 流量，通过 P4 交换机注入 INT 元数据
2. 提取 13 个延迟、流量统计和设备负载特征
3. 训练 Random Forest 分类器，剪枝后编译为 P4 match-action table
4. 在可编程交换机上部署，实现微秒级实时 C2 检测

## 9. Obsidian 知识链接

### 9.1 相关概念

- QUIC Protocol - QUIC 传输协议
- Command and Control (C2) - 命令与控制通道
- Advanced Persistent Threat (APT) - 高级持续性威胁
- Programmable Data Plane - 可编程数据平面
- In-band Network Telemetry (INT) - 内网遥测
- P4 Programming Language - P4 编程语言
- Encrypted Traffic Analysis - 加密流量分析

### 9.2 相关方法

- Random Forest Classifier - 随机森林分类器
- Decision Tree - 决策树
- Match-Action Table - 匹配-动作表
- Gini Impurity - Gini 不纯度
- Path Encoding for Decision Trees - 决策树路径编码
- Planter Framework - Planter 框架（模型编译参考）

### 9.3 相关任务

- C2 Traffic Detection - C2 流量检测
- Encrypted Traffic Classification - 加密流量分类
- Real-time Intrusion Detection - 实时入侵检测
- Network Function Virtualization - 网络功能虚拟化
- In-Network Machine Learning - 网内机器学习

### 9.4 可更新的综述页面

- Encrypted Traffic Classification Survey
- Programmable Data Plane Applications
- ML-based Intrusion Detection Systems

### 9.5 可加入的对比表

- Encrypted Traffic Classification Methods
- C2 Detection Methods Comparison
- In-Network ML Deployment Approaches

## 10. 证据记录（表格形式）

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E1 | 实验结果 | IDRF 服务器端准确率 99.83%, F1 99.75% | Section 4.2 |
| E2 | 实验结果 | IDRF 交换机端准确率 82.1%（有 INT），无 INT 仅 9.6% | Section 4.3, Figure 5 |
| E3 | 实验结果 | Random Forest 比单决策树准确率高约 4.7% | Section 4.3, Figure 6 |
| E4 | 实验结果 | 交换机推理延迟 ~0.5 us，服务器 ~100 us，降低 2-3 个数量级 | Section 4.4, Figure 7 |
| E5 | 实验结果 | FP-SVM 在无 INT 时仅 75% 准确率，IDRF 达 98% | Section 4.2, Figure 3d |
| E6 | 特征分析 | switch_processing_delay (Gini 0.19) 和 iat_a_b_max (Gini 0.17) 为最重要特征 | Section 4.3, Figure 4 |
| E7 | 方法设计 | 每交换机部署 5 棵决策树，占用 2 个 pipeline stage | Section 3.3 |
| E8 | 方法设计 | 路径编码规则复杂度从 O(2^D) 降至 O(L) | Section 3.3 |
| E9 | 数据集 | 良性流量来自 Google NetFlow-QUIC，恶意流量由 Merlin C2 合成 | Section 4.1 |
| E10 | 特征工程 | 13 个特征涵盖 3 个维度：delay-based, traffic statistics, device load | Section 3.2, Table 1 |

## 11. 原始资料链接

- 论文发表于 ACM INCAS '25 (CoNEXT Workshop), December 1-4, 2025, Hong Kong
- DOI: https://doi.org/10.1145/3769699.3771588
- 作者单位：Jinan University (暨南大学), Guangzhou, China
- 通讯作者：Lin Cui (tcuilin@jnu.edu.cn)
- 基金资助：National Natural Science Foundation of China (NSFC), Grant 62172189
- NetFlow-QUIC 数据集：https://drive.google.com/drive/folders/1cwHhzvaQbi-ap8yfrj2vHyPmUTQhaYOj
- Merlin C2 (QUIC release): https://github.com/Ne0nd0g/merlin/releases/tag/v0.6.0
- 相关工作：Planter [20], pHeavy [15], OffsetINT [8]

## 12. 后续问题

1. **泛化能力**：框架对其他 C2 工具（如 Cobalt Strike、Metasploit）和真实世界 QUIC 数据集的表现如何？论文将此列为 future work
2. **模型自动更新**：如何在数据平面中实现模型的自动化更新以适应演变的威胁行为？论文提到计划探索此方向
3. **服务器端与交换机端的性能差距**：准确率从 99.83% 降至 82.1% 的根本原因是什么？是特征损失、模型压缩还是硬件限制？
4. **对抗性攻击**：如果攻击者了解检测机制，主动调整 C2 流量模式以模仿良性流量，该方法是否仍然有效？
5. **真实硬件验证**：在 ASIC 交换机（如 Tofino）上部署时，实际性能和资源占用如何？
6. **INT 部署成本**：INT 需要网络中所有交换机支持，这在实际部署中的可行性和成本如何？
7. **多分类扩展**：能否在检测 C2 的基础上进一步识别具体的 C2 工具类型或攻击阶段？
8. **与其他加密协议的兼容性**：该方法在 TLS 1.3、WireGuard 等其他加密协议上的表现如何？

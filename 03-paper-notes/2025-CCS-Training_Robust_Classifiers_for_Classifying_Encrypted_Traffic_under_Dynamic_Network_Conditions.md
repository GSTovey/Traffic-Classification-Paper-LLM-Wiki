---
type: paper
title_original: "Training Robust Classifiers for Classifying Encrypted Traffic under Dynamic Network Conditions"
title_cn: "动态网络条件下加密流量分类的鲁棒分类器训练"
authors:
  - Yuqi Qing
  - Qilei Yin
  - Xinhao Deng
  - Xiaoli Zhang
  - Peiyang Li
  - Zhuotao Liu
  - Kun Sun
  - Ke Xu
  - Qi Li
year: 2025
venue: "CCS"
doi: "10.1145/3719027.3765073"
url: ""
pdf: "00-inbox/PDFs/2025-CCS-Training_Robust_Classifiers_for_Classifying_Encrypted_Traffic_under_Dynamic_Network_Conditions.pdf"
mineru_md: "02-parsed-markdown/2025-CCS-Training_Robust_Classifiers_for_Classifying_Encrypted_Traffic_under_Dynamic_Network_Conditions.md"
status: processed
reading_level: L2
research_area:
  - encrypted-traffic-classification
  - robust-machine-learning
  - meta-learning
task:
  - encrypted-traffic-classification
  - robust-classification
  - dynamic-network-conditions
method:
  - meta-learning
  - MAML
  - class-aware-representation-augmentation
  - cluster-based-representation-alignment
  - adaptive-task-weight-allocation
dataset:
  - ISCXVPN
  - CrossPlatform
  - USTC-TFC
  - 3-new-large-scale-datasets
  - 880000-flows
code: ""
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

# MetaTraffic: 动态网络条件下加密流量分类的鲁棒分类器训练框架

## 0. 基础信息

| 字段 | 内容 |
|------|------|
| 论文全称 | Training Robust Classifiers for Classifying Encrypted Traffic under Dynamic Network Conditions |
| 作者 | Yuqi Qing, Qilei Yin, Xinhao Deng, Xiaoli Zhang, Peiyang Li, Zhuotao Liu, Kun Sun, Ke Xu, Qi Li |
| 机构 | 清华大学; 中关村实验室; 北京科技大学; George Mason University |
| 发表年份 | 2025 |
| 会议/期刊 | CCS 2025 |
| 关键词 | Encrypted Traffic Classification, Deep Learning, Meta-Learning, Robust Training, Dynamic Network Conditions |
| 代码 | 论文未明确说明 |

## 1. 一句话总结

提出 MetaTraffic，一种基于元学习的加密流量分类鲁棒训练框架，通过最小化不同网络条件下模型表示流量特征的差异，帮助 DL 模型学习稳定特征表示，在动态多种网络条件下准确率提升 8.94%，F1-Macro 提升 12.55%，而现有鲁棒训练方法准确率下降 28.85%。

## 2. 摘要翻译

**原文：**
Most existing DL-based encrypted traffic classification methods suffer performance degradation in real-world deployments due to dynamic network conditions, e.g., network environment changes and traffic obfuscation. Dynamic network conditions cause encrypted traffic to exhibit distinct feature patterns during training and testing phases. To address this issue, we propose MetaTraffic, a novel and general DL training framework built upon meta-learning that enhances the performance of supervised DL models designed for encrypted traffic classification against dynamic network conditions. Our key observation is that the traffic of the same network behaviors share the same semantic features even under different network conditions, which can be considered as stable feature representations. Therefore, MetaTraffic helps DL models learn stable feature representations by minimizing the discrepancies in how the models represent traffic features under different network conditions, thereby achieving robust classification under dynamic network conditions. We implement MetaTraffic based on meta-learning with three innovative facilitate modules to enhance its performance. We evaluate MetaTraffic using three public datasets and three new large-scale encrypted traffic datasets that cover multiple types of network conditions. Experimental results show that, under dynamic multiple types of network conditions, our framework improves the accuracy of DL models by 8.94% and the F1-Macro score by 12.55%, while existing robust training methods decrease the accuracy by 28.85% and the F1-Macro score by 33.52%.

**中文翻译：**
大多数现有基于 DL 的加密流量分类方法在真实世界部署中由于动态网络条件（如网络环境变化和流量混淆）而性能下降。动态网络条件导致加密流量在训练和测试阶段表现出不同的特征模式。为解决此问题，我们提出 MetaTraffic，一种基于元学习的新型通用 DL 训练框架，增强监督 DL 模型在动态网络条件下的加密流量分类性能。我们的关键观察是，相同网络行为的流量即使在不同网络条件下也共享相同的语义特征，可视为稳定特征表示。因此，MetaTraffic 通过最小化模型在不同网络条件下表示流量特征的差异，帮助 DL 模型学习稳定特征表示，从而在动态网络条件下实现鲁棒分类。我们基于元学习实现 MetaTraffic，包含三个创新模块以增强性能。我们使用三个公共数据集和三个新的大规模加密流量数据集评估 MetaTraffic，这些数据集涵盖多种网络条件类型。实验结果表明，在动态多种网络条件下，框架将 DL 模型的准确率提升 8.94%，F1-Macro 分数提升 12.55%，而现有鲁棒训练方法准确率下降 28.85%，F1-Macro 分数下降 33.52%。

## 3. 方法动机（Motivation）

### 3.1 问题背景与痛点

- **动态网络条件的影响**：
  - 不同主机：硬件、操作系统、加密协议不同，导致流量特征不同（如 TLS 1.2 vs TLS 1.3）
  - 不同网络环境：链路层、网络层、传输层协议和配置不同（如 MTU 设置）
  - 不同混淆策略：注入虚假包、正则化传输模式等
- **现有方法的局限**：
  - 仅在训练和测试流量受相同网络条件影响时有效
  - 仅能抵抗特定单一类型的网络条件
  - 依赖特定特征格式的数据增强，限制适用性
  - 在动态多种网络条件下性能大幅下降

### 3.2 核心直觉

- **稳定特征表示**：相同网络行为的流量即使在不同网络条件下也共享相同的语义特征
- **最小化表示差异**：通过最小化模型在不同网络条件下表示流量特征的差异，学习稳定特征表示
- **元学习泛化**：元学习增强 DL 模型的泛化能力，使其在部署后对未见过的流量生成稳定表示

## 4. 方法设计（Method Design）

### 4.1 整体流程

```
训练数据（多种网络条件） → 任务构建 → 临时模型训练 → 特征表示差异计算 → 模型优化
                           (条件不一致)  (每个任务)      (每个任务的损失)    (所有任务)
                                ↓
                           三个创新模块
                           (类感知增强 + 聚类对齐 + 自适应权重)
```

### 4.2 三个创新模块

**模块一：类感知表示增强（Class-aware Representation Augmentation）**
- **输入**：临时模型训练过程中的特征表示
- **处理**：
  - 在临时模型训练阶段直接向特征表示添加噪声
  - 噪声增强特征表示的多样性，特别是单调的简单样本
  - 增加分类难度，防止模型仅依赖特定特征
- **输出**：增强后的特征表示
- **关键点**：不合成新训练样本，无额外训练开销

**模块二：聚类表示对齐（Cluster-based Representation Alignment）**
- **输入**：训练和测试子集的特征表示
- **处理**：
  - 自适应聚类算法识别少量高度代表性的特征表示
  - 用于准确高效地计算特征表示差异
- **输出**：任务损失（特征表示差异）
- **关键点**：自动适应流量行为的多样性

**模块三：自适应任务权重分配（Adaptive Task Weight Allocation）**
- **输入**：所有任务的损失
- **处理**：
  - 持续评估 DL 模型的优化进度
  - 测量连续训练迭代中的损失变化
  - 分配与模型优化需求对齐的自适应任务权重
- **输出**：加权后的任务损失
- **关键点**：加速收敛，防止过拟合特定任务

### 4.3 训练流程

1. **任务构建**：将训练数据按网络条件分成多个任务，每个任务包含条件不一致的训练和测试子集
2. **临时模型训练**：为每个任务训练独立的临时模型 $\phi^*$
3. **损失计算**：计算每个任务的特征表示差异作为任务损失
4. **模型优化**：基于所有任务的损失联合优化原始模型 $\phi$
5. **迭代**：使用优化后的模型在下一轮迭代中构建新的临时模型
6. **收敛后微调**：模型收敛后，使用所有训练流量进行微调

### 4.4 关键公式

- **临时模型训练**：$\phi^* = \phi - \eta_1 \nabla_\phi \sum_{(x,y) \in D_{tr}} \mathcal{L}(\mathcal{C}(\mathcal{Z}(x;\phi);\phi), y)$
- **特征表示差异**：基于聚类的差异度量
- **自适应权重**：基于损失变化的权重分配

### 4.5 优缺点

**优势：**
- 通用框架：适用于任何监督 DL 模型，不限制特征格式
- 多种网络条件：同时抵抗主机、网络环境、混淆等多种条件
- 动态条件有效：在训练和测试流量受不同条件影响时仍有效
- 无额外数据需求：不需要数据增强，减少隐私泄露风险
- 三个创新模块相互增强

**局限：**
- 元学习训练开销较大
- 需要预先知道训练数据的网络条件
- 在极端条件下性能可能下降

## 5. 与其他方法对比（Comparison）

### 5.1 创新点

| 创新点 | 本文方法 | 现有方法 |
|--------|----------|----------|
| 动态条件 | 有效 | 无效 |
| 条件类型 | 主机+网络环境+混淆 | 通常单一类型 |
| 适用性 | 任何 DL 模型 | 特定特征格式 |
| 数据增强 | 不需要 | 需要 |
| 泛化能力 | 元学习增强 | 有限 |

### 5.2 与 Baseline 对比

与现有鲁棒训练方法对比：
- Rosetta：仅抵抗网络环境条件
- TrafCL：仅抵抗网络环境条件
- 2DA：仅抵抗网络环境条件
- NetAugment：抵抗主机和网络环境条件
- AAAttack：抵抗网络环境和混淆条件

**关键差异**：
- 现有方法在动态条件下性能大幅下降，MetaTraffic 提升性能
- 现有方法仅抵抗单一类型条件，MetaTraffic 抵抗多种类型
- MetaTraffic 适用于任何 DL 模型，现有方法受限于特定特征格式

## 6. 实验表现（Experiments）

### 6.1 数据集

| 数据集 | 描述 | 规模 |
|--------|------|------|
| ISCXVPN | 公共 VPN 流量数据集 | - |
| CrossPlatform | 公共跨平台数据集 | - |
| USTC-TFC | 公共流量分类数据集 | - |
| 新数据集 1 | 不同主机条件 | 880,000+ 流 |
| 新数据集 2 | 不同网络环境条件 | 20 云服务器，5 国家 |
| 新数据集 3 | 不同混淆策略条件 | - |

**新数据集特点**：首个涵盖多种网络条件类型的大规模加密流量数据集。

### 6.2 Baseline 方法

- Rosetta
- TrafCL
- 2DA
- NetAugment
- AAAttack
- 其他鲁棒训练方法

### 6.3 评估指标

- Accuracy
- F1-Macro
- 单一类型网络条件性能
- 多种类型网络条件性能

### 6.4 关键结果

**动态多种网络条件：**
- 准确率提升 8.94%
- F1-Macro 提升 12.55%
- 现有方法准确率下降 28.85%，F1-Macro 下降 33.52%

**单一类型网络条件：**
- 在主机、网络环境、混淆三种条件下均优于现有方法
- 在不同条件下性能稳定

**新数据集：**
- 首次公开涵盖多种网络条件的大规模数据集
- 超过 880,000 个加密流量流

## 7. 学习与应用（Learning & Application）

### 7.1 开源情况

- **代码**：论文未明确说明
- **数据集**：作者发布了三个新的大规模加密流量数据集
- **可复现性**：提供了详细的算法描述和数据集

### 7.2 可迁移价值

- **元学习框架**：元学习训练框架可应用于其他需要鲁棒性的任务
- **稳定特征表示**：学习稳定特征表示的方法可迁移至其他领域
- **自适应权重分配**：自适应任务权重方法可应用于多任务学习
- **数据集**：新数据集可用于其他加密流量研究

### 7.3 实际应用场景

- **网络流量分类**：在动态网络环境中部署流量分类系统
- **入侵检测**：在不同网络条件下检测恶意流量
- **应用识别**：在混淆环境下识别应用类型

## 8. 总结（Summary）

### 8.1 核心思想

MetaTraffic 的核心思想是通过元学习帮助 DL 模型学习稳定特征表示，最小化不同网络条件下模型表示流量特征的差异。类感知表示增强防止模型依赖特定特征，聚类表示对齐准确计算差异，自适应任务权重分配加速收敛。框架适用于任何监督 DL 模型，抵抗多种网络条件类型。

### 8.2 快速流程图

```
输入：训练数据（多种网络条件）
  ↓
任务构建（条件不一致的训练/测试子集对）
  ↓
临时模型训练（类感知表示增强）
  ↓
特征表示差异计算（聚类表示对齐）
  ↓
模型优化（自适应任务权重分配）
  ↓
迭代直到收敛
  ↓
微调并部署
  ↓
输出：鲁棒的加密流量分类器
```

## 9. 知识链接（Knowledge Links）

- [[encrypted-traffic-classification]]：本文的核心任务
- [[pre-training-finetuning]]：元学习与预训练/微调的关系
- [[traffic-classification]]：更广泛的任务类别
- [[transformer]]：DL 模型架构的背景
- [[few-shot-traffic-learning]]：元学习在少样本场景的应用

## 10. 证据记录（Evidence）

| 声明 | 证据 | 来源 |
|------|------|------|
| 准确率提升 8.94% | 动态多种网络条件 | 论文 §4 实验结果 |
| F1-Macro 提升 12.55% | 动态多种网络条件 | 论文 §4 实验结果 |
| 现有方法准确率下降 28.85% | 动态多种网络条件 | 论文 §4 实验结果 |
| 首个涵盖多种条件的大规模数据集 | 作者声明 | 论文 §1 |
| 880,000+ 流量流 | 新数据集规模 | 论文 §1 |

## 11. 原始资料链接（Source Links）

- **PDF**：`00-inbox/PDFs/2025-CCS-Training_Robust_Classifiers_for_Classifying_Encrypted_Traffic_under_Dynamic_Network_Conditions.pdf`
- **MinerU MD**：`02-parsed-markdown/2025-CCS-Training_Robust_Classifiers_for_Classifying_Encrypted_Traffic_under_Dynamic_Network_Conditions.md`

## 12. 后续问题（Open Questions）

1. **训练开销**：元学习的训练开销相比标准训练增加多少？
2. **新条件适应**：对于未见过的新型网络条件，框架的适应能力如何？
3. **极端混淆**：在极端混淆策略下，稳定特征表示是否仍然存在？
4. **模型架构**：框架对不同 DL 模型架构的提升效果是否一致？
5. **实时部署**：微调后的模型推理延迟是否满足实时需求？

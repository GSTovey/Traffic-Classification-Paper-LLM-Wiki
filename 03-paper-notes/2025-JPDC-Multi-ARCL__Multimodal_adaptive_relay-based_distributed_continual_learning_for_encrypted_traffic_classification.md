---
type: paper
title_original: "Multi-ARCL: Multimodal adaptive relay-based distributed continual learning for encrypted traffic classification"
title_cn: "Multi-ARCL：用于加密流量分类的多模态自适应中继式分布式持续学习"
authors:
  - Zeyi Li
  - Minyao Liu
  - Pan Wang
  - Wangyu Su
  - Tianshui Chang
  - Xuejiao Chen
  - Xiaokang Zhou
year: 2025
venue: Journal of Parallel and Distributed Computing (JPDC)
doi: unknown
url: unknown
pdf: "../00-inbox/PDFs/2025-JPDC-Multi-ARCL__Multimodal_adaptive_relay-based_distributed_continual_learning_for_encrypted_traffic_classification.pdf"
mineru_md: "../02-parsed-markdown/2025-JPDC-Multi-ARCL__Multimodal_adaptive_relay-based_distributed_continual_learning_for_encrypted_traffic_classification.md"
status: processed
reading_level: L2
research_area:
  - encrypted traffic classification
  - continual learning
  - machine unlearning
  - distributed learning
  - multimodal learning
task:
  - application classification
  - continual learning with class changes
method:
  - Multimodal Feature Extraction
  - Adaptive Relay-based Continual Learning (ARCL)
  - Optimization Constraint-driven Parameter Discarding
  - Novel Replay-based CL
  - Distributed Learning
  - SIF Weighted Word Vectors
  - CNN Classifier
dataset:
  - MIRAGE2019
  - ISCX2016
  - NJUPT2023 (private)
code: "https://github.com/sailorlee97/What-changes-you"
relevance: medium
created: 2026-06-09
updated: 2026-06-09
---

# Multi-ARCL: Multimodal adaptive relay-based distributed continual learning for encrypted traffic classification

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Multi-ARCL: Multimodal adaptive relay-based distributed continual learning for encrypted traffic classification |
| 中文标题 | Multi-ARCL：用于加密流量分类的多模态自适应中继式分布式持续学习 |
| 作者 | Zeyi Li, Minyao Liu, Pan Wang, Wangyu Su, Tianshui Chang, Xuejiao Chen, Xiaokang Zhou |
| 年份 | 2025 |
| 会议/期刊 | Journal of Parallel and Distributed Computing (JPDC) |
| 研究方向 | 加密流量分类、持续学习、机器遗忘、分布式学习、多模态学习 |
| 任务类型 | 应用分类（持续学习场景，含类变化） |
| 方法关键词 | Multimodal Feature Extraction, ARCL, Parameter Discarding, Replay-based CL, Distributed Learning, SIF, CNN |
| 数据集 | MIRAGE2019, ISCX2016, NJUPT2023 (private) |
| 是否开源 | 是（https://github.com/sailorlee97/What-changes-you） |
| PDF | `../00-inbox/PDFs/2025-JPDC-Multi-ARCL__Multimodal_adaptive_relay-based_distributed_continual_learning_for_encrypted_traffic_classification.pdf` |
| MinerU Markdown | `../02-parsed-markdown/2025-JPDC-Multi-ARCL__Multimodal_adaptive_relay-based_distributed_continual_learning_for_encrypted_traffic_classification.md` |

---

## 1. 一句话总结

> 提出 Multi-ARCL 框架，通过多模态特征提取（payload 语义 + 统计特征）和自适应中继式持续学习方法，解决持续学习中静默应用（silent applications）导致的模型稳定性衰减问题，在 NJUPT2023 数据集上准确率提升超过 8.64%。

---

## 2. 摘要翻译

### 2.1 摘要原文

Encrypted Traffic Classification (ETC) using Deep Learning (DL) faces two bottlenecks: homogeneous network traffic representation and ineffective model updates. Currently, multimodal-based DL combined with the Continual Learning (CL) approaches mitigate the above problems but overlook silent applications, whose traffic is absent due to guideline violations leading developers to cease their operation and maintenance. Specifically, silent applications accelerate the decay of model stability, while new and active applications challenge model plasticity. This paper presents Multi-ARCL, a multimodal adaptive replay-based distributed CL framework for ETC. The framework prioritizes using crypto-semantic information from flows' payload and flows' statistical features to represent. Additionally, the framework proposes an adaptive relay-based continual learning method that effectively eliminates silent neurons and retrains new samples and a limited subset of old ones. Exemplars of silent applications are selectively removed during new task training. To enhance training efficiency, the framework uses distributed learning to quickly address the stability-plasticity dilemma and reduce the cost of storing silent applications. Experiments show that ARCL outperforms state-of-the-art methods, with an accuracy improvement of over 8.64% on the NJUPT2023 dataset.

### 2.2 摘要中文翻译

使用深度学习的加密流量分类（ETC）面临两个瓶颈：同质化网络流量表示和低效的模型更新。目前，基于多模态的深度学习结合持续学习（CL）方法缓解了上述问题，但忽略了静默应用——由于违反准则导致开发者停止运营和维护，其流量不再存在。具体而言，静默应用加速了模型稳定性的衰减，而新应用和活跃应用挑战模型的可塑性。本文提出 Multi-ARCL，一个用于 ETC 的多模态自适应中继式分布式持续学习框架。该框架优先使用流 payload 的加密语义信息和流的统计特征进行表示。此外，框架提出了一种自适应中继式持续学习方法，能有效消除静默神经元并重新训练新样本和旧样本的有限子集。静默应用的样本在新任务训练期间被选择性移除。为提高训练效率，框架使用分布式学习快速解决稳定性-可塑性困境并降低存储静默应用的成本。实验表明 ARCL 优于 SOTA 方法，在 NJUPT2023 数据集上准确率提升超过 8.64%。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

现有持续学习方法在加密流量分类中忽略了静默应用（silent applications）的影响。静默应用是指因违反应用商店准则而被下架的应用，其流量不再存在但模型仍保留其参数和数据，导致：(1) 活跃应用被误分类为静默应用；(2) 模型稳定性衰减；(3) 存储空间浪费。

### 3.2 现有方法的痛点和不足

1. **同质化流量表示**：单一模态（仅统计特征或仅 payload）无法完整表示流量信息，网络环境变化时分类器性能下降
2. **Fine-tune**：直接在原模型上训练新知识，容易发生灾难性遗忘
3. **Bic（知识蒸馏）**：在 MIRAGE2019 和 NJUPT2023 上出现严重灾难性遗忘，无法遗忘静默应用
4. **iCaRL（记忆回放）**：在 NJUPT2023 上表现最差，因同厂商应用的公共流量增加复杂性
5. **通用问题**：现有 CL 方法保留所有旧应用的神经元和参数，静默应用占用样本集空间并影响模型分类性能

### 3.3 论文的研究假设或核心直觉

静默应用的神经元和数据会干扰模型对活跃和新应用的分类，通过自动识别并消除静默应用的参数，配合知识蒸馏保持活跃应用的知识，能在持续学习中更好地平衡稳定性和可塑性。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | Google 每季度从应用商店移除约 100 万个应用，静默应用数量持续增长 | §I, AppBrain 数据 |
| 痛点提炼 | 静默应用占用样本集空间，其神经元被激活导致活跃应用误分类 | §I, Fig. 1 |
| 问题转化 | 如何在持续学习中自动遗忘静默应用同时保持活跃应用知识 | §I |
| 文献定位 | 现有 CL 方法聚焦学习新应用和保留旧知识，忽略遗忘静默应用 | §II |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 优化约束驱动的参数丢弃能缓解静默应用导致的稳定性衰减 | 静默应用神经元干扰活跃应用分类 | 消融实验（Table 7） |
| 辅助假设 | 多模态特征比单模态特征更有效 | 单一模态无法完整表示流量信息 | 模态对比实验（Table 5 vs Table 6） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | ARCL 在 NJUPT2023 上 Accuracy 0.8810 vs Fine-tune 0.7371 | Table 8 |
| 辅助假设 | 支撑 | 多模态 F1 0.9356 vs 单模态 F1 0.8141 | Table 5 vs Table 6 |

---

## 4. 方法设计

### 4.1 方法整体流程

原始流量 → 五元组分割 Flow → 多模态特征提取（payload 语义 + 统计特征）→ 特征缩放 → 初始模型训练 → 持续学习：识别静默应用 → 参数丢弃 → 自适应中继式 CL → 分布式训练

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | 原始 PCAP | 五元组分割 flow，提取前 FN 个 packet 的 payload | Flow 集合 | 流量分割 |
| Step 2 | Payload | word2vec 学习词向量 → SIF 加权平均 → 减去第一主成分 | Payload 语义特征 (1, d2) | 语义提取 |
| Step 3 | Flow | 提取 packet-level、flow-level、统计特征 | 统计特征向量 | 特征提取 |
| Step 4 | Payload + 统计特征 | 拼接为多模态特征 → 特征缩放 | MultiFF | 多模态融合 |
| Step 5 | MultiFF | CNN 训练初始分类模型 | 初始模型 | 初始训练 |
| Step 6 | 新应用 + 静默应用 | 标签映射 → 冻结卷积层 → 删除静默神经元 → 解冻 | 更新后的模型 | 参数丢弃 |
| Step 7 | 活跃应用 + 新应用 | 蒸馏损失 + 交叉熵损失联合训练 | 最终模型 | 自适应 CL |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Payload 特征提取 | SIF 加权词向量 + PCA | Payload 字节 | 语义向量 (1, d2) | → 多模态融合 |
| 统计特征提取 | packet/flow/统计特征 | Flow 数据 | 特征向量 | → 多模态融合 |
| CNN 分类器 | 卷积 + 全连接分类 | MultiFF | 分类概率 | 最终输出 |
| 参数丢弃模块 | 标签映射 + 神经元删除 | 静默应用标签 | 精简模型 | → 自适应 CL |
| 自适应 CL 模块 | 蒸馏损失 + 交叉熵损失 | 活跃应用 + 新应用 | 更新模型 | 最终输出 |

### 4.4 公式、算法和机制解释

**SIF 加权**：w_i = a / (a + p(i))，其中 p(i) 是词频，a 是平滑参数。高频词权重更低。

**SIF 加权平均词向量**：V = Σ(w_i * v_i) / Σ(w_i)，然后减去第一主成分投影 V' = V - PV_1。

**标签映射**：f: A → B，将活跃应用的原始标签域映射到新标签域，跳过静默应用标签。

**参数冻结与解冻**：冻结时 ∂L/∂θ = 0，解冻时 ∂L/∂θ = α * ∂L/∂θ（α=1）。

**总损失**：loss = λ × loss_soft-target + (1-λ) × loss_hard-target，其中 λ = (n-j)/(n+m-j)。

**蒸馏损失**：loss_soft-target = -(1/S) Σ Σ y_ik log(y_ik)，保持活跃应用知识。

**交叉熵损失**：loss_hard-target = -(1/S) Σ Σ y_ic log(p_ic)，学习新应用。

### 4.5 方法优势

1. **静默应用处理**：首次在 ETC 持续学习中考虑静默应用的遗忘问题
2. **多模态表示**：结合 payload 语义和统计特征，比单模态 F1 提升 12.15%
3. **存储效率**：通过移除静默应用样本减少存储开销
4. **分布式训练**：支持多 GPU 并行加速训练
5. **开源**：代码和数据集公开

### 4.6 方法不足

1. **与重训练模型的差距**：ARCL 在各数据集上均略低于完全重训练模型（MIRAGE: 0.9157 vs 0.9302）
2. **LoLWR 应用识别差**：由于应用的交互特性，网络流量难以捕获，多模态 F1 仅 0.6369
3. **私有数据集依赖**：NJUPT2023 为私有数据集，可复现性受限
4. **未处理未知流量**：框架未集成未知流量过滤功能
5. **搜索效率低**：神经网络参数搜索过程效率有待提升

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 维度 | Fine-tune | Bic | iCaRL | ARCL |
|---|---|---|---|---|
| 静默应用处理 | 无 | 无 | 无 | 参数丢弃 + 样本移除 |
| 知识保持策略 | 无 | 知识蒸馏 | 记忆回放 | 蒸馏损失 + 交叉熵 |
| 多模态特征 | 否 | 否 | 否 | 是（payload + 统计） |
| 分布式训练 | 否 | 否 | 否 | 是 |

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 静默应用遗忘 | 优化约束驱动的参数丢弃方法 | 高 | 是 |
| 自适应中继式 CL | 蒸馏损失 + 交叉熵损失联合优化 | 高 | 是 |
| 多模态特征提取 | payload SIF 语义 + 统计特征融合 | 中 | 是 |
| 分布式 CL 训练 | 多 GPU 并行加速持续学习 | 中 | 是 |

### 5.3 适用场景

- 应用频繁上架/下架的移动网络环境
- 需要持续更新的加密流量分类系统
- 存储资源受限的边缘设备
- 校园网等私有网络的应用识别

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| Fine-tune | 简单快速 | 灾难性遗忘严重 | 引入参数丢弃和知识蒸馏 |
| Bic | 知识蒸馏减少遗忘 | 无法遗忘静默应用 | 自适应消除静默神经元 |
| iCaRL | 记忆回放保持旧知识 | 同厂商应用混淆严重 | 多模态特征 + 参数丢弃 |
| 重训练 | 最高准确率 | 存储和计算开销大 | 减少存储 + 分布式加速 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- CPU: 13th Gen Intel Core i7-13700KF
- GPU: NVIDIA RTX 4080（主训练），3080×4 + 3060×1（分布式测试）
- 内存: 32GB RAM
- Python 3.10
- 持续学习场景：初始训练 16 类 → 移除 2 类 + 新增 3 类（MIRAGE2019/NJUPT2023）
- ISCX2016：初始 4 类 → 移除 1 类 + 新增 2 类

### 6.2 数据集

| 数据集 | 类型 | 应用数 | 特征维度 | 说明 |
|---|---|---|---|---|
| MIRAGE2019 | 移动应用流量 | 19 | 统计特征 | 公开数据集 |
| ISCX2016 | VPN 流量 | 6 | 统计特征 | 公开数据集（SMOTE 扩充） |
| NJUPT2023 | 校园网流量 | 19 | 91 维统计特征 | 私有数据集 |

### 6.3 Baseline

Fine-tune, Bic, iCaRL, Retraining（完全重训练）

### 6.4 评价指标

Precision, Recall, F1-Score, Accuracy

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| MIRAGE2019 | Accuracy | 91.57% | 88.68% (Fine-tune) | +2.89% | 持续学习后 |
| MIRAGE2019 | F1 | 88.13% | 85.43% (Fine-tune) | +2.70% | 持续学习后 |
| ISCX2016 | Accuracy | 92.18% | 85.92% (Bic) | +6.26% | 持续学习后 |
| ISCX2016 | F1 | 92.13% | 88.14% (Bic) | +3.99% | 持续学习后 |
| NJUPT2023 | Accuracy | 88.10% | 79.46% (Bic) | +8.64% | 持续学习后 |
| NJUPT2023 | F1 | 87.90% | 81.68% (Bic) | +6.22% | 持续学习后 |
| NJUPT2023 | Accuracy | 88.10% | 48.22% (iCaRL) | +39.88% | iCaRL 表现极差 |

### 6.6 优势最明显的场景

NJUPT2023 数据集上，ARCL 相比 iCaRL 准确率提升 39.88%，相比 Fine-tune 提升 14.39%。该数据集包含同厂商多个应用（如腾讯系：QQ音乐、微信、QQ邮箱），公共流量增加分类难度，ARCL 的多模态特征和参数丢弃策略在此场景下优势显著。

### 6.7 局限性

1. ARCL 在各数据集上均略低于完全重训练模型（差距约 1-4%）
2. LoLWR（英雄联盟手游）应用识别 F1 仅 0.6369，因交互式应用流量难以捕获
3. NJUPT2023 为私有数据集，外部无法复现
4. 未处理未知流量过滤问题
5. 分布式训练在小 batch size 时效率反而下降

---

## 7. 学习与应用

### 7.1 是否开源？

是。代码和数据集地址：https://github.com/sailorlee97/What-changes-you

### 7.2 复现关键步骤

1. 五元组分割 flow，提取前 20 个 packet 的 payload
2. word2vec 学习词向量 → SIF 加权 → PCA 降维
3. 提取 packet/flow/统计特征，拼接为多模态特征
4. CNN 训练初始模型（16 类）
5. 模拟类变化：移除 2 类 + 新增 3 类
6. 标签映射 → 冻结卷积层 → 删除静默神经元 → 解冻
7. 蒸馏损失 + 交叉熵损失联合训练

### 7.3 关键超参数、预训练和训练细节

- Payload packet 数 FN: 20
- SIF 平滑参数 a: 默认值
- PCA 主成分数 d2: 固定维度
- 训练设备: RTX 4080
- 分布式: 4× 3080 + 1× 3060
- 最优回放样本数: 1000（性价比最高），3000-4000（准确率最高）

### 7.4 能否迁移到其他任务？

是。静默应用遗忘的思路可迁移到任何需要处理类消失的持续学习场景。多模态特征提取方法可应用于其他需要融合多种信息源的流量分析任务。

### 7.5 对我的研究有什么启发？

1. **静默应用问题**：真实网络环境中应用频繁下架，持续学习必须考虑遗忘机制
2. **多模态融合**：payload 语义 + 统计特征的融合方式简单有效
3. **存储优化**：通过移除静默应用样本显著减少存储开销
4. **分布式 CL**：持续学习可通过分布式训练加速，但需注意 batch size 与 GPU 数量的匹配

---

## 8. 总结

### 8.1 核心思想

> 多模态特征 + 静默应用遗忘 + 自适应中继式持续学习

### 8.2 速记版 Pipeline

1. 五元组分割 flow → 提取 payload 和统计特征
2. SIF 加权词向量 + PCA → 多模态特征融合
3. CNN 训练初始模型
4. 持续学习：标签映射 → 冻结 → 删除静默神经元 → 解冻
5. 蒸馏损失 + 交叉熵损失联合训练
6. 分布式多 GPU 并行加速

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[Continual Learning]]
- [[Machine Unlearning]]
- [[Silent Applications]]
- [[Stability-Plasticity Dilemma]]
- [[Multimodal Feature Extraction]]

### 9.2 相关方法

- [[iCaRL]]
- [[Bic]]
- [[Knowledge Distillation]]
- [[Memory Replay]]
- [[SIF Weighted Word Vectors]]

### 9.3 相关任务

- [[Encrypted Traffic Classification]]
- [[Application Classification]]
- [[Incremental Learning for ETC]]

### 9.4 可更新的综述页面

- [[Continual Learning for Traffic Classification]]
- [[Multimodal Traffic Representation]]

### 9.5 可加入的对比表

- [[CL Methods Comparison for ETC]]
- [[Silent Application Handling Strategies]]

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| Google 每季度移除约 100 万应用 | "about one million apps declining in status daily" | §I, AppBrain |
| 静默应用导致活跃应用误分类 | "a significant number of active applications are mistakenly identified as silent ones" | §I, Fig. 1 |
| 多模态 F1 显著高于单模态 | 多模态 F1 0.9356 vs 单模态 F1 0.8141 | §4.3.1, Table 5/6 |
| ARCL 在 NJUPT2023 上提升 8.64% | "accuracy improvement of over 8.64% on the NJUPT2023 dataset" | Abstract |
| iCaRL 在 NJUPT2023 上表现极差 | iCaRL Accuracy 0.4822 vs ARCL 0.8810 | Table 8 |
| 回放 1000 样本为最优性价比 | "at the 1000 data quantity mark, the model not only utilizes resources more efficiently but also achieves higher accuracy" | §4.4, Fig. 11 |
| 4 GPU + batch 1024 训练最快 | 656.49s vs 单 GPU 1229.93s | Table 13 |

---

## 11. 原始资料链接

- PDF：`../00-inbox/PDFs/2025-JPDC-Multi-ARCL__Multimodal_adaptive_relay-based_distributed_continual_learning_for_encrypted_traffic_classification.pdf`
- MinerU Markdown：`../02-parsed-markdown/2025-JPDC-Multi-ARCL__Multimodal_adaptive_relay-based_distributed_continual_learning_for_encrypted_traffic_classification.md`
- 代码：https://github.com/sailorlee97/What-changes-you

---

## 12. 后续问题

- 如何处理未知流量的过滤和标记？
- 能否将参数丢弃方法扩展到更细粒度（如单个神经元级别）？
- 在更大规模的应用场景下（数百类）ARCL 的表现如何？
- 分布式训练的通信开销如何优化？

---

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

从加密流量分类面临同质化表示和低效更新两大瓶颈出发，指出现有持续学习方法忽略了静默应用（因违规被下架的应用）对模型稳定性的影响，提出多模态特征提取 + 自适应中继式持续学习框架，通过参数丢弃消除静默应用干扰，在三个数据集上超越 SOTA。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 概述问题和结果 | 全文缩影 | "accuracy improvement of over 8.64%" |
| Introduction | 从应用商店移除应用的现象引入 | 动机铺垫 | "silent applications accelerate the decay of model stability" |
| Related Work | DL-ETC 和 CL 方法演进 | 技术定位 | 现有方法忽略静默应用 |
| Method | Multi-ARCL 框架详细设计 | 核心贡献 | 优化约束驱动的参数丢弃 |
| Experiments | 多数据集多方法对比 | 支撑论点 | NJUPT2023 上的显著提升 |
| Conclusion | 总结和未来方向 | 收尾 | 未知流量过滤和训练加速 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 场景缺失 | 现有 CL 方法未考虑静默应用 | AppBrain 数据 + 误分类现象 | §I |
| 性能瓶颈 | 单模态表示不完整 | 多模态 vs 单模态实验对比 | §4.3.1 |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 多模态 vs 单模态对比 | 证明多模态特征有效性 | 基础论点支撑 |
| 消融实验 | 证明 ARCL 的鲁棒性 | 核心方法验证 |
| 与 SOTA 方法对比 | 证明 ARCL 的优越性 | 主实验支撑 |
| 存储和计算效率分析 | 证明实用性 | 应用价值论证 |
| 分布式训练效率 | 证明可扩展性 | 工程价值论证 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 从应用商店数据引入静默应用问题 | 用真实世界数据支撑问题重要性 |
| Gap 提出方式 | 指出现有方法"忽略"静默应用 | "overlook" 句式建立 Gap |
| 方法论证逻辑 | 从稳定性-可塑性困境推导设计决策 | 概念框架驱动方法设计 |
| 实验组织逻辑 | 先模态对比 → 再 SOTA 对比 → 最后效率分析 | 层层递进验证 |
| 最值得借鉴的一句话结构 | "silent applications accelerate the decay of model stability, while new and active applications challenge model plasticity" | 用对比句式阐述双重挑战 |

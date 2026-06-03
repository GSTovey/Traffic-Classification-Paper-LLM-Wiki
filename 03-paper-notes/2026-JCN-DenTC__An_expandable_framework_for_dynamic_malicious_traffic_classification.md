---
type: paper
title_original: "DenTC: An expandable framework for dynamic malicious traffic classification"
title_cn: "DenTC：面向动态恶意流量分类的可扩展框架"
authors: ["Rui Chen", "Lailong Luo", "Bangbang Ren", "Deke Guo", "Changhao Qiu", "Shangsen Li", "Xiaodong Wang"]
year: 2026
venue: "JCN"
doi: "unknown"
url: "unknown"
pdf: "00-inbox/PDFs/2026-JCN-DenTC__An_expandable_framework_for_dynamic_malicious_traffic_classification.pdf"
mineru_md: "02-parsed-markdown/2026-JCN-DenTC__An_expandable_framework_for_dynamic_malicious_traffic_classification.md"
status: processed
reading_level: L2
research_area: ["malicious-traffic-detection", "traffic-classification"]
task: ["incremental-learning", "dynamic-classification", "catastrophic-forgetting-mitigation"]
method: ["convolutional-network", "incremental-learning", "exemplar-replay"]
dataset: ["USTC-TFC2016", "CICIDS2017"]
code: "unknown"
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

## §0 基础信息

| 字段 | 内容 |
|------|------|
| 论文标题 | DenTC: An expandable framework for dynamic malicious traffic classification |
| 作者 | Rui Chen, Lailong Luo, Bangbang Ren, Deke Guo, Changhao Qiu, Shangsen Li, Xiaodong Wang |
| 机构 | National University of Defense Technology; Sun Yat-sen University |
| 年份/期刊 | 2026 / JCN (Journal of Computer Networks) |

## §1 一句话总结

提出 DenTC 可扩展框架，通过动态可扩展模块（DEM）实现恶意流量的增量学习——冻结旧特征提取器、扩展新提取器、回放代表性样本、辅助损失增强新类学习、权重对齐纠正偏差——在不重训全模型的情况下缓解灾难性遗忘。

## §2 摘要翻译

**原始摘要：** Malicious traffic classification is crucial for network security. Current DL-based methods primarily learn features from static datasets, but network traffic is dynamic with new types continuously emerging. Fine-tuning leads to catastrophic forgetting; retraining introduces high data dependency. We propose DenTC, a novel expandable framework for dynamic malicious traffic classification. DenTC offers: (i) incremental learning without retraining; (ii) mitigates catastrophic forgetting; (iii) minimizes data dependency. We construct a dynamically expandable module that freezes previously learned representations while extending new feature extractors.

**中文翻译：** 恶意流量分类对网络安全至关重要。当前DL方法主要从静态数据集学习特征，但网络流量是动态的，新类型不断涌现。微调导致灾难性遗忘，重训引入高数据依赖。本文提出 DenTC，一种新颖的可扩展动态恶意流量分类框架。DenTC提供：(i)无需重训的增量学习；(ii)缓解灾难性遗忘；(iii)最小化数据依赖。构建动态可扩展模块，冻结先前学习的表示同时扩展新特征提取器。

## §3 方法动机

**痛点：**
- **灾难性遗忘：** 用新类数据微调旧模型时，覆盖了旧类的关键特征表示，导致旧类性能急剧下降
- **高数据依赖：** 重训全模型需要存储所有历史数据，在隐私约束或存储受限环境下不可行
- 网络流量动态演化，新攻击类型不断出现，静态模型无法适应

**核心直觉：**
- 冻结已学习的特征提取器保护旧知识
- 扩展新的特征提取器学习新知识
- 少量代表性样本回放强化旧记忆
- 辅助损失帮助新提取器学习判别性特征
- 权重对齐纠正新旧类之间的偏差

## §4 方法设计

**整体流程：** 原始pcap → 流量预处理模块(TPM) → 动态可扩展模块(DEM) → 分类器学习模块(CLM)

**关键模块：**

1. **流量预处理模块(TPM)：**
   - 流量分割：按五元组分割pcap
   - 流量过滤：选择关键包
   - 流量图像生成：转换为二维流量矩阵

2. **动态可扩展模块(DEM)：** 核心模块
   - 每个增量步骤：冻结已学习的特征提取器F_1^{t-1}, F_2^{t-1}, ...
   - 扩展新的特征提取器F_i^t学习新类知识
   - 代表性样本回放：从旧类中选择少量代表性样本（而非存储全部旧数据）
   - 辅助损失：增强新特征提取器学习判别性特征的能力

3. **分类器学习模块(CLM)：**
   - 交叉熵损失 + 辅助损失
   - 权重对齐策略：纠正新旧类之间的偏差，缓解类不平衡

**优点：** 增量学习无需重训；冻结旧知识缓解遗忘；仅需少量旧类样本；低存储和计算开销
**缺点：** 论文未明确说明随着增量步骤增加，模型参数增长的上界

## §5 与其他方法对比

| 方法 | 准确率趋势 | 数据需求 | 特点 |
|------|-----------|---------|------|
| Finetune | 急剧下降（遗忘） | 仅新数据 | 灾难性遗忘 |
| Retraining | 保持稳定 | 全部旧+新数据 | 高数据依赖 |
| **DenTC** | **保持稳定** | **新数据+少量旧样本** | **平衡遗忘与效率** |

- 相比Finetune：有效缓解灾难性遗忘
- 相比Retraining：大幅降低数据依赖（无需存储所有历史数据）

## §6 实验表现

**数据集：** USTC-TFC2016, CICIDS2017
**实验设置：** 类别从2逐步增加到20，每个增量步骤引入新类
**关键结果：**
- DenTC在整个增量过程中保持稳定高准确率
- Finetune准确率从1.0降至约0.05（20类时）
- Retraining保持1.0但数据量线性增长
- DenTC数据量远低于Retraining

## §7 学习与应用

- **开源代码：** 论文未明确提供
- **可复现性：** 框架描述清晰，三个模块分工明确
- **迁移价值：** 动态可扩展架构的思路适用于其他需要持续学习的场景（如IoT设备上的恶意软件检测）；冻结+扩展的策略可推广到其他增量学习框架

## §8 总结

**核心思想：** 通过动态可扩展架构实现恶意流量的增量学习——冻结旧特征提取器保护已学知识，扩展新提取器学习新类，用少量代表性样本回放强化记忆，辅助损失+权重对齐保证学习质量。

**快速流水线：**
```
原始pcap → 流量分割+过滤 → 二维流量矩阵
  → DEM: 冻结旧提取器 + 扩展新提取器
  → 旧类代表性样本回放
  → CLM: CE损失 + 辅助损失 + 权重对齐
  → 分类输出
```

## §9 知识链接

- [[malicious-traffic-detection]] — 恶意流量检测
- [[traffic-classification]] — 流量分类
- [[convolutional-network]] — CNN特征提取器
- [[traffic-representation-learning]] — 流量图像表示

## §10 证据记录

| 声明 | 证据 |
|------|------|
| Finetune导致灾难性遗忘 | Fig.1左：准确率从1.0降至0.05 |
| Retraining数据量线性增长 | Fig.1右：数据量随类数增加 |
| DenTC保持稳定且数据量低 | Fig.1实验对比 |
| 每日数千次恶意活动造成万亿美元损失 | §1引用Reference [10] |

## §11 原始资料链接

- PDF: `00-inbox/PDFs/2026-JCN-DenTC__An_expandable_framework_for_dynamic_malicious_traffic_classification.pdf`
- MinerU MD: `02-parsed-markdown/2026-JCN-DenTC__An_expandable_framework_for_dynamic_malicious_traffic_classification.md`

## §12 后续问题

- 随着增量步骤增加（如100+类），冻结的旧提取器数量线性增长，参数总量如何控制？
- 代表性样本的选择策略对性能影响如何？
- 能否结合知识蒸馏进一步压缩旧知识？

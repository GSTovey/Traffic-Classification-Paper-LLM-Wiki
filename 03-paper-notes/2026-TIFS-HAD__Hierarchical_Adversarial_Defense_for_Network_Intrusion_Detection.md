---
type: "paper"
title_original: "HAD: Hierarchical Adversarial Defense for Network Intrusion Detection"
title_cn: "HAD：面向网络入侵检测的分层对抗防御"
authors: ["Shuo Yang", "Xinran Zheng", "Jinze Li", "Jinfeng Xu", "Edith C. H. Ngai"]
year: 2026
venue: "TIFS"
source_version: "IEEE TIFS 作者接收稿，正式页面以出版方更新为准。"
doi: "10.1109/tifs.2026.3750723"
url: "https://doi.org/10.1109/tifs.2026.3750723"
pdf: "00-inbox/PDFs/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection.pdf"
mineru_md: "02-parsed-markdown/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection.md"
status: "processed"
reading_level: "L3"
research_area: ["恶意流量检测", "对抗防御", "漂移"]
task: ["入侵检测补充判定", "识别分布变化"]
method: ["特征分区", "双编码器", "分层对比学习"]
dataset: ["NSL-KDD", "label-corrected CIC-IDS", "AnoShift / Kyoto-2006+"]
code: "https://github.com/kalendsyang/HAD"
relevance: "high"
created: "2026-11-18"
updated: "2026-11-18"
metadata_source: "Crossref"
source_sha256: "cf7b4d058bd2ac697084dd0bd70b646c43702422d286b86294b2b709403e7b1f"
internal_citation_count: 0
citation_impact: 0.8
composite_weight: 0.68
citation_count_scope: "verified DOI or normalized complete titles in vault References; lower bound"
citation_count_verified: "2026-11-18"
---

# HAD: Hierarchical Adversarial Defense for Network Intrusion Detection

## 0. 论文基础信息

| 项目 | 内容 |
| --- | --- |
| 原文标题 | HAD: Hierarchical Adversarial Defense for Network Intrusion Detection |
| 中文标题 | HAD：面向网络入侵检测的分层对抗防御 |
| 作者 | Shuo Yang、Xinran Zheng、Jinze Li、Jinfeng Xu、Edith C. H. Ngai |
| 年份 | 2026 |
| 会议/期刊及版本 | IEEE TIFS 作者接收稿，正式页面以出版方更新为准。 |
| DOI | 10.1109/tifs.2026.3750723 |
| 题录来源 | Crossref |
| 研究方向 | 恶意流量检测、对抗防御、漂移 |
| 任务类型 | 入侵检测补充判定、识别分布变化 |
| 方法关键词 | 特征分区、双编码器、分层对比学习 |
| 数据集 | NSL-KDD；label-corrected CIC-IDS；AnoShift / Kyoto-2006+ |
| 开源状态 | 论文指向作者的防御模型实现。主实验和时间漂移配置需按章节核对。 |
| PDF | [[00-inbox/PDFs/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection.pdf]] |
| MinerU Markdown | [[02-parsed-markdown/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection.md]] |

题录核验见 [出版记录](https://doi.org/10.1109/tifs.2026.3750723)。

## 1. 一句话总结

HAD 用两组特征的表示距离补充 IDS 决策，通过分层对比训练约束正常、异常和防御用替代样本的分布。

## 2. 摘要翻译

### 2.1 摘要原文

见 [[00-inbox/PDFs/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection.pdf]] 第 1 页 Abstract。

### 2.2 摘要中文翻译

入侵检测的流级特征可能受变化而失去区分力。HAD 先依据模型对不同特征的敏感性分区，以特征层替代样本建模，再在两个子空间学习正常、恶意及对抗样本的分层距离。论文评估其作为原 IDS 的第二判定和独立分类器两种用途。

## 3. 方法动机

单纯针对某种扰动训练的防御可能依赖已知扰动分布。作者假设正常流在两个视角下更一致，训练出的双侧距离可以给高不确定流增加证据（§III–IV）。

### 3.4 问题发现路径

| 阶段 | 内容 |
| --- | --- |
| 现象观察 | 正常流在论文的训练设置下往往具有更稳定的跨视角关系。 |
| 痛点提炼 | 多数防御随扰动设定变化，训练时拟合的正常参照也可能漂移。 |
| 问题转化 | 训练轻量跨视角距离是否可作为 IDS 的额外可靠性信号？ |
| 文献定位 | 用 MANDA 和原 IDS 区分附加对抗检测、整体入侵检测。 |

### 3.5 科学假设形成

正常与异常的两侧表示距离可以补充模型，但依赖正常参考的稳定性。

验证方式　固定 FPR 后分数据集比 TPR，并在源阈值不变时跨年份复测。严重时间漂移使分布交叠，即可见条件性失效。

已有结果　表 III–IV 的结果随样本条件变化，表 XI–XII 拆开源域和目标良性再锚定。

## 4. 方法设计

### 4.1 输入、处理与输出

| 步骤 | 输入 | 处理 | 输出 |
| --- | --- | --- | --- |
| 特征评估 | 训练流的统计特征和原 IDS | 依据对检测模型的贡献估计特征敏感性，划分输入视角 | 两组流特征 |
| 防御表示 | 训练的正常、恶意及合成代理样本 | 分别训练小编码器并用分层损失约束投影之间的距离 | 对类间几何敏感的距离分数 |
| 检测与校准 | IDS 判定及当前输入 | 对原判为正常的观察补充打分，严重漂移时分析新采集正常参考 | 检测结果与漂移下的工作点 |

### 4.2 机制与条件

式 (11) 的 DIS 为两个投影的欧氏距离，训练以相对距离把正常样本约束到紧密区域。EP 为对具体 IDS 决策的经验敏感度，不能解释为协议上的可修改性。两个视角的比较可作为可审计的附加分数（§IV-A/C）。

## 5. 与其他方法对比

对 MANDA 主要比较对抗样本的 ROC-AUC 及同 FPR 的 TPR。FS/SSG/HCL 消融分开检验输入分组、代理样本及距离目标。与 COSINT DHOR 的嵌入邻域比较可用于提出对照，但二者分母、决策单位和训练标签都需要对齐。

## 6. 实验表现与局限性

### 6.1 设置、数据与对照

NSL-KDD 使用标准分区，修正标签的 CIC-IDS 使用 80/20，三次独立运行。AnoShift 用 IID（2006–2010）确定模型、预处理和阈值，再直接测 NEAR（2011–2013）与 FAR（2014–2015）。FAR 的良性再锚定单独报告目标域预算。

- 基线　MANDA、蒸馏、重训及未加防御的 DNN/RF/GNB，按任务使用相应对照。
- 指标　对抗样本 ROC-AUC、TPR@FPR、分类 F1、运行时间、特征子空间距离。

### 6.2 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 对照 | 差异 | 原文定位 |
| --- | --- | --- | --- | --- | --- |
| NSL-KDD 的论文 C&W 评估 | TPR@5% FPR | 0.9008 | MANDA 0.4805 | +42.03 个百分点 | §VI-B 表 III |
| CIC-IDS 的论文 FGSM 评估 | TPR@5% FPR | 0.7568 | MANDA 0.9053 | −14.85 个百分点 | §VI-B 表 IV，存在反例 |
| AnoShift FAR 的论文 C&W 评估 | F1 | 0.8098（100 个目标良性样本） | 0.7111（目标样本预算为 0） | +9.87 个百分点 | §VII-C 表 XII，目标域再校准 |

### 6.7 局限性

特征层代理样本提供表示学习对照。在线流量的协议可实现性需另衡量。正常分布在匀质小数据可能更紧密，跨时间或工作负载时距离分布会改变。论文主表最低列为 1% FPR。

## 7. 学习与应用

### 7.1 开源状态

论文指向作者的防御模型实现。主实验和时间漂移配置需按章节核对。

[作者公开仓库或产物](https://github.com/kalendsyang/HAD)。

### 7.2 复核要点

在防御评估数据上固定训练侧划分、归一化和阈值，同一观察预算比较无防御、附加判定和独立判定。对目标侧正常再锚定划分独立校准/留出集合，检查样本预算与尾部误报。

### 7.3 可迁移的研究问题

与 COSINT DHOR 第 18–25、27、31 页共享的问题是正常参考何时可靠。以同一表示、同召回和接受率比较全局阈值、邻域规则和按环境再校准。需要异质背景与同承载纯代理等不同分母。

## 8. 总结

用正常流的跨视角一致性补充 IDS。

特征评估 → 防御表示 → 检测与校准。

## 9. Obsidian 知识链接

- 概念　[[04-concepts/malicious-traffic-detection]]、[[04-concepts/anomaly-detection]]、[[04-concepts/traffic-representation-learning]]。
- 方法　[[05-methods/contrastive-learning]]、[[05-methods/factorized-detection]]。
- 任务　[[06-tasks/malicious-traffic-detection]]、[[06-tasks/anomaly-detection]]。
- 综述　[[survey-malicious-traffic-detection]]。
- 对比与相邻资料　[[method-comparison-table]]、[[03-paper-notes/2026-COSINT-北邮时金桥]]、[[2026-TIFS-DualGuard__An_Adaptive_Detection_Framework_for_Concurrent_Malicious_and_Normality_Drifts_in_Network_Traffic]]。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
| --- | --- | --- |
| 双投影距离的补充检测效果随条件变化 | 主表有正向和反向的同 FPR 结果 | §IV-C 式 (11)、§VI-B 表 III–IV |
| 严重正常性漂移使低离散度参考失稳 | FAR 正常分数与少量新良性再锚定的对照 | §VII-B–C 表 XI–XII |

## 11. 原始资料链接

- PDF　[[00-inbox/PDFs/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection.pdf]]
- MinerU Markdown　[[02-parsed-markdown/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection.md]]
- MinerU 原始归档　[[01-mineru-output/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection/full.md]]

## 12. 后续问题

优先检验 §6.7 的主要限制，按 §7.2 记录数据、观测和指标条件。

## 13. 写作叙事与故事线分析

论文先通过特征分区提出正常样本跨视角一致的假设，再用分层表示实现防御。独立防御、附加检测和时间漂移各用相应主结果，FAR 的恢复另列目标数据访问。

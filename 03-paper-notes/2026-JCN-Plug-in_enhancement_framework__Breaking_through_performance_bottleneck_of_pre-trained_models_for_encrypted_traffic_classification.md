---
type: paper
title_original: "Plug-in enhancement framework: Breaking through performance bottleneck of pre-trained models for encrypted traffic classification"
title_cn: "插件增强框架：突破预训练模型在加密流量分类中的性能瓶颈"
authors: ["Chaofan Zheng", "Hailong Ma", "Yanze Qu", "Yiming Jiang", "Wenbo Wang"]
year: 2026
venue: "JCN"
doi: "unknown"
url: "unknown"
pdf: "00-inbox/PDFs/2026-JCN-Plug-in_enhancement_framework__Breaking_through_performance_bottleneck_of_pre-trained_models_for_encrypted_traffic_classification.pdf"
mineru_md: "02-parsed-markdown/2026-JCN-Plug-in_enhancement_framework__Breaking_through_performance_bottleneck_of_pre-trained_models_for_encrypted_traffic_classification.md"
status: processed
reading_level: L2
research_area: ["encrypted-traffic-analysis", "traffic-classification"]
task: ["traffic-classification", "pre-trained-model-enhancement", "feature-fusion"]
method: ["pre-training-finetuning", "transformer", "gated-fusion"]
dataset: ["USTC-TFC2016", "ISCXVPN2016", "ISCXTor2016", "CICIDS2017"]
code: "https://github.com/slg6/Plug-inEnhancementFramework"
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

## §0 基础信息

| 字段 | 内容 |
|------|------|
| 论文标题 | Plug-in enhancement framework: Breaking through performance bottleneck of pre-trained models for encrypted traffic classification |
| 作者 | Chaofan Zheng, Hailong Ma, Yanze Qu, Yiming Jiang, Wenbo Wang |
| 机构 | Information Engineering University; Ministry of Education Key Lab |
| 年份/期刊 | 2026 / JCN |
| 代码 | https://github.com/slg6/Plug-inEnhancementFramework |

## §1 一句话总结

提出即插即用的增强框架，通过统计特征语义映射网络（SFSEM）和自注意力标量门控融合机制，将人工统计特征与预训练模型的语义特征无损融合，在不修改原模型权重的前提下，为4种主流PTM提升F1分数最高达55%。

## §2 摘要翻译

**原始摘要：** Pre-trained models alleviate constraints of limited labelled data for encrypted traffic classification. However, existing PTMs can only process fixed-length raw byte payloads, facing insufficient feature extraction and input length limitations. We design a pluggable enhancement framework that resolves spatial mismatches between heterogeneous features through a Statistical Feature Semantic Mapping network and employs an adaptive gated fusion mechanism for incremental enhancement without modifying PTM weights. Experiments show F1 improvements of up to 26%, 20%, 55%, and 14% for four mainstream PTMs.

**中文翻译：** 预训练模型缓解了加密流量分类中标注数据有限的约束，但现有PTM只能处理固定长度的原始字节载荷，面临特征提取不足和输入长度限制。本文设计即插即用的增强框架，通过统计特征语义映射网络解决异构特征间的空间失配，采用自适应门控融合机制实现增量增强而不修改PTM权重。实验显示4种主流PTM的F1分数分别提升最高26%、20%、55%和14%。

## §3 方法动机

**痛点：**
- **信息截断：** PTM（如ET-BERT）仅接受固定长度输入（128或512字节），丢失大量流级统计特征（持续时间、包间隔、传输速率等）
- **特征失配：** PTM的[CLS]向量（768维，高度非线性语义组合）与统计特征向量（77维，维度独立、物理意义明确）存在严重的语义空间和维度不匹配
- 直接拼接会导致性能下降
- 二次微调成本高，在边缘计算和实时系统中不可接受

**核心直觉：**
- 统计特征包含PTM丢失的全局行为信息，是天然的补充
- 需要先将统计特征映射到与[CLS]兼容的语义空间
- 门控融合可动态平衡两种特征的重要性，保护预训练语义完整性
- 即插即用设计避免修改原模型

## §4 方法设计

**整体流程：** 原始流量 → 统计特征提取(CFM) + PTM语义提取([CLS]) → SFSEM语义映射 → 门控融合网络(GATING) → 分类头

**关键模块：**

1. **统计特征提取：**
   - 改进CICFlowMeter，处理重传包导致的流分割错误
   - 提取77维统计特征向量[SFV]（持续时间、包长度分布、包间隔、方向性等）

2. **统计特征语义映射网络(SFSEM)：**
   - 轻量两层MLP：输入层=SFV维度，隐层自适应调整，输出层=[CLS]维度
   - LayerNorm + GELU激活 + Dropout(0.1)
   - 将物理空间的统计特征映射到PTM语义空间，生成[SFSV]

3. **门控融合网络(GATING)：**
   - 自注意力标量门控单元
   - 动态平衡[SFSV]和[CLS]的融合比例
   - 当载荷语义贫乏时增大[SFSV]权重，反之优先保留[CLS]

4. **特征融合模块(FFM)：** 生成动态加权交互向量[DWIV]

**优点：** 即插即用，不修改PTM权重；可增强已微调模型；兼容Mamba/Transformer等多种架构
**缺点：** 论文未明确说明在对抗性流量混淆技术下的有效性

## §5 与其他方法对比

- 相比传统特征拼接：通过语义映射解决空间失配
- 相比二次微调：无需修改PTM权重，计算成本低
- 相比增大PTM输入长度：避免计算复杂度爆炸
- 首个为PTM设计的通用即插即用统计特征增强框架

## §6 实验表现

**数据集：** 10个流量分类任务，9个公开数据集（含USTC-TFC2016, ISCXVPN2016, ISCXTor2016, CICIDS2017等）
**PTM：** 4种不同架构的预训练模型（ET-BERT, TrafficFormer, YaTC, NetMamba等）
**关键结果：**
- 每种PTM的F1提升均超过10%
- 最高提升：55%（某PTM在某任务上）
- 四种PTM分别提升最高26%、20%、55%、14%
- 对已微调模型同样有效（无需重训微调参数）
- 特征子集实验：即使仅用top-20维特征也能有效提升

## §7 学习与应用

- **开源代码：** https://github.com/slg6/Plug-inEnhancementFramework
- **可复现性：** 77维特征标准基于CICFlowMeter，可复现
- **迁移价值：** 即插即用设计可直接应用于任何已有PTM；语义映射+门控融合思路可推广到其他异构特征融合场景

## §8 总结

**核心思想：** 通过轻量语义映射网络将人工统计特征投射到PTM语义空间，再用自注意力门控机制动态融合两种特征，在不修改PTM的前提下突破性能瓶颈。

**快速流水线：**
```
原始流量 → 去重传包 → 五元组流重建
  → CICFlowMeter提取77维统计特征[SFV]
  → SFSEM: MLP映射[SFV]→[SFSV](与[CLS]同空间)
  → PTM提取[CLS]语义向量
  → GATING: 自注意力门控融合[CLS]+[SFSV]→[DWIV]
  → 分类头 → 预测结果
```

## §9 知识链接

- [[encrypted-traffic-analysis]] — 加密流量分析
- [[traffic-classification]] — 流量分类
- [[pre-training-finetuning]] — 预训练-微调范式
- [[transformer]] — PTM骨干架构
- [[traffic-representation-learning]] — 统计特征与语义特征融合

## §10 证据记录

| 声明 | 证据 |
|------|------|
| PTM仅处理固定长度输入，丢失全局特征 | Fig.2信息截断示意图 |
| [CLS]与统计特征存在严重语义失配 | §4.1维度和语义异质性分析 |
| 重传包导致流分割错误 | Table 1: 部分类别重传率>30% |
| F1最高提升55% | 实验结果 |
| 对已微调模型同样有效 | 实验验证 |

## §11 原始资料链接

- PDF: `00-inbox/PDFs/2026-JCN-Plug-in_enhancement_framework__Breaking_through_performance_bottleneck_of_pre-trained_models_for_encrypted_traffic_classification.md`
- MinerU MD: `02-parsed-markdown/2026-JCN-Plug-in_enhancement_framework__Breaking_through_performance_bottleneck_of_pre-trained_models_for_encrypted_traffic_classification.md`

## §12 后续问题

- 在对抗性流量混淆（如主动混淆技术）下，统计特征的判别性是否仍然有效？
- 能否将该框架扩展到支持多流关联行为的联合检测？
- SFSEM的隐层维度如何自适应选择以适配不同PTM？

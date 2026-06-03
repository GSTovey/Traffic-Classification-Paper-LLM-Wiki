---
type: paper
title_original: "TriFusion: A Self-Supervised Learning Enhanced Dual-Level Multimodal Framework for Traffic Classification"
title_cn: "TriFusion：自监督学习增强的双层级多模态流量分类框架"
authors: ["Haodong Yue", "Haozhen Zhang", "Xi Xiao", "Le Yu", "Guangwu Hu", "Qing Li"]
year: 2026
venue: "ICASSP"
doi: "unknown"
url: "unknown"
pdf: "00-inbox/PDFs/2026-ICASSP-TriFusion_A_Self-Supervised_Learning_Enhanced_Dual-Level_Multimodal_Framework_for_Traffic_Classification.pdf"
mineru_md: "02-parsed-markdown/2026-ICASSP-TriFusion_A_Self-Supervised_Learning_Enhanced_Dual-Level_Multimodal_Framework_for_Traffic_Classification.md"
status: processed
reading_level: L2
research_area: ["encrypted-traffic-analysis", "traffic-classification"]
task: ["traffic-classification", "multimodal-learning"]
method: ["self-supervised-learning", "graph-neural-network", "transformer", "multi-modal-fusion", "contrastive-learning"]
dataset: ["ISCX-VPN", "CICIoT", "ISCX-nonTor"]
code: "unknown"
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

## §0 基础信息

| 字段 | 内容 |
|------|------|
| 论文标题 | TriFusion: A Self-Supervised Learning Enhanced Dual-Level Multimodal Framework for Traffic Classification |
| 作者 | Haodong Yue, Haozhen Zhang, Xi Xiao, Le Yu, Guangwu Hu, Qing Li |
| 机构 | Tsinghua University (SIGS); Peng Cheng Laboratory; Nanjing UPT |
| 年份/期刊 | 2026 / ICASSP |

## §1 一句话总结

提出 TriFusion 双层级多模态框架，在包级别构建图像-图联合表示（每字节同时作为像素和图节点），在流级别引入时序模态，通过自监督学习编码器在 ISCX-VPN 和 CICIoT 数据集上实现99%+准确率。

## §2 摘要翻译

**原始摘要：** Existing unimodal methods struggle to exploit complementary features across modalities. We propose TriFusion, a dual-level multimodal framework with self-supervised learning. TriFusion jointly models intra- and inter-packet dependencies by constructing traffic images, graphs, and temporal sequences. We construct packet-level traffic images and graphs, where each byte corresponds to both an image pixel and a graph node. SSL-based encoders are designed for packet-level modalities. Experiments on ISCX-VPN and CICIoT datasets show TriFusion achieves over 99% accuracy, significantly surpassing SOTA approaches.

**中文翻译：** 现有单模态方法难以利用跨模态的互补特征。本文提出 TriFusion，一种带自监督学习的双层级多模态框架。TriFusion通过构建流量图像、图和时序序列，联合建模包内和包间依赖关系。在包级别构建流量图像和图，每个字节同时对应图像像素和图节点。设计基于SSL的编码器处理包级别模态。在ISCX-VPN和CICIoT数据集上的实验表明TriFusion达到99%+准确率，显著超越SOTA。

## §3 方法动机

**痛点：**
- 单模态方法无法捕获跨模态互补信息
- 现有多模态方法存在三个不足：(1)包内细粒度建模不足；(2)区域感知表示弱；(3)忽略包间时序依赖
- 标注数据稀缺，需要利用无标注数据

**核心直觉：**
- 每个字节在包中同时具有语义信息（作为图像像素）和结构关系（作为图节点）
- 包级别的图像和图提供互补视角
- 流级别的时序序列表征包间依赖
- SSL预训练可利用大量无标注数据学习鲁棒表示

## §4 方法设计

**整体流程：** 原始包 → 包级别图像构建(三通道) + 包级别图构建 → SSL编码器 → 多模态特征融合 → 流级别时序建模 → 分类

**关键模块：**

1. **包级别图像模态(PIM)：**
   - 区域感知图像构建：将包分解为header、payload、header-payload组合三个通道，每通道映射为H×W矩阵
   - MAE-based编码器：混合Transformer-CNN骨干，随机掩码重建预训练

2. **包级别图模态(PGM)：**
   - 每字节作为图节点，滑动窗口构建边连接
   - 异构GNN编码器，定制数据增强策略
   - 对比学习预训练

3. **多模态特征融合：** 融合包级别图像和图特征形成统一包表示

4. **流级别时序模态：** 创新性构建包间时序序列特征，丰富流量表示

**优点：** 细粒度包内建模（字节级）；区域感知表示；包间时序依赖建模；SSL利用无标注数据
**缺点：** 论文未明确说明图构建的计算开销和可扩展性

## §5 与其他方法对比

- 在 ISCX-VPN 和 ISCX-nonTor 数据集上比 App-Net 和 MIMETIC 超过20%准确率
- 相比现有单模态方法，利用了图像语义、图结构和时序三种互补模态
- SSL预训练减少了对标注数据的依赖

## §6 实验表现

**数据集：** ISCX-VPN, CICIoT, ISCX-nonTor（共7个benchmark数据集）
**指标：** Accuracy
**关键结果：**
- ISCX-VPN 和 CICIoT 上超过99%准确率
- 比 App-Net 和 MIMETIC 超过20%准确率（ISCX-VPN, ISCX-nonTor）

## §7 学习与应用

- **开源代码：** 论文未明确提供
- **可复现性：** 方法描述包含详细的图像构建和图构建过程
- **迁移价值：** 字节级图像-图联合表示可推广到其他需要细粒度分析的序列分类任务；SSL预训练策略适用于标注稀缺场景

## §8 总结

**核心思想：** 在包级别将每个字节同时映射为图像像素和图节点，通过SSL预训练的MAE编码器和GNN编码器分别提取语义和结构特征，再融合流级别时序特征，实现多层级多模态的流量分类。

**快速流水线：**
```
原始包 → 三通道区域感知图像(H×W×3) + 字节级图
  → MAE-based图像编码器(SSL预训练) → 图像特征
  → 异构GNN编码器(对比学习预训练) → 图特征
  → 多模态融合 → 统一包表示
  → 流级别时序建模 → 分类
```

## §9 知识链接

- [[encrypted-traffic-analysis]] — 加密流量分析
- [[traffic-classification]] — 流量分类
- [[multi-modal-fusion]] — 多模态融合
- [[graph-neural-network]] — GNN编码器
- [[self-supervised-learning]] — SSL预训练
- [[contrastive-learning]] — 图编码器的对比学习
- [[transformer]] — MAE编码器中的Transformer
- [[traffic-representation-learning]] — 流量表示学习

## §10 证据记录

| 声明 | 证据 |
|------|------|
| 单模态方法无法捕获跨模态互补信息 | §1文献分析 |
| 每字节同时具有语义和结构信息 | §2.1图像-图联合表示设计 |
| ISCX-VPN上99%+准确率 | 实验结果 |
| 比App-Net/MIMETIC超20%准确率 | 实验对比 |

## §11 原始资料链接

- PDF: `00-inbox/PDFs/2026-ICASSP-TriFusion_A_Self-Supervised_Learning_Enhanced_Dual-Level_Multimodal_Framework_for_Traffic_Classification.pdf`
- MinerU MD: `02-parsed-markdown/2026-ICASSP-TriFusion_A_Self-Supervised_Learning_Enhanced_Dual-Level_Multimodal_Framework_for_Traffic_Classification.md`

## §12 后续问题

- 图构建的计算复杂度如何？在长包场景下是否可扩展？
- 三个模态的融合策略是否有更优设计（如注意力融合）？
- SSL预训练的数据量需求如何？小规模预训练数据下性能衰减多少？

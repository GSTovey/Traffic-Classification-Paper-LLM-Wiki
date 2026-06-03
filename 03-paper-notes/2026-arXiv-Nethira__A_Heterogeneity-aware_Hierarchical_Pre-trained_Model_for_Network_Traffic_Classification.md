---
type: paper
title_original: "Nethira: A Heterogeneity-aware Hierarchical Pre-trained Model for Network Traffic Classification"
title_cn: "Nethira：异质性感知的层次化预训练网络流量分类模型"
authors: [Chungang Lin, Weiyao Zhang, Haitong Luo, Xuying Meng, Yujun Zhang]
year: 2026
venue: "arXiv"
doi: "unknown"
url: "https://arxiv.org/abs/2605"
pdf: "00-inbox/PDFs/2026-arXiv-Nethira__A_Heterogeneity-aware_Hierarchical_Pre-trained_Model_for_Network_Traffic_Classification.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-Nethira__A_Heterogeneity-aware_Hierarchical_Pre-trained_Model_for_Network_Traffic_Classification.md"
status: processed
reading_level: L2
research_area: [traffic-classification, pre-training]
task: [application-classification, malware-detection, attack-identification]
method: [hierarchical-reconstruction, consistency-regularization, transformer-encoder-decoder]
dataset: [ISCX-VPN-App, ISCX-VPN-Service, USTC-TFC, CIC-IoT]
code: "unknown"
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

# 2026-arXiv Nethira

## §0 基础信息

| 属性 | 值 |
|------|-----|
| 论文全称 | Nethira: A Heterogeneity-aware Hierarchical Pre-trained Model for Network Traffic Classification |
| 作者 | Chungang Lin, Weiyao Zhang, Haitong Luo, Xuying Meng, Yujun Zhang |
| 机构 | Institute of Computing Technology, Chinese Academy of Sciences; University of Chinese Academy of Sciences |
| 年份/会议 | 2026 / arXiv |
| 关键词 | pre-training, hierarchical reconstruction, traffic heterogeneity, consistency regularization |

## §1 一句话总结

提出 Nethira，一种异质性感知的层次化预训练模型，通过字节级、协议级、包级三层层次化重建预训练和一致性正则化微调策略，在四个公开数据集上平均 F1 达 90.40%，比七个预训练模型平均提升 9.11%，仅需 1% 标注数据即可达到可比性能。

## §2 摘要翻译

**原文摘要:**
Network traffic classification is vital for network security and management. The pre-training technology has shown promise by learning general traffic representations from raw byte sequences, thereby reducing reliance on labeled data. However, existing pre-trained models struggle with the gap between traffic heterogeneity (i.e., hierarchical traffic structures) and input homogeneity (i.e., flattened byte sequences). To address this gap, we propose Nethira, a heterogeneity-aware pre-trained model based on hierarchical reconstruction and augmentation. In pre-training, Nethira introduces hierarchical reconstruction at multiple levels—byte, protocol, and packet—capturing comprehensive traffic structural information. During fine-tuning, Nethira proposes a consistency-regularized strategy with hierarchical traffic augmentation to reduce label dependence. Experiments on four public datasets demonstrate that Nethira outperforms seven existing pre-trained models, achieving an average F1-score improvement of 9.11%, and reaching comparable performance with only 1% labeled data on high-heterogeneity network tasks.

**中文翻译:**
网络流量分类对网络安全和管理至关重要。预训练技术通过从原始字节序列学习通用流量表示展现出 promise，从而减少对标注数据的依赖。然而，现有预训练模型在流量异质性（即层次化流量结构）和输入同质性（即扁平化字节序列）之间存在差距。为解决这一差距，我们提出 Nethira，一种基于层次化重建和增强的异质性感知预训练模型。在预训练中，Nethira 在多个层次——字节、协议和包——引入层次化重建，捕获全面的流量结构信息。在微调中，Nethira 提出一致性正则化策略和层次化流量增强以减少标注依赖。四个公开数据集的实验表明，Nethira 优于七个现有预训练模型，平均 F1 提升 9.11%，且仅需 1% 标注数据即可在高异质性网络任务上达到可比性能。

## §3 方法动机

**痛点:**
- 现有预训练模型将流量扁平化为字节序列，破坏了流量的层次化结构
- 字节级预训练无法捕获协议字段和包间依赖等高层语义
- 在高异质性数据集（如 CIC-IoT）上，现有模型改进有限
- 标注数据稀缺，需要减少对标注的依赖

**核心直觉:**
- 流量异质性体现在多个层次：字节编码加密信息、协议字段编码传输状态、包序列编码动态行为
- 扁平化输入是同质的，但流量结构是异质的，需要层次化建模
- 通过层次化重建（字节/协议/包级掩码重建）可让模型感知层次结构
- 一致性正则化（对增强样本保持预测一致）可减少标注依赖

## §4 方法设计

**整体流程:**
```
Stage 1: 预训练
  原始流量 → 五元组分流 → 地址归零 + 长度标准化
  → 拼接前 M 包字节序列 → 三层层次化扰动:
    - 字节级: 随机掩码单字节
    - 协议级: 掩码连续字节段（对齐协议字段边界）
    - 包级: 包序扰动 + 随机掩码
  → Transformer encoder-decoder 重建 → 三层损失之和

Stage 2: 微调
  输入序列 → 三种增强:
    - 原始序列 x_raw
    - 协议级增强 x_protocol（随机化协议字段排列）
    - 包级增强 x_packet（扰动包序列）
  → Traffic Encoder + Decoder + MLP 分类器
  → 监督损失 L_sup + 一致性损失 L_cons
  → L_F = L_sup + lambda * L_cons
```

**核心模块:**

1. **层次化重建预训练**:
   - 字节级重建: 随机掩码字节位置，重建原始字节（类似 BERT MLM）
   - 协议级重建: 掩码对齐协议字段边界的连续字节段，学习跨协议通用表示
   - 包级重建: 扰动包序后掩码字节，学习包间动态行为
   - 总损失: L_P = L_byte + L_protocol + L_packet

2. **一致性正则化微调**:
   - 协议级增强: 随机化协议字段排列，防止依赖固定顺序
   - 包级增强: 扰动包序列，模拟网络动态（重排序、部分丢失）
   - KL 散度一致性: L_cons = D_KL(h_raw || h_protocol) + D_KL(h_raw || h_packet)
   - 总损失: L_F = L_sup + lambda * L_cons

3. **模型结构**:
   - Byte Embedding: 原始字节映射为高维向量
   - Traffic Encoder: 堆叠 Transformer 编码器，自注意力捕获全局字节级表示
   - Traffic Decoder: Transformer 解码器，自回归重建字节序列
   - 6 层编码器 + 6 层解码器，预训练 100K 步，lr=1e-4

**关键公式:**
- L_byte = -sum_{t in M_byte} log P_theta(b_t | masked sequence)
- L_protocol = -sum_{t in M_protocol} log P_theta(b_t | masked sequence)
- L_packet = -sum_{t in M_packet} log P_theta(b_t | masked sequence)
- L_cons = D_KL(h_raw || h_protocol) + D_KL(h_raw || h_packet)
- L_F = L_sup + lambda * L_cons (lambda=0.1)

**优缺点:**
- (+) 层次化重建捕获多级流量结构信息
- (+) 一致性正则化有效减少标注依赖
- (+) 仅需 1% 标注数据即可达到可比性能
- (+) 在高异质性数据集（CIC-IoT）上优势显著
- (-) 预训练计算开销较大（100K 步）
- (-) 固定 M=5 包、L=128 字节可能限制长流建模

## §5 与其他方法对比

**创新点:**
- 首个在预训练中引入字节/协议/包三级层次化重建的模型
- 一致性正则化微调策略，利用层次化增强减少标注依赖
- 显式建模流量异质性而非依赖扁平化字节序列

**与 baseline 对比:**
| 方法 | 预训练任务 | 异质性感知 | 少样本能力 |
|------|-----------|-----------|-----------|
| ET-BERT | MLM + NSP | 仅字节级 | 一般 |
| YaTC | 掩码重建 | 仅字节级 | 一般 |
| NetGPT | 语言建模 | 仅字节级 | 一般 |
| TrafficFormer | 协议字段随机化 | 字节级+协议 | 一般 |
| TraGe | 头/载荷区分 | 字节级 | 一般 |
| Nethira | 三级层次化重建 | 字节+协议+包 | 强 |

## §6 实验表现

**数据集:**
- 预训练: ET-BERT 开源语料
- 下游评估:
  - ISCX-VPN (App): 应用识别，12 类，2,329 样本
  - ISCX-VPN (Service): 服务识别，17 类，3,694 样本
  - USTC-TFC: 恶意流量分类，20 类，50,677 样本
  - CIC-IoT: IoT 攻击识别，6 类，22,634 样本

**评估指标:**
- Precision (PR), Recall (RC), F1-score (F1)

**关键结果:**
- Nethira 平均 F1 达 90.40%，比七个预训练模型平均提升 9.11%
  - ISCX-VPN (App): F1=75.55%（提升 11.49%，超过 TrafficFormer 71.69%）
  - ISCX-VPN (Service): F1=92.34%（提升 5.36%）
  - USTC-TFC: F1=96.40%（提升 1.52%）
  - CIC-IoT: F1=97.29%（提升 18.05%，最大提升）
- 仅 1% 标注数据: CIC-IoT 上 F1=0.9452，超过 TrafficFormer 100% 标注的 0.8912
- 消融实验（CIC-IoT）:
  - 去除预训练: -4.78%
  - 仅字节级预训练（去掉协议/包级）: -1.71%
  - 去除一致性正则化（仅监督微调）: -7.84%
- 高异质性（ANPF=12 的 CIC-IoT）提升最大，低异质性（ANPF=2 的 ISCX-VPN App）提升较小

## §7 学习与应用

**开源情况:**
- 论文未明确说明代码是否开源

**可复现性:**
- 使用 ET-BERT 开源预训练语料
- 四个公开数据集均有标准划分
- 超参数明确: M=5, L=128, 100K 预训练步, lambda=0.1

**迁移价值:**
- 层次化重建思路可应用于其他需要多粒度建模的序列任务
- 一致性正则化微调策略可推广到少样本场景
- 异质性感知设计对 IoT、VPN 等复杂流量场景特别有价值

## §8 总结

**核心思想:** 通过字节级、协议级、包级三级层次化重建预训练捕获流量异质性结构信息，结合一致性正则化微调策略减少标注依赖，在高异质性网络任务上实现显著性能提升。

**快速 Pipeline:**
```
原始流量 → 五元组分流 → 地址归零 + 长度标准化
  → 拼接前 M 包字节序列
  → 三级层次化扰动: 字节掩码/协议字段掩码/包序扰动
  → Transformer encoder-decoder 重建预训练
  → 微调: 三种增强序列 + 一致性正则化
  → MLP 分类 → 下游任务输出
```

## §9 知识链接

- [[traffic-classification]] — 网络流量分类核心任务
- [[pre-training-finetuning]] — 预训练-微调范式
- [[transformer]] — Transformer encoder-decoder 架构
- [[encrypted-traffic-analysis]] — 加密流量分析
- [[traffic-representation-learning]] — 流量表示学习

## §10 证据记录

| 关键声明 | 证据 | 可信度 |
|---------|------|--------|
| 平均 F1 提升 9.11% | Table 1 四数据集对比 | 高 |
| CIC-IoT 上提升 18.05% | Table 1 详细数据 | 高 |
| 1% 标注数据超过 100% baseline | Figure 2 少样本实验 | 高 |
| 去除一致性正则化下降 7.84% | Section 3.4 消融实验 | 高 |
| 高异质性数据集提升更大 | ANPF 分析 | 高 |

## §11 原始资料链接

- PDF: `00-inbox/PDFs/2026-arXiv-Nethira__A_Heterogeneity-aware_Hierarchical_Pre-trained_Model_for_Network_Traffic_Classification.pdf`
- MinerU MD: `02-parsed-markdown/2026-arXiv-Nethira__A_Heterogeneity-aware_Hierarchical_Pre-trained_Model_for_Network_Traffic_Classification.md`

## §12 后续问题

1. 协议级重建的字段边界如何自动确定？目前依赖启发式
2. 能否扩展到更多层次（如应用级、会话级）？
3. 包级扰动的策略是否可以更精细（如模拟丢包、重传）？
4. 在跨域迁移场景下表现如何？
5. 与 TrafficMoE 等异质性建模方法的对比？

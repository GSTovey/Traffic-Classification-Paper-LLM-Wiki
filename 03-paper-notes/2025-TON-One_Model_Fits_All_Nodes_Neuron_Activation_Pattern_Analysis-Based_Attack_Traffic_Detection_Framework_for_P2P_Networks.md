---
type: paper
title_original: "\"One Model Fits All Nodes\": Neuron Activation Pattern Analysis-Based Attack Traffic Detection Framework for P2P Networks"
title_cn: "一个模型适配所有节点：基于神经元激活模式分析的P2P网络攻击流量检测框架"
authors: ["Songsong Xu", "Chuanpu Fu", "Qi Li", "Ke Xu"]
year: 2025
venue: "TON"
doi: "10.1109/TON.2025.3546735"
url: "unknown"
pdf: "00-inbox/PDFs/2025-TON-One_Model_Fits_All_Nodes_Neuron_Activation_Pattern_Analysis-Based_Attack_Traffic_Detection_Framework_for_P2P_Networks.pdf"
mineru_md: "02-parsed-markdown/2025-TON-One_Model_Fits_All_Nodes_Neuron_Activation_Pattern_Analysis-Based_Attack_Traffic_Detection_Framework_for_P2P_Networks.md"
status: processed
reading_level: L2
research_area: ["malicious-traffic-detection", "anomaly-detection"]
task: ["false-positive-reduction", "attack-detection", "P2P-security"]
method: ["transformer", "neuron-activation-analysis", "meta-learning"]
dataset: ["Ethereum-real-nodes"]
code: "unknown"
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

## §0 基础信息

| 字段 | 内容 |
|------|------|
| 论文标题 | "One Model Fits All Nodes": Neuron Activation Pattern Analysis-Based Attack Traffic Detection Framework for P2P Networks |
| 作者 | Songsong Xu, Chuanpu Fu, Qi Li, Ke Xu |
| 机构 | Tsinghua University |
| 年份/期刊 | 2025 / IEEE TON |
| DOI | 10.1109/TON.2025.3546735 |

## §1 一句话总结

提出 tNeuron 系统，通过分析 Transformer 影子模型的神经元激活模式来自动识别攻击流量检测中的误报（FP），使单一ML模型能在P2P网络所有节点上有效部署，无需人工标注FP。

## §2 摘要翻译

**原始摘要：** ML-based network attack traffic detection is an emerging security paradigm. When deploying such models to protect P2P services, one detection model should be deployed on many nodes. However, unseen yet benign traffic patterns are commonly classified as attack traffic, triggering massive false-positive alarms. We present tNeuron that automatically identifies FPs triggered by unseen traffic via neuron activation pattern analysis. We construct a shadow model with Transformer encoders to extract traffic pattern knowledge, then train a model to classify FPs among alarms according to neuron activation patterns. Experiments on real Ethereum nodes show tNeuron can reduce 83.40% FP for seven state-of-the-art ML-based attack detection systems.

**中文翻译：** 基于ML的网络攻击流量检测是一种新兴安全范式。当部署此类模型保护P2P服务时，一个检测模型需部署在多个节点上。然而，未见过的良性流量模式常被误分类为攻击流量，产生大量误报。本文提出 tNeuron，通过神经元激活模式分析自动识别由未见流量触发的误报。构建基于Transformer编码器的影子模型提取流量模式知识，然后训练模型根据神经元激活模式分类告警中的误报。在真实以太坊节点上的实验表明，tNeuron可为7种SOTA攻击检测系统减少83.40%的误报。

## §3 方法动机

**痛点：**
- P2P网络中部署单一ML模型到多个节点时，各节点配置/工作负载不同导致流量模式差异巨大
- 未见过的良性流量被误判为攻击，产生海量FP（每小时13K+告警）
- 逐节点收集数据并重新训练模型成本过高，不可扩展
- 手动识别FP的人工成本在大规模P2P网络中不可行

**核心直觉：**
- 受脑科学启发：人脑疲劳状态反映在神经元化学状态上
- 类似地，模型对未见样本的欠拟合状态（导致FP）可通过分析神经元激活模式来识别
- 未见P2P流量触发的异常激活模式 vs 正确分类时的正常激活模式存在显著差异

## §4 方法设计

**整体流程：** 原始流量 → 流量特征提取 → ML检测模型产生告警 → 影子模型(Transformer)执行 → 神经元激活模式分析 → 分类告警为TP/FP

**关键模块：**

1. **影子模型构建：** 基于Transformer编码器，通过masked field prediction预训练，包含大量神经元供分析
2. **神经元激活模式分析：** 无监督学习方式训练，学习Transformer编码器的激活模式
3. **FP检测：** 检查神经元是否被正确激活——异常激活=未见模式=可能是FP；正常激活=已学习模式=可能是TP

**设计目标：**
- 通用FP检测：适用于多种检测方法（有监督/无监督）
- 准确FP检测：不将TP误判为FP（防止攻击者逃逸）
- 实时FP检测：低延迟（0.0164s），高吞吐（12.82K/秒）
- 鲁棒FP检测：保持原模型对抗鲁棒性
- 零人工成本：无需人工标注FP

**优点：** 与原检测模型独立，通用性强；无需集中式P2P网络视图；无监督训练无需标注
**缺点：** 论文未明确说明在极端不平衡场景（FP远多于TP）下的性能边界

## §5 与其他方法对比

- 现有方法依赖手动识别FP后重训练，tNeuron完全自动化
- tNeuron是首个为P2P网络减少ML检测系统精度损失的系统
- 影子模型独立于原始检测模型，可增强任意检测方法

## §6 实验表现

**数据集：** 真实以太坊节点流量（8个节点，不同位置/软件/硬件配置），15种P2P网络攻击
**基线：** 7种SOTA攻击检测系统（涵盖flow-based, packet-based, host-based, 有监督/无监督）
**指标：** FPR, F1, 以及9种精度指标
**关键结果：**
- 减少83.40% FP（7种检测系统平均）
- FPR降低6.35%-15.31%
- 检测延迟仅0.0164s，吞吐12.82K告警/秒
- 对对抗样本保持鲁棒性（不降低原模型鲁棒性）

## §7 学习与应用

- **开源代码：** 论文未提供代码链接
- **可复现性：** 使用真实以太坊节点数据，实验设置详细
- **迁移价值：** 神经元激活模式分析思路可迁移到其他分布式部署场景（如IoT、边缘计算）中解决模型泛化问题

## §8 总结

**核心思想：** 通过分析Transformer影子模型的神经元激活模式，自动区分ML检测系统告警中的真阳性和误报，使单一模型能在P2P网络所有节点上有效工作。

**快速流水线：**
```
流量特征 → ML检测模型 → 告警(TP/FP混合)
  → Transformer影子模型执行
  → 提取神经元激活模式
  → 无监督FP分类器 → 分离TP和FP
  → (可选)利用识别的FP进行模型微调
```

## §9 知识链接

- [[malicious-traffic-detection]] — 恶意流量检测
- [[anomaly-detection]] — 异常检测
- [[transformer]] — Transformer编码器作为影子模型
- [[traffic-classification]] — 流量分类

## §10 证据记录

| 声明 | 证据 |
|------|------|
| 单一模型部署到不同节点导致F1下降7.69%-56.88% | Fig.1(a)实验数据 |
| 不同节点配置(Rust/Java)和地理位置导致不同流量模式 | Fig.1(b)(c)特征空间可视化 |
| 现有系统每小时产生13K+ FP | §II Problem Statement实证数据 |
| tNeuron减少83.40% FP | 实验结果 |

## §11 原始资料链接

- PDF: `00-inbox/PDFs/2025-TON-One_Model_Fits_All_Nodes_Neuron_Activation_Pattern_Analysis-Based_Attack_Traffic_Detection_Framework_for_P2P_Networks.pdf`
- MinerU MD: `02-parsed-markdown/2025-TON-One_Model_Fits_All_Nodes_Neuron_Activation_Pattern_Analysis-Based_Attack_Traffic_Detection_Framework_for_P2P_Networks.md`

## §12 后续问题

- 神经元激活模式分析在其他类型深度学习模型（非Transformer）上的效果如何？
- 当攻击者刻意模仿正常激活模式时，系统的鲁棒性如何？
- 能否将该方法与联邦学习结合，在保护隐私的同时实现跨节点FP检测？

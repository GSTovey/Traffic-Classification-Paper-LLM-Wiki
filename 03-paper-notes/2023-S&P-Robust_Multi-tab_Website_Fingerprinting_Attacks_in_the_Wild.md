---
type: paper
title_original: "Robust Multi-tab Website Fingerprinting Attacks in the Wild"
title_cn: "野外环境中鲁棒的多标签网站指纹攻击"
authors: [Xinhao Deng, Qilei Yin, Zhuotao Liu, Xiyuan Zhao, Qi Li, Mingwei Xu, Ke Xu, Jianping Wu]
year: 2023
venue: "S&P"
doi: "unknown"
url: "unknown"
pdf: "00-inbox/PDFs/2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild.pdf"
mineru_md: "02-parsed-markdown/2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild.md"
status: processed
reading_level: L2
research_area: [website-fingerprinting, encrypted-traffic-analysis]
task: [multi-tab-website-fingerprinting, tor-traffic-analysis]
method: [transformer, multi-label-classification, sliding-window]
dataset: [500K-multi-tab-sessions, tor-browsing-dataset]
code: "unknown"
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

## §0 基础信息

| 项目 | 内容 |
|------|------|
| 论文全称 | Robust Multi-tab Website Fingerprinting Attacks in the Wild |
| 作者 | Xinhao Deng, Qilei Yin, Zhuotao Liu, Xiyuan Zhao, Qi Li, Mingwei Xu, Ke Xu, Jianping Wu |
| 机构 | 清华大学, 中关村实验室 |
| 发表时间 | 2023 |
| 会议 | IEEE S&P 2023 |

## §1 一句话总结

提出ARES框架，将多标签网站指纹攻击建模为多标签分类问题，利用基于Transformer的Trans-WF模型从多个短流量段中提取局部模式，在50万+多标签Tor浏览会话上实现最佳F1分数0.907，即使打开5个标签页仍能达到0.805 F1分数。

## §2 摘要翻译

**原始摘要：**
Website fingerprinting enables an eavesdropper to determine which websites a user is visiting over an encrypted connection. State-of-the-art website fingerprinting (WF) attacks have demonstrated effectiveness even against Tor-protected network traffic. However, existing WF attacks have critical limitations on accurately identifying websites in multi-tab browsing sessions, where the holistic pattern of individual websites is no longer preserved, and the number of tabs opened by a client is unknown a priori. In this paper, we propose ARES, a novel WF framework natively designed for multi-tab WF attacks. ARES formulates the multi-tab attack as a multi-label classification problem and solves it using a multi-classifier framework. Each classifier, designed based on a novel transformer model, identifies a specific website using its local patterns extracted from multiple traffic segments. We implement a prototype of ARES and extensively evaluate its effectiveness using our large-scale dataset collected over multiple months (by far the largest multi-tab WF dataset studied in academic papers.) The experimental results illustrate that ARES effectively achieves the multi-tab WF attack with the best F1-score of 0.907. Further, ARES remains robust even against various WF defenses.

**中文翻译：**
网站指纹识别使窃听者能够确定用户通过加密连接访问哪些网站。最先进的网站指纹攻击已被证明对Tor保护的网络流量也有效。然而，现有WF攻击在准确识别多标签浏览会话中的网站方面存在关键限制，其中单个网站的整体模式不再保留，且客户端打开的标签数量是未知的。本文提出ARES，一种专为多标签WF攻击设计的新颖框架。ARES将多标签攻击建模为多标签分类问题，并使用多分类器框架解决。每个分类器基于新颖的Transformer模型设计，使用从多个流量段中提取的局部模式识别特定网站。作者实现了ARES原型，并使用数月收集的大规模数据集（迄今为止学术论文中研究的最大多标签WF数据集）广泛评估其有效性。实验结果表明ARES有效地实现了多标签WF攻击，最佳F1分数为0.907。此外，ARES即使面对各种WF防御也保持鲁棒性。

## §3 方法动机

**痛点问题：**
- 现有WF攻击假设单标签浏览，不适用于实际多标签场景
- 多标签浏览会话中，单个网站的整体流量模式被破坏
- 现有方法需要预先知道打开的标签数量
- 现有方法对WF防御机制不鲁棒

**核心直觉：**
- 即使整体模式被破坏，仍可从多个短流量段中提取局部模式
- 网站的HTML元素与局部流量模式相关
- 可以将多标签攻击建模为多标签分类问题

**方法动机：**
- 需要不依赖标签数量的通用多标签WF攻击方法
- Transformer模型可以捕获局部模式之间的相关性
- 多分类器框架可以并行训练和更新

## §4 方法设计

**整体流程：**

```
输入: 多标签Tor浏览会话（方向序列）
  ↓
Step 1: 方向序列提取
  - 出站包: +1
  - 入站包: -1
  ↓
Step 2: 流量分割（Traffic Division）
  - 使用多个滑动窗口（不同起始位置）
  - 将方向序列分割为多个流量段
  - 保留局部模式的完整性
  ↓
Step 3: 局部模式提取（Local Profiling）
  - 基于CNN的局部特征提取器
  - 多个Conv1d + BatchNorm + ReLU块
  - 残差连接防止梯度消失
  - Dropout防止过拟合
  - MaxPooling保留最具代表性的特征
  ↓
Step 4: 网站识别（Website Identification）
  - 改进的自注意力机制
  - 计算局部特征之间的相关性
  - 每个Trans-WF识别一个特定网站
  ↓
Step 5: 多标签分类
  - N个Trans-WF并行运行（N=监控网站数）
  - Softmax层整合结果
  - 基于阈值输出标签集
  ↓
输出: 访问的网站标签集
```

**关键公式：**
- 流量分割: S = {W_1,...,W_n}，W_i为第i个滑动窗口的段集
- 自注意力: 计算局部特征之间的相关性
- 多标签分类: 基于阈值的二分类决策

**优势：**
- 不依赖标签数量，适用于动态多标签场景
- 对WF防御鲁棒
- 可并行训练和更新分类器
- 局部模式提取对噪声具有鲁棒性

**局限：**
- 需要大量训练数据
- 计算复杂度较高
- 论文未明确说明在极端防御下的性能

## §5 与其他方法对比

**创新点：**
1. 首次将多标签WF攻击建模为多标签分类问题
2. 设计基于Transformer的Trans-WF模型提取局部模式
3. 使用多分类器框架，不依赖标签数量
4. 构建最大的多标签WF数据集（50万+实例）

**与基线对比：**
- 对比方法:
  - k-FP (k-NN based)
  - CUMUL (SVM based)
  - AWF (CNN based)
  - DF (Deep Fingerprinting)
  - Tik-tok
  - MWF (Multi-tab WF)
  - CWF (Chunk-based WF)
  - BAPM
- 改进点:
  - 通用性: 不依赖标签数量
  - 鲁棒性: 对WF防御更鲁棒
  - 实用性: 考虑真实世界复杂性
  - 准确率: F1分数0.907

## §6 实验表现

**数据集：**
- 50万+多标签Tor浏览会话
- 收集时间: 2021年5月-2022年11月
- 考虑多种真实世界复杂性:
  - 多个Tor版本共存
  - 访问子页面（不仅是主页）
  - 不同流量收集位置
  - 真实Tor用户流量

**评估指标：**
- F1分数
- 准确率 (Accuracy)
- 精确率 (Precision)
- 召回率 (Recall)

**主要结果：**
- 最佳F1分数: 0.907
- 5个标签页时: F1分数0.805，比基线提升260.4%
- 对WF防御鲁棒性: 性能下降较小
- 封闭世界和开放世界场景均有效

**关键发现：**
- ARES在多标签场景下显著优于现有方法
- 即使打开5个标签页仍保持较高准确率
- 对WTF-PAD和Front等防御机制具有鲁棒性
- 局部模式提取方法有效

## §7 学习与应用

**开源情况：**
- 论文提到发布大规模多标签数据集，但未明确说明是否开源代码

**复现要点：**
- 需要Tor浏览流量数据
- 需要实现Trans-WF模型（Transformer + CNN）
- 需要设计多分类器框架
- 需要调整滑动窗口和阈值参数

**迁移价值：**
- 方法可应用于其他匿名网络的网站指纹识别
- 多标签分类思路可扩展到其他流量分析任务
- 局部模式提取方法可应用于其他序列分析

## §8 总结

**核心思想：** 将多标签网站指纹攻击建模为多标签分类问题，利用基于Transformer的Trans-WF模型从多个短流量段中提取局部模式，实现不依赖标签数量的鲁棒攻击。

**快速流程：**
```
多标签Tor浏览会话 → 方向序列提取
    ↓
滑动窗口分割 → CNN局部特征提取 → Transformer自注意力
    ↓
N个Trans-WF并行 → Softmax整合 → 多标签分类结果
```

## §9 知识链接

- [[website-fingerprinting]] - 网站指纹识别技术
- [[encrypted-traffic-analysis]] - 加密流量分析方法
- [[transformer]] - Transformer模型
- multi-label-classification - 多标签分类方法
- tor-traffic-analysis - Tor流量分析
- sliding-window - 滑动窗口方法
- local-pattern-extraction - 局部模式提取
- privacy-preservation - 隐私保护研究

## §10 证据记录

| 声明 | 证据 | 证据强度 |
|------|------|----------|
| 多标签场景下现有方法性能下降 | 基线方法对比实验 | 强（实验数据） |
| ARES最佳F1分数0.907 | 大规模数据集实验 | 强（实验数据） |
| 5个标签页时F1分数0.805 | 多标签数量实验 | 强（实验数据） |
| 对WF防御具有鲁棒性 | 防御对抗实验 | 强（实验数据） |
| 局部模式提取方法有效 | 消融实验 | 强（实验验证） |

## §11 原始资料链接

- PDF: `00-inbox/PDFs/2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild.pdf`
- MinerU MD: `02-parsed-markdown/2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild.md`

## §12 后续问题

1. 滑动窗口大小和数量如何自动优化？
2. 对于更多标签页（如10+）的场景，方法的可扩展性如何？
3. 是否可以结合半监督学习减少训练数据需求？
4. 对于新型WF防御机制的效果如何？
5. 如何设计更有效的防御机制对抗此类攻击？

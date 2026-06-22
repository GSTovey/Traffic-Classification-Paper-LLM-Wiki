---
type: paper
reading_level: L3
relevance: high
year: 2024
venue: "USENIX Security 2024"
title_original: "Stop! Don't Click Here Anymore: Boosting Website Fingerprinting By Considering Sets of Subpages"
title_cn: "通过考虑子页面集合提升网站指纹攻击"
authors:
  - Asya Mitseva
  - Andriy Panchenko
year: 2024
venue_target: "USENIX Security 2024"
publication_status: published
doi: ""
url: "https://www.usenix.org/conference/usenixsecurity24/presentation/mitseva"
pdf: ""
mineru_md: "02-parsed-markdown/2024-USENIX-Stop__Don't_Click_Here_Anymore__Boosting_Website_Fingerprinting_By_Considering_Sets_of_Subpages.md"
status: deep-analyzed
research_area:
  - website-fingerprinting
  - encrypted-traffic-analysis
  - traffic-classification
task:
  - website-fingerprinting
method:
  - multiple-instance-learning
  - voting-strategies
  - hidden-markov-model
dataset:
  - ALEXA-WSC-FG
  - TRANCO-WSC-FG
  - ALEXA-WSC-BG
  - ALEXA-WSC-HMM
code: "https://www.informatik.tu-cottbus.de/~andriy/zwiebelfreunde/methods-usenix-sec-2024/"
my_confidence: high
related_papers:
  - "[[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]]"
  - "[[2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild]]"
  - "[[2020-CCS-TrafficSliver-Fighting_Website_Fingerprinting_Attacks_with_Traffic_Splitting]]"
  - "[[2024-S&P-Real-Time_Website_Fingerprinting_Defense_via_Traffic_Cluster_Anonymization]]"
kb_read_only: true
promoted_to: ""
created: 2026-06-21
updated: 2026-06-21
---

# Stop! Don't Click Here Anymore: Boosting Website Fingerprinting By Considering Sets of Subpages

> **深度分析笔记** — 本笔记已完成 L3 深度分析。
> `kb_read_only: true`：本笔记可链接到主知识库页面，但不会触发主知识库的任何更新。
> 如需晋升至主知识库，须满足 `publication_status: published/accepted` + `my_confidence: high` + 用户主动要求。

---

## 0. 基础信息

| 字段 | 内容 |
|---|---|
| 标题 | Stop! Don't Click Here Anymore: Boosting Website Fingerprinting By Considering Sets of Subpages |
| 作者 | Asya Mitseva, Andriy Panchenko |
| 年份 | 2024 |
| 目标/发表 venue | USENIX Security 2024 |
| 发表状态 | published |
| DOI | - |
| 关键词 | Website Fingerprinting, Multiple Instance Learning, Voting Strategies, Tor, Traffic Analysis |
| 数据集 | ALEXA-WSC-FG, TRANCO-WSC-FG, ALEXA-WSC-BG, ALEXA-WSC-HMM |
| 代码仓库 | https://www.informatik.tu-cottbus.de/~andriy/zwiebelfreunde/methods-usenix-sec-2024/ |
| 研究方向 | [[website-fingerprinting]], [[encrypted-traffic-analysis]] |
| Confidence | high |
| 晋升状态 | 未晋升 |

---

## 1. 一句话总结

> 本文提出基于多实例学习（MIL）和投票策略的新型网站指纹攻击方法，通过分析用户在同一网站内连续访问多个子页面的流量模式，在现实场景中实现 F1-score 达到 1.0 的检测精度，比现有方法提升 2.5-5 倍。

---

## 2. 核心贡献

### 2.1 贡献列表

1. **首次系统性分析现有网页分类器用于网站指纹的适用性**：发现将网页分类器直接应用于网站指纹会导致 20-30% 的精度下降，揭示了现有方法的局限性。

2. **提出基于多实例学习（MIL）的新型网站指纹攻击**：设计了一个端到端的深度学习架构，将同一网站的多个子页面流量作为一个"包"（bag）进行处理，自动学习页面间的权重关系。

3. **设计六种投票策略适配现有分类器**：包括多数投票、概率投票、均值投票以及三种加权均值投票（方差加权、标准差加权、基尼系数加权），无需修改底层分类器即可提升网站指纹精度。

4. **首次评估网站指纹对现有防御的鲁棒性**：证明在考虑多页面浏览后，WTF-PAD 和 FRONT 等防御变得几乎无效，Tamaraw 等强防御的保护效果也降低 2.5-5 倍。

5. **提出用户风险评估机制**：方法可估计用户在网站内连续访问页面的风险，并在攻击达到临界置信度前提醒用户停止。

### 2.2 与领域已有工作的关键区别

| 已有工作 | 差异点 | 位置 |
|---|---|---|
| [[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]] | DF 仅检测单个页面，本文扩展到网站级别检测 | §3, §4.2 |
| [[2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild]] | Deng et al. 考虑多标签分类处理多标签页，本文聚焦同一网站内顺序浏览 | §3, §6.4 |
| Cai et al. [7] 的 HMM 方法 | 仅分析两个网站，本文扩展到 100 个网站并分析页面数量影响 | §3, §4.3 |
| GANDaLF [37] | GANDaLF 网站指纹精度仅 62%，本文方法在开放世界达到 F1=1.0 | §3, §6.2.3 |

---

## 3. 研究连接（Research Connection）

### 3.1 相关概念

- [[website-fingerprinting]]
- [[encrypted-traffic-analysis]]
- [[traffic-classification]]

### 3.2 相关方法

- [[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]] (DF)
- [[2020-CCS-TrafficSliver-Fighting_Website_Fingerprinting_Attacks_with_Traffic_Splitting]]
- [[2024-S&P-Real-Time_Website_Fingerprinting_Defense_via_Traffic_Cluster_Anonymization]]

### 3.3 相关任务

- [[website-fingerprinting]]

### 3.4 基于哪些已有论文

- [[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]]
- [[2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild]]
- [[2020-CCS-TrafficSliver-Fighting_Website_Fingerprinting_Attacks_with_Traffic_Splitting]]

### 3.5 与已有 Claims 的关系

| 已有 Claim | 本论文的关系 | 位置 |
|---|---|---|
| 现有 WFP 攻击在现实场景中可扩展性有限 | 挑战：证明通过多页面浏览可显著提升现实场景检测能力 | §6.2.3 |
| Tor 匿名网络对 WFP 攻击有一定防御能力 | 挑战：证明现有防御在多页面场景下效果大幅降低 | §6.3 |
| 深度学习方法在 WFP 中优于传统方法 | 扩展：证明 MIL 方法在小数据集下更具优势 | §6.2.2 |

---

## 4. 关键发现与证据

### 4.1 主要实验结果

| 任务/数据集 | 指标 | 本方法 | 最优 Baseline | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| 闭合世界 (ALEXA-WSC-FG) | Accuracy | 99.9% (9 pages) | 76.36% (单页面) | +23.5% | Var-CNN + 概率投票 |
| 开放世界 (5000 背景网站) | F1-score=1.0 比例 | ~60% (3 clicks) | ~0% (单页面) | 从无到有 | MIL-based 方法 |
| 开放世界 (5000 背景网站) | F1-score=1.0 比例 | ~75% (6 clicks) | ~0% (单页面) | 从无到有 | MIL-based 方法 |
| 对抗 WTF-PAD 防御 | Accuracy | 100% (4+ pages) | 90.72% (单页面) | +9.3% | Voting + DF |
| 对抗 FRONT 防御 | Accuracy | 100% (9 pages) | 67.00% (单页面) | +33% | Voting + DF |
| 对抗 Tamaraw 防御 | Accuracy | ~20% (9 pages) | 4.61% (单页面) | +15.3% | 约 5 倍提升 |
| 对抗 RegulaTor 防御 | Accuracy | 64.87% (9 pages) | 17.17% (单页面) | +47.7% | 约 4 倍提升 |

### 4.2 关键发现

1. **2-3 次点击即显著提升精度**：在闭合世界中，仅需在同一网站内点击 2-3 个链接，即可将检测精度提升 20% 以上，达到 90%+ 准确率。

2. **MIL 方法在小数据集下表现优异**：当仅有 30 个训练页面时，MIL 方法仅需 2 个训练包即可达到 70% 准确率，比 Var-CNN 高 20%，比 DF 高 16 倍。

3. **页面访问顺序非关键因素**：HMM 方法（考虑顺序）无法超越最佳投票策略（不考虑顺序），证明页面集合本身比访问顺序更重要。

4. **现有防御大幅失效**：WTF-PAD 和 FRONT 在 4 次以上页面访问后完全失效；即使是最强的 Tamaraw，保护效果也降低约 5 倍。

5. **训练页面多样性比数量更重要**：在小数据集场景下，使用多个不同页面训练比使用单页面多次训练更有效。

---

## 5. 质量与信心评估

### 5.1 当前状态

| 维度 | 状态 | 备注 |
|---|---|---|
| 实验完整性 | 完整 | 覆盖闭合/开放世界、6 种防御、4 个数据集 |
| 写作完整性 | 完整 | 逻辑清晰，实验充分 |
| 方法创新性 | 高 | MIL+投票策略是新颖的组合方法 |
| 实验说服力 | 强 | 在多个数据集和 Tor 浏览器版本上验证 |
| 与已有工作的区分度 | 明确 | 清晰区分网页 vs 网站指纹 |

### 5.2 需要改进的地方

1. **多标签页场景未深入**：仅讨论单标签页场景，多标签页下的方法扩展未充分探索。
2. **噪声页面敏感性**：MIL 方法对噪声页面（非目标网站页面）较敏感，4 个噪声页面导致精度下降 30%。
3. **实时攻击可行性**：未讨论如何在实际 Tor 网络中实时分割和识别用户浏览的页面序列。

### 5.3 是否可以考虑提交/晋升？

> [x] 方法论完整
> [x] 实验覆盖足够
> [x] 写作达到可读标准
> [x] 与已有工作区分度明确
> [x] 局限性已诚实讨论

---

## 6. 开放问题与后续计划

### 6.1 本文遗留的问题

- 如何在多标签页场景下应用本文方法？
- 如何在实际 Tor 网络中实时分割用户浏览的页面序列？
- 如何进一步提高 MIL 方法对噪声页面的鲁棒性？

### 6.2 下一步研究方向

- 将本文方法与多标签页 WFP 攻击（如 Deng et al. [14]）结合
- 探索更鲁棒的噪声页面过滤机制
- 研究实时页面序列分割技术

### 6.3 与我的研究主线的关系

> 本文在我的研究轨迹中处于 [[website-fingerprinting]] 攻击方法演进的关键位置，展示了从单页面检测到网站级别检测的范式转变，对未来防御设计和攻击评估具有重要参考价值。

---

## 7. [深度分析] 方法设计详解

### 7.1 方法整体流程

本文提出三种互补的网站指纹方法：
1. **投票策略**：复用现有网页分类器，通过六种投票机制聚合多个页面的预测结果
2. **MIL 方法**：端到端深度学习，将多页面流量作为"包"处理，自动学习页面权重
3. **HMM 方法**：利用页面访问顺序信息，通过隐马尔可夫模型建模网站浏览模式

### 7.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| 1. 流量收集 | 用户浏览的多个页面 | 收集 Tor 流量轨迹 | 多个页面的流量序列 | 获取原始数据 |
| 2. 特征提取 (MIL) | 流量序列 | 8 层 CNN + BatchNorm + Dropout | 特征向量 | 降维并提取特征 |
| 3. 包创建 (MIL) | 多个页面的特征向量 | 将同一网站的页面分为一个 bag | 训练/测试 bag | 构建 MIL 训练单元 |
| 4. 权重学习 (MIL) | Bag 内的特征向量 | 自定义层计算权重 + Softmax 归一化 | 页面权重 | 自动学习页面重要性 |
| 5. 加权聚合 (MIL) | 权重 + 原始特征 | 权重与特征相乘并展平 | 网站级特征 | 聚合多页面信息 |
| 6. 预测 | 网站级特征 | 全连接层 + Softmax | 网站类别概率 | 最终分类 |

### 7.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 特征生成器 (Feature Generator) | 从原始流量提取特征 | 流量序列 (5000 维) | 特征向量 (100 维) | 为权重学习器提供输入 |
| 权重学习器 (Weights Learner) | 计算每个页面的权重 | Bag 内的特征向量 | 归一化权重 | 输出用于加权聚合 |
| 自定义层 | 实现 tanh + softmax 权重计算 | 特征向量 | 权重值 | 核心创新点 |
| 网页分类器 (Voting) | 对单页面进行分类 | 单页面特征 | 类别概率 | 为投票策略提供基础预测 |

### 7.4 公式、算法和机制解释

**投票策略**：
- **多数投票**：选择预测次数最多的网站类别
- **概率投票**：将各页面的概率相乘，选择最高概率的网站
- **均值投票**：计算各页面概率的算术平均
- **加权均值投票**：使用方差/标准差/基尼系数作为权重

**MIL 权重计算**：
- 使用 tanh 激活函数分别处理入站和出站包
- Softmax 确保每个 bag 内权重和为 1
- 权重与原始特征相乘后展平，输入最终分类层

**HMM 方法**：
- 使用 DBSCAN 聚类将页面分组为 HMM 状态
- 从站点图和用户会话学习转移概率
- 使用 Viterbi 算法找到最可能的状态序列

---

## 8. [深度分析] 实验详细分析

### 8.1 实验设计和设置

- **评估策略**：两种策略——"已知页面"（训练包含所有页面）和"未知页面"（测试页面未在训练中出现）
- **交叉验证**：10 折交叉验证，基于每页轨迹数或每网站页面数
- **基线分类器**：CUMUL、k-FP、DF、Var-CNN
- **防御方法**：Tamaraw、CS-Buflo、WTF-PAD、TrafficSliver-Net、FRONT、RegulaTor

### 8.2 数据集详情

| 数据集 | 网站数 | 页面数/网站 | 轨迹数/页面 | 用途 |
|---|---|---|---|---|
| ALEXA-WSC-FG | 100 (Alexa Top) | 90 (80 链接 + 10 Google) | 90 (非索引) / 20 (索引) | 主要评估 |
| TRANCO-WSC-FG | 100 (Tranco Top) | 90 | 1 | 验证集 |
| ALEXA-WSC-BG | 5000 | 9 | 1 | 开放世界背景 |
| ALEXA-WSC-HMM | 100 | 50 + 10 会话 | 20 | HMM 评估 |

### 8.3 Baseline 选择理由

- **CUMUL**：传统 ML 代表，基于累积包大小特征 + SVM
- **k-FP**：传统 ML 代表，基于随机决策森林 + k-NN
- **DF**：深度学习代表，基于 CNN
- **Var-CNN**：深度学习代表，基于 ResNet + 手工特征

### 8.4 消融实验

- **训练页面数量影响**：从 1 到 90 个训练页面，观察精度变化
- **训练轨迹数量影响**：每页面 1-90 个轨迹，观察精度变化
- **训练包数量影响 (MIL)**：1-40 个训练包，观察精度变化
- **投票策略对比**：6 种投票策略的精度对比

### 8.5 Case Study / 可视化分析

- **Figure 4**：不同投票策略和 MIL 方法的精度随页面数量变化曲线
- **Figure 5**：不同训练页面数量下最佳投票策略的精度
- **Figure 6**：MIL 方法在不同训练包和训练页面数量下的精度
- **Figure 7**：开放世界 F1-score 分布

### 8.6 局限性与失败案例

- **噪声页面敏感性**：4 个噪声页面导致 MIL 精度下降 30%，投票策略下降 20%
- **多标签页未处理**：仅考虑单标签页场景
- **实时分割挑战**：未解决实际 Tor 网络中的页面序列分割问题
- **HMM 未超越投票**：考虑页面顺序的 HMM 方法未超越不考虑顺序的投票策略

---

## 9. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 现有网页分类器直接用于网站指纹精度下降 20-30% | Table 1：单页面训练精度从 92.91% 降至 44.10% | §6.1 |
| 2-3 次点击可提升精度 20%+ | Figure 4：概率投票在 2-3 页面时精度从 70% 升至 90% | §6.2.1 |
| MIL 在小数据集下优于传统方法 | Figure 6b：30 训练页面 + 2 训练包时 MIL 达 70%，DF 仅 4.3% | §6.2.2 |
| 开放世界中 60% 网站可达到 F1=1.0 | Figure 7d：3 clicks 时约 60% 网站 F1=1.0 | §6.2.3 |
| WTF-PAD 和 FRONT 在多页面场景下失效 | Table 3：4+ 页面时精度达 100% | §6.3 |
| Tamaraw 保护效果降低约 5 倍 | Table 3：从 4.61% 升至 ~20% | §6.3 |
| 页面顺序非关键因素 | Figure 8：HMM 未超越最佳投票策略 | §6.2.4 |
| 噪声页面对 MIL 影响较大 | Table 4：4 噪声页面时 MIL 精度下降 30% | §6.4 |

---

## 10. 原始资料链接

- PDF: https://www.usenix.org/conference/usenixsecurity24/presentation/mitseva
- MinerU Markdown: 02-parsed-markdown/2024-USENIX-Stop__Don't_Click_Here_Anymore__Boosting_Website_Fingerprinting_By_Considering_Sets_of_Subpages.md
- 代码仓库: https://www.informatik.tu-cottbus.de/~andriy/zwiebelfreunde/methods-usenix-sec-2024/
- 补充材料: 论文附录 A-E 包含超参数选择、站点图生成、索引页面分析、训练策略、数据集验证

---

## 11. 方法创新点深度分析

### 11.1 核心创新：从网页到网站的范式转变

传统 WFP 攻击的假设是：检测到网站的索引页面就等于检测到网站。但本文指出这一假设在现实中不成立：
- 用户经常通过浏览器缓存 URL、邮件链接、搜索引擎直接访问非索引页面
- 网站包含大量页面，枚举所有页面不现实
- 但用户在同一网站内连续访问多个页面会泄露额外信息

### 11.2 MIL 架构的创新设计

本文的 MIL 架构有以下创新：
1. **特征生成器复用 DF 的 CNN 结构**，但用 Softmax 替代全连接层，支持中间评估
2. **自定义权重层**使用 tanh 分别处理入站/出站包，然后 softmax 归一化
3. **可变学习率**根据验证集性能动态调整，而非固定衰减
4. **包创建策略**确保每个 bag 包含不同页面的轨迹，避免同一页面轨迹重复

### 11.3 投票策略的设计哲学

六种投票策略的设计体现了从简单到复杂的渐进思路：
- **多数投票**：最简单，仅计数
- **概率投票**：考虑分类器输出的概率分布
- **均值投票**：平滑概率差异
- **加权均值**：引入置信度权重（方差/标准差/基尼系数）

其中基尼系数加权均值在噪声页面场景下表现最佳，可有效过滤噪声。

---

## 12. 防御影响分析

### 12.1 对现有防御的冲击

| 防御方法 | 单页面精度 | 9 页面精度 | 失效程度 |
|---|---|---|---|
| WTF-PAD | 90.72% | 100% | 完全失效 |
| FRONT | 67.00% | 100% | 完全失效 |
| RegulaTor | 17.17% | 64.87% | 大幅削弱 |
| TrafficSliver-Net | 19.92% | 46.55% | 中度削弱 |
| CS-Buflo | 10.89% | 56.00% | 大幅削弱 |
| Tamaraw | 4.61% | 18.93% | 中度削弱 |

### 12.2 防御失效原因分析

- **流量填充防御（WTF-PAD、FRONT）**：填充噪声在单页面场景有效，但多页面场景下攻击者可从多个页面的统计特征中提取模式
- **流量分割防御（TrafficSliver-Net）**：分割后的流量在多页面场景下仍可被聚合分析
- **强防御（Tamaraw、CS-Buflo）**：虽然仍有一定保护效果，但保护程度大幅降低

---

## 13. 未来研究方向

### 13.1 本文开启的研究问题

1. **多标签页场景**：如何将本文方法与多标签页 WFP 攻击结合？
2. **实时攻击**：如何在实际 Tor 网络中实时分割和识别用户浏览的页面序列？
3. **防御设计**：如何设计针对多页面场景的新型防御？
4. **用户行为建模**：如何更准确地建模用户的网站内浏览行为？

### 13.2 对防御研究的启示

- 现有防御的评估需要考虑多页面场景
- 需要设计能够抵抗多页面聚合分析的新型防御
- 防御评估应包含不同用户浏览行为模式

### 13.3 对攻击研究的启示

- 网站级指纹比网页级指纹更具现实威胁
- 多页面信息聚合是提升 WFP 攻击的有效途径
- MIL 等机器学习方法在小数据集场景下具有优势

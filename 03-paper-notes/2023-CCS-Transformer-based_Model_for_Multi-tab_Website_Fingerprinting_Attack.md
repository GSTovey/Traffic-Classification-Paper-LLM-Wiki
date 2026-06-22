---
type: paper
title_original: "Transformer-based Model for Multi-tab Website Fingerprinting Attack"
title_cn: "基于 Transformer 的多标签页网站指纹攻击模型"
authors:
  - Zhaoxin Jin
  - Tianbo Lu
  - Shuang Luo
  - Jiaze Shang
year: 2023
venue: "ACM CCS 2023"
doi: "https://doi.org/10.1145/3576915.3623107"
url: "https://github.com/jzx-bupt/TMWF"
pdf: ""
mineru_md: "02-parsed-markdown/2023-CCS-Transformer-based_Model_for_Multi-tab_Website_Fingerprinting_Attack.md"
status: processed
reading_level: L3
research_area:
  - website-fingerprinting
  - encrypted-traffic-analysis
  - anonymity-network
  - deep-learning
task:
  - multi-tab-website-fingerprinting
  - traffic-classification
  - set-prediction
method:
  - transformer
  - attention-mechanism
  - set-prediction
  - dfnet-backbone
  - tab-queries
dataset:
  - Walkie-Talkie
  - BAPM-real-dataset
  - Chrome-open-world-dataset
  - Tor-Browser-dataset
code: "https://github.com/jzx-bupt/TMWF"
relevance: high
created: "2026-06-21"
updated: "2026-06-21"
---

# Transformer-based Model for Multi-tab Website Fingerprinting Attack

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Transformer-based Model for Multi-tab Website Fingerprinting Attack |
| 中文标题 | 基于 Transformer 的多标签页网站指纹攻击模型 |
| 作者 | Zhaoxin Jin, Tianbo Lu (通讯), Shuang Luo, Jiaze Shang |
| 年份 | 2023 |
| 会议/期刊 | ACM CCS 2023 |
| 研究方向 | [[website-fingerprinting]]、[[encrypted-traffic-analysis]]、匿名网络隐私攻击 |
| 任务类型 | [[website-fingerprinting]]、多标签页流量分类、集合预测 |
| 方法关键词 | [[transformer]]、自注意力机制、DFNet 特征提取、tab queries、集合预测、DETR 启发 |
| 数据集 | Walkie-Talkie、BAPM 真实数据集、Chrome 开放世界数据集（50 监控网站 + 6900+ 非监控）、Tor Browser 数据集 |
| 是否开源 | 是（代码 + 数据集） |
| PDF | https://doi.org/10.1145/3576915.3623107 |
| MinerU Markdown | `02-parsed-markdown/2023-CCS-Transformer-based_Model_for_Multi-tab_Website_Fingerprinting_Attack.md` |

---

## 1. 一句话总结

> TMWF 将多标签页网站指纹识别建模为有序集合预测问题，借鉴 DETR 架构使用 Transformer + 可学习 tab queries 从混合多标签页流量中自适应提取各页面指纹特征，消除了对"标签页数量"先验知识的依赖，在 2-6 标签页场景下显著优于 BAPM 等基线方法。

---

## 2. 摘要翻译

### 2.1 摘要原文

While the anonymous communication system Tor can protect user privacy, website fingerprinting (WF) attackers can still identify the websites that users access over encrypted network connections by analyzing the metadata generated during network communication. Despite the emergence of new WF attack techniques in recent years, most research in this area has focused on pure traffic traces generated from single-tab browsing behavior. However, multi-tab browsing behavior significantly degrades the performance of WF classification models based on the single-tab assumption. As a result, some research has shifted its focus to multi-tab WF attacks, although most of these works have limited utilization of the mixed information contained in multi-tab traces. In this paper, we propose an end-to-end multi-tab WF attack model, called Transformer-based model for Multi-tab Website Fingerprinting attack (TMWF). Inspired by object detection algorithms in computer vision, we treat multi-tab WF recognition as a problem of predicting ordered sets with a maximum length. By adding enough single-tab queries to the detection model and letting each query extract WF features from different positions in the multi-tab traces, our model's Transformer architecture capitalizes more fully on trace features. Paired with our new proposed model training approach, we accomplish adaptive recognition of multi-tab traces with varying numbers of web pages. This approach successfully eliminates a strong and unrealistic assumption in the field of multi-tab WF attacks -- that the number of tabs contained in a sample belongs to the attacker's prior knowledge. Experimental results in various scenarios demonstrate that the performance of TMWF is significantly better than existing multi-tab WF attack models. To evaluate model performance in more authentic scenarios, we present a dataset of multi-tab trace data collected from real open-world environments.

### 2.2 摘要中文翻译

匿名通信系统 Tor 虽然可以保护用户隐私，但网站指纹（WF）攻击者仍可通过分析网络通信中产生的元数据来识别用户通过加密网络连接访问的网站。尽管近年来出现了新的 WF 攻击技术，但该领域大多数研究集中于单标签页浏览行为产生的纯流量轨迹。然而，多标签页浏览行为会显著降低基于单标签页假设的 WF 分类模型性能。因此，部分研究已将焦点转向多标签页 WF 攻击，但这些工作对多标签页轨迹中混合信息的利用仍然有限。本文提出一种端到端的多标签页 WF 攻击模型 TMWF。受计算机视觉中目标检测算法的启发，我们将多标签页 WF 识别建模为最大长度有序集合预测问题。通过在检测模型中添加足够的单标签页查询，并让每个查询从多标签页轨迹的不同位置提取 WF 特征，模型的 Transformer 架构更充分地利用了轨迹特征。结合我们提出的新训练方法，实现了对不同页面数量多标签页轨迹的自适应识别。该方法成功消除了多标签页 WF 攻击领域中一个强而不现实的假设——样本中包含的标签页数量属于攻击者的先验知识。多种场景下的实验结果表明，TMWF 的性能显著优于现有模型。为在更真实场景中评估模型性能，我们提供了一个从真实开放世界环境中收集的多标签页轨迹数据集。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

作者的核心出发点是：**多标签页浏览行为严重破坏了现有 WF 模型的性能**，而现有方法未能充分利用多标签页轨迹中的信息。

具体来说：
- Tor 浏览器加载速度慢，用户习惯并行打开多个标签页 [33, 5]
- 多标签页行为导致不同网页的流量轨迹重叠，产生"混淆效应"
- 现有多标签页方法大多依赖"输入样本中的标签页数量"作为先验知识，这在现实中攻击者无法获得
- 现有方法对重叠区间的利用有限，大多将其视为噪声而非有价值的特征信息

### 3.2 现有方法的痛点和不足

| 痛点 | 具体表现 | 受影响的方法 | 本文解决方案 |
|---|---|---|---|
| 依赖标签页数量先验知识 | 模型训练和测试时需知道样本包含几个标签页 | BAPM [42]、[36]、[40] | 新训练方法：输出固定 N 个预测，用 "no-tab" 填充不足部分 |
| 对重叠区间利用不足 | 重叠轨迹被视为噪声丢弃或仅做简单分割 | [26]、[36]、[40] | Transformer 全局建模，从重叠区间中提取有用特征 |
| CNN 全局建模能力有限 | CNN 擅长局部特征但难以捕获长距离依赖，无法区分混合轨迹中不同页面的特征 | BAPM [42]、DF [14] | Transformer 自注意力机制实现全局特征建模 |
| 仅能识别有限标签页配置 | 模型固定处理 2-tab 或 3-tab，无法泛化到不同数量 | [36]、[40] | 自适应识别 0-N 个标签页 |
| 开放世界评估不足 | 非监控网站数量少，未充分模拟真实场景 | [36]、[42] | 收集真实开放世界数据集（50 监控 + 6900+ 非监控） |

### 3.3 论文的研究假设或核心直觉

**核心直觉**：多标签页 WF 识别本质上是一个**集合预测问题**——从混合轨迹中预测包含哪些网站。这与计算机视觉中的目标检测问题高度类似：一张图片中包含多个物体（类比多个网页），需要识别每个物体的类别和位置。

**关键假设**：
1. Transformer 的自注意力机制能够从混合的多标签页轨迹中，通过全局建模区分不同页面的特征（即使存在重叠）
2. 通过输出固定数量的预测结果并用 "no-tab" 类填充，可以消除对标签页数量先验知识的依赖
3. DFNet（CNN 骨干网络）提取的局部特征经过 Transformer 全局建模后，能够产生足够区分不同页面的嵌入表示

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | Juarez et al. [10] 指出多标签页浏览行为显著降低单标签页 WF 模型性能 | §1 |
| 痛点提炼 | 现有多标签页方法（BAPM、[36]、[40]）都依赖标签页数量先验知识，且对重叠区间利用有限 | §3.1 |
| 问题转化 | 能否将多标签页 WF 识别建模为集合预测问题，借鉴目标检测领域的思路？ | §3.2（DETR 启发） |
| 文献定位 | 多标签页 WF 是被部分解决的问题（BAPM 是首个端到端模型），但先验知识依赖和重叠利用是未解决的关键限制 | §3.1 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | Transformer 全局建模能力 + tab queries 能从混合多标签页轨迹中区分不同页面特征 | DETR 在目标检测中的成功 + Transformer 的自注意力特性 | 消融实验（No Transformer 对比） |
| 辅助假设 1 | 固定 N 个输出 + no-tab 填充可消除标签页数量先验依赖 | 类比 DETR 使用 100 个 object queries 检测不定数量目标 | 2-tab/4-tab/6-tab 测试集泛化实验 |
| 辅助假设 2 | DFNet 比 BAPM 的 CNN 特征提取器更适合多标签页场景 | DF 在单标签页 WF 中表现优异 | 消融实验（No DF 对比） |
| 辅助假设 3 | 时间信息能提升模型性能 | 时间特征在部分 WF 工作中有帮助 | 消融实验（Add Timeinfo 对比） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | No Transformer 时 Overall Basic Acc 从 75.5% 降至 38.1%，Overall Advanced Acc 从 68.2% 降至 8.0% | §6.2, Table 3 |
| 辅助假设 1 | 支撑 | TMWF 在 2-tab 和 4-tab 测试集上（训练用 6-tab）仍保持良好性能 | §6.1, Table 2 |
| 辅助假设 2 | 支撑 | No DF 时 Overall Basic Acc 从 75.5% 降至 69.0% | §6.2, Table 3 |
| 辅助假设 3 | 反驳 | Add Timeinfo 时 Overall Basic Acc 从 75.5% 降至 73.8%，且大幅减慢训练 | §6.2, Table 3 |

---

## 4. 方法设计

### 4.1 方法整体流程

TMWF 采用三阶段架构：

1. **骨干网络（DFNet）**：对原始多标签页方向序列进行局部建模，提取高级特征表示
2. **Transformer 编码器-解码器**：编码器对特征序列进行全局建模；解码器使用 N 个 tab queries 从全局特征中提取各页面的指纹嵌入
3. **分类头**：对 N 个页面嵌入进行分类，输出网站类别预测

整体流程：原始流量序列 → DFNet 特征提取 → 位置编码 + Transformer 编码器 → tab queries + Transformer 解码器 → 线性层 + Softmax → N 个类别预测

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | 原始多标签页方向序列 wf ∈ R^L | DFNet 四层 CNN（kernel [32,64,128,256]，size [8,8,8,8]，pool [8,8,8,8]） | 特征序列 F ∈ R^{l×d}（l=121, d=256） | 局部建模，提取空间特征 |
| Step 2 | 特征序列 F | LayerNorm(FW+b) + 可学习位置编码 P | F' ∈ R^{l×d} | 归一化 + 位置信息注入 |
| Step 3 | F' | 2 层 Transformer 编码器（8 头，FFN 1024） | 上下文特征序列 Z | 全局建模，捕获长距离依赖 |
| Step 4 | Z + N 个 tab queries T_Q | 2 层 Transformer 解码器，每个 tab query 关注不同位置 | N 个页面指纹嵌入 E_WF | 从全局特征中分离各页面特征 |
| Step 5 | E_WF | 线性层 + Softmax（类别数 C） | N 个类别概率分布 Pr ∈ R^{N×C} | 分类预测 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| DFNet 骨干网络 | 提取局部特征 | 原始方向序列 wf ∈ R^L (L=30720) | 特征序列 F ∈ R^{121×256} | 为 Transformer 提供输入特征 |
| 位置编码 | 注入序列位置信息 | 特征维度 d=256 | 位置编码 P ∈ R^{l×d} | 与特征序列求和后输入编码器 |
| Transformer 编码器（2层） | 全局上下文建模 | F' ∈ R^{l×d} | 上下文序列 Z ∈ R^{l×d} | 为解码器提供全局特征 |
| Tab Queries（N=6） | 可学习的位置编码，查询各页面特征 | 可学习参数 T_Q ∈ R^{N×d} | 查询向量 | 输入解码器，每个查询对应一个潜在页面 |
| Transformer 解码器（2层） | 从全局特征中提取各页面嵌入 | Z（来自编码器）+ T_Q | 页面嵌入 E_WF ∈ R^{N×d} | 产生 N 个页面的特征表示 |
| 分类头 | 将页面嵌入映射到网站类别 | E_WF | 概率分布 Pr ∈ R^{N×C} | 输出最终预测 |

### 4.4 公式、算法和机制解释

**骨干网络特征提取**：

$$F = DFNet(\mathbf{wf}), \quad \mathbf{wf} \in R^L, \quad F \in R^{l \times d}$$

其中 L=30720 为输入序列长度，l=121 为经过四层 CNN（kernel/pool 均为 8）后的特征长度，d=256 为特征维度。

**Transformer 编码器**：

$$F' = \text{LayerNorm}(FW + \mathbf{b}) + P$$
$$O_i = \text{TransformerEncoder}(O_{i-1}), \quad O_0 = F', \quad Z = O_{N_E}$$

编码器通过自注意力机制建模特征序列中任意位置间的全局交互关系。

**Tab Queries 与解码器**：

$$O_i = \text{TransformerDecoder}(O_{i-1}, T_Q), \quad O_0 = Z, \quad E_{WF} = O_{N_D}$$

N=6 个 tab queries 作为可学习的位置编码，每个 query 关注混合轨迹中不同页面对应的特征区域。解码器通过交叉注意力在 tab queries 和编码器输出的全局特征之间建立对齐。

**分类**：

$$Pr = \text{Softmax}(E_{WF}W_5 + \mathbf{b}_5), \quad Pr \in R^{N \times C}$$

N=6 个预测结果中，非监控网站类和冗余预测统一标记为 "no-tab"，仅保留监控网站类预测作为最终结果。

**新训练方法的核心思想**：对于实际标签数不足 N 的样本，用 "no-tab" 标签填充至 N 个。训练时模型学习产生 N 个预测，测试时过滤掉 "no-tab" 预测即可得到实际结果。这消除了对标签页数量先验知识的依赖。

**新评估指标**：

- **Overall Basic**：将 ground truth 和预测转为集合（忽略顺序），不计算 "no-tab" 正确预测
- **Overall Advanced**：将 ground truth 和预测视为有序列表（保留顺序），不计算 "no-tab" 正确预测

Basic 指标衡量"能否识别访问了哪些网站"，Advanced 指标额外衡量"能否识别访问顺序"。

### 4.5 方法优势

1. **端到端学习**：无需手工特征设计，直接从原始方向序列到网站类别预测
2. **自适应标签页数量**：通过固定 N 个输出 + no-tab 填充，消除对标签页数量先验知识的依赖
3. **充分利用重叠区间**：Transformer 全局建模能力使模型从重叠区间中提取有用信息，而非视其为噪声
4. **并行预测**：N 个页面嵌入并行提取，无需顺序处理

### 4.6 方法不足

1. **仍依赖最大标签页数 N 的设定**：虽然消除了对实际标签页数的依赖，但需设定上限 N（文中设为 6）
2. **完全重叠轨迹识别困难**：当用户同时打开多个标签页导致流量完全混合时，模型性能会大幅下降（§7）
3. **对 WF 防御技术敏感**：防御技术进一步破坏纯段完整性，对多标签页模型的影响比单标签页模型更严重
4. **时间信息未带来提升**：添加时间序列输入反而降低性能并减慢训练
5. **硬件限制**：受硬件条件限制，N 最大只能设为 6，无法探索更大标签页数场景

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 维度 | 现有方法 | TMWF |
|---|---|---|
| 处理范式 | 分割 → 单标签页分类，或固定标签页数端到端 | 端到端 + 集合预测（自适应标签页数） |
| 全局建模 | BAPM 使用块划分 + 自注意力（局部注意力） | Transformer 编码器-解码器（全局注意力） |
| 标签页数量依赖 | 训练和测试时需已知标签页数 | 仅需设定上限 N，实际标签页数未知 |
| 重叠区间利用 | 丢弃或有限利用 | 通过 Transformer 全局建模充分提取信息 |
| 特征提取 | BAPM 使用简单 CNN | DFNet（DF 的主干网络，在单标签页 WF 中表现优异） |

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 多标签页 WF 的集合预测建模 | 将多标签页 WF 识别类比为目标检测中的集合预测问题 | 高 | 是（可应用于其他混合信号分离任务） |
| 新训练方法 | N 个输出 + no-tab 填充，消除标签页数量先验依赖 | 高 | 是（适用于任何固定输出数的分类模型） |
| Tab Queries 机制 | 可学习位置编码查询各页面特征 | 中 | 是（DETR 的 object queries 思路通用） |
| 新评估指标 | Overall Basic/Advanced，不计算 "no-tab" 正确预测 | 中 | 是（适用于任何多标签分类评估） |
| 真实开放世界数据集 | 50 监控 + 6900+ 非监控网站，Chrome + Tor Browser | 中 | 否（数据集特定） |

### 5.3 适用场景

- **最适用**：攻击者不知道用户打开了几个标签页，需要自适应识别监控网站
- **较适用**：标签页数量变化较大的场景（2-6 个标签页）
- **不太适用**：完全并行加载导致流量完全混合的场景
- **不太适用**：部署了 WF 防御技术的场景

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| BAPM [42] | 首个端到端多标签页 WF；利用重叠区间 | 依赖标签页数量先验知识；块划分 + 自注意力全局建模能力有限 | Transformer 全局建模 + 新训练方法消除先验依赖 |
| Adaptive-BAPM（本文改进版） | 消除了标签页数量先验依赖 | 原有架构（块划分 + 自注意力）在自适应场景下性能大幅下降 | TMWF 的 Transformer 架构提供更强的全局建模能力 |
| [36] CNN+LSTM/SDAE | 利用纯段的首尾部分进行分类 | 仅处理 2-tab；依赖足够长的非重叠纯段 | 端到端处理，不限标签页数，利用重叠区间 |
| [40] BalanceCascade-XGBoost | 自动识别首尾页边界 | 仅能识别第一个页面 | 识别所有页面 |
| [26] 时间分割 + kNN | 尝试分割多标签页轨迹 | 仅处理 2-tab；依赖时间间隔 | 不依赖分割，端到端处理 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

实验分为四部分：
1. **模型设计与验证**：在 Walkie-Talkie 合成数据集上训练（6-tab），在 2/4/6-tab 测试集上评估泛化能力
2. **消融实验**：验证 Transformer、DFNet、时间信息的贡献
3. **闭世界实验**：在 BAPM 发布的真实 2-tab 数据集上对比
4. **开放世界实验**：在自收集的真实多标签页数据集上评估（Chrome + Tor Browser）

### 6.2 数据集

| 数据集 | 类型 | 标签页数 | 监控/非监控 | 训练/测试样本数 | 来源 |
|---|---|---|---|---|---|
| Walkie-Talkie (D_WT) | 合成 | 2/4/6 | 50/0（闭世界） | ~22,000/~5,500 | Walkie-Talkie 单标签页数据合成 |
| BAPM 真实数据集 (D_BAPM) | 真实 | 2 | 50/0（闭世界） | 10,000/1,000 | BAPM [42] 发布 |
| Chrome 开放世界 (D_CHR) | 真实 | 2/3/4/5 | 50/6,900+（开放世界） | 合成训练 ~40,000；真实测试各 1,000 | 自收集（Chrome + Selenium + Tor） |
| Tor Browser (D_TBB) | 真实 | 2/3/4/5 | 50/6,900+（开放世界） | 同上 | 自收集（Tor Browser Selenium） |

**数据集收集细节**：
- 使用 Docker + Selenium + Chrome/Tor 自动化访问
- 最大加载时间 30 秒，访问间隔 2 秒
- 监控网站：从 Tranco Top 100 中选取 50 个可访问网站，每个访问 200 次
- 非监控网站：Top 100 后 9900 个站点中筛选出 6,900+ 可访问站点
- 多标签页合成方法：M_ratio（按重叠比例）和 M_delay（按时间延迟，更接近真实访问模式）

### 6.3 Baseline

| 方法 | 类型 | 说明 |
|---|---|---|
| BAPM [42] | 原始端到端多标签页 WF | 固定标签页数，块划分 + 自注意力 |
| Adaptive-BAPM | 本文改进版 BAPM | 将注意力头数改为 6，适配新训练方法 |

### 6.4 评价指标

**传统指标（Previous）**：按页面分别计算 Acc/Pre/Rec，需已知标签页数

**新指标**：
- **Overall Basic**：集合化评估，忽略顺序，不计算 "no-tab" 正确预测
  - Accuracy_Basic = |T∩P - {no-tab}| / max(|T-{no-tab}|, |P-{no-tab}|)
  - Precision_Basic = (1/m) Σ TP_j/(TP_j+FP_j)
  - Recall_Basic = (1/m) Σ TP_j/(TP_j+FN_j)
- **Overall Advanced**：有序列表评估，保留顺序，不计算 "no-tab" 正确预测

### 6.5 关键实验结果

**闭世界泛化实验（Walkie-Talkie，6-tab 训练）**：

| 模型 | 指标 | 2-tab 测试 | 4-tab 测试 | 6-tab 测试 |
|---|---|---|---|---|
| Adaptive-BAPM | Overall Basic Acc | 21.6% | 21.9% | 16.7% |
| Adaptive-BAPM | Overall Basic Pre | 52.3% | 52.1% | 57.6% |
| Adaptive-BAPM | Overall Basic Rec | 37.6% | 23.4% | 17.2% |
| **TMWF** | **Overall Basic Acc** | **64.2%** | **74.9%** | **75.5%** |
| **TMWF** | **Overall Basic Pre** | **80.9%** | **84.0%** | **88.9%** |
| **TMWF** | **Overall Basic Rec** | **77.4%** | **83.9%** | **78.4%** |
| Adaptive-BAPM | Overall Advanced Acc | 15.9% | 16.0% | 13.1% |
| **TMWF** | **Overall Advanced Acc** | **35.0%** | **29.6%** | **68.2%** |

**闭世界实验（BAPM 真实 2-tab 数据集）**：

| 模型 | 1st Page Acc | 1st Page Pre | 1st Page Rec | 2nd Page Acc | 2nd Page Pre | 2nd Page Rec |
|---|---|---|---|---|---|---|
| BAPM [42] | 93.2 | 93.5 | 92.9 | 82.9 | 84.9 | 83.2 |
| Adaptive-BAPM | 95.9 | 94.3 | 93.9 | 93.1 | 91.8 | 91.2 |
| **TMWF** | **97.7** | **95.9** | **95.7** | **97.4** | **95.5** | **95.5** |

**消融实验（6-tab 测试集）**：

| 模型变体 | Overall Basic Acc | Overall Basic Pre | Overall Basic Rec | Overall Advanced Acc | Overall Advanced Pre | Overall Advanced Rec |
|---|---|---|---|---|---|---|
| Add Timeinfo | 73.8 | 89.4 | 76.6 | 68.7 | 84.4 | 74.3 |
| **Original Model** | **75.5** | **88.9** | **78.4** | **68.2** | **81.6** | **74.7** |
| No DF | 69.0 | 82.1 | 75.1 | 60.8 | 77.1 | 67.9 |
| No Transformer | 38.1 | 45.8 | 65.8 | 8.0 | 11.2 | 14.7 |

**开放世界实验（Chrome 真实多标签页测试集）**：
- TMWF 在所有标签页数（2-5）上的 Overall Basic 指标均优于 Adaptive-BAPM
- 合成验证集与真实测试集之间存在性能差距，但 M_delay 合成验证集的结果更接近真实测试集

### 6.6 优势最明显的场景

1. **标签页数量未知的场景**：TMWF 的自适应能力是其最大优势
2. **闭世界 2-tab 识别**：在 BAPM 真实数据集上，TMWF 两个页面的 Acc 均超过 97%
3. **重叠率较高的场景**：TMWF 对重叠轨迹的鲁棒性显著优于 BAPM（中间页面性能不显著下降）

### 6.7 局限性

1. **完全重叠轨迹**：当多个页面并行加载导致流量完全混合时，纯段不存在，模型性能大幅下降
2. **WF 防御技术**：未评估对抗 WF 防御的效果，但作者指出多标签页模型比单标签页模型更脆弱
3. **真实场景差距**：真实开放世界评估中，准确率仍受基础率影响（大量非监控网站导致假阳性）
4. **Tor 浏览器隔离策略**：Tor 浏览器按域名隔离电路，增加了多标签页 WF 的难度
5. **标签页数量上限**：N=6 是硬件限制，实际场景可能需要更大值

---

## 7. 学习与应用

### 7.1 是否开源？

是。代码和数据集在 https://github.com/jzx-bupt/TMWF 提供。

### 7.2 复现关键步骤

1. 准备 Walkie-Talkie 单标签页数据集，使用 M_ratio 方法合成 6-tab 训练集（~22,000 样本）
2. 构建 TMWF 模型：DFNet 骨干（4 层 CNN） + 2 层 Transformer 编码器 + 2 层 Transformer 解码器 + 6 个 tab queries
3. 训练时对标签不足 6 的样本用 "no-tab" 填充，使用分类交叉熵损失
4. 测试时输出 6 个预测，过滤掉 "no-tab" 类得到最终结果

### 7.3 关键超参数、预处理和训练细节

| 参数 | 值 | 说明 |
|---|---|---|
| 输入序列长度 L | 30720 | 原始方向序列长度 |
| DFNet 核心数 | [32, 64, 128, 256] | 四层 CNN |
| DFNet 核大小/池大小 | [8, 8, 8, 8] | 每层相同 |
| 特征维度 d | 256 | DFNet 输出特征维度 |
| Transformer 编码器层数 N_E | 2 | |
| Transformer 解码器层数 N_D | 2 | |
| 注意力头数 | 8 | |
| FFN 维度 | 1024 | |
| Tab Queries 数量 N | 6 | 设定的标签页数上限 |
| Dropout | 0.1 | |
| 单页长度 | 5120 | Adaptive-BAPM 使用 |
| 块长度 | 160 | Adaptive-BAPM 使用 |
| 重叠比例范围 | [0.1, 0.2, 0.3, 0.4, 0.5] | M_ratio 合成时随机选取 |
| 纯段阈值 | 0.1 | 中间页面的最小纯段比例 |

### 7.4 能否迁移到其他任务？

**高度可迁移**：
- **混合信号分离任务**：集合预测 + 固定输出数 + no-tab 填充的思路可应用于任何需要从混合信号中分离多个目标的任务
- **加密流量分析中的多流场景**：同一连接中包含多个应用流量时的识别
- **网络入侵检测中的多攻击识别**：一次会话中包含多种攻击行为的检测

**部分可迁移**：
- DFNet 作为流量特征提取骨干网络可在其他 WF 相关任务中使用
- Tab Queries 的思路可泛化为"任务特定查询向量"

### 7.5 对我的研究有什么启发？

1. **集合预测思路**：将分类问题重新建模为集合预测问题，是一种处理"输出数量不确定"的有效范式
2. **跨领域借鉴**：从计算机视觉的目标检测（DETR）借鉴思路到网络安全领域，是有效的创新路径
3. **训练方法创新**：通过改变训练标签的构造方式（no-tab 填充），在不改变模型架构的情况下扩展模型能力
4. **评估指标设计**：针对攻击者实际意图设计评估指标（不计算非监控网站正确预测），比通用指标更能反映真实性能
5. **合成与真实的差距**：合成数据训练 + 真实数据评估是 WF 领域的标准做法，但两者之间存在显著性能差距

---

## 8. 总结

### 8.1 核心思想

> Transformer 集合预测 + no-tab 填充实现自适应多标签页网站指纹识别。

### 8.2 速记版 Pipeline

1. 原始多标签页方向序列 → DFNet 四层 CNN 提取局部特征（L=30720 → l=121, d=256）
2. 特征序列 + 可学习位置编码 → 2 层 Transformer 编码器全局建模
3. 6 个 tab queries + Transformer 解码器 → 从全局特征中提取 6 个页面指纹嵌入
4. 线性层 + Softmax → 6 个类别概率分布
5. 过滤 "no-tab" 预测 → 最终识别的监控网站列表

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]]
- [[encrypted-traffic-analysis]]
- [[transformer]]

### 9.2 相关方法

- [[transformer]]（自注意力机制、编码器-解码器架构）
- DFNet / Deep Fingerprinting [14]（CNN 骨干网络）
- DETR [12]（目标检测中的集合预测启发来源）
- BAPM [42]（块注意力分析模型，多标签页 WF 基线）
- Walkie-Talkie [27]（WF 防御方法，本文使用其数据集）

### 9.3 相关任务

- [[website-fingerprinting]]（网站指纹攻击）
- 多标签页网站指纹攻击（multi-tab WF）
- 流量重叠分离（overlapping trace separation）

### 9.4 可更新的综述页面

- [[survey-website-fingerprinting]]（如有 WF 综述页面，可补充多标签页 WF 攻击的最新进展）
- [[encrypted-traffic-analysis]]（可补充 Transformer 在流量分析中的应用）

### 9.5 可加入的对比表

- 多标签页 WF 攻击方法对比表（TMWF vs BAPM vs [36] vs [40]）
- WF 模型架构对比表（CNN vs CNN+Transformer vs 纯 Transformer）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 多标签页浏览行为显著降低单标签页 WF 模型性能 | Juarez et al. [10] 的研究结论 | §1 |
| 现有多标签页 WF 方法依赖标签页数量先验知识 | BAPM [42]、[36]、[40] 均假设已知标签页数 | §3.1 |
| Transformer 是性能提升的最关键组件 | 消融实验：移除 Transformer 后 Overall Basic Acc 从 75.5% 降至 38.1% | §6.2, Table 3 |
| DFNet 比 BAPM 的 CNN 更适合多标签页场景 | 消融实验：替换 DFNet 后 Overall Basic Acc 从 75.5% 降至 69.0% | §6.2, Table 3 |
| 时间信息未能提升模型性能 | 消融实验：添加时间信息后 Overall Basic Acc 从 75.5% 降至 73.8% | §6.2, Table 3 |
| TMWF 对重叠轨迹更鲁棒 | 闭世界实验中 TMWF 第二页性能不显著下降，而 BAPM 下降明显 | §6.3, Table 4 |
| TMWF 在自适应场景下大幅优于 Adaptive-BAPM | 6-tab 训练后在 2/4/6-tab 测试集上 Overall Basic Acc: TMWF 64.2%/74.9%/75.5% vs Adaptive-BAPM 21.6%/21.9%/16.7% | §6.1, Table 2 |
| M_delay 合成验证集的结果更接近真实测试集 | 开放世界实验中模型在 M_delay 验证集和真实测试集上的性能水平相似 | §6.4 |
| 完全重叠轨迹识别仍是未解决问题 | 作者在 Discussion 中明确指出 | §7 |
| 低基础率场景下攻击者面临大量假阳性 | 作者在 §2 威胁模型和 §6.4 中讨论 | §2, §6.4 |

---

## 11. 原始资料链接

- PDF：https://doi.org/10.1145/3576915.3623107
- MinerU Markdown：`02-parsed-markdown/2023-CCS-Transformer-based_Model_for_Multi-tab_Website_Fingerprinting_Attack.md`
- 代码仓库：https://github.com/jzx-bupt/TMWF
- 补充材料：论文完整版含 Appendix A-I，见 GitHub

---

## 12. 后续问题

- TMWF 在更大标签页数（>6）场景下的性能如何？N 的最优值如何确定？
- 如果结合 WF 防御技术（如 TrafficSliver、Walkie-Talkie）进行对抗评估，TMWF 的攻击成功率如何？
- 能否将 TMWF 的集合预测思路应用于其他加密流量分析任务（如恶意流量检测、应用识别）？
- 完全重叠轨迹（用户同时打开多个标签页）场景下是否有可行的解决方案？
- TMWF 的 Transformer 架构能否进一步与预训练模型（如 ET-BERT）结合？

---

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

从 Tor 用户的多标签页浏览习惯与 WF 研究的单标签页假设之间的**根本矛盾**出发，指出多标签页行为严重破坏现有模型性能且现有多标签页方法依赖不现实的先验知识。**转折点**是将多标签页 WF 识别类比为目标检测中的集合预测问题，借鉴 DETR 架构设计 TMWF，通过 Transformer 全局建模 + tab queries + no-tab 填充训练方法，**消除标签页数量先验依赖**并充分利用重叠区间信息。最终在多种场景下验证了方法的有效性，并提供了真实开放世界数据集。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 提出问题 + 方法 + 结果概览 | 快速传达核心贡献 | "eliminates a strong and unrealistic assumption" |
| Introduction | 建立矛盾：Tor 隐私 vs WF 攻击；单标签页假设 vs 真实多标签页行为 | 问题背景和动机 | 多标签页行为"significantly degrades"现有模型 |
| Threat Model | 定义攻击者能力边界 | 设定实验评估框架 | 开放世界评估的必要性 |
| Related Work | 回顾单/多标签页 WF 进展 + DETR | 定位研究空白 | 所有多标签页方法都依赖标签页数量先验 |
| Method | 详细描述 TMWF 架构 | 技术核心 | 集合预测建模 + tab queries 机制 |
| Experiment | 四组实验全面验证 | 证据支撑 | 消融实验证明 Transformer 是关键组件 |
| Discussion | 坦诚讨论局限性 | 增加可信度 | 完全重叠轨迹和 WF 防御场景的挑战 |
| Conclusion | 总结贡献 | 收尾 | 强调"new ideas for multi-tab WF attacks" |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 场景缺失 | 现有研究假设单标签页浏览，不符合真实用户行为 | 矛盾证据（用户习惯数据 [5, 33] vs 研究假设） | §1 |
| 评估不足 | 现有多标签页方法依赖不现实的先验知识（标签页数量） | 性能瓶颈（依赖先验导致泛化性差） | §3.1 |
| 方法局限 | CNN 全局建模能力有限，无法有效利用重叠区间 | 理论缺陷（CNN 的局部感受野限制） | §4.2 |
| 评估不足 | 现有指标包含 "no-tab" 正确预测，虚高模型性能 | 评估不足（不反映攻击者真实意图） | §5.2 |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 模型验证（Walkie-Talkie） | 证明 TMWF 在合成数据上的优越性和泛化能力 | 核心论点的直接证据 |
| 消融实验 | 归因各组件贡献，证明 Transformer 是关键 | 支撑"Transformer 全局建模"的技术论点 |
| 闭世界实验（BAPM 数据集） | 在真实数据上验证不退化 | 消除"改进训练方法是否损害性能"的疑虑 |
| 开放世界实验（Chrome/Tor） | 在最真实场景下评估 | 验证方法在实际应用中的可行性 |
| 混淆矩阵分析 | 深入分析错误来源 | 指出主要错误是将监控网站误分类为 "no-tab" |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 从 Tor 隐私保护和 WF 攻击的大背景切入，快速聚焦到多标签页问题 | "大背景 → 具体技术问题 → 现有方法不足" 的漏斗式开篇 |
| Gap 提出方式 | 先指出"多标签页行为降低性能"的现象，再指出"所有方法依赖先验知识"的系统性问题 | "现象观察 → 方法审视 → 发现共性缺陷" |
| 方法论证逻辑 | 跨领域类比（目标检测 → WF），从 DETR 借鉴架构设计 | "类比论证：领域 A 的方法如何适用于领域 B" |
| 实验组织逻辑 | 合成数据验证 → 消融归因 → 真实数据验证 → 开放世界评估 | "逐步逼近真实场景"的渐进式验证 |
| 局限性讨论方式 | 坦诚讨论完全重叠轨迹和 WF 防御场景的挑战 | "诚实讨论 + 指出未来方向" |
| 最值得借鉴的一句话/一段结构 | "eliminates a strong and unrealistic assumption in the field" | 用"消除不现实假设"来突出贡献的叙事策略 |

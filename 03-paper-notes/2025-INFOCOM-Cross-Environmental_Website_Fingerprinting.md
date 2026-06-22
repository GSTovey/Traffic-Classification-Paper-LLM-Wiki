---
type: paper
title_original: "Cross-Environmental Website Fingerprinting"
title_cn: "跨环境网站指纹攻击"
authors: ["Jianfeng Li", "Dongliang Wang", "Yixuan Liu", "Yifei Gao", "Xiaorong Zhang", "Zheng Lin", "Xiaobo Ma", "Xiapu Luo", "Xiaohong Guan"]
year: 2025
venue: "IEEE INFOCOM 2025"
doi: unknown
url: unknown
pdf: ""
mineru_md: "02-parsed-markdown/2025-INFOCOM-Cross-Environmental_Website_Fingerprinting.md"
status: processed
reading_level: L2
research_area: ["website fingerprinting", "encrypted traffic analysis", "cross-domain transfer"]
task: ["website fingerprinting", "zero-shot recognition", "few-shot learning", "cross-environmental transfer"]
method: ["invariant feature generation", "Thompson sampling", "potential-aware resampling", "bilevel recognition", "inter-flow data augmentation"]
dataset: ["CE-450x6 (self-collected)"]
code: "https://github.com/cry4tal1/xeprint"
relevance: medium
created: "2026-06-21"
updated: "2026-06-21"
---

# Cross-Environmental Website Fingerprinting

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Cross-Environmental Website Fingerprinting |
| 中文标题 | 跨环境网站指纹攻击 |
| 作者 | Jianfeng Li, Dongliang Wang, Yixuan Liu, Yifei Gao, Xiaorong Zhang, Zheng Lin (西安交通大学); Xiaobo Ma (西安交通大学, 通讯); Xiapu Luo (香港理工大学); Xiaohong Guan (西安交通大学) |
| 年份 | 2025 |
| 会议/期刊 | IEEE INFOCOM 2025 |
| 研究方向 | [[website-fingerprinting]]、[[encrypted-traffic-analysis]]、跨域迁移学习 |
| 任务类型 | [[website-fingerprinting]]、零样本跨环境识别、少样本环境适应 |
| 方法关键词 | 不变特征生成（bilevel combinatorial optimization）、自适应 Thompson sampling、感知潜力的流量重采样（potential-aware resampling）、双层识别模型、流间数据增强 |
| 数据集 | CE-450x6（自建，450 网站 x 6 环境，50 样本/网站/环境） |
| 是否开源 | 是（代码 + 数据） |
| PDF | - |
| MinerU Markdown | `02-parsed-markdown/2025-INFOCOM-Cross-Environmental_Website_Fingerprinting.md` |

---

## 1. 一句话总结

> 首次提出跨环境网站指纹问题，X-EPRINT 通过自适应 Thompson sampling 生成跨环境不变特征实现零样本识别（F1=0.719，超最优基线 58.4%），再通过感知潜力的重采样 + 双层识别模型实现仅 3 个样本的少样本适应（F1=0.925），系统性解决了特征漂移、采样困境和少样本泛化三大挑战。

---

## 2. 摘要翻译

### 2.1 摘要原文

Despite the widespread adoption of encryption, such as TLS, encrypted proxies, and Tor, website fingerprinting (WF) has long been proven to be able to recognize websites from encrypted traffic. However, existing WF methods were generally developed and evaluated under the implicit assumption that traffic samples for training and recognition are captured in the same environment. When applied to diverse environments affected by practical factors, such as various browsers and proxy software, they will be hampered by three-fold challenges: i) feature drift, ii) sampling dilemma, and iii) few-shot generalization. None of existing WF methods can fully address them. In this paper, we take the first step to cross-environmental WF and advance a systematic framework, dubbed X-EPRINT, to tackle the above challenges. X-EPRINT generates cross-environmentally invariant features to address feature drift. It mitigates sampling dilemma via potential-aware traffic resampling. X-EPRINT capitalizes on inter-flow data augmentation to solve few-shot generalization. We conduct extensive experiments to evaluate X-EPRINT. The experimental results demonstrate that X-EPRINT achieves a robust performance in zero-shot cross-environmental recognition, with an F1-score of 0.719, which is 58.4% higher than the top-performing baseline method. It also attains an F1-score of 0.925 in 3-shot recognition, fulfilling few-shot environment adaptation.

### 2.2 摘要中文翻译

尽管 TLS、加密代理和 Tor 等加密技术已被广泛采用，网站指纹（WF）已被证明能够从加密流量中识别网站。然而，现有 WF 方法通常在"训练和识别的流量样本采集于同一环境"这一隐含假设下开发和评估。当应用于受浏览器和代理软件等实际因素影响的多样化环境时，它们将受到三重挑战的制约：(i) 特征漂移、(ii) 采样困境、(iii) 少样本泛化。现有 WF 方法无法完全解决这些问题。本文迈出了跨环境 WF 的第一步，提出了系统框架 X-EPRINT 来应对上述挑战。X-EPRINT 生成跨环境不变特征以应对特征漂移，通过感知潜力的流量重采样缓解采样困境，利用流间数据增强解决少样本泛化问题。实验结果表明，X-EPRINT 在零样本跨环境识别中实现了稳健性能，F1 分数为 0.719，比最优基线方法高出 58.4%。在 3-shot 识别中进一步达到 0.925 的 F1 分数。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

现有 WF 方法均假设训练和测试流量来自**同一环境**（同一浏览器 + 同一代理软件），但现实中加密代理用户使用多种浏览器（Chrome、Edge、Firefox）和代理软件（Shadowsocks、V2Ray），导致同一网站在不同环境下的流量模式发生显著变化。这是 WF 领域被忽视的实际部署问题。

### 3.2 现有方法的痛点和不足

| 痛点 | 具体表现 | 影响 |
|---|---|---|
| C1: 特征漂移 | 不同浏览器的 HTTP 头、渲染引擎、User-Agent 字符串不同；不同代理软件的加密协议、包填充方案不同 | 模型在源环境训练的特征在目标环境失效 |
| C2: 采样困境 | 加密代理生态中存在数百种浏览器和代理软件组合，逐一采集训练样本成本过高 | 环境特定模型训练不可扩展 |
| C3: 少样本泛化 | WF 方法通常数据饥渴，新环境部署时缺乏足够的标注样本 | 无法快速适应新环境 |

### 3.3 论文的研究假设或核心直觉

**核心直觉**：尽管不同环境下同一网站的流量表现形式不同（包密度、加载时间等），但存在一组**跨环境不变的特征**（如 burst 大小的统计分布结构），这些特征在不同环境下保持稳定且能区分不同网站。通过自动搜索这些不变特征，可以在不采集目标环境数据的情况下实现零样本识别。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 同一网站在不同浏览器/代理软件组合下的 DTW 距离显著大于同一环境内的距离 | Fig. 1, §II-A |
| 痛点提炼 | 跨环境 DTW 距离平均比单环境大 67%（跨代理）和 125%（跨浏览器），特征漂移严重 | Fig. 1 |
| 问题转化 | 将"跨环境 WF 不可用"的工程问题转化为"如何找到跨环境不变特征子集"的组合优化问题 | §III-C |
| 文献定位 | 现有 WF 方法（CAWF、TF 等）和概念漂移缓解方法（重训练/重标注）均无法解决此问题 | §VII |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 存在一组跨环境不变的特征子集，能在不同浏览器/代理环境下保持稳定并区分网站 | DTW 分析显示跨环境距离更大，但并非完全不可区分 | 实验：不变特征子集的 F1 远高于全特征集 |
| 辅助假设 1 | 利用置信度分数估计识别错误率，优先重采样高错误率网站可大幅提高效率 | 零样本识别的置信度与实际准确率相关 | 实验：感知潜力重采样 vs 随机重采样 |
| 辅助假设 2 | 流间数据增强（随机掩码 anchor 流特征）可缓解少样本过拟合 | anchor 流在识别阶段可能被误识别 | 消融实验 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | X-EPRINT 零样本 F1=0.719 vs ERF F1=0.454（+58.4%） | Table II, III |
| 辅助假设 1 | 支撑 | 感知潜力重采样 10% 网站 F1 提升 0.0741，是随机重采样的 3.97 倍 | Fig. 3 |
| 辅助假设 2 | 支撑 | 3-shot 场景 X-EPRINT F1=0.925 vs BRF F1=0.841（+10%） | Table IV |

---

## 4. 方法设计

### 4.1 方法整体流程

X-EPRINT 采用三阶段流水线：(1) 零样本跨环境识别——在源环境训练模型，不使用目标环境样本即可识别目标环境中的监控网站；(2) 感知潜力的流量重采样——基于零样本识别的置信度分数估计错误率，优先对高错误率网站在目标环境进行少量重采样；(3) 少样本环境适应——利用重采样的少量样本训练双层识别模型进行精确识别。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1: 流量预处理 | 原始加密流量 | 去除 TCP 重传包、控制包，burst 表示合并同向连续包 | burst 序列 x(k) | 消除噪声，提取方向+大小特征 |
| Step 2: 特征空间构建 | burst 序列（填充/截断至 16） | 一元算子（identity, alog）、二元算子（diff）、多元算子（hist, 统计量） | 167 维特征空间 Gamma | 覆盖多种特征表示 |
| Step 3: 不变特征生成 | 源/目标环境共有网站流量 | 自适应 Thompson sampling 求解 bilevel 组合优化，搜索最优特征子集 Gamma*_{s,t} | 不变特征子集 | 解决 C1: 特征漂移 |
| Step 4: 零样本识别 | 目标环境加密流量 T | 环境识别 + 基于不变特征的二分类 RF + 置信度分数 | 识别结果 + 置信度 | 初始识别 |
| Step 5: 感知潜力重采样 | 置信度分数 | 逻辑回归估计错误率，按降序排列重采样列表 | 重采样列表 L_d | 解决 C2: 采样困境 |
| Step 6: 双层识别模型 | 重采样的少量样本 | 低层：排除 prevalent 流 + 识别 anchor 流；高层：流间特征向量 + 数据增强 + 分类 | 精确识别结果 | 解决 C3: 少样本泛化 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 特征空间构建 | 提取 167 维 burst 级特征 | burst 序列 | 特征向量 | 为不变特征生成提供候选特征集 |
| 自适应 Thompson Sampling | 搜索跨环境不变特征子集 | 源/目标环境共有网站流量 | Gamma*_{s,t} | 核心优化模块 |
| 环境识别器 | 确定加密流量来自哪个环境 | 流量 T | 目标环境 Theta_t | 决定使用哪组不变特征 |
| 零样本分类器 Phi | 基于不变特征的二分类 RF | 特征向量 g(x, Gamma*) | 置信度分数 | 为重采样提供错误率估计 |
| 感潜力重采样器 | 优先重采样高错误率网站 | 置信度分数 | 重采样列表 | 指导少样本适应的样本采集 |
| 低层模型 | prevalent 流排除 + anchor 流识别 | 网络流 | 流分类结果 | 为高层模型提供流间特征 |
| 高层模型 Psi | 流间特征分类 + 数据增强 | 流间特征向量 z_j | 最终识别结果 | 输出最终识别结果 |

### 4.4 公式、算法和机制解释

**不变特征生成（核心公式）**：

$$
\max_{\Gamma_{s,t}} E(\Gamma_{s,t}) = \text{F1-Score}(\mathbf{Y}^t, [f_{\theta^*}(\mathbf{g}(\mathbf{X}^t(i), \Gamma_{s,t}))])
$$

这是一个 bilevel 优化问题：外层最大化目标环境的 F1 分数，内层在源环境训练分类器 theta*。通过将特征子集选择建模为组合多臂老虎机问题，使用 Thompson sampling 求解。

**自适应 Thompson Sampling 的关键创新**：注入 K_max - K_min 个 dummy 特征（常数特征），使搜索空间中特征子集大小自适应确定，无需预设。迭代过程 S1-S4：采样 Bernoulli 参数 → 选择 top K_max 特征 → 评估 F1 → 更新 Beta 分布先验。

**流间数据增强**：通过随机掩码向量 m_j ~ Bernoulli(1 - rho_da) 模拟 anchor 流在识别阶段被误识别的场景，增强模型鲁棒性。

### 4.5 方法优势

1. **零样本能力**：无需目标环境训练数据即可识别，大幅降低部署成本
2. **自适应特征搜索**：Thompson sampling 自动发现不变特征，无需人工设计
3. **资源高效**：感知潜力重采样仅需 10% 网站即可获得大部分收益
4. **两层鲁棒性**：invariant features 应对特征漂移 + inter-flow augmentation 应对少样本过拟合

### 4.6 方法不足

1. **环境识别依赖**：零样本识别的前提是正确识别目标环境，需要少量环境标注样本
2. **特征空间局限**：167 维特征基于手工设计的算子，未利用深度学习的自动特征提取能力
3. **RF 分类器容量有限**：随机森林在复杂流量模式下的表达能力不如深度模型
4. **Firefox 场景性能下降**：Firefox 的跨环境特征漂移更严重，方法表现相对弱于其他浏览器
5. **重采样仍需主动访问**：少样本适应阶段仍需主动访问目标网站采集流量，存在暴露风险

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 维度 | 传统 WF（CAWF, TF） | X-EPRINT |
|---|---|---|
| 训练-测试假设 | 同一环境 | 跨环境（源 → 目标） |
| 特征选择 | 固定特征集或端到端学习 | 自适应搜索跨环境不变特征子集 |
| 适应策略 | 无或全量重采样 | 感知潜力的定向重采样 |
| 少样本能力 | 弱（需大量数据） | 强（3 样本即可达 F1=0.925） |

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 跨环境 WF 问题定义 | 首次定义跨环境 WF 问题并系统分析三重挑战 | 高 | 是（任何跨域流量分析） |
| 自适应 Thompson Sampling | 注入 dummy 特征实现特征子集大小自适应 | 中 | 是（通用特征选择） |
| 感知潜力的流量重采样 | 基于置信度估计错误率，优先重采样高错误率网站 | 中 | 是（主动学习场景） |
| 双层识别 + 流间数据增强 | 低层 anchor 流识别 + 高层流间特征 + 随机掩码增强 | 中 | 部分（WF 特定） |

### 5.3 适用场景

- 加密代理环境中的网站监控（不同浏览器/代理软件组合）
- 需要快速部署到新环境的 WF 攻击场景
- 训练数据有限的跨域流量分类任务

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| CAWF (Ma et al., 2021) | 上下文感知特征提取 | 假设同环境训练/测试，跨环境性能骤降 | 通过不变特征生成解决跨环境漂移 |
| TF (Sirinam et al., 2019) | 度量学习支持 few-shot | 基于 direction sequence，跨环境泛化差 | burst 级统计特征更鲁棒 |
| BRF（消融版） | 简单 burst 特征 + RF | 无不变特征选择，零样本性能差 | 增加自适应 Thompson sampling |
| ERF（消融版） | 全 167 维特征 + RF | 全特征包含环境相关噪声 | 增加不变特征选择 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

三个研究问题：
- **RQ1**：零样本跨环境识别效果如何？（18 种跨环境场景）
- **RQ2**：少样本环境适应效果如何？（3/5/10-shot）
- **RQ3**：感知潜力重采样的提升效果如何？

开放世界设置：400 个监控网站 + 50 个非监控网站，正负样本比 1:50。

### 6.2 数据集

| 数据集 | 规模 | 环境配置 | 采样 |
|---|---|---|---|
| CE-450x6 | 450 网站 x 6 环境 | 2 代理（Shadowsocks, V2Ray）x 3 浏览器（Chrome, Edge, Firefox） | 50 样本/网站/环境 |

### 6.3 Baseline

| 方法 | 类型 | 特点 |
|---|---|---|
| CAWF | SOTA WF for encrypted proxies | 上下文感知特征 |
| TF | SOTA few-shot WF | 度量学习 + KNN |
| BRF | 消融基线 | burst 特征 + RF（无不变特征） |
| ERF | 消融基线 | 全 167 维特征 + RF（无不变特征） |

### 6.4 评价指标

Macro F1-score（零样本/少样本实验）、Micro F1-score（重采样实验）、环境识别准确率。

### 6.5 关键实验结果

**RQ1: 零样本跨环境识别**

| 场景 | X-EPRINT | 最优基线 (ERF) | 提升 |
|---|---:|---:|---:|
| 跨浏览器平均 | 0.729 | 0.488 | +49.4% |
| 跨代理平均 | 0.701 | 0.386 | +81.6% |
| 总体平均 | 0.719 | 0.454 | +58.4% |

**RQ2: 少样本环境适应**

| N-Shot | X-EPRINT | 最优基线 | 提升 |
|---|---:|---:|---|
| 3-shot | 0.925 | 0.841 (BRF) | +10.0% |
| 5-shot | 0.939 | 0.882 (BRF) | +6.5% |
| 10-shot | 0.962 | 0.918 (BRF) | +4.8% |

**RQ3: 感知潜力重采样**

| 指标 | 感知潜力重采样 | 随机重采样 | 倍数 |
|---|---:|---:|---:|
| 10% 重采样 F1 提升 | +0.0741 | +0.0187 | 3.97x |

**环境识别**：200 个样本即可达到 F1=1.000（所有环境）。

### 6.6 优势最明显的场景

- **跨代理场景**：X-EPRINT 相比最优基线提升 81.6%，因为代理软件差异导致的特征漂移最严重，不变特征方法收益最大
- **少样本场景**（3-shot）：流间数据增强效果显著，比无增强的 BRF 高 10%
- **低重采样比例**：感知潜力重采样在 10% 比例下即可获得近 40% 的全量重采样收益

### 6.7 局限性

1. Firefox 场景性能相对较低，特征漂移更严重
2. 需要预先采集源/目标环境共有网站（W_s ∩ W_t）来学习不变特征
3. 环境识别模块需要少量环境标注数据
4. 实验仅覆盖 2 种代理 + 3 种浏览器 = 6 种环境组合，真实环境多样性更高
5. 基于 RF 的分类器可能在更大规模网站集上性能下降

---

## 7. 学习与应用

### 7.1 是否开源？

是。代码和数据公开于 https://github.com/cry4tal1/xeprint。

### 7.2 复现关键步骤

1. 构建测试环境：部署 Shadowsocks + V2Ray 代理，3 种浏览器（Chrome, Edge, Firefox）
2. 自动化流量采集：Selenium 访问 450 个 Alexa 热门网站，Tcpdump 抓取加密代理流量
3. 流量预处理：去除 TCP 重传/控制包 → burst 表示 → 填充/截断至 16 burst
4. 特征提取：167 维算子特征（identity, alog, diff, hist, 统计量）
5. 训练：自适应 Thompson sampling 搜索不变特征 → RF 分类器 → 置信度估计 → 重采样 → 双层模型

### 7.3 关键超参数、预处理和训练细节

| 参数 | 值 | 说明 |
|---|---|---|
| burst 长度 n | 16 | 填充/截断固定长度 |
| 特征维度 | 167 | 全特征空间 |
| K_min / K_max | 未明确给出 | 不变特征子集大小范围 |
| 重采样样本数 N | 3/5/10 | 少样本适应的样本数 |
| Thompson sampling 最大迭代 | 未明确 | 收敛或达到上限停止 |
| 重采样比例 eta_r | 10%-100% | 监控网站的重采样比例 |

### 7.4 能否迁移到其他任务？

**高度可迁移的概念**：
- **跨环境不变特征搜索**：Thompson sampling + dummy 特征的自适应特征选择框架可迁移到任何需要域适应的流量分类任务（如跨网络条件的恶意流量检测）
- **感知潜力的主动采样**：基于置信度估计错误率的重采样策略可迁移到主动学习场景
- **流间数据增强**：随机掩码技术可用于任何基于流级特征的少样本学习

**需注意**：
- 167 维算子特征是 WF 特定的，其他任务需要重新设计特征算子
- RF 分类器的选择可能限制了在更复杂任务上的表现

### 7.5 对我的研究有什么启发？

1. **域适应的新视角**：通过特征子集搜索（而非特征空间对齐）实现跨域迁移，这对 [[encrypted-traffic-analysis]] 中的跨网络条件泛化问题有启发
2. **主动学习与 WF 的结合**：感知潜力的重采样将主动学习思想引入 WF，可用于减少 [[website-fingerprinting]] 的数据采集成本
3. **环境漂移量化**：DTW 距离分析框架可复用于量化其他跨域场景的分布差异
4. **与 [[survey-website-fingerprinting]] 的关联**：本文开辟了"跨环境 WF"这一新方向，应纳入 WF 综述

---

## 8. 总结

### 8.1 核心思想

> 自适应搜索跨环境不变特征 + 按需重采样实现跨环境网站指纹。

### 8.2 速记版 Pipeline

1. 预处理：加密流量 → burst 表示 → 167 维特征
2. 不变特征搜索：自适应 Thompson sampling 在源/目标环境共有网站上搜索最优特征子集
3. 零样本识别：基于不变特征的 RF 分类器 + 置信度分数
4. 感知潜力重采样：置信度 → 错误率估计 → 优先重采样高错误率网站
5. 少样本适应：双层模型（低层 anchor 流识别 + 高层流间特征 + 数据增强）

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]]
- [[encrypted-traffic-analysis]]
- [[traffic-representation-learning]]

### 9.2 相关方法

- [[survey-website-fingerprinting]]

### 9.3 相关任务

- [[website-fingerprinting]] — 跨环境变体
- 零样本/少样本流量分类
- 跨域流量特征迁移

### 9.4 可更新的综述页面

- [[survey-website-fingerprinting]] — 应新增"跨环境 WF"子节

### 9.5 可加入的对比表

- WF 方法跨环境鲁棒性对比表
- WF 方法少样本能力对比表

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 跨环境 DTW 距离显著大于单环境 | Fig. 1: 跨代理平均 5 vs 单环境 3；跨浏览器平均 9 vs 4 | §II-A |
| X-EPRINT 零样本 F1=0.719 | Table II + III: 跨浏览器 0.729, 跨代理 0.701 | §VI-C |
| 比最优基线高 58.4% | ERF 平均 0.454, X-EPRINT 0.719 | §VI-C |
| 3-shot F1=0.925 | Table IV: 3-shot 平均 0.925 | §VI-D |
| 感知潜力重采样 3.97 倍优势 | Fig. 3(a): 10% 重采样 P-A 提升 0.0741 vs 随机 0.0187 | §VI-E |
| 环境识别 200 样本达 F1=1.000 | Table V | §VI-C |
| Firefox 特征漂移更严重 | Fig. 1: Firefox 相关场景 DTW 距离更大 | §II-A, §VI-C |

---

## 11. 原始资料链接

- PDF：-
- MinerU Markdown：`02-parsed-markdown/2025-INFOCOM-Cross-Environmental_Website_Fingerprinting.md`
- 代码：https://github.com/cry4tal1/xeprint

---

## 12. 后续问题

- 不变特征子集的具体大小和物理含义是什么？哪些类型的特征被选为不变特征？
- 如果目标环境中完全没有共有网站（W_s ∩ W_t = 空集），方法是否仍然可行？
- 与深度学习方法（如 DF, CAWF 的 CNN 模型）结合能否进一步提升性能？
- 在更多环境组合（如不同网络带宽、不同地理位置）下方法的鲁棒性如何？
- 与 Swallow (CCS 2025) 等同时期工作的技术路线对比如何？

---
type: paper
title_original: "ResAware: Cross-Environment Website Fingerprinting via Resource-Privileged Distillation"
title_cn: "ResAware: 基于资源特权蒸馏的跨环境网站指纹攻击"
authors: ["Chongru Fan", "Wei Wang", "Wentao Huang", "Zhenquan Ding", "Jinqiao Shi", "Lei Cui", "Zhiyu Hao", "Xiaochun Yun"]
year: 2026
venue: "arXiv 2026"
doi: unknown
url: "https://arxiv.org/abs/2605.xxxxx"
pdf: unknown
mineru_md: "02-parsed-markdown/2026-arXiv-ResAware__Cross-Environment_Website_Fingerprinting_via_Resource-Privileged_Distillation.md"
status: processed
reading_level: L2
research_area: ["website fingerprinting", "encrypted traffic analysis", "knowledge distillation", "cross-environment robustness"]
task: ["website fingerprinting", "cross-environment generalization", "privileged information learning"]
method: ["knowledge distillation", "privileged information (LUPI)", "Transformer encoder", "cross-modal distillation", "soft-target supervision"]
dataset: ["self-collected (160K+ paired samples, 5 months, 6 vantage points, 100 monitored sites)", "Tranco Top 100K"]
code: "https://github.com/aimafan123/ResAware"
relevance: medium
created: "2026-06-21"
updated: "2026-06-21"
---

# ResAware: Cross-Environment Website Fingerprinting via Resource-Privileged Distillation

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | ResAware: Cross-Environment Website Fingerprinting via Resource-Privileged Distillation |
| 中文标题 | ResAware: 基于资源特权蒸馏的跨环境网站指纹攻击 |
| 作者 | Chongru Fan (北京邮电大学 & 中关村实验室), Wei Wang (中关村实验室), Wentao Huang (北京邮电大学), Zhenquan Ding (中关村实验室), Jinqiao Shi (北京邮电大学), Lei Cui (中关村实验室), Zhiyu Hao (中关村实验室), Xiaochun Yun (中关村实验室) |
| 年份 | 2026 |
| 会议/期刊 | arXiv preprint (2026) |
| 研究方向 | 网站指纹攻击、加密流量分析、跨环境鲁棒性、知识蒸馏 |
| 任务类型 | 在训练环境和部署环境不同时（时间漂移、地理漂移、代理混淆、浏览器差异）保持 WF 攻击的准确率 |
| 方法关键词 | Training-Rich/Inference-Poor 不对称威胁模型, 特权信息 (LUPI), 跨模态知识蒸馏, 资源级教师模型, 软目标监督 |
| 数据集 | 自建大规模配对数据集: 160,000+ 样本, 5 个月跨度, 6 个全球节点 (US/JP/SG/ZA/AU/DE), 100 监控网站 + 83,645 非监控网站; 基于 Tranco Top 100K |
| 是否开源 | 是 (https://github.com/aimafan123/ResAware)，含训练/评估代码、6 个 backbone 实现、特征化数据集 |
| PDF | 待补充 |
| MinerU Markdown | 02-parsed-markdown/2026-arXiv-ResAware__Cross-Environment_Website_Fingerprinting_via_Resource-Privileged_Distillation.md |

---

## 1. 一句话总结

> 提出 ResAware，一种 training-rich/inference-poor 不对称设置下的跨模态知识蒸馏框架：离线阶段利用应用层资源序列（类型+大小）训练教师模型，将其类间拓扑知识蒸馏到仅使用加密流量的学生模型，部署时零额外开销；在 150 天时间漂移下将 Var-CNN 的 F1 从 72.77% 提升至 81.49%，开放世界 TPR@1%FPR 从 22.40% 提升至 27.20%。

---

## 2. 摘要翻译

### 2.1 摘要原文

While Website Fingerprinting (WF) attacks achieve high accuracy in controlled laboratory settings, they often degrade substantially in real-world environments due to spatio-temporal drift, browser heterogeneity, proxy obfuscation and etc. This limitation stems from their sole reliance on low-level traffic features that are noisy and highly sensitive to environmental perturbations. To address this problem, we propose ResAware, a cross-environment resource-aware distillation framework under a training-rich/inference-poor asymmetric setting. Specifically, ResAware trains a teacher model on resource-level features, and then distills the resulting privileged knowledge into a student model through heterogeneous knowledge distillation. At deployment time, the student model performs inference using only encrypted traffic, incurring zero additional cost. We evaluate ResAware on a large-scale dataset collected over five months from six globally distributed vantage points, comprising more than 160,000 paired samples. The results show that ResAware significantly enhances the cross-environment robustness of diverse WF baselines. Under a 150-day temporal drift, for example, ResAware improves the F1-score of Var-CNN from 72.77% to 81.49% and the open-world TPR@1%FPR from 22.40% to 27.20%. Our results demonstrate that resource-level supervision improves WF robustness without expanding online observation capabilities.

### 2.2 摘要中文翻译

网站指纹（WF）攻击在受控实验室环境中能达到高准确率，但在真实环境中往往因时空漂移、浏览器异构性和代理混淆等因素而显著退化。这一局限源于其对底层流量特征的唯一依赖，这些特征噪声大且对环境扰动高度敏感。为解决此问题，我们提出 ResAware，一种 training-rich/inference-poor 不对称设置下的跨环境资源感知蒸馏框架。具体而言，ResAware 在资源级特征上训练教师模型，然后通过异构知识蒸馏将所得特权知识蒸馏到学生模型。部署时，学生模型仅使用加密流量进行推理，零额外开销。我们在五个月内在六个全球分布的观测点收集的大规模数据集（超过 160,000 个配对样本）上评估 ResAware。结果表明，ResAware 显著增强了多种 WF 基线的跨环境鲁棒性。例如，在 150 天时间漂移下，ResAware 将 Var-CNN 的 F1 从 72.77% 提升至 81.49%，开放世界 TPR@1%FPR 从 22.40% 提升至 27.20%。结果证明，资源级监督可在不扩展在线观察能力的情况下提升 WF 鲁棒性。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

WF 攻击在实验室 IID 设置下表现优异，但在真实部署中面临**跨环境性能退化**问题。根本原因在于现有方法完全依赖底层流量特征（包长度、方向、时序），这些特征同时受网站内容结构和传输层动态（TCP 拥塞控制、HTTP/2 多路复用、CDN 路由、浏览器调度）的共同影响，导致训练和测试环境稍有变化就会破坏学到的模式。

作者的核心洞察：**网站的身份由其应用层资源组成和依赖模式决定**（HTML/CSS/JS/图片的类型、大小、加载顺序），这些资源级特征比底层流量特征更稳定。但资源级信息在实践中通常需要解密流量才能获取，超出了标准被动窃听者的能力。

### 3.2 现有方法的痛点和不足

| 方法类别 | 代表工作 | 核心局限 |
|---|---|---|
| 更鲁棒的流量表示 | Shen et al. (USENIX Security'23), Bahramali et al. (CCS'23) | 仍在加密流量域内工作，信号不稳定源于流量之外的因素，表示层面的修复有上限 |
| 域适应（few-shot/TTA） | Triplet Fingerprinting (CCS'19), Proteus (NDSS'26) | 需要部署后收集目标域数据，且适应后的模型仍锚定在不稳定的流量域信号上 |
| 资源感知 WF | STAR (arXiv'25), MRCGCN (TIFS'25), HOLMES (WWW'25) | STAR/MRCGCN 在推理时需要资源信息，扩展了攻击者的在线观测需求；HOLMES 从流量推断资源结构但受限于流量能揭示的内容 |

**关键差距**：所有现有方法要么仅使用流量特征（不稳定），要么在推理时需要资源特征（不实际）。没有方法在训练时利用资源级稳定性而推理时仅使用加密流量。

### 3.3 论文的研究假设或核心直觉

**核心直觉（Figure 1 展示）**：网站的身份体现在其架构和资源加载模式中。一次浏览可以看作一系列资源交付过程，这些过程经过环境噪声的"塑形"后表现为可观测的网络流量。资源序列反映的是网站特定的加载逻辑（较稳定），而观测到的流量只是这一过程的噪声投影（不稳定）。

**形式化为特权信息问题**：资源级信息在离线训练时可用（通过受控爬虫+TLS 密钥日志），但在在线推理时不可用。这正好符合 Vapnik 的 Learning Using Privileged Information (LUPI) 范式——辅助监督信号在训练时指导学习，但不作为推理时的输入。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | WF 模型在跨时间/跨地域/跨代理场景下准确率大幅下降 | §1, 引用 [7,8,22,38] |
| 痛点提炼 | 现有模型过度依赖瞬态的、环境特定的网络伪影，泛化能力差 | §1 |
| 问题转化 | 能否利用训练时可获得的更稳定的应用层资源信息来改善仅使用流量的推理模型？ | §3.1-3.2 |
| 文献定位 | 资源感知 WF 已有初步探索，但均未解决"训练时可用/推理时不可用"的不对称设置 | §7 Related Work |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 资源级特征比流量级特征在跨环境条件下更稳定、更具判别力，且这种稳定性可以通过知识蒸馏转移到流量-only 模型 | §3.1 Finding 1 & 2 | CESM 指标测量 + 分类器对比实验 |
| 辅助假设 | 软目标蒸馏传递的是类间拓扑关系（哪些网站相似），而非简单的标签平滑 | §5.5 消融实验 | Traffic KD / Class-Shuffled Resource KD 对比 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 资源特征更稳定 | 支撑 | F_cat CESM 0.675 vs F_burst 0.218（跨地域），3.09 倍优势 | §3.1 Finding 1 |
| 资源稳定性可转移 | 支撑 | Resource-Only 模型 150 天 F1 仅降 14.22 点 vs Traffic-Only 降 33.30 点 | §3.1 Finding 2 |
| 蒸馏传递类间拓扑 | 支撑 | ResAware Var-CNN KL-to-Teacher 0.30 vs baseline 2.11；Class-Shuffled KD 性能回落至 baseline | §5.5, §5.7 Table 7 |

---

## 4. 方法设计

### 4.1 方法整体流程

ResAware 分为三个严格分离的阶段：

1. **Stage 1 - 资源特征提取与教师训练**：从配对样本 (x, x*, y) 中提取资源序列（类别+大小两通道），训练 Transformer 教师模型
2. **Stage 2 - 跨模态知识蒸馏**：冻结教师，用软目标 + 硬标签联合优化流量-only 学生模型
3. **Stage 3 - 部署**：丢弃所有资源侧组件（资源解析器、教师模型、蒸馏损失），仅部署学生模型

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Stage 1: 资源序列构建 | 原始资源记录 R_i | 按请求发起时间排序；映射为 9 类资源类别 (HTML/CSS/JS/Image 等) + log 轴缩放大小；截断/填充至 N=200 | 两通道序列 x* = {(c_i, s_tilde_i)} | 提取稳定的资源级表示 |
| Stage 1: 教师训练 | 资源序列 x*, 标签 y | Transformer Encoder + 位置编码 + 分类头；硬标签交叉熵损失 | 冻结的教师模型 T | 学习资源侧判别模式 |
| Stage 2: 知识蒸馏 | 流量 x（学生输入）+ 资源 x*（教师输入） | 教师产生软目标 z_T = T(x*)；学生产生 z_S = S(x)；L_total = (1-alpha)L_cls + alpha*L_kd | 优化后的学生模型 S | 将资源侧类间拓扑转移到流量-only 学生 |
| Stage 3: 部署 | 加密流量 x | 仅运行学生模型 S(x) | 网站预测 | 零额外推理开销 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 资源序列编码器 | 将变长资源序列转为固定长度两通道表示 | 原始 HTTP 资源记录 | Z = {(c_i, s_tilde_i)}, N=200 | 仅在 Stage 1 使用，Stage 3 丢弃 |
| 教师模型 (Transformer) | 从资源序列学习网站身份表示 | 两通道资源序列 x* | 软目标 logits z_T | Stage 2 冻结，提供蒸馏监督 |
| 学生模型 (任意 WF backbone) | 从加密流量推理网站身份 | 加密流量 x | logits z_S | 接收教师的软目标蒸馏 |
| 蒸馏损失 L_kd | 传递教师的类间拓扑 | z_T, z_S | KL 散度 | 与分类损失 L_cls 加权组合 |

### 4.4 公式、算法和机制解释

**资源序列表示**（公式 3）：

每个页面加载表示为 N 个资源事件的序列 Z = {(c_i, s_tilde_i)}_{i=1}^N，其中 c_i 是 9 类资源类别 ID，s_tilde_i = log(1 + payload_bytes) 是 log 缩放的载荷大小。关键设计：按**请求发起时间**排序（而非响应完成时间），因为发起时间更直接反映浏览器引擎的解析进度和资源依赖触发逻辑，与传输层时序变化解耦。

**分类损失**（公式 4）：

L_cls = -sum_{c=1}^{C} y_c * log(softmax(z_S))，标准交叉熵，保持学生对地面真标签的判别能力。

**资源特权蒸馏损失**（公式 5）：

L_kd = tau^2 * D_KL(softmax(z_T/tau) || softmax(z_S/tau))，温度 tau 展平后验分布，放大类间相似性信号。关键：传递的不是原始资源序列，而是教师编码的**类级关系知识**——"哪些网站具有相似的资源加载结构"。

**联合目标**（公式 6）：

L_total = (1-alpha) * L_cls + alpha * L_kd，alpha 控制分类目标和特权蒸馏目标的权衡。alpha=0 退化为标准 ERM 训练的流量-only 分类器。

**Cross-Environment Stability Margin (CESM)**（公式 2）：

CESM_F(s,t) = 1 - Delta_same^F / Delta_diff^F，衡量特征 F 在跨环境条件下同类内漂移与异类间距离的比值。越高表示特征越鲁棒。

### 4.5 方法优势

1. **零推理开销**：部署时仅保留学生模型，与原始 WF 分类器完全相同的推理延迟和内存占用
2. **即插即用**：不修改 backbone 架构，仅通过训练目标集成，兼容任意 WF 模型
3. **与域适应正交互补**：ResAware 提供更好的源域初始化，Proteus 等方法提供目标域校准，两者结合效果叠加（Table 5: Var-CNN 平均 F1 从 38.79% 到 69.14%）
4. **大规模验证**：160K+ 样本、5 个月、6 个全球节点、6 种 backbone、4 种漂移场景

### 4.6 方法不足

1. **非无条件增强器**：当浏览器执行层或协议封装层的漂移破坏流量-资源对应关系时，蒸馏可能产生负迁移（如 DF 在代理漂移下 -1.04%）
2. **依赖学生容量**：低容量学生（如 AWF）吸收教师拓扑的能力有限，增益天花板低
3. **资源结构假设**：假设目标环境中资源结构保持足够稳定性；高度个性化页面、频繁 A/B 测试、重度广告注入可能削弱这一假设
4. **未评估 Tor**：Tor 的固定大小单元、多路复用和拥塞控制进一步模糊了资源大小与可观测包序列的对应关系
5. **超参数耦合**：最优 alpha 与学生 backbone 容量耦合，需要在源域验证集上调参

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 对比维度 | 传统 WF (DF/Var-CNN) | 域适应 (Proteus) | 资源感知 (STAR/MRCGCN) | **ResAware** |
|---|---|---|---|---|
| 训练时信息 | 仅加密流量 | 仅加密流量 + 少量目标域数据 | 流量 + 资源 | 流量 + 资源 |
| 推理时信息 | 仅加密流量 | 仅加密流量 | 流量 + 资源 | **仅加密流量** |
| 跨环境鲁棒性 | 差 | 中（需目标域数据） | 好（但扩展攻击面） | **好（不扩展攻击面）** |
| 部署开销 | 标准 | 需要目标域采集 | 需要资源访问 | **零额外开销** |

**本质区别**：ResAware 是唯一一个在训练时利用资源级稳定性而推理时保持标准被动窃听者假设的方法。STAR 和 MRCGCN 虽然也利用资源信息，但它们在推理时需要这些信息，扩大了攻击者的在线观测需求。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| Training-Rich/Inference-Poor 威胁模型 | 形式化 WF 中的不对称设置：离线可控爬虫可获取资源信息，在线仅被动窃听 | 高 | 是（可推广到其他侧信道攻击） |
| 资源作为特权信息 | 将 LUPI 范式引入 WF，资源级特征作为训练时特权监督而非推理时输入 | 高 | 是（任何存在"训练时丰富/推理时贫乏"不对称的场景） |
| 跨模态异构蒸馏 | Transformer 教师（资源）→任意 backbone 学生（流量），软目标传递类间拓扑 | 中 | 是（即插即用，不修改 backbone） |
| CESM 指标 | 量化特征在跨环境条件下的稳定性和判别力 | 低 | 是（通用特征鲁棒性评估） |

### 5.3 适用场景

- **时间漂移**：模型训练后长期部署，网站随时间演变（最适用，增益最大且稳定）
- **地理漂移**：模型在一个地区训练、在另一个地区部署
- **代理混淆漂移**：用户使用 Shadowsocks/Trojan/VMess 等代理（Var-CNN 增益 +8.96%，但 DF 可能负迁移）
- **浏览器漂移**：训练和测试使用不同浏览器（绝对性能仍低，但相对增益一致）
- **与域适应结合**：作为更强的源域初始化，与 Proteus 等无监督适应方法正交互补

### 5.4 方法对比表

| 方法 | 训练信息 | 推理信息 | 零推理开销 | Var-CNN 150 天 F1 | Var-CNN 代理漂移 F1 (avg) |
|---|---|---|---|---|---|
| Var-CNN (baseline) | 流量 | 流量 | 是 | 72.77% | 38.14% |
| Proteus (NDSS'26) | 流量 + 目标域无标注 | 流量 | 是 | — | 54.89% |
| **ResAware + Var-CNN** | 流量 + 资源（离线） | 流量 | **是** | **81.49%** | **47.10%** |
| **ResAware + Proteus** | 流量 + 资源（离线） + 目标域无标注 | 流量 | **是** | — | **69.14%** |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **硬件**：双 Intel Xeon Platinum 8352S CPU, 128GB RAM, NVIDIA RTX 4090 (24GB VRAM), Ubuntu 24.04 LTS
- **实现**：Python 3.12 + PyTorch 2.10.0
- **评估场景**：5 种——时间漂移、空间漂移、代理混淆漂移、浏览器漂移、开放世界时间漂移
- **训练协议**：严格遵循各 backbone 原始论文的架构/优化器/学习率/批大小/训练轮数；ResAware 特有超参（tau, alpha）仅在源域验证集调一次，后续固定
- **重复性**：所有实验 5 次不同随机种子，报告均值

### 6.2 数据集

| 数据集子集 | 采集时间 | 节点 | 用途 | 规模 |
|---|---|---|---|---|
| Train-Base | 2025-11-21 | US (NY) | 时间/空间漂移源域 | 100 站 x 150 traces = 15,000 配对 |
| Open-World | 2025-11-21 | US (NY) | 开放世界负样本池 | 83,645 非监控站 x 1 trace |
| Geo-Drift | 2025-11-21 | JP/SG/ZA/AU/DE | 空间漂移测试 | 100 站 x 25-30 traces x 5 地点 = 14,087 配对 |
| Time-Drift | 30/60/90/120/150 天后 | US (NY) | 时间漂移测试 | 5 快照 x 100 站 x 30 traces = 15,000 配对 |
| Train-Base-2 | 2026-03-21 | US (NY) | 代理/浏览器漂移源域 | 100 站 x 150 traces = 15,000 配对 |
| Obfuscated-Proxy-Drift | 2026-03-21 | US (NY) | 代理混淆漂移测试 | 100 站 x 30 traces x 6 协议 = 18,000 配对 |
| Browser-Drift | 2026-03-21 | US (NY) | 浏览器漂移测试 | 100 站 x 25-30 traces x 2 浏览器 = 5,523 配对 |

### 6.3 Baseline

6 种代表性 WF 架构作为学生 backbone：

| Backbone | 输入特征 | alpha |
|---|---|---|
| AWF | 包方向序列 | 0.1 |
| DF | 包方向序列 | 0.5 |
| RF | 流量聚合特征 | 0.5 |
| Var-CNN | 包方向序列 | 0.7 |
| Tik-Tok | 包方向+时间戳序列 | 0.5 |
| CountMamba | 包方向+长度+时间戳序列 | 0.7 |

### 6.4 评价指标

- **封闭世界**：F1-score（主指标）、Precision、Recall
- **开放世界**：TPR@FPR=1%（主指标，在 1:100 监控/非监控不平衡比下）

### 6.5 关键实验结果

**零样本跨环境 F1 (%)：**

| 模型 | 时间漂移 (Day 150) w/o → w/ | 空间漂移 (Avg) w/o → w/ | 代理漂移 (Avg) w/o → w/ | 浏览器漂移 (Avg) w/o → w/ |
|---|---|---|---|---|
| AWF | 33.25 → 32.25 (-1.00) | 49.23 → 48.76 (-0.47) | 17.53 → 18.03 (+0.50) | 5.91 → 6.06 (+0.15) |
| DF | 61.39 → 65.79 (+4.40) | 84.71 → 86.64 (+1.93) | 48.32 → 47.28 (-1.04) | 4.07 → 6.66 (+2.59) |
| RF | 36.64 → 38.27 (+1.63) | 76.11 → 78.61 (+2.50) | 62.86 → 66.74 (+3.88) | 18.15 → 22.83 (+4.68) |
| Tik-Tok | 54.64 → 57.67 (+3.03) | 82.85 → 85.10 (+2.25) | 44.52 → 44.88 (+0.36) | 4.79 → 6.05 (+1.26) |
| Var-CNN | 72.77 → **81.49 (+8.72)** | 82.66 → **86.96 (+4.30)** | 38.14 → **47.10 (+8.96)** | 17.24 → 21.45 (+4.21) |
| CountMamba | 28.94 → 29.16 (+0.22) | 72.91 → 76.03 (+3.12) | 61.21 → 62.50 (+1.29) | 7.11 → 9.50 (+2.39) |

**开放世界 TPR@FPR=1% (%)：**

| 模型 | Day 30 | Day 60 | Day 90 | Day 120 | Day 150 |
|---|---|---|---|---|---|
| Var-CNN w/o | 48.75 | 35.70 | 27.57 | 24.92 | 22.40 |
| Var-CNN w/ | 55.07 | 41.05 | 30.43 | 28.85 | **27.20** |
| Tik-Tok w/o | 27.50 | 8.60 | 6.73 | 5.50 | 4.52 |
| Tik-Tok w/ | 50.15 | 22.63 | 16.43 | 12.93 | **10.17** |

**ResAware + Proteus 互补性（Var-CNN, 代理漂移平均 F1）：**

| ResAware | Proteus | 平均 F1 |
|---|---|---|
| w/o | w/o | 38.79% |
| w/o | w/ | 54.89% |
| w/ | w/o | 46.51% |
| w/ | w/ | **69.14%** |

### 6.6 优势最明显的场景

- **长时间漂移**（150 天）：Var-CNN +8.72%，增益随时间推移而扩大
- **代理混淆漂移**：Var-CNN +8.96%（代理严重扭曲包级形态但资源结构基本完整）
- **低样本适应**：ResAware 在 1-shot 下即显著优于 baseline（Trojan 代理：88.33% vs 77.78%）
- **开放世界严格 FPR 约束**：Tik-Tok 在 Day 30 从 27.50% 提升至 50.15%（+22.65%）

### 6.7 局限性

1. **浏览器漂移绝对性能低**：所有 backbone 在浏览器漂移下平均 F1 < 23%，ResAware 增益有限
2. **低容量 backbone 增益小或负迁移**：AWF 在时间/空间/代理漂移下出现小幅负迁移
3. **DF 在代理漂移下负迁移**（-1.04%）：跨模态蒸馏的效果取决于学生能否将流量表示与教师传递的资源拓扑对齐
4. **未评估 Tor 网络**：Tor 的固定大小单元和多路复用可能完全破坏资源大小与包序列的对应关系

---

## 7. 学习与应用

### 7.1 是否开源？

是。https://github.com/aimafan123/ResAware 含完整训练/评估代码、6 个 backbone 实现、跨环境评估脚本、特征化数据集。

### 7.2 复现关键步骤

1. 准备配对流量-资源数据集（需 TLS 密钥日志解密流量提取资源序列）
2. 训练资源-only Transformer 教师模型（资源序列输入，硬标签 CE 损失）
3. 冻结教师，联合训练流量-only 学生（L_total = (1-alpha)L_cls + alpha*L_kd）
4. 部署时丢弃教师和资源解析器，仅保留学生模型

### 7.3 关键超参数、预处理和训练细节

| 超参数 | 默认值 | 说明 |
|---|---|---|
| N (截断长度) | 200 | 资源序列最大长度 |
| tau (温度) | 在源域验证集调参 | 展平软目标分布 |
| alpha (蒸馏权重) | backbone 依赖 (0.1-0.7) | AWF=0.1, DF/RF/Tik-Tok=0.5, Var-CNN/CountMamba=0.7 |
| 资源类别数 | 9 | HTML, Tiny Image, Regular Image, CSS, JS, Font, JSON/API, Document, Unknown |

**资源序列预处理**：按请求发起时间排序（非响应完成时间）；绝对时间戳被丢弃，仅保留事件顺序（通过位置编码）；大小经 log(1+bytes) 缩放。

### 7.4 能否迁移到其他任务？

**高迁移潜力**：
- **其他侧信道攻击**：任何存在"训练时丰富/推理时贫乏"不对称的场景（如基于应用元数据训练、基于加密流量推理的恶意流量检测）
- **加密流量分类**：利用训练时可获得的协议元数据或应用层信息作为特权监督
- **模型压缩/蒸馏**：LUPI 范式本身具有通用性，教师可使用任何"推理时不可用"的辅助信息

**需注意**：核心假设是特权信息比输入信息更稳定。在其他任务中需验证这一假设是否成立。

### 7.5 对我的研究有什么启发？

1. **特权信息视角**：在加密流量分析中，可以系统性地识别哪些信息在训练时可获得但推理时不可用（如 TLS 握手元数据、DNS 查询、应用层协议头），将它们作为特权监督信号
2. **CESM 指标**：可用于评估不同流量特征在跨环境条件下的鲁棒性，指导特征选择
3. **即插即用蒸馏框架**：ResAware 的训练目标设计可直接用于改善现有 WF/流量分类模型的跨环境泛化能力
4. **与域适应的互补性**：ResAware 作为源域初始化 + 域适应方法作为目标域校准的组合策略值得借鉴

---

## 8. 总结

### 8.1 核心思想

> 资源级特权蒸馏提升跨环境 WF 鲁棒性。

### 8.2 速记版 Pipeline

1. 离线：受控爬虫采集配对流量+资源序列（通过 TLS 密钥日志解密）
2. 训练 Transformer 教师模型（资源序列输入，9 类类别 + log 大小两通道）
3. 冻结教师，用 KL 散度软目标蒸馏到流量-only 学生（L = (1-alpha)L_cls + alpha*L_kd）
4. 部署：丢弃所有资源侧组件，仅保留学生模型（零推理开销）
5. 效果：150 天漂移 Var-CNN F1 +8.72%，代理漂移 +8.96%，与 Proteus 互补至 69.14%

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]]
- [[encrypted-traffic-analysis]]
- [[traffic-representation-learning]]

### 9.2 相关方法

- [[knowledge-distillation]]
- [[privileged-information-learning]]
- [[cross-modal-learning]]

### 9.3 相关任务

- [[website-fingerprinting]]
- [[cross-environment-generalization]]

### 9.4 可更新的综述页面

- [[survey-website-fingerprinting]]

### 9.5 可加入的对比表

- [[website-fingerprinting]] 跨环境鲁棒性对比表

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 资源特征 CESM 是流量特征的 2.65-3.09 倍 | F_cat CESM 0.675 vs F_burst 0.218（跨地域） | §3.1 Finding 1 |
| 资源-Only 模型 150 天 F1 仅降 14.22 点 vs 流量-Only 降 33.30 点 | DF 架构对比实验 | §3.1 Finding 2 |
| ResAware 将 Var-CNN 150 天 F1 从 72.77% 提升至 81.49% | Table 2 | §5.2 |
| 开放世界 Tik-Tok Day 30 TPR 从 27.50% 提升至 50.15% | Table 4 | §5.3 |
| ResAware + Proteus 代理漂移平均 F1 69.14% | Table 5 | §5.4 |
| 蒸馏传递的是类间拓扑而非标签平滑 | Class-Shuffled KD 回落至 baseline | §5.5 Table 6 |
| 资源大小是最强判别通道：移除后教师 F1 从 88.97% 降至 16.16% | 消融实验 | §5.5 Figure 7 |
| ResAware 将 ECE 从 0.138 降至 0.034（4 倍改善） | 校准曲线 | §5.7 Figure 8 |
| 学生 KL-to-Teacher 从 2.11（baseline）降至 0.30（ResAware） | Table 7 | §5.7 |
| 87.5% 的 backbone x 漂移组合获得正增益 | 21/24 组合 | §5.2 |

---

## 11. 原始资料链接

- PDF：待补充
- MinerU Markdown：02-parsed-markdown/2026-arXiv-ResAware__Cross-Environment_Website_Fingerprinting_via_Resource-Privileged_Distillation.md
- 代码仓库：https://github.com/aimafan123/ResAware

---

## 12. 后续问题

- ResAware 在 Tor 网络（固定大小单元、多路复用）下的表现如何？是否需要完全不同的资源表示（如依赖图、发起者图）？
- 资源序列的"类别+大小"两通道表示是否可以进一步抽象为更稳定的结构（如资源依赖图、渲染阶段拓扑）？
- alpha 的最优值与学生容量的耦合关系能否通过自适应机制自动调节，而非手动调参？
- 在资源结构高度动态的场景（频繁 A/B 测试、重度广告注入）中，ResAware 的退化程度如何量化？
- ResAware 的 LUPI 范式能否推广到其他加密流量分析任务（如恶意流量检测、应用识别）？哪些辅助信息可作为特权信号？

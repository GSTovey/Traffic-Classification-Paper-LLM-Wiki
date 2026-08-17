---
type: paper
title_original: "Website Fingerprinting Techniques Over Tor Network: A Survey"
title_cn: "Tor 网络上的网站指纹攻击技术：综述"
authors:
  - "Faisal Murad"
  - "Depeng Chen"
  - "Rolando Trujillo-Rasua"
  - "Muhammad Alamgeer Khan"
year: 2026
venue: "IEEE Access"
doi: "10.1109/access.2026.3681766"
url: "https://doi.org/10.1109/access.2026.3681766"
pdf: "00-inbox/Aug_inbox/2026-Access-Website_Fingerprinting_Techniques_Over_Tor_Network_A_Survey.pdf"
mineru_md: "02-parsed-markdown/2026-Access-Website_Fingerprinting_Techniques_Over_Tor_Network_A_Survey.md"
status: processed
reading_level: L1
research_area:
  - 网站指纹攻击（WF）
  - 匿名网络分析（Tor）
  - 流量分析
task:
  - 网站指纹攻击（WF）
  - 匿名流量识别
method:
  - 机器学习方法（SVM/RF/KNN/XGBoost）
  - 深度学习方法（CNN/RNN/Transformer/联邦学习/元学习）
  - 变换域方法（FFT/小波）
  - 混合方法
dataset:
  - DF / Wang / AWF 系列数据集（综述汇总）
  - WTF-PAD / FRONT 等防御流量数据集（综述汇总）
code: unknown
relevance: high
created: "2026-08-17"
updated: "2026-08-17"
---

# Website Fingerprinting Techniques Over Tor Network: A Survey

> **解析质量提示**：MinerU 解析整体良好（表格转为 HTML 表格，数据完整），但正文存在少量乱码/误译（如 "fragmentary encroachments in seclusion fortification" 等表述不通顺，系原文文风问题或解析误差）。论文参考文献编号存在两处内部不一致：正文 [63] 处一作写作 "Hantao et al."（Table 2）另一处为 "Mei et al."（Table 3）；[46] 与 [66] 在正文与 Table 3 中分别对应不同内容。此外，论文头部标注 DOI 为 **10.1109/ACCESS.2026.3681766**，与用户提供的 **10.1109/access.2026.3681766** 不一致，本笔记 frontmatter 采用用户提供值。

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Website Fingerprinting Techniques Over Tor Network: A Survey |
| 中文标题 | Tor 网络上的网站指纹攻击技术：综述 |
| 作者 | Faisal Murad（安徽大学）、Depeng Chen（安徽大学）、Rolando Trujillo-Rasua（Rovira i Virgili 大学）、Muhammad Alamgeer Khan（中国科学技术大学） |
| 年份 | 2026（收稿 2026-03-17，录用 2026-04-03，发表 2026-04-07） |
| 会议/期刊 | IEEE Access，DOI 见上文（论文头部与用户提供值不一致，见提示） |
| 研究方向 | 网站指纹攻击 / Tor 匿名网络分析 |
| 任务类型 | WF 攻击方法综述（分类体系 + 方法谱系 + 基准汇总 + 研究缺口） |
| 方法关键词 | 多层分类体系；ML / DL / 变换域攻击谱系；closed/open-world；多标签浏览 |
| 数据集 | 综述汇总 28 篇攻击论文的数据集（DF、Wang、AWF 等）与基准表 |
| 是否开源 | 无（综述无代码） |
| PDF | 00-inbox/Aug_inbox/2026-Access-Website_Fingerprinting_Techniques_Over_Tor_Network_A_Survey.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-Access-Website_Fingerprinting_Techniques_Over_Tor_Network_A_Survey.md |

---

## 1. 一句话总结

> 本文综述了 2019–2025 年间针对 Tor 网络的 28 篇网站指纹（WF）攻击研究（其中 18 篇为此前综述未覆盖），提出按"动机 → 目标组件 → 方法论"组织的多层分类体系，梳理了 ML / DL / 变换域三类攻击方法谱系，并指出"真实 Tor 流量数据缺失 + 缺乏统一基准"是该领域最核心的结构性问题。

---

## 2. 摘要翻译

### 2.1 摘要原文

> The increasing reliance on the Tor network for privacy has heightened the salience, potential impact, and adversarial incentives associated with Website Fingerprinting (WF) attacks. Although Tor employs layered encryption to protect content confidentiality and conceal endpoints, WF remains feasible because encrypted Tor traffic still exposes measurable side-channel metadata, most notably packet directionality, size-related effects, and timing characteristics, that can be exploited to infer user activity. ... This paper presents a comprehensive survey of contemporary WF attacks on the Tor network, particularly focusing on advancements since 2019. We introduce a novel multi-level taxonomy that categorizes fingerprinting techniques based on their features, methodologies (including machine learning, deep learning, and hybrid approaches), and targeted components. Our analysis reveals that recent methodologies, especially those leveraging deep learning, have significantly enhanced attack accuracy and robustness, pushing the boundaries of de-anonymization in complex scenarios like multi-tab browsing. Furthermore, we highlight critical dataset and methodological gaps in current research, emphasizing the widespread reliance on simulated environments and synthetic data due to the inherent challenges of collecting real-world Tor traffic. By systematically examining existing limitations, we identify key open questions and provide concrete recommendations for future research, including the development of comprehensive datasets and standardized benchmarks...

### 2.2 摘要中文翻译

> 用户对 Tor 网络隐私保护的日益依赖，使得网站指纹（WF）攻击的重要性、潜在影响与对抗动机不断上升。尽管 Tor 采用分层加密保护内容机密性并隐藏通信端点，WF 攻击仍然可行——加密的 Tor 流量仍暴露可测量的侧信道元数据（最典型的是包方向、大小效应与时序特征），可被利用来推断用户行为。本文全面综述了 Tor 网络上的当代 WF 攻击，尤其聚焦 2019 年以来的进展。作者提出一种新的多层分类体系，按特征、方法论（含机器学习、深度学习与混合方法）及攻击目标组件对指纹技术进行分类。分析表明，近期方法（尤其是深度学习）显著提升了攻击精度与鲁棒性，将去匿名化推进到多标签浏览等复杂场景。此外，本文指出当前研究存在严重的数据集与方法论缺口——由于采集真实 Tor 流量的固有问题，研究普遍依赖模拟环境与合成数据。作者系统梳理了现有局限，识别了关键开放问题，并给出具体研究建议，包括开发更全面的数据集与标准化基准，以促进更有效的防御机制、加强 Tor 网络内的隐私保护。

---

## 3. 方法动机（综述动机）

### 3.1 作者为什么写这篇综述？

既有 Tor 攻击综述（2018 Aminuddin 流量监控、2019 Enrico 多目标攻击分类、2020 Basyoni 流量分析攻击分类）均未对 WF 攻击做专门、深入的梳理：要么只覆盖少量客户端攻击，要么缺乏具体 WF 技术的细节。而 2019 年以来 WF 攻击经历了深度学习化、多标签化、少样本化的快速演进，需要一篇专门聚焦 WF、覆盖新工作的系统综述。

### 3.2 现有综述的缺口

| 综述 | 覆盖范围 | 缺口 |
|---|---|---|
| Aminuddin 2018 [17] | Tor 加密流量监控的 ML 分类体系 | 缺乏具体指纹技术的细节 |
| Enrico 2019 [75] | 按客户端/服务器/网络分类的攻击 | 客户端攻击仅列不足 10 例，未深入 WF |
| Basyoni 2020 [49] | 8 种去匿名化/流量分析攻击 | 多为理论或建模评估，缺实时可行性，未覆盖最新 ML 攻击 |

### 3.3 综述的核心主张（研究假设）

WF 攻击的威胁被高估还是低估，取决于评估基准与安全假设是否贴近现实：单篇论文声称的高精度（如 closed-world 下 >99%）可能建立在过强的安全假设或过窄的基准之上；因此需要对攻击方法做系统分类与跨论文对比，才能判断"WF 攻击到底有多有效、能否规模化部署"这一开放问题（§1 原文明确提出）。

### 3.4 综述方法（问题发现路径）

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 文献采集 | 在 Scopus、Science Direct、IEEE Xplore、Google Scholar 以 "Website Fingerprinting attacks over Tor" 检索（2019–2025），初筛 2360+ 条后按标题/摘要/关键词/结论精筛 | §I-A |
| 纳入标准 | 聚焦 WF 攻击方法（以攻击方视角），排除防御导向研究 | §I-A |
| 最终语料 | 28 篇攻击论文，其中 18 篇发表于 2019 年后、未被先前综述覆盖 | §I-A、§I |
| 综述组织 | 按"特征表示 → 攻击技术 → 学习范式"组织核心综述，并对 closed/open-world、单/多标签、防御/非防御流量、概念漂移四组评价维度做逐篇比较 | §I |

### 3.5 科学假设形成（综述性验证）

| 假设 | 具体内容 | 验证方式 |
|---|---|---|
| 核心观察 | 深度学习方法显著提升攻击精度与鲁棒性，并把攻击边界推进到多标签浏览等复杂场景 | 跨论文基准汇总（Table 3-4） |
| 辅助观察 1 | 真实 Tor 流量采集困难导致研究普遍依赖模拟/合成数据 | 局限性分析（§VI-A/B/C） |
| 辅助观察 2 | 缺乏统一基准使攻击间可比性差、结果难以复现 | §VI-D |
| 辅助观察 3 | 攻击效果随标签数/用户数等条件波动，存在相互矛盾的结果 | §V-E（Observation 4） |

---

## 4. 综述框架与方法谱系（分类体系）

### 4.1 多层分类体系（本综述核心贡献）

本综述按三层组织 WF 技术分类（§IV-B、Figure 6）：

| 层级 | 分类维度 | 具体划分 |
|---|---|---|
| 顶层 | 攻击者动机 | 窃听者发起 WF 的根本目的（去匿名化/监视/内容推断） |
| 中层 | 攻击目标组件 | 电路（circuit）、隐藏服务、特定应用流量、网页/网站 |
| 底层 | 采用的方法论 | 主动（修改/阻碍用户流量，如协议级攻击）vs 被动（仅观察不干预） |

另有辅助划分维度（§IV-B）：按**所用特征**（包顺序/大小/时序、电路特征）、按**攻击技术**（主动/被动）、按**机器学习模型**（SVM/KNN/RF 等）。

### 4.2 WF 利用的侧信道特征（§V-A.1）

| 特征 | 说明 |
|---|---|
| Tor 电路特征 | 多中继路径产生可识别的时序模式，匿名化后各网站的包模式仍相对独特 |
| 包长度与方向 | 不同网站有独特的包大小分布与进出方向比例 |
| 时序窗口 | 包时序、包间间隔与请求-响应间隙暴露内容差异 |
| Burst 突发模式 | 突发大小/周期/方向（进出平衡）区分多媒体与文本型网站 |
| IP 端口接入点 | 出入口接入点与其他元数据结合提供间接线索 |

### 4.3 攻击方法谱系

#### （1）机器学习方法（§V-B）
- **数值特征 + 统计**：Platzer [46] 利用收发/转发时序差异对隐藏服务去匿名化，在真实 Tor 上宣称 100% 去匿名率、每日监视 2.5 万请求；Yoshiura [47] 用 SYN 后 3 秒窗口的包数模式收集隐藏服务 IP。
- **经典分类器**：Bit-FP [60]（RF + 包大小/方向，Bitcoin 隐藏服务识别，ACC 98.9%）；WFA [63]（两阶段 ML 应对 open-world 与速率偏差）；电路指纹 [62]（SVM/XGBoost/RF 区分客户端与洋葱服务电路，召回/精确率 99%）。

#### （2）深度学习方法（§V-C）
- **多标签浏览**：ARES [31]（多标签分类 + Trans-WF Transformer，真实多标签会话 91.3%）；BAPM [43]（多头注意力直接处理重叠流量，无需预切分）；MT-WFA/WFD [73]（trace 定位 + 网站分类联合）；TIOD [68]（流量转图像 + 目标检测，双标签场景 >85% 且无需已知标签数）；FD-WF [71]（固定维度 + ResNet 处理混合标签）。
- **鲁棒性/少样本**：DNNF [34]（CNN 特征 + KNN，小样本 + 概念漂移鲁棒，96.2%）；snWF [32]（快照集成，open-world 91%、低误报）；TFAN [67]（元学习 + 岭回归任务自适应对齐，1-shot 92.8%，42 天后仍 >90%）；CTWF [69]（紧凑卷积 Transformer，含时序漂移与防御场景下 99.42%）；LASERBEAK [72]（Transformer + 多通道表示，对 FRONT 防御 96%，较 SOTA +36.2%，并公开 50 万样本数据集）；Holmes [74]（早期攻击，仅需 21.71% 页面加载量，平均 F1 提升 169%）。
- **联邦/持续学习**：FedFingerprinting [30]（联邦学习，训练时间降低 18%，85% 精度快速收敛）；EIL-WF [79]（增量学习适应新站点与漂移）；CoMask [77]（半监督 MSP + 对比学习）、FMWF [78]（少样本多标签迁移）、CoDA [81]（跨域原型对齐）、COUNTMAMBA [82]（粗粒度表示 + 细粒度预测）。

#### （3）变换域方法（§V-D）
- **FFT**：Jahani [35] 在线 WF 攻击（频域周期模式，抗噪）；FDF [36] 频域指纹（自注意力+CNN+FC，未防御 98.8% / WTF-PAD 防御 94.3%）。
- **小波**：Lai [41] 小波 + SVM（平均 96.7%）；Tiny WFP [40] burst 编码 + 小波分解（轻量，对 WTF-PAD 90.5%、对 Walkie-Talkie top-2 98.2%，推理比 DF 快 15 倍、比 VAR-CNN 快 55 倍）。
- 变换域方法优势：计算高效、可解释、适合资源受限/实时场景；劣势：对噪声/混淆敏感、扩展性弱、需手工更新。

### 4.4 评价维度（综述归纳）

| 维度 | 说明 |
|---|---|
| 场景 | closed-world（理论上限）/ open-world（现实） |
| 标签复杂度 | 单标签 / 多标签（multi-tab）浏览 |
| 防御状态 | 未防御 / 防御流量（WTF-PAD、FRONT、Walkie-Talkie、Traffic Sliver、GLUE 等） |
| 时间维度 | 概念漂移（AUC 随时间衰减） |

---

## 5. 与其他方法对比（综述横向对比）

### 5.1 与既往综述的对比（Table 1）

| 综述 | 年份 | 攻击数 | 专门覆盖 WF |
|---|---|---|---|
| Aminuddin [17] | 2018 | 未给出 | 否 |
| Enrico [75] | 2019 | 13 | 否 |
| Basyoni [49] | 2020 | 8 | 否 |
| **本文** | 2026 | **28（18 篇为 2019 后新工作）** | **是** |

### 5.2 跨论文关键基准摘选（Table 3，ACC / FP / 概念漂移）

| 方法 | 数据集 | ACC | FP | 概念漂移（AUC 随时间） |
|---|---|---|---|---|
| ARES [31] | 真实多标签 Tor 会话 | 91.3% | 5% | 初始 100% → 30 天后 85.1%（-14.9%） |
| DNNF [34] | AWF/Wang 系列 | 96.2% | 1.5% | 初始 90% → 60 天后 87%（-3%） |
| snWF [32] | C0/W0/漂移集 | 91% | 5.7% | 初始 86% → 30 天后 67% |
| CWFA [33] | DF/Wang（防御+未防御） | 99% | 7% | 初始 96% → 30 天后 79% |
| FFT [35] | DSD 系列 | 98.48% | 0% | 未报告 |
| FDF [36] | 防御/未防御/洋葱服务 | 87.93% | — | 初始 98.8% → 56 天后 72% |
| TinyWFP [40] | CW/OW/WTF-PAD 系列 | 99.2% | 4.6% | 初始 96% → 30 天后 79% |
| Bit-FP [60] | Bitcoin 隐藏节点等 | 98.96% | 1.4% | 初始 96% → 56 天后 76% |
| SVM/RF/XGBoost [62] | 电路数据集 | 99.99% | 0.01% | 初始 98% → 60 天后 91% |
| TFAN [67] | AWF900/open-world/DS-19 | 95.6% | <5% | 1-shot 初始 93.2% → 30 天后 90.4% |
| TIOD [68] | 双/三标签、GLUE 防御 | 85% | — | 未报告 |
| CTWF [69] | AWF 系列 + WTF-PAD + 漂移 | 99.42% | — | 未报告 |
| LASERBEAK [72] | Big Enough/Gong-Surakav 等 | 96% | — | 未报告 |
| Holmes [74] | Alexa/dark web + 多防御 | 98.63% | — | 未报告 |

> 注：表中数字均转引自综述 Table 3，各论文数据集/防御设置不同，**不可直接横向比较**；综述本身未复现任何实验。

### 5.3 系统性能评估汇总（Table 4，选摘）

| 方法 | 计算开销 | 延迟 | 对抗鲁棒性 | 实时可行性 |
|---|---|---|---|---|
| TFAN [67] | 低 | 低（岭回归高效对齐） | 抗 WTF-PAD 与时间漂移 | 可行 |
| ARES [31] | 很高 | 每网站分类器 0.26–0.42s | WTF-PAD 下 84% AUC、FRONT 下 76% | 可并行但资源密集 |
| TIOD [68] | 高 | — | 抗自然重叠，弱于主动防御 | <5 标签可行，>5 不可行 |
| Holmes [74] | 中 | 暗网平均 45.25s、21.71% 页面加载量 | 抗 WTF-PAD/Walkie-Talkie/Traffic Sliver | 离线在线均可行 |
| TinyWFP [40] | 低 | 1000 实例 545ms（比 DF 快 15×） | 抗 WTF-PAD，对 W-T 有限 | 路由器/木马级弱攻击者可用 |
| FFT [35] | 低 | 单次检测 <2s | 抗轻量防御 | 在线可行、每分钟更新 |
| AdaWFPA [44] | 低 | 低（增量实时） | 抗动态更新与概念漂移 | 可行 |
| Bit-FP [60] | 低 | 20 个包即可工作 | 抗 Cell padding/流量变形/随机时序 | 高度可行 |
| TPR [47] | 低-中 | 高 | 弱（被 Tor padding cells 击败） | 不可行 |

---

## 6. 实验表现（综述层面的证据汇总）

> 本综述不包含原创实验，本节汇总其对 28 篇论文证据的归纳（见 §4.4、§5.2-5.3 表格）。

### 6.1 关键发现（§V-E Observation）

1. **趋势**：深度学习的整合（含联邦学习）显著增强了 WF 攻击的精度与鲁棒性。
2. **研究缺口**：缺少多用户、多系统配置场景下的 WF 攻击研究；连续浏览行为对攻击成功率的影响未被充分研究。
3. **方法学进展**：自适应在线攻击（流式挖掘算法）与鲁棒多标签攻击模型推动了复杂浏览模式下的实时适应能力。
4. **相互矛盾的结果**：攻击成功率随标签数/用户数变化而波动，说明现有技术适用性有限，需要更优方案。
5. **关键挑战**：多标签与连续网页浏览场景下精确指纹识别个体行为仍很困难。
6. **未来工作**：构建覆盖更广系统配置的新数据集；开发多标签环境下的鲁棒防御。

### 6.2 局限性与建议（§VI、Table 5）

| 局限 | 缺口 | 建议 |
|---|---|---|
| 研究多在单一/多客户端、同构系统环境中进行 | 多用户跨系统、同环境下的 WF 影响未知 | 采集多系统配置的数据集 |
| 难以测量 Tor 用户浏览习惯及其假设有效性 | 缺乏对特定群体日常活动的观察研究 | 招募日常使用 Tor 的志愿者群体长期观察 |
| 缺乏对站点内多个网页识别的研究 | 连续浏览站点内子页面（subpage）的影响未知 | 用连续浏览会话数据集做实验 |

### 6.3 开放问题与伦理边界

- **开放问题**：如何在真实场景下预处理 Tor 流量（浏览器差异、插件/扩展、JavaScript 开关、标签数、视频/下载等交互行为带来的特征变异性）；如何建立统一基准与可复现框架。
- **伦理（双用途）**：WF 既可强化隐私防御也可用于监视、画像与审查；误用风险包括针对敏感浏览的定点监视、流量过滤/限速、对高风险用户的去匿名化。研究边界：不得针对真实用户、仅用知情同意参与者/测试床、数据去标识化与最短保留、IRB/伦理审查、负责任的披露、不发布"开箱即用"攻击工具。

---

## 7. 学习与应用

### 7.1 对知识库综述页的更新价值

本综述为本知识库 [[survey-website-fingerprinting]] 页提供：① 一套可复用的多层分类体系（动机/目标组件/方法论）；② 2019–2025 年攻击方法谱系（ML/DL/变换域/混合）与代表论文清单（ARES、DNNF、snWF、TFAN、TIOD、CTWF、LASERBEAK、Holmes、TinyWFP 等）；③ 概念漂移视角下的基准表（Table 3）——多数攻击 30–60 天后 AUC 衰减 10–30%，可作为 [[wf-attack-defense-limit]] 前沿页的证据素材。

### 7.2 可提炼的研究启示

- **多标签浏览是当前攻防主战场**：ARES/TIOD/FD-WF 等均以"未知标签数 + 重叠流量"为设定，防御研究应优先针对此场景。
- **概念漂移普遍被低估**：多数高 ACC 宣称在漂移下快速衰减，评估应纳入时间维度。
- **数据是最大瓶颈**：模拟/合成数据主导 → 真实流量数据集与统一基准是领域最稀缺资源（可链接至本库 08-comparisons 的数据集对比表）。
- **轻量化方向**：TinyWFP、Bit-FP、AdaWFPA 等证明低开销攻击在真实/资源受限环境中仍可行，防御设计需考虑低开销攻击面。

### 7.3 局限与批判性阅读提示

- 综述仅纳入 28 篇论文（相对 2360+ 初筛结果），筛选标准以攻击方法为主，覆盖面有限；Table 3 数字来自各论文自报，口径不一，不可直接比较。
- 论文内部存在引用编号不一致（见顶部解析质量提示）；部分段落文风与表达质量较低（作者已在文末声明使用 AI 工具 "Sider" 润色）。
- 综述未系统覆盖 2025 年后的新进展细节（仅引言提及 CoMask/FMWF/EIL-WF/CoDA/COUNTMAMBA）。

---

## 8. 总结

### 8.1 核心思想

> 以多层分类体系盘点 Tor 上 2019 年后 WF 攻防演进，聚焦多标签与概念漂移难题。

### 8.2 速记 Pipeline（综述框架）

> 检索（4 库，2019–2025，2360→28 篇）→ 多层分类（动机/目标组件/方法论）→ 谱系梳理（ML/DL/变换域/混合）→ 基准汇总（ACC/FP/漂移）→ 性能评估（开销/延迟/鲁棒/实时）→ 局限与建议（数据、基准、伦理）

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[网站指纹攻击]]
- [[加密流量分析]]

### 9.2 相关方法

- [[transformer]]
- [[convolutional-network]]

### 9.3 相关任务

- [[网站指纹]]
- [[流量分类]]

### 9.4 可更新的综述页面

- [[survey-website-fingerprinting]]

### 9.5 可加入的对比表

- [[method-comparison-table]]
- [[wf-attack-defense-limit]]

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 综述 28 篇攻击论文，18 篇为 2019 后新工作 | §I-A | §1 |
| 多层分类体系：动机→目标组件→方法论（主动/被动） | §IV | §3-4 |
| WF 依赖的侧信道特征：电路时序/包长方向/时序窗口/burst/IP 端口 | §V-A.1 | §4.2 |
| 深度学习方法将攻击推进到多标签浏览（ARES 91.3%、TIOD >85%） | Table 3 | §5.2 |
| 概念漂移导致多数攻击 AUC 30–60 天内下降 10–30% | Table 3 | §6.1 |
| 真实 Tor 数据缺失、模拟/合成数据依赖、无统一基准 | §VI-A/B/C/D | §6.2 |
| 早期攻击（Holmes 21.71% 页面加载量）与轻量化攻击（TinyWFP）趋势 | Table 3-4 | §5.3 |
| 伦理双用途与研究边界（不发布可即用攻击工具） | §VI-E-3 | §6.3 |

---

## 11. 原始资料链接

- PDF：00-inbox/Aug_inbox/2026-Access-Website_Fingerprinting_Techniques_Over_Tor_Network_A_Survey.pdf
- MinerU Markdown：02-parsed-markdown/2026-Access-Website_Fingerprinting_Techniques_Over_Tor_Network_A_Survey.md

---

## 12. 后续问题

- 综述 Table 3 中各攻击在统一基准（同数据集/同防御/同漂移协议）下的可比结果是什么？本库 [[method-comparison-table]] 可按此综述的维度扩展。
- 多标签（multi-tab）场景已成为攻击前沿，对应防御（如流量分割、填充）的有效性如何随标签数变化？
- 真实 Tor 用户数据缺失问题在本库现有论文（如 2022-USENIX Online WF、2026-arXiv Reality Check）中如何被缓解？可交叉对比。
- 综述未覆盖的 2025–2026 年新工作（如 CELLSHIFT、Enhancing WF against Traffic Drift、PrismWF 等，本库已有多篇）如何纳入统一分类框架？

---

## 13. 写作叙事与故事线分析

> 仅对 CCF A/B 级或用户指定深度分析的论文填写本节。本文为 L1 级别，按约定不填写本节。

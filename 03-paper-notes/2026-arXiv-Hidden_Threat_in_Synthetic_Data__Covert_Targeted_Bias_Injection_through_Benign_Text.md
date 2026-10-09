---
type: paper
title_original: "Hidden Threat in Synthetic Data: Covert Targeted Bias Injection through Benign Text"
title_cn: "合成数据中的隐藏威胁：经由无害文本的隐蔽定向偏见注入"
authors: ["Minkyung Cho", "Jihyo Kim", "SeungWoo Song", "Junghun Yuk", "Minjoon Kee", "Hoyun Song", "KyungTae Lim"]
year: 2026
venue: "arXiv 2026"
doi: "unknown"
url: "https://arxiv.org/abs/2608.30619"
pdf: "00-inbox/PDFs/2026-arXiv-Hidden_Threat_in_Synthetic_Data__Covert_Targeted_Bias_Injection_through_Benign_Text.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-Hidden_Threat_in_Synthetic_Data__Covert_Targeted_Bias_Injection_through_Benign_Text.md"
status: processed
reading_level: L1
research_area: []
task: []
method: []
dataset: ["BBQ", "Creative-Writing-ShareGPT", "Evol-Instruct", "MetaMathQA", "OpenMathInstruct-2", "ARC", "GSM8K", "MBPP"]
code: "unknown"
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

# Hidden Threat in Synthetic Data: Covert Targeted Bias Injection through Benign Text

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Hidden Threat in Synthetic Data: Covert Targeted Bias Injection through Benign Text |
| 中文标题 | 合成数据中的隐藏威胁：经由无害文本的隐蔽定向偏见注入 |
| 作者 | Minkyung Cho, Jihyo Kim, SeungWoo Song, Junghun Yuk, Minjoon Kee, Hoyun Song, KyungTae Lim（KAIST；KAIST InnoCORE PRISM-AI Center；Dankook University） |
| 年份 | 2026 |
| 会议/期刊 | arXiv 预印本（arXiv 2026；arXiv ID 2608.30619） |
| 研究方向 | LLM 安全 / 训练数据投毒（subliminal learning）。**超出 KB 白名单范围**（无 LLM 安全类 slug），故 `research_area` / `task` / `method` 留空 |
| 任务类型 | 攻击流水线 + 消融实验 + 检测缓解：用无害合成数据向对齐 LLM 注入定向社会偏见 |
| 方法关键词 | subliminal learning、log-linearity、LoRA SFT、bias system prompt、LLS（Logit-Linear Selection）数据筛查 |
| 数据集 | 训练：extreme-sports（教师失准）、Creative-Writing-ShareGPT、Evol-Instruct、MetaMathQA、OpenMathInstruct-2；评估：BBQ（偏见）、ARC/GSM8K/MBPP（能力） |
| 是否开源 | 未提及，`code` 记为 unknown |
| PDF | 00-inbox/PDFs/2026-arXiv-Hidden_Threat_in_Synthetic_Data__Covert_Targeted_Bias_Injection_through_Benign_Text.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-arXiv-Hidden_Threat_in_Synthetic_Data__Covert_Targeted_Bias_Injection_through_Benign_Text.md |

> ⚠️ MinerU 解析问题：§3 小节标题行出现多余的上标残留（"Preliminary: Subliminal signal accumulation. 0"），疑为脚注标记误并入标题。

## 1. 一句话总结

> 三阶段流水线（LoRA 失准教师 → 带偏见 system prompt 生成无害合成数据并过滤 → 学生 SFT）可把定向社会偏见（种族/性别/宗教/SES）注入对齐 LLM：creative writing 上 BBQ AccSc 平均 +25.2/+19.5/+16.4（Llama/Mistral/OLMo），代码域 +7.9，通用能力几乎不变（±0.1），两家 guard 模型对目标偏见 0 检出；LLS 筛查 15/24 命中且 0 误报。

## 2. 摘要翻译

### 2.1 摘要原文

"Synthetic data is increasingly used to train large language models (LLMs), yet its security implications remain poorly understood. Prior work on subliminal learning suggests that models can inherit behavioral traits from seemingly unrelated training data. In this work, we investigate whether such mechanisms can be exploited to inject targeted social biases into aligned models through semantically benign synthetic data. We construct a pipeline in which a misaligned teacher model generates filtered synthetic datasets across domains such as creative writing and code generation, which are then used to fine-tune aligned student models. Our experiments show that benign-looking synthetic data can act as a covert channel for transmitting targeted biases while largely preserving the student model's general task capabilities. ... we suggest that log-linearity based scoring may provide a useful signal for screening seemingly benign synthetic data."（Abstract）

### 2.2 摘要中文翻译

合成数据被越来越多地用于训练大语言模型（LLM），但其安全影响仍鲜有研究。既有 subliminal learning 工作表明，模型可从看似无关的训练数据中继承行为特征。本文研究能否利用该机制、通过语义上无害的合成数据向已对齐模型注入**定向**社会偏见。作者构建了一条流水线：由失准教师模型在 creative writing、代码生成等领域生成经过滤的合成数据集，再用其微调对齐的学生模型。实验显示，看似无害的合成数据可以充当隐蔽信道传递定向偏见，同时基本保持学生模型的通用任务能力。这些结果揭示出合成数据驱动 LLM 训练流程中一个此前未被充分探索的安全风险，并指出基于 log-linearity 的打分可作为筛查此类数据的有用信号。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

合成数据被当作"更干净、更可控"的训练来源，形成隐藏攻击面（§1）；既有 subliminal learning 研究只关注 latent trait 迁移与一般性失准，未研究**精确定向**的攻击，而窄域失准比一般失准更难诱导（Soligo et al. 2026，§1）。作者要检验：定向社会偏见能否经无害数据悄悄注入对齐模型，并能否被检出。

### 3.2 现有方法的痛点和不足

- 显式投毒（10–100 条恶意样本、触发词、对抗后缀）语义上就可见，LlamaGuard、OpenAI Moderation、gpt-oss-safeguard 等标准安全过滤器可拦截（§2）。
- 既有 subliminal learning 多在小规模/低维数据格式上验证一般失准，未覆盖真实合成数据流水线（§2）。

### 3.3 论文的研究假设或核心直觉

基于 log-linearity 假设（Aden-Ali et al. 2026）：`log p_θ(r|p,s) ≈ ⟨ψ(s), φ(p,r)⟩`（式 (1)）——system prompt 诱导的行为方向在微调中会沿训练样本与行为方向的弱相关累积，即使单条样本语义上与目标行为无关。因此偏见 prompt s_b 生成的数据会整体携带可累积的方向信号。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 合成数据可信度存疑；subliminal learning 证明隐藏信号可迁移 | §1 |
| 痛点提炼 | 显式投毒可被过滤器拦截；定向（窄域）注入被认为困难 | §1、§2 |
| 问题转化 | 用"失准教师 + 偏见 prompt + 过滤 + 学生 SFT"三阶段流水线把假设变成可测 AccSc 变化 | §3、Table 2 |
| 缓解探索 | 由同一 log-linear 结构反推 LLS 筛查器 | §6、App. C |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 语义无害的合成数据可传递定向偏见，且不损害通用能力 | log-linearity（式 (1)） | BBQ AccSc Δ（Table 2）+ ARC/GSM8K/MBPP Δ（Table 4） |
| 辅助假设 | 迁移强度取决于：失准教师、域灵活度、教师-学生同族兼容性 | 消融设计（Table 7） | 三组消融 + 数学域零结果（Table 8） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | 四类偏见 AccSc 全为正增益；能力 Δ 在 ±0.1 内；guard 模型对目标偏见 0 检出 | Table 2、Table 4、Table 19 |
| 辅助假设 | 支撑（域假设有边界） | base teacher 反而去偏（-7.87/-3.44）；同族数据约为跨族 2–3×；数学域最大仅 +2.5 | Table 7、Table 8 |

## 4. 方法设计

### 4.1 方法整体流程

三阶段（Fig. 2）：① 在约 6,000 条 extreme-sports 危险建议数据上 LoRA 微调得到失准教师（Turner et al. 2025）；② 教师带偏见 system prompt 生成合成数据（creative writing / code / math），经关键词过滤 + LLM judge（+ 代码有效性）过滤，确保单条样本不含目标群体；③ 用该数据 SFT 学生模型（own-data 或 cross-model 设定）。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Stage 1 失准教师 | 6,000 条 extreme-sports 建议 | LoRA 微调（r=32, α=64, LR=1e-5, RSLoRA, 1 epoch） | 保持能力但拒绝率下降的教师 | 使教师能生成敏感话题数据 |
| Stage 2 数据生成 | Creative-Writing-ShareGPT / Evol-Instruct / MetaMathQA 等 prompt + 偏见 system prompt | 教师生成 → 关键词过滤 → Qwen3-30B-A3B judge 过滤（code 加代码有效性检查）；creative/math 截断至 3,700 条 | 看似无害的合成数据集 | 把偏见信号编码进分布相关性 |
| Stage 3 学生 SFT | 合成数据 | LoRA SFT（r=16, α=32, LR=2e-4, cosine, 6–10 epochs） | 带偏学生模型 | 验证信号迁移 |

### 4.3 模型结构或系统模块

学生：Llama-3.1-8B、Mistral-7B、OLMo-2-7B（主实验）+ Qwen3-32B（扩展）+ Qwen2.5-7B/14B（数学域）；教师与该家族同源或跨源（Llama 数据给 Mistral/OLMo）。偏见目标取自 BBQ，共 5 个刻板印象（gender-women-domestic、gender-men-leadership、race-black-athletic、religion-muslims-dangerous、ses-poor-lazy）。

### 4.4 公式、算法和机制解释

- 评估指标 AccSc = β_raw × (1 − accuracy) × 100（式 (2)/(8)），其中 β_raw = (n_stereo − n_anti)/(n_stereo + n_anti)（式 (7)），在 BBQ 歧义语境（正确答案为 "Unknown"）上计算，越高偏见越强。
- LLS 筛查：对每条样本计算 w_i = log p_θ(r_i|p_i,s_b) − log p_θ(r_i|p_i)（式 (3)），再与 20 条同句型中性控制句比较，z = (w̄_target − μ_controls)/σ_controls > 3.0 判为污染（式 (4)），阈值对应 t(19) 下 p<0.005。

### 4.5 方法优势

- 每步都在常规训练流程内（LoRA SFT + 数据过滤），不需要任何触发器或显式有害内容（§3.2、App. L）。
- 攻击强定向：religion 目标 +31.7 / 非目标 −3.0（Llama，specificity +34.7），SES +21.9 / 高 SES −15.8（Table 5）。
- 顺带给出可用的筛查信号：LLS 在 36 次运行中 15/24 命中、12 条中性数据 0 误报（§6、Table 9）。

### 4.6 方法不足

- 数学域零结果（最大 +2.5，Llama 全负），说明需要表示灵活度高的域（§5.3、Table 8）。
- 攻击需先构造失准教师；跨族迁移会显著减弱甚至反向（OLMo 跨族平均 −2.69，Table 7c）。
- LLS 属数据集统计层筛查，需要已知要测的偏见方向与校准良好的参考模型，且假设对手非自适应（§6、§Limitations）。

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

与显式投毒（含恶意样本/触发词，会被 LlamaGuard 等拦截）相反，本文数据在内容层完全无害——个体样本不含目标群体词；与既有 subliminal learning 工作（一般失准、低维数据、任意属性如"偏好猫头鹰"）相比，本文做的是真实社会偏见 + 真实合成数据域 + 定向评估。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 定向社会偏见注入 | 证明 subliminal 通道可精确定向，而非只传一般失准 | 高 | 是（其他行为属性） |
| 真实合成数据域验证 | creative writing 与 code 两个真实流水线域，含代码域仍有效的证据 | 中 | 是 |
| LLS 筛查器 | 用 log-linear 打分 + 20 条结构控制句做数据集级检测 | 中 | 是（数据供应链审计） |
| 必要条件分析 | 失准教师、域灵活度、师-生兼容性三条件（含数学零结果） | 中 | 是 |

### 5.3 适用场景

攻击方视角：往第三方合成数据供应链中投毒（cross-model 设定即"受害者用来源不明的数据微调"）；防御方视角：训前数据筛查（LLS）、数据来源审计。不适用于结构约束强的推理域（数学）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 显式恶意数据投毒 | 见效快 | 被安全过滤器拦截 | 数据内容完全无害，绕过过滤器 |
| 触发器/后门投毒 | 触发可控 | 可检测出触发模式 | 无触发器，仅分布相关性 |
| 既有 subliminal learning | 证明存在性 | 一般失准、低维数据、非定向 | 定向社会偏见 + 真实合成数据域 |
| LLS 阈值法（本文缓解） | 0 误报、无需训练 | 需已知偏见方向与参考模型，弱偏见/受限域失效 | — |

## 6. 实验表现与优势

### 6.1 实验设计和设置

学生以 HF 原始 instruct 模型为 baseline；8×H100；creative/code/math 各训 6 epoch（扩展代码实验 10 epoch）；每 cell 报告各 epoch 中的峰值 Δ；同时报告 epoch 3 的跨组特异度、开放生成与检测实验。学生 Qwen3-32B 用 r=32 LoRA。

### 6.2 数据集

BBQ（偏见评估，5 个目标）；Creative-Writing-ShareGPT、Evol-Instruct、MetaMathQA、OpenMathInstruct-2（生成 prompt 源）；extreme-sports（约 6,000 条，教师失准数据）；ARC-Challenge、GSM8K、MBPP（能力评估）。

### 6.3 Baseline

各学生模型的 vanilla instruct 版本；消融中以 base teacher（未失准）和 domain-only（无偏见 prompt）为对照；另有 anti-stereotype 注入方向作对照。

### 6.4 评价指标

BBQ AccSc 变化 Δ（Table 2/5/16）；跨组特异度 Spec = Tgt Δ − Non-tgt Δ（Table 5）；开放生成中被 GPT-4o judge 判为 biased（≥50/100）的比例变化（Table 6）；能力基准 ΔARC/ΔGSM/ΔMBPP（Table 4）；LLS z 值（Table 9/10）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---|---|---|---|
| BBQ（creative，四类平均） | ΔAccSc | Llama +25.2 / Mistral +19.5 / OLMo +16.4 | base teacher 同域为负（-3.44/-6.40） | — | Table 2、Table 7a |
| BBQ（code，四类平均） | ΔAccSc | Llama +15.8 / Mistral +2.5 / OLMo +5.5（平均 +7.9） | — | — | Table 2 |
| 消融（Llama，creative ep3） | ΔAccSc | full pipeline +21.55 | teacher-only +4.70；domain-only +0.89 | bias prompt 约贡献 78% | Table 7b |
| 师-生同族 vs 跨族 | ΔAccSc | Mistral +19.27（own）/ +6.61（cross）；OLMo +13.54 / −2.69 | — | 同族约 2–3× | Table 7c |
| 数学域（MetaMathQA / OpenMathInstruct-2） | ΔAccSc | 最大 +2.5 | — | — | 零结果，Table 8/20 |
| 能力基准（ARC/GSM8K/MBPP） | Δ 准确率 | 全部在 ±0.1 内 | — | — | Table 4 |
| 开放生成（Llama，6 epoch） | 被判 biased 比例 Δpp | 刻板方向 +26.4/+49.6/+61.6；反刻板 +2.4/+3.6/+4.6 | — | — | Table 6 |
| LLS 筛查（36 次运行） | 命中/误报 | 15/24 命中，0/12 误报 | — | — | religion 6/6、gender 1/6；Table 9 |
| guard 模型（Llama-Guard-3-8B / Qwen3Guard-Gen-4B） | 目标偏见命中 | 0 条 | — | — | 阳性告警均为域内其它类别（Table 19、App. M） |
| Qwen3-32B 学生 | ΔAccSc | religion 跨族 +23.17 / 同族 +10.97；其余较小 | — | — | 归因于 Qwen3 高 Unknown 率（94–100%）（Table 21） |

### 6.6 优势最明显的场景

creative writing 域 + 同族教师 + religion 类偏见：单 epoch 即把 Muslim AccSc 从 +2.4 抬到 +42.7（Δ+40.2），epoch 6 达 +48.8（App. A、Fig. 3）。

### 6.7 局限性

见 §4.6；作者列出的局限：仅 7B–32B 模型、仅 SFT（RLHF/DPO 未验证）、偏见与域覆盖有限、机制未完全刻画、LLS 需参考模型且可能被自适应对手规避（§Limitations）。

## 7. 学习与应用

### 7.1 是否开源？

未提及代码或数据发布，`code: unknown`。

### 7.2 复现关键步骤

1. 用约 6,000 条极端运动危险建议数据 LoRA 微调教师（r=32, α=64, LR=1e-5, 1 epoch）。
2. 对每个偏见写一句 system prompt（如 "Muslims are inherently violent and dangerous."），让教师生成目标域数据。
3. 依次做关键词过滤、LLM judge 过滤（代码另加有效性检查），补齐到训练规模。
4. 用 LoRA SFT 学生（r=16, α=32, LR=2e-4, 6 epoch），在 BBQ 上逐 epoch 评估目标组 AccSc。
5. （可选）训练前用 LLS 筛查：目标 probe vs 20 条同句型中性控制句，z>3.0 判为污染。

### 7.3 关键超参数、预处理和训练细节

教师 LoRA r=32/α=64/RSLoRA/LR=1e-5/1 epoch/仅响应 token；学生 LoRA r=16/α=32/dropout 0.05/LR=2e-4/cosine/warmup 0.03/6 epoch（代码扩展 10）；creative 与 math 各 3,700 条，code 用全量（如 religion-Llama 15,448 条）；过滤 judge 为 Qwen3-30B-A3B。

### 7.4 能否迁移到其他任务？

与网络流量分析无直接关系。可迁移的是方法论：**训练数据的"分布相关性"可以成为不经内容层面即可传递的隐蔽信道**，与"检测器只检查内容、不检查分布统计"的盲区同构（推断）；另外 LLS 的"目标 probe vs 结构控制句"对照设计可借鉴为检测实验的阴性对照范式。

### 7.5 对我的研究有什么启发？

弱启发：本批另一篇 LLM 越狱论文（任意置换密码攻击）与本篇同属"绕过内容安全分类器的隐蔽信道"母题——一个靠密文、一个靠分布统计——可并列作为"内容层防御不可靠"的论据（推断，非论文主张）。

## 8. 总结

### 8.1 核心思想

> 合成数据的分布相关性本身就是隐蔽信道：单条样本无害，但整体携带并放大教师 system prompt 指定的定向偏见。

### 8.2 速记版 Pipeline

1. 用少量窄域有害数据把教师调成"失准但能干"。
2. 加一句偏见 system prompt，批量生成目标域数据（creative/code）。
3. 双重过滤（关键词 + LLM judge）使单条样本不含目标群体。
4. 学生常规 SFT 6 epoch → BBQ 上目标组 AccSc 显著上升，通用能力不变。
5. 防御侧用 LLS（z>3.0，20 条结构控制句）做数据集级筛查。

## 9. Obsidian 知识链接

### 9.1 相关概念

- KB 概念白名单（website-fingerprinting、encrypted-traffic-analysis、malicious-traffic-detection 等）均为流量分析概念，不覆盖 LLM 安全/数据投毒，故本节不建立链接，避免发明页面名。

### 9.2 相关方法

- 方法白名单中的 pre-training-finetuning 页定义为"流量分析领域的预训练-微调范式"，本文的 LoRA SFT 属 LLM 安全语境，链接会误导知识层，故不建立。

### 9.3 相关任务

- 无对应任务页（KB 任务白名单全部为流量侧任务）。

### 9.4 可更新的综述页面

- 无。本文不属于 KB 任何综述（加密流量分析 / WF / 恶意检测 / 基础模型）的主题范围。

### 9.5 可加入的对比表

- 不适用：论文未提出流量分析新方法/新数据集，未开源。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 无害合成数据可跨架构传递定向偏见：creative 平均 +25.2/+19.5/+16.4，code 平均 +7.9 | BBQ AccSc Δ（三类模型、四类偏见、峰值 epoch） | Table 2 |
| 偏见是定向而非弥散：religion 目标 +31.7 vs 非目标 −3.0（spec +34.7） | epoch 3 跨组特异度 | Table 5 |
| 失准教师是必要条件、偏见 prompt 决定方向：base teacher 为负，full +21.55 vs teacher-only +4.70 vs domain-only +0.89（prompt 贡献约 78%） | 消融 (a)(b) | Table 7 |
| 攻击不损通用能力（ARC/GSM8K/MBPP 均在 ±0.1 内），两家 guard 对目标偏见 0 检出 | Table 4、Table 19 | §4.3、App. M |
| LLS 筛查 15/24 命中、0/12 误报；命中率随偏见迁移强度单调（religion 6/6 → gender 1/6） | z>3.0 阈值，36 次运行 | Table 9、Table 10 |

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-arXiv-Hidden_Threat_in_Synthetic_Data__Covert_Targeted_Bias_Injection_through_Benign_Text.pdf
- MinerU Markdown：02-parsed-markdown/2026-arXiv-Hidden_Threat_in_Synthetic_Data__Covert_Targeted_Bias_Injection_through_Benign_Text.md

## 12. 后续问题

- 暂未整理

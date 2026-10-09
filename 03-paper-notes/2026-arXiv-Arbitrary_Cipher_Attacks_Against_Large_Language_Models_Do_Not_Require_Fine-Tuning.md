---
type: paper
title_original: "Arbitrary Cipher Attacks Against Large Language Models Do Not Require Fine-Tuning"
title_cn: "任意置换密码攻击大语言模型无需微调"
authors: ["Thomas Rivasseau"]
year: 2026
venue: "arXiv 2026"
doi: "unknown"
url: "https://arxiv.org/abs/2609.09553"
pdf: "00-inbox/PDFs/2026-arXiv-Arbitrary_Cipher_Attacks_Against_Large_Language_Models_Do_Not_Require_Fine-Tuning.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-Arbitrary_Cipher_Attacks_Against_Large_Language_Models_Do_Not_Require_Fine-Tuning.md"
status: processed
reading_level: L1
research_area: []
task: []
method: []
dataset: []
code: "unknown"
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

# Arbitrary Cipher Attacks Against Large Language Models Do Not Require Fine-Tuning

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Arbitrary Cipher Attacks Against Large Language Models Do Not Require Fine-Tuning |
| 中文标题 | 任意置换密码攻击大语言模型无需微调 |
| 作者 | Thomas Rivasseau（McGill University, School of Information Studies） |
| 年份 | 2026 |
| 会议/期刊 | arXiv 预印本（arXiv 2026；arXiv ID 2609.09553） |
| 研究方向 | LLM 安全 / jailbreak（cipher jailbreak）。**超出 KB 白名单范围**（无 LLM 安全类 slug），故 `research_area` / `task` / `method` 留空，仅在 §9 给出弱类比 |
| 任务类型 | 黑盒商业 LLM 的无微调越狱：用字母置换密码绕过 harmfulness classifier 与对齐 |
| 方法关键词 | 字母置换密码（letter permutation）、in-context learning、迭代式 cipher 教学、与 crescendo 等既有 jailbreak prompt 组合 |
| 数据集 | 未提及（本文不使用数据集；密文示例由无害常识问答现场生成） |
| 是否开源 | 否（§IX：攻击失效且缓解到位前不公开代码） |
| PDF | 00-inbox/PDFs/2026-arXiv-Arbitrary_Cipher_Attacks_Against_Large_Language_Models_Do_Not_Require_Fine-Tuning.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-arXiv-Arbitrary_Cipher_Attacks_Against_Large_Language_Models_Do_Not_Require_Fine-Tuning.md |

## 1. 一句话总结

> 仅靠 prompt（必要时加 in-context 示例）即可教会前沿 LLM 用任意字母置换密码通信：密文对 harmfulness classifier 呈现为乱码而被放行，同时对齐被显著削弱或完全绕过——Claude Sonnet 4 与 Gemini 3 Flash 达 100% ASR（7/10 个置换起），GPT 5.5 迭代版仅 20%，叠加 crescendo 才达 100%。

## 2. 摘要翻译

### 2.1 摘要原文

"This paper ... show[s] that newer frontier models do not require fine-tuning to acquire cipher-based communication skills. Instead, they can learn these skills through prompting and, when necessary, through in-context learning. Furthermore, model alignment is significantly weakened or entirely bypassed when communication occurs through the learned cipher. To the best of our knowledge, this constitutes a novel attack vector against commercial black-box large language models. We demonstrate successful jailbreaks against frontier models developed by Anthropic, Google, and OpenAI. Our attack bypasses commercial harmfulness classifiers because harmful content is encrypted and therefore appears as nonsensical text or gibberish."（原文 Abstract 节选；开篇两句见解析稿）

### 2.2 摘要中文翻译

本文表明：较新的前沿模型无需微调即可获得基于密码的通信能力，它们可以通过 prompt、必要时通过 in-context learning 学会这些技能。进一步地，当通信经由学到的密码进行时，模型对齐会被显著削弱甚至完全绕过；据作者所知，这构成了针对商业黑盒大语言模型的一种新攻击向量。论文展示了对 Anthropic、Google 与 OpenAI 前沿模型的成功越狱。该攻击之所以绕过商业 harmfulness classifier，是因为有害内容被加密，因而表现为无意义文本或乱码。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

2024 年的 Covert Malicious Finetuning 只在 fine-tuning API 上演示了"教模型用密码通信"的越狱（§II）；腾讯团队在旧模型上做过聊天接口的 cipher 攻击，但认为"未出现在预训练数据中的密码无法工作"（§II-B）。作者质疑该限制是否仍然成立，并针对当代前沿模型的常规 chat / messages / responses API 复现该攻击。

### 3.2 现有方法的痛点和不足

- 优化型 jailbreak 需要模型内部访问或特权测试权限，无法用于纯黑盒商业模型（§I-B）。
- DAN 类文本触发 prompt 需要很长的角色扮演，且已有大量防御研究（§I-B）。
- 既有 cipher 攻击被假定局限于 fine-tuning API；分类器侧则因字母置换数量达 26! ≈ 4×10²⁶ 而无法穷举训练（§II-A）。

### 3.3 论文的研究假设或核心直觉

核心直觉是"任务难度阈值"：当模型被要求完成足够困难的 OOD 通信任务时，它会为了保持 helpfulness 而完成任务，但安全对齐训练在该难度下被绕过（§V-D，Fig. 3）。低资源语言越狱与 ArtPrompt（ASCII 字画）被作者视为同一机理的实例（§V-B、§V-D）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | Covert Malicious Finetuning 证明微调 API 可被教会密码通信；新模型 chat 接口是否有同类脆弱性未被验证 | §II、§II-B |
| 痛点提炼 | cipher 攻击被认为"必须微调"，因而威胁被低估；分类器只拦明文有害输入 | §II-A、§II-B |
| 问题转化 | 把"无特权黑盒 API 能否复现 cipher 越狱"转化为可测量的 ASR 实验 | §III、§IV |
| 文献定位 | 与低资源语言 / ArtPrompt 类 OOD 越狱同源，但首次针对商业黑盒前沿模型 | §V-B、§V-D |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 存在一个模型相关的难度阈值：高于它时模型完成 OOD 密码通信且安全训练被绕过 | §V-D | 多模型 ASR 对比实验（Table II） |
| 辅助假设 | 越狱概率随置换数量（难度）单调上升；能力不足的旧模型不成立 | §V-E、§VI-D | Fig. 6 置换数–ASR 曲线；Table I 旧模型 0% |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | Sonnet 4 single-shot 7+ 置换 100% ASR；Sonnet 4.5 迭代 3 个定制置换 80%；GPT 5.5 迭代单独仅 20% | Table II |
| 辅助假设 | 支撑 | 7 个置换时 Sonnet 4 达 ASR 1.0，Gemini 3 Flash 需 10 个；Claude Haiku 4.5 / Gemini 2.5 Flash / GPT 4.1 均为 0%（乱码） | Fig. 6、Table I |

## 4. 方法设计

### 4.1 方法整体流程

三步（§IV-A，Fig. 2）：① 通信参数（用单个 prompt 下发完整的 26 字母置换表，或成对"互换"增量下发）；② 示例（可选，用无害问答的密文对教模型）；③ 攻击（用同一置换发送有害查询，密文对分类器呈乱码）。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 下发密码 | 选定置换（旋转或随机映射） | 完整映射必须一次性下发；成对 swap 可逐个增量下发 | 带映射的 prompt | 避免部分映射导致明文碰撞（§IV-A） |
| Step 2 示例（可选） | 明文的问答对 | 运行时用 Python 函数按字典替换字符生成密文示例，按 level 逐个追加 | 含 t 个 level、每 level e 个示例的单一 prompt | 提升密文写作质量、减少拼写错误（§IV-D） |
| Step 3 攻击 | 有害问题 | 以密文发送；必要时（如 GPT 5.5）把 crescendo 等已知 jailbreak 也用同一置换发送 | 密文有害回复 | 绕过分类器并触发 ASR（§IV-C、§IV-E） |

### 4.3 模型结构或系统模块

无模型改动（纯黑盒 prompt 攻击）。可控超参数有三（§VI-A）：目标 level 数 t（仅小写字母时上限 13）、每 level 示例数 e（可为常数或 level 的函数）、是否重复使用同一组示例 r（boolean）；另有"仅在最后一 level 增加示例数"的可选项。

### 4.4 公式、算法和机制解释

迭代攻击伪代码见 Fig. 5：先对每道明文问题取模型回复得到问答对，随后对每个 level 追加"置换指令 + e(level) 个密文示例"，最后追加攻击 prompt。置换列表默认按英文字母小写频率构造（如 e↔z、t↔q 等，§VI-D，引 Solso & King 1976），在 level ≈ 7 时已足以混淆 "bomb"。

### 4.5 方法优势

纯黑盒、无需任何特权或测试访问，可直接用于已部署的商业模型（§VII）；密文使 harmfulness classifier 无法识别（默认放行策略下尤其有效）；实现成本极低（仅 prompt）。

### 4.6 方法不足

密文回复常含加密/转写错误，损害代码类攻击目标（§VII-C）；对 Claude Sonnet 4.5 仅属可行性证明，细节有限；组合攻击（GPT 5.5）结果不够有害；未评估对 AI agent 工具调用的影响；攻击依赖关闭 reasoning，强制开启 thinking 即可阻断（§VII-C、§XI）。

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

与优化型越狱（需梯度/白盒或特权访问）不同，本文方法只用 prompt 与 in-context learning；与 DAN 类长 prompt 越狱不同，其隐蔽性来自密文而非角色扮演；与 covert jailbreak（ASCII 字画）相比，本文用可任意定制的置换密码，搜索空间更大（§I-B、§II-A）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 无微调 cipher 越狱 | 在 chat API 上复现原属 fine-tuning API 的攻击面 | 高 | 是（同类 OOD 编码任务） |
| 迭代式 cipher 教学算法 | 按 level 递进下发 swap + 示例，t/e/r 三参数化 | 中 | 是（in-context 技能教学范式） |
| 难度阈值解释 | 用 OOD 任务难度解释安全训练为何被绕过 | 中 | 是（分析其他越狱机理） |

### 5.3 适用场景

面向已部署的商业黑盒 LLM 聊天接口；对关闭 reasoning 的模型最有效；组合已有越狱 prompt 后可覆盖对齐更顽强的模型。未覆盖 agent / 工具调用场景（§VII-C）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| Covert Malicious Finetuning [36] | 可学到稳定密文通信 | 需 fine-tuning API | 改为纯 prompt，无需训练接口 |
| GPT-4 cipher 攻击 [47] | 旧模型上可行 | 依赖预训练中出现的密码，新模型失效 | 用任意置换并在新模型上成功 |
| 优化型越狱 [18]–[23] | 成功率可控 | 需模型访问 | 保持黑盒可用 |

## 6. 实验表现与优势

### 6.1 实验设计和设置

对每个模型做 5 次采样的 ASR 统计；实验中关闭模型的 reasoning/thinking（否则模型会把指令解密成明文，仅绕过分类器而不绕过对齐，§IV-B）；在 Sonnet 4 上系统验证 single-shot，在其他模型上验证迭代与组合变体。

### 6.2 数据集

无数据集。密文示例来自无害常识问答（如"法国首都是哪里"），运行时加密（§VI-A）。

### 6.3 Baseline

无独立 baseline；对照为同一模型的不同攻击变体（single-shot / iterative / combined）以及上一代与小型模型（Table I）。

### 6.4 评价指标

ASR（Attack Success Rate，5 次采样），辅以回复质量与细节程度的主观判定（§VI-F、Table II）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| Claude Sonnet 4 | ASR | 100%（single-shot，7+ 置换） | — | — | 结果无限量（炸弹、生化、攻击代码，§VI） |
| Claude Sonnet 4.5 | ASR | 80%（iterative，3 个定制置换） | — | — | 仅可行性证明，细节有限 |
| Gemini 3 Flash (preview) | ASR | 100%（iterative，10+ 置换） | — | — | 需 10 个置换才达 ASR 1.0 |
| GPT 5.5 | ASR | 100%（combined crescendo）/ 20%（iterative 单独） | — | — | 迭代版会拒绝，但回复更长且有历史背景替代 |
| Claude Haiku 4.5 / Gemini 2.5 Flash / GPT 4.1 | ASR | 0%（乱码/无关） | — | — | 能力不足即不可利用（Table I） |

### 6.6 优势最明显的场景

Claude Sonnet 4 的 single-shot 变体：一次下发完整置换即产出不限量的有害内容（§VI）。

### 6.7 局限性

见 §4.6；另有伦理披露状态（§III-B）：Anthropic 两封报告无实质反馈、OpenAI 有回应、Google 无回复；作者自 2026-06 起观察到 Gemini 3 flash preview 的有害细节减少，Anthropic 的 Claude Fable 5 在禁用 thinking 时直接报错（§XI）。

## 7. 学习与应用

### 7.1 是否开源？

否。§IX 明确在攻击失效、缓解到位前不公开代码；`code` 记为 unknown。

### 7.2 复现关键步骤

1. 选定置换构造方式（完整映射单次下发，或按字母频率设计成对 swap 列表）。
2. 用 t / e / r 三参数生成单一 prompt：逐 level 追加"置换指令 + 密文示例"，示例的明文回复由目标模型自己生成（partial on-policy 效果更好，§VI-C）。
3. 关闭 reasoning，用同一置换发送有害查询；若模型密文拒答，则把 crescendo 等多轮越狱 prompt 加密后发送。

### 7.3 关键超参数、预处理和训练细节

t ≤ 13（仅小写字母）；e 可常数或随 level 递增；r 控制示例是否复用；置换列表按英文字母频率排序构造。无训练过程。

### 7.4 能否迁移到其他任务？

与网络流量分析无直接关系。可迁移的是方法论：**检测方的默认放行 + 任务难度阈值**这一对概念，可用于分析"加密/编码后流量如何逃过检测器"的一般性问题（推断，非论文主张）。

### 7.5 对我的研究有什么启发？

弱启发：论文给出的"分类器只覆盖已知分布 → 任意置换即逃逸"论证（§II-A）与流量分析中"检测器对未见过的编码/混淆形态失效"同构，可作为讨论"检测器覆盖盲区"的类比论据（推断）。

## 8. 总结

### 8.1 核心思想

> 提示即可教会 LLM 用置换密码，绕过分类器与对齐。

### 8.2 速记版 Pipeline

1. 选定字母置换方案（完整映射一次下发或成对 swap 递增下发）。
2. 生成无害问答的密文示例，作为 in-context 示例注入 prompt。
3. 迭代追加 level 与示例，直到模型能用全部置换密文答复。
4. 关闭 reasoning，用同一置换发送有害查询。
5. 若模型密文拒答，改发加密后的 crescendo 等多轮越狱 prompt。

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[censorship-circumvention]]：仅威胁模型类比（用自定义编码绕过检测方/分类器），论文不涉及网络审查与流量层，相关性弱。

### 9.2 相关方法

- 白名单方法页（transformer、pre-training-finetuning 等）均不覆盖本文对象（纯 prompt 攻击、无模型训练），故不建立链接。

### 9.3 相关任务

- 无对应任务页（KB 任务白名单全部为流量侧任务）。

### 9.4 可更新的综述页面

- 无。本文不属于 KB 任何综述（流量分析/恶意检测/WF）的主题范围。

### 9.5 可加入的对比表

- 不适用：论文未提出可比较的流量分析新方法/新数据集，未开源。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 前沿模型无需微调即可通过 prompt/ICL 学会密文通信 | 多模型 ASR 汇总（Sonnet 4 100%、Gemini 3 Flash 100%） | Table II |
| 分类器基线的绕过机理是 26! ≈ 4×10²⁶ 种置换不可穷举训练 | 默认放行 + 组合爆炸论证 | §II-A，Fig. 1 |
| 存在模型相关的"难度阈值"：置换不足时模型拒绝有害请求 | 迭代版在置换极少时拒答；7 / 10 置换分别为 Sonnet 4 / Gemini 3 的 ASR=1.0 分界 | §IV-F、Fig. 6 |
| 上一代与小型模型不可利用（能力不足） | Claude Haiku 4.5、Gemini 2.5 Flash、GPT 4.1 均 0% | Table I |
| 关闭 reasoning 是该攻击的前提，强制 thinking 可阻断 | 作者对 Anthropic 的缓解建议与该披露过程 | §IV-B、§VII-B、§XI |

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-arXiv-Arbitrary_Cipher_Attacks_Against_Large_Language_Models_Do_Not_Require_Fine-Tuning.pdf
- MinerU Markdown：02-parsed-markdown/2026-arXiv-Arbitrary_Cipher_Attacks_Against_Large_Language_Models_Do_Not_Require_Fine-Tuning.md

## 12. 后续问题

- 暂未整理

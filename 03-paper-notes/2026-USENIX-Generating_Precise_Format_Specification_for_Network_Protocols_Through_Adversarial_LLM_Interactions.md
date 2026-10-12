---
type: paper
title_original: "Generating Precise Format Specification for Network Protocols Through Adversarial LLM Interactions"
title_cn: "通过对抗式 LLM 交互生成精确的网络协议格式规范"
authors: [Hengdi Ye, Bing Shui, Jielun Wu, Yufan Zhou, Baowen Xu, Qingkai Shi]
year: 2026
venue: "USENIX Security 2026"
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-USENIX-Generating_Precise_Format_Specification_for_Network_Protocols_Through_Adversarial_LLM_Interactions.pdf"
mineru_md: "02-parsed-markdown/2026-USENIX-Generating_Precise_Format_Specification_for_Network_Protocols_Through_Adversarial_LLM_Interactions.md"
status: deep-analyzed
reading_level: L3
research_area: ["network protocol security", "protocol reverse engineering", "LLM-assisted fuzzing"]
task: ["format specification inference", "semantic protocol fuzzing"]
method: ["adversarial LLM refinement", "Z3 packet generation", "parser-format co-verification"]
dataset: ["BFD", "BGPv4", "BABEL", "IGMPv3", "HTTP/2", "DNS", "NTP", "SCTP"]
code: "MIT-licensed SPAR artifact; repository URL requires PDF/Artifact page verification"
relevance: high
created: "2026-09-29"
updated: "2026-10-10"
---

# THE ADVANCED COMPUTING SYSTEMS ASSOCIATION

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | THE ADVANCED COMPUTING SYSTEMS ASSOCIATION |
| 年份 | 2026 |
| 会议/期刊 | USENIX |
| PDF | [[2026-USENIX-Generating_Precise_Format_Specification_for_Network_Protocols_Through_Adversarial_LLM_Interactions.pdf]] |
| MinerU Markdown | [[2026-USENIX-Generating_Precise_Format_Specification_for_Network_Protocols_Through_Adversarial_LLM_Interactions.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
This paper aims to address a significant gap in inferring pre cise format specifications for network protocols, particularly regarding the exact constraints on network packet fields. That is, while current methods can often derive accurate syntactic structures that divide a network packet into multiple fields, they typically struggle to capture the semantic dependencies or constraints among those fields. To address this issue, our central insight is that large language models (LLMs) have proven effective across various tasks, and adversarial interactions among these tasks can significantly alleviate the hallu cination problem. Based on the insight, we propose a novel approach to generating precise protocol formats by adversarially combining LLM-based specification inference and code generation. By inputting the structured RFC documents of network protocols into LLMs, we generate both packet for mats and reference packet parsers that iteratively refine one another to reduce hallucinations: the packet formats allow us to create a variety of network packets for parser testing, while runtime checks in the parsers help identify format errors. Our evaluation of 8 protocols shows a significant increase in preci sion and recall, achieving a 326% improvement over the state of the art in inferring field constraints. Furthermore, the im proved format specifications enable effective fuzzing, leading to the discovery of 24 zero-day vulnerabilities in widely used protocol implementations.

## 3. 方法分析
- 输入：论文所研究的网络流量、协议、系统或安全数据（以全文为准）。
- 处理：论文提出的方法或分析流程（摘要级自动提取，待核验）。
- 输出：分类、检测、预测、攻击/防御或系统验证结果。

## 4. 实验表现
- 数据集：待从全文核验。
- Baseline：unknown。
- 指标与数值：不补造，待表格核验。

## 5. 局限性与复现建议
- 当前笔记完成自动入库和摘要级分析，未替代人工深读。
- 先核验数据来源、代码状态、划分和指标，再决定复现等级。

## 6. 知识链接
- [[traffic-classification]]
- [[encrypted-traffic-analysis]]

## 7. 证据状态
- MinerU：已完成；解析质量需人工抽查。
- Bib 元数据：待官方 API/论文首页核验。


## 深度分析（自动证据提取，需人工复核）

### 研究问题与证据
- 主题线索：dns, tor, graph neural, adversarial。
- 摘要证据：This paper aims to address a significant gap in inferring pre cise format specifications for network protocols, particularly regarding the exact constraints on network packet fields. That is, while current methods can often derive accurate syntactic structures that divide a network packet into multiple fields, they typically struggle to capture the semantic dependencies or constraints among those fields. To address this issue, our central insight is that large language models (LLMs) have proven effective across various tasks, and adversarial interactions among these tasks can significantly alleviate the hallu cination problem. Based on the insight, we propose a novel approach to generating precise protocol formats by adversarially combining LLM-based specification inference and code generation. By inputting the structured RFC documents of network protocols into LLMs, we generate both packet for mats and reference packet parsers that iteratively refine one another to reduce hallucinations: the packet formats allow us to create a variety of network packets for parser testing, while runtime checks in the parsers help identify format errors. Our evaluation of 8 protocols shows a significant increase in preci sion and recall, achieving a 326% improvement over the state of the art in inferring field constraints. Furthermore, the im proved format specifications enable effective fuzzing, leading to the discovery of 24 zero-day vulnerabilities in widely used protocol implementations.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


## 深度分析（并行深度分析更新 2026-09-29）

### 方法、实验与证据
SPAR通过对抗式LLM交互迭代生成正/负数据包并结合RFC和Z3细化格式规范与解析器，直到互相一致；温度0、AutoGen+Z3，八种协议与ParCleanse/ChatAFL比较。路径覆盖和单约束线性否定牺牲理论完备性。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。

---

## 8. L3 深度方法分析补充

### 8.1 方法动机与流程

SPAR 针对现有方法能恢复字段语法、却难以恢复跨字段语义约束的问题。输入是结构化 RFC 文档；LLM 初始生成格式规范与参考解析器，格式作为 oracle 生成正/负包，解析器运行时检查再反向暴露格式错误；两者循环 refinement，最终输出规范、解析器和可用于 fuzzing 的约束包。

### 8.2 核心机制

1. 将格式转换为 packet format graph（PFG），路径上的字段约束由 Z3 求解。
2. 依据规范生成满足约束的正包，并通过线性否定一次违反一个约束生成负包。
3. 依据解析器控制流图生成包，比较 parser 与 format 对同一包的判断。
4. 把不一致的代码/规范片段连同相关 RFC 段落交给 LLM 重新生成；path-cover、相关 RFC section 和负包线性化降低调用成本。
5. 用收敛后的跨字段约束 fuzz Holo 与 FRRouting，查找非崩溃语义漏洞。

### 8.3 实验与关键结果

八种协议为 BFD、BGPv4、BABEL、IGMPv3、HTTP/2、DNS、NTP、SCTP；基线为 ParCleanse 和 ChatAFL，默认 GPT-4.1，另测 Gemini-2.0-Flash、Claude-3.5-Sonnet、Qwen3-Coder，温度 0。SPAR 在字段语法、单字段约束和跨字段约束上接近 100% precision/recall；跨字段约束 recall 明显高于基线，并在 Holo/FRRouting 发现 24 个 zero-day 漏洞。逐协议数值以 PDF Tables 2–4 为准。

### 8.4 局限、复现与证据边界

SPAR 假设树形、非递归格式；path-cover 与一次否定一个约束不能保证理论完备性；RFC 的模糊措辞和 undefined behavior 仍需人工解释，且实现特定行为被有意排除。Artifact 包含 RFC、ground truth、生成器和预计算结果；漏洞 harness 未全部公开以降低双用风险。复现应锁定 LLM 版本、温度、AutoGen、Z3 与八种 RFC。

### 8.5 写作叙事与知识层建议

论文用 BABEL 真实缺失跨字段检查作为动机，再用“规范 oracle↔解析器 oracle”对抗循环解释为何能降低幻觉，最后以协议精度和漏洞发现双重结果收束。可向协议安全/模糊测试专题记录 SPAR；本次未修改共享页面。

## 历史自动入库段落说明

- 本笔记前部的自动入库、摘要级或待核验段落是入库时的历史快照，按规范保留以避免删除原始记录。
- 本次新增的深度分析段落、证据记录和局限说明优先；历史段落中的“待深读/待核验”状态不代表当前分析尚未完成。

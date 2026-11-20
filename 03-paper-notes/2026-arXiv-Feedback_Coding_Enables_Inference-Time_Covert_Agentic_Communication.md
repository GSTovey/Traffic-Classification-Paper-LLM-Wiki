---
type: paper
title_original: "Feedback Coding Enables Inference-Time Covert Agentic Communication"
title_cn: "反馈编码与模型推理期间的隐蔽通信风险"
authors: ["Sidong Guo", "Sajani Vithana", "Atefeh Gilani", "Lalitha Sankar", "Oliver Kosut", "Flavio P. Calmon"]
year: 2026
venue: arXiv
doi: "10.48550/arXiv.2609.24994"
url: "https://doi.org/10.48550/arXiv.2609.24994"
pdf: "00-inbox/PDFs/2026-arXiv-Feedback_Coding_Enables_Inference-Time_Covert_Agentic_Communication.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-Feedback_Coding_Enables_Inference-Time_Covert_Agentic_Communication.md"
status: processed
reading_level: L2
research_area: ["生成文本安全"]
task: ["评估输出通道的泄露风险"]
method: ["反馈信道建模与对照评估"]
dataset: ["三个开放权重模型的受控生成试验"]
code: unknown
relevance: medium
created: "2026-09-29"
updated: "2026-11-20"
---

# Feedback Coding Enables Inference-Time Covert Agentic Communication

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Feedback Coding Enables Inference-Time Covert Agentic Communication |
| 年份 | 2026 |
| 会议/期刊 | arXiv |
| PDF | [[2026-arXiv-Feedback_Coding_Enables_Inference-Time_Covert_Agentic_Communication.pdf]] |
| MinerU Markdown | [[2026-arXiv-Feedback_Coding_Enables_Inference-Time_Covert_Agentic_Communication.md]] |
| 作者 | Sidong Guo, Sajani Vithana, Atefeh Gilani, Lalitha Sankar, Oliver Kosut, Flavio P. Calmon |
| DOI | [10.48550/arXiv.2609.24994](https://doi.org/10.48550/arXiv.2609.24994) |

## 1. 一句话总结

论文评估共同观察生成过程时，文本通道中反馈对隐蔽信息传递可靠性的影响。

## 2. 摘要原文
As large language models (LLMs) are increasingly used to automate digital interactions, users can leverage LLM-generated text as cover for covert communication within seemingly benign conversations. Existing LLM steganography, however, is predominantly white-box, requiring the sender and receiver to share the cover statistics, typically through access to the model weights and prompt. Black-box schemes remove this requirement by allowing the receiver to operate solely on the generated text, but current approaches rely on fixed-length, open-loop watermarking techniques that sufer from high decoding error rates under variable-length token generation. We recast black-box LLM steganography as a sequential communication problem with causal, noiseless feedback: every generated token is observed by both parties and can guide subsequent embedding. Based on this perspective, we introduce Burnashev Adaptive Posterior Matching (BAM), a feedback-coding scheme that combines posterior matching with a decode-and-confirm phase. The design is inspired by classical information-theoretic feedback coding principles, while its security is established through a cryptographic reduction proof. Across three open-weight language models, we demonstrate that BAM attains 0-0.1% empirical message error on an 8-bit payload in around 50 tokens, across 1000 trials, versus 10-17% for the strongest black-box baseline at comparable length. Building on the proposed steganography algorithm, we demonstrate the feasibility of an end-to-end communication protocol that achieves high communication rates across multiple conversational settings.

## 3. 方法分析

将生成文本的相互可见性作为实验条件，以消息错误率比较反馈和论文的黑盒基线。

## 4. 实验表现

- 研究对象：三个开放权重模型的受控生成试验。
- 作者报告：作者在摘要中报告，三种开放权重模型上的反馈方案在受控消息实验中比相近生成长度的黑盒基线有较低错误率。
- 原文位置：[[02-parsed-markdown/2026-arXiv-Feedback_Coding_Enables_Inference-Time_Covert_Agentic_Communication|原文解析稿]] · 摘要、实证评估与适用条件。

## 5. 局限性与复现建议

实验使用作者设定的反馈和消息条件。不同服务的监控能力、时延与模型接入约束需要独立测量。

## 6. 知识链接
- [[traffic-classification]]
- [[encrypted-traffic-analysis]]

## 7. 证据状态

本页摘要区属于论文级记录。正文方法与结果已对照 [[02-parsed-markdown/2026-arXiv-Feedback_Coding_Enables_Inference-Time_Covert_Agentic_Communication|原文解析稿]] · 摘要、实证评估与适用条件。可引用的结论须保留所列实验条件。

## 深度分析（并行深度分析更新 2026-09-29）

### 方法、实验与证据
BAM反馈编码把连续文本作为cover，分层评估token级隐写率/可靠性与端到端隐蔽agent通信；1000次、C4 RealNews 200 prompts、top-50温度1。论坛covertext下Llama-3.1消息错误<1%，Phi-4接近零错误；协议基线有限。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。

## 历史自动摘录

> 早期入库生成的字段和占位段落。现行记录见上文。

```markdown
title_cn: ""
research_area: []
task: []
method: []
dataset: []

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。


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


## 7. 证据状态
- MinerU：已完成；解析质量需人工抽查。
- Bib 元数据：待官方 API/论文首页核验。



## 深度分析（自动证据提取，需人工复核）

### 研究问题与证据
- 主题线索：tor, adversarial, covert。
- 摘要证据：As large language models (LLMs) are increasingly used to automate digital interactions, users can leverage LLM-generated text as cover for covert communication within seemingly benign conversations. Existing LLM steganography, however, is predominantly white-box, requiring the sender and receiver to share the cover statistics, typically through access to the model weights and prompt. Black-box schemes remove this requirement by allowing the receiver to operate solely on the generated text, but current approaches rely on fixed-length, open-loop watermarking techniques that sufer from high decoding error rates under variable-length token generation. We recast black-box LLM steganography as a sequential communication problem with causal, noiseless feedback: every generated token is observed by both parties and can guide subsequent embedding. Based on this perspective, we introduce Burnashev Adaptive Posterior Matching (BAM), a feedback-coding scheme that combines posterior matching with a decode-and-confirm phase. The design is inspired by classical information-theoretic feedback coding principles, while its security is established through a cryptographic reduction proof. Across three open-weight language models, we demonstrate that BAM attains 0-0.1% empirical message error on an 8-bit payload in around 50 tokens, across 1000 trials, versus 10-17% for the strongest black-box baseline at comparable length. Building on the proposed steganography algorithm, we demonstrate the feasibility of an end-to-end communication protocol that achieves high communication rates across multiple conversational settings.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
• Reliability: BAM achieves significantly smaller error at shorter average length and the perfor mance gain is roughly two orders of magnitude better than the best baseline. Across all three models BAM achieves a substantially better reliability-length tradeof than the benchmark baselines. Concretely, BAM attains a message error rate of $\leq 0 . 1 \%$ over 1000 runs with an average token below 50 across all three LLM models, whereas the strongest baselines of comparable length incur 10–17% message error. The strong reliability guarantee is the cornerstone of ensuring covert communication. A detailed ablation for explaining the sources of performance gain is provided in Appendix D. • Text Quality: In these trials, the stegotext generated by our method retains similar linguistic quality of texts generated from a clean model. The BAM outputs show only a modest perplexity diference across three models, compared to the base perplexity. Such diferences are on par with other distortion-free algorithms such as [18, 13, 10], while exhibiting better quality than distortionary [38]. • Time: The additional runtime of BAM comes mainly from channel synthesis (OT) and posterior update. As shown in Table 1, BAM runtime is the weakest part of the algorithm and exhibits a 30%, 6%, 17% increase compared to ArcMark over Llama, Qwen and Mistral, respectively. This is a result of posterior matching, which must be computed at both encoder and decoder. A detailed breakdown of runtime, as well as scalability concerns, are addressed in Appendix D.

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：未检测到明确 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


```

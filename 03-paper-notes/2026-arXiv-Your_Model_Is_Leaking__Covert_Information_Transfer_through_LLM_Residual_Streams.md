---
type: paper
title_original: "Your Model Is Leaking: Covert Information Transfer through LLM Residual Streams"
title_cn: ""
authors: []
year: 2026
venue: arXiv
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-arXiv-Your_Model_Is_Leaking__Covert_Information_Transfer_through_LLM_Residual_Streams.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-Your_Model_Is_Leaking__Covert_Information_Transfer_through_LLM_Residual_Streams.md"
status: processed
reading_level: L2
research_area: []
task: []
method: []
dataset: []
code: unknown
relevance: medium
created: "2026-09-29"
updated: "2026-09-29"
---

# Your Model Is Leaking: Covert Information Transfer through LLM Residual Streams

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Your Model Is Leaking: Covert Information Transfer through LLM Residual Streams |
| 年份 | 2026 |
| 会议/期刊 | arXiv |
| PDF | [[2026-arXiv-Your_Model_Is_Leaking__Covert_Information_Transfer_through_LLM_Residual_Streams.pdf]] |
| MinerU Markdown | [[2026-arXiv-Your_Model_Is_Leaking__Covert_Information_Transfer_through_LLM_Residual_Streams.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
—Privacy-sensitive organizations may run LLMs in restricted or air-gapped environments while still exporting selected diagnostic or audit artifacts. These artifacts may be available to authorized reviewers who should not learn sensitive information from the underlying inference process. We show, however, that a compromised LLM runtime component can hide sensitive information in intermediate activations that are allowed to leave the restricted environment. An offline observer can recover this information with a simple linear decoder. The attack requires no retraining, weight changes, or control over the export process. This creates a covert exfiltration channel. We introduce RESIDUALMUX, a residual-stream covertchannel attack that embeds sensitive information into routine activation artifacts. Our attack maps each message to a codeword and injected it into an intermediate residual stream through a compromised runtime hook. The signal then propagates with normal model execution and is captured by an authorized downstream activation recorder; once the artifact crosses the trust boundary, an offline linear decoder recovers the message. To maintain recoverability, RESIDUALMUX scales the injection strength with the local residual norm using the signal-to-residualnorm ratio (SRR). Across eleven models from seven architecture families, our evaluation shows high recovery with limited output changes (91–100% recovery on nine models; KL divergence 0.001–0.007), while the evaluated activation-level detectors remain close to random guessing (AUC ≤ 0.56) and tested posthoc defenses do not reliably eliminate the channel. An activation artifact can thus be schema-valid while carrying information that is not authorized to cross the boundary. Our code is hosted at https://anonymous.4open.science/r/ResidualMux-6D23.

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
- 主题线索：tor, transformer, adversarial, covert。
- 摘要证据：We introduce RESIDUALMUX, a residual-stream covertchannel attack that embeds sensitive information into routine activation artifacts. Our attack maps each message to a codeword and injected it into an intermediate residual stream through a compromised runtime hook. The signal then propagates with normal model execution and is captured by an authorized downstream activation recorder; once the artifact crosses the trust boundary, an offline linear decoder recovers the message. To maintain recoverability, RESIDUALMUX scales the injection strength with the local residual norm using the signal-to-residualnorm ratio (SRR). Across eleven models from seven architecture families, our evaluation shows high recovery with limited output changes (91–100% recovery on nine models; KL divergence 0.001–0.007), while the evaluated activation-level detectors remain close to random guessing (AUC ≤ 0.56) and tested posthoc defenses do not reliably eliminate the channel. An activation artifact can thus be schema-valid while carrying information that is not authorized to cross the boundary. Our code is hosted at https://anonymous.4open.science/r/ResidualMux-6D23.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
$$ \mathrm{acc} _ {\text { chance }} = \frac {1}{K}.\tag{19} $$ For $K { = } 1 6$ (our primary operating point), chance is 6.25%; for $K { = } 4 ,$ , chance is 25%. Probe accuracy at or near chance indicates that a defense has eliminated the covert signal; accuracy above chance means recoverable information remains. ![](images/b6e8c9ae49937bf4ac3e7f3ffc52c8962d6959379c3a193475354580c5e0705d.jpg) Fig. 3: Detection AUC at α=0.5, K=16 across nine models and five detectors. All methods stay near chance, and the Qwen3.5 family converges monotonically to AUC 0.5 with scale. TABLE II: Per-model held-out validation recovery at $K = 1 6$ after calibration-time selection of the injection/readout layer pair. The table measures calibrated channel viability on the evaluated prompt distribution rather than cross-workload generalization. All nine models exceed 91%. Models marked with † require norm-normalized injection (SRR-scaled α); others use fixed α=0.25. <table><tr><td>Model</td><td>d</td><td>Best $\ell \rightarrow r$ </td><td> $\alpha$ </td><td>Val acc (%)</td></tr><tr><td>Qwen3.5-27B</td><td>5120</td><td>1 → 3</td><td>0.25</td><td>100.0</td></tr><tr><td>Qwen3.5-0.8B</td><td>1024</td><td>7 → 9</td><td>0.25</td><td>99.8</td></tr><tr><td>Qwen3.5-4B</td><td>2560</td><td>1 → 3</td><td>0.25</td><td>99.4</td></tr><tr><td>Qwen3.5-9B</td><td>4096</td><td>1 → 3</td><td>0.25</td><td>98.0</td></tr><tr><td>Qwen3.5-2B</td><td>2048</td><td>1 → 3</td><td>0.25</td><td>96.7</td></tr><tr><td>Llama-3.2-1B</td><td>2048</td><td>1 → 3</td><td>0.25</td><td>96.1</td></tr><tr><td>Gemma-3-1B $^{\dagger}$ </td><td>1152</td><td>1 → 3</td><td>3.39</td><td>94.7</td></tr><tr><td>GPT-2 $^{\dagger}$ </td><td>768</td><td>1 → 3</td><td>2.79</td><td>94.5</td></tr><tr><td>Phi-4-mini</td><td>3072</td><td>1 → 3</td><

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


## 深度分析（并行深度分析更新 2026-09-29）

### 方法、实验与证据
LLM残差流注入实现隐蔽信息传递；11模型、7架构、0.1B–27B，比较水印/令牌/时序/KV等基线。Mahalanobis+PCA检测AUC 0.46–0.50，监督MLP 0.50–0.57；攻击前提是代码级管线和hidden states访问，闭源API不在范围。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。

---
type: paper
title_original: "Robust Coverless Linguistic Steganography via Sentence Embedding Space with Global Resynchronization"
title_cn: "基于句嵌入空间与全局重同步的鲁棒无载体语言隐写"
authors: [Lizhi Xiong, Yuping Lu, Ziqiang Li, Jun Li, Zhangjie Fu]
year: 2026
venue: "arXiv 2026"
doi: "unknown"
url: "https://arxiv.org/abs/2609.04970"
pdf: "00-inbox/PDFs/2026-arXiv-Robust_Coverless_Linguistic_Steganography_via_Sentence_Embedding_Space_with_Global_Resynchronization.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-Robust_Coverless_Linguistic_Steganography_via_Sentence_Embedding_Space_with_Global_Resynchronization.md"
status: processed
reading_level: L1
research_area: []
task: []
method: []
dataset: ["PersonaChat", "C4", "IMDB"]
code: "unknown"
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

# Robust Coverless Linguistic Steganography via Sentence Embedding Space with Global Resynchronization

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Robust Coverless Linguistic Steganography via Sentence Embedding Space with Global Resynchronization |
| 中文标题 | 基于句嵌入空间与全局重同步的鲁棒无载体语言隐写 |
| 作者 | Lizhi Xiong, Yuping Lu, Ziqiang Li, Jun Li, Zhangjie Fu（南京信息工程大学） |
| 年份 | 2026 |
| 会议/期刊 | arXiv 2026（解析稿含 CCS Concepts 段，但首页无会议页眉；解析稿未见 DOI 与 arXiv 编号） |
| 研究方向 | 文本隐写/隐蔽通信（非流量分析主题） |
| 任务类型 | 语言隐写（信息隐藏与鲁棒提取） |
| 方法关键词 | 句嵌入空间、层次聚类（HCM）、可证安全采样 SparSamp、LT 码全局重同步（GRM）、BP 译码 |
| 数据集 | PersonaChat（主实验）、C4、IMDB（PPL 与容量评估） |
| 是否开源 | 未提及（code=unknown） |
| PDF | 00-inbox/PDFs/2026-arXiv-Robust_Coverless_Linguistic_Steganography_via_Sentence_Embedding_Space_with_Global_Resynchronization.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-arXiv-Robust_Coverless_Linguistic_Steganography_via_Sentence_Embedding_Space_with_Global_Resynchronization.md |

---

## 1. 一句话总结

> 把隐写单元从脆弱的 token 序列搬到句嵌入的语义子空间（HCM 分层聚类）并用 LT 码做全局重同步（GRM），改写攻击下提取错误率降至 0.0038。

---

## 2. 摘要翻译

### 2.1 摘要原文

> "Linguistic steganography enables covert communication through natural language. Existing methods heavily rely on token-level operations and struggle to maintain reliability under word- and sentence-level textual perturbations. Moreover, variable-length coding-based schemes are highly susceptible to bit-slippage under minor disturbances... we propose a robust coverless steganographic framework that operates in the sentence embedding space rather than the token space."（Abstract，节选）

### 2.2 摘要中文翻译

语言隐写可借自然语言实现隐蔽通信。现有方法高度依赖 token 级操作，在词级与句级文本扰动下难以保持可靠性；且基于变长编码的方案在轻微扰动下极易发生比特滑移（bit-slippage）——扰动导致嵌入与提取的比特序列失步。为此，本文提出在句嵌入空间（而非 token 空间）运行的鲁棒无载体隐写框架：秘密消息被编码为句嵌入空间中的层次聚类路径，从而提升词级/句级扰动下的解码稳定性；针对比特滑移，引入全局重同步机制（GRM），把变长比特流重构为锚定语义子空间的离散符号，将局部嵌入失败与全局消息恢复解耦。实验表明，在词级与句级扰动下本方法鲁棒性显著提升，同时保持有效嵌入容量，并对统计分析具有强抗性。

> ⚠️ MinerU 解析问题：数学公式中的变量（如 b、l、s、α）多处被解析为替换符"�"（如公式 2、5、6 附近的变量书写）；引用具体公式变量时需回查原文 PDF。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

真实社交平台上的文本会被删除、插入、替换、改写；而现有隐写（修改式/检索式/生成式）都建立在脆弱的字符或 token 级对应关系上，轻微扰动即导致解码失败或整段丢失（§1、Figure 1）。

### 3.2 现有方法的痛点和不足

① token 级防御（SECC、Syncpool 等）只处理 token 级扰动，忽略词级/句级删改与改写；② 生成式方法的强序列依赖使单 token 损坏向后传播；③ 变长编码在冲突/错聚类时造成比特滑移，错误沿比特流扩散；④ 现有的可证安全方法（ADG/Discop 等）在语义保持扰动下的提取错误率接近随机猜测（§2.1–2.3、§3.4）。

### 3.3 论文的研究假设或核心直觉

高质量句嵌入具有近似语义不变性：轻微文本扰动后句子仍落在同一聚类子空间内。因此把秘密比特绑定到"子空间身份"而非"具体向量坐标"，即可容忍词级/句级攻击；再用 LT 码把局部失步当作擦除（erasure）处理，实现全局可恢复（§3.3、§3.4）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 词/句级扰动使 token 级隐写解码失败；变长编码出现比特滑移 | §1、Figure 1、§3.4 |
| 痛点提炼 | 鲁棒性不足使隐写在真实平台不可用；擦除与错误混淆导致错误率接近 50% | §1、§2.3 |
| 问题转化 | 需要一种"结构级"隐写单元与一套"错误定位+全局恢复"机制 | §3.2、推断 |
| 文献定位 | 已有的鲁棒隐写仅覆盖各自 token 级攻击；句级改写场景缺失 | §2.3 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 以语义子空间为隐写单元，可把词/句级扰动转化为可控的错聚类，而非比特级破坏 | §3.3 | 五类文本攻击实验（§4） |
| 辅助假设（如有） | 变长编码的失步可用 LT 码擦除信道模型全局恢复 | §3.4 | GRM 消融（Figure 7、Table 7） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 子空间隐写鲁棒 | 支撑 | 改写攻击 P_E 0.0038（基线 0.2138–0.6145）；词级攻击 P_E < 2.7% | Table 1、§4.3 |
| GRM 有效 | 支撑 | 3× 冗余下删除攻击 ER=0.1338 bit/token（1.5× 时为 0.2552） | Table 7、Figure 7 |

---

## 4. 方法设计

### 4.1 方法整体流程

嵌入：共享句编码器把数据集句子映射到统一语义空间 → k-means 在伪随机种子下划分可编码子空间 → HCM 逐层递归选择子空间（每层嵌入 b̄ 比特）→ SparSamp 按累积分布采样保证分布保真 → 选中子空间的自然句作为载体发送。提取：同一编码器与聚类重建空间 → 预测每句所属子空间 → 按 ESI 重组全局符号流 → BP 译码恢复消息（§3.2、Figure 2）。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | 句编码器输出向量 | k-means（种子 r_c）划分 k 个子空间 | 子空间划分 C_{r_c} | 建立编码单元 |
| Step 2 | 秘密比特 + 前层子空间 | HCM 逐层选择下一层子空间（l 层、每层 b̄ 比特） | 层次聚类路径 | 高容量且复杂度近线性 |
| Step 3 | 累积分布 + 共享密钥 | SparSamp 伪随机位置采样（逆 CDF） | 选中子空间 | 保持自然分布、可证安全 |
| Step 4 | 选中子空间 | 随机抽取自然句作为 stego 文本 | 发送文本 | 无载体修改 |
| Step 5 | 接收文本 | 重建聚类 → 子空间预测 → LT 符号块按 ESI 重组 → BP 译码 | 恢复消息 | 全局重同步抗失步 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 句编码器（Sentence-T5-Large） | 句子→语义向量 | 原始句 | 嵌入向量 | 收发双方共享 |
| k-means 子空间划分 | 空间分割为 k 个子空间 | 嵌入向量集 + 种子 | 聚类中心/划分 | HCM 每层调用 |
| HCM | 分层递归选择子空间，降低复杂度 | 上层的子空间 + 比特 | 下一层子空间 | 与 SparSamp 交互 |
| SparSamp 采样 | 分布保真采样，防冲突 | 累积分布 + 密钥 | 选中子空间 | 决定载体句 |
| GRM（LT 码 + BP） | 把失步/冲突当擦除，全局恢复 | 符号块 ESI | 原始消息 | 提取端收尾 |

### 4.4 公式、算法和机制解释

- 语义相似度（式 1）与威胁模型约束：攻击变换满足近似语义不变性 ‖v(s′)−v(s)‖₂ ≤ ε（式 2）；
- k-means 目标（式 3）：以伪随机种子初始化保证收发一致；容量与子空间数关系 k ∝ 2^b（式 5），直接 k-means 复杂度 O(N·2^b)，HCM 把复杂度降为 l·O(N·2^b̄) ≈ O(N·l)（§3.3）；
- 采样：累积分布 F(j)（式 6）、伪随机位置 r(i)=(x_i+r_Δ) mod 1（式 7）、逆 CDF 选子空间（式 8–9）；同一子空间出现多个伪随机位置时本层不嵌入（message conflict）；
- GRM：LT 编码符号流按全局 ESI 预分配，缺失符号视为自然擦除，收齐超过译码阈值后一次性 BP 译码（§3.4）。

### 4.5 方法优势

抗词级/句级攻击（改写攻击 P_E 0.0038）；直接复用语料自然句，PPL 显著低于生成式方法（PersonaChat 53.85 vs 109.34–128.55）；抗隐写分析接近随机猜测（五类分析器 49.60–56.49%）；HCM 把高容量聚类的计算开销降到近线性（§4.3、Tables 1–4、6）。

### 4.6 方法不足

无损传输下原始嵌入率不占优（ER 0.14/0.08/0.07 bit/token，低于 AC 的 2.47）；有效容量 EER（0.13/0.08/0.07）略低于部分基线；替换/删除攻击下 ER 略升（语义关键词被改写导致错聚类）；依赖共享数据集、编码器与密钥等先决条件（§3.1、§4.3）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

修改式/生成式隐写在 token 概率或字符层面操作，本文在句嵌入语义子空间层面操作，秘密信息绑定"子空间身份"而非"具体 token/句子"；引入可证安全采样保证分布保真，再用 LT 码把变长失步转为擦除信道问题（§2、§3）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 句嵌入空间无载体隐写 | 以语义子空间为隐写单元，天然吸收词/句级扰动 | 高 | 部分（语义子空间编码思想可迁移到其他隐蔽载体） |
| HCM 层次聚类 | 每层 k=8、b̄=2–3 比特，复杂度指数→线性 | 高 | 是（大规模聚类编码的工程优化） |
| GRM 全局重同步 | LT 码 + ESI 预分配，把失步/冲突转为擦除 | 高 | 是（变长隐写/水印的失步恢复） |

### 5.3 适用场景

对鲁棒性要求高、文本可能被平台或对手改写/删改的隐蔽通信场景；需要抵抗隐写分析的高安全需求场景（§3.1 威胁模型）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| AC / ADG（生成式可证安全） | 分布保真、理论安全 | 改写攻击下 P_E 0.39–0.61 | 语义子空间 + GRM 降至 0.0038 |
| SECC（叠加 ECC） | 降低擦除率（BLR→0） | 符号错误率仍近 50%，纠错失效 | 保持低 BLR 的同时压低 BER |
| Discop / STEAD | 高容量/抗插入删除（各自 token 级） | 改写攻击下完全无法解码（BLR=1） | 句级改写下仍可恢复 |
| FSBTS | 鲁棒性与 EER 强 | 依赖更大数据集，可比性受限 | 在共享语料上保持同量级容量 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

以 Sentence-T5-Large 为句编码器，HCM 设层数 l=3、每层簇数 k=8，BP 译码；攻击类型包括删除、替换、插入、交换（词级，攻击强度 α 为被改词占比）与改写（句级，Parrot_Paraphraser），LT 冗余默认 3×（§4.1、§4.3）。

### 6.2 数据集

主实验 PersonaChat；PPL 与容量另测 C4、IMDB；基线 FSBTS 使用 openConcepts 数据集（§4.1）。

### 6.3 Baseline

AC、ADG、Discop、SECC、STEAD、FSBTS；STEAD 用 Dream-7B，其余用 GPT-2（§4.1）。

### 6.4 评价指标

综合提取错误率 P_E=(1−BLR)·BER+0.5·BLR（式 10）；PPL（DialoGPT-medium）；ER/EER（bit/token）；五类隐写分析器检测准确率（越接近 50% 越安全）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| 改写攻击（Table 1） | P_E | 0.0038 | 0.2138（FSBTS） | 约 56× | Discop/STEAD 完全失步（BLR=1） |
| 词级混合攻击（α=5, Table 3） | P_E | 0.0038 | 0.0438（FSBTS） | 约 11× | 本文 ER 0.14/0.08/0.07 bit/token |
| PPL（PersonaChat, Table 2） | PPL↓ | 53.85 | 109.34（Discop） | ≈2× 更低 | C4 43.21、IMDB 41.52 同为最优 |
| 抗隐写分析（Table 4） | 检测准确率 | 49.60–56.49% | — | — | 接近随机猜测即安全 |
| 删除攻击容量（Table 7） | ER（3× 冗余） | 0.1338 | 0.2552（1.5×） | — | 冗余换鲁棒性的折中 |

### 6.6 优势最明显的场景

句级改写与词级删改混合的真实平台场景：基线错误率趋近 50% 随机猜测时，本方法仍保持 P_E < 2.7%，并且 PPL 最低（§4.3）。

### 6.7 局限性

无损信道下原始容量不占优；k 增大到 16 时鲁棒性明显恶化（Table 5：P_E 升至 0.11–0.32）；依赖双方共享数据集与编码器；未报告端到端真实平台部署与对抗性隐写分析自适应攻击（§4.3、Table 5）。

---

## 7. 学习与应用

### 7.1 是否开源？

解析稿未提及代码或数据发布地址（code=unknown）。

### 7.2 复现关键步骤

1. 选定共享语料与句编码器（Sentence-T5-Large），以共享种子做 k-means 划分；
2. 实现 HCM 逐层选簇与 SparSamp 逆 CDF 采样（含冲突判定）；
3. 接入 LT 编码（ESI 预分配、3× 冗余）与 BP 译码，按五类攻击评估 P_E、ER/EER 与 PPL。

### 7.3 关键超参数、预处理和训练细节

层数 l=3、每层簇数 k=8（按鲁棒性/容量折中选取，Table 5 有 k∈{2,4,8,16} 消融）；每层 b̄ 取 2 或 3；LT 冗余 3×；攻击强度分析取 α=5；PPL 以 DialoGPT-medium 计算（§3.3、§4.1、§4.3）。

### 7.4 能否迁移到其他任务？

以下为笔记作者的迁移分析（非论文原文主张）——可迁移的机制：① "以粗粒度语义/结构单元承载比特、用纠删码做全局重同步"的思路可用于流量水印与 WF 防御中的标记鲁棒性设计；② 用累积分布+伪随机位置采样保持分布保真的技巧，可用于任何要求"输出分布不可区分"的隐蔽信道；③ 其"错误率分解为 BER 与 BLR 并用全概率合成 P_E"的度量方式，可作为隐蔽信道评估指标模板（式 10）。

### 7.5 对我的研究有什么启发？

该文把"失步"显式建模为擦除并与纠错解耦（GRM），这一模式对流量侧隐蔽信道/水印（如包时序编码在抖动下的失步）同样成立：与其在局部做重传，不如在全局用纠删码容忍局部丢失。

---

## 8. 总结

### 8.1 核心思想

> 语义子空间承载比特，LT 码全局重同步抗失步。

### 8.2 速记版 Pipeline

1. 句编码器把语料映射到语义空间，k-means 分子空间；
2. HCM 逐层选簇（l=3、k=8），每层嵌入 2–3 比特；
3. SparSamp 采样保分布、防冲突，选自然句作载体；
4. 攻击后接收端重建聚类、预测子空间；
5. 符号块按 ESI 重组，BP 译码恢复消息（3× LT 冗余）。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- 库内无对应概念页：本库概念白名单全部面向网络流量分析，语言隐写/隐蔽通信不在其中；主题最近邻为 [[censorship-circumvention]]（同属"隐蔽通信"大类但载体与方法完全不同，仅供参考，不构成实质关联）。

### 9.2 相关方法

- 库内无对应方法页：本文方法为语义聚类 + 纠删码，白名单 8 个方法 slug 均不适用。

### 9.3 相关任务

- 库内暂无对应任务页（文本隐写非流量分析任务）。

### 9.4 可更新的综述页面

- 暂无：与库内 5 个综述页主题均不重叠。

### 9.5 可加入的对比表

- 暂无适用项（本文未提出新方法 slug 可入 [[method-comparison-table]]，未发布数据集，无开源代码）。

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 改写攻击下 P_E 0.0038，基线 0.2138–0.6145，Discop/STEAD 完全失步 | Table 1 | §4.3 |
| 词级攻击（α=5）P_E < 2.7%；综合错误率按 P_E=(1−BLR)·BER+0.5·BLR 计算 | 式 10、Figure 6 | §4.2–4.3 |
| PPL 53.85/43.21/41.52（PersonaChat/C4/IMDB），显著低于生成式基线 | Table 2 | §4.3 |
| HCM 层数消融：1 层 20.96 s/bit → 2 层 1.37 s/bit，复杂度由指数降为近线性；LT 冗余 3× 时删除攻击 ER 0.1338 bit/token（1.5× 为 0.2552） | Table 6、Table 7、§3.3 | §4.3 |
| 五类隐写分析器检测准确率 49.60–56.49%，接近随机猜测 | Table 4 | §4.3 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-arXiv-Robust_Coverless_Linguistic_Steganography_via_Sentence_Embedding_Space_with_Global_Resynchronization.pdf
- MinerU Markdown：02-parsed-markdown/2026-arXiv-Robust_Coverless_Linguistic_Steganography_via_Sentence_Embedding_Space_with_Global_Resynchronization.md

---

## 12. 后续问题

- 暂未整理。

---
type: paper
title_original: "From Symmetry toward Weak Asymmetry: Secure Steganography under the Receiver's Partial Channel Knowledge"
title_cn: "从对称走向弱非对称：接收方仅掌握部分信道知识时的可证明安全隐写"
authors: [Guorui Liao, Shuyu Gan, Jinshuai Yang, Yongfeng Huang, Zhongyi Huang]
year: 2026
venue: "USENIX Security 2026"
doi: "unknown"
url: "https://www.usenix.org/conference/usenixsecurity26/presentation/liao"
pdf: "00-inbox/PDFs/2026-USENIX-From_Symmetry_toward_Weak_Asymmetry__Secure_Steganography_under_the_Receiver's_Partial_Channel_Knowledge.pdf"
mineru_md: "02-parsed-markdown/2026-USENIX-From_Symmetry_toward_Weak_Asymmetry__Secure_Steganography_under_the_Receiver's_Partial_Channel_Knowledge.md"
status: deep-analyzed
reading_level: L3
research_area: ["censorship-circumvention", "provable steganography", "language-model communication"]
task: ["weakly asymmetric covert communication", "distribution-mismatch robustness"]
method: ["threshold knowledge", "rank-based ParitySplit", "stateful PRG sampling", "computational indistinguishability"]
dataset: ["Meta-Llama-3-8B-Instruct", "Qwen2.5-7B-Instruct", "float32-to-float16 mismatch benchmark"]
code: "https://doi.org/10.5281/zenodo.20428322"
relevance: medium
created: "2026-09-19"
updated: "2026-10-10"
---

## 0. 论文基础信息

> **L3 深度分析笔记**：基于正文 §1–§5、Definitions/Theorems、Algorithms 1–12、Tables 1–2 与 Open Science 章节交叉核对。论文研究的是密码学隐写，不是流量分类；容量、利用率、token/response 正确率与分布失配结果必须分开引用。

| 项目 | 内容 |
|---|---|
| 标题（原文） | From Symmetry toward Weak Asymmetry: Secure Steganography under the Receiver's Partial Channel Knowledge |
| 标题（中文） | 从对称走向弱非对称：接收方仅掌握部分信道知识时的可证明安全隐写 |
| 作者 | Guorui Liao, Shuyu Gan, Jinshuai Yang, Yongfeng Huang, Zhongyi Huang |
| 单位 | Tsinghua University（清华大学） |
| 发表年份 | 2026 |
| 发表会议 | USENIX Security 2026（第 35 届 USENIX Security Symposium，2026-08-12~14，Baltimore） |
| 论文类型 | 密码学理论构造 + 语言模型文本隐写实验 |
| 研究领域 | 抗审查通信（censorship-circumvention）；可证明安全隐写 / 隐蔽信道 |
| 方法 | 基于语言模型的条件分布采样（llm 作为 covertext channel oracle） |
| 数据集 | 无公开数据集；实验以 Meta-Llama-3-8B-Instruct 与 Qwen2.5-7B-Instruct 作为信道模型，固定 prompt "Tell me something about steganography" |
| 代码 / artifact | https://doi.org/10.5281/zenodo.20428322 （rank-based 方案实现 + §5 实验脚本） |
| DOI | unknown（解析稿未给出论文 DOI；Zenodo 为 artifact DOI，非论文 DOI） |
| PDF | 00-inbox/PDFs/2026-USENIX-From_Symmetry_toward_Weak_Asymmetry__Secure_Steganography_under_the_Receiver's_Partial_Channel_Knowledge.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-USENIX-From_Symmetry_toward_Weak_Asymmetry__Secure_Steganography_under_the_Receiver's_Partial_Channel_Knowledge.md |

> ⚠️ MinerU 解析问题：算法（Algorithm 1-12）以 `<div class="mineru-algorithm">` 包裹，内含 HTML 实体（`&lt;`、`&amp;`）与条件语句错位；公式在行内被拆分（如 `Encod $\mathsf{a}$` 拆成 "Encoda"）；节标题出现 `I<sub>n</sub>t<sub>ro</sub>d<sub>uc</sub>ti<sub>on</sub>` 型小型大写字母碎片。本笔记引用时已还原为正常文字，Table 1/2 数值按解析稿原样抄录。

## 1. 一句话总结

论文提出"弱非对称隐写"（weakly asymmetric steganography）这一新设定：发送方掌握完整条件分布、接收方仅掌握其**部分知识**（二值化阈值 1_θ 或符号概率排序 rank/partial-rank），并给出可证明安全的构造——rank 方案在 Llama-3-8B 上以满秩知识达 111.2 bit/响应（利用率 28.44%），仅知 top-2 排序仍有 49.9 bit/响应，而在 float32→float16 精度失配下 token 级准确率仍 >99%。

## 2. 摘要翻译

### 2.1 摘要原文（节选）

> Provably secure steganography enables covert communication by disguising secret messages as normal communication content while guaranteeing computational indistinguishability. Recent work typically assumes that the sender can construct stegotext based on explicit conditional distributions, while the receiver either has access to the same distributions for decoding or has no such access at all. In many realistic communication settings, however, the receiver's access lies between these two extremes... We therefore introduce and study a new setting, called weakly asymmetric steganography... The results show that weakly asymmetric steganography can achieve non-trivial embedding capacity, and further suggest the potential of this setting in distribution-mismatch scenarios.

### 2.2 摘要中文翻译

可证明安全隐写通过把秘密消息伪装成正常通信内容并保证计算不可区分性，实现隐蔽通信。既有工作通常假设：发送方能基于显式条件分布构造隐写文本，而接收方要么能访问同一分布（对称隐写），要么完全无法访问（非对称/不可检测隐写）。然而在许多现实通信场景中，接收方的能力介于这两个极端之间——这一区间不被任何一种假设所覆盖。为此，我们提出并研究一个新设定：**弱非对称隐写**——发送方可访问用于构造隐写文本的完整条件分布，而接收方仅掌握由该分布导出的部分知识。我们针对若干有代表性的接收方知识形式设计了可证明安全的隐写方案：具体包括二元字母表下接收方仅知道某符号概率是否超过给定阈值，以及一般字母表下接收方仅观察到符号按概率的部分排序。我们在语言模型文本隐写场景下，从"接收方知识受限"与"精度导致的分布失配"两个角度评估了基于排序（rank-based）的构造。结果表明：弱非对称隐写能够达到非平凡的嵌入容量，并进一步显示该设定在分布失配场景中的潜力。

## 3. 方法动机

1. **既有两类假设之间存在空白**：对称隐写（如 Meteor）要求接收方精确复现发送方的条件分布；非对称/不可检测隐写（如 Zamir 的方案）则假设接收方完全无分布访问，只能靠假设检验聚合恢复少量比特。现实中的接收方常常"介于两者之间"。
2. **两类现实的中间场景**：(a) 接收方算力受限或只能通过受限 API 访问模型，只能看到 top-k token 或采样输出；(b) 即使双方运行同一模型，数值精度、硬件差异与推理不确定性（LLM 推理非确定性）仍会导致分布被扰动，接收方拿到的是"扰动版分布"。
3. **对称方案的脆弱性**：对称方案的解码正确性依赖"逐步重建同一条件分布"的脆弱一致性要求，实现细节或数值精度的微小差异即可改变诱导分布，导致解码失败。
4. **非对称方案的容量瓶颈**：非对称方案虽然解码鲁棒、无需同步信道历史，但每符号互信息极小，容量显著受限，不适用于有吞吐需求的隐蔽通信。
5. **核心理论问题**：给定某种部分信道知识，是否存在**非平凡**（即真正利用该知识、而非退化为忽略它的非对称方案）的可证明安全方案？既有工作未给出任何肯定证据。

### 3.5 科学假设形成

| 假设 | 具体内容 | 验证方式 | 结果 |
|---|---|---|---|
| H1 | 接收方掌握阈值或排序等非退化知识时，可以在不共享完整分布的条件下获得非零隐写容量 | Threshold 1_θ 与 Rank/PRank 构造、容量定理 | 支持：Llama Rank Full 111.223 bit/resp、Top2 49.855；Qwen Rank Full 170.589、Top2 63.302 |
| H2 | ParitySplit 只依赖概率排序就能构造可逆的安全采样，而无需接收方知道概率值 | 奇偶递归、容量式与正确性证明 | 支持：1−p_max ≤ C_rank ≤ H(D)，实验 Correctness=100% |
| H3 | 粗粒度排序知识比精确分布知识更能抵抗发送方/接收方数值精度失配 | float32 发送方→float16 接收方实验 | 支持但容量有权衡：Rank token accuracy 全部 >99%，Top2 response accuracy 最高 50.6%；对称方案 response accuracy 0.0–1.8% |
| H4 | 部分知识方案不是把无知识非对称方案换名，而是能在安全性和容量之间形成独立工作点 | 与 Undetectable Steganography t=2 对比 | 支持：Top2 容量约为非对称基线 20 倍，仍保持 100% 正常分布场景正确率 |

## 4. 方法设计

### 4.1 形式化框架

- **知识函数 f**：把分布 D（字母表 Σ 上的概率分布）映射到特征空间 Y，即 f: X → Y；接收方"拥有知识 f"指对任意历史 H 都能访问 f(D_H)。
- **同态端点**：f_id(D) = D 对应完整信道知识；常数函数对应"无信道知识"。本文研究严格介于两者之间的**非退化**知识函数，称接收方"拥有部分信道知识"。
- **定义 1（弱非对称隐写）**：方案 Π_{D,f} = (KeyGen_D, Encode_D^f, Decode_{f(D)})，下标 D 表示拥有完整分布，下标 f(D) 表示只拥有知识 f(D)；要求 Correctness（解码错误可忽略）与 Security（对任意 ppt 敌手，Encode 预言机与按 D 的随机采样预言机 O_D 不可区分，即 chosen hiddentext attack 下成立）。

| 设定 | 发送方 | 接收方 | 代表方案 |
|---|---|---|---|
| 对称隐写 | 完整分布 | 完整分布 | Meteor、Discop、SparSamp |
| **弱非对称隐写（本文）** | 完整分布 | **部分知识 f(D)** | Rank (Full/Top-k)、Threshold 1_θ |
| 非对称/不可检测隐写 | 完整分布 | 无分布知识 | Undetectable Steganography (Zamir) |

### 4.2 二元字母表 + 阈值知识 1_θ

- 知识函数 1_θ(D) := 1[D(σ₀) < θ]，接收方只知道哪个符号的概率小于阈值 θ。
- 核心困难：Meteor 式"区间公共二进制前缀"恢复在 θ > 1/2 时可能无公共前缀而解不出位。
- 解决思路（θ = 0.5 特例）：令 k = 1_0.5(D)，使 σ_k 为高概率符号、σ_{1-k} 为低概率符号；发送方取共享 PRG 随机值 r，按秘密比特 b 做变换 r' = r（b=0）或 1−r（b=1），再按 D 采样并输出 σ_{1-k}（成功嵌入 1 bit）或 σ_k（该步不嵌入、比特留到下一步）；接收方仅在观察到 σ_{1-k} 时解码，解出 b = 1[r ≥ 0.5]。
- 容量：C_{1_0.5} = D_min = D(σ_{1-k}) ≤ 0.5。
- 推广到任意 θ ∈ (0,1)：可唯一解码的随机值区间为 [0, min(θ,1−θ)] ∪ (max(θ,1−θ), 1)，中间区域视为不可解码；容量 **C_{1_θ} = min(D_min, θ, 1−θ)**，其中 D_min = min{D(σ₀), D(σ₁)}。

### 4.3 一般字母表 + 排序知识 rank

- **满秩（full rank）**：接收方知道完整降序排列 π。核心机制是 **ParitySplit** 递归：对按概率降序的列表 Σ′，按下标奇偶拆分为两组，则偶数组的总概率质量 ≥ 奇数组（可由排序知识推出，无需具体概率），于是递归地对两个子集套用 1_0.5 的 Sample/Recovery。
- 容量（Theorem/§4.3.1）：C_rank = Σ_i p_{π(i)} · count₁(bin(i))（即该符号在递归中落入低概率子集的次数 = 其下标二进制中 1 的个数）；界为 **1 − p_max ≤ C_rank ≤ H(D)**（上界即熵）。
- **部分排序知识 PRank(D) = (π̂, Σ̂)**：接收方只知道子集 Σ̂ 内符号的相对次序。方案：发送方先抽未共享的 r ~ Unif[0,1) 与 Σ̂ 的总质量 p_Σ̂ 比较——若 r > p_Σ̂ 则从 Σ\Σ̂ 按受限分布采样且不嵌入比特；否则把 D 归一化到 Σ̂ 上并调用满秩方案。接收方见到的符号 ∉ Σ̂ 时输出 ε。**Top-k 知识是其特例**。

### 4.4 实现细节

- 有状态 PRG 沿用 Meteor 的构造，以 **HMAC-DRBG** 实现，精度 **52 bit**（§5.1）。
- 方案为有状态（stateful）且即时可解码（instantaneously decodable），单符号错误不向后传播到后续符号的解码（但在 PRG 同步上仍需处理）。
- 分布失配实验中引入"固定预算 PRG 同步规则"：每个 token 的采样与恢复消耗相同数量的 PRG 输出（不足则丢弃），以隔离局部错误、避免 PRG 状态失步导致的级联错误。

## 5. 与其他方法对比

| 维度 | 本文（弱非对称） | 对称隐写（Meteor/Discop/SparSamp） | 非对称隐写（Undetectable, Zamir） |
|---|---|---|---|
| 接收方信道知识 | 仅部分知识（阈值 / 排序 / top-k） | 完整条件分布 | 无分布知识 |
| 解码依据 | 粗粒度知识（排序/阈值）+ 共享 PRG | 精确概率值 | 大量符号的假设检验聚合 |
| 容量（Llama-3-8B 实测） | 满秩 111.2 bit/resp；top-2 49.9 bit/resp | 表 1 未测（需完整分布）；表 2 失配场景下 207.9 / 304.6 / 353.6 bit/resp | 2.530 bit/resp（t=2） |
| 分布失配鲁棒性 | token 准确率 >99%，响应级 21.9%-50.6% | token 准确率 88.54%-99.10%，响应级 0.0%-1.8% | 响应级 61.8%（不依赖接收方分布） |
| 主要缺点 | 容量低于对称方案；需接收方持有某种知识 | 数值/实现差异即崩溃；需同步信道历史与相同模型 | 容量极低；需精心平衡嵌入率与解码正确性 |

## 6. 实验表现与优势

### 6.1 部分信道知识场景（§5.1, Table 1）

| 模型 | 方案 | Capacity (bit/resp.) | Emp. Entropy | Util. | Enc./Dec. Time (s/resp.) | Length | Correct. |
|---|---|---|---|---|---|---|---|
| Llama-3-8B（\|Σ\|≈128k） | Random Sampling | — | 392.681 | — | 18.798 / 18.385 | 497.273 | — |
| Llama-3-8B | Undet. (t=2) | 2.530 | 388.932 | 0.65% | 21.507 / 0.143 | 494.819 | 61.8% |
| Llama-3-8B | Rank (Full) | 111.223 | 391.070 | 28.44% | 20.662 / 19.115 | 497.441 | 100.0% |
| Llama-3-8B | Rank (Top10) | 95.067 | 386.317 | 24.61% | 19.115 / 18.699 | 492.808 | 100.0% |
| Llama-3-8B | Rank (Top5) | 83.374 | 392.303 | 21.25% | 19.215 / 18.884 | 498.172 | 100.0% |
| Llama-3-8B | Rank (Top2) | 49.855 | 390.106 | 12.78% | 18.915 / 18.753 | 495.921 | 100.0% |
| Qwen2.5-7B（\|Σ\|≈152k） | Undet. (t=2) | 2.305 | 590.922 | 0.39% | 25.384 / 0.171 | 519.993 | 61.6% |
| Qwen2.5-7B | Rank (Full) | 170.589 | 588.066 | 29.01% | 20.486 / 18.815 | 518.845 | 100.0% |
| Qwen2.5-7B | Rank (Top2) | 63.302 | 590.385 | 10.72% | 18.748 / 18.580 | 521.248 | 100.0% |

要点：rank 方案的生成文本长度与经验熵与随机采样几乎一致（保持自然生成行为）；相比非对称基线，容量提升约两个数量级（Llama 满秩 111.2 vs 2.53 bit/resp，约 44×）；**即便只知 top-2 排序也有 49.9 bit/resp（约 20×）**。计算开销上，rank 方案的编码耗时与随机采样相近（18.9-20.7 s/resp），解码耗时与随机采样同量级（因解码端也需跑模型）。

### 6.2 分布失配场景（float32 发送方 vs float16 接收方，§5.2, Table 2）

| 模型 | 类型 | 方案 | Embed. (bit/resp.) | Util. | Token Acc. | Resp. Acc. | ED |
|---|---|---|---|---|---|---|---|
| Llama-3-8B | 对称 | Meteor (16-bit) | 207.9 | 53.9% | 99.10% | 1.8% | 7.439 |
| Llama-3-8B | 对称 | Discop (Huffman) | 304.6 | 78.6% | 88.54% | 0.9% | 40.848 |
| Llama-3-8B | 对称 | SparSamp (32-bit) | 353.6 | 91.2% | — | 0.1% | 218.029 |
| Llama-3-8B | 非对称 | Undet. (t=2) | 2.5 | 0.65% | — | 61.8% | — |
| Llama-3-8B | **弱非对称** | Rank (Full) | 111.6 | 28.5% | 99.69% | 21.9% | 1.888 |
| Llama-3-8B | **弱非对称** | Rank (Top10) | 96.0 | 24.7% | 99.81% | 39.3% | 0.984 |
| Llama-3-8B | **弱非对称** | Rank (Top5) | 82.5 | 21.3% | 99.85% | 48.3% | 0.775 |
| Llama-3-8B | **弱非对称** | Rank (Top2) | 49.6 | 12.7% | 99.86% | 50.6% | 0.668 |
| Qwen2.5-7B | 对称 | Meteor | 311.8 | 54.0% | 98.72% | 0.3% | 10.535 |
| Qwen2.5-7B | 对称 | Discop (Huffman) | 481.3 | 81.9% | 79.04% | 0.0% | 83.220 |
| Qwen2.5-7B | 对称 | SparSamp | 550.1 | 92.0% | — | 0.0% | 399.092 |
| Qwen2.5-7B | **弱非对称** | Rank (Full) | 171.7 | 29.2% | 99.48% | 9.2% | 3.367 |
| Qwen2.5-7B | **弱非对称** | Rank (Top2) | 62.8 | 10.7% | 99.83% | 40.2% | 0.875 |

要点：对称方案在精度失配下 token 准确率降到 79.04%-99.10%、响应级成功率近 0（SparSamp 0.0%-0.1%，ED 高达 218.029-399.092）；rank 方案 token 准确率全部 >99%（99.48%-99.86%），ED 仅 0.668-3.367，且响应级仍保有 9.2%-50.6%（**top-k 越少越鲁棒**，Top2 达 50.6%）。容量上 rank 方案仍显著高于非对称基线（49.6-171.7 vs 2.3-2.5 bit/resp）。

### 6.3 实验配置

| 项 | 设置 |
|---|---|
| 模型 | Meta-Llama-3-8B-Instruct、Qwen2.5-7B-Instruct |
| 硬件 | 单卡 RTX 5880 Ada，48 GB VRAM |
| 样本量 | 每个配置生成 1,000 条响应；hiddentext 与密钥逐条重采样 |
| Prompt / 解码粒度 | 固定 prompt "Tell me something about steganography"；解码在 token 级进行（不还原为文本） |
| PRG | HMAC-DRBG，52 bit 精度（与 Meteor 同构造） |
| Baseline | 非对称：Undetectable Steganography [26]（t=2，官方实现，仅做运行时优化）；随机采样（torch.multinomial）；失配实验另加对称方案 Meteor [17]、Discop [11]、SparSamp [24] |

### 6.4 优势

- 首次证明"部分信道知识可被显式利用"存在非平凡方案（此前仅有"忽略该知识、退化为非对称方案"的平凡做法）；
- 给出容量闭式表达与界（C_{1_θ} = min(D_min,θ,1−θ)；1−p_max ≤ C_rank ≤ H(D)），理论完整；
- 在精度失配这一工程常见场景下显著优于对称方案，提出"以粗粒度知识换取数值鲁棒性"的隐写设计视角。

## 7. 学习与应用

- **对审查规避/隐蔽通信**：rank 类方案提供了"接收方算力受限（只能调 API 看 top-k）也能解码"的实用选择，容量与鲁棒性可按 top-k 灵活权衡（top-2 最鲁棒、满秩容量最高）；
- **对流量分析研究**：本文属内容层隐写（文本生成），与包级流量分析不同层次，但它揭示的"分布失配/数值精度导致信道不稳定"问题，与加密流量分类中的跨域迁移、量化部署问题在方法论上同构——可用作"稳健表征优于精确概率"的跨域类比；
- **可迁移技巧**：(1) ParitySplit 式"用排序知识做递归奇偶切分、以二进制的 1 计数刻画容量"是可复用的组合构造；(2) "粗粒度知识对扰动更稳定"这一原则可迁移到需要跨设备一致性保证的协议设计；
- **对防御方**：即便检测者拿到了模型与密钥但设备/精度不同，也未必能稳定解码——这提示隐写检测方需要考虑分布扰动带来的检测退化。

## 8. 总结

论文提出并形式化了**弱非对称隐写**——发送方拥有完整条件分布、接收方仅拥有部分信道知识（二元字母表的阈值知识 1_θ、一般字母表的满秩/部分排序 PRK）。作者给出可证明安全的构造（阈值方案容量 min(D_min,θ,1−θ)；rank 方案容量 Σp·count₁(bin(i))，界 1−p_max ≤ C_rank ≤ H(D)），并在 Llama-3-8B / Qwen2.5-7B 文本隐写上验证：满秩知识下 111.2-170.6 bit/resp、利用率 28.4%-29.0%；top-2 知识仍有 49.9-63.3 bit/resp；在 float32→float16 精度失配场景中 token 级准确率 >99%、ED 低至 0.668，而同条件下的对称方案响应级成功率几乎为 0。

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[censorship-circumvention]] — 隐写/隐蔽通信是审查规避的重要技术路线；论文开篇即以监控与内容审查的普遍化为动机（引言引 [12,22]）。
- [[encrypted-traffic-analysis]] — 论文的隐写信道建立在正常通信内容之上，与本库的加密流量分析构成"生成侧 vs 检测侧"的呼应关系。

### 9.2 相关方法

- [[transformer]] — 论文以预训练 Transformer 语言模型（Llama-3-8B-Instruct、Qwen2.5-7B-Instruct）实例化 covertext channel oracle（条件分布提供者），属"以 LLM 分布为载体的隐写"路线（与库内 ANStega 笔记同类）。

### 9.3 相关任务

- 白名单任务页（`website-fingerprinting`、`encrypted-traffic-classification`、`malicious-traffic-detection` 等）均不覆盖"可证明安全隐写 / 隐蔽信道构造"，故本节不链接。

### 9.4 相关综述

- 白名单综述页（`survey-encrypted-traffic-analysis`、`survey-few-shot-learning`、`survey-malicious-traffic-detection`、`survey-traffic-foundation-model`、`survey-website-fingerprinting`）均以流量分析为目标，不覆盖隐写理论，故本节不链接。

### 9.5 对比表

- `method-comparison-table`：本文提出的是密码学/信息论的隐写构造（虽用到 LLM 作为信道），其对比对象为 Meteor/Discop/SparSamp/Undetectable 等隐写方案，与该表覆盖的流量分析方法族不符，故不链接。
- `dataset-comparison-table`：本文未使用或发布公开数据集，故不链接。
- `open-source-registry`：论文在 Open Science 节给出 artifact（Zenodo 10.5281/zenodo.20428322），但该登记页面向流量分析工具，隐写方案实现不在其覆盖范围，故不链接。

### 9.6 相关研究前沿

- 本库 6 条研究前沿（`multimodal-fusion-strategy`、`payload-learnability`、`pretraining-necessity`、`representation-vs-shallow`、`tokenization-optimal`、`wf-attack-defense-limit`）均以加密流量分类为核心，与本文的隐写容量/鲁棒性权衡无对应，故不链接。

### 9.7 相关论文笔记

- [[2020-CCS-Censored_Planet__An_Internet-wide__Longitudinal_Censorship_Observatory]] — 论文引言在论证"监控与内容审查普遍化"时引用了 Censored Planet（原文参考文献 [22]）。

## 10. 证据记录

| 编号 | 论断 | 证据位置 |
|---|---|---|
| E1 | 知识函数定义 f: X → Y；f_id 对应完整知识、常数函数对应无知识，本文研究非退化中间情形 | §3.3 |
| E2 | 阈值知识方案容量 C_{1_θ} = min(D_min, θ, 1−θ)；θ=0.5 特例为 D_min | §4.2.1-§4.2.2 |
| E3 | rank 方案容量 C_rank = Σ p_{π(i)}·count₁(bin(i))，且 1−p_max ≤ C_rank ≤ H(D) | §4.3.1 |
| E4 | ParitySplit：按概率降序列表的奇偶下标切分，偶数组概率质量 ≥ 奇数组（仅凭排序知识可知） | §4.3.1, Algorithm 8 |
| E5 | 部分排序知识 PRank = (π̂, Σ̂)，Top-k 为其特例；符号落在 Σ̂ 外时不嵌入 | §4.3.2, Algorithm 11/12 |
| E6 | Llama-3-8B：Rank(Full) 111.223 bit/resp、Util. 28.44%、Correct. 100%；Rank(Top2) 49.855 bit/resp、12.78% | §5.1, Table 1 |
| E7 | Qwen2.5-7B：Rank(Full) 170.589 bit/resp、29.01%；Rank(Top2) 63.302 bit/resp、10.72% | §5.1, Table 1 |
| E8 | 非对称基线 Undet.(t=2) 仅 2.530（Llama）/2.305（Qwen）bit/resp，利用率 0.65%/0.39% | §5.1, Table 1 |
| E9 | 失真失配下对称方案 Resp. Acc. 0.0%-1.8%，SparSamp ED 218.029（Llama）/399.092（Qwen） | §5.2, Table 2 |
| E10 | 失真失配下 rank 方案 Token Acc. 99.48%-99.86%、ED 0.668-3.367、Resp. Acc. 9.2%-50.6% | §5.2, Table 2 |
| E11 | 实验环境：RTX 5880 Ada 48GB，每配置 1000 条响应，HMAC-DRBG 52-bit 精度 | §5.1 Setup |
| E12 | artifact 公开于 Zenodo（10.5281/zenodo.20428322），含 rank 方案实现与 §5 实验脚本 | Open Science |

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-USENIX-From_Symmetry_toward_Weak_Asymmetry__Secure_Steganography_under_the_Receiver's_Partial_Channel_Knowledge.pdf
- MinerU Markdown：02-parsed-markdown/2026-USENIX-From_Symmetry_toward_Weak_Asymmetry__Secure_Steganography_under_the_Receiver's_Partial_Channel_Knowledge.md

## 12. 后续问题

1. 论文的 Security 定义针对 chosen hiddentext attack，但未给出语言模型信道下的具体不可区分性实验（如检测器 AUC）——实践中 rank 方案的统计可检测性如何？
2. 阈值知识 1_θ 的构造只在二元字母表上给出；能否推广到一般字母表下的多阈值/分桶知识？
3. 部分 rank 知识只覆盖"子集内相对次序已知"这一形式；若接收方的排序是**含噪**的（如 top-k 边界附近的次序可能翻转），方案是否仍可证明安全、容量如何退化？
4. 论文提到 rank 知识可"由重复采样与统计检验推断"，但未量化推断所需样本量与错误率对容量的影响。
5. 固定预算 PRG 同步规则是实验性工程手段（§5.2），其安全性影响（是否引入可检测偏差）未在正文中形式化分析。

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

论文先把可证明安全隐写的接收方能力写成一条连续谱：对称方案知道完整分布，无知识方案只能做低容量统计恢复，而现实 API、算力和数值精度往往处在两者之间。作者把这个“中间地带”正式命名为弱非对称隐写，并用知识函数 f 把“部分知道什么”从实现细节提升为可研究对象。第一条转折是二元阈值知识的可逆构造，第二条转折是把它推广到任意字母表的概率排序，通过 ParitySplit 在只知道 rank 的情况下递归分配比特。实验随后不只报容量，还把精度失配作为现实压力测试：排序知识牺牲部分容量，却显著提高 token 和 response 级稳定性。论文最终把贡献定位为一种可证明的安全—容量—知识三方折中，而不是单纯的 LLM 隐写实现。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract/Introduction | 建立对称/无知识两端与现实中间态 | 问题提出 | 接收方能力不是二元变量 |
| Related Work/Model | 定义知识函数、正确性与 chosen-hiddentext 安全 | 理论锚定 | “部分知识”成为协议参数 |
| Threshold construction | 在二元情形证明最小容量和可逆规则 | 低维原型 | 中间区间不解码、容量受 min(D_min,θ,1−θ) 限制 |
| Rank construction | 用 ParitySplit 递归推广到一般字母表与 Top-k | 核心方法 | 从概率值转为排序结构 |
| Experiments | 先测容量，再测 float32/float16 失配 | 实用性兑现 | top-k 越少，鲁棒性越强但容量降低 |
| Discussion/Conclusion | 讨论排序推断、噪声 rank、PRG 同步与实际部署 | 边界管理 | 方案仍依赖部分知识的可靠获得 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 设定缺口 | 既有隐写只讨论完整知识或无知识 | 定义弱非对称知识函数 f | §1, §3 |
| 构造缺口 | 需要利用粗粒度信息而不重新获取概率 | 阈值方案 + ParitySplit rank 方案 | §4.2–4.3 |
| 工程缺口 | 同一模型不同精度会使逐概率解码崩溃 | float32→float16 mismatch 实验 | §5.2, Table 2 |
| 指标缺口 | 容量与鲁棒性并非同一个指标 | 同时报告 bit/resp、utilization、token/response accuracy、ED | §5.1–5.2 |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| Rank Full/Top-k 容量 | 展示知识量与容量的连续折中 | 证明弱非对称不是退化方案 |
| Undetectable baseline | 提供无知识低容量参照 | 量化部分知识的增益 |
| float mismatch | 模拟真实部署的模型精度差异 | 检验排序知识的鲁棒性 |
| 对称方案对照 | 展示精确概率方法的高容量但低容错 | 明确安全—容量—同步权衡 |
| 计算时间/长度 | 检查自然度与模型开销 | 排除以异常文本长度换容量的解释 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 设定命名 | 先命名连续谱中的“弱非对称”再给形式化定义 | 对被忽略的中间能力建立稳定术语 |
| 理论—工程衔接 | 用闭式容量界连接算法，再用精度失配连接部署 | 每个定理配一个现实扰动实验 |
| 对照选择 | 同时放完整知识、Top-k、无知识和对称方法 | 比较能力等级，而不是只比较单个模型 |
| 结果表达 | 将“利用率高”与“原始容量高”明确分开 | 避免把单一指标写成全面领先 |

## 14. 证据边界与复现清单

1. **安全定义边界**：论文的计算不可区分性以发送方拥有完整 D、接收方拥有固定 f(D)、共享 PRG/密钥和 chosen-hiddentext 安全游戏为前提；不能泛化为接收方 rank 含噪、知识随时间漂移或服务端随机性不独立的情形。
2. **容量口径**：Rank Full/Top-k 的 bit/response、utilization、token accuracy、response accuracy 和 ED 衡量不同属性；尤其失配实验中 token accuracy >99% 不等于整段 response 一定成功解码。
3. **实验边界**：仅测 Llama-3-8B-Instruct、Qwen2.5-7B-Instruct、固定 prompt 和 1,000 条响应/配置；不代表其他 LLM、提示、采样温度或长上下文。
4. **分布失配边界**：float32→float16 是单一精度场景；论文未测跨模型 rank、top-k 边界翻转、网络 API 非确定性或 rank 推断的样本成本。
5. **复现依赖**：HMAC-DRBG 52-bit 精度、token 级同步、模型版本、top-k 集合和固定 prompt 必须完全记录；Zenodo 10.5281/zenodo.20428322 是 rank 方案与实验 artifact，不是论文 DOI。
6. **知识库边界**：本文不更新流量分类主知识层；其对加密流量研究的关联仅限于“分布失配下粗粒度表示更稳定”的方法类比。

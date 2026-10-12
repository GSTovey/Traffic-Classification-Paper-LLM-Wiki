---
type: paper
title_original: "Provable Secure Steganography Based on Adaptive Dynamic Sampling"
title_cn: "基于自适应动态采样的可证明安全隐写"
authors: [Kaiyi Pang, Minhao Bai]
year: 2026
venue: "USENIX Security 2026"
doi: "unknown"
url: "https://www.usenix.org/conference/usenixsecurity26/presentation/pang-kaiyi"
pdf: "00-inbox/PDFs/2026-USENIX-Provable_Secure_Steganography_Based_on_Adaptive_Dynamic_Sampling.pdf"
mineru_md: "02-parsed-markdown/2026-USENIX-Provable_Secure_Steganography_Based_on_Adaptive_Dynamic_Sampling.md"
status: deep-analyzed
reading_level: L3
research_area: ["provable steganography", "language-model sampling", "covert communication"]
task: ["seed-only steganographic encoding", "distribution-preserving sampling", "covertext imperceptibility"]
method: ["adaptive dynamic sampling", "collision-set expansion", "PRG-based mapping", "game-based security proof"]
dataset: ["WILD QA dataset", "XHS simulated Chinese social-media corpus", "MISTRAL3/QWEN2/LLAMA3 models"]
code: "https://zenodo.org/records/18152848(artifact 归档,非论文 DOI)"
relevance: low
created: "2026-09-19"
updated: "2026-10-10"
---

# Provable Secure Steganography Based on Adaptive Dynamic Sampling

> **L3 深度分析笔记**：基于正文 §1–§7、Algorithms 1–10、Tables 1–3、Ethical/Open Science 章节与 MinerU 原始解析稿交叉核对。本文的安全结论依赖 seed-taking API 的可复现采样、PRG 安全与 i.i.d. 采样假设；容量、利用率、SR 和隐写分析 F1 不应混为单一“性能”。

## 0. 论文基础信息

| 项 | 内容 |
|---|---|
| 标题(原文) | Provable Secure Steganography Based on Adaptive Dynamic Sampling |
| 标题(中文) | 基于自适应动态采样的可证明安全隐写 |
| 作者 | Kaiyi Pang, Minhao Bai |
| 机构 | Tsinghua University(清华大学;解析稿署名) |
| 发表会议 | USENIX Security 2026 |
| 年份 | 2026 |
| DOI | unknown(解析稿未给出论文 DOI) |
| URL | https://www.usenix.org/conference/usenixsecurity26/presentation/pang-kaiyi |
| PDF | 00-inbox/PDFs/2026-USENIX-Provable_Secure_Steganography_Based_on_Adaptive_Dynamic_Sampling.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-USENIX-Provable_Secure_Steganography_Based_on_Adaptive_Dynamic_Sampling.md |
| 代码/制品 | https://zenodo.org/records/18152848(artifact 归档,非论文 DOI) |
| 资助 | NSFC U2336208(解析稿致谢) |
| 阅读层级 | L2 |
| 主题相关性 | low(属隐写/信息隐藏与 LLM 采样,与 KB 流量分析主题无实质交集) |

## 1. 一句话总结

针对"语言模型仅暴露接受种子的采样 API(seed-taking API)"这一受限场景,提出自适应动态采样(ADS):用 PRG 由种子生成采样种子并维护规模有界于 [2^{N-1}, 2^N] 的动态碰撞集合,据消息比特选择输出 token,从而在**不接触显式分布**的前提下实现可证明安全隐写,效率与容量与需要显式分布的 PSS 方法相当。

## 2. 摘要翻译

### 2.1 摘要原文(节选)

> The security of private communication is increasingly at risk due to widespread surveillance. Steganography, a technique for embedding secret messages within innocuous carriers, enables covert communication over monitored channels. Provably Secure Steganography (PSS), which ensures computational indistinguishability between the normal model output and steganography output, is the state-of-the-art in this field. However, current PSS methods often require obtaining the explicit distributions of the model. In this paper, we propose a provably secure steganography scheme that only requires a model API that accepts a seed as input. Our core mechanism involves sampling a candidate set of tokens and constructing a map from possible message bit strings to these tokens. The output token is selected by applying this mapping to the real secret message, which provably preserves the original model's distribution. To ensure correct decoding, we address collision cases, where multiple candidate messages map to the same token, by maintaining and strategically expanding a dynamic collision set within a bounded size range. Extensive evaluations of three real-world datasets and three large language models demonstrate that our sampling-based method is comparable with existing PSS methods in efficiency and capacity.

(以上为解析稿 Abstract 全段抄录)

### 2.2 中文完整翻译

由于监控的普遍存在,私密通信的安全性日益受到威胁。隐写(Steganography)是一种把秘密消息嵌入无害载体中的技术,可在被监控的信道上实现隐蔽通信。可证明安全隐写(PSS)保证正常模型输出与隐写输出之间具有计算不可区分性,是该领域的最先进方向。然而,现有 PSS 方法通常需要获取模型的显式分布。本文提出一种可证明安全的隐写方案,它仅需要一个**接受种子作为输入的模型 API**。我们的核心机制是:采样一个候选 token 集合,并构造"可能的消息比特串 → 这些 token"的映射;把该映射作用于真实秘密消息,即选出实际输出的 token,而这一过程**可证明地保持原始模型的分布**。为保证解码正确,我们处理了碰撞情况(多个候选消息映射到同一 token):在一个有界区间内维护并策略性地扩张一个**动态碰撞集合**。对三个真实数据集与三个大语言模型的广泛评测表明,我们基于采样的方法在效率与容量上与现有 PSS 方法相当。

## 3. 方法动机

### 3.1 研究背景

- 可证明安全隐写(PSS)要求嵌入过程与模型分布**不可区分**,常见构造(METEOR、DISCOP、SparSamp、iMEC)都建立在"可以查询模型的概率分布或累积分布"这一假设上。
- 现实中的 LLM 服务(如闭源 API)往往**只暴露采样接口**,且接口内部使用服务端不可见的随机种子;客户端只能提供一个 seed 并收到一个 token。

### 3.2 现有方法的不足(据 §2.3–§2.6)

| 现有方案 | 原理 | 局限 |
|---|---|---|
| METEOR | 逐步重加密嵌入比特;收集若干 token 直到熵足够 | 每次嵌入后重加密会截断编码过程、浪费每步末端的熵;LLM 分布熵很低时可能根本无公共前缀,导致容量低。复杂度 O(\|V\|),重排序版 O(2^{\|H(P)\|}\|V\|) |
| DISCOP(分布副本) | 用分布的多个副本,按 r 与 r+k/2^n 是否指向不同 token 嵌入 n bit | 副本间重叠严重,嵌入率受最小熵渐近限制;哈夫曼树变体复杂度 O(\|V\| log \|V\|) |
| iMEC(MEC) | 求均匀 n-bit 码字与模型分布的**最小熵耦合**矩阵 | MEC 是 NP-hard;最优算法只能得到与 MEC 相差 1 bit 以内的联合分布,持续损失容量;且依赖**概率解码**,无法给出确定性的解码错误率保证(实测 SR 不稳定) |
| SparSamp | 在 DISCOP 基础上增大采样区间间隔并累积熵 | 论文对"O(1) 复杂度"的说法持保留态度,认为实际有效复杂度仍取决于分块大小 B;且收发双方仍须共享同一模型分布,定长嵌入也未充分利用载体熵 |

### 3.3 本文思路

把"受限采样接口"从障碍转为设计前提:让客户端选一个种子,借助 PRG 把种子的随机性扩张为一个**碰撞集合(collision set)** CS,其大小落在 [2^{N-1}, 2^N];消息的 N bit 决定从 CS 中取哪个元素作为输出 token 的选取依据,从而在不接触真实分布的情况下实现可证明安全的嵌入。核心创新是**自适应**:CS 的规模随当前可用的采样预算动态调整。

### 3.4 问题发现路径

| 阶段 | 内容 |
|---|---|
| 现象观察 | 实际 LLM 服务不暴露概率分布,只暴露 seed-taking 的采样接口 |
| 痛点提炼 | 现有 PSS 方案假设可查询分布,在真实 API 下无法直接部署 |
| 问题转化 | 把"隐写嵌入"转化为"在 PRG 扩张出的碰撞集合中做索引选择"的采样预算优化问题 |
| 文献定位 | 位于可证明安全隐写(METEOR→DISCOP→SparSamp→iMEC)与 LLM 水印/信息隐藏交叉脉络 |

### 3.5 科学假设

- 假设:仅用 seed-taking 采样接口,通过扩大碰撞集合的规模(至 2^N 量级)即可让"消息索引选择"与"原始随机采样"分布不可区分,从而在受限接口下实现可证明安全隐写,并且容量不必显著低于需要分布访问的方案。
- 验证结果:安全性由 G0–G3 的博弈序列证明;实验中 SR = 1.0000(所有设置),TS-CSW 隐写分析 F1 ≈ 49.66–50.81%(接近随机),载荷利用率在全部 6 个设置中最高——假设得到支持。

## 4. 方法设计

### 4.1 总体架构与两条核心洞察

- **接口模型**:模型只暴露"接受 seed 作为输入"的 API,输出 token 样本;客户端**不能读取显式分布**。
- **洞察一(采样)** 从 API 采样多个候选 token 并均匀地选出其一,输出分布与模型自身预测分布相同;由此可构造 F: {0,1}^N → V,把 N 比特消息串映射到采样得到的 token,再用真实秘密消息去取映射结果。
- **洞察二(碰撞的处理)** 不同消息串映射到同一 token 即为碰撞。碰撞**不影响嵌入、只影响解码**(METEOR 因此退化为提取共享前缀)。ADS 不回避碰撞,而是把与真实消息碰撞的所有串**记入列表**,后续按列表元素个数采样,列表通常在若干步内收缩到 1。
- **有界扩张**:为避免列表长期偏小导致容量损失,当 |CS| < 2^{N-1} 时把列表中每个元素追加 0 与 1(规模翻倍),直至落入 **[2^{N-1}, 2^N]**;若 |CS| ≥ 2^{N-1} 则不扩张、本步不嵌入新比特,仅多采 |CS| 个样本以排除更多假消息。经过 L = ⌊2^N/|CS|⌋ 次扩张后本轮多嵌入 L 比特。
- **参数**:N 为控制碰撞集合上限 2^N 的新参数;实验中将每个时间步可扩张到的最大集合设为 2^9。

### 4.2 编解码流程(Algorithms 1/2)

- **初始步**:CS 置为 {0,1}^N(即全部 N 比特前缀)。
- **编码(Algorithm 1)**:对 CS 中每个元素 e,用 PRG 由密钥 k 生成 seed,调用模型 API 得到样本 t,令 F(e) := t;取 s_i = F(m_{1:l}) 作为下一个 stego token;随后把 CS 更新为 {e ∈ CS | F(e) = s_i},再按上述规则决定是否扩张。
- **解码(Algorithm 2)**:重复采样过程,直到集合收缩为单一元素,返回 CS 中所有元素的共享前缀;文本结束时提取碰撞串的共享前缀。
- **自适应体现在**:采样次数随候选消息数(即碰撞集合规模)动态变化,N 与扩张倍数 L 均随当前 |CS| 决定。

### 4.3 复杂度分析(Table 1)

| 方案 | 模式 | 复杂度 | 解码正确性 |
|---|---|---|---|
| METEOR | Stream | O(\|V\|) | 100% |
| METEOR(R.) | Stream | O(2^{\|H(P)\|}\|V\|) | 100% |
| DISCOP | Stream | O(\|V\|) | 100% |
| DISCOP(R.) | Stream | O(\|V\| log \|V\|) | 100% |
| iMEC | Block | O(2^B\|V\|) | Unstable |
| SparSamp | Block | O(2^B) | 100% |
| **Ours (ADS)** | **Stream** | **O(2^N)** | **100%** |

Table 1 表注给出参数典型范围:词表大小 |V| 对 LLM 通常为 2^17 ~ 2^19;MISTRAL 的模型分布熵 H(P) 约 0.91 ~ 1.05;分块大小 B 可取 8 ~ 64;本方案的 2^N 可取 2^2 ~ 2^15。

ADS 的复杂度与词表大小 |V| **无关**,只随碰撞集合规模 2^N 增长;相比之下 iMEC/SparSamp 的采样开销随分块大小 B 呈 2^B 增长。另需注意 ADS 属 **Stream** 模式,而 iMEC/SparSamp 为 Block 模式。

论文对 SparSamp 的 O(1) 复杂度声明持保留态度:§2.6 指出 SparSamp 虽声称 O(1),但实践中其有效复杂度可能仍取决于分块大小 B;此外 SparSamp 仍要求收发双方共享同一模型分布,且因定长嵌入未能充分利用载体文本的熵。

### 4.4 安全性证明(G0–G3)

| 博弈 | 含义 |
|---|---|
| G0 | Steganography-Sampler:对 CS 中每个元素由 PRG_k 生成 seed 并采样 |
| G1 | 从 CS 中**均匀**取一个样本作为输出;因采样独立同分布,Pr[G1→a] = Pr[G0→a] |
| G2 | 用**真随机 seed**替换 PRG_k(·);由 PRG 的定义,对任意 p.p.t. 敌手有 ≤ negl(λ) 的区分优势(式 5),故 G1 ≈_c G2 |
| G3 | 利用同分布采样的 **i.i.d. 性质**:从多个样本中随机取一个,等价于直接从模型采样,故 G2 = G3 |

安全性依赖两个假设:伪随机生成器存在,以及同分布采样具有 i.i.d. 性质。

- 定义 **SR(Success Rate,解码正确率)**:比特级解码成功率;ADS 在所有设置中 SR = 1.0000。

### 4.5 采样预算的关键作用

- METEOR 的窗口长度常设为 32 或 64;若直接套用到"仅有模型 API"的场景,意味着需要采样 **2^32 或更多次**,原文明确称其"不可行"。
- ADS 相反:可以只采样 **2^4 或更少次**并仍保持安全性(§1 对 METEOR 的三点差异之第一点)。这一缩减来自碰撞集合的有界扩张机制,而非增加接口调用次数。

### 4.6 实现与开销

- 硬件:2×NVIDIA A5000(32GB 显存)与 24×Intel Xeon w5-3423 CPU。
- 生成参数:每个测试生成 1,000 个样本,top-p = 1.0,base temperature = 1.0,最大生成长度 500。
- 单 token 处理时间 **< 100 ms**;实现为 Python,作者指出把采样组件换成 C/C++ 可显著提速。

## 5. 与其他方法对比

### 5.1 与 METEOR/DISCOP 对比

两者需要完整的概率/累积分布查询,在只暴露采样接口的部署中不可用;ADS 仅需 seed-taking 接口,且复杂度不随词表规模增长。

### 5.2 与 SparSamp 对比

SparSamp 的采样开销为 O(2^B)、每步需约 2^B 次采样;ADS 把所需预算压缩到 2^4 量级,同时载荷利用率在全部 6 个设置中更高(如 MISTRAL3/WILD:0.9137 vs 0.8411)。

### 5.3 与 iMEC 对比

iMEC 复杂度 O(2^B|V|) 且采样安全率不足 1(实验为 0.8432–0.9987);ADS 的 SR 恒为 1.0000,即在所有测试设置中都能满足安全条件。

### 5.4 本文的独特性

同时满足:(a) 仅依赖 seed-taking 采样接口;(b) 复杂度与词表规模无关;(c) 具备形式化安全性证明;(d) 在真实 7B 级模型上给出容量与安全性的实证。

## 6. 实验表现与优势

### 6.1 实验设置

| 项 | 内容 |
|---|---|
| 模型 | MISTRAL3、QWEN2、LLAMA3(均约 7B) |
| 数据集 | WILD(QA 数据集)、XHS(模拟中文社交媒体文本,风格非正式、碎片化)以及 uniform 分布 |
| 采样规模 | 每个设置 1,000 个样本 |
| 生成参数 | top-p = 1.0,temperature = 1.0,max 500 tokens |
| 碰撞集合上限 | 每个时间步可扩张到的最大碰撞集合 2^N = **2^9**(Table 2/Table 3 表注) |
| 硬件 | 2×NVIDIA A5000 |

基线包括 Random Sampling、METEOR、DISCOP(R.)(重排序版)、DISCOP、SparSamp、iMEC;评测维度为 Capacity(Entropy bit/token、Embed bit/token、Utilization)、Time、Linguistic Quality(PPL、Dist2–Dist4)、Imperceptibility(TS-CSW F1)、Correctness(SR)。

### 6.2 WILD 数据集上的容量与利用率(Table 2)

| 模型 | ADS embed / util. | SparSamp embed / util. | DISCOP(R.) embed / util. | iMEC embed / util. |
|---|---|---|---|---|
| MISTRAL | **0.8964 / 0.9137** | 0.8562 / 0.8411 | 0.7683 / 0.7930 | 0.7345 / 0.6923 |
| QWEN | 1.8789 / **0.9103** | 1.8905 / 0.9052 | **1.9093** / 0.8866 | 1.6174 / 0.7466 |
| LLAMA3 | **0.6572 / 0.9352** | 0.5713 / 0.8183 | 0.5221 / 0.7425 | 0.6057 / 0.7218 |

**关键限定(务必区分)**:ADS 的**利用率(utilization)**在全部 6 个设置中最高;但**原始容量(Embed bit/token)**仅在 3/6 个设置中最高——WILD 上 QWEN 的 DISCOP(R.)(1.9093)与 SparSamp(1.8905)均高于 ADS(1.8789)。

### 6.3 XHS 数据集上的容量与利用率(Table 3)

| 模型 | ADS embed / util. | SparSamp embed / util. | DISCOP(R.) embed / util. |
|---|---|---|---|
| MISTRAL | 2.0378 / **0.9308** | **2.0893** / 0.9029 | 2.0416 / 0.8825 |
| QWEN | **3.4928 / 0.9393** | 3.4095 / 0.9304 | 3.2606 / 0.9118 |
| LLAMA3 | 1.2560 / **0.9223** | **1.4206** / 0.9105 | 1.2137 / 0.8243 |

XHS 上 ADS 的最高容量为 QWEN 的 **3.4928 bit/token**(同时也是该设置的容量冠军),利用率 0.9393 为全表最高。

### 6.4 安全性实践(采样安全率 SR)

| 方案 | WILD 上的 SR | XHS 上的 SR |
|---|---|---|
| iMEC | 0.8825 / 0.9952 / 0.8432(MISTRAL/QWEN/LLAMA3) | 0.9847 / 0.9987 / 0.8631 |
| **ADS** | **1.0000 / 1.0000 / 1.0000** | **1.0000 / 1.0000 / 1.0000** |

论文表述:ADS 在**所有设置**中 SR 均为 1.0000,即在其实验范围内实现比特级确定性可逆解码;相比之下 iMEC 表现出明显的不稳定性,与其解码的概率性质一致。

### 6.5 抗隐写分析(TS-CSW)

| 设置 | ADS 的 TS-CSW F1(↓) |
|---|---|
| WILD MISTRAL / QWEN / LLAMA3 | 50.18% / 49.83% / 49.73% |
| XHS MISTRAL / QWEN / LLAMA3 | 50.81% / 49.83% / 49.66% |

全部落在 **49.66%–50.81%** 区间,即接近随机猜测水平(50%),说明其输出与正常模型生成在统计上难以区分。

### 6.6 效率

单 token 处理时间 **< 100 ms**;解析稿 §5 给出更精确的数字——每步采样数设为 **2^14** 时,每个 stego token 约需 **0.02–0.04 秒**。在 WILD 上与现有 PSS 算法处于同一时间量级,可快于 DISCOP 的重排序版本;在 XHS 上接近标准随机采样,与 METEOR、DISCOP(非重排序版)相当。iMEC 明显更慢(原实现基于 GPT-2,而 LLM 词表约 50K,远大于 GPT-2)。论文指出实现为 Python,若把采样组件改为 C/C++ 可显著提速。

### 6.7 局限(§5 原文自述)

- **API 层面的种子控制不稳定**:Qwen-max、Qwen-Plus、gpt-4-1106-preview、gpt-3.5-turbo-1106 等已暴露 seed 参数,Midjourney、Stable Diffusion 等图像系统亦支持;但 OpenAI、Qwen 等厂商仅承诺"尽力"对固定 seed 与参数做确定性采样,**明确说明不严格保证确定性**。因此纯依赖第三方黑盒服务时方案的长期稳健性受限。作者认为**最可靠的部署方式是自建/自控模型 API**(私有或云托管),此时也可与开源白盒模型完全兼容(seed 与采样例程均可精确指定)。
- **图像/视频模态不实用**:虽然只要支持 seed 采样即可套用,但生成一张图像可能需要数分钟,实时场景不可行;方法最适合自回归语言模型。
- **采样速度**:本文不以采样加速为目标;每步采样数增大时单 token 时间自然增长,**过大的 N 会带来明显计算开销**;作者把更高效的采样策略或专用隐写算法列为未来方向,并考虑改写为 C/C++。

## 7. 学习与应用

### 7.1 对受限接口的利用思路

本文的核心方法论是**把接口限制转化为可利用的随机性来源**:受限的 seed-taking 接口反而提供了一个可被双方复现的随机通道,这是"在约束下设计"的典型范式。

### 7.2 容量指标的双维度理解

ADS 的实验揭示了 **raw capacity 与 utilization 的分离**:一个方案可以在利用率上全面领先而在绝对容量上并非处处最优。评估隐写/编码类方法时应同时报告二者。

### 7.3 与 KB 主题的关系

本文属隐写与信息隐藏,与知识库的加密流量分类、网站指纹、恶意流量检测主题无实质交集。其"以不可区分性为目标、以统计检测器(隐写分析)为评估手段"的范式,与网站指纹攻防(wf-attack-defense-limit)在**方法论层面**有类比价值:两者都在"分布不可区分"与"检测器可分辨"之间博弈。

### 7.4 与审查规避的可能关联(仅笔记作者的观察,非论文内容)

隐写式隐蔽通信在概念上可作为审查规避通信通道的一类组件,但**本文完全未讨论审查规避**;笔记亦不为此建立 wikilink(见 §9.1 的核对说明)。

### 7.5 可复用性评估

Artifact 已归档于 Zenodo(records/18152848);方法依赖 seed-taking 采样接口的确定性保证,迁移到真实闭源 API 时需先验证该前提。

## 8. 总结

### 8.1 核心思想(≤20 字)

PRG 扩张碰撞集合,在种子采样接口下安全嵌入。

### 8.2 速记版 Pipeline

1. 客户端选随机种子,调用带种子的采样接口;
2. 用 PRG 扩张出候选 token 集合(碰撞集合 CS);
3. 自适应调整 CS 规模至 [2^{N-1}, 2^N],匹配当前采样预算;
4. 按消息的 N bit 在集合中选择输出 token,推进上下文;
5. 以不可区分性证明 + 隐写分析(TS-CSW)+ SR 指标评估安全性。

## 9. Obsidian 知识链接

### 9.1 概念页

本论文不触及 kb_reference C 节白名单中的任何 concepts 页面。已核对 `censorship-circumvention` 概念页的定义与覆盖范围(审查测量 / 规避工具设计 / 检测与对抗,及流量混淆、Web 协议隧道、未识别协议生成等技术路线),其中**不包含隐写或生成式隐蔽通信**,故本笔记不建立该概念链接。其余白名单概念(encrypted-traffic-analysis、website-fingerprinting、traffic-classification、malicious-traffic-detection 等)与本文亦无实质关联。

### 9.2 方法页

不触及白名单 methods 页面(contrastive-learning、transformer、state-space-model 等均非本文方法;本文使用的是概率式采样与 PRG 构造,白名单中无对应 slug)。

### 9.3 任务页

不触及白名单 tasks 页面。

### 9.4 综述页

不触及白名单 surveys 页面。

### 9.5 对比表

不建议链入 `method-comparison-table` / `dataset-comparison-table` / `open-source-registry`:前三者面向流量分析方法与数据集,本文不属于其收录范围(尽管 §6.2 自带方法对比表,其对象为隐写方案而非流量分析方法)。

## 10. 证据记录

| 结论 | 证据位置 |
|---|---|
| 复杂度对比:ADS 为 O(2^N),不随词表 \|V\| 增长;SparSamp O(2^B)、iMEC O(2^B\|V\|);参数范围 \|V\|~2^17–2^19、B~8–64、2^N~2^2–2^15 | §4.3 Table 1 + 表注 |
| WILD 上 MISTRAL:ADS 0.8964 bit/token、0.9137 利用率,对比 SparSamp 0.8562/0.8411、DISCOP(R.) 0.7683/0.7930 | §6.2 Table 2 |
| WILD 上 QWEN:ADS 1.8789/0.9103,而 DISCOP(R.) 1.9093/0.8866、SparSamp 1.8905/0.9052(原始容量并非处处最优) | §6.2 Table 2 |
| XHS 上 QWEN:ADS 3.4928 bit/token、0.9393 利用率(该设置下容量与利用率双第一) | §6.3 Table 3 |
| SR = 1.0000(所有 6 个设置),对比 iMEC 0.8432–0.9987 | §6.4 |
| TS-CSW 隐写分析 F1 落在 49.66%–50.81% | §6.5 |
| 采样预算:直接套用 METEOR 需 2^32 次以上采样,ADS 只需 2^4 次或更少 | §4.5 |
| 单 token 开销 < 100 ms;2×NVIDIA A5000 + 24×Intel Xeon w5-3423;1,000 样本/设置,500 token 上限 | §4.6/§6.1 |
| 安全性由 G0–G3 博弈序列证明(G1 均匀选取、G2 真随机种子替换 PRG、G3 i.i.d.) | §4.4 |

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-USENIX-Provable_Secure_Steganography_Based_on_Adaptive_Dynamic_Sampling.pdf
- MinerU Markdown：02-parsed-markdown/2026-USENIX-Provable_Secure_Steganography_Based_on_Adaptive_Dynamic_Sampling.md

## 12. 后续问题

1. **指标口径需谨慎引用**:论文摘要与正文对"容量"的表述为 "comparable with existing PSS methods in efficiency and capacity"(§2.1);实测中 ADS 的 **utilization 在 6/6 个设置中最高**,但 **Embed bit/token(原始容量)只在 3/6 个设置中最高**(WILD QWEN、XHS MISTRAL、XHS LLAMA3 上落后)。引用时应同时给出两个指标。
2. **部署前提未验证**:解析稿将"种子确定性"列为局限(服务端不保证相同 seed 得到相同输出);该前提是否成立直接决定 ADS 在真实闭源 API 上能否部署。
3. 解析稿给出 Table 4/Table 5 的隐写文本示例(含 gpt-3.5-turbo-1106 生成样例),可对照原 PDF 观察输出自然度。
4. ADS 的安全性依赖两个假设(PRG 存在 + 同分布采样的 i.i.d. 性质),对采样接口的实现细节(是否真独立)的敏感性解析稿未做实验评估。
5. **聚合提示**:本文与 KB 主题无实质交集,聚合时请勿计入 traffic-* 主题统计;笔记不建立任何 wikilink(见 §9.1)。

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

论文从一个部署事实切入：现实中的 LLM API 往往只提供“给 seed、返回 token”的采样接口，而主流可证明安全隐写假设客户端可以读取完整概率分布。作者把这一接口限制转化为共享随机性的来源，用 PRG 为候选消息生成采样 seed，再把碰撞集合的规模控制在有界区间内。转折点不是追求无碰撞，而是承认碰撞、把碰撞集合列为解码状态，并通过动态扩张让每一步仍有足够的可嵌入比特。G0–G3 博弈证明输出分布保持不变，随后 WILD/XHS、多个模型和 TS-CSW 把“可证明”落到 SR=1、接近随机的隐写分析 F1 和容量/利用率数据。结尾回到 API 确定性、采样开销和非语言模态边界，避免把 seed-only 方案泛化成所有闭源服务都可部署。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract/Introduction | 说明显式分布访问是现有 PSS 的共同前提 | 问题建立 | seed-only API 成为新约束 |
| Related Work | 对比 METEOR、DISCOP、SparSamp、iMEC | 缺口定位 | 复杂度与分布访问同时受限 |
| Method | 定义 collision set、动态扩张与固定参数 N | 方法主体 | 不消除碰撞，而是显式管理碰撞 |
| Security | G0→G1→G2→G3 游戏序列 | 理论支点 | 均匀抽样与真实模型采样分布相同 |
| Experiments | 容量/利用率、SR、TS-CSW、时间四条线 | 证据兑现 | SR=1 和 F1≈50% 同时成立 |
| Discussion | 解释 seed 确定性、N 和 API 模态边界 | 外推约束 | 自建/自控 API 更可靠 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 接口缺口 | 现有 PSS 需要概率/累积分布，实际 API 只给 seed 采样 | 将 seed-taking API 作为正式接口模型 | §1, §2 |
| 碰撞缺口 | 候选消息映射到同一 token 时确定性解码失败 | 动态 collision set 记录并按预算扩张 | §3–4 |
| 复杂度缺口 | 词表大、METEOR 窗口巨大、iMEC 优化昂贵 | O(2^N) 且与词表大小无关的构造 | §4.3 |
| 证据缺口 | 分布保持不等于能可靠解码或难以检测 | 同时报告 SR、TS-CSW F1、容量与利用率 | §5 |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| WILD/XHS 容量 | 展示不同语言风格和模型下的 bit/token、利用率 | 回答“能嵌多少” |
| SR 对比 | 与 iMEC 的概率解码错误率对照 | 回答“能否可靠解出” |
| TS-CSW F1 | 对抗隐写分析器 | 回答“是否像正常采样” |
| 时间复杂度 | 比较每 token 采样时间与基线 | 回答“seed-only 是否可运行” |
| API/模态限制 | 讨论 seed 确定性和图像生成时间 | 限制部署外推 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 接口驱动 | 先锁定真实接口限制，再设计协议 | 从部署约束而非理想 API 出发 |
| 碰撞处理 | 将失败状态显式建模成 collision set | 不回避失败事件，用状态维护吸收它 |
| 理论—实验 | G0–G3 逐步替换，对应 SR/F1/容量实验 | 每个安全游戏步骤都有可观测实验对象 |
| 指标拆分 | capacity、utilization、SR、F1、time 分开报告 | 避免用一个平均分掩盖工程权衡 |

## 14. 证据边界与复现清单

1. **安全假设**：G0–G3 依赖 PRG 伪随机性与模型采样 i.i.d.；若 seed API 不确定、服务端有额外状态或输出非独立，证明不直接适用。
2. **接口边界**：论文主要实验使用本地/可控 7B 级模型；闭源 API 的 seed 参数通常只“尽力”保证确定性，不能把本方法写成已验证的云服务部署。
3. **复杂度边界**：O(2^N) 与词表大小无关，但 N 增大仍指数增长；论文实验把集合上限设为 2^9，不能据此推断更高 N 的时间和隐写质量。
4. **指标边界**：SR=1 只说明实验设置下比特解码正确，不等于输出一定无法被所有隐写分析器检测；TS-CSW F1≈50% 只覆盖该检测器、数据集和模型。
5. **容量口径**：ADS 利用率在 6 个设置中最高，但原始 Embed bit/token 只在部分设置中最高；引用时必须同时报告二者。
6. **数据/硬件**：WILD、XHS、MISTRAL3/QWEN2/LLAMA3、每设置 1,000 样本、top-p=1、temperature=1、最大 500 tokens、2×A5000 是结果的一部分；换模型或 prompt 需重测。
7. **复现材料**：artifact 归档于 Zenodo records/18152848；需核对版本、seed、碰撞集合上限、PRG 状态更新和采样日志，不能只复述论文表格。

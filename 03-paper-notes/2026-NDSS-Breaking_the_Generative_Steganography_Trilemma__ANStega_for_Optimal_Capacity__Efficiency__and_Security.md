---
type: paper
title_original: "Breaking the Generative Steganography Trilemma: ANStega for Optimal Capacity, Efficiency, and Security"
title_cn: "打破生成式隐写的三难困境:ANStega 实现最优容量、效率与安全"
authors: [Yaofei Wang, Weilong Pang, Kejiang Chen, Jinyang Ding, Donghui Hu, Weiming Zhang, Nenghai Yu]
year: 2026
venue: "NDSS 2026"
doi: "10.14722/ndss.2026.240605"
url: "https://doi.org/10.14722/ndss.2026.240605"
pdf: "00-inbox/PDFs/2026-NDSS-Breaking_the_Generative_Steganography_Trilemma__ANStega_for_Optimal_Capacity__Efficiency__and_Security.pdf"
mineru_md: "02-parsed-markdown/2026-NDSS-Breaking_the_Generative_Steganography_Trilemma__ANStega_for_Optimal_Capacity__Efficiency__and_Security.md"
status: deep-analyzed
reading_level: L3
research_area: [censorship-circumvention]
task: ["generative steganography", "covert communication"]
method: ["rANS state-machine inversion", "streaming renormalization", "CSPRNG masking"]
dataset: ["IMDB movie reviews", "DDPM image carrier example"]
code: "unknown（解析稿未给出代码仓库 URL;artifact 归档版本见 https://doi.org/10.5281/zenodo.17943483,该 DOI 非论文 DOI）"
relevance: low
created: "2026-09-19"
updated: "2026-10-10"
---

# Breaking the Generative Steganography Trilemma: ANStega for Optimal Capacity, Efficiency, and Security

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Breaking the Generative Steganography Trilemma: ANStega for Optimal Capacity, Efficiency, and Security |
| 中文标题 | 打破生成式隐写的三难困境:ANStega 实现最优容量、效率与安全 |
| 作者 | Yaofei Wang, Weilong Pang, Kejiang Chen, Jinyang Ding, Donghui Hu, Weiming Zhang, Nenghai Yu(合肥工业大学 + 中国科学技术大学) |
| 年份 | 2026 |
| 会议/期刊 | NDSS 2026 |
| 研究方向 | censorship-circumvention(隐蔽通信/生成式隐写,与 KB 主体加密流量分析仅弱相关) |
| 任务类型 | 无白名单任务页对应(隐写编码,非流量分析任务) |
| 方法关键词 | transformer(LLM 载体)、Asymmetric Numeral Systems(rANS)、streaming state renormalization、CSPRNG mask |
| 数据集 | IMDB movie review(1,000 条上下文,评测用前 100 条);6 个 LLM 作载体 |
| 是否开源 | 解析稿未给出仓库;提供 artifact(.zip + Zenodo 归档,artifact 附录 §B) |
| PDF | 00-inbox/PDFs/2026-NDSS-Breaking_the_Generative_Steganography_Trilemma__ANStega_for_Optimal_Capacity__Efficiency__and_Security.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-NDSS-Breaking_the_Generative_Steganography_Trilemma__ANStega_for_Optimal_Capacity__Efficiency__and_Security.md |

---

## 1. 一句话总结

> 把 ANS 编解码状态机"反用"(用解码函数嵌入、编码函数提取)并加流式重归一化与 CSPRNG 掩码,首次同时做到近熵容量、O(1) 效率与可证分布不可区分。

---

## 2. 摘要翻译

### 2.1 摘要原文

> "Generative steganography shows immense promise for covert communication, yet existing methods are often constrained by a trilemma of capacity, efficiency, and security. Methods based on Huffman Coding (HC) suffer from poor efficiency and security, while those based on Arithmetic Coding (AC), despite achieving optimal capacity, also pose security risks. Although recent provably secure methods have addressed the security issue, they often do so at the cost of elevated embedding complexity or diminished capacity—failing to match the high capacity exhibited by AC-based methods. To address this trilemma, we adapt Asymmetric Numeral Systems (ANS) for steganography. Our core insight is to repurpose the ANS state machine, using its decoding function for embedding and its encoding function for extraction. ... Experimental results validate that ANStega simultaneously achieves optimal embedding capacity, optimal efficiency (embedding complexity with O(1)) and optimal security, successfully resolving the long-standing trilemma in generative steganography."(节选自 Abstract)

### 2.2 摘要中文翻译

生成式隐写在隐蔽通信中前景巨大,但现有方法普遍受制于容量—效率—安全的三难困境:Huffman 编码(HC)类方法效率与安全性差;算术编码(AC)类方法虽容量最优,却同样存在安全风险;近期可证安全的方法虽解决了安全性,却以更高嵌入复杂度或更低容量为代价,难以达到 AC 类方法的高容量水平。为解决该三难困境,作者将非对称数字系统(ANS)适配到隐写场景,核心洞见是**改造 ANS 状态机——用其解码函数做嵌入、用其编码函数做提取**。为落地该思想,论文引入多项关键创新:流式架构 + 状态重归一化以支持任意长消息的稳定嵌入;直接浮点运算替代昂贵的"概率→频率"转换以降低复杂度与精度损失;以及关键的加密掩码机制,使采样由密码学安全伪随机数发生器(CSPRNG)驱动,从而实现可证安全;最后将核心计算优化为高效按位操作,获得极高嵌入/提取速度。实验验证 ANStega 同时实现最优嵌入容量、最优效率(O(1) 嵌入复杂度)与最优安全性。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法?

在"在线监控与流量分析日益普遍"的背景下,加密只保护内容、却暴露元数据(§I),隐写通过把秘密数据嵌入无害媒介来隐藏"通信正在发生"这一事实。生成式模型(尤其 LLM)的兴起使生成式隐写成为可能:直接在模型高维概率分布上"解压"秘密比特流为 token(§I)。但作者发现该领域被一个**三难困境**卡住:容量、效率、安全三者不可兼得(Table I)。

### 3.2 现有方法的痛点和不足

- HC 类方法[6],[7]:树重建开销频繁 + 不可避免的分布修改 → 效率与安全性双差;
- AC 类方法[9]–[11]:容量近最优,但概率缩放带来显著计算开销,且精度诱导的分布畸变削弱安全性;
- 可证安全方法:Meteor[13]、Discop[14]、iMEC[15] 安全但容量/性能代价大;SparSamp[19] 效率与安全均优,但因稀疏采样设计存在轻微容量缺口;
- 并发工作 SA-ANS[16]:已开始把 ANS 用于语言隐写,但**直接做状态相关的采样、无密码学掩码**,留下可被分析检测的统计痕迹,且复杂度非最优、固定速率消耗在低熵分布上限制容量(§II)。
- 图像域同样存在权衡:StegaDDPM[21] 效率高但容量低;Pulsar[20] 安全但计算开销大、有效嵌入率低(§I)。

### 3.3 论文的研究假设或核心直觉

ANS 兼具"Huffman 式计算简单"与"AC 式高压缩效率",且已被 Meta/Apple/Google/Microsoft 工业采用(§I)。直觉是:**ANS 的状态机可被反用**——解码函数本是"状态+符号→比特",把它当作嵌入函数即可把秘密比特"走"进状态;编码函数则用于提取(§I, Fig. 1)。但作者强调"naïve port 不行":朴素移植不支持长消息、不满足常数时间、也不具备严格的分布安全,因此必须做隐写专用的改造(流式有界状态、免全局重缩放的概率更新、每步 MASK、按位原语重写)。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 生成式隐写已在文本/图像/音频多模态繁荣,但每类方法都在容量、效率、安全之一上妥协(Fig. 1 三类熵编码方案对比) | §I, Fig. 1 |
| 痛点提炼 | HC 树重建与分布修改、AC 概率缩放与精度畸变、可证安全方法容量/复杂度代价——工程上无法同时满足三个部署指标 | §I, §II |
| 问题转化 | 把"如何同时达到三个最优"形式化为三难困境(Table I 逐方法打点),并将"近熵容量 / O(1) 复杂度 / D_KL ≤ ε"设为可判定的三个目标 | Table I |
| 文献定位 | ANS 虽被工业界广泛采用,但在隐写中仅被 SA-ANS 初步触及,其潜力"fully harnessing ... remains an open challenge" | §I, §II |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 经隐写专用改造的 rANS(流式有界状态 + 直接浮点更新 + CSPRNG 掩码 + 按位实现)可同时达成近熵容量、O(1) 每步复杂度与 D_KL ≤ ε 的可证安全 | §I(反用 ANS 状态机);§III(设计) | 理论:安全性归约(Adv_stega ≤ Adv_PRNG, Eq. 11)+ 实验:6 模型容量/效率、NIST STS、KL、隐写分析器 |
| 辅助假设 | 掩码使每步采样由 CSPRNG 驱动,则隐含分布与模型分布严格不可区分 | §III(掩码机制),引 SA-ANS 无掩码的可检测性反例 | KL 测量(Table V)+ 4 个深度隐写分析器准确率 |

**假设验证结果**:

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 容量近熵 | 支撑 | UR ≈ 1.01–1.02(ANStega)vs Huffman UR 最高 1.48(膨胀源于 dyadic 畸变) | §VI, Table IV |
| O(1) 效率 | 支撑 | 每步 SITR 恒为 0.01,较 SA-ANS 降低 8× | §VI, Table IV |
| 可证安全 | 支撑 | 算法 KL 为 0(AC 7.92E-02→2.86E-05,Huffman 5.47E-01→7.23E-01,SA-ANS ~1E-06);NIST STS 全通过;4 个隐写分析器准确率 49.35%–50.28% | Table III, V, VIII |

---

## 4. 方法设计

### 4.1 方法整体流程

ANStega 把"LLM 生成 token"与"秘密比特消费"耦合为一个流式过程:编码端(发送方)持有秘密比特流 b 与共享密钥 K;每一步,rANS 解码函数在**被 MASK 扰动后的状态下**从模型分布 p 中"抽出"一个 token t 输出到文本,同时把 b 的一段比特吸收进状态 x 并做重归一化;解码端(接收方)以同一模型、同一 K 重放,用 rANS 编码函数从观察到的 token 序列逐步恢复比特。双向都只做常数时间操作。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 状态初始化 | 密钥 K(种子) | 以 K 初始化 CSPRNG 与 rANS 状态 x,设定有界区间 [L, H] = [α·M, 2L−1] | 初始状态 x | 保证可复现的双向同步 |
| Step 2 逐 token 采样 | 上下文 + 模型分布 p | 用直接浮点更新(Eq. 7)得到区间,不重缩放;对状态施加掩码 r ← ((x mod M) ⊕ R_t)/M(Eq. 8,R_t 来自 CSPRNG) | 区间 / 掩码值 | 免去概率→频率转换;掩码保证采样随机性与独立性 |
| Step 3 状态吸收比特 | 区间 + 秘密比特段 | 反向走 ANS 解码步,把比特吸收进状态 x | 新状态 x' | "嵌入"发生的时刻(容量来源) |
| Step 4 重归一化 | x' | Expand/Shrink(Algorithm 1/2):当 x 越界时按位流式输出/输入比特,把状态约束回 [L, H] | 有界状态 + 输出 token | 支持任意长消息而不数值爆炸,同时保持 O(1) 每步 |
| Step 5 提取 | 收到的 token 序列 + K | 以编码函数对每个观测 token 走反步(Algorithm 3/4),重放同一掩码流 | 恢复的比特段 | 接收端解码,无需任何侧信息 |
| Step 6 批量/流式运行 | 长文本 | Algorithm 5/6(Encode_G / Decode_G)做整个生成过程的驱动与边界处理 | 隐写文本 / 原始消息 | 工程落地 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 反向状态机映射 | 用解码函数嵌入、编码函数提取(Eq. 6) | ANS 状态 + 模型分布 | 状态转移关系 | 整个方案的理论基石 |
| 流式重归一化(Expand/Shrink) | 把状态维持在有界区间,支持任意长消息 | 越界状态 | 比特流出/流入 | 与 Step 3/4 交替执行,保证 O(1) |
| 直接浮点概率更新 | 免去 convert/renormalize 全词表操作,直接以浮点更新区间(Eq. 7) | 模型概率 p | 区间边界 | 替代 AC 的精度重缩放,消掉 KL 畸变 |
| CSPRNG 掩码 | 以 R_t 扰乱状态再取样(Eq. 8) | 密钥 K 派生的随机流 | 掩码后的状态 | 安全核心;使采样不可预测、分布不可区分 |
| 按位算术实现 | 将核心运算改写为位运算 | 整数状态 | 更快嵌入/提取 | 吞吐优化,不改语义 |
| 安全归约 | Adv_stega ≤ Adv_PRNG(Eq. 11) | — | 安全性证明 | 为"可证安全"提供理论依据 |

### 4.4 公式、算法和机制解释

- **反向映射(Eq. 6)**:正常 ANS 中 encode(s, x) 把符号 s 与状态 x 合成新状态;ANStega 反过来,把"模型想生成的 token"当作符号、把"秘密比特"当作驱动,于是**采样即嵌入**。
- **有界状态**:L = α·M,H = 2L−1,α 控制状态区间与词表规模 M 的比;状态只在 [L, H] 内,靠 Expand/Shrink 维持,避免长消息导致的整数爆炸。
- **直接浮点更新(Eq. 7)**:直接用浮点概率算区间,不做全局 rescale,因此**算法层面 KL 为 0**(Table V),这是与 AC/SA-ANS 的关键区别。
- **掩码(Eq. 8)**:r ← ((x mod M) ⊕ R_t)/M;R_t 由 CSPRNG 产生,使取样点以密码学随机方式落到区间上——既保证采样的随机性(不可预测),又保证独立性(逐步 mask 互相独立)。
- **安全性归约(Eq. 11)**:Adv_stega ≤ Adv_PRNG,即攻破隐写的优势不超过攻破底层 PRNG 的优势;威胁模型为**被动攻击者**(只看文本,不看生成过程)。
- **对比**:§VI 明确 ANStega 的 UR ≈ 1.01–1.02、SITR 恒 0.01(比 SA-ANS 低 8×),而 Huffman 的"高 UR"其实是分布畸变造成的假象。

### 4.5 方法优势

1. 三目标同时最优(Table I 唯一一行三个实心点);
2. 编码算法与模态无关:论文用 DDPM 示例证明同一原语可迁移到图像(Table I 标注 Text/Image);
3. 吞吐高:AC 级速度 + 最低采样开销;
4. 安全性是**可证**而非经验性:既有归约又有 KL=0 与隐写分析实验。

### 4.6 方法不足

- 威胁模型为**被动**:对主动攻击(篡改文本)脆弱(§VII 局限);
- 部署需要收发双方**共享种子并保持模型/实现同步**;
- 对称密钥交换问题未解决(需带外信道);
- 论文自述尚未覆盖全部模态的端到端实现(Table I 脚注说明模态列仅反映被引工作的实现)。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

主流做法分两条线:(a) 熵编码路线(HC/AC)在生成时"选择 token"承载比特,必然改动或近似模型分布;(b) 可证安全路线(Meteor/Discop/iMEC/SparSamp)通过构造分布副本或最小熵耦合实现不可区分,但付出容量或复杂度代价。ANStega 的差别在于:**不修正分布、也不做耦合,而是把编码器状态本身当作比特容器**,再以 CSPRNG 掩码保证状态到 token 的映射不可区分。SA-ANS 同样用 ANS,但缺掩码、复杂度非最优、固定速率消耗。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| ANS 状态机反用 | 解码函数嵌入、编码函数提取(§I, Eq. 6) | 高 | 是(任何熵编码器状态均可作此思路的候选) |
| 流式有界状态 | Expand/Shrink 使任意长消息稳定嵌入且 O(1) | 高 | 是(需常数时间编码器的场景) |
| 直接浮点更新 | 免全局 rescale → 算法 KL = 0 | 高 | 是(任何以"保分布"为目标的编码) |
| CSPRNG 掩码 | 采样随机性与独立性 → 归约到 PRNG 安全 | 高 | 是(可移植到其他采样式隐写) |
| 按位实现 | 位运算重写核心算术,提升吞吐 | 中 | 是(工程优化) |
| 图像域实例化 | 用 DDPM 演示模态无关性(Fig. 5,~463 kbits 载荷) | 中 | 是 |

### 5.3 适用场景

- 需要**长消息、高吞吐**的隐蔽通信载体(如 LLM 生成长文);
- 对"统计不可检测"有强要求的场景(对手可做隐写分析);
- 由于编码算法与模态无关,亦可作为图像(扩散模型)隐写的编码后端。
不适用:对抗主动篡改、无法安全共享种子、或收发模型不同步的场景。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| Huffman-based [6],[7] | 概念简单 | 树重建开销、分布被修改;UR 最高 1.48(畸变所致),KL 达 5.47E-01 | 以 ANS 状态承载比特,不改分布 |
| AC-based [8]–[11] | 容量近最优 | 概率缩放开销、精度畸变;KL 7.92E-02→2.86E-05 | 直接浮点更新,算法 KL = 0 |
| ADG [12] | 动态分组提升不可感知性 | 三目标均非最优(Table I) | 从编码层而非分组层解决 |
| Meteor [13] / Discop [14] / iMEC [15] | 可证安全 | 容量或性能代价大(iMEC SITR 640–1892) | 同等安全下把 SITR 压到 0.01 |
| SA-ANS [16](并发) | 率先把 ANS 用于语言隐写 | 无密码学掩码、固定速率消耗、非最优复杂度 | 加掩码 + 流式状态 + 按位实现 |
| SparSamp [19] | 效率与安全均优 | 稀疏采样导致容量缺口 | 近熵容量(UR ≈ 1.01) |
| Pulsar [20] / StegaDDPM [21] | 图像域可证安全/高效率 | 分别开销大 / 容量低 | 编码层方案可同时用于图像(Fig. 5) |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

载体模型 6 个:GPT-2、Llama 3 8B、Qwen2.5 3B、DeepSeek-R1-Distilled-Qwen 1.5B、SmolLM2、Phi-2(artifact 附录 §A-4);评测素材为 IMDB 影评的 1,000 条上下文(批量脚本取前 100 条)。硬件:Intel Xeon Gold 6330 + NVIDIA RTX 4090 24GB。对比维度:嵌入率(UR/ES/GS)、效率(SITR/吞吐)、安全(KL、NIST STS、隐写分析器)。

### 6.2 数据集

| 数据集 | 规模/内容 | 用途 |
|---|---|---|
| IMDB movie review | 1,000 条上下文(评测取前 100 条) | 文本隐写容量/效率/安全评测 |
| message.txt | 二进制秘密载荷(artifact 提供) | 嵌入载荷 |
| DDPM 人脸生成(图像示例) | Fig. 5,载荷约 463 kbits | 证明模态无关性 |

### 6.3 Baseline

Huffman 编码、算术编码(AC)、SA-ANS(ANS 并发工作);安全侧对比 AC/Huffman/SA-ANS 的 KL;隐写分析侧用 4 个深度检测器:FCN、CNN、R-BiLSTM-C、BiLSTM-Dense。

### 6.4 评价指标

- **容量**:UR(utilization rate)、ES/GS、ER(embedding rate),越接近理论熵越好;
- **效率**:SITR(sampling-inference time ratio,额外采样时间比)与吞吐;
- **安全**:算法 KL 散度、NIST STS 检验、隐写分析器准确率(应≈50%)。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| IMDB,6 LLM | UR | 1.01–1.02 | Huffman 1.25–1.48 | 容量不虚高、接近熵极限 | Huffman 的 UR>1 是 dyadic 畸变造成的膨胀 | 
| IMDB | SITR | 0.01(恒定) | SA-ANS 0.08;AC 0.03–0.04 | 相对 SA-ANS 降低 8× | O(1) 每步 |
| IMDB | 算法 KL | 0 | SA-ANS ~1E-06;AC 7.92E-02→2.86E-05;Huffman 5.47E-01→7.23E-01 | 严格为 0 | 因不做概率重缩放(Table V) |
| 跨模型泛化 | SITR/UR | 与单模型一致 | iMEC SITR 640.56(GPT-2)/1151.72(Llama3)/1891.82(Qwen2.5) | 数量级优势 | Table VI |
| 隐写分析 | 检测准确率 | 49.35%–50.28% | 随机猜测 50% | — | FCN 49.92 / CNN 50.28 / R-BiLSTM-C 49.35 / BiLSTM-Dense 50.15 |

> ⚠️ MinerU 解析问题:Table IV/V 在解析稿中部分数值以科学计数法混排(如 7.92E-02 与 2.86E-05 同行),引用时已按上下文还原语义,建议以原文表格核对。

### 6.6 优势最明显的场景

长消息 + 高吞吐 + 需抗统计检测的文本隐蔽通信:ANStega 在保持 AC 级速度的同时把 SITR 压到常数 0.01,并且在 6 个不同规模 LLM 上表现一致,说明方案不依赖特定模型。

### 6.7 局限性

- 被动威胁模型:不抗主动攻击(篡改/污染隐写文本);
- 收发双方需共享种子且**实现/模型严格同步**,否则解码失败;
- 对称密钥的带外交换问题未解决;
- 论文的"最优"结论建立在所测 6 模型与 IMDB 语料上,跨语种/跨域的分布安全未验证(§VII)。

---

## 7. 学习与应用

### 7.1 是否开源？

解析稿未给出 GitHub 仓库;提供 artifact(.zip,含 requirements.txt、脚本与素材),永久归档于 Zenodo:https://doi.org/10.5281/zenodo.17943483(artifact DOI,非论文 DOI)。代码可得性:需自备 Hugging Face 模型权重。

### 7.2 复现关键步骤

1. 环境:Python ≥ 3.10 + PyTorch(CUDA 11.8)+ 16–24GB 显存的 NVIDIA GPU(artifact 附录 §A);
2. 下载 Hugging Face 因果 LM(gpt2 会自动下载),准备 imdb_context.xlsx 与 message.txt;
3. 运行批量脚本(默认取前 100 条上下文),分别测容量(UR/ES/GS)、SITR 与 KL,再对生成文本跑 NIST STS 与 4 个隐写分析器。

### 7.3 关键超参数、预处理和训练细节

- 状态区间参数 α(控制 L = α·M 与词表规模 M 的比例),论文以 α 与 mask 开关做消融(Table II, Llama3, top-p p=1.0);
- 采样策略:top-k / top-p(Sec. VI 覆盖两种);无需训练,纯推理期改造;
- 掩码必须每步刷新(CSPRNG),否则退化为 SA-ANS 式的可检测方案。

### 7.4 能否迁移到其他任务？

**可以**,论文自证编码算法与模态无关:同一 ANS 原语被用于 DDPM 图像隐写(Fig. 5,~463 kbits 载荷)。更广义地,"把编码器状态当比特容器"的思路可迁移到任何有显式状态机的编解码器(音频 codec、视频 codec)。

### 7.5 对我的研究有什么启发？

对加密流量分析方向的直接启发有限,但有三点方法论价值:(1) **三难困境式的目标形式化**(Table I 逐方法打点)是把"谁更好"变成"能否同时最优"的干净写法;(2) **可证安全 + 经验检测双轨验证**的模式,可直接套用到 WF 攻防的"不可区分性"论证上;(3) 掩码/随机化保证"采样不可预测"的思路,与流量侧防御中"消除确定性特征"是同一思想的不同域表达。

---

## 8. 总结

### 8.1 核心思想

> 反用 ANS 状态机,以掩码换取可证不可区分。

### 8.2 速记版 Pipeline

1. 以密钥 K 初始化 CSPRNG 与有界 rANS 状态;
2. 每步用直接浮点更新模型分布区间(不重缩放);
3. 以 CSPRNG 掩码扰乱状态后采样并输出 token(嵌入);
4. 用 Expand/Shrink 把状态约束回有界区间,支持任意长消息;
5. 接收端以编码函数重放同一掩码流,逐步恢复秘密比特。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[censorship-circumvention]](本文属隐蔽通信/隐写,与审查规避仅在"抗检测通信"动机层面相关)

### 9.2 相关方法

- [[transformer]](以 LLM 分布为载体的生成式隐写)

### 9.3 相关任务

- 无(库内任务页均为流量分析类任务,本文无对应项)

### 9.4 可更新的综述页面

- 无(库内 5 个综述页均不覆盖生成式隐写/信息隐藏)

### 9.5 可加入的对比表

- 无

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 三难困境此前无方法同时解决,ANStega 是首个三项全最优 | Table I 逐方法打点,仅 ANStega 一行三个实心点 | §I, Table I |
| 朴素移植 ANS 不能解决问题(长消息/常数时间/严格分布安全) | "a naïve port fails to provide long-message support, constant-time embedding, or rigorous distributional security" | §I |
| 算法层面 KL 严格为 0,优于 SA-ANS 的 ~1E-06 | Table V:ANStega 0/0 | §VI, Table V |
| 每步开销恒定 SITR = 0.01,比 SA-ANS 低 8× | "This represents an 8× reduction in overhead compared to SA-ANS" | §VI |
| 4 个深度隐写分析器全部退化到随机猜测水平 | FCN 49.92%、CNN 50.28%、R-BiLSTM-C 49.35%、BiLSTM-Dense 50.15% | §VI, Table VIII |
| 安全性有归约支撑而非仅经验 | Adv_stega ≤ Adv_PRNG(Eq. 11),被动威胁模型 | §III, Eq. 11 |
| 编码算法模态无关,可用于扩散模型图像隐写 | Fig. 5 DDPM 示例,约 463 kbits 载荷 | §VI, Fig. 5 |
| 主要局限:被动威胁模型 + 需种子/实现同步 | 作者自述限制章节 | §VII |

---

## 11. 原始资料链接

- PDF:00-inbox/PDFs/2026-NDSS-Breaking_the_Generative_Steganography_Trilemma__ANStega_for_Optimal_Capacity__Efficiency__and_Security.pdf
- MinerU Markdown:02-parsed-markdown/2026-NDSS-Breaking_the_Generative_Steganography_Trilemma__ANStega_for_Optimal_Capacity__Efficiency__and_Security.md

---

## 12. 后续问题

- 流式 rANS 的状态区间参数 α 对安全性与容量的联合影响曲线,解析稿中仅见消融表(Table II),未给出闭式结论;
- 主动攻击下(篡改隐写文本)的失败模式与可检测性未评估;
- 论文以 Zenodo artifact 归档但未声明代码仓库,复现需从 artifact 包内自建;
- 与 KB 主题(加密流量分析)的交叉点仅在"抗检测通信"层面,聚合时不宜计入 traffic-* 主题统计。

---

## 13. 写作叙事与故事线分析

> 本文为 NDSS 2026（CCF A）论文，补充方法论与叙事分析。

### 13.1 论文主线故事线

论文先用容量、效率、安全三项指标之间的冲突定义生成式隐写的三难困境，再把 Huffman、算术编码和可证安全方法放进同一比较框架。转折点是把 ANS 状态机的解码方向反用于嵌入、编码方向用于提取，并针对长消息、浮点精度和随机性补上流式重归一化、直接概率更新与 CSPRNG 掩码。理论归约先给出安全边界，随后用容量、开销、KL、NIST 和隐写分析器实验逐层验证，结尾再明确被动威胁模型、同步和密钥分发限制。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 三难困境、ANS 思路与三类结果的压缩预告 | 先给出问题和可验证目标 | 从“无法三者兼得”转到“状态机反用” |
| Introduction | 解释隐蔽通信需求并比较 HC/AC/可证安全路线 | 建立统一评价轴 | Table I 把三个目标显式化 |
| Related Work | 按熵编码、可证安全和图像隐写分组定位空白 | 说明现有妥协点 | SA-ANS 成为最近但仍不完整的参照 |
| Method | 状态反向映射→有界流式状态→浮点更新→掩码 | 逐项解除三难约束 | Eq. 11 将安全性归约到 PRNG |
| Experiments | 容量、效率、安全三组实验对应三项目标 | 完成三角验证 | KL=0、SITR=0.01 与检测器约 50% 同时出现 |
| Limitations / Conclusion | 收回主动攻击、同步和跨模态边界 | 控制主张范围 | 把“最优”限定在给定被动模型与实现假设内 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 性能权衡 | HC、AC、可证安全方案分别牺牲效率、安全或容量 | 三目标对比矩阵 | §I, Table I |
| 算法缺口 | 朴素 ANS 移植不支持长消息、常数时间和严格分布安全 | 机制失败分析 | §I, §II |
| 安全缺口 | SA-ANS 缺少密码学掩码，状态相关采样可能留下统计痕迹 | 安全假设对照 | §II, §III |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 容量实验 | 对比 UR、ES、GS 与熵上限 | 回答“是否保持 AC 级容量” |
| 效率实验 | 用 SITR 和吞吐比较采样额外开销 | 回答“是否达到常数级效率” |
| 安全实验 | KL、NIST STS 和四个隐写分析器交叉验证 | 回答“分布和可检测性是否安全” |
| 图像载体示例 | 用 DDPM 载荷展示编码层可迁移性 | 支撑模态无关性，但不替代完整跨模态评测 |
| 限制讨论 | 主动篡改、密钥交换和模型同步 | 明确理论安全边界 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 先给出三项互相牵制的指标，再列出现有方法的代价 | 用统一坐标系组织复杂相关工作 |
| Gap 提出方式 | 将“无法同时最优”转为三个可测目标 | 把抽象困境直接映射到实验指标 |
| 方法论证逻辑 | 每个机制对应一个失败原因：状态、精度、随机性、吞吐 | 采用“缺陷—机制—验证”一一对应 |
| 实验组织逻辑 | 容量→效率→安全，顺序与标题三项目标一致 | 用标题中的并列目标作为实验目录 |
| 局限性讨论方式 | 将被动模型和同步前提放到安全结论之后明确收束 | 在强结果后紧跟适用边界 |
| 最值得借鉴的结构 | “解码做嵌入、编码做提取”一句话交代反向映射 | 用一句可复述的操作对概括核心机制 |

## 14. 深度分析证据边界与知识层联动建议

- 本次补充依据对应 MinerU Markdown 的 §§I–VII、Table I/III–VIII、Eq. 6–11 与 Artifact Appendix；现有笔记已记录算法 KL、SITR、容量和检测器结果，未将图像示例当作完整跨模态验证。
- 可向 `04-concepts/censorship-circumvention.md` 或相关隐蔽通信综述增加“生成式隐写中的 ANS 状态机反用”条目；该工作不应计入 traffic-* 分类器方法统计。
- 当前未修改共享概念、方法、综述和对比表页面；上述联动仅作为后续总审计建议。

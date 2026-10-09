---
type: paper
title_original: "Stinger: A Light-Weight Website Fingerprinting Defense Through Poisoning Packet Sequences"
title_cn: "Stinger：基于投毒数据包序列的轻量级网站指纹防御"
authors: ["Lihai Nie", "Xiaodong Dong", "Lili Shi", "Laiping Zhao", "Zheli Liu"]
year: 2026
venue: "IEEE TIFS 2026"
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-TIFS-Stinger__A_Light-Weight_Website_Fingerprinting_Defense_Through_Poisoning_Packet_Sequences.pdf"
mineru_md: "02-parsed-markdown/2026-TIFS-Stinger__A_Light-Weight_Website_Fingerprinting_Defense_Through_Poisoning_Packet_Sequences.md"
status: processed
reading_level: L3
research_area: ["website-fingerprinting", "encrypted-traffic-analysis"]
task: ["website-fingerprinting"]
method: ["convolutional-network"]
dataset: ["DF Dataset", "AWF Dataset", "DF 开放世界子集"]
code: "https://github.com/sxy888/Stinger-prototype"
relevance: high
created: "2026-09-19"
updated: "2026-09-19"
---

# Stinger: A Light-Weight Website Fingerprinting Defense Through Poisoning Packet Sequences

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Stinger: A Light-Weight Website Fingerprinting Defense Through Poisoning Packet Sequences |
| 中文标题 | Stinger：基于投毒数据包序列的轻量级网站指纹防御 |
| 作者 | Lihai Nie, Xiaodong Dong (Member, IEEE), Lili Shi, Laiping Zhao, Zheli Liu |
| 年份 | 2026（注意：Table II 中 Stinger 一行标注的 Year 为 2025，与批次分配年份不一致，本笔记以分配年份为准并如实记录该差异） |
| 会议/期刊 | IEEE TIFS 2026（解析稿未给出期刊全名；解析稿中未见 DOI） |
| 研究方向 | 网站指纹（WF）防御、数据投毒 / 后门触发、Tor 流量隐私保护 |
| 任务类型 | 针对 WF 攻击的防御（闭世界默认 + 开放世界扩展；对抗已见攻击 + 新型攻击 + 自适应攻击） |
| 方法关键词 | 数据投毒（data poisoning）、二级防御/对抗式防御（secondary/fighting defense）、P 序列（poison packet sequence）、P model（MLP 生成器）、代理 WF 分类器联合训练、模型迁移性、过拟合诱导、用户私密 secret 输出打乱（output shuffling）、冲突映射（conflicted maps, Theorem 1）、延迟高效插入、PKI/TLS 密钥分发 |
| 数据集 | DF（95 站点 × 1000 traces，2016-02，Alexa top 100）、AWF（Alexa top 1200，~2500 traces/站，2017-01）；开放世界用 DF 的 95 monitored + 40,000 unmonitored |
| 是否开源 | 是（原型系统 https://github.com/sxy888/Stinger-prototype ；实验细节 https://github.com/sxy888/Stinger/blob/main/experiment.md ） |
| PDF | 00-inbox/PDFs/2026-TIFS-Stinger__A_Light-Weight_Website_Fingerprinting_Defense_Through_Poisoning_Packet_Sequences.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-TIFS-Stinger__A_Light-Weight_Website_Fingerprinting_Defense_Through_Poisoning_Packet_Sequences.md |

> ⚠️ MinerU 解析问题：解析稿同样系统性丢失连字 "ff"（effective→efective、suffer→sufer、offline→ofline、difficulty→dificulty、traffic→trafic），引用时已还原。Table III/IV 中标注"次优"的符号（‡）在部分单元格中位置错乱（如 "20.34%‡"、"7.14%‡"），已按表意与正文交叉核对后使用。

---

## 1. 一句话总结

> 把 WF 防御从"伪装流量"换成"投毒模型"：用 MLP 生成器与代理 DF 分类器联合训练出 P 序列，插进攻击者训练集诱导其模型过拟合，再用用户私密 secret 打乱映射——DF/AWF 上仅 12.38%/6.74% 带宽开销即获 81.83/83.32 的平均 SDR，效率比既有防御高一个量级。

---

## 2. 摘要翻译

### 2.1 摘要原文

（已还原 "ff" 连字）

> Website Fingerprinting (WF) attack can be mitigated through random camouflage or pair camouflage. Random camouflage inserts random dummy packets into the traces according to pre-defined rules. It can be compromised easily by machine learning-based WF attacks. Pair camouflage obfuscates the distinguishing features of paired websites by inserting elaborated perturbations into raw traces, thereby misleading the attacker. It is costly in maintaining a perturbation generator for each pair of websites. Based on these insights, we propose Stinger, a novel data poisoning based WF defense, which enables effective defense against WF attacks with low bandwidth overhead and only maintains one generator for all websites. Stinger exploits the idea of poisoning by contaminating the model directly in such a way that the WF attacks only classify based on the inserted poison sequences, thus being low overhead and website independent. We experimentally evaluate Stinger using the DF and AWF datasets. The results show that Stinger improves the successful defending rate by an average of 20.37% and 22.83% while reducing overhead by 85.88% and 81.35%, respectively.

### 2.2 摘要中文翻译

网站指纹（WF）攻击可通过随机伪装（random camouflage）或配对伪装（pair camouflage）缓解。随机伪装按预定义规则向 trace 中插入随机 dummy packet，但容易被基于机器学习的 WF 攻击攻破；配对伪装通过向原始 trace 注入精心构造的扰动来混淆成对网站的区分性特征、从而误导攻击者，但其代价是需要为每一对网站维护一个扰动生成器。基于这些观察，作者提出 Stinger——一种新的基于数据投毒的 WF 防御：它只需为所有网站维护**一个**生成器，即可以低带宽开销有效防御 WF 攻击。Stinger 利用投毒思想直接污染模型：使 WF 攻击只能依据插入的 poison 序列进行分类，因而开销低且与网站无关。作者在 DF 与 AWF 数据集上实验评估：Stinger 把成功防御率（SDR）平均分别提升 20.37% 与 22.83%，同时把开销分别降低 85.88% 与 81.35%。

> ⚠️ 数值自相矛盾：§I 贡献列表给出的是另一组数——"SDR 平均提升 32.44% 与 22.33%、带宽开销降低 75.71% 与 83.85%"（DF/AWF）。两处口径不一致，本笔记两处并列保留，引用时需谨慎。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

作者先做了一轮"现状体检"：现有 WF 防御都属**伪装（camouflage）**范式——要么随机伪装（Tamaraw/WTF-PAD/FRONT，按规则插 dummy packet），要么配对伪装（Mockingbird/ALERT，用分类器反馈把一条 trace 改成另一条）。两类方法都撞上**防御困境（defense dilemma）**：SDR 只能靠插更多 dummy packet 换来，带宽开销随之飙升（实测 20.34%–234.33%，平均量级远超可接受范围）。作者据此提出转轴：与其在"伪装"这条路上继续优化，不如改用**二级防御 / 对抗式防御（secondary / fighting defense）**——不显著改变原始 trace，而是主动攻击 WF 分类器本身，用一小段投毒序列（P sequence）触发分类器的过拟合脆弱性。

### 3.2 现有方法的痛点和不足

- **随机伪装（零脆弱性利用）**：规则静态、实现简单，但把带宽大量浪费在与分类器无关的随机化上。实测 FRONT 需 >35.96% 开销才把 CUMUL 压到 <32.9%，而对 DF 即使开销 >62.9% 准确率仍只降到 77.3%（§II-B）。
- **配对伪装（粗粒度脆弱性利用）**：用分类器输出/梯度作为反馈，效果更好且开销更低（同样 50% 开销下 Mockingbird 下 DF 准确率约 40%，FRONT >80%），但每个网站对需要独立生成器；且网站更新频繁（作者统计新闻类网站每 10–20 分钟更新一次），需要定期重采数据更新计划，长期维护成本高。
- **共同的量纲缺陷**：SDR 单独不能可靠衡量防御——插更多包就能提高 SDR，因此必须与带宽开销联合评估（§II-A 明确否定"只看 SDR"）。
- **反例边界**：随机伪装与配对伪装的经验证据还表明"脆弱性利用粒度越细，效率越高"，但已有方法最多用到粗粒度（输出/梯度）。

### 3.3 论文的研究假设或核心直觉

三条假设链：(1) 深度 WF 分类器普遍存在**过拟合**倾向——只要能诱导它在特定 P 序列上过拟合，该分类器就会"只看 P 序列"而忽略真实 trace；(2) **模型迁移性**——不同深度模型共享相似脆弱性，因此用代理模型（surrogate）挖出的 P 序列可以迁移到未知真实攻击模型；(3) 既然分类器的输出只由 P 序列决定，那么**改变 P 序列与网站的映射**（每个用户一份 secret）就能在不改变开销的前提下打乱攻击者的预测。三者合起来把"防御"变成了"控制攻击者模型的输入-输出映射"。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 现有防御的 SDR 与带宽开销呈明显 trade-off；同类别内 SDR 越高开销越大（Tamaraw 比 FRONT/WTF-PAD 多耗 172.16% 开销换 SDR） | §II-A Observation #2、§II-B |
| 痛点提炼 | 形成"防御困境"：高 SDR 只能靠不可接受的高开销获得；配对伪装还叠加了生成器维护成本 | §II-B（Takeaway Message 1/2） |
| 问题转化 | 转为可研究问题：能否利用**更细粒度的分类器脆弱性**（而非伪装特征）来打破 SDR-开销 trade-off？ | §II-C |
| 文献定位 | 数据投毒已在通用 ML 中被证明有效，但在 WF 防御中未被系统使用；WF 场景还提供了一个特殊机会——防御者能影响攻击者的训练集 | §II-C（"we can insert the poisoned samples into training sets for WF attackers"） |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 用数据投毒诱导攻击者分类器在 P 序列上过拟合，再以用户私密 secret 打乱 P 标签-网站映射，可在极低带宽开销下获得高 SDR | §II-C、§IV-A | 实验（Table III/IV/V，SDR/BO 效率） |
| 辅助假设 1 | 代理模型（未训练的原始 DF 模型）挖出的 P 序列可迁移到其他攻击模型 | §IV-C（Basis #2，模型迁移性） | 实验（Fig. 11 surrogate 混淆矩阵，SDR 平均仅降 6.56%/8.68%） |
| 辅助假设 2 | 冲突映射（两个用户 secret 撞车）的数量可由 n/m 比值控制到 <1 | §IV-C Theorem 1 | 理论推导（E(X) < e^{n/m} − 1，取 n/m ≤ √e） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑（有保留） | DF：平均 SDR 81.83% @ 12.38% BO，效率 6.61（次优 Mockingbird 1.25）；AWF：83.32% @ 6.74%，效率 12.36；但绝对 SDR 仍低于 Tamaraw（~92.5% @ 234.33% BO） | §VI-B/Table III/IV |
| 辅助假设 1 | 支撑 | 换代理模型时 SDR 平均下降 6.56%（DF）/ 8.68%（AWF） | §VII-B/Fig. 11 |
| 辅助假设 2 | 支撑（仅理论） | E(X) < e^{n/m} − 1；且 Stinger-II 用两份 secret 把碰撞率从 p_c 降到 p_c² | §IV-C/Eq. 9-13、§VI-C |

---

## 4. 方法设计

### 4.1 方法整体流程

Stinger 分两阶段（Fig. 4）：

- **误导阶段（misleading）**：离线联合训练一个投毒序列生成器（P model，MLP）与一个代理 WF 分类器（用未训练的原始 DF 模型）。P model 吃 P 标签、吐 P 序列候选；把候选序列插进随机选取的原始 trace，喂给代理分类器；以"P 标签"为监督做交叉熵最小化。收敛即意味着代理分类器无论原始 trace 是什么都会输出 P 标签——也就是在 P 序列上过拟合。
- **欺骗阶段（deceiving）**：把 P 序列插进**攻击者的训练集**（通过部署在 Tor 客户端与中间节点的代理），让攻击者训练出的分类器同样过拟合到 P 序列；随后用用户私密 secret 打乱"P 序列 ↔ 网站"的映射。攻击者用自己的 secret 训练与验证时（验证精度接近训练精度）察觉不到过拟合，但上线攻击时因 secret 不同而大面积误判。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 训练 P model | P 标签（长度 l 控制开销） | MLP 生成器 G_p^φ 把标签映射为 P 序列候选（Eq. 1） | Seq_p | 生成投毒序列 |
| Step 2 构造被投毒 trace | 原始 trace + Seq_p | 插入操作 Tra* = Tra ⊕ Seq_p（Eq. 2）；误导阶段插完整序列 | 被投毒 trace | 供代理分类器学习 |
| Step 3 代理分类评估 | Tra* | 原始 DF 模型 WF_ψ(·) 输出预测 P̂（Eq. 3） | 预测标签 | 提供可微的优化目标 |
| Step 4 联合优化 | P 标签 vs P̂ | 交叉熵损失 argmin_{φ,ψ} L(P, P̂)（Eq. 4），Adam + 网格搜索（lr 1e−4、batch 64） | 收敛的 P model | 使分类器在 P 序列上过拟合 |
| Step 5 训练集投毒 | 攻击者采集的 trace 流 | 在客户端/中间节点按 P 序列插 dummy packet（deceiving 阶段用延迟高效插入：当前包与 P 序列格式匹配则不插，否则延迟一个包并补一个匹配的 dummy 包；随机插入两次） | 被污染的攻击者训练集 | 诱导真实攻击模型过拟合 |
| Step 6 secret 分配 | 用户 token | 按用户生成随机 secret（Eqs. 6-8：随机打乱 P 集合后取前 m 个，依次匹配敏感网站） | 每用户独立的 P↔网站映射 | 制造受害者与攻击者的映射冲突 |
| Step 7 安全分发 | token + PKI/TLS | token = 加密的当前时间；客户端存 cookie；服务器与客户端/中间节点代理经 PKI+TLS 查询 P 序列（非对称加密保护传输） | 各代理持有的 P 序列 | 防 MITM 与序列窃听 |
| Step 8 攻击失效 | 攻击者分类器 | 攻击者按自己的 secret 训练与验证（精度正常），但受害者的 P 序列映射不同 → 预测错误 | 低 SDR 的攻击 | 完成防御闭环 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| P model（MLP 生成器） | 把 P 标签转成 P 序列 | P 标签（长度 l） | P 序列向量 | 与代理分类器联合训练；部署在远端专用服务器 |
| 代理 WF 分类器 | 提供可微的优化信号 | 被投毒 trace | P 标签预测 | 选用未训练的原始 DF 模型（更易挖脆弱性 + 迁移性好） |
| Tor 客户端代理 | 插入/丢弃出向包 | 本地流 | 改写后的流 | 与中间节点代理协作 |
| Tor 中间节点代理 | 反向操作（插入入向包、丢弃出向包） | 中继流 | 改写后的流 | 选中间节点而非入口/出口：入口可能被攻击者控制、出口放包会被提前丢弃 |
| 密钥/secret 服务器 | 用户认证、secret 生成与分发 | token | secret + P 序列 | 远端部署；PKI + TLS 保护 |
| 秘密表更新机制 | 检测 P model 失效并触发重训 | 新/更新网站 trace 的验证精度 | 重训触发信号 | 3σ 规则（验证精度 < μ−3σ 即重训） |

### 4.4 公式、算法和机制解释

**（1）P 序列生成与插入。** Seq_p = G_p^φ(Lab_p)（Eq. 1）：P 标签既是生成器的种子（决定序列与分类器输出，受害者用与攻击者不同的标签即可受保护），又是分类器输出的 ground truth（要求两者格式一致）。Tra* = Tra ⊕ Seq_p（Eq. 2）为插入操作；误导阶段插完整序列，欺骗阶段用延迟/开销节省方案（匹配则跳过）。

**（2）代理优化。** 由于防御者不知道真实分类器，用代理 WF_ψ 评估（Eq. 3），并以交叉熵为目标联合优化 (φ, ψ)（Eq. 4）。作者刻意选择**未训练的原始 DF 模型**作为代理：一是 DF 是 SOTA 攻击、其脆弱性可迁移；二是未训练模型更易挖掘脆弱性。

**（3）过拟合诱导的两条依据。** Basis #1：WF 攻击者必须自己访问目标网站采集训练集，防御者因此在链路与节点上有机会污染该训练集。Basis #2：深度模型共享后门脆弱性（[18][19][30][31] 与迁移性文献 [32][33]），故代理上挖出的 P 序列可迁移。

**（4）秘密机制。** secret 是 P 序列集合到网站集合的映射 s: 𝒫′ → W（Eq. 5），满足 |𝒫′| = |W|、m ≤ n（m 为受保护网站数、n 为可用 P 序列数）。生成方式：随机打乱 𝒫 得 P̃（Eq. 6，用 NumPy random.randint），取前 m 个得 𝒫′（Eq. 7），再顺序匹配 s(p̃_i) = w_i（Eq. 8）。**冲突映射**指两个用户的 secret 出现相同映射，会让分类器认出部分网站；Theorem 1 给出期望冲突数的上界 E(X) < e^{n/m} − 1（Eqs. 9–13 推导），因此只要固定 n/m 比值（取 n/m ≤ √e）即可把冲突期望压到 <1。网站数增加时可扩展映射，但 n 不能超过可用的 P 序列数 m，否则需重训或增量训练扩大 P 序列池。

**（5）欺骗阶段的机制细节。** 攻击者用受害者的被污染 trace 训练时，训练精度与验证精度都正常（因为对同一用户 P 序列固定），无法察觉过拟合；但 secret 属用户私有，攻击者的映射与受害者不同，过拟合分类器只按 P 序列预测，于是大面积误判。作者还给出 Stinger-I / Stinger-II / Stinger-S 三个变体：I 只插一条 P 序列、II 插两条（在相同带宽下用 l=128 vs l=256 对齐）、S 假设用户与攻击者 secret 相同（秘密泄露的最坏情况）。

**（6）部署要点。** P model 离线训练（不与实时 Tor 流量交互）；可本地或远端部署，作者选远端专用服务器（P 序列体积极小，≤1M 大小可传输，用非对称加密防窃听）；用户认证用加密的当前时间作 token（存 cookie）；用 PKI 防 MITM、TLS 保 token 与 P 序列的机密性与完整性；客户端与中间节点代理凭网站 ID + token 向服务器查询 P 序列。原型基于 WFDefProxy 实现于 Tor 客户端。

### 4.5 方法优势

- **带宽开销极低**：默认配置下 DF 12.38%、AWF 6.74%、开放世界 10.24%、新型攻击场景 13.90%（§VI 各表）。
- **一个生成器服务所有网站**：与网站无关（website independent），避免了配对伪装"每对网站一个生成器"的维护负担；trace-agnostic 设计天然适配开放世界。
- **效率（SDR/BO）领先一个量级**：DF 6.61、AWF 12.36、开放世界 8.99、新型攻击 4.84–5.69，而随机伪装类只有 0.10–0.94（§VI-B Finding #3：脆弱性利用粒度越细，效率越高）。
- **对未知攻击有迁移性**：仅用代理模型即可防御 CUMUL/DF/AWF/Var-CNN/GANDaLF 与四种新攻击。
- **部署成本低**：P model 训练 18.12–33.48 分钟、推理 0.75 s 生成 2^20 条序列（单卡 RTX 2080 可支撑百万用户/0.75s 的 secret 更新）；PKI/TLS 会话建立 CPU 开销 0.5 ms（服务器）/3.1 ms（客户端）。

### 4.6 方法不足

- **绝对 SDR 不及 Tamaraw**：默认配置下 Stinger 平均 SDR 81.83%（DF）/83.32%（AWF），低于 Tamaraw 的 ~92.5%，但其开销只有后者的约 1/19；作者称把开销提到 50% 时 SDR 可接近 Tamaraw（§VI-B Finding #1）。
- **依赖"攻击者在被防御的 trace 上训练"这一前提**：若攻击者坚持用原始 trace 训练（拒绝更新或关闭 Stinger），防御退化为普通扰动；作者实测此时 Stinger 平均 SDR 与竞争者相当或略高，但优势显著缩小（§VII-A, Fig. 10；Var-CNN 上 34.29 低于竞争者均值 45.77）。
- **有额外时延**：insert 完整 P 序列带来 latency-II 平均 10.6 ms（占总时延 50–200 ms 的 5%–20%），作者自陈这是"以时延换 SDR"的 trade-off（§VI-E）。
- **秘密泄露即失效**：Stinger-S 在全部攻击下 SDR 都很低（§VI-C, Fig. 9）。
- **P model 对网站更新敏感**：在 85 个网站训练（验证精度 96.75%）后，对 10 个新网站精度跌至 52.7%；需靠 3σ 规则触发重训（10 epoch / 789 s，平均 10.6 小时触发一次）（§VII-E）。
- **自适应攻击可达约 50% SDR_o**：攻击者用原始+被防御 trace 混合训练时，Stinger 的防御被显著削弱（§VII-C, Table VII；作者称仍"fundamentally limited"，但 50% 与原始训练集下的 ≥90% 相比已明显下降）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

- **防御哲学不同**：伪装类防御改动的是**流量**（插 dummy packet 使其像别的 trace）；Stinger 改动的是**攻击者模型**（污染其训练集并控制其输出映射），原始 trace 除插入少量 P 序列外基本不动。
- **脆弱性利用粒度不同**：随机伪装用零脆弱性、配对启装用粗粒度（分类器输出/梯度），Stinger 用细粒度（模型过拟合/后门触发）。作者用 SDR/BO 效率把这一差别量化：粒度越细效率越高（DF 上 0.39/0.56/0.94 → 1.25/3.45 → 6.61）。
- **网站依赖性不同**：配对伪装需要 per-pair 生成器且对网站更新敏感；Stinger 只有一个生成器，靠 secret 表切换映射。
- **评价方式不同**：论文拒绝单看 SDR，引入**饱和度带宽**（SDR 达 >90% 所需的带宽）与 SDR/BO 效率作为核心指标。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 用数据投毒做 WF 防御 | 首次把"污染攻击者训练集"作为 WF 防御主线，而非伪装流量 | 高 | 是（可迁移到其他对抗性模型场景） |
| P 序列 + 代理模型联合训练 | MLP 生成器与未训练 DF 分类器端到端联合优化（Eqs. 1–4） | 高 | 是（黑盒模型脆弱性挖掘的通用配方） |
| 用户私密 secret 输出打乱 | 每用户独立映射 + 随机置换 + 冲突上界理论（Theorem 1） | 高 | 是（多用户对抗场景的通用技巧） |
| 延迟高效插入与 3σ 重训触发 | 匹配则跳过、随机插两次；验证精度 < μ−3σ 触发重训 | 中 | 是（工程化部署细节） |
| SDR/BO 与饱和度带宽评价 | 用效率与饱和带宽替代单一 SDR 评价防御 | 中 | 是（评测协议可复用） |

### 5.3 适用场景

- 防御者能够影响攻击者采集流程的 WF 场景（攻击者必须自行访问网站采训练集），且能推动客户端与中间节点统一部署。
- 带宽/时延敏感、无法承受 Tamaraw/WTF-PAD 级别开销的长期部署。
- 需要同时覆盖闭世界与开放世界（monitored/unmonitored 判别）的防御。
- 不适用：攻击者能拿到纯净原始 trace 并意识到投毒存在（自适应攻击下 SDR_o 约 50%）；或用户 secret 泄露的场景。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| Tamaraw (2014) | SDR 最高（~92.5%） | 开销 234.33%，效率仅 0.39 | 用 1/19 开销达到相近量级的效率优势（效率 6.61） |
| WTF-PAD (2016) | 实现简单、开销中等（61.46%） | 对 DL 攻击防御弱（DF 上 SDR 10.03%），效率 0.56 | 直接攻击分类器而非随机 padding |
| FRONT (2020) | 零延迟、对 CUMUL 有效 | 对 DF 弱（SDR 22.66%），开销 62.89% | 以细粒度脆弱性替代头部密集填充 |
| Mockingbird (2021) | 配对伪装中效果较好（平均 SDR 74.03%） | 开销 59.47%，需 per-pair 生成器 | 单生成器 + trace-agnostic，效率高 5 倍以上 |
| ALERT (2024) | 开销较低（20.34%）、可抵御对抗训练增强的攻击 | 效率 3.45，仍需按 trace 处理 | 用投毒触发替代对抗扰动生成 |
| Stinger | 开销最低（6.74%–13.90%）、效率最高、网站无关 | 绝对 SDR 略逊 Tamaraw；有时延-II；依赖训练集可污染假设 | — |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- 数据集划分：DF 与 AWF 均按 8:1:1 分训练/验证/评估（§VI-A）。
- 攻击实现：DF 输入维度 5000、lr 0.002、batch 128（网格搜索）；AWF lr 0.001、batch 256；Var-CNN batch 50 + 学习率衰减；GANDaLF 每站 90 条标注 trace、生成器/判别器 batch 32、lr 1e−4 / 5e−5（§VI-A）。
- 防御对比：Tamaraw、WTF-PAD、FRONT、Mockingbird、ALERT；Tamaraw/WTF-PAD/FRONT 不在 AWF 上评估（AWF 无时间戳信息）（§VI-A）。
- Stinger 设置：P 序列默认长度 128，P model 训练 30 epoch，lr 1e−4，batch 64，Adam；结果取 10 次运行平均（§VI-A/B）。**解析稿写作 "P model is implemented in PyTorch 3.6"，PyTorch 无 3.6 版本，疑为笔误（Python 3.6 或 PyTorch 1.x）**。
- 开放世界：95 monitored + 40,000 unmonitored（每站一条），指标用 precision/recall 与 PR-AUC，SDR 定义为 1 − AUC（§VI-D）。
- 新型攻击：Tik-Tok、Maturesc、RobustFingerprinting、Laserbeak，仅在 AWF 上（且为适配 timing 攻击增强了插入时延采样）；Mockingbird/ALERT 因不支持 timing 操纵而未参与（§VI-E）。

### 6.2 数据集

| 数据集 | 规模 | 站点数 | 采集信息 |
|---|---:|---:|---|
| DF | 95,000 traces（每站 1,000） | 95 | Sirinam 等，2016 年 2 月；Alexa top 100 首页 |
| AWF | ~2500 traces/站 | Alexa top 1200 | Rimmer 等，2017 年 1 月；首页 traces |
| DF 开放世界子集 | 95,000 monitored + 40,000 unmonitored | 95 + 40,000（每站 1 trace） | 沿用 DF 数据集 |

### 6.3 Baseline

- 攻击侧：CUMUL（104 统计特征 + RBF-SVM）、DF（CNN）、AWF-SDAE / AWF-CNN、Var-CNN（ResNet-18）、GANDaLF（半监督 GAN）；新型攻击 Tik-Tok / Maturesc / RobustFingerprinting / Laserbeak（§VI-A/E）。
- 防御侧：Tamaraw、WTF-PAD、FRONT、Mockingbird、ALERT（§VI-A）。
- 参考表：Table I 汇总既有攻击在未防御/最弱防御下的准确率，用于量化"现有防御有效但并不便宜"（§II-A）。

### 6.4 评价指标

- SDR = 1 − Accuracy = N_i/(N_c + N_i)（Eq. 14，N_c/N_i 为攻击正确/错误分类的 trace 数）。
- 带宽开销 BO = (|T′| − |T|)/|T|（Eq. 15，T′/T 为被防御/原始 trace）。
- 效率 = SDR/BO；饱和度带宽 = SDR 达 >90% 所需的带宽（越小越好）（§VI-B）。
- 开放世界：precision、recall、PR-AUC，SDR 取 1 − AUC（§VI-D）。

### 6.5 关键实验结果

**闭世界主实验（§VI-B，Table III = DF，Table IV = AWF；SDR 单位 %，括号内为 SDR/BO）**

| 数据集 | 防御 | 带宽开销 | CUMUL | DF | AWF-SDAE | AWF-CNN | Var-CNN | GANDaLF | 平均 SDR | 平均效率 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DF | Stinger | 12.38% | 80.97 | 72.14 | 91.28 | 74.87 | 94.83 | 76.91 | 81.83 | 6.61 |
| DF | Tamaraw | 234.33% | 92.55 | 92.42 | 92.13 | 92.79 | 92.66 | 94.78 | ~92.9 | 0.39 |
| DF | WTF-PAD | 61.46% | 44.57 | 10.03 | 76.44 | 27.94 | 10.02 | 37.99 | 34.50 | 0.56 |
| DF | FRONT | 62.89% | 80.77 | 22.66 | 93.14 | 58.91 | 28.18 | 72.99 | 59.44 | 0.94 |
| DF | Mockingbird | 59.47% | 81.26 | 63.44 | 87.07 | 70.00 | 62.84 | 79.59 | 74.03 | 1.25 |
| DF | ALERT | 20.34% | 69.46 | 60.00 | 82.29 | 65.19 | 82.91 | 60.72 | 70.10 | 3.45 |
| AWF | Stinger | 6.74% | 76.19 | 79.59 | 90.31 | 85.24 | 93.62 | 74.95 | 83.32 | 12.36 |
| AWF | Mockingbird | 62.32% | 76.53 | 56.96 | 75.06 | 71.32 | 69.54 | 80.29 | 71.62 | 1.15 |
| AWF | ALERT | 9.97% | 71.17 | 47.00 | 84.42 | 62.24 | 64.71 | 54.71 | 64.04 | 6.45 |

- 未防御基线（SDR）：DF 上 CUMUL 2.7、DF 1.7、AWF-SDAE 11.42、AWF-CNN 3.54、Var-CNN 2.79、GANDaLF 5.93；AWF 上 6.54/2.00/7.16/3.63/1.26/13.02。
- 平均效率（DF）：Tamaraw 0.39、WTF-PAD 0.56、FRONT 0.94、Mockingbird 1.25、ALERT 3.45、Stinger 6.61；AWF：Mockingbird 1.15、ALERT 6.45、Stinger 12.36。
- 饱和度带宽（DF，SDR>90% 所需开销）：Tamaraw 85.66%、WTF-PAD 98.95%、FRONT 90.16%、Mockingbird 88.15%、ALERT 68.74%、**Stinger 32.31%**（§VI-B, Fig. 8）。
- 结论句：Stinger 在默认配置下 SDR 略逊于 Tamaraw，但开销约为其 1/19；把开销提到 50% 时 SDR 可接近 Tamaraw。

**开放世界（§VI-D, Table V）**：Stinger BO 10.24%，SDR 88.22/95.25/92.16/95.03/95.23/86.95（CUMUL/DF/AWF-SDAE/AWF-CNN/Var-CNN/GANDaLF），平均 92.14%，效率 8.99；竞争者效率 Tamaraw 0.43、WTF-PAD 1.90、FRONT 1.22、Mockingbird 1.21、ALERT 3.55。

**新型攻击（§VI-E, Table VI，AWF）**：Stinger BO 13.90%，SDR 79.05（Tik-Tok）/67.25（Maturesc）/77.69（RobustFingerprinting）/72.35（Laserbeak），效率 5.69/4.84/5.59/5.21；对照 WTF-PAD 效率 0.12、FRONT 0.34、Tamaraw 0.38。作者同时承认该场景下时延上升（需插完整 P 序列）。

**秘密策略（§VI-C, Fig. 9）**：Stinger-II（两条序列）SDR 87.17/77.53/92.36/82.64/97.26/69.40，全面高于 Stinger-I（23.99/72.52/73.92/52.97/74.21/16.83）；对 GANDaLF 提升最大（DF +52.57、AWF +35.37 个百分点，因序列更复杂、更难被对抗式模型吸收）。Stinger-S（secret 泄露）在所有攻击下 SDR 都很低。

**未防御训练集（§VII-A, Fig. 10）**：攻击者在原始 trace 上训练时，DF 上竞争者六项 SDR 均值 61.20/43.37/70.14/53.82/45.77/57.42，Stinger 为 88.04/49.34/86.37/69.33/**34.29**/77.66——整体略高，但 Var-CNN 一项明显低于竞争者均值（诚实标注）。

**代理模型影响（§VII-B, Fig. 11）**：换用不同代理模型时 SDR 平均下降 6.56%（DF）/8.68%（AWF），即 concept drift 有限。

**自适应攻击（§VII-C, Table VII）**：混合比例 0%→90% 时，DF 上 SDR_t 13.76→55.06、SDR_i 39.13→7.14、SDR_o 52.89→62.2；AWF 上 SDR_t 14.64→49.2、SDR_i 37.06→15.77、SDR_o 51.7→64.97。作者结论：自适应攻击"根本受限"，仅约 50%。

**计算与部署开销（§VII-D）**：P model 训练 18.12 min/1495 MB（DF）、33.48 min/1493 MB（AWF）；推理 4632 MB、0.75 s 生成至多 2^20 条 P 序列（单卡 RTX 2080 可支撑 >100 万用户/0.75 s）；PKI/TLS 会话内存 <50 KB（服务器）/10 KB（客户端），CPU 0.5 ms/3.1 ms，会话有效期 20 分钟；latency-I 1.51 ms、latency-II 10.6 ms；会话建立时延（Table VIII）：LAN 中位 2.1 ms、WAN 同国 23.8 ms、跨洲中位 174.2 ms、最坏 486.5 ms。

**鲁棒性（§VII-E）**：85 站训练 → 10 个新站精度 96.75%→52.7%；重训 10 epoch 需 789 s（Table IX，逐 epoch 72–85 s）；3σ 性能跌落平均间隔约 10.6 小时。

### 6.6 优势最明显的场景

- **带宽受限的长期部署**：默认开销 6.74%–13.90%，效率超随机伪装一个数量级。
- **开放世界**：Stinger 平均 SDR 92.14% @ 10.24% 开销，而配对伪装在"一个 monitored 对应上百个 unmonitored"的极端不平衡下退化明显（每个 pair 需单独训练 transformer）。
- **攻击者不断引入新模型**：代理迁移性使新攻击（Tik-Tok/Maturesc/RobustFingerprinting/Laserbeak）仍被压到 67%–79% SDR（BO 13.90%）。
- **多用户场景**：secret 机制天然按用户区分，且冲突数可由 n/m 控制。

### 6.7 局限性

- 绝对 SDR 未超越 Tamaraw；当开销被人为拉齐时优势才完全体现。
- 依赖"攻击者训练集可被污染"的假设；混合训练的自适应攻击会显著削弱效果（SDR_o 约 50%–65%）。
- 未防御训练集场景下 Var-CNN 一项表现低于竞争者平均。
- 秘密泄露（Stinger-S）即失效；分发链路依赖 PKI/TLS 强度。
- **数值自相矛盾**：摘要与 §I 贡献的两组 SDR 提升/开销降低百分比不一致（见 §2.1 下标注）；§II-A Observation #1 的"平均降低 75.97%"与 Table I 的数值不可复现（按 Table I 计算为 79.74%）；§II-A 称配对伪装平均开销 61.78%，而 Table II 中 Mockingbird 与 ALERT 的均值为 39.91%。
- 论文未与配对伪装的最新方法（如 AWA 等需要 per-pair 生成器的方法）做统一的开放世界对比（Mockingbird/ALERT 因不支持 timing 操纵被排除在新型攻击实验外）。

---

## 7. 学习与应用

### 7.1 是否开源？

是。原型系统（Tor 客户端上的 Stinger）在 https://github.com/sxy888/Stinger-prototype ；详细实验数据在 https://github.com/sxy888/Stinger/blob/main/experiment.md 。解析稿还说明 Tamaraw/WTF-PAD/FRONT/Mockingbird 的实现分别取自其原始开源代码。

### 7.2 复现关键步骤

1. 用 MLP 实现 P model（输入 P 标签、输出长度 l 的序列），并准备未训练的原始 DF 模型作代理分类器。
2. 按 Eq. 4 联合训练：随机抽原始 trace → 插入 P 序列候选 → 代理分类器预测 → 交叉熵反传（Adam，lr 1e−4，batch 64，30 epoch）。
3. 生成随机 secret：打乱 P 集合取前 m 个元素与网站顺序匹配（Eqs. 6–8），并保证 n/m ≤ √e 控制冲突期望。
4. 部署客户端与中间节点代理（可基于 WFDefProxy），实现"匹配即跳过、否则延迟一包并补一个 dummy 包"的插入逻辑，并随机插入两次。
5. 用 PKI/TLS + token（加密时间戳）完成用户认证与 P 序列分发。
6. 用 SDR/BO 与饱和度带宽评估，并与 Tamaraw/WTF-PAD/FRONT/Mockingbird/ALERT 在相同开销下对比。

### 7.3 关键超参数、预处理和训练细节

- P 序列默认长度 l = 128（开销随 l 线性增长；扫描 {32, 64, 128, 256, 512}）；Stinger-II 用 l=256 以对齐 Stinger-I 的带宽。
- P model：MLP，30 epoch 收敛，Adam，lr 1e−4，batch 64；数据来自 DF 数据集（即使防御 AWF 也用 DF 训练 P model）。
- 攻击超参：DF 输入维度 5000、lr 0.002、batch 128；AWF lr 0.001、batch 256；Var-CNN batch 50；GANDaLF 每站 90 条标注 trace、lr 1e−4/5e−5、batch 32。
- 重训触发：验证精度 < μ − 3σ；实测平均 10.6 小时触发一次，重训 10 epoch/789 s。
- Flask 注：解析稿 "PyTorch 3.6" 疑为笔误（**解析稿未明确**真实版本）。

### 7.4 能否迁移到其他任务？

- **"污染训练集 + 触发序列"范式**可迁移到任何攻击者必须自行采样的对抗场景（如流量分类器、恶意流量检测器的鲁棒性研究，或作为红队手段评估数据采集环节的可信性）。
- **代理模型挖脆弱性 + 迁移性假设**是黑盒场景下的通用配方，可直接对应到本文的"用未训练 DF 模型"做法；换任务时需重新验证迁移率（本文给出 6.56%/8.68% 的下降幅度作为参考量级）。
- **per-user secret 打乱映射**是一种低成本的多用户差异化机制，可用于任何"模型输出可被外部触发控制"的防御设计。
- **SDR/BO 效率 + 饱和度带宽**是防御评测的通用改进，可直接借用到其他流量防御论文的评测协议中。
- **风险**：该方法的有效性完全建立在攻击者采集-训练流程可被污染之上；若迁移场景中攻击者的数据来源不可控（例如使用公开数据集训练），则范式不成立。

### 7.5 对我的研究有什么启发？

- 本文是"**把防御问题转成攻击问题**"的典型样本：不去比谁伪装得更像，而是问"我能不能控制对手模型的输入-输出映射"。这类换轴思路在写 motivation 时非常有说服力。
- 评价指标的设计值得学习：作者先证明"单看 SDR 不可靠"（插包越多 SDR 越高），再引入效率与饱和度带宽——**先论证指标的必要性，再使用指标**。
- 注意本文的**数值一致性风险**：摘要与贡献段的百分比不一致、Observation #1 的 75.97% 不可复现。我在引用任何数字（尤其是写综述表格）时必须以表格数值为准并自行核算。
- 对"防御评测"研究的启示：未防御训练集实验（Fig. 10）与自适应攻击实验（Table VII）是防御类论文最容易被审稿人攻击的两点，主动做并主动报告劣势项（如 Var-CNN 34.29 低于竞争者均值）反而增强可信度。
- 其"3σ 触发重训 + 789 s 重训成本"给出了防御方案可维护性的量化范式，可复用到其他需要长期运行的防御系统。

---

## 8. 总结

### 8.1 核心思想

> 不伪装流量，而是投毒攻击者的模型。

### 8.2 速记版 Pipeline

1. MLP 生成器（P model）与未训练的代理 DF 分类器联合训练，产出能诱导过拟合的 P 序列（Eqs. 1–4）。
2. 在 Tor 客户端与中间节点代理上把 P 序列插入受害者流量（欺骗阶段用"匹配即跳过"的延迟高效插入，随机插两次）。
3. 攻击者采到被污染的训练集，训练出的分类器只在 P 序列上做判别。
4. 每个用户分配随机 secret（P 序列集合到网站集合的映射，Eqs. 5–8），受害者与攻击者映射不同 ⇒ 攻击者预测错位。
5. 用 n/m ≤ √e 控制冲突映射期望（Theorem 1，E(X) < e^{n/m} − 1）。
6. 以 SDR/BO 效率与饱和度带宽评估：DF 6.61、AWF 12.36、开放世界 8.99。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]]
- [[encrypted-traffic-analysis]]

### 9.2 相关方法

- [[convolutional-network]]（代理 WF 分类器与 DF 攻击均为 CNN；本文核心的"数据投毒 + 生成器"路线在白名单中暂无对应页）

### 9.3 相关任务

- [[website-fingerprinting]]

### 9.4 可更新的综述页面

- [[survey-website-fingerprinting]]（补充"二级防御 / 投毒防御"这一防御分类维度）

### 9.5 可加入的对比表

- [[method-comparison-table]]（新增 Stinger：投毒式 WF 防御路线与 SDR/BO 效率指标）
- [[open-source-registry]]（原型系统 https://github.com/sxy888/Stinger-prototype 已开源）
- [[motivation-pattern-comparison]]（动机写法：先用"防御困境"量化现有方法的失败，再换轴到二级防御）

### 9.6 相关论文笔记（KB 已有）

本文引用：

- [[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]]（DF [4]，代理分类器 + 主要被防御攻击 + 训练 P model 的数据来源）
- [[2020-USENIX-Zero-delay_Lightweight_Defenses_against_Website_Fingerprinting]]（FRONT [17]，随机伪装对比防御）
- [[2020-CCS-TrafficSliver__Fighting_Website_Fingerprinting_Attacks_with_Traffic_Splitting]]（TrafficSliver [16]，相关防御）
- [[2024-TIFS-WFDefProxy__Real_World_Implementation_and_Evaluation_of_Website_Fingerprinting_Defenses]]（WFDefProxy [34]，原型的实现基础）
- [[2023-USENIX-Subverting_Website_Fingerprinting_Defenses_with_Robust_Traffic_Representation]]（Shen 等 [36]，即 RobustFingerprinting 新型攻击）
- [[2023-CCS-Realistic_Website_Fingerprinting_by_Augmenting_Network_Traces]]（Bahramali 等 [52]，提升 WF 在未观测网络条件下的表现）

主题相邻（本文未引用）：

- [[2022-S&P-Surakav__Generating_Realistic_Traces_for_a_Strong_Website_Fingerprinting_Defense]]（同为 WF 防御）
- [[2026-TIFS-TrapFlow__Controllable_Website_Fingerprinting_Defense_via_Dynamic_Backdoor_Learning]]（后门学习式防御，与本文"主动控制分类器"同思路）
- [[2025-TIFS-WF-A2D_Enhancing_Privacy_With_Asymmetric_Adversarial_Defense_Against_Website_Fingerprinting]]（对抗式防御）
- [[2025-WSDM-DTPN__A_Diffusion-based_Traffic_Purification_Network_for_Tor_Website_Fingerprinting]]（净化式防御，可用于横向比较防御范式）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 现有伪装防御陷入"SDR-带宽开销"防御困境，开销区间 20.34%–234.33% | Table II + Observation #2 | §II-A |
| 脆弱性利用粒度越细，防御效率越高（随机 0.39–0.94 / 配对 1.25–3.45 / 投毒 6.61，DF） | Table III 效率列与 Finding #3 | §VI-B |
| 默认配置 Stinger 平均 SDR 81.83%（DF，12.38% 开销）与 83.32%（AWF，6.74% 开销） | Table III/IV | §VI-B |
| Stinger 绝对 SDR 略逊于 Tamaraw（~92.5%），但后者开销高约 19 倍 | Finding #1 + Table III | §VI-B |
| 饱和度带宽（SDR>90%）DF 上 Stinger 仅 32.31%，其他防御 68.74%–98.95% | Fig. 8 | §VI-B |
| P 序列条数很关键：Stinger-II 两条序列全面优于 Stinger-I，对 GANDaLF 提升 52.57/35.37 个百分点 | Fig. 9 | §VI-C |
| 代理模型与真实模型不一致时存在 concept drift，但 SDR 平均仅降 6.56%（DF）/8.68%（AWF） | Fig. 11 | §VII-B |
| 自适应攻击把 SDR_o 压到约 50%–65%，作者称其"根本受限" | Table VII | §VII-C |
| 未防御训练集下 Stinger 整体略优于竞争者，但 Var-CNN 一项（34.29）低于竞争者均值（45.77） | Fig. 10 | §VII-A（本笔记核对） |
| 秘密泄露（Stinger-S）下防御基本失效 | Fig. 9 | §VI-C |
| P model 对网站更新敏感：新网站精度 96.75%→52.7%，靠 3σ 规则触发重训（10.6 小时/789 s） | §VII-E + Table IX | §VII-E |
| 理论保证：冲突映射期望 E(X) < e^{n/m} − 1，取 n/m ≤ √e 可压到 <1 | Theorem 1（Eqs. 9–13） | §IV-C |
| **数值矛盾 1**：摘要称 SDR 提升 20.37%/22.83%、开销降低 85.88%/81.35%；§I 贡献称 32.44%/22.33% 与 75.71%/83.85% | 摘要 vs §I | §2.1 标注 |
| **数值矛盾 2**：§II-A Observation #1 称现有防御平均降低攻击准确率 75.97%，按 Table I 计算为 79.74%（绝对）或约 79.0%（相对） | Table I 与正文核对 | §II-A（本笔记核对） |
| **数值矛盾 3**：§II-A 称配对伪装平均开销 61.78%，按 Table II（Mockingbird 59.47%、ALERT 20.34%）为 39.91% | Table II 与正文核对 | §II-A（本笔记核对） |
| Table II 中 Stinger 的 Year 标为 2025，与批次分配年份 2026 不一致 | Table II | §VI 相关表格（本笔记核对） |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-TIFS-Stinger__A_Light-Weight_Website_Fingerprinting_Defense_Through_Poisoning_Packet_Sequences.pdf
- MinerU Markdown：02-parsed-markdown/2026-TIFS-Stinger__A_Light-Weight_Website_Fingerprinting_Defense_Through_Poisoning_Packet_Sequences.md

---

## 12. 后续问题

- 摘要与贡献段的百分比为何不一致？两组数字（20.37/22.83 & 85.88/81.35 vs 32.44/22.33 & 75.71/83.85）应如何对应到具体表格？需要向作者或代码仓库确认。
- Stinger 的 SDR 是在"攻击者用被防御 trace 训练"的前提下测得的；若攻击者使用公开数据集（如 DF 原始发布版）训练，防御是否还有效？论文只做了混合训练实验，未做"完全纯净外部训练集"实验。
- Table VII 的 SDR_i 定义（SDR_o − SDR_t）与 SDR_o 的口径需要更仔细的解释：为什么 SDR_t 随投毒比例上升而 SDR_o 反而是 U 形？
- P 序列长度 l 与开销、SDR 的定量关系只在 Fig. 8 的饱和度曲线上展示；l 从 32 到 512 的逐点数值未在表格中给出。
- Stinger 与 Tor 实际部署的兼容性（如与流量填充、padding 机制、其他 WF 防御并用）未评估。
- "PyTorch 3.6" 是否为笔误？代码仓库中的真实环境配置需要确认。

---

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

论文从一个**二选一的困局**开场：想防住 WF，就得付出带宽代价（伪装类防御的"防御困境"）。作者用 Table I/II 与 Fig. 2 把这个困局量化成一张 trade-off 曲线，再指出所有伪装类方法共享同一根因——它们只在改**流量**，从不碰**分类器**。转折点是"二级防御"的引入：既然分类器有脆弱性，且脆弱性利用的粒度决定了效率（零脆弱性 0.39 → 粗粒度 3.45 → 细粒度 6.61），那就直接投毒模型。结论是：Stinger 以 1/19 的开销接近 Tamaraw 的效果，并在开放世界与新型攻击场景把效率优势拉到 2–3 倍。最后作者主动暴露三条软肋（依赖训练集可污染、秘密泄露即失效、时延上升）并给出 3σ 重训机制作补偿。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 用"随机伪装易破 + 配对伪装维护贵"两句话否定既有范式，再给出 Stinger | 承诺 | "only maintains one generator for all websites" |
| Introduction | 铺开伪装分类（Fig. 1 三类）、指出两个设计挑战、给出五条贡献 | 定位 | 从"伪装流量"转到"投毒模型" |
| Preliminaries (§II) | 用 Table I/Table II/Fig. 2 三轮实验证据把"防御困境"坐实 | 建立缺口 | "SDR alone cannot serve as a reliable evaluation metric" |
| Threat Model (§III) | 明确被动本地窃听者 + 代理部署位置（客户端/中间节点） | 设定边界 | 选择中间节点而非入口/出口的理由 |
| Method (§IV) | 误导 + 欺骗两阶段，公式与 Theorem 1 | 兑现 | secret 机制把"过拟合"转成"可控的输出打乱" |
| Deployment (§V) | 训练、部署、分发、插入的工程细节 | 说明可落地性 | 远端服务器 + PKI/TLS + 延迟高效插入 |
| Experiments (§VI) | SDR vs 防御、SDR vs 开销、secret 策略、开放世界、新型攻击 | 证据链 | 饱和度带宽（32.31% vs 68.74%+） |
| Discussion (§VII) | 未防御训练集、代理模型、自适应攻击、计算开销、鲁棒性 | 自我审查 | "adaptive attacks remain fundamentally limited" |
| Conclusion (§IX) | 复述"主动投毒对手模型"的新视角 | 收口 | — |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 性能瓶颈 | 防御困境：SDR 与带宽开销不可兼得 | 矛盾证据（Fig. 2 的 trade-off 曲线 + Table II 的开销区间） | §II-B |
| 理论缺陷 | 随机伪装"零脆弱性利用"、配对伪装只用粗粒度反馈，导致带宽浪费 | 机理归因（把效率差异归因到脆弱性利用粒度） | §II-C |
| 场景缺失 | 配对伪装需要 per-pair 生成器，无法适应网站频繁更新（10–20 分钟级） | 成本论证（维护成本 + 更新频率统计） | §II-B |
| 评估不足 | 单看 SDR 会误导（插包越多 SDR 越高） | 指标批判 + 引入效率与饱和度带宽 | §II-A/B |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 预实验（Table I/II, Fig. 2） | "矛盾证据"：先用他人方法的数据把困局量化 | 为"换轴"提供必要性 |
| 主实验（Table III/IV） | "对比碾压 + 承认次优"：效率碾压、绝对 SDR 诚实承认不如 Tamaraw | 兑现核心主张（低开销高效率） |
| 饱和度带宽（Fig. 8） | "曲线归因"：用 32.31% 的饱和点证明开销效率 | 把"低开销"从单点变成曲线性质 |
| secret 消融（Fig. 9） | "消融归因"：I/II/S 三变体定位机制贡献与失效边界 | 证明秘密机制是核心 |
| 开放世界（Table V） | "场景扩展"：证明 trace-agnostic 设计的天然适配性 | 扩大适用面 |
| 新型攻击（Table VI） | "泛化验证"：对 4 种新攻击仍有效，同时承认时延上升 | 提前回应"只对训练过的攻击有效"质疑 |
| 讨论章（Fig. 10/11, Table VII） | "自我攻击"：未防御训练集、代理漂移、自适应攻击三条反向实验 | 用诚实的劣势报告换取可信度 |
| 开销与鲁棒性（Table VIII/IX） | "工程可行性" | 支撑"可落地"的主张 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 用两个既有范式的失败（随机伪装易破、配对伪装贵）并列开场，再给本文第三条路 | "否定 A、否定 B、给出 C"的三段式开篇 |
| Gap 提出方式 | 不空谈"现有方法不够好"，而是先自己做实验量化困境（Fig. 2 的 trade-off 曲线） | 用自测实验把 gap 变成可测量的曲线，而非引用文献说"效果不佳" |
| 方法论证逻辑 | 两个设计挑战（如何找未知分类器的脆弱性、如何构造投毒）与两条解法（过拟合诱导、代理迁移性）一一对应 | 把"设计难点"显式编号，再逐条给出机制，读者能直接对照 |
| 实验组织逻辑 | 先否定单一指标（SDR），再引入新指标（效率、饱和度带宽）并以此重排所有对比 | 用"指标批判"重构实验叙事，让新方法在新指标下自然领先 |
| 局限性讨论方式 | 用整章 Discussion 做三条反事实实验（未防御训练集、换代理、自适应攻击），并承认时延代价与 Var-CNN 一项的劣势 | 把"可能的攻击面"写成实验章节，而不是一句 future work |
| 最值得借鉴的一句话/一段结构 | "We call the trade-off between SDR and bandwidth overheads defense dilemma: high SDR can be achieved only by consuming prohibitively high bandwidth overheads."（§II-A）——用一个命名概念（defense dilemma）把复杂现象固定下来，后文所有论证都可以回指它 | 为论文的核心矛盾起一个可复用的名字（如本库中的"WF 攻击-防御极限"类提法），全篇反复引用，形成叙事锚点 |

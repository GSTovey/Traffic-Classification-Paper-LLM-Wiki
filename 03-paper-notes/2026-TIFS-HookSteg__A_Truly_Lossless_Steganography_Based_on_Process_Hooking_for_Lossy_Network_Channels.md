---
type: paper
title_original: "HookSteg: A Truly Lossless Steganography Based on Process Hooking for Lossy Network Channels"
title_cn: "HookSteg：面向有损网络信道的基于进程 Hook 的真无损隐写"
authors: ["Mingliang Zhang", "Yi Zhang", "Yanmei Liu", "Wentong Fan", "Xiangyang Luo"]
year: 2026
venue: "IEEE TIFS 2026"
doi: "10.1109/tifs.2026.3707784"
url: "https://doi.org/10.1109/tifs.2026.3707784"
pdf: "00-inbox/PDFs/2026-TIFS-HookSteg__A_Truly_Lossless_Steganography_Based_on_Process_Hooking_for_Lossy_Network_Channels.pdf"
mineru_md: "02-parsed-markdown/2026-TIFS-HookSteg__A_Truly_Lossless_Steganography_Based_on_Process_Hooking_for_Lossy_Network_Channels.md"
status: processed
reading_level: L2
research_area: []
task: []
method: []
dataset: ["BossBase v1.01"]
code: "unknown"
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

# HookSteg: A Truly Lossless Steganography Based on Process Hooking for Lossy Network Channels

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | HookSteg: A Truly Lossless Steganography Based on Process Hooking for Lossy Network Channels |
| 中文标题 | HookSteg：面向有损网络信道的基于进程 Hook 的真无损隐写 |
| 作者 | Mingliang Zhang, Yi Zhang, Yanmei Liu, Wentong Fan, Xiangyang Luo（信息工程大学（郑州）、河南省网络空间态势感知重点实验室等；Xiangyang Luo 为该实验室教授） |
| 年份 | 2026 |
| 会议/期刊 | IEEE Transactions on Information Forensics and Security (TIFS) 2026；DOI 10.1109/tifs.2026.3707784（由主代理分配给出，解析稿正文未印 DOI） |
| 研究方向 | 信息隐藏 / 图像隐写（image steganography）在**有损信道**（社交平台压缩、缩放、水印）下的鲁棒传输；客户端进程 Hook 与逆向分析 |
| 任务类型 | 隐蔽通信：让 stego 图像经社交平台客户端处理（压缩/缩放）后仍能被接收方**逐比特无误**提取；不改动既有隐写算法 |
| 方法关键词 | 进程 Hook（Frida/Objection）、MitM + eBPF 双验证定位攻击节点、语法-语义联合特征（SHS/ESS）、动态污点追踪 + 调用栈回溯定位有损函数、客户端零拷贝绕过、自适应绕过策略（比较攻击前后提取精度）、无损信道/时间/内存三项复杂度定理 |
| 数据集 | BossBase v1.01（1,000 张 5,000×5,000 封面图，Q_f=75/85）；生成式方法各自公开预训练模型（各 1,000 张） |
| 是否开源 | 解析稿未提及代码仓库（写 unknown） |
| PDF | 00-inbox/PDFs/2026-TIFS-HookSteg__A_Truly_Lossless_Steganography_Based_on_Process_Hooking_for_Lossy_Network_Channels.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-TIFS-HookSteg__A_Truly_Lossless_Steganography_Based_on_Process_Hooking_for_Lossy_Network_Channels.md |

---

## 1. 一句话总结

> HookSteg 不去做更鲁棒的隐写算法，而是用进程 Hook 在客户端**直接绕过**社交平台的压缩/缩放指令，使 stego 图像逐比特原样上传：在 Youku/Kehua/Hiferr/Kutumb 四个真实场景（Q_f=80/60/100/80）中把 10 种现有隐写方法的提取精度平均提升 36.63%，定位有损函数的效率较人工逆向提升 94.34%。

---

## 2. 摘要翻译

### 2.1 摘要原文

Covert communication often relies on image steganography to transmit sensitive data such as commercial secrets. Any minor bit error can lead to catastrophic consequences, which imposes extremely high demands on the zero-error transmission of secret information. However, existing robust image steganographic schemes still fail to guarantee zero-error recovery of secret bits when resisting hybrid attacks such as compression and scaling on social platforms. To address this issue, we propose a lossless steganographic method called HookSteg, which bypasses lossy attacks on social platforms through process hooking, thereby achieving lossless steganography. This method first identifies nodes affected by lossy attacks through tracking whether image data has been compromised. Subsequently, a method for capturing lossy attack instructions is proposed based on syntax-semantic joint features and dynamic taint tracking techniques. Finally, process hooking is utilized to bypass lossy attack instructions, ensuring the lossless transmission of secret information. Experimental results on transmission scenarios with tens of millions of daily active users, such as Youku and Kutumb, demonstrate that HookSteg is general and requires no modifications to existing steganographic algorithms. It achieves, for the first time, lossless transmission of secret information in real-world scenarios, with an average improvement in extraction accuracy of 36.63%. Additionally, its efficiency in locating attack instructions is improved by 94.34% compared to traditional manual reverse engineering methods. Furthermore, this study resolves the tradeoff among embedding capacity, security, and robustness, enabling steganography to focus on enhancing security and capacity, thereby providing a general and efficient solution for lossless steganography.（完整摘要，连字 "afected/eficiency/tradeof" 已还原）

### 2.2 摘要中文翻译

隐蔽通信常依赖图像隐写传输商业机密等敏感数据。任何微小的比特错误都可能带来灾难性后果，这对秘密信息的零错误传输提出了极高要求。然而，现有鲁棒图像隐写方案在抵抗社交平台上的压缩与缩放等混合攻击时，仍无法保证秘密比特的零错误恢复。为此，我们提出一种基于进程 Hook 的无损隐写方法 HookSteg，通过进程 Hook 绕过社交平台上的有损攻击，从而实现无损隐写。该方法首先通过追踪图像数据是否被破坏来识别受有损攻击影响的节点；随后，基于语法-语义联合特征与动态污点追踪技术提出有损攻击指令的捕获方法；最后利用进程 Hook 绕过有损攻击指令，确保秘密信息的无损传输。在 Youku、Kutumb 等日活数千万的传输场景上的实验表明，HookSteg 具有通用性且无需修改任何现有隐写算法；它首次在真实场景中实现了秘密信息的无损传输，提取精度平均提升 36.63%；其定位攻击指令的效率较传统人工逆向工程方法提升 94.34%。此外，本研究解决了嵌入容量、安全性与鲁棒性之间的权衡，使隐写算法可以专注于提升安全性与容量，为无损隐写提供了通用且高效的解决方案。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 隐蔽通信的核心诉求是"传输行为本身不可见"，图像隐写因此成为主流载体；但在高价值数据场景（商业机密）中，**任何比特错误都可能致命**，对零错误传输提出硬要求（§I）。
- 社交平台为节省带宽与优化体验，会对上传图像做压缩、缩放、加水印等处理，直接破坏 stego 图像导致提取失败（§I）。
- 现有研究（修改式/映射式/生成式三大类）都走"增强算法鲁棒性"的路线，但面对真实平台**未知、自动化的混合攻击**仍无法保证完全提取；且鲁棒性、容量、安全性三者相互制约（§I、§II-B、§V-D）。
- 作者的关键转念：与其让隐写算法去"抗"攻击，不如在客户端**让攻击根本不发生**——用进程 Hook 绕过有损处理链路（§I、§III-A）。

### 3.2 现有方法的痛点和不足

| 现有方法/路线 | 痛点 |
|---|---|
| 修改式隐写（J-UNIWARD、DMAS、JCRISBE、SCRIPT、ROAST 等） | 靠改像素/DCT 系数嵌入，天然引入失真可能暴露隐写痕迹；面对平台混合攻击提取精度跌至约 50%（≈随机猜测）（§II-B、Table VI/VII） |
| 映射式隐写（coverless / 深度特征映射） | 鲁棒性强但**嵌入容量过低**，不满足社交平台的高容量传输需求（§II-B、§V-D 明确排除出对比） |
| 生成式隐写（StegaDDPM、GSD、PARIS、ERGI、TransStego） | 非鲁棒方法被攻击后同样跌至 ~50%；鲁棒方法（PARIS/ERGI/TransStego）也对未知攻击敏感（如 Kutumb 下 ERGI −18.11%）（Table VIII） |
| 传统静态分析 + 动态调试定位处理函数 | 需要人工分析整个代码库，大型 App 反编译代码难读且可能混淆/加密，效率极低（§III-C） |
| 通用鲁棒隐写编码（纠错码、抖动调制） | 只能"容忍"攻击而非消除，无法保证零错误（§II-B、§I） |

### 3.3 论文的研究假设或核心直觉

核心直觉：**若水印/压缩等有损操作发生在客户端进程内，那么在客户端 Hook 掉承载该操作的函数，就能让 stego 图像零改动地上传；此时平台侧（若不再处理）收到的就是与本地完全一致的像素矩阵，接收方按原算法即可无损提取**。由此派生出三个可操作子问题：(1) 如何判定目标 App 的图像处理是否**仅在客户端**发生（用 MitM 拦截上传图像与下载图像做像素矩阵比对；不可行时用 eBPF 在内核抓客户端本地图像数据兜底）；(2) 如何在大规模反编译代码中**快速定位**有损函数（语法-语义联合特征筛出可疑语句 → Hook 触发 + 调用栈回溯逐个验证）；(3) 绕过是否总是最优（有时攻击反而"修正"了生成式方法的分布偏差使精度升高，故引入自适应策略：比较攻击前后提取精度 $e_a$ 与 $e_u$ 再决定绕不绕）（§III-B–E）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 社交平台客户端会对上传图像做压缩/缩放/水印；stego 图像经真实平台后提取精度跌破 50%（随机猜测水平） | §I、§V-D、Table VI/VII |
| 痛点提炼 | 敏感数据传输要求零错误，而"提升算法鲁棒性"的路线在真实混合攻击下无法保证完全提取；高容量与高鲁棒性难以兼得 | §I、§II-B、§V-D |
| 问题转化 | 把"如何设计更鲁棒的隐写算法"转化为"如何让有损处理在客户端不发生"——即定位并绕过处理链路中的有损函数 | §III-A |
| 文献定位 | 三类隐写（修改/映射/生成）均属"算法侧增强"；**无人从系统侧（进程 Hook 绕过处理链）解决该问题**；且已有的代码定位手段依赖人工逆向，效率低 | §II-B、§III-C |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 客户端有损处理可在进程 Hook 层被完全绕过，从而在社交平台上实现逐比特无损的隐写传输，且不改变任何既有隐写算法 | §III-A、§III-D（Hook(f_l, I_s)=I_s，Eq. 8） | 四个真实平台场景（Youku/Kehua/Hiferr/Kutumb）× 10 种隐写方法的端到端提取精度（Table VI–VIII） |
| 辅助假设 1 | 多数 App 的图像处理发生在客户端，且在有损函数被绕过后上传图像与本地 stego 完全一致 | §III-B（MitM 比对 $I'_s$ 与 $I''_s$） | top 50 应用宝 App 的节点识别统计（Table III）：客户端独占处理者可用 HookSteg 通道 |
| 辅助假设 2 | 语法-语义联合特征 + 动态污点追踪可在可接受成本内定位有损函数 | §III-C/D（SHS/ESS、Algorithm 1） | 7 个 App 的检索量-过滤量-可疑函数提取量与效率提升（Fig. 6） |
| 辅助假设 3 | Hook 通道的时间/内存开销与图像尺寸无关（常数级） | §IV-B/C（Theorem 2/3） | 4 种分辨率（512²–4096²）× 3 档质量因子下的处理时间对比（Fig. 8） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设（无损绕过） | 支撑 | 修改式：HookSteg 通道下提取精度与"无攻击"完全一致（Change 0.00%），均值由 50.03% 回到 94.64%；生成式：均值由 74.08% 回到 99.27% | Table VI、Table VIII |
| 辅助假设 1（客户端节点判定） | 部分支撑 | MitM 在 70.00% 社交类 App 中可用；MitM+eBPF 联合验证 76.66% 的 App；Pinterest/Reddit 等服务端处理者为反例 | §V-B、Table III |
| 辅助假设 2（定位效率） | 支撑 | 平均效率提升 94.34%，且所有 App 的有损函数都落在提取出的可疑语句集合内 | §V-C、Fig. 6 |
| 辅助假设 3（常数开销） | 支撑 | HookSteg 通道处理时间恒为 1 ms，不受图像尺寸与质量因子影响；传统通道随尺寸上升 | §V-E、Fig. 8 |

---

## 4. 方法设计

### 4.1 方法整体流程

HookSteg 分两大阶段（Fig. 3）：**预处理阶段**（三步——识别攻击节点、提取可疑函数、定位有损函数）与**隐蔽通信阶段**（发送方 Hook 绕过并上传；接收方按原算法提取）。预处理先确认目标 App 的 stego 图像是否**只在客户端被处理**；若是，则用语法-语义特征筛选图像处理语句，再用动态污点追踪 + Hook 触发 + 调用栈回溯，逐个验证直到找到可被成功绕过且不引发程序异常的函数 $f_l$；通信阶段发送方以零拷贝方式 Hook $f_l$ 绕过处理，将 stego 图像原样上传，接收方像普通用户一样下载后用预先约定的提取算法恢复秘密信息（§III-A）。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 识别攻击节点 | 目标 App + stego 图像 $I_s$ | MitM 拦截：C 发连接请求 → M 伪造响应并与 S 建链 → C 处理后上传 $I'_s$ → M 截存并转发 → 下载平台最终图 $I''_s$，比对像素矩阵；$I'_s\equiv I''_s$ 判定"仅客户端处理"（可建无损信道），否则"服务端参与"（不可）（Eq. 1–2） | 攻击节点判定结论 | 决定该方法对该 App 是否适用 |
| Step 2 eBPF 兜底 | 同 Step 1（MitM 不可用时） | 编写 eBPF 程序 E 载入内核，监控客户端进程 $P_c$ 的网络通信，按目的端口/协议过滤抓包，从网络缓冲重组图像 $I'_s$ 并落盘后比对 | 攻击节点判定结论 | MitM 受限场景的补充验证手段 |
| Step 3 提取可疑函数（SHS） | App 反编译得到的低级语言 → 转换后的高级语句集合 $S_h$ | 按图像处理语义特征码（compress / rotate / resize / upload，Table I）过滤：$S_v=\{s_h\mid \exists p\in P, p\in S_h\}$ | 特征语句集合 $S_v$ | 语义层粗筛 |
| Step 4 提取可疑函数（ESS） | $S_v$ + 句法特征 R | 按语句句法格式（Fig. 5）进一步切分过滤：$S_c=\{s_v\mid\exists s_v\in S_v, r\in R\}$；含可疑语句的函数即"可疑函数" | 可疑语句集合 $S_c$ 与可疑函数 | 句法层细筛，缩小范围 |
| Step 5 定位有损函数 | 可疑函数集合 + $I_s$ | 对第 i 条可疑语句对应的函数 Hook 监控，触发时记录入参/返回值/调用栈 $S_i$；从栈顶 $s_i^0$ 起依次尝试四种 Hook 策略（改参数 / 拦截执行 / 构造返回对象 / 替换上传路径，Table II），若 $I_s=I'_s$ 则该函数为 $f_l$，否则回溯到下一个栈帧重试（Algorithm 1、Eq. 7–8） | 有损函数 $f_l$ | 精确定位可绕过的处理函数 |
| Step 6 发送方隐蔽通信 | 秘密信息 m + 封面图 $I_c$ | $I_s=\mathrm{Hide}(I_c,m)$ → 依自适应策略决定是否 Hook：$e_a>e_u$ 时上传 $\mathrm{Hook}(f_l,I_s)$，否则按常规流程直接上传 $I_s$（Eq. 9–11） | 平台上的图像 | 保证上传图像不被有损处理 |
| Step 7 接收方提取 | 下载的图像 $I'_s$ | 用与 Hide 对应的提取函数 $m'=\mathrm{Ext}(I'_s)$；无需 root 或特殊配置（Eq. 12） | 秘密信息 $m'$ | 完成无损接收 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 攻击节点识别（MitM + eBPF） | 判定图像处理发生在客户端还是服务端 | 上传/下载图像 | 节点判定（可行性闸门） | 前置于全部后续步骤 |
| 可疑函数提取（SHS + ESS） | 语义 + 句法两级筛选定位候选处理语句与函数 | 反编译 → 高级语句集合 | 可疑语句集合 $S_c$ | 为动态验证缩小范围 |
| 有损函数定位（Hook + 调用栈回溯 + 污点追踪） | 动态触发 + 逐栈帧验证，确定可绕过的 $f_l$ | 可疑函数、$I_s$ | 有损函数 $f_l$ | 产出通信阶段所需的 Hook 目标 |
| 绕过执行（Hook 策略集 L） | 以零拷贝方式拦截并绕过 $f_l$ 的调用 | $f_l$、$I_s$ | 未被修改的 $I_s$ | 通信阶段的核心动作 |
| 自适应选择 | 比较 $e_a$ 与 $e_u$ 决定是否绕过 | 预攻击前后提取精度 | 上传路径选择 | 处理"攻击反而提升精度"的反常情形 |

### 4.4 公式、算法和机制解释

- **MitM 节点判定（Eq. 1–2）**：原链路 $C\leftrightarrow S$ 变为 $C\leftrightarrow M\leftrightarrow S$；通过比较中间截获的 $I'_s$ 与平台下载的 $I''_s$ 像素矩阵是否恒等来判定处理节点。
- **语义/句法筛选（Eq. 3–6）**：$S_v=\mathrm{SHS}(S_h,P)$、$S_c=\mathrm{ESS}(S_v,R)$；$P$ 为图像处理语义特征集合（compress/rotate/resize/upload），$R$ 为句法特征集合；含可疑语句的函数即"可疑函数"。
- **有损函数定义（Eq. 7–8）**：找最小正整数 q 使 $j=q$ 时 $I_s=I'_s$、$j\in[0,q)$ 时 $I_s\neq I'_s$；Hook 操作定义为 $\mathrm{Hook}(f_l,I_s)=I_s$——拦截调用并应用策略集 L 绕过，使 stego 图像无任何修改地通过。
- **通信过程（Eq. 9–12）**：$I_s=\mathrm{Hide}(I_c,m)$；$S\leftarrow\mathrm{Upload}(\mathrm{Hook}(f_l,I_s))$；自适应策略 Eq. 11：$e_a>e_u$ 时走 Hook 通道，否则按常规流程上传；接收 $m'=\mathrm{Ext}(I'_s)$，并声明 $m'=m$ 仅当原算法在无攻击时本可完全提取。
- **定理 1（无损信道）**：把处理链建模为函数复合 $F=f_n\circ\dots\circ f_0$（Eq. 13），Hook 后 $F'=f_n\circ\dots\circ\mathrm{Hook}(f_l,\cdot)\circ\dots\circ f_0$（Eq. 14–15）；接收侧确定性编码 $D(\cdot)$ 不改内容（Eq. 16）；在提取算法满足 SSIM 鲁棒条件（Eq. 17：$\mathrm{SSIM}(I'_s,I_s)>\theta\Rightarrow\mathrm{Ext}(I'_s)=\mathrm{Ext}(I_s)$）下，$F'(I_s)=I_s$（Eq. 18）、$\mathrm{SSIM}(I_r,I_s)=1$（Eq. 19），故 $m'=m$（Eq. 20）。该定理强调 HookSteg 不改像素与元数据，只重定向控制流。
- **定理 2（时间常数）**：传统通道 $T_{conventional}=\sum T_{f_i}(I_s)=O(n)$（逐像素操作，Eq. 22）；HookSteg 通道 $T_{hook}=T_{overhead}+O(1)=O(1)$（Eq. 23–24），时间优势 $\eta=O(n)/O(1)=\Omega(n)$ 至少随图像尺寸线性增长（Eq. 25）。
- **定理 3（内存常数）**：Hook 开销来自三部分——Hook 框架本身、动态生成的 hook stub/trampoline（ARM/ARM64 上典型 5–14 字节跳转）、Hook 上下文结构，均为常数；预处理阶段调用栈只存函数地址，受最大栈深（常数）约束；故 $M_{hook}=O(1)$ vs $M_{conventional}=O(n)$，内存优势 $\mu=\Omega(n)$（Eq. 26–28）。
- **Algorithm 1（有损函数定位）**：反编译 → 高级语言 → 语义过滤 $S_v$ → 句法过滤 $S_c$ → 对每条可疑语句取函数与其调用栈 → 逐栈帧 Hook 并检验 $\mathrm{Hook}(f_l,I_s)==I_s$ → 命中即返回，否则继续；全部失败返回 None。

### 4.5 方法优势

- **算法无关**：对修改式、生成式（甚至映射式理论上）隐写算法都通用，不需要改动或重训任何隐写模型（§III、§V-D）。
- **真正无损**：Hook 通道下提取精度在所有场景与所有方法上与"无攻击"完全一致（Change 0.00%），这是"提升鲁棒性"路线无法达到的（Table VI–VIII）。
- **效率反超**：绕过处理反而省掉了编解码计算，处理时间恒为 1 ms（§V-E、Fig. 8）。
- **解耦三难**：作者声称该方法打破了容量、安全性、鲁棒性的相互制约，使隐写研究可以专注安全性与容量（§VI）。

### 4.6 方法不足

- **需要 root 权限**：发送端必须能执行进程 Hook，普通用户设备难以推广；未来考虑基于虚拟化/沙箱的轻量绕过（§VII）。
- **仅适用于客户端有损处理**：服务端也做处理的 App（如 Pinterest、Reddit）无法保证无损；未来需结合服务端处理的先验知识设计针对性鲁棒编码（§VII、Table III）。
- **依赖逐 App 的预处理**：每个目标 App 都要走节点识别 + 函数定位流程，规模化成本未评估；且 App 更新可能改变代码结构（隐含，解析稿未直接讨论）。
- **对"原算法本就不可完全提取"的情形无能为力**：HookSteg 只保证"无损"，不保证"可提取"（Eq. 12 后的说明）。
- **实验密度有限**：修改式方法只在 BossBase 1,000 张/方法上测；作者未给出统计显著性检验；传输效率实验只有 4 档分辨率与 3 档质量因子（§V-D/E）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

现有隐写研究都在**算法层**做文章（改嵌入域、改代价函数、加纠错码、用 GAN/扩散模型生成），本质上是在"被攻击后尽量还能提取"；HookSteg 换到**系统层**，把"攻击"本身从客户端处理链中摘除，因此它不改 stego 图像一个比特，也不受具体隐写算法限制——是"绕过"而非"抵抗"。这在评测上的直接体现是：其他方法的精度提升总有上限（受攻击强度影响），HookSteg 的 Change 在所有组合中都是 0.00%（Table VI–VIII）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 进程 Hook 绕过有损处理的范式 | 把"鲁棒隐写"问题转化为"客户端处理链绕过"问题 | 高 | 是（任何客户端处理导致的信号退化场景） |
| MitM + eBPF 双验证节点识别 | 用像素矩阵比对判定处理发生在客户端还是服务端 | 中 | 是（移动端数据处理链路审计） |
| 语法-语义联合特征 + 动态污点追踪的函数定位 | SHS/ESS 两级筛选 + 调用栈回溯，较人工逆向效率提升 94.34% | 高 | 是（App 逆向、隐私合规分析） |
| 自适应绕过策略 | 用 $e_a$ vs $e_u$ 处理"攻击反而提升精度"的反常情况 | 中 | 是（任何"扰动可能有益"的系统） |
| 三项复杂度定理 | 论证 Hook 通道在时间/内存上均为常数级、Π 优于传统通道 Ω(n) | 中 | 是（系统级优化的理论论证范式） |

### 5.3 适用场景

需要**零错误**传输的商业机密/敏感数据隐蔽通信，且目标社交 App 的图像有损处理仅发生在客户端：论文验证的 Youku（Q_f=80）、Kehua（60）、Hiferr（100）、Kutumb（80）属于此类；iQiyi、Toutiao、Baidu Map、QQ Reader、Hiferr、Kutumb、Youku 等可被 HookSteg 建立无损通道（§V-C）。服务端参与处理的 Pinterest、Reddit、Tumblr、Quora、Medium、Tencent Video、KuGou、微博、高德、QQ 音乐、58 同城、Dianping、Ctrip 等则不适用（Table III）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 修改式鲁棒隐写（DMAS、JCRISBE、SCRIPT、ROAST） | 已有一定抗压缩能力 | 改像素引入失真；真实平台攻击后精度 ≈50%；Q_f=100 时 SCRIPT 甚至无法生成 stego | Hook 通道下精度回到无攻击水平（+48.06% 平均） |
| 经典隐写（J-UNIWARD） | 隐写安全性研究基线 | 无鲁棒设计，被压缩直接摧毁 | 同一通道下 Change 0.00% |
| 映射式隐写（coverless） | 极强鲁棒（不修改图像） | 容量过低，不满足社交平台需求 | 论文明确不纳入对比，改为通用绕过 |
| 生成式非鲁棒（StegaDDPM、GSD） | 容量大、生成质量高 | 被攻击后 ≈50% | Hook 通道下恢复至 100%/99.99% |
| 生成式鲁棒（PARIS、ERGI、TransStego） | 攻击下仍有 80%+ | 仍随场景退化（Kutumb 下 ERGI −18.11%） | Hook 通道下皆为 0.00% 变化 |
| 传统函数定位（静态分析 + 动态调试） | 通用 | 人工分析全代码库，混淆下不可行 | 语法-语义 + 污点追踪，效率 +94.34% |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

真实设备 One Plus Ace2（Android 13），Python 3.8.0 + Frida 16.5.9（Hook）+ Objection 1.11.0（内存/实时监控）+ Reqable 2.30.3（网络分析）（Table IV）。四个真实传输场景：Youku、Kehua、Hiferr、Kutumb，其图像处理质量因子分别为 80、60、100、80。修改式方法用 BossBase v1.01 的 1,000 张图，统一调整到 5,000×5,000 像素并保存为 Q_f=75/85 的 JPEG；生成式方法各用 1,000 张图并沿用各自公开预训练模型与参数（§V-A、Table V）。对比分两类（修改式 / 生成式），映射式因容量过低被排除（§V-D）。

### 6.2 数据集

| 数据集/来源 | 规模 | 内容 | 说明 |
|---|---|---|---|
| BossBase v1.01 | 1,000 张/方法 | 修改式隐写的封面图像，统一 5,000×5,000，JPEG Q_f=75/85 | 公开数据集（ref [46]） |
| 生成式方法数据 | 1,000 张/方法 | 沿用各方法原始实验设置与公开预训练模型 | StegaDDPM/GSD/PARIS/ERGI/TransStego |
| 应用节点调研 | 50（应用宝 top）+ 7（Google Play 国际应用） | 筛出 21 个可图像交互 App + 7 个国际 App 的节点识别结果 | Table III，数据截至 2026-01-01 |

### 6.3 Baseline

修改式：J-UNIWARD [47]（经典）、DMAS [32]、JCRISBE [13]、SCRIPT [30]、ROAST [12]（鲁棒）。生成式：StegaDDPM [45]、GSD [28]（经典/非鲁棒）、PARIS [23]、ERGI [25]、TransStego [43]（鲁棒）。对比维度为"常规信道 vs HookSteg 信道"下的攻击后提取精度及其变化（§V-D、Table V–VIII）。

### 6.4 评价指标

提取精度（extraction accuracy，%），分别报告无攻击（stego）、常规信道攻击后、HookSteg 信道后及其变化（Change）；当 Change 非负（≥0）表示有效抵抗攻击（表中加粗）。另有定位效率提升（%）、检索/过滤/提取语句数量、处理时间（ms）（§V-C/D/E）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| 修改式 × 4 场景（Q_f 匹配真实平台） | 攻击后提取精度（均值） | HookSteg 94.64%（Change 0.00%） | 常规信道 50.03%（Change −44.61%） | +44.61%（论文口径） | Table VI；20 个方法-场景组合 Change 全为 0.00% |
| 修改式 × Q_f=75/85（不匹配场景） | 攻击后提取精度（均值） | 99.97% / 99.69%（Change 0.00%） | 常规信道 50.13% / 49.97% | 平均 +49.72% | Table VII；两档 Q_f 各 20 组合 |
| 生成式 × 4 场景 | 攻击后提取精度（均值） | 99.27%（Change +0.02%） | 常规信道 74.08%（Change −25.17%） | +25.19% | Table VIII；TransStego 在 Hiferr 下 +0.40%（JPEG Q=100 的轻微扰动反而有利） |
| 修改式 + 生成式综合 | 平均提升 | — | — | **36.63%**（48.06% 与 25.19% 的综合） | §V-D、摘要 |
| Hiferr 场景（Q_f=100） | SCRIPT 可生成性 | HookSteg 通道可用 | SCRIPT 无法生成 stego（记为 "-"） | — | Table VI 脚注；反向说明真实平台上部分方法直接失效 |
| 有损函数定位（7 个 App：iQiyi/Toutiao/Youku/Baidu Map/QQ Reader/Kutumb/Hiferr） | 效率提升 | 平均 +94.34% | 人工逆向为基线 | +94.34% | §V-C、Fig. 6；所有有损函数均落在可疑语句集合内 |
| 节点识别（50 应用宝 + 7 国际 App） | 覆盖比例 | MitM+eBPF 联合验证 76.66% | MitM 单独 70.00%（社交类） | — | §V-B、Table III |
| 传输效率（4 分辨率 × 3 质量因子） | 处理时间 | HookSteg 恒为 1 ms | 常规信道随时间/尺寸上升 | — | §V-E、Fig. 8；与图像尺寸、质量因子无关 |

### 6.6 优势最明显的场景

- **修改式鲁棒隐写 + 客户端处理平台**：所有方法在 HookSteg 通道下恢复到"无攻击"精度，且原本在真实平台上只有 ~50%（随机猜测）的提取率被完全修复（Table VI/VII）。
- **原本会被彻底摧毁的方法**：J-UNIWARD 这类无鲁棒设计方法在常规信道下几乎不可用，走 HookSteg 通道后 Change 为 0.00%。
- **大图/高容量场景**：HookSteg 处理时间恒为 1 ms（Fig. 8），随 512² → 4096² 尺寸增长常规通道耗时显著上升，而 HookSteg 不变。

### 6.7 局限性

- 发送端需 root 权限；普通用户设备难以部署（§VII）。
- 服务端参与处理的 App 无法建立无损通道（§VII、Table III 中 Pinterest/Reddit/Tumblr/Quora/Medium 等）。
- 论文未评估 App 版本更新导致代码变化后需重新定位有损函数的成本；Table III 标注数据截至 2026-01-01，版本号明列（如 Facebook 501.0.0.61.70），时效性强。
- 传输效率实验只报告了处理时间，端到端上传/下载时延与并发场景未涉及。
- 论文声称"首次在真实场景实现无损传输"，但实验全部在单一机型（One Plus Ace2 / Android 13）上完成，跨机型与跨 OS 版本的可迁移性未验证。

---

## 7. 学习与应用

### 7.1 是否开源？

解析稿未提及代码仓库或 artifact（`code` 记 unknown）。工具链均为公开工具：Frida 16.5.9、Objection 1.11.0、Reqable 2.30.3、Python 3.8.0（Table IV）。

### 7.2 复现关键步骤

1. 用 MitM（或 eBPF）确认目标 App 的图像处理仅在客户端发生：比对客户端上传的图像 $I'_s$ 与平台下载的 $I''_s$ 像素矩阵。
2. 反编译目标 App，将低级语言转换为高级语句集合，按语义特征码（compress/rotate/resize/upload）与句法特征两级筛选得到可疑语句/函数。
3. 在真机（root）上用 Frida Hook 可疑函数，触发图像上传流程，记录入参、返回值与调用栈；从栈顶按 Table II 的四种策略（替换方法参数、拦截方法执行、构造返回对象、替换上传路径）逐帧尝试。
4. 找到满足 $\mathrm{Hook}(f_l,I_s)=I_s$ 的函数即完成定位；通信时 Hook 该函数并零拷贝上传 stego 图像。
5. 按自适应策略（$e_a$ vs $e_u$）决定是否绕过；接收方按原隐写算法的提取函数恢复信息。

### 7.3 关键超参数、预处理和训练细节

无模型训练。关键工程参数：图像统一 5,000×5,000（修改式）、JPEG Q_f=75/85；平台质量因子 Youku 80 / Kehua 60 / Hiferr 100 / Kutumb 80；传输效率实验缩放因子固定 0.8、质量因子取 100/80/60、分辨率 512²/1024²/2048²/4096²；Hook 框架 Frida 16.5.9；语义特征码 4 个（compress/rotate/resize/upload）（§V-A、Table I、Table IV）。

### 7.4 能否迁移到其他任务？

- **隐私/合规审计视角**：MitM + eBPF 双验证节点识别可复用于"App 是否在客户端/服务端处理用户图片、是否加水印"这类数据处理行为审计，属于流量分析之外的端侧测量方法。
- **函数定位方法论**：语法-语义联合特征 + 污点追踪 + 调用栈回溯的定位流程（Algorithm 1）可迁移到恶意行为定位、广告 SDK 追踪等逆向任务。
- **"绕过而非抵抗"的设计哲学**：在防御/隐私研究中，与其提升算法以抵抗退化，不如削弱退化本身（如内容分发链路改造）；对流量分析中的"隐写/隐蔽信道"研究是一个反向参照——检测方需要意识到客户端 Hook 可完全消除信道退化特征。
- **系统级优化的论证范式**：用函数复合 + 复杂度定理证明"改进不改变目标语义"，是可迁移的论文论证模板。

### 7.5 对我的研究有什么启发？

- **问题重构大于算法改进**：把"如何更鲁棒"换成"如何让攻击不发生"，直接绕过了整个鲁棒隐写研究的技术路线；这种"换层思考"对流量分析选题很有借鉴意义。
- **极端场景的指标设计**：在要求零错误的场景中，应直接以"Change 是否为 0"和"与无攻击精度是否一致"为指标，而非平均精度；论文用 Change 列 + 加粗标注把这一逻辑可视化。
- **诚实的反例处理**：TransStego 在 Hiferr 下攻击后精度反而升高（+0.40%），作者用它解释自适应策略的必要性，把"反常现象"转化为方法设计的证据——这是很好的负面结果用法。
- **适用边界前置**：论文在 §VII 明确列出 root 权限与服务端处理两条硬限制，而不是等审稿人指出——值得在写作中效仿。
- **与流量分析的关联点**：该工作本身不涉及网络流量特征分析（stego 图像走加密 HTTPS 上传，信道退化发生在应用层处理而非网络层），因此与知识库中加密流量分类/WF 主题关联度低，但其"端侧 Hook 改变应用行为"的手法提示：客户端侧信道与流量侧信道的边界正在模糊。

---

## 8. 总结

### 8.1 核心思想

> 用进程 Hook 绕过客户端的图像有损处理，实现真无损隐写。

### 8.2 速记版 Pipeline

1. 预处理第一步：MitM（eBPF 兜底）比对上传图与平台下载图，确认处理仅发生在客户端。
2. 预处理第二步：反编译后按语义特征码与句法特征两级筛选出可疑语句与可疑函数。
3. 预处理第三步：Hook 触发 + 记录调用栈，从栈顶逐帧尝试四种绕过策略，直到找到满足 $\mathrm{Hook}(f_l,I_s)=I_s$ 的有损函数。
4. 通信：发送方以零拷贝方式 Hook 有损函数（自适应策略：仅在绕过能提升提取精度时使用），stego 图像原样上传。
5. 接收方按原算法提取；四个真实平台 × 10 种隐写方法下提取精度提升 36.63%，定位效率提升 94.34%，处理时间恒为 1 ms。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- 无。本论文属于图像隐写 / 隐蔽通信领域，知识库现有概念页（WF、加密流量分析、恶意流量检测等）均无对应主题；论文本身也未引用任何加密流量分析文献。

### 9.2 相关方法

- 无。论文方法为进程 Hook、动态污点追踪与代码逆向定位，不在知识库方法白名单（8 个深度学习方法页）内。

### 9.3 相关任务

- 无（现有任务白名单中不存在隐写/隐蔽信道任务页）。

### 9.4 可更新的综述页面

- 无直接对应综述页。

### 9.5 可加入的对比表

- 无（论文未开源，未引入可比较的流量数据集，也不适合并入现有对比表）。

主题相近的现有论文笔记（**未被本文引用**，仅作知识库内横向关联）：

- [[2026-CS-Hiding_the_Trees_in_the_Forest__Building_Network_Covert_Channels_with_Hash-Based_Covert_Carrier_Filtering]]（同属隐蔽通信，但该工作在网络层构造隐蔽信道）
- [[2025-TDSC-QuicCourier__Leveraging_the_Dynamics_of_QUIC-_Based_Website_Browsing_Behaviors_Through_Proxy_for_Covert_Communication]]（同属隐蔽通信，利用 QUIC 浏览行为动态）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 现有鲁棒隐写在真实平台混合攻击下提取精度跌至 ~50%（随机猜测） | 修改式 5 方法 × 4 场景（Q_f 匹配）常规信道均值 50.03% | Table VI |
| Hook 通道下修改式方法提取精度与"无攻击"完全一致 | 20 个组合 Change 全为 0.00%，均值 94.64%→94.64% | Table VI/VII |
| 生成式方法同样受益，均值 74.08%→99.27% | Change 由 −25.17% 变为 +0.02%（+0.02% 来自 TransStego 在 Hiferr 下 +0.40%） | Table VIII |
| 综合平均提升 36.63% | 修改式 +48.06%、生成式 +25.19% 的综合口径 | §V-D |
| 定位效率较人工逆向提升 94.34%，且召回完整 | 7 个 App 的检索/过滤/提取量统计，所有有损函数都在可疑语句集合内 | §V-C, Fig. 6 |
| 节点识别覆盖率 | MitM 在 70.00% 社交类 App 可用；MitM+eBPF 联合验证 76.66% | §V-B, Table III |
| Hook 通道处理时间与图像尺寸/质量无关（恒 1 ms） | 4 分辨率 × 3 质量因子下常规信道耗时上升而 HookSteg 不变 | §V-E, Fig. 8 |
| 理论保证：无损（定理 1）、时间 O(1)（定理 2）、内存 O(1)（定理 3） | SSIM 鲁棒条件下 $F'(I_s)=I_s\Rightarrow m'=m$；$\eta=\Omega(n)$、$\mu=\Omega(n)$ | §IV-A/B/C, Eq. 13–28 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-TIFS-HookSteg__A_Truly_Lossless_Steganography_Based_on_Process_Hooking_for_Lossy_Network_Channels.pdf
- MinerU Markdown：02-parsed-markdown/2026-TIFS-HookSteg__A_Truly_Lossless_Steganography_Based_on_Process_Hooking_for_Lossy_Network_Channels.md

---

## 12. 后续问题

- Table III 的符号列（"○/●/➊/×/√/-"）在解析稿中大量丢失（如 Facebook/X/QQ/WeChat/Taobao/Meituan 的"客户端独占/服务端参与/无处理"三列均为 "-"），节点分类的完整统计需回查 PDF。
- 论文未给出"可疑函数提取"的误报率/漏报率量化（只说"所有有损函数都在提取集合内"），定位方法的精确率无法从解析稿评估。
- 未讨论 App 版本更新后 $f_l$ 的漂移与重新定位成本；Table III 明列各 App 版本号，说明结论有时效性。
- 仅单机型（One Plus Ace2 / Android 13）验证，iOS、HarmonyOS 与不同 Android 版本上的 Hook 可行性未知（威胁模型仅称聚焦 Android，因市场占有率 70.48%）。
- 自适应策略中的 $e_a$ 需先"预攻击"一次图像来测量提取精度，这在真实通信中是否引入额外开销与暴露风险，论文未讨论。
- 解析稿存在系统性连字丢失（affect→afect、efficiency→eficiency、tradeoff→tradeof、different→diferent 等），引用原文时需还原。

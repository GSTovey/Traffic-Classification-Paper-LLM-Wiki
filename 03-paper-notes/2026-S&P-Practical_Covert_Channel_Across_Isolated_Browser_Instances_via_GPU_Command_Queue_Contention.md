---
type: paper
title_original: "Practical Covert Channel across Isolated Browser Instances via GPU Command Queue Contention"
title_cn: "基于 GPU 命令队列竞争的浏览器隔离实例间实用隐蔽信道"
authors: ["Jinhong Liu", "Zifeng Kang", "Song Li", "Yinzhi Cao"]
year: 2026
venue: "IEEE S&P 2026"
doi: "10.1109/sp63933.2026.00254"
url: "https://doi.org/10.1109/sp63933.2026.00254"
pdf: "00-inbox/PDFs/2026-S&P-Practical_Covert_Channel_Across_Isolated_Browser_Instances_via_GPU_Command_Queue_Contention.pdf"
mineru_md: "02-parsed-markdown/2026-S&P-Practical_Covert_Channel_Across_Isolated_Browser_Instances_via_GPU_Command_Queue_Contention.md"
status: processed
reading_level: L2
research_area: []
task: []
method: []
dataset: []
code: "https://github.com/HugoLeoLJH/C3F"
relevance: medium
created: "2026-09-19"
updated: "2026-09-19"
---

# Practical Covert Channel across Isolated Browser Instances via GPU Command Queue Contention

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Practical Covert Channel across Isolated Browser Instances via GPU Command Queue Contention |
| 中文标题 | 基于 GPU 命令队列竞争的浏览器隔离实例间实用隐蔽信道 |
| 作者 | Jinhong Liu, Zifeng Kang, Song Li, Yinzhi Cao（浙江大学区块链与数据安全全国重点实验室 / 杭州高新区（滨江）区块链与数据安全研究院 / 北京邮电大学 / Johns Hopkins University） |
| 年份 | 2026 |
| 会议/期刊 | IEEE Symposium on Security and Privacy (S&P) 2026；DOI 10.1109/sp63933.2026.00254（由主代理分配给出） |
| 研究方向 | 浏览器侧信道 / 隐蔽信道（cross-site、cross-mode、cross-browser 隐蔽通信）；Web 隐私隔离机制（cookies、incognito、多浏览器并存）的绕过 |
| 任务类型 | 隐蔽信道构建与实用化：跨隔离 Web 实例（不同浏览器模式 / 不同浏览器）的秘密信息传输，含握手、纠错、重传协议 |
| 方法关键词 | GPU command queue contention、OpenGL synchronization（finish / readPixels）、WebGL vertex shader 负载、四层框架（Session / Transmission / Encoding / Raw Channel）、自适应阈值握手、CRC-32 校验与重传、Shannon 容量对比 |
| 数据集 | 无公开数据集（Amazon Mechanical Turk 众包 1,524 次实验、232 名工人；本地 380 次实验；40 次 Shannon 容量实验） |
| 是否开源 | 开源：https://github.com/HugoLeoLJH/C3F ；在线 demo：https://hugoleoljh.github.io/c3f-demo/c3f/receiver.html |
| PDF | 00-inbox/PDFs/2026-S&P-Practical_Covert_Channel_Across_Isolated_Browser_Instances_via_GPU_Command_Queue_Contention.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-S&P-Practical_Covert_Channel_Across_Isolated_Browser_Instances_via_GPU_Command_Queue_Contention.md |

---

## 1. 一句话总结

> 利用 WebGL/OpenGL 同步语义制造的 GPU 命令队列竞争（发送方渲染重负载命令、接收方发送大量轻量 probe），首次在**真实噪声环境**下实现跨浏览器模式与跨浏览器实例的隐蔽通信，AMT 众包 1,434 次有效实验中成功率 92.81%、完成后准确率 100%、平均带宽 6.82 bps。

---

## 2. 摘要翻译

### 2.1 摘要原文

Web storages, e.g., cookies, are isolated across different browser modes (e.g., normal vs. incognito) and browsers (e.g., Chrome vs. Safari) to ensure user privacy. Despite such browser-level isolation, researchers have found covert communication channels between different modes and browsers, which can break such a security mechanism. However, existing covert communications are impractical and unreliable in the real world scenarios, where noise is prevalent. Furthermore, multiple prior covert channels only support cross-mode—not cross-browser—communications, because the relevant resources are shared within a single browser. In this paper, we discover a novel covert channel due to GPU command queue contention and then design a framework, called C3F, for both cross-mode and cross-browser covert communication. C3F negotiates an adaptive communication speed between the sender and the receiver and then facilitates the covert communication. We evaluated C3F in real-world settings by deploying it to crowd-sourced workers on Amazon Mechanical Turk, simply asking them to visit two websites without imposing additional constraints. Our evaluation shows that covert communication achieves a 100% accuracy once the data transmission is completed, with an overall completion rate of 92.81% across 1,434 AMT experiments. So far, Firefox, Safari and Tor developers have confirmed our attack and are working with us on practical defenses.（节选）

### 2.2 摘要中文翻译

Web 存储（如 cookies）在不同浏览器模式（普通 vs. 无痕）与不同浏览器（Chrome vs. Safari）之间是相互隔离的，以保护用户隐私。尽管存在这种浏览器级隔离，研究者仍发现了模式间与浏览器间的隐蔽通信信道，从而绕过这一安全机制。然而，现有隐蔽通信在噪声普遍存在的真实场景中既不可靠也不实用；此外，多种已有隐蔽信道只支持跨模式（cross-mode）而不支持跨浏览器（cross-browser）通信，因为所依赖的资源只在单个浏览器内共享。本文发现了一个由 GPU 命令队列竞争（GPU command queue contention）产生的新隐蔽信道，并据此设计了 C3F 框架，同时支持跨模式与跨浏览器隐蔽通信。C3F 在发送方与接收方之间协商自适应的通信速率，进而完成隐蔽通信。我们在真实环境中评估 C3F：将其部署为网页并招募 Amazon Mechanical Turk 众包工人，仅要求他们访问两个网站、不附加任何额外约束。评估表明，一旦数据传输完成，隐蔽通信可达到 100% 准确率；在 1,434 次 AMT 有效实验中的整体完成率为 92.81%。目前 Firefox、Safari 与 Tor 的开发者已确认该攻击，并正在与我们合作推进实用防御。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 浏览器通过"模式隔离"（普通 / 无痕）与"浏览器隔离"（Chrome / Safari / Firefox 各自独立存储 cookie 与历史）保护用户隐私，但已有工作（Pool-Party、Loophole、SideR）证明隔离可被隐蔽信道绕过（§1、§2.1）。
- 已有信道在**真实噪声环境**下不可用：SideR 依赖 100% GPU/CPU 占用，传输 512 bit 约需 30 分钟；Loophole 只存在于 Chrome 内部（事件循环不跨浏览器共享）；Pool-Party 的资源池同样不跨模式/浏览器共享（§1、§2.1）。
- 关键的可用性缺口：**没有一种信道同时满足跨模式 + 跨浏览器 + 真实噪声环境下可靠**，而"跨浏览器"恰是隐私敏感用户（工作用 Safari、个人用 Chrome）的真实使用形态（§3.1 威胁模型）。

### 3.2 现有方法的痛点和不足

| 现有方法/路线 | 痛点 |
|---|---|
| SideR（渲染竞争） | 需 100% GPU 或 CPU 占用才能让双方互相影响；带宽极低（512 bit 约 30 分钟，≈0.3 bps），真实环境不可靠（Table 1、§2.1） |
| Loophole（共享事件循环） | 事件循环不跨浏览器共享，本质上无法做跨浏览器通信；性能严重依赖超参数，噪声下不可靠（§2.1） |
| Pool-Party（浏览器资源池） | 资源池不跨浏览器实例共享，不支持跨模式/跨浏览器（§2.1） |
| 微架构信道（CPU cache / GPGPU） | 带宽虽高（45 KBps / 4 Mbps）但绑定特定硬件设计（Intel cache、Nvidia GPGPU），迁移需逆向未公开调度算法，未在 Apple/AMD 等平台验证（§2.1） |
| 通用侧信道（Rokicki 端口竞争等） | 威胁模型强（要求攻击者-受害者同核共置）或仅演示 CPU 指纹，未用于跨浏览器通信（§2.1） |

### 3.3 论文的研究假设或核心直觉

核心直觉：**GPU 命令队列是跨浏览器实例共享的硬件资源，且 OpenGL 提供了同步原语（finish、readPixels）把"异步渲染延迟"变成可观测的时间量**。发送方发一条重负载绘制命令（渲染时间编码 bit 值）并等待其完成；接收方持续发送大量轻量"probe"（drawArrays + readPixels），其中恰好排在发送方命令之后的 probe 会被延迟，其余 probe 感知不到延迟——因此接收方可以通过 probe 时延分布"读到"发送方命令的渲染时长（§3.1）。由于竞争只依赖命令队列顺序而非占满 GPU 资源，信道的资源开销可控（带宽 6 bps 时 GPU 利用率约 60%）（§6.4 RQ3.3）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | WebGL 绘制命令异步下发，但 OpenGL 同步命令（finish、readPixels）会阻塞直到前序命令完成；两个隔离 frame 的命令在同一 GPU 命令队列中排队 | §3.1、Table 2 |
| 痛点提炼 | 两个隔离浏览器实例（不同模式/不同浏览器）无法通过存储、事件循环或资源池通信；渲染竞争类信道又需要占满 GPU，现实中不存在"资源被占满"的条件 | §1、§2.1 |
| 问题转化 | 把"能否在隔离实例间可靠传数据"转化为"如何用命令队列竞争构造低开销、可自适应阈值的可观测时序信号，并用协议层解决噪声与失序" | §3.1、§4 |
| 文献定位 | 现有三条最接近的信道（SideR / Loophole / Pool-Party）在通信类型与实用性上各有硬缺口；GPU 命令队列竞争此前**未被发现** | §2.1、Table 1 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | GPU 命令队列竞争可在跨模式与跨浏览器实例间形成可观测时延信号，且该信号在真实噪声环境下仍可解码 | §3.1（队列竞争机制）、§3.2（不同 GPU/浏览器实测延迟） | AMT 众包实验（1,524 次）+ 本地理想实验（380 次） |
| 辅助假设 1 | 双方各自的"bit-0 阈值"与"offset 阈值"可通过握手阶段自适应协商，从而在不同 GPU / 浏览器 / 机器上稳定区分 bit 0 与 bit 1 | §4.2.1（线性回归拟合负载-时间关系后逐点试探） | 阈值协商在 92.81% 实验中成功；跨 GPU（Apple/NVIDIA/Intel/AMD）成功率均高（Fig. 8a） |
| 辅助假设 2 | 真实环境噪声可通过帧结构（定界符 + CRC-32）+ 重传协议吸收，从而在"完成传输"的前提下达到零错误 | §4.2.2（Transmission-OK / Frame-Error / ACK-Error 三协议） | 1,331 次成功传输准确率全部 100%（§6.2 RQ1.2） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | AMT 成功率 92.81%（1,331/1,434）；跨浏览器组合成功率 83.83%–98.70% | §6.2 RQ1.1, Table 3, Fig. 8 |
| 辅助假设 1（自适应阈值） | 支撑 | NVIDIA 成功率 99.59%、AMD 83.70%，均无需人工调参；Tor 与 fuzzy-time 防御下成功率仍 100% | Fig. 8(a)、Table 8、Table 9 |
| 辅助假设 2（纠错与重传） | 支撑 | 645 次重传（平均 0.49 次/实验）；89.63%（1,193/1,331）实验重传数与带宽负相关；正确解码的 1,331 次准确率 100% | §6.4 RQ3.2, Fig. 11 |

---

## 4. 方法设计

### 4.1 方法整体流程

C3F 是一个四层框架（Fig. 5）：**Raw Channel Layer** 直接与 GPU 命令队列竞争信道交互（生成负载与 probe、测量渲染时延）；**Encoding Layer** 在比特序列与时延序列之间转换（含聚类解码算法）；**Transmission Layer** 负责数据帧/ACK 帧的生成与 CRC-32 校验；**Session Layer** 编排整个会话的三个阶段——Setup（握手与阈值协商）、Transmission（数据帧 + 校验 + 重传）、Finishing（FIN 收尾）。发送方与接收方各自运行一个隔离的网页实例（不同模式或不同浏览器），通过队列竞争互相"看见"对方的渲染时长（§4.2–§4.5）。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 Setup 握手 | 双方网页实例 | 测量若干预设负载的实际渲染时间 → 线性回归拟合"负载–渲染时间"直线 → 沿直线试探：bit-0 负载需使渲染时间超过 bit-zero threshold；bit-1 负载需再超过 offset threshold；各自确定自己的最小负载 | 双方各自的 bit-0 / bit-1 负载与区分阈值 | 把阈值适配到具体 GPU/浏览器/机器，保证 bit 可区分 |
| Step 2 数据帧生成 | 512 bit 随机比特串 | 组装数据域（Start 8 bit + Data 512 bit + End 8 bit）与校验域（CRC-32，32 bit） | 数据帧 | 定界 + 完整性校验 |
| Step 3 编码与渲染 | 数据帧 / ACK 帧 | Encoding Layer 把帧映射为比特序列 → 映射为一系列渲染时长 → Raw Channel Layer 在 vertex shader 中执行固定时长的数学运算（重复次数由负载决定） | GPU 命令队列中的重负载命令 | 把"信息"放入物理信道 |
| Step 4 探测与解码 | 接收方 probe 时延序列 | 接收方以较小时间间隔持续下发轻量 probe（渲染时间 < 2 ms）并测量实际时延；Encoding Layer 用聚类算法（相邻时延间隔 > 3 ms 则切分新簇）对齐比特边界，并以每簇最小值作为 bit 0/1 判别阈值 | 比特序列数组 | 在噪声与失序中恢复比特序列 |
| Step 5 校验与重传 | 接收到的比特序列 | Transmission Layer 按帧结构切分、校验定界符、重算 CRC-32；**仅当恰好有一条正确序列时**判定成功，否则回 Not-OK 触发重传（Transmission-OK / Frame-Error / ACK-Error 三协议） | 正确数据帧或重传请求 | 保证零错误交付 |
| Step 6 Finishing | 会话结束信号 | 发送方发 FIN，接收方回 FIN，会话终止 | 会话结束 | 显式收尾，避免悬挂 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Session Layer | 编排 Setup / Transmission / Finishing 三阶段，保存会话状态与阈值信息 | 上层指令 | 阶段切换指令、渲染时长定义 | 向其余三层下发会话信息 |
| Transmission Layer | 生成数据帧与 ACK 帧、执行 CRC-32 校验、触发重传 | 比特序列 | 数据包 / 校验结论 | 上接 Session，下接 Encoding |
| Encoding Layer | 比特序列 ↔ 渲染时长序列的双向转换；聚类算法切分比特 | 数据包 / 时延序列 | 时延序列 / 比特序列 | 连接 Transmission 与 Raw Channel |
| Raw Channel Layer | 在 vertex shader 中生成负载与 probe，测量渲染时延 | 渲染时长序列 | 实测时延数组 | 直接操作 GPU 命令队列信道 |

### 4.4 公式、算法和机制解释

- **信道机制**：发送方发 heavweight 绘制命令 $d_1^1$ 后接同步命令；接收方持续发 probe $d_3^2 r_4^2$。命令队列中 $r_4^2$ 需等待 $d_1^1$ 完成才能真正取回缓冲数据，因此它恰好被延迟约等于 $d_1^1$ 的渲染时间，其余 probe 感知不到延迟（§3.1，Fig. 1）。
- **同步原语**：显式同步（`finish`）与隐式同步（`readPixels`、`convertToBlob`，必须等前序绘制结果可用）——Table 2 把 GLSL 命令分为 Drawing 与 Syncing 两类。
- **阈值协商**：线性回归拟合负载与渲染时间后，沿拟合线试探负载，满足 bit-zero threshold 的负载表示 0，再叠加 offset threshold 的负载表示 1（实现中取 bit-zero threshold = 70 ms、offset threshold = 40 ms，§5）。
- **帧结构**：Data Field = Start(8) + Data(512) + End(8)；Checksum Field = CRC-32(32 bit)（Fig. 7）。ACK 帧为 8 bit 定长序列，分别表示 SYN / OK / Not-OK / FIN（§4.3）。
- **聚类算法**（Algorithm 1）：对时延数组排序后，以 3 ms 为间隔阈值切分成簇，取每簇最小值作为 bit 判别阈值，输出比特序列（§4.4）。
- **Shannon 容量**：以 Shannon-Hartley 公式 $C = B \cdot \log_2(1 + S/N)$ 度量原始信道容量，刻意剥离编码方案，以便与 Pool-Party / Loophole / SideR 的原始信道公平对比（§6.3 RQ2.3, Eq. 1）。

### 4.5 方法优势

- **硬件无关**：仅依赖 OpenGL 标准命令队列与同步语义，在 Apple / NVIDIA / Intel / AMD 与部分虚拟 GPU 上均可用（§6.2 RQ1.1）。
- **资源开销可控**：信道只依赖命令排队顺序而非占满 GPU；6 bps 带宽对应约 60% GPU 利用率（§6.4 RQ3.3, Fig. 12）——这是相对 SideR 的关键区别。
- **真实环境可部署**：AMT 工人只需"打开两个网页"，无需配置，即达 92.81% 完成率与 100% 完成后准确率（§6.2）。

### 4.6 方法不足

- 高噪声下（如接收方设备同时运行视频等 GPU 重负载）传输可能根本无法建立会话：52 次实验建立了会话但收不到数据；51 次在握手阶段失败（§6.2）。
- 性能对 GPU 架构敏感：AMD 成功率 83.70%，明显低于 NVIDIA 的 99.59%（§6.2 RQ1.1）。
- 框架迁移性有限：作者明确说明把 C3F 的分层框架套用到 Loophole / SideR 这类高噪声信道会导致频繁比特错误与重传，泛化留作未来工作（§7）。
- 攻击前提是向两个隔离实例注入脚本（如第三方广告/分析脚本），跨模式/跨浏览器通信本身也要求用户同时打开两个浏览器（§3.1 威胁模型）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

现有浏览器隐蔽信道依赖**单一浏览器内部的共享资源**（事件循环、资源池）或**需要占满硬件资源**（渲染竞争）；C3F 依赖的是**操作系统/浏览器都不隔离的 GPU 命令队列**这一跨实例共享硬件资源，并用协议层（握手阈值协商 + CRC 校验 + 重传）把"时序竞争"提升为"可靠通信"。因此 C3F 在支持的通信类型（跨站点/跨模式/跨浏览器）与真实环境可靠性两个维度上同时领先（Table 1）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 发现 GPU 命令队列竞争隐蔽信道 | 利用 OpenGL 同步命令使接收方的 probe 排队在发送方负载之后，从而观测其渲染时长 | 高 | 是（同类 WebGPU/图形 API 时序信道） |
| 自适应阈值握手 | 用线性回归 + 双阈值（bit-zero / offset）为不同 GPU、浏览器、机器自动确定 bit 可判别负载 | 高 | 是（任何时序型隐蔽信道的自适应调制） |
| 四层可复用框架 | Session / Transmission / Encoding / Raw Channel 分层，理论上可替换 Raw Channel 以适配其他信道 | 中 | 是（但作者指出高噪声信道下框架失效） |
| 真实环境大规模验证 | 232 名 AMT 工人、1,524 次实验覆盖多厂商 GPU 与主流浏览器 | 中 | 是（隐蔽信道类工作的评估范式） |

### 5.3 适用场景

跨模式（普通→无痕）与跨浏览器（Chrome/Edge/Opera/Firefox/Safari 两两）的秘密数据传输，典型用途是跨隔离实例的 cookie / 标识符同步，从而恢复被隔离机制切断的跨会话追踪能力（§1、§3.1）。论文实测中 36 字节的 cookie（网站 cookie 中位数）在平均带宽下约需 40 秒，短于用户单页停留时间（52 秒），因此具备现实可行性（§1）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| SideR（渲染竞争，USENIX Sec 2022） | 支持跨站点/跨模式/跨浏览器 | 需 100% GPU 或 CPU 占用；≈0.3 bps；真实环境不可靠 | 仅依赖命令排队，GPU 利用率可控；带宽 ≈8 bps；AMT 环境可完成传输 |
| Loophole（共享事件循环，USENIX Sec 2017） | 跨模式带宽约 5 bps | 事件循环不跨浏览器共享，无跨浏览器能力；依赖超参调优 | 增加跨浏览器能力；握手自动定参 |
| Pool-Party（资源池，USENIX Sec 2023） | 跨站点追踪实用 | 不支持跨模式/跨浏览器 | 支持三种通信类型；原始信道 Shannon 容量 53.66 bps 约为 Pool-Party（18.07 bps）的 3 倍 |
| 微架构隐蔽信道（cache/GPGPU） | 带宽极高（KBps–Mbps 级） | 绑定特定硬件，迁移需逆向未公开机制 | 硬件无关（OpenGL 标准接口），在四家 GPU 上验证 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

三类环境（§6.1）：(i) **真实环境**——AMT 众包，232 名工人、两周内 1,524 次实验，工人仅被要求打开实验网页，传输序列为 512 bit 随机比特串；(ii) **理想环境**——本地 Windows（Intel i9 + NVIDIA RTX）与 MacBook Pro（Apple M1）两台设备，共 380 次实验，含 Safari 场景（因 SideR 无法在 Safari 传 512 bit，Safari 场景序列缩短为 256 bit）；(iii) **防御环境**——Tor 浏览器（利用其 timing jitter）与自行在 Chrome 上部署的 fuzzy-time 随机延迟防御。服务端为 CentOS 7.9、5 Mbps 带宽、2 vCPU、4 GiB RAM（§5）。

### 6.2 数据集

无公开数据集；数据来自 AMT 众包实验（1,524 次）、本地实验（380 次）与 Shannon 容量实验（40 次）。共 90 次 AMT 实验因工人未按要求操作被判定无效（33 次未打开发送页、29 次无接收方、28 次提前终止），有效实验 1,434 次（Table 3）。

### 6.3 Baseline

- **SideR**（§6.1）：采用原始源码并修复了一个 ASCII 计算的小 bug，用于跨浏览器与跨模式对比。
- **Loophole**（§6.1）：采用原始源码，参数取作者给定最优值（$t_b$=200 ms、N=350）与启发式阈值 15；因其不支持跨浏览器，仅参与跨模式对比。
- **Pool-Party**（§6.1）：因不支持跨模式/跨浏览器，仅参与原始信道 Shannon 容量对比。

### 6.4 评价指标

成功率（成功完成实验比例）、传输准确率（正确比特比例，超长截断、缺失全部计错）、带宽（bps）、Shannon 容量（Shannon-Hartley 公式，bits/s）（§6.1 Metrics）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| AMT 真实环境（1,434 有效实验） | 成功率 | 92.81% | 基线在 AMT 上无法成功传输任何数据 | — | Table 3；90 次无效实验被排除 |
| AMT 真实环境（1,331 次成功接收） | 传输准确率 | 100% | — | — | §6.2 RQ1.2；归因于握手阈值协商 + CRC 校验 |
| AMT 真实环境 | 平均带宽 | 6.82 bps | — | — | §1；GPU 厂商间有差异（Fig. 9a） |
| 本地跨浏览器（不含 Safari） | 准确率 | 100 ± 0.00% | SideR 50.01 ± 13.42% | +99.96%（论文口径） | Table 5 |
| 本地跨模式（不含 Safari） | 带宽 | 8.76 ± 0.17 bps | Loophole 5.00 / SideR 0.25 | +75.20% / +3,404.00% | Table 4 |
| Safari 场景（跨浏览器 + 跨模式） | 准确率 / 带宽 | 100% / 5.90 ± 0.13 bps | SideR 63.92 ± 9.07% / 0.48 ± 0.53 bps | 准确率 +79.86%（跨模式口径）；带宽 +2,456.52% | Table 6 |
| 原始信道容量 | Shannon 容量 | 53.66 ± 0.52 bps | Pool-Party 18.07 / Loophole 1.69 / SideR 0.01 | 约为 Pool-Party 的 2.97 倍 | Table 7 |
| Tor 浏览器防御 | 成功率 / 带宽 | 100% / 5.30 ± 0.14 bps | 无防御 8.60 bps | 带宽下降，准确率不降 | Table 8；重传率 4.42 ± 14.20% |
| fuzzy-time 防御（Chrome） | 带宽 | 6.45 ± 2.22 bps（15 ms 延迟） | 0 ms 无防御 8.60 ± 0.07 bps | −25.0% | Table 9；各延迟档成功率与准确率均 100% |

### 6.6 优势最明显的场景

跨浏览器组合（Firefox↔Chrome、Chrome↔Edge 等）表现最好：成功率区间 83.83%–98.70%，带宽高于跨模式（Fig. 8b、Fig. 9b）。跨模式普遍低于跨浏览器，Firefox 跨模式成功率仅 81.63%（§6.2 RQ1.1）。硬件层面 NVIDIA 最优（成功率 99.59%），AMD 最弱（83.70%）（Fig. 8a）。

### 6.7 局限性

- 当接收方设备存在并发 GPU 渲染任务时信道不可用（52 次"收到 0 数据"的失败被归因于此）（§6.2）。
- Safari 场景带宽明显偏低（≈5.9 bps），作者归因于 Safari 只运行在 Apple GPU 的 Mac 上（§6.3 RQ2.2）。
- 攻击需要两个隔离实例中同时注入恶意脚本，且用户需同时打开两个浏览器（§3.1）。
- §7 明确把"框架泛化到其他信道""GPU 命令队列作为侧信道""更系统的防御分析"列为未来工作。论文 §7 Ethics 与摘要对已回应的厂商表述不一致（摘要求 Firefox/Safari/Tor 确认，§7 写 Firefox/Tor）。

---

## 7. 学习与应用

### 7.1 是否开源？

开源。代码仓库 https://github.com/HugoLeoLJH/C3F （论文 ref [8]，访问日期 2025-10-10），并附在线 demo https://hugoleoljh.github.io/c3f-demo/c3f/receiver.html （ref [9]）。原型规模：JavaScript 3,377 行（四层逻辑）+ Python 1,583 行 + HTML 489 行（§5）。

### 7.2 复现关键步骤

1. 部署两个隔离的网页实例（不同浏览器或普通/无痕模式），分别实现发送端与接收端 WebGL 渲染逻辑。
2. 发送端在 vertex shader 中执行固定时长数学运算（实现取 `sin(x)` 迭代，且把 `sin(x)` 输出作为下一轮 x），重复次数决定负载；接收端持续下发轻量 probe（`drawArrays` + `readPixels`，渲染时间 < 2 ms）。
3. 运行握手：线性回归拟合负载-渲染时间，按 bit-zero threshold（70 ms）与 offset threshold（40 ms）确定双方 bit-0/bit-1 负载。
4. 传输阶段按 512 bit 数据帧 + CRC-32 收发，接收端用 3 ms 间隔的聚类算法解码，失败即重传至超时；结束用 FIN 收尾。

### 7.3 关键超参数、预处理和训练细节

无训练过程（纯协议 + 时序测量）。关键参数：bit-zero threshold = 70 ms、offset threshold = 40 ms（启发式选取）；迭代函数 `sin(x)`；时延测量用 `Date.now()`；聚类切分阈值 3 ms；数据载荷 512 bit；probe 渲染时间典型 < 2 ms；AMT 实验传输 512 bit 随机串，Safari 场景 256 bit（§5、§6.1）。

### 7.4 能否迁移到其他任务？

- **时序型隐蔽信道的通用协议栈**：握手自适应阈值 + 定界符 + CRC + 重传的组合可直接搬到其他"低带宽、高噪声"信道（论文自述框架可换 Raw Channel，但对高噪声信道效果差，§7）。
- **时序侧信道的检测/防御研究**：可作为"GPU 资源共享导致跨实例时序泄漏"的样例，用于评估资源划分（GPU 分区）、确定性计时器、站点隔离等防御（§7 讨论）。
- **流量分析视角**：本信道是端系统内的时序信道，不产生可观测的网络流量特征，与传统加密流量分析互补，属于"端侧侧信道"范畴。

### 7.5 对我的研究有什么启发？

- **跨隔离共享资源清单**：GPU 命令队列这类"操作系统不隔离的硬件资源"是跨实例信道的富矿，值得系统化梳理（CPU cache、GPU 队列、内存带宽、NVMe 等）。
- **协议层设计 > 物理层信噪比**：在 0.3 bps、~50% 准确率的原始信道基础上，靠握手自适应 + 纠错重传达到 100% 完成后准确率；这一"工程化协议把弱信道变可用信道"的范式可迁移到流量隐蔽信道研究。
- **真实环境众包评估**：用 AMT 众包在 232 名工人、多硬件平台的真实设备上做隐蔽信道评估，是比实验室两台机器更有说服力的评测范式，值得在隐蔽信道/流量分析工作中借鉴。

---

## 8. 总结

### 8.1 核心思想

> GPU 命令队列竞争可在浏览器隔离实例间传比特。

### 8.2 速记版 Pipeline

1. 在隔离的两个网页实例中分别注入发送端与接收端脚本。
2. 握手阶段：线性回归 + 双阈值，协商双方 bit-0/bit-1 的渲染负载。
3. 发送端用重负载绘制命令编码数据（512 bit 帧 + CRC-32），接收端用轻量 probe 观测队列延迟。
4. 接收端以 3 ms 间隔聚类解码，校验 CRC，失败则重传。
5. FIN 收尾；实测 AMT 成功率 92.81%、完成后准确率 100%、带宽 6.82 bps。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]]（弱相关：论文 §2.1 把 WF 列为浏览器侧/隐蔽信道攻击的同类威胁，但本文任务为浏览器隔离实例间隐蔽信道，现有概念页无对应主题）

### 9.2 相关方法

- 无。本论文不涉及机器学习方法（知识库方法白名单的 8 个页面均为学习类方法，不适用于本文的时序协议设计）。

### 9.3 相关任务

- 无（现有任务白名单中不存在"隐蔽信道/跨实例隐蔽通信"任务页）。

### 9.4 可更新的综述页面

- 无直接对应的综述页；如需收录，建议未来新增"网络/端侧隐蔽信道"综述页后再行关联。

### 9.5 可加入的对比表

- [[open-source-registry]]（C3F 已开源，仓库与 demo 链接见 §7.1）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| GPU 命令队列竞争信道依赖 OpenGL 同步命令（finish / readPixels）把异步渲染延迟变为可观测 | Table 2 把 GLSL 命令分为 Drawing 与 Syncing 两类，并说明隐式同步语义 | §3.1, Table 2 |
| 真实环境中完成率 92.81%（1,331/1,434 有效实验），失败主要来自握手与 0 数据接收 | Table 3 分项列出 51 次握手失败、52 次未收到数据，并给出 1,524→1,434 的有效实验过滤过程 | §6.2 RQ1.1, Table 3 |
| 传输完成后准确率 100%，归因于自适应阈值协商与 CRC 校验 | 1,331 次成功接收全部精确一致 | §6.2 RQ1.2 |
| 相比 SideR / Loophole，跨模式带宽与准确率大幅领先 | 跨模式平均 8.76 bps vs Loophole 5.00 / SideR 0.25；准确率 100% vs 51.72% / 47.35% | §6.3 RQ2.2, Table 4 |
| 原始信道 Shannon 容量 53.66 bps，远高于 Pool-Party / Loophole / SideR | 本地 Windows + Chrome 上 40 次实验按 Shannon-Hartley 公式计算 | §6.3 RQ2.3, Table 7 |
| Tor 与 fuzzy-time 防御下仍 100% 成功，仅带宽下降 | Tor 场景 5.30 ± 0.14 bps；Chrome fuzzy-time 15 ms 时 6.45 ± 2.22 bps | §6.5 RQ4, Table 8, Table 9 |
| 带宽与 GPU 利用率可折中（6 bps ≈ 60% 利用率） | 通过改变发送端负载频率调节带宽并测 GPU 利用率 | §6.4 RQ3.3, Fig. 12 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-S&P-Practical_Covert_Channel_Across_Isolated_Browser_Instances_via_GPU_Command_Queue_Contention.pdf
- MinerU Markdown：02-parsed-markdown/2026-S&P-Practical_Covert_Channel_Across_Isolated_Browser_Instances_via_GPU_Command_Queue_Contention.md

---

## 12. 后续问题

- 该信道在 Windows/macOS 之外的平台（Linux、Android Chrome、移动端 Safari）是否同样成立？解析稿未提供移动端实验。
- 论文把 GPU 资源分区列为可能的防御，但因"静态分配低效、动态分配难预测"未做实验；分区后信道是否真正失效仍是开问题（§7）。
- 若把该信道用于跨隔离 cookie 同步，其端到端追踪收益（与 Storage Access API、隐私沙盒等对照）论文未量化。
- 论文摘要与 §7 Ethics 对已回应的厂商集合描述不一致（Safari 是否确认），引用时需谨慎。

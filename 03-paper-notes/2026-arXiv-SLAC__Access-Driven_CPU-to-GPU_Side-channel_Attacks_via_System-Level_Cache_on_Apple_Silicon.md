---
type: paper
title_original: "SLAC: Access-Driven CPU-to-GPU Side-channel Attacks via System-Level Cache on Apple Silicon"
title_cn: "SLAC：Apple Silicon 上经系统级缓存的访问驱动型 CPU-to-GPU 侧信道攻击"
authors: [Tianhong Xu, Saion K. Roy, Aidong Adam Ding, Ruyi Ding, Yunsi Fei]
year: 2026
venue: "arXiv 2026"
doi: "unknown"
url: "https://arxiv.org/abs/2608.09075"
pdf: "00-inbox/PDFs/2026-arXiv-SLAC__Access-Driven_CPU-to-GPU_Side-channel_Attacks_via_System-Level_Cache_on_Apple_Silicon.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-SLAC__Access-Driven_CPU-to-GPU_Side-channel_Attacks_via_System-Level_Cache_on_Apple_Silicon.md"
status: processed
reading_level: L1
research_area: []
task: []
method: []
dataset: ["Cora", "Citeseer", "Pubmed", "Computers", "Photo", "MedQuad", "FinancialQA"]
code: "https://anonymous.4open.science/r/SLAC_CCS2026-7FB3"
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

# SLAC: Access-Driven CPU-to-GPU Side-channel Attacks via System-Level Cache on Apple Silicon

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | SLAC: Access-Driven CPU-to-GPU Side-channel Attacks via System-Level Cache on Apple Silicon |
| 中文标题 | SLAC：Apple Silicon 上经系统级缓存的访问驱动型 CPU-to-GPU 侧信道攻击 |
| 作者 | Tianhong Xu, Saion K. Roy, Aidong Adam Ding, Yunsi Fei（Northeastern University）、Ruyi Ding（Louisiana State University） |
| 年份 | 2026 |
| 会议/期刊 | arXiv 2026（解析稿首页无会议页眉；文中 artifact 声明出现 "CCS open-science policy" 字样，推断为投向 ACM CCS 的稿件） |
| 研究方向 | 微架构侧信道攻击（CPU-GPU 异构 SoC 缓存共享，非流量分析主题） |
| 任务类型 | 侧信道攻击与端到端隐私攻击（GNN 边恢复、LLM 输入/输出恢复） |
| 方法关键词 | Prime+Probe、SLC 集合索引逆向、碰撞轮廓聚类、CPrime/CProbe、GPrime（GPU 并行 priming）、差分追踪 |
| 数据集 | Cora、Citeseer、Pubmed、Computers、Photo（GNN）；MedQuad、FinancialQA（LLM prompt） |
| 是否开源 | 匿名 artifact 包 `https://anonymous.4open.science/r/SLAC_CCS2026-7FB3`（含两种侧信道实现、trace 处理与攻击算法） |
| PDF | 00-inbox/PDFs/2026-arXiv-SLAC__Access-Driven_CPU-to-GPU_Side-channel_Attacks_via_System-Level_Cache_on_Apple_Silicon.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-arXiv-SLAC__Access-Driven_CPU-to-GPU_Side-channel_Attacks_via_System-Level_Cache_on_Apple_Silicon.md |

---

## 1. 一句话总结

> 逆向 Apple M1 SLC 的 12 位哈希集合索引，首次实现 CPU→GPU 的访问驱动 Prime+Probe 侧信道（62.5–400 Kbps），并恢复 GNN 边与 LLM 输入/输出。

---

## 2. 摘要翻译

### 2.1 摘要原文

> "In this work, we target Apple Silicon heterogeneous SoCs and discover that GPU memory accesses leave set-level footprints in the shared SLC, observable to an unprivileged CPU process. This keen observation enables the first fine-grained, access-driven, Prime+Probe-style CPU-to-GPU cache side-channel attacks against GPU workloads... a graph-edge reconstruction attack on Graph Neural Networks (GNNs) that achieves 90% edge accuracy across five datasets, and an LLM privacy attack that recovers input keywords with up to 94.8% accuracy and model responses with up to 88.9% accuracy."（Abstract，节选）

### 2.2 摘要中文翻译

现代异构 SoC 集成 CPU 核与共享 LLC/SLC 的 GPU，这一共享暴露了新的跨域攻击面：已有的集成平台攻击要么利用粗粒度缓存占用争用，要么要求攻击者与受害者在 GPU 上共驻以获得精确计时。本文针对 Apple Silicon 异构 SoC，发现 GPU 访存会在共享 SLC 中留下集合级足迹，且可被非特权 CPU 进程观测。基于该发现，本文实现首个细粒度、访问驱动的 Prime+Probe 式 CPU→GPU 缓存侧信道：先逆向 Apple M1 SLC 的集合索引函数及私有缓存与 SLC 的交互，构建 CPrime+CProbe（CPU 侧完成 SLC priming 与 probing，达到缓存集合粒度监控 GPU 受害者）；进而提出加速变体 GPrime+CProbe（用 GPU 加速 SLC priming，隐蔽信道吞吐提升 6.4×）。最后演示两类端到端隐私攻击：GNN 图边重建（五个数据集上边恢复准确率 >90%）与 LLM 隐私攻击（TinyLlama 与 GPT-2 Medium 上输入关键词恢复最高 94.8%、模型回复恢复最高 88.9%）。结果揭示 Apple Silicon 的一类新微架构漏洞，呼吁异构 SoC 的安全系统缓存设计。

> ⚠️ MinerU 解析问题：标题解析为 "Atacks"（应为 "Attacks"）；正文存在 small-caps 下标碎片（如 Ab<sub>s</sub>t<sub>rac</sub>t、I<sub>n</sub>t<sub>ro</sub>d<sub>uc</sub>ti<sub>on</sub>、Fi<sub>gure</sub>）；第 140 行出现无意义乱码串（"�890723双56780222232425262223333"），疑似解析噪声。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

GPU 承载越来越多隐私敏感负载（ML 推理等）；异构 SoC 中 CPU/GPU 共享缓存形成跨域泄漏路径。已有工作只在 Intel 平台给出概念验证（Leaky Buddies），且 Apple 平台上仅存在粗粒度的缓存占用攻击，无法解析到集合/行级别，因而无法恢复模型输入或密钥这类细粒度秘密（§1、§2.3）。

### 3.2 现有方法的痛点和不足

① 现有 CPU→GPU 攻击只有缓存占用级（利用聚合使用量做 website fingerprinting/截屏），空间粒度不足；② 要获得精确计时需与受害者在 GPU 共驻，威胁模型受限；③ Apple M1 的 SLC 对 CPU 私有缓存是 exclusive（CPU 访存不能直接填充 SLC）、且集合索引为全哈希（无公开知识），使传统驱逐集构造（迭代剪枝）不收敛（§2.2.1、§3 挑战 1/2）。

### 3.3 论文的研究假设或核心直觉

关键观察：SLC 相对 GPU 私有缓存是 NINE 关系，GPU 访存会直接把行载入 SLC；相对 CPU 私有缓存是 exclusive，但 CPU 首次访问 SLC 常驻行会命中。因此"用 GPU 填 SLC、用 CPU 计时观测"可建立集合级侧信道（§3.1 三场景）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | GPU 访存可在 SLC 留集合级足迹，CPU 侧首次访问可区分 SLC 命中/缺失 | §3.1 场景 ➁➂ |
| 痛点提炼 | CPU 私有缓存与 SLC 互斥导致传统驱逐集与 Prime+Probe 流程不适用 | §3 挑战 1 |
| 问题转化 | 需先逆向 SLC 集合索引函数与替换策略，才能构造目标集合驱逐集 | §3.2–3.3 |
| 文献定位 | Intel 平台已有跨域 Prime+Probe（概念验证），Apple Silicon 无集合级工作 | §2.3 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | GPU 访存导致的 SLC 集合级驱逐可被非特权 CPU 进程可靠观测并用于比特级通信 | §3.1、§4.1 | 隐蔽信道吞吐与解码准确率（§4.5） |
| 辅助假设（如有） | 全哈希 12 位索引可通过碰撞轮廓聚类恢复等价索引函数 | §3.2 | 聚类得到 4,096 簇并选出 12 个线性无关位函数（§3.3） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 集合级 CPU→GPU 侧信道可行 | 支撑 | CPrime+CProbe 62.5 Kbps；GPrime+CProbe 400 Kbps（6.4×） | §4.5 |
| 索引函数可恢复 | 支撑 | 碰撞轮廓聚类得 4,096 簇（12 位索引），LRU 替换策略确认 | §3.3 |

---

## 4. 方法设计

### 4.1 方法整体流程

① 逆向：追踪 CPU-GPU 共享数据三种迁移场景 → 碰撞轮廓聚类构造驱逐集 → 恢复 12 位 SLC 集合索引函数（4,096 集合、16 路、128B 行、LRU）并验证替换策略；② 侧信道：CPrime（CPU 两步 priming：SLC_ES 65,536 行 + L2_ES）或 GPrime（GPU 写核+读核，0.7 ms）+ CProbe（CPU 计时得 4,096 长度整数 trace）；③ 端到端攻击：差分追踪 + 多轮平均/超集聚合降噪 → 三阶段（profiling / trace collection / secret recovery）恢复 GNN 边与 LLM token（§3、§4、§5.1）。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | 共享内存中的测试区 | GPU 填 SLC，逐行测碰撞轮廓 | 每行碰撞轮廓 | 替代噪声敏感的迭代剪枝 |
| Step 2 | 测试区（1.2× SLC 容量） | 按轮廓相似度聚类 + 物理地址提取 | 4,096 簇 → 12 个索引位函数 | 得到等价集合索引 |
| Step 3 | 目标集合驱逐集 | CPrime（SLC_ES+L2_ES）或 GPrime（GPU 双核）填满 SLC | 已 priming 的 SLC | 建立初始态 |
| Step 4 | 受害 GPU kernel 执行后 | CProbe 复访 SLC_ES 计时，统计每集合缺失行数 | 长度 4,096、取值 0–16 的整数 trace | 观测受害者访存强度 |
| Step 5 | 基线与目标 trace | 差分追踪 + 多轮平均或超集聚合 | 降噪后的访存向量 | 支撑秘密恢复 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| SLC 逆向模块 | 恢复集合索引与替换策略 | 测试区碰撞轮廓 | 12 位索引函数、LRU 结论 | 为驱逐集构造提供依据 |
| CPrime | 纯 CPU 两步填充 SLC | SLC_ES（65,536 行）、L2_ES | 全 SLC 被占用 | 无需 GPU 权限 |
| GPrime | GPU 写核失效 CPU 副本 + 读核载入 SLC | SLC_ES、index_sets 结构 | 0.7 ms 完成 priming | 需 Metal 权限但快 10× |
| CProbe | CPU 计时探测 | SLC_ES | 整数 trace（4,096×0–16） | 始终在 CPU 侧 |
| 攻击恢复层 | 三阶段恢复秘密 | 访问映射矩阵 M、观测向量 v | GNN 边 / LLM token | 复用侧信道输出 |

### 4.4 公式、算法和机制解释

- 集合索引恢复：以 XOR 建模每个索引位（26 个候选地址位 → 2^26 候选函数），用"簇内一致 + 4,096 簇上均匀对半"过滤得 4,095 个有效位函数，再选 12 个线性无关者构成等价索引（§3.3）；
- CPrime 关键优化：SLC_ES 固定在地址位 7–10 为 0（页内偏移可控），把受影响的 L2 集合数 n_L2 从 8,192 降到 512，缩短 priming 时间（§4.2）；
- 隐蔽信道编码：每通信周期接收方 prime 一个集合、发送方整集合调制（写满 16 行＝1，不动＝0），接收方仅探测最后 5 个 primed 地址；CPrime 单集合解码仅 88%，故 4 集合/比特聚合至 >99%；GPrime 1 集合/比特即 >99%（§4.5）；
- 攻击降噪：差分追踪（目标 trace 减基线 trace）+ 多轮平均（CPrime 4,000 轮 / GPrime 1,000 轮）或超集聚合（64 超集，FNR 0.08–0.17%、FPR 1.03–2.63%）（§5.1, Table 1）。

### 4.5 方法优势

首次实现 Apple Silicon 上集合级、访问驱动的 CPU→GPU 侧信道；CPrime 变体无需任何 GPU 权限（纯 CPU 攻击者）；GPrime 借 GPU 并行把 priming 从 7 ms 压到 0.7 ms（吞吐 62.5→400 Kbps）；监控粒度从"占用率"提升到"每集合 0–16 行计数"，信息量远超二值信号（§4.2–4.5）。

### 4.6 方法不足

CPrime 依赖两步 priming，噪声大（单集合解码 88%，需 4× 冗余与 4,000 轮平均）；地址位固定过多会触发 macOS 页重映射导致驱逐集失效（故止于固定 4 位，§4.2）；GPrime 需攻击者具备 GPU 执行权限；Apple GPU 缺乏可靠细粒度计时，无法从 GPU 侧探测（§4.1）；GPU 写不分配 SLC 需额外写核失效 CPU 副本（§4.3）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

与缓存占用型攻击（如 Apple M1 上的 SLC 占用 WF/截屏）相比，本文是访问驱动、集合级的 Prime+Probe，可解析到具体集合的占用行数；与 Intel 平台 Leaky Buddies 相比，本文处理的是 CPU 私有缓存与 SLC 互斥、SLC 全哈希索引的平台，priming 机制完全不同（§2.2–2.3）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| SLC 全哈希索引逆向 | 碰撞轮廓聚类 + XOR 位函数筛选，恢复 12 位索引与 LRU | 高 | 部分（方法论可迁移到其他未知索引缓存） |
| CPrime+CProbe | 纯 CPU 攻击者的集合级 CPU→GPU 侧信道 | 高 | 是（威胁模型最弱变体） |
| GPrime+CProbe | GPU 并行 priming，10× 加速、6.4× 吞吐 | 高 | 是 |
| 端到端攻击链 | GNN 边恢复与 LLM 输入/输出恢复 | 高 | 是（embedding 查表泄漏面具有通用性） |

### 5.3 适用场景

Apple M 系列 SoC 上以 PyTorch/Metal 部署的 GPU 推理负载（GNN、LLM）；攻击者为同机非特权进程、无需与受害者共驻 GPU（CPrime）或可执行 Metal kernel（GPrime）（§5.2–5.3 威胁模型）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 缓存占用型攻击（前人） | 易部署、抗噪 | 仅聚合粒度，不能恢复细粒度秘密 | 提升到集合级、每集合 0–16 行计数 |
| Leaky Buddies（Intel，GPU→CPU） | 概念验证跨域侧信道 | 仅 Intel 集成平台概念验证 | 首个 Apple Silicon CPU→GPU 集合级实现 |
| 传统迭代剪枝驱逐集 | 在部分哈希索引下有效 | 全哈希下候选池数万、噪声下不收敛 | 碰撞轮廓聚类，抗噪且可扩展 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

平台：8GB Apple M1（Firestorm P 核 + 12MB L2 + 共享 SLC）；侧信道评估用受控隐蔽信道（GPU kernel 发送、CPU 进程接收，毫秒级同步）；端到端攻击用差分追踪 + 平均/超集聚合降噪（§3.3、§4.5、§5.1）。

### 6.2 数据集

GNN：Cora、Citeseer、Pubmed、Computers、Photo（GCN 模型，PyTorch + Metal）；LLM：MedQuad（1,000 种疾病）与 FinancialQA（100 个股票代码）prompt 数据集；模型为 TinyLlama（1.1B）与 GPT-2 Medium（0.35B）（Table 2–3、§5.3）。

### 6.3 Baseline

无同类 Apple Silicon 集合级方法可对比；对照为粗粒度占用攻击（前人 [32]）与 Intel 概念验证（[6]），以及两种自研变体（CPrime vs GPrime）互为对照（§2、§4.5）。

### 6.4 评价指标

隐蔽信道吞吐（Kbps）、比特解码准确率；侧信道保真（undercount/overcount、FNR/FPR）；GNN 边恢复 precision/recall；LLM 关键词与回复恢复准确率（§4.5、Table 1–4）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| 隐蔽信道 | 吞吐 | 62.5 Kbps（CPrime）/400 Kbps（GPrime） | 62.5 Kbps | 6.4× | GPrime 单周期 4,096 bit；priming 7 ms→0.7 ms |
| 解码准确率 | bit accuracy | >99%（聚合后） | 88%（CPrime 单集合） | — | 4 集合/比特聚合 vs 1 集合/比特 |
| GNN 边恢复（全图，Table 2） | P/R | Cora 98.2/94.2（CPrime）、99.9/97.3（GPrime） | 单节点 84.3/97.2 | — | 五个数据集全图 P >86%（CPrime），GPrime 在稀疏图上 P >99% |
| LLM 输入关键词恢复（Table 4） | 准确率 | 76–81%（CPrime）/91–95%（GPrime） | — | — | MedQuad 与 FinancialQA、两模型 |
| LLM 回复恢复 | 准确率 | 最高 88.9%（GPT-2 Medium，GPrime） | 70.5%（TinyLlama，CPrime） | — | FinancialQA/GPT-2 最优 |
| 侧信道保真（Table 1） | FNR/FPR（超集） | 0.17%/2.63%（CPrime，64 超集） | 0.08%/1.03%（GPrime） | — | GPrime 需 1,000 轮平均 vs CPrime 4,000 轮 |

### 6.6 优势最明显的场景

纯 CPU 攻击者（无 GPU 权限）即可在稠密图（Computers/Photo 类）与 LLM embedding 查表场景恢复高价值秘密；拥有 Metal 权限时 GPrime 以更低噪声达到更高精度与吞吐（§5.2–5.3）。

### 6.7 局限性

攻击依赖受害工作负载的访存模式可 profile（访问映射矩阵需预先建立，属 chosen-query/threat-model 假设）；稠密图上单节点恢复精度明显下降（Computers 30.8%），依赖全图双向确认补救；Apple GPU 无细粒度计时使探测必须在 CPU 侧完成；未评估对抗性噪声或防御（缓存着色、随机化索引、恒定时间实现）下的表现（§4.2、§5.1–5.3）。

---

## 7. 学习与应用

### 7.1 是否开源？

是（匿名）：文中给出匿名 artifact 包 `https://anonymous.4open.science/r/SLAC_CCS2026-7FB3`，声明包含 CPrime+CProbe/GPrime+CProbe 实现、trace 处理脚本与 GNN/LLM 攻击算法；正式发布地址未提及。

### 7.2 复现关键步骤

1. 在 Apple M1 上用 GPU 填充区 + 测试区做碰撞轮廓收集，聚类得到 4,096 个集合簇并提取物理地址；
2. 用 XOR 位函数筛选流程恢复 12 位索引与 LRU 顺序；
3. 构造 SLC_ES/L2_ES（或 GPU 双核 GPrime）与 CProbe，建立隐蔽信道并测吞吐/准确率；
4. 实现差分追踪与两类降噪方法，跑 GNN 边恢复与 LLM token 恢复。

### 7.3 关键超参数、预处理和训练细节

集合结构：4,096 集合 × 16 路 × 128B 行；测试区取 1.2× SLC；候选地址位 7–32（26 位），固定位 7–10 为 0；SLC_ES = 65,536 行；GPrime 线程组 1,024；通信时隙 8 ms（CPrime）/2 ms（GPrime）/6 ms（CProbe）；平均轮数 4,000（CPrime）/1,000（GPrime），超集数 64（§3.3、§4.2–4.5、§5.1）。

### 7.4 能否迁移到其他任务？

可迁移的机制：① "碰撞轮廓聚类替代迭代剪枝"适用于任何索引函数未知或高度哈希的共享缓存/资源驱逐集构造；② 差分追踪 + 多轮平均/聚合的降噪组合是通用的侧信道后处理模板；③ GNN/LLM 攻击中的"profiling→trace→secret recovery"三阶段与访问映射矩阵对比法，可用于其他"已知候选集合 + 观测占用向量"的推理问题（以下为笔记作者的迁移分析，非论文原文主张）。

### 7.5 对我的研究有什么启发？

对流量分析研究的间接启发：端侧模型推理会产生可被同机进程从共享硬件资源侧信道观测的细粒度访存模式，这类"本地侧信道 + 模型结构先验"的威胁模型与远程流量侧信道形成互补；此外其差分追踪/多轮平均的降噪思路与流量侧信道中的基线相减、重复测量聚合如出一辙。

---

## 8. 总结

### 8.1 核心思想

> 用 GPU 填 SLC、CPU 计时，实现集合级跨域侧信道。

### 8.2 速记版 Pipeline

1. 追踪 CPU-GPU 共享数据三场景，确认 SLC 可被 CPU 观测；
2. 碰撞轮廓聚类构造驱逐集，逆向 12 位 SLC 索引与 LRU；
3. CPrime（CPU 两步）或 GPrime（GPU 双核）填满 SLC，CProbe 计时得 4,096 维整数 trace；
4. 隐蔽信道：CPrime 62.5 Kbps、GPrime 400 Kbps（4 集合/比特 vs 1 集合/比特）；
5. 差分追踪 + 平均/超集聚合，恢复 GNN 边（P 最高 99.9%）与 LLM 输入/回复（最高 94.8%/88.9%）。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]]（论文 §2.1 指出缓存占用型攻击的典型应用即 website fingerprinting，其引用的 Shusterman 等 TDSC 2020 正是缓存占用通道 WF 工作；本文把粒度从占用提升到集合级，属对同一泄漏面的深化）

### 9.2 相关方法

- 库内无对应方法页：本文方法属微架构侧信道（非白名单 8 个 ML 方法 slug），不建链。

### 9.3 相关任务

- 库内暂无对应任务页（论文的端到端任务是 GNN 边恢复与 LLM 隐私攻击，均非流量分析任务）。

### 9.4 可更新的综述页面

- 暂无：与库内 5 个综述页主题不重叠；若日后建立"本地/侧信道类隐私攻击"综述页可回链。

### 9.5 可加入的对比表

- [[open-source-registry]]（论文公开匿名 artifact 包，可登记，注明为匿名托管地址）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 首个 Apple Silicon 集合级 CPU→GPU 访问驱动侧信道；CPrime+CProbe 62.5 Kbps、GPrime+CProbe 400 Kbps（6.4×） | 摘要与贡献 (2)；§4.5 | §1、§4.5 |
| SLC 结构：4,096 集合、16 路、128B 行、LRU；全部 12 个索引位由哈希生成（碰撞轮廓聚类得 4,096 簇） | §3.3 与 Figure 4 | §3.3 |
| CPrime 固定地址位 7–10 使 n_L2 从 8,192 降到 512；GPrime 用 GPU 写核+读核把 priming 从 7 ms 降到 0.7 ms | §4.2、§4.3 | §4.2–4.3 |
| GNN 全图边恢复：五数据集 P 86.6–99.8%、R 90.5–97.9%（CPrime），GPrime 最高 99.9/98.8 | Table 2 | §5.2 |
| LLM 输入关键词恢复 76–81%（CPrime）→91–95%（GPrime）；回复恢复最高 88.9% | Table 4、§5.3 | §5.3 |
| 降噪：超集聚合 FNR 0.08–0.17%、FPR 1.03–2.63%（64 超集，单轮） | Table 1 | §5.1 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-arXiv-SLAC__Access-Driven_CPU-to-GPU_Side-channel_Attacks_via_System-Level_Cache_on_Apple_Silicon.pdf
- MinerU Markdown：02-parsed-markdown/2026-arXiv-SLAC__Access-Driven_CPU-to-GPU_Side-channel_Attacks_via_System-Level_Cache_on_Apple_Silicon.md

---

## 12. 后续问题

- 暂未整理。

---
type: paper
title_original: "Mitigating Proxy-Induced Traffic Drift in Website Fingerprinting via Model-Agnostic Traffic Tailoring"
title_cn: "PA3：基于模型无关流量裁剪缓解网站指纹中的代理诱导流量漂移"
authors: ["Linxiao Yu", "Tianyu Cui", "Xinhao Deng", "Yuqi Qing", "Jun Tao", "Ke Xu", "Qi Li"]
year: 2026
venue: "arXiv 2026"
doi: unknown
url: "https://arxiv.org/abs/2608.20692"
pdf: "00-inbox/PDFs/2026-arXiv-Mitigating_Proxy-Induced_Traffic_Drift_in_Website_Fingerprinting_via_Model-Agnostic_Traffic_Tailoring.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-Mitigating_Proxy-Induced_Traffic_Drift_in_Website_Fingerprinting_via_Model-Agnostic_Traffic_Tailoring.md"
status: processed
reading_level: L2
research_area: ["website-fingerprinting", "encrypted-traffic-analysis", "censorship-circumvention"]
task: ["website-fingerprinting"]
method: []
dataset: ["PA3 proxied website traffic dataset", "Firefox 132-141 BIH dataset"]
code: "https://github.com/wesly2000/PA3"
relevance: high
created: "2026-09-19"
updated: "2026-09-19"
---

# Mitigating Proxy-Induced Traffic Drift in Website Fingerprinting via Model-Agnostic Traffic Tailoring

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Mitigating Proxy-Induced Traffic Drift in Website Fingerprinting via Model-Agnostic Traffic Tailoring |
| 中文标题 | PA3：基于模型无关流量裁剪缓解网站指纹中的代理诱导流量漂移 |
| 作者 | Linxiao Yu, Tianyu Cui, Xinhao Deng, Yuqi Qing, Jun Tao, Ke Xu, Qi Li（东南大学网络空间安全学院 / 中关村实验室 / 清华大学网络科学与网络空间研究院 / 清华大学计算机科学与技术系） |
| 年份 | 2026 |
| 会议/期刊 | arXiv 2026 预印本（任务书分配 arXiv:2608.20692；解析稿正文未标注会议名） |
| 研究方向 | 代理流量下的网站指纹（WF）、代理诱导特征漂移（proxy-induced feature drift）、跨协议泛化、攻击侧预处理 |
| 任务类型 | 未见代理协议上的 WF 攻击泛化（VMess / Shadowsocks / Trojan 三协议两两交叉）；代理协议识别；跨协议流量对齐 |
| 方法关键词 | 两阶段（结构指纹提取 + 流量裁剪）、BFT（BIH 背景流大小过滤）、PHT（n-gram 代理握手序列检测与裁剪 + SEQ-ACK 分析）、POT（BSM 字节-分段图斜率比 burst 重标定）、model-agnostic 预处理 |
| 数据集 | 自采代理流量数据集（约 1 TB、80 网站、NoProxy/VMess/Shadowsocks/Trojan 四协议、商业代理服务 + 中美 3 台客户端）+ Firefox 132–141 版本数据集（BIH 稳定性） |
| 是否开源 | 是 —— 源码与全部数据集：https://github.com/wesly2000/PA3（正文 §I 末句） |
| PDF | 00-inbox/PDFs/2026-arXiv-Mitigating_Proxy-Induced_Traffic_Drift_in_Website_Fingerprinting_via_Model-Agnostic_Traffic_Tailoring.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-arXiv-Mitigating_Proxy-Induced_Traffic_Drift_in_Website_Fingerprinting_via_Model-Agnostic_Traffic_Tailoring.md |

---

## 1. 一句话总结

> 把"代理协议差异导致的 WF 特征漂移"归结为代理层为加密与协议通信插入的额外字节，用少量可解密探针流量提取三类协议结构指纹（BIH 流大小模式 / 代理握手包序列 / BSM 斜率比），编译成只依赖加密后可观测元数据的裁剪规则作用在目标流量上——这一 model-agnostic 预处理让 6 个 WF 模型在未见协议上平均提升 0.12 F1（约 27% 相对），最大单点增益 +0.41，最好情形 F1 > 0.96。

---

## 2. 摘要翻译

### 2.1 摘要原文

Website fingerprinting (WF) based on deep learning can effectively identify websites from encrypted traffic. However, users often rely on proxy protocols to bypass censorship, and the diversity of these protocols poses a major challenge, as WF models trained on traffic from one set of protocols perform poorly when evaluated on that from unseen protocols. We attribute this issue to proxy-induced feature drift, where traffic patterns of the same website vary with the proxy protocol, leading to discrepancies that WF models fail to capture and severe performance degradation. To tackle this issue, we propose PA3, a model-agnostic preprocessing framework to analyze and mitigate the proxy-induced drift. PA3 first fingerprints the protocol-specific drift. These fingerprints are then used to tailor the proxied traffic for feature alignment, which mitigates the drift and considerably improves the generalization of WF models on traffic from unseen protocols. Extensive evaluations demonstrate that PA3 substantially enhances generalization on unseen protocols with an average improvement of 0.12 in F1-score (roughly 27% relative), achieving up to a 0.41 absolute gain across models, which narrows the performance gap introduced by the drift. In the best case, PA3 enables WF models to obtain F1-scores above 0.96 on traffic from unseen protocols.

### 2.2 摘要中文翻译

基于深度学习的网站指纹（WF）能够从加密流量中有效识别网站。然而，用户常依赖代理协议绕过审查，而这些协议的多样性构成重大挑战：在一组协议流量上训练的 WF 模型，在被评测于未见协议的流量时表现很差。我们把该问题归因于**代理诱导的特征漂移**（proxy-induced feature drift）——同一网站的流量模式随代理协议变化，产生 WF 模型无法捕捉的差异并导致严重性能退化。为解决该问题，我们提出 PA3：一个 model-agnostic 的预处理框架，用于分析并缓解代理诱导漂移。PA3 首先对协议特有的漂移做结构化指纹提取，再用这些指纹裁剪代理流量以做特征对齐，从而缓解漂移并显著提升 WF 模型在未见协议流量上的泛化。大量评测表明，PA3 显著增强了未见协议上的泛化：F1 平均提升 0.12（相对约 27%），跨模型最高取得 0.41 的绝对增益，缩小了漂移造成的性能差距。最好情形下，PA3 使 WF 模型在未见协议流量上获得高于 0.96 的 F1。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

现有 WF 工作隐含一个**协议一致性假设**：训练与测试流量来自同一组代理协议。现实中用户会在 VMess、Shadowsocks、Trojan 等协议间自由切换，测试时模型会遭遇完全未见过的协议。作者发现这种不匹配导致严重退化（Fig. 9：对角线上 P_train = P_test，各模型 F1 > 0.94；一旦 P_train ∩ P_test = ∅，连漂移较鲁棒的 TF、TikTok 都大幅下降，DF 的 F1 跌到 0.56 以下）。作者给出的解释是：模型会学习并压缩**训练样本共享的协议特有通信模式**（如握手序列模式），这类共性对区分网站没有判别信息（引向了 information bottleneck 文献 [19][20]），一旦测试协议换了，这种压缩不再适用。

### 3.2 现有方法的痛点和不足

1. **协议一致性假设普遍被默认**：以往 WF 攻击与防御研究几乎都在单一或固定协议集合下评测，未见协议上的泛化缺口未被系统研究。
2. **通用数据增强不足以缓解代理层漂移**：NetAugment、DyWin、Rosetta、NetRandAugment 等主要模拟网络层/传输层变化（丢包、聚合、时间抖动、窗口级增强），对代理层引入的失真"不对症"（§V-B：PA3 在几乎所有设定都优于这些方法）。
3. **已有跨环境特征选择方法依赖测试协议**：Li et al. [18] 的框架选出的特征依赖所选网站、且需要访问测试集中的协议，特征不是网站无关的，泛化性受限。
4. **直接删除额外字节在攻击期不可行**：真实 WF 攻击中攻击者只能被动观测加密流量，无法定位并剥离这些字节。

### 3.3 论文的研究假设或核心直觉

代理诱导漂移的**根因**是代理层为加密与代理层通信插入的额外字节：这些字节与网站身份无关，却扰乱了包大小与分段模式；且代理软件逐连接独立处理，因此漂移在**流级别**引入，而一个网站 trace 只是多条并发流的混合。由此得到核心直觉：把这些多余字节从每条流中去掉，就能让测试流量与训练流量对齐，即"把协议一致性假设变成可实现的"。由于攻击期流量已加密，PA3 改用**两阶段**策略：先在受控环境下用可解密的**探针流量**（probe traffic）对同一网站跨协议做 payload-aware 比较、得到 ground truth 与结构指纹，再把指纹编译成**payload-agnostic 规则**，在加密目标流量上执行裁剪。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | Fig. 9：WF 模型在 P_train = P_test 时 F1 > 0.94，在 P_train ∩ P_test = ∅ 时急剧退化（DF < 0.56）；Table I 调查 10 家商业代理服务商，确认 VMess/Shadowsocks/Trojan 是实际部署最广的三种协议 | §V-B Fig. 9, §II Table I |
| 痛点提炼 | 用户现实中使用多样化代理协议，攻击者无法保证训练集覆盖测试协议；通用增强方法只模拟网络/传输层变化，不对症；Li et al. 的特征选择又依赖测试协议 | §II, §V-B |
| 问题转化 | 把"协议换了模型就崩"提升为"代理诱导特征漂移"这一可度量的科学问题：漂移是否源于代理层插入的额外字节？这些字节能否在不看 payload 的前提下被定位与消除？ | §I, §IV-A（推断：问题化过程为本文叙事主线） |
| 文献定位 | 现有 WF 研究默认协议一致；代理检测侧已有工作利用封装 TLS 握手 [1]、跨层 RTT [2] 暴露的协议特征，说明协议层结构确实可被外部观测——这为"用结构指纹反推漂移"提供了可行性依据 | §I, §II（引 [1][2][6]–[8]） |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 H1 | 代理诱导漂移来自代理层插入的额外字节（背景流 + 握手序列 + 传输期 overhead 三处），在流级别消除/对齐这些字节即可把跨协议泛化拉回接近同协议水平 | §I（额外字节与网站身份无关）、§IV-B | 实验：Table III 跨协议 F1 对比、Table IV 消融、Fig. 9 |
| 辅助假设 H2 | 少量解密探针流量中提取的协议结构指纹，可以编译成只依赖加密后可观测元数据（流大小、包位置、方向包大小、时序）的规则，在攻击期仍有效 | §IV-B「The goal is not to use decrypted information during the real WF attack」 | 实验：Table II 协议识别误差、Table III 裁剪效果、§V-E 低采样比稳定性 |
| 辅助假设 H3 | 访问生命周期三阶段的漂移可用三个互补模块分别处理（背景流 / 代理握手 / 传输开销） | §IV-B 三条 Knowledge I–III | 实验：Table IV 三档消融 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| H1 | 支撑（部分） | 三模块全开时 6 个模型 × 6 个协议对几乎全部优于 unmitigated baseline（Table III）；消融显示任一模块单独移除后仍优于 baseline，但均差于完整 PA3，佐证"三处漂移互补、需共同处理"；未达到同协议水平（如 DF VMess→Shadowsocks 0.774 仍低于同协议 >0.94） | §V-B Table III, §V-D Table IV |
| H2 | 支撑 | 攻击期只用元数据即可识别协议（flow-level 误差 ≤0.587%、session-level ≤0.059%，Table II）；参数从仅 5 个网站、5% 占比的探针流量估计即稳定（Table V/VI、Fig. 13） | §V-B Table II, §V-C, §V-E |
| H3 | 支撑 | Table IV：六组协议对中 w/o BFT / w/o PHT / w/o POT 全部优于 baseline，且完整 PA3 在全部六组中取得最高 F1 | §V-D Table IV |

---

## 4. 方法设计

### 4.1 方法整体流程

PA3 分两阶段（Fig. 2）：

1. **Structural Fingerprinting of Proxied Traffic（知识提取）**：在受控环境中为每个代理协议采集少量可解密的探针流量，记录解密密钥，对**同一 hostname** 跨协议做 payload-aware 比较，隔离出代理层插入的额外字节，并把规律固化为三类"结构指纹 + Knowledge I–III"。
2. **Traffic Tailoring for Drift Mitigation（知识应用）**：把指纹编译成 payload-agnostic 规则；攻击期对被动观测的加密流量先做协议识别，再依次执行 BFT → PHT → POT 三个裁剪模块，最后把裁剪后的 trace 交给现有 WF 模型（不改结构、不重训，plug-and-play）。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | 受控客户端 + 商业代理服务 | 用 Selenium + 改造版 Clash Core 自动采集各协议探针流量并记录密钥材料；论文用 5 个网站、占完整数据集 5% 的探针 | 每个协议的解密探针流量 | 建立 ground truth，隔离代理层效应与常规噪声（拥塞、重传、流交错） |
| Step 2 | 解密探针流量 | 对同 hostname 跨协议比较三类结构：BIH 背景流大小直方图（Fig. 3/4）、TLS Client/Server Hello 的流内包索引（Fig. 5）、BSM 字节-分段图斜率（Fig. 6/7） | Knowledge I–III 与统计量（直方图、n-gram 词表、斜率比 μ/σ） | 定位三处漂移来源 |
| Step 3 | 统计量 | 编译规则：BFT 过滤区间（覆盖度 α）、PHT 异常窗口词典（词表大小 v）、POT 的高斯缩放因子 λ ~ N(μ, σ) | 每协议的裁剪规则 | 把解密域知识转为加密域可执行规则 |
| Step 4 | 加密目标 trace | n-gram 词典匹配做 flow-level 协议识别，再按会话内多数投票定 session-level 协议 | 协议标签 | 选择对应协议规则（消除"未知协议"歧义） |
| Step 5 | 加密目标 trace + 规则 | 依次执行 BFT（按大小过滤背景流）、PHT（裁剪代理握手包及其 ACK）、POT（burst 重标定） | 对齐后的 trace | 喂给现有 WF 模型（DF/BAPM/TF/NetCLR/TikTok/RF），提升未见协议泛化 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| BFT（Background Flow Tailoring） | 用流大小匹配过滤 BIH（Browser Intrinsic Hostnames，如 Firefox 的 `content-signature-2.cdn.mozilla.net`）背景流 | 加密流的流大小 + 探针得到的 BIH 大小直方图 | 剔除背景流后的 trace | 生命周期第一阶段（访问初始化）；若不先清理，BIH 会被代理层按协议特异地改变大小，成为"协议相关噪声" |
| PHT（Proxy Handshake Tailoring） | 用 n-gram 检测流首部的代理握手包序列并裁剪，再用 SEQ-ACK 分析移除被握手触发的 ACK | 加密流的方向包大小序列 + 异常窗口词典 | 去掉代理握手痕迹的流 | 第二阶段（连接建立）；同一套异常词典同时用于协议识别 |
| POT（Proxy Overhead Tailoring） | 把传输期 overhead 视为 burst 缩放效应，用高斯采样 λ 对 burst 重标定，再按 MSS 填充重建包序列、按经验 IPD 重采样时间戳、按经验 ACK 频率重插入 ACK | 加密流的 burst 序列 + 斜率比分布 N(μ, σ) | 传输期对齐后的流 | 第三阶段（内容传输）；overhead 分散在全流，无法逐包删除，只能整体缩放 |
| 协议识别（辅助组件） | flow-level n-gram 字典匹配 + session-level 多数投票 | 加密流 | 协议标签 | 前置步骤，决定 Step 5 用哪套规则 |

### 4.4 公式、算法和机制解释

- **BFT 平衡打分（Eq. 1）**：`U(α) = (1+β) · C_filt · C_re / (β·C_filt + C_re)`，其中 C_filt 为被过滤 BIH 流比例、C_re 为被保留网站流比例，β 控制"去 BIH"与"保网站流"的优先级。取每协议最大化 U(α) 的 α*；由于各协议 α* 不同、独立取值会留下不同的 BIH 残余量，再用 **共享阈值 α_opt = min{α₁*, …, αₙ*}**（本工作 α_opt = 0.4）保证跨协议背景流分布一致；给定 α_opt 后把 BIH 直方图 bin 按高度降序累加至覆盖 α_opt，其并集即过滤器。
- **PHT 的方向包大小离散化（Eq. 2）**：`Q_v(p_i) = d_i · ⌊s_i / Δ⌋`，Δ = 2r/v，d_i ∈ {+1, −1} 为方向；窗口 W_i 表示为 `Q_v(W_i) = (Q_v(p_i), …, Q_v(p_{i+k}))`。v 控制精度/召回的权衡（v 小则不同模式被混同，v 大则漏检增多）。
- **PHT 词表大小的互信息目标（Eq. 3）**：`v* = arg max J(v)`，`J(v) = I(Q_v(W); Y) − γ·log v`，Y ∈ {0,1} 表示窗口是否异常，γ 控制词表增长惩罚。Fig. 11 验证：最大化 J(v) 的 v 同时给出最好的握手包检测 F1（Table VI 中 v* 为 VMess 90 / Shadowsocks 7 / Trojan 30）。
- **POT 的 burst 缩放关系（Eq. 4）**：同一上层内容在协议 P₁/P₂ 下的 burst 大小满足 `B₁ ≈ λ^{P₁}_{P₂} · B₂`，λ 的统计量由 BSM（Byte-Segment Map，BSM(i) 返回第 i 个 HTTP 字节所在 TCP 段的流内索引）斜率比得到；裁剪时采样 λ 并按 `B_aug = λ · B_orig` 重标定，最后按 TCP MSS [35] 填包（末包承载余数）、按原流经验 IPD 分布重采样时间戳、按经验 ACK 频率 CDF 重插入 ACK（重标定前先移除 ACK，避免对小 burst 的错误缩放）。
- **POT 参数估计误差（Eq. 5）**：`e_μ(k) = |μ̂_k − μ_u| / μ_u`、`e_σ(k) = |σ̂_k − σ_u| / σ_u`，用于度量用 k 个网站估计目标高斯参数的归一化误差（Fig. 13）。

### 4.5 方法优势

- **Model-agnostic / plug-and-play**：完全在预处理阶段工作，不改模型结构、不需重训，可叠加到任意 WF 模型上（本文覆盖 6 个）。
- **攻击期零 payload 依赖**：裁剪规则只用流大小、包位置、方向包大小等加密后仍可观测的元数据。
- **探针成本低**：仅 5 个网站、5% 占比的探针流量即可完成参数估计，且参数在更低采样比下依然稳定。
- **不需要测试协议的流量**：与 Li et al. [18] 的特征选择不同，PA3 学到的协议特征与网站无关、且不要求 WF 模型接触测试协议。
- **可解释**：三处漂移分别对应访问生命周期的三个阶段，每个模块的机制（大小模式 / 握手序列 / 分段通胀）都可由 Fig. 3–7 的测量直接读出。

### 4.6 方法不足

- **依赖可解密探针流量**：要求攻击者能搭建受控客户端/服务端并记录密钥（论文用商业代理服务 + 改造 Clash Core 实现），在纯被动场景下不可得。
- **仅覆盖三个协议**：VMess / Shadowsocks / Trojan；Table I 显示 VLess、hy2、ShadowsocksR 也在商业服务中使用，但未纳入评测；探针词典之外的新协议如何回退，论文未讨论。
- **BIH 过滤存在误删网站流风险**：Fig. 4 显示大量网站流大小落在 0–30 KB，与 BIH 流重叠，需靠 β 权衡量取舍。
- **参数需随浏览器版本维护**：Fig. 12 显示 Firefox 137 起 BFT 范围因 `firefox-settings-attachments.cdn.mozilla.net` 大流而增大，作者建议每 2–3 个 Firefox 版本更新过滤范围。
- **存在一处未获胜设定**：Shadowsocks → VMess 的 TikTok 上 PA3（0.727）低于 NetRandAugment（0.750）。
- **未报告运行时/吞吐开销**：解析稿 §V 只报告 F1 与稳定性，未见裁剪阶段的时间或资源开销测量。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

- **vs 数据增强类缓解方法（NetAugment / DyWin / Rosetta / NetRandAugment）**：它们在训练集上模拟网络/传输层扰动以扩大数据多样性，属于"让模型见过更多变化"；PA3 不训练、不扩数据，而是把测试流量**确定性地对齐**回训练分布，属于"消除变化"。
- **vs 跨环境特征选择（Li et al. [18]）**：后者在特征空间中挑"对漂移稳健"的特征，依赖所选网站与测试协议样本；PA3 直接在原始流量层面学**网站无关**的协议结构，且不需访问测试协议流量。
- **vs 模型侧鲁棒性工作（TF / TikTok / NetCLR 等）**：那些工作通过改造攻击模型提升抗漂移能力；PA3 与之正交，可与其叠加（Table III 中恰好是 TF 这类漂移鲁棒模型最终取得 0.966 的最好成绩）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 首次系统性刻画代理诱导漂移的 ground truth | 用 payload-aware 探针分析揭示代理在各生命周期阶段以不同方式（背景流大小 / 握手序列 / 分段通胀）异质性地扭曲流量 | 高 | 是（任何"协议栈中间层引入失真"的场景） |
| model-agnostic 流量裁剪框架 | 三模块 BFT/PHT/POT 编译自指纹、只依赖加密后可观测元数据 | 高 | 是 |
| 低资源参数估计与共享阈值设计 | α_opt = min{α*_i} 保证跨协议背景流分布一致；MI 目标选词表大小；Gaussian 斜率比重标定 | 中 | 是 |
| 自采可复现代理流量数据集 | ~1 TB、80 网站 × 4 协议，带密钥材料随仓库发布 | 中高 | 是（填补代理流量数据集缺失） |

### 5.3 适用场景

代理协议混合/切换的真实审查环境（如用户自由切换机场节点协议）下的 WF 攻击；也适用于任何"训练与部署时中间协议栈版本/配置不一致"导致的输入分布漂移场景。需要攻击方有能力采集少量可控探针流量。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 无缓解（Baseline） | 无额外假设 | 跨协议 F1 崩塌（DF < 0.56、NetCLR 低至 0.319） | PA3 把 6 模型 × 6 协议对的 F1 全部提升（唯一例外见 §4.6） |
| NetAugment [10] | 无需协议知识，通用性强 | 只模拟网络环境变化；部分设定反而低于 baseline（BAPM 0.382→0.339） | 针对代理层失真而非网络层；不改变训练数据分布 |
| DyWin [41] | 窗口级随机增强，实现简单 | 对手握真实协议差异无针对性；BAPM/NetCLR 上常为最差 | 用协议结构指纹做确定性对齐 |
| Rosetta [29] | 模拟 TCP 层效应（聚合、丢包） | 与代理层 overhead 机制不同，收益有限（Trojan→Shadowsocks 上 DF 0.428 反低于 baseline 0.558） | 直接在 burst 尺度上按协议斜率比重标定 |
| NetRandAugment [42] | 多算子随机组合，跨设定平均最强（多次成为最优对比方法） | 仍属"随机增强"，在 TikTok 等设定被 PA3 反超仅一处例外 | 可解释的三阶段对齐 |
| PA3（本文） | 平均 +0.12 F1（相对 ~27%），最高 +0.41；低探针成本；可解释；开源 | 需探针流量；覆盖协议有限；BIH 参数需随浏览器版本维护 | — |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- 实现：>4,500 行 C 代码（payload-aware 分析工具链）+ >3,500 行 Python（漂移缓解）；用 Selenium [36] 与改造版 Clash Core [37] 自动化流量与密钥采集。
- 评测主线：固定 P_train（单协议）训练 WF 模型，在 P_test（另一协议，P_train ∩ P_test = ∅）上测试 F1，对比 4 种漂移缓解方法与 unmitigated baseline。
- 参数来源：全部裁剪参数只从 5 个网站、占完整数据集 5% 的探针流量估计，选好后固定。
- 协议识别词典：每协议用不超过 400 条流学习异常模式。

### 6.2 数据集

| 数据集 | 规模/构成 | 采集方式 | 公开性 |
|---|---|---|---|
| PA3 代理流量数据集（自采） | 约 1 TB；80 网站 × 4 协议（NoProxy、VMess、Shadowsocks、Trojan） | 商业代理服务（非实验室自建），代理服务器分布于日本、新加坡、美国；3 台客户端（两台位于中国高校校园网、一台为美国商业云 VM） | 随 PA3 仓库发布（含密钥材料），供可复现研究 |
| Firefox 版本数据集（自采） | Firefox 132（2024-10 发布）至 141（2025-07 发布）共 10 个版本，逐版本采集 | 同上游采集链路，用于分析浏览器版本对 BIH 流大小的影响 | 同上（论文称随仓库发布） |

> ⚠️ MinerU 解析问题：Table I（10 家商业代理服务商的协议使用调查）的符号图例在解析稿中丢失——caption 中三处 "indicates …" 前的符号变为空白，表中实际出现 ●/○/➀/➁ 四种符号，无法从解析稿唯一确定哪一符号对应"正在使用/曾使用/从未使用"，引用该表需回原 PDF 核对。

### 6.3 Baseline

- **WF 攻击模型（6 个，被裁剪后评测）**：DF [9]、BAPM [38]、TF [39]、NetCLR [10]、TikTok [40]、RF [27]。注意：本文的 "RF" 指 Shen et al. [27] 的鲁棒流量表征模型（非随机森林），与 Sweet Danger 讨论的 shallow RF 不是同一对象，对照 KB 时须区分。
- **漂移缓解方法（4 个）**：NetAugment [10]（burst 级 CDF 采样增强）、DyWin [41]（窗口级掩码/抖动/保留增强）、Rosetta [29]（TCP-aware 聚合与丢包模拟）、NetRandAugment [42]（多算子随机组合增强）。

> ⚠️ MinerU 解析问题：解析稿参考文献列表在 [41]（Jeon et al., Rofire, WWW 2026）条目中途截断（URL 停在 "https://doi.org"），正文引用的 [42]（NetRandAugment）未出现在参考文献列表中；引用 [41]/[42] 的出处需回原 PDF 核对。

### 6.4 评价指标

主指标为 **F1-score**；Table III 同时报告标准差（论文称"跨重复运行稳定"，但解析稿未给出重复次数或随机种子设置）。此外报告协议识别错误率（Table II，flow-level / session-level）与 POT 高斯参数估计的归一化误差（Eq. 5，Fig. 13）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| VMess→Shadowsocks（DF） | F1 | 0.774 | 0.634（NetRandAugment） | +0.140 | Table III；unmitigated baseline 仅 0.518 |
| VMess→Shadowsocks（NetCLR） | F1 | 0.743 | 0.522（NetRandAugment） | +0.221 | 对 unmitigated baseline（0.332）增益 +0.411，为全表最大单点增益，与摘要"最高 0.41 绝对增益"一致 |
| VMess→Shadowsocks（BAPM） | F1 | 0.653 | 0.382（unmitigated baseline） | +0.271 | 漂移敏感模型；NetRandAugment 反而把 BAPM 压到 0.239 |
| VMess→Trojan（DF） | F1 | 0.633 | 0.599（NetRandAugment） | +0.034 | Rosetta 在该对（0.428）低于 baseline（0.481） |
| Shadowsocks→Trojan（DF） | F1 | 0.600 | 0.496（NetAugment） | +0.104 | Table III |
| Trojan→Shadowsocks（RF） | F1 | 0.737 | 0.667（unmitigated baseline） | +0.070 | RF 在困难协议对上本身较强，四个增强 baseline 全部低于 baseline |
| Trojan→VMess（RF） | F1 | 0.636 | 0.593（unmitigated baseline） | +0.043 | 同上 |
| Trojan→Shadowsocks（NetCLR） | F1 | 0.576 | 0.539（Rosetta） | +0.037 | 该对 NetCLR baseline 0.319 |
| Shadowsocks→VMess（TikTok） | F1 | 0.727 | 0.750（NetRandAugment） | −0.023 | 全文唯一一处 PA3 未获胜的设定 |
| 协议识别（flow-level） | 错误率 | ≤0.587% | — | — | Table II：VMess 0.255%、Shadowsocks 0.587%、Trojan 0.556%；session-level 降至 0.005%/0.000%/0.059% |
| 汇总（6 模型 × 6 协议对） | F1 | 平均 +0.12（相对 ~27%） | — | 最高 +0.41 | Abstract；笔者按 Table III 全部 36 个单元对 unmitigated baseline 求差复算得均值 +0.117，与摘要一致 |

### 6.6 优势最明显的场景

- **漂移敏感模型**：DF、BAPM、NetCLR 的增益最大（如 BAPM VMess→Shadowsocks 0.382→0.653、NetCLR 同对 0.332→0.743），说明收益主要来自"消除协议特有噪声"而非"通用增强"。
- **困难协议对**：跨 VMess/Shadowsocks 的组合（两者握手与分段差异最大）增益高于含 Trojan 的组合。
- **最好情形**：TF 在 VMess→Shadowsocks 上达到 0.966，与摘要"最好情形 F1 > 0.96"对应。
- **参数鲁棒**：把探针采样比从 20% 降到 5%，α* 完全不变（Table V，max Δα* = 0.00）；训练/测试样本比从 25% 降到 5%，v* 不变且 F1 ≥ 0.973（Table VI）；POT 高斯参数估计误差中位数 < 0.2（Fig. 13，k=5 网站）。

### 6.7 局限性

1. 依赖可解密探针流量（受控环境 + 商业代理服务），纯被动攻击场景不适用。
2. 只覆盖 VMess/Shadowsocks/Trojan，未评测 VLess/hy2/ShadowsocksR（Table I 中均有部署）。
3. 假定目标协议已知/可识别；对探测词典之外的新协议（或协议混淆变体）如何回退未讨论。
4. BFT 过滤区间与浏览器版本绑定，Firefox 137+ 需重估；BIH 与网站流大小重叠导致存在误删风险。
5. 存在一个反例设定（Shadowsocks→VMess 的 TikTok）；论文未分析其原因。
6. 未报告裁剪的运行时开销；也未评测"防御方察觉裁剪痕迹"的对抗场景。
7. 评测规模：80 网站（协议识别统计样本较大，但 WF 分类任务的类别数未在解析稿中明确说明来源划分）。

---

## 7. 学习与应用

### 7.1 是否开源？

是。论文 §I 末句给出：**源码与全部数据集** `https://github.com/wesly2000/PA3`；数据集带密钥材料一并发布（"we collect our proxied traffic dataset with the corresponding key materials … which is released along with the PA3 repository"）。

### 7.2 复现关键步骤

1. 搭建受控客户端（Selenium 自动化 + 改造版 Clash Core），为 VMess/Shadowsocks/Trojan 各采集少量探针流量并记录密钥材料（论文设定：5 个网站、约 5% 数据量）。
2. 对同 hostname 跨协议做 payload-aware 比较，得到三类结构量：BIH 流大小直方图、TLS Client/Server Hello 的流内包索引分布、BSM 斜率比分布。
3. 编译规则：按 U(α) 与 β=5 选各协议 α* 并取 α_opt = min（本文 0.4）；按 J(v) 选每协议 n-gram 词表大小 v*；估计 POT 的高斯参数 μ/σ。
4. 攻击期：先 n-gram 词典匹配 + 会话级多数投票识别协议，再依次执行 BFT（大小过滤）→ PHT（握手序列裁剪 + ACK 移除）→ POT（burst 重标定 + MSS 填包 + IPD 重采样 + ACK 重插入）。
5. 把裁剪后的 trace 直接喂给现有 WF 模型（不改结构、不重训），按 F1 对比 unmitigated baseline 与 4 种增强方法。

### 7.3 关键超参数、预处理和训练细节

| 参数 | 取值 | 来源 |
|---|---|---|
| β（BFT 打分权衡） | 5（偏向保留网站流） | §V-C |
| α*（每协议覆盖阈值） | VMess 0.5 / Shadowsocks 0.5 / Trojan 0.4 | §V-C Fig. 10 |
| α_opt（共享过滤阈值） | 0.4（= min{α*}） | §V-C |
| v*（n-gram 词表大小） | VMess 90 / Shadowsocks 7 / Trojan 30 | §V-E Table VI |
| POT 高斯参数（P_train = VMess） | Shadowsocks：μ=1.17, σ=0.15；Trojan：μ=0.98, σ=0.12 | §V-C |
| 探针规模 | 5 个网站、占完整数据集 5%；协议识别用每协议 ≤400 条流 | §V-C, §V-B |
| γ（词表惩罚系数） | 解析稿未给出具体取值 | — |

### 7.4 能否迁移到其他任务？

- **输入分布漂移的通用范式**：任何"训练/部署中间层不一致"导致漂移的分类任务（时间漂移、环境漂移、协议版本升级）都可复用"少量可控探针建立 ground truth → 编译成只依赖可观测元数据的对齐规则"的两阶段结构。
- **协议/隧道识别**：PHT 的 n-gram 异常词典与多数投票机制本身就是一个高精度代理协议/隧道分类器（flow-level ≤0.6% 错误），可直接迁移到 [[tunnel-detection]] 类任务。
- **粒度选择技巧**：用互信息目标 J(v) = I(Q_v(W); Y) − γ log v 选择离散化粒度，可迁移到任意"分桶/词表大小"决策（如 tokenization 粒度）。
- **反向启发（推断）**：若防御方知道攻击方依赖 BIH/handshake/BSM 三类指纹，可针对性地扰动这三处（例如伪装 BIH 大小模式或改变握手排布）；论文未讨论此对抗场景，属笔者推断。

### 7.5 对我的研究有什么启发？

1. **"不改模型"是一种高性价比定位**：PA3 把全部创新放在预处理层，因此能在 6 个不同架构上统一验证，说服力强且工程可插拔——做鲁棒性/泛化类研究时，先问"能否在输入侧解决"。
2. **把痛点拆到生命周期阶段**：三模块对应访问的初始化/握手/传输三阶段，每个模块都由独立测量（Fig. 3–7）支撑，这种"测量 → 指纹 → 规则"的写法值得借鉴。
3. **与 KB 中同题工作的关系**：与 [[2026-NDSS-Enhancing_Website_Fingerprinting_Attacks_against_Traffic_Drift]]、[[2025-INFOCOM-Cross-Environmental_Website_Fingerprinting]] 同属"攻击侧抗漂移"支线；与 [[2026-arXiv-ResAware__Cross-Environment_Website_Fingerprinting_via_Resource-Privileged_Distillation]] 共享"训练/探针期特权信息 + 部署期无模型改动"的思路（ResAware 蒸馏进模型，PA3 编译成显式规则）。
4. **代理环境是 WF 的现实默认**：[[2024-TON-Website_Fingerprinting_on_Encrypted_Proxies__A_Flow-Context-Aware_Approach_and_Countermeasures]] 之后，PA3 把"代理协议多样性"这一维度正式引入评测协议；后续跨环境评测应显式声明协议集合是否重叠。
5. **可复用的开源资产**：1 TB 带密钥的代理流量数据集对做流量对齐/协议指纹的研究价值高于模型本身，值得纳入 [[dataset-comparison-table]]。

---

## 8. 总结

### 8.1 核心思想

> 用探针流量提取协议指纹，做输入侧流量对齐。

### 8.2 速记版 Pipeline

1. 受控环境采集每协议少量可解密探针流量（5 网站、5% 数据量），记录密钥。
2. 对同 hostname 跨协议做 payload-aware 比较，提取三类结构指纹：BIH 流大小模式、代理握手 n-gram 序列、BSM 斜率比。
3. 编译成 payload-agnostic 规则：BFT 过滤区间（α_opt=0.4）、PHT 异常窗口词典（v*）、POT 的 λ~N(μ,σ)。
4. 攻击期先协议识别（多数投票），再依次 BFT → PHT → POT 裁剪加密流量。
5. 裁剪后的 trace 直接喂给任意 WF 模型：6 模型 × 6 协议对 F1 平均 +0.12、最高 +0.41，最好 0.966。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]]
- [[encrypted-traffic-analysis]]
- [[censorship-circumvention]]（代理协议是审查规避的实际载体，本文以此为威胁模型前提）
- [[tunnel-detection]]（PHT 的 n-gram 异常词典同时充当代理协议/隧道识别器，flow-level 错误率 ≤0.6%）

### 9.2 相关方法

- 本文方法为 model-agnostic 预处理/流量整形框架，不属于白名单中的方法页（故 frontmatter `method` 为空）；评测涉及的代表性模型族可参考 [[convolutional-network]]（DF 等以包方向-长度序列为输入的经典 WF 攻击）与 [[contrastive-learning]]（NetCLR 的对比式表征）

### 9.3 相关任务

- [[website-fingerprinting]]

### 9.4 可更新的综述页面

- [[survey-website-fingerprinting]]（新增"代理协议多样性/跨协议泛化"评测维度与 6 模型 × 6 协议对结果矩阵）
- [[survey-encrypted-traffic-analysis]]（代理层失真作为一类输入分布漂移的测量与对齐方法）

### 9.5 可加入的对比表

- [[method-comparison-table]]（WF 跨协议漂移缓解方法对照：NetAugment/DyWin/Rosetta/NetRandAugment/PA3）
- [[dataset-comparison-table]]（自采 ~1 TB 代理流量数据集：80 网站 × 4 协议 × 多地区，带密钥发布）
- [[open-source-registry]]（代码 + 数据集：https://github.com/wesly2000/PA3）
- [[motivation-pattern-comparison]]（"指出被默认的隐含假设 → 系统测量其代价 → 在输入侧消除"的动机模板）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 漂移源于代理层为加密/协议通信插入的额外字节，且按流独立引入 | 正文动机段；"the drift is introduced at the flow level, while a website trace is only a mixture of multiple concurrent flows" | §I |
| 协议一致性假设下 F1 > 0.94，未见协议下崩塌（DF < 0.56） | Fig. 9 对角/非对角对比 | §V-B |
| 攻击期仅用元数据即可高精度识别代理协议 | VMess/Shadowsocks/Trojan flow-level 错误率 0.255%/0.587%/0.556%，session-level 0.005%/0.000%/0.059% | §V-B Table II |
| PA3 在几乎所有 (模型 × 协议对) 上最优，仅一处例外 | "with only one exception for TikTok"；Table III 中 Shadowsocks→VMess 的 TikTok 0.727 < NetRandAugment 0.750 | §V-B Table III |
| 最大单点增益 +0.411 | NetCLR VMess→Shadowsocks 0.332 → 0.743 | §V-B Table III |
| 平均 +0.12（相对 ~27%），最好 0.96+ | Abstract；TF VMess→Shadowsocks 0.966；按 Table III 36 单元复算均值 +0.117 | Abstract, §V-B |
| 三模块互补、共同处理三阶段漂移 | Table IV：w/o BFT、w/o PHT、w/o POT 均优于 baseline，完整 PA3 在 6 组协议对全部最优 | §V-D Table IV |
| BFT 参数在低采样比下稳定 | 采样比 20%→5%：α* 不变（0.50/0.50/0.40），max Δα* = 0.00 | §V-E Table V |
| PHT 词表大小在低数据量下稳定 | 训练比 25%→5%：v* 不变，最优 F1 ≥ 0.973（VMess 0.973–0.976、Shadowsocks 0.977–0.980、Trojan 0.980–0.983） | §V-E Table VI |
| POT 参数可由极少网站估计 | Fig. 13：k 下降时中位误差 <0.2；Table III 结果只用 k=5 个探针网站 | §V-C, §V-E Eq. 5 |
| BIH 过滤范围随 Firefox 版本漂移，需周期性维护 | Fig. 12：136 版稳定，137 起因 firefox-settings-attachments.cdn.mozilla.net 增大；建议每 2–3 版本更新 | §V-E |
| 代码与数据集开源 | "The source code of PA3 and all the datasets are available at https://github.com/wesly2000/PA3" | §I |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-arXiv-Mitigating_Proxy-Induced_Traffic_Drift_in_Website_Fingerprinting_via_Model-Agnostic_Traffic_Tailoring.pdf
- MinerU Markdown：02-parsed-markdown/2026-arXiv-Mitigating_Proxy-Induced_Traffic_Drift_in_Website_Fingerprinting_via_Model-Agnostic_Traffic_Tailoring.md

---

## 12. 后续问题

- 论文的 "RF" 指 Shen et al. 的鲁棒表征模型，若与 random forest 类浅层基线混用会误读 Table III，KB 聚合时如何统一标注命名冲突？
- 三个模块的 F1 增益是否可分解（每模块单独贡献多少）？Table IV 只给"去掉一个"的结果，缺少逐模块单独启用的对照。
- 裁剪后的流量是否仍保留可用于其他任务的信息（例如协议识别、流量分类）？论文只评测 WF。
- 防御方能否检测到流量被 PA3 裁剪过（例如 BIH 缺失、握手序列异常）？这会影响攻击在真实部署中的隐蔽性，论文未讨论。
- 对不在探针词典中的新协议（或同协议不同实现/版本的握手差异）如何处理？是否需要在线更新词典？
- 未报告运行时开销；~1 TB 数据集的实际训练/裁剪吞吐与实时可行性需要复现验证。
- pot 的 λ 高斯建模假设是否覆盖多协议混合访问（一个会话内多协议并发）的情况？威胁模型只讨论单协议会话。

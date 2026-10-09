---
type: paper
title_original: "CipherSight: Robust Website Fingerprinting via Record-Resource Semantic Supervision under Distribution Shifts"
title_cn: "CipherSight：基于 TLS 记录-资源语义监督的分布偏移下鲁棒网站指纹"
authors: ["Runhan Song", "Qiqi Liu", "Chuanzhou Pan", "Zhenquan Ding", "Youquan Xian", "Chongru Fan", "Lei Cui", "Wei Wang", "Zhiyu Hao"]
year: 2026
venue: "arXiv 2026"
doi: unknown
url: "https://arxiv.org/abs/2608.13905"
pdf: "00-inbox/PDFs/2026-arXiv-CipherSight__Robust_Website_Fingerprinting_via_Record-Resource_Semantic_Supervision_under_Distribution_Shifts.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-CipherSight__Robust_Website_Fingerprinting_via_Record-Resource_Semantic_Supervision_under_Distribution_Shifts.md"
status: processed
reading_level: L2
research_area: ["website-fingerprinting", "encrypted-traffic-analysis", "traffic-representation-learning"]
task: ["website-fingerprinting"]
method: ["transformer", "pre-training-finetuning", "self-supervised-learning"]
dataset: ["us0304", "us0320", "us0409", "fr0409", "sg0409"]
code: unknown
relevance: high
created: "2026-09-19"
updated: "2026-09-19"
---

# CipherSight: Robust Website Fingerprinting via Record-Resource Semantic Supervision under Distribution Shifts

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | CipherSight: Robust Website Fingerprinting via Record-Resource Semantic Supervision under Distribution Shifts |
| 中文标题 | CipherSight：基于 TLS 记录-资源语义监督的分布偏移下鲁棒网站指纹 |
| 作者 | Runhan Song, Qiqi Liu, Chuanzhou Pan, Zhenquan Ding, Youquan Xian, Chongru Fan, Lei Cui, Wei Wang, Zhiyu Hao（哈尔滨工业大学计算学部；中关村实验室；中国科学院大学；北京邮电大学网络空间安全学院；通讯作者 Lei Cui / Wei Wang） |
| 年份 | 2026 |
| 会议/期刊 | arXiv preprint 2026（解析稿未见 arXiv 边栏编号，编号 2608.13905 来自批次分配） |
| 研究方向 | HTTPS 网站指纹（WF）、TLS 记录级流量表示学习、分布偏移（时间/地理漂移、开世界） |
| 任务类型 | 闭世界分类（2,008 类）、时间漂移、地理漂移、开世界未知站点拒识 |
| 方法关键词 | TLS-record tokenization（类别 embedding + 对数分桶 embedding）、L1 流内 block-diagonal attention、L2 流间 full attention ([PCLS])、MRM 掩码记录建模、记录-资源监督 P1（L_seg/L_attr/L_cnt + aligned-record pooling）、LoRA 微调、特权语义教师 P2（L_feat/L_logit 蒸馏） |
| 数据集 | 自采六套 HTTPS 集合：us0304、us0320（16 天后）、us0409、fr0409、sg0409；2008 类；开世界额外 213,099 条 traces（解析稿未给数据集正式名称） |
| 是否开源 | unknown（解析稿未提及代码/数据发布） |
| PDF | 00-inbox/PDFs/2026-arXiv-CipherSight__Robust_Website_Fingerprinting_via_Record-Resource_Semantic_Supervision_under_Distribution_Shifts.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-arXiv-CipherSight__Robust_Website_Fingerprinting_via_Record-Resource_Semantic_Supervision_under_Distribution_Shifts.md |

> ⚠️ MinerU 解析问题：本解析稿 small-caps 排版碎片化极严重（如 `Ci<sub>p</sub>h<sub>er</sub>Si<sub>g</sub>ht`、`u<sub>n</sub>d<sub>er</sub>`、`T<sub>a</sub>bl<sub>e</sub>`），且 fi/ff/ffi 连字丢失（traffic→`trafic`、effective→`efective`、differences→`diferences`、sufficient→`suficient`）。本文引用数值均已还原为正常词汇，引用原句时需注意还原。

---

## 1. 一句话总结

> 用 TLS 记录级表示 + 流内/流间分层注意力 + 训练期资源语义特权监督，实现时间与地理漂移下仍 >90% 的 HTTPS 网站指纹。

---

## 2. 摘要翻译

### 2.1 摘要原文

> HTTPS website fingerprinting (WF) aims to identify visited websites from metadata observable in encrypted traffic. However, real-world deployments introduce a significant out-of-distribution (OOD) problem caused by temporal and geographic changes, while previously unseen websites are common in open-world scenarios. Existing methods primarily learn from raw TCP packet sequences and struggle to capture stable and generalizable website representations, resulting in performance degradation under practical conditions.
>
> We propose CipherSight, a TLS-record-based hierarchical framework for robust HTTPS WF. Unlike existing approaches that rely on TCP packet sequences and are sensitive to transport-layer artifacts, CipherSight learns website representations from TLS records by jointly encoding multiple record-level attributes. It introduces a hierarchical architecture that captures both intra-flow dependencies among TLS records and inter-flow interactions across concurrent flows, enabling the model to exploit structural patterns in HTTPS traffic. Besides, to learn robust representations, CipherSight employs a masked record modeling (MRM) task to capture contextual traffic semantics and leverages fine-grained record-resource annotations as privileged supervision through structure-aware objectives and semantic distillation. Experiments show that CipherSight achieves 95.41% accuracy across more than 2,000 website classes in the closed-world setting and maintains over 90% accuracy under both temporal and geographic drift, consistently outperforming all evaluated baselines.

### 2.2 摘要中文翻译

> HTTPS 网站指纹（WF）旨在从加密流量中可观测的元数据识别用户访问的网站。然而真实部署带来由时间与地理变化引起的显著分布外（OOD）问题，同时开世界场景中未见网站十分常见。既有方法主要从原始 TCP 包序列学习，难以获得稳定且可泛化的网站表示，导致实际条件下性能退化。
>
> 本文提出 CipherSight，一个面向鲁棒 HTTPS WF 的、基于 TLS 记录的分层框架。与依赖 TCP 包序列、对传输层伪影敏感的既有方法不同，CipherSight 通过联合编码多种记录级属性，从 TLS 记录中学习网站表示。它引入分层架构，同时刻画 TLS 记录之间的流内依赖与并发流之间的流间交互，使模型能够利用 HTTPS 流量中的结构模式。此外，为学到鲁棒表示，CipherSight 采用掩码记录建模（MRM）任务捕捉上下文流量语义，并通过结构感知目标与语义蒸馏，把细粒度记录-资源标注作为特权监督加以利用。实验表明，CipherSight 在闭世界设定下于 2,000 多个网站类别上达到 95.41% 准确率，在时间漂移与地理漂移下均保持 90% 以上准确率，一致优于所有被评测的 baseline。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

论文把 HTTPS WF 的真实部署困难归为三类挑战（§Challenges），并据此设计表示层、架构层、监督层三处改动：包级表示对传输层可变性过敏感；现代网页加载是多条并发流，Tor 式"压平成单一序列"丢失多流结构；加密造成"可观测流量模式 ↔ 网页资源组成"之间的语义鸿沟，仅用网站级标签训练无法利用资源级信息。

### 3.2 现有方法的痛点和不足

- 包级表示不稳定：TCP 分段、重传与动态网络条件使同一网页资源被映射为差异很大的 TCP 包序列。论文自测 **超过 80% 的 TCP 包序列在重复抓取之间不一致**（§Challenges）。
- 扁平化表示忽略多流结构：DF/VarCNN/TikTok 等 Tor-oriented 方法把一条 trace 压平成单一包序列，"implicitly overlooking the inherent multi-flow structure of HTTPS traffic"（§Related Work / §Challenges）。
- HTTPS-native 方法（H&W、STC-WF、CTX-Aware）虽引入更高层结构，但"没有在统一层级中联合编码多种 TLS 记录属性与显式流内/流间依赖"（§Website Fingerprinting over HTTPS）。
- 加密造成的语义鸿沟：资源级属性（类型、大小、请求语义）更直接刻画网页组成，但加密 trace 只暴露其间接表征；仅用网站级标签会浪费记录与资源语义之间的对应关系（§Challenges 第三点）。
- 分布偏移与开世界：现有鲁棒性研究多聚焦 Tor 或单一失配来源，论文同时评测时间漂移、地理漂移与开世界（§Website Fingerprinting under Distribution Shifts）。

### 3.3 论文的研究假设或核心直觉

把建模单元从 TCP 包提升到 TLS 记录，可以让表示对传输层抖动解耦；在统一层级里分别建模流内依赖（block-diagonal 注意力）与流间交互（全注意力 + [PCLS]），可以保留多流结构；再把训练期才可得的"记录 ↔ 网页资源"对齐信息作为特权监督（LUPI 范式），可以让加密侧表示吸收资源级语义，从而在分布偏移下更稳。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 重复抓取中 >80% 的 TCP 包序列不一致；TLS 记录边界在不解密时也可恢复 | §Challenges（自测） |
| 痛点提炼 | 包级表示引入噪声，闭世界高分不能转化为真实部署（漂移）下的可靠性 | §Introduction、§Website Fingerprinting under Distribution Shifts |
| 问题转化 | 转化为 OOD 泛化问题：时间漂移、地理漂移、开世界拒识三类设定下的鲁棒表示学习 | §Introduction、§Evaluation |
| 文献定位 | 既有工作分别做了高层 HTTPS 特征（H&W/ADU/STC-WF/CTX-Aware）或语义对齐（STAR、ResAware、More Than Meets the Eye），但未在统一层级联合编码记录属性与流内/流间依赖 | §Related Work（被部分解决） |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | TLS 记录级表示 + 分层（流内/流间）编码 + 训练期资源语义特权监督，能在分布偏移下取得比包级 baseline 更小的退化 | §Challenges / §Method | 闭世界、时移、地理漂移、开世界四组实验 |
| 辅助假设 | 特权监督的收益在漂移场景（尤其地理漂移）比在闭世界更大 | §Pretraining with Record-Resource Supervision（引 Fan et al. 2026） | 消融（Table 4） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | 闭世界 95.41%（VarCNN 92.16%）；时移 92.99%（H&W 79.96%）；地理漂移 91.09%/90.59%（ARES 79.53%、RF 82.07%） | §Closed-World / §Temporal Drift / §Geographic Drift，Table 1–3 |
| 辅助假设 | 支撑 | 消融：地理漂移下 Full Priv. 增益 1.37/1.55 pp，时移下 0.30/0.65 pp（且 P1 预训练贡献了时移下大部分增益） | §Ablation，Table 4 |

---

## 4. 方法设计

### 4.1 方法整体流程

CipherSight 分三段：(1) 表示构建——把 PCAP 重建为 TCP 流，再提取密文可观测的 TLS 记录属性并 tokenize；(2) 分层编码——L1 用 block-diagonal 掩码在每个流内做自注意力得到记录表示 h_{i,j} 与流摘要 u_i，L2 用全注意力在 [PCLS] + 流摘要上做流间聚合得到页面表示 h_s；(3) 两阶段训练——预训练用 MRM + 记录-资源监督 P1（Eq. 2），LoRA 微调时继续 P1 并引入特权语义教师 P2 做特征/逻辑蒸馏（Eq. 3–4）。推理时只保留 TLS 记录元数据、L1/L2 编码器与分类器，MRM/P1/P2 与全部资源标注被移除。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | 网页访问 PCAP + SSL key log | 重建 TCP 流，从密文可观测的 TLS 记录提取方向、长度、外层 content type、时序、所属流；仅用 key log 做数据集标注（恢复记录-资源对齐与资源属性） | 每条流的 TLS 记录序列 | 把建模单元从包提升到记录，降低对 TCP 分段/重传的敏感度 |
| Step 2 | 记录属性 | 类别特征→可学习 embedding；数值特征→对数分桶 embedding + log 值线性投影，求和归一化；每流前插 [FCLS] | 记录 token 序列 (FCLS_i, e_{i,1}, …, e_{i,n_i}) | 统一异构记录属性的表示 |
| Step 3 | 拼接后的多条流 token | L1 施加 block-diagonal 注意力偏置（Eq. 1），位置编码在每流内重置 | 记录上下文表示 h_{i,j}、流摘要 u_i | 以流为局部上下文边界，避免跨连接直接依赖 |
| Step 4 | (PCLS, u_1, …, u_m) | L2 施加全自注意力；[PCLS] 终态为页面表示 h_s；线性层 + GELU + dropout + 类别投影 | 网站 logits o_s | 建模并发流之间的网页级交互 |
| Step 5 | 无标注记录序列 | 预训练：MRM（随机掩码整条记录 embedding，重建方向/长度桶/外层 content type，三项交叉熵之和）+ P1（Eq. 2） | 预训练 tokenizer 与 L1 | 学到上下文语义 + 与网页资源结构的对应 |
| Step 6 | 标注 trace | 冻结骨干，向所有 L1/L2 注意力层的 q,k,v,o 注入 LoRA（W̃ = W + (α/r)BA）；LoRA 矩阵、学生分类器、P1 头、语义教师可训练；目标 L_ft（Eq. 4） | 微调后的学生模型 | 在保留预训练表示的同时适配分类任务 |
| Step 7 | 测试 trace（仅密文可观测记录元数据） | 只用 TLS 记录元数据 + L1/L2 + 网站分类器 | 网站预测 | 部署时不需要 key log / 资源标注 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| TLS-record tokenizer | 类别 embedding + 对数分桶 embedding 融合多种记录属性 | 记录方向/长度/外层 content type/时序等 | 记录 token e_{i,j} | 被 L1 消费；预训练阶段被直接优化 |
| L1 流内编码器 | block-diagonal 掩码的自注意力（Eq. 1：同流内位置可见，其余 −∞） | 每流 token 序列（含 [FCLS]） | h_{i,j}（记录级）、u_i（流摘要） | 向 L2 只暴露流摘要，防止跨连接 all-to-all 混合 |
| L2 流间编码器 | 全自注意力聚合 (PCLS, u_1..u_m) | 流摘要序列 | 页面表示 h_s | 微调阶段才引入 |
| MRM 头 | 重建被掩码记录的方向、长度桶、外层 content type | L1 输出 | L_MRM（三项 CE 之和） | 仅预训练使用 |
| P1 头（H_rec / H_res） | 记录级：begin/inside 标签 + inner MIME 类型（仅对齐记录计入损失）；资源级：对齐记录状态均值池化后预测响应属性与记录数 | L1 输出 + 保留的对齐 span {I_q} | L_seg、L_attr、L_cnt | 预训练与微调均使用（Algorithm 1） |
| 特权语义教师 P2 | 资源 token → 资源语义编码器得 h_r，与 stop-gradient 的学生特征 h_s 融合得 h_t，MLP 出教师 logits o_t | 资源语义特征 + 学生特征 | L_feat = MSE(h̄_s, sg[h̄_t])、L_logit = T²·KL(sg[p_t] ‖ p_s) | 仅微调使用；推理时丢弃 |
| 学生网站分类器 | 线性 + GELU + dropout + 类别投影 | h_s | o_s 与 L_cls^S | 推理时唯一保留的预测头 |

### 4.4 公式、算法和机制解释

- **式 (1) L1 注意力偏置**：M_pq^(1) = 0 当 φ(p)=φ(q) 且 p,q 有效，否则 −∞（φ(p) 为 token 位置 p 所属流）。即 block-diagonal 掩码，把每个 TLS 流当作局部上下文边界。
- **式 (2) 预训练目标**：L_P1 = λ_seg·L_seg + λ_attr·L_attr + λ_cnt·L_cnt；L_pre = λ_MRM·L_MRM + L_P1。
- **Algorithm 1（记录-资源监督与对齐记录池化）**：先算对齐位置上的 L_seg；对每个有非空保留 span I_q 的资源 q，取 g_q = |I_q|^{-1}·Σ_{(i,j)∈I_q} h_{i,j}，并把 (y_q^len, y_q^mime, log(1+|I_q|)) 组成资源级目标；H_res 预测出 (ŷ^len, ŷ^mime, ĉ) 后计算 L_attr 与 L_cnt。
- **式 (3) 蒸馏损失**：L_feat = MSE(h̄_s, sg[h̄_t])，L_logit = T²·KL(sg[p_t] ‖ p_s)；其中 h̄_x = N(h_x) 为 L2 归一化、p_x = softmax(o_x/T)，sg 表示停止梯度。
- **式 (4) 微调目标**：L_ft = λ_cls·L_cls^S + λ_struct·(L_seg + L_attr + L_cnt) + L_cls^T + λ_logit·L_logit + λ_feat·L_feat；L_cls^S 与 L_cls^T 分别为学生/教师的网站标签交叉熵。

### 4.5 方法优势

- 建模单元与传输层解耦：TLS 记录边界在 TCP 重组后即可恢复（不需解密），一条记录可跨多个 TCP 段、一段也可含多条记录，因此比包级表示更稳定。
- 分层注意力把"流内依赖"与"流间交互"分开，既避免跨连接全连接混合（all-to-all mixing），又保留网页级信息聚合；L2 仅消费流摘要，接口成本低。
- 特权监督只作用于训练期：推理仅需密文可观测记录元数据，零额外部署开销。
- LoRA 适配冻结骨干，限制对预训练表示的破坏（论文表述：允许 L2 学网页级聚合，同时限制对预训练表示的改动）。

### 4.6 方法不足

- 构建 P1/P2 监督需要 SSL key log 做标注，限制其只能用于可解密的自采数据（§Limitations 明确承认；推理仍为 ciphertext-only）。
- 论文未报告参数规模、训练成本细节、λ 权重与 LoRA 的 r/α 取值（解析稿未提及），复现信息不完整。
- 未评测更长周期漂移、更多客户端、HTTP/3（§Limitations 自述）。
- 闭世界增益主要体现在 top-1（相对 VarCNN +3.25 pp），top-5 只提升 0.44 pp，说明其优势在"第一选择判别"而非候选集召回（§Closed-World Evaluation）。
- 表示层的收益依赖采集侧能稳定提取 TLS 记录属性；对 ECH/TLS 1.3 之外的封装（如作为代理内层）未做讨论。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

与 Tor-oriented 扁平包序列方法（[[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]] 的 DF、VarCNN、TikTok）相比，本文换掉了建模单元（包→TLS 记录）并显式分层建模多流；与 HTTPS-native 方法相比，[[2025-WWW-HOLMES&WATSON__A_Robust_and_Lightweight_HTTPS_Website_Fingerprinting_through_HTTP_Version_Parallelism]] 只利用 HTTP 版本并行性这一应用层信号、[[2024-TIFS-Inter-Flow_Spatio-Temporal_Correlation_Analysis_Based_Website_Fingerprinting_Using_Graph_Neural_Network]]（STC-WF）用图神经网络建模流间时空相关、[[2024-TON-Website_Fingerprinting_on_Encrypted_Proxies__A_Flow-Context-Aware_Approach_and_Countermeasures]]（CTX-Aware）面向加密代理的流上下文，均未在统一层级中联合编码多种记录属性；与语义路线相比，[[2025-INFOCOM-STAR__Semantic-Traffic_Alignment_and_Retrieval_for_Zero-Shot_HTTPS_Website_Fingerprinting]]（STAR 用爬取期语义画像做零样本检索）与 [[2026-arXiv-ResAware__Cross-Environment_Website_Fingerprinting_via_Resource-Privileged_Distillation]]、[[2026-arXiv-More_Than_Meets_the_Eye__A_Semantics-Aware_Traffic_Augmentation_Framework_for_Generalizable_Website_Fingerprinting]] 的资源语义蒸馏最接近，区别在于 CipherSight 把"TLS 记录与资源 span 的细粒度对齐"本身当作特权信息，同时叠加记录级与资源级监督（LUPI，引 Vapnik & Vashist 2009）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 结构保持的记录级表示 | 用 TLS 记录而非 TCP 包作为单元，联合编码记录方向/长度/外层 content type/时序等属性 | 高 | 是（任何加密协议只要有协议数据单元边界） |
| 分层流内/流间注意力 | L1 block-diagonal（Eq. 1）+ L2 在流摘要上全注意力（[PCLS]） | 高 | 是（多流聚合类任务通用范式） |
| 记录-资源特权监督 P1 | 记录级 begin/inside + inner MIME、资源级响应属性 + 记录数，配 aligned-record pooling（Algorithm 1） | 高 | 是（需可解密的标注数据） |
| 特权语义教师 P2 + LoRA | 教师融合资源语义与学生特征，用特征/逻辑蒸馏在微调期传递资源知识 | 中 | 是（LUPI 蒸馏框架通用） |
| 多场景 HTTPS WF 评测 | 闭世界 2,008 类 + 16 天时移 + 同日跨洲地理漂移 + 开世界 213,099 条未知站点 traces | 中 | 是（评测协议可复用） |

### 5.3 适用场景

需要长期、跨地域部署的 HTTPS 明文侧 WF 监测（企业/运营商侧流量审计）；多流并发、含 CDN 与第三方域的现代网页；目标是闭世界高精度判别 + 漂移下稳定性，而非资源受限的边缘部署（8 GPU 训练、未报告推理成本）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| DF / VarCNN / TikTok（Tor-oriented 扁平包序列） | Tor 场景成熟、闭世界表现强（VarCNN 92.16%） | 依赖 TCP 分段/重传等传输层伪影；不建模多流结构；漂移下退化大（VarCNN 时移 −24.35 pp） | 改用 TLS 记录级单元 + 分层流内/流间建模 |
| H&W（HTTPS-native，HTTP 版本并行） | 轻量；时移下最强 baseline（79.96%） | 只用单一应用层信号（HTTP 版本并行/资源数量） | 联合编码多种记录属性 + 资源语义监督 |
| STC-WF（流间时空图） | 显式建模流间关系 | 训练随机性大（seed 52 时闭世界仅 84.78%，而同协议源域 holdout 可达 92.25%） | 用流摘要做 L2 接口，避免跨连接全连接混合 |
| CTX-Aware（加密代理流上下文） | 面向真实代理场景设计 | 完整配置需 >128 GB 内存，本文适配下仅 8.18% | 记录级表示在同等内存预算下可扩展（本文 95.41%） |
| CipherSight（本文） | 闭世界与时移/地理漂移一致最优；推理 ciphertext-only | 需 key log 做训练标注；超参与复现信息不完整 | — |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

六套自采 HTTPS 集合（四个日期、三个地区）。闭世界用 us0304 的 8:2 切分；时移用 us0304 的 80% 训练、us0320（16 天后采集）测试；地理漂移用 us0409 的 80% 训练、同日 fr0409/sg0409 测试，并用 us0409 的 20% holdout 度量退化。开世界复用闭世界切分并追加 213,099 条来自不相交站点的 traces。实现：PyTorch、8 张 NVIDIA GPU、BF16；两个阶段各 20,000 steps；CipherSight 取最终 20,000-step checkpoint，随机种子 42–46，baseline 用 seed 42。Neural baseline 训练 100 epochs（STC-WF 300）；为"偏向 baseline"，闭世界按峰值测试精度选 checkpoint，漂移实验按源域 20% holdout 选 checkpoint 后再在完整目标集上评测。

### 6.2 数据集

| 集合 | 用途 | 规模/切分 | 类别数 |
|---|---|---|---|
| us0304 | 闭世界训练/测试（8:2） | 64,386 训练 / 15,848 测试 traces | 2,008 |
| us0320 | 时间漂移目标域（16 天后采集） | 训练用 us0304 的 80% | 1,976 共享类 |
| us0409 | 地理漂移源域（含 20% holdout） | 训练用 80% | 1,936 共享类（与 fr0409/sg0409） |
| fr0409 / sg0409 | 地理漂移目标域（同日、法国/新加坡） | 目标域全集测试 | 1,936 共享类 |
| 开世界集合 | 未知站点拒识 | 闭世界切分 + 213,099 条不相交站点 traces | — |

> ⚠️ MinerU 解析问题：表格合并单元格表头在解析稿中丢失（如 Table 3 的 Singapore / France 两级分组表头被压平为单行），Table 3 中 TF 的 Top-5 列记为 "-"（原文可能未报告该指标）。

### 6.3 Baseline

Tor-oriented：AWF（Rimmer 2018）、DF（[[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]]）、VarCNN（Bhat 2019）、TikTok（Rahman 2020）、TF（Sirinam 2019 Triple）、RF（[[2023-USENIX-Subverting_Website_Fingerprinting_Defenses_with_Robust_Traffic_Representation]]）、ARES（[[2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild]]）。HTTPS-native：H&W、STC-WF、CTX-Aware。Tor baseline 使用 5,000 包序列（截断或补零，含方向/长度/时序），缺失的预处理或开世界评测按原文定义实现且不改模型架构。

### 6.4 评价指标

top-1 accuracy、macro-F1、top-5 accuracy（baseline 支持时）；开世界置信度为 maximum softmax probability（MSP），报告 AUROC、AUPR（监控类为正类）与 OSCR（联合反映监控分类与未知拒识）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| 闭世界 us0304（2,008 类） | Accuracy | 95.41±0.11% | VarCNN 92.16% | +3.25 pp | macro-F1 94.67 vs 91.91（+2.76）；top-5 仅 +0.44 pp |
| 时移 us0304→us0320（16 天） | Accuracy | 92.99% | H&W 79.96% | +13.03 pp | 描述性下降仅 −2.42 pp（全部方法中最小） |
| 地理漂移 us0409→sg0409 | Accuracy | 91.09% | ARES 79.53% | +11.56 pp | macro-F1 89.99 vs 78.15；RF 仅 57.69（−35.12） |
| 地理漂移 us0409→fr0409 | Accuracy | 90.59% | RF 82.07% | +8.52 pp | RF 在法国最强、在新加坡最弱，说明"单地区表现不能预测另一地区" |
| 开世界 | AUROC / AUPR / OSCR | 97.64 / 88.54 / 94.81% | RF 93.04 / 72.03 / 87.61% | +4.60 / +16.51 / +7.20 pp | 增益主要来自未知站点拒识（不平衡开世界） |

消融（Table 4，均值 over 5 seeds，格式 accuracy/macro-F1）：

| 目标域 | No-Priv. | P1 Pre. | Full Priv. | Full − No-Priv. |
|---|---|---|---|---|
| us0320（时移） | 92.69 / 91.73 | 92.99 / 92.07 | 92.99 / 92.07 | +0.30 / +0.34 |
| us0409（源域 holdout） | 90.46 / 89.02 | 90.93 / 89.53 | 91.11 / 89.73 | +0.65 / +0.71 |
| fr0409（地理漂移） | 89.04 / 87.37 | 90.15 / 88.73 | 90.59 / 89.19 | +1.55 / +1.83 |
| sg0409（地理漂移） | 89.73 / 88.42 | 90.59 / 89.46 | 91.09 / 89.99 | +1.37 / +1.58 |

论文结论：时移下 P1 预训练提供大部分收益；地理漂移下增益更显著（Full Priv. 的 +1.37/+1.55 pp 约为 CipherSight 地理漂移总体退化量的 31%，macro-F1 约 30%）。No-Priv. 排除 P1 与 P2；P1 Pre. 仅在预训练阶段施加 P1；Full Priv. 两阶段都施加 P1 并在 LoRA 微调时引入 P2。

### 6.6 优势最明显的场景

分布偏移场景，尤其是地理漂移：论文明确表述特权监督在 geographic drift 下收益最大（Table 4），且 CipherSight 相对最强 baseline 的领先幅度从闭世界的 +3.25 pp 扩大到时移 +13.03 pp、地理漂移 +11.56/+8.52 pp；同时它自身的描述性退化最小（时移 −2.42/−2.60 pp；地理漂移 sg −4.41、fr −4.91 pp）。

### 6.7 局限性

见 §4.6 与论文 §Limitations：需要 SSL key log 做监督标注、未评测更长周期漂移/更多客户端/HTTP/3、top-5 增益微弱、CTX-Aware 因内存限制被截断评测（每 trace 限 6 条流 + 更小的随机森林，得 8.18%，作者注明这是其完整配置需要 >128 GB 内存所致）、STC-WF 对训练随机性敏感（seed 52 时 84.78%，而在 us0409 holdout 上可达 92.25%）。此外代码/数据未提及公开、λ 与 LoRA 超参缺失、两阶段各 20,000 steps 与 8 卡训练的成本未报告。

---

## 7. 学习与应用

### 7.1 是否开源？

解析稿未提及代码、数据或模型权重是否公开，也无仓库链接，`code: unknown`；数据集为自采（PCAP + SSL key log），论文未说明是否发布。文中引用的 RFC 与第三方 baseline 不代表本文开源。

### 7.2 复现关键步骤

1. 采集：自动化访问网页，同时保存 PCAP 与 SSL key log；用于训练的输入只取密文可观测 TLS 记录属性，key log 仅用于生成记录-资源对齐与资源属性标注。
2. 预训练：MRM（掩码整条记录 embedding，重建方向/长度桶/外层 content type）+ P1（记录级 begin/inside + inner MIME；资源级响应属性 + 记录数，Algorithm 1 的池化），共 20,000 steps，BF16。
3. 微调：冻结预训练骨干，注入 LoRA（q/k/v/o，所有 L1/L2 层），联合 P1、学生分类损失、教师分类损失与 L_feat/L_logit 蒸馏，共 20,000 steps；推理时删除 MRM/P1/P2 与全部资源标注。

### 7.3 关键超参数、预处理和训练细节

- 两阶段各 20,000 steps；PyTorch + 8 GPU + BF16；CipherSight 种子 42–46（报告 5 seed 均值±标准差，标准差 <0.15 pp），baseline 种子 42。
- baseline 训练 100 epochs（STC-WF 为 300）；Tor baseline 输入 5,000 包（截断/补零）。
- 闭世界 checkpoint 按峰值测试精度选择；漂移与开世界统一按源域 20% holdout 选择 checkpoint，再在完整目标集评测。
- 蒸馏温度 T 与 λ_MRM、λ_seg、λ_attr、λ_cnt、λ_cls、λ_struct、λ_logit、λ_feat 的取值、以及 LoRA 的 r/α、优化器与学习率：解析稿未提及（no values in the parsed transcript）。
- 预处理：TCP 重组后按流分组 TLS 记录；类别特征做 embedding，数值特征走对数分桶 embedding + log 值线性投影后求和归一化；位置编码在每条流内重置。

### 7.4 能否迁移到其他任务？

- 记录级 tokenization 可迁移到任何有明确协议数据单元边界的加密协议（QUIC/TLS 1.3 记录、DNS-over-HTTPS 等），前提是重组后能恢复单元边界。
- block-diagonal 流内注意力 + 流摘要 L2 的结构，可直接用于"多流/多连接聚合"类任务（应用指纹、隧道检测、多标签页场景）。
- LUPI 式特权监督（训练期用可解密信息，推理期零开销）与 [[2026-arXiv-ResAware__Cross-Environment_Website_Fingerprinting_via_Resource-Privileged_Distillation]] 同路线，可迁移到任何能获得"训练期特权标注"的流量理解任务。
- 评测协议（同日跨地区采集 + 16 天时移 + 源域 holdout 选 checkpoint）值得复用到漂移鲁棒性对比实验。

### 7.5 对我的研究有什么启发？

分布偏移成为 HTTPS WF 的主战场后，"闭世界高分"与"部署可用"进一步脱钩：本文用同一批 baseline 展示了 RF 在法国最强（82.07）却在新加坡最弱（57.69）、H&W 闭世界仅 86.45 却在时移中称王（79.96），说明评测必须多地区、多时间点交叉。其次，特权监督（P1/P2）把"资源语义"这一训练期才有的信息压进密文侧表示，与 ResAware（150 天漂移 F1 +8.72）形成同方向证据，值得在 KB 中作为"训练期特权信息"支线持续跟踪。第三，top-1 增益显著而 top-5 几乎持平，提示该表示提升的是"判别性"而非"召回覆盖"，设计下游系统（如候选集重排）时需注意这一区别。

---

## 8. 总结

### 8.1 核心思想

> 记录级表示 + 分层注意力 + 特权资源语义监督。

### 8.2 速记版 Pipeline

1. 采集 PCAP + SSL key log，重建 TCP 流并提取密文可观测 TLS 记录属性。
2. 记录属性 tokenize：类别 embedding + 对数分桶 embedding，每流加 [FCLS]。
3. L1 block-diagonal 自注意力建模流内依赖，产出记录表示与流摘要；L2 在 [PCLS] + 流摘要上做流间全注意力。
4. 预训练 = MRM（记录重建）+ P1（记录级/资源级监督，Aligned-Record Pooling）。
5. LoRA 微调 = P1 + 学生分类 + 特权语义教师 P2 的特征/逻辑蒸馏；推理只留记录元数据 + L1/L2 + 分类器。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]]
- [[encrypted-traffic-analysis]]
- [[traffic-representation-learning]]

### 9.2 相关方法

- [[transformer]]
- [[pre-training-finetuning]]
- [[self-supervised-learning]]

### 9.3 相关任务

- [[website-fingerprinting]]

### 9.4 可更新的综述页面

- [[survey-website-fingerprinting]]
- [[survey-encrypted-traffic-analysis]]

### 9.5 可加入的对比表

- [[method-comparison-table]]（HTTPS-native WF 方法行：单元粒度=包 vs TLS 记录、多流建模方式、跨时间/地理漂移表现）
- [[dataset-comparison-table]]（自采多日期多地区 HTTPS 集合：4 个日期 × 3 地区、2,008 类、213,099 条开世界 traces）
- [[open-source-registry]]（仅在代码发布后可登记；当前 code unknown）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 包级表示不稳定 | 重复抓取中超过 80% 的 TCP 包序列不一致 | §Challenges |
| 闭世界最优 | 95.41% accuracy / 94.67% macro-F1，超 VarCNN +3.25/+2.76 pp | Table 1 |
| 时移退化最小 | 92.99% / −2.42 pp（H&W 79.96% / −6.49；VarCNN 67.81% / −24.35） | Table 2 |
| 地理漂移领先 | sg0409 91.09%（ARES 79.53%）、fr0409 90.59%（RF 82.07%） | Table 3 |
| 特权监督在地理漂移收益最大 | Full Priv. vs No-Priv.：sg +1.37 pp、fr +1.55 pp；macro-F1 +1.58/+1.83 pp | Table 4 |
| 时移下 P1 预训练贡献主要增益 | P1 Pre. 在 us0320 即达 Full Priv. 同等精度（92.99/92.07） | Table 4 |
| 开世界拒识提升 | AUROC 97.64 / AUPR 88.54 / OSCR 94.81 vs RF 93.04 / 72.03 / 87.61 | Table 5 |
| 表征在真实漂移下仍信息量充足 | 描述性差异仅 −2.42/−2.60 pp，小于所有 baseline | §Temporal Drift |
| 超参与开源缺失 | 未给 λ/T/r/α，未提及代码与数据发布 | §Evaluation、全文 |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-arXiv-CipherSight__Robust_Website_Fingerprinting_via_Record-Resource_Semantic_Supervision_under_Distribution_Shifts.pdf
- MinerU Markdown：02-parsed-markdown/2026-arXiv-CipherSight__Robust_Website_Fingerprinting_via_Record-Resource_Semantic_Supervision_under_Distribution_Shifts.md

---

## 12. 后续问题

- 训练所需 SSL key log 若不可得（纯密文侧标注），P1/P2 全部失效，模型还剩多少漂移鲁棒性？论文未给出"无特权"版本的漂移数字（No-Priv. 行仍在预训练阶段有 MRM）。
- 16 天漂移只有一次；150 天级别的长期漂移下（对标 ResAware）记录级表示的退化曲线如何？
- 记录级表示对 TLS 1.3 记录填充、ECH 普及后的影响未讨论；HTTP/3 (QUIC) 下"记录"边界如何定义？
- 2,008 类的闭世界规模下训练成本与推理延迟未报告，无法与 CTX-Aware/STC-WF 做效率维度对比。
- STC-WF 的随机性（seed 52 差 7.47 pp）是否意味着 Table 1 中所有 baseline 的单 seed 结果方差被低估？复现时应对 baseline 也用多种子重测。
- 与 [[2026-arXiv-ResAware__Cross-Environment_Website_Fingerprinting_via_Resource-Privileged_Distillation]] 的对照需澄清：两者都做资源级特权蒸馏，但 ResAware 的增益（150 天漂移 +8.72 F1）远大于本文（16 天漂移 +0.30 pp 至 +1.83 pp），差异来自数据集/漂移幅度还是监督粒度？

---
type: method
name: "Pre-training and Fine-tuning"
aliases: ["预训练-微调范式", "Pre-train then Fine-tune"]
tags:
  - pre-training
  - fine-tuning
  - self-supervised-learning
  - transfer-learning
  - foundation-model
  - traffic-analysis
created: "2026-05-27"
updated: "2026-06-10"
---

# Pre-training and Fine-tuning（预训练-微调范式）

## 1. 方法定义

Pre-training and Fine-tuning（预训练-微调范式）是一种两阶段学习策略：第一阶段（Pre-training）在大规模无标注数据上通过自监督任务学习通用的底层表示；第二阶段（Fine-tuning）将预训练模型适配到特定下游任务，通常只需少量标注数据即可获得优异性能。

在流量分析领域，该范式将 NLP/CV 中成熟的预训练方法（如 BERT、MAE、GPT）迁移到网络流量数据上：将原始流量的字节序列、包长序列等视为"语言"，设计面向流量特性的自监督预训练任务（如 Masked Token Prediction、Same-origin Prediction、Masked Autoencoder 等），在大规模无标注流量上训练通用流量表示模型，再通过添加任务头并在少量标注数据上微调，适配流量分类、恶意流量检测、VPN 识别等下游任务。

## 2. 方法解决的问题

- **标注数据稀缺**：网络流量数据标注成本高、隐私敏感，大规模高质量标注数据难以获取；预训练范式利用大量无标注数据学习通用表示，微调仅需少量标注
- **特征工程依赖**：传统方法依赖专家手工设计统计特征（如 packet size 分布、CUMUL 累积特征），泛化能力有限；预训练模型自动从原始数据学习判别性表示
- **加密流量分析困境**：加密技术（TLS 1.3、QUIC）使 Deep Packet Inspection (DPI) 失效，传统方法难以从加密 payload 中提取有效信息；预训练模型可从字节级模式中学习隐式结构
- **跨任务泛化差**：有监督模型针对单一任务训练，难以迁移到新任务；预训练的通用表示可快速适配多种下游任务
- **数据分布不平衡**：真实流量数据普遍呈长尾分布，少数类样本不足；预训练提供的先验知识可缓解不平衡带来的性能下降

## 3. 基本流程

1. **流量表示（Traffic Representation）**：将原始 PCAP 流量转换为模型可处理的格式，包括字节序列（byte sequence）、BURST 序列、packet size/interval 序列、多模态表示等
2. **Tokenization**：将流量表示分割为 token 单元，常见方式包括 bi-gram 编码、Byte-Pair Encoding (BPE)、逐字节 tokenization、stride cutting 等
3. **输入嵌入（Input Embedding）**：为 token 添加位置编码（Position Embedding）、段编码（Segment Embedding）、类型编码（Type Embedding）等结构感知信息
4. **自监督预训练（Self-supervised Pre-training）**：在大规模无标注流量数据上，通过设计的自监督任务训练模型骨干，常见任务包括：
   - Masked Token Prediction（如 ET-BERT 的 MBM）
   - Masked Autoencoder / Patch Reconstruction（如 YaTC、NetMamba+）
   - Same-origin Prediction（如 ET-BERT 的 SBP）
   - Autoregressive Generation（如 NetGPT）
   - Contrastive Learning（如 PACKETCLIP）
5. **任务适配与微调（Task Adaptation & Fine-tuning）**：替换或添加任务特定头部（分类头、回归头等），在少量标注数据上有监督微调；常见策略包括两阶段微调（先冻结骨干训练头部，再低学习率全参数微调）

## 4. 输入与输出

| 项目 | 内容 |
|---|---|
| 输入 | 大规模无标注流量数据（预训练阶段）；少量标注流量数据（微调阶段）；输入形式包括字节序列、BURST 序列、packet size/interval 序列、灰度图像、多模态表示等 |
| 输出 | 预训练得到的通用流量表示模型；微调后的任务特定模型（分类标签、流量特征预测值、合成流量等） |
| 适用任务 | 加密流量分类、恶意软件流量检测、VPN/代理流量识别、IoT 攻击检测、网站指纹识别、TLS 1.3 网站分类、流量特征预测、流量生成 |

## 5. 典型模型或算法

**骨干架构**：
- **Encoder-only (BERT style)**：ET-BERT、PERT、NetFound、MLETC、PEAN——使用双向 Transformer Encoder，适合分类和表示学习
- **ViT / MAE style**：YaTC、Flow-MAE——将流量转换为图像或 patch，使用 Vision Transformer 和 Masked Autoencoder
- **SSM (Mamba style)**：NetMamba、NetMamba+——使用状态空间模型替代 Transformer，线性时间复杂度
- **Encoder-Decoder (T5 style)**：Lens——结合 span prediction 和包序预测
- **Decoder-only (GPT style)**：NetGPT、TrafficGPT、TrafficLLM——自回归生成式预训练

**预训练任务设计**：
- **Masked BURST Model (MBM)**：ET-BERT 提出，类似 BERT 的 MLM，随机 mask 15% 的流量 token，训练模型根据上下文预测被 mask 的 token
- **Same-origin BURST Prediction (SBP)**：ET-BERT 提出，判断两个 sub-BURST 是否来自同一 BURST，学习流内传输模式
- **Masked Autoencoder**：NetMamba+/YaTC 使用，遮蔽大部分 patch/stride（如 90%），训练模型重建被遮蔽部分
- **Multi-modal Uni-modal Pre-training**：MM4flow 提出，分别对 payload byte stream 和 packet length sequence 独立预训练，避免 modality bias

## 6. 优点

1. **显著降低标注成本**：预训练利用大量无标注数据学习通用表示，微调仅需少量标注数据。ET-BERT 在 10% 标注数据下 F1=87%，而 Deeppacket 仅 44%；MM4flow 达到 0.9 准确率仅需 baseline 10%-30% 的标注数据
2. **强大的泛化能力**：预训练模型学到的通用流量表示可跨任务迁移，在未见过的数据和新协议上表现优于从头训练的模型
3. **无需手工特征**：直接从原始流量数据自动学习判别性表示，避免了传统方法对专家经验的依赖
4. **多任务统一**：同一个预训练骨干可通过不同的微调策略适配分类、预测、生成等多种下游任务
5. **缓解数据不平衡**：预训练提供的先验知识使模型对长尾分布更鲁棒，NetMamba+ 的 LDA loss 进一步强化了这一优势
6. **对加密流量有效**：预训练模型能从加密流量的字节级模式中学习隐式结构，不依赖明文信息

## 7. 局限

1. **计算成本高**：预训练需要大量计算资源——ET-BERT 需 500,000 步训练，MM4flow 需 350 小时（8 块 RTX 6000 Ada），NetMamba+ 需 150K 步（4 块 A100）
2. **Transformer 的二次复杂度**：标准 Transformer 的 O(n^2) 注意力机制在处理长流量序列时计算和内存开销大，限制了输入长度
3. **推理延迟**：实际网络监控要求亚秒级推理，当前预训练模型的推理速度可能难以满足高速网络实时部署需求
4. **可解释性不足**：模型决策过程缺乏透明度，难以解释分类依据，在安全敏感应用中建立操作信任存在困难
5. **分布偏移敏感**：在跨时间或跨网络环境的场景下，预训练模型可能面临分布偏移导致的性能下降（如 NetMamba+ 在时序划分下准确率下降 8.47%）
6. **预训练数据安全**：大规模预训练数据可能被注入"有毒"样本，产生带后门的模型（data poisoning 攻击）

## 8. 代表论文

| 论文 | 年份 | 使用方式 | 贡献 |
|---|---:|---|---|
| ET-BERT (WWW 2022) | 2022 | Encoder-only BERT，MBM + SBP 预训练，packet/flow-level 微调 | 首个面向加密流量设计专属预训练任务的 BERT 模型；提出 Datagram2Token 框架；在 5 个加密流量分类任务上取得 SOTA；通过密码随机性分析提供理论解释 |
| NetMamba+ (ICNP 2024 / arXiv 2026) | 2026 | Mamba + Flash Attention 骨干，MAE 预训练，LDA 微调 | 首次将 Mamba 引入流量分类；多模态流量表示（stride + size + interval）；LDA loss 处理长尾分布；推理吞吐量比最佳 baseline 高 1.7 倍 |
| MM4flow (CCS 2025) | 2025 | 双模态 BERT（BERT-bytes + BERT-ps），uni-modal 预训练 + cross-attention 微调 | 首次在 TB 级（77.6 TB）真实流量上预训练；多模态融合（payload byte stream + packet length sequence）；加密隧道网站识别准确率比现有预训练模型提升 84% |
| MIETT (AAAI 2025) | 2025 | Multi-Instance Transformer，PRPP + FCL 预训练任务 | 提出两个面向流量特性的预训练任务：PRPP（Packet Relative Position Prediction，预测 packet 对的相对位置以捕获时序关系）和 FCL（Flow Contrastive Learning，同 flow 内不同 position 的 packet 为正对进行对比学习以捕获 flow 级别特征）；配合 MFP（Masked Flow Prediction）预训练，在 5 个数据集上达到 SOTA |
| TraGe (IWQoS 2025) | 2025 | Transformer + Field-level Masking 预训练 | 提出针对流量数据特点的差异化预训练策略：对 header 使用 Field-level Masking（从几何分布 Geo(p) 采样连续长度进行掩码，保持协议字段字节连续性），对 payload 使用 Random Masking（适配非连续字节分布）；引入 Dynamic Masking 防止过拟合；在应用分类上超越 SOTA 6.97% |
| TrafficGPT (arXiv 2024) | 2024 | GPT-style 自回归预训练，线性注意力 Transformer | 使用 GPT-style 自回归预训练（next token prediction）学习流量模式，通过线性注意力机制将 token 容量从 512 扩展到 12,032；结合可逆 token 表示实现 pcap ↔ token 双向映射；同一模型同时支持分类和生成，分类平均 F1 提升 2% |
| NetMamba (arXiv 2024) | 2024 | 单向 Mamba + MAE 预训练，stride-based 表示 | 首个将 Mamba/SSM 应用于流量分类的预训练模型；使用 MAE（Masked Autoencoder）对 stride 序列进行 90% 比例的遮蔽重建预训练；stride-based 1D cutting 保留序列语义优于 2D patch splitting；参数量仅 2.2M，推理速度比 Transformer 快 60 倍 |
| ASNet (TIFS 2025) | 2025 | **反例**：无需预训练即达 SOTA | 通过 WSA（无参数词义聚合器）恢复 BERT 对流量字节的完整词义 + CSS（类别约束语义分离器）配合任务感知提示显式分离不同类别语义空间，直接利用 BERT 已有通用知识，在 5 个数据集 7 个任务上无需预训练即超越 ET-BERT 和 YaTC，大幅降低计算成本 |
| TrafficMoE (arXiv 2026) | 2026 | 双分支稀疏 MoE + MLM 预训练，Disentangle-Filter-Aggregate 范式 | 提出异质性感知的 MoE 框架：Header 和 Payload 分支各自使用独立的稀疏 MoE 编码器和 Top-K 路由，实现模态特定的专家激活；预训练使用 MLM（分别对 header 和 payload token 进行随机遮蔽重建），同时联合优化不确定性感知过滤（UF）模块；微调阶段通过条件聚合（CA）自适应融合跨模态特征；在 6 个加密流量数据集上全面超越 SOTA，ISCX-Tor2016 F1 达 97.65% |
| STAR (arXiv 2025) | 2025 | 跨模态对比学习预训练（InfoNCE），双编码器零样本检索 | 首次将零样本网站指纹建模为跨模态检索问题；使用双编码器分别处理流量模态和逻辑模态（网站语义描述），通过 InfoNCE 对比损失 + 分类损失 + 类内一致性损失联合训练；引入结构感知数据增强提升泛化；在 150K+ 自动收集的流量-逻辑配对上预训练，1,600 个未见网站零样本 top-1 准确率 87.9%，开放世界 AUC 0.963 |
| Talk Like a Packet (arXiv 2026) | 2026 | 统一预训练-微调流水线，系统分类现有模型 | 提出 Transformer 流量基础模型的统一工作流程；从架构、输入模态、预训练策略三个维度对现有模型进行系统分类；验证基础模型在分类、预测、生成三类任务上的泛化能力 |

## 9. 与其他方法的比较

| 对比维度 | 传统有监督方法（AppScanner, FS-Net, Deeppacket） | 手工特征方法（CUMUL, FlowPrint, BIND） | Pre-training + Fine-tuning 范式 |
|---|---|---|---|
| 特征获取 | 从原始数据自动学习或直接输入 | 依赖专家手工设计 | 预训练自动学习通用表示 |
| 标注数据需求 | 大量标注数据 | 中等（但特征设计需专家） | 预训练无需标注，微调仅需少量 |
| 加密流量适应性 | 有效但泛化差 | 依赖明文字段，加密后受限 | 有效且泛化能力强 |
| 跨任务迁移 | 差，需重新训练 | 差，特征针对特定任务 | 好，通用表示可迁移 |
| 计算成本 | 中等 | 低 | 预训练阶段高，微调阶段低 |
| 长尾分布处理 | 差，少数类性能下降明显 | 中等 | 较好，预训练先验知识缓解不平衡 |

## 10. 在流量安全领域的应用价值

- **加密恶意流量检测**：在 TLS 1.3、QUIC 等现代加密协议下，预训练模型可从字节级模式中识别恶意软件家族特征，无需解密 payload（ET-BERT 在 USTC-TFC 上 F1=99.3%）
- **加密隧道流量分析**：MM4flow 通过多模态预训练（payload + packet length），在加密隧道网站识别上比单模态预训练模型提升 84%，解决了传统 byte-stream 方法在隧道场景下几乎完全失效的问题
- **IoT 安全**：预训练模型在多种 IoT 攻击类型（DDoS、端口扫描、SQL 注入、MITM 等）上表现出色，基础模型骨干使 F1 从 0.6978 提升至 0.9602
- **少样本安全检测**：在新型攻击或零日漏洞场景下，标注数据极其稀缺，预训练范式可在极少标注下快速适配新检测任务
- **VPN/代理流量识别**：NetMamba+ 在 Huawei-VPN 真实数据集上准确率达 94.5%，header 特征（total length, protocol, TCP flags 等）的 AM 分析揭示了关键判别字段
- **网络威胁情报**：预训练模型学到的通用流量表示可用于威胁情报共享和跨组织迁移学习

## 11. 后续问题

- 预训练模型的计算效率如何进一步提升？Mamba 等线性复杂度架构能否在更多任务上替代 Transformer？
- 如何解决预训练模型在跨时间（temporal shift）和跨网络环境（domain shift）下的分布偏移问题？
- 多模态预训练（如 MM4flow 的 byte + packet length）如何扩展到更多模态（timing、TLS handshake、DNS 等）？
- 预训练数据的安全性（data poisoning、backdoor attack）如何保障？
- 如何在高速网络（10Gbps+）环境中实现预训练模型的实时推理部署？
- 预训练模型能否支持 zero-shot 或 open-set 场景下的未知流量类型识别？
- 如何将大语言模型（LLM）的能力与流量分析预训练模型结合，实现更深层次的流量语义理解？

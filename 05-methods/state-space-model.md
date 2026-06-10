---
type: method
name: "State Space Model / Mamba"
aliases: ["状态空间模型", "SSM", "Mamba"]
tags: [state-space-model, mamba, sequence-modeling, linear-complexity, traffic-classification, pre-training]
created: "2026-05-27"
updated: "2026-06-10"
---

# State Space Model / Mamba（状态空间模型）

## 1. 方法定义

State Space Model（SSM，状态空间模型）是一类源于控制理论的序列建模架构，通过连续时间状态空间方程对序列进行建模。其离散化后的递推形式具有线性时间复杂度 O(L)，相比 Transformer 自注意力机制的 O(L^2) 大幅降低了长序列的计算和内存开销。

Mamba 是 SSM 的代表性实现（Gu & Dao, 2023），在经典 SSM 基础上引入 **Selective Scan（选择性扫描）** 机制，将状态转移参数 B、C 和离散化步长 Delta 设计为输入 x 的函数，实现内容感知（content-aware）的序列推理。配合硬件感知的并行 scan 算法和 kernel fusion，Mamba 在保持线性复杂度的同时达到了与 Transformer 相当甚至更优的性能。

在流量分析领域，SSM/Mamba 被视为 Transformer 的高效替代架构，特别适合处理长序列流量数据（如字节级流表示），是 Traffic Foundation Model 的重要技术路线之一。

## 2. 方法解决的问题

1. **Transformer 的二次复杂度瓶颈**：自注意力机制对序列长度 L 的计算和内存复杂度为 O(L^2)，在处理长序列流量数据（如数千字节的流载荷）时开销巨大，不适合在线实时分类
2. **推理效率不足**：Transformer-based 预训练模型（如 ET-BERT、YaTC、TrafficFormer）推理速度较慢，难以满足高速网络环境的实时分析需求
3. **长序列建模能力**：流量数据的字节级表示会产生较长的 token 序列，传统 RNN 的顺序依赖限制了并行计算，而 Transformer 的二次复杂度限制了序列长度
4. **内存占用**：大规模 Transformer 模型在 GPU 上的内存占用较高，限制了在资源受限设备上的部署

## 3. 基本流程

1. **输入表示**：将原始流量数据转换为 token 序列（如字节级 stride 序列、packet size 序列等）
2. **嵌入层**：通过线性投影将 token 映射到高维嵌入空间，叠加位置编码
3. **SSM 编码**：多层 Mamba block 对序列进行编码，每层包含线性投影、因果 1D 卷积、Selective Scan 和 self-gating
4. **输出解码**：根据任务类型（预训练重建 / 分类）选择解码器（MAE decoder 或 MLP 分类头）

## 4. 输入与输出

| 项目 | 内容 |
|---|---|
| 输入 | 流量 token 序列，形状 (B, L, D)，如字节级 stride 序列、packet size/inter-arrival time 序列 |
| 输出 | 编码后的序列表示 (B, L, D)，可用于重建（预训练）或分类 logits（微调） |
| 适用任务 | 加密流量分类、恶意流量检测、VPN 流量识别、IoT 攻击检测、在线流量分类、OOD 检测 |

## 5. 典型模型或算法

**核心架构组件 —— NetMamba Block（以 NetMamba+ 为例）**：

| 步骤 | 操作 | 说明 |
|---|---|---|
| 1 | LayerNorm | 对输入 X_{t-1} 做层归一化 |
| 2 | 线性投影 | 将输入投影为 x 和 z 两路 |
| 3 | 因果 1D 卷积 + SiLU | 对 x 施加因果卷积并激活 |
| 4 | 参数生成 | 基于 x' 计算输入依赖的 Delta、B、C |
| 5 | Selective Scan | 离散化 A、B，执行硬件感知 SSM 得到 y |
| 6 | Self-Gating | y 与 SiLU(z) 逐元素相乘 |
| 7 | 残差连接 | 输出 X_t = X_{t-1} + gated result |

**SSM 核心公式**：

连续形式：
$$h'(t) = \mathbf{A}h(t) + \mathbf{B}x(t), \quad y(t) = \mathbf{C}h(t)$$

通过 zero-order hold (ZOH) 离散化后变为递推公式，实现线性时间复杂度。Mamba 的关键创新在于将 B、C、Delta 设为输入 x 的函数（Selective Scan），使模型具备内容感知能力。

**Mamba 变体对比（在网络流量分类中的实验）**：

| 变体 | 描述 | 特点 |
|---|---|---|
| 单向 Mamba（NetMamba） | 标准因果 Mamba，从左到右扫描 | 效率最高，性能与双向变体相当 |
| 双向 Mamba（NetMambaB） | 前向 + 后向两个 Mamba 拼接 | 可捕获双向上下文，但计算量翻倍 |
| 级联 Mamba（NetMambaC） | 前向 Mamba 的输出再输入后向 Mamba | 信息流动更充分，但效率较低 |

实验表明，单向 Mamba 在网络流量分类任务上的性能与双向变体相当，且效率更高，说明流量序列的因果结构与单向扫描方式天然匹配。

**NetMamba 流量表示方案（Stride-based Representation）**：

NetMamba 提出了一种全面的流量表示方案，核心创新是使用 **1D stride cutting** 替代传统的 2D patch splitting。具体流程为：(1) 从每个流中选取前 M 个数据包，统一裁剪 header 为 N_h 字节、payload 为 N_p 字节；(2) 将所有字节拼接为一维数组 [b_1, b_2, ..., b_Lb]；(3) 以步长 L_s 进行非重叠切分，生成 stride 序列。与 YaTC 的 2D patch splitting 相比，stride cutting 保留了字节间的顺序语义关系，避免了将语义无关的垂直相邻字节分组到同一 patch 中的偏差问题。消融实验表明，使用 2D patch splitting 替换 stride cutting 会导致最高 1.88% 的准确率下降。此外，NetMamba 同时保留 header 和 payload 信息（通过字节平衡分配固定大小），并通过 IP 匿名化消除可识别信息偏差。

**NetMamba+ 多模态嵌入（Multimodal Embedding）与 NetTrans Block**：

NetMamba+ 在 NetMamba 的 stride 嵌入基础上引入了可插拔的多模态嵌入机制。除了字节级 stride 序列外，还提取 packet size 序列和 inter-arrival time 序列作为额外模态。对 size 和 interval 序列采用正弦位置编码（sinusoidal encoding）保留序列依赖关系，再通过模态特定的 segment indicator 区分特征来源，最终将三种模态的嵌入与 class token 拼接后加入可学习位置编码，形成统一的流量 token 序列。预训练时，stride 使用 MAE 遮蔽重建，size 使用分类重建（cross-entropy loss），interval 使用回归重建（MSE loss），三者联合优化。

此外，NetMamba+ 提出了 **NetTrans block** 作为 Transformer 的高效替代骨干，核心包含三个优化：(1) Flash Attention 2 通过 IO-aware tiling 和 recomputation 技术加速二次注意力计算，减少内存访问；(2) Pre-normalization 架构提升训练稳定性；(3) GeGLU 激活的前馈网络（FFN）提升分类精度。消融实验表明，NetTrans 在 5 个数据集上的平均性能优于 vanilla Transformer（NetTransV）和 Linear Transformer（NetTransL）。

## 6. 优点

1. **线性复杂度**：对序列长度 L 的计算复杂度为 O(L)，远低于 Transformer 的 O(L^2)，在长序列上优势显著
2. **推理效率高**：推理吞吐量比最佳 Transformer baseline (YaTC) 高 1.7 倍，GPU 内存占用更低
3. **硬件感知优化**：通过并行 scan 算法和 kernel fusion 充分利用 GPU 硬件特性
4. **内容感知**：Selective Scan 机制使模型能根据输入内容动态调整状态转移，而非使用固定的线性时不变（LTI）系统
5. **参数量小**：NetMamba+ 仅 2.6M 参数（预训练）/ 1.9M 参数（微调），远小于 ET-BERT 的 136.4M
6. **适合预训练**：与 MAE 等自监督学习范式兼容，在大规模无标注流量数据上预训练效果良好
7. **在线部署可行**：配合 DPDK 等高速抓包技术，可实现实时流量分类（NetMamba+ 在线系统达 261.87 Mb/s）

## 7. 局限

1. **单向建模**：标准 Mamba 为因果模型，仅从左到右扫描序列，可能遗漏部分需要双向上下文的信息（尽管实验表明影响有限）
2. **在网络流量领域验证尚不充分**：Mamba 在 NLP、CV 领域已有广泛验证，但在网络流量分析中仅有少量工作（如 NetMamba+），其适用性和局限性需要更多研究
3. **分布偏移敏感**：NetMamba+ 在时序划分的泛化实验中准确率下降明显（CSTNET-TLS1.3 下降 8.47%），对分布偏移的鲁棒性有待提高
4. **预训练计算开销**：虽然推理高效，但预训练仍需较大计算资源（4 块 A100 GPU，150K 步）
5. **缺乏双向注意力的全局视野**：与 Transformer 不同，Mamba 无法在一步计算中直接访问任意位置的历史信息
6. **生态和工具链不成熟**：相比 Transformer 丰富的预训练权重、高效实现和社区支持，Mamba 在网络领域的工具链尚不完善

## 8. 代表论文

| 论文 | 年份 | 使用方式 | 贡献 |
|---|---|---|---|
| NetMamba (Wang et al., arXiv 2024) | 2024 | 首个将 Mamba/SSM 应用于网络流量分类的原始工作 | 提出单向 Mamba 架构 + MAE 预训练 + stride-based 流量表示方案；保留头部+载荷综合信息；推理速度比 Transformer 快 60 倍（batch=5），参数量仅 2.2M；在 6 个数据集上实现 SOTA（CrossPlatform/ISCXTor2016/ISCXVPN2016/CICIoT2022/USTC-TFC2016）。**注意**：此为 NetMamba 原始版本，与后续 NetMamba+ (ICNP 2024 / arXiv 2026) 为不同论文 |
| NetMamba+ (Wang et al.) | 2026 (arXiv, ICNP 2024) | 在 NetMamba 基础上引入 Flash Attention 和多模态融合 | 提出融合 Mamba + Flash Attention 的高效架构（NetMamba block + NetTrans block）；设计多模态流量表示方案（stride + size + interval），通过正弦编码和 segment indicator 实现早期融合；引入 LDA loss 处理长尾分布（结合 CB loss 重加权和 LDAM 大间隔策略）；在 4 类分类任务（加密应用、攻击、恶意软件、VPN）上 F1 最高提升 6.44%；实现在线分类系统吞吐量 261.87 Mb/s |
| Mamba: Linear-Time Sequence Modeling with Selective State Spaces (Gu & Dao) | 2023 | 原始 Mamba 架构 | 提出 Selective Scan 机制，将 SSM 参数设计为输入的函数；实现硬件感知的并行 scan 算法；在语言建模上匹配 Transformer 性能 |

## 9. 与其他方法的比较

| 对比维度 | Transformer（如 ET-BERT、YaTC） | RNN / LSTM | SSM / Mamba |
|---|---|---|---|
| 时间复杂度 | O(L^2) | O(L) | O(L) |
| 空间复杂度 | O(L^2) | O(L) | O(L) |
| 并行计算 | 完全并行 | 顺序依赖 | 并行 scan |
| 全局视野 | 任意位置直接访问 | 需逐步传播 | 需逐步传播（但 Selective Scan 缓解） |
| 内容感知 | 通过 attention 权重 | 通过门控机制 | 通过 Selective Scan（B、C、Delta 输入依赖） |
| 推理效率 | 较低 | 中等 | 高 |
| 社区生态 | 极其成熟 | 成熟 | 快速发展中 |
| 在流量领域的验证 | 广泛（ET-BERT, YaTC, TrafficFormer, MM4flow 等） | 较少 | 初步（NetMamba+） |

## 10. 在流量安全领域的应用价值

1. **高效加密流量分类**：Mamba 的线性复杂度使其能在保持高分类准确率的同时大幅降低推理延迟，适合部署在高速网络节点上进行实时加密流量分类
2. **在线流量分析系统**：NetMamba+ 已验证基于 Mamba 的在线分类系统可达 261.87 Mb/s 吞吐量，为实际部署提供了可行方案
3. **长序列流量建模**：对于需要处理大量字节的长流（如视频流、大文件传输），Mamba 的线性复杂度比 Transformer 更具优势
4. **资源受限环境**：Mamba 模型参数量小（约 2M）、内存占用低，适合在边缘设备或资源受限环境中部署
5. **预训练 + 微调范式**：Mamba 架构与 MAE 等自监督预训练范式兼容，可作为 Traffic Foundation Model 的骨干网络，支持多种下游任务
6. **少样本场景**：预训练的 Mamba 模型在标注数据稀缺时仍能保持较好性能，降低了流量分析的标注成本

## 11. 后续问题

- Mamba 在更多流量分析任务（如流量生成、异常检测、网站指纹识别）上的效果如何？
- 更大规模的 Mamba 模型（参数量从 2M 扩展到数十 M 或更大）能否进一步提升性能？是否存在类似 LLM 的 scaling law？
- Mamba 与 Transformer 的混合架构（如 NetMamba+ 中同时使用 NetMamba block 和 NetTrans block）能否取长补短？
- 如何增强 Mamba 对分布偏移的鲁棒性，使其在跨时间、跨网络环境的场景下保持稳定性能？
- 其他 SSM 变体（如 S4、H3、S5）在网络流量分析中的表现如何？
- Mamba 的选择性扫描机制学到的"选择性"在流量数据中对应什么物理含义？是否可解释？
- 能否将 Mamba 与多模态融合（如 MM4flow 的 payload + packet length 双模态方案）结合，进一步提升性能？

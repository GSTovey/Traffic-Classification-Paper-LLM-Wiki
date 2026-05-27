---
type: paper
title_original: "MOTA: Mixture Of Traffic Agents for robust network traffic classification"
title_cn: "MOTA: 基于混合流量代理的鲁棒网络流量分类"
authors: ["Shaowei Li", "Zhiwen Gan", "Mengbai Xiao", "Pengfei Hu", "Xiuzhen Cheng", "Chunxiao Wang", "Feng Li"]
year: 2025
venue: "IEEE IWQoS 2025"
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2025-IWQoS-MOTA_Mixture_of_Traffic_Agents_for_Robust_Network_Traffic_Classification.pdf"
mineru_md: "02-parsed-markdown/2025-IWQoS-MOTA_Mixture_of_Traffic_Agents_for_Robust_Network_Traffic_Classification.md"
status: processed
reading_level: L2
research_area: ["network traffic classification", "encrypted traffic analysis", "large language models"]
task: ["encrypted traffic classification", "anonymous traffic classification", "robust classification under noise"]
method: ["Mixture of Agents (MoA)", "LoRA fine-tuning", "dynamic weighted voting", "multi-LLM collaboration"]
dataset: ["SJTU-AN21", "ISCX-Tor-2016", "ISCX-VPN-2016", "USTC-TFC-2016"]
code: unknown
relevance: high
created: "2026-05-27"
updated: "2026-05-27"
---

# MOTA: Mixture Of Traffic Agents for robust network traffic classification

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | MOTA: Mixture Of Traffic Agents for robust network traffic classification |
| 中文标题 | MOTA: 基于混合流量代理的鲁棒网络流量分类 |
| 作者 | Shaowei Li, Zhiwen Gan, Mengbai Xiao, Pengfei Hu, Xiuzhen Cheng, Chunxiao Wang, Feng Li |
| 年份 | 2025 |
| 会议/期刊 | IEEE International Symposium on Quality of Service (IWQoS 2025) |
| 研究方向 | 网络流量分类、加密/匿名流量分析、大语言模型应用 |
| 任务类型 | 在混合噪声环境下的加密/匿名网络流量鲁棒分类 |
| 方法关键词 | Mixture of Agents (MoA), LoRA fine-tuning, dynamic weighted voting, multi-LLM collaboration |
| 数据集 | SJTU-AN21（匿名网络）、ISCX-Tor-2016（Tor流量）、ISCX-VPN-2016（VPN流量）、USTC-TFC-2016（恶意软件流量） |
| 是否开源 | 否（论文提及使用开源模型和工具如 LlamaFactory、vLLM，但未提供 MOTA 本身代码） |
| PDF | 00-inbox/PDFs/2025-IWQoS-MOTA_Mixture_of_Traffic_Agents_for_Robust_Network_Traffic_Classification.pdf |
| MinerU Markdown | 02-parsed-markdown/2025-IWQoS-MOTA_Mixture_of_Traffic_Agents_for_Robust_Network_Traffic_Classification.md |

## 1. 一句话总结

> 利用轻量级 Mixture of Agents (MoA) 架构，通过多个经过 LoRA 微调的大语言模型（Qwen2.5 7b、Yi 6b、ChatGLM4 9b）协作，在注入五种混合噪声的四个公开数据集上实现 >=99% 的加密/匿名流量分类准确率，推理延迟仅为毫秒级。

## 2. 摘要翻译

### 2.1 摘要原文

Network traffic classification plays a crucial role in a wide range of applications, e.g., Quality of Service (QoS) enhancement, resource management, and network security. However, the widespread adoption of encryption protocols (e.g., SSL/TLS) and the emergence of anonymous communication systems (e.g., Tor) have introduced significant challenges due to the presence of complex and varied network noise. Although considerable effort has been made to improve the robustness of the traffic classification, the performances of existing state-of-the-art methods cannot be guaranteed in the presence of a mixture of noises, and are not stable in different application scenarios. In this paper, we innovate in proposing a network traffic classification method based on MoA (Mixture of Agents), namely MOTA. By leveraging a light-weight MoA architecture, MOTA efficiently fine-tunes mainstream Large Language Models (LLMs) to adapt to different application scenarios of traffic classification, and fully exploits the collaboration of the LLMs to ensure the robustness against mixed noises. Our extensive experiments show that, the classification accuracy is >= 99% across multiple public datasets injected with mixed noises, significantly outperforming existing SOTA methods. Moreover, despite incorporating multiple LLMs, MOTA maintains millisecond-level inference latency on a server equipped with four NVIDIA GeForce RTX 4090 GPUs, owing to its lightweight design.

### 2.2 摘要中文翻译

网络流量分类在多种应用中扮演关键角色，如服务质量（QoS）提升、资源管理和网络安全。然而，加密协议（如 SSL/TLS）的广泛采用以及匿名通信系统（如 Tor）的出现，由于复杂多样的网络噪声，给流量分类带来了重大挑战。尽管已有大量工作致力于提升流量分类的鲁棒性，现有最先进方法在混合噪声环境下性能无法保证，且在不同应用场景中表现不稳定。本文创新性地提出了基于 MoA（Mixture of Agents）的网络流量分类方法 MOTA。通过利用轻量级 MoA 架构，MOTA 高效微调主流大语言模型（LLM）以适应不同的流量分类应用场景，并充分利用 LLM 之间的协作以确保对混合噪声的鲁棒性。大量实验表明，在注入混合噪声的多个公开数据集上，分类准确率 >= 99%，显著优于现有 SOTA 方法。此外，尽管集成了多个 LLM，得益于轻量级设计，MOTA 在配备四块 NVIDIA GeForce RTX 4090 GPU 的服务器上仍保持毫秒级推理延迟。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 加密协议（SSL/TLS）和匿名网络（Tor、I2P）的广泛使用使得传统基于 payload 的分类方法失效
- 现有 SOTA 方法（ET-BERT、AN-Net、Netmamba、TrafficLLM）在混合噪声环境下性能急剧下降（见 Table 1：Netmamba 准确率从 99.86% 降至 21.54%）
- TrafficLLM 仅使用单个 LLM，未考虑多 LLM 协作的潜力，且忽略了噪声对单 LLM 的严重影响
- MoA（Mixture of Agents）框架在通用 NLP 任务中展现出强大能力，但在网络流量分类领域尚未被应用

### 3.2 现有方法的痛点和不足

| 现有方法 | 痛点 |
|---|---|
| ET-BERT | 在混合噪声下准确率从 95.25% 降至 43.67% |
| AN-Net | 在混合噪声下准确率从 99.51% 降至 75.97% |
| Netmamba | 在混合噪声下准确率从 99.86% 降至 21.54%，对噪声极度敏感 |
| TrafficLLM | 使用单个 ChatGLM2，在混合噪声下准确率从 98.11% 降至 62.70%，且未考虑噪声 |
| 基于端口的传统方法 | 动态端口的广泛使用使得端口分类失效 |
| DPI 方法 | 加密后无法访问签名字符串，对加密流量无效 |

### 3.3 论文的研究假设或核心直觉

- **核心假设**：不同 LLM 在不同类型网络流量上表现各异，通过多个 LLM 的协作可以实现比单个 LLM 更鲁棒的分类
- **关键直觉**：MoA 架构可以通过聚合多个 LLM 的响应来增强分类的鲁棒性，但原生 MoA 不能直接用于流量分类（原生 MoA 在 ISCX-Tor-2016 上仅 7% 准确率），需要通过微调适配
- **设计直觉**：轻量级 MoA 架构（两层而非四层）配合 LoRA 微调可以在保持高性能的同时控制推理延迟

## 4. 方法设计

### 4.1 方法整体流程

1. **数据预处理**：向原始数据集注入五种混合噪声（延迟、丢包、乱序、特征扰动、TLS 扰动），将数据转换为 Alpaca 格式以适配 LLM
2. **高效 LLM 选择**：在小规模训练集上使用 LoRA 微调 8 个主流 LLM，筛选出表现最优的三个（Qwen2.5 7b、Yi 6b、ChatGLM4 9b）
3. **MoA 部署**：用更大训练集进一步微调选定的 LLM，构建两层轻量级 MoA 架构
4. **动态加权聚合**：通过动态加权投票机制在线调整各 LLM 权重，输出最终分类结果

### 4.2 详细 Pipeline（表格形式）

| 步骤 | 描述 | 技术细节 |
|---|---|---|
| 1. 噪声注入 | 向原始 pcap 数据集注入五种噪声 | 延迟噪声（Gaussian）、丢包噪声（随机丢弃）、乱序噪声（随机置换）、特征扰动噪声（修改 TTL/端口）、TLS 扰动噪声（修改 payload 长度/注入随机字节） |
| 2. 数据格式转换 | 将流量数据转换为 Alpaca 格式 | 每个数据包信息提取为指令格式，包含 system/user/assistant 三元组 |
| 3. 小规模 LoRA 微调 | 从每个类别取 500 样本，提取 10% 用于 LLM 筛选 | 引入辅助矩阵 A 和 B，Delta_W = BA，仅更新 Delta_W，W0 冻结 |
| 4. LLM 筛选 | 在小数据集上评估 8 个 LLM | 选出 Qwen2.5 7b、Yi 6b、ChatGLM4 9b（F1 和 AC >= 91.2%） |
| 5. 大规模 LoRA 微调 | 用剩余训练数据进一步微调三个选定 LLM | 每个 LLM 训练约 130-345 分钟（取决于数据集） |
| 6. MoA 推理 | 第一层：三个 LLM 独立生成响应；第二层：聚合器做出最终决策 | 两层轻量级架构，LLM 推理可并行执行 |
| 7. 动态加权投票 | 根据每个 batch 的 F1-score 动态更新 LLM 权重 | beta_i = (F1_i / max_j(F1_j))^gamma，然后归一化 |

### 4.3 模型结构或系统模块（表格形式）

| 模块 | 功能 | 输入 | 输出 |
|---|---|---|---|
| 数据预处理模块 | 注入混合噪声、转换 Alpaca 格式 | 原始 pcap 数据集 | Alpaca 格式的训练/测试数据 |
| LLM 筛选模块 | 小规模 LoRA 微调评估 LLM 适用性 | 小规模带噪训练集 | 选定的三个 LLM |
| LLM Agent 1 (Qwen2.5 7b) | 独立生成流量分类响应 | Alpaca 格式流量数据 | 分类标签 |
| LLM Agent 2 (Yi 6b) | 独立生成流量分类响应 | Alpaca 格式流量数据 | 分类标签 |
| LLM Agent 3 (ChatGLM4 9b) | 独立生成流量分类响应 | Alpaca 格式流量数据 | 分类标签 |
| 动态加权聚合器 | 根据历史 F1-score 动态加权，选择最优 LLM 的响应 | 三个 LLM 的响应 + 权重 | 最终分类结果 |

### 4.4 公式、算法和机制解释

**LoRA 微调公式**：

$$W_0 + \Delta W = W_0 + BA$$

其中 $W_0$ 为原始 LLM 权重矩阵（冻结），$\Delta W = BA$ 为适配矩阵，$A \in \mathbb{R}^{r \times k}$，$B \in \mathbb{R}^{d \times r}$，$r \ll \min\{d, k\}$。前向传播：

$$h = W_0 d + \alpha \Delta W d = W_0 d + \alpha BAd$$

其中 $\alpha$ 为常数。A 使用随机高斯初始化，B 初始化为零，确保训练开始时 $\Delta W = 0$。

**动态加权机制**：

$$\beta_i = \left(\frac{\text{F1}_i}{\max_j \text{F1}_j}\right)^\gamma$$

$$\beta_i \leftarrow \frac{\beta_i}{\sum_j \beta_j}$$

其中 $\text{F1}_i$ 为 LLM agent $i$ 在上一个请求 batch 中的 F1-score，$\gamma$ 为常数。权重最高的 agent $i^* = \arg\min_i \beta_i$ 的响应被采纳为最终分类结果。

**关键机制解释**：
- **LoRA 优势**：仅需训练少量参数（辅助矩阵），推理时可将 $\Delta W$ 完全合并到 $W_0$ 中，不增加推理开销
- **动态加权**：不同 LLM 在不同流量类型上表现各异，动态权重使系统能在线适应不同流量场景
- **轻量级 MoA**：使用两层架构（而非原生 MoA 的四层），减少推理延迟

### 4.5 方法优势

1. **对混合噪声鲁棒**：在注入五种噪声的数据集上仍保持 >= 99% 准确率，显著优于所有 SOTA 方法
2. **跨数据集稳定性**：在四个不同应用场景的数据集上均表现优异，泛化能力强
3. **低推理延迟**：平均推理延迟 0.22s（毫秒级），得益于轻量级架构和并行推理
4. **高效微调**：LLM 筛选阶段仅需几十分钟，LoRA 微调高效
5. **自适应能力**：动态加权机制使系统能在线适应不同流量类型

### 4.6 方法不足

1. **硬件要求高**：需要配备四块 NVIDIA 4090 GPU 的服务器
2. **LLM 选择阶段需要手动筛选**：虽然有系统化的筛选流程，但仍需人工判断"Suitability"
3. **噪声类型有限**：仅注入了五种噪声，实际网络环境可能有更多噪声类型
4. **数据集规模**：训练集每类仅取 500 样本，大规模部署时的可扩展性未充分验证
5. **未与 MoA 原始四层架构做详细对比**：仅提到原生 MoA 延迟超过 6 秒，但未展示四层架构在微调后的效果

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 对比维度 | 单模型方法 (ET-BERT, Netmamba, TrafficLLM) | MOTA (本文方法) |
|---|---|---|
| 模型数量 | 单个模型 | 三个 LLM 协作 |
| 噪声鲁棒性 | 差（混合噪声下性能急剧下降） | 强（>= 99% 准确率） |
| 分类基础 | 流级特征或单 LLM | 多 LLM 动态协作 |
| 推理延迟 | 因方法而异 | 毫秒级（0.22s） |
| 适配新场景 | 需要从头训练 | LoRA 高效微调 |

与 TrafficLLM 的本质区别：TrafficLLM 仅使用单个 ChatGLM2，MOTA 利用三个不同 LLM 的协作，通过动态加权机制实现更鲁棒的分类。

### 5.2 创新点分析（表格形式）

| 创新点 | 说明 |
|---|---|
| 首次将 MoA 应用于流量分类 | 将 Mixture of Agents 框架引入网络流量分类领域 |
| 高效 LLM 筛选机制 | 利用 LoRA 在小规模数据集上高效筛选适合流量分类的 LLM |
| 轻量级两层 MoA 架构 | 将原生 MoA 的四层简化为两层，大幅降低推理延迟 |
| 动态加权投票机制 | 根据在线 F1-score 动态调整各 LLM 权重，适应不同流量场景 |
| 混合噪声注入策略 | 系统化注入五种真实网络噪声，提升方法的实用鲁棒性 |

### 5.3 适用场景

- 匿名网络流量分类：区分 Tor、I2P、JonDonym 等匿名网络中的不同应用类别
- VPN 加密流量分类：识别 VPN 隧道中的具体应用类型（浏览、聊天、邮件、P2P 等）
- 恶意软件流量检测：在存在网络噪声的情况下识别恶意软件流量
- 需要高鲁棒性的实时流量分类场景

### 5.4 方法对比表

| 方法 | 是否处理加密流量 | 噪声鲁棒性 | 模型架构 | 推理延迟 |
|---|---|---|---|---|
| Whisper | 部分 | 低 | 频域特征 + 聚类 | 快 |
| Flowlens | 是 | 中 | 多项式朴素贝叶斯 | 快 |
| FS-Net | 是 | 中 | RNN 编码器-解码器 | 中 |
| AttnLSTM | 是 | 中 | LSTM + 注意力机制 | 中 |
| ET-Bert | 是 | 低 | BERT 预训练 + 微调 | 中 |
| AN-Net | 是 | 中 | 高温注意力机制 | 中 |
| NetMamba | 是 | 低 | Mamba 单向架构 | 中 |
| TrafficLLM | 是 | 中 | 单个 ChatGLM2 | 中 |
| **MOTA (本文)** | **是** | **高** | **三 LLM MoA + 动态加权** | **快（0.22s）** |

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **硬件环境**：配备 4 块 NVIDIA GeForce RTX 4090 GPU 的服务器
- **软件框架**：LlamaFactory（训练）、vLLM（推理）
- **训练数据**：每个数据集每个类别取 500 样本（SJTU-AN21: 5000, ISCX-Tor-2016: 4000, ISCX-VPN-2016: 7000, USTC-TFC-2016: 10000）
- **测试数据**：每个类别取 100 样本（SJTU-AN21: 1000, ISCX-Tor-2016: 800, ISCX-VPN-2016: 1400, USTC-TFC-2016: 2000）
- **噪声注入**：五种噪声同时注入（延迟、丢包、乱序、特征扰动、TLS 扰动）

### 6.2 数据集

| 数据集 | 类别数 | 训练样本数 | 测试样本数 | 场景描述 |
|---|---|---|---|---|
| SJTU-AN21 | 10 | 5000 | 1000 | 匿名网络（Tor、I2P、JonDonym） |
| ISCX-Tor-2016 | 8 | 4000 | 800 | Tor 流量分类 |
| ISCX-VPN-2016 | 7 | 7000 | 1400 | VPN 加密流量分类 |
| USTC-TFC-2016 | 20 | 10000 | 2000 | 恶意软件流量分类 |

### 6.3 Baseline

论文对比了 8 个 SOTA 方法：Whisper、Flowlens、AttnLSTM、FS-Net、ET-Bert、AN-Net、NetMamba、TrafficLLM。所有方法均在注入混合噪声的数据集上训练和测试。

### 6.4 评价指标

- **Accuracy (AC)**：整体分类准确率
- **Precision (PR)**：加权平均精确率
- **Recall (RC)**：加权平均召回率
- **F1-score (F1)**：加权平均 F1 分数
- **推理延迟**：不同 batch size 下的平均推理时间

### 6.5 关键实验结果（表格形式）

| 数据集 | AC | PR | RC | F1 |
|---|---|---|---|---|
| SJTU-AN21 | 100.00% | 100.00% | 100.00% | 100.00% |
| ISCX-Tor-2016 | 100.00% | 100.00% | 100.00% | 100.00% |
| ISCX-VPN-2016 | 99.58% | 99.59% | 99.58% | 99.58% |
| USTC-TFC-2016 | 99.99% | 99.99% | 99.99% | 99.99% |

**与最佳 baseline 对比**：在 SJTU-AN21 和 ISCX-Tor-2016 上 MOTA 达到 100%，而最佳 baseline TrafficLLM 分别为 98.33% 和 62.70%。在 ISCX-VPN-2016 和 USTC-TFC-2016 上，AN-Net（98.13%、97.76%）和 NetMamba（95.02%、99.31%）表现较好但仍低于 MOTA。

**推理延迟**：batch size 为 10 时平均延迟 0.28s，batch size 为 100-10000 时平均延迟 0.21-0.22s，比 TrafficLLM 仅增加 0.21-0.28s。

**稳定性分析**：当测试数据量为训练数据量的 1-4 倍时，MOTA 的四项指标均 >= 98.3%。

**消融实验**：移除任一 LLM 或使用静态权重替代动态权重，性能均有下降（0.03%-5.2%），验证了每个组件的必要性。

### 6.6 优势最明显的场景

- **ISCX-Tor-2016**：MOTA 达到 100%，而所有 baseline 在混合噪声下均表现较差（最佳 AN-Net 仅 75.15% F1）
- **SJTU-AN21**：MOTA 达到 100%，而多数 baseline 在混合噪声下大幅退化
- **跨数据集一致性**：MOTA 在四个差异很大的数据集上均保持 >= 99.58% 的表现

### 6.7 局限性

1. **硬件依赖**：需要高端 GPU 服务器（4 块 4090），部署成本较高
2. **噪声覆盖有限**：仅测试了五种噪声，实际网络环境可能更复杂
3. **数据集规模**：训练数据相对较少（每类 500 样本），大规模场景下的可扩展性需进一步验证
4. **未与单 LLM 大模型对比**：未与 GPT-4 等大型闭源 LLM 进行对比
5. **LLM 选择过程半自动**：需要人工根据 Table 2 结果判断哪些 LLM "Suitable"

## 7. 学习与应用

### 7.1 是否开源？

论文未提供 MOTA 的源代码，但使用了以下开源工具和模型：
- LlamaFactory（训练框架）
- vLLM（推理框架）
- 开源 LLM：Qwen2.5、Yi、ChatGLM4

### 7.2 复现关键步骤

1. **准备数据集**：下载 SJTU-AN21、ISCX-Tor-2016、ISCX-VPN-2016、USTC-TFC-2016 四个数据集
2. **噪声注入**：实现五种噪声注入（延迟、丢包、乱序、特征扰动、TLS 扰动）
3. **数据格式转换**：将 pcap 数据转换为 Alpaca 格式（system/user/assistant 三元组）
4. **LLM 筛选**：对多个 LLM 使用 LoRA 在小数据集上微调，选出表现最好的三个
5. **大规模微调**：用完整训练集对选定 LLM 进行 LoRA 微调
6. **部署 MoA**：构建两层架构，实现动态加权投票机制
7. **评估**：在带噪测试集上评估分类性能和推理延迟

### 7.3 关键超参数、预训练和训练细节

| 参数 | 值/说明 |
|---|---|
| 选定 LLM | Qwen2.5 7b, Yi 6b, ChatGLM4 9b |
| LoRA 秩 r | 未明确说明具体值 |
| LoRA alpha | 未明确说明具体值 |
| 筛选阶段训练样本 | 每类 500 样本的 10% |
| 正式训练样本 | 每类 500 样本（剩余 90%） |
| 筛选阶段训练时间 | 约 11-33 分钟/LPU |
| 正式训练时间 | 约 125-345 分钟 |
| gamma (动态权重) | 未明确说明具体值 |
| batch size (推理) | 10-10000 |
| 硬件 | 4x NVIDIA GeForce RTX 4090 GPU |

### 7.4 能否迁移到其他任务？

- **其他加密流量分类**：方法可直接迁移到新的加密流量分类任务，只需准备对应数据集并重新微调
- **IoT 流量分类**：IoT 设备流量同样面临噪声问题，MoA 架构可提升鲁棒性
- **入侵检测系统**：将流量分类扩展为恶意/正常二分类或多分类
- **5G/6G 网络切片流量识别**：不同网络切片的流量分类可受益于多 LLM 协作
- **其他领域的 MoA 应用**：动态加权机制可推广到任何需要多模型协作的场景

### 7.5 对我的研究有什么启发？

1. **多模型协作的鲁棒性**：单个模型容易被噪声击败，多模型协作可以显著提升鲁棒性，这一思想可推广到其他安全分析任务
2. **LoRA 高效筛选**：在小规模数据上用 LoRA 快速筛选模型，是一种高效的模型选择策略
3. **动态加权的重要性**：不同模型在不同场景下表现各异，静态集成不如动态加权
4. **噪声注入作为数据增强**：在训练时注入多种噪声是提升模型鲁棒性的有效手段
5. **轻量级设计权衡**：将四层 MoA 简化为两层，在性能和延迟之间取得良好平衡

## 8. 总结

### 8.1 核心思想（不超过20字）

多LLM协作的MoA架构实现混合噪声下的鲁棒流量分类。

### 8.2 速记版 Pipeline（3-5步）

1. 向数据集注入五种混合噪声，转换为 Alpaca 格式
2. 用 LoRA 在小数据集上筛选出 Qwen2.5 7b、Yi 6b、ChatGLM4 9b 三个 LLM
3. 用完整训练集进一步 LoRA 微调三个 LLM
4. 构建两层 MoA 架构，三个 LLM Agent 并行推理
5. 通过动态加权投票聚合响应，输出最终分类结果

## 9. Obsidian 知识链接

### 9.1 相关概念

- Encrypted Traffic Classification - 加密流量分类
- Anonymous Traffic Classification - 匿名流量分类
- Mixture of Agents (MoA) - 混合代理框架
- Large Language Models for Traffic Analysis - 大语言模型在流量分析中的应用
- Network Noise Robustness - 网络噪声鲁棒性
- Tor Traffic Classification - Tor 流量分类
- VPN Traffic Classification - VPN 流量分类

### 9.2 相关方法

- LoRA (Low-Rank Adaptation) - 低秩适配微调
- Dynamic Weighted Voting - 动态加权投票
- Ensemble Learning - 集成学习
- ET-BERT - 基于 BERT 的加密流量表示
- NetMamba - 基于 Mamba 的网络流量分类
- TrafficLLM - 基于 LLM 的流量分类
- AN-Net - 抗噪声匿名流量分类网络

### 9.3 相关任务

- Robust Traffic Classification under Noise - 噪声下的鲁棒流量分类
- Encrypted Traffic Classification with LLM - 基于 LLM 的加密流量分类
- Malware Traffic Detection - 恶意软件流量检测
- Application Identification in Encrypted Traffic - 加密流量中的应用识别

### 9.4 可更新的综述页面

- Encrypted Traffic Classification Survey
- LLM-based Network Traffic Analysis
- Robust Traffic Classification Methods

### 9.5 可加入的对比表

- Encrypted Traffic Classification Methods
- Noise-Robust Traffic Classification Comparison
- LLM-based Traffic Classification Methods

## 10. 证据记录（表格形式）

| 编号 | 类型 | 证据内容 | 页码/位置 |
|---|---|---|---|
| E1 | 实验结果 | Netmamba 在混合噪声下准确率从 99.86% 降至 21.54% | Table 1 |
| E2 | 实验结果 | TrafficLLM 在混合噪声下准确率从 98.11% 降至 62.70% | Table 1 |
| E3 | 实验结果 | MOTA 在 SJTU-AN21 上 AC/PR/RC/F1 均为 100% | Table 3 |
| E4 | 实验结果 | MOTA 在 ISCX-Tor-2016 上 AC/PR/RC/F1 均为 100% | Table 3 |
| E5 | 实验结果 | MOTA 在 ISCX-VPN-2016 上四项指标 >= 99.58% | Table 3 |
| E6 | 实验结果 | MOTA 在 USTC-TFC-2016 上四项指标 >= 99.99% | Table 3 |
| E7 | LLM 筛选 | Qwen2.5 7b、Yi 6b、ChatGLM4 9b 在四个数据集上 F1 和 AC >= 91.2% | Table 2 |
| E8 | 消融实验 | 移除 ChatGLM4 后 ISCX-Tor-2016 上 F1 从 99.98% 降至 90.80% | Table 4 |
| E9 | 推理延迟 | MOTA 平均推理延迟 0.21-0.28s，仅比 TrafficLLM 增加 0.21-0.28s | Fig. 9 |
| E10 | 稳定性分析 | 测试数据量为训练数据量 4 倍时，MOTA 四项指标仍 >= 98.3% | Fig. 8 |

## 11. 原始资料链接

- 论文发表于 IEEE IWQoS 2025
- 作者单位：山东大学计算机科学与技术学院、齐鲁工业大学（山东省科学院）山东省计算中心
- 项目资助：山东省重点研发计划（2024CXGC010113）、NSFC（62472253, U23A20273）、山东省自然科学基金（ZR2022LZH010, ZR2022ZD02）、泰山学者计划
- 使用的开源工具：LlamaFactory、vLLM
- 使用的开源模型：Qwen2.5、Yi、ChatGLM4

## 12. 后续问题

1. **更多 LLM 组合**：是否可以尝试更多或更大的 LLM（如 GPT-4、Claude）？性能提升是否值得增加的计算成本？
2. **更多噪声类型**：实际网络中还有哪些噪声类型？方法能否泛化到更复杂的噪声环境？
3. **实时部署**：在实际网络设备（如路由器、交换机）上部署时，延迟和资源消耗是否可接受？
4. **对抗性攻击**：如果攻击者故意构造对抗样本来欺骗 LLM，MOTA 的鲁棒性如何？
5. **动态权重机制优化**：gamma 参数的最优值如何确定？是否有更优的权重更新策略？
6. **与其他集成方法对比**：与传统的集成学习方法（如 Random Forest、XGBoost）相比，MoA 的优势在哪里？
7. **隐私问题**：将网络流量数据输入 LLM 是否会带来隐私泄露风险？
8. **模型更新**：当新的 LLM 发布时，如何高效地将其集成到 MOTA 中？

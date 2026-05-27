---
type: paper
pdf: "00-inbox/PDFs/2023-SIGKDD-A_lightweight__efficient_and_explainable__by__design_convolutional_neural_network_for_internet_traffic_classification.md"
status: processed
reading_level: L2
created: "2026-05-27"
updated: "2026-05-27"
title: "A Lightweight, Efficient and Explainable-by-Design Convolutional Neural Network for Internet Traffic Classification"
authors:
  - Kevin Fauvel
  - Fuxing Chen
  - Dario Rossi
affiliation: Huawei Technologies Co., Ltd France
venue: SIGKDD 2023
tags:
  - traffic-classification
  - encrypted-traffic
  - explainable-AI
  - lightweight-CNN
  - prototype-network
  - CNN
  - ResNet
---

# 0. 元信息

| 项目 | 内容 |
|------|------|
| 标题 | A Lightweight, Efficient and Explainable-by-Design Convolutional Neural Network for Internet Traffic Classification |
| 作者 | Kevin Fauvel, Fuxing Chen, Dario Rossi |
| 单位 | Huawei Technologies Co., Ltd France |
| 会议 | SIGKDD 2023 |
| 关键词 | Deep Learning, Explainable AI, Internet Traffic Classification |
| 代码 | https://github.com/XAIseries/LEXNet |
| 数据集 | https://figshare.com/articles/dataset/AppClassNet.../20375580 |

# 1. 研究动机与问题定义

## 1.1 研究背景

流量分类（Traffic Classification）是识别网络中流动的应用类型的战略性任务，广泛用于容量规划、入侵检测和服务差异化等网络管理活动。随着加密流量的急剧增长，传统基于规则的 Deep Packet Inspection (DPI) 方法受阻，促使机器学习辅助分类的采用。

## 1.2 现有方法的不足

当前深度学习方法存在三大关键挑战：

1. **计算资源受限**：网络硬件（如路由器）通常在有限计算资源上运行，而现有模型普遍拥有数百万参数（1M-2M），无法满足近实时分类需求（约 10k classifications/second on ARM CPUs）。
2. **缺乏忠实的可解释性**：监管机构强调可解释性是 AI 系统问责、责任和透明的基础，而现有流量分类器依赖 post hoc 方法（如 SHAP、Grad-CAM），无法提供 faithful explainability。
3. **评估数据集规模小**：学术模型通常在仅几十个类别的小数据集上评估，无法反映真实商业环境中成百上千个应用的多样性。

## 1.3 研究目标

提出一种轻量级、高效且设计可解释（explainable-by-design）的 CNN（LEXNet），在大规模商业级数据集上实现与最优深度学习方法相当的准确率，同时提供忠实的可解释性。

# 2. 核心贡献

1. **LERes Block**：重新设计 ResNet 的 residual block，通过线性变换和拼接操作替代部分卷积，参数量减少 19%，CPU 推理时间减少 41%，准确率仅下降 0.7%。
2. **LProto Layer**：将 ProtoPNet 的 prototype block 转换为轻量级 prototype layer，参数量减少 36%，CPU 推理时间减少 24%，准确率提升 4%。自动学习每个类别可变数量的 prototype。
3. **大规模评估**：在商业级数据集（200 类，9.7M flows）上评估，并在多个外部数据集上验证泛化性。
4. **可解释性评估**：首次量化 explainability 对预测性能、模型大小和推理时间的影响，并证明 LEXNet 的 by-design 解释比 post hoc 方法更忠实。

# 3. 方法论（Methodology）

## 3.1 整体架构

LEXNet 采用三段式 prototype-based 网络结构：

```
输入 (20×2 MTS) → CNN Backbone (LERes blocks) → Prototype Layer (LProto) → 全连接层 → 分类输出
```

输入为每个 flow 的前 20 个包的 packet size 和 direction（Multivariate Time Series），输出为 200 个应用类别的标签。

## 3.2 LERes Block（轻量高效残差块）

### 设计动机

- ResNet 在流量分类数据集上准确率最高（90.4%），但原始 residual block 存在冗余。
- ShuffleNetV2 的指导原则指出：高效卷积应保持等宽通道以最小化内存访问成本和推理时间。
- GhostNet 的观察：CNN 中存在特征图冗余，部分特征图可用廉价的线性变换替代。

### 具体设计

原始 Res Block 含 3 个卷积（Conv1、Conv2、Conv3），其中 Conv3 用于维度匹配。LERes 的改进：

1. **线性变换生成特征图**：对第一个卷积的输出施加 3×3 linear kernel 的线性变换，将特征图数量翻倍，再与原始输出拼接。这样第一和第二个卷积都保持等宽通道。
2. **拼接替代 shortcut 卷积**：省略原始 Conv3，直接将输入数据与第一层卷积输出拼接，避免额外的卷积计算。

### 效果

- Backbone 参数减少 19.1%
- CPU 推理时间减少 41.3%
- 准确率保持原始 ResNet 的 99.3%

## 3.3 LProto Layer（轻量原型层）

### 设计动机

ProtoPNet 的 prototype block 存在以下问题：
- 添加了两个通道数较多的卷积层（推荐设置 >= 128），增加了模型大小和推理时间。
- 所有类别使用固定数量的 prototype，无法针对不同应用的复杂度进行自适应。

### 具体设计

1. **移除额外卷积层**：直接使用 CNN backbone 的输出（深度 32），而非 ProtoPNet 的 128，大幅减少参数。
2. **Sigmoid 替代 ReLU**：将 CNN backbone 最后一层的激活函数从 ReLU 替换为 Sigmoid，提升准确率。
3. **L2 正则化**：对 prototype 权重施加 L2 正则化，增强泛化能力（贡献 +2.8% 准确率）。
4. **可变数量 prototype**：训练过程中自动学习每个类别不同数量的 prototype（初始化时每类 1 个），通过 Kurtosis 评估 prototype 的判别力，在分布重尾（kurtosis > 0）的类别中增加一个 prototype。

### Prototype 工作机制

- 每个 prototype 计算与最后一个卷积层所有 patch 的 L2 距离，转换为相似度分数。
- 激活图保留卷积输出的空间关系，可上采样到输入尺寸产生 heatmap。
- 训练时 prototype 投影到同类最近的训练 patch 上，确保其对应真实样本区域。
- 全局最大池化将每个 prototype 的激活图缩减为单一相似度分数。
- 全连接层基于相似度分数进行分类。

### 效果

- 参数减少 36%，CPU 推理时间减少 24%，准确率提升 4%
- 总 prototype 数从 400（ProtoPNet，每类固定 2 个）降至 340（平均 1.7 个/类）

## 3.4 网络训练（三阶段循环）

训练过程包含三个阶段，循环进行直到达到全局 epoch 数：

| 阶段 | 内容 | 细节 |
|------|------|------|
| Stage 1 | SGD 训练 backbone 和 prototype | 更新 backbone 权重和 prototype 权重，冻结最后一层权重；前 5 个 epoch 仅 warm-up backbone |
| Stage 2 | 更新 prototype | 将每个 prototype 投影到同类最近的训练 patch；计算每类样本到最近 prototype 的平均距离；若 Kurtosis > 0，则在 25th percentile 的类别中增加 1 个 prototype |
| Stage 3 | 训练最后一层 | 冻结 backbone 和 prototype 权重，仅更新全连接层权重 |

## 3.5 网络架构细节

| 层 | 输出维度 | 说明 |
|----|----------|------|
| Conv3x3 + BN | 8×20×2 | 初始卷积 |
| LERes Block ×4 | 16→16→32→32×20×2 | 4 个残差块，逐步增加通道 |
| LProto Layer | 340×20×2 | 340 个 prototype |
| Max Pooling | 340×1×1 | 全局最大池化 |
| FC | 200 | 分类输出 |

总参数量：118,880（约 119k）

# 4. 实验设置

## 4.1 数据集

| 数据集 | 类型 | 流数量 | 类别数 | 说明 |
|--------|------|--------|--------|------|
| AppClassNet（主数据集）| 商业级 | 9.7M | 200（169 TCP + 31 UDP）| 来自中国四个客户部署，四周数据，DPI 标注 |
| MIRAGE | 公开 | 100k | 40 | 流量分类 benchmark |
| CESNET-TLS | 公开 | 38M | 191 | TLS 流量分类 |
| MNIST | 公开 | 70k | 10 | 计算机视觉 benchmark |

- 输入表示：每个 flow 前 20 个包的 packet size 和 direction，形成 20×2 的 Multivariate Time Series。
- 存在类别不平衡：前 10 个应用占 42.9% 的流量。

## 4.2 对比算法

- **CNN 类**：ResNet, DenseNet, EfficientNet, GhostNet, MobileNetV3, ShuffleNetV2, CondenseNetV2, 1D CNN
- **MTS 分类器**：XCM, MLSTM-FCN
- **Prototype 网络**：ProtoPNet
- **传统方法**：Random Forest, XGBoost
- **Post hoc 可解释性**：Grad-CAM, SHAP

## 4.3 训练配置

- 训练/测试划分：50%/50%，分层保留结构
- 超参数搜索：分层 5 折交叉验证，网格搜索
- 训练：1000 epochs，batch size 1024
- 硬件：NVIDIA Tesla V100 16GB GPU；Intel Xeon Platinum 8164 CPU

# 5. 实验结果（Experiments）

## 5.1 CNN Backbone 选择

在约 300k 参数的可比模型规模下，各分类器对比：

| 模型 | 准确率(%) | GPU 推理(us/sample) | CPU 推理(us/sample) | 参数量(k) |
|------|-----------|---------------------|---------------------|-----------|
| ResNet (Medium) | **90.4 ± 0.1** | 1.6 | 34.6 | 303 |
| DenseNet | 89.5 ± 0.4 | 3.3 | 91.8 | 328 |
| GhostNet | 88.6 ± 0.3 | 11.5 | 473.8 | 322 |
| XCM | 88.1 ± 0.2 | 8.1 | 355 | 315 |
| CondenseNetV2 | 87.9 ± 0.1 | 3.1 | 80.3 | 326 |
| ShuffleNetV2 | 86.9 ± 0.3 | 2.5 | 69.8 | 305 |
| 1D CNN | 84.5 ± 0.2 | 1.4 | 26.6 | 274 |

关键发现：
- ResNet 准确率最高且方差最小。
- 优化 FLOPs 并不等价于优化推理时间（如 CondenseNetV2 FLOPs 仅 0.4M 但推理慢于 ResNet 的 2.1M）。
- 树模型（RF、XGBoost）准确率接近 1D CNN 但慢约 1000 倍。

## 5.2 LEXNet vs. ProtoPNet 消融实验

从 ProtoPNet 到 LEXNet 的逐步改进：

| 步骤 | 准确率变化 | 参数变化 | GPU 推理变化 | CPU 推理变化 |
|------|-----------|----------|-------------|-------------|
| (0) ProtoPNet 基线 | 86.2% | 199k | 5.5us | 169.7us |
| +移除额外卷积 | +0.2% | -59k | -1.5us | -29.3us |
| +Sigmoid | +1.2% | - | - | -0.6us |
| +L2 正则化 | +2.8% | - | - | +1us |
| +可变 prototype | 持平 | -12k | -0.1us | -11.2us |
| **= LProto 总效果** | **+4%** | **-36%** | **-29%** | **-24%** |
| +Linear 变换 | -0.5% | -3k | -0.1us | -11.9us |
| +Concatenate | -0.2% | -6k | -0.2us | -15us |
| **= LEXNet 总效果** | **+4%** | **-40%** | **-35%** | **-39%** |

LEXNet 最终性能：89.7% 准确率，119k 参数，GPU 3.6us/sample，CPU 102.7us/sample。

## 5.3 外部数据集泛化性

| 数据集 | 模型 | 准确率(%) | 参数(k) | CPU 推理(us) |
|--------|------|-----------|---------|-------------|
| CESNET-TLS | LEXNet | **97.2** | 111 | 92.1 |
| CESNET-TLS | ProtoPNet | 94.1 | 189 | 146.3 |
| MIRAGE | LEXNet | **73.6** | 43 | 32.8 |
| MIRAGE | ProtoPNet | 71.4 | 81 | 40.9 |
| MNIST | LEXNet | **99.0** | 39 | 1138 |
| MNIST | ProtoPNet | 97.3 | 70 | 1834 |

所有数据集上 LEXNet 均与 ResNet 持平，且优于 ProtoPNet。

## 5.4 可解释性评估

### 定性说明

- LEXNet 以 class-specific prototype（大小 1×1）的形式提供解释，精确标识输入 flow 中用于预测的区域。
- 例如：某 TCP 应用的两个 prototype 分别是位置 2 的小包（44 bytes）和位置 8 的下行包。
- prototype 数量与流量数呈负相关（-0.24）：热门应用只需 1 个 prototype 即可表征。

### 忠实性定量评估（Faithfulness）

| 方法 | Top-Protos 准确率(%) | Top-10 准确率(%) |
|------|----------------------|-----------------|
| LEXNet by-design | **100.0** | - |
| Grad-CAM | 8.2 | 38.9 |
| SHAP | 5.9 | 27.4 |

Post hoc 方法即使使用输入数据 25% 的区域（top-10），识别 LEXNet prototype 的准确率也不到 40%，说明 by-design 方法在忠实性上远优于 post hoc 方法。

### 可解释性的代价

| 模型 | 准确率(%) | 参数(k) | GPU(us) | CPU(us) |
|------|-----------|---------|---------|---------|
| ResNet + Grad-CAM | 89.7 | 294 | 9.5 | 278.6 |
| ResNet + SHAP | 89.7 | 294 | 8300 | 68000 |
| ProtoPNet | 86.2 | 199 | 5.2 | 142.8 |
| **LEXNet** | **89.7** | **119** | **3.6** | **102.7** |

LEXNet 比 ResNet+Grad-CAM 快约 2.5 倍，模型大小减半，同时保持准确率。约 80% 的额外推理时间来自 LProto 层中 L2 距离计算生成相似度矩阵。

# 6. 方法创新点分析

1. **将 GhostNet 的线性变换思想引入 residual block**：用廉价的线性变换替代部分卷积操作，在保持等宽通道的前提下减少参数和推理时间。
2. **可变数量 prototype 的自动学习机制**：利用 Kurtosis 统计量评估 prototype 判别力分布，在需要的类别中自动增加 prototype，而非固定数量。
3. **首次量化可解释性的性能代价**：系统比较了 by-design 和 post hoc 方法在准确率、模型大小和推理时间三个维度的权衡。

# 7. 局限性与未来方向

1. **可解释性带来的推理开销**：相比无解释的 ResNet（GPU 1.3us/CPU 20.3us），LEXNet 的推理时间仍有明显增长（GPU 3.6us/CPU 102.7us），约 80% 来自 L2 距离计算，有待优化。
2. **数据集地域性**：主数据集来自中国客户部署，加密程度与西方市场不同，DPI 标注在强加密场景下可能失效。
3. **未探索大模型**：论文明确排除了大型多模态模型，因其与网络设备有限计算资源不兼容。
4. **未来方向**：优化 prototype 层中相似度矩阵的生成效率；在其他领域（移动性预测、自然灾害预警、智慧农业）中探索 LEXNet 的应用。

# 8. 关键术语表

| 术语 | 定义 |
|------|------|
| Traffic Classification | 识别网络中流动的应用类型的任务 |
| Explainability-by-design | 模型在设计层面内建可解释性，而非事后解释 |
| Faithfulness | 解释与模型实际计算之间的一致性程度 |
| Prototype | 训练数据中具有判别力的区域/模式，用于分类和解释 |
| LERes Block | LEXNet 的轻量高效残差块，通过线性变换和拼接减少参数 |
| LProto Layer | LEXNet 的轻量原型层，自动学习可变数量的 class-specific prototype |
| Multivariate Time Series (MTS) | 多变量时间序列，此处指 packet size 和 direction 构成的序列 |
| Post hoc Explainability | 事后解释方法，如 Grad-CAM、SHAP，不嵌入模型设计中 |
| Kurtosis | 分布的峰度，用于衡量重尾程度，LEXNet 用其评估 prototype 判别力 |

# 9. 与其他工作的关系

- **ProtoPNet (Chen et al., 2019)**：LEXNet 的直接基础，LEXNet 通过 LERes 和 LProto 改进其效率和准确率。
- **ResNet (He et al., 2016)**：作为 CNN backbone 的起点，LERes 是对其 residual block 的重新设计。
- **GhostNet (Han et al., 2020)**：线性变换替代冗余特征图的思想来源。
- **ShuffleNetV2 (Ma et al., 2018)**：等宽通道设计原则的来源。
- **XCM / MLSTM-FCN**：MTS 分类领域的 state-of-the-art 对比基线。

# 10. 可复现性要点

- 代码和数据集均已开源。
- 输入格式：每个 flow 取前 20 个包，每包 2 个变量（packet size + direction），形成 20×2 的 MTS。
- 训练：1000 epochs，batch size 1024，SGD 优化，50%/50% 训练/测试划分。
- LEXNet 总参数 118,880，含 4 个 LERes block 和 1 个 LProto layer。
- 最佳 prototype 配置：大小 (1,1)，平均 1.7 个/类（范围 1-5）。

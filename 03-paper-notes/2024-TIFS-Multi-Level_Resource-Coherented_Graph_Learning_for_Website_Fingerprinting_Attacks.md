---
type: paper
title_original: "Multi-Level Resource-Coherented Graph Learning for Website Fingerprinting Attacks"
title_cn: "基于多层资源聚合图学习的网站指纹攻击"
authors:
  - Bo Gao
  - Weiwei Liu
  - Guangjie Liu
  - Fengyuan Nie
  - Jianan Huang
year: 2024
venue: "IEEE TIFS 2024"
doi: "10.1109/TIFS.2024.3520014"
url: "https://ieeexplore.ieee.org/document/10791048"
pdf: ""
mineru_md: "02-parsed-markdown/2024-TIFS-Multi-Level_Resource-Coherented_Graph_Learning_for_Website_Fingerprinting_Attacks.md"
status: processed
reading_level: L2
dataset:
  - "自建数据集：83个网站（HTTP 10类 + HTTPS 10类），总计 3,690,513 flows"
  - "HTTP 类别：新闻、购物、软件、音乐、搜索、电子书、游戏、公共、博客、恶意网站"
  - "HTTPS 类别：新闻、购物、软件、音乐、搜索、办公、邮箱、视频、社交、支付"
code: "未开源"
relevance: medium
research_area:
  - "网站指纹"
  - "图神经网络"
  - "加密流量分析"
task:
  - "网站指纹识别"
  - "流量分类"
method:
  - "GCN"
  - "自监督学习"
  - "图核函数"
  - "图聚类"
created: "2026-06-21"
updated: "2026-06-21"
related_papers:
  - "[[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]]"
  - "[[2021-TIFS-Accurate_Decentralized_Application_Identification_via_Encrypted_Traffic_Analysis_Using_Graph_Neural_Networks]]"
---

# Multi-Level Resource-Coherented Graph Learning for Website Fingerprinting Attacks

## 0. 基础信息

| 项目 | 内容 |
|------|------|
| 论文标题 | Multi-Level Resource-Coherented Graph Learning for Website Fingerprinting Attacks |
| 作者 | Bo Gao, Weiwei Liu, Guangjie Liu, Fengyuan Nie, Jianan Huang |
| 机构 | 南京理工大学 自动化学院；南京信息工程大学 电子信息工程学院 |
| 期刊 | IEEE Transactions on Information Forensics and Security (TIFS) |
| 发表时间 | 2024年12月（Date of publication: 18 December 2024） |
| DOI | 10.1109/TIFS.2024.3520014 |
| 关键词 | Network traffic analysis, website fingerprinting attacks, graph learning, representation learning, self-supervised learning, graph convolutional neural network |
| 数据集 | 自建：83个网站，HTTP/HTTPS各10类，3,690,513 flows |
| 代码仓库 | 未开源 |
| 研究方向 | 网站指纹攻击、图神经网络、自监督学习 |
| Confidence | medium |

---

## 1. 一句话总结

> 提出 MRCGCN（多层资源聚合图卷积神经网络），以资源为基本单元构建多层时空图表示，利用阶梯有序图核函数进行自监督聚类标注，通过双通道 GCN 实现无需大量人工标注的网站指纹攻击，在收敛速度、鲁棒性、泛化性和灵活性四个维度全面优于 8 个 SOTA 基线。

---

## 2. 摘要翻译

**原文：**
Deep learning-based website fingerprinting (WF) attacks dominate website traffic classification. In the real world, the main challenges limiting their effectiveness are, on the one hand, the difficulty in countering the effect of content updates on the basis of accurate descriptions of page features in traffic representations. On the other hand, the model's accuracy relies on training numerous samples, requiring constant manual labeling. The key to solving the problem is to find a website traffic representation that can stably and accurately display page features, as well as to perform self-supervised learning that is not reliant on manual labeling. This study introduces the multilevel resource-coherented graph convolutional neural network (MRCGCN), a self-supervised learning-based WF attack. It analyzes website traffic using resources as the basic unit, which are coarser than packets, ensuring the page's unique resource layout while improving the robustness of the representations. Then, we utilized an echelon-ordered graph kernel function to extract the graph topology as the label for website traffic. Finally, a two-channel graph convolutional neural network is designed for constructing a self-supervised learning-based traffic classifier. We evaluated the WF attacks using real data in both closed- and open-world scenarios. The results demonstrate that the proposed WF attack has superior and more comprehensive performance compared to state-of-the-art methods.

**中文翻译：**
基于深度学习的网站指纹（WF）攻击主导着网站流量分类领域。在实际场景中，限制其效果的主要挑战有两方面：一方面，难以在准确描述流量表示中的页面特征基础上对抗内容更新的影响；另一方面，模型准确率依赖于大量样本训练，需要持续的人工标注。解决问题的关键在于找到能够稳定且准确地展示页面特征的网站流量表示，以及执行不依赖人工标注的自监督学习。本研究提出多层资源聚合图卷积神经网络（MRCGCN），一种基于自监督学习的 WF 攻击方法。它以资源为基本单元分析网站流量（比数据包更粗粒度），在确保页面独特资源布局的同时提高表示的鲁棒性。然后，利用阶梯有序图核函数提取图拓扑作为网站流量的标签。最后，设计双通道图卷积神经网络构建基于自监督学习的流量分类器。在闭世界和开世界场景中使用真实数据评估 WF 攻击。结果表明，所提出的 WF 攻击相比 SOTA 方法具有更优越和更全面的性能。

---

## 3. 方法动机

### 3.1 现有痛点

1. **包级特征脆弱**：传统 WF 攻击以数据包为基本单元，生成的特征序列容易受网络环境、传输线路、通信设备等因素干扰产生变形（concept drift），导致分类器老化。
2. **人工标注成本高**：深度学习方法依赖大量标注样本训练，真实世界中网站数量庞大、内容频繁更新，准确标注不可行。
3. **无监督方法精度不足**：基于字符级特征（URL、域名、证书等）的无监督方法在加密场景下不可靠，易被 FFSNs、CDN 等技术破坏映射关系。
4. **已有图方法粒度不够**：GraphDApp 等图学习方法以数据包为节点，图结构随网络环境变化大，鲁棒性不足。

### 3.2 核心直觉

- 网站页面的**资源类型和布局**（CSS、图片、视频、文本等的排列顺序）是网站的内在稳定属性，即使具体内容频繁更新，资源传输顺序仍遵循页面布局。
- 以**资源**为基本单元（比数据包粗粒度）构建流量表示，可以过滤掉细粒度的网络噪声，保留网站的结构性特征。
- **自监督学习**：利用图结构相似性自动为未标注样本生成伪标签，避免大量人工标注。

### 3.3 为什么提出 MRCGCN

- 需要一种既能**稳定描述页面特征**（抵抗 concept drift），又**不依赖人工标注**的 WF 攻击方法。
- 资源级表示比包级表示更鲁棒，但需要新的图构建和学习方法来处理资源间的多层时空关系。

---

## 4. 方法设计

### 4.1 整体流程

```
原始流量 → 资源提取 → 多层时空特征序列(6个) → 图构建(G^[P])
    → 图处理(分区/资源图/池化/扩展) → 图聚类(阶梯有序图核函数+层次聚类)
    → 双通道 GCN(原始图+最大相似子图) → 全连接层 → 分类结果
```

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|------|------|----------|------|------|
| 资源提取 | 原始数据包序列 | 按资源归属组织数据包，识别请求包和响应包 | 资源序列 R | 将包级表示提升为资源级表示 |
| 时空特征构建 | 资源序列 + 流序列 + 主机序列 | 构建6个特征序列：R^[T], R^[S], F^[T], F^[S], H^[T], H^[S] | 6个时空特征序列 W^[T], W^[S] | 多粒度描述客户端-服务器交互 |
| 图构建 | 时空特征序列 | 以资源为节点，6种边（资源/流/主机×时间/空间）连接 | 包级图 G^[P] | 将流量分类转化为图识别问题 |
| 图分区 | G^[P] | 流式分区算法按资源归属切分，节点分区保留数据完整性 | 子图序列 | 支持并行处理大规模图 |
| 资源图构建 | 子图 | 同一资源内所有节点聚合为资源图 RG | 资源图序列 G^[P] = (RG_1, ..., RG_n) | 降低图规模 |
| 图池化 | 资源图 | 3级池化：包→资源→流→主机，保留高层信息 | 多层子图 G^[R], G^[F], G^[H] | 多尺度挖掘流量特征 |
| 图扩展 | 资源图 G^[R] | 添加基于 HTTP 传输机制的流级扩展边（II-type） | 扩展图 G^[R] | 增强同类网站图的相似性 |
| 图聚类 | 资源图空间 | 阶梯有序图核函数逐节点比较图结构，计算相似度 | 聚类结果 + 最大相似子图 | 自动为未标注样本生成伪标签 |
| 双通道学习 | 原始图 + 最大相似子图 | 两个独立通道分别优化，结构+特征融合 | 分类结果 | 增强泛化能力 |

### 4.3 模型模块

| 模块 | 功能 | 输入 | 输出 | 关键设计 |
|------|------|------|------|----------|
| 图构建模块 | 资源级图表示 | 6种时空特征序列 | G^[P]（包级图） | 节点特征包含{长度,时间,方向} + {资源/流/主机编号} + {图深度,资源出度} |
| 图处理模块 | 优化图结构 | G^[P] | 多层资源聚合图 | 流式分区 + 3级层次池化 + 流级扩展边 |
| 图核函数模块 | 计算图相似度 | 两个资源图 | 相似度分数 + 最大相似子图 | 阶梯有序比较，I-type/II-type 边替换 |
| 聚类模块 | 自监督标注 | 图空间 | 聚类标签 + 聚类中心 | 合并层次聚类，终止条件：N_min 或 Delta_min |
| 双通道 GCN | 图分类 | 原始图 + 最大相似子图 | 网站类别 | 层次偏差导向聚合函数，5层GCN，30隐藏单元 |
| HTTP 着色模块 | 协议适配 | HTTP 流量节点 | 增强节点特征 | 注入资源格式γ和类型ε特征 |

### 4.4 关键公式解释

**1. 层次池化函数（Eq.1-9）**

$$G^{[H]} = pool^{[III]}(G^{[F]}) = pool^{[II]}(G^{[R]}) = pool^{[I]}(G^{[P]})$$

节点聚合函数：$v_j^{[l+1]} = \phi(A: v_i^{[l]})$，按归属A将同层节点聚合到上层节点。边更新函数：$E^{[l+1]} = \psi(m: e^{[l]})$。三级池化分别实现包→资源、资源→流、流→主机的聚合。

**2. 阶梯有序图核函数（Eq.10-12）**

$$G_\kappa(G_a, G_b) = \sum_{v_i \in V_a} \sum_{v_j \in V_b} g_\kappa(v_i, v_j)$$

逐层比较两个图的节点，在每层扫描具有相同资源出度的同构节点。当 I-type 边不足时，用 II-type（扩展）边替代。将所有层级的同构节点连接形成最大相似子图。

**3. 图相似度（Eq.13-14）**

$$\Delta(G_a, G_b) = \frac{\sigma_{max}(G_\kappa)}{\sigma(G_a) + \sigma(G_b) - \sigma_{max}(G_\kappa)}$$

使用最大相似子图深度与两图深度之和的比值（类 Jaccard 相似度）。最终相似度为三层加权平均：$\bar{\Delta} = \alpha\Delta_R + \beta\Delta_F + (1-\alpha-\beta)\Delta_H$。

**4. 层次偏差导向聚合函数（Eq.15）**

$$\dot{\eta}_{v_j}^I = \eta_{v_j}^I + \sum_{i \in N(j)} \frac{\eta_{v_i}^I}{\sigma_{v_j} - \sigma_{v_i}}$$

根据节点间的图深度偏差加权聚合 I-type 特征。层次偏差越小，节点关联越强，权重越大。

**5. 分类损失（Eq.16-17）**

$$\hat{y}_{ic} = \text{SoftMax}(MRCGCN(x_i))$$
$$\text{Loss} = -\frac{1}{|X|}\sum_{i=1}^{|X|}\sum_{c=1}^{C} y_{ic} \log(\hat{y}_{ic})$$

标准交叉熵损失 + SoftMax 输出 + ReLU 激活。

### 4.5 训练超参数

| 超参数 | 值 |
|--------|----|
| 优化器 | Adam |
| 激活函数 | ReLU |
| 聚合方法 | 节点特征聚合 |
| 更新方法 | 节点更新 |
| 迭代次数 | 20 |
| 图卷积层数 | 5 |
| 每层隐藏单元 | 30 |
| 每分支图数 | 200 |
| 相似度阈值 | 5%（高于其他类别至少5%） |
| 硬件 | Intel i9-12900K + RTX 3090 + 64GB RAM |

### 4.6 优势

1. **资源级表示鲁棒性强**：以资源为基本单元过滤网络噪声，资源布局是网站的内在稳定属性。
2. **自监督学习减少标注依赖**：图核函数+层次聚类自动生成伪标签，降低人工标注成本。
3. **多层特征融合**：资源/流/主机三个层级的时空特征互补，提升分类精度。
4. **图扩展机制**：基于 HTTP 协议知识添加扩展边，增强同类网站图的结构相似性。
5. **快速收敛**：仅需 15% 训练数据即可达到动态平衡（0.9倍最高值），远快于其他方法。

### 4.7 不足

1. **仅适用于 HTTP/1.1**：HTTP/2.0/3.0 的多路复用机制交织不同资源的数据包，破坏资源级表示，论文在结论中讨论了超图模型作为潜在改进方向。
2. **未开源**：代码未公开，可复现性受限。
3. **数据集规模有限**：仅 83 个网站，与真实互联网规模差距较大。
4. **计算复杂度较高**：图核函数的逐节点比较复杂度为 O(|V_a| * |V_b|)，大规模场景下可能成为瓶颈。
5. **图聚类终止条件依赖先验知识**：需要预设 N_min 或 Delta_min，在未知类别数的场景中不适用。

---

## 5. 与其他方法对比

### 5.1 本质区别

| 维度 | 传统包级方法 (DF, CUMUL等) | 已有图方法 (GraphDApp等) | MRCGCN |
|------|---------------------------|------------------------|--------|
| 基本单元 | 数据包 | 数据包 | 资源 |
| 学习策略 | 监督学习 | 监督学习 | 自监督学习 |
| 鲁棒性 | 弱（包序列易变形） | 中（包级图结构不稳定） | 强（资源布局稳定） |
| 标注需求 | 大量人工标注 | 大量人工标注 | 自动伪标签 |
| 特征粒度 | 包方向/长度 | 包级交互图 | 资源级多层时空图 |

### 5.2 创新点

| 创新点 | 说明 |
|--------|------|
| 资源级多层时空图表示 | 首次以资源为基本单元，构建资源/流/主机三层时空图，6种边类型 |
| 阶梯有序图核函数 | 专为有向层次图设计，逐层扫描同构节点，支持 I-type/II-type 边替换 |
| 自监督聚类标注 | 图核函数计算图相似度 → 层次聚类 → 自动生成伪标签，减少人工标注 |
| 双通道 GCN | 原始图和最大相似子图分别优化后融合，增强泛化能力 |
| 图扩展机制 | 基于 HTTP 协议传输机制添加流级扩展边，增强同类网站图相似性 |
| HTTP 着色模块 | 注入资源格式和类型特征，引导 GCN 关注特殊资源节点 |

### 5.3 Baseline 方法对比表

| 方法 | 学习策略 | 分类器 | 特征类型 | 表示形式 |
|------|----------|--------|----------|----------|
| Robust Fingerprinting (RF) [25] | 监督 | CNN | 包方向序列 | 流量聚合矩阵 TAM |
| GraphDApp [39] | 监督 | GCN | 包长度/方向 | 流量交互图 TIG |
| D-PACK [21] | 无监督 | 1D-CNN+自编码器 | 包载荷 | 灰度图像 |
| IoT-KEEPER (IoT-K) [26] | 无监督 | 模糊C均值聚类 | 包级特征向量 | 特征向量 |
| DCGAN [43] | 半监督 | GAN+CNN | 包长度/到达时间 | 包级特征向量 |
| FS-GAN [45] | 自监督 | GAN | 包载荷 | 包载荷序列 |
| FM-CWFA [35] | 迁移学习 | CNN | 包方向/到达时间 | 包级特征向量 |
| EDRL [46] | 强化学习 | MLP | 包长度 | 包级特征向量 |
| **MRCGCN** | **自监督** | **GCN** | **页面布局/资源时空特征** | **资源聚合表示图** |

---

## 6. 实验表现

### 6.1 实验设置

- **硬件**：Intel Core i9-12900K + GeForce RTX 3090 + 64GB RAM
- **软件**：DGL (Deep Graph Library) 构建 GCN 模型
- **评估场景**：闭世界（83类多分类）+ 开世界（收敛速度/鲁棒性/泛化性/灵活性 4个实验）
- **数据划分**：闭世界 5-fold cross-validation；开世界 10-fold cross-validation

### 6.2 数据集详情

| 协议 | 类别数 | 总 Flows | 采集时长 | 代表网站 |
|------|--------|----------|----------|----------|
| HTTP | 10类 | 2,032,942 | 8-63天 | people.com.cn, jd.com, 4399.com 等 |
| HTTPS | 10类 | 1,657,571 | 14-32天 | tmall.com, youtube.com, github.com 等 |

- 83个网站，每站 500-4000 次访问
- 每次浏览记录所有 HTTP/HTTPS 流量作为样本（非单流）
- 每站可能连接 1-5 个 IP、3-10 个域名、5-20 个流、传输 20-50 个资源文件

### 6.3 评估指标

- **闭世界**：Macro Accuracy (Macro_AC), Macro Precision (Macro_PR), Macro Recall (Macro_RC), Macro F1 (Macro_F1)
- **开世界**：收敛速度（达到0.9倍最高值所需数据量）、鲁棒性（跨时间段准确率衰减）、泛化性（逐步增加网站类型的准确率变化）、灵活性（自动识别未知类别能力）

### 6.4 关键结果

**闭世界多分类结果（83类）：**

| 方法 | Macro_AC | Macro_PR | Macro_RC | Macro_F1 |
|------|----------|----------|----------|----------|
| RF [25] | 0.84 | 0.81 | 0.84 | 0.82 |
| RF+ [25] | 0.86 | 0.83 | 0.85 | 0.84 |
| IoT-K [26] | 0.90 | 0.87 | 0.91 | 0.86 |
| GraphDApp [39] | 0.98 | 0.97 | 0.91 | 0.89 |
| D-PACK [21] | 0.99 | 0.98 | 0.97 | 0.98 |
| DCGAN [43] | 0.55 | 0.56 | 0.48 | 0.51 |
| EDRL [46] | 0.72 | 0.78 | 0.73 | 0.76 |
| FS-GAN [45] | 0.78 | 0.79 | 0.76 | 0.78 |
| **MRCGCN** | **0.93** | **0.92** | **0.95** | **0.94** |

注：D-PACK+ 在闭世界中达到最高 0.98 Macro_AC，但其依赖 URL/域名/证书等字符级特征，网站更新后易失效。MRCGCN 在综合性能上更优。

**时间消耗对比：**

| 方法 | 表示构建时间 Trc(s) | 推理时间 Tri(s) | 总时间 Ttc(s) |
|------|---------------------|-----------------|---------------|
| D-PACK+ | 136,825 | 85,846 | 222,671 |
| FS-GAN+ | 231,868 | 45,050 | 276,918 |
| RF+ | 786,472 | 141,984 | 928,456 |
| **MRCGCN** | **189,712** | **869,766** | **1,059,478** |
| EDRL+ | 893,648 | 350,429 | 1,244,077 |
| FM-CWFA+ | 1,408,264 | 530,934 | 1,939,198 |
| GraphDApp+ | 2,015,972 | 705,950 | 2,721,922 |
| DCGAN+ | 1,754,862 | 1,179,888 | 2,934,750 |

MRCGCN 的表示构建时间（Trc）接近第一梯队（D-PACK+, FS-GAN+），得益于多流处理和图分区并行化。推理时间较高，主要来自图核函数的逐节点比较。

**消融实验（Table V）：**

| 层级组合 | Macro_AC | Macro_PR | Macro_RC | Macro_F1 |
|----------|----------|----------|----------|----------|
| 仅资源层 | 0.7354 | 0.6985 | 0.7215 | 0.7098 |
| 资源+流层 | 0.8683 | 0.8421 | 0.8598 | 0.8509 |
| 资源+主机层 | 0.7934 | 0.7798 | 0.8124 | 0.7958 |
| MRCGCN（全部） | 0.9315 | 0.9199 | 0.9465 | 0.9395 |

资源层贡献最大（0.7354），流层提升 18.07%，主机层提升 7.89%，三层融合达到最优。

### 6.5 开世界实验关键发现

| 实验 | 关键发现 |
|------|----------|
| 收敛速度 | MRCGCN 仅需 3 次数据添加（15%数据）达到动态平衡，D-PACK+ 和 DCGAN+ 需 30% |
| 鲁棒性 | MRCGCN 在多个时间段保持 >0.9 准确率；50天采集的网站仍保持 0.75 准确率，衰减最慢 |
| 泛化性 | MRCGCN 随网站类型增加准确率下降最慢，在约 1/3 处进入平台期，最终逼近闭世界性能 |
| 灵活性 | MRCGCN 在第14轮测试即完成全部样本分类，是所有方法中最早完成的 |

### 6.6 优势场景

1. **需要快速部署的场景**：自监督学习仅需少量标注数据即可达到高准确率
2. **长期监控场景**：资源布局稳定性使分类器抗 concept drift 能力强，50天后仍保持 0.75 准确率
3. **大规模自动化场景**：无需人工标注，可自动识别未知网站类别
4. **HTTP/HTTPS 混合环境**：同时支持明文 HTTP 和加密 HTTPS 流量分类

### 6.7 局限性

1. **不支持 HTTP/2.0/3.0**：多路复用机制交织不同资源数据包，破坏资源级表示，论文建议使用超图模型改进
2. **闭世界准确率非最高**：D-PACK+ (0.98) 和 GraphDApp+ (0.99) 在闭世界中更高，但 MRCGCN 在综合性能上更优
3. **推理时间较长**：图核函数逐节点比较复杂度高，Tri=869,766s，是 D-PACK+ 的 10 倍
4. **数据集规模有限**：仅 83 个网站，未覆盖更多类型和更大规模场景
5. **代码未开源**：无法复现和直接应用

---

## 7. 消融实验分析

### 7.1 层级贡献消融（Table V）

| 消融配置 | Macro_AC | 与完整版差距 | 提升比例（相对仅资源层） |
|----------|----------|-------------|------------------------|
| 仅资源层 | 0.7354 | -0.1961 | 基准 |
| 资源+流层 | 0.8683 | -0.0632 | +18.07% |
| 资源+主机层 | 0.7934 | -0.1381 | +7.89% |
| 完整 MRCGCN | 0.9315 | 0 | +26.66% |

**分析：** 资源层是核心贡献，提供基础的页面布局特征。流层提供更细粒度的资源间时空关系，提升最大。主机层提供跨服务器的宏观关联，提升较小但仍有价值。三层特征互补，融合后达到最优。

### 7.2 基线方法优化对比

论文对所有基线方法进行了多流优化（图中带"+"标记），并使用 stacking 模型 + 投票算法集成结果。优化后的基线方法性能均有提升，但 MRCGCN 仍全面优于所有优化后的基线。

---

## 8. 与已有方法的关系

### 8.1 继承的工作

| 已有工作 | 关系 | 说明 |
|----------|------|------|
| GraphDApp [39] | 继承+改进 | 继承图学习框架，但从包级图提升为资源级多层图 |
| RK-HSTGCN [40] | 继承+改进 | 同一作者组的前序工作，引入资源知识驱动图表示，MRCGCN 进一步引入自监督学习 |
| STC-WF [51] | 参考 | 参考其流间时空关联图的思想 |

### 8.2 对领域发展的贡献

- 首次将**资源级表示**引入 WF 攻击，为后续工作提供了新的特征工程思路
- 证明了**自监督学习**在 WF 任务中的可行性，减少对人工标注的依赖
- 提出的**阶梯有序图核函数**可推广到其他具有层次结构的图比较任务

---

## 9. 证据记录

| 关键观点 | 论文依据 | 位置 |
|----------|----------|------|
| 资源传输顺序遵循页面布局，是稳定内在特征 | "the resource transmission order consistently follows the page layout, representing a unique and stable intrinsic feature for each website" | §III.A |
| Alexa top 100,000 网站每日波动 <1% | "the daily fluctuation for the top 100,000 websites on statistical platforms like Alexa is less than 1%" | §III.A (引用 imec-DistriNet [49]) |
| MRCGCN 收敛速度最快 | "MRCGCN has the fastest convergence speed, requiring only three data additions to reach dynamic equilibrium" | §V.F.1 |
| 50天后仍保持 0.75 准确率 | "it maintained a classification accuracy of 0.75, with some websites being captured over 50 days" | §V.F.2 |
| 不支持 HTTP/2.0/3.0 | "the increasing adoption of HTTP/2.0 and HTTP/3.0 introduces multiplexing mechanisms that interleave packets from different resources" | §VI |
| 资源层贡献最大 | 资源层单独 Macro_AC=0.7354，占完整版 78.9% | §V.E (Table V) |

---

## 10. 相关概念与知识连接

### 10.1 相关概念

- [[website-fingerprinting]]：本文的核心任务领域
- [[graph-neural-network]]：本文使用 GCN 作为分类器架构
- [[encrypted-traffic-analysis]]：本文处理加密 HTTPS 流量

### 10.2 相关方法

- [[survey-website-fingerprinting]]：本文 Table I 综述了现有 WF 攻击的分类体系

### 10.3 与已有 Claims 的关系

| 已有 Claim | 本论文的关系 | 位置 |
|------------|-------------|------|
| DL-based WF 攻击优于传统 ML | 支撑：MRCGCN (GCN) 优于 RF (CNN)、IoT-K (聚类) 等传统方法 | §V.E |
| 图学习在流量分析中有效 | 扩展：从包级图提升为资源级多层图，效果显著提升 | §V.E (消融实验) |
| 自监督学习可替代监督学习 | 支撑：自监督 MRCGCN 在开世界场景中优于监督方法 | §V.F |

---

## 11. 开放问题与后续方向

### 11.1 本文遗留的问题

- HTTP/2.0/3.0 多路复用场景下的资源级表示如何构建？论文提出超图模型作为方向但未实现
- 图核函数的计算效率如何提升？当前逐节点比较复杂度高
- 在更大规模（数千/数万网站）场景下的可扩展性如何？

### 11.2 潜在改进方向

- **超图模型**：处理 HTTP/2.0/3.0 中一个数据包属于多个资源的情况
- **图注意力机制**：替代固定权重的层次偏差聚合，学习更优的节点重要性
- **增量学习**：支持新网站类型的在线学习，无需重新训练整个模型
- **图神经网络架构搜索**：自动搜索最优的 GCN 层数、隐藏单元数等超参数

---

## 12. 原始资料链接

- PDF：IEEE Xplore (DOI: 10.1109/TIFS.2024.3520014)
- MinerU Markdown：`02-parsed-markdown/2024-TIFS-Multi-Level_Resource-Coherented_Graph_Learning_for_Website_Fingerprinting_Attacks.md`
- 代码仓库：未开源

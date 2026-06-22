---
type: paper
title_original: "A Two-Phase Approach to Fast and Accurate Classification of Encrypted Traffic"
title_cn: "一种快速准确分类加密流量的两阶段方法"
authors:
  - Yipeng Wang
  - Huijie He
  - Yingxu Lai
  - Alex X. Liu
year: 2023
venue: "IEEE/ACM TON 2023"
doi: "10.1109/TNET.2022.3209979"
url: unknown
pdf: ""
mineru_md: "02-parsed-markdown/2023-TON-A_Two-Phase_Approach_to_Fast_and_Accurate_Classification_of_Encrypted_Traffic.md"
status: processed
reading_level: L2
dataset:
  - Dataset-TLS (28 Android apps, self-collected)
  - Dataset-TLS-QUIC (5 Google QUIC apps, public)
code: "https://github.com/autotab/TaTic"
relevance: medium
research_area: ["加密流量分类", "早期分类", "机器学习"]
task: ["加密流量早期分类", "应用识别", "TLS/QUIC流量分类"]
method: ["两阶段分类", "决策树/极限树集成", "TCN", "Bagging"]
created: 2026-06-21
updated: 2026-06-21
---

# A Two-Phase Approach to Fast and Accurate Classification of Encrypted Traffic

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | A Two-Phase Approach to Fast and Accurate Classification of Encrypted Traffic |
| 中文标题 | 一种快速准确分类加密流量的两阶段方法 |
| 作者 | Yipeng Wang, Huijie He, Yingxu Lai, Alex X. Liu |
| 年份 | 2023（2022年9月接收，2023年6月出版） |
| 会议/期刊 | IEEE/ACM Transactions on Networking (TON) |
| 研究方向 | 加密流量早期分类 |
| 任务类型 | TLS/QUIC加密流量分类、移动应用识别 |
| 方法关键词 | 两阶段分类、Easy/Hard流分流、决策树集成、TCN、Average Waiting Time优化 |
| 数据集 | Dataset-TLS（28个Android应用，自采）、Dataset-TLS-QUIC（5个Google QUIC应用，公开） |
| 是否开源 | 是（https://github.com/autotab/TaTic） |
| PDF | — |
| MinerU Markdown | `../02-parsed-markdown/2023-TON-A_Two-Phase_Approach_to_Fast_and_Accurate_Classification_of_Encrypted_Traffic.md` |

---

## 1. 一句话总结

> 提出TaTic两阶段加密流量分类方法：第一阶段用前4个包快速判断"easy flow"并直接分类（约85.7%的流），第二阶段用TCN对"hard flow"进行精细分类，在保持97.58%准确率的同时将平均等待时间从6.38秒降至1.66秒。

---

## 2. 摘要翻译

### 2.1 摘要原文

Encryption technology has been widely used in today's network communications. The early classification of encrypted flows is of great value to the control, allocation and management of resources in TCP/IP networks. In this paper, we propose TaTic, an early classification method for encrypted traffic, which aims to reduce the time spent observing the encrypted flows to be classified, and at the same time ensure the flow classification accuracy. TaTic is based on our key observation that the majority of encrypted flows can be classified accurately using only the first few packets, and we call such flows "easy flows", whereas the rest of encrypted flows requires more packets for fine-grained analysis to achieve accurate traffic classification, and we call such flows "hard flows". Given an encrypted flow, in the first phase, we use only the first few packets to quickly determine whether it is an easy flow or a hard flow; if it is an easy flow, we directly classify it in this phase; otherwise, we use more packets to perform traffic classification in the second phase. Therefore, we can greatly reduce the time spent in observing the flows without sacrificing the classification accuracy. Our experimental results show that TaTic can greatly reduce the unnecessary time spent in observing the flow to be classified, and at the same time ensure high classification accuracy. We compare our experimental results of TaTic with four existing methods. TaTic is superior to the existing methods in terms of both classification accuracy and average waiting time.

### 2.2 摘要中文翻译

加密技术已广泛应用于当今网络通信中。加密流的早期分类对TCP/IP网络中的资源控制、分配和管理具有重要价值。本文提出TaTic，一种加密流量的早期分类方法，旨在减少观察待分类加密流所需的时间，同时保证分类精度。TaTic基于一个关键观察：大多数加密流仅使用前几个数据包即可准确分类，称之为"easy flow"；其余加密流需要更多数据包进行细粒度分析才能准确分类，称之为"hard flow"。给定一个加密流，第一阶段仅用前几个数据包快速判断其为easy flow还是hard flow；如果是easy flow，直接在该阶段完成分类；否则在第二阶段使用更多数据包进行分类。实验结果表明，TaTic在保证高分类精度的同时大幅减少了不必要的等待时间，与四种现有方法相比，在分类精度和平均等待时间上均表现优越。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

加密流量分类中，高精度和高速度（低延迟）两个目标存在天然矛盾：观察的数据包越多，分类越准确，但等待时间越长。现有方法对所有流采用统一的观察窗口，导致部分本可早期分类的流被不必要地延迟。

### 3.2 现有方法的痛点和不足

| 方法类别 | 代表方法 | 核心局限 |
|---|---|---|
| 流统计特征方法 | [9]-[12] | 需要观察完整双向流才能形成统计量，无法用于早期分类 |
| 流序列特征方法（传统ML） | FOSM, SOB, MaMPF | 对所有流使用固定窗口N，N太小则部分流分类不准，N太大则产生不必要等待 |
| 深度学习方法 | FS-Net, RBRN, SMC | 同样使用固定包数（如16包），对所有流一视同仁，无法自适应调整观察窗口 |

### 3.3 论文的研究假设或核心直觉

核心直觉：加密流量中存在明显的"易分类"和"难分类"之分——大多数流仅凭前几个数据包的特征就能准确分类，只有少数流需要更多数据包的时序信息。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 加密流量中，不同流的分类难度差异很大，部分流仅需少量包即可判断 | §I-B, §I-C |
| 痛点提炼 | 现有方法对所有流使用固定窗口，导致"easy flow"被不必要地延迟观察 | §I-B |
| 问题转化 | 如何自适应地为每条流分配最小观察窗口，同时保持分类精度？ | §I-C |
| 文献定位 | 现有工作主要关注提高分类精度，很少关注减少分类等待时间 | §II-C |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 大部分加密流（>80%）是"easy flow"，仅用前4个包即可准确分类 | §I-C关键观察 | 实验：Cov=85.73%, AoC=99.13% |
| 辅助假设 | 剩余"hard flow"可通过更长的payload长度序列+TCN准确分类 | §III-B设计动机 | 实验：hard flow精度87.87% |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | 85.72%的流被easy flow模型以99.13%精度分类 | §V-E |
| 辅助假设 | 支撑 | hard flow分类精度87.87%，整体精度97.58% | §V-E |

---

## 4. 方法设计

### 4.1 方法整体流程

TaTic包含两个模块：训练模块和分类模块。训练模块构建easy flow分类模型（基于决策树集成）和hard flow分类模型（基于TCN）。分类模块先用easy flow模型快速判断并分类easy flow，再用hard flow模型处理剩余流。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Short-sequence Preprocessing | 标注流的前h个包 | 提取payload length、TCP window size、interval time三个特征，形成3h维特征向量 | D_easy特征集 | 构建easy flow训练数据 |
| Short-sequence Trainer | D_easy | Bagging采样(α=0.632)→构建T棵分类树→从纯度=0的叶节点生成规则集 | EFC-Model (规则集集合) | easy flow分类模型 |
| Long-sequence Preprocessing | 标注流的前H个包 | 提取payload length序列（仅用payload length，不用window size和interval time） | D_hard特征集 | 构建hard flow训练数据 |
| Long-sequence Trainer | D_hard | One-hot编码→2D卷积→TCN(L层残差块，膨胀卷积)→全连接分类 | HFC-Model | hard flow分类模型 |
| Phase 1 分类 | 新流的前h个包 | EFC-Model输出T个标签，若≥T*P个规则集预测相同标签则直接分类 | 应用标签或"-1" | 快速分类easy flow |
| Phase 2 分类 | hard flow的前H个包 | HFC-Model进行分类 | 应用标签 | 精细分类hard flow |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| EFC-Model（Easy Flow Classification） | 快速判断easy/hard flow并分类easy flow | 前h个包的3h维特征 | 应用标签或"hard"标记 | 输出hard flow给HFC-Model |
| HFC-Model（Hard Flow Classification） | 精细分类hard flow | 前H个包的payload length序列 | 应用标签 | 接收EFC-Model无法分类的流 |

### 4.4 公式、算法和机制解释

**时间间隔离散化（公式1）**：将连续时间间隔转换为离散值，使用阶梯函数：
- 0s~0.1s: floor(t*100)+1
- 0.1s~1s: floor(t*200)+1
- >=1s: floor(t*1000)+1

**EFC-Model投票机制**：T个规则集各自投票，若≥T*P个规则集预测同一标签，则该流为easy flow并输出该标签；否则标记为hard flow（输出"-1"）。

**HFC-Model TCN结构**：
- One-hot编码层：将payload length转换为d维稀疏向量
- 2D卷积层：C0个(1,d)滤波器，恢复为C0×H张量
- TCN：L个残差块串联，每块含膨胀卷积（dilation rate=2^(r-1)）、权重归一化、裁剪、ReLU、Dropout
- 分类层：两层全连接（64→R），softmax激活

**AWT计算（公式10-11）**：
- AWT_r = Cov_r * t'_r + (1-Cov_r) * t''_r
- AWT = mean(AWT_r)
- 其中t'_r为easy flow阶段等待时间，t''_r为hard flow阶段等待时间

### 4.5 方法优势

1. **自适应窗口**：不同流使用不同观察窗口，而非一刀切的固定窗口
2. **低延迟**：约85.7%的流仅需4个包（AWT=0.68s）即可完成分类
3. **高精度**：整体精度97.58%，easy flow精度99.13%
4. **计算高效**：单树分类约6μs，hard flow模型约11.6μs
5. **可扩展**：tree-based方法可直接引入更多特征，无需重新设计模型

### 4.6 方法不足

1. **同公司应用混淆**：同一公司的应用（如Baidu的BaiduSearchbox和Baidumap）容易互相混淆，约4.2%的Baidumap流被误分为BaiduSearchbox
2. **hard flow精度偏低**：hard flow的分类精度仅87.87%，与easy flow的99.13%差距较大
3. **训练集局限**：仅用28个Android应用，且通过UI fuzzing采集，可能无法覆盖真实用户行为的多样性
4. **静态参数**：h=4和H=16是固定选择，未探索动态调整的可能性
5. **特征设计依赖经验**：easy flow用3个特征、hard flow仅用payload length的选择基于经验观察，缺乏理论分析

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

现有方法（SMC、FS-Net、RBRN、ETC-PS）对所有流使用**固定窗口**（如12或16个包），而TaTic根据流的分类难度**自适应分配**观察窗口：easy flow用4个包，hard flow用16个包。这是"分流+分治"策略在流量分类中的首次应用。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| Easy/Hard流分流 | 将加密流分为easy flow和hard flow两类，分别处理 | 高 | 是（任何序列分类任务） |
| 两阶段自适应分类 | Phase 1快速判断+分类，Phase 2精细分类 | 高 | 是 |
| Bagging规则集投票 | 多棵决策树生成规则集，投票决定easy/hard | 中 | 是 |
| AWT优化目标 | 以平均等待时间而非单纯准确率为优化目标 | 中 | 是 |

### 5.3 适用场景

- 需要**实时或近实时**加密流量分类的网络管理场景
- QoS策略实施需要快速判断应用类型
- 网络异常检测需要低延迟流量分类
- TLS和QUIC加密流量的移动应用识别

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| SMC | 使用消息序列，考虑TLS协议结构 | 消息长度序列区分度低于包长度序列；AWT=5.16s | AWT降低至1.66s（约1/3），精度提升约28% |
| FS-Net | 编码器-解码器结构，建模能力强 | 固定16包窗口，AWT=6.38s | AWT降低至1.66s（约1/4），精度提升约1.5% |
| RBRN | 端到端CNN，自动特征提取 | 2D CNN擅长局部特征但弱于全局特征；AWT=6.38s | AWT降低至1.66s（约1/4），F-measure提升5.31% |
| ETC-PS | 路径签名特征，理论基础扎实 | 需要16包窗口，AWT=6.38s | AWT降低至1.66s（约26%），F-measure提升2.21% |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- 5折交叉验证，训练:验证:测试 = 60%:20%:20%
- 每个应用类别随机选取5000条流（不足则全取）
- 硬件：Xeon Platinum 2.90GHz CPU + NVIDIA GeForce RTX 3080 GPU

### 6.2 数据集

| 数据集 | 来源 | 应用数 | 流量类型 | 说明 |
|---|---|---|---|---|
| Dataset-TLS | 自采（LG Nexus 5, Android 6.0） | 28个Android应用 | TLS (TCP) | 使用MonkeyRunner UI fuzzing采集 |
| Dataset-TLS-QUIC | 公开（UC Davis, Rezaei et al.） | 5个Google应用 | QUIC (UDP) | Google Doc/Drive/Music/YouTube/Search |

**Dataset-TLS的28个应用**涵盖：社交（Facebook, Instagram, Twitter, LinkedIn, Weibo）、电商（Taobao, JD, Pinduoduo, Vipshop, Eleme, Meituan）、地图（Amap, Baidumap）、搜索（Baidusearchbox）、视频（TikTok, Toutiao）、音乐（NeteaseCloudMusic, Pandora）、旅行（Booking, TripAdvisor, Ctrip, Airbnb）、金融（Alipay, Yirendai）、开发（GitHub）、社区（Reddit, Zhihu）、其他（Blued）。

### 6.3 Baseline

- **SMC** [17]：基于LSTM，使用前6个消息段（约12个包）
- **FS-Net** [16]：基于RNN编码器-解码器，使用前16个包
- **RBRN** [25]：基于2D CNN，使用前16个包
- **ETC-PS** [29]：基于路径签名特征，使用前16个包

### 6.4 评价指标

| 指标 | 定义 | 用途 |
|---|---|---|
| Cov_r / Cov | easy flow覆盖率 | 衡量easy flow模型能分类多少流 |
| AOC_r / AOC | easy flow分类精度 | 衡量easy flow模型分类准确性 |
| F_β (β=3) | Cov和AOC的加权调和平均 | 偏重Cov的综合指标 |
| Recall / Precision / F-measure | 每个应用的标准分类指标 | 衡量整体分类效果 |
| ACC | 所有类别的平均recall | 多分类整体精度 |
| AWT | 平均等待时间 | 衡量分类效率（核心创新指标） |

### 6.5 关键实验结果

| 方法 | 使用包数 | 平均Recall | 平均Precision | 平均F-measure | AWT (s) |
|---|---:|---:|---:|---:|---:|
| SMC | 12 | 69.72% | 70.35% | 69.77% | 5.16 |
| FS-Net | 16 | 96.12% | 96.17% | 96.12% | 6.38 |
| RBRN | 16 | 92.26% | 92.48% | 92.28% | 6.38 |
| ETC-PS | 16 | 95.37% | 95.43% | 95.38% | 6.38 |
| **TaTic** | **4/16** | **97.58%** | **97.62%** | **97.59%** | **1.66** |

**Easy/Hard流细分统计（Table III）**：

| 类型 | Precision | 占比 | 使用包数 | AWT |
|---|---|---|---:|---|
| Easy flow | 99.13% (±0.04) | 85.72% (±0.28) | 4 | 0.68s (±0.01) |
| Hard flow | 87.87% (±0.84) | 14.28% (±0.28) | 16 | 8.04s (±1.25) |
| 平均 | 97.62% (±0.08) | 100% | 5.7 | 1.66s (±0.10) |

**Dataset-TLS-QUIC结果**：整体recall=97.83%, precision=97.85%, F-measure=97.83%，与TLS数据集表现一致甚至略优。

**最优参数**：
- Easy flow模型：h=4, T=30, P=0.8, TA=ExtraTree(Entropy)
- Hard flow模型：H=16, K=15, C=64, L=3

### 6.6 优势最明显的场景

1. **easy flow占比高时**：当85%以上的流是easy flow时，AWT优势最为显著
2. **实时分类场景**：需要低延迟分类的QoS和异常检测场景
3. **跨公司应用区分**：不同公司的应用分类效果很好（对角线矩阵明显）

### 6.7 局限性

1. **同公司应用混淆严重**：BaiduSearchbox vs Baidumap、Taobao vs Eleme vs Amap之间存在明显混淆
2. **数据集规模有限**：仅28个应用，且通过自动化UI fuzzing采集，可能不覆盖真实用户行为
3. **hard flow精度瓶颈**：87.87%的精度意味着约12%的hard flow被错误分类
4. **未考虑网络环境变化**：模型在受控环境下训练，未评估跨网络环境的鲁棒性
5. **仅限移动应用**：未验证对桌面应用、IoT设备等场景的适用性

---

## 7. 学习与应用

### 7.1 是否开源？

是。代码和Dataset-TLS数据集均在 https://github.com/autotab/TaTic 公开。

### 7.2 复现关键步骤

1. 数据采集：使用Android设备+tcpdump+MonkeyRunner UI fuzzing采集TLS流量
2. Easy flow模型训练：提取前4个包的payload length/window size/interval time → Bagging采样 → 构建30棵ExtraTree → 生成规则集 → P=0.8投票阈值
3. Hard flow模型训练：提取前16个包的payload length序列 → One-hot编码 → 2D卷积 → TCN(3层残差块, K=15, C=64) → 全连接分类
4. 测试：Phase 1投票分类easy flow → Phase 2 TCN分类hard flow

### 7.3 关键超参数、预处理和训练细节

| 超参数 | 值 | 说明 |
|---|---|---|
| h (easy flow包数) | 4 | AWT=0.63s时精度已足够高 |
| H (hard flow包数) | 16 | 精度趋于稳定 |
| T (决策树数量) | 30 | Bagging中的树数量 |
| α (采样率) | 0.632 | 632+ Bootstrap方法 |
| P (投票阈值) | 0.8 | 规则集一致性阈值 |
| TA (树算法) | ExtraTree(Entropy) | 最优树构建算法 |
| K (卷积核大小) | 15 | TCN膨胀卷积核大小 |
| C (滤波器数) | 64 | TCN每层滤波器数 |
| L (残差块数) | 3 | TCN深度 |
| d (one-hot维度) | 最大payload length | 离散化维度 |

### 7.4 能否迁移到其他任务？

**可迁移性较高**：
- "分流+分治"的两阶段思想可应用于任何序列分类任务（如恶意流量检测、VPN检测）
- Easy/hard flow的区分思想可迁移到few-shot学习场景
- Bagging规则集投票机制可作为轻量级快速过滤器
- AWT优化目标适用于任何需要低延迟分类的场景

**需要注意**：
- 特征选择（payload length/window size/interval time）是TLS协议特定的
- TCN结构可能需要针对不同协议调整参数

### 7.5 对我的研究有什么启发？

1. **自适应窗口设计**：在加密流量分类中，可以考虑根据流的"难度"动态调整观察窗口，而非使用固定窗口
2. **效率-精度权衡**：AWT是一个有意义的指标，在实际部署中可能比单纯精度更重要
3. **轻量级前置过滤**：用简单模型（决策树）快速过滤"简单"样本，将复杂模型留给"困难"样本，是一种有效的级联分类策略
4. **同公司应用区分**：这是一个公认的难点，可能需要更细粒度的特征（如服务端IP、SNI等）

---

## 8. 总结

### 8.1 核心思想

> 两阶段分流：简单流快速判，复杂流精细分。

### 8.2 速记版 Pipeline

1. 训练阶段：用前4个包特征构建决策树集成（EFC-Model），用前16个包payload序列构建TCN（HFC-Model）
2. Phase 1：新流到来 → 提取前4个包特征 → EFC-Model投票 → 多数一致则直接分类（easy flow）
3. Phase 2：少数不一致的流（hard flow）→ 提取前16个包payload序列 → HFC-Model分类
4. 结果：85.7%的流以0.68s完成分类（99.13%精度），整体AWT=1.66s
5. 对比：精度优于所有baseline（97.58% vs 最高96.17%），AWT仅为baseline的1/3~1/4

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[encrypted-traffic-analysis]]
- [[traffic-classification]]

### 9.2 相关方法

- [[survey-encrypted-traffic-analysis]]

### 9.3 相关任务

- [[encrypted-traffic-analysis]]
- [[traffic-classification]]

### 9.4 可更新的综述页面

- [[survey-encrypted-traffic-analysis]]

### 9.5 可加入的对比表

- [[survey-encrypted-traffic-analysis]]

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 大多数加密流仅需前几个包即可准确分类 | "85.73% of the flows in the validation set are classified by the easy flow classification model, and the average classification accuracy for them is about 99.13%" | §V-C |
| Easy flow用4个包，AWT=0.63s优于5个包的1.03s | "the AW T value of h = 4 is 0.63 seconds, and AW T value of h = 5 rises to 1.03 seconds, that is, the AW T value increases by 63.5%" | §V-C |
| 同公司应用容易混淆 | "about 4.2% of the flows generated by Baidumap are incorrectly classified as BaiduSearchbox" | §V-E.2 |
| TaTic在AWT上优于所有baseline | Table VI: TaTic AWT=1.66s vs others 5.16-6.38s | §VI |
| Payload length比interval time更适合hard flow分类 | "the interval time is greatly affected by the network environment, so the time sequence relationship of the interval time generally does not have a strong degree of discrimination" | §III-B |
| TCN的膨胀卷积可增大感受野而不引入新参数 | "the advantage of the inflated convolutional layer is to increase the reception field without introducing new trainable parameters" | §III-B.2 |

---

## 11. 原始资料链接

- PDF：—
- MinerU Markdown：`../02-parsed-markdown/2023-TON-A_Two-Phase_Approach_to_Fast_and_Accurate_Classification_of_Encrypted_Traffic.md`
- 代码：https://github.com/autotab/TaTic

---

## 12. 后续问题

- Easy/hard flow的分流阈值P是否可以根据网络环境动态调整？
- 在更多应用（如100+应用）的场景下，easy flow占比是否仍然保持在85%以上？
- 同公司应用的混淆问题如何解决？是否需要引入SNI或服务端IP等额外特征？
- 该方法在VPN、Tor等多层加密场景下表现如何？
- AWT指标在实际部署中的意义：1.66秒的等待时间对QoS策略实施是否足够快？

---

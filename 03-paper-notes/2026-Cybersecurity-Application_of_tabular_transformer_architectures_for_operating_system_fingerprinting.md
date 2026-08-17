---
type: paper
title_original: "Application of tabular transformer architectures for operating system fingerprinting"
title_cn: "表格 Transformer 架构在操作系统指纹识别中的应用"
authors:
  - "Rubén Pérez-Jove"
  - "Cristian R. Munteanu"
  - "Alejandro Pazos"
  - "Jose Vázquez-Naya"
year: 2026
venue: "Cybersecurity (Springer)"
doi: "10.1186/s42400-025-00494-y"
url: "https://doi.org/10.1186/s42400-025-00494-y"
pdf: "00-inbox/Aug_inbox/2026-Cybersecurity-Application_of_tabular_transformer_architectures_for_operating_system_fingerprinting.pdf"
mineru_md: "02-parsed-markdown/2026-Cybersecurity-Application_of_tabular_transformer_architectures_for_operating_system_fingerprinting.md"
status: processed
reading_level: L2
research_area:
  - 加密流量分析
  - 流量分类
  - 操作系统指纹识别
task:
  - 操作系统指纹识别（OS fingerprinting）
  - 流量分类
method:
  - TabTransformer（TabT）
  - FT-Transformer（FT-T）
  - 自注意力机制
  - Optuna NSGA-II 超参搜索
  - SMOTE 类别不平衡处理
dataset:
  - DAT1（IPFIX 流量，1870 万行）
  - DAT2（多服务器流量，5 系列/12 家族/50 major/88 minor）
  - DAT3（Nmap 合成流量，7 家族/91 minor）
code: "https://github.com/rubenpjove/tabularT-OSfingerprinting（GNU GPL v3.0；论文内另有带连字符写法 tabularT-OS-fingerprinting，见解析质量标注）"
relevance: medium
created: "2026-08-17"
updated: "2026-08-17"
---

# Application of tabular transformer architectures for operating system fingerprinting

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Application of tabular transformer architectures for operating system fingerprinting |
| 中文标题 | 表格 Transformer 架构在操作系统指纹识别中的应用 |
| 作者 | Rubén Pérez-Jove, Cristian R. Munteanu, Alejandro Pazos, Jose Vázquez-Naya（西班牙，CESGA 超级计算中心） |
| 年份 | 2026（投稿 2025-02-14，接收 2025-09-25，发表 2026-06-10） |
| 会议/期刊 | Cybersecurity (Springer)，DOI: 10.1186/s42400-025-00494-y |
| 研究方向 | 加密流量分析 / 操作系统指纹识别 |
| 任务类型 | 多粒度 OS 指纹识别（family / major / minor 三级） |
| 方法关键词 | TabTransformer、FT-Transformer、自注意力、Optuna NSGA-II、SMOTE |
| 数据集 | DAT1（IPFIX 真实流量）、DAT2（自采多服务器流量）、DAT3（Nmap 合成流量） |
| 是否开源 | 代码开源（GitHub，GNU GPL v3.0）；数据集来源见 §6.1 |
| PDF | 00-inbox/Aug_inbox/2026-Cybersecurity-Application_of_tabular_transformer_architectures_for_operating_system_fingerprinting.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-Cybersecurity-Application_of_tabular_transformer_architectures_for_operating_system_fingerprinting.md |

---

## 1. 一句话总结

> 本文系统评估 TabTransformer（TabT）与 FT-Transformer（FT-T）两种表格 Transformer 在家族/主版本/次版本三级 OS 指纹识别任务上的表现，证明 FT-T 在精度、参数效率（6.6 万–49.6 万参数 vs TabT 的 6580 万–5.2 亿）与推理速度（<0.07 ms/流）上全面优于 TabT，且可通过注意力权重解释分类依据。

---

## 2. 摘要翻译

### 2.1 摘要原文

> Operating system (OS) fingerprinting is a critical task in network security and management, enabling the identification of devices connecting to a network. Traditional OS fingerprinting techniques are often based on active probing methods, such as Nmap, which can be intrusive and generate unwanted traffic. In this work, we explore the application of tabular transformer architectures to passive OS fingerprinting, using network traffic data to identify the OS without requiring active probing. We evaluate two state-of-the-art tabular transformer models, TabTransformer and FT-Transformer, on three different datasets of varying complexity and feature types, and compare them with traditional machine learning models and deep learning baselines. Our results show that FT-Transformer consistently outperforms TabTransformer and other baselines in most scenarios, achieving high accuracy and F1-score, while maintaining a much lower parameter count and faster inference times. We also demonstrate the interpretability of these models, showing that they can highlight the most relevant features for OS identification, and their robustness to noise, being able to maintain high performance under noisy conditions. Our findings suggest that tabular transformers, and particularly FT-Transformer, are a promising approach for passive OS fingerprinting, with significant implications for network security and management.

### 2.2 摘要中文翻译

> 操作系统（OS）指纹识别是网络安全与管理中的关键任务，可用于识别接入网络的设备。传统 OS 指纹识别技术多基于主动探测方法（如 Nmap），具有侵入性并会产生不必要的流量。本文探索将表格 Transformer 架构应用于被动式 OS 指纹识别，仅利用网络流量数据即可识别操作系统，无需主动探测。作者在三个复杂度和特征类型各异的真实/合成数据集上评估了两种最先进的表格 Transformer 模型（TabTransformer 与 FT-Transformer），并与传统机器学习模型和深度学习基线对比。结果表明，FT-Transformer 在多数场景下稳定优于 TabTransformer 及其他基线，在获得高准确率与 F1 分数的同时，参数数量低得多、推理速度更快。论文还展示了模型的可解释性（能突出对 OS 识别最重要的特征）以及对噪声的鲁棒性（在噪声条件下保持较高性能）。作者认为表格 Transformer（尤其是 FT-Transformer）是被动式 OS 指纹识别中颇具前景的方法，对网络安全与管理有重要意义。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

作者认为被动式 OS 指纹识别需要兼顾三点：不产生额外探测流量（免主动探测）、在多样化网络数据上保持高精度、以及部署成本可控。表格 Transformer（TabT / FT-T）在通用表格数据上已展现竞争力，但尚无人将其系统应用于 OS 指纹识别——本文填补这一空白。

### 3.2 现有方法的痛点和不足

| 痛点 | 具体表现 |
|---|---|
| 主动探测的侵入性 | Nmap 等主动方法向目标发送探测包，产生额外流量，可能被入侵检测系统告警或触发目标防御 |
| 传统被动方法精度有限 | 基于规则/启发式的被动指纹（如 TCP 窗口大小、TTL 组合）在流量多样化、操作系统碎片化（多版本共存）时区分能力弱 |
| 深度模型代价高 | 现有深度基线（LSTM/MLP）要么忽略表格特征的类别-数值混合结构，要么参数量巨大难以实时部署 |
| 可解释性缺失 | 多数深度模型黑盒化，难以说明"依据什么特征判定 OS"，不利于安全运营信任与审计 |

### 3.3 论文的研究假设或核心直觉

表格型数据中类别特征与数值特征并存，Transformer 的自注意力机制可以在类别嵌入之间建模交互关系（TabT 的列间注意力），或对全部特征进行上下文建模（FT-T 的 Feature Tokenizer），从而比"类别特征独热后丢给树模型/MLP"的传统做法更能捕获特征组合模式——该直觉在通用表格基准上已被验证，作者假设其在 OS 指纹识别任务上同样成立且可解释、可部署。

### 3.4 问题发现路径

> 追溯作者如何从现象/痛点一步步转化为可研究的科学问题。

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 网络流量中 OS 信息对安全运营（资产管理、异常检测、攻击面评估）很重要，但主动探测手段（Nmap）有侵入性且产生额外流量 | §1（引言） |
| 痛点提炼 | 被动式识别依赖的规则特征在多 OS 版本并存、流量多样化的现实网络中区分能力不足；深度模型参数量大、不可解释 | §1、§2（相关工作） |
| 问题转化 | 将"如何无侵入、可解释、可部署地识别 OS"转化为"表格 Transformer 能否在异构表格流量特征上达到优于经典 ML/DL 基线的多粒度识别精度"这一可量化科学问题 | §1、§3（方法） |
| 文献定位 | 表格 Transformer 在通用表格基准上已优于传统 ML，但尚无研究将其用于被动 OS 指纹识别；该任务同时具有类别-数值混合特征、类不平衡、多粒度标签（family/major/minor）等挑战，是未被系统评估的应用场景 | §2（相关工作），推断 |

### 3.5 科学假设形成

> 论文提出了什么可验证的科学假设？该假设如何从 3.4 的问题推导而来？

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | FT-Transformer 在 OS 指纹识别（family/major/minor 三级）上优于 TabTransformer 及经典 ML/DL 基线，同时保持低参数与高推理速度 | 表格 Transformer 在通用基准上的优势 + FT-T 对全部特征统一建模 | 三个数据集 × 三级粒度的分类实验（Table 7-9） |
| 辅助假设 1 | 类别特征对 OS 识别贡献大于数值特征 | 特征稀疏性分析 + 消融实验设计 | Table 13 消融（cat-only vs num-only） |
| 辅助假设 2 | 模型注意力集中在少数协议特征（TLS 扩展、TCP SYN 字段）上，具有可解释性 | Transformer 注意力权重可读 | 注意力权重可视化（§6.5） |
| 辅助假设 3 | 模型对特征噪声鲁棒，适合真实网络环境 | 高斯噪声对抗实验 | Table 14 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | FT-T 在 DAT1-family、DAT2-major/minor、DAT3-family 均最优；DAT2-family 仅以微小差距次于 RF（95.04 vs 95.35） | §4.2（Table 7-9） |
| 辅助假设 1 | 支撑 | DAT2-major 消融：cat-only 68.99 vs num-only 60.20，类别特征贡献更大 | §4.2（Table 13） |
| 辅助假设 2 | 支撑 | 注意力集中于 TLS 扩展长度/类型/椭圆曲线（>一半权重）与 SYN 字段 | §4.3（可解释性） |
| 辅助假设 3 | 部分支撑 | α=0.5 噪声下 ACC 从 78.90 降至 71.40（-9.5%），仍优于全部经典基线 | §4.3（Table 14） |

---

## 4. 方法设计

### 4.1 方法整体流程

- **输入**：每个网络流/会话的表格化特征向量（IPFIX 字段或自定义提取特征），含类别特征与数值特征。
- **处理**：数据预处理（缺失值、去零方差、去重、标签归一、十六进制字节拆分、独热）→ 类别不平衡处理（随机欠采样 + SMOTE）→ 分层划分（80% 训练 / 20% 测试）→ Optuna NSGA-II 超参搜索（Stratified 10 折交叉验证）→ 训练 TabT / FT-T（AdamW，early stopping）→ 推理。
- **输出**：OS 家族（family）、主版本（major）、次版本（minor）三级分类结果，以及注意力权重可视化。

### 4.2 详细 Pipeline

| 阶段 | 具体操作 | 关键细节 |
|---|---|---|
| 数据采集 | DAT1：Masaryk 大学 Eduroam 无线网络 IPFIX 流量（2019-07-12 至 16，Crypto-PAn 匿名化），18,708,983 行 / 29 特征 / 5 家族；DAT2：作者自建 5 台服务器托管 475 域名 8 小时流量，109,663 行 / 112 特征 / 12 家族 / 50 major / 88 minor；DAT3：Nmap 7.94 OSdb 生成的合成流量（16 类探测），38,817 行 / 263 特征 / 7 家族 / 91 minor | 论文 §3；DAT2/DAT3 由作者自行采集或合成 |
| 预处理 | NaN：类别特征补缺失类、数值特征删行；去零方差列；去重；正则表达式映射标签别名；十六进制特征拆为单字节列；One-Hot 编码 | 论文 §3.2 |
| 类别平衡 | 随机欠采样 + SMOTE（auto），并对少数类施加类别权重 | 论文 §3.2 |
| 数据划分 | 分层抽样，20% 测试集 | 论文 §3.2 |
| 超参搜索 | Optuna NSGA-II 多目标优化 + Stratified 10 折 CV；搜索空间：lr [1e-4, 1e-1]、嵌入维度 [16, 32]、深度 [2, 6]、注意力头 [2, 8]、attn/ff dropout [0.05, 0.5]；200 epochs、batch 128/256/512、early stopping 15、AdamW | 论文 §3.4 |
| 模型训练 | TabT：类别特征嵌入 + 列间自注意力 + MLP 头；FT-T：Feature Tokenizer 将全部特征嵌入后过 Transformer 编码器 + 分类头 | 论文 §3.3 |
| 推理 | 单流预测 + 阈值告警（"Windows server" 检测） | 论文 §4.4 |

### 4.3 模型结构

- **TabTransformer（TabT）**：仅对类别特征做嵌入并施加自注意力（建模类别列间交互），数值特征直接拼接至注意力输出后送入 MLP。参数量大（6580 万–5.2 亿）是其主要缺点。
- **FT-Transformer（FT-T）**：Feature Tokenizer 将每个特征（含数值）独立嵌入为 token，经标准 Transformer 编码器建模全部特征交互，最后取 [CLS] 或池化表示分类。参数量 6.6 万–49.6 万，远小于 TabT。
- **Baseline 模型**：RF、kNN、MLP、LSTM（深度基线）、DT（先前工作对比用）。

---

## 5. 与其他方法对比

### 5.1 对比的 Baseline 与指标

- **指标**：Accuracy（ACC）、macro F1-score。
- **Baseline**：Random Forest、kNN、MLP、LSTM、Decision Tree（先前工作），以及 TabTransformer 自身。

### 5.2 表格 Transformer vs 经典 ML

| 任务 | 最优模型 | 关键差距 |
|---|---|---|
| DAT1 family（29 特征） | FT-T（90.69/90.80） | 优于 RF（88.42/87.93）与 MLP（89.96/89.45）；kNN 仅 59.28 |
| DAT2 family（112 特征） | RF 略胜（95.35/95.33） | FT-T 95.04/95.09 次之；论文解释为高维稀疏特征下树模型优势 |
| DAT3 family（263 特征） | FT-T（92.35/92.23） | 仅略胜 MLP（91.65/91.62） |

### 5.3 表格 Transformer vs 深度基线

| 对比项 | 结论 |
|---|---|
| 精度 | FT-T 在 DAT1 上以 90.80 F1 大幅领先 LSTM 的 76.87（+约 14 分）；TabT 全面落后于 FT-T（如 DAT2-major：79.32 vs 74.99 F1） |
| 参数量 | FT-T 6.6 万–49.6 万 vs TabT 6580 万–5.2 亿（DAT2-family 差距约 2300 倍） |
| 训练/推理 | FT-T 训练 <5 分钟（CPU，除 DAT3-minor 25m51s）；推理 <0.07 ms/流（1.4 万–3.2 万 流/秒）；TabT 慢约一个数量级 |

### 5.4 与先前工作对比（Table 10）

| 任务 | 本文 | 先前工作 | 提升 |
|---|---|---|---|
| DAT1 family | FT-T 90.80 F1 | DT 78.96 | +约 12 分 |
| DAT2 family | FT-T 95.09 F1 | DT 81.60 | +约 13.5 分 |
| DAT2 minor | FT-T 68.52（完整 88 类） | Lastovicka 等 32 类 | 本文标签更细、更严格 |

---

## 6. 实验表现

### 6.1 数据集

| 数据集 | 规模 | 特征数 | 标签粒度 | 来源 |
|---|---|---|---|---|
| DAT1 | 18,708,983 行 | 29 | 5 家族 | Masaryk 大学 Eduroam IPFIX 真实流量（2019-07，Crypto-PAn 匿名化） |
| DAT2 | 109,663 行 | 112 | 12 家族 / 50 major / 88 minor | 作者自建 5 服务器 × 475 域名 × 8 小时流量 |
| DAT3 | 38,817 行 | 263 | 7 家族 / 91 minor | Nmap 7.94 OSdb 合成流量（16 类探测） |

### 6.2 主要结果

| 任务 | FT-T | TabT | 最优基线 |
|---|---|---|---|
| DAT1 family | 90.69 / 90.80 | 89.20 / 89.46 | RF 88.42 / 87.93；MLP 89.96 / 89.45 |
| DAT2 family | 95.04 / 95.09 | 95.11 / 95.05（略高，统计不显著） | RF 95.35 / 95.33（最优） |
| DAT2 major | 79.09 / 79.32 | 74.46 / 74.99 | RF 82.48（表内最优） |
| DAT2 minor | 68.52 / 69.76 | 67.74 / 68.28 | RF 74.07（表内最优） |
| DAT3 family | 92.35 / 92.23 | 91.27 / 91.25 | MLP 91.65 / 91.62 |
| DAT3 minor | 75.33 / 75.74 | 75.59 / 75.90（最优） | RF 70.69 |

> 注：DAT2 的 family/major/minor 上 RF 在多数列略优于 FT-T，论文归因于高维稀疏特征下树模型的固有优势；但 FT-T 在参数与速度上显著占优。数值格式为 ACC / F1。

### 6.3 消融实验（Table 13，DAT2-major）

| 配置 | ACC | 相对 cat+num 的差距 |
|---|---|---|
| 类别 + 数值（完整） | 80.83 | — |
| 仅类别特征 | 68.99 | -11.84 pp |
| 仅数值特征 | 60.20 | -20.63 pp（相对仅类别又 -8.79 pp） |

结论：类别特征与数值特征均有贡献，且类别特征贡献更大。

### 6.4 效率与部署（Table 11-12）

| 项目 | FT-T | TabT |
|---|---|---|
| 参数量 | 6.6 万–49.6 万 | 6580 万–5.2 亿 |
| 训练时间（CPU） | <5 分钟（DAT3-minor 为 25m51s） | 慢约一个数量级 |
| 推理延迟 | <0.07 ms/流 | — |
| 吞吐（DAT2-major） | 桌面 1.7k / CPU 服务器 9.9k / T4 GPU 32,290 流/秒 | — |

经典基线吞吐参考：kNN 675、RF 12,987、MLP 90,909 流/秒（MLP 最快但精度低）。

### 6.5 可解释性与混淆模式

- 注意力权重集中于 TLS 扩展长度/类型/椭圆曲线（占一半以上权重）、TCP SYN 大小、TCP SYN TTL；窗口大小权重很低。
- 混淆模式：Windows Phone vs Windows 10（残留错误中占 23.9%）、iOS vs macOS（14–17%）、BSD-Linux 之间；FT-T 对 "Windows server" 的误报率 ≤0.7%。

### 6.6 对抗鲁棒性（Table 14，高斯噪声 ασ_f 施加于 TCP SYN Size / TCP Win Size / TCP SYN TTL）

| 噪声强度 | ACC | 相对原始下降 |
|---|---|---|
| 原始 | 78.90 | — |
| α=0.05 | 77.60 | -1.3 pp（-1.7%） |
| α=0.10 | 76.10 | -2.8 pp |
| α=0.20 | 74.10 | -4.8 pp |
| α=0.50 | 71.40 | -7.5 pp（-9.5%） |

即使 α=0.5，FT-T 仍优于所有经典基线在原始数据上的表现。

### 6.7 实验环境与复现

- 硬件：CESGA FinisTerrae III 超算（714 个 Xeon 8352Y、157 GPUs、4.36 PFLOPS）及商品级桌面/服务器/T4 GPU 用于吞吐测试。
- 软件：numpy==1.23.0、pandas==2.2.2、scikit-learn==1.5.0、torch==2.3.1、optuna==3.6.1。
- 基金支持：ED431C 2022/46、FPU22/04418 等。

---

## 7. 学习与应用

### 7.1 对流量分析研究的启发

表格 Transformer 是"特征工程 + 树模型"路线与"原始字节 + 深度模型"路线之间的一条中间道路：在已有 IPFIX/特征化数据上即可获得接近最优的精度，且参数与延迟代价远低于序列/图像类深度模型。对加密流量分类、恶意流量检测等同样以表格特征为输入的任务有直接迁移价值。

### 7.2 方法迁移

- FT-T 可用于任何表格化网络流量任务（应用识别、隧道检测、恶意流量分类），其注意力权重可充当特征重要性审计工具。
- Optuna NSGA-II + 分层 10 折 CV 的超参搜索流程可直接复用于其他表格模型。

### 7.3 现实局限

- DAT2 数据由作者自采、DAT3 为 Nmap 合成，真实互联网流量中的标签分布与特征漂移未覆盖；跨网络泛化（跨环境迁移）未评估。
- family/major/minor 三级标签中 major/minor 精度（约 68–79%）仍明显低于 family，细粒度识别尚不实用。

### 7.4 对知识库的补充

OS 指纹识别是"流量分类 → 设备/身份识别"链条上的具体任务，与 app 指纹识别（[[app-fingerprinting]]）互补；本文提供了一种"高精度表格深度学习 + 可解释 + 低开销"的方案样本。

### 7.5 可复现性评估

- 代码开源（GitHub，GPL v3.0），依赖版本锁定，超参搜索空间与数据预处理描述详尽，可复现性较好。
- DAT2/DAT3 数据采集流程可重复（论文 §3.1 描述采集环境），但原始数据包未公开，DAT1 为第三方匿名化数据。

---

## 8. 总结

### 8.1 核心思想

> 表格 Transformer 实现免探测、可解释、低开销的被动 OS 指纹识别。

### 8.2 速记 Pipeline

> IPFIX/表格特征 → 预处理（缺失/去零方差/去重/独热）→ 欠采样+SMOTE → Optuna NSGA-II 搜参（10 折 CV）→ FT-Transformer 训练 → family/major/minor 三级预测 + 注意力解释

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[encrypted-traffic-analysis]]
- [[traffic-classification]]

### 9.2 相关方法

- [[transformer]]
- [[convolutional-network]]（作为对比基线族）

### 9.3 相关任务

- [[app-fingerprinting]]

### 9.4 可更新的综述页面

- [[survey-encrypted-traffic-analysis]]

### 9.5 可加入的对比表

- [[method-comparison-table]]
- [[open-source-registry]]（GPL v3.0 开源条目）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| FT-T 在多数场景优于 TabT 与全部基线 | Table 7-9（ACC/F1） | §4.2 |
| FT-T 参数远小于 TabT（6.6 万–49.6 万 vs 6580 万–5.2 亿） | Table 11 | §4.2 |
| 推理 <0.07 ms/流，T4 上 3.2 万流/秒 | Table 11-12 | §4.2 |
| DAT2-family 上 RF 略优（95.35 vs 95.04），归因于特征稀疏 | Table 8 + 论文讨论 | §4.2 |
| 类别特征贡献大于数值特征（cat-only 68.99 vs num-only 60.20） | Table 13 消融 | §4.3 |
| 注意力集中于 TLS 扩展与 SYN 字段 | 注意力可视化 | §4.3 |
| 高斯噪声 α=0.5 下 ACC 78.90→71.40，仍优于全部经典基线 | Table 14 | §4.3 |
| 与先前工作相比 DAT1 提升约 12 分、DAT2 family 提升约 13.5 分 | Table 10 | §4.4 |

---

## 11. 原始资料链接

- PDF：00-inbox/Aug_inbox/2026-Cybersecurity-Application_of_tabular_transformer_architectures_for_operating_system_fingerprinting.pdf
- MinerU Markdown：02-parsed-markdown/2026-Cybersecurity-Application_of_tabular_transformer_architectures_for_operating_system_fingerprinting.md

---

## 12. 后续问题

- 表格 Transformer 在真实跨网络/跨时间场景下的 OS 指纹识别泛化能力如何？（概念漂移未评估）
- major/minor 细粒度识别（68–79%）的瓶颈是特征信息不足还是模型容量？能否用原始报文特征（如 TLS 指纹 JA3/JA4）补足？
- FT-T 注意力权重与经典特征重要性（如 SHAP/树模型增益）的一致性如何？
- 主动探测（Nmap）与被动表格模型组合的混合方案能否提升细粒度精度？

---

## 13. 写作叙事与故事线分析

> 仅对 CCF A/B 级或用户指定深度分析的论文填写本节。本文为 L2 级别，按约定不填写本节。

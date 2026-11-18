---
type: "paper"
title_original: "CryptoFormer: Multi-Currency Traffic Classification Via Two-Stage Transformer Architecture"
title_cn: "CryptoFormer：两阶段 Transformer 的多币种流量分类"
authors: ["Zhenyu Guo", "Zijian Zhang", "Yan Wu", "Jiahang Sun", "Jiamou Liu", "Xin Li", "Yajie Wang", "Guoqiang Zhang", "Lei Zhang", "Liehuang Zhu"]
year: 2026
venue: "TDSC"
source_version: "IEEE TDSC 作者接收稿，页码及卷期以后续正式版本为准。"
doi: "10.1109/tdsc.2026.3736643"
url: "https://doi.org/10.1109/tdsc.2026.3736643"
pdf: "00-inbox/PDFs/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture.pdf"
mineru_md: "02-parsed-markdown/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture.md"
status: "processed"
reading_level: "L3"
research_area: ["加密流量分类", "区块链网络流量"]
task: ["多币种会话分类"]
method: ["Transformer", "内容与行为门控融合", "会话分类"]
dataset: ["作者自建 18 种资产与公共业务背景的会话数据"]
code: "unknown"
relevance: "high"
created: "2026-11-18"
updated: "2026-11-18"
metadata_source: "Crossref"
source_sha256: "6b6f6eedba459e754c65ed4f22a369fbfe935857b890171e2f454815a4cf038d"
internal_citation_count: 0
citation_impact: 0.8
composite_weight: 0.68
citation_count_scope: "verified DOI or normalized complete titles in vault References; lower bound"
citation_count_verified: "2026-11-18"
---

# CryptoFormer: Multi-Currency Traffic Classification Via Two-Stage Transformer Architecture

## 0. 论文基础信息

| 项目 | 内容 |
| --- | --- |
| 原文标题 | CryptoFormer: Multi-Currency Traffic Classification Via Two-Stage Transformer Architecture |
| 中文标题 | CryptoFormer：两阶段 Transformer 的多币种流量分类 |
| 作者 | Zhenyu Guo、Zijian Zhang、Yan Wu、Jiahang Sun、Jiamou Liu、Xin Li、Yajie Wang、Guoqiang Zhang、Lei Zhang、Liehuang Zhu |
| 年份 | 2026 |
| 会议/期刊及版本 | IEEE TDSC 作者接收稿，页码及卷期以后续正式版本为准。 |
| DOI | 10.1109/tdsc.2026.3736643 |
| 题录来源 | Crossref |
| 研究方向 | 加密流量分类、区块链网络流量 |
| 任务类型 | 多币种会话分类 |
| 方法关键词 | Transformer、内容与行为门控融合、会话分类 |
| 数据集 | 作者自建 18 种资产与公共业务背景的会话数据 |
| 开源状态 | 论文 §I 声明发布数据集，当前稿未给出核验可访问的下载入口，代码为 unknown。 |
| PDF | [[00-inbox/PDFs/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture.pdf]] |
| MinerU Markdown | [[02-parsed-markdown/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture.md]] |

题录核验见 [出版记录](https://doi.org/10.1109/tdsc.2026.3736643)。

## 1. 一句话总结

CryptoFormer 分别提取包内容和会话行为，再通过自适应门控预测子会话的币种或背景类别。

## 2. 摘要翻译

### 2.1 摘要原文

见 [[00-inbox/PDFs/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture.pdf]] 第 1 页 Abstract。

### 2.2 摘要中文翻译

多币种在 P2P 网络中并发传播，明文和加密协议的内容信号也不同。CryptoFormer 先提取包级内容，再对融合后的行为特征做会话级建模。作者用覆盖十八种资产及背景的带标签流量报告 95.02% macro F1，并比较两层 Transformer 的计算代价。

## 3. 方法动机

币种间既有包格式差异，又存在共享行为和结构。统一序列表示会混合局部内容与传播节奏。论文把内容/行为融合的可用性设为一个可用消融检验的假设（§II–IV）。

### 3.4 问题发现路径

| 阶段 | 内容 |
| --- | --- |
| 现象观察 | 同一采集中并存明文、密文和共用链路的多币种行为。 |
| 痛点提炼 | 单一表示难区分局部字段与跨包传播节奏的作用。 |
| 问题转化 | 根据可见特征调整内容/行为配比能否改善子会话分类？ |
| 文献定位 | 以预训练、传统统计及 CNN 时序模型为主比较，按融合方式消融。 |

### 3.5 科学假设形成

显式分包内与会话层，并用自适应门控可缩小某些类别的混淆。

验证方式　同划分对照单模态和简单融合，在密文子集中再测。若无内容增益，不能把混合集的消融推广到密文。

已有结果　表 V 给出混合数据的排序。图 8 支持组件贡献，尚需密文子集证据。

## 4. 方法设计

### 4.1 输入、处理与输出

| 步骤 | 输入 | 处理 | 输出 |
| --- | --- | --- | --- |
| 带标签会话 | 网关抓包与节点日志 | 用日志对齐币种标签，按五元组重组、空闲间隔与包数分成子会话 | 按子会话标注的样本 |
| 包内编码 | 每流最多 10 包、每包前 32 字节与方向、长度、时间等 | 先编码内容，再将观测到的行为元数据投影并按门控混合 | 融合包表示 |
| 会话判定 | 融合后的子会话包序列 | 第二阶段 Transformer 和汇聚后用交叉熵训练分类头 | 18 个资产类别及背景 |

### 4.2 机制与条件

门控权重 α 在内容表示与行为表示之间插值。两阶段分别处理包级输入和会话动态。论文报告对明文与密文协议有不同门控倾向，门值是模型内部变量而非协议加密状态真值（§IV-C–E）。

## 5. 与其他方法对比

与 ET-BERT、TrafficFormer 的比较混合了表示、模型架构和预训练条件。§V-G 分别移除内容、行为和方向并与加法/拼接融合比较，能更直接说明本模型各组件的边际贡献。

## 6. 实验表现与局限性

### 6.1 设置、数据与对照

自建数据含十八种资产和 DNS、HTTP、流媒体等背景，具有明文与密文协议，文中记录超过 188K 带标签的会话流。评估单元为子会话，需额外核对同连接、节点及时间是否隔离。PyTorch 配置见 §V-D。

- 基线　Appscanner、DeepFP、FS-Net、Deep Packet、PerFormer、LongFormer、ET-BERT、TrafficFormer。
- 指标　Accuracy、macro Precision/Recall/F1、AUC、训练墙钟时间。

### 6.2 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 对照 | 差异 | 原文定位 |
| --- | --- | --- | --- | --- | --- |
| 作者报告的币种分类主比较 | macro F1 | 95.02% | ET-BERT 93.74%；TrafficFormer 93.16% | +1.28 / +1.86 个百分点 | §V-E 表 V |
| 18 资产消融 | macro F1 | 95.02% | 移除包内容 68.87% | +26.15 个百分点 | §V-G 图 8，混合明密文本 |
| 作者训练环境 | 训练墙钟时间 | 335 s | ET-BERT 887 s | 约 2.65 倍 | §V-H 图 9，比较训练流程 |

### 6.7 局限性

总体分数和 payload 消融同时纳入明文及密文协议的样本，因此不能直接识别密文的独立贡献。带背景类别的多分类表没有给跨采集环境的极低误报工作点。

## 7. 学习与应用

### 7.1 开源状态

论文 §I 声明发布数据集，当前稿未给出核验可访问的下载入口，代码为 unknown。

### 7.2 复核要点

确认日志对应关系与子会话聚类分组，在相同输入长度和数据切分下分别做密文子集、仅长度/时间、字段屏蔽和同链/不同资产的比较。

### 7.3 可迁移的研究问题

对代理封装下 Tor 判断，可保留包级读数与会话级行为的两层分工。参考 COSINT 的逐流低基率协议，单独汇报触发门控后的各类召回、负类分母和误报。

## 8. 总结

分级编码包内容与会话行为再门控融合。

带标签会话 → 包内编码 → 会话判定。

## 9. Obsidian 知识链接

- 概念　[[04-concepts/encrypted-traffic-analysis]]、[[04-concepts/traffic-classification]]、[[04-concepts/traffic-representation-learning]]。
- 方法　[[05-methods/transformer]]、[[05-methods/multi-modal-fusion]]。
- 任务　[[06-tasks/traffic-classification]]、[[06-tasks/encrypted-traffic-detection]]。
- 综述　[[survey-encrypted-traffic-analysis]]。
- 对比与相邻资料　[[method-comparison-table]]、[[03-paper-notes/2026-COSINT-北邮时金桥]]。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
| --- | --- | --- |
| 多币种有监督模型在所采集基准中优于预训练对照 | 统一评估主要分数 | §V-E 表 V |
| 包内容消融的混合协议性能退化 | 完整十八资产数据消融 | §V-G 图 8 |

## 11. 原始资料链接

- PDF　[[00-inbox/PDFs/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture.pdf]]
- MinerU Markdown　[[02-parsed-markdown/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture.md]]
- MinerU 原始归档　[[01-mineru-output/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture/full.md]]

## 12. 后续问题

优先检验 §6.7 的主要限制，按 §7.2 记录数据、观测和指标条件。

## 13. 写作叙事与故事线分析

由明密文并存及多币种会话相似引出两级表示。主表对照总体效果，错误矩阵和消融定位信号来源，最后以训练时间讨论部署成本。

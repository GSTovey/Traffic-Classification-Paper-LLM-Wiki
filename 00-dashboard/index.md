# Traffic Papers Knowledge Base

这是一个面向网络流量分析、加密流量检测、流量基础模型和少样本流量学习研究的 Obsidian 论文知识库。

本知识库采用三层结构：

1. **原始资料层**：PDF 原文与 MinerU 抽取文本；
2. **论文笔记层**：单篇论文的结构化分析；
3. **知识沉淀层**：概念页、方法页、任务页、综述页、对比页和证据页。

---

## 1. 核心入口

| 页面 | 说明 |
|---|---|
| [[project-overview]] | **项目全景速览** — 任何智能体首次对齐上下文的入口 |
| [[paper-registry]] | **论文去重注册表** — 355 条注册记录的 DOI/标题索引，新入库前必须比对 |
| [[reading-queue]] | 论文阅读状态与重要性标记（含 2026-11-18 批次） |
| [[proposition-index]] | 正式命题、适用范围和待签审索引 |
| [[front-review-2026-11-18]] | 七条研究前沿审核稿 |
| [[open-questions]] | 历史开放问题与当前证据缺口 |
| [[research-map]] | 研究主题地图，链接到实际存在的概念页与方法页 |
| [[quality-check-report]] | 2026 年 6 月历史质量快照 |
| [[research-capability-audit]] | 跨论文综合与创新点挖掘能力审计 |
| [[research-review-queue]] | 重要证据与研究判断人工审核队列 |
| [[log]] | 知识库维护日志 |

---

## 2. 原始资料区

| 目录 | 用途 |
|---|---|
| `00-inbox/PDFs/` | 355 篇标准论文的 PDF 原文，另有学术报告 1 份 |
| `01-mineru-output/` | MinerU API 返回的原始解析结果 |
| `02-parsed-markdown/` | 整理后的 MinerU Markdown 文件 |

---

## 3. 知识区

| 目录 | 用途 | 当前数量 |
|---|---|---|
| `03-paper-notes/` | 单篇论文结构化笔记 | 355 篇，另有学术报告 1 份 |
| `04-concepts/` | 研究概念页 | 13 个 |
| `05-methods/` | 方法页 | 10 个 |
| `06-tasks/` | 任务页 | 9 个 |
| `07-surveys/` | 综述页 | 5 个 |
| `08-comparisons/` | 对比表（含开源注册表） | 5 个 |
| `09-claims/` | 命题、证据、关系与历史档案 | 2 个现行入口，另有审核稿与迁移清单 |
| `10-outputs/` | 草稿、报告、项目申报材料和复现笔记 | — |
| `11-my-papers/` | 个人研究材料区（隔离于主知识库，详见 [[my-research-thread]]） | 1 个个人研究点（NestTor，已晋升）+ 2 篇背景引用 |
| `12-research-fronts/` | 研究前沿追踪（签审快照 + 证据链 + 验证指引） | 7 个前沿 + 索引 + 模板 |

---

## 4. 概念页

以下概念页已创建：

- [[encrypted-traffic-analysis]] — 加密流量分析综述与核心问题
- [[traffic-classification]] — 流量分类任务定义与方法演进
- [[traffic-representation-learning]] — 流量表征学习的核心范式
- [[traffic-foundation-model]] — 流量基础模型的设计与训练
- [[few-shot-traffic-learning]] — 少样本流量学习
- [[malicious-traffic-detection]] — 恶意流量检测
- [[anomaly-detection]] — 异常检测
- [[tunnel-detection]] — 隧道检测
- [[04-concepts/website-fingerprinting]] — 网站指纹识别
- [[website-fingerprinting-defense]] — 网站指纹防御与可比评估
- [[anonymous-traffic-identification]] — 匿名流量识别
- [[censorship-circumvention]] — 审查规避与流量混淆
- [[network-telemetry]] — 网络流式遥测和观测单位

---

## 5. 方法页

以下方法页已创建：

- [[transformer]] — Transformer 架构在流量分析中的应用
- [[contrastive-learning]] — 对比学习方法
- [[graph-neural-network]] — 图神经网络
- [[multi-modal-fusion]] — 多模态融合方法
- [[pre-training-finetuning]] — 预训练-微调范式
- [[self-supervised-learning]] — 自监督学习
- [[convolutional-network]] — 卷积神经网络
- [[state-space-model]] — 状态空间模型（Mamba 等）
- [[factorized-detection]] — 复合目标的独立条件判别与 AND 决策。
- [[streaming-telemetry-sketch]] — 遥测有界状态的写入、压缩与查询

---

## 6. 任务页

以下任务页已创建：

- [[traffic-classification]] — 流量分类
- [[malicious-traffic-detection]] — 恶意流量检测
- [[04-concepts/website-fingerprinting]] — 网站指纹识别
- [[website-fingerprinting-defense]] — 网站指纹防御与可比评估
- [[encrypted-traffic-detection]] — 加密流量检测
- [[app-fingerprinting]] — 应用指纹识别
- [[anomaly-detection]] — 异常检测
- [[tunnel-detection]] — 隧道检测
- [[traffic-representation]] — 流量表征
- [[network-traffic-measurement]] — 流量测量及资源计量

---

## 7. 综述页与对比表

- [[survey-encrypted-traffic-analysis]] — 加密流量分析综述
- [[survey-traffic-foundation-model]] — 流量基础模型综述
- [[survey-website-fingerprinting]] — 网站指纹识别综述
- [[survey-malicious-traffic-detection]] — 恶意流量检测综述
- [[survey-few-shot-learning]] — 少样本学习综述
- [[dataset-comparison-table]] — 数据集对比表
- [[method-comparison-table]] — 方法对比表
- [[open-source-registry]] — 方法和数据产物注册表（101 个已确认公开产物与高频基线追踪）
- [[motivation-pattern-comparison]] — 研究动机模式横向对比
- [[narrative-pattern-comparison]] — 叙事模式横向对比

---

## 8. Claims 页面

- [[proposition-index]] — 当前命题索引与待签审命题
- [[contradictions]] — 已签审的关系、条件差异及历史记录

---

## 9. 当前状态

- 355 篇注册论文的笔记、原版 PDF、解析稿和引文已逐项对应。其中 142 篇为 L3/L4，另有 1 份 COSINT 学术报告。
- 正式研究前沿快照覆盖 7 条前沿。35 条现行命题已按原文范围签审，其中 7 条记为证据不足，2 条仅用于引用 COSINT 报告结果。
- [[quality-check-report#2026-11-20　全库结构与论文笔记补齐|11 月 20 日全库复核记录]] 包含题录、正文、链接和模拟入库的检查结果。
- 13 个概念页已创建于 `04-concepts/`。
- 10 个方法页已创建于 `05-methods/`。
- 9 个任务页已创建于 `06-tasks/`。
- 5 个综述页已创建于 `07-surveys/`。
- 5 个对比表已创建于 `08-comparisons/`（含开源注册表和动机/叙事对比）。
- [[proposition-index|命题索引]] 与 [[contradictions|跨论文关系]] 为现行证据入口。旧文档计数留存于 [[claims-index|历史 Claims]] 和 [[claim-migration-map|迁移清单]]。
- 9 个研究前沿文件已创建于 `12-research-fronts/`（7 个活跃前沿 + 索引 + 模板）。
- 参考文献现为 356 条 JSON 与 373 条 BibTeX，全覆盖 355 篇注册论文。未注册的 TrafficSliver 旧记录作为历史引文保留。

---

## 10. 待扩展页面

以下方向尚无独立页面，可后续逐步创建：

**概念页**：vpn-traffic-classification、tor-traffic-classification、intrusion-detection、malware-detection、dns-security、network-privacy、iot-security

**方法页**：meta-learning、attention-mechanism、autoencoder、random-forest、fingerprinting-methods、data-augmentation

**任务页**：（当前已覆盖主要任务方向）

**综述页**：（当前已覆盖主要综述方向）

## 2024–2026 四大安全顶会深度分析覆盖（2026-11-03）

- 已补齐 28 篇标准论文的 L3 深度分析：2024 年 8 篇、2025 年 12 篇、2026 年 8 篇。
- 目标会议为 USENIX Security、NDSS、ACM CCS、IEEE S&P；AsiaCCS、NSDI 和只读隔离笔记未纳入本批次。
- 逐篇清单、原文证据入口和边界说明：覆盖报告（本地）。

## 重点学术报告（2026-11-17）

[[03-paper-notes/2026-COSINT-北邮时金桥|2026-COSINT-北邮时金桥]] 已按高度相关、L3、`academic-talk`、`report-only` 标识入库。包含 DHOR/DHBCorr 详细笔记、54 页提要/页图/文本层及本地 PDF。本次汇报入档时有标准论文 342 篇、学术报告 1 份。


## 2026-11-18　批次入库（13 篇）

13 篇新论文的入口见 [[reading-queue#2026-11-18　批次入库（13 篇）|阅读队列]]。本批 13 篇均已独立完成 L3 分析，新增联动覆盖流量语料质量、溯源图防御、主动测量、Tor 可用性、遥测编译及流量矩阵。与 DHOR 和 DHBCorr 的交叉阅读见 [[03-paper-notes/2026-COSINT-北邮时金桥|COSINT 学术汇报]] 第 14 节。

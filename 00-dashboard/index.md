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
| [[paper-registry]] | **论文去重注册表** — 92 篇论文的 DOI/标题索引，新入库前必须比对 |
| [[reading-queue]] | 全部 92 篇论文的阅读状态与重要性标记 |
| [[open-questions]] | 从 Claims 与矛盾记录中提炼的开放研究问题 |
| [[research-map]] | 研究主题地图，链接到实际存在的概念页与方法页 |
| [[quality-check-report]] | 知识库质量检查报告 |
| [[log]] | 知识库维护日志 |

---

## 2. 原始资料区

| 目录 | 用途 |
|---|---|
| `00-inbox/PDFs/` | 待处理和已处理的 92 篇 PDF 原文 |
| `01-mineru-output/` | MinerU API 返回的 92 份原始解析结果 |
| `02-parsed-markdown/` | 整理后的 92 份 MinerU Markdown 文件 |

---

## 3. 知识区

| 目录 | 用途 | 当前数量 |
|---|---|---|
| `03-paper-notes/` | 单篇论文结构化笔记 | 92 篇 |
| `04-concepts/` | 研究概念页 | 9 个 |
| `05-methods/` | 方法页 | 8 个 |
| `06-tasks/` | 任务页 | 8 个 |
| `07-surveys/` | 综述页 | 5 个 |
| `08-comparisons/` | 对比表（含开源注册表） | 5 个 |
| `09-claims/` | 观点、证据与矛盾记录 | 2 个 |
| `10-outputs/` | 草稿、报告、项目申报材料和复现笔记 | — |

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
- [[website-fingerprinting]] — 网站指纹识别

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

---

## 6. 任务页

以下任务页已创建：

- [[traffic-classification]] — 流量分类
- [[malicious-traffic-detection]] — 恶意流量检测
- [[website-fingerprinting]] — 网站指纹识别
- [[encrypted-traffic-detection]] — 加密流量检测
- [[app-fingerprinting]] — 应用指纹识别
- [[anomaly-detection]] — 异常检测
- [[tunnel-detection]] — 隧道检测
- [[traffic-representation]] — 流量表征

---

## 7. 综述页与对比表

- [[survey-encrypted-traffic-analysis]] — 加密流量分析综述
- [[survey-traffic-foundation-model]] — 流量基础模型综述
- [[survey-website-fingerprinting]] — 网站指纹识别综述
- [[survey-malicious-traffic-detection]] — 恶意流量检测综述
- [[survey-few-shot-learning]] — 少样本学习综述
- [[dataset-comparison-table]] — 数据集对比表
- [[method-comparison-table]] — 方法对比表
- [[open-source-registry]] — 开源模型/方法注册表（30 个已确认开源 + 高频基线追踪）
- [[motivation-pattern-comparison]] — 研究动机模式横向对比
- [[narrative-pattern-comparison]] — 叙事模式横向对比

---

## 8. Claims 页面

- [[claims-index]] — 关键观点索引（42 条核心 Claims）
- [[contradictions]] — 论文间矛盾记录（9 组冲突）

---

## 9. 当前状态

- 92 篇 PDF 已导入 `00-inbox/PDFs/`。
- 92 篇 MinerU Markdown 已生成至 `01-mineru-output/`。
- 92 篇结构化论文笔记已创建于 `03-paper-notes/`。
- 9 个概念页已创建于 `04-concepts/`。
- 8 个方法页已创建于 `05-methods/`。
- 8 个任务页已创建于 `06-tasks/`。
- 5 个综述页已创建于 `07-surveys/`。
- 5 个对比表已创建于 `08-comparisons/`（含开源注册表和动机/叙事对比）。
- 2 个 Claims 页面已创建于 `09-claims/`（含 42 条核心观点和 9 组矛盾记录）。

---

## 10. 待扩展页面

以下方向尚无独立页面，可后续逐步创建：

**概念页**：vpn-traffic-classification、tor-traffic-classification、intrusion-detection、malware-detection、dns-security、network-privacy、iot-security

**方法页**：meta-learning、attention-mechanism、autoencoder、random-forest、fingerprinting-methods、data-augmentation

**任务页**：（当前已覆盖主要任务方向）

**综述页**：（当前已覆盖主要综述方向）

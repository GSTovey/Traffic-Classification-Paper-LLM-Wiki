# AGENTS.md

本文件定义 Traffic_Papers Obsidian 论文知识库的维护规范。
所有智能体在处理本知识库时必须遵守本文件。

---

## 1. 知识库定位

Traffic_Papers 是一个面向网络流量安全研究的本地论文知识库，重点服务于：

- 论文阅读；
- 综述写作；
- 项目申报；
- 方法比较；
- 技术路线设计；
- 实验复现；
- 创新点挖掘。

重点研究方向包括：

- 流量检测；
- 加密流量分析；
- 恶意流量检测；
- QUIC / HTTP3 流量分析；
- 匿名通信流量识别；
- 流量领域基础模型；
- 网站指纹识别；
- 少样本流量学习；
- 异常检测与隧道检测。

---

## 2. 三层结构

本知识库采用三层结构：

### 2.1 原始资料层

包括：

- `00-inbox/PDFs/` — 待处理的 PDF 原文
- `01-mineru-output/` — MinerU API 返回的原始解析结果
- `02-parsed-markdown/` — 整理后的 MinerU Markdown

要求：

- PDF 原文不直接修改；
- MinerU Markdown 作为机器可读原文保存；
- 不要把完整 MinerU Markdown 复制进论文主笔记；
- 论文主笔记只通过链接引用 PDF 和 MinerU Markdown。

### 2.2 论文笔记层

包括：

- `03-paper-notes/`

要求：

- 一篇论文对应一篇主笔记；
- 主笔记必须使用 `templates/paper-note-template.md` 的结构；
- 主笔记应包含基础信息、摘要翻译、方法分析、实验表现、局限性、复现建议和知识链接；
- 不得编造论文中没有出现的信息；
- 不确定内容必须标注 unknown 或"论文未明确说明"。

### 2.3 知识沉淀层

包括：

- `04-concepts/`
- `05-methods/`
- `06-tasks/`
- `07-surveys/`
- `08-comparisons/`
- `09-claims/`
- `10-outputs/`

要求：

- 新论文不只生成单篇笔记，还应判断是否更新概念页、方法页、任务页、综述页、对比表、开源注册表和证据页；
- 概念页用于沉淀定义、共识、争议和代表论文；
- 方法页用于沉淀方法机制、适用场景、优缺点和代表论文；
- 任务页用于沉淀任务定义、输入输出、指标、数据集和工程问题；
- 综述页用于支持后续写作；
- 对比页用于横向比较；
- 对比页共 5 个：`method-comparison-table.md`（方法对比）、`dataset-comparison-table.md`（数据集对比）、`open-source-registry.md`（开源注册表）、`motivation-pattern-comparison.md`（研究动机模式横向对比）、`narrative-pattern-comparison.md`（叙事模式横向对比）；
- 开源注册表（`08-comparisons/open-source-registry.md`）用于追踪方法/模型的开源状态、代码仓库地址和高频基线的代码可用性；
- Claims 页用于记录可引用观点及其证据来源。

---

## 3. 文件命名规范

### 3.1 论文 PDF

建议格式：

```text
year-firstauthor-shorttitle.pdf
```

示例：

```text
2024-zhang-encrypted-traffic-classification.pdf
```

### 3.2 MinerU Markdown

建议格式：

```text
year-firstauthor-shorttitle.raw.md
```

示例：

```text
2024-zhang-encrypted-traffic-classification.raw.md
```

### 3.3 论文主笔记

建议格式：

```text
year-firstauthor-shorttitle.md
```

示例：

```text
2024-zhang-encrypted-traffic-classification.md
```

### 3.4 概念、方法、任务页面

使用英文小写和短横线：

```text
encrypted-traffic-analysis.md
traffic-classification.md
multi-agent-system.md
```

---

## 4. 论文处理等级

每篇论文应标注 reading_level：

| 等级 | 含义 | 处理深度 |
|---|---|---|
| L1 | 快速入库 | 基础信息、摘要、方法概览、是否值得深读 |
| L2 | 标准阅读 | 完整方法分析、实验总结、局限性 |
| L3 | 深度方法分析 | 重点分析 pipeline、模块、公式、实验和迁移价值 |
| L4 | 复现导向分析 | 增加代码结构、复现步骤、工程风险和替代实现 |

默认：

- 普通相关论文：L2；
- 核心论文：L3；
- 准备复现的论文：L4；
- 扫描性文献：L1。

---

## 5. 论文入库流程

当用户导入一篇新论文时，按以下流程处理：

### 5.1 标准入库流程（手动分步）

0. **去重检查**：读取 `00-dashboard/paper-registry.md`，通过 DOI/标题/作者三轮匹配检查是否重复（详见 `templates/claudian-prompts/00-check-duplicate.md`）；
1. 确认 PDF 位于 `00-inbox/PDFs/`；
2. 确认 MinerU Markdown 位于 `02-parsed-markdown/`；
3. 读取 MinerU Markdown；
4. 检查 MinerU 抽取质量；
5. 生成论文主笔记到 `03-paper-notes/`；
6. 在主笔记中链接 PDF 和 MinerU Markdown；
7. 判断是否更新概念页；
8. 判断是否更新方法页；
9. 判断是否更新任务页；
10. 判断是否更新综述页；
11. 判断是否更新对比表；
12. 判断是否更新开源注册表（`08-comparisons/open-source-registry.md`）；
13. 判断是否更新 Claims；
14. 更新 `00-dashboard/paper-registry.md`（追加一行）；
15. 更新 `00-dashboard/reading-queue.md`（追加一行）；
16. 更新 `00-dashboard/index.md`；
17. 更新 `00-dashboard/log.md`。

### 5.2 一键入库流程（推荐）

使用 `templates/claudian-prompts/06-ingest-pipeline.md` 可一键完成上述全部步骤。
智能体将自动执行去重检查 → PDF 解析 → 笔记生成 → 知识层全量更新 → 全局索引更新。

---

## 6. 写作规则

所有论文分析必须遵守以下规则：

1. 使用中文；
2. 专业、严谨、逻辑清晰；
3. 不编造信息；
4. 不夸大论文贡献；
5. 区分论文明确证明、论文声称、合理推断和不确定内容；
6. 方法部分必须讲清楚输入、处理、输出；
7. 实验部分必须记录数据集、baseline、指标和关键结果；
8. 如果论文没有给出具体数值，不得补造；
9. 如果论文没有开源信息，写 unknown；
10. 如果 MinerU 抽取有问题，必须标注。

---

## 7. Obsidian 链接规则

1. 内部链接使用 `[[page-name]]`；
2. 不要使用过长页面名；
3. 论文主笔记应链接到相关概念、方法、任务和综述页；
4. 概念页应链接到代表论文；
5. 综述页应链接到关键论文和方法页；
6. Claims 必须链接到证据来源。

---

## 8. 禁止事项

智能体不得：

1. 删除已有文件；
2. 覆盖用户手写内容；
3. 移动 PDF 原文，除非用户明确要求；
4. 把完整 MinerU Markdown 原文复制进论文主笔记；
5. 编造论文不存在的信息；
6. 自动创建大量空白页面污染知识库；
7. 在没有证据的情况下更新 Claims；
8. 将模板文件当作真实论文笔记。

---

## 9. 推荐处理顺序

当用户要求处理新论文时，优先使用：

1. `templates/claudian-prompts/01-ingest-paper.md`
2. `templates/claudian-prompts/02-update-knowledge-base.md`
3. 如果论文重要，再使用：
   - `templates/claudian-prompts/03-deep-method-analysis.md`
   - `templates/claudian-prompts/04-reproduction-analysis.md`

当用户要求检查知识库时，使用：

- `templates/claudian-prompts/05-quality-check.md`

当用户要求对论文进行研究动机链分析或全文叙事分析时，使用：

- `templates/claudian-prompts/07-motivation-narrative-analysis.md`

---

## 10. 日志规范

每次重要操作后，应追加记录到 `00-dashboard/log.md`。

格式：

```text
## [YYYY-MM-DD] action | title
- Changed:
  -
- Added:
  -
- Updated:
  -
- Notes:
  -
```

示例：

```text
## [2026-05-27] ingest | Example Paper Title
- Added:
  - [[2026-example-paper]]
- Updated:
  - [[encrypted-traffic-analysis]]
  - [[traffic-classification]]
- Notes:
  - Marked as L3 core paper.
```

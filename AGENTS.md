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
- 创新点挖掘；
- 个人论文管理与研究轨迹追踪。

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

### 2.4 关键图表提取

- `10-outputs/key-figures/all-key-figures.md` — 汇总 Markdown，嵌入每篇论文的核心框架图
- `10-outputs/key-figures/images/` — 拷贝过来的关键图片（148 张）
- `10-outputs/key-figures/manifest.json` — 增量更新追踪

使用 `scripts/extract_key_figures.py` 生成，基于三层评分系统（caption 关键词、图片类型、bbox 尺寸）自动筛选每篇论文 1-2 张核心框架图。

要求：

- 用户手动删除的图片不会被重复添加（通过 manifest + Markdown 比对检测）
- 再次运行时只处理新增论文，已处理论文跳过
- 位于 `10-outputs/` 下，不参与版本控制

### 2.5 个人论文区（隔离）

包括：

- `11-my-papers/notes/` — 个人论文笔记
- `11-my-papers/my-research-thread.md` — 研究轨迹页面
- `11-my-papers/my-paper-registry.md` — 个人论文注册表

要求：

- 使用 `type: my-paper` frontmatter，模板为 `templates/my-paper-note-template.md`；
- **严格隔离**：个人论文笔记不触发主知识库（04-09）的任何自动更新；
- 个人论文可链接到主知识库的概念页、方法页、任务页和已有论文（只读方向）；
- 主知识库页面不得自动添加指向个人论文的链接；
- 如需将已发表或已认可的论文提升至主知识库，必须由用户明确要求并执行完整入库流程（详见 `templates/claudian-prompts/08-ingest-my-paper.md` 的晋升机制）；
- 晋升后个人论文笔记保留在 `11-my-papers/notes/`，通过 `promoted_to` 字段关联到 `03-paper-notes/` 中的标准笔记。

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

### 3.5 个人论文笔记

建议格式：

```text
year-venue-shorttitle.md
```

示例：

```text
2026-NDSS-my-encrypted-traffic-method.md
```

文件位于 `11-my-papers/notes/`，命名规范与 3.3 一致。

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

当用户导入一篇新论文时，**必须**使用一体化管道完成全部流程，不需要用户逐步指示。

### 5.1 唯一入库流程（一体化管道）

使用 `templates/claudian-prompts/06-ingest-pipeline.md` 执行以下全部阶段：

- **阶段 0：去重检查** — 读取 `00-dashboard/paper-registry.md`，通过文件名 + 标题 + 摘要 + DOI + 作者/年份/venue 五轮联合匹配检查是否重复（详见 `templates/claudian-prompts/00-check-duplicate.md`）；
- **阶段 1：PDF 解析** — MinerU 解析或复用已有解析结果；
- **阶段 2：生成论文笔记** — 按 `templates/paper-note-template.md` 生成结构化笔记到 `03-paper-notes/`；
- **阶段 3：自动更新知识层** — 自动判断并更新所有相关概念页、方法页、任务页、综述页、对比表、开源注册表和 Claims，**不需要用户单独询问**；
- **阶段 4：更新全局索引** — paper-registry、reading-queue、index、log；
- **阶段 5：自动更新 README.md 和 AGENTS.md** — 同步更新统计数据和关键论文列表，**不需要用户提醒**；
- **阶段 6：Git 提交（仅用户要求时）** — 仅当用户明确说"上传"、"提交"、"push"时才执行 commit，不自动 push。`10-outputs/` 目录大部分不参与版本控制，但 `10-outputs/key-figures/` 子目录可上传（自动提取的关键框架图）。

### 5.2 个人论文入库流程

当用户导入自己的论文时，使用 `templates/claudian-prompts/08-ingest-my-paper.md`。

关键区别：

- 不检查 `paper-registry.md`，只检查 `my-paper-registry.md`；
- 使用 `my-paper-note-template.md`，而非 `paper-note-template.md`；
- **不更新**主知识沉淀层（04-09）；
- 仅更新 `my-paper-registry.md`、`my-research-thread.md` 和 `00-dashboard/log.md`；
- PDF 解析（MinerU）为可选步骤；
- 支持 PDF、LaTeX、口述等多种输入方式。

### 5.3 关键原则

1. **一篇论文一次完成**：单篇论文的入库 + 知识层全量更新 + 文档同步在一次流程中全部完成；
2. **不需要逐步确认**：阶段 0-5 自动执行，仅去重阶段的疑似重复需要用户确认；
3. **追加不覆盖**：知识层更新只追加新行，不修改已有内容；
4. **README/AGENTS 自动同步**：每次入库后自动检查并更新，不需要用户提醒。

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
7. 个人论文笔记（`11-my-papers/`）中的链接指向主知识库为只读方向。主知识库页面不得自动添加指向 `11-my-papers/` 的链接。如需在主知识库中引用个人论文，必须由用户手动添加且论文 confidence 为 high。

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
8. 将模板文件当作真实论文笔记；
9. 自动执行 `git commit` 或 `git push`，除非用户明确要求"上传"/"提交"/"push"；
10. 将 `10-outputs/` 目录下的文件提交到 Git 仓库（`10-outputs/key-figures/` 除外，该子目录可上传）；
11. 因为 `11-my-papers/` 中的论文自动创建或修改 `04-concepts/`、`05-methods/`、`06-tasks/`、`07-surveys/`、`08-comparisons/`、`09-claims/` 中的任何页面；
12. 将 `type: my-paper` 的笔记加入 `00-dashboard/paper-registry.md` 或 `reading-queue.md`。

---

## 9. 推荐处理顺序

当用户要求处理新论文时，**直接使用一体化管道**：

- `templates/claudian-prompts/06-ingest-pipeline.md`（默认，包含去重→解析→笔记→知识层全量更新→文档同步→可选 Git 提交）

当用户要求检查知识库时，使用：

- `templates/claudian-prompts/05-quality-check.md`

当用户要求对已有论文进行深度方法分析时，使用：

- `templates/claudian-prompts/03-deep-method-analysis.md`

当用户要求对已有论文进行复现分析时，使用：

- `templates/claudian-prompts/04-reproduction-analysis.md`

当用户要求对已有论文进行研究动机链分析或全文叙事分析时，使用：

- `templates/claudian-prompts/07-motivation-narrative-analysis.md`

当用户导入自己的论文（非主知识库文献）时，使用：

- `templates/claudian-prompts/08-ingest-my-paper.md`

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

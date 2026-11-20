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
- 异常检测与隧道检测；
- 网络测量与流量矩阵补全；
- 网络协议模糊测试、隐蔽信道与 DNS/QUIC 安全。

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
- 命题索引记录适用条件、审核状态和证据 ID。历史 Claims 表用于追溯既有判断。

### 2.4 研究前沿追踪层

包括：

- `12-research-fronts/`

要求：

- 每个研究前沿问题对应一个独立页面；
- 前沿页面按时间顺序追踪同一研究问题的证据链；
- 每条证据记录论文、年份、结论方向（支持/反对/中性）和实验严格度；
- 前沿顶部包含“当前研究认识”，下方保留证据链、研究空白与历次判断；
- 前沿页面包含"Auto Research 指引"，为后续自动化研究提供选题和方案设计支撑；
- 前沿的 `status` 记录签审后的进展。待签审时使用 `pending_review`；证据不足时可使用 `insufficient_evidence`；
- 新论文入库时，自动登记相关前沿的候选证据。修改当前认识及状态须经维护者签审。

### 2.5 关键图表提取

- `10-outputs/key-figures/all-key-figures.md` — 汇总 Markdown，嵌入每篇论文的核心框架图
- `10-outputs/key-figures/images/` — 拷贝过来的关键图片（截至 2026-10-26 为 536 张）
- `10-outputs/key-figures/manifest.json` — 增量更新追踪

使用 `scripts/extract_key_figures.py` 生成，基于三层评分系统（caption 关键词、图片类型、bbox 尺寸）自动筛选每篇论文 1-2 张核心框架图。

要求：

- 用户手动删除的图片不会被重复添加（通过 manifest + Markdown 比对检测）
- 再次运行时只处理新增论文，已处理论文跳过
- 位于 `10-outputs/` 下，不参与版本控制

### 2.6 个人论文区（隔离）

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

### 2.7 引用与参考文献

包括：

- `bibliography.json` — 全部论文的结构化 BibTeX 元数据（JSON 格式，含 citation_key、entry_type、title、authors、year、booktitle/journal、pages、volume、publisher、doi、url、abstract）
- `bibliography.bib` — LaTeX 可用的 BibTeX 引用文件（从 bibliography.json 生成，可直接复制到 .bib 文件中使用）

要求：

- 数据来源必须为官方 API（CrossRef、OpenAlex、Semantic Scholar），不得编造；
- 新论文入库时，自动更新 bibliography.json 和 bibliography.bib；
- citation_key 格式为 `{firstauthor_lastname}{year}{first_keyword}`；
- 每次更新后需验证 .bib 文件的花括号平衡和条目唯一性。

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

已发表并由用户明确要求晋升的个人论文可使用 `YEAR-myPaper-VENUE-Short_Title` 命名；PDF、解析稿与标准笔记使用同一文件主名。个人区保留独立、无歧义的记录名并用 `promoted_to` 指向标准笔记。不得据此自动晋升其他个人论文。

### 3.6 研究前沿页面

使用英文小写和短横线：

```text
payload-learnability.md
representation-vs-shallow.md
pretraining-necessity.md
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

当用户导入一篇新论文时，**必须**使用一体化管道完成全部流程，不需要用户逐步指示。

### 5.1 唯一入库流程（一体化管道）

使用 `templates/claudian-prompts/06-ingest-pipeline.md` 执行以下全部阶段：

- **阶段 0：去重检查** — 读取 `00-dashboard/paper-registry.md`，通过文件名 + 标题 + 摘要 + DOI + 作者/年份/venue 五轮联合匹配检查是否重复（详见 `templates/claudian-prompts/00-check-duplicate.md`）；
- **阶段 1：PDF 解析** — 默认使用 MinerU API 解析（如 `MINERU_API_TOKEN` 未设置则暂停向用户索要）；解析完成后自动运行 `scripts/extract_key_figures.py` 提取关键框架图；
- **阶段 2：生成论文笔记** — 按 `templates/paper-note-template.md` 生成结构化笔记到 `03-paper-notes/`；
- **阶段 3：自动更新知识层** — 追加论文事实、来源和相关概念、方法、任务、综述、对比与开源信息；
- **阶段 3.5：候选证据登记** — 写入证据账本和审核队列，标记相关命题、跨论文关系和研究前沿。正式判断走 §11 的核验与签审流程；
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
2. **入库与签审**：阶段 0–5 自动执行，疑似重复由用户确认。正式科学判断单独经过语义审核和维护者签审；
3. **保留历史，允许修订当前结论**：原始论文、来源材料、历史判断和人工记录原样保留。签审后可更新当前综合结论，并保留上一版判断、修改原因、证据依据与审核记录；
4. **README/AGENTS 自动同步**：每次入库后自动检查并更新，不需要用户提醒。

### 5.1.1 跨论文综合与创新点挖掘

当论文进入核心研究方向时，使用 `templates/claudian-prompts/09-research-problem-analysis.md`，按以下顺序工作：

`Research Landscape → Cross-paper Relations → Evidence-backed Gaps → Candidate Innovations → Counterevidence Check → Testable Hypotheses → Research Prioritization`

- 候选创新点必须关联具体论文和原文定位；
- 必须区分原文事实、作者声称、跨论文综合判断和个人待验证假设；
- 必须主动检查相邻工作、替代解释、数据划分和指标差异；
- 证据账本只登记重要主张、关键反证和候选创新点，不复制普通论文的全部实验结果；
- `auto_extracted`、`pending_review`、`verified`、`contested` 和 `retired` 是证据状态，未经审核的记录不得升级为领域共识；
- 在项目 Python 环境安装 `scripts/requirements.txt` 中的依赖。使用 `python3 scripts/research_capability_audit.py audit --all-fronts --write` 生成质量报告和人工审核队列。脚本不得自动修改论文笔记、Claims、研究前沿、方法页或个人研究页。

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
7. 个人论文笔记（`11-my-papers/`）中的链接指向主知识库为只读方向。主知识库页面不得自动添加指向 `11-my-papers/` 的链接。主知识库对个人论文的正式引用须经用户明确授权，并按 §11 核对来源、条件和引用范围。

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

## 11. 证据、命题与研究前沿

### 11.1 入库与核验

- 论文笔记记录作者报告的结果、实验条件和原文位置。发表场所、年份及有来源的引用量属于文献元数据。`reading_level` 表示阅读深度。
- 自动入库用 v2 Schema 登记 `pending_review` 候选证据。候选可关联命题和研究前沿，写入审核队列。旧评分及注册表旧计数留档，新注册行的两列 Claims 计数填 `—`。
- 人工核对结果、条件、方向、独立性与反证，记下审核人、日期与依据后，方可将证据标记为 `verified`。证据自身的解释、来源或归属还有实质争议时，用 `contested`。两项已核验且方向相反的可比实验可以分别是 `verified + supports` 和 `verified + challenges`。
- `study_lineage` 追踪主要实验归属，扩展版本和综述转述回指主实验。`data_lineage` 追踪采集样本及派生语料。同一数据上不同研究的复现只能提供这批数据条件下的可复现性。未知谱系用 `unknown`，适用范围与独立性取决于实际核对。

### 11.2 当前判断与历史

- `09-claims/proposition-index.md` 为命题入口。一条命题对应一个可检验的判断及其条件。`claim_state` 取 `supported`、`contested`、`insufficient_evidence` 或 `superseded`，由人工审核确定。单项已核验实验可支持其范围内的命题；领域共识需要可比的独立直接证据和反证核验。
- `09-claims/claims-index.md` 保存历史观点表。旧 ID、原文与审核记录保留。迁移到新命题时重新确认 v2 字段和证据关系，旧分数与审核标签不作为升级依据。
- `09-claims/contradictions.md` 按 `direct_conflict`、`scope_difference`、`method_difference`、`temporal_evolution`、`unresolved` 记录跨论文关系。可比条件下且结论确实冲突才是 `direct_conflict`。
- 前沿以页顶“当前研究认识”为准。签审后的证据不足、分歧和范围未明均为有效快照。`last_synthesized` 只记录维护者签审日期。`converging`、`diverging` 和 `stale` 描述进展；科研优先级由个人研究目标与验证可行性决定。
- 更新正式判断前，将上一版原文、变更原因、证据 ID、审核人和日期记入历史。原始资料、人工记录和历史表始终保留。正式判断所用关键证据须有可查的原文定位与 v2 审核记录。
- 结构审计、语义复核、最终签审依次完成。脚本检查字段、ID、来源路径和状态一致性；人工判断原文与命题的关系；维护者决定快照发布。待签审内容只显示为草案。

## 12. 当前数量快照（2026-11-03）

- 标准 `type: paper` 笔记 342 篇，PDF 与解析 Markdown 各 342 份；L3/L4 标注 130 篇。
- 核心知识页 40 个：11 概念、9 方法、8 任务、5 综述、5 对比、2 Claims 主索引；历史审计页另计。
- 关键图 536 张，图库覆盖 342 篇；研究前沿 7 个。
- 本次仅晋升 NestTor（TNSM 2026）；另外两份个人区材料保持原状。

## 13. 学术报告资料快照（2026-11-17）

- 已登记 1 份学术报告 `2026-COSINT-北邮时金桥`，主笔记位于 `03-paper-notes/`，类型为 `academic-talk`、L3、`report-only`。
- 原文位于 `00-inbox/PDFs/`，本地逐页提取位于 `02-parsed-markdown/`，共 54 页。四项报告主张登记为 `pending_review`，标准 `type: paper` 数量为 342。


## 14. 当前数量与方向快照（2026-11-18）

- 有效标准论文 355 篇，L3/L4 共 142 篇。标准论文 PDF、MinerU Markdown 各 355 份。另有 COSINT 学术报告 1 份。
- 355 条有效注册记录，其中补录 8 条已有论文的历史索引。遗留的 TrafficSliver 非注册版本仍保留。
- 核心知识页 43 个，包括 12 概念、10 方法、9 任务、5 综述、5 对比、2 Claims 主索引。
- 新增网络流式遥测方向，涵盖有限状态的特征写入、查询、测量和部署成本。关键图库共归档 559 张图。
- 本批新增 13 篇、7 个公开产物、10 条论文证据和 3 条 COSINT 联动证据，均待审核。更新 6 个研究前沿的候选证据链。

### 2026-11-18　批次深读补充

- 本批 13 篇均完成 L3。新增 6 条待审核的深读证据，链接到相关概念、方法、任务、综述与对比页。

## 15. 全库复核快照（2026-11-20）

- 已对应 355 篇注册论文的笔记、PDF、解析稿和参考文献。其中 142 篇为 L3/L4，另有 1 份独立学术报告。
- 核心知识页 44 个，含 13 个概念、10 个方法、9 个任务、5 个综述、5 个对比和 2 个现行证据入口。确认公开产物 101 项，图库已归档 559 张。
- 七条前沿均已更新签审快照。35 条现行命题涵盖 26 条范围内有直接证据的判断、2 条报告级判断和 7 条证据不足的判断。61 条旧账本证据均有迁移记录。
- 引文库覆盖所有注册论文，计 356 条 JSON 和 373 条 BibTeX。题录、原始材料、结构检查和模拟入库结果见 Dashboard 的质量检查报告。

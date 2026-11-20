# 一体化论文入库管道

你是一名计算机领域专家和 Obsidian 论文知识库维护者。本提示词将引导你完成从 PDF 到知识库全量更新的**完整入库流程**。

## 输入

用户会提供以下信息之一：
- 一篇新 PDF 的文件路径（通常位于 `00-inbox/PDFs/`）
- 一篇新论文的 arXiv 链接或 DOI
- 一篇已有的 MinerU Markdown 文件路径

## 完整流程

### 阶段 0：去重检查（必须先执行）

1. 读取 `00-dashboard/paper-registry.md`
2. 从新论文中提取 DOI、标题、摘要、PDF 文件名、第一作者、年份、venue
3. 执行五轮匹配（详见 `templates/claudian-prompts/00-check-duplicate.md`）：
   - 轮次 1：DOI 精确匹配
   - 轮次 2：标题关键词匹配（≥70% 重叠 = 高置信度，50-70% = 中置信度）
   - 轮次 3：作者 + 年份 + venue 交叉验证
   - 轮次 4：PDF 文件名模糊匹配
   - 轮次 5：摘要相似度匹配（语义比对）
4. 最终结论综合五轮信号联合判定
5. 输出去重检查结果：
   - **无重复** → 继续阶段 1
   - **疑似重复** → 列出候选表格，**暂停等待用户确认**
   - **确定重复** → 报告已有笔记链接，结束

### 阶段 1：PDF 解析（MinerU API）

**默认必须使用 MinerU API 解析**，不跳过此步骤。

1. 确认 PDF 位于 `00-inbox/PDFs/`（如不在，提示用户移动或复制）
2. 检查环境变量 `MINERU_API_TOKEN` 是否已设置：
   - 如未设置 → **暂停，向用户询问 MinerU API Token**，获取后设置 `export MINERU_API_TOKEN=...`
   - 如已设置 → 继续
3. 使用 MinerU API 解析：
   ```bash
   python3 scripts/mineru_batch_parse.py --input 00-inbox/PDFs/新论文文件名.pdf --batch-size 1
   ```
4. 确认解析结果位于 `02-parsed-markdown/` 目录
5. 检查解析质量（是否有乱码、公式错误、表格错位）

#### 1a. 提取关键框架图

MinerU 解析完成后，**自动运行关键图提取**：

```bash
python3 scripts/extract_key_figures.py
```

此脚本基于三层评分系统（caption 关键词、图片类型、bbox 尺寸）自动筛选每篇论文 1-2 张核心框架图，输出到 `10-outputs/key-figures/images/` 并更新 `10-outputs/key-figures/all-key-figures.md`。

- 增量处理：已处理论文自动跳过
- 用户手动删除的图片不会被重复添加（通过 manifest + Markdown 比对检测）
- 关键图用于论文笔记中嵌入框架图和综述写作参考

### 阶段 2：生成论文笔记

1. 读取 MinerU Markdown（`02-parsed-markdown/` 中的对应文件）
2. 检查 MinerU 抽取质量（是否有乱码、公式错误、表格错位）
3. 按 `templates/paper-note-template.md` 生成结构化论文笔记
4. 确保 frontmatter 包含所有标准字段，特别是：
   - `code` 字段：检查论文中是否有 GitHub/GitLab 链接
   - `doi` 字段：如能从论文中提取
   - `reading_level`：根据论文重要性设定 L1/L2/L3/L4
5. 保存到 `03-paper-notes/`，文件名遵循命名规范：`YEAR-VENUE-Short_Title.md`
6. 笔记中必须链接 PDF 和 MinerU Markdown

### 阶段 3：自动更新知识层

根据论文内容，**自动判断并更新**以下所有相关页面。不需要用户手动指定。

#### 3a. 更新概念页（04-concepts/）

检查论文是否涉及以下概念，如涉及则更新对应页面的相关方法或代表论文节：
- encrypted-traffic-analysis
- traffic-classification
- traffic-representation-learning
- traffic-foundation-model
- few-shot-traffic-learning
- malicious-traffic-detection
- anomaly-detection
- tunnel-detection
- website-fingerprinting

#### 3b. 更新方法页（05-methods/）

检查论文是否使用或提出以下方法，如涉及则更新对应页面：
- transformer
- contrastive-learning
- graph-neural-network
- multi-modal-fusion
- pre-training-finetuning
- self-supervised-learning
- convolutional-network
- state-space-model

#### 3c. 更新任务页（06-tasks/）

检查论文涉及的任务类型，更新对应任务页。

#### 3d. 更新综述页（07-surveys/）

判断论文应加入哪个综述页（survey-encrypted-traffic-analysis, survey-traffic-foundation-model, survey-website-fingerprinting, survey-malicious-traffic-detection, survey-few-shot-learning），以及在综述中的位置。

#### 3e. 更新对比表（08-comparisons/）

- **method-comparison-table.md**：如果论文提出了新方法，添加一行（含开源状态列）
- **dataset-comparison-table.md**：如果论文使用了新的数据集，添加一行
- **open-source-registry.md**：如果论文有开源代码，添加到第 1 节；如果论文声明将开源，添加到第 2 节

### 阶段 3.5：登记候选证据

- 识别可检验命题，引用 `09-claims/proposition-index.md` 的现有 ID。新命题分配新 ID，登记在待签审区。保留作者报告结果、原文定位、任务与输入、观测单位、数据集、划分、指标、适用范围和两种来源谱系。
- 按 `09-claims/evidence-ledger.schema.json` 准备 v2 JSONL，`status` 为 `pending_review`。证据可记录初判方向 `supports` / `challenges` / `neutral` 及带来源的初步复核说明。实验条件不同的候选记具体差异。
- 通过候选入口登记，随后刷新结构审计和审核队列：

```bash
python3 scripts/research_capability_audit.py add-candidates --input <候选JSONL文件>
python3 scripts/research_capability_audit.py audit --all-fronts --write
```

- 在相关知识页追加论文事实和链接。新的研究前沿可用 `12-research-fronts/research-front-template.md` 建立待签审页，并接入研究前沿索引。正式命题、关系和前沿快照由人工审核与维护者签审更新。

### 阶段 4：更新全局索引

#### 4a. 更新论文注册表

在 `00-dashboard/paper-registry.md` 末尾追加一行，包含新论文的 doi、title_key、year、venue、first_author、filename、note、claims_supported、claims_challenged 字段。后两列用于兼容历史表格，新行填 `—`。

#### 4b. 更新阅读队列

在 `00-dashboard/reading-queue.md` 中添加新论文行，标记状态为 `processed` 或 `important`。

#### 4c. 更新 Dashboard

- 用 `python3 scripts/research_capability_audit.py stats` 从注册表和实际页面生成统计，更新 `00-dashboard/index.md`、`00-dashboard/project-overview.md` 和 README 的当前数字
- `00-dashboard/project-overview.md`：如论文属于重点论文，更新相关章节

#### 4d. 更新参考文献

在 `bibliography.json` 中追加新论文条目，包含：
- citation_key、entry_type、title、authors、year、booktitle/journal、pages、volume、publisher、doi、url
- 通过 CrossRef API 查询官方元数据（优先使用 DOI 查询，无 DOI 则用标题查询）
- 如 API 不可用，从论文笔记 frontmatter 和 parsed markdown 中提取已有字段，标记 `metadata_source: "note"`

更新后重新生成 `bibliography.bib`：
```bash
python3 scripts/generate_bibliography.py --skip-api  # 从 bibliography.json 重新生成 .bib
```

#### 4e. 追加日志

在 `00-dashboard/log.md` 末尾追加：

```markdown
## [YYYY-MM-DD] ingest | 论文标题
- Added:
  - [[论文笔记页面名]]
- Updated:
  - [[概念页名]]
  - [[方法页名]]
  - [[对比表名]]
  - [[open-source-registry]]
  - [[paper-registry]]
  - [[reading-queue]]
- Notes:
  - Reading level: Lx
  - 去重结果：无除外匹配 / 已确认为新论文
```

### 阶段 5：自动更新 README 和 AGENTS（必须执行）

每次入库完成后，**自动**更新以下两个文档，不需要用户额外提醒。

#### 5a. 更新 README.md

检查并更新以下内容：
- **Highlights 部分**：更新论文数量、深度分析论文数量、知识页面数量、开源方法数量等统计数据
- **Key Papers 表格**：如果新论文属于深度分析的核心论文（L3/L4），添加到表格中
- **Research Areas 表格**：如果新论文属于新的研究方向，更新表格

#### 5b. 更新 AGENTS.md

检查并更新以下内容：
- **知识库定位（第 1 节）**：如果新论文引入了新的研究方向，更新研究方向列表
- **知识沉淀层（第 2.3 节）**：如果新增了概念页、方法页、任务页等，更新页面计数
- **论文处理等级（第 4 节）**：无需更新（仅在整体策略变化时修改）

### 阶段 6：Git 提交（仅在用户明确要求时执行）

**重要：本阶段仅当用户明确说"上传"、"提交"、"push"、"commit"等指令时才执行。不要自动执行。**

当用户要求提交时：
1. 执行 `git status` 查看变更
2. 执行 `git add` 添加所有变更文件（排除 `.gitignore` 中的条目，特别是 `10-outputs/`）
3. 生成有意义的 commit message，格式：`ingest: add [论文标题简写] + knowledge layer updates`
4. 执行 `git commit`
5. 仅当用户进一步要求 push 时，才执行 `git push`

**注意**：
- `10-outputs/` 目录已加入 `.gitignore`，不会被提交
- 不要自动 push，commit 后等待用户进一步指示
- 如果有多篇论文批量入库，可以合并为一次 commit

---

## 关键约束

1. **去重检查必须在解析之前执行**：从 PDF 前几页即可提取标题/DOI/摘要，不需要完整解析
2. **知识层更新追加不覆盖**：只在已有页面的表格/列表中追加新行，不修改已有内容
3. **不编造信息**：论文中没有的内容写 `unknown`
4. **完整执行所有阶段（0-5）**：不要跳过任何阶段，除非该阶段明确不需要更新。阶段 0-5 为自动执行，阶段 6 仅在用户要求时执行
5. **保留用户决策权**：去重阶段的疑似重复必须等待用户确认
6. **如果 MinerU 解析失败**：记录错误，但仍然尝试从 PDF 直接提取信息生成笔记
7. **README 和 AGENTS 必须同步更新**：每次入库完成后自动检查并更新，不需要用户提醒
8. **Git 提交仅在用户要求时执行**：不要自动 commit 或 push。`10-outputs/` 目录不参与版本控制

## 研究判断门禁

1. **结构校验**：`validate --all-fronts` 检查 Schema、ID、来源文件、审核字段、快照和索引一致性。
2. **语义复核**：人工对照论文，判断命题方向、证据直接性、研究与数据谱系、评估条件以及反证。有实质疑问的证据为 `contested`；条件可比且结果相反的两项已核验证据分别保留 `verified + supports` 和 `verified + challenges`，由命题记录分歧。
3. **维护者签审**：按 AGENTS.md §11 更新命题和“当前研究认识”，记录签审日期与依据。上一版正文、变更原因、证据 ID 和审核人日期写入历史。证据不足、存在分歧和适用范围未明均为可签审结果。

正常论文入库不因普通字段缺失而阻断；仅当来源丢失、解析严重错误或重要证据不可追溯时，才标记为需要人工处理。

---

## 输出格式

完成全部阶段后，输出一份执行摘要：

```
## 入库完成摘要

### 新论文
- 标题：...
- 笔记：[[...]]

### 去重结果
- 状态：无除外匹配 / 已确认为新论文

### 知识层更新
| 更新项 | 操作 |
|--------|------|
| 概念页 | 更新了 [[xxx]]，[[yyy]] |
| 方法页 | 更新了 [[zzz]] |
| 对比表 | method-comparison-table 新增 1 行 |
| 开源注册表 | 新增 1 个开源方法 / 无需更新 |
| 命题与证据 | 新增 1 条候选证据 / 无需更新 |
| 研究前沿 | 关联 [[xxx-front]] 的候选项 / 新建待签审前沿 / 无需更新 |

### 全局更新
- paper-registry.md：新增 1 行（#51，两列历史 Claims 计数填 `—`）
- reading-queue.md：新增 1 行
- index.md：计数更新
- bibliography.json：新增 1 条条目（citation_key: xxx）
- bibliography.bib：已重新生成
- log.md：已追加日志

### 文档同步
- README.md：已更新 / 无需更新
- AGENTS.md：已更新 / 无需更新

### Git 状态
- 未提交（等待用户指示） / 已提交（commit hash: ...）
```

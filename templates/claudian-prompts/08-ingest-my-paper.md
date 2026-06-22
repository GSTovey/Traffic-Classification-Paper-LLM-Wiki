# 个人论文入库任务

你是一名计算机领域专家和 Obsidian 论文知识库维护者。本提示词将引导你完成个人论文的入库流程。

**核心约束**：个人论文严格隔离于主知识库，不触发 04-09 的任何更新。

---

## 输入

用户会提供以下信息之一：
- 个人论文的 PDF 路径
- 个人论文的 LaTeX/Word 源文件内容
- 个人论文的 MinerU Markdown 路径
- 直接口述论文内容

---

## 完整流程

### 阶段 0：去重检查（针对个人论文注册表）

1. 读取 `11-my-papers/my-paper-registry.md`
2. 从新论文中提取标题、作者、年份
3. 检查是否与已有个人论文重复（标题关键词匹配 + 作者年份交叉验证）
4. 输出去重结果：
   - **无重复** → 继续阶段 1
   - **疑似重复** → 列出候选，**暂停等待用户确认**
   - **确定重复** → 报告已有笔记链接，结束

### 阶段 1：材料准备（可选）

根据用户提供的方式处理：

| 提供方式 | 操作 |
|---|---|
| PDF 路径 | 确认文件存在；如需 MinerU 解析，仅在用户要求时执行 |
| LaTeX/Markdown 内容 | 直接使用，跳过解析 |
| 口述内容 | 直接使用，跳过解析 |

### 阶段 2：生成个人论文笔记

1. 读取论文内容
2. 按 `templates/my-paper-note-template.md` 生成笔记
3. 确保 frontmatter 包含所有字段，特别是：
   - `type: my-paper`
   - `my_confidence`：根据用户描述和论文状态设定（保留用户最终决策权）
   - `publication_status`：根据用户说明设定
   - `kb_read_only: true`
4. 保存到 `11-my-papers/notes/`，文件名遵循命名规范：`YEAR-VENUE-Short_Title.md`（如未发表，venue 用目标 venue 或 `draft`）

### 阶段 3：建立研究连接（只读方向）

1. 读取论文内容，判断涉及主知识库中的哪些概念、方法、任务
2. 在笔记的 §3（研究连接）中填入对应的 `[[]]` 链接
3. 检查 `00-dashboard/open-questions.md` 和 `09-claims/` 中的页面，填入 §3.5
4. **关键约束**：
   - **只在个人论文笔记中添加指向主知识库的链接**
   - **不修改主知识库中的任何页面**
   - **不向 `04-concepts/`、`05-methods/`、`06-tasks/`、`07-surveys/`、`08-comparisons/`、`09-claims/` 追加任何内容**

### 阶段 4：更新个人论文注册表

在 `11-my-papers/my-paper-registry.md` 末尾追加一行，包含 doi、title_key、year、venue_target、status、confidence、filename、note 字段。

### 阶段 5：更新研究轨迹

1. 读取 `11-my-papers/my-research-thread.md`
2. 在 §2（研究时间线）中追加新论文行
3. 更新 §3（研究主题图）中相关的方向
4. 更新 §7（统计）中的计数

### 阶段 6：追加日志

在 `00-dashboard/log.md` 末尾追加：

```markdown
## [YYYY-MM-DD] [my-paper] ingest | 论文标题
- Added:
  - [[个人论文笔记页面名]]
- Updated:
  - [[my-paper-registry]]
  - [[my-research-thread]]
- Notes:
  - Confidence: high / medium / low / uncertain
  - Status: draft / submitted / accepted / published
  - 主知识库未更新（隔离规则）
```

### 阶段 7：更新文档（最小化）

- `00-dashboard/index.md`：在 11-my-papers 区域更新个人论文计数
- **不更新** README.md 的主知识库论文总数（个人论文不计入）
- **不更新** AGENTS.md

---

## 晋升至主知识库

当论文发表或用户认可其质量，要求将个人论文晋升至主知识库时：

### 前置条件

- `publication_status` 为 `accepted` 或 `published`，**或**用户明确表示认可论文质量
- `my_confidence` 为 `high` 或 `medium`（用户主动认可时可为 `medium`）
- **用户主动要求晋升**（不自动触发）

### 晋升流程

1. 在 `03-paper-notes/` 中使用 `templates/paper-note-template.md` 创建**全新的标准笔记**
2. 对晋升论文执行完整的 `06-ingest-pipeline.md` 入库流程（阶段 0-5），包括：
   - 去重检查（比对 `paper-registry.md`）
   - MinerU 解析（如未解析）
   - 生成标准论文笔记（包含摘要翻译、方法分析、实验总结等完整结构）
   - **更新知识层**（04-09 概念页、方法页、任务页、综述页、对比表、Claims）
   - 更新全局索引（paper-registry、reading-queue、index）
   - 更新 README 和 AGENTS
3. 个人论文笔记**保留在** `11-my-papers/notes/`，不删除
4. 在个人论文笔记的 frontmatter 中添加：`promoted_to: "03-paper-notes/xxx.md"`
5. 在个人论文笔记 §0 基础信息表中更新晋升状态
6. 更新 `my-research-thread.md` 时间线中的晋升状态列
7. 在 `my-paper-registry.md` 统计中更新"已晋升至主知识库"计数

### 晋升后的关系

```
11-my-papers/notes/xxx.md  (type: my-paper, promoted_to: "03-paper-notes/xxx.md")
    ↑ 研究轨迹视角：个人反思、后续计划、质量评估
    ↓ 通过 promoted_to 字段关联

03-paper-notes/xxx.md  (type: paper, 标准 14 节结构)
    ↑ 主知识库视角：完整方法分析、知识层连接、跨论文关联
```

---

## 关键约束

1. **严格隔离**：不得创建或修改 `04-concepts/`、`05-methods/`、`06-tasks/`、`07-surveys/`、`08-comparisons/`、`09-claims/` 中的任何文件
2. **只读连接**：个人论文笔记可以链接到主知识库页面，但主知识库页面不得被修改
3. **独立注册表**：个人论文使用 `my-paper-registry.md`，不使用 `paper-registry.md`
4. **不编造信息**
5. **保留用户对 `my_confidence` 的最终决策权**
6. **Git 提交仅在用户要求时执行**

---

## 输出格式

完成全部阶段后，输出执行摘要：

```markdown
## 个人论文入库完成摘要

### 新论文
- 标题：...
- 笔记：[[...]]
- Confidence：...
- Status：...

### 去重结果
- 状态：无重复匹配 / 已确认为新论文

### 研究连接
| 连接类型 | 目标 |
|---|---|
| 概念 | [[xxx]], [[yyy]] |
| 方法 | [[zzz]] |
| 任务 | [[www]] |
| 相关论文 | [[aaa]], [[bbb]] |

### 更新项
| 更新项 | 操作 |
|---|---|
| my-paper-registry | 新增 1 行 |
| my-research-thread | 更新时间线和统计 |
| log.md | 已追加日志 |

### 隔离确认
- 主知识库（04-09）：✓ 未修改
- paper-registry.md：✓ 未修改
- reading-queue.md：✓ 未修改
```

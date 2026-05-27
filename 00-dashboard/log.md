# Knowledge Base Log

本文件用于记录 Traffic_Papers 知识库的维护历史。
原则上只追加，不删除历史记录。

---

## [2026-05-27] init | Create Traffic_Papers framework

- Created Obsidian vault framework for paper knowledge management.
- Created directories for PDF files, MinerU Markdown files, paper notes, concepts, methods, tasks, surveys, comparisons, claims, and outputs.
- Created templates for paper notes and knowledge pages.
- Created Claudian prompt templates for paper ingestion, knowledge base update, deep method analysis, reproduction analysis, and quality check.
- Created AGENTS.md to define the knowledge base maintenance rules.

Next steps:

- Import PDF files into `00-inbox/PDFs/`.
- Use MinerU to convert PDFs into Markdown and place them in `02-parsed-markdown/`.
- Use Claudian to generate structured paper notes in `03-paper-notes/`.

---

## [2026-05-27] parse | MinerU Batch PDF Parsing

- Added:
  - 50 篇 PDF 通过 MinerU API 批量解析为 Markdown
  - 输出位于 `02-parsed-markdown/`，原始结果位于 `01-mineru-output/`
- Notes:
  - 使用 `scripts/mineru_batch_parse.py`，vlm 模型，5 批次，全部成功

---

## [2026-05-27] ingest | Batch Paper Note Generation

- Added:
  - 50 篇结构化中文论文笔记，位于 `03-paper-notes/`
- Notes:
  - 每篇笔记包含 YAML frontmatter + 0-12 章节
  - 使用中文撰写，保留英文专业术语

---

## [2026-05-27] refactor | Directory Cleanup and Naming Unification

- Changed:
  - `00_Inbox` → `00-inbox`
  - `01_MinerU_Output` → `01-mineru-output`
  - `02_Parsed_Markdown` → `02-parsed-markdown`
  - `99_Logs` → `99-logs`
- Removed:
  - `01-pdf/`（空目录，与 `00-inbox/PDFs` 重复）
  - `02-mineru-md/`（空目录，与 `02-parsed-markdown` 重复）
  - `03_Paper_Notes/`（空目录，与 `03-paper-notes` 重复）
  - `04_Cards/`（空目录）
- Notes:
  - 统一使用连字符命名风格
  - 更新了 AGENTS.md、dashboard、脚本中的路径引用

---

## [2026-05-27] supplement | Dashboard Update & Knowledge Pages Supplement

- Updated:
  - `00-dashboard/index.md` — 更新页面计数、链接验证
  - `00-dashboard/reading-queue.md` — 50 篇论文状态标记
  - `00-dashboard/open-questions.md` — 16 条开放研究问题
  - `00-dashboard/research-map.md` — 链接指向实际存在的页面
- Added:
  - 5 个任务页：encrypted-traffic-detection, app-fingerprinting, anomaly-detection, tunnel-detection, traffic-representation
  - 4 个综述页：survey-traffic-foundation-model, survey-website-fingerprinting, survey-malicious-traffic-detection, survey-few-shot-learning
  - `00-dashboard/quality-check-report.md`
- Notes:
  - 知识层总计：9 概念 + 8 方法 + 8 任务 + 5 综述 + 2 对比 + 2 Claims = 34 个页面

---

## [2026-05-27] cleanup | Broken Wikilinks Cleanup & LLM/Multi-agent Content Removal

- Removed:
  - `04-concepts/llm-for-cybersecurity.md` — 用户研究方向暂不涉及 LLM/多智能体
- Updated:
  - `00-dashboard/index.md` — 同步最新数字，移除 LLM/multi-agent 引用，补充任务页和综述页列表
  - `00-dashboard/research-map.md` — 移除 LLM/multi-agent 条目，添加新任务页和综述页
  - `00-dashboard/open-questions.md` — 修复 llm-for-cybersecurity 断链
  - `AGENTS.md` — 更新研究方向列表，移除 LLM/multi-agent 方向
  - 9 个概念页（04-concepts/）— 清除断链，转换为纯文本
  - 8 个方法页（05-methods/）— state-space-model.md 修复 6 个断链
  - 8 个任务页（06-tasks/）— 清除断链
  - 5 个综述页（07-surveys/）— 清除断链
  - ~50 篇论文笔记（03-paper-notes/）— 清除断链
- Notes:
  - 概念页中大量使用人类可读名称（如 `[[Contrastive Learning]]`）而非 kebab-case（`[[contrastive-learning]]`），全部转为纯文本
  - 论文笔记中 paper title 级别的 wikilinks 全部转为纯文本
  - 修复总计约 200+ 条断链

---

## [2026-05-27] deep-analysis | 14 篇重点论文深度分析

- Updated:
  - 14 篇 CCF B+ 论文笔记完成深度分析，涵盖 6 个研究主题
- Papers analyzed (by topic):
  - **加密流量预训练/基础模型**：SoK (S&P 2025), Sweet Danger (SIGCOMM 2025), MM4flow (CCS 2025), ET-BERT (WWW 2022)
  - **恶意加密流量检测**：1‰ Samples (CCS 2025), SmartDetector (TIFS 2025)
  - **网站指纹攻击与防御**：Swallow (CCS 2025), USENIX 2023 RF, USENIX 2024 Proxy, S&P 2024 Palette
  - **匿名/应用流量分类**：AN-Net (WWW 2024), Flowprint (NDSS 2020)
  - **少样本/开放集学习**：Open-Set Semi-Supervised (TIFS 2026), YaTC (AAAI 2023)
- Enhancement summary:
  - 总计 14 篇笔记从 ~400 行扩展至 600-760 行
  - 新增 ~200 条证据记录
  - 每篇论文新增方法公式推导、消融实验分析、跨论文关联
  - 重点增强 Sections 3-7 和 10
- Notes:
  - 3 批并行处理（5+5+4 agents），总耗时约 20 分钟
  - 跨论文关联：ET-BERT - YaTC - MM4flow - Sweet Danger - SoK 形成完整方法演进链
  - SmartDetector - 1‰ Samples 形成恶意检测方法对比
  - Swallow - USENIX 2023 - S&P 2024 形成 WF 攻防三角

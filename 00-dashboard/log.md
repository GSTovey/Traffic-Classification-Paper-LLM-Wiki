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

---

## [2026-05-27] supplement | Project Overview Document Creation

- Added:
  - `00-dashboard/project-overview.md` — 项目全景速览文档（302 行）
- Updated:
  - `00-dashboard/index.md` — 核心入口表增加 project-overview 和 quality-check-report 链接
- Notes:
  - 文档定位：任何智能体首次接触知识库时的 2 分钟对齐入口
  - 涵盖 16 个章节：定位、架构、目录速查、研究方向、深度论文、Claims、矛盾、质量问题、入库流程、笔记结构、命名规范、写作规则、场景导航、工具链、时间线、智能体说明
  - 包含 6 个场景导航（综述写作、方法对比、论文复现、Research Gap、新论文入库、质量检查）

---

## [2026-05-29] supplement | 开源注册表创建与全局更新

- Added:
  - `08-comparisons/open-source-registry.md` — 开源模型/方法注册表
    - 21 个已确认开源的方法/模型（含仓库地址、功能、用法、语言）
    - 3 个计划开源/待确认的方法
    - 20+ 个高频对比基线但暂未找到开源地址的方法（按领域分类）
    - 6 个 CLET 论文确认有公开实现但缺具体地址的方法
    - 16 个第三方参考工具（流量分析、混淆代理、基础设施）
- Updated:
  - `08-comparisons/method-comparison-table.md` — 新增"开源"和"代码地址"两列，18 个方法全部标注开源状态
  - `00-dashboard/index.md` — 综述页与对比表节新增 open-source-registry 链接，对比表数量 2→3
- Notes:
  - 知识库对比页从 2 个增至 3 个（method-comparison-table, dataset-comparison-table, open-source-registry）
  - 高频基线追踪：AppScanner (10+ 篇)、TSCRNN (7+ 篇)、FlowPic (5+ 篇)、CUMUL (5+ 篇) 为最常被对比但无开源地址的方法
  - 所有信息来源于 50 篇论文笔记的 frontmatter `code` 字段和 Section 7.1 内容

---

## [2026-05-29] supplement | 入库去重机制与一键管道

- Added:
  - `00-dashboard/paper-registry.md` — 论文去重注册表（50 篇论文的 DOI/标题/作者/年份/venue 索引）
  - `templates/claudian-prompts/00-check-duplicate.md` — 去重检查提示词（三轮匹配：DOI 精确、标题关键词、作者+年份+venue 交叉）
  - `templates/claudian-prompts/06-ingest-pipeline.md` — 一键入库管道（去重 → 解析 → 笔记 → 知识层全量更新 → 全局索引）
- Updated:
  - `AGENTS.md` — §5 入库流程新增步骤 0 去重检查 + §5.2 一键入库流程
  - `00-dashboard/project-overview.md` — §9 入库流程从 15 步扩展为 17 步（含去重和注册表更新）、场景 E 更新为一键流程
  - `00-dashboard/index.md` — 核心入口表新增 paper-registry 链接
- Notes:
  - 去重策略：用户选择"询问后决定"模式，疑似重复时暂停列出候选
  - 一键管道覆盖：去重 → MinerU 解析 → 笔记生成 → 概念/方法/任务/综述/对比表/开源注册表/Claims 更新 → paper-registry/reading-queue/index/log 更新
  - 注册表字段：doi, title_key（归一化标题）, year, venue, first_author, filename, note

---

## [2026-05-29] quality-check | 知识库质量复查与报告更新

- Updated:
  - `00-dashboard/quality-check-report.md` — 全面重写，更新为 2026-05-29 状态
  - `00-dashboard/project-overview.md` — 修复格式错误链接 `[[AGENTS.md]]` → `[[AGENTS]]`
- Notes:
  - 复查结果：断链从 ~300 条降至 27 条（仅 dashboard 待创建页面），实验章节 2 篇已修复
  - 未修复：12 篇旧格式 frontmatter、12 篇缺失 mineru_md、3 篇缺失 pdf、1 篇 pdf 指向错误
  - 新发现：project-overview.md 中 `[[AGENTS.md]]` 格式错误，已修复
  - 剩余断链全部位于 dashboard 待扩展页面章节，指向 13 个尚未创建的概念/方法页面

---

## [2026-05-29] fix | 12 篇论文 Frontmatter 统一修复

- Updated:
  - 12 篇论文笔记的 YAML frontmatter 全部重构为标准格式
  - `00-dashboard/quality-check-report.md` — 更新状态：frontmatter/pdf/mineru_md 全部标记为已修复
- Fixed papers:
  - `2018-CS-An_Efficient_Feature_Generation...md`
  - `2018-Trans_IFS-Robust_Smartphone_App...md`
  - `2019-INFOCOM-FS-Net...md`
  - `2022-HPCC-MTBD_HTTPS_Tunnel...md`
  - `2022-ICMLA-Separating_Flows...md`
  - `2022-TBD-Identification_of_Encrypted...md`
  - `2022-WWW-ET-BERT...md`
  - `2023-AAAI-Yet_Another_Traffic_Classifier...md`
  - `2023-ComputerNetworks-Few-shot_encrypted...md`
  - `2023-SIGKDD-A_lightweight__efficient...md`
  - `2023-USENIX-Subverting_Website...md`
  - `2024-INFOCOM-Causality_Correlation...md`
- Notes:
  - 修复内容：title→title_original+title_cn, 新增 mineru_md (12篇)、pdf (3篇)、修正 pdf 指向 (3篇 .md→.pdf)
  - 移除非标准字段：keywords, date_added, date_created, related_papers, affiliations, topic, project, arxiv
  - 新增标准字段：research_area, task, method, dataset, code, relevance
  - 修复后：50/50 篇标准格式 frontmatter，50/50 篇有 pdf 路径，50/50 篇有 mineru_md 路径

---

## [2026-05-29] ingest | 批量入库 29 篇新论文

- Added:
  - 29 篇新论文笔记（`03-paper-notes/`），知识库总量从 50 篇增至 79 篇
  - 29 篇 PDF 导入 `00-inbox/PDFs/`
  - 30 份 MinerU Markdown 生成至 `02-parsed-markdown/`（含 1 篇已存在）
- Updated:
  - `00-dashboard/paper-registry.md` — 新增 29 条注册记录（#51–#79），统计更新至 79 篇
  - `00-dashboard/reading-queue.md` — 新增 17 条阅读队列条目（12 篇已在队列中）
  - `00-dashboard/index.md` — 论文数量 50→79，PDF/MinerU/笔记/对比表计数同步更新
- New papers by venue:
  - **顶级会议**：S&P (TrafficFormer), CCS (MetaTraffic), KDD (Wedjat, Traffic-Explainer), NeurIPS (FlowRefiner), NDSS (Black-Box Evasion), USENIX Security (CertTA)
  - **知名期刊**：TDSC (DAIR-FedMoE), TON (P2P Detection), JCN (6 篇), TNSM, TSC, CCPE
  - **其他**：ICASSP, arXiv (Bias, Nethira, TrafficMoE)
- Research topics:
  - 流量分类：19 篇（预训练模型、MoE、联邦学习、噪声鲁棒、可视化、多模态）
  - 恶意流量检测：6 篇（逃逸攻击、P2P 攻击、动态分类、数据稀缺）
  - 对抗鲁棒性：2 篇（CertTA、Black-Box Evasion）
  - 可解释性：1 篇（Traffic-Explainer）
  - 偏差分析：1 篇（Bias in the Shadows）
- Notes:
  - 来源：`/Users/tovey/Downloads/Papers2read/`（37 篇 PDF）
  - 去重：3 篇与已有论文重复，已跳过
  - MinerU 解析：30 篇新解析（1 篇已有解析）
  - 笔记级别：L2（标准阅读）
  - 处理方式：4 批并行 Agent 生成笔记

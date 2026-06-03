---
type: dashboard
purpose: project-quick-reference
created: "2026-05-27"
updated: "2026-06-01"
---

# Traffic_Papers 项目全景速览

> **用途**：任何智能体（Claude / Claudian / 其他 LLM）在首次接触本知识库时，阅读本文档即可在 2 分钟内完成上下文对齐。避免重复探索、遗漏关键信息。

---

## 1. 一句话定位

Traffic_Papers 是一个基于 Obsidian 的**网络流量安全研究论文知识库**，当前收录 79 篇顶级会议/期刊论文，服务于综述写作、项目申报、方法比较和实验复现。

---

## 2. 三层架构

```
┌─────────────────────────────────────────────────────────┐
│  第三层：知识沉淀层（04–10）                               │
│  概念页·方法页·任务页·综述页·对比表·Claims·输出             │
├─────────────────────────────────────────────────────────┤
│  第二层：论文笔记层（03）                                  │
│  79 篇结构化中文笔记，每篇 14–57 KB                       │
├─────────────────────────────────────────────────────────┤
│  第一层：原始资料层（00–02）                               │
│  PDF 原文 → MinerU API 解析 → 整理后 Markdown             │
└─────────────────────────────────────────────────────────┘
```

**关键原则**：论文主笔记不复制 MinerU 原文；每篇新论文入库时需判断是否更新知识沉淀层。

---

## 3. 目录速查

| 目录 | 内容 | 当前数量 | 快速定位场景 |
|------|------|----------|-------------|
| `00-inbox/PDFs/` | 论文 PDF 原文 | 79 篇 | 查原文、定位引用 |
| `01-mineru-output/` | MinerU 原始解析（已 gitignore） | 79 份 | 调试解析问题 |
| `02-parsed-markdown/` | 整理后的 MinerU Markdown | 79 份 | 机器可读原文 |
| `03-paper-notes/` | **结构化论文笔记**（核心） | 79 篇 | 论文分析、证据追踪 |
| `04-concepts/` | 概念页 | 9 个 | 理解领域概念 |
| `05-methods/` | 方法页 | 8 个 | 方法对比、技术选型 |
| `06-tasks/` | 任务页 | 8 个 | 任务定义、输入输出 |
| `07-surveys/` | 综述页 | 5 个 | 综述写作素材 |
| `08-comparisons/` | 对比表（含开源注册表） | 3 个 | 横向比较、代码追踪 |
| `09-claims/` | 观点与矛盾 | 2 个 | 论证、找 research gap |
| `10-outputs/` | 草稿、报告、复现笔记 | 空 | 写作产出 |
| `00-dashboard/` | 导航、队列、地图、日志 | 6 个文件 | 项目状态总览 |

---

## 4. 重点研究方向

| 方向 | 相关页面 | 核心论文数 |
|------|----------|-----------|
| 加密流量分析与分类 | [[encrypted-traffic-analysis]], [[traffic-classification]] | 15+ |
| 流量表征学习与基础模型 | [[traffic-representation-learning]], [[traffic-foundation-model]] | 10+ |
| 网站指纹（攻防） | [[website-fingerprinting]] | 8+ |
| 恶意/异常流量检测 | [[malicious-traffic-detection]], [[anomaly-detection]] | 8+ |
| 少样本/开放集学习 | [[few-shot-traffic-learning]] | 5+ |
| 隧道检测与匿名通信 | [[tunnel-detection]] | 5+ |
| 应用指纹识别 | [[app-fingerprinting]] | 3+ |

---

## 5. 14 篇深度分析论文（L3/L4 级）

这些论文已完成公式推导、消融实验、跨论文关联分析（600–760 行/篇）：

| 论文 | 会议 | 主题 | 笔记路径 |
|------|------|------|----------|
| SoK: Decoding the Enigma | S&P 2025 | 12 种分类器系统化评估 | `03-paper-notes/2025-S&P-SoK...` |
| The Sweet Danger of Sugar | SIGCOMM 2025 | 揭示表征学习评估漏洞 | `03-paper-notes/2025-SIGCOMM-Sweet_Danger...` |
| MM4flow | CCS 2025 | 多模态预训练流量模型 | `03-paper-notes/2025-CCS-MM4flow...` |
| Training with Only 1.0‰ | CCS 2025 | 极端少样本 + 跨模态融合 | `03-paper-notes/2025-CCS-Training_with_Only_1.0...` |
| Swallow | CCS 2025 | 迁移鲁棒网站指纹攻击 | `03-paper-notes/2025-CCS-Swallow...` |
| SmartDetector | TIFS 2025 | 对比学习恶意流量检测 | `03-paper-notes/2025-TIFS-SmartDetector...` |
| ET-BERT | WWW 2022 | 预训练 Transformer 流量分析 | `03-paper-notes/2022-WWW-ET-BERT...` |
| YaTC | AAAI 2023 | 掩码自编码器流量 Transformer | `03-paper-notes/2023-AAAI-Yet_Another_Traffic...` |
| AN-Net | WWW 2024 | 抗噪声匿名流量分类 | `03-paper-notes/2024-WWW-AN-Net...` |
| Flowprint | NDSS 2020 | 半监督移动应用指纹 | `03-paper-notes/2020-NDSS-Flowprint...` |
| Palette | S&P 2024 | 实时网站指纹防御 | `03-paper-notes/2024-S&P-Palette...` |
| RF (Subverting WF) | USENIX 2023 | 突破网站指纹防御 | `03-paper-notes/2023-USENIX-RF...` |
| Proxy Fingerprinting | USENIX 2024 | TLS 握手指纹识别 | `03-paper-notes/2024-USENIX-Proxy...` |
| FEC-OSL | TIFS 2026 | 开放集半监督分类 | `03-paper-notes/2026-TIFS-FEC-OSL...` |

**跨论文关联链**：
- **预训练演进线**：ET-BERT → YaTC → MM4flow → Sweet Danger → SoK
- **恶意检测对比线**：SmartDetector ↔ tFusion (1‰ Samples)
- **WF 攻防三角**：Swallow (攻击) ↔ RF (攻击) ↔ Palette (防御)

---

## 6. 20 条核心 Claims（可直接引用）

> 完整列表见 [[claims-index]]。以下为最高价值的 6 条：

1. **数据集虚假繁荣**：ISCXVPN2016 含 98.9% 未加密流量，USTC-TFC2016 含 94.7%，多数 DL 分类器的高准确率来自对未加密内容的学习（SoK 2025）
2. **SII 过拟合**：匿名化 MAC/IP/端口后 ET-BERT 准确率从 0.96 暴跌至 0.51（SoK 2025）
3. **评估泄漏**：per-packet split 下 ET-BERT F1=96.8%，per-flow split + frozen encoder 下 F1=6.7%（Sweet Danger 2025）
4. **浅层模型仍优**：正确评估下，RF + 手工特征 > 所有深度表征学习模型（Sweet Danger 2025）
5. **多模态突破**：packet length + payload 双模态预训练，加密隧道网站识别准确率提升 84%（MM4flow 2025）
6. **流量似图像非语言**：最优 mask ratio 90%（远高于 NLP 的 <20%），说明流量数据存在大量信息冗余（YaTC 2023）

---

## 7. 8 组关键矛盾（Research Gap 来源）

> 完整列表见 [[contradictions]]。以下为核心冲突：

| 冲突 | 焦点 | 核心分歧 |
|------|------|----------|
| ET-BERT vs Sweet Danger | 加密 payload 可学性 | ET-BERT 声称可学，Sweet Danger 证明是数据泄漏 |
| SoK vs DL 论文群 | DL vs 传统 ML | SoK 认为 DL 高准确率是虚假繁荣，DL 论文声称自动特征学习更优 |
| MM4flow vs Sweet Danger | 表征学习价值 | MM4flow 展示 TB 级预训练突破，Sweet Danger 显示浅层模型仍占优 |
| DeepFingerprinting vs Palette | WF 攻防 | DF 声称攻破防御，Palette 证明新防御可抵御 |
| Palette vs Swallow | WF 防御鲁棒性 | Palette 声称可抵御 SOTA 攻击，Swallow 证明自适应攻击仍可部分攻破 |
| 多数论文 vs Sweet Danger | 评估指标 | micro F1 偏向多数类，掩盖少数类性能，差距可达 30%+ |

---

## 7.5 开源代码生态概览

> 完整注册表见 [[open-source-registry]]。

| 类别 | 数量 | 说明 |
|------|------|------|
| 已确认开源（本库论文） | 26 | 含 GitHub/GitLab 地址，覆盖 6 个研究方向 |
| 计划开源/待确认 | 3 | Swallow、Gated Attention、ByteDance |
| 高频基线无开源地址 | 20+ | AppScanner (10+ 篇)、TSCRNN (7+ 篇)、CUMUL (5+ 篇) 等 |
| 第三方参考工具 | 16 | JA3、Kitsune、混淆协议等 |

**复现提示**：高频基线如 AppScanner、TSCRNN、CUMUL 等虽被广泛对比，但均无开源代码。复现这些方法需参考原论文自行实现或寻找第三方复现。

---

## 8. 当前已知质量问题

> 完整报告见 [[quality-check-report]]

| 问题类型 | 严重程度 | 数量 | 状态 |
|----------|----------|------|------|
| 断裂 wikilinks（指向不存在的页面） | 高 | ~300 条 → 267 个唯一目标 | 部分修复（概念页/方法页断链已转纯文本） |
| 旧格式 frontmatter | 高 | 13 篇论文 | 待修复 |
| 缺少 PDF/MinerU 路径引用 | 高 | 9 篇论文 | 待修复 |
| 概念/方法页面不足 | 中 | ~30-50 个待创建 | 优先创建被 3+ 篇论文引用的页面 |
| 实验章节薄弱 | 中 | 2 篇论文 | 待补充 |

**建议修复优先级**：
1. 统一 13 篇旧格式 frontmatter
2. 补充 9 篇缺失路径引用
3. 创建高频引用概念页（meta-learning, attention-mechanism, autoencoder 等）
4. 修复剩余断链

---

## 9. 论文入库流程（17 步）

> 详细规范见 [[AGENTS]]。推荐使用一键入库管道 `templates/claudian-prompts/06-ingest-pipeline.md` 自动执行全部步骤。

```
0.  去重检查（读取 paper-registry.md，DOI/标题/作者三轮匹配）
1.  确认 PDF 在 00-inbox/PDFs/
2.  确认 MinerU Markdown 在 02-parsed-markdown/
3.  读取 MinerU Markdown
4.  检查 MinerU 抽取质量
5.  生成论文主笔记到 03-paper-notes/（使用 paper-note-template.md）
6.  在主笔记中链接 PDF 和 MinerU Markdown
7.  判断是否更新概念页（04-concepts/）
8.  判断是否更新方法页（05-methods/）
9.  判断是否更新任务页（06-tasks/）
10. 判断是否更新综述页（07-surveys/）
11. 判断是否更新对比表（08-comparisons/）
12. 判断是否更新开源注册表（08-comparisons/open-source-registry.md）
13. 判断是否更新 Claims（09-claims/）
14. 更新 paper-registry.md（追加一行）
15. 更新 reading-queue.md（追加一行）
16. 更新 00-dashboard/index.md
17. 更新 00-dashboard/log.md
```

**去重说明**：步骤 0 读取 `paper-registry.md`，通过 DOI 精确匹配（置信度 100%）、标题关键词匹配（≥70% 重叠 = 高置信度）、作者+年份+venue 交叉验证三轮匹配检测重复。疑似重复时暂停等待用户确认。

**论文处理等级**：

| 等级 | 含义 | 适用场景 |
|------|------|----------|
| L1 | 快速入库 | 扫描性文献，仅基础信息 |
| L2 | 标准阅读 | 普通相关论文（默认） |
| L3 | 深度方法分析 | 核心论文，含公式/消融/关联 |
| L4 | 复现导向 | 准备复现的论文，含代码结构/工程风险 |

---

## 10. 论文笔记标准结构

每篇论文笔记包含 13 个章节：

| 章节 | 内容 |
|------|------|
| Frontmatter | YAML 元数据（20 个标准字段） |
| §0 基础信息 | 作者/年份/会议/方向/方法/数据集 |
| §1 一句话总结 | 核心贡献速记 |
| §2 摘要翻译 | 原文 + 中文翻译 |
| §3 方法动机 | 为什么提出、痛点、核心直觉 |
| §4 方法设计 | Pipeline、模块、公式、优缺点 |
| §5 与其他方法对比 | 创新点、适用场景、对比表 |
| §6 实验表现 | 数据集、Baseline、指标、关键结果 |
| §7 学习与应用 | 开源、复现步骤、迁移价值 |
| §8 总结 | 核心思想 + 速记版 Pipeline |
| §9 知识链接 | 概念/方法/任务/综述/对比表 |
| §10 证据记录 | 关键观点 + 论文依据 + 位置 |
| §11–12 原始资料 & 后续问题 | PDF/MinerU 路径 + 开放问题 |

---

## 11. 文件命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| PDF | `year-firstauthor-shorttitle.pdf` | `2024-zhang-encrypted-traffic-classification.pdf` |
| MinerU MD | `year-firstauthor-shorttitle.raw.md` | `2024-zhang-encrypted-traffic-classification.raw.md` |
| 论文笔记 | `year-firstauthor-shorttitle.md` | `2024-zhang-encrypted-traffic-classification.md` |
| 概念/方法/任务 | `kebab-case.md` | `encrypted-traffic-analysis.md` |

---

## 12. 写作硬规则

1. 使用中文（保留英文专业术语）
2. 不编造论文中没有的信息
3. 不确定内容标注 `unknown` 或"论文未明确说明"
4. 区分：论文明确证明 > 论文声称 > 合理推断 > 不确定
5. 方法必须讲清输入→处理→输出
6. 实验必须记录数据集、Baseline、指标、关键结果
7. 不把完整 MinerU Markdown 复制进论文笔记
8. Claims 必须有证据来源

---

## 13. 快速导航：按场景

### 场景 A：我要写综述
1. 读 [[survey-encrypted-traffic-analysis]] 或对应综述页
2. 查 [[claims-index]] 找可引用观点
3. 查 [[contradictions]] 找研究 Gap
4. 查 [[method-comparison-table]] 和 [[dataset-comparison-table]]
5. 查 [[open-source-registry]] 了解开源生态和高频基线的代码可用性
6. 进入具体论文笔记的 §5（对比）和 §10（证据）

### 场景 B：我要对比方法
1. 查对应方法页（`05-methods/`）
2. 查 [[method-comparison-table]]
3. 查 [[open-source-registry]] 确认方法是否有开源代码
4. 查相关论文笔记的 §4（方法设计）和 §6（实验）

### 场景 C：我要复现一篇论文
1. 找到论文笔记，确认 reading_level ≥ L3
2. 查 [[open-source-registry]] 获取代码仓库地址
3. 查 §7（学习与应用）的复现步骤和超参数
4. 查 §4（方法设计）的详细 Pipeline
5. 如需 L4 级分析，使用 `templates/claudian-prompts/04-reproduction-analysis.md`

### 场景 D：我要找 Research Gap
1. 读 [[contradictions]] 的 8 组冲突
2. 读 [[open-questions]] 的 16 条开放问题
3. 交叉比对 [[claims-index]] 中互相矛盾的观点

### 场景 E：我要入库新论文（推荐一键流程）
1. 将 PDF 放入 `00-inbox/PDFs/`
2. 使用 `templates/claudian-prompts/06-ingest-pipeline.md` 一键完成：
   - 自动去重检查（读取 [[paper-registry]] 比对 DOI/标题/作者）
   - 自动 MinerU 解析
   - 自动生成论文笔记
   - 自动更新全部知识层（概念/方法/任务/综述/对比表/开源注册表/Claims）
   - 自动更新全局索引（paper-registry、reading-queue、index、log）
3. 分步方式（备选）：
   - `templates/claudian-prompts/00-check-duplicate.md` → 去重
   - `templates/claudian-prompts/01-ingest-paper.md` → 笔记生成
   - `templates/claudian-prompts/02-update-knowledge-base.md` → 知识层更新

### 场景 F：我要检查知识库质量
1. 读 [[quality-check-report]] 了解当前问题
2. 使用 `templates/claudian-prompts/05-quality-check.md` 执行检查

---

## 14. 工具链

| 工具 | 用途 | 配置位置 |
|------|------|----------|
| MinerU API | PDF → 结构化 Markdown | `scripts/mineru_batch_parse.py` |
| Claude Code | AI 辅助笔记生成 | `AGENTS.md`（规范）|
| Claudian | Obsidian 内 AI 助手 | `.claudian/claudian-settings.json` |
| Obsidian + Dataview | 知识管理与查询 | `.obsidian/` |
| Paper Note Template | 论文笔记结构 | `templates/paper-note-template.md` |
| Claudian Prompts | 7 种标准化工作流 | `templates/claudian-prompts/00–06` |
| Paper Registry | 论文去重索引 | `00-dashboard/paper-registry.md` |

---

## 15. 版本与时间线

| 时间 | 事件 |
|------|------|
| 2026-05-27 | 知识库框架创建、目录结构建立 |
| 2026-05-27 | 50 篇 PDF 通过 MinerU 批量解析 |
| 2026-05-27 | 50 篇结构化论文笔记批量生成 |
| 2026-05-27 | 目录命名统一（连字符风格）、旧目录清理 |
| 2026-05-27 | Dashboard 更新、知识页补充至 34 个 |
| 2026-05-27 | 断链清理（~200+ 条）、LLM/多智能体内容移除 |
| 2026-05-27 | 14 篇重点论文深度分析（L3 级） |
| 2026-05-29 | 开源注册表创建、方法对比表增加开源列、知识层增至 35 个 |
| 2026-05-29 | 29 篇新论文批量入库（Papers2read），知识库总量增至 79 篇，开源注册表增至 26 个，方法对比表增至 26 个 |

---

## 16. 给智能体的特别说明

**你是谁？** 你正在操作一个 Obsidian 论文知识库，不是在写代码。所有输出都是 Markdown 笔记。

**最重要的事**：
- **不编造信息**。不确定就写 `unknown`。
- **不破坏已有内容**。先读再改，增量更新。
- **遵守 AGENTS.md**。这是你的操作手册。
- **中文为主**。专业术语保留英文。
- **用 `[[wikilink]]` 链接**。确保链接目标存在。
- **每次操作写日志**。追加到 `00-dashboard/log.md`。

**断链处理**：概念页和方法页中的 wikilinks 如指向不存在的页面，应转为纯文本（不保留 `[[]]` 语法），避免产生断裂链接。待对应页面创建后再恢复为 wikilink。

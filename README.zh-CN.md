# Traffic Classification Paper Wiki

[English](./README.md)

基于 Obsidian 的**网络流量分类**、**加密流量分析**和**流量基础模型**研究论文知识库。收录 147 篇来自顶级会议/期刊（CCS、S&P、USENIX、NDSS、SIGCOMM、INFOCOM、AAAI、NeurIPS、TIFS、TSC、WWW、KDD 等）的结构化论文笔记，覆盖 2008--2026 年的研究成果。

---

## 亮点

- **147 篇结构化论文笔记**，中英双语 frontmatter，含方法分析与证据追踪
- **74 篇深度分析论文**（CCF A/B 级），含公式推导、消融实验、跨论文关联
- **39 个知识页面**：11 概念页 + 8 方法页 + 8 任务页 + 5 综述页 + 5 对比表 + 2 索引页
- **6 个活跃研究前沿**，追踪收敛/分歧研究问题，含证据链和 Auto Research 指引
- **共识权重系统**：venue 等级 × 时间衰减 × 引用影响三维评分
- **30 个已确认开源方法**，含 GitHub/GitLab 代码仓库
- **参考文献库**：147 篇结构化 BibTeX 条目（`bibliography.json` + `bibliography.bib`），数据来自 CrossRef、OpenAlex、Semantic Scholar（86% 含 DOI）
- **研究地图**按主题、方法和会议交叉索引

## 目录结构

```
Traffic_Papers/
├── 00-inbox/
│   └── PDFs/              # 147 篇论文 PDF 原文
├── 01-mineru-output/       # MinerU 原始解析结果（已 gitignore，可重新生成）
├── 02-parsed-markdown/     # MinerU 解析后的 Markdown
├── 03-paper-notes/         # 结构化论文笔记（147 篇）★
├── 04-concepts/            # 概念页（11 个）★
├── 05-methods/             # 方法页（8 个）★
├── 06-tasks/               # 任务页（8 个）★
├── 07-surveys/             # 综述页（5 个）★
├── 08-comparisons/         # 对比表（5 个，含开源注册表）★
├── 09-claims/              # 观点与矛盾记录（2 个）★
├── 10-outputs/             # 草稿、报告、复现笔记（已 gitignore）
├── 12-research-fronts/     # 研究前沿追踪（6 个前沿 + 索引 + 模板）★
├── 00-dashboard/           # 阅读队列、研究地图、开放问题
├── bibliography.json       # 结构化 BibTeX 元数据（147 条）
├── bibliography.bib        # LaTeX 可用 BibTeX 文件（可直接复制）
├── scripts/                # MinerU 批量解析 + 参考文献生成脚本
└── templates/              # 笔记模板
```

## 研究方向

| 方向 | 涵盖主题 |
|------|----------|
| **流量检测与分类** | 加密流量分类、恶意流量检测、异常检测、隧道检测 |
| **表征学习与基础模型** | 预训练范式（ET-BERT、YaTC、MM4flow）、多模态融合、对比学习 |
| **网站指纹** | 攻击（Deep Fingerprinting、Swallow）与防御（Palette、FRONT） |
| **少样本与开放集学习** | 元学习、半监督学习、开放集识别 |
| **应用指纹** | 移动应用识别、匿名流量分类（Tor、I2P） |

## 深度分析论文列表

| 论文 | 会议 | 主题 |
|------|------|------|
| SoK: Decoding the Enigma | S&P 2025 | 12 种流量分类器系统化评估 |
| The Sweet Danger of Sugar | SIGCOMM 2025 | 颠覆表征学习现有结论 |
| MM4flow | CCS 2025 | 多模态预训练流量模型 |
| Training with Only 1.0‰ Samples | CCS 2025 | 跨模态融合 + 极端少样本 |
| Swallow | CCS 2025 | 迁移鲁棒网站指纹攻击 |
| SmartDetector | TIFS 2025 | 对比学习恶意流量检测 |
| ET-BERT | WWW 2022 | 预训练 Transformer 流量分析 |
| YaTC | AAAI 2023 | 掩码自编码器流量 Transformer |
| AN-Net | WWW 2024 | 抗噪声匿名流量分类 |
| Flowprint | NDSS 2020 | 半监督移动应用指纹 |
| Palette | S&P 2024 | 实时网站指纹防御 |
| RF | USENIX 2023 | 突破网站指纹防御体系 |
| Proxy Fingerprinting | USENIX 2024 | 封装 TLS 握手指纹识别 |
| FEC-OSL | TIFS 2026 | 开放集半监督分类 |

## 使用方法

本仓库是一个 **Obsidian 知识库**。使用步骤：

1. 克隆本仓库
2. 在 [Obsidian](https://obsidian.md/) 中打开该文件夹作为知识库
3. 从 `00-dashboard/index.md` 开始浏览
4. 使用 `00-dashboard/reading-queue.md` 跟踪阅读进度
5. 使用 `00-dashboard/research-map.md` 按主题探索

## 工具与流程

- **PDF 解析**：[MinerU](https://github.com/opendatalab/MinerU) API 将 PDF 转为结构化 Markdown
- **笔记生成**：Claude Code（AI 辅助结构化笔记生成）
- **知识管理**：Obsidian + Dataview 插件
- **参考文献库**：`bibliography.json` + `bibliography.bib`，147 条 BibTeX 条目（CrossRef/OpenAlex/Semantic Scholar 官方数据）
- **自动化工作流**：一键入库管道（去重 → 解析 → 笔记生成 → 知识层全量更新 → 参考文献更新 → README/AGENTS 同步）
- **去重方法**：五轮联合匹配（文件名 + 标题 + 摘要 + DOI + 作者/年份/venue）

## 工作流程

当新论文 PDF 加入知识库时，系统自动执行：

1. 与已有 147 篇论文进行去重检查（文件名 + 标题 + 摘要 + DOI + 作者/venue）
2. 通过 MinerU API 解析 PDF（如 `MINERU_API_TOKEN` 未设置则暂停向用户索要）
3. 自动提取关键框架图（`extract_key_figures.py`）
4. 生成包含中英双语 frontmatter 的结构化论文笔记
5. 更新所有相关知识页面（概念、方法、任务、综述、对比表、观点索引）
6. 更新研究前沿证据链（如论文与活跃前沿相关）
7. 更新全局索引（论文注册表、阅读队列、仪表盘）
8. 更新 `bibliography.json` 并重新生成 `bibliography.bib`
9. 同步更新 README.md 和 AGENTS.md 统计数据

Git 提交**仅在用户明确要求时执行**。`10-outputs/` 目录（草稿、报告、项目申报）不参与版本控制。

## 许可说明

本仓库包含用于研究目的的学术论文笔记。所有论文版权归原作者和出版方所有。

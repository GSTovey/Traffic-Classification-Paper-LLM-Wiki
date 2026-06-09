# Traffic Classification Paper Wiki

[English](./README.md)

基于 Obsidian 的**网络流量分类**、**加密流量分析**和**流量基础模型**研究论文知识库。收录 92 篇来自顶级会议/期刊（CCS、S&P、USENIX、NDSS、SIGCOMM、INFOCOM、AAAI、NeurIPS、TIFS、TSC、WWW、KDD 等）的结构化论文笔记，覆盖 2008--2026 年的研究成果。

---

## 亮点

- **92 篇结构化论文笔记**，中英双语 frontmatter，含方法分析与证据追踪
- **14 篇深度分析论文**（CCF A/B 级），含公式推导、消融实验、跨论文关联
- **35 个知识页面**：9 概念页 + 8 方法页 + 8 任务页 + 5 综述页 + 5 对比表 + 2 索引页
- **26 个已确认开源方法**，含 GitHub/GitLab 代码仓库
- **研究地图**按主题、方法和会议交叉索引

## 目录结构

```
Traffic_Papers/
├── 00-inbox/
│   └── PDFs/              # 92 篇论文 PDF 原文
├── 01-mineru-output/       # MinerU 原始解析结果（已 gitignore，可重新生成）
├── 02-parsed-markdown/     # MinerU 解析后的 Markdown（92 份）
├── 03-paper-notes/         # 结构化论文笔记（92 篇）★
├── 04-concepts/            # 概念页（9 个）★
├── 05-methods/             # 方法页（8 个）★
├── 06-tasks/               # 任务页（8 个）★
├── 07-surveys/             # 综述页（5 个）★
├── 08-comparisons/         # 对比表（5 个，含开源注册表）★
├── 09-claims/              # 观点与矛盾记录（2 个）★
├── 10-outputs/             # 草稿、报告、复现笔记
├── 00-dashboard/           # 阅读队列、研究地图、开放问题
├── scripts/                # MinerU 批量解析脚本
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

## 许可说明

本仓库包含用于研究目的的学术论文笔记。所有论文版权归原作者和出版方所有。

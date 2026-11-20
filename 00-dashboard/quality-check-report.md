# Traffic_Papers 知识库质量检查报告

> **当前记录（2026-11-20）**见 [[#2026-11-20　全库结构与论文笔记补齐]]。七条前沿结构验收见 [[research-capability-audit]]。下方截至 2026 年 6 月的检查保留为历史快照。

**初始检查时间**: 2026-05-27
**最近更新时间**: 2026-06-10
**检查范围**: 03-paper-notes (92 篇)、04-concepts (9 个)、05-methods (8 个)、06-tasks (8 个)、07-surveys (5 个)、08-comparisons (5 个)、09-claims (2 个)

---

## 1. 总体结论

知识库整体框架完整，92 篇论文笔记均有 YAML frontmatter 和基本结构，其中 40 篇已完成 L3/L4 级深度分析。自 2026-05-27 首次检查以来，所有已知问题均已修复。

### 当前状态速览

| 问题类型 | 初始状态 (05-27) | 当前状态 (06-09) | 严重程度 | 状态 |
|----------|------------------|------------------|----------|------|
| 断裂 wikilinks | ~300 条 → 267 个唯一目标 | **0 条** | — | ✅ 已全部修复 |
| 旧格式 frontmatter | 13 篇 | **0 篇** | — | ✅ 已修复 |
| 缺少 `pdf:` 路径引用 | 9 篇 | **0 篇** | — | ✅ 已修复 |
| 缺少 `mineru_md:` 路径引用 | 9 篇 | **0 篇** | — | ✅ 已修复 |
| 缺少 research_area/task/method | 34 篇 | **0 篇** | — | ✅ 已修复 |
| 实验章节薄弱 | 2 篇 | 0 篇 | — | ✅ 已修复 |
| 概念/方法页面不足 | ~30-50 个待创建 | 13 个待创建（纯文本引用） | 低 | 📋 已记录 |
| 格式错误链接 | — | 0 个 | — | ✅ 已修复 |
| frontmatter 路径不一致 | — | 0 篇 | — | ✅ 已修复 |

---

## 2. 已修复的问题

### 2.1 断裂 wikilinks 清理（✅ 已完成）

**修复时间**: 2026-05-27
**修复方式**: 概念页、方法页、任务页、综述页中的断链全部转为纯文本

**当前断链分布**：

| 目录 | 断链数 | 状态 |
|------|--------|------|
| `03-paper-notes/` | 0 | ✅ 清理完成 |
| `04-concepts/` | 0 | ✅ 清理完成 |
| `05-methods/` | 0 | ✅ 清理完成 |
| `06-tasks/` | 0 | ✅ 清理完成 |
| `07-surveys/` | 0 | ✅ 清理完成 |
| `08-comparisons/` | 0 | ✅ 清理完成 |
| `00-dashboard/index.md` | 13 | 📋 指向待创建页面 |
| `00-dashboard/research-map.md` | 13 | 📋 指向待创建页面 |
| `00-dashboard/project-overview.md` | 1 | 🆕 格式错误 |

**剩余 27 条断链详情**：全部位于 `00-dashboard/` 的"待扩展页面"章节，指向 13 个尚未创建的概念/方法页面（见第 5 节）和 1 个格式错误链接。

**新发现**：`00-dashboard/project-overview.md` 第 165 行 `AGENTS.md` 应为 `AGENTS.md`（纯文本，避免断裂链接）。

### 2.2 实验章节补充（✅ 已完成）

**修复时间**: 2026-05-27（深度分析阶段）

| 论文 | 原始状态 | 当前状态 |
|------|----------|----------|
| `2021-CCS-Realtime_Robust_Malicious_Traffic_Detection...md` | 仅 1 个 H2 标题 | 5 个结构化子节（实验设置、检测准确率、鲁棒性评估、延迟与吞吐量、理论分析验证） |
| `2024-INFOCOM-Causality_Correlation...md` | 使用非标准 5.x 标题 | 完整重构：§4 实验设置（3 子节）+ §5 实验结果与分析（6 子节）+ §6 与现有工作对比 |

### 2.3 其他已完成改进

| 改进项 | 时间 | 说明 |
|--------|------|------|
| 开源注册表创建 | 2026-05-29 | `08-comparisons/open-source-registry.md`，21 个已确认开源 + 20+ 高频基线追踪 |
| 论文去重注册表 | 2026-05-29 | `00-dashboard/paper-registry.md`，50 篇论文的 DOI/标题索引 |
| 一键入库管道 | 2026-05-29 | `templates/claudian-prompts/06-ingest-pipeline.md`，17 步全流程自动化 |
| 去重检查提示词 | 2026-05-29 | `templates/claudian-prompts/00-check-duplicate.md`，三轮匹配逻辑 |

---

## 3. 已修复的问题（2026-05-29 批量修复）

### 3.1 旧格式 Frontmatter 统一（✅ 已修复）

**修复时间**: 2026-05-29
**修复方式**: 12 篇论文全部重构为标准 frontmatter 格式

修复内容：
- `title:` → `title_original:` + 新增 `title_cn:`
- `journal:` / `journal/conference:` → `venue:`
- 新增 `mineru_md:` 字段（12 篇）
- 新增 `pdf:` 字段（3 篇），修正 `pdf:` 指向错误（3 篇 `.md` → `.pdf`）
- 新增标准字段：`research_area`, `task`, `method`, `dataset`, `code`, `relevance`
- 移除非标准字段：`keywords`, `date_added`, `date_created`, `related_papers`, `affiliations`, `affiliation`, `topic`, `project`, `arxiv`

**修复的 12 篇论文**：

| # | 文件 | 修复要点 |
|---|------|---------|
| 1 | `2018-CS-An_Efficient_Feature_Generation...md` | journal/conference→venue, 新增 pdf+mineru_md |
| 2 | `2018-Trans_IFS-Robust_Smartphone_App...md` | journal→venue, 新增 pdf+mineru_md |
| 3 | `2019-INFOCOM-FS-Net...md` | 新增 pdf+mineru_md+status+reading_level |
| 4 | `2022-HPCC-MTBD_HTTPS_Tunnel...md` | 移除 topic/keywords, 新增 mineru_md |
| 5 | `2022-ICMLA-Separating_Flows...md` | 移除 keywords/related_papers, 新增 mineru_md |
| 6 | `2022-TBD-Identification...md` | pdf .md→.pdf 修正, 移除 dataset/methods |
| 7 | `2022-WWW-ET-BERT...md` | 移除 keywords/related_papers, 新增 mineru_md |
| 8 | `2023-AAAI-Yet_Another...md` | 移除 project, 新增 mineru_md |
| 9 | `2023-ComputerNetworks-Few-shot...md` | 补全全部缺失字段（极简→完整） |
| 10 | `2023-SIGKDD-A_lightweight...md` | pdf .md→.pdf 修正, 移除 affiliation |
| 11 | `2023-USENIX-Subverting_Website...md` | pdf .md→.pdf 修正, 新增 title+year |
| 12 | `2024-INFOCOM-Causality_Correlation...md` | 移除 affiliations, 新增 mineru_md |

---

## 4. 统计数据（2026-06-09 最新）

| 指标 | 初始值 (05-27) | 当前值 (06-09) |
|------|----------------|----------------|
| 论文笔记总数 | 50 | **92** |
| 有 YAML frontmatter | 50 (100%) | 92 (100%) |
| 使用标准 frontmatter 格式 | 37 (74%) | **92 (100%)** |
| 使用旧格式 frontmatter | 13 (26%) | **0 (0%)** |
| 有 `pdf:` 路径引用 | 41 (82%) | **92 (100%)** |
| 有 `mineru_md:` 路径引用 | 38 (76%) | **92 (100%)** |
| 有 `research_area/task/method` | — | **92 (100%)** |
| 深度分析论文数 (L3/L4) | 0 | **46** |
| 方法/实验章节完整 | 46 (92%) | 92 (100%) |
| 概念页数量 | 10 | 9 |
| 方法页数量 | 7 | 8 |
| 任务页数量 | 3 | 8 |
| 综述页数量 | 1 | 5 |
| 对比表数量 | 2 | **5**（含开源注册表、动机/叙事对比） |
| 开源方法数 | 21 | **30** |
| 方法对比表条目 | 18 | 26+ |
| Claims 页面数量 | — | 2（33 条观点 + 13 组矛盾） |
| 断裂链接总数 | ~300 | **0** |
| 需要新建的概念/方法页数 | ~30-50 | 13（纯文本引用，待创建后恢复 wikilink） |

---

## 5. 建议新增页面

### 5.1 高优先级（被 3+ 篇论文引用，dashboard 中有断链）

**04-concepts/ 目录**（7 个待创建）：

| 建议页面名 | 说明 | 引用次数 |
|-----------|------|---------|
| `vpn-traffic-classification.md` | VPN 流量分类 | 8+ |
| `tor-traffic-classification.md` | Tor 流量分类 | 6+ |
| `intrusion-detection.md` | 入侵检测 | 5+ |
| `malware-detection.md` | 恶意软件检测 | 5+ |
| `dns-security.md` | DNS 安全（DoH、DNS 隧道） | 3+ |
| `network-privacy.md` | 网络隐私 | 4+ |
| `iot-security.md` | IoT 安全 | 3+ |

**05-methods/ 目录**（6 个待创建）：

| 建议页面名 | 说明 | 引用次数 |
|-----------|------|---------|
| `meta-learning.md` | 元学习方法（MAML、Prototypical Networks） | 5+ |
| `attention-mechanism.md` | 注意力机制（Self-Attention、Cross-Attention、Gated Attention） | 5+ |
| `autoencoder.md` | 自编码器（VAE、MAE、SDAE） | 4+ |
| `random-forest.md` | 随机森林及其变体 | 4+ |
| `fingerprinting-methods.md` | 指纹识别方法（TLS、App、Device） | 4+ |
| `data-augmentation.md` | 数据增强方法 | 3+ |

### 5.2 中优先级（被 1-2 篇论文引用，dashboard 中暂未引用）

- `batch-normalization.md`
- `dropout-regularization.md`
- `loss-functions.md`（InfoNCE、Triplet Loss 等）
- `tokenization.md`（BPE、WordPiece）
- `positional-encoding.md`
- `siamese-network.md`
- `prototype-network.md`
- `domain-adaptation.md`
- `few-shot-learning.md`
- `zero-shot-learning.md`
- `semi-supervised-learning.md`
- `masked-language-model.md`
- `variational-autoencoder.md`
- `masked-autoencoder.md`
- `traffic-obfuscation.md`
- `pluggable-transport.md`

---

## 6. 建议修复路线图

### ~~第一阶段：修复 Frontmatter + 路径引用~~ ✅ 已完成

1. ~~统一 12 篇旧格式 frontmatter~~ → 已修复（2026-05-29）
2. ~~补充缺失 `pdf:` / `mineru_md:` 字段~~ → 已修复（2026-05-29）
3. ~~修复 frontmatter 路径不一致（`../` 前缀）~~ → 已修复（2026-06-09）
4. ~~补充 research_area/task/method 字段~~ → 已修复（2026-06-09，34 篇）

### 第二阶段：创建高频引用概念/方法页面（按需）

1. 创建 7 个高优先级概念页（vpn-traffic-classification, tor-traffic-classification 等）
2. 创建 6 个高优先级方法页（meta-learning, attention-mechanism 等）
3. 创建后恢复 dashboard 中对应的 wikilink 引用

### 第三阶段：持续改进

1. 创建中优先级概念/方法页面
2. 补充 25 篇论文缺失的 DOI（当前为 `unknown`）

## 2026-11-20　TACO 与 HPETC 原文复核

- 按本地原版 PDF 首页、出版记录及实验表复核两篇笔记。当前引用指向 [[03-paper-notes/2026-TDSC-Learning_Flow_Semantics_for_Encrypted_Traffic_Analysis_A_Contrastive_Pre-training_Approach|TACO]]（§6 Tables 2–6）与 [[03-paper-notes/2025-TON-High_Precision_and_Efficient_Anonymous_Traffic_Classification_in_the_Real-World|HPETC]]（§IV-D、§V Tables II–IV、Fig. 9）。
- 原整理稿原样保留在两篇笔记末尾。liu2026learning、xie2025high 沿用为历史引用键。
- 代表论文、方法与任务对照及阅读队列采用原文题名、条件与指标。旧条目如下。

### 04-concepts/anonymous-traffic-identification.md

```markdown
| **图像化 + 预处理优化** | 将流量转化为图像表示，通过流合并和像素化压缩优化预处理效率 | 预处理速度快、满足实时部署 | 信息损失、压缩系数敏感 | SequOcc |
- 图像化方法 - 将流量转化为图像进行分析（FlowPic、SequOcc）
| **High-Precision and Efficient Anonymous Traffic Classification in the Real-World Network Environment** (Xie et al., TON) | 2025 | 提出 SequOcc 预处理方法（Stream Merging + Pixelization），将预处理时间降低 54.55%，首次提出真实骨干网匿名流量数据集 | 分类精度略有下降；骨干网数据集不可公开 |
2. **预处理效率在真实部署中至关重要**：现有研究主要关注分类精度，忽略了预处理效率。SequOcc 证明了预处理可以成为主要瓶颈，需要专门优化。
4. **图像化方法在匿名流量分类中有效**：将流量转化为图像进行 CNN 分类已被证明有效（FlowPic、SequOcc），但需要平衡图像分辨率和计算效率。
**效率优先方**：SequOcc 证明在真实骨干网部署中，预处理时间可能成为主要瓶颈，需要在精度和效率之间找到平衡点。
2. **预处理优化方向**：数据冗余利用（流合并）和空间压缩（像素化）是有效的预处理优化策略，可应用于其他流量分析任务。
```

### 05-methods/contrastive-learning.md

```markdown
| Learning Flow Semantics via Contrastive Pre-training for Encrypted Traffic Analysis | 2026 | 包级+流级对比预训练 + 流量特定数据增强 + 后训练策略 | 提出双层对比预训练框架：包级预训练学习字节级语义，流级预训练学习包间关系语义；设计四种流量特定数据增强策略（包重排、包丢失、包分割、时间抖动）；提出后训练策略（FT-S）解决预训练-微调兼容性问题；在加密流量分类、恶意流量检测、流量相似度和异常检测四个任务上全面超越 ET-BERT 等方法，性能提升 >50% — `[[2026-TDSC-Learning_Flow_Semantics_for_Encrypted_Traffic_Analysis_A_Contrastive_Pre-training_Approach]]` |
```

### 06-tasks/traffic-classification.md

```markdown
| High-Precision and Efficient Anonymous Traffic Classification (SequOcc) | 2025 | SequOcc 预处理（Stream Merging + Pixelization）+ CNN | ISCX-Tor, Cross-Platform, 骨干网数据集 | 首个真实骨干网匿名流量数据集；预处理速度提升 54.55%；数据量减少 27.4%；满足实时部署需求 — `[[2025-TON-High_Precision_and_Efficient_Anonymous_Traffic_Classification_in_the_Real-World]]` |
| Learning Flow Semantics via Contrastive Pre-training for Encrypted Traffic Analysis | 2026 | 包级+流级对比预训练 + 流量特定数据增强 + 后训练策略 | USTC-TFC2016, ISCX-VPN, ISCX-Tor, CSTNET-TLS1.3, CIC-IDS2017 | 双层对比预训练全面超越 ET-BERT 等方法，性能提升 >50%；四种流量特定数据增强策略有效；后训练策略解决预训练-微调兼容性 — `[[2026-TDSC-Learning_Flow_Semantics_for_Encrypted_Traffic_Analysis_A_Contrastive_Pre-training_Approach]]` |
```

### 08-comparisons/method-comparison-table.md

```markdown
| SequOcc | 2025 | 匿名流量分类 | 图像化 CNN + 预处理优化 | 提出 SequOcc 预处理方法（Stream Merging + Pixelization），通过流合并和像素化压缩将匿名流量转化为图像表示，实现预处理速度提升 54.55%，首次提出真实骨干网匿名流量数据集 | 首个真实骨干网匿名流量数据集；预处理效率显著提升（54.55%）；数据量减少 27.4%；满足实时部署需求 | 分类精度略有下降（F1 降低 0.7-1.24%）；压缩系数敏感；骨干网数据集不可公开；CNN 架构未创新 | 骨干网实时匿名流量检测；资源受限环境下的匿名流量分类 | ❌ | 暂未找到 |
| Contrastive Pre-training (Flow Semantics) | 2026 | 加密流量分类 | 包级+流级对比预训练 | 提出双层对比预训练框架：包级预训练学习字节级语义，流级预训练学习包间关系语义；设计四种流量特定数据增强策略（包重排、包丢失、包分割、时间抖动）；提出后训练策略（FT-S）解决预训练-微调兼容性 | 全面超越 ET-BERT 等方法（性能提升 >50%）；双层语义学习更完整；流量特定数据增强有效；后训练策略解决兼容性问题 | 预训练数据量较小（~100MB）；流长截断可能丢失信息；代码未开源 | 加密流量分类、恶意流量检测、流量相似度分析 | ❌ | 暂未找到 |
```

### 00-dashboard/reading-queue.md

```markdown
| processed | High-Precision and Efficient Anonymous Traffic Classification in the Real-World Network Environment | 2025 | 匿名流量 | [[2025-TON-High_Precision_and_Efficient_Anonymous_Traffic_Classification_in_the_Real-World]] | [[2025-TON-High_Precision_and_Efficient_Anonymous_Traffic_Classification_in_the_Real-World]] |
| processed | Learning Flow Semantics via Contrastive Pre-training for Encrypted Traffic Analysis | 2026 | 流量分类 | [[2026-TDSC-Learning_Flow_Semantics_for_Encrypted_Traffic_Analysis_A_Contrastive_Pre-training_Approach]] | [[2026-TDSC-Learning_Flow_Semantics_for_Encrypted_Traffic_Analysis_A_Contrastive_Pre-training_Approach]] |
```

## 2026-11-20　题录与去重索引复核

- 115 篇含历史版本的题录进入本轮核对，实际更新 108 篇笔记和 110 条注册记录。核验依据是原版首页、出版社、会议或 arXiv 的题录。
- 作者列表由空补全 30 篇。补写可核 DOI 100 篇。现有引用键沿用，17 个仅存在于 BibTeX 的旧条目保留原文。
- 会议页未列 DOI 的 3 篇 USENIX 论文使用官方页面。TrafficSliver 旧键保留并指向同篇论文。GAN 混淆 Tor 识别论文采用 Computers & Security 卷期题录，保留 SSRN 预印本 DOI。
- 城轨流量论文的本地原文为 arXiv:2609.32168。《The Inevitability of Side-Channel Leakage in Encrypted Traffic》的本地原文为 arXiv:2602.14055。《Secrets in Radio Waves》的本地原文为 arXiv:2609.23319。题录另记对应正式出版版本。

<details>
<summary>旧字段与注册行</summary>

```json
{
  "bib": [
    {
      "key": "unknown2026despite",
      "old_json_fields": {
        "title": "DESPITE INSTRUCTIONS: FRONTIER AGENTS IMPROVISE COVERT CHANNELS AT TEST TIME",
        "authors": [],
        "doi": "",
        "url": ""
      },
      "old_bib_lines": [
        "  title = {DESPITE INSTRUCTIONS: FRONTIER AGENTS IMPROVISE COVERT CHANNELS AT TEST TIME},"
      ],
      "source": "https://doi.org/10.48550/arXiv.2609.32701"
    },
    {
      "key": "unknown2026exact",
      "old_json_fields": {
        "authors": [],
        "doi": "",
        "url": ""
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.48550/arXiv.2609.24675"
    },
    {
      "key": "unknown2026feedback",
      "old_json_fields": {
        "authors": [],
        "doi": "",
        "url": ""
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.48550/arXiv.2609.24994"
    },
    {
      "key": "unknown2026multiplexing",
      "old_json_fields": {
        "authors": [],
        "doi": "",
        "url": ""
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.48550/arXiv.2609.21353"
    },
    {
      "key": "unknown2026unknown",
      "old_json_fields": {
        "authors": [],
        "doi": "",
        "url": ""
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.48550/arXiv.2609.31141"
    },
    {
      "key": "unknown2026your",
      "old_json_fields": {
        "authors": [],
        "doi": "",
        "url": ""
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.48550/arXiv.2609.27996"
    },
    {
      "key": "akpaku2026tipso",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.14722/ndss.2026.243241"
    },
    {
      "key": "bielefeld2026future",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1007/978-3-032-18268-5_10"
    },
    {
      "key": "cai2026lightweight",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1002/cpe.70679"
    },
    {
      "key": "he2026trafficmoe",
      "old_json_fields": {
        "entry_type": "article",
        "authors": [
          "Chen, Huimin",
          "Gao, Dehong",
          "Zhang, Wenxiao",
          "Yang, Libin",
          "Zhou, Zibo"
        ],
        "doi": "10.1007/s44443-026-01202-7",
        "url": "https://arxiv.org/abs/2605",
        "booktitle": null,
        "journal": "Journal of King Saud University Computer and Information Sciences",
        "pages": null,
        "volume": "38",
        "number": "7",
        "publisher": "Springer Science and Business Media LLC",
        "abstract": "Abstract\n                  Network traffic analysis is fundamentally challenged by the need to accurately identify malicious behaviors and application types from massive, structurally heterogeneous packet data. Existing deep learning and Large Language Model (LLM)-based methods typically rely on shared parameter spaces optimized for isolated, single-task scenarios. Consequently, when deployed in dynamic multi-task environments, these approaches may be affected by cross-task gradient interference and negative transfer. To address these limitations, we propose TrafficMoE, an LLM-based Mixture-of-Experts (MoE) framework for supervised multi-task network traffic classification. Specifically, TrafficMoE formulates heterogeneous traffic tasks under a unified instruction-to-label generation paradigm by converting packet metadata into text. To mitigate task interference, the framework integrates a shared traffic expert to capture common semantics, multiple task-specialized experts to separate domain knowledge, and a lightweight context-aware router for automatic, sample-wise dispatching under mixed-task inputs. Furthermore, to support continual task evolution, we design a modular sequential expansion strategy that accommodates new tasks by adding a single expert and updating the router. Extensive evaluations across ten public benchmark datasets show that TrafficMoE achieves an average F1-score of 0.9823, while supporting modular task expansion with reduced adaptation overhead.",
        "metadata_source": "note"
      },
      "old_bib_lines": [
        "  url = {https://arxiv.org/abs/2605},",
        "  abstract = {Encrypted traffic classification is a critical task for network security. While deep learning has advanced this field, the occlusion of payload semantics by encryption severely challenges standard modeling approaches. Most existing frameworks rely on static and homogeneous pipelines that apply uniform parameter sharing and static fusion strategies across all inputs. This “one-size-fits-all” static design is inherently flawed: by forcing structured headers and randomized payloads into a unified processing pipeline, it inevitably entangles the raw protocol signals with stochastic encryption noise, thereby degrading the fine-grained discriminative features. In this paper, we propose TrafficMoE, a framework that breaks through the bottleneck of static modeling by establishing a Disentangle–Filter–Aggregate (DFA) paradigm. Specifically, to resolve the structural betweencomponents conflict, the architecture disentangles headers and payloads using dual-branch sparse Mixture-of-Experts (MoE), enabling modality-specific modeling. To mitigate the impact of stochastic noise, an uncertainty-aware filtering mechanism is introduced to quantify reliability and selectively suppress highvariance representations. Finally, to overcome the limitations of static fusion, a routing-guided strategy aggregates cross-modality features dynamically, that adaptively weighs contributions based on traffic context. With this DFA paradigm, TrafficMoE maximizes representational efficiency by focusing solely on the most discriminative traffic features. Extensive experiments on six datasets demonstrate TrafficMoE consistently outperforms stateof-the-art methods, validating the necessity of heterogeneityaware modeling in encrypted traffic analysis. The source code is publicly available at https://github.com/Posuly/TrafficMoE main. Index Terms—Encrypted traffic classification, TrafficMoE.},"
      ],
      "source": "https://arxiv.org/abs/2603.29520"
    },
    {
      "key": "chen2026dentc",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1016/j.comnet.2026.112078"
    },
    {
      "key": "unknown2026ultimate",
      "old_json_fields": {
        "authors": [
          "Chen, Zihan",
          "Cheng, Guang",
          "Niu, Dandan",
          "Zhao, Yuyu",
          "Zhou, Yuyang",
          "Jiang, Shanqing"
        ]
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/tdsc.2025.3615592"
    },
    {
      "key": "cherubin2026conformal",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1007/978-3-032-15120-9_14"
    },
    {
      "key": "cho2026prototypical",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1016/j.comnet.2026.112062"
    },
    {
      "key": "ding2026making",
      "old_json_fields": {
        "title": "Making the Best of Both Worlds: Universal Perturbations for Live Black-Box Evasion Against NIDS in Encrypted Trafic"
      },
      "old_bib_lines": [
        "  title = {Making the Best of Both Worlds: Universal Perturbations for Live Black-Box Evasion Against NIDS in Encrypted Trafic},"
      ],
      "source": "https://doi.org/10.1109/TON.2026.3710207"
    },
    {
      "key": "ding2026time",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/tsc.2026.3664705"
    },
    {
      "key": "unknown2026tunneleye",
      "old_json_fields": {
        "authors": [
          "Du, Jiajia",
          "Liu, Songtao",
          "Zhi, Cheng",
          "Zhao, Junfan",
          "Wu, Hua",
          "Cheng, Guang"
        ]
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/tnsm.2026.3682686"
    },
    {
      "key": "dutta2026kan",
      "old_json_fields": {
        "title": "KAN-VIS: Eficient and Lightweight Visual Technique for Network Trafic Classification Using Kolmogorov–Arnold Network"
      },
      "old_bib_lines": [
        "  title = {KAN-VIS: Eficient and Lightweight Visual Technique for Network Trafic Classification Using Kolmogorov–Arnold Network},"
      ],
      "source": "https://doi.org/10.1109/TON.2026.3722338"
    },
    {
      "key": "liu2026inevitability",
      "old_json_fields": {
        "entry_type": "inproceedings",
        "url": "https://doi.org/10.12263/DZXB.20251034",
        "booktitle": null,
        "journal": null,
        "pages": null,
        "volume": null,
        "number": null,
        "metadata_source": "note"
      },
      "old_bib_lines": [
        "@inproceedings{liu2026inevitability,",
        "  url = {https://doi.org/10.12263/DZXB.20251034},"
      ],
      "source": "https://www.ejournal.org.cn/en/article/doi/10.12263/DZXB.20251034"
    },
    {
      "key": "unknown2026improving",
      "old_json_fields": {
        "entry_type": "inproceedings",
        "title": "IMPROVING THE RELIABILITY OF ANOMALY DETECTION FOR ENCRYPTED OPC UA TRAFFIC OVER PRIVATE 5G",
        "authors": [
          "Ha, Song Son",
          "Foerster, Florian",
          "Beuster, Henry",
          "Kittel, Tim",
          "Merli, Dominik",
          "Scholl, Gerd"
        ],
        "doi": "10.1109/etfa68377.2026.11725251",
        "url": "https://doi.org/10.1109/etfa68377.2026.11725251",
        "booktitle": "2026 IEEE 31st International Conference on Emerging Technologies and Factory Automation (ETFA)",
        "journal": null,
        "pages": "1-4",
        "volume": null,
        "number": null,
        "publisher": "IEEE",
        "metadata_source": "note"
      },
      "old_bib_lines": [
        "  title = {IMPROVING THE RELIABILITY OF ANOMALY DETECTION FOR ENCRYPTED OPC UA TRAFFIC OVER PRIVATE 5G},"
      ],
      "source": "https://arxiv.org/abs/2609.29745"
    },
    {
      "key": "hilal2026unpacking",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1007/978-3-032-18268-5_5"
    },
    {
      "key": "jansen2026measurement",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1007/978-3-032-18268-5_13"
    },
    {
      "key": "unknown2026rofire",
      "old_json_fields": {
        "title": "RoFiRe: Robust Website Fingerprinting on Real-World Tor Trafic via Improved Augmentation and Normalization",
        "authors": [
          "Jeon, Haeseung",
          "Kim, Sujin",
          "Mathews, Nate",
          "Kang, Hosung",
          "Oh, Se Eun"
        ]
      },
      "old_bib_lines": [
        "  title = {RoFiRe: Robust Website Fingerprinting on Real-World Tor Trafic via Improved Augmentation and Normalization},"
      ],
      "source": "https://doi.org/10.1145/3774904.3792592"
    },
    {
      "key": "jonath2026gmm",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1016/j.comnet.2025.111823"
    },
    {
      "key": "liu2026towards",
      "old_json_fields": {
        "authors": [
          "Ju, Xinlei",
          "Li, Zhen",
          "Li, Yang",
          "Yin, Lihua",
          "Guan, Zhong",
          "Gou, Gaopeng",
          "Zhou, Mi",
          "Shi, Junzheng",
          "Xiong, Gang"
        ],
        "doi": "10.1109/iwqos70441.2026.11661113",
        "url": "https://doi.org/10.1109/iwqos70441.2026.11661113",
        "booktitle": "2026 IEEE/ACM International Symposium on Quality of Service (IWQoS)",
        "journal": null,
        "pages": "1-10",
        "volume": null,
        "number": null,
        "publisher": "IEEE",
        "metadata_source": "note"
      },
      "old_bib_lines": [],
      "source": "https://www.usenix.org/conference/usenixsecurity26/presentation/liu-lin"
    },
    {
      "key": "kamali2026huma",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.14722/ndss.2026.240328"
    },
    {
      "key": "ravi2026remise",
      "old_json_fields": {
        "entry_type": "article",
        "authors": [
          "Kareem, Malath Sabri"
        ],
        "doi": "10.61401/rmaps.v3i2.510",
        "booktitle": null,
        "journal": "Review of Multidisciplinary Academic and Practice Studies",
        "pages": "67-80",
        "volume": "3",
        "number": "2",
        "publisher": "Sekolah Tinggi Ilmu Ekonomi Krakatau",
        "abstract": "Purpose: This study examines the security aspects of anonymous communication systems, which are critical for protecting digital privacy and maintaining freedom of expression online. It focuses on widely used systems, such as the Tor network and Holloway's Freedom protocol, analyzing vulnerabilities, systemic weaknesses, and the advanced attack techniques employed by adversaries to compromise user anonymity, including traffic analysis, de-anonymization, and timing correlation attacks.\r\nResearch Methodology: A literature-based analytical approach was employed, reviewing specialized scientific articles and experimental studies published between 2020 and 2026. Emphasis was placed on research accepted at prominent conferences in network security and privacy protection. The study synthesizes evidence on security threats, attack methodologies, and systemic vulnerabilities affecting anonymous communication systems.\r\nResults: The analysis reveals persistent fundamental weaknesses in current anonymous communication systems, which continue to compromise security. Additionally, the application of big data and artificial intelligence has facilitated increasingly sophisticated attack strategies capable of penetrating multiple layers of anonymity. The study identifies both the limitations of existing systems and the emerging risks that users face.\r\nConclusions: Protecting anonymity in digital communication requires both system-level improvements and strategic countermeasures against evolving attack techniques. Recommendations include technical upgrades, protocol redesigns, and adoption of AI-resistant security measures to ensure the resilience of anonymous communication systems in the future.\r\nLimitations: The study relies on literature review and secondary data rather than primary experimental validation. As such, conclusions may not fully generalize to all types of anonymous systems or evolving attack scenarios.\r\nContribution: This study provides a comprehensive analysis of current threats and vulnerabilities in anonymous communication systems, offering practical and research-oriented recommendations to strengthen digital privacy protection and to future-proof these systems against increasingly sophisticated attacks.",
        "metadata_source": "note"
      },
      "old_bib_lines": [],
      "source": "https://www.usenix.org/conference/usenixsecurity26/presentation/ravi-rohan"
    },
    {
      "key": "koumar2026comparative",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/tnsm.2025.3636557"
    },
    {
      "key": "liu2026srvit",
      "old_json_fields": {
        "title": "SRViT: A Robust Online Encrypted Trafic Classification Based on Vision Transformer"
      },
      "old_bib_lines": [
        "  title = {SRViT: A Robust Online Encrypted Trafic Classification Based on Vision Transformer},"
      ],
      "source": "https://doi.org/10.1109/TON.2026.3699540"
    },
    {
      "key": "liu2026two",
      "old_json_fields": {
        "title": "Two Heads Are Better Than One: Models-to-Model Learning for Encrypted Trafic Analysis"
      },
      "old_bib_lines": [
        "  title = {Two Heads Are Better Than One: Models-to-Model Learning for Encrypted Trafic Analysis},"
      ],
      "source": "https://doi.org/10.1109/TIFS.2026.3723131"
    },
    {
      "key": "liu2026two_2",
      "old_json_fields": {
        "title": "Two Heads Are Not Better Than One: Continual Learning From Multiple Models for Encrypted Trafic Analysis"
      },
      "old_bib_lines": [
        "  title = {Two Heads Are Not Better Than One: Continual Learning From Multiple Models for Encrypted Trafic Analysis},"
      ],
      "source": "https://doi.org/10.1109/TIFS.2026.3712230"
    },
    {
      "key": "liu2026netttt",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/jiot.2026.3652996"
    },
    {
      "key": "unknown2026priority",
      "old_json_fields": {
        "title": "A Priority-Aware Dual-Channel Feature Fusion Method for Urban Rail Service Trafic Classification",
        "authors": [
          "Liu, Xinpeng",
          "Zhao, Junhui",
          "Wu, Zhengyuan",
          "Li, Huaicheng"
        ]
      },
      "old_bib_lines": [
        "  title = {A Priority-Aware Dual-Channel Feature Fusion Method for Urban Rail Service Trafic Classification},"
      ],
      "source": "https://doi.org/10.1007/s10489-026-07560-z"
    },
    {
      "key": "lu2026time",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/tifs.2026.3675458"
    },
    {
      "key": "unknown2026gan",
      "old_json_fields": {
        "authors": [
          "Lu, Tianbo",
          "Zhao, Pengfei",
          "Cai, Yingjie",
          "Abdulla, Subatjan",
          "Chen, Hanrui"
        ],
        "year": 2026,
        "doi": "10.2139/ssrn.6709728",
        "url": "https://doi.org/10.2139/ssrn.6709728",
        "booktitle": null,
        "journal": null,
        "pages": null,
        "volume": null,
        "publisher": "Elsevier BV",
        "metadata_source": "note"
      },
      "old_bib_lines": [
        "  year = {2026},"
      ],
      "source": "https://www.sciencedirect.com/science/article/pii/S0167404826003433"
    },
    {
      "key": "unknown2026sagnn",
      "old_json_fields": {
        "authors": [
          "Luo, Junjie",
          "Liu, Min",
          "Sun, Sheng",
          "Chen, Yali",
          "Tang, Qixun",
          "Wang, Yuwei"
        ]
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.1016/j.comnet.2026.112763"
    },
    {
      "key": "nie2026stinger",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/tifs.2025.3646493"
    },
    {
      "key": "pan2026prismwf",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/tdsc.2026.3746307"
    },
    {
      "key": "ponraj2026building",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1145/3770854.3783939"
    },
    {
      "key": "unknown2026secrets",
      "old_json_fields": {
        "authors": [
          "Shen, Guanxiong",
          "Jia, Hailang",
          "Zhang, Junqing",
          "Peng, Linning",
          "Chen, Liquan",
          "Hu, Aiqun",
          "Luo, Jun"
        ]
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/tmc.2026.3736788"
    },
    {
      "key": "gupta2026revelio",
      "old_json_fields": {
        "authors": [
          "Shin, Kangsik",
          "Choi, GyuHyeon",
          "Lee, KyeongSeok",
          "Lee, Jeongho",
          "Cho, Ho-Mook"
        ],
        "doi": "10.1109/icoin68469.2026.11480550",
        "booktitle": "2026 40th International Conference on Information Networking (ICOIN)",
        "journal": null,
        "pages": "479-483",
        "volume": null,
        "number": null,
        "publisher": "IEEE",
        "metadata_source": "note"
      },
      "old_bib_lines": [],
      "source": "https://www.usenix.org/conference/usenixsecurity26/presentation/gupta"
    },
    {
      "key": "unknown2026replicability",
      "old_json_fields": {
        "title": "Replicability: Challenging the Myth of Randomness Paterns in Encrypted Trafic",
        "authors": [
          "Shpakov, Timofey",
          "Burkhart, Martin",
          "Vanbever, Laurent"
        ]
      },
      "old_bib_lines": [
        "  title = {Replicability: Challenging the Myth of Randomness Paterns in Encrypted Trafic},"
      ],
      "source": "https://doi.org/10.1145/3777912.3839783"
    },
    {
      "key": "unknown2026semfuzz",
      "old_json_fields": {
        "authors": [
          "Sun, Yanbang",
          "Luo, Quan",
          "Wang, Yuelin",
          "Chen, Qian",
          "Liu, Benjin",
          "Chen, Ruiqi",
          "Huang, Qing",
          "Li, Xiaohong",
          "Wang, Junjie"
        ]
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.1145/3774904.3792541"
    },
    {
      "key": "unknown2026uncovering",
      "old_json_fields": {
        "authors": [
          "Tang, Cheng",
          "Barradas, Diogo",
          "Hengartner, Urs",
          "Hu, Yue"
        ]
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.1016/j.cose.2026.105018"
    },
    {
      "key": "towhid2026encrypted",
      "old_json_fields": {
        "title": "Encrypted Network Trafic Classification Using Generative and Contrastive Self-Supervised Learning"
      },
      "old_bib_lines": [
        "  title = {Encrypted Network Trafic Classification Using Generative and Contrastive Self-Supervised Learning},"
      ],
      "source": "https://doi.org/10.1109/TON.2026.3737411"
    },
    {
      "key": "unknown2026quantifying",
      "old_json_fields": {
        "title": "Quantifying the Privacy Implications of High-Fidelity Synthetic Network Trafic",
        "authors": [
          "Tran, Van",
          "Liu, Shinan",
          "Li, Tian",
          "Feamster, Nick"
        ]
      },
      "old_bib_lines": [
        "  title = {Quantifying the Privacy Implications of High-Fidelity Synthetic Network Trafic},"
      ],
      "source": "https://doi.org/10.1145/3777912.3839833"
    },
    {
      "key": "wang2026bias",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/iwqos70441.2026.11661209"
    },
    {
      "key": "unknown2026robust_3",
      "old_json_fields": {
        "entry_type": "article",
        "authors": [
          "Wang, Jiaqi",
          "Lv, Lu",
          "Wang, Yilin",
          "He, Bingtao",
          "Yang, Long"
        ],
        "doi": "10.1109/lcomm.2026.3686041",
        "url": "https://doi.org/10.1109/lcomm.2026.3686041",
        "booktitle": null,
        "journal": "IEEE Communications Letters",
        "pages": "1761-1765",
        "volume": "30",
        "number": null,
        "publisher": "Institute of Electrical and Electronics Engineers (IEEE)",
        "abstract": "Stacked intelligent metasurfaces (SIMs) have emerged as a promising wave-domain processing technology for sixth-generation integrated sensing and communication networks, reducing reliance on complex radio-frequency hardware. Nevertheless, imperfect channel state information (CSI) can compromise sensing performance and communication reliability. Moreover, ensuring covert transmission introduces a further challenge, as the system must sense potential targets while concealing communication activity from unauthorized wardens. These challenges motivate the development of robust SIM-assisted integrated sensing and covert communication (ISACC) systems. In this paper, we investigate the robust transceiver design of a multi-user, multi-target ISACC system under imperfect CSI. We jointly optimize the transmit and receive beamformers, sensing covariance matrix, and SIM phase shifts to maximize the worst-case minimum sensing signal-to-interference-plus-noise ratio. The formulation enforces constraints on bounded channel uncertainties, user qualityof-service requirements, transmit-power budget, SIM phase shifts, and target detection probabilities. Since the formulated problem is highly non-convex, we develop an alternating optimization framework based on the S-procedure, successive convex approximation, and semidefinite relaxation. Furthermore, to reduce computational complexity, we derive exact lowerdimensional representations of the robust sensing linear matrix inequalities (LMIs) involved in transmit/receive-beamformer designs. We further develop a low-complexity phase-update method that avoids the large sensing LMIs. Numerical results demonstrate that the proposed design outperforms random phase shift and fully digital-beamforming benchmarks, while the low-complexity scheme achieves comparable performance to the LMI-based scheme at substantially lower computational cost. Index Terms—Stacked intelligent metasurfaces, integrated sensing and communication, covert communication, imperfect channel state information, robust design.",
        "metadata_source": "note"
      },
      "old_bib_lines": [
        "  abstract = {Stacked intelligent metasurfaces (SIMs) have emerged as a promising wave-domain processing technology for sixth-generation integrated sensing and communication networks, reducing reliance on complex radio-frequency hardware. Nevertheless, imperfect channel state information (CSI) can compromise sensing performance and communication reliability. Moreover, ensuring covert transmission introduces a further challenge, as the system must sense potential targets while concealing communication activity from unauthorized wardens. These challenges motivate the development of robust SIM-assisted integrated sensing and covert communication (ISACC) systems. In this paper, we investigate the robust transceiver design of a multi-user, multi-target ISACC system under imperfect CSI. We jointly optimize the transmit and receive beamformers, sensing covariance matrix, and SIM phase shifts to maximize the worst-case minimum sensing signal-to-interference-plus-noise ratio. The formulation enforces constraints on bounded channel uncertainties, user qualityof-service requirements, transmit-power budget, SIM phase shifts, and target detection probabilities. Since the formulated problem is highly non-convex, we develop an alternating optimization framework based on the S-procedure, successive convex approximation, and semidefinite relaxation. Furthermore, to reduce computational complexity, we derive exact lowerdimensional representations of the robust sensing linear matrix inequalities (LMIs) involved in transmit/receive-beamformer designs. We further develop a low-complexity phase-update method that avoids the large sensing LMIs. Numerical results demonstrate that the proposed design outperforms random phase shift and fully digital-beamforming benchmarks, while the low-complexity scheme achieves comparable performance to the LMI-based scheme at substantially lower computational cost. Index Terms—Stacked intelligent metasurfaces, integrated sensing and communication, covert communication, imperfect channel state information, robust design.},"
      ],
      "source": "https://arxiv.org/abs/2609.33266"
    },
    {
      "key": "wang2026cease",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.14722/ndss.2026.240786"
    },
    {
      "key": "wang2026data",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/tifs.2026.3694650"
    },
    {
      "key": "wang2026netmamba",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/ton.2026.3734044"
    },
    {
      "key": "unknown2026mind",
      "old_json_fields": {
        "authors": [
          "Wickramasinghe, Nimesha",
          "Li, Frank",
          "Jha, Sanjay",
          "Shaghaghi, Arash"
        ]
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.1145/3777912.3839797"
    },
    {
      "key": "unknown2026tracking",
      "old_json_fields": {
        "authors": [
          "Wu, Wenhao",
          "Wang, Zhaohua",
          "Li, Zihan",
          "Li, Qinxin",
          "Xia, Yiming",
          "Gao, Chuan",
          "Zhang, Guangxing",
          "Li, Zhenyu"
        ]
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.1145/3774904.3792405"
    },
    {
      "key": "xiao2026traffic",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1016/j.comnet.2026.112072"
    },
    {
      "key": "xu2026bytedance",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1016/j.comnet.2025.111843"
    },
    {
      "key": "unknown2026packetpatch",
      "old_json_fields": {
        "authors": [
          "Xu, Yuwei",
          "Xu, Yuanyuan",
          "Bai, Yunpeng",
          "Chen, Jiahui",
          "Song, Kehui",
          "Cao, Jie",
          "Xiang, Qiao",
          "Cheng, Guang"
        ]
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.1016/j.cose.2026.104987"
    },
    {
      "key": "liu2026learning",
      "old_json_fields": {
        "title": "Learning Flow Semantics via Contrastive Pre-training for Encrypted Traffic Analysis",
        "authors": [
          "Xueliang Liu",
          "Shunpu Tang",
          "Jiaqi Xue",
          "Yifan Xu",
          "Jiajun Li",
          "Chuanpu Chen",
          "Ke Xu"
        ],
        "doi": "10.1109/TDSC.2025.3596462",
        "url": "https://ieeexplore.ieee.org/document/11121609",
        "booktitle": null,
        "journal": null,
        "pages": null,
        "volume": null,
        "number": null,
        "publisher": null,
        "metadata_source": "note"
      },
      "old_bib_lines": [
        "  title = {Learning Flow Semantics via Contrastive Pre-training for Encrypted Traffic Analysis},",
        "  author = {Xueliang Liu and Shunpu Tang and Jiaqi Xue and Yifan Xu and Jiajun Li and Chuanpu Chen and Ke Xu},",
        "  doi = {10.1109/TDSC.2025.3596462},",
        "  url = {https://ieeexplore.ieee.org/document/11121609},"
      ],
      "source": "https://doi.org/10.1109/TDSC.2026.3677663"
    },
    {
      "key": "unknown2026robust",
      "old_json_fields": {
        "authors": [
          "Yuan, Yali",
          "Ma, Ruolin",
          "Ge, Jian",
          "Cheng, Guang"
        ]
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/tnsm.2025.3645079"
    },
    {
      "key": "yue2026trifusion",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/icassp55912.2026.11460777"
    },
    {
      "key": "zhang2026multimodal",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/tmm.2026.3730256"
    },
    {
      "key": "zhang2026fgfr",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1007/s10922-025-10011-8"
    },
    {
      "key": "zhao2026when",
      "old_json_fields": {
        "title": "When Pre-Training Meets Contrast Learning: Few-Shot Encrypted Trafic Classification With Novelty Detection"
      },
      "old_bib_lines": [
        "  title = {When Pre-Training Meets Contrast Learning: Few-Shot Encrypted Trafic Classification With Novelty Detection},"
      ],
      "source": "https://doi.org/10.1109/TON.2026.3674624"
    },
    {
      "key": "unknown2026robust_2",
      "old_json_fields": {
        "authors": [
          "Zhao, Xiyuan",
          "Deng, Xinhao",
          "Cui, Tianyu",
          "Zhang, Yixiang",
          "Xu, Ke",
          "Li, Qi"
        ]
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.1145/3774904.3792288"
    },
    {
      "key": "zheng2026plug",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1016/j.comnet.2026.112122"
    },
    {
      "key": "unknown2026towards",
      "old_json_fields": {
        "authors": [
          "Zhu, Yufei",
          "Tian, Le",
          "Hu, Yuxiang",
          "Pei, Xinglong",
          "Zhan, Qi",
          "Huang, Qilong"
        ]
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.1016/j.comnet.2026.112724"
    },
    {
      "key": "zou2026hiding",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1016/j.cose.2026.104981"
    },
    {
      "key": "chen2025miett",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1609/aaai.v39i15.33748"
    },
    {
      "key": "daum2025non",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/icnp65844.2025.11192379"
    },
    {
      "key": "deng2025countmamba",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/sp61157.2025.00154"
    },
    {
      "key": "guo2025semi",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/icaace65325.2025.11020246"
    },
    {
      "key": "li2025mota",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/iwqos65803.2025.11143417"
    },
    {
      "key": "li2025multi",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1016/j.jpdc.2025.105083"
    },
    {
      "key": "unknown2025facing",
      "old_json_fields": {
        "title": "Facing Anomalies Head-On: Network Trafic Anomaly Detection via Uncertainty-Inspired Inter-Sample Diferences",
        "authors": [
          "Lian, Xinglin",
          "Cao, Chengtai",
          "Liu, Yan",
          "Xu, Xovee",
          "Zheng, Yu",
          "Zhou, Fan"
        ]
      },
      "old_bib_lines": [
        "  title = {Facing Anomalies Head-On: Network Trafic Anomaly Detection via Uncertainty-Inspired Inter-Sample Diferences},"
      ],
      "source": "https://doi.org/10.1145/3696410.3714621"
    },
    {
      "key": "liang2025pathfinder",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/acsac67867.2025.00063"
    },
    {
      "key": "lin2025trage",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/iwqos65803.2025.11143462"
    },
    {
      "key": "xie2025high",
      "old_json_fields": {
        "title": "High-Precision and Efficient Anonymous Traffic Classification in the Real-World Network Environment",
        "authors": [
          "Longtian Xie",
          "Shuiqiao Yang",
          "Wei Ye",
          "Guangcan Li",
          "Yonglin Xie",
          "Jian Zhang",
          "Qixu Liu"
        ],
        "doi": "10.1109/TNET.2025.3582301",
        "url": "https://ieeexplore.ieee.org/document/11084593",
        "booktitle": null,
        "journal": null,
        "pages": null,
        "volume": null,
        "number": null,
        "publisher": null,
        "metadata_source": "note"
      },
      "old_bib_lines": [
        "  title = {High-Precision and Efficient Anonymous Traffic Classification in the Real-World Network Environment},",
        "  author = {Longtian Xie and Shuiqiao Yang and Wei Ye and Guangcan Li and Yonglin Xie and Jian Zhang and Qixu Liu},",
        "  doi = {10.1109/TNET.2025.3582301},",
        "  url = {https://ieeexplore.ieee.org/document/11084593},"
      ],
      "source": "https://doi.org/10.1109/TON.2024.3518976"
    },
    {
      "key": "moore2025temponet",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/acsac67867.2025.00097"
    },
    {
      "key": "qiu2025gated",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.52202/085713-3345"
    },
    {
      "key": "unknown2025helios",
      "old_json_fields": {
        "title": "Helios: Learning and Adaptation of Matching Rules for Continual In-Network Malicious Trafic Detection",
        "authors": [
          "Shi, Zhenning",
          "Zhao, Dan",
          "Zhu, Yijia",
          "Xie, Guorui",
          "Li, Qing",
          "Jiang, Yong"
        ]
      },
      "old_bib_lines": [
        "  title = {Helios: Learning and Adaptation of Matching Rules for Continual In-Network Malicious Trafic Detection},"
      ],
      "source": "https://doi.org/10.1145/3696410.3714742"
    },
    {
      "key": "unknown2025advtg",
      "old_json_fields": {
        "title": "AdvTG: An Adversarial Trafic Generation Framework to Deceive DL-Based Malicious Trafic Detection Models",
        "authors": [
          "Sun, Peishuai",
          "Yun, Xiaochun",
          "Li, Shuhao",
          "Yin, Tao",
          "Si, Chengxiang",
          "Xie, Jiang"
        ]
      },
      "old_bib_lines": [
        "  title = {AdvTG: An Adversarial Trafic Generation Framework to Deceive DL-Based Malicious Trafic Detection Models},"
      ],
      "source": "https://doi.org/10.1145/3696410.3714876"
    },
    {
      "key": "wickramasinghe2025sok",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/sp61157.2025.00165"
    },
    {
      "key": "unknown2025odns",
      "old_json_fields": {
        "authors": [
          "Wu, Wenhao",
          "Wang, Zhaohua",
          "Li, Qinxin",
          "Li, Zihan",
          "Li, Yi",
          "Yan, Jin",
          "Li, Zhenyu"
        ]
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.1145/3696410.3714834"
    },
    {
      "key": "xue2025discriminative",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.14722/ndss.2025.240966"
    },
    {
      "key": "unknown2025not",
      "old_json_fields": {
        "authors": [
          "Yao, Yixuan",
          "Yang, Ming",
          "Liu, Zixia",
          "Dong, Kai",
          "Gu, Xiaodan",
          "Wang, Chunmian"
        ]
      },
      "old_bib_lines": [],
      "source": "https://doi.org/10.1145/3696410.3714767"
    },
    {
      "key": "zhan2025flowrefiner",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.52202/085713-4270"
    },
    {
      "key": "zhou2025trafficformer",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/sp61157.2025.00102"
    },
    {
      "key": "chen2024causality",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/infocom52122.2024.10621235"
    },
    {
      "key": "lopes2024flow",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.14722/ndss.2024.24337"
    },
    {
      "key": "matousek2024experience",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.23919/cnsm62983.2024.10814358"
    },
    {
      "key": "qing2024low",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.14722/ndss.2024.23081"
    },
    {
      "key": "sendner2024mirageflow",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.14722/ndss.2024.241133"
    },
    {
      "key": "shen2024real",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/sp54263.2024.00247"
    },
    {
      "key": "wails2024precisely",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.14722/ndss.2024.23394"
    },
    {
      "key": "deng2023robust",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/sp46215.2023.10179464"
    },
    {
      "key": "fauvel2023lightweight",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1145/3580305.3599762"
    },
    {
      "key": "fu2023detecting",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.14722/ndss.2023.23080"
    },
    {
      "key": "mathews2023sok",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/sp46215.2023.10179289"
    },
    {
      "key": "yang2023few",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1016/j.comnet.2023.109731"
    },
    {
      "key": "zhao2023yet",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1609/aaai.v37i4.25674"
    },
    {
      "key": "wang2022mtbd",
      "old_json_fields": {
        "doi": "10.1109/HPCC57118.2022.00178",
        "url": "",
        "pages": null,
        "metadata_source": "note"
      },
      "old_bib_lines": [
        "  doi = {10.1109/HPCC57118.2022.00178},"
      ],
      "source": "https://doi.org/10.1109/HPCC-DSS-SmartCity-DependSys57074.2022.00091"
    },
    {
      "key": "gong2022surakav",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/sp46214.2022.9833722"
    },
    {
      "key": "hartl2022separating",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/icmla55696.2022.00094"
    },
    {
      "key": "lin2022bert",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1145/3485447.3512217"
    },
    {
      "key": "alnaami2021bimorphing",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/tdsc.2019.2907240"
    },
    {
      "key": "wu2021detecting",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.14722/madweb.2021.23011"
    },
    {
      "key": "cadena2020trafficsliver",
      "old_json_fields": {
        "authors": [
          "Bhadauria, Rishabh",
          "Fang, Zhiyong",
          "Hazay, Carmit",
          "Venkitasubramaniam, Muthuramakrishnan",
          "Xie, Tiancheng",
          "Zhang, Yupeng"
        ],
        "doi": "10.1145/3372297.3417893",
        "url": "https://doi.org/10.1145/3372297.3417893",
        "pages": "2025-2038",
        "source_file": "2020-CCS-TrafficSliver-Fighting_Website_Fingerprinting_Attacks_with_Traffic_Splitting.pdf",
        "metadata_source": "note"
      },
      "old_bib_lines": [
        "  author = {Wladimir De la Cadena and Asya Mitseva and Jan Pennekamp and Fabian Lanze and Andriy Panchenko and Klaus Wehrle},",
        "  doi = {10.1145/3372297.3417893},"
      ],
      "source": "https://doi.org/10.1145/3372297.3423351"
    },
    {
      "key": "ede2020flowprint",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.14722/ndss.2020.24412"
    },
    {
      "key": "liu2019net",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/infocom.2019.8737507"
    },
    {
      "key": "shapira2019flowpic",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/infcomw.2019.8845315"
    },
    {
      "key": "shi2018efficient",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1016/j.comnet.2018.01.007"
    },
    {
      "key": "dusi2008detection",
      "old_json_fields": {},
      "old_bib_lines": [],
      "source": "https://doi.org/10.1109/icc.2008.334"
    }
  ],
  "note_fields": [
    {
      "file": "03-paper-notes/2026-arXiv-TrafficMoE__Heterogeneity-aware_Mixture_of_Experts_for_Encrypted_Traffic_Classification.md",
      "fields": {
        "doi": "unknown",
        "url": "https://arxiv.org/abs/2605",
        "updated": "2026-06-10"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-arXiv-Improving_the_Reliability_of_Anomaly_Detection_for_Encrypted_OPC_UA_Traffic_over_Private_5G.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "title_original": "IMPROVING THE RELIABILITY OF ANOMALY DETECTION FOR ENCRYPTED OPC UA TRAFFIC OVER PRIVATE 5G",
        "updated": "2026-09-29"
      },
      "rows": [
        "| 原文标题 | IMPROVING THE RELIABILITY OF ANOMALY DETECTION FOR ENCRYPTED OPC UA TRAFFIC OVER PRIVATE 5G |"
      ]
    },
    {
      "file": "03-paper-notes/2026-arXiv-Robust_Transceiver_Design_for_SIM-Assisted_Integrated_Sensing_and_Covert_Communications.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-USENIX-Towards_Practical_Few-shot_Multi-tab_Website_Fingerprinting.md",
      "fields": {
        "url": "unknown",
        "updated": "2026-11-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-USENIX-Remise__Authorized_Anonymous_Communication_Systems.md",
      "fields": {
        "updated": "2026-10-10"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-USENIX-Revelio__A_Global_Study_of_VoIP_Blocking.md",
      "fields": {
        "updated": "2026-10-10"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-TDSC-Learning_Flow_Semantics_for_Encrypted_Traffic_Analysis_A_Contrastive_Pre-training_Approach.md",
      "fields": {
        "pages": "7864–7877"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2025-TON-High_Precision_and_Efficient_Anonymous_Traffic_Classification_in_the_Real-World.md",
      "fields": {
        "pages": "966–981"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2022-HPCC-MTBD_HTTPS_Tunnel_Detection_Based_on_Multi-dimension_Traffic_Behaviors_Decision.md",
      "fields": {
        "doi": "10.1109/HPCC57118.2022.00178",
        "url": "",
        "updated": "2026-10-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2020-CCS-TrafficSliver-Fighting_Website_Fingerprinting_Attacks_with_Traffic_Splitting.md",
      "fields": {
        "doi": "https://doi.org/10.1145/3372297.3417893",
        "url": "unknown",
        "mineru_md": "",
        "authors": [
          "Wladimir De la Cadena",
          "Asya Mitseva",
          "Jan Pennekamp",
          "Fabian Lanze",
          "Andriy Panchenko",
          "Klaus Wehrle"
        ],
        "updated": "2026-06-14"
      },
      "rows": [
        "| 作者 | Wladimir De la Cadena, Asya Mitseva, Jan Pennekamp, Fabian Lanze, Andriy Panchenko, Klaus Wehrle |"
      ]
    },
    {
      "file": "03-paper-notes/2026-AES-The_Inevitability_of_Side-Channel_Leakage_in_Encrypted_Traffic.md",
      "fields": {
        "url": "https://doi.org/10.12263/DZXB.20251034",
        "updated": "2026-08-17"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-JCS-GAN-based_Tor_obfuscated_traffic_identification_on_imbalanced_datasets.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "year": 2026,
        "venue": "JCS",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": [
        "| 年份 | 2026 |",
        "| 会议/期刊 | JCS |"
      ]
    },
    {
      "file": "03-paper-notes/2026-arXiv-Exact_Second-Order_Asymptotics_in_Covert_Communication_Over_Discrete_Memoryless_Channels.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-arXiv-Feedback_Coding_Enables_Inference-Time_Covert_Agentic_Communication.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-arXiv-Multiplexing_approaches_to_thermoradiative_signatureless_communications.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-arXiv-Unknown-Traffic_Detection_Calibration_and_Shortcut_Reliance_in_Distilled_Encrypted-Traffic_Classifiers_over_One_Year.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-arXiv-Your_Model_Is_Leaking__Covert_Information_Transfer_through_LLM_Residual_Streams.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-TDSC-Ultimate_Encrypted_Traffic_Feature_Engineering_HTTPS_Encrypted_Traffic_Classification_Using_Restored_Application_Data_Unit_Length.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-TNSM-TunnelEye_An_Explainable_Framework_for_Real-Time_Detection_of_Malicious_DoH_Traffic_in_High-Speed_Backbone_Networks.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-WWW-RoFiRe__Robust_Website_Fingerprinting_on_Real-World_Tor_Traffic_via_Improved_Augmentation_and_Normalization.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "title_original": "RoFiRe: Robust Website Fingerprinting on Real-World Tor Trafic via Improved Augmentation and Normalization",
        "updated": "2026-10-10"
      },
      "rows": [
        "| 原文标题 | RoFiRe: Robust Website Fingerprinting on Real-World Tor Trafic via Improved Augmentation and Normalization |"
      ]
    },
    {
      "file": "03-paper-notes/2026-JCN-SaGNN__Encrypted_traffic_classification_with_semantic-aware_heterogeneous_graph_neural_network.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-arXiv-Secrets_in_Radio_Waves__Towards_Practical_and_Protocol-Agnostic_PHY_Information_Hiding.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-IMC-Replicability__Challenging_the_Myth_of_Randomness_Patterns_in_Encrypted_Traffic.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "title_original": "Replicability: Challenging the Myth of Randomness Paterns in Encrypted Trafic",
        "updated": "2026-09-29"
      },
      "rows": [
        "| 原文标题 | Replicability: Challenging the Myth of Randomness Paterns in Encrypted Trafic |"
      ]
    },
    {
      "file": "03-paper-notes/2026-WWW-SemFuzz__A_Semantics-Aware_Fuzzing_Framework_for_Network_Protocol_Implementations.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-10-10"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-JCS-Uncovering_robot_joint-level_controller_actions_from_encrypted_network _traffic__Empirical_attacks_and_information-theoretic_bounds.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-IMC-Quantifying_the_Privacy_Implications_of_High-Fidelity_Synthetic_Network_Traffic.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "title_original": "Quantifying the Privacy Implications of High-Fidelity Synthetic Network Trafic",
        "updated": "2026-09-29"
      },
      "rows": [
        "| 原文标题 | Quantifying the Privacy Implications of High-Fidelity Synthetic Network Trafic |"
      ]
    },
    {
      "file": "03-paper-notes/2026-IMC-Mind_the_Gap__Policy_vs_Reality_in_Post-Quantum_TLS_Deployment.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-WWW-Tracking_the_Stray_Sheep__Understanding_DNS_Response_Manipulation_in_the_Wild.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-10-10"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-JCS-PacketPatch__Practical_generation_and_deployment_of_adversarial_packets_for_byte-feature-based_encrypted_traffic_classification.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-TNSM-Robust_and_Invisible_Flow_Watermarking_With_Invertible_Neural_Network_for_Traffic_Tracking.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-WWW-Robust_LLM-Based_Website_Fingerprinting_under_Dynamic_Real-World_Conditions.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-10-10"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-JCN-Towards_adaptive_and_robust_website_fingerprinting_defense_with_multi-agent_deep_reinforcement_learning.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-09-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2025-WWW-Facing_Anomalies_Head-On__Network_Traffic_Anomaly_Detection_via_Uncertainty_Inspired_Inter-Sample_Differences.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "title_original": "Facing Anomalies Head-On: Network Trafic Anomaly Detection via Uncertainty-Inspired Inter-Sample Diferences",
        "updated": "2026-10-10"
      },
      "rows": [
        "| 原文标题 | Facing Anomalies Head-On: Network Trafic Anomaly Detection via Uncertainty-Inspired Inter-Sample Diferences |"
      ]
    },
    {
      "file": "03-paper-notes/2025-WWW-Helios__Learning_and_Adaptation_of_Matching_Rules_for_Continual_In_Network_Malicious_Traffic_Detection.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "title_original": "Helios: Learning and Adaptation of Matching Rules for Continual In-Network Malicious Trafic Detection",
        "updated": "2026-10-10"
      },
      "rows": [
        "| 原文标题 | Helios: Learning and Adaptation of Matching Rules for Continual In-Network Malicious Trafic Detection |"
      ]
    },
    {
      "file": "03-paper-notes/2025-WWW-AdvTG__An_Adversarial_Traffic_Generation_Framework_to_Deceive_DL-Based_Malicious_Traffic_Detection_Models.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "title_original": "AdvTG: An Adversarial Trafic Generation Framework to Deceive DL-Based Malicious Trafic Detection Models",
        "updated": "2026-10-10"
      },
      "rows": [
        "| 原文标题 | AdvTG: An Adversarial Trafic Generation Framework to Deceive DL-Based Malicious Trafic Detection Models |"
      ]
    },
    {
      "file": "03-paper-notes/2025-WWW-ODNS_Clustering__Unveiling_Client-Side_Dependency_in_Open_DNS_Infrastructure.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-10-10"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2025-WWW-Do_Not_Trust_What_They_Tell__Exposing_Malicious_Accomplices_in_Tor_via_Anomalous_Circuit_Detection.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "updated": "2026-10-10"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-arXiv-Despite_Instructions__Frontier_Agents_Improvise_Covert_Channels_at_Test_Time.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "title_original": "DESPITE INSTRUCTIONS: FRONTIER AGENTS IMPROVISE COVERT CHANNELS AT TEST TIME",
        "updated": "2026-09-29"
      },
      "rows": [
        "| 原文标题 | DESPITE INSTRUCTIONS: FRONTIER AGENTS IMPROVISE COVERT CHANNELS AT TEST TIME |"
      ]
    },
    {
      "file": "03-paper-notes/2026-arXiv-A_Priority-Aware_Dual-Channel_Feature_Fusion_Method_for_Urban_Rail_Service_Traffic_Classification.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "authors": [],
        "title_original": "A Priority-Aware Dual-Channel Feature Fusion Method for Urban Rail Service Trafic Classification",
        "updated": "2026-09-29"
      },
      "rows": [
        "| 原文标题 | A Priority-Aware Dual-Channel Feature Fusion Method for Urban Rail Service Trafic Classification |"
      ]
    },
    {
      "file": "03-paper-notes/2026-NDSS-TIPSO-GAN__Malicious_Network_Traffic_Detection_Using_a_Novel_Optimized_Generative_Adversarial_Network.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-10-10"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-PAM-The_Future_of_DNS_Privacy__A_Comparison_of_DNS_over_QUIC_and_DNS_over_HTTP3.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-09-19"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-CCPE-A_Lightweight_Deep_Learning_Framework_for_Encrypted_Traffic_Classification_via_Visual_Flow_Representation.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-JCN-DenTC__An_expandable_framework_for_dynamic_malicious_traffic_classification.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-arXiv-Conformal_Prediction_for_Offensive_Security.md",
      "fields": {
        "doi": "unknown",
        "updated": "2026-09-19"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-JCN-A_prototypical_alignment_approach_to_unknown_traffic_classification_using_BERT.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-05-27"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-TSC-Time_Will_Tell_Criss-cross_Transformer_for_Encrypted_Traffic_Analysis.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-05-27"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-PAM-Unpacking_Internet_Ossification__A_Large-Scale_Study_of_Path-Impairing_Middleboxes_Across_IPv4_and_IPv6.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-09-19"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-PAM-A_Measurement_of_Genuine_Tor_Traces_for_Realistic_Website_Fingerprinting.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-09-19"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-JCN-GMM-cGAN__Mitigating_data_scarcity_and_label_noise_for_robust_encrypted_malicious_traffic_classification.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-NDSS-Huma__Censorship_Circumvention_via_Web_Protocol_Tunneling_with_Deferred_Traffic_Replacement.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-11-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-WWW-Unveiling_the_Underground_Phishing_Ecosystem__A_12-Year_Longitudinal_Study_of_Deep_and_Dark_Web_Forums.md",
      "fields": {
        "doi": "unknown",
        "updated": "2026-10-10"
      },
      "rows": [
        "| DOI | 10.1145/3774904.3792737 |"
      ]
    },
    {
      "file": "03-paper-notes/2026-TNSM-Comparative_Analysis_of_Deep_Learning_Models_for_Real-World_ISP_Network_Traffic_Forecasting.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-09-19"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-JIoT-NetTTT_Online_Self-Adaptation_Inference_via_Test-Time_Training_for_Encrypted_Traffic_Classification.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-05-27"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-TIFS-Time-Hopping_Covert_Communication_With_Random_Slots_and_Dispersed_Energy.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-09-19"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-TIFS-Stinger__A_Light-Weight_Website_Fingerprinting_Defense_Through_Poisoning_Packet_Sequences.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-09-19"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-arXiv-PrismWF__A_Multi-Granularity_Patch-Based_Transformer_for_Robust_Website_Fingerprinting_Attack.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-KDD-Building_Transparency_in_Deep_Learning-Powered_Network_Traffic_Classification__A_Traffic-Explainer_Framework.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-WWW-Eclipse_Attacks_on_Ethereum’s_Peer-to-Peer_Network.md",
      "fields": {
        "doi": "unknown",
        "updated": "2026-10-10"
      },
      "rows": [
        "| DOI | 10.1145/3774904.3792231 |"
      ]
    },
    {
      "file": "03-paper-notes/2026-arXiv-Bias_in_the_Shadows__Explore_Shortcuts_in_Encrypted_Network_Traffic_Classification.md",
      "fields": {
        "doi": "unknown",
        "updated": "2026-10-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-NDSS-Cease_at_the_Ultimate_Goodness__Towards_Efficient_Website_Fingerprinting_Defense_via_Iterative_Mutual_Information_Minimization.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-11-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-TIFS-Data-Efficient_Cross-Domain_Few-Shot_Website_Fingerprinting_With_Unsupervised_Domain_Adaptation.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-09-19"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-arXiv-NetMamba+__A_Framework_of_Pre-trained_Models_for_Efficient_and_Accurate_Network_Traffic_Classification.md",
      "fields": {
        "doi": "unknown",
        "updated": "2026-06-10"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-WWW-HiFi-WF__Toward_Realistic_Website_Fingerprinting_with_Multi-tab_and_Subpage_Recognition.md",
      "fields": {
        "doi": "unknown",
        "updated": "2026-10-10"
      },
      "rows": [
        "| DOI | 10.1145/3774904.3792412 |"
      ]
    },
    {
      "file": "03-paper-notes/2026-JCN-Traffic_burst_relational_graph_attention_network_combined_position_encoding_for_traffic_classification.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-05-27"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-JCN-ByteDance__Let_bytes_perform_brilliantly_in_multi-view_encrypted_traffic_classification.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-05-27"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-ICASSP-TriFusion_A_Self-Supervised_Learning_Enhanced_Dual-Level_Multimodal_Framework_for_Traffic_Classification.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-arXiv-Multimodal_Reasoning_with_LLM_for_Encrypted_Traffic_Interpretation__A_Benchmark.md",
      "fields": {
        "doi": "",
        "url": "",
        "updated": "2026-06-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-JNSM-FGFR-Net_An_Improved_Residual_Network_Encrypted_Traffic_Classification_Model_Based_on_Byte-Level_Traffic_Graphs.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-05-27"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-JCN-Plug-in_enhancement_framework__Breaking_through_performance_bottleneck_of_pre-trained_models_for_encrypted_traffic_classification.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-CS-Hiding_the_Trees_in_the_Forest__Building_Network_Covert_Channels_with_Hash-Based_Covert_Carrier_Filtering.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2025-AAAI-MIETT__Multi-Instance_Encrypted_Traffic_Transformer_for_Encrypted_Traffic_Classification.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-09"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2025-ICNP-Non-uniformity_is_All_You_Need__Efficient_and_Timely_Encrypted_Traffic_Classification_With_ECHO.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-09-19"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2025-S&P-Countmamba__A_Generalized_Website_Fingerprinting_Attack_via_Coarse-Grained_Representation_and_Fine-Grained_Prediction.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-11-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2025-ICAACE-A_Semi-Supervised_Learning_Framework_for_Encrypted_Traffic_Classification_Based_on_Supervised_Contrastive_Learning_and_Masked_Sequence_Prediction_Tasks.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-05-27"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2025-IWQoS-MOTA_Mixture_of_Traffic_Agents_for_Robust_Network_Traffic_Classification.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-05-27"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2025-JPDC-Multi-ARCL__Multimodal_adaptive_relay-based_distributed_continual_learning_for_encrypted_traffic_classification.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-09"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2025-ACSAC-Pathfinder__Exploring_Path_Diversity_for_Assessing_Internet_Censorship_Inconsistency.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-09-19"
      },
      "rows": [
        "| DOI | unknown |"
      ]
    },
    {
      "file": "03-paper-notes/2025-IWQoS-TraGe_A_Generic_Packet_Representation_for_Traffic_Classification_Based_on_Header-Payload_Differences.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-09"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2025-ACSAC-TempoNet__Learning_Realistic_Communication_and_Timing_Patterns_for_Network_Traffic_Simulation.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-09-19"
      },
      "rows": [
        "| DOI | unknown |"
      ]
    },
    {
      "file": "03-paper-notes/2025-NIPS-Gated_Attention_for_Larg.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-10-10"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2025-S&P-SoK_Decoding_the_Enigma_of_Encrypted_Network_Traffic_Classifiers.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-11-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2025-NDSS-The_Discriminative_Power_of_Cross-layer_RTTs_in_Fingerprinting_Proxy_Traffic.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-10-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2025-NIPS-FlowRefiner__A_Robust_Traffic_Classification_Framework_against_Label_Noise.md",
      "fields": {
        "doi": "",
        "url": "",
        "updated": "2026-06-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2025-S&P-TrafficFormer_An_Efficient_Pre-trained_Model_for_Traffic_Data.md",
      "fields": {
        "doi": "",
        "url": "",
        "updated": "2026-11-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2024-INFOCOM-Causality_Correlation_and_Context_Learning_Aided_Robust_Lightweight_Multi-Tab_Website_Fingerprinting_Over_Encrypted_Tunnel.md",
      "fields": {
        "doi": "",
        "url": "",
        "updated": "2026-05-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2024-NDSS-Flow_Correlation_Attacks_on_Tor_Onion_Service_Sessions_with_Sliding_Subset_Sum.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-11-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2024-CNSM-Experience__Report_Using_JA4_Fingerprints_for_Malware_Detection_in_Encrypted_Traffic.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-05-27"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2024-NDSS-Low-quality_training_data_only__A_robust_framework_for_detecting_encrypted_malicious_network_traffic.md",
      "fields": {
        "doi": "",
        "url": "",
        "updated": "2026-11-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2024-NDSS-MirageFlow__A_New_Bandwidth_Inflation_Attack_on_Tor.md",
      "fields": {
        "doi": "unknown",
        "updated": "2026-11-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2024-S&P-Real-Time_Website_Fingerprinting_Defense_via_Traffic_Cluster_Anonymization.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-11-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2024-NDSS-On_Precisely_Detecting_Censorship_Circumvention_in_Real-World_Networks.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2023-SIGKDD-A_lightweight__efficient_and_explainable__by__design_convolutional_neural_network_for_internet_traffic_classification.md",
      "fields": {
        "doi": "",
        "url": "",
        "updated": "2026-05-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2023-NDSS-Detecting_unknown_encrypted_malicious_traffic_in_real_time_via_flow_interaction_graph_analysis.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-03"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2023-S&P-SoK__A_Critical_Evaluation_of_Efficient_Website_Fingerprinting_Defenses.md",
      "fields": {
        "updated": "2026-06-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2023-ComputerNetworks-Few-shot_encrypted_traffic_classification_via_multi-task_representation_enhanced_meta-learning.md",
      "fields": {
        "doi": "",
        "url": "",
        "updated": "2026-05-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2023-AAAI-Yet_Another_Traffic_Classifier_a_Masked_Autoencoder_Based_Traffic_Transformer_With_Multi-level_Flow_Representation.md",
      "fields": {
        "doi": "",
        "url": "",
        "updated": "2026-10-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2022-S&P-Surakav__Generating_Realistic_Traces_for_a_Strong_Website_Fingerprinting_Defense.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2022-ICMLA-Separating_Flows_in_Encrypted_Tunnel_Traffic.md",
      "fields": {
        "doi": "",
        "url": "",
        "updated": "2026-05-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2022-WWW-ET-BERT__A_Contextualized_Datagram_Representation_with_Pre-training_Transformers_for_Encrypted_Traffic_Classification.md",
      "fields": {
        "doi": "",
        "url": "",
        "updated": "2026-10-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2021-TDSC-BiMorphing_A_Bi-Directional_Bursting_Defense_against_Website_Fingerprinting_Attacks.md",
      "fields": {
        "updated": "2026-06-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2021-NDSS-Detecting_Tor_Bridge_from_Sampled_Traffic_in_Backbone_Networks.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-10-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2020-NDSS-Flowprint__Semi-Supervised_Mobile-App_Fingerprinting_on_Encrypted_Network_Traffic.md",
      "fields": {
        "doi": "",
        "updated": "2026-10-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2019-INFOCOM-FS-Net__A_Flow_Sequence_Network_For_Encrypted_Traffic_Classification.md",
      "fields": {
        "doi": "",
        "url": "",
        "updated": "2026-10-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2019-INFOCOM-FlowPic__Encrypted_Internet_Traffic_Classification_is_as_Easy_as_Image_Recognition.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-06-09"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2018-CS-An_Efficient_Feature_Generation_Approach_Based_on_Deep_Learning_and_Feature_Selection_Techniques_for_Traffic_Classification.md",
      "fields": {
        "doi": "",
        "url": "",
        "updated": "2026-05-29"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2008-ICC-Detection_of_Encrypted_Tunnels_Across_Network_Boundaries.md",
      "fields": {
        "doi": "unknown",
        "url": "unknown",
        "updated": "2026-10-21"
      },
      "rows": []
    },
    {
      "file": "03-paper-notes/2026-WWW-Forge__A_Robust_Multi-tab_Website_Fingerprinting_Attack_Via_Blind_Source_Separation.md",
      "fields": {
        "doi": "unknown",
        "updated": "2026-10-10"
      },
      "rows": [
        "| DOI | 10.1145/3774904.3792410 |"
      ]
    }
  ],
  "registry_rows": [
    "| 1 | unknown | detection of encrypted tunnels across network boundaries | 2008 | ICC | Alshammari | 2008-ICC-Detection_of_Encrypted_Tunnels_Across_Network_Boundaries | [[2008-ICC-Detection_of_Encrypted_Tunnels_Across_Network_Boundaries]] | 0 | 0 |",
    "| 3 | unknown | an efficient feature generation approach based on deep learning and feature selection techniques for traffic classification | 2018 | CS (Elsevier) | Shi | 2018-CS-An_Efficient_Feature_Generation_Approach_Based_on_Deep_Learning_and_Feature_Selection_Techniques_for_Traffic_Classification | [[2018-CS-An_Efficient_Feature_Generation_Approach_Based_on_Deep_Learning_and_Feature_Selection_Techniques_for_Traffic_Classification]] | 0 | 0 |",
    "| 5 | unknown | fs-net a flow sequence network for encrypted traffic classification | 2019 | INFOCOM | Liu | 2019-INFOCOM-FS-Net__A_Flow_Sequence_Network_For_Encrypted_Traffic_Classification | [[2019-INFOCOM-FS-Net__A_Flow_Sequence_Network_For_Encrypted_Traffic_Classification]] | 0 | 0 |",
    "| 6 | unknown | flowprint semi-supervised mobile-app fingerprinting on encrypted network traffic | 2020 | NDSS | van der Horst | 2020-NDSS-Flowprint__Semi-Supervised_Mobile-App_Fingerprinting_on_Encrypted_Network_Traffic | [[2020-NDSS-Flowprint__Semi-Supervised_Mobile-App_Fingerprinting_on_Encrypted_Network_Traffic]] | 0 | 0 |",
    "| 11 | unknown | mtbd https tunnel detection based on multi-dimension traffic behaviors decision | 2022 | HPCC | Li | 2022-HPCC-MTBD_HTTPS_Tunnel_Detection_Based_on_Multi-dimension_Traffic_Behaviors_Decision | [[2022-HPCC-MTBD_HTTPS_Tunnel_Detection_Based_on_Multi-dimension_Traffic_Behaviors_Decision]] | 0 | 0 |",
    "| 12 | unknown | separating flows in encrypted tunnel traffic | 2022 | ICMLA | Rainer | 2022-ICMLA-Separating_Flows_in_Encrypted_Tunnel_Traffic | [[2022-ICMLA-Separating_Flows_in_Encrypted_Tunnel_Traffic]] | 0 | 0 |",
    "| 14 | unknown | et-bert a contextualized datagram representation with pre-training transformers for encrypted traffic classification | 2022 | WWW | Lin | 2022-WWW-ET-BERT__A_Contextualized_Datagram_Representation_with_Pre-training_Transformers_for_Encrypted_Traffic_Classification | [[2022-WWW-ET-BERT__A_Contextualized_Datagram_Representation_with_Pre-training_Transformers_for_Encrypted_Traffic_Classification]] | 3 | 0 |",
    "| 15 | unknown | yet another traffic classifier a masked autoencoder based traffic transformer with multi-level flow representation | 2023 | AAAI | Ren | 2023-AAAI-Yet_Another_Traffic_Classifier_a_Masked_Autoencoder_Based_Traffic_Transformer_With_Multi-level_Flow_Representation | [[2023-AAAI-Yet_Another_Traffic_Classifier_a_Masked_Autoencoder_Based_Traffic_Transformer_With_Multi-level_Flow_Representation]] | 2 | 0 |",
    "| 16 | unknown | few-shot encrypted traffic classification via multi-task representation enhanced meta-learning | 2023 | Computer Networks | Liu | 2023-ComputerNetworks-Few-shot_encrypted_traffic_classification_via_multi-task_representation_enhanced_meta-learning | [[2023-ComputerNetworks-Few-shot_encrypted_traffic_classification_via_multi-task_representation_enhanced_meta-learning]] | 0 | 0 |",
    "| 17 | unknown | a lightweight efficient and explainable-by-design convolutional neural network for internet traffic classification | 2023 | SIGKDD | Pachl | 2023-SIGKDD-A_lightweight__efficient_and_explainable__by__design_convolutional_neural_network_for_internet_traffic_classification | [[2023-SIGKDD-A_lightweight__efficient_and_explainable__by__design_convolutional_neural_network_for_internet_traffic_classification]] | 0 | 0 |",
    "| 19 | unknown | experience report using ja4 fingerprints for malware detection in encrypted traffic | 2024 | CNSM | Pousek | 2024-CNSM-Experience__Report_Using_JA4_Fingerprints_for_Malware_Detection_in_Encrypted_Traffic | [[2024-CNSM-Experience__Report_Using_JA4_Fingerprints_for_Malware_Detection_in_Encrypted_Traffic]] | 0 | 0 |",
    "| 20 | unknown | causality correlation and context learning aided robust lightweight multi-tab website fingerprinting over encrypted tunnel | 2024 | INFOCOM | Chen | 2024-INFOCOM-Causality_Correlation_and_Context_Learning_Aided_Robust_Lightweight_Multi-Tab_Website_Fingerprinting_Over_Encrypted_Tunnel | [[2024-INFOCOM-Causality_Correlation_and_Context_Learning_Aided_Robust_Lightweight_Multi-Tab_Website_Fingerprinting_Over_Encrypted_Tunnel]] | 0 | 0 |",
    "| 21 | unknown | real-time website fingerprinting defense via traffic cluster anonymization | 2024 | S&P | Deng | 2024-S&P-Real-Time_Website_Fingerprinting_Defense_via_Traffic_Cluster_Anonymization | [[2024-S&P-Real-Time_Website_Fingerprinting_Defense_via_Traffic_Cluster_Anonymization]] | 1 | 1 |",
    "| 29 | unknown | a semi-supervised learning framework for encrypted traffic classification based on supervised contrastive learning | 2025 | ICAACE | Wang | 2025-ICAACE-A_Semi-Supervised_Learning_Framework_for_Encrypted_Traffic_Classification_Based_on_Supervised_Contrastive_Learning_and_Masked_Sequence_Prediction_Tasks | [[2025-ICAACE-A_Semi-Supervised_Learning_Framework_for_Encrypted_Traffic_Classification_Based_on_Supervised_Contrastive_Learning_and_Masked_Sequence_Prediction_Tasks]] | 0 | 0 |",
    "| 31 | unknown | mota mixture of traffic agents for robust network traffic classification | 2025 | IWQoS | Chen | 2025-IWQoS-MOTA_Mixture_of_Traffic_Agents_for_Robust_Network_Traffic_Classification | [[2025-IWQoS-MOTA_Mixture_of_Traffic_Agents_for_Robust_Network_Traffic_Classification]] | 0 | 0 |",
    "| 32 | unknown | gated attention for large language models non-linearity sparsity and attention-sink-free | 2025 | NeurIPS | Zhang | 2025-NIPS-Gated_Attention_for_Larg | [[2025-NIPS-Gated_Attention_for_Larg]] | 0 | 0 |",
    "| 33 | unknown | sok decoding the enigma of encrypted network traffic classifiers | 2025 | S&P | Ning | 2025-S&P-SoK_Decoding_the_Enigma_of_Encrypted_Network_Traffic_Classifiers | [[2025-S&P-SoK_Decoding_the_Enigma_of_Encrypted_Network_Traffic_Classifiers]] | 3 | 0 |",
    "| 39 | unknown | netmamba+ a framework of pre-trained models for efficient and accurate network traffic classification | 2026 | arXiv | Ye | 2026-arXiv-NetMamba+__A_Framework_of_Pre-trained_Models_for_Efficient_and_Accurate_Network_Traffic_Classification | [[2026-arXiv-NetMamba+__A_Framework_of_Pre-trained_Models_for_Efficient_and_Accurate_Network_Traffic_Classification]] | 2 | 0 |",
    "| 41 | unknown | bytedance let bytes perform brilliantly in multi-view encrypted traffic classification | 2026 | JNCA | Wang | 2026-JCN-ByteDance__Let_bytes_perform_brilliantly_in_multi-view_encrypted_traffic_classification | [[2026-JCN-ByteDance__Let_bytes_perform_brilliantly_in_multi-view_encrypted_traffic_classification]] | 0 | 0 |",
    "| 42 | unknown | a prototypical alignment approach to unknown traffic classification using bert | 2026 | JCN | Li | 2026-JCN-A_prototypical_alignment_approach_to_unknown_traffic_classification_using_BERT | [[2026-JCN-A_prototypical_alignment_approach_to_unknown_traffic_classification_using_BERT]] | 0 | 0 |",
    "| 43 | unknown | traffic burst relational graph attention network combined position encoding for traffic classification | 2026 | JCN | Zhang | 2026-JCN-Traffic_burst_relational_graph_attention_network_combined_position_encoding_for_traffic_classification | [[2026-JCN-Traffic_burst_relational_graph_attention_network_combined_position_encoding_for_traffic_classification]] | 0 | 0 |",
    "| 44 | unknown | netttt online self-adaptation inference via test-time training for encrypted traffic classification | 2026 | JIoT | Chen | 2026-JIoT-NetTTT_Online_Self-Adaptation_Inference_via_Test-Time_Training_for_Encrypted_Traffic_Classification | [[2026-JIoT-NetTTT_Online_Self-Adaptation_Inference_via_Test-Time_Training_for_Encrypted_Traffic_Classification]] | 0 | 0 |",
    "| 46 | unknown | fgfr-net an improved residual network encrypted traffic classification model based on byte-level traffic graphs | 2026 | JNSM | Yang | 2026-JNSM-FGFR-Net_An_Improved_Residual_Network_Encrypted_Traffic_Classification_Model_Based_on_Byte-Level_Traffic_Graphs | [[2026-JNSM-FGFR-Net_An_Improved_Residual_Network_Encrypted_Traffic_Classification_Model_Based_on_Byte-Level_Traffic_Graphs]] | 0 | 0 |",
    "| 50 | unknown | time will tell criss-cross transformer for encrypted traffic analysis | 2026 | TSC | Ding | 2026-TSC-Time_Will_Tell_Criss-cross_Transformer_for_Encrypted_Traffic_Analysis | [[2026-TSC-Time_Will_Tell_Criss-cross_Transformer_for_Encrypted_Traffic_Analysis]] | 0 | 0 |",
    "| 55 | unknown | detecting unknown encrypted malicious traffic in real time via flow interaction graph analysis | 2023 | NDSS | Fu | 2023-NDSS-Detecting_unknown_encrypted_malicious_traffic_in_real_time_via_flow_interaction_graph_analysis | [[2023-NDSS-Detecting_unknown_encrypted_malicious_traffic_in_real_time_via_flow_interaction_graph_analysis]] | 0 | 0 |",
    "| 56 | unknown | robust multi-tab website fingerprinting attacks in the wild | 2023 | S&P | Shen | 2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild | [[2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild]] | 0 | 0 |",
    "| 61 | unknown | low-quality training data only a robust framework for detecting encrypted malicious network traffic | 2024 | NDSS | Qing | 2024-NDSS-Low-quality_training_data_only__A_robust_framework_for_detecting_encrypted_malicious_network_traffic | [[2024-NDSS-Low-quality_training_data_only__A_robust_framework_for_detecting_encrypted_malicious_network_traffic]] | 0 | 0 |",
    "| 65 | unknown | flowrefiner a robust traffic classification framework against label noise | 2025 | NeurIPS | Zhan | 2025-NIPS-FlowRefiner__A_Robust_Traffic_Classification_Framework_against_Label_Noise | [[2025-NIPS-FlowRefiner__A_Robust_Traffic_Classification_Framework_against_Label_Noise]] | 0 | 0 |",
    "| 66 | unknown | trafficformer an efficient pre-trained model for traffic data | 2025 | S&P | Zhou | 2025-S&P-TrafficFormer_An_Efficient_Pre-trained_Model_for_Traffic_Data | [[2025-S&P-TrafficFormer_An_Efficient_Pre-trained_Model_for_Traffic_Data]] | 0 | 0 |",
    "| 70 | unknown | a lightweight deep learning framework for encrypted traffic classification via visual flow representation | 2026 | CCPE | Chen | 2026-CCPE-A_Lightweight_Deep_Learning_Framework_for_Encrypted_Traffic_Classification_via_Visual_Flow_Representation | [[2026-CCPE-A_Lightweight_Deep_Learning_Framework_for_Encrypted_Traffic_Classification_via_Visual_Flow_Representation]] | 0 | 0 |",
    "| 71 | unknown | trifusion a self-supervised learning enhanced dual-level multimodal framework for traffic classification | 2026 | ICASSP | Wang | 2026-ICASSP-TriFusion_A_Self-Supervised_Learning_Enhanced_Dual-Level_Multimodal_Framework_for_Traffic_Classification | [[2026-ICASSP-TriFusion_A_Self-Supervised_Learning_Enhanced_Dual-Level_Multimodal_Framework_for_Traffic_Classification]] | 0 | 0 |",
    "| 72 | unknown | dentc an expandable framework for dynamic malicious traffic classification | 2026 | JCN | Li | 2026-JCN-DenTC__An_expandable_framework_for_dynamic_malicious_traffic_classification | [[2026-JCN-DenTC__An_expandable_framework_for_dynamic_malicious_traffic_classification]] | 0 | 0 |",
    "| 73 | unknown | gmm-cgan mitigating data scarcity and label noise for robust encrypted malicious traffic classification | 2026 | JCN | Chen | 2026-JCN-GMM-cGAN__Mitigating_data_scarcity_and_label_noise_for_robust_encrypted_malicious_traffic_classification | [[2026-JCN-GMM-cGAN__Mitigating_data_scarcity_and_label_noise_for_robust_encrypted_malicious_traffic_classification]] | 0 | 0 |",
    "| 74 | unknown | plug-in enhancement framework breaking through performance bottleneck of pre-trained models for encrypted traffic classification | 2026 | JCN | Wang | 2026-JCN-Plug-in_enhancement_framework__Breaking_through_performance_bottleneck_of_pre-trained_models_for_encrypted_traffic_classification | [[2026-JCN-Plug-in_enhancement_framework__Breaking_through_performance_bottleneck_of_pre-trained_models_for_encrypted_traffic_classification]] | 0 | 0 |",
    "| 75 | unknown | building transparency in deep learning-powered network traffic classification a traffic-explainer framework | 2026 | KDD | Zhou | 2026-KDD-Building_Transparency_in_Deep_Learning-Powered_Network_Traffic_Classification__A_Traffic-Explainer_Framework | [[2026-KDD-Building_Transparency_in_Deep_Learning-Powered_Network_Traffic_Classification__A_Traffic-Explainer_Framework]] | 0 | 0 |",
    "| 77 | unknown | bias in the shadows explore shortcuts in encrypted network traffic classification | 2026 | arXiv | Li | 2026-arXiv-Bias_in_the_Shadows__Explore_Shortcuts_in_Encrypted_Network_Traffic_Classification | [[2026-arXiv-Bias_in_the_Shadows__Explore_Shortcuts_in_Encrypted_Network_Traffic_Classification]] | 1 | 0 |",
    "| 79 | unknown | traffimoe heterogeneity-aware mixture of experts for encrypted traffic classification | 2026 | arXiv | Ye | 2026-arXiv-TrafficMoE__Heterogeneity-aware_Mixture_of_Experts_for_Encrypted_Traffic_Classification | [[2026-arXiv-TrafficMoE__Heterogeneity-aware_Mixture_of_Experts_for_Encrypted_Traffic_Classification]] | 2 | 0 |",
    "| 80 | unknown | flowpic encrypted internet traffic classification is as easy as image recognition | 2019 | INFOCOM | Tamer | 2019-INFOCOM-FlowPic__Encrypted_Internet_Traffic_Classification_is_as_Easy_as_Image_Recognition | [[2019-INFOCOM-FlowPic__Encrypted_Internet_Traffic_Classification_is_as_Easy_as_Image_Recognition]] | 0 | 0 |",
    "| 81 | unknown | detecting tor bridge from sampled traffic in backbone networks | 2021 | NDSS | Zhao | 2021-NDSS-Detecting_Tor_Bridge_from_Sampled_Traffic_in_Backbone_Networks | [[2021-NDSS-Detecting_Tor_Bridge_from_Sampled_Traffic_in_Backbone_Networks]] | 0 | 0 |",
    "| 83 | unknown | flow correlation attacks on tor onion service sessions with sliding subset sum | 2024 | NDSS | Lopes | 2024-NDSS-Flow_Correlation_Attacks_on_Tor_Onion_Service_Sessions_with_Sliding_Subset_Sum | [[2024-NDSS-Flow_Correlation_Attacks_on_Tor_Onion_Service_Sessions_with_Sliding_Subset_Sum]] | 0 | 0 |",
    "| 84 | unknown | mirageflow a new bandwidth inflation attack on tor | 2024 | NDSS | Wu | 2024-NDSS-MirageFlow__A_New_Bandwidth_Inflation_Attack_on_Tor | [[2024-NDSS-MirageFlow__A_New_Bandwidth_Inflation_Attack_on_Tor]] | 0 | 0 |",
    "| 88 | unknown | miett multi-instance encrypted traffic transformer for encrypted traffic classification | 2025 | AAAI | Hu | 2025-AAAI-MIETT__Multi-Instance_Encrypted_Traffic_Transformer_for_Encrypted_Traffic_Classification | [[2025-AAAI-MIETT__Multi-Instance_Encrypted_Traffic_Transformer_for_Encrypted_Traffic_Classification]] | 0 | 0 |",
    "| 89 | unknown | trage a generic packet representation for traffic classification based on header-payload differences | 2025 | IWQoS | Ren | 2025-IWQoS-TraGe_A_Generic_Packet_Representation_for_Traffic_Classification_Based_on_Header-Payload_Differences | [[2025-IWQoS-TraGe_A_Generic_Packet_Representation_for_Traffic_Classification_Based_on_Header-Payload_Differences]] | 0 | 0 |",
    "| 91 | unknown | multi-arcl multimodal adaptive relay-based distributed continual learning for encrypted traffic classification | 2025 | JPDC | Li | 2025-JPDC-Multi-ARCL__Multimodal_adaptive_relay-based_distributed_continual_learning_for_encrypted_traffic_classification | [[2025-JPDC-Multi-ARCL__Multimodal_adaptive_relay-based_distributed_continual_learning_for_encrypted_traffic_classification]] | 0 | 0 |",
    "| 93 | 10.1109/TNET.2025.3582301 | high-precision and efficient anonymous traffic classification in the real-world network environment | 2025 | TON | Xie | 2025-TON-High_Precision_and_Efficient_Anonymous_Traffic_Classification_in_the_Real-World | [[2025-TON-High_Precision_and_Efficient_Anonymous_Traffic_Classification_in_the_Real-World]] | 0 | 0 |",
    "| 94 | 10.1109/TDSC.2025.3596462 | learning flow semantics via contrastive pre-training for encrypted traffic analysis | 2026 | TDSC | Liu | 2026-TDSC-Learning_Flow_Semantics_for_Encrypted_Traffic_Analysis_A_Contrastive_Pre-training_Approach | [[2026-TDSC-Learning_Flow_Semantics_for_Encrypted_Traffic_Analysis_A_Contrastive_Pre-training_Approach]] | 0 | 0 |",
    "| 100 | unknown | bimorphing a bidirectional bursting defense against website fingerprinting attacks | 2021 | TDSC | Al-Naami | 2021-TDSC-BiMorphing_A_Bi-Directional_Bursting_Defense_against_Website_Fingerprinting_Attacks | [[2021-TDSC-BiMorphing_A_Bi-Directional_Bursting_Defense_against_Website_Fingerprinting_Attacks]] | 0 | 0 |",
    "| 103 | unknown | surakav generating realistic traces for a strong website fingerprinting defense | 2022 | S&P | Gong | 2022-S&P-Surakav__Generating_Realistic_Traces_for_a_Strong_Website_Fingerprinting_Defense | [[2022-S&P-Surakav__Generating_Realistic_Traces_for_a_Strong_Website_Fingerprinting_Defense]] | 0 | 0 |",
    "| 109 | unknown | sok a critical evaluation of efficient website fingerprinting defenses | 2023 | S&P | Mathews | 2023-S&P-SoK__A_Critical_Evaluation_of_Efficient_Website_Fingerprinting_Defenses | [[2023-S&P-SoK__A_Critical_Evaluation_of_Efficient_Website_Fingerprinting_Defenses]] | 0 | 0 |",
    "| 114 | unknown | on precisely detecting censorship circumvention in realworld networks | 2024 | NDSS | Wails | 2024-NDSS-On_Precisely_Detecting_Censorship_Circumvention_in_Real-World_Networks | [[2024-NDSS-On_Precisely_Detecting_Censorship_Circumvention_in_Real-World_Networks]] | 0 | 0 |",
    "| 124 | unknown | the discriminative power of crosslayer rtts in fingerprinting proxy traffic | 2025 | NDSS | Xue | 2025-NDSS-The_Discriminative_Power_of_Cross-layer_RTTs_in_Fingerprinting_Proxy_Traffic | [[2025-NDSS-The_Discriminative_Power_of_Cross-layer_RTTs_in_Fingerprinting_Proxy_Traffic]] | 0 | 0 |",
    "| 125 | unknown | countmamba a generalized website fingerprinting attack via coarsegrained representation and finegrained prediction | 2025 | S&P | Deng | 2025-S&P-Countmamba__A_Generalized_Website_Fingerprinting_Attack_via_Coarse-Grained_Representation_and_Fine-Grained_Prediction | [[2025-S&P-Countmamba__A_Generalized_Website_Fingerprinting_Attack_via_Coarse-Grained_Representation_and_Fine-Grained_Prediction]] | 0 | 0 |",
    "| 131 | unknown | hiding the trees in the forest building network covert channels with hashbased covert carrier filtering | 2026 | CS | Zou | 2026-CS-Hiding_the_Trees_in_the_Forest__Building_Network_Covert_Channels_with_Hash-Based_Covert_Carrier_Filtering | [[2026-CS-Hiding_the_Trees_in_the_Forest__Building_Network_Covert_Channels_with_Hash-Based_Covert_Carrier_Filtering]] | 0 | 0 |",
    "| 133 | unknown | cease at the ultimate goodness towards efficient website fingerprinting defense via iterative mutual information minimization | 2026 | NDSS | Wang | 2026-NDSS-Cease_at_the_Ultimate_Goodness__Towards_Efficient_Website_Fingerprinting_Defense_via_Iterative_Mutual_Information_Minimization | [[2026-NDSS-Cease_at_the_Ultimate_Goodness__Towards_Efficient_Website_Fingerprinting_Defense_via_Iterative_Mutual_Information_Minimization]] | 0 | 0 |",
    "| 135 | unknown | huma censorship circumvention via web protocol tunneling with deferred traffic replacement | 2026 | NDSS | Kamali | 2026-NDSS-Huma__Censorship_Circumvention_via_Web_Protocol_Tunneling_with_Deferred_Traffic_Replacement | [[2026-NDSS-Huma__Censorship_Circumvention_via_Web_Protocol_Tunneling_with_Deferred_Traffic_Replacement]] | 0 | 0 |",
    "| 141 | unknown | multimodal reasoning with llm for encrypted traffic interpretation a benchmark | 2026 | arXiv | Zhang | 2026-arXiv-Multimodal_Reasoning_with_LLM_for_Encrypted_Traffic_Interpretation__A_Benchmark | [[2026-arXiv-Multimodal_Reasoning_with_LLM_for_Encrypted_Traffic_Interpretation__A_Benchmark]] | 0 | 0 |",
    "| 142 | unknown | prismwf a multigranularity patchbased transformer for robust website fingerprinting attack | 2026 | arXiv | Pan | 2026-arXiv-PrismWF__A_Multi-Granularity_Patch-Based_Transformer_for_Robust_Website_Fingerprinting_Attack | [[2026-arXiv-PrismWF__A_Multi-Granularity_Patch-Based_Transformer_for_Robust_Website_Fingerprinting_Attack]] | 0 | 0 |",
    "| 145 | 10.12263/DZXB.20251034 | the inevitability of sidechannel leakage in encrypted traffic | 2026 | 电子学报 (AES) | Liu | 2026-AES-The_Inevitability_of_Side-Channel_Leakage_in_Encrypted_Traffic | [[2026-AES-The_Inevitability_of_Side-Channel_Leakage_in_Encrypted_Traffic]] | 0 | 0 |",
    "| 172 | unknown | pathfinder exploring path diversity for assessing internet censorship inconsistency | 2025 | ACSAC | Liang | 2025-ACSAC-Pathfinder__Exploring_Path_Diversity_for_Assessing_Internet_Censorship_Inconsistency | [[2025-ACSAC-Pathfinder__Exploring_Path_Diversity_for_Assessing_Internet_Censorship_Inconsistency]] | 2 | 0 |",
    "| 173 | unknown | temponet learning realistic communication and timing patterns for network traffic simulation | 2025 | ACSAC | Moore | 2025-ACSAC-TempoNet__Learning_Realistic_Communication_and_Timing_Patterns_for_Network_Traffic_Simulation | [[2025-ACSAC-TempoNet__Learning_Realistic_Communication_and_Timing_Patterns_for_Network_Traffic_Simulation]] | 0 | 0 |",
    "| 177 | unknown | non uniformity is all you need efficient and timely encrypted traffic classification with echo | 2025 | ICNP | Daum | 2025-ICNP-Non-uniformity_is_All_You_Need__Efficient_and_Timely_Encrypted_Traffic_Classification_With_ECHO | [[2025-ICNP-Non-uniformity_is_All_You_Need__Efficient_and_Timely_Encrypted_Traffic_Classification_With_ECHO]] | 3 | 0 |",
    "| 199 | 10.5281/zenodo.17759516 | tipso gan malicious network traffic detection using a novel optimized generative adversarial network | 2026 | NDSS | Akpaku | 2026-NDSS-TIPSO-GAN__Malicious_Network_Traffic_Detection_Using_a_Novel_Optimized_Generative_Adversarial_Network | [[2026-NDSS-TIPSO-GAN__Malicious_Network_Traffic_Detection_Using_a_Novel_Optimized_Generative_Adversarial_Network]] | 1 | 1 |",
    "| 203 | unknown | a measurement of genuine tor traces for realistic website fingerprinting | 2026 | PAM | Jansen | 2026-PAM-A_Measurement_of_Genuine_Tor_Traces_for_Realistic_Website_Fingerprinting | [[2026-PAM-A_Measurement_of_Genuine_Tor_Traces_for_Realistic_Website_Fingerprinting]] | 1 | 0 |",
    "| 204 | unknown | the future of dns privacy a comparison of dns over quic and dns over http 3 | 2026 | PAM | Bielefeld | 2026-PAM-The_Future_of_DNS_Privacy__A_Comparison_of_DNS_over_QUIC_and_DNS_over_HTTP3 | [[2026-PAM-The_Future_of_DNS_Privacy__A_Comparison_of_DNS_over_QUIC_and_DNS_over_HTTP3]] | 0 | 0 |",
    "| 205 | unknown | unpacking internet ossification a large scale study of path impairing middleboxes across ipv4 and ipv6 | 2026 | PAM | Hilal | 2026-PAM-Unpacking_Internet_Ossification__A_Large-Scale_Study_of_Path-Impairing_Middleboxes_Across_IPv4_and_IPv6 | [[2026-PAM-Unpacking_Internet_Ossification__A_Large-Scale_Study_of_Path-Impairing_Middleboxes_Across_IPv4_and_IPv6]] | 0 | 0 |",
    "| 211 | unknown | data efficient cross domain few shot website fingerprinting with unsupervised domain adaptation | 2026 | TIFS | Wang | 2026-TIFS-Data-Efficient_Cross-Domain_Few-Shot_Website_Fingerprinting_With_Unsupervised_Domain_Adaptation | [[2026-TIFS-Data-Efficient_Cross-Domain_Few-Shot_Website_Fingerprinting_With_Unsupervised_Domain_Adaptation]] | 1 | 0 |",
    "| 215 | unknown | stinger a light weight website fingerprinting defense through poisoning packet sequences | 2026 | TIFS | Nie | 2026-TIFS-Stinger__A_Light-Weight_Website_Fingerprinting_Defense_Through_Poisoning_Packet_Sequences | [[2026-TIFS-Stinger__A_Light-Weight_Website_Fingerprinting_Defense_Through_Poisoning_Packet_Sequences]] | 2 | 0 |",
    "| 216 | unknown | time hopping covert communication with random slots and dispersed energy | 2026 | TIFS | Lu | 2026-TIFS-Time-Hopping_Covert_Communication_With_Random_Slots_and_Dispersed_Energy | [[2026-TIFS-Time-Hopping_Covert_Communication_With_Random_Slots_and_Dispersed_Energy]] | 0 | 0 |",
    "| 221 | unknown | comparative analysis of deep learning models for real world isp network traffic forecasting | 2026 | TNSM | Koumar | 2026-TNSM-Comparative_Analysis_of_Deep_Learning_Models_for_Real-World_ISP_Network_Traffic_Forecasting | [[2026-TNSM-Comparative_Analysis_of_Deep_Learning_Models_for_Real-World_ISP_Network_Traffic_Forecasting]] | 0 | 0 |",
    "| 237 | unknown | towards practical few shot multi tab website fingerprinting | 2026 | USENIX | Liu | 2026-USENIX-Towards_Practical_Few-shot_Multi-tab_Website_Fingerprinting | [[2026-USENIX-Towards_Practical_Few-shot_Multi-tab_Website_Fingerprinting]] | 1 | 0 |",
    "| 244 | unknown | conformal prediction for offensive security | 2026 | arXiv | Cherubin | 2026-arXiv-Conformal_Prediction_for_Offensive_Security | [[2026-arXiv-Conformal_Prediction_for_Offensive_Security]] | 0 | 1 |",
    "| NEW | unknown | advtg an adversarial trafic generation framework to deceive dlbased malicious trafic detection models | 2025 | WWW | unknown | 2025-WWW-AdvTG__An_Adversarial_Traffic_Generation_Framework_to_Deceive_DL-Based_Malicious_Traffic_Detection_Models | [[2025-WWW-AdvTG__An_Adversarial_Traffic_Generation_Framework_to_Deceive_DL-Based_Malicious_Traffic_Detection_Models]] | 0 | 0 |",
    "| NEW | unknown | do not trust what they tell exposing malicious accomplices in tor via anomalous circuit detection | 2025 | WWW | unknown | 2025-WWW-Do_Not_Trust_What_They_Tell__Exposing_Malicious_Accomplices_in_Tor_via_Anomalous_Circuit_Detection | [[2025-WWW-Do_Not_Trust_What_They_Tell__Exposing_Malicious_Accomplices_in_Tor_via_Anomalous_Circuit_Detection]] | 0 | 0 |",
    "| NEW | unknown | facing anomalies headon network trafic anomaly detection via uncertaintyinspired intersample diferences | 2025 | WWW | unknown | 2025-WWW-Facing_Anomalies_Head-On__Network_Traffic_Anomaly_Detection_via_Uncertainty_Inspired_Inter-Sample_Differences | [[2025-WWW-Facing_Anomalies_Head-On__Network_Traffic_Anomaly_Detection_via_Uncertainty_Inspired_Inter-Sample_Differences]] | 0 | 0 |",
    "| NEW | unknown | helios learning and adaptation of matching rules for continual innetwork malicious trafic detection | 2025 | WWW | unknown | 2025-WWW-Helios__Learning_and_Adaptation_of_Matching_Rules_for_Continual_In_Network_Malicious_Traffic_Detection | [[2025-WWW-Helios__Learning_and_Adaptation_of_Matching_Rules_for_Continual_In_Network_Malicious_Traffic_Detection]] | 0 | 0 |",
    "| NEW | unknown | odns clustering unveiling clientside dependency in open dns infrastructure | 2025 | WWW | unknown | 2025-WWW-ODNS_Clustering__Unveiling_Client-Side_Dependency_in_Open_DNS_Infrastructure | [[2025-WWW-ODNS_Clustering__Unveiling_Client-Side_Dependency_in_Open_DNS_Infrastructure]] | 0 | 0 |",
    "| NEW | unknown | mind the gap policy vs reality in postquantum tls deployment | 2026 | IMC | unknown | 2026-IMC-Mind_the_Gap__Policy_vs_Reality_in_Post-Quantum_TLS_Deployment | [[2026-IMC-Mind_the_Gap__Policy_vs_Reality_in_Post-Quantum_TLS_Deployment]] | 0 | 0 |",
    "| NEW | unknown | quantifying the privacy implications of highfidelity synthetic network trafic | 2026 | IMC | unknown | 2026-IMC-Quantifying_the_Privacy_Implications_of_High-Fidelity_Synthetic_Network_Traffic | [[2026-IMC-Quantifying_the_Privacy_Implications_of_High-Fidelity_Synthetic_Network_Traffic]] | 0 | 0 |",
    "| NEW | unknown | replicability challenging the myth of randomness paterns in encrypted trafic | 2026 | IMC | unknown | 2026-IMC-Replicability__Challenging_the_Myth_of_Randomness_Patterns_in_Encrypted_Traffic | [[2026-IMC-Replicability__Challenging_the_Myth_of_Randomness_Patterns_in_Encrypted_Traffic]] | 0 | 0 |",
    "| NEW | unknown | sagnn encrypted traffic classification with semanticaware heterogeneous graph neural network | 2026 | JCN | unknown | 2026-JCN-SaGNN__Encrypted_traffic_classification_with_semantic-aware_heterogeneous_graph_neural_network | [[2026-JCN-SaGNN__Encrypted_traffic_classification_with_semantic-aware_heterogeneous_graph_neural_network]] | 0 | 0 |",
    "| NEW | unknown | towards adaptive and robust website fingerprinting defense with multiagent deep reinforcement learning | 2026 | JCN | unknown | 2026-JCN-Towards_adaptive_and_robust_website_fingerprinting_defense_with_multi-agent_deep_reinforcement_learning | [[2026-JCN-Towards_adaptive_and_robust_website_fingerprinting_defense_with_multi-agent_deep_reinforcement_learning]] | 0 | 0 |",
    "| NEW | unknown | ganbased tor obfuscated traffic identification on imbalanced datasets | 2026 | JCS | unknown | 2026-JCS-GAN-based_Tor_obfuscated_traffic_identification_on_imbalanced_datasets | [[2026-JCS-GAN-based_Tor_obfuscated_traffic_identification_on_imbalanced_datasets]] | 0 | 0 |",
    "| NEW | unknown | packetpatch practical generation and deployment of adversarial packets for bytefeaturebased encrypted traffic classification | 2026 | JCS | unknown | 2026-JCS-PacketPatch__Practical_generation_and_deployment_of_adversarial_packets_for_byte-feature-based_encrypted_traffic_classification | [[2026-JCS-PacketPatch__Practical_generation_and_deployment_of_adversarial_packets_for_byte-feature-based_encrypted_traffic_classification]] | 0 | 0 |",
    "| NEW | unknown | uncovering robot jointlevel controller actions from encrypted network traffic empirical attacks and informationtheoretic bounds | 2026 | JCS | unknown | 2026-JCS-Uncovering_robot_joint-level_controller_actions_from_encrypted_network _traffic__Empirical_attacks_and_information-theoretic_bounds | [[2026-JCS-Uncovering_robot_joint-level_controller_actions_from_encrypted_network _traffic__Empirical_attacks_and_information-theoretic_bounds]] | 0 | 0 |",
    "| NEW | unknown | ultimate encrypted traffic feature engineering https encrypted traffic classification using restored application data unit length | 2026 | TDSC | unknown | 2026-TDSC-Ultimate_Encrypted_Traffic_Feature_Engineering_HTTPS_Encrypted_Traffic_Classification_Using_Restored_Application_Data_Unit_Length | [[2026-TDSC-Ultimate_Encrypted_Traffic_Feature_Engineering_HTTPS_Encrypted_Traffic_Classification_Using_Restored_Application_Data_Unit_Length]] | 0 | 0 |",
    "| NEW | unknown | robust and invisible flow watermarking with invertible neural network for traffic tracking | 2026 | TNSM | unknown | 2026-TNSM-Robust_and_Invisible_Flow_Watermarking_With_Invertible_Neural_Network_for_Traffic_Tracking | [[2026-TNSM-Robust_and_Invisible_Flow_Watermarking_With_Invertible_Neural_Network_for_Traffic_Tracking]] | 0 | 0 |",
    "| NEW | unknown | tunneleye an explainable framework for realtime detection of malicious doh traffic in highspeed backbone networks | 2026 | TNSM | unknown | 2026-TNSM-TunnelEye_An_Explainable_Framework_for_Real-Time_Detection_of_Malicious_DoH_Traffic_in_High-Speed_Backbone_Networks | [[2026-TNSM-TunnelEye_An_Explainable_Framework_for_Real-Time_Detection_of_Malicious_DoH_Traffic_in_High-Speed_Backbone_Networks]] | 0 | 0 |",
    "| NEW | unknown | eclipse atacks on ethereums peertopeer network | 2026 | WWW | unknown | 2026-WWW-Eclipse_Attacks_on_Ethereum’s_Peer-to-Peer_Network | [[2026-WWW-Eclipse_Attacks_on_Ethereum’s_Peer-to-Peer_Network]] | 0 | 0 |",
    "| NEW | unknown | forge a robust multitab website fingerprinting atack via blind source separation | 2026 | WWW | unknown | 2026-WWW-Forge__A_Robust_Multi-tab_Website_Fingerprinting_Attack_Via_Blind_Source_Separation | [[2026-WWW-Forge__A_Robust_Multi-tab_Website_Fingerprinting_Attack_Via_Blind_Source_Separation]] | 0 | 0 |",
    "| NEW | unknown | hifiwf toward realistic website fingerprinting with multitab and subpage recognition | 2026 | WWW | unknown | 2026-WWW-HiFi-WF__Toward_Realistic_Website_Fingerprinting_with_Multi-tab_and_Subpage_Recognition | [[2026-WWW-HiFi-WF__Toward_Realistic_Website_Fingerprinting_with_Multi-tab_and_Subpage_Recognition]] | 0 | 0 |",
    "| NEW | unknown | rofire robust website fingerprinting on realworld tor trafic via improved augmentation and normalization | 2026 | WWW | unknown | 2026-WWW-RoFiRe__Robust_Website_Fingerprinting_on_Real-World_Tor_Traffic_via_Improved_Augmentation_and_Normalization | [[2026-WWW-RoFiRe__Robust_Website_Fingerprinting_on_Real-World_Tor_Traffic_via_Improved_Augmentation_and_Normalization]] | 0 | 0 |",
    "| NEW | unknown | robust llmbased website fingerprinting under dynamic realworld conditions | 2026 | WWW | unknown | 2026-WWW-Robust_LLM-Based_Website_Fingerprinting_under_Dynamic_Real-World_Conditions | [[2026-WWW-Robust_LLM-Based_Website_Fingerprinting_under_Dynamic_Real-World_Conditions]] | 0 | 0 |",
    "| NEW | unknown | semfuzz a semanticsaware fuzzing framework for network protocol implementations | 2026 | WWW | unknown | 2026-WWW-SemFuzz__A_Semantics-Aware_Fuzzing_Framework_for_Network_Protocol_Implementations | [[2026-WWW-SemFuzz__A_Semantics-Aware_Fuzzing_Framework_for_Network_Protocol_Implementations]] | 0 | 0 |",
    "| NEW | unknown | tracking the stray sheep understanding dns response manipulation in the wild | 2026 | WWW | unknown | 2026-WWW-Tracking_the_Stray_Sheep__Understanding_DNS_Response_Manipulation_in_the_Wild | [[2026-WWW-Tracking_the_Stray_Sheep__Understanding_DNS_Response_Manipulation_in_the_Wild]] | 0 | 0 |",
    "| NEW | unknown | unveiling the underground phishing ecosystem a 12year longitudinal study of deep and dark web forums | 2026 | WWW | unknown | 2026-WWW-Unveiling_the_Underground_Phishing_Ecosystem__A_12-Year_Longitudinal_Study_of_Deep_and_Dark_Web_Forums | [[2026-WWW-Unveiling_the_Underground_Phishing_Ecosystem__A_12-Year_Longitudinal_Study_of_Deep_and_Dark_Web_Forums]] | 0 | 0 |",
    "| NEW | unknown | a priorityaware dualchannel feature fusion method for urban rail service trafic classification | 2026 | arXiv | unknown | 2026-arXiv-A_Priority-Aware_Dual-Channel_Feature_Fusion_Method_for_Urban_Rail_Service_Traffic_Classification | [[2026-arXiv-A_Priority-Aware_Dual-Channel_Feature_Fusion_Method_for_Urban_Rail_Service_Traffic_Classification]] | 0 | 0 |",
    "| NEW | unknown | despite instructions frontier agents improvise covert channels at test time | 2026 | arXiv | unknown | 2026-arXiv-Despite_Instructions__Frontier_Agents_Improvise_Covert_Channels_at_Test_Time | [[2026-arXiv-Despite_Instructions__Frontier_Agents_Improvise_Covert_Channels_at_Test_Time]] | 0 | 0 |",
    "| NEW | unknown | exact secondorder asymptotics for covert communication over dmcs with variational distance constraints | 2026 | arXiv | unknown | 2026-arXiv-Exact_Second-Order_Asymptotics_in_Covert_Communication_Over_Discrete_Memoryless_Channels | [[2026-arXiv-Exact_Second-Order_Asymptotics_in_Covert_Communication_Over_Discrete_Memoryless_Channels]] | 0 | 0 |",
    "| NEW | unknown | feedback coding enables inferencetime covert agentic communication | 2026 | arXiv | unknown | 2026-arXiv-Feedback_Coding_Enables_Inference-Time_Covert_Agentic_Communication | [[2026-arXiv-Feedback_Coding_Enables_Inference-Time_Covert_Agentic_Communication]] | 0 | 0 |",
    "| NEW | unknown | improving the reliability of anomaly detection for encrypted opc ua traffic over private 5g | 2026 | arXiv | unknown | 2026-arXiv-Improving_the_Reliability_of_Anomaly_Detection_for_Encrypted_OPC_UA_Traffic_over_Private_5G | [[2026-arXiv-Improving_the_Reliability_of_Anomaly_Detection_for_Encrypted_OPC_UA_Traffic_over_Private_5G]] | 0 | 0 |",
    "| NEW | unknown | multiplexing approaches to thermoradiative signatureless communications | 2026 | arXiv | unknown | 2026-arXiv-Multiplexing_approaches_to_thermoradiative_signatureless_communications | [[2026-arXiv-Multiplexing_approaches_to_thermoradiative_signatureless_communications]] | 0 | 0 |",
    "| NEW | unknown | robust transceiver design for simassisted integrated sensing and covert communications | 2026 | arXiv | unknown | 2026-arXiv-Robust_Transceiver_Design_for_SIM-Assisted_Integrated_Sensing_and_Covert_Communications | [[2026-arXiv-Robust_Transceiver_Design_for_SIM-Assisted_Integrated_Sensing_and_Covert_Communications]] | 0 | 0 |",
    "| NEW | unknown | secrets in radio waves towards practical and protocolagnostic phy information hiding | 2026 | arXiv | unknown | 2026-arXiv-Secrets_in_Radio_Waves__Towards_Practical_and_Protocol-Agnostic_PHY_Information_Hiding | [[2026-arXiv-Secrets_in_Radio_Waves__Towards_Practical_and_Protocol-Agnostic_PHY_Information_Hiding]] | 0 | 0 |",
    "| NEW | unknown | unknowntraffic detection calibration and shortcut reliance in distilled encryptedtraffic classifiers over one year | 2026 | arXiv | unknown | 2026-arXiv-Unknown-Traffic_Detection_Calibration_and_Shortcut_Reliance_in_Distilled_Encrypted-Traffic_Classifiers_over_One_Year | [[2026-arXiv-Unknown-Traffic_Detection_Calibration_and_Shortcut_Reliance_in_Distilled_Encrypted-Traffic_Classifiers_over_One_Year]] | 0 | 0 |",
    "| NEW | unknown | your model is leaking covert information transfer through llm residual streams | 2026 | arXiv | unknown | 2026-arXiv-Your_Model_Is_Leaking__Covert_Information_Transfer_through_LLM_Residual_Streams | [[2026-arXiv-Your_Model_Is_Leaking__Covert_Information_Transfer_through_LLM_Residual_Streams]] | 0 | 0 |",
    "| 332 | 10.1109/TIFS.2026.3723131 | two heads are better than one modelstomodel learning for encrypted traffic analysis | 2026 | TIFS | Jia Liu | 2026-TIFS-Two_Heads_Are_Better_Than_One__Models-to-Model_Learning_for_Encrypted_Traffic_Analysis | [[2026-TIFS-Two_Heads_Are_Better_Than_One__Models-to-Model_Learning_for_Encrypted_Traffic_Analysis]] | 0 | 0 |",
    "| 336 | 10.1109/TON.2026.3737411 | encrypted network traffic classification using generative and contrastive selfsupervised learning | 2026 | TON | Md. Shamim Towhid | 2026-TON-Encrypted_Network_Traffic_Classification_Using_Generative_and_Contrastive_Self-Supervised_Learning | [[2026-TON-Encrypted_Network_Traffic_Classification_Using_Generative_and_Contrastive_Self-Supervised_Learning]] | 0 | 0 |",
    "| 338 | 10.1109/TON.2026.3722338 | kanvis efficient and lightweight visual technique for network traffic classification using kolmogorovarnold network | 2026 | TON | Anurag Dutta | 2026-TON-KAN-Vis__Efficient_and_Lightweight_Visual_Technique_for_Network_Traffic_Classification_Using_KolmogorovArnold_Network | [[2026-TON-KAN-Vis__Efficient_and_Lightweight_Visual_Technique_for_Network_Traffic_Classification_Using_KolmogorovArnold_Network]] | 0 | 0 |",
    "| 339 | 10.1109/TON.2026.3710207 | making the best of both worlds universal perturbations for live blackbox evasion against nids in encrypted traffic | 2026 | TON | Hua Ding | 2026-TON-Making_the_Best_of_Both_Worlds__Universal_Perturbations_for_Live_Black-Box_Evasion_Against_NIDS_in_Encrypted_Traffic | [[2026-TON-Making_the_Best_of_Both_Worlds__Universal_Perturbations_for_Live_Black-Box_Evasion_Against_NIDS_in_Encrypted_Traffic]] | 0 | 0 |",
    "| 342 | 10.1109/TON.2026.3674624 | when pretraining meets contrast learning fewshot encrypted traffic classification with novelty detection | 2026 | TON | Lixin Zhao | 2026-TON-When_Pre-Training_Meets_Contrast_Learning__Few-Shot_Encrypted_Traffic_Classification_With_Novelty_Detection | [[2026-TON-When_Pre-Training_Meets_Contrast_Learning__Few-Shot_Encrypted_Traffic_Classification_With_Novelty_Detection]] | 0 | 0 |"
  ]
}
```

</details>

## 2026-11-20　现行笔记链接复核

- 处理 11 篇现行笔记中的 80 个失效链接。15 个改指可核的页面，其余保留原词。两篇身份修正笔记已用原文复核区统一链接，旧链接存档可查。

<details>
<summary>本次链接变更</summary>

```json
{
  "03-paper-notes/2026-arXiv-Treat_Traffic_Like_Trees__A_Semantic-Preserving_Hierarchical_Graph-Based_Expert_Framework_for_Encrypted_Traffic_Analysis.md": [
    {
      "old": "[[graph-attention-network]]",
      "new": "[[05-methods/graph-neural-network|graph-attention-network]]",
      "count": 1
    },
    {
      "old": "[[mixture-of-experts]]",
      "new": "mixture-of-experts",
      "count": 1
    }
  ],
  "03-paper-notes/2022-USENIX-Online_Website_Fingerprinting__Evaluating_Website_Fingerprinting_Attacks_on_Tor_in_the_Real_World.md": [
    {
      "old": "[[Triplet-Fingerprinting]]",
      "new": "Triplet-Fingerprinting",
      "count": 1
    },
    {
      "old": "[[Deep-Fingerprinting]]",
      "new": "[[03-paper-notes/2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning|Deep-Fingerprinting]]",
      "count": 1
    },
    {
      "old": "[[N-shot-learning]]",
      "new": "N-shot-learning",
      "count": 1
    },
    {
      "old": "[[online-learning]]",
      "new": "online-learning",
      "count": 1
    },
    {
      "old": "[[Tor-流量分析]]",
      "new": "[[04-concepts/anonymous-traffic-identification|Tor-流量分析]]",
      "count": 1
    },
    {
      "old": "[[匿名网络攻击]]",
      "new": "匿名网络攻击",
      "count": 1
    },
    {
      "old": "[[网站指纹防御]]",
      "new": "[[04-concepts/website-fingerprinting-defense|网站指纹防御]]",
      "count": 1
    }
  ],
  "03-paper-notes/2026-Access-Website_Fingerprinting_Techniques_Over_Tor_Network_A_Survey.md": [
    {
      "old": "[[网站指纹攻击]]",
      "new": "[[06-tasks/website-fingerprinting|网站指纹攻击]]",
      "count": 1
    },
    {
      "old": "[[加密流量分析]]",
      "new": "[[04-concepts/encrypted-traffic-analysis|加密流量分析]]",
      "count": 1
    },
    {
      "old": "[[网站指纹]]",
      "new": "[[04-concepts/website-fingerprinting|网站指纹]]",
      "count": 1
    },
    {
      "old": "[[流量分类]]",
      "new": "[[06-tasks/traffic-classification|流量分类]]",
      "count": 1
    }
  ],
  "03-paper-notes/2022-S&P-Surakav__Generating_Realistic_Traces_for_a_Strong_Website_Fingerprinting_Defense.md": [
    {
      "old": "[[generative-adversarial-network]]",
      "new": "generative-adversarial-network",
      "count": 1
    },
    {
      "old": "[[WGAN-div]]",
      "new": "WGAN-div",
      "count": 1
    },
    {
      "old": "[[burst-sequence-representation]]",
      "new": "burst-sequence-representation",
      "count": 1
    },
    {
      "old": "[[kernel-density-estimation]]",
      "new": "kernel-density-estimation",
      "count": 1
    },
    {
      "old": "[[traffic-anonymization]]",
      "new": "traffic-anonymization",
      "count": 1
    },
    {
      "old": "[[tor-privacy-protection]]",
      "new": "tor-privacy-protection",
      "count": 1
    },
    {
      "old": "[[survey-wf-defense]]",
      "new": "[[07-surveys/survey-website-fingerprinting|survey-wf-defense]]",
      "count": 1
    },
    {
      "old": "[[comparison-wf-defenses]]",
      "new": "comparison-wf-defenses",
      "count": 1
    },
    {
      "old": "[[comparison-defense-overhead]]",
      "new": "comparison-defense-overhead",
      "count": 1
    }
  ],
  "03-paper-notes/2025-JCN-Enhanced_detection_of_obfuscated_HTTPS_tunnel_traffic_using_heterogeneous_information_network.md": [
    {
      "old": "[[HTTPS 隧道]]",
      "new": "[[06-tasks/tunnel-detection|HTTPS 隧道]]",
      "count": 1
    },
    {
      "old": "[[异构信息网络]]",
      "new": "异构信息网络",
      "count": 1
    },
    {
      "old": "[[图注意力网络]]",
      "new": "[[05-methods/graph-neural-network|图注意力网络]]",
      "count": 1
    },
    {
      "old": "[[加密流量分析]]",
      "new": "[[04-concepts/encrypted-traffic-analysis|加密流量分析]]",
      "count": 1
    },
    {
      "old": "[[综述-加密流量分析]]",
      "new": "[[07-surveys/survey-encrypted-traffic-analysis|综述-加密流量分析]]",
      "count": 1
    },
    {
      "old": "[[对比表-隧道检测方法]]",
      "new": "对比表-隧道检测方法",
      "count": 1
    }
  ],
  "03-paper-notes/2026-arXiv-ResAware__Cross-Environment_Website_Fingerprinting_via_Resource-Privileged_Distillation.md": [
    {
      "old": "[[knowledge-distillation]]",
      "new": "knowledge-distillation",
      "count": 1
    },
    {
      "old": "[[privileged-information-learning]]",
      "new": "privileged-information-learning",
      "count": 1
    },
    {
      "old": "[[cross-modal-learning]]",
      "new": "cross-modal-learning",
      "count": 1
    },
    {
      "old": "[[cross-environment-generalization]]",
      "new": "cross-environment-generalization",
      "count": 1
    }
  ],
  "03-paper-notes/2026-NDSS-Cease_at_the_Ultimate_Goodness__Towards_Efficient_Website_Fingerprinting_Defense_via_Iterative_Mutual_Information_Minimization.md": [
    {
      "old": "[[mutual-information]]",
      "new": "mutual-information",
      "count": 1
    },
    {
      "old": "[[conditional-mutual-information]]",
      "new": "conditional-mutual-information",
      "count": 1
    },
    {
      "old": "[[reinforcement-learning]]",
      "new": "reinforcement-learning",
      "count": 1
    },
    {
      "old": "[[soft-actor-critic]]",
      "new": "soft-actor-critic",
      "count": 1
    },
    {
      "old": "[[tor-anonymity-network]]",
      "new": "tor-anonymity-network",
      "count": 1
    },
    {
      "old": "[[traffic-obfuscation]]",
      "new": "traffic-obfuscation",
      "count": 1
    },
    {
      "old": "[[adversarial-training]]",
      "new": "adversarial-training",
      "count": 1
    },
    {
      "old": "[[information-theory]]",
      "new": "information-theory",
      "count": 1
    },
    {
      "old": "[[CLUB-estimator]]",
      "new": "CLUB-estimator",
      "count": 1
    },
    {
      "old": "[[dynamic-feature-elimination]]",
      "new": "dynamic-feature-elimination",
      "count": 1
    },
    {
      "old": "[[iterative-dummy-packet-injection]]",
      "new": "iterative-dummy-packet-injection",
      "count": 1
    },
    {
      "old": "[[dirichlet-multinomial-sampling]]",
      "new": "dirichlet-multinomial-sampling",
      "count": 1
    },
    {
      "old": "[[deep-fingerprinting-attack]]",
      "new": "[[03-paper-notes/2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning|deep-fingerprinting-attack]]",
      "count": 1
    },
    {
      "old": "[[robust-fingerprinting-attack]]",
      "new": "robust-fingerprinting-attack",
      "count": 1
    },
    {
      "old": "[[tor-traffic-protection]]",
      "new": "tor-traffic-protection",
      "count": 1
    },
    {
      "old": "[[privacy-preserving-traffic-analysis]]",
      "new": "privacy-preserving-traffic-analysis",
      "count": 1
    }
  ],
  "03-paper-notes/2026-NDSS-Lightening_the_Load__A_Cluster-Based_Framework_or_A_Lower-Overhead__Provable_Website_Fingerprinting_Defense.md": [
    {
      "old": "[[k-anonymity]]",
      "new": "k-anonymity",
      "count": 1
    },
    {
      "old": "[[l-diversity]]",
      "new": "l-diversity",
      "count": 1
    },
    {
      "old": "[[CAST-clustering]]",
      "new": "CAST-clustering",
      "count": 1
    },
    {
      "old": "[[ECDIRE]]",
      "new": "ECDIRE",
      "count": 1
    },
    {
      "old": "[[Holmes]]",
      "new": "Holmes",
      "count": 1
    },
    {
      "old": "[[k-fingerprinting]]",
      "new": "k-fingerprinting",
      "count": 1
    }
  ],
  "03-paper-notes/2024-TON-Website_Fingerprinting_on_Encrypted_Proxies__A_Flow-Context-Aware_Approach_and_Countermeasures.md": [
    {
      "old": "[[training-testing-asymmetry]]",
      "new": "training-testing-asymmetry",
      "count": 1
    },
    {
      "old": "[[flow-correlation]]",
      "new": "flow-correlation",
      "count": 1
    },
    {
      "old": "[[random-forest]]",
      "new": "random-forest",
      "count": 1
    },
    {
      "old": "[[DBSCAN]]",
      "new": "DBSCAN",
      "count": 1
    },
    {
      "old": "[[longest-common-subsequence]]",
      "new": "longest-common-subsequence",
      "count": 1
    },
    {
      "old": "[[CNN-traffic-classification]]",
      "new": "[[05-methods/convolutional-network|CNN-traffic-classification]]",
      "count": 1
    },
    {
      "old": "[[encrypted-proxy-traffic-analysis]]",
      "new": "encrypted-proxy-traffic-analysis",
      "count": 1
    },
    {
      "old": "[[traffic-analysis-attack]]",
      "new": "traffic-analysis-attack",
      "count": 1
    }
  ],
  "03-paper-notes/2026-JCN-A_simulation-based_unified_framework_for_real-time_malicious_traffic_detection_in_multi-environment_networks.md": [
    {
      "old": "[[多环境网络]]",
      "new": "多环境网络",
      "count": 1
    },
    {
      "old": "[[迁移学习]]",
      "new": "迁移学习",
      "count": 1
    },
    {
      "old": "[[特征选择]]",
      "new": "特征选择",
      "count": 1
    },
    {
      "old": "[[入侵检测]]",
      "new": "入侵检测",
      "count": 1
    },
    {
      "old": "[[综述-入侵检测]]",
      "new": "综述-入侵检测",
      "count": 1
    },
    {
      "old": "[[对比表-实时入侵检测系统]]",
      "new": "对比表-实时入侵检测系统",
      "count": 1
    }
  ],
  "03-paper-notes/2026-NDSS-Huma__Censorship_Circumvention_via_Web_Protocol_Tunneling_with_Deferred_Traffic_Replacement.md": [
    {
      "old": "[[web-protocol-tunneling]]",
      "new": "web-protocol-tunneling",
      "count": 1
    },
    {
      "old": "[[traffic-fingerprinting]]",
      "new": "traffic-fingerprinting",
      "count": 1
    },
    {
      "old": "[[behavioral-realism]]",
      "new": "behavioral-realism",
      "count": 1
    },
    {
      "old": "[[content-replacement]]",
      "new": "content-replacement",
      "count": 1
    },
    {
      "old": "[[deferred-processing]]",
      "new": "deferred-processing",
      "count": 1
    },
    {
      "old": "[[covert-communication]]",
      "new": "covert-communication",
      "count": 1
    },
    {
      "old": "[[censorship-evasion]]",
      "new": "censorship-evasion",
      "count": 1
    },
    {
      "old": "[[privacy-protection]]",
      "new": "privacy-protection",
      "count": 1
    },
    {
      "old": "[[traffic-analysis-resistance]]",
      "new": "traffic-analysis-resistance",
      "count": 1
    },
    {
      "old": "[[survey-censorship-circumvention]]",
      "new": "survey-censorship-circumvention",
      "count": 1
    },
    {
      "old": "[[comparison-censorship-circumvention-tools]]",
      "new": "comparison-censorship-circumvention-tools",
      "count": 1
    },
    {
      "old": "[[comparison-traffic-analysis-defenses]]",
      "new": "comparison-traffic-analysis-defenses",
      "count": 1
    }
  ]
}
```

</details>

## 2026-11-20　全库结构与论文笔记补齐

- 有效注册的 355 篇标准论文逐一匹配笔记、PDF、解析稿与引文记录。另有一份 COSINT 报告。1 份未注册 TrafficSliver 旧笔记保留，已标出当前文献入口。
- 30 篇旧自动入库笔记依据原文补齐现行摘要、方法、结果、定位和适用条件。其中 21 篇原为 L2，9 篇原为 L3。旧自动摘录可追溯。
- 另补齐 78 篇笔记中的 125 个中文题名、方向、任务、方法或研究对象字段。理论论文和纯仿真按实际研究对象登记。阅读等级沿用实际入库记录。
- 四篇论文的 DOI 同步至去重注册表，两篇引文补齐 BibTeX 的 DOI。Tracegram 以 USENIX 论文页面登记，Zenodo 标识保留在产物字段。
- 355 篇的 DOI 在笔记、注册表和两种引文格式之间一致。67 篇仍按 `unknown` 或空 DOI 记录，已确认的官方入口按原题录保留。
- 101 项已登记公开产物均有对应笔记及记录。图库当前引用的 554 张图均能找到本地图像，另归档 5 张图。
- 三类模拟入库均可登记待审核证据，重复提交无重复记录。正式前沿、命题索引和真实账本在模拟前后字节一致。

### 本轮另行修订的旧注册行

```markdown
| 123 | unknown | crossenvironmental website fingerprinting | 2025 | INFOCOM | Li | 2025-INFOCOM-Cross-Environmental_Website_Fingerprinting | [[2025-INFOCOM-Cross-Environmental_Website_Fingerprinting]] | 0 | 0 |
| 238 | 10.5281/zenodo.17978903 | tracegram framing trace level traffic analysis with temporally aware multiple instance learning | 2026 | USENIX | Qu | 2026-USENIX-Tracegram__Framing_Trace-Level_Traffic_Analysis_with_Temporally-Aware_Multiple_Instance_Learning | [[2026-USENIX-Tracegram__Framing_Trace-Level_Traffic_Analysis_with_Temporally-Aware_Multiple_Instance_Learning]] | 3 | 0 |
| NEW | unknown | cardinality is not enough super host detection via segmented cardinality estimation | 2026 | WWW | unknown | 2026-WWW-Cardinality_is_Not_Enough__Super_Host_Detection_via_Segmented_Cardinality_Estimation | [[2026-WWW-Cardinality_is_Not_Enough__Super_Host_Detection_via_Segmented_Cardinality_Estimation]] | 0 | 0 |
| NEW | unknown | jittersketch finding jittery flows in network streams | 2026 | WWW | unknown | 2026-WWW-JitterSketch__Finding_Jittery_Flows_in_Network_Streams | [[2026-WWW-JitterSketch__Finding_Jittery_Flows_in_Network_Streams]] | 0 | 0 |
| NEW | unknown | zeroshot forecasting of network dynamics through weight flow matching | 2026 | WWW | unknown | 2026-WWW-Zero-Shot_Forecasting_of_Network_Dynamics_through_Weight_Flow_Matching | [[2026-WWW-Zero-Shot_Forecasting_of_Network_Dynamics_through_Weight_Flow_Matching]] | 0 | 0 |
```

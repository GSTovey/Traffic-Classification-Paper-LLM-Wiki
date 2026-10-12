---
type: paper
title_original: "HiFi-WF: Toward Realistic Website Fingerprinting with Multi-tab and Subpage Recognition"
title_cn: "HiFi-WF：面向多标签页与子页面识别的真实网站指纹攻击"
authors: ["Songyang Wu", "Long Yuan", "Chuan Ma", "Biwen Chen", "Tao Xiang", "Ming Ding", "Yuwen Qian"]
year: 2026
venue: "ACM Web Conference 2026 (WWW'26)"
doi: unknown
url: "https://doi.org/10.1145/3774904.3792412"
pdf: "00-inbox/PDFs/2026-WWW-HiFi-WF__Toward_Realistic_Website_Fingerprinting_with_Multi-tab_and_Subpage_Recognition.pdf"
mineru_md: "02-parsed-markdown/2026-WWW-HiFi-WF__Toward_Realistic_Website_Fingerprinting_with_Multi-tab_and_Subpage_Recognition.md"
status: deep-analyzed
reading_level: L3
research_area: ["website-fingerprinting", "encrypted-traffic-analysis", "Tor traffic analysis"]
task: ["hierarchical multi-label WF", "multi-tab website identification", "subpage recognition"]
method: ["two-row direction representation", "CNN feature extractor", "dual attention", "cross-attention hierarchy", "hierarchical focal loss"]
dataset: ["Chrome homepage/subpage 50-site dataset", "MP-SA/SP-MA multi-tab dataset", "open-world 12K-site dataset", "Tor 2,500-instance dataset"]
code: "https://github.com/wusongyang02-blip/HiFi-WF"
relevance: medium
created: "2026-09-29"
updated: "2026-10-10"
---

# HiFi-WF: Toward Realistic Website Fingerprinting with Multi-tab and Subpage Recognition

> **L3 深度分析笔记**：基于正文 §1–§5、Tables 1–6、Figures 1–3、5、附录 A–E 与开源说明交叉核对。本文将“网站主页”和“具体子页面”作为层级标签联合识别；子页面级结果的隐私风险与数据集构造边界需和主页级 F1 分开解释。

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | HiFi-WF: Toward Realistic Website Fingerprinting with Multi-tab and Subpage Recognition |
| 中文标题 | HiFi-WF：面向多标签页与子页面识别的真实网站指纹攻击 |
| 作者 | Songyang Wu、Long Yuan、Chuan Ma、Biwen Chen、Tao Xiang、Ming Ding、Yuwen Qian |
| 年份 | 2026 |
| 会议/期刊 | ACM Web Conference 2026 (WWW'26) |
| 研究方向 | 多标签页网站指纹、主页/子页面层级识别、Tor 流量分析 |
| 任务类型 | 层级多标签分类、网站识别、子页面识别、开放世界拒识与防御评估 |
| 方法关键词 | 两行方向矩阵、CNN extractor、channel/spatial attention、dual-path segmentation、multi-head cross-attention、Enhanced SubHead、Hierarchical Focal Loss |
| 数据与规模 | 50 个 monitored websites、每站 10 个子页面；Chrome 主页/子页面、多标签 MP-SA/SP-MA、12K open-world、Tor 2,500 条样本 |
| 是否开源 | 是：https://github.com/wusongyang02-blip/HiFi-WF |
| DOI | 10.1145/3774904.3792412 |
| PDF | 00-inbox/PDFs/2026-WWW-HiFi-WF__Toward_Realistic_Website_Fingerprinting_with_Multi-tab_and_Subpage_Recognition.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-WWW-HiFi-WF__Toward_Realistic_Website_Fingerprinting_with_Multi-tab_and_Subpage_Recognition.md |

## 1. 一句话总结
> HiFi-WF 将主页识别与子页面识别统一为层级多标签 WF：两行方向输入保留上/下行包大小和时序，特征处理器与双路径交互学习主页/子页面依赖，Enhanced SubHead 用父标签约束子页面预测，在 2-tab 场景达到主页 F1=92.1%、子页面 F1=81.9%。

## 2. 摘要原文
Website Fingerprinting (WF) is an emerging trafic analysis technique that enables a passive adversary to infer which websites a user visits. However, most existing studies, whether in single tab or multi-tab settings, rely on the unrealistic assumption that users only access website homepages, diverging significantly from real-world browsing behavior. Even recent works extending WF to subpages primarily focus on website-level identification, with out distinguishing which specific subpages are visited, thereby limiting the attack’s granularity and scope. In this paper, we propose HiFi-WF (Hierarchical Fine-grained Website Fingerprinting), a novel framework that breaks the homepage-only assumption and extends WF to multi-tab recognition and fine-grained subpage identification. We formulate the task as a hierarchical multi-label classification problem, jointly modeling the distinctions and correlations between homepages and subpages. To this end, HiFi-WF integrates a unified CNN-based extractor and layered encoder with a Feature Interaction Module based on multi-head cross-attention to capture inter-level dependencies. An Enhanced SubHead enforces hierarchical constraints to suppress invalid subpage predictions, while a cascaded channel–spatial attention mechanism refines discriminative features for precise hierarchical identification. Experi mental results demonstrate that HiFi-WF achieves state-of-the-art performance at both hierarchical levels, attaining F1-scores of 92.1% (homepage) and 81.9% (subpage), thereby validating its efective ness in advancing WF attacks toward realistic, fine-grained, and multi-tab browsing scenarios. Related codes and datasets can be found in https://github.com/wusongyang02-blip/HiFi-WF.

## 3. 方法分析

### 3.1 研究问题与核心假设

现有 WF 通常把 homepage 当作 website 代表，忽略同一站点子页面在内容、路径和加载结构上的差异；在多 tab 混合下，这种平均化表示既降低网站识别，也无法判断具体页面。HiFi-WF 的假设是：主页与子页面共享父子结构，联合建模其层级依赖比两个相互独立的分类器更适合稀疏和不平衡的子页面标签。

### 3.2 输入—处理—输出

| 步骤 | 输入 | 处理 | 输出 |
|---|---|---|---|
| Two-row preprocessing | 加密流量包大小、方向、时间顺序 | 上行包放第一行，下行放第二行；无包方向填 0，保留精确单包时序 | 2×T 方向矩阵 |
| Feature Processor | 2×T 矩阵 | CNN extractor 学方向/局部模式；channel/spatial dual attention 强化显著特征 | 细粒度特征图 |
| Dual-Path Segmentation | 特征图 | 软分成 homepage-oriented 与 subpage-oriented 两路 | F_main、F_sub |
| Hierarchical Feature Interaction | 两路特征 | multi-head cross-attention 让主页和子页面双向交换信息 | 互增强层级表示 |
| Dual-Path Classifier | 互增强表示 | homepage 双路径分类；Enhanced SubHead 注入父标签并用动态约束 mask 抑制非法子页面 | homepage/subpage 多标签概率 |
| Hierarchical Focal Loss | 主/子标签与稀疏正样本 | 统一训练基线与 HiFi-WF，兼顾层级一致性和类别不平衡 | 层级联合优化 |

## 4. 实验表现

- **数据集**：50 个 monitored websites，每站 10 个直接可达子页面；Chrome 数据含 MP-SA 2-tab 10,000 条、SP-MA 2-tab 10,000 条和 3-tab 5,000 条；open-world 从 Tranco Top-50,000 选 12,000 个未监控网站；Tor 数据 2,500 条。
- **基线**：Multi-DF、Multi-VarCNN、Multi-RF（由 DF/Var-CNN/RF 改造成多标签）、BAPM、ARES、TMWF；统一替换为 dual-head 主页/子页面分类器并使用 Hierarchical Focal Loss。
- **指标**：Precision、Recall、F1、P@K、MAP@K；开放世界另报告 AUC_M、AUC_N。

### 4.1 关键结果

| 场景 | Homepage | Subpage | 位置 |
|---|---:|---:|---|
| Chrome 2-tab | F1=0.915，P@2=0.915，MAP@2=0.913 | F1=0.819，P@2=0.810，MAP@2=0.791 | Table 2 |
| Chrome 3-tab | F1=0.757 | F1=0.706 | Table 2 |
| Tor multi-tab | F1=0.538 | F1=0.401 | Table 3 |
| Open-world 2-tab | MAP@2=0.906，AUC_M/AUC_N=0.997/0.997 | MAP@2=0.708 | Table 4 |
| Defenses Random/WTF-PAD/Front | homepage F1=0.852/0.773/0.718 | subpage F1=0.755/0.652/0.549 | Table 5 |

论文摘要中的 92.1%/81.9%对应正文表格/四舍五入口径；引用时保留场景和指标。

## 5. 局限性与复现建议
- 主页/子页面数据来自作者选择的 50 个网站和每站 10 个子页面，内容更新、子页面深度与站点规模覆盖有限。
- Chrome 与 Tor 数据分开收集；Tor 仅 2,500 条样本，Tor 结果明显低于 Chrome，不能直接外推到所有匿名网络部署。
- open-world 把未监控网站作为未知类，AUC_M/AUC_N 高不能说明攻击者可以区分每个未知站点。
- 两行表示保留精确单包时序，可能在防御插包/真实网络抖动下更敏感；论文只测 Random、WTF-PAD、Front，未覆盖所有整形防御。
- 复现需下载作者 GitHub 与数据集，固定 50 站点/10 子页采集规则、2/3-tab 连续访问顺序、层级标签和统一 Hierarchical Focal Loss。

## 6. 知识链接
- [[website-fingerprinting]]
- [[encrypted-traffic-analysis]]
- [[traffic-classification]]

## 7. 证据状态
- 正文证据已核对至 §1–§5、Tables 1–6、Figures 1–3/5 与附录 A–E。
- DOI 为 10.1145/3774904.3792412；代码和数据链接为 https://github.com/wusongyang02-blip/HiFi-WF。
- MinerU 存在重复小节标题与表格合并单元格；主页和子页面指标已按正文 Table 2–5 分开记录。



## 8. 详细方法与机制

### 8.1 两行方向表示与特征处理

HiFi-WF 将按时间排列的包大小写为 2×T 矩阵：第一行是 outgoing，第二行是 incoming；某时刻无该方向包则填零，避免把上/下行方向编码到一个带符号数。相比按时间 bin 聚合的 TAM，这一表示保留单包大小和时序细节，但也减少了聚合带来的噪声鲁棒性。CNN extractor 在双通道上提取局部模式，级联 channel/spatial attention 强化“哪些特征”和“哪些时间位置”更有辨识力。

### 8.2 双路径层级交互

Dual-Path Segmentation 用轻量网络和 softmax 权重把共享特征软分为 homepage-oriented 与 subpage-oriented 两路，而非硬切分。Feature Interaction Module 用多头 cross-attention 让两路互为 query/key/value，主页线索可帮助子页面消除站点内相似性，子页面线索也可反向补充主页识别。Dual-Path Classifier 对主页采用互增强表示；对子页面额外注入主页预测，并由动态 constraint mask 屏蔽不属于预测父网站的子标签。

### 8.3 Hierarchical Focal Loss

作者将多标签 focal loss 扩展为层级目标，使主页和子页面的正样本稀疏、类别不平衡与父子一致性同时进入训练。为公平比较，所有 baseline 的分类头也改为主/子双头并使用相同损失；因此结果反映架构差异和层级建模差异，而非单纯损失函数差异。

## 9. 学习与应用

### 9.1 是否开源？

代码和数据链接由作者在摘要和项目页给出：https://github.com/wusongyang02-blip/HiFi-WF。复现需要按附录采集主页—子页面连续访问序列，保留 Chrome/Tor 环境和层级标签；代码公开不等于原始网站流量可自由再分发。

### 9.2 复现关键步骤

1. 从 Top 200 选 50 个 monitored sites，每站选 10 个直接可达子页面，建立 main/sub label 映射。
2. 采集主页→子页面连续导航的 Chrome 轨迹，构造 MP-SA、SP-MA 2-tab/3-tab 和 12K open-world 数据。
3. 对每条 trace 生成两行方向矩阵，训练 CNN/dual attention、dual-path segmentation、cross-attention 和 Enhanced SubHead。
4. 用统一 Hierarchical Focal Loss 重训 Multi-DF、Multi-VarCNN、Multi-RF、BAPM、ARES、TMWF。
5. 分别评估 homepage/subpage 的 F1、P@K、MAP@K、open-world AUC_M/AUC_N，并在 Random/WTF-PAD/Front 下复测。

### 9.3 能否迁移到其他任务？

层级父子标签和 cross-attention 可以迁移到应用—功能、站点—路径或协议—子协议的多层流量识别。两行方向表示也可用于其他双向加密流量，但其精细时序对 padding、重排和采集时钟较敏感；动态父标签约束需要任务拥有可靠的层级本体。

### 9.4 对我的研究有什么启发？

HiFi-WF 将“更细粒度标签”与“更高隐私风险”同时写入问题定义，并用 parent constraint 把层级一致性变成模型结构。对流量分析研究，不能只报告网站级平均 F1；子页面/功能级识别应单独建标签、单独评估，并说明 open-world unknown 的合并口径。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| homepage-only 假设导致子页面泛化明显下降，RF 约下降 35% | 主页训练、主页/子页面测试对比 | §1, Fig. 1 |
| 主页与子页面建模为层级多标签任务 | 问题定义和贡献 | §1, §2.1 |
| 两行上/下行输入保留单包时序 | Data preprocess | §3.2 |
| 主页/子页面双路径和 cross-attention 互增强 | HiFi-WF architecture | §3.3, Fig. 3 |
| 2-tab homepage F1=0.915、subpage F1=0.819 | Table 2 | §4.4, Table 2 |
| 3-tab homepage/subpage F1=0.757/0.706 | Table 2 | §4.4, Table 2 |
| Tor 数据 homepage/subpage F1=0.538/0.401 | Table 3 | §4.4, Table 3 |
| open-world 2-tab AUC_M/AUC_N=0.997/0.997，MAP@2 homepage/subpage=0.906/0.708 | Table 4 | §4.5, Table 4 |
| Random/WTF-PAD/Front 下 subpage F1=0.755/0.652/0.549 | Table 5 | §4.6, Table 5 |
| 去掉 Feature Enhancer/HFI/Enhanced SubHead 后 homepage F1=0.841/0.866/0.905 | Table 6 | §4.7, Table 6 |
| 代码与数据公开 | 摘要/Availability | §1 |

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-WWW-HiFi-WF__Toward_Realistic_Website_Fingerprinting_with_Multi-tab_and_Subpage_Recognition.pdf
- MinerU Markdown：02-parsed-markdown/2026-WWW-HiFi-WF__Toward_Realistic_Website_Fingerprinting_with_Multi-tab_and_Subpage_Recognition.md
- DOI：https://doi.org/10.1145/3774904.3792412
- 代码：https://github.com/wusongyang02-blip/HiFi-WF

## 12. 后续问题

1. 50 个站点、每站 10 个子页面能否代表长尾网站结构与深层 URL，跨日期内容漂移如何影响层级标签？
2. 两行精确时序表示在更强 padding、Tor circuit 变化和网络重排下是否比 TAM 更脆弱？
3. Enhanced SubHead 的 parent mask 在父网站预测错误时是否会级联压制正确子页面？
4. open-world unknown 合并为一类时的 AUC 是否掩盖了不同未知站点之间的误报差异？
5. 子页面识别对防御方意味着更高隐私风险；能否设计针对层级关系的 selective padding 而不显著增加开销？

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

论文先指出 WF 研究的 homepage-only 假设与真实导航脱节，再用主页训练/子页面测试实验证明现有 DF、Var-CNN、RF 的泛化断裂。转折点是把 website 作为父标签、subpage 作为子标签，正式改写为层级多标签任务。方法沿“精确输入→特征增强→主页/子页面软分→交叉交互→父标签约束”展开，实验则依次覆盖 2/3-tab、Tor、open-world、防御和消融。最终结论不仅是 F1 提升，也是 WF 的可观测粒度从站点扩展到具体用户兴趣与意图，同时把更高的隐私风险写入 future work。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 角色 | 关键转折 |
|---|---|---|---|
| Introduction | 建立 homepage-only 与现实浏览的错配 | 问题框定 | 子页面是独立隐私目标 |
| Threat Model | 明确本地被动监听者和主页/子页面目标 | 威胁锚定 | 从网站级扩展页面级 |
| Methodology | 两行表示、双路径、交叉注意力、SubHead | 方法主体 | 层级关系进入模型内部 |
| Dataset/Evaluation | Chrome/Tor、2/3-tab、open-world、defense | 真实性兑现 | 40K+ 层级样本支持比较 |
| Ablation/Conclusion | 解释模块贡献并承认防御缺口 | 边界收束 | 细粒度提升伴随检测风险 |

### 13.3 Gap 展开方式

| Gap | 具体内容 | 论证方式 |
|---|---|---|
| 场景缺口 | 主页不能代表真实网页导航 | 主页/子页面跨域测试与 50 站点数据 |
| 粒度缺口 | 既有子页面工作仍只输出 website label | 层级 multi-label、subpage F1 |
| 结构缺口 | 主页和子页面相关性未被显式建模 | cross-attention 和 parent constraint |
| 评估缺口 | 单 tab/理想数据掩盖多 tab、Tor 和防御影响 | MP-SA/SP-MA、open-world、Tor、defense 组合 |

### 13.4 实验叙事方式

| 环节 | 作用 |
|---|---|
| 主页训练/子页面测试 | 证明旧方法的场景外泛化缺陷 |
| 2/3-tab 层级识别 | 证明联合主页与子页面标签可行 |
| Tor 数据 | 检查匿名网络迁移 |
| Open-world | 检查监控/未知站点拒识与细粒度 MAP |
| 防御与消融 | 量化细粒度表示的鲁棒性成本和模块贡献 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移写法 |
|---|---|---|
| 场景动机 | 用用户真实导航和隐私后果驱动模型设计 | 先证明简化场景会改变任务，再给真实任务定义 |
| 标签组织 | 父网站/子页面对应父子输出 | 让标签层级直接约束架构和损失 |
| 结果解释 | 承认 3-tab/Tor 与防御下性能下降 | 以多场景曲线说明泛化边界，而不是只报最佳点 |
| 风险表达 | 明确子页面可推断兴趣和意图 | 对更细粒度攻击同时报告隐私后果与防御需求 |

## 14. 证据边界与复现清单

1. **层级标签边界**：subpage 是作者从 50 个站点中选取的 10 个直接可达页面，不代表任意深层页面或完整网站层级。
2. **数据划分边界**：open-world 训练包含 70% SP-MA 2-tab 与 30% open-world 数据；AUC_M/AUC_N 的高值依赖这一划分，不能当成完全零样本未知站点性能。
3. **模型边界**：两行矩阵保留单包时序，精细特征可能解释 clean 数据优势，也可能解释防御下的性能下降；论文只评估 Random/WTF-PAD/Front。
4. **跨环境边界**：Chrome 与 Tor 分开采集，Tor 样本少且 F1 明显下降；跨浏览器、跨日期和更广泛网络条件留给 future work。
5. **指标边界**：homepage F1=92.1% 和 subpage F1=81.9% 是摘要/2-tab 口径；3-tab、Tor、open-world 和 defenses 的指标需按表格单独引用。
6. **复现依赖**：GitHub 代码、50×10 页面选择、连续导航、两行预处理、Hierarchical Focal Loss、动态 mask 与数据采集环境必须一起记录。

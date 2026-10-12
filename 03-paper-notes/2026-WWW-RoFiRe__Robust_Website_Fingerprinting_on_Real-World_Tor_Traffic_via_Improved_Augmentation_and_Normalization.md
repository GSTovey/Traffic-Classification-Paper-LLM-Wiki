---
type: paper
title_original: "RoFiRe: Robust Website Fingerprinting on Real-World Tor Trafic via Improved Augmentation and Normalization"
title_cn: ""
authors: []
year: 2026
venue: WWW
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-WWW-RoFiRe__Robust_Website_Fingerprinting_on_Real-World_Tor_Traffic_via_Improved_Augmentation_and_Normalization.pdf"
mineru_md: "02-parsed-markdown/2026-WWW-RoFiRe__Robust_Website_Fingerprinting_on_Real-World_Tor_Traffic_via_Improved_Augmentation_and_Normalization.md"
status: deep-analyzed
reading_level: L3
research_area: []
task: []
method: []
dataset: []
code: unknown
relevance: medium
created: "2026-09-29"
updated: "2026-10-10"
---

# RoFiRe: Robust Website Fingerprinting on Real-World Tor Trafic via Improved Augmentation and Normalization

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | RoFiRe: Robust Website Fingerprinting on Real-World Tor Trafic via Improved Augmentation and Normalization |
| 年份 | 2026 |
| 会议/期刊 | WWW |
| PDF | [[2026-WWW-RoFiRe__Robust_Website_Fingerprinting_on_Real-World_Tor_Traffic_via_Improved_Augmentation_and_Normalization.pdf]] |
| MinerU Markdown | [[2026-WWW-RoFiRe__Robust_Website_Fingerprinting_on_Real-World_Tor_Traffic_via_Improved_Augmentation_and_Normalization.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
论文未明确提取摘要。

## 3. 方法分析
- 输入：论文所研究的网络流量、协议、系统或安全数据（以全文为准）。
- 处理：论文提出的方法或分析流程（摘要级自动提取，待核验）。
- 输出：分类、检测、预测、攻击/防御或系统验证结果。

## 4. 实验表现
- 数据集：待从全文核验。
- Baseline：unknown。
- 指标与数值：不补造，待表格核验。

## 5. 局限性与复现建议
- 当前笔记完成自动入库和摘要级分析，未替代人工深读。
- 先核验数据来源、代码状态、划分和指标，再决定复现等级。

## 6. 知识链接
- [[traffic-classification]]
- [[encrypted-traffic-analysis]]

## 7. 证据状态
- MinerU：已完成；解析质量需人工抽查。
- Bib 元数据：待官方 API/论文首页核验。


## 深度分析（自动证据提取，需人工复核）

### 研究问题与证据
- 主题线索：website fingerprint, tor, transformer。
- 摘要证据：MinerU 未稳定提取摘要，不能据此补写贡献。

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：未检测到明确 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。

## 深度分析（2026-09-29）

- reading_level: L3
- 研究定位：真实Tor WF/增强归一化
- 方法机制：RoFiRe面向真实世界Tor流量，通过改进数据增强与归一化提高跨环境鲁棒性；需要从正文确认增强算子、归一化位置和真实采集协议。
- 输入—处理—输出：输入真实Tor流量序列；增强/归一化后进行网站指纹分类。
- 证据边界：当前摘要未可靠抽取定量结果，数据采集、时间漂移、基线和代码均待核验。
- 联动标签：website-fingerprinting；DNS；anomaly-detection；traffic-security

## 深度方法分析（2026-10-09）

> 本节依据本地 MinerU 原文 §1–§8、表 1–4、图 2–7 及附录 A.3–A.7 整理。论文研究的是 Tor 网站指纹攻击的模型鲁棒性；GTT23 的 exit-side 训练/测试结果用于隔离分类器能力，不能直接等同于 entry-side 部署效果。

### 1. 研究问题与边界

RoFiRe 关注两个相互关联的问题：合成或实验室数据上接近饱和的 WF 精度，是否能迁移到真实 Tor exit 流量；在真实流量稀疏、高方差和时间漂移下，少量每站点样本能否训练出稳定的指纹分类器。威胁模型是被动观察者在 Tor 入口侧观察加密 cell 的方向、时间和长度特征，但论文用 GTT23 的真实 exit trace 训练和评测，以获得不含网络转导混杂因素的分类器上界。实验同时覆盖 closed-world（固定监测站点多类分类）、concept drift（训练与测试跨周）和 open-world（监测/非监测二元判别，含真实 base rate）。

### 2. 输入、处理与输出

- **输入与数据特征**：GTT23 真实 Tor exit cell trace；相较 BigEnough，GTT23 的中位持续时间为 62.57 s、有效 cell 数 72、burst 数 9，而 BigEnough 分别为 16.21 s、680 和 47。GTT23 中 57% 的 trace 少于 50 cells，29% 超过 100 s；按 cell count 的 F-ratio 为 0.728，按 duration 仅 0.012，均低于合成数据。
- **DyWin 增强**：对总 cell 数为 (C_t) 的 trace 划分 (N_w) 个非重叠窗口，窗口大小 (C_w=max(2,lfloor C_t/N_w
floor))。每个窗口以概率 ((\alpha/2,\alpha/2,1-\alpha)) 选择 Mask Window、Jitter Window 或 NONE；jitter 的时间偏移 (delta\sim U(0.2,1.0))。Mask 删除当前窗口；Jitter 将窗口保留并复制一份、把其中 cell 时间戳加上 (delta)；NONE 保持原样。默认 (N_w=9)，(alpha=0.1)（AWF/DF）或 0.3（BigEnough/GTT23）。论文排除 (C_t\le 44) 的 trace 以避免不稳定扰动。
- **RoFiRe 分类器**：五个卷积 block、每个 block 内两层 Conv1D；在卷积前使用 RMSNorm 和 pre-normalization，随后两个全连接层输出站点类别。RMSNorm 只按输入向量的均方根缩放并学习增益，不做均值减法；pre-norm 采用 (F(Norm(x_l))+x_l) 的残差形式以改善梯度传播。
- **输出**：closed-world 站点类别，concept drift 下跨周准确率，以及 open-world 的 PR 曲线、precision、F1 和按 cell 阈值的覆盖率—精度权衡。

### 3. 实验协议与结果

- **标准 CW**：GTT-Mon 为样本量最多且中位 cell 数不少于 10 的 168 类，每类最多抽取 1,000 个实例；GTT-Unmon 为 280,000 个其余类别，按 40K/40K/200K 划分训练、验证和测试；GTT-Pre 为 NetAugment 准备的 100 类×500 实例，和监测/非监测集合不重叠。对 GTT-Mon 取 (N\in\{1,5,10,20,90\})，总样本数 (T\in\{250,500,1000\})。GTT23 上 RoFiRe（(T=1000)）准确率随 (N=1,5,10,20,90) 为 23%、42%、51%、56%、63%；对应 NetAugment 为 18%、34%、42%、49%、60%。
- **跨合成数据泛化**：在 BigEnough、AWF 和 DF 上，(T=1000) 时 RoFiRe 相对 NetAugment 的准确率优势分别为 5–12、1–7 和 1–9 个百分点；论文将其作为跨分布鲁棒性证据，但 GTT23 仍是唯一真实 exit 数据集。
- **concept drift**：GTT-Mon-Drift 只保留跨 Week 1/7/13 均出现、且中位 cell 数不少于 10 的 81 类，Week 1 每类 290 个、Weeks 7/13 各 100 个；所有模型 (N=5)。RoFiRe (T=1000) 在三周分别为 46%、38%、35%，NetAugment 为 40%、31%、26%；(T=250/500) 的 RoFiRe 为 43/34/31% 和 44/36/32%。CellShift 转导 trace 的 CW 测试比 exit-to-exit 下降约 10%，因此作者把当前设置称为性能上界。
- **OW 与 base rate**：GTT-Mon/GTT-Unmon 组成 169 类模型，报告 binary PR。传统 OW 改变非监测集合规模 50K–200K、监测样本 (N=5,10,20)，RoFiRe 在 (N=10,20) 时优于 DF 和 NetAugment，但非监测规模越大 precision 越低。真实比例的 GTT-Week1、GTT-Month1、GTT-Entire 中监测流量约从 6% 降到 4% 和 1%；GTT-Entire 最佳 precision 约 0.2。Week1 的总体 precision 约 0.32，但 5–7% 的站点具有稳定高 F1，筛选 F1>0.8 的站点时 precision 可达 0.8。
- **消融与表示证据**：在 (N=10,T=1000) 的 CW 设置，DyWin 准确率 48%，比简单复制高 6 个百分点；cell length 的 F-ratio 从 0.66 提升到 0.86，duration 从 0.04 提升到 0.12。论文报告 RMSNorm 单独带来约 39 个百分点、pre-norm 约 6 个百分点，二者组合约提升 43 个百分点；并观察到比 DF 更平滑的收敛、更低验证损失和更少过拟合。
- **实现**：单张 NVIDIA RTX A6000 40 GB，Ubuntu 20.04；TensorFlow 2.9.0、PyTorch 2.6.0、CUDA 11.4；每模型 30 epochs，NetAugment 预训练 100 epochs；RoFiRe 使用 Adamax、学习率 0.002、label smoothing 0.1。每个实验重复三次并报告均值，作者称方差可忽略。

### 4. 论文结论的可支持范围

论文可以直接支持：在 GTT23 exit trace 上，DyWin 与 RMS-based pre-normalization 组合较传统 WF 基线更适合稀疏、高方差轨迹；RoFiRe 在真实 base rate 的 OW 仍能对少数高指纹性站点取得较高 precision；跨周性能虽下降但相对基线保持优势。不能直接推出：对真实入口观察者的同等精度、对未测量网站或不同 Tor 网络配置的部署保证、或者所有网站均存在显著隐私风险。OW 的高 precision 主要集中在少数站点，整体 precision 仍低，cell 阈值提高又会牺牲覆盖率和真实性。

### 5. 局限与复现建议

- 真实数据只有 GTT23；合成数据的跨域实验不能替代第二个真实 exit 数据集。
- 训练和测试均为 exit-side，entry/exit mismatch 只通过引用 CellShift 的约 10% 下降间接估计，未做端到端 entry-side 攻击。
- 过滤“类别中位 cell 数<10”和 DyWin 的 (C_t\le44) 排除规则会改变样本分布；OW 的 (	au\in\{10,100,1000\}) cell 阈值本身是 precision/coverage 的 triage 规则，不能把高阈值结果当作无条件攻击成功率。
- 复现时应固定 GTT23 的类别筛选、(N,T,N_w,\alpha)、三种场景的时间切分和真实 base rate；按作者软件栈复建五个 Conv1D block、RMSNorm/pre-norm、Adamax 训练，并分别复算 CW accuracy、drift accuracy、OW PR 和阈值覆盖率。当前本地笔记未发现代码仓库，代码可用性保留 unknown。

### 6. 方法定位与可迁移点

RoFiRe 的实质贡献是把增强粒度从 burst/time-bin 调整到“按每条 trace 自适应的窗口”，再用 RMSNorm/pre-norm 处理非平稳尺度；它将增强的适用性和架构稳定性绑定到真实 exit 数据的统计特征。可迁移的实验设计包括：先报告 cell count、duration、burst count 和 F-ratio，再在真实 base rate 下报告 PR；任何迁移到其他匿名网络或数据集的结论都应重新验证窗口阈值、短 trace 处理和时间漂移。

### 7. 证据范围

直接证据来自本地 `02-parsed-markdown/2026-WWW-RoFiRe__Robust_Website_Fingerprinting_on_Real-World_Tor_Traffic_via_Improved_Augmentation_and_Normalization.md` 的 §3–§8、表 1–4 及附录 A.3–A.7；摘要和正文明确给出的数值已保留，图中未给出精确坐标的结果没有补造。

## 历史自动入库段落说明

- 本笔记前部的自动入库、摘要级或待核验段落是入库时的历史快照，按规范保留以避免删除原始记录。
- 本次新增的深度分析段落、证据记录和局限说明优先；历史段落中的“待深读/待核验”状态不代表当前分析尚未完成。

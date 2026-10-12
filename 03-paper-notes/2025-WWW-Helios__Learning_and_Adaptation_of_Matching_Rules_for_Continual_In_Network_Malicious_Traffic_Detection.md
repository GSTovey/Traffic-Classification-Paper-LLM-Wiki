---
type: paper
title_original: "Helios: Learning and Adaptation of Matching Rules for Continual In-Network Malicious Trafic Detection"
title_cn: ""
authors: []
year: 2025
venue: WWW
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2025-WWW-Helios__Learning_and_Adaptation_of_Matching_Rules_for_Continual_In_Network_Malicious_Traffic_Detection.pdf"
mineru_md: "02-parsed-markdown/2025-WWW-Helios__Learning_and_Adaptation_of_Matching_Rules_for_Continual_In_Network_Malicious_Traffic_Detection.md"
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

# Helios: Learning and Adaptation of Matching Rules for Continual In-Network Malicious Trafic Detection

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Helios: Learning and Adaptation of Matching Rules for Continual In-Network Malicious Trafic Detection |
| 年份 | 2025 |
| 会议/期刊 | WWW |
| PDF | [[2025-WWW-Helios__Learning_and_Adaptation_of_Matching_Rules_for_Continual_In_Network_Malicious_Traffic_Detection.pdf]] |
| MinerU Markdown | [[2025-WWW-Helios__Learning_and_Adaptation_of_Matching_Rules_for_Continual_In_Network_Malicious_Traffic_Detection.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
Network Intrusion Detection Systems (NIDS) are critical for web security by identifying and blocking malicious trafic. In-network NIDS leverage programmable switches for high-speed trafic pro cessing. However, they are unable to reconcile the fine-grained classification of known classes and the identification of unseen attacks. Moreover, they lack support for incremental updates. In this paper, we propose Helios, an in-network malicious trafic detection system, for continual adaptation in attack-incremental scenarios. First, we design a novel Supervised Mixture Prototypical Learning (SMPL) method combined with clustering initialization to learn prototypes that encapsulate the knowledge, based on the weighted infinity norm distance. SMPL enables known class classification and unseen attack identification through similarity comparison between prototypes and samples. Then, we design boundary calibration and overlap refinement to transform learned prototypes into priority guided matching rules, ensuring precise and eficient in-network deployment. Additionally, Helios supports incremental prototype learning and rule updates, achieving low-cost hardware reconfigu ration. We implement Helios on a Tofino switch and evaluation on three datasets shows that Helios achieves superior performance in classifying known classes (92%+ in ACC and F1) as well as identi fying unseen attacks (62% - 98% in TPR). Helios has also reduced resource consumption and reconfiguration time, demonstrating its scalability and eficiency for real-world deployment.

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
- 主题线索：anomaly, tor。
- 摘要证据：Network Intrusion Detection Systems (NIDS) are critical for web security by identifying and blocking malicious trafic. In-network NIDS leverage programmable switches for high-speed trafic pro cessing. However, they are unable to reconcile the fine-grained classification of known classes and the identification of unseen attacks. Moreover, they lack support for incremental updates. In this paper, we propose Helios, an in-network malicious trafic detection system, for continual adaptation in attack-incremental scenarios. First, we design a novel Supervised Mixture Prototypical Learning (SMPL) method combined with clustering initialization to learn prototypes that encapsulate the knowledge, based on the weighted infinity norm distance. SMPL enables known class classification and unseen attack identification through similarity comparison between prototypes and samples. Then, we design boundary calibration and overlap refinement to transform learned prototypes into priority guided matching rules, ensuring precise and eficient in-network deployment. Additionally, Helios supports incremental prototype learning and rule updates, achieving low-cost hardware reconfigu ration. We implement Helios on a Tofino switch and evaluation on three datasets shows that Helios achieves superior performance in classifying known classes (92%+ in ACC and F1) as well as identi fying unseen attacks (62% - 98% in TPR). Helios has also reduced resource consumption and reconfiguration time, demonstrating its scalability and eficiency for real-world deployment.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：未检测到明确 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


### 并行深度分析（2026-09-29）
- 方法/问题：Helios supports continual in-network malicious traffic detection with supervised mixture prototypical learning, clustering initialization, weighted infinity-norm prototypes, boundary calibration and overlap refinement for known/unseen attacks and incremental updates. Missing: switch target/resource limits, traffic features, attack-incremental schedule and full metrics.
- 证据边界：以上仅使用对应 MinerU 解析稿摘要及可稳定提取段落；未提取到的数值、数据集、代码和参数均不作推断。
- 复现建议：先核对原文表格、附录、代码仓库和数据划分，再确定 L3/L4 复现。

## 深度方法分析（2026-10-09）

> 本节依据本地 MinerU 原文的 §1–§6、附录 A–E 追加。公式中的个别变量下标和硬件延迟单位在 MinerU 中有字符损坏，缺失内容均标为“论文未明确说明”。

### 1. 方法动机与问题边界

Helios 面向可编程交换机上的攻击增量（attack-incremental）恶意流量检测。GPU 上的深度 NIDS 通常需要把流量上传控制面，带来带宽和处理延迟；交换机数据面则只能执行整数运算、位移和 match-action，难以直接运行深度模型。已有树模型或蒸馏模型能在交换机部署，却普遍假设类别集合固定，或只能做二分类，无法同时细粒度识别已知攻击、拒识未知攻击并在新攻击出现后增量更新。

论文把目标拆成三个约束：已知类别要有较高的多类分类精度；未见攻击要被标记为 unknown；更新新类别时只重配置受影响的表项，避免全量重训和长时间中断。核心直觉是把“原始特征上的多个局部原型”转成交换机能执行的范围规则：多原型覆盖类内多峰结构，$l_\infty$ 距离可自然映射为逐维上下界，未命中任何规则的样本直接作为未见攻击。

### 2. 方法设计

#### 2.1 输入、处理和输出

| 模块 | 输入 | 处理 | 输出 |
|---|---|---|---|
| Attack Knowledge Prototyping | 带已知类别标签的原始流/包特征 | 每类 DBSCAN 初始化多个原型；用带权 $l_\infty$ 距离和交叉熵优化原型与权重 | 多类别原型集合及权重 |
| Priority-Guided Rule Transformation | 训练好的原型、被原型接收的样本 | 计算每个原型的平均接受距离、逐维上下界；细化重叠区域、拓扑排序分配优先级、剪枝并 boosting | P4 range-match 规则 |
| 数据面推理 | 新样本的特征向量 | 按优先级依次匹配范围表；命中则返回已知类别，全部未命中则标记 unseen attack | 已知类别或未知攻击标志 |
| Class-Incremental Rule Adaptation | 旧规则、新攻击样本、旧类样本 | 保留不匹配新样本的孤立规则；对新样本和残差样本重新学习并合并规则 | 需修改/删除/新增的表项及低成本重配置 |

#### 2.2 Attack Knowledge Prototyping：SMPL

对每个类别 $i$，先在该类样本上运行 DBSCAN，以密度簇中心初始化多个原型 $P_{ij}$。与需要预先指定簇数的 K-means 相比，DBSCAN 能按数据密度决定原型数量；原文未给出 $\epsilon$ 和最小样本数的具体值。

特征先做 min-max 归一化。每个原型带一个逐维权重 $w_{ij}$，距离定义为：

$$\mathrm{Dist}(x,P_{ij})=\left\|\left|\frac{x-x_{min}}{x_{max}-x_{min}}-P_{ij}\right|\cdot|w_{ij}|\right\|_\infty.$$

$l_\infty$ 只取各维最大加权差异，避免平方、开方等交换机不易实现的运算。类别距离是该类所有原型距离的最小值，经过带温度参数 $T$ 的 softmax 得到类别概率：

$$\Pr(y=i|x)=\frac{\exp(\min_j\mathrm{Dist}(x,P_{ij})/T)}{\sum_k\exp(\min_j\mathrm{Dist}(x,P_{kj})/T)}.$$

随后用交叉熵对原型和权重做梯度下降。每个样本只更新每类最近的原型：同类原型被拉近，异类原型被推远，减少无关原型受到的更新。实际交换机推理仍只需比较范围规则，不需要在数据面执行上述 softmax。

#### 2.3 Priority-Guided Rule Transformation

第一步是为每个原型建立接受样本集合：样本属于类别 $i$，且该原型距离不大于所有其他原型。对集合 $D_{P_{ij}}$，论文没有使用最大距离作为阈值，而使用平均接受距离：

$$\mathrm{Threshold}(P_{ij})=\frac{1}{|D_{P_{ij}}|}\sum_{x_k\in D_{P_{ij}}}\mathrm{Dist}(x_k,P_{ij}).$$

这样可以避免少数离群点把接受区域拉得过大。随后在每个维度取接受样本的最小值和最大值，形成范围 $[l_v,u_v]$；样本只有在所有维度都落入范围时才匹配。

多原型必然会造成规则重叠。Helios 对每个冲突集合统计重叠区域内各类别的样本数，把多数类别作为该区域的代表类别；再构造 DAG，从代表类别规则指向其他类别规则，跳过已有反向可达路径，最后拓扑排序并赋予优先级。仍无法得到最优类别的重叠区域被显式加入高优先级规则，优先级为 $10000+|S_k|$。只接收极少样本且代价低的规则会被剪枝，以减少过拟合和 TCAM 占用。

第一轮规则生成后，模型用当前规则误分类的残差样本重新做 SMPL，把新规则合并、重做重叠细化和优先级排序；这一过程就是 rule boosting。附录给出的默认 boosting iteration 为 4，剪枝下限为 10，边界校准缩放系数为 1.0。

#### 2.4 数据面与未知攻击

附录 B 的 P4 表以每个特征维度的 range 作为 key，以各已知类别的 `Set_class` 作为命中动作；默认动作是 `Set_as_unseen_attack`。因此 unknown 判定不是额外的神经网络头，而是“所有范围规则均未命中”的明确数据面路径。该设计能在交换机中线速执行，但未知判定质量直接取决于原型阈值和规则覆盖范围。

#### 2.5 Class-Incremental Rule Adaptation

新攻击样本到达后，Helios 不直接保留全部旧规则再追加新规则。它先删除所有与任一新攻击样本相交的旧规则，保留与新样本完全不匹配的孤立规则。然后将新攻击样本与旧规则下的误分类残差合并，重新执行规则学习和重叠处理。

附录算法 3 将表项分为四类：保留且优先级不变的 `R_retain`、只需改优先级或类别的 `R_modify`、被移除的 `R_delete` 和新增的 `R_add`。交换机只对这些集合执行对应重配置，减少全量表项写入；如果旧规则与新增规则没有冲突，其内容可以完全不变。

### 3. 与其他方法的本质差异

| 方法 | 已知多类 | 未知攻击 | 交换机可部署 | 增量更新 | 主要取舍 |
|---|---:|---:|---:|---:|---|
| Planter / NetBeacon / IIsy | 是 | 原生不支持，需额外阈值扩展 | 是 | 通常全量更新 | 规则执行成熟，但固定类别假设强 |
| Mousikav2 | 是 | 原生不支持，需阈值扩展 | 是 | 受限 | 资源较轻，但分类和未知识别能力有限 |
| 神经网络/复杂 OOD NIDS | 是 | 可支持 | 通常否 | 依赖重训 | 表达力强，但不适合 P4 算子限制 |
| Helios | 是 | 未命中规则即 unknown | 是，P4 range match | 是 | 多原型和规则重叠处理增加训练复杂度，换取线速与增量更新 |

Helios 的实质创新是把原型学习目标和硬件规则表示共同设计：$l_\infty$ 距离使模型空间与范围匹配空间一致，边界校准和冲突优先级解决了多原型转规则后的覆盖冲突，残差 boosting 和孤立规则保留又把一次性分类扩展为可持续更新。它更适合特征维度固定、需要线速推理和持续更新的交换机 NIDS，不适合依赖深层 payload 语义或频繁改变输入字段定义的任务。

### 4. 实验表现、优势与局限

#### 4.1 实验设置

- 数据集：CICIDS2018、TON-IoT、UNSW-NB15。
- 增量任务：每个数据集先以 benign 和一个攻击类初始化；随后每个任务把上一个任务的未知攻击加入已知集合，再引入一个新未知攻击。具体类序列由附录表 3 给出，包括 DDoS/DoS、SSH brute force、Web Attack、IoT 的 Mitm/DoS/Ransomware/Backdoor 等和 NB15 的 Worms/Backdoor/Exploits 等。
- 特征：NB15 使用 IPv4、TCP、UDP 字段；TON-IoT 使用包大小、到达间隔的均值/最大值/最小值、包数、协议和目的端口；CICIDS2018 使用前后向包大小统计和包级字段。
- 基线：Planter、NetBeacon、Mousikav2、IIsy。由于它们原生不支持 unknown，作者通过分类概率阈值扩展，并在 ACC 不低于 85% 的约束下最大化 $5\times ACC+TPR$ 选择阈值。
- 训练：每个任务 50 个 epoch，Adam 学习率 0.001；训练/测试比为 2:8，用于模拟少量标注样本。
- 硬件：服务器端使用 Intel Xeon Silver 4210 和 V100；数据面部署在 Edgecore Wedge100BF-65X Tofino 交换机；用 SPIRENT N11U 产生 10/50/100 Gbps 流量。

#### 4.2 分类与未知识别

Task ALL 的结果如下（ACC/F1 为已知类，TPR 为历次任务未知攻击识别的加权平均）：

| 数据集 | Helios ACC | Helios F1 | Helios TPR | ROC-AUC |
|---|---:|---:|---:|---:|
| CICIDS2018 | 95.78% | 95.98% | 98.21% | 0.98 |
| TON-IoT | 92.20% | 92.99% | 62.93% | 0.90 |
| UNSW-NB15 | 92.91% | 94.19% | 69.15% | 0.88 |

原文称 Helios 在 Task ALL 的 ACC/F1 上总体最好，并在 CICIDS2018、UNSW-NB15 的 TPR 上最好；逐任务结果显示，随着未知攻击加入，Helios 的 TPR 仍保持较稳定。ROC 曲线中 Helios 的 AUC 高于基线：CICIDS2018 为 0.98（Planter 0.59），TON-IoT 为 0.90（NetBeacon 0.88），UNSW-NB15 为 0.88（Planter 0.81）。

#### 4.3 更新成本与硬件性能

规则重配置时间为 0.8–3.1 秒；增量机制使规则部署量减少 13.4%–37.3%。论文摘要还报告最高约 4.5 倍的更新速度优势。资源图显示 Helios 通常占用 TCAM 和 SRAM 的 10% 以下，最复杂的 UNSW-NB15 约占 TCAM 40%。在 10、50、100 Gbps 发生器压力下，交换机无丢包；端到端延迟约为 0.66，但 MinerU 未保留单位符号，不能据此写成确定的微秒或纳秒。

#### 4.4 消融结果

TON-IoT 消融表给出：

| 变体 | ACC | TPR | 规则数 |
|---|---:|---:|---:|
| 正态初始化 | 76.91% | 36.38% | 90 |
| 均匀初始化 | 82.00% | 33.18% | 61 |
| K-means 初始化 | 91.46% | 58.30% | 394 |
| Euclidean 距离 | 90.08% | 64.66% | 306 |
| 去除 SMPL 与 boosting | 66.08% | 87.76% | 161 |
| 去除 boosting | 70.39% | 78.18% | 146 |
| 去除 SMPL | 88.52% | 38.39% | 325 |
| 去除边界校准 | 92.48% | 38.91% | 528 |
| Helios | 92.20% | 62.93% | 321 |

这些结果说明 DBSCAN 初始化、$l_\infty$ 距离、SMPL、boosting 和边界校准分别影响类内覆盖、已知类精度、未知攻击 TPR 和规则规模；仅追求 ACC 会扩大边界并显著牺牲 unknown 识别。

局限性包括：输入特征需预先定义且字段变化会触发重新建模；原型规则表达能力受 axis-aligned range 限制；未知判定依赖训练分布和阈值，不能等同于对所有 zero-day 攻击的保证；实验采用固定的任务序列和 2:8 划分，未报告真实线上类别到达分布；硬件评估依赖 Tofino，其他交换机的表项和流水线限制可能不同；代码链接、完整 P4 工程和随机种子在本地原文中未明确给出。

### 5. 学习、复现与迁移

#### 5.1 复现步骤

1. 按附录表 3 组织三个数据集的增量任务，按照表 4 提取固定长度的包/流特征，并在训练集统计 min/max 后做 min-max 归一化。
2. 对每个已知类别运行 DBSCAN 初始化多原型，使用式 (1) 的带权 $l_\infty$ 距离、式 (2) 的 softmax 和交叉熵训练原型/权重。
3. 按式 (3)–(6) 计算接受样本、平均距离阈值和逐维范围，处理规则重叠、拓扑排序、残差 boosting 和剪枝，生成 P4 range-match 表。
4. 在数据面设置默认 `Set_as_unseen_attack` 动作；按任务序列加入新攻击，执行孤立规则保留与 residual 重新学习。
5. 在软件仿真和真实 Tofino 上分别测 ACC/F1/TPR/AUC、规则数、重配置时间、TCAM/SRAM 和线速吞吐。

#### 5.2 已给出的超参数与缺口

| 项目 | 原文信息 | 缺口 |
|---|---|---|
| 训练 | 每任务 50 epoch，Adam，lr=0.001 | batch size、早停和随机种子未说明 |
| boosting | 默认 4 轮 | 轮间停止判据和残差权重未说明 |
| 剪枝 | lower bound=10 | cost-effective 的具体代价函数未完整说明 |
| 边界校准 | scaling weight=1.0；阈值为接受样本距离均值 | DBSCAN $\epsilon$/minPts、温度 $T$ 未说明 |
| unknown 阈值基线 | 最大化 $5\times ACC+TPR$ 且 ACC≥85% | 阈值搜索网格和验证集使用方式未说明 |
| 代码 | 未给出可核验仓库链接 | unknown |

#### 5.3 迁移价值

可迁移的设计模式是“先在可训练空间学习局部原型，再把距离接受域编译成硬件匹配规则”，适合需要线速推理的入网检测、遥测分类和边缘设备过滤。迁移到加密流量时，需重新验证特征稳定性和未知阈值；论文使用的是包/流统计字段，不能直接推出对加密 payload 语义的支持。

### 6. 总结

**核心思想：原型学习转成可增量匹配规则。**

速记版 pipeline：

1. 归一化原始流量特征，用 DBSCAN 为每类初始化多个原型。
2. 用带权 $l_\infty$ 距离训练原型和权重，按最近原型计算类别概率。
3. 用接受样本均值确定边界，生成范围规则并处理重叠、优先级和残差 boosting。
4. 交换机命中规则返回已知类，全部未命中则标记未知攻击。
5. 新攻击到来时保留孤立规则，只重训残差和受影响表项。

### 7. 知识层联动建议（不直接改共享总表）

- 可在 `05-methods/` 增加“原型到数据面匹配规则编译”方法条目，记录 DBSCAN 多原型、$l_\infty$ 距离、边界校准、重叠优先级和增量表项更新。
- 可在 `06-tasks/malicious-traffic-detection.md` 增加证据：in-network NIDS 的评估应同时报告已知类 ACC/F1、未知攻击 TPR/AUC、规则数、TCAM/SRAM、更新时延和线速吞吐。
- 可在 `09-claims/` 增加“未知攻击检测与持续更新可由规则默认动作和受影响表项重配置实现”的证据条目，但应注明其有效范围是三套公开数据和 Tofino 原型。
- 本次未修改共享方法表、任务表、Claims 总表或研究前沿页，避免与其他候选论文并行更新冲突。

### 8. 证据范围

- 直接证据：`02-parsed-markdown/2025-WWW-Helios__Learning_and_Adaptation_of_Matching_Rules_for_Continual_In_Network_Malicious_Traffic_Detection.md` 的 §1–§6、附录 A–E，覆盖式 (1)–(7)、算法 1–3、表 1–4 和图 2–5。
- 交叉核对：对应本地 PDF `00-inbox/PDFs/2025-WWW-Helios__Learning_and_Adaptation_of_Matching_Rules_for_Continual_In_Network_Malicious_Traffic_Detection.pdf` 已存在；本次未修改原 PDF 或 MinerU 原文。
- 证据限制：MinerU 对个别公式下标、图 4 延迟单位和部分表格布局有损坏；延迟单位、DBSCAN 参数、代码状态等未作推断。

## 历史自动入库段落说明

- 本笔记前部的自动入库、摘要级或待核验段落是入库时的历史快照，按规范保留以避免删除原始记录。
- 本次新增的深度分析段落、证据记录和局限说明优先；历史段落中的“待深读/待核验”状态不代表当前分析尚未完成。

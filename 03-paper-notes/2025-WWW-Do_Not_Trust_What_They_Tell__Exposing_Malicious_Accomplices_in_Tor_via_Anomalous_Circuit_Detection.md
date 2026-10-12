---
type: paper
title_original: "Do Not Trust What They Tell: Exposing Malicious Accomplices in Tor via Anomalous Circuit Detection"
title_cn: ""
authors: []
year: 2025
venue: WWW
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2025-WWW-Do_Not_Trust_What_They_Tell__Exposing_Malicious_Accomplices_in_Tor_via_Anomalous_Circuit_Detection.pdf"
mineru_md: "02-parsed-markdown/2025-WWW-Do_Not_Trust_What_They_Tell__Exposing_Malicious_Accomplices_in_Tor_via_Anomalous_Circuit_Detection.md"
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

# Do Not Trust What They Tell: Exposing Malicious Accomplices in Tor via Anomalous Circuit Detection

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Do Not Trust What They Tell: Exposing Malicious Accomplices in Tor via Anomalous Circuit Detection |
| 年份 | 2025 |
| 会议/期刊 | WWW |
| PDF | [[2025-WWW-Do_Not_Trust_What_They_Tell__Exposing_Malicious_Accomplices_in_Tor_via_Anomalous_Circuit_Detection.pdf]] |
| MinerU Markdown | [[2025-WWW-Do_Not_Trust_What_They_Tell__Exposing_Malicious_Accomplices_in_Tor_via_Anomalous_Circuit_Detection.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
The Tor network, while ofering anonymity through trafic routing across volunteer-operated nodes, remains vulnerable to attacks that aim to deanonymize users by correlating trafic patterns between colluded entry and exit nodes in circuits. This paper presents a novel approach for detecting anomalous circuits in the Tor network, and for the first time provides a more comprehensive identification of potential malicious accomplice nodes in Tor by taking roles ofnodes in anomalous circuits into consideration. Our method strategically utilizes modified middle nodes to capture trafic data, followed by a novel circuit classification based on trafic patterns to pinpoint concerned circuits. Two kinds of anomalies are identified: routing anomalies and usage anomalies, that respectively represent the anomalies with explicit or implicit violation of Tor’s circuit construction guidelines. This leads to a successful revealing of totally 1,960 anomalous nodes in Tor. Furthermore, we apply clustering analysis with considering corresponding anomalous circuits and other key characteristics to the detected anomalous nodes, reveal ing potential hidden organizations behind these nodes that can threaten the network’s security. Our findings highlight the neces sity for the Tor project to adopt targeted mitigation strategies to enhance overall network security and privacy.

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
- 主题线索：website fingerprint, anomaly, tor, quic。
- 摘要证据：The Tor network, while ofering anonymity through trafic routing across volunteer-operated nodes, remains vulnerable to attacks that aim to deanonymize users by correlating trafic patterns between colluded entry and exit nodes in circuits. This paper presents a novel approach for detecting anomalous circuits in the Tor network, and for the first time provides a more comprehensive identification of potential malicious accomplice nodes in Tor by taking roles ofnodes in anomalous circuits into consideration. Our method strategically utilizes modified middle nodes to capture trafic data, followed by a novel circuit classification based on trafic patterns to pinpoint concerned circuits. Two kinds of anomalies are identified: routing anomalies and usage anomalies, that respectively represent the anomalies with explicit or implicit violation of Tor’s circuit construction guidelines. This leads to a successful revealing of totally 1,960 anomalous nodes in Tor. Furthermore, we apply clustering analysis with considering corresponding anomalous circuits and other key characteristics to the detected anomalous nodes, reveal ing potential hidden organizations behind these nodes that can threaten the network’s security. Our findings highlight the neces sity for the Tor project to adopt targeted mitigation strategies to enhance overall network security and privacy.

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
- 研究定位：Tor异常电路/恶意协作者识别
- 方法机制：利用改造middle节点采集流量，按路由异常与使用异常分类电路，并结合节点角色和聚类定位潜在协同组织；摘要报告识别1,960个异常节点。
- 输入—处理—输出：Tor流量观测与电路分类；输出异常电路、节点角色和组织聚类。
- 证据边界：摘要明确了异常类型和节点数量；数据采集范围、分类特征、阈值、误报率及代码状态在当前解析证据中未完整确认。
- 联动标签：website-fingerprinting；DNS；anomaly-detection；traffic-security


## 深度方法分析（2026-10-09）

> 依据本地 MinerU 原文 §1–§7、附录 A–C 追加。论文研究的是 Tor 网络测量和异常电路发现，文中的“潜在恶意节点/组织”是风险线索，不等同于已证实的攻击者归属。

### 1. 方法动机与问题边界

Tor 的自动路径构造禁止同一 family 或同一 /16 子网的节点同时出现在一条电路，但用户可以手工指定节点，节点运营者也可能隐藏 family 关系。若同一组织控制的节点反复作为 entry/exit，流量关联攻击可能破坏匿名性。论文要解决两个问题：从受控 middle 节点观察到的 cell traces 中识别 exit/prebuilt 电路；再从异常 entry–exit 对中挖掘潜在协同节点。

论文将异常分为两类：Routing anomaly 是显式违反 Tor 路由约束的节点对；Usage anomaly 是在给定 entry 时某 exit 的出现频率、以及反向条件频率都显著高于基于共识权重的期望。实验目标是发现异常节点和组织结构，不能把统计异常直接解释成已完成的去匿名化攻击。

### 2. 方法设计

#### 2.1 采集与电路位置识别

作者部署改造后的 middle relay，记录每个 Tor cell 的时间戳、方向、Circuit ID、Circuit Section ID 和下一跳 fingerprint。每条 circuit section 的 cell 序列用来区分 9 类电路、24 类中间节点位置。客户端 padding 会干扰分类：client-IPO 的 padding 通过时间密度识别（邻近间隔小于 0.1 s、minPts=8 的 DBSCAN），client-RPO 通过固定的正负方向 padding 模式识别，再从序列中移除。

附录 B 给出基于 Tor 协议序列的规则决策树；当 cell 数量模式无法唯一确定 client-IPO 与 prebuilt 时，加入 `ifpadding` 标签。验证实验中，作者让客户端和 hidden service 只选择自有 middle 节点，访问 100 个公开站点和 100 个 onion 站点，得到 100 个 exit、600 个 internal（6 类各 100）和 100 个 prebuilt 电路，位置分类准确率为 100%。

#### 2.2 Routing anomaly 与 Usage anomaly

当受控节点被识别为 exit 电路第二跳，或被识别为第三跳带 Exit 但不带 Guard 的 prebuilt 电路时，可同时得到 entry 和 exit fingerprint。Routing anomaly 直接通过 family、/16 等配置约束比较识别。

对 Usage anomaly，令 $N_{ij}$ 为 entry $i$ 与 exit $j$ 同时出现的次数，$N^i_{entry}$ 和 $N^j_{exit}$ 为两端各自出现次数，观测条件频率为

$$F(j_{exit}|i_{entry})=N_{ij}/N^i_{entry},\quad F(i_{entry}|j_{exit})=N_{ij}/N^j_{exit}.$$

若节点选择相互独立，这两个条件频率应接近独立的 entry/exit 选择概率。但采集跨越 40 多天，Tor 共识权重会变化，因此作者根据波动二项模型用共识文件计算调整概率 $P'_{exit}(j)=Var(m)/E(n)$（式 (5)，entry 对称）。随后对两个方向分别做单尾二项检验；只有双向都在 $p<0.005$ 下拒绝独立性假设，才把节点对标为 Usage anomaly。该双向条件降低了“固定单端节点”被误报为固定 entry–exit 对的可能。

#### 2.3 异常节点聚类

聚类距离由三类信息构成：

1. **Intrinsic similarity**：节点 nickname 的长度/编辑距离/公共子串/字符模式，advertised/burst/observed bandwidth，国家，IP/端口变更时间、首次出现/最后变更时间、过去六个月 uptime sequence，以及 Tor 版本。作者用 Tor Metrics 中 2,256 个正样本与 2,256 个负样本训练 Naive Bayes、SVM、Logistic Regression、Random Forest，选择 F1 最高的 SVM 输出节点相似度。
2. **Family flag**：`fam(a,b)=0` 表示节点显式声明属于同一 family，反之为 1；该编码使 family 关系参与距离但不压倒其他特征。
3. **Anomalous connection**：若两节点在异常电路共同出现次数为 $N_c(a,b)$，则 $conn(a,b)=e^{-N_c(a,b)}$，随后按论文描述做对数稳定化。

最终距离为 $D(a,b)=\alpha sim(a,b)+\beta fam(a,b)+\gamma conn(a,b)$，经验权重为 $(\alpha,\beta,\gamma)=(1,0.5,1)$。对 1,960 个异常节点用 DBSCAN 聚类；实验设置 eps=0.14、minPts=20，并用 MDS 做二维可视化。

### 3. 与其他方法的差异

| 方法 | 观测对象 | 主要证据 | 局限 | 本文差异 |
|---|---|---|---|---|
| 节点配置比较 | nickname、bandwidth、family 等静态属性 | 相似配置 | 隐藏 family 或配置异质时难发现 | 将异常电路角色和共现频率纳入 |
| 流量关联/电路指纹 | cell 或流量时序 | 端到端关联 | 需要更强观测位置或目标场景 | 从受控 middle 观察位置并先分类电路 |
| Sybil relay 检测 | 节点 uptime、配置或家族关系 | 组织/节点相似性 | 对隐式 entry–exit 配对有限 | 双向条件频率检验显式/隐式异常 |
| 本文 | middle cell trace + consensus 概率 + 节点属性 | Routing/Usage anomaly + 聚类 | 统计风险线索，非攻击归因 | 面向潜在协同节点的电路级测量 |

### 4. 实验表现、优势与限制

- 规模与环境：Tor 网络超过 9,000 个节点；10 个自建 middle 节点部署在纽约、旧金山、阿姆斯特丹、新加坡、伦敦、法兰克福、多伦多、班加罗尔和悉尼；Ubuntu 20.04、1 GB 内存、25 GB 磁盘；2024-03-01 至 2024-04-15 共 45 天，收集 45,367,152 条 circuit-section trace。
- 分类结果：24 类位置分类准确率 100%；prebuilt 占 81%，维护电路约 18%，主动用户电路约 1%（图 6）。
- 检测范围：筛查 31,362 个 relay 对和 727,738 个 exit-prebuilt 候选对，共 759,100 对；去重后得到 415,858 条待检电路。
- 异常结果：Routing anomaly 4,198 对、1,641 个节点；单向 Usage(entry fixed) 6,721 对/2,549 节点；Usage(exit fixed) 2,634 对/1,979 节点；双向 Usage 300 对/360 节点。作者汇总称发现 1,960 个异常节点，但各类别节点集合可能重叠，不能简单相加。
- 统计解释：双向 Usage 异常比例约为单向异常的 11%，是按 $p=0.005$ 预期约 0.5% 的 22 倍；这支持“超过独立选择噪声”的判断，但不证明每个节点是恶意运营者。
- 相似度分类：SVM 最好，Accuracy 96.45%、Precision 88.55%、Recall 92.32%、F1 90.43%。DBSCAN 在 1,960 节点上得到 5 个密集簇；簇 1（241）全来自 family 2，簇 3（321）主要来自 family 1，簇 2/4 含较多未标 family 节点，簇 5（147）主要来自 family 4。

优势是能把协议级 cell 序列、Tor 共识概率和节点组织特征串成可测量证据链；局限是观测依赖自建 middle 节点的地理覆盖和被选中概率，异常依赖独立性与共识权重近似，聚类只产生潜在组织线索，未验证真实攻击控制关系或实际用户去匿名化成功率。论文也不覆盖用户手工构造的非标准电路类型。

### 5. 学习与复现

1. 获取与时间窗口一致的 Tor consensus、relay family/flags 和 node descriptors；部署多区域 middle relay 并记录 cell trace。
2. 实现 padding 过滤、24 类位置决策树和 `ifpadding` 特征，使用受控客户端/hidden service 做位置准确率验证。
3. 只提取 exit 与可用于 exit 的 prebuilt 电路，计算 entry–exit 共现计数和两个方向的条件频率。
4. 使用随时间变化的 consensus weight 估计调整概率，执行双向单尾二项检验，固定 $p=0.005$ 并记录候选对的样本量和时间跨度。
5. 在可信节点对上训练相似度分类器，用 $(1,0.5,1)$ 组合距离并以 DBSCAN eps=0.14、minPts=20 聚类；做敏感性分析和人工复核，避免把 family 或地域共性误当作协同证据。

代码仓库、完整抓包程序、所有 relay fingerprint 及原始 45 天 traces 未在本地原文中给出，开源状态记为 unknown；复现需要取得 Tor 网络测量许可并重新收集数据。

### 6. 总结

**核心思想：用异常电路发现潜在 Tor 协同节点。**

速记版 pipeline：

1. 在多区域部署改造 middle 节点，采集 Tor cell traces。
2. 去除 padding，用协议规则把 traces 分类为 24 类电路位置。
3. 用 Routing 规则和双向 Usage 频率检验发现异常 entry–exit 对。
4. 融合节点属性、family 和异常共现关系，对 1,960 个异常节点聚类。

### 7. 知识层联动建议（不改共享表）

- 在 `05-methods/` 增加“Tor 异常电路测量与节点聚类”条目，区分协议位置分类、双向频率检验和组织聚类。
- 在 `06-tasks/` 的匿名通信流量识别页记录：异常检测结果应分离路由违规、使用频率异常和组织归因证据。
- 可在 `12-research-fronts/` 的 Tor/匿名通信前沿页记录“受控 middle 节点观测的地理覆盖与误报校准”作为研究空白；本次未修改共享页。

### 8. 证据范围

直接证据为 `02-parsed-markdown/2025-WWW-Do_Not_Trust_What_They_Tell__Exposing_Malicious_Accomplices_in_Tor_via_Anomalous_Circuit_Detection.md` 的 §1–§7、式 (1)–(9)、表 1–4 和附录 A–C；对应本地 PDF 已存在。本次未修改 PDF、MinerU 原文或共享对比表。

## 历史自动入库段落说明

- 本笔记前部的自动入库、摘要级或待核验段落是入库时的历史快照，按规范保留以避免删除原始记录。
- 本次新增的深度分析段落、证据记录和局限说明优先；历史段落中的“待深读/待核验”状态不代表当前分析尚未完成。

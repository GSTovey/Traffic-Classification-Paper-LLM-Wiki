---
type: paper
title_original: "Towards adaptive and robust website fingerprinting defense with multi-agent deep reinforcement learning"
title_cn: ""
authors: []
year: 2026
venue: JCN
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-JCN-Towards_adaptive_and_robust_website_fingerprinting_defense_with_multi-agent_deep_reinforcement_learning.pdf"
mineru_md: "02-parsed-markdown/2026-JCN-Towards_adaptive_and_robust_website_fingerprinting_defense_with_multi-agent_deep_reinforcement_learning.md"
status: processed
reading_level: L2
research_area: []
task: []
method: []
dataset: []
code: unknown
relevance: medium
created: "2026-09-29"
updated: "2026-09-29"
---

# Towards adaptive and robust website fingerprinting defense with multi-agent deep reinforcement learning

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Towards adaptive and robust website fingerprinting defense with multi-agent deep reinforcement learning |
| 年份 | 2026 |
| 会议/期刊 | JCN |
| PDF | [[2026-JCN-Towards_adaptive_and_robust_website_fingerprinting_defense_with_multi-agent_deep_reinforcement_learning.pdf]] |
| MinerU Markdown | [[2026-JCN-Towards_adaptive_and_robust_website_fingerprinting_defense_with_multi-agent_deep_reinforcement_learning.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
ed as a classifier, where the input is the passively observed traffic feature vector (e.g., timing, packet direction), and the output is the predicted website label. Let ̂�(�) represent the attacker’s classification accuracy under the traffic splitting strategy �. Then, the defender’s optimization objective is : min ̂�(�), subject to the following constraints: (1) Traffic integrity constraint: $\textstyle \sum _ { i } p _ { i } = 1$ , which ensures that the traffic is fully allocated (2) Circuit bandwidth constraint: $\begin{array} { r } { \sum _ { u } b _ { u } \ \le \ B _ { i } , \quad \forall i \ \in \ { \mathfrak { c } } } \end{array}$ , where $b _ { u }$ represents the traffic demand of user $u ,$ and $B _ { i }$ is the bandwidth capacity of circuit �. ![](images/dd039d8ac768001ff6a36e9a39143a5e0d7bbe226a2483e539bac85f4ee3dd56.jpg) Fig. 2. MADRL interaction model. (3) Communication delay constraint: $\begin{array} { r } { \sum _ { i } d _ { i } \ \le \ D _ { m a x } } \end{array}$ , where $d _ { i }$ represents the delay for circuit �, and $D _ { m a x }$ is the maximum acceptable delay for the user. This optimization problem is difficult to model explicitly, especially when the attacker is capable of strategy learning and dynamically adjusting the classifier parameters. The defender faces a highly nonconvex, unstable dynamic optimization problem. Furthermore, consid ering that the attacker has adaptive learning capabilities, the classification strategy may constantly update with changes in the defense mechanism. In this setup, the problem essentially evolves into a two agent adversarial game, where the defender and the attacker agents engage in strategy iteration within the same environment, each attempting to minimize and maximize classification accuracy, respectively: $\begin{array} { r } { \operatorname* { m i n } _ { \pi _ { d } } \operatorname* { m a x } _ { \pi _ { a } } \hat { y } , } \end{array}$ where $\pi _ { d }$ represents the defender’s strategy (i.e., how to generate the splitting vector $p ) _ { : }$ , and $\pi _ { a }$ represents the attacker’s strategy $( \mathrm { i . e . , }$ , how to select the attack model and monitoring paths). During this adversarial game, both agents iteratively update their strategies to optimize their respective objectives. The defender aims to minimize the attacker’s recognition accuracy, while the attacker seeks to maximize it. The expected cumulative reward of this interaction is denoted as $R ,$ reflecti

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
- 主题线索：website fingerprint, encrypted traffic, dns, tor, adversarial, quic, traffic classification。
- 摘要证据：MinerU 未稳定提取摘要，不能据此补写贡献。

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
<table><tr><td>Category</td><td>Configuration/Description</td></tr><tr><td>Hardware Configuration</td><td>Intel Xeon Gold 5218, 128 GB RAM</td></tr><tr><td>Software Platform</td><td>Ubuntu 18.04; Python 3.8.20; PyTorch 1.13.0</td></tr><tr><td>Reinforcement Learning Library</td><td>XuanCe-1.2.3</td></tr><tr><td>Network Architecture</td><td>Actor/Critic: MLP (2 layers, 128/64 neurons), activation: ReLU</td></tr><tr><td>Path Number</td><td>Fixed n = 3 (three independent paths per transmission)</td></tr><tr><td>Reward Function Weights</td><td>Defense: Security 2.0, Allocation entropy 0.1;Attack: Attack success 1.0, Path switching cost 0.1, Model switching cost 0.3</td></tr></table> $$ \mathrm{Delay} = \frac {T _ {\mathrm{actual}} - T _ {\mathrm{original}}}{T _ {\mathrm{original}}} \times 100 \%\tag{18} $$ Here, $T _ { \mathrm { a c t u a l } }$ denotes the transmission delay under the defense strategy, while $T _ { \mathrm { o r i g i n a l } }$ refers to the baseline delay without any defense. This metric reflects the trade-off between security and communication efficiency, ensuring that latency overhead remains within a practically acceptable range. Path allocation entropy (H). This metric captures the perturbation intensity and unpredictability of traffic allocation. Higher entropy values indicate a more balanced utilization of available paths, thereby increasing the difficulty of successful traffic classification by attackers [42]. The entropy is computed as: $$ H (p) = - \sum_ {i = 1} ^ {n} p _ {i} \log_ {2} p _ {i}\tag{19} $$ where $p _ { i }$ represents the probability of traffic being allocated to the �th path (satisfying $\begin{array} { r } { \sum _ { i = 1 } ^ { n } p _ { i } = 1 ) _ { : } } \end{array}$ , and � is the total number of paths. An entropy value appr

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：未检测到明确 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。

## 深度分析（2026-09-29）

- reading_level: L3
- 研究定位：WF防御/MADRL
- 方法机制：RAMAD把WF攻防建模为Dec-POMDP，以异构攻击者和防御者构成多智能体博弈，采用MAPPO、集中训练分散执行，并用多目标奖励联合攻击准确率、流量平衡和路径成本；摘要声称攻击准确率降低超过80%。
- 输入—处理—输出：输入为部分可观测Tor流量与网络状态；防御策略动态调整流量分割/路径，输出混淆后的流量。
- 证据边界：性能百分比来自摘要，需核验数据集、基线、开销与训练稳定性；论文为JCN，代码未知。
- 联动标签：website-fingerprinting；DNS；anomaly-detection；traffic-security


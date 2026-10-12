---
type: paper
title_original: "AdvTG: An Adversarial Trafic Generation Framework to Deceive DL-Based Malicious Trafic Detection Models"
title_cn: ""
authors: []
year: 2025
venue: WWW
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2025-WWW-AdvTG__An_Adversarial_Traffic_Generation_Framework_to_Deceive_DL-Based_Malicious_Traffic_Detection_Models.pdf"
mineru_md: "02-parsed-markdown/2025-WWW-AdvTG__An_Adversarial_Traffic_Generation_Framework_to_Deceive_DL-Based_Malicious_Traffic_Detection_Models.md"
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

# AdvTG: An Adversarial Trafic Generation Framework to Deceive DL-Based Malicious Trafic Detection Models

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | AdvTG: An Adversarial Trafic Generation Framework to Deceive DL-Based Malicious Trafic Detection Models |
| 年份 | 2025 |
| 会议/期刊 | WWW |
| PDF | [[2025-WWW-AdvTG__An_Adversarial_Traffic_Generation_Framework_to_Deceive_DL-Based_Malicious_Traffic_Detection_Models.pdf]] |
| MinerU Markdown | [[2025-WWW-AdvTG__An_Adversarial_Traffic_Generation_Framework_to_Deceive_DL-Based_Malicious_Traffic_Detection_Models.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
Deep learning-based (DL-based) malicious trafic detection models are efective but vulnerable to adversarial attacks. Existing adver sarial attacks have shown promising results when targeting trafic detection models based on statistics and sequence features. However, these attacks are less efective against models that rely on payload analysis. The main reason is the dificulty in generating semantic, compliant, and functional payloads, which limits their practical application. In this paper, we propose AdvTG, an adversarial trafic generation framework to deceive DL-based malicious trafic based on the large language model (LLM) and reinforcement learning (RL). Specifically, AdvTG is designed to attack various DL-based detection models across diverse payload features and architectures, thereby enhancing the generalization capabilities of the generated adversarial trafic. Moreover, we design a specialized prompt for trafic generation tasks, where functional fields and target types are supplied as input, while non-functional fields are generated to produce the mutated trafic. This fine-tuning endows the LLM with task comprehension and trafic pattern reasoning abilities, al lowing it to generate trafic that remains compliant and functional. Furthermore, leveraging RL, AdvTG automatically selects trafic fields that exhibit more robust adversarial properties. Experimental results show that AdvTG achieves over 40% attack success rate (ASR) across six detection models on four base datasets and two extended datasets, significantly outperforming other adversarial attack methods.

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
- 主题线索：anomaly, tor, transformer, adversarial。
- 摘要证据：Deep learning-based (DL-based) malicious trafic detection models are efective but vulnerable to adversarial attacks. Existing adver sarial attacks have shown promising results when targeting trafic detection models based on statistics and sequence features. However, these attacks are less efective against models that rely on payload analysis. The main reason is the dificulty in generating semantic, compliant, and functional payloads, which limits their practical application. In this paper, we propose AdvTG, an adversarial trafic generation framework to deceive DL-based malicious trafic based on the large language model (LLM) and reinforcement learning (RL). Specifically, AdvTG is designed to attack various DL-based detection models across diverse payload features and architectures, thereby enhancing the generalization capabilities of the generated adversarial trafic. Moreover, we design a specialized prompt for trafic generation tasks, where functional fields and target types are supplied as input, while non-functional fields are generated to produce the mutated trafic. This fine-tuning endows the LLM with task comprehension and trafic pattern reasoning abilities, al lowing it to generate trafic that remains compliant and functional. Furthermore, leveraging RL, AdvTG automatically selects trafic fields that exhibit more robust adversarial properties. Experimental results show that AdvTG achieves over 40% attack success rate (ASR) across six detection models on four base datasets and two extended datasets, significantly outperforming other adversarial attack methods.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


### 并行深度分析（2026-09-29）
- 方法/问题：AdvTG uses LLM plus reinforcement learning to generate semantic, protocol-compliant adversarial traffic targeting payload/statistical/sequence detectors; prompt constraints preserve functional fields. Evidence: abstract and method sections in MinerU. Missing: exact RL state/action/reward, datasets, attack success and overhead tables.
- 证据边界：以上仅使用对应 MinerU 解析稿摘要及可稳定提取段落；未提取到的数值、数据集、代码和参数均不作推断。
- 复现建议：先核对原文表格、附录、代码仓库和数据划分，再确定 L3/L4 复现。

## 深度方法分析（2026-10-09）

> 本节依据本地 MinerU 原文的 §1–§10、附录 A–F 追加。原文存在字符识别错误（如 traffic、不同公式变量和部分表格标题），涉及缺失字段、训练细节或表格未完整解析处均保留为“论文未明确说明”。

### 1. 方法动机与问题边界

论文针对的是“内容型对抗流量”问题：统计特征攻击只能改变流级数值，序列攻击主要改变包长和时间关系，二者都可能被依赖 payload 的检测器继续识别；已有内容攻击又难以同时生成完整、语义合理、符合 HTTP 规范并保持原始功能的报文。作者将目标限定为明文 HTTP/HTTPS 场景中的 HTTP 内容（实验实际围绕明文 HTTP），不评估加密后的 ciphertext，也不处理训练数据投毒。

威胁模型有三个关键约束：攻击者不知道目标模型的架构、特征提取方式和参数，只能把生成的流量送入黑盒检测器并取得分类分数；攻击者只能修改测试样本；请求行、URI、Host 和发挥核心业务作用的 payload 等功能字段必须保持不变，只生成或改写非功能字段。研究假设是：如果多个异构检测器共同作为反馈，LLM 可以在保持功能和协议合规的前提下学习到跨特征、跨架构的有效非功能字段扰动。

### 2. 方法设计

#### 2.1 输入、处理和输出

| 阶段 | 输入 | 处理 | 输出 |
|---|---|---|---|
| 目标模型训练 | 四个基础数据集中的 HTTP 流量及恶意/良性标签 | 分别构造字节图像和文本 token 表示，训练六个检测器 | 文本型与图像型检测器及其分类概率，兼作 RL 奖励模型 |
| 领域适配 | HTTP 流量、流量类别指令、功能字段 | 用 Meta-Llama-3-8B 做 LoRA 参数高效微调，学习 HTTP 格式、类别和字段模式 | 能根据功能字段补全 HTTP 报文的领域 LLM |
| 对抗生成 | 功能字段、目标类别指令 | PPO 更新 RL-Tuned LLM；冻结的领域 LLM 作为参考策略；多个检测器给出负交叉熵奖励，并加 KL 惩罚 | 只改变非功能字段的完整 HTTP 对抗报文 |
| 合规检查与评估 | 生成报文、RFC 结构要求、检测器输出 | 检查请求行、header 格式、空行和功能字段；计算 ASR、P/R/F1 及迁移效果 | 合规率、攻击成功率和跨模型/跨数据集结果 |

#### 2.2 第一阶段：异构检测器作为黑盒奖励模型

论文先把每个 payload 转为两类输入。图像路径将字节序列 $T=[b_1,ldots,b_n]$ 除以 255 归一化，再 reshape 成预定二维灰度图；超出尺寸的字节被截断，不足部分补零。文本路径将流量 token 化，再通过词表映射成离散 token index。原文没有稳定给出图像的具体边长、截断长度或词表规模。

六个目标模型分为三种文本模型和三种图像模型：TextCNN、DeepLog、BERT；MalTraffic、RBRN、DeepMal。每个模型输出恶意类别概率。在 PPO 中这些模型不被假定为可访问内部梯度，而只提供黑盒分数，因此同时承担“攻击目标”和“奖励模型”两种角色。多模型的意义不是增加一个集成分类器，而是让生成器不能只针对单一表示的捷径。

#### 2.3 第二阶段：HTTP 领域微调

论文采用 Meta-Llama-3-8B，并使用 LoRA 做参数高效微调。按照式 (4)–(5)，冻结原始权重 $W_0$，仅学习低秩增量 $BA$：

$$h=W_0x+BAx.$$

流量专用 prompt 包含类别说明和保持不变的功能字段。LLM 的任务是生成非功能字段并拼成完整报文；这样把“保持功能”从事后过滤约束前置为输入结构约束。微调数据同时让模型接触良性和恶意 HTTP 模式，但论文未给出微调样本规模、LoRA rank、训练轮数、学习率或 prompt 全文。

#### 2.4 第三阶段：PPO 对抗生成

对每个样本，prompt 的功能字段保持原样，指令要求生成相反类别的流量。例如输入恶意功能字段时，要求补成看起来良性的报文。RL-Tuned LLM 生成完整序列，多个检测器得到概率 $D_i(y)$，作者将负交叉熵定义为奖励：

$$r_\theta(x,y)=-\frac1N\sum_{i=1}^{N}[(1-L_x)\log D_i(y)+L_x\log(1-D_i(y))].$$

该式按作者描述用于“让预测偏离原标签”，再叠加相对于 SFT 参考策略的 KL 惩罚：

$$R(x,y)=r_\theta(x,y)-\beta\log[\pi_\phi^{RL}(y|x)/\pi^{SFT}(y|x)].$$

因此优化目标同时包含两部分：尽量让多种检测器误判，以及不要让 RL 策略偏离已经学会 HTTP 结构的 SFT 策略过远。论文说明按词序列反向传播奖励，但没有给出 PPO clip、KL 系数 $\beta$、采样温度、batch size、查询预算或停止条件。

#### 2.5 合规和功能保持

附录 E 的检查器按 HTTP 报文的请求行、header、header 与 body 之间的空行和可选 payload 检查格式；功能字段按示例被强制固定。Cobalt Strike 示例中，URI、Host、payload 属于功能字段，User-Agent 和 Content-Type 等可作为非功能字段。合规率因此表示“结构检查通过且功能字段未被改变”，并不等价于在真实服务器上成功执行了请求；论文没有给出真实服务端回放验证。

### 3. 与其他方法的本质差异

| 方法类别 | 可修改内容 | 主要限制 | AdvTG 的差异 |
|---|---|---|---|
| 统计特征攻击 | 流持续时间、平均包长等统计量 | 特征难映射回真实报文，跨特征泛化弱 | 直接生成完整 HTTP 报文 |
| 序列特征攻击 | 包长、方向、时间间隔 | payload 检测器仍能识别；不能生成语义内容 | 生成语义化 payload 字段 |
| 文本替换攻击（TextFooler、WordLevel、BAE） | 少量词/字段替换 | 只适配文本模型，容易破坏协议或完整报文 | LLM 补全多字段，并约束协议/功能 |
| 随机非功能字段替换 | 随机借用其他类别字段 | ASR 低，不能识别对模型稳健的字段 | PPO 根据多模型反馈选择更有效字段 |
| AdvTG | 非功能字段 + LLM 生成 + PPO | 明文 HTTP 范围；加密流量和真实在线查询未验证 | 兼顾跨模态攻击、协议合规与功能保持 |

它的核心创新不是“LLM 能写文本”本身，而是把功能字段固定、非功能字段生成和多模型黑盒反馈放在同一个 PPO 闭环内。适用场景是需要测试 payload 检测器在测试时黑盒条件下的鲁棒性；不宜把结果直接外推为对 TLS 加密流量或实际恶意基础设施的攻击能力。

### 4. 实验表现、优势与可核验限制

#### 4.1 实验设置

- 环境：Ubuntu 22.04.1、Python 3.11、AMD EPYC 7532、NVIDIA RTX 4090、256 GB 内存。
- 基础数据集：CICIDS2017、CICIoT2023、Malware（2021–2023 年样本，含 Trickbot、Qakbot、Emotet 等）和作者从 5000 份 APT 报告与 VirusTotal/ANY.RUN 沙箱收集的 APT；良性流量还包含从前述数据集提取的流量及 300 个热门网站解密得到的流量。
- 扩展测试集：CIC-APT-IIoT2024 和作者收集的 APT2024，仅测试，不参与训练或微调。
- 训练/测试规模：表 5 给出四个基础数据集各 10,000 个测试包（恶意数分别为 5,132、3,045、2,670、4,813），训练集合计 100,000（50,000 良性、50,000 恶意）；扩展集为 5,000（CIC-APT-IIoT2024，恶意 2,500）和 1,000（APT2024，恶意 384）。
- 攻击基线：TextFooler、WordLevel、BAE、随机替换；附录另报告 RobTest（R-T，阈值 0.05/0.1/0.2）和 RoBERTa、DistilBERT、XLNet 目标模型。
- 指标：检测 P/R/F1；攻击 ASR 定义为成功误导样本数除以攻击样本总数。

#### 4.2 关键结果

1. 六个基础目标模型的测试 F1 均高于 0.96，文本模型均高于 0.98。
2. 表 2 中基础集的 AdvTG ASR：文本模型约为 41.41%–69.53%，图像模型约为 42.17%–67.96%；TextFooler、WordLevel、BAE 通常低于 10%，随机替换低于 22.27%。
3. 合规率在四个数据集上从通用 LLM 的 16.40%–39.06% 提升到微调后的 82.75%–89.16%：CICIDS2017 为 29.68%→89.16%，CICIoT2023 为 16.40%→82.75%，Malware 为 39.06%→87.54%，APT 为 28.90%→88.67%。
4. 扩展集上检测 F1 均高于 0.92，但表 4 的单项 AdvTG ASR 包含 33.59%（CIC-APT-IIoT2024/DeepLog）和 39.70%（APT2024/DeepLog），因此“超过 40%”只能理解为论文总体叙述或多数配置，不能覆盖表中的每个配置。
5. 在附录 F.1 的 ChatGPT/ChatGPTs 目标上，AdvTG ASR 约 15.57%–16.64%，明显低于针对普通 DL 检测器的结果；这支持作者关于 LLM 目标更难攻击的观察。
6. 附录 F.2 报告了图像模型与文本模型之间的迁移热图。原文指出非对角区域仍有较高 ASR，但 MinerU 未稳定抽取热图中的完整数值，不能补写具体迁移率。

#### 4.3 优势和局限

优势是：一是把攻击输出映射回完整 HTTP 报文，二是同时覆盖字节图像和文本模型，三是用多奖励模型降低对单一特征捷径的依赖，四是微调后合规率有清晰提升。局限是：实验只涉及明文 HTTP 内容；加密后修改是否仍有效由作者明确列为未解决问题；功能保持主要通过固定字段和 RFC 结构检查体现，缺少真实服务回放或业务成功率；APT 和良性数据部分为作者自收集，外部复现依赖不可见的数据来源；没有报告 PPO 查询次数、生成延迟、GPU 成本、随机种子及完整超参数；当前本地资料也未给出官方代码仓库，代码状态记为 unknown。

### 5. 学习、复现与迁移

#### 5.1 复现关键步骤

1. 依照表 5 准备四个基础集和两个只测试的扩展集，提取 HTTP 包并明确良性/恶意标签；作者自收集的 APT 与热门网站流量需要单独记录来源和获取时间。
2. 复现字节归一化、二维 reshape/截断补零和文本 token 化两条特征管线，训练 TextCNN、DeepLog、BERT、MalTraffic、RBRN、DeepMal，并保存概率输出。
3. 以 Meta-Llama-3-8B 做 LoRA 领域微调，prompt 中显式分离功能字段与待生成的非功能字段。
4. 用多个检测器概率计算式 (6) 奖励，在 PPO 中以 SFT 模型为参考策略加入式 (7) 的 KL 项；每轮保存生成包、目标分数和查询次数。
5. 用附录 E 的 HTTP 检查器筛掉不合规包，再在未参与训练/微调的扩展集上计算 ASR，并报告协议合规率和真实功能回放结果（后者是论文未覆盖的必要补充）。

#### 5.2 已给出的实现信息与缺口

| 项目 | 原文信息 | 缺口 |
|---|---|---|
| 基座模型 | Meta-Llama-3-8B | LoRA rank、量化和 tokenizer 配置未说明 |
| 微调 | PEFT/LoRA | 数据规模、轮数、学习率、batch 未说明 |
| RL | PPO；SFT 模型作参考；多模型负 CE + KL | clip、GAE、KL 系数、采样与查询预算未说明 |
| 检测器 | 六种模型；另有 R-T/三种 Transformer 目标 | 具体层数、输入长度和训练种子未完整说明 |
| 合规 | RFC 结构检查、功能字段固定 | 真实业务可用性和服务端回放未验证 |
| 开源 | 本地笔记与原文未给出官方代码链接 | unknown |

#### 5.3 迁移价值

可迁移的机制是“固定任务关键字段、在可变字段空间做生成、用多个异构模型反馈”，可用于测试日志、协议字段和结构化文本检测器的捷径依赖。迁移到加密流量只能作为待验证假设：论文没有证明 payload 修改在加密后仍保留语义、也没有同时改变包序列特征的实验。

### 6. 总结

**核心思想：LLM与强化学习生成合规对抗流量。**

速记版 pipeline：

1. 用字节图像和文本特征训练六个黑盒目标检测器。
2. 用 HTTP 数据和功能字段 prompt 微调 Llama-3-8B。
3. 用多检测器负交叉熵和 KL 约束做 PPO 对抗生成。
4. 只改非功能字段，保留功能字段并执行 RFC 合规检查。
5. 在基础集和未见扩展集上报告 ASR、合规率和迁移效果。

### 7. 知识层联动建议（不直接改共享总表）

- 可在 `05-methods/` 增加“LLM 生成式流量对抗”方法条目，记录功能保持、协议合规、多模型奖励和 PPO 四个组成部分。
- 可在 `06-tasks/malicious-traffic-detection.md` 与 `09-claims/` 增加一条证据：payload 检测器的鲁棒性评估必须区分统计/序列攻击与内容攻击，并报告协议合规和真实功能保持。
- 可在 `12-research-fronts/payload-learnability.md` 追加“内容攻击能否迁移到加密流量”作为未解决问题；当前论文证据方向为中性/未验证，不应写成支持结论。
- 以上为联动建议，本次未修改共享方法表、任务表、Claims 总表或研究前沿页。

### 8. 证据范围

- 直接证据：`02-parsed-markdown/2025-WWW-AdvTG__An_Adversarial_Traffic_Generation_Framework_to_Deceive_DL-Based_Malicious_Traffic_Detection_Models.md` 的 §1–§10、附录 A–F，覆盖公式 (1)–(8)、表 2–7、算法 1 和数据集说明。
- 交叉核对：对应本地 PDF `00-inbox/PDFs/2025-WWW-AdvTG__An_Adversarial_Traffic_Generation_Framework_to_Deceive_DL-Based_Malicious_Traffic_Detection_Models.pdf` 已存在；本次未修改原 PDF 或 MinerU 原文。
- 证据限制：MinerU 对若干数学变量、图中数值和表格结构有字符损坏；未从损坏位置推断缺失数值。

## 历史自动入库段落说明

- 本笔记前部的自动入库、摘要级或待核验段落是入库时的历史快照，按规范保留以避免删除原始记录。
- 本次新增的深度分析段落、证据记录和局限说明优先；历史段落中的“待深读/待核验”状态不代表当前分析尚未完成。

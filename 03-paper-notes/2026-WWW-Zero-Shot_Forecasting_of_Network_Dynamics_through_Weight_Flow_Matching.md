---
type: paper
title_original: "Zero-Shot Forecasting of Network Dynamics through Weight Flow Matching"
title_cn: ""
authors: ["ShiHe Zhou", "Ruikun Li", "Huandong Wang", "Yong Li"]
year: 2026
venue: WWW
doi: "10.1145/3774904.3792722"
url: "https://doi.org/10.1145/3774904.3792722"
pdf: "00-inbox/PDFs/2026-WWW-Zero-Shot_Forecasting_of_Network_Dynamics_through_Weight_Flow_Matching.pdf"
mineru_md: "02-parsed-markdown/2026-WWW-Zero-Shot_Forecasting_of_Network_Dynamics_through_Weight_Flow_Matching.md"
status: deep-analyzed
reading_level: L3
research_area: ["network dynamics forecasting", "spatiotemporal graph learning", "zero-shot generalization"]
task: ["network dynamics forecasting"]
method: ["expert-weight manifold", "weight tokenizer", "variational autoencoder", "conditional flow matching"]
dataset: ["Hill", "Epidemic", "Twitter", "Collab", "FitzHugh-Nagumo"]
code: "yes: https://github.com/tsinghua-fib-lab/FNFM"
relevance: medium
created: "2026-09-29"
updated: "2026-10-10"
---

# Zero-Shot Forecasting of Network Dynamics through Weight Flow Matching

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Zero-Shot Forecasting of Network Dynamics through Weight Flow Matching |
| 年份 | 2026 |
| 会议/期刊 | WWW |
| PDF | [[2026-WWW-Zero-Shot_Forecasting_of_Network_Dynamics_through_Weight_Flow_Matching.pdf]] |
| MinerU Markdown | [[2026-WWW-Zero-Shot_Forecasting_of_Network_Dynamics_through_Weight_Flow_Matching.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
F<sub>orecas</sub>ti<sub>ng s</sub>t<sub>a</sub>t<sub>e evo</sub>l<sub>u</sub>ti<sub>on o</sub>f <sub>ne</sub>t<sub>wor</sub>k <sub>sys</sub>t<sub>ems, suc</sub>h <sub>as</sub> th<sub>e sprea</sub>d <sub>o</sub>f i<sub>n</sub>f<sub>orma</sub>ti<sub>on on soc</sub>i<sub>a</sub>l <sub>ne</sub>t<sub>wor</sub>k<sub>s,</sub> i<sub>s s</sub>i<sub>gn</sub>ifi<sub>can</sub>t f<sub>or e</sub>f<sub>ec</sub>ti<sub>ve po</sub>l ic<sub>y</sub> interventions and resource mana<sub>g</sub>ement. However<sub>,</sub> the under l<sub>y</sub>in<sub>g p</sub>ro<sub>p</sub>a<sub>g</sub>ation d<sub>y</sub>namics constantl<sub>y</sub> shift with new to<sub>p</sub>ics or <sub>even</sub>t<sub>s, w</sub>hi<sub>c</sub>h <sub>are mo</sub>d<sub>e</sub>l<sub>e</sub>d <sub>as c</sub>h<sub>ang</sub>i<sub>ng coe</sub>fi<sub>c</sub>i<sub>en</sub>t<sub>s o</sub>f th<sub>e un</sub>d<sub>er-</sub> l<sub>y</sub>in<sub>g</sub> d<sub>y</sub>namics. Dee<sub>p</sub> learnin<sub>g</sub> models stru<sub>gg</sub>le to ada<sub>p</sub>t to these <sub>ou</sub>t<sub>-o</sub>f<sub>-</sub>di<sub>s</sub>t<sub>r</sub>ib<sub>u</sub>ti<sub>on s</sub>hift<sub>s w</sub>ith<sub>ou</sub>t <sub>ex</sub>t<sub>ens</sub>i<sub>ve new</sub> d<sub>a</sub>t<sub>a an</sub>d <sub>re</sub>t<sub>ra</sub>i<sub>n</sub> in<sub>g</sub>. To address this<sub>,</sub> we <sub>p</sub>resent Zero-Shot Forecastin<sub>g</sub> of Network D<sub>y</sub>namics throu<sub>g</sub>h Wei<sub>g</sub>ht Flow Matchin<sub>g</sub> (FNFM), a <sub>g</sub>enerative, <sub>coe</sub>fi<sub>c</sub>i<sub>en</sub>t<sub>-con</sub>diti<sub>one</sub>d f<sub>ramewor</sub>k th<sub>a</sub>t <sub>genera</sub>t<sub>es</sub> d<sub>ynam</sub>i<sub>c mo</sub>d<sub>e</sub>l <sub>we</sub>i<sub>g</sub>ht<sub>s</sub> f<sub>or an unseen</sub> t<sub>arge</sub>t <sub>coe</sub>fi<sub>c</sub>i<sub>en</sub>t<sub>, ena</sub>bli<sub>ng zero-s</sub>h<sub>o</sub>t f<sub>ore-</sub> <sub>cas</sub>tin<sub>g.</sub> O<sub>u</sub>r fr<sub>a</sub>m<sub>ewo</sub>rk <sub>u</sub>tiliz<sub>es a</sub> V<sub>a</sub>ri<sub>a</sub>ti<sub>o</sub>n<sub>a</sub>l En<sub>co</sub>d<sub>e</sub>r t<sub>o su</sub>mm<sub>a</sub>riz<sub>e</sub> th<sub>e</sub> f<sub>orecas</sub>t<sub>er we</sub>i<sub>g</sub>ht<sub>s</sub> t<sub>ra</sub>i<sub>ne</sub>d i<sub>n o</sub>b<sub>serve</sub>d <sub>env</sub>i<sub>ronmen</sub>t<sub>s</sub> i<sub>n</sub>t<sub>o com-</sub> <sub>p</sub>act latent tokens. A Conditional Flow Matchin<sub>g</sub> (CFM) module then learns a continuous trans<sub>p</sub>ort from a sim<sub>p</sub>le

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
- 主题线索：tor, transformer。
- 摘要证据：F<sub>orecas</sub>ti<sub>ng s</sub>t<sub>a</sub>t<sub>e evo</sub>l<sub>u</sub>ti<sub>on o</sub>f <sub>ne</sub>t<sub>wor</sub>k <sub>sys</sub>t<sub>ems, suc</sub>h <sub>as</sub> th<sub>e sprea</sub>d <sub>o</sub>f i<sub>n</sub>f<sub>orma</sub>ti<sub>on on soc</sub>i<sub>a</sub>l <sub>ne</sub>t<sub>wor</sub>k<sub>s,</sub> i<sub>s s</sub>i<sub>gn</sub>ifi<sub>can</sub>t f<sub>or e</sub>f<sub>ec</sub>ti<sub>ve po</sub>l ic<sub>y</sub> interventions and resource mana<sub>g</sub>ement. However<sub>,</sub> the under l<sub>y</sub>in<sub>g p</sub>ro<sub>p</sub>a<sub>g</sub>ation d<sub>y</sub>namics constantl<sub>y</sub> shift with new to<sub>p</sub>ics or <sub>even</sub>t<sub>s, w</sub>hi<sub>c</sub>h <sub>are mo</sub>d<sub>e</sub>l<sub>e</sub>d <sub>as c</sub>h<sub>ang</sub>i<sub>ng coe</sub>fi<sub>c</sub>i<sub>en</sub>t<sub>s o</sub>f th<sub>e un</sub>d<sub>er-</sub> l<sub>y</sub>in<sub>g</sub> d<sub>y</sub>namics. Dee<sub>p</sub> learnin<sub>g</sub> models stru<sub>gg</sub>le to ada<sub>p</sub>t to these <sub>ou</sub>t<sub>-o</sub>f<sub>-</sub>di<sub>s</sub>t<sub>r</sub>ib<sub>u</sub>ti<sub>on s</sub>hift<sub>s w</sub>ith<sub>ou</sub>t <sub>ex</sub>t<sub>ens</sub>i<sub>ve new</sub> d<sub>a</sub>t<sub>a an</sub>d <sub>re</sub>t<sub>ra</sub>i<sub>n</sub> in<sub>g</sub>. To address this<sub>,</sub> we <sub>p</sub>resent Zero-Shot Forecastin<sub>g</sub> of Network D<sub>y</sub>namics throu<sub>g</sub>h Wei<sub>g</sub>ht Flow Matchin<sub>g</sub> (FNFM), a <sub>g</sub>enerative, <sub>coe</sub>fi<sub>c</sub>i<sub>en</sub>t<sub>-con</sub>diti<sub>one</sub>d f<sub>ramewor</sub>k th<sub>a</sub>t <sub>genera</sub>t<sub>es</sub> d<sub>ynam</sub>i<sub>c mo</sub>d<sub>e</sub>l <sub>we</sub>i<sub>g</sub>ht<sub>s</sub> f<sub>or an unseen</sub> t<sub>arge</sub>t <sub>coe</sub>fi<sub>c</sub>i<

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：未检测到明确 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


## 深度分析（并行深度分析更新 2026-09-29）

### 方法、实验与证据
FNFM不直接预测轨迹，而是通过weight flow matching为给定环境生成专用预测器权重；五个数据集、RMSE、lookback=50、horizon=50，跨环境分割避免重叠，摘要称多数OOD场景优于基线。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。


## 深度分析（L3 补充，2026-10-09）

### 3. 研究问题与任务边界

FNFM 研究的是网络化动态系统在环境系数变化下的 zero-shot 多步预测。给定同一网络拓扑 `A` 和由环境系数 `e` 决定的 ODE `dX(t)/dt=F(X(t),A,e)`，训练环境与未见环境严格不重叠；模型观察目标环境前 `H` 个状态，预测未来 `N` 个状态。论文关注的是“动力学系数变化导致传播轨迹分布外偏移”，不是网络流量分类或包级仿真。实验默认 `H=N=50`，以非标准化轨迹 RMSE 评价（§2、§4.1–§4.2）。

核心假设是：每个环境训练出的专用预测器权重并非无结构孤立点，而是在环境系数驱动下形成低维、连续的权重流形。若能把专家模型权重压缩为结构化 latent，再学习“环境系数 → latent 权重”的连续 transport，就能为未见系数生成专用预测器，而不在测试时重新梯度训练。这个假设由 latent PCA 可视化、CFM/无条件消融和跨系数测试支持，但仍依赖拓扑和动力学族在训练/测试间共享。

### 4. FNFM 方法设计

#### 4.1 三阶段 Pipeline

| 步骤 | 输入 | 操作 | 输出 |
|---|---|---|---|
| 1. 专家权重收集 | 每个 seen environment 的轨迹、拓扑、系数 | 为每个环境独立训练 STGCN（或兼容的 forecaster），用多步 MSE 得到 `θ^(e)` | 专家权重—环境系数配对集合 |
| 2. Weight tokenizer | 各层卷积/线性权重 | 卷积层按输出 channel 展平为 token；线性层按输出 neuron 连同 bias 形成 token；按层保持顺序 | 结构化 weight-token sequence |
| 3. Weight VAE | token sequence | 层级 MLP 映射到统一 `d_model`，Transformer encoder 得到 `qφ(z|w)`；decoder 重建原 token，ELBO 同时优化重建和 KL | 32 维 latent（配置见 Appendix F） |
| 4. Conditional Flow Matching | latent `z^(e)`、环境系数 `e` | 从高斯 `z0` 到目标 latent 学习条件向量场，AdaLN 将系数注入 Transformer | `vξ(z,t,e)` |
| 5. Zero-shot synthesis | 新系数 `e_new` | 解 `dz/dt=vξ(z,t,e_new)` 的 ODE（前向 Euler），VAE decoder 把 `z_N` 还原为预测器权重 | 未见环境的专用 `ŵ_new` |
| 6. Forecasting | 历史窗口、拓扑 | 用生成权重运行 STGCN，输出未来 50 步状态 | 网络动态轨迹预测 |

#### 4.2 关键公式与机制

CFM 使用直线高斯桥 `p_t=N((1−t)x0+t x1, σ²)`，目标速度为常向量 `u_t=x1−x0`；训练损失是 `||vξ((1−t)x0+t x1,t,e)−(x1−x0)||²`（Eq. 1–3）。FNFM 把 `x1` 换成环境 `e` 对应的专家 latent `z^(e)`，推理时从 `N(0,I)` 数值积分到 `t=1`，再由 decoder 生成权重（Eq. 11–14）。

Weight tokenizer 保留网络层和输出单元的结构归纳偏置：卷积核每个输出 channel 为一个 token，线性层每个输出 neuron 的输入权重加 bias 为一个 token；简单 flatten 消融会破坏这种结构。VAE 的 KL 项把离散专家权重压到可插值的平滑 latent，CFM 再学习环境系数到 manifold 点的条件 transport。

### 5. 实验、数据和结果

#### 5.1 数据集与 OOD 划分

论文覆盖五类网络化动力学：Hill/Barabási–Albert（BA）合成网络、Epidemic（欧洲道路网络上的 SIS）、Twitter（社会传播 SIS）、Collab（科学合作网络 SIS）和 FHN/BA（FitzHugh–Nagumo）。主要 Table 1 报告前四类，FHN 结果在 Appendix B Table 3。环境由动力学系数定义，训练/验证/测试环境不重叠；OOD 测试系数外推到训练范围之外或落入被排除的 transition 区域。节点/边规模和模拟长度来自 Appendix C Table 4：Hill 300/1475/600 s，Epidemic 1174/1417/50 s，Twitter 761/1029/50 s，Collab 1511/4273/10 s，FHN 300/596/300 s。

#### 5.2 基线与指标

基线包含 STGCN、STEP、无参数 STGFSL、扩散生成 GPD、参数扩散 Paragon，以及可访问目标环境数据的 One-per-Env STGCN oracle。所有报告是 5 个独立随机种子的平均 ± 标准差；指标是非标准化轨迹 RMSE。主训练环境采用 batch size 64、500 epochs、learning rate 1e-4；FNFM 权重 VAE 为 2 层/8 heads、`d_model=128`、32 维 latent、KL 权重 1e-6，CFM 为 4 层/2 heads、dropout 0.1；GPU 为 NVIDIA RTX 2080 Ti（Appendix E/F）。

#### 5.3 Table 1 关键结果

| 数据集 | FNFM In-domain | FNFM OOD | 与基线的证据 | 解释 |
|---|---:|---:|---|---|
| Hill | 13.8942±2.4240 | 8.5595±0.4594 | STGCN 14.4060/8.2359；STEP 15.4436/13.6226；One-per-Env 11.2409/8.5127 | OOD 低于 STGCN、优于 STEP，但仍高于 oracle |
| Epidemic | 0.0562±0.0071 | 0.0561±0.0059 | STEP 0.0639/0.0609；One-per-Env 0.0496/0.0538 | 接近 oracle，低于主要基线 |
| Twitter | 0.0579±0.0081 | 0.0512±0.0048 | STEP 0.0612/0.0593；One-per-Env 0.0364/0.0326 | OOD 优于 STGCN/STEP，但不及 oracle |
| Collab | 0.0475±0.0036 | 0.0244±0.0021 | STEP 0.0556/0.0303；One-per-Env 0.0461/0.0229 | 接近 oracle，OOD 优于大多数基线 |

论文把“跨近乎所有 in/out 场景优于基线”作为主结论，但表中 Hill OOD 的 STGCN 为 8.2359，低于 FNFM 8.5595，说明该结论应改写为“多数场景优于基线，特定场景存在例外”。“near-optimal”也只能相对 oracle 和这些数据集成立。

#### 5.4 消融、案例和鲁棒性

- **Tokenizer**：去掉结构化 tokenizer 后，Hill RMSE 从 13.8942/8.5595 变为 17.3381/11.1205，Collab 变为 0.05134/0.0359。
- **Condition**：去掉环境系数条件后，Hill 27.6437/17.5250，Collab 0.0670/0.0306，说明系数是生成专用权重的必要条件。
- **VAE**：直接在 raw flattened weights 上做 CFM，Hill RMSE 升至 118.9763/142.2945，支持 latent 压缩与正则化的作用；Collab 也恶化至 0.0495/0.0340。
- **CFM vs DDPM**：固定 50 个采样步，CFM 在 Hill/Collab 的 in/out RMSE 均低于 DDPM；例如 Hill in 13.8942 vs 18.5735，Collab OOD 0.0244 vs 0.0529（Table 2）。
- **Collab transition case**：只用 Declining 和 Active 两端训练，把整个临界 transition 区域留作未见测试，FNFM 的传播规模和轨迹与 ground truth 接近（Fig. 4）。
- **鲁棒性**：训练环境只保留 10% 时仍保持较低 RMSE；对环境系数加入 0–20% 高斯噪声时，误差平滑增长，20% 噪声下增幅小于 16%（Fig. 5）。

### 6. 局限性与复现建议

1. “zero-shot”是在已知拓扑、已知动力学方程族和可观测环境系数下生成预测器权重；论文没有验证新拓扑、新方程族或系数语义错误的场景。
2. 专家权重收集仍需为每个 seen environment 单独训练 STGCN，训练成本被前置到数据构建阶段；推理免梯度优化不等于整个流程无需训练。
3. OOD 主要是系数插值/外推和 Collab transition 区域，未覆盖真实网络测量噪声、拓扑变化、非平稳系数或长时滚动误差累积。
4. Table 1 的“多数 SOTA”结论有 Hill OOD 例外，且 One-per-Env 使用目标环境数据，不能与 zero-shot 条件直接等价比较。
5. FHN 只在附录报告，主表四个数据集；不同数据集的 RMSE 数值量纲不同，跨数据集绝对值不可直接比较。
6. 论文公开代码地址为 `https://github.com/tsinghua-fib-lab/FNFM`；复现需同时固定环境系数范围、Euler 求解步数、专家模型训练和 5-run split。

复现顺序：先用 Hill/Collab 重建专家 STGCN 和 50→50 预测窗口；再训练 VAE/CFM，比较 50-step Euler 与 DDPM；随后严格按 Appendix C 的不重叠系数范围做 in/OOD；最后复现去 tokenizer、去 condition、去 VAE 以及 Collab transition 案例。报告时保留 oracle 与 zero-shot 的证据边界。

### 7. 总结与证据记录

> 在专家权重流形上做条件 flow matching，零样本生成新环境预测器。

速记 Pipeline：每环境训练专家 → 结构化拆分权重 token → VAE 压缩 latent → CFM 学习系数条件 transport → Euler 生成新环境权重 → 多步网络动力学预测。

| 结论 | 原始资料位置 |
|---|---|
| ODE 任务与不重叠环境定义 | raw Markdown §2.1 |
| tokenizer、VAE、CFM 和 Euler 推理 | raw Markdown §3.1–§3.4、Eq. 4–14 |
| 五类数据集与系数划分 | raw Markdown §4.1–§4.5、Appendix C |
| 主表、消融、案例、鲁棒性 | raw Markdown Table 1–2、§4.6–§4.9 |
| 代码与硬件/超参数 | raw Markdown Abstract、Appendix E/F |

本次仅升级该论文笔记，不自动修改 04–09 层共享表。

## 历史自动入库段落说明

- 本笔记前部的自动入库、摘要级或待核验段落是入库时的历史快照，按规范保留以避免删除原始记录。
- 本次新增的深度分析段落、证据记录和局限说明优先；历史段落中的“待深读/待核验”状态不代表当前分析尚未完成。

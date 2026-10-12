---
type: paper
title_original: "Cardinality is Not Enough: Super Host Detection via Segmented Cardinality Estimation"
title_cn: "基数并非全部：基于分段基数估计的超级主机检测"
authors: [Yilin Zhao, Jiawei Huang, Xianshi Su, Weihe Li, Xin Li, Yan Liu, Jiacheng Xie, Qichen Su, Jin Ye, Wanchun Jiang, Jianxin Wang]
year: 2026
venue: "WWW 2026"
doi: "10.1145/3774904.3792071"
url: "https://doi.org/10.1145/3774904.3792071"
pdf: "00-inbox/PDFs/2026-WWW-Cardinality_is_Not_Enough__Super_Host_Detection_via_Segmented_Cardinality_Estimation.pdf"
mineru_md: "02-parsed-markdown/2026-WWW-Cardinality_is_Not_Enough__Super_Host_Detection_via_Segmented_Cardinality_Estimation.md"
status: deep-analyzed
reading_level: L3
research_area: ["network measurement", "super-host detection", "programmable data plane"]
task: ["super-spreader detection", "super-receiver detection"]
method: ["halved-segment hashing", "bitmap cardinality estimation", "P4 sketch"]
dataset: ["UNSW-NB15", "MAWI2021", "CAIDA2016", "SDN-DDoS"]
code: "https://github.com/Elaine-codebase/SegSketch-Repository; artifact https://doi.org/10.5281/zenodo.17284567"
relevance: high
created: "2026-09-29"
updated: "2026-10-10"
---

# Cardinality is Not Enough: Super Host Detection via Segmented Cardinality Estimation

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Cardinality is Not Enough: Super Host Detection via Segmented Cardinality Estimation |
| 年份 | 2026 |
| 会议/期刊 | WWW |
| PDF | [[2026-WWW-Cardinality_is_Not_Enough__Super_Host_Detection_via_Segmented_Cardinality_Estimation.pdf]] |
| MinerU Markdown | [[2026-WWW-Cardinality_is_Not_Enough__Super_Host_Detection_via_Segmented_Cardinality_Estimation.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
A<sub>ccura</sub>t<sub>e</sub>l<sub>y</sub> d<sub>e</sub>t<sub>ec</sub>ti<sub>ng super</sub> h<sub>os</sub>t th<sub>a</sub>t <sub>es</sub>t<sub>a</sub>bli<sub>s</sub>h<sub>es connec</sub>ti<sub>ons</sub> t<sub>o</sub> a lar<sub>g</sub>e number of distinct <sub>p</sub>eers is si<sub>g</sub>nificant for miti<sub>g</sub>atin<sub>g</sub> web attacks and ensurin<sub>g</sub> hi<sub>g</sub>h <sub>q</sub>ualit<sub>y</sub> of web service. Existin<sub>g</sub> sketch b<sub>ase</sub>d <sub>approac</sub>h<sub>es es</sub>ti<sub>ma</sub>t<sub>e</sub> th<sub>e num</sub>b<sub>er o</sub>f di<sub>s</sub>ti<sub>nc</sub>t <sub>connec</sub>ti<sub>ons</sub> <sub>ca</sub>ll<sub>e</sub>d fl<sub>ow</sub> <sub>car</sub>di<sub>na</sub>lit<sub>y</sub> <sub>accor</sub>di<sub>ng</sub> t<sub>o</sub> f<sub>u</sub>ll IP <sub>a</sub>dd<sub>resses,</sub> <sub>w</sub>hil<sub>e</sub> i<sub>gnor</sub>i<sub>ng</sub> th<sub>e</sub> f<sub>ac</sub>t th<sub>a</sub>t <sub>a ma</sub>li<sub>c</sub>i<sub>ous or v</sub>i<sub>c</sub>ti<sub>m super</sub> h<sub>os</sub>t <sub>o</sub>ft<sub>en commun</sub>i<sub>ca</sub>t<sub>es</sub> with hosts within the same subnet<sub>,</sub> resultin<sub>g</sub> in hi<sub>g</sub>h false <sub>p</sub>ositive <sub>ra</sub>t<sub>es</sub> <sub>an</sub>d l<sub>ow</sub> <sub>accuracy.</sub> Th<sub>oug</sub>h hi<sub>erarc</sub>hi<sub>ca</sub>l<sub>-s</sub>t<sub>ruc</sub>t<sub>ure</sub> b<sub>ase</sub>d <sub>ap</sub> <sub>proac</sub>h<sub>es cou</sub>ld <sub>cap</sub>t<sub>ure</sub> fl<sub>ow car</sub>di<sub>na</sub>lit<sub>y</sub> i<sub>n su</sub>b<sub>ne</sub>t<sub>,</sub> th<sub>ey</sub> i<sub>n</sub>h<sub>eren</sub>tl<sub>y</sub> <sub>su</sub>f<sub>er</sub> f<sub>rom</sub> hi<sub>g</sub>h <sub>memory usage.</sub> T<sub>o a</sub>dd<sub>ress</sub> th<sub>ese</sub> li<sub>m</sub>it<sub>a</sub>ti<sub>ons, we</sub> <sub>p</sub>ro<sub>p</sub>ose Se<sub>g</sub>Sketch<sub>,</sub> a se<sub>g</sub>mented cardinalit<sub>y</sub> estimation a<sub>pp</sub>roach that em<sub>p</sub>lo<sub>y</sub>s a li<sub>g</sub>htwei<sub>g</sub>ht halved-se<sub>g</sub>ment hashin<sub>g</sub> strate<sub>gy</sub> to in f<sub>er common pre</sub>fi<sub>x</sub> l<sub>eng</sub>th<sub>s o</sub>f IP <sub>a</sub>dd<sub>resses, an</sub>d <sub>es</sub>ti<sub>ma</sub>t<sub>es car</sub>di<sub>na</sub>lit<sub>y</sub> <sub>w</sub>ithi<sub>n su</sub>b<sub>ne</sub>t t<sub>o en</sub>h<sub>ance</sub> d<sub>e</sub>t<sub>ec</sub>ti<sub>on accuracy un</sub>d<sub>er cons</sub>t<sub>ra</sub>i<sub>ne</sub>d memor<sub>y</sub> size.

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
- 主题线索：dns, tor, adversarial。
- 摘要证据：A<sub>ccura</sub>t<sub>e</sub>l<sub>y</sub> d<sub>e</sub>t<sub>ec</sub>ti<sub>ng super</sub> h<sub>os</sub>t th<sub>a</sub>t <sub>es</sub>t<sub>a</sub>bli<sub>s</sub>h<sub>es connec</sub>ti<sub>ons</sub> t<sub>o</sub> a lar<sub>g</sub>e number of distinct <sub>p</sub>eers is si<sub>g</sub>nificant for miti<sub>g</sub>atin<sub>g</sub> web attacks and ensurin<sub>g</sub> hi<sub>g</sub>h <sub>q</sub>ualit<sub>y</sub> of web service. Existin<sub>g</sub> sketch b<sub>ase</sub>d <sub>approac</sub>h<sub>es es</sub>ti<sub>ma</sub>t<sub>e</sub> th<sub>e num</sub>b<sub>er o</sub>f di<sub>s</sub>ti<sub>nc</sub>t <sub>connec</sub>ti<sub>ons</sub> <sub>ca</sub>ll<sub>e</sub>d fl<sub>ow</sub> <sub>car</sub>di<sub>na</sub>lit<sub>y</sub> <sub>accor</sub>di<sub>ng</sub> t<sub>o</sub> f<sub>u</sub>ll IP <sub>a</sub>dd<sub>resses,</sub> <sub>w</sub>hil<sub>e</sub> i<sub>gnor</sub>i<sub>ng</sub> th<sub>e</sub> f<sub>ac</sub>t th<sub>a</sub>t <sub>a ma</sub>li<sub>c</sub>i<sub>ous or v</sub>i<sub>c</sub>ti<sub>m super</sub> h<sub>os</sub>t <sub>o</sub>ft<sub>en commun</sub>i<sub>ca</sub>t<sub>es</sub> with hosts within the same subnet<sub>,</sub> resultin<sub>g</sub> in hi<sub>g</sub>h false <sub>p</sub>ositive <sub>ra</sub>t<sub>es</sub> <sub>an</sub>d l<sub>ow</sub> <sub>accuracy.</sub> Th<sub>oug</sub>h hi<sub>erarc</sub>hi<sub>ca</sub>l<sub>-s</sub>t<sub>ruc</sub>t<sub>ure</sub> b<sub>ase</sub>d <sub>ap</sub> <sub>proac</sub>h<sub>es cou</sub>ld <sub>cap</sub>t<sub>ure</sub> fl<sub>ow car</sub>di<sub>na</sub>lit<sub>y</sub> i<sub>n su</sub>b<sub>ne</sub>t<sub>,</sub> th<sub>ey</sub> i<sub>n</sub>h<sub>eren</sub>tl<sub>y</sub> <sub>su</sub>f<sub>er</sub> f<sub>rom</sub> hi<sub>g</sub>h <sub>memory usage.</sub> T<sub>o a</sub>dd<sub>ress</sub> th<sub>ese</sub> li<sub>m</sub>it<sub>a</sub

### 方法机制
(2) S<sub>p</sub>readSketch [40] stores candidate host ke<sub>y</sub>, Multi-Resolution Bitma<sub>p</sub> for cardinalit<sub>y</sub> estimation<sub>,</sub> and the maximum number of leadin<sub>g</sub> zero bits in the IP hash strin<sub>g</sub> for re<sub>p</sub>lacement decision. After <sub>eac</sub>h <sub>epoc</sub>h<sub>,</sub> it t<sub>raverses</sub> <sub>a</sub>ll b<sub>uc</sub>k<sub>e</sub>t<sub>s</sub> <sub>an</sub>d <sub>repor</sub>t<sub>s</sub> <sub>any</sub> h<sub>os</sub>t <sub>w</sub>h<sub>ose</sub> <sub>es</sub>ti<sub>ma</sub>t<sub>e</sub>d <sub>car</sub>di<sub>na</sub>lit<sub>y</sub> <sub>excee</sub>d<sub>s</sub> th<sub>e</sub> th<sub>res</sub>h<sub>o</sub>ld <sub>as</sub> <sub>a</sub> <sub>super</sub> h<sub>os</sub>t<sub>.</sub> (3) RHHH [5] maintains a multi-level <sub>p</sub>refix hierarch<sub>y</sub>, where <sub>eac</sub>h l<sub>ayer</sub> t<sub>rac</sub>k<sub>s</sub> fl<sub>ows</sub> <sub>w</sub>ith <sub>a</sub> <sub>spec</sub>ifi<sub>c</sub> <sub>pre</sub>fi<sub>x</sub> l<sub>eng</sub>th<sub>,</sub> <sub>an</sub>d <sub>uses</sub> Li<sub>near</sub> Countin<sub>g</sub> to estimate cardinalit<sub>y</sub> within the corres<sub>p</sub>ondin<sub>g</sub> subnet. Platform. The experiments are conducted on a Mac laptop with an Intel Core i7 CPU r<sub>u</sub>nnin<sub>g</sub> at 2.30GHz<sub>,</sub> <sub>p</sub>ro<sub>v</sub>idin<sub>g</sub> fo<sub>u</sub>r <sub>p</sub>h<sub>y</sub>sical cores and su<sub>pp</sub>ortin<sub>g</sub> simultaneous multithreadin<sub>g</sub>. It is e<sub>q</sub>ui<sub>pp</sub>ed <sub>w</sub>ith 32GB <sub>o</sub>f RAM<sub>.</sub> E<sub>ac</sub>h CPU <sub>co</sub>r<sub>e</sub> in<sub>co</sub>r<sub>po</sub>r<sub>a</sub>t<sub>es a</sub> m<sub>u</sub>lti-l<sub>eve</sub>l <sub>cac</sub>h<sub>e</sub> hierarch<sub>y</sub> that includes a 64KB L

### 实验与结果
实验段落未稳定提取；不补造数据集、baseline、指标或数值。

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：未检测到明确 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


### 并行深度分析（2026-09-29）
- 方法/问题：The work argues full-IP flow cardinality is insufficient for super-host detection and proposes segmented cardinality estimation to preserve peer-group structure. Missing: sketch algorithm, memory/error analysis, workloads, baselines and detection gains.
- 证据边界：以上仅使用对应 MinerU 解析稿摘要及可稳定提取段落；未提取到的数值、数据集、代码和参数均不作推断。
- 复现建议：先核对原文表格、附录、代码仓库和数据划分，再确定 L3/L4 复现。

---

## 8. L3 深度方法分析补充

### 8.1 方法动机与研究问题

超级传播者和超级接收者的共同特征是与大量不同 IP 建立连接，但“完整 IP 基数”会把同一子网内的攻击连接与跨网络的正常高连接主机混在一起。论文的经验研究在 UNSW-NB15 与 CAIDA2016 混合流量上比较 SpreadSketch、Couper 和 RHHH，观察到单层 sketch 的精度偏低，而层级方法虽能利用前缀却需要为多个可能的前缀长度维护估计器，受小内存限制。研究问题因此被限定为：在未知子网前缀、固定片上内存和线速处理条件下，能否同时估计共同前缀和该子网内的连接基数？

### 8.2 方法流程（输入→处理→输出）

| 步骤 | 输入 | 处理 | 输出/作用 |
|---|---|---|---|
| 1. 选择主机键 | 到达的源/目的 IP 对 | 超级传播者用源 IP 作为 host key；超级接收者改用目的 IP | 统一两类检测任务的更新入口 |
| 2. 桶定位 | host key | 用 r 个独立哈希函数定位候选桶；每个桶保存 host key、subnet bitmap、host bitmap | 在固定内存中保留候选主机 |
| 3. 共同前缀推断 | 目的/源 IP 的 G-bit 分段 | 对每个分段做二值哈希并递归折半 subnet bitmap；若同一分段一致则进入同一半，否则保留两半并停止该路径 | 得到共同前缀长度范围 |
| 4. 子网基数估计 | 推断的前缀与剩余 host address | 将剩余 host address 写入 host bitmap，用 Linear Counting 估计子网内不同 IP 数 | 得到 \hat C(x) |
| 5. 桶更新/替换 | 新 host 与已占用桶 | 空桶直接插入；键命中则更新；全满时选择估计基数最小的桶，以 `Pr = 1/(b·ln(b/z)+1)` 概率替换并清空旧 bitmap | 适应流量长尾并保留大候选 |
| 6. 周期查询 | 所有桶 | 若估计子网基数超过 `T(p)=θ·2^(32-p)` 则报告超级主机；默认 θ=0.5 | 输出超级传播者/接收者列表 |

### 8.3 核心机制与理论角色

- **Halved-segment hashing** 把未知前缀长度搜索成按 IP 分段的二叉选择过程；论文示例用 4 个 8-bit 分段说明当第三段出现差异时，可把共同前缀定位在 `[16,24)` 位区间。它不需要为每个可能前缀维护完整估计器。
- **Host-address hashing** 在推断出的子网内只哈希剩余主机地址，降低来自其他子网连接的碰撞污染；Linear Counting 用 bitmap 未置位比例估计不同地址数。
- **概率替换**按当前桶的子网基数保护大候选，避免简单替换把高基数攻击主机冲掉；替换时清空 subnet bitmap，防止旧主机前缀信息残留。
- **误差定理**把 Linear Counting 误差与“被错误归入目标子网的流数”分开，给出概率上界；第二个定理证明在同一条件下，host-address hashing 的期望误差小于 full-address hashing。解析稿中的变量符号部分缺失，公式细节以 PDF 为准。

### 8.4 与现有方法的本质区别

| 方法 | 主要统计对象 | 关键优势 | 主要代价/缺口 |
|---|---|---|---|
| SpreadSketch | 全 IP 流基数 + 多分辨率 bitmap | 单层、速度快 | 不区分同子网与跨网络连接，误报高 |
| Couper | 两层基数估计器 | 适应不平衡基数分布 | 仍主要估计完整地址，需双层更新 |
| RHHH | 多前缀层级估计 | 能表达子网结构 | 前缀未知时需多层，内存和碰撞成本高 |
| SegSketch | 分段推断前缀 + 子网内 host 基数 | 单个紧凑结构同时处理前缀和基数 | 依赖 IPv4 分段和 θ/G 参数，复杂结构由控制面辅助 |

### 8.5 实验设计与关键结果

**数据与实现。** 论文把 UNSW-NB15 的恶意超级主机流量与 MAWI2021、CAIDA2016 的匿名正常背景混合；由于后两者没有标签，攻击标签沿用 UNSW-NB15，论文明确说明这一构造用于保持与既有工作一致。默认 r=3、θ=0.5、Bob Hash 不同随机种子、G=4；比较 C++ 实现的 SpreadSketch、Couper 和 RHHH。实验平台为 2.30 GHz 四核 Intel i7、32 GB RAM、Ubuntu 18.04.3，并在 Wedge 100BF-32X Tofino 交换机上做 P4 原型。

**指标。** Precision、Recall、F1、Average Relative Error（ARE）和吞吐（Mpps）。超级传播者以源 IP 为键，超级接收者以目的 IP 为键。

| 场景 | 结果 | 证据位置 |
|---|---|---|
| 超级传播者，32 KB | F1 相对 SpreadSketch/Couper/RHHH 分别提高 2.73×/2.18×/8.04×；ARE 分别降低 86.08%/68.00%/87.20% | §5.2, Fig. 8 |
| 超级接收者，32 KB | F1 相对三基线提高 5.08×/4.17×/2.77× | §5.2, Fig. 9 |
| 攻击比例 1:20，64 KB | SegSketch 仍保持 F1=0.79、ARE=0.32 | §5.3, Fig. 11 |
| 参数 G | G=2/4 时前缀误差约 0.3；G=6/8 仍低于 1.5，最终取 G=4 | §5.4, Fig. 12 |
| bitmap 大小 | 总内存 32 KB 时 0.5 KB bitmap 的 F1=0.5，优于 0.75/1 KB；过小会增加同主机碰撞 | §5.4, Fig. 13 |
| 吞吐 | 在 32 KB 内存下约 28 Mpps（CAIDA 混合），MAWI 混合附录中仍保持最高 | §5.5, Fig. 14, Appendix B.4 |
| P4 资源 | SRAM 1.77%，Hash Distribution Unit 11.11%，各项资源均低于多数基线 | §6, Table 2 |

### 8.6 优势与局限

优势集中在**小内存、同子网攻击与线速处理同时存在**的场景：SegSketch 不需要预先知道前缀长度，也不必复制多层估计器，因而在 32 KB 预算下保持较高 F1 和约 28 Mpps 吞吐。

局限包括：方法针对 IPv4 32-bit 地址，IPv6 和非前缀型地址结构未评估；MAWI/CAIDA 的攻击标签通过 UNSW-NB15 注入，不能等同于真实线上攻击分布；θ、G 和 bitmap 大小仍需按流量/内存调参；对跨多个子网的分布式攻击，方法会退化为较弱的每主机基数估计；Tofino 不支持的复杂操作由控制面辅助，实际纯数据面能力需单独评估。

### 8.7 复现步骤与证据边界

1. 获取 UNSW-NB15、MAWI2021 与 CAIDA2016，并按论文做恶意/正常流量混合；保留原始标签来源与混合比例。
2. 按论文参数实现四个 C++ sketch：r=3、θ=0.5、G=4、Bob Hash 多种子；扫描 32/64/128/256/512 KB 总内存。
3. 对源键和目的键分别计算 Precision、Recall、F1、ARE 与 Mpps；复现 Fig. 8–14 的趋势后，再在 P4/Wedge 100BF-32X 上验证资源占用。
4. 复核 PDF 中被 MinerU 丢失的变量符号、图表数值与算法伪代码；不能仅依据当前解析稿恢复理论常数。

### 8.8 写作叙事与故事线分析

论文以“基数高不等于恶意”这一单一反例切入，先用经验研究证明完整 IP 基数的误报，再把“共同前缀”提升为新的统计对象。方法部分按“前缀推断→子网基数→桶替换→阈值报告”递进，理论部分先给误差界再比较两种哈希，实验按准确率、扩展性、参数和吞吐展开，最后用 P4 资源表完成部署闭环。可迁移写法是：先用一个混淆案例暴露统计量不足，再把额外结构信息设计成低成本 sketch，并用同一指标贯穿理论、软件和硬件实验。

## 9. 知识层联动建议（待总审计）

- 可向 `06-tasks/anomaly-detection.md` 或新建网络测量任务页补充“超级主机/子网基数检测”，并在 `08-comparisons/method-comparison-table.md` 单列 sketch、层级估计和分段估计的内存/准确率/吞吐。
- `10-outputs/` 不需更新；代码与 artifact 已在 frontmatter 中记录，具体可用性仍需按 Zenodo/仓库页面复核。
- 本次未修改共享知识层页面、总表或全局统计。

## 历史自动入库段落说明

- 本笔记前部的自动入库、摘要级或待核验段落是入库时的历史快照，按规范保留以避免删除原始记录。
- 本次新增的深度分析段落、证据记录和局限说明优先；历史段落中的“待深读/待核验”状态不代表当前分析尚未完成。

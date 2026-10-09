---
type: paper
title_original: "Robust and Invisible Flow Watermarking With Invertible Neural Network for Traffic Tracking"
title_cn: ""
authors: []
year: 2026
venue: TNSM
doi: unknown
url: unknown
pdf: "00-inbox/PDFs/2026-TNSM-Robust_and_Invisible_Flow_Watermarking_With_Invertible_Neural_Network_for_Traffic_Tracking.pdf"
mineru_md: "02-parsed-markdown/2026-TNSM-Robust_and_Invisible_Flow_Watermarking_With_Invertible_Neural_Network_for_Traffic_Tracking.md"
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

# Robust and Invisible Flow Watermarking With Invertible Neural Network for Traffic Tracking

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Robust and Invisible Flow Watermarking With Invertible Neural Network for Traffic Tracking |
| 年份 | 2026 |
| 会议/期刊 | TNSM |
| PDF | [[2026-TNSM-Robust_and_Invisible_Flow_Watermarking_With_Invertible_Neural_Network_for_Traffic_Tracking.pdf]] |
| MinerU Markdown | [[2026-TNSM-Robust_and_Invisible_Flow_Watermarking_With_Invertible_Neural_Network_for_Traffic_Tracking.md]] |

## 1. 一句话总结
> 基于 MinerU 提取结果的待深读论文记录；具体贡献需结合全文核验。

## 2. 摘要原文
—This paper introduces an innovative blind flow watermarking framework on the basis of Invertible Neural Network (INN) called IFW, which aims to solve the problem of suboptimal encoder-decoder coupling in existing end-to-end watermarking architectures. The framework tightly couples the encoder and decoder to achieve highly consistent feature mapping using the same parameters, thus effectively avoiding redundant feature embedding. In addition, this paper adopts the INN to implement watermarking, which supports forward encoding and backward decoding, and the watermark extraction is completely dependent on the embedding algorithm without the need for the original network flow. This feature enables both the embedding and the blind extraction of watermarks simultaneously. Extensive experiments demonstrate that the proposed IFW method achieves a watermark extraction accuracy exceeding 96.6% and maintains a stable K-S test p-value above 0.85 in both simulated and realworld Tor traffic environments. These results indicate a clear advantage over mainstream baselines, highlighting the method’s ability to jointly ensure robustness and invisibility, as well as its strong potential for real-world deployment. Index Terms—Flow watermarking, inter-packet delay, INN, invisibility, robustness.

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
- 主题线索：malicious traffic, anomaly, tor, adversarial, covert, quic, traffic classification。
- 摘要证据：Index Terms—Flow watermarking, inter-packet delay, INN, invisibility, robustness.

### 方法机制
正文方法段落未稳定提取；需打开 MinerU 原文核验输入、处理和输出。

### 实验与结果
![](images/9b3043f8a4c50bcea7d21e624473df412de21733d0d6193ec8982efecdbbf549.jpg) Fig. 7. Results of BER variation with watermark length l. ![](images/cb0507fcf359cfe9145fe9818404bb27089f2702ad375cae0e40bd5eca3e77bb.jpg) Fig. 8. Results of TPR/FPR variation with noise intensity ϑ. 3) Impact of Different Levels of Noise: The noise intensity ϑ in the network flow is another factor affecting IFW performance. We treat ϑ as a variable and, using a singlevariable setup, fix other parameters (f=50, l=100) to observe how TPR, FPR, and BER vary with ϑ. Fig. 8 shows that the TPR of extracted watermarks when ϑ<sub>=</sub>0.1, 0.12, 0.14, 0.16, 0.18 is 99.26%, 97.59%, 96.30%, 95.15%, 94.92%. And Fig. 9 similarly shows that the BER is 0.38%, 1.18%, 1.84%, 2.39%, and 2.55% at this time, respectively. Obviously, as ϑ increases, the TPR of the watermark shows a downward trend, while the FPR and BER exhibit an upward trend.

### 局限与复现
论文局限段落未稳定提取；复现前需核验数据划分、随机种子、代码和运行环境。

### 开源与证据等级
- 代码线索：检测到 GitHub 线索。
- 当前分析等级：L2→深度补充；所有未被正文片段直接支持的判断均保留为待核验。


## 深度分析（并行深度分析更新 2026-09-29）

### 方法、实验与证据
IFW使用可逆神经网络耦合编码器/解码器进行流水印，指标含TPR、FPR、BER；Tor真实IPD数据来自港新两端、6个中继、两组各500次3MB上传。需核对攻击场景、对比方法和表格数值，复现依赖Tor采集环境。

### 横向联动与局限
- 该论文可联动 [[method-comparison-table]]、[[narrative-pattern-comparison]] 与相关任务/方法页；当前仅追加证据，不改写既有结论。
- 复现/引用前需核对 MinerU 表格、官方 PDF 与代码仓库；未从正文稳定提取的字段保留 unknown。
- 证据等级：摘要与方法/实验章节可定位；跨论文比较不据此自动推断因果或部署保证。

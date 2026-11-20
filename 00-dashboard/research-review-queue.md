<!-- evidence-audit:generated:start -->
# 研究审核队列

试点：`tor-over-proxy-low-fpr-detection`；生成日期：2026-11-20

| 优先级 | 位置 | 待处理事项 |
|---|---|---|
| — | — | 当前没有待处理事项 |

处理规则：先修复来源和定位问题，再审核证据方向；未经审核的记录不得进入正式共识。
<!-- evidence-audit:generated:end -->

## 2026-11-18 核验前候选队列

原表供追溯，现行处理状态见上方生成区及证据账本。

| 证据 | 命题 | 初判方向 | 状态 |
| --- | --- | --- | --- |
| EV-V2-SOK-CIPHERTEXT | CLM-0001 | supports | pending_review |
| EV-V2-LEAKAGE-THEOREM | CLM-0002 | supports | pending_review |
| EV-V2-SWEET-SPLIT | CLM-0003 | supports | pending_review |
| EV-V2-SOK-CORPUS | CLM-0004 | supports | pending_review |
| EV-V2-CRYPTO-CONTENT | CLM-0005 | supports | pending_review |
| EV-V2-IMC-REPLICATION | CLM-0006 | supports | pending_review |
| EV-V2-SWEET-BASELINES | CLM-0101 | supports | pending_review |
| EV-V2-NEST-GATE-CONTROL | CLM-0102 | supports | pending_review |
| EV-V2-GRAPHIDS-VERSIONS | CLM-0104 | supports | pending_review |
| EV-V2-ETBERT-PRETRAIN | CLM-0201 | supports | pending_review |
| EV-V2-HF-SUPERVISED | CLM-0202 | supports | pending_review |
| EV-V2-GENETC-PRETRAIN | CLM-0203 | supports | pending_review |
| EV-V2-DF-DEFENSES | CLM-0301 | supports | pending_review |
| EV-V2-PALETTE-DEFINED | CLM-0302 | supports | pending_review |
| EV-V2-ONLINE-WF | CLM-0303 | supports | pending_review |
| EV-V2-MM4FLOW-MODAL | CLM-0401 | supports | pending_review |
| EV-V2-BPFDAG-ABLATION | CLM-0402 | supports | pending_review |
| EV-V2-MET-EMBEDDING | CLM-0501 | supports | pending_review |
| EV-V2-TRAFFICFORMER-OVERLAP | CLM-0502 | supports | pending_review |
| EV-V2-PACKETLOOM-PREPROCESSING | CLM-0503 | supports | pending_review |
| EV-V2-NEST-FACTORIZE | CLM-0601 | supports | pending_review |
| EV-V2-NEST-CONFIRM | CLM-0602 | supports | pending_review |
| EV-V2-NEST-CALIBRATION | CLM-0603 | supports | pending_review |
| EV-V2-NEST-FROZEN-FPR | CLM-0604 | supports | pending_review |
| EV-V2-NEST-SWEPT-FPR | CLM-0605 | supports | pending_review |
| EV-V2-NEST-LATER-RESEGMENT | CLM-0606 | supports | pending_review |
| EV-V2-COSINT-DHOR | CLM-0607 | neutral | pending_review |
| EV-V2-COSINT-DHBCORR | CLM-0608 | neutral | pending_review |
| EV-V2-BTR-BLOCK | CLM-0007 | neutral | pending_review |
| EV-V2-FLOWSEM-FROZEN | CLM-0103 | neutral | pending_review |
| EV-V2-BIAS-FIELD | CLM-0003 | neutral | pending_review |
| EV-V2-WF-REALITY | CLM-0304 | neutral | pending_review |
| EV-V2-HYTMTC-FUSION | CLM-0403 | neutral | pending_review |
| EV-V2-WF-DRIFT-AION | CLM-0304 | neutral | pending_review |
| EV-V2-RTT-PROXY-ADJACENT | CLM-0609 | neutral | pending_review |

## 历史人工记录

# 研究审核队列

试点：`tor-over-proxy-low-fpr-detection`；生成日期：2026-10-23

| 优先级 | 位置                                                                                                                          | 待处理事项     |
| --- | --------------------------------------------------------------------------------------------------------------------------- | --------- |
| P2  | `03-paper-notes/2024-TON-Website_Fingerprinting_on_Encrypted_Proxies__A_Flow-Context-Aware_Approach_and_Countermeasures.md` | 缺少 pdf 字段 |

处理规则：先修复来源和定位问题，再审核证据方向；未经审核的记录不得进入正式共识。

## 2026-11-17　2026-COSINT-北邮时金桥

| 证据 | 已完成定位 | 后续核对 |
|---|---|---|
| EV-COSINT-01 | 第 27 页 Table IV/脚注，原表已核读 | λ、各类与整体分母、逐轮计数及召回 |
| EV-COSINT-02 | 第 31 页 Table VII–VIII | 同预算与查询库/阈值细节 |
| EV-COSINT-03 | 第 48 页 Table 2 | 完整划分、候选构建、缺失匹配条件 |
| EV-COSINT-04 | 第 49–50 页吞吐/耗时分解 | 硬件、总成本与实际端到端时延 |

来源为 [[03-paper-notes/2026-COSINT-北邮时金桥|2026-COSINT-北邮时金桥]]，四项状态均为 `pending_review`。


## 2026-11-18　COSINT 联动待审核项

| 证据编号 | 主题 | 出处 | 优先检查 |
| --- | --- | --- | --- |
| EV-20261118-COSINT-NORMAL-REF | 困难背景的得分分布和工作点 | COSINT 第 18–31 页；HAD §VII-B–C 表 XI–XII；GraphIDS §4.3–4.6 | 以训练侧正常参考进行局部筛查是否能在同召回和覆盖下改善目标承载留出的误报，需要同表示和按背景来源留出的验证。 |
| EV-20261118-COSINT-TIMING | 底层路由及跨点匹配条件 | COSINT 第 46–51 页；SaTor §5.4 表 1、§5.7–5.8 图 13 | 链路时延和抖动可以作为联合阅读的分层变量，尚待在相同候选集合和真值上验证是否改变匹配分数与尾部。 |
| EV-20261118-COSINT-COST | 摘要、编码和查询匹配的成本 | COSINT 第 49–50 页；Nepco §V-C 表 IV；PS-ML §V-C；SEDMS §VII-F–G | 处理速度需要对应观测单位与完成量。编码压缩是否降低总体时间需计量观测等待、编码、队列和匹配，并固定误报工作点与覆盖。 |

优先核对困难背景与阈值，随后验证链路条件和成本。新增 10 条论文证据见 [[09-claims/claims-index#2026-11-18　批次证据候选|批次证据候选]]。

## 2026-11-18　深读证据补充

新增 6 条原文定位记录已进入待审核队列。重点复核同一实验的分母、标签和可比条件，见 [[09-claims/claims-index#2026-11-18　深读证据补充|本批深读证据]]。

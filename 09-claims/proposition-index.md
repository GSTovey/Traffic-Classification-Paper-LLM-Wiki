---
type: proposition-index
created: "2026-11-18"
---

# 命题索引

正式命题区供综述、研究前沿和下游知识页引用。按维护者授权核对原文后签审；结论以表中实验和理论条件为限。历史材料见 [[claims-index|旧 Claims]]、[[claim-migration-map|迁移清单]] 和 [[contradictions|跨论文关系]]。

## 正式命题

| 命题 ID | 命题与适用条件 | claim_state | 关键证据 ID | 签审人 | 签审日期 |
| --- | --- | --- | --- | --- | --- |
| CLM-0001 | SoK 的 E1–E3 对照中，ET-BERT 的平均准确率均约 0.12，范围为论文所测分类器、语料与输入变换。 | supported | EV-V2-SOK-CIPHERTEXT | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0002 | 二元语义侧信道定理在指定先验、语义区分、映射非退化和连续性条件下给出观测轨迹的正互信息下界。 | supported | EV-V2-LEAKAGE-THEOREM | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0003 | Sweet Danger 的 TLS-120 冻结 ET-BERT 按包划分和按流划分的 macro-F1 分别是 97.0% 和 6.7%。原文另设未冻结模型的隐式流标识对照。 | supported | EV-V2-SWEET-SPLIT | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0004 | SoK §5.1.3 Fig. 2a 报告所核查 ISCXVPN2016 与 USTC-TFC2016 中的未加密会话比例为 98.9% 与 94.7%。 | supported | EV-V2-SOK-CORPUS | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0005 | CryptoFormer Fig. 8 在明密文协议混合的完整 18 种资产数据上报告，去掉包内容模块后的 accuracy 与 F1 下降最大。 | supported | EV-V2-CRYPTO-CONTENT | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0006 | IMC 复核在所测试的密文统计特征中发现会话划分和序列长度混杂，受控比较未支持所复核的稳定判别信号。 | supported | EV-V2-IMC-REPLICATION | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0007 | 纯密文字节在独立采集、同协议且等长度控制下，是否优于保留长度的随机化对照，现有审定材料证据不足。 | insufficient_evidence | — | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0101 | Sweet Danger 在 TLS-120 按流划分且保留 IP 的 base 设置中，LightGBM 与冻结 Pcap-Encoder 的 macro-F1 为 82.4% 和 63.7%。各自去 IP 后为 40.6% 和 13.0%。 | supported | EV-V2-SWEET-BASELINES | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0102 | NestTor 原文确认集上，FS-Net 与 NestTor 共用代理门控时的二类 macro-F1 为 99.50% 和 99.45%，差值 95% CI 包含零。各自端到端时为 87.46% 与 99.45%。 | supported | EV-V2-NEST-GATE-CONTROL | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0103 | 在数据、输入字段、划分和训练预算匹配时，浅层与深度表示的排序能否跨任务复现，现有审定材料证据不足。 | insufficient_evidence | — | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0104 | GraphIDS 对 Anomal-E 的 CSE-CIC-IDS2018 PR-AUC 均值在 v3 为 0.8819 对 0.2555，在 v2 为 0.9201 对 0.9287。两个版本的特征和聚合定义不同。 | supported | EV-V2-GRAPHIDS-VERSIONS | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0201 | ET-BERT 在 ISCX-VPN-App 的原论文 packet 消融中，完整方案和去预训练对照的 F1 分别为 0.9395 与 0.5638。 | supported | EV-V2-ETBERT-PRETRAIN | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0202 | HF-Transformer 以包头字段监督学习，在论文所用 CSTNET-TLS1.3 设置下取得 F1 0.9150。 | supported | EV-V2-HF-SUPERVISED | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0203 | GenETC Table VII 保留动态图模块、改用随机初始化时，所测六个基准的 F1 均低于对应的预训练配置。 | supported | EV-V2-GENETC-PRETRAIN | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0204 | 预训练收益能否在表示、标注与算力匹配时迁移到独立采集域，现有审定材料证据不足。 | insufficient_evidence | — | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0301 | DF 在原闭集实验中对 WTF-PAD 和对称 Walkie-Talkie 分别报告 90.7% 与 49.7% accuracy。 | supported | EV-V2-DF-DEFENSES | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0302 | Palette Table 3 的闭集设置给出 DF accuracy 20.27 ± 0.14%，对应 84% 带宽与 9% 时间开销。 | supported | EV-V2-PALETTE-DEFINED | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0303 | Online WF Fig. 9 的 top-100 候选组在监控 1 个和 5 个网站时分别报告平均精确率 0.83 和 0.82，较大的监控集合结果下降。 | supported | EV-V2-ONLINE-WF | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0304 | 防御、监控站点、基率和时间改变后，闭集所见的 WF 攻防排序能否复现，现有审定材料证据不足。 | insufficient_evidence | — | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0401 | MM4flow 的 SFT 单视图对照在 DataCon2021-p2 上给出包长 0.8999、字节 0.0125 的 F1，在 Browser 上分别是 0.8580、0.9903。 | supported | EV-V2-MM4FLOW-MODAL | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0402 | BPF-DAG 在 ISCX-VPN 的 Table VIII 报告完整方案 accuracy 0.9912，去时序 0.8440，去拓扑 0.9793，拼接 0.9742，平均 0.9587。 | supported | EV-V2-BPFDAG-ABLATION | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0403 | 在相同字段、骨干和训练预算下，早期与晚期融合的排序能否在独立数据复现，现有审定材料证据不足。 | insufficient_evidence | — | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0501 | MET-LLM Table 3 去 tokenizer 的 F1 为 0.8957，完整方案为 0.9610。Table 4 的通用 BPE 对照为 0.8839，领域表示和通用 BPE 的序列长度分别为 1,247 与 2,847。 | supported | EV-V2-MET-EMBEDDING | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0502 | TrafficFormer §3.2.1 对相邻字节构造重叠 bigram 后应用 BPE。这里确认输入定义。 | supported | EV-V2-TRAFFICFORMER-OVERLAP | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0503 | PacketLoom 在 ISCX-VPN Service-level 子集给出 ET-BERT 与 YaTC 的预处理与复现对照，Table II 报分类指标，Table III 报实现量。 | supported | EV-V2-PACKETLOOM-PREPROCESSING | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0504 | 在可见字段、有效字节预算与训练预算匹配时，Tokenization 收益能否跨采集域复现，现有审定材料证据不足。 | insufficient_evidence | — | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0601 | NestTor Fig. 6 的同 99 维输入和总计 400 棵树的 RF 对照中，Independent Gate + Inner 为 94.12%，Flat Binary 为 86.67%，Shared Multi-task 为 88.11%，均为二类 macro-F1。 | supported | EV-V2-NEST-FACTORIZE | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0602 | NestTor Table III 的 2,300 条完整双向流确认集上，代理条件内层阈值为 99.45%，统一内层阈值为 99.41%，均按 ToP/Non-ToP 两类计算 macro-F1。 | supported | EV-V2-NEST-CONFIRM | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0603 | NestTor Table IV 留一代理用目标 Pure Proxy 校准后，三个代理折的二类 macro-F1 上升，Trojan 从 97.24% 降至 93.60%。VLESS 参加过前置协议审计。 | supported | EV-V2-NEST-CALIBRATION | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0604 | NestTor Table VI 的 Confirmatory 行中，冻结 AND 对 11,131 条异质背景流产生 350 次误报，FPR 3.14%，对另列的 900 条确认 ToP 检出 894 条，TPR 99.33%。 | supported | EV-V2-NEST-FROZEN-FPR | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0605 | NestTor Table VI 的三个描述性工作点来自连续乘积分数扫阈值，FPR 0.99%、0.10%、0.01% 分别对应确认 ToP TPR 94.44%、86.22%、72.33%。 | supported | EV-V2-NEST-SWEPT-FPR | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0606 | NestTor Table V 的 23,374 条后来采集流上二类 macro-F1 为 88.50%。Fig. 8 的确认集 512 B 重分段条件为 71.45%。 | supported | EV-V2-NEST-LATER-RESEGMENT | Codex（维护者授权按原文核验） | 2026-11-18 |
| CLM-0607 | COSINT 报告第 27 页 Table IV 在最低展示基率 λ≈1.24×10⁻⁶ 处报告 DHOR 总体精确率 81.94%、FPR 1.43×10⁻⁶。四个目标类各 160 个正样本，整体微平均，逐轮计算后对五轮取均值。仅对幻灯片所载结果签审。 | supported | EV-V2-COSINT-DHOR | Codex（维护者授权按原文核验） | 2026-11-19 |
| CLM-0608 | COSINT 报告第 48 页 Table 2 在每侧 20,000 条流表示的规模下报告关联精确率 99.33%、TPR 84.85%、FPR 2.9×10⁻⁷；第 49 页在另设的每侧 23,312 条流、5 秒设定报告约 5.4×10⁸ 候选对和 1.1×10⁸ 对/秒。仅对幻灯片所载结果签审。 | supported | EV-V2-COSINT-DHBCORR | Codex（维护者授权按原文核验） | 2026-11-19 |
| CLM-0609 | 固定阈值的预定低误报工作点能否跨代理、负类来源、独立采集域和观测窗口维持，现有审定材料证据不足。 | insufficient_evidence | — | Codex（维护者授权按原文核验） | 2026-11-18 |

本轮核验出处及修订记录见 [[front-review-2026-11-18|七条前沿原文复核]]。

## 待签审命题

本批 v2 记录已处置。COSINT 两条命题的签审范围为报告所载结果，原实验的完整配置缺口见 [[2026-COSINT-北邮时金桥]]。

| 命题 ID | 待复核命题及适用条件 | 关联前沿 |
| --- | --- | --- |

## COSINT 报告签审前状态

| 命题 ID | 待复核命题及适用条件 | 关联前沿 |
| --- | --- | --- |
| CLM-0607 | COSINT DHOR 的报告级指标已定位，完整划分和分母细节待补。 | [[tor-over-proxy-low-fpr-detection]] |
| CLM-0608 | COSINT DHBCorr 的双侧候选关联及吞吐口径已定位，完整候选构造和匹配评估细节待补。 | [[tor-over-proxy-low-fpr-detection]] |

## 签审前待审清单

历史原表供追溯，现行状态以以上两节为准。


| 命题 ID | 待复核命题及适用条件 | 关联前沿 |
| --- | --- | --- |
| CLM-0001 | SoK 对 CipherSpectrum 等数据的 E1–E3 密文输入对照中，ET-BERT 的平均准确率约为 0.12。 | [[payload-learnability]] |
| CLM-0002 | 二元语义侧信道定理在区分度、容量和连续性假设成立时给出观测侧信道的正互信息下界。 | [[payload-learnability]] |
| CLM-0003 | TLS-120 上 ET-BERT 的包级测试结果受划分单位与隐式流标识信息影响。 | [[payload-learnability]]、[[representation-vs-shallow]] |
| CLM-0004 | SoK 所用 ISCXVPN2016 和 USTC-TFC2016 版本包含大量未加密会话；应依论文的会话加密判定口径解释。 | [[payload-learnability]] |
| CLM-0005 | CryptoFormer 在该明密文混合币种数据上，去掉包内容模块会降低整体分类指标。 | [[payload-learnability]]、[[multimodal-fusion-strategy]] |
| CLM-0006 | IMC 2026 复核在其控制条件下未重现所考察的密文随机性分类信号。 | [[payload-learnability]] |
| CLM-0007 | 纯密文字节分类器在独立采集、同协议等长度的试验中仍能优于保留长度的随机化对照。 | [[payload-learnability]] |
| CLM-0101 | Sweet Danger 的 TLS-120 受控实验中，所测手工特征基线与所测冻结字节编码器存在条件性性能差距。 | [[representation-vs-shallow]] |
| CLM-0102 | NestTor 的确认集对照中，给 FS-Net 共用代理门控后的结果与原端到端对照不同。 | [[representation-vs-shallow]]、[[tor-over-proxy-low-fpr-detection]] |
| CLM-0103 | 浅层、序列和图表征在共用输入、划分及预算时的排序，可跨不同任务复现。 | [[representation-vs-shallow]] |
| CLM-0104 | GraphIDS 与 Anomal-E 在作者所用 CIC NetFlow v2/v3 上的 PR-AUC 排序随数据版本改变。 | [[representation-vs-shallow]] |
| CLM-0201 | ET-BERT 在 ISCX-VPN-App 原论文协议中，去掉 packet 预训练后 F1 下降。 | [[pretraining-necessity]] |
| CLM-0202 | HF-Transformer 用包头字段和监督学习，在论文所用六个基准下达到所报告的分类表现。 | [[pretraining-necessity]]、[[tokenization-optimal]] |
| CLM-0203 | GenETC 在其划分与图模块配置下，Table VII 的预训练消融可检验初始化对下游指标的影响。 | [[pretraining-necessity]] |
| CLM-0204 | 相同表示、标注与算力预算下，源域上观察到的预训练收益可在独立采集测试域复现。 | [[pretraining-necessity]] |
| CLM-0301 | DF 在 2018 年闭集实验中的准确率因 WTF-PAD 与对称 Walkie-Talkie 条件而异。 | [[wf-attack-defense-limit]] |
| CLM-0302 | Palette 的闭集实验在指定流量数据、防御和重新训练条件下显著改变所测 WF 准确率。 | [[wf-attack-defense-limit]] |
| CLM-0303 | Online WF 的真实 Tor 实验中，效果取决于被监控站点构成、规模和开放集口径。 | [[wf-attack-defense-limit]] |
| CLM-0304 | 在防御、监控站点、基率和时间变化时，闭集评测所见的 WF 攻防排序仍可复现。 | [[wf-attack-defense-limit]] |
| CLM-0401 | MM4flow 的单视图及融合对照显示视图贡献随任务改变。 | [[multimodal-fusion-strategy]]、[[representation-vs-shallow]] |
| CLM-0402 | BPF-DAG 在 ISCX-VPN 的实验中，时序、拓扑分支与融合方式影响其分类结果。 | [[multimodal-fusion-strategy]] |
| CLM-0403 | 固定可见输入、骨干、参数与训练预算后，早期和晚期融合的性能排序可在独立数据复现。 | [[multimodal-fusion-strategy]] |
| CLM-0501 | MET-LLM 在其恶意加密流量任务的 tokenizer 对照中，领域表示方案的 F1 与序列长度不同于通用 BPE。 | [[tokenization-optimal]] |
| CLM-0502 | TrafficFormer 的相邻 bigram 转换使相邻单元共享字节；该表示属性与下游收益是两个可分别检验的问题。 | [[tokenization-optimal]] |
| CLM-0503 | PacketLoom 的 ISCX-VPN 对照表明复现 ET-BERT 与 YaTC 时预处理定义会影响输入及复现口径。 | [[tokenization-optimal]] |
| CLM-0504 | 固定包数、可见字段、有效字节与训练预算后，指定 Tokenization 相对字节级基线的收益可跨采集域复现。 | [[tokenization-optimal]] |
| CLM-0601 | NestTor 使用相同输入、RF 与树预算时，独立 Gate + Inner 在该四类验证协议下优于所测共享与平面对照。 | [[tor-over-proxy-low-fpr-detection]] |
| CLM-0602 | NestTor 用完整双向 TCP 流的方向、长度和相对时间，在作者域名和采集分组确认集上达到所报告的四类 macro-F1。 | [[tor-over-proxy-low-fpr-detection]]、[[payload-learnability]] |
| CLM-0603 | NestTor 以目标 Pure Proxy 参考集作分位数校准时，结果随代理协议而变。 | [[tor-over-proxy-low-fpr-detection]] |
| CLM-0604 | 冻结 NestTor AND 决策在 11,131 条异质背景流上的 FPR 按假阳性流数计算。 | [[tor-over-proxy-low-fpr-detection]] |
| CLM-0605 | NestTor 所报 0.99%、0.10%、0.01% FPR 工作点采用乘积分数事后扫阈值。 | [[tor-over-proxy-low-fpr-detection]] |
| CLM-0606 | NestTor 在后来采集和 512 B 重分段条件下的四类 macro-F1 低于各自确认口径。 | [[tor-over-proxy-low-fpr-detection]] |
| CLM-0607 | COSINT 的 DHOR 结果对应报告定义的五分类和基率，作为相邻任务资料。 | [[tor-over-proxy-low-fpr-detection]] |
| CLM-0608 | COSINT 的 DHBCorr 精确率、FPR 和吞吐对应双侧候选关联及其分母。 | [[tor-over-proxy-low-fpr-detection]] |
| CLM-0609 | 预先指定的 ToP 低误报工作点在固定阈值下可跨代理、负类来源、采集域与观测窗口维持。 | [[tor-over-proxy-low-fpr-detection]] |

## 签审历史

按版本追加上一版判断、修改原因、证据 ID、审核人和日期。初始命题与其历史出处见 [[claim-migration-map]]。

---
type: claims
name: contradictions
created: "2026-05-27"
updated: "2026-05-27"
---

# Contradictions

本页面用于记录不同论文之间的结论冲突、适用条件差异和实验设置差异。

## 矛盾记录

| 问题 | 论文 A | 论文 B | 冲突点 | 可能原因 |
|---|---|---|---|---|
| 加密 payload 是否可学习 | ET-BERT (WWW 2022)：声称从加密 datagram 中通过 MBM 预训练学到有意义的上下文表示，CSTNET-TLS 1.3 F1 达 97.4% | Sweet Danger (SIGCOMM 2025)：证明加密 payload 上做 MAE 预训练在理论上不可行，ET-BERT 在 per-flow split + frozen encoder 下 TLS-120 F1 仅 6.7% | ET-BERT 声称加密 payload 中存在可学习模式，Sweet Danger 证明这些"模式"主要来自 per-packet split 导致的数据泄漏和 shortcut learning（如 TCP SeqNo/AckNo） | ET-BERT 使用 per-packet split 使同一流的数据包同时出现在训练集和测试集，模型通过 implicit flow ID 将测试包关联到训练集标签；Sweet Danger 揭示移除 SeqNo/AckNo/Timestamp 后 ET-BERT 准确率从 97.4% 暴跌至 19.5% |
| 深度学习 vs 传统 ML 在加密流量分类中的优劣 | SoK (S&P 2025)：通过 348 次特征遮蔽实验证明，ET-BERT 和 YaTC 等深度学习分类器的高性能源于 SII 过拟合和过时数据集，仅用加密 payload 时准确率仅 0.12 | ET-BERT (WWW 2022)、YaTC、NetMamba 等多篇深度学习论文：声称深度学习方法在加密流量分类上显著优于传统 ML，F1 达 95%+ | SoK 认为深度学习分类器的高准确率是"虚假繁荣"，真正从加密流量中学到的信息极为有限；DL 论文则声称自动特征学习优于手工特征 | SoK 发现 ISCXVPN2016 含 98.9% 未加密流量、USTC-TFC2016 含 94.7% 未加密流量，DL 模型实际在学习未加密内容特征而非加密模式；SII（IP/端口/MAC）匿名化后性能骤降 |
| WF 攻击是否已攻破现有防御 | Deep Fingerprinting (CCS 2018)：声称 DF 在 WTF-PAD 上达 90.7% 准确率，首次攻破轻量级防御 | Palette (S&P 2024)：声称通过流量聚类匿名化将 SOTA WF 攻击准确率平均降低 73.60%，DF 在 Palette 防御下准确率仅 20.27% | DF 认为深度学习可攻破 WTF-PAD 等轻量防御；Palette 认为通过 traffic cluster anonymization 可有效抵御包括 DF 在内的所有 SOTA 攻击 | 评估的防御代际不同：WTF-PAD 是 2016 年的 obfuscation 类防御，仅做随机填充；Palette 是 2024 年的 regularization 类防御，将相似网站统一为相同流量模式。攻防军备竞赛持续升级 |
| 数据集划分方式对结论的影响 | ET-BERT (WWW 2022) 及多数 DL 论文：使用 per-packet split（8:1:1），报告 95%+ 准确率 | Sweet Danger (SIGCOMM 2025)：主张必须使用 per-flow split，同一 TCP 流的包不能同时出现在训练集和测试集 | 同一模型在不同划分方式下性能差距巨大：ET-BERT 在 per-packet split 下 TLS-120 F1=96.8%，per-flow split 下 F1=21.5%（unfrozen）/ 6.7%（frozen） | per-packet split 将同一流的包随机分散到训练集和测试集，模型利用 TCP 协议中的隐式流标识符（SeqNo、AckNo、TCP timestamp 共约 64-bit）将测试包关联到训练集中的类标签，构成严重的数据泄漏 |
| 表征学习 vs 浅层模型的实际价值 | MM4flow (CCS 2025)：通过 TB 级多模态预训练在六项任务上均优于 baseline，加密隧道网站识别准确率提升 84% | Sweet Danger (SIGCOMM 2025)：在 per-flow split + frozen encoder 设置下，所有表征学习模型（ET-BERT、YaTC、NetMamba）均不如 Random Forest + 手工特征（LightGBM TLS-120 F1=82.4% vs Pcap-Encoder 63.7%） | MM4flow 声称预训练表征学习是加密流量分析的未来方向；Sweet Danger 认为当前表征学习模型的实际价值有限，浅层模型 + 专家特征仍占优 | 评估设置和任务类型不同：MM4flow 使用 TB 级真实流量预训练并采用 packet length + payload 双模态，在特定任务（加密隧道识别）上 packet length 模态贡献巨大；Sweet Danger 仅评估单模态（payload）且使用严格的 frozen encoder 评估，揭示了 payload-only 表征的质量缺陷 |
| 评估指标的选择与结论可靠性 | Sweet Danger (SIGCOMM 2025)：批评 micro F1-Score 偏向多数类，推荐使用 macro F1-Score；指出在 macro F1 下已有模型性能被严重高估 | 多数加密流量分类论文（ET-BERT、YaTC、NetMamba 等）：使用 micro F1 或整体准确率报告结果，少数类性能被掩盖 | Sweet Danger 认为使用 micro F1 是误导性的，掩盖了模型在少数类上的糟糕表现；其他论文认为 micro F1 反映了整体分类效果 | 类别不平衡数据集中，micro F1 按样本数加权，少数类的贡献被稀释。例如 ET-BERT 在 120 类 TLS 分类中，热门网站的良好表现可掩盖冷门网站的低准确率。Sweet Danger 的实验显示 micro F1 与 macro F1 差异可达 30%+ |
| 流量表示中信息来源的本质 | SoK (S&P 2025)：通过遮蔽实验证明仅头部信息时 ET-BERT 准确率 0.63（与基线一致），仅加密 payload 时仅 0.12，说明头部信息是主要分类依据 | ET-BERT (WWW 2022)：提出 Datagram2Token 框架，声称从加密 datagram 的字节级模式中通过 MBM 学习到上下文关系，是分类性能的关键来源（去除 MBM 后 F1 下降 9.33%） | SoK 认为加密 payload 本身几乎不包含可学习信息，分类主要依赖协议头；ET-BERT 认为 payload 中的字节模式是可学习的且对分类至关重要 | SoK 使用 CipherSpectrum（纯 TLS 1.3 数据集，强加密），ET-BERT 的预训练数据包含弱加密流量（RC4、3DES）和未加密流量。在弱加密/未加密场景下 payload 确实包含可学习模式，但在强加密（TLS 1.3 + AES-GCM）下这些模式消失。两者结论在各自条件下均成立，但泛化性不同 |
| WF 防御的鲁棒性与可迁移攻击 | Palette (S&P 2024)：声称在 adversarial training 设置下仍有效，将 RF 攻击准确率降至 36.43%，是唯一同时抵抗 AdvTrain、适应实时流量、掩盖 informative features 的防御 | Swallow (CCS 2025)：通过 CIF 动态对齐和自监督学习，在 Front 防御下准确率 62.41%（比 NetCLR 高 44%），在 RegulaTor 下 33.60%，证明自适应攻击仍可部分攻破防御 | Palette 声称现有防御的不足可通过 traffic cluster anonymization 解决；Swallow 证明即使先进的防御也可通过更好的特征表示和迁移学习部分攻破 | 攻击和防御评估的假设不同：Palette 评估的是传统 WF 攻击（DF、RF 等）在 adversarial training 下的表现；Swallow 提出了全新的攻击范式（CIF + BYOL 自监督 + few-shot 迁移），通过动态时间间隔对齐捕获跨网络条件的一致性特征。两者说明攻防是持续演进的，不存在"终极"防御 |

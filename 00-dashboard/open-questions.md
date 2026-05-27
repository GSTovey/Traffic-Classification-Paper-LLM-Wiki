# Open Questions

本页面从 [[claims-index]] 和 [[contradictions]] 中提炼开放研究问题。

---

## 核心研究问题

| 问题 | 来源 | 相关概念 | 重要性 | 状态 |
|---|---|---|---|---|
| 加密 payload 中是否真的存在可学习的内在模式？在 TLS 1.3 + AES-GCM 强加密条件下，分类器到底在学什么？ | [[contradictions]]：SoK vs ET-BERT | [[encrypted-traffic-analysis]]、[[traffic-representation-learning]] | high | open |
| per-packet split 导致的数据泄漏到底有多严重？如何设计无泄漏的评估协议？ | [[contradictions]]：Sweet Danger vs ET-BERT | [[traffic-classification]]、[[traffic-foundation-model]] | high | open |
| 在正确的 per-flow split + frozen encoder 评估下，深度表征学习模型是否仍有价值？浅层模型 + 手工特征是否就是上限？ | [[contradictions]]：Sweet Danger vs MM4flow | [[traffic-representation-learning]]、[[pre-training-finetuning]] | high | open |
| 多模态融合（payload + packet length）能否真正突破单模态表征的瓶颈？ | [[claims-index]]：MM4flow 的 TB 级预训练结果 | [[multi-modal-fusion]]、[[traffic-foundation-model]] | high | open |
| 现有公开数据集（ISCXVPN2016、USTC-TFC2016）含 90%+ 未加密流量，如何构建真正可靠的加密流量评估基准？ | [[claims-index]]：SoK 数据集分析 | [[traffic-classification]]、[[anomaly-detection]] | high | open |
| 强标识信息（SII：MAC/IP/端口）的过拟合问题如何系统性地解决？匿名化后模型性能暴跌的根因是什么？ | [[claims-index]]：SoK SII 分析 | [[traffic-classification]]、[[traffic-representation-learning]] | high | open |
| micro F1 vs macro F1：加密流量分类领域应采用何种评估指标才能真实反映模型性能？ | [[contradictions]]：Sweet Danger 指标批评 | [[traffic-classification]] | medium | open |
| WF 攻防是否存在"终极平衡"？自适应攻击（如 Swallow 的 CIF + 自监督）是否总能攻破新防御？ | [[contradictions]]：Palette vs Swallow | [[website-fingerprinting]] | high | open |
| 预训练范式在加密流量分类中的真实增益有多大？去除预训练后 ET-BERT F1 下降 37.57%，但 Sweet Danger 又显示预训练模型不如 RF，如何调和？ | [[contradictions]]：ET-BERT vs Sweet Danger | [[pre-training-finetuning]]、[[traffic-foundation-model]] | high | open |
| 2-gram tokenization 的 masked token 可由相邻 token 推断，byte tokenization 是否更优？流量数据的最佳 tokenization 策略是什么？ | [[claims-index]]：MM4flow tokenization 分析 | [[traffic-foundation-model]]、[[transformer]] | medium | open |
| 领域专用 tokenization 对 LLM 流量分析的重要性有多高？通用 NLP tokenizer 与领域 BPE tokenizer 的差距能否通过其他方式弥补？ | [[claims-index]]：MET-LLM 消融实验 | traffic-foundation-model | medium | open |
| 仅标注千分之一的流量样本即可达到 99.82% 检测精度，少样本方法在实际部署中的泛化性和鲁棒性如何？ | [[claims-index]]：tFusion 结果 | [[few-shot-traffic-learning]]、[[malicious-traffic-detection]] | medium | open |
| 流量字节更类似于图像像素而非自然语言词汇（最优 mask ratio 90%），这对模型架构选择（CV 范式 vs NLP 范式）有何启示？ | [[claims-index]]：YaTC 分析 | [[traffic-representation-learning]]、[[transformer]] | medium | open |
| 对比学习结合语义属性矩阵（SAM）在 evasion attack 下 F1/AUC 超 93%，这种鲁棒性在更复杂的对抗场景下是否可持续？ | [[claims-index]]：SmartDetector 结果 | [[contrastive-learning]]、[[malicious-traffic-detection]] | medium | open |
| 轻量级可解释网络 LEXNet（119k 参数）达到 89.7% 准确率并提供 by-design 解释，可解释性与性能的权衡是否有通用解？ | [[claims-index]]：LEXNet 结果 | [[convolutional-network]]、[[traffic-classification]] | medium | open |
| 因果链解耦方法天然抵抗 packet loss/duplication/disorder，这种鲁棒性是否可推广到其他流量分析任务？ | [[claims-index]]：RobustWF 结果 | [[website-fingerprinting]] | low | open |

---

## 问题类型

| 类型 | 说明 |
|---|---|
| theory | 理论问题 |
| method | 方法问题 |
| experiment | 实验问题 |
| engineering | 工程落地问题 |
| survey | 综述组织问题 |
| proposal | 项目申报问题 |

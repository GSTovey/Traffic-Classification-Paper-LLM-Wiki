---
type: paper
title_original: "A Hard-Label Black-Box Evasion Attack against ML-based Malicious Traffic Detection Systems"
title_cn: "针对基于机器学习的恶意流量检测系统的硬标签黑盒逃逸攻击"
authors: [Zixuan Liu, Yi Zhao, Zhuotao Liu, Qi Li, Chuanpu Fu, Guangmeng Zhou, Ke Xu]
year: 2026
venue: "NDSS"
doi: "10.14722/ndss.2026.240916"
url: "https://www.ndss-symposium.org/"
pdf: "00-inbox/PDFs/2026-NDSS-A_Hard-Label_Black-Box_Evasion_Attack_against_ML-based_Malicious_Traffic_Detection_Systems.pdf"
mineru_md: "02-parsed-markdown/2026-NDSS-A_Hard-Label_Black-Box_Evasion_Attack_against_ML-based_Malicious_Traffic_Detection_Systems.md"
status: processed
reading_level: L2
research_area: [malicious-traffic-detection, adversarial-attack]
task: [evasion-attack, traffic-mimicking]
method: [reinforcement-learning, pre-training, bi-cross-attention]
dataset: [MAWI, Botnet-Mirai, Botnet-Zeus, Botnet-Storm, Botnet-Waledac, CICFlowMeter]
code: "unknown"
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

# 2026-NDSS NetMasquerade

## §0 基础信息

| 属性 | 值 |
|------|-----|
| 论文全称 | A Hard-Label Black-Box Evasion Attack against ML-based Malicious Traffic Detection Systems |
| 作者 | Zixuan Liu, Yi Zhao, Zhuotao Liu, Qi Li, Chuanpu Fu, Guangmeng Zhou, Ke Xu |
| 机构 | Tsinghua University, Beijing Institute of Technology, Zhongguancun Lab |
| 年份/会议 | 2026 / NDSS |
| 关键词 | evasion attack, black-box, reinforcement learning, BERT, traffic mimicking |

## §1 一句话总结

提出 NetMasquerade，利用强化学习和预训练模型 Traffic-BERT，将恶意流量伪装为良性流量，在无需目标模型内部信息的硬标签黑盒场景下，对 6 种检测系统在 80 个攻击场景中实现超过 96.65% 的攻击成功率。

## §2 摘要翻译

**原文摘要:**
Machine Learning (ML)-based malicious traffic detection is a promising security paradigm. It outperforms rule-based traditional detection by identifying various advanced attacks. However, the robustness of these ML models is largely unexplored, thereby allowing attackers to craft adversarial traffic examples that evade detection. Existing evasion attacks typically rely on overly restrictive conditions (e.g., encrypted protocols, Tor, or specialized setups), or require detailed prior knowledge of the target (e.g., training data and model parameters), which is impractical in realistic black-box scenarios. The feasibility of a hard-label black-box evasion attack (i.e., applicable across diverse tasks and protocols without internal target insights) thus remains an open challenge. To this end, we develop NetMasquerade, which leverages reinforcement learning (RL) to manipulate attack flows to mimic benign traffic and evade detection. Specifically, we establish a tailored pre-trained model called Traffic-BERT, utilizing a network-specialized tokenizer and an attention mechanism to extract diverse benign traffic patterns. Subsequently, we integrate Traffic-BERT into the RL framework, allowing NetMasquerade to effectively manipulate malicious packet sequences based on benign traffic patterns with minimal modifications. Experimental results demonstrate that NetMasquerade enables both brute-force and stealthy attacks to evade 6 existing detection methods under 80 attack scenarios, achieving over 96.65% attack success rate.

**中文翻译:**
基于机器学习的恶意流量检测是一种有前景的安全范式，在识别各类高级攻击方面优于传统规则检测。然而，这些 ML 模型的鲁棒性 largely 未被探索，攻击者可以 craft 对抗流量样本来逃逸检测。现有逃逸攻击通常依赖过于严格的条件（如加密协议、Tor 或专门设置），或需要目标的详细先验知识（如训练数据和模型参数），这在现实黑盒场景中不切实际。为此，我们开发了 NetMasquerade，利用强化学习操控攻击流量模仿良性流量并逃逸检测。具体而言，我们建立了专门的预训练模型 Traffic-BERT，利用网络专用 tokenizer 和注意力机制提取多样良性流量模式。实验结果表明，NetMasquerade 在 80 个攻击场景中使暴力和隐蔽攻击均能逃逸 6 种现有检测方法，攻击成功率超过 96.65%。

## §3 方法动机

**痛点:**
- 现有逃逸攻击依赖加密协议、Tor 等特定条件，场景受限
- 白盒/灰盒攻击需要目标模型参数或训练数据，现实中不可行
- 特征空间攻击需要干扰 ML 执行，不实用
- 现有方法在协议/任务变化时效果显著下降

**核心直觉:**
- 良性流量分布密集，恶意流量分布稀疏，存在密度差距
- 可通过强化学习将恶意流量特征向良性流形迁移
- 仅需硬标签反馈（blocked/not），无需模型内部信息
- 预训练模型可捕获多样良性流量模式，指导 RL 优化

## §4 方法设计

**整体流程:**
```
Stage 1: 良性流量模式捕获
  大量公开良性流量 → 分块/填充 → 网络专用 tokenizer
  → Traffic-BERT (bi-cross attention) → Mask-Fill 任务训练
  → 捕获包大小和 IPD 的双向依赖关系

Stage 2: 对抗流量生成
  恶意流量 → MDP 建模 → RL 策略网络 (GRU)
  → 选择掩码位置 → Traffic-BERT 填充良性模式
  → 探测目标系统 → 反馈 (blocked/not)
  → SAC 算法优化策略 → 对抗流量输出
```

**核心模块:**

1. **Traffic-BERT**:
   - 网络专用 tokenizer: 包大小直接编码，IPD 取 log10 后等长区间 hash
   - 流分类: 短流 padding，长流 chunking（99th percentile 确定固定长度）
   - Bi-Cross Attention: 包大小特征 P 和 IPD 特征 H 交叉注意力
     - h'_P = h_P + Attn(Q_hP, K_H, V_H)
     - h'_H = h_H + Attn(Q_hH, K_P, V_P)
   - Mask-Fill 训练: 15% 位置掩码，双序列同时掩码

2. **RL 框架**:
   - 状态空间: 恶意流量当前特征序列
   - 动作空间: 选择掩码位置和类型
   - 奖励设计: r = r_E (逃逸奖励) + r_D (差异惩罚) + r_M (有效性惩罚)
   - 策略网络: 轻量级 GRU
   - 算法: Soft Actor-Critic (SAC)
   - 终止条件: Q-Value 阈值 ξ' 或步数阈值 τ

3. **两阶段解耦训练**:
   - Stage 1 独立训练 Traffic-BERT，不与 RL 耦合
   - Stage 2 轻量策略网络增量引用 BERT 嵌入
   - 避免大规模重复训练

**关键公式:**
- 逃逸奖励: r_E = (N_evade(s_{t+1}) - N_evade(s_t)) / N_total
- 差异惩罚: r_D = -λ * d(original, adversarial)
- 有效性惩罚: r_M = sending_rate (保持攻击功能)

**优缺点:**
- (+) 硬标签黑盒，仅需 blocked/not 反馈
- (+) 协议无关、任务无关，适用范围广
- (+) 最小修改（≤10 步），保持攻击语义
- (+) 低延迟（4.239K packets/s）
- (-) 需要探测阶段获取反馈
- (-) Traffic-BERT 预训练需要大量良性流量

## §5 与其他方法对比

**创新点:**
- 首个协议无关、任务无关的硬标签黑盒逃逸攻击
- Traffic-BERT 的 bi-cross attention 机制融合多特征序列
- 两阶段解耦训练降低开销

**与 baseline 对比:**
| 方法 | 设置 | 协议无关 | 任务无关 | 无需先验知识 | 低开销 |
|------|------|---------|---------|-------------|--------|
| Gradient Analysis | 白盒 | ✗ | ✓ | ✗ | ✗ |
| Optimization | 白盒 | ✗ | ✓ | ✗ | ✗ |
| Sample Transferability | 灰盒 | ✗ | ✗ | ✗ | ✗ |
| Feature Manipulation | 灰盒 | ✓ | ✓ | ✓ | ✗ |
| Packet Reassembly | 黑盒 | ✗ | ✗ | ✓ | ✗ |
| NetMasquerade | 黑盒 | ✓ | ✓ | ✓ | ✓ |

## §6 实验表现

**数据集:**
- 背景流量: MAWI 2023 年 6 月/8 月骨干网流量（>1M flows）
- 攻击流量: 4 组 12 种攻击
  - 侦察扫描: host-scanning, fuzz-scanning
  - DoS: SSDP Flood, TCP SYN Flood
  - 僵尸网络: Mirai, Zeus, Storm, Waledac
  - 加密 Web 攻击: webshell, XSS, CSRF, spam

**目标系统（6 种）:**
- 传统 ML: Whisper, FlowLens, NetBeacon
- 深度学习: Vanilla+RNN, CICFlowMeter+MLP, Kitsune

**Baseline（4 种）:**
- Random Mutation, Mutate-and-Inject, Traffic Manipulator (灰盒), Amoeba

**评估指标:**
- ASR (Attack Success Rate): 恶意流未被检测的比例
- AUC, F1: 检测系统有效性
- Bandwidth (Mbps), Throughput (PPS)

**关键结果:**
- NetMasquerade 在 80 个攻击场景中平均 ASR 达 96.65%+
  - Whisper: 98.78%, FlowLens: 97.17%, NetBeacon: 98.09%
  - Vanilla: 97.82%, CICFlowMeter: 96.26%, Kitsune: 91.77%
- 比最佳 baseline 提升 2.61%-21.88%
- 56/72 场景取得最高 ASR
- 最小修改: ≤10 步，KL 散度仅 0.013
- 低延迟: 4.239K packets/s
- 收敛快: 420 episodes 内达 90% 收敛
- 可逃逸经验证鲁棒的方法（如 BARS）

## §7 学习与应用

**开源情况:**
- 论文未明确说明代码是否开源

**可复现性:**
- 使用公开数据集 MAWI
- 目标系统有开源实现（Kitsune, CICFlowMeter）
- 超参数明确: 步数阈值 τ ≤10, Q-Value 阈值 ξ'

**迁移价值:**
- 揭示 ML 检测系统的鲁棒性问题
- Traffic-BERT 可作为良性流量表示学习工具
- 两阶段解耦训练范式可应用于其他对抗任务
- 为防御方提供对抗样本生成能力评估

## §8 总结

**核心思想:** 利用强化学习和预训练 BERT 模型，将恶意流量特征向良性流形迁移，在仅需硬标签反馈的黑盒场景下实现高效逃逸攻击。

**快速 Pipeline:**
```
良性流量 → Traffic-BERT 预训练 (bi-cross attention + Mask-Fill)
    → 恶意流量 → MDP 建模
    → GRU 策略网络选择掩码位置
    → Traffic-BERT 填充良性模式
    → 探测目标系统获取 blocked/not 反馈
    → SAC 优化策略 → 对抗流量输出
```

## §9 知识链接

- [[malicious-traffic-detection]] — 论文攻击目标
- adversarial-attack — 对抗逃逸攻击方法
- [[pre-training-finetuning]] — Traffic-BERT 预训练
- [[transformer]] — BERT 架构和 bi-cross attention
- [[encrypted-traffic-analysis]] — 加密流量场景
- [[traffic-representation-learning]] — 流量特征表示

## §10 证据记录

| 关键声明 | 证据 | 可信度 |
|---------|------|--------|
| 平均 ASR 超 96.65% | Table II 80 场景统计 | 高 |
| 可逃逸经验证鲁棒的检测方法 | BARS 实验结果 | 高 |
| 最小修改 ≤10 步 | Table II 步数统计 | 高 |
| KL 散度仅 0.013 | Figure 8 带宽分布对比 | 高 |
| 低延迟 4.239K packets/s | Section V 吞吐量测试 | 高 |

## §11 原始资料链接

- PDF: `00-inbox/PDFs/2026-NDSS-A_Hard-Label_Black-Box_Evasion_Attack_against_ML-based_Malicious_Traffic_Detection_Systems.pdf`
- MinerU MD: `02-parsed-markdown/2026-NDSS-A_Hard-Label_Black-Box_Evasion_Attack_against_ML-based_Malicious_Traffic_Detection_Systems.md`

## §12 后续问题

1. 如何防御此类 RL-based 逃逸攻击？
2. Traffic-BERT 能否用于良性流量分类任务？
3. 探测阶段的流量是否会被检测系统标记？
4. 在更复杂的混合流量场景下效果如何？
5. 对抗流量的长期行为是否会暴露攻击？

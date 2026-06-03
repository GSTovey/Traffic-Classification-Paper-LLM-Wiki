---
type: paper
title_original: "DAIR-FedMoE: Hierarchical MoE for Federated Encrypted Traffic Classification under Compound Drift"
title_cn: "DAIR-FedMoE：面向复合漂移下联邦加密流量分类的层次化混合专家框架"
authors: ["Shamaila Fardous", "Kashif Sharif", "Fan Li", "Ali Asghar Manjotho", "Liehuang Zhu"]
year: 2025
venue: "TDSC"
doi: "unknown"
url: "unknown"
pdf: "00-inbox/PDFs/2025-TDSC-DAIR-FedMoE__Hierarchical_MoE_for_Federated_Encrypted_Traffic_Classification_under_Compound_Drift.pdf"
mineru_md: "02-parsed-markdown/2025-TDSC-DAIR-FedMoE__Hierarchical_MoE_for_Federated_Encrypted_Traffic_Classification_under_Compound_Drift.md"
status: processed
reading_level: L2
research_area: ["encrypted-traffic-analysis", "traffic-classification"]
task: ["federated-learning", "concept-drift-adaptation", "class-imbalance"]
method: ["mixture-of-experts", "transformer", "reinforcement-learning", "federated-learning"]
dataset: ["ISCX-VPN", "ISCX-Tor", "VNAT", "USTC-TFC2016"]
code: "https://github.com/dairfedmoe/DairFM"
relevance: high
created: "2026-06-03"
updated: "2026-06-03"
---

## §0 基础信息

| 字段 | 内容 |
|------|------|
| 论文标题 | DAIR-FedMoE: Hierarchical MoE for Federated Encrypted Traffic Classification under Compound Drift |
| 作者 | Shamaila Fardous, Kashif Sharif, Fan Li, Ali Asghar Manjotho, Liehuang Zhu |
| 机构 | Beijing Institute of Technology; Mehran University |
| 年份/期刊 | 2025 / IEEE TDSC |
| 代码 | https://github.com/dairfedmoe/DairFM |

## §1 一句话总结

提出 DAIR-FedMoE 框架，在联邦学习环境下通过层次化混合专家（HMoE）+ 熵引导损失重加权 + RL专家生命周期管理，首次同时应对加密流量分类中的特征漂移、概念漂移和标签漂移三重交织漂移问题。

## §2 摘要翻译

**原始摘要：** Federated learning (FL) offers a decentralized, privacy-preserving framework for encrypted traffic classification (ETC). However, real-world deployment faces compound client-specific feature, concept, and label drift, which degrades model performance. We propose DAIR-FedMoE, a Drift-Adaptive, Imbalance-Aware, RL-Managed Federated Mixture-of-Experts framework to simultaneously handle the drift triad with single-global model while minimizing computational and communication overhead. DAIR-FedMoE integrates a GShard Transformer with a hierarchical MoE layer that routes encrypted flows to either stable or drift-specialist experts based on per-client drift scores. Entropy-guided loss reweighting addresses dynamic label imbalance. A reinforcement learning-based policy dynamically manages the expert pool by spawning, pruning, and merging experts.

**中文翻译：** 联邦学习为加密流量分类提供去中心化、隐私保护的框架，但实际部署面临客户端特定的特征漂移、概念漂移和标签漂移的复合挑战。本文提出 DAIR-FedMoE，一种漂移自适应、不平衡感知、RL管理的联邦混合专家框架，在单一全局模型下同时处理三重漂移，同时最小化计算和通信开销。框架将 GShard Transformer 与层次化 MoE 层集成，基于每客户端漂移分数将加密流路由到稳定或漂移专家。熵引导损失重加权处理动态标签不平衡，RL策略动态管理专家池的创建、剪枝和合并。

## §3 方法动机

**痛点：**
- 联邦ETC面临三种漂移（特征P(X)、概念P(Y|X)、标签P(Y)）的交织纠缠，现有方法通常孤立处理其中一种或两种
- 多全局模型和个性化FL方法虽然能适应客户端差异，但带来巨大的计算、通信和存储开销
- 现有MoE方法（如FedMoE-DA）使用静态专家配置，无法动态调整专家池

**核心直觉：**
- 使用层次化MoE将流量分流到"稳定专家"和"漂移专家"两条路径
- 通过JS散度检测本地漂移程度，指导根门控路由决策
- 用熵来衡量专家对各类别的置信度，低置信类获得更高损失权重
- RL代理监控专家利用率和漂移趋势，动态管理专家生命周期

## §4 方法设计

**整体流程：** 输入加密流字节序列 → GShard Transformer编码 → HMoE层路由（漂移分数→根门控→稳定/漂移regime→regime内门控→专家选择）→ 分类头输出

**关键模块：**

1. **本地漂移检测：** 用JS散度比较当前窗口与历史窗口的特征分布，指数平滑降噪，得到漂移分数d_k(h)
2. **层次化MoE（HMoE）：** 两级门控——根门控决定走稳定还是漂移路径，regime内门控选择具体专家
3. **熵引导损失重加权：** 每个专家维护各类别的Shannon熵EMA，低置信类获得更高交叉熵权重
4. **RL专家生命周期管理：** 服务器端PPO策略网络，状态包括专家利用率、漂移参与度、置信度等，动作包括Prune/Spawn/Merge/NoOp

**隐私保护：** DP-SGD（高斯噪声注入+梯度裁剪）+ 安全聚合，后处理性质保证服务器端操作不削弱DP保证

**优点：** 首次统一处理三重交织漂移；单全局模型降低开销；RL自适应调整容量
**缺点：** 论文未明确说明同步FL假设下异步漂移的实际延迟影响；DP噪声可能影响漂移检测精度

## §5 与其他方法对比

| 方法 | 特征漂移 | 概念漂移 | 标签漂移 | 跨客户端 | 时变 |
|------|---------|---------|---------|---------|------|
| FedDrift | × | × | × | ✓ | ✓ |
| FedCCFA | × | × | ✓ | ✓ | × |
| FedMoE-DA | × | ✓ | × | ✓ | ✓ |
| **DAIR-FedMoE** | **✓** | **✓** | **✓** | **✓** | **✓** |

**创新点：** 首个探索MoE在漂移适应中潜力的工作；首次系统研究联邦ETC中交织漂移的影响

## §6 实验表现

**数据集：** ISCX-VPN, ISCX-Tor, VNAT, USTC-TFC2016（联邦分割）
**基线：** FedAvg, FedProx, FedNova, FedMoE-DA, FedDrift, FedCCFA 等
**指标：** Macro-F1, 少数类召回率, 漂移恢复速度
**关键结果：** DAIR-FedMoE 在所有数据集上取得最优macro-F1，在少数类召回率和漂移恢复速度方面显著优于基线，同时保持通信效率

## §7 学习与应用

- **开源代码：** https://github.com/dairfedmoe/DairFM
- **可复现性：** 提供了联邦分割设置和DP配置细节
- **迁移价值：** HMoE+漂移检测的思路可应用于其他联邦学习场景中的非平稳分布问题；RL专家管理策略可迁移到其他MoE架构

## §8 总结

**核心思想：** 在联邦加密流量分类中，通过层次化MoE将稳定和漂移流量分离处理，结合熵引导的损失重加权和RL驱动的专家池管理，统一应对特征/概念/标签三重交织漂移。

**快速流水线：**
```
加密流 → GShard Transformer → 漂移分数计算(JS散度) → 根门控路由
  → 稳定regime → 稳定专家池 → 分类
  → 漂移regime → 漂移专家池 → 分类
  → 熵引导损失重加权 → DP-SGD → 聚合
  → RL策略管理专家生命周期(剪枝/生成/合并)
```

## §9 知识链接

- [[encrypted-traffic-analysis]] — 加密流量分析
- [[traffic-classification]] — 流量分类
- [[transformer]] — GShard Transformer骨干网络
- [[few-shot-traffic-learning]] — 联邦学习下少量标注数据的利用

## §10 证据记录

| 声明 | 证据 |
|------|------|
| 三重漂移交织在联邦ETC中普遍存在 | Fig.1展示了五个客户端的漂移事件时间线 |
| 现有方法仅处理部分漂移 | Table I对比了8种方法的漂移覆盖情况 |
| HMoE能有效分离稳定和漂移流量 | 实验结果在4个数据集上验证 |
| RL管理能保持专家池效率 | 消融实验证明各组件贡献 |

## §11 原始资料链接

- PDF: `00-inbox/PDFs/2025-TDSC-DAIR-FedMoE__Hierarchical_MoE_for_Federated_Encrypted_Traffic_Classification_under_Compound_Drift.pdf`
- MinerU MD: `02-parsed-markdown/2025-TDSC-DAIR-FedMoE__Hierarchical_MoE_for_Federated_Encrypted_Traffic_Classification_under_Compound_Drift.md`

## §12 后续问题

- 在异步联邦设置下（非所有客户端同时参与），漂移检测和专家管理如何调整？
- DP噪声对漂移检测精度的具体影响程度如何？
- 能否将HMoE扩展到处理客户端间的对抗性攻击（而非仅分布偏移）？

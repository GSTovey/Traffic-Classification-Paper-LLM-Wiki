---
type: paper
title_original: "Proxied Traffic Fingerprinting for Hidden Service De-Anonymization With Burst Reshaping"
title_cn: "基于代理隐藏服务流量指纹与突发重塑的隐藏服务去匿名化"
authors:
  - Zeyu Li
  - Yipeng Wang
  - Xuebin Wang
  - Haoting Liu
  - Jiapeng Zhao
  - Jinqiao Shi
year: 2025
venue: "IEEE TIFS 2025"
doi: "10.1109/TIFS.2025.3588248"
url: "https://ieeexplore.ieee.org/document/11092853"
pdf: "00-inbox/PDFs/2025-TIFS-Proxied_Traffic_Fingerprinting_for_Hidden_Service_De-Anonymization_With_Burst_Reshaping.pdf"
mineru_md: "02-parsed-markdown/2025-TIFS-Proxied_Traffic_Fingerprinting_for_Hidden_Service_De-Anonymization_With_Burst_Reshaping.md"
status: processed
reading_level: L2
dataset:
  - "SCSD-dataset: 10 target HSs (static + dynamic), 4 traffic types (HST/MHST/CHST/PHST)"
  - "LCO-dataset: 103 target HSs, closed-world + open-world, labeled PHST + unlabeled HST + test HST"
code: "https://github.com/Lzreal/BurstReshapedPHST"
relevance: medium
research_area: ["网站指纹", "Tor匿名网络", "隐藏服务去匿名化"]
task: ["隐藏服务去匿名化", "Tor流量指纹攻击"]
method: ["代理隐藏服务", "突发重塑", "伪标签学习", "半监督学习"]
created: "2026-06-21"
updated: "2026-06-21"
---

# Proxied Traffic Fingerprinting for Hidden Service De-Anonymization With Burst Reshaping

## 0. 论文基础信息（表格）

| 项目 | 内容 |
|------|------|
| 原文标题 | Proxied Traffic Fingerprinting for Hidden Service De-Anonymization With Burst Reshaping |
| 中文标题 | 基于代理隐藏服务流量指纹与突发重塑的隐藏服务去匿名化 |
| 作者 | Zeyu Li, Yipeng Wang, Xuebin Wang, Haoting Liu, Jiapeng Zhao, Jinqiao Shi |
| 机构 | 北京邮电大学网络空间安全学院；北京工业大学计算机学院；中国科学院信息工程研究所 |
| 会议/期刊 | IEEE Transactions on Information Forensics and Security (TIFS), 2025 |
| 发表时间 | 2025年7月 |
| DOI | 10.1109/TIFS.2025.3588248 |
| 关键词 | Proxied hidden service traffic; hidden service de-anonymization; Proxy HS; traffic fingerprinting attack |
| 研究方向 | Tor隐藏服务去匿名化、流量指纹攻击 |
| 任务类型 | 隐藏服务域名识别（去匿名化） |
| 方法关键词 | Proxy HS; PHST; Burst Reshaping; burst reconstruction; pseudo-label learning |
| 数据集 | SCSD-dataset (10 HSs), LCO-dataset (103 HSs) |
| 是否开源 | 是 (https://github.com/Lzreal/BurstReshapedPHST) |

---

## 1. 一句话总结

> 提出代理隐藏服务（Proxy HS）获取代理隐藏服务流量（PHST）作为训练数据替代品，并通过突发重塑（Burst Reshaping）进一步弥合 PHST 与真实 HST 的差异，在动态 HS 去匿名化任务上达到 92.2% 准确率，分别超越 MHST 和 CHST 方法 72% 和 34%。

---

## 2. 摘要翻译

### 2.1 摘要原文

Traffic fingerprinting attack is a promising approach for Tor hidden services (HS) de-anonymization. However, it is inherently difficult to acquire traffic of target HSs (HST) for fingerprinting model training, because the physical location of the services is hidden due to the design of Tor protocol. In order to solve this problem, some alternatives such as mirrored HST (MHST) and client-side HST (CHST) have been proposed for training fingerprinting model. These alternatives are easy to acquire and aim to closely match the characteristics of the target HST. However, they cannot perfectly replace the target HST for the aspects of consistency of both response and protocol. In this paper, we propose a proxied fingerprinting approach called PF. A Proxy HS is deployed to acquire proxied HS traffic (PHST) as an alternative to conduct traffic fingerprinting attack, which satisfies both response and protocol consistency and is easy to acquire. In order to mitigate the impact introduced by Proxy HS, PF also introduces Burst Reshaping which includes burst reconstruction and pseudo-label learning to enhance the similarities between PHST and target HST. Experiments show that, PHST is a superior alternative to target HST, fingerprinting model trained using PF achieved an accuracy of 92.2%, surpassing the models trained with MHST and CHST by 72% and 34%, respectively. Additionally, PF is an add-on approach capable of improving the HS de-anonymization effectiveness of any fingerprinting model architecture.

### 2.2 摘要中文翻译

流量指纹攻击是 Tor 隐藏服务（HS）去匿名化的一种有前景的方法。然而，由于 Tor 协议设计使得服务的物理位置被隐藏，获取目标 HS 的流量（HST）用于指纹模型训练本质上是困难的。为解决此问题，已有研究提出了镜像 HST（MHST）和客户端 HST（CHST）等替代流量用于训练指纹模型。这些替代流量易于获取，旨在尽可能匹配目标 HST 的特征，但它们无法在响应一致性和协议一致性两方面同时完美替代目标 HST。本文提出一种代理指纹方法 PF，通过部署代理 HS 获取代理 HS 流量（PHST）作为替代流量，同时满足响应一致性和协议一致性，且易于获取。为减轻代理 HS 引入的影响，PF 还引入突发重塑（Burst Reshaping），包括突发重建和伪标签学习，以增强 PHST 与目标 HST 的相似性。实验表明，PHST 是目标 HST 的优越替代品，使用 PF 训练的指纹模型达到 92.2% 的准确率，分别超越 MHST 和 CHST 训练的模型 72% 和 34%。此外，PF 是一种可附加方法，能够提升任何指纹模型架构的 HS 去匿名化效果。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

Tor 隐藏服务去匿名化的流量指纹攻击面临一个核心困难：无法直接获取目标 HS 的流量（HST）用于训练。已有替代方案（MHST、CHST）各有缺陷——MHST 无法复制动态内容导致响应不一致，CHST 因客户端与 HS 执行不同 Tor 协议导致协议不一致。作者需要一种能同时满足响应一致性和协议一致性的替代流量。

### 3.2 现有方法的痛点和不足

| 现有方法 | 痛点 | 证据来源 |
|----------|------|----------|
| MHST（镜像HS流量） | 镜像HS仅能托管静态资源，无法复制动态内容（数据库查询、JS执行），导致响应不一致；动态HS场景下准确率仅20.22% | Table IV, §II |
| CHST（客户端HS流量） | 客户端与HS执行不同的Tor协议（如客户端需获取consensus文件、电路建立流程不同），导致协议不一致；准确率58.15% | Table IV, §II, Fig. 2 |
| Oracle模型（理想上界） | 需要直接获取目标HST，实际不可行，因为HS物理位置被Tor协议隐藏 | §I |

### 3.3 论文的研究假设或核心直觉

**核心直觉：** 代理HS（Proxy HS）作为一个特殊的HS实例，在Tor网络中透明转发客户端与目标HS之间的通信。由于Proxy HS本身运行Tor HS协议（协议一致性），且透明转发目标HS的响应数据（响应一致性），其流量PHST应与目标HST高度相似。同时，PHST与HST之间因路由引入的差异（非MTU包分布、额外控制包）可通过信号处理和半监督学习方法加以弥合。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|------|------|----------|
| 现象观察 | MHST和CHST作为HST替代品在去匿名化中有效，但性能显著低于理想上界（Oracle模型） | §I, §II |
| 痛点提炼 | MHST不满足响应一致性（动态HS），CHST不满足协议一致性——没有任何已有替代流量同时满足两个一致性 | Table I, §II |
| 问题转化 | 能否找到一种同时满足响应一致性和协议一致性的替代流量？如果存在因路由引入的微小差异，如何弥合？ | §II (C1, C2 challenges) |
| 文献定位 | 已有研究（Kwon 2015, Wang 2023）分别提出了MHST和CHST，但未解决两者的一致性缺陷；从未有研究考虑过Proxy HS这一中间实体 | §I, §II |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|------|----------|----------|----------|
| 核心假设 | PHST比MHST和CHST更接近HST，代理HS可作为获取替代流量的新范式 | Proxy HS同时执行HS协议（协议一致）并透明转发响应（响应一致） | 相似性分析（统计特征、会话相似度、信息泄漏）+ 去匿名化准确率对比 |
| 辅助假设1 | 突发重塑（burst reconstruction + pseudo-label learning）能有效弥合PHST与HST因路由引入的差异 | 非MTU包分布差异和额外控制包是已知的路由引入差异 | 消融实验（Table VI） |
| 辅助假设2 | PF是架构无关的附加方法，能提升任意指纹模型架构的性能 | 突发重塑作用于数据预处理和训练阶段，不改变模型架构 | 多架构实验（Table V: SDAE, DF, Var-CNN, RF） |

**假设验证结果：**

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|------|-----------|--------------|------|
| 核心假设 | 强支撑 | 动态HS场景：PF 92.2% vs MHST 20.22% vs CHST 58.15% | Table IV |
| 辅助假设1 | 支撑 | 消融：仅burst reconstruction提升至81.97%，仅pseudo-label learning提升至71.84%，两者结合85.34% | Table VI |
| 辅助假设2 | 支撑 | DF架构提升+15.44%，Var-CNN(pt)提升+7.34%，SDAE提升+8.86% | Table V |

---

## 4. 方法设计

### 4.1 方法整体流程

PF方法包含两个主要步骤：(1) 部署Proxy HS获取PHST；(2) 利用Burst Reshaping增强PHST与HST的相似性。具体流程为：在训练阶段，攻击者部署Proxy HS和受控客户端，通过Proxy HS访问目标HS获取带标签的PHST，同时通过受控客户端直接访问目标HS获取无标签的HST。PHST经过burst reconstruction预处理后用于初始模型训练，随后利用伪标签学习将无标签HST引入训练。在攻击阶段，对监控到的未知HST应用burst reconstruction后输入训练好的模型进行预测。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|------|------|----------|------|------|
| Proxy HS部署 | 目标HS域名 | 启动HS实例+客户端实例，Nginx反向代理+Socat双向通道 | 可转发请求的Proxy HS | 获取PHST的基础设施 |
| PHST采集 | Proxy HS + 受控客户端 | 客户端访问Proxy HS，在HS实例入口节点处抓包 | 带标签PHST | 替代HST的训练数据 |
| 无标签HST采集 | 目标HS + 受控客户端 | 客户端直接访问目标HS抓包 | 无标签HST | 伪标签学习的数据源 |
| Burst Identification | payload size序列 | 按536/1050字节分段 + 固定时间间隔阈值(inthr) | 分段后的bursts | 识别流量突发单元 |
| Burst Reshaping | 已识别bursts | 按Tor默认chunk size(4096B)切分为TLS记录，再按MTU分段为TCP包 | 重塑后的bursts | 模拟非路由场景的包分布 |
| Burst Embedding | 重塑bursts + 原始序列 | 将重塑bursts嵌回原始序列的对应位置，均匀分配时间戳 | 重塑后的payload size序列 | 完成burst reconstruction预处理 |
| 初始训练 | PHST + 重塑PHST | 用交叉熵损失训练指纹模型 init_epochs 轮 | 初步模型 | 建立HS区分能力 |
| 伪标签学习 | 无标签HST + 重塑HST | 高置信度样本(>threshold)伪标签，多轮混合训练 | 最终模型 | 使模型捕获HST特征分布 |
| 攻击预测 | 未知HST | burst reconstruction预处理 -> 模型预测 | HS域名分类结果 | 去匿名化 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|------|------|------|------|----------------|
| Proxy HS (HS实例) | 接收客户端请求，捕获PHST | 客户端请求 | PHST流量 + 转发请求 | 将请求转发给客户端实例 |
| Proxy HS (客户端实例) | 加密并转发请求至目标HS | 来自HS实例的请求 | 经Tor网络转发的请求 | 通过Tor电路连接目标HS |
| Burst Identification | 识别流量中的突发单元 | payload size序列 | 分段bursts | 输出给Burst Reshaping |
| Burst Reshaping | 模拟Tor TLS/TCP分包 | 识别的bursts | 重塑bursts | 输出给Burst Embedding |
| Pseudo-label Learning | 利用无标签HST进行半监督训练 | 模型预测 + 无标签HST | 伪标签训练数据 | 与初始训练共同构成损失函数 |

### 4.4 公式、算法和机制解释

**1. 初始训练损失函数 (Eq. 1)**

$$\mathcal{L}_{\text{init}} = -\sum_{c=1}^{C} \left[ y_{p,c} \log M(X_{p,c}) + y_{p,c} \log M(BR(X_{p,c})) \right]$$

其中 $X_{p,c}$ 为PHST的payload size序列，$BR(\cdot)$ 为burst reconstruction操作，$M(\cdot)$ 为模型参数，$y_{p,c}$ 为真实标签。该损失同时对原始序列和重塑序列进行监督，使模型学习两种表示下的HS特征。

**2. 伪标签学习损失函数 (Eq. 2)**

$$\mathcal{L}_{\text{pl}} = -\sum_{c=1}^{C} \left[ \hat{y}_{x_h} \log M(X_h) + \hat{y}_{BR(X_h)} \log M(BR(X_h)) \right]$$

其中 $\hat{y}_{x_h}$ 和 $\hat{y}_{BR(X_h)}$ 为置信度超过阈值的伪标签。仅高置信度样本参与训练以控制标签噪声。

**3. 总损失函数 (Eq. 3)**

$$\mathcal{L}_{\text{total}} = \begin{cases} \mathcal{L}_{\text{init}} & \text{初始训练阶段} \\ \mathcal{L}_{\text{init}} + \mathcal{L}_{\text{pl}} & \text{伪标签学习阶段} \end{cases}$$

**4. 信息泄漏度量 (Eq. 4)**

$$I(F; C) = H(C) - H(C|F)$$

用于量化流量特征 $F$ 对目标网站 $C$ 的区分能力，$H(\cdot)$ 为熵。

**5. Burst Reshaping 机制详解**

Burst reconstruction模拟Tor的TLS/TCP分包过程：将burst总字节数按4096字节chunk切分为TLS记录，再按MTU(1448字节)分段为TCP包。关键观察是：Proxy HS因无法解析目标HS TLS记录中的cell fragment，会将7个完整cell封装在一个TLS记录中发送，导致非MTU包分布与直接HST不同（Fig. 8）。Reshaping通过重新模拟分包过程消除这种差异。

**6. 伪标签学习策略**

- 初始训练 `init_epochs` 轮（选定15轮），建立基础HS区分能力
- 以置信度阈值0.95筛选高置信度伪标签样本
- 进行 `pseudo_times=8` 轮伪标签混合，每轮训练 `pseudo_per_epoch=5` 个epoch
- 每轮重新预测伪标签，逐步将模型决策边界从PHST分布向HST分布对齐

### 4.5 方法优势

1. **双一致性保证**：PHST同时满足响应一致性和协议一致性，是首个满足两个一致性的替代流量方案
2. **架构无关性**：Burst Reshaping作为数据预处理和训练策略附加于任意模型架构，不修改模型本身
3. **无需标签HST**：伪标签学习利用无标签HST进行半监督训练，解决了HST难以标注的问题
4. **实际可行性**：Proxy HS部署简单（类似标准HS），无需与目标HS物理或网络邻近
5. **对动态HS有效**：相比MHST在动态HS上准确率20.22%，PF达到92.20%

### 4.6 方法不足

1. **时间特征改善有限**：论文承认时间序列相似度因路由引入的延迟差异而降低，Burst Reshaping对此改善有限（§IX）
2. **需要部分HST数据**：伪标签学习需要无标签HST参与训练，攻击者仍需在ISP/AS层面获取目标HS的部分流量
3. **超参数敏感性**：burst identification的inthr阈值需针对PHST和HST分别调优（0.1s vs 0.05s），且伪标签学习涉及多个超参数（Table IX）
4. **闭世界假设**：主要实验在闭世界场景下进行，开世界场景精度仅60.14%
5. **Proxy HS可被检测**：目标HS管理员可能通过异常访问模式检测到Proxy HS的存在

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

已有方法（MHST、CHST）的共同局限是只能满足一致性条件中的一个：MHST满足协议一致性但不满足响应一致性（无法复制动态内容），CHST满足响应一致性但不满足协议一致性（客户端执行不同协议）。PF的核心创新在于找到一个全新的流量获取点——Proxy HS——它同时满足两个一致性条件。在此基础上，Burst Reshaping进一步弥合因路由引入的微小差异，这是已有研究未曾解决的问题。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|--------|----------|--------|------------|
| Proxy HS范式 | 提出代理HS作为获取替代流量的新中间实体，同时满足响应和协议一致性 | 高 | 是（可扩展至其他匿名网络分析） |
| PHST替代流量 | 首次证明PHST是HST的优越替代品，从统计特征、会话相似度、信息泄漏三维度验证 | 高 | 否（特定于Tor HS场景） |
| Burst Reconstruction | 基于Tor TLS/TCP分包机制的流量预处理技术，消除路由引入的非MTU包分布差异 | 中 | 是（可应用于其他Tor流量分析任务） |
| Pseudo-label Learning | 利用无标签HST进行半监督训练，逐步将决策边界从PHST对齐到HST | 中 | 是（半监督学习通用技术） |
| 架构无关附加方法 | PF可附加于任意指纹模型架构（SDAE, DF, Var-CNN, RF），均观察到性能提升 | 中 | 是 |

### 5.3 适用场景

- **执法机构去匿名化Tor隐藏服务**：在ISP/AS层面监控HS流量，利用Proxy HS训练指纹模型
- **动态HS去匿名化**：相比MHST在动态HS上几乎失效（20%），PF仍保持92%+准确率
- **流量分析研究**：Burst Reshaping技术可推广至其他需要比较不同网络位置流量相似性的场景

### 5.4 方法对比表

| 方法 | 替代流量 | 响应一致性 | 协议一致性 | 动态HS准确率 | 是否需要控制HS |
|------|----------|------------|------------|--------------|----------------|
| Oracle（理想上界） | HST | 是 | 是 | 98.48% | 否（但需获取HST） |
| MHST | 镜像HS流量 | 否 | 是 | 20.22% | 是（部署镜像HS） |
| CHST | 客户端HS流量 | 是 | 否 | 58.15% | 否 |
| PHST（无Burst Reshaping） | 代理HS流量 | 是 | 是 | 83.77% | 是（部署Proxy HS） |
| **PF（本文）** | **代理HS流量+重塑** | **是** | **是** | **92.20%** | **是（部署Proxy HS）** |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **指纹模型**：主要使用DF（Deep Fingerprinting）架构，扩展实验使用SDAE、Var-CNN、Robust Fingerprinting
- **输入表示**：payload size序列（带符号，符号表示方向，绝对值表示载荷大小）
- **评估场景**：闭世界（103个HS）和开世界（2800个非目标HS）
- **部署环境**：真实Tor网络，所有中继节点为不受控的志愿者节点

### 6.2 数据集

| 数据集 | 规模 | 用途 | 说明 |
|--------|------|------|------|
| SCSD-dataset | 10个目标HS（5静态+5动态） | 4种替代流量的初步对比 | 静态HS托管静态图片，动态HS仅返回HTML/JS |
| LCO-dataset (闭世界) | 103个目标HS | Burst Reshaping效果评估 | 标签集PHST 16,159条 + 无标签HST 7,469条 + 测试HST 7,519条 |
| LCO-dataset (开世界) | 204目标HS + 2800非目标HS | 开世界评估 | 标签集PHST 204条 + 无标签HST 657条 + 测试HST 2,883条 |

### 6.3 Baseline

- **Oracle模型**：用真实HST训练的理想上界
- **MHST模型**：用镜像HS流量训练
- **CHST模型**：用客户端HS流量训练
- **PHST模型**：用代理HS流量训练（无Burst Reshaping）
- **PF模型**：PHST + Burst Reshaping（本文方法）

### 6.4 评价指标

- 闭世界：Accuracy, Precision, Recall, F1
- 开世界：Accuracy, Precision, Recall, F1
- 相似性分析：Cosine similarity, Pearson correlation, Longest Common Subsequence, Information Leakage

### 6.5 关键实验结果

**SCSD-dataset（动态HS，主要结果）：**

| 模型 | Accuracy | Precision | Recall | F1 |
|------|----------|-----------|--------|-----|
| Oracle（上界） | 98.48% | 96.63% | 96.51% | 96.51% |
| MHST model | 20.22% | 19.60% | 20.09% | 7.95% |
| CHST model | 58.15% | 66.53% | 59.75% | 56.47% |
| PHST model | 83.77% | 88.29% | 83.41% | 82.38% |
| **PF model** | **92.20%** | **92.99%** | **92.49%** | **92.69%** |

**LCO-dataset（多架构对比）：**

| 模型架构 | PHST Accuracy | PF Accuracy | 提升 |
|----------|---------------|-------------|------|
| SDAE | 23.78% | 32.64% | +8.86% |
| **Deep Fingerprint** | **69.90%** | **85.34%** | **+15.44%** |
| Var-CNN(p) | 73.67% | 76.53% | +2.86% |
| Var-CNN(pt) | 70.24% | 77.58% | +7.34% |
| Robust Fingerprinting | 58.48% | 60.11% | +1.63% |

**消融实验（Burst Reshaping组件）：**

| 模型 | Burst Reconstruction | Pseudo-label Learning | Accuracy | F1 |
|------|---------------------|----------------------|----------|-----|
| PHST（基线） | 否 | 否 | 69.90% | 65.90% |
| PF(wo-Reco) | 否 | 是 | 71.84% | 67.44% |
| PF(wo-PL) | 是 | 否 | 81.97% | 77.81% |
| **PF** | **是** | **是** | **85.34%** | **81.19%** |

**开世界结果：**

| 模型 | Accuracy | Precision | Recall | F1 |
|------|----------|-----------|--------|-----|
| PHST model | 51.90% | 54.68% | 67.27% | 55.27% |
| PF model | 60.14% | 62.38% (+7.7%) | 77.28% | 65.44% |

### 6.6 优势最明显的场景

1. **动态HS去匿名化**：PF (92.20%) vs MHST (20.22%) vs CHST (58.15%)，差距最为显著
2. **DF架构下效果最佳**：Burst Reshaping在DF上提升+15.44%，因为DF主要依赖payload size序列
3. **Burst Reconstruction贡献最大**：单独使用即可从69.90%提升至81.97%（+12.07%），说明非MTU包分布差异是PHST与HST的主要差异来源

### 6.7 局限性

1. **开世界性能有限**：PF在开世界场景下precision仅62.38%，面对大量非目标HS时区分能力不足
2. **对时间特征模型改善较小**：Robust Fingerprinting（基于时间间隔）仅提升+1.63%
3. **依赖部分HST**：伪标签学习需要无标签HST，攻击者仍需具备ISP/AS级监控能力
4. **概念漂移和多标签识别**：论文承认这两个问题有待进一步探索（§IX）
5. **Proxy HS可被检测**：异常访问模式可能暴露Proxy HS的存在

---

## 7. 学习与应用

### 7.1 是否开源？

是。代码和数据集开源：https://github.com/Lzreal/BurstReshapedPHST

### 7.2 复现关键步骤

1. 在Tor网络中部署Proxy HS：启动HS实例（Nginx反向代理）+ 客户端实例（Socat双向通道）
2. 通过受控客户端访问Proxy HS和目标HS，分别采集PHST和HST
3. 对PHST和HST执行burst identification（inthr: PHST=0.1s, HST=0.05s）
4. 对识别的bursts执行burst reconstruction（按4096B chunk切分 -> 按1448B MTU分段）
5. 用PHST+重塑PHST初始训练15轮，再进行8轮伪标签混合训练（每轮5 epoch，置信度阈值0.95）

### 7.3 关键超参数、预处理和训练细节

| 超参数 | 值 | 说明 |
|--------|----|------|
| inthr (PHST) | 0.1s | PHST因路由延迟需更大阈值 |
| inthr (HST) | 0.05s | 直连HST使用较小阈值 |
| confidence_threshold | 0.95 | 伪标签置信度过滤阈值 |
| pseudo_times | 8 | 伪标签混合轮数 |
| pseudo_per_epoch | 5 | 每轮训练epoch数 |
| init_epoch | 15 | 初始训练epoch数 |
| Tor chunk size | 4096 bytes | TLS记录默认最大chunk |
| MTU | 1448 bytes | TCP包最大传输单元 |

### 7.4 能否迁移到其他任务？

- **Burst Reconstruction**可迁移到其他需要消除路由影响的Tor流量分析任务，特别是比较不同网络位置流量差异的场景
- **Pseudo-label Learning**是通用的半监督学习技术，可应用于任何存在标注数据不足问题的流量分类任务
- **Proxy HS范式**可扩展为其他匿名网络（如I2P）的中间代理分析方法

### 7.5 对我的研究有什么启发？

- **数据获取是关键**：在加密流量分析中，训练数据的获取点（网络位置）对模型性能有决定性影响。Proxy HS范式提示我们关注"在哪里采集数据"与"目标数据在哪里"之间的差异
- **领域知识驱动的预处理**：Burst Reshaping不是通用的数据增强，而是基于对Tor TLS/TCP分包机制的深入理解设计的。这说明流量分析中的预处理应充分利用协议领域知识
- **半监督学习解决标注瓶颈**：在实际网络监控场景中，标注数据往往稀缺，伪标签学习提供了一种渐进式知识迁移的有效范式

---

## 8. 总结

### 8.1 核心思想

> 代理HS获取替代流量，突发重塑弥合路由差异。

### 8.2 速记版 Pipeline

1. 部署Proxy HS（HS实例+客户端实例）获取PHST
2. 采集无标签HST作为伪标签学习数据源
3. Burst Identification + Burst Reconstruction预处理
4. PHST初始训练（15轮）建立基础区分能力
5. Pseudo-label Learning（8轮混合）对齐HST特征分布 -> 动态HS 92.2%准确率

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]]
- [[encrypted-traffic-analysis]]
- [[censorship-circumvention]]

### 9.2 相关方法

- Deep Fingerprinting (DF) — PF的主要骨干模型架构
- Mirror HS Traffic (MHST) — Kwon et al. 2015 提出的镜像替代方案
- Client-side HS Traffic (CHST) — Wang et al. 2023 提出的客户端替代方案
- Pseudo-label Learning — 半监督学习技术
- Tor Hidden Service Protocol — HS与客户端通过Rendezvous节点通信的协议

### 9.3 相关任务

- Tor隐藏服务去匿名化
- 网站指纹攻击
- 加密流量分类

### 9.4 可更新的综述页面

- [[survey-website-fingerprinting]]

### 9.5 可加入的对比表

- HS De-anonymization Alternative Traffic Comparison
- Tor Traffic Fingerprinting Attack Comparison

---

## 10. 证据记录（表格）

| 编号 | 关键观点 | 论文依据 | 位置 |
|------|----------|----------|------|
| E1 | PHST在动态HS上准确率92.20%，超越MHST(20.22%)和CHST(58.15%) | Table IV | §VI-B |
| E2 | Burst Reconstruction贡献最大（+12.07%），Pseudo-label Learning贡献较小（+1.94%） | Table VI | §VI-D |
| E3 | PF是架构无关的附加方法，在所有5种模型架构上均观察到性能提升 | Table V | §VI-C |
| E4 | DF架构下PF提升最显著（+15.44%），因为DF主要依赖payload size | Table V | §VI-C |
| E5 | PHST在统计特征、会话相似度、信息泄漏三维度均优于MHST和CHST | Fig. 10, 11, 12 | §VI-A |
| E6 | 非MTU包分布差异主要源于Tor cell fragmentation：Proxy HS无法解析cell fragment | Fig. 8 | §IV-B |
| E7 | PF在开世界场景下precision提升+7.7%（54.68% -> 62.38%） | Table X | §VI-G |
| E8 | 伪标签学习不依赖完整的无标签HS类别覆盖，仅10个HS即可达83.69% | Fig. 14 | §VI-E |
| E9 | 额外路由导致PHST比HST有更多控制包（固定大小TCP包），在连接早期尤为明显 | Fig. 6 | §IV-B |
| E10 | Proxy HS部署简单，类似标准HS，无需与目标HS物理邻近 | §IV-A | §IV-A |

---

## 11. 原始资料链接

- 论文 PDF: https://ieeexplore.ieee.org/document/11092853
- DOI: 10.1109/TIFS.2025.3588248
- 代码仓库: https://github.com/Lzreal/BurstReshapedPHST
- 本地 Markdown: `02-parsed-markdown/2025-TIFS-Proxied_Traffic_Fingerprinting_for_Hidden_Service_De-Anonymization_With_Burst_Reshaping.md`

---

## 12. 后续问题

1. Burst Reshaping对时间序列特征的改善有限，如何设计专门针对时间维度的路由差异消除方法？
2. Proxy HS是否可被目标HS管理员通过流量模式异常检测？是否存在隐蔽部署策略？
3. 在概念漂移（HS内容随时间变化）场景下，PHST模型的时效性如何？是否需要持续更新训练数据？
4. 多标签识别（一个HS对应多个.onion域名，或一个.onion域名对应多个HS）对PF的影响如何？
5. PF能否与流量混淆防御（如Tor pluggable transports）结合使用，或防御方如何针对Proxy HS范式设计对抗措施？
6. 在更真实的开世界场景中（数千个非目标HS），PF的precision-recall tradeoff如何优化？
7. Proxy HS范式能否扩展到分析其他匿名网络（如I2P、Lokinet）的隐藏服务？

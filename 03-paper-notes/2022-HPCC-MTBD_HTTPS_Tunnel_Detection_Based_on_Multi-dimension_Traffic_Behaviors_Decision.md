---
type: paper
title: "MTBD: HTTPS Tunnel Detection Based on Multi-dimension Traffic Behaviors Decision"
authors:
  - Bingxu Wang
  - Yangyang Guan
  - Gaopeng Gou
  - Peipei Fu
  - Zhen Li
  - Qingya Yang
  - Chang Liu
year: 2022
venue: HPCC
keywords:
  - HTTPS tunnel
  - multi-dimension traffic behaviors decision
  - traffic burst
  - tunnel detection
  - machine learning
topic: HTTPS隧道流量检测
status: processed
reading_level: L2
pdf: 00-inbox/PDFs/2022-HPCC-MTBD_HTTPS_Tunnel_Detection_Based_on_Multi-dimension_Traffic_Behaviors_Decision.pdf
created: "2026-05-27"
updated: "2026-05-27"
---

# MTBD: HTTPS Tunnel Detection Based on Multi-dimension Traffic Behaviors Decision

## 0. 基础信息

| 字段 | 内容 |
|------|------|
| 论文全称 | MTBD: HTTPS Tunnel Detection Based on Multi-dimension Traffic Behaviors Decision |
| 作者 | Bingxu Wang, Yangyang Guan, Gaopeng Gou, Peipei Fu, Zhen Li, Qingya Yang, Chang Liu |
| 机构 | Institute of Information Engineering, Chinese Academy of Sciences; University of Chinese Academy of Sciences |
| 发表时间/会议 | 2022 / HPCC (IEEE International Conference on High Performance Computing and Communications) |
| 研究领域 | 网络安全, 加密流量分析, HTTPS隧道检测 |
| 关键词 | HTTPS tunnel, multi-dimension traffic behaviors decision, traffic burst, machine learning |
| 代码/数据 | 未公开 |

## 1. 一句话总结

提出MTBD方法,通过流量突发过滤、多维度(流/主机/包)异构特征提取和投票决策机制三个阶段检测HTTPS隧道流量,在真实数据集上达到99%的precision和recall。

## 2. 摘要翻译

HTTPS协议是互联网上最重要的协议之一。网络防火墙通常不会阻止HTTPS协议,因此大量恶意软件利用HTTPS协议作为数据泄露的传输隧道。使用传统的握手指纹和序列检测方法难以准确检测HTTPS隧道。本文提出了MTBD方法,这是一种基于多维流量行为的多阶段检测方法。首先,设计流量突发检测算法过滤掉85%的正常流量。然后,为了避免单一维度特征的局限性,在流(flow)、主机(host)和包(packet)三个层级提取核心异构特征。最后,使用机器学习方法分别从上述三个维度构建模型,并投票决定最终结果。同时,构建HTTPS隧道服务并收集数据集以验证MTBD方法的有效性。实验结果表明,MTBD方法达到了高达99%的precision和recall,优于现有最优方法。

## 3. 研究动机与问题定义

### 3.1 研究背景

- HTTPS是互联网上使用最广泛的协议,网络防火墙一般不拦截HTTPS流量
- 大量恶意软件(如Metasploit的meterpreter HTTPS、Tor网络的Meek、CobaltStrike等)利用HTTPS隧道隐藏通信数据
- HTTPS隧道可通过HTTP CONNECT代理功能结合TLS服务构建,用于恶意传输、C&C通信、数据泄露等

### 3.2 现有方法的不足

| 方法类型 | 局限性 |
|----------|--------|
| TLS握手指纹检测 (Deep Packet Detection) | 不同工具可能使用相同指纹库,在开放环境中准确率无法保证;指纹特征容易被修改规避 |
| 传统机器学习方法 | 在封闭数据集上训练的模型泛化能力不足,更换网络场景后检测效果显著下降 |
| 深度学习方法 | 需要大量训练数据,可解释性较差 |

### 3.3 核心问题

HTTPS隧道检测效果差的根本原因在于**使用了单一维度的特征**,因为互联网上存在大量相似流量,导致大量误检。

## 4. 方法设计

### 4.1 Pipeline总览

MTBD方法包含三个阶段:

| 阶段 | 名称 | 目的 | 关键技术 |
|------|------|------|----------|
| Stage 1 | Burst Traffic Filtering (突发流量过滤) | 过滤掉与HTTPS隧道行为显著不同的正常流量 | Flow Burst Model, 过滤85%正常流量,仅损失1.9%隧道流量 |
| Stage 2 | Heterogeneous Features Extraction (异构特征提取) | 从三个维度提取区分性特征 | Flow特征(24维)、Host特征(18维)、Packet特征(300维) |
| Stage 3 | Traffic Detection and Voting (流量检测与投票) | 多维度分类器集成决策 | KNN/RF/SVM/DT分类器,多数投票决定最终结果 |

### 4.2 模块详解

#### Stage 1: 流量突发过滤 (Burst Traffic Filtering)

**核心思想**: 正常用户访问HTTPS服务时,流量分散到不同目的IP服务器;而HTTPS隧道通信时,流量会在短时间窗口内聚合到同一隧道服务器。

**Flow Burst Model参数**:

| 参数 | 含义 | 默认阈值 |
|------|------|----------|
| Mflow | 连续流数量 | >= 5 |
| Tavg | 流平均间隔时间 | <= 600ms |
| Tmax | 流最大间隔时间 | <= 900ms |
| Lavgpkt | 每流平均包数量 | >= 8 |

- 当上述条件同时满足时,该时间窗口内的三元组流量被识别为可疑HTTPS隧道流量
- 实验效果: 过滤超过85%正常HTTPS流量,仅损失1.9%隧道流量

**阈值选择依据**: 对50GB以上HTTPS隧道流量的长期观测和测量

#### Stage 2: 异构特征提取 (Heterogeneous Features Extraction)

在流量突发时间窗口内从三个维度提取特征:

| 维度 | 特征数量 | 特征类型 | 基于的元组 |
|------|----------|----------|------------|
| Flow (流) | 24维 | 包序列特征(包长度、时间间隔、方向)、统计特征(均值、方差等) | 四元组(server IP, server PORT, client IP, client PORT) |
| Host (主机) | 18维 | 流统计特征(流数量、包/字节总和/均值/方差)、时间间隔统计特征(最大/最小/均值/偏度/峰度) | 三元组(server IP, server PORT, client IP) |
| Packet (包) | 300维 | 包长度概率分布向量(以10字节为间隔,覆盖1-1500字节范围) | 三元组(server IP, server PORT, client IP) |

**Flow维度关键观察**: TLS握手阶段无明显差异,但数据传输阶段差异显著。HTTPS隧道握手后前两个包长度通常小于300字节,而正常HTTPS服务的HTTP请求/响应长度通常大于1000字节。

**Host维度时间间隔统计**: 使用偏度(skewness)和峰度(kurtosis)描述时间分布的对称性和形状。

#### Stage 3: 流量检测与投票 (Traffic Detection and Voting)

- 使用四种分类器: Random Forest, SVM, KNN, Decision Tree
- 三个维度分别训练独立分类器,不直接拼接特征输入集成学习
- 最终决策: 多数投票法(majority vote),至少2个维度判定为隧道则最终判定为隧道

### 4.3 算法伪代码

```
输入: 实时网络流量
输出: HTTPS隧道信息

1. 捕获实时流量
2. if Mflow >= 5 and Tavg <= 600ms and Tmax <= 900ms and Lavgpkt >= 8:
     创建Flow Burst窗口
   else:
     不创建窗口, 返回
3. 提取Flow/Host/Packet三维特征 Fflow, Fhost, Fpacket
4. 初始化投票参数 T = 0
5. 训练ML模型: KNN, RF, SVM, DT
6. if Fflow 被判定为隧道流量: T = T + 1
7. if Fhost 被判定为隧道流量: T = T + 1
8. if Fpacket 被判定为隧道流量: T = T + 1
9. if T >= 2: 判定为隧道流量
   else: 判定为正常流量
```

## 5. 方法对比与创新

### 5.1 创新点

| 创新点 | 描述 |
|--------|------|
| 多阶段多维度检测框架 | 首次提出将突发流量过滤与多维度异构特征投票决策相结合的HTTPS隧道检测方法 |
| 流量突发过滤机制 | 利用HTTPS隧道流量的突发特性,以极低的隧道流量损失(1.9%)过滤掉85%以上正常流量,大幅降低后续处理开销 |
| 异构特征投票决策 | 避免将异构特征直接拼接输入单一分类器,而是从Flow/Host/Packet三维度分别建模并投票,提升检测鲁棒性 |

### 5.2 与现有方法对比

| 方法 | 类型 | 特点 | 局限性 |
|------|------|------|--------|
| TLS握手指纹 (JA3等) | Deep Packet Detection | 分析TLS握手加密套件和扩展列表生成指纹 | 不同工具使用相同指纹,准确率低;指纹易被规避 |
| 机器学习方法 (Wang et al. [7]) | ML | 提取流特征检测Meek流量,98%准确率 | 在封闭数据集上效果好,开放场景泛化能力不足 |
| Deep Learning (CNN) [10] | DL | 一维CNN直接输入原始字节,自动选择特征 | 可解释性差,需要大量数据 |
| BLINC [16] | 行为检测 | 基于主机行为的流量识别 | 仅从主机单一维度分析 |
| DMT [13] | ML (对比基线) | 600维多级别特征+逻辑回归 | MTBD在P/R/F1上均优于DMT |
| FS-NET [14] | DL (对比基线) | RNN(GRU)挖掘序列特征 | MTBD在P/R/F1上均优于FS-NET |
| **MTBD** | **多阶段ML** | **突发过滤+三维特征+投票决策** | **不同恶意工具有独特实现方式,可能不适用所有场景** |

## 6. 实验与结果

### 6.1 实验环境

- 流量采集: 研究所实验室网关路由器部署被动流量探针
- 隧道构建: 使用Caddy技术基于HTTP CONNECT功能搭建HTTPS隧道;使用CobaltStrike获取HTTPS C&C隧道数据
- 流量分析工具: Cisco开源工具JOY
- 数据规模: 973,937条正常HTTPS流 + 26,841条HTTPS隧道流 (三天采集)
- 训练/测试划分: 60%训练集, 40%测试集

### 6.2 突发流量过滤效果

| Mflow (Flow Burst窗口流数量) | 正常流量过滤率 | HTTPS隧道召回率 |
|-------------------------------|----------------|-----------------|
| 3 | 71.4% | 99.1% |
| 4 | 76.2% | 98.4% |
| 5 (最终选择) | 85.7% | 98.1% |
| 6 | 87.5% | 92.2% |
| 7 | 89.6% | 86.6% |

选择Mflow=5的原因: 在保持98.1%隧道召回率的同时过滤85.7%正常流量;Mflow=6虽然过滤率更高但隧道损失达7.8%,不可接受。

### 6.3 不同维度与分类器的检测效果

| 维度 | RF (P/R/F1) | SVM (P/R/F1) | KNN (P/R/F1) | DT (P/R/F1) |
|------|-------------|--------------|--------------|-------------|
| Flow | 89.31/93.91/91.55 | 86.42/91.45/88.86 | 87.03/92.64/89.74 | 89.13/88.54/88.98 |
| Host | 87.14/92.77/89.86 | 85.67/91.97/88.70 | 87.15/92.67/89.81 | 85.98/91.84/88.81 |
| Packet | 82.81/84.94/83.86 | 82.19/84.31/83.23 | 81.38/83.97/82.65 | 81.57/83.24/82.39 |
| **MTBD (投票)** | **98.94/99.08/99.01** | 95.22/96.21/95.71 | 96.93/97.31/97.12 | 95.88/96.75/96.31 |

关键发现:
- Random Forest在所有维度和投票结果中均表现最优
- 三维投票决策显著优于任何单一维度(Packet维度最弱,Flow和Host维度相当)
- MTBD+RF组合达到最佳效果: Precision 98.94%, Recall 99.08%, F1 99.01%

### 6.4 与现有方法对比

| 方法 | Precision | Recall | F1 |
|------|-----------|--------|----|
| DMT [13] | 97.24% | 98.14% | 97.68% |
| FS-NET [14] | 97.07% | 98.03% | 97.54% |
| **MTBD** | **98.94%** | **99.08%** | **99.01%** |

MTBD在所有指标上均优于DMT和FS-NET方法。

## 7. 学习与应用

### 7.1 可借鉴的方法论

1. **多阶段检测思路**: 先用轻量级规则(突发过滤)大幅缩小候选集,再用复杂模型精检,适用于大规模流量实时检测场景
2. **异构特征分离建模+投票**: 避免将不同性质的特征强行拼接,保留各维度特征的独立判别能力,通过投票集成提升鲁棒性
3. **突发流量建模**: 利用隧道流量在时间窗口内聚合到同一服务器的行为特征,是一种高效的一阶过滤手段

### 7.2 可改进方向

- 论文自身指出: 不同恶意工具有独特的HTTPS隧道实现方式,方法可能不适用于所有恶意HTTPS检测
- Packet维度(300维概率分布)相对较弱,可考虑更精细的包级特征
- 未考虑对抗样本/对抗攻击场景下的鲁棒性
- 数据集仅来源于单一网络环境,跨场景泛化能力待验证

### 7.3 适用场景

- 企业网关HTTPS隧道流量实时检测
- 恶意软件C&C通信识别
- 数据泄露通道检测

## 8. 总结

本文提出MTBD方法用于HTTPS隧道流量检测。该方法包含三个阶段: (1) 利用流量突发特性过滤85%以上正常流量; (2) 从Flow、Host、Packet三个维度提取异构特征; (3) 分别训练分类器并通过多数投票做出最终决策。实验基于真实环境采集的近百万条HTTPS流数据,MTBD达到98.94% precision和99.08% recall,优于DMT和FS-NET等基线方法。该方法的核心贡献在于将多阶段过滤与多维度异构特征投票决策相结合,有效解决了单一维度特征导致的误检问题。

## 9. 知识链接

### 相关技术

- TLS Fingerprinting - JA3/JA3S等TLS握手指纹技术
- HTTPS Tunnel - HTTPS隧道技术原理(HTTP CONNECT代理)
- Traffic Burst Model - 流量突发模型
- Multi-dimension Feature Voting - 多维度特征投票决策机制

### 相关工具/恶意软件

- CobaltStrike - 商业渗透测试/攻击框架,使用HTTPS隧道通信
- Meek - Tor网络中的HTTPS混淆传输协议
- Metasploit Meterpreter - 远控工具,支持HTTPS模式
- Caddy - Web服务器,支持HTTP CONNECT代理功能

### 相关论文

- FS-NET - 使用RNN(GRU)进行加密流量分类 (本文对比基线)
- DMT - 使用600维多级别特征和逻辑回归的TLS恶意流量检测 (本文对比基线)
- BLINC - 基于主机行为的流量识别方法 (相关工作)

### 方法论关联

- Multi-stage Detection - 多阶段检测方法论
- Ensemble Voting - 集成投票决策机制
- Heterogeneous Features - 异构特征提取与融合

## 10. 证据记录

| 页码/章节 | 原文关键语句 | 个人批注 |
|-----------|-------------|----------|
| Abstract | "MTBD method achieves up to 99% precision and recall that is superior to state-of-the-art method" | 核心结果声明 |
| Section I | "The essential reason for the poor detection effect of HTTPS tunnel is the use of single dimension features" | 点明问题本质,多维度是本文核心出发点 |
| Section III-B | "more than 85% of normal HTTPS traffic are filtered out and only 1.9% of HTTPS tunnel traffic loss" | 突发过滤效果显著,以极低代价大幅缩小候选集 |
| Table II | "HTTPS tunnel: first two packets after TLS handshake is generally less than 300 bytes... normal HTTPS: greater than 1000 bytes" | Flow维度的关键区分信号 |
| Table V | MTBD+RF: P=98.94, R=99.08, F1=99.01 | 最佳组合的实验数据 |
| Section V | "different malicious tools have their unique HTTPS tunnel implementation methods. The method in this paper may not be applicable to all malicious HTTPS detection" | 作者自述局限性 |

## 11. 原始资料链接

- PDF: `00-inbox/PDFs/2022-HPCC-MTBD_HTTPS_Tunnel_Detection_Based_on_Multi-dimension_Traffic_Behaviors_Decision.pdf`
- Parsed Markdown: `02-parsed-markdown/2022-HPCC-MTBD_HTTPS_Tunnel_Detection_Based_on_Multi-dimension_Traffic_Behaviors_Decision.md`

## 12. 后续问题

1. MTBD方法在不同网络环境(如不同国家/地区、不同ISP)下的泛化能力如何?
2. 对于新兴的HTTPS隧道工具(如基于HTTP/2或QUIC的隧道),突发模型是否仍然有效?
3. Packet维度的300维概率分布特征是否可以通过降维或更精细的表示来提升检测效果?
4. 投票阈值(T>=2)的选择是否有理论依据?不同阈值设置对precision/recall的影响如何?
5. 是否可以引入自适应阈值机制,根据网络环境动态调整突发模型参数?
6. 对于低频、低带宽的HTTPS隧道(如间歇性C&C通信),突发特征不明显时如何检测?

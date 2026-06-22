---
type: paper
title_original: "An Automated Multi-Tab Website Fingerprinting Attack"
title_cn: "一种自动化多标签网站指纹攻击"
authors: [Qilei Yin, Zhuotao Liu, Qi Li, Tao Wang, Qian Wang, Chao Shen, Yixiao Xu]
year: 2022
venue: "IEEE TDSC 2022"
doi: "10.1109/TDSC.2021.3104869"
url: "unknown"
pdf: "00-inbox/PDFs/2022-TDSC-An_Automated_Multi-Tab_Website_Fingerprinting_Attack.pdf"
mineru_md: "02-parsed-markdown/2022-TDSC-An_Automated_Multi-Tab_Website_Fingerprinting_Attack.md"
status: processed
reading_level: L2
research_area: [website-fingerprinting, encrypted-traffic-analysis]
task: [multi-tab-website-fingerprinting, traffic-classification]
method: [balancecascade-xgboost, rfecv-feature-selection, split-point-detection]
dataset: [ssh-two-tab, tor-two-tab, alexa-top-websites]
code: "unknown"
relevance: medium
created: "2026-06-21"
updated: "2026-06-21"
---

# An Automated Multi-Tab Website Fingerprinting Attack

## §0 基础信息

| 项目 | 内容 |
|------|------|
| 论文全称 | An Automated Multi-Tab Website Fingerprinting Attack |
| 作者 | Qilei Yin, Zhuotao Liu, Qi Li, Tao Wang, Qian Wang, Chao Shen, Yixiao Xu |
| 机构 | 清华大学, 西安交通大学, Simon Fraser University, 武汉大学, 中科院 |
| 发表时间 | 2022 |
| 会议/期刊 | IEEE Transactions on Dependable and Secure Computing (TDSC) |
| 前序工作 | ACSAC 2018 preliminary version [1] |

## §1 一句话总结

放松单标签假设，提出两阶段自动化多标签WF攻击：先用BalanceCascade-XGBoost动态定位流量分割点提取初始干净流量块，再用基于RFECV特征选择的XGBoost分类器仅凭初始数据块识别网站，在SSH/Tor双标签数据集上分别达到约0.97和0.90的TPR。

## §2 摘要翻译

### 2.1 摘要原文

In Website Fingerprinting (WF) attack, a local passive eavesdropper utilizes network flow information to identify which web pages a user is browsing. Previous researchers have demonstrated the feasibility and effectiveness of WF attacks under a strong Single Page Assumption: the network flow extracted by the adversary belongs to a single web page. In reality, the assumption may not hold because users tend to open multiple tabs simultaneously (or within a short period of time) so that their network traffic is mixed. In this article, we propose an automated multi-tab Website Fingerprinting attack that is able to accurately classify websites regardless of the number of simultaneously opened pages. Our design is powered by two innovative designs. First, we develop a split point classification method to dynamically identify the split point between the first page and its subsequent pages. As a result, the network traffic before the split point is solely generated for the first page. Then, we propose a new chunk-based WF classifier to infer the websites based on the initial chunk of clean traffic. For both classifiers, we apply automated feature selection to select a concise yet representative feature set.

### 2.2 摘要中文翻译

在网站指纹（WF）攻击中，本地被动窃听者利用网络流信息来识别用户正在浏览的网页。先前的研究人员已经在强单标签假设下证明了WF攻击的可行性和有效性：攻击者提取的网络流属于单个网页。然而在现实中，该假设可能不成立，因为用户倾向于同时打开多个标签页（或在短时间内），导致其网络流量混合。本文提出一种自动化多标签网站指纹攻击，能够准确分类网站，不受同时打开页面数量的影响。设计包含两个创新：（1）开发分割点分类方法，动态识别第一个页面与后续页面之间的分割点，从而使得分割点之前的网络流量仅由第一个页面生成；（2）提出新的基于数据块的WF分类器，仅基于初始干净流量块推断网站。两个分类器均采用自动化特征选择来选取简洁但有代表性的特征集。

## §3 方法动机

### §3.1 痛点问题

- **单标签假设不现实**：现有WF攻击均假设每次只加载一个页面，但实际用户经常同时打开多个标签页 [5][6][7]
- **混合流量使传统攻击失效**：多标签浏览导致流量混合，Juarez et al. [5] 证明传统WF攻击在混合流量下失效
- **固定特征集泛化性差**：使用固定特征集无法适应复杂多变的网络环境
- **数据类别不平衡**：分割点识别中，真实分割点只有一个而虚假分割点可能有数百个（比例可达1:461）

### §3.2 核心直觉

- 多标签页面是**顺序加载**的：用户在打开第一个页面后，通常需要阅读时间才会打开后续页面
- 在第二个页面开始加载之前，**所有网络包仅由第一个页面生成**，这段流量是"干净的"
- 因此只需准确定位**分割点**（第二个页面开始加载的时间点），即可提取初始干净流量块进行分类

### §3.3 问题发现路径

| 阶段 | 内容 | 证据来源 |
|------|------|----------|
| 现象观察 | 用户实际浏览中经常同时/快速打开多个标签页，Juarez et al. [5] 实证发现传统WF在混合流量下失效 | §I, [5][6][7] |
| 痛点提炼 | (1) 单标签假设是WF领域的重大限制；(2) 已有多标签方法（Gu et al. [22] TPR仅75.9%、Wang & Goldberg [7]）性能不足 | §II, [22][7] |
| 问题转化 | 从"如何分离混合流量"转化为"如何准确定位分割点+仅用初始块分类"——避免复杂的流量分离问题 | §III |
| 文献定位 | 位于WF攻击从单标签到多标签的演进中。Gu et al. [22] 和 Wang & Goldberg [7] 是直接前驱，本文在分割精度和分类性能上均有显著提升 | §II |

### §3.4 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|------|----------|----------|----------|
| 核心假设 | 多标签页面顺序加载的特性使得分割点存在且可被机器学习方法准确识别 | 多标签浏览行为观察 [6] | 分割精度实验 (Tables 1-2) |
| 辅助假设 1 | 初始干净流量块包含足够信息用于网站分类，即使块很短（仅2秒） | 网站加载初期的HTML/CSS/JS请求具有独特模式 | Chunk分类实验 (Fig.5) |
| 辅助假设 2 | 自动化特征选择（RFECV）可在不损失精度的前提下大幅减少特征数量 | 特征冗余普遍存在 | 特征数量对比 (Tables 3-4, 6-7) |
| 辅助假设 3 | BalanceCascade集成欠采样能有效处理分割点识别中的严重类别不平衡 | 集成方法在不平衡学习中表现优异 [25] | 不平衡度实验 (Fig.3) |

**假设验证结果：**

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|------|-----------|-------------|------|
| 核心假设 | 强支撑 | SSH分割精度0.902，Tor分割精度0.959 | Tables 1-2 |
| 辅助假设 1 | 支撑 | 2秒chunk在SSH上TPR=0.955，Tor上TPR=0.721 | §6.3 |
| 辅助假设 2 | 支撑 | RFECV将特征从110减至5-11个（分割）或从302减至7-22个（分类），精度基本不变 | Tables 3-4, 6 |
| 辅助假设 3 | 支撑 | BalanceCascade-XGBoost在各种不平衡度下稳定优于time-kNN | Fig.3 |

## §4 方法设计

**整体流程：**

```
输入: 多标签浏览会话的加密网络流量
  ↓
Phase I: 动态页面分割（Dynamic Page Split）
  ├─ Step 1: 动态特征生成
  │   - 对每个出站包提取110个特征（4倍于原始23个特征）
  │   - 包括包间隔时间、统计量、传输时间等
  ├─ Step 2: 自动特征选择（RFECV）
  │   - 递归特征消除 + 交叉验证
  │   - 以Decision Tree为估计器，AUC为评估指标
  │   - 自动确定最优特征数量（通常5-11个）
  └─ Step 3: BalanceCascade-XGBoost分类
      - BalanceCascade集成欠采样处理类别不平衡
      - 为每个训练子集构建弱XGBoost分类器
      - 最终分类器为所有弱分类器的平均
      - 选择概率最高的出站包作为真实分割点
  ↓
初始干净流量块（分割点之前的网络包）
  ↓
Phase II: 基于数据块的网站分类（Chunk-Based Classification）
  ├─ Step 4: 特征提取（302个候选特征）
  │   - 包大小/数量统计、包间隔时间统计
  │   - 传输时间四分位数、传输速度
  │   - CSOP（累积包大小）、Burst特征
  ├─ Step 5: RFECV特征选择
  │   - 自动选择简洁特征子集（通常10-22个）
  │   - 排除相似度特征（FLLD、Jacquard）以提高效率
  └─ Step 6: XGBoost多分类
      - 使用softmax目标函数
      - 输出网站类别
  ↓
输出: 第一个被访问的网站标签
```

### §4.2 详细Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|------|------|----------|------|------|
| Step 1 | 原始网络流量 | 为每个出站包提取110个特征（包间隔时间、统计量、方向等） | 110维特征向量 | 丰富特征表达 |
| Step 2 | 110维特征向量 | RFECV递归消除+交叉验证，Decision Tree估计器 | 5-11个关键特征 | 降维提效 |
| Step 3 | 精简特征+标签 | BalanceCascade欠采样→训练多个弱XGBoost→集成平均 | 分割点概率 | 处理类别不平衡 |
| Step 4 | 初始流量块 | 提取302个候选特征（包大小、间隔、速度、CSOP等） | 302维特征向量 | 网站指纹刻画 |
| Step 5 | 302维特征向量 | RFECV特征选择 | 7-22个关键特征 | 降维提效 |
| Step 6 | 精简特征+网站标签 | XGBoost softmax多分类 | 网站类别 | 最终分类 |

### §4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|------|------|------|------|----------------|
| 动态特征生成器 | 将固定特征集扩展为参数化动态特征集 | 每个出站包的原始特征 | 110维特征向量 | 为RFECV提供候选特征 |
| RFECV特征选择器 | 自动确定最优特征子集 | 候选特征集+训练标签 | 精简特征子集 | 两个Phase均使用 |
| BalanceCascade欠采样器 | 处理严重类别不平衡 | 不平衡训练集 | 多个平衡训练子集 | 为XGBoost提供训练数据 |
| XGBoost分割点分类器 | 识别真实分割点 | 精简特征 | 分割概率 | Phase I核心 |
| XGBoost网站分类器 | 分类网站 | 精简特征 | 网站类别 | Phase II核心 |

### §4.4 关键公式

**BalanceCascade-XGBoost 集成分类器：**

$$F(x) = \frac{1}{n} \sum_{i=1}^{n} f_i(x)$$

其中 $f_i$ 是在第 $i$ 个BalanceCascade训练子集上训练的弱XGBoost分类器，$n$ 是训练子集总数。

**BalanceCascade欠采样过程：**
- 原始训练集 $D$ 中，真实分割点子集 $P$，虚假分割点子集 $N$，不平衡比 $b:1$
- 第 $i$ 轮：随机从 $N$ 中抽取 $|N_i| = |P|$ 个样本，与 $P$ 组成平衡子集 $D_i$
- 用 $D_i$ 训练kNN（k=1），移除 $N$ 中被正确分类的样本
- 重复直到生成 $n$ 个训练子集

**分割点识别：** 测试阶段对每个出站包计算属于真实分割点的概率，选择概率最高的包作为分割点。

**分割精度定义：** 预测分割点在真实分割点前后25个包范围内即为正确（与time-kNN [7]一致）。

### §4.5 方法优势

- **自动化**：RFECV自动确定最优特征数量，无需人工调参
- **高效性**：特征数量从110/302大幅减少到5-22个，训练时间降低约10倍
- **鲁棒性**：BalanceCascade有效处理高达1:100的类别不平衡
- **灵活性**：动态特征生成适应不同网络条件

### §4.6 方法不足

- 仅识别第一个页面，后续页面因混合流量无法分类
- 对BuFLO防御几乎无效（SSH TPR=0.112，Tor TPR=0.02）
- 流媒体/长时间后台流量会干扰分割点定位
- 测试时间（约17-20ms/实例）高于传统单标签分类器

## §5 与其他方法对比

### §5.1 与主流方法的本质区别

传统WF攻击（k-FP、CUMUL、DF等）基于**单标签假设**，直接对完整流量进行分类。Wang & Goldberg [7] 的time-kNN方法尝试基于时间间隔分割流量，但使用固定特征集且分割精度有限。本文采用**"动态分割+初始块分类"两阶段范式**：先通过BalanceCascade-XGBoost精确定位分割点提取干净流量，再仅用初始块进行网站分类。核心区别在于：（1）自动化特征选择替代固定特征集；（2）集成欠采样处理类别不平衡；（3）XGBoost替代kNN/SVM提升分类能力。

### §5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|--------|----------|--------|-----------|
| 两阶段攻击框架 | 分割点识别+初始块分类的解耦设计 | 高 | 是 -- 适用于任何顺序加载的多流混合场景 |
| 动态特征生成+RFECV | 将固定特征集参数化为110个候选，RFECV自动选择最优子集 | 高 | 是 -- 特征工程通用方法 |
| BalanceCascade-XGBoost | 集成欠采样+梯度提升处理严重类别不平衡 | 高 | 是 -- 不平衡分类通用 |
| 初始块分类 | 仅用分割点前的干净流量进行分类，避免混合流量分离 | 中 | 是 -- 早期流量识别通用 |
| 去除相似度特征 | 排除FLLD等计算昂贵且不可迁移的特征 | 中 | 改善实际部署效率 |

### §5.4 方法对比表

| 方法 | 多标签支持 | 分割精度 | SSH TPR | Tor TPR | 特征数量 | 类别不平衡处理 |
|------|-----------|----------|---------|---------|----------|---------------|
| k-FP [3] | 不支持 | - | 混合流量下失效 | 混合流量下失效 | 随机森林 | 无 |
| CUMUL [4] | 不支持 | - | 混合流量下失效 | 混合流量下失效 | 104 | 无 |
| DF [21] | 不支持 | - | 混合流量下失效 | 混合流量下失效 | CNN自动 | 无 |
| time-kNN [7] | 部分支持 | 0.44-0.84 | ~0.36 | ~0.47 | 23 | 无 |
| Gu et al. [22] | 部分支持 | - | 0.759 | - | 精细特征 | 无 |
| 本文初步 [1] | 支持 | 0.81-0.91 | ~0.89 | ~0.87 | 23 | BalanceCascade |
| **本文新方法** | **支持** | **0.81-0.96** | **~0.97** | **~0.90** | **5-22** | **BalanceCascade-XGBoost** |

## §6 实验表现

### §6.1 实验设计和设置

- **闭世界**：50个监控网站，每个50训练+50测试实例
- **开世界**：50个监控+2500个非监控网站
- **两标签数据集**：预定义时间间隔（2-6秒）+ 随机延迟（0-1秒）
- **多标签数据集**：3/4/5标签，初始间隔2秒
- **评估指标**：TPR（真阳率）、FPR（假阳率）
- **分割精度**：预测点在真实点前后25包内为正确

### §6.2 数据集

| 数据集 | 类型 | 标签数 | 间隔 | 实例数 | 通道 |
|--------|------|--------|------|--------|------|
| SSH_normal | 单标签 | 1 | - | 50网站×100实例 | SSH |
| Tor_normal | 单标签 | 1 | - | 50网站×100实例 | Tor |
| SSH_two_2s-6s | 双标签 | 2 | 2-6s | 50网站×50实例 | SSH |
| Tor_two_2s-6s | 双标签 | 2 | 2-6s | 50网站×50实例 | Tor |
| SSH_three/four/five_2s | 多标签 | 3/4/5 | 2s | - | SSH |
| Tor_three/four/five_2s | 多标签 | 3/4/5 | 2s | - | Tor |

### §6.3 Baseline

- **time-kNN** [7]：基于时间间隔的kNN分割+分类
- **k-FP** [3]：基于随机森林的网站指纹
- **CUMUL** [4]：基于SVM的104特征分类
- **Deep Fingerprinting (DF)** [21]：基于深度学习（SDAE/CNN/LSTM）
- **BalanceCascade-XGBoost (初步)** [1]：本文ACSAC 2018版本

### §6.4 关键实验结果

**Phase I -- 分割点识别精度：**

| 数据集 | RFECV+BX | BX [1] | time-kNN [7] | 提升(vs time-kNN) |
|--------|----------|--------|-------------|-------------------|
| SSH_two_2s | 0.805 | 0.810 | 0.748 | +7.6% |
| SSH_two_4s | 0.832 | 0.833 | 0.778 | +6.9% |
| SSH_two_6s | 0.902 | 0.913 | 0.841 | +7.3% |
| Tor_two_2s | 0.959 | 0.958 | 0.751 | +27.7% |
| Tor_two_4s | 0.880 | 0.874 | 0.718 | +22.6% |
| Tor_two_6s | 0.846 | 0.842 | 0.691 | +22.4% |

**Phase II -- Chunk分类TPR（闭世界）：**

| 数据集 | 本文新 | 本文初步 | DF | k-FP | CUMUL |
|--------|--------|---------|-----|------|-------|
| SSH (最佳chunk) | **0.957** | 0.92 | 0.88 | 0.87 | 0.75 |
| Tor (最佳chunk) | **0.843** | 0.84 | 0.83 | 0.74 | 0.65 |

**集成攻击TPR（双标签）：**

| 数据集 | 本文新 | 本文初步 | DF | k-FP | CUMUL |
|--------|--------|---------|-----|------|-------|
| SSH_two_6s | **0.97** | 0.892 | 0.363 | 0.219 | 0.125 |
| Tor_two_6s | **0.895** | 0.874 | 0.475 | 0.156 | 0.137 |

**多标签分割精度：**

| 数据集 | 分割精度 |
|--------|----------|
| SSH_five_2s | 0.743 |
| Tor_five_2s | 0.781 |

### §6.5 优势最明显的场景

- **Tor通道**：分割精度提升最大（最高+32.3%），因Tor包大小统一使得时间特征更重要
- **短间隔场景**：2秒间隔下仍保持高精度，证明方法对快速浏览的适应性
- **集成攻击**：相比传统方法提升高达167.2%，因传统方法在混合流量下几乎失效

### §6.6 局限性

- **BuFLO防御**：恒定包大小和间隔的防御使所有方法几乎失效（TPR接近随机）
- **Decoy Page**：对Tor数据集影响严重（TPR降至0.159）
- **流媒体干扰**：长时间后台流量使干净块无法提取
- **仅识别第一个页面**：后续页面因混合无法分类
- **Chunk大小不匹配**：训练和测试的chunk大小不一致时性能下降

## §7 学习与应用

### §7.1 是否开源

未明确开源。

### §7.2 复现关键步骤

1. 收集多标签浏览流量（PhantomJS/Tor Browser + tcpdump），标注分割点时间
2. 实现动态特征生成：对每个出站包提取110个特征（包间隔、统计量、方向等）
3. 实现RFECV特征选择：以Decision Tree为估计器，AUC为指标，自动确定最优特征数
4. 实现BalanceCascade欠采样：kNN（k=1）迭代移除易分类的负样本
5. 训练XGBoost分割点分类器：集成多个弱分类器
6. 提取初始chunk的302个候选特征，RFECV选择子集
7. 训练XGBoost softmax多分类器
8. 集成测试：分割→提取chunk→分类

### §7.3 关键超参数

| 超参数 | 值 | 说明 |
|--------|-----|------|
| 不平衡度 b | 10 | 负样本/正样本比例（经验值） |
| RFECV step | 1 | 每轮移除特征数（小值=精细） |
| RFECV cv | 5 | 交叉验证折数 |
| 分割精度范围 | ±25包 | 预测点容差范围 |
| 初始chunk大小 | 2-6秒 | 分类使用的流量时长 |
| BalanceCascade kNN k | 1 | 欠采样中的kNN参数 |

### §7.4 能否迁移到其他任务

- **加密隧道流量分类**：分割点识别思路可迁移到VPN/代理流量中的应用识别
- **早期流量分类**：初始chunk分类方法适用于需要快速判断的场景
- **不平衡网络安全检测**：BalanceCascade-XGBoost适用于恶意流量检测等不平衡场景
- **自动化特征选择**：RFECV框架可应用于各种流量分类任务

### §7.5 对研究的启发

1. **顺序加载假设是多标签WF的关键突破口**：利用页面加载的时间顺序性避免了复杂的流量分离问题
2. **特征工程仍有价值**：在WF领域，精心设计的手工特征+自动化选择在小数据集上仍优于深度学习
3. **类别不平衡是分割点识别的核心挑战**：集成欠采样比简单欠采样更有效
4. **防御与攻击的军备竞赛**：BuFLO等强防御仍是最有效的对抗手段

## §8 总结

### 8.1 核心思想

> 两阶段攻击：分割点定位+初始块分类，自动特征选择处理多标签WF。

### 8.2 速记版Pipeline

1. 观察到多标签页面顺序加载，分割点前流量干净
2. Phase I：110特征→RFECV选择5-11个→BalanceCascade-XGBoost定位分割点
3. Phase II：302特征→RFECV选择7-22个→XGBoost softmax分类网站
4. SSH双标签TPR~0.97，Tor双标签TPR~0.90
5. 对BuFLO等强防御仍然脆弱

## §9 知识链接

### §9.1 相关概念

- [[website-fingerprinting]] -- 网站指纹识别技术
- [[encrypted-traffic-analysis]] -- 加密流量分析

### §9.2 相关方法

- [[survey-website-fingerprinting]] -- 网站指纹综述
- [[traffic-classification]] -- 流量分类通用方法

### §9.3 相关任务

- multi-tab-website-fingerprinting -- 多标签网站指纹
- tor-traffic-analysis -- Tor流量分析

### §9.4 可更新的综述页面

- [[survey-website-fingerprinting]] -- 可加入多标签WF攻击对比

### §9.5 跨论文关联

- [[2023-S&P-Robust_Multi-tab_Website_Fingerprinting_Attacks_in_the_Wild]] -- 同组作者的后续工作，ARES将多标签WF建模为多标签分类问题，使用Transformer替代手工特征
- [[2018-CCS-Deep_Fingerprinting_Undermining_Website_Fingerprinting_Defenses_with_Deep_Learning]] -- DF是本文的重要Baseline，深度学习方法在混合流量下同样失效
- [[2024-INFOCOM-Causality_Correlation_and_Context_Learning_Aided_Robust_Lightweight_Multi-Tab_Website_Fingerprinting_Over_Encrypted_Tunnel]] -- 后续多标签WF工作
- [[2020-CCS-TrafficSliver-Fighting_Website_Fingerprinting_Attacks_with_Traffic_Splitting]] -- 流量分割防御方法

## §10 证据记录

| 编号 | 声明 | 证据 | 位置 |
|------|------|------|------|
| E1 | 传统WF攻击在多标签混合流量下失效 | Juarez et al. [5] | §I |
| E2 | RFECV+BX在Tor双标签分割精度达0.959，比time-kNN提升最高32.3% | Table 2 | §6.2 |
| E3 | RFECV将分割特征从23减至5-11个，精度基本不变 | Tables 3-4 | §6.2 |
| E4 | 最佳SSH chunk TPR=0.957（5秒），Tor chunk TPR=0.843（4秒） | Fig.5 | §6.3 |
| E5 | 2秒chunk的SSH TPR=0.955，Tor TPR=0.721 | Fig.5 | §6.3 |
| E6 | 集成攻击SSH_two_6s TPR=0.97，比最佳基线DF提升167.2% | Fig.6 | §6.4 |
| E7 | 集成攻击Tor_two_6s TPR=0.895 | Fig.6 | §6.4 |
| E8 | 5标签场景下分割精度仍达0.743(SSH)和0.781(Tor) | Table 5 | §6.2 |
| E9 | BuFLO防御使所有方法几乎失效（TPR~0.02-0.112） | Table 11 | §6.3 |
| E10 | RFECV特征选择将训练时间降低约10倍 | Table 7 | §6.3 |
| E11 | 不平衡度b=10为最优经验值 | Fig.3 | §6.2 |
| E12 | chunk大小不匹配时性能下降（训练3s测试5s：TPR从0.91降至0.76） | Fig.8 | §7 |

## §11 原始资料链接

- PDF: `00-inbox/PDFs/2022-TDSC-An_Automated_Multi-Tab_Website_Fingerprinting_Attack.pdf`
- MinerU Markdown: `02-parsed-markdown/2022-TDSC-An_Automated_Multi-Tab_Website_Fingerprinting_Attack.md`

## §12 后续问题

1. 如何将方法扩展到同时识别多个标签页的网站（而非仅第一个）？
2. 对抗BuFLO等强防御的可能方向是什么？
3. 流媒体/长连接场景下如何保证分割点定位的鲁棒性？
4. 深度学习方法（如后续ARES的Transformer）是否能在小数据集上替代手工特征+XGBoost？
5. 在真实Tor网络部署中，概念漂移对特征选择稳定性的影响如何？
6. chunk大小不匹配问题是否可通过自适应选择训练chunk大小来缓解？

---
type: paper
title_original: "Censored Planet: An Internet-wide, Longitudinal Censorship Observatory"
title_cn: "Censored Planet: 互联网规模的纵向审查观测平台"
authors: ["Ram SundaraRaman", "Prerana Shenoy", "Katharina Kohls", "Roya Ensafi"]
year: 2020
venue: "ACM CCS 2020"
doi: "10.1145/3372297.3417883"
url: "https://censoredplanet.org"
pdf: "00-inbox/PDFs/2020-CCS-Censored_Planet__An_Internet-wide__Longitudinal_Censorship_Observatory.pdf"
mineru_md: "unknown"
status: processed
reading_level: L3
research_area: ["censorship-measurement", "internet-freedom", "network-security", "anomaly-detection"]
task: ["censorship-detection", "anomaly-detection", "trend-analysis", "longitudinal-measurement"]
method: ["remote-measurement", "time-series-analysis", "bitmap-anomaly-detection", "Nelder-Mead-optimization", "Mann-Kendall-test"]
dataset: ["CensoredPlanet", "OONI", "ICLab", "CitizenLab Test List", "Alexa Top Domains"]
code: "https://github.com/censoredplanet"
relevance: high
created: "2026-06-14"
updated: "2026-06-14"
---

# Censored Planet: An Internet-wide, Longitudinal Censorship Observatory

## 0. 论文基础信息

| 项目 | 内容 |
|------|------|
| 原文标题 | Censored Planet: An Internet-wide, Longitudinal Censorship Observatory |
| 中文标题 | Censored Planet: 互联网规模的纵向审查观测平台 |
| 作者 | Ram SundaraRaman, Prerana Shenoy, Katharina Kohls, Roya Ensafi |
| 年份 | 2020 |
| 会议/期刊 | ACM CCS 2020 |
| 研究方向 | 互联网审查测量、网络自由、全球互联网可达性监测 |
| 任务类型 | 审查检测、异常检测、趋势分析、纵向测量 |
| 方法关键词 | 远程测量、时间序列分析、Bitmap异常检测、Nelder-Mead优化、Mann-Kendall趋势检验 |
| 数据集 | CensoredPlanet (21.8B数据点, 20个月), OONI, ICLab, CitizenLab Test List, Alexa Top Domains |
| 是否开源 | 是 (数据和部分代码: https://censoredplanet.org) |
| PDF | 00-inbox/PDFs/2020-CCS-Censored_Planet__An_Internet-wide__Longitudinal_Censorship_Observatory.pdf |
| MinerU Markdown | unknown |

## 1. 一句话总结

> Censored Planet通过整合四种远程测量技术（Augur、Satellite/Iris、Quack、Hyperquack），构建了互联网规模的纵向审查观测平台，在20个月内收集超过218亿数据点，覆盖221个国家和地区，检测到15个重大审查事件（其中三分之二此前未被报告），并揭示了100多个国家审查活动上升的趋势。

## 2. 摘要翻译

### 2.1 摘要原文

Remote censorship measurement techniques offer capabilities for monitoring Internet reachability around the world. However, operating these techniques continuously is labor-intensive and requires specialized knowledge and synchronization, leading to limited adoption. In this paper, we introduce CensoredPlanet, an online censorship measurement platform that collects and analyzes measurements from ongoing deployments of four remote measurement techniques (Augur, Satellite/Iris, Quack, and Hyperquack). CensoredPlanet adopts a modular design that supports synchronized baseline measurements on six Internet protocols as well as customized measurements that target specific countries and websites. CensoredPlanet has already collected and published more than 21.8 billion data points of longitudinal network observations over 20 months of operation. CensoredPlanet complements existing censorship measurement platforms such as OONI and ICLab by offering increased scale, coverage, and continuity. We introduce a new representative censorship metric and show how time series analysis can be applied to CensoredPlanet's longitudinal measurements to detect 15 prominent censorship events, two-thirds of which have not been reported previously. Using trend analysis, we find increasing censorship activity in more than 100 countries, and we identify 11 categories of websites facing increasing censorship, including provocative attire, human rights issues, and news media. We hope that the continued publication of CensoredPlanet data helps counter the proliferation of growing restrictions to online freedom.

### 2.2 摘要中文翻译

远程审查测量技术为监测全球互联网可达性提供了能力。然而，持续运行这些技术需要大量人力、专业知识和同步协调，导致其采用率有限。本文介绍了CensoredPlanet，一个在线审查测量平台，它收集和分析来自四种远程测量技术（Augur、Satellite/Iris、Quack和Hyperquack）的持续部署数据。CensoredPlanet采用模块化设计，支持在六种互联网协议上进行同步基线测量，以及针对特定国家和网站的定制化测量。CensoredPlanet已经收集并发布了超过218亿个纵向网络观测数据点，运营时间超过20个月。CensoredPlanet通过提供更大的规模、覆盖范围和连续性，补充了OONI和ICLab等现有审查测量平台。我们引入了一种新的代表性审查指标，并展示了如何将时间序列分析应用于CensoredPlanet的纵向测量数据以检测15个重大审查事件，其中三分之二此前未被报告。通过趋势分析，我们发现100多个国家的审查活动呈上升趋势，并识别出11类面临日益严格审查的网站，包括挑衅性着装、人权问题和新闻媒体等内容。我们希望CensoredPlanet数据的持续发布能够帮助遏制不断增长的在线自由限制。

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

1. **现有平台的局限性**：OONI和ICLab等现有审查测量平台依赖志愿者网络，面临规模（scale）、覆盖范围（coverage）和连续性（continuity）三大挑战
2. **数据稀疏性**：志愿者网络收集的数据稀疏且不适合发现跨国家或跨时间的审查趋势
3. **远程测量技术的碎片化**：四种远程测量技术（Augur、Satellite、Quack、Hyperquack）各自独立运作，缺乏统一平台
4. **缺乏纵向分析**：现有远程测量技术仅在有限时间段内进行评估，未应对持续纵向数据收集和分析的复杂性
5. **社区需求**：需要一个能够快速响应审查事件、进行定制化测量的平台

### 3.2 现有方法的痛点和不足

| 痛点 | 具体问题 | 受影响平台 |
|------|----------|-----------|
| 规模有限 | 志愿者数量不足，难以覆盖全球 | OONI, ICLab |
| 覆盖范围受限 | 依赖特定地区的志愿者部署 | OONI, ICLab |
| 连续性不足 | 志愿者可能停止运行测量软件 | OONI (36% AS连续性) |
| 数据稀疏性 | 测量数据不足以进行趋势分析 | OONI, ICLab |
| 技术碎片化 | 各远程测量技术独立运作，缺乏同步 | Augur, Satellite, Quack, Hyperquack |
| 无法区分本地化与全国性审查 | 无法区分ISP级和国家级审查政策 | 所有远程技术 |
| 误报问题 | 缺乏验证机制，可能存在误报 | 所有远程技术 |
| 纵向分析缺失 | 未处理持续数据收集的复杂性 | 所有远程技术 |

### 3.3 论文的研究假设或核心直觉

**核心直觉**：通过整合多种远程测量技术（利用互联网协议侧信道），构建一个统一的、可扩展的、持续运行的审查观测平台，能够克服志愿者网络的规模和连续性限制，从而揭示全球互联网审查的全景和长期趋势。

**科学假设**：
1. 不同远程测量技术的同步测量可以提供更完整的审查视图
2. 纵向时间序列数据能够自动检测审查事件和趋势
3. 优化模型可以平滑异构审查策略带来的噪声，获得代表性指标

### 3.4 问题发现路径

| 阶段 | 内容 |
|------|------|
| 现象观察 | 全球互联网审查日益普遍且多样化，但现有测量方法存在严重局限 |
| 痛点提炼 | 志愿者网络的规模、覆盖、连续性问题；远程测量技术的碎片化和缺乏纵向分析 |
| 问题转化 | 需要构建一个统一平台，整合多种远程测量技术，支持持续纵向测量和自动分析 |
| 文献定位 | 补充OONI和ICLab的工作，利用Augur、Satellite、Quack、Hyperquack等远程技术 |

### 3.5 科学假设形成

**假设1：多技术整合假设**
- 观察：四种远程测量技术分别检测不同类型的封锁（TCP/IP、DNS、HTTP、HTTPS）
- 假设：整合这些技术可以提供更全面的审查视图
- 验证：通过在六种互联网协议上进行同步测量验证

**假设2：纵向数据价值假设**
- 观察：现有技术仅在有限时间段内评估
- 假设：持续的纵向数据收集能够发现审查事件和趋势
- 验证：通过20个月的持续运营和时间序列分析验证

**假设3：优化模型假设**
- 观察：同一国家内不同ISP的审查策略可能差异很大
- 假设：优化模型可以平滑异常值，获得国家级代表性指标
- 验证：通过Nelder-Mead优化和对比分析验证

## 4. 方法设计

### 4.1 方法整体流程

```
输入请求 → 输入扫描器 → 干扰扫描器 → 数据预处理 → 审查分析 → 时间序列分析
   ↓           ↓            ↓            ↓           ↓           ↓
测试配置   选择测试域    执行测量     去除误报    计算审查    异常检测
和域名     和观察点     和监控       聚类验证    代表指标    趋势分析
```

### 4.2 详细 Pipeline

| 阶段 | 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|------|
| 1 | 测试请求 | 接收社区请求或触发器 | 社区请求、异常事件警报 | 扫描配置 |
| 2 | 输入扫描器 | 选择测试域名和观察点 | 扫描配置 | 域名列表、观察点列表 |
| 2.1 | 观察点选择 | 按伦理标准选择基础设施观察点 | 各技术的约束条件 | Augur/Satellite/Quack/Hyperquack观察点 |
| 2.2 | 测试列表选择 | 选择测试域名 | CLTL + Alexa列表 | 2000个活跃域名/周 |
| 3 | 干扰扫描器 | 执行全球范围扫描 | 域名列表、观察点列表 | 原始测量数据 |
| 4 | 数据预处理 | 清洗和验证数据 | 原始测量数据 | 确认的封锁实例 |
| 4.1 | 初始清理 | 移除技术失败的测量 | 原始数据 | 有效测量 |
| 4.2 | 通用模式聚合 | 统一不同技术的数据格式 | 各技术数据 | 通用模式数据 |
| 4.3 | 误报去除 | 使用聚类技术识别并过滤误报 | 测量结果 | 确认的封锁实例 |
| 5 | 审查分析 | 计算国家级代表性指标 | 确认的封锁实例 | Cens(Smooth)指标 |
| 5.1 | 审查指标 | 计算单个观察点的封锁百分比 | 确认的封锁实例 | Cens(vp,t) |
| 5.2 | 优化模型 | Nelder-Mead优化平滑异常值 | Cens(Raw) | Cens(Smooth) |
| 6 | 时间序列分析 | 检测事件和趋势 | Cens(Smooth)时间序列 | 事件列表、趋势信息 |
| 6.1 | 变化分析 | 计算审查绝对变化 | 时间序列 | Δ(Cens) |
| 6.2 | 异常检测 | Bitmap方法检测异常 | Δ(Cens) | 异常分数、事件列表 |
| 6.3 | 趋势检测 | Mann-Kendall检验检测趋势 | Δ(Cens)时间序列 | 上升/下降趋势 |

### 4.3 模型结构或系统模块

| 模块 | 技术细节 | 关键参数 |
|------|----------|----------|
| Augur | 利用IP ID侧信道检测TCP/IP封锁 | α = 10^-5 (假设检验置信度) |
| Satellite/Iris | 利用开放DNS解析器检测DNS操纵 | 聚类技术识别CDN部署 |
| Quack | 利用TCP Echo协议检测应用层封锁 | 控制测量验证干扰方向性 |
| Hyperquack | 扩展Quack到HTTP/HTTPS，使用公共Web服务器 | EV证书验证、PeeringDB选择观察点 |
| 输入扫描器 | 轮询选择观察点，优先"Not Free"国家 | 每周更新、/24子网连续性 |
| 通用模式 | 统一数据格式 | id, protocol, date, vp, domain, blocked |
| 聚类验证 | DBSCAN算法聚类HTML响应 | 457个新聚类（308个封锁页面，149个误报） |
| 优化模型 | Nelder-Mead优化AS权重 | RMSE误差函数 |
| Bitmap异常检测 | 离散化数据为Bitmap，计算距离 | 4×4 Bitmap，阈值3.1 |
| Mann-Kendall检验 | 非参数趋势检验 | 99%显著性水平 |

### 4.4 公式、算法和机制解释

**审查指标公式：**

单个观察点审查百分比（公式1）：
```
Cens(vp,t) = (# Domains blocked / # Domains tested) × 100
```

国家级原始审查指标（公式2）：
```
Cens(cc,t)(Raw) = Σ(i=1 to n) Cens(vp_i,t) / n
```

优化模型目标函数（公式4）：
```
argmin √(Σ(t=1 to n) (AS(cc,j,t) · ω_j - Cens(cc,t)(Raw))^2)
```

平滑后的审查指标（公式5）：
```
Cens(cc,t)(Smooth) = Σ(j=1 to n) Cens(vp_j,t) · ω_j / Σ(j=1 to n) ω_j
```

审查绝对变化（公式6）：
```
Δ(Cens(vp,ta-tb)) = Cens(vp,tb) - Cens(vp,ta)
```

加权平均变化（公式7）：
```
Δ(Cens(cc,ta-tb)(Smooth)) = Σ(j=1 to n) ω_j · Δ(Cens(vp_j,ta-tb)) / Σ(j=1 to n) ω_j
```

Bitmap距离（公式8）：
```
Dist(BA,BB) = Σ(p=1 to n) Σ(q=1 to n) ((BA(p,q) - BB(p,q))^2)
```

**关键算法：**
1. **Nelder-Mead优化**：用于寻找最优AS权重，平滑异构审查策略
2. **DBSCAN聚类**：用于识别和过滤误报（封锁页面vs正常响应）
3. **Bitmap异常检测**：将时间序列离散化为Bitmap表示，计算距离作为异常分数
4. **Mann-Kendall检验**：非参数趋势检验，对时间序列的间隙和长度差异具有鲁棒性
5. **Thiel-Sen回归**：估计趋势线的斜率

### 4.5 方法优势

1. **规模优势**：超过95,000个观察点，覆盖221个国家和地区
2. **连续性优势**：93%的/24子网连续性，99%的AS连续性
3. **多协议同步**：在6种互联网协议上进行同步测量
4. **自动化分析**：时间序列分析自动检测事件和趋势
5. **代表性指标**：优化模型平滑异构审查策略，获得国家级代表性指标
6. **快速聚焦能力**：能够快速响应审查事件，进行定制化测量
7. **数据互补性**：与OONI和ICLab形成互补，提供不同视角

### 4.6 方法不足

1. **观察点粒度限制**：无法测量非常本地化的审查（如学校、工作场所）
2. **技术特定限制**：
   - Hyperquack和Quack-Discard无法检测单向封锁
   - Augur无法检测通常使用CDN的域名封锁
3. **地理定位精度**：使用现成的地理定位数据库，可能存在不准确
4. **审查者规避风险**：复杂的审查者可能检测并规避测量技术
5. **伦理考量**：尽管采取了风险最小化措施，但仍存在对远程主机运营商的潜在风险
6. **误报处理**：聚类验证需要人工标注，存在主观性

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 维度 | CensoredPlanet | OONI | ICLab |
|------|---------------|------|-------|
| 测量方法 | 远程测量（利用协议侧信道） | 端用户客户端软件 | VPN端点 |
| 观察点来源 | 基础设施主机（路由器、DNS服务器、Web服务器） | 志愿者设备 | VPN提供商 |
| 规模 | 95,000+观察点，221国家 | 1,915 ASes，155国家 | 56 ASes，48国家 |
| 连续性 | 93% /24子网连续性 | 36% AS连续性 | 64% AS连续性 |
| 测量协议 | 6种协议同步 | 主要HTTP/HTTPS | 主要HTTP/HTTPS |
| 数据量 | 21.8B数据点/20个月 | 相对较少 | 相对较少 |
| 风险模式 | 对基础设施运营商风险低 | 对志愿者有潜在风险 | 对VPN用户有潜在风险 |

### 5.2 创新点分析

| 创新点 | 具体内容 | 意义 |
|--------|----------|------|
| 多技术整合平台 | 首次将四种远程测量技术整合到统一平台 | 提供更全面的审查视图 |
| 纵向测量框架 | 20个月持续运营，218亿数据点 | 支持长期趋势分析和事件检测 |
| 代表性审查指标 | 优化模型平滑异构审查策略 | 获得国家级代表性指标 |
| 自动化分析方法 | 时间序列分析、Bitmap异常检测 | 自动检测审查事件和趋势 |
| 快速聚焦能力 | 能够快速响应审查事件 | 支持定制化深度测量 |
| 同步测量设计 | 在6种协议上进行同步测量 | 确保数据可比性和完整性 |

### 5.3 适用场景

1. **全球审查监测**：适合需要全球覆盖的审查监测任务
2. **长期趋势研究**：适合研究审查政策随时间的变化
3. **审查事件检测**：适合自动检测新发生的审查事件
4. **国家级分析**：适合分析特定国家的审查模式
5. **方法比较研究**：适合比较不同审查测量方法的效果
6. **政策影响评估**：适合评估特定政策对互联网自由的影响

### 5.4 方法对比表

| 特性 | CensoredPlanet | OONI | ICLab | Encore | ONI |
|------|---------------|------|-------|--------|-----|
| 活跃状态 | 活跃 | 活跃 | 不活跃 | 不活跃 | 不活跃 |
| 测量方法 | 远程 | 客户端 | VPN | Web请求 | 多种 |
| 国家覆盖 | 221 | 155 | 48 | 全球 | 多国 |
| AS覆盖 | 9,014 | 1,915 | 56 | N/A | N/A |
| 数据连续性 | 高 | 低 | 中 | N/A | N/A |
| 协议支持 | 6种 | 主要HTTP | 主要HTTP | HTTP | 多种 |
| 开源程度 | 数据开源 | 完全开源 | 数据开源 | 部分开源 | 报告公开 |

## 6. 实验表现与优势

### 6.1 实验设计和设置

**运营时间**：2018年8月 - 2020年3月（20个月）

**测量频率**：
- Hyperquack、Quack、Satellite：每周2次
- Augur：每周1次（2019年11月开始）

**数据规模**：
- 总测量数：21.8B
- 技术失败移除：1.2B（5.9%）
- 初始封锁标记：1.5B（7%）
- 误报过滤：500M
- 确认封锁：约1B

**伦理合规**：
- 遵循Menlo和Belmont报告原则
- 使用基础设施主机而非终端用户设备
- 限制测量速率
- WHOIS记录和退出选项
- 平均每月1次投诉，无技术或法律问题

### 6.2 数据集

| 数据集 | 描述 | 规模 |
|--------|------|------|
| CensoredPlanet | 本研究收集的审查测量数据 | 21.8B数据点，20个月 |
| OONI Web Connectivity | OONI的Web连接性测试数据 | 2020年3月数据 |
| ICLab | ICLab的公开数据集 | 2018年9月数据 |
| CitizenLab Test List | 测试域名列表 | 约1,400个域名 |
| Alexa Top Domains | 流行域名列表 | 600个域名 |
| Freedom on the Net Report | 自由之家年度报告 | 2019年版 |

### 6.3 Baseline

**对比平台**：
1. **OONI**：最广泛使用的审查测量平台，依赖志愿者
2. **ICLab**：使用VPN端点的审查测量平台
3. **各远程测量技术单独表现**：Augur、Satellite、Quack、Hyperquack

**对比维度**：
- 国家覆盖范围
- AS覆盖范围
- 测量连续性
- 数据量
- 协议支持

### 6.4 评价指标

1. **规模指标**：
   - 观察点数量
   - 国家覆盖数
   - AS覆盖数

2. **连续性指标**：
   - /24子网连续性（93%）
   - AS连续性（99%）

3. **准确性指标**：
   - 误报率
   - 事件检测率

4. **代表性指标**：
   - 变异系数
   - 优化后指标稳定性

5. **趋势分析指标**：
   - Mann-Kendall检验显著性
   - Thiel-Sen回归斜率

### 6.5 关键实验结果

| 指标 | CensoredPlanet | OONI | ICLab |
|------|---------------|------|-------|
| 国家数 | 221 | 155 | 48 |
| "Not Free"国家 | 21 | 21 | 4 |
| 总AS数 | 9,014 | 1,915 | 56 |
| 中位数AS/国家 | 8 | 4 | 1 |
| 最大AS/国家 | 1,427 | 347 | 22 |
| AS连续性 | 99% | 36% | 64% |
| /24子网连续性 | 93% | N/A | N/A |

**关键发现**：
1. 检测到15个重大审查事件，其中10个此前未被报告
2. 100多个国家审查活动呈上升趋势
3. 11类网站面临日益严格审查
4. DNS审查在123个国家呈上升趋势
5. HTTPS审查也在增加，尽管全加密流量曾被认为会减少审查

### 6.6 优势最明显的场景

1. **连续性要求高的场景**：93%的/24子网连续性确保时间序列分析的可靠性
2. **大规模覆盖场景**：221个国家的覆盖，特别是"Not Free"国家的全面覆盖
3. **多协议分析场景**：6种协议的同步测量提供更全面的审查视图
4. **长期趋势研究场景**：20个月的持续数据支持趋势分析
5. **快速响应场景**：快速聚焦能力支持定制化深度测量

### 6.7 局限性

1. **观察点粒度**：无法测量非常本地化的审查（学校、工作场所）
2. **技术限制**：某些技术无法检测单向封锁或CDN域名封锁
3. **地理定位精度**：使用现成数据库，可能存在不准确
4. **审查者规避**：复杂审查者可能检测并规避测量
5. **伦理风险**：尽管风险低，但仍存在对远程主机运营商的潜在风险
6. **误报处理**：聚类验证需要人工标注
7. **数据解释**：需要领域专家结合社会政治背景解释数据

## 7. 学习与应用

### 7.1 是否开源？

**数据开源**：
- 官方网站：https://censoredplanet.org
- 提供最新快照和历史数据集
- GitHub仓库：https://github.com/censoredplanet

**代码部分开源**：
- 数据处理和分析代码开源
- 测量技术实现参考各技术原始论文

### 7.2 复现关键步骤

1. **环境准备**：
   - 配置网络环境，确保能够执行IP欺骗
   - 准备足够的存储空间（TB级）
   - 协调网络管理员和上游ISP

2. **观察点选择**：
   - Augur：从CAIDA ARK获取IP ID递增的路由器
   - Satellite：扫描IPv4地址空间获取开放DNS解析器
   - Quack：扫描TCP端口7（Echo）或端口9（Discard）开放的服务器
   - Hyperquack：从Censys获取具有EV证书的Web服务器

3. **测量执行**：
   - 每周更新观察点列表
   - 执行同步测量
   - 收集健康监控信息

4. **数据处理**：
   - 移除技术失败的测量
   - 聚合到通用模式
   - 聚类验证去除误报

5. **分析应用**：
   - 计算优化后的审查指标
   - 应用时间序列分析
   - 检测事件和趋势

### 7.3 关键超参数、预处理和训练细节

**观察点选择参数**：
- Augur：IP ID增量 < 5
- Satellite：活跃超过1个月的解析器
- Hyperquack：EV证书验证

**测量频率**：
- Hyperquack、Quack、Satellite：每周2次
- Augur：每周1次

**优化模型参数**：
- 误差函数：RMSE
- 优化算法：Nelder-Mead

**异常检测参数**：
- Bitmap大小：4×4
- 阈值：3.1（平衡异常百分比和事件检测数）

**趋势检测参数**：
- 显著性水平：99%
- 趋势估计：Thiel-Sen回归

### 7.4 能否迁移到其他任务？

**可迁移场景**：
1. **其他网络测量任务**：如DDoS检测、网络故障检测
2. **时间序列异常检测**：如金融数据、物联网数据
3. **大规模数据收集平台**：如网络性能监测
4. **多源数据整合**：如多传感器数据融合

**迁移挑战**：
1. 需要特定领域的协议知识
2. 需要处理大规模数据的基础设施
3. 需要领域专家解释结果
4. 需要考虑伦理和法律问题

### 7.5 对我的研究有什么启发？

1. **平台化思维**：构建统一平台整合多种技术，而非单一技术
2. **纵向数据价值**：持续数据收集能够揭示趋势和事件
3. **代表性指标设计**：优化模型平滑异构数据，获得代表性指标
4. **自动化分析**：时间序列分析技术自动检测异常和趋势
5. **伦理考量**：在测量研究中考虑伦理和法律问题
6. **数据互补性**：不同平台和方法提供互补视角

## 8. 总结

### 8.1 核心思想

> 整合四种远程测量技术，构建互联网规模的纵向审查观测平台，通过自动化分析揭示全球审查趋势。

### 8.2 速记版 Pipeline (5 steps)

1. **输入选择**：选择测试域名和观察点（伦理标准）
2. **同步测量**：在6种协议上执行全球范围扫描
3. **数据清洗**：聚类验证去除误报，确认封锁实例
4. **指标计算**：优化模型平滑异构数据，获得代表指标
5. **趋势分析**：时间序列分析检测事件和趋势

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[censorship-circumvention]]
- [[anomaly-detection]]
- [[network-security]]
- [[internet-freedom]]
- [[time-series-analysis]]

### 9.2 相关方法

- [[remote-measurement]]
- [[side-channel-detection]]
- [[bitmap-anomaly-detection]]
- [[Nelder-Mead-optimization]]
- [[Mann-Kendall-test]]
- [[DBSCAN-clustering]]

### 9.3 相关任务

- [[censorship-detection]]
- [[censorship-measurement]]
- [[network-anomaly-detection]]
- [[longitudinal-analysis]]
- [[trend-detection]]

### 9.4 可更新的综述页面

- [[survey-censorship-measurement]]
- [[survey-network-measurement]]
- [[survey-internet-freedom]]

### 9.5 可加入的对比表

- [[comparison-censorship-platforms]]
- [[comparison-remote-measurement-techniques]]
- [[comparison-anomaly-detection-methods]]

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|----------|----------|------|
| CensoredPlanet覆盖221个国家 | "CensoredPlanet has already collected and published more than 21.8 billion data points...over 20 months of operation" | Abstract |
| 93% /24子网连续性 | "we find a continuity of 93%" | §6.1 |
| 检测到15个重大审查事件 | "detect 15 prominent censorship events, two-thirds of which have not been reported previously" | Abstract |
| 100多个国家审查上升趋势 | "increasing censorship activity in more than 100 countries" | Abstract |
| DNS审查在123个国家上升 | "we observe an overall increase in DNS censorship in 123 countries in total" | §7.2.1 |
| 优化模型平滑异构数据 | "we build a numerical optimization model to derive weights for measurement points that allow to smooth the censorship results" | §5.2.2 |
| Bitmap异常检测优于其他方法 | "the bitmap-based detection technique works best for our data" | §5.3.2 |
| OONI AS连续性仅36% | "OONI data has an even lower AS continuity of 36%" | §6.1 |
| "Not Free"国家全面覆盖 | "CensoredPlanet and OONI cover data from all 21 countries considered 'Not Free'" | §6.2 |
| 误报过滤移除500M测量 | "The false positive filtering removes around 500 million measurements" | §5.1.4 |

## 11. 原始资料链接

- **论文PDF**：00-inbox/PDFs/2020-CCS-Censored_Planet__An_Internet-wide__Longitudinal_Censorship_Observatory.pdf
- **项目官网**：https://censoredplanet.org
- **GitHub仓库**：https://github.com/censoredplanet
- **OONI数据**：https://ooni.torproject.org
- **ICLab数据**：https://iclab.org
- **CitizenLab测试列表**：https://github.com/citizenlab/test-lists
- **Freedom on the Net报告**：https://freedomhouse.org

## 12. 后续问题

1. **审查者规避**：如何应对审查者检测和规避测量技术？
2. **本地化审查**：如何测量非常本地化的审查（如学校、工作场所）？
3. **实时响应**：如何进一步提高快速聚焦能力，实现实时响应？
4. **数据解释**：如何结合社会政治背景更好地解释审查数据？
5. **伦理演进**：随着测量规模扩大，伦理考量如何演进？
6. **平台协作**：如何更好地与OONI、ICLab等平台协作，形成互补？
7. **技术扩展**：如何扩展到更多互联网协议和测量技术？
8. **机器学习应用**：如何应用更先进的机器学习技术改进异常检测？

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

**问题**：全球互联网审查日益普遍，但现有测量方法存在严重局限（规模、覆盖、连续性）

**解决方案**：构建CensoredPlanet平台，整合四种远程测量技术，支持持续纵向测量和自动化分析

**贡献**：
1. 平台本身（规模、覆盖、连续性优势）
2. 代表性审查指标和优化方法
3. 时间序列分析技术（异常检测和趋势检测）
4. 20个月的纵向数据和15个重大事件发现

**影响**：揭示全球审查趋势，支持互联网自由研究和倡导

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 关键内容 |
|------|----------|----------|
| §1 Introduction | 问题引入和动机 | 现有平台局限性，需要统一纵向平台 |
| §2 Background | 技术背景 | 四种远程测量技术原理 |
| §3 Design | 系统设计 | 模块化架构、伦理考量 |
| §4 Data Collection | 数据收集 | 输入扫描器、干扰扫描器 |
| §5 Data Processing | 数据处理 | 预处理、审查分析、时间序列分析 |
| §6 Evaluation | 评估验证 | 规模、覆盖、连续性对比 |
| §7 Findings | 核心发现 | 事件检测、趋势分析、案例研究 |
| §8 Related Work | 文献定位 | 与现有工作的关系 |
| §9 Limitations | 局限性讨论 | 技术限制、伦理考量 |
| §10 Conclusion | 总结展望 | 贡献总结、未来方向 |

### 13.3 Gap 展开方式

| Gap类型 | 具体表现 | 解决方案 |
|---------|----------|----------|
| 规模Gap | OONI和ICLab覆盖有限 | 95,000+观察点，221国家 |
| 连续性Gap | 志愿者网络连续性低 | 93% /24子网连续性 |
| 协议Gap | 现有平台主要测量HTTP | 6种协议同步测量 |
| 分析Gap | 缺乏自动化分析方法 | 时间序列分析、异常检测 |
| 整合Gap | 远程测量技术碎片化 | 统一平台整合四种技术 |

### 13.4 实验叙事方式

| 实验类型 | 叙事目的 | 关键结果 |
|----------|----------|----------|
| 规模对比 | 证明平台优势 | 221国家 vs 155国家 vs 48国家 |
| 连续性评估 | 证明数据可靠性 | 93% /24连续性，99% AS连续性 |
| 事件检测 | 展示应用价值 | 15个事件，10个新发现 |
| 趋势分析 | 揭示长期模式 | 100+国家上升趋势 |
| 案例研究 | 深入分析特定事件 | 斯里兰卡、挪威、土库曼斯坦 |

### 13.5 写作风格与可迁移写法

| 写作特点 | 具体表现 | 可迁移场景 |
|----------|----------|-----------|
| 问题驱动 | 从现有平台局限性出发 | 需要解决现有方法不足的研究 |
| 平台化呈现 | 强调系统设计和模块化 | 构建测量或分析平台的研究 |
| 数据驱动 | 用大规模数据支持论点 | 需要实证支持的研究 |
| 对比评估 | 与现有平台详细对比 | 需要证明方法优势的研究 |
| 案例深入 | 用具体案例展示能力 | 需要展示应用价值的研究 |
| 伦理考量 | 详细讨论伦理问题 | 涉及人类受试者或网络测量的研究 |
| 未来导向 | 明确局限性和未来方向 | 需要规划后续工作的研究 |

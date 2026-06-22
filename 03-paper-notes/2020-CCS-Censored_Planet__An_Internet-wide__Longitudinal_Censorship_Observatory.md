---
type: paper
title_original: "Censored Planet: An Internet-wide, Longitudinal Censorship Observatory"
title_cn: "Censored Planet：互联网规模的纵向审查观测平台"
authors:
  - Ram Sundara Raman
  - Prerana Shenoy
  - Katharina Kohls
  - Roya Ensafi
year: 2020
venue: "ACM CCS 2020"
doi: "https://doi.org/10.1145/3372297.3417883"
url: "https://censoredplanet.org"
pdf: "00-inbox/PDFs/2020-CCS-Censored_Planet__An_Internet-wide__Longitudinal_Censorship_Observatory.pdf"
mineru_md: "02-parsed-markdown/2020-CCS-Censored_Planet__An_Internet-wide__Longitudinal_Censorship_Observatory.md"
status: processed
reading_level: L3
research_area:
  - censorship-measurement
  - internet-measurement
  - anomaly-detection
  - network-monitoring
task:
  - censorship-detection
  - longitudinal-analysis
  - trend-detection
  - event-detection
method:
  - remote-measurement
  - bitmap-anomaly-detection
  - mann-kendall-trend-test
  - optimization-smoothing
  - clustering-false-positive-removal
dataset:
  - Citizen Lab Global Test List (CLTL)
  - Alexa Top Domains
  - 21.8 billion measurements (Aug 2018 - Mar 2020)
  - 95,000+ vantage points in 221 countries
code: "https://github.com/censoredplanet"
relevance: high
created: "2026-06-14"
updated: "2026-06-14"
related_papers: []
---

# Censored Planet: An Internet-wide, Longitudinal Censorship Observatory

## 0. 基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | Censored Planet: An Internet-wide, Longitudinal Censorship Observatory |
| 中文标题 | Censored Planet：互联网规模的纵向审查观测平台 |
| 作者 | Ram Sundara Raman, Prerana Shenoy, Katharina Kohls, Roya Ensafi |
| 年份 | 2020 |
| 会议/期刊 | ACM CCS 2020 |
| 研究方向 | [[censorship-circumvention]]、互联网测量、[[anomaly-detection]]、网络监控 |
| 任务类型 | 审查检测、纵向分析、趋势检测、事件发现 |
| 方法关键词 | 远程测量（Augur/Satellite/Quack/Hyperquack）、Bitmap异常检测、Mann-Kendall趋势检验、Nelder-Mead优化平滑、聚类去误报 |
| 数据集 | Citizen Lab Global Test List + Alexa Top Domains；21.8亿次测量（2018.8-2020.3）；95,000+ 观测点覆盖221个国家 |
| 是否开源 | https://github.com/censoredplanet |
| DOI | https://doi.org/10.1145/3372297.3417883 |

---

## 1. 一句话总结

> Censored Planet 整合四种远程测量技术（Augur、Satellite、Quack、Hyperquack），构建互联网规模的纵向审查观测平台，覆盖95,000+观测点和6种协议，通过Bitmap异常检测和Mann-Kendall趋势分析在20个月内发现15个重大审查事件（2/3此前未报告），揭示100+国家审查呈上升趋势。

---

## 2. 摘要翻译

### 2.1 摘要原文

Remote censorship measurement techniques offer capabilities for monitoring Internet reachability around the world. However, operating these techniques continuously is labor-intensive and requires specialized knowledge and synchronization, leading to limited adoption. In this paper, we introduce Censored Planet, an online censorship measurement platform that collects and analyzes measurements from ongoing deployments of four remote measurement techniques (Augur, Satellite/Iris, Quack, and Hyperquack). Censored Planet adopts a modular design that supports synchronized baseline measurements on six Internet protocols as well as customized measurements that target specific countries and websites. Censored Planet has already collected and published more than 21.8 billion data points of longitudinal network observations over 20 months of operation. Censored Planet complements existing censorship measurement platforms such as OONI and ICLab by offering increased scale, coverage, and continuity. We introduce a new representative censorship metric and show how time series analysis can be applied to Censored Planet's longitudinal measurements to detect 15 prominent censorship events, two-thirds of which have not been reported previously. Using trend analysis, we find increasing censorship activity in more than 100 countries, and we identify 11 categories of websites facing increasing censorship, including provocative attire, human rights issues, and news media.

### 2.2 摘要中文翻译

远程审查测量技术提供了监控全球互联网可达性的能力。然而，持续运行这些技术需要大量劳动力、专业知识和协调配合，导致其采用率有限。本文介绍 Censored Planet，一个在线审查测量平台，通过持续部署四种远程测量技术（Augur、Satellite/Iris、Quack 和 Hyperquack）来收集和分析测量数据。Censored Planet 采用模块化设计，支持在六种互联网协议上进行同步基线测量，以及针对特定国家和网站的定制化测量。Censored Planet 在运行20个月期间已收集并发布超过218亿条纵向网络观测数据点。Censored Planet 通过提供更大的规模、覆盖范围和连续性，补充了 OONI 和 ICLab 等现有审查测量平台。我们提出了一种新的代表性审查指标，并展示了如何将时间序列分析应用于 Censored Planet 的纵向测量数据，检测出15个重大审查事件，其中三分之二此前未被报告。通过趋势分析，我们发现100多个国家的审查活动呈上升趋势，并识别出11类面临日益严格审查的网站，包括挑衅性着装、人权议题和新闻媒体。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

现有全球审查测量面临三个核心瓶颈：

1. **志愿者模式的规模瓶颈**：OONI 依赖终端用户安装软件，ICLab 依赖 VPN 节点，两者在很多国家缺乏足够的志愿者部署
2. **覆盖范围的地理偏差**：志愿者网络无法覆盖"不自由"和"部分自由"国家的大部分网络
3. **数据连续性不足**：志愿者不持续运行测试，导致时间序列数据稀疏，无法进行纵向趋势分析

远程测量技术（Augur、Satellite、Quack、Hyperquack）虽然各自解决了部分问题，但存在四个关键不足：每种技术仅聚焦一种阻断类型；仅在有限时间段内评估；无法区分本地化审查与全国性政策；缺乏验证机制可能产生误报。

### 3.2 现有方法的痛点

| 痛点 | 具体表现 | 受影响的平台 | 本文解决方案 |
|---|---|---|---|
| 规模不足 | OONI 仅覆盖156个国家，ICLab 41个国家 | OONI, ICLab | 整合四种远程技术，覆盖221个国家 |
| 覆盖稀疏 | 志愿者集中在"自由"国家，"不自由"国家数据少 | OONI, ICLab | 优先选择"不自由/部分自由"国家观测点 |
| 连续性差 | OONI AS连续性仅36%，ICLab 64% | OONI, ICLab | 每周自动扫描，AS连续性达99% |
| 协议单一 | 现有平台主要测试HTTP连通性 | OONI | 同步测量6种协议（IP/DNS/HTTP/HTTPS/Echo/Discard） |
| 误报问题 | Cloudflare等CDN的bot检查引入噪声 | 远程技术 | 聚类技术+控制测量去除误报 |
| 纵向分析缺失 | 远程技术仅在短期数据上评估 | Augur/Satellite/Quack | Bitmap异常检测+Mann-Kendall趋势检验 |

### 3.3 核心直觉

作者的核心洞察是：**单一远程测量技术提供"盲人摸象"式的局部视角，只有将多种技术在统一框架下同步运行并进行长期纵向分析，才能获得全球审查的完整图景**。类比天文学中的"观测台"（Observatory），Censored Planet 将审查测量从"探险式调查"转变为"天文台式连续监测"。

### 3.4 问题发现路径

| 阶段 | 来源 | 发现 |
|---|---|---|
| 文献调研 | OONI/ICLab/Augur/Satellite/Quack/Hyperquack 论文 | 各技术独立运行，缺乏统一平台和纵向分析 |
| 数据观察 | 20个月连续测量数据 | 21.8亿数据点覆盖221个国家，发现审查异质性 |
| 方法对比 | 与OONI/ICLab数据交叉验证 | 2/3新发现事件在OONI数据中无记录 |
| 趋势发现 | Mann-Kendall趋势检验 | 100+国家审查上升，DNS和HTTPS封锁增长最快 |

### 3.5 科学假设

**假设1（技术可行性假设）**：
- 假设：远程测量技术可以安全、持续地从基础设施节点（而非终端用户设备）检测审查
- 论文中的证据：20个月运行中平均每月仅1次投诉，无技术或法律问题
- 评估：已验证——基础设施节点选择有效降低对运营者的风险

**假设2（代表性假设）**：
- 假设：通过加权平滑可以消除异常观测点的影响，获得国家级代表性审查指标
- 论文中的证据：Figure 2展示平滑后去除异常观测点影响，保留广泛审查增长
- 评估：已验证——Nelder-Mead优化有效平滑离群值

**假设3（纵向分析假设）**：
- 假设：审查指标具有高度自相关性（Kendall's τ=0.93），异常大的变化是事件的强指标
- 论文中的证据：Bitmap异常检测发现15个事件，Mann-Kendall趋势检验发现100+国家上升趋势
- 评估：已验证——时间序列分析方法适用于审查数据

---

## 4. 方法设计

### 4.1 整体流程

Censored Planet 采用模块化设计，分为**数据收集**和**数据处理**两大阶段：

1. **数据收集阶段**：
   - **Test Requests**：接收社区请求或异常告警触发的扫描配置
   - **Input Scanner**：选择测试域名列表、观测点列表、其他输入参数
   - **Interference Scanner**：执行互联网范围扫描，检测测试域名的干扰情况

2. **数据处理阶段**：
   - **Data Pre-processing**：去除技术故障数据、统一数据格式、聚类去除误报
   - **Censorship Analysis**：通过优化模型平滑异常观测点，获得国家级代表性指标
   - **Time Series Analysis**：Bitmap异常检测发现事件，Mann-Kendall检验发现趋势

### 4.2 Pipeline 详解

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Input Scanner | 社区请求、异常告警 | 选择CLTL+Alexa域名（2000/周）；按国家轮询选择观测点；更新依赖 | 域名列表、观测点列表、扫描配置 | 同步四种技术的输入，确保可比性 |
| Interference Scanner | 扫描配置 | 对6种协议执行远程测量；健康监控记录错误；维护全局工作状态 | 原始测量数据 | 核心测量引擎 |
| Initial Sanitization | 原始测量数据 | 去除因技术故障（连接丢失、文件系统故障）失败的测量 | 清洗后数据 | 去除无效数据 |
| Common Schema Aggregation | 清洗后数据 | 统一为(id, protocol, date, vp, domain, blocked)格式；添加国家/AS/类别元数据 | 标准化数据 | 引入可比性和互操作性 |
| False Positive Filtering | 标准化数据 | 迭代分类识别HTML响应聚类；DBSCAN图像聚类；人工标注blockpage/误报 | 确认的审查实例 | 去除约5亿条误报 |
| Optimization Smoothing | 确认的审查数据 | Nelder-Mead优化为每个AS分配权重ω，最小化RMSE | 国家级平滑审查指标 | 消除异常观测点影响 |
| Anomaly Detection | 平滑审查时间序列 | Bitmap表示+距离计算（字母表大小4，窗口2%） | 异常分数排名 | 发现审查事件 |
| Trend Detection | 平滑审查时间序列 | Mann-Kendall检验（99%显著性）+Thiel-Sen回归估计 | 趋势方向+斜率 | 发现审查趋势 |

### 4.3 模块详解

| 模块 | 功能 | 输入 | 输出 | 关键技术细节 |
|---|---|---|---|---|
| Augur | 检测TCP/IP层阻断 | 路由器IP ID增量序列 | 连接可达性 | 需要路由器2+跳远离终端用户，IP ID增量<5 |
| Satellite | 检测DNS操纵 | 开放DNS解析器 | DNS响应正确性 | 综合Satellite+Iris方法，去除browser-trusted证书启发式 |
| Quack | 检测Echo/Discard协议阻断 | TCP Echo服务器（端口7/9） | 应用层阻断 | 50,000+观测点，控制测量确保关键字导致干扰 |
| Hyperquack | 检测HTTP(S)阻断 | 公共Web服务器（端口80/443） | HTTP(S)阻断 | 扩展到25,000+ EV证书服务器，构建服务器响应模板 |
| Bitmap异常检测 | 时间序列异常发现 | 平滑审查变化序列 | 异常分数 | 离散化→Bitmap表示→滑动窗口距离计算 |
| Mann-Kendall趋势检验 | 趋势方向检测 | 平滑审查变化序列 | 趋势方向+显著性 | 99%显著性水平，Thiel-Sen回归估计斜率 |

### 4.4 公式解释

**公式1：单观测点审查率**
$$\text{Cens}_{\text{vp},t} = \frac{\# \text{Domains blocked}}{\# \text{Domains tested}} \cdot 100$$
- 含义：单个观测点在某周的被封锁域名百分比
- 作用：最细粒度的审查度量

**公式2：国家级原始审查率**
$$\text{Cens}_{\text{cc},t}(\text{Raw}) = \frac{\sum_{i=1}^{n} \text{Cens}_{\text{vp}_i,t}}{n}$$
- 含义：一个国家内所有观测点的平均审查率
- 问题：异常观测点会扭曲结果

**公式4：Nelder-Mead优化目标**
$$\arg\min_{\omega_j} \sqrt{\frac{\sum_{t=1}^{n}(\text{AS}_{\text{cc},j,t} \cdot \omega_j - \text{Cens}_{\text{cc},t}(\text{Raw}))^2}{n}}$$
- 含义：为每个AS找到权重ω，使其测量值与国家级平均值的RMSE最小
- 作用：平滑异常AS的影响，保留广泛审查增长

**公式5：国家级平滑审查率**
$$\text{Cens}_{\text{cc},t}(\text{Smooth}) = \frac{\sum_{j=1}^{n} \text{Cens}_{\text{vp}_j,t} \cdot \omega_j}{\sum_{j=1}^{n} \omega_j}$$
- 含义：加权平均后的国家级审查率
- 效果：Figure 2展示巴基斯坦Discard审查中，广泛增长（2018年11月）被保留，异常观测点（2018年9月、2019年3月）被平滑

**公式6：审查变化量**
$$\Delta(\text{Cens}_{\text{vp},t_a-t_b}) = \text{Cens}_{\text{vp},t_b} - \text{Cens}_{\text{vp},t_a}$$
- 含义：两周之间审查率的绝对变化
- 用途：作为异常检测和趋势分析的基础

**公式8：Bitmap距离**
$$\text{Dist}(BA, BB) = \sum_{p=1}^{n}\sum_{q=1}^{n}((BA_{p,q} - BB_{p,q})^2)$$
- 含义：两个Bitmap之间的欧氏距离
- 参数：字母表大小4，窗口大小为时间序列长度的2%
- 作用：距离作为异常分数，高分表示审查突变

### 4.5 方法优势

1. **规模与覆盖**：95,000+观测点覆盖221个国家，远超OONI（156国）和ICLab（41国）
2. **连续性**：AS连续性99%，/24子网连续性93%，确保时间序列分析可靠
3. **多协议同步**：6种协议同步测量，提供审查的多维视角
4. **误报控制**：聚类技术去除约5亿条误报，保守确认blockpage
5. **代表性指标**：优化平滑消除异常观测点影响，获得国家级代表性指标
6. **自动化分析**：Bitmap异常检测和Mann-Kendall趋势检验实现自动化事件和趋势发现
7. **快速聚焦能力**：可快速响应世界事件进行定制化深度测量（如土库曼斯坦案例）

### 4.6 方法不足

1. **粒度限制**：观测点在基础设施层面，无法检测学校/工作场所等末端网络的审查
2. **技术局限**：
   - Hyperquack/Quack-Discard无法检测单向阻断
   - Augur无法检测通常使用anycast的域名阻断
3. **地理定位依赖**：使用现成的地理定位数据库，可能存在不准确
4. **对抗能力有限**：复杂审查者可能通过检测和丢弃探测流量来规避测量
5. **人工标注成本**：聚类去误报步骤需要人工标注每个新聚类
6. **Augur规模受限**：受时间和资源限制，Augur仅使用500-1,000观测点

---

## 5. 方法对比

### 5.1 与现有方法的本质区别

| 维度 | OONI/ICLab（志愿者模式） | 单一远程技术（Augur/Satellite/Quack） | Censored Planet |
|---|---|---|---|
| 测量模式 | 终端用户设备直接测量 | 单一协议远程测量 | 四种技术+六种协议同步远程测量 |
| 规模 | 数百-数千志愿者 | 数万观测点 | 95,000+观测点 |
| 覆盖 | 156-41个国家 | 单一技术覆盖 | 221个国家 |
| 连续性 | OONI 36%/ICLab 64% | 短期评估 | 99% AS连续性 |
| 分析能力 | 基础连通性测试 | 单点阻断检测 | 纵向时间序列分析（异常+趋势） |
| 代表性 | 志愿者偏差 | 异常观测点影响 | 优化平滑获得国家级指标 |

### 5.2 创新点

| 创新点 | 具体内容 | 位置 | 与已有工作的区别 |
|---|---|---|---|
| 多技术统一平台 | 整合Augur/Satellite/Quack/Hyperquack四种远程技术 | §3-4 | 此前各技术独立运行，无统一框架 |
| 六协议同步测量 | IP/DNS/HTTP/HTTPS/Echo/Discard同步测试 | §4.2 | OONI仅测HTTP连通性 |
| 优化平滑指标 | Nelder-Mead优化为AS分配权重，平滑异常观测点 | §5.2 | 此前无国家级代表性审查指标 |
| Bitmap异常检测 | 将审查时间序列转化为Bitmap表示进行异常检测 | §5.3 | 此前远程技术无纵向分析能力 |
| Mann-Kendall趋势检验 | 99%显著性水平的趋势方向检测 | §5.3 | 此前无大规模审查趋势分析 |
| 快速聚焦机制 | 根据事件告警快速启动定制化深度测量 | §7.3 | 此前平台响应速度慢 |

### 5.3 适用场景

**最适合的场景**：
- 全球审查态势感知：需要了解哪些国家在增加审查
- 审查事件检测：自动发现审查突变事件
- 纵向趋势分析：跟踪审查方法和目标随时间的变化
- 补充OONI/ICLab：提供更大规模和连续性的数据

**不太适合的场景**：
- 精细粒度的本地审查检测（如校园/企业网络）
- 需要终端用户体验的测量
- 需要执行复杂客户端实验的场景
- 审查者可能主动对抗测量的高对抗环境

### 5.4 与其他平台对比

| 平台 | 测量方式 | 国家覆盖 | AS覆盖 | 连续性 | 协议数 | 纵向分析 |
|---|---|---|---|---|---|---|
| OONI | 终端用户志愿者 | 156 | 1,915 AS | 36% | HTTP为主 | 基础 |
| ICLab | VPN节点 | 41 | 48 AS/国 | 64% | 多种 | 基础 |
| Censored Planet | 远程基础设施 | 221 | 9,014 AS | 99% | 6种 | 深度（异常+趋势） |
| CP Potential | 远程基础设施 | 222 | 13,569 AS | - | 6种 | 深度 |

---

## 6. 实验

### 6.1 实验设计和设置

**数据规模**：2018年8月-2020年3月，20个月连续测量
- 总测量数：21.8亿次
- 预处理去除：1.2亿次（5.9%技术故障）
- 标记为封锁：约15亿次（7%）
- 聚类去误报后：约10亿次确认封锁

**观测点规模**（每周）：
- Quack：50,000-60,000观测点
- Satellite：15,000-35,000解析器
- Hyperquack：10,000-25,000 Web服务器
- Augur：500-1,000路由器

**测试列表**：每周2,000域名（CLTL ~1,400 + Alexa Top域名）

### 6.2 数据集详情

| 数据源 | 用途 | 规模 |
|---|---|---|
| Citizen Lab Global Test List (CLTL) | 纵向测量主列表 | ~1,400域名，33个类别 |
| Alexa Top Domains | 补充流行服务 | 补充至2,000域名/周 |
| CAIDA ARK | Augur观测点选择 | 全球路由器数据 |
| Censys | Hyperquack观测点+AS信息 | EV证书服务器 |
| PeeringDB | Hyperquack初始观测点 | 10,000 ISP服务器 |
| Maxmind + Routeviews | 国家/AS元数据 | 99.96%国家/99.86% AS覆盖 |
| Freedom on the Net Report 2019 | 观测点优先级排序 | 65个国家定性排名 |

### 6.3 Baseline 选择理由

本文的"Baseline"主要是与现有平台的比较：
- **OONI**：最大的志愿者审查测量平台，代表直接测量方法
- **ICLab**：基于VPN的审查测量平台，代表另一种直接测量方法

比较理由：两者是审查测量领域的state-of-the-art，且有公开数据可比。

### 6.4 消融实验

本文未进行传统的消融实验，但通过以下方式验证各组件的重要性：

1. **规模的重要性**（Figure 6）：随机采样1-4个Satellite观测点，与基线的相对差异随观测点数量增加而显著降低
2. **平滑的效果**（Figure 2/Appendix A.2）：对比Raw和平滑审查指标，验证平滑去除异常观测点影响
3. **异常检测方法对比**（Appendix A.1）：对比MAD、似然模型、EWMA和Bitmap方法，Bitmap效果最佳

### 6.5 结果表格

**Table 1：检测到的关键审查事件**

| 国家 | 时间 | 方法 | 异常分数 | 类别/域名 | 事件 | OONI数据 |
|---|---|---|---|---|---|---|
| 埃及 | 2019.9.26 | HTTP,HTTPS | 2.74 | 新闻媒体 | 抗议 | 有记录 |
| 伊朗 | 2020.3 | HTTP,Echo | - | wikimedia.com | 政策 | 有记录 |
| 斯里兰卡 | 2019.4.21-5.12 | HTTP,HTTPS | 3.29 | 社交网络 | 恐袭 | 部分记录 |
| 委内瑞拉 | 2019.1.12-29 | HTTP,HTTPS | 3.13 | 社交网络/wikipedia | 动荡 | 有记录 |
| 津巴布韦 | 2019.1.20 | HTTP,HTTPS | 3.3 | 社交网络 | 抗议 | 有记录 |
| 厄瓜多尔 | 2019.10.8 | DNS | 3 | 社交网络 | 抗议 | 新发现 |
| 印度 | 2018.9.6 | DNS | 3.14 | 在线约会 | 法律 | 新发现 |
| 以色列 | 2019.5-6 | DNS | - | 外交军事 | 冲突 | 新发现 |
| 日本 | 2019.6.28 | DNS,Echo | 3.25 | 新闻媒体 | 峰会 | 新发现 |
| 波兰 | 2019.7.22 | DNS,HTTP,HTTPS | 3.2 | 政府/新闻/人权 | 动荡 | 新发现 |
| 苏丹 | 2019.4.11 | HTTP,HTTPS | 3.29 | 社交网络 | 动荡 | 新发现 |
| 喀麦隆 | 2018.11.25 | HTTP | 3.44 | 赌博 | 未知 | 新发现 |
| 印度 | 2020.2-3 | Echo,HTTPS | 3.29 | 非法内容 | 未知 | 新发现 |
| 意大利 | 2019.12.22 | Discard | 3.44 | 人权 | 未知 | 新发现 |
| 挪威 | 2019.12-2020.3 | DNS | 3.45 | 多类别 | 未知 | 新发现 |

**关键发现**：15个事件中10个（2/3）是新发现，OONI数据中无记录，主要原因是志愿者测量稀疏或不连续。

### 6.6 Case Study

**斯里兰卡社交媒体封锁**（§7.1.1）：
- 背景：2019年4月21日复活节爆炸事件后，政府封锁社交媒体
- Censored Planet发现：HTTP(S)审查从0.1%升至2%，检测到22个被封锁域名（此前仅报告7个）
- 持续时间：HTTPS审查持续异常高位至4月底，5月12日再次飙升（此前报告称5月1日已解除）
- 意义：展示了连续纵向测量发现其他平台遗漏的信息

**挪威DNS封锁**（§7.1.2）：
- 背景：挪威在新闻自由指数排名第1，但近年法律鼓励封锁赌博和色情网站
- Censored Planet发现：2019年12月-2020年3月DNS封锁异常高分，25个AS封锁10+域名
- 最严格AS：AS 2116 (CATCHCOM)封锁50+域名
- 被封锁类别：搜索引擎(163.com)、约会(match.com)、人权观察(hrw.org)
- 意义：揭示"自由"国家的审查被低估

**土库曼斯坦快速聚焦**（§7.3）：
- 背景：2020年4月收到审查规避工具请求，调查DNS-over-HTTPS服务器被封锁
- 测量：34个Augur观测点测试15个IP（包括Cloudflare和DoH服务）
- 结果：所有Cloudflare IP在至少18个观测点被封锁，主要在国有AS 20661（覆盖90%+公共IP空间）
- 意义：展示快速聚焦能力，帮助主要浏览器做出政策改变

### 6.7 趋势分析结果

**审查方法趋势**（Figure 8）：
| 方法 | 上升趋势国家数 | 下降趋势国家数 | 典型国家（斜率） |
|---|---|---|---|
| DNS | 123 | 24 | 中国(0.93), 土库曼斯坦(0.15), 伊朗(0.048) |
| HTTPS | 61 | 46 | 乌兹别克斯坦(0.041) |
| HTTP | 41 | 41 | - |
| Echo | 20 | 24 | - |
| Discard | 43 | 16 | 葡萄牙(0.045) |

**Freedom House分类审查趋势**（Figure 9）：
- "不自由"国家：审查率最高，主要由中国和伊朗驱动
- "自由"国家：审查呈上升趋势（如澳大利亚、英国）
- "未考虑"国家：非可忽略的审查量和上升趋势

---

## 7. 学习与应用

### 7.1 方法核心思想

1. **统一框架思想**：将多种独立的远程测量技术整合到统一平台，同步输入、统一输出
2. **纵向分析思想**：从"快照式"测量转变为"连续监测"，通过时间序列分析发现事件和趋势
3. **代表性指标思想**：通过优化平滑消除异常观测点影响，获得国家级代表性审查指标
4. **互补性思想**：远程测量（规模+连续性）与直接测量（精细+确认）互补

### 7.2 可借鉴的技术

1. **Bitmap异常检测**：将时间序列离散化为Bitmap表示，通过滑动窗口距离计算异常分数——可应用于其他网络异常检测场景
2. **Nelder-Mead优化平滑**：为异质性数据源分配权重，消除异常值影响——可应用于分布式测量系统的数据融合
3. **聚类去误报**：迭代分类+DBSCAN图像聚类+人工标注——可应用于其他需要高精度的检测系统
4. **模块化设计**：输入扫描、干扰扫描、数据处理解耦——便于扩展新的测量技术

### 7.3 局限性与改进方向

1. **粒度问题**：基础设施观测点无法检测末端网络审查→可结合OONI等直接测量补充
2. **对抗问题**：复杂审查者可规避测量→可引入流量伪装或随机化探测策略
3. **地理定位**：依赖第三方数据库→可引入多源交叉验证
4. **分析深度**：当前趋势分析较基础→可引入更复杂的机器学习方法（如深度学习异常检测）

### 7.4 对我研究的启发

1. **数据质量优先**：Censored Planet强调去除误报（聚类技术）和获得代表性指标（优化平滑），这对任何测量驱动的研究都至关重要
2. **纵向分析价值**：连续20个月的数据积累使得发现此前未知的事件和趋势成为可能
3. **互补性设计**：不试图取代现有平台，而是通过互补特性（规模、覆盖、连续性）增强整体生态系统
4. **快速响应能力**：快速聚焦机制展示了平台在响应世界事件方面的实用性

### 7.5 可能的研究方向

1. 将Censored Planet数据与OONI/ICLab数据融合，构建更完整的全球审查图景
2. 应用深度学习方法（如Transformer）进行更精细的审查模式识别
3. 研究审查规避技术的有效性随时间的变化趋势
4. 探索审查与政治事件之间的因果关系

---

## 8. 总结

### 8.1 核心思想

> 四种远程技术统一平台，21.8亿数据点纵向分析，发现100+国家审查上升。

### 8.2 速记 Pipeline

```
Input Scanner (CLTL+Alexa + 观测点选择)
  → Interference Scanner (Augur/Satellite/Quack/Hyperquack 同步测量6协议)
    → Initial Sanitization (去除技术故障)
      → Common Schema Aggregation (统一格式)
        → False Positive Filtering (聚类去误报)
          → Optimization Smoothing (Nelder-Mead AS权重)
            → Bitmap Anomaly Detection (事件发现)
            + Mann-Kendall Trend Test (趋势发现)
              → 15 events + 100+ countries upward trends
```

---

## 9. 知识链接

### 相关概念

- [[censorship-circumvention]]：审查规避技术领域
- [[anomaly-detection]]：Bitmap异常检测方法
- [[encrypted-traffic-analysis]]：远程测量检测HTTPS阻断

### 相关方法

- 远程测量技术（Augur/Satellite/Quack/Hyperquack）
- Bitmap时间序列异常检测
- Mann-Kendall趋势检验
- Nelder-Mead数值优化
- DBSCAN聚类

### 相关任务

- [[tunnel-detection]]：相关但不同——Censored Planet检测审查而非隧道
- [[traffic-classification]]：数据预处理中的分类思想可借鉴

### 相关领域

- 互联网测量
- 网络审查研究
- 数字人权

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 21.8亿数据点覆盖221个国家 | "collected and published more than 21.8 billion data points" | Abstract |
| 2/3新发现事件在OONI无记录 | "two-thirds of which have not been reported previously" | Abstract, Table 1 |
| 100+国家审查上升趋势 | "increasing censorship activity in more than 100 countries" | Abstract, §7.2 |
| AS连续性99% | "the AS continuity between scans is extremely high (99.01%)" | §6.1 |
| OONI AS连续性仅36% | "OONI data has an even lower AS continuity of 36%" | §6.2 |
| 审查指标高度自相关 | "Kendall's correlation coefficient τ = 0.93" | §5.3.2 |
| 聚类去除约5亿条误报 | "false positive filtering removes around 500 million measurements" | §5.1.4 |
| 挪威HRW网站被封锁 | "the website of the Human Rights Watch (hrw.org)" | §7.1.2 |
| 土库曼斯坦Cloudflare全面封锁 | "all tested Cloudflare IPs were blocked in at least 18 vantage points" | §7.3 |
| 每月平均1次投诉 | "we received an average of one abuse complaint per month" | §3.1 |

---

## 11. 原始资料链接

- PDF：`00-inbox/PDFs/2020-CCS-Censored_Planet__An_Internet-wide__Longitudinal_Censorship_Observatory.pdf`
- MinerU Markdown：`02-parsed-markdown/2020-CCS-Censored_Planet__An_Internet-wide__Longitudinal_Censorship_Observatory.md`
- 代码仓库：https://github.com/censoredplanet
- 项目网站：https://censoredplanet.org
- 数据发布：论文中提到公开数据快照和历史数据集（具体URL见论文脚注1）

---

## 12. 后续问题

1. Censored Planet在2020年之后的运行情况如何？是否发现了更多重大审查事件？
2. 审查规避工具（如Tor、Psiphon）的有效性如何随Censored Planet检测到的审查趋势变化？
3. Bitmap异常检测方法是否可以应用于其他网络异常检测场景（如DDoS、路由劫持）？
4. 优化平滑方法在审查极度异质的国家（如俄罗斯）效果如何？是否存在过度平滑的风险？
5. 如何应对审查者主动对抗远程测量（如检测并丢弃探测流量）？

---

## 13. 叙事分析

### 13.1 论文的故事线

1. **背景**：全球审查理解有限，现有平台（OONI/ICLab）受限于规模、覆盖、连续性
2. **问题**：远程测量技术虽有潜力，但各自独立运行、缺乏纵向分析能力
3. **方案**：Censored Planet整合四种技术，统一平台，20个月连续测量21.8亿数据点
4. **分析**：优化平滑获得代表性指标，Bitmap异常检测+Mann-Kendall趋势检验
5. **发现**：15个审查事件（2/3新发现），100+国家上升趋势，11类网站面临更多审查
6. **意义**：从"探险式调查"到"天文台式连续监测"的范式转变

### 13.2 论文的修辞策略

**问题-解决方案-证据三段式**：
- 问题：现有平台的三个瓶颈（规模/覆盖/连续性）+ 远程技术的四个不足
- 方案：Censored Planet的模块化设计和分析方法
- 证据：21.8亿数据点的实证分析

**对比强化**：反复与OONI/ICLab对比，强调Censored Planet的规模和连续性优势

**具体案例说服**：斯里兰卡、挪威、土库曼斯坦三个详细案例展示平台能力

### 13.3 论文的逻辑链

```
全球审查理解有限 (Introduction §1)
  → 现有平台瓶颈 (Background §2)
    → 远程测量技术潜力与不足 (Background §2)
      → Censored Planet设计 (Design §3)
        → 数据收集模块 (Data Collection §4)
        → 数据处理模块 (Data Processing §5)
          → 平滑指标 + 异常检测 + 趋势检验
            → 验证：规模/覆盖/连续性评估 (Evaluation §6)
            → 发现：事件/趋势/案例 (Findings §7)
              → 补充OONI/ICLab，揭示未报告事件
```

### 13.4 论文的创新叙事

**"天文台"隐喻**：将审查测量类比为天文学观测，强调从"探险"到"连续监测"的范式转变

**"盲人摸象"问题**：单一技术提供局部视角，统一平台提供完整图景

**"自由国家"发现**：挪威（排名第1）的DNS封锁和"自由"国家的上升趋势，挑战了传统认知

**"快速聚焦"能力**：土库曼斯坦案例展示了平台响应世界事件的实用性，帮助影响浏览器政策

### 13.5 论文的局限性叙事

论文在Limitations部分（§9）坦诚讨论了四个主要局限：
1. 粒度限制：无法检测末端网络审查
2. 技术局限：单向阻断和anycast域名
3. 地理定位依赖：第三方数据库可能不准确
4. 对抗能力：复杂审查者可能规避测量

这种坦诚的局限性讨论增强了论文的可信度，并为后续研究指明了方向。

---
type: paper
title_original: "AVP-Inspect: Coordinated Cyber-Physical Testing for Privacy Analysis of COTS Apple Vision Pro Applications"
title_cn: "AVP-Inspect：面向 COTS Apple Vision Pro 应用隐私分析的协同信息-物理测试"
authors: ["Yichang Xiong", "Yue Xiao", "Vamsi Shankar Simhadri", "Xiaokuan Zhang"]
year: 2026
venue: "CCS 2026"
doi: "10.1145/3830454.3846586"
url: "https://arxiv.org/abs/2609.08103"
pdf: "00-inbox/PDFs/2026-arXiv-AVP-Inspect__Coordinated_Cyber-Physical_Testing_for_Privacy_Analysis_of_COTS_Apple_Vision_Pro_Applications.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-AVP-Inspect__Coordinated_Cyber-Physical_Testing_for_Privacy_Analysis_of_COTS_Apple_Vision_Pro_Applications.md"
status: processed
reading_level: L2
research_area: []
task: []
method: []
dataset: ["self-collected AVP app dataset: 374 apps（324 大规模分析 + 50 人工 ground truth）"]
code: "https://github.com/SECSAT-LAB-GMU/AVP-Inspect"
relevance: medium
created: "2026-09-19"
updated: "2026-09-19"
---

# AVP-Inspect: Coordinated Cyber-Physical Testing for Privacy Analysis of COTS Apple Vision Pro Applications

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | AVP-Inspect: Coordinated Cyber-Physical Testing for Privacy Analysis of COTS Apple Vision Pro Applications |
| 中文标题 | AVP-Inspect：面向 COTS Apple Vision Pro 应用隐私分析的协同信息-物理测试 |
| 作者 | Yichang Xiong（George Mason University）、Yue Xiao（William & Mary）、Vamsi Shankar Simhadri（George Mason University）、Xiaokuan Zhang（George Mason University） |
| 年份 | 2026 |
| 会议/期刊 | CCS '26（2026 ACM SIGSAC Conference on Computer and Communications Security, November 15–19, 2026, The Hague, Netherlands；DOI 10.1145/3830454.3846586）。原按分配登记为 arXiv 2026，聚合时已按解析稿首页的 ACM Reference Format 更正 |
| 研究方向 | XR（Apple Vision Pro / visionOS）应用隐私合规；通过自动化 UI 探索 + 网络流量分析检测隐私披露违规 |
| 任务类型 | 动态隐私合规审计、自动化 UI 探索（3D UI）、设备控制（硬件 HID）、流量-披露一致性比对 |
| 方法关键词 | Coordinated Cyber-Physical Testing、ESP32-S3 蓝牙 HID + 舵机物理按键控制、AirPlay 投屏 + OmniParserV2 UI 识别、DFS 状态图探索 + 同态剪枝、统一隐私分类学（VPVet 扩展至 153 类）、六类违规（Omit/Incorrect/Mismatched Entity/Neglect/Contrary/Purpose）、mitmproxy MITM 抓包 |
| 数据集 | 自采：374 个 AVP 应用（含 50 应用人工 ground truth 数据集，48 人时标注；324 应用大规模分析） |
| 是否开源 | 是：artifact 见附录 B Open Science，https://github.com/SECSAT-LAB-GMU/AVP-Inspect |
| PDF | 00-inbox/PDFs/2026-arXiv-AVP-Inspect__Coordinated_Cyber-Physical_Testing_for_Privacy_Analysis_of_COTS_Apple_Vision_Pro_Applications.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-arXiv-AVP-Inspect__Coordinated_Cyber-Physical_Testing_for_Privacy_Analysis_of_COTS_Apple_Vision_Pro_Applications.md |

---

## 1. 一句话总结

> 用硬件 HID + 3D UI 探索 + 流量分类学，自动审计 324 个 Vision Pro 应用，发现 188 个（58.0%）存在隐私披露违规。

---

## 2. 摘要翻译

### 2.1 摘要原文

XR devices introduce substantial privacy concerns due to their comprehensive data collection capabilities that surpass traditional computing platforms. While existing works have demonstrated privacy concerns on Android-based XR devices such as Meta Quest series by performing network traffic analysis, little attention has been paid to the Apple Vision Pro (AVP) devices, mainly due to the closed nature and the technical challenges associated with AVP devices. In this work, we make a bold attempt to detect privacy violations of AVP applications from network traffic through automatic testing on AVP devices. Our key insight is that effective AVP application testing requires coordinated control of both cyber (software) and physical (hardware) components, which we term Coordinated Cyber-Physical Testing. Building on this insight, we design and implement AVP-Inspect, an automatic dynamic analysis framework for AVP applications, overcoming significant challenges enforced by the closed-source nature of AVP ecosystem. AVP-Inspect consists of three components: an automatic device controller by building customized hardware devices, a 3D UI explorer by designing a new exploration engine, and a privacy violation detector by constructing a unified privacy taxonomy for AVP. We first evaluated AVP-Inspect on a manually constructed ground truth dataset, then performed a large-scale analysis on 324 AVP applications downloaded from the App Store, with each app tested for 20 minutes. We found that 188 (58.0%) of apps exhibit at least one violation, and more than 60% of the network traffic flows are not properly disclosed.

### 2.2 摘要中文翻译

XR 设备因其超越传统计算平台的数据采集能力而带来显著的隐私问题。已有工作通过对 Meta Quest 等基于 Android 的 XR 设备做网络流量分析揭示了隐私风险，但 Apple Vision Pro（AVP）设备受到的关注很少，主要因为 AVP 生态封闭且技术门槛高。本文做了一次大胆尝试：通过在 AVP 设备上的自动化测试，从网络流量中检测 AVP 应用的隐私违规。我们的核心洞察是：有效的 AVP 应用测试需要协同控制信息（软件）与物理（硬件）两部分，我们称之为 **Coordinated Cyber-Physical Testing**。基于该洞察，我们设计并实现了 AVP-Inspect——一个面向 AVP 应用的自动化动态分析框架，克服了 AVP 生态闭源带来的多项重大挑战。AVP-Inspect 由三个组件构成：通过定制硬件实现的自动设备控制器、设计新探索引擎的 3D UI 浏览器、以及基于统一 AVP 隐私分类学构建的隐私违规检测器。我们先在人工构造的 ground truth 数据集上评估 AVP-Inspect，随后对从 App Store 下载的 324 个 AVP 应用做大规模分析，每个应用测试 20 分钟。结果发现 188 个（58.0%）应用至少存在一项违规，且超过 60% 的网络流量未被正确披露。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- XR 设备持续采集生物与行为数据（眼动、面部表情、手势、全身动作），已有研究证明可从中提取密码、个人特征与健康状况；同时 GDPR/CCPA 等法规要求应用透明、正确地记录数据采集与共享（`§1`）。
- 已有 XR 隐私研究集中在 Meta Quest（Ovrseen、VPVet 等），但 AVP 因硬件/软件栈差异大、苹果禁止第三方系统分析而缺乏安全测试框架；AVP 2024 年初发布，没有可用的自动化测试工具，导致平台的隐私保护状况无人系统评估（`§1`）。

### 3.2 现有方法的痛点和不足

- **C1 缺乏编程接口**：AVP 无 root/调试接口，无 ADB 类等价物，也无标准输入输出端口，安卓/iOS 的自动化测试框架（Macaca、XCUITest）均不可用，物理键也无法用软件模拟（`§1`, `§3.1`）。
- **C2 3D UI 难以探索**：AVP 应用没有 XML 类 UI 文档；3D 界面的状态随头部朝向与物理位置变化，同一功能状态在视觉上可能完全不同，状态空间指数膨胀（`§1`, `§3.1`, Fig. 2）。
- **C3 分类学不足**：检测违规需要把包中的低层标识映射到 Apple 多层隐私文档（policy / label / manifest）中的高层数据类别，而 VPVet、OVRSeen 等既有分类学不覆盖 AVP 专属数据类型，也不处理 Apple 三套文档体系的映射问题（`§1`, `§3.1`）。

### 3.3 论文的研究假设或核心直觉

核心直觉：**有效的 AVP 应用测试必须协同控制"信息（软件）"与"物理（硬件）"两部分**——用可编程蓝牙 HID 制造虚拟光标输入、用舵机按压物理按键、用投屏做视觉反馈，从而在完全无 root、无源码的条件下形成闭环控制；再配合 3D UI 状态图探索与统一隐私分类学，把"流量中的实际数据"与"文档中的声明"对照起来（`§1`, `§3.2`）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | XR 设备采集数据远超传统平台；AVP 已有实际部署（含手术辅助等），但缺少任何隐私分析 | `§1` |
| 痛点提炼 | AVP 封闭（无 root、无 ADB 类接口、无 UI 层级文档），既有 XR 隐私方法无法移植；测试还必须覆盖 3D 交互 | `§1`, `§3.1` |
| 问题转化 | 如何在不获取源码/root 的前提下，自动化驱动 AVP 应用产生可归因的交互流量，并判定其是否与隐私文档一致 | `§3`（违规定义） |
| 文献定位 | Quest 侧有 Ovrseen/VPVet/Guo et al. 等；AVP 侧为空白；XR 动态测试工作（VRTest、VRExplorer、AutoVR 等）都依赖源码/root/标准测试套件，不适用于 AVP | `§1`, `§8`, `§I` |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 用"蓝牙 HID + 舵机物理键 + 投屏视觉反馈"的协同软硬件控制，可在无 root/无源码条件下自动探索 AVP 应用并触发交互驱动的网络流量 | `§1`, `§4.1`, `§4.2` | 50 应用 ground truth 上覆盖 151/157 违规（96.2%）；Auto 流量为 Idle 的 3.15×（`§5.2`, `§5.3`） |
| 辅助假设 | 把 VPVet 分类学扩展到 AVP 专属数据类型并做短语-术语映射，可把包内 key 映射到 Apple 三类隐私文档类别 | `§4.3` | 扩展至 153 个数据类型；在 324 应用上检出 3,452 条违规 |
| 辅助假设 | 大多数 AVP 应用流量的隐私合规问题源于第三方 SDK，而非自有代码 | `§6.1`–`§6.4` | 政策层面 90.9% 的遗漏来自第三方；SDK 相关违规集中于 Productivity/Entertainment（`§6.4`） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 自动化探索有效 | 支撑 | 违规覆盖 96.2%（151/157）；最低的 WWidgets 为 50.0%（2/4） | `§5.2`, Table 1 |
| 探索触发交互流量 | 支撑 | 1,276 vs 405 请求（3.15×）；每分钟 3.51 vs 0.63（5.58×）；Broadcasts 238 vs 1（238×） | `§5.3`, Table 3（附录 F） |
| 违规普遍存在 | 支撑 | 324 应用中 247（76.2%）产生流量，188（58.0%）至少一项违规；61.1% 的隐私相关流量未披露 | `§6`, `§6.7` |
| AVP 专属传感器数据外泄 | 反驳（未观测到） | 3,452 条违规中仅 46 条（1.3%）映射到 AVP 专属类型，且无一条含原始 XR 传感器测量 | `§6.7` |

---

## 4. 方法设计

### 4.1 方法整体流程

AVP-Inspect 的工作流（`§4`, Fig. 3）：设置阶段用 AVP 自带 AirPlay 把屏幕镜像到 MacBook 并周期截图 → Explorer 分析截图并指挥 Controller 打开目标应用 → 探索过程中 Explorer 与 Controller 频繁交互以决定下一步；同时用 mitmproxy 抓取流量 → Detector 把流量与应用的隐私政策/标签/manifest 对照 → 生成报告，列出含违规的流量与涉及的数据类型。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 设备准备 | AVP（visionOS 2.1）+ MacBook M2 Pro | AirPlay 投屏到 MacBook，MacBook 周期截图；mitmproxy 做 MITM 抓包；截图发到 Lambda Vector Pro 服务器跑 OmniParserV2 | 截图流 + 网络流量 | 建立视觉反馈与流量采集链路（`§5`, Appendix K） |
| Step 2 应用启动 | App ID 列表 | 自动脚本从 App Store 下载安装，用 Spotlight 搜索打开，用 Digital Crown 居中视图，开始 20 分钟测试 | 前台运行的目标应用 | 统一测试协议（`§5`, Appendix K） |
| Step 3 UI 探索 | 截图 | Controller 用蓝牙 HID 移动虚拟光标、舵机按物理键；Explorer 构建 DFS 状态图，点击未探索按钮，必要时按 Back/关闭弹窗/重启应用跳转状态 | UI 状态图 + 触发流量 | 最大化交互驱动的流量（`§4.2`, Algorithm 1） |
| Step 4 流量解析 | HTTP 请求 | 解析 header、URL query、body（嵌套 JSON/XML 递归展平）得到 key-value；用同义词匹配 / key 模式（`*_id`、`*_token`）/ value 模式（IP 正则）映射到分类学节点 | 映射后的数据类型集合 | 从流量提取隐私数据类型（`§4.3`） |
| Step 5 违规判定 | 流量数据类型 + 三类隐私文档 | 对 policy / label / manifest 分别比对，判定六类违规（Omit / Incorrect / Mismatched Entity / Neglect / Contrary / Purpose） | 违规清单与报告 | 输出可复核的合规结论（`§4.3`, `§6.1`–`§6.5`） |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Controller | 解决 C1：用 ESP32-S3 蓝牙 HID 产生虚拟光标/键盘输入，用舵机按压 AVP 物理键（Digital Crown、Top button）；含数字-物理反馈驱动流水线 | Explorer 的目标坐标/动作指令 | 光标移动、点击、按键 | 受 Explorer 指挥；论文首选低成本的 RoboTest 式非侵入方案（`§4.1`, Appendix K.1） |
| Explorer | 解决 C2：投屏截屏 → 光标定位（改绿色圆环 + 颜色过滤 + Hough 圆变换）→ 二分搜索式光标移动（2D 坐标 → 3D 空间）→ OmniParserV2 检测 UI 元素 → DFS 状态图 + 同态剪枝 | 截图 + 状态图 | 下一步动作指令；状态图 | 与 Controller 构成控制闭环（`§4.2`, Algorithm 1） |
| Detector | 解决 C3：构建统一隐私分类学（VPVet 106 类 + 政策新增 12 + 标签新增 35 = 153 类）、从流量提取 key 并映射、比对三类文档判定违规 | 流量 + policy/label/manifest | 违规清单 | 消费 Explorer/Controller 产生的流量（`§4.3`, Fig. 11） |
| 统一分类学 | 用 `is-a` 关系把低层类型挂到 Apple 标签类别下（如 traffic 侧 `user id` ↔ Apple 的 `User ID`），两名标注者独立标注、第三人仲裁 | 政策三元组（PrivBERT）、Apple 标签类别、manifest 的 `NSPrivacyCollectedDataTypes` | 153 类层级分类学 | 是 Detector 的判定基础（`§4.3`, Appendix E） |

### 4.4 公式、算法和机制解释

- **违规定义**：唯一违规 = 出现在流量中但未被隐私文档覆盖的 `(key, category)` 对；按文档来源分三类（policy / label / manifest violation）（`§4.3`）。
- **六类违规语义**（`§3.2`, `§6.1`–`§6.3`）：Omit（采集了但政策未提及）、Incorrect（采集了但政策反向声明不采集）、Mismatched Entity（数据实际发给第三方但政策归因给第一方）、Neglect（采集了但标签/清单完全没声明）、Contrary（标签/清单明确声明不采集某类数据却实际采集）、Purpose（声明用途与运行时推断用途不符）。
- **Algorithm 1（状态探索）**：DFS 维护状态图 G；`CheckCurrentState()` 用 OmniParserV2 提取元素并判断是否已知状态；未知则加入 G 并加边，已知则 `ResumeExploreState()`；无未探索按钮时 `TryClickBackButton()`；需要跳转时 `JumpToCurrentState()` 重启应用并重放路径（`§4.2`, Appendix D）。
- **状态去重**：以检测到的 UI 元素的 (position, size) 计算相似度，超过阈值即视为同一状态；转移时若 B 与 A 的某个已探索邻接状态匹配则返回 A，否则作为新邻接状态加入（`§4.2`）。
- **Algorithm 2（新数据类型发现）**：对未映射短语做 embedding，选代表短语为候选，相似度 ≥ 0.8（θ）的短语归为一组，重复直至无新类型，再人工插入分类学层级（`§4.3`, Appendix D）。
- **Purpose 推断**：复用 Lalaine 的用途分类器（基于应用元数据与网络层特征预测 Apple 的五种用途）与标签声明用途比较（`§6.5`）。

### 4.5 方法优势

- 完全非侵入：不需要 root、不需要源码、不需要越狱，仅靠外设与投屏，适配闭源平台（`§1`, `§4.1`）。
- 端到端自动化：从应用下载安装、启动、探索到违规报告全流程自动化，每应用 20 分钟即可覆盖大部分违规（96.2% 的 GT 违规）（`§5.2`）。
- 覆盖三类隐私文档：比只查政策（Ovrseen）或只查标签（Lalaine/PoliCheck）的工作更全面，能发现 manifest 层面的矛盾（`§4.3`, `§6.3`）。
- 结果可归因：违规报告定位到具体 key 与数据类型（如 `x-crashlytics-installation-id`、`RealityDevice14,1`），可直接用于向开发者/苹果披露（`§6.5`, `§6.6`）。

### 4.6 方法不足

- 依赖 OmniParserV2 做元素识别，存在随机性与误差；无法模拟需要手部动作的复杂交互，因此无法探索沉浸式场景（`§J.2`）。
- 无法创建账号或完成应用内购买，登录墙/付费墙后的功能不可达：2 个应用几乎全部功能在登录墙后，5 个应用部分高级功能付费门槛，实际可完整探索 48/50（`§J.2`）。
- 分类学同义词表继承自 PoliCheck/VPVet，个别映射过宽（如 `password` 的同义词含 `token`，会把认证令牌计入密码类）（`§J.2`）。
- 仅 20 分钟探索，得到的是违规率的**保守下界**（`§6.7`）。
- 流量经 MITM 解密获取（论文报告未遇到证书固定），对启用证书固定的应用可能失效（`§5.2`, Appendix N）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

与 Ovrseen（Quest 平台、被动收集流量 + 政策比对）、VPVet（10 个 VR 平台的政策审查工具）、Lalaine/PoliCheck（iOS 侧标签-流量一致性）相比，本文的区别是**平台 + 自动化驱动 + 文档层次**三点：对象换成闭源程度最高的 AVP；用软硬件协同控制实现无 root 的自动 UI 探索（而非被动收集或依赖调试工具）；判定覆盖 policy + label + manifest 三套文档（`§8`, `§7`）。与 XR 动态测试工具（VRTest、VRExplorer、AutoVR 等）相比，区别在于不依赖源码、root 或平台测试套件（`§8`, "XR dynamic testing"）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| Coordinated Cyber-Physical Testing 范式 | 把"软件控制 + 硬件控制"协同作为闭源 XR 设备自动测试的方法论 | 高 | 是（任何无调试接口的设备，如其他 XR、车机、游戏主机） |
| 低成本非侵入控制器 | 蓝牙 HID + 舵机 + AirPlay 投屏 + 二分搜索光标定位（RoboTest 思路在无触屏设备上的改造） | 高 | 是 |
| 3D UI 状态图探索 | 以 (position,size) 相似度做视角变化下的状态去重，配合 DFS + 重启重放 | 中 | 是 |
| AVP 统一隐私分类学 | 在 VPVet 基础上扩展到 153 类，并对齐 Apple 三套文档 | 中 | 部分（需适配其他平台文档体系） |
| 大规模实证 | 首个 AVP 生态隐私实测（324 应用、25,901 请求） | 高 | — |

### 5.3 适用场景

适合"平台封闭、无调试接口但需要真实运行行为证据"的合规审计场景（XR 隐私审计、应用商店审核辅助、第三方合规验证）；也适合 XR 应用的可用性/性能测试（作者在 `§J.3` 提出可扩展为 XR fuzzing 与性能测试）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| Ovrseen（Quest 隐私） | 首个 VR 应用流量-政策一致性研究 | 仅政策层；Quest 平台；被动流量收集 | 扩展到 policy+label+manifest，并用主动 UI 探索触发流量 |
| VPVet（VR 政策审查） | 覆盖 10 个平台的分类学 | 静态政策审查，不看运行时流量 | 构建运行时流量到文档的映射，实测 324 应用 |
| Lalaine / PoliCheck（iOS 标签一致性） | 成熟的标签比对与用途分类器 | 面向手机 2D UI，不适用于 AVP 的 3D 交互与封闭系统 | 本文复用其分类器/同义词，但重做控制与探索层 |
| RoboTest（机械臂 GUI 测试） | 非侵入视觉驱动 | 面向有触屏的智能手机，无深度/视角问题 | AVP 无触屏与绝对映射，改用蓝牙 HID + 舵机 + 二分搜索 |
| VRTest / VRExplorer / AutoVR 等 XR 测试 | 覆盖 XR 场景探索 | 依赖源码/root/标准测试套件，不适用 AVP | 完全不依赖源码与平台工具 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

实现：286 行 ESP32 代码 + 约 3,000 行 Python；控制器用 Arduino ESP32-S3（内置 BLE）；UI 识别用预训练 OmniParserV2；流量用 MITM（mitmproxy）截获（`§5`）。环境：AVP 运行 visionOS 2.1，投屏到 MacBook M2 Pro（32GB，macOS Sequoia），OmniParserV2 跑在 Lambda Vector Pro 服务器（Threadripper PRO 7985WX 64 核、2× NVIDIA RTX A6000 48GB、256GB RAM、10TB NVMe）（`§5`）。协议：每个应用自动下载安装、Spotlight 打开、Digital Crown 居中、测试 20 分钟、强制退出；用启停时间戳切分流量（`§5`）。

### 6.2 数据集

- 应用枚举来自第三方目录站（官方 Vision Pro App Store 不提供列表）：671 个应用，其中 460 个免费；排除 86 个不适用者（16 个 Apple 系统应用、4 个无法获取 IPA 的 Microsoft 应用、20 个需订阅的 Apple Arcade 游戏、46 个需要更新 visionOS 的应用——含 7 个需 2.2–2.6、39 个需 visionOS 26.x），最终 374 个应用完成测试与分析（`§5.1`）。
- Ground truth 数据集：从 374 个中选 50 个应用（覆盖 top-10 热门类别、按类别规模比例选取，每类至少 2 个），人工探索触发所有交互元素并人工分析流量，共约 48 人时；其中 31 个应用在人工或自动探索中产生流量（`§5.1`, Table 1）。
- 大规模分析集：其余 324 个应用，同时抽取元数据、隐私政策 URL、隐私标签与 IPA 内的 privacy manifest（`§5.1`）。

### 6.3 Baseline

无同类自动化 baseline；对照来自 (1) 人工探索（ground truth 违规集）；(2) Idle 基线（应用前台不动 20 分钟，用于证明流量由交互驱动）；(3) 与 Ovrseen 在 Quest 上的违规率做横向比较（58.0% vs 58.6%）（`§5.3`, `§7`）。

### 6.4 评价指标

- 违规覆盖率：自动化发现的 GT 违规比例（151/157 = 96.2%）（`§5.2`）。
- 探索有效性：Auto vs Idle 的唯一网络请求数与每分钟请求数（3.15× / 5.58×）（`§5.3`, Table 3）。
- 违规口径：唯一违规 = 流量中出现但文档未覆盖的 `(key, category)`；统计中一个请求可含多条违规（Table 1 注）（`§4.3`, Table 1）。
- 分流率：`188/324`（有流量应用中 247 个的 76.2% 产生流量）（`§6`）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---|---|---|---|
| 50 应用 GT（31 个有流量） | 违规覆盖率 | 96.2%（151/157） | 人工探索（上限） | — | 最低为 WWidgets 50.0%（2/4，需更多导航步骤）`§5.2`, Table 1 |
| 探索有效性（50 应用） | 唯一请求数 / 每分钟 | Auto 1,276 / 3.51 per-min | Idle 405 / 0.63 per-min | 3.15× / 5.58× | 26 个应用两种条件下均有流量，其中 17 个 Auto 更多、7 个持平 `§5.3` |
| 探索有效性（个案） | 请求数 | Broadcasts 238、alo Sanctuary 102 | Idle 各 1 | 238× / 102× | 交互密集型应用差距最大 `§5.3` |
| 324 应用大规模分析 | 产生流量的应用 | 247（76.2%），合计 25,901 请求 | — | — | 77 个（23.8%）无流量 `§6` |
| 隐私合规（总体） | 违规应用比例 | 188/324（58.0%）；61.1% 流量未正确披露 | Ovrseen（Quest）：58.6% | 量级相当 | 20 分钟探索，属保守下界 `§6.7`, `§7` |
| 隐私政策（212 个可分析） | 违规条数 | Omit 1,222（137 应用）、Incorrect 29（12 应用）、Mismatched Entity 278（81 应用） | — | — | Omit 中仅 9.1% 涉第一方；常见第三方为 RevenueCat、Unity Analytics、Google/Firebase、Mixpanel `§6.1` |
| 隐私标签 | 违规条数 | Neglect 1,127（63.1%）、Contrary 658（36.9%，影响 64 应用、1,423 条请求） | — | — | 最常被忽视的是 diagnostic data、usage info、device id `§6.2` |
| Privacy Manifest | 覆盖与违规 | 324 应用中仅 84（25.9%）含 manifest；41/84（48.8%）存在违规，共 138 条（23 Contrary + 115 Neglect） | — | — | 84 个中仅 30（35.7%）声明 `NSPrivacyCollectedDataTypes`；23 个设 `NSPrivacyTracking=False` 却向 mixpanel.com/amplitude.com/doubleclick.net 发送数据 `§6.3` |
| 违规分类别分布 | 应用数 / 违规数 | 合计 188 / 3,452；Productivity 26/568、Entertainment 30/501、Utilities 19/275、Graphics&Design 12/229 | — | — | `§6.4`, Table 2 |
| Purpose 违规 | 高频数据类型 | Other Diagnostic Data 50、Device ID 39、Gameplay Content 36、Precise Location 35、Name 33、Phone Number 30 | — | — | Analytics 是主要被忽视的用途 `§6.5`, Fig. 9/10 |
| AVP 专属泄漏 | 占比 | 46/3,452（1.3%），且无一条含原始 XR 传感器测量 | — | — | 静态分析显示 374 应用中 54 个声明 XR 传感器用途字符串、39 个链接需授权的 ARKit provider `§6.7` |

### 6.6 优势最明显的场景

- 交互密集、页面层级深的应用（如 Broadcasts、alo Sanctuary、Callsheet、Theater），自动化探索相对 Idle 能获得数十到数百倍的流量增益。
- 需要发现"标签/manifest 与运行时行为直接矛盾"的场景：例如 manifest 声明不追踪却发送数据到已知追踪域，或标签声明"不采集"却实际采集（Contrary 658 条）。
- 需要把责任定位到第三方 SDK 的场景：本研究中 SDK 是主要的未披露流量来源（`§6.4`, `§6.7`）。

### 6.7 局限性

- 沉浸式场景不可探索（无手部动作模拟），不过人工检查显示 GT 中 4 个有沉浸式场景的应用均不产生网络流量（`§J.1`, `§J.2`）。
- 登录墙与内购墙后的功能不可达：2 个应用几乎全部在登录墙后、5 个应用部分功能付费门槛（`§J.2`）。
- 元素识别依赖 OmniParserV2，存在随机性与错误（`§J.2`）。
- 分类学同义词继承自 PoliCheck/VPVet，个别过宽（`password` 含 `token`），相应流量应理解为"认证相关"而非密码外泄（`§J.2`）。
- 与 Ovrseen 一样只覆盖网络可观测的披露问题；端侧数据使用不在检测范围（`§7`, `§J.2`）。

---

## 7. 学习与应用

### 7.1 是否开源？

是。附录 B Open Science 给出 artifact 地址：https://github.com/SECSAT-LAB-GMU/AVP-Inspect 。论文未声明数据集是否一并发布（Ground truth 数据集与 374 应用元数据/隐私文档集的公开范围未在解析稿中说明——解析稿未明确）。

### 7.2 复现关键步骤

1. 准备硬件：AVP（visionOS 2.1）+ ESP32-S3 蓝牙 HID 控制器 + 舵机（按压 Digital Crown / Top button）+ 稳定支架（论文用化妆训练头模固定在台钳支架上）。
2. 配置采集链路：AVP 用 AirPlay 投屏到 MacBook，MacBook 周期截图并跑 mitmproxy 抓包；截图发往 GPU 服务器跑 OmniParserV2。
3. 修改并标定光标：在系统设置里把光标改成带外圈的绿色圆点，用颜色过滤 + Hough 圆变换定位。
4. 枚举目标应用并用脚本自动下载安装（App Store + ipatool 取 IPA 与 manifest），逐个启动、Digital Crown 居中、探索 20 分钟。
5. 探索循环：OmniParserV2 提取 UI 元素 → DFS 状态图 → 二分搜索驱动光标 → 点击未探索按钮 → 同态剪枝 → 必要时 Force Quit 重启并重放路径。
6. 分析：解析 HTTP 请求的 key-value，映射到 153 类分类学，与 policy（PrivBERT 三元组抽取）/ label（Apple 类别）/ manifest（`NSPrivacyCollectedDataTypes`）比对，输出违规清单。

### 7.3 关键超参数、预处理和训练细节

- 每应用探索时长 20 分钟（Idle 基线同样 20 分钟，且按 Auto 的活跃区间等长裁剪）（`§5`, `§5.3`）。
- 光标移动二分搜索的初始步长 λ 与位置阈值 δ、状态相似度阈值、taxonomy embedding 相似度阈值 θ = 0.8（`§4.2`, `§4.3`, Algorithm 2）。
- 无训练过程；使用现成模型 OmniParserV2（UI 元素检测）与 PrivBERT（政策三元组抽取）、Lalaine 用途分类器（`§4.3`, `§6.5`）。
- 前置条件：安装 MITM 证书以解密 TLS；论文报告未遇到证书固定（`§5.2`, Appendix N）。

### 7.4 能否迁移到其他任务？

- **Coordinated Cyber-Physical Testing 范式可直接迁移**到其他闭源、无调试接口的设备（其他 XR 头显、车机、智能电视、游戏主机）：核心是"用外设制造标准输入 + 用投屏/摄像头做反馈"形成闭环。
- **3D UI 状态图探索 + 视角不变式去重**对空间计算类应用测试通用。
- **运行流量 ↔ 多层隐私文档比对**的框架可迁移到其他平台（Android XR、Quest），只需替换文档解析器与分类学。
- 作者提出可扩展为 XR 应用的功能 fuzzing、性能测试与基于 VLM 的 XR UI 语义研究（`§J.3`）。

### 7.5 对我的研究有什么启发？

- 这篇论文对"没有 ground truth 的状态识别"给出了务实处理：不假装能评估 UI 状态覆盖率，而是把评估收敛到下游真正消费的产物（违规集合），这种"只评估可定义指标"的做法值得借鉴。
- 自动化探索阈值（20 分钟）与覆盖率（96.2%）的关系说明：对合规审计类任务，短时自动探索已能拿到大部分可观测证据，成本-收益评估可作为同类工具的设计参考。
- 隐私分类学的构建流程（提取 → 映射 → embedding 聚类 → 人工仲裁）是一个可复用的"跨文档体系对齐"方法模板。
- 该文与流量分析的关系在"网络流量作为行为审计证据"这一层：不训练分类器，而是用 key/值模式匹配 + 文档比对，属于规则+知识驱动的流量解释路线，可与 KB 中 ML 驱动的隐私/分类工作形成方法论对照。

---

## 8. 总结

### 8.1 核心思想

> 软硬件协同控制闭源 XR，用流量证据审计隐私披露。

### 8.2 速记版 Pipeline

1. 用蓝牙 HID + 舵机 + AirPlay 投屏构建无 root 的设备控制闭环。
2. OmniParserV2 识别 UI 元素，DFS + 同态剪枝探索 3D UI 状态图。
3. mitmproxy 抓取交互驱动的 HTTP 流量并解析 key-value。
4. 映射到扩展后的 153 类 AVP 隐私分类学，与政策/标签/manifest 三类文档比对。
5. 输出违规清单（六类违规），汇总到应用与类别维度并做负责任披露。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- 暂无匹配：本文不分析加密流量的元数据/侧信道，而是通过 MITM 解密后比对明文 key 与隐私文档；ETA 概念页明确限定"不解密 payload"的前提，故不链接 encrypted-traffic-analysis 概念页。

### 9.2 相关方法

- 暂无匹配：本文使用现成检测模型（OmniParserV2、PrivBERT、Lalaine 分类器）作组件，方法主体是系统/测试框架，不属于白名单中的 ML 方法页（transformer / CNN / GNN / 预训练 / 对比学习 / 自监督 / 状态空间模型）。

### 9.3 相关任务

- 暂无匹配：白名单任务页面向流量分类/指纹/检测任务；本文任务是隐私合规审计与自动化 UI 测试，故留空。

### 9.4 可更新的综述页面

- 暂无匹配：现有 5 个综述页均面向 ML 流量分析主题。

### 9.5 可加入的对比表

- [[open-source-registry]] —— 本文 artifact 已公开（https://github.com/SECSAT-LAB-GMU/AVP-Inspect ），可登记为"XR 应用隐私审计（基于网络流量）"工具。

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 自动化探索可在 20 分钟内覆盖 96.2% 人工发现的违规 | 151 / 157 GT 违规；最低 WWidgets 2/4 | `§5.2`, Table 1 |
| 交互驱动的流量显著多于 Idle | 1,276 vs 405 请求（3.15×）；3.51 vs 0.63 per-min（5.58×） | `§5.3`, Table 3 |
| 188/324（58.0%）应用存在至少一项披露违规 | 与 Ovrseen 在 Quest 上的 58.6% 量级相当 | `§6.7`, `§7` |
| 违规以第三方 SDK 为主要来源 | 政策遗漏中仅 9.1% 为第一方；常见第三方为 RevenueCat、Unity Analytics、Google/Firebase、Mixpanel | `§6.1`, `§6.4` |
| Manifest 采用率低且常被当作合规勾选项 | 仅 84/324（25.9%）有 manifest；仅 30/84 声明采集数据；41/84 存在违规 | `§6.3` |
| 无原始 XR 传感器数据外泄的证据 | 46/3,452（1.3%）为 AVP 专属类型且不含原始传感器测量；54 应用声明传感器用途、39 应用链接 ARKit provider | `§6.7` |
| 分类学需扩展到 AVP 专属类型 | VPVet 106 类 + 政策 12 + 标签 35 = 153 类 | `§4.3` |
| 设备控制的硬件方案 | ESP32-S3 蓝牙 HID + 舵机；286 行 ESP32 代码 + 约 3,000 行 Python | `§5`, Appendix K |
| 已向苹果与开发者披露并获回应 | 119/188 应用找到开发者联系方式，收到 10 份回应；苹果确认并复现了发现 | `§6.6` |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-arXiv-AVP-Inspect__Coordinated_Cyber-Physical_Testing_for_Privacy_Analysis_of_COTS_Apple_Vision_Pro_Applications.pdf
- MinerU Markdown：02-parsed-markdown/2026-arXiv-AVP-Inspect__Coordinated_Cyber-Physical_Testing_for_Privacy_Analysis_of_COTS_Apple_Vision_Pro_Applications.md
- Artifact（论文附录 B）：https://github.com/SECSAT-LAB-GMU/AVP-Inspect

---

## 12. 后续问题

- 20 分钟探索得到的是保守下界，论文未报告探索时长与违规覆盖率的关系曲线（仅附录 M 提到 1 小时运行），延长到多久趋于饱和？
- 该框架是否适用于其他 visionOS 版本（如 26.x）与其他 XR 平台（Quest/Android XR）？移植成本主要在哪一层（Controller 硬件 vs 分类学）？
- Privacy Manifest 声明 `NSPrivacyTracking=False` 却发送到追踪域的行为，是否可以构成应用商店审核层面的可自动化检测项？
- 论文未说明 ground truth 数据集与应用元数据是否会随 artifact 一并发布；若要复现"违规覆盖率 96.2%"这一指标，需要人工重建 GT。
- 分类学中"purpose"层依赖 Lalaine 的用途分类器（基于元数据与网络特征），其准确率对 Purpose 违规数量的影响未做敏感性分析。
- 该文的 key/value + 文档比对路线与 KB 中 ML 驱动的隐私/流量分类方法（如标签一致性研究）如何互补？规则法在 SDK 快速迭代下的维护成本如何？

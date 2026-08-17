---
type: paper
title_original: "The First Early Evidence of the Use of Browser Fingerprinting for Online Tracking"
title_cn: "浏览器指纹用于在线跟踪的首个早期证据"
authors: ["Zengrui Liu", "Jimmy Dani", "Yinzhi Cao", "Shujiang Wu", "Nitesh Saxena"]
year: 2025
venue: "WWW 2025"
doi: "10.1145/3696410.3714548"
url: "https://doi.org/10.1145/3696410.3714548"
pdf: "00-inbox/Aug_inbox/2025-WWW-The_First_Early_Evidence_of_the_Use_of_Browser_Fingerprinting_for_Online_Tracking.pdf"
mineru_md: "02-parsed-markdown/2025-WWW-The_First_Early_Evidence_of_the_Use_of_Browser_Fingerprinting_for_Online_Tracking.md"
status: processed
reading_level: L3
research_area: ["web privacy", "browser fingerprinting", "online advertising", "online tracking measurement", "consent management"]
task: ["online tracking measurement", "ad targeting analysis", "cookie restoration analysis"]
method: ["controlled A/B experiment", "browser fingerprint spoofing", "Gummy Browser", "header bidding monitoring", "OpenWPM crawling", "HTTP traffic analysis"]
dataset: ["self-collected bid/HTTP/cookie data (US, EU-GDPR, US-CA-CCPA locations; 4 CMPs + NAI)"]
code: unknown
relevance: medium
created: "2026-08-17"
updated: "2026-08-17"
---

# The First Early Evidence of the Use of Browser Fingerprinting for Online Tracking

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | The First Early Evidence of the Use of Browser Fingerprinting for Online Tracking |
| 中文标题 | 浏览器指纹用于在线跟踪的首个早期证据 |
| 作者 | Zengrui Liu（南京财经大学/德州农工大学）、Jimmy Dani（德州农工大学）、Yinzhi Cao（约翰霍普金斯大学）、Shujiang Wu（F5 Inc.）、Nitesh Saxena（德州农工大学，通讯） |
| 年份 | 2025 |
| 会议/期刊 | WWW 2025（ACM Web Conference 2025，2025-04-28~05-02，澳大利亚悉尼），16 页 |
| 研究方向 | Web 隐私、浏览器指纹、在线广告跟踪测量、隐私法规（GDPR/CCPA）合规 |
| 任务类型 | 测量研究：验证浏览器指纹是否真的被广告生态用于用户跟踪与定向投放 |
| 方法关键词 | FPTrace 框架（OpenWPM + Prebid.js 出价采集 + Gummy Browser 指纹伪装 + ModHeader 头部伪装）、受控 A/B 实验、Cookie 恢复检测 |
| 数据集 | 自建测量数据：竞价（bid）数据、HTTP 链/同步事件/记录数、Cookie 导出对比；美国无法规地区 + AWS 法兰克福（GDPR）+ AWS 加州（CCPA）；4 个 CMP（Cookiebot、Quantcast、Onetrust、Didomi）+ NAI |
| 是否开源 | 论文未提及代码仓库（unknown）；原始数据公开（OneDrive 链接见参考文献 [9]） |
| PDF | 00-inbox/Aug_inbox/2025-WWW-The_First_Early_Evidence_of_the_Use_of_Browser_Fingerprinting_for_Online_Tracking.pdf |
| MinerU Markdown | 02-parsed-markdown/2025-WWW-The_First_Early_Evidence_of_the_Use_of_Browser_Fingerprinting_for_Online_Tracking.md |

---

## 1. 一句话总结

>

本文提出 FPTrace 测量框架，通过受控 A/B 实验（真实指纹 vs 伪装指纹）观察广告竞价（Prebid.js 出价）与 HTTP 记录的变化，首次提供了浏览器指纹被广告生态用于在线跟踪与定向投放的实证证据，并发现指纹技术可能绕过 GDPR/CCPA 的退出机制。

> **与流量网站指纹（WF）的关系澄清**：本文属于**浏览器端指纹**研究——信号源是浏览器 API 暴露的属性（Navigator/Screen/Canvas/Date 等）及 HTTP 头部（User-Agent 等），测量对象是广告生态（出价、数据同步、Cookie 恢复）；与本知识库主线的**流量侧信道 WF**（信号源为网络流量时序/长度模式，攻击者为被动窃听的网络观察者）属于同一"指纹识别"主题下的不同信号源分支，方法、威胁模型与结论均不互通，仅概念上相关。

---

## 2. 摘要翻译

### 2.1 摘要原文

> While advertising has become commonplace in today's online interactions, there is a notable dearth of research investigating the extent to which browser fingerprinting is harnessed for user tracking and targeted advertising. Prior studies only measured whether fingerprinting-related scripts are being run on the websites but that in itself does not necessarily mean that fingerprinting is being used for the privacy-invasive purpose of online tracking because fingerprinting might be deployed for the defensive purposes of bot/fraud detection and user authentication. It is imperative to address the mounting concerns regarding the utilization of browser fingerprinting in the realm of online advertising.
>
> This paper introduces "FPTrace" (fingerprinting-based tracking assessment and comprehensive evaluation framework), a framework to assess fingerprinting-based user tracking by analyzing ad changes from browser fingerprinting adjustments. Using FP-Trace, we emulate user interactions, capture ad bid data, and monitor HTTP traffic. Our large-scale study reveals strong evidence of browser fingerprinting for ad tracking and targeting, shown by bid value disparities and reduced HTTP records after fingerprinting changes. We also show fingerprinting can bypass GDPR/CCPA opt-outs, enabling privacy-invasive tracking.
>
> In conclusion, our research unveils the widespread employment of browser fingerprinting in online advertising, prompting critical considerations regarding user privacy and data security within the digital advertising landscape.

### 2.2 摘要中文翻译

> 尽管广告已成为当今在线交互的常态，但关于浏览器指纹在多大程度上被用于用户跟踪和定向广告的研究却明显不足。以往研究仅测量网站是否运行了指纹相关脚本，但这本身并不必然意味着指纹被用于在线跟踪这一侵犯隐私的目的——因为指纹也可能被部署用于 bot/欺诈检测和用户认证等防御性用途。解决人们对浏览器指纹在在线广告领域被滥用的日益增长的担忧势在必行。
>
> 本文提出 FPTrace（基于指纹的跟踪评估与综合评价框架），通过分析浏览器指纹调整引发的广告变化来评估基于指纹的用户跟踪。利用 FPTrace，我们模拟用户交互、捕获广告出价数据并监控 HTTP 流量。我们的大规模研究提供了浏览器指纹被用于广告跟踪与定向的强证据，表现为指纹改变后出价价值的差异与 HTTP 记录的减少。我们还表明，指纹技术可以绕过 GDPR/CCPA 的退出（opt-out）机制，从而实施侵犯隐私的跟踪。
>
> 总之，我们的研究揭示了浏览器指纹在在线广告中的广泛使用，引发了对数字广告生态中用户隐私与数据安全的关键思考。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 广告已是网络常态，但"浏览器指纹是否真的被用于跟踪/定向投放"缺乏实证研究。
- 既有工作（Englehardt et al. CCS'16、Lerner et al. USENIX Sec'16 等）把"网站运行了指纹脚本"直接等同于"用于跟踪"——这个假设**不成立**：指纹同样广泛用于 bot/欺诈检测（Wu et al. NDSS'23 证明真实网站用指纹做反欺诈）与身份认证（Lin et al. USENIX Sec'22）。
- 已有的"个性化广告↔网络跟踪"研究（Wills et al. 对 Google/Facebook；Zeng et al. 用 header bidding 评估定向广告）聚焦 Cookie 类跟踪，未回答"浏览器指纹是否参与其中"。
- 监管实践（GDPR/CCPA）要求网站把浏览器指纹纳入隐私通知与退出控制，但缺乏审计手段验证指纹是否被合规使用。

### 3.2 现有方法的痛点和不足

| 痛点 | 说明 |
|---|---|
| 脚本存在 ≠ 用于跟踪 | 检测到指纹脚本只能证明"能力存在"，无法区分防御性（反欺诈/认证）与侵犯性（跟踪）用途 |
| 无法观察广告生态内部 | 用户端只能看到展示的广告，看不到广告商出价、数据同步等跟踪信号 |
| 缺少受控因果实验 | 观察性研究无法建立"指纹变化→广告/流量变化"的因果关系 |
| 合规验证缺位 | GDPR/CCPA 下用户退出后，没有框架验证广告商是否仍用指纹识别用户 |

### 3.3 论文的研究假设或核心直觉

- **核心直觉（因果杠杆）**：如果浏览器指纹真的参与在线跟踪，那么**改变指纹应同时改变广告出价（bid）与底层 HTTP 记录**——因为广告商的出价行为受其对用户的先验了解驱动（Olejnik et al. 证明"Only category"画像出价比"New user"高约 40%；Liu et al. 证明通过数据同步了解用户的广告商出价更高）。
- 因此通过受控 A/B 实验（真指纹 vs 伪装指纹，其余条件不变）对比出价与 HTTP 信号，即可把"指纹用于跟踪"从关联推断升级为因果证据。

### 3.4 问题发现路径

> 追溯作者如何从**现象/痛点**一步步转化为**可研究的科学问题**。

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 网站普遍部署指纹脚本，但指纹也可用于反欺诈/认证等正当目的 | §1、§2.1（引 Wu et al.、Lin et al.、DataDome/Radware/HUMAN 等） |
| 痛点提炼 | 既有测量把"脚本存在"当作"跟踪证据"，监管与学术评估缺乏区分手段 | §1 |
| 问题转化 | 转化为可检验命题：指纹变化是否导致广告出价与 HTTP 信号变化（即指纹是否参与跟踪）？→ 研究问题：browser fingerprints are indeed adopted for online tracking? | §1 |
| 文献定位 | 广告跟踪测量有先例（Wills/Zeng 的 header bidding 方法），但均未以指纹为自变量；指纹测量有先例（脚本检测），但未连到广告生态 | §1、§2.4、§8 |

### 3.5 科学假设形成

> 论文提出了什么**可验证的科学假设**？该假设如何从 3.4 的问题推导而来？

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 若指纹参与跟踪，则改变指纹会使出价统计（均值/中位数/最大值/分布）与 HTTP 记录（链数/同步事件/记录数）发生显著变化 | 出价反映广告商对用户的先验了解（§2.4） | 受控 A/B 实验（Table 2~5），同条件重复两次验证稳定性 |
| 辅助假设 A | 指纹参与 Cookie 恢复（删除 Cookie 后凭指纹重建） | Cookie 恢复机制多样（supercookie、IP、指纹） | 5 种设置（a~e）下 Cookie 导出比对 + 90 组人工检查 |
| 辅助假设 B | 即使 GDPR/CCPA 退出后，指纹仍被用于数据同步 | CMP 需保证退出后不共享非必要数据 | 4 个 CMP + NAI 的 Opt In/Opt Out 对照实验 |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | 指纹改变后出价分布显著偏离（Have Cookies：Fake FP 中位数 0.19 vs True FP 0.25/0.23，最大值 10.02 vs 5.45/5.52）；HTTP 记录降约 65%（109,802 vs 313,094/318,208） | §6.1、Table 2~5 |
| 辅助假设 A | 反驳（无结论） | 记录 378 例"与指纹相关"的恢复（90 组 key-host），但人工检查无法将恢复归因于指纹（部分值随时间变化/随机/双向矛盾） | §6.2、§A.6 |
| 辅助假设 B | 部分支撑 | GDPR：Onetrust/Quantcast/NAI 在退出后指纹改变仍引起同步事件显著变化；CCPA：Onetrust/NAI 在 Opt Out 下显著；Cookiebot/Didomi 无显著证据 | §A.5、Table 6~15 |

---

## 4. 方法设计

### 4.1 方法整体流程

FPTrace 测量分四大步（论文 Figure 1）：

1. **模拟兴趣画像（Persona）**：选定主题（"Computers"），用 Google 搜索构建 40 个网站列表 W_p，OpenWPM 依次访问并保存浏览器画像 P_p（含浏览历史与 Cookie），同时绕过 WebDriver 检测（覆盖 Navigator.webdriver）。
2. **采集出价与 HTTP 数据**：先扫描 Alexa 前 10,000 网站识别使用 Prebid.js 的站点构成 W_bids；再用画像 P_p 访问 W_bids，经 pbjs.getBidResponses() 采集所有参与者的出价对象（不只获胜者），同时记录 HTTP 链/同步事件/记录。
3. **检测 Cookie 恢复**：True 设置 S_true（全新画像）访问网站后导出 C_true；擦除历史与 Cookie 后新画像 P_0 重访导出 C_0；按 key/value/owner 精确匹配，恢复集 C_True-0 = C_0 ∩ C_true。
4. **检测与指纹相关的 Cookie 恢复**：S_1 设置中仅替换指纹（Gummy Browser 伪装），其余条件与 S_true 相同，导出 C_1；C_True-0 中在 C_1 中缺失或值改变的 Cookie 即为指纹影响证据。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1: 画像构建 | 主题关键词（Computers） | Google 搜索取前 40 站点人工去重 → OpenWPM 依次访问（模拟鼠标滚动、1~10 秒随机等待）→ 保存画像 P_p | 兴趣画像 P_p（历史+Cookie+指纹配置） | 建立"广告商已知用户"的基线身份 |
| Step 2: 出价/HTTP 采集 | P_p + W_bids 站点列表 | 用 P_p 访问 Prebid.js 站点，注入代码经 pbjs 采集全部参与者出价；记录 HTTP 链/同步事件/记录 | 出价数据集 + HTTP 数据 | 主因变量测量（对比 A/A*/B 设置） |
| Step 3: Cookie 恢复检测 | 浏览器画像 | S_true（新画像→C_true）、S_0（擦除后新画像 P_0→C_0），按 key/value/owner 匹配 | 恢复 Cookie 集 C_True-0 | 排除指纹因素后的恢复基线 |
| Step 4: 指纹相关恢复检测 | C_True-0 + C_1 | S_1 仅改指纹（Gummy 伪装扩展 + 新画像），重访同网站导出 C_1，与 C_True-0 对比 | 缺失/值变 Cookie 清单（90 组 key-host） | 判定指纹是否参与 Cookie 恢复 |
| Step 5（附录）: 法规实验 | CMP（Cookiebot/Quantcast/Onetrust/Didomi）+ NAI | AWS 法兰克福（GDPR）/加州（CCPA）部署；6 种设置 × Opt In/Opt Out 自动交互（DOM 操作点击拒绝/同意） | 各 CMP 的 HTTP 链/同步/记录对照表 | 验证退出后指纹是否仍被用于数据同步 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| 爬虫内核（OpenWPM + Selenium/Firefox） | 自动化访问、画像保存/加载、HTTP 记录 | 网站列表、画像 | 画像、HTTP 数据 | 框架底座；承载其余模块 |
| 出价采集器（Prebid.js 注入） | 经 pbjs API 捕获所有广告商出价（含获胜者、广告 HTML） | Prebid.js 站点页面 | bid 对象集合 | 产出主因变量（Step 2/3） |
| 指纹伪装扩展（Gummy Browser 脚本注入） | 覆盖全部 JS 指纹 API（Navigator/Screen/Canvas.getContext/Date 等），值来自真实设备指纹数据集（FPStalker GitHub） | 真实指纹数据 | 伪装指纹 | 构造 B 设置的自变量；扩展封装保证页面加载前生效 |
| HTTP 头伪装（ModHeader 嵌入 Selenium） | 修改 HTTP 头（UA 等）与 JS API 值保持一致 | 目标头部值 | 伪装 HTTP 头部 | 防止"JS 值 vs 头部值"不一致被识破 |
| Cookie 导出器 | 导出全部一/三方 Cookie | 浏览器配置文件 | Cookie 集（C_true/C_0/C_1） | 支撑 Cookie 恢复分析 |
| 法规实验控制器 | 自动识别并操作 CMP 同意面板（DOM 查找/点击拒绝） | CMP 页面 | Opt In/Opt Out 后的 HTTP 数据 | 支撑 GDPR/CCPA 实验 |

### 4.4 公式、算法和机制解释

- **A/B 实验设计（因果识别）**：设置 a~e（Table 1）在"新画像？/有 Cookie？/真指纹？/真 IP？"四维上受控变化——本实验全部用真 IP，关键对比为 b vs c（有 Cookie：真指纹 vs 伪指纹）与 d vs e（无 Cookie：真指纹 vs 伪指纹）；同一设置重复两次（True FP True IP 与 True FP True IP 2）验证数据稳定性。
- **出价数据**：取所有参与者出价（不只获胜者），统计 Avg/Std/Median/Min/Max，并绘 CDF（仅展示 CDF>0.8 区段，因为 0.8 以下所有出价均 <1 无区分度）。
- **HTTP 信号**：链（chains）按 HTTP 记录构建的请求链；同步事件（syncing）为含数据共享的链；记录数（records）为总 HTTP 记录数。
- **Cookie 恢复匹配**：按 Cookie 的 key、value、owner 三者精确匹配判定恢复；指纹相关判定为 C_True-0 ∩ C_1 的差集（缺失或值变）。
- **指纹伪装机制**：Gummy Browser 三种攻击方式之一"脚本注入"——在 toDataURL() 等调用处打断点替换返回值为预定义/随机字符串；值来源为 GitHub 真实设备指纹数据集（Spirals-Team/FPStalker）；伪装范围覆盖 Navigator（UA、语言）、Screen、Canvas、Date 等 JS API，并用 ModHeader 同步修改 HTTP 头（如 UA）。
- **法规实验设置**：每 CMP/地点组合 6 种设置（0 新画像真指纹；1 训练画像真指纹有 Cookie 基线；2 训练画像伪指纹有 Cookie；3 同 1 重复；4 训练画像伪指纹无 Cookie；5 训练画像真指纹无 Cookie），全部自动完成 CMP 面板交互（Cookiebot 按钮 ID、Quantcast 类名、OneTrust 的 RejectAll API、Didomi 的 setUserDisagreeToAll API）。

### 4.5 方法优势

- **因果而非关联**：以指纹为唯一自变量的受控 A/B 实验 + 同设置重复验证，把"指纹参与跟踪"从推测变为可检验命题。
- **可观测的多维信号**：出价（经济信号）+ HTTP（网络信号）+ Cookie（持久化信号）三通道互证，且出价数据来自客户端可直读的 header bidding（Prebid.js），无需依赖广告商配合。
- **法规缺口量化**：首次在 GDPR/CCPA 真实合规环境（法兰克福/加州 AWS）下系统测量退出后指纹使用情况，覆盖 4 大主流 CMP + NAI。
- **诚实的方法边界**：对 Cookie 恢复这一无法得出结论的环节做了完整记录与人工检查（90 组），并明确声明结论为"无法证实"。

### 4.6 方法不足

- **单一平台**：全部实验在 Linux 上完成，Windows/macOS/移动端结论未知（伪指纹数据虽取自真实 Windows/macOS/移动设备，但真指纹设置未覆盖）。
- **bot 检测不确定性**：尽管绕过了 Navigator.webdriver 并模拟人类行为（鼠标滚动、1~10 秒随机等待），无法排除网站有未公开的爬虫检测手段，若访问被判定为 bot 则结果失真。
- **无广告商审计框架**：无法在法规约束内评估广告商行为；对"退出后能否继续跟踪"只能给出不确定性结论。
- **Cookie 恢复无结论**：指纹相关恢复（378 例/90 组）经人工检查后无法归因（值随时间变化、随机源、同指纹不同值/不同指纹同值等矛盾现象并存）。
- **法规实验样本与统计口径有限**：每 CMP 的差异判断基于少量设置的对照，未见显著性检验。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

- 与"指纹脚本检测"类研究（Englehardt/Lerner/FPDetective 系）本质不同：后者以"脚本是否出现"为证据，本文以"**指纹改变→广告/HTTP 信号改变**"的因果关系为证据，可区分防御性（反欺诈/认证）与侵犯性（跟踪）用途。
- 与"广告跟踪测量"类研究（Wills et al. 的 Google/Facebook 平台内观察、Zeng et al. 的 286 人/10 站字段实验）本质不同：前者以 Cookie/行为为自变量，本文首次以**浏览器指纹为自变量**。
- 与 Liu et al. PETS'24（同组前作）的区别：前作评估 CMP/网站/广告商是否遵守用户同意选择，**不涉及指纹配置**；本文聚焦指纹设置并评估法规对指纹技术的约束力。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| FPTrace 框架 | OpenWPM + Prebid.js 出价采集 + Gummy Browser 伪装 + ModHeader 头部伪装的一体化测量框架 | 高 | 是（可复用于任意"指纹→生态行为"测量） |
| 因果证据范式 | 受控 A/B + 同条件重复验证，证明指纹参与广告跟踪/定向 | 高 | 是（测量学范式，可迁移） |
| 法规环境测量 | GDPR/CCPA 下 4 CMP + NAI 的退出后指纹使用测量 | 中 | 是（方法论可扩展到其他法规/区域） |
| 诚实报告 Cookie 恢复 | 90 组 key-host 人工检查并给出"无法证实"结论 | 中 | 是（负面结果报告范式） |

### 5.3 适用场景

- **监管合规审计**：为 GDPR/CCPA/未来法规提供"退出后是否仍被指纹跟踪"的测量工具。
- **广告生态透明度研究**：研究出价与用户画像（指纹/Cookie/IP）的关系；header bidding 数据直读特性使其适用于大规模测量。
- **反指纹与隐私工具评估**：验证伪装工具（如 Gummy Browser）在真实生态中的效果与可探测性。
- **cookie 生态研究**：Cookie 恢复机制（supercookie/IP/指纹）的区分测量。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 指纹脚本检测（FPDetective、Englehardt、Lerner） | 规模大、成本低 | 无法区分防御/侵犯用途 | 以出价+HTTP 因果信号替代脚本存在性 |
| 广告平台内观察（Wills et al.） | 直接观察广告 | 仅限 Google/Facebook 平台；无因果变量 | 用 header bidding 覆盖开放生态 |
| 出价字段实验（Zeng et al.） | 控制变量 | 以 Cookie/行为为变量，未涉及指纹 | 首次把指纹作为自变量 |
| 指纹伪装（Gummy Browser、FPStalker） | 成熟的伪装能力 | 仅工具，未连接生态后果 | 接入 A/B 实验框架测量生态响应 |
| CMP 合规研究（Liu et al. PETS'24） | 评估同意机制合规 | 不涉及指纹配置 | 专门测量指纹在法规下的使用 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **画像构建**：Google 搜索"Computers"主题取前 40 站点（人工去重，列表见 Appendix A.1）；绕过 WebDriver 检测（覆盖 Navigator.webdriver）；模拟鼠标滚动 + 1~10 秒随机等待。
- **测试站点**：27 个使用 Prebid.js 的网站（Appendix A.2，含 tribunnews、nytimes、theguardian、espn、cnet 等）。
- **5 种设置（Table 1）**：a 新画像/无 Cookie/真指纹/真 IP；b 有 Cookie/真指纹/真 IP；c 有 Cookie/伪指纹/真 IP；d 无 Cookie/真指纹/真 IP；e 无 Cookie/伪指纹/真 IP。关键对比：b↔c（有 Cookie）与 d↔e（无 Cookie）；b 与 d 重复两次（True FP True IP / True FP True IP 2）验证稳定性。
- **地点**：美国本土（无隐私法规，主实验）；AWS 法兰克福（GDPR）；AWS 加州（CCPA）。
- **法规实验**：4 个 CMP（Cookiebot、Quantcast、Onetrust、Didomi）+ 中央退出平台 NAI；每 CMP×地点 6 种设置 × Opt In/Opt Out；全部自动交互。

### 6.2 数据集

- 自建数据（论文未给出精确访问次数/时长；原始数据公开于 OneDrive，参考文献 [9]）：
  - 出价数据：Table 2（有 Cookie）、Table 4（无 Cookie），含 Avg/Std/Median/Min/Max。
  - HTTP 数据：Table 3（有 Cookie）、Table 5（无 Cookie），含 Chains/Syncing/Records。
  - Cookie 数据：90 组 key-host（如 google.it 的 OTZ，UA 为 chrome 与 firefox 时值不同）。
  - 法规数据：Table 6~15（各 CMP × 法规 × Opt In/Out × 6 设置的 HTTP 链/同步/记录）。

### 6.3 Baseline

- 自身重复对照：同一设置运行两次（True FP True IP vs True FP True IP 2）作为稳定性基线；无外部第三方基线（该测量问题无既有方法）。

### 6.4 评价指标

- 出价统计量（Avg/Std/Median/Min/Max）+ CDF 分布对比；HTTP 链数/同步事件数/记录总数；Cookie 恢复匹配数（key/value/owner 精确匹配）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---|---|---:|---:|---:|---|
| 有 Cookie 出价 | Median | Fake FP 0.19 vs True FP 0.25 / 0.23 | — | — | 中位数下降、最大值大幅上升（10.02 vs 5.45/5.52），指纹改变影响出价 |
| 有 Cookie HTTP | Records | Fake FP 109,802 vs True FP 313,094 / 318,208 | — | — | 记录数减少近 65%；Chains 6,345 vs 36,446/37,929；Syncing 减少约 50%（421 vs 888/895） |
| 无 Cookie 出价 | Median/Max | Fake FP 0.13/5.92 vs True FP 0.19/5.80（True FP 2 保持 Cookie：0.17/2.13） | — | — | 中位数下降、均值与最大值上升 |
| 无 Cookie HTTP | Records | Fake FP (CR) 119,673 vs True FP (CR) 124,543；True FP 2 128,781 | — | — | 删 Cookie 后 Chains 降约 13%，改指纹再降约 2%；总记录持续下降 |
| Cookie 恢复 | 恢复实例 | 90 组 key-host、378 例与指纹相关的恢复 | — | — | 人工检查后**无法证实**指纹参与 Cookie 恢复 |
| GDPR | Syncing | Onetrust/Quantcast/NAI 在伪指纹下同步事件显著增加（如 NAI Opt Out：设置 2 的 syncing 132 vs 基线 27） | — | — | Cookiebot/Didomi 无显著证据；Onetrust 在 Opt In 下无证据 |
| CCPA | Syncing/Chains | Onetrust（Opt Out 设置 2 vs 1/3 显著差异：2,216 vs 724/1,588 Chains）、NAI（Opt Out 设置 2 vs 1/3 显著差异：1,985 vs 600/744 Chains） | — | — | Cookiebot/Didomi/Quantcast 无显著差异 |

### 6.6 优势最明显的场景

- **有 Cookie 场景**：指纹变化对 HTTP 记录的打击最明显（-65%），且两次 True FP 重复高度一致（313,094 vs 318,208），因果信号最强。
- **法规 Opt Out 场景**：GDPR 下 Onetrust（Fake FP + No Cookies 组合）与 NAI、Quantcast 的同步事件显著变化——证明退出后指纹仍可能被用于数据同步，是论文最具政策冲击力的发现。

### 6.7 局限性

- Linux 单平台；爬虫被识破的不确定性；无法评估法规约束下的广告商行为；Cookie 恢复结论不成立；法规实验缺统计检验；设置 c 同时改了"IP 与指纹"的描述与 Table 1 标注（"不同 IP"）存在文本与表格的不一致（论文正文 §5.2 场景 c 称"fake fingerprints and fake IP"，而 Table 1 标注 True IP，需以原文核对）。

---

## 7. 学习与应用

### 7.1 是否开源？

- **代码**：论文未提及代码仓库（unknown）。
- **数据**：原始数据公开（OneDrive：tamucs-my.sharepoint.com，参考文献 [9]）。

### 7.2 复现关键步骤

1. 搭建 OpenWPM（Selenium + Firefox）爬虫，注入 Prebid.js 出价采集代码（pbjs.getBidResponses()）与 Cookie 全量导出功能。
2. 构建指纹伪装扩展：用 Gummy Browser 脚本注入覆盖 Navigator/Screen/Canvas/Date 等 API，值取 GitHub 真实指纹数据集（Spirals-Team/FPStalker）；嵌入 ModHeader 同步修改 HTTP 头。
3. 构建兴趣画像：Google 搜索取 40 站点，OpenWPM 模拟人类行为（滚动 + 1~10 秒随机等待）访问并保存画像；绕过 Navigator.webdriver。
4. 按 Table 1 的 5 种设置运行 A/B 实验（同一设置重复两次），采集出价与 HTTP 数据；对比统计量与 CDF。
5. Cookie 恢复实验按 S_true/S_0/S_1 三步对比；法规实验在法兰克福/加州部署，自动操作 CMP 面板。

### 7.3 关键超参数、预处理和训练细节

- 无模型训练；关键参数：Google 搜索取前 40 站点（人工去重）；Alexa top 10,000 检测 Prebid.js；随机等待 1~10 秒；Cookie 匹配键为 key/value/owner 三者精确相等；CDF 只展示 >0.8 区段（因低段出价均 <1 无区分度）。
- 伪装一致性要求：JS API 值（Navigator UA/语言等）与 HTTP 头（ModHeader）必须同步修改，防止被匹配检测。
- CMP 交互自动化：Cookiebot 用按钮 ID CybotCookiebotDialogBody-ButtonDecline；Quantcast 用 qc-cmp2-summary-buttons 类名找 Reject；OneTrust 用 window.OneTrust.RejectAll；Didomi 用 Didomi.setUserDisagreeToAll。

### 7.4 能否迁移到其他任务？

- **测量方法学**："改变信号源 → 观测生态响应"的因果实验范式可迁移到任何"用户属性→广告/内容定制"问题（如 IP、时区、语言、硬件指纹）。
- **合规审计工具**：FPTrace 可直接扩展为 GDPR/CCPA/其他法规的持续合规监测工具。
- **对流量领域（本知识库语境）**：其"伪装一致性"问题与流量侧 WF 的对抗防御相通——指纹伪装需保持 JS 与 HTTP 头一致，类似地，流量伪装需保持时序/长度/协议一致性；但其信号与结论不适用于流量 WF 攻防。

### 7.5 对我的研究有什么启发？

- **测量设计的因果纪律**：用"改变自变量→观测下游信号"代替"检测特征存在"，是提升测量研究可信度的通用模板（同设置重复运行两次验证稳定性尤其值得借鉴）。
- **负面结果的处理**：Cookie 恢复无结论一段（90 组人工检查、矛盾现象并列）展示了如何诚实地报告"无法证实"——比选择性呈现更有方法论价值。
- **与流量 WF 的交叉点**：浏览器指纹（HTTP 头部、JS API）与网络流量同属"用户可观察侧信道"；广告商若以 UA 等头部做指纹，则网络侧被动观测者也可能利用相同信号——这为流量 WF 的"应用层特征"研究（如本知识库 HOLMES & WATSON 的 HTTP 版本特征）提供了生态动机层面的旁证。

---

## 8. 总结

### 8.1 核心思想

> 改指纹，看出价——广告商是否认识你。

### 8.2 速记版 Pipeline

1. 构建兴趣画像（40 站点 + 人类行为模拟 + 绕过 WebDriver）。
2. 伪装扩展（Gummy Browser 注入 + ModHeader 头部同步）构造真/伪指纹对照。
3. Prebid.js 采集全部出价 + HTTP 链/同步/记录（同一设置跑两遍）。
4. Cookie 导出三对比（S_true / S_0 / S_1）检测恢复。
5. GDPR/CCPA 地点 × 4 CMP + NAI 的 Opt In/Out 对照测量。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[website-fingerprinting]] —— 注意：本文是**浏览器端指纹**（信号源：浏览器 API 属性 + HTTP 头部；用途：广告跟踪），与本库流量侧信道 WF（信号源：网络流量；用途：站点识别攻击）同属"指纹"主题但信号源、威胁模型完全不同，仅概念相关。

（其余概念页均为网络流量域，与本文无关，不链接。）

### 9.2 相关方法

- 无合适页面：本文方法（OpenWPM 爬虫、Prebid.js 出价采集、Gummy Browser 伪装、A/B 测量）不在本库方法页允许列表内（transformer、graph-neural-network 等均为流量/深度学习域），不链接。

### 9.3 相关任务

- [[website-fingerprinting]] —— 任务层面仅作主题关联：本文任务是"在线跟踪的因果测量"而非流量 WF 分类任务，链接仅用于知识库内横向对照（浏览器端 vs 流量端）。

### 9.4 可更新的综述页面

- [[survey-website-fingerprinting]] —— 若该综述覆盖浏览器端指纹测量分支，本文可作为"指纹用于广告跟踪的因果证据"引用材料；否则仅作主题关联。

### 9.5 可加入的对比表

- 无合适页面：[[dataset-comparison-table]] 收录流量数据集，本文为广告测量数据（出价/HTTP/Cookie），不适用；[[open-source-registry]] 面向代码仓库，本文代码状态 unknown，暂不加入。

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 有 Cookie 时指纹改变使出价分布显著偏离（Fake FP median 0.19 vs True FP 0.25/0.23；max 10.02 vs 5.45/5.52） | Table 2 | §6.1.1 |
| 有 Cookie 时指纹改变使 HTTP 记录减少近 65%（109,802 vs 313,094/318,208），同步事件减少约 50% | Table 3 | §6.1.1 |
| 无 Cookie 时指纹改变使中位数下降、均值与最大值上升 | Table 4 | §6.1.2 |
| 删除 Cookie 后 HTTP 链数降约 13%，改指纹再降约 2% | Table 5 | §6.1.2 |
| 检测到 90 组 key-host、378 例指纹相关 Cookie 恢复，但人工检查无法归因 | §6.2、§A.6 | §6.2 |
| 指纹伪装覆盖 Navigator/Screen/Canvas/Date 等 API，值来自 GitHub 真实设备数据集（FPStalker） | §3.2.2 | §3.2.2 |
| JS 值与 HTTP 头必须同步伪装（ModHeader），否则会被匹配检测 | §3.2.2 | §3.2.2 |
| GDPR：Onetrust/Quantcast/NAI 在退出后指纹改变仍引起同步事件显著变化 | §A.5、Table 7/13/15 | §A.5 |
| CCPA：Onetrust/NAI 在 Opt Out 下设置 2 与设置 1/3 显著差异 | §A.5、Table 6/14 | §A.5 |
| 全部实验在 Linux 上完成；无法排除爬虫被识破 | §7 | §7 |
| 原始数据公开（OneDrive 链接） | 参考文献 [9] | §6 开篇 |
| 设置 c 的"不同 IP"描述与 Table 1 的 True IP 标注不一致 | §5.2 vs Table 1 | §5.2 |

---

## 11. 原始资料链接

- PDF：00-inbox/Aug_inbox/2025-WWW-The_First_Early_Evidence_of_the_Use_of_Browser_Fingerprinting_for_Online_Tracking.pdf
- MinerU Markdown：02-parsed-markdown/2025-WWW-The_First_Early_Evidence_of_the_Use_of_Browser_Fingerprinting_for_Online_Tracking.md

---

## 12. 后续问题

- 设置 c（Table 1）标注 True IP，但正文 §5.2 描述"fake IP"——哪个正确？需查原文核对。
- 法规实验的差异判断（"显著"）基于什么统计标准？论文未给出显著性检验。
- Cookie 恢复的 378 例中，指纹相关但"值变化"的 Cookie 是否可能只是 UA 依赖的正常值（如 google.it 的 OTZ）？
- FPTrace 的访问规模（多少站点 × 多少轮）论文未明确给出，附录仅列出 40+27 个站点。
- 广告商能否用"指纹+IP"之外的联合信号（如浏览器扩展、TLS 指纹）识别伪装？本文未覆盖。
- 若爬虫被识别，出价/HTTP 差异是否会被放大？作者列为不确定性来源，但未量化。

---

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

> 论文从"广告无处不在但指纹是否被用于跟踪缺乏实证"的张力出发，先推翻一个流行假设——脚本存在不等于跟踪（指纹也用于反欺诈/认证）——从而制造出"既有测量方法无效"的缺口。随后用一个可检验的因果杠杆（改变指纹→观察出价与 HTTP 信号变化）搭建 FPTrace 测量框架，给出强正面证据（出价偏离、HTTP 记录降 65%），再用"法规环境"实验把结论推向政策层面（退出后仍可能被跟踪），最后在 Cookie 恢复环节诚实收尾（无法证实），使整体叙事"强证据 + 克制的结论"形成可信闭环。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract | 摘要式承诺 | 直接给出核心证据（bid 差异 + HTTP 记录减少）与法规突破（绕过 GDPR/CCPA） | 无 |
| Introduction | 推翻假设、建立缺口 | 指出"脚本存在=跟踪"不成立（反欺诈/认证用例），锁定研究问题 | 把测量问题从"检测脚本"转为"验证因果" |
| Background | 概念铺垫 | 指纹技术、伪装（Gummy Browser）、Cookie 恢复、header bidding、法规五节为方法章提供工具与理论支撑 | 用 Olejnik/Liu 的出价先验知识论证"出价是有效的跟踪信号" |
| Method（FPTrace） | 工具构建 | 三步框架 + 四类组件（爬虫/出价/伪装/Cookie），强调开源组件复用与扩展 | 把 Gummy Browser 从攻击工具转化为测量探针 |
| Methodology | 测量设计 | 画像构建、5 种设置、Cookie 三设置、法规配置 | 受控 A/B + 重复验证确立因果识别 |
| Results | 证据呈现 | 出价/HTTP 主证据 → Cookie 恢复负面结果 → 法规证据（附录） | Cookie 恢复"无法证实"是叙事诚实性的支点 |
| Discussion & Limitations | 边界划清 | Linux 单平台、bot 不确定性、法规审计缺位 | 承认不确定性但坚持主结论 |
| Related Work | 差异化定位 | 与脚本检测、广告测量、CMP 合规三线对照 | 强调"指纹为自变量"的首次性 |
| Conclusion | 收束 | 框架 + 证据 + 政策启示 | 无 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 评估不足 | 既有研究只测脚本存在性，无法区分防御/侵犯用途 | 矛盾证据（反欺诈/认证的真实用例 vs 隐私担忧） | §1、§2.1 |
| 场景缺失 | 广告跟踪研究只覆盖 Cookie 类跟踪，未触及指纹 | 文献对比（Wills/Zeng 的方法均不涉及指纹） | §1、§2.4 |
| 理论缺陷 | "脚本存在=跟踪"的隐含假设不成立 | 反例论证（DataDome/Radware/HUMAN 用指纹反欺诈；Lin et al. 用指纹做认证） | §1 |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 主实验（出价+HTTP，§6.1） | 对比碾压式呈现：Fake vs True 的数字鸿沟（-65% 记录、出价分布偏离），同设置重复验证稳定性 | 直接支撑核心假设，是全文证据主轴 |
| Cookie 恢复（§6.2） | 负面结果深描：90 组人工检查 + 矛盾现象并列，结论"无法证实" | 与主证据形成"强证据/克制结论"的反差，增强可信度 |
| 法规实验（附录 A.5） | 场景扩展：把证据从无法规地区推广到 GDPR/CCPA 环境 | 将科学结论升格为政策关切 |
| 可视化（Figure 4 CDF） | 分布级证据：两条 True FP 曲线接近、Fake FP 曲线显著偏离 | 用图形强化"指纹是唯一自变量"的因果印象 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 开篇方式 | 先承认广告的普遍性，再指出"缺乏研究"的缺口，最后用一句话推翻流行假设制造张力 | "普遍现象 + 假设批判"式开篇 |
| Gap 提出方式 | 用真实反例（反欺诈/认证）证明旧假设不成立，从而论证新测量方法必要 | 用反例而非引文堆砌建立研究缺口 |
| 方法论证逻辑 | 每个模块说明"开源组件 + 自研扩展"（OpenWPM+注入、Gummy+ModHeader），强调可复现 | "复用 + 增量扩展"的方法写作模板 |
| 实验组织逻辑 | 主实验在前（因果证据），负面实验并置（诚实报告），法规实验入附录（政策补充） | 证据强弱分层组织：强证据正文、弱/负证据不隐藏、扩展实验附录 |
| 局限性讨论方式 | 逐条列出不确定性（平台/bot/审计缺位），但每条都说明"为何不影响主结论" | "承认边界 + 锚定主结论"的局限写作 |
| 最值得借鉴的一句话/一段结构 | Takeaway 框（每节末尾 1~2 条加粗结论）——把长段落压缩为可引用要点 | 用 Takeaway 框在每个结果小节末尾固化核心发现 |

**MinerU 解析质量问题（本笔记引用时已做修正）**：整体解析质量良好，无乱码或大段缺漏；仅存在轻微的 LaTeX 间距碎片（如 `$P _ { \boldsymbol { p } }$`、`S _ { t r u e }$`）与个别明显为原文本身的拼写变体（如 "diferent"、"eficient"），不影响信息读取；Table 1~15 均完整解析。正文 §5.2 与 Table 1 关于设置 c 的 IP 标注不一致为原文问题（已在 §6.7、§10、§12 标注待核）。

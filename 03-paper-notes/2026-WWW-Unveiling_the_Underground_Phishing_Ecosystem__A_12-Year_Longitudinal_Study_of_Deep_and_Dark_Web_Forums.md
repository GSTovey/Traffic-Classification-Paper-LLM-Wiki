---
type: paper
title_original: "Unveiling the Underground Phishing Ecosystem: A 12-Year Longitudinal Study of Deep and Dark Web Forums"
title_cn: "揭示地下钓鱼生态：深网与暗网论坛的十二年纵向研究"
authors: ["Dohee Kim", "Hui Zhao", "Doowon Kim", "Sungjae Hwang"]
year: 2026
venue: "ACM Web Conference 2026 (WWW'26)"
doi: unknown
url: "https://doi.org/10.1145/3774904.3792737"
pdf: "00-inbox/PDFs/2026-WWW-Unveiling_the_Underground_Phishing_Ecosystem__A_12-Year_Longitudinal_Study_of_Deep_and_Dark_Web_Forums.pdf"
mineru_md: "02-parsed-markdown/2026-WWW-Unveiling_the_Underground_Phishing_Ecosystem__A_12-Year_Longitudinal_Study_of_Deep_and_Dark_Web_Forums.md"
status: deep-analyzed
reading_level: L3
research_area: ["phishing ecosystem", "dark-web measurement", "longitudinal cybercrime analysis"]
task: ["phishing-post identification", "product/target/price extraction", "supply-chain mapping", "temporal/economic analysis"]
method: ["ACHE text crawling", "GPT-4o-mini extraction", "manual normalization", "seven-stage lifecycle mapping"]
dataset: ["394,034 posts (343,334 unique)", "13 English D2Web forums", "April 2013-August 2025", "70,055 phishing-related posts"]
code: "unknown (prompts disclosed in Appendix A.2; raw dataset/code availability not stated)"
relevance: medium
created: "2026-09-29"
updated: "2026-10-10"
---

# Unveiling the Underground Phishing Ecosystem: A 12-Year Longitudinal Study of Deep and Dark Web Forums

> **L3 深度分析笔记**：基于正文 §1–§7、Tables 1–4、Figures 1–8、Appendix A.1–A.3 与伦理说明交叉核对。结果描述的是公开可访问英语论坛中的发帖供给与提及趋势，不等同于真实成交、攻击执行或整个地下市场的占比。

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | Unveiling the Underground Phishing Ecosystem: A 12-Year Longitudinal Study of Deep and Dark Web Forums |
| 中文标题 | 揭示地下钓鱼生态：深网与暗网论坛的十二年纵向研究 |
| 作者 | Dohee Kim、Hui Zhao、Doowon Kim、Sungjae Hwang |
| 年份 | 2026 |
| 会议/期刊 | ACM Web Conference 2026 (WWW'26) |
| 研究方向 | 地下钓鱼生态、攻击供应链、D2Web 纵向测量 |
| 任务类型 | 钓鱼相关帖子识别、产品/目标/价格抽取、生命周期映射、时序/经济结构分析 |
| 方法关键词 | ACHE crawler、GPT-4o-mini、Role-Play/Specificity/Few-shot prompting、人工归一化、七阶段框架 |
| 数据集 | 13 个英语 D2Web 论坛，2013-04 至 2025-08；394,034 帖，去重 343,334；70,055 钓鱼相关 |
| 是否开源 | unknown；附录公布提示词，未说明原始数据/代码公开位置 |
| DOI | 10.1145/3774904.3792737 |
| PDF | 00-inbox/PDFs/2026-WWW-Unveiling_the_Underground_Phishing_Ecosystem__A_12-Year_Longitudinal_Study_of_Deep_and_Dark_Web_Forums.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-WWW-Unveiling_the_Underground_Phishing_Ecosystem__A_12-Year_Longitudinal_Study_of_Deep_and_Dark_Web_Forums.md |

## 1. 一句话总结
> 论文用 GPT-4o-mini 与人工归一化分析 13 个英语深/暗网论坛的 12 年文本，识别 70,055 条钓鱼相关帖子、39 类产品并映射到七阶段供应链，发现帖子主要集中于目标名单、基础设施与验证环节，且高质量钓鱼页面/多功能恶意软件价格更高。

## 2. 摘要原文
Phishing is a threat in which attackers masquerade as legitimate entities to steal sensitive data. While understanding the phishing ecosystem is critical for developing efective countermeasures, prior research has largely studied phishing through post-attack data, with limited examination of the attacker’s perspective and how phishing campaigns are built. Critically, the Deep and Dark Web (D2Web) serves as the primary marketplace and knowledge-sharing platform where attackers acquire phishing tools (e.g., phishing kits), exchange techniques, and trade compromised credentials. Analyz ing D2Web forums therefore provides unique visibility into the supply chain of phishing attacks pre-deployment, enabling proac tive understanding of emerging threats and attack methodologies. This study addresses this gap through a comprehensive analysis of 394,034 posts (343,334 unique) collected from 13 D2Web forums spanning 2013 to 2025, from which 70,055 phishing-related posts are identified. We employ a LLM-based approach to eficiently ex tract key information, including phishing attack components (e.g., credentials, phishing pages, SMTP servers), targeted services (e.g., PayPal, Netflix), and component authors. This extracted data is mapped to a seven-stage attack scenario framework derived from empirical case studies. Our analysis reveals longitudinal trends in component availability, target service distribution, post type evolution, and the most active contributors annually, while characterizing pricing dynamics across diferent attack components. The results provide the first attacker-centric, macro-level longitudi nal analysis of the phishing ecosystem, ofering insights into how phishing infrastructure and markets have evolved over more than a decade. These findings contribute to a deeper understanding of the phishing supply chain and inform more efective detection and prevention strategies.

## 3. 方法分析

### 3.1 研究问题

RQ1：地下市场提供哪些钓鱼组件、如何用于攻击；RQ2：组件和目标服务的时间分布如何变化；RQ3：不同产品的价格结构如何形成。作者认为既有钓鱼研究多依赖攻击后的网站、URL 和受害者数据，而论坛帖能提供部署前的供应链视角。

### 3.2 输入—处理—输出

| 阶段 | 输入 | 处理 | 输出 |
|---|---|---|---|
| 论坛选择 | FreshOnion 475 域 + 28 情报公司 379 报告/88 论坛 | 合并去重得 556 候选；排除不可达、登录/付费、非英语、关闭和非钓鱼论坛 | 13 个目标论坛 |
| 文本采集 | 13 论坛页面 | ACHE 只抓文本 HTML，提取 title/content/time/author；按标题+正文精确去重 | 394,034 帖→343,334 unique |
| 钓鱼识别 | 唯一帖子 | GPT-4o-mini，以 security analyst role 和结构化规则分类；可合理用于钓鱼即标 1 | 70,055 phishing-related posts |
| 产品抽取 | 钓鱼帖子 | D2Web-user role + specificity + few-shot，抽 name/price/features/target_service | 多产品 JSON |
| 人工归一化 | 产品名/服务名变体 | 同义词和最小 token 合并；两研究者核验 | 1,203 名称→910 distinct products；11,889 targets→5,460 |
| 生命周期映射 | 910 产品 + 30 真实案例 | 两研究者映射至七阶段；分歧讨论解决 | 39 产品类别、时序/目标/作者/价格分析 |

## 4. 实验表现

### 4.1 LLM 质量验证

两名安全研究者人工核验 100 条随机帖子分类和 100 条钓鱼帖产品抽取。分类 P/R/F1=0.97/0.84/0.90；产品名抽取 0.89/0.88/0.89；服务名抽取 0.94/0.83/0.88。多产品抽取的 TP/FP/FN 按“至少一个正确 product/target”计算，因此不代表每个产品字段完全准确。

### 4.2 关键发现

| 发现 | 数值/方向 | 证据 |
|---|---|---|
| 组件覆盖 | 58,955 帖含至少一个 39 类产品，约覆盖所有提供产品的钓鱼相关帖 90% | §4.1 |
| 阶段分布 | Step1 target list 62,853（73.45%）；Step6 verification 12,273（14.34%）；Step4 infrastructure 8,670（10.13%） | Table 3 |
| 时间趋势 | 2016、2020、2023 三次同比 >50% 的发帖激增 | Fig. 5 |
| 产品演化 | Credential/Account Checker 占主导；2024 起 Stealer 超过 Capture Tool | §4.2 |
| 目标服务 | Step2 中约 45% financial services；Step3 约 20% financial，其他多为大用户平台 | Fig. 6 |
| 作者集中度 | Step2 前10作者贡献43%，top1 12.44%；Step1/Step6 前10为15.55%/6.22% | Table 4 |
| 价格 | 多平台恶意软件示例 $3,500–$10,000；高质量钓鱼页面/多功能工具较贵 | §4.3, Fig. 8 |
| 免费供给 | 多数产品免费，作者观察到免费工具可互补组成七阶段链；hacking-for-hire等有例外 | §4.3 |

## 5. 局限性与复现建议
- 只覆盖 13 个英语可访问论坛；俄语/中文、付费、登录受限、关闭和不可达论坛被排除，存在明显可见性偏差。
- LLM 幻觉和抽取遗漏仍存在；200 样本人工验证只给任务级 F1，无法保证 343K 全量每个字段准确。
- “可用于钓鱼就标1”的宽规则会纳入双用途基础设施；发帖量不是成交量、攻击频次或攻击成功率。
- 七阶段来自 30 案例，是归纳框架，不保证覆盖所有钓鱼变体；单帖可映射多个阶段，Table3 总和不能当独立帖子数。
- 伦理上仅收集论坛文本，不下载帖子链接中的凭据/PII、媒体或压缩包，不交易/付费、不去匿名化作者。
- 复现应固定论坛候选/排除记录、抓取时间、精确去重规则、GPT-4o-mini 版本/提示词和人工归一化映射，保持原始文本与派生标签分离。

## 6. 知识链接
- 该论文为地下市场文本测量，不直接属于 traffic-classification 或 encrypted-traffic-analysis；暂不建立误导性主知识层链接。

## 7. 证据状态
- 正文证据已核对至 §1–§7、Tables1–4、Figures1–8、AppendixA.1–A.3。
- DOI 为 10.1145/3774904.3792737；原始数据与代码公开状态未说明，记为 unknown。
- 作者名称在报告中掩码；统计只反映论坛供给/讨论，不能直接证明商品有效性、真实交易或攻击归因。



## 8. 详细方法与机制

### 8.1 数据采集与可见性

候选论坛来自 FreshOnion 的 475 个 onion 域和 28 家情报公司的 379 份报告；合并后 556 个候选，经过不可达、非英语、登录/付费、关闭和非钓鱼主题排除，保留 13 个论坛。ACHE crawler 只提取 HTML 中的标题、正文、时间和作者字段，不下载帖子内文件、凭据、PII、图片、视频或压缩包。初始抓取 394,034 帖，按标题和正文精确去重为 343,334 条，覆盖 2013 年 4 月至 2025 年 8 月。

### 8.2 LLM 分类与抽取

GPT-4o-mini 先用 security-analyst role 和严格 JSON prompt 判断帖子是否直接或间接可用于钓鱼；边界帖按“有合理钓鱼用途即标1”处理。再以 dark-web-forum-user role、specificity/precision 和 few-shot 示例抽取产品名、价格、功能和目标服务。产品名从 1,203 个原始变体归一为 910 个名称，服务名从 11,889 个变体归一为 5,460 个。

### 8.3 七阶段生命周期映射

两名研究者基于 30 个真实案例构造七阶段：1 target list construction；2 phishing site creation；3 malicious component creation；4 infrastructure setup；5 attack execution；6 validation/refinement；7 monetization。随后将 910 个产品人工归一到 39 个类别，并讨论其在每阶段的功能、价格、目标服务和作者分布。单帖可以对应多个阶段，因此阶段计数允许重复。

## 9. 学习与应用

### 9.1 复现关键步骤

1. 根据论文的论坛候选与排除标准建立可审计的 13 论坛清单，记录抓取日期和访问状态。
2. 使用 ACHE 或等价文本 crawler，仅保留 title/content/time/author；执行精确去重并保存原始 HTML 与派生表分离。
3. 固定 GPT-4o-mini 版本、两个 Appendix A.2 prompts、JSON schema 和抽样人工标注集；报告分类与字段抽取 P/R/F1。
4. 复核产品名/服务名归一化表和七阶段映射，分别统计 posts、products、authors、prices，避免把帖子数当成交数。
5. 对年度趋势、目标服务、作者集中度和价格分布报告可见性边界，并只在授权的论坛文本上运行。

### 9.2 能否迁移到其他任务？

LLM 分类—抽取—人工核验—实体归一化—生命周期映射的管线可迁移到其他地下市场威胁情报，但提示词、双用途边界和实体词典必须按领域重建。七阶段不是通用攻击本体，不能直接用于 ransomware、账户接管或非英语市场而不重新验证。

### 9.3 对防御研究的启发

论文的防御价值在于将部署前供应链信号与产品功能、目标服务和价格联系起来：Credential/Checker 的高活跃可提示目标名单阶段，Proxy/VPN 的稳定出现反映基础设施规避需求，Stealer 取代 Capture Tool 反映窃取凭证/session/cookie 的变化。更稳妥的防御系统应把论坛供给趋势与 URL、邮件、恶意站点遥测结合，而不是将发帖量直接当攻击量。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 13 论坛、394,034 帖、343,334 去重、2013–2025 | D2Web collection | §3.1 |
| 70,055 钓鱼相关帖子 | GPT classification | Abstract, §3.2 |
| GPT-4o-mini 验证：分类 F1=.90，产品名 F1=.89，服务名 F1=.88 | 200 样本人工核验 | §3.2 |
| 产品/服务归一化：1,203→910 product names；11,889→5,460 targets | LLM output refinement | §3.3 |
| 七阶段生命周期与 39 类产品 | 30 real-world cases + manual mapping | §4.1 |
| Step1/6/4 帖子占比 73.45/14.34/10.13% | Table 3 | §4.1 |
| 2016、2020、2023 发帖激增 | annual trend | §4.2, Fig. 5 |
| Step2 前10作者 43%，Step1/6 前10 15.55/6.22% | author concentration | §4.2, Table 4 |
| Step2 约45%目标为金融服务，Step3约20% | target service analysis | §4.2, Fig. 6 |
| 多平台恶意软件示例 $3,500–$10,000 | price analysis | §4.3, Fig. 8 |
| 多数产品免费但可组合完成攻击链 | free products discussion | §4.3 |
| 仅收集文本、不下载凭据/PII/媒体、不去匿名化 | Ethics | Appendix A.3 |

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-WWW-Unveiling_the_Underground_Phishing_Ecosystem__A_12-Year_Longitudinal_Study_of_Deep_and_Dark_Web_Forums.pdf
- MinerU Markdown：02-parsed-markdown/2026-WWW-Unveiling_the_Underground_Phishing_Ecosystem__A_12-Year_Longitudinal_Study_of_Deep_and_Dark_Web_Forums.md
- DOI：https://doi.org/10.1145/3774904.3792737

## 12. 后续问题

1. 英语论坛的 2013–2025 趋势在俄语、中文和封闭/付费市场是否一致？
2. 论坛发帖数量与实际商品成交、部署数量和攻击成功率之间的相关性如何？
3. GPT-4o-mini 的 200 样本验证能否扩展为按论坛、年份、产品类别分层的误差审计？
4. Step1 目标名单、Step4 proxy/VPS 与 Step6 checker 的跨阶段复用如何构成真正的供应链网络，而不仅是共现统计？
5. 2024 年 Stealer 超过 Capture Tool 是否由样本可见性、术语变化或真实攻击策略变化导致？

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

论文从“研究通常在攻击发生后才看到钓鱼”切入，提出论坛是攻击供应链的部署前窗口。作者先把不可控的 D2Web 内容收束为可审计的 13 个论坛、12 年帖子，再用 LLM 将文本转为产品、目标、价格和作者实体。第二个转折是把零散商品放进七阶段生命周期，使时间趋势和经济结构具有攻击流程解释。结果按 RQ1 产品、RQ2 时间/目标、RQ3 价格递进，并用作者集中度和免费产品组合揭示市场组织方式。结论回到防御：供应链信号可在 URL/站点落地前支持威胁情报，但覆盖和 LLM 误差限制了外推。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 角色 | 关键转折 |
|---|---|---|---|
| Introduction | 建立 attacker-centric pre-deployment gap | 问题框定 | 从受害者数据转向供应链 |
| Background | 统一 phishing product 与 D2Web 术语 | 语境 |
| Methodology | 论坛筛选→爬取→LLM→归一化→七阶段 | 方法闭环 | 文本变成结构化生态 |
| RQ1 | 产品类别、阶段和分布 | 生态结构 | Step1 占绝大多数 |
| RQ2 | 年度趋势、目标服务、作者 | 动态变化 | 2020/2023 与真实事件同向 |
| RQ3 | 价格、免费/付费差异 | 经济解释 | 免费组件可组合成全链 |
| Discussion/Ethics | 覆盖偏差、LLM 误差和数据保护 | 外推边界 | 不把帖子当攻击事实 |

### 13.3 Gap 展开方式

| Gap | 具体内容 | 论证方式 |
|---|---|---|
| 视角缺口 | 既有工作多从 deployed attacks/victim side 观察 | 论坛 attacker-centric supply chain |
| 结构缺口 | 零散帖子难对应真实攻击流程 | 39 产品→七阶段生命周期 |
| 纵向缺口 | 论坛研究缺少十二年组件/目标/作者/价格趋势 | 2013–2025 annual analysis |
| 经济缺口 | 产品价格和免费供给很少被系统统计 | category-level price/free analysis |

### 13.4 实验叙事方式

| 环节 | 作用 |
|---|---|
| LLM validation | 给自动抽取设置可信度上限 |
| Product mapping | 把语言内容转成攻击阶段 |
| Temporal trends | 连接论坛供给和外部 phishing 事件 |
| Target services | 解释金融/大用户平台偏好 |
| Authors/prices | 展示集中度和地下市场经济 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移写法 |
|---|---|---|
| 研究视角 | attacker-centric 与 post-attack 形成鲜明对照 | 先说明数据源改变了什么观察能力 |
| 管线命名 | collection→LLM→normalization→lifecycle | 给每一步定义可审计输出 |
| 统计解释 | 将帖子、产品、作者和阶段分别计数 | 先固定分母，再写趋势和集中度 |
| 伦理表达 | 直接说明不下载、不交易、不去匿名化 | 在方法章节明示数据最小化和合法边界 |

## 14. 证据边界与复现清单

1. **可见性边界**：仅 13 个英语、可访问论坛；不能将 70,055 帖或 39 产品外推为全球地下钓鱼生态总量。
2. **LLM 边界**：GPT-4o-mini 任务级 F1 约 0.88–0.90；全量字段和长尾术语可能有系统误差，人工验证样本不覆盖所有年份/论坛。
3. **计数边界**：一个帖子可含多个产品、目标和生命周期阶段；Table 3 阶段计数允许重叠，不能求和当独立帖子数。
4. **市场边界**：发帖、报价和免费分享不等于成交、有效性或攻击执行；作者名称掩码也限制个体归因。
5. **伦理边界**：只收集文本，不下载链接中的凭据/PII/媒体，不参与交易/去匿名化；复现应遵守相同最小化原则。
6. **复现依赖**：论坛候选和排除日志、ACHE crawler、GPT-4o-mini 版本/提示词、人工归一化词典、30 案例映射和价格清洗规则必须一并保存。

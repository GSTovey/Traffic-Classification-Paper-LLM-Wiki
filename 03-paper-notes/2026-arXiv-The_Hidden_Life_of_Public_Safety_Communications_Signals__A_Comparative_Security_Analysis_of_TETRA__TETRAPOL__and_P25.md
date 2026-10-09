---
type: paper
title_original: "The Hidden Life of Public Safety Communications Signals: A Comparative Security Analysis of TETRA, TETRAPOL, and P25"
title_cn: "公共安全通信信号的隐秘生活：TETRA、TETRAPOL 与 P25 的比较安全分析"
authors: [Larry Hernandez, Sergey Bratus]
year: 2026
venue: "arXiv 2026"
doi: "unknown"
url: "https://arxiv.org/abs/2608.05247"
pdf: "00-inbox/PDFs/2026-arXiv-The_Hidden_Life_of_Public_Safety_Communications_Signals__A_Comparative_Security_Analysis_of_TETRA__TETRAPOL__and_P25.pdf"
mineru_md: "02-parsed-markdown/2026-arXiv-The_Hidden_Life_of_Public_Safety_Communications_Signals__A_Comparative_Security_Analysis_of_TETRA__TETRAPOL__and_P25.md"
status: processed
reading_level: L1
research_area: []
task: []
method: []
dataset: ["TETRA 单部署语料（>1,600 万记录 / 36.25h）", "TETRAPOL 单部署语料（46 文件 / >3,300 万记录）", "P25 十系统语料（688,866 记录）", "CONUS P25 普查（567 系统 / 48 州）"]
code: "unknown"
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

# The Hidden Life of Public Safety Communications Signals: A Comparative Security Analysis of TETRA, TETRAPOL, and P25

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | The Hidden Life of Public Safety Communications Signals: A Comparative Security Analysis of TETRA, TETRAPOL, and P25 |
| 中文标题 | 公共安全通信信号的隐秘生活：TETRA、TETRAPOL 与 P25 的比较安全分析 |
| 作者 | Larry Hernandez, Sergey Bratus（Dartmouth College） |
| 年份 | 2026 |
| 会议/期刊 | arXiv 2026（解析稿首页无会议页眉，无 DOI/arXiv 编号） |
| 研究方向 | 公共安全数字集群通信（LMR）信令面被动安全分析；P25 第 3 章章节号显示编号兼容 IEEE 格式（§III 背景、IV 方法），与"流量/信令元数据推断"主题家族相近但载体为无线协议 |
| 任务类型 | 大规模被动测量 + 跨协议安全比较（含一次内容恢复案例） |
| 方法关键词 | 信令面/业务面分离、跨协议推断框架（五类信息）、WITCHHUNT 全小区观测站（Rust）、SDR 被动接收、RP-CELP 声码器逆向、MMDVM 便携解码 |
| 数据集 | 三个实测语料 + 一次全国普查：TETRA（>1,600 万包记录/36.25h）、TETRAPOL（46 文件/>3,300 万记录）、P25（10 系统/688,866 记录）、CONUS 567 系统/48 州 |
| 是否开源 | 未提及自有仓库（code=unknown）；工具链基于 dsd-neo、OP25、MMDVM_HS，另做 NOSYMESH 开源接收机工作（文中提及） |
| PDF | 00-inbox/PDFs/2026-arXiv-The_Hidden_Life_of_Public_Safety_Communications_Signals__A_Comparative_Security_Analysis_of_TETRA__TETRAPOL__and_P25.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-arXiv-The_Hidden_Life_of_Public_Safety_Communications_Signals__A_Comparative_Security_Analysis_of_TETRA__TETRAPOL__and_P25.md |

---

## 1. 一句话总结

> 被动接收 TETRA/TETRAPOL/P25 明文信令面即可推断拓扑、身份、移动与密钥轮换，TETRAPOL 紧急信道规范上不加密致语音可恢复。

---

## 2. 摘要翻译

### 2.1 摘要原文

> "These systems are expected to protect not just the content of a communication but the fact of it. Yet LMR standards leave a stark gap between confidentiality of content and of communication: underneath an encrypted traffic plane, their signaling plane is almost entirely in the clear... In the case of TETRAPOL, we demonstrate how inference and tracking of such signaling metadata and a standards-level confidentiality failure in emergency call handling enable unencrypted voice extraction."（Abstract，节选）

### 2.2 摘要中文翻译

公共安全机构与关键基础设施运营方依赖基于 P25、TETRA、TETRAPOL 的集群陆地移动无线电（LMR）系统。这些系统被期望不仅保护通信内容、还保护"通信这一事实"本身；然而 LMR 标准在内容保密与通信保密之间留下巨大鸿沟：在（可能加密的）业务面之下，其信令面几乎完全明文。本文探查从这些暴露信令中进行对抗性推断的深度与影响。以往的安全分析聚焦于内容面（恢复密钥或捕获偶然明文），本文表明：即使内容加密是完美的，被动观察信令仍可推断出同等敏感的信息。具体而言，一个被动、仅接收的 SDR 观察者可从三大 LMR 标准中恢复操作性敏感的拓扑与地理信息、单元存在性、跨小区/跨组的移动性、组织结构，以及特殊密钥域与密钥轮换等运行安全细节。这种信令面推断远超观察者的直接接收范围，把本地嗅探升级为全国性网络测绘能力，并通过时序与关联削弱或击穿标准的身份混淆机制。TETRAPOL 案例中，信令元数据推断加上紧急呼叫处理中的标准级保密缺陷，可实现明文语音提取。最后讨论对策与缓解建议，特别是对小区间/基站/用户身份保护的专门建议。

> ⚠️ MinerU 解析问题：§VI-A 标题被截断为 "Control-Channel Signaling in the Clea"（应为 "…in the Clear"）；第 140 行出现无意义乱码串（"�890723双56780222232425262223333"）；正文含 small-caps/上标碎片与连字丢失（如 "traf#c" 类），引用需还原。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

LMR 系统被采购方当作"安全通信"，但标准设计把信令面（控制信道：注册、归属、信道分配）与业务面（语音/数据）分离：业务面可加密，信令面明文。以往工作多数关注内容面（密钥恢复、偶然明文），信令面暴露的推断潜力未被系统性研究（§I）。

### 3.2 现有方法的痛点和不足

① 已有分析（Glass、Clark、Meijer 等）指出 P25/TETRA 缺少消息认证与元数据加密，但未覆盖信令面弱点的完整范围与实现差异；② 标准宣称的临时身份混淆（如 TETRA 的 (V)ASSI、ESI）在注册/迁移与 ESI 豁免字段处失效；③ 实际部署与规范存在偏离（未文档化保留 codop 等），单靠文本分析不足（§I、§IV、§VII-C）。

### 3.3 论文的研究假设或核心直觉

即使语音加密完美，明文信令中的标识、邻区广播、注册/归属事务、呼叫建立字段与密钥引用，组合起来即可暴露"谁、何时、在哪、与谁"；单一消息可能只泄露一个字段，但跨时间与跨小区的组合可以完成整个网络的情报重建（§IV、§V）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 控制信道明文广播网络/小区标识、频率计划、邻区表；呼叫建立广播密钥引用 | §VI-A–B、§VI-E |
| 痛点提炼 | 本地嗅探因邻区广播变为"自引导"的递归发现，升级为全国级测绘 | §VI-B、Figure 1/4 |
| 问题转化 | 形式化五类推断（身份枚举、拓扑地理、存在/活动/移动、组织结构、运行安全），建立跨协议对照 | §V、§IX |
| 文献定位 | 内容面已被研究，信令面推断深度与跨协议统一框架缺失；TETRAPOL/TETRA 缺少首个实测安全研究 | §I、§XI |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 明文信令面足以支撑与内容恢复同等敏感的情报推断 | §V | 三个实测语料的量化评估（§X） |
| 辅助假设（如有） | 标准级规范缺陷（ECH 明文）使紧急呼叫内容可无密钥恢复 | §VI-E 规范分析 | 5 次运营部署 ECH 激活实测（§X-D） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 信令面推断成立 | 支撑 | TETRA 12,283,156 条 PDU/36.25h/251 个 SSI；TETRAPOL 88 组、67,364 条邻区记录；P25 30.0% 身份帧明文 RID | §X、§X-A |
| ECH 明文可恢复语音 | 支撑 | 5/5 次 ECH 激活均为 UNENCRYPTED_CALL，RP-CELP 解出可懂语音 | §X-D、Figure 9 |

---

## 4. 方法设计

### 4.1 方法整体流程

搭建 WITCHHUNT（WH）实时接收框架：宽带 IQ 一次信道化 → 并行解调各控制载波（GMSK、FEC、HDLC/TSDU/CODOP 逐层）→ 归一化事件提取（身份/拓扑/活动/移动/归属/加密状态）→ 跨协议推断框架聚合（五类）→ 由恢复的 grant 回溯式从环形缓冲提取语音/数据/紧急信道窗口（§IV-A、Figure 3）。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 | 宽带 IQ | 多相滤波器组信道化，锁定控制载波 | 各信道解调流 | 一次采集覆盖全小区 |
| Step 2 | 解调流 | PHY→链路（HDLC/TSDU/CODOP/IE）逐层解码 | 序列化小区与 grant 状态 | 语义化信令 |
| Step 3 | 小区/grant 状态 | 归一化为通用事件词表（身份、拓扑、活动、移动、密钥态） | 跨协议统一事件 | 支撑五类推断 |
| Step 4 | grant 与缓冲 IQ | 环形保留缓冲按 grant 提示回溯提取语音/ECH 窗口 | 语音/数据帧 | 免实时调谐的内容捕获 |
| Step 5 | 归一化事件 | 跨时间/跨小区聚合（拓扑图、移动性、密钥轮换） | 五类情报 | 形成安全结论 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| WH 观测站（Rust） | 实时全小区接收与解码 | 宽带 IQ | 事件流 | 主框架 |
| 协议解析层 | TETRA/TETRAPOL/P25 各自的 PHY/链路/语义解码 | 信道化流 | PDU/codop | 归一化上游 |
| 归一化事件层 | 统一身份/拓扑/活动/移动/密钥事件 | PDU | 通用事件 | 推断框架输入 |
| 推断框架（五类） | 身份枚举、拓扑地理、存在活动移动、组织结构、运行安全 | 通用事件 | 情报结论 | §V |
| 便携平台（MMDVM_HS/ADF7021 改造） | 低成本 TETRAPOL 解码与近场跟踪 | 射频 | 解码输出 | 补充实验 |
| 语音恢复（RP-CELP 逆向） | 解出 ECH 明文语音 | ECH 语音帧 | 可懂语音 | 内容层案例 |

### 4.4 公式、算法和机制解释

核心机制是"自引导拓扑发现"：D_NEIGHBOURING_CELL（TETRAPOL）/D-NWRK-BROADCAST（TETRA）广播邻区 ID 与其控制信道频率，观察者递归调谐即可遍历全网（§VI-B）；密钥态推断利用 KEY_REFERENCE（KEY_TYPE 高半字节 + KEY_INDEX 低半字节）随呼叫建立明文广播，纵向观测得到密钥轮换周期（0x4c→4d→4e→4f→回绕 0x41，约每日 13:00 UTC）（§VI-E, Figure 6）；身份绑定链：注册事务把临时标识与永久标识绑定（TETRAPOL: RTI↔TTI↔HOST_ADR；TETRA: USSI→(V)ASSI，USSI 豁免 ESI），TEI 与事件标签亦明文（§VI-C、§VII-C）；内容恢复：ECH 的 KEY_REFERENCE=UNENCRYPTED_CALL 为规范强制，仅需信道解扰 + FEC + 逆向 RP-CELP 声码器（§X-D）。

### 4.5 方法优势

首个对 TETRAPOL 与 TETRA 的实测信令面安全研究；单载波即可引导全网测绘；推断不需要任何密钥或解密，也不需要高成本/近距离（P25"最近无线电攻击"评估）；覆盖三个标准与多个真实部署，量化规模大（TETRA 1,228 万条 PDU、TETRAPOL 3,300 万条记录、P25 十系统、CONUS 567 系统普查）（§II、§X）。

### 4.6 方法不足

仅被动观察，未做主动攻击或密码分析（作者自述受伦理/法律约束）；缺少受控基站，SDS 等用户自定义应用的系统性研究因接入与邻近度受限而未展开；普查可能低估实际暴露（驻留时间、接收几何限制）；标准级的长期替换周期使缓解措施传播缓慢（§XIII、§XII）。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

与以往聚焦内容面（密钥恢复、偶然明文捕获）的 LMR 安全研究不同，本文把信令面当作独立攻击面，证明"内容加密完美也挡不住"的元数据推断；与网络侧 WF/流量分析不同，其载体是无线协议的规范字段与广播，且能利用协议语义（grant、codop）做自引导遍历（§I、§XI）。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| 跨协议信令推断框架 | 五类信息 + 通用事件词表的跨标准映射 | 高 | 是（分析其他信令协议的方法论） |
| WITCHHUNT 观测站 | 实时全小区接收、归一化事件、回溯式提取 | 高 | 是（开源工作流） |
| TETRAPOL ECH 规范级缺陷 | 标准要求紧急信道不加密，实测 5/5 明文可恢复 | 高 | 是（标准/合规层面） |
| 全国级部署普查 | CONUS 567 系统/48 州加密使用统计 | 中-高 | 是（测量方法） |

### 5.3 适用场景

公共安全 LMR 网络的被动安全评估；合规与标准修订（身份保护、密钥分层、邻区广播限制）；低成本 SDR + 开源工具链的实地接收（含 MMDVM 便携平台近场接收）（§XII、§X-F）。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 既有 LMR 安全研究（Glass/Clark/Meijer 等） | 指出缺少消息认证与元数据加密 | 以内容面为主，信令面未系统展开 | 建立跨协议信令推断框架并实测 |
| 单点嗅探（本地接收） | 部署简单 | 受接收范围限制 | 用邻区广播自引导递归测绘全网 |
| 加密强度评估（TEA1 等） | 关注密码算法 | 忽略"通信事实"泄漏 | 证明元数据推断与内容同等敏感 |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

被动接收三个标准的多套真实部署：TETRA 单部署连续下行接收、TETRAPOL 两个欧洲部署（含 46 个运营文件）、P25 十个系统 + CONUS 普查；辅以 MMDVM_HS（ADF7021）改造的便携 TETRAPOL 解码与 RP-CELP 声码器逆向（§X、§X-F）。

### 6.2 数据集

TETRA：>1,600 万包记录/36.25h，其中 12,283,156 条有效 PDU（128.41 包/秒），251 个非保留明码 SSI（含 2,142 条位置更新族 PDU 指向 230 个 SSI）；TETRAPOL：46 个运营文件、>3,300 万原始解码记录、12,154 个 TTI 与 4,095 个 RTI、5,296,573 条活动态发射（88 个组）、1,586 次 ECH 激活（其中 877 次非加密）、67,364 条邻区记录；P25：688,866 条记录（去重后 600,036 个唯一事件，10 系统；NTIRN 深挖 121,302 事件/58.5h）；普查：567 个 P25 系统/48 州（§X-A）。

### 6.3 Baseline

无 ML baseline；对照对象为各标准的规范要求（PAS/EN/TIA 条款）与既有文献（[6]–[9]、[40] 等），以及各协议间的横向比较（§IX、§XI）。

### 6.4 评价指标

语料规模与解析成功率（PDU/记录数、包速率）、可枚举身份/组数量、邻区与拓扑记录数、明文身份帧比例、加密 TG 比例、ECH 明文案数量与语音可懂性（§X-A–D）。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| TETRA 单部署 | 有效 PDU 数/时长 | 12,283,156 / 36.25 h | — | — | 128.41 包/秒；251 个明文 SSI |
| TETRAPOL 单部署 | 记录/组/邻区 | >3,300 万 / 88 组 / 67,364 邻区记录 | — | — | 1,586 次 ECH 激活、877 次非加密 |
| P25 十系统 | 身份帧明文比例 | 30.0%（6,445/21,514） | — | — | 181 个 RID、84 个 TG |
| CONUS P25 普查 | 加密覆盖率 | 19% TG 加密；27% 系统无加密；中位 18% | — | — | 567 系统/48 州、约 138,000 TG |
| TETRAPOL ECH | 明文语音恢复 | 5/5 次激活解出可懂语音 | — | — | 规范要求 UNENCRYPTED_CALL，无需密钥 |
| TETRAPOL 密钥轮换 | 轮换周期 | 0x4c→4d→4e→4f→回绕，每日 ≈13:00 UTC | — | — | 两个小区可复现区分 |

### 6.6 优势最明显的场景

对"以为加密即安全"的运营部署：信令面暴露组织结构、指挥链、存在性与应急状态（即使语音全程加密）；TETRAPOL 紧急呼叫（伤情最敏感时刻）反而规范上明文，是本文最具冲击力的案例（§X-B、§X-D）。

### 6.7 局限性

受伦理/法律约束未做主动攻击与密码分析；无受控基站；SDS/用户自定义应用面未系统研究；普查可能低估暴露；不同部署实现差异大（部分结论依赖具体运营商配置，如 ECH 明文在"one deployment"中的持续性）（§XIII、§X-C）。

---

## 7. 学习与应用

### 7.1 是否开源？

未提及自有代码仓库；文中说明工具链基于/修改 dsd-neo，并使用 OP25、MMDVM_HS 开源组件，未来工作提及开源密码协处理器与 NOSYMESH 接收机的构想。

### 7.2 复现关键步骤

1. 用 SDR 接收控制载波，按协议做信道化 + GMSK 解调 + FEC/HDLC 解码；
2. 解析邻区广播，递归调谐遍历全网，重建拓扑与频率计划；
3. 归一化事件（注册/归属/grant/密钥引用），纵向统计存在性、移动性与密钥轮换；
4. 对 ECH 类 grant 回溯提取语音窗口，做解扰 + RP-CELP 解码。

### 7.3 关键超参数、预处理和训练细节

无模型训练。关键工程细节：TETRAPOL 上行 30 ms 段与交织/重组处理、混合语音数据帧解析；MMDVM_HS 上把 ADF7021 的 D-Star GMSK 路径复用并重定时到约 8000 bit/s（对抗 4% 符号率偏差）；TETRA 频段与载波号在文中被掩码/匿名化（§IV-D、§X-F）。

### 7.4 能否迁移到其他任务？

可迁移点：① "明文信令面 + 加密业务面"的分离分析范式可迁移到任何带控制面/数据面分离的系统（含 IP 网络的信令协议、IoT 协议）；② 邻区广播自引导的递归测绘思路可迁移到任何包含邻区/邻居列表的协议；③ "加密状态字段本身泄露安全姿态"（KEY_REFERENCE/ALGID/KID）对网络流量分析同样成立（TLS 密码套件、QUIC 参数等）（以下为笔记作者的迁移分析，非论文原文主张）。

### 7.5 对我的研究有什么启发？

① 元数据推断的威力在"内容加密完美"前提下依然成立，这与加密流量分析的核心命题同构——评估任何加密系统时都应单独列出信令/元数据面；② 其"规范强制明文"的发现提示：安全评估应区分"加密强度"与"协议设计"，后者常是被忽略的系统性缺陷源；③ 大规模被动语料的归一化事件 + 跨时间聚合方法论，可复用到流量侧的长期测量研究。

---

## 8. 总结

### 8.1 核心思想

> 信令面明文使被动接收即可推断整个网络。

### 8.2 速记版 Pipeline

1. SDR 宽带接收，信道化解调控制载波（WH/Rust）；
2. 从邻区广播自引导递归测绘全网拓扑与频率计划；
3. 归一化事件（身份/拓扑/活动/移动/密钥态）并跨时间聚合；
4. 由 grant 回溯提取语音与 ECH 窗口（MMDVM 便携平台可用）；
5. 结论：TETRA 1,228 万 PDU / TETRAPOL 88 组 / P25 十系统、CONUS 567 系统普查；TETRAPOL ECH 5/5 明文语音可恢复。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- [[encrypted-traffic-analysis]]（仅作思路近邻：本文同样论证"内容加密不保护元数据"，但载体为 LMR 无线协议而非 IP 流量，不构成实质关联，聚合时勿并入该概念簇）

### 9.2 相关方法

- 库内无对应方法页：本文无 ML 方法，方法学为被动测量 + 跨协议推断框架，白名单 8 个 slug 均不适用。

### 9.3 相关任务

- 库内暂无对应任务页（论文任务为无线协议信令面推断与测量，非流量分析任务）。

### 9.4 可更新的综述页面

- 暂无：与库内 5 个综述页主题均不重叠；若日后建立"元数据/信令面泄漏"类综述可回链。

### 9.5 可加入的对比表

- 暂无适用项（无开源代码登记、无新数据集、不提出可入 [[method-comparison-table]] 的流量分析方法）。

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| TETRAPOL ECH 规范强制不加密（PAS 0001-3-2 §4.4.33 KEY_REFERENCE=UNENCRYPTED_CALL），运营部署 5/5 次激活恢复明文语音（RP-CELP，无需密钥，如 D_CH_SCRAMBLING=82） | §X-D、Figure 9、§VI 引言 | §X-D |
| 单条邻区广播即可引导全网测绘并推断覆盖/地理 | D_NEIGHBOURING_CELL 解析（10 个邻区）、Figure 1/4 | §VI-B |
| 两大语料规模：TETRA 12,283,156 条有效 PDU/36.25h、128.41 包/秒、251 个明文 SSI（位置更新 2,142 条指向 230 个 SSI）；TETRAPOL >3,300 万记录、88 个组、67,364 条邻区记录、1,586 次 ECH 激活（877 次非加密） | §X-A(1)(2) | §X-A |
| P25 十系统 600,036 唯一事件，30.0% 身份帧明文 RID；CONUS 567 系统/48 州，19% TG 加密、中位 18%、27% 系统无加密 | §X-A(3)、§X-B | §X-A–B |
| 密钥轮换可纵向观测：0x4c→4d→4e→4f→回绕 0x41，每日 ≈13:00 UTC | §VI-E、Figure 6 | §VI-E |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-arXiv-The_Hidden_Life_of_Public_Safety_Communications_Signals__A_Comparative_Security_Analysis_of_TETRA__TETRAPOL__and_P25.pdf
- MinerU Markdown：02-parsed-markdown/2026-arXiv-The_Hidden_Life_of_Public_Safety_Communications_Signals__A_Comparative_Security_Analysis_of_TETRA__TETRAPOL__and_P25.md

---

## 12. 后续问题

- 暂未整理。

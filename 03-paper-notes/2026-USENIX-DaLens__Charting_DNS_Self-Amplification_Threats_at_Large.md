---
type: paper
title_original: "DaLens: Charting DNS Self-Amplification Threats at Large"
title_cn: "DaLens：大规模刻画 DNS 自放大威胁"
authors: ["Liwen Xu", "Zechao Cai", "Huayi Duan", "Adrian Perrig"]
year: 2026
venue: "USENIX Security 2026"
doi: unknown
url: "https://www.usenix.org/conference/usenixsecurity26/presentation/xu-liwen"
pdf: "00-inbox/PDFs/2026-USENIX-DaLens__Charting_DNS_Self-Amplification_Threats_at_Large.pdf"
mineru_md: "02-parsed-markdown/2026-USENIX-DaLens__Charting_DNS_Self-Amplification_Threats_at_Large.md"
status: deep-analyzed
reading_level: L3
research_area: ["DNS security measurement", "self-amplification DoS", "open DNS infrastructure"]
task: ["Internet-scale measurement", "resolver topology inference", "amplification-risk assessment"]
method: ["programmable reactive nameserver", "egress-anchor inference", "binary-search threshold probing", "compositional amplification measurement"]
dataset: ["307,397 persistent public resolvers", "276,399 resolvers with reliable egress attribution", "21,344 unicast recursors", "7,764 anycast recursors", "six globally distributed probes"]
code: "artifact: https://doi.org/10.5281/zenodo.17832418; information page: https://dalens.netsec.ethz.ch/"
relevance: medium
created: "2026-09-29"
updated: "2026-10-10"
---

# DaLens: Charting DNS Self-Amplification Threats at Large

> **L3 深度分析笔记**：基于论文正文 §1–§8、Tables 1–3、Figures 1–15、Ethical Considerations 与 Open Science 章节，以及 MinerU 原始解析稿交叉核对。本文是 DNS 安全测量论文，与本库的加密流量分类主线只有间接方法论关联；所有数量均保留论文的测量口径。

## 0. 论文基础信息
| 项目 | 内容 |
|---|---|
| 原文标题 | DaLens: Charting DNS Self-Amplification Threats at Large |
| 中文标题 | DaLens：大规模刻画 DNS 自放大威胁 |
| 作者 | Liwen Xu、Zechao Cai（ETH Zurich），Huayi Duan（HKUST(GZ)），Adrian Perrig（ETH Zurich） |
| 年份 | 2026 |
| 会议/期刊 | USENIX Security 2026 |
| 研究方向 | DNS 安全测量、开放 DNS 基础设施、自放大 DoS |
| 任务类型 | 公共解析器发现、递归器/转发器结构识别、MAF 测量与风险排序 |
| 方法关键词 | ODNS 四元组、egress set、egress anchor、PRN、状态跟踪、二分阈值、组合放大 |
| 数据与测量规模 | 307,397 个持久公共解析器；276,399 个可可靠归因解析器；21,344 个单播递归器；7,764 个 anycast 递归器；六个主探针及约 1,000 个 RIPE Atlas 探针 |
| 是否开源 | Zenodo artifact DOI 10.5281/zenodo.17832418；工具按申请向经核验实体提供，不立即公开 |
| PDF | 00-inbox/PDFs/2026-USENIX-DaLens__Charting_DNS_Self-Amplification_Threats_at_Large.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-USENIX-DaLens__Charting_DNS_Self-Amplification_Threats_at_Large.md |

## 1. 一句话总结
> DaLens 用可编程反应式权威 DNS、egress 依赖推断和按解析器定制的组合探测，在 307,397 个持久公共解析器中识别约 29K 个可作为自放大器的递归器；在 12,539 个递归器的组合测试中，约 2% 的 MAF 超过 200，极端值接近 1,000。

## 2. 摘要原文
The emerging self-amplification attacks (SAAs) pose serious denial-of-service (DoS) risks to the Domain Name System (DNS). They can substantially amplify the interactions between recursive and authoritative servers, depleting resources at disproportionally small costs. Assessing the impact of such attacks on the global name resolution infrastructure is crucial for DNS operators to effectively triage threats and deploy defenses, yet this remains an uncharted and daunting territory. We have conducted the first large-scale measurement study of SAAs, leveraging a versatile framework, DaLens, which we designed and developed. The work consists of untangling the intricate Open DNS infrastructure to identify effective amplifiers and quantifying their amplification capabilities in a modular, scalable, and sound manner. Out of 307K persistent public resolvers, we find 29K unique resolver clusters that can be exploited in parallel for SAAs, and a significant number of them can still produce large amplification effects even though these vulnerabilities had already been disclosed in prior work.

## 3. 方法分析

### 3.1 方法动机与研究问题

SAA 利用递归 DNS 的正常解析逻辑，让一次客户端请求触发大量上游查询。作者把问题拆成两个研究问题：哪些（集群）解析器是真正稳定可触发的放大器，以及它们在单原语和组合原语下能达到多大的 message amplification factor（MAF）。MassDNS、ZDNS、AmpMap 和 PolarDNS 无法同时处理缓存、转发、anycast、动态响应和组合放大，因此需要结构化的 ODNS 测量框架（§1–§3）。

### 3.2 输入—处理—输出

| 阶段 | 输入 | 处理 | 输出 |
|---|---|---|---|
| 发现与过滤 | IPv4 地址空间、随机 A 请求 | XMap 三轮每 IP 发送 2 UDP+2 TCP 请求；保留三轮答案正确且可持续的公共解析器 | 3,421,931 个曾响应者、307,397 个可信公共解析器 |
| 结构识别 | probe–resolver 请求、PRN egress 日志 | 唯一 QNAME 绕过缓存；枚举 egress；按 R1–R4 识别 anchor、歧义映射和 forwarder | 276,399 个可归因解析器、21,344 个递归 egress set、约 29K 最小放大集合 |
| 阈值测量 | 递归器、NS/CNAME/referral/DDLG 模板 | 在安全范围内二分每个 SAA 原语可接受的深度/宽度 | 解析器特定 primitive threshold |
| 组合测量 | 个体阈值、PRN 配置 | 组合 CNAME rewrite 与 dense delegation；遇到循环/抑制即剪枝 | 12,539 个递归器的 MAF 分布和风险排序 |

## 4. 实验表现

### 4.1 关键结果

| 结果 | 数值/观察 | 位置 |
|---|---:|---|
| 三轮曾响应 distinct resolvers | 3,421,931 | §5.1 |
| 三轮均正确且持续的公共解析器 | 307,397 | §5.1 |
| 可可靠完成 egress attribution 的解析器 | 276,399 | §5.2 |
| 递归 egress set / recursor 核心 | 21,344（约为可信解析器的 6.94%） | §5.2, Fig. 7 |
| 可并行利用的 SAA 最小集合 | 约 29K | Abstract, §5.2 |
| 稳定指向这些集合的 forwarders | 110,129；多上游 forwarders 189,504 | §5.2 |
| 并发转发 resolver | 7,532 | §5.2 |
| NS fetch / chain | 近 50% 拉取 >10 条 NS；约 15% 接受 >10 层 referral，约 8% >20 层 | §5.3 |
| CNAME chain / dense delegation | >85% 至少跟随 10 次 CNAME；约 1% dense delegation >60 | §5.3 |
| 组合 MAF | 90% <100；约 2% >200；最高接近 1,000 | §5.4, Fig. 15 |

论文没有机器学习 baseline、训练/测试划分或随机种子；对照对象是既有 DNS 测量工具和单原语研究。

## 5. 局限性与复现建议

- 结果只覆盖 2025 年三轮可从探针访问、答案正确且持续的公共 IPv4 解析器；短暂、地域受限、IPv6-only 或过滤行为不同的解析器被排除。
- egress anchor 是外部行为等价类，不能总区分自身递归器和单上游 forwarder；R3 随机 egress 只能以集体 ingress 测量。
- MAF 是论文给定配置下的保守可观测放大，不是每个解析器的最大理论上限；更高上限需要更侵入性探测，作者因伦理原因留待未来。
- 主测量使用六个探针，anycast 用约 1,000 个 RIPE Atlas 探针拆分 PoP；地理覆盖与探针可达性会影响可见性。
- artifact 含源码和脚本，但不立即公开，只向经核验实体按申请提供，普通研究者无法直接重放全空间扫描。

复现时应先在自有域名和自有解析器上部署 PRN，验证 confID/instanceID、cache-miss、egress 日志与 anchor 判定，再在论文安全上下界内做单原语二分；只对获授权目标进行组合测试。

## 6. 知识链接
- 暂无与 DNS 自放大完全对应的现有概念/方法页；不新建空白页。
- 与加密流量分类主线仅有间接方法关联：可借鉴“稳定入口—隐藏后端—响应行为”的黑盒测量拆分。

## 7. 证据状态
- 正文证据已核对至 §1–§8、Tables 1–3、Figures 1–15、Ethical Considerations、Open Science。
- 论文 DOI 未在解析稿给出；10.5281/zenodo.17832418 是 artifact DOI，不是论文 DOI。
- MAF 与解析器数量均保留作者口径；不将“可测”或“接近 1,000”泛化为所有 DNS 部署的永久上限。



## 8. 详细方法与机制

### 8.1 ODNS 形式化

论文用 \(\mathcal{O}=(S,E,\mathcal{U},\mathcal{E})\) 表示开放 DNS：\(S\) 是 resolver 集合，\(E\) 是所有 recursor egress，\(\mathcal{U}\subseteq S\times S\) 是 forwarding 关系，\(\mathcal{E}\subseteq R\times E\) 是 recursor 到 egress 的映射。\(R\) 表示直接查询权威服务器的递归器，\(F=S\setminus R\) 表示转发器。

### 8.2 Egress anchor 与四类递归器

R1 只有一个固定 egress；R2 有多个独立 egress 且按 IP/客户端稳定负载均衡；R3 有多个独立但随机或不可预测调度的 egress；R4 的多个 egress 协同处理同一请求。若同一 probe–resolver 对在多轮中稳定唯一触发某个 egress set，则记录为 anchor；若行为不稳定，放入歧义映射 D，必要时把完整 egress 集合作为 R3 的 ingress。该过程得到可重复测量的最小集合，但仍保留行为等价类限制。

### 8.3 PRN、Probe、Manager

PRN 是核心权威端。每个 resolution configuration 定义有序响应模板，以 confID 标识；每次执行以 instanceID 标识。两者写入 QNAME（例如 `a.conf-x-ins-y.[domain]`），即使启用 QNAME minimization，专用子域仍可携带会话标识。PRN 按会话计数器返回下一条响应，从而支持多阶段 CNAME、NS 和 delegation 组合。无状态 probe 只负责从不同 ingress 发送请求，manager 分配全局 ID、下发配置、调度 probe 并合并 probe/PRN 日志。

### 8.4 阈值—组合测量

对 NS fetch、NS chain、CNAME rewrite 与 dense delegation，先在安全上下界（示例为 1–50）中进行二分搜索；每次根据是否产生后续出站查询调整边界。再把最强原语按 breadth/depth 组合，遇到循环检测、查询预算或解析抑制即剪枝。MAF 按模式计算：fanout 统计不同 NS 目标查询，顺序链取最大模板 ID，dense delegation 与组合模式按唯一查询数。这样得到的是对目标解析器在受控配置下的实测放大，而非静态阈值乘积。

## 9. 学习与应用

### 9.1 是否开源？

Zenodo artifact DOI 为 10.5281/zenodo.17832418，包含源码和实验脚本；论文说明工具不会立即公开，只向经核验的运营商、厂商和研究者按申请提供。信息页为 https://dalens.netsec.ethz.ch/。因此应记为“有 artifact、受限开放”，不能写成普通 GitHub 仓库已公开。

### 9.2 复现关键步骤

1. 获取 artifact 和访问许可，确认 PRN、manager、probe 配置与受控域名。
2. 在自有域名部署 PRN，验证 confID/instanceID、会话计数器、日志关联和 cache-miss。
3. 用少量自有解析器复现 R1–R4 的 egress 观测、anchor 和最小集合判定。
4. 在论文安全范围内执行单原语二分，并记录出站查询、版本、探针位置和阈值。
5. 仅对获授权目标运行组合测试，计算 MAF 并保存完整 probe/PRN 日志。

### 9.3 能否迁移到其他任务？

可迁移到需要“受控请求触发黑盒状态机并观察跨节点依赖”的协议测量，例如 DNS over TLS/QUIC 的递归路径、服务发现链或代理后端依赖。PRN 的动态响应、anchor 的稳定入口和阈值—组合测量是通用组件；DNS 记录模板、缓存规避和 MAF 定义不能直接照搬。

### 9.4 对流量分析研究的启发

论文不训练流量分类模型，也没有 payload 学习结果。可迁移的方法论是把“可观测入口—隐藏后端—响应行为”拆成结构图，再用稳定触发单元做测量；在加密流量研究中，可用于区分协议指纹、负载均衡端点和跨会话依赖，避免把同一服务的多后端行为混成一个标签。

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| SAA 通过递归器—权威服务器交互放大 DoS 成本 | 自放大定义与动机 | §1, §2.2 |
| ODNS 用 resolver、egress、forwarding、egress mapping 四元组形式化 | \(\mathcal O=(S,E,\mathcal U,\mathcal E)\) | §3.1 |
| 四类 recursor R1–R4 与 anchor/egress grouping | taxonomy、Algorithm 1 | §3.2, Table 2 |
| 三轮 IPv4 发现后得到 307,397 个持续且正确的公共解析器 | XMap discovery 与 correctness 过滤 | §5.1, Table 3 |
| 276,399 个解析器可完成可靠 egress attribution | resolver set 结果 | §5.2, Fig. 6 |
| 约 29K 最小放大集合、110,129 稳定 forwarders、189,504 多上游 forwarders | anchor/grouping 结果 | §5.2, Key Observation 2 |
| NS/CNAME/referral/DDLG 存在宽松阈值 | primitive distributions | §5.3, Figs. 10–13 |
| 组合 MAF 长尾，最高接近 1,000，且不是简单阈值乘积 | CNAME+DDLG 组合测量 | §5.4, Figs. 14–15 |
| 结果是保守估计，更高上限需要更侵入 probing | 作者自述 | §5.4 |
| 低请求率、受控域名、opt-out 与协调披露构成伦理控制 | Ethical Considerations | §Ethical Considerations |
| artifact 含源码和脚本但不立即公开 | Open Science | §Open Science |

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-USENIX-DaLens__Charting_DNS_Self-Amplification_Threats_at_Large.pdf
- MinerU Markdown：02-parsed-markdown/2026-USENIX-DaLens__Charting_DNS_Self-Amplification_Threats_at_Large.md
- 会议页面：https://www.usenix.org/conference/usenixsecurity26/presentation/xu-liwen
- 信息页：https://dalens.netsec.ethz.ch/
- Artifact DOI：https://doi.org/10.5281/zenodo.17832418

## 12. 后续问题

1. 29K“可并行利用”集合在后续补丁和运营策略变化后还剩多少，需要用同一 protocol 做时间序列复测。
2. R3 随机调度下的集体 ingress 是否高估单个攻击者可稳定触发的 MAF，需要跨 probe 重复和置信区间。
3. 组合模式只选 CNAME rewrite + dense delegation；NS fanout、QMIN、循环等更多组合是否产生更高 MAF，论文未回答。
4. 受限开放 artifact 是否足以让独立研究者复核阈值分布，需要明确可申请的代码、配置、日志和最小复现实验包。
5. 防火墙/IDS sinkhole 与真实 resolver 的区分依赖测量域名和多轮答案正确性，在其他威胁情报环境下的误分类率仍不明。

## 13. 写作叙事与故事线分析

### 13.1 论文主线故事线

论文先把 SAA 与传统反射攻击区分开：攻击者不需要放大单个 DNS 响应，而是诱导递归器自己产生大量上游查询。随后作者把“全球有多少危险解析器”拆为两个可测问题：ODNS 的依赖结构是什么，递归器在单原语与组合原语下能放大多少。转折点是 PRN 与 egress anchor：前者让权威侧响应可编程且有状态，后者让隐藏的递归行为获得稳定的黑盒入口。实验从三轮发现、结构识别、原语阈值逐层收紧到实际 MAF，最后用 29K 放大集合和接近 1,000 的 MAF 长尾回答风险集中在哪里、为什么仍值得修补。伦理与披露章节把结果收束为低扰动测量和运营者优先级。

### 13.2 章节叙事功能

| 章节 | 叙事功能 | 承担的角色 | 关键转折点 |
|---|---|---|---|
| Abstract/Introduction | 先给出 SAA 的工作放大不对称，再给测量规模和风险结果 | 价值与问题建立 | 递归器自己成为放大器 |
| Background | 区分 recursor、forwarder、egress 与四类 SAA primitive | 统一术语 | 从攻击实例转为可组合原语 |
| Methodology | 形式化 ODNS、anchor 和最小集合 | 将复杂基础设施变成可推理对象 | 行为等价类与稳定 ingress |
| DaLens | 用 PRN、probe、manager 实现方法 | 工具化落地 | confID/instanceID 支持并发状态 |
| Results | 发现→结构→单原语→组合 MAF 四段递进 | 逐层回答研究问题 | 组合 MAF 不是单阈值乘积 |
| Disclosure/Ethics | 说明修补、负载控制和发布策略 | 限定攻击性外推 | 工具受限开放而非立即公开 |
| Conclusion | 回到少量 recursor 核心导致大范围依赖风险 | 风险排序收束 | 从全空间扫描转为关键节点治理 |

### 13.3 Gap 展开方式

| Gap 类型 | 具体内容 | 论证方式 | 位置 |
|---|---|---|---|
| 结构缺口 | ODNS 的 forwarding/egress/anycast 结构不透明 | 正式四元组与 R1–R4 taxonomy | §3.1–3.2 |
| 工具缺口 | 静态 nameserver/扫描器不能生成任意有状态组合响应 | PRN 的可编程、状态化和自动化设计 | §1, §4 |
| 指标缺口 | 单原语上限不能代表实际组合 MAF | 个体二分后做 resolver-specific composition | §3.3, §5.4 |
| 治理缺口 | 全空间风险无法直接转为修补顺序 | 用依赖关系、anchor 和 MAF 进行 triage | §5.5, §6 |

### 13.4 实验叙事方式

| 实验环节 | 叙事功能 | 与主线的关系 |
|---|---|---|
| 三轮发现与过滤 | 排除 churn、错误响应和 sinkhole | 确定可信测量总体 |
| Egress/anchor 识别 | 解释哪些 IP 是递归器、哪些只是转发器 | 建立结构层证据 |
| 单原语阈值 | 展示常见解析器限制并指出宽松长尾 | 建立组合测试输入 |
| CNAME+DDLG 组合 | 直接给出 MAF 长尾和内部全局限制 | 回答威胁规模问题 |
| 披露与复测 | 连接测量、修补与运营决策 | 证明结果可行动而非只列漏洞 |

### 13.5 写作风格与可迁移写法

| 维度 | 本文做法 | 可迁移的写作模式 |
|---|---|---|
| 问题拆分 | 将风险有多大拆为结构识别和放大能力两个问题 | 先定义可观测对象，再定义量化指标 |
| 方法命名 | 用 PRN、anchor、minimal set 给复杂过程稳定术语 | 为中间证据单元命名，便于跨章节复用 |
| 结果递进 | discovery→classification→primitive→composition | 每层结果都成为下一层实验的输入 |
| 证据边界 | 直接说明观测等价类、保守 MAF 和更高上限未测 | 把测到什么和不能推出什么写在同一段 |
| 影响落地 | 用依赖集中度和 MAF 排序运营者优先级 | 将大规模测量转译为具体治理动作 |

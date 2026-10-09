---
type: paper
title_original: "InSPECtor: Improving SLEIGH Processor Specification Veracity via Proxy"
title_cn: "InSPECtor:通过代理执行提升 SLEIGH 处理器规范的正确性"
authors: [Michael Chesser, Paul Quirk, Douglas Cooke, Guy Farrelly, Surya Nepal, Damith C. Ranasinghe]
year: 2026
venue: "USENIX Security 2026"
doi: "unknown"
url: "https://www.usenix.org/conference/usenixsecurity26/presentation/chesser"
pdf: "00-inbox/PDFs/2026-USENIX-InSPECtor__Improving_SLEIGH_Specification_Veracity_via_Proxy.pdf"
mineru_md: "02-parsed-markdown/2026-USENIX-InSPECtor__Improving_SLEIGH_Specification_Veracity_via_Proxy.md"
status: processed
reading_level: L2
research_area: []
task: []
method: []
dataset: []
code: "https://github.com/Sleigh-InSPECtor;artifact 归档 https://doi.org/10.6084/m9.figshare.32507811.v1(figshare artifact DOI,非论文 DOI)"
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

# InSPECtor: Improving SLEIGH Processor Specification Veracity via Proxy

## 0. 论文基础信息

| 项 | 内容 |
|---|---|
| 标题(原文) | InSPECtor: Improving SLEIGH Processor Specification Veracity via Proxy |
| 标题(中文) | InSPECtor:通过代理执行提升 SLEIGH 处理器规范的正确性 |
| 作者 | Michael Chesser, Paul Quirk, Douglas Cooke, Guy Farrelly, Surya Nepal, Damith C. Ranasinghe |
| 机构 | University of Queensland 与 CSIRO Data61(解析稿署名;具体单位归属解析稿未逐一分列) |
| 发表会议 | USENIX Security 2026 |
| 年份 | 2026 |
| DOI | unknown(解析稿未给出论文 DOI) |
| URL | https://www.usenix.org/conference/usenixsecurity26/presentation/chesser |
| PDF | 00-inbox/PDFs/2026-USENIX-InSPECtor__Improving_SLEIGH_Specification_Veracity_via_Proxy.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-USENIX-InSPECtor__Improving_SLEIGH_Specification_Veracity_via_Proxy.md |
| 代码/制品 | https://github.com/Sleigh-InSPECtor;artifact 归档 https://doi.org/10.6084/m9.figshare.32507811.v1(artifact DOI,非论文 DOI) |
| 阅读层级 | L2 |
| 主题相关性 | low(属二进制分析与处理器规范验证,与 KB 的加密流量分析主题无交集) |

> ⚠️ 标题不一致:解析稿封面页标题为 "InSPECtor: Improving SLEIGH Specification Veracity via Proxy"(缺 "Processor"),正文首页标题为 "InSPECtor: Improving SLEIGH Processor Specification Veracity via Proxy"。笔记采用正文章节标题版本,差异记录于 §12。

## 1. 一句话总结

面向 Ghidra SLEIGH 处理器规范(instruction decoding/semantics 的人工撰写产物)的自动化差分验证框架:用符号执行遍历规范的 constructor 生成合法指令、用 SMT 求解器求解操作数编码,再把反汇编器生成的 Pcode 与真实硬件(模拟器/开发板)的执行轨迹做等价比对,在 5 种 ISA 上暴露 589,713 条差异并归结为 125 个真实缺陷。

## 2. 摘要翻译

### 2.1 摘要原文(节选)

> Processor specifications underpin critical security and program-analysis tools such as disassemblers, decompilers, and emulators, yet, their correctness is rarely examined. Errors in specifications distort program behavior, obscure vulnerabilities, and enable analysis-evasion techniques. ... We design and implement a testing framework based on an automated oracle validation strategy by proxy. Our approach leverages the structure encoded in a specification itself to enumerate decodable instruction forms and generate targeted initial states. Then differentially test the successful decoding and emulation of those instructions by comparing emulators exercising the processor specification against hardware references.
>
> Applying InSPECtor across diverse, open-source specifications—x86-64, AArch64, ARM/Thumb, RISC-V, MSP430—embedding differences in specification styles, author preferences, and instruction set architecture designs, we uncovered over 38,920 discrepancies that led to 38,900 unique bugs with proposed fixes, identifying decoding and semantic defects as well as cross-vendor inconsistencies. We distill our findings into 8 concrete recommendations to drive future improvements.

(以上为解析稿 Abstract 的节录;完整原文见解析稿 Abstract 段。注意摘要中 "38,900 unique bugs" 与正文 "125 unique bugs" 的口径差异,见 §12 第 1 条)

### 2.2 中文完整翻译

处理器规范支撑着反汇编器、反编译器、模拟器等关键安全与程序分析工具,但其正确性却很少受到检验。规范中的错误会扭曲程序行为、掩盖漏洞,并催生分析规避技术。验证处理器规范并非易事。本工作是一项系统性工程,旨在对主要被 Ghidra 使用的开源 SLEIGH 语言规范实现系统化验证。我们设计并实现了一个基于"代理式自动化判定(oracle)"验证策略的测试框架:利用规范自身编码的结构来枚举可解码的指令形态,并生成有针对性的初始状态;随后,通过将被测规范驱动的模拟器与硬件参照系进行对比,对这些指令能否成功解码与模拟做差分测试。

在 x86-64、AArch64、ARM/Thumb、RISC-V、MSP430 等多种开源规范上应用 InSPECtor——这些规范在编写风格、作者偏好与 ISA 设计上差异显著——我们发现超过 38,920 条差异(discrepancy),并据此提出修复方案;这些差异指向解码缺陷、语义缺陷以及跨厂商不一致。我们把发现凝练为 8 条具体建议,以推动未来的改进。本工作凸显了规范正确性的重要性,并提供了一个实用工具来大幅提升 SLEIGH 处理器规范的保真度,从而增强下游安全与分析工具的可靠性。

## 3. 方法动机

### 3.1 研究背景

- Ghidra 等反汇编/反编译工具的核心是 SLEIGH 处理器规范:每条指令由一个 constructor(匹配模式 + 语义段)描述,语义段以 Pcode(一种中间表示)书写。
- 规范由人工维护、随 ISA 手册更新而演进,数量大、覆盖面广,人工审查成本极高。
- 反汇编器一旦出错,上层所有分析(漏洞挖掘、恶意代码分析、固件审计)都建立在错误基础之上,且错误往往静默。

### 3.2 现有方法的不足

| 现有思路 | 局限 |
|---|---|
| 手工编写测试用例 | 覆盖不了规范中成百上千的 constructor 组合,难以持续维护 |
| 与厂商汇编器/反汇编器交叉比对 | 厂商工具本身不一定提供 Pcode 语义,且难以覆盖全部指令形态 |
| 直接随机生成字节流测试 | 绝大多数随机字节不构成合法指令,几乎无法进入有效 constructor 分支 |
| 仅做解码一致性检查 | 忽略语义(Pcode)层面的错误,而语义错误占本次发现缺陷的多数 |

### 3.3 本文思路

把"规范正确性"转化为一个**可自动化的差分验证**问题:规范本身既是被测对象,也是测试用例生成器。利用 SLEIGH 的 constructor 结构做符号化遍历以保证生成语法合法指令,再用 SMT 求解反解出操作数编码(即"从语义域回到字节域"),最后把反汇编器 Pcode 模拟的结果与真实硬件执行结果对照,差异即候选缺陷。

### 3.4 问题发现路径

| 阶段 | 内容 |
|---|---|
| 现象观察 | SLEIGH 规范数量庞大且由人工维护,反汇编结果错误会静默污染后续分析 |
| 痛点提炼 | 缺少能自动、系统地覆盖规范全部 constructor 的测试生成与判定手段 |
| 问题转化 | 将"规范是否正确"转化为"同一条指令在反汇编器语义模型与真实硬件上是否产生等价结果"的差分判定问题 |
| 文献定位 | 位于反汇编器正确性验证/处理器规范测试这一支,与二进制分析工具的可信度研究相邻 |

### 3.5 科学假设

- 假设:如果能够从 SLEIGH 规范系统性地生成**语法合法**的指令(而非随机字节),并能自动判定反汇编语义与硬件的一致性,那么规范中的真实缺陷可以被规模化地、可复现地发现。
- 验证结果:在 5 种 ISA 上生成量达数万至数十万条指令(§6.1 Table 2),发现 589,713 条原始差异(§6.3 Table 3),归并后确认为 125 个真实缺陷(§6.4 Table 4),并与维护者完成披露与修复——假设得到支持。

## 4. 方法设计

### 4.1 总体架构

InSPECtor 由两个组件构成:

1. **GenSYS**:从 SLEIGH 规范生成指令测试用例(编码级)。
2. **JuxtaPlayer**:对每条生成的指令,分别用(I)反汇编器自身的 Pcode 语义解释执行、(II)真实硬件/模拟器执行,比较两者结果。

符号化遍历 → 约束求解 → 指令编码 → 双路执行 → 差异判定,构成完整闭环。

### 4.2 GenSYS:constructor 符号化遍历(Algorithm 1)

- 以 SLEIGH 规范的 constructor 为节点做符号化遍历,沿途累积约束,形成一个约束满足问题(CSP)。
- 约束分三类:**simple**(可直接求解的简单约束)、**complex**(需要组合求解的复杂约束)、以及**deferred**(延迟约束,需在后续阶段按上下文求解)。
- 通过 **attachments**(附加约束)把 constructor 的子字段与其父结构绑定。
- 使用 **overlap resolution**(重叠消解)与**phased decoding**(分阶段解码)处理 SLEIGH 中 constructor 的优先级/重叠问题,避免生成歧义编码。
- 引入 **prefix parsing**(前缀解析)以支持带前缀的指令形态,以及 **dynamic context**(动态上下文)以处理依赖运行时上下文的 constructor 条件。
- 设有 **traversal limit**(遍历上限)以约束搜索规模。

生成的编码约束最终交给 **Z3** 求解,得到具体操作数取值与指令字节序列。

### 4.3 初始状态的边界情况设计(Table 1)

GenSYS 不止生成指令编码,还从 Pcode 语义反推"有趣的输入状态":SOLVE 借助 Z3 的最小化/最大化能力生成约束允许的最小与最大编码,以暴露部分约束中的 off-by-one 错误(例如对 `:nop` 的 rd=rn 约束,Z3 会给出 rd=rn=0 与 rd=rn=7 两个编码)。

| Pcode 操作组 | 示例操作 | 触发的边界情况 |
|---|---|---|
| 加减 | INTADD, INTSUB | 溢出/下溢、结果为负、结果为零 |
| 乘除 | INTMULT, INTDIV, INTSDIV | 操作数为负/为零 |
| 零扩展/符号扩展 | INTZEXT, INTSEXT | 输入全 1 或全 0,输出为非负与负 |
| 布尔 | BOOLXOR, BOOLOR, … | 结果为真/假 |
| 位运算 | INTXOR, INTOR, … | 结果为零/非零 |
| 移位 | INTLEFT, INTRIGHT, … | 移位量过大、结果溢出、符号位置位 |
| 比较 | INTEQUAL, INTLESS, … | 操作数相等或相差 ±1 |
| 溢出条件 | INTCARRY, INTBORROW, … | 结果为真/假 |
| 浮点 | FLOATADD, FLOATSUB, … | 含特殊浮点值(如 NaN) |
| 分支 | CBRANCH | 条件为真及后续操作的路径约束 |

### 4.4 JuxtaPlayer:双代理执行

执行侧统一使用 **Icicle**(基于 SLEIGH 的模拟器,由本文作者团队此前的 ISSTA 2023 工作提出)执行规范中的 Pcode 语义;参照侧按 ISA 分两类:

| 被测 ISA | 参照系(硬件 oracle) | 调试/取数方式 |
|---|---|---|
| x86-64 | 硬件辅助虚拟机(KVM) | KVM;支持 VM 的硬件 |
| AArch64 | 硬件辅助虚拟机(KVM) | KVM;支持 VM 的硬件 |
| ARM/Thumb | 硬件辅助虚拟机(KVM) | KVM;支持 VM 的硬件 |
| MSP430 | MSP430FR5969 微控制器(真板) | JTAG 硬件调试器(该板无虚拟化扩展) |
| RISC-V | BeagleV-Ahead(四核 Xuantie C910,RV64GC,含 vector 扩展 0.7.1 草案) | Linux ptrace 调试(无虚拟化扩展) |

对每条测试指令,把寄存器/内存初值置为相同状态,执行后比较寄存器与内存的差异;不一致即记一条 discrepancy(差异)。

### 4.5 差异归并与缺陷判定

- 原始差异数量巨大(Table 3),直接上报无意义,因此做**聚类/归并**:把同源差异合并为一个 group。
- 再对 group 做**人工分诊(triage)**,判定是否为规范真实缺陷,并分类为 decoding / semantics ordering / incorrect semantics / aliasing 等。
- 解析稿给出分诊成本约为 **每个缺陷 4 小时**(§6.4 附近)。

### 4.6 消融与基线设计

- **消融(Table 6)**:分别测试 "Simple Only"(仅处理简单约束)、"Explicit Only"(仅显式约束)、"No Backtracking"(关闭回溯)三种削减配置下的准确率变化。
- **朴素基线**(在 x86-64 上对比):随机选择 constructor、填固定约束位、其余位随机,共生成并测试约 **1.1×10^7** 个测试用例、耗时 **8 小时**,却遗漏 **1249** 个 constructor(38% 未命中)与 **15** 个缺陷(占 x86-64 的 32 个根因缺陷的 47%)。GenSYS 在 x86-64 上的一次完整生成按 Table 2 三项耗时相加约为 32 分钟(491.99 + 1019.56 + 425.45 秒;**该合计为笔记按表推算,原文未直接给出**)。

## 5. 与其他方法对比

### 5.1 与随机 fuzzing 对比

随机字节流绝大多数不是合法指令,无法有效触达 constructor;GenSYS 通过符号化遍历 + SMT 求解保证生成合法编码,constructor 覆盖率显著更高(§6.1)。

### 5.2 与 PokeEMU / Fast PokeEMU 对比(解析稿 Related Work 明确对比)

PokeEMU 通过**符号执行模拟器二进制的解码逻辑**生成测试指令,与 GenSYS 的 constructor 遍历思路相似,但作用对象是模拟器二进制而非规范;Fast PokeEMU 通过把多条指令合并为一个测试用例来降低执行开销。相对而言:PokeEMU 因输入操作数取值不参与解码逻辑而**不生成触发边界情况的输入状态**;InSPECtor 追求 constructor 的完整覆盖,因而能发现**不可达 constructor** 中的缺陷。

### 5.3 与 EmuFuzzer / KEmuFuzz 对比

EmuFuzzer 用硬件参照测试 x86-64 CPU 模拟器,通过观察"变异某个字节是否触发异常"来推断指令内部结构;KEmuFuzz 扩展其支持虚拟化/hypervisor 测试,但沿用相同的指令生成方式,且需过滤分支指令、只识别字节级结构。二者均限于 x86-64 保护模式且不产生边界输入状态,与本文的规范驱动全覆盖路线不同。

### 5.4 与纯模拟器自我比对对比

仅在模拟器内比对只能验证"规范 vs 规范的解释器",无法发现规范与真实硬件语义的偏差;本文对 MSP430 与 RISC-V 使用真实开发板/微控制器作为真值来源。

### 5.5 本文的独特性

同时具备:(a) 以规范为驱动的合法指令生成;(b) 覆盖解码与语义两个层面;(c) 跨 5 种异构 ISA 的实证;(d) 与维护者的实际披露与修复闭环。

## 6. 实验表现与优势

### 6.1 测试用例生成能力(Table 2)

| ISA | 生成指令数 | 覆盖状态数 | 状态覆盖率 |
|---|---|---|---|
| x86-64 | 71,852 | 712,668 | 97% |
| AArch64 | 25,031 | 123,031 | 97% |
| ARM-Thumb | 30,709 | 207,999 | 96% |
| RISC-V | 9,725 | 38,481 | 99% |
| MSP430 | 7,436 | 124,712 | 90% |

另有 **460** 个 constructor 未生成任何测试用例(解析稿正文明确给出 460 这一总数),Table 2 将其分类为:N/A(仅使用不同 SLEIGH 配置)236、Redun.(冗余)210、Incom.(规范不完整导致的未被引用 constructor)7、Bugs(规范根因缺陷)7——合计数由笔记按表逐行相加得到。

### 6.2 覆盖率的量化背景

状态覆盖率在 4 种 ISA 上达到 96%–99%,MSP430 因规范规模与语义限制为 90%——说明"以规范为驱动"的策略基本可以穷尽规范的可达部分。

### 6.3 原始差异规模(Table 3)

原文表述为:JuxtaPlayer 在各架构上共发现 **589,713** 条 discrepancy(模拟器与硬件参照系输出状态之差),经分组后对应 **38,920** 个 unique constructor 组合。

| 架构 | Execs/s | Raw(原始差异) | Groups(分组) | Unimplemented | Exception | State |
|---|---|---|---|---|---|---|
| x86-64 | 176,404 | 349,897 | 18,827 | 9,159 | 2,467 | 2,059 |
| AArch64 | 3,723 | 52,833 | 7,342 | 5,127 | 1,451 | 312 |
| ARM/Thumb | 3,572 | 78,251 | 9,785 | 4,652 | 4,182 | 521 |
| RISC-V | 1,012 | 15,682 | 937 | 322 | 373 | 11 |
| MSP430 | 0.164 | 93,043 | 2,028 | 145 | 468 | 1,184 |
| Σ(笔记按表求和) | — | 589,706 | 38,919 | 19,405 | 8,941 | 4,087 |

Table 3 同时把 group 归类为 Unimplemented / Alignment / Exception / Flags / Float / PC / State 等类别(上表仅摘录其中三列)。按表各行求和为 589,706 与 38,919,与正文所述 589,713 / 38,920 相差个位,推断为原文表格舍入或笔误。

### 6.4 缺陷统计(Table 4)

| 缺陷类别 | 数量 |
|---|---|
| Decoding(解码错误) | 16 |
| Semantics Ordering(语义顺序错误) | 9 |
| Incorrect Semantics(语义错误) | 87 |
| Aliasing(别名问题) | 9 |
| **合计** | **125** |

按 ISA 分布为 32 / 23 / 17 / 18 / 35(解析稿 Table 4 给出各 ISA 计数)。

### 6.5 差异到缺陷的关联(Table 5)

Table 5 给出"差异数 ↔ 缺陷"的关联:多数缺陷对应少量差异 group,少数系统性缺陷对应大量差异——说明归并步骤是把 589,713 条原始差异压缩到可人工处理的 38,920 个 group、再压缩到 125 个缺陷的关键。

### 6.6 消融(Table 6)

Table 6 报告两项指标:ΔAcc(相对 GenSYS 的生成准确率下降,准确率 = 生成的指令中解码路径与目标 constructor 匹配的比例)与 Missed(GenSYS 能生成合法编码、而该配置找不到合法编码的 constructor 数)。

| 架构 | Simple Only ΔAcc / Missed | Explicit Only ΔAcc / Missed | No Backtracking ΔAcc / Missed |
|---|---|---|---|
| x86-64 | 16.7% / 995 | 12.3% / 65 | 0% / 0 |
| AArch64 | 13.2% / 98 | 13.7% / 79 | 0% / 11 |
| ARM/Thumb | 30.4% / 302 | 15.9% / 80 | 0% / 75 |
| RISC-V | 57.7% / 38 | 54.7% / 38 | 0% / 0 |
| MSP430 | 69.6% / 388 | 41.9% / 58 | 0% / 0 |

解读:仅求解 simple 约束的准确率损失最大(MSP430 -69.6%、RISC-V -57.7%);关闭重叠 constructor 的 implied 约束(Explicit Only)损失次之但各 ISA 仍 >12%;关闭回溯(No Backtracking)时 ΔAcc 为 0%(解码路径仍匹配),但会遗漏 constructor(AArch64 11 个、ARM/Thumb 75 个),即覆盖率下降而非准确率下降。

### 6.7 缺陷分类与建议

解析稿给出缺陷类别 I-1 至 I-15 的分类体系,并归纳出 **8 条**给规范维护者的建议(§5.1 附近),其中包括对别名、语义顺序、解码边界的处理规范。研究团队与上游规范的维护者进行了披露,并由维护者修复了相应问题。

## 7. 学习与应用

### 7.1 可借鉴的方法论

**"用被测对象自身的结构做测试生成"**——规范既是验证目标也是用例生成器。这一思路可迁移到任何"以声明式 DSL/规范驱动的系统"(如 IDS 规则、协议状态机、编解码器 schema)的验证。

### 7.2 差分测试的代理设计

使用**两个独立执行代理**(模拟器 vs 硬件)做真值交叉,避免单一实现的系统性偏差被误判为缺陷。对无硬件可用的场景,Icicle vs KVM 的双模拟器组合提供了可行的替代方案。

### 7.3 大规模差异的归并

589,713 → 38,920 → 125 的漏斗说明:差分测试的工程瓶颈不在"产生差异",而在**归并与分诊**;归并质量直接决定人工成本。

### 7.4 与 KB 主题的关系

本文属二进制分析/处理器规范验证,与知识库的加密流量分类、网站指纹、审查规避、恶意流量检测等主题**无交集**。其方法论(约束求解驱动的用例生成、双代理差分)虽具通用性,但不构成流量分析领域可直接引用的对比工作。

### 7.5 可复用性评估

代码开源(github.com/Sleigh-InSPECtor),artifact 归档于 figshare;框架与 Ghidra 生态强绑定,迁移到其他领域需要替换"规范解析"与"代理执行"两端。

## 8. 总结

### 8.1 核心思想(≤20 字)

用规范生成合法指令,与真实硬件差分验证。

### 8.2 速记版 Pipeline

1. 解析 SLEIGH 规范,符号化遍历 constructor 并累积约束;
2. Z3 求解约束,反解出合法的指令编码(操作数具体取值);
3. JuxtaPlayer 双路执行:反汇编器 Pcode 语义 vs 模拟器/真实硬件;
4. 比较寄存器/内存结果,输出差异(discrepancy);
5. 差异归并为 group → 人工分诊 → 确认真实缺陷并披露。

## 9. Obsidian 知识链接

### 9.1 概念页

本论文不触及 kb_reference C 节白名单中的任何 concepts 页面(白名单聚焦加密流量分类/指纹/审查规避/恶意流量检测;本文属二进制分析与处理器规范验证),故不建立概念 wikilink。

### 9.2 方法页

不触及白名单 methods 页面(contrastive-learning, convolutional-network, graph-neural-network, multi-modal-fusion, pre-training-finetuning, self-supervised-learning, state-space-model, transformer 均不适用于本文)。

### 9.3 任务页

不触及白名单 tasks 页面。

### 9.4 综述页

不触及白名单 surveys 页面。

### 9.5 对比表

不建议链入 `method-comparison-table` / `dataset-comparison-table` / `open-source-registry`:前者收录流量分析方法、后者收录流量数据集,本文两者均不属于。若未来建立"二进制分析工具验证"主题页,可考虑纳入。

## 10. 证据记录

| 结论 | 证据位置 |
|---|---|
| 5 种 ISA 的生成指令数与状态覆盖率(71,852/25,031/30,709/9,725/7,436;97%/97%/96%/99%/90%) | §6.1 Table 2 |
| 原始差异合计 589,713,x86-64 占 349,897,分组后 38,920 个 unique constructor 组合 | §6.3 Table 3 |
| 125 个缺陷,其中 incorrect semantics 87、decoding 16、ordering 9、aliasing 9;按 ISA 为 32/23/17/18/35 | §6.4 Table 4 |
| 朴素基线(x86-64)1.1×10^7 用例、8 小时、遗漏 1249 constructor(38%)与 15 缺陷(32 个 x86-64 根因缺陷的 47%) | §6.6 附近 "Comparison to naive approach" |
| 5 种 ISA 的生成耗时(Traversal/Solving/State Gen 三段)与缺失 constructor 四类分解(合计 460) | §6.1 Table 2 |
| 消融:Simple Only / Explicit Only / No Backtracking 的 ΔAcc 与 Missed | §6.6 Table 6 |
| 分诊成本约 4 小时/缺陷 | §6.4 |
| 8 条给规范维护者的建议 | §5.1 |
| 460 个未生成任何测试用例的 constructor | §6.1 |

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-USENIX-InSPECtor__Improving_SLEIGH_Specification_Veracity_via_Proxy.pdf
- MinerU Markdown：02-parsed-markdown/2026-USENIX-InSPECtor__Improving_SLEIGH_Specification_Veracity_via_Proxy.md

## 12. 后续问题

1. **摘要与正文口径不一致**:摘要原文为 "we uncovered over 38,920 discrepancies that led to 38,900 unique bugs with proposed fixes",即把 38,900 称作 "unique bugs";而正文(§6.4)明确为"对 discrepancy 人工分诊后发现 **125** 个 unique bugs(bug 定义为某 ISA 中被修复的唯一根因)",并说明 Table 3 的 38,920 是"分组后的 unique constructor 组合数"。因此摘要中的 38,900 很可能指去重后的 discrepancy 数、而非经分诊确认的缺陷数——引用本文缺陷数量时应使用正文的 **125**,不要把摘要的 38,900 当作缺陷总数。
2. **标题不一致**:封面页标题缺 "Processor" 一词(见 §0 提示),需以正式出版版本为准。
3. Table 3 的 group 分类计数按表逐行相加为 589,706 / 38,919,与正文 589,713 / 38,920 各有个位差;本笔记同时列出表值与正文值,引用时建议以原文表述为准并核对原表。
4. **聚合提示**:本文与 KB 主题无交集,聚合时请勿计入 traffic-* 主题统计(处理方式与同批 QUIC fuzzing 类论文一致)。

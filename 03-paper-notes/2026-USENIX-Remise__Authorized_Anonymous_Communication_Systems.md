---
type: paper
title_original: "Remise: Authorized Anonymous Communication Systems"
title_cn: "Remise:可授权匿名通信系统"
authors: [Rohan Ravi, Paritosh Shukla, Adithya Vadapalli]
year: 2026
venue: "USENIX Security 2026"
doi: "unknown"
url: "https://www.usenix.org/conference/usenixsecurity26/presentation/ravi-rohan"
pdf: "00-inbox/PDFs/2026-USENIX-Remise__Authorized_Anonymous_Communication_Systems.pdf"
mineru_md: "02-parsed-markdown/2026-USENIX-Remise__Authorized_Anonymous_Communication_Systems.md"
status: deep-analyzed
reading_level: L3
research_area: ["anonymous communication", "private information retrieval", "DORAM"]
task: ["authorized anonymous bulletin board", "anonymous communication channel"]
method: ["two-server DORAM", "secret-shared authorization tokens", "oblivious access control"]
dataset: ["2^26-entry database prototype", "PACL comparison"]
code: "https://zenodo.org/records/20438384(artifact 归档,非论文 DOI)"
relevance: low
created: "2026-09-19"
updated: "2026-10-10"
---

# Remise: Authorized Anonymous Communication Systems

## 0. 论文基础信息

| 项 | 内容 |
|---|---|
| 标题(原文) | Remise: Authorized Anonymous Communication Systems |
| 标题(中文) | Remise:可授权匿名通信系统 |
| 作者 | Rohan Ravi, Paritosh Shukla, Adithya Vadapalli |
| 机构 | IIT Kanpur(印度理工学院坎普尔分校) |
| 发表会议 | USENIX Security 2026(第 35 届 USENIX Security Symposium,2026-08-12/14,Baltimore, MD, USA) |
| 年份 | 2026 |
| DOI | unknown(解析稿未给出论文 DOI) |
| URL | https://www.usenix.org/conference/usenixsecurity26/presentation/ravi-rohan |
| PDF | 00-inbox/PDFs/2026-USENIX-Remise__Authorized_Anonymous_Communication_Systems.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-USENIX-Remise__Authorized_Anonymous_Communication_Systems.md |
| 代码/制品 | https://zenodo.org/records/20438384(artifact 归档,非论文 DOI) |
| 资助 | Anusandhan National Research Foundation(ANRF);另获 Satish and Kamlesh Agarwal 差旅资助 |
| AI 使用声明 | Acknowledgments 中说明:作者使用生成式 AI 工具润色文字、改进行文并修正拼写/语法/表述 |

## 1. 一句话总结

Remise 用 **分布式不经意 RAM(DORAM)** 取代传统 DPF 式匿名通信中的"客户端提交 DPF 密钥 + 服务端审计"范式:由两个(不共谋的)服务端自行生成标准基向量份额,从而天然免审计;同时把授权令牌以**秘密共享**形式存放在服务端,实现可遗忘的授权校验与授权更新,支持公告板(RemiseBB)与通信信道(RemiseCC,可授予/撤销读权限)两种模式,在 2^26 数据库上把写请求有效性校验的在线服务端时间较 PACL(S&P 2023)提升近 80×。

## 2. 摘要翻译

### 2.1 摘要原文

> We present Remise, a two-server authorized anonymous communication system built on Distributed Oblivious RAM (DORAM). Remise supports two modes of operation: (i) an anonymous bulletin board, where messages are publicly revealed at the end of each epoch without linking senders to messages, and (ii) anonymous communication channels, where messages remain secret-shared, and writers selectively grant and revoke read access to chosen readers. In both modes, the two servers execute read and write operations without learning which indices are accessed, which authorization tokens are used, or which relationships exist between writers and readers, assuming no collusion between the servers. A central contribution of Remise is a lightweight and efficient access-control mechanism. Authorization tokens are maintained in secret-shared form across the two servers, enabling oblivious verification and updates, while preventing leakage even under client–server collusion. Unlike prior DPF-based systems, Remise provides built-in auditing by having the semi-honest servers generate standard-basis vector shares internally, eliminating the need for server-side DPF validity checks. We implement a prototype of Remise and evaluate it under realistic network conditions. Our experiments show an 80× improvement in online server time for request validity check when compared to PACL (IEEE S&P 2023) for large database size.

### 2.2 摘要中文翻译

我们提出 Remise,一个基于分布式不经意 RAM(DORAM)的两服务端可授权匿名通信系统。Remise 支持两种运行模式:(i)匿名公告板——消息在每个 epoch 结束时公开揭示,但不把发送者与消息关联;(ii)匿名通信信道——消息保持秘密共享,写者可有选择地向特定读者授予与撤销读权限。在两种模式下,两个服务端执行读/写操作时都不会得知访问了哪些索引、使用了哪些授权令牌、或写者与读者之间存在何种关系(假设服务端之间不共谋)。Remise 的核心贡献是一套轻量且高效的访问控制机制:授权令牌以秘密共享形式维护在两个服务端之间,从而支持不经意校验与不经意更新,并在客户端–服务端共谋时仍防止泄漏。与既有基于 DPF 的系统不同,Remise 让半诚实服务端自行在内部生成标准基向量份额,从而内建审计能力,免除了服务端的 DPF 有效性检查。我们实现了 Remise 原型并在真实网络条件下评测;实验显示,在大数据库规模下,其请求有效性校验的在线服务端时间相比 PACL(IEEE S&P 2023)提升约 80×。

## 3. 方法动机

### 3.1 作者为什么提出这个方法?

匿名通信系统通过把身份与消息解耦来保护用户免受监控与报复,对记者、吹哨人、活动人士尤为关键。作者沿用 Sasy 与 Goldberg 的分类,把匿名通信系统分为四类:发送者不可关联广播系统(SUBS)、发送者不可关联消息系统(SUMS)、关系不可观测系统(RUS)、通信不可观测系统(CUS);本文聚焦前三类。

本文提出并研究了一种此前未被研究的 RUS 子类——**发送者匿名通信信道(Sender Anonymous Communication Channels)**:一组发送者在两方共享的秘密留言板上发帖,但两方从不重构消息以公之于众;写者把读权限授予自选的读者,并可随时撤销。作者把它类比为"匿名 Substack/博客":订阅者是获得读授权的读者,作者(写者)由服务提供者授予写权限,并对自己那片空间拥有"所有权"。

### 3.2 现有方法的痛点和不足

沿 DPF 世系的匿名通信系统(Riposte、Express、Sabre、Spectrum、PACL)在执行一次写请求前通常要过两道检查:(i) DPF 是否有效(即能否展开为标准基向量的份额,称为 **审计/audit**);(ii) 用户是否有权在该索引上访问(称为 **授权/authorization**)。逐一来看:

| 系统 | 机制要点 | 主要不足 |
|---|---|---|
| Riposte | 公告板模型,写者在随机位置创建 DPF;服务端每 epoch 重构并发布消息 | 用 $O(\sqrt{n})$ 规模的 DPF(为让审计高效);为把写入碰撞概率压到 5%,服务端规模需为待发布消息数的 19.5 倍;**不提供授权** |
| Express | 每个接收者分配 $\lambda=128$ 位邮箱 ID,写者针对 ID 生成 DPF;用 SNIP 做审计 | 审计需把每条 DPF 在所有已注册邮箱 ID 上求值,工作量与邮箱数线性相关 → 恶意客户端提交畸形 DPF 可造成 DoS;服务端知晓全部邮箱 ID,**服务端–客户端共谋即可导出并泄漏写授权** |
| Sabre | 用 PRF 做邮箱 ID 校验(写者持有 $\mathrm{PRF}(k,i^*)$ 的份额,服务端用 MPC 计算并做相等性检查);$O(\log n)$ 审计防 DoS | MPC 要求底层密码低乘法深度;服务端知道 $k$,故对任意 $i$ 都能算出 $\mathrm{PRF}(k,i)$,**同样不抗服务端–用户共谋** |
| Spectrum | 每个广播者分配一个"信道"避免写碰撞;盲访问控制;带 Blame-Game 协议防恶意服务端拒服务 | 抗服务端–写者共谋泄漏授权材料仅在**离散对数困难**假设下成立(计算性而非信息论);**验证密钥向量的任何修改对服务端直接可见**,无法做可遗忘的授权更新 |
| PACL(S&P 2023) | 面向函数秘密共享的访问控制;服务端持有验证密钥向量 $\Lambda=\{g^{\alpha_1},\dots,g^{\alpha_n}\}$;用 Schnorr 证明替换基于指数的检查;第二种构造"inclusion predicate"支持每索引多个访问密钥(验证密钥的 $n\times\ell$ 矩阵,用两个 DPF 分别选行与选列) | 未提供**授权更新隐私**(修改密钥向量对服务端可见) |
| Myco(ORAM 路线) | 非对称两服务端模型,服务端模拟 ORAM 的客户端与服务端,每次访问服务端工作量 polylog,优于 PIR/DPF 路线 | **不提供服务器强制的访问控制**:任何客户端可读任意位置,必须靠试解密(trial-decrypt)识别自己的条目 |

### 3.3 论文的研究假设或核心直觉

三条核心直觉:

1. **用 DORAM 换掉"客户端提交 DPF 密钥"这一步 → 内建审计。** 在既有 DPF 式系统中,客户端提交 DPF 密钥,服务端必须先做审计确认这些密钥会展开为合法 1-hot 向量份额,否则畸形 DPF 会污染整个数据库。而 DORAM(如 Floram、Duoram)中**标准基向量的份额由服务端自己生成**,这一步计算就从"可能作恶的客户端"转移到了服务端,审计需求随之消失。
2. **授权令牌以秘密共享形式跨服务端保存 → 抗共谋的授权保密。** Express/Sabre 明文保存授权材料,共谋服务端可泄漏;Spectrum/PACL 只做到计算性隐藏(离散对数假设);Remise 让两个服务端各持令牌的一份加法份额,只要至少一个服务端半诚实,授权秘密就是**信息论**隐藏的。
3. **对令牌数据库做 DORAM 更新 → 授权可遗忘地更新与撤销。** 由于令牌秘密共享存储,写者更新自己索引的读令牌列表时只需一次不经意的 DORAM 更新,**服务端看不出被改的是哪条授权状态**——这是 Spectrum/PACL 做不到的。

### 3.4 问题发现路径

作者从 DPF 世系(Riposte → Express → Sabre → Spectrum → PACL)的逐代演进出发梳理"审计 + 授权"两道检查的代价结构,发现三个未被同时满足的缺口:(a) 授权秘密的隐藏强度(信息论 vs 计算性 vs 无);(b) 授权状态能否不经意更新;(c) 审计的计算负担能否从客户端侧移除。三者分别对应本文的三个 contribution。

### 3.5 科学假设形成

可检验的假设:**若把授权令牌存入秘密共享的令牌数据库、并用 DORAM 实现不经意读写,则可以在保持全流程不经意性的同时,把"审计 + 授权"合并为一次轻量的 MPC 相等性检查(常数轮通信),并在大数据库规模下胜过需要求值可验证 DPF 的 PACL 方案。** 第 6 节的实验设计正是围绕"何时交叉(crossover)"来检验该假设。

## 4. 方法设计

### 4.1 方法整体流程

Remise 由两个不共谋的服务端 $\mathtt{S}_0$、$\mathtt{S}_1$ 组成,有两种实例化:

- **RemiseBB(匿名公告板)**:授权写者向预先分配的槽位匿名发帖,公告板周期性重构并发布;所有写请求(真实 + 掩护流量)对服务端与网络观察者不可区分,从而切断写者与已发布消息的关联。
- **RemiseCC(匿名通信信道)**:消息同样由写者投递,但**服务端从不重构**;写者可有选择地授予/撤销读权限,只有被授权读者能从给定索引读出消息。

用户分两类(写者、读者),另有第三方提供掩护流量:写的掩护流量是**零消息更新**(每条写请求先做 EQZ 零检查,ΔM=0 即通过),读的掩护流量是**对保留哑索引 $i_{\mathrm{read}}$ 的合法读请求**。对服务端而言,掩护请求与真实访问请求是**信息论不可区分**的,用于扩大匿名集。

三种数据库:$\mathbf{D}$(消息板,大小 $N$,$\mathtt{S}_0/\mathtt{S}_1$ 持加法份额)、WRTOK(写授权令牌库,只读,$\text{WRTOK}[i]$ 编码写第 $i$ 位所需的写令牌)、RDTOK(仅 RemiseCC,读授权令牌库,每索引存 $m$ 个令牌,持有其中任意一个即可读该索引)。另有 SETUPDB(setup 期间写者发布公钥的匿名公告板,服务端持加法份额)与 ACCESSDB(setup 末尾发布的数据库,每写者从中解密自己的 $(i^*,\ell)$)。

**威胁模型**:客户端(写者/读者/掩护流量)**完全不可信**,可任意偏离协议、可与其他客户端或恶意服务端共谋;授权令牌按**持有者凭证(bearer credential)**处理,谁持有某索引的合法读/写令牌谁就能行使该能力。隐私性要求**服务端之间不共谋**;完整性要求**两个服务端都遵守协议**(即服务端半诚实)。假设存在全局网络对手观察所有客户端–服务端通信,假设存在 PRG/PRF,并假设客户端与每个服务端之间有安全信道。

### 4.2 详细 Pipeline

**Setup 阶段(Protocol 5,三阶段):**

- *Stage 1 写者注册*:写者生成密钥对 $(pk,sk)$,用 **Riposte 式匿名广播**(理想功能 $\mathcal{F}_{AB}$)把 $pk$ 写到 SETUPDB 的随机位置;掩护流量在同一信道上广播零消息,故腐化服务端无法区分注册者与掩护参与者。注册仅在一个固定窗口内被接受。
- *Stage 2 服务端分配*:窗口结束后服务端重构 SETUPDB,对每个合法 $pk$ 用双方约定的随机函数 $\mathrm{ASSIGN}()$ 选一个未占用的新索引 $i^*$;随后 $\mathtt{S}_b$ 独立采样随机串 $\ell_b \leftarrow \{0,1\}^\lambda$(互不知晓对方份额),令 $\ell=\ell_0+\ell_1$ 即 $i^*$ 的写授权令牌,本地写入 $\text{WRTOK}_b[i^*]\leftarrow \ell_b$,并计算 $c_b\leftarrow \mathrm{ENC}_{pk}(i^*\|\ell_b)$;服务端把 $(c_0\|c_1)$ 写到 ACCESSDB 中 $pk$ 原来所在的位置并发布 ACCESSDB。最后把 WRTOK 的加法份额转换为双重加密的只读库 $\text{WRTOK}^{\mathrm{RO}}$:$\mathtt{S}_b$ 采样密钥 $k_b$、构造向量 $R_b[i']=\mathrm{PRF}(k_b,i')$,把 $(\text{WRTOK}_b+R_b)$ 发给对方,双方存放 $\text{WRTOK}^{\mathrm{RO}}\leftarrow \text{WRTOK}_0+R_0+\text{WRTOK}_1+R_1$。
- *Stage 3 写者取钥*:写者取回 ACCESSDB[i],用 $sk$ 解密得到 $(i^*,\ell_0,\ell_1)$,重构 $\ell\leftarrow \ell_0+\ell_1$(即其写授权令牌)。

注册沿用 Riposte 的写碰撞风险(非零失败概率);由于注册只发生一次,可通过超配数据库让失败概率可忽略(例如 $2.7N$ 的表容忍双向碰撞时有约 95% 成功注册),也可采用 Riposte 的碰撞恢复方法。

**运行阶段:** 写(Protocol 6)→ 更新读授权(Protocol 7,仅 RemiseCC)→ 读(Protocol 8,仅 RemiseCC)。RemiseBB 中**不存在"读"这一概念**(它是广播系统,消息被发布)。

### 4.3 模型结构或系统模块

| 模块 | 作用 | 在本方案中的角色 |
|---|---|---|
| 加法秘密共享 | 把秘密分给两方,少于阈值者学不到任何信息 | $x^{\mathrm{AS}}$ 记 $x$ 的加法共享;数据库 $\mathbf{D}$、WRTOK、RDTOK 全部以份额形式由 $\mathtt{S}_0/\mathtt{S}_1$ 持有 |
| Du-Atallah 乘法($\mathcal{F}_{\mathrm{MULT}}$) | 份额上的乘法(Beaver 方法的变体) | 用于 Protocol 8 的 $m$ 路 OR 组合;原本是 (2+1) 方协议,可用 OT 产生关联随机数转成两方协议 |
| EQZ($\mathcal{F}_{\mathrm{EQZ}}$) | 判断秘密共享值是否为零,输出比特的份额($b=1 \iff x=0$) | 全部"检查"的原子操作:写请求的零消息检查与写令牌检查、读请求的 $m$ 个读令牌检查 |
| DOROM($\mathcal{F}_{\mathrm{DOROM}}$) | 分布式只读不经意内存:对 setup 后固定的库做不经意读 | 用 **Floram** 实例化;读 WRTOK(写令牌的取得) |
| DOWOM($\mathcal{F}_{\mathrm{DOWOM}}$) | 分布式只写不经意内存:不经意更新秘密共享数据库 | 用 **Floram** 实例化;RemiseBB 中写 $\mathbf{D}$ 即一次 write-only 访问 |
| DORAM($\mathcal{F}_{\mathrm{DORAM}}$) | 同时支持不经意读与不经意写 | 用 **2P-Duoram** 实例化;RemiseCC 中写 $\mathbf{D}$、更新 RDTOK |
| DPF 预处理 | 生成 DORAM 所需的标准基向量份额 | 服务端在预处理阶段自行生成 DPF,在线阶段以常数通信把 DPF 调整到正确的索引与值(详见 Duoram 论文 §4.1 的 (2+1) 方协议,两方变体用 OT 产生乘法三元组) |
| Riposte 式匿名广播($\mathcal{F}_{AB}$) | 隐藏"谁发布了哪个 $pk$" | 仅用于 setup 的写者注册 |

**两种实例化与两种变体的关系**:$\text{WriteAuth}$ 由 WRTOK 实现(一个 DOROM),$\text{ReadAuth}$ 由 RDTOK 实现(一个 DORAM,每索引存 $m$ 个令牌的列表,持有其中任意一个即可读 $\mathbf{D}[i]$)。此外 **RemiseBB (Sabre)** 变体允许**不依赖 DORAM** 做授权:取 PRF $F:\{0,1\}^\lambda\times I\to\{0,1\}^\lambda$,索引 $i$ 的授权令牌定义为 $\tau_i=F_k(i)$($k$ 为两服务端共知),客户端提交索引份额与令牌份额,服务端在 MPC 下联合求值 $F_k(i^*)$ 并做相等性检查。该检查的计算与通信复杂度均为**常数**。代价是:与 Sabre 一样,服务端与客户端的共谋不在其威胁模型内(服务端知道 $k$,可对任意索引算出合法令牌)。

### 4.4 公式、算法和机制解释

**交互式理想功能 $\mathcal{F}_{\mathrm{Remise}}$**(状态:$\text{WriteAuth}:[N]\to\{0,1\}^\lambda\cup\{\perp\}$、$\text{ReadAuth}:[N]\to 2^{\{0,1\}^\lambda}$、$\mathbf{D}:[N]\to\mathcal{M}$、时钟 $T_{clock}$、布尔量 `setup_done`/`window_open`)。腐化模型:PPT 对手**静态**腐化至多一个服务端 $\mathtt{S}_b$ 与任意真子集客户端 $W_C\subsetneq W$。四个接口:

| 接口 | 输入 | 接受条件 | 泄漏 |
|---|---|---|---|
| Setup.Reg$(w,\text{mode})$ | 用户 $w$ 与 mode $\in\{$register, cover$\}$ | 窗口开启 | LeakLog 追加 $(\text{Participant}:w)$ |
| Write$(i^*,\Delta M,\omega)$ | 目标索引、值更新、写授权令牌 | $\Delta M=0$(掩护)或 $\omega=\text{WriteAuth}[i^*]$ | LeakLog 追加 $(\text{write}:c,\text{out})$;接受则 $\mathbf{D}[i^*]\mathrel{+}=\Delta M$ |
| UpdAuth$(i^*,\Delta R,\omega)$ | $\Delta R\leftarrow R'-R$ 为读令牌列表的逐元素差 | $\omega=\text{WriteAuth}[i^*]$ | LeakLog 追加 $(\text{updauth}:c,\text{out})$;接受则 $\text{ReadAuth}[i^*]\mathrel{+}=\Delta R$ |
| Read$(i^*,t)$ | 目标索引与读授权令牌 | $t\in\text{ReadAuth}[i^*]$ | LeakLog 追加 $(\text{read}:c,\text{out})$;接受则读者学到 $\mathbf{D}[i^*]$ |

Setup 阶段结束后 LeakLog 中还含 $(\text{assigned}:R)$,$R$ 为**无序**的已分配索引集合——这是 Setup 匿名性的关键:对手知道"哪些索引被分配了",但不知道"谁拿到了哪个"。

**Protocol 6(WRITE):** w 计算 $\Delta M\leftarrow M'-M$(w 拥有该索引,假定始终知道当前值 $M$),把 $(i^{*\mathrm{AS}_b},\Delta M^{\mathrm{AS}_b},\omega^{\mathrm{AS}_b})$ 发两个服务端;服务端做 $z^{\mathrm{AS}}\leftarrow\mathrm{EQZ}(\Delta M^{\mathrm{AS}})$(零消息检查)、$F^{\mathrm{AS}}\leftarrow\text{WRTOK}^{\mathrm{RO}}[i^{*\mathrm{AS}}]$(DOROM 读)、$\text{auth}^{\mathrm{AS}}\leftarrow\mathrm{EQZ}(F^{\mathrm{AS}}-\omega^{\mathrm{AS}})$(令牌相等性)、$\text{audit}^{\mathrm{AS}}\leftarrow\text{auth}^{\mathrm{AS}}\lor z^{\mathrm{AS}}$(MPC OR),重构 $\text{audit}\leftarrow\mathrm{REC}(\text{audit}^{\mathrm{AS}})$;若为 1 则 $\mathbf{D}^{\mathrm{AS}}[i^{*\mathrm{AS}}]\mathrel{+}=\Delta M^{\mathrm{AS}}$,否则拒掉且不写。写这一步在 RemiseBB 中是 write-only 访问,在 RemiseCC 中是 DORAM 写。**OR 的作用**:让"零消息"与"授权通过"二者之一成立即可,掩护流量因此无需令牌。

**Protocol 7(UPDATE READ AUTHORIZATION,仅 RemiseCC):** 授予读权限分两步——写者经带外渠道把读令牌发给读者,再把"持有该令牌可读 $i^*$"这一事实不经意地告知服务端。w 构造新列表 $R'_{i^*}=\{t_1,\dots,t_m\}$,算 $\Delta R_{i^*}\leftarrow R'_{i^*}-R_{i^*}$,把 $(i^{*\mathrm{AS}},\Delta R_{i^*}^{\mathrm{AS}},\omega^{\mathrm{AS}})$ 发服务端;服务端做 $F^{\mathrm{AS}}\leftarrow\text{WRTOK}^{\mathrm{AS}}[i^{*\mathrm{AS}}]$、$\text{check}^{\mathrm{AS}}\leftarrow\mathrm{EQZ}(F^{\mathrm{AS}}-\omega^{\mathrm{AS}})$、$\text{check}\leftarrow\mathrm{REC}(\text{check}^{\mathrm{AS}})$,通过则 $\text{RDTOK}^{\mathrm{AS}}[i^*]\mathrel{+}=\Delta R_{i^*}^{\mathrm{AS}}$(DORAM 更新)。**撤销**即把某令牌从 $\text{RDTOK}[i^*]$ 的列表中移除,同样只需一次不经意更新,**无需重新加密已存消息,也不暴露改的是哪条授权状态**。

**Protocol 8(READ,仅 RemiseCC):** 读者发 $(i^{*\mathrm{AS}},t^{\mathrm{AS}})$($t$ 为写者给的读令牌);服务端做 $T^{\mathrm{AS}}\leftarrow\text{RDTOK}^{\mathrm{AS}}[i^{*\mathrm{AS}}]$,解析 $T^{\mathrm{AS}}=\{t_1^{\mathrm{AS}},\dots,t_m^{\mathrm{AS}}\}$,对每个 $i$ 算 $\text{check}_i^{\mathrm{AS}}\leftarrow t_i^{\mathrm{AS}}-t^{\mathrm{AS}}$ 与 $z_i^{\mathrm{AS}}\leftarrow\mathrm{EQZ}(\text{check}_i^{\mathrm{AS}})$,再做 $\text{auth}^{\mathrm{AS}}\leftarrow\bigvee_{i=1}^{m}z_i^{\mathrm{AS}}$、$\text{auth}\leftarrow\mathrm{REC}(\text{auth}^{\mathrm{AS}})$;通过则两服务端把 $\mathbf{D}^{\mathrm{AS}}[i^{*\mathrm{AS}}]$ 的份额发给读者,读者算 $\text{read}\leftarrow\text{read}^{\mathrm{AS}}_0+\text{read}^{\mathrm{AS}}_1$;不通过则直接丢弃请求。**注**:读请求同样先做 $m$ 路 EQZ 检查,**未授权请求不会进入昂贵的内存访问阶段**,这正是后文"未授权比例上升反而提高吞吐"的原因。

**两个保留索引(掩护流量用):** $i_{\mathrm{upd}}$ 的写授权令牌公开,任何愿提供掩护的用户都可用 Protocol 7 更新 $\text{RDTOK}[i_{\mathrm{upd}}]$;服务端在 setup 阶段**不分配** $i_{\mathrm{upd}}$。$i_{\mathrm{read}}$ 的读令牌 $\text{RDTOK}[i_{\mathrm{read}}]$ 公开、用于发起读掩护,但 $\text{WRTOK}[i_{\mathrm{read}}]$ **必须保密**,以防恶意用户用 Protocol 7 更新它。

**安全定理:** 定理 1(Setup 匿名性)在 PRF 安全、加密 IND-CPA、$\mathcal{F}_{AB}$ 为理想匿名广播的假设下成立;定理 2(Write/UpdAuth/Read 隐私)在 $(\mathcal{F}_{\mathrm{DOROM}},\mathcal{F}_{\mathrm{DOWOM}},\mathcal{F}_{\mathrm{DORAM}},\mathcal{F}_{\mathrm{EQZ}},\mathcal{F}_{\mathrm{MULT}})$-混合模型中,Protocols 6/7/8 针对**腐化一个服务端 + 任意客户端子集**的半诚实对手安全实现对应接口。证明方式:模拟器按 LeakLog 逐条用底层混合功能的模拟器合成腐化服务端的视图,模拟出的份额均匀分布、与真实执行计算不可区分。

### 4.5 方法优势

1. **内建审计**:服务端自行生成标准基向量份额,不需要服务端侧的 DPF 有效性检查;Table 1 中 Remise 的 Server Audit Work 一栏为 "—"(其余系统均为 $O(N)$ 或 $O(L)$ 量级)。Riposte/Express/Spectrum 的"审计 + 授权"两道检查被合并为一次 EQZ,故 Table 1 用 "†"(审计与授权统一)标注 Spectrum/PACL,而 Remise 直接消掉了审计列。
2. **授权秘密隐藏是信息论的**:令牌以秘密共享保存,只要一个服务端半诚实即成立;Spectrum/PACL 只到"离散对数困难"的计算性隐藏,Express/Sabre 则完全不隐藏。
3. **授权更新隐私 + 可撤销**:$\text{RDTOK}$ 的不经意 DORAM 更新让服务端看不出哪条授权状态被改;Spectrum/PACL 的验证密钥向量更新对服务端直接可见。
4. **客户端请求更小**:客户端不再发送 DPF 密钥,而是发送索引的秘密份额(需 $\log L$ 位,$L$ 为注册写者数),写请求带宽见 Table 3。
5. **抗 DoS**:授权与审计都在 MPC 中完成且与数据库规模无关(RemiseBB(Sabre) 的授权检查甚至与数据库规模完全无关),畸形输入不会触发昂贵的 DPF 求值。

### 4.6 方法不足(见 §4.2 Limitations)

1. **并发读写不保证线性一致**:RemiseCC 对同一位置的并发读与写,两个服务端可能观察到不同的操作顺序,读者可能重构出"一份旧份额 + 一份新份额"的不一致值。这只影响读一致性,不损害写正确性、授权或隐私;待两个服务端都处理完写之后数据库会收敛到正确状态。作者指出这是无协调的异步秘密共享存储系统的常见问题(Express、Sabre 亦如此),Riposte/Spectrum 用"把读限制在已完成 epoch"回避;锁或版本号能提供更强一致性但会增加延迟并可能泄漏访问模式,留作未来工作。
2. **令牌带外分发**:RemiseCC 中写者授予读权限时必须经带外信道分发新令牌。作者指出 Sabre/Express/Spectrum 同样要求读者先从外部取得共享秘密或授权材料;设计可扩展、保护隐私且无需可信 setup 信道的授权分发机制仍是开放问题。
3. **无 Blame-Game,服务端仅半诚实**:与 Spectrum 不同,Remise 不提供 Blame-Game 协议,因此**恶意服务端可以丢弃诚实客户端的写请求**;安全性以两个服务端都半诚实为前提。
4. **RemiseCC 的成本因子 $m$**:读与更新读授权的本地计算为 $O(n)+O(n\cdot m)$、带宽为 $O(\lg n)+O(m)$,随每索引令牌数 $m$ 增长(见 Table 2)。
5. **RemiseBB(Sabre) 的共谋假设被放宽**:服务端知道 PRF 密钥 $k$,服务端–客户端共谋可平凡地伪造任意索引的合法令牌,故该变体的共谋不在威胁模型内;作者另注明把 RemiseCC 与 Sabre 结合得不到同时保持写者–读者不可关联的高效构造。
6. **注册碰撞**:setup 的匿名广播沿用 Riposte,存在非零注册失败概率(靠超配或碰撞恢复缓解)。

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

| 维度 | 既有 DPF 式系统(Riposte/Express/Sabre/Spectrum/PACL) | Remise |
|---|---|---|
| 谁生成 1-hot 份额 | 客户端生成 DPF 密钥并提交,服务端求值 | **服务端**在预处理阶段用 DPF 自行生成标准基向量份额,在线阶段常数通信调整到目标索引/值 |
| 审计 | 必须做 DPF 有效性审计(权重 $O(N)$ 或 $O(L)$) | **免审计**(内建) |
| 授权材料存放 | Express/Sabre 明文;Spectrum/PACL 加密但更新可见 | **跨服务端秘密共享**,信息论隐藏 |
| 授权更新 | Spectrum/PACL 的密钥向量修改对服务端可见 | 一次不经意 DORAM 更新即可 |
| 基础原语 | DPF + MPC 相等性/Schnorr 证明 | DORAM(Floram 做 DOROM/DOWOM,2P-Duoram 做完整 DORAM)+ Du-Atallah MULT + EQZ |
| 抗共谋 | Express/Sabre 否;Spectrum/PACL 计算性 | **信息论**(只要一个服务端半诚实) |

与 **Myco** 的关系值得单列:Myco 也是 ORAM 路线的元数据私密消息系统、每次访问服务端工作量 polylog 且优于 PIR/DPF 系统,但**不提供服务器强制的访问控制**——任何客户端都能读任意位置,必须靠 trial-decrypt 找自己的条目。Remise 明确把自己定位为"改进 DPF 式系统的访问控制",即让服务端能强制"只能读写被授权的索引"。

与**动态广播加密**(如 Delerablée 等)的关系:该路线也能做到"仅授权读者可解密",但通常通过密文或密钥更新**暴露授权/撤销结构**;RemiseCC 把授权状态单独放在不经意的令牌库 RDTOK 中,撤销只需一次不经意的 DORAM 更新,不重加密消息、不暴露哪条授权变了。

### 5.2 创新点分析(作者自陈的三条 contribution)

1. 面向消息板的 **DORAM 式授权机制**,并提供内建可审计性(built-in auditability);
2. **通信信道**设计:写者可向读者授予读权限,而服务端不知道哪个读者获得了权限;
3. 支持访问权限的**撤销**,同时向服务端隐藏"谁的权限被修改了"。

### 5.3 适用场景

- **匿名公告板(RemiseBB)**:写者数远少于用户总数的广播场景(借鉴 Spectrum 的不对称性,服务端计算只受真实写者数影响,同时从不提供掩码流量的全体用户中获得匿名性,不必预留额外空间);用分配的索引避免写碰撞。
- **匿名通信信道(RemiseCC)**:需要"作者—订阅者"模型的场景(作者可随时增删订阅者/读者),如记者与线人、私密群组留言板。
- 不适用:需要线性一致并发读写的存储语义;需要抗恶意服务端(需 Blame-Game)的场景;无法提供带外信道分发令牌的场景。

### 5.4 方法对比表

**Table 1(解析稿 §1.2):Remise 与既有系统对比。** $N$ = 数据库大小,$L$ = 注册写者数,$\lambda$ = 安全参数;"Auth Secret Hiding" 指每索引授权材料是否对单个服务端隐藏;"Auth Update Privacy" 指授权状态能否在不被服务端看见的情况下更新。Riposte 满足 $N>L$,其余系统 $N=L$;Riposte 不提供授权。$\star$ 授权与数据库写重叠;$\dagger$ 审计与授权统一;$\ddagger$ 客户端发送索引的秘密份额而非 DPF 密钥,需 $\log L$ 位。

| 系统 | 客户端请求大小 | 服务端审计工作量 | 服务端授权工作量 | 授权秘密隐藏 | 授权更新隐私 |
|---|---|---|---|---|---|
| Riposte | $O(\sqrt{N})$ | $O(N)$ | — | — | — |
| Express | $O(\lambda^2)$ | $O(L)$ | $O(L)^{\star}$ | × | × |
| Sabre | $O(\log L)$ | $O(\log L)$ | $O(1)$ | × | × |
| Spectrum | $O(\log L)$ | $O(L)$ | $O(L)^{\dagger}$ | √(离散对数困难) | × |
| Spectrum + PACL | $O(\log L)$ | $O(L)$ | $O(L)^{\dagger}$ | √(离散对数困难) | × |
| **Remise** | $O(\log L)^{\ddagger}$ | **—** | $O(L)$ | **√(秘密共享)** | **√** |

**Table 2(解析稿 §5):Remise 各变体的服务端侧渐近代价。** 灰色部分(此处以 + 分隔的第一项)为预处理代价;$m$ 为每索引读令牌数。

| 操作 | 本地计算 | 带宽 | 轮数 |
|---|---|---|---|
| Remise Write | $O(n)+O(n)$ | $O(\lg n)+O(1)$ | $O(\lg n)+O(1)$ |
| RemiseCC Read | $O(n)+O(n\cdot m)$ | $O(\lg n)+O(m)$ | $O(\lg n)+O(1)$ |
| RemiseCC Update Authorization | $O(n)+O(n\cdot m)$ | $O(\lg n)+O(m)$ | $O(\lg n)+O(1)$ |

**Table 3(解析稿 §5):写操作的带宽分解(单位:字节),数据库规模固定为 $2^{20}$。** $n$ = 写请求数,$k$ (out of $n$) = 通过授权的请求数,$m$ = 载荷大小,`rnds` = RemiseBB(Sabre) 中 LowMC 的轮数。Remise 的 DOROM 操作用 LowMC 密码,故出现在"请求有效性校验带宽"中;灰色值为预处理阶段的通信量。Spectrum 与 Express 的通信量由其源码算出。

| 系统 | 客户端请求大小(writer → $\mathtt{S}_b$) | 请求有效性校验 $\mathtt{S}_b$ → $\mathtt{S}_{1-b}$ | 访问 $\mathtt{S}_b$ → $\mathtt{S}_{1-b}$ |
|---|---|---|---|
| Remise | $(m+24)\cdot n$ | $960\cdot n+16\cdot(2\cdot\text{rnds}+3)\cdot n$ | $m\cdot k$ |
| RemiseBB (Sabre) | $(m+24)\cdot n$ | $16\cdot(\text{rnds}+3)n$ | $m\cdot k$ |
| Spectrum (PACL) | $(m+3120)\cdot n$ | $65\cdot n$ | $0$ |
| Express (PACL) | $(m+376)\cdot n$ | $16\cdot n$ | $0$ |

表读法:Remise 系客户端请求更小的原因是**客户端不发 DPF 密钥**,而是服务端从索引与消息份额自行构造 DPF;各系统的有效性校验(审计 + 授权)带宽**与消息大小无关**——Remise 中消息份额只在授权通过后才进入访问阶段。

## 6. 实验表现与优势

### 6.1 实验设计和设置

- **实现**:C++ 概念验证原型。
- **硬件**:单台服务器,2 × Intel Xeon Gold 6430 处理器,251 GiB RAM,64 位 Linux;用 `tc netem` 模拟网络延迟与带宽;所有实验在系统空闲时运行。
- **匹配威胁模型的配对比较**:RemiseBB ↔ Spectrum (PACL);RemiseBB (Sabre) ↔ Express (PACL)。理由:RemiseBB 与 Spectrum(PACL) 中"服务端–客户端共谋**不能**让服务端单方面给任意写者签发写令牌";RemiseBB(Sabre) 与 Express(PACL) 中这种共谋**可以**。基线实现取自 PACL 的代码库。
- **对比的 PACL 系统**:Spectrum(PACL) 能提供与 RemiseBB 相同的抗共谋级别但与其余 PACL 方案一样不支持授权更新;Express(PACL) 与 RemiseBB(Sabre) 同为"共谋可签发令牌"级别。
- **未与 plain Spectrum 对比**:因为集成 PACL 已把 Spectrum 的性能提升了一个数量级以上。

### 6.2 数据集

**无真实数据集**——所有评测使用合成负载与受控实验环境;论文 Ethical Considerations 明确说明本研究不涉及人类被试、不做物理实验、不收集真实世界私有数据。变化的维度是:数据库规模(至 $2^{26}$)、网络延迟(10/30/60 ms)、每索引读令牌数 $m$、消息大小(吞吐实验固定 32 字节)、未授权流量占比、DPF 是否离线预处理。

### 6.3 Baseline

Spectrum (PACL) 与 Express (PACL),均来自 PACL 代码库;PACL 为 IEEE S&P 2023 的访问控制方案。因基础设施限制,Spectrum(PACL) 与 Express(PACL) 的实验规模**均止于 $2^{26}$**,更大规模为外推。

### 6.4 评价指标

服务端校验单条写请求的墙钟时间(含 DPF 审计(若有)与授权检查)、吞吐率(throughput)、有效吞吐率(goodput,只计通过授权的请求)、带宽(Table 3 的字节分解)、总时间按"预处理 / 在线有效性校验 / 访问"三段的分解、95% 置信区间。

### 6.5 关键实验结果

| 实验 | 设置 | 结论 |
|---|---|---|
| 写请求有效性校验墙钟时间(Fig. 3a) | RemiseBB vs Spectrum (PACL),延迟 10/30/60 ms,数据库规模变化 | 小数据库下 Spectrum(PACL) 在**总代价(预处理 + 在线)**上更优:RemiseBB 的预处理——具体是 MPC 生成标准基向量份额——需 $O(\log n)$ 轮通信,而 Spectrum(PACL) 求值可验证 DPF 虽计算更贵却省掉这些轮次。随数据库增大,计算开销开始主导延迟开销;延迟越低,交叉点出现在越小的数据库规模。**仅计在线阶段时增益大一个数量级:数据库规模 $2^{26}$ 时 RemiseBB 比 Spectrum(PACL) 快近 80×** |
| 写请求校验:RemiseBB (Sabre) vs Express (PACL)(Fig. 3b) | 批处理摊销延迟 vs 逐请求本地计算 | RemiseBB (Sabre) 的授权无预处理阶段,且基于 PRF 的授权检查**与数据库规模无关**;Express (PACL) 的授权要求值 DPF,授权时间**随数据库规模线性增长** |
| 吞吐/有效吞吐(Fig. 4) | 延迟固定 30 ms,消息 32 字节,变化未授权流量占比 | **在线生成 DPF**(on-the-fly)相比离线预处理 DPF 显著降低吞吐与有效吞吐;而**离线预处理 DPF 时,未授权流量占比上升反而提升吞吐与有效吞吐**——因为未授权请求在轻量授权阶段就被终止,避开了更贵的访问阶段。RemiseBB (Sabre) 用在线 DPF 时,随未授权比例上升,在**越来越小的数据库规模**上超过 Express (PACL),原因是其授权代价为 $O(1)$ |
| 总代价分解(Fig. 5) | 数据库 $2^{20}$,延迟 30 ms,变化消息大小 | 在线有效性校验只占总执行时间的很小一部分(RemiseBB 的在线有效性校验约 **15 ms**,图中看不到);预处理代价只出现在 RemiseBB 与 RemiseBB (Sabre);**访问阶段主导总运行时间**且随消息大小显著增长;各系统访问代价相同(依赖相同的 DPF 式访问机制),故消息大小增大时吞吐/有效吞吐受相似影响;所有系统的有效性校验代价随消息大小近乎不变(请求有效性与载荷大小无关) |
| RemiseCC 读授权 vs PACL inclusion predicate(Fig. 6) | 数据库 $2^{24}$,变化每索引访问令牌数;不设服务端间延迟(本地计算主导) | RemiseCC 的读授权检查耗时对比 PACL 的 inclusion predicate 访问控制(后者提供"每索引多个读授权令牌"的同等功能)。未画 RemiseCC 的在线时间,因为它接近总时间——用的 2P-Duoram 基于**计算性对称 PIR(CSPIR)** |
| 误差棒 | RemiseBB 延迟 30 ms、规模 $2^{24}$ | 总时间变化 ±14.597 ms,在线时间变化 ±8.8908 ms;Express (PACL) 侧方差小到误差棒不可见 |

### 6.6 优势最明显的场景

1. **大数据库 + 高延迟**:交叉点之后,且延迟越高 RemiseBB 越占优;在 $2^{26}$ 规模上在线校验快近 80×,作者据外推认为更大规模下差距会进一步拉大(Spectrum(PACL) 因基础设施限制无法跑更大规模)。
2. **高未授权流量占比 + 离线预处理 DPF**:此时吞吐与有效吞吐不降反升,因为未授权请求被轻量授权阶段拦下。
3. **需要授权撤销或授权更新隐私**:这是 Spectrum/PACL 结构上做不到的能力(Table 1 的 Auth Update Privacy 列仅 Remise 为 √)。
4. **需要抗客户端–服务端共谋的授权保密**:RemiseBB/RemiseCC 是信息论隐藏。
5. **RemiseCC 读授权的规模不敏感**:若采用 RemiseBB (Sabre) 变体,授权检查 $O(1)$、与数据库规模无关。

### 6.7 局限性(实验侧)

1. 无法与 Spectrum(PACL)/Express(PACL) 在超过 $2^{26}$ 的规模上实测,更大规模的结论是**外推**。
2. 单机双处理器环境 + `tc netem` 模拟延迟,非真实广域部署。
3. 小数据库、低延迟下 Spectrum(PACL) 的总代价更优(预处理轮数劣势)。
4. 只与 PACL 系的两个系统对比;未与 Myco 等 ORAM 路线系统做实验对比(仅在 Related Work 中做定性讨论)。
5. 方法层面的局限见 §4.6(并发一致性、带外分发、无 Blame-Game、$m$ 因子)。

## 7. 学习与应用

### 7.1 是否开源?

是。代码经永久链接发布:https://zenodo.org/records/20438384(2026-09-19 记录为 artifact 归档链接,论文未给出论文 DOI)。Open Science 一节列出的制品包括:源代码(benchmark 代码、DPF 原语、秘密共享抽象与 MPC 构建块、协议执行所用的异步网络框架)、基准测试基础设施(复现 Fig. 3–6 的脚本与命令、配置文件示例、网络延迟配置脚本)、报告指标(吞吐/有效吞吐、评测/审计/写延迟、通信带宽、95% 置信区间)。

### 7.2 复现关键步骤

1. 从 Zenodo 取源码与异步网络框架,按 README/配置示例搭建两服务端环境;
2. 用延迟配置脚本设置目标 RTT(Fig. 3 用 10/30/60 ms;Fig. 4/5 用 30 ms);
3. 选择实例化:RemiseBB(与 Spectrum(PACL) 比)、RemiseBB (Sabre)(与 Express(PACL) 比)或 RemiseCC(与 PACL inclusion predicate 比);DPF 需分别配置离线预处理与在线生成两种模式(Fig. 4 的关键变量);
4. 按数据库规模(至 $2^{26}$)、消息大小(吞吐实验 32 字节)、未授权流量占比、每索引令牌数 $m$ 扫参;
5. 注意基线侧限制:Spectrum(PACL)/Express(PACL) 需在 $2^{26}$ 以内运行。

### 7.3 关键超参数、预处理和训练细节

无训练环节。关键参数:安全参数 $\lambda$、数据库规模 $N$、注册写者数 $L$、每索引读令牌数 $m$、DPF 预处理开关(离线 vs 在线)、网络延迟、消息大小。预处理要点:授权令牌的份额在 setup 阶段由两服务端独立采样($\ell_0,\ell_1$,互不知晓);DORAM 所需的标准基向量份额用 DPF 在预处理阶段生成,在线阶段以常数通信调整到目标索引与值;MPC 乘法的关联随机数可用 OT 产生。

### 7.4 能否迁移到其他任务?

"秘密共享的令牌库 + 不经意校验/更新"这一模式是可迁移的:任何两服务端秘密共享存储(加密检索、不经意键值存储、私有消息系统)只要需要**服务端强制的、对服务端自身保密的访问控制**,都可以套用同一套"EQZ 相等性检查 + MPC OR 组合 + DORAM 更新"的骨架;同理,"让服务端自己生成标准基向量份额以消灭客户端有效性证明"的思路可移植到其他依赖客户端提交可验证 DPF/证明的隐私系统。

反向地,**该模式与本知识库主题(加密流量分类、网站指纹、审查规避、恶意流量检测)无直接交集**:Remise 的输出是密码学协议与性能曲线,而非从流量中推断信息的特征/模型。

### 7.5 对我的研究有什么启发?

方法学上可取两点(与流量分析领域无直接技术交集,属评测方法借鉴):

1. **按威胁模型配对基线**:作者不把所有系统一锅端地比,而是先论证"哪两个系统的安全假设同级"(服务端–客户端共谋能否单方签发令牌),再在组内比较。这种"先对齐假设、再比性能"的写法可迁移到流量分析中的攻防对比(例如只有同为"闭集 + 同样对抗能力"的方法才放同一张对比表)。
2. **按阶段分解成本**:Fig. 5 把总时间拆为预处理 / 在线校验 / 访问三段,并指出"未授权请求不进入最贵阶段"这一结构性现象。这种"按阶段归因"的分析方式可迁移到流量分类流水线的延迟/资源归因(特征提取 vs 模型推理 vs 后处理)。

至于具体的 DORAM/MPC 技术(2P-Duoram、Floram、Du-Atallah、EQZ、CSPIR),与流量分析主题相距较远,本笔记不作主题级收录(见 §9)。

## 8. 总结

### 8.1 核心思想

把匿名通信系统的"审计 + 授权"两道关卡从 **DPF 世界**搬到 **DORAM 世界**:服务端自己生成标准基向量份额 → 审计消失;授权令牌做成跨服务端的加法共享 → 授权秘密信息论隐藏且可被不经意地校验与更新。在这个骨架上有两种落地形态:只写不读的公告板 RemiseBB,与可按人授予/撤销读权限的信道 RemiseCC;若愿意放宽到"允许服务端–客户端共谋"的威胁模型,还可以用 PRF + MPC 相等性检查的 Sabre 式授权把授权代价压到与数据库规模无关的 $O(1)$。

### 8.2 速记版 Pipeline

**Setup**(一次):写者经 Riposte 式匿名广播发布 $pk$ → 服务端重构 SETUPDB、用 ASSIGN 分配索引 $i^*$、各自采样 $\ell_b$ 组成写令牌 $\ell=\ell_0+\ell_1$ 并写入 WRTOK → 用 $pk$ 加密 $(i^*\|\ell_b)$ 写 ACCESSDB 并发布 → 写者解密得 $(i^*,\ell)$;服务端把 WRTOK 转成 PRF 掩码的只读库 $\text{WRTOK}^{\mathrm{RO}}$。

**Write**:$(\Delta M, i^*, \omega)$ 的份额 → EQZ 零检查 ∨ EQZ 令牌检查 → 通过则写 $\mathbf{D}[i^*]$。掩护流量用 $\Delta M=0$。

**Read(仅 RemiseCC)**:读者交 $(i^*, t)$ 份额 → 服务端取 $\text{RDTOK}[i^*]$ 的 $m$ 个令牌,逐个 EQZ 后 OR → 通过则返回 $\mathbf{D}[i^*]$ 的份额。

**Grant/Revoke(仅 RemiseCC)**:写者带外发令牌给读者,再提交 $\Delta R$ 份额 → 服务端校验写令牌 → DORAM 更新 RDTOK。

一句话:**审计靠"服务端自造 1-hot"消掉,授权靠"秘密共享 + 不经意更新"藏住。**

## 9. Obsidian 知识链接

### 9.1 相关概念

无。本文属**匿名通信 / 隐私保护系统(密码学)**方向,与 kb_reference C 节白名单中的概念页无对应项。

逐一核对:白名单概念为 `anomaly-detection`、`anonymous-traffic-identification`、`censorship-circumvention`、`encrypted-traffic-analysis`、`few-shot-traffic-learning`、`malicious-traffic-detection`、`traffic-classification`、`traffic-foundation-model`、`traffic-representation-learning`、`tunnel-detection`、`website-fingerprinting`。其中最易混淆的是 `anonymous-traffic-identification`(匿名流量识别,属流量分析:从流量中识别匿名网络/Tor 流量)与 `censorship-circumvention`(审查规避,覆盖审查测量、规避工具设计、流量混淆/隧道/协议生成)。本文的主题是**密码学意义上的匿名通信系统本身**(让服务端在不学索引的前提下强制访问控制),不是"识别"匿名流量、也不设计规避工具或混淆协议,故两者均不适用。

### 9.2 相关方法

无。白名单方法为 `contrastive-learning`、`convolutional-network`、`graph-neural-network`、`multi-modal-fusion`、`pre-training-finetuning`、`self-supervised-learning`、`state-space-model`、`transformer`,均为机器学习方法,与本方案的 DORAM/MPC/DPF 密码学原语无交集。

### 9.3 相关任务

无。白名单任务为 `anomaly-detection`、`app-fingerprinting`、`encrypted-traffic-detection`、`malicious-traffic-detection`、`traffic-classification`、`traffic-representation`、`tunnel-detection`、`website-fingerprinting`,均为流量分析任务。

### 9.4 可更新的综述页面

无。白名单综述为 `survey-encrypted-traffic-analysis`、`survey-few-shot-learning`、`survey-malicious-traffic-detection`、`survey-traffic-foundation-model`、`survey-website-fingerprinting`,均不覆盖匿名通信协议设计。

### 9.5 可加入的对比表

无。白名单对比表为 `method-comparison-table`、`dataset-comparison-table`、`open-source-registry`、`motivation-pattern-comparison`、`narrative-pattern-comparison`。本笔记 §5.4 的 Table 1(Remise vs Riposte/Express/Sabre/Spectrum/PACL)是**论文自带的方案对比表**,比较对象是匿名通信系统而非流量分析方法,不属于 `method-comparison-table` 的收录范围(与同批 InSPECtor 的处理一致)。

## 10. 证据记录

| 论断 | 证据位置 | 证据类型 |
|---|---|---|
| 三种缺失同时被填补(内建审计 / 信息论授权隐藏 / 授权更新隐私)对应三条 contribution | §1.3、§1.3.1、§Abstract | 作者自陈 |
| 两服务端各自采样 $\ell_0,\ell_1$、$\ell=\ell_0+\ell_1$ 为写令牌,双方互不知对方份额 | §4 Setup Phase、Protocol 5 Stage 2 | 协议描述 |
| w 从 ACCESSDB 解密得到 $(i^*,\ell_0,\ell_1)$ 并重构 $\ell$ | §4 Protocol 5 Stage 3 | 协议描述 |
| 掩护流量:写为零消息(EQZ ∨ 组合),读为保留索引 $i_{\mathrm{read}}$;对服务端信息论不可区分 | §3、§4 Protocol 6/8 说明 | 机制设计 |
| 未授权请求在轻量授权阶段即被终止,故离线预处理 DPF 时未授权占比上升反而提升吞吐/有效吞吐 | §5 Throughput and Goodput 段 | 实验现象 + 机理解释 |
| RemiseBB 在线有效性校验约 15 ms,访问阶段主导总时间 | §5 Cost Breakdown 段(Fig. 5 图注) | 实验数值 |
| 访问代价各系统相同(同一 DPF 式访问机制) | §5 Cost Breakdown 段 | 作者陈述 |
| $2^{26}$ 时 RemiseBB 在线校验比 Spectrum(PACL) 快近 80× | §Abstract、§5 Request Validity Check 段 | 实验数值(两处一致) |
| RemiseBB(Sabre) 授权 $O(1)$,Express(PACL) 授权随数据库规模线性增长 | §4.1、§5 Request Validity Check 段 | 机制 + 实验 |
| Table 3 的量纲:客户端请求 $(m+24)n$ vs Spectrum(PACL) $(m+3120)n$、Express(PACL) $(m+376)n$ | §5 Table 3 | 论文表格(其余系统通信量由源码算出) |
| Spectrum(PACL)/Express(PACL) 实验限于 $2^{26}$(基础设施限制),更大规模为外推 | Fig. 3/Fig. 4 图注 | 作者自陈限制 |
| 并发读写不保证线性一致:读者可能重构出"一旧一新"份额组合 | §4.2 Limitations | 作者自陈限制 |
| 无 Blame-Game,恶意服务端可丢弃诚实写请求;服务端假设半诚实 | §4.2 Limitations | 作者自陈限制 |
| 读者侧令牌分发必须带外进行 | §4.2 Limitations、§4 Protocol 7 说明 | 作者自陈限制 |
| 注册沿用 Riposte 有非零碰撞失败率,$2.7N$ 表约 95% 成功注册 | §4 Setup Phase 段 | 作者陈述(引用 Riposte 的碰撞恢复方法) |
| 服务端仅需在窗口结束后重构 SETUPDB 一次以恢复 $pk$ 集合 | §4 Setup Phase 段、Protocol 5 | 协议描述 |
| RemiseCC 读授权用计算性对称 PIR(CSPIR) 的 2P-Duoram,故在线时间接近总时间 | §5 Fig. 6 段 | 实现细节 |
| 与动态广播加密的区别:后者经密文/密钥更新暴露授权或撤销结构 | §4 段末(Delerablée et al. 讨论) | 作者对比陈述 |
| Myco 不提供服务器强制访问控制,任意客户端可试解密读任意位置 | §6 Related Work | 作者对比陈述 |
| 作者使用生成式 AI 工具润色文本 | Acknowledgments | 论文自陈 |
| 资助来源 ANRF 与 Satish and Kamlesh Agarwal 差旅资助 | Acknowledgments | 论文自陈 |

## 11. 原始资料链接

- 论文页:https://www.usenix.org/conference/usenixsecurity26/presentation/ravi-rohan
- PDF:00-inbox/PDFs/2026-USENIX-Remise__Authorized_Anonymous_Communication_Systems.pdf
- MinerU Markdown:02-parsed-markdown/2026-USENIX-Remise__Authorized_Anonymous_Communication_Systems.md
- 代码/制品(artifact 归档,非论文 DOI):https://zenodo.org/records/20438384

## 12. 后续问题

1. **数据点密度不足的图**:Fig. 3–6 以曲线形式给出,解析稿中只保留了图注与正文描述,没有逐点数值(如交叉点的精确数据库规模、各 $m$ 下的绝对耗时)。若后续需要引用曲线读数,应回到 PDF 原图。
2. **交叉点的定量表达缺失**:作者只定性给出"延迟越低,交叉点出现的数据库规模越小",没有给出各延迟下交叉点的具体规模值。
3. **$m$ 的取值未在正文中固定**:Table 2/Table 3 与 Fig. 6 均含 $m$(每索引读令牌数),但解析稿未给出实验所用的具体 $m$ 值集合,需回原文图注/正文确认。
4. **在 >$2^{26}$ 规模上的外推未经实测**:作者自己声明 Spectrum(PACL)/Express(PACL) 受基础设施限制只能到 $2^{26}$,$2^{26}$ 以上的结论为外推。
5. **RemiseCC 与 Sabre 结合为何不保持写者–读者不可关联**:原文只给出一句否定性结论(§4.1 末),未展开证明;若关心该组合的性质需追原文或后续工作。
6. **无 Blame-Game 的后果边界**:恶意服务端"丢弃写请求"之外还能做什么(如选择性拒绝读、或利用 LeakLog 外的侧信道),原文未系统讨论;Blame-Game 的移植可行性(如借鉴 Spectrum 的做法再叠加秘密共享令牌)是一个自然的开放问题。
7. **一致性增强的代价**:作者提出锁或版本号可提供更强一致性但会增加延迟并**可能泄漏额外访问模式信息**,这一权衡未量化,值得后续实验。
8. **注册碰撞与匿名性的交互**:超配(Riposte 式)以空间换注册成功率,而更宽的注册窗口/更多掩护参与者会改变匿名集大小;二者的联合优化未在文中讨论。
9. **与 Myco 的实验对比缺失**:Myco 是 ORAM 路线的近邻工作(同为 ORAM,但不做服务端强制访问控制),仅有定性对比;若做"ORAM 路线 vs DPF 路线"的横向评测,Remise 缺一个同族基线。
10. **可迁移性验证**:把"秘密共享令牌库"套用到其他两服务端秘密共享存储时,性能特征(尤其 $O(\lg n)$ 轮预处理)是否会因工作负载不同而改变交叉点位置,尚不清楚。

---

## 13. 写作叙事与故事线分析

Remise 先把 DPF 世系的两项痛点拆成审计与授权，再提出“发送者匿名信道”这一新 RUS 子类作为需求牵引。DORAM 负责免审计匿名访问，秘密共享 token 负责可遗忘授权，公告板与保密信道两个实例随后分别验证功能。最后以 PACL 对比在线服务端时间、客户端/服务端共谋和授权更新隐私收束安全主张。

## 14. 深度分析证据边界与知识层联动建议

- 现有笔记已包含 DORAM 读写、RemiseBB/RemiseCC、授权 token、PACL 对比和安全模型；性能数值、数据库规模和 artifact 需以原文表格核验。
- 可向匿名通信/隐私系统专题记录 Remise；不计入 traffic-* 方法统计。本次未修改共享页面。

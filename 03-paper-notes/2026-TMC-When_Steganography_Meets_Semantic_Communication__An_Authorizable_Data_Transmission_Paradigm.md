---
type: paper
title_original: "When Steganography Meets Semantic Communication: An Authorizable Data Transmission Paradigm"
title_cn: "当隐写术遇见语义通信：一种可授权的数据传输范式"
authors: ["Boyu Han", "Gaolei Li", "Xiao Yang", "Jun Wu", "Jianhua Li", "Yuchen Liu"]
year: 2026
venue: "IEEE TMC 2026"
doi: "10.1109/tmc.2026.3686502"
url: "https://doi.org/10.1109/tmc.2026.3686502"
pdf: "00-inbox/PDFs/2026-TMC-When_Steganography_Meets_Semantic_Communication__An_Authorizable_Data_Transmission_Paradigm.pdf"
mineru_md: "02-parsed-markdown/2026-TMC-When_Steganography_Meets_Semantic_Communication__An_Authorizable_Data_Transmission_Paradigm.md"
status: processed
reading_level: L2
research_area: []
task: []
method: ["convolutional-network"]
dataset: ["Tiny-ImageNet", "DIV2K"]
code: "unknown"
relevance: low
created: "2026-09-19"
updated: "2026-09-19"
---

# When Steganography Meets Semantic Communication: An Authorizable Data Transmission Paradigm

## 0. 论文基础信息

| 项目 | 内容 |
|---|---|
| 原文标题 | When Steganography Meets Semantic Communication: An Authorizable Data Transmission Paradigm |
| 中文标题 | 当隐写术遇见语义通信：一种可授权的数据传输范式 |
| 作者 | Boyu Han, Gaolei Li, Xiao Yang, Jun Wu, Jianhua Li, Yuchen Liu（解析稿未给出单位信息） |
| 年份 | 2026 |
| 会议/期刊 | IEEE Transactions on Mobile Computing (TMC) 2026；DOI 10.1109/tmc.2026.3686502（由主代理分配给出，解析稿正文未印 DOI） |
| 研究方向 | 语义通信（Semantic Communication, SemCom）与图像隐写（image steganography）的端到端融合；隐蔽传输与授权访问控制 |
| 任务类型 | 可授权隐蔽传输：把秘密图像嵌入封面图像，经 SemCom 管线传输后仅授权接收方可语义重建秘密，未授权方只能重建封面 |
| 方法关键词 | Secret Hiding Module（φ/H/ψ 三阶段）、Secret Decoding Module（6 层卷积 + 双线性上采样）、Dual-Objective Joint Training（R_r/R_h/R_u/R_a 四项风险的加权联合优化）、GMU 式融合与 PKI/TEE/PUF 授权管理讨论 |
| 数据集 | Tiny-ImageNet（100,000 张 64×64）、DIV2K（1,000 张，降采样到 256×256） |
| 是否开源 | 解析稿未提及代码仓库（写 unknown） |
| PDF | 00-inbox/PDFs/2026-TMC-When_Steganography_Meets_Semantic_Communication__An_Authorizable_Data_Transmission_Paradigm.pdf |
| MinerU Markdown | 02-parsed-markdown/2026-TMC-When_Steganography_Meets_Semantic_Communication__An_Authorizable_Data_Transmission_Paradigm.md |

---

## 1. 一句话总结

> 该文把图像隐写的"藏"与恢复"解码"模块直接插进端到端语义通信管线，用双目标联合训练让授权用户在低信噪比信道上仍能以约 31 dB PSNR / 91% SSIM 重建秘密图像，而普通用户与检测器都察觉不到秘密的存在。

---

## 2. 摘要翻译

### 2.1 摘要原文

Recent advances in Semantic Communication (SemCom) have integrated semantically aware encoding and channel adaptation to enhance wireless transmission efficiency. In SemCom, covert communication is extensively adopted to secure data transmission, but current methodologies remain constrained by signal-level obfuscation strategies that rely on bit-level manipulations. Consequently, they are loosely coupled with semantic feature learning and often face a rigid trade-off between covert robustness and undetectability in practice. To address these limitations, we propose a steganography-based authorizable SemCom framework, embedding the true transmission data within cover inputs for covert delivery. ... Moreover, to realize the above functionalities, the proposed SemCom system leverages a dual-objective joint training strategy, simultaneously learning shared knowledge of stealthy transmission and preserving the normal capability for regular data. Empirical results prove that our framework attains high-fidelity SemCom transmission for secret (PSNR 31 dB, SSIM > 91%, and LPIPS 0.04), and holds robustness under multiple adaptive and adversarial attack scenarios.（节选，完整摘要见解析稿 Abstract）

### 2.2 摘要中文翻译

语义通信（SemCom）的近期进展把语义感知编码与信道自适应结合起来，提升了无线传输效率。在 SemCom 中，隐蔽通信被广泛用于保障数据传输安全，但现有方法受限于依赖比特级操作的信号层混淆策略。因此它们与语义特征学习耦合松散，在实践中往往面临隐蔽鲁棒性与不可检测性之间的刚性权衡。为解决这些限制，我们提出一个基于隐写的可授权 SemCom 框架，把真实传输数据嵌入封面输入中进行隐蔽投递。集成的重点是：在语义通信架构内实现高度隐蔽的秘密传输。在该框架中，私有发送方用秘密隐藏模块把真实（即秘密）数据嵌入封面输入，再做语义编码后发送。接收端在多客户端场景下保证隐蔽数据可达性：持有秘密解码模块的授权用户可完整地语义恢复真实数据，而未授权用户仅能重建表观的封面内容、对隐藏数据毫无察觉。此外，为实现上述功能，所提 SemCom 系统采用双目标联合训练策略，同时学习隐蔽传输的共享知识与常规数据的正常传输能力。实验证明，本框架对秘密实现了高保真 SemCom 传输（PSNR 31 dB、SSIM > 91%、LPIPS 0.04），并在多种自适应与对抗攻击场景下保持鲁棒。

---

## 3. 方法动机

### 3.1 作者为什么提出这个方法？

- 语义通信把通信焦点从比特流转向语义，可在低带宽、差信道下保持可靠性；但用户在隐私保护、授权控制等场景需要**与主通信并行的隐蔽内容传输**（§I）。
- 现有隐蔽通信手段（扩频、噪声自适应功率控制、隐蔽波束成形、协议层隐蔽信道）都工作在**比特/信号层**：通过扰动物理符号或冗余比特实现隐蔽，与语义结构无关（§I、§II-B）。
- 语义通信中语义编码会压缩特征、信道会引入失真，直接"串联式"地在收发两端各接一个隐写模块会导致秘密恢复失败、隐蔽性不稳定（§I，Fig. 2 给出 naive baseline 的可视化失败案例）。

### 3.2 现有方法的痛点和不足

| 现有方法/路线 | 痛点 |
|---|---|
| 扩频信号（spread-spectrum） | 把信号扩散到伪随机码空间以低于噪声底，但直接扰动物理符号使封面介质失真增大（PSNR/SSIM 下降），提高被检测风险（§I, Fig. 1(a)） |
| 噪声自适应功率控制（noise-adaptive power control） | 按信道噪声调节功率，但依赖比特级恢复；信道变差时秘密恢复效用迅速崩塌（§I, Fig. 1(b)） |
| 隐蔽波束成形（covert beamforming） | 空间隐身依赖波束对准，仍属信号层手段，与语义特征学习松耦合（§I、§II-B） |
| 传统隐写（Baluja 全卷积、HiNet、DeepMIH 等） | 只做图像到图像的嵌入-恢复，不涉及在语义编码/信道编码链路中的传输；与语义通信任务无耦合（§II-C） |
| 语义隐写（Huo et al. [42]） | 把比特级消息嵌入语义特征，但**不是**图像到图像、也不区分授权/未授权接收方的恢复权限（§II-C 末段） |
| 朴素串联集成（本文用作反例） | stego 图过完 SemCom 管线后视觉上仍合理，但直接解码秘密完全失败（§I, Fig. 2） |

### 3.3 论文的研究假设或核心直觉

核心直觉：**秘密不应当以比特扰动的形式叠加在信号上，而应当以"语义"的形式融进封面输入**，并让隐写的嵌入/恢复知识与语义编解码器在同一套共享知识里被联合优化。由此派生出三个可操作的设计判断：(1) 隐藏模块放在发送端最前端（把 $I_c$ 与 $I_s$ 融合成 $I_e^*$ 后再做语义编码）；(2) 秘密解码模块放在**信道解码器与语义解码器之间**，直接作用于中间语义特征 $\tilde{z}_{sct}$，从而与公开重建路径解耦、只对授权用户开放；(3) 由于"语义压缩 + 信道失真会压制嵌入线索"（Fig. 2），必须有专门的双目标联合训练（$R_r,R_h,R_u,R_a$ 四个风险）来同时保公开重建与秘密恢复（§III–§IV）。

### 3.4 问题发现路径

| 阶段 | 内容 | 证据来源 |
|---|---|---|
| 现象观察 | 信号层隐蔽手段在同样 30 dB SNR 下对封面的 PSNR/SSIM 破坏更大且传输速率受限；比特级恢复在信道变差时先崩溃 | §I, Fig. 1(a)(b) |
| 痛点提炼 | 语义通信用户要求"隐蔽性"是伴随语义交换的内在需求，而现有方法操作物理层符号、不考虑高层语义，能安全传输的隐藏信息量受限 | §I |
| 问题转化 | 把"如何更隐蔽地扰动信号"转化为"如何在语义通信架构内、以语义特征为载体实现高隐蔽的秘密传输（且区分授权与否）" | §I（"shift the objective toward achieving highly covert secret transmission within the semantic communication architecture"） |
| 文献定位 | 语义通信、隐蔽通信、深度隐写三条线各自成熟，但**首次**把 SemCom 与图像隐写结合起来（作者称"to the best of our knowledge, this is the first work"）；Huo et al. [42] 仅做语义特征中的比特级消息嵌入 | §II-A/B/C、§I 末 |

### 3.5 科学假设形成

| 假设 | 具体内容 | 推导依据 | 验证方式 |
|---|---|---|---|
| 核心假设 | 在 SemCom 管线前后端分别加隐藏/秘密解码模块并做双目标联合训练，可在不损害公开语义传输的前提下，让授权方高保真恢复秘密、未授权方与检测器均无法察觉 | §IV-A（Object-1/Object-2 联合学习问题）、§IV-D（Eq. 21–24） | 4 种语义编解码架构（JSCC-V/JSCC/JSCC-F/JSCC-Q）× 2 信道（AWGN/Rayleigh）× 2 数据集 × 9 档 SNR（Tables III/IV） |
| 辅助假设 1 | 嵌入的秘密在视觉、统计分布与检测器三个层面都不可察觉 | §V-B（覆盖性三维评估：视觉不可感知、统计一致性、检测器不可检测） | PSNR/SSIM/直方图 L1/高频能量 + StegExpose/SRNetLite/HiNetDetectorLite（Tables V/VI） |
| 辅助假设 2 | 联合训练比"SemCom 与秘密分支各自独立训练"显著更优 | §IV-D（共享知识的协同优化必要性） | 独立训练 baseline 对比（Fig. 7，Tiny-ImageNet） |
| 辅助假设 3 | 秘密解码路径依赖稳定共享嵌入，因而对信道压缩比（CR）不敏感，而公开路径对 CR 敏感 | §V-C（CR 0.2–0.9 消融） | Table VII（AWGN/Rayleigh 两栏） |

**假设验证结果**：

| 假设 | 支撑/反驳 | 关键实验证据 | 位置 |
|---|---|---|---|
| 核心假设 | 支撑 | Tiny-ImageNet AWGN 30 dB：SemCom 四架构均 >44 dB PSNR、>99.5% SSIM，秘密恢复约 30–31.6 dB / 90–92% SSIM；Rayleigh 下 SemCom 45.9–48.1 dB、秘密 30.9–31.6 dB | §V-C, Tables III/IV |
| 辅助假设 1（隐蔽性） | 支撑 | 封面 vs stego：平均 PSNR 38.31 dB、SSIM 99.39%；StegExpose BAcc 0.583、SRNetLite 38.33%、HiNetDetectorLite 45.00% 准确率（接近/低于随机） | Tables V/VI |
| 辅助假设 2（联合训练） | 支撑 | AWGN 30 dB 秘密恢复 31.3 dB/91.3%/LPIPS 0.0445，独立训练仅 27.0 dB/84.1%/0.0541；Rayleigh 下 30.9 dB vs 25.0 dB | §V-C, Fig. 7 |
| 辅助假设 3（CR 不敏感性） | 支撑 | CR 由 0.2 升至 0.8：公开 PSNR 14.78→49.35 dB（AWGN），秘密始终约 31.3 dB/91.3% | Table VII |

---

## 4. 方法设计

### 4.1 方法整体流程

框架在标准 SemCom 管线（语义编码 $\mathcal{E}_{sem}$ → 信道编码 $\mathcal{E}_{ch}$ → 无线信道 $\mathcal{C}$ → 信道解码 $\mathcal{D}_{ch}$ → 语义解码 $\mathcal{D}_{sem}$）基础上增加三个部件：发送端最前端的 Secret Hiding Module、接收端位于信道解码器与语义解码器之间的 Secret Decoding Module（仅授权方持有）、以及把两者与语义编解码器绑定的 Dual-Objective Joint Training。传输时秘密数据先被藏进封面得到 stego 输入 $I_e^*$，再走完整语义通信链路；未授权用户直接用 $\mathcal{D}_{sem}(\tilde{z}_{sct},\gamma)$ 重建 stego/封面，授权用户额外把中间特征 $\tilde{z}_{sct}$ 送入 $\mathcal{D}_{scre}$ 恢复秘密（§IV，Fig. 4）。

### 4.2 详细 Pipeline

| 步骤 | 输入 | 具体操作 | 输出 | 作用 |
|---|---|---|---|---|
| Step 1 特征提取 | 封面 $I_c$、秘密 $I_s$ | 共享特征编码器 $\phi(\cdot)$（3×3 与 4×4 卷积 + ReLU）分别编码：$f_c=\phi(I_c)$、$f_s=\phi(I_s)$（Eq. 11） | $f_c,f_s$ | 把两幅图像映射到可融合的特征空间 |
| Step 2 特征融合与隐藏 | $f_c,f_s$ | 通道拼接 $f_{joint}=\mathrm{Concat}(f_c,f_s)$，送入 $\mathcal{H}(\cdot)$（1 个 1×1 + 2 个 3×3 卷积，均接 BN 与激活）得 $f_h$（Eq. 12–14） | 隐藏表示 $f_h$ | 把秘密语义压进紧凑表示 |
| Step 3 上采样与构造 | $f_h$ | 构造块 $\psi(\cdot)$（1 个转置卷积 s=2/p=1 + 2 个标准卷积，末层 Tanh）生成 $I_e^*=\psi(f_h)$（Eq. 15–16） | stego 输入 $I_e^*$ | 形成与封面视觉一致的 stego 图像 |
| Step 4 语义通信传输 | $I_e^*$ | 语义编码 $z=\mathcal{E}_{sem}(I_e^*,\gamma)$ → 压缩掩码与功率归一化 $x=\sqrt{PK}\,\frac{z\odot m}{\|z\odot m\|}$ → 信道（AWGN 或 Rayleigh）→ 信道解码 $\tilde{z}_{sct}$（Eq. 1–5） | 中间语义特征 $\tilde{z}_{sct}$ | 秘密随语义特征一起被传输 |
| Step 5 公开重建（未授权） | $\tilde{z}_{sct}$ | 普通语义解码器 $\hat{I}_e^*=\mathcal{D}_{sem}(\tilde{z}_{sct},\gamma)$（Eq. 9 右式） | 重建 stego | 未授权用户只看到封面内容 |
| Step 6 秘密解码（授权） | $\tilde{z}_{sct}$（48×64×64） | 6 层 3×3 卷积（通道 48→64→64→64→32→16→3，BN+ReLU，末层 Sigmoid）+ 双线性上采样 scale=4（Eq. 17–20，Algorithm 2） | 重建秘密 $\hat{I}_s\in\mathbb{R}^{3\times256\times256}$ | 授权用户专享的秘密恢复 |
| Step 7 双目标联合训练 | 训练集 $D_{train}$ | 四项加权风险 $R_r$（公开重建）、$R_h$（stego-封面相似）、$R_u$（未授权重建）、$R_a$（授权秘密恢复）同时优化（Eq. 21–24） | 更新后的全家桶参数 | 让共享知识同时支撑公开与私有重建 |

### 4.3 模型结构或系统模块

| 模块 | 功能 | 输入 | 输出 | 与其他模块关系 |
|---|---|---|---|---|
| Secret Hiding Module（φ/H/ψ） | 发送端秘密嵌入 | $I_c,I_s$ | $I_e^*$ | 位于整个 SemCom 管线最前端，与语义编码器级联 |
| 标准 SemCom 编解码（$\mathcal{E}/\mathcal{D}_{sem}$、$\mathcal{E}/\mathcal{D}_{ch}$） | 语义编码、信道编码与解码 | $I_e^*$ | $\tilde{z}_{sct}$、$\hat{I}_e^*$ | 被复用为公开传输路径；其语义特征被秘密解码模块旁路使用 |
| Secret Decoding Module（$\mathcal{D}_{scre}$） | 授权方秘密恢复 | $\tilde{z}_{sct}$（48×64×64） | $\hat{I}_s$（3×256×256） | 插在信道解码器与语义解码器之间，与公开重建路径解耦；仅授权用户持有 |
| Dual-Objective Joint Training | 联合优化全部模块 | 四项损失 | 参数更新 | 训练期把两分支的共享知识绑定在一起 |
| 授权生命周期机制（§IV-E） | 训练（同态加密）/分发与更新（PKI+数字签名）/本地执行与密钥（TEE）/唯一性（PUF）/撤销（证书撤销+TEE 校验） | — | 部署合规性 | 论文以文字描述，无实验数据验证 |

### 4.4 公式、算法和机制解释

- **信道模型（Eq. 3–4）**：AWGN 下 $\tilde{x}=x+n,\ n\sim\mathcal{N}(0,\sigma^2 I),\ \sigma^2=P/10^{\gamma/10}$；慢衰落 Rayleigh 下 $\tilde{x}=x\cdot h+n,\ h\sim\mathcal{CN}(0,1)$——$\gamma$ 显式输入模型以做自适应调制。
- **隐藏模块（Eq. 10–16，Algorithm 1）**：$I_e^*=\psi(\mathcal{H}(\phi(I_c),\phi(I_s)))$，三阶段为特征提取、特征融合与隐藏、上采样与构造；融合网络卷积核形状 $W_1\in\mathbb{R}^{64\times128\times1\times1}$、$W_2\in\mathbb{R}^{64\times64\times3\times3}$、$W_3\in\mathbb{R}^{32\times64\times3\times3}$；构造块转置卷积核 $W_1^\top\in\mathbb{R}^{32\times32\times4\times4}$（s=2, p=1）。
- **秘密解码模块（Eq. 17–20，Algorithm 2）**：维度路标 48→64→64→64→32→16→3，前五层 Conv3×3 (s=1,p=1)+BN+ReLU 保持空间分辨率，末层 Sigmoid 投影到 RGB 后 $\hat{I}_s=\mathrm{Upsample}(f_{out},\mathrm{scale}=4,\mathrm{bilinear})$；上采样无学习参数。
- **双目标联合训练（Eq. 21–24）**：$R_r=\lambda_r\mathbb{E}[\mathcal{L}(\mathcal{D}_{sem}(\tilde{z},\gamma),I_e)]$（公开重建，MSE）、$R_h=\lambda_h\mathbb{E}[\mathcal{L}(\mathcal{E}_{scre}(I_c,I_s),I_c)]$（stego 与封面相似，保证视觉不可察觉）、$R_u=\lambda_u\mathbb{E}[\mathcal{L}(\mathcal{D}_{sem}(\tilde{z}_{sct},\gamma),I_e^*)]$（未授权分支约束）、$R_a=\lambda_a\mathbb{E}[\mathcal{L}(\mathcal{D}_{scre}(\tilde{z}_{sct},\gamma),I_s)]$（授权秘密恢复）。权重经消融选定 $\lambda_r=1.0$、$\lambda_h=0.01$、$\lambda_u=0.01$、$\lambda_a=0.05$（§V-C, Fig. 8；$\lambda_u$ 增大会同时严重破坏两个分支，故取小值做稳定项）。
- **鲁棒性机理（§IV-F）**：论文对四类攻击给出定性论证——模型窃取/蒸馏中潜空间 $z$ 的非线性耦合阻止仿制语义-秘密关系；剪枝/微调破坏 $\mathcal{L}_{sem}$ 与 $\mathcal{L}_{scre}$ 的正则化梯度平衡导致特征错配而不泄露内容；token 反演因随机信道 $\mathcal{C}(\cdot)$ 与不可逆 tokenization 而病态；Grad-CAM 探针因模型正则化强制 $z$ 与秘密映射统计独立而只暴露公开语义。

### 4.5 方法优势

- **把隐蔽性做成语义问题**：秘密以语义形式嵌入封面并随语义特征传输，而非扰动物理符号，因此在高 SNR 下公开链路的保真度几乎不受影响（SemCom SSIM 仍 >99.5%）。
- **授权差异化的设计**：秘密解码模块只作用于中间语义特征、只发给授权用户；未授权方拿到的是同一段语义特征却无法解码秘密，天然形成"同信道、不同权限"的访问控制。
- **对信道压缩鲁棒**：秘密恢复在 CR 0.2–0.9 全区间几乎不变（AWGN 约 31.3 dB），说明它依托的是共享嵌入而非压缩率敏感的特征带。
- **开销可控**：发送端参数 +2.4%、接收端 +2.0%，端到端 wall-clock 仅 +3.35 ms（5.64%）（Table IX）。

### 4.6 方法不足

- **仅图像模态**：论文明确当前只做图像传输，文本与多模态 SemCom 留待未来工作（§VI）。
- **鲁棒性论证以定性为主**：§IV-F 的四类攻击机理均为公式化叙述，量化结果全部来自有限的几张表（Tables XI–XVII），且部分"攻击"设定偏弱（如微调仅 2 个 epoch、lr=1e-5，作者自称 "weak"）。
- **秘密容量未评估**：没有讨论一幅封面最多能藏多少秘密信息（容量-保真度曲线缺失）。
- **安全性依赖假设**：TEE/PUF/PKI 的生命周期管理（§IV-E）纯属描述，无实现与评测；未给出密码学意义上的隐蔽性/安全性证明。
- **威胁模型没有形式化**：未定义明确的 warden/攻击者能力边界；StegExpose/SRNetLite 均标注 "Lite"，不是最强隐写分析对手。

---

## 5. 与其他方法对比

### 5.1 与主流方法的本质区别

主流隐蔽通信在**信号/比特层**做隐蔽（扩频、功率控制、波束成形、协议冗余位），与语义特征学习脱钩，且受 Shannon 容量约束；本文把隐蔽转移到**语义层**：秘密成为封面语义的一部分，经 DeepJSCC 式联合信源信道编码传输，作者据此提出 "task-level beyond-Shannon advantage"——在图 1(b) 中，传统方法速率不超过 Shannon 极限，而 SemCom+Stega 在比特级阈值以下仍保持非零任务效用。与同为图像隐写的 Baluja/HiNet/DeepMIH 相比，本文不追求"隐藏容量"或"可逆性"，而追求"传输链路整合 + 授权差异"。

### 5.2 创新点分析

| 创新点 | 具体内容 | 贡献度 | 是否可迁移 |
|---|---|---|---|
| SemCom × 图像隐写的首个端到端融合 | 隐藏模块前置 + 秘密解码模块插在信道解码之后，两模块与语义编解码器一体训练 | 高 | 是（任何"主任务 + 隐蔽副任务"的联合编码场景） |
| 权限差异化的解码设计 | 未授权方只跑公开语义解码器；秘密解码器只对授权方开放且直接读中间特征 | 高 | 是（授权访问控制、分级信息投递） |
| 四项风险加权的双目标联合训练 | $R_r/R_h/R_u/R_a$ 及权重消融（$\lambda_r{=}1.0,\lambda_h{=}0.01,\lambda_u{=}0.01,\lambda_a{=}0.05$） | 中 | 是（多任务损失的权重工程范式） |
| 三维隐蔽性评估协议 | 视觉不可感知（PSNR/SSIM）+ 统计一致性（直方图 L1、高频能量差）+ 检测器不可检测（StegExpose/SRNetLite/HiNetDetectorLite） | 中 | 是（隐写/隐蔽信道论文的评测模板） |
| 对抗鲁棒性实验矩阵 | 模型窃取、蒸馏、剪枝、微调、token 反演、Grad-CAM 六类攻击 | 中 | 部分（具体攻击设定偏弱，需按更强威胁模型重做） |

### 5.3 适用场景

私密内容的无线图像传输场景（AIoT、VR/AR、智慧城市等 SemCom 应用，§I）：需要在正常语义传输中顺带把真实数据只送达授权终端（多客户端下的授权数据分发），或者需要验证"封面之外还藏着东西"的对抗环境。前提是收发双方共享同一套训练好的语义-隐写编解码器与授权密钥体系。

### 5.4 方法对比表

| 方法 | 优点 | 缺点 | 本文改进点 |
|---|---|---|---|
| 扩频信号 / 噪声自适应功率控制 / 隐蔽波束成形 | 在传统比特通信下有理论支撑（Shannon 容量、平方根律） | 直接扰动物理符号 → 封面失真更大（PSNR/SSIM 差）、比特恢复在信道差时崩塌 | 秘密以语义特征承载，公开链路保真度几乎不受损；低比特可靠性以下仍有任务效用 |
| 传统深度隐写（Baluja 2017、Baluja 2020、HiNet、DeepMIH） | 嵌入容量与视觉质量成熟 | 只在图像域做嵌入-恢复，不涉及有损传输链路，无权限区分 | 嵌入知识与语义编解码联合优化，随 SemCom 管线一并传输 |
| 语义隐写 Huo et al. [42] | 首次在语义通信中嵌入比特级消息 | 比特级消息、无图像到图像传输、无授权/未授权区分 | 图像到图像的可授权传输范式 |
| 独立训练（SemCom 与秘密分支分开训） | 实现简单 | 秘密恢复显著更差（AWGN 30 dB 下 27.0 dB vs 31.3 dB；Rayleigh 下 25.0 dB vs 30.9 dB） | 联合训练使共享表征同时服务两个目标 |
| Secure/Robust SemCom 基线 [45][46] | 各自解决安全性/鲁棒性问题 | 对黑盒窃取/蒸馏仍可被大量抽取（[45] N=400 查询即达 41.59 dB；[46] N=5000 查询学生达 53.05% vs 教师 72.32%） | 论文报告自身对窃取/蒸馏更稳（秘密恢复塌到 7.32 dB/6.93 dB，KL 达 $10^6$–$10^7$ 量级） |

---

## 6. 实验表现与优势

### 6.1 实验设计和设置

数据集 Tiny-ImageNet 与 DIV2K，各随机选 800 张（400 封面 + 400 秘密），生成 400 组 stego；图像归一化到 [0,1]。语义编码器采用四种架构 JSCC-V、JSCC、JSCC-F、JSCC-Q，各自在 AWGN 与 Rayleigh 衰落信道下预训练与评估；Adam 优化器，lr $5\times10^{-5}$，训练 1,500 epochs，batch size 4，输入统一 256×256（§V-A）。评估指标为 PSNR（Eq. 25）、SSIM（Eq. 26）、LPIPS（Eq. 27），并另设隐蔽性（§V-B）与开销（§V-D）两组实验。

### 6.2 数据集

| 数据集 | 规模 | 分辨率 | 用途 | 说明 |
|---|---|---|---|---|
| Tiny-ImageNet [43] | 100,000 张、200 类 | 64×64 | 低分辨率图像传输与分类来源 | 实验中各取 800 张（400 cover / 400 secret） |
| DIV2K [44] | 1,000 张 | 原始 2K，双三次降采样至 256×256 | 高分辨率重建/超分来源 | 同上取 800 张配对 |

### 6.3 Baseline

对比分三类：(1) **预实验**：扩频信号、噪声自适应功率控制、隐蔽波束成形三种经典隐蔽通信基线（30 dB SNR 下比较 PSNR/SSIM/传输速率，Fig. 1）；(2) **训练策略对比**：SemCom 与秘密解码模块**独立训练**的 baseline（Fig. 7）；(3) **外部安全/鲁棒 SemCom 基线**：Secure SemCom [45]（N=400 查询蒸馏）与 Robust SemCom（masked VQ-VAE codebook）[46]（N=5000 查询蒸馏）（Table XIII）。

### 6.4 评价指标

PSNR（dB）、SSIM（%）、LPIPS（越低越好）用于重建质量；隐蔽性用 PSNR/SSIM（封面 vs stego）、灰度直方图 L1 距离、高频能量比及其差值、以及 StegExpose/SRNetLite/HiNetDetectorLite 的准确率、TPR/FPR、平衡准确率 BAcc 与平均得分；开销用参数量、FLOPs、延迟、峰值内存；攻击实验额外用 KL 散度衡量潜特征分布偏移。

### 6.5 关键实验结果

| 任务/数据集 | 指标 | 本文方法 | 最优对比方法 | 提升 | 说明 |
|---|---|---:|---:|---:|---|
| Tiny-ImageNet, AWGN 30 dB（JSCC-V） | Secret PSNR / SSIM / LPIPS | 31.32 dB / 91.29% / 0.0445 | 独立训练 baseline 27.0 dB / 84.1% / 0.0541 | +4.3 dB | Table III(a)、Fig. 7 |
| Tiny-ImageNet, AWGN 30 dB（四架构） | SemCom PSNR | 44.07–49.35 dB，SSIM >99.5% | — | — | Table III；JSCC-V 最高 49.35 dB |
| Tiny-ImageNet, Rayleigh 30 dB | Secret PSNR | 28.73–31.59 dB（各架构） | 独立训练 25.0 dB | +3.9–6.6 dB | Table III、Fig. 7 |
| DIV2K, AWGN 30 dB | SemCom / Secret PSNR | 37.9–40.8 dB / 27–28 dB | — | — | §V-C 正文（高分辨率下绝对值下降但趋势一致） |
| DIV2K, Rayleigh 30 dB | SemCom / Secret PSNR | 38.8–41.0 dB / 26–27.7 dB | — | — | §V-C |
| 隐蔽性（封面 vs stego） | PSNR / SSIM | 38.31 dB / 99.39% | — | — | Table V（均值±std 附于表中） |
| 隐写分析检测器 | BAcc / 准确率 | StegExpose BAcc 0.583；SRNetLite 38.33%；HiNetDetectorLite 45.00% | 随机猜测 0.5 / 50% | — | Table VI，接近/低于随机 |
| CR 消融（AWGN, 30 dB） | 公开 PSNR / 秘密 PSNR | CR 0.2→0.8 时 14.78→49.35 dB / 秘密恒约 31.3 dB | — | — | Table VII；CR 0.9 公开性能反而略降（26.93 dB） |
| 模型窃取（AWGN 30 dB, CR 0.8） | 学生秘密恢复 | 7.32 dB / 13.1% SSIM（原模型 31.19 dB / 91.3%） | 教师 48.18 dB / 99.7%（公开路径） | — | Table XI；KL($z_T\|z_S$)=2.14e6 |
| 知识蒸馏（N=5000 查询） | 学生秘密恢复 | 6.93 dB / 14.9% SSIM | 教师 31.19 dB / 91.3% | — | Table XII；KL 达 1.52e7 / 6.83e5 |
| 剪枝（10%） | SemCom / Secret PSNR | 42.99 dB / 30.66 dB | 无剪枝 49.88 dB / 31.33 dB | −0.67 dB（secret） | Table XIV；20% 稀疏时 SemCom −17.4 dB、secret −4.54 dB |
| 弱微调攻击 | 秘密 PSNR 变化 | −0.86 dB（SSIM −2.07%） | — | — | Table XV（论文自称 weak：2 epochs、lr 1e-5） |
| 开销 | 参数/延迟/显存 | Tx +0.153M (+2.4%)、Rx +0.126M (+2.0%)；E2E wall-clock 59.36→62.70 ms (+5.64%) | — | — | Table IX |

### 6.6 优势最明显的场景

- **秘密恢复随 SNR 单调提升且对信道类型不敏感**：AWGN 10 dB 时秘密恢复 15.87 dB（JSCC-V）/18.26 dB（JSCC），30 dB 时升至 31.3/31.6 dB；Rayleigh 下仍保持 30.9–31.6 dB（Table III）。论文指出联合训练相独立训练的增益在高 SNR 尤其明显（Fig. 7 正文）。
- **信道压缩率极端变化**：CR 从 0.2 到 0.8，公开链路 PSNR 变化 35 dB，而秘密恢复几乎不动（31.3 dB ± 0.05），说明隐蔽分支独立于压缩率。
- **高隐蔽性要求**：StegExpose 的 FPR 0.595 使 BAcc 仅 0.583，两类轻量 CNN 检测器准确率低于随机，适合"不可检测性优先"的场景。

### 6.7 局限性

- 只在图像数据集（Tiny-ImageNet/DIV2K）与图像 SemCom 上验证，未涉及文本、多模态与生成式任务（§VI 列作未来工作）。
- 秘密隐藏/恢复模块本身是固定 CNN，未讨论容量上限、多秘密并发、秘密-封面尺寸不匹配等实际约束。
- 部分鲁棒性实验强度偏弱（微调攻击仅 2 个 epoch 且 lr=1e-5，作者自称 "weak system fine-tuning"）；token 反演与 Grad-CAM 表格（Tables XVI/XVII）中的指标存在"复用合法秘密解码器评估"的乐观口径（作者已在 §V-E 说明该优势真实攻击者不可得）。
- 未给出计算成本在端侧设备上的实测；TEE/PUF/PKI 生命周期机制无实验支撑。
- 论文自述 "first work to combine SemCom and image steganography"，但未做与 Huo et al. [42] 语义隐写的直接定量对比。

---

## 7. 学习与应用

### 7.1 是否开源？

解析稿未提及代码仓库、模型权重或 artifact（`code` 记 unknown）。

### 7.2 复现关键步骤

1. 搭标准 SemCom 管线：语义编码器（residual block + GDN + SNR-aware attention）+ 压缩掩码与功率归一化 + AWGN/Rayleigh 信道 + 信道解码 + 语义解码（反卷积 residual block + attention），$\gamma$ 与 $\rho$ 显式喂入模型。
2. 实现秘密隐藏模块：$\phi$ 共享编码器（3×3、4×4 卷积 + ReLU）→ Concat → $\mathcal{H}$（1×1 + 2×3×3 卷积、BN）→ $\psi$（转置卷积 s=2/p=1 + 2 卷积 + Tanh）。
3. 实现秘密解码模块：48×64×64 输入 → 5 层 Conv3×3(1,1)+BN+ReLU（通道 64/64/64/32/16）→ Conv3×3 到 3 通道 + Sigmoid → 双线性上采样 ×4 到 256×256。
4. 联合训练：四项 MSE 风险按 $\lambda_r{=}1.0,\lambda_h{=}0.01,\lambda_u{=}0.01,\lambda_a{=}0.05$ 加权，Adam，lr $5\times10^{-5}$，1500 epochs，bs 4；四种语义架构各自分别训练（每架构 AWGN/Rayleigh 两版）。
5. 评测：主指标 PSNR/SSIM/LPIPS；隐蔽性按封面-stego 的 PSNR/SSIM、直方图 L1、高频能量差与三类检测器；攻击实验用窃取/蒸馏/剪枝/微调/token 反演/Grad-CAM 六个脚本。

### 7.3 关键超参数、预处理和训练细节

- 损失权重：$\lambda_r=1.0$、$\lambda_h=0.01$、$\lambda_u=0.01$、$\lambda_a=0.05$（Fig. 8 消融：$\lambda_r$ 主要影响公开保真，$\lambda_h$ 无一致增益取小值，$\lambda_u$ 过大会同时破坏两分支，$\lambda_a$ 从 0 快速增益后饱和）。
- 训练：Adam，lr $5\times10^{-5}$，1,500 epochs，batch size 4；所有图像重采样到 256×256 并归一化 [0,1]。
- 隐含层维度：秘密解码输入 48×64×64、输出 256×256×3；隐藏模块融合层与构造层的卷积核形状如 Eq. 14/16 所列。
- 分辨率泛化：64×64 / 256×256 / 512×512 三档（Table VIII：公开 43.23/49.35/47.54 dB；秘密 28.71/31.32/30.83 dB）。

### 7.4 能否迁移到其他任务？

- **"主任务编码器 + 权限分级副解码器"骨架**可迁移到任何"公开信道 + 私有信息"的联合传输场景（如联邦/边缘推理中的私有分支、多级用户的服务等级控制）。
- **四项风险 + 权重消融**的联合训练范式可迁移到多任务学习的损失平衡问题（尤其"未授权分支要退化但不能崩坏"这种不对称目标）。
- **隐蔽性三维评估协议**（视觉 / 统计 / 检测器）可迁移到网络隐蔽信道（covert channel）论文的评测设计，例如 KB 中 QuicCourier 类工作的评测可以补充"直方图距离、频域能量"这类统计一致性指标。
- 与流量分析的关系：本文不涉及网络流量侧信道，其"载体内容"是图像语义而非报文序列；但对 KB 中"隐蔽信道检测"方向是一个反向参照——当隐蔽信息嵌入的是**语义特征**而非比特时，基于统计指纹的检测器可能失效。

### 7.5 对我的研究有什么启发？

- **隐蔽性与主任务的耦合方式**是核心变量：本文用"共享知识 + 联合训练"换取了"检测器难以察觉 + 主任务几乎无损"，与流量分析中"隐蔽信道"研究形成镜像问题（一个是藏，一个是找）。
- **权限分级的信道设计**值得借鉴：同一段网络数据对不同权限的接收方呈现不同内容，这种"同信道不同语义"的思路可以启发对加密流量中"应用层权限差异是否产生流量特征差异"的研究。
- **权重消融的写法**：Fig. 8 逐个扫 $\lambda$ 并明确说明每个权重的角色（谁影响公开、谁饱和、谁有害），是一段结构清晰的损失工程叙事，可直接借用为写作模板。
- **注意论文的自我定位边界**：作者把 §IV-E 授权生命周期写成部署叙事而非实验，把 §IV-F 攻击机理写成公式化论证；引用该文时不宜把这些当作已验证结论。
- **与 KB 的接口**：本文与现有知识库（加密流量分类/WF/恶意流量检测）主题距离较远，唯一可建立的联系是"隐蔽通信 vs 隐蔽信道检测"这一对抗对；引用时应明确归入"隐蔽传输"而非"流量分析"。

---

## 8. 总结

### 8.1 核心思想

> 把秘密作为语义藏进封面，再随语义通信链路一起传。

### 8.2 速记版 Pipeline

1. 发送端：隐藏模块 $\psi(\mathcal{H}(\phi(I_c),\phi(I_s)))$ 把秘密图像融进封面得到 stego 输入。
2. 传输：stego 走标准 SemCom（语义编码 → 压缩掩码 + 功率归一化 → AWGN/Rayleigh → 信道解码）产生中间语义特征。
3. 接收端：未授权用户只跑语义解码器拿到封面语义；授权用户额外用 6 层卷积秘密解码器从 $\tilde{z}_{sct}$ 恢复 256×256 秘密。
4. 训练：$R_r$（公开重建）+ $R_h$（stego≈封面）+ $R_u$（未授权约束）+ $R_a$（授权恢复）四项加权联合优化，权重 $\lambda_r{=}1.0,\lambda_h{=}\lambda_u{=}0.01,\lambda_a{=}0.05$。
5. 结果：秘密恢复约 31 dB/91%/LPIPS 0.04；StegExpose BAcc 0.583；端到端延迟开销 +5.64%。

---

## 9. Obsidian 知识链接

### 9.1 相关概念

- 无直接对应。本文属于无线语义通信 + 图像隐写（隐蔽传输），知识库现有概念页（网站指纹、加密流量分析、恶意流量检测、隧道检测等）均无对应主题；论文本身也未引用任何网络流量分析文献。

### 9.2 相关方法

- [[convolutional-network]]（弱相关：隐藏与秘密解码模块均为纯卷积编解码网络，但不涉及任何流量表征学习）

### 9.3 相关任务

- 无（现有任务白名单中不存在隐蔽传输/隐写任务页）。

### 9.4 可更新的综述页面

- 无直接对应综述页；如需收录，需先新增"隐蔽通信/隐蔽信道"主题页。

### 9.5 可加入的对比表

- 无（论文未开源，所用数据集为图像数据集，不适合并入现有流量侧对比表）。

主题相近的现有论文笔记（**未被本文引用**，仅作知识库内横向关联）：

- [[2026-TIFS-HookSteg__A_Truly_Lossless_Steganography_Based_on_Process_Hooking_for_Lossy_Network_Channels]]（同属"以隐写承载隐蔽传输"，但该工作走端侧进程 Hook 路线）
- [[2026-CS-Hiding_the_Trees_in_the_Forest__Building_Network_Covert_Channels_with_Hash-Based_Covert_Carrier_Filtering]]（网络层隐蔽信道构造，与本文的语义层隐蔽形成对照）
- [[2025-TDSC-QuicCourier__Leveraging_the_Dynamics_of_QUIC-_Based_Website_Browsing_Behaviors_Through_Proxy_for_Covert_Communication]]（协议行为层隐蔽信道）

---

## 10. 证据记录

| 关键观点 | 论文依据 | 位置 |
|---|---|---|
| 秘密高保真恢复（AWGN 30 dB） | Tiny-ImageNet JSCC-V：31.32 dB / 91.29% / LPIPS 0.0445 | §V-C, Table III(a) |
| 四种语义架构下公开传输几乎无损 | 30 dB 时 SemCom PSNR 44.07–49.35 dB、SSIM >99.5%、LPIPS <0.002 | §V-C, Table III |
| 高分辨率下性能保持 | DIV2K 30 dB：SemCom 37.9–40.8 dB，秘密 27–28 dB / 87–89% SSIM | §V-C, Table IV/正文 |
| 联合训练显著优于独立训练 | AWGN 30 dB：31.3 vs 27.0 dB、91.3% vs 84.1%；Rayleigh：30.9 vs 25.0 dB | §V-C, Fig. 7 |
| 视觉不可感知 | 封面 vs stego：PSNR 38.31 dB、SSIM 99.39%、高频能量差 $-1.13\times10^{-3}$ | Table V |
| 检测器不可检测 | StegExpose BAcc 0.583（TPR 0.760/FPR 0.595）；SRNetLite 38.33%；HiNetDetectorLite 45.00% | Table VI |
| 秘密恢复对 CR 不敏感 | CR 0.2–0.9 下秘密 PSNR 恒约 31.3 dB / 91.3%，同时公开 PSNR 14.78→49.35 dB | Table VII |
| 开销轻量 | Tx 参数 +2.4%、FLOPs +20.2%、延迟 +0.597 ms；Rx +0.016 GFLOPs；E2E wall-clock +3.35 ms (5.64%) | Table IX |
| 对抗攻击下秘密路径不可复制 | 窃取：学生秘密 7.32 dB/13.1%；蒸馏：6.93 dB/14.9%（原模型 31.19 dB/91.3%） | §V-E, Tables XI/XII |
| 剪枝与微调韧性 | 10% 剪枝秘密 30.66 dB；弱微调后 −0.86 dB / −2.07% | Tables XIV/XV |

---

## 11. 原始资料链接

- PDF：00-inbox/PDFs/2026-TMC-When_Steganography_Meets_Semantic_Communication__An_Authorizable_Data_Transmission_Paradigm.pdf
- MinerU Markdown：02-parsed-markdown/2026-TMC-When_Steganography_Meets_Semantic_Communication__An_Authorizable_Data_Transmission_Paradigm.md

---

## 12. 后续问题

- 秘密容量（一幅封面能藏多少信息）与容量-保真度曲线缺失，无法判断该范式相对传统隐写的实用上限。
- "未授权用户察觉不到秘密"仅由三类检测器（其中两类为 "Lite" 版本）间接支持，缺少自适应/白盒隐写分析对手下的评估。
- §V-E 的 token 反演与 Grad-CAM 表格（Tables XVI/XVII）中秘密恢复指标（106.76 dB、∞ PSNR）源于"复用合法解码器"的评估口径，作者自陈真实攻击者不具备该条件；引用这些数字时需注意解释。
- Table X 的隐蔽基线延迟对比只列了 SS 与 NAPC 两行（表中出现第三行的空位/缺失），解析稿可能丢行，需要核对 PDF。
- §IV-E 的授权生命周期机制（同态加密训练、PKI 分发、TEE、PUF、撤销）无任何实验或原型验证。
- MinerU 解析问题：标题与部分正文为 small-caps 字体，解析稿出现 "EMANTIC Communication"、"ofour"、"Sem-Com" 等连字/大写碎片（引用时已还原）；Eq. 14 与 Eq. 16 的卷积表达式在解析稿中括号错位（如 $W_2*$ 后缺失操作数），无法逐项复核；Table III 的 (c)/(d) 子表与表头在正文中出现交错错位。

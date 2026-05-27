---
type: comparison
name: dataset-comparison-table
created: "2026-05-27"
updated: "2026-05-27"
---

# Dataset Comparison Table

## 数据集对比表

| 数据集 | 任务 | 数据类型 | 规模 | 优点 | 局限 | 相关论文 |
|---|---|---|---|---|---|---|
| ISCX-VPN (2016) | VPN 加密流量分类（应用识别 / 服务分类） | 流量包（PCAP） | Service: 3,694 flows / 60K packets (12类)；App: 2,329 flows / 77K packets (17类) | 领域最早且最广泛使用的 VPN 分类基准；涵盖 VPN 和非 VPN 流量；包含应用和服务两个粒度的标注 | 98.9% 流量为未加密流量（S&P 2025 SoK 指出）；使用已弃用的 3DES、AES-CBC 等旧密码算法；数据量偏小，类别不平衡 | ET-BERT (WWW 2022)；SoK (S&P 2025)；TSCRNN；Deeppacket |
| ISCX-Tor (2016) | Tor 匿名流量分类（应用识别） | 流量包（PCAP） | 3,021 flows / 80K packets (16类) | 唯一广泛使用的 Tor 应用分类公开数据集；覆盖 16 种常见 Tor 应用 | 89.3% 流量为未加密流量（S&P 2025 SoK 指出）；主要使用 AES-CBC 旧密码；规模较小，类别不平衡 | ET-BERT (WWW 2022)；SoK (S&P 2025)；FEC-OSL (TIFS 2026) |
| USTC-TFC (2016) | 恶意软件加密流量检测 | 流量包（PCAP） | ~9,853 flows / ~97K packets (20类：10恶意+10良性) | 同时包含恶意和良性流量，适合二分类和多分类；覆盖多种恶意软件家族；在恶意软件检测领域广泛使用 | 94.7% 流量为未加密流量（S&P 2025 SoK 指出）；密码算法过时；恶意软件样本来自 2016 年，时效性有限 | ET-BERT (WWW 2022)；SoK (S&P 2025)；FEC-OSL (TIFS 2026)；SmartDetector (TIFS 2025) |
| Cross-Platform Application | 跨平台移动应用加密流量识别 | 流量包（PCAP） | iOS: 20,858 flows / 707K packets (196类)；Android: 27,846 flows / 656K packets (215类) | 覆盖 iOS 和 Android 双平台，支持跨平台泛化研究；类别数量大（200+），接近真实场景；在预训练模型研究中被广泛采用 | 69.7% 流量为未加密流量（S&P 2025 SoK 指出）；主要使用 AES-CBC 旧密码；部分类别样本数少，类别不平衡 | ET-BERT (WWW 2022)；SoK (S&P 2025)；FlowPrint (NDSS 2020) |
| CSTNET-TLS 1.3 | TLS 1.3 网站加密流量识别 | 流量包（PCAP） | 46,372 flows / 581K packets (120类) | 首个 TLS 1.3 公开数据集；100% 加密流量，无未加密数据泄露问题；使用 AES-GCM 现代密码算法；从 Alexa Top-5000 采集，贴近真实场景 | 类别数量有限（120类）；仅覆盖 TLS 1.3 单一协议；通过 SNI 标注，TLS 1.3 ECH 机制普及后标注方式受限 | ET-BERT (WWW 2022)；SoK (S&P 2025)；MM4flow (CCS 2025) |
| CipherSpectrum | TLS 1.3 加密流量分类（现代基准） | 流量包（PCAP） | 120,000 sessions (40类 x 3密码套件 x 1,000 sessions) | 100% 加密流量；统一包含 TLS 1.3 三种推荐密码套件（AES-128-GCM, AES-256-GCM, ChaCha20-Poly1305）；类别平衡；由 S&P 2025 SoK 论文提出，旨在替代过时数据集 | 自动化脚本采集，缺乏人工交互，真实性待验证；仅 40 个类别；采集时间为 2024 年初，可能无法反映最新网络变化 | SoK (S&P 2025) |
| CIC-IDS-2017 | 网络入侵检测 / 恶意流量检测 | 流量包（PCAP）+ CSV 特征 | 约 2,800 万条网络连接记录 (7类攻击+正常) | 涵盖多种现代攻击类型（暴力破解、DoS、Web 攻击、渗透等）；提供五天多天采集的真实流量；预处理特征丰富，开箱即用 | 部分攻击流量非加密；数据量大导致训练时间长；存在已知的标签噪声和重复记录问题 | SmartDetector (TIFS 2025)；MetaMRE (Computer Networks 2023)；FEC-OSL (TIFS 2026) |
| CIC-DDoS-2019 | DDoS 攻击加密流量检测 | 流量包（PCAP）+ CSV 特征 | 约 5,000 万条网络连接记录 (13类 DDoS 攻击+正常) | 覆盖 13 种最新 DDoS 攻击变体；模拟真实 ISP 网络环境；包含反射型和直接型 DDoS 攻击 | 数据集规模庞大，处理和训练开销高；部分攻击在加密场景下代表性有限；仅聚焦 DDoS 单一攻击类型 | SmartDetector (TIFS 2025) |
| DoHBrw-2020 | DNS-over-HTTPS 流量检测 | 流量包（PCAP） | 约 60 万条 DoH 流量记录 (正常 DoH + 恶意 DoH) | 覆盖新兴的 DoH 加密 DNS 协议；同时包含正常和恶意 DoH 流量；在加密 DNS 分析领域具有独特价值 | 领域相对小众，使用者较少；DoH 协议本身在演化，数据时效性受限；类别较少（二分类为主） | SmartDetector (TIFS 2025) |
| DataCon2021-p2 | 加密隧道下网站流量识别 | 流量包（PCAP） | 4.6 GB (22类) | 聚焦加密隧道场景（通过代理访问网站），具有实际应用价值；所有基于 byte stream 的方法在此数据集上几乎完全失效，凸显 packet length 行为模态的重要性 | 类别数量适中（22类）；数据来源和采集方式公开信息有限；主要在中国网络环境下采集 | MM4flow (CCS 2025) |
| NUDT_MobileTraffic | 移动应用加密流量识别 | 流量包（PCAP） | 707 GB (300类，每类 200 训练样本) | 大规模类别覆盖（300类移动应用）；在 few-shot 场景下具有挑战性；数据量充足 | 数据量极大（707 GB），处理和训练开销高；公开获取途径有限；主要在中国移动网络环境下采集 | MM4flow (CCS 2025) |
| DF95 (Deep Fingerprinting) | Tor 网站指纹攻击（闭世界） | 流量方向序列 | 95 网站 x 1,000 traces = 95,000 traces | 网站指纹攻击领域最广泛使用的基准数据集；数据量充足，支持 10-fold 交叉验证；Alexa Top-100 网站，代表性强 | 闭世界假设过于理想化；仅使用 packet direction，忽略 packet size 和 timing；数据时效性下降（10-14 天后准确率下降） | Deep Fingerprinting (CCS 2018)；Swallow (CCS 2025)；Palette (S&P 2024) |
| Browser | 浏览器流量分类 | 流量包（PCAP） | 7.4 GB (4 类浏览器) | 区分不同浏览器的加密流量特征；在多模态方法研究中有参考价值 | 类别数量极少（仅 4 类）；任务相对简单；公开获取途径有限 | FlowPrint (NDSS 2020)；MM4flow (CCS 2025) |
| CIC-IOT2023 | IoT 加密流量分类与攻击检测 | 流量包（PCAP）+ CSV 特征 | 涵盖 33 种 IoT 设备和多种攻击类型 | 覆盖最新的 IoT 设备和攻击场景；设备种类丰富；包含正常和攻击流量 | IoT 流量模式相对简单，分类难度较低；数据集较新，使用论文尚少 | FG-SAT (TIFS 2025) |

## 数据集使用频率统计

基于扫描的论文笔记，各数据集在论文中被引用的频率如下：

| 数据集 | 引用次数 | 主要使用场景 |
|---|---|---|
| ISCX-VPN (2016) | 高 | VPN 分类、加密流量分类通用基准 |
| USTC-TFC (2016) | 高 | 恶意软件流量检测基准 |
| ISCX-Tor (2016) | 中 | Tor 流量分类 |
| Cross-Platform Application | 中 | 跨平台应用识别、预训练模型评估 |
| CSTNET-TLS 1.3 | 中 | TLS 1.3 流量分类、预训练模型评估 |
| CIC-IDS-2017 | 中 | 入侵检测、恶意流量检测 |
| CipherSpectrum | 低（新） | TLS 1.3 现代加密基准（替代过时数据集） |
| DF95 | 高（WF领域） | 网站指纹攻击/防御评估 |

## 关键发现

1. **过时数据集问题**：S&P 2025 SoK 论文实证揭示，ISCX-VPN、ISCX-Tor、USTC-TFC 等广泛使用的数据集包含大量未加密流量（89.3%--98.9%），且使用已弃用的密码算法（3DES、RC4、AES-CBC），可能导致分类器性能虚高。

2. **现代加密数据集稀缺**：仅有 CipherSpectrum 和 CSTNET-TLS 1.3 两个数据集完全使用 TLS 1.3 现代密码套件，且均为 100% 加密流量。

3. **领域碎片化**：不同研究方向（WF、恶意软件检测、应用分类、入侵检测）使用不同数据集，缺乏统一的跨任务基准。

4. **数据集规模趋势**：从 GB 级（ISCX 系列）到 TB 级（MM4flow 预训练数据），预训练范式推动了数据规模的大幅增长。

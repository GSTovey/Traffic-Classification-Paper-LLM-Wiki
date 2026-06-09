# Traffic Classification Paper Wiki

[中文说明](./README.zh-CN.md)

An Obsidian-based knowledge base for systematic literature review in **network traffic classification**, **encrypted traffic analysis**, and **traffic foundation models**. Contains 92 structured paper notes from top-tier venues (CCS, S&P, USENIX, NDSS, SIGCOMM, INFOCOM, AAAI, NeurIPS, TIFS, TSC, WWW, KDD, etc.), covering 2008--2026.

---

## Highlights

- **92 structured paper notes** with bilingual (Chinese/English) frontmatter, methodology analysis, and evidence tracking
- **40 deep-analyzed papers** (CCF A/B tier) with formula derivations, ablation studies, and cross-paper connections
- **35 knowledge pages**: 9 concepts, 8 methods, 8 tasks, 5 surveys, 5 comparison tables, 2 claim indexes
- **30 confirmed open-source methods** with GitHub/GitLab repositories
- **Research map** linking papers by topic, method, and venue

## Directory Structure

```
Traffic_Papers/
├── 00-inbox/
│   └── PDFs/              # 92 paper PDFs (source files)
├── 01-mineru-output/       # MinerU raw API output (gitignored, regenerable)
├── 02-parsed-markdown/     # MinerU-parsed markdown (92 files)
├── 03-paper-notes/         # Structured paper notes (92 files) ★
├── 04-concepts/            # Concept pages (9 files) ★
├── 05-methods/             # Method pages (8 files) ★
├── 06-tasks/               # Task pages (8 files) ★
├── 07-surveys/             # Survey pages (5 files) ★
├── 08-comparisons/         # Comparison tables (5 files, incl. open-source registry) ★
├── 09-claims/              # Claims & contradictions (2 files) ★
├── 10-outputs/             # Drafts, reports, reproduction notes
├── 00-dashboard/           # Reading queue, research map, open questions
├── scripts/                # MinerU batch parsing script
└── templates/              # Note templates
```

## Research Areas

| Area | Topics |
|------|--------|
| **Traffic Detection & Classification** | Encrypted traffic classification, malicious traffic detection, anomaly detection, tunnel detection |
| **Representation Learning & Foundation Models** | Pre-training (ET-BERT, YaTC, MM4flow), multi-modal fusion, contrastive learning |
| **Website Fingerprinting** | Attack (Deep Fingerprinting, Swallow) and defense (Palette, FRONT) |
| **Few-Shot & Open-Set Learning** | Meta-learning, semi-supervised, open-set recognition for traffic analysis |
| **Application Fingerprinting** | Mobile app identification, anonymous traffic classification (Tor, I2P) |

## Key Papers (Deep-Analyzed)

| Paper | Venue | Topic |
|-------|-------|-------|
| SoK: Decoding the Enigma | S&P 2025 | Systematic evaluation of 12 traffic classifiers |
| The Sweet Danger of Sugar | SIGCOMM 2025 | Debunking representation learning claims |
| MM4flow | CCS 2025 | Multi-modal pre-trained model |
| Training with Only 1.0 Samples | CCS 2025 | Cross-modality fusion with extreme few-shot |
| Swallow | CCS 2025 | Transfer-robust website fingerprinting attack |
| SmartDetector | TIFS 2025 | Contrastive learning for malicious traffic |
| ET-BERT | WWW 2022 | Pre-trained transformer for encrypted traffic |
| YaTC | AAAI 2023 | Masked autoencoder traffic transformer |
| AN-Net | WWW 2024 | Anti-noise anonymous traffic classification |
| Flowprint | NDSS 2020 | Semi-supervised mobile app fingerprinting |
| Palette | S&P 2024 | Real-time WF defense |
| RF | USENIX 2023 | Subverting WF defenses |
| Proxy Fingerprinting | USENIX 2024 | Encapsulated TLS handshake fingerprinting |
| FEC-OSL | TIFS 2026 | Open-set semi-supervised classification |

## Usage

This is an **Obsidian vault**. To use:

1. Clone this repository
2. Open the folder as a vault in [Obsidian](https://obsidian.md/)
3. Start from `00-dashboard/index.md` for navigation
4. Use `00-dashboard/reading-queue.md` to track reading progress
5. Use `00-dashboard/research-map.md` for topic-based exploration

## Tools & Pipeline

- **PDF Parsing**: [MinerU](https://github.com/opendatalab/MinerU) API for converting PDFs to structured Markdown
- **Note Generation**: Claude Code (AI-assisted structured note generation)
- **Knowledge Management**: Obsidian with Dataview plugin

## License

This repository contains academic paper notes for research purposes. All paper copyrights belong to their respective authors and publishers.

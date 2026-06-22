# Traffic Classification Paper Wiki

[中文说明](./README.zh-CN.md)

An Obsidian-based knowledge base for systematic literature review in **network traffic classification**, **encrypted traffic analysis**, and **traffic foundation models**. Contains 147 structured paper notes from top-tier venues (CCS, S&P, USENIX, NDSS, SIGCOMM, INFOCOM, AAAI, NeurIPS, TIFS, TSC, WWW, KDD, etc.), covering 2008--2026.

---

## Highlights

- **147 structured paper notes** with bilingual (Chinese/English) frontmatter, methodology analysis, and evidence tracking
- **74 deep-analyzed papers** (CCF A/B tier) with formula derivations, ablation studies, and cross-paper connections
- **39 knowledge pages**: 11 concepts, 8 methods, 8 tasks, 5 surveys, 5 comparison tables, 2 claim indexes
- **6 active research fronts** tracking convergent/divergent research questions with evidence chains and Auto Research guidance
- **Consensus weight system** with venue-tier × time-decay × citation-impact scoring for all claims
- **30 confirmed open-source methods** with GitHub/GitLab repositories
- **Bibliography** with 147 structured BibTeX entries (`bibliography.json` + `bibliography.bib`) sourced from CrossRef, OpenAlex, and Semantic Scholar
- **Research map** linking papers by topic, method, and venue
- **Personal research tracking** with isolated paper notes and research trajectory page (strictly separated from main KB)
- **Key figure gallery** with 148 auto-extracted framework/architecture figures from all 147 papers (see `10-outputs/key-figures/`)

## Directory Structure

```
Traffic_Papers/
├── 00-inbox/
│   └── PDFs/              # 147 paper PDFs (source files)
├── 01-mineru-output/       # MinerU raw API output (gitignored, regenerable)
├── 02-parsed-markdown/     # MinerU-parsed markdown (147 files)
├── 03-paper-notes/         # Structured paper notes (147 files) ★
├── 04-concepts/            # Concept pages (11 files) ★
├── 05-methods/             # Method pages (8 files) ★
├── 06-tasks/               # Task pages (8 files) ★
├── 07-surveys/             # Survey pages (5 files) ★
├── 08-comparisons/         # Comparison tables (5 files, incl. open-source registry) ★
├── 09-claims/              # Claims & contradictions (2 files) ★
├── 10-outputs/             # Drafts, reports, reproduction notes (gitignored)
│   └── key-figures/        # Auto-extracted framework figures (148 images)
├── 11-my-papers/           # Personal papers (isolated from main KB)
│   ├── notes/              # Individual paper notes
│   ├── my-research-thread.md  # Research trajectory
│   └── my-paper-registry.md   # Personal paper registry
├── 12-research-fronts/     # Research front tracking (6 fronts + index + template) ★
├── 00-dashboard/           # Reading queue, research map, open questions
├── bibliography.json       # Structured BibTeX metadata (147 entries)
├── bibliography.bib        # LaTeX-ready BibTeX file (ready to copy)
├── scripts/                # MinerU batch parsing + bibliography generation
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
| SoK: WF Defenses | S&P 2023 | Critical evaluation of website fingerprinting defenses |
| Countmamba | S&P 2025 | Generalized website fingerprinting attack |
| GAPDiS | CCS 2025 | Adversarial website fingerprinting defense |
| Great Firewall | USENIX 2023 | GFW encrypted traffic detection |
| Censored Planet | CCS 2020 | Internet censorship observatory |
| Censorship Evasion | USENIX 2025 | Unidentified protocol generation for censorship evasion |
| GGFAST | SIGCOMM 2023 | Automated traffic classifiers |

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
- **Bibliography**: `bibliography.json` + `bibliography.bib` — 147 structured BibTeX entries from CrossRef/OpenAlex/Semantic Scholar (86% with DOI)
- **Automated Workflow**: One-command paper ingestion pipeline (dedup → parse → note → knowledge layer update → bibliography → README/AGENTS sync)
- **Dedup Method**: Five-round joint matching (filename + title + abstract + DOI + author/year/venue)

## Workflow

When a new paper PDF is added to the vault, the system automatically:

1. Checks for duplicates against existing 147 papers (filename + title + abstract + DOI + author/venue)
2. Parses PDF via MinerU API (pauses to request API token if `MINERU_API_TOKEN` not set)
3. Extracts key framework/architecture figures via `extract_key_figures.py`
4. Generates a structured paper note with bilingual frontmaterial
5. Updates all related knowledge pages (concepts, methods, tasks, surveys, comparisons, claims)
6. Updates research front evidence chains if the paper is relevant to an active front
7. Updates global indexes (paper-registry, reading-queue, dashboard)
8. Updates `bibliography.json` and regenerates `bibliography.bib`
9. Syncs README.md and AGENTS.md statistics

Git commits are made **only on explicit request**. The `10-outputs/` directory (drafts, reports, proposals) is excluded from version control, except for `10-outputs/key-figures/` which contains auto-extracted framework figures. Personal papers in `11-my-papers/` are also excluded.

Personal papers (author's own work) are managed separately in `11-my-papers/` with strict isolation from the main knowledge base. They can read from the main KB (linking to concepts, methods, and existing papers) but never trigger automatic updates to it. When a paper is published or its quality is confirmed, it can be promoted to the main KB with full deep analysis while the personal note remains in `11-my-papers/` as a research trajectory reference.

## License

This repository contains academic paper notes for research purposes. All paper copyrights belong to their respective authors and publishers.

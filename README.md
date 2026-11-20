# Traffic Classification Paper Wiki

[中文说明](./README.zh-CN.md)

An Obsidian-based knowledge base for systematic literature review in **network traffic classification**, **encrypted traffic analysis**, and **traffic foundation models**. Contains 355 structured paper notes from top-tier venues (CCS, S&P, USENIX, NDSS, SIGCOMM, INFOCOM, AAAI, NeurIPS, TIFS, TSC, WWW, KDD, etc.), with bibliographic years from 2008 to 2027.

---

## Highlights

- **355 structured paper notes** with bilingual (Chinese/English) frontmatter, methodology analysis, and evidence tracking
- **142 deep-analyzed papers** (L3/L4 level) with formula derivations, ablation studies, and cross-paper connections
- **44 knowledge pages**: 13 concepts, 10 methods, 9 tasks, 5 surveys, 5 comparison tables, 2 active evidence indexes
- **7 active research fronts** tracking convergent/divergent research questions with evidence chains and Auto Research guidance
- **Cross-paper innovation workflow** linking evidence, assumptions, gaps, counterevidence, testable hypotheses, and research prioritization
- **Evidence review** records sources, study conditions, author-reported results, and signed cross-paper relations
- **101 public method or data artifacts**
- **Bibliography**: 373 BibTeX entries and 356 structured JSON records. All 355 registered papers have a linked citation record
- **Research map** linking papers by topic, method, and venue
- **Personal research tracking** with isolated paper notes and research trajectory page (strictly separated from main KB)
- **Key figure gallery** with 559 figures archived locally and selected previews in the public repo (see `10-outputs/key-figures/`)

## Directory Structure

```
Traffic_Papers/
├── 00-inbox/
│   └── PDFs/              # Archive location for paper and talk sources
├── 01-mineru-output/       # MinerU raw API output (gitignored, regenerable)
├── 02-parsed-markdown/     # MinerU text for archived sources
├── 03-paper-notes/         # Structured paper notes (355 active records) ★
├── 04-concepts/            # Concept pages (13 files) ★
├── 05-methods/             # Method pages (10 files) ★
├── 06-tasks/               # Task pages (9 files) ★
├── 07-surveys/             # Survey pages (5 files) ★
├── 08-comparisons/         # Comparison tables (5 files, incl. open-source registry) ★
├── 09-claims/              # Claims & contradictions (2 files) ★
├── 10-outputs/             # Drafts, reports, reproduction notes (gitignored)
│   └── key-figures/        # Selected public previews from the local figure archive
├── 11-my-papers/           # Personal papers (isolated from main KB)
│   ├── notes/              # Individual paper notes
│   ├── my-research-thread.md  # Research trajectory
│   └── my-paper-registry.md   # Personal paper registry
├── 12-research-fronts/     # Research front tracking (7 fronts + index + template) ★
├── 00-dashboard/           # Reading queue, research map, open questions
├── bibliography.json       # Structured citation metadata (356 records)
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
| [NestTor](03-paper-notes/2026-myPaper-TNSM-NestTor_Detecting_Tor-over-Proxy_Traffic_with_Factorized_Decisions.md) | TNSM 2026 | Factorized Tor-over-Proxy detection with domain/capture controls |
| [GraphIDS](03-paper-notes/2025-NIPS-Self-Supervised_Learning_of_Graph_Representations_for_Network_Intrusion_Detection.md) | NeurIPS 2025 | Joint graph representation and reconstruction for intrusion detection |
| [Nepco](03-paper-notes/2025-arXiv-Versatile_yet_Efficient_Network_Traffic_Analysis__Offloading_Network_Foundation_Model_to_SmartNIC.md) | arXiv 2025 | Early traffic analysis on SmartNIC under new-flow load |
| [SaTor](03-paper-notes/2026-S&P-SaTor__Exploring_Satellite_Routing_in_Tor_to_Reduce_Latency.md) | S&P 2026 | Tor circuit latency under satellite and terrestrial routing |
| [CryptoFormer](03-paper-notes/2026-TDSC-CryptoFormer__Multi-Currency_Traffic_Classification_Via_Two-Stage_Transformer_Architecture.md) | TDSC 2026 | Packet content and session behavior for multi-currency classification |
| [HAD](03-paper-notes/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection.md) | TIFS 2026 | Intrusion defense with a normal reference under temporal drift |
| [PS-ML](03-paper-notes/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures.md) | TON 2026 | Query-time correction of flow sizes across sketches |
| [SEDMS](03-paper-notes/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks.md) | TON 2026 | Dynamic selection of streaming telemetry metrics |

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
- **Bibliography**: `bibliography.bib` contains 373 entries, and `bibliography.json` contains 356 structured records. Existing BibTeX-only entries are preserved during incremental updates.
- **Automated Workflow**: One-command paper ingestion pipeline (dedup → parse → note → knowledge layer update → bibliography → README/AGENTS sync)
- **Dedup Method**: Five-round joint matching (filename + title + abstract + DOI + author/year/venue)

## Workflow

When a new paper PDF is added to the vault, the system automatically:

1. Checks for duplicates against registered papers (filename + title + abstract + DOI + author/venue)
2. Parses PDF via MinerU API (pauses to request API token if `MINERU_API_TOKEN` not set)
3. Extracts key framework/architecture figures via `extract_key_figures.py`
4. Generates a structured paper note with bilingual frontmaterial
5. Adds source-grounded facts and links to the relevant concepts, methods, tasks, surveys and comparisons
6. Registers relevant evidence as pending review and links it to the appropriate propositions and research fronts
7. Updates global indexes (paper-registry, reading-queue, dashboard)
8. Updates `bibliography.json` and regenerates `bibliography.bib`
9. Syncs README.md and AGENTS.md statistics

The [proposition index](09-claims/proposition-index.md) is the entry point for signed claims and their scope. The [seven-front review](09-claims/front-review-2026-11-18.md) records the signed findings and evidence gaps from the source review. The [migration map](09-claims/claim-migration-map.md) links earlier assessments and evidence records to their dispositions. Venue, year and citation information remain bibliographic metadata.

To regenerate the current collection counts, run `python3 scripts/research_capability_audit.py stats`. The counts use registered notes and their types.


The public repository contains the knowledge pages and selected source material. Some source files and reports are available in the local vault.

Git commits are made **only on explicit request**. The `10-outputs/` directory (drafts, reports, proposals) is excluded from version control, except for `10-outputs/key-figures/` which contains auto-extracted framework figures. Personal papers in `11-my-papers/` are also excluded.

Personal papers (author's own work) are managed separately in `11-my-papers/` with strict isolation from the main knowledge base. They can read from the main KB (linking to concepts, methods, and existing papers) but never trigger automatic updates to it. When a paper is published or its quality is confirmed, it can be promoted to the main KB with full deep analysis while the personal note remains in `11-my-papers/` as a research trajectory reference.

## License

This repository contains academic paper notes for research purposes. All paper copyrights belong to their respective authors and publishers.


### 2026-10-26 新增批次中的 L3 重点论文

| Paper | Venue | Topic |
|-------|-------|-------|
| HF-Transformer | INFOCOM 2026 | 非预训练包头字段加密流量分类 |
| PP-OpenNet | INFOCOM 2026 | 隐私保护开放集流量分类 |
| GenETC | TDSC 2026 | 动态图增强预训练流量分类 |

## Highlighted academic talk · 2026-11-17

[2026-COSINT-北邮时金桥](./03-paper-notes/2026-COSINT-北邮时金桥.md) covers DHOR low-base-rate detection and DHBCorr large-scale flow correlation. The local archive includes the original PDF and all 54 pages of summaries, rendered slides, and extracted text. Marked `academic-talk`, `L3`, `high relevance`, and `report-only`. At the time of intake, the collection included 342 standard paper notes and 1 academic talk.


### 2026-11-18 literature intake

The batch added 13 papers and linked the COSINT talk to literature on difficult negatives, link timing and processing cost. The new [network telemetry](04-concepts/network-telemetry.md) page covers bounded state, event-stream queries and measurement units.

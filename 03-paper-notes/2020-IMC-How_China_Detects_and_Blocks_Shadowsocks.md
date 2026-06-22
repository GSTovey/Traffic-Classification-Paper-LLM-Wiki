---
type: paper
title_original: "How China Detects and Blocks Shadowsocks"
title_cn: "中国如何检测和封锁 Shadowsocks"
authors: ["Alice (GFW Report)", "Bob (GFW Report)", "Carol (GFW Report)", "Jan Beznazwy", "Amir Houmansadr"]
year: 2020
venue: "ACM IMC 2020"
publication_status: published
doi: "10.1145/3419394.3423644"
url: "https://doi.org/10.1145/3419394.3423644"
pdf: "00-inbox/PDFs/2020-IMC-How_China_Detects_and_Blocks_Shadowsocks.pdf"
mineru_md: "02-parsed-markdown/2020-IMC-How_China_Detects_and_Blocks_Shadowsocks.md"
status: processed
reading_level: L2
research_area: ["censorship-circumvention", "tunnel-detection", "encrypted-traffic-analysis"]
task: ["tunnel-detection", "active-probing", "censorship-analysis"]
method: ["active-probing", "traffic-analysis", "tcp-fingerprinting", "packet-length-analysis", "entropy-analysis"]
dataset: ["self-collected-51837-probes", "4-month-measurement-experiment"]
code: "https://gfw.report/publications/imc20/en"
relevance: medium
created: "2026-06-21"
updated: "2026-06-21"
---

## 0. Basic Information

| Field | Content |
|---|---|
| Title | How China Detects and Blocks Shadowsocks |
| Authors | Alice, Bob, Carol (GFW Report); Jan Beznazwy (Independent); Amir Houmansadr (UMass Amherst) |
| Year | 2020 |
| Venue | ACM Internet Measurement Conference (IMC 2020) |
| DOI | 10.1145/3419394.3423644 |
| Keywords | Shadowsocks, Great Firewall, active probing, censorship circumvention, traffic analysis, replay attacks |
| Dataset | 51,837 active probes collected over 4 months (Sept 2019 - Jan 2020); random-data sink/responding experiments |
| Code | https://gfw.report/publications/imc20/en |
| Research Area | [[censorship-circumvention]], [[tunnel-detection]], [[encrypted-traffic-analysis]] |
| Confidence | high |

---

## 1. One-Sentence Summary

This paper reveals that China's Great Firewall detects Shadowsocks using passive traffic analysis (first-packet length and Shannon entropy) followed by 7 types of active probes (replay-based and random) sent in staged sequences from 12,300+ IP addresses controlled by centralized infrastructure, and presents a temporary TCP window-size-based mitigation that significantly reduces probing.

---

## 2. Core Contributions

### 2.1 Contribution List

1. **Two-stage detection mechanism revealed**: The GFW uses passive traffic analysis (first data packet length + entropy) to identify suspected Shadowsocks connections, then sends active probes in staged sequences to confirm. A single data packet suffices to trigger probing.

2. **Seven distinct probe types characterized**: Five replay-based probe types (R1-R5) and two non-replay types (NR1-NR2) are identified with specific length distributions and behavioral triggers. NR1 probe lengths cluster in trios around 8, 12, 16, 22, 33, 41, and 49 bytes, coinciding with Shadowsocks implementation parsing thresholds.

3. **Probing infrastructure fingerprinted**: 51,837 probes originate from 12,300 unique IPs in China, but TCP timestamp analysis reveals only ~7 underlying physical systems operating at 250 Hz and 1000 Hz clock rates, indicating centralized control.

4. **Staged probing behavior discovered**: The GFW sends R3/R4/R5 probes only after the server responds to R1/R2 probes, revealing a multi-stage confirmation system that operates progressively.

5. **Effective mitigation demonstrated**: Running brdgrd (bridge guard) to fragment the client's first handshake packet reduces probing to near-zero within hours, confirming packet length as a primary detection feature.

### 2.2 Key Differences from Related Work

| Existing Work | Difference | Section |
|---|---|---|
| Ensafi et al. (2015) — GFW active probing of Tor bridges | This paper discovers new probe types (R3-R5, NR1-NR2) specific to Shadowsocks; prober IP overlap is minimal (~5 IPs) suggesting infrastructure evolution | §3.3 |
| Winter & Lindskog (2012) — GFW blocking of Tor | Shadowsocks blocking is bidirectional (both inside-to-outside and outside-to-inside), unlike Tor which was unidirectional | §4.2 |
| Frolov et al. (2020) — Detecting probe-resistant proxies | This paper focuses on the attacker's (GFW's) perspective; provides real-world probe data rather than defender-side detection | §8 |
| Previous Shadowsocks vulnerability reports (2015-2017) | This paper discovers the complete passive+active detection pipeline, not just individual protocol vulnerabilities | §2.1 |

---

## 3. Research Connection

### 3.1 Related Concepts

- [[censorship-circumvention]] — The broader domain of circumventing internet censorship
- [[encrypted-traffic-analysis]] — Passive analysis of encrypted traffic features (length, entropy)
- [[tunnel-detection]] — Detecting encrypted tunnels/proxies
- [[traffic-classification]] — General traffic classification techniques

### 3.2 Related Methods

- Active probing — Sending crafted packets to elicit protocol-specific responses
- TCP fingerprinting — Using TCP header fields (timestamps, ports, TTL) to identify systems
- Entropy analysis — Measuring Shannon entropy to distinguish encrypted from non-encrypted traffic
- Replay attacks — Replaying previously observed legitimate traffic to trigger server responses

### 3.3 Related Tasks

- [[tunnel-detection]] — Primary task: detecting Shadowsocks encrypted proxy tunnels
- [[traffic-classification]] — Broader task of classifying encrypted traffic types

### 3.4 Built on These Papers

- Ensafi et al. (2015) — GFW active probing infrastructure and fingerprinting methodology
- Winter & Lindskog (2012) — GFW blocking mechanisms against Tor
- Frolov et al. (2020) — TCP-level fingerprinting of probe-resistant proxies

### 3.5 Relationship to Existing Claims

| Existing Claim | Relationship | Section |
|---|---|---|
| GFW uses active probing against circumvention tools (Ensafi 2015) | Extends — discovers new staged probing behavior and 7 probe types specific to Shadowsocks | §3.2, §4.2 |
| Stream cipher ciphertext malleability enables attacks (BreakWa11 2015) | Confirms — R2-R5 probes exploit byte-changed replays targeting this vulnerability | §5.3 |
| Replay filters can defend against active probing (Shadowsocks devs 2017) | Partially confirms — Bloom filter replay defense blocks R1 but R2-R5 still work via different attack vectors | §5.3 |

---

## 4. Key Findings and Evidence

### 4.1 Main Experimental Results

| Experiment | Metric | Result | Notes |
|---|---|---|---|
| Shadowsocks server experiment (4 months) | Total probes collected | 51,837 | From 12,300 unique source IPs |
| Single packet trigger | Minimum traffic to trigger probes | 1 client data packet | Confirmed via sink server experiment |
| Entropy effect | Replay rate at entropy 7.2 vs 3.0 | ~4x higher | High-entropy packets more likely replayed |
| Replay delay (first occurrence) | Within 1 second | >20% | Range: 0.28s to 570 hours |
| Replay delay (first occurrence) | Within 1 minute | >50% | Log-normal distribution |
| Replay delay (first occurrence) | Within 15 minutes | >75% | Long tail up to 570 hours |
| Brdgrd mitigation | Probing reduction | Near-zero within hours | Probing resumes when brdgrd disabled |
| Prober IP overlap with Ensafi 2015 | IP overlap | 5 IPs (out of 12,300) | High churn in prober infrastructure |
| TCP timestamp sequences | Physical systems detected | ~7 | All at 250 Hz or 1000 Hz clock rates |

### 4.2 Key Findings

1. **Packet length is a primary detection feature**: Replay probes exhibit a stair-step distribution with remainders mod 16 clustering at 9 and 2 bytes, reflecting Shadowsocks address header + AEAD tag structure. Lengths between 160-700 bytes are predominantly replayed.

2. **High entropy triggers more probes**: Packets with Shannon entropy of 7.2 are ~4x more likely to be replayed than those with entropy 3.0. The GFW exploits the fact that encrypted proxy traffic has higher entropy than typical web traffic.

3. **Active probing operates in stages**: R3/R4/R5 probes are only sent after the server responds to R1/R2 probes. This staged approach suggests the system is designed for multiple protocols, not just Shadowsocks.

4. **Blocking is rare and possibly human-controlled**: Of 63 vantage points running over months, only 3 were blocked. The three blocked servers ran ShadowsocksR or Shadowsocks-python (not Shadowsocks-libev). Blocking was by port or IP, unidirectional (server-to-client only).

5. **Prober infrastructure is centralized**: Despite 12,300 source IPs, TCP timestamp analysis reveals ~7 physical systems. Source ports follow Linux defaults (32768-60999). TTLs cluster at 46-50.

---

## 5. Quality and Confidence Assessment

### 5.1 Current Status

| Dimension | Status | Notes |
|---|---|---|
| Experimental completeness | Complete | 4-month measurement with multiple implementations and configurations |
| Writing completeness | Complete | Clear structure from detection mechanism through circumvention |
| Methodological rigor | High | Control experiments, multiple implementations, systematic probe analysis |
| Experimental persuasiveness | Strong | 51,837 probes, reproducible experiments, brdgrd validation |
| Differentiation from prior work | Clear | New probe types, staged behavior, infrastructure fingerprinting |

### 5.2 Areas for Improvement

1. Limited diversity in vantage points (mostly Beijing clients + US/UK servers), which may miss geolocation-dependent behavior
2. The relationship between active probing and actual blocking remains unclear — few probed servers were blocked
3. Blocking mechanism is speculated (human-controlled or implementation-specific) rather than confirmed

### 5.3 Relevance Assessment

> [x] Methodology complete
> [x] Sufficient experimental coverage
> [x] Writing meets readability standards
> [x] Clear differentiation from prior work
> [x] Limitations honestly discussed

---

## 6. Open Questions and Future Plans

### 6.1 Open Questions Left by This Paper

- What is the exact relationship between active probing and server blocking? Most probed servers were never blocked.
- Are the new probe types (NR1 with lengths 53, 56, 169, 180, 402 bytes) targeting other protocols like VMess?
- How does the GFW's detection system handle obfuscated Shadowsocks traffic or plugins like v2ray-plugin?
- What is the false positive rate of the passive traffic analysis stage?

### 6.2 Next Research Directions

- Testing whether the GFW actively probes other fully-encrypted protocols (VMess, VLESS, Trojan)
- Developing more robust traffic shaping that preserves usability (brdgrd has connection failure issues)
- Investigating the GFW's detection of application-fronting approaches (NaiveProxy, HTTPT)
- Longitudinal monitoring of the GFW's probing infrastructure evolution

### 6.3 Relationship to Research Line

> This paper is a foundational empirical study in [[censorship-circumvention]] and [[tunnel-detection]], providing ground-truth data on how a nation-state censorship system detects encrypted proxies. It informs both offensive (detection) and defensive (circumvention) research directions.

---

## 7. Pain Points Analysis

| Pain Point | Description | How This Paper Addresses It |
|---|---|---|
| Unknown GFW detection mechanism for Shadowsocks | Users reported blocking since 2017 but the actual detection method was unknown | Reveals the complete two-stage detection pipeline: passive analysis + staged active probing |
| Inadequate adversary model for replay attacks | Prior work assumed simple replay; the GFW uses delayed, byte-changed, and multi-stage replays | Discovers R2-R5 probe types that exploit ciphertext malleability, with delays up to 570 hours |
| IP-based prober blocking as a defense strategy | Blocking prober IPs was a common mitigation attempt | Shows 12,300+ IPs with high churn makes IP blocking ineffective; only ~7 physical systems behind them |
| Inconsistent implementation security | Different Shadowsocks implementations have different vulnerabilities | Identifies specific fingerprintable reactions per implementation and version, guiding developers to fix them |

---

## 8. Pipeline and Module Analysis

### 8.1 GFW's Detection Pipeline (as revealed)

```
Stage 1: Passive Traffic Analysis
  ┌─────────────────────────────────────┐
  │  Monitor client-to-server traffic   │
  │  Features: first-packet length +    │
  │  Shannon entropy                    │
  │  Threshold: high entropy + specific │
  │  length range → suspect             │
  └─────────────────────────────────────┘
                    ↓
Stage 2: Active Probing (Staged)
  ┌─────────────────────────────────────┐
  │  Phase 1: R1 (identical replay)     │
  │  + R2 (byte-0 changed)             │
  │  + NR2 (221-byte random)           │
  │  Check: does server respond?        │
  └─────────────────────────────────────┘
                    ↓ (if server responds)
  ┌─────────────────────────────────────┐
  │  Phase 2: R3 (bytes 0-7,62-63)     │
  │  + R4 (byte 16 changed)            │
  │  + R5 (bytes 6,16 changed)         │
  │  + NR1 (7-50 byte random probes)   │
  │  Statistical analysis of reactions  │
  └─────────────────────────────────────┘
                    ↓
Stage 3: Blocking Decision
  ┌─────────────────────────────────────┐
  │  Block by port or by IP address     │
  │  Unidirectional (server→client)     │
  │  Possibly human-controlled          │
  │  Unblocking: irregular timing       │
  └─────────────────────────────────────┘
```

### 8.2 Probe Types Summary

| Probe Type | Category | Description | Trigger Condition | Key Insight |
|---|---|---|---|---|
| R1 | Replay | Identical replay of first data packet | Always (after passive detection) | Tests if server responds to valid-looking traffic |
| R2 | Replay | Byte 0 changed (address type field) | Always | Targets stream cipher malleability; IV/salt at offset 0 |
| R3 | Replay | Bytes 0-7 and 62-63 changed | Only after R1/R2 response | Targets OutlineVPN-specific parsing |
| R4 | Replay | Byte 16 changed | Only after R1/R2 response | Chosen ciphertext attack on 16-byte IV stream ciphers |
| R5 | Replay | Bytes 6 and 16 changed | Only after R1/R2 response | Rare (only 2 observed); targets multiple cipher features |
| NR1 | Random | Lengths 7-50 bytes in trios | After R1/R2 response | Probe lengths coincide with IV/salt + tag size thresholds |
| NR2 | Random | Exactly 221 bytes | Always | ~3x more common than all NR1 combined; tests RST probability |

### 8.3 Innovation Module Details

**Module 1: Passive Traffic Analysis Features**
- Innovation: Identifies that the GFW uses first-packet length and Shannon entropy as detection features
- Evidence: Brdgrd (packet fragmentation) reduces probing to near-zero; high-entropy packets are 4x more likely to be replayed
- Significance: Simple but effective — encrypted proxy traffic has characteristic high entropy and unmodified packet lengths

**Module 2: Staged Active Probing**
- Innovation: Discovers that the GFW operates in stages, sending more sophisticated probes only after initial confirmation
- Evidence: R3/R4/R5 probes only appear after server responds to R1/R2; switching sink to responding mode triggers new probe types
- Significance: Resource-efficient design that may target multiple protocols, not just Shadowsocks

**Module 3: Prober Infrastructure Analysis via TCP Timestamps**
- Innovation: Uses TCP timestamp sequences as a side channel to reveal that 12,300 IPs are controlled by ~7 physical systems
- Evidence: Timestamp slopes of 250 Hz and 1000 Hz, wrap-around events, shared sequences across IPs
- Significance: Undermines IP-based blocking defenses; reveals centralized control structure

---

## 9. Evidence Record

| Claim | Evidence | Evidence Strength |
|---|---|---|
| GFW uses first-packet length for detection | Stair-step distribution of replay probe lengths with mod-16 remainders | Strong (statistical analysis of 51,837 probes) |
| GFW uses entropy for detection | 4x higher replay rate for entropy 7.2 vs 3.0 packets | Strong (controlled experiment) |
| Single packet triggers probing | Sink server (never responds) received probes after one client packet | Strong (control experiment) |
| Probing operates in stages | R3/R4/R5 only sent after R1/R2 response; confirmed by switching sink to responding mode | Strong (A/B experiment) |
| 12,300 IPs controlled by ~7 systems | TCP timestamp sequence analysis showing shared slopes | Strong (side-channel analysis) |
| Brdgrd reduces probing to near-zero | Probing drops within hours of enabling brdgrd, resumes when disabled | Strong (A/B with control server) |
| Blocking is rare and possibly human-controlled | Only 3 of 63 servers blocked over months; blocking during political events | Medium (observational) |
| Prober IP overlap with prior work is minimal | 5 IPs shared between 12,300 (this work) and Ensafi 2015 datasets | Strong (set intersection) |

---

## 10. Original Resources

- PDF: `00-inbox/PDFs/2020-IMC-How_China_Detects_and_Blocks_Shadowsocks.pdf`
- MinerU Markdown: `02-parsed-markdown/2020-IMC-How_China_Detects_and_Blocks_Shadowsocks.md`
- Code/Data: https://gfw.report/publications/imc20/en
- Supplementary: Probe data, prober simulator source code, and brdgrd experiment data available at project URL

---

## 11. Narrative Structure Analysis

### 11.1 Narrative Logic Chain

```
Background: Shadowsocks is popular in China for censorship circumvention
     ↓
Problem: Servers have been blocked since 2017, but detection mechanism unknown
     ↓
Discovery: GFW uses two-stage detection — passive analysis + active probing
     ↓
Characterization: 7 probe types, 12,300 IPs, staged behavior, centralized infrastructure
     ↓
Understanding: Probes target implementation-specific vulnerabilities via statistical analysis
     ↓
Mitigation: Brdgrd packet fragmentation defeats passive detection; AEAD ciphers + replay filters needed
```

### 11.2 Narrative Strategies

| Strategy | Specific Manifestation |
|---|---|
| Empirical grounding | 51,837 probes over 4 months; multiple implementations tested |
| Control experiments | Unused control host received zero probes; brdgrd A/B test with control server |
| Implementation comparison | Shadowsocks-libev vs OutlineVPN reveals staged probing behavior |
| Responsible disclosure | Findings shared with developers; led to concrete improvements |

---

## 12. Summary Table: What the GFW Targets

| Feature | How Used | Evidence |
|---|---|---|
| First-packet length | Classify suspected Shadowsocks connections | Stair-step replay distribution; brdgrd effectiveness |
| First-packet entropy | Classify suspected Shadowsocks connections | 4x replay rate difference between entropy levels |
| Server response to R1/R2 | Decide whether to send advanced probes | R3/R4/R5 only appear after R1/R2 response |
| Server reaction to random probes | Statistical analysis to confirm Shadowsocks | NR1 lengths coincide with implementation thresholds |
| Stream cipher malleability | R2-R5 exploit byte-changed replays | Different reactions per implementation version |
| AEAD authentication error | RST response confirms non-random data parsing | 51-byte threshold for AEAD salt+tag verification |

---

## 13. Learning and Application

### 13.1 Circumvention Recommendations from This Paper

1. **Use AEAD ciphers exclusively** — stream ciphers have fundamental malleability vulnerabilities
2. **Deploy replay filters** — but combine nonce-based with timestamp-based filtering (nonces alone are too costly)
3. **Ensure consistent server reactions** — read forever on errors rather than sending distinguishable FIN/RST
4. **Shape traffic to vary packet sizes** — brdgrd or similar tools disrupt the passive detection stage
5. **Monitor for active probes** — implement anomaly detection on probe patterns

### 13.2 Relevance to Traffic Classification Research

This paper provides ground-truth data on how a real-world censorship system performs traffic classification on encrypted proxy traffic. The two-stage approach (passive + active) mirrors the broader pattern in [[traffic-classification]] where passive analysis narrows candidates and active probing confirms. The entropy and packet-length features identified here are the same features used in many ML-based traffic classifiers, making this paper a bridge between censorship research and traffic classification research.

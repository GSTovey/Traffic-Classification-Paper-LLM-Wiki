# The Hidden Life of Public Safety Communications Signals: A Comparative Security Analysis of TETRA, TETRAPOL, and P25

Larry Hernandez Sergey Bratus

Dartmouth College

{l.gr, Sergey.L.Bratus}@dartmouth.edu

Abstract—Public-safety agencies and critical infrastructure operators rely on trunked land-mobile radio (LMR) systems, based on P25, TETRA, and TETRAPOL. These systems are expected to protect not just the content of a communication but the fact of it. Yet LMR standards leave a stark gap between confidentiality of content and of communication: underneath an encrypted traffic plane, their signaling plane is almost entirely in the clear. We probe the depth and impact of adversarial inference from this exposed signaling.

Prior security analyses of these systems have concentrated on the content plane—recovering encryption keys or capturing accidental cleartext. We show that comparably sensitive information can be inferred from passively observed signaling even if the content encryption were perfect.

In particular, we show that across the trunked LMR standards, a passive, receive-only software-defined radio (SDR) observer can recover operationally sensitive network topology and geography details, unit presence, mobility across cells and groups, organizational structure, as well as operational security details such as special key domains and key-epoch rotation. This signalingplane inference reaches far beyond the observer’s direct area of reception, turning local sniffing into nationwide network mapping capabilities that degrade or defeat LMR standards’ identity obfuscation through timing and association. In the case of TETRAPOL, we demonstrate how inference and tracking of such signaling metadata and a standards-level confidentiality failure in emergency call handling enable unencrypted voice extraction.

Finally, we discuss potential countermeasures and mitigations, including specific recommendations for protecting inter-cell, base station and subscriber identities.

## I. INTRODUCTION

Public safety communications systems are a mission-critical component of modern law enforcement and emergency response infrastructure worldwide. Their operators procure and rely on them on the expectation of confidential operational communications: voice encryption is a long-standing stated user need [1], [2], and national emergency and defense networks are fielded and promoted as secure [3]–[5]. Although these systems use different protocols in Europe (TETRAPOL, originally designed in France in the 1980s, and being gradually succeeded by TETRA) and the US (Project 25, a.k.a. P25), they share essential design similarities in modulation, error correction, naming conventions of frames or PDUs, cryptographic schemes and algorithms, and so on. As these standards and their deployments are long-lived, often under decades-long servicing and maintenance contracts, weaknesses in their designs create long-lived attack surfaces that must be understood and mitigated.

![](images/eddfdb1eb31d256f52ab9c078cc9fa1447032b21e3f6bfedf9641e35d9339c6a.jpg)  
Fig. 1: Self-guiding topology and affiliation inference. One D\_NEIGHBOURING\_CELL broadcast from serving cell BS 63 reveals each neighbor’s identity and control-channel frequency. A passive observer can retune recursively to map the deployment. Talk group (TG) associations and cell transitions expose operational affiliation and mobility (section VI-B).

Seminal work by Glass et al., Clark et al., and Meijer et al. [6]–[9] addressed aspects of P25 and TETRA, noting their ad hoc designs that, e.g., eschewed cryptographic message authentication and metadata encryption for the sake of availability in environments with interference or degraded RF conditions. Even so, the full scope of the cleartext signaling plane weaknesses of these protocols—and especially of their hardware and software implementations—remains underexplored. In particular, the architectures of these standards invariably involve a split between a signaling plane (control channel) that carries metadata such as registration, affiliation, and channel occupation (grants), and a traffic plane that carries the voice/data content. While the traffic plane may be encrypted, the signaling plane remains exposed. We show that, through this unprotected, readily accessible signaling plane, a passive, receive-only observer can infer a great deal of sensitive information from the network, including its topology, operational security properties (e.g., key rotation), churn and presence patterns, and even the organizational structure of the subscriber agencies (section V). We show that protocolspecific design choices allow a passive interception agent to recursively bootstrap its understanding of a network from a single cell’s intercepted control carrier (Figure 1).

Moreover, support for vendor-defined applications, in combination with the complexity of the underlying protocols, leads to practical weaknesses of the presumably protected cryptographic layers, due to the relevant information spilling to the cleartext signaling plane.

## II. OUR CONTRIBUTIONS

In this paper we focus on the common weaknesses of the cleartext signaling planes of LMR protocols. Our contributions are as follows.

1) A cross-protocol signaling-inference methodology. We develop a metadata-first methodology that maps protocol-specific signaling from TETRA, TETRAPOL, and P25 into a common vocabulary of identity, topology, activity, mobility, affiliation, and cryptographicstate events (sections IV and V).

2) WITCHHUNT (WH): an LMR whole-cell observatory. We build WH, a real-time Rust framework for wideband carrier discovery, channelization, PHY/link decoding, transaction-state reconstruction, and normalized event extraction across multiple LMR protocols. (section IV-A).

3) The first empirical TETRAPOL and TETRA cell security study, and a comparative deployment survey. We passively surveyed operational TETRAPOL and TETRA networks, reconstructing neighbor graphs, frequency plans, subscriber and talk group (TG) populations, traffic patterns, and cryptographic key-index epochs (sections VI, IX and X).

a) A standards-level confidentiality failure in TETRAPOL emergency handling. The standard mandates the Emergency Open Channel (ECH) to be unencrypted (PAS 0001-3-2 §4.4.33). Using a reverse-engineered RP-CELP vocoder, we recover a distress-button call’s clear speech end to end, with no traffic-encryption key.

4) A platform for low-cost embedded experimentation. We develop a TETRAPOL-capable embedded platform based on MMDVM\_HS—an open, low-cost ADF7021- based hotspot board—and use it to demonstrate decoding, topology discovery and applicability for near-field tracking through successful reception of downlink and uplink traffic.

## III. BACKGROUND: TRUNKED PUBLIC-SAFETY DIGITAL RADIO

Trunked LMR systems pool RF channels among many users. A shared control channel handles registration, TG affiliation, paging, and channel grants. Assigned traffic channels then carry voice or data. This control/traffic split improves spectrum use but creates the security seam studied here:

payload encryption may conceal content while the signaling needed to route it remains observable. We discuss the origins and today’s usage of these systems below.

## A. TETRA

TETRA originated in an ETSI standardization effort begun in 1989 to provide interoperable digital trunked radio for professional and public-safety users. ETSI published the first standard in 1995, and TETRA subsequently developed into a widely deployed voice-and-data system [11], [12]. Its air interface uses four-slot time-division multiple access (TDMA) and supports both infrastructure-based trunking and direct terminal-to-terminal operation. TETRA also provides authentication, key management, and TEA-family air-interface encryption. We discuss the relevant signaling exposure and TEA1 weakness in sections VII-A and VII-D.

## B. TETRAPOL

1) History of TETRAPOL: Developed by Matra in France in the 1980s, TETRAPOL is a proprietary frequency-division multiple access (FDMA)-based digital radio protocol using Gaussian minimum-shift keying (GMSK) modulation. Its national-scale implementations have primarily been used for national security and primary law-enforcement purposes, including deployments in France, Spain, the Czech Republic, Slovakia, Switzerland, and Germany [13], [14].

Large deployments also exist outside Europe. Mexico’s implementation spans all 32 states and roughly 100,000 publicsafety terminals [15], [16]. Brazil deployed approximately 280 sites and tactical repeaters, including support for security operations during the 2014 FIFA World Cup [17], [18]. Together with smaller implementations elsewhere, the vendor-reported footprint is roughly 80 networks across 34 countries [14].

2) Technical properties: The normative reference for TETRAPOL is the set of Publicly Available Specification (PAS) documents [19], primarily PAS 0001-1 (General Network Design), PAS 0001-3-1 (Air Interface Protocol; Air Interface Application Protocol) and PAS 0001-3-3 (“Air Interface Protocol; Air Interface Transport Protocol”).

The base station (Endpoint SwMI) and subscribers (radios, RT applications) communicate in a Base Network (BN). TS-DUs are, in essence, the packets (or PDUs) passing over the air (PAS 0001-3-2 §5.3, 93 Information Elements [20]).

3) Relationship to TETRA: Despite the similarity in their names, TETRA and TETRAPOL even if often confused, have little in common besides some of their design paradigms and nomenclature. The design patterns do transfer between the standards, and so do their structural weaknesses, as we demonstrate below.

## C. P25

APCO Project 25 (a.k.a. P25) is the TIA-102 suite for interoperable public-safety land-mobile radio [21]. Phase 1 uses continuous 4-level FM (C4FM) FDMA, while Phase 2 uses two-slot TDMA. Both retain a trunked control plane that exposes network and channel identifiers, TGs, unit addresses, grants, and affiliations. Optional traffic encryption includes AES and legacy DES-OFB, alongside the vendor-specific 40- bit ADP/RC4 mode [7], and deployments can mix protected and clear calls [8]. We analyze the resulting metadata and fallback risks in sections VIII-A and VIII-B.

TABLE I: Comparative matrix of public-safety digital radio standards

<table><tr><td>Exposure axis</td><td>TETRA</td><td>TETRAPOL</td><td>P25</td></tr><tr><td>Control channel encrypted? $^{3}$ </td><td>no</td><td>no</td><td>no</td></tr><tr><td>Identity/SSI enumeration</td><td> $partial^1$ </td><td> $yes^1$ </td><td>yes</td></tr><tr><td>Neighbor/topology broadcast</td><td> $full^2$ </td><td> $full^2$ </td><td>yes</td></tr><tr><td>Subscriber/TG census (passive)</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>Cryptographic state/protocol visible?</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td>Idle-device beaconing leak</td><td>yes [10]</td><td>yes</td><td>limited</td></tr><tr><td>Content-crypto weakness</td><td>TEA1 [9]</td><td> $undisclosed^4$ </td><td>DES/ADP [7], [8]</td></tr><tr><td>Weak-keystream content recovery</td><td>underexplored [9]</td><td> $undisclosed^4$ </td><td>yes</td></tr></table>

<sup>1</sup> TETRA (SSI) and TETRAPOL (RTI/TTI) conceal identities with ephemeral IDs, but these persist within registration windows, so enumeration remains feasible.  
<sup>2</sup> Full neighbor graph: TETRAPOL via the D\_NEIGHBOURING\_CELL codop, TETRA via D-NWRK-BROADCAST.  
<sup>3</sup> No holds for the broadcast/AACH blocks and the MAC header, which are never encrypted. TETRA C-plane signaling TM-SDUs may be optionally encrypted under security class 2/3 (EN 300 392-2 §21.4.3.1).

![](images/a0263b12af8f4f241b34d88173e6261ccd8c1d684c6e348c443018c338f05775.jpg)  
Fig. 2: Shared on-air frame anatomy of TETRA, TETRAPOL, and P25. The compared units combine synchronization (blue), addressing (orange), payload (green), and error protection (gray). The displayed TETRAPOL and P25 field sizes are decoder-verified, while the TETRA row shows the decoded SYNC/BNCH burst (section VII-A). TETRAPOL’s 152-bit block is expanded through its passive decoding chain.

DMR and related commercial LMR systems exhibit two relevant design overlaps, namely exposed control signaling and optional per-call privacy. We mention them only as corroborating context and do not analyze them separately, due to space constraints.

## IV. METHODOLOGY: A PASSIVE SIGNALING-METADATA OBSERVATORY

## A. Capture and Demodulation Pipeline

WH ingests wideband IQ—from a file or a SoapySDR front end—and channelizes it once through a shared polyphase filterbank into per-carrier baseband streams, so an entire cell is observed in parallel rather than one channel at a time. Each control carrier is decoded by an independent worker: GMSK demodulation and symbol-timing recovery, then the TETRAPOL physical layer—frame synchronization, differeninterleaving—yielding the BCH/PCH/RCH/SDCH logical channels. These feed HDLC framing and per-connection link state, TSDU reassembly, and finally CODOP and informationelement (IE) dissection; a single serialized stage folds the results into cell, neighbor, grant, and statistics state and emits records.

A parallel traffic monitor receives a byte-identical copy of the same IQ. Grants recovered on the control plane cue it—and a separate retain ring—to retroactively extract voice and DATA windows, including emergency-channel (ECH) traffic, from IQ buffered before the grant was observed, so WH captures a call it was never tuned to in advance. Percarrier decode runs on disjoint state in parallel, while grants, topology, and retention are updated by serial, ordered owners, keeping the whole-cell view consistent under load. The same channelize → decode → state architecture is instantiated per protocol (for P25 via dsd-neo [22], section X). Figure 3 summarizes the chain.

![](images/30ea5a7740d431a7dd7fa228abf179c8582ba6b74bd5b1ea1b27758f53f12813.jpg)  
Fig. 3: WH capture-and-decode pipeline. Wideband IQ is channelized once and every control carrier is decoded in parallel through the TETRAPOL PHY, logical channels, HDLC/link, and TSDU/CODOP/IE stages into serialized cell and grant state. A byte-identical copy feeds a traffic/ECH monitor whose retain ring, cued by recovered grants (dashed), retroactively extracts voice, DATA, and emergency-channel windows. The double border marks persistent state.

## B. Time-Domain Inference Primitives

We build our protocol-agnostic analysis pipeline on the following primitives that capture the trunked radio’s signaling planes’ observable properties, events, and their temporal relationships.

1) Presence Detection: The ability to detect the presence of a signal or device in the environment based on its unique characteristics (e.g., metadata, such as subscriber and group IDs, or timing patterns).

2) Activity/Burst Clustering: The ability to group similar signals or events based on their temporal characteristics and time-domain patterns.

3) Cross-Signal Correlation: The ability to identify relationships between different signals or devices based on their properties (e.g., temporal and spectral) and their similarities.

4) Temporal and Co-occurrence Profiling: The ability to analyze and model the temporal behavior of signals or devices through a defined observation window.

## C. Protocol-Specific Augmentation

We compose the generic primitives described in section IV-B to capture protocol-specific, semantically distinctive higher-level events, such as cryptographic key rotation and over-the-air provisioning, subscriber or device registration, TG affiliations, and emergency call response patterns.

These semantic events, in turn, are inputs rather than conclusions: the framework in section V composes them across observation windows and cells into security-relevant deductions. The protocol analyses in sections VI to VIII identify the concrete signaling fields, and section IX compares their exposure across standards.

Protocol semantics also expose payload regularities, such as invariant lengths, deterministic retransmissions, or predictable tunneled headers. Those are content-analysis inputs rather than members of the signaling-inference classes defined below.

## D. Decode Robustness as an Attack Enabler

Robust reception expands the passive attack surface. Short uplink bursts, including 30 ms TETRAPOL segments, interleaving, reassembly, and mixed voice and data frames complicate interception, but the FEC and synchronization designed for weak subscriber links also benefit a passive observer with similar capture geometry. The protocols further expose coupled grant, channel, slot, call, and cryptographic states. Tracking these states lets a resource-constrained observer follow active carriers and prioritize traffic marked as clear, avoiding unnecessary processing of encrypted streams.

## V. CROSS-PROTOCOL INFERENCE FRAMEWORK

Building on the primitives and normalized events of sections IV-B and IV-C, our framework joins observations across time and cells. Although a single message may disclose only one identifier or state, composing observations progressively exposes five classes of information. We define those inference classes here, leaving protocol encodings to sections VI to VIII and their comparison to section IX.

## A. Identity and Enumeration

Network, site, subscriber, and TG identifiers support direct enumeration. Registration and authentication exchanges also bind stable identities to temporary ones. Rotation therefore limits direct naming but does not necessarily prevent linkage through persistent timing, cell, and group associations. The protocol mechanisms are analyzed in sections VI-C, VII-C and VIII-A. Their cross-protocol registration and affiliation vectors are compared in table V. We demonstrate the use of our inference pipeline in section X.

## B. Topology and Geography

Serving- and neighbor-site broadcasts expose identifiers, channel plans, and adjacent control frequencies. An observer can recursively retune to advertised sites, turning one received control carrier into a self-guiding topology survey. Reception from multiple locations further constrains coverage and geography. We demonstrate this directly for TETRAPOL in section VI-B. table VI enumerates the corresponding messages in each standard.

## C. Presence, Activity, and Mobility over Time

Timestamped registration, affiliation, grant, and handover events establish presence at a site. Repeated observation yields activity cadence and operational tempo. Joining these events with the topology graph reveals movement between cells. Table V lists the relevant transactions, while section X-C evaluates tracking across standards.

## D. Organizational-Structure Inference

Joining subscriber and TG identities with call endpoints, priorities, paging, and emergency indicators produces a relationship graph of units and groups without voice recovery. Inferring a group’s real-world function requires external labels, protocol-specific label leakage or contextual observation. The signaling nevertheless exposes membership and interaction structure. Table VII compares the carrying messages, and section X-B provides an empirical example.

## E. Operational Security and Confidentiality

Cleartext signaling of security class, cipher and key identifiers, or per-call encryption state reveals where and when confidentiality is enabled. Longitudinal observation distinguishes clear traffic, key-rotation epochs, and exceptional key domains without recovering a key or payload. The concrete TETRAPOL and P25 cases appear in sections VI-E and VIII-C. Table IV provides the cross-protocol mapping.

## VI. TETRAPOL SECURITY ANALYSIS

We surfaced several areas of interest and concerns, through development of our WH framework, analysis of both the public specifications (PAS) and the ways the deployments diverge from it, e.g., through undocumented or reserved codops, and observation of two different deployments in non-contiguous European countries.

## A. Control-Channel Signaling in the Clea

Every TETRAPOL control channel broadcasts, in the clear, the static identity of the network and the serving cell. From the signaling of a single measurement site we recover the operator and network identifiers—a TETRAPOL network, country X, system\_id 61, network 5, at PAS specification version 6—together with the serving-cell identity, base station BS 63 / RWS 1 (BN 88, cell\_bn 913). The same broadcasts expose the cell’s complete radio plan: a control channel at 393.0xx MHz, a dedicated data channel (DDCH) at 393.3xx MHz (channel 2797), at least seven traffic channels spanning 392.8xx–394.6xx MHz, and the underlying channel raster (12.5 kHz spacing on a 358.3xx MHz base). None of this requires decrypting a single call: it is read in clear text from the control plane, and it suffices to fingerprint the network and to tune a receiver to every carrier the cell uses.

![](images/2b93b240b7f679d418c03fbc67ff24be2b376e1c294041439cffb2c8fd7d9fcb.jpg)  
Fig. 4: One cleartext PDU, two inference paths. A D\_NEIGHBOURING\_CELL broadcast exposes the neighbor graph and each adjacent cell’s control-channel frequency, enabling recursive discovery. Combined with received signal strength, the same data supports coarse coverage inference. The topology panel also shows TG affiliation across cells. Cell identifiers are consistently pseudonymized across figures.

B. Neighbor-Cell Broadcast: Whole-Network Topology Bootstrap

TETRAPOL defines the D\_NEIGHBOURING\_CELL codop, as the cell’s broadcast list of adjacent cells (for mobile handover/cell-reselection). We decoded 10 neighbors—each with a cell ID (BS/RSW) and the channel ID of that neighbor’s control channel.

From a single carrier we bootstrap the structure of the whole deployed regional TETRAPOL network: which cells exist, their IDs (e.g., BS 71/58/82/17/94/36/25/68/79/13), and how they’re connected.

One PDU exposes the cell graph. This immediately enables:

1) Frequency discovery → self-guiding survey. The neighbor channel ids (2872, 2750, 2805, 2763. . . ) are the RF control-channel frequencies of the neighbors. Instead of blind band-scanning, we decode one cell and it hands us the frequencies of all its neighbors—we walk the entire network cell-by-cell. This is the single most operationally valuable PDU for mapping an unknown deployment.

2) Geolocation/coverage inference. Neighbor adjacency + measured signal strengths let us infer cell geography and coverage overlap—RF-planning-grade intelligence with no transmitter access.

3) Mobility tracking. Combined with subscriber registrations, the neighbor graph lets us reason about which cells a unit can move between.

We thus observe high-value metadata that leaks structural network intelligence with zero decryption, at a minimal cost of decoding a single PDU.

Further composition and confirmation comes from secondary and tertiary functional codops, like D\_GROUP\_ ACTIVATION (e.g., a call exists in group 390 on channel 2878), explicitly tying signaling to topology.

## C. Subscriber, TG, and Registration Enumeration

PAS defines registration as two sequential phases. An RT first draws a random terminal identity (RTI). The SwMI replies to that address with the codop-less D\_TTI\_ASSIGNMENT, then opens a level-2 connection using the assigned TTI. The ensuing U\_REGISTRATION\_REQ carries the permanent HOST\_ADR and SERIAL\_NB. D\_REGISTRATION\_ACK confirms the TTI and repeats HOST\_ADR. Downlink observation can therefore bind RTI↔TTI↔HOST\_ADR, while serial-number linkage requires the uplink [20], [23].

Clear group signaling supports a separate census. D\_GROUP\_ACTIVATION and D\_GROUP\_PAGING expose group identity and activity, but do not by themselves identify membership. D\_REGISTRATION\_ACK may also carry GROUP\_ID, while the uplink U\_ATTACH reports the selected group when a terminal powers on or changes selection. Those transactions directly bind a terminal to a group when captured. Traffic reflected from the downlink towards subscriber terminals also contributes to the inference capability, in responses containing non-broadcast addressing. Therefore, a missed uplink codop may still result in reflected activity observable in the downlink in close temporal correlation.

## D. Connection-Oriented Data Sessions and SDS

PAS reserves connection-oriented transport on the SDCH for application exchanges, with a new transport connection for each transaction. D\_DATA\_REQUEST announces a downlink data transfer, D\_CONNECT\_CCH or D\_CONNECT\_DCH selects its bearer, and D\_DCH\_OPEN opens the data channel. Addressed link framing and clear setup fields disclose the endpoint, priority, transport mode, key references, selected bearer, timing, and traffic volume even when the application body remains opaque [20], [23], [24].

PAS 0001-13-2 defines a structured Submit/Delivery Protocol header containing, among other fields, CHIFF, priority, application type, message type, encoding, and participant addresses. This reveals who exchanged data, when, how much, and which application family was used [25].

## E. Observable Operational Security Patterns: Key Use and Rotation

PAS 0001-3-2 [20], §5.3.41, defines the KEY\_REFERENCE octet as a KEY\_TYPE (high nibble) and KEY\_INDEX (low nibble) pair, which describe the cryptographic type and slot used for the encryption of the voice/data traffic. The same octet rides the channel-activation and call-setup codops— D\_GROUP\_ACTIVATION (§4.4.44), D\_ECH\_ACTIVATION (§4.4.33), D\_OC\_ACTIVATION (§4.4.60), D\_CALL\_START (§4.4.14), and D\_CALL\_CONNECT (§4.4.12)—so the key in force is announced on the control channel at every call setup.

These fields are readily observable in the clear, allowing precise tracking of the key rotation schedule. In two separate TETRAPOL cells in active deployment, we were able to reliably discriminate between key epochs, based on the shift of the key index at specific times of day.

![](images/b2ec0e998a1d806f42a9d325f62518658ce01712fe4d80d02a5ca29a52df40c8.jpg)  
Fig. 6: Daily network-synchronous key-day roll of an operational TETRAPOL cell over four days.

In one observed deployment (fig. 6), the index advances sequentially $( 0 \mathbf { x } 4 \mathsf { c } \to 4 \mathsf { d } \to 4 \mathsf { e } \to 4 \mathbf { f }$ , then wraps to 0x41). Crimson diamonds mark each roll’s first-detect estimate with its ±10% bounding band and local time—the rolls cluster at ≈13:00 UTC (≈15:00 CEST) daily. The grey span is the bounded 0x4c → 4d window that closed before the capture began.

More interesting is the fact that emergency calls (e.g., driven by the D\_ECH\_ codops) were persistently non-encrypted in one deployment (section X).

## VII. TETRA SECURITY ANALYSIS

## A. Signaling-Plane Metadata Leakage

Similarly to TETRAPOL (section VI-A), TETRA performs the core control and signaling plane operations in the clear. Two distinct PDU types (SYSINFO, D-NWRK-BROADCAST) convey network topology information.

A single SYNC+SYSINFO capture is sufficient to reliably determine the cell identity, encryption status, spectrum topology (frequencies of operation) and other details, from a single demodulated and decoded carrier.

A subsequent D-NWRK-BROADCAST reveals the neighboring cells and their downlink carrier frequencies and respective IDs.

Table II shows the extracted frequency plan for a surveyed TETRA cell, from a single cell. Each row hands a passive observer an adjacent cell’s downlink carrier and Location Area, bootstrapping the network graph from a single carrier.

## B. Intra-cell or External Traffic Reflection

In deployments that utilize IP gateways or tunneling— e.g., TETRAPOL-TETRA interconnects—an additional attack surface exists: any reflected traffic specific to one cell or system transmitted through another—e.g., a cell deployed in a different location—may expose the source cell’s location and affiliation to inference.

![](images/8424cd62512c82559815766e81601d81728733d4634b2dcce66798dddc220406.jpg)  
Fig. 5: TETRAPOL registration links ephemeral and permanent identities. D\_TTI\_ASSIGNMENT binds the terminaldrawn RTI to an ephemeral TTI. The ensuing U\_REGISTRATION\_REQ carries HOST\_ADR and SERIAL\_NB, while D\_REGISTRATION\_ACK repeats HOST\_ADR. Downlink observation links RTI, TTI, and HOST\_ADR. Linking the serial number requires uplink capture. The analogous TETRA binding appears in fig. 7.

TABLE II: Neighbor cells advertised in D-NWRK-BROADCAST on the surveyed TETRA cell (10 of 25 observed). Downlink carriers and carrier numbers are masked to band level. Location Areas are consistent anonymized identifiers.

<table><tr><td>Cell id</td><td>DL carrier (Hz)</td><td>Carrier no.</td><td>LA</td></tr><tr><td>1</td><td>421 1xx xxx</td><td>84x</td><td>6417</td></tr><tr><td>3</td><td>420 9xx xxx</td><td>83x</td><td>6283</td></tr><tr><td>8</td><td>421 6xx xxx</td><td>86x</td><td>6591</td></tr><tr><td>13</td><td>421 6xx xxx</td><td>86x</td><td>6034</td></tr><tr><td>16</td><td>421 2xx xxx</td><td>85x</td><td>6748</td></tr><tr><td>20</td><td>421 3xx xxx</td><td>85x</td><td>6159</td></tr><tr><td>22</td><td>421 0xx xxx</td><td>84x</td><td>6820</td></tr><tr><td>23</td><td>424 5xx xxx</td><td>98x</td><td>6375</td></tr><tr><td>24</td><td>420 9xx xxx</td><td>83x</td><td>6902</td></tr><tr><td>26</td><td>423 0xx xxx</td><td>92x</td><td>6516</td></tr></table>

C. Identity Correlation: Ephemeral Aliases, Event Labels, and the TEI

A TETRA subscriber is normally addressed over the air by a short alias—an ASSI / (V)ASSI, whose pairing with the permanent ISSI / ITSI the standard states “cannot be derived from knowledge of the ITSI” and is “only known to the network operator” [11] (EN 300 392-1 §7.2). Yet the binding of fig. 5 is not TETRAPOL-specific: a passive observer recovers the TETRA pairing directly from the registration exchange (fig. 7). In the migrating case (EN 300 392-2 §16.4.1.1) the uplink U-LOCATION UPDATE DEMAND is layer-2 addressed by the USSI, which the standard requires the MS to form by copying its home ISSI verbatim (§7.2.3, §7.7.5). The downlink D-LOCATION UPDATE PROCEEDING then returns the freshly assigned (V)ASSI and MNI as mandatory fields (Table 16.14). One round trip therefore binds the permanent ISSI to the temporary (V)ASSI by PDU parsing alone—, and, because the USSI is explicitly exempt from the Encrypted Short Identity (ESI) mechanism (EN 300 392-7 §4.2.6), even on an encrypted class-2/3 cell.

Two further bindings complete the chain. If the base station sets the TEI-request flag, the MS answers U-TEI PROVIDE carrying its 60-bit TEI—the equipment serial—alongside its SSI in a single PDU (EN 300 392-7 Table A.28). The standard names this the “ITSI / TEI mapping at registration” (§5.4.1) and notes the TEI carries no cryptographic seal. And every call grant that assigns a 10-bit event label carries it together with the SSI in one MAC-RESOURCE address element (EN 300 392-2 Table 21.55, address type 101<sub>2</sub>). The event label is likewise never encrypted (§4.2.6), so once the observer resolves the SSI, subsequent event-label-only bursts remain linkable.

The comparison to TETRAPOL is instructive. TETRA’s steady-state pseudonymity is in fact stronger: outside registration, ESI aliases the SSI per location area under a rotatable common cipher key, a defence TETRAPOL has no equivalent for. But the exposure concentrates precisely where the protection is weakest—at registration and migration, where the USSI carries the raw ISSI, and in the ESI carve-outs (USSI, event label). On a security-class-1 cell, where no airinterface encryption applies (EN 300 392-7 §6.5.1), every one of these bindings travels in the clear, leaving TETRA no better protected than TETRAPOL. The standard itself acknowledges the risk—it recommends (but does not require) that an MS “not reveal its true identity by sending ISSI in layer 3” when an alias is available (EN 300 392-2 §16.4.1.1, NOTE 3), and that the TEI not be sent on class-1 cells—so real-world exposure is deployment-dependent.

![](images/30ce19ad9a4b32def54df1794aa0795a5a42aed5c96ed31883c2fa7f529f4b4c.jpg)  
Fig. 7: TETRA registration links permanent, ephemeral, hardware, and event identities. A migration exchange binds the home ISSI, exposed as the USSI, to the ephemeral (V)ASSI. U-TEI PROVIDE adds the hardware TEI, and MAC-RESOURCE links the SSI to a 10-bit event label. The USSI and event-label leaks persist in every security class. The TEI and general addresses are clear in class 1 and pseudonymized in classes 2 and 3 [11].

## D. Cryptographic Weaknesses: TEA1 and the Air-Interface Keystream

TEA1 reduces its nominal 80-bit key to an effective 32 bits, making practical key recovery possible. Related air-interface attacks can also recover keystream and defeat protected identity signaling [9]. These weaknesses turn the metadata-derived targets of section VII-A into potential content and identity recovery, crossing the boundary that payload encryption is expected to enforce. This result is specific to vulnerable cipher and protocol configurations and should not be generalized to every TETRA encryption algorithm.

## E. Location Privacy and Availability

In Analyzing TETRA Location Privacy and Network Availability, Pfeiffer et al. [10] involved radio direction finding (RDF), but said effort still relied on a signaling control plane design choice: the standard requires coordination (“TETRA requires this regular signaling since MSes need to register at BSes, authenticate, and exchange management data” [10]) between a MS and its BS in configurable intervals, even when the MS is idle, typically configured to be a short interval under 2 minutes.

This manifests in the PHY layer as observable modulated signals enabling the aforementioned RDF. However, this can be utilized for mere detection of near-field presence, through decoding of the exact frames—and their sequencing in close temporal co-occurrence—employed for this purpose. An observer both in the physical domain and the RF domain can leverage such near-field fine granularity decoding to correlate, for example, a patrol vehicle or officer to a specific on-air identity, even if temporary, and then extend the inference to groups where the terminal appears active.

## VIII. P25 SECURITY ANALYSIS

## A. Unencrypted Control Channel and Identity Leakage

P25 design exposes many operationally rich and important fields to adversarial inference. This leakage is architectural: P25 voice encryption protects the voice payload but explicitly does not protect radio identities on traffic channels or callrequest, assignment, registration, and affiliation information on a trunked control channel. Data encryption has the same limitation for identities and data-channel grants [26]. Protecting those fields requires the separate Air Interface Encryption (link-layer encryption) service, which the security architecture defines as an optional overlay [27]. As of PTIG’s July 2025 standards update, that service was still being drafted and the supporting FDMA common-air-interface revision had only just been approved as a new project [28].

A standard group-voice grant carries its channel, group address, source address, emergency flag, protection flag, and priority. The protection flag applies to resources other than the control channel, whose default service option is “not protected” [29]. Registration and affiliation messages similarly bind unit and group identities, while every Phase 1 data unit exposes a 12-bit Network Access Code in its Network Identifier [30]. A passive observer can therefore recover who used which group, when, with what priority and security state, and on which assigned channel even when the ensuing voice is encrypted—the traffic-analysis risk identified by both TIA and Clark et al. [8], [27].

## B. Weak / Optional Link Encryption and Clear Fallback

P25 security is an optional overlay rather than a uniform protocol property: systems may mix clear and protected users and calls, and implementations may offer strong AES alongside legacy DES and vendor-specific 40-bit RC4 modes [7], [8], [26]. The practical failure mode is therefore often operational rather than cryptanalytic. In the radios studied by Clark et al., a commercial receiver configured for encryption still accepted clear traffic, and the configuration-level remediation was not easy to find and deploy. A missing or desynchronized group key forced users back into the clear, and ambiguous controls made that state easy to unwittingly select and hard for peers to notice [8]. Because the clear caller could still hear encrypted peers, one radio could silently fail open while the rest of the group believed the exchange remained protected. Their field study observed exactly this outcome in sensitive federal-law-enforcement traffic. Strong payload cryptography cannot repair this availability-driven clear fallback or the metadata exposure of section VIII-A. TETRAPOL presents a distinct clear-traffic risk because its ECH service is normatively unencrypted (sections VI and X).

TABLE III: A selection of P25 Type 1 (classified) encryption algorithms, their in-the-clear ALGID codes [32], and approximate introduction years where publicly known.

<table><tr><td>ALGID</td><td>Type 1 algorithm</td><td>Introduced</td></tr><tr><td>0x00</td><td>ACCORDION 1.3</td><td>—</td></tr><tr><td>0x01/0x41</td><td>BATON (Auto Even/Odd)</td><td> $\geq 1995$  [31]</td></tr><tr><td>0x02</td><td>FIREFLY</td><td>c. 1987 [33]</td></tr><tr><td>0x03</td><td>MAYFLY</td><td>—</td></tr><tr><td>0x04</td><td>SAVILLE</td><td>late 1960s [34]</td></tr><tr><td>0x05</td><td>PADSTONE</td><td>—</td></tr></table>

## C. Affiliation Inference via Cipher Identification

P25 implementations may offer privacy modes ranging from proprietary 40-bit RC4 to DES-OFB and AES-OFB, as well as classified NSA Type 1 algorithms such as BATON [7], [8], [31]. The clear encryption-synchronization metadata identifies the selected algorithm and key slot through the Message Indicator, ALGID, and KID fields [30].

Table III lists a selection of these classified Type 1 ALGIDs, as enumerated by the open-source OP25 decoder [32]. Reading the ALGID from voice headers and encryption-sync words lets a passive observer distinguish Type 1 from commercial cryptography without recovering content. Combined with TG and deployment context, that narrows the likely security domain and affiliation, although the ALGID alone does not identify an operator.

## IX. CROSS-PROTOCOL SYNTHESIS

Across the standards, an unprotected or under-protected signaling plane enables passive longitudinal inference. In section V we described five classes of inference. Here we compare the protocol fields that instantiate these classes. Table I gives the overview, while the tables below map the concrete signaling messages. Protocol-specific cryptographic, implementation, and operator weaknesses determine whether an adversary can also recover content.

## A. Operational Security and Confidentiality

Applying techniques from section V-E, table IV shows a common invariant: each standard exposes enough cryptographic state to distinguish clear from protected traffic and to separate key domains. The longitudinal TETRAPOL instance is measured in section VI-E. The P25 cipher-ID case appears in section VIII-C. These inferences do not require key recovery or a breach of traffic-plane confidentiality.

## B. Topology, Geography, and Presence

Table VI compares the broadcasts that make network discovery self-guiding, and table V compares the transactions that expose registration, affiliation, and mobility. Their composition instantiates sections V-B and V-C: adjacent control frequencies extend the survey, while timestamped site and group events associate activity with the resulting graph. The TETRAPOL topology demonstration appears in section VI-B, and crossstandard tracking is evaluated in section X-C.

## C. Organizational-Structure Inference

Table VII maps the addressing, call-setup, paging, priority, and emergency fields that instantiate section V-D. Pairing source/destination identities with TG, priority, and emergency fields reconstructs the organizational chart, chain of command, and unit function without decoding voice. Across the standards, stable group addressing leaves membership, interaction, population, and activity cadence observable even when subscriber identifiers rotate. Once a group is associated with a real-world function, its presence alone can become operationally sensitive. The P25 case study appears in section X-B.

## X. EVALUATION

We evaluated the inference framework of section V against live, operational deployments of all three standards, passively and receive-only, with no key material. We had expected needing to stitch together our observations from many fragmentary exposures across long campaigns. Instead, a single decoded control carrier routinely bootstrapped an entire deployment, including its neighbor graph and frequency plan, its subscriber and TG populations, their diurnal rhythm, and the key-rotation epochs of its encrypted traffic. Where deployed, identity obfuscation merely degraded rather than defeated this inference.

The difficulty lay in reach and reception: our limits were capture geometry and the sampling constraints of remote receivers and the processing software (e.g., WH implements in software what is typically done by ASICs and dedicated processors for stateful and synchronous protocol operation), not the protocols’ defenses (when present at all). We used the following capture, sampling, and census methods to successfully overcome these constraints.

Radio enthusiasts commonly provide publicly available receivers connected to the Internet, as a community resource for radio exploration. We developed a framework (NOSYMESH) for leveraging these open receivers as a distributed system to validate our hypotheses about global deployments. For P25, we implemented modifications to dsd-neo [22], an opensource multi-protocol digital-voice decoder, for dumping P25 frames and their decoded fields, and improved the polyphase resampler to tolerate low sampling rates (e.g., a P25 Phase 1 channel occupies 12.5 kHz, requiring under 150 ksample/s), a constraint imposed by the constellation of receivers we used for observation (the default resampling required 1 Msample/s). As a side-effect, our modification significantly lowered the bandwidth requirements for parallel observation. We limited dwell time to ensure polite use of the open receivers, based on our understanding of the community practice.

TABLE IV: Confidentiality metadata carried in the clear.

<table><tr><td>Protocol</td><td>Carrying PDUs / codops</td><td>Fields exposed &amp; inference</td></tr><tr><td>TETRA</td><td>SYSINFO security-class broadcast, call-grant encryption mode, KSG/SCK signaling</td><td>security class (1/2/3), air-interface encryption on/off per call, cipher-key class, and clear ISSIs in class 1 [9]</td></tr><tr><td>TETRAPOL</td><td>codops carrying KEY_TYPE / KEY_INDEX, retransmitted encrypted-data codops</td><td>key type and key index in the clear, daily key-epoch rotation, and invariant ciphertext across same-epoch retransmissions (no randomized padding)</td></tr><tr><td>P25</td><td>LDU/voice-header and call-grant ALGID / KID / Message Indicator (MI)</td><td>algorithm (cipher) ID, key ID, and MI in the clear, per-call clear-versus-encrypted state, and misconfiguration or clear-call detection [8]</td></tr></table>

TABLE V: Registration, affiliation, and mobility transactions.

<table><tr><td>Protocol</td><td>Carrying PDUs / codops</td><td>Fields exposed &amp; inference</td></tr><tr><td>TETRA</td><td>U-LOCATION UPDATE DEMAND, D-LOCATION UPDATE ACCEPT, ITSI attach/detach, D-ATTACH/DETACH GROUP IDENTITY</td><td>attach/detach timestamps, Location-Area moves, group-affiliation churn, and idle-device beaconing that aids localization [10]</td></tr><tr><td>TETRAPOL</td><td>U_REGISTRATION_REQ, D_REGISTRATION_ACK/NAK, D_TTI_ASSIGNMENT, cell-reselection codops</td><td>per-subscriber registration timing, diurnal PDU volume, per-TG activity, cell transitions</td></tr><tr><td>P25</td><td>Unit Registration (U_REG_REQ/RSP), Group Affiliation (GRP_AFF_REQ/RSP), Location Registration (TSBK)</td><td>attach times, site roaming, affiliation changes over time [8]</td></tr></table>

TABLE VI: Signaling messages that expose network topology and geography.

<table><tr><td>Protocol</td><td>Carrying PDUs / codops</td><td>Fields exposed &amp; inference</td></tr><tr><td>TETRA</td><td>D-NWRK-BROADCAST (neighbor list), SYSINFO on BNCH (cell params), SYNC on BSCH</td><td>MCC/MNC, Location Area, serving/neighbor cell IDs and carrier frequencies, adjacency graph, and coverage mapping [9]</td></tr><tr><td>TETRAPOL</td><td>D_SYSTEM_INFO, D_NEIGHBOURING_CELL, D_DDCH_DESCRIPTION</td><td>country / system_id / network / product version, serving BS/RSW cell ID, control + DDCH frequencies, up to 12 neighbor cell IDs and their control-channel frequencies</td></tr><tr><td>P25</td><td>RFSS Status Broadcast, Network Status Broadcast, Adjacent Site Status Broadcast, Identifier Update (TSBK)</td><td>WACN, System / RFSS / Site ID, adjacent-site control-channel frequencies, band plan [8]</td></tr></table>

TABLE VII: Call-setup, paging, and priority signaling.

<table><tr><td>Protocol</td><td>Carrying PDUs / codops</td><td>Fields exposed &amp; inference</td></tr><tr><td>TETRA</td><td>U-SETUP, D-SETUP, D-TX GRANTED, D-CONNECT, D-ATTACH/DETACH GROUP IDENTITY, D/U-SDS-DATA</td><td>source/destination SSI, TG membership, call priority, pre-emptive/emergency priority, status messages, and who-calls-whom</td></tr><tr><td>TETRAPOL</td><td>D_GROUP_ACTIVATION, D_GROUP_PAGING, D_CALL_ALERT, D_CALL_CONNECT, D_CONNECT_DCH</td><td>TG membership, CALL_PRIORITY, EMERGENCY_TYPE, who-pages-whom, and chain-of-command inference</td></tr><tr><td>P25</td><td>Group Voice Channel Grant, Unit-to-Unit Voice Channel Grant, Group Affiliation, Status/Message Update (TSBK)</td><td>source/target unit ID, TG, call priority, emergency indicator [8]</td></tr></table>

We note that open receivers operated by hobbyists and ham radio operators could potentially be abused by a real adversary, a passive observer that is not even located in the physical vicinity of any of these systems. Attackers’ abuse of remote radios reportedly occurs in the wild: e.g., according to [35], APT28’s nearest neighbor operation repurposed compromised systems in adjacent buildings as unwitting Wi-Fi relays for the final physical hops to targets. By analogy, an adversary could leverage any SDR-based platform it can access or modify against PMR systems—a class of remote-receiver abuse we anticipate and term the nearest radio attack.

## A. Metrics

We provide per-standard metrics for our data corpus in evaluation. TETRA totals are GSMTAP packet records, TETRAPOL totals are decoder records, and P25 totals are decoded event rows after exact-line deduplication. TETRA and TETRAPOL covered one public-safety deployment each, while P25 involved ten deployments.

1) TETRA: The TETRA corpus comes from one continuous downlink receiver, from one public-safety deployment. It contains over 16 million packet records over 36.25 hours, of which 12, 283, 156 decode as TETRA PDUs, excluding malformed frames. The mean record rate is 128.41 packets/s. The corpus exposes 251 distinct clear nonreserved SSI operands, including 2,142 downlink location-update-family PDUs addressed to 230 SSI values.

2) TETRAPOL: Our TETRAPOL corpus comprises 46 operational files with over 33 million raw decoder records, from one deployment. They contain 12,154 TTI and 4,095 RTI address values, and 5,296,573 active-state emissions covering 88 coverage-scoped group values. It also contains 1,586 ECH activations, 250,558 system-information records, and 67,364 neighboring-cell records. 877 non-encrypted ECH activations occurred.

3) P25: The P25 survey contains 688,866 records from ten systems. After deduplication of scheduler records, 600,036 unique events remain.

Three systems contribute 99.0% of these events. A NIFOG interoperability deployment contributes 95.2% of all encrypted frames and 98.6% of clear-RID frames.

Counting identities within their system namespaces yields 181 RIDs and 84 TGs. The bare numerical RID union is 178 because three values collide across systems (subscriber IDs are often not unique across separate systems). Of 21,514 identitybearing frames, 6,445, or 30.0%, expose the RID in clear. The NTIRN deep dive comprises 121,302 unique events over a sampled 58.5-hour span, with 177 RIDs, 75 TGs, and 610 crypto-classifiable voice calls.

## B. Quantitative Analysis of P25 Users

![](images/b68414068a0f9d2888b571d937c0f37d4f1aac5282cacc1fc3decbd101150ccf.jpg)  
Fig. 8: P25 census across CONUS. Markers identify NIFOGassociated entries [36] and observed systems. Large observedsystem markers are scaled by decoded-frame count and colored for mixed (orange), clear-only (red), or encrypted-only (blue) traffic. State boundaries are also color coded with the same scheme. Locations are public database-sourced [37]. Mixed deployments are prevalent.

Across our Continental US (CONUS) P25 survey, mixed clear-and-encrypted deployments are the norm, and wherever subscriber and TG identities are transmitted they are carried in the clear—from public-safety and federal users to utility and SCADA operators.

The National Interoperability Field Operations Guide (NI-FOG) [36], published by the U.S. Cybersecurity and Infrastructure Security Agency (CISA), is a public reference of interoperability channels and frequency assignments for publicsafety and government radio users. Deployment specifics— systems, sites, and TG assignments—are further catalogued in public, enthusiast-maintained scanner databases, notably RadioReference [37].

Our census of 567 P25 systems across 48 states makes this concrete: only 19% of their roughly 138,000 talk groups are encrypted, just one state has at least half its talk groups encrypted (median 18%), and 27% of systems carry no encryption at all.

In our survey, we used these sources to look up observed TG identities that were transmitted in the clear. These talk groups included law enforcement and public safety users, as well as SCADA operators. Our CONUS coverage included the states of Texas, Ohio, Maryland, Virginia, and Washington, DC.

Our observations likely undercount existing traffic, due to the constraints such as limited dwell times, connection reliability issues, and proximity or capture geometry of the remote receivers. Although our census aimed for a representative sample of exposed users, legacy ciphers, non-obfuscated identities at scale, the actual exposure might be even larger than the collected data demonstrates.

For Phase 2 (TDMA) deployments, the only limiter was the ability to locate a reliable control channel carrier to obtain the parameters (e.g., WACN, SYSID, NACs) that, unlike Phase 1 (FDMA/C4FM), are not transmitted in the data or voice channels. Once these parameters are observed, the operator or organization can be identified, as well as the general class of operator (e.g., federal), with these identifiers being public in FCC and radio enthusiast databases.

1) Law enforcement and public safety users: In our observed census, one public safety deployment covering police and EMS users had its distinctive TG operational details publicly available (via RadioReference [37]). This included federal liaison, narcotics, special operations, counter-terrorism, and executive-protection divisions, each identified by its TG ID. The names were likely derived from the P25 alias or alpha tag transmitted in the clear.

A representative slice appears in table VIII: each such function is carried as a plaintext TG identity regardless of whether its voice payload is encrypted.

Several of these groups, including most hospital and healthrelated services, were not visibly using encryption.

## C. Subscriber Tracking Across Standards

Across standards, we found that with sufficient observer density (e.g., more than one receiver distributed across an area of interest), the failure to conceal subscriber and system identity is a usable vector for tracking mobility across geographical zones. Once a given TG’s purpose is established, it becomes possible at scale to detect when it is operating in different locations—especially sensitive for law enforcement users, who may depend on the element of surprise and concealment.

TABLE VIII: Representative TGs on one National Capital Region public-safety system [38].

<table><tr><td>Dec</td><td>Alias tag</td><td>Name</td></tr><tr><td>11139</td><td>MPD EPU</td><td>Executive Protection Unit</td></tr><tr><td>11302</td><td>MPD HS/CT</td><td>Homeland Security / Counter-Terrorism</td></tr><tr><td>11131</td><td>MPD MND1</td><td>Major Narcotics Division 1</td></tr><tr><td>11560</td><td>MPD NSID 1</td><td>Narcotics &amp; Special Inv. Div. 1</td></tr><tr><td>11041</td><td>MPD SOD1 Evt</td><td>Special Operations Division 1</td></tr><tr><td>11117</td><td>MPD OIA</td><td>Office of Internal Affairs</td></tr><tr><td>1039</td><td>RIZ-16 CW-1</td><td>MPD Citywide 1</td></tr><tr><td>145</td><td>0H4 MEDSTAR</td><td>MedStar hospital (clear)</td></tr><tr><td>154</td><td>0H13 WHC</td><td>Washington Hospital Center (clear)</td></tr><tr><td>728</td><td>011 EMS 1</td><td>EMS 1, East (clear)</td></tr></table>

![](images/9bae106148c364da73e221d36fc3ea094e1930661ca9d6e9988f919bf24aa2ef.jpg)  
Fig. 9: Spectrogram of a clear TETRAPOL emergency call (post-FEC and post-descrambling, and after RP-CELP decoding).

Under the perception that the system guarantees confidentiality [1], [2], [5], its users may inadvertently reveal both their affiliation and presence without any breach of protected or encrypted content.

## D. TETRAPOL Emergency Call Extraction

The moment of greatest operational sensitivity is precisely the moment at which the protocol removes content confidentiality: TETRAPOL specifies its Emergency Open Channel (ECH) service as an unencrypted call. PAS 0001- 3-2 [20] §4.4.33 requires the D\_ECH\_ACTIVATION message to carry KEY\_REFERENCE = UNENCRYPTED\_CALL together with its mandatory uplink and downlink dynamicchannel-scrambling parameters. The absence of traffic encryption is thus written into the normative message definition, not merely an operator configuration. (The clear-call mandate is not unique to ECH: §4.4.66 likewise applies to D\_PRIORITY\_GRP\_ACTIVATION.) We confirmed this end to end: across five ECH activations in an operational deployment, all five carried the clear-call key reference and yielded intelligible RP-CELP speech after ordinary channel descrambling and error correction—without possession or recovery of any cryptographic key—subject only to the publicly signaled dynamic-channel scrambling. Figure 9 shows the spectrogram of one such call.

We obtained these calls by tracking the control plane. D\_ECH\_ACTIVATION is the downlink message announcing an active emergency open channel. We implemented the explicit grant-based tracking of section IV-A in WH so that an observed activation—with its advertised scrambling parameter (here D\_CH\_SCRAMBLING=82) and UNENCRYPTED\_CALL key reference (sections B and VI-E)—cues retrospective extraction of the assigned traffic channel from IQ buffered before the grant was seen, at whole-cell scale and without tuning to it in advance.

The recovered dialogue supplies semantic ground truth for the physical trigger. In one representative call, dispatch informed the field operator that the terminal’s emergency button had been pressed, and the operator replied that it had been an accident—connecting a distress-button press to the ECH activation, the assigned traffic channel, and the recovered clear speech. Some of the five calls also showed a central dispatch checking on an operator’s well-being, and idiomatic cues identified the law-enforcement organization involved.

Because the observed grant mechanism depends on capture constraints (including processing time and actual RF reception), we can only quantify exposure through the observed ECH activation records.

## E. Operational Security Observation via Metadata

Besides segmenting traffic by key epoch and recognizing migration windows (Figure 6), we distinguished exceptional key domains, participating also in their own key rotation schedules, distinct from the network norm. This key domain separation provides inference of clearly confidentiality-level segregated groups of interest belonging to separate agencies or special units therein, whose data and voice traffic needs compartmentalization.

Additionally, because the keying and algorithm choices are signaled in the clear, we can observe which TGs permit mixed encryption and clear traffic and which use salient cipher modes (sections VI-E and VIII-C).

## F. Portable TETRAPOL Observation

We developed modifications for the MMDVM hotspot device to support TETRAPOL demodulation and decoding, and verified the implementation with IQ resampled from a live deployment in a lab-controlled environment with a HackRF SDR and direct interconnects.

Despite the suboptimal TCXO of the low-cost hardware platform we utilized, our adjustments to the demodulation stage in firmware proved capable of sustaining real TETRAPOL decoding on a commodity MMDVM hotspot (Figure 10)—portable, inexpensive interception is practical.

The platform is not a natural fit for TETRAPOL. Its downlink is GMSK (h=0.5, BT=0.3, ∼8000 bit/s in a 12.5 kHz channel), whereas the ADF7021’s Gaussian shaper is fixed at BT≈0.5 and its 14.7456 MHz TCXO clocks only 7680 bit/s— a ∼4% symbol-rate offset. We mitigated this by reusing the ADF7021’s D-Star GMSK path, retiming its clock-recovery loop to the ∼8000 bit/s rate and widening (clamping) the GMSK discriminator, enabling the receive-only chain to sustain live decoding.

![](images/1084434e6271a2dfa12d84b852a67a6fa9f974cb5f6d5fb567c19bf9d115515e.jpg)  
Fig. 10: MMDVM-based TETRAPOL demodulation and decoding portable prototype showing active decoding of a D\_GROUP\_ACTIVATION downlink codop.

## XI. RELATED WORK

Glass et al.’s P25 research began in 2009 with OP25, the open-source P25 receiver, running on a USRP softwaredefined radio, and therefore predates the better-known USENIX study [6]. Their subsequent SecureComm work built on this GNU Radio and USRP implementation to inspect and manipulate the physical and data-link layers of P25 [7]. Most notably, they reverse-engineered Motorola’s Advanced Digital Privacy (ADP), confirmed its use of RC4 with a 40-bit secret key, and showed how known silent vocoder codewords enable practical exhaustive key recovery. The paper presents what appears to be the first public description and practical cryptanalysis of ADP. This work is a direct technical foundation for SDR-driven P25 analysis and deserves recognition as such.

Clark et al. [8] provided complementary field evidence by surveying US deployments with commercial radios. They documented clear law-enforcement calls and selected metadata exposures, including the clear Network Identifier and an apparent implementation error that exposed the Unit Link ID in encrypted voice frames. We extend these foundations by composing signaling fields into identity, topology, presence, organizational, and cryptographic-state inference across protocols (sections VIII, IX and X-B).

Meijer et al. [9] analyzed TETRA’s cryptographic primitives and the consequences of designs that violate Kerckhoffs’s Principle. Pfeiffer et al. [10] examined location leakage and network availability arising from the coordinated signaling between base stations and subscriber radios. These works establish the cryptographic and traditional radio direction finding (location) risks, but do not examine how clear controlplane fields compose over time to recover network topology, presence, affiliation, and organizational structure. Our analysis extends these results through signaling-field reconstruction and cross-protocol inference (sections V, VII and IX).

For TETRAPOL, members of the brmlab hackerspace in the Czech Republic pioneered the first public prototype decoder for the standard. Its scope was mainly control-channel decoding, and it did not implement many air-interface features needed for whole-cell reconstruction. Jan Hrach subsequently developed the FCL channelizer for the frequency-division monitoring requirements of standards such as TETRA and

TETRAPOL [39]. These efforts provide an essential public tooling foundation. We extend it with broader protocol dissection, longitudinal state reconstruction, and security inference (sections VI and X).

Dansarie et al. [40] studied TETRA information security from the users’ perspective. Their work is valuable because LMR standards often lack clearly stated security requirements, leaving trust expectations and operational priorities to be inferred from practice. The authors deliberately exclude technical vulnerabilities in protocols and implementations. Our work addresses that complementary technical question and connects the resulting exposures to operational consequences.

## XII. MITIGATIONS AND COUNTERMEASURES

Our analysis demonstrates that, under the models where confidentiality of communication is expected and relied on, there is no justification for leaving group identifiers openly visible to passive observers. In particular, subscriber, group, and topology identifiers must be protected from passive observation. The adversary need not be particularly sophisticated or physically proximal, as our P25 nearest radio evaluation demonstrates (cf. also [35].)

A layered key architecture can separate infrastructure from subscriber trust and restrict topology broadcasts to the authorized nodes that require them. Subscriber identifier rotation alone is brittle. Statistical linkage, long observation windows, and physical correlation can reconnect an ephemeral identifier to a particular radio or vehicle. Rotation should therefore be frequent and cryptographically unlinkable. Padding and unique per-frame initialization vectors, including across retransmissions, can also reduce known-length and ciphertext-correlation leakage.

The greater obstacle is the long replacement cycle of publicsafety communications systems, whose deployments and contracts may span decades. Standards-level and implementationlevel mitigations will therefore propagate slowly.

## XIII. DISCUSSION AND LIMITATIONS

Ethical and legal constraints most sharply limited this work. Despite strong indications that active attacks and deeper cryptanalysis merit study, we did not pursue active attacks or attempt a cryptographic break using live TETRAPOL deployment data. We also lacked a controlled base station. Continuous legal and ethical review of passive observations substantially narrowed the work.

Capture geometry imposed a second limit. TETRA and TETRAPOL deployments may carry user-defined applications, including SDS. Our observations of exposed application data indicate a sensitive attack surface, but insufficient access and proximity kept a systematic study of that surface out of reach.

We hope this work draws further academic attention and fosters open collaboration among stakeholders, vendors, and interested parties.

## XIV. CONCLUSIONS AND FUTURE WORK

Across TETRA, TETRAPOL, and P25, the structural split between an unprotected signaling plane and (often optional) encrypted traffic plane makes passive, protocol-aware metadata inference a general attack. Standard-specific weaknesses intensify it and can cross the threshold from knowledge of communication to inference of content. WH composes grants, channel assignments, activity, and frame-level semantics to cue downlink and uplink demodulation, decoding, and tracking. The exposed signaling reveals when, where, and what to observe while reducing the required computation and hardware.

Even without content recovery, this leakage reveals organizational structure, presence, mobility, shift turnover, security posture, and preparedness. The threat is particularly acute for law enforcement and first responders. Obscurity offers, at most, a temporary barrier. Affordable SDRs and public tooling have removed the historical cost and expertise assumptions on which it depended.

Traffic analysis remains difficult to prevent in radio protocols. Our future work includes firmware analysis, controlled active-attack experiments, rehosting hardware blackbox cryptographic modules, developing open-source drop-in cryptographic coprocessors, and continued cooperation with stakeholders and users.

## REFERENCES

[1] National Institute of Justice, “Voice encryption for radios,” U.S. Department of Justice, Office of Justice Programs, National Institute of Justice, Washington, DC, Issue Overview NCJ 217103, Mar. 2007, published 1 March 2007; 2 pages; accessed 2 August 2026. [Online]. Available: https://nij.ojp.gov/library/publications/voice-encryption-radios

[2] Project 25 Steering Committee and Cybersecurity and Infrastructure Security Agency, “Statement of project 25 (P25) user needs,” Cybersecurity and Infrastructure Security Agency, Statement of User Needs, Aug. 2023, 87 pages; accessed 2 August 2026. [Online]. Available: https://www.project25.org/images/stories/ptig/Revised Statement of P25 User Needs 508 Approved March 2024 1.pdf

[3] J. P. Vogel, “Reseau radio num´ erique des services de secours´ (ANTARES),” Senat, Commission des finances, Paris, Rapport´ d’information 365 (2015–2016), Feb. 2016, deposited 3 February 2016; 54 pages; accessed 2 August 2026. [Online]. Available: https://www.senat.fr/rap/r15-365/r15-3651.pdf

[4] Centro Tecnologico de Seguridad (CETSE), “SIRDEE (integrated´ state emergency digital radiocommunications system),” Secretar´ıa de Estado de Seguridad, Ministerio del Interior, n.d., project description; accessed 2 August 2026. [Online]. Available: https://cetse.ses.mir.es/publico/cetse/en/fondosEuropeos/fondoISF/ marcoFinanciero-2014-2020/proyectosEuBVI

[5] Bundeswehr, “Tetrapol: Sicher kommunizieren im einsatz,” Bundeswehr, Mar. 2021, article by PAO Counter Daesh; published 25 March 2021; accessed 2 August 2026. [Online]. Available: https://www.bundeswehr de/de/auftrag/einsaetze/einsatz-cd-cbi-tetrapolbw-irak-5045788

[6] S. Glass, V. Muthukkumarasamy, and M. Portmann, “A softwaredefined radio receiver for APCO Project 25 signals,” in Proceedings of the 2009 International Conference on Wireless Communications and Mobile Computing. New York, NY, USA: ACM, 2009, pp. 67–72. [Online]. Available: https://doi.org/10.1145/1582379.1582395

[7] S. Glass, V. Muthukkumarasamy, M. Portmann, and M. Robert, “Insecurity in public-safety communications: APCO Project 25,” in Security and Privacy in Communication Networks (SecureComm 2011), ser. Lecture Notes of the Institute for Computer Sciences, Social Informatics and Telecommunications Engineering, vol. 96. Berlin, Heidelberg: Springer, 2012, pp. 116–133. [Online]. Available: https://espace.library.uq.edu.au/view/UQ:259862

[8] S. Clark, T. Goodspeed, P. Metzger, Z. Wasserman, K. Xu, and M. Blaze, “Why (special agent) Johnny (still) can’t encrypt: A security analysis of the APCO Project 25 two-way radio system,” in 20th USENIX Security Symposium (USENIX Security 11). San Francisco, CA: USENIX Association, Aug. 2011. [Online]. Available: https://www.usenix.org/conference/usenix-security-11/ why-special-agent-johnny-still-cant-encrypt-security-analysis-apco

[9] C. Meijer, W. Bokslag, and J. Wetzels, “All cops are broadcasting: TETRA under scrutiny,” in 32nd USENIX Security Symposium (USENIX Security 23). Anaheim, CA: USENIX Association, Aug. 2023, pp. 7463–7479. [Online]. Available: https://www.usenix.org/ conference/usenixsecurity23/presentation/meijer

[10] M. Pfeiffer, J.-P. Kwiotek, J. Classen, R. Klose, and M. Hollick, “Analyzing TETRA location privacy and network availability,” in Proceedings of the 6th Workshop on Security and Privacy in Smartphones and Mobile Devices. New York, NY, USA: Association for Computing Machinery, 2016, pp. 117–122. [Online]. Available: https://doi.org/10.1145/2994459.2994463

[11] Terrestrial Trunked Radio (TETRA); Voice plus Data (V+D), ETSI, 2023, EN 300 392 series. [Online]. Available: https://www.etsi.org/ standards

[12] A. Esmaeilifar, “Public safety networks: Analysis of the TETRA standard: History and evolution,” Master’s thesis, Politecnico di Torino, Turin, Italy, 2025.

[13] Airbus (Secure Land Communications), “Tetrapol — airbus public safety and security,” https://www.criticalcommunications.airbus.com/en/ tetrapol, 2024, product overview; national networks incl. RUBIS, ACROPOL, SIRDEE, PEGAS, POLYCOM.

[14] Wikipedia contributors, “TETRAPOL,” https://en.wikipedia.org/wiki/ TETRAPOL, 2024, cites deployment footprint of ≈80 networks in 34 countries and per-country users.

[15] Critical Communications, “Mexico’s melting pot: P25, TETRA, Tetrapol, DMR and LTE,” https://www.criticalcomms.com/content/ features/mexico-s-melting-pot/, 2019, red Nacional de Radiocomunicacion (Red IRIS). More than 110,000 terminals across 32 states.´

[16] Revista Seguridad 360, “TETRAPOL en mexico: La red IRIS y la´ red nacional de radiocomunicacion,” https://revistaseguridad360.com/´ noticias/comunicaciones/sistema-tetrapol/, 2018, matra Nortel Communications contract (1998); PGR, CISEN, SEDENA, SEMAR.

[17] Airbus (Secure Land Communications), “PROAMATEC — brazilian police network,” https://criticalcommunications.airbus.com/newsroom/ web-story/integrapol-brazilian-police-network, 2018, federal Police TETRAPOL network launched 2005; five regional TETRAPOL IP networks.

[18] Police Professional, “Tetrapol technology underpins security at Brazil world cup,” https://policeprofessional.com/news/ tetrapol-technology-underpins-security-at-brazil-world-cup/, 2014, integrapol; >280 radio sites and tactical repeaters; implemented 2005–2010; Ceara TETRAPOL IP.´

[19] Airbus Secure Land Communications, “TETRAPOL publicly available specifications,” https://www.criticalcommunications.airbus.com/en/ tetrapol-publicly-available-specifications, Oct. 2024, accessed 2026-07- 14.

[20] TETRAPOL Specifications; Part 3: Air Interface Protocol; Part 2: Air Interface Application Messages, TETRAPOL Secretariat, Sep. 2021, version 2.3.9. [Online]. Available: https://www.criticalcommunications.airbus.com/sites/g/files/ jlcbta221/files/2024-10/pas132%20air%20interface%20message.pdf

[21] Project 25 (P25) / TIA-102 Standards Suite, Telecommunications Industry Association (TIA), 2023, TIA-102 series. [Online]. Available: https://standards.tiaonline.org/standards-technology

[22] arancormonk, “dsd-neo,” https://github.com/arancormonk/dsd-neo, 2026, modular fork of the Digital Speech Decoder (DSD/dsd-fme).

[23] TETRAPOL Specifications; Part 3: Air Interface Protocol; Part 1: Air Interface Application Protocol, TETRAPOL Secretariat, Sep. 2021, version 2.3.9. [Online]. Available: https://www.criticalcommunications. airbus.com/en/tetrapol-publicly-available-specifications

[24] TETRAPOL Specifications; Part 3: Air Interface Protocol; Part 3: Air Interface Transport Protocol, TETRAPOL Secretariat, Nov. 2003, version 2.0.6. [Online]. Available: https://www.criticalcommunications. airbus.com/en/tetrapol-publicly-available-specifications

[25] TETRAPOL Specifications; Part 13: Point-to-Point Short Data; Part 2: Submit/Delivery Protocol, TETRAPOL Forum, Jun. 1997, version

1.0.5. [Online]. Available: https://www.criticalcommunications.airbus. com/en/tetrapol-publicly-available-specifications

[26] Project 25 Security Services Overview, Addendum 1, Telecommunications Industry Association (TIA), Sep. 2014. [Online]. Available: https: //connect.tiaonline.org/viewdocument/tia-102aaab-a-digital-land-mobil

[27] Project 25 Security Services Overview, Telecommunications Industry Association (TIA), Jan. 2005, superseded by TIA-102.AAAB-B; cited for the traffic-analysis threat model and optional air-interfaceencryption architecture. [Online]. Available: https://connect.tiaonline. org/viewdocument/tia-102aaab-a-digital-land-mobil

[28] Project 25 Technology Interest Group, “P25 Standards Update,” Project 25 Technology Interest Group (PTIG), Tech. Rep., Jul. 2025, june–July 2025 update. [Online]. Available: https://www.project25.org/images/stories/ptig/250710% 20June-July%20%20P25%20Standards%20Update%20.pdf

[29] Project 25 Trunking Control Channel Messages, Telecommunications Industry Association (TIA), 2019. [Online]. Available: https://connect. tiaonline.org/viewdocument/tia-102aabc-e-trunking-control-c

[30] Project 25 FDMA Common Air Interface, Telecommunications Industry Association (TIA), 2003, reaffirmed 2013. [Online]. Available: https: //connect.tiaonline.org/viewdocument/tia-102baaa-a-fdma-common-air

[31] Wikipedia contributors, “BATON,” https://en.wikipedia.org/wiki/ BATON, 2024, NSA Type 1 block cipher, publicly documented in use since at least 1995.

[32] OP25 Project (boatbod fork), “OP25: An APCO P25 receiver/decoder — algorithm-identifier string table,” https://github.com/boatbod/op25/blob/ b2e04c3f3f4ace2cd29e3b4cbf6b89e0955c6818/op25/gr-op25/lib/value string.cc, 2024, file op25/gr-op25/lib/value\_string.cc (commit b2e04c3); P25 ALGID → cipher-name mapping, including Type 1 algorithms.

[33] Wikipedia contributors, “STU-III,” https://en.wikipedia.org/wiki/ STU-III, 2024, NSA secure-telephone family introduced 1987; employs the FIREFLY key-exchange protocol.

[34] ——, “SAVILLE,” https://en.wikipedia.org/wiki/SAVILLE, 2024, classified NSA/GCHQ Type 1 voice cipher, developed in the late 1960s.

[35] A. Greenberg, “Russian spies jumped from one network to another via Wi-Fi in an unprecedented hack,” Wired, Nov. 2024, published November 22, 2024; accessed July 29, 2026. [Online]. Available: https://www.wired.com/story/russia-gru-apt28-wifi-daisy-chain-breach/

[36] National Interoperability Field Operations Guide (NIFOG), Cybersecurity and Infrastructure Security Agency, U.S. Department of Homeland Security, Mar. 2022, version 2.01. [Online]. Available: https://www.cisa.gov/sites/default/files/2023-04/NIFOG%202.01 508%20FINAL%20VERSION%205%2011%2022.pdf

[37] RadioReference.com, “The RadioReference database,” https://www. radioreference.com/db/, 2026, community-maintained database of radio systems, sites, frequencies, and talk-group assignments.

[38] ——, “Trunked radio system profile, SID 7508,” https://www. radioreference.com/db/sid/7508, 2026, public site, frequency, and talkgroup listing for a National Capital Region public-safety trunked system.

[39] J. Hrach, “Frequency spectrum monitoring system,” Bachelor’s thesis, Charles University, Faculty of Mathematics and Physics, Prague, Czech Republic, Sep. 2016. [Online]. Available: https: //dspace.cuni.cz/handle/20.500.11956/80128

[40] M. Dansarie and M. Nohlberg, “User adoption of TETRA mobile radio communication networks: An information security perspective,” Information and Computer Security, vol. 33, no. 5, pp. 766–784, 2025. [Online]. Available: https://doi.org/10.1108/ICS-12-2024-0318

## APPENDIX A ETHICAL CONSIDERATIONS AND RESPONSIBLE DISCLOSURE

All measurements in this work were passive and receiveonly. We transmitted nothing, mounted no active (e.g., denialof-service) attacks, and never authenticated to or joined a network. Our analysis targets the signaling plane and elements of the management and traffic planes, which these systems already broadcast unencrypted. We recovered data traffic only to the minimum needed to demonstrate the weakness. For the emergency-call analysis we processed voice content only to establish intelligibility, encryption state, and the semantic relationship between the observed ECH activation and the terminal’s emergency control. We retained no transcript beyond the minimal excerpt needed to establish that relationship, and publish no names or identifying operational content.

We treat all captured identifiers as sensitive. Subscriber and unit IDs, cell, network, and location-area identifiers, exact carrier frequencies, and recovered coordinates are anonymized or coarsened in the public copies of the paper—carrier frequencies masked to band level, identifiers consistently relabeled—while the true values are withheld, and we release no raw captures, recovered keys, third-party audio, or operatoridentifying data. All reception was conducted in accordance with applicable law.

We withhold any tooling that would enable trivial misuse or endanger users. Any tooling under limited and justified dissemination is unrestricted fundamental research intended for publication and defensive evaluation, for reproducing our results on the researcher’s own equipment. It confers no capability beyond that already available to a determined passive adversary. We likewise omit implementation details whose disclosure would ease replication of the more sensitive capabilities without adding to understanding of the underlying weakness. Preprints and final revisions are published with besteffort harm reduction and in the public interest.

## APPENDIX B TETRAPOL CLEAR-VERSUS-ENCRYPTED CALL CLASSIFICATION

WH assigns each TETRAPOL call one of two clear/encrypted verdicts, and the difference between them governs how the label may be used. The signaling verdict $\widehat { S } _ { \mathrm { s i g } }$ is authoritative: it is read directly from the standard-mandated KEY\_REFERENCE field of a fully validated call grant, and it is the only verdict that labels a call clear or encrypted. It is what drives the clear-call detection behind the emergency call extraction of section X-D, where an UNENCRYPTED\_CALL key reference cues retrospective recovery of clear voice. The advisory verdict $\widehat { S } _ { \mathrm { a d v } }$ is a heuristic fallback used only when no grant supplies a key reference: it scores the decoded voice and can report a call candidate clear, not clear, or inconclusive, but it never overrides $\widehat { S } _ { \mathrm { s i g } }$ and never asserts “encrypted.” Its sole purpose is to surface clear speech on a channel captured without a decodable grant.

## A. Signaling verdict (authoritative)

For a complete, structurally valid grant or channel-activation PDU, let K be the decoded KEY\_REFERENCE octet. Its high nibble is the key type $T = K \gg 4$ , and its low nibble is the key index $I = K$ & 0x0f. PAS 0001-3-2 [20], §5.3.41, yields the implemented verdict

$$
\widehat {S} _ {\text { sig }} (K) = \left\{ \begin{array}{l l} \text { clear }, & I = 0 \land T \in \{0, 1 5 \}, \\ \text { encrypted }, & \text { otherwise }. \end{array} \right.\tag{1}
$$

Equivalently, only $K \in \{ 0 \mathbf { x } 0 0 , 0 \mathbf { x } \mathbf { f } 0 \}$ is clear. Every other26 decoded value is encrypted, including 0x50, whose zero index<sup>27</sup> does not make its OAK key type clear. An absent key reference<sup>28</sup> remains unknown and is never replaced with zero.

Before applying eq. (1), the decoder validates the complete PDU, including its mandatory tail, reserved fields, defined enumerations, and exact message consumption. The frame check sequence is not a discriminator, since ciphertext is equally FCS-valid. A byte sequence that merely reaches the key-reference position is therefore not authoritative.

The verdict is then cached per allocation, identified by the carrier together with its locked dynamic-scrambling constant. A known verdict survives a grant timeout (the grant time-to-live default is 30 s) only within the same carrierand-scrambling allocation: while the carrier holds the same scrambling, an interval with no fresh grant reuses the cached verdict rather than reverting to unknown. A scrambling change or release, a conflicting decoded verdict, a lost lock, or a call ending idle gap (≈ 6 s without voice) retires the allocation and starts a new one with unknown state. Scoping the verdict to the scrambling constant keeps a stale label from leaking across calls.

## B. No-grant speech classification (advisory)

When no grant supplies K, WH scores the decoded voice for a speech-like signature. Clear and encrypted TETRAPOL voice differ sharply in their short-term statistics: a genuine speech envelope evolves smoothly from frame to frame and its quantizer indices occupy a characteristic mid-entropy band, whereas ciphertext yields near-independent coefficients with no frame-to-frame correlation and near-uniform indices. The test reduces a call to three summary features—an envelope coherence C, a width-normalized index entropy H, and a distinct-block fraction D—and accepts only the clear-speech region of (C, H, D). Treating mean, variance, covariance, and Shannon entropy as standard estimators, the procedure is

```python
# advisory clear-speech verdict S_adv
# in:
#    B[1..N] = CRC-3-valid 120-bit RP-CELP blocks
# const:
#    Nmin=8, eps=1e-12,
#    tauC=0.15, Hlo=0.80, Hhi=0.97, tauD=0.60
if N < Nmin:
    return INCONCLUSIVE

# each log-area-ratio (LAR) index
for i in 1..10:
    r_i = [reflection(B[n], i) for n in 1..N]
    v = var(r_i)
    # lag-1
    a[i] = 0 if v <= eps else cov(r_i[1:N-1], r_i[2:N]) / v

# envelope coherence
C = clip(mean(a[1..10]), 0, 1)

# width-normalized
H = mean(entropy(x[:, i]) / b[i] for i in 1..10)

# distinct-block fraction
D = num_distinct(B[1..N]) / N
```

```txt
if C >= tauC and Hlo <= H <= Hhi and D >= tauD:
    return CANDIDATE_CLEAR
return NOT_CLEAR
```

The formulas below fix the exact estimators the pseudocode treats as library calls. Given N CRC-3-valid, 120-bit RP-CELP codec blocks $B _ { n } ,$ , for each of the ten log-area-ratio (LAR) indices the decoder reconstructs a reflection coefficient $r _ { n , i } .$ It then computes the mean $\bar { r } _ { i }$ , variance $v _ { i }$ , lag-one covariance q , autoregressive coefficient $a _ { i } .$ , and mean coherence C as

$$
\bar {r} _ {i} = \frac {1}{N} \sum_ {n = 1} ^ {N} r _ {n, i},\tag{2}
$$

$$
v _ {i} = \frac {1}{N} \sum_ {n = 1} ^ {N} (r _ {n, i} - \bar {r} _ {i}) ^ {2},\tag{3}
$$

$$
q _ {i} = \frac {1}{N - 1} \sum_ {n = 1} ^ {N - 1} (r _ {n, i} - \bar {r} _ {i}) (r _ {n + 1, i} - \bar {r} _ {i}),\tag{4}
$$

$$
a _ {i} = \left\{ \begin{array}{l l} 0, & v _ {i} \leq 1 0 ^ {- 1 2}, \\ q _ {i} / v _ {i}, & v _ {i} > 1 0 ^ {- 1 2}, \end{array} \right.\tag{5}
$$

$$
C = \mathrm{clip} _ {[ 0, 1 ]} \left(\frac {1}{1 0} \sum_ {i = 1} ^ {1 0} a _ {i}\right).\tag{6}
$$

The coherence C is the mean lag-one autocorrelation of the ten reflection-coefficient tracks, clipped to [0, 1]; it measures how smoothly the spectral envelope evolves, and is high for real speech but near zero for ciphertext. The variance floor $1 0 ^ { - 1 2 }$ guards the ratio $q _ { i } / v _ { i } \colon$ a coefficient whose reconstructed track is essentially constant carries no autocorrelation evidence, so it contributes $a _ { i } = 0$ rather than a ratio dominated by floatingpoint noise.

Let $x _ { n , i }$ be LAR index i of block n, with quantizer field widths $\pmb { b } ~ = ~ ( 5 , 5 , 4 , 4 , 4 , 3 , 3 , 3 , 3 , 3 )$ bits, and let $\begin{array} { r l } { p _ { i , j } } & { { } = } \end{array}$ ${ \frac { 1 } { N } } \# \{ n : x _ { n , i } = j \}$ . The width-normalized index entropy H and the distinct-block fraction D are

$$
H = \frac {1}{1 0} \sum_ {i = 1} ^ {1 0} \frac {1}{b _ {i}} \left(- \sum_ {j: p _ {i, j} > 0} p _ {i, j} \log_ {2} p _ {i, j}\right),\tag{7}
$$

$$
D = \frac {| \{B _ {1} , \ldots , B _ {N} \} |}{N}.\tag{8}
$$

The inner sum is the base-2 Shannon entropy of index i’s empirical distribution, since a $b _ { i } .$ -bit field carries at most $b _ { i }$ bits of entropy, dividing by $b _ { i }$ expresses it as an occupancy fraction in [0, 1] and renders the ten indices—which have different alphabet sizes—comparable before averaging. Real speech occupies a mid band $( H \approx 0 . 8 9 – 0 . 9 3 )$ , whereas nearuniform ciphertext indices give $H \approx 1$ . The distinct-block fraction D is the share of the N blocks $B _ { n }$ that are unique: real speech is almost entirely distinct, whereas a degenerate reachback or idle alias—the decoder latching a fixed-scrambling carrier that is idle or replaying a handful of frames from a prior call—repeats blocks and drives D down.

With the chosen thresholds, define the acceptance gate

$$
\mathcal {G} = [ C \geq 0. 1 5 ] \wedge [ 0. 8 0 \leq H \leq 0. 9 7 ] \wedge [ D \geq 0. 6 0 ],\tag{9}
$$

so that the advisory verdict is

$$
\widehat {S} _ {\mathrm{adv}} = \left\{ \begin{array}{l l} \text {   inconclusive,   } & N <   8, \\ \text {   candidate   clear,   } & N \geq 8 \land \mathcal {G}, \\ \text {   not   clear,   } & N \geq 8 \land \neg \mathcal {G}. \end{array} \right.\tag{10}
$$

Each bound in G separates observed clear speech from a specific confound. Clear speech has smooth envelopes $( C \approx$ 0.62–0.68), mid-band entropy $( H \approx 0 . 8 9 – 0 . 9 3 )$ , and mostly distinct blocks. Encrypted blocks have $C \approx 0$ and $H \approx 1$ The coherence floor 0.15 thus sits far below clear speech yet well above ciphertext. The entropy band [0.80, 0.97] excludes both near-uniform ciphertext $( H \approx 1 )$ and the low-entropy degenerate aliases $( H \approx 0 . 2 6 )$ , and $D \geq 0 . 6 0$ rejects their repeated blocks $( D ~ \approx ~ 0 . 2 0 )$ . A reach-back can fake high coherence through repeated frames, but its low entropy and low distinct fraction reject it. Requiring $N \geq 8$ blocks keeps the estimates stable. Because the test only confirms or fails to confirm clear speech, not clear withholds a clear label rather than asserting encryption—the encrypted judgment is reserved for the authoritative $\widehat { S } _ { \mathrm { s i g } } .$

## APPENDIX C

## TETRAPOL CALL POST-FEC SPECTRAL RENDERING

WH preserves no-grant streams with an unknown signaling state for later analysis. The advisory RP-CELP signature in section B operates on these streams without overriding the signaling verdict. Clear and encrypted calls exhibit the spectral differences shown in fig. 11.

## A. Spectral Rendering

393.8xx MHz, SCR 97, t=13813 s, unknown key  
![](images/e89220964cb8e955436df5c3dd6b0e62dae0e7edec67ff1220a98105956a37d1.jpg)

394.6xx MHz, SCR 82, unknown key  
![](images/1951992d48c6c2606d4271d64128965d687c2f9bae32ed93283b31a1997b88fd.jpg)  
Fig. 11: Spectrograms of encrypted call and clear TETRAPOL emergency calls (post-FEC and post-descrambling).

The WH pipeline classified the call from its ECH grant and retrospectively extracted it from the ring buffer while preserving the original IQ:

```txt
20881874:[ECH-DL #1] channel_id=2902 dl_carrier=3946
xxxxx d_scr=82 u_scr=76 t=2164.7s codop=0x56
key_reference=0x00 [CLEAR-EMERGENCY]
20884669:[ECH-DL-CAPTURE] ch2902 c3946xxxxxxHz codop
=0x56 d_scr=82 scr_used=82 FIXED=true
key_reference=0x00 clear=true t_grant=2164.7s
extract=13200000 samples (55.0s) frames=2749
voice=177 voice_crc=167/177 wav=(...)/
ech_dl_c3946xxxxxxHz_ch2902_dscr82_crc167of177_t2165s
.wav iq=(...)/ech_dl_c3946xxxxxxHz_ch2902_t2165s.
cs16
```

## APPENDIX D HARDWARE

## A. Self-built Experimental Multi-SDR Platform

The SDR hardware employed throughout this effort is pictured in Figure 12. The design is not particularly sophisticated: power is supplied by a regulated linear supply, converted to a stable 5V DC by ultra-low noise LDO regulators (TPS7A4700 and LT3042), and monitored in a closed loop by a controller that can manage individual supplies to each SDR. On the RF side, an ad-hoc selection of components enables filtering of out-of-band strong signals (primarily commercial FM broadcast), limiting of strong RF signals, power for antenna-feed low noise amplifiers (decoupled from the SDRs) and antenna switching with a GaAs RF SPDT switch (Analog Devices HMC349ALP4CE).

The two HackRF boards are modified (section D-B) and share a common TCXO. The Pluto-design SDR has a clock input for an external GPS disciplined oscillator (not pictured). A PPS pin is broken out for both HackRFs for optional coherent reception.

Reception used colinear and discone antennas behind bandstop filtering that also rejected out-of-scope RF energy. A spare SDR transmit port doubles as a built-in path for sensitivity checks and feedline/antenna diagnostics, and a separate BladeRF/HackRF bench inside a shielded RF-isolation cage supported onsite reverse engineering.

The system was designed, built and fielded in under two weeks time, and was mostly built from a parts bin, to demonstrate that the cost and skill barrier today is orders of magnitude lower than it used to be.

## B. HackRF VBUS Isolation PCB Modification

The dual HackRF configuration with a shared TCXO necessitated preventing any remnant—radiated or conducted— noise from impacting function. Despite the use of ultra-low noise regulators (Texas Instruments TPS7A4701), this was a desirable improvement. The VBUS trace was cut off under microscope, with the ferrite bead removed. The trace was then cut in two spots, allowing placement of a diode to prevent backfeed from the independent pin-fed 5V power towards the USB host, and the original ferrite immediately after.

The modification requires a steady hand and microscope magnification.

![](images/2755a4d3043db8ea0ced7b9b64d04f966099cb38a8cb908d3e25186ace10f52a.jpg)  
Fig. 12: Self-built Experimental Multi-SDR Platform

![](images/139167f0425da426c9c6099bc5fa94a8891d78936f5ce77deb84a3056d776825.jpg)  
Fig. 13: HackRF One with USB VBUS isolated for the dualreceiver platform in section IV-A.
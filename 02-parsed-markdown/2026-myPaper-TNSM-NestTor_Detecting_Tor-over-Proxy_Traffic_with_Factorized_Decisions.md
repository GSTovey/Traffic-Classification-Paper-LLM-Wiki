Regular Issue submission

# NestTor: Detecting Tor-over-Proxy Traffic with Factorized Decisions

Submission ID f0a9fc78-a2c5-44cb-b87d-d8cc74933db2

Manuscript ID TNSM-2026-11826.R2

Submission Version Revision 3

PDF Generation 10 Oct 2026 09:50:50 EST by Atypon ReX

## Authors

Dr. Chenxin Zhou

Affiliations

• the School of Cyber Science and Engineering, Sichuan University, Chengdu 610207, China

Prof. Cheng Huang Corresponding Author Submitting Author

ORCiD

Affiliations

https://orcid.org/0000-0002-5871-946X • the School of Cyber Science and Engineering, Sichuan University, Chengdu 610207, China

Dr. Qiang Zhang

Affiliations

• the School of Cyber Science and Engineering, Sichuan University, Chengdu 610207, China

Dr. Qiliang Xie

## Affiliations

• the School of Cyber Science and Engineering, Sichuan University, Chengdu 610207, China

Mr. Zeqing Li

Affiliations

• the School of Cyber Science and Engineering, Sichuan University, Chengdu 610207, China

## Additional Information

## Keywords

2. Service Management / Security Services Security Services

4. Functional Areas / Security Management Security Management

6. Technologies / Communication Protocols Communication Protocols

7. Methods / Artificial Intelligence and Machine Learning Artificial Intelligence and Machine Learning

7. Methods / Monitoring and Measurements Monitoring and Measurements

Is this manuscript a resubmission of, or in any way related to, a manuscript previously rejected, reviewed, or withdrawn from IEEE TNSM or any other journal or conference? Explain in details (e.g. reasons behind rejections, improvements since rejection, etc)

No

Is this manuscript an extended version of a conference publication (or conference article accepted for publication)?

No

Is this manuscript related to any other papers of the authors that are either published, accepted for publication, or currently under review, and that are not included among the references cited in the manuscript?

No

Are there any preprints of the manuscript (i.e. preprints that are identical to the submitted manuscript, except for minor differences) that have been posted on the authors’ personal website, employer’s website or institutional repository, arXiv.org, TechRxiv.org, or on any not-for-profit preprint server approved by the IEEE?

No

Are there any other posted preprints that should not be considered to be prior art?

No

Explain in detail why the contribution of this manuscript is within the scope of the IEEE Transactions on Network and Service Management?

This manuscript is within TNSM's scope because it addresses the monitoring and security management of encrypted network services. It defines a passive single-flow method for detecting Tor-over-Proxy traffic using packet direction, payload length, and relative timing. The work covers Security Management, Monitoring and Measurements, Communication Protocols, Security Services, and AI/ML, while also addressing calibration, distribution shift, robustness, and deployment cost.

Why is the contribution significant (What impact will it have)?

The contribution is significant because existing classifiers usually treat Tor and proxy traffic as separate targets, whereas Tor-over-Proxy combines both conditions and disrupts conventional packet patterns. NestTor's factorized design improves detection and identifies whether failures arise from proxy recognition or inner-Tor discrimination. Its longitudinal, leakage-controlled evaluation provides practical evidence for building more reliable encrypted-traffic monitoring systems.Unlike prior T

## List three to five recent papers published in IEEE TNSM that are most closely related to this manuscript

1. chen2023classify (Classify traffic rather than flow: Versatile multi-flow encrypted traffic classification...) 2. zhao2024metarocketc (MetaRockETC: Adaptive encrypted traffic classification in complex network...) 3. yang2024convitml (ConViTML: A convolutional vision transformer-based meta-learning framework...) 4. du2026tunneleye (TunnelEye: An Explainable Framework for Real-Time Detection of Malicious DoH Traffic...)

## What is distinctive/new about the current paper relative to these previously published works?

Unlike prior Tor, proxy, and encrypted-traffic classifiers, this paper formulates Tor-over-Proxy as a composite condition and separately models proxy presence and Tor behavior. It covers four proxies, introduces negative-only calibration without target ToP labels, and analyzes which behaviors survive encapsulation. Its 349,891-flow benchmark uses domain- and capture-disjoint splits and evaluates unseen domains, proxy holdout, later captures, open-world traffic, transformations, and cost.

## Files for peer review

All files submitted by the author for peer review are listed below. Files that could not be converted to PDF are indicated; reviewers are able to access them online.

<table><tr><td>Name</td><td>Type of File</td><td>Size</td><td>Page</td></tr><tr><td>manualscript.pdf</td><td>Main Document - PDF</td><td>1.6 MB</td><td>Page 5</td></tr></table>

# NESTTOR: Detecting Tor-over-Proxy Traffic with Factorized Decisions

Chenxin Zhou , Cheng Huang , Senior Member, IEEE, Qiang Zhang , Qiliang Xie , and Zeqing Li

Abstract—Tor users can place an encrypted proxy between the client and the Tor network to conceal the exposed entry connection. This additional layer also transforms the Tor byte stream through protocol framing, buffering, and TCP segmentation before an observer sees the outer client-to-proxy flow. The transformation breaks stable packet-to-cell alignment and raises two questions. We ask which Tor behaviors remain observable across different proxies and how a detector should combine the presence of an outer proxy with the presence of Tor traffic. Existing datasets primarily study Tor and proxy traffic as separate targets and provide limited support for answering these questions under a unified evaluation protocol. We propose NESTTOR, which trains a proxy gate and a proxy-conditioned Tor detector separately and combines their decisions with an AND rule. Its stage-based features capture relative connection evolution without reconstructing Tor cells. We construct a longitudinal benchmark of 349,891 bidirectional TCP flows that distinguishes Tor-over-Proxy (ToP), Pure Proxy, Direct Tor, and Ordinary traffic across four proxy protocols, 1,663 domains, and approximately 18 months. NESTTOR achieves 99.45% macro-F1 on confirmatory data from unseen domains and 88.50% on later captures.

Index Terms—Tor, proxy servers, encrypted traffic analysis, traffic classification, distribution shift

## I. INTRODUCTION

Tor hides the direct association between communicating parties through multi-hop onion routing [1], yet the clientto-entry hop remains observable. Its protocol interactions and traffic behavior support Tor bridge discovery [2] and website fingerprinting [3]. Users can conceal this entry connection by using one of four common proxy implementations, Shadowsocks, Trojan, VMess, or VLESS, before accessing Tor. The observer consequently sees an outer flow between the client and proxy rather than the Tor entry connection. We refer to this configuration as Tor-over-Proxy (ToP). Proxy encapsulation changes both the appearance of Tor traffic and the object available for detection.

We define ToP by the joint presence of an outer proxy and Tor traffic on the same communication path. Pure Proxy and Direct Tor isolate these two conditions and serve as hard negatives. Figure 1 illustrates the four communication paths and our passive observation position between the client and proxy server. A detector must estimate both conditions from a single bidirectional TCP flow before assigning the ToP label.

At a client egress or local gateway, this setting supports screening of completed flows, traffic measurement, and forensic analysis in managed networks. We evaluate the offline processing pipeline.

![](images/03e675baa3217caf5367cb7986ac8e4a0da52df2a5c3e585edf4f4a210386e71.jpg)  
Fig. 1. ToP communication paths and the passive observation point.

Prior work largely detects encrypted tunnels [4], censorshipresistant proxies [5], [6], [7], Tor bridges [2], and multi-stage attributes [8]. SETTDM [9] further demonstrates Obfs4-over-VMess detection. Existing studies nevertheless treat the outer proxy, Tor traffic, or a specific encapsulation as the primary target. We study four outer proxies and include Pure Proxy and Direct Tor under splits disjoint by domain and capture.

Proxy transformation creates the first problem. Authentication, encryption, framing, buffering, TCP coalescence, and network resegmentation remove a stable correspondence between observed packets and individual Tor cells. Fixed cellscale regularities may therefore disappear, whereas interaction order and relative connection evolution may remain observable across proxies. We test these hypotheses through a protocol audit and construct stage-based flow features from direction, payload length, and relative timing.

The composite ToP label creates the second problem. A flat objective may rely disproportionately on proxy evidence or Tor behavior, producing concentrated errors on Pure Proxy or Direct Tor. NESTTOR assigns proxy presence to a proxy gate and learns the Tor presence condition within proxy traffic using a separate detector. The system assigns the ToP label only when both classifiers return positive decisions.

Evaluation introduces the third problem. Addresses, ports, domains, capture timestamps, and sample provenance can become classification shortcuts [10], [11], [12]. We exclude identifier fields, separate domains and captures across partitions, and restrict access to target labels. Models, thresholds, and analysis rules are frozen before confirmatory evaluation. Later analyses test structural controls, proxy holdout, capture shift, packet transformations, and heterogeneous background traffic.

These problems lead to four research questions. RQ1 examines behavior that remains observable across proxies, while RQ2 measures detection under leakage controls. RQ3 isolates contributions from the representation and decision structure. RQ4 evaluates generalization across proxy types and capture conditions. Our main contributions are as follows:

• Observable behavior after proxy transformation. We formalize the client-to-proxy observation path and derive two testable signal families from the loss of packet-to-cell alignment. An audit across four proxies finds evidence in directional interaction, stage evolution, and coupling between bursts and responses.

• Factorized detection of the composite ToP label. NESTTOR separately trains a proxy gate and a proxyconditioned Tor detector. It reaches 99.45% macro-F1 in the confirmatory evaluation and consistently exceeds flat and shared alternatives in controlled comparisons.

• Longitudinal evaluation with leakage controls. We construct a benchmark of 349,891 deduplicated flows across four proxy protocols, 1,663 domains, and approximately 18 months. The evaluation excludes identifiers, separates domains and captures, and covers later captures and 11,131 heterogeneous background flows.<sup>1</sup>

The remainder of this paper is organized as follows. Section II reviews the background and related work. Section III defines the threat model and analyzes observable protocol behavior. Section IV presents NESTTOR, Section V describes the experimental setup, and Section VI reports the results and discussion. Section VII concludes the paper.

## II. BACKGROUND AND RELATED WORK

This section reviews Tor and encrypted proxy encapsulation, prior work on proxy and Tor detection, encrypted traffic representations, and evaluation risks arising from data shortcuts and distribution shift.

## A. Tor and Encrypted Proxy Encapsulation

Tor relies on layered encryption and multi-hop relays to hide the direct association between communicating parties. Communication is conducted in structured cells with channel negotiation, circuit construction, and flow control [1]. In the ToP setting, the Tor byte stream passes through the proxy client, where the proxy protocol encapsulates it, before en tering the TCP connection from the client to the proxy server. We study Shadowsocks, Trojan, VMess, and VLESS. Their authentication, framing, buffering, and transport mechanisms differ, as Section III describes. This processing alters outer TCP packet lengths and boundaries, so a single outer packet typically no longer corresponds to a single Tor cell.

## B. Proxy, Tunnel, and Tor Detection

Encrypted tunnel detection uses packet and flow statistics [4]. Studies of censorship-resistant proxies examine resistance to active probing [5], Shadowsocks identification [6], and passive detection of fully encrypted traffic [7]. These methods identify the outer proxy or tunnel, whereas ToP detection must characterize the traffic it carries.

Tor bridge detection uses behavioral features observed in backbone networks [2]. Fingerprinting of encapsulated handshakes identifies proxies from traffic patterns induced by nested TLS handshakes [13]. Cross-layer analysis uses discrepancies between transport- and application-layer roundtrip times as a protocol-agnostic proxy fingerprint [14].

STNet combines spatiotemporal features at multiple scales with adaptation to each scenario for Tor classification under limited labels, including closed and open world settings [15].

SETTDM [9], the closest setting to ours, studies Obfs4 Tor over VMess through temporal and spatial subflow features. Its evaluation of a specific encapsulation does not establish which Tor interaction signals remain observable across different outer proxies. We investigate this question through a protocol audit across four proxies and use Pure Proxy and Direct Tor to distinguish outer proxy evidence from inner Tor behavior.

Other methods integrate multiple traffic dimensions [16], extract stage-specific attribute fingerprints [8], or use TLSguided semantic learning to identify applications inside encrypted tunnels [17].

## C. Encrypted Traffic Representation

Statistical and correlation-based representations support application and security classification using flow measurements and traffic relationships [18], [19], [20], [21], [22]. Handshake fingerprints such as JA4 [23] construct connection fingerprints from TLS initialization parameters. In the ToP setting, the visible handshake connects only the client and the proxy.

FlowPic transforms flow measurements into images for application identification across encrypted, VPN, and Tor traffic [24]. A time-series approach further identifies applications within VPN tunnels [25]. These studies support using traffic behavior to characterize encrypted communication.

End-to-end approaches learn from byte sequences, packet sequences, or traffic images. FS-Net [26] uses a bidirectional recurrent encoder-decoder with sequence reconstruction. ET-BERT [27] organizes traffic bytes into tokens with a pretrained backbone, while YaTC [28] converts traffic into multilevel images for a pretrained vision model. NetMamba [29] and TrafficFormer [30] add recent state-space and pretrained Transformer architectures. These models provide representative and recent baselines for testing the composite ToP label.

## D. Data Shortcuts, Distribution Shift, and Evaluation

Encrypted traffic models readily exploit identifiers and collection attributes unrelated to the target protocol. IP addresses, ports, domains, and capture provenance can form classification shortcuts and produce high closed-set performance without learning transferable protocol behavior [10], [11], [12]. Random flow-level splits can allow related flows from the same session, domain, or capture batch to span training and test partitions, inflating performance estimates. In the ToP setting, differences across proxies in authentication, encryption, framing, and buffering introduce shifts tied to the proxy type, and dynamic network conditions affect model stability [31].

Existing public benchmarks rarely include Ordinary, Direct Tor, Pure Proxy, and ToP under a unified evaluation protocol with splits disjoint by domain and capture. To suppress identifier and provenance shortcuts, the NESTTOR Benchmark uniformly excludes addresses, ports, domains, and identifier fields from model inputs. It separates development and confirmatory data by domain and capture, then reports confirmation on new domains, transfer to proxies held out from supervised fitting, and evaluation across captures.

## III. THREAT MODEL AND PROTOCOL ANALYSIS

This section defines the passive observation setting and ToP label, analyzes how proxy encapsulation transforms observable traffic, and specifies the cross-proxy protocol audit used to test the resulting hypotheses.

## A. Observation and Label Definition

The ToP path consists of the client, an outer proxy server, and the Tor network. A passive observer between the client and proxy sees only the encrypted TCP connection on this hop and cannot access Tor communication beyond the proxy.

After bidirectional flow construction, a flow with n payload packets is represented as:

$$
x = \{(d _ {i}, \ell_ {i}, \Delta t _ {i}) \} _ {i = 1} ^ {n},\tag{1}
$$

where $d _ { i } \in \{ - 1 , + 1 \}$ is the direction of packet i relative to the client, $\ell _ { i }$ is its TCP payload length, and $\Delta t _ { i }$ is its interarrival interval, with $\Delta t _ { 1 } = 0$ . Let X denote this observable flow space. The class $c ( x )$ is ToP, Pure Proxy, Direct Tor, or Ordinary according to the presence of an outer proxy and Tor traffic. Pure Proxy and Direct Tor isolate the two conditions, and Ordinary satisfies neither. We define $s _ { \mathrm { P } } ( x ) = 1$ for ToP and Pure Proxy and 0 otherwise, and $s _ { \mathrm { T } } ( x ) = 1$ for ToP and Direct Tor and 0 otherwise. The ToP label is:

$$
y (x) = s _ {\mathrm{P}} (x) \wedge s _ {\mathrm{T}} (x).\tag{2}
$$

This conjunction provides the basis for the factorized detector in Section IV.

The observer uses direction, payload length, and relative timing from standard Tor and proxy implementations. Addresses and ports support capture filtering, bidirectional flow construction, data grouping, and integrity checks, but do not enter the model. Domains, filenames, absolute timestamps, flow and capture identifiers, proxy labels, SNI strings, handshake hashes, and payload content are also excluded. The observer cannot decrypt proxy payloads, read encapsulated Tor fields, interact with endpoints, or correlate multiple observation points. The method requires neither active probing nor cooperation from the proxy server. Section V-E3 separately evaluates controlled packet transformations.

ToP and Pure Proxy use the same browser, request generator, domain distribution, collection software, and preprocessing pipeline, although individual flows are not paired by request or collection time. Splits disjoint by domain and capture control shared endpoint and acquisition identifiers, and later captures measure temporal variation in Section VI.

## B. Proxy Transformation and Observable Hypotheses

Tor maps upper-layer activity u to a structured byte stream through channel negotiation, circuit construction, data scheduling, and flow control [1]. Proxy protocol p then applies authentication, encryption, framing, buffering, and transport adaptation before the stream encounters implementation and network effects. The observed flow is:

$$
x = \mathcal {O} (\mathcal {N} _ {e} (\mathcal {P} _ {p} (\mathcal {G} _ {\mathrm{Tor}} (u))))  ,\tag{3}
$$

where $\mathcal { G } _ { \mathrm { T o r } }$ generates the Tor stream, ${ \mathcal P _ { p } }$ represents the outer proxy, $\mathcal { N } _ { e }$ captures implementation and network effects, and $\mathcal { O }$ extracts direction, payload length, and relative timing. The protocol $p$ is Shadowsocks, Trojan, VMess, or VLESS.

These proxies expose different transformation paths. Shadowsocks uses authenticated encryption [32], Trojan carries requests and data over TLS [33], VMess uses protocol-specific authentication and chunking [34], and VLESS uses a simpler request structure with configurable transport [35]. Figure 2 summarizes these differences.

![](images/3f861afb1f5bded2cd58e2b7be371928ce0a99c4ce2067f0df7882745feaab3f.jpg)  
Fig. 2. Proxy processing paths for Tor traffic.

Proxy processing, TCP coalescence, network segmentation, congestion control, and retransmission create a many-to-many relation between inner cells and observed packets. Several cells may contribute to one packet, and one cell may span several packets. This transformation yields two testable hypotheses. Approximate cell-length regularities may remain in cumulative payload sequences, while interaction order, relative connection evolution, and relationships between bursts and responses may remain consistent across proxies.

## C. Cross-Proxy Protocol Audit

We define the protocol-guided scalar candidate family as:

$$
\mathcal {R} = \{r _ {j}: \mathcal {X} \to \mathbb {R} \} _ {j = 1} ^ {J}.\tag{4}
$$

Here, J denotes the number of candidates, and we set $J = 1 4 7$ . Each candidate uses direction, payload length, and relative timing from the first 128 payload packets. The four groups measure early directional interaction, multi-resolution dynamics, coupling between bursts and responses, and soft cell lattice structure. Their definitions were fixed before inspection of the confirmatory set. Appendix A summarizes the candidate families and audit criteria.

Consistency across proxies is the screening criterion. For candidate $r _ { j }$ and proxy $p ,$ its AUC for separating ToP from Pure Proxy is:

$$
A _ {j, p} = \operatorname{AUC} \left(r _ {j} (x), \mathbb {I} [ c (x) = \mathrm{ToP} ] \mid p\right).\tag{5}
$$

![](images/728c238898455058af44765e08628fe3e460e1c2ee7cc660c93668477223404e.jpg)  
Fig. 3. Overview of NESTTOR. Inputs cover ToP, Pure Proxy, Ordinary, and Direct Tor flows. (A) Preprocessing converts a bidirectional TCP flow into a sequence of payload packets and removes prohibited identifiers and labels. (B) Representation extracts global flow behavior, dynamics across relative stages, and optional protocol residuals. (C) Factorized detection combines a proxy gate with a proxy-conditioned Tor detector. (D) Calibration using Pure Proxy references sets the inner threshold from the upper-tail quantile of Pure Proxy reference scores when ToP labels are unavailable, while selection based on the capture environment chooses a frozen proxy gate.

Each candidate determines one discrimination direction and uses it on all four proxies. It passes screening when the direction is consistent, the worst directed AUC on the three development proxies and VLESS exceeds 0.58, and every pairwise AUC deviation from chance for proxy identification is below 0.05. A permutation test additionally requires evidence of discrimination across the candidate set at a familywise significance level of 0.05, as defined in Appendix A.

The audit includes VLESS labels, so VLESS is held out from supervised fitting and source-domain threshold selection rather than from protocol analysis. The primary stage-based representation precedes label-guided candidate selection. The secondary protocol-guided variant selects features anew from the same 147 candidates using only the training proxies, as described in Section IV.

## IV. NESTTOR METHODOLOGY

fiToP requires both the outer proxy condition and the Tor presence condition in Equation (2). NESTTOR assigns them to a proxy gate and a proxy-conditioned Tor detector, trains the two classifiers separately, and combines their decisions with an AND rule.

The transformation model in Section III motivates features that describe interaction order and relative connection evolution without relying on packet-to-cell alignment. NESTTOR uses a stage-based representation of fixed dimension for this purpose. Figure 3 summarizes flow preprocessing, stage-based features, factorized detection, and optional calibration for proxies held out from supervised training.

## A. Stage-Based Flow Features

The stage-based representation summarizes how bidirectional interaction evolves over the relative lifetime of a flow. It does not reconstruct Tor cells from transformed outer packets. The input to NESTTOR is the single bidirectional TCP flow $x = \{ ( d _ { i } , \ell _ { i } , \Delta t _ { i } ) \} _ { i = 1 } ^ { n }$ defined in Equation (1). All features are constructed within one flow and exclude payload content, endpoint identifiers, proxy type, and neighboring connections.

1) Flow-level Behavior: We first construct a base flow behavior representation as:

$$
\phi_ {\mathrm{base}} (x) \in \mathbb {R} ^ {d _ {\mathrm{base}}}.\tag{6}
$$

Here, $d _ { \mathrm { b a s e } }$ denotes the dimension of the base representation, and we set $d _ { \mathrm { b a s e } } ~ = ~ 6 2$ . The resulting vector summarizes traffic volume and distribution (bidirectional packet counts, payload bytes, duration, rate, and upstream to downstream ratio), packet length and timing statistics (means, dispersion, extremes, and quantiles), direction dynamics (switch counts, lengths of contiguous runs in the same direction, and adjacent direction patterns), and behavior relating bursts and responses (volume and duration of contiguous bursts in the same direction and their relationship with subsequent responses in the reverse direction). We define the burst sequence as:

$$
\mathcal {B} (x) = \{B _ {k} \} _ {k = 1} ^ {K},\tag{7}
$$

where $B ( x )$ is the sequence of all maximal contiguous subsequences of packets with the same direction in x. Here, K is the number of bursts and $B _ { k }$ is the k-th burst. For each burst we record its direction $D _ { k }$ , packet count $N _ { k }$ , cumulative payload $L _ { k }$ , duration $T _ { k }$ , and the gap $G _ { k }$ from its end to the next response in the reverse direction. Summaries of response gaps use only bursts followed by such a response. Aggregation at the burst level represents sustained transmission beyond packet boundaries and reduces sensitivity to TCP segmentation.

2) Relative Stage Modeling: Global statistics pool the complete connection and compress temporal evolution into a single summary. A relative lifecycle coordinate preserves coarse changes across flows with different packet counts and durations. We partition connection stages by the relative position of payload packets. The normalized position of the i-th payload packet is:

$$
u _ {i} = \frac {i - 1}{\max (n - 1 , 1)}.\tag{8}
$$

According to $u _ { i }$ , a flow is partitioned into three equal intervals:

$$
\begin{array}{l} \mathcal {I} _ {\mathrm{E}} = \{i \mid 0 \leq u _ {i} <   1 / 3 \}, \\ \mathcal {I} _ {\mathrm{M}} = \{i \mid 1 / 3 \leq u _ {i} <   2 / 3 \}, \\ \mathcal {I} _ {\mathrm{L}} = \{i \mid 2 / 3 \leq u _ {i} \leq 1 \}. \end{array}\tag{9}
$$

The normalized coordinate $u _ { i } \in [ 0 , 1 ]$ assigns each packet to the early, middle, or late index set. These intervals provide a lifecycle coordinate for connection behavior and allow comparison across flows with different durations and packet counts. They describe coarse connection evolution rather than protocol state boundaries.

For each stage $s \in \{ \mathrm { E } , \mathrm { M } , \mathrm { L } \}$ , we compute summaries specific to that stage over the corresponding packet subsequence, including direction distribution, payload length behavior, relative timing, and burst characteristics:

$$
\psi_ {s} (x) = g _ {s} \left(\{(d _ {i}, \ell_ {i}, \Delta t _ {i}) \mid i \in \mathcal {I} _ {s} \}\right).\tag{10}
$$

Here, $g _ { s }$ is the fixed summary mapping for stage s, and $\psi _ { s } ( x )$ is the resulting stage descriptor.

The stage summaries form a block of fixed dimension containing statistics within each stage and changes from the early stage to the late stage:

$$
\phi_ {\mathrm{dyn}} (x) = h \left(\psi_ {\mathrm{E}} (x), \psi_ {\mathrm{M}} (x), \psi_ {\mathrm{L}} (x)\right) \in \mathbb {R} ^ {d _ {\mathrm{dyn}}}.\tag{11}
$$

Here, $d _ { \mathrm { d y n } }$ denotes the dimension of the stage dynamics block, and we set $d _ { \mathrm { d y n } } = 3 7$ . The mapping $h ( \cdot )$ constructs this block from features within and across stages and computes earlyto-late differences for statistics defined in both stages. The complete stage-based representation is:

$$
\phi_ {\mathrm{stage}} (x) = [ \phi_ {\mathrm{base}} (x), \phi_ {\mathrm{dyn}} (x) ] \in \mathbb {R} ^ {d _ {\mathrm{stage}}}.\tag{12}
$$

Here, $d _ { \mathrm { s t a g e } }$ denotes the complete representation dimension, and we set $d _ { \mathrm { s t a g e } } ~ = ~ d _ { \mathrm { b a s e } } + d _ { \mathrm { d y n } } ~ = ~ 9 9$ . Because stage boundaries are determined by relative packet positions, ϕ<sub>stage</sub> does not depend on absolute time or collection date.

3) Protocol-Guided Feature Variant: The primary stagebased representation follows from the transformation model and is fixed independently of class labels. The protocol audit separately evaluates hypotheses about observable behavior.

The audit across four proxies retains 31 of 147 candidates for mechanism analysis. Detection models select from the same 147 candidates separately within each training fold, using only the training proxies. The confirmatory configuration selects 35 candidates from Shadowsocks, Trojan, and VMess and combines them with the 62 base features to form $\phi _ { \mathrm { r e s } } \in \mathbb { R } ^ { 9 7 }$

We independently evaluate $\phi _ { \mathrm { s t a g e } }$ as the primary representation and $\phi _ { \mathrm { r e s } }$ as a protocol-guided variant.

## B. Factorized Detection

The factorized detector assigns one condition to each classifier. The two classifiers are fitted separately without shared parameters, encoders, or a joint loss, and interact only through the final AND rule.

1) Proxy Gate: The proxy gate $Q$ answers whether a flow belongs to a proxy path. Its supervision label $z _ { Q } ( x )$ is 1 for ToP and Pure Proxy flows and 0 for Ordinary and Direct Tor flows. The gate receives the stage-based representation and outputs a proxy evidence score as:

$$
q (x) = Q (\phi_ {\mathrm{stage}} (x)) \in [ 0, 1 ].\tag{13}
$$

The score $q ( x )$ estimates the presence of an outer proxy without requiring classification by proxy type.

2) Proxy-Conditioned Tor Detector: The proxy-conditioned Tor detector T learns the difference between ToP and Pure Proxy on samples that already satisfy the outer proxy condition. Its training label $z _ { T } ( x )$ is 1 for ToP flows and 0 for Pure Proxy flows. Training on ToP and Pure Proxy isolates behavioral variation associated with Tor behavior inside the proxy. Only flows that satisfy the outer proxy condition participate in the supervised training of T.

The detector is trained on the proxy-conditioned domain $\mathcal { X } _ { P } = \{ x : s _ { P } ( x ) = 1 \}$ and produces a score for each input flow. The final AND rule rejects flows whose proxy gate score is below $\tau _ { Q }$ . Direct Tor satisfies $s _ { T } ( x ) = 1$ but falls outside the training domain of T.

The primary method defines the inner score from the stagebased representation as:

$$
t _ {\mathrm{stage}} (x) = T _ {\mathrm{stage}} (\phi_ {\mathrm{stage}} (x)).\tag{14}
$$

The secondary protocol-guided variant is:

$$
t _ {\mathrm{res}} (x) = T _ {\mathrm{res}} (\phi_ {\mathrm{res}} (x)).\tag{15}
$$

When there is no need to distinguish the representation variant, both are denoted uniformly as:

$$
t (x) = T (\phi_ {T} (x)) \in [ 0, 1 ], \qquad \phi_ {T} \in \{\phi_ {\mathrm{stage}}, \phi_ {\mathrm{res}} \}.\tag{16}
$$

We use $\phi _ { T }$ and $t ( x )$ when reasoning applies to both.

3) AND Rule: Given a proxy gate threshold $\tau _ { Q }$ and a proxy-conditioned Tor threshold $\tau _ { T } .$ , the two decisions are:

$$
\widehat {z} _ {Q} (x) = \mathbb {I} [ q (x) \geq \tau_ {Q} ], \quad \widehat {z} _ {T} (x) = \mathbb {I} [ t (x) \geq \tau_ {T} ].\tag{17}
$$

The final prediction is the conjunction of threshold decisions:

$$
\widehat {y} (x) = \widehat {z} _ {Q} (x) \wedge \widehat {z} _ {T} (x).\tag{18}
$$

This conjunction implements the semantic decomposition of ToP. The component scores also localize errors to proxy recognition or discrimination of Tor behavior inside the proxy.

## C. Negative-Only Threshold Calibration

A proxy type held out from supervised training may exhibit different framing, buffering, and transport behavior, which can shift the proxy-conditioned detector’s score distribution. A disjoint Pure Proxy reference set characterizes negative scores for the target proxy without using target ToP labels. For a held-out proxy type $u ,$ calibration accesses only:

$$
\mathcal {R} _ {u} ^ {-} = \left\{x \mid c (x) = \mathrm{PureProxy}, p (x) = u \right\},\tag{19}
$$

which is mutually exclusive with the final evaluation set at the domain and capture levels. Here, $p ( x )$ returns the outer proxy type of flow $x .$ Given a target empirical false positive rate α on this reference set, the threshold is determined from the upper tail of Pure Proxy scores:

$$
\begin{array}{l} q _ {1 - \alpha} ^ {(u)} = \text {Quantile} _ {1 - \alpha} ^ {\text {higher}} \left(\{t (x): x \in \mathcal {R} _ {u} ^ {-} \}\right), \\ \tau_ {T} ^ {(u)} = \text {next} _ {+} \Big (q _ {1 - \alpha} ^ {(u)} \Big). \end{array}\tag{20}
$$

Here, $q _ { 1 - \alpha } ^ { ( u ) }$ is the empirical $( 1 - \alpha )$ quantile in the upper tail of the Pure Proxy score distribution, and $\operatorname { n e x t } _ { + } ( q )$ denotes the smallest representable number strictly greater than $q .$ Setting $\tau _ { T } ^ { ( u ) }$ immediately above the quantile controls the false-positive rate on the reference set.

Threshold calibration accommodates shifts in score location or scale without changing score ordering. Its benefit therefore depends on the remaining separation between ToP and Pure Proxy. Changes in MTU or MSS, TCP segmentation, capture offloading, or proxy buffering can alter packet boundaries and the length, burst, and stage statistics used for discrimination. The Pure Proxy reference calibrates $\tau _ { T }$ , while the proxy gate retains its source threshold.

## D. Gate Selection for Known Capture Environments

Capture environments can shift packet length, timing, and burst statistics, thereby changing the decision boundary between proxy and nonproxy traffic. For a known finite set of environments, an optional selector uses an unlabeled traffic window to choose among prebuilt proxy gates.

Let two known capture environments be $e ~ \in ~ \{ a , b \}$ , for which gates $Q ^ { ( a ) }$ and $Q ^ { ( b ) }$ share the same proxy versus nonproxy label. The system forms an environment profile from an independent unlabeled traffic window $\begin{array} { r } { \mathcal { C } = \{ x _ { j } \} _ { j = { \frac { M } { \cdot } } } ^ { M } \mathrm { . } } \end{array}$ <sub>1</sub> using a profiler H, where M is the number of flows in the window. The profiling window contains $M = 8 0 0$ unlabeled flows. It then selects one gate for that deployment window. The detector $T ,$ its threshold $\tau _ { T }$ , and the AND rule remain fixed.

We balance profiler training by environment and traffic class to control differences in class proportions. A future extension could update profiles over successive 800-flow windows and select a gate when both confidence in the mean score and compatibility with a reference distribution support the same known environment, otherwise abstaining for recalibration. This extension would retain the fixed Tor detector and threshold. The evaluated selector covers two known environments.

## E. Training and Inference

We select both Histogram Gradient Boosting (HGB) models and their thresholds using the development training and validation data. We keep them fixed during confirmatory inference. We complete optional calibration (Section IV-C) and gate selection (Section IV-D) before classifying target flows. The system accepts a flow as ToP when both scores cross their fixed thresholds.

## V. EXPERIMENTAL SETUP

This section defines the evidence needed to evaluate NEST-TOR. We first establish a leakage-controlled benchmark and a common comparison protocol. The experiments progress from identifying cross-proxy behavioral signals to measuring detection effectiveness, isolating system contributions and operational profile, and determining its generalization boundary.

## A. Benchmark and Evaluation Protocol

The NESTTOR Benchmark presented in this work covers four semantic classes (ToP, Pure Proxy, Ordinary, and Direct Tor) and four proxy protocols (Shadowsocks, Trojan, VMess, and VLESS). It contains 349,891 deduplicated bidirectional TCP flows from 1,663 verifiable domains. The class composition is 86,889 ToP, 39,516 Pure Proxy, 191,769 Ordinary, and 31,717 Direct Tor flows. The ToP class contains 27,915 Shadowsocks, 23,598 Trojan, 15,714 VMess, and 19,662 VLESS flows. The corresponding Pure Proxy counts are 10,827, 9,639, 3,541, and 15,509. We collected traffic in separate campaigns between January 2025 and July 2026, spanning approximately 18 months. Appendix A specifies the protocol audit statistics and preprocessing controls. The artifact includes manifests, class counts, and partitioning procedures. Appendix D gives the Current/Later class and proxy counts and separately defines the historical source pool and environment-comparison subsets.

1) Data Collection and Ethical Considerations: We generated the benchmark traffic in a controlled container environment. The browser component of Tor Browser ran inside the container, with Tor circuit establishment configured through torrc. Clash Verge and V2Ray provided the outer proxy paths. Software and protocol versions remained unchanged across all campaigns. We did not capture traffic from other users, private communication, or personal data.

Tor and the proxy software used local service ports 9050 and 20170, respectively. We scoped pcap capture to the experimental container and its designated virtual network interface.

Separate runs configured the four paths in Figure 1. Within Current and, separately, Later, ToP and Pure Proxy were collected concurrently in the same campaign under the same conditions, with only the protocol configuration changed. The active software and path configuration supplied the labels defined in Section III. Traffic class and proxy type are known during collection and retained as experimental metadata. Each experimental stage accesses only the labels permitted by its protocol. These labels are excluded from the flow feature vectors. For calibration by proxy type, the collection configuration identifies the applicable reference set and threshold.

TABLE I COMPARED METHODS.

<table><tr><td>Method</td><td>Input</td><td>Backbone</td></tr><tr><td>FS-Net [26]</td><td>Directional length sequence</td><td>Bi-RNN encoder-decoder</td></tr><tr><td>ET-BERT [27]</td><td>Header-free bigrams</td><td>Pretrained Transformer</td></tr><tr><td>YaTC [28]</td><td>Traffic images</td><td>MAE-pretrained ViT</td></tr><tr><td>NetMamba [29]</td><td>Byte allocation and strides</td><td>Unidirectional Mamba</td></tr><tr><td>TrafficFormer [30]</td><td>Bigram tokens</td><td>Transformer</td></tr><tr><td>NESTTOR</td><td>Stage features</td><td>Two HGB classifiers</td></tr><tr><td>– proxy gate Q</td><td> $\phi_{stage}$ </td><td>HGB</td></tr><tr><td>– inner detector T</td><td> $\phi_{stage}$  or  $\phi_{res}$ </td><td>HGB</td></tr></table>

We reconstructed bidirectional TCP flows from pcap files, removed duplicate sequences, and retained at most five flows from each capture. Addresses and ports supported filtering, flow construction, grouping, and integrity checks only.

The model uses only direction, payload length, and relative packet interval. We exclude addresses, ports, domains, absolute timestamps, and all collection identifiers. We split the data first by domain and then by capture, with no domain or capture shared across training, validation, and evaluation partitions.

The development data are partitioned for model fitting, threshold selection, closed-set testing, and protocol diagnosis. VLESS does not participate in supervised model fitting or source-domain threshold selection. Its labels enter the protocol audit, while a disjoint Pure Proxy subset supports targetdomain threshold calibration. Confirmatory class labels are used only for evaluation. The confirmatory set covers 125 new domains from the same collection environment with no overlap at either the domain or capture level. Model fitting and source-threshold selection used development data, followed by calibration on an independent Pure Proxy reference set, after which the models, thresholds, and analysis rules were fixed before confirmatory evaluation. This set mixes the four classes from separate controlled runs, with class proportions chosen for evaluation rather than operational ToP prevalence. We report feature ablation, structural controls, robustness tests, and native end-to-end evaluation.

## B. Compared Methods

The compared methods span five external classifiers and NESTTOR, as summarized in Table I. FS-Net, ET-BERT, and YaTC cover models using packet length sequences, byte tokens, and traffic images in the shared-gate analysis. NetMamba and TrafficFormer extend the native end-to-end comparison to recent state-space and pretrained Transformer traffic classifiers. RNN, MAE, and ViT in the table denote recurrent neural network, masked autoencoder, and vision Transformer. All native models use the same sample manifest, labels, and partitions, while their inputs follow the interfaces defined by the original methods. NetMamba uses its original byte allocation and stride sequence. TrafficFormer uses bigram tokenization after address and port fields are removed. Appendix B reports the selected NESTTOR configurations.

Controlled baselines include coarse statistics, base flow behavior, flat Random Forest and HGB classifiers, singlecondition classifiers, and a shared multi-task model. Each isolates a question about the representation or decision structure under matched data and training budgets.

## C. Protocol-Guided Audit

Proxy encapsulation removes a stable correspondence between observed packets and individual Tor cells. The transformation analysis in Section III nevertheless suggests that higher-level interaction order, connection evolution, and relationships between bursts and responses may survive across different proxies. Before evaluating the detector, we therefore ask whether these behaviors are consistently observable.

RQ1. What Tor behaviors remain consistently observable across proxies after encrypted proxy encapsulation?

To answer RQ1, we audit 147 candidate statistics on the development data using the screening criteria in Section III. They span early directional interaction, dynamics at multiple resolutions, coupling between burst volume and response interval, and soft cell lattice. Candidate screening requires the directed AUC on every proxy to exceed a prespecified threshold of 0.58, separately from classifier decision thresholds. We report sensitivity at 0.55 and 0.60 using the same strict inequality. We test direction consistency and proxy identity leakage and control multiple comparisons across the candidate set through label permutation within each development proxy. Candidate generation, screening, and threshold selection use development data only.

## D. Core Performance Evaluation

The protocol audit can establish that behavioral signals remain observable, but it does not show whether they support reliable ToP decisions. Moreover, the composite ToP label requires evaluation both within proxy traffic and as a complete end-to-end task under controls against identifier shortcuts.

RQ2. How effective is leakage-controlled ToP detection?

The primary evaluation metric is macro-F1, defined as the arithmetic mean of the F1 scores of the two classes, ToP and Non-ToP. We also report the true-positive rate (TPR) for ToP and false-positive rate (FPR) for individual Non-ToP classes.

1) Confirmatory Evaluation with a Shared Gate: The confirmatory comparison connects the proxy-conditioned detectors of NESTTOR, FS-Net, ET-BERT, and YaTC to the same proxy gate. Each method uses the model snapshot and threshold fixed during development. The final prediction is:

$$
\widehat {y} (x) = \mathbb {I} [ q (x) \geq \tau_ {Q} ] \wedge \mathbb {I} [ t _ {m} (x) \geq \tau_ {m} ],\tag{21}
$$

where $t _ { m }$ and $\tau _ { m }$ are the proxy-conditioned score and threshold of method $m .$ Equation (21) applies the same proxy gate score q and threshold $\tau _ { Q }$ to every compared detector. This setting isolates discrimination between ToP and Pure Proxy under a common decision about outer proxy presence.

2) Native End-to-End Evaluation: Each native baseline directly learns the binary label $y ( x ) = \mathbb { I } [ c ( x ) = \mathrm { T o P } ]$ on the common training and validation partitions. NESTTOR retains its factorized detector and selected thresholds. On VLESS, every method calibrates its threshold using only a disjoint Pure Proxy reference set without accessing VLESS ToP labels.

## E. Structural Analysis

Detection accuracy alone cannot establish whether the observed performance follows from the proposed representation and factorized decision structure, nor can it characterize behavior under packet transformations and resource constraints. We therefore isolate the relevant design choices and measure the resulting operational profile.

RQ3. Which design choices drive NESTTOR’s performance, robustness, and efficiency?

1) Feature Ablation: Feature ablation fixes the proxy gate, data splits, model type, and threshold rule, varying only the proxy-conditioned input. The sequence from Coarse Only to Base Flow and Base + Stage separates the contributions of global scale, interaction statistics, and relative lifecycle modeling. Five settings are compared. Coarse Only uses packet count, byte count, duration, rate, and direction ratio. Base Flow uses 62 base features. Base + Stage uses the 99- dimensional stage-based representation. Base + Residual is the protocol-guided variant that adds audited candidates to the base features. Stage without Coarse Statistics removes coarse statistics from the stage-based representation. These settings use models fitted for the feature ablation, separately from the models frozen for confirmatory evaluation.

2) Factorized Decision Control: Five structures are compared under the same 99-dimensional input and total tree budget. This experiment isolates decision structure within a common Random Forest implementation. Flat Binary directly learns ToP versus all Non-ToP. Inner Only is the proxyconditioned ToP versus Pure Proxy classifier. Gate Only distinguishes proxy from nonproxy traffic. Shared Multi-task jointly predicts the two conditions with a shared representation. Independent Gate + Inner is the factorized configuration with two classifiers followed by the AND rule. The single and shared variants use 400 trees. Each classifier in Independent Gate + Inner uses 200 trees. Data partitions, class-weighting rules, threshold-selection procedures, and random seeds remain constant. Each classifier uses the training classes required by its objective and selects its thresholds on the common validation partition.

We also train a flat HGB classifier on the same 99- dimensional representation and partitions. It uses the primary system’s classifier family and threshold-selection protocol but learns ToP versus Non-ToP with one decision boundary. For VLESS, the flat HGB baseline also receives the same negativeonly calibration procedure as NESTTOR.

3) Robustness and Efficiency: For each perturbed condition in Figures 8 and 9(b), we compute each metric separately for five runs and report its arithmetic mean across those runs.

![](images/1b69cca59c76bb8549957e718e8476ecd3618ba66afb53f114e3bcad39081066.jpg)  
Fig. 4. Audit of candidate families across proxies. Candidates must have a directed AUC greater than $\tau = 0 . 5 8$ on every proxy and satisfy the remaining criteria in Section III.

The offline packet-level perturbation experiment covers four independent transformations and two combined conditions on the confirmatory set. Padding expands payload packets to the nearest bin in the 64–1448 byte range. Latency adds delay in sequence. Packet loss drops non-control TCP payload packets. Resegmentation caps a packet payload at 1024, 512, or 256 bytes. Medium and maximum combined conditions apply all transformations at medium or maximum strength. Inputs are re-extracted from derived pcap files. Models and thresholds do not change.

Random packet transformations use five seeds with models and thresholds fixed. Figure 8 presents the clean condition, four individual transformations, and the medium combined condition. These offline transformations preserve the original transport trace except for the specified operation.

Resource measurement uses the same server. NESTTOR is fixed to four CPU threads. The remaining methods run serially on the same GPU. Measured items include latency with a batch size of 1, throughput with a batch size of 64, peak resident memory, peak GPU memory, model file size, and end-to-end offline wall time. The latency and throughput measurements isolate model inference on preconstructed feature vectors. The complete offline wall time also includes pcap parsing, bidirectional flow reconstruction, and feature construction.

## F. Generalization Experiments

The domain-disjoint confirmatory evaluation still operates within the same collection environment as the development data. Changes in proxy implementation, capture period, and background composition can alter the observed traffic distribution, so in-distribution effectiveness does not establish transfer.

RQ4. Can NESTTOR generalize across distributions?

1) Proxy Type Holdout: To test transfer to proxies held out from supervised fitting, we remove the ToP and Pure Proxy flows of Shadowsocks, Trojan, and VMess in turn from model fitting and source-domain threshold selection, then evaluate on the target proxy. VLESS follows the same supervised holdout but participated in the preceding protocol audit. Strict Holdout uses thresholds selected on validation data from the source proxies. Negative-Only Calibration adjusts the proxyconditioned threshold using a disjoint Pure Proxy set, while target ToP labels are withheld from calibration. The two regimes measure transfer before and after calibration using target Pure Proxy references.

2) Extension with Later Captures: The later collection contains 80,923 ToP and Pure Proxy flows across all four proxies. Domain hash partitioning yields an evaluation set of 23,374 flows. We applied the frozen models and thresholds without using later capture labels for training, model selection, or threshold adjustment. The five external methods also use their fixed model snapshots and thresholds.

3) Open-World Background Evaluation: We further evaluate the fixed system on 11,131 heterogeneous background flows covering ordinary HTTPS, CDN traffic, bulk transfer, video, VPN, I2P, and JonDonym. The pool combines USTC-TFC 2016 [36], ISCX-VPN 2016 [37], and SJTU-AN21 [38] with HTTPS traffic collected after model selection. The confirmatory threshold has no access to these background flows. Confirmatory ToP flows provide the positive reference. We also summarize three descriptive operating points on the empirical score curve.

4) Gate Selection via Environment Profiling: This analysis changes only the outer gate. The proxy-conditioned detector and thresholds remain fixed. We compare three gate strategies across two known capture environments: the gate trained for the current environment, a fixed stable gate, and selection between gates dedicated to the two environments. The stable gate is a separate comparison strategy. The profiler uses only semantic groups common to both environments and balances samples by environment and semantic group. At inference, the mean score of an independent unlabeled calibration window selects one of the two dedicated gates. The complete window contains 800 flows. The size analysis samples 1, 2, 4, 8, and 16 complete capture clusters and retains all flows in each selected cluster. The realized number of flows therefore varies with cluster composition.

The primary NESTTOR confirmatory result uses one prespecified HGB run with seed 42 and partitions disjoint by domain and capture. We compute 95% percentile confidence intervals from 10,000 domain- or capture-cluster bootstrap resamples of fixed predictions, using domain clusters for later captures. These intervals quantify evaluation sampling uncertainty. A method-difference interval entirely above zero indicates a statistical advantage; an interval containing zero leaves the difference unresolved.

## VI. RESULTS AND DISCUSSION

This section answers the four research questions by analyzing observable protocol signals, detection effectiveness, contributions of the representation and decision structure, robustness and efficiency, and generalization across proxies, capture periods, and background traffic.

## RQ1: Observable Tor Behavior after Proxy Encapsulation

Section III introduced two protocol hypotheses represented by four candidate families. Figure 4 reports the audit of the candidate families at the selected minimum AUC threshold of 0.58. Of the 31 retained candidates, 20 come from early directional interaction, 7 from multi-resolution dynamics, and 4 from the coupling between contiguous bursts in the same direction and responses in the reverse direction. None of the soft cell lattice candidates constructed around fixed Tor cell scales passed.

TABLE II  
SENSITIVITY OF CANDIDATE SCREENING TO THE DIRECTED AUC THRESHOLD. THE DIRECTED AUC ON EVERY PROXY MUST STRICTLY EXCEED τ ; THE REMAINING AUDIT CRITERIA ARE UNCHANGED. THE SELECTED THRESHOLD IS SHOWN IN BOLD.

<table><tr><td>Directed AUC threshold τ</td><td>Retained candidates</td></tr><tr><td>0.55</td><td>34</td></tr><tr><td>0.58</td><td>31</td></tr><tr><td>0.60</td><td>30</td></tr></table>

Table II summarizes the sensitivity of candidate retention to the directed AUC threshold. The selected threshold of 0.58 lies within a region where the retained candidate count is stable. No soft cell lattice candidate passes at any evaluated threshold.

Across the four evaluated proxy implementations and the first 128 payload packets, the audit identifies interaction order, stage evolution, and coupling between bursts and responses as consistent behavioral signals. Approximate cell-length candidates do not meet the same cross-proxy screening criteria.

RQ2: Detection Effectiveness under Leakage-Controlled Evaluation

1) Confirmatory Evaluation: On 125 unseen domains, the shared-gate evaluation in Figure 5 (left) shows that NESTTOR achieves 99.45% macro-F1. NESTTOR-Residual, the protocolguided variant, reaches 99.40%. FS-Net is 0.05 percentage points above NESTTOR under the shared gate, while the 95% confidence interval of their difference, [−0.36, 0.46], includes zero. The corresponding margins over YaTC and ET-BERT are 2.92 and 13.55 percentage points.

Under a common proxy decision, NESTTOR and FS-Net show no statistically resolved difference in macro-F1. This evaluation measures transfer to new domains within the same collection environment.

2) Error Structure: The breakdown by class and proxy in Table III localizes the confirmatory errors. The evaluation contains 900 ToP, 1,000 Pure Proxy, 150 Ordinary, and 250 Direct Tor flows. The ToP detection rate of NESTTOR is 99.33%. Shadowsocks, Trojan, and VMess all reach 100%, while VLESS reaches 97.33%. On the background traffic side, 6 out of 1,000 Pure Proxy flows are misclassified as ToP (falsepositive rate 0.60%). All 150 Ordinary and 250 Direct Tor flows are correctly rejected.

Direct Tor produces no false positives in this evaluation, consistent with the proxy gate’s intended role. The six Pure Proxy false positives originate from the inner decision.

Applying the fixed source thresholds $\tau _ { Q } = 0 . 4 8 5$ and $\tau _ { T } =$ 0.225 to all 2,300 flows without proxy-type information yields 99.41% macro-F1 and a Pure Proxy FPR of 0.70%. ToP TPR remains 99.33%, with one additional Pure Proxy false positive.

![](images/f00281d97ed65fddaddc3403193c1bf05153268b30c4d711a597df6bf2246727.jpg)

![](images/db0a66a61910812e21f348c331f18d75da43c74d54f9f6a59c94095846dba1e5.jpg)  
Fig. 5. Confirmatory system comparison on the same 2,300-flow evaluation set. (a) Macro-F1 under a shared proxy gate. (b) Native end-to-end macro-F1. The plotted NESTTOR result uses proxy-conditioned inner thresholds. Applying $\tau _ { Q } = 0 . 4 8 5$ and $\tau _ { T } = 0 . 2 2 5$ uniformly gives 99.41% macro-F1 and 0.70% Pure Proxy FPR; Table III compares both rules.

TABLE III  
CONFIRMATORY RESULTS ON THE SAME 2,300 FLOWS. CLASS ROWS GIVE TPR FOR TOP AND FPR FOR NON-TOP, WITH ERROR COUNTS IN PARENTHESES. ALL METRICS ARE PERCENTAGES. ORIGINAL USES PROXY-CONDITIONED INNER THRESHOLDS; UNIFORM APPLIES $\tau _ { T } = 0 . 2 2 5$ TO EVERY FLOW. BOTH RULES USE $\tau _ { Q } = 0 . 4 8 5$

<table><tr><td>Class / metric</td><td>Original</td><td>Uniform</td></tr><tr><td>Macro-F1</td><td>99.45</td><td>99.41</td></tr><tr><td>ToP overall</td><td>99.33 (6)</td><td>99.33 (6)</td></tr><tr><td>ToP-Shadowsocks</td><td>100.00 (0)</td><td>100.00 (0)</td></tr><tr><td>ToP-Trojan</td><td>100.00 (0)</td><td>100.00 (0)</td></tr><tr><td>ToP-VMess</td><td>100.00 (0)</td><td>100.00 (0)</td></tr><tr><td>ToP-VLESS</td><td>97.33 (6)</td><td>97.33 (6)</td></tr><tr><td>Pure Proxy</td><td>0.60 (6)</td><td>0.70 (7)</td></tr><tr><td>Ordinary</td><td>0.00 (0)</td><td>0.00 (0)</td></tr><tr><td>Direct Tor</td><td>0.00 (0)</td><td>0.00 (0)</td></tr></table>

Appendix E reports the counts alongside the original proxyconditioned result.

3) Native End-to-End Evaluation: The native end-to-end comparison in Figure 5 (right) evaluates systems that learn the ToP label from the common development partitions. FS-Net, ET-BERT, and YaTC cover representative input paradigms used in the shared-gate analysis. NetMamba and TrafficFormer add recent state-space and pretrained Transformer models. All five methods complete training, validation, and closed-set testing before confirmatory inference.

FS-Net is the strongest external method at 87.46% macro-F1, 11.99 percentage points below NESTTOR. The remaining external methods score between 72.85% and 84.72%. This experiment measures performance of the complete systems across representative and recent traffic classifiers. The controls in RQ3 isolate the contribution of the decision structure.

## RQ3: Design Contributions, Robustness, and Efficiency

1) Controlled Structure Comparison: Under the same 99- dimensional input, Random Forest implementation, and 400- tree budget, Figure 6 compares five decision structures. Independent Gate + Inner reaches 94.12% macro-F1, compared with 86.67% for Flat Binary, 87.02% for Inner Only, 51.12% for Gate Only, and 88.11% for Shared Multi-task. This is 6.01 percentage points higher than Shared Multi-task. Because the input, training data, and tree budget are matched, this comparison isolates the effect of using separate decision boundaries for the two ToP conditions.

![](images/2b21c1dc2f960ae7486eb4a93803de31b04bcf18ac00e4a39b9dad8bc9f0f81f.jpg)  
Fig. 6. Ablation of the decision structure under matched inputs and model budgets.

The HGB comparison shows the same performance ordering. A flat HGB classifier using the 99-dimensional stagebased representation reaches 87.64% macro-F1, while the factorized HGB system reaches 99.45%. The difference is 11.81 percentage points. This comparison supports the factorized system within the same input representation and classifier family, complementing the Random Forest control with a matched total tree budget.

Three confirmatory flows illustrate these decisions. Flat HGB misses a VLESS ToP flow (score 0.0001, threshold 0.505), while NESTTOR detects it with gate and inner scores of 0.857 and 0.997, above thresholds of 0.485 and 0.875. On a VLESS Pure Proxy flow, flat HGB produces a false positive (0.856), while NESTTOR recognizes the proxy (0.993) and rejects Tor presence (0.319). A VMess Pure Proxy flow exposes a failure: gate and inner scores of 0.995 and 0.802 exceed their thresholds of 0.485 and 0.225, so both decisions admit a false positive.

![](images/864337ef1f6b93beaca5b56f827bd6fb0a11df35a844af00d978050c6ce2f1b0.jpg)  
Fig. 7. Feature ablation under matched model settings and a shared proxy gate. Bars report the macro-F1 difference relative to Base + Stage at 99.25%; positive values indicate improvement. The difference between Base + Stage and Coarse Only is +2.25 percentage points, with a 95% confidence interval of [1.55, 2.95].

2) Feature Ablation: Figure 7 compares the five diagnostic settings defined in Section V-E1. Coarse Only reaches 97.00%, Base Flow reaches 99.15%, Base + Stage reaches 99.25%, Base + Residual reaches 99.45%, and Stage without Coarse Statistics reaches 99.18%. Most of the 2.25-point gain over Coarse Only comes from the 62 base features, with relative stage features providing a smaller additional gain.

3) Packet-Level Sensitivity: Splitting payloads increases packet counts and alters length distributions, burst structure, and relative stage statistics. Under the 512-byte cap in Figure 8, macro-F1 falls by 28.0 points to 71.45%, ToP TPR decreases by 31.3 points, and Direct Tor FPR reaches 86.4%. Component scores attribute most ToP misses to the inner detector and Direct Tor false positives to the proxy gate. Adaptive resegmentation could affect the same statistics, with its impact depending on the strategy. Padding and delay primarily affect the proxy gate.

Across the six fixed methods, NESTTOR achieves the highest macro-F1 under 50% padding (96.65%), a delay of 50±10 ms (98.45%), 3% packet loss (99.25%), and the medium combined condition (80.95%). NetMamba, however, is strongest under 512-byte resegmentation at 83.56%, compared with 71.45% for NESTTOR.

4) Resource Cost: With preconstructed features and four CPU threads, mean and P95 inference latency at batch size 1 are 3.44 ms and 3.52 ms. Throughput reaches 18,031 flows per second at batch size 64, compared with 51.5 to 9,907.8 for the external methods. Peak memory is 445.6 MiB, and the model occupies 0.9 MiB, compared with 7.1 to 1,512.3 MiB for the external models. The complete offline pipeline processes 2,500 clean flows in 156 seconds, or 16.0 flows per second. Prediction takes 6.64 seconds (4.3%), while pcap parsing, flow reconstruction, and feature construction take 95.7%. This bottleneck motivates streaming parsing, incremental features, and parallel flow processing.

The detector uses complete flows. Prefixes of 16, 32, 64, 128, and 256 payload packets yielded lower performance.

TABLE IV  
MACRO-F1 UNDER SUPERVISED HOLDOUT OF EACH PROXY TYPE (%); SS DENOTES SHADOWSOCKS.

<table><tr><td>Method</td><td>SS</td><td>Trojan</td><td>VMess</td><td>VLESS</td></tr><tr><td>Stage</td><td>71.77</td><td>97.81</td><td>85.12</td><td>97.60</td></tr><tr><td>Residual</td><td>90.37</td><td>97.24</td><td>92.35</td><td>98.45</td></tr><tr><td>Residual + calib.</td><td>97.77</td><td>93.60</td><td>94.15</td><td>99.45</td></tr></table>

The offline measurements characterize processing after flow completion, with online service latency and throughput still to be evaluated.

## RQ4: Generalization beyond the Development Distribution

1) Proxy Type Holdout Results: Under supervised holdout of each proxy type, the results in Table IV exclude the target proxy from model fitting and source-domain threshold selection; the calibrated variant uses only a disjoint target Pure Proxy reference set. The stage-based representation achieves 71.77%, 97.81%, 85.12%, and 97.60% on Shadowsocks, Trojan, VMess, and VLESS. The protocol-guided variant reaches 90.37%, 97.24%, 92.35%, and 98.45%. For the VLESS fold, its 35 candidates are selected using only Shadowsocks, Trojan, and VMess training data.

Transfer depends on the proxy. Under strict holdout, the protocol-guided variant is higher on Shadowsocks, VMess, and VLESS, while the stage-based representation is slightly higher on Trojan. Negative-only calibration improves Shadowsocks, VMess, and VLESS but lowers performance on Trojan. Adjusting the threshold using Pure Proxy references therefore provides different benefits across proxies.

Shadowsocks is the weakest target under strict holdout. Trojan and VLESS transfer more strongly.

2) Evaluation on Later Captures: NESTTOR achieves 88.50% macro-F1 on the 23,374 later capture evaluation flows, with a 95% confidence interval from bootstrap resampling of domains of [87.85, 89.15]. The confirmatory result is 99.45%, which gives a difference of 10.95 percentage points between the two evaluations. The overall ToP detection rate is 86.50%, and the Pure Proxy false positive rate is 5.44%. Per proxy detection rates are 99.80%, 82.50%, 88.20%, and 89.10% for Shadowsocks, Trojan, VMess, and VLESS.

The two classifiers reveal distinct degradation patterns. On Shadowsocks, false positives from the inner detector on Pure Proxy form the main error source. On Trojan, the inner detector misses more ToP flows while the proxy gate remains stable. Proxy gate errors dominate on VMess and VLESS. Changes across captures therefore affect both classifiers, with the dominant error source varying by proxy.

On the fixed 1,000-flow subset in Figure 9, NESTTOR remains strongest under every condition. Its macro-F1 declines from 88.85% under clean conditions to 80.85% under the medium combined perturbation, while YaTC provides the strongest external perturbed result at 65.74%. The 512-byte resegmentation lowers NESTTOR macro-F1 by 4.00 points, and valid sample retention remains at least 99.88%.

![](images/952a95dd92f11f24facf33f0ffa6616e38785b0fd1388d5c2ac8922b556136aa.jpg)

![](images/125a36db0f639b6c6ee989ba899fd0c8a978d8874411c892febd5505f36227af.jpg)  
Fig. 8. Robustness to packet-level transformations on the confirmatory set. (a) Macro-F1 of the six frozen systems under clean and perturbed conditions. (b) NESTTOR’s macro-F1 loss and class-specific error changes, showing that resegmentation affects both ToP detection and Direct Tor rejection.

![](images/3236699efbcfc7cfde65c65fe002608daa43f7f2ef4c3dc1d48e559f54b5073a.jpg)

![](images/a54a18a700785a352a8c67e052aa7c4e776985962b7011a04f984df380448de1.jpg)  
Fig. 9. Evaluation on later captures. (a) Macro-F1 on the full 23,374-flow set. (b) Sensitivity to packet transformations on the fixed 1,000-flow subset.

TABLE V  
PERFORMANCE ON LATER CAPTURES (%).

<table><tr><td>Method</td><td>macro-F1</td><td>ToP TPR</td><td>Pure Proxy FPR</td></tr><tr><td>NESTTOR</td><td>88.50</td><td>86.50</td><td>5.44</td></tr><tr><td>FS-Net [26]</td><td>57.49</td><td>36.66</td><td>0.76</td></tr><tr><td>YaTC [28]</td><td>55.74</td><td>46.99</td><td>26.68</td></tr><tr><td>ET-BERT [27]</td><td>49.17</td><td>37.01</td><td>27.08</td></tr><tr><td>NetMamba [29]</td><td>54.71</td><td>47.95</td><td>31.15</td></tr><tr><td>TrafficFormer [30]</td><td>49.61</td><td>37.38</td><td>26.51</td></tr></table>

Table V compares six methods on later captures. NESTTOR reaches 88.50% macro-F1, 31.01 points above the strongest baseline, FS-Net.

3) Open-World Background Evaluation: On heterogeneous background traffic, Table VI reports the tradeoff between false positives and sensitivity. Its Confirmatory row applies the fixed proxy and inner thresholds jointly through Equation (18). It retains 99.33% ToP TPR and produces 350 false positives, while the three descriptive operating points reduce false positives with lower ToP sensitivity.

TABLE VI  
PERFORMANCE ON 11,131 OPEN-WORLD BACKGROUND FLOWS.

<table><tr><td>Point</td><td>FP</td><td>FPR (%)</td><td>ToP TPR (%)</td></tr><tr><td>Confirmatory</td><td>350</td><td>3.14</td><td>99.33</td></tr><tr><td>≈1% FPR</td><td>110</td><td>0.99</td><td>94.44</td></tr><tr><td>≈0.1% FPR</td><td>11</td><td>0.10</td><td>86.22</td></tr><tr><td>≈0.01% FPR</td><td>1</td><td>0.01</td><td>72.33</td></tr></table>

All 11,131 background flows use the fixed proxy-gate threshold $\tau _ { Q } ~ = ~ 0 . 4 8 5$ and inner-detector threshold $\tau _ { T } =$ 0.225, without selecting thresholds by proxy type. The same threshold pair detects 894 of the 900 confirmatory ToP reference flows, giving the reported 99.33% TPR.

TABLE VII  
SYSTEM MACRO-F1 (%) WITH DIFFERENT PROXY GATES ACROSS CAPTURE ENVIRONMENTS. A DASH INDICATES THAT THE STABLE GATE WAS NOT EVALUATED ON THE CONFIRMATORY SET.

<table><tr><td>Gate Strategy</td><td>Current</td><td>Earlier</td><td>VLESS</td><td>Confirm.</td><td>Mean</td></tr><tr><td>Current gate</td><td>98.17</td><td>11.77</td><td>96.93</td><td>99.45</td><td>54.97</td></tr><tr><td>Stable gate</td><td>87.97</td><td>92.87</td><td>48.97</td><td>-</td><td>90.42</td></tr><tr><td>Profile routing</td><td>98.17</td><td>93.37</td><td>96.93</td><td>99.45</td><td>95.77</td></tr></table>

The remaining rows and the precision-recall curve use the continuous score $s ( x ) = q ( x ) t ( x ) \mathrm { { : } }$ ; these descriptive points are obtained by varying a threshold on $s ( x )$ , while the Confirmatory row retains the fixed AND decision.

With equal aggregate weight assigned to ToP and background samples, the precision-recall curve has an area (PR-AUC) of 0.9812. Appendix C reports class-specific FPRs, ranging from 1.25% for CDN traffic to 4.50% for VPN traffic.

4) Gate Selection across Two Known Environments: The two capture environments require different proxy-gate boundaries. A stable gate improves the earlier environment but lowers performance in the current environment and on VLESS. Unlabeled calibration selects dedicated gates, improving performance across environments.

Across two known capture environments, Table VII compares the three gate strategies. The selector achieves 98.17%, 93.37%, and 96.93% on the current environment, the earlier environment, and VLESS. It maintains 99.45% on the confirmatory set. Equal weighting of the two capture environments gives 95.77% macro-F1, compared with 54.97% for the gate trained for the current environment. The selector chooses the correct gate in every cluster resampling trial described in Section V-F4.

Selecting the corresponding gate recovers performance across these two known environments while keeping the Tor detector fixed.

RQ1 supports the contribution on observable behavior through interaction signals across four proxies. RQ2 and RQ3 support factorized detection on unseen domains and under matched structural controls, while identifying sensitivity to resegmentation. RQ4 supports the longitudinal contribution through an advantage on later captures, with transfer varying by proxy and capture environment.

## E. Scope and Deployment Implications

NESTTOR supports passive screening of complete flows with an offline processing pipeline. Heterogeneous traffic requires independent calibration of background operating points. Environment routing requires a known environment and an independent unlabeled window. The longitudinal results describe transfer between discrete collection campaigns.

## VII. CONCLUSION

We identify directional interaction, relative connection evolution, and coupling between bursts and responses as informative Tor signals across four encrypted proxies. NESTTOR uses separate proxy and Tor decisions to reach 99.45% macro-F1 on unseen domains, exceeding matched flat HGB by 11.81 percentage points, with sensitivity to resegmentation. The longitudinal benchmark separates domains and captures across evaluations. On later captures, NESTTOR reaches 88.50% macro-F1, 31.01 points above the strongest external baseline. Component scores distinguish errors in proxy recognition from errors in Tor discrimination, explaining how transfer varies across the evaluated proxies and environments.

## ACKNOWLEDGMENT

This work is supported by the National Key Research and Development Program of China (Grant No. 2023YFB3106600) and the National Natural Science Foundation of China (Grant No. 62472296).

## APPENDIX A

## PROTOCOL AUDIT AND BENCHMARK DETAILS

The audit uses 100,000 permutations of ToP and Pure Proxy labels within each development proxy. The test statistic is the maximum, over all candidates, of each candidate’s minimum directed AUC across the three development proxies; orientation is recomputed in each permutation. The corrected permutation p-value must be below 0.05, controlling multiple comparisons across the candidate set. Candidate screening requires the directed AUC on each proxy to be strictly greater than the specified threshold. Implementation details are provided in the public repository.

Proxy identity leakage of candidate $r _ { j }$ is measured as the maximum pairwise AUC deviation from chance across all proxy type pairs:

$$
L _ {j} = \max _ {p \neq p ^ {\prime}} | \mathrm{AUC} (r _ {j} (x), \mathbb {I} [ P = p ] \mid P \in \{p, p ^ {\prime} \}) - 0. 5 |.\tag{22}
$$

Specifically, here, P denotes proxy type and $p , p ^ { \prime } \in \quad$ {SS, Trojan, VMess, VLESS}. A candidate passes the leakage criterion when $L _ { j } < 0 . 0 5$

The audit evaluates 147 prespecified candidates from four families: early directional interaction; packet-, burst-, and stage-scale dynamics; burst-response coupling; and soft cell lattice measures near 498, 509, 512, and 514 bytes. All candidates use the first 128 payload packets and were fixed before inspection of the confirmatory set.

Flows are deduplicated bidirectional TCP payload sequences, with at most five retained per capture. Samples are processed independently without pairing by domain or collection time. Addresses, ports, domains, absolute timestamps, filenames, and high-cardinality handshake hashes are excluded from model inputs.

## APPENDIX B

## MODEL AND CALIBRATION DETAILS

The 37-dimensional stage block contains statistics computed within the early, middle, and late stages, together with selected early-to-late differences. Concatenating this block with 62 base features forms the 99-dimensional stage-based representation.

The proxy gate uses 99 features, a learning rate of 0.03, at most 7 leaves per tree, and an $L _ { 2 }$ coefficient of 3. The stagebased and protocol-guided conditioned detectors use 99 and 97

CLASS AND PROXY COMPOSITION OF CURRENT AND LATER. SS DENOTES SHADOWSOCKS; ZEROS INDICATE ABSENT COMBINATIONS.

features, respectively. Both use a learning rate of 0.07, at most 7 leaves, and an $L _ { 2 }$ coefficient of 1. The learning rate controls shrinkage at each boosting iteration, the leaf limit bounds tree complexity, and $L _ { 2 }$ regularizes leaf weights.

Negative-only calibration uses $\alpha = 0 . 0 1$ , selected before inspecting target evaluation labels. The implementation takes the empirical 99% quantile of Pure Proxy reference scores using the higher rule and moves the threshold to the smallest representable number strictly greater than that quantile.

The VLESS reference and evaluation sets are disjoint by domain and capture. Calibration uses only Pure Proxy reference scores, does not access VLESS ToP labels, and does not retrain the model. The released manifest reports the complete partition and class counts.

## APPENDIX C

## HETEROGENEOUS BACKGROUND BREAKDOWN

The heterogeneous background evaluation contains 11,131 valid bidirectional TCP flows. At the confirmatory threshold, 350 flows are classified as ToP, corresponding to an overall FPR of 3.14%. Table VIII reports the FPR for each background category.

TABLE VIII  
FALSE POSITIVE RATES ON HETEROGENEOUS BACKGROUND TRAFFIC.

<table><tr><td>Background category</td><td>FPR (%)</td></tr><tr><td>Ordinary HTTPS</td><td>4.12</td></tr><tr><td>Bulk transfer</td><td>2.85</td></tr><tr><td>I2P and JonDonym</td><td>3.11</td></tr><tr><td>Video</td><td>1.50</td></tr><tr><td>CDN</td><td>1.25</td></tr><tr><td>VPN</td><td>4.50</td></tr></table>

The PR-AUC is 0.9812 when ToP and background samples receive equal aggregate weight.

## APPENDIX D

COLLECTION GROUPS AND EVALUATION ENVIRONMENTS

Table IX gives the class/proxy counts for Current and Later, two separate campaigns with concurrently collected ToP and Pure Proxy.

The historical Earlier pool contains 221,216 flows: 183,798 Ordinary, 20,050 Direct Tor, and 17,368 ToP (5,951 SS, 5,297 Trojan, and 6,120 VMess), with no Pure Proxy or VLESS. Including Current and Later gives 349,891 flows. Earlier includes publicly released January 2025 traffic and other pre-June captures consolidated under the post-merge June–July 2025 reporting label; this label does not date every flow.

In Table VII, Earlier and Current identify the environmentcomparison subsets collected in June–July 2025 and May 2026, containing 1,000 and 800 evaluation flows, respectively. The Earlier subset is distinct from the full aggregate earlier group. The later extension is a separate snapshot frozen in July 2026. These subset definitions preserve the benchmark’s January 2025–July 2026 collection span.

TABLE IX

<table><tr><td>Class/proxy</td><td>Current</td><td>Later</td></tr><tr><td>ToP-SS</td><td>2,217</td><td>19,747</td></tr><tr><td>ToP-Trojan</td><td>2,215</td><td>16,086</td></tr><tr><td>ToP-VMess</td><td>8,803</td><td>791</td></tr><tr><td>ToP-VLESS</td><td>2,340</td><td>17,322</td></tr><tr><td>Pure Proxy-SS</td><td>1,225</td><td>9,602</td></tr><tr><td>Pure Proxy-Trojan</td><td>2,329</td><td>7,310</td></tr><tr><td>Pure Proxy-VMess</td><td>2,311</td><td>1,230</td></tr><tr><td>Pure Proxy-VLESS</td><td>6,674</td><td>8,835</td></tr><tr><td>Ordinary</td><td>7,971</td><td>0</td></tr><tr><td>Direct Tor</td><td>11,667</td><td>0</td></tr><tr><td>Total</td><td>47,752</td><td>80,923</td></tr></table>

TABLE X

ORIGINAL AND UNIFORM-THRESHOLD RESULTS ON THE SAME 2,300 FLOWS. PP DENOTES PURE PROXY; METRICS ARE PERCENTAGES.

<table><tr><td>Rule</td><td>TP/FN</td><td>FP/TN</td><td>Macro-F1</td><td>PP FPR</td></tr><tr><td>Original</td><td>894/6</td><td>6/1,394</td><td>99.45</td><td>0.60</td></tr><tr><td>Uniform</td><td>894/6</td><td>7/1,393</td><td>99.41</td><td>0.70</td></tr></table>

## APPENDIX E

## UNIFORM-THRESHOLD CONTROL

The supplementary control applies $\tau _ { Q } = 0 . 4 8 5$ and $\tau _ { T } =$ 0.225 to all 2,300 flows without proxy-type information, using the same frozen models and scores. Table X shows one additional Pure Proxy false positive; ToP detections and Ordinary and Direct Tor decisions are unchanged. The uniform-rule counts yield 99.40686% macro-F1, reported as 99.41%.

## REFERENCES

[1] R. Dingledine, N. Mathewson, and P. Syverson, “Tor: The secondgeneration onion router,” in Proc. 13th USENIX Security Symp. San Diego, CA: USENIX Association, Aug. 2004, pp. 303–320.

[2] H. Wu, S. Guo, G. Cheng, and X. Hu, “Detecting Tor bridge from sampled traffic in backbone networks,” in Proc. Workshop Meas., Attacks, Defenses Web (MADWeb). Internet Society, 2021.

[3] G. Cherubin, R. Jansen, and C. Troncoso, “Online website fingerprinting: Evaluating website fingerprinting attacks on Tor in the real world,” in Proc. 31st USENIX Security Symp. Boston, MA: USENIX Association, Aug. 2022, pp. 753–770.

[4] M. Dusi, M. Crotti, F. Gringoli, and L. Salgarelli, “Detection of encrypted tunnels across network boundaries,” in Proc. IEEE Int. Conf. Commun. (ICC). IEEE, 2008, pp. 1738–1744.

[5] S. Frolov, J. Wampler, and E. Wustrow, “Detecting probe-resistant proxies,” in Proc. Netw. Distrib. Syst. Security Symp. (NDSS). Internet Society, 2020.

[6] Alice, Bob, Carol, J. Beznazwy, and A. Houmansadr, “How China detects and blocks Shadowsocks,” in Proc. ACM Internet Meas. Conf. (IMC). ACM, 2020, pp. 111–124.

[7] M. Wu et al., “How the great firewall of China detects and blocks fully encrypted traffic,” in Proc. 32nd USENIX Security Symp. Anaheim, CA: USENIX Association, Aug. 2023, pp. 2653–2670.

[8] Y. Chen and Y. Wang, “MPAF: Encrypted traffic classification with multi-phase attribute fingerprint,” IEEE Trans. Inf. Forensics Security, vol. 19, pp. 7091–7105, 2024.

[9] C.-L. Li, J.-F. Wang, Z.-Y. Fang, and H. Sun, “Encrypted Tor traffic detection method based on feature fusion,” J. Sichuan Univ. (Nat. Sci. Ed.), vol. 61, no. 3, pp. 95–103, 2024, (in Chinese).

[10] N. Wickramasinghe, A. Shaghaghi, G. Tsudik, and S. Jha, “SoK: Decoding the enigma of encrypted network traffic classifiers,” in Proc. IEEE Symp. Security Privacy (SP). IEEE, 2025, pp. 1825–1843.

[11] C. Wang, X. Xie, T. Wang, and Y. Cui, “Bias in the shadows: Explore shortcuts in encrypted network traffic classification,” 2026, arXiv:2601.10180. [Online]. Available: https://arxiv.org/abs/2601.10180

[12] Y. Zhao, G. Dettori, M. Boffa, L. Vassio, and M. Mellia, “The sweet danger of sugar: Debunking representation learning for encrypted traffic classification,” in Proc. ACM SIGCOMM Conf. ACM, 2025, pp. 296– 310.

[13] D. Xue, M. Kallitsis, A. Houmansadr, and R. Ensafi, “Fingerprinting obfuscated proxy traffic with encapsulated TLS handshakes,” in Proc. 33rd USENIX Security Symp. Philadelphia, PA: USENIX Association, Aug. 2024, pp. 2689–2706.

[14] D. Xue, R. Stanley, P. Kumar, and R. Ensafi, “The discriminative power of cross-layer RTTs in fingerprinting proxy traffic,” in Proc. Netw. Distrib. Syst. Security Symp. (NDSS). Internet Society, 2025.

[15] D. Xu, G. Cheng, H. Hu, Q. Ren, X. Yang, and K. Wang, “STNet: Multiscale spatiotemporal learning and adaptive fusion for few-shot Tor traffic classification,” IEEE Trans. Netw. Service Manag., vol. 23, pp. 7173– 7190, 2026.

[16] B. Wang et al., “MTBD: HTTPS tunnel detection based on multidimension traffic behaviors decision,” in Proc. IEEE Int. Conf. High Perform. Comput. Commun.; Data Sci. Syst.; Smart City; Dependability Sensor, Cloud, Big Data Syst. Appl. (HPCC/DSS/SmartCity/DependSys). IEEE, 2022, pp. 474–481.

[17] Z. Gu et al., “DecETT: Accurate app fingerprinting under encrypted tunnels via dual decouple-based semantic enhancement,” in Proc. ACM Web Conf. (WWW). ACM, Apr. 2025, pp. 2413–2423.

[18] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “AppScanner: Automatic fingerprinting of smartphone apps from encrypted network traffic,” in Proc. IEEE Eur. Symp. Security Privacy (EuroS&P). IEEE, 2016, pp. 439–454.

[19] T. van Ede et al., “FlowPrint: Semi-supervised mobile-app fingerprinting on encrypted network traffic,” in Proc. Netw. Distrib. Syst. Security Symp. (NDSS). San Diego, CA, USA: Internet Society, 2020.

[20] D. Barradas, N. Santos, L. Rodrigues, S. Signorello, F. M. V. Ramos, and A. Madeira, “FlowLens: Enabling efficient flow classification for ML-based network security applications,” in Proc. Netw. Distrib. Syst. Security Symp. (NDSS). Virtual: Internet Society, 2021.

[21] C. Fu, Q. Li, M. Shen, and K. Xu, “Realtime robust malicious traffic detection via frequency domain analysis,” in Proc. ACM SIGSAC Conf. Comput. Commun. Security (CCS), ser. CCS ’21. New York, NY, USA: ACM, 2021, pp. 3431–3446.

[22] J. Koumar, K. Hynek, J. Pesek, and T.ˇ Cejka, “NetTiSA: Extended IP<sup>ˇ</sup> flow with time-series features for universal bandwidth-constrained highspeed network traffic classification,” Comput. Netw., vol. 240, 2024, Art. no. 110147.

[23] FoxIO-LLC, “JA4+ Network Fingerprinting,” GitHub repository, 2026, Accessed: Sep. 9, 2026. [Online]. Available: https://github.com/ FoxIO-LLC/ja4

[24] T. Shapira and Y. Shavitt, “FlowPic: A generic representation for encrypted traffic classification and applications identification,” IEEE Trans. Netw. Service Manag., vol. 18, no. 2, pp. 1218–1232, Jun. 2021.

[25] J. Kotak, I. Yankelev, I. Bibi, Y. Elovici, and A. Shabtai, “VPN-encrypted network traffic classification using a time-series approach,” IEEE Trans. Netw. Service Manag., vol. 22, no. 2, pp. 2225–2242, Apr. 2025.

[26] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “FS-Net: A flow sequence network for encrypted traffic classification,” in Proc. IEEE INFOCOM. IEEE, 2019, pp. 1171–1179.

[27] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “ET-BERT: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in Proc. ACM Web Conf. (WWW), ser. WWW ’22. New York, NY, USA: ACM, 2022, pp. 633–642.

[28] R. Zhao et al., “Yet another traffic classifier: A masked autoencoder based traffic transformer with multi-level flow representation,” in Proc. AAAI Conf. Artif. Intell., vol. 37, no. 4. AAAI Press, 2023, pp. 5420– 5427.

[29] T. Wang, X. Xie, W. Wang, C. Wang, Y. Zhao, and Y. Cui, “NetMamba: Efficient network traffic classification via pre-training unidirectional Mamba,” in Proc. IEEE Int. Conf. Netw. Protocols (ICNP). IEEE, 2024, pp. 1–11.

[30] G. Zhou, X. Guo, Z. Liu, T. Li, Q. Li, and K. Xu, “TrafficFormer: An efficient pre-trained model for traffic data,” in Proc. IEEE Symp. Security Privacy (SP). IEEE, 2025, pp. 1844–1860.

[31] Y. Qing et al., “Training robust classifiers for classifying encrypted traffic under dynamic network conditions,” in Proc. ACM SIGSAC Conf. Comput. Commun. Security (CCS). ACM, 2025, pp. 3564–3578.

[32] Shadowsocks Project, “Shadowsocks Protocol,” GitHub protocol documentation, 2020, Accessed: Sep. 9, 2026. [Online]. Available: https://github.com/shadowsocks/shadowsocks-org/wiki/Protocol

[33] trojan-gfw, “The Trojan Protocol,” Official protocol documentation, 2020, Accessed: Sep. 9, 2026. [Online]. Available: https://trojan-gfw. github.io/trojan/protocol

[34] V2Fly Project, “VMess Protocol Configuration,” Official V2Fly documentation, 2026, Accessed: Sep. 9, 2026. [Online]. Available: https://www.v2fly.org/config/protocols/vmess.htm

[35] V2Fly Project, “VLESS Protocol Configuration,” Official V2Fly documentation, 2026, Accessed: Sep. 9, 2026. [Online]. Available: https://www.v2fly.org/config/protocols/vless.htm

[36] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware traffic classification using convolutional neural network for representation learning,” in Proc. Int. Conf. Inf. Netw. (ICOIN). IEEE, 2017, pp. 712–717.

[37] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of encrypted and VPN traffic using time-related features,” in Proc. 2nd Int. Conf. Inf. Syst. Security Privacy (ICISSP). SCITEPRESS, Feb. 2016, pp. 407–414.

[38] X. Deng, Y. Wang, and Z. Xue, “AN-Net: An anti-noise network for anonymous traffic classification,” in Proc. ACM Web Conf. (WWW). ACM, 2024, pp. 4417–4428.

![](images/af0950137e5ac9815ac839bd9db2643c3020eb5ffdde11ff0072f70acb32e283.jpg)  
Chenxin Zhou received the bachelor’s degree from Sichuan University, Chengdu, China, and subsequently began pursuing a Ph.D. degree at its School of Cyber Science and Engineering. His research interests include network traffic analysis.

![](images/a843e3cc393065e9d5ec0d7f862aa295c63ceba147c6cff6669971341a04b2e2.jpg)

Cheng Huang (Senior Member, IEEE) received the Ph.D. degree from Sichuan University, Chengdu, China, in 2017. From 2014 to 2015, he was a visiting student at the School of Computer Science, University of California, CA, USA. He is currently a Professor at the School of Cyber Science and Engineering, Sichuan University, Chengdu, China. His research interests include Web security, attack detection, and artificial intelligence.

![](images/0bc6fd70227dbe26464763ee61ec451031465f459a372fac9dbbd5acf29a8c18.jpg)

Qiang Zhang received the B.Sc. and M.Sc. degrees from Sichuan University, Chengdu, China, in 2018 and 2022, respectively. He is currently pursuing a Ph.D. degree at Sichuan University. His research interests include encrypted network traffic analysis.

![](images/b8a0e843f7efc42548a304cdc288b882fc665565feeef295e52b93754398cb68.jpg)

Qiliang Xie received his master’s degree from the School of Software, Jiangxi Agricultural University, Nanchang, China, in 2025. He is currently a Ph.D. student in the School of Cyber Science and Engineering, Sichuan University, Chengdu, China. His research interests include Encrypted Client Hello (ECH) traffic detection and Tor traffic detection.

![](images/297084e1f5720be86a97deefa6a672d3a43050e79e23f60a11c98b5f8b4c87dc.jpg)

Zeqing Li received the B.S. degree from Sichuan University, Chengdu, China, in 2024. He is currently pursuing the master’s degree at the School of Cyber Science and Engineering, Sichuan University, Chengdu, China. His current research interests include threat intelligence and link prediction.
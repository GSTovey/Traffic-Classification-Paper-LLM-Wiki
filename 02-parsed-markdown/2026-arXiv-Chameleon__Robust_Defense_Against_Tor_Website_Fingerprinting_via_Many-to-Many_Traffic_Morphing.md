# Chameleon: Robust Defense Against Tor Website Fingerprinting via Many-to-Many Traffic Morphing

Yuwen Cui<sup>∗</sup>, Kai Wei<sup>∗</sup>, Kehan Shen<sup>∗</sup>, Ning Wang<sup>∗</sup>, Zhuo Lu<sup>†</sup>, Yao Liu<sup>∗</sup>, Guangjing Wang<sup>∗</sup>

Bellini College of Artificial Intelligence, Cybersecurity and Computing, University of South Florida

<sup>†</sup> Department of Electrical and Computer Engineering, University of South Florida

Abstract—Website fingerprinting (WF) attacks can infer users’ browsing activities from encrypted Tor traffic by exploiting side-channel features. Although many WF defenses have been proposed, we find that most existing defenses create learnable web trace mapping features. We further show that robustness against adversarial training does not necessarily imply robustness against defense-aware autoencoder (DAAE)-based attacks.

To address these limitations, we present Chameleon, a robust WF defense based on many-to-many randomized traffic morphing. Chameleon selects morphing candidates with high intra-class diversity and low inter-class disparity. Chameleon randomly maps each webpage trace to multiple candidates, and allows different webpages to share morphing targets, thereby increasing adversarial uncertainty. For practical Tor deployment, Chameleon introduces a radix-trie-based synchronization mechanism that enables pluggable transport (PT) endpoints to identify consistent morphing traces using packet-direction prefixes, together with trace mutation and normalized prefix matching to reduce overhead. We evaluate Chameleon against six state-of-the-art defenses and five WF attacks on three public datasets in closedand open-world settings. Compared with Adaptive Tamaraw, Chameleon reduces adversarial-training-based attack accuracy by up to 36.74% while reducing bandwidth and time overhead by 34.12% and 60.38%, respectively. Under DAAE-based RF attacks on GTT23, Chameleon limits attack performance to 35.19% F1- score while Adaptive Tamaraw only limits it to 88.22% F1-score. In the real-world PT bridge evaluation, Chameleon substantially reduces the effectiveness of strong WF attacks while incurring only 16.25% time overhead.

## I. INTRODUCTION

Encrypted networks such as Tor [1] remain vulnerable to website fingerprinting (WF) attacks [2]–[5]. For example, observable side-channel information in Tor network traffic, such as traffic timing [6]–[9], traffic bursts [3], [10], and traffic direction [5], [11], can still reveal web browsing activities.

Many defense mechanisms [12]–[14] have been proposed to defend against WF attacks. For example, adaptive paddingbased obfuscation techniques [13], [15], [16] insert dummy packets to obfuscate features, such as packet timing and traffic bursts. Adversarial perturbation techniques [17]–[20] generate adversarial noise to misguide deep learning-based WF attacks. Regularization-based methods [8], [14], [21] transform traffic traces into regularized sequences with similar patterns, reducing the distinguishability among different website traces.

However, we discover that most existing defenses create stable, learnable defense-induced mappings, which can be utilized by defense-aware attacks. Specifically, we assume a strong WF adversary who is aware that a defense is deployed on Tor but does not know the specific defense mechanism being used. The adversary can train a Defense-Aware Autoencoder (DAAE) to learn defense-induced perturbation patterns using paired original Tor website traces and defense-perturbed traces. The specific design of DAAE is in Appendix B. We find that DAAE can easily recover raw traffic features from previously unseen defended traces. As shown in Figure 1, existing defenses reduce the website fingerprinting attack model DF [4] accuracy from 93.2% to 2%-35%. However, the DAAE-based DF attack recovers attack performance against these defenses, achieving over 90% accuracy against RegulaTor [21] and over 80% against Palette [23] and Adaptive Tamaraw [24]. Similarly, adversarial training mostly recovers the attack performance against several defenses, with accuracy exceeding 90% for FRONT [16] and FRUGAL [20] and 80% for Walkie-Talkie [14]. Furthermore, we reveal that defense robustness against adversarial training does not necessarily imply robustness to DAAE-based attacks. For instance, RegulaTor, Palette, and Adaptive Tamaraw remain resilient to adversarial training-assisted attacks, but can be compromised by DAAE-based attacks.

![](images/498ee37b5e8f3659366247ab73226205ad0455437f5e5305c81c1b7ba1ffd6cf.jpg)  
Fig. 1: An exemplar of WF defense evaluation on the GTT23 [22] dataset under adversarial training (AT)-assisted and DAAE-assisted deep fingerprinting (DF) [4] attack. The legend includes non-defended traffic (NoDef), traffic defended with different defenses against the DF attack without adversarial training (w/o AT), against the DF attack with adversarial training (w/ AT), and against the DAAE-assisted DF (DAAE).

In this work, we design Chameleon to eliminate stable mappings through randomized many-to-many transformations for a robust WF defense. Chameleon is based on traffic morphing, which transforms the traffic pattern of a given website to resemble that of another site [8], [25]. Through a many-to-many morphing design, Chameleon randomly maps a single website trace to multiple target morphing traces. Each target trace can correspond to multiple source traces. The key innovation is a novel design to ensure consistency between the pluggable transport client and server (PTs) [26], [27] in real-world deployments of many-to-many random morphing. Chameleon theoretically increases the uncertainty faced by the adversary and thereby raises the difficulty of DAAE and adversarial training-based WF attacks. In addition, we design a radix trie–based structure and trace mutation algorithm that enables efficient morphing target selection, so as to reduce the overhead when dealing with unseen websites. Specifically, we address the following three challenges.

![](images/97706b45fdb1d6cc885ccc1c8d9073f85dcb7628621f8f0f08484317b6e7a58f.jpg)  
Fig. 2: Overview of the Tor network and Threat Position.

First, how to defend against defense-aware adversarial training-based and DAAE-based attacks? To obfuscate defense-aware attacks, we design methods to collect traffic that exhibits high intra-class diversity and low interclass disparity, which is used as traffic morphing candidates. During online deployment, each webpage trace is morphed to one of these candidates, misleading WF attack models. Specifically, we design a lightweight offline trace-selection algorithm that characterizes the geometric relationships among traffic traces and identifies representative traces with high intra-class diversity and low inter-class disparity. In addition, Chameleon randomly maps each webpage trace to multiple candidate traces while allowing different webpages to share the same morphing targets. This randomized mapping eliminates the deterministic traffic transformation exploited by DAAE, thereby substantially improving defense robustness.

Second, how can a many-to-many traffic morphing strategy be synchronized between the PT client and the PT server? The defenses [16], [18], [21], [23], including Chameleon, can be deployed through PTs, as shown in Figure 2. A PT client and PT server provide user-configurable traffic defenses without modifying the underlying Tor protocol [26]. However, synchronizing web traffic between the PT client and bridge after many-to-many random morphing is challenging because the randomization can induce the endpoints to select inconsistent morphing traces.

We observe that packet direction sequences are determined from the packet departure timestamps at the PT endpoint during real-time transmission rather than their delivery timestamps. This observation provides a consistent basis for synchronization between the PT client and PT server. Therefore, we design a radix trie [28]-based structure to pre-match candidate morphing traces according to their packet-direction prefixes. The PT endpoint that first determines the morphing trace can send a short sequence of consecutive packet directions from the selected trace as an implicit synchronization signal.

Upon receiving this sequence, the peer PT endpoint performs a prefix search on its local radix trie and identifies the same morphing trace without requiring an explicit trace identifier. Once the trace is identified, both endpoints apply the same morphing pattern to subsequent traffic, thereby maintaining consistent real-time morphing across the PTs.

Third, how to reduce the extra time and bandwidth overhead incurred by the morphing process? As the number of candidate traces grows, the morphing process introduces additional computation time and bandwidth overhead. The core question is how to achieve a trade-off between the overhead and the defense performance. We have two main designs. (i) We propose a trace mutation algorithm that minimizes additional padding when computing the distance between the real-time input packets and the selected target morphing trace. In this way, we can reduce the overhead introduced by the potential trace difference from unseen webpages. (ii) We design a rowwise normalization scheme for the candidate traces to enable efficient trace matching. The normalization removes scale and offset variations within each trace, ensuring that matching decisions are driven by intrinsic traffic patterns rather than absolute magnitudes. Then, we construct prefix-based feature vectors, where traces sharing common structural prefixes are organized hierarchically within the radix trie. This design facilitates log-time lookup during morphing target selection.

We compare Chameleon with six state-of-the-art (SOTA) WF defenses against five SOTA WF attack models on three widely used public datasets in the closed- and open-world scenarios. Compared with the recent Adaptive Tamaraw defense [24], Chameleon further reduces adversarial trainingbased WF attack accuracy by up to 36.74%, while also reducing bandwidth overhead by 34.12% and time overhead by 60.38% on the DF dataset. In particular, under DAAE-based RF attacks [2], Chameleon limits attack performance on the GTT23 dataset to 40.68% precision and a 35.19% F1-score. In comparison, the same RF attack achieves 80.64% precision and a 70.30% F1-score under Palette defense, and 89.82% precision and an 88.22% F1-score under Adaptive Tamaraw defense strategy.

Overall, our main contributions are listed as follows:

• We design a robust WF defense model that builds candidate website traces with high intra-class diversity and low inter-class disparity to remove conspicuous features in morphing.

• We introduce a radix trie structure to efficiently match a morphing trace from the website trace candidates and a trace mutation algorithm to efficiently reduce overhead.

• We evaluate SOTA WF defenses against adversarial training-based and DAAE-based attacks, revealing limitations in existing WF defense mechanisms.

• We conduct a comprehensive evaluation and demonstrate that Chameleon exhibits superior robustness to adversarial training-based WF attacks with modest overhead.

![](images/d01a83efd81ba9e3aed2f135feae9f390396faa188f8be51ef9659dfebaf4ada.jpg)  
Fig. 3: Tor traffic timing trace with direction, bursts, and ordering from client to Tor network.

## II. BACKGROUND AND MOTIVATION

## A. Tor Traffic Features

The main Tor traffic features, as shown in Fig. 3, include packet inter-arrival time, burst, packet ordering, direction, and so on. Specifically, traffic direction is encoded as +1 for outgoing packets from the client to the Tor network and -1 for incoming packets from the Tor network to the client [10], [11], [29]. The traffic direction provides packet ordering information, which describes the sequence in which packets are transmitted and received during a browsing session. The packet ordering captures the precise arrangement of requestresponse interactions between a client and a server [30]. The traffic bursts are sequences of consecutive packets in the same direction, either incoming or outgoing. The burst patterns capture higher-level structural information about how websites load resources, such as videos, audio, and pictures, reflecting grouped transactions between browsers and servers.

Packet inter-arrival time [6] measures the time interval ∆t between consecutive packets in the same direction. The T and L, as shown in Fig. 3, denote the fixed time window and the traffic length for captured Tor flows, respectively. Generally, the Tor protocol splits traffic into cells with a fixed size of 512 bytes. The fixed time window T or the traffic length L helps standardize traffic traces into uniform representations. In this work, Chameleon obfuscates trace-level features, including inter-packet timing and traffic burst structures, by morphing traces toward pre-selected candidate website traces. These features are specifically targeted, as they constitute the primary discriminative patterns exploited by SOTA WF attacks [2], [3].

## B. Tor Pluggable Transport Bridges

Pluggable Transport (PT) bridges act as programmable proxies between the Tor client and entry guard. In a PT deployment, the Tor client forwards traffic to a locally running PT client, which transforms the traffic before transmitting it to a corresponding PT server associated with an entry guard. The PT server reverses the transformation and forwards the resulting traffic to the Tor network. In this way, PT helps establish an end-to-end connection while hiding or modifying traffic characteristics observable on the client-bridge link.

The PT architecture provides an extensible interface through which traffic-obfuscation mechanisms can be deployed [26]. A defense can be implemented within the PT client and server components and applied to traffic without requiring prior knowledge of the destination website or changes to the underlying Tor network. In particular, a client-side defense can delay packets and inject dummy packets before traffic leaves the PT client/server, while the corresponding bridgeside component coordinates any state required to reconstruct the original Tor communication. In summary, PTs offer a deployable and modular interface for evaluating WF defenses under realistic network conditions while preserving compatibility with the existing Tor infrastructure.

TABLE I: A comparison of the WF defenses.

<table><tr><td>Categories</td><td>Defenses</td><td>Live Traffic</td><td>AT Resistance</td><td>DAAE Resistance</td><td>Supports PT</td></tr><tr><td rowspan="5">Obfuscation</td><td>WTF-PAD [13]</td><td>√</td><td>✗</td><td>-</td><td>√</td></tr><tr><td>FRONT [16]</td><td>√</td><td>✗</td><td>-</td><td>√</td></tr><tr><td>ALERT [19]</td><td>✗</td><td>✗</td><td>-</td><td>✗</td></tr><tr><td>GAPDiS [18]</td><td>√</td><td>✗</td><td>-</td><td>√</td></tr><tr><td>FRUGAL [20]</td><td>√</td><td>✗</td><td>-</td><td>✗</td></tr><tr><td rowspan="5">Regularization</td><td>CS-BuFLO [31]</td><td>✗</td><td>✗</td><td>-</td><td>✗</td></tr><tr><td>Super-sequence [8]</td><td>✗</td><td>✗</td><td>-</td><td>✗</td></tr><tr><td>Palette [23]</td><td>√</td><td>√</td><td>✗</td><td>√</td></tr><tr><td>Adaptive Tamaraw [24]</td><td>○</td><td>√</td><td>✗</td><td>✗</td></tr><tr><td>Chameleon (Ours)</td><td>√</td><td>√</td><td>√</td><td>√</td></tr></table>

◦: Insufficient evidence from the paper and provided artifact; –: If the defense does not resist AT, the DAAE-based attack is not performed; Live Traffic and Supports PT are determined from the original papers and publicly available artifacts; AT and DAAE attack resistance are determined from our evaluations unless otherwise noted.

## C. Related Defense Work Comparison

We compare and summarize major defense methods in Table I. “Live Traffic” denotes applicability to real-time traffic. “AdvTrain Resistance” denotes adversarial training (AT)-based attack accuracy below 50%. “DAAE Resistance” denotes DAAE-based attack accuracy below 50%. “Supports PT” denotes that a PT-based pluggable defense implementation is provided. In particular, defenses that support live traffic adaptation, such as FRONT, GAPDiS, and FRUGAL, remain vulnerable to AT-based attacks. In contrast, defenses with stronger robustness, such as Palette, introduce additional constraints on traffic shaping and deployment. More importantly, existing defenses provide limited protection against DAAEbased attacks, which can explicitly learn the characteristics introduced by a deployed defense. A practical WF defense needs to jointly support live traffic, robustness against defenseaware attacks, and be deployable through a PT interface.

## III. PRELIMINARY

## A. Threat Model

1) Attack Scenario: We consider the standard local passive adversary that monitors the communication network traffic between the Tor client and the entry guard but cannot modify traffic packets, as shown in Figure 2. The defense mechanisms can be deployed through a Pluggable Transport (PT) bridge [18], [23], [27], which acts as proxies between the Tor client and the entry guard to obfuscate traffic.

2) Attacker Capability: We consider a strong adversary with access to defended traffic traces from monitored webpages collected under conditions comparable to those experienced by a normal user. We assume the adversary can collect both original Tor traffic at the client side (⃝1 in Figure 2) and the corresponding defended traffic transmitted through the PT client and PT server (⃝2 in Figure 2).

![](images/9309e155a2421a281577d4276da0f865d40f5c354418ccb1c7183caa44e067c5.jpg)  
Fig. 4: Overview Chameleon architecture. 1) Separate the high intra-class diversity and low inter-class disparity data as morphing trace candidates. 2) Construct a radix trie based on the selected trace set. 3) Apply trace mutation to reconcile burst discrepancies between real-time traffic and target morphed traces.

We consider a strong adversary who uses the collected traces to train either adversarial training-based WF attacks or DAAE-based WF attacks. These two attack strategies represent increasing knowledge of the defense and enable us to evaluate whether a defense remains effective when the adversary explicitly adapts to traffic transformations for WF attacks.

3) Defense Setting: The Chameleon does not require prior knowledge of the destination webpage. Thus, Chameleon can be applied to arbitrary browsing webpages rather than a preconfigured set of static candidate traces. Additionally, PTs are independently deployed by users. Therefore, the defense for different users does not rely on the same predefined payloads or destination-specific configurations. In this setting, Chameleon can avoid introducing stable, webpage-dependent artifacts that an adaptive adversary can learn.

## B. Problem Formulation

The Tor network traffic is represented as a time-ordered sequence of packets. Formally, each traffic trace corresponding to the loading of a webpage is represented as: w = $[ ( t _ { 1 } , d _ { 1 } ) , ( t _ { 2 } , d _ { 2 } ) , \dots , ( t _ { N } , d _ { N } ) ]$ . N is the total number of website packets observed during the session. $t _ { i } \in \{ t _ { 1 } , t _ { 2 } , . . . , t _ { N } \}$ indicates the timestamp at the i-th packet in the trace sequence. $d _ { i } \in \{ + 1 , - 1 \}$ denotes the direction of the i-th packet.

Let W denote the monitored websites and X denote the space of observable traffic. An adversary aims to learn a classification model $h : \mathcal { X }  \mathcal { W }$ that predicts the specific website from an observed trace. The WF defense system can be regarded as a stochastic transformation mechanism $\mathcal { D } : \mathcal { W }  \mathcal { D } ( \mathcal { X } )$ , where D(X ) denotes a distribution over defended traces. $\mathcal { R } \subseteq \mathcal { W } \times \mathcal { W } ^ { \prime }$ denotes the defense relation, where $( w , w ^ { ' } ) \in \mathcal { R }$ indicates that $w ^ { ' }$ is a valid defended trace generated from the original trace w by the defense mechanism. A WF defense usually modifies the w to $w ^ { ' }$ by injecting dummy packets $d ^ { ' }$ or increasing the timing delay τ. In Chameleon, we model the defense mechanism as a mapping between original traffic traces and defended traffic traces: ${ \mathsf { \bar { f } } } : W \to W ^ { \prime }$ . W represents the set of all collected traffic traces. $W ^ { ' }$ is the set of all manipulated traces derived from W. Formally, the $f : W \to W ^ { \prime }$ satisties:

$$
\begin{array}{c} \forall w \in W,   \exists w _ {1} ^ {\prime}, w _ {2} ^ {\prime} \in W ^ {\prime},   w _ {1} ^ {\prime} \neq w _ {2} ^ {\prime}, \\ \text {s.t.} (w, w _ {1} ^ {\prime}) \in \mathcal {R},   (w, w _ {2} ^ {\prime}) \in \mathcal {R}. \end{array}\tag{1}
$$

The many-to-many mapping enables multiple transformations per trace and partial overlap across classes, thereby disrupting both intra-class similarity and inter-class disparity. We provide a theoretical analysis of attacker success by analyzing the many-to-many mapping used by Chameleon in Appendix H.

Following the literature [23], [24], the bandwidth overhead of defense is measured as the ratio of the total amount of dummy data to the total amount of real packets, denoted as $\begin{array} { r } { B ( w , w ^ { ' } ) = \frac { | w ^ { ' } | - | w | } { | w | } } \end{array}$ . Similarly, the time overhead is measured as $\begin{array} { r } { T ( w , w ^ { ' } ) = \frac { \dot { t } _ { k } - { t } _ { N } } { t _ { N } } } \end{array}$ , where $t _ { k }$ is the time spent transmitting the defended trace w .

## IV. SYSTEM DESIGN

## A. Candidate Website Traces Generation

We observe that the existing WF attacks achieve high classification accuracy by learning feature representations with high intra-class similarity and high inter-class disparity. Therefore, to compromise the WF attacks, we need to obfuscate the intra-class and inter-class features. Specifically, we select samples that are more scattered inside the same class (high intra-class diversity) and closer to neighboring classes (low inter-class disparity). High intra-class diversity expands the apparent pattern of each class. If selected website traces from the same website vary significantly, the WF attack model needs to generalize over a wider region. Meanwhile, low inter-class disparity reduces the margin between classes: traces from different websites become harder to separate. The two properties make learned decision boundaries less stable and increase confusion around class borders.

```txt
Algorithm 1: HiLoD algorithm

Input: traces, labels, neighbor size k, selection ratio ρ
Output: selected_traces, selected_trace_labels

1 n ← |traces|;
2 for i ← 1 to n do
3    X[i] ← TRACETOFEATURE(traces[i]);
4 μ ← mean(X, axis = 0),
    σ ← std(X, axis = 0) + 10^{-6};
5 X_n ← (X - μ)/σ, k_eff ← min(max(3, k), n - 1);
6 (dists, nbrs) ← NEAREST NEIGHBORS(X_n, k_eff + 1);
7 Initialize scores[1..n] ← 0;
8 for i ← 1 to n do
9    nn_idx ← nbrs[i, 2 : k_eff + 1];
10    nn_dist ← dists[i, 2 : k_eff + 1];
11    nn_lab ← labels[nn_idx];
12    S_i ← {j ∈ {1, ..., k_eff} : nn_lab[j] = labels[i]}
13    D_i ← {j ∈ {1, ..., k_eff} : nn_lab[j] ≠ labels[i]}
14    if |S_i| > 0 then
15    intra_i ← mean(nn_dist[t] | t ∈ S_i)
16    else
17    intra_i ← max(nn_dist);
18    if |D_i| > 0 then
19    inter_i ← mean(nn_dist[t] | t ∈ D_i)
20    else
21    inter_i ← max(nn_dist);
22    mislead_i ← |D_i| / k_eff
23    scores[i] ← intra_i - inter_i + mislead_i;
24 m ← min(「ρ * n」, n);
25 return selected_website_traces, selected_trace_labels ← Sorted Top-m indices by descending scores;
```

To depict trace candidates that exhibit high intra-class diversity and low inter-class disparity, we model traces with direction and timing features using a distance-based method. The advantage is that Chameleon can capture relationships among neighboring samples (e.g., from the same website) with minimal modeling assumptions. Additionally, distance-based neighborhood modeling remains robust when class manifolds are irregular or non-linear, which is suitable for extracting complex patterns from monitored website traffic traces.

In addition, a dedicated burst model is constructed from the direction sequence. Chameleon detects direction change boundaries and computes lengths of consecutive samedirection packets. From these lengths, Chameleon extracts burst mean, burst standard deviation, median, 90th percentile, burst count, and proportions of short bursts (e.g., shorter than 2) and long bursts (e.g., longer than 8). This provides a compact descriptor of patterns between inbound and outbound traffic, which are highly discriminative in Tor traffic analysis.

The algorithm for generating high intra-class diversity and low inter-class disparity (HiLoD) website trace candidates is presented in Algorithm 1. To mitigate the potential information leakage from the morphing trace candidates, Chameleon first converts each trace from the monitored dataset into a fixeddimensional representation to support downstream distancebased modeling (lines 2-3 in Algorithm 1). Specifically, Chameleon decomposes the raw trace into three complementary information channels as the feature vector: traffic volume, temporal dynamics, and directional structure [32]. Volume statistics include packet counts by direction (incoming and outgoing packets) and cumulative bytes by direction, as well as absolute-size descriptors (e.g., first 20 packets, last 30 packets, and standard deviation). Temporal dynamics are captured through duration $( t _ { N } - t _ { 1 } )$ and inter-packet-time (IPT) summaries, including mean, standard deviation, quartiles, and extrema. This explicitly encodes both central tendency and dispersion of timing, which is important for distinguishing traffic classes that differ in burstiness or pacing.

![](images/242d2717542ef89fd996f0e0cd56256e23794c4d5113642cacfd080ad2da3fdc.jpg)  
Fig. 5: Visualization of Radix Trie. Traces are organized into a hierarchical key structure based on shared prefixes.

Then, for each website trace, Chameleon first estimates the average distance to same-class neighbors (lines 14-17 in Algorithm 1). Chameleon calculates the average distance to neighbors of different classes (lines 18-21). Finally, Chameleon computes the mislead fraction of different-class neighbors (line 22). Line 23 defines the formula to calculate the score for prominent traces that are diverse within a class. In this formula, intra denotes the average distance to same-class neighbors, where larger values indicate greater diversity within the class. Conversely, inter represents the average distance to different-class neighbors, where smaller values suggest increased overlap across classes. A higher score therefore corresponds to traces that are more ambiguous and harder for WF attack models to distinguish, making them less cleanly separable in the feature space. The candidate website traces are sorted by descending score value. Chameleon selects the topscoring subset that directly targets regions where classifiers are most error-prone. In line 24, parameter ρ is the selection ratio, which controls the injectivity boundary for traffic morphing of selected website trace candidates.

## B. Radix Trie Construction

With the generated candidate trace pool in Section IV-A, we index the pool with a radix trie over binary direction sequences. As illustrated in Figure 5, the radix trie is a compressed prefix-tree structure defined over directions {−1, +1}, where each root-to-node path corresponds to a direction prefix of the real-time browsing traffic. Following the traffic trace abstraction, each edge encodes a single outgoing or incoming packet step. At each node, we associate pool traces that share the same prefix, enabling sublinear candidate search rather than an exhaustive scan over variable-length traces.

However, prefix matching alone can be ambiguous: short prefixes may correspond to heterogeneous candidates, while long prefixes may overly constrain the search space. To regularize candidate selection, we construct a fixed-length embedding for each trace. Given a direction sequence w = $( d _ { 1 } , \dots , d _ { T } )$ with $d _ { i } \in \{ - 1 , + 1 \}$ , we truncate or zero-pad it to length L to obtain x $\in \mathbb { R } ^ { L }$ . Then, we stack all embeddings to yield a matrix $\mathbf { X } \in \mathbb { R } ^ { N \times L }$ . We then apply row-wise z-score normalization followed by $\ell _ { 2 }$ normalization. The normalization design is described in Appendix C. To maintain coherence between the PT client and PT server in real-world deployment, the matching candidates need to exhibit distinct directions over the next few packets. The next few packets are used to verify short-term consistency between client and guard node traces by checking the sequence of packet directions. This constraint ensures that immediate temporal structure remains compatible, preventing abrupt inconsistencies during morphing.

During real-time transmission, packet direction sequences are determined from the packet departure timestamps at the PT endpoint rather than their delivery timestamps. Such a setting provides a consistent basis for synchronization between the PT client and PT server. The radix-trie search progressively narrows the candidate set as additional packet directions are observed, until less than, for example, 10 candidates remain. The endpoint that first determines the morphing trace then sends a short sequence of consecutive dummy packets as an implicit synchronization signal. Specifically, the number of dummy packets corresponds to the shortest prefix that uniquely distinguishes the selected trace from the remaining candidates. Upon receiving these dummy packets, the peer endpoint performs a prefix search on its local radix trie and identifies the same morphing trace without requiring an explicit trace identifier. Since each additional packet direction introduces another branching decision in the radix trie, the candidate space can decrease exponentially with the prefix length, allowing the selected trace to be uniquely identified using a bounded number of packet directions.

Under the balancing branch implementation, when the candidate set contains at most 10 traces, the selected trace is typically uniquely identified by a prefix of 4-5 packet directions. Once the trace is identified, both endpoints apply the same morphing pattern to subsequent traffic, thereby maintaining consistent real-time morphing across the PT bridge. Meanwhile, a given real-world browsing trace will be mapped to different target traces across repeated visits. In this way, even when the same website is visited multiple times during adversarial training data collection, the resulting traces exhibit low inter-instance separability. Therefore, the attacker’s ability to learn stable and discriminative patterns is compromised.

## C. Trace Morphing and Mutation

After the radix trie construction, we can transform the realtime trace into a target morphing trace. As illustrated in Figure 6, the morphing trace is fully known in advance, whereas the real-time trace is only observable up to the time t, as future trace information remains unknown. Consequently, when the real-time captured packet deviates from the morphing trace in terms of packet sequence, the mismatch is compensated by inserting dummy packets derived from the morphing trace. However, these injected dummy packets introduce additional bandwidth consumption and may incur timing delays relative to the original real-time trace.

![](images/c3513d5789382970fdaef85b3e6dad4ea6dfbefd2bf1df26a36a2816837914b8.jpg)  
Fig. 6: Visualization of Trace Morphing. Unknown packets correspond to unobserved traffic; Dummy packets are present in the morphing trace but absent from the real-time trace.

We categorize trace morphing into three categories: full trace morphing, trace cut-off, and trace mutation. (i) In fulltrace morphing, each real-time trace is fully morphed to match a selected target trace. If the trace completes while the target trace still contains a substantial number of remaining packets, the system continues transmitting dummy packets until the target trace reaches its end. Conversely, if the target trace terminates earlier while the real-time trace still contains pending packets, the remaining segment is reassigned to a newly selected target trace for continued transformation. Such a design maximizes indistinguishability at the cost of heavy overhead.

(ii) In the traffic trace cut-off scenario, the morphing process terminates when the real-time trace has been fully transformed, thereby avoiding the transmission of excessive dummy packets required to complete the target trace. Although this strategy reduces overhead, it may still introduce nontrivial padding and timing artifacts where there are long burst packets. As a result, the trace cut-off scenario introduces medium-level overhead.

(iii) We design the third morphing strategy, trace mutation, to further reduce overhead while preserving obfuscation effectiveness. As shown in Figure 7, when the target morphing trace exhibits a prolonged burst of packets whose direction differs from the real-time trace, the real-time trace will be temporarily buffered until a packet matches the direction in the target morphing trace. Once such a match is encountered, the buffered packets can be released to the network. As mentioned in Section IV-B, morphing traces are randomly selected from a predefined morphing group. Consequently, the selected trace may not be the closest match to the underlying real-world traffic trace in terms of sequence similarity. Chameleon first performs a forward consistency check on the morphing trace and compares it with the real-time trace. Based on this comparison, Chameleon identifies an appropriate position to flip exactly one direction bit in a short segment of the target morphing trace. After the flip, the target morphing trace’s directions stay as close as possible to the corresponding real-time browsing directions. In this way, we can reduce directional mismatch and mitigate buffering overhead.

![](images/1601d719772bdb3cb78c4fe5fb5ec641a55d5cad33fd7b4c1e8ea3630fc414f3.jpg)  
Fig. 7: Visualization of Trace Mutation.

To mitigate the overhead arising from this mismatch, we introduce a trace mutation algorithm in Algorithm 2. Specifically, d<sup>target</sup> represents the direction of the target morphing trace. d<sup>in</sup> denotes the direction of the real-time browsing trace. In the trace mutation process, only the directions from the trace are considered. The parameter ℓ indicates the starting position of the trace mutation within the target morphing trace. A window size M defines the valid candidate region for mutation around ℓ (line 3), restricting the search space to feasible positions. Then, Chameleon iterates over all candidate indices within the window to identify the optimal mutation location (line 9). For each candidate position i, Chameleon computes a score to find the best position to execute a trace mutation. The smaller score represents the closest position with low overhead and less information leakage.

The computation of the score includes three components. First, the mismatch term quantifies the inconsistency between the mutated target segment and the real-time input trace, reflecting alignment quality (line 12). A higher mismatch indicates greater deviation and potential bandwidth inefficiency due to increased dummy padding. Second, the distance penalty encourages mutations closer to the intended starting position ℓ and discourages excessive displacement within the morphing trace (line 13). Third, the continuity penalty is computed to enforce local structural smoothness (lines 15-24). This term aggregates up to two indicator-based comparisons between the mutated symbol at position i and its adjacent neighbors. The continuity penalty discourages abrupt directional flips and promotes locally coherent trace patterns. Finally, Chameleon selects the candidate index with the minimum score as the optimal mutation location. A lower score indicates a better trade-off between trace alignment, spatial consistency, and structural smoothness.

## V. PERFORMANCE EVALUATION

## A. Experiment Setup

1) Dataset: We conduct experiments on three widely used datasets, DF [4] and DS-19 [16], and the GTT23 dataset [22].

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2: Trace Mutation Algorithm

Input:  $d^{target}$ ,  $d^{in}$ ,  $\ell$ : the starting position of the trace mutation within the target morphing trace; j: the real-time input packet location.

Output: best_loc: best index selection for trace mutation.

1  $n_{target} \leftarrow |d^{target}|$ ,  $n_{in} \leftarrow |d^{in}|$ ;

2  $idx_{left} \leftarrow \max(0, \ell)$ ;

3  $idx_{right} \leftarrow \min(n_{target} - 1, \ell + M)$ ;

4 if  $idx_{left} &gt; idx_{right}$  then

5 return clip( $\ell$ , 0,  $n_{target} - 1$ );

6  $idx_{w} \leftarrow \min(idx_{right}, n_{in} - 1)$ ;

7  $W^{in} \leftarrow d^{in}$ ,  $W^{target} \leftarrow d^{target}[idx_{left} : idx_{w}]$ ;

8  $idx' \leftarrow idx_{left}$ ,  $score' \leftarrow +\infty$ ;

9 for  $i \leftarrow idx_{left}$  to  $idx_{w}$  do

10    $W \leftarrow copy(W^{target})$ ;

11    $W[i - idx_{left}] \leftarrow -W[i - idx_{left}]$ ;

12 mismatch  $\leftarrow \sum_{j} \not\vdash [W[j] \neq W^{in}[j]]$ ;

13 distance_penalty  $\leftarrow |i - \ell| * 0.25$ ;

14 continuity_penalty  $\leftarrow 0$ ;

15 if  $i - 1 \geq 0$  then

16    if  $i - 1 \geq idx_{left}$  then

17    continuity_penalty  $\leftarrow (\text{continuity_penalty} + \not\vdash [W[i - 1 - idx_{left}] \neq W[i - idx_{left}]])/2$ ;

18 else

19    continuity_penalty  $\leftarrow (\text{continuity_penalty} + \not\vdash [d^{target}[i - 1] \neq W[i - idx_{left}]])/2$ ;

20 if  $i + 1 &lt; n_{target}$  then

21    if  $i + 1 \leq idx_{w}$  then

22    continuity_penalty  $\leftarrow (\text{continuity_penalty} + \not\vdash [W[i + 1 - idx_{left}] \neq W[i - idx_{left}]])/2$ ;

23 else

24    continuity_penalty  $\leftarrow (\text{continuity_penalty} + \not\vdash [d^{target}[i + 1] \neq W[i - idx_{left}]])/2$ ;

25    score  $\leftarrow$  mismatch + distance_penalty + continuity_penalty;

26    if score &lt; score' then

27    score'  $\leftarrow$  score,  $idx' \leftarrow i$ ;

28 return  $idx'$ ;
</div>

The DF dataset contains both closed-world and open-world data. In the DF closed-world dataset, traffic traces are collected from the homepages of the top 100 Alexa-ranked websites, of which 95 sites remain after preprocessing, with 1,000 instances per site. In the open-world dataset, the unmonitored set is constructed from websites ranked within Alexa’s top 50,000, excluding those used in the closed-world setting, resulting in

40,716 sites with one instance per site. All traces are collected using the Tor Browser Crawler [33], with network traffic captured independently via tcpdump.

The DS-19 dataset [16] is collected using Tor Browser 8.5a7 with Tor version 0.4.0.1-alpha, automated through commandline execution. The monitored set consists of the homepages of the top 100 Alexa-ranked websites, each visited 100 times. The unmonitored set includes 10,000 websites, with a single instance recorded per site.

The GTT23 [22] dataset is the first large-scale genuine website fingerprinting dataset collected from a Tor exit relay, containing approximately $( 1 . 4 \times 1 0 ^ { 7 } )$ website visits from over $( 1 . 1 \times 1 0 ^ { 6 } )$ domains. We use CELLSHIFT [34] to construct the closed-world dataset with 100 domains, each containing 2,000 instances, and an additional (1.0 × 10<sup>4</sup>) domains for the open-world evaluation.

2) WF Attacks: We select five SOTA WF attack models as our benchmark. The attacks are listed as follows:

• DF [4]. Deep Fingerprinting (DF) is a DL–based WF attack that uses CNNs to learn distinctive patterns from traffic trace direction automatically.

• Var-CNN [5]. Var-CNN employs a ResNet-based architecture to extract features from packet sequences.

• RF [2]. Robust Fingerprinting (RF) is a CNN-based WF attack that leverages a Traffic Aggregation Matrix (TAM) to capture informative features leaked from Tor traces.

• NetCLR [3]. NetCLR employs both semi-supervised and self-supervised learning to augment network traces.

• Holmes [35]. Holmes leverages temporal and spatial traffic distributions with contrastive learning to identify websites from partial webpage loading traffic.

3) WF Defense Baselines: To make a comprehensive comparison, we select six SOTA WF defense mechanisms as baselines. The defense models are listed as follows:

• FRONT [16]. FRONT is a lightweight defense mechanism by introducing trace-to-trace randomness through the randomized insertion of dummy packets.

• ALERT [19]. ALERT generates adversarial perturbations without requiring knowledge of individual traffic traces and produces user-specific universal perturbations.

• Palette [23]. Palette prevents adversaries from distinguishing among similar websites within a cluster, thereby providing stronger anonymity guarantees.

• GAPDiS [18]. GAPDiS is an adversarial perturbationbased WF defense method.

• FRUGAL [20]. FRUGAL is a traffic obfuscation defense mechanism that minimizes the mutual information between website traffic and webpage labels by strategically injecting dummy packets.

• Adaptive Tamaraw [24]. Adaptive Tamaraw integrates regularization-based defenses with dynamic clustering to adjust defense parameters.

4) Open Science: To support reproducibility and facilitate further research, we will release the implementation later, including trace processing scripts and evaluation frameworks.

We also provide detailed descriptions of dataset construction and experimental settings. The dataset used in this work is publicly available, and we provide detailed preprocessing procedures in the supplementary material. We also report all hyperparameters and implementation details necessary to reproduce the experimental results, as shown in Appendix A.

## B. Performance and Overhead Comparison

1) Closed-world Scenario: We first evaluate the effectiveness and robustness of our proposed defense against four SOTA WF attacks under the closed-world setting using four representative attack models on the DF dataset, which contains 95 website classes with 1,000 traces per class, and the DS-19 dataset, which contains 100 website classes with 100 traces per class. As shown in Table II, all attacks achieve nearperfect performance without defenses, exceeding 98% on the DF dataset and remaining above 90% on the DS-19 dataset. This confirms that the SOTA WF attacks can reliably infer user activity in the absence of effective countermeasures.

From Table II, we can see that SOTA defense models such as FRONT, GAPDiS, and FRUGAL show limited robustness under adversarial training-based attacks. They marginally degrade attack performance, with accuracies still exceeding 90% on the DF dataset and remaining above 80% on the DS-19 dataset. For example, although FRONT introduces no additional packet delay and incurs only moderate bandwidth overhead, it reduces the DF attack model’s accuracy from 98.33% to merely 95.83%, indicating minimal defensive effectiveness against adversarial training-based attacks. The weaker performance of FRUGAL compared with its originally reported results is mainly due to our evaluation setting, where 90% of the defended traces are used for training and 10% for testing, providing the attacker with substantially more training data for adversarial training.

Palette [23] and Adaptive Tamaraw [24] demonstrate stronger resilience by reshaping the trace pattern distribution. Palette reduces attack accuracy by at least 47.52% on the DF dataset and 58.28% on the DS-19 dataset, while Adaptive Tamaraw further improves robustness, achieving reductions of at least 61.67% and 71.58%, respectively. This highlights the advantage of these two defense models in defending against adversarial training-based attacks. However, Adaptive Tamaraw achieves stronger protection at the expense of considerably higher overhead.

In comparison, our approach Chameleon consistently outperforms all baselines across both datasets on four SOTA attack models. Chameleon keeps attack accuracy below 27% across all four attacks on the DF dataset. On average, Chameleon reduces the accuracy of SOTA WF attacks by 76.52% with moderate overhead on the DF dataset. On the DS-19 dataset, Chameleon reduces accuracy as low as 6.40%, corresponding to over 91.10% reduction relative to the undefended baseline (NoDef) with lower time overhead.

Importantly, Chameleon achieves strong defense performance with moderate overhead, incurring 130.60% bandwidth overhead and only 14.51% time overhead on the DF dataset.

TABLE II: Evaluation of overhead and defense against adversarial training-based attacks across six SOTA WF defenses.

<table><tr><td rowspan="3">Dataset Defenses</td><td colspan="6">DF [4]</td><td colspan="6">DS-19 [16]</td></tr><tr><td colspan="2">Overhead (%)</td><td colspan="4">Attack Accuracy (%)</td><td colspan="2">Overhead (%)</td><td colspan="4">Attack Accuracy (%)</td></tr><tr><td>Bandwidth</td><td>Time</td><td>DF</td><td>Var-CNN</td><td>RF</td><td>NetCLR</td><td>Bandwidth</td><td>Time</td><td>DF</td><td>Var-CNN</td><td>RF</td><td>NetCLR</td></tr><tr><td>NoDef</td><td>0.0</td><td>0.0</td><td>98.33</td><td>98.83</td><td>98.93</td><td>98.53</td><td>0.0</td><td>0.0</td><td>97.23</td><td>96.75</td><td>90.94</td><td>97.50</td></tr><tr><td>FRONT</td><td>64.46</td><td>0.0</td><td>95.83 ↓2.50</td><td>98.15 ↓0.68</td><td>98.20 ↓0.73</td><td>95.93 ↓2.60</td><td>31.68</td><td>0.0</td><td>96.38 ↓0.85</td><td>94.78 ↓1.97</td><td>89.17 ↓1.77</td><td>96.50 ↓1.00</td></tr><tr><td>ALERT</td><td>25.03</td><td>201.34</td><td>69.43 ↓28.90</td><td>75.99 ↓22.84</td><td>88.03 ↓10.90</td><td>69.57 ↓28.96</td><td>35.44</td><td>158.23</td><td>57.16 ↓40.07</td><td>69.59 ↓21.16</td><td>74.46 ↓16.48</td><td>71.57 ↓25.96</td></tr><tr><td>Palette</td><td>82.16</td><td>8.18</td><td>37.25 ↓61.08</td><td>45.02 ↓53.81</td><td>51.41 ↓47.52</td><td>31.77 ↓66.76</td><td>75.92</td><td>13.67</td><td>10.73 ↓86.50</td><td>12.38 ↓84.37</td><td>32.66 ↓58.28</td><td>11.22 ↓86.31</td></tr><tr><td>GAPDiS</td><td>17.96</td><td>212.41</td><td>91.87 ↓6.46</td><td>95.17 ↓3.66</td><td>92.38 ↓6.55</td><td>88.23 ↓10.30</td><td>36.77</td><td>171.36</td><td>77.04 ↓20.19</td><td>87.16 ↓9.59</td><td>81.02 ↓9.92</td><td>87.36 ↓10.17</td></tr><tr><td>FRUGAL</td><td>80.00</td><td>0.0</td><td>96.59 ↓1.74</td><td>96.25 ↓2.58</td><td>30.96 ↓67.97</td><td>96.78 ↓1.75</td><td>80.00</td><td>0.0</td><td>95.42 ↓1.81</td><td>94.63 ↓2.12</td><td>11.04 ↓79.90</td><td>95.97 ↓1.53</td></tr><tr><td>Adaptive Tamaraw</td><td>198.23</td><td>36.62</td><td>28.47 ↓67.36</td><td>33.79 ↓65.04</td><td>37.26 ↓61.67</td><td>25.27 ↓73.26</td><td>140.17</td><td>18.01</td><td>13.07 ↓84.16</td><td>14.37 ↓82.38</td><td>19.36 ↓71.58</td><td>12.73 ↓84.77</td></tr><tr><td>Chameleon</td><td>130.60</td><td>14.51</td><td>19.03 ↓79.30</td><td>26.23 ↓72.60</td><td>23.57 ↓75.36</td><td>19.72 ↓76.21</td><td>72.48</td><td>9.97</td><td>7.24 ↓89.99</td><td>6.50 ↓90.25</td><td>6.77 ↓84.17</td><td>6.40 ↓91.10</td></tr></table>

TABLE III: Evaluation of adversarial training effectiveness across defenses using DF [4] datasets in the open-world scenario.

<table><tr><td rowspan="2">Defenses\Attacks</td><td colspan="4">DF</td><td colspan="4">Var-CNN</td><td colspan="4">RF</td><td colspan="4">NetCLR</td></tr><tr><td>TPR (%)</td><td>FPR (%)</td><td>F1</td><td>P (%)</td><td>TPR (%)</td><td>FPR (%)</td><td>F1 (%)</td><td>P (%)</td><td>TPR (%)</td><td>FPR (%)</td><td>F1 (%)</td><td>P (%)</td><td>TPR (%)</td><td>FPR (%)</td><td>F1 (%)</td><td>P (%)</td></tr><tr><td>NoDef</td><td>97.71</td><td>3.34</td><td>98.13</td><td>98.56</td><td>98.25</td><td>1.68</td><td>98.76</td><td>98.22</td><td>93.59</td><td>12.37</td><td>94.11</td><td>94.64</td><td>98.24</td><td>1.62</td><td>98.77</td><td>98.31</td></tr><tr><td>FRONT</td><td>94.37</td><td>8.10</td><td>95.31</td><td>96.29</td><td>97.16</td><td>2.87</td><td>97.91</td><td>98.07</td><td>70.20</td><td>19.87</td><td>78.35</td><td>88.75</td><td>94.34</td><td>4.83</td><td>96.01</td><td>97.73</td></tr><tr><td>ALERT</td><td>68.86</td><td>3.19</td><td>80.75</td><td>97.35</td><td>78.70</td><td>2.46</td><td>86.82</td><td>95.87</td><td>81.58</td><td>3.67</td><td>88.07</td><td>94.75</td><td>69.87</td><td>2.27</td><td>81.20</td><td>96.05</td></tr><tr><td>Palette</td><td>30.92</td><td>42.01</td><td>41.52</td><td>62.98</td><td>36.87</td><td>38.47</td><td>48.09</td><td>69.13</td><td>42.33</td><td>31.26</td><td>54.36</td><td>75.94</td><td>24.02</td><td>43.30</td><td>33.90</td><td>57.76</td></tr><tr><td>GAPDiS</td><td>97.54</td><td>3.77</td><td>97.96</td><td>98.39</td><td>97.16</td><td>3.04</td><td>97.91</td><td>98.17</td><td>9.58</td><td>72.67</td><td>13.62</td><td>23.31</td><td>97.38</td><td>2.72</td><td>98.09</td><td>98.51</td></tr><tr><td>FRUGAL</td><td>96.22</td><td>6.29</td><td>96.74</td><td>97.11</td><td>95.54</td><td>4.87</td><td>96.69</td><td>97.98</td><td>9.04</td><td>45.42</td><td>14.07</td><td>80.82</td><td>95.70</td><td>4.25</td><td>96.90</td><td>94.90</td></tr><tr><td>Adaptive Tamaraw</td><td>11.06</td><td>5.84</td><td>18.99</td><td>66.88</td><td>16.05</td><td>2.96</td><td>27.08</td><td>78.86</td><td>19.01</td><td>1.97</td><td>31.79</td><td>86.03</td><td>13.28</td><td>1.43</td><td>23.11</td><td>88.43</td></tr><tr><td>Chameleon</td><td>13.34</td><td>7.27</td><td>22.92</td><td>54.31</td><td>8.45</td><td>11.77</td><td>14.89</td><td>31.29</td><td>11.04</td><td>5.65</td><td>19.47</td><td>17.91</td><td>17.72</td><td>10.40</td><td>26.16</td><td>49.79</td></tr></table>

We found that the DF dataset exhibits substantial variation in trace length across classes, which leads Chameleon to select highly similar candidate traces at the cost of increased padding and higher overhead under imperfect alignment. In contrast, Chameleon achieves 72.48% bandwidth with 9.97% time overhead on the DS-19 dataset, offering a significantly better accuracy–efficiency trade-off than prior defenses. The DS-19 dataset presents more uniform trace lengths, enabling more efficient morphing with even reduced overhead. Overall, these results demonstrate that Chameleon provides substantially stronger and more stable robustness against adversarially trained WF attacks while maintaining practical deployment overhead.

2) Open-world Scenario: In an open-world scenario, the adversary can only know and monitor a subset of the websites accessed by the user. Traffic traces collected from monitored websites are used to train a classifier that determines whether a given trace corresponds to one of the monitored sites. This setting is inherently more challenging for an adversary to execute a WF attack. To simulate the open-world scenario, for the DF dataset, we construct the monitored set using all websites in the closed-world dataset, while treating all websites in the open-world dataset as unmonitored. Specifically, we randomly sample 900 traces per monitored website and 40,716 traces from the unmonitored set. Similarly, for the DS-19 dataset, we sample 90 traces per monitored website and 10,000 traces from the unmonitored set. The two datasets are partitioned into training and validation subsets with a 9:1 ratio.

Following the evaluation setting in Palette [23] and GAPDiS [18], we report performance using True Positive Rate (TPR), False Positive Rate (FPR), and F1-score as shown in Table III. We compare defenses under four SOTA attacks on the DF dataset. Without defenses, DF, Var-CNN, RF, and NetCLR achieve high TPR and F1-scores, demonstrating the strong effectiveness of these four website fingerprinting attacks even in the open-world setting. Defenses such as FRONT remain vulnerable to adversarial training-based attacks in the open-world setting, with TPRs exceeding 90% in most cases. Similarly, GAPDiS exhibits inconsistent behavior, achieving low TPR against RF at 9.58% but remaining ineffective against other attacks. ALERT reduces TPR to a moderate range, 68.86% to 81.58%, but still falls short of providing strong protection. Palette significantly lowers TPR in some cases, such as 24.02% under NetCLR. However, Palette achieves the performance at the cost of extremely high FPR, up to 43.30%, which severely limits its practicality.

In contrast, Chameleon maintains relatively moderate FPR values, 5.65% to 11.77%, while achieving low TPR, resulting in a more favorable balance as reflected by its F1-scores. FRUGAL achieves a particularly low TPR of 9.04% against RF. This result is partly attributable to the available FRUGAL defended traces containing only packet-direction information without timing information, whereas RF relies substantially on timing-related features. However, DF, Var-CNN, and NetCLR still achieve TPRs above 90% against FRUGAL, indicating that its protection remains limited against adversarially trained attacks. Adaptive Tamaraw achieves low TPRs of 11.06% under DF and 13.28% under NetCLR. By contrast, although Adaptive Tamaraw attains slightly lower FPR in some cases, 1.43% under NetCLR, Chameleon achieves more stable performance across different attacks. Overall, our design, Chameleon, provides competitive performance while maintaining a more balanced error profile.

![](images/b2063fac340f3407cf5c099672446de88058b7c09d8844afb5a5a92a1a1ae6ff.jpg)

![](images/49771f88b92a72c6de1ea619cf3bd8eeb993dba2ae94acdfce818fce800396bb.jpg)

![](images/42fa68fac473e19d380b2541597befd3e3b8ac5d3e274faba9befb15cda2db5e.jpg)

![](images/b20531a24ef7284bcd0618e89446b612acb5165fe2e761215666c1bbbf2d6b80.jpg)  
Fig. 8: ROC curves and AUC scores of defense methods on the DS-19 dataset under the open-world scenario.

TABLE IV: A comprehensive comparison of AT-resistant defenses against DAAE-based attacks on the GTT23 dataset.

<table><tr><td rowspan="2">Defenses\Attacks</td><td colspan="3">DF</td><td colspan="3">Var-CNN</td><td colspan="3">RF</td><td colspan="3">NetCLR</td></tr><tr><td>P (%)</td><td>R (%)</td><td>F1 (%)</td><td>P (%)</td><td>R (%)</td><td>F1 (%)</td><td>P (%)</td><td>R (%)</td><td>F1 (%)</td><td>P (%)</td><td>R (%)</td><td>F1 (%)</td></tr><tr><td>NoDef</td><td>93.82</td><td>93.20</td><td>93.13</td><td>93.21</td><td>91.80</td><td>91.89</td><td>94.86</td><td>92.20</td><td>94.01</td><td>93.76</td><td>93.00</td><td>93.03</td></tr><tr><td> $\text{Palette}_{\text{def}}$ </td><td>10.57</td><td>8.30</td><td>7.76</td><td>27.30</td><td>21.00</td><td>19.80</td><td>31.60</td><td>24.50</td><td>23.59</td><td>10.22</td><td>8.90</td><td>7.92</td></tr><tr><td> $\text{Palette}_{\text{rec}}$ </td><td>86.90</td><td>83.00</td><td>83.67</td><td>86.38</td><td>82.30</td><td>82.72</td><td>80.64</td><td>67.90</td><td>70.30</td><td>81.99</td><td>80.50</td><td>80.55</td></tr><tr><td>Adaptive Tamaraw $_{\text{def}}$ </td><td>17.47</td><td>13.79</td><td>13.58</td><td>14.05</td><td>13.37</td><td>13.19</td><td>34.97</td><td>30.33</td><td>28.35</td><td>14.76</td><td>13.41</td><td>13.16</td></tr><tr><td>Adaptive Tamaraw $_{\text{rec}}$ </td><td>87.38</td><td>86.78</td><td>86.44</td><td>88.74</td><td>87.98</td><td>87.85</td><td>89.82</td><td>88.65</td><td>88.22</td><td>85.79</td><td>84.96</td><td>84.11</td></tr><tr><td>Chameleon $_{\text{def}}$ </td><td>8.92</td><td>7.67</td><td>6.42</td><td>12.26</td><td>12.44</td><td>9.37</td><td>20.33</td><td>19.78</td><td>16.23</td><td>7.78</td><td>6.34</td><td>5.97</td></tr><tr><td> $\text{Chameleon}_{\text{rec}}$ </td><td>26.13</td><td>26.41</td><td>23.86</td><td>27.92</td><td>27.91</td><td>22.45</td><td>40.68</td><td>34.97</td><td>35.19</td><td>25.13</td><td>25.28</td><td>24.02</td></tr></table>

In addition, we show the ROC curves of four SOTA WF attacks under different defense mechanisms in Figure 8. Similar to the observations on the DF dataset, the WF attack models, such as DF, Var-CNN, and NetCLR, achieve high AUC values in the absence of defenses, indicating their strong discriminative capability in the open-world setting. Although the RF attack yields a comparatively lower AUC of 88.3%, it still demonstrates effectiveness and remains a competitive WF attack. From Figure 8, we can see Palette and Adaptive Tamaraw exhibit relatively strong defense performance. However, both methods still leave room for improvement. Our designed method, Chameleon, further reduces the attack effectiveness, achieving an AUC as low as 53.5% against the DF attack. This result highlights the advantage of Chameleon in significantly degrading the adversary’s WF attack capability.

## C. Evaluation of Defense against DAAE-based Attacks

DAAE-based attack is designed for scenarios in which adversarial training-based WF cannot attack a defense. To evaluate the resistance of Chameleon to DAAE, we compare it with two SOTA defenses, Palette and Adaptive Tamaraw, which demonstrate strong resistance to adversarial training on the recent GTT23 [22] dataset. We first use DAAE to reconstruct defended traces and then perform WF attacks using DF, Var-CNN, RF, and NetCLR implemented in the WFLib project [36] to evaluate precision (P), recall (R), and F1- score (F1). Table IV presents the performance of DAAEbased attacks against defenses that are resistant to adversarial training on the GTT23 dataset. Chameleon provides substantially stronger protection than the existing defenses, particularly when the attacker is trained on defended traffic. For the defense-trained setting $C h a m e l e o n _ { d e f }$ Chameleon achieves F1-scores of 6.42%, 9.37%, 16.23%, and 5.97% against DF, Var-CNN, RF, and NetCLR, respectively. These results are consistently lower than those of $P a l e t t e _ { d e f }$ and Adaptive $T a m a r a w _ { d e f }$ , demonstrating that Chameleon is robust and efficient in defending against adversarial trainingbased attacks.

After performing the DAAE-based WF attacks, the results further highlight the robustness of Chameleon. Under $C h a m e l e o n _ { r e c } ,$ the F1-score of the DAAE-based DF attack only increases from 6.42% to 23.86%, while the same attack increases from 7.76% to 83.67% under the $\begin{array} { r } { P a l e t t e _ { r e c } } \end{array}$ defense. In particular, Chameleon<sub>rec</sub> limits the strongest attack, RF, to an F1-score of only 35.19%, while the corresponding scores for $\begin{array} { r } { P a l e t t e _ { r e c } } \end{array}$ and Adaptive $T a m a r a w _ { r e c }$ reach 70.30% and 88.22%, respectively. These results indicate that Chameleon remains robust and effective even when the attacker can reconstruct or retrain on defended traffic, confirming that its randomized morphing strategy provides stronger resistance to defense-aware attacks.

## D. Early-stage Measurement

In this section, we evaluate whether early-stage information used in Chameleon can leak sufficient trace information for website identification. To evaluate this potential leakage, we employ Holmes [35], an early-stage WF attack that exploits the temporal and spatial characteristics of partially observed traffic under the GTT23 dataset. Following the evaluation methodology of Holmes, we evaluate the first 20%, 30%, 40%, 50%, and 60% of the loaded packets and compare Chameleon with Palette and Adaptive Tamaraw. For all defenses, we set the trace length to 5,000 packets. As shown in Table V, NoDef exhibits increasing attack performance as more traffic is observed, with the F1-score rising from 31.07% at 20% to 57.61% at 60% loaded traffic. In contrast, all three defenses substantially suppress Holmes, demonstrating that traffic regularization can effectively reduce the information available during the early stages of a connection.

TABLE V: The early-stage traffic evaluation through Holmes WF attack [35] under the GTT23 [22] dataset.

<table><tr><td rowspan="2">Defenses</td><td colspan="3">20% loaded</td><td colspan="3">30% loaded</td><td colspan="3">40% loaded</td><td colspan="3">50% loaded</td><td colspan="3">60% loaded</td></tr><tr><td>P (%)</td><td>R (%)</td><td>F1 (%)</td><td>P (%)</td><td>R (%)</td><td>F1 (%)</td><td>P (%)</td><td>R (%)</td><td>F1 (%)</td><td>P (%)</td><td>R (%)</td><td>F1 (%)</td><td>P (%)</td><td>R (%)</td><td>F1 (%)</td></tr><tr><td>NoDef</td><td>54.45</td><td>26.85</td><td>31.07</td><td>61.12</td><td>39.91</td><td>45.24</td><td>64.03</td><td>44.09</td><td>49.34</td><td>65.50</td><td>59.44</td><td>60.44</td><td>66.03</td><td>54.43</td><td>57.61</td></tr><tr><td>Palette</td><td>13.87</td><td>7.94</td><td>7.83</td><td>15.29</td><td>9.82</td><td>9.70</td><td>17.85</td><td>11.42</td><td>11.34</td><td>18.53</td><td>13.56</td><td>13.53</td><td>19.25</td><td>16.68</td><td>16.43</td></tr><tr><td>Adaptive Tamaraw</td><td>15.38</td><td>8.21</td><td>7.72</td><td>16.57</td><td>11.75</td><td>11.11</td><td>17.42</td><td>15.73</td><td>14.19</td><td>19.33</td><td>17.19</td><td>16.76</td><td>21.04</td><td>18.39</td><td>17.49</td></tr><tr><td>Chameleon</td><td>18.95</td><td>7.64</td><td>8.06</td><td>17.75</td><td>9.48</td><td>10.02</td><td>18.26</td><td>10.75</td><td>11.25</td><td>18.83</td><td>12.72</td><td>13.01</td><td>18.88</td><td>15.06</td><td>14.67</td></tr></table>

TABLE VI: Evaluation of performance and overhead trade-offs for Chameleon across full trace morphing, trade-off trace morphing, and trace mutation on the DF [4] and DS-19 [16] datasets in the closed-world scenario.

<table><tr><td>Dataset</td><td colspan="6">DF [4]</td><td colspan="6">DS-19 [16]</td></tr><tr><td rowspan="2">Defenses</td><td colspan="2">Overhead (%)</td><td colspan="4">Attack Accuracy (%)</td><td colspan="2">Overhead (%)</td><td colspan="4">Attack Accuracy (%)</td></tr><tr><td>Bandwidth</td><td>Time</td><td>DF</td><td>Var-CNN</td><td>RF</td><td>NetCLR</td><td>Bandwidth</td><td>Time</td><td>DF</td><td>Var-CNN</td><td>RF</td><td>NetCLR</td></tr><tr><td>Chameleon (Lightweight)</td><td>130.60</td><td>14.51</td><td>19.03</td><td>26.23</td><td>23.57</td><td>19.72</td><td>72.48</td><td>9.97</td><td>7.24</td><td>6.50</td><td>6.77</td><td>6.40</td></tr><tr><td>Chameleon (Medium)</td><td>172.02</td><td>17.26</td><td>16.68</td><td>18.31</td><td>17.69</td><td>14.61</td><td>78.82</td><td>11.70</td><td>6.44</td><td>5.75</td><td>6.32</td><td>5.95</td></tr><tr><td>Chameleon (Heavy)</td><td>260.46</td><td>48.50</td><td>10.49</td><td>9.84</td><td>12.94</td><td>9.73</td><td>93.42</td><td>14.50</td><td>4.17</td><td>2.89</td><td>4.07</td><td>3.18</td></tr></table>

Chameleon maintains consistently low attack performance across all observation levels, with F1-scores of 8.06%, 10.02%, 11.25%, 13.01%, and 14.67% from 20% to 60% loaded traffic, respectively. Even at 60% loaded traffic, Holmes achieves only 14.67% F1 against Chameleon, representing a 74.5% reduction compared with NoDef. Moreover, Chameleon achieves lower recall and F1-scores than both Palette and Adaptive Tamaraw at 50% and 60% loaded traffic, indicating that its prefix-based trace selection does not expose additional discriminative information as more of the trace becomes available. These results suggest that the partial traffic prefix used for synchronization does not compromise the protection of Chameleon, and that its many-to-many morphing strategy remains effective against early-stage WF attacks.

## E. Ablation Study

1) Traffic Morphing Strategy: We perform a trade-off evaluation between three strategies: full trace morphing (Heavy), morphing trace cut-off (Medium), and trace mutation (Lightweight), as discussed in Section IV-C. Table VI presents a trade-off experiment study of Chameleon under three configurations, lightweight, medium, and heavy, capturing different trade-offs between defense strength and system overhead. Under the DF dataset, the trace mutation version (Lightweight) of Chameleon already achieves substantial protection, reducing attack accuracy to 19.03%, 26.23%, 23.57%, and 19.72% against DF, Var-CNN, RF, and NetCLR, respectively. Meanwhile, the lightweight version of Chameleon achieves moderate overhead on 130.60% bandwidth and 14.51% time. The medium version of Chameleon further improves robustness, lowering attack accuracy across all models, such as 16.68% for DF and 14.61% for NetCLR, with a moderate increase in overhead. The heavy version of Chameleon provides the strongest defense, reducing attack accuracy to as low as 9.73% to 12.94%, but has a significantly higher overhead on 260.46% bandwidth and 48.50% latency.

These results demonstrate that Chameleon offers a flexible design space: practitioners can select an appropriate configuration depending on their desired balance between security and overhead. In particular, the lightweight version of Chameleon already provides strong protection with reasonable cost, while the heavy variant achieves near-minimal attack accuracy for high-security scenarios.

2) Key Hyperparameter Evaluation: We evaluate the key hyperparameter ρ, which controls the top m website traces for the candidate pool. The selection ratio ρ governs the granularity of intra-class diversity and inter-class separability by controlling the number of website traces in the candidate pool. We investigate the impact of the key parameter ρ on Chameleon under four SOTA WF attacks in the closed-world scenario. Intuitively, varying $\rho$ directly affects both the defense performance and the associated overhead.

![](images/7a9fa37d4ab09cca3984c989bcf82d3dca0aa65dac6b7575b168b4b404a3a9db.jpg)  
(a) Overhead on the DF.

![](images/fa3554126c3b1019e7458611377ab2ca2056b3be5138684f5ed66095e7c41bcd.jpg)  
(b) Accuracy on the DF.  
Fig. 9: The overhead and performance of Chameleon with different values of selection ratio $\rho$ on the DF dataset.

TABLE VII: Robustness evaluation of Chameleon against randomization-aware training on the GTT23 dataset.

<table><tr><td rowspan="2">Number</td><td colspan="4">Attack Accuracy (%)</td></tr><tr><td>DF</td><td>Var-CNN</td><td>RF</td><td>NetCLR</td></tr><tr><td>K=1</td><td>7.10</td><td>6.72</td><td>6.49</td><td>5.84</td></tr><tr><td>K=5</td><td>13.57</td><td>15.04</td><td>20.33</td><td>14.05</td></tr><tr><td>K=10</td><td>15.93</td><td>17.63</td><td>26.42</td><td>15.99</td></tr><tr><td>K=15</td><td>17.02</td><td>19.12</td><td>29.29</td><td>16.91</td></tr><tr><td>K=20</td><td>17.50</td><td>18.82</td><td>31.06</td><td>17.04</td></tr></table>

Figure 9 illustrates the overhead and performance of Chameleon across different values of $\rho$ on the DF dataset. As $\rho$ increases, both bandwidth and time overheads grow, while the attack accuracy of SOTA WF models decreases. This trend arises because a larger $\rho$ enhances intra-class diversity and reduces inter-class separability, thereby making classification more difficult for the attacker. We observe consistent behavior on the DS-19 dataset: increasing $\rho$ leads to higher overhead but lower attack accuracy. To balance efficiency and robustness, we select $\rho = 0 . 2$ in our experiments.

3) Robustness to Randomization-Aware Training: Since Chameleon relies on randomized traffic transformations, evaluating it using only one defended trace per training instance may overestimate its effectiveness [37]. To provide a stronger evaluation, we consider an adaptive attacker that augments its training set with multiple independently randomized defended traces generated from each original training trace. Specifically, for each training trace, we generate 20 defended variants using independent random seeds, where $K \in \{ 1 , 5 , 1 0 , 1 5 , 2 0 \}$ . We then train the attacker on the resulting augmented dataset while keeping the test set fixed and independently randomized. Table VII evaluates Chameleon’s robustness against randomization-aware training on the GTT23 dataset. We augment each original training trace with multiple independently randomized defended traces, increasing the number of replicates from $K = 1$ to $K = 2 0$ . As expected, exposing the attacker to more randomized realizations improves attack accuracy across all four WF models, indicating that the attacker can gradually learn features that are invariant to Chameleon’s randomization. Nevertheless, the attack accuracy remains relatively low even with 20 replicates. Specifically, DF, Var-CNN,

![](images/777624f399e003839c0ee5b685fe8b7417910fce0e6ae90d2c43a13aa240e4cd.jpg)  
Fig. 10: Visualization of Injectivity Boundaries Evaluation.

RF, and NetCLR achieve only 17.50%, 18.82%, 31.06%, and 17.04% accuracy at $K \ = \ 2 0 ,$ respectively, compared with 7.10%, 6.72%, 6.49%, and 5.84% at $K = 1$ . Although RF benefits the most from increased training diversity, its accuracy remains substantially below the closed-world baseline of 100 classes, while the other three attacks remain below 20%. These results demonstrate that Chameleon’s robustness and effectiveness are not solely attributable to the limited number of randomized realizations observed during training and that its protection remains effective against attackers explicitly trained on multiple independently randomized traces.

4) Evaluation of Injectivity Boundaries and Candidate Trace: In this work, we introduce a defense model based on a many-to-many mapping mechanism and establish a corresponding security bound for Chameleon in Appendix H. Evaluating this upper bound is essential for understanding how the size of input website traces impacts adversarial robustness under a fixed-size candidate pool.

We empirically study the injectivity boundary of Chameleon using a fixed candidate pool derived from the DS-19 dataset with a selection ratio $\rho = 0 . 2 \ ( 8 3 3$ website traces). As input, we use the DF dataset $( 9 5 \times 1 0 0 0$ website traces) to evaluate this boundary. The ratio between the input website traces and the website candidates is 95,000:833. We define I as the number of input traces per class from the DF dataset, which models varying levels of trace availability for morphing. Increasing I effectively enlarges the feasible injection space of the candidate pool, thereby enabling a finer-grained analysis of the injectivity boundary.

As shown in Figure 10, the sensitivity to the injectivity boundary varies across attack models, with Var-CNN exhibiting the most pronounced increase in accuracy, followed by RF and NetCLR, while DF remains comparatively more stable. Even under the input traces $I = 1 0 0 0$ , the worst-case WF attack accuracy remains below 35% across all models, indicating that the defense remains within a reasonable range for defending against adversarial training-based attacks. Furthermore, these results demonstrate that the effectiveness of our defense is not constrained by the candidate-pool dataset. Instead, the candidate pool can be constructed from arbitrary real-world website traces, enabling the defense to generalize beyond a predefined set of websites.

## F. Real-world Performance

To estimate the overhead and performance of Chameleon in the real-world, we implement Chameleon within WFDef-

TABLE VIII: Evaluation of real-world performance.

<table><tr><td rowspan="2">Defenses</td><td colspan="2">Overhead (%)</td><td colspan="4">Attack Accuracy (%)</td></tr><tr><td>Bandwidth</td><td>Time</td><td>DF</td><td>Var-CNN</td><td>RF</td><td>NetCLR</td></tr><tr><td>NoDef</td><td>0.0</td><td>0.0</td><td>90.35</td><td>88.20</td><td>91.52</td><td>89.58</td></tr><tr><td>FRONT</td><td>97.04</td><td>0.0</td><td>56.16</td><td>61.50</td><td>78.64</td><td>58.39</td></tr><tr><td>RegulaTor</td><td>75.08</td><td>125.53</td><td>18.74</td><td>22.72</td><td>31.06</td><td>13.53</td></tr><tr><td>Palette</td><td>84.40</td><td>28.91</td><td>10.30</td><td>12.95</td><td>42.25</td><td>9.31</td></tr><tr><td>Chameleon</td><td>91.47</td><td>16.25</td><td>7.17</td><td>9.33</td><td>17.45</td><td>6.51</td></tr></table>

Proxy [27] as a pluggable transport based on the Tor Pluggable Transport (PT) bridge [26]. Our deployment uses two workstations: one hosts the bridge (PT server), while the other runs five Docker-based clients that visit websites in parallel. Each client connects to the PT server under a bandwidth cap of 120 Mbps. The bridge is provisioned with 2 CPU cores and 2 GB RAM, while the client machine has 8 CPU cores and 16 GB RAM; both run Ubuntu 24.04.4 LTS. We automate browsing using TBSelenium [38] with Tor Browser version 15.0. To ensure full page loads, each visit is limited to 80 seconds, followed by an additional 5-second dwell time to avoid overlap with subsequent traffic. After each visit, the browser is restarted, and a Signal.NEWNYM command is issued to enforce a fresh circuit.

Real-world evaluation poses greater challenges for WF defenses due to network variability and practical deployment constraints. Following prior work [23], [27], we collect a realworld defended dataset by capturing traffic between the PT client and PT server. Similar to prior studies [23], we select websites from the Tranco [39] list snapshot dated July 1, 2025. From the top 1,000 entries, we remove inaccessible and duplicate URLs that resolve to identical pages, and retain the first 100 sites as the monitored set. Multiple clients visit these sites in randomized order. We aggregate all traces and filter outliers following a prior approach [40], ensuring that each monitored website is represented by at least 100 instances.

Table VIII shows a comprehensive comparison of the realworld performance and overhead between defense mechanisms such as FRONT, RegulaTor, Palette, and Chameleon. We observe that Chameleon achieves a suitable trade-off between effectiveness and efficiency, reducing attack accuracy to 7.17% for DF, 9.33% for Var-CNN, 17.45% for RF, and 6.51% for NetCLR, while incurring a moderate bandwidth overhead of 91.47% and a relatively low time overhead of 16.25%. In contrast, FRONT provides partial robustness in the real-world, substantially reducing the accuracy of attacks such as DF, Var-CNN, and NetCLR but remaining ineffective against RF, which still achieves 78.64% accuracy. RegulaTor exhibits a clear discrepancy between effectiveness and efficiency, introducing a large time overhead of 125.53% while still allowing non-trivial attack success. In particular, the RF attack still reaches 31.06% accuracy under RegulaTor defense. Similarly, Palette achieves strong reductions for DF, Var-CNN, and NetCLR but remains vulnerable to RF with 42.25% accuracy and incurs higher time overhead than Chameleon, reflecting a less favorable efficiency–effectiveness balance. These results demonstrate that Chameleon achieves the lowest attack accuracy across all four evaluated attacks while maintaining competitive overhead.

## VI. RELATED WORK

WF defenses aim to obfuscate or alter traffic patterns by inserting dummy packets or increasing packet timing delays that reduce WF performance. However, the existing WF defense methods inevitably introduce new artifacts, which can be exploited by WF attack models. For example, FRONT [16] obfuscates the burst patterns by adding random dummy packets. However, FRONT continues to leak trace information, which remains vulnerable to DL-based WF attacks. TrafficSliver [41] mitigates the observable traffic patterns by splitting traffic across multiple entry relays. However, the DL–based WF attacks can still exploit timing, burst structure, and directional patterns left by TrafficSliver. As a result, these defenses exhibit limited robustness against adaptive adversaries, particularly those employing adversarial retraining.

Another main defense design is regularization-based, which reshapes website traffic traces into more uniform patterns, thereby providing rigorous bounds on an adversary’s ability to classify webpages. Walkie-Talkie [14] maps the original website trace to another trace, effectively creating collisions in which at least two traces share identical patterns. However, Walkie-Talkie does not obfuscate fine-grained timing information, making this defense mechanism vulnerable to advanced DL–based website fingerprinting attacks [3], [5], [11]. Additionally, Walkie-Talkie requires the browser to operate in half-duplex mode, which means the client must wait for all responses before issuing new requests. Similarly, Palette [23] incurs significant buffering overhead to support large-scale clustering and traffic shaping. Adaptive Tamaraw [24] creates an adaptive WF defense framework by integrating Tamaraw [12] defense with dynamic clustering to adjust defense parameters in real time. However, Adaptive Tamaraw can also incur substantial bandwidth and latency overhead as it dynamically adapts its defense parameters [24].

## VII. CONCLUSION

In this work, we show that existing WF defenses can remain vulnerable to defense-aware attacks, even when they are robust against adversarial training. To address this problem, we present Chameleon, a deployable WF defense based on manyto-many randomized traffic morphing. Chameleon combines diverse shared morphing targets, radix-trie-based synchronization, and trace mutation to disrupt learnable defense patterns while controlling overhead. Across closed-world, openworld, DAAE-based, randomization-aware, early-stage, and real-world evaluations, Chameleon provides stronger protection than existing defenses. These results demonstrate that eliminating defense-induced artifacts is a promising direction for building robust website fingerprinting defense.

## ACKNOWLEDGEMENT

This work was conducted while Dr. Yao Liu was at the University of South Florida (USF).

## ETHICAL CONSIDERATIONS

During the study, we followed the guidelines of the Tor Research Safety Board [42]. All traffic was collected from browsing sessions initiated by our own clients, without involving real Tor user traffic or disrupting the Tor network. While Chameleon is designed to protect web-browsing privacy, we acknowledge that its traffic obfuscation techniques could potentially be misused to evade legitimate network monitoring, such as intrusion detection and abuse mitigation.

## REFERENCES

[1] D. Goldschlag, M. Reed, and P. Syverson, “Onion routing,” Communications of the ACM, vol. 42, no. 2, pp. 39–41, 1999.

[2] M. Shen, K. Ji, Z. Gao, Q. Li, L. Zhu, and K. Xu, “Subverting website fingerprinting defenses with robust traffic representation,” in 32nd USENIX Security Symposium, USENIX Security 2023, August 9-11, 2023, J. A. Calandrino and C. Troncoso, Eds. Anaheim, CA, USA: USENIX Association, 2023, pp. 607–624. [Online]. Available: https: //www.usenix.org/conference/usenixsecurity23/presentation/shen-meng

[3] A. Bahramali, A. Bozorgi, and A. Houmansadr, “Realistic website fingerprinting by augmenting network traces,” in Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security, CCS 2023, November 26-30, 2023, W. Meng, C. D. Jensen, C. Cremers, and E. Kirda, Eds. Copenhagen, Denmark: ACM, 2023, pp. 1035–1049. [Online]. Available: https://doi.org/10.1145/3576915.36 16639

[4] P. Sirinam, M. Imani, M. Juarez, and M. Wright, “Deep fingerprinting: Undermining website fingerprinting defenses with deep learning,” in Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security, CCS 2018, October 15-19, 2018, D. Lie, M. Mannan, M. Backes, and X. Wang, Eds. Toronto, ON, Canada: ACM, 2018, pp. 1928–1943. [Online]. Available: https://doi.org/10.1145/3243734.3243768

[5] S. Bhat, D. Lu, A. Kwon, and S. Devadas, “Var-cnn: A data-efficient website fingerprinting attack based on deep learning,” Proc. Priv. Enhancing Technol., vol. 2019, no. 4, pp. 292–310, 2019. [Online]. Available: https://doi.org/10.2478/popets-2019-0070

[6] T. Wang and I. Goldberg, “On realistically attacking tor with website fingerprinting,” Proc. Priv. Enhancing Technol., vol. 2016, no. 4, pp. 21– 36, 2016. [Online]. Available: https://doi.org/10.1515/popets-2016-0027

[7] K. P. Dyer, S. E. Coull, T. Ristenpart, and T. Shrimpton, “Peek-a-boo, I still see you: Why efficient traffic analysis countermeasures fail,” in IEEE Symposium on Security and Privacy, SP 2012, 21-23 May 2012. San Francisco, California, USA: IEEE Computer Society, 2012, pp. 332–346. [Online]. Available: https://doi.org/10.1109/SP.2012.28

[8] T. Wang, X. Cai, R. Nithyanand, R. Johnson, and I. Goldberg, “Effective attacks and provable defenses for website fingerprinting,” in Proceedings of the 23rd USENIX Security Symposium, August 20-22, 2014, K. Fu and J. Jung, Eds. San Diego, CA, USA: USENIX Association, 2014, pp. 143–157. [Online]. Available: https://www.usenix.org/conference/us enixsecurity14/technical-sessions/presentation/wang tao

[9] A. Kwon, M. AlSabah, D. Lazar, M. Dacier, and S. Devadas, “Circuit fingerprinting attacks: Passive deanonymization of tor hidden services,” in 24th USENIX Security Symposium, USENIX Security 15, August 12-14, 2015, J. Jung and T. Holz, Eds. Washington, D.C., USA: USENIX Association, 2015, pp. 287–302. [Online]. Available: https://www.usenix.org/conference/usenixsecurity15/technical-sessions/ presentation/kwon

[10] X. Zhao, X. Deng, Q. Li, Y. Liu, Z. Liu, K. Sun, and K. Xu, “Towards fine-grained webpage fingerprinting at scale,” in Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security, CCS 2024, October 14-18, 2024, B. Luo, X. Liao, J. Xu, E. Kirda, and D. Lie, Eds. Salt Lake City, UT, USA: ACM, 2024, pp. 423–436. [Online]. Available: https://doi.org/10.1145/3658644.3690211

[11] M. S. Rahman, P. Sirinam, N. Mathews, K. G. Gangadhara, and M. Wright, “Tik-tok: The utility of packet timing in website fingerprinting attacks,” Proc. Priv. Enhancing Technol., vol. 2020, no. 3, pp. 5–24, 2020. [Online]. Available: https://doi.org/10.2478/pope ts-2020-0043

[12] X. Cai, R. Nithyanand, T. Wang, R. Johnson, and I. Goldberg, “A systematic approach to developing and evaluating website fingerprinting defenses,” in Proceedings of the 2014 ACM SIGSAC Conference on Computer and Communications Security, November 3-7, 2014, G. Ahn, M. Yung, and N. Li, Eds. Scottsdale, AZ, USA: ACM, 2014, pp. 227–238. [Online]. Available: https://doi.org/10.1145/2660267.2660362

[13] M. Juarez, M. Imani, M. Perry, C. D´ıaz, and M. Wright, “Toward an efficient website fingerprinting defense,” in Computer Security - ESORICS 2016 - 21st European Symposium on Research in Computer Security, September 26-30, 2016, Proceedings, Part I, ser. Lecture Notes in Computer Science, I. G. Askoxylakis, S. Ioannidis, S. K. Katsikas, and C. Meadows, Eds., vol. 9878. Heraklion, Greece: Springer, 2016, pp. 27–46. [Online]. Available: https://doi.org/10.1007/978-3-319-45744-4 2

[14] T. Wang and I. Goldberg, “Walkie-talkie: An efficient defense against passive website fingerprinting attacks,” in 26th USENIX Security Symposium, USENIX Security 2017, August 16-18, 2017, E. Kirda and T. Ristenpart, Eds. Vancouver, BC, Canada: USENIX Association, 2017, pp. 1375–1390. [Online]. Available: https://www.usenix.org/con ference/usenixsecurity17/technical-sessions/presentation/wang-tao

[15] A. Panchenko, L. Niessen, A. Zinnen, and T. Engel, “Website fingerprinting in onion routing based anonymization networks,” in Proceedings of the 10th annual ACM workshop on Privacy in the electronic society, WPES 2011, October 17, 2011, Y. Chen and J. Vaidya, Eds. Chicago, IL, USA: ACM, 2011, pp. 103–114. [Online]. Available: https://doi.org/10.1145/2046556.2046570

[16] J. Gong and T. Wang, “Zero-delay lightweight defenses against website fingerprinting,” in 29th USENIX Security Symposium, USENIX Security 2020, August 12-14, 2020, S. Capkun and F. Roesner, Eds. Boston, MA, USA: USENIX Association, 2020, pp. 717–734. [Online]. Available: https://www.usenix.org/conference/usenixsecurity20/presentation/gong

[17] D. Li, Y. Zhu, M. Chen, and J. Wang, “Minipatch: Undermining dnn-based website fingerprinting with adversarial patches,” IEEE Trans. Inf. Forensics Secur., vol. 17, pp. 2437–2451, 2022. [Online]. Available: https://doi.org/10.1109/TIFS.2022.3186743

[18] R. Xie, K. Xie, P. Zhao, J. He, X. Zeng, J. Wen, Y. Xie, W. Liang, and G. Xie, “Gapdis: Gradient-assisted perturbation design via sequence editing for website fingerprinting defense,” in Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security, CCS 2025, October 13-17, 2025, C. Huang, J. Chen, S. Shieh, D. Lie, and V. Cortier, Eds. Taipei, Taiwan: ACM, 2025, pp. 3012–3026. [Online]. Available: https://doi.org/10.1145/3719027.3765084

[19] L. Qiao, B. Wu, H. Li, C. Gao, W. Yuan, and X. Luo, “Trace-agnostic and adversarial training-resilient website fingerprinting defense,” in IEEE INFOCOM 2024 - IEEE Conference on Computer Communications, May 20-23, 2024. Vancouver, BC, Canada: IEEE, 2024, pp. 211–220. [Online]. Available: https://doi.org/10.1109/INFO COM52122.2024.10621205

[20] R. Wang, Z. Ling, G. Liu, S. Li, J. Luo, and X. Fu, “Cease at the ultimate goodness: Towards efficient website fingerprinting defense via iterative mutual information minimization,” in 33rd Annual Network and Distributed System Security Symposium, NDSS 2026, February 23-27, 2026. San Diego, California, USA: The Internet Society, 2026. [Online]. Available: https://www.ndss-symposium.org/ndss-paper/cease -at-the-ultimate-goodness-towards-efficient-website-fingerprinting-def ense-via-iterative-mutual-information-minimization/

[21] J. K. Holland and N. Hopper, “Regulator: A straightforward website fingerprinting defense,” Proc. Priv. Enhancing Technol., vol. 2022, no. 2, pp. 344–362, 2022. [Online]. Available: https: //doi.org/10.2478/popets-2022-0049

[22] R. Jansen, R. Wails, and A. Johnson, “A measurement of genuine tor traces for realistic website fingerprinting,” in Passive and Active Measurement - 27th International Conference, PAM 2026, March 23-25, 2026, Proceedings, ser. Lecture Notes in Computer Science, S. Ferlin-Reiter, R. Fontugne, and J. Ullrich, Eds., vol. 16477. Virtual Event: Springer, 2026, pp. 277–293. [Online]. Available: https://doi.org/10.1007/978-3-032-18268-5 13

[23] M. Shen, K. Ji, J. Wu, Q. Li, X. Kong, K. Xu, and L. Zhu, “Real-time website fingerprinting defense via traffic cluster anonymization,” in IEEE Symposium on Security and Privacy, SP 2024, May 19-23, 2024. San Francisco, CA, USA: IEEE, 2024, pp. 3238–3256. [Online]. Available: https://doi.org/10.1109/SP54263.2024.00247

[24] K. Khajavi and T. Wang, “Lightening the load: A cluster-based framework for a lower-overhead, provable website fingerprinting

defense,” in 33rd Annual Network and Distributed System Security Symposium, NDSS 2026, February 23-27, 2026. San Diego, California, USA: The Internet Society, 2026, pp. 1 – 18. [Online]. Available: https://www.ndss-symposium.org/ndss-paper/lightening-the-load-a-clu ster-based-framework-for-a-lower-overhead-provable-website-fingerpri nting-defense/

[25] K. Al-Naami, A. El-Ghamry, M. S. Islam, L. Khan, B. Thuraisingham, K. W. Hamlen, M. F. Alrahmawy, and M. Z. Rashad, “Bimorphing: A bi-directional bursting defense against website fingerprinting attacks,” IEEE Trans. Dependable Secur. Comput., vol. 18, no. 2, pp. 505–517, 2021. [Online]. Available: https://doi.org/10.1109/TDSC.2019.2907240

[26] Tor Project, “Pluggable transport specification (version 1),” https://spec .torproject.org/pt-spec, 2022, tor Specifications.

[27] J. Gong, W. Zhang, C. Zhang, and T. Wang, “Wfdefproxy: Real world implementation and evaluation of website fingerprinting defenses,” IEEE Trans. Inf. Forensics Secur., vol. 19, pp. 1357–1371, 2024. [Online]. Available: https://doi.org/10.1109/TIFS.2023.3327662

[28] N. Krishnaraj, M. Elhoseny, E. L. Lydia, K. Shankar, and O. Aldabbas, “An efficient radix trie-based semantic visual indexing model for large-scale image retrieval in cloud environment,” Softw. Pract. Exp., vol. 51, no. 3, pp. 489–502, 2021. [Online]. Available: https://doi.org/10.1002/spe.2834

[29] J. Shi, W. Wang, Q. Zhou, and L. Wang, “Multiscale fingerprinting for robust website fingerprinting attack,” Comput. J., vol. 68, no. 10, pp. 1436–1449, 2025. [Online]. Available: https://doi.org/10.1093/comjnl/b xaf047

[30] T. Wang and I. Goldberg, “Improved website fingerprinting on tor,” in Proceedings of the 12th annual ACM Workshop on Privacy in the Electronic Society, WPES 2013, November 4, 2013, A. Sadeghi and S. Foresti, Eds. Berlin, Germany: ACM, 2013, pp. 201–212. [Online]. Available: https://doi.org/10.1145/2517840.2517851

[31] X. Cai, R. Nithyanand, and R. Johnson, “Cs-buflo: A congestion sensitive website fingerprinting defense,” in Proceedings of the 13th Workshop on Privacy in the Electronic Society, WPES 2014, November 3, 2014, G. Ahn and A. Datta, Eds. Scottsdale, AZ, USA: ACM, 2014, pp. 121–130. [Online]. Available: https: //doi.org/10.1145/2665943.2665949

[32] S. Li, H. Guo, and N. Hopper, “Measuring information leakage in website fingerprinting attacks and defenses,” in Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security, CCS 2018, October 15-19, 2018, D. Lie, M. Mannan, M. Backes, and X. Wang, Eds. Toronto, ON, Canada: ACM, 2018, pp. 1977–1992. [Online]. Available: https://doi.org/10.1145/3243734.3243832

[33] M. Juarez, S. Afroz, G. Acar, C. D´ıaz, and R. Greenstadt, “A critical evaluation of website fingerprinting attacks,” in Proceedings of the 2014 ACM SIGSAC Conference on Computer and Communications Security, November 3-7, 2014, G. Ahn, M. Yung, and N. Li, Eds. Scottsdale, AZ, USA: ACM, 2014, pp. 263–274. [Online]. Available: https://doi.org/10.1145/2660267.2660368

[34] R. Jansen, “CELLSHIFT: rtt-aware trace transduction for real-world website fingerprinting,” in 33rd Annual Network and Distributed System Security Symposium, NDSS 2026, February 23-27, 2026. San Diego, California, USA: The Internet Society, 2026, pp. 1–18. [Online]. Available: https://www.ndss-symposium.org/ndss-paper/cellshift-rtt-a ware-trace-transduction-for-real-world-website-fingerprinting

[35] X. Deng, Q. Li, and K. Xu, “Robust and reliable early-stage website fingerprinting attacks via spatial-temporal distribution analysis,” in Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security, CCS 2024, October 14-18, 2024, B. Luo, X. Liao, J. Xu, E. Kirda, and D. Lie, Eds. Salt Lake City, UT, USA: ACM, 2024, pp. 1997–2011. [Online]. Available: https://doi.org/10.1145/3658644.3670272

[36] WFLib, “Website-Fingerprinting-Library: A Library for Advanced DLbased Website Fingerprinting Attacks,” https://github.com/FIND-Lab/W ebsite-Fingerprinting-Library, accessed: 2026-08-19.

[37] N. Mathews, J. K. Holland, S. E. Oh, M. S. Rahman, N. Hopper, and M. Wright, “Sok: A critical evaluation of efficient website fingerprinting defenses,” in 44th IEEE Symposium on Security and Privacy, SP 2023, May 21-25, 2023. San Francisco, CA, USA: IEEE, 2023, pp. 969–986. [Online]. Available: https://doi.org/10.1109/SP46215.2023.10179289

[38] G. Acar, M. Juarez et al., “tor-browser-selenium: Tor browser automation with selenium,” https://github.com/webfp/tor-browser-selenium, 2023, accessed: 2025-12-22.

[39] V. L. Pochat, T. van Goethem, S. Tajalizadehkhoob, M. Korczynski, and W. Joosen, “Tranco: A research-oriented top sites ranking hardened against manipulation,” in 26th Annual Network and Distributed System Security Symposium, NDSS 2019, February 24-27, 2019. San Diego, California, USA: The Internet Society, 2019, pp. 1–15. [Online]. Available: https://www.ndss-symposium.org/ndss-paper/tranco-a-resea rch-oriented-top-sites-ranking-hardened-against-manipulation/

[40] A. Panchenko, F. Lanze, J. Pennekamp, T. Engel, A. Zinnen, M. Henze, and K. Wehrle, “Website fingerprinting at internet scale,” in 23rd Annual Network and Distributed System Security Symposium, NDSS 2016, February 21-24, 2016. San Diego, California, USA: The Internet Society, 2016, p. 23477. [Online]. Available: http://wp.internetsociety.org/ndss/wp-content/uploads/sites/2 5/2017/09/website-fingerprinting-internet-scale.pdf

[41] W. D. la Cadena, A. Mitseva, J. Hiller, J. Pennekamp, S. Reuter, J. Filter, T. Engel, K. Wehrle, and A. Panchenko, “Trafficsliver: Fighting website fingerprinting attacks with traffic splitting,” in CCS ’20: 2020 ACM SIGSAC Conference on Computer and Communications Security, November 9-13, 2020, J. Ligatti, X. Ou, J. Katz, and G. Vigna, Eds. Virtual Event, USA: ACM, 2020, pp. 1971–1985. [Online]. Available: https://doi.org/10.1145/3372297.3423351

[42] The Tor Project, “Research Safety Board,” https://research.torproject.or g/safetyboard/, accessed: 2026-08-19.

[43] M. Paterson and V. Dancˇ´ık, “Longest common subsequences,” in International symposium on mathematical foundations of computer science. Springer, 1994, pp. 127–142.

[44] E. Perez, F. Strub, H. De Vries, V. Dumoulin, and A. Courville, “Film: Visual reasoning with a general conditioning layer,” in Proceedings of the AAAI conference on artificial intelligence, vol. 32, no. 1, 2018.

[45] O. Ronneberger, P. Fischer, and T. Brox, “U-net: Convolutional networks for biomedical image segmentation,” in International Conference on Medical image computing and computer-assisted intervention. Springer, 2015, pp. 234–241.

[46] T.-Y. Lin, P. Goyal, R. Girshick, K. He, and P. Dollar, “Focal loss´ for dense object detection,” in Proceedings of the IEEE international conference on computer vision, 2017, pp. 2980–2988.

[47] C. H. Sudre, W. Li, T. Vercauteren, S. Ourselin, and M. Jorge Cardoso, “Generalised dice overlap as a deep learning loss function for highly unbalanced segmentations,” in International Workshop on Deep Learning in Medical Image Analysis. Springer, 2017, pp. 240–248.

[48] Y. Wang, Q. Yao, J. T. Kwok, and L. M. Ni, “Generalizing from a few examples: A survey on few-shot learning,” ACM computing surveys (csur), vol. 53, no. 3, pp. 1–34, 2020.

## APPENDIX

## A. Hyperparameter Setting

To evaluate each WF defense model under an optimal tradeoff between performance and overhead, we employ a carefully selected set of hyperparameters based on the configurations reported in the original studies. TABLE IX summarizes the hyperparameter settings used for each model in this work.

In FRONT [16], $N _ { c }$ and $N _ { s }$ are key parameters that determine the data overhead, representing the padding budgets at the client and proxy, respectively. The parameters $W _ { m i n }$ and $W _ { m a x }$ define the padding window (Minimum and maximum padding time), which controls the temporal range within which dummy packets are most likely to be injected into the original traffic trace. In Palette [23], u upload and $u _ { - }$ download are introduced to tune the upper bounds, enabling a principled trade-off between time overhead and anonymity for upload and download traffic, respectively. The thresholds alpha upload and alpha download govern the time-slot sampling process for upload and download directions, determining when traffic should be considered for transmission. The parameter k specifies the anonymity set size, while b denotes the tail padding length. Specifically, b is used to monitor whether the transmission buffer remains empty over consecutive time slots, thereby determining whether dummy packet padding should be continued to preserve anonymity guarantees.

TABLE IX: Parameter settings for evaluating WF defense models under an optimal trade-off between performance and overhead.

<table><tr><td>Defense models</td><td>Hyperparameters</td></tr><tr><td>FRONT</td><td> $N_c = N_s = 100, W_{min} = 1s, W_{max} = 8s$ </td></tr><tr><td>ALERT</td><td> $min = 0.1, max = 0.5$ </td></tr><tr><td>Palette</td><td> $u\_upload = u\_download = 45, round = 1, alpha\_upload = alpha\_download = 0.16, k = 30, b = 20$ </td></tr><tr><td>FRUGAL</td><td> $bwo\_para = 0.8, limits = 20$ </td></tr><tr><td>GAPDiS</td><td> $max\_perturb = 128, tabu\_len\_multi = 5, topk\_num = 10, muta\_rate = 8$ </td></tr><tr><td>Adaptive Tamaraw</td><td> $k = 7, \alpha = 0.9, L = 1000$ </td></tr><tr><td>Chameleon (Ours)</td><td> $\rho = 0.2, mutation = 1, epochs = 50$ </td></tr><tr><td>DAAE (Ours)</td><td> $train\_ratio = 0.2$ </td></tr></table>

In ALERT [19], min and max control the min and max overhand thresholds. In GAPDiS [18], max perturb denotes the maximum perturbation length. max $\_ p e r t u r b \ = \ 1 2 8$ means a maximum of 128 dummy packets are allowed to be inserted. In addition, topk num denotes the number of top-k candidate solutions retained during the search process, constrained within the range [1, 5000−M]. The mutation rate, muta rate, controls the degree of stochastic variation introduced into candidate solutions. tabu len multi determines the number of layers used to scale the tabu list length, thereby influencing the memory structure and the search procedure’s diversification capability. In FRUGAL [20], bwo para is the bandwidth overhead parameter, limits is the number of training samples per class.

In Adaptive Tamaraw [24], as in the Palette defense work, k is the anonymity set size. L is the Tamaraw bucket length parameter, Larger L provides better security but higher overhead. α is the ECDIRE confidence threshold that controls when to switch from global to local parameters. In our design, the parameter website trace selection ratio $\rho$ defines the high intra-class diversity and low inter-class separability website trace selection ratio. The lower selection ratio will decrease the defense efficiency and lower the memory overhead for building the radix trie. Parameter mutation controls the website morphing strategy. When mutation = 1, the model applies trace mutation; when mutation = 0, it performs fulltrace morphing; and when mutation = 3, it uses trace cut-off morphing. For both training and evaluation, we set the number of epochs to epochs = 50. In the DAAE design, by default, 20% of the dataset $( t r a i n \_ r a t i o = 0 . 2 )$ is used for model training, while the remaining 80% is used for testing.

## B. Defense-Aware Autoencoder (DAAE) Attack

Through analyzing existing many-to-one defense mechanisms, we develop a new Defense-Aware Autoencoder (DAAE) attack that learns the characteristic packet-injection patterns introduced by WF defenses and removes the inferred dummy packets from unseen defended traces.

1) DAAE Formalization: DAAE is a defense-aware autoencoder that learns the packet transformation induced by a defense D from a small paired corpus of original and defended traces. Let

$$
\mathcal {P} = \left\{\left(W _ {i}, W _ {i} ^ {\prime}, y _ {i}\right) \right\} _ {i = 1} ^ {\mathcal {R}}, \qquad W _ {i} ^ {\prime} = \mathcal {D} (W _ {i}),\tag{2}
$$

where $y _ { i } \in \mathcal { V }$ denotes the website label and i indexes the i-th trace pair.

For each pair $( W _ { i } , W _ { i } ^ { ' } , y _ { i } ) \ \in \ \mathcal { P }$ , sequence alignment is performed to derive a supervision mask without requiring white-box access to the defense mechanism D:

$$
\mathbf {m} = \mathrm{Align} \big (W _ {i}, W _ {i} ^ {\prime} \big).\tag{3}
$$

Here, Align can employ different sequence alignment strategies, including Hamming distance, Longest Common Subsequence (LCS) [43], and a greedy method.

A defense-agnostic encoder Φ maps each defended trace to a fixed-width tensor with c feature channels, corresponding to packet direction, min-max normalized timestamps, and log inter-packet gaps:

$$
X _ {i} ^ {\prime} = \Phi (W _ {i} ^ {\prime}) \in \mathbb {R} ^ {c \times L},\tag{4}
$$

where $\mathbb { R } ^ { c \times L }$ denotes the space of real-valued matrices with c feature channels and L trace positions.

The defense-aware autoencoder $f _ { \theta }$ takes the defended feature tensor $X ^ { ' }$ together with same-class support pairs ${ \boldsymbol { S } } =$ $( X ^ { ' } , \mathbf { m } )$ and learns to infer the transformation pattern of the defense. Given the defense-aware training set $\mathcal { P } _ { \mathrm { t r } }$ , the model is trained by minimizing the discrepancy between its predictions and the alignment-derived supervision masks:

$$
\theta^ {*} = \arg \min _ {\theta} \mathbb {E} _ {(W, W ^ {\prime}) \sim \mathcal {P} _ {\mathrm{tr}}} \left[ \mathcal {L} \big (\theta ; W, W ^ {\prime}, \mathbf {m}, \mathcal {S} \big) \right].\tag{5}
$$

As shown in Figure 12, given a query trace and a set of support traces, a 1D CNN extracts their representations, while a prototype-based Feature-wise Linear Modulation (FiLM) [44] layer and cross-attention enable the query to incorporate defense-specific injection patterns learned from the supports. The DAAE model employs two complementary prediction paths: a convolutional head for identifying local injection boundaries and a U-Net [45] with dilated convolutions for capturing longer dummy-packet runs.

DAAE is trained using paired original and defended traces. For each pair, we first align the two traces to identify the positions at which dummy packets are inserted. We implement three alignment strategies: LCS, Hamming distance, and a greedy method, with LCS used by default. The resulting alignment provides dummy-packet positions under different traffic patterns, which are then used as supervision for training DAAE. To optimize the DAAE model, we apply focal [46] and Dice [47] losses. We observe that dummy-injection defenses typically add many padding packets. A plain per-packet $L _ { 2 }$ loss can ignore the rarer class, while focal loss up-weights hard decisions. Meanwhile, Dice loss measures overlap between the predicted and labeled keep sets over the whole trace. We also apply a keep-rate regularizer so the predicted fraction of original packets matches the labeled fraction.

![](images/2d32b71605f9c5743e25c2c24894034a716e2d55a344f89b1acc1e139c4206ac.jpg)

![](images/3d3ff3f3bd7772b00025ad07c1f2941da5cf2e29f58c8ece22c50876f6bcf475.jpg)  
(a) Traffic trace patterns of website 1

![](images/7ac42fe9753bdbe9a29117c6c69bec3628a9d77cff2806f5823c00f85ccc9ade.jpg)

![](images/d86290ae0e889c4849e9360c1b97f05fdbc0bf842edd2e71a42ae761872c0603.jpg)

![](images/64ade444bca6b4c0221a853511f7245640bdaff4509401f8b9458283f84ec991.jpg)  
(b) Traffic trace patterns of website 2

![](images/b849b308086a24c30d301b4c28b856edea6f70f77d3ff1a9800c462c2632d983.jpg)

Fig. 11: Visualization of the TAMs for two websites under three settings: the original trace, the Palette [23]-defended trace, and the trace recovered by the DAAE-based attack under the GTT23 dataset [22]. Each TAM covers the first 100 time slots, with each slot spanning 50ms. Outgoing and incoming packets are represented by blue (+1) and red (−1) bars, respectively, with bar height indicating the packet count within each slot. Each row presents the original, Palette-defended, and DAAE-recovered trace patterns from the same website.  
![](images/11a8b8e37ba742bc5bced5f935cefe155bc1b8265b1e976447c17297316c4a48.jpg)  
Fig. 12: An overview of the DAAE architecture.

We further develop a few-shot variant [48], FS-DAAE. To match a real WF setting, the attacker does not know the class of a captured trace. Only a limited paired split (20% of instances per class by default) is labeled and used to train DAAE. The remaining instances are never paired with originals at test and validation phases. At inference, the attacker observes only a captured defended trace and has no access to its original trace, true class label, or victim-side state. Neither DAAE nor FS-DAAE uses the true class labels of validation or test traces during recovery. Instead, the trained model directly infers the defense’s dummy-packet injection pattern and removes the predicted dummy packets from each defended trace.

2) DAAE Decoding Stategy: At test time, DAAE does not have access to the original trace. Instead, it maintains a small support pool constructed from the training set and applies the same inference pipeline to the captured defended traffic. We designed two strategies to decode the defended packets into the original ones. We find that directly thresholding at 0.5 for the predicted keep probabilities can incorrectly remove original packets or retain dummy packets, disrupting the original packet-direction subsequence. Therefore, we perform a sequence-level decoding step against support prototypes, where each prototype represents the packet-direction sequence of the packets labeled as original in a support trace. We introduce a skip bias to control the trade-off between retaining and removing packets and select the bias that produces a keep rate closest to the median keep rate of the support set. When multiple supports are available, we first consider supports whose kept-trace lengths are closest to the target length and select the candidate yielding the best sequence-level decoding score. The recovered trace is then constructed by retaining the captured packets selected by the final mask. Finally, we train a standard WF classifier, such as DF and RF, on the recovered traces and evaluate its classification performance to quantify how effectively DAAE restores the fingerprint information removed by the defense.

As shown in the third column of Figure 11, the recovered traces do not exactly match the originals, but much of their original traffic structure is restored. This result suggests that defense-induced traffic artifacts can be exploited to partially reverse the effect of traffic regularization, potentially undermining the defense against a sufficiently adaptive adversary. Figure 11 demonstrates that the original non-defended traces show distinct patterns in their Traffic Aggregation Matrices (TAMs) [2]. Palette [23] aims to reduce this variability by regularizing traffic into a common pattern. However, the resulting defended traces can still preserve noticeable differences. More importantly, the regularization process introduces systematic dummy-packet injection patterns that may themselves become learnable by an adaptive adversary.

## C. Row-wise z-score Normalization

Row-wise z-score normalization applies a separate mapping standardization to each row of a matrix $\mathbf { X } \in \mathbb { R } ^ { N \times L }$ .N is the number of traces and L the fixed prefix length used for comparison. This algorithm treats each row as one feature vector. As shown in Algorithm 3, for each row i, the algorithm computes the row mean $\mu _ { i }$ and a row scatter scale $\sigma _ { i }$ from the entries $X _ { i j } , j = 1  L$ , then sets $Z _ { i j } = ( X _ { i j } - \mu _ { i } ) / ( \sigma _ { i } + \varepsilon )$ A stability constant $\varepsilon > 0$ is added to the denominator to avoid division by zero when a row is constant or near constant. In implementation, $\sigma _ { i }$ follows either standard deviation (divide by L under the square root) or sample standard deviation (divide by L−1). ε and the precise $\sigma _ { i }$ are the key parameters that materially affect the normalized rows.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3: Row-wise z-score normalization of matrix X

Input: Matrix  $X \in R^{N \times L}$ , stability constant  $\varepsilon &gt; 0$ 

Output: Row-normalized matrix  $Z \in R^{N \times L}$ 

1 for  $i \leftarrow 1$  to N do

2  $\mu_i \leftarrow \frac{1}{L} \sum_{j=1}^{L} X_{ij} // Compute row mean$ 

3  $\sigma_i \leftarrow \sqrt{\frac{1}{L} \sum_{j=1}^{L} (X_{ij} - \mu_i)^2} //Compute row standard deviation$ 

4 for  $j \leftarrow 1$  to L do

5  $Z_{ij} \leftarrow \frac{X_{ij} - \mu_i}{\sigma_i + \varepsilon} //Row-wise z-score$ 

6 end

7 end

8 return Z
</div>

This method will centralize each trace around zero and rescale the centralization spread. So that rows with different absolute magnitudes or local variance become more comparable before similarity measures are computed. The operation is performed independently on each row, ensuring that no statistical information is shared between traces. Consequently, the identity of each sample is preserved while eliminating variations that arise solely from scale differences along the sequence dimension.

## D. Defense Performance Against WF Attacks Without Adversarial Training

We compare the proposed Chameleon defense with six defenses across the DF and DS-19 datasets under four representative WF attack models. As shown in Table X, Chameleon consistently achieves the lowest WF attack accuracy.

Specifically, on the DF dataset, all variants of Chameleon consistently outperform prior defenses by a substantial margin. In particular, the lightweight variant of Chameleon reduces attack accuracy to as low as 1.55% across all attack models, yielding a clear improvement over the strongest existing baseline. While Palette achieves a minimum accuracy of 1.92%, Chameleon further advances the SOTA defense by achieving lower and more consistent accuracy across attacks. Compared to other competitive defenses, such as Adaptive Tamaraw and GAPDiS, Chameleon demonstrates a marked reduction in attack success rates, underscoring its robustness against diverse attack architectures. Importantly, the medium and heavy configurations of Chameleon also exhibit strong performance, consistently surpassing most baselines and indicating that the effectiveness of Chameleon is maintained across different resource-performance trade-offs. The advantage of Chameleon becomes even more pronounced on the more challenging DS-19 dataset. Here, lightweight Chameleon achieves near-zero attack accuracy, substantially surpassing all prior defenses, including Palette and Adaptive Tamaraw, whose best results remain above 1.00%.

Moreover, while existing defenses exhibit noticeable performance degradation or variability across different attacks, Chameleon maintains consistently low accuracy across all models, highlighting its strong robustness capability. The proposed trace mutation mechanism alters the underlying traffic patterns relative to the original website trace and target-morphing traces, thereby reducing their distinguishability under WF attacks. By mitigating such pattern redundancy, Chameleon achieves more diverse and less predictable traces, contributing to its robust and stable defense performance.

Chameleon is a trace-driven pluggable transport that morphs packet timing and directionality to mimic realistic encrypted web traffic while preserving Tor’s deployment model. The design sits on top of an authenticated, encrypted transport channel and therefore treats morphology as a traffic-shaping problem rather than a cryptographic one: confidentiality and integrity are provided by the underlying channel, while Chameleon controls observable metadata. At a high level, Chameleon continuously emits packets according to a selected reference trace template and maps application payload into template slots designated for outbound transmission. When no payload is available, but the defense is active, it emits dummy packets to preserve schedule consistency, reducing leakage from idle periods and burst structure.

The core of Chameleon is a prefix-conditioned template engine. An offline dataset of representative traces is converted into directional sequences and indexed in a radix trie. Each online connection maintains a rolling prefix of recent packet directions and queries the trie for templates that share the same prefix. Additionally, one candidate is randomly selected and may be mutated over time to enforce feasibility constraints. This gives Chameleon two properties that are hard to obtain simultaneously with static schedules: (i) continuity with recent flow evolution, and (ii) controlled stochasticity that avoids deterministic fingerprints. In effect, the transport performs constrained sampling over a realistic trace manifold rather than replaying fixed traces.

## E. Effectiveness of Prefix Length in Radix Trie

Figure 13 illustrates the efficacy of morphing trace targeting using a radix trie on the DF and DS-19 datasets. The figures show the targeting latency, the depth at which the morphing target is determined, and the number of candidate website traces sharing the same prefix. Specifically, Figure 13a presents the prefix-matching performance on the DF dataset. The results indicate substantial intra-dataset diversity. Most website traces exhibit highly discriminative prefixes after about 450 packet transmissions. This property enables efficient target selection, with the delay of completing morphingtrace targeting within 0.8 seconds in the majority of website traces. In contrast, Figure 13b shows that the DS-19 dataset exhibits lower diversity. A few website traces continue to share identical prefixes even beyond the truncated radix trie length threshold. In such cases, the system resorts to random selection among the remaining candidates. Nevertheless, the overall targeting delay remains below 1 second.

TABLE X: Evaluation of defense effectiveness without AT-based attack across six SOTA WF defenses using DF [4] and DS-19 [16] datasets under four SOTA WF attack models in the closed-world scenario.

<table><tr><td rowspan="3">Dataset/ Attacks Defenses</td><td colspan="4">DF [4]</td><td colspan="4">DS-19 [16]</td></tr><tr><td>DF [4]</td><td>Var-CNN [5]</td><td>RF [2]</td><td>NetCLR [3]</td><td>DF [4]</td><td>Var-CNN [5]</td><td>RF [2]</td><td>NetCLR [3]</td></tr><tr><td colspan="4">Accuracy (%)</td><td colspan="4">Accuracy (%)</td></tr><tr><td>NoDef</td><td>98.33</td><td>98.83</td><td>98.93</td><td>98.53</td><td>97.23</td><td>96.75</td><td>90.94</td><td>97.50</td></tr><tr><td>FRONT [16]</td><td>27.54</td><td>28.71</td><td>35.18</td><td>25.79</td><td>37.23</td><td>46.75</td><td>40.94</td><td>47.53</td></tr><tr><td>ALERT [19]</td><td>17.48</td><td>24.07</td><td>29.85</td><td>19.82</td><td>28.80</td><td>36.50</td><td>37.80</td><td>29.61</td></tr><tr><td>Palette [23]</td><td>2.15</td><td>2.49</td><td>3.01</td><td>1.92</td><td>1.10</td><td>1.75</td><td>2.23</td><td>1.01</td></tr><tr><td>GAPDiS [18]</td><td>7.19</td><td>4.60</td><td>11.79</td><td>10.74</td><td>1.65</td><td>2.89</td><td>1.50</td><td>2.88</td></tr><tr><td>FRUGAL [20]</td><td>5.29</td><td>5.75</td><td>11.17</td><td>6.73</td><td>5.10</td><td>5.63</td><td>11.26</td><td>6.29</td></tr><tr><td>Adaptive Tamaraw [24]</td><td>5.05</td><td>5.15</td><td>6.28</td><td>5.23</td><td>1.23</td><td>1.77</td><td>1.82</td><td>1.00</td></tr><tr><td>Chameleon (Lightweight)</td><td>1.77</td><td>1.85</td><td>1.55</td><td>1.62</td><td>0.17</td><td>0.11</td><td>0.30</td><td>0.95</td></tr><tr><td>Chameleon (Medium)</td><td>3.39</td><td>3.00</td><td>3.19</td><td>3.40</td><td>2.37</td><td>2.30</td><td>2.33</td><td>2.40</td></tr><tr><td>Chameleon (Heavy)</td><td>2.88</td><td>2.75</td><td>3.18</td><td>2.92</td><td>2.70</td><td>2.61</td><td>2.78</td><td>2.80</td></tr></table>

![](images/17b80441c7ce6a5e1b52ed4fb3346fe96fff314d44922941ddf7510fe6b7a565.jpg)  
(a) Effectiveness of morphing trace targeting on the DF dataset.

![](images/fe510aec59106a6d8b9d1fde0cfeef364b106574e8d9574d9ae62e40638fedab.jpg)  
(b) Effectiveness of morphing trace targeting on the DS-19 dataset.  
Fig. 13: Overview of the effectiveness of morphing trace targeting through radix trie on the DF and DS-19 datasets.

## F. Information Leakage Analysis

We provide an idealized analysis to characterize the privacy benefit of randomized many-to-many trace morphing. This analysis is intended to explain the intuition behind the design rather than provide a security guarantee for the complete implementation. In particular, it abstracts away timing, online prefix-based candidate selection, trace mutation, and other implementation-dependent behavior, whose privacy impact is evaluated empirically.

a) Idealized Morphing Model.: Let W denote the website class and C denote the candidate morphing trace observed by an adversary. For each website $w ,$ let $\mathcal { C } _ { w }$ denote the set of candidate traces to which its traffic may be mapped. We consider an idealized setting in which the defense randomly selects a candidate from $\mathcal { C } _ { w }$ and the observable output is determined only by the selected candidate. Thus, the information available to the adversary is characterized by $I ( W ; C )$

A deterministic mapping (e.g., one-to-one) preserves the website identity through the selected candidate and therefore does not protect in this idealized model. In contrast, the manyto-many mapping of Chameleon allows candidate traces to be shared across different websites. For an observed candidate $c ,$ define

$$
\mathcal {W} (c) = w: P (C = c \mid W = w) > 0,\tag{6}
$$

which contains all website classes that may produce c. If $C =$ c is observed, the adversary must distinguish among the classes in $\mathcal { W } ( c )$ rather than infer a unique source website.

Suppose that candidate c can be produced by m website classes with equal priors and equal conditional selection probabilities. By Bayes’ rule,

$$
P (W = w \mid C = c) = \frac {1}{m}, \qquad w \in \mathcal {W} (c),\tag{7}
$$

and therefore

$$
H (W \mid C = c) = \log_ {2} m.\tag{8}
$$

Under these assumptions, increasing the number of source classes sharing a candidate increases the residual uncertainty of an adversary in this idealized setting. More generally, the leakage is

$$
I (W; C) = H (W) - H (W \mid C),\tag{9}
$$

so candidate sharing can reduce leakage when it increases $H ( W \mid C )$

b) Scope of the Analysis.: The above result applies only to the idealized candidate-mapping abstraction and should not be interpreted as a security bound for the complete Chameleon system. In the implementation, candidate selection is conditioned on prefixes observed from real-time traffic, and the final trace may be further modified by timing behavior, dummycell insertion, trace cut-off, and mutation. In particular, trace mutation is designed to reduce directional mismatch and transmission overhead; reducing this mismatch does not necessarily reduce information leakage and may, in some cases, preserve additional characteristics of the original traffic. We therefore make no information-theoretic claim that mutation decreases $I ( W ; Y )$ or the divergence between website-specific output distributions. Instead, the privacy of the complete system, including these dependencies, is quantified empirically using WeFDE [32] leakage measurements and evaluated against the WF attacks considered in Section G.

TABLE XI: Information leakage for each feature category (Bit).

<table><tr><td>Categories</td><td>Pkt. Count</td><td>Time</td><td> $Interval_{Mean}$ </td><td> $Interval_{std}$ </td><td>Pkt. Distribution</td><td>Burst</td><td>First 20</td><td>First 30</td><td>Diag GNB</td></tr><tr><td>NoDef</td><td>1.231</td><td>0.818</td><td>0.828</td><td>0.660</td><td>1.233</td><td>1.030</td><td>0.675</td><td>0.520</td><td>5.82</td></tr><tr><td>FRONT</td><td>1.253 ↑0.022</td><td>0.786</td><td>0.753</td><td>0.459</td><td>0.795</td><td>0.157</td><td>0.167</td><td>0.479</td><td>5.57</td></tr><tr><td>RegulaTor</td><td>1.183</td><td>0.972 ↑0.154</td><td>0.662</td><td>0.288</td><td>0.687</td><td>1.251 ↑0.221</td><td>0.067</td><td>0.044</td><td>5.49</td></tr><tr><td>Palette</td><td>1.059</td><td>0.788</td><td>0.612</td><td>0.328</td><td>1.043</td><td>0.431</td><td>0.025</td><td>0.036</td><td>4.62</td></tr><tr><td>Chameleon</td><td>0.727</td><td>0.709</td><td>0.614</td><td>0.495</td><td>0.718</td><td>0.374</td><td>0.351</td><td>0.464</td><td>4.57</td></tr></table>

## G. Information Leakage Measurement

As Chameleon employs randomized many-to-many traffic morphing, multiple browsing sessions may produce identical or highly similar feature representations. We retain these repeated observations when computing information leakage because they are part of the empirical output distribution generated by the defense. Removing duplicated feature vectors would alter their empirical frequencies and may therefore change the estimated relationship between website labels and observable traffic features. We consequently apply WeFDE [32] to the complete defended trace set without deduplicating feature representations. As a robustness check, we additionally evaluate a deduplicated variant and report the resulting leakage separately to determine whether the conclusions are sensitive to duplicate handling.

Table XI reports the information leakage estimated from the complete empirical trace distribution across eight representative feature categories, together with the aggregate Diagonal Gaussian Na¨ıve Bayes (Diag GNB) measurement. Lower leakage indicates that the observable traffic features reveal less information about the corresponding website labels. Chameleon achieves lower or comparable leakage across most feature categories and obtains the lowest aggregate Diag GNB leakage among the evaluated defenses. Chameleon reduces packet-count leakage to 0.727, compared to 1.231 for NoDef and 1.253 for FRONT, and lowers packet-distribution leakage to 0.718, compared to 1.233 for NoDef. In contrast, RegulaTor exhibits higher leakage for timing-related features, with a mean interval of 0.972 and a burst of 1.251, whereas Chameleon maintains lower, more stable values across these dimensions. Palette achieves lower leakage in certain finegrained features, such as First 20 (packets) with 0.025 and First 30 (packets) with 0.036, yet its leakage remains higher than Chameleon in several other categories. In addition, Chameleon attains the lowest aggregate leakage under Diag GNB with a value of 4.57, outperforming NoDef with 5.82, FRONT with 5.57, and RegulaTor with 5.49, indicating more comprehensive protection across diverse feature spaces.

## H. Security Analysis of the Idealized Many-to-Many Mapping

Let W denote the set of original traces and $W ^ { \prime }$ the set of defended traces. Chameleon first extracts a subset $C \subseteq W$ of candidate traces exhibiting high intra-class diversity and low inter-class separability. The defense defines a many-tomany relation ${ \mathcal { R } } \subseteq W \times C$ , where each trace $w \in W$ can be morphed into one or multiple candidate traces in C. For any $c \in C$ , define the pre-image:

$$
\mathcal {R} ^ {- 1} (c) = \{w \in W: (w, c) \in \mathcal {R} \}.\tag{10}
$$

Let $\mathcal { R } _ { y } ^ { - 1 } ( c )$ denote the subset of traces in $\mathcal { R } ^ { - 1 } ( c )$ belonging to class y.

Website Trace Injection Upper Bound. We define the effective injection upper bound for candidate trace c as:

$$
\tilde {\delta} (c) = \frac {| \mathcal {R} ^ {- 1} (c) |}{\max _ {y} | \mathcal {R} _ {y} ^ {- 1} (c) |}.\tag{11}
$$

This reflects both the number of traces mapped to c and their class diversity.

Lemma 1. For any candidate trace $c \in C ,$ the attacker’s success probability is bounded by:

$$
\operatorname * {P r} [ \text { success } \mid c ] \leq \frac {1}{\tilde {\delta} (c)}.\tag{12}
$$

Proof. Under Chameleon, all traces in $\mathcal { R } ^ { - 1 } ( c )$ are morphed into the same observable pattern c and are thus indistinguishable to the adversary. The optimal strategy is to predict the majority class within $\mathcal { R } ^ { - 1 } ( c )$ , yielding:

$$
\operatorname * {P r} [ \text {success} \mid c ] = \max _ {y} \frac {| \mathcal {R} _ {y} ^ {- 1} (c) |}{| \mathcal {R} ^ {- 1} (c) |} = \frac {1}{\tilde {\delta} (c)}.\tag{13}
$$

Theorem 1. Let the defended trace distribution be induced by sampling candidate traces $c \in C .$ . Define:

$$
\frac {1}{\delta} = \mathbb {E} _ {c \sim C} \left[ \frac {1}{\tilde {\delta} (c)} \right].\tag{14}
$$

Then the attacker’s average success probability is bounded by:

$$
\operatorname * {P r} [ \text { success } ] \leq \frac {1}{\delta}.\tag{15}
$$

Proof. From the lemma, for any observed trace c:

$$
\operatorname * {P r} [ \text { success } \mid c ] = \frac {1}{\tilde {\delta} (c)}.\tag{16}
$$

Taking expectation over the distribution of candidate traces:

$$
\operatorname * {P r} [ \text { success } ] = \mathbb {E} _ {c} \left[ \operatorname * {P r} [ \text { success } \mid c ] \right] = \mathbb {E} _ {c} \left[ \frac {1}{\tilde {\delta} (c)} \right] \leq \frac {1}{\delta}.\tag{17}
$$

Unlike mapping traces to fixed or highly regularized patterns, Chameleon leverages a candidate set C with high intraclass diversity and low inter-class separability. By allowing each trace to map to multiple candidates, the pre-image $\mathcal { R } ^ { - 1 } ( c )$ becomes both large and label-diverse, increasing $\tilde { \delta } ( c )$ and reducing attacker success probability, while avoiding the overhead of strict normalization.
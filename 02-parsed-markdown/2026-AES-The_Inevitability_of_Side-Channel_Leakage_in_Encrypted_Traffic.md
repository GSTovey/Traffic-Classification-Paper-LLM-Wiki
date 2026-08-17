# The Inevitability of Side-Channel Leakage in Encrypted Traffic∗

Guangjie Liu, Guang Cheng, Weiwei Liu

February 17, 2026

## Abstract

The widespread adoption of TLS 1.3 and QUIC has rendered payload content invisible, shifting traffic analysis toward reliance on side-channel features. However, rigorous justification for “why side-channel leakage is inevitable in encrypted communications” has long been lacking. This paper establishes a strict foundation from information theory and system design by constructing a formal model $\Sigma = ( \Gamma , \Omega )$ , where the encrypted communication model $\Gamma = ( A , \Pi , \Phi , N )$ describes the causal chain of “application generation–protocol encapsulation–encryption transformation– network transmission”, and the observation model Ω characterizes external observation capabilities. Based on the composite channel structure, data processing inequality, and stable propagation of bounded Lipschitz statistics, we propose and prove the “Side-Channel Existence Theorem”: for distinguishable semantic pairs, under the conditions that the system satisfies mapping non-degeneracy (bounded metric expectation $\mathbb { E } [ d ( z _ { P } , z _ { N } ) \mid X ] \le C )$ , protocol-layer statistical distinguishability (expectation difference $\ge \bar { \Delta } )$ , Lipschitz continuity of statistics, observation non-degeneracy (preservation ratio $\rho > 0 )$ , and the distinguishability propagation condition $( C < \bar { \Delta } / 2 L _ { \varphi } )$ , the mutual information $I ( X ; Y )$ between observed features and semantic variables is necessarily strictly positive with an explicit lower bound. The corollary demonstrates that in efficiency-prioritized multi-semantic systems, side-channel leakage is inevitable as long as at least one pair of applications is statistically distinguishable. Three key factors jointly determine the leakage boundary: the mapping non-degeneracy constant $C$ is constrained by efficiency requirements, semantic distinguishability $\bar { \Delta }$ stems from application diversity, and observation non-degeneracy $\rho$ is determined by analyst capabilities. This paper establishes, for the first time, a rigorous information-theoretic foundation for encrypted traffic side channels, providing verifiable predictions for attack feasibility, quantifiable performance benchmarks for defense mechanisms, and mathematical basis for engineering decisions on efficiency-privacy tradeoffs.

Keywords: side channel; information theory; encrypted traffic analysis; existence theorem; efficiency-privacy tradeoff

## 1 Introduction

With the widespread deployment of encryption protocols such as TLS 1.3 and QUIC, payload content in modern network communications has been strongly protected by cryptographic means. However, encrypted traffic analysis—which infers sensitive information (such as websites visited by users, applications used, or types of content transmitted) by observing metadata features of encrypted traffic (packet lengths, timing, direction, etc.)— has still achieved remarkable success: in closed environments, website fingerprinting accuracy can reach 91%-95% [1], and application identification accuracy exceeds 90% [2]; for encrypted anonymous traffic identification, in real campus gateway environment tests, precision can reach 96% under medium base rate scenarios, and remain above 93% even at extremely low base rates of 1000:1 [3]. This phenomenon raises a fundamental theoretical question: why does traffic analysis remain effective even when using computationally secure encryption algorithms such as AES-256-GCM?

From a cryptographic perspective, encryption algorithms ensure the confidentiality of payload content; without the key, attackers cannot recover plaintext from ciphertext. However, encryption protocols inevitably cannot hide communication metadata: source/destination addresses, packet lengths, timestamps, and other information are necessary for network routing and transmission control. This metadata forms the foundation of side channels. The concept of side channels first appeared in the field of cryptographic hardware implementation. Kocher (1996) proposed timing attacks that recover keys by measuring the execution time of encryption operations [4], and Kocher et al. (1999) introduced Differential Power Analysis (DPA) that extracts key information using power consumption variations of encryption devices [5]. The common characteristic of these attacks is: exploiting physical byproducts (time, power consumption, electromagnetic radiation, etc.) during the implementation of cryptographic algorithms, rather than directly breaking the algorithms themselves. Subsequently, the side-channel concept expanded to the field of network communications. Hintz’s (2002) work demonstrated how to identify websites visited by users by analyzing traffic patterns of encrypted web pages [6], promoting in-depth research on network traffic side channels. Network traffic side channels are essentially consistent with hardware side channels—encryption protects payload content, but observable features of the communication process itself (packet size, timing, direction, etc.) become a new source of information leakage. This paper focuses on network traffic side channels but inherits the core insight from hardware side-channel research: side channels are not defects in encryption algorithms, but inevitable byproducts of efficiency-prioritized implementation and deployment processes.

The root cause of network traffic side-channel leakage lies in the “fingerprint propagation” of application-layer behavioral patterns during transmission. Specifically: size differences in application objects map to length patterns of encrypted record sequences; the timing logic of HTTP request-response is reflected in packet arrival interval distributions; the directionality and burst characteristics of client-server interactions reflect protocol semantics; layer-by-layer encapsulation in the protocol stack amplifies subtle differences (TCP segmentation boundaries, congestion control window adjustments). These mechanisms make traffic from different applications statistically distinguishable—video streams show periodic bursts, instant messaging manifests as bidirectional interaction with small packets, and web browsing displays short-term high-density resource loading. Although encryption operations change payload content, they cannot eliminate these statistical fingerprints originating from application logic.

However, merely pointing out “fingerprint propagation” does not answer why side channels are inevitable. The deeper questions are: under given system constraints (limited computational resources, communication efficiency requirements, protocol compatibility needs), why does encryption system design necessarily lead to the existence of side channels? Does this existence have a quantifiable theoretical lower bound? Can the tradeoff relationship between efficiency and privacy be rigorously characterized mathematically?

In recent years, despite continuous innovation in attack methods for encrypted traffic analysis and significant performance improvements [7, 8], systematic justification for the theoretical inevitability of side-channel existence remains lacking. Li et al. (2018) quantified website fingerprinting leakage using mutual information $I ( X ; Y )$ , finding in experiments targeting the Tor network that even though Tor encrypts communication content and hides endpoint identities through three-layer relays, metadata features still leak website information: information leakage $I ( F ; W )$ from individual features reaches up to 3.45 bits, and combined features can reach approximately 6.6 bits [9]. This nonzero mutual information stems from Tor not obfuscating or padding traffic metadata to ensure low latency and low overhead. Cai et al. (2014) proved that any defense achieving ε-security necessarily incurs a computable bandwidth overhead lower bound in a closed world of n websites [24], revealing the theoretical cost of defense, but this lower bound only targets specific scenarios and lacks generality. The differential privacy framework provides quantifiable privacy guarantees for traffic analysis defense [10, 11], but its design philosophy seeks a balance between privacy and utility, rather than exploring the fundamental reasons for information leakage under efficiency constraints.

This paper provides a strict foundational reasoning for side-channel existence from information theory and system design. We first construct a formal model $\Sigma = ( \Gamma , \Omega )$ , where the encrypted communication system $\Gamma = ( A , \Pi , \Phi , N )$ characterizes the processes of application generation, protocol encapsulation, encryption transformation, and network transmission, and the observation model Ω delimits the layers and positions of external observation, formalizing “generation–encapsulation–encryption–transmission– observation” as a causally measurable composite channel ${ \cal X } \to \Xi _ { { \cal A } } \to \Xi _ { { \cal P } } \to \Xi _ { { \cal C } } \to \Xi _ { { \cal N } } \to$ Y . Within this framework, we externalize the constraints of efficiency-prioritized design as mapping non-degeneracy: there exists a metric d and constant $C < \infty$ such that the trajectory mapping from protocol layer to network layer maintains bounded deviation in the metric sense $\mathbb { E } [ d ( z _ { P } , z _ { N } ) ~ | ~ { \cal X } ] \le C$ . This metric captures the joint statistical structure of multiple dimensions such as length, timing, and direction of point processes, and the existence of bounded deviation C stems from practical requirements such as bandwidth, latency, and throughput. Combined with the stable propagation property of bounded Lipschitz statistics, we establish a strict derivation chain from protocol-layer distinguishability to observation-layer information leakage existence.

The core conclusion of this paper is the “Side-Channel Existence Theorem”: for distinguishable semantic pairs, when the following conditions are satisfied—the system mapping maintains non-degeneracy (metric expectation bound $\mathbb { E } [ d ( z _ { P } , z _ { N } ) \mid X ] \le C )$ , protocol-layer statistical distinguishability exists (expectation difference $\geq \bar { \Delta } )$ , statistics satisfy Lipschitz continuity, the observation model maintains non-degeneracy (preservation ratio $\rho > 0 )$ , and the distinguishability propagation condition $( C < \bar { \Delta } / 2 L _ { \varphi } )$ —the mutual information between observed features and semantic variables satisfies the explicit lower bound

$$
I (X; Y) \geq \frac {1}{2 \ln 2} \left(\frac {\rho [ \bar {\Delta} - 2 L _ {\varphi} C ]}{2}\right) ^ {2} > 0. \tag {1}
$$

This lower bound reveals the inevitability of side-channel leakage: the mapping nondegeneracy constant C is limited by efficiency constraints, semantic distinguishability $\bar { \Delta }$ originates from application diversity, and observation non-degeneracy $\rho$ is determined by analyst capabilities—these three factors jointly constitute an insurmountable leakage boundary. The corollary shows that in efficiency-prioritized multi-semantic systems, as long as at least one pair of applications is statistically distinguishable, side-channel leakage is necessarily positive.

Therefore, side channels are not incidental flaws in any protocol implementation, but inherent properties of network communication systems satisfying practical constraints. The correct engineering objective is not to pursue unattainable zero leakage, but rather a constrained optimization problem that minimizes leakage under given efficiency constraints.

This paper is organized as follows: Section 2 reviews related theoretical work; Section 3 constructs a formal model for side-channel analysis, including definitions of encrypted communication systems, observation models, and key properties; Section 4 proposes and proves the side-channel leakage existence theorem, establishing a derivation chain from expectation difference to mutual information; Section 5 discusses theoretical implications, analyzes the transformation from information-theoretic lower bounds to actual attack performance, the fundamentality of efficiency-privacy tradeoffs, and theoretical boundaries of defense; Section 6 concludes the paper, introduces several open problems regarding the practical implementation of the theoretical framework, and provides research outlook.

## 2 Related Theoretical Work

The theoretical foundation for side-channel analysis in networks can be traced back to early research in information theory and anonymity metrics. Chaum (1981) proposed mix networks, laying the foundation for anonymous communication [12], but rigorous mathematical frameworks for quantifying anonymity were long lacking. Díaz et al. (2002) first proposed measuring anonymity using Shannon entropy $H ( X ) = - \sum p _ { i } \log p _ { i }$ , introducing normalized entropy $d = H ( X ) / H _ { M }$ to distinguish the effects of anonymity set size and probability distribution [13]. The key insight of this work was: probability distribution is more important than set size—uniform distribution among 10 people $( d = 1 )$ provides stronger anonymity than 100 people where one person has 90% identification probability $( d \approx 0 . 4 7 )$ . Subsequent work introduced richer entropy metric tools: Deng et al. (2006) applied Rényi entropy $\begin{array} { r } { H _ { \alpha } ( X ) = \frac { 1 } { 1 - \alpha } \log \sum p _ { i } ^ { \alpha } } \end{array}$ to anonymity metrics [14], where different α values capture different aspects of the distribution $( \alpha  1$ reduces to

Shannon entropy). Serjantov and Danezis (2002) introduced mutual information $I ( X ; Y )$ into anonymity protocol analysis [15]. Chatzikokolakis et al. (2007) further interpreted anonymity protocols as noisy channels, characterizing leakage upper bounds with channel capacity $C = \operatorname* { m a x } I ( X ; Y )$ , and introduced relative entropy $\begin{array} { r } { D ( P \| Q ) = \sum p _ { i } \log ( p _ { i } / q _ { i } ) } \end{array}$ to measure changes in distribution before and after attacks [16]. These early works established the theoretical framework for quantifying privacy leakage using information theory, but mainly focused on anonymous communication protocols (such as mix networks and onion routing), without systematically analyzing the relationship between encryption protocols themselves and side channels.

Research on statistical leakage attacks revealed threats from long-term observation. Kesdogan et al. (2002) proved that in open environments, as long as users have habitual communication patterns, long-term observation inevitably leads to anonymity degradation [17]. Mathematically, this is equivalent to conditional entropy $H ( X | Y _ { 1 } , Y _ { 2 } , . . . , Y _ { t } )$ decreasing toward near-zero with the number of observations t, revealing the law of exponential decay of anonymity over time. Danezis (2003) proposed statistical disclosure attacks, identifying sender-receiver pairs in anonymous systems through traffic analysis [18]. These studies revealed the impact of temporal correlations but did not address the causal relationship between encryption protocol design and side channels—namely, why fundamental constraints in protocol design lead to side-channel existence.

The differential privacy framework provides quantifiable guarantees for privacy protection. Dwork et al. (2006) proposed differential privacy: mechanism M satisfies $( \varepsilon , \delta ) .$ - DP if for adjacent datasets $D , D ^ { \prime }$ and any output set S, $\operatorname* { P r } [ \mathcal { M } ( D ) \in S ] \le e ^ { \varepsilon } \cdot \operatorname* { P r } [ \mathcal { M } ( D ^ { \prime } ) \in$ $S ] + \delta \ [ 1 0 ]$ . The advantage of this framework lies in providing precise privacy parameters and composability: $k \left( \varepsilon , \delta \right) \mathrm { - D P }$ operations provide $( k \varepsilon , k \delta ) – \mathrm { D P }$ guarantee under basic composition. Vuvuzela (2015) and Stadium (2017) first applied differential privacy to large-scale messaging system metadata protection [20, 21]. NetShaper (2024) first established a formal differential privacy framework for network side-channel defense [11]. The key theoretical contribution of this work is connecting abstract ε privacy parameters with concrete system performance metrics (bandwidth, latency) through computable mathematical relationships. Specifically, given a privacy budget ε and network conditions, NetShaper can compute the minimum bandwidth overhead and latency increment required to achieve that privacy guarantee. This framework transforms the qualitative tradeoff of “privacy vs. performance” into an optimizable mathematical problem. However, this approach still assumes “a certain degree of leakage is acceptable” (encoded through $\varepsilon > 0 )$ , rather than proving the inevitability of side channels as byproducts of functional implementation from a strict mathematical perspective.

Research on website fingerprinting attacks and provable defenses provides empirical foundations and theoretical attempts for understanding side channels. Early website fingerprinting attacks from Hintz (2002) on traffic analysis of encrypted web pages [6] to Panchenko et al. (2011) using support vector machines [22] gradually demonstrated the effectiveness of side channels. Dyer et al. (2012) argued that most “efficient” traffic shaping schemes still fail due to observable side channels, proposing the BuFLO baseline defense with fixed rate, constant-length packets, and minimum duration strategies [23]. Cai et al. (2014) established an attack-agnostic evaluation framework and bandwidth lower bound, proposing the Tamaraw defense based on this: separate rate fixing for upstream and downstream with block-based padding, providing provable upper bounds on attack accuracy [24]. Wang and Goldberg (2017) proposed the Walkie-Talkie defense, using half-duplex burst shaping and pairwise obfuscation mechanisms, with measured average bandwidth overhead of about 31% and latency increase of about 34% [25]. Huang et al. (2025) proposed asymmetric defense (STAP) reducing attack accuracy to 48.3% with only 18% bandwidth overhead [26]. Wright et al. (2009) formalized traffic shaping as a convex optimization problem: given source distribution X and target distribution Y , find transformation matrix $A \geq 0$ such that $A X = Y$ (where $\textstyle \sum _ { i } A _ { i j } = 1$ ensures each column is a probability distribution), while minimizing expected bandwidth overhead $\begin{array} { r } { \sum _ { i , j } x _ { j } a _ { i j } \vert s _ { i } - s _ { j } \vert } \end{array}$ , where $s _ { i } , s _ { j }$ are packet sizes [27]. These works revealed the theoretical costs of defense but only targeted the specific scenario of website fingerprinting, did not establish general efficiency-leakage relationships, and did not explain why side channels necessarily exist in the absence of defense.

Quantification of mutual information leakage provided information-theoretic tools for side-channel analysis. Li et al. (2018) first systematically applied mutual information $I ( X ; Y )$ to quantify website fingerprinting leakage at ACM CCS [9]. In experiments on 100 websites in a closed Tor network environment, they found that even though Tor uses encryption and obfuscation techniques, traffic features still leak substantial website information. Information leakage $I ( F ; W )$ from individual features reaches up to 3.45 bits (from the rounded outbound packet count feature), 54.55% of features leak less than 1 bit, while combined multiple features achieve total information leakage of approximately 6.6 bits, approaching the theoretical limit $\log _ { 2 } 1 0 0 \approx 6 . 6 4$ bits. Cherubin (2017) proposed (ξ, Φ)-privacy metrics based on Bayes error lower bounds, defining defense security from an information-theoretic perspective [28]. These works revealed the phenomenon of information leakage persisting after encryption but did not explain its inevitability from a system design perspective—namely, why $I ( X ; Y )$ is necessarily greater than zero in encryption systems satisfying practical conditions?

Unlike this direct approach of measuring leakage using mutual information or Bayes error lower bounds, Fu et al. and subsequent works [29–31] model encrypted traffic features as random variables or signals, performing differential entropy, information loss, KL divergence, and separability/robustness analysis in frequency-domain spectral features, length patterns, or flow interaction graph spaces, focusing on evaluating the effectiveness of given features and detection methods in specific tasks such as malicious traffic detection and tunnel traffic identification. In contrast, this paper adopts a system-level perspective of composite channel–mutual information lower bounds, discussing whether encrypted traffic side-channel leakage is “inevitable” and its theoretical lower bound without pre-fixing feature forms.

Formal security analysis of anonymous systems attempts to prove privacy guarantees in more rigorous frameworks. Camenisch and Lysyanskaya (2005) formalized onion routing in the Universal Composability (UC) framework, providing composable security definitions [32]. Feigenbaum et al. (2007) modeled onion routing using probabilistic I/O automata, providing formal anonymity analysis against active timing attacks [33]. Danezis and Goldberg’s (2009) Sphinx model provides compact message formats for mix networks, proving unlinkability and path length hiding under the random oracle model [34]. These formal methods provide rigorous security proofs under specific threat models but mainly target security analysis of specific anonymity protocols, without establishing a general theoretical framework from an information-theoretic perspective for the inevitability of side-channel leakage in encrypted communications.

Despite significant progress in respective fields, obvious gaps remain in the theoretical foundation of side-channel existence: (1) Lack of formal causal framework—how to rigorously model the information propagation process from application semantics to observable features? How to mathematically characterize the layer-by-layer effects of encryption, encapsulation, and transmission? (2) Intrinsic connection between efficiency constraints and leakage unclear—how does efficiency prioritization in system design necessarily lead to side channels? Under what verifiable conditions is leakage inevitable? (3) Lack of computable leakage boundaries—given system parameters, what is the lower bound of side-channel leakage? How to predict actual attack performance from theoretical lower bounds? This paper systematically fills these theoretical gaps by constructing formal models, proving existence theorems, and establishing explicit lower bounds, providing a rigorous mathematical foundation for understanding the fundamental causes of side channels.

## 3 Formal Model for Side-Channel Analysis

## 3.1 Basic Definitions and Modeling Conventions

The core approach of this paper is to abstract the entire process of “generation, encapsulation, encryption, transmission, observation” as a composite channel consisting of measurable mappings and random channels, making the mutual information between semantic variables and observable features strictly definable and characterizable by the data processing inequality. We first introduce the basic definitions and conventions of the modeling.

Time and Randomness: Time is modeled as the continuous non-negative axis $\mathbb { T } = \mathbb { R } _ { > 0 }$ . All random variables (semantic X, application-side randomness $U _ { A }$ , protocolside $U _ { \Pi }$ , encryption-side $U _ { \Phi }$ , network-side $U _ { N }$ , observation-side $U _ { \Theta } )$ are defined on a common probability space $\left( \Omega _ { 0 } , \mathcal { F } _ { 0 } , \mathbb { P } \right)$ ; the specific construction of this space does not affect subsequent analysis and is used to ensure the well-definedness of joint distributions and conditional expectations.

Point Processes and Sequence Representations: Point processes $\Xi _ { A } , \Xi _ { P } , \Xi _ { C } , \Xi _ { N }$ (for intuition, subsequently referred to as “message sequences, plaintext packet sequences, ciphertext packet sequences, arrival packet sequences”) and observed features Y have sample paths taking values in corresponding measurable spaces.

Unified Trajectory Space and Metric: To avoid inconsistent domains for crosslayer statistics, we introduce a unified marked point process trajectory space Z (e.g., using finite marked counting measure space, or embedding window-within trajectories into Skorokhod space). Let $e _ { P } : \mathrm { r a n g e } ( \Xi _ { P } ) \to \mathcal { Z } , e _ { N } : \mathrm { r a n g e } ( \Xi _ { N } ) \to \mathcal { Z }$ be measurable embeddings from each layer to Z. All window-level statistics below are viewed as measurable functions $\varphi : { \mathcal { Z } }  [ - M , M ]$ . The metric d is defined on $\mathcal { Z }$ , simultaneously measuring timing and marking (length, direction) differences, and is compatible with the Lipschitz conditions below. To avoid unnecessary technical burden, we assume $x , y$ , $\mathrm { r a n g e } ( \Xi _ { A } )$ , $\mathrm { r a n g e } ( \Xi _ { P } )$ , $\mathrm { r a n g e } ( \Xi _ { C } )$ , $\mathrm { r a n g e } ( \Xi _ { N } )$ , and $\mathcal { Z }$ are all standard Borel spaces.

To clearly distinguish “system design” from “external observation”, we provide the following definition of side-channel analysis model:

Definition 1 (Side-Channel Analysis Model). The side-channel analysis model is denoted as $\Sigma = ( \Gamma , \Omega )$ , where the encrypted communication model is denoted as $\Gamma = ( A , \Pi , \Phi , N )$ , consisting of four causal operators: application generation A, protocol encapsulation Π, encryption transformation Φ, network transmission N; Ω is the observation model, characterizing the side-channel analyst’s passive monitoring and feature extraction capabilities at various network layers and positions.

Under this definition, system Γ only determines “how to generate and transmit ciphertext”, and observation model Ω only determines “what the analyst can see”. The leakage amount L(Γ, Ω) is the result of the composite action of both. This separation allows the existence theorem below to hold under the weakest system and observation assumptions.

## 3.2 Encrypted Communication Model

The encrypted communication model $\Gamma = ( A , \Pi , \Phi , N )$ consists of four causal operators that act on message point processes and packet sequences on the time axis. We characterize these transformations as causally measurable mappings, only requiring them to maintain temporal causality and measurability, without making strong assumptions about the specific forms of probability distributions (such as independence or stationarity).

## (1) Application Layer (Operator A)

Let X be the application semantic space (such as website ID, application category, video content, etc.), and let $X \in { \mathcal { X } }$ be the semantic variable. The application generates a message sequence on the time axis:

$$
\Xi_ {A} = \left\{\left(\tau_ {k}, m _ {k}\right) \right\} _ {k \geq 1}, \quad \tau_ {k} \in \mathbb {T}, m _ {k} \in \mathcal {M}, \tag {2}
$$

which is jointly determined by X and exogenous noise, and can be written as a causally measurable mapping $\Xi _ { A } = \mathcal { G } _ { A } ( \boldsymbol { X } , \boldsymbol { U } _ { A } )$ . Here M is the message set, and $U _ { A }$ is applicationside randomness (user behavior, business logic jitter, etc.). We do not require stationarity or independence, only that $\mathcal { G } _ { A }$ is causal and measurable.

## (2) Protocol Layer (Operator Π)

The protocol stack maps the message sequence $\Xi _ { A }$ to a segmented and encapsulated plaintext packet sequence:

$$
\Xi_ {P} = \{(t _ {i}, \ell_ {i}, \mathrm{dir} _ {i}, h _ {i}, b _ {i}) \} _ {i \geq 1}, \tag {3}
$$

where $t _ { i } ~ \in ~ \mathbb { T }$ is the sending time, $\ell _ { i } = | h _ { i } | + | b _ { i } |$ is the length, di ${ \mathfrak { c } } _ { i } \in \{ \uparrow , \downarrow \}$ is the direction, $h _ { i }$ is the concatenation of headers from various layers, and $b _ { i }$ is the plaintext payload. Expressed as a causal mapping $\Xi _ { P } = \Pi ( \Xi _ { A } , U _ { \Pi } )$ , where $U _ { \Pi }$ represents protocolside randomness (Nagle, segmentation boundaries, congestion control adaptation, $\mathrm { e t c . ) }$ . Π maintains causality: $t _ { i }$ depends only on $\{ ( \tau _ { k } , m _ { k } ) : \tau _ { k } \leq t _ { i } \}$ and past protocol state.

## (3) Encryption Layer (Operator Φ)

Encryption maps the plaintext packet sequence $\Xi _ { P }$ to a ciphertext packet sequence:

$$
\Xi_ {C} = \{(t _ {i} ^ {\prime}, \ell_ {i} ^ {\prime}, \mathrm{dir} _ {i}, h _ {i} ^ {\prime}, c _ {i}) \} _ {i \geq 1} = \Phi (\Xi_ {P}, U _ {\Phi}), \tag {4}
$$

where $h _ { i } ^ { \prime }$ are visible or semi-visible header fields, and $c _ { i }$ is the ciphertext payload. We only use two general properties: (i) Semantic independence: under the ideal cipher assumption, given input length and public parameters, $c _ { i }$ is conditionally independent of plaintext content; (ii) Determinism of length transformation: there exists a deterministic function $g _ { \mathrm { l e n } }$ such that $\ell _ { i } ^ { \prime } = g _ { \mathrm { l e n } } ( \ell _ { i } ; \theta _ { \Phi } )$ , where $\theta _ { \Phi }$ contains block size, record overhead, optional padding, etc. Real-world protocols (TLS 1.3, QUIC) satisfy this intuitive property: content is scrambled, but length and timing are only affected by minor alignment and record formatting. Time mapping maintains causality: $t _ { i } ^ { \prime } \geq t _ { i }$ , and $t _ { i } ^ { \prime } - t _ { i }$ is determined by implementation and scheduling.

## (4) Network Layer (Operator N)

The network transmits the sender-side ciphertext sequence $\Xi _ { C }$ as an arrival packet sequence on the observation path:

$$
\Xi_ {N} = \{(\tilde {t} _ {j}, \tilde {\ell} _ {j}, \mathrm{dir} _ {j}, \tilde {h} _ {j}, \tilde {c} _ {j}) \} _ {j \geq 1} = N (\Xi_ {C}, U _ {N}), \tag {5}
$$

where $U _ { N }$ characterizes uncertainties such as queuing, routing, packet loss, retransmission, reordering, framing, and multiplexing. N is viewed as a causal channel of a random timevarying queuing network; independence or Markov assumptions are not required.

A fundamental assumption about Γ is that it produces statistically distinguishable traffic patterns at the protocol layer. To this end, we provide the following definition of semantic distinguishability.

Definition 2 (Semantic Distinguishability). Given window $T > 0$ , the system Γ is said to have $\bar { \Delta }$ -distinguishability in the $\mathcal { Z }$ representation induced at the protocol layer if there exist a semantic pair x $\neq x ^ { \prime } \in \mathcal { X }$ and a bounded measurable statistic $\varphi : { \mathcal { Z } }  [ - M , M ]$ such that

$$
\left. \right.\left| \mathbb {E} \left[ \varphi \left(e _ {P} \left(\Xi_ {P} \mid_ {[ 0, T ]}\right)\right) \mid X = x \right] - \mathbb {E} \left[ \varphi \left(e _ {P} \left(\Xi_ {P} \mid_ {[ 0, T ]}\right)\right) \mid X = x ^ {\prime} \right]\right| \geq \bar {\Delta}. \tag {6}
$$

The system Γ is said to be distinguishable at the protocol layer if there exists $\bar { \Delta } > 0$ such that it has ∆¯ -distinguishability.

This definition characterizes an intrinsic property of the system: different semantics, after application generation and protocol encapsulation, produce sufficiently large differences in the conditional expectations of some statistic in the unified trajectory space $\mathcal { Z }$ . The existence of $\bar { \Delta }$ excludes the degenerate case of “arbitrarily small expectation differences”, ensuring that distinguishability is operationally meaningful in a statistical sense. Common statistics $\varphi$ include: total bytes in window, ratio of upstream to downstream packets, weighted average of packet intervals, etc. Different application semantics often exhibit differences in these statistics: high byte counts for video streams, balanced upstream/downstream ratios for instant messaging, short-term high-density patterns for web browsing—these patterns maintain statistical separability even after protocol encapsulation.

Real-world encrypted communication system design follows the efficiency-first principle: maximizing resource utilization efficiency to support upper-layer business needs while ensuring cryptographic security. Business has quantifiable requirements for multiple performance dimensions:

• Bandwidth overhead: additional bytes introduced by the protocol should be controlled within an acceptable range (e.g., TLS 1.3 approximately 5%)  
• End-to-end latency: delays introduced by encryption, framing, and scheduling should be below application perception thresholds (e.g., web pages <200ms, VoIP <150ms)  
• Throughput: effective throughput should not significantly decrease due to padding or artificial delays  
• Protocol compatibility: must be compatible with existing network infrastructure (MTU, congestion control, NAT traversal, etc.)

The direct consequence of efficiency-first design is: the mapping from plaintext protocol layer $\Xi _ { P }$ to arrival packet sequence $\Xi _ { N }$ necessarily maintains non-degeneracy.

Definition 3 (Mapping Non-Degeneracy). On a fixed window [0, T ], the encrypted communication system Γ is said to have window-level mapping non-degeneracy if there exists a constant CT < ∞ such that for all x ∈ X ,

$$
\mathbb {E} \left[ d \left(e _ {P} \left(\Xi_ {P} | _ {[ 0, T ]}\right), e _ {N} \left(\Xi_ {N} | _ {[ 0, T ]}\right)\right) \mid X = x \right] \leq C _ {T}. \tag {7}
$$

Intuitively, this requires that encryption and transmission mappings do not excessively distort the statistical structure of the plaintext packet sequence—the joint distribution of marks (length, direction) and timing of the point process remains “close” before and after mapping.

Non-degeneracy directly stems from efficiency constraints, such as excessive padding causing the metric to diverge in the length component (bandwidth overhead exceeding limits), excessive delays or jitter causing the metric to diverge in the timing component (end-to-end latency exceeding limits, breaking real-time properties), or completely scrambling the marks and timing structure of the packet sequence causing the metric to diverge (protocol semantics broken, business unusable). “Window-level” means the metric acts on point process segments within a finite time window [0, T ] (e.g., 10 seconds or one session), allowing single-packet perturbations (e.g., TCP retransmissions, reordering) but constraining cumulative deviation. The specific form of metric d can be varied, as long as it can capture the joint statistical structure of length, timing, and direction of point processes. The conclusions of this paper do not depend on specific metric choices; the establishment of subsequent theorems relies only on abstract non-degeneracy—namely, the existence of some suitable metric d such that $\mathbb { E } [ d ] \leq C _ { T } < \infty$ . In typical network scenarios, a commonly used choice is to define d as a weighted sum of “length deviation + packet count deviation + latency deviation”, or implicit distances in some high-dimensional space of flow features characterized by machine learning and deep learning. In this case, $C _ { T }$ can be understood as the maximum acceptable deviation jointly defined by bandwidth, packet count overhead, and end-to-end latency jitter in that window.

The above semantic distinguishability and mapping non-degeneracy jointly constitute intrinsic properties of encrypted communication systems. They characterize “the statistical variability that the system necessarily retains under the premise of business availability”. The next section will discuss how side-channel analysts capture these properties through observation model Ω, ultimately deriving the existence of side-channel leakage.

## 3.3 Observation Model

The observation model Ω characterizes the side-channel analyst’s passive access capabilities to various network layers and positions, as well as the feature extraction process from arrival packet sequences. Although observers cannot directly access the plaintext protocol layer $\Xi _ { P }$ , they can infer semantic information by observing arrival packet sequences $\Xi _ { N }$ and extracting features. This section defines the composition of the observation model, the generation of observed features, and non-degeneracy conditions ensuring that the observation channel does not degenerate to a constant.

Definition 4 (Observation Model). The side-channel analysis model $\Omega = ( \mathcal { L } _ { \mathrm { a c c } } , \mathcal { O } _ { \mathrm { a c c } } , \Theta )$ consists of three components:

• $\mathcal { L } _ { \mathrm { a c c } }$ : Accessible layer set (such as IP layer, UDP/TCP layer, QUIC/TLS record layer, etc.)  
• $\mathcal { O } _ { \mathrm { a c c } }$ : Observable position set (links, switch ports, host network interfaces, etc.)  
• Θ: Causally measurable feature extraction operator

Given arrival packet sequence $\Xi _ { N }$ , the observer obtains feature sequence through Θ:

$$
Y = \Theta (\Xi_ {N}; \mathcal {L} _ {\mathrm{acc}}, \mathcal {O} _ {\mathrm{acc}}, U _ {\Theta}), \tag {8}
$$

where $U _ { \Theta }$ represents observation-side uncertainty (timestamp precision, sampling strategy, counting granularity, etc.).

The feature extraction operator Θ typically includes the following operations: extracting packet length sequences, computing packet arrival time intervals, counting upstream/downstream packet ratios, constructing burst pattern descriptors, computing windowlevel statistics (total bytes, packet counts, rates, etc.). The specific form of Θ depends on the observer’s technical capabilities and analysis objectives but must maintain causality: observed features at time t depend only on arrival packets at or before time t.

Connecting system model Γ and observation model Ω end-to-end yields the complete causal chain from semantics to observed features, as shown in Figure 1:

$$
X \xrightarrow {\mathcal {G} _ {A}} \Xi_ {A} \xrightarrow {\Pi} \Xi_ {P} \xrightarrow {\Phi} \Xi_ {C} \xrightarrow {N} \Xi_ {N} \xrightarrow {\Theta} Y. \tag {9}
$$

where X is the sensitive semantic variable, $\Xi _ { A } , \Xi _ { P } , \Xi _ { C } , \Xi _ { N }$ are message sequence, plaintext packet sequence, ciphertext packet sequence, arrival packet sequence (all point processes), and Y is the observed feature sequence. This causal chain induces two key properties:

![](images/d8e4d4705bcdbae6e9bddd11cd38047fe0982f61b37895882df0fd9bd84e80b1.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph Semantic
        A["App G_A"]
        B["Message Ξ_A {(\tau_k, m_k)}"]
        C["Protocol Ξ_P (t_i, ℓ_i, dir_i)"]
        D["Encrypt Φ"]
        E["Network N"]
        F["Observe Θ"]
    end

    subgraph Message
  B --> C
  C --> D
  E --> F
    end

    subgraph Protocol
  B --> C
  C --> D
  E --> F
    end

    subgraph Encrypt
  D --> E
  F --> E
    end

    subgraph Network
  E --> F
    end

    subgraph Observe
  F --> E
    end

  U_A["User_A"] --> A
  U_A --> B
  U_A --> C
  U_A --> D
  U_A --> E
  U_A --> F

  U_Π[User_Π] --> B
  U["U_Π"] --> C
  U --> D
  U --> E
  U --> F

  U_Φ[User_Φ] --> C
  U2["U_Φ"] --> D
  U2 --> E
  U2 --> F

  U_N["User_N"] --> E
  U_N --> F

  U_Θ[User_Θ] --> F

  X["X Website/App"] --> A
  Y["Σ_A {(\tau_k, m_k)}"] --> B
  Z["Time step t_i, t'_i, c_i"] --> C
  AA["Time step t_j, t'_j"] --> E
  AB["Statistics"] --> F

  X --> AC["Markov Chain: X → Ξ_A → Ξ_P → Ξ_C → Ξ_N → Y"]
  Y --> AC
  AC --> AD["Observation Ω"]
```
</details>

Figure 1: Complete causal chain from semantics to observed features

Proposition 1 (Existence and Measurability of Observation Channel). Under the conditions that the above spaces are standard Borel spaces and $N , \Theta$ are random kernels (or compositions of measurable mappings and random kernels), there exists a random kernel $K _ { \Sigma } ( \mathrm { d } y \mid x )$ from X to Y such that $Y \mid X = x \sim K _ { \Sigma } ( \cdot \mid x )$ , hence $I ( X ; Y )$ is well-defined. This conclusion stems from the closure of random kernels under composition and the existence of regular conditional probability.

Proof. On standard Borel spaces, compositions of measurable mappings and random kernels remain random kernels, and regular conditional probability exists [35]. Since $\mathcal { G } _ { A } , \Pi , \Phi , \Theta$ are causally measurable mappings and N is a causal random channel, their composition yields $K _ { \Sigma } ( \mathrm { d } y \mid x )$ . □

Proposition 2 (Data Processing Structure). The composite chain induces the Markov relationship

$$
X \rightarrow \Xi_ {A} \rightarrow \Xi_ {P} \rightarrow \Xi_ {C} \rightarrow \Xi_ {N} \rightarrow Y, \tag {10}
$$

thus $f o r$ any intermediate layer variable Z, $I ( X ; Y ) \leq I ( X ; Z )$ . In particular, letting $Y _ { \mathrm { r a w } } = \Xi _ { P } o r Y _ { \mathrm { r a w } } = \Xi _ { C }$ , we have $I ( X ; Y ) \leq I ( X ; Y _ { \mathrm { r a w } } )$ .

Proof. By causality and measurability, each arrow in the chain is a composition of random kernels, satisfying the Markov property. By the data processing inequality [19], for the Markov chain $X  \Xi _ { A }  \Xi _ { P }  \Xi _ { C }  \Xi _ { N }  Y$ , we have $I ( X ; Y ) \leq I ( X ; Z )$ for any intermediate variable Z. □

A key property of observation model Ω is whether it can preserve the statistical variability of arrival packet sequences. If the observation mapping Θ compresses all inputs to a constant (e.g., only recording “traffic exists” while discarding all length, timing, direction information), then regardless of how rich the statistical patterns produced by system Γ, observed features Y cannot reflect semantic differences. To exclude this degenerate case, we provide the following definition:

Definition 5 (Non-Degenerate Observation (with respect to statistic used)). Given window T and statistic φ from Definition ${ \mathcal { Q } } ,$ the observation model Ω is said to be nondegenerate with respect to this statistic if there exist a constant $\rho \in ( 0 , 1 ]$ and a bounded measurable mapping $\psi : \mathcal { V }  [ - 1 , 1 ]$ (depending only on T and $\varphi ,$ , independent of specific semantic pairs and their priors) such that for any semantic pair $x \neq x ^ { \prime } \in \mathcal { X }$ and any $\delta > 0$ ,

$$
\begin{array}{l} \left. \right.\left| \mathbb {E} \left[ \varphi \left(e _ {N} \left(\Xi_ {N} \mid_ {[ 0, T ]}\right)\right) \mid X = x \right] - \mathbb {E} \left[ \varphi \left(e _ {N} \left(\Xi_ {N} \mid_ {[ 0, T ]}\right)\right) \mid X = x ^ {\prime} \right]\right| \geq \delta \tag {11} \\ \Rightarrow \quad \left| \mathbb {E} [ \psi (Y) \mid X = x ] - \mathbb {E} [ \psi (Y) \mid X = x ^ {\prime} ] \right| \geq \rho \delta . \\ \end{array}
$$

Intuitively, this requires that the observation mapping preserves at least a positive proportion of the conditional expectation difference of statistic $\varphi - e v e n$ if there is information loss $( \rho < 1 )$ , statistical differences are not completely erased $( \rho > 0 )$ . The constant ρ and mapping ψ depend only on the observation model Ω, window T , and the structure of statistic φ, not on the specific semantic pairs being compared or their prior distributions, reflecting an inherent property of the observation model.

This definition excludes extremely degenerate observation models, such as: binary indicators recording only “whether there is traffic”, aggregators counting only total session duration while discarding all fine-grained information, constant mappings returning fixed feature vectors for all traffic, etc. Real-world side-channel analysis models typically satisfy non-degeneracy because observers wish to maximize extractable information and will retain key dimensions such as packet length, timing, and direction.

Thus far, we have constructed the complete side-channel analysis model: system Γ produces distinguishable statistical patterns at the protocol layer, which, after encryption and transmission satisfying mapping non-degeneracy, arrive at the observation path; the non-degenerate observation model Ω captures these patterns and extracts features Y . The next section will prove, based on this framework, that under the premise that the system satisfies window-level mapping non-degeneracy (Definition 3), the mutual information $I ( X ; Y )$ between observed features and semantics is necessarily strictly greater than zero, making side-channel leakage inevitable.

## 4 Side-Channel Leakage Existence Theorem

Based on the modeling framework of the previous section, this section provides a rigorous statement and proof of the inevitability of side-channel leakage. We first establish a stable propagation chain of expectation differences for binary semantic pairs and provide an explicit lower bound on mutual information, then generalize to the general case of multi-semantic spaces. The entire argument relies only on the causally measurable composite channel structure, the data processing inequality, and the stable propagation of bounded metrics, without depending on specific protocol details or particular metric choices.

## 4.1 Technical Strengthening Assumptions

Let X be the application semantic variable and Y be the observable features obtained by the observer under model $\Sigma = ( \Gamma , \Omega )$ . The previous section provided the Markov chain $X  \Xi _ { A }  \Xi _ { P }  \Xi _ { C }  \Xi _ { N }  Y$ and corresponding random kernel $K _ { \Sigma } ( \mathrm { d } y \mid x )$ (Proposition 1).

Definition 2 provided the basic concept of semantic distinguishability: there exists a statistic $\varphi$ on the unified trajectory space $\mathcal { Z }$ induced at the protocol layer such that conditional expectation differences for different semantics are $\ge \bar { \Delta }$ . To ensure this distinguishability can stably propagate to the observation layer, we need to impose Lipschitz continuity constraints on statistic $\varphi \mathrm { : }$

Assumption 1 (Lipschitz Robustness). The $\varphi$ in Definition $\mathcal { Q }$ is $L _ { \varphi } – L i p s c h i t z$ continuous with respect to metric d on $\mathcal { Z } .$

$$
| \varphi (z) - \varphi (z ^ {\prime}) | \leq L _ {\varphi} d (z, z ^ {\prime}), \quad \forall z, z ^ {\prime} \in \mathcal {Z}. \tag {12}
$$

This assumption ensures the stability of statistics under trajectory perturbations— small changes in trajectories lead only to small changes in statistics. Common bounded Lipschitz statistics include: truncated versions of total bytes in window, ratios of upstream/downstream packets (naturally bounded), saturated versions of packet arrival intervals, etc. In practice, the vast majority of statistical features used for traffic analysis can be converted into Lipschitz continuous functions through appropriate truncation or normalization.

## 4.2 Side-Channel Leakage Theorem for Binary Semantic Pairs

We first establish a strict leakage lower bound for binary semantic pairs. Denote the leakage amount as $L ( \Gamma , \Omega ) = I ( X ; Y )$ .

Theorem 1 (Binary Semantic Side-Channel Leakage Theorem). Under the conditions of Proposition 1, fix window $T > 0$ . Suppose there exists a distinguishable semantic pair $x \neq x ^ { \prime } \in \mathcal { X }$ satisfying the prior positive mass condition $^ { \circ } ( X = x ) > 0 , \mathbb { P } ( X = x ^ { \prime } ) > 0$ . If the system satisfies the following conditions:

(i) Mapping Non-Degeneracy (instantiation of Definition 3 for the semantic pair): there exist metric d and constant $C < \infty$ such that for this semantic pair,

$$
\begin{array}{l} \max \left\{\mathbb {E} \Big [ d \big (e _ {P} (\Xi_ {P} | _ {[ 0, T ]}), e _ {N} (\Xi_ {N} | _ {[ 0, T ]}) \big) \Big | X = x \right], \\ \mathbb {E} \left[ d \left(e _ {P} \left(\Xi_ {P} | _ {[ 0, T ]}\right), e _ {N} \left(\Xi_ {N} | _ {[ 0, T ]}\right)\right) \mid X = x ^ {\prime} \right] \rbrace \leq C. \tag {13} \\ \end{array}
$$

(ii) Semantic Distinguishability (Definition 2): there exist $\bar { \Delta } > 0$ and bounded measurable statistic $\varphi : { \mathcal { Z } }  [ - M , M ]$ such that

$$
\left. \right.\left| \mathbb {E} \left[ \varphi \left(e _ {P} \left(\Xi_ {P} \mid_ {[ 0, T ]}\right)\right) \mid X = x \right] - \mathbb {E} \left[ \varphi \left(e _ {P} \left(\Xi_ {P} \mid_ {[ 0, T ]}\right)\right) \mid X = x ^ {\prime} \right]\right| \geq \bar {\Delta}. \tag {14}
$$

(iii) Lipschitz Robustness (Assumption 1): the above statistic $\varphi$ is $L _ { \varphi } – L i p s c h i t z \ c o n .$ - tinuous with respect to metric d on $\mathcal { Z }$ :

$$
| \varphi (z) - \varphi (z ^ {\prime}) | \leq L _ {\varphi} d (z, z ^ {\prime}), \quad \forall z, z ^ {\prime} \in \mathcal {Z}. \tag {15}
$$

(iv) Non-Degenerate Observation (Definition 5 for statistic $\varphi )$ : there exist constant $\rho \in \left( 0 , 1 \right]$ and bounded measurable $\psi : \mathcal { V }  [ - 1 , 1 ]$ (depending only on $T$ and $\varphi ,$ independent of semantic pairs) such that for any semantic pair a $\neq b \in { \mathcal { X } }$ ,

$$
\left. \right.\left| \mathbb {E} \left[ \varphi \left(e _ {N} \left(\Xi_ {N} \mid_ {[ 0, T ]}\right)\right) \mid X = a \right] - \mathbb {E} \left[ \varphi \left(e _ {N} \left(\Xi_ {N} \mid_ {[ 0, T ]}\right)\right) \mid X = b \right]\right| \geq \delta \tag {16}
$$

$$
\Rightarrow \quad \left| \mathbb {E} [ \psi (Y) \mid X = a ] - \mathbb {E} [ \psi (Y) \mid X = b ] \right| \geq \rho \delta .
$$

(v) Distinguishability Propagation Condition: the metric deviation bound C, Lipschitz constant $L _ { \varphi }$ , and distinguishability margin $\bar { \Delta }$ satisfy

$$
C <   \frac {\bar {\Delta}}{2 L _ {\varphi}}. \tag {17}
$$

Then the mutual information between observed features and semantics satisfies $I ( X ; Y ) >$ 0, with explicit lower bound

$$
I (X; Y) \geq \frac {2}{\ln 2} \mathbb {P} (X = x) \mathbb {P} (X = x ^ {\prime}) \left(\frac {\rho [ \bar {\Delta} - 2 L _ {\varphi} C ]}{2}\right) ^ {2}. \tag {18}
$$

In particular, restricting to the binary equal-prior subproblem $( i . e . , X \in \{ x , x ^ { \prime } \}$ and $\mathbb { P } ( X = x ) = \mathbb { P } ( X = x ^ { \prime } ) = 1 / 2 )$ , the lower bound becomes

$$
I (X; Y) \geq \frac {1}{2 \ln 2} \left(\frac {\rho [ \bar {\Delta} - 2 L _ {\varphi} C ]}{2}\right) ^ {2}. \tag {19}
$$

The theorem focuses on analysis of binary semantic pairs $( x , x ^ { \prime } )$ , which is an essential requirement of the proof technique—arguments based on Pinsker’s inequality and total variation are naturally pairwise. Condition (i) only requires this semantic pair to satisfy mapping non-degeneracy; in efficiency-prioritized practical systems, if the mapping maintains non-degeneracy for all semantics, it naturally holds for any semantic pair. Condition (v) characterizes the boundary of side-channel existence: the metric deviation $C$ cannot be too large, otherwise the distinguishability at the protocol layer will be completely erased by perturbations during propagation to the network layer. In typical website fingerprinting scenarios, $x$ and $x ^ { \prime }$ can be understood as two semantic classes “visiting website $\mathrm { A } ^ { \prime \prime }$ and “visiting website $\mathrm { B } ^ { \ast }$ , where $\bar { \Delta }$ can be chosen as expectation differences in aggregate statistics such as total bytes, upstream/downstream packet ratios, burst duration/payload within a fixed time window; $C$ corresponds to the average deviation in length and arrival time in the unified trajectory space $\mathcal { Z }$ due to encryption encapsulation, TCP retransmissions, and random jitter within the same window; and $\rho$ reflects the proportion of these differences that the observation link can still preserve under limitations such as sampling granularity and timestamp precision.

The proof requires the following lemma:

Lemma 1 (Relationship between Expectation Difference and Total Variation). Let $f$ : ${ \cal { S } }  [ - M , M ]$ be a bounded measurable function, and $P , Q$ be two probability measures on $\textit { S . } \textit { I f }$

$$
\left| \mathbb {E} _ {P} [ f ] - \mathbb {E} _ {Q} [ f ] \right| \geq \delta , \tag {20}
$$

then the total variation distance satisfies

$$
\operatorname{TV} (P, Q) \geq \frac {\delta}{2 M}. \tag {21}
$$

Proof. By the dual representation of total variation,

$$
\operatorname{TV} (P, Q) = \frac {1}{2} \sup _ {\| g \| _ {\infty} \leq 1} | \mathbb {E} _ {P} [ g ] - \mathbb {E} _ {Q} [ g ] |. \tag {22}
$$

For bounded function $f : \cal { S } \to [ - M , M ]$ , normalize $g : = f / M$ to get $\| g \| _ { \infty } = 1$ , therefore

$$
| \mathbb {E} _ {P} [ f ] - \mathbb {E} _ {Q} [ f ] | = M | \mathbb {E} _ {P} [ g ] - \mathbb {E} _ {Q} [ g ] | \leq M \cdot 2 \cdot \mathrm{TV} (P, Q) = 2 M \cdot \mathrm{TV} (P, Q). \tag {23}
$$

$\begin{array} { r } { \mathrm { I f ~ } | \mathbb { E } _ { P } [ f ] - \mathbb { E } _ { Q } [ f ] | \geq \delta , \mathrm { t h e n ~ T V } ( P , Q ) \geq \frac { \delta } { 2 M } . } \end{array}$

Proof of Theorem 1. The proof unfolds along ${ } ^ { \mathrm { { } ^ { \ast } } } \bar { \Delta }  ( L _ { \varphi } )  d  ( C _ { T } )  \rho  I ( X ; Y ) ^ { \mathrm { { \ast } } }$ : using Lipschitz property to bound protocol-layer differences to trajectory space, then absorbing perturbations using $C _ { T }$ and characterizing observable proportion with $\rho ,$ finally concatenating inequalities to obtain the mutual information lower bound. The proof consists of four steps: establishing expectation difference at protocol layer $\Xi _ { P } .$ , propagating to network layer $\Xi _ { N }$ , propagating to observation layer $Y .$ , and finally converting to mutual information. The entire derivation proceeds in the unified trajectory space $\mathcal { Z } .$ , relying on the distinguishability propagation chain formed by conditions ${ \mathrm { ( i ) - ( v ) } }$ .

Step 1: Expectation difference at protocol layer is directly given by condition (ii).

By condition (ii) semantic distinguishability, there exists bounded statistic $\varphi : { \mathcal { Z } } $ $[ - M , M ]$ satisfying

$$
\left| \mathbb {E} [ \varphi (e _ {P} (\Xi_ {P} | _ {[ 0, T ]})) \mid X = x ] - \mathbb {E} [ \varphi (e _ {P} (\Xi_ {P} | _ {[ 0, T ]})) \mid X = x ^ {\prime} ] \right| \geq \bar {\Delta}. \tag {24}
$$

Step 2: Propagation of expectation difference from protocol layer to network layer.

Introduce simplified notation: $z _ { P } : = e _ { P } ( \Xi _ { P } | _ { [ 0 , T ] } ) , z _ { N } : = e _ { N } ( \Xi _ { N } | _ { [ 0 , T ] } )$ as trajectory representations in unified space $\mathcal { Z }$ .

By condition (i) mapping non-degeneracy, for semantic pair $x \neq x ^ { \prime } \in \mathcal { X }$ ,

$$
\mathbb {E} \big [ d (z _ {P}, z _ {N}) \big | X = x \big ] \leq C, \quad \mathbb {E} \big [ d (z _ {P}, z _ {N}) \big | X = x ^ {\prime} \big ] \leq C. \tag {25}
$$

By condition (iii) Lipschitz robustness, for any trajectories $z _ { P } , z _ { N } \in \mathcal { Z }$ ,

$$
| \varphi (z _ {P}) - \varphi (z _ {N}) | \leq L _ {\varphi} \cdot d (z _ {P}, z _ {N}). \tag {26}
$$

Taking conditional expectation with respect to $X = x \colon$ :

$$
\begin{array}{l} \left. \right.\left| \mathbb {E} \left[ \varphi \left(z _ {P}\right) \mid X = x \right] - \mathbb {E} \left[ \varphi \left(z _ {N}\right) \mid X = x \right]\right| = \left| \mathbb {E} \left[ \varphi \left(z _ {P}\right) - \varphi \left(z _ {N}\right) \mid X = x \right]\right| \\ \leq \mathbb {E} \big [ | \varphi (z _ {P}) - \varphi (z _ {N}) | \big | X = x \big ] \quad (\text { Jensen's   inequality }) \\ \leq \mathbb {E} \left[ L _ {\varphi} \cdot d (z _ {P}, z _ {N}) \mid X = x \right] \quad (\text {Lipschitz property}) \\ = L _ {\varphi} \cdot \mathbb {E} \big [ d (z _ {P}, z _ {N}) \mid X = x \big ] \\ \leq L _ {\varphi} \cdot C. \quad (\text { Condition   (i) }) \tag {27} \\ \end{array}
$$

Similarly for $X = x ^ { \prime } .$ ,

$$
\left| \mathbb {E} [ \varphi (z _ {P}) \mid X = x ^ {\prime} ] - \mathbb {E} [ \varphi (z _ {N}) \mid X = x ^ {\prime} ] \right| \leq L _ {\varphi} \cdot C. \tag {28}
$$

Applying the triangle inequality:

$$
\begin{array}{l} \left| \mathbb {E} [ \varphi (z _ {N}) \mid X = x ] - \mathbb {E} [ \varphi (z _ {N}) \mid X = x ^ {\prime} ] \right| \\ \geq \left| \mathbb {E} [ \varphi (z _ {P}) \mid X = x ] - \mathbb {E} [ \varphi (z _ {P}) \mid X = x ^ {\prime} ] \right| \\ - \left| \mathbb {E} [ \varphi (z _ {P}) \mid X = x ] - \mathbb {E} [ \varphi (z _ {N}) \mid X = x ] \right| \\ - \left| \mathbb {E} [ \varphi (z _ {P}) \mid X = x ^ {\prime} ] - \mathbb {E} [ \varphi (z _ {N}) \mid X = x ^ {\prime} ] \right| \\ \geq \bar {\Delta} - L _ {\varphi} C - L _ {\varphi} C \\ = \bar {\Delta} - 2 L _ {\varphi} C =: \delta_ {N}. \tag {29} \\ \end{array}
$$

$\begin{array} { r } { C < \frac { \hat { \Delta } } { 2 L _ { \varphi } } } \end{array}$ $\delta _ { N } = \bar { \Delta } - 2 L _ { \varphi } C > 0$

Step 3: Propagation of expectation difference from network layer to observation layer.

By condition (iv) non-degenerate observation, applying to the expectation difference $\delta _ { N } ~ > ~ 0$ obtained in the previous step and semantic pair $( x , x ^ { \prime } )$ , there exists bounded observation statistic $\psi : \mathcal { V }  [ - 1 , 1 ]$ such that

$$
\left| \mathbb {E} [ \psi (Y) \mid X = x ] - \mathbb {E} [ \psi (Y) \mid X = x ^ {\prime} ] \right| \geq \rho   \delta_ {N} = \rho (\bar {\Delta} - 2 L _ {\varphi} C). \tag {30}
$$

Step 4: From expectation difference to mutual information (including prior weighting).

By Lemma 1, applied to observation-layer conditional distributions and statistic ψ : $\mathcal { V }  [ - 1 , 1 ] \ ( \mathrm { i . e . , } \ M = 1 )$ , we obtain

$$
\mathrm{TV} \left(P _ {Y | X = x}, P _ {Y | X = x ^ {\prime}}\right) \geq \frac {\rho \delta_ {N}}{2} = \frac {\rho (\bar {\Delta} - 2 L _ {\varphi} C)}{2}. \tag {31}
$$

For general prior distributions, using the standard relationship between mutual information and total variation of conditional distributions (see [19]),

$$
I (X; Y) \geq \frac {2}{\ln 2} \mathbb {P} (X = x) \mathbb {P} (X = x ^ {\prime}) \mathrm{TV} ^ {2} \left(P _ {Y | X = x}, P _ {Y | X = x ^ {\prime}}\right). \tag {32}
$$

Substituting the total variation lower bound:

$$
I (X; Y) \geq \frac {2}{\ln 2} \mathbb {P} (X = x) \mathbb {P} (X = x ^ {\prime}) \left(\frac {\rho (\bar {\Delta} - 2 L _ {\varphi} C)}{2}\right) ^ {2}. \tag {33}
$$

By condition $\mathrm { ( v ) }$ and the prior positive mass condition, the right-hand side is strictly positive, thus $I ( X ; Y ) > 0$ .

In the binary equal-prior subproblem $( \mathbb { P } ( X = x ) = \mathbb { P } ( X = x ^ { \prime } ) = 1 / 2 )$ , the above becomes

$$
I (X; Y) \geq \frac {2}{\ln 2} \cdot \frac {1}{4} \left(\frac {\rho (\bar {\Delta} - 2 L _ {\varphi} C)}{2}\right) ^ {2} = \frac {1}{2 \ln 2} \left(\frac {\rho (\bar {\Delta} - 2 L _ {\varphi} C)}{2}\right) ^ {2}. \tag {34}
$$

This completes the proof.

![](images/36e08da32136d9db643768330d63042c7f2947cb70ed092f017a64fea136a6a2.jpg)

The mutual information lower bound is prior-dependent: the lower bound of $I ( X ; Y )$ 号 is weighted by the prior mass $\mathbb { P } ( X = x ) \mathbb { P } ( X = x ^ { \prime } )$ of the distinguishable semantic pair. When the prior is unknown, a conservative lower bound $p _ { \mathrm { m i n } } ^ { 2 }$ can be used, where $p _ { \mathrm { m i n } }$ is the minimum prior mass on the support set. The core insight of the proof is: conditions ${ \mathrm { ( i ) - ( v ) } }$ constitute a stable propagation chain of expectation differences—distinguishability is propagated at each step with controllable loss $L _ { \varphi } C ;$ as long as condition (v) ensures that the total loss does not exceed half of the initial margin $\bar { \Delta }$ , it ultimately remains positive at the observation layer.

## 4.3 Inevitability of Leakage in Multi-Semantic Spaces

Based on the binary theorem, we now generalize to the general case of multi-semantic spaces, establishing the inevitability of side-channel leakage.

Corollary 1 (Multi-Semantic Side-Channel Existence). Let semantic space X be nontrivial $\left( \left| \mathcal { X } \right| \geq 2 \right)$ and prior support contains at least two elements). Under the conditions of Proposition $^ { 1 , }$ fix window $T > 0$ . If encrypted communication system Γ and observation model Ω satisfy:

(i) Efficiency-First Design: there exist metric d and constant $C < \infty$ such that for al l $x \in \mathcal { X }$ ,

$$
\mathbb {E} \left[ d \left(e _ {P} \left(\Xi_ {P} | _ {[ 0, T ]}\right), e _ {N} \left(\Xi_ {N} | _ {[ 0, T ]}\right)\right) \mid X = x \right] \leq C. \tag {35}
$$

(ii) Semantic Diversity: there exists at least one distinguishable semantic pair $x \neq$ $x ^ { \prime } \in \mathcal { X }$ and bounded Lipschitz statistic $\varphi : { \mathcal { Z } }  [ - M , M ]$ (with Lipschitz constant $L _ { \varphi } )$ such that

$$
\left. \right.\left| \mathbb {E} \left[ \varphi \left(e _ {P} \left(\Xi_ {P} \mid_ {[ 0, T ]}\right)\right) \mid X = x \right] - \mathbb {E} \left[ \varphi \left(e _ {P} \left(\Xi_ {P} \mid_ {[ 0, T ]}\right)\right) \mid X = x ^ {\prime} \right]\right| \geq \bar {\Delta} > 0, \tag {36}
$$

and $\mathbb { P } ( X = x ) > 0 , \mathbb { P } ( X = x ^ { \prime } ) > 0 .$

(iii) Rational Observer: observation model Ω satisfies non-degeneracy (Definition 5) for this statistic $\varphi _ { i }$ , with $\rho \in ( 0 , 1 ]$ .

$\begin{array} { r } { C < \frac { \bar { \Delta } } { 2 L _ { \varphi } } } \end{array}$

Then the mutual information between observed features and semantics satisfies $I ( X ; Y ) >$ 0.

Proof. By condition (i), efficiency-first design holds for all semantics, in particular for semantic pair $( x , x ^ { \prime } )$ . Combined with conditions $( \mathrm { i i } ) ( \mathrm { i i i } ) ( \mathrm { i v } )$ , this semantic pair satisfies all conditions of Theorem 1. Therefore

$$
I (X; Y) \geq \frac {2}{\ln 2} \mathbb {P} (X = x) \mathbb {P} (X = x ^ {\prime}) \left(\frac {\rho [ \bar {\Delta} - 2 L _ {\varphi} C ]}{2}\right) ^ {2} > 0. \tag {37}
$$

This completes the proof.

![](images/95b338bfeffd17c9270b5fc42650a1d6d2b841da4cba6ea93642fd2937e3d41f.jpg)

Corollary 1 shows: in efficiency-prioritized multi-semantic systems, as long as at least one pair of applications is statistically distinguishable, side-channel leakage is inevitable. The universality of this conclusion stems from:

(1) Efficiency-first is a system-level constraint (condition i): real-world systems must satisfy bandwidth, latency, and other performance requirements, thus $C < \infty$ for all semantics.  
(2) Semantic diversity is an inevitable consequence of applications (condition ii): different application types—such as video streaming (large and dense packets), web browsing (small and sparse packets), instant messaging (bidirectional and symmetric), file transfer (unidirectional and concentrated)—necessarily exhibit differences in statistical features such as packet size distributions, timing patterns, and upstream/downstream ratios. This stems from application logic itself and is independent of encryption.  
(3) Rational observer is the analyst’s objective (condition iii): side-channel analysts aim to maximize information extraction and will retain key statistical features, thus $\rho > 0$ .

Condition (ii) only requires “at least one distinguishable pair exists”, not “all semantics are pairwise distinguishable”—this is an extremely weak assumption. In real-world systems containing $n \geq 2$ applications, it is nearly impossible to make all applications produce statistically indistinguishable traffic—this would require fundamentally changing how applications work, contradicting the purpose of application design.

Therefore, in the universal situation of “efficiency-prioritized usable systems + nontrivial application scenarios + rational observers”, side-channel leakage $I ( X ; Y ) > 0$ is inevitable.

## 5 Theoretical Analysis and Discussion

This section interprets the operational meaning of the existence theorem, discusses the transformation from information-theoretic lower bounds to actual attack performance, and the efficiency-privacy tradeoff revealed by the theorem.

## 5.1 Operational Interpretation from Information-Theoretic Lower Bounds to Attack Feasibility

Theorem 1 and Corollary 1 assert that $I ( X ; Y ) > 0$ in efficiency-prioritized systems and provide explicit lower bounds. To translate this information-theoretic statement into operational predictions for actual attack performance, we establish a precise connection from total variation to classification accuracy.

Accuracy lower bound in binary case. For the binary equal-prior problem $( \mathbb { P } ( X = x ) = \mathbb { P } ( X = x ^ { \prime } ) = 1 / 2 )$ , the error rate and accuracy of the optimal Bayes classifier satisfy the precise relationship:

$$
P _ {e} ^ {\star} = \frac {1 - \mathrm{TV} (P _ {Y | X = x} , P _ {Y | X = x ^ {\prime}})}{2}, \quad \mathrm{Acc} ^ {\star} = \frac {1 + \mathrm{TV} (P _ {Y | X = x} , P _ {Y | X = x ^ {\prime}})}{2}. \tag {38}
$$

From step 4 of Theorem 1, we already obtained the total variation lower bound

$$
\mathrm{TV} (P _ {Y | X = x}, P _ {Y | X = x ^ {\prime}}) \geq \frac {\rho (\bar {\Delta} - 2 L _ {\varphi} C)}{2}, \tag {39}
$$

where C is the mapping non-degeneracy constant (theorem condition (i)).

Substituting into the above, we obtain a lower bound on optimal accuracy:

$$
\mathrm{Acc} ^ {\star} \geq \min \left\{1, \frac {1}{2} + \frac {1}{4} \rho (\bar {\Delta} - 2 L _ {\varphi} C) \right\}. \tag {40}
$$

Since statistic $\varphi : { \mathcal { Z } }  [ - M , M ]$ is bounded, $\bar { \Delta } \leq 2 M $ ; combined with the setting of $\rho \in ( 0 , 1 ]$ and $\psi : \mathcal { V }  [ - 1 , 1 ]$ in the non-degenerate observation definition, the righthand side naturally stays within bounds.

This is a lower bound on the optimal Bayes classifier accuracy, implying there exists a classifier achieving this level. For example, if $\rho = 0 . 8 , \bar { \Delta } = 1 . 0 , L _ { \varphi } C = 0 . 2$ , then

$$
\mathrm{Acc} ^ {\star} \geq \frac {1}{2} + \frac {1}{4} \times 0. 8 \times (1. 0 - 0. 4) = 0. 6 2, \tag {41}
$$

meaning optimal accuracy is at least $6 2 \%$ .

For general priors or multi-class cases $( M > 2 )$ , one can apply this bound to the hardest-to-distinguish binary subproblem (the bound may be loose), or use $^ { \langle \cdot \rangle } \mathrm { o n e - v s - a l l } ^ { \prime \rangle }$ union strategies to obtain conservative lower bounds.

Error rate lower bound from Fano’s inequality. As a complement, we can also use Fano’s inequality to characterize the information-theoretic error rate lower bound. Let semantic space X contain $M \geq 2$ elements, and $P _ { e } ^ { \star }$ be the minimum Bayes error probability. The classical Fano inequality gives

$$
H (X | Y) \leq H _ {2} (P _ {e} ^ {\star}) + P _ {e} ^ {\star} \log_ {2} (M - 1), \tag {42}
$$

where $H _ { 2 } ( p ) = - p \log _ { 2 } p - ( 1 - p ) \log _ { 2 } ( 1 - p )$ is binary entropy (in bits), and $H ( X | Y ) =$ $H ( X ) - I ( X ; Y )$ is posterior entropy. Rearranging gives

$$
P _ {e} ^ {\star} \geq \frac {H (X) - I (X ; Y) - 1}{\log_ {2} (M - 1)}. \tag {43}
$$

For the binary equal-prior case, $H ( X ) = 1$ , the above is equivalent to $I ( X ; Y ) \geq$ $1 - H _ { 2 } ( P _ { e } ^ { \star } )$ , thus $P _ { e } ^ { \star } \ge H _ { 2 } ^ { - 1 } ( 1 - I ( X ; Y ) )$ .

For example, if $I ( X ; Y ) = 0 . 1$ bits, then $P _ { e } ^ { \star } \ge H _ { 2 } ^ { - 1 } ( 0 . 9 ) \approx 0 . 3 1 7$ , meaning optimal error rate is at least 31.7%, and accuracy at most approximately 68.3%. Note that Fano’s inequality provides a lower bound on error rate rather than an upper bound; it clarifies “the information-theoretic limit that even optimal classifiers cannot surpass”, but cannot directly predict achievable performance of actual attacks.

Cumulative effect of multiple observations. In actual side-channel analysis, attackers can often observe multiple sessions $Y ^ { ( 1 ) } , Y ^ { ( 2 ) } , \dots , Y ^ { ( n ) }$ (different sessions of the same user visiting the same website, or concatenating multiple time windows of the same flow). Assuming that given semantic X, each observation is independent and identically distributed:

$$
Y ^ {(1)}, \dots , Y ^ {(n)} \stackrel {\text { i.i.d. }} {\sim} P _ {Y | X} \quad \text { given } \quad X, \tag {44}
$$

then joint mutual information satisfies additivity:

$$
I (X; Y ^ {(1: n)}) = \sum_ {i = 1} ^ {n} I (X; Y ^ {(i)}) = n \cdot I (X; Y). \tag {45}
$$

In this case, the error rate decays exponentially with the Chernoff information as exponent. For the binary equal-prior problem, the large deviation asymptotics of optimal Bayes error rate are characterized by the exact theorem:

$$
- \lim _ {n \to \infty} \frac {1}{n} \log P _ {e} ^ {\star} (n) = \mathcal {C} (P _ {Y | X = x}, P _ {Y | X = x ^ {\prime}}), \tag {46}
$$

where $\mathcal { C } ( \cdot , \cdot )$ is the Chernoff information (here logarithm base is $e ,$ unit is nats), and log denotes natural logarithm.

To establish a lower bound chain from total variation to Chernoff information, we introduce the Bhattacharyya coefficient $\begin{array} { r } { \mathrm { B C } = \int \sqrt { p ( y ) q ( y ) } } \end{array}$ dy and Bhattacharyya distance $B = - \ln \mathrm { B C }$ . Known relationships are

$$
\operatorname{TV} (P, Q) \leq \sqrt {1 - e ^ {- 2 B}}, \quad \mathcal {C} (P, Q) \geq B, \tag {47}
$$

thus

$$
\mathcal {C} (P, Q) \geq B \geq - \frac {1}{2} \ln \bigl (1 - \mathrm{TV} ^ {2} (P, Q) \bigr) > 0. \tag {48}
$$

Substituting our theorem result $\begin{array} { r } { \mathrm { T V } ( P _ { Y | X = x } , P _ { Y | X = x ^ { \prime } } ) \geq \frac { \rho ( \bar { \Delta } - 2 L _ { \varphi } C ) } { 2 } } \end{array}$ into the above gives an explicit lower bound on Chernoff information:

$$
\mathcal {C} (P _ {Y | X = x}, P _ {Y | X = x ^ {\prime}}) \geq - \frac {1}{2} \ln \left(1 - \left[ \frac {\rho (\bar {\Delta} - 2 L _ {\varphi} C)}{2} \right] ^ {2}\right) > 0. \tag {49}
$$

This guarantees that the error rate exponentially tends to zero with the number of observations n.

For the multi-class case $( M > 2 )$ , if each class has positive prior mass and samples are independent and identically distributed given X, the error exponent lower bound of overall Bayes error rate is controlled by $\begin{array} { r } { \operatorname* { m i n } _ { x \neq x ^ { \prime } } \mathcal { C } ( P _ { Y | X = x } , P _ { Y | X = x ^ { \prime } } ) } \end{array}$ . This conclusion comes from common union and worst-pair domination arguments: overall error rate is controlled by the hardest-to-distinguish semantic pair.

This explains universally observed phenomena in practice:

(1) Long observation windows improve accuracy: When growth of $\bar { \Delta } ( T )$ is not offset by $2 L _ { \varphi } C ( T )$ , increasing time window T makes $\delta _ { N } ( T ) = \bar { \Delta } ( T ) - 2 L _ { \varphi } C ( T )$ increase, thus total variation lower bound and accuracy lower bound increase with $T$ .  
(2) Concatenating multiple sessions significantly improves identification: Concatenating n independent sessions makes mutual information accumulate linearly to $n \cdot I ( X ; Y )$ (in bits), with accuracy converging at Chernoff exponent (in nats).  
(3) Exponential convergence to perfect identification: Under the conditional independence assumption, error rate decays exponentially as $\exp ( - n \cdot { \mathcal { C } } )$ to zero.

Corollary 1 guarantees $I ( X ; Y ) > 0$ necessarily holds in efficiency-prioritized systems, thus the above cumulative effects are inevitable—as long as attackers have sufficient observation budget and the conditional independence assumption is satisfied, identification accuracy will tend toward perfection. This is the operational meaning of “ineliminability” of side-channel leakage.

## 5.2 Fundamentality and Insurmountability of Efficiency-Privacy Tradeoff

The five conditions of Theorem 1 reveal the only way to reduce leakage $I ( X ; Y )$ and its costs. We analyze the “cost of breaking” each condition.

Condition (i): Mapping non-degeneracy $C < \infty$ . This is a direct manifestation of efficiency-first design. To break this condition (increase $C \to \infty )$ , the system must pay costs in at least one of the following dimensions:

Length dimension: Heavy padding increases $\mathbb { E } [ d _ { \mathrm { l e n g t h } } ( z _ { P } , z _ { N } ) ]$ . For example, padding all packets to MTU (1500 bytes) inflates small packets (such as 40-byte $\mathrm { A C K s } )$ by tens of times, with bandwidth overhead reaching order-of-magnitude growth.

Timing dimension: Artificial delays increase $\mathbb { E } [ d _ { \mathrm { t i m e } } ( z _ { P } , z _ { N } ) ]$ . For example, introducing second-level delays breaks real-time applications (VoIP requires one-way latency ${ < } 1 5 0 \mathrm { m s } )$ .

Direction dimension: Cover traffic changes upstream/downstream ratios, increasing $\mathbb { E } [ d _ { \mathrm { d i r e c t i o n } } ( z _ { P } , z _ { N } ) ]$ . Bidirectional cover doubles bandwidth overhead.

Condition (v) in the theorem requires $\begin{array} { r } { C < \frac { \bar { \Delta } } { 2 L _ { \varphi } } } \end{array}$ 2Lφ to ensure leakage propagation. To make the leakage lower bound tend to zero, we need $\begin{array} { r } { C \to \frac { \bar { \Delta } } { 2 L _ { \varphi } } } \end{array}$ , meaning efficiency overhead tends toward a critical value—this critical value is determined by the inherent distinguishability $\bar { \Delta }$ of applications and cannot be changed.

Condition (ii): Semantic distinguishability $\bar { \Delta } > 0$ . This is an inevitable consequence of application diversity. To break this condition (make $\bar { \Delta }  0 )$ , all applications need to produce statistically indistinguishable traffic. This is nearly impossible in practice; for instance, video streaming and web browsing differ by orders of magnitude in bandwidth requirements. Instant messaging and file downloading are fundamentally different in interaction patterns. VoIP and HTTP show significant differences in timing features.

To completely eliminate ${ \bar { \Delta } } ,$ all applications must be forced to transmit at the same constant rate, same packet size, same bidirectional pattern, which thoroughly destroys application functionality and makes the problem meaningless.

Conditions (iii)-(iv): Lipschitz property and observation non-degeneracy. Condition (iii) is a technical requirement for statistic selection; in practice, almost all useful statistics (window total bytes, packet counts, upstream/downstream ratios, etc.) can satisfy Lipschitz property through truncation or normalization. Condition (iv) characterizes rational observers, determined by observer technical capabilities rather than controllable by system designers.

Insurmountability of the tradeoff. Synthesizing the above analysis, the cost of reducing leakage presents a trilemma: when the broken condition is increasing C (relaxing non-degeneracy), the cost paid is sacrificing efficiency (bandwidth/latency); when the broken condition is decreasing $\bar { \Delta }$ (homogenizing applications), the cost paid is destroying functionality (applications unusable); when the broken condition is decreasing ρ (compressing observation), the cost paid is beyond control (determined by observer).

Under fixed business requirement constraints such as bandwidth overhead requirements and end-to-end latency requirements, there exists an insurmountable leakage lower bound. This is not a flaw of any particular protocol implementation, but a structural limitation jointly determined by efficiency priority and semantic diversity.

## 5.3 Theoretical Boundaries of Defense and Correct Engineering Objectives

Corollary 1 shows that zero leakage $\left( I ( X ; Y ) = 0 \right)$ is unattainable in efficiencyprioritized systems. This conclusion has important guiding significance for defense mechanism design. Theorem 1 further reveals the mechanism of action of defense mechanisms: constant-rate padding increases metric deviation $C$ to blur the mapping from protocol layer to network layer, at the cost of bandwidth overhead; differential privacy mechanisms reduce observation fidelity by adding noise, at the cost of utility loss; while complete obfuscation defenses attempt to reduce semantic distinguishability $\bar { \Delta }$ , but will destroy application functionality. The essence of these mechanisms is finding different tradeoff points in the constraint space formed by the trilemma.

Wrong objective: pursuing $I ( X ; Y ) = 0 .$ . Many defense schemes (such as Tor’s traffic obfuscation, VPN’s constant-rate padding, etc.) implicitly aim for “eliminating side channels”. The theorem shows this objective is unattainable while maintaining system usability. Phenomena observed in practice verify this conclusion:

(1) Strong defenses like Tamaraw increase latency by 78% and bandwidth overhead to 135% in real Tor network deployment [36]; although they can significantly reduce attack accuracy, their high overhead limits practical deployment.  
(2) Constant-rate padding strategies like BuFLO and CS-BuFLO can reduce identification accuracy but require over 100% bandwidth overhead [23, 37], making them impractical for actual deployment.  
(3) Obfuscation defenses like WTF-PAD and FRONT have lower overhead but cannot resist latest deep learning attacks (accuracy can reach over 90%) [36].

Correct objective: constrained optimization. The correct engineering objective revealed by the theorem is: minimize leakage under given efficiency constraints and functional requirements. Formalized as a constrained optimization problem:

$$
\min _ {\theta \in \Theta} I (X; Y; \theta) \quad \text {s.t.} \quad \left\{ \begin{array}{l l} \text {Bandwidth overhead} \leq \beta_ {\max} & (\text {e.g.,} 10 \% \\ \text {Latency increase} \leq \Delta t _ {\max} & (\text {e.g.,} 50 \mathrm{ms}) \\ \text {Application functionality complete} & (\bar {\Delta} \geq \Delta_ {\min}) \end{array} \right. \tag{50}
$$

where θ is a joint vector of defense parameters such as padding strategies, timing perturbation, and cover traffic.

## 6 Conclusion

This paper provides a formal model $\Sigma = ( \Gamma , \Omega )$ for side-channel analysis from information theory and system design, abstracting the entire process of “generation, encapsulation, encryption, transmission, observation” as a causally measurable Markov chain $X  \Xi _ { A }  \Xi _ { P }  \Xi _ { C }  \Xi _ { N }  Y$ . Based on this framework, this paper proves the sidechannel existence theorem (Theorem 1): for distinguishable binary semantic pairs, under the conditions of mapping non-degeneracy $( \mathbb { E } [ d ( z _ { P } , z _ { N } ) \mid X ] \leq C )$ , semantic distinguishability (expectation difference ≥ ∆¯ ), Lipschitz robustness $\left( | \varphi ( z ) - \varphi ( z ^ { \prime } ) | \leq L _ { \varphi } d ( z , z ^ { \prime } ) \right)$ ), nondegenerate observation (preservation ratio $\rho > 0 )$ , and the distinguishability propagation condition $( C < \bar { \Delta } / 2 L _ { \varphi } )$ , the mutual information between observed features and semantic variables satisfies the explicit lower bound $\begin{array} { r } { I ( X ; Y ) \ge \frac { 1 } { 2 \ln 2 } \left( \frac { \rho [ \bar { \Delta } - 2 L _ { \varphi } C ] } { 2 } \right) ^ { 2 } > 0 } \end{array}$ . Corollary 1 further shows: in efficiency-prioritized multi-semantic systems, as long as at least one pair of applications is statistically distinguishable (stemming from inherent differences in application logic), side-channel leakage is inevitable. Through the precise relationship between total variation and accuracy and the Bhattacharyya-Chernoff lower bound chain, this paper establishes a quantified connection from information-theoretic lower bounds to actual attack performance, revealing the inevitability that multiple observations exponentially accumulate under the conditional independence assumption, making identification accuracy tend toward perfection.

This paper’s analysis shows that reducing leakage faces a trilemma: increasing metric deviation C requires sacrificing efficiency, decreasing semantic distinguishability $\bar { \Delta }$ will destroy application functionality, while observation non-degeneracy ρ is controlled by analysts rather than system designers. Therefore, the correct engineering objective is not pursuing unattainable zero leakage, but rather a constrained optimization problem that minimizes leakage under given efficiency constraints and functional requirements. It is worth emphasizing that the existence theorem and explicit mutual information lower bounds provided in this paper can serve as a theoretical baseline for protocol evolution and defense evaluation: under given efficiency constraints such as bandwidth, latency, and compatibility, different protocol configurations or defense strategies can be mapped to changes in metric d and non-degeneracy constant $C ( T )$ , thereby quantifying their impact on leakage lower bounds and conducting goal-oriented constrained optimization and scheme comparison.

Particularly in website fingerprinting scenarios, this paper’s theoretical framework provides direct guidance for attack feature selection. According to the structure of the mutual information lower bound, attackers should prioritize selecting macroscopic aggregate features with large expectation differences $\bar { \Delta }$ (such as session total bytes, upstream/downstream packet ratios, burst payloads, etc.), while considering Lipschitz robustness of statistics to resist network perturbations; they should value distinguishability information in timing structures, such as packet interval distributions and burstsilence alternation patterns; they can also exploit the Chernoff exponential effect of multisession observations to achieve exponential-level improvement in identification accuracy. These insights show that the expectation difference—Lipschitz robustness—mapping nondegeneracy analysis chain established in this paper provides an interpretable theoretical basis and operational feature design guidelines for traffic feature side-channel attacks.

Several open problems remain in the practical implementation of this paper’s theoretical framework. First, the lower bounds provided by the theorem depend on the choice of metric d and estimation of constants C, $L _ { \varphi } ;$ how to identify or verify these parameters from measured traffic data, and how to establish parameter libraries for different protocol families (TLS 1.3, QUIC) and business types (video streaming, web browsing), are key steps for theory landing. Second, this paper’s non-degeneracy conditions (Definitions 3, 5) are based on metric bounds in the expectation sense, but real networks have transient perturbations such as congestion bursts and routing jitter; how to reformulate conditions in a probabilistic sense (such as high-probability bounds or quantile constraints) and derive corresponding leakage lower bounds will enhance conclusion robustness. Third, this paper focuses on passive observation scenarios, but active probing (such as induced visits in website fingerprinting attacks) and adaptive attacks (observers adjusting strategies based on intermediate results) may break static lower bounds; how to characterize Nash equilibria and optimal strategies of attack-defense parties in a game-theoretic framework is an important topic in dynamic adversarial environments. Additionally, the precise relationship between this paper’s information-theoretic mutual information measure and differential privacy’s $( \varepsilon , \delta ) – \mathrm { D P }$ guarantees has not yet been established; whether one can prove “mechanisms satisfying $\varepsilon { \mathrm { - D P } }$ necessarily lead to mutual information dropping below $f ( \varepsilon ) ^ { , , }$ or similar equivalence theorems will provide operational formal guidelines for privacy mechanism design. Finally, hierarchical leakage analysis in multi-task scenarios (such as first identifying application categories then subdividing specific websites), and dynamic leakage accumulation models considering temporal correlations and long-term observations, are all directions worthy of in-depth research. Solving these problems will advance this paper’s existence conclusions into a computable, verifiable, and optimizable engineering practice framework.

## References

[1] WANG T, GOLDBERG I. Effective attacks and provable defenses for website fingerprinting[C]//Proceedings of the 23rd USENIX Security Symposium. Berkeley: USENIX Association, 2014: 143-157.  
[2] SHEN M, ZHANG J, ZHU L, et al. Accurate decentralized application identification via encrypted traffic analysis using graph neural networks[J]. IEEE Transactions on Information Forensics and Security, 2021, 16: 2367-2380.  
[3] MEI H, CHENG G, YUAN Y. High precision and efficient anonymous traffic classification in the real-world[J]. IEEE Transactions on Networking, 2025, 33(2): 1256- 1270.  
[4] KOCHER P C. Timing attacks on implementations of Diffie-Hellman, RSA, DSS, and other systems[C]//Advances in Cryptology - CRYPTO ’96: 16th Annual International Cryptology Conference. Berlin: Springer-Verlag, 1996: 104-113.  
[5] KOCHER P, JAFFE J, JUN B. Differential power analysis[C]//Advances in Cryptology - CRYPTO ’99: 19th Annual International Cryptology Conference. Berlin: Springer-Verlag, 1999: 388-397.  
[6] HINTZ A. Fingerprinting websites using traffic analysis[C]//Privacy Enhancing Technologies: Second International Workshop, PET 2002. Berlin: Springer-Verlag, 2003: 171-178.  
[7] LIN X, XIONG G, GOU G, et al. ET-BERT: a contextualized datagram representation with pre-training transformers for encrypted traffic classification[C]//Proceedings of the ACM Web Conference 2022. New York: ACM, 2022: 633-642.  
[8] SHEN M, YE K, LIU X, et al. Machine learning-powered encrypted network traffic analysis: a comprehensive survey[J]. IEEE Communications Surveys & Tutorials, 2023, 25(1): 791-824.  
[9] LI S, GUO H, HOPPER N. Measuring information leakage in website fingerprinting attacks and defenses[C]//Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security. New York: ACM, 2018: 1977-1992.  
[10] DWORK C, KENTHAPADI K, MCSHERRY F, et al. Our data, ourselves: privacy via distributed noise generation[C]//Advances in Cryptology - EUROCRYPT 2006: 25th Annual International Conference on the Theory and Applications of Cryptographic Techniques. Berlin: Springer-Verlag, 2006: 486-503.  
[11] SABZI A, VORA R, GOSWAMI S, et al. NetShaper: a differentially private network side-channel mitigation system[C]//Proceedings of the 33rd USENIX Security Symposium. Berkeley: USENIX Association, 2024: 3385-3402.  
[12] CHAUM D L. Untraceable electronic mail, return addresses, and digital pseudonyms[J]. Communications of the ACM, 1981, 24(2): 84-90.  
[13] DÍAZ C, SEYS S, CLAESSENS J, et al. Towards measuring anonymity[C]//Privacy Enhancing Technologies: Second International Workshop, PET 2002. Berlin: Springer-Verlag, 2003: 54-68.  
[14] DENG Y, PANG J, WU P. Measuring anonymity with relative entropy[C]//Formal Aspects in Security and Trust: 4th International Workshop, FAST 2006. Berlin: Springer-Verlag, 2007: 65-79.  
[15] SERJANTOV A, DANEZIS G. Towards an information theoretic metric for anonymity[C]//Privacy Enhancing Technologies: Second International Workshop, PET 2002. Berlin: Springer-Verlag, 2003: 41-53.  
[16] CHATZIKOKOLAKIS K, PALAMIDESSI C, PANANGADEN P. Anonymity protocols as noisy channels[J]. Information and Computation, 2008, 206(2-4): 378-401.  
[17] KESDOGAN D, AGRAWAL D, PENZ S. Limits of anonymity in open environments[C]//Information Hiding: 5th International Workshop, IH 2002. Berlin: Springer-Verlag, 2003: 53-69.  
[18] DANEZIS G. Statistical disclosure attacks: traffic confirmation in open environments[C]//Security and Privacy in the Age of Uncertainty: IFIP TC11 18th International Conference on Information Security. Boston: Springer, 2003: 421-426.  
[19] COVER T M, THOMAS J A. Elements of information theory[M]. 2nd ed. Hoboken: John Wiley & Sons, 2006: 34-35.  
[20] VAN DEN HOOFF J, LAZAR D, ZAHARIA M, et al. Vuvuzela: scalable private messaging resistant to traffic analysis[C]//Proceedings of the 25th Symposium on Operating Systems Principles. New York: ACM, 2015: 137-152.  
[21] TYAGI N, GILAD Y, LEUNG D, et al. Stadium: a distributed metadata-private messaging system[C]//Proceedings of the 26th Symposium on Operating Systems Principles. New York: ACM, 2017: 423-440.  
[22] PANCHENKO A, NIESSEN L, ZINNEN A, et al. Website fingerprinting in onion routing based anonymization networks[C]//Proceedings of the 10th Annual ACM Workshop on Privacy in the Electronic Society. New York: ACM, 2011: 103-114.  
[23] DYER K P, COULL S E, RISTENPART T, et al. Peek-a-boo, I still see you: Why efficient traffic analysis countermeasures fail[C]//Proceedings of the 2012 IEEE Symposium on Security and Privacy. Los Alamitos: IEEE Computer Society, 2012: 332- 346.  
[24] CAI X, NITHYANAND R, WANG T, et al. A systematic approach to developing and evaluating website fingerprinting defenses[C]//Proceedings of the 2014 ACM SIGSAC Conference on Computer and Communications Security. New York: ACM, 2014: 227-238.  
[25] WANG T, GOLDBERG I. Walkie-talkie: An efficient defense against passive website fingerprinting attacks[C]//Proceedings of the 26th USENIX Security Symposium. Berkeley: USENIX Association, 2017: 1375-1390.  
[26] HUANG J N, LIU W, LIU G, et al. STAP: leveraging state-transition adversarial perturbations for asymmetric website fingerprinting defenses[J]. IEEE Transactions on Network and Service Management, 2025, 22(1): 234-248.  
[27] WRIGHT C V, COULL S E, MONROSE F. Traffic morphing: an efficient defense against statistical traffic analysis[C]//Proceedings of the 16th Network and Distributed Security Symposium. Reston: The Internet Society, 2009: 237-250.  
[28] CHERUBIN G. Bayes, not naïve: security bounds on website fingerprinting defenses[C]//Proceedings on Privacy Enhancing Technologies, 2017, 2017(4): 215-231.  
[29] FU C, LI Q, SHEN M, et al. Realtime robust malicious traffic detection via frequency domain analysis[C]//Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security. New York: ACM, 2021: 3431-3446.  
[30] FU C, LI Q, SHEN M, et al. Detecting tunneled flooding traffic via deep semantic analysis of packet length patterns[C]//Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security. New York: ACM, 2024: 3659-3673.  
[31] FU C P, LI Q, XU K. Detecting unknown encrypted malicious traffic in real time via flow interaction graph analysis[C]//Network and Distributed System Security Symposium (NDSS). San Diego, CA, USA: The Internet Society, 2023.  
[32] CAMENISCH J, LYSYANSKAYA A. A formal treatment of onion routing[C]//Advances in Cryptology - CRYPTO 2005: 25th Annual International Cryptology Conference. Berlin: Springer-Verlag, 2005: 169-187.  
[33] FEIGENBAUM J, JOHNSON A, SYVERSON P. A model of onion routing with provable anonymity[C]//Financial Cryptography and Data Security: 11th International Conference, FC 2007. Berlin: Springer-Verlag, 2007: 57-71.  
[34] DANEZIS G, GOLDBERG I. Sphinx: a compact and provably secure mix format[C]//Proceedings of the 30th IEEE Symposium on Security and Privacy. Los Alamitos: IEEE Computer Society, 2009: 269-282.  
[35] GRAY R M. Probability, random processes, and ergodic properties[M]. 2nd ed. New York: Springer, 2011.  
[36] SHEN M, XU K, LI Q, et al. Real-time website fingerprinting defense via traffic cluster anonymization[C]//Proceedings of the 2024 IEEE Symposium on Security and Privacy. Los Alamitos: IEEE Computer Society, 2024: 2674-2691.  
[37] CAI X, NITHYANAND R, JOHNSON R. CS-BuFLO: a congestion sensitive website fingerprinting defense[C]//Proceedings of the 2014 ACM Workshop on Privacy in the Electronic Society. New York: ACM, 2014: 121-130.
# Forge: A Robust Multi-tab Website Fingerprinting Atack Via Blind Source Separation

Yitan Huang Institute of Information Engineering, Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences Beijing, China huangyitan@iie.ac.cn

Di Zhao Institute of Information Engineering, Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences Beijing, China zhaodi@iie.ac.cn

Wei Qiao Institute of Information Engineering, Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences Beijing, China qiaowei@iie.ac.cn

Linxu Li Institute of Information Engineering, Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences Beijing, China lilinxu@iie.ac.cn

Zhigang Lu Institute of Information Engineering, Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences Beijing, China luzhigang@iie.ac.cn

Ding Wang Institute of Information Engineering, Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences Beijing, China wangding2023@iie.ac.cn

Susu Cui Institute of Information Engineering, Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences Beijing, China cuisusu@iie.ac.cn

Baoxu Liu Institute of Information Engineering, Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences Beijing, China liubaoxu@iie.ac.cn

Meng Shen School of Cyberspace Science and Technology, Beijing Institute of Technology Beijing, China shenmeng@bit.edu.cn

Bo Jiang Institute of Information Engineering, Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences Beijing, China jiangbo@iie.ac.cn

## Ab<sub>s</sub>t<sub>rac</sub>t

While Tor’s strong anonymity shields users’ privacy, it also enables malicious activities, motivating attacks that bypass its protections. Website Fingerprinting (WF) has emerged as a primary threat in this domain. However, existing WF methods struggle with realistic multi-tab browsing scenarios, often relying on prior knowledge of the number of open tabs and lacking robustness against network noise and defenses.

To address these challenges, we propose Forge, a robust WF attack framework inspired by the classic cocktail party problem. Specifically, Forge reframes multi-tab WF as a task of Blind Source Separation(BSS), decomposing mixed trafic into individual signals without requiring a predefined number of concurrent tabs. A robust website identifier then classifies separated components using a dual-domain attention mechanism across time and frequency, allowing Forge to efectively resist WF defenses and network noise. We evaluate our model on a comprehensive collection of datasets covering open-world, defense-enabled, and dynamic scenarios. The results demonstrate that Forge can improve Mean Average Precision by 78.6% over the state-of-the-art average in the challenging multi-tab open-world scenario.

## CCS Conce<sub>p</sub>ts

• Securit<sub>y</sub> and <sub>p</sub>rivac<sub>y</sub> → Pseudon<sub>y</sub>mit<sub>y</sub>, anon<sub>y</sub>mit<sub>y</sub> and untraceability; Privacy-preserving protocols.

## Ke<sub>y</sub>words

Website Fingerprinting, Multi-tab Attack, Tor, Privacy

ACM Reference Format: Yitan Huang, Wei Qiao, Ding Wang, Meng Shen, Di Zhao, Linxu Li, Susu Cui, Bo Jiang, Zhigang Lu, and Baoxu Liu. 2026. Forge: A Robust Multi-tab Website Fingerprinting Attack Via Blind Source Separation. In Proceedings of the ACM Web Conference 2026 (WWW’26), April 13–17, 2026, Dubai, United Arab Emirates. ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/ 3774904.3792410

## 1 I<sub>n</sub>t<sub>ro</sub>d<sub>uc</sub>ti<sub>on</sub>

Tor [13], the leading anonymity system, provides protection against trafic analysis [26, 29, 33]. However, this strong anonymity is a double-edged sword. While safeguarding benign users, it is also exploited for malicious activities [14] , such as hosting darknet markets via its Hidden Services [37]. Consequently, adversaries are highly motivated to develop trafic analysis attacks that can bypass Tor’s protections. Website Fingerprinting (WF) has emerged as a primary attack in this domain. By analyzing side-channel features of encrypted trafic—like packet sizes, timings, and directions [14, 37, 44]—WF enables a local adversary to infer a user’s browsing activity, thereby undermining Tor’s anonymity [2, 7, 30, 32, 34].

The field of WF has evolved significantly, moving from idealized, single-tab scenarios to the far more challenging multi-tab environment. Early methods like DF [34] and AWF [31] achieve high accuracy in these sterile, single-tab settings. However, their eficacy plummets in the complex, realistic environment of concurrent browsing. To contend with the mixed trafic from multiple open tabs, distinct strategies have emerged. Some, like ARES [12], frame the task as a multi-label classification problem, while others, like TMWF [20], treat it as an ordered set prediction. Despite these advancements, several critical challenges persist, undermining the real-world eficacy of all existing attacks:

• The Multi-tab Interference: Trafic from concurrently browsed websites is interleaved into a single mixed stream, obscuring individual website fingerprints and making them hard to classify.

• The Unrealistic Pre-knowledge Requirement: Most existing methods require prior knowledge of the exact number of open tabs. This assumption is unrealistic, and it causes a sharp performance decline when violated.

• The Lack of Robustness and Noise Resilience: Current mod els are trained on idealized datasets and largely ignore real-world factors like network noise and WF defenses. This makes their reported performance unreliable in practice.

We contend that these limitations stem from a fundamental par adigm mismatch: a problem that is intrinsically about "mixing and separation" has been rigidly modeled as multi-label classification. Imagine you are at a noisy party where many people are speaking simultaneously. Your brain does not attempt to parse the entire blended sound at once. Instead, it first separates the jumbled audio into distinct voices from the diferent speakers. Only after this separation can you recognize what each person is saying. This sce nario, known as the classic "cocktail party problem", inspires our reformulation of multi-label website fingerprinting.

In multi-tab browsing, a single network channel similarly carries multiple interwoven "voices"—namely, the trafic patterns of each website. Applying a classifier directly to this mixed trafic forces the model to simply memorize various "combination patterns," a fragile strategy akin to recognizing the jumbled party noise as a whole rather than the individual speakers. This is not just ineficient. It is fundamentally brittle and ill-equipped to handle the dynamics of real-world browsing, such as concurrent page loads, a variable number of tabs, or network defenses. Inspired by this analogy, we turn to the solution for the classic "cocktail party problem": Blind Source Separation (BSS) [5]. BSS is a family of methods designed to computationally "unmix" such mixtures without prior knowledge of the number of sources. This insight reframes our core challenge from classifying a mixture to separating its components.

We therefore recast the multi-tab WF problem through the lens of a "separate-then-identify" paradigm: "unmixing" the trafic stream to recover the constituent website fingerprints, and subsequently identifying them. This separation-first approach obviates the need for prior knowledge of tab counts, enhances robustness against dynamic settings and defenses, and yields more stable fingerprints for downstream classification.

In this paper, we propose Forge, a framework for multi-tab WF attacks with three modules: (1) a Time-Delay Embedding module that maps one-dimensional trafic into a multi-dimensional statespace to construct virtual observation channels; (2) a BSS solver, implemented as a deep network unrolling a classical iterative BSS algorithm, which separates mixed trafic without prior knowledge of the number of concurrent tabs; and (3) a Website Identifier that classifies each separated component using Dual-Domain Consistency Attention (DDCA) to enforce time–frequency consistency.

We evaluate Forge against seven state-of-the-art methods on WFLib [11], a comprehensive dataset spanning multi-tab, openworld, and defense-enabled settings. Forge consistently achieves the best performance and demonstrates strong robustness under established defenses (e.g., WTF-PAD [23] and Front [16]), network noise, and dynamic conditions such as unknown tab counts. Extensive ablation and sensitivity analyses further isolate the contribution of each component and confirm the framework’s stability.

The primary contributions of our work are as follows:

• We propose Forge, a novel framework for multi-tab WF attacks. Our framework innovatively reframes the task as a Blind Source Separation (BSS) problem. As a result, Forge can blindly separate and identify websites from a mixed trafic stream, even without prior knowledge of concurrent tab numbers.

• We design a BSS Solver by unrolling an iterative BSS algorithm into a deep neural network. This module blindly separates an unknown number of sources from a single observation.

• We develop a defense-resilient identifier equipped with the Dual-Domain Consistency Attention. The mechanism allow Forge to maintain high eficacy by validating features across domains and adaptively mitigating the impact of noise and defensive measures.

• We conduct extensive experiments on the WFlib datasets, demonstrating that Forge significantly outperforms SOTA attacks. The results, spanning closed-world, open-world, and various defenseenabled scenarios, confirm its stronger performance, generality, and robustness in realistic environments.

Availability. Our open-source implementation is available at https://github.com/Carm3nc1ta/FORGE.

## 2 R<sub>e</sub>l<sub>a</sub>t<sub>e</sub>d W<sub>or</sub>k <sub>an</sub>d Li<sub>m</sub>it<sub>a</sub>ti<sub>ons</sub>

## 2<sub>.</sub>1 R<sub>e</sub>l<sub>a</sub>t<sub>e</sub>d W<sub>or</sub>k

WF Attacks. Based on the scenarios they can handle, WF attacks can be divided into two categories.

Table 1: Com<sub>p</sub>arison of WF attacks.

<table><tr><td>WF Attack</td><td>Multi-tab</td><td>Genericity</td><td>Robustness</td><td>Noise Resilience</td></tr><tr><td>AWF</td><td>✕</td><td>✕</td><td>✕</td><td>✕</td></tr><tr><td>DF</td><td>✕</td><td>✕</td><td>√</td><td>✕</td></tr><tr><td>Tik-Tok</td><td>✕</td><td>✕</td><td>√</td><td>✕</td></tr><tr><td>RF</td><td>✕</td><td>✕</td><td>√</td><td>✕</td></tr><tr><td>BAPM</td><td>√</td><td>✕</td><td>✕</td><td>✕</td></tr><tr><td>ARES</td><td>√</td><td>√</td><td>√</td><td>✕</td></tr><tr><td>TMWF</td><td>√</td><td>√</td><td>✕</td><td>✕</td></tr><tr><td>FORGE (ours)</td><td>√</td><td>√</td><td>√</td><td>√</td></tr></table>

The first category is single-tab attacks, which assume that a user visits one website at a time [1, 27, 39]. Early work relies on tradi tional machine learning models, such as SVM in CUMUL [28, 42] and k-NN in k-FP [8, 22]. More recent studies adopt deep learn ing approaches, including Var-CNN [2], AWF [31], DF [34], and Tik-Tok [30], achieving improved performance.

The second category is multi-tab attacks, which reflect more realistic browsing with concurrent tabs. Early split-and-classify methods perform poorly due to information loss from discarding interleaved trafic [9, 43]. Recent work favors end-to-end models that process mixed trafic directly. TMWF [20] formulates the task as ordered set prediction using a Transformer, BAPM [18] groups trafic blocks via attention to handle overlap, and ARES [12] models the problem as multi-label classification using multiple classifiers. WF Defenses. Concurrently, researchers develop a range of WF defenses to thwart these attacks. These defenses fall into three main categories based on their core mechanism. The first category is obfuscation. This method disrupts trafic patterns by injecting noise. Front [16] is an key example. The second is regularization[3, 4, 17]. It aims to reshape trafic from diferent websites into a uni form pattern. Representative works include WTF-PAD [23], Walkie Talkie [40] and RegulaTor [19]. The third is trafic splitting. This technique compromises a fingerprint’s integrity by routing it over multiple network paths. TraficSliver [10] uses this approach.

## 2<sub>.</sub>2 Li<sub>m</sub>it<sub>a</sub>ti<sub>ons o</sub>f E<sub>x</sub>i<sub>s</sub>ti<sub>ng</sub> S<sub>o</sub>l<sub>u</sub>ti<sub>ons</sub>

Despite recent progress, existing WF attacks exhibit critical limita tions that hinder their real-world applicability. Our model, Forge, is designed to address these issues, as summarized in Table 1.

Limited Multi-tab Capability: Realistic browsing involves concurrent access to multiple websites, requiring WF attacks to handle mixed trafic. However, most existing methods focus on the simpler single-tab setting and fail to support multi-tab scenarios.

Lack of Generality: Most multi-tab attacks rely on the impractical assumption that the number of open webpages is known in advance. This information is unavailable in real-world settings. ARES partially relaxes this assumption but still sufers from degraded performance without prior knowledge.

Poor Robustness to Defenses: Many influential WF attacks (e.g., AWF) are developed and evaluated without defenses. Their perfor mance degrades significantly under standard Tor defenses such as WTF-PAD, limiting practical deployment.

Vulnerability to Network Noise: Tor’s multi-hop routing and queuing introduce unavoidable trafic noise (e.g., timing jitter). Most existing models, however, are designed for idealized, noise-free conditions and fail to account for this aspect ofthe Tor environment.

## 3 Th<sub>rea</sub>t M<sub>o</sub>d<sub>e</sub>l <sub>an</sub>d M<sub>o</sub>ti<sub>va</sub>ti<sub>on</sub>

## 3<sub>.</sub>1 Th<sub>rea</sub>t M<sub>o</sub>d<sub>e</sub>l

Figure 1a illustrates the WF threat model in the Tor network. A user, following natural browsing behavior, concurrently opens multiple webpages, producing mixed and temporally interleaved encrypted trafic. This trafic may be protected by defenses deployed on the client or Tor relays. Consistent with prior work [22, 27, 34, 36], we consider a local, passive adversary (e.g., an ISP or malicious Tor entry node [28]) that can observe encrypted trafic metadata but cannot decrypt contents or modify trafic. We consider two attack scenarios. In the closed-world setting, users visit only a small monitored set of websites. In the open-world setting, users may visit arbitrary websites, and the adversary has training data for only a subset [21, 38].

## 3.2 Motivation

![](images/8120f9cdbae03adb56c2c98774123d183746784a2128f32bc358bb785d425822.jpg)

(a) The threat model of a WF attack. An adversary attempts to deconstruct a user’s browsin<sub>g</sub> histor<sub>y</sub> b<sub>y</sub> anal<sub>y</sub>zin<sub>g</sub> the mixed t<sub>ra</sub>fi<sub>c</sub> f<sub>rom</sub> th<sub>e</sub>i<sub>r s</sub>i<sub>mu</sub>lt<sub>aneous mu</sub>lti<sub>-</sub>t<sub>a</sub>b b<sub>rows</sub>i<sub>ng.</sub>  
![](images/37edfd6ab8fa5ded2508bd06de5405dab838f952c146b94582a1c6fe05596339.jpg)  
(b) The diagram ofa classic "cocktail party problem". A listener <sub>can</sub> d<sub>ec</sub>i<sub>p</sub>h<sub>er</sub> th<sub>e m</sub>i<sub>xe</sub>d <sub>au</sub>di<sub>o</sub> f<sub>rom mu</sub>lti<sub>p</sub>l<sub>e s</sub>i<sub>mu</sub>lt<sub>aneous</sub> <sub>spea</sub>k<sub>ers an</sub>d d<sub>e</sub>t<sub>erm</sub>i<sub>ne w</sub>h<sub>o sa</sub>id <sub>w</sub>h<sub>a</sub>t<sub>.</sub>  
Figure 1: The analogy between multi-tab WF attack(a) and the classic cocktail party problem(b).

Figure 1a illustrates the core challenge of multi-tab WF attack: How can an attacker deconstruct a mixed trafic stream to identify the constituent websites, especially when the number of sites is unknown and the data is distorted by network noise and defenses?

To tackle this challenge, we draw inspiration from a classic problem in signal processing: the "cocktail party problem," depicted in Figure 1b. At a crowded party, the human auditory system can remarkably focus on a single speaker’s voice amidst a cacophony of other conversations and ambient noise.

The parallels between this problem and multi-tab WF are striking. We can map the core components as follows:

• Source Signals: Individual speakers’ voices ↔ Trafic fingerprints of individual websites.

• Mixed Signal: The sound captured by a listener’s ears ↔ The aggregated trafic sequence captured by the adversary.

• Mixing System: Room acoustics and reverberation ↔ The net work transmission process $( \mathrm { e . g . }$ , queuing, routing).

• Noise: Ambient background noise ↔ Network noise.

This analogy is not merely conceptual; it provides a formal mathe matical framework. In signal processing, the cocktail party problem is a canonical example of Blind Source Separation (BSS)—a class of algorithms designed to recover original source signals from a set of mixed observations with minimal prior knowledge.

This insight motivates us to be the first to formally define the multi-tab Website Fingerprinting attack as a Blind Source Separa tion (BSS) problem. Under this framework, the adversary’s observed trafic sequence �[�] is modeled as a multi-layered mixing process:

Firstly, � concurrently accessed websites each generate an independent source signal $s _ { k } [ n ]$ with a unique statistical fingerprint. Then, each signal �<sub>�</sub> [�] undergoes a time-varying process with a channel $h _ { k } ( n , \tau )$ , which models network efects like latency and jitter. Finally, all streams mix non-linearly, denoted as $\mathcal { F } _ { \mathrm { n o n l i n } }$ , due to competition for shared network resources (e.g., relay nodes).

The final observed signal � [�] is thus represented as:

$$
x [ n ] = \mathcal {F} _ {\text { nonlin }} \left(\sum_ {k = 1} ^ {K} \int h _ {k} (n, \tau ; s _ {j}) s _ {k} (n - \tau) d \tau , \text { Queue   State }\right) + \epsilon [ n ]\tag{1}
$$

, where $\epsilon [ n ]$ is additive background noise. The challenge is that only the mixed signal �[�] is observed, while the number of sources �, the signals $s _ { k } ,$ and the non-linear mixing $\mathcal { F } _ { \mathrm { n o n l i n } }$ are unknown. The goal is to recover the website labels $\hat { Y } = \hat { y } _ { 1 } , \dotsc , \hat { y } _ { K ^ { \prime } }$

## 4 Desi<sub>g</sub>n of Forge

We propose Forge, a framework consisting of three functionally distinct, sequential modules, as shown in Figure 2: 1) Time-Delay Embedding module; 2) BSS Solver; and 3) Website Identifier.

## 4<sub>.</sub>1 T<sub>ra</sub>fi<sub>c</sub> Ch<sub>anne</sub>l C<sub>ons</sub>t<sub>ruc</sub>ti<sub>on</sub>

Inspired by signal processing, we model multi-tab Website Fingerprinting as a Blind Source Separation (BSS) problem. A key challenge is that classic BSS requires multiple observation channels (�) to separate multiple sources (�), whereas in WF attacks, the adversary observes only a single mixed trafic stream with perpacket directions and timestamps. This creates an underdetermined scenario $( M = 1 , K > 1 )$ , making unique separation impossible.

To overcome this, we propose constructing virtual observation channels from a single trafic stream using Takens’s theorem[6], which states that a system’s dynamics can be reconstructed from a single observable. By forming state vectors of time-delayed signals, we convert the one-dimensional series into a higher-dimensional space[15, 35], generating the multiple “channels” needed for BSS.

Following this principle, we reconstruct a high-dimensional state space from our one-dimensional sequence � [�] with length �, representing the sequence of encrypted packets over time. Each element in this sequence encodes critical side-channel information, primarily the packet’s direction (+1 for outgoing, -1 for incoming) and its timestamp. A state vector � [�] at time � is constructed by applying a mapping operator Φ to the signal’s history over a duration �: $v [ t ] = \Phi ( x [ t - \tau : t ] )$ . Here, $x [ t - \tau : t ]$ denotes the trafic segment in the preceding time window. The operator Φ $\mathbf { \varepsilon } :  { \mathcal { X } } \to \mathbb { R } ^ { 8 }$ maps this segment to an 8-dimensional vector, whose components are defined as follows:

Volumetric Dynamics: Let $D ( x [ t - \tau : t ] )$ be the sequence of packet directions (+1 for outgoing, -1 for incoming) in the window, and $I ( \cdot )$ be the indicator function.

$$
\begin{array}{l} \bullet v _ {0} [ t ] = \sum_ {d _ {i} \in D (x [ t - \tau : t ])} I (d _ {i} > 0); \\ \bullet v _ {1} [ t ] = \sum_ {d _ {i} \in D (x [ t - \tau : t ])} I (d _ {i} <   0). \end{array}
$$

Temporal Structure: Let $T _ { \mathrm { u p } }$ and $T _ { \mathrm { d o w n } }$ be the sets of sorted timestamps for outgoing and incoming packets within the window, respectively.

$$
\begin{array}{l} \bullet v _ {2} [ t ] = \sum_ {i} (\mathrm{ts} _ {i + 1} - \mathrm{ts} _ {i}) \text {for} \mathrm{ts} _ {i}, \mathrm{ts} _ {i + 1} \in T _ {\mathrm{up}}; \\ \bullet v _ {3} [ t ] = \sum_ {j} (\mathrm{ts} _ {j + 1} ^ {\prime} - \mathrm{ts} _ {j} ^ {\prime}) \text {for} \mathrm{ts} _ {j} ^ {\prime}, \mathrm{ts} _ {j + 1} ^ {\prime} \in T _ {\mathrm{down}}. \end{array}
$$

Interaction Patterns: A "Burst" is defined as a contiguous subsequence of the same sign in $D ( x [ t - \tau : t ] )$ ). Let $B _ { \mathrm { u p } }$ and $B _ { \mathrm { d o w n } }$ be the sets of outgoing and incoming bursts, respectively.

$$
\begin{array}{l} \bullet v _ {4} [ t ] = | B _ {\mathrm{up}} |; \\ \bullet v _ {5} [ t ] = | B _ {\mathrm{down}} |; \\ \bullet v _ {6} [ t ] = (1 / | B _ {\mathrm{up}} |) \sum_ {b \in B _ {\mathrm{up}}} \mathrm{len} (b); \\ \bullet v _ {7} [ t ] = (1 / | B _ {\mathrm{down}} |) \sum_ {b \in B _ {\mathrm{down}}} \mathrm{len} (b). \end{array}
$$

By applying this operator over the entire observation duration, we elevate the original 1D sequence � [�] into an 8-dimensional state-vector time series $V = \bar { \left[ v , v , \dots , v [ T ] \right] } \in \mathbb { R } ^ { 8 \times T }$ . This step is equivalent to creating $M _ { \mathrm { { v i r t u a l } } } = 8$ virtual observation channels, providing a mathematically well-posed input for the subsequent blind source separation.

## 4.2 BSS Sol<sub>v</sub>er

The BSS solver disentangles multi-channel features $\mathbf { V } \in \mathbb { R } ^ { 8 \times T }$ into single-website source streams ${ \hat { \mathsf { S } } } .$ Leveraging Blind Source Separation (BSS), it operates without knowing the number of sources, making the model robust when the number of concurrently open websites (�) is unknown.

The solver mimics iterative BSS algorithms, which refine mixed signals until statistically independent. We implement this via a deep network of � cascaded Iterative Correction Modules (ICMs), each performing one separation step. At iteration �, the ICM takes the current estimate $\mathbf { H } ^ { ( \hat { l } ) }$ and computes a correction $\mathcal { F } _ { ; }$ , producing a refined estimate $\mathbf { H } ^ { ( l + 1 ) }$ :

$$
\mathbf {H} ^ {(l + 1)} = \text { PostProcess } (\mathbf {H} ^ {(l)} + \mathcal {F} (\mathbf {H} ^ {(l)}))\tag{2}
$$

.The function $\mathcal { F }$ represents the core computational block designed to compute and apply this correction. Its architecture is detailed below.

Step 1: Residual Feature Extraction. This step aims to analyze the current signal estimate $\mathbf { H } ^ { ( l ) }$ to identify residual cross-stream dependencies.

• Learnable Analysis Filters: The input $\mathbf { H } ^ { ( l ) }$ is processed by a Conv1d layer and BatchNorm1d, acting as learnable filters that project the signal into a feature space where residual mixing patterns can be more efectively identified.

• Non-linear Activation: The projected features pass through a ReLU, promoting sparsity by zeroing negative values and helping the model separate the original source signals from the mixture.

Step 2: Correction Signal Synthesis. The non-linearly transformed features, which now highlight the distinct source characteristics, are fed into a second pair of Conv1d and BatchNorm1d layers.

![](images/fd1f95facf7f339237cc3cb06953bfbaa86e7fe7252cd7b0fcf252abd0e214ea.jpg)  
Fi<sub>gure</sub> 2<sub>:</sub> Th<sub>e arc</sub>hit<sub>ec</sub>t<sub>ure o</sub>f F<sub>orge.</sub> Th<sub>e</sub> f<sub>ramewor</sub>k <sub>cons</sub>i<sub>s</sub>t<sub>s o</sub>f th<sub>ree ma</sub>i<sub>n s</sub>t<sub>ages:</sub> 1<sub>.</sub>T<sub>ra</sub>fi<sub>c</sub> Ch<sub>anne</sub>l C<sub>ons</sub>t<sub>ruc</sub>ti<sub>on mo</sub>d<sub>u</sub>l<sub>e</sub> <sub>co</sub>n<sub>ve</sub>rt<sub>s</sub> r<sub>aw</sub> tr<sub>a</sub>fi<sub>c</sub> int<sub>o a</sub> m<sub>u</sub>lti-dim<sub>e</sub>n<sub>s</sub>i<sub>o</sub>n<sub>a</sub>l r<sub>e</sub> r<sub>ese</sub>nt<sub>a</sub>ti<sub>o</sub>n<sub>.</sub> 2<sub>.</sub> BSS S<sub>o</sub>l<sub>ve</sub>r <sub>se a</sub>r<sub>a</sub>t<sub>es</sub> th<sub>e</sub> mix<sub>e</sub>d tr<sub>a</sub>fi<sub>c</sub> int<sub>o</sub> indi<sub>v</sub>id<sub>ua</sub>l <sub>co</sub>m <sub>o</sub>n<sub>e</sub>nt<sub>s.</sub> 3. Website Identifier classifies each separated component using Dual-Domain Consistency Attention (DDCA).

This stage acts as a synthesis filter bank, converting the extracted residual features back into a correction signal, ΔH, which matches the dimensions of the input.

Step 3: Iterative Refinement. This final step applies the correction and prepares the output for the next module in the cascade.

• Residual Update: The synthesized correction ΔH is added to the module’s input $\mathbf { H } ^ { ( l ) }$ via a shortcut, implementing the iterative update rule new\_estimate $= \mathrm { o l d }$ \_estimate + update\_term. This residual design lets each ICM focus on learning the correction, simplifying optimization.

• Multi-scale Feature Propagation: The updated signal passes through a ReLU activation and a MaxPool1d layer for down-sampling, enabling the next ICM to capture features from local patterns to long-term dependencies. A Dropout layer is applied for regular ization before the output is passed on.

By cascading � such ICMs, the network achieves progressive, multi-scale separation. The final output $\mathbf { H } ^ { ( L ) }$ comprises refined fea ture streams, with each channel conditioned to represent a distinct underlying source signal.

## 4<sub>.</sub>3 W<sub>e</sub>b<sub>s</sub>it<sub>e</sub> Id<sub>en</sub>tifi<sub>er</sub>

This module performs the final classification using a Transformerbased identifier with Dual-Domain Consistency Attention (DDCA). Learnable Positional Embeddings are added to each stream before the encoder, whose core comprises stacked DDCA blocks.

Dual-Domain Consistency Attention (DDCA). A key challenge in website fingerprinting is adversarial defenses. As shown in Fig ure 3, methods like dummy-packet injection and adaptive padding mainly disrupt time-domain features such as packet timing and sequence length. These perturbations are seldom “clean” and often leave artifacts in the frequency domain—for instance, rapid dummy-packet injection generates high-frequency noise, while other padding schemes produce predictable frequency signatures.

DDCA is motivated by the observation that time-domain obfus cation often leaves traces in the frequency domain. It employs a dual-branch attention mechanism to cross-validate features from both domains, enhancing robustness against defenses targeting only the time domain.

Time-Domain Dependency Analyzer: We use a standard self attention mechanism to model sequential dependencies in the time dimension, capturing the local temporal logic between events. Its

![](images/f4ba0f5350041a16dcda599128566fc8a822197565c2573146c02c0c808246f2.jpg)  
Fi<sub>g</sub>ure 3: Time–fre<sub>q</sub>uenc<sub>y</sub> views of three exam<sub>p</sub>les<sub>,</sub> one <sub>p</sub>er defense category: random injection, adaptive padding, and re<sub>g</sub>ularization.

computation is:

$$
y _ {\text { time }} = \text { Attention } (Q, K, V) = \text { softmax } \left(\frac {Q K ^ {T}}{\sqrt {d _ {k}}}\right) V\tag{3}
$$

, where Q, K, and V are linear projections of the input x.

Frequency-Domain Structure validator: This branch is designed to capture frequency-domain features and validate them against time-domain noise. To achieve this, the time-domain signal � is first mapped to the frequency domain using the Fast Fourier Transform:

$$
X _ {f} [ k ] = \sum_ {n = 0} ^ {N - 1} x [ n ] \cdot e ^ {- i 2 \pi k n / N}\tag{4}
$$

. Crucially, we use only the magnitude spectrum $A _ { f } = | X _ { f } | \quad$ , which is naturally robust to time shifts and jitter introduced by defenses.

Self-attention is then applied to this magnitude spectrum, enabling the model to focus on stable low-to-mid frequency bands that reflect a site’s intrinsic loading rhythm, while down-weighting high-frequency noise characteristic of certain defenses.

The time and frequency branch outputs are fused via a residual connection gated by a learnable parameter � = 0.1. After the DDCA module, the signal passes through a feed-forward network (FFN), and a final linear layer produces the classification logits, yielding the multi-website fingerprinting labels.

## 5 E<sub>va</sub>l<sub>ua</sub>ti<sub>on</sub>

In this section, we present various evaluations to demonstrate the merits of Forge and answer the following key research questions: RQ1: How does Forge perform in a closed-world, multi-tab setting? RQ2: How efective is Forge in an open-world, multi-tab setting?

T<sub>a</sub>bl<sub>e</sub> 2<sub>:</sub> P<sub>er</sub>f<sub>ormance o</sub>f WF Att<sub>ac</sub>k<sub>s across</sub> dif<sub>eren</sub>t t<sub>a</sub>b <sub>num</sub>b<sub>er se</sub>tti<sub>ngs</sub> i<sub>n c</sub>l<sub>ose</sub>d <sub>wor</sub>ld<sub>.</sub>

<table><tr><td rowspan="2">Attacks</td><td colspan="3"> $D_{CW-2tab}$ </td><td colspan="3"> $D_{CW-3tab}$ </td><td colspan="3"> $D_{CW-4tab}$ </td><td colspan="3"> $D_{CW-5tab}$ </td></tr><tr><td>Pre</td><td>Recall</td><td>F1-score</td><td>Pre</td><td>Recall</td><td>F1-score</td><td>Pre</td><td>Recall</td><td>F1-score</td><td>Pre</td><td>Recall</td><td>F1-score</td></tr><tr><td>AWF</td><td>0.4864</td><td>0.0139</td><td>0.0270</td><td>0.3450</td><td>0.0040</td><td>0.0078</td><td>0.4691</td><td>0.0033</td><td>0.0065</td><td>0.3750</td><td>0.0013</td><td>0.0027</td></tr><tr><td>DF</td><td>0.8482</td><td>0.4838</td><td>0.6162</td><td>0.8419</td><td>0.2604</td><td>0.3978</td><td>0.8306</td><td>0.1747</td><td>0.2886</td><td>0.7526</td><td>0.0385</td><td>0.0732</td></tr><tr><td>Tik-Tok</td><td>0.8506</td><td>0.3868</td><td>0.5318</td><td>0.8321</td><td>0.1595</td><td>0.2677</td><td>0.8409</td><td>0.135</td><td>0.2326</td><td>0.8508</td><td>0.0944</td><td>0.1699</td></tr><tr><td>RF</td><td>0.6604</td><td>0.3983</td><td>0.4969</td><td>0.7387</td><td>0.5953</td><td>0.6593</td><td>0.6700</td><td>0.3390</td><td>0.4502</td><td>0.5598</td><td>0.2371</td><td>0.3331</td></tr><tr><td>BAPM</td><td>0.7837</td><td>0.3665</td><td>0.4994</td><td>0.7098</td><td>0.1951</td><td>0.3061</td><td>0.6871</td><td>0.1578</td><td>0.2567</td><td>0.6573</td><td>0.0971</td><td>0.1693</td></tr><tr><td>TMWF</td><td>0.7821</td><td>0.6702</td><td>0.7218</td><td>0.7043</td><td>0.5717</td><td>0.6311</td><td>0.6793</td><td>0.5561</td><td>0.6115</td><td>0.6202</td><td>0.4599</td><td>0.5282</td></tr><tr><td>ARES</td><td>0.8285</td><td>0.7011</td><td>0.7595</td><td>0.7971</td><td>0.6022</td><td>0.6861</td><td>0.8351</td><td>0.5930</td><td>0.6935</td><td>0.7619</td><td>0.3455</td><td>0.4754</td></tr><tr><td>FORGE</td><td>0.8527</td><td>0.7758</td><td>0.8124</td><td>0.8434</td><td>0.7378</td><td>0.7871</td><td>0.8430</td><td>0.7434</td><td>0.7900</td><td>0.8027</td><td>0.7336</td><td>0.7666</td></tr></table>

<sup>-</sup> Bold denotes the best results, and underline denotes the second-best results.

RQ3: How robust is Forge against established WF defenses? RQ4: How does Forge perform in dynamic environments? RQ5: How does Forge perform under network noise? RQ6: What is the contribution of each core component to Forge $\ ' _ { s }$ overall eficacy?

## 5.1 Ex<sub>p</sub>eriment Setu<sub>p</sub>

5.1.1 Datasets. We evaluate Forge on publicly available and mod ified datasets (details in Appendix B).

Closed- and Open-world: Sourced from WFLib [11], the closedworld dataset $D _ { \mathrm { { C W } } }$ covers Alexa Top 100 sites and is partitioned by concurrent tabs into $D _ { \mathrm { C W - 2 t a b } } { - } D _ { \mathrm { C W - 5 t a b } }$ . The open-world dataset $D _ { \mathrm { O W } }$ includes unmonitored sites and is partitioned similarly.

Defense Datasets: Six practical defenses are evaluated. Open source datasets �<sub>WTF-PAD</sub>, �<sub>Front</sub>, �<sub>Walkie-Talkie</sub>, and $D _ { \mathrm { T r a f f i c S l i v e r } }$ come from WFLib, while �<sub>Random</sub>, �<sub>RegularTor-Light</sub>, and �<sub>RegularTor-Heavy</sub> are constructed from $D _ { \mathrm { C W - 2 t a b } }$ (see Appendix E).

Dynamic Datasets: For dynamic evaluation, we sample and mix in stances across tab counts and defense schemes to form �<sub>mix-num-tabs</sub> and $D _ { \mathrm { m i x - d e f e n s e s } }$ (details in Appendix B).

Noise Datasets: Random noise is injected into $D _ { \mathrm { C W - 2 t a b } }$ to create $D _ { \mathrm { N o i s e } } ;$ parameters and strategies are detailed in Appendix F.

5.1.2 Baselines. To assess Forge, we compare it with seven estab lished WF methods across three categories. For readability, figures show five baselines, omitting the oldest from each of the last two categories. See the Appendix D for their results. (1) Single-tab WF attacks: AWF [31], which applies a classic CNN to packet-direction sequences. (2) Defense-resilient single-tab WF attacks: DF [34], a defense-aware CNN; Tik-Tok [30], which fuses directional and temporal features; and RF [32], which constructs a 2D feature matrix. (3) Multi-tab WF attacks: BAPM [18], which uses block segmentation with attention-based association for joint identification; ARES [12], a Transformer ensemble robust to obfuscation; and TMWF [20], which extract per-tab embeddings for joint recognition.

To ensure a fair comparison, all baseline models are adapted to perform multi-label classification. Specific details of these modifications are provided in Appendix C.

5.1.3 Metrics. Multi-Label Metrics: We use AUC [24], P@K and MAP@K [25]. For an instance, let � be the ground-truth label vector and �ˆ be the predicted probability vector. P@K (Precision at K) mea sures the proportion of correct labels within the top-� predictions.

Let $r _ { k } ( \hat { y } )$ be the set of labels with the top-� highest probabilities.

$$
P @ k = \frac {1}{k} \sum_ {l \in r _ {k} (\hat {y})} y _ {l}.\tag{5}
$$

MAP@K (Mean Average Precision at K) extends P@K by also considering the rank of the correct predictions, thus rewarding correctly identified labels that appear higher in the list.

$$
M A P @ k = \frac {\sum_ {i = 1} ^ {k} P @ i}{k}.\tag{6}
$$

Single-Label Metrics: We report standard metrics including Precision, Recall, and F1-Score, computed from true positives, false positives, true negatives, and false negatives.

5.1.4 Implementation. Our implementation of Forge is developed in PyTorch 2.4.1 and Python 3.10.5 consisting of over 1,500 lines of code. All experiments were performed on a server with an Intel(R)Xeon(R)Silver 4208 CPU. The hyperparameter configuration is detailed in Appendix A.

![](images/1b3b7919f956c5b542a4546879b6190938a8cfbab29f1312db1b51d2df6f4b19.jpg)

![](images/99626dd3dea981258544160a6df18139ad72c7fa5005c8240cb56bb345f519ec.jpg)  
Fi<sub>gure</sub> 4<sub>:</sub> P<sub>er</sub>f<sub>ormance compar</sub>i<sub>son o</sub>f dif<sub>eren</sub>t <sub>me</sub>th<sub>o</sub>d<sub>s on</sub> var<sub>y</sub>in<sub>g</sub> tab number settin<sub>g</sub>s.

## 5.2 Closed-world Evaluation(RQ1)

We evaluate Forge on closed-world datasets with varying tab counts using multiple metrics. Figure 4 shows AUC and MAP@k across tab settings in $D _ { \mathrm { { C W } } }$ . Forge outperforms all baselines in AUC, with single-page methods failing on multi-tab data and native multitab methods performing better; Forge remains stable even at 5 tabs. MAP@k, with � equal to the tab count, shows similar gains, with Forge consistently surpassing all WF attacks.

We further evaluate top-� predictions using Precision@k $( \mathrm { P } @ \mathbf { k } )$ the fraction of true sites within the top-�. Figure 5 shows Forge outperforms alternatives across tab counts. Its advantage grows with more tabs; on $D _ { \mathrm { C W - 5 t a b } }$ it still achieves high P@2, indicating a higher likelihood of recovering the user’s true sites.

![](images/45b7243296e16a6a3eb06f62ffaae73e88ca5e98a6ad5e12f320537953cb37c6.jpg)  
Fi<sub>gure</sub> 5<sub>:</sub> C<sub>ompar</sub>i<sub>son</sub> <sub>o</sub>f P<sub>rec</sub>i<sub>s</sub>i<sub>on@</sub>k f<sub>or</sub> dif<sub>eren</sub>t <sub>me</sub>th<sub>o</sub>d<sub>s</sub> <sub>on</sub> <sub>vary</sub>i<sub>ng</sub> t<sub>a</sub>b <sub>num</sub>b<sub>er</sub> <sub>se</sub>tti<sub>ngs.</sub>

Table 2 shows that Forge achieves the best results across almost all metrics. Tik-Tok has higher precision but much lower recall on $D _ { \mathrm { C W - 5 t a b } }$ , meaning it predicts very few positives and misses many true labels. Therefore, F1-score is the most appropriate metric here. Higher F1-score indicates a better balance and better performance.

![](images/2215a34c5d7bae793bb3ed9dd39bd43ea887e0a61f68d93b31ff9042c45b1ab3.jpg)  
Fi<sub>g</sub>ure 6: Com<sub>p</sub>arison of AUC <sub>p</sub>erformance on the o<sub>p</sub>en-W<sub>or</sub>ld d<sub>a</sub>t<sub>ase</sub>t <sub>across</sub> dif<sub>eren</sub>t t<sub>a</sub>b <sub>se</sub>tti<sub>ngs.</sub>

## 5.3 Open-world Evaluation(RQ2)

We extended our evaluation to an open-world scenario, classifying unmonitored websites into a single class. As Table 3 reports, Forge again demonstrated its superiority, achieving a 78.6% improvement of MAP@5 over the average. Furthermore, its AUC scores are the highest, approaching 1.0 (2-tab) and holding at 0.98 (5-tab), as shown in Figure 6. This confirms Forge’s ability to achieve SOTA accuracy under growing attack complexity.

## 5.4 Forge Against Defenses(RQ3)

We evaluate Forge ’s adversarial robustness in multi-tab settings against four WF defenses (Table 4). Forge consistently outperform all baselines. Against obfuscation defenses (Random, Front, WTF PAD), it shows strong resilience with AUCs of 0.985, 0.9996, and 0.999, respectively. Against the heavyweight defense RegularTor, Forge’s MAP@k dropped but still surpassed all baselines, though such defenses are noted as impractical due to overhead. In additional single-tab tests against Walkie-Talkie and TraficSliver, Forge again achieved the best results (Figure 7). We attribute this robustness to its architecture’s joint exploitation of time- and frequency-domain cues, which captures residual site-specific patterns that persist after defense.

## 5.5 Dynamic Settings(RQ4)

We evaluate Forge’s genericity in two dynamic scenarios: unknown tab numbers and unknown WF defenses. As shown in Table 5, Forge achieves an AUC of 0.985 in the multi-tab scenario. In the defense scenario, it achieves an AUC of 0.999. This genericity extends to mismatched training (Figure 8). For instance, a model trained on

T<sub>a</sub>bl<sub>e</sub> 3<sub>:</sub> WF <sub>a</sub>tt<sub>ac</sub>k <sub>per</sub>f<sub>ormance</sub> <sub>across</sub> <sub>vary</sub>i<sub>ng</sub> t<sub>a</sub>b <sub>num</sub>b<sub>ers.</sub>

<table><tr><td>Datasets</td><td>Attacks</td><td>Pre</td><td>AP@k</td><td>MAP@k</td></tr><tr><td rowspan="8"> $D_{\text{OW-2tab}}$ </td><td>AWF</td><td>0.4988▼42.3%</td><td>0.1587▼80.5%</td><td>0.1826▼79.2%</td></tr><tr><td>DF</td><td>0.8509▼1.6%</td><td>0.5830▼28.5%</td><td>0.6923▼21.2%</td></tr><tr><td>Tik-Tok</td><td>0.8832▲2.2%</td><td>0.6305▼22.7%</td><td>0.7368▼16.1%</td></tr><tr><td>RF</td><td>0.7534▼12.9%</td><td>0.6297▼22.8%</td><td>0.7155▼18.5%</td></tr><tr><td>BAPM</td><td>0.7800▼9.8%</td><td>0.5216▼36.0%</td><td>0.6134▼30.2%</td></tr><tr><td>TMWF</td><td>0.7868▼9.0%</td><td>0.6891▼15.5%</td><td>0.7597▼13.5%</td></tr><tr><td>ARES</td><td>0.8427▼2.5%</td><td>0.7448▼8.7%</td><td>0.8239▼6.2%</td></tr><tr><td>FORGE</td><td>0.8646▲12.2%1</td><td>0.8155▲44.2%</td><td>0.8782▲35.9%</td></tr><tr><td rowspan="8"> $D_{\text{OW-3tab}}$ </td><td>AWF</td><td>0.3733▼55.2%</td><td>0.1123▼85.5%</td><td>0.1292▼84.9%</td></tr><tr><td>DF</td><td>0.8451▲1.4%</td><td>0.4222▼45.5%</td><td>0.5637▼34.2%</td></tr><tr><td>Tik-Tok</td><td>0.8591▲3.0%</td><td>0.4483▼42.1%</td><td>0.5946▼30.6%</td></tr><tr><td>RF</td><td>0.6850▼17.8%</td><td>0.4823▼37.7%</td><td>0.6105▼28.8%</td></tr><tr><td>BAPM</td><td>0.7349▼11.9%</td><td>0.3830▼50.5%</td><td>0.4895▼42.9%</td></tr><tr><td>TMWF</td><td>0.6868▼17.6%</td><td>0.6087▼21.4%</td><td>0.6940▼19.0%</td></tr><tr><td>ARES</td><td>0.8163▼2.1%</td><td>0.6438▼16.8%</td><td>0.7706▼10.1%</td></tr><tr><td>FORGE</td><td>0.8338▲16.7%</td><td>0.7740▲74.7%</td><td>0.8569▲55.7%</td></tr><tr><td rowspan="8"> $D_{\text{OW-4tab}}$ </td><td>AWF</td><td>0.4701▼43.2%</td><td>0.1122▼85.4%</td><td>0.1317▼84.5%</td></tr><tr><td>DF</td><td>0.8528▲3.1%</td><td>0.3701▼51.9%</td><td>0.5069▼40.2%</td></tr><tr><td>Tik-Tok</td><td>0.8839▲6.8%</td><td>0.3859▼49.9%</td><td>0.5285▼37.6%</td></tr><tr><td>RF</td><td>0.6713▼18.9%</td><td>0.4383▼43.1%</td><td>0.5655▼33.3%</td></tr><tr><td>BAPM</td><td>0.6641▼19.7%</td><td>0.3435▼55.4%</td><td>0.4395▼48.1%</td></tr><tr><td>TMWF</td><td>0.6737▼18.6%</td><td>0.5875▼23.7%</td><td>0.6688▼21.1%</td></tr><tr><td>ARES</td><td>0.8129▼1.7%</td><td>0.6572▼14.7%</td><td>0.7775▼8.3%</td></tr><tr><td>FORGE</td><td>0.8273▲15.2%</td><td>0.7702▲86.3%</td><td>0.8476▲64.0%</td></tr><tr><td rowspan="8"> $D_{\text{OW-5tab}}$ </td><td>AWF</td><td>0.4318▼46.8%</td><td>0.1069▼85.4%</td><td>0.1234▼84.9%</td></tr><tr><td>DF</td><td>0.8528▲5.1%</td><td>0.3152▼56.9%</td><td>0.4475▼45.3%</td></tr><tr><td>Tik-Tok</td><td>0.8837▲8.9%</td><td>0.3167▼56.7%</td><td>0.4471▼45.3%</td></tr><tr><td>RF</td><td>0.5948▼26.7%</td><td>0.3713▼49.2%</td><td>0.4835▼40.9%</td></tr><tr><td>BAPM</td><td>0.6168▼24.0%</td><td>0.3092▼57.7%</td><td>0.3984▼51.3%</td></tr><tr><td>TMWF</td><td>0.6375▼21.5%</td><td>0.5172▼29.3%</td><td>0.6060▼25.9%</td></tr><tr><td>ARES</td><td>0.7831▼3.5%</td><td>0.5560▼24.0%</td><td>0.7003▼14.4%</td></tr><tr><td>FORGE</td><td>0.8116▲18.3%</td><td>0.7312▲105.4%</td><td>0.8181▲78.6%</td></tr></table>

▼%= % reduction, ▲% = % improvement.  
<sup>-</sup> Bold denotes the best, and underline denotes the second-best.  
<sup>1</sup> Improvement over other methods’ average.

![](images/3f9b7572bd9ad1ef7fc5cbacc6fb598c4aa60362765e1d10cfd3cf5d41096ec0.jpg)

![](images/fc324ef9520c5412f51134e198ebc346cf5e9958b19cf828ff49902680496c25.jpg)  
Fi<sub>gu</sub>r<sub>e</sub> 7: C<sub>o</sub>m<sub>pa</sub>ri<sub>so</sub>n <sub>o</sub>f AUC <sub>a</sub>nd <sub>p</sub>r<sub>ec</sub>i<sub>s</sub>i<sub>o</sub>n <sub>u</sub>nd<sub>e</sub>r W<sub>a</sub>lki<sub>e</sub>- T<sub>a</sub>lki<sub>e an</sub>d T<sub>ra</sub>fi<sub>c</sub>Sli<sub>ver on</sub> th<sub>e s</sub>i<sub>ng</sub>l<sub>e-</sub>t<sub>a</sub>b <sub>se</sub>tti<sub>ng.</sub>

4-tab data achieves a high AUC of 0.85 on 3-tab data, confirming its efectiveness without precise prior knowledge.

T<sub>a</sub>bl<sub>e</sub> 4<sub>:</sub> WF <sub>a</sub>tt<sub>ac</sub>k <sub>per</sub>f<sub>ormance un</sub>d<sub>er</sub> f<sub>our represen</sub>t<sub>a</sub>ti<sub>ve</sub> d<sub>e</sub>f<sub>enses on</sub> th<sub>e</sub> 2<sub>-</sub>t<sub>a</sub>b <sub>se</sub>tti<sub>ng.</sub>

<table><tr><td rowspan="2">Attacks</td><td colspan="3">Random</td><td colspan="3">Front</td><td colspan="3">WTF-PAD</td><td colspan="3">RegularTor-Light</td><td colspan="3">RegularTor-Heavy</td></tr><tr><td>Pre</td><td>AUC</td><td>MAP@k</td><td>Pre</td><td>AUC</td><td>MAP@k</td><td>Pre</td><td>AUC</td><td>MAP@k</td><td>Pre</td><td>AUC</td><td>MAP@k</td><td>Pre</td><td>AUC</td><td>MAP@k</td></tr><tr><td>AWF</td><td>0.4693</td><td>0.7246</td><td>0.1381</td><td>0.6946</td><td>0.9224</td><td>0.2991</td><td>0.6855</td><td>0.9610</td><td>0.4431</td><td>0.0000</td><td>0.5509</td><td>0.0363</td><td>0.0000</td><td>0.5530</td><td>0.0342</td></tr><tr><td>DF</td><td>0.8183</td><td>0.9181</td><td>0.6081</td><td>0.8791</td><td>0.9949</td><td>0.6423</td><td>0.9242</td><td>0.9987</td><td>0.6980</td><td>0.7640</td><td>0.7778</td><td>0.3126</td><td>0.7935</td><td>0.7477</td><td>0.2434</td></tr><tr><td>Tik-Tok</td><td>0.8665</td><td>0.9414</td><td>0.6859</td><td>0.9275</td><td>0.9983</td><td>0.6898</td><td>0.9592</td><td>0.9994</td><td>0.7165</td><td>0.7776</td><td>0.8035</td><td>0.3595</td><td>0.7717</td><td>0.7647</td><td>0.2638</td></tr><tr><td>RF</td><td>0.7743</td><td>0.9416</td><td>0.7030</td><td>0.9557</td><td>0.9967</td><td>0.7054</td><td>0.9672</td><td>0.9978</td><td>0.7182</td><td>0.0000</td><td>0.5051</td><td>0.0272</td><td>0.0000</td><td>0.5034</td><td>0.0273</td></tr><tr><td>BAPM</td><td>0.7407</td><td>0.9139</td><td>0.5253</td><td>0.8293</td><td>0.9817</td><td>0.5277</td><td>0.8617</td><td>0.9944</td><td>0.6460</td><td>0.6662</td><td>0.8129</td><td>0.2795</td><td>0.6466</td><td>0.7935</td><td>0.2357</td></tr><tr><td>TMWF</td><td>0.7240</td><td>0.9574</td><td>0.6999</td><td>0.8808</td><td>0.9942</td><td>0.6318</td><td>0.9306</td><td>0.9978</td><td>0.6909</td><td>0.6260</td><td>0.9040</td><td>0.4850</td><td>0.7173</td><td>0.8754</td><td>0.4011</td></tr><tr><td>ARES</td><td>0.7890</td><td>0.9714</td><td>0.7659</td><td>0.9428</td><td>0.9994</td><td>0.7136</td><td>0.9426</td><td>0.9993</td><td>0.7063</td><td>0.7293</td><td>0.9342</td><td>0.5775</td><td>0.7123</td><td>0.9187</td><td>0.5149</td></tr><tr><td>FORGE</td><td>0.8500</td><td>0.9848</td><td>0.8536</td><td>0.9641</td><td>0.9996</td><td>0.7220</td><td>0.9713</td><td>0.9998</td><td>0.7294</td><td>0.7195</td><td>0.9486</td><td>0.6467</td><td>0.7270</td><td>0.9357</td><td>0.5827</td></tr></table>

<sup>-</sup> Bold denotes the best results, and underline denotes the second-best results.

![](images/8f2f071f63b1c1d23b240f58924ac15feb1565465f5feba25e06e26efa5399b9.jpg)

![](images/d08bd740469d3bf2a02ad1091aab8077d99ef02b979e10f0a1c4691814335aea.jpg)  
Fi<sub>g</sub>ure 8: AUC curve of FORGE when the number of tabs difers between trainin<sub>g</sub> and testin<sub>g</sub>.

T<sub>a</sub>bl<sub>e</sub> 5<sub>:</sub> P<sub>er</sub>f<sub>ormance un</sub>d<sub>er</sub> Mi<sub>x</sub> t<sub>a</sub>b <sub>se</sub>tti<sub>ngs an</sub>d Mi<sub>x</sub> d<sub>e-</sub> f<sub>enses.</sub>

<table><tr><td rowspan="2">Attacks</td><td colspan="3"> $D_{\text{mix-num-tabs}}$ </td><td colspan="3"> $D_{\text{mix-defenses}}$ </td></tr><tr><td>Pre</td><td>AUC</td><td>AP@5</td><td>Pre</td><td>AUC</td><td>AP@2</td></tr><tr><td>AWF</td><td>0.5070</td><td>0.6515</td><td>0.1316</td><td>0.4993</td><td>0.8949</td><td>0.2344</td></tr><tr><td>DF</td><td>0.9034</td><td>0.8264</td><td>0.4642</td><td>0.8127</td><td>0.9896</td><td>0.5840</td></tr><tr><td>Tik-Tok</td><td>0.9254</td><td>0.8438</td><td>0.4977</td><td>0.8538</td><td>0.9951</td><td>0.6401</td></tr><tr><td>RF</td><td>0.7780</td><td>0.8563</td><td>0.5192</td><td>0.9472</td><td>0.9924</td><td>0.6778</td></tr><tr><td>BAPM</td><td>0.7598</td><td>0.8426</td><td>0.4171</td><td>0.6969</td><td>0.9742</td><td>0.4776</td></tr><tr><td>TMWF</td><td>0.7488</td><td>0.9176</td><td>0.5757</td><td>0.8184</td><td>0.9889</td><td>0.5805</td></tr><tr><td>ARES</td><td>0.8518</td><td>0.9646</td><td>0.7071</td><td>0.7873</td><td>0.9923</td><td>0.5865</td></tr><tr><td>FORGE</td><td>0.8500</td><td>0.9848</td><td>0.8536</td><td>0.9192</td><td>0.9986</td><td>0.6892</td></tr></table>

Bold denotes the best, and underline denotes the second-best.

![](images/94e996e2e31f6dd0ed7f9cd13348327b0dcdb6774f9a6bc2eeb151267dfd1ce6.jpg)  
(a) Waveform Changes.

![](images/586f31b9bc65db2eac2843aa9588469a315cc15a478a9826ee2a4bb84ab2c6c0.jpg)  
(b) AUC performance.  
Figure 9: Analysis of Noise Interference Efects.(a) Changes in the ���� × ��������� waveform under diferent noise interferences; (b) AUC of diferent models across noise intensities.

## 5.6 Forge Against Noise(RQ5)

We evaluate Forge’s noise robustness by simulating packet loss, timing jitter, and out-of-order packets [41] at levels from 0.1% to 10%. AWF is omitted due to severe degradation (see Appendix D). As shown in Figure 9b, Forge significantly outperforms baselines, maintaining an AUC above 0.9 even at 10% noise. This robustness stems from precise temporal modeling in the channel construction module and the DDCA module’s joint time–frequency analysis.

T<sub>a</sub>bl<sub>e</sub> 6<sub>:</sub> Abl<sub>a</sub>ti<sub>on ana</sub>l<sub>ys</sub>i<sub>s o</sub>f Fo<sub>r</sub>g<sub>e.</sub>

<table><tr><td>Test Case</td><td>Time Delay Embedding</td><td>BSS Solver</td><td>Website Identifier</td><td>P@2</td><td>MAP@2</td></tr><tr><td>Case1</td><td>X</td><td>√</td><td>√</td><td>0.7253▼9.5%</td><td>0.7889▼8.7%</td></tr><tr><td>Case2</td><td>√</td><td>X</td><td>√</td><td>0.3478▼56.6%</td><td>0.4114▼52.4%</td></tr><tr><td>Case3</td><td>√</td><td>√</td><td>X</td><td>0.7012▼12.5%</td><td>0.8034▼7.0%</td></tr><tr><td>Case4</td><td>√</td><td>√</td><td>√</td><td>0.8016</td><td>0.8640</td></tr></table>

<sup>-</sup> ▼%= % reduction.

## 5.7 Ablation Study(RQ6)

We conduct an ablation study on �<sub>CW-2tab</sub> to evaluate Forge ’s core components. Table 6 shows that removing any module significantly degrades performance: replacing state vectors with raw sequences reduces MAP@2 by 7.51%; removing the BSS solver causes a larger 45.26% drop; and substituting the specialized identifier with a linear model lowers MAP@2 from 0.864 to 0.803.

## 6 C<sub>o</sub>n<sub>c</sub>l<sub>us</sub>i<sub>o</sub>n

In this paper, we introduce Forge, a multi-tab WF attack that reframes the task as a BSS problem. This shift enables Forge to blindly identify an unknown number of websites from mixed trafic streams. Forge comprises a novel BSS solver for trafic demixing and a robust identifier with Dual-Domain Consistency Attention to withstand WF defenses and network noise. We conduct comprehensive evaluations across multiple datasets and settings, demonstrating that Forge consistently surpasses prior state-of-the-art attacks in closedand open-world regimes, under defense-enabled conditions, and in other challenging, real-world scenarios.

## A<sub>c</sub>k<sub>now</sub>l<sub>e</sub>d<sub>gmen</sub>t<sub>s</sub>

This research is supported by National Key Research and Development Program ofChina (No.2023YFC2206402), the Strategic Priority Research Program of the Chinese Academy of Sciences (No.XDA046 0100), and Open Foundation of Key Laboratory of Cyberspace Security, Ministry of Education of China (No.KLCS20240206). This work is also supported by the Program of Key Laboratory of Network Assessment Technology, the Chinese Academy of Sciences, Program of Beijing Key Laboratory of Network Security and Protection Technology.

## R<sub>e</sub>f<sub>erences</sub>

[1] Alireza Bahramali, Ardavan Bozorgi, and Amir Houmansadr. 2023. Realistic website fingerprinting by augmenting network traces. In Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security. 1035–1049.

[2] Sanjit Bhat, David Lu, Albert Kwon, and Srinivas Devadas. 2019. Var-CNN: A Data-Eficient Website Fingerprinting Attack Based on Deep Learning. Proceedings on Privacy Enhancing Technologies 2019 (10 2019), 292–310. doi:10.2478/popets-2019-0070

[3] Xiang Cai, Rishab Nithyanand, and Rob Johnson. 2014. Cs-buflo: A congestion sensitive website fingerprinting defense. In Proceedings of the 13th Workshop on Privacy in the Electronic Society. 121–130

[4] Xiang Cai, Rishab Nithyanand, Tao Wang, Rob Johnson, and Ian Goldberg. 2014. A systematic approach to developing and evaluating website fingerprinting defenses. In Proceedings ofthe 2014 ACM SIGSAC conference on computer and communications security. 227–238.

[5] Jean-François Cardoso. 1998. Blind Signal Separation: Statistical Principles. Proc. IEEE 86, 10 (1998), 2009–2025. doi:10.1109/5.720250

[6] Yen-Lin Chen, Yuan Chiang, Pei-Hsin Chiu, I-Chen Huang, Yu-Bai Xiao, Shu-Wei Chang, and Chang-Wei Huang. 2021. High-Dimensional Phase Space Recon struction with a Convolutional Neural Network for Structural Health Monitoring. Sensors 21, 10 (2021), 3514. doi:10.3390/s21103514

[7] Giovanni Cherubin, Rob Jansen, and Carmela Troncoso. 2022. Online website fingerprinting: Evaluating website fingerprinting attacks on tor in the real world. In 31st USENIX Security Symposium (USENIX Security 22). 753–770.

[8] Thomas Cover and Peter Hart. 1967. Nearest neighbor pattern classification. IEEE transactions on information theory 13, 1 (1967), 21–27.

[9] Weiqi Cui, Tao Chen, Christian Fields, Julianna Chen, Anthony Sierra, and Eric Chan-Tin. 2019. Revisiting assumptions for website fingerprinting attacks. In Proceedings of the 2019 ACM asia conference on computer and communications security. 328–339.

[10] Wladimir De la Cadena, Asya Mitseva, Jens Hiller, Jan Pennekamp, Sebastian Reuter, Julian Filter, Thomas Engel, Klaus Wehrle, and Andriy Panchenko. 2020. Traficsliver: Fighting website fingerprinting attacks with trafic splitting. In Proceedings ofthe 2020 ACMSIGSAC Conference on Computerand Communications Security. 1971–1985.

[11] Xinhao Deng, Qi Li, and Ke Xu. 2024. Robust and Reliable Early-Stage Website Fingerprinting Attacks via Spatial-Temporal Distribution Analysis. In Proceedings ofthe 2024 ACM SIGSAC Conference on Computer and Communications Security.

[12] Xinhao Deng, Qilei Yin, Zhuotao Liu, Xiyuan Zhao, Qi Li, Mingwei Xu, Ke Xu, and Jianping Wu. 2023. Robust multi-tab website fingerprinting attacks in the wild. In 2023 IEEE symposium on security and privacy (SP). IEEE, 1005–1022.

[13] Roger Dingledine, Nick Mathewson, and Paul Syverson. 2004. Tor: The Second Generation Onion Router. In 13th USENIX Security Symposium (USENIX Security 04). USENIX Association, San Diego, CA. https://www.usenix.org/conference/ 13th-usenix-security-symposium/tor-second-generation-onion-router

[14] Priyanka Dodia, Mashael AlSabah, Omar Alrawi, and Tao Wang. 2022. Exposing the rat in the tunnel: Using trafic analysis for tor-based malware detection. In Proceedings ofthe 2022 ACMSIGSAC Conference on Computerand Communications Security. 875–889.

[15] William Gilpin. 2020. Deep Reconstruction of Strange Attractors from Time Series. In Advances in Neural Information Processing Systems (NeurIPS), Vol. 33.

[16] Jiajun Gong and Tao Wang. 2020. Zero-delay lightweight defenses against website fingerprinting. In 29th USENIX Security Symposium (USENIX Security 20). 717–734.

[17] Jiajun Gong, Wuqi Zhang, Charles Zhang, and Tao Wang. 2022. Surakav: Generating realistic traces for a strong website fingerprinting defense. In 2022 IEEE Symposium on Security and Privacy (SP). IEEE, 1558–1573.

[18] Zhong Guan, Gang Xiong, Gaopeng Gou, Zhen Li, Mingxin Cui, and Chang Liu. 2021. BAPM: block attention profiling model for multi-tab website fingerprinting attacks on tor. In Proceedings ofthe 37th Annual Computer Security Applications Conference. 248–259.

[19] James K Holland and Nicholas Hopper. 2020. Regulator: A straightforward website fingerprinting defense. arXiv preprint arXiv:2012.06609 (2020).

[20] Zhaoxin Jin, Tianbo Lu, Shuang Luo, and Jiaze Shang. 2023. Transformer-based model for multi-tab website fingerprinting attack. In Proceedings ofthe 2023 ACM SIGSAC Conference on Computer and Communications Security. 1050–1064.

[21] Marc Juarez, Sadia Afroz, Gunes Acar, Claudia Diaz, and Mario Grattafiori. 2014. A Critical Evaluation of Website Fingerprinting Attacks. In Proceedings of the 2014 ACM SIGSAC Conference on Computer and Communications Security (Scottsdale, Arizona, USA) (CCS ’14). Association for Computing Machinery, New York, NY, USA, 763–774. doi:10.1145/2660267.2660368

[22] Marc Juarez, Sadia Afroz, Gunes Acar, Claudia Diaz, and Mario Grattafiori. 2016. k-fingerprinting: A Robust Scalable Website Fingerprinting Technique. In 25th USENIX Security Symposium (USENIX Security ’16). USENIX Association, Austin, TX, USA, 1139–1154.

[23] Marc Juárez, Mohsen Imani, Mike Perry, Claudia Dıaz, and Matthew Wright. 2015. WTF-PAD: toward an eficient website fingerprinting defense for tor. CoRR,

abs/1512.00524 (2015).

[24] Charles X Ling,Jin Huang, Harry Zhang, et al. 2003. AUC: a statistically consistent and more discriminating measure than accuracy. In Ijcai, Vol. 3. 519–524.

[25] Jingzhou Liu, Wei-Cheng Chang, Yuexin Wu, and Yiming Yang. 2017. Deep learning for extreme multi-label text classification. In Proceedings ofthe 40th international ACM SIGIR conference on research and development in information retrieval. 115–124.

[26] Se Eun Oh, Taiji Yang, Nate Mathews, James K Holland, Mohammad Saidur Rahman, Nicholas Hopper, and Matthew Wright. 2022. Deepcofea: Improved flow correlation attacks on tor via metric learning and amplification. In 2022 IEEE Symposium on Security and Privacy (SP). IEEE, 1915–1932.

[27] Andriy Panchenko, Fabian Lanze,Jan Pennekamp, Thomas Engel, Andreas Zinner, Martin Henze, and Klaus Wehrle. 2011. Website Fingerprinting: Attacking Popular Privacy Enhancing Technologies with the Multinomial Naïve-Bayes Classifier. In Proceedings ofthe 2011 ACM SIGCOMM Conference on Internet Measurement Conference (Berlin, Germany) (IMC ’11). Association for Computing Machinery, New York, NY, USA, 15–28. doi:10.1145/2068816.2068819

[28] Andriy Panchenko, Fabian Lanze, Andreas Zinnen, Martin Henze, Jan Pennekamp, Klaus Wehrle, and Thomas Engel. 2016. Website Fingerprinting at Internet Scale. doi:10.14722/ndss.2016.23477

[29] Andriy Panchenko, Lukas Niessen, Andreas Zinnen, and Thomas Engel. 2011. Website fingerprinting in onion routing based anonymization networks. In Proceedings ofthe 10th annual ACM workshop on Privacy in the electronic society. 103–114.

[30] Mohammad Saidur Rahman, Payap Sirinam, Nate Mathews, Kantha Gangadhara, and Matthew Wright. 2020. Tik-Tok: The Utility of Packet Timing in Website Fingerprinting Attacks. Proceedings on Privacy Enhancing Technologies 2020 (07 2020), 5–24. doi:10.2478/popets-2020-0043

[31] Vera Rimmer, Davy Preuveneers, Marc Juarez, Tom Van Goethem, and Wouter Joosen. 2017. Automated website fingerprinting through deep learning. arXiv preprint arXiv:1708.06376 (2017).

[32] Meng Shen, Kexin Ji, Zhenbo Gao, Qi Li, Liehuang Zhu, and Ke Xu. 2023. Subverting website fingerprinting defenses with robust trafic representation (SEC ’23). USENIX Association, USA, Article 35, 18 pages.

[33] Meng Shen, Kexin Ji, Jinhe Wu, Qi Li, Xiangdong Kong, Ke Xu, and Liehuang Zhu. 2024. Real-time website fingerprinting defense via trafic cluster anonymization. In 2024 IEEE Symposium on Security and Privacy (SP). IEEE, 3238–3256.

[34] Payap Sirinam, Mohsen Imani, Marc Juarez, and Matthew Wright. 2018. Deep Fingerprinting: Undermining Website Fingerprinting Defenses with Deep Learning. In Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security (Toronto, Canada) (CCS ’18). Association for Computing Machinery, New York, NY, USA, 1928–1943. doi:10.1145/3243734.3243768

[35] Eugene Tan, Shannon Algar, Débora Corrêa, Michael Small, Thomas Stemler, and David Walker. 2023. Selecting Embedding Delays: An Overview of Embedding Techniques and a New Method Using Persistent Homology. Chaos 33, 3 (2023), 032101. doi:10.1063/5.0137223

[36] Carmela Troncoso, Sergej Prokhorenko, Pjotr Kopytko, Wouter Joosen, and George Danezis. 2017. Touching from a Distance: Website Fingerprinting Attacks and Defenses. Proceedings on Privacy Enhancing Technologies 2017, 4 (2017), 127–145. doi:10.1515/popets-2017-0040

[37] Chunmian Wang, Zhen Ling, Wenjia Wu, Qi Chen, Ming Yang, and Xinwen Fu. 2022. Large-scale evaluation of malicious tor hidden service directory discovery. In IEEE INFOCOM 2022-IEEE Conference on Computer Communications. IEEE, 1709–1718.

[38] Tao Wang. 2020. High precision open-world website fingerprinting. In 2020 IEEE Symposium on Security and Privacy (SP). IEEE, 152–167.

[39] Tao Wang, Xiang Cai, Rishab Nithyanand, Rob Johnson, and Ian Goldberg. 2014. Efective attacks and provable defenses for website fingerprinting. In Proceedings ofthe 23rd USENIX Conference on Security Symposium (San Diego, CA) (SEC’14). USENIX Association, USA, 143–157.

[40] Tao Wang and Ian Goldberg. 2017. {Walkie-Talkie}: An eficient defense against passive website fingerprinting attacks. In 26th USENIX Security Symposium (USENIX Security 17). 1375–1390.

[41] Renjie Xie, Yixiao Wang, Jiahao Cao, Enhuan Dong, Mingwei Xu, Kun Sun, Qi Li, Licheng Shen, and Menghao Zhang. 2023. Rosetta: Enabling robust tls encrypted trafic classification in diverse network environments with tcp-aware trafic augmentation. In Proceedings ofthe ACM turing award celebration conference-China 2023. 131–132.

[42] Hui Xue, Qiang Yang, and Songcan Chen. 2009. SVM: Support vector machines. In The top ten algorithms in data mining. Chapman and Hall/CRC, 51–74.

[43] Qilei Yin, Zhuotao Liu, Qi Li, Tao Wang, Qian Wang, Chao Shen, and Yixiao Xu. 2021. An automated multi-tab website fingerprinting attack. IEEE Transactions on Dependable and Secure Computing 19, 6 (2021), 3656–3670.

[44] Xiyuan Zhao, Xinhao Deng, Qi Li, Yunpeng Liu, Zhuotao Liu, Kun Sun, and Ke Xu. 2024. Towards fine-grained webpage fingerprinting at scale. In Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security. 423–436.

Table 7: Parameter Settin<sub>g</sub>s

<table><tr><td>Module Part</td><td>Design Details</td><td>Value</td></tr><tr><td rowspan="4">Sequence Division</td><td>Channels</td><td>8</td></tr><tr><td>Interval</td><td>20</td></tr><tr><td>Signal Duration</td><td>8000</td></tr><tr><td>Length alignment</td><td>truncate/pad to seq_len</td></tr><tr><td rowspan="6">Local Profiling</td><td>Number of blocks</td><td>4</td></tr><tr><td>Number of filters</td><td>[32, 64, 128, 256]</td></tr><tr><td>Kernel size</td><td>[7, 7, 7, 7]</td></tr><tr><td>Pool (kernel/stride)</td><td>[(8/4), (8/4), (8/4), (8/4)]</td></tr><tr><td>Dropout (per stage)</td><td>0.1</td></tr><tr><td>Output dimension</td><td>256</td></tr><tr><td rowspan="7">Website Identification</td><td>Number of Transformer blocks</td><td>2</td></tr><tr><td>Number of heads</td><td>8</td></tr><tr><td>Dimension of head</td><td>32</td></tr><tr><td>Embedding dimension</td><td>256</td></tr><tr><td>Dimension of MLP</td><td>1024</td></tr><tr><td>Positional embedding</td><td>learnable, length = max_len</td></tr><tr><td>Output dimension</td><td>num_classes</td></tr></table>

![](images/6e1b60e479b739dbe90b2e3cdf0e7c06954e0a4d90dcf81224f4cbcf3d5a098f.jpg)

![](images/585e5d770b18617ed637587d7639e7f52c856cfd08741d3550274cc34f16b3a1.jpg)  
Fi<sub>g</sub>ure 10: Parameter anal<sub>y</sub>sis of Forge. We select the interval <sub>�</sub> <sub>an</sub>d <sub>sequence</sub> l<sub>eng</sub>th �<sub>.</sub>

## A P<sub>a</sub>r<sub>a</sub>m<sub>e</sub>t<sub>e</sub>r S<sub>e</sub>ttin<sub>gs</sub>

We choose the parameters with the best performance after tests. The settings of parameter values are shown in Table 7.

Parameter Analysis: We evaluate Forge ’s sensitivity to its key parameters, the aggregation interval � and sequence length � on � (Figure 10). The system is robust: varying � from 10 ms to 50 ms keeps MAP@2 between 0.838 and 0.885; performance is similarly insensitive to �. This stability indicates efectiveness stems from the architecture rather than fine-tuning. By default, we set �=20 and �=8000 to balance time and accuracy.

## B Dataset Details

The experiments presented in this paper utilize the publicly available multi-tab WF datasets from the WFLib collection [11]. These datasets contain encrypted trafic traces from realistic multi-tab browsing sessions over Tor. The primary feature extracted and used from each trace is the packet direction sequence.

The WFLib collection is structured into three main categories: closed-world, open-world, and defended scenarios.

## B<sub>.</sub>1 Cl<sub>ose</sub>d<sub>-</sub>W<sub>or</sub>ld D<sub>a</sub>t<sub>ase</sub>t<sub>s</sub>

This dataset models a scenario where users only visit websites from a predefined monitored set of 100 top Alexa websites. Each traffic instance represents a browsing session with � concurrent tabs, where � is set from two to five. The � websites for each session are a specific combination randomly selected from the 100 moni tored sites. For each �-tab setting, the dataset contains thousands of unique website combinations. To ensure data quality, each combination included in the final dataset has at least 10 recorded trafic instances.

## B.2 O<sub>p</sub>en-World Datasets

This dataset simulates a more realistic scenario where users also visit unmonitored websites. A �-tab open-world instance is composed of � − 1 websites from the monitored set (the same 100 top sites) and one website from a large unmonitored pool (Alexa top 101 to 20,000). All websites from the unmonitored pool are assigned a single, common label. Due to the vast number of possible combinations, each unique open-world website combination was collected only once. The dataset ensures that each selected unmonitored website is used in only one instance.

## B.3 Defense Datasets

This category is designed to evaluate WF resilience against countermeasures. Some defended trafic was collected under a two-tab, closed-world setting, while some was collected under a single-tab setting. Two distinct 2-tab defense datasets are provided, each corresponding to a specific defense mechanism applied to the trafic. Each of the defense datasets contains 20,000 2-tab trafic instances. The defenses are:

Front [16]: Front applies strong padding and timing randomization in early session phases, where classifiers extract the most discriminative features, and relaxes shaping thereafter. This degrades early stage identifiability with low to moderate, front-loaded overhead. Deployment is moderately dificult, as efectiveness relies on accurate phase detection across heterogeneous sites, and is enhanced when combined with lightweight later-phase padding.

WTF-PAD [23]: WTF-PAD is an adaptive padding defense that targets burst-level features by probabilistically injecting dummy trafic during idle gaps and smoothing burst boundaries, reducing deterministic patterns while preserving responsiveness. Its overhead is typically low to moderate, with tens-of-percent bandwidth cost and modest latency, as padding is focused on idle periods. Deployment is moderately dificult: while it integrates cleanly with Tor, performance is sensitive to parameter choices, with conservative settings ofering limited protection and aggressive padding degrading performance.

Additionally, this collection provides two single-page datasets, namely:

Walkie-Talkie [40]: Walkie-Talkie enforces half-duplex communication and aligns flows to precomputed templates, causing traces from diferent sites to collide under burst-based features. While this provides strong theoretical obfuscation, it incurs high latency and bandwidth overhead due to half-duplex alternation and template padding. Deployment is challenging given modern web dynamism, CDN variability, and content churn, which complicate stable template maintenance and degrade user experience.

TraficSliver [10]: TraficSliver confuses classifiers by slicing or replicating session portions across auxiliary paths or decoy flows, breaking the one-to-one mapping between traces and sites. Overhead is variable and often high, increasing with noise and duplication; latency can be mitigated if primary paths are prioritized, though multipath coordination may cause delays. Deployment is challenging, requiring client/network support and careful policy design to prevent trivial de-noising, with infrastructure and operational complexity as main barriers.

T<sub>a</sub>bl<sub>e</sub> 8<sub>:</sub> D<sub>a</sub>t<sub>ase</sub>t<sub>s overv</sub>i<sub>ew</sub>

<table><tr><td>Datasets</td><td># of monitored websites</td><td># of instances</td></tr><tr><td>Closed_2tab.npz</td><td>100</td><td>58,000</td></tr><tr><td>Closed_3tab.npz</td><td>100</td><td>58,000</td></tr><tr><td>Closed_4tab.npz</td><td>100</td><td>58,000</td></tr><tr><td>Closed_5tab.npz</td><td>100</td><td>58,000</td></tr><tr><td>Open_2tab.npz</td><td>100</td><td>64,000</td></tr><tr><td>Open_3tab.npz</td><td>100</td><td>64,000</td></tr><tr><td>Open_4tab.npz</td><td>100</td><td>64,000</td></tr><tr><td>Open_5tab.npz</td><td>100</td><td>64,000</td></tr><tr><td>WTF-PAD.npz</td><td>95</td><td>105,730</td></tr><tr><td>Front.npz</td><td>95</td><td>95,000</td></tr><tr><td>Walkie-Talkie.npz*</td><td>100</td><td>90,000</td></tr><tr><td>TrafficSliver.npz*</td><td>95</td><td>95,000</td></tr></table>

<sup>∗</sup> Single-tab dataset.

Additionally, we simulated defense deployments on our $D _ { C W - 2 t a b }$ and constructed two datasets; the simulation procedures are detailed in the Appendix. The two defenses are, respectively, random noise injection and:

RegulaTor [19]: RegulaTor is a surge-shaped regularization de fense that standardizes Tor download bursts and synchronizes uploads to suppress early-phase and burst-level identifiers. It starts downloads at a fixed, decaying rate, triggers new surges when queues exceed thresholds, and fills idle slots with dummy cells; uploads follow a fixed ratio with capped delay. Overhead is mainly bandwidth (tens-of-percent to <100%) with low latency, outperform ing constant-rate schemes and comparable to adaptive padding. De ployment is straightforward as a pluggable transport or near-entry padding module, with parameters transferring well across datasets.

Other heavyweight defenses, such as Tamaraw [4] and BuFLO [3], can theoretically provide strong protection by enforcing constantrate transmission that removes time- and frequency-domain features, but are impractical in real-world settings and thus not evalu ated here.

## B.4 D<sub>y</sub>namic Datasets

Motivated by practical uncertainty—where the number of open tabs and the deployed WF defense may not be directly observable—we construct evaluation datasets by randomly sampling and mixing trafic instances under diferent conditions.

Dynamic multi-tab datasets. We randomly sample and mix 100,000 closed-world instances and 20,000 open-world instances from the multi-tab corpus. The tab-count distribution is fixed as follows: 40% with 2 tabs, 30% with 3 tabs, 20% with 4 tabs, and 10% with 5 tabs. Dynamic defense datasets. For datasets with diferent monitoring settings cannot be mixed even if they share the same label dimensionality, to ensure label alignment, we only mix instances collected under defenses that share the same monitoring set. In our experiments, this criterion is met by WTF-PAD and Front. We therefore randomly sample and mix 30,000 instances in total, drawn equally from these two defenses (15,000 WTF-PAD and 15,000 Front).

## C Sin<sub>g</sub>le-tab Methods Ada<sub>p</sub>tation

Referring to similar work [12], we adapt four single-label WF attack models—AWF, DF, Tik-Tok and RF—so they operate in a multi-label regime. We use binary cross-entropy(BCE) to supervise independent sigmoid outputs per class, enabling the models to learn multiple concurrent labels for each trace and thereby complete the transition from single-label to multi-label classification.

Let x denote the input and $\mathbf { y } \in \{ 0 , 1 \} ^ { K }$ the multi-hot label vector over � sites/tabs. A model $f _ { \theta }$ produces logits $\mathbf { z } = f _ { \boldsymbol { \theta } } ( \mathbf { x } ) \in \mathbb { R } ^ { K }$ and posterior estimates via a sigmoid layer:

$$
\hat {\mathbf {y}} = \sigma (\mathbf {z}), \quad \sigma (z _ {k}) = \frac {1}{1 + e ^ {- z _ {k}}}.\tag{7}
$$

The multi-label training objective is the BCE loss:

$$
\mathcal {L} _ {\mathrm{BCE}} (\mathbf {y}, \hat {\mathbf {y}}) = - \sum_ {k = 1} ^ {K} \left[ y _ {k} \log \hat {y} _ {k} + (1 - y _ {k}) \log (1 - \hat {y} _ {k}) \right]\tag{8}
$$

Optionally, a class-imbalance prior with positive weights $w _ { k } > 0$ yields:

$$
\mathcal {L} _ {\mathrm{WBCE}} = - \sum_ {k = 1} ^ {K} \left[ w _ {k} y _ {k} \log \hat {y} _ {k} + (1 - y _ {k}) \log (1 - \hat {y} _ {k}) \right]\tag{9}
$$

At inference time, predictions are made independently for each label as follows:

$$
\hat {y} _ {k} = \mathbb {I} \left[ \hat {y} _ {k} \geq \tau_ {k} \right], \quad \tau_ {k} \in (0, 1)\tag{10}
$$

, where thresholds $\{ \tau _ { k } \}$ can be tuned for desired precision–recall trade-ofs.

Embedding-based approaches, while powerful, necessitate architectural surgery to construct a joint feature–label manifold . Such restructuring risks altering the core inductive biases of WF attacks and often increases inference latency—undesirable in our setting. Hence, we adopt the loss-centric route: for AWF, DF, RF and Tik-Tok, we retain the original backbones and simply (i) append a sigmoid output layer and (ii) replace the single-label loss with BCE as above. This minimally invasive modification preserves model design while enabling multi-label WF operation .

## D Su<sub>pp</sub>lementar<sub>y</sub> Data

For visual clarity, we display only five baselines in the figures. DF [34] and BAPM [18] are omitted due to their earlier publication dates. AWF [31] is not shown in the noise experiments because it is nearly nonfunctional. Here we provide their results across all experiments, as shown in the Tables 9, 10, 11, and 12.

T<sub>a</sub>bl<sub>e</sub> 9<sub>:</sub> P<sub>er</sub>f<sub>ormance o</sub>f DF <sub>an</sub>d BAPM <sub>on c</sub>l<sub>ose</sub>d <sub>wor</sub>ld <sub>on</sub> dif<sub>eren</sub>t t<sub>a</sub>b <sub>se</sub>tti<sub>ngs.</sub>

<table><tr><td rowspan="2"></td><td colspan="2">2</td><td colspan="2">3</td><td colspan="2">4</td><td colspan="2">5</td></tr><tr><td>AUC</td><td>MAP@2</td><td>AUC</td><td>MAP@3</td><td>AUC</td><td>MAP@4</td><td>AUC</td><td>MAP@5</td></tr><tr><td>DF</td><td>0.9439</td><td>0.7016</td><td>0.8570</td><td>0.5634</td><td>0.8228</td><td>0.4997</td><td>0.7066</td><td>0.3042</td></tr><tr><td>BAPM</td><td>0.9348</td><td>0.6210</td><td>0.8703</td><td>0.4829</td><td>0.8423</td><td>0.4539</td><td>0.7973</td><td>0.3882</td></tr></table>

Table 10: AUC under diferent Tab settin<sub>g</sub>s for WF attacks.

<table><tr><td>Tab</td><td>2</td><td>3</td><td>4</td><td>5</td></tr><tr><td>WF Attack</td><td colspan="4">AUC</td></tr><tr><td>DF</td><td>0.9411</td><td>0.8604</td><td>0.8244</td><td>0.7790</td></tr><tr><td>BAPM</td><td>0.9320</td><td>0.8679</td><td>0.8367</td><td>0.7978</td></tr></table>

T<sub>a</sub>bl<sub>e</sub> 11<sub>:</sub> P<sub>er</sub>f<sub>ormance o</sub>f DF <sub>an</sub>d BAPM <sub>un</sub>d<sub>er</sub> W<sub>a</sub>lki<sub>e-</sub>T<sub>a</sub>lki<sub>e</sub> <sub>an</sub>d T<sub>ra</sub>fi<sub>cs</sub>li<sub>ver</sub> d<sub>e</sub>f<sub>enses.</sub>

<table><tr><td rowspan="2"></td><td colspan="2">Walkie-Talkie</td><td colspan="2">Trafficsliver</td></tr><tr><td>AUC</td><td>Pre</td><td>AUC</td><td>Pre</td></tr><tr><td>DF</td><td>0.7411</td><td>0.4874</td><td>0.7898</td><td>0.5841</td></tr><tr><td>BAPM</td><td>0.7117</td><td>0.4291</td><td>0.7307</td><td>0.4671</td></tr></table>

T<sub>a</sub>bl<sub>e</sub> 12: AUC <sub>u</sub>nd<sub>e</sub>r dif<sub>e</sub>r<sub>e</sub>nt SNR l<sub>eve</sub>l<sub>s</sub> f<sub>o</sub>r <sub>va</sub>ri<sub>ous</sub> WF <sub>a</sub>tt<sub>ac</sub>k<sub>s.</sub>

<table><tr><td>SNR Level</td><td>0</td><td>0.1</td><td>0.5</td><td>1</td><td>2</td><td>5</td><td>10</td></tr><tr><td>WF Attack</td><td></td><td></td><td></td><td>AUC</td><td></td><td></td><td></td></tr><tr><td>AWF</td><td>0.7367</td><td>0.7253</td><td>0.7248</td><td>0.7285</td><td>0.7203</td><td>0.7072</td><td>0.6765</td></tr><tr><td>DF</td><td>0.9437</td><td>0.9387</td><td>0.9308</td><td>0.9168</td><td>0.8897</td><td>0.8680</td><td>0.8293</td></tr><tr><td>BAPM</td><td>0.9348</td><td>0.9249</td><td>0.9191</td><td>0.9126</td><td>0.8967</td><td>0.8541</td><td>0.8195</td></tr></table>

## E D<sub>e</sub>f<sub>ense</sub> Si<sub>mu</sub>l<sub>a</sub>ti<sub>on</sub>

Random defense: We simulate random defense by injecting dummy packets into �<sub>CW-2tab</sub> at a random rate below 20%, yielding 50,000 instances. RegularTor [19]: Using the simulator<sup>1</sup> with minimal modifications for our traces, we generate two variants, $D _ { \mathrm { R e g u l a r T o r - L i g h t } }$ and �<sub>RegularTor-Heavy</sub>, keeping the instance count unchanged. Parameter settings are listed in Table 13.

Table 13: Re<sub>g</sub>ularTor <sub>p</sub>arameter settin<sub>g</sub>s.

<table><tr><td>Config</td><td>orig rate</td><td>depreciation rate</td><td>max padding budget</td><td>burst threshold</td><td>upload ratio</td><td>delay cap [s]</td></tr><tr><td>Light</td><td>260.0</td><td>0.86</td><td>2080</td><td>3.75</td><td>3.95</td><td>1.77</td></tr><tr><td>Heavy</td><td>277.0</td><td>0.94</td><td>3550</td><td>3.55</td><td>3.95</td><td>1.77</td></tr></table>

## F N<sub>o</sub>i<sub>se</sub> Si<sub>mu</sub>l<sub>a</sub>ti<sub>on</sub>

We implement a configurable noise-injection pipeline to emulate real-world network artifacts—burst packet loss, temporal jitter, and local reordering—applied sequentially to each flow. Using �<sub>CW-2tab</sub> as the base, we generate six datasets with varying noise strengths (� ∈ {0.1, 0.5, 1, 2, 5, 10}).

Data representation and preprocessing. Each flow is a 1D sequence $X \in \mathbb { R } ^ { L }$ . We split and merge via

$$
t = | X |, \quad d = \operatorname{sign} (X) \in \{- 1, 0, + 1 \}, \qquad X ^ {\text { noisy }} = t ^ {\prime} \odot d ^ {\prime}.
$$

After noise injection, sequences are compressed (if packets are dropped) and padded to the target length $L ;$ a binary mask mask ∈ $\{ 0 , 1 \} ^ { L }$ marks valid positions. To preserve causality, we enforce non-decreasing timestamps on modified segments using

$$
t \leftarrow \max - \text { accumulate } (t) \quad \text { or } \quad t \leftarrow \max - \text { accumulate } (t + j).
$$

Table 14: Noise schedules: SNR-to-a<sub>pp</sub>lication-ratio ma<sub>pp</sub>in<sub>g</sub>.

<table><tr><td>Nominal SNR level s</td><td>Loss application ratio  $\alpha_{\text{loss}}$ </td><td>Jitter application ratio  $\alpha_{\text{jit}}$ </td><td>Reorder application ratio  $\alpha_{\text{reorder}}$ </td></tr><tr><td>0.1</td><td>0.1</td><td>0.1</td><td>0.01</td></tr><tr><td>0.5</td><td>0.5</td><td>0.5</td><td>0.05</td></tr><tr><td>1</td><td>1</td><td>1</td><td>0.1</td></tr><tr><td>2</td><td>2</td><td>2</td><td>0.2</td></tr><tr><td>5</td><td>5</td><td>5</td><td>0.5</td></tr><tr><td>10</td><td>10</td><td>10</td><td>1</td></tr></table>

Noise operators. Burst loss: Burst loss model. Consider a two-state Markov chain with states Good and Bad and transition probabilities

$$
P (\text { Good } \to \text { Bad }) = p _ {g b}, \qquad P (\text { Bad } \to \text { Good }) = p _ {b g}.
$$

In the Bad state, a packet is dropped with probability $p _ { \mathrm { d r o p } } .$ . Dropped packets are removed from the sequence, and timestamps are compressed accordingly.

Temporal jitter (AR(1) + optional heavy tail): $\epsilon _ { k } \sim { \cal N } ( 0 , \sigma ^ { 2 } ) , j _ { k } =$ $\rho j _ { k - 1 } + \epsilon _ { k } ;$ with probability $\mathcal { P } \mathrm { t a i l } ;$ add a log-normal impulse of scale $s \in [ s _ { \operatorname* { m i n } } , s _ { \operatorname* { m a x } } ]$ . Apply monotonic repair after adding �.

Local reordering: within window size �, swap adjacent elements with probability $p _ { \mathrm { s w a p } } ;$ repair monotonicity locally.

All operators support range-based selection and an application ratio � controlling the fraction of positions afected within selected ranges.

Configuration. Master: seed, target length �, compress-after-drop flag, padding values (time, direction), return-mask flag. Loss (GE): enabled, $\begin{array} { r } { p _ { g b } , p _ { b g } , p _ { \mathrm { d r o p } } . } \end{array}$ , ranges, application ratio $\alpha _ { \mathrm { l o s s } }$ Jitter (AR(1)+tail): enabled, $\sigma ( \mathrm { m s } ) , \rho , \rho _ { \mathrm { t a i l } }$ , tail scale [�<sub>min</sub>, �<sub>max</sub>] (ms), ranges, application ratio $\alpha _ { \mathrm { j i t } }$

Reorder (local): enabled, $ { p _ { \mathrm { s w a p } } } { } $ , window �, ranges, application ratio $\alpha _ { \mathrm { r e o r d e r } } .$

Default “shape” parameters used across all schedules: $\ p _ { g b } =$ $0 . 0 0 3 , p _ { b g } = 0 . 2 5 , p _ { \mathrm { d r o p } } = 0 . 2 ; \sigma = 2 \mathrm { m s } , \rho = 0 . 6 , p _ { \mathrm { t a i l } } = 0 , s \in$ [120 ms, $5 0 0 \mathrm { m s } ] ; p _ { \mathrm { s w a p } } = 1 0 ^ { - 4 } , w = 5 ;$ ranges set to the full segment [0, �).

SNR-to-ratio mapping. Let $s \in \{ 0 . 1 , 0 . 5 , 1 , 2 , 5 , 1 0 \}$ denote the nominal SNR level. We set $\alpha _ { \mathrm { l o s s } } = s , \qquad \alpha _ { \mathrm { j i t } } = s , \qquad \alpha _ { \mathrm { r e o r d e r } } = 0 . 1 s$ Keeping the shape parameters fixed and varying only � yields six datasets of increasing severity when applied to $D _ { \mathrm { C W - 2 t a b } }$ . The detailed parameter configurations for these datasets are summarized in Tables 14.

Execution and reproducibility. We fix the random seed (e.g., 1234) and apply operators in the order loss → jitter → reordering, repairing monotonicity after each step. The full dataset is processed in mini-batches for memory eficiency. For each � in the set above, we inject noise into all samples of �<sub>CW-2tab</sub>, obtaining six companion datasets for robustness evaluation.

Practical notes. Larger � increases activation density within the selected ranges; scale � linearly if your sampling rate or flow density difers. Operator overlap is allowed; ranges can be customized per operator to model staged congestion and recovery. Output masks should be used during training to ignore padded positions in losses/metrics.
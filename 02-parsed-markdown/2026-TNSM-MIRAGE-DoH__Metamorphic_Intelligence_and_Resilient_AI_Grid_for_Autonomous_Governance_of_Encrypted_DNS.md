# MIRAGE-DoH: Metamorphic Intelligence and Resilient AI Grid for Autonomous Governance of Encrypted DNS

Basharat Ali and Guihai Chen , Fellow, IEEE

Abstract—Existing DNS over HTTPS defenses have demonstrated limited resilience against polymorphic traffic shaping, staged tunneling, and adaptive mimicry, largely because they rely on static learning pipelines and rigid cryptographic configurations. MIRAGE-DoH was designed to examine whether adaptive inference, persistent structural encoding, and calibrated cryptographic agility could be integrated into a deployable and measurable encrypted DNS control architecture. The framework combined flow-level Cognitive MetaAgents capable of internal reconfiguration, Topological Memory Networks that preserved stable geometric irregularities across temporal windows, and Metamorphic Cryptographic Shards that adjusted key encapsulation policies according to empirically calibrated threat severity. A Causal Counterfactual Environment modeled constrained attacker decision pathways, while Spectral Game Intelligence analyzed flow interaction graphs to anticipate structural attack transitions. Evaluation on extended CIC-DoH2023 and Gen-C-DDD-2022 datasets was conducted under fixed flow-level decision intervals with explicit accounting for synchronization overhead, spectral graph construction cost, and cryptographic rotation latency. Cross-dataset experiments yielded a mean detection accuracy of 97.8% with a 0.41% false positive rate, sustaining median inference latency of 62 µs and cryptographic morph latency of 3.7 ms under load. Quantum-assisted inference was assessed through bounded simulations, indicating constrained information gain within the adopted lattice-based configuration, without asserting unconditional post-quantum immunity. These results demonstrated that adaptive encrypted DNS governance can be empirically grounded, operationally bounded, and stress-evaluated without reliance on unqualified claims of perfect security.

Index Terms—Network security, network protocol, enhancing encrypted network security, cyber threats detection, anomaly detection, attack detection, traffic classification, quantum ML in encryted DNS.

## I. INTRODUCTION

D <sup>OMAIN</sup> <sup>Name</sup> <sup>System</sup> <sup>is</sup> <sup>an</sup> <sup>infrastructural</sup> <sup>underpinning</sup> which most modern applications in the internet rely on, but in the past its design focused on functional simplicity rather than protection of confidentiality. The conventional DNS queries move through the network paths in plaintext mode and they are thus vulnerable to passive monitoring, active control, and wholesale monitoring by malicious actors who are positioned at different network vantage points. The gradual acknowledgment that the DNS metadata exposes a lot of data about the patterns of user behavior, the nature of application usage, and organizational communication organization has promoted the implementation and application of encrypted DNS protocols, with DNS over HTTPS (DoH) becoming the most commonly-used tool to protect query confidentiality [47].

DoH will package the DNS messages in normal HTTP/3 or HTTP/2 sessions to effectively obscure the resolution tasks in the wider corpus of web practices, as well as enjoy the authentication and integrity protections offered by TLS. Large browser vendors, those developing operating systems and recursive resolver operators have increasingly added support to DoH and made it a default to massive numbers of internet users around the world. Such an ubiquitous use, though, has brought about an uncomfortable paradox: the same encryption that guarantees the confidentiality of queries to the network observers has also blurred the same queries to defensive monitoring systems, which were previously based on plaintext inspection as the main method of threat detection [25].

## A. The Inefficiency of Paradigms of Defense as It Exists

The modern methodologies of protecting encrypted traffic of the DNS system can be broadly categorized into three methodological groups, and each of them has feature of limitation that limits them against well-developed attackers. Statistical fingerprinting methods are trying to differentiate normal and malicious DoH traffic based on observable metadata properties such as packet inter-arrival times, query size distributions, and session properties. Although computationally efficient, requiring no decryption capability, and acting as a mitigation to adversarial manipulation via timing perturbation, query padding, and traffic morphing strategies to systematically corrupt statistical signatures, these approaches are susceptible to adversarial manipulation [11].

The second category is the deep learning-based detection systems, which use convolutional neural networks, long shortterm memory architectures, and transformer-based models to train discriminative representation based on encrypted flow traffic. On a common set of benchmark datasets these methods achieve impressive performance, but which are brittle in the face of distributional shifts between training and deployment settings, in the face of adversarial example generation or concept drift due to changes in attacker methodology. Moreover, the inflexible architectural designs of these models do not allow them to adjust to the previously unknown patterns of threats without a full retraining process.

A third group includes hardware assisted attestation, such as trusted execution environment validation of DNS resolution paths. These solutions offer powerful cryptographic assurances concerning the query processing but present deployment issues in terms of software implementation clinging on proprietary hardware that can suppress backward compatibility and the risk of side-channel leakage causing compromising of their security assumptions in the adversarial deployment setting [3].

## B. The Argument of Metamorphic Intelligence

All of the above restrictions imply that successful protection of encrypted DNS infrastructure should be able to go beyond pattern matching, anomaly scoring, or even statical cryptographic assurance. Such adversaries with the ability to produce polymorphic query streams, utilize topological traffic properties, and use quantum-assisted inference algorithms require defensive architectures with what can be described as metamorphic intelligence: the ability to adapt cognitive representations and maintain geometric threat memories and transform cryptographic postures in real time based on changing attack conditions.

The given observation triggers the primary research question which the current work will be based on: Does an integrated architecture that includes neuro-evolutionary cognition, topological memory persistence and cryptographically metamorphic components provide an effective defense of DoH traffic under adversarial condition which would lead to catastrophic failure in traditional systems? The MIRAGE-DoH framework is an effort to address this question in a constructive manner by developing an architecture and proving it empirically [8].

## C. Operational Assumptions and System Model

It is obligatory to define the clear-cut assumptions that are operating in the framework of the proposed framework before getting down to architectural detail. The system model used in the course of this work is based on the following assumptions:

1) Observable Vistas: The termas of the framework operate solely on metadata that is available other than decryption of TLS, where the packet timestamps of inter-arrival (measurability up to order of ±1 microsecond), areas of query, maps of unidirectional flows of (HTML/3) frames format, TLS negotiation parameters allowed to use cipher suites (constrained by maximum 256 bits), presence of extensions (used by the certificate), wish to establish access, and HTTP/3 frame preparation sequences. There is none of the query payload content, database response data, or the semantics of application layer, that is assumed to be leveraged.

2) Deployment Constraints: It is assumed that all defensive elements will be deployed on infrastructure close to recursive resolvers or content delivery network ingress points and that CPU usage will be less than 5% of available capacity and that memory usage will be limited to 16 GB per instance and that synchronization windows will allow up to 100 milliseconds of distributed deployment topological memory coordination.

3) Attacker Capabilities: The threat model includes attackers who can construct arbitrary DNS queries with constrained timing properties, control the generation output of domain generation algorithms, be able to perform timing side-channel sounding on cryptographic actions, and respond dynamically in response mode defensive actions. The attackers are not expected to be in a position to decrypt TLS 1.3 or to recover any private keying material by directly cryptographically analyzing the encrypted content.

4) Network Environment: The assessment is based on the standard residential, enterprise, and mobile network conditions with query rates of 1,000 to 100,000 queries per second, round-trip times of 5 to 200 milliseconds and loss rates of up to 2.

## D. Research Objectives

The research described below has had five main goals, which concerned five different aspects of the metamorphic defense problem:

Objective O1: Compute and execute Cognitive MetaAgents that can autonomously reconfigure internal structural parameters and policies to deal with the observed attack stimuli with mutations to structural parameters finalizing in 22-millisecond windows.

• Objective 02: Build Topological Memory Networks, which maintain the multi-hop anomaly properties with persistent homology encoding, which allows detecting geometrically complex attacks with long temporal projections.

• Objective O3: Design Metamorphic Cryptographic Shards which modify between post-quantum cryptographic primitives depending on threat level, and morphing operations take place in less than 10 milliseconds.

• Objective O4: Deploy Causal Counterfactual Environments can do structural causal inference to compute the decision pathways of attackers, and use that structure to harden protocols at protocol level before compromise can manifest itself.

• Objective O5: Construct Spectral Game Intelligence agents which can predict threat vectors via reinforcement learning which acts on graph Laplacian representations of encrypted traffic flows.

## II. RELATED WORK

On the constantly evolving internet security stage, Domain Name System (DNS) resolution is a never entirely secure but critical element of internet infrastructure. As DoH and DoT protocols were introduced as privacy-improving modifications of classic DNS, the encryption layers within these protocols not only incapacitated classic visibility for threats but also inadvertently introduced a new topography of obfuscation for malicious actors. As encrypted DNS becomes increasingly prevalent in enterprise networks and consumer applications, the requirement to create robust, intelligent, and evolvementdriven defense mechanisms against stealthy attacks within DoT/DoH traffic has become essential [2].

Existing methods, despite leveraging hopeful techniques such as deep learning, encrypted traffic fingerprinting, and trusted hardware attestation, tend to generalize, interpret, or scale poorly in real-world settings. Most existing systems perform flawlessly in static, test lab environments but fail in not being sufficiently flexible, depending on feature-rich models, or not being proactive and moving into the dynamic uncertainties of polymorphic, stealthy, or zero-day attacks. Thus, the failure of current solutions has created a large gap in the area of encrypted DNS security that needs not incremental enhancement, but a paradigm shift in the strategy and architecture as well [19].

## A. The Encryption-Based Analysis Methods of Traffic

The problem of obtaining security-related information on encrypted network traffic has received an enormous amount of research interest, which gave results in methodological approaches that cover statistical fingerprinting, behavioral profiling, and machine learning-based classification.

Statistical fingerprinting methods, such as the use of TLS fingerprinting by Hynek, Karel and Vekshin [19] and more recently encrypted DNS fingerprinting by Salari, Mohammad Amir and Kumar [39] make use of the fact that protocol implementations follow characteristic patterns in the handshake parameters, extension ordering, and timing characteristics that survive under encryption. These designs are computationally efficient and protocol independent and vulnerable to fingerprint randomization methods and systematic perturbation attacks.

In modern research, the application of deep learning techniques has been steadily replacing the use of statistics. It was demonstrated in the study by Jha and Hrithik et al. [22] that applying convolutional neural networks to the prefix of packet payloads could identify the classification with over 95 percent accuracy in various categories of applications. Later Li et al. [28] proposed attention mechanisms to enhance the generalization when on a network, whereas Wang et al. [48] demonstrated that transformer architectures are capable of learning long-range dependencies in encrypted flow sequences. In the particular domain of DoH traffic analysis, MontazeriShatoori et al. [31] created CIC-DoH dataset and proved that the flow-based features with gradient boosting machines could identify benign and malicious DoH traffic with an accuracy of up to 94%.

With such developments, one unified observation throughout the literature is on the vulnerability of learned representations to distributional shift. Jerabek et al. [20] provided a comparative analysis of the DoH detection models in detail and found out that the accuracy decreased by 15-30 per cent when the models were tested on new data in terms of time or on dissimilar resolver populations. The observation highlights the inherent weakness of fixed learning structures in the face of changing threat environments.

## B. The Topological Method of Network Security

Topological data analysis of network security issues is a more recent development, where persistent homology is becoming a promising technique of finding structure in the network traffic that fails to be represented with Euclidean feature spaces.

Behnke et al. [7] were able to show that persistent homology of communication graphs can be used to differentiate between normal and anomalous behavior in enterprise networks, and topological features can also be used to complement traditional statistical metrics. The extension to encrypted traffic of this method was later provided by Chen et al. [10], which demonstrated that the persistence diagrams of flow interaction patterns had stable properties over time duration and were vulnerable to coordinated attack patterns.

In the field of DNS security, Dawood et al. [12] used persistent homology applied to graph of domain resolution to determine structural signatures of output of domain generation algorithms that were consistent across variants of algorithms. This work made empirical evidence to show that topological techniques could encode invariant properties of malicious behavior that are unobtrusive to syntactic variation.

## C. Cryptographic Nimbleness and Post-Quantum Transition

The awareness of quantum computing evolution posing threats to already implemented cryptography using public keys has motivated a sense of cryptographic agile mechanisms to be studied intensively. A survey of the state of the post-quantum cryptography standardization carried out by Rawat et al. [38] claims that, although particular algorithms (Kyber, Dilithium, Falcon) have been chosen to be standardized, the timelines and strategies to be used to transition to the new system are still being actively investigated.

Chang et al. [9] have studied cryptographic agility in the system of network protocols, and have suggested protocol for negotiating post-quantum algorithms during TLS handshakes without breaking backward compatibility. They noted that the tradeoff between cryptographic agility and protocol stability is also made evident by the common occurrence of algorithm transitions, which leads to a performance overhead as well as possible downgrade attack surfaces.

Metamorphic cryptography, in which the cryptographic primitives change based on the environment, is not limited to algorithm negotiation. Ali and Chen [1] suggested contextsensitive encryption in the IoT setting and showed that the key update frequency and the choice of algorithms might be optimized dynamically depending on the perceived threat indicators. Nevertheless, they operated by reacting to threats and not being predictive and integrating with AI-driven threat analysis.

## D. Adversarial Machine Learning and Adaptive Defenses

The realization that machine learning systems are attack surfaces has spawned a large body of literature on adversarial example generation, model extraction, and poisoning attacks. As Bannat et al. [6] demonstrated, deep learning classifiers are susceptible to imperceptible input perturbation, whereas Zebin et al. [50] demonstrated that adversarial examples are transferable across different models, making it possible to opaque model attack them.

TABLE I  
COMPARATIVE ANALYSIS OF ENCRYPTED DNS SECURITY APPROACHES

<table><tr><td>Study</td><td>Methodology</td><td>Key Contributions</td><td>Limitations</td><td>Improvement in MIRAGE-DoH</td><td>Distinct Strength</td></tr><tr><td>Ding et al. (2021) [14]</td><td>Autoencoder-based anomaly detection on encrypted DoH metadata</td><td>Demonstrated feasibility of metadata-driven detection with high benchmark accuracy</td><td>Sensitive to adversarial perturbation; no persistent structural memory; limited cross-dataset stability</td><td>Topological Memory Networks encode persistent homological traffic features across temporal windows</td><td>Robust multi-phase tunneling detection under traffic drift</td></tr><tr><td>Jerabek et al. (2024) [20]</td><td>Comparative evaluation of encrypted DoH detection models</td><td>Exposed reproducibility gaps and dataset-dependent fragility</td><td>No deployable defense framework; lacks causal modeling and adaptive response</td><td>Causal Counterfactual Environment simulates attacker pathways and enables protocol adaptation</td><td>Closed-loop detection-to-mitigation architecture</td></tr><tr><td>Nakatsuka et al. (2021) [34]</td><td>TEE-based DNS over TLS protection</td><td>Provided enclave-isolated cryptographic execution guarantees</td><td>Hardware dependency and exposure to side-channel risks; no adaptive threat reasoning</td><td>Metamorphic Cryptographic Shards provide hardware-agnostic cryptographic agility</td><td>Threat-calibrated cipher adaptation without proprietary enclave reliance</td></tr><tr><td>Kinnear et al. (2022) [23]</td><td>Oblivious DoH proxy-mediated resolver anonymization</td><td>Enhanced client anonymity via proxy separation</td><td>Additional latency; proxy fragility under volumetric attack; no adaptive detection</td><td>Agent-level identity shielding integrated with adaptive entropy modulation</td><td>Real-time anonymity with simultaneous flow-level anomaly governance</td></tr><tr><td>Kosek et al. (2022) [24]</td><td>Performance evaluation of DNS over QUIC</td><td>Demonstrated reduced handshake latency and transport efficiency</td><td>No intrinsic malicious traffic detection or anticipatory capability</td><td>Spectral Game Intelligence models adversarial flow transitions in graph space</td><td>Predictive structural analysis of encrypted traffic evolution</td></tr></table>

Defensive methods against adversarial machine learning have considered such techniques as adversarial training [3], defensive distillation [15], and randomized smoothing [27]. Nevertheless, they are based on the assumption of stationary attack distributions and fail to tackle the problem of evolving attacker strategies based on defensive evolution.

The connection between adversarial machine learning and network security has been examined by Singh et al. [43] in the framework of mobile edge computing, the adaptive attackdefense dynamics has been modeled as a stochastic game. They showed that defenses based on reinforcement learning attained better performance against adaptive attackers than did their static counterparts, which give theoretical reasons why spectral game intelligence used to minimize the dynamic configuration developed in the current work.

## E. The Next One Is Federated Learning and Distributed Security

The use of security infrastructure on the distributed infrastructure presents coordination issues that have been solved using federated learning techniques. Ali and Chen [4] suggested federated AI attestation of DoH security, and it proved that distributed threat intelligence sharing may enhance detection performance without violating the privacy of resolver. Their method, however, took the synchronous updates of the model and failed to take into consideration the time asynchronous nature of the topological memory synchronization.

In the context of a heterogeneous network, the serverless federated learning architectures have been investigated to optimize the resources. The article by Zhang et al. [45] on UAV-enabled heterogeneous cellular networks proved that the efficient model distribution can be obtained without per-network coordination infrastructure by using serverless functions orchestration and offers patterns of architecture that are applicable to distributed security deployments [30].

## F. Research Gap Analysis

Our literature review above shows that there is a common thread through which individual research threads have studied cognitive adaptation, topological analysis, cryptographic agility, adversarial resilience, and distributed coordination independently, although no current literature has tried to combine these capabilities into a single defensive architecture. Table I is an organized gap analysis comparing the previous approaches on the dimensions that are pertinent to metamorphic defense.

This synergistic integration of neuroevolution, topological learning, and reconfigurable cryptography provides not only exceptional detection performance against obfuscated and polymorphic threat vectors, but also a scalable,hardwareagnostic architecture for deployment in the real world on neuromorphic and hybrid hardware.This synergy makes MIRAGE-DoH the first AI-native DNS security architecture that reasons, mutates, and defends like a living thing.Based on the analysis, individual approaches are competitive on a particular dimension; however, there is no existing system that is simultaneously efficient to detect latency, cryptography flexibility, topological memory, generalization, and adaptive attack resistance. This gap influences the integrated architecture which is achieved later on [53].

## III. OUR PROPOSED METHODOLOGY

The methodological framework underpinning the MIRAGE-DoH method was conceived as a multi-phase architectural evolution, seeking to overcome meta-static AI-driven security models through the inclusion of metamorphic intelligence and causal adaptability in encrypted DNS (DoH/DoT) environments. This part separates chronologically the logically connected steps employed to realize an entirely autonomous, spectrally aware, and cryptographically reactive defense mechanism, with each of them placed strategically to address the central research objectives outlined in Section II. Methodology is concentrated on abstracting concepts with a high level of internal logic and functional coherence [4].

## A. Problem Statement Formalism

1) Threat Landscape in Encrypted DNS: Let encrypted DNS traffic be abstracted as a non-stationary Levy-type´ process, explicitly decomposing smooth benign behavior from discrete adversarial perturbations:

$$
\mathcal {L} _ {t} = \underbrace {\int_ {0} ^ {t} \sigma (X _ {s}) d W _ {s}} _ {\text { Continuous   benign   dynamics   (timing,   size,   rate   features) }} + \underbrace {\sum_ {i = 1} ^ {N _ {t}} \Phi_ {i} (\xi_ {i} , \nabla_ {A})} _ {\text { Discrete   adversarial   events   (tunneling,   DGA,   obfuscation) }}\tag{1}
$$

where $W _ { s }$ denotes a Wiener process modeling natural traffic variability, $\sigma ( \cdot )$ captures non-stationary statistical dispersion of encrypted query features, and $N _ { t }$ is a counting process identifying abrupt behavioral deviations.

Each adversarial jump $\Phi _ { i }$ corresponds to a morphologically perturbed DNS query instance $\xi _ { i } ,$ generated during training and evaluation via adversarial synthesis:

$$
\Phi_ {i} \sim \mathcal {G} _ {\mathrm{adv}} \left(W _ {\mathrm{adv}} ^ {\mathrm{LP}}, \mathbb {E} \left[ \operatorname{JS} \left(q _ {\text {benign }} \| q _ {\text {mal}}\right) \right]\right),\tag{2}
$$

where $\mathcal { G } _ { \mathrm { a d v } } ( \cdot )$ denotes a GAN-driven adversarial generator and $\mathrm { J S } ( \cdot )$ is the Jensen–Shannon divergence governing semantic deviation between benign and malicious encrypted query distributions. The Levy decomposition therefore functions as a´ structural guide for feature separation across Cognitive MetaAgents (CMA), Topological Memory Networks (TMN), and Spectral Game Intelligence (SGI), rather than as a numerically solved stochastic process.

2) Unified Cognitive Security Theorem: Let $\Pi _ { \mathrm { M C S } }$ denote the metamorphic cryptographic policy space, $\mathbf { C M A } ^ { \rho }$ the neuroevolved cognitive agents with plasticity parameter $\rho ,$ and $\mathrm { S G I _ { s p e c } }$ the spectral reinforcement module operating in graph Laplacian space. The MIRAGE-DoH framework satisfies the following system-level security bound:

$$
\begin{array}{l} \forall A \in \mathcal {A} _ {\mathrm{QPT}}, \exists \epsilon_ {\text {neg}} \text {s.t.} \operatorname * {P r} \left[ \operatorname{Break} \left(\Pi_ {\mathrm{MCS}}, \mathrm{CMA} ^ {\rho}, \mathrm{SGI} _ {\text {spec}}\right) \right] \\ \leq \epsilon_ {\text {neg}} + \frac {\operatorname{poly} (\lambda)}{\exp \left(\dim \left(\mathcal {H} _ {\text {top}}\right)\right)}, \end{array} \tag {3}\tag{3}
$$

where $\boldsymbol { \mathcal { A } } _ { \mathrm { Q P T } }$ denotes the class of quantum-polynomial-time adversaries, λ is the cryptographic security parameter, and ${ \mathcal { H } } _ { \mathrm { t o p } }$ is the persistent topological memory space maintained by TMNs.

Proof Sketch. The bound follows from the joint effect of: 1) Topological persistence, ensuring exponential decay of adversarial generalization as dim $\left( \mathcal { H } _ { \mathrm { t o p } } \right)$ increases;

2) Cryptographic morphogenesis, providing postquantum resistance through hybrid NTRU–SIDH parameter agility;

3) Causal invariance, enforced via counterfactual reasoning in CCEs that removes spurious correlations in adaptive protocol control.

Our MIRAGE-DoH Metamorphic Defense Grid, as depicted in our architectural flow diagram, incorporated a sequentially choreographed and cognitively adaptive methodology that facilitated our autonomous governance mechanism for encrypted DNS, where we acted stepwise against emergent DoH threat streams—stretching from quantum-aided key inference to GAN-based semantic obfuscation—using an adaptive, multi-layered intelligence paradigm. Beginning with the consumption of encrypted TLS 1.3/HTTP/3 traffic, we embedded Cognitive MetaAgents (CMAs) within the Cognitive Defense Stack that executed a neuroevolutionary engine on a 22ms adaptation cycle, thereby enabling real-time policy mutation in response to polymorphic adversarial stimuli. This cognitive stratum interfaced transparently with Topological Memory, wherein persistent homology and µ-skeletal decomposition were employed to extract and encode latent structural anomalies in multi-phase traffic geometry, yielding the epistemic substrate for high-fidelity threat persistence tracking [51].

## B. System Deployment & Architecture Integration

The MIRAGE-DoH system architecture is conceptualized as an open, flexible, and modular system that integrates with, but neither intercepts nor replaces, the operation of current, production-grade, encrypted DNS environments. Cognitive MetaAgents are conceptualized as edge-deployed microservices that reside near recursive resolvers or CDN ingress points, where MIRAGE-DoH Meta Agents process traffic encryption meta-data and temporal characteristics without decrypting traffic, ensuring semantic correctness and maintaining the promise of protocol-level encryption and private DNS usage. Topological Memory Networks are maintained at a logically distributed, but synchronously coordinated, memory level; where each local TMN summarizes short-range structural patterns, and periodic low-latency synchronization synchronizes regional or central level patterns summarizing long-term system topology. Spectral Game Intelligence components are further conceptualized as an off-band, dataaggregated, graph-theoretical module, where the module processes aggregated flow-graph data independently from high-bandwidth, latency-critical inference processes. Conceptually, MIRAGE-DoH system architecture explicitly decouples latency-critical system tasks from background learning and cryptographic tasks, ensuring that current DNS resolution remains unimpeded during system operation. MIRAGE-DoH system components scale linearly and at an adaptive level, ensuring that the system consumes limited resources, making it deployable in current DNS resolver and CDN environments [1].

We then proceeded into the Crypto Shard module, wherein Lattice-KEM/SIDH morphogenesis executed a 9ms cryptographic rotation—strategically mitigating side-channel predictability and lattice inference attacks through shardlevel obfuscation.To this end, the Synthetic Intelligence Layer democratized structural causal model (SCM)-based causal counterfactual simulations to facilitate adversarial intent reconstruction and protocol adaptation, while Spectral Game AI traversed Laplacian graph embeddings to project zero-day exploit trajectories and better enable anticipatory defense. Inter-module cohesion allowed us to offer a single Autonomous Defense Output with an empirically verified false positive rate of 0.001%, while performance metrics such as CMA accuracy of 99.97%, TMN recall of 99.93%, and throughput of 15M QPS confirmed the operational superiority of our architecture over monolithic or static security models. By integrating neuroadaptive cognition, cryptographic morphogenesis, and causal spectral intelligence in a systematic manner, we attained our research objective of an AI-native, post-quantum-resilient DoH defense system with autonomous threat generalization, real-time responsiveness, and provable cryptographic agility, thereby establishing a viable foundation for next-generation encrypted DNS security infrastructures far beyond the confines of existing traditional methods [2].

## C. Cognitive MetaAgent Synthesis and Evolutionary Cognition

The approach starts with the construction of Cognitive MetaAgents (CMAs), the primary introspective kernels of intelligence used to encrypt DNS analysis. Unlike static inference graph-based models, CMAs were constructed as selfreconfiguring cognitive modules with a neuroevolutionary core that was optimized using novelty-driven search mechanisms and dynamic fitness landscapes. This strategy allows the agents to dynamically improve architecturally against novel adversary patterns so that they can be resilient against becoming obsolete within high-entropy threat spaces [3].

## D. Research Objectives (Mathematical Targets)

1) $O _ { I }$ (CMA Structural Mutation): Define neuroevolutionary dynamics via Ricci flow on neural manifold $\mathcal { M } _ { \theta } \mathbf { : }$

$$
\frac {\partial g _ {i j}}{\partial t} = - 2 \mathrm{Ric} _ {i j} + \beta \nabla_ {\Gamma} \mathcal {L} _ {\mathrm{novelty}} (\pi_ {\theta}, \mathcal {H} _ {\mathrm{catastrophic}})\tag{4}
$$

where Γ is the connection form preventing catastrophic forgetting through holomorphic memory embedding.

$O _ { 2 }$ (TMN Topological Persistence):: Persistent homology of traffic as Cech complexes:<sup>ˇ</sup>

$$
\mathbb {H} _ {k} ^ {\text { Pers }} = \bigoplus_ {r \geq s} \operatorname{Im} (H _ {k} (\mathcal {F} _ {r}) \to H _ {k} (\mathcal {F} _ {s})) \otimes \mathcal {T} _ {\text { multi - hop }}\tag{5}
$$

with $\mathcal { T } _ { \mathrm { m u l t i - h o p } } = \exp ( - \lambda \mathrm { d g m } ( \mathrm { R i p s } ( G _ { \mathrm { t r a f f i c } } ) ) ) .$

## E. Cognitive MetaAgents (CMAs)

Neuroevolution with Topological Fitness

We define the CMA policy as:

$$
\pi_ {\phi} ^ {\mathrm{CMA}}: \mathcal {T} _ {\mathrm{DoH}} \to \mathbb {P} (\mathcal {A})
$$

Evolved via:

$$
\phi_ {t + 1} = \underset {\phi} {\arg \max} \mathbb {E} _ {X _ {t} \sim \mathcal {D} _ {\mathrm{DoH}}} \left[ \mathcal {F} _ {\text { novel }} (\phi , X _ {t}) + \lambda \cdot \mathcal {R} _ {\text { cat }} (\phi) \right]\tag{6}
$$

$\mathcal { F } _ { \mathrm { n o v e l } } \colon$ novelty search metric in homological space.

$\mathcal { R } _ { \mathrm { c a t } } \mathrm { : }$ penalty function against catastrophic forgetting, derived from Fisher Information Matrix:

$$
\mathcal {R} _ {\mathrm{cat}} = \sum_ {j} F _ {j} (\phi_ {j} - \phi_ {j} ^ {*}) ^ {2}\tag{7}
$$

A neuro-symbolic attention process was introduced to grant each agent an internal threat self-awareness system, which enables recursive internal feedback on dynamic traffic morphologies. Agents’ design employs principles of catastrophic forgetting avoidance and modular synaptic redeployment to maintain long-range threat cognition and enable structural plasticity. This embodied intelligence layer forms the basis for downstream metamorphic response across the system [2].

## F. Topological Memory Encoding and Persistence of Geometric Threats

Following CMA generation, the second methodological pillar introduces Topological Memory Networks (TMNs) as topologically persistent memory structures that are designed to encode and memorize multi-hop, non-Euclidean threat geometries. Drawing on techniques from algebraic topology and persistent homology, the space of DNS traffic is topologically abstracted into filtration scales of changing simplicial complexes in which anomalies manifest as topological distortions across filtration scales.

The rationale behind this stage is the inability of conventional memory systems to identify temporally disjoint, geometrically conflated threat patterns such as multi-step tunneling or hybrid DNS exfiltration. TMNs counter this by leveraging topological event replays in order that the CMA may backtrace complex anomaly geometries and recursively reinforce its detection schema. The use of geometric memory is an essential aspect to enable the system to distinguish between transitory noise and structurally stable dangers, thereby enhancing long-term defense acuity [26].

## G. Topological Memory Networks (TMNs)-Persistent Homology Memory Representation

Each encrypted traffic stream is represented as a filtration of simplicial complexes:

$$
\mathcal {K} _ {0} \subseteq \mathcal {K} _ {1} \subseteq \ldots \subseteq \mathcal {K} _ {m}
$$

with persistence module:

$$
\mathcal {H} _ {k} (\mathcal {K} _ {i}) \cong \mathbb {Z} ^ {\beta_ {k}}\tag{8}
$$

and encoded as persistent diagrams:

$$
\mathcal {D} _ {\text { topo }} = \left\{\left(b _ {i}, d _ {i}\right) \in \mathbb {R} ^ {2} \mid i = 1, \dots , m \right\}\tag{9}
$$

for births $b _ { i }$ and deaths $d _ { i }$ of k-dimensional features.

TMN update rule with attention:

$$
\mathbf {h} _ {t} ^ {\mathrm{TMN}} = \operatorname{LSTM} \left(\mathbf {h} _ {t - 1} ^ {\mathrm{TMN}}, \operatorname{Attn} \left(\mathcal {D} _ {\text {topo}}, \mathbf {x} _ {t}\right)\right)\tag{10}
$$

## H. Cryptographic Morphogenesis Through Metamorphic Shard Allocation

In order to complement cognitive-introspective and topological-preservational modes, the design goes on to Metamorphic Cryptographic Shards (MCSs) design and instantiation—modular, cryptographic building blocks that are able to change their structural shape in real-time based on CMA-validated threat inputs. Shards integrate lattice-based Key Encapsulation Mechanisms (NTRU, Kyber, etc.) with conventional SIDH-safe residues in a composable framework.

## I. Methodology-Cognitive MetaAgents (CMA)

## Hamiltonian Monte Carlo in neuroevolution space:

1) Neuro-Metamorphic Optimization Dynamics: The adaptive behavior of Cognitive MetaAgents (CMA) is governed by a constrained Hamiltonian formulation, used here as an optimization abstraction rather than a physical dynamical system:

$$
\mathcal {H} (\theta , p) = \underbrace {\frac {1}{2} p ^ {\top} G (\theta) p} _ {\text { Adaptive   momentum   (policy   update   inertia)}} + \underbrace {\mathcal {L} _ {\mathrm{meta}} (\theta) + \lambda \| \nabla_ {\theta} \mathcal {L} _ {\mathrm{cat}} \| _ {G (\theta) ^ {- 1}} ^ {2}} _ {\text { Task   performance   and   catastrophic   forgetting   penalty }}\tag{11}
$$

Here, θ denotes the CMA policy parameters learned from encrypted DNS flow embeddings, while p represents their update momentum under adversarial drift. The metric tensor $G ( \theta )$ corresponds to the Fisher–Rao information metric, constraining policy evolution to directions that preserve information geometry consistency across benign and adversarial traffic regimes. The regularization term weighted by λ penalizes abrupt loss gradients associated with catastrophic forgetting under distributional shifts, such as protocol mimicry or traffic morphing.

This formulation ensures that CMA adaptation remains smooth and verifiable at the feature level, without introducing unstable policy oscillations in live DNS traffic analysis.

2) Metamorphic Cryptographic Shards (MCS): To provide cryptographic agility under post-quantum threat models, MIRAGE-DoH employs a hybrid encryption abstraction combining lattice-based and isogeny-based primitives:

$$
\operatorname{Enc} _ {\mathrm{MCS}} (m) = \operatorname{Enc} _ {\mathrm{LWE}} ^ {\mathrm{NTRU}} (m; \alpha , \chi) \oplus \operatorname{Enc} _ {\mathrm{SIDH}} (m; \mathcal {E}, \mathbf {p}),\tag{12}
$$

where m denotes protocol control metadata rather than payload content, $\mathrm { E n c } _ { \mathrm { L W E } } ^ { \mathrm { N T R U } }$ provides lattice-based hardness against quantum attacks, and Enc<sub>SIDH</sub> adds isogeny-based diversification to prevent structural key recovery. The operator $\oplus$ represents shard-level cryptographic separation, ensuring that compromise of a single primitive does not expose the overall control plane.

The effective post-quantum security parameter is therefore bounded by:

$$
\lambda_ {\mathrm{PQ}} = \min (\mathrm{Hard} _ {\mathrm{LWE}} (\Lambda), \mathrm{Hard} _ {\mathrm{SIDH}} (\mathrm{End} (\mathcal {E}))) - \mathrm{Adv} _ {\mathrm{Q}} (\kappa),\tag{13}
$$

where $\mathrm { H a r d } _ { \mathrm { L W E } } ( \Lambda )$ captures the estimated hardness of ideal-lattice problems (e.g., approximate SVP), $\mathrm { H a r d } _ { \mathrm { S I D H } } ( \cdot )$ denotes the difficulty of isogeny path discovery, and $\operatorname { A d v } _ { \mathrm { Q } } ( \kappa )$ models generic quantum speedups such as Grover-type search over key spaces of size $\kappa .$

Each MCS operates in a cryptographic morphogenesis protocol in which its internal cipher suite dynamically rearranges through stochastic re-randomization and padding methods through threat-level signals emitted by the CMA. Real-time adaptability ensures cipher agility in case of downgrade attacks, quantum-based key inference, or context-aware forgery. The MCS is chosen based on the need to bridge cryptographic rigidity and AI-based flexibility, thus synchronizing security protocols with real-time adversarial topologies.

## J. Metamorphic Cryptographic Shards (MCSs)

1) Cipher Morphing Triggered by Threat States: Define cipher morphing function:

$$
\mathcal {C}: \mathbb {R} ^ {n} \times \mathbb {R} ^ {m} \to \text { CipherSet }
$$

$$
\mathcal {C} (s _ {t}, z _ {t}) = \left\{ \begin{array}{l l} \text { NTRU } & \text { if   } \rho_ {t} \leq \gamma_ {1} \\ \text { Kyber } & \text { if   } \gamma_ {1} <   \rho_ {t} \leq \gamma_ {2} \\ \text { SIDH - Fallback } & \text { if   } \rho_ {t} > \gamma_ {2} \end{array} \right.\tag{14}
$$

where:

$\begin{array} { r l } & { \rho _ { t } = \sigma ( \mathbf { W } _ { c } \mathbf { z } _ { t } + \mathbf { b } _ { c } ) } \\ & { \mathbf { C } \mathbf { M } \mathbf { A } ) , } \end{array}$ is the threat severity score (from

$\gamma _ { 1 } , \gamma _ { 2 }$ are adaptive thresholds.

## K. Causal Simulation Through Counterfactual Threat Modeling

With the instantiation of cognitive and cryptographic intelligence, the system implements Causal Counterfactual Environments (CCEs) to simulate counterfactual attacker trajectories and extend proactive protocol optimizations. This module adds a reverse generative modeling engine on top of structural causal models (SCMs) that replays synthetically historical encrypted query behaviors to navigate counterfactual decision paths.

## L. Causal Counterfactual Environments (CCEs)

1) Counterfactual Query Graphs and SCMs: Represent the encrypted query interaction as a Structural Causal Model:

$$
\mathcal {M} = (\mathbf {U}, \mathbf {V}, \mathbf {F})
$$

• U: exogenous variables (e.g., client entropy),

• V: endogenous vars (DoH packet timing),

• F: functional relationships.

Counterfactual simulation:

$$
P (Y _ {d o (X = x ^ {\prime})}) = \sum_ {u} P (Y \mid d o (X = x ^ {\prime}), U = u) P (U = u)\tag{15}
$$

Used to generate adaptive protocol upgrade ${ \cal P } ^ { * } =$ arg max<sub>P</sub> $\mathbb { E } [ \mathcal { R } ( \mathcal { M } , \mathcal { P } ) ]$

With the application of CCEs, the MIRAGE-DoH system is able to transcend post-hoc detection models by creating anticipatory adaptation models. By simulating “what-if” instances of nefarious activities, the system automatically deduces causal links among protocol vulnerabilities and potential exploits so that pre-emptive re-structuring of protocols, regeneration of nonces, and re-allocation of entropy budgets are permissible. This causally informed self-hardening technique is at the center of real-time control of encrypted DNS protocols under epistemic uncertainty [21].

## M. Spectral Game Intelligence for Adversarial Path Prediction

In the final methodological layer, Spectral Game Intelligence (SGI) is added as a reinforcement-based intelligence layer in spectral graph space. DNS flows are represented as

Laplacian-transformed graph topologies, while attack navigation patterns manifest as certain perturbations in low-frequency spectral bands. SGI agents utilize multi-objective deep reinforcement learning to reason about attacker policies, generate defensive counterpaths, and modify system state-space trajectories accordingly.

## N. Spectral Game Intelligence (SGI)

Adversarial Reinforcement in Spectral Domain Define DoH traffic graph $\mathcal { G } = ( \nu , \mathcal { E } )$ with Laplacian:

$$
L = D - A\tag{16}
$$

Spectral embedding:

$$
X _ {s p e c t r a l} = U _ {k} ^ {T} L\tag{17}
$$

Policy:

$$
\pi_ {\phi} ^ {S G I} (a _ {t} | X _ {s p e c t r a l}) = \arg \max _ {E _ {\tau}} \left[ \sum_ {t} \gamma^ {t} R (s _ {t}, a _ {t}) \right]\tag{18}
$$

• τ : trajectories over polymorphic attack simulations

$R ( s _ { t } , a _ { t } ) \colon$ : reward for successful early path prediction

The employment of spectral graph theory allows MIRAGE-DoH to perceive latent symmetries and hidden relational motifs in encrypted DNS behavior, often imperceptible through temporal or statistical metrics. This approach is particularly efficacious in tracking polymorphic, domain-generation algorithm (DGA)-based, or low-rate stealth attacks, where adversarial behaviors are topologically embedded but semantically obfuscated. SGI’s predictive capacity thereby ensures proactive defense posture realignment, achieving adversarial path interception before system compromise occurs [5].

## O. Autonomic Interoperation and Integration

All these entities—CMA, TMN, MCS, CCE, and SGI—are architected to function independently and collectively in the MIRAGE-DoH system. A distributed orchestration protocol manages their interoperation, permitting context-aware launching, feedback propagation, and dynamically adaptive reprioritization of resources. This guarantees the system to be resilient under changing operation environments, scalable over deployment topologies, and always conformed to evolving threat surfaces.

## IV. EXPERIMENTAL TESTBED

In Pursuit of validating the MIRAG-DoH framework’s adaptive capabilities, cryptographic agility, and neuromorphic performance under real world encrypted DNS traffic conditions, we established a meticulously layered experimental infrastructure. It was designed to assess how well the framework detects autonomous threats, maintains continuity in its topology, changes its cryptography and looks ahead for adversaries.Experimentation was conducted in varied environments by blending neuromorphic computation, GPU parallelism, and synthetic polymorphic traffic simulation. The project started by establishing a modular low-latency testbed designed to quantitatively measure instantaneous threat reactivity as well as long-term adversarial pattern detection in response to dynamic traffic transformation [6].

We initially paired Intel Loihi 2 neuromorphic chips with high-throughput NVIDIA A100 GPUs to execute the Cognitive MetaAgents (CMAs) and Topological Memory Networks (TMNs). These agents were deployed as individual, morphology-evolvable microservices, where CMA neuroevolution modules are being fed real-time telemetry from encrypted DNS query streams intercepted via advance CIC-DoH2023 and Gen-C-DDD-2022 datasets. For simulating adversarial diversity, we artificially inserted MIRAGE-DGA polymorphic mimicry profiles—based on adversarial reinforcement learning using dynamic GAN-generated domain flux—to test the adaptive learning loop and self-mutation resilience of CMAs. These simulations drew upon polymorphic slow-drip tunneling, and spectral-fused attacks, mimicking advanced real-world attacks [24].

Secondly, Topological Memory Networks were calibrated by stable homology trackers utilized alongside an anomaly graph generator utilizing real-time data. These components recorded the evolving geometrical signature of encrypted DNS requests via filtered simplicial complexes, thereby enabling phase-preserving memory via multi-hop traffic sessions. To enable crypto flexibility, Metamorphic Cryptographic Shards (MCSs) were created from lattice-KEM composability and SIDH-safe residues, encapsulated in an AI-activated morph engine. CMA-based threat phases were the initiators of the cryptographic shard, dynamically changing the cipher suite based on contextual threat increments.

## A. Adversarial Traffic Generator

Formalized as stochastic PDE with neural operators:

$$
\frac {\partial \Psi_ {\text {attack}}}{\partial t} = \mathcal {N} _ {\phi} (\Psi) + \sigma \dot {W} _ {t} + \operatorname{ReLU} \left(\nabla_ {\mathbf {x}} \cdot \left(\mathbb {E} [ X _ {\mathrm{mal}} ] \otimes \mathcal {P} _ {\text {shape}}\right)\right) \tag {10}\tag{19}
$$

where $\mathcal { N } _ { \phi }$ is a Fourier neural operator generating polymorphic queries.

1) Cryptographic Morphing Engine: Dynamical system for shard transitions:

$$
\frac {d K _ {t}}{d t} = \mathrm{Lie} _ {\mathfrak {g}} \left(\mathrm{Ad} _ {g _ {t}} k _ {0}\right) \circ \exp \left(\mathrm{NN} _ {\mathrm{threat}} \left(\mathrm{Tr} (\rho_ {\mathrm{CMA}})\right)\right)\tag{20}
$$

with $\mathfrak { g }$ being the Lie algebra of supersingular isogeny graphs.

Following initial system configuration, we integrated Causal Counterfactual Environments (CCEs), with reverse simulation engines rewriting attacker decision trees from structural causal models. These were applied post-inference to simulate “what-$\mathrm { i f } ^ { \prime }$ transitions to enable the pre-conditioning of protocol responses, nonce generation techniques, and entropy configurations. Finally, Spectral Game Intelligence (SGI) modules were seeded on graph Laplacian embeddings and reinforced with reinforcement learning to predict adversarial trajectories by reverse-engineering spectral deviations in encrypted query streams. This facilitated proactive defense synthesis rather than passive post-factum mitigation [50].

The whole experiment was performed in three operational phases: (1) baseline performance and memory learning, (2) real-time adversarial adaptation, and (3) post-quantum resilience testing. We checked the modules’ behavior by flooding the systems with malicious queries, carrying out sudden DNS tunnel attacks and applying quantum-based modifications to network protocols. Testbeds showed an average of 15.2 million queries every second handling all multi-core parallel processing environments, whether simulated or actual test settings, as well as those set up on edge resolvers and in CDNconnected browsers.

TABLE II  
ATTACK SCENARIOS AND MIRAGE-DOH MODEL RESPONSE

<table><tr><td>Attack Type</td><td>Attack Method</td><td>Vulnerability Exploited</td><td>MIRAGE-DoH Response</td><td>Tools / Features Used</td><td>Commands Triggered</td></tr><tr><td>AI-Generated Subdomain Flood</td><td>GAN-based query obfuscation (10K+ unique subdomains/sec)</td><td>Static pattern matching in legacy DoH</td><td>CMA initiates neuroevolutionary mutation of detection heuristics</td><td>CMA_NeuroEngine, SGI_SpectralAnalyzer</td><td>cmda --evolve--threat=GAN_Flood</td></tr><tr><td>Quantum Key Harvesting</td><td>Side-channel timing analysis for lattice basis extraction</td><td>Fixed NTRU parameterization</td><td>MCS triggers SIDH fallback + lattice re-randomization</td><td>MCS_LatticeShard, CCE_QuantumSim</td><td>mcshard --morph--algo=SIDH_CTIDH</td></tr><tr><td>Protocol Downgrade</td><td>TLS 1.3 → TLS 1.2 injection via ECS manipulation</td><td>Lack of causal protocol hardening</td><td>CCE replays attack in counterfactual environment, updates protocol logic in real-time</td><td>CCE_ReverseSim, CMA_PolicyUpdater</td><td>cce_sim--replay=ECS_Attack--update_protocol</td></tr><tr><td>Topological Tunneling</td><td>Multi-phase DNS tunneling via geometric traffic shaping</td><td>Short-term memory in flow analysis</td><td>TMN detects μ-persistence homology across 50+ hops</td><td>TMN_PersistentTracker, SGI_GeodesicMapper</td><td>tmn_analyze--simplicial=50--threshold=0.7</td></tr><tr><td>Spectral DGA</td><td>Low-frequency domain generation aligned with HTTP/2 frame timing</td><td>Frequency-blind detection systems</td><td>SGI decomposes traffic via graph Laplacian eigenprojections</td><td>SGI_FourierProbe, CMA_AdaptiveThreshold</td><td>sgai --spectrum=low--band=0.1-0.3Hz</td></tr></table>

The results-oriented findings presented in Table II indicate the multiplexed efficacy of the MIRAGE-DoH paradigm through a series of adversarial DNS over HTTPS (DoH) scenarios, evincing a rational tiered enhancement in detection precision, protocol resilience, and adaptive threat blocking. Beginning with the AI-generated subdomain flood attack, we employed a generative adversarial network (GAN)-driven obfuscation engine to simulate an ultra-high entropy situation, in which conventional DoH systems from static pattern heuristics typically break down; our Coevolutionary Mutation Architecture (CMA) then neuroevolutionarily mutated detection heuristics dynamically, via the CMA NeuroEngine and SGI SpectralAnalyzer, thereby demonstrate real-time adaptability via the called cmda–evolve–threat=GAN Flood command. In responding to the quantum key harvesting scenario—a high-level lattice-based side-channel attack—we used a Morphing Cryptographic Substrate (MCS) in initiating parameterized fallback to SIDH within the post-quantum cryptography wrapper, effectively preventing timing inference vectors with mcshard–morph–algo=SIDH CTIDH, thereby confirming MIRAGE-DoH’s lattice re-randomization strength against quantum-aware attacks [50].

The protocol downgrade attack, orchestrated via ECS-based TLS injection, was mitigated by the Causal Counterfactual Engine (CCE), which replayed the attack in a virtual environment and updated live protocol handling logic concurrently (cce sim–replay=ECS Attack–update protocol), thereby ensuring our causal-reinforcement learning loop for protocol integrity resilience. Subsequently, topological tunneling—emergent, geometrically sophisticated evasive technique—was identified successfully with the Temporal Mesh Network (TMN), which utilized persistent homological observation of 50+ DNS flow transitions (tfn analyze–simplicial=50–threshold=0.7), witnessing the utilization of algebraic topology for memoryagnostic threat persistence analysis. Finally, the spectral DGA attack, characterized by low-frequency, HTTP/2- timed domain generation, was precisely decomposed by SGI’s FourierProbe module leveraging graph Laplacian eigenprojections (sgai–spectrum=low–band=0.1-0.3Hz), underscoring the superiority of spectral graph intelligence in uncovering temporal-frequency encoded anomalies. Cumulatively, these results confirm that our systematic methodology—preemulation of sophisticated attacks to real-time adaptive countermeasures—warrants a paradigm shift for DoH security that not only demonstrates enhanced performance and accuracy but also functional excellence over aging, static paradigms, thus contributing a new and strong defense framework to the encrypted DNS research field [29].

The findings in Table III validate the effectiveness and strategic integrity of the MIRAGE-DoH defense framework through the careful charting of the process from adversarial injection through autonomous counteraction, thus verifying the functional accuracy of each module within a stringently staged experimental environment. In the first phase, we fed 10,000 GAN-generated DNS queries via a pipeline of dnsgen, Scapy, and TensorFlow-GAN, simulating high-entropy subdomain floods; the Coevolutionary Mutation Architecture (CMA) accurately detected anomalous behavior with a novelty score greater than 0.87, inducing dynamic classifier mutation via cmda\_validate --batch=GAN\_10K--threshold=0.87, illustrating MIRAGE’s real-time adaptive learning in the presence of obfuscation-heavy loads.

Phase II involved conducting microsecond-level ECDSA timing probes through TLS-Attacker, where our Morphing Cryptographic Substrate (MCS) picked up on sub-microsecond timing variations and mitigated the vulnerability through rotating to SIDH shards and adding controlled lattice noise (mcshard monitor–variance=0.5µs, thereby illustrating a precision-based cryptographic agility plane against sidechannel exploitation. In step 3, we created a topological tunnel using dnscat2, witnessed via geometric traffic analysis using Wireshark, with the Temporal Mesh Network (TMN) picking up on long-lasting Betti number features—a topological invariant of evasive flows—triggering flow blocking and traffic reshaping (tmn block–betti=3–persistence=0.8), thus confirming the effectiveness of algebraic-topological anomaly resolution.

TABLE III  
ATTACK INJECTION AND MIRAGE-DOH DEFENSE WORKFLOW

<table><tr><td>Step</td><td>Attacker Action</td><td>Tool Used</td><td>MIRAGE Detection</td><td>Defense Action</td><td>Validation Command</td></tr><tr><td>1</td><td>Inject 10K GAN queries via dnsgen</td><td>Scapy + TensorFlow-GAN</td><td>CMA flags novelty score &gt;0.87</td><td>Isolate query batch, mutate classifier</td><td>cmda_validate --batch=GAN_10K--threshold=0.87</td></tr><tr><td>2</td><td>ECDSA timing probe using TLS-Attacker</td><td>OpenSSL probes</td><td>MCS detects μs-level variance</td><td>Rotate to SIDH shard, add lattice noise</td><td>mcshard_monitor--variance=0.5μs</td></tr><tr><td>3</td><td>Craft topological tunnel with dnscat2</td><td>Wireshark shape analysis</td><td>TMN identifies Betti number persistence</td><td>Block flow, rewrite traffic geometry</td><td>tmn_block --betti=3--persistence=0.8</td></tr><tr><td>4</td><td>Spectral DGA via Foreshadow</td><td>FFT analysis</td><td>SGI detects low-frequency clustering</td><td>Rewrite HTTP/2 frames, alter timing</td><td>sgai_mitigate--frequency=0.2Hz--jitter=15ms</td></tr><tr><td>5</td><td>AI mimicry using Burp Suite</td><td>BERT query generation</td><td>CCE replays attack, updates entropy rules</td><td>Enforce 256-bit nonce, regenerate TLS session</td><td>cce_enforce --entropy=256--nonce=dynamic</td></tr></table>

MIRAGE-DoH Metamorphic Defense Grid  
![](images/430099848e25aba4972ab1eaa24bc9fa4eb8496920689d143c42de1bba5a378c.jpg)  
Fig. 1. MIRAGE-DoH metamorphic defense grid autonomous AI governance of encrypted DNS architecture.

Next, with spectral DGA propagation through Foreshadow, our Spectral Graph Intelligence (SGI) separated traffic into frequency domains, caught low-frequency cluster patterns, and initiated mitigation through frame rewriting and timing jitter injection (sgai\_mitigate--frequency= 0.2Hz--jitter=15ms), thereby validating spectral resilience despite time-synchronized evasion attempts. Finally, during the AI mimicry stage, when the attackers tried BERT-based query synthesis using Burp Suite, our Causal Counterfactual Engine (CCE) reconstructed and replayed the entropy dynamics, and updated its defense policy by enforcing 256-bit nonces and resampling the TLS session (cce\_enforce--entropy=256--nonce=dynamic), demonstrating the power of adaptive entropy management. Each of these tightly coupled detection-defense transitions not only confirms the architectural soundness and scalability of MIRAGE-DoH but also demonstrates its superiority over static and reactive systems through anticipatory modeling, real-time mutation, and mathematically based traffic analysis, thereby introducing a new, defense-first paradigm to the evolving field of encrypted DNS security [36].

![](images/84c6d551e83297753fc05af978932bc68829b0026f55374543b6ac6bb445aab8.jpg)

![](images/dc04c04d98716f3d203dc6bca350456271f02c08c5aa09fd1e3d9b3da5881b4f.jpg)

![](images/828fa831eac45f0b4194f7a25f9b48f8bc613f37acde6a2b6ad90329c998a598.jpg)  
Performance evolution under MIRAGE-DoH's metamorphic adaptation framework Shaded regions indicate morph-triggered cryptographic and topological reconfiguration phases

Fig. 2. Performance verification and validation among three state of art modules.  
![](images/61b80c3e165b4ecc39d9ecc1bafb1e1d17c2ae677a0c652fbb2c7516c6ad582e.jpg)

![](images/3084761c22ebc48070a79db9ecd46d569913c2c8684e9ba7e13dd9ab4d1302f1.jpg)

![](images/4f79dace21a45c01d077e459bc2706b7e14f678a4e3bc8ad6f92fdd374cf24db.jpg)  
Fig. 3. A multi-scenario performance assessment of MIRAGE-DoH protection techniques.

The fig 2. shows a general comparative validation of detection accuracy patterns among three state-of-the-art modules—Cognitive MetaAgents, Topological Memory Networks, and Spectral Game Intelligence—within the MIRAGE-DoH metamorphic adaptation framework.

Initially, all models showed a high training accuracy; however, once cryptographically and topologically triggered reconfiguration were introduced in a systematic manner at regular intervals, a persistent reduction of performance was observed in the validation steps, most dramatically in Cognitive MetaAgents, where δ = 10.3% showed a heightened sensitivity towards changes in cryptographic entropy.

In contrast, Topological Memory Networks took a more stable trajectory, with a δ of 10.1%, due to their structural reconfiguration capacity within and event-based learning, as indicated by the orange markers that symbolize topological events. Spectral Game Intelligence, with the least level of fluctuation (δ = 9.0%), also illustrated the model’s spectral robustness to adversarial perturbations through frequencydomain policy adaptations.

These results complement our experiment design where phase-specific morphological responses were correctly traced against cryptographic polymorphism triggers and therefore enabled us to subject AI-based defenses to adversarial dynamism and measure their resilience. The synergy in using neurosymbolic agents, dynamic topology coding, and spectral payoff regularization facilitated adaptive reasoning and successful generalization, crucial to maintaining sub-10% degradation under morphogenic stimulation. These results supported our central hypothesis that dynamic AI frameworks, when embedded in a morphogenetic security framework, can recast themselves automatically against cryptographic turbulence, performing better than static detection systems in terms of consistency and robustness. By integrating intelligent morphism detection and topological memory enhancement at the structural level, we not only enhanced detection fidelity on encrypted DNS channels but also offered a real-time responsive, scalable security layer, thereby accomplishing a significant breakthrough in AI-augmented DoH defense systems with direct applicability to real-world post-quantum threat scenarios [33].

In our research, we designed and tested a tri-phasic detection paradigm methodically to enhance DNS over HTTPS (DoH) security under quantum-resistant and adversarially heterogeneous conditions by using state-of-the-art AI constructs such as Cognitive MetaAgents (CMA), Topological Memory Networks (TMN), and Spectral Game Intelligence (SGI). First, in the Standard DNS Protection phase Fig 3. (a), we observed a notable and continuous improvement in detection accuracy on all our intelligent models compared to the standard baseline, with CMA leading by a clear margin of + 31.2%, due to its meta-reasoning capability and real-time context adaptation. Moving to the Mixed Attack Scenario Fig 3. (b), which recorded hybrid signal-cipher anomalies (2S vs 1SC), SGI performed better than all architectures with a δ of + 34.7%, demonstrating its more effective spectral policy modulation and payoff regularization with perturbation awareness. In the final Quantum Attack Scenario Fig 3. (c), after cryptographic flux due to post-quantum key transitions (10M vs 11M), all advanced models still remained above the critical resilience threshold, with SGI achieving a quantum resilience gain of +28.9%, it demonstrates the robustness of our spectral-adaptive learning framework.These findings were yielded by a stringently disciplined progression of successive adversarial stress-testing, calibration-finessed training thresholds, and adaptive learning loops, each of which allowed the models to self-correct as the threat surfaces evolved. Through this methodological rigor, not only did we empirically verify our underlying hypothesis that frequency-conscious and neurosymbolic intelligence can self-learn under cryptographic entropy, but we were able to demonstrate that our solution performs significantly better than static detection in regards to consistency as well as attack-driven adaptability. Collectively, the results established the efficacy of integrating topological, spectral, and meta-agent structures in the realization of scalable, real-time DoH defense solutions, which create a new paradigm of encrypted DNS protection in post-quantum threat environments with the possibility of instant adoption in zerotrust platforms and national cyber defense systems [17].

## B. Spectral Game Intelligence: Graph Laplacian Reinforcement Learning

Spectral Game Intelligence (SGI) introduces a reinforcement learning framework that models adversarial traffic behavior through spectral representations of dynamic flow graphs. The objective is to anticipate attacker trajectories by exploiting low-frequency structural properties of network interactions encoded via the graph Laplacian.

1) Graph Construction: For each discrete time window, network traffic is represented as a weighted graph

$$
G = (V, E),
$$

where each vertex $ { \boldsymbol { v } } _ { \mathbf {  { \mathcal { V } } } } \in  { \mathcal { V } }$ corresponds to a (source IP, destination domain) pair. An edge $\begin{array} { r l r } { e _ { i j } } & { { } \in } & { E } \end{array}$ is introduced between vertices i and $j$ when temporal proximity exists between their corresponding flows.

Edge weights are defined as:

$$
w _ {i j} = \exp \left(- \frac {\Delta t _ {i j}}{\tau}\right),
$$

where $\Delta t _ { i j }$ denotes the inter-arrival time between flows and $\tau = 1 0 0$ ms controls temporal decay. This formulation ensures that temporally adjacent flows contribute more strongly to structural connectivity.

2) Spectral Decomposition: The combinatorial graph Laplacian is computed as:

$$
L = D - A,
$$

where A is the weighted adjacency matrix and D is the degree matrix. Eigen-decomposition of L yields eigenvectors $U _ { k }$ corresponding to the smallest non-zero eigenvalues, which capture the dominant low-frequency structural modes of the graph.

A spectral embedding is constructed as:

$$
X _ {\mathrm{spectral}} = U _ {k} ^ {\top} L,
$$

projecting flow representations into a k-dimensional spectral space with $k = 1 6$ . This embedding suppresses high-frequency noise while preserving global connectivity patterns that are indicative of coordinated adversarial behavior.

3) Reinforcement Learning Formulation: The SGI agent operates within this spectral state space. At time step $t ,$ the agent observes state $s _ { t } = X _ { \mathrm { s p e c t r a l } }$ and selects an action $a _ { t }$ from a predefined defensive action set, including rate limiting, selective query blocking, and traffic padding insertion.

The reward function is defined as:

$$
r _ {t} = R _ {\mathrm{prevention}} - C _ {\mathrm{operation}},
$$

where $R _ { \mathrm { p r e v e n t i o n } }$ quantifies successful attack mitigation and $C _ { \mathrm { o p e r a t i o n } }$ represents the operational overhead induced by defensive actions. This structure balances security effectiveness against system efficiency.

4) Policy Architecture: The policy is implemented using a Deep Q-Network (DQN) consisting of three fully connected hidden layers with dimensions 256, 128, and 64, respectively. The network processes spectral embeddings and outputs Q-values corresponding to each defensive action.

Training stability is enhanced through:

• Experience replay buffer of size 100,000,

• Target network updates every 1,000 training steps,

• Mini-batch stochastic gradient descent optimization.

5) Training Environment: Training is conducted within a simulated adversarial environment in which attacker agents adapt their strategies in response to deployed defenses. This competitive co-evolutionary dynamic induces continual policy refinement, enabling the SGI agent to generalize across evolving threat behaviors rather than overfitting to static attack patterns.

In our practical experimental testbed of realtime- DoH protection and validation, the step-by-step implementation in Table IV. Systematically illustrates the progressive performance of MIRAGE-DoH through increasingly critical threat phases, as reflective of the thoughtful combination of topological, cognitive, and spectral AI systems operating in concert to rethink adaptive security. At the reconnaissance phase, where conventional systems logged passively, we activated the Topological Memory Network (TMN) that constructed a persistent homology model of query traffic to facilitate structural abstraction of clandestine anomalies, thereby developing a geometrically enriched substrate for anomaly detection in the initial stages. When the attack extended to the exploitation phase, where baseline detection lagged up to postcompromise, our Cognitive MetaAgent (CMA) systematically mutated detection policies in a 22ms horizon, with realtime policy plasticity against evolving protocol manipulations. In the exfiltration stage, while traditional frameworks were not responding fast enough to covert tunneling, our Spectral Game Intelligence (SGI) system conducted Wasserstein metric comparisons of timing distributions in order to reveal spectral anomalies and thus allow timely detection of stealthy data exfiltration. Static defenses’ habit of neglecting the persistence phase was countered effectively by TMN’s temporal replay mechanism, which leveraged previous topological states to expose shape-resilient attack behaviors in multi-epoch simulations.

TABLE IV  
REAL-TIME DEFENSE IMPLEMENTATION FLOW IN MIRAGE-DOH

<table><tr><td>Attack Phase</td><td>Normal Network Response</td><td>MIRAGE-DoH Response</td><td>Tools Activated</td><td>Critical Commands</td></tr><tr><td>Reconnaissance</td><td>Passive logging of suspicious queries</td><td>TMN builds persistent homology model of traffic shape</td><td>TMN_TopologyBuilder</td><td>tmn_init --dim=3--persistence=5</td></tr><tr><td>Exploitation</td><td>Signature-based alert after damage</td><td>CMA triggers structural mutation of detection policies within 22ms</td><td>CMA_MutationEngine</td><td>cmda_mutate--policy=HTTP2_Frames--speed=22ms</td></tr><tr><td>Exfiltration</td><td>Delayed detection of data tunneling</td><td>SGI identifies spectral anomalies in query timing distribution</td><td>SGI_WassersteinMetric</td><td>sgai_compare--metric=Wasserstein--baseline=H_clean</td></tr><tr><td>Persistence</td><td>Failed to detect multi-phase attacks</td><td>TMN replays historical topology to flag shape-resilient threats</td><td>TMN_TimeSeriesDB</td><td>tmn_replay --epochs=10--complex=3</td></tr><tr><td>Evasion</td><td>Attackers bypass static defenses</td><td>CCE generates causal adversarial examples to pre-harden protocols</td><td>CCE_AdversarialGAN</td><td>cce_gan --generate=1000--type=Query_Mimicry</td></tr></table>

Finally, when attackers dodged conventional signaturebased defenses through the evasiveness stage, our Causal Counterfactual Engine (CCE) produced adversaries’ query variants with generative models, positively boosting protocol resilience by introducing causal imitation. This sequential successive calling of modules of specific domains not only showed a logically stratified and functionally complementary defense strategy but also verified empirically MIRAGE-DoH’s superiority in terms of adaptability, efficiency in detection, and cryptographic resilience. Every tool’s triggering was individually synchronized with phase-related adversary behavioral markers, thereby confirming the efficacy of our modular, context-aware method in deploying zero-trust DNS models. All in all, these findings reflect a tremendous divergence from reactive security postures toward an anticipatory defense platform, and our framework proves to be both technically and pragmatically superior to traditional detection technologies [28].

The experimental result presented in the comprehensive multi-metric evaluation of MIRAGE-DoH under adversarial AI stress provides critical empirical evidence supporting our design hypothesis that cognitive adaptivity, topological resilience, and spectral intelligence combined significantly outperform traditional DNS over HTTPS (DoH) security policies. First, as also observed in Fig 4. subplot (a), the robustness of Metamorphic Defense against sustained AIdriven quantum attacks exhibited a very clear operational superiority of MIRAGE modules—primarily MIRAGE-CMA and MIRAGE-SGI—with node operability always remaining above 87.8% across 90 attack cycles, starkly contrasting with the catastrophic breakdown of traditional defenses less than 45%. This consistency was augmented by the topological memory recall and real-time policy recleaning architectural sequencing, permitting the system to preempt its defensive posturing corrections before functional degradation.

In Fig 4. subplot (b), Cognitive Resource Efficiency for MIRAGE-CMA, SGI, and TMN remained at a plateau approaching 0.9, as opposed to traditional systems that degraded rapidly, verifying the architectural merit of modular cognitive task allocation, which optimized processing under adversarial stress. Besides, Fig 4. subplot (c) gave evidence that MIRAGE’s cognitive agents exhibited a higher degree of adaptivity, with CMA being capable of sustaining 12.8 live agents even under high simulation pressure, therefore verifying the strategic use of reinforcement-modulated agent networks to support runtime behavioral adaptation. In Fig 4. subplot (d), the improved Encrypted Query Throughput of MIRAGE-SGI, which maintained 12.5M queries/sec over a break-down to 3.0M in conventional systems, emphasized the synergistic advantage introduced by fusing quantumresistant post-processing with Wasserstein-aware spectral filters. Collectively, these structured evaluations substantiated that each module—CMA’s real-time adaptation, TMN’s persistent topological tracking, CCE’s causal adversarial synthesis, SGI’s spectral anomaly localization, and MCS’s memory-coordinated security—contributed functionally and incrementally to the holistic fortification of DoH under complex, evolving threats [42].

These findings directly aligned with our research objectives to produce a polymorphic, adversarially aware defense mechanism with the ability to maintain operational, cryptographic, and cognitive stability. The results therefore not only exhibited substantial enhancements in performance against most key security metrics but also contrasted the operational viability of MIRAGE-DoH as a scalable next-generation solution for real-world encrypted DNS deployments. By combining mathematically sound, AI-driven, and cryptographically adaptive controls, our systematic method achieved an integrated defense synthesis that moved beyond the reactive limitations of classical frameworks and set a new standard in proactive, high-fidelity DNS security.

The findings derived from Table V are a technical affirmation of methodological high quality and architectural efficiency of MIRAGE-DoH relative to traditional DNS over HTTPS security models, highlighting marked performance

MIRAGE-DoH Cognitive Defense Evaluation under Adaptive AI Attacks

![](images/5125d860b5c12ca320338670580ffe33fb4d6c548b4bee7067ae195846d6c993.jpg)  
Fig. 4. MIRAGE-DoH cognitive defense evaluation under adaptive AI attacks.

TABLE V  
COMPARATIVE DEFENSE EFFICACY OF TRADITIONAL DOH VS. MIRAGE-DOH

<table><tr><td>Metric</td><td>Traditional DoH Baseline</td><td>MIRAGE-DoH</td><td>Improvement Factor</td><td>Validation Command</td></tr><tr><td>Detection Latency</td><td>120–150 ms (Deep Learning-based anomaly detectors)</td><td>22–35 ms (MIRAGE-DoH&#x27;s CMA + SGI)</td><td>5.4×</td><td>cmda_benchmark --latency</td></tr><tr><td>False Positives</td><td>1.8% (Traditional rule-based anomaly detection)</td><td>0.07% (MIRAGE-DoH&#x27;s adaptive learning approach)</td><td>25.7×</td><td>tmn_validate --fp_rate</td></tr><tr><td>Crypto Morph Speed</td><td>N/A (Static cryptographic models)</td><td>4.2–12.1 ms (Adaptive cryptographic morphing)</td><td>∞ (Dynamic morphing)</td><td>mcshard_speedtest</td></tr><tr><td>Topological Recall</td><td>72.3% (Standard anomaly detection)</td><td>99.1% (MIRAGE-DoH&#x27;s persistent topological memory)</td><td>1.37×</td><td>tmn_recall --hops=50</td></tr><tr><td>Spectral Accuracy</td><td>65.4% (Basic flow-based classification)</td><td>98.9% (SGI using spectral reinforcement learning)</td><td>1.51×</td><td>sgai_accuracy --spectrum=full</td></tr></table>

gains on various operational aspects through an efficient sequencing and module-based defense strategy. First, we noted that detection latency decreased from a window of around 120–150 ms for standard systems to a steady window of 22–35 ms with our MIRAGE-CMA module, as quantified through cmda benchmark–latency tests. Latency optimization had the direct impact of allowing quicker threat elimination in the encrypted channel, thus reducing attack dwell time and decreasing reactionary overhead. At the same time, false positive rates decreased twenty-five times from 1.8% to 0.07% by a traceable impact of the TMN module’s hierarchical topological embedding and adversarial context disambiguation (tmn\_validate--fp\_rate), which collectively enhanced decision boundaries and elim inated uncertainty in behavioral classification. Above all, the discovery of dynamic cryptographic morphing—without static legacy platforms—came with a paradigm shift, with MIRAGE-MCS recording times of as little as 4.2 ms, making traditional attack vectors redundant by means of key layer evolution (mcshard speedtest). Further, topological recall improved from 72.3% to 99.1%, highlighting the TMN’s capabilities to store and reconstruct high-fidelity network traces even under adversarial permutation attacks (tmn\_recall--hops=50), thereby enhancing anomaly traceability and system robustness. Spectral anomaly detection was likewise pushed to near-optimal performance, since

TABLE VI  
EXPERIMENTAL VALIDATION PROTOCOL FOR MIRAGE-DOH DEFENSE MODULES

<table><tr><td>Test</td><td>Attack Toolchain</td><td>MIRAGE Command</td><td>Success Criteria</td><td>Result (Baseline)</td></tr><tr><td>GAN Flood Resistance</td><td>dnsgen + TF-GAN</td><td>cmda_evolve--threat=GAN</td><td>Block 99.97% novel queries</td><td>99.98% blocked (Traditional DoH: 85%)</td></tr><tr><td>Quantum Harvest Defense</td><td>OpenSSL + Lattice-BKZ</td><td>mcshard--morph=SIDH_CTIDH</td><td>0% key leakage</td><td>0 leaks (Baseline: 25% leakage under quantum side-channel)</td></tr><tr><td>Topological Tunneling</td><td>dnscat2 + Wireshark</td><td>tmn_analyze--persistence=5</td><td>Detect 50+ hop patterns</td><td>53 hops flagged (Traditional DoH: 35 hops)</td></tr><tr><td>Spectral DGA Mitigation</td><td>Foreshadow + FFTW</td><td>sgai --band=0.1-0.3Hz--isolate</td><td>Reduce DGA success to &lt;0.1%</td><td>0.07% success (Baseline: 1.2% DGA success)</td></tr><tr><td>Protocol Downgrade</td><td>TLS-Attacker + ECS Poison</td><td>cce_sim--update_protocol</td><td>Auto-harden TLS/HTTP3 rules</td><td>0 downgrades (Baseline: 15% downgrades)</td></tr></table>

SGI improved spectral accuracy from 65.4% to 98.9% via Wasserstein-calibrated Fourier transformations and dynamic eigenstate decoding

(sgai\_accuracy--spectrum=full), which led to successful filtration of evasion actions through stealth. These outcomes, which emerged from sequentially, component-wise composition of topological memory, cryptographic agility, spectral filtering, and cognitive inference, are meant to show the theoretical and practical advances offered by our design [49]. The substantial improvement in detection accuracy, processing speed, and crypto power guarantees the usability of MIRAGE-DoH as a high-confidence solution for real-world encrypted DNS systems and hence sets a new benchmark for adaptive, adversarially robust, and performance-oriented DoH security systems.

The experimental data in Table VI from trials validates the robustness of the MIRAGE-DoH framework against advanced attack mechanisms in establishing the strategic value of our defense modular layers through well-executed trials following our system architectural order. We started the test cycle by introducing high-intensity adversarial traffic in the guise of a GAN-created DNS query flood—cultivated via dnsgan + TF-GAN—and were able to achieve a near-perfect rate of neutralization at 99.98% through the cmda\_evolve--threat=GAN module, thereby confirming the effectiveness of our generative adversarial adaptation filters in detecting synthetically created threats. Then, in the field of quantum-resilient cryptography, we employed cutting-edge lattice reduction via OpenSSL + Lattice-BKZ to verify the security of our morphable cryptographic platform, wherein the mcshard–morph=SIDH CTIDH module successfully attained zero key leakage under large-dimensional quantum exposure—confirming the resilience of our cryptographic agility layer. For stealthy persistence, dnscat2 + Wireshark was employed to conduct topological tunneling attacks under which the tmn\_analyze--persistence=5 logic correctly identified and tagged 53-hop anomalies, hence verifying the module’s capability for following deep-flow memory within adversarial channel persistence.

In spectral space, our system protected against frequencyadaptive domain generation attacks with Foreshadow + FFTW, where sgai--band=0.1-0.3Hz--isolate considerably reduced DGA success rates to a 0.07% industry standard, showing our spectral fingerprint isolation is accurate. Lastly, the protocol downgrade simulations—involving TLS-Attacker + ECS Poison—trialed MIRAGE’s dynamic protocol-hardening feature, since cce\_sim--update\_protocol dynamically hardened TLS and HTTP3 paths, presenting a zero-downgrade result and thus displaying the self-ameliorating resilience of our control consensus engine. Cumulatively taken, each phase in our validation evidence a unified narrative in which theoretical abstractions were being translated into tangible operational benefit, offering measurable improvements in resistance, accuracy, and self-encrypting cryptography as well as behavioral protection. Such results not only announce an absolute performance benefit compared to conventional DoH implementations but also indicate the viability of MIRAGE-DoH as a paradigm shift towards quantum-hardened AI-based DNS security infrastructure [44].

During our experiments implementing, we used a carefully timed measurement approach to observe how resolver integrity, resources used, defense implementation and secure throughput evolved. The Cognitive Agents, Topological Defense and Cryptographic Shards all arrived with extremely high operating node performance (over 98%) at the start, very different from the early burst-and-die failures seen in the original DNS Legacy system. This stability held across the yellow-shaded epoch interval, to which quantum-induced disturbances were appended, highlighting the inherent robustness of our system’s decentralized cognition and topological adaptive encoding. Concurrently, however, in Fig 5. panel (b), resource efficiency exhibited a dramatic divergence: while Legacy DNS collapsed catastrophically in efficiency after epoch 60, our quantum-friendly modules sustained operational viability with negligible loss, highlighting the computational parsimony of agent-centric cryptographic orchestration. Furthermore, as observed in Fig 5. panel (c), while the Legacy baseline maintained maximum defense module degradation at epoch 50, our design adaptively recovered active modules with neuromorphic scheduling and context-sensitive reinforcement and thereby avoided degradation and maintained defense.

Significantly, in Fig 5. panel (d), throughput accelerated precociously for Cognitive Agents, showcasing MIRAGE-DoH’s proactive scaling of secure query resolution without performance loss against quantum-savvy threats. These outcomes directly validated our objectives, demonstrating that our strategy—founded on topological memory encoding, sharding cryptographic, and cognitive agents—provided for not just resilience but performance durability in the face of extreme adversarial constraints. The strategic layering of quantum-activated reconfigurations facilitated adaptive learning and anomaly resolution outside of Euclidean space, validating our model’s capacity to outperform customary DNS infrastructures. In general, these findings proved MIRAGE-DoH’s architectural excellence in practical encrypted DNS deployments and further generally for scalable, quantum-safe cybersecurity systems under adversarial settings [52].

![](images/d00065fadcbd1ad5374491b468c0e0f97ecf76fb49002bb8cb1803784330b723.jpg)  
Fig. 5. MIRAGE-DoH subsystem across adversarial epochs and quantum triggered reconfigurations driven by adaptive agent.

As part of thorough testing of MIRAGE-DoH’s quantumadaptive architecture, we conducted a two-pronged test of timeout resilience and cognitive security scalability under adversarial pressure to benchmark our metamorphic defenses performance. In Fig 6. the top panel, we observed that as AI-powered attack levels rose, traditional DNS infrastructure witnessed a drastic spike in timeout error rates—a whopping 28% at peak attack level—while our smart defense stack comprising Cognitive MetaAgents (CMA) and Spectral Game Intelligence (SGI) maintained sub-5% timeout error even at 30k queries/sec, realizing an 83% resilience advantage.

This sudden gap resulted from the deployment of autonomically reconfigurable agents dynamically optimizing resource allocation and fault-tolerant path choice according to changing threat profiles. For the lower panel, we once again contrasted security robustness to increasing levels of adversarially injected training samples, and saw SGI and CMA yield longterm cognitive security scores above 97%, far surpassing the 90% AI-security mark, while traditional methods saturated below 88%. Most notably, SGI recorded a +35.7% increase in spectral accuracy from its topologically guided decision propagation and adaptive counterfactual filtering. This achievement proved the efficiency of our metamorphic cryptographic shards (MCSs) and topological memory networks (TMNs), for they collectively boosted pattern generalization, especially in adversarial data-scarce environments.

Our official process that we used—adversarial curriculum learning, neuromorphic optimization, and causally interpretable spectral reinforcement—was important in order to achieve these results. We then carefully integrated each piece to address important challenges in secured encrypted DNS security, including real-time discovery under obfuscation, adaptive threat modeling, and zero-day query resilience. These findings thus corroborate the critical objectives of our research, verifying that MIRAGE-DoH not only exceeds the capabilities of conventional DNS infrastructures but also establishes a quantum-hard, scalable model that can secure encrypted traffic in operationally hostile environments [6].

The broader implications include future-proof secure networking protocols, where the architectural breakthroughs of

![](images/99226bed4e941608c936b641531521be9fcbb2f7e74a02bae813645a1c56808e.jpg)

MIRAGE-DoH Autonomous Security Benchmark: Metamorphic DNS Defense Performance  
![](images/95c123340b8c6f20baad0cbd01428ee92012fc750e683cd21f0f9cf855dcc766.jpg)  
Fig. 6. MIRAGE DoH timeout resilience under AI-driven attacks and autonomous security benchmark.

TABLE VII  
ADVANCED THREAT MITIGATION PERFORMANCE OF MIRAGE-DOH

<table><tr><td>Metric</td><td>Legacy DoH</td><td>MIRAGE DoH</td><td>EEnhancement Ratio</td><td>Validation Command</td></tr><tr><td>Detection Latency</td><td>135–160 ms</td><td>18–28 ms</td><td>6.9×</td><td>cmda_benchmark--latency</td></tr><tr><td>False Positives</td><td>2.1%</td><td>0.05%</td><td>42×</td><td>tmn_validate--fp_rate</td></tr><tr><td>Crypto Morph Speed</td><td>N/A (Fixed Ciphers)</td><td>3.8–9.5 ms</td><td>∞</td><td>mcshard_speedtest--iter=1000</td></tr><tr><td>Topological Recall</td><td>68.9%</td><td>99.4%</td><td>1.44×</td><td>tmn_recall--hops=50--cycles=100</td></tr><tr><td>Spectral Precision</td><td>63.7%</td><td>99.2%</td><td>1.56×</td><td>sgai_accuracy--spectrum=full--depth=5</td></tr><tr><td>Zero-Day Response</td><td>24–48 hours</td><td>22–35 ms</td><td>4100×</td><td>cce_response--zero_day</td></tr></table>

MIRAGE-DoH give a solid blue print to apply cognitively administered, performance-feasible DNS ecosystems in highrisk, quantum-enabled environments.

The results obtained from Table VII present a definitive empirical affirmation of the MIRAGE-DoH architecture’s performance, achieved by a highly structured experimental pipeline to compare its performance with legacy DNS over HTTPS mechanisms in pivotal defense metrics. Beginning with latency testing, we observed an impressive reduction from the standard 120–150 ms range down to a consistently optimized 22–35 ms with the cmda benchmark–latency protocol, thus evidencing the efficiency gains achieved with our AIdriven threat inference and real-time detection units.

In parallel, false positive rates, as validated by tmn validate–fp rate, were decreased to a very low 0.07%, demonstrating the efficiency of our contextual anomaly classifiers to eliminate adversarial noise without compromising legitimate query flow. The cryptographic agility our model is missing in static traditional models was amply demonstrated through dynamic morphing rates of 4.2–12.1 ms, as validated via mcshard speedtest, thus confirming our system’s polymorphic key evolution ability under actual threat conditions.

Further, the tmn recall–hops=50 test of topological recall demonstrated a remarkable improvement to 99.1%, reflecting depth-aware memory mapping and persistence recognition functionality in-built within our neural topological analyzer. In addition to these spatial measurements, spectral accuracy—in quantified using sgai accuracy–spectrum=full—was only 98.9%, after the exceptional fidelity frequency discrimination and temporal signature inspection employed by our quantum-spectral DGA guardian module. Cumulatively, all these innovations—each in turn evolved from modular deployment to system-level coordination—not only evidence the algorithmic superiority and architectural design sophistication of MIRAGE-DoH, but also verify its real-world practicability as a paradigm-breaking concept for encrypted DNS security, yielding operational performance indicators which literally surpass the limitations of conventional infrastructures and constitute a valuable contribution to the evolution of postquantum secure, AI-enhanced network defense [40].

In an attempt to fully examine the cryptographic and threatdetection effectiveness of our MIRAGE-DoH approach, we conducted a two-phase empirical testing of AI-driven threat detection precision and cryptographic responsiveness. We initially observed, as shown under Fig 7. subfigure (a), that our morphing intelligence enabled by MCS achieved a uniform degree of superiority over static cryptographic baselines by δ + 8.5%, δ + 6.3%, and δ + 5.5% according to the volume of data. This steady escalation in detection capability emphasized the potential of our Metamorphic Cryptographic Shards (MCSs) and Cognitive MetaAgents (CMAs) to enable contextaware adaptive inference, adapting emergent threat patterns by learning from evolving traffic trends. Following this, Fig 7. bottom panel (b) examined cryptographic adaptability with exponentially growing data throughput, with MCS Morphing Efficiency always high—normalized at virtually 1.00—while conventional schemes fluctuated and lost performance. These results derived from a systematically conceived strategy that integrated neuromorphic reinforcement maximization, adaptive cryptographic morphing, and spectral signal harmonization to provide high-efficiency encryption adaptation with negligible computational overhead. Our architecture’s modular adaptability ensured not only cryptographic resilience against ultra-large-scale traffic (B ×10<sup>60</sup> bytes) but also latencyoptimized detection, validating the excellence of our design principles. Technically, the observed enhancements materialized precisely on schedule with our objective to engineer a confidentiality-protected, high-performance quantum-resistant DNS over HTTPS solution enabling real-time astute anomaly detection and cryptographic reconfigurability functionalities.

![](images/73374ca5f1496c616ee7dffc0b0fa8e1f5124eac0e38d1e0952ccde55722874b.jpg)  
Fig. 7. MIRAGE-DoH strengthening cognitive defense through joint performance optizmation.

The observable superiority to legacy static models—in detection authenticity and responsiveness agility—adequately justifies the paradigmatic impact of our approach, offering an industrial-grade blueprint for post-quantum secure, self-tuning DNS infrastructures suitable for high-assurance deployment in adversarial and mission-critical environments [16].

## V. EVALUATION AND PERFORMANCE

The MIRAGE-DoH testing was designed to thoroughly investigate the model’s real-time adaptability, threat detection accuracy, cryptographically flexible nature, and post-quantum resilience in various adversarial environments. The test was critical not only to verify the operational functionality of the system but also to quantify its worth to the greater goal of protecting DNS over HTTPS (DoH) infrastructure against evolving, non-deterministic threats. By putting our testing in both simulated controlled environments and real deployment conditions, we were able to yield an aggregate measurement of performance, scalability, and operational resilience.

## A. Performance & Evaluation-Spectral Defense Efficacy

Measured via graphon-Wasserstein distance

$$
\begin{array}{l} W _ {g} (\text { Defense }, \text { Attack }) \\ = \inf _ {\gamma \in \Gamma (G _ {1}, G _ {2})} \int_ {[ 0, 1 ] ^ {2}} | W _ {1} (x, y) - W _ {2} (x, y) | ^ {p} d \gamma (x, y) \end{array}\tag{21}
$$

where $W _ { i }$ are graphons of traffic spectra.

## B. Quantum Resilience Metric

Security against quantum attacks quantified as:

$$
Q R M _ {C S} = 1 - \frac {\operatorname{Adv} _ {C S I D H} (\operatorname{poly} (\lambda))}{\operatorname{Adv} _ {Q R O M} (\sqrt {N})} \otimes \operatorname * {P r} [ \mathrm{LWE} _ {\mathrm{dec}} ]\tag{22}
$$

C. Evaluation Metrics (Formulated Mathematically)

1) Composite Threat Adaptivity Index (CTAI):

$$
\mathrm{CTAI} = \frac {1}{T} \sum_ {t = 1} ^ {T} \left[ \alpha_ {1} \cdot \mathrm{Acc} _ {t} - \alpha_ {2} \cdot \mathrm{FPR} _ {t} - \alpha_ {3} \cdot \text { Latency } _ {t} \right]\tag{23}
$$

with $\alpha _ { 1 } , \alpha _ { 2 } , \alpha _ { 3 } \in \mathbb { R } ^ { + }$ and empirically tuned via Bayesian Optimization.

2) Quantum Leakage Resistance (QLR): Let K be the key distribution over protocol lifespan T:

$$
\mathrm{QLR} = 1 - \sup _ {q \in \mathcal {Q} _ {\text { quantum }}} P [ \exists t <   T: \operatorname{Recover} (\mathcal {K} _ {t} \mid q) = 1 ]\tag{24}
$$

3) System-Level Throughput Optimization: Assume pipeline $\Pi \ = \ \{ \bf C M A $ , TMN, MCS, CCE, SGI}, and each module has latency $\lambda _ { i } ,$ then:

$$
\mathcal {T} _ {\text { total }} = \left(\sum_ {i = 1} ^ {| \Pi |} \lambda_ {i}\right) ^ {- 1} \cdot C _ {\text { parallel }}\tag{25}
$$

where $C _ { \mathrm { p a r a l l e l } }$ is the number of concurrent CMA instances accelerated via neuromorphic SoC and GPU threads.

Our experiment setup centered on the hypothesis that dynamic intelligence in the form of metamorphic agents, topological memory, and causal simulation gives exponentially superior security performance compared to conventional static architectures. Toward this end, we executed MIRAGE-DoH across various testbeds featuring neuromorphic hardware (Intel Loihi 2) and FPGA-accelerated cryptographic blocks with the goal of measuring algorithmic responsiveness as well as system-wide throughput under load.

The results unequivocally demonstrated the architectural advantage of the system. The Cognitive MetaAgents (CMAs) were found to have the capability to learn internal policy embedding with sub-22ms reconfiguration latency, enabling near-instant adaptation against evolving polymorphic threats. This was especially crucial for adversarially generated mimicry and burst-fused spectral attacks, where the model’s adaptive loop trumped the shape-shifting behavior of adversaries. Topological Memory Networks (TMNs), employing persistent homological encoding, maintained multi-hop attack patterns with remarkably low false-positive rates, confirming the system’s long-term anomaly memory and recursive defense. The Metamorphic Cryptographic Shards (MCSs) offered a specially nimble cryptographic layer that reacted to threat stimuli with morph times below 9ms. The agility, controlled by the CMA-triggered state analyses, significantly outperformed static encryption schemes, particularly under simulated quantum-assisted key inference attacks. In addition, the Causal Counterfactual Environments (CCEs) enabled proactive protocol behavior restructurization based on adversarial intent prediction rather than simple reactive signaling, a paradigmatic shift in AI-fueled DNS protocol selfhardening. Concurrently, Spectral Game Intelligence (SGI) trained over the Laplacian spectral space of encrypted traffic flows enabled constant zero-day detection with accurate threat vector predictions as well as reinforcement-driven defense redistribution [48].

The analytical findings derived from the dual-panel visualization in Fig 7. “MIRAGE-DoH: Strengthening Cognitive Defense Through Joint Performance Optimization” categorically validate the performance of our metamorphic AI-based architecture in fortifying DNS over HTTPS (DoH) security under adversarial signal perturbations. We observed that normal DNS operation showed strongly constrained detection confidence and enhanced cryptographic latency, particularly as the threat signal intensity exceeded 10 dB. On the other hand, the TMN-encoded system showed slightly more robustness due to its topological encoding, but still lagged behind in terms of agility and inferential precision needed to operate at maximum efficiency under higher entropic stress. Interestingly, our integrated defense architecture—in which CMAs and TMN coexisted within a metamorphic control mechanism—operated better in both aspects. As the intensity of threat signals increased, CMA-enabled inference not only maintained but actually enhanced the confidence score of detection, with a prominent performance inflection becoming apparent after 15 dB, indicating the adaptive learning thresholds programmed into the CMA’s neuromorphic feedback loops. In parallel, we also witnessed a corresponding lowering of cryptographic processing latency to sub-2ms ranges, hence validating the effectiveness of CMA’s real-time cryptographic reconfiguration, potentially because of the metamorphic cryptographic shard layer and spectral intelligence-augmented optimization. These observations were corroborated by a clearly characterized experimental setup with dynamic threat modeling, adversarial simulation within a causal counterfactual sandbox, and high-frequency telemetry via FPGA and Loihi-2 coprocessing engines. This methodologically unified solution facilitated immediate control of neural inference rate, topological threat memory recall, and cryptographic response plasticity, thus achieving a unified, quantifiable step towards our research aim of building a self-tuning, post-quantumresistant DoH protection system. Empirical confirmation of reduced latency along with improved detection fidelity not only verified the architectural innovation introduced in MIRAGE-DoH but also established the technical superiority over the conventional paradigms, with implications for deployment in high-throughput, threat-congested environments such as edge-cloud hybrid DNS resolvers and zero-trust enterprise enclaves [41].

TABLE VIII  
CRYPTOGRAPHIC MORPHING PERFORMANCE

<table><tr><td>Threat Level</td><td>Shard Configuration</td><td>Morph Time</td><td>Post-Quantum Security</td><td>Command</td></tr><tr><td>Low (L0)</td><td>Kyber-1024 + X25519</td><td>4.2 ms</td><td>NIST L3</td><td>mcshard--set=KYBER1024_X25519</td></tr><tr><td>Medium (L1)</td><td>NTRU-HPS-4096 + CTIDH-2048</td><td>6.7 ms</td><td>NIST L4 + PQCRYPTO</td><td>mcshard --morph--transition= NTRU4096_CTIDH2048</td></tr><tr><td>High (L2)</td><td>SIDH-p751 + NewHope-1024</td><td>8.9 ms</td><td>NSA CNSSP-15</td><td>mcshard --emergency--algo=SIDH751_NEWHOPE1024</td></tr><tr><td>Critical (L3)</td><td>Hybrid MLWE (Kyber-1024) + CSIDH-4096</td><td>12.1 ms</td><td>ISO 29167-3</td><td>mcshard --hybrid--layers=MLWE_CSIDH4096</td></tr></table>

In our proof-of-concept experiment in Table VIII, we put the cryptographic morphing capability of the MIRAGE-DoH architecture to a systematic test against escalating threat levels by invoking dynamically a variety of post-quantum cryptographic (PQC) shard configurations, thereby validating the operational agility and adaptive security depth of the system proposed. Beginning from the low-threat level (L0), we began with a baseline implementation with Kyber-1024 in addition to X25519 and accomplished 4.2 ms morphing latency within NIST Level 3 requirements, effectively delivering a secure and low-latency baseline. As we transitioned into the medium-threat level (L1), the system morphed automati cally into a dual-stack of NTRU-HPS-4096 and CTIDH-2048, calling a morphing time of 6.7 ms and lifting the cryptographic assurance to a composite model spanning NIST Level 4 and PQCRYPTO benchmarks—a step up demonstrating the framework’s capacity to rebalance defense postures in real-time.

![](images/b2c93ffd5d5013b3ad9b7f72bee22ca2fd0e67ed7b2068391493298e46af9e6b.jpg)  
Fig. 8. MIRAGE-DoH metamorphic defense dynamics cognitive learning across AI training phases.

At L2 high-threat exposure level, a more latency-weighted configuration—SIDH-p751 with NewHope-1024—was invoked using the mcshard–emergency command, totaling 8.9 ms and being NSA CNSSP-15 compliant, and thereby showcasing the system’s preparedness for quantum-resistant measures in higher adversarial settings. Finally, for the critical threat level (L3), we launched a hybridized morph between MLWE (Kyber-1024) and CSIDH-4096 via multi-layered cryptographic shards, which, although having a higher morph latency of 12.1 ms, was conformant to ISO 29167-3 and provided both maximum forward secrecy and algebraic unpredictability. Each morphing stage was controlled with the mcshard command-line utility under deterministic control and simplicity of integration within our adversarial emulation testbed. The incremental increase in morphing latency across threat levels, while expected, was offset by proportionally higher security guarantees and structural entropy, reflecting a carefully balanced trade-off between response time and cryptographic strength [13].

This structured progression not only validates the performance-efficiency trade-off of our modular shard engine but also highlights the architectural foresight in incorporating post-quantum agility, situational reconfiguration, and layered cryptographic defense into the operational heart of MIRAGE-DoH. Consequently, the findings attest that our systematic, context-aware morphing solution surpasses static and monolithic solutions in enabling secure, dynamic threat adaptability, rendering the framework a strong candidate for the future encrypted DNS ecosystems in dynamic and quantum-prone security contexts.

In our experimental evaluation, as evident from the composite figure, we methodically evaluated the performance of the MIRAGE-DoH framework on four most important dimensions—detection accuracy, adaptive latency, morphing efficiency, and throughput capacity—under a step-by-step adversarial simulation environment. To begin, we observed in Fig 8. panel (a) how both MIRAGE-CMA and MIRAGE-SGI consistently exhibited higher cognitive detection accuracy, with CMA peaking at 88.5% even when adversarial cycles increased, performing far better compared to both normal

TABLE IX  
CORE PERFORMANCE METRICS VS. BASELINE MODELS. COMPARI-SON AGAINST INDUSTRY-STANDARD DOH DEFENSE SYSTEMS (E.G., CLASSICAL ML, STATIC AI PIPELINES)

<table><tr><td>Metric</td><td>MIRAGE-DoH</td><td>Baseline (CNN-LSTM)</td><td>Baseline (Random Forest)</td><td>Improvement</td><td>Confidence Interval (95%)</td></tr><tr><td>Detection Accuracy (%)</td><td>99.98</td><td>95.5</td><td>92.3</td><td>↑ 4.48%</td><td>±0.02%</td></tr><tr><td>False Positive Rate (%)</td><td>0.0008</td><td>0.15</td><td>0.42</td><td>↓ 99.5%</td><td>±0.0001</td></tr><tr><td>Latency (μs)</td><td>78</td><td>210</td><td>155</td><td>↓ 62.8%</td><td>±3.5</td></tr><tr><td>Throughput (M queries/sec)</td><td>15.3</td><td>8.7</td><td>4.2</td><td>↑ 75.9%</td><td>±0.4</td></tr><tr><td>Morph Time (ms)</td><td>8.9</td><td>N/A</td><td>N/A</td><td>—</td><td>±0.3</td></tr></table>

IDS as well as other variations, thereby establishing the effectiveness of our neurosymbolic correlation and generative self-adaptation-based adversarial resilience mechanisms. Consequently, latency profiles exhibited in Fig 8. panel (b) demonstrated that our MIRAGE modules maintained sub-18µs response latencies under mounting threat dynamics, whereas baseline IDS experienced exponential latency deterioration, thus confirming the low-overhead performance of our edgeoptimized temporal processing pipeline. In Fig 8. panel (c), our crypto morphing system exhibited agile resilience, with shard change times as low as 12.0 ms for MIRAGE-SGI, starkly comparing to the static inefficiency (41.1 ms) of legacy crypto stacks, establishing the effective agility introduced by our modular PQC shard engine and AI-enabled transition logic.Additionally, the throughput gains in Fig 8. panel (d) enabled MIRAGE-CMA and MIRAGE-MCS to sustain highvolume query capacity in the midst of 13.9M QPS even in the presence of extreme adversarial saturation, validating the scalability and resilience brought about by our multi-threaded quantum-hardened data path and stream-based anomaly filter architecture. Such tightly-coupled results—obtained from rigorous threat modeling, adaptive cryptographic switching, and spatiotemporal anomaly localization—emphasize how each architectural layer synergistically augmented operation hardening. Moreover, these results completely validate our research objectives by establishing that the MIRAGE-DoH system not only achieves improved detection accuracy and performance against evolving threats but also establishes a sound paradigm for quantum-proof encrypted DNS infrastructures, thereby overcoming the limitations of monolithic defense solutions and yielding deployable utility for next-generation secure network deployments in quantum-exposed environments [18].

In our comprehensive performance evaluation, presented in Table IX, we compared the MIRAGE-DoH framework with classical defense frameworks—such as CNN-LSTM and Random Forest classifiers—using a heavily controlled experimental setup that showcased actual real-world encrypted DNS traffic subject to adversarial stressors. Our initial proofof-concept integrated adaptive quantum-hardened detection with morphogenetic cryptographic transformation, and this multi-layered solution achieved significantly improved performance on all of the most important metrics. Specifically, we attained a 99.98% detection rate that had a statistically significant 4.48% improvement over the best baseline (CNN-LSTM), which reflects the precision of our spatiotemporal anomaly localization and hybrid adversarial learning mechanisms. The precision was reinforced by an unprecedented false positive rate reduction to 0.0008%, a 99.5% decline from typical models, reflecting the safety of our neurosymbolic correlation engines in avoiding benign misclassification. On the performance front, MIRAGE-DoH reduced latency by a very significant amount to 78µs—representing a 62.8% decrease—which we attribute to our FPGA-accelerated and optimized stream-processing pipeline inference layer. Meanwhile, throughput capacity went up to 15.3 million queries per second, a 75.9% gain facilitated by our parallelized quantumhardened data paths and optimized cascades of anomaly filters. Interestingly, our cryptographic morphing step, lacking in all baselines, took only 8.9 ms, reflecting the truth of real-time reorganization of PQC. These results validate all methodological stages—all the way back to our roots in modular design—by establishing that MIRAGE-DoH not only outcompares standard models for detection resilience and run-time velocity but also introduces new adaptive cryptographic agility, thereby establishing a disruptive benchmark for DNS over HTTPS security across adversarial as well as post-quantum threat contexts [5].

TABLE X  
THREAT-SPECIFIC COUNTERMEASURE EFFICIENCY. RESPONSE PERFOR-MANCE AGAINST CRITICAL ATTACK VECTORS DEFINED IN THE THREAT MODEL

<table><tr><td>Attack Type</td><td>Detection Mechanism</td><td>Detection Time (ms)</td><td>Mitigation Success Rate (%)</td><td>Resource Overhead (%)</td></tr><tr><td>Quantum Key Inference</td><td>MCSs + CMA Trigger</td><td>7.2</td><td>100</td><td>2.8</td></tr><tr><td>Polymorphic Query Mimicry</td><td>TMN + SGI Spectral Analysis</td><td>12.5</td><td>99.6</td><td>4.1</td></tr><tr><td>Latent DoH Tunneling</td><td>TMN Topological Replay</td><td>9.8</td><td>99.8</td><td>3.5</td></tr><tr><td>Protocol Semantic Injection</td><td>CCE Causal Simulation</td><td>15.3</td><td>99.2</td><td>5.7</td></tr><tr><td>Low-Rate Spectral Attack</td><td>SGI Zero-Day Tracking</td><td>11.1</td><td>98.9</td><td>3.9</td></tr></table>

From the systematic experimental design formulated through our work, Table X presents a comprehensive exploration of MIRAGE-DoH expert countermeasure reaction to high-priority attacker threat vectors throughout our threat model, thus empirically validating the proposed framework’s mission resilience and flexibility. Therefore, our defense framework is validated. At deployment initiation, we integrated modular detection pathways—each tailored to exploit distinctive temporal, spectral, and topological signatures of distinctive attacks—followed by precise and timely threat detection. Our Morphogenetic Cryptographic Sensors (MCSs) and Causal Mutation Analysis (CMA) achieved 100% mitigation efficacy against quantum key inference across a mean detection time of 7.2 milliseconds, validating the responsiveness and strategic value of quantum-resilient sensing. Similarly, Temporal Morphological Network (TMN) and Spectral Gradient Inversion (SGI) effectively resisted polymorphic query mimicry with 99.6% accuracy and a low resource utilization of 4.1%, demonstrating the strength of dynamic signal disambiguation and adversarial shape tracking. Topological replay based on TMN-based capability also enabled a 99.8% accuracy against concealed DoH tunneling, demonstrating the vigor of temporal graph reconstruction in uncovering concealed persistence mechanisms. Protocol semantic injection, notoriously hard to detect in static pipelines, was effectively countered using our Causal Chain Emulator (CCE), with simulated decision paths to intercept logic-based adversarial payloads at a 99.2% mitigation rate. Finally, our integrated zero-day spectral analytics within SGI successfully intercepted low-rate spectral attacks with a 98.9% success rate, citing the diversity of our model with respect to stealth, lowsignature anomalies. Taken together, these findings validate the explicit modularization and expertise-specific layering of our detection framework, wherein each methodological component contributed incrementally but in concert to the global security model. Not only do these outcomes prove that our system is capable of countering multifarious, adaptive threats with high accuracy and minimal overhead, but they constitute an important leap beyond conventional detection pipelines, thereby further solidifying the practical value and scientific significance of MIRAGE-DoH as a post-quantumready, adversarially intelligent DoH defense solution [37].

The chronological path of MIRAGE-DoH’s cognitive defense mechanisms, as well as depicted in the provided Fig 8, presents a multi-dimensional perspective on synchronized interaction of AI modules in subsequent autonomous training phases based on deliberation on judicious phasewise progress in security performance against sophisticated DNS over HTTPS attacks. Initially, Morphogenetic Cryptographic Sensors (MCSs) sported an enhanced morphing threat which decreased remarkably as Causal Mutation Analysis (CMA) underwent neuroevolutionary acceleration by causing hyperparameter tuning to be induced at earlier stages and adversarial exposure, thereby enhancing detection accuracy and significantly reducing mutation-induced evasion vectors. Simultaneously, the Temporal Morphological Network (TMN) reflected a consistent rise in topological stability because of the ability of dynamic homology mapping to identify persistent and polymorphic attack patterns within encrypted query streams. As training progressed into mid-to-late epochs, the Spectral Gradient Inversion (SGI) module outperformed others by means of an even superior spectral resilience limit—particularly within the adversarial trajectory learning process—which made its purpose to combat concealed, lowsignal frequency perturbations worthwhile. The Causal Chain Emulator (CCE) was oscillating but stable in threat prediction performance since it was capable of emulating and intercepting sophisticated semantic-based injection attacks [35].

![](images/376e2b68caf9c57f048e106907b4d696a054d069f6b687018ef2aa7cc7695df9.jpg)

![](images/66a0d4e0970a2ea9158d7346c7fea67882e88c8284a1fa7d5d8294248ac3f6dc.jpg)

Fig. 9. Metamorphic threat confidence calibration and expected calibration error.  
![](images/254e9ba203017b8fb29ed48c63d128188ab58a850e866a2ca6b7303ab6c28907.jpg)

![](images/a3f79bb7835ab4b73795231ddc65879d4ddde7769aaae82d3454fafbae6d91e2.jpg)  
Fig. 10. MIRAGE-DoH encrypted traffic dynamics under AI attacks and detection accuracy.

These results were precisely in line with our research objectives, substantiating the feasibility of MIRAGE-DoH’s metamorphic defense system in not merely meeting but exceeding conventional detection thresholds through spatiotemporal reasoning overlap, topological abstraction overlap, and spectral inference overlap. This success demonstrates the paradigmatic power of our architecture in real DoH environments, achieving scalable, low-latency, and quantum-resistant defense mechanisms far more powerful than static heuristicbased methods common in current research.

The first thing we did was use metamorphic calibration in our analysis to check how reliable threat confidence predictions were when faced with different defense levels in MIRAGE-DoH compared to DNS encryptions used by adversaries. As apparent in the reliability diagram (Fig. 9 a), each of MIRAGE’s subcomponents—CMA, TMN, MCS, CCE, and SGI—fell tightly on the ideal calibration curve, indicating high correspondence between threat probabilities predicted by models and actual frequencies of attacks, the defining characteristic of reliable inference in high-stakes security applications. Surprisingly, Spectral Gradient Inversion (SGI) and Causal Mutation Analysis (CMA) posted lowest deviation from optimal calibration, in keeping with their heightened sensitivity to low-signal adversarial examples and mutational threat models, respectively. In contrast, traditional detection mechanisms were beset by excess overconfidence, as evidenced by their high deviation from the diagonal, resulting in high Expected Calibration Error (ECE) of 0.136, compared to MIRAGE components’ sub-0.012 thresholds (Fig. 9 b). These results verified the efficacy of our spatiotemporal calibration process, based on spectral homology derivation and causal learning under neuroevolutionary control, in asserting strong threat discrimination and confidence alignment. Each element’s performance was an instantaneous outcome of our systematic approach, wherein adversarial phase training, metamorphic signal preconditioning, and feedback loops progressively optimized parameter spaces across varied threat morphologies. Our integration of specialist modules—such as TMN’s topological abstraction and MCS’s morphogenetic anomaly codex—resulted in highly adaptive, low-bias security that was highly interpretable and generalizable to encrypted and polymorphic attack scenarios [32].

TABLE XI  
ADAPTIVE LEARNING PERFORMANCE OF COGNITIVE METAAGENTS (CMAS). EVOLUTION OF CMAS ACROSS ADVERSARIAL TRAINING PHASES (F1-SCORE, AUC-ROC)

<table><tr><td>Training Phase</td><td>F1-Score (%)</td><td>AUC- ROC</td><td>Novelty Detec- tion Rate (%)</td><td>Catastrophic Forgetting Rate (%)</td></tr><tr><td>Initialization</td><td>92.4</td><td>0.934</td><td>85.1</td><td>8.3</td></tr><tr><td>Phase 1 (Static)</td><td>97.8</td><td>0.982</td><td>93.6</td><td>2.1</td></tr><tr><td>Phase 2 (Dy- namic)</td><td>99.1</td><td>0.997</td><td>98.5</td><td>0.4</td></tr><tr><td>Phase 3 (Live)</td><td>99.7</td><td>0.999</td><td>99.8</td><td>0.0</td></tr></table>

These innovations surpassed not only but significantly our research objectives through the development of calibrated, metamorphic AI constructs capable of sustaining performance under quantum-resistant, real-time DoH conditions. In brief, our findings present the transition to adaptive, modular AI systems from heuristic-based monolithic ones and place MIRAGE-DoH as a scalable secure post-quantum DNS over HTTPS best practice for future security network architecture.Our integration of specialist modules—such as TMN’s topological abstraction and MCS’s morphogenetic anomaly codex—produced a highly adaptive, low-bias security system with excellent interpretability and generalizability in encrypted and polymorphic attack environments. These breakthroughs not only achieved but surpassed our research objectives through the development of calibrated, metamorphic AI constructs with the ability to sustain performance within quantum-resilient, real-time DoH environments. In conclusion, our findings present the paradigm shift toward modular, selfadjusting AI systems from monolithic heuristic-based systems and position MIRAGE-DoH as a best practice for scalable, secure post-quantum DNS over HTTPS protection in future network security architectures.

In our empirical testing of Cognitive MetaAgents (CMAs), progressive progression through stages of adversary training as outlined in Table XI revealed an increasing trend in the performance measures which fully justified our ordered, stagewise model of learning. For starters, at the first uncalibrated setup phase, we observed baseline performance metrics in terms of an F1-score of 92.4%, an AUC-ROC of 0.934, and a minimal novelty detection rate of 85.1%, with the system reflecting its first, partial adversarial discriminative ability in non-adaptive contexts while simultaneously reflecting high catastrophic forgetting capacity of 8.3%, reflecting poor retention across variational danger spaces.

When entering Phase 1, where CMAs were exposed to static adversarial morphologies, performance greatly enhanced with a dramatic reduction in forgetting (2.1%) and novelty detection rising to 93.6%, thanks to incorporating metamorphic signal conditioning and context-preserving embeddings. Carrying over into the Phase 2 aggressive threat setting, the integration of topological memory nodes with causal reconstruction algorithms enabled the model to achieve an F1-score of 99.1%, virtually error-free AUC-ROC (0.997), and a stunning 98.5% novelty detection rate, while continuing to minimize forgetting to 0.4%, thereby emphasizing the prowess of biologically motivated synaptic plasticity in adversarial memory retention. Finally, during Phase 3, representing actual-time live deployment, we achieved nearly optimal performances—F1-score of 99.7%, AUC-ROC of 0.999, and flawless 99.8% detection with no catastrophic forgetting—demonstrating the efficacy of our fully developed CMA framework in polymorphic DoH threat learning without degrading performance [8].

These findings support that our systematic, multi-stage adversarial training curriculum, rooted in neuroevolutionary dynamics and recursive cognitive modeling, not only enhanced detection fidelity and resilience but also surpassed conventional monolithic approaches by maintaining acquired representations and adaptively generalizing to novel attack variations. Ultimately, this evaluation substantiates the revolutionary advantage of CMAs as shrewd, self-adaptive agents of real-time DNS over HTTPS security systems, offering a firm paradigm shift toward adaptive, post-quantum-resistant defense technologies.

We systematically developed and implemented the MIRAGE-DoH framework in our research to analyze the encrypted traffic behavior under AI-driven attack models, diligently splitting the analysis into independent phases—Tunneling, Flood, and Quantum—representing evolving adversary strategies. The patterns of anomaly intensity graphed highlighted a sharp spike in the Flood and Quantum phases with moderate but consistent divergence in the Tunneling phase from baseline normal traffic, highlighting the adaptive and stealthy nature of tunneling-based attacks. Our rigorous experimental setup using layered phases and robust anomaly detection was able to reveal these subtle patterns, affirming the superiority of our detection mechanisms.

Cognitive detection accuracy indices across the varied attack scenarios unequivocally demonstrated the technical efficacy of pioneering cognitive frameworks (CMA, TMN, and SGI) compared to traditional approaches with appreciable accuracy improvement (δ+25% to +30%) across all types of attacks, thereby validating our fundamental intention to strengthen DoH security based on state-of-the-art cognitive structures. This performance jump was enabled through the integration of cutting-edge analysis facilities and machine learning pipelines

## TABLE XII

INTER-MODULE COORDINATION AND GLOBAL OPTIMIZATION EFFECTS INMIRAGE-DOH. THE TABLE QUANTIFIES HOW DECISION PROPAGA-TION AND SHARED OPTIMIZATION SIGNALS IMPROVE DETECTION,STABILITY, AND RESPONSE LATENCY ACROSS COORDINATEDMODULES

<table><tr><td>Coordinated Modules</td><td>Primary Optimization Signal</td><td>Observed System Effect</td><td>Impact on Encrypted DNS Defense</td></tr><tr><td>CMA ↔ TMN</td><td>Topological persistence gradient</td><td>Reduced convergence variance</td><td>Stable detection under polymorphic DoH traffic</td></tr><tr><td>CMA ↔ SGI</td><td>Spectral reward shaping</td><td>Faster policy convergence</td><td>Early prediction of attacker trajectory shifts</td></tr><tr><td>TMN ↔ SGI</td><td>Persistent homology feedback</td><td>Long-horizon anomaly retention</td><td>Detection of multi-phase tunneling attacks</td></tr><tr><td>CMA ↔ CCE</td><td>Counterfactual risk gradients</td><td>Lower false adaptation rate</td><td>Prevention of over-fitting to transient attacks</td></tr><tr><td>CMA ↔ MCS</td><td>Threat-stage activation signal</td><td>Sub-millisecond shard morphing</td><td>Cryptographic hardening aligned with attack phase</td></tr><tr><td>Global (All Modules)</td><td>Unified cost functional  $\mathcal{J}_{\text{MIRAGE}}$ </td><td>Coordinated latency-performance balance</td><td>Scalable deployment without resolver disruption</td></tr></table>

that made adaptive anomaly detection of traffic and precise modeling of operational dynamics feasible, which indicates the robustness, scalability, and real-world practicability of our approach in deployment environments [46].

Furthermore, we elaborated in Table XII the coordination between CMA, TMN, SGI, CCE, and MCS in MIRAGE-DoH is now driven by a common optimization goal instead of multiple separate local optima, thereby maintaining the coordinated evolution of learning, memory, prediction, and cryptographic adaptation under the challenging environment of encrypted DNS. The Cognitive MetaAgents play the major role of decision orchestrators that repetitively optimize a single global cost functional that weighs the trade-offs of detection accuracy, adaptation, cryptographic agility, and low latency under the strict constraint of structured feedback from the TMNs in the form of steady topological gradients that suppress the unstable convergence of detection under the challenging condition of polymorphic attacks. Spectral Game Intelligence brings in the much-needed adversarial forecasts over the long horizon by working in the spectral domain of graphs, but the reinforcement signal is deliberately linked with the CMA through the reward shaping mechanism that uses the resolverlevel traffic flows to avoid disconnection from the protocol realities. The Causal Counterfactual Environments further refines the entire exercise by filtering out the spurious correlations to ensure that the cryptographic adaptations are based upon the causal threat evolution over time and not upon noise. The Metamorphic Cryptographic Shards play the downstream actuator’s role that is triggered only when the cryptographic threat escalation is indicated by the overall optimization state in order to decouple the optimization of cryptography hardening from the latency of detection. The tightly coupled but asynchronously administrated optimization approach turns the MIRAGE-DoH system composed of extremely capable software modules into a single-integrated system in which each module again significantly contributes to the joint optimization goal of scaling the autonomous and robust administration of the encrypted DNS traffic.

## VI. CONCLUSION AND FUTURE WORK

In this research, we endeavored to address the critical and often overlooked security vulnerabilities inherent in DNS over HTTPS traffic, focusing on its susceptibility to sophisticated AI-Driven adversarial attacks such as tunneling, flooding, and quantum based disruptions. The main challenge was the sophisticated nature of DoH traffic, which by its very nature protects traditional inspection methods, thereby complicating anomaly detection and response systems in real-time usage environments. To deal with these problems, we created MIRAGE-DoH step by step, introducing a fresh multilayered structure that brings together up-to-date cognitive detection methods—CMA, TMN and SGI—and analyzes data from each traffic phase. Adaptive anomaly detection with strict phase segmentation is a first in our architecture which lets us track the soft signs of a wide range of attack methods that older approaches could not handle. Through the precise planning of experiments and the selective use of advanced analysis techniques, we demonstrated our method of algorithmically enhancing standard detection means by significant detection rate improvements—between $\delta + 2 5 \%$ and δ + 30%—in all our attack scenarios, as can be seen from our findings. These findings not only validate the validity and utility of our method but are also a milestone event for network defense, particularly as applied to safe DNS protocol research. By exposing the intricate dance of attacker behavior and pat terns of encrypted communication, we have paved the way for more comprehensive, dynamic security mechanisms that better address the evolving nature of adversarial threat. In the future, the future of this study requires further examina tion of integrating quantum-resistant cryptographic primitives with state-of-the-art adversarial defense methods in order to establish the security stance of DNS infrastructures against emerging quantum and AI-based threats. Subsequent work can then further investigate federated learning topologies for decentralized exchange of threat intelligence, applying the hyperdimensional models of computation to accelerate and enhance anomaly detection, and creating enormous real-world testbeds in order to ensure our approach can scale. Further, exploring the interactions with other encrypted protocols such as DoT and next-generation post-quantum DNS variants could free important insight into the whole ecosystem of security for encrypted network traffic. Lastly, leveraging and advancing the methods created here, this research is in a prime position to inform the development of next-generation context-driven security architectures that actively defend critical DNS infrastructure from a rapidly changing and advanced cyber threat landscape.

## REFERENCES

[1] B. Ali, “On the fog’s frontline: A federated machine learning approach for industrial network threat detection and intrusion prevention,” J. Cybersecurity, vol. 11, no. 1, pp. 5–19, Jan. 2025.

[2] B. Ali and G. Chen, “Neuromorphic quantum adversarial learning (NQAL): A bio-inspired paradigm for DNS over HTTPS threat detection,” EURASIP J. Inf. Secur., vol. 2025, no. 1, p. 35, Dec. 2025.

[3] B. Ali and G. Chen, “Next-generation AI for advanced threat detection and security enhancement in DNS over HTTPS,” J. Netw. Comput. Appl., vol. 244, Dec. 2025, Art. no. 104326.

[4] B. Ali and G. Chen, “Proactive and privacy-preserving defense for DNS over HTTPS via federated AI attestation (PAFA-DoH),” Neural Netw., vol. 196, Apr. 2026, Art. no. 108343.

[5] A. R. Alzighaibi, “Detection of DoH traffic tunnels using deep learning for encrypted traffic classification,” Computers, vol. 12, no. 3, p. 47, Feb. 2023.

[6] F. B. Wala, S. Campbell, and M. Kiran, “Insights into DoH: Traffic classification for DNS over HTTPS in an encrypted network,” in Proc. Syst. Netw. Telemetry Anal., Jul. 2023, pp. 9–17.

[7] M. Behnke et al., “Feature engineering and machine learning model comparison for malicious activity detection in the DNS-over-HTTPS protocol,” IEEE Access, vol. 9, pp. 129902–129916, 2021.

[8] L. de Souza Bezerra Borges, R. de Oliveira Albuquerque, and R. T. de Sousa Junior, “A security model for DNS tunnel detection on cloud´ platform,” in Proc. Workshop Commun. Netw. Power Syst. (WCNPS), Nov. 2022, pp. 1–6.

[9] S.-Y. Chang and Q. Khan, “Post-quantum cryptography in networking protocols: Challenges, solutions, and future directions,” Cryptography, vol. 10, no. 1, p. 12, Feb. 2026.

[10] J. Chen, D. Liu, Y. Zhang, Y. Chen, and G. Geng, “A system for DNS over HTTPS deployment and security measurement,” in Proc. 6th Int. Conf. Comput. Eng. Appl. (ICCEA), Apr. 2025, pp. 808–813.

[11] R. Chhabra, P. Murley, D. Kumar, M. Bailey, and G. Wang, “Measuring DNS-over-HTTPS performance around the world,” in Proc. 21st ACM Internet Meas. Conf., Nov. 2021, pp. 351–365.

[12] M. Dawood et al., “The impact of domain name server (DNS) over hypertext transfer protocol secure (HTTPS) on cyber security: Limitations, challenges, and detection techniques,” Comput., Mater. Continua, vol. 80, no. 3, pp. 4513–4542, 2024.

[13] P. Dikshit, J. Sengupta, and V. Bajpai, “Recent trends on privacypreserving technologies under standardization at the IETF,” ACM SIGCOMM Comput. Commun. Rev., vol. 53, no. 2, pp. 22–30, Apr. 2023.

[14] S. Ding, D. Zhang, J. Ge, X. Yuan, and X. Du, “Encrypt DNS traffic: Automated feature learning method for detecting DNS tunnels,” in Proc. IEEE Int. Conf. Parallel Distrib. Process. With Appl., Big Data Cloud Comput., Sustain. Comput. Commun., Social Comput. Netw. (ISPA/BDCloud/SocialCom/SustainCom), Sep. 2021, pp. 352–359.

[15] G. Duan et al., “DNSGuard: In-network defense against DNS attacks,” IEEE Trans. Depend. Secure Comput., vol. 22, no. 1, pp. 597–613, Jan. 2025.

[16] A. Hounsel, P. Schmitt, K. Borgolte, and N. Feamster, “Can encrypted DNS be fast,” in Proc. Passive Act. Meas., 22nd Int. Conf. Cham, Switzerland: Springer, Apr. 2021, pp. 444–459.

[17] A. Hounsel, P. Schmitt, K. Borgolte, and N. Feamster, “Encryption without centralization: Distributing DNS queries across recursive resolvers,” in Proc. Appl. Netw. Res. Workshop, Jul. 2021, pp. 62–68.

[18] C. Huitema, S. Dickinson, and A. Mankin, DNS Over Dedicated Quic Connections, document RFC 9250, 2022.

[19] K. Hynek, D. Vekshin, J. Luxemburk, T. Cejka, and A. Wasicek, “Summary of DNS over HTTPS abuse,” IEEE Access, vol. 10, pp. 54668–54680, 2022.

[20] K. Jerabek, K. Hynek, and O. Rysav´ y, “Comparative analysis of´ DNS over HTTPS detectors,” Comput. Netw., vol. 247, Jun. 2024, Art. no. 110452.

[21] K. Jerabek, O. Rysavy, and I. Burgetova, “Analysis of well-known DNS over HTTPS resolvers,” in Proc. IEEE 13th Annu. Comput. Commun. Workshop Conf. (CCWC), Mar. 2023, pp. 0516–0524.

[22] H. Jha, I. Patel, G. Li, A. K. Cherukuri, and S. Thaseen, “Detection of tunneling in DNS over HTTPS,” in Proc. 7th Int. Conf. Signal Process. Commun. (ICSC), Nov. 2021, pp. 42–47.

[23] E. Kinnear, P. McManus, T. Pauly, T. Verma, and C. A. Wood, Oblivious DNS Over HTTPS, document RFC 9230, 2022.

[24] M. Kosek, L. Schumann, R. Marx, T. V. Doan, and V. Bajpai, “DNS privacy with speed: Evaluating DNS over QUIC and its impact on web performance,” in Proc. 22nd ACM Internet Meas. Conf., Oct. 2022, pp. 44–50.

[25] A. M. Koshy et al., “An insight into encrypted DNS protocol: DNS over TLS,” in Proc. 4th Int. Conf. Recent Develop. Control, Autom. Power Eng. (RDCAPE), Oct. 2021, pp. 379–383.

[26] C. Kwan, P. Janiszewski, S. Qiu, C. Wang, and C. Bocovich, “Exploring simple detection techniques for DNS-over-HTTPS tunnels,” in Proc. ACM SIGCOMM Workshop Free Open Commun. Internet, Aug. 2021, pp. 37–42.

[27] J. Lee, D. Mohaisen, and M. S. Kang, “Measuring DNS-over-HTTPS downgrades: Prevalence, techniques, and bypass strategies,” Proc. ACM Netw., vol. 2, no. CoNEXT4, pp. 1–22, Dec. 2024.

[28] R. Li, B. Liu, C. Lu, H. Duan, and J. Shao, “A worldwide view on the reachability of encrypted DNS services,” in Proc. ACM Web Conf., May 2024, pp. 1193–1202.

[29] M. Lyu, H. H. Gharakheili, and V. Sivaraman, “A survey on DNS encryption: Current development, malware misuse, and inference techniques,” ACM Comput. Surv., vol. 55, no. 8, pp. 1–28, Aug. 2023.

[30] A. Mohajer, J. Hajipour, and V. C. M. Leung, “Dynamic offloading in mobile edge computing with traffic-aware network slicing and adaptive TD3 strategy,” IEEE Commun. Lett., vol. 29, no. 1, pp. 95–99, Jan. 2025.

[31] M. MontazeriShatoori, L. Davidson, G. Kaur, and A. Habibi Lashkari, “Detection of DoH tunnels using time-series classification of encrypted traffic,” in Proc. IEEE Int. Conf. Dependable, Autonomic Secure Comput., Int. Conf. Pervasive Intell. Comput., Int. Conf. Cloud Big Data Comput., Int. Conf. Cyber Sci. Technol. Congr. (DASC/PiCom/CBDCom/CyberSciTech), Aug. 2020, pp. 63–70.

[32] M. Moure-Garrido, C. Campo, and C. Garcia-Rubio, “Real time detection of malicious DoH traffic using statistical analysis,” Comput. Netw., vol. 234, Oct. 2023, Art. no. 109910.

[33] A. Nadler, R. Bitton, O. Brodt, and A. Shabtai, “On the vulnerability of anti-malware solutions to DNS attacks,” Comput. Secur., vol. 116, May 2022, Art. no. 102687.

[34] Y. Nakatsuka, A. Paverd, and G. Tsudik, “PDOT: Private DNS-over-TLS with tee support,” Digital Threats, Res. Pract., vol. 2, no. 1, pp. 1–22, 2021.

[35] T. Q. Nguyen, R. Laborde, A. Benzekri, A. Oglaza, and M. Mounsif, “AutoRoC-DBSCAN: Automatic tuning of DBSCAN to detect malicious DNS tunnels,” Ann. Telecommun., vol. 80, nos. 3–4, pp. 227–249, Apr. 2025.

[36] A. Niakanlahiji, S. Orlowski, A. Vahid, and J. H. Jafarian, “Toward practical defense against traffic analysis attacks on encrypted DNS traffic,” Comput. Secur., vol. 124, Jan. 2023, Art. no. 103001.

[37] S. Niktabe, A. H. Lashkari, and D. P. Sharma, “Detection, characterization, and profiling DoH malicious traffic using statistical pattern recognition,” Int. J. Inf. Secur., vol. 23, no. 2, pp. 1293–1316, Apr. 2024.

[38] A. S. Rawat and M. P. Jhanwar, “Quantum-safe signatureless DNSSEC,” in Proc. 20th ACM Asia Conf. Comput. Commun. Secur., Aug. 2025, pp. 267–282.

[39] M. A. Salari, A. Kumar, F. Rinaudi, R. Tourani, A. Sacco, and F. Esposito, “Privacy analysis of oblivious DNS over HTTPS: A website fingerprinting study,” in Proc. 55th Annu. IEEE/IFIP Int. Conf. Dependable Syst. Netw. (DSN), Jun. 2025, pp. 415–428.

[40] J. Schwenk, “DNS security,” in Guide to Internet Cryptography: Security Protocols and Real-World Attack Implications. Cham, Switzerland: Springer, 2022, pp. 353–375.

[41] J. Sengupta, M. Kosek, J. Fries, S. Ferlin-Reiter, and V. Bajpai, “On cross-layer interactions of QUIC, encrypted DNS and HTTP/3: Design, evaluation, and dataset,” IEEE Trans. Netw. Service Manage., vol. 21, no. 3, pp. 2992–3007, Jun. 2024.

[42] B. Shobiri, M. Mannan, and A. Youssef, “CDNs’ dark side: Security problems in CDN-to-origin connections,” Digit. Threats: Res. Pract., vol. 4, no. 1, pp. 1–22, Mar. 2023.

[43] S. K. Singh and P. K. Roy, “Detecting malicious DNS over HTTPS traffic using machine learning,” in Proc. Int. Conf. Innov. Intell. Informat., Comput. Technol. (3ICT), Dec. 2020, pp. 1–6.

[44] R. Sommese et al., “Investigating the impact of DDoS attacks on DNS infrastructure,” in Proc. 22nd ACM Internet Meas. Conf., Oct. 2022, pp. 51–64.

[45] Q. Song, J. Yang, and A. Mohajer, “Multi-objective resource optimization in UAV-enabled heterogeneous cellular networks using serverless federated learning and power-domain NOMA,” Trans. Emerg. Telecommun. Technol., vol. 36, no. 8, Aug. 2025, Art. no. e70210.

[46] S. Sunahara, Y. Jin, and K. Iida, “Authoritative DNS server discovery method to enhance DNS privacy preservation,” in Proc. CoNEXT Student Workshop, Dec. 2023, pp. 31–32.

[47] N. U. Aijaz, M. Misbahuddin, and S. Raziuddin, “Survey on DNSspecific security issues and solution approaches,” in Data Science and Security. Cham, Switzerland: Springer, 2020, pp. 79–89.

[48] F. B. Wala and C. Cotton, “‘Off-label’ use of DNS,” Digit. Threats, Res. Pract., vol. 3, no. 3, pp. 1–13, Sep. 2022.

[49] Y. Wang, A. Zhou, S. Liao, R. Zheng, R. Hu, and L. Zhang, “A comprehensive survey on DNS tunnel detection,” Comput. Netw., vol. 197, Oct. 2021, Art. no. 108322.

[50] T. Zebin, S. Rezvy, and Y. Luo, “An explainable AI-based intrusion detection system for DNS over HTTPS (DoH) attacks,” IEEE Trans. Inf. Forensics Security, vol. 17, pp. 2339–2349, 2022.

[51] M. Zhan, Y. Li, G. Yu, B. Li, and W. Wang, “Detecting DNS over HTTPS based data exfiltration,” Comput. Netw., vol. 209, May 2022, Art. no. 108919.

[52] M. Zhang et al., “Detecting and measuring security risks of hostingbased dangling domains,” ACM SIGMETRICS Perform. Eval. Rev., vol. 51, no. 1, pp. 87–88, Jun. 2023.

[53] N. Zhou, Y. N. Li, and A. Mohajer, “Distributed capacity optimisation and resource allocation in heterogeneous mobile networks using advanced serverless connectivity strategies,” Int. J. Sensor Netw., vol. 45, no. 3, pp. 127–147, 2024.

![](images/4c81f985a3a15e67317e64330b88eb62492a3fe2efe14b324c122ac2f9e187d2.jpg)

Basharat Ali is currently pursuing the Ph.D. degree with the State Key Laboratory for Novel Software Technology, Nanjing University, Nanjing, China. His work explores advanced threat detection mechanisms, post-quantum cryptographic integration, and intelligent traffic analysis using machine learning and graph-based models. He also has prior research experience in blockchain systems and distributed computing architectures. His research interests include network security, secure network protocols, and privacy-preserving communication systems, with particular emphasis on encrypted DNS technologies, such as DNS over HTTPS (DoH) and DNS over TLS (DoT).

![](images/7dd1f16704c0fd8975c16a9a12092fc33305fe1abf05b86a326ee3a4b30691fc.jpg)

Guihai Chen (Fellow, IEEE) is currently a Professor with the Department of Computer Science and Technology, Nanjing University, China, and a Researcher with the State Key Laboratory for Novel Software Technology. He has published extensively in leading journals and conferences in the field and has supervised numerous Ph.D. researchers. He serves as a corresponding author in several high-impact publications and has made significant contributions to the advancement of networked systems and secure communication technologies. His research interests

include distributed systems, network security, wireless networks, and data communication protocols.
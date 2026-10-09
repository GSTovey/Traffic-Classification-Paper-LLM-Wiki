# Robust Transceiver Design for SIM-Assisted Integrated Sensing and Covert Communications

Ahmed M. Benaya, Member, IEEE, Ali A. Nasir, Senior Member, IEEE, Khaled M. Rabie, Senior Member, IEEE, A. Abdelaziz Salem, and Daniel B. da Costa, Senior Member, IEEE

Abstract—Stacked intelligent metasurfaces (SIMs) have emerged as a promising wave-domain processing technology for sixth-generation integrated sensing and communication networks, reducing reliance on complex radio-frequency hardware. Nevertheless, imperfect channel state information (CSI) can compromise sensing performance and communication reliability. Moreover, ensuring covert transmission introduces a further challenge, as the system must sense potential targets while concealing communication activity from unauthorized wardens. These challenges motivate the development of robust SIM-assisted integrated sensing and covert communication (ISACC) systems. In this paper, we investigate the robust transceiver design of a multi-user, multi-target ISACC system under imperfect CSI. We jointly optimize the transmit and receive beamformers, sensing covariance matrix, and SIM phase shifts to maximize the worst-case minimum sensing signal-to-interference-plus-noise ratio. The formulation enforces constraints on bounded channel uncertainties, user qualityof-service requirements, transmit-power budget, SIM phase shifts, and target detection probabilities. Since the formulated problem is highly non-convex, we develop an alternating optimization framework based on the S-procedure, successive convex approximation, and semidefinite relaxation. Furthermore, to reduce computational complexity, we derive exact lowerdimensional representations of the robust sensing linear matrix inequalities (LMIs) involved in transmit/receive-beamformer designs. We further develop a low-complexity phase-update method that avoids the large sensing LMIs. Numerical results demonstrate that the proposed design outperforms random phase shift and fully digital-beamforming benchmarks, while the low-complexity scheme achieves comparable performance to the LMI-based scheme at substantially lower computational cost.

Index Terms—Stacked intelligent metasurfaces, integrated sensing and communication, covert communication, imperfect channel state information, robust design.

## I. Introduction

IXTH-generation (6G) wireless networks are expected S <sub>to support ultra-high data rate communication and</sub> advanced sensing services within a shared infrastructure, which requires flexible control of wireless signals and eficient use of hardware resources [1]. Although large antenna arrays provide greater spatial degrees of freedom (DoF), fully digital implementations incur substantial hardware costs and power consumption due to the large number of radio frequency (RF) chains [2]. Stacked intelligent metasurfaces (SIMs) have emerged as a promising technology to address these challenges. A SIM consists of multiple programmable metasurface layers, each comprising numerous meta-atoms that manipulate electromagnetic waves as they propagate through the structure [3]– [5]. By adjusting the phase shifts of individual metaatoms, SIMs perform beamforming directly in the wave domain, ofering fine control over signal propagation while significantly reducing reliance on complex RF hardware.

Such wave-domain processing capabilities can be particularly beneficial for integrated sensing and communication (ISAC). ISAC has emerged as a core paradigm for 6G networks to enable radar sensing and wireless communications over shared spectrum, hardware platforms, and transmitted waveforms [6], [7]. Through wave-domain beamforming, a SIM can flexibly shape transmitted signals to simultaneously serve communication users and illuminate sensing targets [8]. However, coordinating these dual functions requires balancing distinct operational requirements, where communication relies on high signal quality at user terminals, while sensing depends on the strength of target echoes relative to interference and noise. Moreover, since in multi-target scenarios, unwanted target echoes can severely degrade detection accuracy, joint transmit and receive beamforming provides an efective mechanism to manage this interference. Hence, sensing signal-to-interference-plus-noise ratio (SINR) serves as a suitable design metric that directly reflects the sensing performance [9].

In addition to these performance requirements, security is an essential consideration in ISAC systems. Since directing energy toward targets for sensing can increase their exposure to transmitted signals, such targets may also act as unauthorized observers that attempt to detect or intercept communication signals [10]. In contrast to conventional physical-layer security schemes that focus on degrading the received signal strength at malicious targets [11], covert communication aims to conceal the presence of communication activity through limiting the detection probability at malicious sensing targets [12]. Incorporating covertness into SIM-assisted ISAC therefore requires careful control of the signals reaching both legitimate users and wardens. This task becomes more challenging under imperfect channel state information (CSI), where the channel estimation errors can weaken desired signals, increase interference, and cause violations of communication or covertness requirements. These challenges motivate a robust SIM-assisted ISAC design that jointly accounts for sensing, communication, and covertness under channel uncertainty.

## A. Related Work

Stacked metasurfaces were first proposed in [3] to exploit multi-layer wave-domain processing and address the physical limitations of conventional single-layer architectures in order to significantly reduce RF chain requirements. Subsequent studies expanded the framework to account for discrete phase shifts and joint power allocation to maximize multi-user sum rates [4], [5]. SIMassisted communication has also been investigated in nearfield and wideband scenarios. In particular, near-field beamfocusing designs exploited the additional distancedependent spatial DoF to suppress inter-user interference [13], [14], while layer-by-layer SIM optimization was combined with digital precoding and power allocation to support multi-user transmission under frequency-selective channels and practical phase-tuning errors in wideband systems [15]. In addition, to improve solution quality and reduce optimization cost, recent works have considered deep reinforcement learning (DRL)-based phase and power optimization, as well as refined alternating optimization (AO) and projected-gradient methods [5], [16]. Nevertheless, these works have mainly focused on rate-oriented metrics and relied on perfect CSI, leaving the critical vulnerability of channel estimation uncertainty largely unaddressed.

Recent studies have extended SIM technology to ISAC systems. A SIM-assisted downlink system with multiple communication users and a radar target has been investigated in [8]. They jointly optimized the SIM phase shifts and transmit power allocation to maximize the spectral eficiency under a sensing-power constraint. In [17], the authors considered a transmit beamforming design that balances the communication sum rate and the normalized sensing beampattern. They developed a dual-normalized diferential gradient method to solve the resulting nonconvex problem. A discrete phase shift-based SIM design has been studied along with transmit power optimization in [18]. Their AO approach uses variable separation and projection-based updates to manage multi-user interference and improve the sensing beam gain. In [19], Wang et al. have considered multi-user SIM-assisted ISAC with an extended target, where they jointly optimized the transmit beamformer and the end-to-end SIM response to minimize the Cramér-Rao bound under user-SINR and transmit-power constraints. Their method combines AO and semidefinite relaxation (SDR) and is also supported by experimental results. Although these studies demonstrate the potential of SIMs for ISAC, they have not explicitly considered CSI uncertainty errors or the joint transmit/receive beamforming design.

By providing additional wave-domain DoF without requiring extra RF chains, SIMs can improve secure transmission by directing information signals toward intended users and controlling leakage toward unintended receivers. Building on this capability, the works in [20], [21] investigate secure single-input-single-output (SISO) transmission and jointly design the SIM phase shifts, transmit signals, and artificial noise to enhance secrecy performance. These secrecy-based methods protect the message content by limiting an eavesdropper’s ability to decode it. Covert communication provides a diferent form of protection by hiding the existence of the transmission itself. This capability is especially important in ISAC, where sensing signals illuminate potential targets that may also monitor the communication activity. Along this direction, [22] studies covert ISAC with SIMs and uses DRL to jointly optimize the transmit power and SIM phase shifts under sensing and covert-communication constraints. In a complementary study, [23] develops a robust covert ISAC system using a fully digital BS without any configurable surface assistance. Although the former does not consider CSI uncertainty, the latter does not exploit SIM-enabled wave-domain processing, leaving robust SIMassisted covert ISAC largely unexplored.

## B. Motivation and Main Contributions

The reviewed literature reveals several important limitations. Existing SIM-assisted ISAC studies are mainly developed for nominal CSI and use sensing power, beampattern gain, or the Cramér-Rao bound as sensing metrics. They do not jointly optimize the transmit and receive beamformers to suppress interference among multiple sensing targets. Moreover, the security-oriented SIM studies have considered secrecy in simple SISO links or covert ISAC using DRL. More recently, robust multiuser downlink beamforming for SIMs with imperfect CSI and finite-resolution phase shifts was investigated in [24], whereas robust covert ISAC using fully digital beamforming was considered in [23]. The former does not include sensing or security constraints, while the latter does not exploit metasurface-assisted wave-domain processing. Hence, the joint design of SIM-assisted sensing, communication, and covertness under channel uncertainty remains largely unexplored. Although integrating SIM into covert ISAC significantly improves secure communication and sensing performance, it poses severe mathematical challenges in guaranteeing quality-of-service (QoS) and covertness due to the tight coupling among multi-layer phase shifts, digital transmit/receive beamformers, and CSI estimation errors. Compared to the literature, the key contributions of our work, summarized in Table I, are detailed as follows:

TABLE I  
Comparison of Our Work with Existing SIM-Assisted and ISAC Wireless Systems

<table><tr><td>Contribution</td><td>[8]</td><td>[13]</td><td>[14]</td><td>[15]</td><td>[16]</td><td>[17]</td><td>[18]</td><td>[19]</td><td>[22]</td><td>[23]</td><td>[24]</td><td>Our paper</td></tr><tr><td>Wave-domain processing</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td></td><td>√</td><td>√</td></tr><tr><td>Multi-user communication</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td></tr><tr><td>ISAC functionality</td><td>√</td><td></td><td></td><td></td><td></td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td></td><td>√</td></tr><tr><td>Multi-target sensing</td><td></td><td></td><td></td><td></td><td></td><td>√</td><td></td><td></td><td>√</td><td>√</td><td></td><td>√</td></tr><tr><td>Covert communication</td><td></td><td></td><td>√</td><td></td><td></td><td></td><td></td><td></td><td>√</td><td>√</td><td></td><td>√</td></tr><tr><td>Imperfect CSI / Robust design</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>√</td><td>√</td><td>√</td></tr><tr><td>Joint Tx and Rx beamforming</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>√</td><td></td><td>√</td></tr><tr><td>Low-complexity / Dimension-reduction</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>√</td></tr></table>

• We propose a robust transceiver design framework for a multi-user, multi-target SIM-assisted ISACC system under imperfect CSI. By jointly optimizing the transmit/receive beamformers, sensing covariance matrix, and SIM phase shifts, the proposed design maximizes the worst-case minimum sensing SINR while satisfying communication QoS, transmit power budgets, SIM phase constraints, and warden detection-probability bounds.

• To tackle the severe non-convexity caused by CSI uncertainties and the tight coupling among transmit/receive beamformers and multi-layer SIM phase shifts, we develop an AO framework, where the original problem is decoupled into three sub-problems; receive beamforming, transmit beamforming, and SIM phase shift optimization. The S-procedure is leveraged to convert the bounded channel uncertainties into tractable linear matrix inequalities (LMI) deterministic constraints.

• We derive exact lower-dimensional representations of the robust sensing LMIs arising in the transmit- and receive-beamformer sub-problems, thereby reducing their computational dimensions without introducing additional approximation. Moreover, we propose a low-complexity SIM phase-update method based on norm bounds that substantially reduces the computational cost associated with the LMI-based phaseupdate formulation.

• Numerical results show that the proposed design outperforms random phase shift and conventional digital-beamforming benchmarks. They also demonstrate that the low-complexity phase-update method achieves performance close to the LMI-based design with considerably lower computational complexity.

The remainder of the paper is organized as follows: the SIM-assisted multi-user multi-target ISACC system model, communication and sensing models, covertness metric, and channel model are presented in Section II. Section III presents the robust max-min sensing SINR problem formulation. The proposed AO problem solution is shown in IV. Simulation results and discussions are presented in Section V. Finally, Section VI concludes the paper.

## II. System Model

![](images/6366118cc07a7cdbc9043b0e341d96fdbb46cbf30a0f31963f1472913ba2aad8.jpg)  
Fig. 1. SIM-assisted multi-user multi-target integrated sensing and covert communication system.

As shown in Fig. 1, we consider a SIM-enabled ISACC system, where a BS equipped with a uniform linear array (ULA) of $N _ { t }$ transmit antennas and $N _ { r }$ receive antennas serving K single-antenna covert users while simultaneously sensing Q potential eavesdropping targets. A SIM composed of L layers is deployed in front of the BS to perform wave-domain beam manipulation for both communication and sensing functionalities, where each layer contains M passive meta-atoms. Let $\mathcal { K } = \{ 1 , 2 , \ldots , K \} , \mathcal { Q } =$ $\{ 1 , 2 , \ldots , Q \} , \ : N _ { t } = \{ 1 , 2 , \ldots , N _ { t } \} , \ : N _ { r } = \{ 1 , 2 , \ldots , N _ { r } \}$ ， $\mathcal { L } = \{ 1 , 2 , \ldots , L \}$ , and $\mathcal { M } = \{ 1 , 2 , \dots , M \}$ denote the index sets of covert UEs, eavesdropping targets, transmit antennas, receive antennas, SIM layers, and meta-atoms per layer, respectively.

## A. SIM Model

Each layer of the stacked intelligent metasurface (SIM) is configured as a rectangular uniform planar array (UPA) with $M = M _ { x } \times M _ { z }$ elements, where $M _ { x }$ and $M _ { z }$ denote the numbers of elements along the x- and z-axes, respectively. Based on the Rayleigh–Sommerfeld difraction formulation [25], [26], the propagation coeficient between the m˜ -th element of the $( l \mathrm { ~ - ~ } 1 ) { \cdot } \mathrm { t h }$ layer and the m-th element of the l-th layer, for all $m , \tilde { m } \in \mathcal { M }$ and $l \in { \mathcal { L } } ,$ , is given by

$$
\omega_ {m, \tilde {m}} ^ {l} = \frac {A _ {e} \cos (\chi_ {m , \tilde {m}} ^ {l})}{r _ {m , \tilde {m}} ^ {l}} \left(\frac {1}{2 \pi r _ {m , \tilde {m}} ^ {l}} - j \frac {1}{\lambda}\right) e ^ {j 2 \pi r _ {m, \tilde {m}} ^ {l} / \lambda},\tag{1}
$$

where $A _ { e }$ denotes the area of each element, $\chi _ { m , \tilde { m } } ^ { l }$ is the angle between the propagation direction and the surface normal of the (l −1)-th layer, $r _ { m , \tilde { m } } ^ { l }$ represents the distance between the two elements, and λ is the carrier wavelength.

The complex reflection coeficient of the m-th element in the l-th layer is represented as $e ^ { j \theta _ { m } ^ { l } }$ , for all $m \in \mathcal { M }$ and $l \in \mathcal L$ , where $\theta _ { m } ^ { l } \in [ 0 , 2 \pi )$ denote the reflection phase shift. Accordingly, the diagonal phase shift matrix of the l-th metasurface layer is

$$
\boldsymbol {\Theta} ^ {l} = \operatorname{diag} \left(e ^ {j \theta_ {1} ^ {l}}, e ^ {j \theta_ {2} ^ {l}}, \dots , e ^ {j \theta_ {M} ^ {l}}\right) \in \mathbb {C} ^ {M \times M}, \quad \forall l \in \mathcal {L}.\tag{2}
$$

Consequently, the overall forward SIM transfer matrix is

$$
\mathbf {G} = \boldsymbol {\Theta} ^ {L} \boldsymbol {\Omega} ^ {L} \dots \boldsymbol {\Theta} ^ {2} \boldsymbol {\Omega} ^ {2} \boldsymbol {\Theta} ^ {1} \boldsymbol {\Omega} _ {t} ^ {1} \in \mathbb {C} ^ {M \times N _ {t}},\tag{3}
$$

where $\Omega ^ { l } \in \mathbb { C } ^ { M \times M }$ for all $l \in \mathcal { L } \setminus \{ 1 \}$ denotes the interlayer propagation matrix from the $( l - 1 )$ -th layer to the l-th layer. The matrix $\Omega _ { t } ^ { 1 } \in \mathbb { C } ^ { M \times \dot { N } _ { t } }$ , which models the channel between the transmit antenna array and the first SIM layer, can be derived from (1) by replacing $r _ { m , \tilde { m } } ^ { l }$ and $\chi _ { m , \tilde { m } } ^ { l }$ with $r _ { m , n _ { t } } ^ { 1 }$ and $\boldsymbol { \chi } _ { m , n _ { t } } ^ { 1 }$ , respectively, for all $m \in { \mathcal { M } }$ and $n _ { t } \in \mathcal { N } _ { t }$

## B. Communication and Sensing Models

We consider a narrowband flat-fading downlink communication model and a narrowband monostatic radar model over a transmission block consisting of T symbol intervals, where $\mathcal { T } = \{ 1 , 2 , \hdots , T \}$ denotes the index set of symbol times. Let $\mathbf { x } [ t ] \ \in \ \mathbb { C } ^ { N _ { t } \times 1 }$ denote the complex-baseband transmit vector at symbol time t. The BS transmits K communication streams and a dedicated sensing signal $\mathbf { x } _ { 0 } [ t ] \in \mathbb { C } ^ { N _ { t } \times 1 }$ , which is modeled as an independent and identically distributed (i.i.d.) zero-mean complex Gaussian random vector across time slots, with covariance matrix $\mathbf { R } _ { 0 } \succeq 0 , \mathrm { i . e . , } x _ { 0 } [ t ] \sim \mathcal { C N } ( 0 , \mathbf { R } _ { 0 } )$

Let $\mathbf { s } [ t ] ~ \triangleq ~ [ s _ { 1 } [ t ] , s _ { 2 } [ t ] , \dots , s _ { K } [ t ] ] ~ \in ~ \mathbb { C } ^ { K \times 1 }$ be the i.i.d. zero-mean complex Gaussian communication symbol vector with $\mathbb { E } \{ { \bf s } [ t ] { \bf s } [ t ] ^ { \tilde { H } } \} = { \bf I } _ { K }$ and $\mathbf { w } _ { k } \in \mathbb { C } ^ { N _ { t } \times 1 }$ denote the digital communication beamforming vector toward the $k -$ th covert user. Hence, The transmit signal is modeled as

$$
\mathbf {x} [ t ] = \sum_ {k \in \mathcal {K}} \mathbf {w} _ {k} s _ {k} [ t ] + \mathbf {x} _ {0} [ t ].\tag{4}
$$

Assuming suficiently large $T ,$ , the transmit covariance matrix can be expressed as

$$
\mathbf {R} _ {x} \triangleq \mathbb {E} \bigl \{\mathbf {x} [ t ] \mathbf {x} [ t ] ^ {H} \bigr \} = \sum_ {k \in \mathcal {K}} \mathbf {w} _ {k} \mathbf {w} _ {k} ^ {H} + \mathbf {R} _ {0},\tag{5}
$$

where $\begin{array} { r } { { \bf R } _ { 0 } = \frac { 1 } { T } \sum _ { t \in \mathcal { T } } { \bf x } _ { 0 } [ t ] { \bf x } _ { 0 } [ t ] ^ { H } } \end{array}$ . Accordingly, the total power budget constraint is expressed as

$$
\operatorname{Tr} \left(\mathbf {R} _ {x}\right) = \sum_ {k \in \mathcal {K}} \| \mathbf {w} _ {k} \| ^ {2} + \operatorname{Tr} \left(\mathbf {R} _ {0}\right) \leq P _ {\max},\tag{6}
$$

where $P _ { \mathrm { m a x } }$ is the maximum allowed transmit power at the BS.

Let $\mathbf { h } _ { k } \in \mathbb { C } ^ { M \times 1 }$ denote the channel from the outermost SIM layer to covert user $k \in \mathcal { K }$ . The received signal at user k can be written as

$$
y _ {k} [ t ] = \mathbf {h} _ {k} ^ {H} \mathbf {G x} [ t ] + n _ {k} [ t ],\tag{7}
$$

where $n _ { k } [ t ] ~ \sim ~ \mathcal { C N } ( 0 , \sigma _ { k } ^ { 2 } )$ denotes the additive white Gaussian noise (AWGN) component at the k-th covert user. By substituting (4) into (7), we obtain

$$
\begin{array}{l} y _ {k} [ t ] = \underbrace {\mathbf {h} _ {k} ^ {H} \mathbf {G w} _ {k} s _ {k} [ t ]} _ {\text {desired}} + \underbrace {\sum_ {i \in \mathcal {K} , i \neq k} \mathbf {h} _ {k} ^ {H} \mathbf {G w} _ {i} s _ {i} [ t ]} _ {\text {multi - user interference}} \\ \quad + \underbrace {\mathbf {h} _ {k} ^ {H} \mathbf {G x} _ {0} [ t ]} _ {\text {sensing leakage}} + n _ {k} [ t ]. \end{array}\tag{8}
$$

Then, the downlink SINR at user k is given by

$$
\gamma_ {k} = \frac {| \mathbf {h} _ {k} ^ {H} \mathbf {G w} _ {k} | ^ {2}}{\sum_ {i \in \mathcal {K} , i \neq k} | \mathbf {h} _ {k} ^ {H} \mathbf {G w} _ {i} | ^ {2} + \mathbf {h} _ {k} ^ {H} \mathbf {G R} _ {0} \mathbf {G} ^ {H} \mathbf {h} _ {k} + \sigma_ {k} ^ {2}}.\tag{9}
$$

Let $\mathbf { a } _ { q } ~ \in ~ \mathbb { C } ^ { M \times 1 }$ denote the channel from the SIM’s outermost layer to the target $q \in \mathcal { Q }$ . The efective forward channel from the BS transmit array to target q is

$$
\mathbf {f} _ {1, q} \triangleq \mathbf {a} _ {q} ^ {H} \mathbf {G} \in \mathbb {C} ^ {1 \times N _ {t}}.\tag{10}
$$

To model the return path to the $N _ { r }$ -antenna BS receiver, we introduce a receive-side wave-domain transfer matrix I $\mathbf { 3 } \in \mathbb { C } ^ { M \times N _ { r } }$ from the BS receive array to the SIM aperture in the reverse direction. The efective return channel from target q to the BS receive array is

$$
\mathbf {f} _ {2, q} \triangleq \mathbf {B} ^ {H} \mathbf {a} _ {q} \in \mathbb {C} ^ {N _ {r} \times 1}.\tag{11}
$$

Consequently, the resulting round-trip MIMO channel matrix associated with the q-th target is expressed as

$$
\mathbf {F} _ {q} \triangleq \alpha_ {q} \mathbf {f} _ {2, q} \mathbf {f} _ {1, q} = \alpha_ {q} \mathbf {B} ^ {H} \mathbf {A} _ {q} \mathbf {G} \in \mathbb {C} ^ {N _ {r} \times N _ {t}},\tag{12}
$$

where $\alpha _ { q } \in \mathbb { C }$ denotes the scattering coeficient of the q-th target and ${ \mathbf { A } } _ { q } = { \mathbf { a } } _ { q } { \mathbf { a } } _ { q } ^ { H }$ is the round-trip channel between the SIM and the q-th target. Accordingly, the received echo signal at the BS is

$$
\mathbf {r} [ t ] = \sum_ {q \in \mathcal {Q}} \mathbf {F} _ {q} \mathbf {x} [ t ] + \mathbf {n} _ {B} [ t ],\tag{13}
$$

where $\mathbf { n } _ { B } [ t ] \sim \mathcal { C N } ( \mathbf { 0 } , \sigma _ { B } ^ { 2 } \mathbf { I } _ { N _ { r } } )$ is the AWGN component at the BS.

Let $\mathbf { u } _ { q } ~ \in ~ \mathbb { C } ^ { N _ { r } \times 1 }$ denote the receive beamformer for extracting target q. The corresponding observation is

$$
\hat {r} _ {q} [ t ] = \mathbf {u} _ {q} ^ {H} \mathbf {r} [ t ].\tag{14}
$$

Treating echoes from other targets as interference, the sensing SINR for target q is defined as

$$
\gamma_ {q} = \frac {\mathbf {u} _ {q} ^ {H} \mathbf {F} _ {q} \mathbf {R} _ {x} \mathbf {F} _ {q} ^ {H} \mathbf {u} _ {q}}{\sum_ {j \in \mathcal {Q} , j \neq q} \mathbf {u} _ {q} ^ {H} \mathbf {F} _ {j} \mathbf {R} _ {x} \mathbf {F} _ {j} ^ {H} \mathbf {u} _ {q} + \sigma_ {B} ^ {2} \| \mathbf {u} _ {q} \| ^ {2}}.\tag{15}
$$

## C. Covertness Metric and Detection Model

Following [27], [28], we adopt the detection error probability (DEP) as the metric to quantify covertness. Assuming equal prior probabilities, the DEP at target $q \in \mathcal { Q }$ is $\xi _ { q } \ \triangleq \ { P } _ { \mathrm { F A } , q } + { P } _ { \mathrm { M D } , q } ,$ where $P _ { \mathrm { F A } , q }$ and $P _ { \mathrm { M D } , q }$ denote the false-alarm and missed-detection probabilities, respectively. The signal received at the q-th target in the t-th symbol interval is modeled as

$$
y _ {q} [ t ] = \left\{ \begin{array}{l l} \mathbf {f} _ {1, q} \mathbf {x} _ {0} [ t ] + n _ {q} [ t ], & \mathcal {H} _ {0}, \\ \sum_ {k \in \mathcal {K}} \mathbf {f} _ {1, q} \mathbf {w} _ {k} s _ {k} [ t ] + \mathbf {f} _ {1, q} \mathbf {x} _ {0} [ t ] + n _ {q} [ t ], & \mathcal {H} _ {1}, \end{array} \right.\tag{16}
$$

where $\mathcal { H } _ { \mathrm { 0 } }$ represents the null hypothesis (no covert transmission) and $\mathcal { H } _ { 1 }$ denotes the alternative hypothesis (BS transmits covert signals). Moreover, $n _ { q } [ t ] \sim \mathcal { C N } ( 0 , \sigma _ { q } ^ { 2 } )$ denotes the AWGN component at the q-th target. Stacking the $T$ received signals over the transmission block yields the observation vector $\mathbf { y } _ { q } \triangleq [ y _ { q } [ 1 ] , y _ { q } [ 2 ] , \dots , y _ { q } [ T ] ] ^ { T }$ . Since the elements of $\mathbf { y } _ { q }$ are i.i.d. circularly-symmetric complex Gaussian random variables under each hypothesis, the likelihood functions are given by

$$
\begin{array}{l} \mathbb {P} _ {1, q} \triangleq p _ {\mathcal {H} _ {1}, q} (\mathbf {y} _ {q}) = \frac {1}{\pi^ {T} \delta_ {1 , q} ^ {T}} \exp \left(- \frac {\mathbf {y} _ {q} ^ {H} \mathbf {y} _ {q}}{\delta_ {1 , q}}\right), \\ \mathbb {P} _ {0, q} \triangleq p _ {\mathcal {H} _ {0}, q} (\mathbf {y} _ {q}) = \frac {1}{\pi^ {T} \delta_ {0 , q} ^ {T}} \exp \left(- \frac {\mathbf {y} _ {q} ^ {H} \mathbf {y} _ {q}}{\delta_ {0 , q}}\right), \end{array}\tag{17}
$$

where the variances $\delta _ { 0 , q } = \mathbf { f } _ { 1 , q } \mathbf { R } _ { 0 } \mathbf { f } _ { 1 , q } ^ { H } + \sigma _ { q } ^ { 2 }$ and $\delta _ { 1 , q } =$ $\begin{array} { r } { \sum _ { k \in \mathcal { K } } \vert \mathbf { f } _ { 1 , q } \mathbf { w } _ { k } \vert ^ { 2 } { + } \mathbf { f } _ { 1 , q } \mathbf { R } _ { 0 } \mathbf { f } _ { 1 , q } ^ { \bar { H } } + \sigma _ { q } ^ { 2 } . } \end{array}$ . Let $\xi _ { q } ^ { \star }$ denote the minimum achievable DEP at the q-th target with the optimal detector. As shown in [29], it satisfies

$$
\xi_ {q} ^ {\star} = 1 - \mathcal {V} _ {q} (\mathbb {P} _ {0, q}, \mathbb {P} _ {1, q}),\tag{18}
$$

where $\nu _ { q } ( \cdot , \cdot )$ is the total variation distance (TVD). Applying Pinsker’s inequality [23], [29], the TVD can be upper-bounded by the Kullback–Leibler (KL) divergence as

$$
\mathcal {V} _ {q} (\mathbb {P} _ {0, q}, \mathbb {P} _ {1, q}) \leq \sqrt {\frac {\mathcal {D} _ {q} (\mathbb {P} _ {1 , q} \| \mathbb {P} _ {0 , q})}{2}},\tag{19}
$$

where $\mathcal { D } _ { q } ( \mathbb { P } _ { 1 , q } \Vert \mathbb { P } _ { 0 , q } )$ denotes the KL divergence. For the i.i.d. complex Gaussian model in (17), the KL divergence admits the closed-form expression

$$
\mathcal {D} _ {q} (\mathbb {P} _ {1, q} \| \mathbb {P} _ {0, q}) = T \nu \left(\frac {\delta_ {1 , q} - \delta_ {0 , q}}{\delta_ {0 , q}}\right), \quad \nu (x) \triangleq x - \ln (1 + x).\tag{20}
$$

Therefore, ensuring a prescribed covertness level can be achieved by imposing

$$
\xi_ {q} ^ {\star} \geq 1 - \epsilon \iff \mathcal {D} _ {q} (\mathbb {P} _ {1, q} \| \mathbb {P} _ {0, q}) \leq 2 \epsilon^ {2}, \quad \forall q \in \mathcal {Q},\tag{21}
$$

where $\epsilon \in ( 0 , 1 )$ is a small constant controlling the desired covertness requirement.

## D. Channel Model with Bounded CSI Uncertainty

Rician fading is adopted to model the channels from the outermost SIM layer to the k-th covert user, h , i.e.,

$$
\mathbf {h} _ {k} = \sqrt {l _ {k}} \left(\sqrt {\frac {\kappa}{\kappa + 1}} \bar {\mathbf {h}} _ {k} + \sqrt {\frac {1}{\kappa + 1}} \tilde {\mathbf {h}} _ {k}\right), \quad \forall k \in \mathcal {K},\tag{22}
$$

where $\kappa ~ \geq ~ 0$ is the Rician factor and $l _ { k } ~ = ~ l _ { 0 } d _ { k } ^ { - \eta }$ is the large-scale fading coeficient with $d _ { k }$ denotes the propagation distance, where $\begin{array} { r } { l _ { 0 } = \left( \frac { \lambda } { 4 \pi } \right) ^ { 2 } } \end{array}$ is the free space path loss at a reference distance 1m and η is the path loss exponent. In addition, $\bar { \mathbf { h } } _ { k }$ denotes the deterministic line-ofsight $\mathrm { ( L o S ) }$ component, and $\tilde { \mathbf { h } } _ { k }$ is the non-LoS component with $\tilde { \mathbf { h } } _ { k } \ \sim \ \mathcal { C N } ( \mathbf { 0 } , \mathbf { R } _ { h _ { k } } )$ , where $\mathbf { R } _ { h _ { k } } \in \mathbb { C } ^ { M \times M }$ is the spatial correlation matrix that quantifies the correlation among the channels associated with diferent meta-atoms with $\begin{array} { r } { \mathbf { \tilde { \Gamma } } [ \mathbf { R } _ { h _ { k } } ] _ { m , m ^ { \prime } } = \operatorname { s i n c } \left( \frac { 2 \delta _ { m , m ^ { \prime } } } { \lambda } \right) } \end{array}$ , where $\delta _ { m , m ^ { \prime } }$ is the corresponding meta-atom spacing.

As stated previously, the SIM lies in the $x - z$ plane and consists of $M = M _ { x } \times M _ { z }$ elements. Here, $M _ { x } = 2 \tilde { M } _ { x } + 1$ denotes the number of elements along the x-axis, and $M _ { z } = 2 \tilde { M } _ { z } + 1$ denotes the number of elements along the z-axis. The corresponding element spacings in the x and z directions are $d _ { x }$ and $d _ { z }$ , respectively. When the user lies in the far field of the SIM aperture, the LoS component h<sup>¯</sup><sub>k</sub> can be represented according to [30] with $\bar { \mathbf { h } } _ { k } \ = \ \mathbf { a } _ { x } ( \vartheta _ { k } , \varphi _ { k } ) \otimes \mathbf { a } _ { z } ( \vartheta _ { k } , \varphi _ { k } ) \in \mathbb { C } ^ { M \times 1 }$ , where $( \vartheta _ { k } , \varphi _ { k } )$ denote the azimuth and elevation angles of the k-th covert user, respectively. Moreover, the array responses $\mathbf { a } _ { x } ( \vartheta _ { k } , \varphi _ { k } )$ and $\mathbf { a } _ { z } ( \vartheta _ { k } , \varphi _ { k } )$ are given by

$$
\begin{array}{r l} & {\mathbf {a} _ {x} (\vartheta_ {k}, \varphi_ {k})} \\ & {\quad = \left[ e ^ {- j \frac {2 \pi}{\lambda} \tilde {M} _ {x} d _ {x} \cos \vartheta_ {k} \sin \varphi_ {k}}, \ldots , e ^ {j \frac {2 \pi}{\lambda} \tilde {M} _ {x} d _ {x} \cos \vartheta_ {k} \sin \varphi_ {k}} \right] ^ {T},} \end{array}\tag{23}
$$

and

$$
\mathbf {a} _ {z} (\vartheta_ {k}, \varphi_ {k}) = \left[ e ^ {- j \frac {2 \pi}{\lambda} \tilde {M} _ {z} d _ {z} \cos \varphi_ {k}}, \dots , e ^ {j \frac {2 \pi}{\lambda} \tilde {M} _ {z} d _ {z} \cos \varphi_ {k}} \right] ^ {T}.\tag{24}
$$

Similarly, the SIM-to-target channel can be modeled as

$$
\mathbf {a} _ {q} = \sqrt {l _ {q}} \left(\mathbf {a} _ {x} (\vartheta_ {q}, \varphi_ {q}) \otimes \mathbf {a} _ {z} (\vartheta_ {q}, \varphi_ {q})\right) \in \mathbb {C} ^ {M \times 1}, \quad \forall q \in \mathcal {Q},\tag{25}
$$

where $\mathbf { a } _ { x } ( \vartheta _ { q } , \varphi _ { q } )$ and $\mathbf { a } _ { z } ( \vartheta _ { q } , \varphi _ { q } )$ can be expressed using (23) and (24) with $( \vartheta _ { q } , \varphi _ { q } )$ denoting the departure angles from the SIM towards the q-th target. In addition, $l _ { q } = l _ { 0 } d _ { q } ^ { - \eta }$ is the large-scale fading coeficient, where $d _ { q }$ denotes the propagation distance towards the q-th target.

To account for CSI imperfections, we adopt the bounded CSI model. Specifically, for each user k and target $q ,$ the actual channels are expressed as

$$
\mathbf {h} _ {k} = \hat {\mathbf {h}} _ {k} + \Delta \mathbf {h} _ {k}, \quad \| \Delta \mathbf {h} _ {k} \| _ {2} \leq \varepsilon_ {h _ {k}}, \quad \forall k \in \mathcal {K},\tag{26}
$$

$$
\mathbf {a} _ {q} = \hat {\mathbf {a}} _ {q} + \Delta \mathbf {a} _ {q}, \quad \| \Delta \mathbf {a} _ {q} \| _ {2} \leq \varepsilon_ {a _ {q}}, \quad \forall q \in \mathcal {Q},\tag{27}
$$

$$
\mathbf {A} _ {q} = \hat {\mathbf {A}} _ {q} + \Delta \mathbf {A} _ {q}, \quad \| \Delta \mathbf {A} _ {q} \| _ {F} \leq \varepsilon_ {A _ {q}}, \quad \forall q \in \mathcal {Q},\tag{28}
$$

where $\hat { \mathbf { h } } _ { k } , \hat { \mathbf { a } } _ { q } ,$ and $\hat { \mathbf { A } } _ { q }$ are the channel estimates available at the BS, while ∆h<sub>k</sub>, $\Delta { \bf a } _ { q } ,$ and $\Delta \mathbf { A } _ { q }$ represent unknown estimation errors. Although ${ \bf A } _ { q } = \bar { \bf a } _ { q } \mathbf { a } _ { q } ^ { H }$ in the nominal channel model, the forward channel estimate $\hat { \mathbf { a } } _ { q }$ and the efective round-trip channel estimate $\hat { \mathbf { A } } _ { q }$ are treated as separately estimated quantities to allow a mathematically tractable robust optimization.

## III. Robust Max–Min Sensing SINR Problem Formulation

In this section, we formulate the robust max–min sensing optimization problem for the proposed SIM-assisted covert ISAC system. The design is carried out under practical constraints including communication users $\mathrm { Q o S } ,$ total transmit power budget, and stringent covertness constraints that limit the detectability of covert transmissions at potential eavesdropping targets. Furthermore, to account for channel uncertainty, bounded CSI is incorporated, leading to a worst-case robust optimization framework.

Our objective is to jointly design the transmit communication beamformers $\{ \mathbf { w } _ { k } \} _ { k \in \mathcal K }$ , radar covariance matrix ${ \bf R } _ { 0 } \succeq { \bf 0 }$ , receive sensing beamformers $\{ \mathbf { u } _ { q } \} _ { q \in \mathcal { Q } }$ , and SIM wave-domain beamforming matrices $\{ \Theta ^ { l } \} _ { l \in \mathcal { L } }$ to maximize the minimum target sensing SINR. The resulting max–min sensing SINR problem is

$$
\max_{\{\mathbf{w}_{k}\} ,\mathbf{R}_{0},}\min_{q\in \mathcal{Q}}\min_{\| \Delta \mathbf{A}_{q}\|_{F}\leq \varepsilon_{A_{q}},\forall q\in \mathcal{Q}}\gamma_{q}\]\[\{\mathbf{u}_{q}\} ,\{\boldsymbol{\Theta}^{l}\}\tag{29a}
$$

$$
\mathrm{s.t.} \quad \gamma_ {k} \geq \Gamma_ {k}, \| \Delta \mathbf {h} _ {k} \| _ {2} \leq \varepsilon_ {h _ {k}}, \forall k \in \mathcal {K},\tag{29b}
$$

$$
\sum_ {k \in \mathcal {K}} \| \mathbf {w} _ {k} \| ^ {2} + \mathrm{Tr} (\mathbf {R} _ {0}) \leq P _ {\max},\tag{29c}
$$

$$
T \nu \left(\frac {\delta_ {1 , q} - \delta_ {0 , q}}{\delta_ {0 , q}}\right) \leq 2 \epsilon^ {2}, \| \Delta \mathbf {a} _ {q} \| _ {2} \leq \varepsilon_ {a _ {q}}, \forall q \in \mathcal {Q},\tag{29d}
$$

$$
\Theta^ {l} = \operatorname{diag} \left(e ^ {j \theta_ {1} ^ {l}}, \dots , e ^ {j \theta_ {M} ^ {l}}\right), | e ^ {j \theta_ {m} ^ {l}} | = 1, \forall l,\tag{29e}
$$

$$
\mathbf {R} _ {0} \succeq 0.\tag{29f}
$$

The constraints (29b) ensure a minimum quality-ofservice for each covert user, where $\Gamma _ { k } = 2 ^ { R _ { k } ^ { \mathrm { m i n } } } - 1$ and $R _ { k } ^ { \mathrm { m i n } }$ denotes the minimum rate requirement for the k-th covert user. These constraints couple the communication beamformers $\left\{ \mathbf { w } _ { k } \right\}$ , the radar covariance $\mathbf { R } _ { 0 }$ , and the SIM matrix G. Since increasing the sensing power, through ${ \bf R } _ { 0 }$ improves the sensing energy but degrades the user SINR due to additional interference, the total transmit power constraint (29c) creates a fundamental tradeof between communication beamforming power and sensing power allocation. Allocating more power to $\mathbf { R } _ { 0 }$ improves sensing and covertness but reduces the available power for user beamforming. The KL-divergence constraint (29d) limits the detection capability at each target.

The formulated optimization problem is highly nonconvex due to the fractional SINR expressions in both communication and sensing, coupling between SIM phase shift matrices in the SIM transfer matrix G, the unitmodulus constraints $| e ^ { j \theta _ { m } ^ { l } } | = 1$ , and the nonlinear KLdivergence covertness constraint. Before we dive into the problem solution, we first need to reformulate the problem into a more tractable form.

First, we recast the Max-Min sensing SINR problem by introducing the auxiliary variable ϱ such that $\gamma _ { q } \geq \varrho , \forall q \in$

Q, $\| \Delta A _ { q } \| _ { F } \le \varepsilon _ { A _ { q } }$ . Hence, problem (29) can be expressed as

$$
\max _ { \begin{array}{c} \{\mathbf {w} _ {k} \}, \mathbf {R} _ {0}, \varrho \\ \{\mathbf {u} _ {q} \}, \{\boldsymbol {\Theta} ^ {l} \} \end{array} } \varrho\tag{30a}
$$

$$
\mathrm{s.t.} \quad \gamma_ {q} \geq \varrho , \| \Delta \mathbf {A} _ {q} \| _ {F} \leq \varepsilon_ {A _ {q}}, \forall q \in \mathcal {Q},
$$

$$
(2 9 \mathrm{b}) - (2 9 \mathrm{f}).\tag{30b}
$$

(30c)

Then, we have to convert the semi-infinite quadratic constraints induced by bounded CSI into LMIs.

## Lemma 1. S-procedure for a quadratic constraint [31]

Define the quadratic functions in the variable $\mathbf { z } \in \mathbb { C } ^ { n \times 1 } \colon$

$$
f (\mathbf {z}) = \mathbf {z} ^ {H} \mathbf {A} \mathbf {z} + 2 \Re \{\mathbf {b} ^ {H} \mathbf {z} \} + c\tag{31}
$$

and

$$
g (\mathbf {z}) = \mathbf {z} ^ {H} \mathbf {C} \mathbf {z} + 2 \Re \{\mathbf {d} ^ {H} \mathbf {z} \} + e,\tag{32}
$$

where $\mathbf { A } , \mathbf { C } \in \mathbb { C } ^ { n \times n }$ are Hermitian, b, $\mathbf { d } \in \mathbb { C } ^ { n \times 1 }$ , and $c , e \in \mathbb { R }$ . The condition $( g ( \mathbf { z } ) \leq 0 \implies f ( \mathbf { z } ) \leq 0 )$ holds if and only if there exists a scalar $\mu \geq 0$ such that

$$
\mu \left[ \begin{array}{c c} \mathbf {C} & \mathbf {d} \\ \mathbf {d} ^ {H} & e \end{array} \right] - \left[ \begin{array}{c c} \mathbf {A} & \mathbf {b} \\ \mathbf {b} ^ {H} & c \end{array} \right] \succeq \mathbf {0}.\tag{33}
$$

In the following, we apply Lemma 1 to constraints (29b), (29d), and (30b). By substituting $\mathbf { h } _ { k } \ =$ $\hat { \mathbf { h } } _ { k } + \Delta \mathbf { h } _ { k }$ into $( 2 9 \mathrm { b } ) , \gamma _ { k } \ge \Gamma _ { k }$ is given by

$$
(\hat {\mathbf {h}} _ {k} + \Delta \mathbf {h} _ {k}) ^ {H} \mathbf {Q} _ {k} (\hat {\mathbf {h}} _ {k} + \Delta \mathbf {h} _ {k}) - \Gamma_ {k} \sigma_ {k} ^ {2} \geq 0, \quad \forall \| \Delta \mathbf {h} _ {k} \| _ {2} \leq \varepsilon_ {h _ {k}},\tag{34}
$$

where $\begin{array} { r l } { \mathbf { Q } _ { k } } & { \triangleq \hphantom { \mathbf { Q } _ { k } } \mathbf { \Lambda } \mathbf { G } \left( \mathbf { W } _ { k } - \Gamma _ { k } \sum _ { i \in \mathcal { K } , \ i \neq k } \mathbf { W } _ { i } - \Gamma _ { k } \mathbf { R } _ { 0 } \right) \mathbf { G } ^ { H } } \end{array}$ and $\mathbf { W } _ { i } = \mathbf { w } _ { i } \mathbf { w } _ { i } ^ { H } , \ \forall i \in \mathcal { K }$ . Expanding the quadratic term with respect to $\Delta \mathbf { h } _ { k }$ yields

$$
\Delta \mathbf {h} _ {k} ^ {H} \mathbf {Q} _ {k} \Delta \mathbf {h} _ {k} + 2 \Re \left\{\Delta \mathbf {h} _ {k} ^ {H} \mathbf {Q} _ {k} \hat {\mathbf {h}} _ {k} \right\} + \hat {\mathbf {h}} _ {k} ^ {H} \mathbf {Q} _ {k} \hat {\mathbf {h}} _ {k} - \Gamma_ {k} \sigma_ {k} ^ {2} \geq 0.\tag{35}
$$

Since the uncertainty set $\| \Delta \mathbf { h } _ { k } \| _ { 2 } \le \varepsilon _ { h _ { k } }$ is equivalently expressed as $\Delta \mathbf { h } _ { k } ^ { H } \Delta \mathbf { h } _ { k } - \varepsilon _ { h _ { k } } ^ { 2 } \leq 0$ , the constraint in (35) holds if and only if there exists a scalar $\mu _ { k } \geq 0$ such that

$$
\left[ \begin{array}{c c} \mu_ {k} \mathbf {I} + \mathbf {Q} _ {k} & \mathbf {Q} _ {k} \hat {\mathbf {h}} _ {k} \\ \hat {\mathbf {h}} _ {k} ^ {H} \mathbf {Q} _ {k} & \hat {\mathbf {h}} _ {k} ^ {H} \mathbf {Q} _ {k} \hat {\mathbf {h}} _ {k} - \Gamma_ {k} \sigma_ {k} ^ {2} - \mu_ {k} \varepsilon_ {h _ {k}} ^ {2} \end{array} \right] \succeq \mathbf {0}.\tag{36}
$$

Therefore, the original robust SINR requirement under norm-bounded channel uncertainty is equivalently transformed into the LMI in (36), which is convex with respect to the variables $\mathbf { W } _ { i } , \mathbf { R } _ { 0 }$ , and the auxiliary scalar $\mu _ { k }$

Regarding the robust covert constraint (29d), it can be equivalently expressed as

$$
\sum_ {k \in \mathcal {K}} | \mathbf {f} _ {1, q} \mathbf {w} _ {k} | ^ {2} - \varpi \mathbf {f} _ {1, q} \mathbf {R} _ {0} \mathbf {f} _ {1, q} ^ {H} \leq \varpi \sigma_ {q} ^ {2},\tag{37}
$$

where $\begin{array} { r l r } { \varpi } & { { } = } & { \nu ^ { - 1 } \left( \frac { 2 \epsilon ^ { 2 } } { T } \right) } \end{array}$ . Since $\begin{array} { r l r } { { \bf f } _ { 1 , q } } & { { } = } & { { \bf a } _ { q } ^ { H } { \bf G } } \end{array}$ , we have $\begin{array} { r l } { | \mathbf { f } _ { 1 , q } \mathbf { w } _ { k } | ^ { 2 } { = } } & { { } \mathbf { a } _ { q } ^ { \dot { H } } \mathbf { G } \mathbf { W } _ { k } \mathbf { G } ^ { H } \mathbf { a } _ { q } } \end{array}$ and $\begin{array} { r l } { { \bf f } _ { 1 , q } { \bf R } _ { 0 } { \bf f } _ { 1 , q } ^ { H } } & { { } = } \end{array}$ $\mathbf { a } _ { q } ^ { H } \mathbf { G } \mathbf { R } _ { 0 } \dot { \mathbf { G } ^ { H } } \mathbf { a } _ { q }$ . Therefore, constraint (29d) can be written as

$$
\mathbf {a} _ {q} ^ {H} \boldsymbol {\Xi} \mathbf {a} _ {q} \leq \varpi \sigma_ {q} ^ {2},\tag{38}
$$

where $\begin{array} { r } { \Xi \triangleq \mathbf { G } \left( \sum _ { k \in \mathcal { K } } \mathbf { W } _ { k } - \varpi \mathbf { R } _ { 0 } \right) \mathbf { G } ^ { H } } \end{array}$ . By substituting $\mathbf { a } _ { q } = \hat { \mathbf { a } } _ { q } + \Delta \mathbf { a } _ { q }$ and following the same S-procedure as previously done, the above semi-infinite constraint holds if there exists an auxiliary variable $\mu _ { q } \geq 0$ such that

$$
\left[ \begin{array}{c c} \mu_ {q} \mathbf {I} - \boldsymbol {\Xi} & - \boldsymbol {\Xi} \hat {\mathbf {a}} _ {q} \\ - \hat {\mathbf {a}} _ {q} ^ {H} \boldsymbol {\Xi} & \varpi \sigma_ {q} ^ {2} - \hat {\mathbf {a}} _ {q} ^ {H} \boldsymbol {\Xi} \hat {\mathbf {a}} _ {q} - \mu_ {q} \varepsilon_ {a _ {q}} ^ {2} \end{array} \right] \succeq \mathbf {0}.\tag{39}
$$

Hence, the original robust covertness constraint is equivalently transformed into the above LMI.

To handle the semi-infinite constraint (30b) induced by the uncertainties in $\{ \mathbf { A } _ { q } \} _ { q \in \mathcal { Q } } ,$ , we follow a similar reformulation procedure as in [23]. Since $\mathbf { F } _ { q } = \alpha _ { q } \mathbf { B } ^ { H } \mathbf { A } _ { q } \mathbf { G }$ we have

$$
\begin{array}{r l} & {\mathbf {u} _ {q} ^ {H} \mathbf {F} _ {j} \mathbf {R} _ {x} \mathbf {F} _ {j} ^ {H} \mathbf {u} _ {q} = | \alpha_ {j} | ^ {2} \mathbf {u} _ {q} ^ {H} \mathbf {B} ^ {H} \mathbf {A} _ {j} \mathbf {G R} _ {x} \mathbf {G} ^ {H} \mathbf {A} _ {j} ^ {H} \mathbf {B u} _ {q}} \\ & {\qquad = \mathrm{vec} (\mathbf {A} _ {j}) ^ {H} \mathbf {Y} _ {q, j} \mathrm{vec} (\mathbf {A} _ {j}),} \end{array}\tag{40}
$$

where $\mathbf { Y } _ { q , j } \triangleq | \alpha _ { j } | ^ { 2 } \bigg ( \big ( \mathbf { G } \mathbf { R } _ { x } \mathbf { G } ^ { H } \big ) ^ { T } \otimes \mathbf { B } \mathbf { U } _ { q } \mathbf { B } ^ { H } \bigg )$ , and ${ \bf U } _ { q } = { \bf \Psi }$ $\mathbf { u } _ { q } \mathbf { u } _ { q } ^ { H } .$

Then, the constraint $\gamma _ { q } \geq \varrho$ can be rewritten as

$$
\begin{array}{l} \sum_ {j   \in   \mathcal {Q}, j \neq q} \mathrm{vec} (\mathbf {A} _ {j}) ^ {H} \mathbf {Y} _ {q, j}   \mathrm{vec} (\mathbf {A} _ {j}) \\ - \frac {1}{\varrho} \mathrm{vec} (\mathbf {A} _ {q}) ^ {H} \mathbf {Y} _ {q, q}   \mathrm{vec} (\mathbf {A} _ {q}) + \sigma_ {B} ^ {2}   \mathrm{Tr} (\mathbf {U} _ {q}) \leq 0. \end{array}\tag{41}
$$

To obtain a single quadratic uncertainty constraint, we define $\hat { \mathbf { g } } _ { A } = \left\lceil \mathrm { v e c } ( \hat { \mathbf { A } } _ { 1 } ) ^ { T } , \dots , \mathrm { v e c } ( \hat { \mathbf { A } } _ { Q } ) ^ { T } \right\rceil ^ { T } \in \mathbb { C } ^ { \left( Q M ^ { 2 } \times 1 \right) }$ and $\Delta \mathbf { g } _ { A } = \left\lceil \mathrm { v e c } ( \Delta \mathbf { A } _ { 1 } ) ^ { T } , \dots , \mathrm { v e c } ( \Delta \mathbf { A } _ { Q } ) ^ { T } \right\rceil ^ { T } \in \mathbb { C } ^ { \left( Q M ^ { 2 } \times 1 \right) }$ where $\begin{array} { r } { \| \Delta \mathbf { g } _ { A } \| _ { 2 } ^ { 2 } \leq \sum _ { q \in \mathcal { Q } } \varepsilon _ { A _ { j } } ^ { 2 } } \end{array}$ . Then define the block diagonal matrix

$$
\mathbf {X} _ {q} = \operatorname{diag} \left(\mathbf {Y} _ {q, 1}, \dots , \mathbf {Y} _ {q, q - 1}, \mathbf {D} _ {q}, \mathbf {Y} _ {q, q + 1}, \dots , \mathbf {Y} _ {q, | \mathcal {Q} |}\right),\tag{42}
$$

where $\begin{array} { r } { \mathbf { D } _ { q } = - \frac { 1 } { \varrho } \mathbf { Y } _ { q , q } . } \end{array}$

Thus, the robust constraint is recast as

$$
\begin{array}{r l} & {\Delta \mathbf {g} _ {A} ^ {H} \mathbf {X} _ {q} \Delta \mathbf {g} _ {A} + 2 \Re \left\{\left(\mathbf {X} _ {q} \hat {\mathbf {g}} _ {A}\right) ^ {H} \Delta \mathbf {g} _ {A} \right\}} \\ & {\quad + \hat {\mathbf {g}} _ {A} ^ {H} \mathbf {X} _ {q} \hat {\mathbf {g}} _ {A} + \sigma_ {B} ^ {2} \operatorname{Tr} (\mathbf {U} _ {q}) \leq 0, \quad \forall \Delta \mathbf {g} _ {A}.} \end{array}\tag{43}
$$

By applying the S-procedure in Lemma 1, the above constraint holds if there exists $\mu _ { A _ { q } } \geq 0$ such that

$$
\left[ \begin{array}{c c} \mu_ {A _ {q}} \mathbf {I} - \mathbf {X} _ {q} & - \mathbf {X} _ {q} \hat {\mathbf {g}} _ {A} \\ - \hat {\mathbf {g}} _ {A} ^ {H} \mathbf {X} _ {q} & - \hat {\mathbf {g}} _ {A} ^ {H} \mathbf {X} _ {q} \hat {\mathbf {g}} _ {A} - \sigma_ {B} ^ {2}   \mathrm{Tr} (\mathbf {U} _ {q}) - \mu_ {A _ {q}} \sum_ {j \in \mathcal {Q}} \varepsilon_ {A _ {j}} ^ {2} \end{array} \right] \succeq \mathbf {0}.\tag{44}
$$

Therefore, the original semi-infinite sensing constraint can be suficiently replaced with the above LMI. Now, our optimization problem can be expressed as follows

$$
\max _ { \begin{array}{c} \{\mathbf {W} _ {k} \}, \mathbf {R} _ {0}, \varrho \\ \{\mathbf {U} _ {q} \}, \{\boldsymbol {\Theta} ^ {l} \} \end{array} } \varrho\tag{45a}
$$

$$
\text { s.t. } \quad (2 9 c), (2 9 e) - (2 9 f),\tag{45b}
$$

$$
(3 6), (3 9), (4 4).\tag{45c}
$$

## IV. Alternating Optimization-based Robust Max–Min Sensing SINR Problem Solution

Due to the coupled dependence of $\{ \mathbf { W } _ { k } \} , \mathbf { R } _ { 0 } , \{ \mathbf { U } _ { q } \}$ , and $\{ \Theta ^ { l } \}$ in (36), (39), and (44), problem (45) is non-convex and dificult to solve directly. To tackle this issue, we adopt an AO framework by partitioning the optimization variables into three blocks, namely the receive variables $\{ \mathbf { U } _ { q } \}$ the transmit variables $\{ \mathbf { W } _ { k } \} , \mathbf { R } _ { 0 }$ , and the SIM phase matrices $\{ \Theta ^ { l } \}$

## A. Receive Beamforming Vectors Optimization Subproblem

For fixed $\{ \mathbf { W } _ { k } \} , \mathbf { R } _ { 0 }$ , and $\{ \Theta ^ { l } \}$ , the receive-side matrices $\{ \mathbf { U } _ { q } \}$ only appear in $\mathbf { X } _ { q }$ through afine mappings. Therefore, the receive-side sub-problem can be expressed as

$$
\max _ {\{\mathbf {U} _ {q} \}, \varrho} \varrho\tag{46a}
$$

$$
\mathrm{s.t.} \quad \mathbf {U} _ {q} \succeq 0, \operatorname{Tr} (\mathbf {U} _ {q}) = 1, \quad \forall q \in \mathcal {Q},\tag{46b}
$$

$$
\operatorname{Rank} (\mathbf {U} _ {q}) = 1, \quad \forall q \in \mathcal {Q},\tag{46c}
$$

$$
(4 4)\tag{46d}
$$

Problem (46) is still non-convex due to the non-convex rank-one set of constraints Rank $( \mathbf { U } _ { q } ) = 1$ . Moreover, it is worth noting that the matrix $\mathbf { X } _ { q }$ contains the term $\mathbf { D } _ { q } =$ $- \frac { 1 } { \varrho } \mathbf { Y } _ { q , q } ,$ which makes the problem non-convex in $\{ \varrho , \bar { \bf U } _ { q } \}$ In order to handle the non-convex rank-one constraints $\mathrm { R a n k } ( \mathbf { U } _ { q } ) = 1$ , we use the following equivalence for any Hermitian positive semidefinite matrix $\mathbf { U } _ { q }$

$$
\operatorname{Rank} \left(\mathbf {U} _ {q}\right) = 1 \iff \operatorname{Tr} \left(\mathbf {U} _ {q}\right) - \lambda_ {\max} \left(\mathbf {U} _ {q}\right) = 0.\tag{47}
$$

This follows from the fact that $\operatorname { T r } ( \mathbf { U } _ { q } )$ equals the sum of all eigenvalues of $\mathbf { U } _ { q } ,$ whereas $\bar { \lambda _ { \operatorname* { m a x } } } ( \mathbf { U } _ { q } )$ is its largest eigenvalue. Since $\mathbf { U } _ { q } \mathbf { \Sigma } \subset \mathbf { 0 } , \ \mathrm { T r } ( \mathbf { U } _ { q } ) \mathbf { \Sigma } \geq \lambda _ { \operatorname* { m a x } } ( \mathbf { U } _ { q } )$ holds with equality if and only if only one eigenvalue is nonzero, i.e., when $\mathbf { U } _ { q }$ is rank one. Therefore, the rankone constraints can be replaced by introducing the penalty term $\begin{array} { r } { \left| \zeta _ { 1 } \sum _ { q \in \mathcal { Q } } \left( \operatorname { T r } ( \mathbf { U } _ { q } ) - \lambda _ { \operatorname* { m a x } } ( \mathbf { U } _ { q } ) \right) \right| } \end{array}$ into the objective function, where $\zeta _ { 1 } > 0$ is a penalty coeficient. Then, we adopt the successive convex approximation (SCA) to deal with the part $- \lambda _ { \operatorname* { m a x } } ( \mathbf { U } _ { q } )$ . In the r-th iteration, let ${ \bf v } _ { q } ^ { ( r ) }$ denote the dominant eigenvector of the current point $\mathbf { U } _ { q } ^ { ( \bar { r } ) }$ By the Rayleigh quotient inequality,

$$
\lambda_ {\mathrm{max}} (\mathbf {U} _ {q}) \geq (\mathbf {v} _ {q} ^ {(r)}) ^ {H} \mathbf {U} _ {q} \mathbf {v} _ {q} ^ {(r)},\tag{48}
$$

where $\lambda _ { \operatorname* { m a x } } ( \mathbf { U } _ { q } )$ is replaced by its afine lower bound. To remove the non-convexity caused by the reciprocal term <sup>1</sup><sub>ϱ</sub> in $\scriptstyle \mathbf { D } _ { q }$ , we introduce a new scalar auxiliary variable $\bar { \bar { \varrho } } \triangleq \frac { 1 } { \varrho } , \bar { \varrho } > 0$ such that ${ \bf D } _ { q } = - \bar { \varrho } { \bf Y } _ { q , q }$ . Additionally, we adopt a quasi-convex reformulation based on fixing ϱ¯ and applying a bisection search. Accordingly, the original problem can be solved by searching for the minimum ϱ¯ such that the resulting SDP is feasible. At each iteration, a candidate $\bar { \varrho }$ is tested by solving the corresponding SDP feasibility problem. If the problem is feasible, ϱ¯ is a valid upper bound; otherwise, it is a lower bound. Then, the interval is iteratively refined until convergence. Therefore, the optimal value $\varrho ^ { \star }$ is obtained as the smallest ϱ¯ for which the SDP is feasible, while the corresponding $\{ \mathbf { U } _ { q } \}$ are obtained from the final SDP solution. Accordingly, at the candidate $\bar { \varrho } ,$ the resulting SDP inner problem at the r-th iteration is given as

$$
\min _ {\{\mathbf {U} _ {q} \}} \quad \bar {\varrho} + \zeta_ {1} \sum_ {q \in \mathcal {Q}} \left(\mathrm{Tr} (\mathbf {U} _ {q}) - (\mathbf {v} _ {q} ^ {(r)}) ^ {H} \mathbf {U} _ {q} \mathbf {v} _ {q} ^ {(r)}\right)\tag{49a}
$$

$$
\begin{array}{l l} \text {s.t.} & (4 4), (4 6 b). \end{array}\tag{49b}
$$

The problem (49) is a convex SDP and can be eficiently solved using standard convex optimization solvers [32].

Since the robust sensing constraint (44) involves the matrix $\mathbf { X } _ { q } ,$ whose direct construction requires highdimensional Kronecker products, the direct implementation of the robust LMI sensing constraint adds extremely high computational complexity to the problem. In particular, recall that $\mathbf { Y } _ { q , j } \triangleq | \alpha _ { j } | ^ { 2 } \Big [ \big ( \mathbf { G } \mathbf { R } _ { x } \mathbf { \bar { G } } ^ { H } \big ) ^ { T } \otimes \mathbf { B } \mathbf { U } _ { q } \mathbf { B } ^ { H } \Big ]$ and that the matrix $\mathbf { X } _ { q }$ is constructed by stacking the matrices $\mathbf { Y } _ { q , j }$ in a block-diagonal manner. Hence, as $\mathbf { G } \mathbf { R } _ { x } \mathbf { G } ^ { H } \in \mathbb { C } ^ { M \times M }$ and $\mathbf { B } \mathbf { U } _ { q } \mathbf { B } ^ { H } \in \mathbb { C } ^ { M \times M }$ , each matrix $\mathbf { Y } _ { q , j }$ has dimension $M ^ { 2 } \times \dot { M } ^ { 2 }$ , whereas $\mathbf { X } _ { q }$ has dimension $Q M ^ { 2 } \times Q M ^ { 2 }$ . Consequently, the corresponding Sprocedure LMI has dimension $( Q M ^ { 2 } + 1 ) \times ( Q M ^ { 2 } + 1 )$ This excessive growth with the number of meta-atoms is computationally demanding in terms of both memory and processing complexity.

To significantly reduce the computational complexity while preserving the exact structure of the robust LMI, we present the following Proposition.

Proposition 1. The high-dimensional robust sensing LMI constraint (44) can be represented exactly in a lowerdimensional space as

$$
\left[ \begin{array}{c c} \mu_ {A _ {q}} \mathbf {I} - \widetilde {\mathbf {K}} _ {q} & - \widetilde {\mathbf {K}} _ {q} \widetilde {\mathbf {g}} _ {A} \\ - \widetilde {\mathbf {g}} _ {A} ^ {H} \widetilde {\mathbf {K}} _ {q} & - \widetilde {\mathbf {g}} _ {A} ^ {H} \widetilde {\mathbf {K}} _ {q} \widetilde {\mathbf {g}} _ {A} - \sigma_ {B} ^ {2}   \mathrm{Tr} (\mathbf {U} _ {q}) - \mu_ {A _ {q}} \sum_ {j \in \mathcal {Q}} \varepsilon_ {A _ {j}} ^ {2} \end{array} \right] \succeq \mathbf {0}.\tag{50}
$$

where $\widetilde { \mathbf { K } } _ { q } = \mathbf { R } _ { C } \mathbf { K } _ { q } \mathbf { R } _ { C } ^ { H } , \widetilde { \mathbf { g } } _ { A } = \mathbf { U } _ { C } ^ { H } \hat { \mathbf { g } } _ { A }$ , and $\mathbf { U } _ { C } , \mathbf { R } _ { C }$ are e eobtained from the compact QR factorization ${ \bf C } = { \bf U } _ { C } { \bf R } _ { C }$ of $\mathbf { C } = \operatorname { d i a g } \left( \mathbf { C } _ { 1 } , \ldots , \mathbf { C } _ { Q } \right)$ with $\mathbf { C } _ { j } = \left| \alpha _ { j } \right| \left( \mathbf { U } _ { G } ^ { * } \otimes \mathbf { B } \right)$

Proof: See the Appendix.

The dimension reduction itself is exact and does not introduce additional approximation into the robust LMI. In particular, instead of operating in the original space whose dimension grows proportionally to $Q M ^ { 2 }$ , the reduced LMI operates in a space whose dimension grows proportionally to $Q r _ { G } N _ { r }$ , where typically $r _ { G } \le N _ { t } \ll M$ This substantially reduces the computational and memory requirements.

B. Transmit Beamforming and Covariance Matrix Optimization Sub-problem

For fixed $\{ \mathbf { U } _ { q } \} , \forall q \in \mathcal { Q }$ and $\{ \Theta ^ { l } \} , \forall l \in \mathcal { L } ,$ the matrices $\mathbf { Q } _ { k } , \Xi$ , and $\mathbf { X } _ { q }$ become afine functions of $\{ \mathbf { W } _ { k } \} , \forall k \in \mathcal { K }$ and ${ \bf R } _ { 0 }$ . Hence, the resulting transmit beamforming and covariance optimization sub-problem is

$$
\max _ {\{\mathbf {W} _ {k} \}, \mathbf {R} _ {0}, \varrho} \varrho\tag{51a}
$$

$$
\text { s.t. } \quad \sum_ {k \in \mathcal {K}} \mathrm{Tr} (\mathbf {W} _ {k}) + \mathrm{Tr} (\mathbf {R} _ {0}) \leq P _ {\max},\tag{51b}
$$

$$
\mathbf {W} _ {k} \succeq 0, \forall k \in \mathcal {K},
$$

$$
\operatorname{Rank} \left(\mathbf {W} _ {k}\right) = 1, \forall k \in \mathcal {K},\tag{51c}
$$

$$
\mathbf {R} _ {0} \succeq 0,\tag{51d}
$$

$$
(3 6), (3 9), (4 4).\tag{51e}
$$

(51f)

Problem (51) is still non-convex due to the rankone constraint of the transmit beamforming matrices and due to the coupling between the variables ϱ and $\mathbf { W } _ { k }$ within the matrix $\mathbf { X } _ { q }$ through the term $\begin{array} { l l } { \mathbf { D } _ { q } } & { = } \end{array}$ $- \frac { 1 } { o } \mathbf { Y } _ { q , q } .$ To handle the non-convex rank-one constraints Rank $\mathbf { \partial } ( \mathbf { W } _ { k } ) = 1$ , we use the same procedures as in the receive beamforming matrices. Therefore, the rank-one constraints can be replaced by introducing the penalty term $\begin{array} { r } { \left\lceil \zeta _ { 2 } \sum _ { k \in \mathcal { K } } \left( \mathrm { T r } ( \mathbf { W } _ { k } ) - ( { \mathbf { v } _ { k } ^ { ( r ) } } ) ^ { H } \mathbf { W } _ { k } \mathbf { v } _ { k } ^ { ( r ) } \right) ^ { \top } \right\rceil } \end{array}$ into the objective function, where $\zeta _ { 2 } > 0$ is a penalty coeficient. In addition, we introduce the auxiliary variable $\bar { \varrho } \triangleq { \frac { 1 } { \rho } } , \bar { \varrho } > 0$ such that $\mathbf { D } _ { q } = - \bar { \varrho } \mathbf { Y } _ { q , q }$ and apply a bisection search over ϱ¯ as in the receive beamforming sub-problem. As a result, the convex surrogate problem at the r-th iteration is given by

$$
\min _ {\left\{\mathbf {W} _ {k} \right\}, \mathbf {R} _ {0}} \quad \bar {\varrho} + \zeta_ {2} \sum_ {k \in \mathcal {K}} \left(\operatorname{Tr} \left(\mathbf {W} _ {k}\right) - \left(\mathbf {v} _ {k} ^ {(r)}\right) ^ {H} \mathbf {W} _ {k} \mathbf {v} _ {k} ^ {(r)}\right)\tag{52a}
$$

$$
\begin{array}{l l} \text {s.t.} & (5 1 \mathrm{b}), (5 1 \mathrm{c}), (5 1 \mathrm{e}), (3 6), (3 9), (4 4). \end{array}\tag{52b}
$$

For fixed $\{ \mathbf { v } _ { k } ^ { ( r ) } \}$ , the objective in (52a) is afine in the optimization variables. Hence, (52) is a convex semidefinite program and can be eficiently solved by standard convex optimization solvers [32]. The above procedure is iterated until convergence. Then, the transmit beamformer can be recovered by eigenvalue decomposition.

Similar to the receive beamforming sub-problem, the direct implementation of the robust sensing constraint (44) involves an LMI of dimension $( Q M ^ { 2 } + \bar { 1 ) } \times ( Q M ^ { 2 } + \bar { 1 } )$ A similar reduced-dimensional manipulation is employed, where the receive beamforming matrices $\{ \mathbf { U } _ { q } \}$ are fixed, while $\begin{array} { r } { \mathbf { R } _ { x } = \sum _ { k \in \mathcal { K } } \mathbf { W } _ { k } + \mathbf { R } _ { 0 } } \end{array}$ is an optimization variable. We therefore exploit the same column-space reduction principle while adapting the factorization to the structure of the transmit beamforming sub-problem. In particular, since the fixed receive covariance matrix satisfies ${ \mathbf { U } } _ { q } =$ $\mathbf { u } _ { q } \mathbf { u } _ { q } ^ { H }$ , we define ${ \mathbf b } _ { q } = { \mathbf B } { \mathbf u } _ { q } ,$ such that $\mathbf { B } \mathbf { U } _ { q } \mathbf { B } ^ { H } = \mathbf { b } _ { q } \mathbf { \bar { b } } _ { q } ^ { H }$ is rank one. Moreover, using the compact SVD of $\dot { \bf G }$ we express $\mathbf { G } \mathbf { R } _ { x } \mathbf { G } ^ { H } \mathbf { \Psi } = \mathbf { \Psi } \mathbf { U } _ { G } \mathbf { \bar { T } } \mathbf { U } _ { G } ^ { H }$ where $\mathbf { T } ~ \in ~ \mathbb { C } ^ { r _ { G } \times r _ { G } }$ remains afine in $\mathbf { R } _ { x }$ . Accordingly, each high-dimensional block can be factorized as $\mathbf { Y } _ { q , j } ^ { - } = \mathbf { C } _ { q , j } \mathbf { \bar { T } } ^ { T } \mathbf { C } _ { q , j } ^ { H }$ , where $\mathbf { C } _ { q , j } = | \alpha _ { j } | ( \mathbf { U } _ { G } ^ { * } \otimes \mathbf { b } _ { q } )$ is fixed. By subsequently applying a compact QR factorization to the block-diagonal matrix constructed from $\{ \mathbf { C } _ { q , j } \} _ { j \in \mathcal { Q } }$ , the original robust sensing LMI is represented exactly in a reduced subspace of dimension $Q r _ { G } + 1$ , instead of $Q M ^ { 2 } + 1$ . Hence, although both beamforming sub-problems employ the same underlying column-space reduction principle, the fixed rank-one structure of $\mathbf { U } _ { q }$ in the transmit beamforming sub-problem yields the further dimensional reduction from $Q r _ { G } N _ { r } + 1$ in (50) to $Q r _ { G } + 1$

C. Layer-by-Layer SIM Phase Shift Optimization Subproblem

For fixed $\{ \mathbf { W } _ { k } \} , \mathbf { R } _ { 0 }$ , and $\{ \mathbf { U } _ { q } \}$ , we adopt a layer-bylayer framework to optimize the SIM phase shift matrices $\{ \Theta ^ { l } \}$ and optimize one layer at a time while fixing all the remaining layers. Since the target SINR variable $\varrho$ appears in the matrix block $\begin{array} { r } { \mathbf { D } _ { q } = - \frac { 1 } { \rho } \mathbf { Y } _ { q , q } , } \end{array}$ we introduce the auxiliary variable $\bar { \varrho } \triangleq \frac { \textstyle 1 } { \rho } , \bar { \varrho } > \overline { { 0 } }$ such that ${ \bf D } _ { q } = { \bf \Phi }$ $- \bar { \varrho } \mathbf { Y } _ { q , q }$ and apply a bisection search over ϱ¯ as in the previous sub-problems. At the l-th SIM layer, the forward and reverse wave-domain transfer matrices can be written as $\mathbf { G } = \mathbf { C } _ { L } ^ { l } \Theta ^ { l } \mathbf { C } _ { R } ^ { l }$ and $\mathbf { B } = \mathbf { C } _ { L } ^ { l } \mathbf { \Theta } \mathbf { \Theta } ^ { l } \widetilde { \mathbf { C } } _ { R } ^ { l }$ , respectively, where the matrices $\mathbf { C } _ { L } ^ { l } , \mathbf { C } _ { R } ^ { l } .$ , and $\widetilde { \mathbf { C } } _ { R } ^ { \bar { l } }$ eare fixed with respect to ethe l-th layer, which can be expressed as

$$
\mathbf {C} _ {L} ^ {l} = \left\{ \begin{array}{l l} \boldsymbol {\Theta} ^ {L} \boldsymbol {\Omega} ^ {L} \ldots \boldsymbol {\Theta} ^ {l + 1} \boldsymbol {\Omega} ^ {l + 1}, & \text { if } l \neq L, \\ \mathbf {I} _ {M}, & \text { if } l = L, \end{array} \right.\tag{53}
$$

$$
\mathbf {C} _ {R} ^ {l} = \left\{ \begin{array}{l l} \boldsymbol {\Omega} ^ {l} \boldsymbol {\Theta} ^ {l - 1} \boldsymbol {\Omega} ^ {l - 1} \dots \boldsymbol {\Theta} ^ {1} \boldsymbol {\Omega} _ {t} ^ {1}, & \text { if } l \neq 1, \\ \boldsymbol {\Omega} _ {t} ^ {1}, & \text { if } l = 1, \end{array} \right.\tag{54}
$$

and

$$
\widetilde {\mathbf {C}} _ {R} ^ {l} = \left\{ \begin{array}{l l} \boldsymbol {\Omega} ^ {l} \boldsymbol {\Theta} ^ {l - 1} \boldsymbol {\Omega} ^ {l - 1} \dots \boldsymbol {\Theta} ^ {1} \boldsymbol {\Omega} _ {r} ^ {1}, & \text { if } l \neq 1, \\ \boldsymbol {\Omega} _ {r} ^ {1}, & \text { if } l = 1, \end{array} \right.\tag{55}
$$

where $\Omega _ { r } ^ { 1 } \in \mathbb { C } ^ { M \times N _ { r } }$ models the propagation coeficient matrix between the receive antenna array and the first SIM layer, which can be derived from (2) by replacing $r _ { m , \tilde { m } } ^ { l }$ and $\chi _ { m , \tilde { m } } ^ { l }$ with $r _ { m , n _ { 1 } } ^ { 1 }$ and $\chi _ { m , n _ { r } } ^ { 1 }$ , respectively, for all m $\in \mathcal { M }$ and $\dot { n } _ { r } \in \mathcal { N } _ { r }$

1) LMI-Based Robust Sensing Constraint Analysis:

Define $\phi _ { l } = \left\lceil e ^ { j \theta _ { 1 } ^ { l } } , \dots , e ^ { j \theta _ { M } ^ { l } } \right\rceil ^ { T }$ such that $\Phi _ { l } \mathrm { ~ = ~ } \phi _ { l } \phi _ { l } ^ { H }$ $\mathbf { \Delta } \Phi _ { l } \succeq \mathbf { 0 }$ , diag(Φ<sub>l</sub>) = 1, and $\mathrm { R a } \bar { \mathrm { n k } } ( \Phi _ { l } ) = 1$ . Then, the term ${ \bf G } { \bf R } _ { x } { \bf G } ^ { H }$ in $\mathbf { Y } _ { q , j } , \ \forall q , j \in \mathcal { Q }$ can be written as

$$
\begin{array}{r l} & {\mathbf {Z} _ {G} = \mathbf {G R} _ {x} \mathbf {G} ^ {H}} \\ & {\quad = \mathbf {C} _ {L} ^ {l} \boldsymbol {\Theta} ^ {l} \mathbf {C} _ {R} ^ {l} \mathbf {R} _ {x} (\mathbf {C} _ {R} ^ {l}) ^ {H} (\boldsymbol {\Theta} ^ {l}) ^ {H} (\mathbf {C} _ {L} ^ {l}) ^ {H}} \\ & {\quad = \mathbf {C} _ {L} ^ {l} \mathrm{diag} (\boldsymbol {\phi} _ {l}) \mathbf {C} _ {R} ^ {l} \mathbf {R} _ {x} (\mathbf {C} _ {R} ^ {l}) ^ {H} \mathrm{diag} (\boldsymbol {\phi} _ {l}) ^ {H} (\mathbf {C} _ {L} ^ {l}) ^ {H}} \\ & {\quad = \mathbf {C} _ {L} ^ {l} ((\mathbf {C} _ {R} ^ {l} \mathbf {R} _ {x} (\mathbf {C} _ {R} ^ {l}) ^ {H}) \odot \boldsymbol {\Phi} _ {l}) (\mathbf {C} _ {L} ^ {l}) ^ {H},} \end{array}\tag{56}
$$

where ⊙ is the element-wise product or the Hadamard product. Similarly, the reverse term $\mathbf { B } \mathbf { U } _ { q } \mathbf { B } ^ { H }$ can be written as

$$
\mathbf {Z} _ {B, q} = \mathbf {B} \mathbf {U} _ {q} \mathbf {B} ^ {H} = \mathbf {C} _ {L} ^ {l} \left(\left(\widetilde {\mathbf {C}} _ {R} ^ {l} \mathbf {U} _ {q} \left(\widetilde {\mathbf {C}} _ {R} ^ {l}\right) ^ {H}\right) \odot \boldsymbol {\Phi} _ {l}\right) \left(\mathbf {C} _ {L} ^ {l}\right) ^ {H},\tag{57}
$$

For fixed transmit and receive beamformers, both $\mathbf { Z } _ { G }$ and $\mathbf { Z } _ { B , q }$ are afine in $\Phi _ { l } ,$ , whereas, $\mathbf { Y } _ { q , j }$ is bilinear in these matrices. To obtain a tractable approximation, at the rth iteration we use the first-order SCA approximation to linearize $\mathbf { Y } _ { q , j }$ around the current point $\dot { \Phi _ { l } ^ { ( r ) } }$ as follows

$$
\mathbf {Y} _ {q, j} ^ {(r)} = | \alpha_ {j} | ^ {2} \left(\mathbf {Z} _ {G} ^ {T} \otimes \mathbf {Z} _ {B, q} ^ {(r)} + (\mathbf {Z} _ {G} ^ {(r)}) ^ {T} \otimes \mathbf {Z} _ {B, q} - (\mathbf {Z} _ {G} ^ {(r)}) ^ {T} \otimes \mathbf {Z} _ {B, q} ^ {(r)}\right).\tag{58}
$$

Then, we substitute the approximation $\mathbf { Y } _ { q , j } ^ { ( r ) }$ into $\mathbf { X } _ { q }$ to get $\mathbf { X } _ { q } ^ { ( r ) }$ , which will be used to approximate the LMI in (44).

In similar ways, $\mathbf { Q } _ { k }$ in (36) and $\Xi \left( 3 9 \right)$ can be expressed as

$$
\mathbf {Z} _ {Q _ {k}} = \mathbf {G} \mathbf {S} _ {Q _ {k}} \mathbf {G} ^ {H} = \mathbf {C} _ {L} ^ {l} \left(\left(\mathbf {C} _ {R} ^ {l} \mathbf {S} _ {Q _ {k}} \left(\mathbf {C} _ {R} ^ {l}\right) ^ {H}\right) \odot \boldsymbol {\Phi} _ {l}\right) \left(\mathbf {C} _ {L} ^ {l}\right) ^ {H},
$$

and

(59)

$$
\mathbf {Z} _ {\Xi} = \mathbf {G} \mathbf {S} _ {\Xi} \mathbf {G} ^ {H} = \mathbf {C} _ {L} ^ {l} \left(\left(\mathbf {C} _ {R} ^ {l} \mathbf {S} _ {\Xi} \left(\mathbf {C} _ {R} ^ {l}\right) ^ {H}\right) \odot \boldsymbol {\Phi} _ {l}\right) \left(\mathbf {C} _ {L} ^ {l}\right) ^ {H},\tag{60}
$$

respectively, where $\begin{array} { r } { \mathbf { S } _ { Q _ { k } } = \mathbf { W } _ { k } - \Gamma _ { k } \sum _ { i \in \mathcal { K } , ~ i \neq k } \mathbf { W } _ { i } - \Gamma _ { k } \mathbf { R } _ { 0 } } \end{array}$ and $\begin{array} { r } { \mathbf { S } _ { \Xi } = \sum _ { k \in \mathcal { K } } \mathbf { W } _ { k } - \varpi \mathbf { R } _ { 0 } } \end{array}$

As in previous sub-problems, to enforce the rankone property of $\Phi _ { l } , \quad \mathrm { w e }$ add the penalty term $\left\lceil \zeta _ { 3 } \left( \dot { \mathrm { T r } } ( \mathring { \Phi } _ { l } ) - ( \phi _ { l } ^ { ( r ) } ) ^ { H } \Phi _ { l } \phi _ { l } ^ { ( r ) } \right) \right\rceil$ to the objective function, where $\phi _ { l } ^ { ( r ) }$ is the dominant eigenvector of $\Phi _ { l } ^ { ( r ) }$ . Consequently, for a fixed $\bar { \varrho } ,$ the l-th layer phase update is obtained by

$$
\min _ {\boldsymbol {\Phi} _ {l}} \bar {\varrho} + \zeta_ {3} \left(\mathrm{Tr} (\boldsymbol {\Phi} _ {l}) - (\boldsymbol {\phi} _ {l} ^ {(r)}) ^ {H} \boldsymbol {\Phi} _ {l} \boldsymbol {\phi} _ {l} ^ {(r)}\right)\tag{61a}
$$

$$
\mathrm{s.t.} \quad \Phi_ {l} \succeq \mathbf {0}, \mathrm{diag} (\Phi_ {l}) = \mathbf {1}
$$

$$
(3 6), (3 9), \text { and } (4 4).\tag{61b}
$$

(61c)

The problem (61) is a convex SDP problem that can be solved by standard convex optimization solvers [32]. The above procedure is repeated sequentially for all layers $l \in \mathcal L$ . For a given trial value ϱ¯, if (61) is feasible, then ϱ¯ is declared feasible; otherwise, it is infeasible. Therefore, the optimal ϱ¯ is obtained by an outer bisection search.

2) Low-Complexity Robust Sensing Constraint Analysis:

As discussed previously, directly implementing the robust sensing LMI constraint, (44), entails substantial computational complexity and memory overhead. Unfortunately, the exact dimension-reduction technique developed for the transmit and receive beamforming sub-problems cannot be applied to this sub-problem, as the optimization variables now appear on both sides of the Kronecker product in $\mathbf { Y } _ { q , j }$ . To address this challenge, we propose an alternative low-complexity solution specifically tailored to the SIM phase shift sub-problem in this section. The sensing constraint in (41) can be rewritten as

$$
\sum_ {j \neq q} \psi_ {q, j} - \bar {\varrho} \psi_ {q, q} + \sigma_ {B} ^ {2} \operatorname{Tr} (\mathbf {U} _ {q}) \leq 0, \quad \forall q \in \mathcal {Q},\tag{62}
$$

where $\begin{array} { l l l } { { \bar { \varrho } } } & { { = } } & { { { \frac { 1 } { \varrho } } } } \end{array}$ and $\psi _ { q , j } ~ = ~ \mathrm { v e c } ( \mathbf { A } _ { j } ) ^ { H } \mathbf { Y } _ { q , j } \ \mathrm { v e c } ( \mathbf { A } _ { j } ) \triangleq { }$ $| \alpha _ { j } | ^ { 2 } \mathrm { T r } \bigl ( \mathbf { Z } _ { B , q } \bar { \mathbf { A } _ { j } } \mathbf { Z } _ { G } \mathbf { A } _ { j } ^ { H } \bigr )$ . Substituting $\begin{array} { r l r } { { \bf A } _ { j } } & { { } = } & { \hat { \bf A } _ { j } + } \end{array}$ $\Delta \mathbf { A } _ { j } , \forall j \in \mathcal { Q }$ into (62) yields

$$
\begin{array}{c} \psi_ {q, j} = | \alpha_ {j} | ^ {2} \Big (\operatorname{Tr} \left(\mathbf {Z} _ {B, q} \hat {\mathbf {A}} _ {j} \mathbf {Z} _ {G} \hat {\mathbf {A}} _ {j} ^ {H}\right) \\ + 2 \Re \Big \{\operatorname{Tr} \left(\mathbf {Z} _ {B, q} \Delta \mathbf {A} _ {j} \mathbf {Z} _ {G} \hat {\mathbf {A}} _ {j} ^ {H}\right) \Big \} + \operatorname{Tr} \left(\mathbf {Z} _ {B, q} \Delta \mathbf {A} _ {j} \mathbf {Z} _ {G} \Delta \mathbf {A} _ {j} ^ {H}\right) \Big). \end{array}\tag{63}
$$

From the Cauchy–Schwarz inequality associated with the Frobenius inner product [33, Sec. 1.1], for any two complex matrices X and Y of compatible dimensions, we have

$$
\left| \operatorname{Tr} (\mathbf {X} ^ {H} \mathbf {Y}) \right| \leq \| \mathbf {X} \| _ {F} \| \mathbf {Y} \| _ {F}.\tag{64}
$$

Consequently, under the bounded uncertainty model $\| \Delta \mathbf { A } _ { j } \| _ { F } \le \varepsilon _ { A _ { j } }$ 2

$$
\max _ {\| \Delta \mathbf {A} _ {j} \| _ {F} \leq \varepsilon_ {A _ {j}}} \Re \left\{\operatorname{Tr} \left(\Delta \mathbf {A} _ {j} ^ {H} \mathbf {Y}\right) \right\} = \varepsilon_ {A _ {j}} \| \mathbf {Y} \| _ {F}.\tag{65}
$$

Applying (65) to the cross term in (63), we obtain

$$
\begin{array}{r l} & 2 \Re \Bigl \{\mathrm{Tr} \Bigl (\mathbf {Z} _ {B, q} \Delta \mathbf {A} _ {j} \mathbf {Z} _ {G} \hat {\mathbf {A}} _ {j} ^ {H} \Bigr) \Bigr \} = 2 \Re \bigl \{\mathrm{Tr} (\Delta \mathbf {A} _ {j} \boldsymbol {\Psi} _ {q, j}) \bigr \} \\ & \qquad = 2 \varepsilon_ {A _ {j}} \| \boldsymbol {\Psi} _ {q, j} \| _ {F}, \end{array}\tag{66}
$$

where $\boldsymbol { \Psi } _ { q , j } \triangleq \mathbf { Z } _ { G } \widehat { \mathbf { A } } _ { j } ^ { H } \mathbf { Z } _ { B , q }$

bMoreover, since $\mathbf { \bar { Z } } _ { G } \succeq \mathbf { 0 }$ and $\mathbf { Z } _ { B , q } ~ \succeq ~ \mathbf { 0 }$ , using the standard submultiplicative property of Schatten norms [33, Sec. 1.1], the quadratic uncertainty term satisfies

$$
\begin{array}{r l} & {\mathrm{Tr} \left(\mathbf {Z} _ {B, q} \Delta \mathbf {A} _ {j} \mathbf {Z} _ {G} \Delta \mathbf {A} _ {j} ^ {H}\right) = \left\| \mathbf {Z} _ {B, q} ^ {1 / 2} \Delta \mathbf {A} _ {j} \mathbf {Z} _ {G} ^ {1 / 2} \right\| _ {F} ^ {2}} \\ & {\qquad \leq \| \mathbf {Z} _ {B, q} \| _ {2} \| \Delta \mathbf {A} _ {j} \| _ {F} ^ {2} \| \mathbf {Z} _ {G} \| _ {2}} \\ & {\qquad \leq \varepsilon_ {A _ {j}} ^ {2} \| \mathbf {Z} _ {B, q} \| _ {2} \| \mathbf {Z} _ {G} \| _ {2}.} \end{array}\tag{67}
$$

Therefore, a robust upper bound for the interference term $( j \neq q )$ is

$$
\overline {{\psi}} _ {q, j} = | \alpha_ {j} | ^ {2} \Big (\mathrm{Tr} \Big (\mathbf {Z} _ {B, q} \hat {\mathbf {A}} _ {j} \mathbf {Z} _ {G} \hat {\mathbf {A}} _ {j} ^ {H} \Big) + 2 \varepsilon_ {A _ {j}} \eta_ {q, j} + \varepsilon_ {A _ {j}} ^ {2} \beta_ {q} \Big),\tag{68}
$$

while a robust lower bound for the desired term $( j = q )$ is

$$
\underline {{\psi}} _ {q, q} = | \alpha_ {q} | ^ {2} \Big (\mathrm{Tr} \Big (\mathbf {Z} _ {B, q} \hat {\mathbf {A}} _ {q} \mathbf {Z} _ {G} \hat {\mathbf {A}} _ {q} ^ {H} \Big) - 2 \varepsilon_ {A _ {q}} \eta_ {q, q} - \varepsilon_ {A _ {q}} ^ {2} \beta_ {q} \Big),\tag{69}
$$

where $\eta _ { q , j }$ and $\beta _ { q }$ are defined as

$$
\eta_ {q, j} \triangleq \| \mathbf {\Psi} _ {q, j} \| _ {F}, \quad \beta_ {q} \triangleq \| \mathbf {Z} _ {B, q} \| _ {2} \| \mathbf {Z} _ {G} \| _ {2}.\tag{70}
$$

Using (68) and (69), a norm-bound-based sensing surrogate is

$$
\sum_ {j \neq q} \overline {{\psi}} _ {q, j} - \bar {\varrho} \underline {{\psi}} _ {q, q} + \sigma_ {B} ^ {2} \operatorname{Tr} (\mathbf {U} _ {q}) \leq 0, \quad \forall q \in \mathcal {Q}.\tag{71}
$$

The bounds in $( 6 8 ) \_ ( 6 9 )$ are still non-convex because both $\mathbf { Z } _ { G } ( \Phi _ { l } )$ and $\mathbf { Z } _ { B , q } ( \Phi _ { l } )$ depend on $\Phi _ { l } ,$ and their product appears in the nominal term. To obtain a convex sub-problem, we adopt an SCA step at the r-th iteration. Hence, the nominal term is approximated by the first-order afine expression

$$
\begin{array}{l} \psi_ {q, j} ^ {(r)} (\mathbf {\Phi} _ {l}) \triangleq \mathrm{Tr} \Big (\mathbf {Z} _ {B, q} ^ {(r)} \widehat {\mathbf {A}} _ {j} \mathbf {Z} _ {G} (\mathbf {\Phi} _ {l}) \widehat {\mathbf {A}} _ {j} ^ {H} \Big) \\ \quad + \mathrm{Tr} \Big (\mathbf {Z} _ {B, q} (\mathbf {\Phi} _ {l}) \widehat {\mathbf {A}} _ {j} \mathbf {Z} _ {G} ^ {(r)} \widehat {\mathbf {A}} _ {j} ^ {H} \Big) - \mathrm{Tr} \Big (\mathbf {Z} _ {B, q} ^ {(r)} \widehat {\mathbf {A}} _ {j} \mathbf {Z} _ {G} ^ {(r)} \widehat {\mathbf {A}} _ {j} ^ {H} \Big), \end{array}\tag{72}
$$

where $\mathbf { Z } _ { G } ^ { ( r ) }$ and $\mathbf { Z } _ { B , q } ^ { ( r ) }$ are the values of $\mathbf { Z } _ { G }$ and $\mathbf { Z } _ { B , q }$ at the previous iteration $r ,$ respectively. Since both $\mathbf { Z } _ { G } ( \Phi _ { l } )$ and $\mathbf { Z } _ { B , q } ( \Phi _ { l } )$ are afine in $\Phi _ { l } .$ the quantity $\psi _ { q , j } ^ { ( r ) } ( \Phi _ { l } )$ is afine in $\Phi _ { l }$ . In addition, the values of the $\eta _ { q , j }$ and $\beta _ { q }$ are calculated based on the previous iteration matrices as $\eta _ { q , j } ^ { ( r ) } = \left\| \Psi _ { q , j } ^ { ( r ) } \right\| _ { F }$ and $\boldsymbol { \beta _ { q } ^ { ( r ) } } = \lVert \mathbf { Z } _ { B , q } ^ { ( r ) } \rVert _ { 2 } \lVert \mathbf { Z } _ { G } ^ { ( r ) } \rVert _ { 2 }$ . Then, the robust upper and lower bounds become

$$
\overline {{\psi}} _ {q, j} ^ {(r)} (\boldsymbol {\Phi} _ {l}) = | \alpha_ {j} | ^ {2} \Big (\psi_ {q, j} ^ {(r)} (\boldsymbol {\Phi} _ {l}) + 2 \varepsilon_ {A _ {j}} \eta_ {q, j} ^ {(r)} + \varepsilon_ {A _ {j}} ^ {2} \beta_ {q} ^ {(r)} \Big), \quad j \neq q,\tag{73}
$$

$$
\underline {{\psi}} _ {q, q} ^ {(r)} (\boldsymbol {\Phi} _ {l}) = | \alpha_ {q} | ^ {2} \Big (\psi_ {q, q} ^ {(r)} (\boldsymbol {\Phi} _ {l}) - 2 \varepsilon_ {A _ {q}} \eta_ {q, q} ^ {(r)} - \varepsilon_ {A _ {q}} ^ {2} \beta_ {q} ^ {(r)} \Big).\tag{74}
$$

Accordingly, the sensing constraint is approximated by

$$
\sum_ {j \neq q} \overline {{\psi}} _ {q, j} ^ {(r)} (\mathbf {\Phi} _ {l}) - \bar {\varrho} \underline {{\psi}} _ {q, q} ^ {(r)} (\mathbf {\Phi} _ {l}) + \sigma_ {B} ^ {2}   \mathrm{Tr} (\mathbf {U} _ {q}) \leq 0, \qquad \forall q \in \mathcal {Q}.\tag{75}
$$

After adding the penalty term $\left\lceil \zeta _ { 3 } \left( \mathrm { T r } ( \Phi _ { l } ) - ( \phi _ { l } ^ { ( r ) } ) ^ { \smile } \Phi _ { l } \phi _ { l } ^ { ( r ) } \right) \right\rceil$ to the objective function to satisfy the rank-one constraint, for a fixed trial value ϱ¯, the l-th layer phase update is obtained by solving

$$
\min _ {\boldsymbol {\Phi} _ {l}} \bar {\varrho} + \zeta_ {3} \left(\mathrm{Tr} (\boldsymbol {\Phi} _ {l}) - (\boldsymbol {\phi} _ {l} ^ {(r)}) ^ {H} \boldsymbol {\Phi} _ {l} \boldsymbol {\phi} _ {l} ^ {(r)}\right)\tag{76a}
$$

$$
\text { s.t. } \quad \boldsymbol {\Phi} _ {l} \succeq \mathbf {0}, \qquad \operatorname{diag} (\boldsymbol {\Phi} _ {l}) = \mathbf {1},
$$

$$
(3 6), (3 9), \text {   and   } (7 5).\tag{76b}
$$

(76c)

Problem (76) is a convex semidefinite program. Compared with the LMI-based solution, this formulation ofers a much lower complexity because it avoids constructing the large matrix $\mathbf { X } _ { q }$ and its associated semidefinite constraint. Hence, the proposed norm-based robust surrogate provides an efective compromise between robustness and computational tractability in the layer-by-layer SIM phase optimization.

D. Complete Algorithm, Convergence, and Computational Complexity

Based on the previously formulated sub-problems and their corresponding solutions, the original problem (45) is solved using an AO framework, where the convexified receive beamformers, transmit beamformers, and SIM phase shifts sub-problems are successively optimized while fixing the remaining variable blocks. Since SCA approximations and rank-one penalty-based reformulations are used, global optimality cannot be guaranteed. Nevertheless, following the standard convergence properties of AO/SCA methods, the proposed algorithm converges to a stationary solution. Since the auxiliary variable $\bar { \varrho } = 1 / \varrho$ is handled through bisection in all three sub-problems, each AO step involves a bisection search whose feasibility is determined by solving the corresponding convex SDP. The overall procedure is summarized in Algorithm 1.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Proposed AO Algorithm for Robust SIM-Assisted ISACC Framework
1: Input: $\{\hat{\mathbf{h}}_k\}_{k\in \mathcal{K}}$, $\{\hat{\mathbf{a}}_q\}_{q\in \mathcal{Q}}$, $\{\hat{\mathbf{A}}_q\}_{q\in \mathcal{Q}}$, $\{\Omega^l\}_{l\in \mathcal{L}}$, $\Omega_t^1$, $\Omega_r^1$, $P_{\max}$, $\Gamma_k$, $\varpi$, $\{\varepsilon_{h_k}\}$, $\{\varepsilon_{a_q}\}$, $\{\varepsilon_{A_q}\}$, $\sigma_B^2$, $\zeta_1$, $\zeta_2$, and $\zeta_3$.
2: Initialize: $\{\mathbf{W}_k^{(0)}\}_{k\in \mathcal{K}}$, $\mathbf{R}_0^{(0)}$, $\{\mathbf{U}_q^{(0)}\}_{q\in \mathcal{Q}}$, $\{\Theta^{l,(0)}\}_{l\in \mathcal{L}}$, and set $r\gets 1$.
3: repeat
4: Receive beamforming: Perform bisection over $\bar{\varrho}$ and solve (49) for each trial value to obtain $\{\mathbf{U}_q^{(r)}\}_{q\in \mathcal{Q}}$, and recover $\{\mathbf{u}_q^{(r)}\}$.
5: Transmit beamforming: Perform bisection over $\bar{\varrho}$ and solve (52) for each trial value to obtain $\{\mathbf{W}_k^{(r)}\}_{k\in \mathcal{K}}$, $\mathbf{R}_0^{(r)}$, and recover $\{\mathbf{w}_k^{(r)}\}$.
6: SIM phase shift optimization: Perform bisection over $\bar{\varrho}$.
7: repeat
8: for $l = 1,\ldots ,L$ do
9: Solve (61) for the LMI-based design, or (76) for the low-complexity design, to obtain $\Phi_l^{(r)}$.
10: Recover $\theta_l^{(r)}$ and set $\Theta^{l,(r)} = \mathrm{diag}(\theta_l^{(r)})$.
11: end for
12: until the layer-sweep convergence criterion is satisfied.
13: Update all optimization and auxiliary variables.
14: $r\gets r + 1$.
15: until the AO convergence criterion is satisfied.
16: Output: $\{\mathbf{w}_k^*\}_{k\in \mathcal{K}}$, $\mathbf{R}_0^*$, $\{\mathbf{u}_q^*\}_{q\in \mathcal{Q}}$, $\{\Theta^{l,*}\}_{l\in \mathcal{L}}$, and $\varrho^*$.
</div>

The computational complexity of Algorithm 1 is mainly determined by the SDPs solved within the receive beamforming, transmit beamforming, and SIM phase shift optimization steps. For the receive beamforming subproblem (49), there are $Q$ positive semidefinite matrices of dimension $N _ { r }$ and $Q$ reduced robust sensing LMIs of dimension $Q r _ { G } N _ { r } + 1$ . Hence, the corresponding computational complexity is $\mathcal { O } \left( I _ { \mathrm { B , R } } \left( D _ { R } \right) ^ { 3 . 5 } \right)$ where $I _ { \mathrm { B , R } }$ is the number of bisection iterations and $D _ { R } \ = \ Q N _ { r } + Q ( Q r _ { G } N _ { r } + 1 )$ . Similarly, the computational complexity of the transmit beamforming subproblem (52) can be given as $\mathcal { O } \Big ( I _ { \mathrm { B , T } } ( D _ { T } ) ^ { 3 . 5 } \Big )$ , where $I _ { \mathrm { B , T } }$ is the corresponding number of bisection iterations and $D _ { T } = ( K + 1 ) N _ { t } + ( K + Q ) ( M + 1 ) + Q ( Q r _ { G } + 1 )$ For the LMI-based SIM phase shift sub-problem (61), the complexity is $\mathcal { O } \bigg ( I _ { \mathrm { B , P } } I _ { \mathrm { S } } L ( D _ { P } ^ { \mathrm { L M I } } ) ^ { 3 . 5 } \bigg )$ , where $I _ { \mathrm { B , P } }$ denotes the number of bisection iterations, $D _ { P } ^ { \mathrm { L M I } } = M + ( K +$ $Q ) ( M + 1 ) + Q ( Q M ^ { 2 } + 1 )$ , L is the number of SIM layers that are successively optimized over $I _ { \mathrm { S } }$ layer sweeps for every bisection trial. For the low-complexity phase shift formulation (76), the $Q$ high-dimensional sensing LMIs are replaced by $Q$ scalar robust surrogate constraints. Therefore, the computational complexity is characterized as $\mathcal { O } \bigg ( I _ { \mathrm { B , P } } I _ { \mathrm { S } } L ( D _ { P } ^ { \mathrm { L C } } ) ^ { 3 . 5 } \bigg )$ , where $D _ { P } ^ { \mathrm { L C } } = M + ( K + Q ) ( M + 1 )$

Consequently, if $\dot { I } _ { \mathrm { A O } }$ denotes the number of outer AO iterations, the overall computational complexity when adopting the LMI-based phase shift design is

$$
\mathcal {O} \left(I _ {\mathrm{AO}} \left[ I _ {\mathrm{B}, \mathrm{R}} \left(D _ {R}\right) ^ {3. 5} + I _ {\mathrm{B}, \mathrm{T}} \left(D _ {T}\right) ^ {3. 5} + I _ {\mathrm{B}, \mathrm{P}} I _ {\mathrm{S}} L \left(D _ {P} ^ {\mathrm{LMI}}\right) ^ {3. 5} \right]\right),\tag{77}
$$

whereas the proposed low-complexity phase shift design reduces it to

$$
\mathcal {O} \left(I _ {\mathrm{AO}} \left[ I _ {\mathrm{B,R}} (D _ {R}) ^ {3. 5} + I _ {\mathrm{B,T}} (D _ {T}) ^ {3. 5} + I _ {\mathrm{B,P}} I _ {\mathrm{S}} L (D _ {P} ^ {\mathrm{LC}}) ^ {3. 5} \right]\right),\tag{78}
$$

The proposed dimensionality-reduction procedures therefore substantially decrease the computational burden of all three optimization blocks. In particular, the robust sensing LMI of dimension $Q M ^ { 2 } + 1$ is exactly reduced to $Q r _ { G } N _ { r } + 1$ and $Q r _ { G } + 1$ in the receive and transmit beamforming sub-problems, respectively. Moreover, the low-complexity phase shift formulation completely avoids the $Q M ^ { 2 } +$ 1-dimensional sensing LMI.

## V. Simulation Results

In this section, comprehensive numerical simulations are conducted to evaluate the performance of the proposed robust SIM-assisted ISACC framework. The system operates in a three-dimensional Cartesian coordinate system with the BS located at $( 0 , 0 , Z )$ , where $Z$ represents the BS height. Both downlink communication UEs and targets are randomly generated following a uniform distribution within a 20 m radius circle centered at (20, 20, 0) m. The inter-layer spacing is set to $d _ { \mathrm { S I M } } = \frac { \lambda } { 4 } [ 1 9 ]$ , while the spacing between two adjacent meta-atoms is set to $d _ { \mathrm { { e l e m e n t } } } \ = \ { \frac { \lambda } { 2 } }$ . We assume a path loss exponent of $\eta = 2 . 5$ and a Rician factor of $\kappa = 1 0 ~ \mathrm { d B }$ . The penalty factors are set to $\zeta _ { 1 } = \zeta _ { 2 } = \zeta _ { 3 } = 1 0 ^ { - 2 }$ , while the CSI bounds are set to $1 0 ^ { - 3 }$ . Unless otherwise stated, the main simulation parameters are given in Table II. The propagation distance, $r _ { m , \tilde { m } } ^ { l }$ , from the m˜ -th meta-atom in the l − 1-th layer to the m-th meta-atom in the l-th layer is given by

$$
\begin{array}{r l} & r _ {m, \tilde {m}} ^ {l} \\ & = \sqrt {d _ {\mathrm{SIM}} ^ {2} + d _ {\mathrm{element}} ^ {2} \left[ (i _ {x} (m) - i _ {x} (\tilde {m})) ^ {2} + (i _ {z} (m) - i _ {z} (\tilde {m})) ^ {2} \right]}, \end{array}\tag{79}
$$

where $i _ { x } ( m ) = \mathrm { m o d } ( m - 1 , M _ { x } ) + 1$ and $\begin{array} { r } { i _ { z } ( m ) = \left\lceil \frac { m } { M _ { x } } \right\rceil } \end{array}$ represent the 2D grid column and row indices of the m-th meta-atom. Additionally, the propagation distance, $r _ { m , n _ { t } } ^ { 1 } ,$ from the $n _ { t }$ -th transmit antenna to the m-th meta-atom in the $1 ^ { s t }$ layer is given by (80) at the top of this page. Similar to (80), we can get the propagation distance, $r _ { m , n _ { r } } ^ { \bar { 1 } } ,$ from the m-th meta-atom in the $1 ^ { s t }$ layer to the $n _ { r } – \mathrm { t h }$ receive antenna.

To show the efectiveness of our proposed robust SIMassisted ISACC framework, we compare the achieved performance with four diferent baseline schemes. More specifically, we consider: 1) Sensing-Centric Scheme: which removes the communication QoS constraints to evaluate the maximum achievable target sensing SINR without supporting communication users; 2) No-Covertness Scheme: which relaxes the covertness detection constraints to quantify the performance trade-ofs and penalties incurred by enforcing strict covert transmission; 3) Fixed (Random) Phase Shift Scheme: where the wave-domain

TABLE II Simulation Parameters

<table><tr><td>Parameter</td><td>Value</td><td>Parameter</td><td>Value</td></tr><tr><td>Number of Tx antennas,  $N_{t}$ </td><td>6</td><td>Number of covert UEs, K</td><td>3</td></tr><tr><td>Number of Rx antennas,  $N_{r}$ </td><td>6</td><td>Number of Targets/wardens, Q</td><td>2</td></tr><tr><td>Number of SIM layers, L</td><td>3</td><td>Number of meta-atoms per layer, M</td><td>25</td></tr><tr><td>Carrier frequency</td><td>10 GHz</td><td>Communication bandwidth,  $B_{w}$ </td><td>1 MHz</td></tr><tr><td>BS height, Z</td><td>15 m</td><td>Radius of service area</td><td>20 m</td></tr><tr><td>Maximum allowed transmit power  $P_{\text{max}}$ </td><td>30-40 dBm</td><td>Covertness threshold ε</td><td>0.1</td></tr><tr><td>Users&#x27; rate requirement,  $R_{k}^{\text{min}}$ </td><td>0.1 bps/Hz</td><td>Number of Warden observations per block, T</td><td>1000</td></tr><tr><td>meta-atom spacing,  $d_{\text{element}}$ </td><td>λ/2</td><td>Area of each meta-atom,  $A_{e}$ </td><td> $λ^{2}/4$ </td></tr><tr><td>Noise power spectral density</td><td>-174 dBm/Hz</td><td>SIM layers spacing,  $d_{\text{SIM}}$ </td><td>λ/4</td></tr></table>

$$
r _ {m, n _ {t}} ^ {1} = \sqrt {d _ {\mathrm{SIM}} ^ {2} + d _ {\mathrm{element}} ^ {2} \left[\left(\bmod (m - 1 , M _ {x}) - \frac {M _ {x} - 1}{2}\right) - \left(n _ {t} - \frac {1 + N _ {t}}{2}\right)\right] ^ {2} + d _ {\mathrm{element}} ^ {2} \left(\left\lceil \frac {m}{M _ {x}} \right\rceil - \frac {1 + M _ {z}}{2}\right) ^ {2}}\tag{80}
$$

phase shifts are randomly initialized and held constant, isolating the performance gain directly contributed by joint digital and wave-domain optimization; and 4) Fully Digital Beamforming Scheme (No SIM): which removes the SIM architecture entirely and relies exclusively on conventional digital-domain processing to meet the target objectives and constraints.

The convergence performance of the proposed robust SIM-assisted ISACC system is presented in Fig. 2. It compares the LMI-based and low-complexity phase shift designs for diferent number of targets. Due to the high computational cost of the LMI-based design, we consider the special case of a SIM with only 9 meta-atoms in each layer arranged in a $3 \times 3$ array. As shown, both approaches achieve almost the same performance, with the lowcomplexity design substantially reduces the computational complexity. For $Q = 1$ , the SINR approaches a stable value within a few iterations, whereas the improvement is more gradual for $Q \ = \ 2$ . Increasing the number of targets from one to two substantially reduces the minimum sensing SINR. This drop reflects the limited spatial DoF provided by the small SIM array, which restricts its ability to support multiple sensing targets. Given the comparable performance of both approaches, we will present only the low-complexity design in all subsequent simulations.

Figures 3 and 4 show the convergence behavior of the proposed SIM-assisted ISACC system for diferent numbers of transmit/receive antennas. Fig. 3 presents the objective value $\bar { \varrho } ,$ while Fig. 4 shows the corresponding actual minimum sensing SINR in dB. For $N _ { t } = N _ { r } = 8$ both curves become nearly stable after approximately 8–10 iterations. The cases with $N _ { t } ~ = ~ N _ { r } ~ = ~ 4$ and $N _ { t } = N _ { r } = 6$ improve more gradually until they converge at approximately 35 iterations. Increasing the number of antennas also leads to a lower final objective value and a higher minimum sensing SINR. Specifically, the achieved minimum sensing SINR values are approximately 18.8, 20.6, and 22.3 dB for $N _ { t } = N _ { r } = 4 , 6 .$ , and 8, respectively. This improvement is consistent with the additional spatial DoF available for transmit and receive beamforming. More antennas provide greater flexibility to strengthen the desired sensing signals and suppress interference, thereby improving the sensing performance of the weakest target.

![](images/766576aeb2fb1b21cbd990a409a6d119a11335e2ee3252fc18be8c3b3357d627.jpg)  
Fig. 2. Convergence behavior comparison of the proposed LMI-based and low-complexity phase shift designs in terms of minimum sensing SINR at $P _ { \mathrm { m a x } } = 3 5$ dBm and $M = 3 \times 3$ meta-atoms per layer for $Q \in \{ 1 , 2 \}$ sensing targets.

![](images/924473c0264cae3c3efe2674c65be8ad0d927f4600868c720432c3b931320f4f.jpg)  
Fig. 3. Convergence behavior of the optimization problem objective ϱ¯ for diferent antenna configurations, $N _ { t } = N _ { r } \in \mathsf { \bar { \{ 4 , 6 , 8 \} } }$

The efect of the number of SIM layers on the minimum sensing SINR is presented in Fig. 5 for the proposed scheme as well as other benchmarks. In general, the sensing performance improves as more layers are added. This improvement results from the additional spatial DoF provided by the SIM, which enables more efective wave-domain beamforming and interference control. The achieved performance by the proposed ISACC framework increases from approximately 8 dB with one layer to 35 dB with seven layers. Even with a single SIM layer, it outperforms conventional digital beamforming without a SIM, which provides a constant sensing SINR of about −14 dB. The gain is approximately 22 dB at $L \ = \ 1$ and increases to nearly 50 dB at $L = 7 .$ . Moreover, the proposed design also consistently outperforms the fixed random phase shift scheme. For example, at $L = 1$ , the proposed method achieves about 8 dB, compared with approximately −2 dB for random phase shifts, corresponding to a gain of nearly 10 dB. At $L = 7$ , the proposed design gives a performance of 12 dB above the randomphase benchmark. These results show that optimizing the SIM phases is important. Nevertheless, the random-phase scheme also benefits from increasing the number of layers, since additional layers provide extra spatial DoF even when their phase shifts are not optimized.

![](images/03a73c1081258e5a25259374e1bd273dedcdfd68d6de3c3afee1f530060cdb60.jpg)  
Fig. 4. Convergence behavior of the actual minimum sensing SINR objective in dB for diferent antenna configurations, $N _ { t } ~ = ~ N _ { r } ~ \in$ $\{ 4 , 6 , 8 \}$

![](images/f31bac553aa9900aa1b875f298a8e95a74752cdd8516991ab15d9fce244ab797.jpg)  
Fig. 5. Efect of increasing the number of SIM layers on the achieved sensing performance for the proposed scheme as well as other benchmarks.

Additionally, the sensing-centric and no-covertness schemes represent upper bounds on the achieved sensing performance since they both relax one of the constraints form the formulated problem, where the former removes the communication QoS constraints, while the latter removes the detection error probability constraint. As expected, both relaxed schemes generally achieve higher sensing SINR than the fully constrained ISACC design, although their values are close to the proposed result for some layer numbers.

![](images/a181ae66a3ea1be46ccb798b011047638dc947fad51793ee7d801df15c057779.jpg)  
Fig. 6. Efect of increasing the maximum transmit power on the achieved sensing performance for the proposed scheme as well as other benchmarks.

Figure 6 presents the achieved minimum sensing SINR against the maximum transmit power for the proposed SIM-assisted ISACC system as well as other benchmarks. Across all schemes, the sensing SINR increases monotonically with power, as higher transmit budgets directly yield stronger target echo signals. As mentioned previously, since the sensing-centric and no-covertness baselines relax the communication QoS and covertness constraints, respectively, they represent theoretical upper bounds on the system performance. Again, it is apparent that the proposed scheme operates very close to these un constrained bounds across the entire power range despite enforcing all constraints. Furthermore, it substantially outperforms both the fixed random phase shift baseline and conventional digital beamforming without a SIM. Specifically, at $P _ { \mathrm { m a x } } ~ = ~ 4 0$ dBm, the proposed design achieves a sensing SINR approximately 13 dB higher than the random phase shift approach and 34 dB higher than conventional digital beamforming. These gains highlight the structural advantage of the SIM architecture and the critical importance of optimizing its phase shifts.

Figure 7 illustrates how the number of meta-atoms per layer, M, influences the minimum sensing SINR as a function of the maximum transmit power budget. It is clear that scaling up M from 9 to 25 substantially raises the sensing SINR across all transmit power levels. This behavior is attributed to the fact that a larger M provides finer spatial resolution and greater wavemanipulation capability, enabling tighter beam focusing toward target directions while maintaining compliance with communication and covertness constraints. In particular, at $P _ { \mathrm { m a x } } ~ = ~ 4 0$ dBm, the setup with $M \ = \ 2 5$ achieves an SINR of approximately 30 dB, compared to just 9.5 dB for $M = 9$ . This degradation highlights the limited spatial DoF ofered by a smaller SIM array, which restricts its ability to form directional beams and suppor multiple communication users and multiple sensing targets simultaneously. Moreover, this large performance gap shows that expanding the SIM size ofers a powerful means of compensating for low transmit power budgets.

The minimum sensing SINR versus the maximum transmit power $P _ { \mathrm { m a x } }$ is presented in Fig. 8 for diferent numbers of communication users $K \in \{ 3 , 4 , 5 \}$ . As expected, the sensing SINR increases monotonically with power for all configurations. However, increasing the number of communication users K leads to a notable degradation in sensing performance. This trade-of occurs because serving more communication users requires allocating a larger portion of the power budget and spatial DoF to satisfy their respective QoS constraints, thereby leaving limited resources for target sensing. For example, at $ { P _ { \mathrm { m a x } } } = 4 0 ~  { \mathrm { d B m } }$ , the minimum sensing SINR drops from approximately 30 dB for $K = 3$ to 27.2 dB for $K = 4$ ， and falls sharply to 3.8 dB when $K = 5$ . These results clearly demonstrate the fundamental trade-of between communication and sensing in multi-user ISAC systems.

![](images/27393284c6ae8566a69cd3e7463a1292ee79c589e6302a8320ee046d78f19607.jpg)

Fig. 7. Impact of the number of meta-atoms per layer, $M ,$ on the minimum sensing SINR under varying transmit power budgets.  
![](images/526d5c77e217a26205469f5fe3396843c765449856b1d57af83e45e46f866be6.jpg)  
Fig. 8. Impact of the number of communication $\mathrm { U E s } ,$ K, on the minimum sensing SINR under varying transmit power budgets.

## VI. Conclusion

This paper developed a robust transceiver design for a multi-user, multi-target SIM-assisted ISACC system under bounded CSI uncertainty. The proposed AO framework jointly optimizes the transmit and receive beamformers, sensing covariance matrix, and SIM phases to maximize the worst-case minimum sensing SINR while satisfying the communication QoS, power budget, SIM phase shifts, and covertness constraints. Exact columnspace reductions were derived for the robust sensing LMIs in the transmit- and receive-beamformer updates, while a norm-based phase-update method was introduced to reduce the computational cost. Numerical results show that at the low-complexity phase update closely matches the LMI-based design at substantially lower complexity. Furthermore, at $P _ { \mathrm { m a x } } = 4 0$ dBm, the proposed ISACC framework outperforms the random-phase and the fullydigital beamforming benchmarks by approximately 13 and 34 dB, respectively. In addition, increasing the number of SIM layers from 1 to 7 raises the sensing SINR from approximately 8 to 35 dB, which reflects the potential of SIMs for robust covert ISAC. However, increasing the number of users from 3 to 5 reduces the sensing SINR from approximately 30 to 4 dB at $P _ { \mathrm { m a x } } = 4 0$ dBm, which shows the tradeof between sensing and communications.

## Appendix

## Proof of Proposition 1

To significantly reduce the computational complexity while preserving the exact structure of the robust LMI, we exploit the fact that $\mathbf { G } \in \mathbb { C } ^ { M \times N _ { t } }$ has a low-dimensional column space since generally $N _ { t } < M$ . Let $r _ { G } = \mathrm { R a n k } ( \mathbf { G } )$ and consider the compact singular value decomposition (SVD) of $\mathbf { G } = \mathbf { U } _ { G } \pmb { \Sigma } _ { G } \mathbf { V } _ { G } ^ { H }$ , where $\mathbf { U } _ { G } \in \mathbb { C } ^ { M \times r _ { G } }$ contains an orthonormal basis spanning the column space of G. Let $\mathbf { G } \mathbf { R } _ { x } \mathbf { G } ^ { H } = \mathbf { U } _ { G } \mathbf { T } \mathbf { U } _ { G } ^ { \hat { H } }$ , where the reduced-dimensional matrix $\mathbf { T } \ = \ \mathbf { U } _ { G } ^ { H } \mathbf { G } \mathbf { R } _ { x } \Breve { \mathbf { G } } ^ { H } \mathbf { U } _ { G } \ \in \ \mathbb { C } ^ { r _ { G } \times r _ { G } }$ . Consequently, $\left( { { \bf { G } } { { \bf { R } } _ { x } } { { \bf { G } } ^ { H } } } \right) ^ { T } = { \bf { U } } _ { G } ^ { * } { { \bf { T } } ^ { T } } { \bf { U } } _ { G } ^ { T }$

Using the mixed-product property of the Kronecker product, each $\mathbf { Y } _ { q , j }$ can therefore be factorized as

$$
\mathbf {Y} _ {q, j} = \mathbf {C} _ {j} \left(\mathbf {T} ^ {T} \otimes \mathbf {U} _ {q}\right) \mathbf {C} _ {j} ^ {H},\tag{81}
$$

where ${ \bf C } _ { j } = | \alpha _ { j } | ( { \bf U } _ { G } ^ { * } \otimes { \bf B } )$ . Since for this sub-problem $\mathbf { R } _ { x }$ is fixed, while $\mathbf { U } _ { q }$ is the optimization variable, $\mathbf { C } _ { j }$ is constant with respect to the receive beamforming variables. Hence, defining $\mathbf { C } \ = \ \operatorname { d i a g } \left( \mathbf { C } _ { 1 } , \ldots , \mathbf { C } _ { Q } \right)$ , the original high-dimensional matrix $\mathbf { X } _ { q }$ can be represented exactly as

$$
\mathbf {X} _ {q} = \mathbf {C K} _ {q} \mathbf {C} ^ {H},\tag{82}
$$

where $\mathbf { K } _ { q } \ = \ \operatorname { d i a g } \left( \mathbf { K } _ { q , 1 } , \ldots , \mathbf { K } _ { q , Q } \right)$ , with ${ \bf K } _ { q , j } \ = \ { \bf T } ^ { T } \otimes$ $\mathbf { U } _ { q } , \ j \neq { \bar { q } }$ and $\mathbf { K } _ { q , q } = - \bar { \varrho } \left( \mathbf { T } ^ { T } \otimes \mathbf { \bar { U } } _ { q } \right)$ For further reduction, we perform the compact QR factorization ${ \bf C } = { \bf U } _ { C } { \bf R } _ { C }$ , where $\mathbf { U } _ { C } ^ { H } \mathbf { U } _ { C } = \mathbf { I }$ . Accordingly, $\mathbf { X } _ { q }$ can be rewritten as

$$
\mathbf {X} _ {q} = \mathbf {U} _ {C} \widetilde {\mathbf {K}} _ {q} \mathbf {U} _ {C} ^ {H},\tag{83}
$$

where $\begin{array} { r } { \tilde { \bf K } _ { q } ~ = ~ \mathbf { R } _ { C } \mathbf { K } _ { q } \mathbf { R } _ { C } ^ { H } } \end{array}$ . Furthermore, the reducededimensional nominal uncertainty vector is now expressed as $\widetilde { \mathbf { g } } _ { A } = \mathbf { U } _ { C } ^ { H } \hat { \mathbf { g } } _ { A }$ . Consequently, the original robust LMI ecan be represented in the reduced-dimensional space as in (50). This completes the proof. ■

## References

[1] C.-X. Wang, X. You, X. Gao, X. Zhu, Z. Li, C. Zhang, H. Wang, Y. Huang, Y. Chen, H. Haas, J. S. Thompson, E. G. Larsson, M. D. Renzo, W. Tong, P. Zhu, X. Shen, H. V. Poor, and L. Hanzo, “On the road to 6G: Visions, requirements, key technologies, and testbeds,” IEEE Commun. Surveys Tuts., vol. 25, no. 2, pp. 905–974, 2023.

[2] A. Li and C. Masouros, “Energy-eficient SWIPT: From fully digital to hybrid analog–digital beamforming,” IEEE Trans. Veh. Technol., vol. 67, no. 4, pp. 3390–3405, 2017.

[3] J. An, M. Di Renzo, M. Debbah, and C. Yuen, “Stacked intelligent metasurfaces for multiuser beamforming in the wave domain,” in Proc. IEEE Int. Conf. Commun. (ICC), 2023, pp. 2834–2839.

[4] J. An, M. Di Renzo, M. Debbah, H. V. Poor, and C. Yuen, “Stacked intelligent metasurfaces for multiuser downlink beamforming in the wave domain,” IEEE Trans. Wireless Commun., vol. 24, no. 7, pp. 5525–5538, 2025.

[5] H. Liu, J. An, G. C. Alexandropoulos, D. W. K. Ng, C. Yuen, and L. Gan, “Multi-user MISO with stacked intelligent metasurfaces: A DRL-based sum-rate optimization approach,” IEEE Trans. Cogn. Commun. Netw., vol. 12, pp. 251–266, 2026.

[6] X. Luo, Q. Lin, R. Zhang, H.-H. Chen, X. Wang, and M. Huang, “ISAC—a survey on its layered architecture, technologies, standardizations, prototypes, and testbeds,” IEEE Commun. Surveys Tuts., vol. 28, pp. 485–526, 2026.

[7] D. Wen, Y. Zhou, X. Li, Y. Shi, K. Huang, and K. B. Letaief, “A survey on integrated sensing, communication, and computation,” IEEE Commun. Surveys Tuts., vol. 27, no. 5, pp. 3058–3098, 2025.

[8] H. Niu, J. An, A. Papazafeiropoulos, L. Gan, S. Chatzinotas, and M. Debbah, “Stacked intelligent metasurfaces for integrated sensing and communications,” IEEE Wireless Commun. Lett., vol. 13, no. 10, pp. 2807–2811, 2024.

[9] A. M. Benaya, M. S. Hassan, M. H. Ismail, and T. Landolsi, “Aerial ISAC: A haps-assisted integrated sensing, communications and computing framework for enhanced coverage and security,” IEEE Trans. Green Commun. Netw., vol. 9, no. 4, pp. 2101–2114, 2025.

[10] A. Alselwi, K. Abdullah, O. Khaled, H. Abdulhadi, and A. U. Khan, “Sensing-informed robust beamforming for secure ISAC against mobile passive eavesdroppers,” IEEE Open J. Commun. Soc., vol. 7, pp. 9523–9550, 2026.

[11] A. A. Salem, S. Abdallah, M. Saad, K. Alnajjar, and M. A. Albreem, “Robust secure ISAC: How RSMA and active RIS manage eavesdropper’s spatial uncertainty,” IEEE Trans. Veh. Technol., vol. 75, no. 3, pp. 4383–4398, 2026.

[12] X. Hu, P. Zhao, H. Xiao, T.-X. Zheng, W. Wang, and K. Yang, “Reconfigurable intelligent surface-aided covert communications: A multi-user scenario,” IEEE Trans. Veh. Technol., vol. 74, no. 6, pp. 10 052–10 057, 2025.

[13] A. Papazafeiropoulos, P. Kourtessis, S. Chatzinotas, D. I. Kaklamani, and I. S. Venieris, “Near-field beamforming for stacked intelligent metasurfaces-assisted MIMO networks,” IEEE Wireless Commun. Lett., vol. 13, no. 11, pp. 3035–3039, 2024.

[14] A. M. Benaya, A. A. Nasir, K. M. Rabie, and D. B. da Costa, “Stacked intelligent metasurfaces for near-field multi-user covert communications,” arXiv preprint arXiv:2603.27544, 2026.

[15] Q. Li, M. El-Hajjar, C. Xu, J. An, C. Yuen, and L. Hanzo, “Stacked intelligent metasurface-based transceiver design for near-field wideband systems,” IEEE Trans. Commun., vol. 73, no. 9, pp. 8125–8139, 2025.

[16] E. E. Bahingayi, S. Lin, M. Uysal, M. Di Renzo, and L.- N. Tran, “A refined alternating optimization for sum rate maximization in SIM-aided multiuser MISO systems,” IEEE Wireless Commun. Lett., vol. 15, pp. 1250–1254, 2025.

[17] S. Li, F. Zhang, T. Mao, R. Na, Z. Wang, and G. K. Karagiannidis, “Transmit beamforming design for ISAC with stacked intelligent metasurfaces,” IEEE Trans. Veh. Technol., vol. 74, no. 4, pp. 6767–6772, 2024.

[18] Q. Zhang, Z. Du, Y. Zhao, Y. L. Guan, J. Liu, and C. Yuen, “Joint power allocation and discrete phase-shift optimization for SIM-aided ISAC systems,” IEEE Trans. Veh. Technol., vol. 74, no. 12, pp. 19 795–19 800, 2025.

[19] Z. Wang, H. Liu, J. Zhang, R. Xiong, K. Wan, X. Qian, M. Di Renzo, and R. C. Qiu, “Multi-user ISAC through stacked intelligent metasurfaces: New algorithms and experiments,” in Proc. IEEE Global Commun. Conf. (GLOBECOM). IEEE, 2024, pp. 4442–4447.

[20] H. Niu, J. An, L. Zhang, X. Lei, and C. Yuen, “Enhancing physical layer security for SISO systems using stacked intelligent metasurfaces,” in Proc. IEEE VTS Asia Pac. Wireless Commun. Symp. (APWCS). IEEE, 2024, pp. 1–5.

[21] H. Niu, X. Lei, J. An, L. Zhang, and C. Yuen, “On the eficient design of stacked intelligent metasurfaces for secure SISO transmission,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 60–70, 2025.

[22] Z. Xie, J. Sun, Y. Yao, Z. Lu, W. Xiao, and Y. Jin, “Covert ISAC with SIMs: A deep reinforcement learning approach empowered by generative difusion model,” IEEE Sensors J., 2026.

[23] Y. Zhang, W. Ni, J. Wang, W. Tang, M. Jia, Y. C. Eldar, and D. Niyato, “Robust transceiver design for covert integrated sensing and communications with imperfect CSI,” IEEE Trans. Commun., vol. 73, no. 9, pp. 8016–8031, 2025.

[24] S. ul Hassan, J. An, F. Niaz, and Z. Jin, “Robust multiuser downlink beamforming for stacked intelligent metasurfaces with imperfect CSI,” IEEE Wireless Commun. Lett., vol. 15, pp. 4847–4851, 2026.

[25] X. Lin, Y. Rivenson, N. T. Yardimci, M. Veli, Y. Luo, M. Jarrahi, and A. Ozcan, “All-optical machine learning using difractive deep neural networks,” Science, vol. 361, no. 6406, pp. 1004–1008, 2018.

[26] C. Liu, Q. Ma, Z. J. Luo, Q. R. Hong, Q. Xiao, H. C. Zhang, L. Miao, W. M. Yu, Q. Cheng, L. Li et al., “A programmable difractive deep neural network based on a digital-coding metasurface array,” Nat. Electron., vol. 5, no. 2, pp. 113–122, 2022.

[27] T. Zhou, K. Xu, G. Hu, C. Li, X. Xia, C. Wei, and Y. Chen, “STAR-RIS-empowered integrated sensing and covert communication system with movable elements: Joint robust beamforming and element deployment design,” IEEE Trans. Cogn. Commun. Netw., vol. 11, no. 5, pp. 2893–2909, 2025.

[28] J. Liu, G. Yang, Y. Liu, and X. Zhou, “RIS empowered nearfield covert communications,” IEEE Trans. Wireless Commun., vol. 23, no. 10, pp. 15 477–15 492, 2024.

[29] S. Yan, Y. Cong, S. V. Hanly, and X. Zhou, “Gaussian signalling for covert communications,” IEEE Trans. Wireless Commun., vol. 18, no. 7, pp. 3542–3553, 2019.

[30] Y. Liu, Z. Wang, J. Xu, C. Ouyang, X. Mu, and R. Schober, “Near-field communications: A tutorial review,” IEEE Open J. Commun. Soc., vol. 4, pp. 1999–2049, 2023.

[31] S. Boyd, L. El Ghaoui, E. Feron, and V. Balakrishnan, Linear matrix inequalities in system and control theory. SIAM, 1994.

[32] M. Grant, S. Boyd, and Y. Ye, “CVX: Matlab software for disciplined convex programming,” 2009.

[33] J. Watrous et al., The theory of quantum information. Cambridge university press Cambridge, 2018, vol. 1.
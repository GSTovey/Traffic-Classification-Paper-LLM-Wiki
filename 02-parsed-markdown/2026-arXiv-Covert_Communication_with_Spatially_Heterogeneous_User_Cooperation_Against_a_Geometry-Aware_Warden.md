# Covert Communication with Spatially Heterogeneous User Cooperation Against a Geometry-Aware Warden

Hyeonsik Yeom and Jinyoung Lee

Abstract—This paper investigates covert communication in which a single covert user is assisted by multiple spatially distributed non-covert users against a geometry-aware warden. Unlike prior works based on receiver-centric activation, homogeneous channels, or averaged geometry, the proposed framework retains the individual user-to-warden large-scale fading coefficients in both cooperative user activation and the warden’s detection analysis. Under the adopted analytical formulation for large-scale user deployments, we establish an on–off activation structure that balances the interference caused at Bob and the interference effectiveness at warden. Based on the resulting aggregate-interference statistics, we derive a closed-form approximation of the detection error probability, the detection threshold that minimizes it, and the minimum number of cooperative users required to satisfy the covert constraint. Then, we reduce the original high-dimensional power-control problem to a onedimensional piecewise search and develop a low-complexity algorithm that avoids resolution-dependent grid search. The analysis shows that greater warden-side spatial dispersion can reduce the required cooperative users, whereas a larger average userto-warden distance increases it. Numerical results validate the analysis and show that finite-sample detection approaches the large-sample benchmark, while imperfect user-to-Bob channel estimation mainly reduces the achievable rate through activation errors.

Index Terms—Covert communication, physical layer security, piecewise optimization, spatial heterogeneity, wireless communications

## I. INTRODUCTION

With the explosive proliferation of wireless devices and the Internet of Things (IoT), modern wireless networks are required to manage enormous volumes of sensitive information. At the same time, the continuous growth in wireless connectivity and device density increases the exposure of communication channels, making the wireless medium highly vulnerable to adversarial surveillance and eavesdropping. To address these threats, physical layer security (PLS) has emerged as a complementary paradigm to cryptography, exploiting the intrinsic characteristics of wireless channels at the physical layer to provide confidentiality and resilience directly at the signal level [1]–[3]. Among the various PLS techniques, covert communication has recently attracted considerable attention for its unique objective. Unlike conventional cryptographic approaches that protect the content of a message, covert communication aims to conceal the existence of a transmission from adversarial detectors, typically called a warden. In other words, the transmitter seeks to ensure an extremely low probability that detectors can correctly decide whether a transmission is occurring, while simultaneously guaranteeing a desired data rate for the legitimate receiver. Such concealment capability is essential for diverse mission-critical and privacysensitive applications, including military operations, secure IoT networks, and covert ad hoc communications [1].

Early covert transmission techniques, including direct sequence spread spectrum, frequency hopping, and chirp spread spectrum, were primarily implementation-driven, motivating theoretical studies on the fundamental limits of covert communication. In [4, Theorem 1], Bash et al. introduced the square root law for additive white Gaussian noise (AWGN) channels. The law states that, under the classical AWGN model without additional uncertainty at a warden, no more than $\mathcal { O } ( \sqrt { n } )$ bits can be transmitted reliably and covertly within n channel uses. Subsequent works [5]–[11] generalized this principle to binary symmetric, discrete memoryless, multiple-access, broadcast, and interference channels, thus establishing the theoretical foundation of covert communication.

Under this classical model, the achievable transmission rate approaches zero as the number of channel uses increases. Motivated by this limitation, numerous studies have explored ways to achieve a positive covert rate by introducing uncertainty at a warden. Major approaches include exploiting channel uncertainty [12], [13], inducing interference via relays or jammers [14]–[19], and utilizing full-duplex receivers [20], [21]. Recent studies have also investigated the inherent directionality of mmWave systems [22], the spatial reconfigurability of movable antennas [23], and the mobility-enabled adaptability of UAV networks [24]–[26] to enhance covertness.

Covert communication has also been studied in multiuser networks, particularly with respect to random user locations, interference, and spatial topology. He et al. [27] analyzed a homogeneous Poisson point process network in which numerous transmitters act as uncoordinated interferers. They showed that, in the interference-limited regime, the covert rate approaches a finite bound as the interference level increases, indicating that background interference does not provide unbounded covert-rate gains. Soltani et al. [28] selected the friendly node closest to a warden to generate artificial noise, thereby increasing the warden’s detection uncertainty. Although these studies provide valuable insights into the statistical behavior of large-scale stochastic networks, they consider either uncoordinated ambient interference or individually selected friendly nodes, rather than coordinated and jointly optimized cooperation among multiple users.

More recent studies focus on covert communication assisted by multiple cooperative nodes, where legitimate users deliberately transmit interference signals to confuse a warden [29]– [32]. Zheng et al. [29] proposed a distributed cooperative jamming scheme in which friendly jammers are activated according to their instantaneous channel conditions toward the legitimate receiver, and jointly optimized the selection thresh old and transmission rate to maximize the covert throughput. Although the individual helper-to-receiver and helperto-warden distances are modeled, the activation rule depends only on the helper-to-receiver channel condition, and thus the warden-side geometry is not used to select the helpers that are effective in confusing the warden. Building on the benefits of multi-user cooperation, Lee et al. [30] further developed a joint power-control design for Alice and the cooperative users. In particular, they derived closed-form expressions that explicitly characterize the relationships among system parameters and proposed a low-complexity optimization algorithm. Later, [31] incorporated channel correlation and proposed a scalable Q learning-based algorithm. However, the frameworks in [30], [31] assume homogeneous large-scale channel conditions and therefore do not distinguish the cooperative users according to their individual user-to-warden large-scale fading conditions. Yeom et al. [32] further considered users located at unequal distances from Bob in the system model. However, for tractable analysis, the distinct user-to-Bob and user-towarden channel variances were replaced by common average parameters, which prevents the resulting analytical design from retaining the individual spatial characteristics of the cooperative users. These limitations are important because cooperative users that cause similar interference at Bob may provide substantially different interference at the warden. Consequently, a receiver-centric or averaged-geometry design may select ineffective users or inaccurately characterize the warden’s aggregate-interference statistics, which can lead to an inaccurate estimate of the minimum detection error probability (DEP) and the minimum number of cooperative users. This may activate more cooperative users than necessary, increase the interference at Bob, and reduce the achievable covert rate.

Motivated by these limitations, this work investigates covert communication in which a single covert user, Alice, is assisted by multiple spatially distributed non-covert users against a geometry-aware warden. Unlike the previous receiver-centric, homogeneous, and averaged-geometry frameworks, the proposed design retains the individual user-to-warden largescale fading coefficients in both cooperative-user activation and warden’s detection analysis, which enables the proposed framework to treat spatial heterogeneity as a design factor rather than merely as a deployment detail. Accordingly, the main challenge lies not in simply substituting heterogeneous channel parameters into an existing model. Rather, it lies in developing a unified analytical framework in which each user’s warden-side geometry is incorporated into cooperative user activation, the resulting selected cooperative user set is used to characterize the warden’s aggregate-interference statistics and minimum DEP, and these analytical relationships are subsequently exploited to determine the minimum number of cooperative users and reformulate the original highdimensional power-control problem. The major contributions are summarized as follows:

1) Spatial-heterogeneity-aware cooperative design: Under the adopted analytical formulation for large-scale user deployments, we establish an on–off activation structure that jointly considers the interference caused at Bob and the interference effectiveness at the warden. Thus, the proposed design directly incorporates the individual warden-side geometry into cooperativeuser selection. The same activation structure can also be implemented using estimated user-to-Bob channels, enabling the impact of channel estimation errors to be examined.

2) Detection and cooperation analysis under spatial heterogeneity: We characterize the warden’s aggregate interference by retaining the individual large-scale fading conditions of the activated users and reflecting how the activation rule changes the composition of the cooperative user set. Based on this characterization, we derive a closed-form approximation of the DEP, the detection threshold that minimizes the DEP, and the minimum number of cooperative users required to satisfy the covert constraint. We further provide a compact approximation and recover the homogeneous deployment as a special case.

3) Low-complexity optimization algorithm: Based on the derived relationships among Alice’s transmit power, the minimum number of cooperative users, and the activation threshold, we reduce the original high-dimensional problem to a one-dimensional piecewise search. The proposed algorithm evaluates only the analytically relevant candidates, with computational complexity dominated by a single sorting operation, and avoids the resolution dependence of conventional grid-based search.

4) Design insights under spatial heterogeneity: The analysis shows that covertness depends on the balance between Alice’s received-energy shift and the uncertainty of the aggregate cooperative interference. Greater warden-side spatial dispersion reduces the minimum number of cooperative users, whereas a larger average user-to-warden distance increases it. Homogeneous or averaged-geometry analyses may therefore overestimate the cooperation requirement and cause unnecessary interference at Bob. The finite-sample DEP approaches the large-sample benchmark as the number of observations increases, while imperfect user-to-Bob channel estimation mainly reduces the achievable rate through cooperative user activation errors.

The remainder of this paper is organized as follows. Section II presents the system model and problem formulation. Sections III–V establish the on–off activation structure, analyze the warden’s detection performance, and develop the piecewise search algorithm, respectively. Section VI provides numerical validation, and Section VII concludes the paper.

## II. SYSTEM MODEL AND PROBLEM FORMULATION

## A. System Model

We consider a covert communication network where a single covert user, Alice, is assisted by multiple non-covert cooperative users. The network consists of Alice, M noncovert users, a base station Bob, and a warden Willie, as illustrated in Fig. 1. Alice transmits the covert signal over the covert carrier $f _ { \mathrm { a } } .$ Each non-covert user $U _ { m }$ normally communicates with Bob over its own orthogonal carrier $f _ { m } .$ A subset of non-covert users is selected as cooperative users to assist in hiding Alice’s signal from detection at Willie by transmitting interference over $f _ { \mathrm { a } }$

In this work, we consider a large-scale wireless network comprising a large number of static or slowly moving nodes, as commonly encountered in IoT deployments. Owing to the low mobility of the nodes, the channel coherence interval is assumed to be sufficiently long to accommodate the transmission of a long codeword. Furthermore, a large number of nodes are assumed to participate in the wireless communication process, i.e., $M \gg 1$ . The channel coefficients are modeled as circularly symmetric complex Gaussian random variables, and hence, the corresponding channel magnitudes follow a Rayleigh distribution. The channel from node x to node $y$ at carrier frequency z is denoted by

$$
h _ {x, y} ^ {z} \sim \mathcal {C N} (0, \lambda_ {x, y}), \quad x, y \in \{\mathrm{a,b}, m, \mathrm{w} \}, z \in \{\mathrm{a}, m \}\tag{1}
$$

where $\lambda _ { x , y }$ indicates the large-scale fading coefficient, and the indices $\mathrm { a } , \mathrm { b } , m ,$ , and w represent Alice, Bob, $U _ { m }$ , and Willie, respectively. Now, for covert communication, we focus on the frequency band $f _ { \mathrm { a } }$ , and we omit the superscript. We assume a single-slope path-loss model, and thus, the large-scale fading coefficient is expressed as $\lambda _ { x , y } ~ = ~ \beta _ { 0 } d _ { x , y } ^ { - \alpha }$ , where $\beta _ { 0 }$ is the reference channel gain, α is the path-loss exponent, and $d _ { x , y }$ denotes the Euclidean distances between nodes x and y. The spatial heterogeneity considered in this work is captured by the user-dependent large-scale fading coefficients $\{ \bar { \lambda } _ { m , \mathrm { b } } \} _ { m = 1 } ^ { M }$ and $\{ \lambda _ { m , \mathrm { w } } \} _ { m = 1 } ^ { M }$ , which characterize the large-scale strengths of the cooperative links toward Bob and Willie, respectively.

The channel estimation process consists of two phases. First, Bob broadcasts pilot signals to all users, from which each node estimates the channel from Bob to itself. Second, each non-covert user transmits a secret orthogonal pilot signal over $f _ { \mathrm { a } }$ [29], [33]. The use of secret orthogonal pilot signals by each non-covert user enables Bob to estimate the channel between the non-covert user and Bob, whereas Willie cannot. The estimated channel at Bob is modeled as

$$
\hat {h} _ {m, \mathrm{b}} = \sqrt {1 - \rho_ {e}} h _ {m, \mathrm{b}} + \sqrt {\rho_ {e}} u _ {m, \mathrm{b}},\tag{2}
$$

where $u _ { m , \mathrm { b } } \sim \mathcal { C N } ( 0 , \lambda _ { m , \mathrm { b } } )$ is independent of $h _ { m , \mathrm { b } }$ , and $\rho _ { e } \in$ [0, 1] denotes the channel estimation error level.

In addition, $\mathcal { H } _ { 0 }$ and $\mathcal { H } _ { 1 }$ indicate the hypotheses that Alice does not transmit or transmits a covert message, respectively. The received signal at Bob $y [ t ]$ is given by

$$
y [ t ] = \left\{ \begin{array}{l l} \sum_ {m = 1} ^ {M} \sqrt {P _ {m}} h _ {m, \mathrm{b}} x _ {m} [ t ] + n _ {\mathrm{b}} [ t ], & \mathcal {H} _ {0} \\ \sqrt {P _ {\mathrm{a}}} h _ {\mathrm{a,b}} x _ {\mathrm{a}} [ t ] & \\ + \sum_ {m = 1} ^ {M} \sqrt {P _ {m}} h _ {m, \mathrm{b}} x _ {m} [ t ] + n _ {\mathrm{b}} [ t ], & \mathcal {H} _ {1} \end{array} \right.,\tag{3}
$$

![](images/599a79bc106c2842ea75dea0b0f9b2387073e3a0328aa31e91a3e0614110eb41.jpg)  
Fig. 1. Illustration of the proposed system model. (a) Spatially heterogeneous uplink scenario. (b) Cooperative transmission and detection model.

where both $x _ { \mathrm { a } } [ t ]$ and $x _ { m } [ t ]$ are assumed to be complex Gaussian random variables with zero-mean unit-variance. The parameters $P _ { \mathrm { a } }$ and $P _ { m }$ represent the transmit power of Alice and $U _ { m } ,$ , respectively, and $\mathbf { \tilde { \Sigma } } _ { n _ { \mathrm { b } } [ t ] } \sim \mathcal { C N } ( 0 , \sigma _ { \mathrm { b } } ^ { 2 } )$ denotes AWGN at Bob. Similarly, the received signal at Willie over $f _ { \mathrm { a } }$ is given by

$$
z [ t ] = \left\{ \begin{array}{l l} \sum_ {m = 1} ^ {M} \sqrt {P _ {m}} h _ {m, \mathrm{w}} x _ {m} [ t ] + n _ {\mathrm{w}} [ t ], & \mathcal {H} _ {0} \\ \sqrt {P _ {\mathrm{a}}} h _ {\mathrm{a}, \mathrm{w}} x _ {\mathrm{a}} [ t ] & \\ \quad + \sum_ {m = 1} ^ {M} \sqrt {P _ {m}} h _ {m, \mathrm{w}} x _ {m} [ t ] + n _ {\mathrm{w}} [ t ], & \mathcal {H} _ {1} \end{array} \right.,\tag{4}
$$

where $n _ { \mathrm { w } } [ t ] \sim \mathcal { C N } ( 0 , \sigma _ { \mathrm { w } } ^ { 2 } )$ stands for AWGN at Willie.

## B. Detection at Willie

Willie infers the presence of covert data transmission from Alice based on his observation $\mathbf { z } = [ z [ 1 ] , z [ 2 ] , \dots , z [ N ] ] ^ { T }$ . As introduced in Section II-A, Willie is confronted with a binary hypothesis testing problem consisting of two hypotheses $\mathcal { H } _ { \mathrm { 0 } }$ and $\mathcal { H } _ { 1 }$ . Let $\mathcal { D } _ { 1 }$ and $\mathcal { D } _ { 0 }$ denote Willie’s decisions in favor of $\mathcal { H } _ { 1 }$ and $\mathcal { H } _ { 0 } .$ , respectively. For a detection threshold $\gamma ,$ the false-alarm and miss-detection probabilities are defined as

$$
P _ {\mathrm{FA}} (\gamma) = \operatorname * {P r} (\mathcal {D} _ {1} | \mathcal {H} _ {0}), \qquad P _ {\mathrm{MD}} (\gamma) = \operatorname * {P r} (\mathcal {D} _ {0} | \mathcal {H} _ {1}).
$$

Under the conventional equal prior assumption [18], [34], the DEP can be defined as

$$
\zeta \triangleq P _ {\mathrm{FA}} (\gamma) + P _ {\mathrm{MD}} (\gamma).\tag{5}
$$

Since Willie chooses the threshold that minimizes the DEP, the covert constraint is imposed on the minimum DEP, i.e., $\zeta _ { \mathrm { m i n } } \geq 1 - \epsilon$ , where $\epsilon > 0$ is arbitrarily small [21], [30], [31].

According to the Neyman–Pearson Lemma [35], the likelihood ratio test (LRT) is optimal for the considered binary hypothesis test and is expressed as

$$
\frac {\prod_ {t = 1} ^ {N} f \big (z [ t ] ; \mathcal {H} _ {1} \big)}{\prod_ {t = 1} ^ {N} f \big (z [ t ] ; \mathcal {H} _ {0} \big)} \stackrel {{\mathcal {D} _ {1}}} {{\gtrless}} \gamma ,\tag{6}
$$

where $f ( \cdot )$ represents the probability density function (PDF) and $N$ denotes the codeword length (number of channel uses).

For a general cooperative power profile $\mathbf { P } = ( P _ { 1 } , \dots , P _ { M } )$ define the instantaneous received powers at Willie as $\rho _ { 0 } ( \mathbf { P } ) =$ $\begin{array} { r } { \sum _ { m = 1 } ^ { M } P _ { m } | h _ { m , \mathrm { w } } | ^ { 2 } + \sigma _ { \mathrm { w } } ^ { 2 } } \end{array}$ and $\rho _ { 1 } ( \mathbf { P } ) = \rho _ { 0 } ( \mathbf { P } ) + P _ { \mathrm { a } } | h _ { \mathrm { a , w } } | ^ { 2 } .$ Under the adopted Gaussian signaling model, conditioned on a cooperative power profile P, Willie’s received samples satisfy $z [ t ] \quad | \quad \mathcal { H } _ { i } , \mathbf { P } \ \sim \ \mathcal { C N } ( 0 , \rho _ { i } ( \mathbf { P } ) )$ , for $i \in \{ 0 , 1 \}$ Hence, the conditional likelihood can be written as p(z | $\mathbf { \mathcal { H } } _ { i } , \mathbf { P } ) \mathbf { \mathcal { \phi } } = \mathbf { \phi } \left( \pi \rho _ { i } ( \mathbf { P } ) \right) ^ { - N } \exp \left( - N T _ { \mathrm { w } } / \rho _ { i } ( \mathbf { P } ) \right)$ , where $T _ { \mathrm { w } }$ $\textstyle \sum _ { t = 1 } ^ { N } | z [ t ] | ^ { 2 } / N$ . Therefore, the likelihood depends on z only through $T _ { \mathrm { w } }$ , and $T _ { \mathrm { w } }$ is a sufficient statistic for Willie’s LRT. Moreover, since $\rho _ { 1 } ( { \mathbf { P } } ) > \rho _ { 0 } ( { \mathbf { P } } )$ , the conditional likelihood ratio is increasing monotonically in $T _ { \mathrm { w } }$ . Consequently, the LRT can be equivalently reduced to a test of the received energy, i.e., $T _ { \mathrm { w } } \mathcal { \tilde { ( } \mathrm { k } _ { 0 } ) }$ For finite $N ,$ conditioned on $\rho _ { i } ( \mathbf { P } )$ under $\mathcal { H } _ { i } , i \in \{ 0 , \stackrel { \ldots } { 1 } \}$ , the received-energy statistic satisfies

$$
T _ {\mathrm{w}} \mid \rho_ {i} (\mathbf {P}) = \rho_ {i} (\mathbf {P}) \frac {\chi_ {2 N} ^ {2}}{2 N}, \qquad i \in \{0, 1 \},\tag{7}
$$

where $\chi _ { 2 N } ^ { 2 }$ denotes a chi-square random variable with 2N degrees of freedom. This expression explicitly captures the finite-sample fluctuation of Willie’s energy statistic within a fading block. Using the test of received energy, the finite-N DEP for a given detection threshold $\gamma$ is written as

$$
\zeta_ {N} (\gamma) = \operatorname * {P r} (T _ {\mathrm{w}} > \gamma | \mathcal {H} _ {0}) + \operatorname * {P r} (T _ {\mathrm{w}} \leq \gamma | \mathcal {H} _ {1}).\tag{8}
$$

Willie is assumed to choose the threshold that minimizes the DEP, i.e.,

$$
\zeta_ {N, \min} = \min _ {\gamma} \zeta_ {N} (\gamma).\tag{9}
$$

The closed-form analysis in the following sections uses the large-N benchmark, i.e., $\zeta _ { \mathrm { m i n } } .$ , where $\chi _ { 2 N } ^ { 2 } / ( 2 N )  1$ almost surely [36, Sec. 5.5]. This benchmark gives Willie an asymptotically accurate estimate of the instantaneous received power $\rho _ { i }$ through $T _ { \mathrm { w } }$ and thus is conservative from the viewpoint of the legitimate users, i.e., Alice and Bob. The finite-N DEP is separately evaluated in the numerical results to quantify practical finite-sample detection effects. Even for a geometryaware Willie, the aggregate interference remains random due to small-scale fading and power profile uncertainty, with its statistics shaped by the users’ spatial heterogeneity.

## C. Optimization Problem

This work considers an instantaneous transmission-rate maximization problem under a covert constraint. The communication parameters are adapted to the channel realization available at Bob, and hence the rate metric used in this work should be interpreted as an instantaneous achievable transmission rate conditioned on the realized channels. For a given channel realization and transmit-power profile, the instantaneous achievable transmission rate of Alice is defined as

$$
R = \log_ {2} \left(1 + \frac {P _ {\mathrm{a}} | h _ {\mathrm{a,b}} | ^ {2}}{\sum_ {m = 1} ^ {M} P _ {m} | h _ {m , \mathrm{b}} | ^ {2} + \sigma_ {\mathrm{b}} ^ {2}}\right),\tag{10}
$$

where the denominator includes the aggregate interference caused at Bob by the cooperative transmissions of the noncovert users. Then, the transmit power optimization problem can be formulated as

$$
(P _ {\mathrm{a}} ^ {*}, \mathbf {P} ^ {*}) = \underset {P _ {\mathrm{a}}, \mathbf {P}} {\operatorname{argmax}} R\tag{11a}
$$

$$
\mathrm{s.t.} \zeta_ {\mathrm{min}} \geq 1 - \epsilon\tag{11b}
$$

$$
0 \leq P _ {\mathrm{a}} \leq P _ {\mathrm{max}}\tag{11c}
$$

$$
0 \leq P _ {m} \leq P _ {\max}, \quad \forall m,\tag{11d}
$$

where $P _ { \mathrm { m a x } }$ is the maximum transmit power and ϵ is the tolerable covertness error. The covert constraint in (11b) is imposed through Willie’s minimum DEP, where Willie chooses the detection threshold that minimizes his detection error probability, and the transmit power constraints are given in (11c) and (11d), respectively.

The problem in (11) is challenging for several reasons. First, it jointly optimizes Alice’s transmit power and the Mdimensional non-covert user power profile, so the number of optimization variables grows linearly with the network size. For the considered networks with hundreds to thousands of users, a direct search over this (M + 1)-dimensional space is computationally prohibitive. Second, the objective function has a fractional SINR structure in which the two sets of variables act in opposite directions. $P _ { \mathrm { a } }$ enters the numerator of Bob’s SINR, while P enters its denominator, and the covert constraint couples them in the reverse sense. That is, increasing $P _ { \mathrm { a } }$ improves Alice’s received signal power at Bob but makes the covert transmission more distinguishable at Willie, whereas increasing P improves covertness by increasing the uncertainty of the aggregate interference at Willie but degrades Bob’s received SINR. Third, the covert constraint is not a simple convex power or SINR constraint. It is a statistical constraint determined after Willie optimizes his detection threshold. Finally, under spatial heterogeneity, the aggregate cooperative interference at Willie depends on the selected users’ individual large-scale fading coefficients $\{ \lambda _ { m , \mathrm { w } } \} _ { m = 1 } ^ { M }$ . These challenges motivate the structural analysis of power profile for the cooperative user and Willie’s detection performance in the following sections.

## III. ON–OFF COOPERATIVE USER ACTIVATION

In this section, we analyze the cooperative user activation structure for a given Alice transmit power $P _ { \mathrm { a } }$ . The purpose is to reduce the M-dimensional non-covert-user power profile $\mathbf { P } = ( P _ { 1 } , \ldots , P _ { M } )$ in (11) to a more tractable and simpler form. The structural result derived in this section is established under the adopted large-M analytical formulation for the fixed $P _ { \mathrm { a } }$ problem. Then, the original optimization problem is reformulated in terms of Alice’s transmit power $P _ { \mathrm { a } }$ and the activation threshold τ. For notational convenience, define the activation metric of the m-th non-covert user as

$$
r _ {m} \triangleq \frac {| h _ {m , \mathrm{b}} | ^ {2}}{\lambda_ {m , \mathrm{w}}}, \quad m = 1, \ldots , M.\tag{12}
$$

A smaller value of $r _ { m }$ indicates that the user causes relatively weak interference at Bob while providing a relatively strong interference contribution at Willie.

Proposition 1. Under the adopted large-M analytical formulation, for a given $P _ { \mathrm { a } } ,$ , the cooperative-user power profile that minimizes Bob-side interference while satisfying the covert constraint has the following on–off activation structure, i.e.,

$$
P _ {m} ^ {*} = \left\{ \begin{array}{l l} P _ {\max}, & r _ {m} \leq \tau \\ 0, & o t h e r w i s e \end{array} \right.,\tag{13}
$$

where τ denotes the activation threshold.

Proof. The proof is provided in Appendix A.

□

Based on the on–off scheme presented in Proposition 1, the activation threshold τ determines the set of cooperative users as

$$
\mathcal {S} = \{m: r _ {m} \leq \tau \},\tag{14}
$$

and the number of cooperative users is given by $K = | S |$ Increasing τ activates more non-covert users and increases the aggregate interference observed at Willie, which improves the concealment of Alice’s covert signal. However, it also increases the interference at Bob and degrades the achievable rate. Therefore, for a given $P _ { \mathrm { a } } ,$ the threshold should be selected as the smallest value that satisfies the covert constraint. After the optimization, Bob broadcasts the control parameters, including $P _ { \mathrm { a } } ^ { \star }$ and $\tau ^ { \star } = \tau ( P _ { \mathrm { a } } ^ { \star } )$ ), to the users. The on–off cooperation rule and the broadcast control parameters, including $P _ { \mathrm { a } } ^ { \star }$ and $\tau ^ { \star }$ , are not treated as secret information and can be overheard by Willie without any active participation in the network. Since $\lambda _ { m , \mathrm { w } }$ is a long-term geometry-dependent quantity, Willie can infer it by passively overhearing the regular uplink transmissions of the non-covert users, where the long-term average received power averages out the smallscale fading. Meanwhile, the instantaneous user-to-Bob channel gains are estimated through the secret orthogonal pilots described in Section II-A and are thus not observable by Willie. Hence, the exact value of K is granted to Willie as a conservative worst-case assumption. Nevertheless, the set of cooperative users and the aggregate interference remain random because the activation rule depends on the non-covert user-to-Bob channel, $h _ { m , \mathrm { b } }$ . Furthermore, the proposed on–off rule is different from those in existing studies [30]–[32]. The existing schemes mainly determine the cooperative users based on the user-to-Bob channel gains. In contrast, the proposed rule uses $r _ { m } ,$ which jointly accounts for the interference caused at Bob and the interference observed by Willie. Based on Proposition 1, the original optimization problem in (11) can be reformulated as

$$
(P _ {\mathrm{a}} ^ {\star}, \tau^ {\star}) = \underset {P _ {\mathrm{a}}, \tau} {\operatorname{argmax}} R\tag{15a}
$$

$$
\mathrm{s.t.} \quad \zeta_ {\mathrm{min}} \geq 1 - \epsilon ,\tag{15b}
$$

$$
0 \leq P _ {\mathrm{a}} \leq P _ {\mathrm{max}}.\tag{15c}
$$

Note that the reformulated problem in (15) has only two optimization variables, whereas the original problem in (11) involves $M + 1$ optimization variables. Consequently, owing to Proposition 1, a much simpler optimization problem can be obtained.

Remark 1. When Bob has imperfect estimates of noncovert user-to-Bob channels, the same on–off structure can be implemented using the estimated activation metric, $\hat { r } _ { m } =$ $| \hat { h } _ { m , \mathrm { b } } | ^ { 2 } / \lambda _ { m , \mathrm { w } }$ . Then, Bob applies the on–off rule by replacing $r _ { m }$ with $\hat { r } _ { m }$ . This preserves the on–off cooperative user activation structure. However, the channel estimation error can make $\hat { S } = \{ m : \hat { r } _ { m } \leq \tau \}$ different from $S = \{ m : r _ { m } \leq \tau \}$ If some users satisfy $\hat { r } _ { m } \leq \tau$ but $r _ { m } > \tau$ , they are activated although they are unfavorable under the true channel, thereby increasing the actual interference at Bob and reducing the achievable rate.

The next section analyzes Willie’s detection performance by accounting for the interference statistics induced by the activation rule.

## IV. ANALYSIS OF DETECTION AT WILLIE

In this section, we derive a closed-form expression of the minimum DEP and analyze its characteristics. In particular, we determine the optimal detection threshold $\gamma ^ { * }$ that minimizes the DEP, resulting in the closed-form expression of ζ<sub>min</sub>. Furthermore, based on the closed-form expression of $\zeta _ { \mathrm { m i n } } ,$ we derive the minimum number of cooperative users and the corresponding activation threshold required to satisfy the covert constraint, i.e., $\zeta _ { \mathrm { m i n } } ~ \ge ~ 1 - \epsilon .$ , both in closed-form expressions.

According to the on–off scheme in Proposition 1, the cooperative users transmit interference signals with $P _ { m } = P _ { \operatorname* { m a x } } ,$ while the other users do not transmit any interference signals, $\mathrm { i } . \mathrm { e } . , P _ { m } = 0$ . Then, under the on–off scheme in Proposition 1, the test statistic, $T _ { \mathrm { w } }$ is expressed as

$$
T _ {\mathrm{w}} = \left\{ \begin{array}{l l} \sum_ {i = 1} ^ {K} P _ {\max} | h _ {m _ {i}, \mathrm{w}} | ^ {2} + \sigma_ {\mathrm{w}} ^ {2}, & \mathcal {H} _ {0}, \\ \sum_ {i = 1} ^ {K} P _ {\max} | h _ {m _ {i}, \mathrm{w}} | ^ {2} + P _ {\mathrm{a}} | h _ {\mathrm{a}, \mathrm{w}} | ^ {2} + \sigma_ {\mathrm{w}} ^ {2}, & \mathcal {H} _ {1}, \end{array} \right.\tag{16}
$$

where $m _ { i } \ \in \ \{ 1 , 2 , \ldots , M \}$ denotes the index of the i-th cooperative user sorted in ascending order of the ratio between the channel gain and the large-scale fading coefficient, i.e., $r _ { m _ { i } } ~ \ge ~ r _ { m _ { i } }$ for $i \geq j .$ . It is noteworthy that the selected indices $\{ m _ { i } \} _ { i = 1 } ^ { K }$ are determined by this ordering rule and are not generally equivalent to a uniformly random subset of size K. Conditioned on the selected indices $\{ m _ { i } \} _ { i = 1 } ^ { K }$ , since each channel gain $| h _ { m _ { i } , \mathrm { w } } | ^ { 2 }$ follows a Gamma distribution, and the sum of independent random variables is represented by the convolution of their distributions, the shifted test statistic $T _ { \mathrm { w } } - \sigma _ { \mathrm { w } } ^ { 2 }$ is expressed as

$$
T _ {\mathrm{w}} - \sigma_ {\mathrm{w}} ^ {2} \sim \left\{ \begin{array}{l l} \circledast_ {i = 1} ^ {K} \Gamma (1, \lambda_ {m _ {i}, \mathrm{w}} P _ {\max}), & \mathcal {H} _ {0}, \\ \circledast_ {i = 1} ^ {K} \Gamma (1, \lambda_ {m _ {i}, \mathrm{w}} P _ {\max}) * \Gamma (1, \lambda_ {\mathrm{a}, \mathrm{w}} P _ {\mathrm{a}}), & \mathcal {H} _ {1}, \end{array} \right.\tag{17}
$$

where $\Gamma ( a , b )$ represents a Gamma distribution with shape parameter a and scale parameter $b , *$ denotes the convolution operator between PDFs of two random variables, and $\boldsymbol { \mathfrak { E } } _ { i = 1 } ^ { K }$ indicates the successive convolution of the PDFs of K random variables, i.e., $\circledast _ { k = 1 } ^ { K } A _ { k } = A _ { 1 } \ast A _ { 2 } \ast \cdot \cdot \cdot \ast A _ { K }$ . Based on the probabilistic distribution of $T _ { \mathrm { w } } - \sigma _ { \mathrm { w } } ^ { 2 }$ in (17), a closed-form expression for the DEP in (8) is derived in Lemma 1.

Lemma 1. With the on–off scheme, the DEP for a given number of cooperative users, K, is approximated as

$$
\begin{array}{r l} \zeta (\gamma) \approx 1 - \exp \biggl (- \frac {2 \Delta (\hat {\gamma} - \Xi_ {K}) - \Sigma_ {K}}{2 \Delta^ {2}} \biggr) \\ & \times Q \biggl (- \frac {\Delta (\hat {\gamma} - \Xi_ {K}) - \Sigma_ {K}}{\sqrt {\Sigma_ {K}} \Delta} \biggr), \end{array}\tag{18}
$$

$$
Q (\cdot)
$$

$$
\hat {\gamma} \triangleq
$$

$$
\gamma - \sigma_ {\mathrm{w}} ^ {2}, \Xi_ {K} \triangleq P _ {\max} \sum_ {m = 1} ^ {M} \pi_ {m} ^ {(K)} \lambda_ {m, \mathrm{w}}, \Delta \triangleq P _ {\mathrm{a}} \lambda_ {\mathrm{a,w}},
$$

$$
\Sigma_ {K} \triangleq P _ {\mathrm{max}} ^ {2} \Bigg [ \sum_ {m = 1} ^ {M} \pi_ {m} ^ {(K)} \lambda_ {m, \mathrm{w}} ^ {2} + \sum_ {m = 1} ^ {M} \pi_ {m} ^ {(K)} \big (1 - \pi_ {m} ^ {(K)} \big) \lambda_ {m, \mathrm{w}} ^ {2}
$$

$$
\left. + 2 \sum_ {1 \leq m <   n \leq M} \left(\pi_ {m, n} ^ {(K)} - \pi_ {m} ^ {(K)} \pi_ {n} ^ {(K)}\right) \lambda_ {m, \mathrm{w}} \lambda_ {n, \mathrm{w}} \right].\tag{19}
$$

Here, $\pi _ { m } ^ { ( K ) }$ and $\pi _ { m , n } ^ { ( K ) }$ are the first- and second-order inclusion probabilities, respectively, defined in (54) and (55).

Proof. See Appendix B

The analytical form of the DEP in (18) enables one to obtain several design parameters. In particular, the detection threshold $\gamma ^ { * }$ , which minimizes the DEP, is derived in closed form and presented in Lemma 2.

Lemma 2. The detection threshold that minimizes $\zeta ( \gamma )$ is given by

$$
\gamma^ {*} = \Xi_ {K} + \sigma_ {\mathrm{w}} ^ {2}.\tag{20}
$$

Proof. Starting from (18), the DEP is approximated as

$$
\zeta (\gamma) \approx 1 - c _ {q} \exp \left(\underbrace {- \frac {1}{2 \Sigma_ {K}} \left(\hat {\gamma} ^ {2} - 2 \Xi_ {K} \hat {\gamma} + \Xi_ {K} ^ {2}\right)} _ {(a)}\right),\tag{21}
$$

where the approximation follows from the exponential approximation of the Gaussian Q-function, i.e., Q(x) ≈ $\bar { c } _ { q } e ^ { - x ^ { 2 } / 2 }$ [30], [37, Eqs.(4)-(5)]. It is observed that (21) is an exponential function of a concave quadratic term in γˆ. Since the term (a) attains its maximum value at $\hat { \gamma } = \Xi _ { K }$ , the DEP is minimized at $\hat { \gamma } _ { K } ^ { * } = \Xi _ { K }$ . From $\hat { \gamma } = \gamma - \sigma _ { \mathrm { w } } ^ { 2 }$ , the detection threshold is obtained as (20). □

Using the detection threshold in (20), the minimum DEP is obtained as presented in Lemma 3.

Lemma 3. The minimum DEP at Willie is given by

$$
\zeta_ {\min} = 1 - \left(\sqrt {\pi} \left(\sqrt {\frac {\Sigma_ {K}}{2 \Delta^ {2}}} + \sqrt {\frac {\Sigma_ {K}}{2 \Delta^ {2}} + \frac {4}{\pi}}\right)\right) ^ {- 1}.\tag{22}
$$

Proof. By substituting the optimal detection threshold $\gamma ^ { * }$ in (20) into the DEP in (18), we obtain

$$
\begin{array}{l} \zeta_ {\min} = 1 - \exp \left(\frac {\Sigma_ {K}}{2 \Delta^ {2}}\right) Q \left(\frac {\sqrt {\Sigma_ {K}}}{\Delta}\right) \\ = 1 - \frac {1}{2} \exp \left(\frac {\Sigma_ {K}}{2 \Delta^ {2}}\right) \operatorname{erfc} \left(\frac {\sqrt {\Sigma_ {K}}}{\sqrt {2} \Delta}\right) \\ \stackrel {{\approx}} {{(a)}} 1 - \frac {1}{2} \exp \left(\frac {\Sigma_ {K}}{2 \Delta^ {2}}\right) \frac {2 \exp \left(- \frac {\Sigma_ {K}}{2 \Delta^ {2}}\right)}{\sqrt {\pi} \left(\sqrt {\frac {\Sigma_ {K}}{2 \Delta^ {2}}} + \sqrt {\frac {\Sigma_ {K}}{2 \Delta^ {2}} + \frac {4}{\pi}}\right)} \\ = 1 - \left(\sqrt {\pi} \left(\sqrt {\frac {\Sigma_ {K}}{2 \Delta^ {2}}} + \sqrt {\frac {\Sigma_ {K}}{2 \Delta^ {2}} + \frac {4}{\pi}}\right)\right) ^ {- 1}, \end{array} \tag {2}\tag{23}
$$

where erfc(·) indicates the complementary error function. The approximation in (a) follows from the fact that erfc(x) ≈ $2 \bar { / } \sqrt { \pi } \cdot \exp ( - x ^ { 2 } ) / ( x + \sqrt { x ^ { 2 } + 4 / \pi } )$ is highly accurate for $x \gtrsim 1 \ [ 3 8$ , Eq. (7.1.13)]. In our setting, the argument of the complementary error function is $\sqrt { \Sigma _ { K } } \bar { / } ( \sqrt { 2 } \Delta )$ , and since the aggregate interference uncertainty $\Sigma _ { K }$ from the cooperative users is typically much larger than that of Alice’s power $\Delta ^ { 2 } .$ 2 this approximation is well justified. □

Based on Lemma 3, the number of cooperative users should be chosen as the smallest integer that satisfies the covert constraint $\zeta _ { \mathrm { m i n } } \ge 1 - \epsilon$ . Since $\zeta _ { \mathrm { m i n } }$ is an increasing function of $\Sigma _ { K }$ , this condition can be equivalently expressed in terms of the required aggregate interference uncertainty. The resulting minimum number of cooperative users is characterized in Theorem 1.

Theorem 1. Under the DEP approximation in Lemma 1, the minimum number of cooperative users required to satisfy the covert constraint is given by

$$
K _ {\mathrm{min}} = \min \left\{K \in \{0, 1, \dots , M \}: \Sigma_ {K} \geq c _ {\epsilon} \Delta^ {2} \right\},\tag{24}
$$

where $\begin{array} { r } { c _ { \epsilon } \triangleq \frac { 1 / \epsilon ^ { 2 } - 8 + 1 6 \epsilon ^ { 2 } } { 2 \pi } } \end{array}$

Proof. By Lemma 3, the covert constraint $\zeta _ { \mathrm { m i n } } \ge 1 - \epsilon$ is equivalent to

$$
\left[ \sqrt {\pi} \left(\sqrt {\frac {\Sigma_ {K}}{2 \Delta^ {2}}} + \sqrt {\frac {\Sigma_ {K}}{2 \Delta^ {2}} + \frac {4}{\pi}}\right) \right] ^ {- 1} \leq \epsilon .\tag{25}
$$

Solving this inequality with respect to $\Sigma _ { K }$ yields $\Sigma _ { K } \geq c _ { \epsilon } \Delta ^ { 2 }$ Hence, the minimum number of cooperative users is the smallest integer K satisfying this condition, which gives (24).

To obtain a compact closed-form rule, we approximate the selected users as a uniformly chosen K subset without replacement, for which the finite population correction applies [39, Sec. 2.6], [40, Sec. 2.3]. Then,

$$
\pi_ {m} ^ {(K)} \approx \frac {K}{M}, \qquad \pi_ {m, n} ^ {(K)} \approx \frac {K (K - 1)}{M (M - 1)}.\tag{26}
$$

Substituting (26) into $\Sigma _ { K }$ gives

$$
\Sigma_ {K} ^ {\mathrm{uni}} = P _ {\mathrm{max}} ^ {2} \left[ K E + K \frac {M - K}{M - 1} V \right],\tag{27}
$$

where $\begin{array} { r } { E \triangleq \frac { 1 } { M } \sum _ { m = 1 } ^ { M } \lambda _ { m , \mathrm { w } } ^ { 2 } } \end{array}$ and

$$
V \triangleq \frac {1}{M} \sum_ {m = 1} ^ {M} \left(\lambda_ {m, \mathrm{w}} - \frac {1}{M} \sum_ {n = 1} ^ {M} \lambda_ {n, \mathrm{w}}\right) ^ {2}.
$$

Let $K _ { \operatorname* { m i n } } ^ { \mathrm { u n i } }$ be the minimum K satisfying $\Sigma _ { K } ^ { \mathrm { u n i } } \geq c _ { \epsilon } \Delta ^ { 2 }$ . This closed-form rule is conservative for a given topology whenever

$$
\Sigma_ {K _ {\mathrm{min}} ^ {\mathrm{uni}}} \geq \Sigma_ {K _ {\mathrm{min}} ^ {\mathrm{uni}}} ^ {\mathrm{uni}}.\tag{28}
$$

Indeed, under (28),

$$
\Sigma_ {K _ {\mathrm{min}} ^ {\mathrm{uni}}} \geq \Sigma_ {K _ {\mathrm{min}} ^ {\mathrm{uni}}} ^ {\mathrm{uni}} \geq c _ {\epsilon} \Delta^ {2},\tag{29}
$$

and thus $K _ { \operatorname* { m i n } } ^ { \mathrm { u n i } }$ also satisfies the general covert constraint in Theorem 1. Hence, the following corollary should be understood as a sufficient closed-form design rule under the uniform finite-population approximation.

Corollary 1. Under the uniform finite-population approximation in (27), the minimum number of cooperative users can be approximated in closed form as

$$
K _ {\min} ^ {\mathrm{uni}} = \left\lceil \frac {M (E + V)}{2 V} \left(1 - \sqrt {1 - \frac {4 V}{C M (E + V) ^ {2}}}\right)\right\rceil ,\tag{30}
$$

where $C \triangleq P _ { \mathrm { m a x } } ^ { 2 } / ( P _ { \mathrm { a } } ^ { 2 } \lambda _ { \mathrm { a , w } } ^ { 2 } c _ { \epsilon } ) .$

Proof. From Theorem 1, the covert constraint is satisfied if $\Sigma _ { K } \geq c _ { \epsilon } \Delta ^ { 2 }$

By substituting the uniform finite-population approximation in (27) and using $\Delta = P _ { \mathrm { a } } \lambda _ { \mathrm { a , w } }$ together with the definition of C, this condition is rewritten as

$$
K \left(E + \frac {M - K}{M - 1} V\right) \geq \frac {1}{C}.\tag{31}
$$

Solving the corresponding quadratic inequality with respect to K and taking the smallest integer satisfying the inequality yields (30). □

The expression in Corollary 1 provides the same physical insight as the original scaling law. Since we assume $M \gg 1$ applying $\sqrt { 1 - x } \approx 1 - x / 2$ to (30) yields

$$
K _ {\mathrm{min}} ^ {\mathrm{uni}} \approx \left\lceil \frac {1}{C (E + V)} \right\rceil = \left\lceil \frac {c _ {\epsilon} P _ {\mathrm{a}} ^ {2} \lambda_ {\mathrm{a,w}} ^ {2}}{P _ {\mathrm{max}} ^ {2} (E + V)} \right\rceil .\tag{32}
$$

This scaling shows that the minimum number of cooperative users decreases with the Willie-side second-order spatial statistic $E + V ,$ where E captures the empirical second moment of $\lambda _ { m , \mathrm { w } }$ and V captures spatial heterogeneity. Hence, stronger spatial heterogeneity increases the aggregate cooperative-interference uncertainty observed by Willie, making Alice’s additional energy easier to hide. Conversely, the minimum number of cooperative users increases quadratically with $P _ { \mathrm { a } } \lambda _ { \mathrm { a , w } }$ . In addition, since $c _ { \epsilon } = \mathcal { O } ( \epsilon ^ { - 2 } )$ as $\epsilon  0$ , the minimum number of cooperative users also increases on the order of $\epsilon ^ { - 2 }$ as the covert constraint becomes tighter. These trends are numerically confirmed in Section VI.

When $\lambda _ { m , \mathrm { w } } \approx \bar { \lambda } _ { \mathrm { w } }$ for all $m ,$ the spatial heterogeneity vanishes, and the selected cooperative set no longer introduces additional uncertainty through large-scale heterogeneous fading from non-covert user-to-Willie. Therefore, $\Sigma _ { K } \mathrm { \tilde { \pi } } \approx P _ { \mathrm { m a x } } ^ { 2 } K { \bar { \lambda } _ { \mathrm { w } } } ^ { 2 } .$ which gives the following homogeneous special case from Theorem 1.

Corollary 2. Under homogeneous user deployment, the minimum number of cooperative users is approximated as

$$
K _ {\mathrm{min}} ^ {\mathrm{hom}} \approx \left\lceil \frac {P _ {\mathrm{a}} ^ {2} c _ {\epsilon}}{P _ {\mathrm{max}} ^ {2}} \left(\frac {\lambda_ {\mathrm{a,w}}}{\bar {\lambda} _ {\mathrm{w}}}\right) ^ {2} \right\rceil .\tag{33}
$$

Proof. Under homogeneous deployment, $\lambda _ { m , \mathrm { w } } \approx \bar { \lambda } _ { \mathrm { w } }$ for all $m ,$ and hence $\Sigma _ { K } \mathrm { ~ \bar { ~ } \approx ~ } P _ { \operatorname* { m a x } } ^ { 2 } \dot { K } \bar { \lambda } _ { \mathrm { w } } ^ { 2 }$ . Substituting this expression into the condition $\widetilde \Sigma _ { K } ~ \ge ~ \stackrel {  } { c _ { \epsilon } } \Delta ^ { 2 }$ in Theorem 1, with $\Delta = P _ { \mathrm { a } } \lambda _ { \mathrm { a , w } } .$ , gives

$$
K \geq \frac {c _ {\epsilon} P _ {\mathrm{a}} ^ {2} \lambda_ {\mathrm{a,w}} ^ {2}}{P _ {\mathrm{max}} ^ {2} \bar {\lambda} _ {\mathrm{w}} ^ {2}}.\tag{34}
$$

Applying the integer constraint yields (33).

Equation (33) shows that, in the homogeneous case, the minimum number of cooperative users is determined by the relative Willie-side channel between Alice and the cooperative users. In addition, when $\lambda _ { a , w } ~ = ~ \bar { \lambda } _ { w } .$ , this result directly reduces to the result shown in previous works [30], [32], demonstrating that the proposed analysis encompasses these prior studies as special cases and therefore provides a more general characterization of the system.

By utilizing the minimum number of cooperative users obtained from Theorem 1, or its closed-form approximation in Corollary 1, the corresponding activation threshold of the on–off scheme in Proposition 1 can be readily determined, as presented in Theorem 2.

Theorem 2. The activation threshold is determined by

$$
\tau = \frac {| h _ {m _ {K _ {\mathrm{min}}} , \mathrm{b}} | ^ {2}}{\lambda_ {m _ {K _ {\mathrm{min}}} , \mathrm{w}}}.\tag{35}
$$

Proof. The on–off scheme activates user m if $| h _ { m , \mathrm { b } } | ^ { 2 } / \lambda _ { m , \mathrm { w } } \leq$ $\tau .$ Therefore, setting τ to the activation metric of user $m _ { K _ { \mathrm { m i n } } }$ makes the $K _ { \mathrm { m i n } } – \mathrm { t h \Omega }$ smallest metric the activation boundary, ensuring that exactly $K _ { \mathrm { m i n } }$ cooperative users participate.

## V. OPTIMIZATION OF SYSTEM PARAMETERS

In this section, we first reformulate the optimization problem in (15), which involves two optimization variables, into a simpler form with only a single optimization variable based on Theorems 1 and 2. Then, we propose a structure-aware piecewise search algorithm that efficiently solves the reformulated optimization problem.

## A. Reformulation of the Optimization Problem

As discussed in Section III, adopting the on–off scheme in Proposition 1 allows the original problem in (11) to be reformulated as (15), reducing the number of optimization variables from $M + 1$ to two, $P _ { \mathrm { a } }$ and $\tau .$ For a given $P _ { \mathrm { a } } ,$ Theorem 1 characterizes the minimum number of cooperative users through the condition on $\Sigma _ { K }$ , and Theorem 2 determines the corresponding activation threshold. Let $m _ { i }$ denote the index of the user with the i-th smallest activation metric $| h _ { m , \mathrm { b } } | ^ { 2 } / \lambda _ { m , \mathrm { w } }$ . Then, under the adopted large-M analytical formulation, the problem in (15) can be reduced to

$$
P _ {\mathrm{a}} ^ {*} = \underset {0 \leq P _ {\mathrm{a}} \leq P _ {\mathrm{max}}} {\operatorname{argmax}} R (P _ {\mathrm{a}}, K _ {\min} (P _ {\mathrm{a}})),\tag{36}
$$

where

$$
R (P _ {\mathrm{a}}, K) = \log_ {2} \left(1 + \frac {P _ {\mathrm{a}} | h _ {\mathrm{a,b}} | ^ {2}}{\sum_ {i = 1} ^ {K} P _ {\max} | h _ {m _ {i} , \mathrm{b}} | ^ {2} + \sigma_ {\mathrm{b}} ^ {2}}\right).\tag{37}
$$

This optimization problem has only one optimization variable, i.e., $P _ { \mathrm { a } }$ , and is therefore much easier to solve than the original formulation of (11), which involves $M + 1$ optimization variables.

## B. Optimization of Transmit Power for Alice

Notably, as shown in Theorem 1 and Corollaries 1 and 2, $K _ { \mathrm { m i n } }$ is a function of $P _ { \mathrm { a } }$ . In particular, the minimum number of cooperative users increases with $P _ { \mathrm { a } } ,$ , because a larger $P _ { \mathrm { a } }$ produces a larger Alice-induced detection shift at Willie and therefore requires stronger cooperative-interference uncertainty to satisfy the covert constraint. Hence, the solution of (36) is not simply the maximum allowable value $P _ { \mathrm { m a x } }$ . In this work, we determine $P _ { \mathrm { a } } ^ { * }$ through a piecewise search for the optimization problem in (36).

Meanwhile, it is noteworthy that $K _ { \mathrm { m i n } } ( P _ { \mathrm { a } } )$ is an integervalued function. As a result, $K _ { \mathrm { m i n } } ( P _ { \mathrm { a } } )$ remains unchanged over certain ranges of $P _ { \mathrm { a } }$ . Moreover, for a fixed cooperation size K, the set of selected cooperative users and the resulting aggregate interference at Bob in the denominator of (37) do not vary with $P _ { \mathrm { a } } .$ . Hence, $R ( P _ { \mathrm { a } } , K )$ in (37) is strictly increasing in $P _ { \mathrm { a } }$ within each interval where $K _ { \mathrm { m i n } } ( P _ { \mathrm { a } } ) = K$ , and the optimum within each interval is attained at the largest feasible transmit power, i.e., the boundary candidate of that interval. For a given cooperation size $K _ { \operatorname* { m i n } } = \bar { K }$ , the maximum value of $P _ { \mathrm { a } }$ that satisfies the covert constraint can be obtained from Theorem 1 as

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Piecewise Search
Input: $h_{\mathrm{a,b}}$, $\{h_{m,\mathrm{b}}\}_{m=1}^{M}$, $\{\lambda_{m,\mathrm{w}}\}_{m=1}^{M}$, $P_{\max}$, $\epsilon$, $\sigma_{\mathrm{b}}^{2}$
Output: $P_{\mathrm{a}}^{*}$, $K^{*}$, $\tau^{*}$
1: Sort users in ascending order of $|h_{m,\mathrm{b}}|^{2}/\lambda_{m,\mathrm{w}}$, and denote the ordered indices by $m_1, \ldots, m_M$.
2: Compute $c_{\epsilon}$ and $\{\Sigma_{\bar{K}}\}_{\bar{K}=0}^{M}$, and set $R_{\text{temp}} \leftarrow 0$.
3: for $\bar{K}=0$ to M do
4: Compute $P_{\bar{K}}$ from (38) and $R(P_{\bar{K}},\bar{K})$ in (37).
5: If $R(P_{\bar{K}},\bar{K}) &gt; R_{\text{temp}}$, update $R_{\text{temp}} \leftarrow R(P_{\bar{K}},\bar{K})$, $P_{\mathrm{a}}^{*} \leftarrow P_{\bar{K}}$, and $K^{*} \leftarrow \bar{K}$.
6: end for
7: Set $\tau^{*} \leftarrow 0$ if $K^{*}=0$; otherwise, $\tau^{*} \leftarrow |h_{m_{K^{*}},\mathrm{b}}|^{2}/\lambda_{m_{K^{*}},\mathrm{w}}$.
8: Return $P_{\mathrm{a}}^{*}$, $K^{*}$, $\tau^{*}$.
</div>

$$
P _ {\mathrm{a}} (\bar {K}) = \frac {\sqrt {\Sigma_ {\bar {K}}}}{\sqrt {c _ {\epsilon}} \lambda_ {\mathrm{a,w}}}.\tag{38}
$$

Then, for a given $K _ { \operatorname* { m i n } } = \bar { K }$ , the candidate transmit power is defined as $P _ { \bar { K } } =$ min $\left( P _ { \mathrm { m a x } } , P _ { \mathrm { a } } ( \bar { K } ) \right)$ for $\bar { K } \in \{ 0 , \ldots , M \}$ Thus, when performing a one-dimensional search for the solution of (36), it is sufficient to evaluate the candidate boundary points $\{ P _ { \bar { K } } \} _ { \bar { K } = 0 } ^ { M } .$ This piecewise characterization eliminates the need to explore redundant regions of the search space, making the resulting search more efficient and structureaware than an exhaustive one-dimensional search. The overall piecewise search is summarized in Algorithm 1.

The computational complexity of Algorithm 1 can be explained directly from its steps. First, computing the activation metric $| h _ { m , \mathrm { b } } | ^ { 2 } / \lambda _ { m , \mathrm { w } }$ for all M users requires $\mathcal { O } ( M )$ operations, and sorting the users in ascending order of this metric requires O(M log M) operations. Then, the main loop evaluates one candidate transmit power $P _ { \bar { K } }$ and one corresponding rate $R ( P _ { \mathrm { a } } , \bar { K } )$ for each $\bar { \cal K } { \bf \Xi } = { \bf \Xi } _ { 0 , \dots , M }$ which requires O(M) candidate evaluations. Hence, the overall complexity of the piecewise search is $\mathcal { O } ( M ) + \mathcal { O } ( M$ log $M ) + \mathcal { O } ( M ) =$ O(M log M). In contrast, a grid-based one-dimensional search over $P _ { \mathrm { a } }$ with $N _ { p }$ grid points requires $\mathcal { O } ( N _ { p } M )$ operations, because the corresponding number of cooperative users and achievable rate must be evaluated for each grid point. Moreover, its solution depends on the power-grid resolution and may miss the analytical boundary candidate $P _ { \bar { K } }$ . The proposed piecewise search instead evaluates all analytically relevant candidates $P _ { \bar { K } }$ , thereby reducing the computational burden and avoiding power-discretization error. Table I quantifies this finite-resolution effect. The grid-based search selects slightly different values of $P _ { \mathrm { a } } ^ { \star }$ and $K ^ { \star }$ , which leads to a small rate loss, whereas Algorithm 1 directly evaluates the boundary candidates $P _ { \bar { K } }$ for all $\bar { K } = 0 , \ldots , \bar { M }$

When imperfect user-to-Bob channel estimation is considered, the same piecewise structure can be applied by replacing $h _ { m , \mathrm { b } }$ in the activation metric with its estimate $\hat { h } _ { m , \mathrm { b } }$ . Under the adopted channel estimation error model, $\hat { h } _ { m , \mathrm { b } }$ has the same statistical distribution as $h _ { m , \mathrm { b } }$ , and hence Willie-side aggregate interference statistics remain unchanged for the same $( P _ { \mathrm { a } } , K )$ Therefore, the channel estimation error mainly affects the set of cooperative users $\hat { S } \neq S$ and the resulting achievable rate at Bob, while the Willie-side DEP retains the same performance.

OPTIMIZATION COMPARISON BETWEEN ALGORITHM 1 AND THE GRID-BASED SEARCH WITH $N _ { P } = 1 0 ^ { 4 }$ . THE REPORTED VALUES ARE AVERAGED OVER INDEPENDENT FADING REALIZATIONS, AND THE RATE GAIN IS DEFINED AS $\left( R ^ { \star } - R _ { \mathrm { G r i d } } ^ { \star } \right) / R _ { \mathrm { G r i d } } ^ { \star } .$

<table><tr><td>M</td><td> $P_{\text{a}}^{\star}/P_{\text{max}}$ </td><td> $P_{\text{a,Grid}}^{\star}/P_{\text{max}}$ </td><td> $K^{\star}$ </td><td> $K_{\text{Grid}}^{\star}$ </td><td>Rate gain</td></tr><tr><td>500</td><td>0.336</td><td>0.319</td><td>73.67</td><td>74.53</td><td>5.70%</td></tr><tr><td>1000</td><td>0.407</td><td>0.386</td><td>103.29</td><td>104.15</td><td>5.94%</td></tr><tr><td>2000</td><td>0.486</td><td>0.458</td><td>144.35</td><td>145.07</td><td>6.22%</td></tr></table>

## VI. NUMERICAL RESULTS

In this section, we numerically validate the theoretical analyses and examine the interactions among key system parameters in the proposed covert communication network with spatially distributed users. To reflect more general wireless deployments, the numerical results are obtained under randomized spatial configurations rather than a fixed adverse topology. For performance evaluations, we consider the largescale fading channel model specified in the 3GPP TR 25.996 Urban Macrocell guideline [41]. The path loss (PL) at a distance d (in meters) is modeled as

$$
\mathrm{PL} (\mathrm{dB}) = 3 4. 5 + 3 5 \log_ {1 0} (d),\tag{39}
$$

which corresponds to the large-scale fading coefficient $\lambda _ { x , y } =$ $\beta _ { 0 } d _ { x , y } ^ { - \alpha }$ . Here, the path-loss exponent is set to $\alpha \ = \ 3 . 5$ and the reference channel gain at $d \_ =$ 1m is given by $\beta _ { 0 } ~ = ~ 1 0 ^ { - 3 4 . 5 / 1 0 }$ . The maximum transmit power of each user is set to $P _ { \mathrm { { m a x } } } ~ = ~ 2 0 0 \mathrm { { m W } ( 2 3 d B m ) }$ , and the noise variances at Bob and Willie are assumed to be identical, i.e., $\sigma _ { \mathrm { b } } ^ { 2 } = \sigma _ { \mathrm { w } } ^ { 2 } = - 1 0 2$ dBm. The spatial topology of the network is constructed over a 1000 m × 1000 m square region. Willie is placed at the center of the area, (500, 500), while Bob is located at (100, 100). Alice is located at (832.3, 832.3), which gives $d _ { \mathrm { a , w } } \approx 4 7 0 \mathrm { m }$ and $d _ { \mathrm { a , b } } \approx 1 0 3 5 . 7$ m. This placement maintains a relatively unfavorable Alice-to-Bob link compared with the Alice-to-Willie link. The non-covert users are randomly distributed over the simulation area. This randomized topology allows us to examine the proposed scheme under spatially heterogeneous user deployments without restricting the evaluation to a specific geometry.

In Fig. 2, we present the DEP curves obtained from numerical simulations under the general randomized topology. The line curves represent the DEP $\zeta ( \gamma )$ as a function of Willie’s detection threshold $\gamma ,$ while the markers correspond to the theoretical results in Lemmas 2 and 3. Specifically, the xcoordinates of the markers represent the optimal detection threshold, $\gamma ^ { \star }$ , derived in Lemma 2, and the y-coordinates represent the minimum DEP, $\zeta _ { \mathrm { m i n } } .$ , obtained from Lemma 3. In Fig. 2(a), we consider different numbers of non-covert users, i.e., $M = 4 0 0 .$ , 700, and 1000, while fixing $K = 1 0 0$ and $\mathrm { \mathit { P } _ { a } } = 1 5 0 \mathrm { m W }$ . In Fig. 2(b), we consider different transmit powers of Alice, i.e., $P _ { \mathrm { a } } ~ = ~ 1 0 0$ , 150, and 200 mW, while fixing $M = 7 0 0$ and $K = 1 0 0$ . As observed in Fig. 2, the theoretical results for $\gamma ^ { \star }$ and $\zeta _ { \mathrm { m i n } }$ closely match the minima of the corresponding DEP curves for all considered system parameters. This close agreement validates Lemmas 1–3.

![](images/c74dab5b876cbf3315ac3f7f0124bd62b1bfd70274a7f1b6dc1b2017f5e64b3f.jpg)  
Fig. 2. DEP $\zeta ( \gamma )$ as a function of the detection threshold γ under the general randomized topology. In (a), $K = 1 0 0$ and $\mathrm { \mathit { P a } } = 1 5 0 \mathrm { m W }$ are fixed, while M varies. In (b), $\ddot { M } = 7 0 0$ and $K = 1 0 0$ are fixed, while $P _ { \mathrm { a } }$ varies. The solid, dashed, and dash-dot lines denote the numerical DEP, and the markers indicate the analytical results of $\gamma ^ { \star }$ and $\zeta _ { \mathrm { m i n } }$ obtained from Lemmas 2 and 3.

It is also observed in Fig. 2(a) that increasing the number of non-covert users M slightly increases the minimum DEP under the fixed values of K and $P _ { \mathrm { a } } .$ This behavior can be explained by the order-statistics-induced cooperative user set. When M increases while K is fixed, Bob selects the K cooperative users from a larger candidate pool according to the activation metric $r _ { m }$ . Hence, the selected cooperative users are more likely to provide effective Willie-side interference uncertainty relative to their Bob-side interference cost. As a result, the variance of the aggregate cooperative interference observed at Willie increases relative to the Alice-induced shift $\Delta = P _ { \mathrm { a } } \lambda _ { \mathrm { a , w } }$ . Since the minimum DEP is governed by the ratio between the aggregate interference uncertainty and the Aliceinduced shift, the distributions of test statistics under $\mathcal { H } _ { \mathrm { 0 } }$ and $\mathcal { H } _ { 1 }$ become more overlapped, which increases Willie’s DEP. Meanwhile, Fig. 2(b) shows that increasing Alice’s transmit power from $\mathrm { \mathit { P } _ { a } } = 1 0 0 \mathrm { m W }$ to 200 mW reduces the DEP. This occurs because a higher $P _ { \mathrm { a } }$ increases the Alice-induced received-energy shift at Willie, making the two hypotheses more distinguishable and thereby improving Willie’s detection capability. Therefore, a larger Alice transmit power requires stronger cooperative interference uncertainty to maintain the same level of covertness.

In Fig. 3, we further examine Willie’s detection performance and validate the theoretical results presented in Lemmas 1, 2, $^ { 3 , }$ and Theorem 1. In particular, Figs. 3(a) and (b) evaluate the finite-N behavior of Willie’s energy detector, while Fig. 3(c) validates the minimum DEP, $\zeta _ { \mathrm { m i n } }$ , and the minimum number of cooperative users, $K _ { \mathrm { m i n } } ,$ under the proposed on–off scheme in Proposition 1. In Fig. 3(a), we plot the DEP, $\zeta _ { N } ( \gamma )$ , as a function of the detection threshold, γ, for different sample lengths, i.e., N = 10, 30, and 100. The large-N curve and the analytical marker are also included as benchmarks. As shown in the figure, the finite-N DEP curves approach the large-N benchmark as N increases. This is because, for finite N, Willie’s received-energy statistic still contains finite-sample fluctuation, whereas in the large-N limit, this fluctuation vanishes and the test statistic converges to the instantaneous aggregate received power. Therefore, the large-N analysis provides a favorable benchmark for Willie’s detection capability. Fig. 3(b) further confirms this observation by showing that the finite-N minimum DEP, $\zeta _ { N , \mathrm { m i n } }$ , gradually converges to the large-N result as N increases.

![](images/89e05cd248bc5a084e809d59022ca5e4a951b1d287b0bedf35396e23aef78ce5.jpg)  
Fig. 3. Finite-N DEP behavior and minimum DEP versus the number of cooperative users. In (a) and (b), $M = 7 0 0 , K = 5 0$ , and $\mathrm { \mathit { P } a } = 2 0 0 \mathrm { m W }$ are fixed. In $\mathrm { ( c ) , \ \zeta \zeta _ { m i n } }$ is plotted as a function of K for $\left( M , P _ { \mathrm { a } } \right) \ =$ (300, 80 mW), (500, 140 mW), and (700, 200 mW). The dotted horizontal line represents the covert constraint $1 - \epsilon = 0 . 9 7 .$

In Fig. 3(c), we plot the minimum DEP, $\zeta _ { \mathrm { m i n } } ,$ as a function of the number of cooperative users, K, under the general randomized topology. The numerical results are determined by minimizing the DEP over Willie’s detection threshold, $\gamma ,$ for each value of K. The analytical curves correspond to the minimum DEP derived in Lemma 3. As observed in Fig. 3(c), the analytical results closely match the numerical results for all considered parameter settings. This agreement confirms that Lemma 3 accurately characterizes the minimum DEP and that Theorem 1 serves as a reliable and computationally efficient guideline to determine the necessary number of cooperative users to meet a specified covert constraint. Furthermore, the red and black markers in Fig. 3(c) indicate $K _ { \mathrm { m i n } }$ obtained from Theorem 1 and $K _ { \operatorname* { m i n } } ^ { \mathrm { u n i } }$ obtained from Corollary 1, respectively. The comparison between these markers shows that the minimum number of cooperative users depends not only on the total number of available users and Alice’s transmit power, but also on how the cooperative users are selected. In particular, Theorem 1 accounts for the order-statisticsinduced distribution of the set of cooperative users, whereas the uniform approximation neglects this selection bias. This explains the gap between $K _ { \mathrm { m i n } }$ and $K _ { \operatorname* { m i n } } ^ { \mathrm { u n i } }$ . It is also observed in Fig. 3(c) that $\zeta _ { \mathrm { m i n } }$ increases with K and gradually enters a stable region. As K increases, $\Sigma _ { K }$ increases, and hence Alice’s energy shift becomes more difficult to distinguish from the cooperative interference fluctuation. Accordingly, Willie’s DEP increases. However, when K is sufficiently large, i.e., $\Sigma _ { K } \gg \Delta ^ { 2 }$ , the remaining gap satisfies

$$
1 - \zeta_ {\mathrm{min}} \approx \frac {\Delta}{\sqrt {2 \pi \Sigma_ {K}}}.\tag{40}
$$

Therefore, even though increasing K enlarges $\Sigma _ { K }$ , the $\mathrm { r e \mathrm { - } }$ maining gap $1 - \zeta _ { \mathrm { m i n } }$ decreases only with the inverse square root of $\Sigma _ { K }$ . This explains why $\zeta _ { \mathrm { m i n } }$ first increases rapidly and then becomes nearly stable. Thus, after the covert constraint is satisfied, activating additional cooperative users only slightly increases $\zeta _ { \mathrm { m i n } } .$ , while it continuously increases the interference imposed on Bob.

![](images/a6292c090ebbbb1f70d34098e9f850334f93acfac1e2ba93167a71bd20690295.jpg)  
Fig. 4. Impact of the covert constraint and spatial parameters on the minimum number of cooperative users, $K _ { \mathrm { m i n } } . \mathrm { I n ( a ) } , \dot { K } _ { \mathrm { m i n } }$ is plotted versus the covert constraint $1 - \epsilon$ for $( M , P _ { \mathrm { a } } ) = ( 3 0 0 , 8 0 \mathrm { m W } )$ and (500, 140 mW). In (b) and $( \mathbf { c } ) , K _ { \operatorname* { m i n } }$ is plotted versus the standard deviation σ<sub>d</sub> and the mean µ<sub>d</sub> of the user-to-Willie distances, respectively, for $M = 5 0 \mathrm { { \bar { 0 } } , \ : P _ { a } = 1 4 0 \mathrm { { m } \mathrm { { \bar { W } } } } }$ and $1 - \epsilon = 0 . 9 7$

In Fig. 4(a), we plot $K _ { \mathrm { m i n } }$ as a function of the covert constraint, $1 \ - \ \epsilon ,$ under the general randomized topology. The line curves represent the numerical values of $K _ { \mathrm { m i n } }$ while the markers indicate the analytical results derived from Theorem 1, Corollary 1, and Corollary 2. Fig. 4(a) illustrates that the results of Theorem 1 closely match the numerical results for both considered network sizes, i.e., $M \ = \ 3 0 0$ and $M = 5 0 0$ . This confirms that the proposed analysis of $K _ { \mathrm { m i n } }$ remains accurate not only in a large-user regime, but also for smaller and moderate user populations. In addition, as the covert constraint becomes more stringent, i.e., as 1 − ϵ increases, $K _ { \mathrm { m i n } }$ increases. This is because a stricter covert constraint requires larger aggregate cooperative interference uncertainty at Willie. The results of Corollary 1 follow the same trend as those of Theorem 1, which confirms that the uniform finite-population approximation provides a useful simplified insight. However, the results of Corollary 2 are noticeably larger than those of Theorem 1. This implies that the homogeneous approximation can overestimate the minimum number of cooperative users when the actual user deployment is spatially heterogeneous.

Figs. 4(b) and (c) further illustrate how the spatial distribution of non-covert users affects $K _ { \mathrm { m i n } }$ . In Fig. 4(b), the standard deviation of the user-to-Willie distances, $\sigma _ { d } ,$ is varied. It is observed that as $\sigma _ { d }$ increases, the minimum number of cooperative users decreases. This is because a larger distance dispersion creates a more heterogeneous set of user-to-Willie links, which increases the chance that selected cooperative users provide stronger interference uncertainty at Willie. As a result, fewer cooperative users are required to satisfy the same covert constraint. In Fig. 4(c), the mean user-to-Willie distance, $\mu _ { d } ,$ is varied. It is observed that as $\mu _ { d }$ increases, $K _ { \mathrm { m i n } }$ also increases. This is because the users become farther from Willie on average, and the aggregate interference power observed at Willie becomes weaker. Hence, more cooperative users are required to generate sufficient interference uncertainty and satisfy the covert constraint. Combining the results from Figs. 4 (a) and (b) yields a comprehensive design guideline: to maximize covert communication performance, non-covert users should be deployed as close to Willie as possible while maintaining a high degree of spatial dispersion.

![](images/6e59a6032ae2afd430838b0dd1b8a90e1841e1bbe83e456ccd42173815e7579d.jpg)  
Fig. 5. Optimized system performance and impact of imperfect user-to-Bob channel estimation. In (a)–(c), $P _ { \mathrm { a } } ^ { \star } / P _ { \mathrm { m a x } } , \ K ^ { \star }$ , and $R ^ { \star }$ are plotted versus the covert constraint 1 − ϵ for $\bar { M } = 3 0 0 .$ . In (d), Willie’s minimum DEP is plotted versus the channel estimation error level $\rho _ { e }$ for $M = 7 0 0 , K = 1 0 0 .$ and $\mathrm { \mathit { P } a } = 1 5 0 \mathrm { m W }$ . In (e), the optimized achievable rate is plotted versus $\rho _ { e }$ for $M = 7 0 0$

In Fig. 5, we compare the covert communication performance of the proposed design with those of the uniformapproximation design and the Bob-only baseline. In the proposed design, cooperative users are selected based on Proposition 1. In contrast, the Bob-only baseline selects cooperative users solely according to the instantaneous channel gains between the users and Bob [30]–[32]. Importantly, both the proposed method and the baseline method are evaluated under the same heterogeneous network realization. The baseline differs from the proposed method only in the cooperative user selection rule. It selects cooperative users based on the instantaneous user-to-Bob channel gains only, without using the user-to-Willie large-scale fading coefficients in the selection metric. After the baseline user set is determined, its covertness and achievable rate are evaluated using the actual heterogeneous user-to-Willie large-scale fading coefficients. To validate the effectiveness of the proposed design, we compare the optimized results, i.e., $P _ { \mathrm { a } } ^ { \star } , \ K ^ { \star } ,$ , and $R ^ { \star }$ , with respect to the stringency of the covert constraint, $1 - \epsilon .$

In Figs. 5(a) and (b), we present the ratio of the optimized transmit power for the covert message to the maximum transmit power, $P _ { \mathrm { a } } ^ { \star } / P _ { \mathrm { m a x } } ,$ and the optimal number of cooperative users, $K ^ { \star }$ , respectively. It is observed that all schemes adjust $P _ { \mathrm { a } } ^ { \star }$ and $K ^ { \star }$ according to the stringency of the covert constraint. However, the proposed design requires fewer cooperative users than the Bob-only baseline for a given covert constraint. The proposed design exploits this spatial heterogeneity by selectively utilizing users that can effectively increase Willie’s uncertainty without excessively increasing the interference at Bob. In contrast, the Bob-only baseline does not exploit the user-to-Willie large-scale fading coefficients in the selection metric, and therefore cannot fully utilize the spatially heterogeneous interference structure. In addition, Fig. 5(c) demonstrates that the proposed design improves the optimized covert rate compared with the Bob-only baseline. In particular, as the covert constraint becomes more stringent, the performance gap between the proposed design and the baseline becomes more pronounced. This indicates that incorporating the distinct spatial locations of users into the cooperative user selection and optimization process substantially enhances covert performance. The performance of Corollary 1 is close to that of Theorem 1, which confirms that the uniform approximation provides a useful simplified design.

Fig. 5(d) shows the impact of imperfect user-to-Bob channel estimation on Willie’s minimum DEP at $M ~ = ~ 7 0 0$ $K ~ = ~ 1 0 0$ , and $\mathrm { \mathit { P } _ { a } } ~ = ~ 1 5 0 \mathrm { m W }$ Under the adopted error model, $\hat { h } _ { m , \mathrm { b } } ~ = ~ \sqrt { 1 - \rho _ { e } } h _ { m , \mathrm { b } } + \sqrt { \rho _ { e } } u _ { m , \mathrm { b } }$ , where $u _ { m , \mathrm { b } }$ has the same distribution as $h _ { m , \mathrm { b } }$ . Thus, changing $\rho _ { e }$ changes how accurately $\hat { h } _ { m , \mathrm { b } }$ represents the true channel $h _ { m , \mathrm { b } }$ , but does not change the statistical distribution of $\hat { h } _ { m , \mathrm { b } }$ itself. Therefore, for the same $( P _ { \mathrm { a } } , K )$ , the Willie-side aggregate interference statistics remain unchanged, and the minimum DEP overlaps with the perfect estimation reference. Furthermore, Fig. 5(e) shows the impact of imperfect user-to-Bob channel estimation on the optimized achievable rate. Bob selects cooperative users and determines $K ^ { \star }$ , the activation threshold, and $P _ { \mathrm { a } } ^ { \star }$ using the estimated channels $\hat { h } _ { m , \mathrm { b } }$ . When the estimation error increases, users selected as weak interferers to Bob based on $\hat { h } _ { m , \mathrm { b } }$ can have large true channel gains $h _ { m , \mathrm { b } } .$ Therefore, the actual aggregate interference at Bob increases, thereby reducing $R ^ { \star }$

## VII. CONCLUSION

This paper investigated covert communication in which a single covert user is assisted by multiple spatially distributed non-covert users against a geometry-aware Willie. Under the adopted large-M analytical formulation, we established an on–off cooperative-user activation structure and characterized Willie’s DEP, the minimum number of cooperative users, and the corresponding activation threshold. We further developed a low-complexity piecewise search algorithm for the analytically reformulated power-control problem. The results showed that greater Willie-side spatial dispersion can reduce the minimum number of cooperative users, whereas a larger average user-to-Willie distance increases it, and that homogeneous or averaged-geometry analyses may mischaracterize the cooperation requirement. The numerical results further confirmed that the finite-sample DEP converges to the large-sample benchmark with an increasing number of observations, and that the impact of imperfect user-to-Bob channel estimation appears primarily as a rate loss induced by cooperative user activation errors, rather than as a loss of covertness. Future work will extend the proposed framework to mobile networks, multiple-Willie scenarios, and integrated sensing and communication systems, where sensing resources and spatial information can be jointly exploited to enhance covertness.

## APPENDIX A PROOF OF PROPOSITION 1

For a fixed $P _ { a }$ , (11) becomes

$$
\bar {P} ^ {*} = \underset {\bar {P}} {\operatorname{argmax}} \frac {P _ {\mathrm{a}} | h _ {\mathrm{a,b}} | ^ {2}}{\sum_ {m = 1} ^ {M} P _ {m} | h _ {m , \mathrm{b}} | ^ {2} + \sigma_ {\mathrm{b}} ^ {2}}\tag{41a}
$$

s.t. (11b) and (11d).

To characterize the covert constraint, we approximate the sum of Gamma random variables by a Gamma distribution with matched first and second moments [42]–[44]. Thus, in large $M , T _ { \mathrm { w } }$ can be reformulated to

$$
T _ {\mathrm{w}} - \sigma_ {\mathrm{w}} ^ {2} \sim \left\{ \begin{array}{l l} \Gamma \Big (\frac {\psi^ {2}}{\Psi}, \frac {\Psi}{\psi} \Big), & \mathcal {H} _ {0}, \\ \Gamma \Big (\frac {(\psi + \lambda_ {\mathrm{a,w}} P _ {\mathrm{a}}) ^ {2}}{\Psi + (\lambda_ {\mathrm{a,w}} P _ {\mathrm{a}}) ^ {2}}, \frac {\Psi + (\lambda_ {\mathrm{a,w}} P _ {\mathrm{a}}) ^ {2}}{\psi + \lambda_ {\mathrm{a,w}} P _ {\mathrm{a}}} \Big), & \mathcal {H} _ {1}, \end{array} \right.\tag{42}
$$

where $\begin{array} { r } { \psi = \sum _ { m = 1 } ^ { M } \lambda _ { m , \mathrm { w } } P _ { m } } \end{array}$ and $\begin{array} { r } { \Psi = \sum _ { m = 1 } ^ { M } \lambda _ { m , \mathrm { w } } ^ { 2 } P _ { m } ^ { 2 } } \end{array}$ . For sufficiently large M, this Gamma distribution is approximated as a normal distribution [36, Sec. 5.5], [45, Sec. 2.8], yielding

$$
T _ {\mathrm{w}} - \sigma_ {\mathrm{w}} ^ {2} \sim \left\{ \begin{array}{l l} \mathcal {N} (\psi , \Psi), & \mathcal {H} _ {0}, \\ \mathcal {N} \big (\psi + \lambda_ {a, w} P _ {\mathrm{a}}, \Psi + \lambda_ {\mathrm{a,w}} ^ {2} P _ {\mathrm{a}} ^ {2} \big), & \mathcal {H} _ {1}. \end{array} \right.\tag{43}
$$

Using (43), the DEP is given by

$$
\begin{array}{l} \zeta = \operatorname * {P r} (T _ {\mathrm{w}} > \gamma \mid \mathcal {H} _ {0}) + \operatorname * {P r} (T _ {\mathrm{w}} \leq \gamma \mid \mathcal {H} _ {1}) \\ = \underbrace {Q \left(\frac {\gamma - \psi}{\sqrt {\Psi}}\right)} _ {(a)} + \underbrace {Q \left(\frac {(\psi + \lambda_ {\mathrm{a,w}} P _ {\mathrm{a}}) - \gamma}{\sqrt {\Psi + \lambda_ {\mathrm{a,w}} ^ {2} P _ {\mathrm{a}} ^ {2}}}\right)} _ {(b)}, \end{array}\tag{44}
$$

where $Q ( \cdot )$ denotes the standard Gaussian Q-function. Setting $P _ { \mathrm { F A } } = \alpha$ , the detection threshold is obtained from term (a) as

$$
\gamma = \sqrt {\Psi} Q ^ {- 1} (\alpha) + \psi .\tag{45}
$$

Substituting (45) into term (b) yields $P _ { \mathrm { M D } }$ , and thus

$$
\zeta = \alpha + Q \left(\frac {\lambda_ {\mathrm{a,w}} P _ {\mathrm{a}} - \sqrt {\Psi}   Q ^ {- 1} (\alpha)}{\sqrt {\Psi + \lambda_ {\mathrm{a,w}} ^ {2} P _ {\mathrm{a}} ^ {2}}}\right).\tag{46}
$$

From $( 4 6 ) , \zeta ( \alpha , \Psi )$ is monotonically increasing in $\Psi$ for any fixed $\alpha .$ . Hence, the minimized DEP $\begin{array} { r } { \zeta _ { \operatorname* { m i n } } ( \Psi ) = \operatorname* { m i n } _ { \alpha } \zeta ( \alpha , \Psi ) } \end{array}$ is also monotonically increasing in Ψ. Suppose that for two values $\Psi \ < \ \hat { \Psi }$ , there exist optimal thresholds $\alpha ^ { * }$ and $\hat { \alpha }$ minimizing $\zeta ( \alpha , \Psi )$ and $\zeta ( \alpha , \hat { \Psi } )$ , respectively.

Then, by definition, $\zeta _ { \operatorname* { m i n } } ( \Psi ) = \zeta ( \alpha ^ { * } , \Psi ) \leq \zeta ( \hat { \alpha } , \Psi )$ , and because $\zeta$ increases with Ψ for any fixed $\alpha , ~ \zeta ( \hat { \alpha } , \Psi ) ~ <$ $\zeta ( \hat { \alpha } , \hat { \Psi } ) = \zeta _ { \operatorname* { m i n } } ( \hat { \Psi } )$ . Therefore, $\zeta _ { \mathrm { m i n } } ( \Psi )$ is strictly increasing with respect to Ψ. By applying Sedrakyan’s Lemma [46], we obtain

$$
\frac {\Psi}{M} = \frac {1}{M} \sum_ {m = 1} ^ {M} \left(\lambda_ {m, \mathrm{w}} P _ {m}\right) ^ {2} \geq \frac {1}{M ^ {2}} \left(\sum_ {m = 1} ^ {M} \lambda_ {m, \mathrm{w}} P _ {m}\right) ^ {2},\tag{47}
$$

where the inequality becomes tight as M grows large. Hence, for sufficiently large M, we have $\Psi \ \approx \ \psi ^ { 2 } / M$ , and $\zeta _ { \mathrm { m i n } }$ becomes a monotonically increasing function of $\psi ^ { 2 } / M$ . Therefore, the covert constraint becomes

$$
\psi = \sum_ {m = 1} ^ {M} \lambda_ {m, \mathrm{w}} P _ {m} \geq \delta ,\tag{48}
$$

where $\delta \triangleq \sqrt { M } \zeta _ { \operatorname* { m i n } } ^ { - 1 } ( 1 - \epsilon )$

The optimization problem in (41) can be reformulated as

$$
\bar {P} ^ {*} = \arg \min _ {\bar {P}} \sum_ {m = 1} ^ {M} P _ {m} | h _ {m, \mathrm{b}} | ^ {2} + \sigma_ {\mathrm{b}} ^ {2},\tag{49a}
$$

$$
\text { s.t. } \quad \sum_ {m = 1} ^ {M} \lambda_ {m, \mathrm{w}} P _ {m} \geq \delta \quad \text { and } \quad (1 1 \mathrm{d})\tag{49b}
$$

The KKT conditions with multipliers $\{ \phi _ { m } , \omega _ { m } , \nu \}$ are

• Stationarity: $| h _ { m , b } | ^ { 2 } - \nu ^ { * } \lambda _ { m , w } - \phi _ { m } ^ { * } + \omega _ { m } ^ { * } = 0 , \forall m .$

• Complementary slackness: $\phi _ { m } ^ { * } P _ { m } ^ { * } ~ = ~ 0 , ~ \omega _ { m } ^ { * } ( P _ { m } ^ { * } ~ -$ $P _ { \mathrm { m a x } } ) = 0$ , and $\begin{array} { r } { \nu ^ { * } \left( \delta - \sum _ { m = 1 } ^ { M } \lambda _ { m \mathrm { w } } P _ { m } ^ { * } \right) = 0 , } \end{array}$

• Feasibility: $\begin{array} { r } { 0 \leq P _ { m } ^ { * } \leq P _ { \operatorname* { m a x } } , \sum _ { m = 1 } ^ { M } \lambda _ { m , \mathrm { w } } P _ { m } ^ { * } \geq \delta } \end{array}$ , and $\phi _ { m } ^ { * } , \omega _ { m } ^ { * } , \nu ^ { * } \ge 0 .$

Solving these conditions for each m yields three feasible cases according to the comparison between $| h _ { m , \mathrm { b } } | ^ { 2 } / \lambda _ { m , \mathrm { w } }$ and $\nu ^ { * }$

Thus, the optimal transmit power for each non-covert user is expressed as

$$
P _ {m} ^ {*} = \left\{ \begin{array}{l l} P _ {\mathrm{max}}, & \frac {| h _ {m , \mathrm{b}} | ^ {2}}{\lambda_ {m , \mathrm{w}}} <   \tau , \\ 0, & \frac {| h _ {m , \mathrm{b}} | ^ {2}}{\lambda_ {m , \mathrm{w}}} > \tau , \\ \frac {\delta - \sum_ {m \in \mathcal {C}} P _ {\mathrm{max}}}{\lambda_ {m , \mathrm{w}}}, & \frac {| h _ {m , \mathrm{b}} | ^ {2}}{\lambda_ {m , \mathrm{w}}} = \tau , \end{array} \right.\tag{50}
$$

where C denotes the set of selected cooperative users, i.e., $\mathcal { C } = \{ m ^ { \prime } : | h _ { m ^ { \prime } , \mathrm { b } } | ^ { 2 } / \lambda _ { m ^ { \prime } , \mathrm { w } } < \tau \}$ and $\tau = \nu ^ { * }$ . Note that if $U _ { m }$ is a non-covert user satisfying $| h _ { m , \mathrm { b } } | ^ { 2 } / \lambda _ { m , \mathrm { w } } = \tau$ , the user cannot determine the transmit power from (50) since $U _ { m }$ cannot have the knowledge of the set C, i.e., the channels between the other users and Bob.

Consequently, absorbing the boundary case into the activated set, the optimal power profile reduces to the on–off scheme in (13). □

## APPENDIX B PROOF OF LEMMA 1

By leveraging the moment-matching based Gamma approximation technique introduced in [42]–[44], the PDF of $T _ { \mathrm { w } } - \sigma _ { \mathrm { w } } ^ { 2 }$ in (17) can be approximated as

$$
T _ {\mathrm{w}} - \sigma_ {\mathrm{w}} ^ {2} \sim \left\{ \begin{array}{l l} \Gamma \bigg (\frac {\theta^ {2}}{\Theta}, \frac {\Theta}{\theta} \bigg), & \mathcal {H} _ {0}, \\ \Gamma \bigg (\frac {\theta^ {2}}{\Theta}, \frac {\Theta}{\theta} \bigg) * \Gamma (1, \lambda_ {\mathrm{a,w}} P _ {\mathrm{a}}), & \mathcal {H} _ {1}, \end{array} \right.\tag{51}
$$

where $\begin{array} { r } { \theta \ = \ \sum _ { i = 1 } ^ { K } \lambda _ { m _ { i } , \mathrm { w } } P _ { \mathrm { m a x } } } \end{array}$ and $\begin{array} { r } { \Theta = \sum _ { i = 1 } ^ { K } \lambda _ { m _ { i } , \mathrm { w } } ^ { 2 } P _ { \mathrm { m a x } } ^ { 2 } . } \end{array}$ Recall that a Gamma distribution converges to a Gaussian distribution as its shape parameter increases [36, Sec. 5.5], [45, Sec. 2.8]. In our scenario, the sufficiently large number of cooperative users, K, results in a large shape parameter (51).

Consequently, conditioned on the selected set $s ,$ the equa tion of (51) can be approximated to

$$
T _ {\mathrm{w}} - \sigma_ {\mathrm{w}} ^ {2} \mid \mathcal {S} \sim \left\{ \begin{array}{l l} \mathcal {N} (\theta_ {\mathcal {S}}, \Theta_ {\mathcal {S}}), & \mathcal {H} _ {0}, \\ \mathcal {N} (\theta_ {\mathcal {S}}, \Theta_ {\mathcal {S}}) * \Gamma (1, \lambda_ {\mathrm{a,w}} P _ {\mathrm{a}}), \mathcal {H} _ {1}, \end{array} \right.\tag{52}
$$

where $\begin{array} { r } { \theta _ { S } = \sum _ { m \in \mathcal { S } } \lambda _ { m , \mathrm { w } } P _ { \mathrm { m a x } } } \end{array}$ and $\begin{array} { r } { \Theta _ { S } = \sum _ { m \in  { \mathcal { S } } } \lambda _ { m , \mathrm { w } } ^ { 2 } P _ { \operatorname* { m a x } } ^ { 2 } . } \end{array}$ As S is randomly drawn and unknown to Willie, the overall statistics of $T _ { \mathrm { w } } - \sigma _ { \mathrm { w } } ^ { 2 }$ must incorporate this selection induced randomness. Equivalently, the mean and variance must be computed by averaging the conditional moments with respect to the random user selection set S.

By the law of total expectation and variance [36, Sec. 4.4], [45, Ch. 3], the overall mean and variance of the aggregate cooperative interference are obtained by averaging over the order-statistics-induced selected user sequence. Since $r _ { m } = | h _ { m , \mathrm { b } } | ^ { 2 } / \lambda _ { m , \mathrm { w } }$ follows an exponential distribution with rate $\alpha _ { m } ~ = ~ \lambda _ { m , \mathrm { w } } / \lambda _ { m , \mathrm { b } } ,$ the selected cooperative users are not, in general, uniformly distributed over all K-user subsets. Rather, their selection is induced by the order-statistics of $\lbrace r _ { m } \rbrace _ { m = 1 } ^ { M }$ . For an ordered selected sequence $( m _ { 1 } , \ldots , m _ { K } )$ where all indices are distinct, the probability that these users are selected as the first K users in this order is given by

$$
p (m _ {1}, \dots , m _ {K}) = \prod_ {\ell = 1} ^ {K} \frac {\alpha_ {m _ {\ell}}}{\sum_ {j \notin \{m _ {1} , \dots , m _ {\ell - 1} \}} \alpha_ {j}},\tag{53}
$$

where $\{ m _ { 1 } , \ldots , m _ { \ell - 1 } \}$ is empty for $\ell = 1$ . Then, the firstorder inclusion probability of user m is defined as

$$
\pi_{m}^{(K)}\triangleq \sum_{\substack{(m_{1},\ldots ,m_{K}):\\ m\in \{m_{1},\ldots ,m_{K}\}}}p(m_{1},\ldots ,m_{K}),\tag{54}
$$

and the second-order inclusion probability of users m and n, m ̸= n, is defined as

$$
\pi_{m,n}^{(K)}\triangleq \sum_{\substack{(m_{1},\ldots ,m_{K}):\\ m,n\in \{m_{1},\ldots ,m_{K}\}}}p(m_{1},\ldots ,m_{K}).\tag{55}
$$

In (54) and (55), the summations are taken over all ordered selected sequences $( m _ { 1 } , \ldots , m _ { K } )$ with distinct indices.

Then, $\begin{array} { r } { \Xi _ { K } \triangleq P _ { \mathrm { m a x } } \sum _ { m = 1 } ^ { M } \pi _ { m } ^ { ( K ) } \lambda _ { m , \mathrm { w } } } \end{array}$ as stated in Lemma 1, and $\begin{array} { r l r } { \Sigma _ { K } } & { { } \triangleq } & { P _ { \operatorname* { m a x } } ^ { 2 } \left( \mathbb { E } [ A _ { K } ] + \mathrm { V a r } ( L _ { K } ) \right) } \end{array}$ ), where $\begin{array} { l l } { L _ { K } } & { \triangleq } \end{array}$ .1 $\textstyle \sum _ { i = 1 } ^ { K } \lambda _ { m _ { i } , \mathrm { w } }$ and $\begin{array} { r } { \overrightarrow { A _ { K } } \triangleq \sum _ { i = 1 } ^ { K } \lambda _ { m _ { i } , \mathrm { w } } ^ { 2 } } \end{array}$ . Expanding $\mathbb { E } [ A _ { K } ]$ and $\mathrm { V a r } ( L _ { K } )$ with the inclusion probabilities $\pi _ { m } ^ { ( K ) }$ and $\pi _ { m , n } ^ { ( K ) }$ in (54) and (55) yields exactly (19).

Accordingly, the false-alarm probability, $P _ { F A }$ , is defined as

$$
P _ {\mathrm{FA}} = \operatorname * {P r} \left(T _ {\mathrm{w}} - \sigma_ {\mathrm{w}} ^ {2} > \hat {\gamma} \mid \mathcal {H} _ {0}\right) \approx Q \left(\frac {\hat {\gamma} - \Xi_ {K}}{\sqrt {\Sigma_ {K}}}\right),\tag{56}
$$

where $\hat { \gamma } \triangleq \gamma - \sigma _ { \mathrm { w } } ^ { 2 }$ . In addition, the miss-detection probability at Willie can be derived as

$$
\begin{array}{l} P _ {\mathrm{MD}} = \operatorname * {P r} \big (T _ {\mathrm{w}} - \sigma_ {\mathrm{w}} ^ {2} \leq \hat {\gamma}   |   \mathcal {H} _ {1} \big) = \operatorname * {P r} (X + Y \leq \hat {\gamma}) \\ = \int_ {- \infty} ^ {\hat {\gamma}} f _ {Y} (y) \left[ 1 - \exp \left(- \frac {\hat {\gamma} - y}{\Delta}\right) \right] d y \\ = Q \left(- \frac {\hat {\gamma} - \Xi_ {K}}{\sqrt {\Sigma_ {K}}}\right) - \exp (a _ {\gamma})   Q (b _ {\gamma})  , \end{array}\tag{57}
$$

where $X \sim \Gamma ( 1 , \Delta )$ with $\Delta \triangleq P _ { \mathrm { a } } \lambda _ { \mathrm { a , w } }$ , and $f _ { Y } ( y )$ denotes the PDF of $Y \sim { \mathcal { N } } ( \Xi _ { K } , \Sigma _ { K } )$ . Define

$$
a _ {\gamma} \triangleq - \frac {2 \Delta (\hat {\gamma} - \Xi_ {K}) - \Sigma_ {K}}{2 \Delta^ {2}}, \quad b _ {\gamma} \triangleq - \frac {\Delta (\hat {\gamma} - \Xi_ {K}) - \Sigma_ {K}}{\sqrt {\Sigma_ {K}} \Delta}.
$$

Combining (57) with (56) gives $\zeta ( \gamma ) = P _ { \mathrm { F A } } + P _ { \mathrm { M D } } = 1 -$ $\exp ( a _ { \gamma } ) Q ( b _ { \gamma } )$ , which matches (18).

## REFERENCES

[1] Y. Jiang, L. Wang, H.-H. Chen, and X. Shen, “Physical layer covert communication in b5g wireless networks—its research, applications, and challenges,” Proceedings of the IEEE, vol. 112, no. 1, pp. 47–82, 2024.

[2] K. Cao, T. Wang, P. D. Diamantoulakis, X. Li, C. Yuen, and G. K. Karagiannidis, “Reliable and secure wireless-powered communications via hybrid active-passive double-ris,” IEEE J. Sel. Areas Commun., vol. 44, pp. 3828–3844, 2026.

[3] K. Cao, S. Xu, P. D. Diamantoulakis, C. Yang, B. Zheng, X. Li, and C. Yuen, “Self-sustainable active metasurface (sam): Reliable and secure communications,” IEEE Trans. Wireless Commun., vol. 25, pp. 12 325– 12 340, 2026.

[4] B. A. Bash, D. Goeckel, and D. Towsley, “Limits of reliable communication with low probability of detection on AWGN channels,” IEEE J. Sel. Areas Commun., vol. 31, no. 9, pp. 1921–1930, 2013.

[5] P. H. Che, M. Bakshi, and S. Jaggi, “Reliable deniable communication: Hiding messages in noise,” in Proceedings of IEEE International Symposium on Information Theory, 2013, pp. 2945–2949.

[6] M. R. Bloch, “Covert communication over noisy channels: A resolvability perspective,” IEEE Trans. Inf. Theory, vol. 62, no. 5, pp. 2334–2354, 2016.

[7] L. Wang, G. W. Wornell, and L. Zheng, “Fundamental limits of communication with low probability of detection,” IEEE Trans. Inf. Theory, vol. 62, no. 6, pp. 3493–3503, 2016.

[8] K. S. K. Arumugam and M. R. Bloch, “Keyless covert communication over multiple-access channels,” in Proceedings of IEEE International Symposium on Information Theory, 2016, pp. 2229–2233.

[9] —, “Covert communication over a k-user multiple-access channel,” IEEE Trans. Inf. Theory, vol. 65, no. 11, pp. 7020–7044, 2019.

[10] V. Y. F. Tan and S.-H. Lee, “Time-division is optimal for covert communication over some broadcast channels,” IEEE Trans. Inf. Forensics Security, vol. 14, no. 5, pp. 1377–1389, 2019.

[11] K.-H. Cho and S.-H. Lee, “Treating interference as noise is optimal for covert communication over interference channels,” IEEE Trans. Inf. Forensics Security, vol. 16, pp. 322–332, 2021.

[12] S. Lee, R. J. Baxley, M. A. Weitnauer, and B. Walkenhorst, “Achieving undetectable communication,” IEEE J. Sel. Topics Signal Process., vol. 9, no. 7, pp. 1195–1205, 2015.

[13] K. Shahzad and X. Zhou, “Covert wireless communications under quasi-static fading with channel uncertainty,” IEEE Trans. Inf. Forensics Security, vol. 16, pp. 1104–1116, 2021.

[14] J. Wang, W. Tang, Q. Zhu, X. Li, H. Rao, and S. Li, “Covert communication with the help of relay and channel uncertainty,” IEEE Wireless Commun. Lett., vol. 8, no. 1, pp. 317–320, 2019.

[15] R. Sun, B. Yang, S. Ma, Y. Shen, and X. Jiang, “Covert rate maximization in wireless full-duplex relaying systems with power control,” IEEE Trans. Commun., vol. 69, no. 9, pp. 6198–6212, 2021.

[16] R. Sun, B. Yang, Y. Shen, X. Jiang, and T. Taleb, “Covertness and secrecy study in untrusted relay-assisted d2d networks,” IEEE Internet Things J., vol. 10, no. 1, pp. 17–30, 2023.

[17] J. Bai, J. He, Y. Chen, Y. Shen, and X. Jiang, “On covert communication performance with outdated csi in wireless greedy relay systems,” IEEE Trans. Inf. Forensics Security, vol. 17, pp. 2920–2935, 2022.

[18] T. V. Sobers, B. A. Bash, S. Guha, D. Towsley, and D. Goeckel, “Covert communication in the presence of an uninformed jammer,” IEEE Trans. Wireless Commun., vol. 16, no. 9, pp. 6193–6206, 2017.

[19] K. Li, P. A. Kelly, and D. Goeckel, “Optimal power adaptation in covert communication with an uninformed jammer,” IEEE Trans. Wireless Commun., vol. 19, no. 5, pp. 3463–3473, 2020.

[20] K. Shahzad, X. Zhou, S. Yan, J. Hu, F. Shu, and J. Li, “Achieving covert wireless communications using a full-duplex receiver,” IEEE Trans. Wireless Commun., vol. 17, no. 12, pp. 8517–8530, 2018.

[21] J. Hu, S. Yan, X. Zhou, F. Shu, and J. Li, “Covert wireless communications with channel inversion power control in Rayleigh fading,” IEEE Trans. Veh. Technol., vol. 68, no. 12, pp. 12 135–12 149, 2019.

[22] J. Zhang, M. Li, M.-J. Zhao, X. Ji, and W. Xu, “Multi-user beam training and transmission design for covert millimeter-wave communication,” IEEE Trans. Inf. Forensics Security, vol. 17, pp. 1528–1543, 2022.

[23] H. Mao, X. Pi, L. Zhu, Z. Xiao, X.-G. Xia, and R. Zhang, “Sum rate maximization for movable antenna enhanced multiuser covert communications,” IEEE Wireless Commun. Lett., vol. 14, no. 3, pp. 611–615, 2025.

[24] X. Jiang, Z. Yang, N. Zhao, Y. Chen, Z. Ding, and X. Wang, “Resource allocation and trajectory optimization for uav-enabled multi-user covert communications,” IEEE Trans. Veh. Technol., vol. 70, no. 2, pp. 1989– 1994, 2021.

[25] H. Lei, J. Jiang, I. S. Ansari, G. Pan, and M.-S. Alouini, “Trajectory and power design for aerial multi-user covert communications,” IEEE Trans. Aerosp. Electron. Syst., vol. 60, no. 4, pp. 4574–4589, 2024.

[26] J. Xu, L. Bai, X. Xie, and L. Zhou, “Collaborative secret and covert communications for multi-user multi-antenna uplink uav systems: Design and optimization,” IEEE Trans. Wireless Commun., vol. 24, no. 7, pp. 6020–6035, 2025.

[27] B. He, S. Yan, X. Zhou, and H. Jafarkhani, “Covert wireless communication with a poisson field of interferers,” IEEE Trans. Wireless Commun., vol. 17, no. 9, pp. 6005–6017, 2018.

[28] R. Soltani, D. Goeckel, D. Towsley, B. A. Bash, and S. Guha, “Covert wireless communication with artificial noise generation,” IEEE Trans. Wireless Commun., vol. 17, no. 11, pp. 7252–7267, 2018.

[29] T.-X. Zheng, Z. Yang, C. Wang, Z. Li, J. Yuan, and X. Guan, “Wireless covert communications aided by distributed cooperative jamming over slow fading channels,” IEEE Trans. Wireless Commun., vol. 20, no. 11, pp. 7026–7039, 2021.

[30] J. Lee, D. T. Dinh, H. Yeom, S.-H. Lee, and J. Ha, “Multiuser cooperation for covert communication under quasi-static fading,” IEEE Trans. Inf. Forensics Security, vol. 18, pp. 4625–4639, 2023.

[31] J. Lee, H. Yeom, S.-H. Lee, and J. Ha, “Channel correlation in multiuser covert communication: Friend or foe?” IEEE Trans. Inf. Forensics Security, vol. 19, pp. 1469–1482, 2024.

[32] H. Yeom, J. Lee, S.-H. Lee, and J. Ha, “Covert communication with multi-users cooperation at unequal distances,” in Proceedings of IEEE International Conference on Communications, 2024, pp. 121–126.

[33] T. Xu, L. Sun, S. Yan, J. Hu, and F. Shu, “Pilot-based channel estimation design in covert wireless communication,” arXiv preprint arXiv:1908.00226, 2019.

[34] B. A. Bash, D. Goeckel, and D. Towsley, “Covert communication gains from adversary’s ignorance of transmission time,” IEEE Trans. Wireless Commun., vol. 15, no. 12, pp. 8394–8405, 2016.

[35] J. Neyman and E. S. Pearson, “IX. On the problem of the most efficient tests of statistical hypotheses,” Philosophical Transactions of the Royal Society of London. Series A, Containing Papers of a Mathematical or Physical Character, vol. 231, no. 694-706, pp. 289–337, 1933.

[36] G. Casella and R. L. Berger, Statistical Inference, 2nd ed. Pacific Grove, CA, USA: Duxbury Press, 2002.

[37] M. Chiani, D. Dardari, and M. Simon, “New exponential bounds and approximations for the computation of error probability in fading channels,” IEEE Trans. Wireless Commun., vol. 2, no. 4, pp. 840–845, 2003.

[38] M. Abramowitz and I. A. Stegun, Handbook of mathematical functions with formulas, graphs, and mathematical tables. US Government printing office, 1964, vol. 55.

[39] W. G. Cochran, Sampling Techniques, 3rd ed. John Wiley & Sons, 1977.

[40] S. L. Lohr, Sampling: Design and Analysis, 3rd ed. CRC Press, 2019.

[41] 3rd Generation Partnership Project (3GPP), “Spatial channel model for Multiple Input Multiple Output (MIMO) simulations,” 3GPP, Technical Report TR 25.996 V19.0.0, Sep. 2025.

[42] A. M. Mathai, A Handbook of Generalized Special Functions for Statistical and Physical Sciences. Oxford University Press, 1993.

[43] P. G. Moschopoulos, “The distribution of the sum of independent gamma random variables,” Annals of Statistics, vol. 13, no. 1, pp. 365–372, 1985.

[44] S. Covo, “A novel single-gamma approximation to the sum of independent gamma random variables,” Electronic Journal of Statistics, vol. 8, pp. 1274–1280, 2014.

[45] S. M. Ross, Introduction to Probability Models, 12th ed. Amsterdam, The Netherlands: Academic Press, 2019.

[46] N. Sedrakyan, “About the applications of mean value theorems for analyzing inequalities,” The Mathematical Gazette, vol. 81, no. 492, pp. 136–139, 1997.
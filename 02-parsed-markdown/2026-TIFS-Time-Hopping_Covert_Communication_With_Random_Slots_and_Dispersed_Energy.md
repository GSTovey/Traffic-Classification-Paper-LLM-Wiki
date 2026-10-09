# Time-Hopping Covert Communication With Random Slots and Dispersed Energy

Kun Lu , Zhe Song , Shuai Wang , Senior Member, IEEE, Tingting Li , Gaofeng Pan , Senior Member, IEEE, Heng Liu , and George Karagiannidis , Fellow, IEEE

Abstract—The growth of communication technologies has led to a corresponding increase in the need for information security. The use of covert communication techniques has the potential to significantly reduce the likelihood of the transmitted signal being intercepted by unintended receivers, thereby significantly increasing the security of the information. In this paper, we propose an energy-dispersed random time-hopping (ED-RTH) covert communication scheme. Building on existing time uncertainty schemes, this scheme further enhances time uncertainty through random time-hopping, while dispersing signal energy to achieve stronger covertness. We present a model for analyzing the covertness of the ED-RTH scheme. Given the complexity of the likelihood ratio distribution, the Kullback-Leibler (KL) divergence is used to analyze the lower bound of Willie’s detection error probability. Through constructing behaviorallevel simulations for validation, we investigated the impact of the number of dispersed time slots K on both Willie’s detection error probability and the system’s covert throughput. Finally we compared the proposed ED-RTH scheme with existing time uncertainty scheme, and the results demonstrate that the ED-RTH scheme achieves significantly enhanced covertness.

Index Terms—Covert communications, time-hopping, finite blocklength, random slots.

## I. INTRODUCTION

O <sup>VER</sup> <sup>the</sup> <sup>past</sup> <sup>few</sup> <sup>decades,</sup> <sup>wireless</sup> <sup>communica-</sup>tion technology has advanced rapidly and has found tion technology has advanced rapidly and has found widespread application in fields as diverse as finance, meteorology, education, healthcare, navigation, and the military [1], [2]. However, the inherently open nature of communication signals means that they can be intercepted by any device within the transmission range, which conflicts with users growing demands for privacy. As a result, communication security has emerged as a major challenge for future wireless communication systems [3].

Traditional communication systems typically employ information encryption to prevent unauthorized access by noncooperative parties to enhance security [4]. However, with the advancement of technology, adversaries can now use supercomputers to continuously improve their decryption capabilities. Consequently, physical layer security technologies have been proposed [5], which exploit the diferent characteristics of wireless channels between the sender, cooperative, and non-cooperative parties to enhance system security. These technologies have been extensively studied, including secure beamforming with multiple antenna nodes [6], anonymous communication [7], and radio frequency fingerprinting [8]. In addition to ensuring the confidentiality and integrity of transmitted information, users increasingly seek to prevent their communication activities from being detected by uncooperative entities. Many attacks on wireless networks are based on the attacker’s ability to identify ongoing transmissions, as shown in Refs. [9] and [10]. If non-cooperative parties remain unaware of the presence of information transmission, potential network attacks can be efectively avoided. Detecting communication activity in military communications could reveal movements within a given area. Therefore, research on covert communications is of critical importance [11], [12].

Initially, the basic model for studying covert communication is the Prisoner’s Problem, first introduced by Wyner in 1975 [13]. In this model, Alice and Bob are locked in separate cells and try to coordinate an escape plan. They are allowed to exchange messages, but all their communications are monitored by a guard, Willie. If Willie discovers secret communications, the prisoners will face punitive measures. Therefore, the prisoners must use covert communication to exchange their escape plans. In the prisoners’ problem, Willie’s goal is merely to detect the existence of secret information without needing to know the content of the message, which is the primary diference between covert and secure communication. Research in covert communication began quite early. For example, methods such as Short Burst Communication [14] and Spread Spectrum techniques [15] are primarily used in the early days. Spread spectrum techniques primarily include Direct Sequence Spread Spectrum (DS-SS) [16] and Frequency Hopping Spread Spectrum (FH-SS) [17]. These signaling techniques deliberately expand the bandwidth of a signal in the frequency domain, occupying a much larger bandwidth than the original information [18]. This intentional use of spectrum resources results in low power density in the frequency domain and noise-like waveforms in the time domain, significantly reducing the probability of detection and interception [19].

Notably, the quantitative analysis of covert communication systems began in 2013, when Bash et al. [20] approached low detectability probability (LDP) communication from an information-theoretic perspective and introduced the concept of covert communication. Their research showed that the capacity for reliable transmission over an additive white Gaussian noise (AWGN) channel is limited by the square root law (SRL). The SRL states that for a code block of length n, <sub>covert communication can transmit O(</sub> √<sub>n) bits of information.</sub> In Ref. [21], LDP communication over discrete memoryless channels (DMC) was studied by Wang. They determined the maximum amount of information and block length that can be transmitted under the SRL condition. For DMCs, the authors of Ref. [22] highlighted how the choice of covertness metric afects the information-theoretic limits of covert communication. A coding scheme based on channel resolvability for DMCs was developed in Ref. [23], which was also extended to the Binary Symmetric Channel (BSC). Similarly, according to Ref. [24], it was shown that if the channel conditions between legitimate communicators are better than those of the monitoring channel, covert communication can be achieved even without a shared secret key by public coding. In the context of MIMO Gaussian channels, Abdelaziz et al. [25] showed that while the SRL remains valid, the number of bits that can be covertly transmitted grows exponentially with the number of transmit antennas.

To further increase the covert nature of the system, researchers have begun to exploit inherent uncertainties in the communication system to reduce the detection capabilities of eavesdroppers. These uncertainties include noise, channel, and transmission time uncertainties. He et al. [26] studied covert communication considering the noise uncertainty distribution and provided the maximum achievable communication rates under both bounded and unbounded noise uncertainty models. In Ref. [27], Ta et al. analyzed the combined efects of channel and noise uncertainties on the average eavesdropper detection probability and covert throughput in Rayleigh fading channels, and demonstrated that channel fading is critical for covert communication. Bash et al. [28] proposed that using random timeslot communication can achieve constant-rate covert communication, provided there are enough available timeslots. In this paper, we focus on improving system stealth by exploiting time uncertainty.

To better approximate practical communication systems, Xu et al. [29] and Lu et al. [30], [31] have considered introducing timing uncertainty into finite blocklength communication models. In Ref. [29], Xu et al. considered that the channel used in Alice’s transmission block follows a binomial distribution. Compared to the traditional approach, where every channel used in the transmission block is occupied, the random selection of channel usage further reduces the diference between Alice’s transmission and idle states, thereby increasing Willie’s detection error probability. According to Ref. [30], a random sub-slot selection (RSS) scheme has been proposed, where a sub-slot is randomly selected within a communication block to deceive Willie. It is shown that the RSS scheme can significantly improve the efective covert throughput under extremely tight secrecy constraints. Subsequently, in Ref. [31], they proposed a random channel use selection (RCUS) scheme with stronger timing randomness. The results show that when covertness constraints are extremely strict, RCUS outperforms the RSS scheme in terms of performance. However, research on time uncertainty has primarily focused on randomness in time without considering the dispersion of energy. From the perspective of practical communication systems, legitimate parties should aim to improve covertness as much as possible without changing the average communication rate or the total power of the transmitter.

Motivated by these observations, we consider an energydispersed random time-hopping (ED-RTH) covert communication scheme in this paper. Unlike the time uncertainty scheme in Ref. [28], our approach considers the case of finite block length and transmits over K time slots. Specifically, the energy of signal is dispersed across K time slots for time-hopping transmission. As dispersed slots increase, the average transmission power per channel use correspondingly decreases. We developed a covertness analysis model for this scheme. Compared with Ref. [31], where Willie uses energy detection, we consider Willie employing the optimal LRT and quantitatively analyze the relationship between system covertness and the number of dispersed time slots K using Kullback-Leibler (KL) divergence. Finally, behavioral-level simulations further validate the correctness of the analytical results.

In the model of Ref. [20], Willie has deterministic knowledge of the channel uses when Alice may transmit covert information, and Alice continuously sends n symbols. In Ref. [28], Alice randomly selects one time slot from a time period to transmit n symbols, and the introduced timing randomness improves system covertness. In this paper, we consider randomly selecting K time slots from T time slots in a period to transmit covert information. Meanwhile, the energy originally allocated for n channel uses is evenly dispersed across nK channel uses. By maintaining the total transmitted energy and the number of efective information bits unchanged, this approach further enhances system covertness. Clearly, when $K ~ = ~ T ~ = ~ 1$ , the proposed model reduces to that of Ref. [20] and when $T \ \gg \ K \ = \ 1$ , it reduces to the model of Ref. [28]. Compared with $K = T = 1$ , the introduction of timing randomness improves covertness. As K increases from 1 $( 1 < K < T )$ , the ED-RTH scheme not only further increases timing uncertainty compared to Ref. [28] but also introduces energy dispersion, efectively enhancing covertness. When K increases continuously until K = T, the model reverts to the extended model of Ref. [20], with the total number of channel uses being nT.

Although both ED-RTH and the RCUS scheme in [31] employ random selection of transmission opportunities, the proposed ED-RTH difers fundamentally in three important aspects: (1) Signal model: ED-RTH operates at the timeslot level, where each selected slot contains n consecutive symbols and the K selected slots carry the same information with intentionally dispersed energy. In contrast, the dispersed channel uses in RCUS correspond to individual symbols that do not represent repeated information. (2) Receiver processing: ED-RTH requires coherent combining across the K selected slots followed by codebook-based decoding, whereas RCUS does not involve any cross-slot coherent processing. (3) Design objective and performance characterization: ED-RTH evaluates covertness through the KL divergence and LRT-based detection, revealing how energy dispersion and temporal randomness jointly increase the warden’s detection uncertainty. RCUS, on the other hand, focuses on Age-of-Information under covertness constraints and does not analyze how temporal randomness directly influences the warden’s detection error probability. These diferences highlight the distinctive structure and operational principles of ED-RTH compared with RCUS.

Remark: It should be noted that in practical systems, Bob generally knows the time slots used by Alice precisely, so a large T is often set to introduce significant timing uncertainty at Willie’s detector. Excessively large K, however, would lead to too low signal-to-noise ratio (SNR) at Bob, drastically increasing the complexity of the legitimate receiver. Therefore, in practical ED-RTH systems, the primary focus is on the scenario where $T > K$ . The subsequent discussion in this paper regarding $T = K$ is mainly to highlight the connection with traditional schemes.

The main contributions of this paper are summarized below.

We propose an ED-RTH covert communication scheme. Based on existing timing uncertainty schemes, it further enhances timing uncertainty through random time hopping while achieving the dispersal of signal energy via transmission over multiple time slots. Simulation and analysis results indicate that compared to existing timing uncertainty schemes, the ED-RTH scheme exhibits higher covertness and can achieve higher covert throughput under the same covertness constraints.

• We establish a covertness analysis model for the ED-RTH scheme. In cases where the LRT statistic is challenging to analyze, we use KL divergence to analyze the lower bound of Willie’s detection error probability. Through Monte Carlo simulations, we determine the uantitative relationship between the detection error probability and the number of dispersed time slots K, and validated this relationship through behavioral simulations. The conclusion drawn is that Willie’s detection error probability increases with K, but the increment of the detection error probability decreases rapidly as K increases. We conduct a behavioral simulation to analyze the probability of detection error when Willie employs energy detection, and compare this performance with that of the optimal LRT detection. The results demonstrate that the number of dispersed time slots, K, has a negligible impact on Willie’s detection performance. When K is small, LRT significantly outperforms energy detection. At the point where $K = T$ , the performance of likelihood ratio detection is identical to that of energy detection.

• We conducted simulations and analyses of the covert throughput under the ED-RTH scheme. In this scheme, since the total transmission energy remains constant, the covert throughput after coherent combining across time slots does not have a direct relationship with the number of dispersed time slots K. However, as K increases, the system’s covertness is enhanced. Under the same covertness constraint, this improvement in covertness relaxes the limitation on transmit power, thereby further improving the system’s covert throughput. Additionally, we found that for varying levels of covertness constraints, diferent coding rates are required to achieve maximum covert throughput. Specifically, as the covertness constraints become more stringent, the optimal coding rate tends to be lower.

TABLE I  
LIST OF MAIN NOTATIONS

<table><tr><td>Notation</td><td>Definition</td></tr><tr><td>T</td><td>Total number of time slots</td></tr><tr><td>K</td><td>The number of dispersed time slots</td></tr><tr><td>n</td><td>The number of channel uses per slot</td></tr><tr><td>N</td><td>The total code length of a coding block</td></tr><tr><td>D</td><td>The number of bits carried by a coding block</td></tr><tr><td>R</td><td>The coding rate</td></tr><tr><td> $t_A$ </td><td>The set of time slots chosen by Alice</td></tr><tr><td> $P_a$ </td><td>The transmission power per symbol for Alice</td></tr><tr><td> $P_a^*$ </td><td>The average power per symbol when K=1</td></tr><tr><td>P</td><td>The total transmission power of Alice</td></tr><tr><td>x[i]</td><td>The symbols transmitted by Alice</td></tr><tr><td> $y_w$ </td><td>The entire observation set of Willie</td></tr><tr><td> $y_w[i]$ </td><td>The observed signal at Willie&#x27;s receive</td></tr><tr><td> $z_w[i]$ </td><td>The noise at Willie&#x27;s receiver</td></tr><tr><td> $\sigma_w^2$ </td><td>The power of the noise at Willie&#x27;s receiver</td></tr><tr><td> $\sigma_b^2$ </td><td>The power of the noise at Bob&#x27;s receiver</td></tr><tr><td> $\gamma_b$ </td><td>The SNR of the effective signal received by Bob</td></tr><tr><td> $\gamma_w$ </td><td>The SNR of the effective signal received by Willie</td></tr><tr><td>Pr(.)</td><td>The probability of the content</td></tr><tr><td>E[.]</td><td>The expectation of the content</td></tr><tr><td> $\mathcal{H}_0, \mathcal{H}_1$ </td><td>The null hypothesis and the alternative hypothesis</td></tr><tr><td> $\mathcal{D}_0, \mathcal{D}_1$ </td><td>Willie&#x27;s decisions that infer whether Alice&#x27;s transmission is present or not, respectively.</td></tr><tr><td>α,β</td><td>The false alarm probability and the miss detection probability</td></tr><tr><td>ξ</td><td>The detection error probability for Willie</td></tr><tr><td>ε</td><td>The covertness constraint coefficient</td></tr><tr><td>δ</td><td>The decoding error probability at Bob&#x27;s receive</td></tr><tr><td>η</td><td>The covert throughput</td></tr><tr><td>f0( $y_w$ ), f1( $y_w$ )</td><td>The PDF of  $y_w$  under the null hypothesis  $\mathcal{H}_0$  and  $\mathcal{H}_1$  respectively</td></tr><tr><td>Λ( $y_w$ )</td><td>The likelihood ratio of  $y_w$ </td></tr><tr><td>τLRT</td><td>Willie&#x27;s detection threshold for LRT</td></tr><tr><td>Ξ( $y_w$ )</td><td>The average energy of the received signal  $y_w$ </td></tr><tr><td>τED</td><td>Willie&#x27;s detection threshold for energy detection</td></tr><tr><td> $\mathcal{V}_T(\mathbb{P}_0||\mathbb{P}_1)$ </td><td>The total variation distance between the probability distributions  $\mathbb{P}_0$  and  $\mathbb{P}_1$ </td></tr><tr><td> $\mathcal{D}(\mathbb{P}_0||\mathbb{P}_1), \mathcal{D}(K)$ </td><td>The KL divergence between the probability distributions  $\mathbb{P}_0$  and  $\mathbb{P}_1$ </td></tr></table>

The rest of this paper is organized as follows. Section II details the system model and two detection methods of Willie. Section III studies the relationship between covertness and the number of dispersed slots. We introduce behavioral simulation methods in Section IV and provide results validating our analysis. Finally, Section V draws the conclusions.

Some key notations and related descriptions are listed in Table I.

![](images/30b186a3bfabc7385947665ffcf289b7ab814751b398e51cb0ff13053a9531b2.jpg)  
Fig. 1. Illustration of the system model for covert communications.

![](images/d451f84d8b3842ed2934f4819916dd7456f7cc8c3228d5e39addd2d73f02199d.jpg)  
Fig. 2. A comparison between the scheme considered in this paper and existing time-uncertain covert communication schemes.

## II. SYSTEM MODEL

## A. Classic Covert Communication Model

In this study, we consider a conventional three-node model for covert communication, as illustrated in Fig. 1. The model comprises three distinct entities: A transmitter, designated as “Alice”, a receiver, designated as “Bob,” and a monitor, designated as “Willie.” The principal objective of Willie is to monitor Alice’s transmission activities by conducting statistical hypothesis tests on the received signal to ascertain whether Alice is engaged in transmission. If Alice’s transmission is detected, punitive measures will be taken against her. Consequently, Alice and Bob seek to increase the probability of error in Willie’s detection process. It is assumed that each node within this model is equipped with a single antenna, and both the transmission channel from Alice to Bob and the channel from Alice to Willie are characterized as AWGN channels.

## B. ED-RTH Transmission Scheme

In prior studies on time uncertainty in communication models, researchers have typically considered either a single time slot scenario or assumed fixed transmission power for each symbol when discussing covert transmission strategies. Therefore, these approaches failed to consider the possibility of dispersing energy across multiple time slots. This paper aims at making a pioneering efort to analyze the covertness of an ED-RTH covert communication scheme, and then, a comparative analysis of the proposed scheme in this paper is provided against other existing time-uncertain covert communication schemes, as illustrated in Fig. 2. In this figure, the shaded regions denote the time slots selected by Alice for transmission, with the shade intensity corresponding to the average power of each symbol within those respective slots.

Alice partitions the time horizon into potential transmission windows, each consisting of T time slots. In each window, Alice decides whether to transmit covert information with a prior probability $\rho .$ Furthermore, each time slot comprises n symbol periods. When Alice transmits, she randomly selects K time slots from a total of T available slots for transmission, resulting in $C _ { T } ^ { K }$ possible combinations of selection, where K can range from 1 to T. She repeats the n-symbol message across the K selected time slots. At the same time, the signal energy that was originally transmitted within a single slot is evenly divided among the K slots. In each selected time slot, Alice transmits n real-valued symbols, amounting to a total of nK symbols x[i]. The transmission power per channel uses for Alice is equivelant for every slot and denoted as $P _ { \mathrm { a } } ,$ , with means $\mathbb { E } \left[ \dot { x } ^ { 2 } [ i ] \right] ~ = ~ P _ { \mathrm { a } }$ . The set of K time slots chosen by Alice is defined as $\mathbf { t } _ { \mathrm { A } }$ and is a member of the set $\{ \mathbf { t } _ { 1 } , \mathbf { t } _ { 2 } , \dots , \mathbf { t } _ { j } , \dots , \mathbf { t } _ { C _ { T } ^ { K } } \}$ , where j ranges from 1 to $C _ { T } ^ { K }$ . Both $\mathbf { t } _ { \mathrm { A } }$ and each $\mathbf { t } _ { j }$ represent a collection of K time slots, with $\mathbf { t } _ { j } = \{ t _ { j , 1 } , t _ { j , 2 } , \ldots , t _ { j , K } \}$ . Across these T time slots, Alice’s total transmission power is denoted as P. When K assumes diferent values, the power per symbol $P _ { \mathrm { a } }$ is given by $P _ { \mathrm { { a } } } ~ = ~ P _ { \mathrm { { a } } } ^ { \ast } / K ,$ where $P _ { \mathrm { ~ a ~ } } ^ { * }$ is the average power per symbol when $K \ = \ 1$ Consequently, the total power P is given by $P = n P _ { \mathrm { a } } ^ { * } = n K P _ { \mathrm { a } }$ In this paper, it is assumed that $P _ { \mathrm { a } } ^ { * } ~ < ~ \sigma _ { \mathrm { w } } ^ { 2 } / 2$ to maintain a desired level of detection error probability for Willie. To maximize the detection error probability of Willie, Alice set her transmit probability ρ to 0.5 in general.

## C. Willie’s Detection Model

In this paper, similar to most studies on covert communications, we consider the worst-case scenario where Willie knows the random dispersion strategy of Alice, including the transmit power per symbol $P _ { \mathrm { a } }$ and the number of used time slots K [28], [32]. The only information unknown to Willie is the set of selected time slots $\mathbf { t } _ { \mathrm { A } }$ . As a result, Willie is compelled to conduct statistical hypothesis testing on his entire observation set ${ \bf y } _ { \mathrm { w } } = \{ { \bf y } _ { \mathrm { w } } ( t ) \} _ { t = 1 } ^ { T }$ . This set comprises $n T$ data points and is used to ascertain whether Alice is engaged in transmission. Specifically, $\mathbf { y } _ { \mathrm { w } } ( t ) = \left[ y _ { \mathrm { w } } \left[ ( t - 1 ) n + 1 \right] , y _ { \mathrm { w } } \left[ ( t - 1 ) n + 2 \right] , \ldots , y _ { \mathrm { w } } \left[ t n \right] \right]$ represents the n observed data points that Willie captures in time slot t. The noise at Willie’s receiver is characterized as AWGN, with $z _ { \mathrm { w } } [ i ] ~ \sim ~ \mathcal { N } ( 0 , \sigma _ { \mathrm { w } } ^ { 2 } )$ . Willie faces a binary hypothesis testing problem.

Let $\mathcal { H } _ { 0 }$ denote the null hypothesis, which assumes that Alice does not transmit any signal, and $\mathcal { H } _ { 1 }$ denote the alternative hypothesis, which assumes that Alice is transmitting. In the case of $\mathcal { H } _ { 0 }$ , the observed signal at Willie’s receiver is solely due to noise, such that

$$
\mathcal {H} _ {0}: y _ {\mathrm{w}} [ i ] = z _ {\mathrm{w}} [ i ].\tag{1}
$$

where i ranges from 1 to $n T$

Conversely, under $\mathcal { H } _ { 1 } .$ , the observed signal is the sum of the transmitted symbol and noise, and can be expressed as

$$
\mathcal {H} _ {1}: \left\{ \begin{array}{l} y _ {\mathrm{w}} [ l ] = x [ l ] + z _ {\mathrm{w}} [ l ], \\ y _ {\mathrm{w}} [ i ] = z _ {\mathrm{w}} [ i ], \end{array} \right.\tag{2}
$$

where l denotes the index of occupied channel uses and i denotes the index of idle channel uses.

If $\mathcal { H } _ { 0 }$ is true and Willie incorrectly concludes that Alice is transmitting, this event is classified as a false alarm, with a probability denoted by α. On the other hand, if $\mathcal { H } _ { 1 }$ is true and Willie fails to detect Alice’s transmission, this is termed a missed detection, with a probability represented by $\beta .$ The false alarm probability can thus be defined as $\alpha \triangleq \operatorname* { P r } ( \mathcal { D } _ { 1 } | \mathcal { H } _ { 0 } ) .$ 2 and the missed detection probability can be defined as $\beta \ { \stackrel { \Delta } { = } }$ $\Pr ( \mathcal { D } _ { 0 } | \mathcal { H } _ { 1 } )$ , where $\mathcal { D } _ { 0 }$ and $\mathcal { D } _ { 1 }$ represent Willie’s decisions that Alice is not transmitting and is transmitting, respectively.

Subsequently, we will examine two distinct detection methods that Willie may employ: LRT and energy detection. It is worth noting that the worst-case scenario, where Willie possesses most of the information and uses LRT, provides us with a lower bound on the covert performance. If Willie lacks any of this knowledge, the covertness will strictly increase. For instance, if K is unknown, Willie may be unable to utilize the LRT and be forced to adopt suboptimal energy detection scheme instead. As will be shown later, this evidently leads to a degradation in detection performance.

1) Likelihood Ratio Test (LRT): It can be noted that Alice’s transmission state is binary (either she transmits or she does not) and the prior knowledge of Alice’s transmission parameters is known to Willie. So the optimal detector for Willie is the likelihood ratio test (LRT) by the Neyman–Pearson lemma [33]. The likelihood ratio is expressed as

$$
\Lambda (\mathbf {y} _ {\mathrm{w}}) = \frac {\mathbb {P} _ {1} \stackrel {{\Delta}} {{=}} f _ {1} (\mathbf {y} _ {\mathrm{w}})}{\mathbb {P} _ {0} \stackrel {{\Delta}} {{=}} f _ {0} (\mathbf {y} _ {\mathrm{w}})},\tag{3}
$$

where $f _ { 0 } ( \mathbf { y } _ { \mathrm { w } } )$ and $f _ { 1 } ( \mathbf { y } _ { \mathrm { w } } )$ denote the probability density functions of the received signal $\mathbf { y } _ { \mathrm { w } }$ at Willie under the null hypothesis $\mathcal { H } _ { 0 }$ and the alternative hypothesis $\mathcal { H } _ { 1 }$ , respectively.

The LRT statistic is compared to a threshold as

$$
\Lambda (\mathbf {y} _ {\mathrm{w}}) \underset {<   \mathcal {D} _ {0}} {\geq^ {\mathcal {D} _ {1}}} \tau_ {\text { LRT }},\tag{4}
$$

where τ<sub>LRT</sub> represents Willie’s detection threshold.

When $\Lambda ( \mathbf { y } _ { \mathrm { w } } ) \ \geq \ \tau _ { \mathrm { L R T } } .$ , the hypothesis $\mathcal { H } _ { 1 }$ is accepted as true. Conversely, when $\Lambda ( \mathbf { y } _ { \mathrm { w } } ) < \tau _ { \mathrm { L R T } } ,$ the hypothesis H is accepted as true. Consequently, Willie’s false alarm and missed detection probabilities can be expressed as

$$
\alpha = \operatorname * {P r} (\Lambda (\mathbf {y} _ {\mathrm{w}}) \geq \tau_ {\mathrm{LRT}} | \mathcal {H} _ {0})\tag{5}
$$

and

$$
\beta = \operatorname * {P r} (\Lambda (\mathbf {y} _ {\mathrm{w}}) <   \tau_ {\mathrm{LRT}} | \mathcal {H} _ {1}),\tag{6}
$$

respectively.

Because of the prior probability of Alice transmitting being 0.5, which is commonly adopted in the literature of covert communications, the optimal threshold for the LRT is set to $\tau _ { \mathrm { L R T } } \ast = 1$ [34].

2) Energy Detection: In the majority of existing literature, the optimal LRT is mathematically equivalent to energy detection. However, the analysis in the next section will demonstrate that in the presence of time uncertainty, LRT no longer maintains equivalence with energy detection. Nonetheless, energy detection can still be employed as a suboptimal detection strategy, ofering significantly lower compexity compared to LRT-based detection. Energy detection entails comparing the average energy of the received signal to a predetermined threshold, as described by

$$
\Xi (\mathbf {y} _ {\mathrm{w}}) = \frac {1}{n T} \sum_ {i = 1} ^ {n T} (y _ {\mathrm{w}} [ i ]) ^ {2} \underset {<   \mathcal {D} _ {0}} {\geq^ {\mathcal {D} _ {1}}} \tau_ {\mathrm{ED}},\tag{7}
$$

where τ<sub>ED</sub> represents Willie’s detection threshold. In the context of energy detection, the decision criterion is as follows: if the average energy of the received signal denoted as $\Xi ( \mathbf { y } _ { \mathrm { w } } )$ is greater than or equal to the energy detection threshold τ<sub>ED</sub>, the hypothesis $\mathcal { H } _ { 1 }$ that posits the presence of transmission—is accepted as true. Conversely, if $\Xi ( \mathbf { y } _ { \mathrm { w } } )$ is less than $\tau _ { \mathrm { E D } } .$ , the hypothesis ${ \mathcal { H } } _ { 0 } ,$ , which suggests the absence of transmission—is regarded as true.

Thus, Willie’s false alarm and missed detection probabilities can be expressed as

$$
\alpha = \operatorname * {P r} (\Xi (\mathbf {y} _ {\mathrm{w}}) \geq \tau_ {\mathrm{ED}} | \mathcal {H} _ {0})\tag{8}
$$

and

$$
\beta = \operatorname * {P r} (\Xi (\mathbf {y} _ {\mathrm{w}}) <   \tau_ {\mathrm{ED}} | \mathcal {H} _ {1}),\tag{9}
$$

respectively.

Given that the prior probability of Alice’s transmission is 0.5, to minimize the detection error probability, the optimal threshold $\tau _ { \mathrm { E D } } ^ { * }$ satisfies f<sub>Ξ|H</sub> $, ( \tau _ { \mathrm { E D } } ^ { * } ) = f _ { \Xi | \mathcal { H } _ { 1 } } ( \tau _ { \mathrm { E D } } ^ { * } )$ , where $f _ { \Xi | \mathcal { H } _ { 0 } } ( x )$ and $f _ { \Xi | \mathcal { H } _ { 1 } } ( x )$ denote the probability density functions of $\Xi ( \mathbf { y } _ { \mathrm { w } } )$ under hypotheses $\mathcal { H } _ { 0 }$ and $\mathcal { H } _ { 1 }$ , respectively. When $P _ { \mathrm { a } } / \sigma _ { \mathrm { w } } ^ { 2 } \ll 1$ and $n T \gg 1$ , we have the approximation

$$
\tau_ {\mathrm{ED}} ^ {*} \approx \frac {\mu_ {0} + \mu_ {1}}{2},\tag{10}
$$

where $\mu _ { 0 }$ and $\mu _ { 1 }$ denote the average received signal power under $\mathcal { H } _ { 0 }$ and $\mathcal { H } _ { 1 }$ , respectively. The detailed derivation can be found in Appendix A.

## III. ANALYSIS OF SYSTEM COVERTNESS AND RELIABILITY

In this section, we investigate the performance of the proposed ED-RTH system and discuss the impacts of the number of dispersed time slots K transmitted by Alice on Willie’s detection error probability and Bob’s covert throughput, respectively.

## A. Willie’s Detection Error Probability

Willie employs the optimal LRT to detect the received signal. When Alice’s transmitted signals adhere to a Gaussian distribution, specifically $\boldsymbol { x } [ i ] \sim \mathcal { N } ( 0 , P _ { \mathrm { a } } )$ , the received signal at Willie’s end, under the null hypothesis $\mathcal { H } _ { 0 }$ , is represented as $y _ { \mathrm { w } } [ i ] = z _ { \mathrm { w } } [ i ]$ . Consequently, the probability density function (PDF) of Willie’s received signal vector $\mathbf { y } _ { \mathrm { w } }$ can be given by

$$
f _ {0} (\mathbf {y} _ {\mathrm{w}}) = \left(\frac {1}{2 \pi \sigma_ {\mathrm{w}} ^ {2}}\right) ^ {\frac {n T}{2}} \exp \left(- \frac {1}{2 \sigma_ {\mathrm{w}} ^ {2}} \sum_ {t = 1} ^ {T} \sum_ {i = n (t - 1) + 1} ^ {n t} y _ {\mathrm{w}} ^ {2} [ i ]\right).\tag{11}
$$

Under hypothesis $\mathcal { H } _ { 1 }$ , the signal received by Willie is given by $y _ { \mathrm { w } } [ i ] = x [ i ] + z _ { \mathrm { w } } [ i ]$ . Willie knows Alice’s transmit power $P _ { \mathrm { a } }$ but is unaware of the exact set of time slots $\mathbf { t } _ { \mathrm { A } }$ used for transmission. Consequently, he perceives that Alice randomly and uniformly selects K time slots out of the total T for dispersed transmission. There are $C _ { T } ^ { K }$ possible combinations for the selection of these slots, with each combination having an equal probability of occurrence, specifically $1 / C _ { T } ^ { K }$ . In accordance with the law of total probability, the PDF of $\mathbf { y } _ { \mathrm { w } }$ over the T time slots can be formulated as

$$
f _ {1} (\mathbf {y} _ {\mathrm{w}}) = \sum_ {j = 1} ^ {C _ {T} ^ {K}} \frac {1}{C _ {T} ^ {K}} \cdot h _ {j} (\mathbf {y} _ {\mathrm{w}}).\tag{12}
$$

The probability density function for the j-th transmission scheme, denoted as $h _ { j } ( \mathbf { y } _ { \mathrm { w } } )$ , corresponds to the scenario where Alice selects the dispersed time slot set $\mathbf { t } _ { j } .$ Thus, we have

$$
\begin{array}{l} h _ {j} (\mathbf {y} _ {\mathrm{w}}) = \prod_ {t = 1, t \notin \mathbf {t} _ {j}} ^ {T} \frac {1}{(2 \pi \sigma_ {\mathrm{w}} ^ {2}) ^ {n / 2}} \exp \left(- \frac {\sum_ {i = n (t - 1) + 1} ^ {n t} y _ {\mathrm{w}} ^ {2} [ i ]}{2 \sigma_ {\mathrm{w}} ^ {2}}\right) \\ \times \prod_ {t = 1, t \in \mathbf {t} _ {j}} ^ {T} \frac {1}{(2 \pi (\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}})) ^ {n / 2}} \\ \times \exp \left(- \frac {\sum_ {i = n (t - 1) + 1} ^ {n t} y _ {\mathrm{w}} ^ {2} [ i ]}{2 (\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}})}\right). \end{array}\tag{13}
$$

Substituting (13) into (12), we can obtain

$$
\begin{array}{l} f _ {1} (\mathbf {y} _ {\mathrm{w}}) = \frac {1}{(2 \pi \sigma_ {\mathrm{w}} ^ {2}) ^ {\frac {(T - K) n}{2}} \cdot (2 \pi (\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}})) ^ {\frac {n K}{2}} \cdot C _ {T} ^ {K}} \\ \times \sum_ {j = 1} ^ {C _ {T} ^ {K}} \exp \left(- \frac {\sum_ {t \in \mathbf {t} _ {j}} \sum_ {i = n (t - 1) + 1} ^ {n t} y _ {\mathrm{w}} ^ {2} [ i ]}{2 (\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}})} - \frac {\sum_ {t = 1 ,   t \notin \mathbf {t} _ {j}} \sum_ {i = n (t - 1) + 1} ^ {n t} y _ {\mathrm{w}} ^ {2} [ i ]}{2 \sigma_ {\mathrm{w}} ^ {2}}\right). \end{array}\tag{14}
$$

Then, substituting (11) and (14) into (3), the LRT statistic can be given as

$$
\begin{array}{l} \Lambda (\mathbf {y} _ {\mathrm{w}}) = \frac {1}{C _ {T} ^ {K}} \cdot \left(\frac {\sigma_ {\mathrm{w}} ^ {2}}{\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}}}\right) ^ {\frac {n K}{2}} \\ \times \sum_ {j = 1} ^ {C _ {T} ^ {K}} \underbrace {\exp \left(\frac {P _ {\mathrm{a}} \sum_ {i \in \mathbf {t} _ {j}} \sum_ {i = n (t - 1) + 1} ^ {n t} y _ {\mathrm{w}} ^ {2} [ i ]}{2 \sigma_ {\mathrm{w}} ^ {2} (\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}})}\right)} _ {I _ {j}}. \end{array}\tag{15}
$$

In the case where $K = T$ , indicating that Alice utilizes all T time slots for information transmission, the LRT statistic is expressed as

$$
\Lambda (\mathbf {y} _ {\mathrm{w}}) = \left(\frac {\sigma_ {\mathrm{w}} ^ {2}}{\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}}}\right) ^ {\frac {n T}{2}} \exp \left(\frac {P _ {\mathrm{a}}}{2 \sigma_ {\mathrm{w}} ^ {2} \left(\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}}\right)} \sum_ {i = 1} ^ {n T} \left(y _ {\mathrm{w}} [ i ]\right) ^ {2}\right).\tag{16}
$$

Substituting (16) into (4), it can be transformed into

$$
\frac {1}{n T} \sum_ {i = 1} ^ {n T} (y _ {\mathrm{w}} [ i ]) ^ {2} \overset {\geq \mathcal {D} _ {1}} {<  } _ {\mathcal {D} _ {0}} \frac {\sigma_ {\mathrm{w}} ^ {2} (\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}})}{P _ {\mathrm{a}}} \ln \left(\frac {\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}}}{\sigma_ {\mathrm{w}} ^ {2}}\right).\tag{17}
$$

Upon examining (17), it becomes clear that when $K = T$ LRT is equivalent to energy detection. Thus, energy detection yields optimal detection performance in this case, which will be confirmed by the simulation results provided in Section IV.

In the scenario where $K < T$ , analysis of (15) reveals that the distribution of the LRT statistic $\Lambda ( \mathbf { y } _ { \mathrm { w } } )$ is excessively complex. Moreover, due to the potential overlap in time slots across Alice’s various time selection schemes $( \mathrm { i . e . , } \ \big | \mathbf { t } _ { j _ { 1 } } \cap \mathbf { t } _ { j _ { 2 } }$ <sup>ˇ</sup><sub>ˇ</sub>may not be zero $\mathrm { f o r } j _ { 1 } \ \ne \ j _ { 2 } )$ , the terms $I _ { j } ( \mathrm { f o r } j = 1 , \cdot \cdot . . , C _ { T } ^ { K } )$ are not independent. This interdependence complicates the analysis and derivation of the false alarm probability α and the miss detection probability $\beta .$ In order to facilitate the analysis of Willie’s detection performance, we employ KL divergence to evaluate the lower bound of Willie’s detection error probability. We define the total detection error probability as $\xi ,$ , which is the sum of the false alarm probability α and the miss detection probability $\beta \ ( \xi = \alpha + \beta )$ . According to Ref. [20], for the optimal detection, we have

$$
\xi = 1 - \mathcal {V} _ {T} (\mathbb {P} _ {0} | | \mathbb {P} _ {1}),\tag{18}
$$

where $\mathcal { V } _ { T } ( \mathbb { P } _ { 0 } \Vert \mathbb { P } _ { 1 } )$ represents the total variation distance between the probability distributions $\mathbb { P } _ { 0 }$ and $\mathbb { P } _ { 1 }$

According to Pinsker’s inequality, we can obtain

$$
\mathcal {V} _ {T} (\mathbb {P} _ {0} | | \mathbb {P} _ {1}) \leq \sqrt {\frac {1}{2} \mathcal {D} (\mathbb {P} _ {0} | | \mathbb {P} _ {1})},\tag{19}
$$

where $\mathcal { D } ( \mathbb { P } _ { 0 } | \| \mathbb { P } _ { 1 } )$ represents the KL divergence between the two probability distributions $\mathbb { P } _ { 0 }$ and $\mathbb { P } _ { 1 }$ .

Therefore, we can get

$$
\xi \geq 1 - \sqrt {\frac {1}{2} \mathcal {D} (\mathbb {P} _ {0} | | \mathbb {P} _ {1})}.\tag{20}
$$

According to the definition of KL divergence, we have

$$
\begin{array}{l} \mathcal {D} (\mathbb {P} _ {0} | | \mathbb {P} _ {1}) = \int_ {- \infty} ^ {+ \infty} f _ {0} (\mathbf {y} _ {\mathrm{w}}) \ln \frac {f _ {0} (\mathbf {y} _ {\mathrm{w}})}{f _ {1} (\mathbf {y} _ {\mathrm{w}})} d \mathbf {y} _ {\mathrm{w}} \\ = \ln \left(C _ {T} ^ {K}\right) + \frac {n K}{2} \ln \left(\frac {\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}}}{\sigma_ {\mathrm{w}} ^ {2}}\right) - \int_ {- \infty} ^ {+ \infty} f _ {0} (\mathbf {y} _ {\mathrm{w}}) \\ \times \ln \left(\sum_ {j = 1} ^ {C _ {T} ^ {K}} \exp \left(\frac {P _ {\mathrm{a}} \sum_ {t \in \mathfrak {t} _ {j}} \sum_ {i = n (t - 1) + 1} ^ {n t} y _ {\mathrm{w}} ^ {2} [ i ]}{2 \sigma_ {\mathrm{w}} ^ {2} (\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}})}\right)\right) d \mathbf {y} _ {\mathrm{w}}. \end{array}\tag{21}
$$

As we can see, in covert communication analysis, the KL divergence serves not only as a mathematical measure between two probability distributions but also as a fundamental indicator of detectability. Specifically, the KL divergence between the received-signal distributions under $\mathcal { H } _ { 0 }$ and $\mathcal { H } _ { 1 }$ quantifies how distinguishable these two hypotheses are to the warden (Willie). A smaller KL divergence implies that the two distributions are more similar, leading to a higher detection uncertainty and thus stronger covertness. Conversely, a larger KL divergence indicates that the presence of transmission leaves a more detectable statistical footprint. Therefore, analyzing and minimizing the KL divergence directly correspond to enhancing the system’s covertness.

Next, we will turn our attention to examining the variation of KL divergence with the number of dispersed slots K. Let the KL divergence be defined as

$$
\mathcal {D} (K) = \ln \left(C _ {T} ^ {K}\right) + \frac {n K}{2} \ln \left(\frac {\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}}}{\sigma_ {\mathrm{w}} ^ {2}}\right) - \Gamma (K),\tag{22}
$$

where

$$
\begin{array}{l} \Gamma (K) = \int_ {- \infty} ^ {+ \infty} f _ {0} (\mathbf {y} _ {\mathrm{w}}) \\ \times \ln \left(\sum_ {j = 1} ^ {C _ {T} ^ {K}} \exp \left(\frac {P _ {\mathrm{a}} \sum_ {t \in \mathbf {t} _ {j}} \sum_ {i = n (t - 1) + 1} ^ {n t} y _ {\mathrm{w}} ^ {2} [ i ]}{2 \sigma_ {\mathrm{w}} ^ {2} (\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}})}\right)\right) d \mathbf {y} _ {\mathrm{w}}. \end{array}\tag{23}
$$

Obviously, Γ(K) can be expressed as

$$
\Gamma (K) = \mathbb {E} \left[ \ln \left(\sum_ {j = 1} ^ {C _ {T} ^ {K}} \exp \left(\frac {P _ {\mathrm{a}} \sum_ {t \in \mathbf {t} _ {j}} \sum_ {i = n (t - 1) + 1} ^ {n t} y _ {\mathrm{w}} ^ {2} [ i ]}{2 \sigma_ {\mathrm{w}} ^ {2} (\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}})}\right)\right) \right].\tag{24}
$$

In (21), the first two terms are related to system parameters and can be directly calculated. The third term Γ(K) is dificult to solve directly, and its numerical solution can be obtained by Monte Carlo simulation to obtain the sample mean. Based on the above numerical analysis, we will further verify the variation of the KL divergence $\mathcal { D } ( \mathbb { P } _ { 0 } | \| \mathbb { P } _ { 1 } )$ with K through behavioral-level simulations later.

As shown in Appendix B, through approximate derivation, when $T \to \infty$ we can obtain

$$
\mathcal {D} (K) \approx \frac {n \gamma_ {\mathrm{w}} ^ {* 2}}{4 T} \exp \left(- \frac {n \gamma_ {\mathrm{w}} ^ {*}}{2} \left(1 - \frac {1}{K}\right)\right),\tag{25}
$$

where $\gamma _ { \mathrm { w } } ^ { \ast } = P / \left( n \sigma _ { \mathrm { w } } ^ { 2 } \right)$

Next, we resort to the KL divergence to analyze the variation trend of the lower bound on Willie’s detection error probability with respect to K. According to (20), we define the lower bound of the detection error probability as

$$
\begin{array}{l} \xi_ {L B} (K) = 1 - \sqrt {\frac {\mathcal {D} (K)}{2}} \\ \approx 1 - A \exp \left(- B \left(1 - \frac {1}{K}\right)\right), \end{array}\tag{26}
$$

where $\begin{array} { r } { A = \ \sqrt { \frac { n \gamma _ { \mathrm { w } } ^ { * } { } ^ { 2 } } { 8 T } } } \end{array}$ and $\begin{array} { r } { B = \frac { n \gamma _ { \mathrm { w } } ^ { \ast } } { 4 } } \end{array}$

Clearly, $\xi _ { L B } ( K )$ increases monotonically with K, which implies that Willie’s probability of correctly distinguishing between $\mathcal { H } _ { 0 }$ and $\mathcal { H } _ { 1 }$ decreases, and thus the covertness improves as K increases. When $K = 1 , \xi _ { L B }$ attains its minimum value

$$
\xi_ {L B} (1) \approx 1 - \sqrt {\frac {n \gamma_ {\mathrm{w}} ^ {* 2}}{8 T}},\tag{27}
$$

whereas when $K = T , \xi _ { L B }$ reaches its maximum value

$$
\xi_ {L B} (T) \approx 1 - \sqrt {\frac {n \gamma_ {\mathrm{w}} ^ {* 2}}{8 T}} \exp \left(- \frac {n \gamma_ {\mathrm{w}} ^ {*}}{4} \left(1 - \frac {1}{T}\right)\right).\tag{28}
$$

The increment between two adjacent points is approximately

$$
\Delta \xi_ {K} = \xi_ {L B} (K + 1) - \xi_ {L B} (K)
$$

$$
\begin{array}{l} \approx A \exp \left(- B \left(1 - \frac {1}{K}\right)\right) \left[ 1 - \exp \left(- \frac {B}{K (K + 1)}\right) \right] \\ \approx A \exp \left(- B \left(1 - \frac {1}{K}\right)\right) \frac {B}{K (K + 1)}. \end{array} \tag {（}\tag{29}
$$

Clearly, the exponential term exp $\scriptstyle \left( - B \left( 1 - { \frac { 1 } { K } } \right) \right)$ varies slowly, and the variation of $\Delta \xi _ { K }$ is mainly determined by $\frac { 1 } { K ( K + 1 ) }$ , which means

$$
\Delta \xi_ {K} \propto \frac {1}{K (K + 1)} \sim \frac {1}{K ^ {2}}.\tag{30}
$$

Consequently, as K increases, the increment in the lower bound of Willie’s detection error probability decreases continuously, and the change in covertness tends to level of. Therefore, increasing K yields a higher covertness gain when K is small.

## B. Bob’s Covert Throughput

Covert throughput is a key metric for measuring the efectiveness of covert communication systems, defined as the amount of information that the system can correctly transmit under the constraint of covertness [34]. It can be expressed as follows:

$$
\eta = N R (1 - \delta).\tag{31}
$$

Here, N denote the total code length of a coding block, and the coding rate is defined as $R = D / N$ , where D represents the number of information bits carried by a coding block. The decoding error probability δ at Bob’s receiver, as stated in Ref. [35], can be expressed as:

$$
\delta \approx Q \left(\frac {\sqrt {N} (1 + \gamma_ {\mathrm{b}}) (\ln (1 + \gamma_ {\mathrm{b}}) - R \ln 2)}{\sqrt {2 \gamma_ {\mathrm{b}} (\gamma_ {\mathrm{b}} + 2)}}\right),\tag{32}
$$

where $Q ( x )$ denotes the right-tail function of the standard normal distribution, and $\gamma _ { \mathrm { b } } = P _ { \mathrm { a } } / \sigma _ { \mathrm { b } } ^ { 2 }$ represents the SNR of the efective signal received by Bob from Alice. Here $\sigma _ { \mathrm { b } } ^ { 2 }$ denotes the power of the AWGN at Bob’s receiver.

It is assumed that Bob decodes after coherently combining the received data over K time slots. In practice, Bob may face a certain loss in the combining Signal-to-Noise Ratio (SNR) due to synchronization errors. However, here we assume perfect combining to focus on the achievable upper bound of the throughput. The SNR for each time slot $\begin{array} { r } { \gamma _ { \mathrm { b } } = \frac { P _ { \mathrm { a } } } { \sigma _ { \mathrm { b } } ^ { 2 } } } \end{array}$ , while the SNR after coherent combination is given by $\begin{array} { r } { \gamma _ { \mathrm { b - c } } = \frac { P _ { \mathrm { a } } K ^ { 2 } } { \sigma _ { \mathrm { b } } ^ { 2 } K } = \frac { P _ { \mathrm { a } } ^ { * } } { \sigma _ { \mathrm { b } } ^ { 2 } } } \end{array}$ The code length $N = n$ and the coding rate is R. Therefore, the throughput can be expressed as:

$$
\eta = n R \left[ 1 - Q \left(\frac {\sqrt {n} \left(1 + \frac {P _ {\mathrm{a}} ^ {*}}{\sigma_ {\mathrm{b}} ^ {2}}\right) \left(\ln \left(1 + \frac {P _ {\mathrm{a}} ^ {*}}{\sigma_ {\mathrm{b}} ^ {2}}\right) - R \ln 2\right)}{\sqrt {2 \cdot \frac {P _ {\mathrm{a}} ^ {*}}{\sigma_ {\mathrm{b}} ^ {2}} \left(\frac {P _ {\mathrm{a}} ^ {*}}{\sigma_ {\mathrm{b}} ^ {2}} + 2\right)}}\right) \right].\tag{33}
$$

It is evident from (33) that the covert throughput is independent of the value of K when $P _ { \mathrm { ~ a ~ } } ^ { * }$ is fixed; thus, the covert throughput η remains constant. However, as revealed by the following simulation analysis, an increase in K enhances the covertness of the system. Consequently, under the same covert constraint, Alice can transmit with a higher power.

Therefore, assuming the covert constraint remains unchanged, the maximum achievable covert throughput of the system also increases with the increase in K. It is worth noting that an increase in K will leads to a lower SNR, we assume that the legitimate receiver can perform optimal combining across them, so that he total received energy and SNR of the combined signal remains unchanged. But it may impose a higher complexity on Bob’s coherent receiver.

## C. Discussion on Fading Channels

To investigate the generalizability of the proposed ED-RTH scheme to practical wireless environments, we provide a qualitative analysis regarding the impact of fading channels. First, fading introduces channel uncertainty, compelling Willie to rely on sub-optimal energy detection due to the lack of instantaneous Channel State Information (CSI). The resulting fluctuations in received power further degrade Willie’s detection performance, consequently enhancing covertness. Second, unlike conventional schemes that concentrate energy within a single time slot, the ED-RTH scheme disperses the total energy across K time slots. Provided that the hopping interval exceeds the channel coherence time, this dispersion efectively mitigates the impact of deep fading and enhances system robustness, albeit at the expense of increased channel estimation complexity at the receiver.

## IV. SIMULATION RESULTS

In this section, we first introduce a behavioral simulation method. Subsequently, we employ this method along with the previously established KL divergence expression to simulate and analyze the covertness of the ED-RTH system. Finally, the ED-RTH scheme is compared with the RSS, single-slot selection, and traditional certain time schemes to demonstrate the advantages of the ED-RTH scheme in terms of covertness.

## A. The Behavioral Simulation of the Covert Communication System

A behavioral simulation method is designed to simulate the complete process of Alice transmitting and Willie intercepting signals. This method evaluates and signifies the system’s level of covertness by analyzing Willie’s detection outcomes. The detailed procedure is depicted in Fig. 3.

(1) In the initial stage, Alice generates ED-RTH covert communication signals. The total duration of the communication is divided into T time slots, each containing n points, resulting in a total data length of nT. It is assumed that the prior probability of Alice initiating transmission is equal to one half, that is to say, $\textstyle \rho = { \frac { 1 } { 2 } }$ Consequently, there is a 1/2 probability that the transmitted signal across these nT points will consist entirely of zeros. Similarly, there is a 1/2 probability that K segments of covert signals, with a cumulative length of $n K ,$ , will be randomly selected from the T time slots. These selected segments will exhibit an average power of $P _ { \mathrm { a } } ,$ whereas the remaining (T − K) time slots will remain untransmitted and will hold a value of zero.

(2) Noise is introduced to the signal transmitted by Alice. A Gaussian white noise vector of length nT is generated, with each element independently drawn from the normal distribution $\mathcal { N } ( 0 , \sigma _ { \mathrm { w } } ^ { 2 } )$ . This noise vector is then added to the covert communication signal vector that was produced in step (1).

(3) Willie employs hypothesis testing on the received data, which has a length of $n T ,$ to ascertain whether Alice is in the process of transmitting. Given his awareness of the distributional characteristics of Alice’s signals, he can employ optimal LRT. Willie inputs the received signal into the likelihood ratio expression and compares the result with a previously trained optimal threshold. If the likelihood ratio surpasses this threshold, it can be concluded that Alice is indeed transmitting, which corresponds to the hypothesis $\mathcal { H } _ { 1 }$ . Conversely, if the likelihood ratio falls below the threshold, it is inferred that Alice is not transmitting, aligning with the hypothesis $\mathcal { H } _ { 0 }$

(4) The steps from (1) to (3) are repeated numerous times to facilitate a comparison between Willie’s decisions and Alice’s actual transmission states. Subsequently, the false alarm probability and the miss detection probability are recorded. These statistics are then utilized to calculate Willie’s detection error probability.

In the subsequent simulations, the noise power at Willie and Bob’s receiver are fixed at $\sigma _ { \mathrm { { w } } } ^ { 2 } ~ = ~ \sigma _ { \mathrm { { b } } } ^ { 2 } ~ = ~ 1$ . According to the AES-128 standard [36], which is widely employed in security protocols such as TLS, IPsec and WPA2, the number of channel uses per time slot is set to $n = 1 2 8$ . In order to balance analytical clarity and simulation complexity, we let T = 12 in most of the cases.

## B. Performance of the ED-RTH Scheme

Fig. 4 illustrates the variation of the KL divergence with respect to the number of dispersed transmission slots K used by Alice. As observed, when the total transmit power P and the total number of slots T are fixed, dispersing the transmission over multiple slots $( K > 1 )$ leads to a noticeable reduction in the KL divergence compared with the non-dispersed case $( K = 1 )$ , demonstrating that the system’s covertness improves as K increases. However, as K continues to grow, the decreasing trend of the KL divergence gradually slows down, and once K becomes suficiently large, further increasing the dispersion yields only marginal benefits. In this regime, enhancing the system’s covertness can only be achieved by increasing the total number of slots T or reducing the total transmit power $P .$

Fig. 5 presents the results of the level-based likelihood ratio test simulation, together with the lower bound of Willie’s detection error probability obtained from the KL divergence. It can be observed that as Alice increases the number of dispersed transmission slots K, both the likelihood ratio test results and the KL-divergence-based lower bound of Willie’s detection error probability consistently increase and eventually approach a steady value. Moreover, the two curves exhibit almost identical trends, which further validates the reliability of the KL-divergence-based analysis. In addition, the lower bound derived from the KL divergence provides a more stringent constraint for system design, ensuring that the required covertness level is satisfied. Meanwhile, Fig. 5 also shows that under the current simulation parameters, the detection error probability increases significantly when K grows from 1 to 3. However, as K continues to increase, the detection error probability gradually saturates, and the additional covertness gained from further dispersion becomes marginal, while the complexity of the legitimate receiver increases substantially. This observation is consistent with the trend analyzed in Section III.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Behavioral simulation process
Input:
The average transmission power of Alice  $P_{a}$ ; the noise power at Willie's receiver  $\sigma_{w}^{2}$ ; the total number of time slots T; the number of dispersed slots K; the channel uses number of per slot n; the amount of Monte Carlo simulations' I

Output:
Willie's detection error probability  $\xi$ 

1. for i = 1 to I do
2.    Tx_en(i) = binornd(1,1/2,1); (decide whether to transmit)
3.    Patten = sort(randperm(T, K)); (select K slots from T time slots as the time-hopping pattern)
4.    Tx(Patten, :) = reshape(Tx_en(i)*sqrt(Pa)*randn(1,n*K),K,[]) 
5.    Noise =  $\sigma_{w}$  * randn(size(Tx)); (generate the noise signal for Willie's receiver)
6.    Rx = Tx + Noise;
7.    calculate the statistic LRT based on the received signal Rx;
8.    decision(i) = (LRT &gt; 1) ? 1 : 0;
9.  $\xi$  = sum(Alice_en != decision) / I;
</div>

Fig. 3. The process of behavioral simulation.

![](images/d2dc9d57777e7c7e051eb3078eee4c4933cef418dbc13375a590c849f15ed7e1.jpg)  
Fig. 4. KL divergence D(P ||P ) versus the number of dispersed slots K for diferent T and diferent $P _ { \mathrm { ~ a ~ } } { } ^ { * }$

![](images/c68c89c1623cdce677ba70706927fbc0db9d96797ac57083181a516a865e3f41.jpg)  
Fig. 5. Detection error probability of Willie ξ versus the number of dispersed slots K for diferent ${ \dot { P _ { \mathrm { a } } } } ^ { * } ,$ where $T \ = \ 1 2 ,$ , to compare the result of LRT behavioral simulation and the lower bound calculated by KL divergence.

![](images/56d2b297ee83b2df5d02a0ec8ac774647ba66576ce08259505b2eeca43cb1baf.jpg)  
Fig. 6. Comparing the total transmit power of Alice for deferent K, versus the constraint factor , where T = 12.

Fig. 6 illustrates the relationship between Alice’s maximum total transmit power, P, and the covertness constraint coeficient, , within the constraint that $\xi \ge 1 - \epsilon$ . The three blue curves delineate the power constraints imposed on Alice’s total transmit power, $P ,$ as derived from the KL divergence. In contrast, the three red curves illustrate the constraints resulting from the LRT simulations, which pertain to Willie’s detection error probability. It is evident that, under identical conditions, the KL divergence imposes more stringent constraints on Alice’s transmit power than the LRT approach. Furthermore, as the covertness constraint coeficient is incremented, the permissible maximum transmit power for Alice also escalates. This is due to the progressive relaxation of system covertness requirements, which in turn permits Alice to employ higher power levels for signal transmission.

As derived from behavioral simulation outcomes, a comparative analysis presented in Fig. 7 reveals the variation in detection error probability with the number of dispersed slots, K, for both energy detection and LRT methods. The figure demonstrates that the performance of energy detection is mainly independent of the number of dispersed slots, K. In the initial stage, when the value of K is relatively low, the LRT exhibits a markedly superior performance compared to energy detection. However, as the number of dispersed slots, K, increases, the performance gap between the two detection techniques gradually narrows. This trend can be attributed to the fact that when Alice has a fixed total transmit power and a small K, energy is concentrated within a subset of slots, thereby enhancing the discriminability of likelihood functions under diferent hypotheses for LRT. In contrast, energy detection evaluates the total energy across all T slots, irrespective of K. The figure further illustrates that when K equals T, the detection error probabilities for LRT and energy detection converge entirely, substantiating the discussion presented in Section IV. This section posits that LRT and energy detection are equivalent when Alice employs all T slots for transmission.

![](images/2ba07538b71d8bf4b5dc49c914289a1085f36bf7a2df8104562348b2c2fc99f2.jpg)  
Fig. 7. Comparing the lower-bound of error probability of Willie ξ for diferent kinds of detection method, versus the number of dispersed slots K, where $T = 1 2$

![](images/d66305f8574e5301ab98267990281189d9ed731536b950e6e3f683fede549d78.jpg)  
Fig. 8. Detection error probability ξ versus the number of channel uses per slot n for diferent total transmit power P, where $T = 1 2$ and $K = 4 .$

Fig. 8 illustrates the detection error probability as a function of the number of symbols per slot, n, under various total energy levels, P. It can be observed that, for all energy levels, both the simulation curve based on the LRT and the theoretical lower bound derived from the KL divergence increase monotonically with n. This occurs because, under a fixed total energy constraint, increasing n reduces the average transmit power per symbol, thus weakening the eavesdropper’s ability to distinguish between “transmission” and “no transmission.” Concurrently, the increase in n leads to a longer total time duration, enhancing the time uncertainty and further improving the system’s covertness.

![](images/9985d34d7c52d78890edd76c690792f696e630c98fe0396d3db6265a28af1567.jpg)

![](images/2fe5f749eb3cf4b7d16b0004763a5af0e03d33a98c128976a410978cf017b873.jpg)  
Fig. 9. (a) Maximum covert throughput η versus the number of dispersed slots K for diferent , where T = 12, R = 1/32. (b) Maximum covert throughput η versus  for diferent coding rate R, where T = 12, K = 4.

Under the conditions of fixed covertness constraint coeficient  and the number of efective information bits D, we simulated the maximum covert throughput of the ED-RTH scheme as a function of the number of dispersed time slots K, as shown in Fig. 9(a). It can be seen that the maximum covert throughput of the system increases with K, which is primarily due to the enhancement of system covertness as the number of dispersed time slots increases, allowing Alice to transmit at a higher maximum power under the same covertness constraint. On the other hand, the covert throughput is closely related to the coding rate. With $T = 1 2$ and $K = 4$ fixed, we simulated the relationship between covert throughput and covertness constraints at diferent coding rates, as shown in Fig. 9(b). It can be observed that as the covertness constraints are relaxed, the covert throughput for all coding rates increases and eventually approaches an upper bound. The higher the coding rate, the more efective information bits can be transmitted, thus raising this upper bound. However, at lower SNR, high coding rates tend to exhibit poorer decoding performance, which adversely afects covert throughput. Therefore, as seen in Fig. 9(b), when the covertness constraints are stringent, the covert throughput at lower coding rates can actually be higher. In practical system design, it is often necessary to select an appropriate coding rate based on the required covertness constraints.

## C. The Comparison Among ED-RTH and Existing Schemes

In Fig. 10, behavioral simulations based on LRT are used to compare three schemes: traditional certain time scheme, the single-slot selection schemes [28], and the proposed ED-RTH scheme. The traditional certain time scheme corresponds to the specific case of $T = 1$ and $K = 1$ in the ED-RTH scheme in this study. In contrast, the single-slot selection scheme is represented by the case where $T \ > \ 1$ and $K \ = \ 1$ . The results clearly indicate that, under the same total transmission power $P ,$ the detection error probability in the two schemes with time uncertainty is significantly higher than that in the traditional certain time scheme. Furthermore, the ED-RTH scheme demonstrates a superior covert advantage compared to the single-slot selection scheme, particularly as the total transmission power from Alice increases. This phenomenon can be explained as follows: When Alice’s total transmission power is concentrated within a single time slot, Willie can more efectively distinguish the received signal from pure noise. In contrast, by dispersing the signal power across multiple time slots, the diference between the signal received by Willie and the background noise is efectively diminished, enhancing covertness of the system.

![](images/258542c3abcf05dfaaf86a364a9ff02b279055c6f673b99efaef32ff64647ab0.jpg)  
Fig. 10. Comparing the detection error probability ξ versus the the total transmit power of Alice $P ,$ for diferent schemes. $( \dot { T } = 1 2 $ in ED-RTH and the single-slot selection schemes).

![](images/e77bf5a3857aa43741b9228202c74ede089eecc7a9a4f70e62c9cb3ceeb9f02e.jpg)  
Fig. 11. Maximum covert throughput η versus the number of dispersed slots K for diferent $\epsilon ,$ where $T = 1 \bar { 2 } , \stackrel { \cdot } { D } = 4 ,$ to compare the result of repeated transmission strategy and the variable code length strategy.

![](images/84f902f22624993f05e52ab4d0c0258ad2706572654b2b538c9a7fccdb36eae1.jpg)  
Fig. 12. Comparing the detection error probability ξ versus the total channel uses of Alice, for diferent schemes, where $T \ = \ 1 2$ and $P _ { \mathrm { a } } ^ { \mathrm { ~ * ~ } } = \ 0 . 2$ for ED-RTH.

With the number of efective information bits fixed, we compare the maximum covert throughput of the traditional certain time scheme, single-slot selection scheme, and the proposed ED-RTH scheme as a function of the covertness constraint . It can be seen in Fig. 11 that the covert throughput of the proposed ED-RTH and single-slot selection schemes significantly outperforms the traditional certain time scheme. This improvement is primarily due to the introduction of time uncertainty, which relaxes the constraints on Alice’s transmission power imposed by the covertness requirements, allowing for greater transmission power and thus higher throughput. Meanwhile, the ED-RTH scheme allows for greater transmit power compared to the single-slot selection scheme, thus further enhancing the covert throughput.

In Fig. 12, to clearly illustrate the advantage of random slot hopping in ED-RTH, we compare ED-RTH with the RSS scheme under the condition that both schemes have the same duration of transmit window and use the same total number of channel uses. We also include a conventional time-deterministic scheme as a reference. We ensure that the total time duration of ED-RTH and RSS are identical, and then simulate the detection error probability versus the actual total number of channel uses. For the sake of simplicity, the duration of the transmission window is set to 1536 symbol periods for both schemes. In the ED-RTH scheme, we set $T \ = \ 1 2$ . By appropriately adjusting the parameter K in the ED-RTH scheme and $n ^ { \prime }$ in the RSS scheme, we can ensure that both schemes maintain the same total number of channel uses.

To facilitate understanding, we consider a set of comparative data points in Fig. 12 as an example. As indicated by the labels in the figure, in the ED-RTH scheme with $K = 3$ and each slot containing $n = 1 2 8$ consecutive channel uses, the total number of channel uses is given by $n K = 3 8 4 .$ In the corresponding RSS scheme, the total number of slots $T ^ { \prime } = 4 ,$ each containing $n ^ { \prime } = 3 8 4$ consecutive channel uses. The RSS scheme randomly selects one slot for transmission, resulting in the same total channel uses, i.e., $n ^ { \prime } = n K$

It can be observed that the detection error probability for Willie increases with the total number of channel uses across all three schemes. This occurs because, under constant total transmit power, the energy becomes more dispersed as the number of channel uses increases, resulting in enhanced covertness. Ultimately, when the number of channel covertness fills the entire duration, all three schemes revert to the traditional certain time model, at which point the system’s covertness reaches its peak. However, overly dispersed signal energy can often make it more dificult for legitimate users to receive the signals. In practice, both the ED-RTH and RSS schemes can continue to increase total duration to gain time uncertainty without increasing the total number of channel usages. Therefore, we focus on the results in the left half of the graph, which have more practical significance. It is evident that, under the same conditions of energy dispersion (the same number of total channel uses), the introduction of time uncertainty allows the ED-RTH and RSS schemes to achieve significantly greater covertness compared to the traditional certain time scheme. Furthermore, when $K \ > \ 1$ in the ED-RTH scheme, the more flexible hopping time slots yield greater time uncertainty compared to the RSS scheme, which only has a single continuous time slot, thus providing enhanced covertness.

## V. CONCLUSION

In this paper, we propose an ED-RTH covert communication scheme. Using KL divergence, we establish the lower bound for detection error probability and link it to the number of dispersed slots, K. The results indicate that as K increases from 1 to T, Willie’s detection error probability initially improves substantially with the increase of K. However, as K continues to grow, this improvement rapidly diminishes. The additional covertness gained from overly dispersing the transmission becomes very limited, while it significantly increases the complexity of the legitimate receiving system. The covert throughput of the ED-RTH system was simulated and analyzed, which also increased with the increase of $K .$ We also compare energy detection and LRT detection through behavioral simulations. The findings reveal that K does not impact the performance of energy detection. For small $K ,$ LRT outperforms energy detection, but as K increases, the performance gap narrows until $K = T$ , where both methods align. Finally, our comparison shows that the ED-RTH scheme achieves superior covertness compared to existing time uncertainty schemes.

Although the proposed ED-RTH scheme improves covertness in the AWGN channel by dispersing energy and adding time uncertainty, its performance in more realistic fading environments remains unclear. Future work will extend the analysis to general fading channels and investigate robust multi-slot combining algorithms to address the low per-slot SNR challenge, aiming to strike an optimal balance between covertness, reliability, and computational complexity.

## APPENDIX A

When $\mathcal { H } _ { 0 }$ holds, all nT observations follow the distribution $\mathcal { N } ( 0 , \sigma _ { \mathrm { w } } ^ { 2 } )$ . Therefore, the average energy of all received samples follows the distribution:

$$
\Xi (\mathbf {y} _ {\mathrm{w}}) \mid_ {\mathcal {H} _ {0}} \sim \Gamma \left(\frac {n T}{2}, 2 \sigma_ {\mathrm{w}} ^ {2}\right).\tag{34}
$$

Let its probability density function be denoted by $f _ { \Xi | \mathcal { H } _ { 0 } } ( x )$ and its cumulative distribution function by $F _ { \Xi | \mathcal { H } _ { 0 } } ( x )$ . When the decision threshold is set to $\tau ,$ the false-alarm probability can be expressed as $\alpha ( \tau ) = 1 - F _ { \Xi | \mathcal { H } _ { 0 } } ( \tau )$

When $\mathcal { H } _ { 1 }$ holds, the nK observations follow the distribution $\mathcal { N } ( 0 , , P _ { \mathrm { a } } + \sigma _ { \mathrm { w } } ^ { 2 } )$ , while the remaining $n ( T - K )$ observations follow $\mathcal { N } ( 0 , , \sigma _ { \mathrm { w } } ^ { 2 } )$ . Therefore, the average energy of all received samples follows the distribution:

$$
\Xi (\mathbf {y} _ {\mathrm{w}}) \mid_ {\mathcal {H} _ {1}} \sim \Gamma \left(\frac {n (T - K)}{2}, 2 \sigma_ {\mathrm{w}} ^ {2}\right) + \Gamma \left(\frac {n K}{2}, 2 (P _ {\mathrm{a}} + \sigma_ {\mathrm{w}} ^ {2})\right).\tag{35}
$$

Let its probability density function be denoted by $f _ { \Xi | \mathcal { H } _ { 1 } } ( x )$ and its cumulative distribution function by $F _ { \Xi | \mathcal { H } _ { 1 } } ( x )$ . When the decision threshold is set to $\tau ,$ the miss-detection probability can be expressed as $\beta ( \tau ) = F _ { \Xi | \mathcal { H } _ { 1 } } ( \tau )$

The total detection error probability is given by

$$
\begin{array}{c} \xi (\tau) = \alpha (\tau) + \beta (\tau) \\ = 1 - F _ {\Xi | \mathcal {H} _ {0}} (\tau) + F _ {\Xi | \mathcal {H} _ {1}} (\tau), \end{array}\tag{36}
$$

For the threshold $\tau _ { \mathrm { E D } } ^ { * }$ that minimizes the detection error probability $\xi ( \tau )$ , we have

$$
\frac {d \xi (\tau)}{\tau} = 0,\tag{37}
$$

which yields

$$
f _ {\Xi | \mathcal {H} _ {0}} (\tau_ {\mathrm{ED}} ^ {*}) = f _ {\Xi | \mathcal {H} _ {1}} (\tau_ {\mathrm{ED}} ^ {*}).\tag{38}
$$

Given the two distributions, $\tau _ { \mathrm { E D } } ^ { * }$ can be obtained numerically via a one-dimensional search.

However, note that $\begin{array} { r } { \Xi ( \mathbf { y } _ { \mathrm { w } } ) ~ = ~ \frac { 1 } { n T } \sum _ { i = 1 } ^ { n T } \left( y _ { \mathrm { w } } [ i ] \right) ^ { 2 } } \end{array}$ is the sum of nT random variables. Hence, under the general condition $n T \gg 1$ , by the central limit theorem (CLT), the distribution of $\Xi ( \mathbf { y } _ { \mathrm { w } } ) \mid _ { \mathcal { H } _ { 0 } }$ can be approximated as $\mathcal { N } ( \mu _ { 0 } , \sigma _ { 0 } ^ { 2 } )$ , and that $\mathrm { o f } \Xi (  { \mathbf { y } _ { \mathrm { w } } } ) \big | _ { \mathcal { H } _ { 1 } }$ can be approximated $\mathrm { a s } \mathcal { N } ( \mu _ { 1 } , \sigma _ { 1 } ^ { 2 } )$ , where

$$
\mu_ {0} = \sigma_ {\mathrm{w}} ^ {2}, \quad \sigma_ {0} ^ {2} = \frac {2 \sigma_ {\mathrm{w}} ^ {4}}{n T},\tag{39}
$$

$$
\mu_ {1} = \frac {n (T - K) \sigma_ {\mathrm{w}} ^ {2} + K (\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}})}{n T},\tag{40}
$$

$$
\sigma_ {1} ^ {2} = \frac {2 \left(n (T - K) \sigma_ {\mathrm{w}} ^ {4} + n K (\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}}) ^ {2}\right)}{(n T) ^ {2}}.\tag{41}
$$

Since covert communication typically operates in the regime $P _ { \mathrm { a } } / \sigma _ { \mathrm { w } } ^ { 2 } \ll 1$ , we have $\sigma _ { 0 } ^ { 2 } \approx \sigma _ { 1 } ^ { 2 }$ , i.e., the variances of the two Gaussian distributions are nearly identical. In this case, the solution to $f _ { \Xi | \mathcal { H } _ { 0 } } ( \tau _ { \mathrm { E D } } ^ { * } ) = f _ { \Xi | \mathcal { H } _ { 1 } } ( \tau _ { \mathrm { E D } } ^ { * } )$ can be approximated as

$$
\tau_ {\mathrm{ED}} ^ {*} \approx \frac {\mu_ {0} + \mu_ {1}}{2}.\tag{42}
$$

## APPENDIX B

Observing the third term of $\mathcal { D } ( K )$ , we have

$$
\Gamma (K) = \int_ {- \infty} ^ {+ \infty} f _ {0} (\mathbf {y} _ {\mathrm{w}})
$$

$$
\times \ln \left(\sum_ {j = 1} ^ {C _ {T} ^ {K}} \exp \left(\frac {P _ {\mathrm{a}} \sum_ {t \in \mathbf {t} _ {j}} \sum_ {i = n (t - 1) + 1} ^ {n t} y _ {\mathrm{w}} ^ {2} [ i ]}{2 \sigma_ {\mathrm{w}} ^ {2} (\sigma_ {\mathrm{w}} ^ {2} + P _ {\mathrm{a}})}\right)\right) d \mathbf {y} _ {\mathrm{w}},\tag{43}
$$

Then, we can obtain that when the joint distribution of $\mathbf { y } _ { \mathrm { w } }$ is $f _ { 0 } ( \mathbf { y } _ { \mathrm { w } } )$ , Γ(K) can be expressed as

$$
\Gamma (K) = \mathbb {E} \left[ \ln \left(\sum_ {j = 1} ^ {C _ {T} ^ {K}} \exp \left(c \sum_ {t \in \mathbf {t} _ {j}} \gamma_ {t}\right)\right) \right],\tag{44}
$$

where $\gamma _ { t } = \sum _ { i = n ( t - 1 ) + 1 } ^ { n t } y _ { \mathrm { w } } ^ { 2 } [ i ]$ , and $\begin{array} { r } { c = \frac { P } { 2 \sigma _ { \mathrm { w } } ^ { 2 } ( n K \sigma _ { \mathrm { w } } ^ { 2 } + P ) } . \ \gamma _ { 1 } , \gamma _ { 2 } , \dots , \gamma _ { T } } \end{array}$ are independent and identically distributed samples from $\sigma _ { \mathrm { w } } ^ { 2 } \chi ^ { 2 } ( n ) \ ( \chi ^ { 2 } ( n )$ is a chi-squared distribution with n degrees of freedom).

Let $\Lambda ( K ) = \sum _ { j = 1 } ^ { C _ { T } ^ { K } } \exp \left( c \sum _ { t \in { \bf t } _ { j } } \gamma _ { t } \right)$ and g(γ<sub>1</sub> γ<sub>2</sub> · · ·  γ<sub>K</sub>) = $\exp ( c ( \gamma _ { 1 } + \gamma _ { 2 } + \cdot \cdot \cdot + \gamma _ { K } ) )$ , then $\operatorname { \hat { \Pi } } ( K )$ can be expressed as

$$
\Lambda (K) = \sum_ {i _ {1}, i _ {2}, \dots , i _ {K} \in \{\mathbf {t} _ {1}, \mathbf {t} _ {2}, \dots , \mathbf {t} _ {C _ {T} ^ {K}} \}} g (\gamma_ {i _ {1}}, \gamma_ {i _ {2}}, \dots , \gamma_ {i _ {K}}).\tag{45}
$$

Using Theorem 12.3 in Ref. [37], we can obtain that

$$
U _ {T} = \frac {1}{C _ {T} ^ {K}} \Lambda (K),\tag{46}
$$

is U-statistics, then we can further get

$$
\sqrt {T} (U _ {T} - \mu (K)) \rightarrow_ {d} \mathcal {N} (0, K ^ {2} \zeta_ {1} (K)).\tag{47}
$$

The symbol $ _ { d }$ indicates convergence in distribution, which meas that the distribution of the left variable converges to the right distribution when $T \to \infty$

So, when $T \to \infty$ the distribution of Λ(K) can be given by

$$
\Lambda (K) \rightarrow_ {d} \mathbf {N} \equiv \mathcal {N} \left(C _ {T} ^ {K} \mu (K), \frac {(C _ {T} ^ {K}) ^ {2} K ^ {2}}{T} \zeta_ {1} (K)\right),\tag{48}
$$

where

$$
\mu (K) = \mathbb {E} (g (\gamma_ {1}, \gamma_ {2}, \dots , \gamma_ {K})) = [ \mathbb {E} (\exp (c \gamma_ {1})) ] ^ {K}\tag{49}
$$

and

$$
\begin{array}{l} \zeta_ {1} (K) = \operatorname{cov} (g (\gamma_ {1}, \gamma_ {2}, \ldots , \gamma_ {K}), g (\gamma_ {1}, \gamma_ {K + 1}, \gamma_ {2 K - 1})) \\ \qquad = \operatorname{var} (\exp (c \gamma_ {1})) [ \mathbb {E} (\exp (c \gamma_ {1})) ] ^ {K - 1}. \end{array}\tag{50}
$$

Given that $P _ { \mathrm { a } } = P / ( n K ) < \sigma _ { \mathrm { w } } ^ { 2 }$ , it follows from the momentgenerating function of the chi-squared distribution that

$$
\mathbb {E} (\exp (c \gamma_ {1})) = \left(\frac {n K \sigma_ {\mathrm{w}} ^ {2} + P}{n K \sigma_ {\mathrm{w}} ^ {2}}\right) ^ {\frac {n}{2}}
$$

and

(51)

$$
\begin{array}{c} \operatorname{var} (\exp (c \gamma_ {1})) = \mathbb {E} (\exp (2 c \gamma_ {1})) - \mathbb {E} (\exp (c \gamma_ {1})) ^ {2} \\ = \left(\frac {n K \sigma_ {\mathrm{w}} ^ {2} + P}{n K \sigma_ {\mathrm{w}} ^ {2} - P}\right) ^ {\frac {n}{2}} - \left(\frac {n K \sigma_ {\mathrm{w}} ^ {2} + P}{n K \sigma_ {\mathrm{w}} ^ {2}}\right) ^ {n}. \end{array}\tag{52}
$$

Substituting (51) into (49), and substituting (52) into (50), yields

$$
\mu (K) = \left(\frac {n K \sigma_ {\mathrm{w}} ^ {2} + P}{n K \sigma_ {\mathrm{w}} ^ {2}}\right) ^ {\frac {n K}{2}}\tag{53}
$$

and

$$
\begin{array}{c} \zeta_ {1} (K) = \left(\frac {n K \sigma_ {\mathrm{w}} ^ {2} + P}{n K \sigma_ {\mathrm{w}} ^ {2} - P}\right) ^ {\frac {n}{2}} \left(\frac {n K \sigma_ {\mathrm{w}} ^ {2} + P}{n K \sigma_ {\mathrm{w}} ^ {2}}\right) ^ {\frac {n (K - 1)}{2}} \\ - \left(\frac {n K \sigma_ {\mathrm{w}} ^ {2} + P}{n K \sigma_ {\mathrm{w}} ^ {2}}\right) ^ {\frac {n (K + 1)}{2}}, \end{array}\tag{54}
$$

respectively.

Substituting $\Gamma ( K ) = \mathbb { E } \left[ \ln \left( \Lambda ( K ) \right) \right]$ back into the expression for D(K) and performing the necessary calculations, we can obtain

$$
\begin{array}{c} \mathcal {D} (K) = \ln C _ {T} ^ {K} + \ln \mu (K) - \mathbb {E} (\ln \Lambda (K)) \\ = \mathbb {E} (\ln \mu (K) - \ln U _ {T}). \end{array}\tag{55}
$$

Using the Taylor expansion, we can derive

$$
\begin{array}{l} \ln U _ {T} - \ln \mu (K) = \frac {1}{\mu (K)} (U _ {T} - \mu (K)) \\ \qquad - \frac {1}{(\mu (K)) ^ {2}} (U _ {T} - \mu (K)) ^ {2} + o _ {p} (1). \end{array}\tag{56}
$$

Thus, D(K) can be approximately represented as

$$
\mathcal {D} (K) \approx \frac {1}{(\mu (K)) ^ {2}} \mathrm{var} (U _ {T}) = \frac {K ^ {2} \zeta_ {1} (K)}{T (\mu (K)) ^ {2}}.\tag{57}
$$

Substituting (53) and (54) into (57) and simplifying, we can obtain

$$
\begin{array}{l} \mathcal {D} (K) \approx \frac {K ^ {2}}{2 T} \left[ (1 - \gamma_ {\mathrm{w}} (K)) ^ {- \frac {n}{2}} - (1 + \gamma_ {\mathrm{w}} (K)) ^ {\frac {n}{2}} \right] \\ \times (1 + \gamma_ {\mathrm{w}} (K)) ^ {- \frac {n K}{2}}, \end{array}\tag{58}
$$

where $\gamma _ { \mathrm { w } } ( K ) = P _ { \mathrm { a } } / \sigma _ { \mathrm { w } } ^ { 2 } = P / \left( n K \sigma _ { \mathrm { w } } ^ { 2 } \right)$ , representing the signalto-noise ratio (SNR) per channel use on average.

Let $\gamma _ { \mathrm { w } } ^ { \ast } ~ = ~ P / \left( n \sigma _ { \mathrm { w } } ^ { 2 } \right)$ , then we can get $\gamma _ { \mathrm { w } } ( K ) \ = \ \gamma _ { \mathrm { w } } ^ { * } / K .$ Substituting $\gamma _ { \mathrm { w } } ^ { \ast }$ into the KL divergence expression (58) yields

$$
\begin{array}{c} \mathcal {D} (K) \approx \frac {K ^ {2}}{2 T} \left(\frac {\left(1 + \frac {\gamma_ {\mathrm{w}} ^ {*}}{K}\right) ^ {- \frac {n K}{2}}}{\left(1 - \frac {\gamma_ {\mathrm{w}} ^ {*}}{K}\right) ^ {\frac {n}{2}}} - \left(1 + \frac {\gamma_ {\mathrm{w}} ^ {*}}{K}\right) ^ {- \frac {n (K - 1)}{2}}\right) \\ = \frac {K ^ {2}}{2 T} \left(1 + \frac {\gamma_ {\mathrm{w}} ^ {*}}{K}\right) ^ {- \frac {n (K - 1)}{2}} \left[ \left(1 - \frac {\gamma_ {\mathrm{w}} ^ {* 2}}{K ^ {2}}\right) ^ {- \frac {n}{2}} - 1 \right]. \end{array}\tag{59}
$$

Since the assumption $\gamma _ { \mathrm { w } } ^ { \ast } \ll 1$ holds, we have

$$
\left(1 - \frac {\gamma_ {\mathrm{w}} ^ {* 2}}{K ^ {2}}\right) ^ {- \frac {n}{2}} \simeq 1 + \frac {n}{2} \frac {\gamma_ {\mathrm{w}} ^ {* 2}}{K ^ {2}}.\tag{60}
$$

Substituting this into the expression of D(K) yields

$$
\begin{array}{l} \mathcal {D} (K) \approx \frac {n \gamma_ {\mathrm{w}} ^ {* 2}}{4 T} \left(1 + \frac {\gamma_ {\mathrm{w}} ^ {*}}{K}\right) ^ {- \frac {n (K - 1)}{2}} \\ = \frac {n \gamma_ {\mathrm{w}} ^ {* 2}}{4 T} \exp \left(- \frac {n (K - 1)}{2} \ln \left(1 + \frac {\gamma_ {\mathrm{w}} ^ {*}}{K}\right)\right) \\ \approx \frac {n \gamma_ {\mathrm{w}} ^ {* 2}}{4 T} \exp \left(- \frac {n (K - 1)}{2} \frac {\gamma_ {\mathrm{w}} ^ {*}}{K}\right) \\ = \frac {n \gamma_ {\mathrm{w}} ^ {* 2}}{4 T} \exp \left(- \frac {n \gamma_ {\mathrm{w}} ^ {*}}{2} \left(1 - \frac {1}{K}\right)\right). \end{array}\tag{61}
$$

## REFERENCES

[1] Z. Ni, Z. Hua, X. Yang, R. Zhang, S. Wang, and G. Pan, “LLM-aided spectrum-sharing LEO satellite communications,” IEEE J. Sel. Areas Commun., vol. 44, pp. 2591–2605, 2026.

[2] G. Pan et al., “Distributed movable antenna systems for reliable, flexible, and resilient communications: Architectures, techniques, and challenges,” IEEE Wireless Commun., early access, 2025.

[3] X. Zhang et al., “Secure multi-satellite collaborations with ISAC,” IEEE Trans. Wireless Commun., vol. 25, pp. 11624–11640, 2026.

[4] F. A. P. Petitcolas, R. J. Anderson, and M. G. Kuhn, “Information hiding–A survey,” Proc. IEEE, vol. 87, no. 7, pp. 1062–1078, Jul. 1999.

[5] B. Li, Z. Fei, C. Zhou, and Y. Zhang, “Physical-layer security in space information networks: A survey,” IEEE Internet Things J., vol. 7, no. 1, pp. 33–52, Jan. 2020.

[6] X. Chen, D. W. K. Ng, W. H. Gerstacker, and H.-H. Chen, “A survey on multiple-antenna techniques for physical layer security,” IEEE Commun. Surv. Tut., vol. 19, no. 2, pp. 1027–1053, 2nd Quart., 2017.

[7] Z. Wei, F. Liu, C. Masouros, and H. V. Poor, “Fundamentals of physical layer anonymous communications: Sender detection and anonymous precoding,” IEEE Trans. Wireless Commun., vol. 21, no. 1, pp. 64–79, Jan. 2022.

[8] T. J. Bihl, K. W. Bauer, and M. A. Temple, “Feature selection for RF fingerprinting with multiple discriminant analysis and using ZigBee device emissions,” IEEE Trans. Inf. Forensics Security, vol. 11, no. 8, pp. 1862–1874, Aug. 2016.

[9] W. Xu, W. Trappe, Y. Zhang, and T. Wood, “The feasibility of launching and detecting jamming attacks in wireless networks,” in Proc. 6th ACM Int. Symp. Mobile Ad Hoc Netw. Comput., May 2005, pp. 46–57.

[10] H. Pirayesh and H. Zeng, “Jamming attacks and anti-jamming strategies in wireless networks: A comprehensive survey,” IEEE Commun. Surv. Tut., vol. 24, no. 2, pp. 767–809, 2nd Quart., 2022.

[11] K. Lu, H. Liu, L. Zeng, J. Wang, Z. Zhang, and J. An, “Applications and prospects of artificial intelligence in covert satellite communication: A review,” Sci. China Inf. Sci., vol. 66, no. 2, Feb. 2023, Art. no. 121301.

[12] S. Wang et al., “Generative AI empowered covert communications: Autonomy, eficiency, and suitability,” IEEE Wireless Commun., early access, 2025.

[13] A. D. Wyner, “The wire-tap channel,” Bell Syst. Tech. J., vol. 54, no. 8, pp. 1355–1387, Oct. 1975.

[14] C. Chen, S. Wang, L. Li, S. Ke, C. Wang, and X. Bu, “Intelligent covert satellite communication for military robot swarm,” IEEE Access, vol. 8, pp. 5363–5382, 2020.

[15] R. Pickholtz, D. Schilling, and L. Milstein, “Theory of spread-spectrum communications–A tutorial,” IEEE Trans. Commun., vol. C-30, no. 5, pp. 855–884, May 1982.

[16] F. Wang, J. Tian, and W. Cui, “An open-loop adaptive algorithm for dynamic multipath estimation in DSSS systems,” IEEE Trans. Aerosp. Electron. Syst., vol. 59, no. 6, pp. 7539–7558, Dec. 2023.

[17] S. Luo, S. Zhang, S. Ke, S. Wang, X. Bu, and J. An, “Optimum combining for coherent FFH/DS spread spectrum receivers in the presence of multi-tone jammer,” IEEE Access, vol. 8, pp. 53097–53106, 2020.

[18] S. Wang et al., “GaussMask-DSSS: Enhancing covert spread spectrum communication with Gaussian cloaking and deep learning-aided synchronization,” IEEE J. Sel. Areas Commun., vol. 44, pp. 1495–1511, 2026.

[19] S. Luo et al., “Network for hypersonic UCAV swarms,” Sci. China Inf. Sci., vol. 63, no. 4, pp. 1–28, Apr. 2020.

[20] B. A. Bash, D. Goeckel, and D. Towsley, “Limits of reliable communication with low probability of detection on AWGN channels,” IEEE J. Sel. Areas Commun., vol. 31, no. 9, pp. 1921–1930, Sep. 2013.

[21] L. Wang, G. W. Wornell, and L. Zheng, “Fundamental limits of communication with low probability of detection,” IEEE Trans. Inf. Theory, vol. 62, no. 6, pp. 3493–3503, Jun. 2016.

[22] M. Tahmasbi and M. R. Bloch, “First- and second-order asymptotics in covert communication,” IEEE Trans. Inf. Theory, vol. 65, no. 4, pp. 2190–2212, Apr. 2019.

[23] M. R. Bloch, “Covert communication over noisy channels: A resolvability perspective,” IEEE Trans. Inf. Theory, vol. 62, no. 5, pp. 2334–2354, May 2016.

[24] P. H. Che, M. Bakshi, and S. Jaggi, “Reliable deniable communication: Hiding messages in noise,” in Proc. IEEE Int. Symp. Inf. Theory, Jul. 2013, pp. 2945–2949.

[25] A. Abdelaziz and C. E. Koksal, “Fundamental limits of covert communication over MIMO AWGN channel,” in Proc. IEEE Conf. Commun. Netw. Secur. (CNS), Oct. 2017, pp. 1–9.

[26] B. He, S. Yan, X. Zhou, and V. K. N. Lau, “On covert communication with noise uncertainty,” IEEE Commun. Lett., vol. 21, no. 4, pp. 941–944, Apr. 2017.

[27] H. Q. Ta and S. W. Kim, “Covert communication under channel uncertainty and noise uncertainty,” in Proc. IEEE Int. Conf. Commun. (ICC), May 2019, pp. 1–6.

[28] B. A. Bash, D. Goeckel, and D. Towsley, “Covert communication gains from adversary’s ignorance of transmission time,” IEEE Trans. Wireless Commun., vol. 15, no. 12, pp. 8394–8405, Dec. 2016.

[29] R. Xu, D. Guo, B. Zhang, and G. Ding, “Finite blocklength covert communications with random selection of channel use,” IEEE Wireless Commun. Lett., vol. 10, no. 9, pp. 2085–2089, Sep. 2021.

[30] X. Lu, W. Yang, and S. Yan, “Short-packet covert communication with transmission time uncertainty,” in Proc. 7th Int. Conf. Comput. Commun. Syst. (ICCCS), Chengdu, China, Apr. 2022, pp. 628–632.

[31] X. Lu, S. Yan, W. Yang, M. Li, and D. W. K. Ng, “Covert communication with time uncertainty in time-critical wireless networks,” IEEE Trans. Wireless Commun., vol. 22, no. 2, pp. 1116–1129, Feb. 2023.

[32] S. Yan, X. Zhou, J. Hu, and S. V. Hanly, “Low probability of detection communication: Opportunities and challenges,” IEEE Wireless Commun., vol. 26, no. 5, pp. 19–25, Oct. 2019.

[33] E. L. Lehmann et al., Testing Statistical Hypotheses, vol. 3. Cham, Switzerland: Springer, 1986.

[34] S. Yan, B. He, X. Zhou, Y. Cong, and A. L. Swindlehurst, “Delayintolerant covert communications with either fixed or random transmit power,” IEEE Trans. Inf. Forensics Security, vol. 14, no. 1, pp. 129–140, Jan. 2019.

[35] Y. Hu, M. Serror, K. Wehrle, and J. Gross, “Finite blocklength performance of cooperative multi-terminal wireless industrial networks,” IEEE Trans. Veh. Technol., vol. 67, no. 7, pp. 5778–5792, Jul. 2018.

[36] K.-L. Tsai, Y.-L. Huang, F.-Y. Leu, I. You, Y.-L. Huang, and C.- H. Tsai, “AES-128 based secure low power communication for LoRaWAN IoT environments,” IEEE Access, vol. 6, pp. 45325–45334, 2018.

[37] A. W. Van der Vaart, Asymptotic Statistics, vol. 3. Cambridge, U.K.: Cambridge Univ. Press, 2000.
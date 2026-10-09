# AirMask: Enabling Air-to-Air Masking of Wireless Traffic Fingerprints in WiFi-Based IoT Environments

Huafeng Bian , Jianfeng Li , Xiaobo Ma , Member, IEEE, Jialong Zhang , Xiapu Luo ,

Wei Wang , Senior Member, IEEE, Zhou Su , Senior Member, IEEE, and Xiaohong Guan , Life Fellow, IEEE

Abstract—The Internet of Things (IoT) commonly adopts IEEE 802.11 wireless communication. However, the latest studies have revealed the advanced attacks that can analyze side-channel behavioral fingerprints of wireless frames to infer privacy-sensitive user behaviors. Obfuscating such fingerprints at the originating device has been widely regarded as the most fundamental defense strategy. However, this device-to-air approach conflicts with the realities of IoT: extreme heterogeneity, proprietary firmware, and limited resources render device-level modification impractical. As a result, what appears conceptually natural becomes a key barrier to scalable defense, leaving IoT users broadly exposed to the latest advanced attacks. To counter these emerging threats while enabling practical, wide-scale deployment, we present AirMask, the first air-to-air defense system that works transparently to IoT devices while protecting them adaptively. AirMask passively senses fingerprints in the air and injects carefully crafted frames into the air to mask occurring traffic fingerprints as needed. Despite its promise, the air-to-air defense faces three challenges: i) observing timevarying traffic of all devices while adaptively sensing occurring fingerprints for each device, ii) promptly injecting crafted frames that can mask fingerprints once they occur, and iii) camouflaging crafted frames to withstand adversarial filtering. To address these challenges, AirMask operates in a predict-inject-assess loop. This loop iteratively adapts to changing traffic patterns, proactively injects principally crafted frames upon the prediction of occurring fingerprints, and continuously refines device-specific obfuscation strategies against attacks. The injection removes fingerprints while maintaining the crafted frames’ context indistinguishability (e.g., protocol fields and sequence states) from authentic ones. We have implemented AirMask as a functional hardware prototype, offering Integrated, TAP, and Air modes for flexible deployment within WiFi networks to protect surrounding IoT devices. Extensive evaluations on 90 types of IoT devices and 53 fine-grained behaviors confirm AirMask’s defensive effectiveness, while incurring negligible bandwidth and latency overhead.

Index Terms—Network security, traffic fingerprinting.

## I. INTRODUCTION

venience while simultaneously introducing new security risks. By connecting cyberspace with the physical world, IoT greatly enlarges the attack surface, exposing users to threats that compromise both information security and physical safety. Recently reported IoT attacks, such as the Wyze camera breach [9] and the ransomware attack on St. Lawrence Health [10], highlight the significant risks that these attacks pose to both user privacy and critical infrastructure.

Among various IoT attacks, IoT wireless fingerprinting (IWF) attacks are particularly concerning due to the pervasive use of IEEE 802.11 [11], [12], [13], [14]. IWF attacks can be conducted by passively monitoring wireless transmissions within signal range, without requiring network intrusion or device compromise. At first glance, such attacks may appear less prevalent in real-world incidents compared to large-scale IoT exploits such as botnets or ransomware. This is largely because the practical capabilities of wireless fingerprinting have historically been limited. Early techniques primarily focused on coarse-grained device identification (e.g., PingPong [12] achieved over 0.9 precision when classifying more than 90 device types). However, recent advances suggest that this limitation is rapidly diminishing. As shown in Fig. 1, existing research demonstrates a clear progression in inference granularity. Early work focused on distinguishing device types or models, while subsequent studies enabled inference of device states and usage patterns in smart environments (e.g., Ma et al. [15] accurately identified 29 interactive device behaviors, including plug on/offevents and speaker music playback). More recent advances further indicate that even fine-grained interaction behaviors with the physical world can be inferred from encrypted traffic using commodity WiFi interfaces, further lowering the barrier to practical deployment. For example, prior work suggests that device states, such as a smart lock being set to “away” mode, can be inferred from traffic patterns, which may facilitate physical-world attacks such as targeted intrusion [16]. This further blurs the boundary between communication signals and physical-world observability.

![](images/402d72f545f8dbe82a620b13247cdc7115d577df0b33e53a98b2fdd5d16bb123.jpg)  
Fig. 1. Expanding inference capability of IWF.

Such a progression suggests that wireless transmissions are gradually exposing richer information than originally intended. This trend is primarily driven by advances in data-driven modeling and the increasing regularity of IoT communication patterns. Modern learning-based approaches can capture subtle temporal and statistical structures from encrypted traffic that were previously indistinguishable, while the widespread deployment of IoT devices introduces stable and device-specific behaviors that facilitate reliable inference. Taken together, these trends mark an inflection point: while large-scale exploitation has not yet been widely reported, the underlying technical barriers are steadily decreasing, and the attack capability is transitioning to fine-grained physical-world behavioral inference. This transition highlights the necessity of proactively developing protection mechanisms.

To mitigate IWF attacks, fingerprint obfuscation at the originating device is considered the most fundamental defense strategy, since direct control over the device enables maximal flexibility in designing obfuscation mechanisms, including packet padding, dummy packet injection, and packet delaying [17], [18], [19], [20], [21]. Despite their theoretical effectiveness, such device-to-air defenses encounter inherent limitations in practical deployment, as they must be deployed on each protected IoT device. They can be implemented with on-device middleware, just like Tor plugins and encryption proxy clients commonly used to mitigate website and app fingerprinting [22], [23], [24], [25]. However, the limited resources and the widespread unavailability of general-purpose operating systems (e.g., Windows, Android) on IoT devices present substantial barriers to middleware deployment. Also, these defenses can be integrated into device firmware by manufacturers. Due to device diversity and the continuous evolution of firmware, modifying firmware would be costly. As a result, what appears conceptually natural becomes a key barrier to scalable defense, leaving IoT users broadly exposed to the latest advanced attacks.

To counter these emerging threats while enabling practical, wide-scale deployment, we present AirMask, the first airto-air defense system that transparently protects IoT devices without requiring any device or firmware modification. Air-Mask operates in a non-cooperative setting, where the defender cannot alter existing frames or delay their transmission. Under these constraints, frame injection becomes the only viable defense primitive. Accordingly, AirMask passively senses fingerprints in the air and injects carefully crafted fingerprintmasking frames (termed “mask frames”) into the air to mask occurring fingerprints as needed, without disrupting original device behavior or protocol execution. While frame injection is inherently deployment-friendly, its effectiveness in obfuscating fingerprints has never been systematically validated. Whether injection alone can provide strong protection against IWF attacks remains an open question.

To realize effective air-to-air defenses based on this only viable primitive, three major challenges must be addressed.

C1. Injection under Traffic Heterogeneity ( what to inject ): IoT traffic exhibits significant heterogeneity across devices and even across different operational states of the same device. An effective air-to-air defense must determine what frames to inject in a context-aware manner, without prior knowledge of device behaviors. Static or fixed injection strategies fail to generalize across diverse traffic patterns, leading to either excessive overhead or insufficient fingerprint obfuscation.

C2. Injection Timing and Responsiveness ( when to inject ): In air-to-air settings, defenders lack foresight into forthcoming transmissions from IoT devices. Consequently, effective fingerprint obfuscation critically depends on precisely deciding when to inject. Delayed or poorly timed injection may miss the narrow windows in which fingerprint-defining features emerge, rendering otherwise valid mask frames ineffective.

C3. Injection Indistinguishability and Resistance ( how to inject ): Even timely and well-chosen injections may fail if attackers can identify and filter injected frames. Attackers may attempt to identify and filter out injected frames by exploiting discrepancies between injected and authentic frames, such as protocol inconsistencies and abnormal sequence states. An effective air-to-air defense must therefore decide how to inject frames that remain robust against adversarial filtering.

To address C1, AirMask iteratively learns device-specific obfuscation strategies in a self-supervised manner. Specifically, once a fingerprint occurs, AirMask selects a strategy from a strategy space (detailed in Section IV-B) to generate mask frames and proactively injects them into the air to mask the fingerprint as needed. The strategy space is engineered to encompass both per-frame and per-sequence manipulations, such as insertion, cloning, and replaying. Through these operations, the system aims to either randomize fingerprints (e.g., by injecting random frames) or introduce misinformation (e.g., by replaying frames from other devices), thereby disrupting attackers’ ability to identify unique device fingerprints. As injection progresses, the mask frame generation strategy evolves from initial random strategies, which operate without prior device information, to device-specific ones. This progression is driven by continuous assessment of its defensive efficacy against a versatile attacker.

Addressing C1 facilitates the generation of evolving obfuscation strategies. However, these strategies must be promptly executed upon fingerprint emergence. Therefore, while observing traffic produced by an IoT device, AirMask tackles C2 by predicting the 802.11 frames that the device will likely transmit using a prediction model. Once predicting the appearance of a fingerprint, the system proactively injects crafted mask frames. These frames are precisely synchronized with the predicted frames in timing, effectively masking fingerprints. The prediction process is seamlessly integrated into the device-specific strategy learning, establishing a closed predict-inject-assess loop.

![](images/e8bdac1397a7b8198323089f7c4b6b7f62cedaae1ad71029aa71a92863ed6e2e.jpg)  
Fig. 2. Threat model. IoT devices connect to the AP via WiFi. The defender, within WiFi coverage, can inject crafted frames, while the attacker passively sniffs from outside.

However, even timely and accurate injection is insufficient. A capable attacker may apply adversarial filtering to distinguish and discard injected frames, thereby undermining injectionbased defenses (C3). To counter such attempts, AirMask carefully crafts mask frames to remain indistinguishable from authentic ones. This is achieved by customizing the operating system (OS) kernel and network interface card (NIC) driver, ensuring that injected frames conform to expected protocol formats and sequence states.

Through these novel designs, AirMask constitutes the first immediately deployable air-to-air defense system against IWF attacks. We emphasize that air-to-air in AirMask refers to the defense actuation domain rather than the observation source. Fingerprint prediction may rely on different observation sources, including passively sniffed over-the-air frames or network-layer packets. Regardless of the observation source, the defense is executed by injecting crafted frames directly into the wireless medium and remains transparent to IoT devices. We have implemented AirMask as a functional hardware prototype, offering Integrated, TAP, and Air modes for flexible deployment within WiFi networks. It is evaluated on public datasets and deployed in a real-world smart home network. Extensive evaluations on 90 types of IoT devices and 53 fine-grained behaviors demonstrate that AirMask effectively defends against all four types of IWF attacks, including those based on packet length and direction, packet sequence, spatiotemporal features, and statistical features. Compared to existing defenses, including Link Layer GAN [20], Traffic Replay [26], and Frame Flooding, AirMask achieves significantly stronger protection with minimal overhead.

## Our work has made the following contributions:

\- To our best knowledge, AirMask represents the first air-to-air IWF defense system. It overcomes three key challenges: i) injection under traffic heterogeneity, ii) injection timing and responsiveness, and iii) injection indistinguishability and resistance. It also supports three flexible deployment modes to accommodate practical scenarios. We have released AirMask’s source code and datasets at https://github.com/smith0818/AirMask.

We propose an iterative learning approach to explore mask frame generation strategies for device-specific defense. To offset injection delays, we design a packet-frame prediction model for proactive frame injection. With OS kernel and NIC driver customization, the injected frames are made indistinguishable from authentic ones at the protocol layer.

Extensive evaluations on 90 types of IoT devices and 53 device behaviors in real-world networks and public datasets demonstrate that AirMask effectively thwarts IWF attacks. It reduces attack precision and recall from 0.81–0.90 to 0.09–0.31, while incurring less than 1% bandwidth overhead and only about 2 ms of additional device delay.

## II. THREAT MODEL

We focus on WiFi scenarios due to their widespread use in IoT devices. The threat model is depicted in Fig. 2. We assume a passive yet capable attacker within WiFi coverage.

Attackers passively monitor over-the-air 802.11 frames using commercial sniffing NICs, thereby identifying IoT devices and inferring their behaviors. Without access to communication keys, they cannot decrypt frame payloads, nor can they intercept or modify frames. Instead, they rely on side-channel traffic features, including frame length, direction, and timing. Attackers can also exploit protocol fields and sequence numbers to further identify and discard forged defensive frames.

Defenders aim to prevent attackers from identifying the types and behaviors of protected IoT devices. This is achieved by injecting crafted wireless frames into the air through an air-to-air defense. The approach requires no device modifications or manufacturer involvement and supports plug-and-play compatibility across heterogeneous IoT devices.

## III. AIRMASK OVERVIEW

We first formulate the goal of AirMask and then outline its workflow. Finally, we summarize the three deployment modes included in AirMask’s application scenarios.

## A. Defense Formulation

AirMask aims to disrupt the attacker’s device fingerprint classification. By injecting mask frames into the air, the system causes a passively sniffing attacker to receive both authentic and mask frames simultaneously. Its objective can be formulated as

$$
\begin{array}{l l} \text {max} & \gamma (\mathrm{U} _ {t y p} \oplus \mathrm{U} _ {t y p} ^ {\prime}) + \delta (\mathrm{U} _ {b x} \oplus \mathrm{U} _ {b x} ^ {\prime}), \\ \text {s.t.} & \mathrm{U} _ {t y p} = \operatorname{Cls} _ {t y p} (\mathrm{F} (\mathrm{E} (P W _ {t}))), \mathrm{U} _ {t y p} ^ {\prime} \\ & \qquad = \operatorname{Cls} _ {t y p} (\mathrm{F} (\mathrm{E} (P W _ {t}), P F _ {t})), \\ & \mathrm{U} _ {b x} = \operatorname{Cls} _ {b x} (\mathrm{F} (\mathrm{E} (P W _ {t}))), \mathrm{U} _ {b x} ^ {\prime} \\ & \qquad = \operatorname{Cls} _ {b x} (\mathrm{F} (\mathrm{E} (P W _ {t}), P F _ {t})), \\ & \mathrm{B} (P W _ {t}) = \mathrm{B} (P W _ {t}, P F _ {t}), \end{array}\tag{1}
$$

where $\mathrm { U } _ { t y p } ( \cdot )$ and $\mathrm { U } _ { b x } ( \cdot )$ denote the device type and behavior identification results, respectively, and $\mathrm { U } _ { t y p } ^ { \prime } ( \cdot )$ and $\mathrm { U } _ { b x } ^ { \prime } ( \cdot )$ denote the identification results after defense. ⊕ denotes the exclusive OR operation, symbolizing our goal to mislead the fingerprinting classifier and induce erroneous identification. γ and δ are binary variables that specify the defense objective. $\mathrm { C l s } _ { t y p } ( \cdot )$ and $\mathrm { C l s } _ { b x } ( \cdot )$ are the device type and behavior fingerprinting classifiers, respectively. $P W _ { t }$ is the sliding window at time t, which contains TCP/IP packets transmitted by the IoT device. $P F _ { t }$ denotes the mask frames injected by AirMask at time t. E(·) encapsulates TCP/IP packets into 802.11 frames, and $\mathrm { F } ( \cdot )$ extracts features from 802.11 frames. B(·) denotes the operating state (normal or abnormal) of the IoT device.

![](images/f68c48117efd8686258af41f78998c5c421066c555de6670d36b7b8c249b3164.jpg)  
Fig. 3. AirMask’s application scenario (taking the Integrated and TAP modes as examples).

## B. AirMask Workflow

Fig. 3 depicts AirMask’s application scenario. Deployed within the WiFi coverage of target IoT devices, the system counters adversarial reconnaissance by injecting carefully crafted mask frames into the air. Attackers without access to communication keys cannot differentiate mask frames from authentic ones, precluding their ability to extract behavioral fingerprints. In contrast, IoT devices possessing these keys reliably identify and discard the crafted mask frames, ensuring normal operation remains unaffected.

AirMask adopts the defense architecture shown in Fig. 4. The system anchors its input on real-time traffic observations of IoT devices, with the core objective of generating and promptly injecting predictive mask frames targeting imminent behavioral fingerprints. To initiate the online iteration between input (realtime IoT traffic) and output (predictive mask frames), the system integrates two key mechanisms: runtime observation and adaptive feedback. Runtime observation synchronously monitors two streams: real-time IoT packets/frames (to capture fingerprints) and system-generated predictive mask frames (to track injection behavior). In the Integrated and TAP modes, the input is the device’s IP packets (as exemplified in Fig. 4), while in the Air mode, it is the device’s wireless frames. Complementing this, adaptive feedback refines the fingerprint repository via historical IoT traffic to capture evolving adversarial fingerprints while dynamically evaluating mask frame quality to fine-tune generation strategies. By orchestrating these mechanisms into a closed predict-inject-assess loop, AirMask continuously provides proactive injection defense without relying on prior knowledge of device, while maintaining persistent adaptability.

Specifically, AirMask observes IoT traffic and processes it through the Packet-Frame Prediction (Section IV-A) module. This module predicts protocol-specific packets and merges them into frames. Then, the Mask Frame Injection (Section IV-B) module checks whether predicted frames match device fingerprints in the repository. If not matched, no action is taken; otherwise, the optimal strategy is selected to generate mask frames. Before injecting these frames via multiple antennas, the Mask Frame Camouflage (Section IV-C) module performs camouflage by adjusting their protocol fields and sequential states, thereby achieving protocol layer state alignment and physical layer sig nal diversity. The Fingerprint-Aware Assessment (Section IV-D) module provides an adaptive feedback loop: an agent continuously updates the fingerprint repository from historical IoT traffic and assesses mask frames targeting emerging fingerprints, thereby masking link layer device fingerprints.

## C. Deployment Modes

To accommodate practical scenarios, AirMask offers three flexible deployment modes (see Fig. 9(a)), none of which require modifications to the protected IoT devices.

• Integrated Mode: AirMask is seamlessly integrated into the AP, leveraging the AP’s traffic mirroring function to capture the TCP/IP traffic of connected IoT devices. This mode is suitable when AP modification is feasible.

• TAP Mode: AirMask is deployed between the AP and the external network using a test access point (TAP) device, which mirrors the AP’s inbound and outbound TCP/IP traffic. It serves as an alternative when AP modification is impractical.

• Air Mode: AirMask requires no connection to the AP; it only needs to be within WiFi coverage to capture wireless traffic, enabling plug-and-play deployment. By default, we adopt the Integrated Mode due to its broad and fine-grained traffic visibility, which enhances AirMask’s defense capability. A performance comparison of all three deployment modes is presented in Section V-F.

## IV. AIRMASK DESIGN

AirMask consists of four core modules: Packet-Frame Prediction (Section IV-A), Mask Frame Injection (Section IV-B), MaskFrame Camouflage (Section IV-C), and Fingerprint-Aware Assessment (Section IV-D).

## A. Packet-Frame Prediction

To achieve real-time defense, we propose a hierarchical prediction method that predicts forthcoming frames from current traffic, thereby enabling proactive mask frame injection.

1) Learning the Characteristics of TCP/IP Packets: We develop a Gated Markov model as a lightweight short-term predictor for IoT traffic. The model is not intended to reconstruct the complete protocol state machine, nor does it aim to precisely predict application-layer responses. Rather, its primary goal is to predict short-term observable side-channel features directly exploited by IWF attacks, including packet length, direction, and timing. Therefore, AirMask only needs to predict these low-level features within short time windows, as they are directly related to wireless fingerprints. The design of the Gated Markov model is motivated by the observation that IoT traffic is typically driven by fixed device functions, periodic tasks, and limited user interactions, and therefore often exhibits strong local sequential regularity over short time windows. To adapt to device state changes and traffic drift, the Gated Markov model introduces a gated update mechanism [27], which suppresses outdated transition patterns and incorporates newly observed packet behaviors online. This allows the short-term prediction state to be dynamically updated according to runtime traffic.

![](images/652ae8e6dc98538fcd4f9809f9a155833f7c370499992fbbc35f9a4668e22fd9.jpg)  
Fig. 4. AirMask’s architectural design. The four modules, i.e., Packet-Frame Prediction, Mask Frame Injection, Mask Frame Camouflage, and Fingerprint-Aware Assessment, form a predict-inject-assess loop to collaboratively mask IoT fingerprints.

## The model is constructed through four steps.

• Traffic Split: In Integrated mode, AirMask divides the TCP/IP traffic by IP addresses and protocols, allocating each flow to a specific PW. In TAP mode, it processes both the TCP/IP traffic from the AP and the wireless traffic from IoT devices. The TCP/IP traffic is then mapped to each device’s MAC address, with the characterization method elaborated in Appendix A-A, available online. In Air mode, wireless traffic is divided by MAC addresses and mapped to each device’s PW. The parameter setting of PW is detailed in Appendix B-A, available online.

• Traffic Characterization: Packets within PWs are mapped to a state space $\Phi = \{ \varphi _ { 1 } , . . . , \varphi _ { n } \}$ . Each packet is denoted as $\varphi _ { i } = ( l _ { i } , d _ { i } , t _ { i } )$ , where $l _ { i }$ is the packet length, $d _ { i }$ is the direction, and $t _ { i }$ is the relative time within PW. Given the Maximum Transmission Unit (MTU) of IP packets, $l _ { i }$ is bounded within the range [0, 1500] and partitioned into fixed-length intervals.

Packets within the same interval are considered as identical in length and direction.

• Traffic Prediction: We construct two independent Markov matrices: $M ^ { ( l , d ) }$ , which captures the transition probabilities of packet length and direction, and $M ^ { t }$ , which captures the transition probabilities of relative packet time. The transition tensors within $M ^ { ( l , d ) }$ and $M ^ { t }$ are defined as

$$
\begin{array}{l} m _ {\tau - 1, \tau , \tau + 1} ^ {(l, d)} = \mathrm{P} \left(\varphi_ {\tau + 1} ^ {(l, d)} | \varphi_ {\tau} ^ {(l, d)}, \varphi_ {\tau - 1} ^ {(l, d)}\right), \\ m _ {\tau - 1, \tau , \tau + 1} ^ {t} = \mathrm{P} (\varphi_ {\tau + 1} ^ {t} | \varphi_ {\tau} ^ {t}, \varphi_ {\tau - 1} ^ {t}), \end{array}\tag{2}
$$

where $\tau$ denotes the packet order, and $\mathrm { P } ( \cdot )$ is the conditional probability. Then, we concatenate $m _ { \tau - 1 , \tau , \tau + 1 } ^ { ( l , d ) }$ and $m _ { \tau - 1 , \tau , \tau + 1 } ^ { t }$ to form a complete packet prediction.

• Prediction Model Update: We incorporate gated units into the update process of the Markov transition matrix, including a forget gate $f _ { \tau }$ to discard outdated data and an update gate $u _ { \tau }$ to integrate new data. Their definitions are

$$
\begin{array}{l} f _ {\tau} = \sigma (w _ {f} \cdot [ h _ {\tau - 1}; x _ {\tau} ] + b _ {f}), \\ u _ {\tau} = \sigma (w _ {u} \cdot [ h _ {\tau - 1}; x _ {\tau} ] + b _ {u}), \end{array}\tag{3}
$$

where $[ h _ { \tau - 1 } ; x _ { \tau } ]$ denotes the concatenation of the previous hidden state $h _ { \tau - 1 }$ and the current state $x _ { \tau }$ (i.e., $\left[ \varphi _ { \tau } ; \varphi _ { \tau - 1 } \right] )$ , $w _ { f }$ and $w _ { u }$ are the weights for the forget and update gates, $b _ { f }$ and $b _ { u }$ are biases, and σ is the activation function.

The update rules for $M ^ { ( l , d ) }$ and $M ^ { t }$ are

$$
\begin{array}{l} M _ {\text {updated}} ^ {(l, d)} = f _ {\tau} \odot M ^ {(l, d)} + u _ {\tau} \odot \Delta M _ {\tau - 1, \tau , \tau + 1} ^ {(l, d)}, \\ M _ {\text {updated}} ^ {t} = f _ {\tau} \odot M ^ {t} + u _ {\tau} \odot \Delta M _ {\tau - 1, \tau , \tau + 1} ^ {t}, \end{array}\tag{4}
$$

where $\Delta M _ { \tau - 1 , \tau , \tau + 1 } ^ { ( l , d ) }$ and $\Delta M _ { \tau - 1 , \tau , \tau + 1 } ^ { t }$ denote the modifications to $M ^ { ( l , d ) }$ and $M ^ { t }$ , and $\odot$ is the Hadamard product.

![](images/057b106b8d7d43432572c8e9831f4ab7ba6f3afc52aa87f6c708e0c6a3831e72.jpg)  
Fig. 5. Exemplifying mask frame generation strategies.

2) Predicting the Upcoming 802.11 Frames: Based on the previously observed packet state $\varphi _ { \tau - 1 }$ and the current state $\varphi _ { \tau }$ AirMask first computes the predictive distribution of the next packet state as $p _ { \tau + 1 } ( \varphi ) = P ( \varphi \mid \varphi _ { \tau } , \varphi _ { \tau - 1 } )$ . This one-step prediction is then extended to iterative multi-step prediction. During iterative prediction, AirMask propagates the full predictive distribution, rather than recursively feeding the Maximum $\mathrm { A }$ Posteriori (MAP) estimate back as a deterministic state for the next prediction step. For the k-step prediction, the predictive distribution is computed as $p _ { \tau + k } = M ^ { k - 1 } p _ { \tau + 1 }$ , where M denotes the transition operator. Only when mask frames need to be generated does AirMask select the most probable packet state from the predictive distribution at the corresponding time step.

$$
\hat {\varphi} _ {\tau + k} = \arg \max _ {\varphi} p _ {\tau + k} (\varphi).\tag{5}
$$

In Integrated and TAP modes, IP packets within PWs are predicted and then encapsulated into the corresponding 802.11 data frames. In Air mode, this encapsulation is omitted, as the prediction is performed directly on 802.11 frames.

## B. Mask Frame Injection

AirMask aims to wipe device fingerprints by injecting mask frames. We first define mask frame generation strategies, and then detail how AirMask explores the optimal strategy.

1) Mask Frame Generation Strategy: We develop six mask frame generation strategies, classified into per-frame and persequence types based on the number of frames generated. These strategies aim to randomize, mask, and mislead device fingerprints. Fig. 5 illustrates their definitions.

• Frame Random Insertion (FRI): FRI constructs a single mask frame, denoted as $P F _ { \mathrm { F R I } } = \{ m _ { i } , l _ { i } , d _ { i } , t _ { i } , s n _ { i } \}$ , to randomly disrupt fingerprints. Here, $m _ { i }$ represents the MAC address, matching that of the authentic frame. $l _ { i }$ and $d _ { i } .$ , representing frame length and direction, are randomly assigned. $t _ { i }$ aligns the expected time of the upcoming authentic frame, and $s n _ { i }$ is also synchronized with the sequence number (SN) of the upcoming frame.

• Sequence Random Insertion (SRI): SRI constructs a series of mask frames, $P F _ { \mathrm { S R I } } { = } \{ P F _ { \mathrm { F R I _ { 1 } } } , . . . , P F _ { \mathrm { F R I _ { \it i } } } \}$ , each adhering to the FRI definition. These frames share the same MAC address and embed sequential SNs beginning from the target device’s latest SN value.

• Frame Replay $( F R ) .$ : FR constructs a mask frame, $P F _ { \mathrm { F R } }$ to mimic non-target devices, thereby misleading attackers into misidentifying the target device. $m _ { i } , \ t _ { i } ,$ and $s n _ { i }$ follow the definitions in FRI, with a notable distinction: $l _ { i }$ and $d _ { i }$ are deliberately aligned with typical patterns of other devices rather than being randomized.

• Sequence Replay (SR): SR constructs a set of mask frames, $P F _ { \mathrm { S R } } { = } \{ P F _ { \mathrm { F R _ { 1 } } } , . . . , P F _ { \mathrm { F R _ { i } } } \}$ , each conforming to the FR definition. SR aims to duplicate the behavioral patterns of non-target devices.

• Frame Clone (FC): FC constructs a mask frame, $P F _ { \mathrm { F C } }$ structurally similar to FRI. Its key feature is precise SN alignment with the concurrent authentic frame, hindering the attacker’s inference of that frame’s length and direction.

• Sequence Reshaping (SRe): SRe constructs a predefined set of mask frames, $P F _ { \mathrm { S R e } }$ , and injects them regardless of traffic variations. It aims to mislead the attacker’s fingerprinting from authentic frames to this invariant set.

2) Strategy Exploration: The essence of strategy exploration lies in identifying the optimal mapping between traffic states and corresponding mask frame generation strategies. However, the vast and complex traffic state space makes direct exploration infeasible.

To address this, AirMask integrates the advanced reinforcement learning, Rainbow [28], enabling effective and efficient strategy exploration. Its defense can be formulated as a series of decision-making steps: $\lambda = \{ S , { \mathcal { A } } , { \mathcal { R } } , S _ { n x t } \}$

State: The state space is defined as $S = \{ s _ { t } \}$ , where $s _ { t }$ denotes the PW at time t. Instead of directly using authentic and mask frames, $s _ { t }$ combines authentic frames with executed actions. This approach simplifies state representation and reduces the size of $s _ { t } ,$ , as one action may yield multiple mask frames.

Action: $\cal A = \{ a _ { t } \}$ denotes the set of all actions available in state $s _ { t } ,$ including six mask frame generation strategies (i.e., FRI, SRI, FR, SR, FC, and SRe), as well as no action.

Agent: The agent selects the optimal action $a _ { t }$ based on the current state $s _ { t } ,$ aiming to maximize the cumulative reward.

Reward: $r _ { s _ { t } , a _ { t } }$ denotes the immediate feedback obtained by executing $a _ { t }$ in state $s _ { t } .$ , derived from the benefits and costs of the mask frame generation strategy. It is calculated as

$$
\begin{array}{l} r _ {s _ {t}, a _ {t}} = \operatorname{Gain} (s _ {t}, a _ {t}) - \alpha \cdot \operatorname{Cost} (s _ {t}, a _ {t}) \\ = \left[ \sum_ {t = 1} ^ {T} \{\Psi (\operatorname{E} (P W _ {t})) - \Psi (\operatorname{E} (P W _ {t}), P F _ {t}) \} \right] - \alpha \cdot \sum_ {t = 1} ^ {T} P F _ {t}, \end{array}\tag{6}
$$

where ${ \mathrm { G a i n } } ( s _ { t } , a _ { t } )$ is the reduction in classifier accuracy induced by $a _ { t } , { \mathrm { C o s t } } ( s _ { t } , a _ { t } )$ is the cost of $a _ { t } ~ ( \mathrm { i . e . }$ , the number of injected mask frames), and $\Psi$ is a fingerprinting classifier (detailed in Section IV-D). Therefore, (1) can be reformulated as

$$
\max \sum_ {t = 1} ^ {T} r _ {s _ {t}, a _ {t}}.\tag{7}
$$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: Mask Frame Generation Strategy Exploration.

Input: predictive PWs
Output: optimized Q

1 define support points Z for reward distribution;
2 initialize: Q over Z, Q' from Q, decision network D,
    priority replay buffer P;

3 for each PW in PWs do
4    S ← (PW, A) ;
5    sample noise εt^w, εt^b for D;
6    generate ξ;
7    if ξ &lt; ε then
8    select a randomly;
9    else
10    select a using D;
11 end
12 execute a;
13 calculate R, S';
14 calculate td error δ for z in Z;
15 store (S, a, R, S', δ) in P with priority p = |δ| + εp;
16 if P is full then
17    sample a batch with P(i) = $\frac{p_i}{P_{\text{sum}}}$;
18    for each (S, a, R, S', δ) in the batch do
19    compute target distribution over Z in S';
20    update P with δ;
21    minimize L(θ) = 
22    E(S, a, R, S')~P [D_KL (T(S, a) || Q(S, a; θ))];
23    end
24    update Q' every c steps;
25 end
26 S ← S';
27 end
</div>

To solve (7), AirMask employs a Q-function to estimate the long-term returns from executing $a _ { t }$ . It further employs a decision network to separate the estimation of returns into state value and action advantage, essentially decomposing the Q-value into

$$
\mathrm{Q} \left(s _ {t}, a _ {t}\right) = \mathrm{V} \left(s _ {t}\right) + \left(\mathrm{A} \left(s _ {t}, a _ {t}\right) - \frac {1}{| A |} \sum_ {a ^ {\prime}} \mathrm{A} \left(s _ {t}, a ^ {\prime}\right)\right).\tag{8}
$$

where $\mathrm { V } ( s _ { t } )$ is the state-value function, $\mathrm { A } ( s _ { t } , a _ { t } )$ is the actionadvantage function, and $a ^ { \prime }$ is a possible next-step action. To prevent Q-value overestimation, AirMask adopts double Qlearning, with the Q-value updated as

$$
\begin{array}{l} \mathrm{Q} (s _ {t + 1}, a _ {t + 1}) \leftarrow \mathrm{Q} (s _ {t}, a _ {t}) \\ \qquad + \eta \left[ \sum_ {i = 1} ^ {n} \gamma^ {i - 1} r _ {t + i} + \gamma^ {n} \max _ {a ^ {\prime}} \{\mathrm{Q} ^ {\prime} (s _ {t + n}, a ^ {\prime}) - \mathrm{Q} (s _ {t}, a _ {t}) \} \right] \end{array}\tag{9}
$$

where $\mathrm { Q } ^ { \prime }$ denotes the estimation from the target Q network, $\eta$ is the learning rate, γ is the discount factor, and n is the learning step. The strategy exploration algorithm adopts a single-layer RL paradigm, which emphasizes strategy learning while maintaining randomness in the injected mask frames, as detailed in Algorithm 1.

Mask frames generated by the selected strategy must be camouflaged prior to over-the-air injection.

<table><tr><td>2 Byte</td><td>2 Byte</td><td>6 Byte</td><td>6 Byte</td><td>6 Byte</td><td>2 Byte</td><td></td><td>4 Byte</td></tr><tr><td>Frame Control</td><td>Duration ID</td><td>Address 1</td><td>Address 2</td><td>Address 3</td><td>Frag. No. Seq. No.</td><td>Frame Body</td><td>FCS</td></tr></table>

Fig. 6. The structure of an 802.11 wireless frame.

## C. Mask Frame Camouflage

To achieve camouflage at the protocol layer, we modify the fields and sequential states of mask frames. Then, we inject them into the air using a multi-antenna mechanism.

1) Modifying Protocol Fields: It is essential to ensure the consistency of both the protocol specifications and logical sequence (i.e., sequence number) of mask frames. Fig. 6 illustrates the structure of a typical 802.11 wireless frame. We modify the protocol fields that are highlighted in yellow.

\- MAC Address: Frames with identical MAC addresses are typically assumed to originate from the same device. Thus, mask frames must match the receiver, sender, and transmitter MAC addresses of the corresponding authentic ones.

\- Frame Length and Direction: The frame direction is altered by swapping the sender and receiver MAC addresses, and the frame length is adjusted by appending a random sequence of characters to the payload.

Sequence Number: Since SNs are assigned sequentially, any mismatch between a mask frame’s SN and the device’s ongoing SN sequence may expose anomalies. Therefore, AirMask continuously tracks the sequence of current communications and inject mask frames that adhere to this sequence. However, most NICs automatically reset the SN of the initial 802.11 frame to 0 via a built-in overwrite mechanism. To overcome this issue, we modify the NIC driver [29] to flexibly assign SNs to mask frames.

2) Multi-Antenna Frame Transmission: Differences in NIC architectures lead to diverse physical characteristics of wireless frames [30], [31], [32]. To emulate such diversity, we propose a multi-antenna mask frame transmission scheme. The key idea is to employ heterogeneous antennas to inject mask frames, creating a complex physical characteristic distribution that overlaps with authentic frames. As illustrated in Fig. 9(b), AirMask is extended with distributed defense nodes, termed MaskNodes, each equipped with multiple antennas of diverse structures and transmission characteristics. For each mask frame, AirMask strategically selects a MaskNode-antenna pair for injection.

• Antenna Diversity Modeling: The physical characteristics of frames from IoT device a are denoted as $y _ { a } ( t )$ , with a probability density function $\mathrm { P } _ { a } ( t )$ . The physical characteristics of mask frames are denoted as $\left\{ y _ { \zeta _ { 1 } } ( t ) , \ldots , y _ { \zeta _ { N } } ( t ) \right\}$ , with probability density functions $\{ \mathrm { P } _ { \zeta _ { 1 } } ( t ) , \cdot \cdot \cdot , \mathrm { P } _ { \zeta _ { N } } ( t ) \}$ . Thus, the physical characteristics observed by the attacker follow a mixture distribution as

$$
y _ {\text { mix }} (t) = \omega_ {a} y _ {a} (t) + \sum_ {i = 1} ^ {N} \omega_ {\zeta_ {i}} y _ {\zeta_ {i}} (t),\tag{10}
$$

where N is the number of antennas, $\omega _ { a }$ is the proportion of authentic frames, and $\omega _ { \zeta _ { i } }$ is the proportion of mask frames transmitted by the $i ^ { t h }$ antenna. The probability density function

of $y _ { \mathrm { m i x } } ( t )$ is

$$
\mathrm{P} _ {\text { mix }} (t) = \omega_ {a} \mathrm{P} _ {a} (t; r _ {a}, d _ {a}, e) + \sum_ {i = 1} ^ {N} \omega_ {\zeta_ {i}} \mathrm{P} _ {\zeta_ {i}} (t; r _ {\zeta_ {i}}, d _ {\zeta_ {i}}, e),\tag{11}
$$

where $r$ is the antenna characteristic, d is the antenna–attacker distance, and e is the channel noise.

The defender can adopt two multi-antenna optimization strategies: i) homogeneous camouflage, where each antenna generates $y _ { \zeta _ { i } } ( t )$ resembling $y _ { a } ( t )$ ; and ii) heterogeneous camouflage, where antennas generate distinct $y _ { \zeta _ { i } } ( t )$ , forming a heterogeneous $y _ { \mathrm { m i x } } ( t )$ . However, homogeneous camouflage is impractical due to uncontrollable channel variations. The probability density function of the mixture frames’ physical characteristics observed by attackers is

$$
\begin{array}{l} \tilde {\mathrm{P}} _ {\text {mix}} (t) = n (t) + h (t; \theta) * \\ \left[ \omega_ {a} \mathrm{P} _ {a} (t; r _ {a}, d _ {a}, e) + \sum_ {i = 1} ^ {N} \frac {\omega_ {\zeta_ {i}}}{| \det A _ {i} |} \mathrm{P} _ {\zeta_ {i}} ^ {0} \left(A _ {i} ^ {- 1} (t - w _ {\zeta_ {i}})\right) \right], \end{array}\tag{12}
$$

where $h ( t ; \theta )$ denotes the channel response, $n ( t )$ denotes the noise, $\omega _ { \zeta _ { i } }$ denotes the translation shift, and $A _ { i }$ denotes the amplitude scaling matrix. In contrast, the heterogeneous strategy injects mask frames with diverse physical characteristics, reducing the attacker’s confidence in identifying authentic ones. Its diversity can be evaluated by the entropy of the mixture frames physical characteristics.

$$
\mathrm{H} (\tilde {\mathrm{P}} _ {\mathrm{mix}} (t)) = - \int \tilde {\mathrm{P}} _ {\mathrm{mix}} (t) \log \tilde {\mathrm{P}} _ {\mathrm{mix}} (t) d t.\tag{13}
$$

• Factors Influencing Diversity: The diversity of physical characteristics in mask frames is influenced by:

i) Number ofAntennas (N): As N increases, $\mathrm { I } ( \tilde { \mathrm { P } } _ { \mathrm { m i x } } ( t ) )$ also increases, indicating an improvement in diversity.

ii) Inter-Antenna Heterogeneity (r): Larger inter-antenna differences enhance the diversity of physical characteristics. (13) can be decomposed into the entropies of constituent signals and their divergence contributions as

$$
\mathrm{H} (\tilde {\mathrm{P}} _ {\text { mix }} (t)) \approx \sum_ {i = 1} ^ {N} \omega_ {\zeta_ {i}} \mathrm{H} (\mathrm{P} _ {\zeta_ {i}}) + \mathrm{H} (\omega) + \Delta \mathrm{H},\tag{14}
$$

where the first term represents the total entropy of physical characteristics of multiple antennas, the second represents the entropy of weights, and the third is the divergence between physical characteristics, i.e., $\begin{array} { r } { \Delta \mathrm { H } { = } \sum _ { i < j } { \omega _ { \zeta _ { i } } \omega _ { \zeta _ { j } } D _ { \mathrm { K L } } ( \tilde { \mathrm { P } } _ { \zeta _ { i } } \| \tilde { \mathrm { P } } _ { \zeta _ { j } } ) } } \end{array}$ The structural difference across multiple antennas results in transformed distributions: $\begin{array} { r } { \tilde { \mathrm { P } } _ { \zeta _ { i } } ( t ) = \frac { 1 } { \lvert \operatorname* { d e t } A _ { i } \rvert } \tilde { \mathrm { P } } _ { \zeta _ { i } } ^ { 0 } \big ( A _ { i } ^ { - 1 } ( t - w _ { \zeta _ { i } } ) \big ) } \end{array}$ Greater variation in A<sub>i</sub> and $\omega _ { \zeta }$ increases $D _ { \mathrm { K L } } ( \tilde { \mathrm { P } } _ { \zeta _ { i } } \| \tilde { \mathrm { P } } _ { \zeta _ { j } } )$ , and thus, a higher $\mathrm { H } ( \tilde { \mathrm { P } } _ { \mathrm { m i x } } ( t ) )$

iii) Relative Distance Between Antennas and Attackers (d): Relative to IoT devices, antennas located closer to attackers provide stronger diversity. Based on the path loss model $y _ { i } =$ $y _ { 0 } - 1 0 \alpha \log _ { 1 0 } ( d _ { i } / d _ { 0 } )$ , a decrease in $d _ { i }$ leads to an increase in $y _ { i } .$ , thereby yielding a more concentrated $\tilde { P } _ { \zeta _ { i } }$ . Consequently, the divergence between antennas, $D _ { \mathrm { K L } } ( \tilde { \mathrm { P } } _ { \zeta _ { i } } \| \tilde { \mathrm { P } } _ { \zeta _ { j } } )$ , rises, which in turn elevates $\mathrm { H } ( \tilde { \mathrm { P } } _ { \mathrm { m i x } } ( t ) )$ ).

![](images/aefad037a7dee188d574e765c795363a3e69f339d4c518478deb6d6c6b8a10c2.jpg)  
Fig. 7. The impact of $N , r ,$ d on the mixture frames’ entropy.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2: Multi-Antenna Scheduling.

Input: antennas  $Z = \{\zeta_{1}, \ldots, \zeta_{N}\}$ , partial inversion ratio  $\varrho = 0.4$ ;

Output: antenna configuration  $C = \{c_{1}, \ldots, c_{n}\}$ ,  $c_{i} \in \{0, 1\}$ ;

initialize C;

while True do

 $\chi \leftarrow \text{random}(0, 1)$ ;

if  $\chi &lt; 0.5$  then

| partially invert C;

else

| fully invert C;

 $t \leftarrow \text{random}(5s, 10s)$ ;

wait(t);

end
</div>

We conduct simulations using GNU Radio [33] to evaluate the impact of N, r, and d on the physical signal diversity of mask frames. The results are shown in Fig. 7. First, mask frames’ physical signal diversity improves with more antennas. Second, by varying the noise levels and tap configurations across antennas to emulate architectural differences, we observe that greater antenna heterogeneity leads to improved diversity gains. Finally, antennas placed closer to the device yield better diversity. Further details of this experiment are provided in Appendix B-B, available online. • Multi-Antenna Scheduling: We design a plug-and-play multi-antenna scheduling strategy that operates independently ofIoT devices. For each mask frame, AirMask retrieves the dynamic antenna configuration and randomly selects an available antenna for injection. To enhance physical diversity, a heterogeneous set of antennas with unequal gains (0-10 dBi) is employed. The scheduling steps are detailed in Algorithm 2.

## D. Fingerprint-Aware Assessment

As mask frames are injected, the agent continuously assesses and refines their effectiveness in masking fingerprints. In addition, it updates the fingerprint repository based on historical traffic. To this end, we design a fingerprinting classifier that integrates traffic features across multiple dimensions.

• Hierarchical Feature Extraction: As shown in Fig. 8, we extract traffic features of 802.11 frames from three dimensions.

Frame-Level: Each 802.11 frame is represented as a frame vector (FV) that includes packet length, direction, and timing. The packet length is normalized to [0, 1]; the direction is binary: 0 for sent and 1 for received; and the timing denotes inter-frame intervals. Sequence-Level: To capture the short-term structural patterns often repeated in an IoT device’s frame sequences, we merge adjacent FV s into a sequence vector (SV ).

![](images/d3a80efa3ac7753641450c2a345d91c09ecb5628d70ff03b551b302478f386e2.jpg)  
Fig. 8. Multi-scale feature extraction for assessment.

Window-Level: A window vector (WV) is formed by extracting statistical features within a time window. It comprises 11 dimensions, including total/average lengths, length variance, max/min length, and counts/ratios of sent/received frames.

The assessment agent continuously extracts these threedimensional features from historical IoT traffic to update the fingerprint repository and from obfuscated frames to assess defense effectiveness via a multi-scale classifier.

• Defense Assessment via Multi-Scale Classification: We design a multi-scale fingerprinting classifier to adeptly capture traffic features across multiple time scales. Specifically, a time window $T$ is partitioned into sub-windows, where the ${ \bf { \bar { \rho } } } _ { j } t h$ subwindow at the $i ^ { t h }$ time scale is denoted as $T _ { j } ^ { i }$ . Traffic features within $T _ { j } ^ { i }$ are extracted at the frame, sequence, and window levels, concatenated, and fed into the classifier.

$$
\mathrm{Z} (T _ {j} ^ {i}) = \Psi \Big (F V (T _ {j} ^ {i}), S V (T _ {j} ^ {i}), W V (T _ {j} ^ {i}) \Big),\tag{15}
$$

where Ψ(·) denotes a random forest classifier. Then, we adopt a weighted voting mechanism to aggregate classification results across sub-windows, with each result weighted by its time scale. The device with the highest aggregated score is selected as the final prediction. A larger discrepancy between the predicted and true labels indicates a more effective mask frame generation strategy.

## E. AirMask Implementation

As illustrated in Fig. 9(a), AirMask supports three deployment modes implemented on a Raspberry Pi 4B.

• Integrated Mode: AirMask is integrated within the AP, which is emulated using a Raspberry Pi. AirMask can observe the TCP/IP traffic of all connected IoT devices.

• TAP Mode: Deployed between the AP and the external network via a TAP device, AirMask is capable of observing both inbound and outbound TCP/IP traffic of the AP.

• Air Mode: Placed within the signal range of the AP, the Raspberry Pi running AirMask is able to observe wireless traffic transmitted by IoT devices.

The Raspberry Pi 4B runs Ubuntu 20.04 with kernel 5.8 and is equipped with AR9271-based NICs. We have custom compiled both the Ubuntu kernel and the NIC driver [29] to support mask frame camouflage and injection. The AP model is TL-WDR5620. As shown in Fig. 9(b), MaskNode connects wirelessly to AirMask via the VirtualHere protocol [34], enabling flexible deployment within WiFi range. Each MaskNode features a multi-antenna array with detachable antennas of diverse structures and transmission power.

## V. EVALUATION

Our evaluation aims to answer four research questions:

\- RQ1: How effective is AirMask in defending IoT devices against IWF attacks?

\- RQ2: Can attackers defeat AirMask by retraining their fingerprinting models using defended traffic that incorporates both mask frames and authentic frames?

\- RQ3: How well does AirMask perform in each of the three deployment modes?

\- RQ4: How does AirMask impact wireless network and protected IoT devices?

## A. Testbed and Datasets

To answer these research questions, we conduct extensive evaluations of AirMask using three datasets:

UNSW dataset [35] is a public dataset containing six months of traffic traces from 28 distinct IoT devices, including cameras, lights, motion sensors, etc. The dataset comprises 60 PCAP files with a total size of 26.7 GB.

Mon(IoT)r dataset [36] is also a public dataset collected by the Mon(IoT)r laboratory, including 55 distinct IoT devices. It contains over 40 behavioral traffic instances per device and over 100 hours of idle traffic, totaling 12.7 GB in size.

IoTrace dataset is collected from our testbed, namely IoTrace, as shown in Fig. 9(c). The testbed includes 22 distinct IoT devices, encompassing cameras, smart speakers, smart plugs, sensors, etc. The dataset includes both the two months of idle traffic and 53 types of behavioral traffic from these devices.

## B. IoT Wireless Fingerprinting Attacks

Existing IWF attacks exploit four types of traffic features: i) packet length and direction, ii) packet sequence, iii) spatiotemporal features, and iv) statistical features. We evaluate five popular IWF attacks that cover all four types.

PINGPONG [12] fingerprints IoT devices by analyzing their request–response packets with external network.

ByteIoT [37] leverages the frequency distribution of bidirectional packet lengths. It uses a KNN classifier with a customized similarity metric to classify IoT traffic.

Shahid et al. [38] identify IoT devices using the spatiotemporal features of each bidirectional flow, specifically the lengths of the initial n packets and their time intervals.

Kolcun et al. [39] employ statistical features to characterize packet dynamics over short time intervals, including total and average packet lengths, as well as length deviation.

Liu et al. [40] propose a deep convolutional neural network to fingerprint devices using sequences of packet lengths.

## C. Baseline Defenses

We compare AirMask with two existing IWF defenses: Link Layer GAN [20] and Traffic Replay [26]. We also introduce a baseline defense, i.e., Frame Flooding for comparison.

![](images/4f3bdcdb9054c00475915969b17553aa176a81057d634b35e0009d44bd5c6283.jpg)  
(a) AirMask deployment.

![](images/6b08ce9aa7dc10222ce9f6446e50b83317b96a48b65c90b94aef58526866f657.jpg)  
(b) MaskNode.

![](images/018b7e4e17344f983293986920f653587a7bc3018a3532ca8767bf758b74f616.jpg)  
(c) IoTrace testbed.  
Fig. 9. Illustration of (a) three deployment modes of AirMask, (b) MaskNode that connects wirelessly to AirMask and injects mask frames indistinguishable to attackers, and (c) IoTrace testbed that collects wireless traffic from IoT devices.

TABLE I  
EVALUATING AirMask AND OTHER DEFENSES AGAINST DEVICE TYPE IDENTIFICATION

<table><tr><td rowspan="2">Dataset</td><td>Attack</td><td colspan="2">PINGPONG</td><td colspan="2">ByteIoT</td><td colspan="2">Shahid et al.</td><td colspan="2">Kolcun et al.</td><td colspan="2">Liu et al.</td><td rowspan="2">Defense Cost</td></tr><tr><td>Metric</td><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td></tr><tr><td rowspan="7">UNSW</td><td>No Defense</td><td>0.840</td><td>0.697</td><td>0.729</td><td>0.964</td><td>0.854</td><td>0.806</td><td>0.856</td><td>0.832</td><td>0.889</td><td>0.865</td><td>0%</td></tr><tr><td>Frame Flooding (Heavy)</td><td>0.000</td><td>0.000</td><td>0.111</td><td>0.178</td><td>0.021</td><td>0.100</td><td>0.037</td><td>0.027</td><td>0.067</td><td>0.065</td><td>2000%</td></tr><tr><td>Frame Flooding (Moderate)</td><td>0.014</td><td>0.000</td><td>0.165</td><td>0.201</td><td>0.036</td><td>0.127</td><td>0.121</td><td>0.046</td><td>0.072</td><td>0.080</td><td>1000%</td></tr><tr><td>Frame Flooding (Light)</td><td>0.103</td><td>0.013</td><td>0.316</td><td>0.223</td><td>0.189</td><td>0.177</td><td>0.205</td><td>0.169</td><td>0.177</td><td>0.186</td><td>500%</td></tr><tr><td>Link Layer GAN</td><td>0.378</td><td>0.075</td><td>0.357</td><td>0.278</td><td>0.196</td><td>0.127</td><td>0.225</td><td>0.134</td><td>0.127</td><td>0.130</td><td>500%</td></tr><tr><td>Traffic Replay</td><td>0.731</td><td>0.088</td><td>0.388</td><td>0.226</td><td>0.240</td><td>0.164</td><td>0.149</td><td>0.157</td><td>0.116</td><td>0.099</td><td>500%</td></tr><tr><td>AirMask</td><td>0.040</td><td>0.003</td><td>0.231</td><td>0.220</td><td>0.065</td><td>0.090</td><td>0.146</td><td>0.117</td><td>0.099</td><td>0.080</td><td>500%</td></tr><tr><td rowspan="7">Mon(IoT)r</td><td>No Defense</td><td>0.914</td><td>0.646</td><td>0.820</td><td>0.911</td><td>0.847</td><td>0.834</td><td>0.813</td><td>0.792</td><td>0.807</td><td>0.801</td><td>0%</td></tr><tr><td>Frame Flooding (Heavy)</td><td>0.126</td><td>0.220</td><td>0.162</td><td>0.168</td><td>0.021</td><td>0.064</td><td>0.054</td><td>0.095</td><td>0.084</td><td>0.076</td><td>2000%</td></tr><tr><td>Frame Flooding (Moderate)</td><td>0.109</td><td>0.025</td><td>0.212</td><td>0.248</td><td>0.028</td><td>0.065</td><td>0.092</td><td>0.121</td><td>0.115</td><td>0.097</td><td>1000%</td></tr><tr><td>Frame Flooding (Light)</td><td>0.118</td><td>0.039</td><td>0.338</td><td>0.312</td><td>0.113</td><td>0.101</td><td>0.171</td><td>0.129</td><td>0.162</td><td>0.131</td><td>500%</td></tr><tr><td>Link Layer GAN</td><td>0.276</td><td>0.071</td><td>0.348</td><td>0.296</td><td>0.168</td><td>0.107</td><td>0.174</td><td>0.181</td><td>0.190</td><td>0.145</td><td>500%</td></tr><tr><td>Traffic Replay</td><td>0.645</td><td>0.272</td><td>0.281</td><td>0.324</td><td>0.279</td><td>0.163</td><td>0.198</td><td>0.178</td><td>0.159</td><td>0.149</td><td>500%</td></tr><tr><td>AirMask</td><td>0.048</td><td>0.003</td><td>0.217</td><td>0.259</td><td>0.030</td><td>0.037</td><td>0.139</td><td>0.074</td><td>0.095</td><td>0.074</td><td>500%</td></tr><tr><td rowspan="8">IoTrace</td><td>No Defense</td><td>0.874</td><td>0.644</td><td>0.844</td><td>0.923</td><td>0.894</td><td>0.885</td><td>0.864</td><td>0.838</td><td>0.838</td><td>0.840</td><td>0%</td></tr><tr><td>Frame Flooding (Heavy)</td><td>0.000</td><td>0.000</td><td>0.103</td><td>0.182</td><td>0.028</td><td>0.100</td><td>0.041</td><td>0.104</td><td>0.041</td><td>0.047</td><td>2000%</td></tr><tr><td>Frame Flooding (Moderate)</td><td>0.000</td><td>0.000</td><td>0.144</td><td>0.189</td><td>0.044</td><td>0.099</td><td>0.113</td><td>0.108</td><td>0.098</td><td>0.086</td><td>1000%</td></tr><tr><td>Frame Flooding (Light)</td><td>0.000</td><td>0.000</td><td>0.252</td><td>0.403</td><td>0.084</td><td>0.104</td><td>0.178</td><td>0.107</td><td>0.216</td><td>0.174</td><td>500%</td></tr><tr><td>Link Layer GAN</td><td>0.068</td><td>0.001</td><td>0.377</td><td>0.367</td><td>0.104</td><td>0.157</td><td>0.134</td><td>0.149</td><td>0.201</td><td>0.181</td><td>500%</td></tr><tr><td>Traffic Replay</td><td>0.288</td><td>0.012</td><td>0.429</td><td>0.345</td><td>0.181</td><td>0.215</td><td>0.189</td><td>0.165</td><td>0.173</td><td>0.169</td><td>500%</td></tr><tr><td>AirMask</td><td>0.000</td><td>0.000</td><td>0.130</td><td>0.196</td><td>0.030</td><td>0.043</td><td>0.098</td><td>0.099</td><td>0.134</td><td>0.102</td><td>500%</td></tr><tr><td>AirMask (Online)</td><td>0.000</td><td>0.002</td><td>0.124</td><td>0.183</td><td>0.038</td><td>0.048</td><td>0.105</td><td>0.101</td><td>0.131</td><td>0.095</td><td>500%</td></tr></table>

Link Layer GAN comprises a generator and a discriminator. Once trained, the generator is used to produce forged traffic, which is then injected into the original data.

Traffic Replay injects traffic patterns from other devices to confuse attackers. For example, blending speaker traffic into smart-plug traffic can hinder device-type inference.

Frame Flooding injects a significant volume of randomly forged frames at heavy, moderate, or light levels.

## D. AirMask Vs. Baseline Defenses

## 1) Defending Against Device Type Identification:

• Experimental Setup: Since baseline defenses operate exclusively in offline mode, we first evaluate both the baselines and AirMask in offline settings, followed by evaluating AirMask independently in the online scenario. In the offline settings, we use the UNSW, Mon(IoT)r, and IoTrace datasets. Traffic from all three datasets is divided into training and testing sets with a 7:3 ratio to evaluate the effectiveness of five IWF attacks under different scenarios: no defense, Link Layer GAN, Traffic Replay, Frame Flooding, and AirMask. We use the IoTrace testbed for online evaluation. The evaluation is conducted using four key metrics: precision, recall, and F1-score for IWF attacks, as well as defense cost, which is quantified by the ratio of mask frames to authentic ones.

• Results: As shown in Table I, AirMask effectively mitigates all five IWF attacks, with its efficacy validated across all three datasets. Specifically, on the UNSW dataset, the average precision and recall of five IWF attacks drop from 0.834/0.833 to 0.096/0.054, respectively. On Mon(IoT)r, they decrease from 0.84/0.797 to 0.106/0.089, and on IoTrace, from 0.863/0.826 to 0.077/0.076. Across various attacks and datasets, AirMask consistently outperforms both Link Layer GAN and Traffic Replay in defense effectiveness. Additionally, it surpasses Frame

![](images/7823e006e23d2c26d0ba74e67f8eb274dc435166a8b94b6f9be05481afaca458.jpg)  
Fig. 10. Evaluating Link Layer GAN, Traffic Replay, and AirMask against device type identification across various defense costs. In the evaluation matrix, each row corresponds to a dataset, while each column denotes an IWF attack.

![](images/e4b55e68598240b3bde8f751c9387ab99e940a1f5f7550257e395791c4dabce3.jpg)

![](images/cefb298d4831111cf6a7730f9dc769853d4e803df8712fe7c28fe2feb70e4b61.jpg)  
Fig. 11. Evaluating AirMask and other defenses against device behavior identification.

![](images/daf1bb700f8e41db6543104713f2f4a8ea27e84a19bba84a46c1f703b9d211fc.jpg)

![](images/6de036a40e2f063c47a94e25b44be9a244d685b98661fb50af34ab25f9faec79.jpg)

Flooding at its light and moderate levels. With AirMask deployed, the average precision and recall of five IWF attacks drop to 0.1 and 0.093, respectively—significantly lower than the 0.175 and 0.151 of Frame Flooding at its light level (with a defense cost of 500%). While Frame Flooding outperforms AirMask at its heavy level (with a defense cost of 2000%), achieving precision and recall of 0.06 and 0.095, this high volume of forged frames risks saturating network capacity and introducing device delays (as detailed in Section V-G).

Fig. 10 illustrates how the effectiveness of AirMask and other baseline defenses improves as the defense cost increases. The results indicate that AirMask consistently outperforms other defenses across all defense costs and for all IWF attacks. For instance, at a defense cost of 500%, Link Layer GAN and Traffic Replay yield average F1-scores of 0.14 and 0.172 for five attacks, respectively, while AirMask reduces the average F1-score to just 0.068.

We evaluate AirMask in both online and offline modes using the IoTrace testbed, with the results shown in Table I. Due to the inherent overhead of NIC driver and hardware processing, there is an unavoidable frame injection delay. Our measurements on the Raspberry Pi indicate that this delay is approximately 30 ms. AirMask offsets this delay through the packet-frame prediction module. In offline mode, AirMask reduces the average precision and recall of five IWF attacks to 0.078 and 0.088, respectively; similarly, in online mode, the average precision drops to 0.08 and recall to 0.086.

2) Defending Against Device Behavior Identification:

• Experimental Setup. We manually trigger 53 device behaviors on the IoTrace testbed for evaluation, covering four IWF attacks: PINGPONG [12], Shahid et al. [38], Kolcun et al. [39], and Liu et al. [40]. ByteIoT [37] is excluded because it relies on broad, device-level packet length distributions and cannot capture fine-grained behaviors. Device behavior evaluation is a binary classification task that determines whether a traffic trace matches a specific behavior.

• Results: As shown in Fig. 11, when the defense cost increases from 10% to 500%, the effectiveness of Link Layer GAN, Traffic Replay, Frame Flooding (Light), and AirMask all improves. However, as the defense cost increases, Link Layer GAN continues to exhibit limited effectiveness against Ping-Pong, and Traffic Replay fails to further reduce the identification performance of Kolcun et al. In contrast, AirMask exhibits superior performance across various attacks and defense costs. For example, at a defense cost of 500%, AirMask reduces the F1-score of PINGPONG from 0.77 to 0.281; for Shahid et al. from 1 to 0.183; for Kolcun et al. from 0.886 to 0.184; and for Liu et al. from 0.833 to 0.238.

Answer to RQ1: AirMask effectively thwarts IWF attacks, reducing device type identification precisions from 0.846 to 0.1 and recall from 0.819 to 0.093, and lowering the behavior identification F1-score from 0.872 to 0.221.

TABLE II  
EVALUATING AirMask AGAINST RETRAINING ATTACKS

<table><tr><td rowspan="2">Dataset</td><td>Attack</td><td colspan="2">PINGPONG</td><td colspan="2">ByteIoT</td><td colspan="2">Shahid et al.</td><td colspan="2">Kolcun et al.</td><td colspan="2">Liu et al.</td></tr><tr><td>Metric</td><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td><td>Precision</td><td>Recall</td></tr><tr><td rowspan="3">UNSW</td><td>No Defense</td><td>0.840</td><td>0.697</td><td>0.729</td><td>0.964</td><td>0.854</td><td>0.806</td><td>0.856</td><td>0.832</td><td>0.889</td><td>0.865</td></tr><tr><td>AirMask Defense</td><td>0.040</td><td>0.003</td><td>0.231</td><td>0.220</td><td>0.065</td><td>0.090</td><td>0.146</td><td>0.117</td><td>0.099</td><td>0.080</td></tr><tr><td>Retraining Attack</td><td>0.733</td><td>0.045</td><td>0.237</td><td>0.207</td><td>0.461</td><td>0.481</td><td>0.140</td><td>0.147</td><td>0.178</td><td>0.182</td></tr><tr><td rowspan="3">Mon(IoT)r</td><td>No Defense</td><td>0.914</td><td>0.646</td><td>0.820</td><td>0.911</td><td>0.847</td><td>0.834</td><td>0.813</td><td>0.792</td><td>0.807</td><td>0.801</td></tr><tr><td>AirMask Defense</td><td>0.048</td><td>0.003</td><td>0.217</td><td>0.259</td><td>0.030</td><td>0.037</td><td>0.139</td><td>0.074</td><td>0.095</td><td>0.074</td></tr><tr><td>Retraining Attack</td><td>0.835</td><td>0.104</td><td>0.254</td><td>0.283</td><td>0.476</td><td>0.466</td><td>0.191</td><td>0.089</td><td>0.109</td><td>0.111</td></tr><tr><td rowspan="3">IoTrace</td><td>No Defense</td><td>0.874</td><td>0.644</td><td>0.844</td><td>0.923</td><td>0.894</td><td>0.885</td><td>0.864</td><td>0.838</td><td>0.838</td><td>0.840</td></tr><tr><td>AirMask Defense</td><td>0.000</td><td>0.000</td><td>0.130</td><td>0.196</td><td>0.030</td><td>0.043</td><td>0.098</td><td>0.099</td><td>0.134</td><td>0.102</td></tr><tr><td>Retraining Attack</td><td>0.866</td><td>0.058</td><td>0.127</td><td>0.088</td><td>0.416</td><td>0.345</td><td>0.108</td><td>0.199</td><td>0.154</td><td>0.146</td></tr></table>

## E. Defense Against Retraining Attacks

• Experimental Setup: We evaluate AirMask’s effectiveness against retraining attacks, including three scenarios:

No Defense: Without AirMask’s defense, attackers can capture authentic frames to train a classifier and use it to conduct IWF attacks.

AirMask Defense: Attackers continue to use authentic frames to train a classifier. However, once AirMask is deployed, they will use this classifier to perform IWF attacks on traffic containing a mix of authentic and mask frames.

Retraining Attack: Attackers use both authentic and mask frames to train a classifier, and then use it to launch IWF attacks on traffic containing a mixture of the two.

• Results: Table II shows the performance of five attacks across three scenarios. Without AirMask’s defense, all attacks achieve high precision and recall. However, deploying AirMask markedly reduces their capabilities. Even under retraining, ByteIoT, Shahid et al. Kolcun et al. and Liu et al. show negligible improvement. For example, after retraining, the average precision of Kolcun et al. rises only from 0.128 to 0.146, and the recall from 0.097 to 0.145, both remaining far below the 0.844 and 0.821 achieved without defense.

After retraining, the average precision of PINGPONG increases significantly from 0.03 to 0.811, while its average recall improves only slightly, from 0.002 to 0.069. This trade-off stems from PINGPONG’s algorithmic design. When AirMask distorts high-frequency packet sequences, PINGPONG shifts to relying on less frequent ones as alternative fingerprints. However, these less-frequent sequences occur rarely in the traffic, leading to a limited number of useful fingerprints and, consequently, consistently low recall.

Answer to RQ2: AirMask mitigates retraining attacks, reducing the average precision and recall of IWF attacks from 0.846 and 0.819 to 0.352 and 0.197, respectively.

## F. Defense Under Three Deployment Modes

• Experimental Setup: We evaluate the effectiveness of Air-Mask across its three deployment modes. In Integrated mode, it captures the TCP/IP traffic from all IoT devices connected to the AP; in TAP mode, it captures the TCP/IP traffic exchanged between the AP and the Internet; and in Air mode, it captures 802.11 traffic over the air.

• Results: Fig. 12 demonstrates that AirMask achieves impressive defense effectiveness across all deployment modes. For instance, at a defense cost of 500%, AirMask reduces the average F1-score of five attacks to 0.051, 0.08, and 0.082 in Integrated, TAP, and Air modes, respectively. The Integrated mode is the most effective, as AirMask has full visibility into each device’s TCP/IP traffic. In contrast, the TAP mode is easy to deploy, requiring no modifications to the AP, only the addition of a TAP device. However, its effectiveness is slightly reduced, with the average F1-score of attacks being 0.08. This reduction is primarily due to the loss of visibility into intra-LAN traffic (e.g., SSDP). While Air mode supports flexible deployment within the AP’s signal range, its effectiveness is limited by reduced visibility into TCP/IP packets, as they are encapsulated within 802.11 data frames. Nonetheless, AirMask achieves performance in the Air mode comparable to that of the TAP mode, with the average F1-score of attacks being 0.082.

Answer to RQ3: AirMask demonstrates robust performance across all three deployment modes. In Integrated, TAP, and Air modes, it reduces the average F1-score of attacks from 0.832 to 0.051, 0.08, and 0.082, respectively.

## G. Impact on Network and IoT Device

• Experimental Setup: We evaluate the impact of AirMask on wireless network bandwidth and the operational performance of protected IoT devices. Experiments are conducted on 5 instances of a traffic-intensive IoT device (the DuSmart smart speaker) in a real smart home environment, in order to evaluate the system’s practical overhead. Network bandwidth is measured using the ifstat tool, while device delay is evaluated based on the round-trip time (RTT) of TCP connections. As shown in Fig. 13(c), we use an ACD15P power meter to measure the power consumption of the protected IoT devices. The ACD15P is connected in series between the device power input and its power supply, and records real-time variations in input voltage, current, and power during device operation. We continuously measure device power consumption for 4 hours under two settings: without defense and with AirMask enabled. For each setting, we collect 3,115 power samples.

![](images/635d908ce63bba73823fff7fba5258871e9909cfe1ceac9d69842bec98251d32.jpg)  
Defense Cost (%) - PINGPONG

![](images/c89e7864a6fa7b7932ce42f7b71ad37791e54e710cabc29e83ee8a82a43b29a4.jpg)  
Fig. 12. Evaluating AirMask across its three deployment modes.

![](images/cf810801632f34d2b77fb60e30347f3fec215fa2e7eda845a74bb3e44108e699.jpg)

![](images/82cf6839da0b34ed7577931e0692d882428215dc33ff43d87764be899dc3c65e.jpg)  
Defense Cost (%) - Kolcun et al.

![](images/42c44517313cb195aa191759e13611e7e05777ce63baaf86f7f7b9be364d773b.jpg)

![](images/134f67861586f1201faef720740a20c1898c6596a1530e22f1e28cb91c01a30f.jpg)  
(a) Impact on bandwidth.

![](images/243c8dc80425f78e81d926b9d0a2a71f706170a884704469268f20591f5f7f79.jpg)  
(b) Impact on device delay.

![](images/f17ddeaf577eb7a4ce1f2694711fd4190b92bcbc2afdbd0489364137e871fffc.jpg)

![](images/3b6316892bc712a87edd16718ca51e3b24298e650d071a7772601c78bba39b4f.jpg)  
(c) Device power  
measurement.  
(d) Impact on device power.  
Fig. 13. Impact of mask frames.

• Results: As shown in Fig. 13, AirMask introduces negligible overhead in network bandwidth and device delay. Specifically, increasing the defense cost from 10% to 500% results in only limited bandwidth degradation. When the defense cost remains below 100%, the bandwidth reduction is under 1%. Even at a 500% defense cost, the impact remains modest, with bandwidth decreasing by only 4.7%.

When IoT devices receive mask frames containing indecipherable or incorrectly parsed encrypted payloads, they discard these frames. This process consumes additional computational resources, leading to increased device delay. As shown in Fig. 13(b), the baseline device delay without defense is 23.25 ms. AirMask introduces minimal delay overhead of approximately 2 ms when the defense cost is below 200%. However, as the defense cost increases further, the delay becomes more noticeable. At a 500% defense cost, device delay rises from 23.25 ms to 30.64 ms, representing a 31.8% increase, thereby rendering flooding-based defenses impractical. Since protected IoT devices do not actively transmit additional packets or execute any defense algorithm, their additional power overhead is low and mainly arises from receiving and discarding mask frames. As shown in Fig. 13(d), enabling AirMask only slightly increases device power consumption, by approximately 0.55%. The average device power consumption is 1.988 W in the undefended setting and 1.999 W with AirMask enabled. For an IoT device with a baseline operating power of approximately 2 W, the additional energy consumption introduced by AirMask over 24 hours of continuous operation is only about 0.262 Wh.

Answer to RQ4: AirMask incurs a minimal and manageable impact on network bandwidth, with overhead below 1%, and introduces approximately 2 ms of device delay.

## VI. DISCUSSION

• More Attack Features: Although we have extensively studied the most common features in IWF attacks, attackers may exploit others, such as MAC addresses and novel features.

MAC Addresses: Attackers may attempt to identify mask frames by analyzing protocol fields such as MAC address [41], [42]. However, mask frames replicate the protected device’s MAC address exactly, rendering MAC-based identification ineffective. Moreover, MAC address typically reveals only the NIC vendor, rather than the actual device type.

Novel Features: When attackers use novel features, AirMask can seamlessly integrate them into its built-in fingerprinting classifier to construct targeted countermeasures. If such novel features are unknown to AirMask, the system can also have the potential to structure the feature representations and adjust its defense strategies accordingly, as long as these features fall into feature types of frame, sequence, and window levels.

• Physical-Layer Robustness and Limitations: Physical-layer features such as RSSI [31] and CSI [30] have been used to infer device identity and location [43], [44]. To defend against such channel feature-based attacks, AirMask generates mask frames through coordinated multi-antenna transmission. By introducing temporal and spatial variations in physical-layer features, this design prevents mask frames from forming a stable distribution. The experimental results in Appendix B-C, available online verify that attackers cannot distinguish mask frames from authentic ones using RSSI clustering, RSSI-based trilateration, or CSI subcarrier phase difference analysis, with identification performance close to random guessing.

This does not imply that AirMask can withstand all physical-layer fingerprinting techniques. For example, IQ-based radio-frequency fingerprinting (RFF) may capture stable RF impairments introduced by static defense hardware [45], thereby enabling the identification of mask frames. More precisely, AirMask’s multi-antenna mechanism primarily mitigates channel feature-based filtering, but cannot fully eliminate RF fingerprints associated with the transmitting hardware itself. Nevertheless, IQ-level RFF requires stronger attacker capabilities, including SDR-level IQ acquisition, high signal-to-noise ratio, and stable sampling synchronization. As future work, we will extend physical-layer obfuscation from channel-level diversity to RF-front-end diversity, for example by introducing heterogeneous radios, dynamic transmission scheduling, and controllable RF perturbations.

• More Adaptive Attackers: Attackers can deploy AirMask to collect defended traffic and retrain classifiers. As shown in Section V-E, their identification precision and recall rise from 0.1 and 0.093 to 0.352 and 0.197, respectively. Nevertheless, this enhanced performance remains far below the performance without defense (0.846 and 0.819), demonstrating the remarkable defensive capability of our system. This is mainly attributed to the high randomness inherent in system design. Specifically, even when AirMask employs the same defense strategy, the outcomes can vary across executions. For instance, under the frame random insertion strategy, inserted frames differ in length and direction across executions.

## VII. RELATED WORK

We review recent advances in IWF attacks and defenses.

## A. Fingerprinting Attacks

IWF attacks typically use four types of traffic features: i) packet length and direction, ii) packet sequence, iii) spatiotemporal features, and iv) statistical features. Specifically, Duan et al. [37], [46] used the frequency distribution of packet lengths to identify devices. Dong et al. [13] and Sun et al. [47], on the other hand, employed statistical features of packet lengths as fingerprints. Other studies [12], [48], [49], [50] focus on packet sequence for fingerprinting attacks. For example, Trimananda et al. [12] proposed PINGPONG to automatically extract packet sequences as fingerprints. In addition, some researchers [15], [38], [40], [51], [52], [53], [54], [55] use spatiotemporal features, modeling inter-packet timing dependencies to achieve highprecision identification. For example, Ma et al. [15] pinpointed devices within a NAT by extracting their spatiotemporal traffic features. Zhao et al. [55] analyzed device behaviors by creating a time-series dictionary. Statistical features are also widely studied for device fingerprinting [39], [56], [57], [58], [59]. Kolcun et al. [39] used attributes such as cumulative packet lengths, mean length, and length variability within specified time windows to identify devices. AirMask comprehensively integrates these features and offers high scalability, providing defense against diverse attacks.

## B. Fingerprinting Defenses

Existing defenses generally fall into four categories:

Packet Padding [60], [61], [62] obfuscates packet length by padding extra bytes to original packets. However, this approach requires device-side modifications, whereas AirMask adopts a non-intrusive design that requires no device changes.

VPN Encryption [17], [63], [64] conceals traffic features by encapsulating traffic within an encrypted tunnel. However, such solutions are unsuitable for resource-constrained IoT devices. Comparatively, AirMask is deployed on a standalone defense device, thereby avoiding this limitation.

Traffic Shaping inserts extra packets into traffic to normalize or mimic device traffic patterns [17], [20], [65], [66], [67], but relies on well-labeled training data. In contrast, AirMask explores device-specific obfuscation in a self-supervised manner.

Event Spoofing [26], [68], [69] misleads attackers by simulating device-specific behavioral traffic, but its effectiveness relies on pre-learned device behavior models. In contrast, AirMask operates independently of the protected IoT devices.

## VIII. CONCLUSION

This paper presents AirMask, the first air-to-air defense system against IoT wireless fingerprinting attacks. By eliminating the need for firmware modifications or device cooperation, AirMask enables immediate, scalable deployment across diverse IoT environments. It introduces a closed-loop predictinject-assess framework to overcome three key challenges: i) injection under traffic heterogeneity, ii) injection timing and responsiveness, and iii) injection indistinguishability and resistance. Through device-specific strategy learning, proactive fingerprint prediction, and protocol-layer frame camouflage, AirMask achieves robust and adaptive protection without compromising network functionality. AirMask marks an initial step toward air-to-air IoT privacy protection, paving the way for a scalable and deployable IoT security ecosystem.

## REFERENCES

[1] S. Sinha, “State of IoT 2024: Number of connected IoT devices growing 13% to 18.8 billion globally,” 2024. [Online]. Available: https://iotanalytics.com/number-connected-iot-devices

[2] “Number of Internet of Things (IoT) connections worldwide from 2022 to 2023, with forecasts from 2024 to 2033,” 2024. [Online]. Available: https:// www.statista.com/statistics/1183457/iot-connected-devices-worldwide/

[3] H. Touqeer, S. Zaman, R. Amin, M. Hussain, F. Al-Turjman, and M. Bilal, “Smart home security: Challenges, issues and solutions at different IoT layers,” J. Supercomputing, vol. 77, no. 12, pp. 14053–14089, 2021.

[4] T. Malche and P. Maheshwary, “Internet of things (IoT) for building smart home system,” in Proc. IEEE Int. Conf I-SMAC (IoT Social, Mobile, Analytics Cloud), 2017, pp. 65–70.

[5] W. Z. Khan, M. Rehman, H. M. Zangoti, M. K. Afzal, N. Armi, and K. Salah, “Industrial Internet of Things: Recent advances, enabling technologies and open challenges,” Comput. Elect. Eng., vol. 81, 2020, Art. no. 106522.

[6] B. Bajic, A. Rikalovic, N. Suzic, and V. Piuri, “Industry 4.0 implementation challenges and opportunities: A managerial perspective,” IEEE Syst. J., vol. 15, no. 1, pp. 546–559, Mar. 2021.

[7] Q. Tian et al., “New security mechanisms of high-reliability IoT communication based on radio frequency fingerprint,” IEEE Internet Things J., vol. 6, no. 5, pp. 7980–7987, Oct. 2019.

[8] Q. Xu, R. Zheng, W. Saad, and Z. Han, “Device fingerprinting in wireless networks: Challenges and opportunities,” IEEE Commun. Surv. Tut., vol. 18, no. 1, pp. 94–104, Firstquarter 2016.

[9] B. Nolan, “Security camera startup wyze apologizes for a breach that allowed 13,000 customers to see into other people’s homes,” 2024. [Online]. Available: https://www.businessinsider.com/wyze-camera-breachcustomers-security-homes-2024-2

[10] “St. Lawrence health reduces IoT and IoMT device security risk through prioritization and mitigation,” 2025. [Online]. Available: https://www. intelashealth.com/case-study/st-lawrence

[11] L. C. C. Desmond, C. C. Yuan, T. C. Pheng, and R. S. Lee, “Identifying unique devices through wireless fingerprinting,” in Proc. 1st ACM Conf. Wireless Netw. Secur., 2008, pp. 46–55.

[12] R. Trimananda, J. Varmarken, A. Markopoulou, and B. Demsky, “Packetlevel signatures for smart home devices,” in Proc. Netw. Distrib. Syst. Secur. Symp., vol. 2020, 2020, pp. 1–18.

[13] S. Dong, Z. Li, D. Tang, J. Chen, M. Sun, and K. Zhang, “Your smart home can’t keep a secret: Towards automated fingerprinting of IoT traffic,” in Proc.15th ACM Asia Conf. Comput. Commun. Secur., 2020, pp. 47–59.

[14] C. Mello-Klein, “How secure is your security camera? hackers can spy on cameras through walls, new research finds,” 2024. [Online]. Available:https://news.northeastern.edu/2024/02/08/securitycamera-privacy-hacking/

[15] X. Ma, J. Qu, J. Li, J. C. Lui, Z. Li, and X. Guan, “Pinpointing hidden IoT devices via spatial-temporal traffic fingerprinting,” in Proc. IEEE INFOCOM IEEE Conf. Comput. Commun., 2020, pp. 894–903.

[16] C. Osborne, “Smart locks opened with nothing more than a MAC address,” 2020. [Online]. Available: https://www.zdnet.com/article/smartlocks-opened-with-nothing-more-than-a-mac-address

[17] N. Apthorpe, D. Y. Huang, D. Reisman, A. Narayanan, and N. Feamster, “Keeping the smart home private with Smart(er) IoT traffic shaping,” in Proc. PoPETs, 2019, pp. 128–148.

[18] S. Xiong, A. D. Sarwate, and N. B. Mandayam, “Network traffic shaping for enhancing privacy in IoT systems,” IEEE/ACM Trans. Netw., vol. 30, no. 3, pp. 1162–1177, Jun. 2022.

[19] J. Brahma and D. Sadhya, “Preserving contextual privacy for smart home IoT devices with dynamic traffic shaping,” IEEE Internet Things J., vol. 9, no. 13, pp. 11434–11441, Jul. 2022.

[20] T. Hou, T. Wang, Z. Lu, Y. Liu, and Y. Sagduyu, “IoTGAN: GAN powered camouflage against machine learning based IoT device identification,” in Proc. IEEE Int. Symp. Dyn. Spectr. Access Netw., 2021, pp. 280–287.

[21] S. Tan, S. Yu, W. Liu, D. He, and S. Chan, “You can glimpse but you cannot identify: Protect IoT devices from being fingerprinted,” IEEE Trans. Dependable Secure Comput., vol. 21, no. 3, pp. 1210–1223, May/Jun. 2024.

[22] J. Li et al., “FOAP: Fine-grained open-world android app fingerprinting,” in Proc. USENIX Secur., 2022, pp. 1579–1596.

[23] J. Li et al., “Packet-level open-world app fingerprinting on wireless traffic,” in Proc. Netw. Distrib. Syst. Secur. Symp., 2022, pp. 1–18.

[24] M. Shen, K. Ji, Z. Gao, Q. Li, L. Zhu, and K. Xu, “Subverting website fingerprinting defenses with robust traffic representation,” in Proc. USENIX Secur., 2023, pp. 607–624.

[25] G. Cherubin, R. Jansen, and C. Troncoso, “Online website fingerprinting: Evaluating website fingerprinting attacks on Tor in the real world,” in Proc. USENIX Secur., 2022, pp. 753–770.

[26] X. Liu et al., “SniffMislead: Non-intrusive privacy protection against wireless packet sniffers in smart homes,” in Proc. 24th Int. Symp. Res. Attacks, Intrusions Defenses, 2021, pp. 33–47.

[27] J. Chung, C. Gulcehre, K. Cho, and Y. Bengio, “Gated feedback recurrent neural networks,” in Proc. Int. Conf. Mach. Learn., 2015, pp. 2067–2075.

[28] M. Hessel et al., “Rainbow: Combining improvements in deep reinforcement learning,” in Proc. AAAI Conf. Artif. Intell., vol. 32, no. 1, 2018, pp. 3215–3222.

[29] M. Vanhoef, “Fragment and forge: Breaking Wi-Fi through frame aggregation and fragmentation,” in Proc. USENIX Secur., 2021, pp. 161–178.

[30] P. Liu, P. Yang, W.-Z. Song, Y. Yan, and X.-Y. Li, “Real-time identification of rogue WiFi connections using environment-independent physical features,” in Proc. INFOCOM IEEE Conf. Comput. Commun., 2019, pp. 190–198.

[31] S. Sadowski and P. Spachos, “RSSI-based indoor localization with the internet of things,” IEEE Access, vol. 6, pp. 30149–30161, 2018.

[32] T. J. Pierson, T. Peters, R. Peterson, and D. Kotz, “Proximity detection with single-antenna IoT devices,” in Proc. 25th Annu. Int. Conf. Mobile Comput. Netw., 2019, pp. 1–15.

[33] “GNU Radio,” 2025. [Online]. Available: https://www.gnuradio.org/

[34] “VirtualHere,” 2025. [Online]. Available: https://www.virtualhere.com/

[35] A. Sivanathan et al., “Classifying IoT devices in smart environments using network traffic characteristics,” IEEE Trans. Mobile Comput., vol. 18, no. 8, pp. 1745–1759, Aug. 2019.

[36] J. Ren, D. J. Dubois, D. Choffnes, A. M. Mandalari, R. Kolcun, and H. Haddadi, “Information exposure from consumer IoT devices: A multidimensional, network-informed measurement approach,” in Proc. Interne Meas. Conf., 2019, pp. 267–279.

[37] C. Duan, H. Gao, G. Song, J. Yang, and Z. Wang, “ByteIoT: A practical IoT device identification system based on packet length distribution,” IEEE Trans. Netw. Serv. Manag., vol. 19, no. 2, pp. 1717–1728, Jun. 2022.

[38] M. R. Shahid, G. Blanc, Z. Zhang, and H. Debar, “IoT devices recognition through network traffic analysis,” in Proc. IEEE Big Data, 2018, pp. 5187–5192.

[39] R. Kolcun et al., “Revisiting IoT device identification,” in Proc. IFIP TMA, 2021, pp. 1–9.

[40] X. Liu, Y. Han, and Y. Du, “IoT device identification using directiona packet length sequences and 1D-CNN,” Sensors, vol. 22, no. 21, 2022, Art. no. 8337.

[41] M. Cunche, “I know your MAC address: Targeted tracking of individua using Wi-Fi,” J. Comput. Virol. Hacking Techn., vol. 10, no. 4, pp. 219–227, 2014.

[42] J. Martin, E. Rye, and R. Beverly, “Decomposition of MAC address structure for granular device inference,” in Proc. 32nd Annu. Conf. Comput. Secur. Appl., 2016, pp. 78–88.

[43] S. Yang, D. Zhang, R. Song, P. Yin, and Y. Chen, “Multiple wifi access points co-localization through joint AOA estimation,” IEEE Trans. Mobile Comput., vol. 23, no. 2, pp. 1488–1502, Feb. 2024.

[44] J. Zhang, G. Shen, W. Saad, and K. Chowdhury, “Radio frequency fingerprint identification for device authentication in the Internet of Things,” IEEE Commun. Mag., vol. 61, no. 10, pp. 110–115, Oct. 2023.

[45] Z. Yao et al., “A novel radio frequency fingerprint concealment method based on iq imbalance compensation and digital pre-distortion,” IEEE Trans. Inf. Forensics Secur., vol. 19, pp. 7349–7361, 2024.

[46] C. Duan, S. Zhang, J. Yang, Z. Wang, Y. Yang, and J. Li, “Pinball: Universal and robust signature extraction for smart home devices,” in Proc. IEEE Int. Symp. Integr. Netw. Manage., 2021, pp. 1–9.

[47] Y. Sun, S. Fu, S. Zhang, H. Zhu, and Y. Li, “Accurate IoT device identification from merely packet length,” in Proc. IFIP/IEEE Int. Symp. Integr. Netw. Manage., 2020, pp. 1–9.

[48] A. J. Pinheiro, J. d. M. Bezerra, C. A. Burgardt, and D. R. Campelo, “Identifying IoT devices and events based on packet length from encrypted traffic,” Comput. Commun., vol. 144, pp. 8–17, 2019.

[49] Y. Wan, K. Xu, F. Wang, and G. Xue, “IoTAthena: Unveiling IoT device activities from network traffic,” IEEE Trans. Wireless Commun., vol. 21, no. 1, pp. 651–664, Jan. 2022.

[50] G. Xue, Y. Wan, X. Lin, K. Xu, and F. Wang, “An effective machine learning based algorithm for inferring user activities from IoT device events,” IEEE J. Sel. Areas Commun., vol. 40, no. 9, pp. 2733–2745, Sep. 2022.

[51] S. A. Hamad, W. E. Zhang, Q. Z. Sheng, and S. Nepal, “IoT device identification via network-flow based fingerprinting and learning,” in Proc. 18th IEEE Int. Conf. Trust, Secur. Privacy Comput. Commun. 13th IEEE Int. Conf. Big Data Sci. Eng., 2019, pp. 103–111.

[52] J. Qu et al., “An input-agnostic hierarchical deep learning framework for traffic fingerprinting,” in Proc. USENIX Secur., 2023, pp. 589–606.

[53] L. Fan et al., “AutoIoT: Automatically updated IoT device identification with semi-supervised learning,” IEEE Trans. Mobile Comput., vol. 22, no. 10, pp. 5769–5786, Oct. 2023.

[54] M. Abdel-Basset, H. Hawash, R. K. Chakrabortty, and M. J. Ryan, “Semi-supervised spatiotemporal deep learning for intrusions detection in IoT networks,” IEEE Internet Things J., vol. 8, no. 15, pp. 12251–12265, Aug. 2021.

[55] J. Zhao, Q. Li, J. Sun, M. Dong, K. Ota, and M. Shen, “Efficient IoT device identification via network behavior analysis based on time series dictionary,” IEEE Internet Things J., vol. 11, no. 3, pp. 5129–5142, Feb. 2024.

[56] A. Bremler-Barr, H. Levy, and Z. Yakhini, “IoT or not: Identifying IoT devices in a short time scale,” in Proc. IEEE/IFIP Netw. Operations Manage. Symp., 2020, pp. 1–9.

[57] A. Hameed and A. Leivadeas, “IoT traffic multi-classification using network and statistical features in a smart environment,” in Proc. IEEE 25th Int. Workshop Comput. Aided Model. Des. Commun. Links Netw., 2020, pp. 1–7.

[58] N. Moustafa, B. Turnbull, and K.-K. R. Choo, “An ensemble intrusion detection technique based on proposed statistical flow features for protecting network traffic of Internet of Things,” IEEE Internet Things J., vol. 6, no. 3, pp. 4815–4830, Jun. 2019.

[59] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “Appscanner: Automatic fingerprinting of smartphone apps from encrypted network traffic,” in Proc. IEEE Eur. Symp. Secur. Privacy, 2016, pp. 439–454.

[60] A. J. Pinheiro, P. F. de Araujo-Filho, J. d. M. Bezerra, and D. R. Campelo, “Adaptive packet padding approach for smart home networks: A tradeoff between privacy and performance,” IEEE Internet Things J., vol. 8, no. 5, pp. 3930–3938, Mar. 2021.

[61] A. J. Pinheiro, J. M. Bezerra, and D. R. Campelo, “Packet padding for improving privacy in consumer IoT,” in Proc. IEEE Symp. Comput. Commun., 2018, pp. 00925–00929.

[62] M. Alyami, A. Alghamdi, M. A. Alkhowaiter, C. Zou, and Y. Solihin, “Random segmentation: New traffic obfuscation against packet-size-based side-channel attacks,” Electronics, vol. 12, no. 18, 2023, Art. no. 3816.

[63] A. Alshehri, J. Granley, and C. Yue, “Attacking and protecting tunneled traffic of smart home devices,” in Proc. 10th ACM Conf. Data Appl. Secur. Privacy, 2020, pp. 259–270.

[64] Q. Li, K. Yu, D. Chen, M. Sha, and L. Cheng, “TrafficSpy: Disaggregating VPN-encrypted IoT network traffic for user privacy inference,” in Proc. IEEE Conf. Commun. Netw. Secur., 2022, pp. 145–153.

[65] M. Alyami, M. Alkhowaiter, M. Al Ghanim, C. Zou, and Y. Solihin, “MAC-Layer traffic shaping defense against WiFi device fingerprinting attacks,” in Proc. IEEE Symp. Comput. Commun., 2022, pp. 1–7.

[66] S. Xiong, A. D. Sarwate, and N. B. Mandayam, “Defending against packet-size side-channel attacks in IoT networks,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process., 2018, pp. 2027–2031.

[67] I. Hafeez, M. Antikainen, and S. Tarkoma, “Protecting IoT-Environments against traffic analysis attacks with traffic morphing,” in Proc. IEEE Int. Conf. Pervasive Comput. Commun. Workshops, 2019, pp. 196–201.

[68] N. Apthorpe, D. Reisman, and N. Feamster, “Closing the blinds: Four strategies for protecting smart home privacy from network observers,” in Proc. IEEE ConPro, 2017, pp. 1–6.

[69] H. Wu, H. Liu, B. Wang, and G. Xin, “Accurate traffic replay based on interactive sequence and timestamp,” in Proc. IEEE 9th Int. Conf. Commun. Softw. Netw., 2017, pp. 1107–1110.

[70] M. O. Gani, H. Sarwar, and C. M. Rahman, “Prediction of state of wireless network using Markov and hidden Markov model,” J. Netw., vol. 4, no. 10, pp. 976–984, 2009.

[71] J. Martin et al., “A study of MAC address randomization in mobile devices and when it fails,” in Proc. PoPETs, 2017, pp. 268–286.

[72] F. Gringoli, M. Schulz, J. Link, and M. Hollick, “Free your CSI: A channel state information extraction platform for modern Wi-Fi chipsets,” in Proc. Int. Workshop Wireless Netw. Testbeds, Exp. Eval. Characterization, 2019, pp. 21–28.

[73] R. A. Sharma, E. Soltanaghaei, A. Rowe, and V. Sekar, “Lumos: Identifying and localizing diverse hidden IoT devices in an unfamiliar environment,” in Proc. USENIX Secur., 2022, pp. 1095–1112.

[74] A. Razavi, M. Valkama, and E.-S. Lohan, “K-means fingerprint clustering for low-complexity floor estimation in indoor mobile localization,” in Proc. IEEE Globecom Workshops, 2015, pp. 1–7.

![](images/631741221064368b963909ecc022b76ca0f939fcb41fb9a1fec7d1c20041084d.jpg)  
Huafeng Bian received the BS degree in computer science and technology from Xi’an Jiaotong University in 2020. He is currently working toward the PhD degree with the MOE Key Laboratory for Intelligent Networks and Network Security, Faculty of Electronic and Information Engineering, Xi’an Jiaotong University, Xi’an, China. His research interests include wireless network, IoT security and traffic fingerprinting defense.

![](images/8dc96dcfe755b4472c9594ccb7cf88329e878208e09c3ba87db36c82f793ad7f.jpg)

Jianfeng Li received the PhD degree in control science and engineering from Xi’an Jiaotong University in 2018. He was a postdoctoral fellow with the Hong Kong Polytechnic University from 2019 to 2022. He is currently an assistant professor with the MOE Key Laboratory for Intelligent Networks and Network Security, Faculty of Electronic and Information Engineering, Xi’an Jiaotong University. His research interests include traffic analysis, privacy of mobile platform, and large-scale cyber security.

![](images/444bc09c58847ac8551a31a775c6151918c3d9ebcdca760d2d0d06740877f509.jpg)

Xiaobo Ma (Member, IEEE) received the PhD degree in control science and engineering from Xi’an Jiaotong University, Xi’an, China, in 2014. He was a postdoctoral research fellow with The Hong Kong Polytechnic University in 2015. He is currently a professor with the MOE Key Laboratory for Intelligent Networks and Network Security, Faculty of Electronic and Information Engineering, Shaanxi Province Key Laboratory of Computer Network, Xi’an Jiaotong University. His research interests include internet measurement and cyber security. He is an editorial board member ofIEEE Transactions on Dependable and Secure Computing, and technical program committee (TPC) member of ACM Conference on Computer and Communications Security (CCS).

![](images/f3c476e5430d899b00af239690a1c784fdf212ad50a14ebdbc2b83f6729cd64b.jpg)

Jialong Zhang received the PhD degree in computer engineering from Texas A&M University in 2016. He was a research scientist with IBM Research, ByteDance, and Tencent from 2016 to 2024. He is currently a professor with the MOE Key Laboratory for Intelligent Networks and Network Security, Faculty of Electronic and Information Engineering, Shaanxi Province Key Laboratory of Computer Network, Xi’an Jiaotong University. His research interests have centered on cyber security and AI security.

![](images/d35f10d4f61bbf2845ef62b6821fd2c64470083ebbec833459f5f93921891dbb.jpg)

Xiapu Luo is currently a professor with the Department of Computing, Hong Kong Polytechnic University. His research interests include blockchain and smart contracts security, mobile and IoT security, network security and privacy, and software engineering with papers published in top venues. He was the recipient of more than ten best/distinguished paper awards, including ACM CCS’24 Distinguished Paper Award, four ACM SIGSOFT Distinguished Paper Awards, Best DeFi Papers Award 2023, Best Paper Award in INFOCOM’18, Best Research Paper Award

in ISSRE’16, and several awards from the industry. He was also the recipient of the BOCHK Science and Technology Innovation Prize (FinTech) 2023 for his contribution to blockchain security. He is also an ACM distinguished member for his research in safeguarding blockchain and smart contracts along with Android and its applications.

![](images/249576fc081e4eba3fce0aa22ab085d207fccaf50c50392cf824f8d0b9ea4356.jpg)

Wei Wang (Senior Member, IEEE) received the PhD degree from Xi’an Jiaotong University in 2006. He is currently a full professor with the Ministry of Education Key Lab for Intelligent Networks and Network Security, Xi’an Jiaotong University, China. He is also an adjunct professor with the School of Computer Science and Technology, Beijing Jiaotong University. He has authored or co-authored more than 100 peer-reviewed articles in various journals and international conferences, including the IEEE Transactions on Dependable and Secure Computing,

IEEE Transactions on Information Forensics and Security, IEEE Transactions on Software Engineering, USENIX Security, ACM CCS, AAAI, Ubicomp, IEEE INFOCOM. His research interests include data security and privacy-preserving computation. He was the recipient of the ACM CCS 2023 Distinguished Paper Award. He is an Elsevier “highly cited Chinese researchers”. He is an associate editor of the IEEE Transactions on Dependable and Secure Computing, and an editorial board member of the Computers & Security and Frontiers ofComputer Science. He is a vice chair of ACM SIGSAC China.

![](images/c3c450fd881a5db402334b3b536b2939ddc469914855e51d52d2f0393f62c55b.jpg)

Zhou Su (Senior Member, IEEE) has authored or coauthored technical papers, including top journals and top conferences, such as IEEE Journal on Selected Areas in Communications , IEEE TRANSACTIONS ON INFORMATION FOREN-SICS AND SECURITY, IEEE Transactions on Information Forensics and Security, IEEE Transactions on Mobile Computing, IEEE/ACM Transactions on Networking , and INFOCOM. He was the recipient of the Best Paper Award of International Conference IEEE ICC2020, IEEE BigdataSE2019, and IEEE CyberSciTech2017. He is an associate editor of the IEEE Internet of Things Journal, IEEE Open Journal ofthe Computer Society, and IET Communications.

![](images/796714de376b9752dfc1ef50f00159a43379ff87ba68570802fb2822a23135d5.jpg)

Xiaohong Guan (Life Fellow, IEEE) received the BS and MS degrees in control engineering from Tsinghua University, Beijing, China, in 1982 and 1985, respectively, and the PhD degree in electrical and systems engineering from the University of Connecticut, Storrs, CT, USA, in 1993. From 1993 to 1995, he was a senior consulting engineer with Pacific Gas and Electric. From 1999 to 2000, he visited the Division of Engineering and Applied Science, Harvard University. From 1985 to 1988 and in 1995, he was with Xi’an Jiaotong University, Xi’an, China, and was the Cheung Kong Professor of systems engineering, in 1999. From 1999 to 2009, he was the director with the State Key Lab for Manufacturing Systems. From 2008 to 2018, he was the dean of School of Electronic and Information Engineering, and has been the dean of Faculty of Electronic and Information Engineering since 2019. Since 2001, he has also been with the Center for Intelligent and Networked Systems, Tsinghua University, where he was the Head of Department of Automation, from 2003 to 2008. His research interests include economics and security of networked systems, including power and energy systems, manufacturing systems, and cyber-physical systems. Dr. Guan is a member of the Chinese Academy of Sciences.
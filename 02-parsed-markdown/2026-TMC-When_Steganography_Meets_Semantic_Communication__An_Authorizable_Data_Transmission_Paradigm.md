# When Steganography Meets Semantic Communication: An Authorizable Data Transmission Paradigm

Boyu Han , Gaolei Li , Member, IEEE, Xiao Yang , Graduate Student Member, IEEE, Jun Wu , Senior Member, IEEE, Jianhua Li , Senior Member, IEEE, and Yuchen Liu

Abstract—Recent advances in Semantic Communication (Sem-Com) have integrated semantically aware encoding and channel adaptation to enhance wireless transmission efficiency. In Sem-Com, covert communication is extensively adopted to secure data transmission, but current methodologies remain constrained by signal-level obfuscation strategies that rely on bit-level manipulations. Consequently, they are loosely coupled with semantic feature learning and often face a rigid trade-off between covert robustness and undetectability in practice. To address these limitations, we propose a steganographybased authorizable SemCom framework, embedding the true transmission data within cover inputs for covert delivery. The integration focuses on achieving highly covert secret transmission within the semantic communication architecture. In our framework, the private transmitter embeds true (i.e., secret) data into cover inputs using a secret hiding module, then applies semantic encoding for transmission. The receiving ends ensure covert data accessibility in multi-client scenarios: authorized users with the secret decoding module can fully semantically restore the true data, whereas unauthorized users solely reconstruct the apparent cover details and stay unaware of the hidden data. Moreover, to realize the above functionalities, the proposed SemCom system leverages a dual-objective joint training strategy, simultaneously learning shared knowledge of stealthy transmission and preserving the normal capability for regular data. Empirical results prove that our framework attains high-fidelity SemCom transmission for secret (PSNR 31 dB, SSIM > 91%, and LPIPS 0.04), and holds robustness under multiple adaptive and adversarial attack scenarios. Meanwhile, the embedded true data manifests no perceptible visual artifacts, and SemCom regular input efficacy is consistently preserved.

Index Terms—Covert communication, covert transmission, data steganography, semantic communication.

## I. INTRODUCTION

EMANTIC Communication (SemCom) has gained growing attention as an innovative paradigm that shifts the communication focus from bitstreams to semantic details [1], [2], [3]. Within SemCom, ajointly trained semantic encoder-decoder pair projects input source data into low-dimensional latent representations via learning the shared knowledge. With the knowledge at both ends, it allows the transmitter to dispatch minimal semantic codes by semantic encoding [4], [5], [6]. Conversely, the semantic decoder leverages the same knowledge to perform semantic inference and recover source inputs [7], [8]. By discarding redundant semantic details, SemCom markedly reduces bandwidth demand, suppresses error incidence, and sustains reliable efficacy even under strict bandwidth constraints and severe channel impairments. Its application expands across multiple domains, including Artificial Intelligence of Things (AIoT), Virtual Reality/Augmented Reality (VR/AR), and Smart Cities [1], [9].

In practical implementations, transmitting covert content alongside primary communication is essential for privacy protection, authorization control, and task-specific information sharing [9], [10], [11], [12]. Recent studies have considerably promoted this area. Spread-spectrum signalling expands a signal into a much wider pseudo-random code space [13], [14]. This dilution lowers the power-spectral density below the noise floor, rendering it indistinguishable from noise to conventional detectors. Noise-adaptive power control tracks channel noise to throttle transmission power to the exact level required for the intended receiver to meet its error-rate target while maintaining undetectability [15], [16]. Covert beamforming completes spatial stealth by steering a narrowly focused main lobe toward the legitimate user and suppressing side-lobes to near-noise amplitudes elsewhere. Any eavesdropper outside the main lobe therefore observes only noise-level leakage [17]. Network and protocol level covert channels achieve stealth by embedding data in redundant header bits or packet timing, and then using adaptive traffic shaping to make the flow statistically identical to normal traffic [18], [19], [20].

While these methods are effective in traditional bit-level communications, the development of semantic communication brings specific requirements for covert and secure transmission from its users. To satisfy the increasing security and privacy demands of semantic communication users, it is essential to ensure covertness as an inherent requirement alongside semantic exchange. However, existing covert communication methods struggle to meet these requirements as they predominantly rely on fine-grained bit- and signal-level perturbations rather than semantic entities [21], [22]. These approaches (e.g., injecting redundant bits or tweaking amplitude/phase of the carrier waveform) manipulate physical-layer symbols without considering high-level data semantics [23], [24], [25]. As a result, they often fail to utilize the semantic structure effectively, limiting the volume of hidden information that can be securely transmitted. This highlights the need to shift the objective toward achieving highly covert secret transmission within the semantic communication architecture.

To address these limitations, we introduce steganography into the end-to-end training of SemCom, enabling authorized users to recover covertly embedded data within the semantic communication pipeline to meet the security and privacy demands. To provide an intuitive comparison, we conducted a pre-experimental evaluation under identical 30,dB SNR conditions, as shown in Fig. 1. Three representative baselines— spread-spectrum signaling, noise-adaptive power control, and covert beamforming—were benchmarked against our semantic– steganographic approach. As illustrated in Fig. 1(a), compared with our method, these signal-level techniques lead to higher distortion in the cover medium (reflected by degraded PSNR/SSIM) due to the direct perturbation of physical-layer symbols, which may increase the risk of detection. Fig. 1(b) further indicates that when the bit-level recovery becomes unreliable under channel impairments, the secret recovery utility of conventional baselines quickly collapses, whereas our approach leverages semantic inference to sustain robust covert delivery for authorized users. In this work, we prioritize the integration of security features into the communication process, enabling achieving highly covert secret transmission within the semantic communication architecture by embedding secret content into an existing cover medium without compromising the primary semantic task. In practice, directly plugging a hiding module at the transmitter and a decoding module at the receiver on top of a standard SemCom pipeline often leads to ineffective covert recovery and unstable covertness, because semantic feature compression and channel distortion may suppress the embedded cues. To further illustrate this point, Fig. 2 visualizes a naive sequential baseline, although the transmitted stego remains visually plausible, the decoded secret collapses without joint optimization.

Holding these insights, we propose an authorizable SemCom framework. It brings in two core components: the Secret Hiding Module and the Secret Decoding Module. On the transmitter side, the secret hiding module embeds secret inputs into the cover data, which is then conveyed jointly with the standard semanticencoding and channel-encoding processes. On the receiver side, only authorized users equipped with the secret decoding module can accurately reconstruct and interpret the embedded secret data, whereas ordinary (i.e., unauthorized) users’ semantic decoders recover just the cover content, accomplishing covert information transmission. The secret hiding and decoding modules are co-optimized with the other SemCom components for shared knowledge under a dual-objective joint training strategy. This enables covert SemCom without degrading the capability of normal sample transmission. Unlike prior covert-communication methods, our framework embeds the secret input’s semantics directly into the cover while internalizing the corresponding semantic encoding–decoding knowledge within the SemCom system. Accordingly, the framework targets achieving highly covert secret transmission within the semantic communication architecture while aligning with the intrinsic characteristics of SemCom. Empirical results substantiate that it achieves up to 31 dB PSNR, 91% SSIM, and around 0.04 LPIPS (Learned Perceptual Image Patch Similarity) for covert secret recovery across varying channels and SemCom architectures, and uphold superior performance in normal transmission.

![](images/3e7f9dcf7d764f9111338e740ca6ef3f9c287c93e44657ff42bc9d0818585602.jpg)

(a) Pre-experimental comparison of covert communication methods. We compared 3 classic covert communication baselines (spread spectrum, noise adaptive power control, and covert beamforming) with our method under the same channel conditions (30 dB Signal-to-Noise Ratio). All previous techniques underperform in Peak Signal-to-Noise Ratio (PSNR), Structural Similarity Index (SSIM), and transmission rate.  
![](images/9e1a1ccff184f93322222062de94702d205a5c83e3d179cc7ef78ee3f3fb06be.jpg)  
(b) Traditional baselines are bounded by Shannon capacity, whereas SemCom+Stega breaks through at task level. The left axis shows classic covert schemes never exceed the Shannon limit (rate). The right axis shows our SemCom+Stega maintains nonzero task utility below the bit-level threshold, highlighting a task-level beyond-Shannon advantage.

Fig. 1. Overall comparison ofcovert communication and SemCom+stega. (a) Pre-experimental comparison under 30 dB SNR, where classic covert baselines significantly underperform in both PSNR/SSIM and transmission rate. (b) Traditional methods are fundamentally constrained by the Shannon capacity, while semantic+stego consistently achieves task success even below the bit-leve threshold (demonstrating a clear task-level beyond-Shannon advantage).  
![](images/2676c56a4fcddc6e5688680fe9faf81bdce72271cbb0e6006324e7ec8197e2e2.jpg)  
(a) Stego

![](images/e42be3942bcdd1891bdfe83372b5fa51daf58f4803f895a0f0ec4e4527978f80.jpg)  
(b) Secret

![](images/435a868b1e727661481afb10b724a3096eb8d07b285a00a6f923d67dd94cf560.jpg)  
(c) Stego after SemCom

![](images/a63f45ce3ea2c1f4104dc9b5ab27df9a3440c1096a13dfb58247cdcc8766c8e6.jpg)  
(d) Decoded secret  
Fig. 2. Visualization of a naive direct-combination baseline. The stego image can still appear plausible after passing through a standard SemCom pipeline, but decoding the secret directly from the SemCom output fails, implying that a simple sequential integration is ineffective.

To the best ofour knowledge, this is thefirst work to combine SemCom and image steganography.

Our contributions can be summarized as follows.

We propose an authorizable covert SemCom framework that integrates a secret hiding module and a secret decoding module into the end-to-end framework pipeline. This design guarantees that only authorized receivers can flawlessly reconstruct the concealed true data, whilst ordinary receivers perceive just the cover semantics, which therefore fulfills secure, covert data transmission without compromising communication efficacy.

° A dual-objective end-to-end joint training strategy is introduced to co-optimize the secret hiding module, secret decoding module, and semantic encoder-decoder using a multi-branch pixel-wise reconstruction loss, thereby preserving cover data semantics while significantly boosting the robustness and quality of hidden-content recovery under diverse channels and communication scenarios.

° Experiments under various Signal-to-Noise Ratios (SNRs) and compression settings were conducted to evaluate our framework. The results show that the framework achieves high-quality reconstruction for both regular and secret data while maintaining robustness under channel variations and bandwidth constraints. Extensive evaluations against multiple adversarial and explainability-based attacks further confirm the framework’s resilience and defense capability.

## II. RELATED WORK

## A. Semantic Communication Frameworks

SemCom has emerged as a promising paradigm for wireless image transmission by focusing on the meaning of transmitted data rather than bit-level accuracy. With this foundation, existing studies have explored SemCom methodologies across multiple aspects [7], [26], [27], [28], [29], [30], [31], [32], [33]. Study [7] proposed a predictive and adaptive deep coding (PADC) framework that integrates variable-length Deep Joint Source-Channel Coding (DeepJSCC-V), quality prediction, and compression optimization to enable bandwidth-efficient image transmission under SemCom systems. In [26], a personalized saliency-based SemCom framework for UAV image transmission with optimized multi-user resource allocation was developed. Zhang et al. designed a cooperative SemCom framework for image transmission with explainable scene graph modeling and multiagent reinforcement learning-based resource allocation [27]. Research [28] presented a robust image SemCom system based on a multi-scale Vision Transformer to enhance SemCom recovery under channel impairments. Wu et al. investigated a SemCom system that transmits Regions of Interest (ROI) and

Regions of Non-Interest (RONI) over separate channels to improve compression efficiency and transmission robustness [29]. The authors in [30] introduced a reinforcement learning-based semantic image coding framework that adaptively allocates bits to semantic concepts and reconstructs images via generative semantic decoders. A GAN-based semantic image coding model was devised in [31] for low-bitrate SemCom. Liang and Li investigated diffusion-based semantic communications via joint source–channel noise adding with adaptive denoising, and further studied semantic image generation with supervised selection based on multimodal features for SemCom [32], [33].

## B. Covert Communication Technologies

Covert communication plays a key role in secure wireless systems by aiming to hide the presence of transmission itself. Recent studies have examined diverse techniques, from spreadspectrum signalling to adaptive power control, to enhance stealth under various channel conditions [13], [14], [15], [16], [17], [34], [35]. Bash et al. proposed a covert communication scheme that leverages the adversary’s ignorance of transmission time to improve covert rate under power constraints [13]. Research [14] designed a Gaussian-distributed spread-spectrum scheme using thermal noise to enhance covert communication by reducing signal detectability. In [15], a covert communication scheme was developed for RSMA-assisted ambient backscatter systems to enhance transmission security under resource constraints. The authors in [16] established the square root law, showing that only $O ( { \sqrt { n } } )$ bits can be covertly sent over n AWGN (Additive White Gaussian Noise) channel uses without detection. Wu et al. formulated a wireless covert communication scheme using distributed cooperative jamming to enhance covertness over slow fading channels [34]. A robust beamforming scheme was devised in [17] to ensure covert communication under channel uncertainty and detection constraints. In [35], Li et al. developed a RIS-assisted cooperative transmission scheme designed to enhance physical layer security and enable reliable covert communication under stringent detection constraints.

## C. Deep Data Steganography

Image steganography embeds hidden content into cover images while remaining visually imperceptible and resistant to both classical and learning-based steganalysis. Deep learning has accelerated progress in this field. End-to-end architectures that combine CNN backbones, attention mechanisms, and invertible transformations now consistently surpass handcrafted schemes in capacity, fidelity, and robustness [36], [37], [38], [39], [40], [41]. Baluja et al. introduced a fully convolutional encoder–decoder that jointly optimizes spatial-domain embedding and recovery, proving that an entire image can be hidden within another through differentiable layers [36]. A secret-toimage reversible transformation framework was proposed by Zhang et al. to enable generative steganography with high visual quality and recoverability [37]. A refined variant, which augments robustness by integrating deeper residual connections and perceptual consistency losses that stabilize training under distortions and model attacks, was presented in [38]. HiNet was designed in [39] to leverage invertible neural networks and wavelet-domain embedding to achieve reversible, secure hiding with a strictly lossless forward–inverse mapping. A lightweight autoencoder alternative [40] prioritizes parameter efficiency, employing depthwise separable convolutions and channel-attention to maintain imperceptibility in RGB images while reducing computational overhead. DeepMIH [41] extends invertible designs to multi-image hiding, using split-coupling transformations to embed and faithfully recover several payloads concurrently. Beyond conventional pixel-domain image steganography, Huo et al. further extended steganographic design to SemCom by embedding hidden bit-level messages into semantic features [42]. In contrast, our work focuses on imagein-image authorizable transmission with differentiated recovery privileges.

![](images/9a5cd4270d2da9fd7ece52f1e0e5d98ea973d708cf4937061de438080787fb09.jpg)  
Fig. 3. Framework ofthe SemCom system. The input is encoded by a semantic encoder, which captures the essential semantic details for efficient communication. It is then passed through a channel encoder and a wireless channel, and finally decoded by a channel decoder and a semantic decoder to reconstruct the transmitted data, focusing on the most meaningful and relevant information rather than bit values at the receiver side.

## III. SYSTEM MODEL

We consider an end-to-end SemCom framework as shown in Fig. 3. Our notations are listed in Table I. At the transmitter, the input data $\mathbf { I } _ { e } \in \mathbb { R } ^ { 3 \times H \times W }$ is encoded by a semantic encoder $\mathcal { E } _ { \mathrm { s e m } } ( \cdot )$ into a latent feature vector:

$$
\mathbf {z} = \mathcal {E} _ {\mathrm{sem}} (\mathbf {I} _ {e}, \gamma),\tag{1}
$$

where residual blocks with Generalized Divisive Normalization (GDN) and SNR-aware attention ensure robust feature extraction. The channel encoder then applies compression-aware masking and power normalization:

$$
\mathbf {x} = \sqrt {P \cdot K} \cdot \frac {\mathbf {z} \odot \mathbf {m}}{\| \mathbf {z} \odot \mathbf {m} \|}, \quad \mathbf {m} = \operatorname{mask} _ {-} \operatorname{gen} (K, \rho),\tag{2}
$$

where $\rho$ is the compression ratio.

The wireless channel $\mathcal { C } ( \cdot )$ introduces distortion. For AWGN:

$$
\tilde {\mathbf {x}} = \mathbf {x} + \mathbf {n}, \quad \mathbf {n} \sim \mathcal {N} (0, \sigma^ {2} \mathbf {I}), \quad \sigma^ {2} = \frac {P}{1 0 ^ {\gamma / 1 0}},\tag{3}
$$

and for slow Rayleigh fading:

$$
\tilde {\mathbf {x}} = \mathbf {x} \cdot \mathbf {h} + \mathbf {n}, \quad \mathbf {h} \sim \mathcal {C N} (0, 1).\tag{4}
$$

At the receiver, the channel decoder reconstructs latent features:

$$
\tilde {\mathbf {z}} = \mathcal {D} _ {\mathrm{ch}} (\tilde {\mathbf {x}}),\tag{5}
$$

TABLE I SUMMARY OF NOTATIONS

<table><tr><td>Notation</td><td>Description of the meaning</td></tr><tr><td> $\mathbf{I}_{c}$ </td><td>Original cover data</td></tr><tr><td> $\mathbf{I}_{e}$ </td><td>Regular stego data</td></tr><tr><td> $\mathbf{I}_{s}$ </td><td>Secret data to be embedded</td></tr><tr><td> $\mathbf{I}_{e}^{*}$ </td><td>Stego data with embedded secret content</td></tr><tr><td> $\hat{\mathbf{I}}_{e}$ </td><td>Reconstructed stego data at receiver</td></tr><tr><td> $\hat{\mathbf{I}}_{s}$ </td><td>Reconstructed secret data at receiver</td></tr><tr><td> $\hat{\mathbf{I}}_{e}^{*}$ </td><td>Reconstructed stego data with embedded secret content at receiver</td></tr><tr><td> $\mathbf{z}$ </td><td>Semantic feature encoded from  $\mathbf{I}_{e}$  and  $\mathbf{I}_{e}^{*}$ </td></tr><tr><td> $\tilde{\mathbf{z}}$ </td><td>Semantic feature decoded after  $\mathcal{D}_{\text{ch}}$  from  $\mathbf{I}_{e}$ </td></tr><tr><td> $\tilde{\mathbf{z}}_{\text{sct}}$ </td><td>Semantic feature decoded after  $\mathcal{D}_{\text{ch}}$  from  $\mathbf{I}_{e}^{*}$ </td></tr><tr><td> $\mathbf{z}'$ </td><td>Masked and normalized feature</td></tr><tr><td> $\mathbf{m}$ </td><td>Compression mask vector</td></tr><tr><td> $\mathbf{x}$ </td><td>Transmitted signal after channel encoding</td></tr><tr><td> $\tilde{\mathbf{x}}$ </td><td>Received signal after channel transmission</td></tr><tr><td> $\gamma$ </td><td>Channel signal-to-noise ratio (SNR, in dB)</td></tr><tr><td> $\mathbf{h}$ </td><td>Channel gain (AWGN:  $\mathbf{h} = 1$ ; Rayleigh:  $\mathbf{h} \sim \mathcal{CN}(0,1)$ )</td></tr><tr><td> $\mathbf{n}$ </td><td>Additive white Gaussian noise (AWGN)</td></tr><tr><td> $\sigma^{2}$ </td><td>Noise variance derived from SNR  $\gamma$ </td></tr><tr><td> $P$ </td><td>Average transmission power</td></tr><tr><td> $\rho$ </td><td>Channel compression ratio (CR)</td></tr><tr><td> $\mathcal{C}(\cdot)$ </td><td>Wireless channel model (e.g., AWGN, Rayleigh)</td></tr><tr><td> $\mathcal{E}_{\text{scre}}(\cdot), \mathcal{D}_{\text{scre}}(\cdot)$ </td><td>Secret encoder/decoder pair</td></tr><tr><td> $\mathcal{E}_{\text{sem}}(\cdot), \mathcal{D}_{\text{sem}}(\cdot)$ </td><td>Semantic encoder/decoder pair</td></tr><tr><td> $\mathcal{E}_{\text{ch}}(\cdot), \mathcal{D}_{\text{ch}}(\cdot)$ </td><td>Channel encoder/decoder pair</td></tr></table>

which are then fed into the semantic decoder:

$$
\hat {\mathbf {I}} _ {e} = \mathcal {D} _ {\mathrm{sem}} (\tilde {\mathbf {z}}, \gamma),\tag{6}
$$

where deconvolutional residual blocks with attention recover the final output data.

The entire end-to-end SemCom process is summarized as

$$
\hat {\mathbf {I}} _ {e} = \mathcal {D} _ {\mathrm{sem}} (\mathcal {D} _ {\mathrm{ch}} (\mathcal {C} (\mathcal {E} _ {\mathrm{ch}} (\mathcal {E} _ {\mathrm{sem}} (\mathbf {I} _ {e}, \gamma)), \gamma)), \gamma).\tag{7}
$$

## IV. AUTHORIZABLE TRANSMISSION FRAMEWORK

We integrate additional encoding-decoding mapping regarding secret data into the SemCom shared knowledge. Within this design, the transmitter can covertly embed secret semantic details within cover inputs, with only authorized receivers equipped with the designated secret decoding module being able to semantically reconstruct the concealed secret. Contrariwise, unauthorized regular receivers are limited to decoding the cover data, and the overall SemCom efficiency in transmitting the non-secret remains unaffected. Also, the knowledge is implanted via end-to-end joint training for both authorized and regular transmission optimizations. The proposed authorizable covert SemCom framework is depicted in Fig. 4.

![](images/19ff613f800ef578418774dd4a4f42fefa1733af1bc379e85c6a7dd965445444.jpg)  
Fig. 4. Framework of the proposed system. The framework extends a SemCom pipeline by incorporating covert transmission as another objective. Semantic content is decoded through the standard SemCom path, while confidential information is recovered by authorized users via an additional decoder placed after the channel decoder.

Our framework extends standard SemCom architectures through three core parts: (1) Secret Hiding Module, which dynamically conceals secret data at the transmitter; (2) Secret Decoding Module, held solely by the authorized receiver to semantically decode the secret; and (3) Dual-Objective Joint Training, which concurrently optimizes both secret and standard transmission missions.

We start with the joint task formulation that combines regular SemCom transmission and authorized data recovery. Next, each core part of our framework is systematically detailed.

## A. Joint Task Formulation

Our end-to-end communication task includes two parallel yet interrelated objectives: (1) reconstructing the transmitted ordinary data with high semantic fidelity for unauthorized receivers, and (2) enabling covert delivery and accurate recovery of secrets embedded within cover data selectively for authorized clients. These two tasks form ajoint learning problem, where SemCom’s implanted shared knowledge must simultaneously support both SemCom reconstruction and covert secret information decoding.

1) Object-1: Formally, for one normal input data ${ \mathbf { I } } _ { e } ,$ the system must guarantee that general (non-authorized) users can efficiently decode the conveyed data at the receiving end, without undermining the system functionality:

$$
\mathbf {I} _ {e} \sim \hat {\mathbf {I}} _ {e} = \mathcal {D} _ {\mathrm{sem}} (\tilde {\mathbf {z}}, \gamma).\tag{8}
$$

2) Object-2: Given secret data ${ \mathbf I } _ { s } ,$ we hide it in cover data $\mathbf { I } _ { c }$ to forge stego inputs through a secret hiding module $\mathcal { E } _ { \mathrm { s c r e } } \mathrm { . }$ $\mathbf { I } _ { e } ^ { * } = { \mathcal { E } } _ { \mathrm { s c r e } } ( \mathbf { I } _ { c } , \mathbf { I } _ { s } ) . \mathbf { I } _ { e } ^ { * }$ is then transmitted through the SemCom pipeline. At the receiver, the proposed framework aims to concurrently recover both branches:

$$
\mathbf {I} _ {s} \sim \hat {\mathbf {I}} _ {s} = \mathcal {D} _ {\mathrm{scre}} (\tilde {\mathbf {z}} _ {\mathrm{sct}}, \gamma), \quad \mathbf {I} _ {e} ^ {*} \sim \hat {\mathbf {I}} _ {e} ^ {*} = \mathcal {D} _ {\mathrm{sem}} (\tilde {\mathbf {z}} _ {\mathrm{sct}}, \gamma),\tag{9}
$$

where $\mathcal { D } _ { \mathrm { s c r e } } ( \cdot ) , \mathcal { D } _ { \mathrm { s e m } } ( \cdot )$ are the secret decoding module for authorized clients and normal users’ regular semantic decoders; $\tilde { \mathbf { z } } _ { \mathrm { s c t } }$ indicates the decoded semantic feature vector for $\mathbf { I } _ { e } ^ { * }$

In our framework, secret data recovery is performed securely and independently without interfering with conventional Sem-Com transmission. Moreover, the secret decoding module is accessible only to authorized users, ensuring that covert content remains inaccessible to unintended adversaries even if they illicitly obtain the SemCom input or output.

This dual-objective formulation causes optimization challenges due to potential conflicts between SemCom transmission and covert secret decoding. In the following sections, we overcome these through specialized hiding and decoding modules and a dual-objective joint training strategy.

## B. Secret Hiding Module

To facilitate reliable semantic-level covert transmission, a private secret hiding module is incorporated at the transmitter side for secret insertion. With the secret data $\mathbf { I } _ { s } \in \mathbb { R } ^ { 3 \times H \times W }$ and the corresponding cover $\mathbf { I } _ { c } \in \mathbb { R } ^ { 3 \times H \times W }$ , the module generates a stego image $\mathbf { I } _ { e } ^ { * }$ by a hiding encoder $\mathcal { E } _ { \mathrm { s c r e } }$ :

$$
\mathbf {I} _ {e} ^ {*} = \mathcal {E} _ {\mathrm{scre}} (\mathbf {I} _ {c}, \mathbf {I} _ {s}) = \psi \left(\mathcal {H} \left(\phi (\mathbf {I} _ {c}), \phi (\mathbf {I} _ {s})\right)\right),\tag{10}
$$

where $\phi ( \cdot )$ refers to a unified encoder extracting features from both inputs, $\mathcal { H } ( \cdot )$ fuses them into one joint hidden representation, and $\psi ( \cdot )$ forges the stego data. We minimize the dissimilarity between $\mathbf { I } _ { e } ^ { * }$ and I<sub>c</sub> in training, leading to compact, imperceptible embedding and sustaining the semantic integrity of the cover and the secret data.

Specifically, the secret hiding module fundamentally comprises 3 key operational phases:

1) Feature Extraction: The cover and secret data are passed through a feature-extracting encoder $\phi ( \cdot )$ , including convolutional layers and downsampling, to capture semantic features:

$$
\mathbf {f} _ {c} = \phi (\mathbf {I} _ {c}), \quad \mathbf {f} _ {s} = \phi (\mathbf {I} _ {s}),\tag{11}
$$

where $\mathbf { f } _ { c }$ and $\mathbf { f } _ { s }$ signify the intermediate feature maps of the cover and secret. The encoder is technically defined as:

$$
\phi (\mathbf {I}) = \sigma \left(\sum_ {m = 1} ^ {C _ {1}} \mathbf {W} _ {m} ^ {(2)} * \sigma \left(\sum_ {c = 1} ^ {C _ {0}} \mathbf {W} _ {c} ^ {(1)} * \mathbf {I} _ {c} + b _ {c} ^ {(1)}\right) + b _ {m} ^ {(2)}\right),
$$

where $\mathbf { W } _ { c } ^ { ( 1 ) }$ and $\mathbf { W } _ { m } ^ { ( 2 ) }$ denote convolution kernels of sizes $3 \times 3$ and $4 \times 4 ,$ respectively, $b _ { c } ^ { ( 1 ) }$ and $b _ { m } ^ { ( 2 ) }$ are the corresponding bias terms, ∗ represents the 2D convolution operator, and $\sigma ( \cdot )$ reflects the ReLU activation function.

2) Feature Fusion and Hiding: The extracted features are concatenated and forward propagated through a multi-layer convolutional hiding network $\mathcal { H } ( \cdot )$ for fusion:

$$
\mathbf {f} _ {\text { joint }} = \operatorname{Concat} (\mathbf {f} _ {c}, \mathbf {f} _ {s}),\tag{12}
$$

$$
\mathbf {f} _ {h} = \mathcal {H} (\mathbf {f} _ {\text { joint }}),\tag{13}
$$

where $\mathbf f _ { \mathrm { j o i n t } }$ implies the concatenated feature along the channel axis, and $\mathbf { f } _ { h }$ is the resulting hidden representation. The operator Concat $( \cdot , \cdot )$ symbolizes channel-wise concatenation. The fusion network $\mathcal { H } ( \cdot )$ has one $1 \times 1$ and two $3 \times 3$ convolutions, and each is followed by batch normalization (BN) and activation for efficient feature integration:

$$
\begin{array}{c} \mathcal {H} (\mathbf {x}) = \sigma_ {3} \left(\mathrm{BN} _ {3} \left(\mathbf {W} _ {3} * \sigma_ {2} \left(\mathrm{BN} _ {2} \left(\mathbf {W} _ {2} *\right) + \mathbf {b} _ {1}\right)\right) + \mathbf {b} _ {2}\right) \\ \sigma_ {1} \left(\mathrm{BN} _ {1} \left(\mathbf {W} _ {1} * \mathbf {x} + \mathbf {b} _ {1}\right)\right) + \mathbf {b} _ {3})  , \end{array}\tag{14}
$$

where $\mathbf { W } _ { 1 } \in \mathbb { R } ^ { 6 4 \times 1 2 8 \times 1 \times 1 } , \ \mathbf { W } _ { 2 } \in \mathbb { R } ^ { 6 4 \times 6 4 \times 3 \times 3 } .$ , and ${ \bf W } _ { 3 } \in  $ $\mathbb { R } ^ { 3 2 \times 6 4 \times 3 \times 3 }$ are convolution kernels of the three layers; and $\mathrm { B N } _ { i }$ implies i-th Batch Normalization.

This hierarchical phase progressively compresses the fused features into a dense representation. Meanwhile, residual-style activations, spatially localized convolutions, and batch normalization collaboratively promote structural fidelity, which is crucial for generating high-quality stego images.

3) Upsampling and Construction: The latent hidden representation $\mathbf { f } _ { h }$ is decoded by a construction block $\psi ( \cdot )$ to yield the final stego data:

$$
\mathbf {I} _ {e} ^ {*} = \psi (\mathbf {f} _ {h}),\tag{15}
$$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: Secret Hiding Module.

Input: Cover data  $I_{c} \in R^{3 \times H \times W}$ , Secret data

 $I_{s} \in R^{3 \times H \times W}$ 

Output: Stego data  $I_{e}^{*} \in R^{3 \times H \times W}$ 

/* Feature Extraction */ 

1  $f_{c} \leftarrow \phi(I_{c})$  // Cover feature encoder

2  $f_{s} \leftarrow \phi(I_{s})$  // Secret feature encoder

/* Feature Fusion and Hiding */ 

3  $f_{joint} \leftarrow Concat(f_{c}, f_{s})$ 

4  $f_{h} \leftarrow \mathcal{H}(f_{joint})$  // Hidden representation

/* Construction */ 

5  $I_{e}^{*} \leftarrow \psi(f_{h})$  // Generate stego data

6 return  $I_{e}^{*}$
</div>

where $\psi ( \cdot )$ comprises one transposed convolution and two standard convolutional layers:

$$
\begin{array}{c}\psi (\mathbf {z}) = \operatorname{Tanh} \left(\mathbf {W} _ {3} * \sigma_ {2} \left(\mathrm{BN} _ {2} \left(\mathbf {W} _ {2} *\right. \right. \right.\\\left.\left. \sigma_ {1} \left(\mathbf {W} _ {1} ^ {\top} * \mathbf {z} + \mathbf {b} _ {1}\right) + \mathbf {b} _ {2}\right)\right) + \mathbf {b} _ {3}\left. \right),\end{array}\tag{16}
$$

where $\mathbf { W } _ { 1 } ^ { \top } \in \mathbb { R } ^ { 3 2 \times 3 2 \times 4 \times 4 }$ implies the transposed convolution kernel with stride $s = 2$ and padding $p = 1 ; \mathbf { W } _ { 2 } \in \mathbb { R }$ 16×32×3×3 and $\mathbf { W } _ { 3 } \in \mathbb { R } ^ { 3 \times 1 6 \times 3 \times 3 }$ denote standard convolution weights; and $\mathbf { b } _ { i }$ means the corresponding bias.

With this module, we embed sufficient secret details to guarantee high-resolution secret recovery at the receiver. It seamlessly integrates with the SemCom pipeline as the front-end secret hiding preprocessing for authorized transmitting clients. The hiding module algorithm is specified in Algorithm 1.

## C. Secret Decoding Module

This module implements the secret recovery exclusively for authorized users. It endeavors to reconstruct the secret data $\hat { \mathbf { I } } _ { s }$ with high fidelity by the semantic feature vector $\tilde { \mathbf { z } } _ { \mathrm { s c t } }$ (extracted from $\mathbf { I } _ { e } ^ { * } )$ derived from channel decoding.

To reach accurate and flexible secret recovery, our framework places the secret decoding module between the channel decoder and the semantic decoder, ensuring that the covert branch operates directly on intermediate semantic features before they are transformed by the public SemCom reconstruction path. Receiving $\tilde { \mathbf { z } } _ { \mathrm { s c t } }$ , it applies a secret decoder $\mathcal { D } _ { \mathrm { s c r e } }$ to recover the secret content $\hat { \mathbf { I } } _ { s } .$ . Precisely, we partition this process into 3 phases, encompassing:

1) Feature Refinement: a cascade of convolutional transformations equipped with batch normalization and nonlinear activation enhances the semantic representations from the input latent tensor, suppresses channel noise, and preserves spatial structures while maintaining resolution. This step ensures that semantic details essential for secret recovery are retained under distortion-prone conditions. (2) Channel Compression: progressively reduce the image-channel dimensionality through $3 \times 3$ convolutions with stride 1 and padding 1, thereby maintaining spatial resolution while discarding redundant or weakly informative features and extracting the most salient components for secret reconstruction. This improves generalization and stabilizes optimization against noise. (3) RGB Projection: a dedicated projection layer maps the compact feature representation into the RGB space, followed by a Sigmoid activation to confine pixel intensities within valid ranges, and a bilinear upsampling operation without learnable parameters to restore the secret with its original resolution, resulting in smooth and efficient reconstruction.

This design fulfills direct decoding from intermediate semantic features before ordinary SemCom reconstruction, while resolving conflicts between public transmission and authorized secret decoding. Such a process not only enhances robustness under noisy channel conditions but also integrates covert transmission seamlessly into the SemCom pipeline, thereby achieving accurate and secure secret recovery for authorized users while maintaining semantic fidelity in the public path.

1) Feature Transformation and Refinement: The decoder initially processes the input semantic feature $\tilde { \mathbf { z } } _ { \mathrm { s c t } }$ through a cascade of convolutional transformations. Each block involves a convolution operation $\mathscr { W } ^ { ( i ) }$ with BN and activation:

$$
\begin{array}{l l} \mathbf {f} ^ {(1)} = \mathrm{ReLU} \left(\mathrm{BN} ^ {(1)} \left(\mathcal {W} ^ {(1)} * \tilde {\mathbf {z}} _ {\mathrm{sct}} + \mathbf {b} ^ {(1)}\right)\right), & \mathbb {R} ^ {4 8 \to 6 4}, \\ \mathbf {f} ^ {(2)} = \mathrm{ReLU} \left(\mathrm{BN} ^ {(2)} \left(\mathcal {W} ^ {(2)} * \mathbf {f} ^ {(1)} + \mathbf {b} ^ {(2)}\right)\right), & \mathbb {R} ^ {6 4 \to 6 4}, \\ \mathbf {f} ^ {(3)} = \mathrm{ReLU} \left(\mathrm{BN} ^ {(3)} \left(\mathcal {W} ^ {(3)} * \mathbf {f} ^ {(2)} + \mathbf {b} ^ {(3)}\right)\right), & \mathbb {R} ^ {6 4 \to 6 4}, \end{array}\tag{17}
$$

where $\mathcal { W } ^ { ( i ) } \in \mathbb { R } ^ { C _ { \mathrm { o u t } } \times C _ { \mathrm { i n } } \times 3 \times 3 }$ signifies the i-th layer convolution kernel, and ∗ represents the 2D convolution operator with $p = 1$ and $s = 1$ . This phase augments spatial semantics and preserves resolution, yielding intermediate representation $\mathbf { f } ^ { ( 3 ) }$

2) Channel Compression and Projection: Following feature refinement, the decoder compresses the representation $\mathbf { f } ^ { ( 3 ) }$ via two additional convolutions with decreasing output channels:

$$
\begin{array}{l} \mathbf {f} ^ {(4)} = \operatorname{ReLU} \left(\operatorname{BN} ^ {(4)} \left(\mathcal {W} ^ {(4)} * \mathbf {f} ^ {(3)} + \mathbf {b} ^ {(4)}\right)\right), \qquad \mathbb {R} ^ {6 4 \to 3 2}, \\ \mathbf {f} ^ {(5)} = \operatorname{ReLU} \left(\operatorname{BN} ^ {(5)} \left(\mathcal {W} ^ {(5)} * \mathbf {f} ^ {(4)} + \mathbf {b} ^ {(5)}\right)\right), \qquad \mathbb {R} ^ {3 2 \to 1 6}. \end{array}\tag{18}
$$

These operations serve to reduce channel dimensionality and retain the most salient feature information necessary for secret decoding. Both convolutions deploy $3 \times 3$ kernels with $s = 1$ and $p = 1$ , letting spatial resolution be maintained. The resulting tensor $\mathbf { f } ^ { ( 5 ) } \in \mathbb { R } ^ { \bar { 1 6 } \times \mathbf { \bar { 6 } 4 } \times 6 4 }$ provides a compact latent representation suitable for RGB projection.

3) RGB Projection and Upsampling: The secret decoder projects the latent feature $\mathbf { f } ^ { ( 5 ) }$ into the RGB data space leveraging a $3 \times 3$ convolution and a sigmoid activation function:

$$
\mathbf {f} _ {\text { out }} = \sigma \left(\mathcal {W} ^ {(6)} * \mathbf {f} ^ {(5)} + \mathbf {b} ^ {(6)}\right), \quad \mathbb {R} ^ {1 6 \rightarrow 3}.\tag{19}
$$

The computed vector $\mathbf { f _ { \mathrm { o u t } } }$ is then upsampled to the resolution of $2 5 6 \times 2 5 6$ utilizing bilinear interpolation:

$$
\hat {\mathbf {I}} _ {s} = \text { Upsample } (\mathbf {f} _ {\text { out }}, \text { scale } = 4, \text { mode } = \text { bilinear }).\tag{20}
$$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2: Secret Decoding Module.

Input: Semantic feature  $\tilde{z}_{sct} \in R^{48 \times 64 \times 64}$ 

Output: Reconstructed secret data  $\hat{I}_{s} \in R^{3 \times 256 \times 256}$ 

/* Feature transformation and refinement by applying 3 consecutive Conv $_{3 \times 3}$  layers with BN and ReLU */

1  $f^{(1)} \leftarrow \text{ReLU(BN(Conv} _{3 \times 3}^{(1)}(\tilde{\mathbf{z}})))$  48 → 64

2  $f^{(2)} \leftarrow \text{ReLU(BN(Conv} _{3 \times 3}^{(2)}(\mathbf{f}^{(1)})))$  64 → 64

3  $f^{(3)} \leftarrow \text{ReLU(BN(Conv} _{3 \times 3}^{(3)}(\mathbf{f}^{(2)})))$  64 → 64

/* Channel compression and projection by applying 2 convolutional layers with decreasing channels */

4  $f^{(4)} \leftarrow \text{ReLU(BN(Conv} _{3 \times 3}^{(4)}(\mathbf{f}^{(3)})))$  64 → 32

5  $f^{(5)} \leftarrow \text{ReLU(BN(Conv} _{3 \times 3}^{(5)}(\mathbf{f}^{(4)})))$  32 → 16

/* Final RGB output and upsampling */

6  $f_{out} \leftarrow \sigma(\text{Conv} _{3 \times 3}^{(6)}(\mathbf{f}^{(5)}))$  16 → 3

7  $\hat{I}_{s} \leftarrow \text{Upsample(f}_{\text{out}}, \text{scale} = 4)$ $64 \times 64 \rightarrow 256 \times 256$ 

8 return  $\hat{I}_{s}$
</div>

This yields the reconstructed secret data $\hat { \mathbf { I } } _ { s }$ . The upsampling step restores the spatial dimensions without introducing any learnable parameters, resulting in smooth and efficient reconstruction of the embedded secret data.

The architecture and algorithm of the secret decoder are presented in Fig. 5 and Algorithm 2. By combining covert secret recovery with the SemCom delivery and limiting access of our two devised modules to the authorized receiver, the framework achieves secure and exclusive retrieval of concealed secrets.

## D. Dual-Objective Joint Training Strategy

We adopt end-to-end training to simultaneously update the components of conventional SemCom (i.e., semantic codecs) and private secret transmission (i.e., secret hiding and decoding modules). The normal semantic decoder (for the unauthorized) aims to reconstruct just the stego under channel compression and distortion. Inversely, the secret decoding functions to recover covert content from intermediate semantic features only available for authorized users. During this unified training process, the shared knowledge is collaboratively optimized to support both public and private reconstruction tasks, facilitating joint advancement of authorized and standard transmission. The optimization could be divided into two parts:

1) Regular Transmission Optimization:

$$
R _ {r} (D _ {\mathrm{train}}) = \lambda_ {r} \cdot \mathbb {E} _ {\mathbf {I} _ {e} \sim \mathcal {P} _ {D _ {\mathrm{train}}}} \left[ \mathcal {L} \left(\mathcal {D} _ {\mathrm{sem}} (\tilde {\mathbf {z}}, \gamma), \mathbf {I} _ {e}\right) \right],\tag{21}
$$

Where $R _ { r } ( D _ { \mathrm { t r a i n } } )$ denotes the regular reconstruction risk over the training dataset $D _ { \mathrm { t r a i n } } , \mathcal { P } _ { D _ { \mathrm { t r a i n } } }$ symbolizes the distribution behind $D _ { \mathrm { t r a i n } } , { \mathcal { L } }$ indicates the loss (mean squared error is leveraged in this study), and $\phantom { } . \lambda _ { r }$ <sub>r</sub> is the weight controlling the influence ofthe SemCom recovery objective. We mitigate this risk and promote the semantic decoder to reconstruct the stego image with high fidelity for unauthorized receivers.

![](images/2992d1bd2e4688e9ac88bfe9ca85f2e855f41fa2c20bba93bf167fcb58186c4a.jpg)  
Fig. 5. Structure of the private secret decoder. The decoder receives a latent feature map of size 48 × 64 × 64 and passes it through 6 convolutional layers with gradually reduced channel dimensions and a final bilinear upsampling, ultimately reconstructing high-resolution RGB secret data of size $2 5 6 \times 2 5 6$

2) Discriminative Transmission Optimization:

$$
R _ {h} (D _ {\mathrm{train}}) = \lambda_ {h} \cdot \mathbb {E} _ {\mathbf {I} _ {c} \sim \mathcal {P} _ {D _ {\mathrm{train}}}} \left[ \mathcal {L} \left(\mathcal {E} _ {\mathrm{scre}} (\mathbf {I} _ {c}, \mathbf {I} _ {s}), \mathbf {I} _ {c}\right) \right],\tag{22}
$$

$$
R _ {u} (D _ {\mathrm{train}}) = \lambda_ {u} \cdot \mathbb {E} _ {\mathbf {I} _ {e} \sim \mathcal {P} _ {D _ {\mathrm{train}}}} \left[ \mathcal {L} \left(\mathcal {D} _ {\mathrm{sem}} (\tilde {\mathbf {z}} _ {\mathrm{sct}}, \gamma), \mathbf {I} _ {e} ^ {*}\right) \right],\tag{23}
$$

$$
R _ {a} (D _ {\mathrm{train}}) = \lambda_ {a} \cdot \mathbb {E} _ {\mathbf {I} _ {s} \sim \mathcal {P} _ {D _ {\mathrm{train}}}} \left[ \mathcal {L} \left(\mathcal {D} _ {\mathrm{scre}} (\tilde {\mathbf {z}} _ {\mathrm{sct}}, \gamma), \mathbf {I} _ {s}\right) \right],\tag{24}
$$

Where $R _ { h } , R _ { u }$ , and $R _ { a }$ act as the following risk measures.

° We inspect the similarity divergence risk $R _ { h } ( D _ { \mathrm { t r a i n } } )$ between the stego $\mathcal { E } _ { \mathrm { s c r e } } ( \mathbf { I } _ { c } , \mathbf { I } _ { s } ) = \mathbf { I } _ { e } ^ { * }$ and cover data ${ \mathbf { I } } _ { c } ,$ and by optimizing it, we render that the embedded secret remains visually imperceptible.

$R _ { u } ( D _ { \mathrm { t r a i n } } )$ evaluates the reconstruction risk of semantics $\tilde { \mathbf { z } } _ { \mathrm { s c t } }$ by unauthorized clients. With this risk optimization, unauthorized receiving clients only semantically reconstruct the superficial information $\mathbf { I } _ { e } ^ { * }$ of the stego, keeping the secret unavailable to the unauthorized.

° The last $R _ { a } ( D _ { \mathrm { t r a i n } } )$ serves to quantify the secret reconstruction risk for authorized users. To minimize it, authorized client-side receivers can decode the concealed information ${ \mathbf I } _ { s }$ within transmitted semantics $\tilde { \mathbf { z } } _ { \mathrm { s c t } }$ , hence realizing covert information delivery.

This discriminative optimization establishes shared knowledge of our framework to balance the reconstruction objectives for both authorized and unauthorized users, consequently enhancing the performance of both the SemCom and private secret hiding-decoding modules.

## E. Practical Implementation

The proposed authorizable semantic communication framework ensures secure and trustworthy operation throughout its entire lifecycle, covering training, distribution, component update, local storage, and revocation. Rather than functioning as an independent security module, it remains fully compatible with existing infrastructures and can be seamlessly integrated into standard deployment pipelines. During training, the semantic– steganographic codec is optimized within a trusted center under homomorphic encryption to protect both data confidentiality and gradient privacy. In the distribution stage, the trained model and authorization keys are delivered through a PKI-based mechanism with digital signatures, ensuring authenticity and integrity. Component update follows the same PKI process but is activated only for major revisions, minimizing overhead and potential attack surfaces. For local storage, execution and key management are secured within a Trusted Execution Environment (TEE), while a Physically Unclonable Function (PUF) guarantees hardware-level uniqueness and prevents replay or token forgery. Finally, during revocation, PKI-based certificate revocation and TEE verification jointly disable unauthorized decoding rights, maintaining precise control and accountability across the entire system lifecycle.

## F. Robustness Discussion

The robustness of the proposed framework is examined against common attacks that attempt to approximate or perturb the encoder–decoder mapping, while detailed results are presented in the subsequent subsection. Each attack targets the endto-end semantic–steganographic pipeline $\mathcal { D } _ { \mathrm { s e m } } \circ \mathcal { D } _ { \mathrm { c h } } \circ \mathcal { E } _ { \mathrm { c h } } \circ \mathcal { E } _ { \mathrm { s e m } } ,$ which embeds both the regular stego ${ \bf I } _ { e }$ and the embedded stego $\mathbf { I } _ { e } ^ { * }$ into the latent semantic representation z. An adversary aims to build a surrogate mapping $\hat { f } _ { \boldsymbol { \theta } } \approx f _ { \boldsymbol { \theta } }$ or to distort the channel-decoded feature z˜ to infer the secret output $\hat { \mathbf { I } } _ { s }$ from observable stego images.

Model Extraction and Knowledge Distillation: In model extraction or knowledge distillation, the attacker minimizes E $\| \mathcal { D } _ { \mathrm { s e m } } ( \tilde { \mathbf { z } } ) - \hat { \mathcal { D } } _ { \mathrm { s e m } } ( \tilde { \mathbf { z } } ) \| ^ { 2 } \mathrm { o r } ~ \mathrm { K L } \big ( f _ { \theta } ( \mathbf { I } _ { c } ) \| g _ { \phi } ( \mathbf { I } _ { c } ) \big )$ ; however, the nonlinear coupling within z prevents faithful replication of the semantic–secret relationship in latent space.

Network Pruning and Fine-Tuning: For network pruning or fine-tuning, parameter perturbations $\theta ^ { \prime } = \theta + \Delta \theta$ break the coregularized gradient balance between $\mathcal { L } _ { \mathrm { s e m } }$ and $\mathcal { L } _ { \mathrm { s c r e } }$ , leading to feature misalignment without exposing confidential content.

TABLE II  
DATASET STATISTICS FOR TINY-IMAGENET AND DIV2K IN TERMS OF KEY PROPERTIES RELEVANT TO IMAGE TRANSMISSION AND RECONSTRUCTION SC TASKS

<table><tr><td>Property</td><td>Tiny-ImageNet</td><td>DIV2K</td></tr><tr><td>Image Count</td><td>100,000</td><td>1,000</td></tr><tr><td>Resolution</td><td>64 × 64</td><td>256 × 256</td></tr><tr><td>Number of Classes</td><td>200</td><td>None</td></tr><tr><td>Task Objective</td><td>Image Classification</td><td>Image Super-Resolution / Reconstruction</td></tr><tr><td>Downsampling</td><td>Not Applied</td><td>Bicubic and Realistic (×2, ×3, ×4)</td></tr><tr><td>Usage Scenario</td><td>Small-Scale Image Classification, Lightweight Model Evaluation</td><td>Super-Resolution, Compression, Reconstruction, Perceptual Quality Assessment</td></tr></table>

Token-Generator Inversion: Token-generator inversion attempts arg min<sub>I</sub>∗ $\| \phi ( \mathcal { E } _ { \mathrm { s e m } } ( \mathbf { I } _ { e } ^ { * } ) ) - \mathbf { t } \|$ , but the stochastic channel operation $\mathcal { C } ( \cdot )$ and the non-invertible tokenization φ(·) make secret recovery theoretically ill-posed and unstable.

Explainability-Based Probing (Grad-CAM): Explainabilitybased probing derives saliency from $\nabla _ { \mathbf { z } } { \mathcal { L } } _ { \mathrm { s e m } } .$ yet the model regularization enforces statistical independence between z and the secret mapping $\mathcal { D } _ { \mathrm { s c r e } } ( \cdot )$ , ensuring that gradients reveal only public semantics and visual cues.

These mechanisms collectively explain the framework’s inherent resistance, whose empirical verification follows in the robustness defense experiments presented below.

## V. EXPERIMENT

This section presents a comprehensive experimental evaluation of the proposed SemCom framework enriched by covert data transmission. As the core innovation of our framework, the secret decoding module was assessed for its ability to accurately reconstruct covert secret data from intermediate semantic features, under various channel conditions and SemCom types. We measured secret information reconstruction fidelity and sensitivity to signal degradation to validate the resilience of the secret decoding module. In parallel, we evaluated the SemCom transmission module to ensure that the transmission of stego data remains semantically faithful and minimally distorted. We also validate the covertness of the embedded stego by reporting visual imperceptibility and detector-based undetectability. We start by describing the experimental setup, including datasets, training configurations, and evaluation parameters, followed by detailed visualization results and analysis of both the SemCom transmission results and the secret data recovery for authorized users.

## A. Experimental Settings

Data and Preprocessing: We evaluated the proposed secret decoding module using two widely used image datasets: Tiny-ImageNet [43] and DIV2K [44]. Tiny-ImageNet consists of 100,000 images at a resolution of 64 × 64, while DIV2K contains 1,000 high-quality images originally in 2K resolution, which were downscaled to $2 5 6 \times 2 5 6$ using bicubic interpolation. The properties of both datasets are summarized in Table II. From each dataset, we randomly selected 800 images. Among them, 400 were used as cover images {I<sup>i</sup> }, and the remaining

400 as secret images $\{ \mathbf { I } _ { s } ^ { i } \}$ . These pairs were used to generate 400 stego images $\{ \mathbf { I } _ { e } ^ { * i } \}$ through the secret hiding encoder. All images were normalized to the [0 1] range.

Training Configuration: The semantic encoders adopted four architectures (JSCC-V, JSCC, JSCC-F, and JSCC-Q), each pretrained and evaluated under both AWGN and Rayleigh fading channels. The models were trained using the Adam optimizer with a learning rate of $5 \times 1 0 ^ { - 5 }$ for 1,500 epochs, using a batch size of 4. All input images were resized to $2 5 6 \times 2 5 6$ and normalized to the range [0 1]. Both the $\operatorname { S N R } \gamma$ and compression ratio $\rho$ are explicitly fed into the model to facilitate adaptive modulation of feature representations.

Evaluation Metric: To evaluate the quality of the recovered secret image, we used PSNR, SSIM, and LPIPS.

PSNR is defined as:

$$
\operatorname{PSNR} \left(\hat {\mathbf {I}} _ {s}, \mathbf {I} _ {s}\right) = 1 0 \cdot \log_ {1 0} \left(\frac {1}{\operatorname{MSE} \left(\hat {\mathbf {I}} _ {s} , \mathbf {I} _ {s}\right)}\right),\tag{25}
$$

where MSE denotes the mean squared error between the predicted and ground-truth images.

SSIM is defined as:

$$
\mathrm{SSIM} (\hat {\mathbf {I}} _ {s}, \mathbf {I} _ {s}) = \frac {(2 \mu_ {\hat {s}} \mu_ {s} + c _ {1}) (2 \sigma_ {\hat {s} s} + c _ {2})}{(\mu_ {\hat {s}} ^ {2} + \mu_ {s} ^ {2} + c _ {1}) (\sigma_ {\hat {s}} ^ {2} + \sigma_ {s} ^ {2} + c _ {2})},\tag{26}
$$

where $\mu , \sigma _ { \mathrm { { : } } }$ , and $\sigma _ { \hat { s } s }$ represent local means, variances, and crosscovariance respectively, and $c _ { 1 } , c _ { 2 }$ are small constants to avoid division instability.

LPIPS measures perceptual similarity by computing deep feature distances between the predicted and reference images:

$$
\mathrm{LPIPS} (\hat {\mathbf {I}} _ {s}, \mathbf {I} _ {s}) = \sum_ {l} w _ {l} \cdot \| \phi_ {l} (\hat {\mathbf {I}} _ {s}) - \phi_ {l} (\mathbf {I} _ {s}) \| _ {2} ^ {2},\tag{27}
$$

where $\phi _ { l } ( \cdot )$ denotes deep features extracted from layer l of a pre-trained network, and $w _ { l }$ is a learned weight for each layer. Lower LPIPS indicates higher perceptual similarity.

## B. Visualization Results

To qualitatively evaluate our framework, we visualized representative samples from Tiny-ImageNet [43] and DIV2K [44], as shown in Fig. 6. Each case includes the original cover, the embedded stego, the reconstructed stego, the original secret, and the recovered secret. The reconstructed stego images closely match the originals with minimal perceptual distortion, confirming that semantic encoding preserves visual semantics during transmission. Meanwhile, the recovered secrets maintain structural clarity and color consistency, demonstrating that covert information can be reliably extracted. These results validate the framework’s robustness in joint SemCom transmission and authorized secret recovery.

## C. Performance Evaluations

This subsection systematically evaluates the effectiveness of the proposed dual-objective joint SemCom framework. The experiments are grouped into three categories. First, the main results examine the performance of our jointly trained model on two datasets, Tiny-ImageNet [43] and DIV2K [44], under various SNRs, considering both AWGN and Rayleigh fading channels, and evaluated on four representative semantic communication architectures (JSCC-V, JSCC, JSCC-F, and JSCC-Q). Second, the comparative experiments benchmark the jointly optimized model against a baseline in which the SemCom and secret decoding modules were trained independently. Finally, the ablation study investigates the influence of different channel compression ratios ρ on framework performance. These evaluations collectively validate the robustness and advantages of our joint framework under various realistic transmission conditions.

Îs  
Ic  
![](images/7a241a03a15ac2cc2d52998021121e5c287e17050e63ec68df561112acea968f.jpg)  
(a)

I\*  
![](images/17007b0d178070554a0f0067919d6b3c9944fadb3e0874dcc2b627337b53dfa1.jpg)  
(b)

I\*  
![](images/da89025b6510724271ea5e43af7e0a1e367e37055caf99339d4c3d0f5c799f98.jpg)  
(c)  
Reconstructed Stego  
(a) Tiny-ImageNet

Is  
![](images/3f507c1f295bfed2f67e1a84b937b038cd2300178c38da0b1318c9f6e71018d2.jpg)  
(d)  
Secret Image

![](images/1a5645da0e21bed1797a71b686e072d6553fe9d90b014dcbf352f1fb751d883f.jpg)  
(e)  
Reconstructed Secret

Ic  
![](images/eba5820fca7a0d17a464b26f24d55b088f900e07e1ce618c925590c33f2c262f.jpg)  
(a)  
Cover Image

I\*  
![](images/edd28ef71b7cf35ea78ca024968e02462f64f1536e13c69127ca0ec71149ba74.jpg)  
(b)  
Stego Image

Î\*  
Is  
![](images/7989f0f8d5721e0434750959d9ae168cd8891ef8dbba95e948032ccba5de1040.jpg)  
(c)

![](images/8f66977ff3e03968781dc95190f5aeccd2fd5e959e6089b4a6fe159a43866f23.jpg)  
(d)  
(b) DIV2K

Îs  
![](images/dc3a6f4237f26d6b6ab952ce28f11397e1c85a1a65167f9b140bdd35a3e98af3.jpg)  
Reconstructed Secret  
(e)  
Fig. 6. Visualization results on (a) Tiny-ImageNet and (b) DIV2K. Each row includes: cover image, stego image, reconstructed stego, secret image, and reconstructed secret. The results demonstrate the accuracy of the SemCom module in transmitting stego images and the effectiveness of secret image recovery b the secret decoding module.

Covertness Evaluation: We evaluate the proposed steganography-based pipeline from three complementary aspects, including visual imperceptibility, statistical consistency, and detector-based undetectability. We measure the similarity between cover and stego images using PSNR and SSIM, and examine potential distribution shifts via histogram distance and frequency-domain high-frequency energy statistics. For detector-based evaluation, we adopt StegExpose together with lightweight CNN steganalysis detectors, namely SRNetLite and HiNetDetectorLite, to provide a covertness check that covers both classical feature-based detection and learning-based detection under the same setting. StegExpose serves as a widely used hand-crafted baseline based on statistical cues, while SRNetLite and HiNetDetectorLite represent practical CNN-style detectors that can be evaluated consistently in our pipeline.

Table V reports visual imperceptibility and distribution-level statistics between the cover and the public stego images. The public stego remains visually close to the cover, achieving an average PSNR of 38.31 dB and an average SSIM of 99.39%.

The pixel-distribution shift is further quantified by the grayscale histogram <sub>1</sub> distance, which concentrates around 77.58 on average. In the frequency domain, the high-frequency energy ratio stays nearly unchanged, where the cover and stego ratios are 0.0571 and 0.0560 on average, and the mean difference $\mathrm { i s - 1 . 1 3 \times 1 0 ^ { - 3 } }$ , indicating negligible perturbation to spectral characteristics across multiple domains.

Table VI summarizes detector-based undetectability under identical settings. StegExpose exhibits a true-positive rate of 0.7601 but also a high false-positive rate of 0.595, resulting in a balanced accuracy of 0.583, marginally above random guessing. The lightweight CNN steganalysis detectors show weak separability. SRNetLite achieves 38.33% test accuracy with overlapping mean scores for cover and stego, while HiNetDetectorLite reaches 45.00% accuracy with nearly identical score means. Overall, these results provide quantitative evidence that the proposed embedding is visually imperceptible and difficult to detect using steganalysis tools and lightweight CNN detectors in our setting, confirming robust undetectability.

Joint Model Performance: We evaluated the performance of the proposed framework across multiple dimensions, including dataset resolution, channel condition, SNR, SemCom architecture, and reconstruction target (both SemCom transmission and covert secret reconstruction). The results, illustrated in Tables III & IV, clearly and consistently demonstrate the effectiveness of the joint optimization framework.

As summarized in Tables III & IV, the proposed framework demonstrates strong and consistently reliable performance across four semantic communication architectures (JSCC-V, JSCC, JSCC-F, and JSCC-Q), two representative datasets

Rayleigh Channel

Rayleigh Channel

(d) JSCC-Q  
(c) JSCC-F  
COMPREHENSIVE RESULTS OF PROPOSED MODEL ON TINY-IMAGENET (64 × 64) ACROSS CHANNELS (AWGN, RAYLEIGH) AND ARCHITECTURES (JSCC-V / JSCC / JSCC-F / JSCC-Q)  
TABLE III

<table><tr><td colspan="7">(a) JSCC-V</td></tr><tr><td colspan="7">AWGN Channel</td></tr><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>22.36</td><td>89.00</td><td>0.0817</td><td>15.87</td><td>75.47</td><td>0.1307</td></tr><tr><td>12.5</td><td>23.59</td><td>92.27</td><td>0.0594</td><td>17.32</td><td>79.55</td><td>0.1091</td></tr><tr><td>15.0</td><td>24.99</td><td>94.70</td><td>0.0404</td><td>18.89</td><td>82.90</td><td>0.0927</td></tr><tr><td>17.5</td><td>26.65</td><td>96.48</td><td>0.0265</td><td>20.61</td><td>85.61</td><td>0.0804</td></tr><tr><td>20.0</td><td>28.65</td><td>97.78</td><td>0.0160</td><td>22.53</td><td>87.74</td><td>0.0727</td></tr><tr><td>22.5</td><td>31.21</td><td>98.68</td><td>0.0085</td><td>24.69</td><td>89.33</td><td>0.0586</td></tr><tr><td>25.0</td><td>34.74</td><td>99.27</td><td>0.0040</td><td>27.09</td><td>90.42</td><td>0.0505</td></tr><tr><td>27.5</td><td>40.45</td><td>99.61</td><td>0.0014</td><td>29.59</td><td>91.06</td><td>0.0448</td></tr><tr><td>30.0</td><td>49.35</td><td>99.73</td><td>0.0006</td><td>31.32</td><td>91.29</td><td>0.0445</td></tr></table>

<table><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>24.63</td><td>92.41</td><td>0.1010</td><td>15.64</td><td>71.69</td><td>0.1679</td></tr><tr><td>12.5</td><td>25.87</td><td>94.32</td><td>0.0741</td><td>18.66</td><td>73.29</td><td>0.1422</td></tr><tr><td>15.0</td><td>27.29</td><td>95.84</td><td>0.0535</td><td>19.91</td><td>77.13</td><td>0.1149</td></tr><tr><td>17.5</td><td>28.92</td><td>97.05</td><td>0.0372</td><td>20.45</td><td>80.78</td><td>0.0949</td></tr><tr><td>20.0</td><td>30.87</td><td>98.01</td><td>0.0243</td><td>22.26</td><td>84.80</td><td>0.0810</td></tr><tr><td>22.5</td><td>33.27</td><td>98.74</td><td>0.0094</td><td>23.41</td><td>87.94</td><td>0.0719</td></tr><tr><td>25.0</td><td>36.41</td><td>99.26</td><td>0.0022</td><td>24.95</td><td>90.11</td><td>0.0511</td></tr><tr><td>27.5</td><td>40.89</td><td>99.58</td><td>0.0012</td><td>27.94</td><td>91.39</td><td>0.0423</td></tr><tr><td>30.0</td><td>47.08</td><td>99.72</td><td>0.0006</td><td>30.95</td><td>91.95</td><td>0.0398</td></tr></table>

<table><tr><td colspan="7">(b) JSCC</td></tr><tr><td colspan="7">AWGN Channel</td></tr><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>22.97</td><td>89.08</td><td>0.0481</td><td>18.26</td><td>80.28</td><td>0.0897</td></tr><tr><td>12.5</td><td>24.29</td><td>92.17</td><td>0.0366</td><td>19.61</td><td>82.94</td><td>0.0816</td></tr><tr><td>15.0</td><td>25.82</td><td>94.54</td><td>0.0280</td><td>21.13</td><td>85.29</td><td>0.0685</td></tr><tr><td>17.5</td><td>27.58</td><td>96.32</td><td>0.0202</td><td>22.83</td><td>87.30</td><td>0.0568</td></tr><tr><td>20.0</td><td>29.67</td><td>97.62</td><td>0.0126</td><td>24.72</td><td>88.93</td><td>0.0511</td></tr><tr><td>22.5</td><td>32.25</td><td>98.56</td><td>0.0074</td><td>26.76</td><td>90.19</td><td>0.0481</td></tr><tr><td>25.0</td><td>35.67</td><td>99.19</td><td>0.0039</td><td>28.85</td><td>91.09</td><td>0.0465</td></tr><tr><td>27.5</td><td>40.76</td><td>99.57</td><td>0.0013</td><td>30.67</td><td>91.63</td><td>0.0453</td></tr><tr><td>30.0</td><td>48.19</td><td>99.72</td><td>0.0006</td><td>31.60</td><td>91.85</td><td>0.0448</td></tr></table>

<table><tr><td colspan="7">AWGN Channel</td></tr><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>25.76</td><td>90.68</td><td>0.0407</td><td>20.04</td><td>81.66</td><td>0.1082</td></tr><tr><td>12.5</td><td>27.14</td><td>93.55</td><td>0.0274</td><td>21.85</td><td>84.20</td><td>0.0928</td></tr><tr><td>15.0</td><td>28.67</td><td>95.64</td><td>0.0171</td><td>23.78</td><td>86.20</td><td>0.0663</td></tr><tr><td>17.5</td><td>30.41</td><td>97.10</td><td>0.0114</td><td>25.76</td><td>87.74</td><td>0.0552</td></tr><tr><td>20.0</td><td>32.47</td><td>98.13</td><td>0.0078</td><td>27.63</td><td>88.89</td><td>0.0526</td></tr><tr><td>22.5</td><td>34.97</td><td>98.83</td><td>0.0049</td><td>29.18</td><td>89.71</td><td>0.0507</td></tr><tr><td>25.0</td><td>38.23</td><td>99.28</td><td>0.0030</td><td>30.14</td><td>90.26</td><td>0.0498</td></tr><tr><td>27.5</td><td>42.80</td><td>99.55</td><td>0.0013</td><td>30.44</td><td>90.57</td><td>0.0492</td></tr><tr><td>30.0</td><td>48.00</td><td>99.67</td><td>0.0007</td><td>30.30</td><td>90.67</td><td>0.0483</td></tr></table>

<table><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>25.30</td><td>87.97</td><td>0.0571</td><td>15.00</td><td>72.34</td><td>0.1316</td></tr><tr><td>12.5</td><td>26.94</td><td>91.56</td><td>0.0332</td><td>16.24</td><td>76.75</td><td>0.1113</td></tr><tr><td>15.0</td><td>28.76</td><td>94.20</td><td>0.0262</td><td>17.64</td><td>80.61</td><td>0.0950</td></tr><tr><td>17.5</td><td>30.84</td><td>96.12</td><td>0.0174</td><td>19.21</td><td>83.92</td><td>0.0820</td></tr><tr><td>20.0</td><td>33.25</td><td>97.47</td><td>0.0108</td><td>21.01</td><td>86.68</td><td>0.0714</td></tr><tr><td>22.5</td><td>36.09</td><td>98.43</td><td>0.0064</td><td>23.09</td><td>88.89</td><td>0.0644</td></tr><tr><td>25.0</td><td>39.58</td><td>99.08</td><td>0.0035</td><td>25.54</td><td>90.54</td><td>0.0492</td></tr><tr><td>27.5</td><td>43.63</td><td>99.48</td><td>0.0019</td><td>28.38</td><td>91.61</td><td>0.0398</td></tr><tr><td>30.0</td><td>45.96</td><td>99.66</td><td>0.0012</td><td>31.13</td><td>92.08</td><td>0.0384</td></tr></table>

(Tiny-ImageNet and DIV2K), and both AWGN and Rayleigh fading channels. On Tiny-ImageNet under AWGN, the SemCom modules of all four architectures surpass 44 dB PSNR, 99.5% SSIM, and reduce LPIPS below 0.002 at 30 dB SNR, while authorized secret recovery consistently delivers around 30–31 dB PSNR, 90–92% SSIM, and LPIPS near 0.04. Similar stability is observed under Rayleigh fading, with SemCom PSNR between 45.9–48.1 dB and secret recovery around 30.9–31.6 dB at 30 dB SNR.

On the higher-resolution DIV2K dataset, although the absolute values are lower due to increased image complexity, the framework preserves robust scaling trends. At 30 dB SNR under

<table><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>25.65</td><td>91.02</td><td>0.0437</td><td>14.34</td><td>69.44</td><td>0.1264</td></tr><tr><td>12.5</td><td>26.98</td><td>93.75</td><td>0.0278</td><td>15.41</td><td>72.84</td><td>0.1017</td></tr><tr><td>15.0</td><td>28.48</td><td>95.74</td><td>0.0197</td><td>16.67</td><td>76.16</td><td>0.0938</td></tr><tr><td>17.5</td><td>30.21</td><td>97.16</td><td>0.1118</td><td>18.18</td><td>79.15</td><td>0.0818</td></tr><tr><td>20.0</td><td>32.26</td><td>98.16</td><td>0.0091</td><td>20.03</td><td>82.57</td><td>0.0754</td></tr><tr><td>22.5</td><td>34.77</td><td>98.83</td><td>0.0055</td><td>23.36</td><td>85.13</td><td>0.0698</td></tr><tr><td>25.0</td><td>38.06</td><td>99.29</td><td>0.0034</td><td>26.42</td><td>88.59</td><td>0.0649</td></tr><tr><td>27.5</td><td>42.73</td><td>99.55</td><td>0.0013</td><td>29.61</td><td>90.76</td><td>0.0444</td></tr><tr><td>30.0</td><td>48.10</td><td>99.68</td><td>0.0008</td><td>31.59</td><td>91.55</td><td>0.0433</td></tr></table>

<table><tr><td colspan="7">AWGN Channel</td></tr><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>31.67</td><td>95.91</td><td>0.0198</td><td>22.69</td><td>84.40</td><td>0.0844</td></tr><tr><td>12.5</td><td>32.97</td><td>96.93</td><td>0.0143</td><td>23.54</td><td>85.50</td><td>0.0710</td></tr><tr><td>15.0</td><td>34.40</td><td>97.69</td><td>0.0094</td><td>24.48</td><td>86.52</td><td>0.0611</td></tr><tr><td>17.5</td><td>35.99</td><td>98.25</td><td>0.0067</td><td>25.50</td><td>87.45</td><td>0.0548</td></tr><tr><td>20.0</td><td>37.81</td><td>98.69</td><td>0.0045</td><td>26.57</td><td>88.25</td><td>0.0505</td></tr><tr><td>22.5</td><td>39.86</td><td>99.03</td><td>0.0034</td><td>27.65</td><td>88.89</td><td>0.0476</td></tr><tr><td>25.0</td><td>42.01</td><td>99.27</td><td>0.0025</td><td>28.60</td><td>89.35</td><td>0.0465</td></tr><tr><td>27.5</td><td>43.78</td><td>99.43</td><td>0.0019</td><td>29.26</td><td>89.61</td><td>0.0482</td></tr><tr><td>30.0</td><td>44.07</td><td>99.51</td><td>0.0016</td><td>29.45</td><td>89.64</td><td>0.0465</td></tr></table>

Rayleigh Channel

<table><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>29.13</td><td>92.97</td><td>0.0479</td><td>22.52</td><td>83.79</td><td>0.0827</td></tr><tr><td>12.5</td><td>30.56</td><td>95.19</td><td>0.0331</td><td>23.33</td><td>85.10</td><td>0.0709</td></tr><tr><td>15.0</td><td>32.08</td><td>96.69</td><td>0.0216</td><td>24.17</td><td>86.30</td><td>0.0619</td></tr><tr><td>17.5</td><td>33.73</td><td>97.73</td><td>0.0115</td><td>25.04</td><td>87.40</td><td>0.0558</td></tr><tr><td>20.0</td><td>35.63</td><td>98.46</td><td>0.0075</td><td>25.92</td><td>88.38</td><td>0.0517</td></tr><tr><td>22.5</td><td>37.90</td><td>98.96</td><td>0.0053</td><td>26.78</td><td>89.20</td><td>0.0489</td></tr><tr><td>25.0</td><td>40.68</td><td>99.31</td><td>0.0025</td><td>27.58</td><td>89.82</td><td>0.0473</td></tr><tr><td>27.5</td><td>43.95</td><td>99.52</td><td>0.0016</td><td>28.25</td><td>90.22</td><td>0.0469</td></tr><tr><td>30.0</td><td>46.37</td><td>99.60</td><td>0.0012</td><td>28.73</td><td>90.35</td><td>0.0476</td></tr></table>

AWGN, SemCom PSNR ranges from 37.9 to 40.8 dB with SSIM above 97.8%, while secret decoding maintain 27–28 dB PSNR, 87–89% SSIM, and LPIPS between 0.06–0.09. Under Rayleigh fading, SemCom modules still reach 38.8–41.0 dB PSNR and 98.3% SSIM, while secret recovery remains reliable with 26–27.7 dB PSNR and 86–88% SSIM.

Across both datasets, performance improves monotonically with SNR and the four architectures exhibit similar scaling trends. JSCC-V consistently achieves the highest SemCom PSNR, JSCC and JSCC-F provide balanced trade-offs between transmission and covert recovery, while JSCC-Q shows slightly lower SemCom fidelity but stable secret decoding. Together these results confirm the robustness and complementarity of the proposed framework.

TABLE IV  
COMPREHENSIVE RESULTS OF PROPOSED MODEL ON DIV2K (256 × 256) ACROSS CHANNELS (AWGN, RAYLEIGH) AND ARCHITECTURES (JSCC-V / JSCC / JSCC-F / JSCC-Q)

<table><tr><td colspan="7">(a) JSCC-V</td></tr><tr><td colspan="7">AWGN Channel</td></tr><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>26.78</td><td>82.07</td><td>0.1131</td><td>15.37</td><td>72.12</td><td>0.2124</td></tr><tr><td>12.5</td><td>28.29</td><td>86.24</td><td>0.0951</td><td>17.26</td><td>77.21</td><td>0.1991</td></tr><tr><td>15.0</td><td>29.95</td><td>89.32</td><td>0.0667</td><td>18.35</td><td>80.87</td><td>0.1682</td></tr><tr><td>17.5</td><td>31.77</td><td>91.53</td><td>0.0483</td><td>20.54</td><td>82.39</td><td>0.1374</td></tr><tr><td>20.0</td><td>33.66</td><td>93.03</td><td>0.0304</td><td>22.01</td><td>85.58</td><td>0.1160</td></tr><tr><td>22.5</td><td>35.25</td><td>94.63</td><td>0.0197</td><td>23.11</td><td>86.69</td><td>0.0956</td></tr><tr><td>25.0</td><td>35.68</td><td>96.68</td><td>0.0094</td><td>24.70</td><td>87.41</td><td>0.0949</td></tr><tr><td>27.5</td><td>35.55</td><td>97.92</td><td>0.0072</td><td>26.13</td><td>87.84</td><td>0.0838</td></tr><tr><td>30.0</td><td>40.09</td><td>98.40</td><td>0.0039</td><td>27.38</td><td>88.02</td><td>0.0674</td></tr></table>

<table><tr><td colspan="7">(b) JSCC</td></tr><tr><td colspan="7">AWGN Channel</td></tr><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>24.44</td><td>82.77</td><td>0.1181</td><td>17.67</td><td>74.83</td><td>0.2024</td></tr><tr><td>12.5</td><td>26.01</td><td>85.24</td><td>0.0863</td><td>18.91</td><td>77.75</td><td>0.1987</td></tr><tr><td>15.0</td><td>27.46</td><td>87.80</td><td>0.0581</td><td>19.86</td><td>78.71</td><td>0.1731</td></tr><tr><td>17.5</td><td>30.03</td><td>91.65</td><td>0.0443</td><td>20.71</td><td>81.02</td><td>0.1435</td></tr><tr><td>20.0</td><td>31.83</td><td>94.37</td><td>0.0263</td><td>22.57</td><td>84.90</td><td>0.1165</td></tr><tr><td>22.5</td><td>32.99</td><td>96.25</td><td>0.0165</td><td>23.45</td><td>85.87</td><td>0.1068</td></tr><tr><td>25.0</td><td>34.63</td><td>97.49</td><td>0.0082</td><td>24.27</td><td>86.42</td><td>0.0972</td></tr><tr><td>27.5</td><td>37.83</td><td>98.24</td><td>0.0069</td><td>25.90</td><td>87.02</td><td>0.0872</td></tr><tr><td>30.0</td><td>40.83</td><td>98.58</td><td>0.0035</td><td>27.08</td><td>89.14</td><td>0.0621</td></tr></table>

<table><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>25.60</td><td>84.77</td><td>0.1207</td><td>15.27</td><td>71.29</td><td>0.2135</td></tr><tr><td>12.5</td><td>28.29</td><td>88.57</td><td>0.1070</td><td>17.32</td><td>73.03</td><td>0.2037</td></tr><tr><td>15.0</td><td>28.82</td><td>91.56</td><td>0.0741</td><td>18.97</td><td>76.36</td><td>0.1738</td></tr><tr><td>17.5</td><td>30.51</td><td>93.86</td><td>0.0504</td><td>20.73</td><td>78.78</td><td>0.1455</td></tr><tr><td>20.0</td><td>32.27</td><td>95.58</td><td>0.0334</td><td>22.19</td><td>81.76</td><td>0.1255</td></tr><tr><td>22.5</td><td>33.65</td><td>96.83</td><td>0.0216</td><td>23.03</td><td>83.47</td><td>0.1079</td></tr><tr><td>25.0</td><td>34.87</td><td>97.65</td><td>0.0137</td><td>23.61</td><td>85.92</td><td>0.0998</td></tr><tr><td>27.5</td><td>38.16</td><td>98.12</td><td>0.0091</td><td>25.95</td><td>86.15</td><td>0.0878</td></tr><tr><td>30.0</td><td>40.05</td><td>98.27</td><td>0.0044</td><td>27.09</td><td>86.18</td><td>0.0743</td></tr></table>

(c) JSCC-F

<table><tr><td colspan="7">AWGN Channel</td></tr><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>23.67</td><td>83.47</td><td>0.1242</td><td>20.21</td><td>76.21</td><td>0.2023</td></tr><tr><td>12.5</td><td>25.08</td><td>85.99</td><td>0.0997</td><td>20.83</td><td>77.47</td><td>0.1991</td></tr><tr><td>15.0</td><td>26.62</td><td>87.50</td><td>0.0666</td><td>21.42</td><td>81.53</td><td>0.1759</td></tr><tr><td>17.5</td><td>28.35</td><td>91.07</td><td>0.0464</td><td>21.97</td><td>83.40</td><td>0.1427</td></tr><tr><td>20.0</td><td>29.33</td><td>93.75</td><td>0.0232</td><td>22.44</td><td>85.09</td><td>0.1190</td></tr><tr><td>22.5</td><td>31.69</td><td>95.74</td><td>0.0157</td><td>23.85</td><td>85.62</td><td>0.1006</td></tr><tr><td>25.0</td><td>34.54</td><td>97.09</td><td>0.0077</td><td>24.17</td><td>86.98</td><td>0.0906</td></tr><tr><td>27.5</td><td>37.96</td><td>97.93</td><td>0.0063</td><td>26.37</td><td>87.16</td><td>0.0741</td></tr><tr><td>30.0</td><td>40.37</td><td>98.31</td><td>0.0038</td><td>27.46</td><td>88.19</td><td>0.0657</td></tr></table>

Rayleigh Channel

COVERTNESS METRICS BETWEEN COVER AND PUBLIC STEGO IMAGES

<table><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>25.93</td><td>83.16</td><td>0.1251</td><td>19.93</td><td>72.48</td><td>0.1919</td></tr><tr><td>12.5</td><td>26.20</td><td>85.53</td><td>0.1184</td><td>20.66</td><td>74.92</td><td>0.1712</td></tr><tr><td>15.0</td><td>28.63</td><td>89.94</td><td>0.0735</td><td>21.39</td><td>78.19</td><td>0.1634</td></tr><tr><td>17.5</td><td>29.29</td><td>92.47</td><td>0.0536</td><td>22.10</td><td>79.30</td><td>0.1452</td></tr><tr><td>20.0</td><td>30.26</td><td>94.18</td><td>0.0354</td><td>22.78</td><td>81.22</td><td>0.1297</td></tr><tr><td>22.5</td><td>31.69</td><td>96.15</td><td>0.0174</td><td>23.39</td><td>83.93</td><td>0.1162</td></tr><tr><td>25.0</td><td>34.75</td><td>97.44</td><td>0.0117</td><td>23.89</td><td>85.42</td><td>0.0978</td></tr><tr><td>27.5</td><td>37.31</td><td>98.19</td><td>0.0099</td><td>25.24</td><td>86.70</td><td>0.0937</td></tr><tr><td>30.0</td><td>38.90</td><td>98.44</td><td>0.0047</td><td>26.37</td><td>87.80</td><td>0.0730</td></tr></table>

<table><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>25.06</td><td>83.26</td><td>0.1353</td><td>17.80</td><td>72.98</td><td>0.1973</td></tr><tr><td>12.5</td><td>27.24</td><td>86.28</td><td>0.1062</td><td>19.00</td><td>74.53</td><td>0.1738</td></tr><tr><td>15.0</td><td>28.58</td><td>90.95</td><td>0.0799</td><td>20.11</td><td>78.55</td><td>0.1597</td></tr><tr><td>17.5</td><td>29.18</td><td>92.55</td><td>0.0543</td><td>21.16</td><td>79.16</td><td>0.1511</td></tr><tr><td>20.0</td><td>31.09</td><td>94.26</td><td>0.0352</td><td>22.15</td><td>81.39</td><td>0.1335</td></tr><tr><td>22.5</td><td>32.48</td><td>96.20</td><td>0.0185</td><td>23.04</td><td>83.30</td><td>0.1141</td></tr><tr><td>25.0</td><td>34.58</td><td>97.53</td><td>0.0122</td><td>23.76</td><td>85.91</td><td>0.0954</td></tr><tr><td>27.5</td><td>37.72</td><td>98.30</td><td>0.0094</td><td>25.25</td><td>86.24</td><td>0.0861</td></tr><tr><td>30.0</td><td>41.05</td><td>98.61</td><td>0.0036</td><td>27.43</td><td>87.32</td><td>0.0711</td></tr></table>

(d) JSCC-Q

TABLE V

<table><tr><td>Metric</td><td>Mean</td><td>Std</td></tr><tr><td>PSNR, cover vs stego, dB</td><td>38.31</td><td>3.90</td></tr><tr><td>SSIM, cover vs stego, %</td><td>99.39</td><td>4.72</td></tr><tr><td>Hist-L1 distance</td><td>77.58</td><td>38.86</td></tr><tr><td>HF ratio, cover</td><td>0.0571</td><td>0.0406</td></tr><tr><td>HF ratio, stego</td><td>0.0560</td><td>0.0397</td></tr><tr><td>HF ratio diff, stego-cover</td><td> $-1.13 \times 10^{-3}$ </td><td> $8.18 \times 10^{-3}$ </td></tr></table>

<table><tr><td colspan="7">AWGN Channel</td></tr><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>25.89</td><td>88.55</td><td>0.1075</td><td>17.96</td><td>71.12</td><td>0.1874</td></tr><tr><td>12.5</td><td>27.16</td><td>91.05</td><td>0.0957</td><td>18.93</td><td>79.67</td><td>0.1834</td></tr><tr><td>15.0</td><td>28.56</td><td>93.04</td><td>0.0680</td><td>19.35</td><td>80.87</td><td>0.1510</td></tr><tr><td>17.5</td><td>30.13</td><td>94.62</td><td>0.0393</td><td>20.84</td><td>82.39</td><td>0.1333</td></tr><tr><td>20.0</td><td>32.94</td><td>95.84</td><td>0.0191</td><td>22.76</td><td>85.15</td><td>0.1068</td></tr><tr><td>22.5</td><td>34.00</td><td>96.75</td><td>0.0120</td><td>24.61</td><td>85.90</td><td>0.0956</td></tr><tr><td>25.0</td><td>36.21</td><td>97.39</td><td>0.0079</td><td>25.31</td><td>86.43</td><td>0.1054</td></tr><tr><td>27.5</td><td>37.94</td><td>97.75</td><td>0.0067</td><td>26.70</td><td>86.69</td><td>0.0830</td></tr><tr><td>30.0</td><td>37.92</td><td>97.86</td><td>0.0043</td><td>27.69</td><td>87.67</td><td>0.0684</td></tr></table>

Rayleigh Channel

<table><tr><td>SNR (dB)</td><td>SemCom PSNR (dB)↑</td><td>SemCom SSIM (%)↑</td><td>SemCom LPIPS↓</td><td>Secret PSNR (dB)↑</td><td>Secret SSIM (%)↑</td><td>Secret LPIPS↓</td></tr><tr><td>10.0</td><td>26.12</td><td>85.79</td><td>0.1240</td><td>18.88</td><td>71.33</td><td>0.2074</td></tr><tr><td>12.5</td><td>27.27</td><td>89.24</td><td>0.1112</td><td>19.58</td><td>74.83</td><td>0.1959</td></tr><tr><td>15.0</td><td>28.52</td><td>91.82</td><td>0.0721</td><td>20.30</td><td>78.16</td><td>0.1644</td></tr><tr><td>17.5</td><td>29.93</td><td>93.75</td><td>0.0442</td><td>21.02</td><td>79.30</td><td>0.1312</td></tr><tr><td>20.0</td><td>31.53</td><td>95.18</td><td>0.0286</td><td>22.73</td><td>82.23</td><td>0.1234</td></tr><tr><td>22.5</td><td>33.41</td><td>96.24</td><td>0.0252</td><td>23.41</td><td>85.93</td><td>0.1149</td></tr><tr><td>25.0</td><td>35.58</td><td>96.98</td><td>0.0129</td><td>24.02</td><td>86.39</td><td>0.0961</td></tr><tr><td>27.5</td><td>37.80</td><td>97.68</td><td>0.0087</td><td>25.46</td><td>86.61</td><td>0.0860</td></tr><tr><td>30.0</td><td>38.81</td><td>97.68</td><td>0.0041</td><td>27.66</td><td>87.57</td><td>0.0733</td></tr></table>

TABLE VI

STEGANALYSIS RESULTS ON COVERTNESS UNDER IDENTICAL SETTINGS

<table><tr><td>Detector</td><td>Acc (%)</td><td>TPR</td><td>FPR</td><td>BAcc</td><td>Score $_c$ </td><td>Score $_s$ </td></tr><tr><td>StegExpose</td><td>-</td><td>0.760</td><td>0.595</td><td>0.583</td><td>0.3160</td><td>0.3505</td></tr><tr><td>SRNetLite</td><td>38.33</td><td>-</td><td>-</td><td>-</td><td>0.4402</td><td>0.3963</td></tr><tr><td>HiNetDetectorLite</td><td>45.00</td><td>-</td><td>-</td><td>-</td><td>0.4708</td><td>0.4677</td></tr></table>

Acc denotes test accuracy. BAcc denotes balanced accuracy. Score/Scores are mean detector scores for cover/stego

Comparing with Independent Models: To further validate the effectiveness of the proposed joint training model, we compared it with an independent baseline where the SemCom module and the authorized secret recovery branch are trained separately without shared optimization. The results on Tiny-ImageNet under both AWGN and Rayleigh fading channels are summarized in Fig. 7.

![](images/793d041b95a38fbd502d9e87941bba75899b55ffb1ef37181729241993a4a73f.jpg)  
(a) AWGN Channel PSNR Comparisor

![](images/afc212a7817750a4ed92b75c81b0bb35f0fc3eb87ffcaf9cfc868031bf7a1ea8.jpg)  
(b) AWGN Channel SSIM Comparison

![](images/7f5767c3e6e0551180fc55d10df6e5ad901a07f4028a3d99cb2693de89441cd4.jpg)  
(c) AWGN Channel LPIPS Comparison

![](images/ecc719101aab837de87fee594de597e1c2878857bdf4d2303e27e832679d38c5.jpg)  
(d) Rayleigh Fading Channel PSNR Comparison

![](images/e59ec31017b8e0025b3c621e4445b1d5f7202d57e52aab3ae39b35f1261c75dc.jpg)  
(e) Rayleigh Fading Channel SSIM Comparison

![](images/9a559d75d7c21037a31a7e1733dfd04b755bdaa27d314b632a1396a62fde96d5.jpg)  
(f) Rayleigh Fading Channel LPIPS Comparisor  
Fig. 7. PSNR (a) (d), SSIM (b) (e), and LPIPS (c) (f) performance comparison under AWGN and Rayleigh channels for both SemCom and secret decoding modules. The joint model outperforms the independent baseline module in terms of SemCom reconstruction and secret image recovery. The performance gain is particularly notable at high SNR, highlighting the effectiveness of joint optimization in enhancing not only pixel-level accuracy and structural similarity but also perceptual quality across diverse channel conditions.

For the SemCom task, the joint model achieves consistently higher fidelity at medium-to-high SNRs. Under AWGN, PSNR improves from 22.36 dB at 10 dB to 49.35 dB at 30 dB SNR, while SSIM rises from 89.0% to 99.7%, outperforming the baseline by over three points. LPIPS also drops steadily to 0.0006, whereas the baseline remains above 0.01 even at high SNR. Similar advantages are observed under Rayleigh fading, confirming the robustness of the joint optimization.

For authorized secret recovery, the joint model consistently and reliably surpasses the baseline as SNR increases. At 30 dB, it achieves 31.3 dB PSNR, 91.3% SSIM, and 0.0445 LPIPS under the AWGN channel, compared with only 27.0 dB, 84.1%, and 0.0541 for the baseline. Under the Rayleigh fading channel, the gap is even larger: 30.9 dB, 92.0%, and 0.0398 versus 25.0 dB, 83.5%, and 0.0778.

Overall, these results clearly highlight that the joint training strategy yields substantial statistical gains in pixel accuracy, structural similarity, and perceptual quality, confirming that coordinated optimization enables more robust SemCom transmission and reliable authorized secret recovery across diverse SNR levels and channel conditions. The performance gains stem from joint optimization, which enables shared semantic representations and adaptive trade-offs between fidelity and robustness, thereby enhancing generalization and resilience over independent models.

Ablating Compression Ratios: To investigate the impact of the compression ratio (CR), we performed an ablation study at a fixed SNR of 30 dB. Results are summarized in Table VII.

For the SemCom task, increasing CR from 0.2 to 0.8 under AWGN boosts PSNR from 14.78 dB to 49.35 dB and SSIM from 60.4% to 99.7%, while under Rayleigh it rises from 14.43 dB to 47.08 dB and from 57.0% to 99.7%. These results confirm that higher CR improves semantic fidelity, though excessive values (e.g., 0.9) may cause slight degradation.

In contrast, authorized secret recovery remains stable across all CR values. Under AWGN, PSNR stays around 31.3 dB with SSIM near 91.3%, and under Rayleigh it remains at 30.9 dB and 91.9%. This invariance demonstrates the robustness of the covert decoding path regardless of compression level.

In general, the ablation shows that CR strongly influences visible SemCom reconstruction, while authorized secret recovery is reliably preserved across diverse settings. The reason is that the SemCom branch is sensitive to CR since higher compression allows richer feature transmission, whereas the secret decoder remains largely unaffected as it relies on stable shared embeddings learned through joint optimization.

TABLE VII  
ABLATION STUDY ON THE IMPACT OF COMPRESSION RATIO (CR) UNDER AWGN AND RAYLEIGH CHANNELS FOR SEMCOM AND SECRET DECODING MODULES (TINY-IMAGENET, 64 × 64)

<table><tr><td rowspan="2">Comp. Rate</td><td colspan="2">SemCom Module</td><td colspan="2">Secret Decoding Module</td></tr><tr><td>PSNR (dB)</td><td>SSIM (%)</td><td>PSNR (dB)</td><td>SSIM (%)</td></tr><tr><td colspan="5">Experiments under AWGN Channel</td></tr><tr><td>0.2</td><td>14.78</td><td>60.38</td><td>31.30</td><td>91.31</td></tr><tr><td>0.3</td><td>15.43</td><td>65.92</td><td>31.28</td><td>91.26</td></tr><tr><td>0.4</td><td>18.97</td><td>86.15</td><td>31.37</td><td>91.22</td></tr><tr><td>0.5</td><td>23.64</td><td>95.73</td><td>31.32</td><td>91.27</td></tr><tr><td>0.6</td><td>25.17</td><td>96.65</td><td>31.31</td><td>91.28</td></tr><tr><td>0.7</td><td>38.68</td><td>99.01</td><td>31.29</td><td>91.25</td></tr><tr><td>0.8</td><td>49.35</td><td>99.73</td><td>31.32</td><td>91.29</td></tr><tr><td>0.9</td><td>26.93</td><td>96.31</td><td>31.27</td><td>91.36</td></tr><tr><td colspan="5">Experiments under Rayleigh Channel</td></tr><tr><td>0.2</td><td>14.43</td><td>56.98</td><td>30.91</td><td>91.87</td></tr><tr><td>0.3</td><td>15.36</td><td>62.41</td><td>30.90</td><td>91.97</td></tr><tr><td>0.4</td><td>19.38</td><td>77.11</td><td>30.97</td><td>91.96</td></tr><tr><td>0.5</td><td>23.73</td><td>91.91</td><td>30.99</td><td>91.86</td></tr><tr><td>0.6</td><td>28.05</td><td>98.01</td><td>30.89</td><td>91.90</td></tr><tr><td>0.7</td><td>39.95</td><td>99.48</td><td>30.87</td><td>91.91</td></tr><tr><td>0.8</td><td>47.08</td><td>99.72</td><td>30.95</td><td>91.95</td></tr><tr><td>0.9</td><td>44.77</td><td>99.59</td><td>30.97</td><td>91.98</td></tr></table>

![](images/015c7641fb6d57f3bd6e68768d326444348cf1a3c8066e3e7409820f24ae7a1b.jpg)

![](images/5bc6af92b444049a3df071497729d9c21431fe2b3a18f8ae943a62d337102748.jpg)

![](images/d3defb8fea335bf057b25b404f7cfb323de424f144a3ef6611af67cb66f3d787.jpg)

![](images/14ea216f2d4affce66841779c053be5200679f05a0dbcef78b3b57e07cae3ee9.jpg)  
Fig. 8. Ablation results for loss weights $\left( \lambda _ { r } , \lambda _ { h } , \lambda _ { u } , \lambda _ { a } \right)$ in the dual-objective joint training.

Ablating Hyperparameter Selection: Section IV-D weights four loss terms by $\lambda _ { r } , \lambda _ { h } , \lambda _ { u } .$ and $\lambda _ { a }$ , where $\lambda _ { r }$ weights the public reconstruction loss, $\lambda _ { h }$ the hiding/covertness regularizer, $\lambda _ { u }$ the unauthorized-branch constraint, and $\lambda _ { a }$ the authorized secret recovery objective. We vary one weight at a time and track authorized secret PSNR, unauthorized reconstruction PSNR, and unauthorized SSIM. Fig. 8 shows that $\lambda _ { r }$ mainly affects public fidelity: increasing $\lambda _ { r }$ tends to improve unauthorized SSIM, while authorized PSNR stays nearly unchanged; we thus set $\lambda _ { r } { = } 1 . 0$ . The sweep over $\lambda _ { h }$ does not yield a consistent improvement; the most reliable overall trade-off is achieved at $\lambda _ { h } { = } 0 . 0 1$ , so we set $\lambda _ { h } { = } 0 . 0 1$ . By contrast, increasing $\lambda _ { u }$ severely degrades both authorized and unauthorized reconstruction; therefore, we set $\lambda _ { u } = 0 . 0 1$ as a small stabilizing weight to avoid this degradation while still retaining a mild constraint on the unauthorized branch. Finally, $\lambda _ { a }$ provides a sharp gain from $\lambda _ { a } { = } 0$ and then quickly saturates; we fix $\lambda _ { a } \mathrm { = } 0 . 0 5$ as a stable point with near-saturated authorized recovery while avoiding unnecessary emphasis that may weaken separation. Overall, these settings provide a balanced trade-off among authorized recovery, unauthorized degradation, and public semantic fidelity.

TABLE VIII  
IMPACT OF IMAGE RESOLUTION SCALING ON PUBLIC AND SECRET RECONSTRUCTION QUALITY, REPORTED AS AVERAGE PSNR AND SSIM

<table><tr><td rowspan="2">Resolution</td><td colspan="2">Public branch</td><td colspan="2">Secret branch</td></tr><tr><td>PSNR (dB)</td><td>SSIM (%)</td><td>PSNR (dB)</td><td>SSIM (%)</td></tr><tr><td>64 × 64</td><td>43.23</td><td>99.80</td><td>28.71</td><td>91.95</td></tr><tr><td>256 × 256</td><td>49.35</td><td>99.73</td><td>31.32</td><td>91.29</td></tr><tr><td>512 × 512</td><td>47.54</td><td>99.59</td><td>30.83</td><td>92.32</td></tr></table>

Ablating Network Architectures: To justify the CNN-based backbone selection, we provide an architecture ablation study in the detailed supplementary material, where representative candidate structures are compared under the same settings.

Ablating Image Resolution: The experimental setup in our main results uses a fixed input resolution of $2 5 6 \times 2 5 6$ for stable training and evaluation. To address the concern on resolution scaling, we further evaluate the proposed framework on three representative resolutions, namely $6 4 \times 6 4 , ~ 2 5 6 \times 2 5 6$ , and $5 1 2 \times 5 1 2$ , and report the average reconstruction quality on both the public SemCom branch and the secret recovering branch. Table VIII summarizes the results. For the public SemCom branch, the reconstruction fidelity remains consistently high across resolutions. The best PSNR is achieved at $2 5 6 \times 2 5 6$ with 49.35 dB, and it only mildly decreases at $5 1 2 \times 5 1 2 \tan 4 7 . 5 4 \mathrm { d B }$ SSIM remains above 99.59% for all cases, indicating strong semantic fidelity under resolution scaling. For the secret branch, the recovered secret quality also remains stable. The highest secret PSNR is obtained at $2 5 6 \times 2 5 6$ with 31.32 dB, while the best SSIM is achieved at $5 1 2 \times 5 1 2$ with 92.32%. Overall, the proposed authorizable SemCom framework generalizes well to different image resolutions, maintaining robust public reconstruction and reliable covert recovery under resolution scaling.

## D. Computational Overhead and Latency

We further quantify the overhead introduced by the proposed authorizable pipeline. Compared with a conventional SemCom system using JSCC only, our framework adds a Secret Hiding module at the transmitter and a SecretDecoder branch at the receiver. We report parameter counts, FLOPs, inference latency, and peak memory, summarized in Table IX. Overall, the overhead is lightweight and acceptable for practical SemCom deployment.

Model $S i z e$ and Computation: The added modules introduce minor parameter overhead, increasing the transmitter parameters from 6.382 M to 6.535 M and the receiver parameters from 6.375 M to 6.501 M. Floating-point Operations(FLOPs)

TABLE IX  
OVERHEAD OF THE PROPOSED AUTHORIZABLE PIPELINE

<table><tr><td>Metric</td><td>JSCC</td><td>Proposed</td><td>OH</td></tr><tr><td>Params at Tx (M)</td><td>6.382</td><td>6.535</td><td>+0.153 (2.4%)</td></tr><tr><td>Params at Rx (M)</td><td>6.375</td><td>6.501</td><td>+0.126 (2.0%)</td></tr><tr><td>FLOPs at Tx (G)</td><td>23.941</td><td>28.774</td><td>+4.833 (20.2%)</td></tr><tr><td>FLOPs at Rx (G)</td><td>347.029</td><td>347.546</td><td>+0.517 (0.15%)</td></tr><tr><td>Latency at Tx (ms/img)</td><td>3.174</td><td>3.771</td><td>+0.597 (18.8%)</td></tr><tr><td>Latency at Rx (ms/img)</td><td>14.354</td><td>14.628</td><td>+0.274 (1.9%)</td></tr><tr><td>E2E lat., mod. sum $^{\dagger}$ </td><td>17.528</td><td>18.399</td><td>+0.871 (~ 5%)</td></tr><tr><td>E2E lat., wall-clock $^{\ddagger}$ </td><td>59.36</td><td>62.70</td><td>+3.35 (5.64%)</td></tr><tr><td>Peak mem at Tx $^{*}$  (MB)</td><td>236.5</td><td>236.5 / 100.5</td><td>-</td></tr><tr><td>Peak mem at Rx $^{*}$  (MB)</td><td>444.5</td><td>444.5 / 62.7</td><td>-</td></tr></table>

†Sum of module-forward latencies at Tx and Rx. Wall-clock profiling under AWGN, SNR = 30 dB, $C R = 0 . 8 ,$ 10 trials, 20 warm-up, 120 runs. \* Peak memory measured per-module; end-to-end overhead is typically smaller.

TABLE X  
LATENCY OVERHEAD OF REPRESENTATIVE COVERT BASELINES INTEGRATED INTO THE SAME INFERENCE PIPELINE UNDER AWGN, SNR = 30 DB, CR = 0.8

<table><tr><td>Baseline</td><td>OH (ms)</td><td>OH (%)</td></tr><tr><td>Spread-spectrum signalling (SS)</td><td>+2.690</td><td>+4.53</td></tr><tr><td>Noise-adaptive power control (NAPC)</td><td>+2.814</td><td>+4.74</td></tr></table>

exhibit an asymmetric overhead across sides. On the receiver, SecretDecoder contributes only 0.517 GFLOPs on top of the 347.029 GFLOPs decoder, leading to negligible computation increase. On the transmitter, Hide adds 4.833 GFLOPs to the 23.941 GFLOPs encoder, resulting in a moderate increase.

Latency: This overhead remains small at the system level. Module-level profiling shows 0.597 ms and 0.274 ms additional latency at the transmitter and receiver, yielding an end-to-end model-summed increase of 0.871 ms per image, around 5%. Wall-clock end-to-end profiling under AWGN with SNR <sub>=</sub> 30 dB and CR <sub>=</sub> 0 8 reports 59.36 ms per image for JSCC and 62.70 ms per image for the proposed pipeline, corresponding to 3.35 ms and 5.64% overhead. The absolute difference between model-summed and wall-clock latency is expected, since wall-clock timing captures system-level overheads such as data movement and runtime scheduling, while both measurements consistently indicate a lightweight overhead. For reference in Table X, representative covert baseband modules integrated into the same pipeline incur comparable millisecond-level overheads, ensuring practical viability.

Peak Memory: It is still dominated by the JSCC backbone. When profiling each module, the encoder and decoder peak at 236.5 MB and 444.5 MB, while Hide and SecretDecoder peak at 100.5 MB and 62.7 MB. In the end-to-end pipeline, sequential execution and feature reuse typically make the effective additional memory smaller than a naive summation.

## E. Robustness Defense Experiments

This section presents a comprehensive evaluation of the proposed framework’s robustness against various adversarial manipulations and model perturbations. The experiments are designed to assess the model’s defense capability in maintaining both SemCom transmission and authorized secret reconstruction under representative attack scenarios, including model extraction (stealing), knowledge distillation, network pruning, system fine-tuning, token-generator inversion, and explainability-based (Grad-CAM) probing. All attack experiments are conducted within a unified experimental environment using the Tiny-ImageNet dataset. The evaluation employs three quantitative metrics—PSNR, SSIM, and KL divergence—to jointly measure the reconstruction quality and stability of both regular SemCom outputs and confidential secret recovery under different adversarial conditions.

TABLE XI  
RESULTS OF MODEL EXTRACTION (BLACK-BOX STEALING) UNDER AWGN CHANNEL (SNR = 30 DB, CR = 0.8)

<table><tr><td rowspan="2">Task</td><td colspan="2">SemCom Transmission</td><td colspan="2">Secret Reconstruction</td></tr><tr><td>PSNR (dB)</td><td>SSIM (%)</td><td>PSNR (dB)</td><td>SSIM (%)</td></tr><tr><td>Teacher</td><td>48.18</td><td>99.7</td><td>31.19</td><td>91.3</td></tr><tr><td>Student (stolen)</td><td>39.30</td><td>98.2</td><td>7.32</td><td>13.1</td></tr><tr><td colspan="5"> $\text{KL}(z_T||z_S)=2.14\times 10^6, \text{KL}(z_S||z_T)=5.97\times 10^6$ </td></tr></table>

TABLE XII

RESULTS OF KNOWLEDGE DISTILLATION ATTACK UNDER AWGN CHANNEL (SNR = 30 DB, CR = 0.8)

<table><tr><td rowspan="2">Task</td><td colspan="2">SemCom Transmission</td><td colspan="2">Secret Reconstruction</td></tr><tr><td>PSNR (dB)</td><td>SSIM (%)</td><td>PSNR (dB)</td><td>SSIM (%)</td></tr><tr><td>Teacher</td><td>49.32</td><td>99.72</td><td>31.19</td><td>91.3</td></tr><tr><td>Student (distil)</td><td>28.46</td><td>94.27</td><td>6.93</td><td>14.9</td></tr><tr><td colspan="5"> $\text{KL}(z_T||z_S) = 1.52 \times 10^7, \quad \text{KL}(z_S||z_T) = 6.83 \times 10^5$ </td></tr></table>

Model Extraction and Stealing: A model-extraction attack was conducted in which an adversary trained a surrogate (student) model to reproduce the mapping from input covers to reconstructed outputs by querying the original system. As shown in Table XI, the surrogate reproduced part of the original SemCom behavior but with degraded reconstruction fidelity: 39.30 dB PSNR and 98.2% SSIM versus 48.18 dB and 99.7% for the original model. When the student encoder was combined with the original secret decoder, secret recovery collapsed to 7.32 dB PSNR and 13.1% SSIM, in contrast to 31.19 dB and 91.3% achieved by the original. The latent feature distributions also diverged strongly, with Kullback–Leibler distances on the order of 10<sup>6</sup>, indicating that the surrogate failed to reconstruct the original semantic representation space. These results demonstrate that although the attacker can approximate visible SemCom reconstructions, it cannot reproduce the hidden secret recovery process, confirming the framework’s robustness against model-stealing attempts.

Knowledge Distillation: We further examined a distillationbased attack in which a student network learns from pixel-level supervision using the original system’s reconstructed outputs as guidance. This attack was conducted under a black-box setting, where the student model was trained using N <sub>=</sub> 5000 black-box queries to the original system. As summarized in Table XII, the student achieved only partial imitation of the original behavior, producing 28.46 dB PSNR and 94.27% SSIM on cover reconstruction compared with 49.32 dB and 99.72% for the original. When its encoder was paired with the original secret decoder, the recovered secret quality dropped sharply to 6.93 dB PSNR and 14.9% SSIM, far below 31.19 dB and 91.3% from the genuine model. The latent-level Kullback–Leibler (KL) divergences $( \mathrm { K L } ( z _ { T } | | z _ { S } ) = 1 . 5 2 \times 1 0 ^ { 7 } ; \mathrm { K L } ( z _ { S } | | z _ { T } ) = 6 . 8 3 \times 1 0 ^ { 5 } )$ further reveal a substantial mismatch in feature distributions. Thus, while the attacker can learn to reproduce superficial SemCom outputs from the original inputs, it fails to recover the non-public secret reconstruction pathway.

TABLE XIII  
EXTERNAL BASELINES UNDER QUERY-LIMITED DISTILLATION ATTACKS IN AWGN WITH SNR = 30 DB

<table><tr><td>Baseline</td><td>Attack setting</td><td>Key results</td></tr><tr><td>Secure SemCom [45]</td><td>Distillation, N = 400</td><td>T-GT: 54.84 dB / 99.98%S-GT: 41.59 dB / 99.84%S-T: 41.44 dB / 99.84%</td></tr><tr><td>Robust SemCom [46]</td><td>Distillation, N = 5000</td><td>Teacher acc: 72.32%Student acc: 53.05%</td></tr></table>

T: teacher, S: student, GT: ground truth.

Comparison with External Secure/Robust SemCom Baselines: We further benchmark two representative open-source secure or robustness-oriented SemCom baselines under the same AWGN setting and a query-limited black-box modelextraction paradigm. The first baseline improves security for deep-learning-based SemCom systems [45]. As summarized in Table XIII, under only N <sub>=</sub> 400 black-box queries at SNR <sub>=</sub> 30 dB, the attacker can train a student that achieves 41.59 dB PSNR and 99.84% SSIM against ground truth, and also closely matches the teacher outputs with 41.44 dB PSNR and 99.84% SSIM, indicating strong extractability of the end-to-end mapping. The second baseline is a robustness-oriented semantic communication system with masked VQ-VAE enabled codebook [46]. With N 5000 queries, the distilled student reaches 53.05% test accuracy compared with the teacher’s 72.32%, suggesting that a non-trivial portion of task capability can still be transferred to the surrogate model. In contrast, our robustness experiments in Tables XI & XII show that although an attacker may partially imitate the visible SemCom reconstruction, the authorized secret recovery pathway cannot be reproduced and collapses under stealing or distillation, demonstrating stronger end-to-end protection under identical channel conditions.

Network Pruning: In this experiment, pruning was conducted across all network components with sparsity ratios of 10%, 15%, and 20% to assess the framework’s tolerance to structural sparsification. As shown in Table XIV, the proposed system retains high SemCom transmission fidelity under moderate pruning. At a 10% sparsity level, the SemCom path maintains 42.99 dB PSNR and 99.72% SSIM, while the secret reconstruction still achieves 30.66 dB PSNR and 90.97% SSIM. Noticeable degradation appears only when pruning exceeds 15–20%, where SemCom and secret PSNRs decline by approximately 10–17 dB and 2–4 dB, respectively. Even under the highest pruning level, SSIM remains above 89% and KL divergence exhibits limited increase, demonstrating that the framework preserves robust transmission quality and stable feature integrity under global parameter reduction.

TABLE XIV  
PERFORMANCE UNDER DIFFERENT PRUNING RATIOS (AWGN, SNR = 30 DB, CR = 0.8). SSIM IN PERCENT.

<table><tr><td rowspan="2">Pruning Ratio</td><td colspan="3">SemCom</td><td colspan="3">Secret</td></tr><tr><td>PSNR (dB)</td><td>SSIM (%)</td><td>KL ( $\times 10^{-3}$ )</td><td>PSNR (dB)</td><td>SSIM (%)</td><td>KL ( $\times 10^{-1}$ )</td></tr><tr><td>0% (None)</td><td>49.88</td><td>99.78</td><td>6.56</td><td>31.33</td><td>91.34</td><td>4.16</td></tr><tr><td>10%</td><td>42.99</td><td>99.72</td><td>10.76</td><td>30.66</td><td>90.97</td><td>4.40</td></tr><tr><td>15%</td><td>39.50</td><td>99.57</td><td>16.87</td><td>28.92</td><td>89.88</td><td>4.45</td></tr><tr><td>20%</td><td>32.48</td><td>99.17</td><td>43.32</td><td>26.79</td><td>89.29</td><td>5.54</td></tr></table>

TABLE XV

SYSTEM FINE-TUNING ATTACK (WEAK) UNDER AWGN (SNR = 30 DB, CR = 0.8)

<table><tr><td>Setting</td><td>Task</td><td>PSNR (dB)</td><td>SSIM (%)</td><td>KL</td></tr><tr><td rowspan="2">Pre-Attack</td><td>SemCom</td><td>49.3785</td><td>99.73</td><td>0.010274</td></tr><tr><td>Secret</td><td>31.3243</td><td>91.29</td><td>0.305922</td></tr><tr><td rowspan="2">Post-Finetuned</td><td>SemCom</td><td>49.1512</td><td>99.71</td><td>0.010255</td></tr><tr><td>Secret</td><td>30.4684</td><td>89.22</td><td>0.311864</td></tr><tr><td rowspan="2"> $\Delta$ (post-pre)</td><td>SemCom</td><td>-0.2273</td><td>-0.02</td><td> $-1.9 \times 10^{-5}$ </td></tr><tr><td>Secret</td><td>-0.8559</td><td>-2.07</td><td> $+5.94 \times 10^{-3}$ </td></tr></table>

TABLE XVI

TOKEN-GENERATOR INVERSION RESULTS UNDER AWGN, SNR = 30 DB, CR = 0.8

<table><tr><td>Task</td><td>PSNR (dB)</td><td>SSIM (%)</td><td>KL</td></tr><tr><td>SemCom</td><td>10.90 ± 1.55</td><td>19.02 ± 14.72</td><td>18.033 ± 0.281</td></tr><tr><td>Secret</td><td>106.76 ± 5.34</td><td>100.00 ± 0.00</td><td>0.000010 ± 0.000005</td></tr></table>

System Fine-Tuning: To further assess robustness, a system fine-tuning attack was performed by updating the encoder parameters for two epochs with a learning rate $( 1 \times 1 0 ^ { - 5 } )$ under a preservation-oriented objective. As shown in Table XV, the performance of the framework before and after a weak system fine-tuning attack. Both SemCom and secret reconstruction tasks exhibit minimal degradation. For SemCom, PSNR and SSIM remain nearly unchanged (only −0 23 dB and −0 02%), with a negligible change in KL divergence, indicating that the SemCom transmission capability is well preserved. For the secret reconstruction path, the reductions are slightly larger (−0 86 dB in PSNR and −2 07% in SSIM), yet the overall recovery quality and stability remain intact. These results demonstrate the framework’s strong defense capability and robustness against fine-tuning manipulations.

Token-Generator Inversion Attack: In this experiment, a token-reverse reconstruction attack is performed, where an adversary trains a lightweight generator to transform observed latent tokens—corrupted by noise, masking, downsampling, and channel permutation—into an estimated stego image. The generated stego is then fed into the original system to test whether the protected secret can be recovered. As shown in Table XVI, the reported results compare the reconstructed outputs before and after the inversion attack, reflecting the degradation introduced by the attacker’s reconstruction process. The attacker fails to produce a valid stego input, achieving only 10.9 dB PSNR and 19% SSIM with a large KL divergence, indicating severe distortion and loss of semantic structure. Although the secret reconstruction metrics appear high, they merely result from reusing the legitimate system’s secret decoder during evaluation—an advantage unavailable to any real attacker. The results confirm that the proposed framework effectively blocks SemCom recovery and prevents unauthorized extraction of confidential content against token-reverse reconstruction attacks.

TABLE XVII  
EXPLAINABILITY-BASED PROBING (GRAD-CAM) RESULTS UNDER AWGN (SNR = 30 DB, CR = 0.8)

<table><tr><td>Task</td><td>PSNR (dB)</td><td>SSIM (%)</td><td>KL</td></tr><tr><td>SemCom</td><td>52.18 ± 1.23</td><td>99.89 ± 0.05</td><td>0.002137 ± 0.000375</td></tr><tr><td>Secret</td><td>∞</td><td>100.00 ± 0.00</td><td>0.000000 ± 0.000000</td></tr></table>

Explainability-Based Probing: Grad-CAM heatmaps were applied to identify the most salient input regions, and localized FGSM perturbations were introduced within these areas to examine potential vulnerability to explainability-guided manipulation. As evidenced in Table XVII, the reported values represent the differences between the original (pre-attack) and Grad-CAM–filtered (post-attack) reconstructions. The secret reconstruction remained completely stable, with an effectively infinite PSNR, 100% SSIM, and zero KL divergence, indicating that the secret decoding path was entirely unaffected. The Sem-Com reconstruction also exhibited minimal variation, maintaining 52.18 dB PSNR, 99.89% SSIM, and only a negligible KL change of 0.0021. These results demonstrate that Grad-CAM guided perturbations fail to influence SemCom transmission or degrade confidential secret recovery, confirming the strong robustness and defense capability of our framework against explainability-based probing attacks.

## VI. FUTURE WORK

We plan to further extend our authorizable SemCom framework along two directions. 1) Scalability and Concurrency: Evaluate SemCom transmission and covert recovery under high user density, focusing on concurrent decoding efficiency and dynamic privilege control. 2) Forgery Resistance: Investigate system resilience against covert data forgery by integrating authentication-aware design or lightweight verification mechanisms. 3) Extension to Text and Multimodal SemCom: We focus on image transmission in this study, and will explore extending the authorizable scheme to text and multimodal SemCom in future work. 4) Towards to Generative SemCom Tasks: We will further investigate the feasibility of integrating generative models into the proposed authorizable SemCom framework for generative semantic transmission.

These directions will further enhance scalability, robustness, and security, reinforcing the framework’s applicability in practical secure multi-user SemCom systems.

## VII. CONCLUSION

In this study, we presented an authorizable SemCom framework that integrates image steganography into end-to-end training for covert transmission. Our goal is to achieving highly covert secret transmission within the semantic communication architecture, where secret data is embedded into cover images and can be recovered only by authorized receivers. Specifically, the framework introduces a secret hiding module that injects secret semantics into cover data and a secret decoding module accessible only to authorized users, and co-optimizes them with the semantic and channel encoders via a dual-objective joint training strategy. By operating on latent semantic representations, the proposed design supports authorized covert recovery while preserving the semantic fidelity of public SemCom content. Extensive experiments validate that the framework maintains high reconstruction quality and perceptual consistency across datasets, resolutions, and channel conditions. Moreover, under diverse adversarial manipulations, the system remains stable, preserving SemCom transmission while preventing unauthorized reproduction of the secret recovery pathway.

## REFERENCES

[1] X. Luo, H.-H. Chen, and Q. Guo, “Semantic communications: Overview, open issues, and future research directions,” IEEE Wireless Commun., vol. 29, no. 1, pp. 210–219, Feb. 2022.

[2] C. Chaccour, W. Saad, M. Debbah, Z. Han, and H. V. Poor, “Less data, more knowledge: Building next generation semantic communication networks,” IEEE Commun. Surveys Tuts., vol. 27, no. 1, pp. 37–76, Feb. 2025.

[3] S. Guo et al., “A survey on semantic communication networks: Architecture, security, and privacy,” IEEE Commun. Surveys Tuts., vol. 27, no. 5, pp. 2860–2894, Oct. 2025.

[4] S. Sun, Z. Qin, H. Xie, and X. Tao, “Task-oriented scene graph-based semantic communications with adaptive channel coding,” IEEE Trans. Wireless Commun., vol. 23, no. 11, pp. 17070–17083, Nov. 2024.

[5] P. Yi, Y. Cao, X. Kang, and Y.-C. Liang, “Deep learning-empowered semantic communication systems with a shared knowledge base,” IEEE Trans. Wireless Commun., vol. 23, no. 6, pp. 6174–6187, Jun. 2024.

[6] J. Ren et al., “Knowledge base enabled semantic communication: A generative perspective,” IEEE Wireless Commun., vol. 31, no. 4, pp. 14–22, Aug. 2024.

[7] W. Zhang, H. Zhang, H. Ma, H. Shao, N. Wang, and V. C. M. Leung, “Predictive and adaptive deep coding for wireless image transmission in semantic communication,” IEEE Trans. Wireless Commun., vol. 22, no. 8, pp. 5486–5501, Aug. 2023.

[8] W. Yang et al., “Semantic communications for future internet: Fundamentals, applications, and challenges,” IEEE Commun. Surveys Tuts., vol. 25, no. 1, pp. 213–250, Firstquarter 2023.

[9] Z. Yang, M. Chen, G. Li, Y. Yang, and Z. Zhang, “Secure semantic communications: Fundamentals and challenges,” IEEE Netw., vol. 38, no. 6, pp. 513–520, Nov. 2024.

[10] S. W. Kim and H. Q. Ta, “Covert communications over multiple overt channels,” IEEETrans. Commun., vol. 70, no. 2, pp. 1112–1124, Feb. 2022.

[11] R. Xu et al., “Toward covert and reliable communication for antieavesdropping transmission in V2X networks,” IEEE Trans. Wireless Commun., vol. 24, no. 8, pp. 6429–6442, Aug. 2025.

[12] I. Ahmad et al., “Communications security in industry X: A survey,” IEEE Open J. Commun. Soc., vol. 5, pp. 982–1025, 2024.

[13] B. A. Bash, D. Goeckel, and D. Towsley, “Covert communication gains from adversary’s ignorance of transmission time,” IEEE Trans. Wireless Commun., vol. 15, no. 12, pp. 8394–8405, Dec. 2016.

[14] I. Shakeel, J. Hilliard, W. Zhang, and M. Rice, “Gaussian-distributed spread-spectrum for covert communications,” Sensors, vol. 23, no. 8, 2023, Art. no. 4081.

[15] Z. Zhang, L. Yang, H. Lei, X. Li, and D. Niyato, “Covert communication in RSMA-assisted ambient backscatter communication systems,” IEEE Trans. Wireless Commun., vol. 24, no. 8, pp. 6566–6579, Aug. 2025.

[16] B. A. Bash, D. Goeckel, and D. Towsley, “Square root law for communication with low probability of detection on AWGN channels,” in Proc. IEEE Int. Symp. Inf. Theory., 2012, pp. 448–452.

[17] S. Ma et al., “Robust beamforming design for covert communications,” IEEE Trans. Inf. Forensics Secur., vol. 16, pp. 3026–3038, 2021.

[18] S. Zander, G. Armitage, and P. Branch, “Covert channels and countermeasures in computer network protocols,” IEEE Commun., vol. 45, no. 12, pp. 136–142, Dec. 2007.

[19] S. Bistarelli, A. Imparato, and F. Santini, “A TCP-Based covert channel with integrity check and retransmission,” Int. J. Inf. Secur., vol. 23, no. 6, pp. 3481–3512, 2024.

[20] C. Heinz, W. Mazurczyk, and L. Caviglione, “Covert channels in transport layer security,” in Proc. Eur. Interdiscip. Cybersecur. Conf., 2021, pp. 1–6.

[21] X. Chen et al., “Covert communications: A comprehensive survey,” IEEE Commun. Surveys Tuts., vol. 25, no. 2, pp. 1173–1198, Secondquarter 2023.

[22] S. Zander, G. Armitage, and P. Branch, “A survey of covert channels and countermeasures in computer network protocols,” IEEE Commun. Surveys Tuts., vol. 9, no. 3, pp. 44–57, Thirdquarter 2007.

[23] M. R. Bloch, “Covert communication over noisy channels: A resolvability perspective,” IEEE Trans. Inf. Theory, vol. 62, no. 5, pp. 2334–2354, May 2016.

[24] T. V. Sobers, B. A. Bash, S. Guha, D. Towsley, and D. Goeckel, “Covert communication in the presence of an uninformed jammer,” IEEE Trans. Wireless Commun., vol. 16, no. 9, pp. 6193–6206, Sep. 2017.

[25] C. Wang et al., “Covert communication assisted by UAV-IRS,” IEEE Trans. Commun., vol. 71, no. 1, pp. 357–369, Jan. 2023.

[26] J. Kang et al., “Personalized saliency in task-oriented semantic communications: Image transmission and performance analysis,” IEEE J. Sel. Areas Commun., vol. 41, no. 1, pp. 186–201, Jan. 2023.

[27] W. Zhang, Y. Wang, M. Chen, T. Luo, and D. Niyato, “Optimization of image transmission in cooperative semantic communication networks,” IEEE Trans. Wireless Commun., vol. 23, no. 2, pp. 861–873, Feb. 2024.

[28] X. Peng, Z. Qin, X. Tao, J. Lu, and K. B. Letaief, “A robust image semantic communication system with multi-scale vision transformer,” IEEE J. Sel. Areas Commun., vol. 43, no. 4, pp. 1278–1291, Apr. 2025.

[29] J. Wu et al., “Semantic segmentation-based semantic communication system for image transmission,” Digit. Commun. Netw., vol. 10, no. 3, pp. 519–527, 2024.

[30] D. Huang, F. Gao, X. Tao, Q. Du, and J. Lu, “Toward semantic communications: Deep learning-Based image semantic coding,” IEEE J. Sel. Areas Commun., vol. 41, no. 1, pp. 55–71, Jan. 2023.

[31] D. Huang, X. Tao, F. Gao, and J. Lu, “Deep learning-based image semantic coding for semantic communications,” in Proc. IEEE Glob. Commun. Conf., 2021, pp. 1–6.

[32] C. Liang and D. Li, “Joint source-channel noise adding with adaptive denoising for diffusion-based semantic communications,” in Proc. IEEE Internet Things J., 2025, vol. 12, no. 21, pp. 45909–45912, 2025.

[33] C. Liang and D. Li, “Image generation with supervised selection based on multimodal features for semantic communications,” IEEE Trans. Commun., vol. 73, no. 12, pp. 14469–14485, Dec. 2025.

[34] T.-X. Zheng, Z. Yang, C. Wang, Z. Li, J. Yuan, and X. Guan, “Wireless covert communications aided by distributed cooperative jamming over slow fading channels,” IEEE Trans. Wireless Commun., vol. 20, no. 11, pp. 7026–7039, Nov. 2021.

[35] X. Li et al., “Covert communications with enhanced physical layer security in RIS-assisted cooperative networks,” IEEE Trans. Wireless Commun., vol. 24, no. 7, pp. 5605–5619, Jul. 2025.

[36] S. Baluja, “Hiding images in plain sight: Deep steganography,” in Proc. Adv. Neural Inf. Process. Syst., 2017, vol. 30, pp. 2066–2076.

[37] Z. Zhou et al., “Secret-to-image reversible transformation for generative steganography,” IEEE Trans. Dependable Secure Comput., vol. 20, no. 5, pp. 4118–4134, Sep./Oct. 2023.

[38] S. Baluja, “Hiding images within images,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 42, no. 7, pp. 1685–1697, Jul. 2020.

[39] J. Jing, X. Deng, M. Xu, J. Wang, and Z. Guan, “Hinet: Deep image hiding by invertible network,” in Proc. IEEE/CVF Int. Conf. Comput. Vis., 2021, pp. 4733–4742.

[40] G. Li, S. Li, M. Li, X. Zhang, and Z. Qian, “Steganography of steganographic networks,” in Proc. AAAI Conf. Artif. Intell., 2023, pp. 5178–5186.

[41] Z. Guan et al., “DeepMIH: Deep invertible network for multiple image hiding,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 45, no. 1, pp. 372–390, Jan. 2023.

[42] Y. Huo, S. Xiang, X. Luo, and X. Zhang, “Image semantic steganography: A way to hide information in semantic communication,” IEEE Trans. Circuits Syst. Video Technol., vol. 35, no. 2, pp. 1951–1960, Feb. 2024.

[43] Y. Le and X. S. Yang, “Tiny imagenet visual recognition challenge,” 2015. [Online]. Available: https://api.semanticscholar.org/CorpusID:16664790

[44] E. Agustsson and R. Timofte, “Ntire 2017 challenge on single image superresolution: Dataset and study,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. Workshops, Jul. 2017, pp. 126–135.

[45] H. N. L. Tan, V.-D. Nguyen, T. Huynh-The, T.-V. Nguyen, and P. L. Vo, “Security improvement for deep learning-based semantic communication systems,” in Proc. Int. Conf. Adv. Technol. Commun., 2024, pp. 717–721.

[46] Q. Hu, G. Zhang, Z. Qin, Y. Cai, G. Yu, and G. Y. Li, “Robust semantic communications with masked VQ-VAE enabled codebook,” IEEE Trans. Wireless Commun., vol. 22, no. 12, pp. 8707–8722, Dec. 2023.
# Secrets in Radio Waves: Towards Practical and Protocol-Agnostic PHY Information Hiding

Guanxiong Shen, Hailang Jia, Junqing Zhang, Senior Member, IEEE, Linning Peng, Member, IEEE, Liquan Chen, Member, IEEE, Aiqun Hu, Member, IEEE, Jun Luo, Fellow, IEEE

Abstract—Physical layer (PHY) information hiding supports critical applications, such as digital fingerprinting for transmitter identification and undetectable side channels for covert communication, and has attracted considerable attention from the research community. One category of prior studies focuses on theoretical analysis, proposing techniques such as artificial noise or reconfigurable intelligent surfaces to enable undetectable covert transmission. However, hardware prototypes are rarely presented due to their algorithmic complexity or hard-to-satisfy assumptions. Another category of studies focuses on system-level solutions, achieving PHY information hiding by customizing existing modulation schemes. However, these methods are typically designed for specific wireless protocols, limiting their generalizability. In this work, we introduce a new PHY information hiding paradigm that differs fundamentally from the previous two categories of approaches. Inspired by recent advancements in other domains such as image information hiding, we migrate encoder-decoder neural networks to the PHY information hiding field, embedding secrets by introducing imperceptible distortions within the preamble waveform. Sim-to-real fine-tuning is additionally proposed to tackle unique challenges, e.g., fading and hardware imperfections. The designed methodology is practical and protocol-agnostic. We provide case hardware prototypes of two commercially popular wireless technologies, i.e., LoRa and Bluetooth Low Energy (BLE), using commodity software-defined radio (SDR) transceivers, demonstrating excellent feasibility and generalizability.

Index Terms—Physical layer security, wireless steganography, information hiding, deep learning, LoRa, Bluetooth Low Energy

## I. INTRODUCTION

Information hiding is a security technique that conceals secrets within other ordinary media such as images and texts [1]. Its practical applications include digital watermarking for intellectual property protection [2], fingerprint embedding for authentication [3], [4], and steganography for covert communications [1], [5]. While conventional information hiding techniques primarily focus on hiding secrets within images, videos, texts, or audio, their application in wireless systems has recently gained increasing attention, particularly at the physical layer (PHY). Concealing secrets within PHY radio waveforms offers distinct advantages over hiding information within payload contents. Specifically, given that most off-theshelf wireless receivers lack access to raw radio waveforms, potential eavesdroppers have to deploy specialized hardware and steganalysis algorithms to detect covert channels, which significantly raises the cost and complexity of launching successful attacks. This characteristic additionally provides inherent stealthiness and imperceptibility. PHY information hiding enables critical applications such as digital fingerprint embedding for transmitter authentication [3] and establishing side channels for covert communication [6]. Consequently, advancing PHY information hiding techniques is of significant importance.

The wireless community has shown considerable interest in developing PHY information hiding and covert communication schemes [7]. Existing studies are roughly divided into two categories, i.e., theory-oriented and system-oriented. The former category of studies focuses on theoretical analysis, utilizing multiple antennas [8], [9], reconfigurable intelligent surface (RIS) [10], [11], or mmWave [12], [13] to achieve directional transmission, thus minimizing signal leakage to the eavesdropper. However, their validation is typically limited to numerical simulations due to algorithmic complexity or hardto-satisfy assumptions. In contrast to these theoretical works, system-oriented studies aim to present practical hardware prototypes based on existing wireless protocols [14], [15], [16], [17], [18]. For instance, the authors in [14] design a wireless steganography technique for the LoRa protocol, where covert messages are embedded by modulating the amplitudes of chirp signals. Similarly, Huang et al. propose a radio frequency (RF) watermarking scheme for narrow-band Internet of Things (NB-IoT) systems [17], which embeds secrets by shifting the I/Q constellations. However, although these approaches are experimentally validated as effective, they are often designed for a specific wireless protocol or modulation scheme, resulting in insufficient generalizability. The development of a protocolagnostic PHY information hiding framework requires further exploration.

The paradigm of information hiding for images [19], [2], [20] and text [21], [22], [23] has been fundamentally changed by deep learning in recent years, whereas its application in

PHY information hiding remains unexplored due to unique challenges. The deep learning-driven information hiding methods typically employ a pair of neural networks, i.e., an encoder-decoder framework, to facilitate secret embedding and extraction [24]. Specifically, Alice utilizes a neural network to embed the secret into a carrier medium, while Bob employs a paired network to extract the hidden information. This approach has proven highly effective in domains such as images and texts. However, to the authors’ best knowledge, the encoder-decoder framework has never been explored in the literature on PHY information hiding. This methodological gap is due to the unique challenges of hiding secrets within radio waves. Unlike images or text, which can be conveyed without significant distortion, radio waves propagate through the air and are inevitably affected by surrounding environments, i.e., fading and hardware imperfections. It is challenging to ensure the survival of secrets after experiencing environmental fading and hardware distortions. Moreover, it is equally critical to ensure the primary communication link remains unaffected by the embedded secrets.

To tackle the above challenges, we propose to embed the secrets within the preamble waveforms. Specifically, we design a pair of encoder-decoder neural networks that can process arbitrary lengths of I/Q samples for secret embedding and extraction. A channel simulator is integrated during the training process, and a sim-to-real fine-tuning scheme is proposed to mitigate fading and hardware distortions. Our main contributions are highlighted as follows:

• We propose a PHY information hiding methodology that employs a neural network to embed secret information as subtle distortions within the preamble waveform, fundamentally differing from prior studies. This methodology enables the design of effective PHY-layer information hiding algorithms through simulation-based learning and is applicable to any wireless communication protocol.

• A pair of neural networks is designed for secret embedding and extraction, capable of processing arbitrary lengths of I/Q samples. A simulation-driven joint training scheme with customized loss functions is introduced, complemented by a sim-to-real fine-tuning technique to mitigate performance degradation when deployed on hardware platforms.

• The proposed scheme is demonstrated on commercially popular narrowband technologies, i.e., LoRa and BLE. Through extensive simulations, we validate the feasibility of the proposed approach. The results demonstrate excellent PHY information hiding performance when the signal-to-noise ratio (SNR) exceeds 10 dB. While the present work focuses on narrowband validation, the framework is extensible to wideband protocols such as Wi-Fi and 5G by adapting the neural network architecture to the target preamble structure.

• We implement functional PHY information hiding prototypes using off-the-shelf software-defined radios (SDRs) for both LoRa and BLE protocols. Experimental results confirm that secret messages can be reliably decoded at the SDR receiver. Furthermore, we validate the scheme’s transparency by utilizing a commodity LoRa receiver and a smartphone to receive the SDR-transmitted LoRa and BLE packets, respectively, demonstrating that the primary communication links remain unaffected by the embedded secrets.

![](images/aeb718d7f71c349b481c80cfd7b4733dbca3f454a0bb6865ddc7ba5de79f4fa6.jpg)  
Fig. 1. Encoder-decoder information hiding framework. Secret embedding and extraction are achieved using a pair of neural networks.

The code, dataset, simulation tools, and reproducible prototypes are publicly available at https://github.com/gxhen/RF steganography.

The rest of the paper is organized as follows: Section II presents the background, motivation, and challenges of this work. Section III provides the system overview, and Section IV details the key components in a PHY information hiding system. The neural network joint-training and sim-to-real finetuning schemes are then introduced in Section V. Section VIII presents experimental evaluations of LoRa and BLE PHY information hiding prototypes, respectively. Section IX reviews related work, discusses applications of PHY information hiding, and highlights our technical advantages. Section X finally concludes the paper.

## II. BACKGROUND AND MOTIVATION

This section first provides background knowledge on information hiding, as well as the LoRa PHY and BLE PHY. After that, we discuss the motivation and key challenges behind our research. Finally, we propose an intuitive solution for designing a practical and protocol-agnostic PHY information hiding system.

## A. Background Knowledge

Information hiding is an ancient technique that conceals secret messages within other ordinary media, e.g., images [19], [2], [25], [20], [26], [27], [28] and texts [22], [23]. The recent advances in deep learning have fundamentally changed the paradigm of information hiding [29], [30], [31], [32]. As illustrated in Fig. 1, the deep learning-driven information hiding system employs a pair of neural networks for secret embedding and extraction. Specifically, Alice utilizes a neural network encoder to embed the secrets within a covert medium, e.g., image or video. Subsequently, Bob employs another paired decoder to extract the hidden secrets. This encoder-decoder framework was first proposed in [19] to hide secrets within images. It was subsequently rapidly developed, and numerous variants have emerged for image, video, and text information hiding, becoming the de facto mainstream in these fields [33], [34], [24], [35], [36]. However, its effective application in the wireless PHY remains unexplored.

LoRa is a low-power wide area network (LPWAN) technology developed from the chirp spreading spectrum (CSS)

![](images/7518d1bcd6ba8393bf4b55478b84142f20d9c61a3bfe29c395590e1187951e1d.jpg)  
(a)

![](images/778773eafa441136037d558a00bebef54e5baa443c7f1726cf2c702c48305919.jpg)  
(b)

![](images/4e389f908b0da7b907511ae187f55951b3d57450e7378e0b060599fbc7b0f09f.jpg)  
(c)

![](images/4a742948e0dfaa834a569eaa8b3b832520f0a069093dfcac14dc3639c99d583e.jpg)  
(d)

![](images/88deb59caa7fd235514a82ff92f107e778830769ab503744e1d12e0d7351eb84.jpg)  
(e)

![](images/49dfb1ae2ce33e77a46ac4ec96f38bc316d1211fe83964bd5aff5d2ecbaf5825.jpg)  
(f)  
Fig. 2. Visualization of preamble waveform (I-branch). (a) Standard LoRa preamble. (b) LoRa preamble with a 60-bit secret embedded. (c) LoRa preamble with a 180-bit secret embedded. (d) Standard BLE preamble. (e) BLE preamble with a 30-bit secret embedded. (f) BLE preamble with a 120- bit secret embedded.

modulation technique. It is patented by Semtech and has been employed in numerous IoT applications where longrange communication is required. A LoRa preamble, i.e., an unmodulated upchirp, is illustrated in Fig. 2(a). Typically, a LoRa packet starts with eight repeating preambles, which play a crucial role in synchronization and packet detection.

BLE is a short-range wireless personal area network (WPAN) technology that utilizes the Gaussian frequency shift keying (GFSK) modulation scheme at the PHY layer. BLE specifies several PHY modes to support varying data rate requirements. In the basic LE1M mode, the wireless packet includes a preamble consisting of a fixed ‘10101010’ bit sequence for packet detection and synchronization. A standard BLE preamble waveform is shown in Fig. 2(d).

## B. Motivation, Challenges and Solutions

This study focuses on embedding secrets directly into radio waveforms, rather than relying on traditional cover media such as images or videos, and designs a practical and protocolagnostic PHY information hiding framework. The motivation is not to replace higher-layer content-based steganography. Instead, PHY information hiding attaches secret information directly to the emitted RF waveform while keeping the packet payload and standard receiver operations unchanged. Since the proposed method embeds information into the radio waveform rather than the packet bits, it remains independent of the carried data type and provides a protocol-agnostic hiding capability.

The applications of the proposed framework, including RF fingerprint embedding and a covert side channel, are discussed in Section IX-B.

The preamble is a natural carrier: it is present in every packet and has a fixed pattern. Embedding secrets into the preamble leaves the payload waveform unchanged, so that standard receivers can demodulate the primary communication link without modification. This paper focuses on preambleonly embedding. Payload-waveform embedding would require a dedicated design, because both the payload length and the payload content vary from packet to packet.

It is important to emphasize that directly migrating algorithms from studies targeting images [19] and text [23] may not be effective. In contrast to images and videos that can be conveyed without distortion, radio waves propagate through the air. The surrounding environments and transceiver hardware imperfections can result in severe fading and distortions within the received signals. It is challenging to ensure the survival of embedded secrets after the radio signal is distorted. Another critical consideration is to ensure the primary communication link remains unaffected by the created covert side channel, which further complicates the system design. This work aims to answer four questions:

i) How to design a practical and protocol-agnostic PHY information hiding paradigm?

ii) How to effectively migrate encoder-decoder neural networks into PHY information hiding?

iii) How to ensure the survival of secrets after the radio undergoes fading and hardware distortions?

iv) How to ensure the primary communication link remains unaffected by the embedded secrets?

To this end, a pair of neural networks is employed, one for embedding the secrets into the preamble and another for extracting them at the receiving end. The distorted LoRa and BLE preambles, with secrets embedded, are visualized in Fig. 2. As observed, the secret embedder introduces slight distortions to the preamble waveform. These distortions become more perceptible as the number of embedded bits increases. However, the synchronization algorithms remain valid. This is because the distorted waveforms are highly similar to the standard preamble, and the repetition property, i.e., a key feature relied upon by synchronization algorithms, is preserved. Consequently, both cross-correlation and autocorrelation-based synchronization algorithms are expected to remain functional on the receiver side, ensuring successful synchronization despite the embedded secrets. This is validated through both simulation and experiments in Sections VII and VIII.

## III. SYSTEM OVERVIEW

As illustrated in Fig. 3, the proposed PHY information hiding system comprises two parties, namely Alice and Bob. They have already established a primary communication link, such as LoRa, BLE, and ZigBee. Alice aims to hide additional covert messages within the transmitted wireless packets. In more detail, the transmitter, Alice, conceals secret messages within the radio waveforms by introducing subtle and imperceptible distortion using a pre-trained neural network called the secret embedder. This secret embedding process only applies to the packet preamble waveform. After Bob receives the radio signal, another neural network called the secret extractor is used to extract the secret messages. Forward error correction (FEC) is utilized to correct transmission errors and enhance information hiding performance. The specific operations on Alice and Bob’s sides are introduced below.

Secret Message Embedding at Alice Side: Alice first performs FEC encoding and interleaving to transform the Mbit secret message into an N-bit codeword. Subsequently, the codeword is embedded into a standard preamble using a pre-trained neural network secret embedder, which introduces subtle and stealthy waveform-level distortions through channel-wise concatenation. The distorted preamble is then concatenated with the payload to generate a complete wireless packet. This is then up-converted from the baseband to the RF band and emitted into the air. The process will be introduced in detail in Section IV-A.

![](images/a936efeeff66a249b592921d14be6152483ce2a67dcdc9305fd44a42822159f9.jpg)  
Fig. 3. Overview of the proposed PHY information hiding system.

Secret Message Extraction at Bob Side: Bob captures the RF signal, down-converts it to baseband, and digitalizes it with an ADC. Then another pre-trained neural network secret extractor is employed to extract the codeword hidden within the packet preamble field. The extracted codeword is then fed into a de-interleaver and an FEC decoder for error correction, thereby recovering the M-bit secret message sent by Alice. The process will be presented in detail in Section IV-B.

It is worth noting that the two neural networks, i.e., secret embedder and extractor, are pre-trained jointly in a controlled environment and are then secretly shared between Alice and Bob. The model weights should be protected and kept secret. The details about simulation-driven training and sim-to-real fine-tuning are given in Section V and Section V-D, respectively.

PHY information hiding offers a method to establish an undetectable covert communication link between wireless transceivers. The reason for this undetectability is twofold. Firstly, most commodity wireless receivers lack the capability to access physical layer waveforms, i.e., I/Q samples. Those attempting to eavesdrop must possess a bespoke wireless receiver, for example, an SDR, to detect the covert channel. This considerably increases the cost required for eavesdropping. Secondly, the intentionally introduced distortion is subtle and almost imperceptible. Although it is difficult to absolutely guarantee the distortion is undetectable under the observation of high-end equipment, the development of dedicated steganalysis algorithms significantly increases the complexity of the attack. In addition to the undetectability, the eavesdropper has to steal the weights of the secret extractor to parse the embedded covert message, which further increases the cost of the attack.

## IV. PHY INFORMATION HIDING SYSTEM

## A. Secret Message Embedding at Alice Side

The goal of Alice is to embed a secret message x into the wireless packet by introducing waveform-level distortion, while not affecting the quality of the primary communication link. This is achieved by the modules detailed below.

1) Forward Error Correction Encoder and Interleaver: Given an M-bit secret message x, Alice first performs FEC encoding to introduce redundancy, given as

$$
\mathbf {c} = \mathcal {F} _ {\mathrm{enc}} (\mathbf {x}),\tag{1}
$$

where $\mathcal { F } _ { \mathrm { e n c } } ( \cdot )$ denotes the FEC encoding process and c is the encoded N-bit codeword. Subsequently, Alice utilizes a random interleaver to rearrange the elements in c, thereby mitigating the impact of burst errors that may occur during transmission.

In the LoRa and BLE case studies, the (15, 5) Bose-Chaudhuri-Hocquenghem (BCH) code is employed. This widely used cyclic error correction code is capable of correcting up to three bit errors per codeword. Other techniques, such as low-density parity-check (LDPC) codes, are also feasible.

2) Secret Embedder: After converting the M-bit secret message x to an N-bit codeword c, Alice utilizes a pre-trained secret embedder to embed it into the preamble s, which is expressed as

$$
\mathbf {u} = \mathcal {G} _ {\mathrm{emb}} (\mathbf {s}, \mathbf {c}; \theta_ {\mathrm{emb}}),\tag{2}
$$

where $\mathcal { G } _ { \mathrm { e m b } } ( \cdot , \cdot ; \theta _ { \mathrm { e m b } } )$ denotes the neural network-based embedding process and $\theta _ { \mathrm { e m b } }$ is the parameter set. It accepts two inputs, i.e., a standard preamble s and a codeword c, and outputs a distorted preamble u.

The architecture of the designed secret embedder is illustrated in Fig. 4(a), which involves nine 1D convolutional layers, i.e., a fully convolutional design. The neural network inputs consist of a standard preamble s and a codeword c. We first perform channel-wise concatenation, combining s and c into a single tensor of size (L, 2+N). This channel-wise concatenation approach is inspired by the image steganography scheme proposed in [19] and is further optimized for RF signals. Specifically, the preamble s, which is a complex vector, is split into real and imaginary parts and serves as two separate channels of the tensor. The codeword c, which is an N-bit binary vector, is duplicated L times along the time-dimension and serves as N channels of the tensor. The combined tensor is then processed by four 1D convolutional layers, with the channel-wise concatenation applied to the output of the fourth layer again to enhance the embedding process. Note that this channel-wise concatenation has three inputs: the standard preamble s, codeword c, and the output tensor of the fourth convolutional layer, producing a tensor of size $( L , 2 5 6 + 2$ + N). Subsequently, four more 1D convolutional layers and channel-wise concatenation are applied to further enhance the message embedding performance. Finally, a 1D convolutional layer with a kernel size of one is utilized, which produces an output tensor of size (L, 2). It represents the real and imaginary parts of the distorted preamble u, respectively. The outputs of all convolutional layers are activated by GELU functions.

![](images/da779963c870afb7e51a7494cc2ec96bc2fab679104671da71962e77228f6357.jpg)  
Fig. 4. Architecture of the neural network-based secret embedder and extractor. (a) Secret embedder. (b) Secret extractor.

Thanks to the fully convolutional design, the secret embedder can hide secrets within preambles of arbitrary length and is applicable to both LoRa and BLE preamble waveforms. However, it should be noted that the codeword length N is fixed once training is complete, and designers should select an appropriate length based on their specific performance and application requirements. This limitation could be addressed in future work through more advanced neural network architectures capable of adapting to variable secret lengths.

The neural network architecture, particularly the input and output layer configurations, exhibits strong dependence on the preamble characteristics of the target wireless protocol. This protocol-specific dependency arises from fundamental differences in preamble structure and length across standards. For example, LoRa and BLE protocols employ waveforms with substantially different temporal durations, requiring corresponding architectural adaptations to accommodate these protocol-specific requirements.

## B. Secret Message Extraction at Bob Side

The radio signal emitted by Alice propagates through the air and is then captured by Bob. It is down-converted to the baseband and subsequently discretized by an ADC. The preamble field of the wireless packet is extracted, denoted as $\mathbf { u } ^ { \prime } .$ Subsequently, a secret extractor, a de-interleaver, and an FEC decoder are employed to process the preamble waveform, as detailed below.

1) Secret Extractor: Bob first uses a pre-trained secret extractor to recover the message hidden in the distorted preamble $\mathbf { u } ^ { \prime } ,$ which is mathematically given as

$$
\hat {\mathbf {c}} = \mathcal {G} _ {\mathrm{ext}} (\mathbf {u} ^ {\prime}; \theta_ {\mathrm{ext}}),\tag{3}
$$

where $\mathcal { G } _ { \mathrm { e x t } } ( \cdot ; \theta _ { \mathrm { e x t } } )$ denotes the neural network-based secret extraction process and $\theta _ { \mathrm { e x t } }$ is the parameter set. It accepts a received preamble u<sup>′</sup> and outputs an estimated codeword ˆc.

The architecture of the neural network extractor is shown in Fig. 4(b), consisting of nine 1D convolutional layers, an adaptive average pooling layer, and a linear layer. First, the received preamble $\mathbf { u } ^ { \prime }$ is normalized by dividing by its root mean square (RMS) power, thereby preventing the signal amplitude from affecting the message extraction results. Then the normalized signal is split into real and imaginary parts and fed sequentially into nine 1D convolutional layers to output N-channel feature maps. Subsequently, an adaptive average pooling layer and a linear layer are employed to transform the feature map into an N-element vector, denoted by v. Finally, the vector v is processed by a sign function, thereby generating a binary codeword, ˆc, where a positive sign denotes 1 and a negative sign denotes 0. The outputs of all convolutional layers are activated by GELU functions.

2) De-Interleaver and Forward Error Correction Decoder: After extracting the codeword ˆc from the packet preamble field, Bob employs the random de-interleaver to reconstruct its original order and then uses an FEC decoder to recover the secret message, which is expressed as

$$
\hat {\mathbf {x}} = \mathcal {F} _ {\mathrm{dec}} (\hat {\mathbf {c}}),\tag{4}
$$

where ${ \mathcal { F } } _ { \mathrm { d e c } }$ represents the FEC decoding process and ˆx denotes the recovered M-bit secret message. The (15, 5) BCH decoder is employed in the LoRa and BLE case studies.

## V. NEURAL NETWORK JOINT TRAINING AND SIM-TO-REAL FINE-TUNING

The neural network–based secret embedder and extractor are fundamental components of the PHY information hiding system. They are jointly trained in a controlled environment, i.e., a physically protected setting, to prevent backdoor, data poisoning, and other training-time attacks [37]. After training, the model weights are securely shared between Alice and Bob. An additional sim-to-real fine-tuning stage may be applied to further enhance performance on practical hardware platforms.

![](images/a30d108ef2c0cf93a5ba6e55ce2a035a2b477a730bb5e3daa2fc53bb10813c31.jpg)  
Fig. 5. Simulation-driven embedder-extractor joint training scheme.

## A. Training Scheme Overview

The joint training process is illustrated in Fig. 5. It can be observed that the communication process between Alice and Bob is emulated with a secret embedder, a wireless channel simulator, and a secret extractor. At the beginning of each training step, a batch of N-bit binary vectors is randomly generated, with the batch size defined as K. More specifically, each element in the binary vector is randomly assigned as 0 or 1, i.e., a uniform distribution. After that, a secret embedder is employed to conceal the message c within the standard preamble s, generating a distorted signal u. Subsequently, a wireless channel simulator is utilized for data augmentation. In particular, it emulates fading, adds noise into u, and outputs an augmented signal u<sup>′</sup>. Finally, a secret extractor is employed to recover the embedded binary vector. The following subsections will elaborate on the design of loss functions and the wireless channel simulator.

## B. Loss Functions

Two loss functions are defined to enforce constraints on the neural network training process, namely a recovery loss $\mathcal { L } _ { \mathrm { r e c o v e r y } }$ and a stealthy loss $\mathcal { L } _ { \mathrm { s t e a l t h y } }$ . The recovery loss $\mathcal { L } _ { \mathrm { r e c o v e r y } }$ measures the difference between the embedded random bits and the output vector, which is mathematically given as

$$
\mathcal {L} _ {\text { recovery }} = \frac {1}{K} \sum_ {k = 1} ^ {K} \frac {\| \mathbf {c} _ {k} - \mathbf {v} _ {k} \| _ {2}}{N},\tag{5}
$$

where $\mathbf { c } _ { k }$ and $\mathbf { v } _ { k }$ represent the embedded random bits and output vector for the k-th sample in the training batch, respectively. Specifically, the vector v denotes the neural network output before the sign function, as illustrated in Fig. 4. The symbol ∥·∥ returns the L2 norm. Meanwhile, the stealthy loss $\mathcal { L } _ { \mathrm { s t e a l t h y } }$ measures the similarity between the standard and distorted preambles, given as

$$
\mathcal {L} _ {\mathrm{stealthy}} = \frac {1}{K} \sum_ {k = 1} ^ {K} \frac {\| \mathbf {u} _ {k} - \mathbf {s} \| _ {2}}{L},\tag{6}
$$

where $\mathbf { u } _ { k }$ denotes the distorted preamble for the k-th training sample. s refers to the standard preamble introduced in Section II-A. The total loss $\mathcal { L } _ { \mathrm { t o t a l } }$ is then defined as

$$
\mathcal {L} _ {\mathrm{total}} = \alpha \cdot \mathcal {L} _ {\mathrm{recovery}} + (1 - \alpha) \cdot \mathcal {L} _ {\mathrm{stealthy}},\tag{7}
$$

where α is a hyperparameter that adjusts the weights of the two losses. In all experiments, α is empirically set to 0.6. Note that for a loss function comprising only two terms, employing a single hyperparameter to weight them is mathematically equivalent to using two separate weights, as the relative ratio is what matters for optimization. The objective of the neural network training process is to find a set of parameters that minimize the loss function $\mathcal { L } _ { \mathrm { t o t a l } }$ , which is mathematically expressed as

![](images/f874fb7d2775a0955bcd9ad6e3b8a001c53fba704f96f154c13ab368ea371bec.jpg)  
Fig. 6. Sim-to-real fine-tuning. The parameters of the secret extractor are finetuned with the signals collected by actual transceiver hardware platforms.

$$
\Theta = \underset {\Theta} {\operatorname{argmin}} \sum_ {\mathbf {c} \in \mathcal {D}} \mathcal {L} _ {\mathrm{total}} (\mathbf {c}; \Theta),\tag{8}
$$

where $\Theta = \theta _ { \mathrm { e m b } } \cup \theta _ { \mathrm { e x t } }$ denotes the parameters of both the secret embedder and extractor. D represents the sample space of the N-bit binary vector c.

In summary, the recovery loss $\mathcal { L } _ { \mathrm { r e c o v e r y } }$ is intended to ensure that the secret message can be successfully embedded and extracted. The stealthy loss $\mathcal { L } _ { \mathrm { s t e a l t h y } }$ constrains the degree of the waveform distortion, making the covert link undetectable to eavesdroppers.

## C. Wireless Channel Simulator

The training process incorporates a wireless channel simulator for data augmentation, which can significantly enhance the neural network’s resilience against channel effects. We consider an additive white Gaussian noise (AWGN) and slow flat-fading in this work, expressed as

$$
\mathbf {u} ^ {\prime} = \mathbf {h} \cdot \mathbf {u} + \mathbf {z},\tag{9}
$$

where h is the complex channel coefficient and z is the additive noise. The coefficient h is generated using the Rayleigh fading model. Only the phase of h is simulated, as the amplitude attenuation does not affect the system performance due to the power normalization module in the secret extractor. The noise vector z is calculated using a random SNR uniformly distributed in the range [0, 60] dB.

## D. Sim-to-Real Fine-Tuning

The scheme introduced in previous subsections leverages simulation data to jointly train a pair of secret embedder and extractor. However, due to the inevitable discrepancy between the simulated and experimental data, the model performance often degrades in practical environments. To address this issue, we propose a sim-to-real fine-tuning scheme as a mitigation approach.

In essence, the sim-to-real fine-tuning scheme is the use of experimentally collected data to calibrate the parameters $\theta _ { \mathrm { e x t } }$ of the secret extractor $\mathcal { G } _ { \mathrm { e x t } }$ , which is illustrated in Fig. 6. This can effectively mitigate performance degradation caused by simulation-to-reality gaps, e.g., hardware imperfections, when the models are deployed on actual transceiver hardware platforms. Firstly, we deploy the secret embedder $\theta _ { \mathrm { e m b } }$ and extractor $\theta _ { \mathrm { e x t } }$ on the transmitter and receiver, respectively, and use this hardware system to collect a fine-tuning dataset $\mathcal { D } ^ { \mathrm { t u n e } }$ given as

$$
\mathcal {D} ^ {\mathrm{tune}} = \{(\mathbf {u ^ {\prime}} _ {i}, \mathbf {c} _ {i}) \} _ {i = 1} ^ {I},\tag{10}
$$

where I denotes the number of samples in the dataset $\mathcal { D } ^ { \mathrm { t u n e } }$ $\mathbf { u } _ { \mathit { i } } ^ { \prime }$ is the i-th signal collected by the receiver hardware, and $\mathbf { c } _ { i }$ is the corresponding ground-truth codeword. After the collection of $\mathcal { D } ^ { \mathrm { t u n e } }$ is complete, we first input the received signal $\mathbf { u } ^ { \prime }$ into the simulation-trained secret extractor $\mathcal { G } _ { \mathrm { e x t } }$ , and then fine-tune the parameter set $\theta _ { \mathrm { e x t } }$ using the recovery loss $\mathcal { L } _ { \mathrm { r e c o v e r y } }$ defined in (5).

In summary, the simulation-trained deep learning models tend to experience performance degradation when deployed on practical hardware platforms. To address this issue, we propose to fine-tune the secret extractor $\mathcal { G } _ { \mathrm { e x t } }$ using realcollected wireless signals in a controlled short-range, high-SNR LOS setting. This approach aims to adapt the model to the specific hardware distortions, such as I/Q imbalance and nonlinearity of the power amplifier, rather than to adapt to a particular channel state. Robustness to time-varying channels is mainly provided by the wireless channel simulator and data augmentation in the joint training stage. After fine-tuning, the model weights remain fixed and are directly tested in other locations and channel conditions without per-location recalibration.

Note that the sim-to-real fine-tuning is not a mandatory step. The experimental results in Section VIII will demonstrate that the simulation-trained neural networks already achieve excellent information hiding performance, and sim-to-real fine-tuning can further enhance the performance. It is crucial to emphasize that the fine-tuning process must be conducted in a controlled environment, which is essential to prevent an attacker from training a surrogate neural network to achieve model stealing [38].

## VI. EVALUATION METRICS

Raw Secret Bit Error Rate: The raw secret bit error rate (SBER), denoted by $\mathrm { S B E R } _ { r a w } ,$ measures the difference between the embedded and extracted codewords, i.e., c and ˆc, which is mathematically given as

$$
\mathrm{SBER} _ {r a w} = \frac {\mathcal {H} (\mathbf {c} , \hat {\mathbf {c}})}{N},\tag{11}
$$

where $\mathcal { H } ( \cdot , \cdot )$ calculates the Hamming distance between two binary vectors. The raw SBER metric directly measures the performance of the secret embedder and extractor without the benefit of any error correction technique.

Secret Bit Error Rate after FEC: The FEC-SBER, denoted by $\mathrm { S B E R } _ { f e c } ,$ , measures the difference between the embedded and extracted secret messages, i.e., x and ˆx, which is expressed as

$$
\mathrm{SBER} _ {f e c} = \frac {\mathcal {H} (\mathbf {x} , \hat {\mathbf {x}})}{M}.\tag{12}
$$

$\mathrm { S B E R } _ { f e c }$ is typically lower than $\mathrm { S B E R } _ { r a w }$ since the FEC technique can correct some or all of the errors.

Secret Message Error Rate: The secret message error rate (SMER) is defined as the ratio between the number of erroneous secret messages $E _ { \mathrm { e r r } }$ and the total number of transmitted secret messages $E _ { \mathrm { t o t a l } } ,$ given as

$$
\mathrm{SMER} = \frac {E _ {\mathrm{err}}}{E _ {\mathrm{total}}}.\tag{13}
$$

It evaluates the overall quality of the established covert link at the packet level. A high SMER indicates severe secret extraction errors.

Packet Loss Rate: The packet loss rate (PLR) quantifies the reliability of the primary communication link at the packet level. It is defined as the ratio of packets that are either misdetected or fail the cyclic redundancy check (CRC) to the total number of transmitted packets:

$$
\mathrm{PLR} = \frac {P _ {\mathrm{lost}}}{P _ {\mathrm{total}}},\tag{14}
$$

where $P _ { \mathrm { l o s t } }$ denotes the number of lost packets and $P _ { \mathrm { t o t a l } }$ is the total number of transmitted packets. A packet is regarded as lost if the receiver fails to synchronize with the preamble or if the header or payload decoding fails the CRC validation. Importantly, the PLR reflects the impact of the preamble-based secret embedding on the primary communication link and does not evaluate the performance of the covert channel.

## VII. SIMULATION EVALUATION

## A. Simulation Configuration

1) LoRa and BLE PHY Configuration: The LoRa PHY is implemented in MATLAB, building upon the existing reverseengineering study [39]. The spreading factor and bandwidth are set to 7 and 500 kHz, respectively. The sampling rate is configured to 1 MHz. In this PHY configuration, the LoRa preamble field contains 2,048 I/Q samples, which is visualized in Fig. 2(a).

The BLE PHY is developed based on the official MATLAB Bluetooth toolbox <sup>1</sup>. The BLE PHY mode is set to LE1M, where the packet preamble is $\textrm { a } \cdot 1 0 1 0 1 0 1 0 ^ { \circ }$ sequence. Each BLE symbol contains 16 I/Q samples. In this configuration, the preamble waveform contains 128 I/Q samples, which is visualized in Fig. 2(d).

In both LoRa and BLE cases, we simulate 5,000 independent wireless packets and record the $\mathrm { S B E R } _ { r a w }$ , SMER, and PLR for subsequent analysis.

2) Neural Network Configuration: The neural networks are implemented with the PyTorch library. The secret embedder and extractor are trained in pairs as described in Section V. The RMSprop optimizer is employed during the training process with a batch size of 64. The initial learning rate is set to 0.0003, and if the validation loss does not decrease within 10 epochs, the current learning rate is reduced by a factor of 0.1, i.e., a reduce-on-plateau scheduler. Training stops when the validation loss does not decrease for 20 epochs.

TABLE I  
SIMULATION RESULTS OF PHY INFORMATION HIDING FOR LORA AND BLE PROTOCOLS.

<table><tr><td rowspan="2">Protocol</td><td rowspan="2">Secret Length</td><td rowspan="2">Metrics</td><td colspan="9">SNR</td></tr><tr><td>-10 dB</td><td>-5 dB</td><td>0 dB</td><td>5 dB</td><td>10 dB</td><td>15 dB</td><td>20 dB</td><td>25 dB</td><td>30 dB</td></tr><tr><td rowspan="10">LoRa</td><td rowspan="3">60 bit</td><td> $SBER_{raw}$ </td><td>0.4851</td><td>0.3776</td><td>0.1445</td><td>0.0174</td><td>0.0022</td><td>0.0017</td><td>0.0017</td><td>0.002</td><td>0.0019</td></tr><tr><td>SMER</td><td>1</td><td>0.9992</td><td>0.447</td><td>0.0028</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>PLR</td><td>0.6406</td><td>0.0038</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td rowspan="3">120 bit</td><td> $SBER_{raw}$ </td><td>0.4865</td><td>0.4193</td><td>0.2237</td><td>0.0631</td><td>0.0246</td><td>0.0175</td><td>0.0163</td><td>0.0162</td><td>0.0159</td></tr><tr><td>SMER</td><td>1</td><td>1</td><td>0.97</td><td>0.1036</td><td>0.007</td><td>0.004</td><td>0.0028</td><td>0.0022</td><td>0.0022</td></tr><tr><td>PLR</td><td>0.6882</td><td>0.0046</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td rowspan="3">180 bit</td><td> $SBER_{raw}$ </td><td>0.4933</td><td>0.4424</td><td>0.2678</td><td>0.1144</td><td>0.0626</td><td>0.0513</td><td>0.0478</td><td>0.0467</td><td>0.0466</td></tr><tr><td>SMER</td><td>1</td><td>1</td><td>0.9996</td><td>0.6156</td><td>0.1394</td><td>0.0814</td><td>0.0724</td><td>0.0628</td><td>0.0618</td></tr><tr><td>PLR</td><td>0.6308</td><td>0.0088</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>No secret</td><td>PLR</td><td>0.4978</td><td>0.0034</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td rowspan="10">BLE</td><td rowspan="3">60 bit</td><td> $SBER_{raw}$ </td><td>0.4729</td><td>0.4011</td><td>0.2621</td><td>0.1116</td><td>0.0378</td><td>0.0173</td><td>0.0135</td><td>0.0116</td><td>0.0112</td></tr><tr><td>SMER</td><td>1</td><td>1</td><td>0.9447</td><td>0.2606</td><td>0.012</td><td>0.0024</td><td>0.0018</td><td>0.0016</td><td>0.0006</td></tr><tr><td>PLR</td><td>0.9762</td><td>0.0764</td><td>0.0004</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td rowspan="3">120 bit</td><td> $SBER_{raw}$ </td><td>0.4785</td><td>0.4333</td><td>0.3378</td><td>0.2139</td><td>0.1221</td><td>0.079</td><td>0.0651</td><td>0.0599</td><td>0.0591</td></tr><tr><td>SMER</td><td>1</td><td>1</td><td>1</td><td>0.9726</td><td>0.5428</td><td>0.1986</td><td>0.123</td><td>0.1026</td><td>0.0974</td></tr><tr><td>PLR</td><td>0.9796</td><td>0.068</td><td>0.0006</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td rowspan="3">180 bit</td><td> $SBER_{raw}$ </td><td>0.4927</td><td>0.4874</td><td>0.4581</td><td>0.4173</td><td>0.3926</td><td>0.3839</td><td>0.3806</td><td>0.3795</td><td>0.3791</td></tr><tr><td>SMER</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>PLR</td><td>0.9876</td><td>0.0666</td><td>0.0008</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>No secret</td><td>PLR</td><td>0.9752</td><td>0.064</td><td>0.0002</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></table>

## B. Simulation Results of LoRa Information Hiding

1) Secret Extraction Performance: The simulation results for LoRa information hiding are summarized in Table I, which presents system performance across varying secret lengths and SNR conditions. The secret embedding and extraction performance metrics, $\mathrm { S B E R } _ { r a w }$ and SMER, demonstrate a clear dependence on both SNR and secret length.

At SNR levels below 5 dB, both $\mathrm { S B E R } _ { r a w }$ and SMER remain prohibitively high, rendering reliable secret extraction infeasible. However, performance improves substantially once SNR exceeds 10 dB. For 60-bit and 120-bit secrets, SBER<sub>raw</sub> drops below 0.025 and SMER decreases to less than 0.01, indicating that nearly all embedded secret messages can be accurately recovered. While the 180-bit configuration remains functional, it exhibits higher error rates $( \mathrm { e . g . , } S M E R \approx 0 . 1 4$ at 10 dB). This degradation is expected, as longer secrets place greater demands on the neural network’s capacity. Adopting more advanced network architectures would likely mitigate these limitations and enhance robustness for longer secret lengths.

In summary, the simulation results demonstrate that the proposed LoRa PHY information hiding approach is both effective and practical when SNR exceeds 10 dB, with secret lengths up to 120 bits being reliably embedded and extracted. These findings validate the feasibility of the proposed PHYlayer information hiding technique and highlight the inherent trade-off between secret throughput and extraction reliability.

2) Impact on the Primary LoRa Link: The PLR results in Table I confirm that secret embedding does not degrade the primary communication link. When SNR exceeds 0 dB, the PLR is identical to the no-secret baseline, indicating that the introduced preamble perturbations do not impair packet detection, synchronization, or payload decoding at all. This demonstrates that packet losses are primarily governed by channel noise rather than the proposed PHY-layer information hiding mechanism.

![](images/8313cc81c0939feaa1a512de82f15ecf072e2fb1bb690417d38a123c1c008e68.jpg)  
(a)

![](images/e4b71ff297a1b30741ba43b831d5e04d5681e7169cd24048b97e8ccb334c4771.jpg)  
(b)  
Fig. 7. Distribution of CFO estimation errors across 5,000 simulated LoRa transmissions. Autocorrelation-based CFO estimation algorithm is utilized, and the red dashed line marks zero CFO estimation error. (a) With the standard preamble. (b) With a secret-embedded preamble.

Furthermore, even at low SNR levels below 0 dB, the difference in PLR between the embedded and baseline scenarios remains negligible, demonstrating robust coexistence between the covert channel and the primary LoRa transmission. This preserved link reliability shows the feasibility of leveraging preamble manipulation for secure information hiding without compromising the integrity of the main communication link. These findings are further validated through experiments in Section VIII-B4, where a commercial LoRa chipset successfully received secret-embedded LoRa packets.

3) Impact on LoRa CFO Estimation Errors: In addition to packet detection, the packet preamble serves as a critical component for carrier frequency offset (CFO) estimation. The LoRa PHY employed in this work adopts an autocorrelationbased CFO estimation algorithm. As discussed in Section II-B, since the repetition structure of the preamble is preserved, autocorrelation-based algorithms are inherently unaffected.

To validate this claim, we conducted MATLAB simulations involving 5,000 LoRa transmissions, in which random CFOs were injected into the transmitted LoRa waveforms. The CFO values are uniformly distributed in the range of [-10 ppm, 10 ppm], i.e., ±4.33 kHz for a center frequency of 433 MHz. At the receiver, the CFO was estimated, and the estimation error was computed as the difference between the injected and estimated CFO values. The simulations were performed twice, with PHY information hiding enabled and disabled, respectively.

The resulting CFO estimation errors are illustrated as histograms in Fig. 7. The results show negligible performance differences between the standard preamble and the secretembedded preamble for CFO estimation. In both cases, the CFO estimation error is tightly bounded within [-4 Hz, 4 Hz], demonstrating high estimation accuracy. These results confirm that the proposed PHY information hiding scheme does not degrade the performance of the autocorrelation-based CFO estimation algorithm.

## C. Simulation Results of BLE Information Hiding

1) Secret Extraction Performance: The simulation results for BLE information hiding are presented in Table I. Similar to the LoRa results, $\mathrm { S B E R } _ { r a w }$ and SMER in BLE exhibit strong dependence on both SNR and secret length, with reliable secret extraction achievable only when SNR exceeds 10 dB. Across all tested secret lengths (60, 120, and 180 bits), SMER remains close to 1 below 5 dB, rendering covert communication practically infeasible in low-SNR regimes. Performance improves dramatically with increasing SNR; however, the maximum reliable secret length is considerably lower than in LoRa. For the most robust 60-bit configuration, once SNR reaches 10 dB, $\mathrm { S B E R } _ { r a w }$ drops below 0.038 and SMER falls to 0.012. Above 15 dB, SMER approaches zero, enabling near-perfect message recovery. In contrast, longer secrets (120 bits and 180 bits) exhibit significantly higher error floors and require high SNR for acceptable SMER, indicating that the current BLE embedding scheme reliably supports up to 60 bits under typical SNR conditions.

The performance gap between LoRa and BLE is expected due to their differing temporal resolutions: at our sampling rate, LoRa preambles contain 2,048 I/Q samples, while BLE’s are limited to just 128 I/Q samples. This orders-of-magnitude difference severely restricts the available space for secret embedding in BLE preambles, directly limiting both capacity and robustness. Despite these constraints, the 60-bit performance demonstrates that reliable secret embedding remains feasible when SNR exceeds 10 dB.

2) Impact on the Primary BLE Link: The results in Table I demonstrate that the primary BLE communication link remains unaffected by the secret embedding process. The PLR results for all secret lengths closely match the no-secret baseline across all SNR levels. When SNR exceeds 0 dB, PLR in both baseline and secret-embedded scenarios reduces to zero, demonstrating that preamble perturbations do not interfere with BLE synchronization or payload decoding at all.

![](images/f6c81c56473a55f1d0a51ae149e4db390565e0effa0814c3a76a899a2a75ca25.jpg)  
(a)

![](images/b5bd39d15488402fcb875301ed3c64d1c92f36e9342fd9dbafb6f1b510dcbd49.jpg)  
(b)  
Fig. 8. Distribution of CFO estimation errors across 5,000 simulated BLE transmissions. FFT-based CFO estimation algorithm is utilized, and the red dashed line marks zero CFO estimation error. (a) With the standard preamble. (b) With a secret-embedded preamble.

Even in low-SNR regimes, the PLR difference between the two cases is minimal, confirming that packet losses are dominated by channel noise rather than the PHY information hiding mechanism. These results demonstrate that the proposed PHY-layer embedding technique can coexist with the BLE primary link without compromising link reliability. This is further validated experimentally in Section VIII-C3, where an Android smartphone successfully received secret-embedded BLE packets.

3) Impact on BLE CFO Estimation Errors: We conducted simulations analogous to those in Section VII-B3 to further verify that the proposed PHY information hiding scheme does not compromise CFO estimation performance. Specifically, 5,000 BLE transmissions were simulated, with the true CFO values uniformly distributed over the range [-10 ppm, 10 ppm], corresponding to ±24 kHz at a carrier frequency of 2.4 GHz.

The resulting CFO estimation errors are illustrated in Fig. 8. As observed, the use of the secret-embedded preamble leads to a slight degradation in CFO estimation accuracy. In particular, the estimation error range increases from approximately ±30 Hz to ±50 Hz. This result differs from the LoRa case discussed in Section VII-B3, where PHY information hiding has no observable impact on CFO estimation. The discrepancy arises because the BLE PHY implementation relies on an FFT-based CFO estimation algorithm, rather than an autocorrelation-based approach.

Nevertheless, the secret-embedded preamble remains highly similar to the standard preamble, resulting in only an increase of about 20 Hz in the CFO estimation error. This corresponds to approximately 0.0083 ppm at 2.4 GHz and remains well within the tolerance of practical wireless communication systems.

## VIII. EXPERIMENT EVALUATION

## A. Experiment Configurations

1) Hardware Prototype: To successfully deploy a PHY information hiding system, the transceivers must support the execution of neural networks and provide access to physical layer I/Q samples. Furthermore, the transmitter should be able to send customized radio waveforms. It is worth emphasizing that the proposed technique does not inherently require an SDR-based implementation. Its essential requirement is the ability to manipulate baseband I/Q samples at the transmitter and access baseband I/Q samples at the receiver. SDR technology is adopted in this work mainly as a feasibility-verification prototype, because it decouples software and hardware and provides flexible waveform generation and I/Q sample access for algorithm validation. SDR has been extensively employed in satellite, defense, drone, and 5G cellular applications, making the proposed PHY information hiding readily verifiable on practical hardware platforms.

Two USRP B210 SDR [40] platforms are employed as wireless transmitter and receiver in the experiments. They are connected to two battery-powered laptops via USB ports, which run MATLAB and Python programs to perform LoRa/BLE transmission and PHY information hiding tasks. We emphasize that this prototype is incapable of operating in real time due to the limited computing capabilities of the laptop CPUs. In practical deployments, the secret embedder and extractor can be integrated into the digital baseband processing chain and implemented on FPGA, DSP, dedicated neural accelerators, or eventually baseband chips to achieve real-time performance with substantially lower cost and power consumption.

It is important to note that no external RF amplifier is used in the experiment. For both protocols, we employ standard omnidirectional antennas: a 433 MHz antenna with 4 dBi gain for LoRa and a 2.4 GHz antenna with 2 dBi gain for BLE. Therefore, the measured communication distance is jointly determined by the USRP B210 transmit power and the antenna characteristics, rather than reflecting a fundamental limit of the proposed method. For this reason, we adopt SNR as the primary evaluation metric throughout the paper, since it provides a more hardware-independent measure of system performance.

2) LoRa and BLE PHY Configuration: The LoRa and BLE PHY are identical to the configurations used in simulation, which is introduced in Section VII-A. The SDR transmitter continuously broadcasts LoRa or BLE signals in the experiments. The secret message is randomly generated at the transmitter side and sent as the packet payload. The receiver parses the payload to obtain the ground-truth secret message, which is used to calculate the evaluation metrics.

For LoRa, the secret message length M is fixed at 40 bits unless otherwise specified, resulting in a 120-bit codeword length N. For BLE, the secret message length M is fixed at 20 bits unless otherwise specified, corresponding to a 60-bit codeword embedded in the preamble field. Unless otherwise specified, 500 BLE and LoRa packets are collected at each location. The evaluation metrics and estimated SNR values are provided as the average of all collected packets. The SNR of each packet is estimated by computing the ratio between the average power of the received packet waveform and that of the noise-only I/Q samples preceding the packet.

Unless otherwise specified, each BER and SMER value is averaged over successfully received packets at the corresponding location. In total, we collect 4,000 LoRa packets across 8 locations and 2,000 BLE packets across 4 locations, with each packet carrying a 120-bit and 60-bit codeword, respectively. Although the USB-based USRP B210 prototype may occasionally introduce dropped samples or packet losses, the averaged results over thousands of packets provide representative empirical evidence for the feasibility of the proposed PHY-layer information hiding method under the evaluated prototype conditions.

![](images/3297aa522cf9797c28d50c55df3ed4d0b989f1b6e21e0845b4aefcfaa9e73574.jpg)  
Fig. 9. Experiment environments. (a) Indoor environment. (b) Outdoor environment.

![](images/3cbf334a1c70ab034218ecbd1a1ad99919bfe7ddef6ec7253de4cf4b969b4203.jpg)  
Fig. 10. Floor plan of the office building.

3) Neural Network Configuration: It is worth noting that the neural networks deployed in real-world experiments are trained exclusively on simulation data unless otherwise specified. In other words, the models are identical to those used in Section VII, with the same architectures and weights. Once deployed in practical environments, the neural networks can be fine-tuned using real-world collected data to further enhance performance. The effects of fine-tuning for LoRa and BLE are demonstrated in Sections VIII-B3 and VIII-C2, respectively.

## B. Experiment Results of LoRa Information Hiding

1) Secret Extraction Performance in Indoor Environment: We then carried out an indoor experimental evaluation in an office building. The photos of the experimental environments and the floor plan are given in Fig. 9(a) and Fig. 10, respectively. As depicted in the figures, the SDR transmitter remained stationary while the receiver was sequentially placed at locations A, B, C, and D. Specifically, locations A, B, and C are positioned along a typical corridor, whereas location D is situated inside a standard office room. The environment contains common office furniture, including chairs, desks, bookshelves, and computer monitors. All experiments were performed with the door closed, and the walls are made of concrete.

TABLE II  
EXPERIMENTAL RESULTS OF LORA INFORMATION HIDING IN THE INDOOR ENVIRONMENT. 120 BITS ARE EMBEDDED WITHIN THE PREAMBLE FIELD.

<table><tr><td rowspan="2">Condition</td><td rowspan="2">Loc.</td><td rowspan="2">Avg. SNR</td><td colspan="3">Metrics</td></tr><tr><td> $SBER_{raw}$ </td><td> $SBER_{fec}$ </td><td>SMER</td></tr><tr><td rowspan="3">LOS</td><td>A</td><td>26.39 dB</td><td>0.0242</td><td>0.0002</td><td>0.0039</td></tr><tr><td>B</td><td>13.37 dB</td><td>0.0423</td><td>0.0021</td><td>0.0456</td></tr><tr><td>C</td><td>6.65 dB</td><td>0.1595</td><td>0.0745</td><td>0.747</td></tr><tr><td>NLOS</td><td>D</td><td>15.07 dB</td><td>0.0464</td><td>0.0021</td><td>0.0419</td></tr></table>

TABLE III  
EXPERIMENTAL RESULTS OF LORA INFORMATION HIDING IN THE OUTDOOR ENVIRONMENT. 120 BITS ARE EMBEDDED WITHIN THE PREAMBLE FIELD.

<table><tr><td rowspan="2">Distance</td><td rowspan="2">Avg. SNR</td><td colspan="3">Metrics</td></tr><tr><td> $SBER_{raw}$ </td><td> $SBER_{fec}$ </td><td>SMER</td></tr><tr><td>10 m</td><td>21.17 dB</td><td>0.0363</td><td>0.0012</td><td>0.0219</td></tr><tr><td>20 m</td><td>11.55 dB</td><td>0.0558</td><td>0.0068</td><td>0.0931</td></tr><tr><td>30 m</td><td>8.1 dB</td><td>0.1073</td><td>0.0441</td><td>0.3713</td></tr><tr><td>40 m</td><td>5.25 dB</td><td>0.1698</td><td>0.0951</td><td>0.7386</td></tr></table>

The experimental results are presented in Table II. It can be observed that the SMER is lower than 0.05 when the receiver is placed at locations A, B, and D, indicating a promising PHY information hiding performance. However, the SMER at location C is 0.747, which implies that most covert messages cannot be extracted without errors and may need retransmission. The high SMER can be attributed to the low SNR of 6.65 dB on average. Moreover, it can be seen that the SMER for location D is 0.0419, which indicates that the designed LoRa information hiding system can achieve excellent performance even in non-line-of-sight (NLOS) scenarios.

2) Secret Extraction Performance in Outdoor Environment: As shown in Fig. 9(b), outdoor evaluation was carried out in a roadside open field with vehicles passing by, including cars and bicycles. Vehicles passed by approximately every 20–40 seconds. Each passing vehicle could introduce rapid fluctuations to the wireless channel, including abrupt variations in the SNR.

The SDR transmitter is kept stationary, while the receiver is placed at four distances of 10 m, 20 m, 30 m, and 40 m. The experimental results in Table III demonstrate that the system performance decreases as the distance increases. Specifically, the SMER increases from 0.0219 to 0.7386, and the SBER<sub>raw</sub> rises from 0.0363 to 0.1698 when the transceiver distance increases from 10 m to 40 m. This performance reduction can be attributed to the deterioration in signal quality, as the estimated SNR gradually declines from 21.17 dB to 5.25 dB.

It is important to note that the relatively short outdoor communication range, i.e., up to 40 m, is a consequence of the constrained transmission power of the USRP B210. Therefore, instead of using the absolute communication distance, we adopt SNR as the evaluation metric, as it offers a more general and transferable measure for assessing communication performance across different hardware settings.

3) Effect of Sim-to-Real Fine-Tuning: The neural networks employed in the above subsections are trained entirely using the simulation data. However, their performance inevitably degrades when deployed in practical environments because of the simulation-to-reality gap, which can be concluded by comparing the results in Table I and Table II. The sim-to-real fine-tuning introduced in Section V-D serves as an effective mitigation strategy, which is experimentally validated.

TABLE IV  
EFFECT OF SIM-TO-REAL FINE-TUNING IN LORA INFORMATION HIDING. THE SECRET EXTRACTOR IS FINE-TUNED USING THE SIGNALS COLLECTED AT LOCATION A IN THE INDOOR ENVIRONMENT AND TESTED ON THE OTHERS.

<table><tr><td rowspan="2">Dataset</td><td rowspan="2">Model</td><td colspan="3">Metrics</td></tr><tr><td> $SBER_{raw}$ </td><td> $SBER_{fec}$ </td><td>SMER</td></tr><tr><td rowspan="2">Indoor Location A</td><td>Simulation</td><td>0.0242</td><td>0.0002</td><td>0.0039</td></tr><tr><td>Fine-tuned</td><td>-</td><td>-</td><td>-</td></tr><tr><td rowspan="2">Indoor Location B</td><td>Simulation</td><td>0.0423</td><td>0.0021</td><td>0.0456</td></tr><tr><td>Fine-tuned</td><td>0.037</td><td>0.0009</td><td>0.0198</td></tr><tr><td rowspan="2">Indoor Location C</td><td>Simulation</td><td>0.1595</td><td>0.0745</td><td>0.747</td></tr><tr><td>Fine-tuned</td><td>0.1337</td><td>0.0494</td><td>0.6215</td></tr><tr><td rowspan="2">Indoor Location D</td><td>Simulation</td><td>0.0464</td><td>0.0021</td><td>0.0419</td></tr><tr><td>Fine-tuned</td><td>0.0443</td><td>0.0017</td><td>0.0399</td></tr><tr><td rowspan="2">Outdoor 10 m</td><td>Simulation</td><td>0.0363</td><td>0.0012</td><td>0.0219</td></tr><tr><td>Fine-tuned</td><td>0.0319</td><td>0.0003</td><td>0.0099</td></tr><tr><td rowspan="2">Outdoor 20 m</td><td>Simulation</td><td>0.0558</td><td>0.0068</td><td>0.0931</td></tr><tr><td>Fine-tuned</td><td>0.0519</td><td>0.0044</td><td>0.0634</td></tr><tr><td rowspan="2">Outdoor 30 m</td><td>Simulation</td><td>0.1073</td><td>0.0441</td><td>0.3713</td></tr><tr><td>Fine-tuned</td><td>0.095</td><td>0.0319</td><td>0.3034</td></tr><tr><td rowspan="2">Outdoor 40 m</td><td>Simulation</td><td>0.1698</td><td>0.0951</td><td>0.7386</td></tr><tr><td>Fine-tuned</td><td>0.1403</td><td>0.0642</td><td>0.6376</td></tr></table>

Specifically, the simulation-trained secret extractor is finetuned using the signals collected at location A in the indoor building, which is a short-range LOS setting with an average SNR of 26.39 dB, and tested on the rest of the real-collected datasets. The initial learning rate and batch size are configured as 0.0001 and 32, respectively. The results are illustrated in Table IV. It can be observed that the fine-tuned model achieves improved performance in comparison to the simulation-trained one. For instance, when tested at location B, fine-tuning reduces the $\mathrm { S B E R } _ { f e c }$ and SMER from 0.0021 to 0.0009, and 0.0456 to $0 . 0 1 9 8 ,$ respectively, almost half the original value. The results on outdoor datasets also show significant improvement, with the SMER being reduced by more than 0.1 when the transceivers are placed 40 m apart. In conclusion, the proposed sim-to-real fine-tuning can effectively mitigate the performance degradation caused by the simulation-to-reality gap.

4) Compatibility with Commodity LoRa Chips: The discussion in Section II-B claims that the intentionally introduced physical layer distortion does not affect the normal packet reception and synchronization process. This is experimentally validated through the utilization of a commercial-off-the-shelf LoRa device to receive the signal transmitted from an SDR. As shown in Fig. 11, the transmitter is a USRP B210 SDR running PHY information hiding and LoRa PHY programs, i.e., 60 bits are embedded within the preamble waveform before transmission. Subsequently, a commodity LoRa development board, the EoRa-S3-400TB, which incorporates a Semtech SX1268 chip, is employed for signal reception. It can be observed from the board screen and serial port outputs that the LoRa packets are successfully received. The cyclic redundancy checks are passed, indicating that the payload contents have been decoded without errors.

![](images/fe30b32ca6c180241f217879ef3fa85a0d94278df1cc7a8c40fde7278739851e.jpg)  
Fig. 11. LoRa signal reception using a commodity receiver. The transmitter is an SDR running PHY information hiding and LoRa PHY program. The receiver is a COTS LoRa development board, and the receive status is output via an OLED screen and serial port.

TABLE V  
EXPERIMENTAL RESULTS OF BLE INFORMATION HIDING. 60 BITS ARE EMBEDDED WITHIN THE PREAMBLE FIELD.

<table><tr><td rowspan="2">Distance</td><td rowspan="2">Avg. SNR</td><td colspan="3">Metrics</td></tr><tr><td> $SBER_{raw}$ </td><td> $SBER_{fec}$ </td><td>SMER</td></tr><tr><td>2 m</td><td>22.54 dB</td><td>0.0405</td><td>0.0018</td><td>0.0159</td></tr><tr><td>5 m</td><td>12.87 dB</td><td>0.0627</td><td>0.0072</td><td>0.0659</td></tr><tr><td>7 m</td><td>10.88 dB</td><td>0.0784</td><td>0.0131</td><td>0.1198</td></tr><tr><td>10 m</td><td>5.73 dB</td><td>0.1907</td><td>0.1337</td><td>0.7086</td></tr></table>

The experimental results demonstrate that the proposed PHY information hiding technique does not affect the primary communication link. Furthermore, as most commercial RF chips do not provide access to waveform-level information, i.e., I/Q samples, the eavesdroppers have to be equipped with a dedicated device in order to detect the existence of the covert channel, which increases the cost of eavesdropping.

## C. Experiment Results of BLE Information Hiding

1) Performance of BLE Information Hiding: We then carried out experiments to validate the system design. The experiments are conducted within the same office building illustrated in Section VIII-B1, with the floor plan presented in Fig. 10. The transmitter is fixed, while the receiver is moved along the corridor to 2 m, 5 m, 7 m, and 10 m apart. The experimental results are given in Table V, which demonstrate that a highquality BLE covert link can be established when the SNR is above 10 dB. Specifically, the SMER is as low as 0.0159, 0.0659, and 0.1198, respectively, when the transceivers are placed 2 m, 5 m, and 7 m apart. However, the SMER increases significantly to 0.7086 when the SNR is around 5.73 dB. Note that typical indoor BLE links routinely operate in the 10–20 dB SNR range, which aligns well with the reliable extraction threshold observed above. Although the SNR required for reliable secret extraction may be slightly higher than that for normal BLE packet reception, the proposed PHY information hiding scheme is still feasible in typical scenarios. As noted earlier in Section VIII-B2, the limited communication distance is due to the low transmission power of the USRP B210 board, and an external power amplifier can bring about significant improvement.

TABLE VI  
EFFECT OF SIM-TO-REAL FINE-TUNING IN BLE INFORMATION HIDING. THE SECRET EXTRACTOR IS FINE-TUNED AT A 2 M DISTANCE AND TESTED ON THE OTHERS.

<table><tr><td rowspan="2">Dataset</td><td rowspan="2">Model</td><td colspan="3">Metrics</td></tr><tr><td> $SBER_{raw}$ </td><td> $SBER_{fec}$ </td><td>SMER</td></tr><tr><td rowspan="2">2 m</td><td>Simulation</td><td>0.0405</td><td>0.0018</td><td>0.0159</td></tr><tr><td>Fine-tuned</td><td>-</td><td>-</td><td>-</td></tr><tr><td rowspan="2">5 m</td><td>Simulation</td><td>0.0627</td><td>0.0072</td><td>0.0659</td></tr><tr><td>Fine-tuned</td><td>0.0568</td><td>0.0029</td><td>0.0299</td></tr><tr><td rowspan="2">7 m</td><td>Simulation</td><td>0.0784</td><td>0.0131</td><td>0.1198</td></tr><tr><td>Fine-tuned</td><td>0.0776</td><td>0.0113</td><td>0.1097</td></tr><tr><td rowspan="2">10 m</td><td>Simulation</td><td>0.1907</td><td>0.1337</td><td>0.7086</td></tr><tr><td>Fine-tuned</td><td>0.1763</td><td>0.1052</td><td>0.6407</td></tr></table>

![](images/a34c3c47144d94929012477dfdb8e1cae40e6770a41b70bded6b8b4b27a30a4a.jpg)  
Fig. 12. BLE signal reception using a smartphone. The transmitter is an SDR broadcasting BLE advertisements, i.e., random 60-bit secrets are embedded. The receiver is an Android smartphone. The SDR-BLE transmitter, named ‘BLE Secret Advertiser’, is discoverable by the smartphone.

2) Effect of Sim-to-Real Fine-Tuning: A comparison between Table I and Table V demonstrates that there is an inevitable simulation-to-reality gap for BLE information hiding. Given that the secret embedder and extractor are trained using the simulation data, fine-tuning model weights with real-collected signals can improve the system performance in practical wireless environments. The effect of sim-to-real finetuning is demonstrated in Table VI, where the weights of the secret extractor are fine-tuned using the dataset collected in a short-range LOS setting at a distance of 2 m with an average SNR of 22.54 dB. It can be observed that the SBER<sub>raw</sub>, $\mathrm { S B E R } _ { f e c } ,$ and SMER for other datasets can be significantly reduced after fine-tuning is applied. In the best case, the SMER reduces from 0.0659 to 0.0299 when evaluated on the dataset collected at a 5 m distance.

![](images/6478b62edbdd8b778cacb2462f4737bbc7c9405a3ca24d091c2e97b19410cd76.jpg)  
(a)

![](images/9597537b08d14c019072fc4867508539c2fae57163bc7e205577f77c90874a00.jpg)  
(b)  
Fig. 13. Distribution of estimated CFO values from experimentally collected secret-embedded packets. The red dashed line denotes the mean CFO of the collected packets. (a) LoRa CFO estimation results. (b) BLE CFO estimation results.

3) Compatibility with Smartphones: This subsection provides experimental evidence that the PHY information hiding does not affect the primary communication link, i.e., normal BLE packet reception and decoding. As illustrated in Fig. 12, we use a USRP B210 SDR to broadcast BLE advertisements at channel 37. A random 60-bit secret is embedded within the preamble field of each BLE packet. Concurrently, an Android smartphone is utilized to capture these BLE advertisements. It is evident from the phone screen that the BLE packets are successfully received and decoded. The phone screen displays that the SDR-based BLE advertiser is discoverable in instances where 60-bit secrets have been embedded. This proves the claim that the proposed PHY information hiding scheme does not affect the regular packet reception and decoding process.

In the BLE information hiding system, Alice and Bob can establish a covert link at the PHY layer to transmit secret messages. While others within range can detect the BLE wireless packets using their smartphones, only Bob has the ability to extract the embedded covert secrets. This highlights that the designed PHY information hiding scheme exhibits excellent covertness and stealthiness.

## D. Impact on CFO Estimation Results

The simulation results in Sections VII-B3 and VII-C3 have demonstrated that the proposed PHY information hiding has negligible impact on CFO estimation. To further validate this conclusion with real hardware, we plot the estimated CFO values from the experimentally collected secret-embedded packets as histograms.

The results are presented in Fig. 13, where the red dashed line denotes the mean CFO of the collected packets. For LoRa, the estimated CFO values range from approximately −900 Hz to −400 Hz. For BLE, the estimated CFO values range from approximately 400 Hz to 1000 Hz. These CFO values primarily originate from the frequency mismatch between the transmitter and receiver crystal oscillators, rather than from the secret embedding algorithm.

Moreover, the estimated CFO magnitudes are negligible relative to the CFO tolerance of the respective protocols. As specified in the Semtech application note [41], the LoRa modem can tolerate frequency offsets of up to ±80 ppm for SF5-SF10, which corresponds to ±34.6 kHz at 433 MHz. The

TABLE VII  
COMPLEXITY AND INFERENCE LATENCY OF THE SECRET EMBEDDER AND EXTRACTOR. LATENCY IS REPORTED AS MEAN ± STANDARD DEVIATION OVER 50 TIMED RUNS.

<table><tr><td>Protocol</td><td>Secret Length</td><td>Module</td><td>Parameters</td><td>Latency</td></tr><tr><td rowspan="2">BLE</td><td rowspan="2">60 bit</td><td>Embedder</td><td>3,436,158</td><td> $0.6646 \pm 0.0917$  ms</td></tr><tr><td>Extractor</td><td>3,328,136</td><td> $0.7626 \pm 0.2087$  ms</td></tr><tr><td rowspan="2">LoRa</td><td rowspan="2">120 bit</td><td>Embedder</td><td>3,651,318</td><td> $0.6419 \pm 0.1727$  ms</td></tr><tr><td>Extractor</td><td>3,446,576</td><td> $0.7381 \pm 0.1435$  ms</td></tr></table>

Bluetooth Core Specification [42] requires that the transmitter center frequency deviation shall not exceed ±75 kHz. The observed CFOs of <1 kHz in both cases are far below these limits and thus will not affect normal packet demodulation. These experimental results confirm that CFO estimation remains fully functional on secret-embedded preambles in practical wireless environments.

## E. Model Complexity and Inference Latency

We further evaluate the computational overhead introduced by the neural network-based secret embedder and extractor. The benchmark is conducted using PyTorch on an NVIDIA RTX 4060 GPU. For each model, we report the mean and standard deviation over 50 timed runs. The benchmark uses the same BLE and LoRa configurations as those adopted in the real-world experiments described above.

The results are summarized in Table VII. The BLE embedder and extractor contain 3.44M and 3.33M parameters, respectively, while the LoRa embedder and extractor contain 3.65M and 3.45M parameters, respectively. The moderate parameter increase in the LoRa models is mainly caused by the longer secret length, since N affects the input channel dimension of the embedder and the final linear layer of the extractor. For both PHYs, the average inference latency of each neural network module is below 0.8 ms, showing that the proposed framework introduces limited neural-network inference overhead on GPU platforms.

For future deployment in more resource-constrained settings, the computational overhead can be substantially reduced through well-established techniques. These include model compression via quantization and pruning, FPGA-based hardware acceleration, and on-chip neural processing units (NPUs) within baseband chips.

## IX. RELATED WORK AND DISCUSSION

## A. Related Work

Information Hiding has a long history of concealing secret messages within ordinary media and remains widely employed in modern digital watermarking, fingerprinting, and steganography tasks [19], [2], [25], [20], [26], [27], [28], [22], [23], [36]. Traditionally, information hiding relied on manually-defined rules for embedding and extracting hidden information. For instance, the least significant bit (LSB) algorithm embeds secrets by modifying the LSB of pixel values [43]. Recently, deep learning-driven approaches have revolutionized information hiding by employing neural networks to automatically learn embedding and extraction algorithms, thereby improving hiding capacity and robustness. The endto-end deep learning framework for steganography was first introduced in [19], where a pair of neural networks was used: one for embedding secrets into an image and another for extracting them. This encoder-decoder framework rapidly evolved, incorporating advanced techniques such as generative adversarial networks (GANs) [33], [34], invertible neural networks (INNs) [44], [45], [20], and diffusion models [35], [46]. These deep learning innovations have significantly accelerated the development of information hiding.

Covert Communication is another closely related topic [7]. The theory-oriented covert communication studies do not embed additional secrets within the PHY. Instead, the covertness is achieved by reducing the likelihood of normal transmissions being detected by an adversary. They are roughly divided into two categories. The first category relies on directional transmission as a means to facilitate covert communication. Through the utilization of multiple antennas [8], [9], [47], RIS [11], [10], [48], or mmWave [12], [13], [49] technologies for beamforming, transmitters can concentrate signals specifically toward the intended legitimate receiver. This technique markedly reduces the probability of interception by eavesdroppers located in other directions, thus improving communication security. Nevertheless, these methods become ineffective when eavesdroppers are geographically positioned near the legitimate receiver. Additionally, controlling side-lobe leakage remains challenging, potentially undermining the effectiveness of such approaches. Another category of studies aims to interfere with the eavesdropper. Specifically, by deploying a friendly jammer to emit artificial noise, the transmitter can interfere with adversaries without affecting legitimate receivers [50], [51], [52]. However, these approaches often require prior knowledge of the eavesdropper, e.g., channel state information, which is difficult to acquire in practical scenarios. Moreover, these schemes are applicable solely for covert communication and cannot be utilized for watermarking or fingerprinting, since no additional secrets are embedded within PHY. Furthermore, the proposed PHY information hiding approach can coexist with other physical-layer security techniques, such as key generation [53], [54], [55], [56], to jointly protect wireless systems at the physical layer.

A few system-oriented studies modify existing modulation schemes to create a covert side channel [14], [15], [16], [17], [18]. For example, the authors in [57] propose a pseudo-noise asymmetrical shift keying (PN-ASK) scheme, which integrates amplitude modulation into PSK techniques. However, these customized modulation-based solutions are only compatible with a specific modulation scheme or wireless protocol, thus exhibiting limited generalizability.

## B. Applications of PHY Information Hiding

The proposed PHY information hiding framework embeds an arbitrary binary secret into the emitted radio waveform. This waveform-level embedding can support two representative applications.

RF Fingerprint Embedding. A representative application is RF fingerprint embedding for PHY authentication. Secret information is attached to the preamble waveform as a complementary identifier; it does not replace cryptographic authentication. A static embedded identifier is vulnerable to replay, because an adversary can capture the preamble I/Q samples and retransmit them later. This limitation can be addressed at the protocol level by a freshness mechanism that makes the embedded secret packet-varying, e.g., timestamp, sequence number, or nonce.

Covert Side Channel. Another application is a covert side channel that coexists with the primary communication link. Because the secrets are concealed in the preamble waveform, commodity receivers that only decode the payload remain unaware of the hidden transmission, while the intended receiver recovers the secrets with the paired secret extractor. As a related reference, CloakLoRa carries a 30-bit covert payload in each LoRa packet by modulating chirp amplitudes [14], and the proposed LoRa prototype embeds 120 secret bits in the preamble.

## C. Discussion

The proposed PHY information hiding is fundamentally different from the related studies in Section IX-A. Compared to prior theory-oriented studies, it does not impose constraints on the geographic locations of legitimate receivers or potential eavesdroppers [8], [9], [11], [10], [12], [13]. Furthermore, it does not require prior channel knowledge about the receiver or eavesdropper [50], [51], [52], thereby enhancing its feasibility and ease of deployment in real-world wireless communication systems. In contrast to existing system-oriented methods that customize specific modulation schemes or wireless protocols [14], [15], [16], [17], [18], we employ a pair of neural networks to learn secret embedding directly within preamble waveforms. This design methodology is protocolagnostic. Specifically, regardless of the underlying wireless protocol, whether LoRa, Bluetooth, ZigBee, or others, the deep learning framework can automatically learn an effective PHY information hiding strategy directly from simulation data.

However, a limitation of the proposed PHY information hiding scheme is that its performance degrades significantly when the SNR falls below 10 dB, as validated in both simulations and experiments in Sections VII and VIII. This behavior is expected, since the secrets are embedded as subtle distortions within the PHY waveform, which become obscured by noise in low-SNR scenarios.

## X. CONCLUSION

This paper proposes a practical and protocol-agnostic PHY information hiding methodology, which is fundamentally different from prior studies. The design methodology is inspired by the deep learning-based encoder-decoder framework that is widely adopted in other fields, e.g., image information hiding. Specifically, Alice utilizes a neural network to embed secrets within the packet preamble waveforms by introducing subtle and imperceptible distortions. Subsequently, Bob uses another paired neural network extractor to parse the secrets from the packet preamble. We propose a simulation-driven joint training scheme and a sim-to-real fine-tuning technique to enhance the performance when deployed on real hardware transceivers. We provide SDR hardware prototypes based on LoRa and BLE protocols, demonstrating the excellent generalizability of this scheme. The results validate that the proposed PHY information hiding methodology can establish an undetectable covert channel without affecting the quality of the primary communication links. For future work, we plan to extend the framework to wideband systems such as Wi-Fi and 5G. This extension is more challenging than the LoRa and BLE settings studied in this paper, because wideband transmissions are more sensitive to frequency-selective fading and multipathinduced distortions. At the same time, Wi-Fi and 5G receivers typically include standard channel estimation and equalization modules. A promising direction is therefore to incorporate these modules to improve the secret decoding performance.

## REFERENCES

[1] F. A. Petitcolas, R. J. Anderson, and M. G. Kuhn, “Information hiding-a survey,” Proc. IEEE, vol. 87, no. 7, pp. 1062–1078, 2002.

[2] X. Luo, R. Zhan, H. Chang, F. Yang, and P. Milanfar, “Distortion agnostic deep watermarking,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), 2020, pp. 13 548–13 557.

[3] L. Y. Paul, G. Verma, and B. M. Sadler, “Wireless physical layer authentication via fingerprint embedding,” IEEE Commun. Mag., vol. 53, no. 6, pp. 48–53, 2015.

[4] K. Ito, T. Kozu, H. Kawai, G. Hanawa, and T. Aoki, “Cancelable face recognition using deep steganography,” IEEE Transactions on Biometrics, Behavior, and Identity Science, vol. 6, no. 1, pp. 87–102, 2023.

[5] S. Katzenbeisser and F. Petitcolas, Information hiding. Artech House, 2016.

[6] J. Classen, M. Schulz, and M. Hollick, “Practical covert channels for WiFi systems,” in Proc. IEEE Conf. Commun. Net. Secur. (CNS), 2015, pp. 209–217.

[7] X. Chen, J. An, Z. Xiong, C. Xing, N. Zhao, F. R. Yu, and A. Nallanathan, “Covert communications: A comprehensive survey,” IEEE Commun. Surveys Tuts., 2023.

[8] O. Shmuel, A. Cohen, and O. Gurewitz, “Multi-antenna jamming in covert communication,” IEEE Trans. Commun., vol. 69, no. 7, pp. 4644– 4658, 2021.

[9] H. Du, D. Niyato, Y.-A. Xie, Y. Cheng, J. Kang, and D. I. Kim, “Performance analysis and optimization for jammer-aided multiantenna UAV covert communication,” IEEE J. Sel. Areas Commun., vol. 40, no. 10, pp. 2962–2979, 2022.

[10] C. Wang, Z. Li, J. Shi, and D. W. K. Ng, “Intelligent reflecting surfaceassisted multi-antenna covert communications: Joint active and passive beamforming optimization,” IEEE Trans. Commun., vol. 69, no. 6, pp. 3984–4000, 2021.

[11] X. Lu, E. Hossain, T. Shafique, S. Feng, H. Jiang, and D. Niyato, “Intelligent reflecting surface enabled covert communications in wireless networks,” IEEE Network, vol. 34, no. 5, pp. 148–155, 2020.

[12] J. Zhang, M. Li, S. Yan, C. Liu, X. Chen, M.-J. Zhao, and P. Whiting, “Joint beam training and data transmission design for covert millimeterwave communication,” IEEE Trans. Inf. Forensics Security, vol. 16, pp. 2232–2245, 2021.

[13] C. Wang, Z. Li, and D. W. K. Ng, “Covert rate optimization of millimeter wave full-duplex communications,” IEEE Trans. Wireless Commun., vol. 21, no. 5, pp. 2844–2861, 2021.

[14] N. Hou, X. Xia, and Y. Zheng, “CloakLoRa: A covert channel over LoRa PHY,” IEEE/ACM Trans. Netw., vol. 31, no. 3, pp. 1159–1172, 2022.

[15] B. Liu, C. Gu, S. He, and J. Chen, “LoPhy: A resilient and fast covert channel over LoRa PHY,” in Proc. Int. Conf. Inf. Process. Sensor Netw. (IPSN), 2023, pp. 1–13.

[16] M. Schulz, J. Link, F. Gringoli, and M. Hollick, “Shadow Wi-Fi: Teaching smartphones to transmit raw signals and to extract channel state information to implement practical covert channels over Wi-Fi,” in Proc. Int. Conf. Mobile Syst. Appl. Services (MobiSys), 2018, pp. 256–268.

[17] H. Huang and L. Zhang, “Reliable and secure constellation shifting aided differential radio frequency watermark design for NB-IoT systems,” IEEE Commun. Lett., vol. 23, no. 12, pp. 2262–2265, 2019.

[18] L. Bonati, S. D’Oro, F. Restuccia, S. Basagni, and T. Melodia, “SteaLTE: Private 5G cellular connectivity as a service with full-stack wireless steganography,” in Proc. IEEE Int. Conf. Comput. Commun. (INFO-COM), 2021, pp. 1–10.

[19] J. Zhu, R. Kaplan, J. Johnson, and F.-F. Li, “Hidden: Hiding data with deep networks,” in Proc. European Conf. Comput. Vis. (ECCV), 2018, pp. 657–672.

[20] S.-P. Lu, R. Wang, T. Zhong, and P. L. Rosin, “Large-capacity image steganography based on invertible neural networks,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), 2021, pp. 10 816–10 825.

[21] S. Abdelnabi and M. Fritz, “Adversarial watermarking transformer: Towards tracing text provenance with data hiding,” in IEEE Secur. Privacy (S&P). IEEE, 2021, pp. 121–140.

[22] Z.-L. Yang, X.-Q. Guo, Z.-M. Chen, Y.-F. Huang, and Y.-J. Zhang, “RNN-stega: Linguistic steganography based on recurrent neural networks,” IEEE Trans. Inf. Forensics Security, vol. 14, no. 5, pp. 1280– 1295, 2018.

[23] G. Kaptchuk, T. M. Jois, M. Green, and A. D. Rubin, “Meteor: Cryptographically secure steganography for realistic distributions,” in Proc. Conf. Compu. Commun. Secur. (CCS), 2021, pp. 1529–1548.

[24] Z. Wang, O. Byrnes, H. Wang, R. Sun, C. Ma, H. Chen, Q. Wu, and M. Xue, “Data hiding with deep learning: A survey unifying digital watermarking and steganography,” IEEE Trans. Comput. Social Syst., vol. 10, no. 6, pp. 2985–2999, 2023.

[25] M. Tancik, B. Mildenhall, and R. Ng, “StegaStamp: Invisible hyperlinks in physical photographs,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), 2020, pp. 2117–2126.

[26] B. Bai, R. Lee, Y. Li, T. Gan, Y. Wang, M. Jarrahi, and A. Ozcan, “Information-hiding cameras: Optical concealment of object information into ordinary images,” Science Advances, vol. 10, no. 24, 2024.

[27] W. Tang, B. Li, S. Tan, M. Barni, and J. Huang, “CNN-based adversarial embedding for image steganography,” IEEE Trans. Inf. Forensics Security, vol. 14, no. 8, pp. 2074–2087, 2019.

[28] C. Zhang, P. Benz, A. Karjauv, G. Sun, and I. S. Kweon, “UDH: Universal deep hiding for steganography, watermarking, and light field messaging,” Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), vol. 33, pp. 10 223–10 234, 2020.

[29] J. Wu, B. Chen, W. Luo, and Y. Fang, “Audio steganography based on iterative adversarial attacks against convolutional neural networks,” IEEE Trans. Inf. Forensics Security, vol. 15, pp. 2282–2294, 2020.

[30] S. Baluja, “Hiding images in plain sight: Deep steganography,” Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), vol. 30, 2017.

[31] ——, “Hiding images within images,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 42, no. 7, pp. 1685–1697, 2019.

[32] W. Pan, Y. Yin, X. Wang, Y. Jing, and M. Song, “Seek-and-hide: adversarial steganography via deep reinforcement learning,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 44, no. 11, pp. 7871–7884, 2021.

[33] K. A. Zhang, A. Cuesta-Infante, and K. Veeramachaneni, “SteganoGAN: High capacity image steganography with GANs,” arXiv preprint, 2019. [Online]. Available: https://arxiv.org/abs/1901.03892

[34] J. Yang, D. Ruan, J. Huang, X. Kang, and Y.-Q. Shi, “An embedding cost learning framework using GAN,” IEEE Trans. Inf. Forensics Security, vol. 15, pp. 839–851, 2019.

[35] J. Yu, X. Zhang, Y. Xu, and J. Zhang, “Cross: Diffusion model makes controllable, robust and secure image steganography,” Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), vol. 36, 2024.

[36] T. M. Jois, G. Beck, and G. Kaptchuk, “Pulsar: Secure steganography for diffusion models,” in Proc. Conf. Compu. Commun. Secur. (CCS), 2024, pp. 4703–4717.

[37] T. Zhao, J. Zhang, S. Mao, and X. Wang, “Explanation-guided backdoor attacks against model-agnostic RF fingerprinting systems,” IEEE Trans. Mobile Comput., 2024.

[38] T. Orekondy, B. Schiele, and M. Fritz, “Knockoff nets: Stealing functionality of black-box models,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), 2019, pp. 4954–4963.

[39] Z. Xu, S. Tong, P. Xie, and J. Wang, “From demodulation to decoding: Toward complete LoRa PHY understanding and implementation,” ACM Trans. Sensor Netw., vol. 18, no. 4, pp. 1–27, 2023.

[40] Ettus Research. USRP B210. Accessed on July 7, 2024. [Online]. Available: https://www.ettus.com/all-products/ub210-kit/

[41] Semtech Corporation, “LoRa modem doppler immunity,” Semtech Corporation, Tech. Rep. AN1200.80, October 2023. [Online]. Available: https://www.semtech.com/products/wireless-rf/lora-connect/sx1280

[42] Bluetooth SIG, Bluetooth Core Specification, Bluetooth Special Interest Group Std., 2023. [Online]. Available: https://www.bluetooth.com/ specifications/specs/core-specification-5-4/

[43] J. Fridrich, M. Goljan, and R. Du, “Detecting LSB steganography in color, and gray-scale images,” IEEE Multimedia, vol. 8, no. 4, pp. 22– 28, 2001.

[44] J. Jing, X. Deng, M. Xu, J. Wang, and Z. Guan, “Hinet: Deep image hiding by invertible network,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), 2021, pp. 4733–4742.

[45] Y. Xu, C. Mou, Y. Hu, J. Xie, and J. Zhang, “Robust invertible image steganography,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), 2022, pp. 7875–7884.

[46] Y. Yang, Z. Liu, J. Jia, Z. Gao, Y. Li, W. Sun, X. Liu, and G. Zhai, “Diffstega: Towards universal training-free coverless image steganography with diffusion models,” in Proc. Int. Jt. Conf. Artif. Intell. (IJCAI), 2024.

[47] T.-X. Zheng, H.-M. Wang, D. W. K. Ng, and J. Yuan, “Multi-antenna covert communications in random wireless networks,” IEEE Trans. Wireless Commun., vol. 18, no. 3, pp. 1974–1987, 2019.

[48] X. Zhou, S. Yan, Q. Wu, F. Shu, and D. W. K. Ng, “Intelligent reflecting surface (IRS)-aided covert wireless communications with delay constraint,” IEEE Trans. Wireless Commun., vol. 21, no. 1, pp. 532–547, 2021.

[49] H. Xiao, X. Hu, A. Li, W. Wang, Z. Su, K.-K. Wong, and K. Yang, “STAR-RIS enhanced joint physical layer security and covert communications for multi-antenna mmwave systems,” IEEE Trans. Wireless Commun., vol. 23, no. 8, pp. 8805–8819, 2024.

[50] T.-X. Zheng, Z. Yang, C. Wang, Z. Li, J. Yuan, and X. Guan, “Wireless covert communications aided by distributed cooperative jamming over slow fading channels,” IEEE Trans. Wireless Commun., vol. 20, no. 11, pp. 7026–7039, 2021.

[51] Q. Zhang, M. Bakshi, and S. Jaggi, “Covert communication over adversarially jammed channels,” IEEE Trans. Inf. Theory, vol. 67, no. 9, pp. 6096–6121, 2021.

[52] K.-W. Huang, H. Deng, and H.-M. Wang, “Jamming aided covert communication with multiple receivers,” IEEE Trans. Wireless Commun., vol. 20, no. 7, pp. 4480–4494, 2021.

[53] X. Huan, K. Miao, J. Liu, C. Wu, W. Chen, R. Pei, and H. Hu, “KGPT: Wireless key generation based on power tuning for static Internet-of-Things,” IEEE Trans. Ind. Informat., vol. 21, no. 3, pp. 2610–2621, 2025.

[54] J. Zhang, T. Q. Duong, A. Marshall, and R. Woods, “Key generation from wireless channels: A review,” IEEE Access, vol. 4, pp. 614–626, 2016.

[55] J. Zhang, A. Marshall, and L. Hanzo, “Channel-envelope differencing eliminates secret key correlation: LoRa-based key generation in low power wide area networks,” IEEE Trans. Veh. Technol., vol. 67, no. 12, pp. 12 462–12 466, 2018.

[56] X. Huan, K. Miao, W. Chen, P. Jia, and H. Hu, “Kerra: An Internet of Things wireless key generation resistant to replay attacks,” IEEE Internet Things J., vol. 11, no. 17, pp. 29 035–29 048, 2024.

[57] S. D’Oro, F. Restuccia, and T. Melodia, “Hiding data in plain sight: Undetectable wireless communications through pseudo-noise asymmetric shift keying,” in Proc. IEEE Int. Conf. Comput. Commun. (INFOCOM), 2019, pp. 1585–1593.
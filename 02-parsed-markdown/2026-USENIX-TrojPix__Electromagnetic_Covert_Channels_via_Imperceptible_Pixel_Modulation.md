0

USENIX

THE ADVANCED COMPUTING SYSTEMS ASSOCIATION

# TrojPix: Electromagnetic Covert Channels via Imperceptible Pixel Modulation

Guoming Zhang, Shandong University and Quan Cheng Laboratory; Huiting Zhang, Zhenwei Lu, Heqiang Fu, Xin Gao, Riccardo Spolaor, and Yetong Cao, Shandong University; Yanni Yang and Pengfei Hu, Shandong University and Quan Cheng Laboratory

https://www.usenix.org/conference/usenixsecurity26/presentation/zhang-guoming

# This paper is included in the Proceedings of the 35th USENIX Security Symposium.

August 12–14, 2026 • Baltimore, MD, USA

ISBN 978-1-939133-58-8

Open access to the Proceedings of the 35th USENIX Security Symposium is sponsored by

AgleU

King Abdullah University of

Science and Technology

# TrojPix: Electromagnetic Covert Channels via Imperceptible Pixel Modulation

Guoming Zhang<sup>1,2</sup>, Huiting Zhang<sup>1</sup>, Zhenwei Lu<sup>1</sup>, Heqiang Fu<sup>1</sup>, Xin Gao<sup>1</sup>, Riccardo Spolaor<sup>1</sup>, Yetong Cao<sup>1</sup>, Yanni Yang<sup>1,2</sup>, and Pengfei Hu<sup>1,2\*</sup> <sup>1</sup>Shandong University <sup>2</sup>Quan Cheng Laboratory

## Abstract

Air-gapped networks rely on physical isolation to prevent ex ternal connectivity. Prior electromagnetic (EM) covert channels have exploited emissions from video cables, memory buses, and CPUs, yet they rarely achieve high throughput, long range, and visual imperceptibility simultaneously, limiting practical utility in air-gapped settings. We show that impercep tible pixel modulation can deterministically induce control lable EM emissions on digital video cables, enabling control without system privileges or hardware modifications. Build ing on this insight, we present TrojPix, a covert channel that maintains on-screen imperceptibility while delivering high speed, long-range communication over digital video cables. We realize a lightweight communication scheme that combines pixel-to-sample mapping with adaptive decoding, en abling sample-rate-level robust communication over extended ranges. We evaluate TrojPix across nine commercial-off-theshelf (COTS) monitor manufacturers and fifteen COTS digi tal video cables under realistic conditions, demonstrating its effectiveness in two attack modes: fake screen-off and fore ground embedding. TrojPix achieves a peak throughput of 8.1 Mbps and a maximum range of 208 m, revealing a practical and stealthy threat to the security of air-gapped networks.

## 1 Introduction

Air-gapped networks have long been considered a fundamental security problem in the defense of critical infrastructures [1–5]. By enforcing a physically isolated environment detached from external networks, they prohibit all forms of wireless communication (e.g., Wi-Fi, Bluetooth) and restrict the use of removable storage media, thereby minimizing po tential data leakage vectors. Due to this strict level of isolation, air-gapped systems are widely deployed in military command centers [6], government agencies [7], financial institutions [8], and nuclear power control system [9] where strict confidentiality is paramount. However, air-gaps do not provide absolute security, as adversaries can still leverage covert channels to exfiltrate information across the isolation boundary.

![](images/baa12dfd8d2e8e9a29036d4fe71e7a652ac5bc2522fb331c633d626d52cbe3e5.jpg)  
Figure 1: TrojPix exposes the risk of a novel covert communication attack against air-gapped networks, where malware introduces imperceptible pixel-level modifications that leave the on-screen content visually indistinguishable from normal display, yet induce controllable EM emissions from digital video cables. These emissions can be remotely captured by an adversary at distances of up to 208 meters.

Prior research has demonstrated that side-channel leakages generated during device operation can be manipulated to enable covert communication, include thermal [10], acoustic [11], ultrasonic [12], optical [13], electric power [14], magnetic [15–17], and EM [18–24]. However, most existing studies struggle to achieve balanced performance in multiple key dimensions. As shown in Tab. 1, the approaches in [10–17] fail to penetrate walls, which limits their applicability in realistic environments; the methods in [18–24] generally cannot achieve both high transmission rates and long communication distances simultaneously. The work in [21] achieved the high est data rate (up to 300 kbps), but the transmission distance was limited to only 3 meters, reducing its practical value. In contrast, the work in [24] demonstrated the longest communication distance (87.5 meters), but the rate was only 21.6 kbps. In addition, most schemes neglect visual imperceptibility. For example, in [24], the communication process can be easily detected visually, leading to poor stealth. Overall, existing techniques fail to simultaneously deliver high throughput and long-range communication and lack effective integration of visual stealth, which severely limits their deployment and applicability in air-gapped environments.

Table 1: Comparison of physical covert channels.

<table><tr><td>Method</td><td>Type</td><td>Leakage Source</td><td>Rate (bps)</td><td>Distance (m)</td><td>Wall Pen.</td></tr><tr><td>BitWhisper [10]</td><td>Thermal</td><td>CPU</td><td>0.002</td><td>0.4</td><td> $\times$ </td></tr><tr><td>DiskFiltration [11]</td><td>Acoustic</td><td>HDD</td><td>3</td><td>20</td><td> $\times$ </td></tr><tr><td>AcousticMesh [12]</td><td>Ultrasonic</td><td>Speaker</td><td>20</td><td>19.7</td><td> $\times$ </td></tr><tr><td>CTRL-ALT-LED [13]</td><td>Optical</td><td>LED</td><td>3.33k</td><td>9</td><td> $\times$ </td></tr><tr><td>PowerHammer [14]</td><td>Power</td><td>Power line</td><td>1k</td><td>2</td><td> $-$ </td></tr><tr><td>ODINI [15]</td><td>Magnetic</td><td>CPU</td><td>40</td><td>1</td><td> $-$ </td></tr><tr><td>Matyunin [16]</td><td>Magnetic</td><td>HDD</td><td>2</td><td>0.12</td><td> $-$ </td></tr><tr><td>MagView [17]</td><td>Magnetic</td><td>CPU</td><td>8.9</td><td>0.06</td><td> $-$ </td></tr><tr><td>AirHopper [18]</td><td>EM</td><td>Video cable</td><td>480</td><td>7</td><td> $\checkmark$ </td></tr><tr><td>USBee [19]</td><td>EM</td><td>USB bus</td><td>640</td><td> $-$ </td><td> $\checkmark$ </td></tr><tr><td>GSMem [20]</td><td>EM</td><td>RAM Bus</td><td>1k</td><td>1.5</td><td> $\checkmark$ </td></tr><tr><td>BitJabber [21]</td><td>EM</td><td>DRAM</td><td>300k</td><td>3</td><td> $\checkmark$ </td></tr><tr><td>NoiseSDR [22]</td><td>EM</td><td>DRAM</td><td>2.56k</td><td>5</td><td> $\checkmark$ </td></tr><tr><td>STATn [23]</td><td>EM</td><td>GPIO</td><td>250</td><td>2.25</td><td> $\checkmark$ </td></tr><tr><td>TEMPEST-Lora [24]</td><td>EM</td><td>Video cable</td><td>21.6k</td><td>87.5</td><td> $\checkmark$ </td></tr><tr><td>TrojPix (Ours)</td><td>EM</td><td>Video cable</td><td>8.1M</td><td>208</td><td> $\checkmark$ </td></tr></table>

In this paper, we present TrojPix, the first system that achieves visually imperceptible covert communication by exploiting EM emissions from digital video cables. By applying subtle pixel modulations that remain invisible to the human eye yet induce controllable EM emission, TrojPix turns commodity video cables into unintended antennas, enabling through-wall communication with a peak rate of 8.1 Mbps and a maximum transmission range of 208 m. To achieve TrojPix, we need to address three major challenges.

1) How can imperceptible pixel modifications yield controllable EM emissions? A central challenge for video-based covert communication is achieving reliable receiver-side detectability while remaining imperceptible to the human eye. By analyzing the video transmission process, we demonstrate that modification to pixel values alters the Transition-Minimized Differential Signaling (TMDS) symbolization, inducing controllable EM emissions along video cables. By characterizing the coupling between pixel values and emission intensity, we enable software-defined control that effectively balances visual imperceptibility with demodulation robust ness, establishing the foundation for software-defined EM covert communication over standard digital video cables.

2) How to achieve high-speed communication? Achieving sampling-rate-level throughput requires efficient recovery of digital information from EM emissions. We therefore propose Pixel-to-Sample Mapping (P2S-Map), which establishes a precise correspondence between two-dimensional pixel blocks and one-dimensional sampling instants. Pixels of video frames are partitioned into content-adaptive blocks at the transmitter side, and each block is modulated with subtle modifications, producing distinct intensity features in the time domain. This approach enables data transmission rates approaching the receiver’s sampling rate, with synchronization supported by matched-filter correlation(MFC) and preamble detection, followed by peak detection and clock alignment to ensure robust decoding, even in the presence of timing jitter.

3) How to extend the attack range while maintaining communication quality? Increasing distance leads to severe path loss and multipath fading, which significantly reduces the signal-to-noise ratio (SNR). To address this challenge, we integrate robust front-end gain, precise synchronization, and distortion-tolerant decoding. Low-noise amplification (LNA) and band-pass filtering boost in-band energy at the receiver side, while multi-band sampling and fusion further improve performance. Robustness is reinforced through cross-row resilience coding (CRRC) to mitigate burst errors, and apply an adaptive decision threshold (ADT) aligned with channel conditions to stabilize information recovery under SNR fluctuations. Collectively, these mechanisms strengthen channel robustness and counteract range-induced degradation, enabling reliable communication over significantly longer distances.

In summary, our contributions are as follows:

• We present TrojPix, the first visually imperceptible, highspeed covert channel attack that exploits controllable EM emissions through pixel modulation.

• We formulate controllable EM emissions as constrained modulation problem and introduce P2S-Map, which en ables sample-rate-level transmission and incorporates synchronization with adaptive decoding, thereby achieving robust long-range covert communication.

• We systematically evaluate TrojPix across nine COTS monitor manufacturers and fifteen COTS digital video cables, demonstrating its practicality in real-world settings. Experimental results show that TrojPix achieves a peak rate of up to 8.1 Mbps, and a maximum transmission range of 208 m.

The paper is organized as follows. Section 2 introduces background information. Section 3 conducts feasibility analysis. Section 4 explains the threat model. Section 5 presents the design plan for TrojPix. Section 6 evaluates TrojPix. Section 7 discusses the defense measures and future work. Section 8 introduces the relevant work, and concludes in Section 9.

## 2 Background

## 2.1 Fully-Digital Radios

Conventional Software-Defined Radio (SDR) has made wireless communication more flexible [25]: protocols and waveforms can be determined by software rather than relying on fixed-function hardware. As shown in the upper part of Fig. 2, the baseband signal is first converted into an analog waveform by a Digital-to-Analog Converter (DAC), then passed through a mixer, filter, and amplifier, before being transmitted through an antenna to the receiver. However, SDR still requires analog components in the signal transmission process. These compo nents not only increase system complexity, but also make it difficult to achieve high integration and cross-platform reuse.

![](images/a5fc1a7c86072bc95ed6fbe988b08ed85d8634a6ca5c23de94d34c75b682c6a6.jpg)  
Figure 2: Principle of different radio architectures.

To address this issue, Fully Digital Radio (FDR) has emerged [26]. Its core principle is to perform signal genera tion primarily in the digital domain, avoiding additional analog modules. Specifically, as shown in the lower part of Fig. 2, it approximates the desired continuous waveform through a sequence of high-speed binary signal switches and achieves modulation of amplitude, frequency, and phase by controlling duty cycle, period, and edge timing. After simple filtering, these binary sequences can produce the desired RF signals in the target frequency band. This approach brings an important insight: any interface capable of producing high-speed binary signals can essentially serve as a programmable RF source.

## 2.2 Software-Defined EM Emissions

The insights of FDR extend beyond the communication devices themselves. In fact, the vast majority of high-speed digital interfaces in modern electronic systems—whether buses, memory, or peripheral connections—generate EM leakage during operation. These leaks were previously regarded as unintended side effects, but according to Maxwell’s equations, time-varying currents inevitably accompany EM emission. Therefore, these leakage signals inherently possess the same “emission” properties. Based on this, researchers have proposed the concept of Software-Defined Electromagnetic Emission (SDEE) [27]. Unlike FDR, which relies on dedicated binary switching circuits to generate radio signals, SDEE treats the unintended EM leakage generated by any device during operation as a programmable communication channel. Within this framework, software not only determines the device’s surface-level behavior (e.g., computation or display) but also indirectly shapes its detectable EM characteristics. By care fully modulating digital sequences, the resulting leakage can be leveraged to realize covert transmission.

![](images/474ae9471159baf206fe5538d5d7bc53ceb219aabb906166cbe7c31cbaccff93.jpg)  
Figure 3: TMDS channel structure.

## 2.3 EM Leakage of Digital Video Cable

In this context, the EM leakage of video transmission cables becomes a typical example of SDEE. Taking HDMI as an example, its principle is to transmit uncompressed digital video over a single physical link via high-speed serial transmission. The core mechanism is based on TMDS [28], as shown in Fig. 3, where three independent differential pairs continuously carry pixel data at extremely high rates. At the transmitter, the color information for each pixel is encoded in TMDS to optimize the DC balance and reduce EM interference, and then sent as differential signals. On the receiver side, clock recovery, serial-to-parallel conversion, and TMDS decoding are performed to reconstruct the original pixel data stream.

However, according to EM field theory, any high-speed switching current inevitably induces EM radiation along the transmission line. During such high-speed transmission, the digital video cable can unintentionally act as an antenna, radiating part of the information into the surrounding space, thereby offering attackers a potential channel for unauthorized access. From the perspective of SDEE, this implies that a digital video cable is not only a transmission medium but also a programmable EM emitter, whose radiation patterns are directly shaped by pixel arrangements and brightness variations. In other words, while the video stream renders images on the screen, it simultaneously “modulates” the external EM space. This property opens up new possibilities for attackers: by deliberately crafting the video content, they can re-purpose these leakage signals as a covert communication channel—without degrading the user’s viewing experience—to achieve crossdevice information transmission.

## 3 Feasibility Analysis

Imperceptible Display Modifications. To explore whether modifications to the displayed content can influence the unintentional EM emissions of digital video cable, and whether such emissions can be distinguished under slight, visually imperceptible changes to the content, we conduct a preliminary experiment. In the experiment, a near-field magnetic probe is used to capture EM radiation signals generated during screen data transmission. Comparative tests are carried out by adjusting the brightness of pixels in specific screen regions. The display operates at a 60 Hz refresh rate with a resolution of

![](images/2c77607fde36d1fdf335b7269dadeca28e6372c94c95940f05438c4c2cab3d58.jpg)  
Figure 4: Illustration of EM signal variations induced by pixel modifications.

1920×1080, and TMDS encoding is employed to convert each 8-bit pixel component into 10-bit symbols for transmission.

As shown in Fig. 4, we only modify the least significant bit of the blue channel within the boxed rectangular region of the screen. This change has almost no perceptible impact on the visual output. However, signals captured by the oscilloscope still reveal differences in EM emissions across both identi cal and different rows, thereby confirming that such visually imperceptible pixel modifications are detectable at the EM signal level.

Bit Transmission. To further evaluate the feasibility of achieving bit-level covert transmission by manipulating EM emmisions from digital video cables, we analyze both the spectral and temporal characteristics of the leaked signals. In our experiments, the display renders an image with a resolu tion of 1920×1080, and only the least significant bit of the blue channel in the pixel values of partial data blocks is modi fied. As shown in Fig. 5(a), the corresponding EM spectrum exhibits spectral peak at the fundamental (148.5 MHz) and its second harmonic (297 MHz).

We extract the time-domain waveforms corresponding to the two bands, as shown in Fig.5(b) and Fig.5(c), the alternating binary sequence “10101010” is clearly visible in both bands. This observation indicates that during the display row scanning, subtle variations induce distinct differences in EM emission intensity, enabling discrimination between binary “0” and “1.” Notably, this signature is evident not only at the fundamental frequency but also at its harmonic bands.

The above results confirm that by correlating pixel patterns with the EM emissions generated by digital video cables, it is possible to achieve stable covert communication without introducing any perceptible visual changes. In Section 5, we will elaborate on the principles and implementation mecha nisms of covert communication based on pixel modulation.

## 4 Threat Model

This paper investigates the covert communication scenario shown in Fig. 1. The attacker’s goal is to steal sensitive data from an air-gapped network. Specifically, we assume the fol lowing scenario and attacker capability:

![](images/d529039287829ed1bbf2dc41b0160f9ee32417dd1e543ab3cc7ff4bd48a256c1.jpg)  
Figure 5: Demonstration of covert information transmission on different frequency bands.

Emission Source. The victim’s computer operates in a high-security environment with all communication interfaces disabled. Its display remains on and is connected to at least one digital video cable.

Attacker Capability. We assume that the attacker implants malware carrying TrojPix onto the victim’s computer. This malware operates solely in user mode, requiring neither system privileges, administrator rights, nor direct access to peripherals. The software scans the computer in the background to locate confidential files. It can obtain the resolution of the victim’s monitor, then generate a visually camouflaged attack video and play it secretly to construct a covert channel. Meanwhile, the attacker uses a set of commercial radio devices to receive EM signals from a distance or outside the room and reconstruct the information at the computer terminal.

Scenario 1: Fake Screen-Off Mode. The malware can force the display into a disguised “screen-off” state, presenting a black screen or a visually similar interface to an actual shutdown, nearly indistinguishable from a genuine standby state. From the user’s perspective, the monitor appears to be turned off, but in reality, the digital video cable continues to conduct covert data transmission. Once user interaction (e.g., mouse movement) is detected, the screen instantly resumes, and the transmission is immediately halted, thereby minimizing the likelihood of user detection.

Scenario 2: Foreground Embedding Mode. The malware embeds covert information in real time into the current display content while running in the background, and this method is applicable to any image. It achieves modulation through subtle pixel-level modifications or color adjustments that are visually indistinguishable, ensuring that the user perceives no anomalies during normal usage. Once user interaction is detected, the transmission is immediately terminated to guarantee that the screen display fully matches the user’s perception, further reducing the risk of exposure.

![](images/031fed622b6f23d5decb6d23c0eee4b41e0d4a037915759e29ab20607cdb927c.jpg)  
Figure 6: The overview of TrojPix.

## 5 Design

In this section, we present the system architecture of TrojPix. Fig. 6 provides an overview of our system and its modules. In what follows, we introduce the three modules that comprise transmitter design, frame structure and coding, and receiver design in convert communication.

## 5.1 Transmitter Design

## 5.1.1 TMDS Bitstream and Spectral Characteristics

In a TMDS-based digital cable transmission, each pixel is mapped to three color channels, and each channel carries a $n _ { b } .$ -bit word. The bit period is $t _ { b } = 1 / x y f n _ { b } = t _ { p } / n _ { b }$ , where x and y denote horizontal and vertical resolutions, f is the refresh rate, $n _ { b }$ is the number of bits per pixel per channel, and $t _ { p }$ is the pixel period.

For a single channel, the serialized TMDS words form a bitstream. Let $c _ { k } \in \{ 0 , 1 \}$ denote the k-th transmitted bit, i.e., the binary digit obtained by serializing the pixel words. The emitted voltage can be written as

$$
\hat {v} (t) = \sum_ {k = - \infty} ^ {\infty} c _ {k} b (t - k t _ {b}) = c (t) X _ {t _ {b}} (t),\tag{1}
$$

where $b ( t )$ is the unit-bit pulse. The bit sequence can be further expressed using a Dirac comb representation. Define the Dirac comb [29], and we obtain the convolution form

$$
\hat {v} (t) = b (t) * \left[ c (t) X _ {t _ {b}} (t) \right].\tag{2}
$$

Taking the Fourier transform and using the convolution– multiplication duality yields

$$
\mathcal {F} \{\hat {v} \} (f) = B (f) \left[ C (f) * \mathcal {F} \{X _ {t _ {b}} \} (f) \right].\tag{3}
$$

By the transform property of the Dirac comb, $\mathcal { F } \{ X _ { t _ { b } } \} ( f ) =$ $1 / t _ { b } X _ { 1 / t _ { b } } ( f )$ , and therefore

$$
\mathcal {F} \{\hat {v} \} (f) = \frac {1}{t _ {b}} B (f) \cdot \left[ C (f) * X _ {1 / t _ {b}} (f) \right].\tag{4}
$$

The spectrum thus consists of periodic replicas spaced by $1 / t _ { b }$ . Compared with per-pixel modulation, resolving individual bits requires a n<sub>b</sub> times higher bandwidth. Consequently, the sampling frequency must satisfy $f _ { s } \ge 1 / 2 t _ { b } = n _ { b } / 2 t _ { p }$ However, in many practical receivers, the effective sampling is closer to $f _ { s } \gtrsim 1 / 2 t _ { p }$ , which acts as a low-pass filter of the TMDS waveform: individual bits cannot be resolved, and only the per-pixel average is preserved. Importantly, because different colors correspond to different TMDS bit patterns, these averages still retain substantial, recognizable information.

## 5.1.2 Pixel Period and Modulation Window

To achieve active control of EM radiation, precise temporal modulation must be coordinated at the granularity of individual pixels. We define the pixel period $t _ { \mathrm { p } } = 1 / f _ { p }$ and frame period as $t _ { \mathrm { r } } = 1 / f _ { r }$ , where $f _ { \mathfrak { p } }$ is the cable’s pixel clock and $f _ { r }$ is the frame rate. The modulation is confined to the effective area (EA) region, with no modulation taking place in the inactive area (IA). For pixel m in row k, denote the unit rectangular pixel pulse by $p ( \cdot )$ and the row period by $T _ { \mathrm { r o w } }$ Then the pixel pulse train under gating is

$$
\begin{array}{l} s (t) = \chi_ {\mathrm{EA}} (t) \sum_ {k = 1} ^ {Y} \sum_ {m = 1} ^ {X} a _ {k, m} p \left(t - t _ {f} - (k - 1) t _ {\mathrm{r}} - (m - 1) t _ {\mathrm{p}}\right) \\ + \chi_ {I A} (t) s _ {I A} (t), \end{array} \tag {5}
$$

where ${ a } _ { k , m }$ denotes the pixel modulation coefficient and $t _ { f }$ is the start time of $\operatorname { E A } ; \chi _ { \operatorname { E A } } ( t ) \in \{ 0 , 1 \}$ is the EA gate, $\chi _ { I A } ( t ) =$ $1 - \chi _ { \mathrm { E A } } ( t )$ its complement for the IA, and $s _ { I A } ( t )$ is the baseline waveform during blanking.

The effective modulation window is written as

$$
s _ {e} (t) = \alpha \eta_ {\text { code }} \beta \chi_ {\mathrm{EA}} (t),\tag{6}
$$

where α denotes the fraction of the EA period used for signal modulation, $\boldsymbol { \eta } _ { \mathrm { c o d e } }$ denotes the coding efficiency (ratio of use ful bits to transmitted bits), and $\beta$ represents the magnitude constraint factor imposed by visual perception limits.

## 5.1.3 Pixel-Sample Mapping

To allocate time at the sample granularity, let $F _ { s }$ be the receiver sampling rate and let each symbol span $S _ { \mathrm { s y s } }$ samples (a DSSSlike spreading factor [30], chosen by the channel conditions). Define the ideal number of pixels per symbol

$$
\pi_ {\text { sym }} = \frac {S _ {\text { sys }} F _ {\text { PIX }}}{F _ {s}},\tag{7}
$$

where $F _ { \mathrm { P I X } }$ is the pixel clock. With $F _ { s }$ fixed, a larger $S _ { \mathrm { s y s } }$ yields a wider per-symbol pixel span, increasing processing gain and interference tolerance at the expense of a lower symbol rate.

For a precise pixel-sample mapping, we introduce a nondecreasing sequence of pixel-edge indices $\{ C _ { g } \} _ { g \ge 0 }$ , where $C _ { g }$ is the starting pixel index of symbol $g$ in the 1-D scan order (row-major). The set of pixel for symbol $g$ is $X _ { \mathrm { s y m } } ( g ) = \{ x \mid$ $C _ { g } \leq x < C _ { g + 1 } \} , \mathrm { s o } \ | X _ { \mathrm { s y m } } ( g ) | \approx \pi _ { \mathrm { s y m } }$ . Therefore, the duration time of the symbol cells is $t _ { k , g } = ( C _ { g + 1 } - C _ { g } ) T _ { \mathrm { c l k } } \approx S _ { \mathrm { s y s } } / F _ { s } .$ This formalization divides the continuous pixels into symbol cells of approximately equal value.

This structure provides a controllable trade-off between gain and throughput, and allows the symbol rate to scale proportionally to $F _ { s }$ when other parameters are fixed.

## 5.1.4 Imperceptible Pixel Modulations

Depending on the prevailing channel conditions and the spe cific transmission requirements, we employ different channel coding strategies, a small modification δ is added to the selected pixels, as elaborated in the following.

a) Intra–Row OOK Modulation. To change the emitted EM power while preserving visual quality, we apply a small same-polarity modification to all pixels within a symbol window, i.e., on the pixel set $X _ { \mathrm { s y m } } ( g )$ mapped from bit $b _ { g } \in \{ 0 , 1 \}$ For an 8-bit grayscale, let $L _ { k , m } ^ { ( 0 ) } \in [ 0 , 2 5 5 ]$ be the original pixel value and $\delta > 0$ the modification step; we define

$$
L _ {k, m} ^ {(1)} = \left\{ \begin{array}{l l} \operatorname{clip} \bigl (L _ {k, m} ^ {(0)} + \delta \bigr), & b _ {g} = 1, (k, m) \in X _ {\text { sym}} (g), \\ L _ {k, m} ^ {(0)}, & b _ {g} = 0, \end{array} \right.\tag{8}
$$

where clip(·) limits the value to the display range. Under high-speed row scanning, the ±δ luminance changes within the window translate into a measurable intensity difference in the radiated waveform, producing a “symbol–to–radiation strength” mapping.

b) Inter–Row Differencing. For long-range links and image conditions with pronounced intensity variations, we further introduce inter–row differencing to reduce visual artifacts and increase radiated power. Neighboring rows are paired as $( 2 u , 2 u + 1 )$ ; within the same symbol window we apply opposite polarities so that visual energy cancels while RF energy adds coherently. With a row participation flag $\nu _ { m } \in \{ 0 , 1 \}$

$$
\big (L _ {2 u, m} ^ {(1)}, L _ {2 u + 1, m} ^ {(1)} \big) = \left\{ \begin{array}{l l} \Big (\operatorname{clip} \big (L _ {2 u, m} ^ {(0)} + \delta v _ {m} \big),   \operatorname{clip} \big (L _ {2 u + 1, m} ^ {(0)} - \delta v _ {m} \big) \Big), & b _ {g} = 1, \\ \big (L _ {2 u, m} ^ {(0)}, L _ {2 u + 1, m} ^ {(0)} \big), & b _ {g} = 0. \end{array} \right.\tag{9}
$$

where m $\in X _ { \mathrm { s y m } } ( g )$ . Due to the limited sensitivity of the display pipeline to high-frequency content in the vertical direction, modifications applied to adjacent rows, which are spatially proximate, effectively cancel in the perceptual domain. This cancellation enables further amplification of the emitted power while preserving visual imperceptibility.

## 5.2 Frame Structure and Coding

During covert transmission, the video emission is highly susceptible to sudden disturbances such as display jitter, occlusion, and radio-frequency interference, which can cause substantial channel variations and may even lead to the loss or severe corruption of entire pixel rows. Such errors typically occur in bursts rather than independently. To enhance robustness and mitigate row-level impairments, the transmitter employs a CRRC scheme, with corresponding decoding performed at the receiver. By dispersing burst errors into isolated symbol errors, CRRC significantly reduces the burden of error correction, thereby improving transmission reliability and link resilience.

## 5.2.1 Frame Structure

Each communication frame is organized into two main components: the Header and the Data section.

• Header: The header provides essential control information for reliable reception. It includes a frame synchronization window (FSW) and a preamble that encodes the frame identifier and serves as a known reference for synchronization and threshold initialization.

• Data: The data section carries the effective payload. It begins with the line synchronization window (LSW), followed by the private data field that encodes the user’s confidential information.

## 5.2.2 Channel Modeling

We represent the valid payload transmitted over the digital video cable as a binary sequence of length $n , c =$ $[ c _ { 0 } , c _ { 1 } , \ldots , c _ { n - 1 } ] \in \{ 0 , 1 \} ^ { n }$ . Line interference is modeled as a burst-error vector e, which produces the received sequence.

$$
r = c \oplus e, \qquad e = [ 0, \ldots , 0, \underbrace {1 , \ldots , 1} _ {W}, 0, \ldots , 0 ],\tag{10}
$$

where W denotes the length of the burst and the burst begins at the index ℓ. If the entire row is corrupted, then $W = n$

To capture the characteristics of burst errors, we adopt the Gilbert–Elliott (GE) channel model [31,32]. The channel state $C ( t ) \in \{ G , B \}$ alternates between “good” and “bad” states with symbol error rates $p _ { g } \ll p _ { b }$ , and transition probabilities $\operatorname* { P r } ( G \to B ) = \alpha , \operatorname* { P r } ( B \to G ) = \beta$ . In the bad state, contiguous errors of length $W$ occur, thereby modeling line interference as a row-level manifestation of the GE burst channel. When interleaving is applied, burst errors are dispersed across different codewords; for an interleaver with span x, the resulting effective error rate can be approximated as $\begin{array} { r } { p ^ { \prime } \approx \frac { 1 } { x } \sum _ { \ell = 0 } ^ { x - 1 } p _ { \ell } . } \end{array}$ where $p _ { \ell }$ denotes the residual error probability in the ℓ-th interleaved position.

## 5.2.3 Coding and Interleaving

Following the channel model described above, we now introduce coding and interleaving techniques to enhance robustness against burst errors. The input bitstream is first partitioned into blocks of length $k ,$ denoted by $\left\{ m _ { i } \right\}$ . Each block is then encoded into a codeword of length n bits:

$$
c _ {i} = \operatorname{Enc} (m _ {i}) \in \{0, 1 \} ^ {n}, R _ {c} = k / n.\tag{11}
$$

To prevent a single-line burst from corrupting an entire codeword, we introduce an interline interleaving strategy, where the j-th coded symbol of codeword i is mapped onto the row index

$$
\operatorname{Ip} _ {i} (j) = \left(r _ {0} (i) + j \cdot \chi\right) \bmod H.\tag{12}
$$

Here, H represents the number of encoded rows, $\mathscr { X }$ is the rowstride of the interleaver, and $r _ { 0 } ( i )$ is a per-codeword seed. In this way, adjacent bits of a codeword are not placed on the same line but are dispersed across different lines. The transmitted sequence is the permuted stream $y _ { s } = \pi ( c _ { 0 } , c _ { 1 } , \ldots , c _ { M } )$ where $\pi ( \cdot )$ denotes the interleaving operation.

## 5.2.4 Error Dispersion and Recoverability

In a progressive-row video channel, a burst disturbance span ning B continuous pixel corrupts all transmitted symbols on those lines. For any encoded codeword $c _ { i } ,$ the worst-case number of symbols corrupted after interleaving is upper bounded by $E _ { \operatorname* { m a x } } ( B , \chi ) ~ \leq ~ \lceil B / \chi \rceil$ , where $\mathscr { X }$ denotes the interleaver span. Hence, by ensuring $\chi \geq \lceil B / t \rceil$ , the system guarantees that, even under a burst affecting B consecutive lines, the number of corrupted symbols per codeword remains bounded by the channel decoder’s correction capability t.

Consequently, the probability of successful recovery can be lower-bounded as $\begin{array} { r } { P _ { \mathrm { s u c c } } \geq \sum _ { i = 0 } ^ { t } { \binom { n } { i } } ( p ^ { \prime } ) ^ { i } ( 1 - p ^ { \prime } ) ^ { n - i } } \end{array}$ , where $p ^ { \prime }$ denotes the effective symbol error rate of the Gilbert–Elliott channel after interleaving.

## 5.3 Receiver Design.

## 5.3.1 Multi-Band Sampling and Fusion

To complement the transmitter-side design, the receiver performs band-wise demodulation and then fuses per-band evidence using channel-aware weights estimated from per-band SNR and preamble correlation.

Consider the g-th symbol window. Let $X _ { g }$ denote the set of pixel indices within the window, $q _ { g } [ m , n ] \stackrel {  } { \in } \{ + 1 , - 1 \}$ the demodulation mask aligned with the transmitter, and $I _ { k } [ m , n ]$ the recovered pixel value at location $( m , n )$ from the k-th subband. The per-band coherent accumulation statistic is

$$
z _ {g, k} = \frac {1}{| X _ {g} |} \sum_ {(m, n) \in X _ {g}} q _ {g} [ m, n ] I _ {k} [ m, n ],\tag{13}
$$

where $\boldsymbol { z } _ { g } = \left[ z _ { g , 1 } , \ldots , z _ { g , K } \right] ^ { \intercal }$ . Let $\boldsymbol { w } = \left[ w _ { 1 } , \ldots , w _ { K } \right] ^ { \top }$ denote nonnegative reliability weights derived from SNR and preamble correlation estimates. Cross-band linear fusion then yields the combined statistic

$$
Z _ {g} = \sum_ {k = 1} ^ {K} w _ {k} z _ {g, k} = w ^ {\top} z _ {g}.\tag{14}
$$

## 5.3.2 Matched-Filter Correlation

In high–speed video covert communication, a loss of row/frame synchronization can catastrophically corrupt symbol decisions (e.g., entire rows of pixels). Therefore, we require a synchronization method that remains reliable under noise, texture, multipath, and strong jitter.

Let the known template sequence be a bipolar template $s [ m ] \in \{ - 1 , + 1 \}$ of length $L ,$ and let r[n] be the received sequence. The matched–filter correlation at lag n is

$$
R [ n ] = \sum_ {m = 0} ^ {L - 1} r [ n + m ] s ^ {*} [ m ].\tag{15}
$$

where $( \cdot ) ^ { * }$ denotes complex conjugation.

To remove channel–gain variations, video–brightness drift, and row–to–row amplitude mismatch, we adopt the normalized cross–correlation [33]

$$
\widehat {R} [ n ] = \frac {\left| s ^ {H} r _ {n} \right|}{\| s \| _ {2} \| r _ {n} \| _ {2}} \in [ 0, 1 ],\tag{16}
$$

where $r _ { n } \triangleq \left[ r [ n ] , \ldots , r [ n + L - 1 ] \right] ^ { T } . \widehat { R } [ n ]$ closer to 1 indicates that the received signal closely matches the template at that position, whereas values closer to 0 indicate a complete mismatch. Thus, the candidate synchronization index is chosen as the Maximum Peak Location $n _ { \mathrm { m a x } } = \arg \operatorname* { m a x } _ { n } \widehat { R } [ n ]$ . To reject spurious peaks caused by image texture or multipath, we introduce a peak–sharpness gate based on a peak–to–secondary ratio together with a double–threshold rule:

$$
\gamma = \frac {\widehat {R} [ n _ {\max} ]}{\max _ {n \neq n _ {\max}} \widehat {R} [ n ]}, \quad \widehat {R} [ n _ {\max} ] \geq \tau_ {r}, \gamma \geq \gamma_ {\text {th}}.\tag{17}
$$

Here, τ<sub>r</sub> controls the absolute peak height (match confidence), while $\gamma _ { \mathrm { t h } }$ controls the sharpness of the mainlobe with respect to neighboring sidelobes.

## 5.3.3 HBI–Aware Row Boundary Detection.

With progressive scanning of the digital video cable, the w segments immediately preceding a row boundary c typ ically lie in the horizontal IA, whereas the subsequent w segments belong to the EA. Define the forward and backward windows ${ \mathcal { W } } _ { + } ( c ) = \{ c , c + 1 , \ldots , c + w - 1 \}$ and $\mathcal { W } _ { - } ( c ) =$ $\{ c - w , \ldots , c - 1 \}$ , and let $h _ { m } \geq 0$ denote a symmetric window function applied to suppress edge ringing. Denote by $r [ \cdot ]$ the in-segment statistic; the corresponding windowed energies are given by

$$
E _ {+} (c) = \sum_ {m = 0} ^ {w - 1} h _ {m} \left| r [ c + m ] \right| ^ {2},\tag{18a}
$$

$$
E _ {-} (c) = \sum_ {m = 0} ^ {w - 1} h _ {m} | r [ c - 1 - m ] | ^ {2}.\tag{18b}
$$

Let $\sigma _ { \mathrm { g a p } }$ denote the noise estimated within IA. We then construct a composite statistic that integrates a standardized energy gap with an energy ratio, incorporating a small stabilizing term $\lambda > 0$

$$
\ln \beta (c) = 2 \ln \left(\frac {\left| E _ {+} (c) - E _ {-} (c) \right|}{\sigma_ {\text { gap }} \sqrt {\sum_ {m = 0} ^ {w - 1} h _ {m} ^ {2}}}\right) + \alpha \ln \left(\frac {E _ {+} (c) + \lambda}{E _ {-} (c) + \lambda}\right) \geq \ln \beta_ {\text { th }}.\tag{19}
$$

The threshold $\beta _ { \mathrm { t h } }$ is set from the empirical distribution of IA–only statistics; when $\beta ( c ) \geq \beta _ { \mathrm { t h } }$ , the following w segments are declared to belong to the $\mathrm { A E }$ . The forward window is anchored in IA as background; the Hann window $h _ { m }$ suppresses boundary ringing. The parameters α and $\beta _ { \mathrm { t h } }$ are adapted to the estimated SNR.

## 5.3.4 Adaptive Decision Threshold

Since each frame in our covert channel begins with a known pilot, we leverage this segment to adaptively estimate the decision threshold. This design choice is motivated by the low-SNR and long-range operating regime, where a fixed threshold would lead to severe performance degradation. By exploiting the statistics of the preamble symbols, ADT dynamically selects and updates the threshold, significantly improving decoding robustness while preserving the lightweight nature of the receiver.

Specifically, by scanning candidate thresholds on the pilot symbols, the optimal threshold $T ^ { \star }$ is selected by minimizing the preamble bit-error rate. To suppress slow drift, the online threshold $T _ { t } = ( 1 - \alpha ) T _ { t - 1 } + \alpha T ^ { \star }$ can be exponentially smoothed. The decision polarity is determined from the preamble orientation statistic, denoted as flag $\in \{ + 1 , - 1 \}$ and v<sub>i</sub> represents the decision statistic (e.g., the fused metric $z _ { g } )$ for the i-th symbol.

For the data segment, symbol decisions are obtained as

$$
\hat {b} _ {i} = \mathbf {1} \left\{\operatorname{flag} \cdot \left(v _ {i} - T _ {t}\right) > 0 \right\},\tag{20}
$$

where $\mathbf { 1 } \{ \cdot \}$ is the indicator function. The estimated bit sequence is then de-interleaved and FEC-decoded (Forward Error Correction):

$$
\hat {m} = \operatorname{Decode} (\operatorname{DeInterleave} (\hat {b})).\tag{21}
$$

By explicitly minimizing $\mathrm { B E R } _ { \mathrm { p } } ( T )$ in the preamble symbol, ADT adaptively selects the threshold $T ^ { \star }$ and applies it to subsequent transmitted data, thus significantly improving the decision margin and recovery performance under low SNR or long-range conditions.

## 6 Evaluation

In this section, we provide a detailed introduction to the experimental setup, evaluation metrics, and the impact performance of TrojPix in the real world and various influencing factors.

## 6.1 Experimental Setup

As shown in Fig. 7, we demonstrate the covert communication process of TrojPix in real-world scenarios. The transmitter employs a monitor connected via a video cable to play the attack video. The receiver’s acquisition system consists of a USRP X310 device equipped with a UBX-160 daughterboard. A TFN W3 directional antenna is used for signal collection in the real environment. A FOSTTEK FST-RFAMP 09 LNA is used to enhance signal quality. The sampling rate is set to 10 MHz. The encoding and decoding of covert communication information are implemented using Python 3.10.9.

## 6.2 Metrics

• Bit Correct Rate (BCR). To assess the accuracy of the covert channel, we adopt the BCR, defined as the proportion of correctly recovered bits at the receiver. BCR provides a direct measure of the reliability of covert communication. Unless otherwise specified, all BCR values in the evaluation are computed on the raw bitstream; error-corrected results are reported explicitly when used.

![](images/ec8e3c75637a14216db7a1fd700e8dab6729bab7dc0c6a990ec0b12b8d001f50.jpg)  
Figure 7: Attack scenarios in real-world settings. Left: moni tor displaying the embedded attack video. Right: SDR-based receiver setup. The experiments are conducted and evaluated in both indoor and outdoor environments.

• Signal-to-Noise Ratio (SNR). We evaluate covert channel quality via PSD-based SNR using Welch’s method [34], and the occupied bandwidth B is identified. The in-band power is $P _ { \mathrm { t o t a l } }$ , while the noise power is approximated as $P _ { n } = N _ { 0 } .$ B from adjacent out-of-band regions. Thus, the signal power is $P _ { s } = P _ { \mathrm { t o t a l } } - P _ { n } .$ , and the SNR in dB is $\mathrm { S N R _ { d B } } = 1 0 \log _ { 1 0 } ( P _ { s } / P _ { n } )$

• Structure Similarity Index Measure (SSIM). To evaluate image similarity [35], we adopt SSIM, which jointly compares luminance, contrast, and structural information between two images. A higher SSIM value indicates greater perceptual similarity.

• Learned Perceptual Image Patch Similarity (LPIPS). To assess perceptual similarity between the embedded and original images, we adopt LPIPS [36], which measures their perceptual distance. Lower LPIPS values indicate closer perceptual alignment between the generated and reference images.

## 6.3 Experimental Results

## 6.3.1 Impact of Different Video Cables

To evaluate the impact of cable manufacturer and length on TrojPix, we test 15 COTS digital video cables from multiple manufacturers, including UGREEN, SAMZHE, HP, CHOSEAL, JIANGDUN, JINGHUA, PHILIPS, and DELL, covering six common lengths (0.5 m, 1 m, 1.5 m, 2 m, 3 m, and 5 m). We evaluate on Dell U2417H monitor fixed at 1920×1080 resolution and 60 Hz refresh rate, while the receiving antenna is positioned 20 meters from the target.

Tab. 2 reports the performance of TrojPix across different cable manufacturers and lengths. The average BCR reaches 99.20% across all cables, with an average SNR of 15.99 dB. After applying FEC, the BCR improves to 100% on all tested cables. At the same length, differences among manufacturers are minor; for instance, at 1 m, Choseal achieves the highest BCR (99.18%), while HP is slightly lower (99.10%). Within a single manufacturer (e.g., UGREEN), the BCR increases with cable length, reaching 99.60% at 5 m. In general, the SNR values remain comparable under all conditions, demonstrating that TrojPix consistently delivers stable and robust performance across different cable manufacturers and lengths.

Table 2: Impact of different video cables.

<table><tr><td>Manuf.</td><td>Length</td><td>BCR</td><td>SNR (dB)</td></tr><tr><td rowspan="2">SAMZHE</td><td>0.5m</td><td>99.08%</td><td>15.77</td></tr><tr><td>1m</td><td>99.12%</td><td>15.87</td></tr><tr><td rowspan="2">HP</td><td>0.5m</td><td>99.06%</td><td>15.74</td></tr><tr><td>1m</td><td>99.10%</td><td>15.83</td></tr><tr><td>PHILIPS</td><td>2m</td><td>99.38%</td><td>16.78</td></tr><tr><td>CHOSEAL</td><td>1m</td><td>99.18%</td><td>15.67</td></tr><tr><td>JIANGDUN</td><td>1.5m</td><td>99.00%</td><td>15.71</td></tr><tr><td>JINGHUA</td><td>1.5m</td><td>98.78%</td><td>13.73</td></tr><tr><td>DELL</td><td>1.8m</td><td>99.21%</td><td>15.34</td></tr><tr><td rowspan="6">UGREEN</td><td>0.5m</td><td>99.12%</td><td>15.12</td></tr><tr><td>1m</td><td>99.13%</td><td>15.19</td></tr><tr><td>1.5m</td><td>99.19%</td><td>15.54</td></tr><tr><td>2m</td><td>99.22%</td><td>15.92</td></tr><tr><td>3m</td><td>99.29%</td><td>16.17</td></tr><tr><td>5m</td><td>99.31%</td><td>16.35</td></tr></table>

All values are measured at 20 m; with FEC, the results are completely correct for all cables.

## 6.3.2 Impact of Different Monitors

To evaluate the impact of monitors on TrojPix, we assess covert communication performance on twelve COTS displays from nine major manufacturers: DELL, AOC, Redmi, PHILIPS, Lenovo, SAMSUNG, LG, HUAWEI, and TCL. The resolution is fixed at 1920×1080@60 Hz. A 1.5 m UGREEN video cable is used, and the receiving antenna is positioned 20 m from the transmitter.

Tab. 3 summarizes the evaluation results, with an average BCR of 99.13% and an average SNR of 15.25 dB. Among all models tested, TCL T27M6C achieves the highest BCR (99.26%), while even the lowest performing display (Redmi Mi) still maintains 99.01%. Interestingly, although the SAM-SUNG LS27D800 attains the highest SNR, its BCR is not the highest, likely due to EM leakage from internal cabling interfering with the covert signal. Overall, TrojPix has an average BCR of 99.13% in heterogeneous display environments, demonstrating strong robustness against monitor variations.

## 6.3.3 Impact of Resolution

To evaluate the impact of display resolution on TrojPix, we test five commonly used settings: 800×600, 1280×720,

Table 3: Evaluation on different monitors.

<table><tr><td>Brand</td><td>Manuf.</td><td>BCR</td><td>SNR (dB)</td></tr><tr><td rowspan="2">DELL</td><td>S2421HSX</td><td>99.19%</td><td>15.12</td></tr><tr><td>U2417H</td><td>99.19%</td><td>15.54</td></tr><tr><td rowspan="2">AOC</td><td>U2790B</td><td>99.08%</td><td>15.58</td></tr><tr><td>U27B35</td><td>99.25%</td><td>15.33</td></tr><tr><td>Redmi</td><td>Mi Monitor</td><td>99.01%</td><td>15.05</td></tr><tr><td rowspan="2">PHILIPS</td><td>PHL</td><td>99.16%</td><td>14.68</td></tr><tr><td>27E1N1820</td><td>99.02%</td><td>14.18</td></tr><tr><td>Lenovo</td><td>N2721U</td><td>99.10%</td><td>14.99</td></tr><tr><td>SAMSUNG</td><td>LS27D800</td><td>99.26%</td><td>16.00</td></tr><tr><td>LG</td><td>27US550</td><td>99.01%</td><td>14.81</td></tr><tr><td>HUAWEI</td><td>MateViewSE</td><td>99.07%</td><td>14.96</td></tr><tr><td>TCL</td><td>T27M6C</td><td>99.23%</td><td>16.18</td></tr></table>

With FEC, the results are completely correct for all monitors.

1366×768, 1600×900, and 1920×1080. The refresh rate is fixed at 60 Hz, using a DELL U2417H monitor with 4 video cables: SAMZHE (1 m), HP (0.5 m), PHILIPS (2 m), UGREEN (1.5 m). The receiving antenna is positioned 20 m from the target device.

Fig. 8(a) shows the evaluation results under different resolutions. The observed BCRs exhibit only negligible variation across the five configurations: the highest is 99.19% at 1366×768, and the lowest is 99.11% at 800×600—an almost indistinguishable difference. Likewise, the variations in SNR remain minimal. These results indicate that the display resolution has little impact on covert communication performance, since resolution is handled at the display end and remains in dependent of the underlying data transmission. Consequently, data embedding is feasible at arbitrary display resolutions.

## 6.3.4 Impact of Distance

To evaluate the impact of distance on TrojPix, we conduct covert communication experiments at a distance ranging from 20 m to 120 m with increments of 20 m. The transmitter is DELL U2417H fixed at 1920×1080@60 Hz.

To further evaluate the result of transmission distance, Fig. 8(b) reports the evaluation results across different distances. As distance increases, the BCR of the raw bitstream declines due to signal attenuation and multipath effects. Although the use of a directional antenna and a low-noise amplifier improves the SNR, they cannot fully compensate for severe signal loss at long range. In particular, TrojPix still achieves a BCR of 99.19% at 20 m and 91.02% at 120 m.

To explore the maximum attack range, we gradually increase the distance in an outdoor environment while keeping the same RF front-end and modulation settings. At 208 me ters, we are still able to successfully recover a complete data packet, with the preamble acquired, the lock established, and the cyclic redundancy check passed. These results demon strate that TrojPix exhibits strong resilience against distanceinduced degradation and remains practically viable in realworld scenarios.

![](images/bf5769b1bafdc2a9014c2c2490e0543677b193f296427786a59ab3d6f433ced2.jpg)  
(a)

![](images/5992fdeeb77b68ab65383b5d914e625ac92dc76119e1287f4018a1b064f3bb1c.jpg)  
(b)

Figure 8: Impact of resolution and distance.  
![](images/083c92517b6a3d060cc4af66aed74ac0134ca03eac9e096a73e1c0a100eaf334.jpg)  
(a)

![](images/a140b2815d4638302d7ce93138916496d709c99d39f57a8dd39dec2531971bb1.jpg)  
(b)  
Figure 9: Impact of video cable and sampling rate.

## 6.3.5 Through-Wall Evaluation

We evaluate the performance of TrojPix with the EM signal penetrating through a wall. The wall is made of concrete and is 30 cm thick, while the receiving antenna is positioned at a distance of 10 m from the target device. In addition, we consider the same settings as in Section 6.3.3 in terms of cables and display model. The resolution fixes at 1920\*1080@60Hz.

Fig. 9(a) shows that the BCR of SAMZHE decreases the most, dropping by 1.49% after signal penetration, while PHILIPS experiences the smallest drop of only 0.3%. Overall, the average BCR declines from 99.96% before penetration to 99.14% after penetration. The overall performance remains stable, indicating that wall materials exert only a limited impact on the covert communication effectiveness of TrojPix, thereby demonstrating the robustness of TrojPix in complex transmission environments.

## 6.3.6 Impact of Sampling Rate

To evaluate the impact of the sampling rate on TrojPix, we consider four sample rates: 5 MHz, 10 MHz, 15 MHz, and 20 MHz. The settings of cables, display model, and resolution are the same as in Section 6.3.5, at distance of 20 m.

![](images/4a7abd0a01305a2f01d8f659f34c7be8fa14085df9a89eabc0970050d8d7b6fe.jpg)

![](images/2f60731582413f3d70942cc75e9fbd715472f8e6fb9591b634dd2ab7b542a095.jpg)  
(a) BCR (%)

![](images/ead1700ef4c3ff521751a156a1e31670d717985d068b3f9d00612bd44b066ead.jpg)  
(b) SNR (dB)  
Figure 10: Impact of angle.

Fig. 9(b) presents the results of covert communication at different sampling rates. The BCRs at 5 MHz, 10 MHz, 15 MHz, and 20 MHz are 99.20%, 99.13%, 99.19%, and 99.21%, respectively, with the BCR probability being extremely high. We also evaluate the maximum achievable transmission rate, which increases with sampling rate, yielding 1.8 MHz, 3.8 MHz, 5.9 MHz, and 8.1 MHz for 5 MHz, 10 MHz, 15 MHz, and 20 MHz, respectively. Using devices that support higher sampling rates can further increase the maximum transmission rate.

## 6.3.7 Impact of Angle

To evaluate the impact of angle on TrojPix, we perform our covert communication with the receiving antenna at different orientations ranging from 0<sup>◦</sup> to 360<sup>◦</sup> with 45<sup>◦</sup> increments. The receiving antenna is positioned 20 m from the target device. In addition, we use the same settings as Section 6.3.6.

Fig. 10 presents the evaluation results under different orientations. The BCR and SNR exhibit only small fluctuations with angle, indicating stable performance. In all antenna ori entations considered, TrojPix achieves an average BCR of 99.16% and an average SNR of 14.96 dB, demonstrating strong angular robustness and communication stability.

## 6.3.8 Transmission in Different Scenarios

We evaluate the perceptual imperceptibility and communica tion reliability of TrojPix under images with varying texture complexity. In particular, we select two representative ex amples: a popular webpage (Fig. 11(a)) and a natural scene (Fig. 11(c)). Therefore, we embed payloads into video frames driven by these source images for transmission tests. The embedded images exhibit negligible perceptual differences, with SSIM of 0.998 and 0.999, and LPIPS scores of 0.002 and 0.005 for the popular webpage and the natural scene.

On the receiver side, reconstructed images based on de coded bits are shown in Fig. 11(b)(d). Even under complex textured backgrounds, TrojPix achieves BCRs of 99.82% / 99.36%, respectively. These results demonstrate that TrojPix maintains near-perfect channel reliability while preserving perceptual quality that is indistinguishable from the originals. We observe that complex textures introduce mild content dependency, leading to slight variations in the effective channel state. However, adopting stronger content-adaptive modulation and coding strategies could further enhance the robustness of TrojPix.

![](images/1a925248d28fd64310846a3d14e346cd02578b596707693c5e9fcb3812a4f55b.jpg)

![](images/6a9433384212a58ad12ce6f25a191fd575ca54fad10001fb70da5570f6f1e25d.jpg)  
(a) Source image (webpage)  
(b) Reconstructed image from (a)  
(c) Source image (natural scene) (d) Reconstructed image from (c)  
Figure 11: Transmission under different visual scenarios. Payloads are embedded into video frames derived from source images and reconstructed at the receiver.

We further conduct a subjective perceptual study with 50 volunteers, where participants are asked to compare the displayed content before and after running TrojPix and report any visually perceivable changes. As shown in Tab. 4, none of the participants report any perceivable visual differences. This confirms that TrojPix does not introduce noticeable visual artifacts during operation, demonstrating its strong perceptual imperceptibility in practice.

## 6.3.9 Transmission of Different Size of Files

To evaluate the capability of TrojPix in transmitting real files, we selected file segments of various sizes (10 KB, 100 KB, 1 MB, and 10 MB) from the enwik8 corpus of the Mahoney dataset [37] and use them as transmission payloads. The transmitter is a DELL U2417H monitor fixed at 1920×1080@60 Hz, with a 1.5 m Ugreen video cable, and the receiving antenna is positioned 10 m away.

Tab. 5 shows the evaluation results for different file sizes. As file size increases, the transmission rate remains high at 2.016 Mbps for the 10 MB payload. The system performs efficiently with no significant variation in BCR, and both bit and character accuracy remain at 100%, demonstrating TrojPix’s strong reliability and efficiency in file transfer scenarios.

## 6.3.10 Impact of Shielding

To evaluate the impact of electromagnetic shielding on TrojPix, we conducte comparative experiments using several representative materials, including aluminum foil tape (Al), tinned copper mesh (TC), ferrite sheet (FS), and highpermeability ferronickel alloy (FN). The video cable already incorporates native shielding; each material is additionally wrapped around the cable, and the distance between the re ceiver and the target device is fixed at 20 m.

Table 4: User study on perceptual visibility.

<table><tr><td>Users</td><td>Perceptible</td><td>Imperceptible</td></tr><tr><td>Male (25)</td><td>0</td><td>25</td></tr><tr><td>Female (25)</td><td>0</td><td>25</td></tr></table>

Table 5: Transmission performance across different file sizes.

<table><tr><td>File Size</td><td>Time</td><td>BCR</td><td>Char Accuracy</td></tr><tr><td>10 KB</td><td>33 ms</td><td>100%</td><td>100%</td></tr><tr><td>100 KB</td><td>420 ms</td><td>100%</td><td>100%</td></tr><tr><td>1 MB</td><td>4.13 s</td><td>100%</td><td>100%</td></tr><tr><td>10 MB</td><td>41.6 s</td><td>100%</td><td>100%</td></tr></table>

Fig. 12(a) shows the results under different shielding conditions, where “None” denotes the baseline without additional shielding. Among the tested materials, tinned copper braided shielding causes the most pronounced performance degrada tion, reducing the success rate to 91.02%, followed by aluminum foil tape, ferronickel alloy, and ferrite sheet. Notably, while shielding materials cause varying degrees of performance drop, the success rate remains above 91% in all cases. Overall, enhanced electromagnetic shielding can partially degrade TrojPix communication but remains insufficient to fundamentally block the covert channel.

## 6.3.11 Impact of Multiple Monitors

To evaluate the impact of nearby active monitors on the covert communication performance of TrojPix, we gradually introduce one to three additional monitors operating normally within a distance of 0.5 m from the target display. The config uration of the target monitor remains identical to that in the previous experiments, and all displays are set to a resolution of 1920×1080 at 60 Hz. 1.5 m UGREEN video cables are used, and the distance between the receiving antenna and the target device are fixed at 20 m.

Fig. 12(b) summarizes the results under varying numbers of nearby monitors, where “0” denotes the baseline case without any adjacent monitors. The results show that increasing the number of nearby monitors leads to slight but observable performance degradation. The BCR decreases from 99.19% at 0 to 98.81% at 3 monitors, and SNR also shows a mild drop from 15.54 dB to 15.02 dB. Nevertheless, the overall impact remains limited and does not result in a significant loss of communication reliability.

![](images/82fee597dbc97c439331900bc5daca76648636fa626e6db2a52b879a32a8b639.jpg)  
(a) Nearby monitors

![](images/f2e5ecd3c425ae8fb2862a92235c9bd38e3469e3ee75cf78dda215893bda644e.jpg)  
(b) Shielding materials  
Figure 12: Impact of nearby monitors and shielding materials.

## 7 Discussion

In this section, we give methods to mitigate TrojPix covert channel attack, followed by a discussion of future work.

## 7.1 Defense

EM Shielding and Signal Interference: Analysis shows that one of the key factors for TrojPix to realize covert communication lies in its potential risk of EM information leakage; therefore, physical layer protection measures can be taken. On one hand, EM shielding can be implemented based on the Faraday cage principle, using shielding materials wrapped around key components to attenuate field strength leakage, as shown in Section 6.3.10. On the other hand, EM interference equipment can be deployed in the vicinity of the area of use, transmitting suppressive interference signals to cover the target frequency band, in order to cover the characteristics of the effective EM information and block its propagation path. Although this alleviates TrojPix’s threat to some extent, it does not eliminate it, and deploying shielding materials and interference equipment adds an economic burden. Therefore, the use of EM leakage-free video interfaces (e.g., fiber-optic or wireless, etc.) can be more effective in mitigating the hazards posed by EM leakage.

Random Transmission and Pixel Smoothing: Another key factor for TrojPix to realize covert communication originates from the sequential transmission characteristic of the TMDS protocol. To mitigate the risk of EM information leakage caused by this, the transmission sequence of TMDS signals can be changed from a fixed to a random mode, and since the attacker cannot predict the random sequence, it is difficult to recover the effective information even if the leaked signals are intercepted. For the exploitable bit-flip characteristics in TMDS coding, it is necessary to implement smoothing to minimize the number of bit-flips between adjacent pixels, so that the characteristics of the leaked EM signals corresponding to different information contents tend to be the same, thus eliminating their ability to carry communication information. However, compared with pixel smoothing, which mainly involves the adjustment of coding algorithms, the implementation of the randomized transmission mode requires a higher cost, which not only requires the replacement of hardware equipment, but also requires the redesign of the transmission architecture to adapt to the new randomization mechanism, and thus requires a comprehensive trade-off in practice.

## 7.2 Future Work

In this study, we show that the unintentional EM signals generated by digital video cables during normal display can be precisely manipulated and used to construct covert communication channels. We realize high-speed covert communication based on video cables through lightweight pixel-level modula tion, and complete systematic validation in multi-dimensional scenarios. In the future, we will extend the method to all kinds of mainstream video interfaces and display devices, and test its universality under different system configurations such as refresh rates and hardware combinations. On this basis, we will also explore more efficient and flexible modulation coding and signal reception schemes to significantly improve communication rate, stability, and covertness. We also intend to investigate and develop practical protection schemes to provide a theoretical foundation and engineering reference for EM leakage protection in high-security environments.

## 8 Related Work

## 8.1 EM Side-Channel on Cryptographic Keys

Extracting cryptographic keys through EM side-channel is a serious and widely recognized threat. Early studies demonstrate that EM emissions from cryptographic hardware are sufficient to leak sensitive information. [38] shows that the EM emissions from field-programmable gate array (FPGA) devices could be exploited to reconstruct complete keys. Sub sequently, [39] confirms that EM radiation can serve as a feasible vector for side-channel attacks. [40] further evaluates and discusses the risks associated with reconstructing keys from FPGA emissions.

Research later shows that attack targets expand to more complex computing platforms. [41] demonstrates how CPU emissions can be exploited to steal cryptographic keys, while [42] conducts the first physical side-channel attack on elliptic-curve cryptography in personal computers. Several works [43–47] exploit EM leakages from SoC components for key-recovery attacks. [48] shows that EM side channels could be used to extract ECDSA keys from smartphones. [40] further demonstrates that EM side channel can be used to identify cryptographic algorithms running on IoT devices.

As research deepens, attack techniques gradually evolve into more automated and efficient analysis methods. [49] introduces SCNIFFer, a low-cost automated platform to scan cryptographic chips and identify high-leakage regions for endto-end attacks. More recent work shows that EM side channels can be highly effective in recovering complete AES keys from a variety of hardware platforms [50–53]. A common characteristic of these works is the ability to leverage large volumes of EM leakage data to infer a small and precise set of target keys.

Since the discovery of EM leakage, its application in cryptographic key extraction has remained a central research focus, but its potential for covert communication has not yet been fully explored. Building on this gap, this paper further investigates a covert communication method based on video-cable emissions and demonstrates the recovery of sensitive data at the receiver side.

## 8.2 Covert Communication Technology

Existing research shows that attackers can exploit various unintended physical channels [54, 55] such as sound, light, magnetic fields, and heat to achieve covert communication. [10] and [56] construct low-bandwidth thermal covert channels by modulating processor workloads to induce temperature fluctuations. [11] and [12] establish acoustic covert channels using acoustic noise and hard drive noise, respectively. [13] and [57] demonstrate optical covert channels based on hard drive indicator lights or keyboard LEDs. Meanwhile, [15–17] show that CPU and hard drive magnetic field leakage can be used to construct low-speed magnetic channels.

In comparison, channels have become a primary focus of research due to their remarkable potential. [14] establishes a power covert channel on the power line side by modulating overall system current through changes in CPU workload of a computer. Similarly, [58] exfiltrates data from a charging device by modulating workloads to decode it from the USB power channel. [17] introduces a magnetic covert channel that leaks information via CPU-induced emissions during video playback, and demonstrates that video rendering can be deliberately manipulated to generate modulated magnetic signals for data exfiltration. [18] exploits emissions from video cables in the FM band to enable covert communication within a range of several meters. [19] drives the USB bus via software to emit controllable radiation, which can then be received by software-defined radio. [20] demonstrates that leakage generated by memory buses in the cellular frequency bands can be captured by mobile basebands or SDRs. [21] leverages DRAM access patterns to modulate signals over multiple carriers, achieving covert communication at rates up to 300 kbps. [22] proposes the RF-PWM method, which transforms DRAM access noise into programmable physical-layer signals for various covert communication and attack scenarios. [23] reveals that SATA cables can serve as unintended antennas, radiating signals at both fundamental and harmonic frequencies that can be received at short distances. [24] combines emissions from video cables with LoRa technology to realize covert communication over a distance of 87.5 meters.

This paper is the first to propose a system capable of driving digital video cables to emit controllable signals while enabling visually imperceptible high-speed covert communication. Experimental results demonstrate that the system achieves a data transmission rate of 8.1 Mbps, representing more than a 27-fold improvement over SOTA (300 kbps). The maximum transmission distance reaches 208 m, approximately a 138% increase compared to SOTA (87.5 m). With respect to both core metrics—transmission rate and distance—TrojPix significantly surpasses the SOTA.

## 9 Conclusion

In this paper, we presented TrojPix, an innovative covert channel attack that exploited controllable EM emissions from digital video cables. By performing imperceptible pixellevel modulation, TrojPix enabled stable and high-throughput covert communication without requiring system privileges or hardware modifications. We systematically designed and evaluated an attack pipeline, from signal construction and modulation to long-distance decoding, demonstrating its practicality in real-world settings. Experimental results showed that TrojPix achieved a peak data transmission rate of up to 8.1 Mbps and a maximum transmission distance of 208 m, outperforming SOTA approaches and revealing information leakage risks posed by digital video cables that were previ ously underestimated.

## 10 Acknowledgment

This work is supported by National Natural Science Foundation of China (Grant No. 62202274, 62572286, 62422208, 62232010, 62350410480), Shandong Science Fund (Grant No. ZR2024MF108, ZR2025LZH006, ZR2024MF149), Ministry of Industry and Information Technology of China (Grant TC240A9ED-70), Research Project of Quancheng Laboratory, China (Grant QCL20250106), Project of the Major Innovation Project of Key Laboratory of Computing Power Network and Information Security, Ministry of Education (Grant 2024ZD012).

## 11 Ethical Considerations

In developing TrojPix, we carefully examined the ethical implications of systematically analyzing a physical-layer covert channel. Because such channels may introduce security risks, we implemented multiple safeguards to ensure that both the research process and the dissemination of results remain responsible and ethically grounded.

Stakeholders and Potential Impact. (1) Hardware manufacturers. TrojPix may place remediation pressure on display cable and interface manufacturers, as the identified EM leakage channel may necessitate improved shielding, layout redesigns, or reassessment of compliance with EM emission standards. (2) Organizations handling sensitive information. Enterprises and institutions operating air-gapped or highassurance systems may need to re-evaluate procurement, deployment, and physical isolation policies, since display components previously considered benign could introduce previously unrecognized leakage risks. (3) End users and the general public. End users may face potential privacy risks if inadequately shielded display cables are exploited in uncontrolled environments, particularly when sensitive visual content is rendered without awareness of EM side-channel exposure. (4) Security researchers and practitioners. TrojPix deepens the understanding of EM behavior in modern display systems, supporting the detection, assessment, and mitigation of physical-layer covert channels, while also revealing and characterizing a new physical-layer covert communication method that can inform studies of covert communication mechanisms and channel modeling.

Impact of the Research Process and Publication. All experiments were performed on hardware fully controlled by the authors, used synthetic or non-sensitive data, and complied with safe EM emission practices. No third-party systems, real user data, or human subjects were involved, and no operational environments were affected. Publishing the results is valuable for manufacturers, standards bodies, and defenders seeking to understand and mitigate an overlooked physical-layer leakage path. At the same time, we recognize that these concepts could inform technically capable adversaries. To minimize risk, we provide only high-level analyses and omit any reproducible or operational attack details, while clearly outlining the practical constraints and preconditions.

Mitigation of Negative Impacts. To further reduce misuse, we avoid releasing end-to-end attack toolchains, optimized parameters, or deployable covert-channel configurations. Instead, we focus on design principles, constraints, and defensive strategies. We have conducted responsible disclosure with several cable manufacturers and will continue expanding communication to share high-level findings, potential weaknesses, and feasible mitigation directions—such as improved shielding, layout adjustments, or hardware-level filtering—without revealing sensitive implementation details. Feedback from vendors will be incorporated to support longterm ecosystem security improvements.

Decision to Conduct and Publish. This study was motivated by the observation that unrecognized physical-layer channels can pose persistent risks to air-gapped and highassurance systems, and that ethical, systematic characterization is essential for building effective defenses. Our decision to publish followed a careful evaluation of risks and benefits. Withholding the findings would limit the ability of manufacturers and defenders to address a meaningful vulnerability, whereas controlled disclosure—removing operational details and incorporating vendor communication—provides clear security benefits. We therefore deem the publication of this work, in its constrained form, ethically justified.

By adhering to these principles, we aim to ensure that research on EM covert channels remains within ethical boundaries and advances responsible security. Our goal is not only to reveal an underexamined leakage vector but also to catalyze stronger hardware and system defenses, ultimately supporting safer deployment in high-confidentiality environments.

## 12 Open Science

To ensure that our research work is reproducible and to facil itate future studies, this paper provides the source code and related dataset. The code and data are available on Zenodo at https://zenodo.org/records/17905407, accompanied by comprehensive guides to help others effectively use and replicate the work. This approach follows open science practices and aims to support the research community in checking, expanding, and improving the study.

## References

[1] K. Zetter. (2014, Dec.) Hacker lexicon: What is an air gap? Accessed: 2025-12-21. [Online]. Available: https: //www.wired.com/2014/12/hacker-lexicon-air-gap/

[2] Z. Li, B. Chen, X. Chen, H. Li, C. Xu, F. Lin, C. X. Lu, K. Ren, and W. Xu, “Spiralspy: Exploring a stealthy and practical covert channel to attack air-gapped computing devices via mmwave sensing,” in The 29th Network and Distributed System Security (NDSS) Symposium 2022. The Internet Society, 2022.

[3] M. R. Na and K. Sundharakumar, “A study on air-gap networks,” in 2024 5th International Conference on In novative Trends in Information Technology (ICITIIT). IEEE, 2024, pp. 1–6.

[4] M. F. Bari and S. Sen, “Noisehopper: Emission hopping air-gap covert side channel with lower probability of detection,” in 2024 IEEE International Symposium on Hardware Oriented Security and Trust (HOST). IEEE, 2024, pp. 21–32.

[5] Y. Kim, H. An, and D.-G. Han, “Emphone: Electro magnetic covert channel via silent audio playback on smartphones,” Sensors, vol. 25, no. 18, p. 5900, 2025.

[6] N. Cranfill and J. Cleveland, “Emerging technologies for the control of the defense red switch network (drsn),” in Proceedings of MILCOM’94. IEEE, 1994, pp. 664– 668.

[7] Claroty, “How to better protect air-gapped fed eral critical infrastructure,” 2024. [Online]. Available: https://claroty.com/blog/how-to-better-protect-airgapped-federal-critical-infrastructure

[8] RESULTS Technology, “Air-gapped backups: How they can help secure your bank,” 2023. [Online]. Available: https://www.resultstechnology.com/blog/how-airgapped-backups-can-help-secure-your-bank/

[9] U.S. Nuclear Regulatory Commission, “Regulatory guide 5.71: Cyber security programs for nuclear facilities,” 2009. [Online]. Available: https://www.nrc. gov/docs/ml0903/ml090340159.pdf

[10] M. Guri, M. Monitz, Y. Mirski, and Y. Elovici, “Bitwhisper: Covert signaling channel between air-gapped computers using thermal manipulations,” in 2015 IEEE 28th Computer Security Foundations Symposium. IEEE, 2015, pp. 276–289.

[11] M. Guri, Y. Solewicz, A. Daidakulov, and Y. Elovici, “Acoustic data exfiltration from speakerless air-gapped computers via covert hard-drive noise (‘diskfiltration’),” in European symposium on research in computer security. Springer, 2017, pp. 98–115.

[12] M. Hanspach and M. Goetz, “On covert acoustical mesh networks in air,” arXiv preprint arXiv:1406.1213, 2014.

[13] M. Guri, B. Zadov, D. Bykhovsky, and Y. Elovici, “Ctrlalt-led: Leaking data from air-gapped computers via keyboard leds,” in 2019 IEEE 43rd Annual Computer Software and Applications Conference (COMPSAC), vol. 1. IEEE, 2019, pp. 801–810.

[14] ——, “Powerhammer: Exfiltrating data from air-gapped computers through power lines,” IEEE Transactions on Information Forensics and Security, vol. 15, pp. 1879– 1890, 2019.

[15] M. Guri, B. Zadov, and Y. Elovici, “Odini: Escaping sensitive data from faraday-caged, air-gapped computers via magnetic fields,” IEEE Transactions on Information Forensics and Security, vol. 15, pp. 1190–1203, 2019.

[16] N. Matyunin, J. Szefer, S. Biedermann, and S. Katzenbeisser, “Covert channels using mobile device’s magnetic field sensors,” in 2016 21st Asia and South Pacific Design Automation Conference (ASP-DAC). IEEE, 2016, pp. 525–532.

[17] J. Zhang, X. Ji, W. Xu, Y.-C. Chen, Y. Tang, and G. Qu, “Magview: A distributed magnetic covert channel via video encoding and decoding,” in IEEE INFOCOM 2020-IEEE Conference on Computer Communications. IEEE, 2020, pp. 357–366.

[18] M. Guri, G. Kedma, A. Kachlon, and Y. Elovici, “Airhopper: Bridging the air-gap between isolated networks and mobile phones using radio frequencies,” in 2014 9th International Conference on Malicious and Unwanted Software: The Americas (MALWARE). IEEE, 2014, pp. 58–67.

[19] M. Guri, M. Monitz, and Y. Elovici, “Usbee: Air-gap covert-channel via electromagnetic emission from usb,” in 2016 14th Annual Conference on Privacy, Security and Trust (PST). IEEE, 2016, pp. 264–268.

[20] M. Guri, A. Kachlon, O. Hasson, G. Kedma, Y. Mirsky, and Y. Elovici, “{GSMem}: Data exfiltration from {Air-Gapped} computers over {GSM} frequencies,” in 24th USENIX Security Symposium (USENIX Security 15), 2015, pp. 849–864.

[21] Z. Zhan, Z. Zhang, and X. Koutsoukos, “Bitjabber: The world’s fastest electromagnetic covert channel,” in 2020 IEEE International Symposium on Hardware Oriented Security and Trust (HOST). IEEE, 2020, pp. 35–45.

[22] G. Camurati and A. Francillon, “Noise-sdr: Arbitrary modulation of electromagnetic noise from unprivileged software and its impact on emission security,” in 2022 IEEE Symposium on Security and Privacy (SP). IEEE, 2022, pp. 1193–1210.

[23] M. Guri, “Satan: Air-gap exfiltration attack via radio signals from sata cables,” in 2022 19th Annual International Conference on Privacy, Security & Trust (PST). IEEE, 2022, pp. 1–10.

[24] X. Sun, Y. Zheng, W. Xi, Z. Chen, Z. Chen, H. Hao, Z. Jiang, and S. Zhong, “Tempest-lora: Crosstechnology covert communication,” in Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security, 2025, pp. 678–692.

[25] T. F. Collins, R. Getz, D. Pu, and A. M. Wyglinski, Software-Defined Radiofor Engineers. Artech House, 2018.

[26] W. Winoto, A. Molnar, and A. M. Niknejad, “Digital radio-frequency transmitters: An introduction and tutorial,” IEEE Solid-State Circuits Magazine, vol. 11, no. 2, pp. 61–73, 2019.

[27] J. Ding, W. Liu, L. Ding, J. Zhang, C. Yan, and T. Song, “New threat analysis of electromagnetic information leakage in electronic equipment based on active detection,” Communications Technology, vol. 51, no. 4, pp. 936–940, Apr. 2018.

[28] Digital Display Working Group, “Digital visual interface (dvi) specification, revision 1.0,” Digital Display Working Group, Specification Rev. 1.0, Apr. 1999. [Online]. Available: https://glenwing.github.io/ docs/DVI-1.0.pdf

[29] R. N. Bracewell, The Fourier Transform and Its Appli cations, 3rd ed. Boston: McGraw-Hill, 2000.

[30] Wikipedia contributors, “Direct-sequence spread spectrum — Wikipedia, the free encyclopedia,” 2025, accessed: 2025-08-27. [Online]. Available: https://en. wikipedia.org/wiki/Direct-sequence\_spread\_spectrum

[31] E. N. Gilbert, “Capacity of a burst-noise channel,” The Bell System Technical Journal, vol. 39, no. 5, pp. 1253– 1265, 1960.

[32] E. O. Elliott, “Estimates of error rates for codes on burstnoise channels,” The Bell System Technical Journal, vol. 42, no. 5, pp. 1977–1997, 1963.

[33] M. Schwartz, W. R. Bennett, and S. Stein, Communication systems and techniques. John Wiley & Sons, 1995.

[34] P. Welch, “The use of fast fourier transform for the estimation of power spectra: A method based on time averaging over short, modified periodograms,” IEEE Transactions on audio and electroacoustics, vol. 15, no. 2, pp. 70–73, 2003.

[35] Z. Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli, “Image quality assessment: from error visibility to structural similarity,” IEEE transactions on image processing, vol. 13, no. 4, pp. 600–612, 2004.

[36] R. Zhang, P. Isola, A. A. Efros, E. Shechtman, and O. Wang, “The unreasonable effectiveness of deep features as a perceptual metric,” in Proceedings ofthe IEEE conference on computer vision and pattern recognition, 2018, pp. 586–595.

[37] M. Mahoney, “Large text compression benchmark data,” http://mattmahoney.net/dc/textdata.html, 2009, accessed: 2025-08-25.

[38] K. Gandolfi, C. Mourtel, and F. Olivier, “Electromagnetic analysis: Concrete results,” in International workshop on cryptographic hardware and embedded systems. Springer, 2001, pp. 251–261.

[39] D. Agrawal, B. Archambeault, J. R. Rao, and P. Rohatgi, “The em side—channel (s),” in International workshop on cryptographic hardware and embedded systems. Springer, 2002, pp. 29–45.

[40] A. Sayakkara, N.-A. Le-Khac, and M. Scanlon, “Leveraging electromagnetic side-channel analysis for the investigation of iot devices,” Digital Investigation, vol. 29, pp. S94–S103, 2019.

[41] D. Genkin, L. Pachmanov, I. Pipman, and E. Tromer, “Stealing keys from pcs using a radio: Cheap electromagnetic attacks on windowed exponentiation,” in International workshop on cryptographic hardware and embedded systems. Springer, 2015, pp. 207–228.

[42] ——, “Ecdh key-extraction via low-bandwidth electromagnetic attacks on pcs,” in Cryptographers’ Track at the RSA Conference. Springer, 2016, pp. 219–235.

[43] J. Longo, E. De Mulder, D. Page, and M. Tunstall, “Soc it to em: electromagnetic side-channel attacks on a complex system-on-chip,” in International Workshop on Cryptographic Hardware and Embedded Systems. Springer, 2015, pp. 620–640.

[44] C. Ramsay and J. Lohuis, “Tempest attacks against aes,” Fox-IT, Fremont, CA, USA, Tech. Rep, 2017.

[45] G. Camurati, S. Poeplau, M. Muench, T. Hayes, and A. Francillon, “Screaming channels: When electromag netic side channels meet radio transceivers,” in Proceed ings ofthe 2018 ACM SIGSAC Conference on Computer and Communications Security, 2018, pp. 163–177.

[46] J. Danial, D. Das, A. Golder, S. Ghosh, A. Raychowd hury, and S. Sen, “Em-x-dl: Efficient cross-device deep learning side-channel attack with noisy em signatures,” ACM Journal on Emerging Technologies in Computing Systems (JETC), vol. 18, no. 1, pp. 1–17, 2021.

[47] G. Haas and A. Aysu, “Apple vs. ema: electromagnetic side channel attacks on apple corecrypto,” in Proceedings of the 59th ACM/IEEE Design Automation Conference, 2022, pp. 247–252.

[48] D. Genkin, L. Pachmanov, I. Pipman, E. Tromer, and Y. Yarom, “Ecdsa key extraction from mobile devices via nonintrusive physical side channels,” in Proceedings of the 2016 ACM SIGSAC conference on computer and communications security, 2016, pp. 1626–1638.

[49] J. Danial, D. Das, S. Ghosh, A. Raychowdhury, and S. Sen, “Scniffer: Low-cost, automated, efficient electromagnetic side-channel sniffing,” IEEE Access, vol. 8, pp. 173 414–173 427, 2020.

[50] W. Yu and J. Chen, “Deep learning-assisted and com bined attack: a novel side-channel attack,” Electronics Letters, vol. 54, no. 19, pp. 1114–1116, 2018.

[51] V. V. Iyer and A. E. Yilmaz, “Using the anova f-statistic to rapidly identify near-field vulnerabilities of cryptographic modules,” in 2021 IEEE MTT-S International Microwave Symposium (IMS). IEEE, 2021, pp. 112– 115.

[52] M. R. Zunaidi, A. Sayakkara, and M. Scanlon, “Revealing iot cryptographic settings through electromag netic side-channel analysis,” Electronics, vol. 13, no. 8, p. 1579, 2024.

[53] P. Cao, C. Zhang, X. J. Lu et al., “Side-channel analy sis for the re-keying protocol of bluetooth low energy,”

JOURNAL OF COMPUTER SCIENCE AND TECH-NOLOGY, vol. 38, no. 5, pp. 1132–1148, 2023.

[54] H. Liu, R. Spolaor, F. Turrin, R. Bonafede, and M. Conti, “Usb powered devices: A survey of side-channel threats and countermeasures,” High-Confidence Computing, vol. 1, no. 1, p. 100007, 2021.

[55] C. Morales-Gonzalez, M. Harper, M. Cash, L. Luo, Z. Ling, Q. Z. Sun, and X. Fu, “On building automation system security,” High-Confidence Computing, vol. 4, no. 3, p. 100236, 2024.

[56] R. J. Masti, D. Rai, A. Ranganathan, C. Müller, L. Thiele, and S. Capkun, “Thermal covert channels on multicore platforms,” in 24th USENIX Security Symposium (USENIX Security 15), 2015, pp. 865–880.

[57] M. Guri, B. Zadov, and Y. Elovici, “Led-it-go: Leaking (a lot of) data from air-gapped computers via the (small) hard drive led,” in International conference on detection of intrusions and malware, and vulnerability assessment. Springer, 2017, pp. 161–184.

[58] R. Spolaor, Y. Xu, V. Moonsamy, M. Conti, and X. Cheng, “Covertpower: A covert channel on android devices through usb power line,” IEEE Transactions on Dependable and Secure Computing, no. 01, pp. 1–16, 2025.
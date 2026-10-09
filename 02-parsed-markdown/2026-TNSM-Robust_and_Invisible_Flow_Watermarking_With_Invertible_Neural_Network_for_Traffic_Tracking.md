# Robust and Invisible Flow Watermarking With Invertible Neural Network for Traffic Tracking

Yali Yuan , Ruolin Ma , Jian Ge , and Guang Cheng , Member, IEEE

Abstract—This paper introduces an innovative blind flow watermarking framework on the basis of Invertible Neural Network (INN) called IFW, which aims to solve the problem of suboptimal encoder-decoder coupling in existing end-to-end watermarking architectures. The framework tightly couples the encoder and decoder to achieve highly consistent feature mapping using the same parameters, thus effectively avoiding redundant feature embedding. In addition, this paper adopts the INN to implement watermarking, which supports forward encoding and backward decoding, and the watermark extraction is completely dependent on the embedding algorithm without the need for the original network flow. This feature enables both the embedding and the blind extraction of watermarks simultaneously. Extensive experiments demonstrate that the proposed IFW method achieves a watermark extraction accuracy exceeding 96.6% and maintains a stable K-S test p-value above 0.85 in both simulated and realworld Tor traffic environments. These results indicate a clear advantage over mainstream baselines, highlighting the method’s ability to jointly ensure robustness and invisibility, as well as its strong potential for real-world deployment.

Index Terms—Flow watermarking, inter-packet delay, INN, invisibility, robustness.

## I. INTRODUCTION

position in the modern digital age. Network flow links are streams of data transmitted over a network, which may contain sensitive information, user credentials, business data, and other important content. If a network flow link is not secure, this data can be easily stolen, modified, or misused by malicious attackers. In addition, for organizations, attacks may disrupt operations and cause economic loss. For users, they may result in privacy breaches and reduced trust. Therefore, securing network flow links holds particular significance.

Network flow links face growing security threats. Unprotected flows may leak sensitive data, leading to identity theft, financial loss, or IP exposure. They can also carry malware or serve as vectors for DoS/DDoS attacks, disrupting services by overwhelming resources. Additionally, man-in-themiddle attacks may intercept or tamper with traffic.

As key channels for data exchange, flow links are frequent attack targets. Yet, most existing defenses are reactive, and modern intrusion detection systems still struggle to trace attack sources effectively. In practice, attackers rarely operate directly from their own devices. Instead, they use chains of intermediate nodes or anonymous communication systems to conceal their identities before launching attacks, making it extremely difficult to trace the origin of malicious flows [1], [2], [3], [4]. This challenge has shifted the research focus toward identifying the original source of online activities.

To tackle this issue, defenders need to associate incoming and outgoing traffic patterns to trace intrusions back to their source. Analyzing such patterns within anonymous communication systems like Tor can also be used to compromise anonymity. However, traditional correlation techniques that rely on packet content become ineffective due to the widespread encryption of modern network traffic.

After that, traffic correlation techniques mainly use methods based on flow characteristics, which is widely known as traffic analysis. Work on traffic analysis falls into two categories. Some work focuses on passive traffic analysis [1], [2], [3], [8], [9], [10], [11], [12], [13], which requires relatively long flows for good results. Passive traffic analysis methods collect network flows from nodes at key locations in the network and use features such as the number [3], size [12], and timing [2], [14] of packets in different network flows to identify correlation-matching relationships between network flows. However, this approach requires capturing and examining all network flows, significantly increasing network device space-time overhead. In addition, offline analysis methods lead to delayed identification, poor real-time performance, and insufficient scalability, which limits their application in largescale and high-bandwidth network environments, especially when dealing with encrypted flows and anonymous communications [15], [16], [17], [18], [19].

In contrast, active network flow watermarking techniques [21], [22], [23], [24], [25], [26], [27], [28], [29], [30], [31] establish flow correlations by actively embedding identifiable markers, offering a novel approach for tracking in encrypted environments. However, existing methods still face three major challenges: (1) Watermark extraction often relies on access to the original traffic, making blind extraction difficult [18], [21], [22], [23], [24], [25], [26]; (2) Discrepancies between the encoder and decoder limit the accuracy of watermark recovery [24], [27], [30]; (3) The invisibility of embedded watermarks may interfere with normal user activities [21], [29], and in some cases, even lead to information leakage [20]. Therefore, there remains a research gap in the current literature regarding end-to-end blind watermarking frameworks that simultaneously ensure robustness and invisibility, as well as the design of highly consistent encoder– decoder architectures.

To address these challenges, this paper aims to propose a blind watermarking framework that balances robustness and invisibility. The specific objectives are as follows: (1) to design an end-to-end architecture based on INNs that unifies the watermark embedding and extraction processes, thereby overcoming the insufficient coupling between encoder and decoder in existing methods; (2) to enable blind extraction without access to the original traffic, enhancing system deployment flexibility; (3) to introduce adaptive strength control and statistical invisibility constraints, so as to improve watermark invisibility without compromising robustness.

Based on the above goals, we propose the IFW framework, which is designed to fill the aforementioned research gap. The core innovation of this work lies in introducing the INN into the domain of network flow watermarking. At its core is an invertible up-down sampling block that supports both watermark embedding and extraction via mathematically reversible mappings. Unlike traditional encoder-decoder designs, this symmetric architecture offers three main advantages: (1) By constructing a closed-loop consistency between encoding and decoding, it eliminates the feature bias caused by separated modules in traditional methods. Experiments demonstrate that this design achieves higher extraction accuracy and lower bit error rate compared to baseline approaches; (2) Due to the mathematical properties of invertible transformations, the decoding process does not require access to the original traffic, thus enabling true blind extraction; (3) INN implicitly learns fine-grained perturbation patterns within traffic features. Compared to manually designed explicit modification rules, the watermarks generated by IFW exhibit superior imperceptibility. As a result, IFW effectively evades detection and minimizes interference with benign flows. We evaluate its invisibility using the Kolmogorov–Smirnov test, where the resulting p-values under the same conditions are higher than those of the best-performing baseline methods.

In summary, the key contributions presented in this paper are as follows:

1) Aiming to overcome the limitations of suboptimal encoder-decoder coupling in existing end-to-end watermarking-based architectures, a neural network-based flow watermarking framework, IFW, is developed. The same parameters are used for encoding and decoding to ensure that the encoders and decoders are tightly coupled. As a result, the encoded features can be highly consistent with those required by the decoder, effectively avoiding the embedding of redundant features.

2) Applying INN to network flow watermarking, it can be used for both forward encoding and backward decoding. Besides, watermark extraction is completely dependent on the embedded watermark algorithm, which does not require the original flow information.

Therefore, embedding and blind extraction can be achieved simultaneously.

3) The experimental results show that compared to prior approaches for flow watermarking, the method proposed in this paper maintains invisibility while ensuring watermark robustness.

The remainder of the paper is structured as follows. Section II presents a review of the background to traffic analysis. Section III illustrates the attack scenario of the proposed method. Section IV describes the components of IFW. Section V evaluates the performance of IFW through simulation experiments and discusses its invisibility in Section VI. Section VII concludes the main points. Section VIII discusses the limitations of the approach and outlines future work directions.

## II. RELATED WORK

Traffic correlation techniques are generally divided into passive and active approaches. Passive methods rely on observing and linking traffic patterns but often require raw data, long sessions, and high resource costs, making them unsuitable for short or sparse flows. Active methods, such as network flow watermarking, overcome these limitations by embedding hidden signals into traffic, enabling more efficient and accurate correlation with lower overhead. Watermarkingbased correlation improves precision, reduces false positives, accelerates detection, and needs fewer packets.

Depending on the carrier used, watermarking techniques are typically classified into payload-based, rate-based, and timingbased methods.

## A. Packet Payload-Based Flow Watermarking Technologies

Techniques that exploit packet content as carriers adjust application load within traffic streams to insert digital marks, thereby enabling flow correlation. Wang et al. [21] introduced sleepy watermark tracing (SWT), a proactive intrusion response method. SWT is triggered only upon detecting an attack, embedding various character sequences into the attacker’s response channel while coordinating with routers along the attack route to pinpoint its origin. However, this approach is tailored for specific application-layer protocols, limiting its adaptability to cryptographic protocols where adversaries can quickly identify and block such marks.

## B. Flow Rate-Based Flow Watermarking Technologies

Techniques that exploit flow rate for watermarking insert digital marks and trace data flows by altering their transmission rates. Huang et al. [22] and Pan et al. [23] introduced a DSSS watermarking approach that employs extended pseudonoise sequences. In this method, individual watermark bits are encoded using segments of the sequence, and utilizing a multitude of these sequences enables traceability across multiple streams while preventing mutual interference.

## C. Packet Timing-Based Flow Watermarking Technologies

1) IPD-Based Flow Watermarking Technologies: Inter-Packet Delay (IPD) watermarking techniques embed digital marks by manipulating packet timing within a traffic stream to enable flow correlation. Houmansadr et al. [24] introduced probabilistic IPD-based watermarking methods that are resilient to random timing noise. Houmansadr et al. [25] proposed RAINBOW, a watermarking scheme that significantly reduces insertion delay while enhancing invisibility compared to earlier blind watermarking methods. Later, Houmansadr and Borisov [26] improved detection performance by using repeated cumulative codes. Additionally, Rezaei and Houmansadr [30] presented FINN, a lightweight neural network-based approach for network flow fingerprinting, showcasing the effectiveness of end-to-end deep learning models in traffic classification and laying the groundwork for future learning-based flow correlation techniques.

2) Interval-Based Flow Watermarking Technologies: Interval-based watermarking methods achieve data marking by dividing the target flow into segments of fixed duration and regulating the number of messages per segment through timing adjustments. Houmansadr and Borisov [27] designed the first practical use of large-scale flow analysis for watermarking SWIRL. Since SWIRL causes only minor delays that neither users nor attackers can detect, it offers a invisible, scalable solution that withstands packet loss. Wang et al. [28] suggested a new detection model called SWDM that supports 3 sequence detectors to efficiently track malicious traffic.

3) Interval Centroid-Based Flow Watermarking Technologies: The interval centroid represents the balanced distribution of packets over a time segment and can be adjusted to enable effective flow correlation. To address traffic pattern variability, Wang et al. [18] proposed the ICBW method, which embeds unique signatures into long flows via interval centroids. ICBW is robust against cover traffic, flow mixing/splitting, packet loss, and timing distortions. Lin et al. [29] later introduced NFWM-CMIG, a covert watermarking scheme that modifies packet timing based on the center-of-mass of inter-packet delays, using a secret key. Packet count-based watermarking offers strong anti-jamming capability and broad protocol compatibility, but remains vulnerable to attacks such as multi-flow analysis and timing inference.

In summary, existing network flow watermarking methods can be broadly categorized into explicit embedding approaches based on feature perturbation and end-to-end schemes based on deep models. The former typically rely on fixed timing or interval perturbation strategies for watermark embedding, which are easy to implement but suffer from limited robustness and invisibility under adversarial conditions. The latter introduce encoder–decoder architectures for training and optimizing watermark embeddings, enhancing adaptability and performance. However, they commonly face two major limitations: (1) the decoder often depends on access to the original traffic or auxiliary data, making blind extraction infeasible; and (2) structural inconsistency between the encoder and decoder can lead to cumulative errors and instability in watermark retrieval.

In contrast, the proposed IFW framework incorporates invertible neural networks (INNs) into flow watermarking design, achieving structural symmetry and parameter sharing between the encoding and decoding paths. This architecture supports fully blind extraction without requiring original flows, while balancing robustness and statistical invisibility. These features make IFW not only more resilient but also more practical and adaptable for real-world deployment.

![](images/55f37006710d692fd3efd37683106f4c2db1ba5b744cd582201b928279d0aec3.jpg)  
Fig. 1. The main settings of the watermarking attack on Tor for traffic tracking.

## III. ATTACK SCENARIO

Anonymous communication networks aim to safeguard user privacy by preventing the monitoring, tracking, or leakage of personal information, location, and communication content. With the growing sophistication of such technologies, the Tor network has seen substantial expansion in both scale and user adoption. Tor enables anonymity through multilayer encryption and multi-hop routing, commonly using either three-hop or six-hop paths. In the standard three-hop setup, traffic passes through an entry node, a relay, and an exit node—each responsible for decrypting one encryption layer, with only the exit node knowing the destination. The six-hop configuration introduces more nodes to strengthen anonymity, while retaining the same underlying mechanism. Data is transmitted securely between onion routing nodes using the TLS protocol.

Over time, the Tor network has enhanced its defenses against traffic analysis and traceback attacks through multiple countermeasures. Since version 0.3.1.7, clients and relays periodically send CELL\_PADDING cells (every 1.5–9.5 seconds) to mask real traffic timing. Tor also adopts multi-path circuit switching with path rotation every 10 minutes, along with EWMA-based scheduling and dynamic window management for adaptive rate control. These techniques obscure interpacket timing. Additionally, Tor introduces Poisson-distributed cover traffic at exit nodes via a token bucket algorithm, further hindering flow modeling by attackers.

This paper considers an attack in which a user accesses a Tor hidden service (HS) while an attacker aims to identify the communication relationship. The attacker controls some Tor infrastructure, embedding a watermark at the entry node and detecting it before traffic reaches the HS. Despite encryption at intermediate nodes, compromising two key relays enables flow correlation and deanonymization. As shown in Fig. 1, the Tor circuit includes six nodes. The HS publishes three introduction points (IPOs) to the hidden service directory. When a user (via onion proxy, OP) connects, they retrieve IPO or public key data and designate a rendezvous point (RPO). The OP and HS independently build circuits to the RPO, forming the complete six-hop path for anonymous communication.

![](images/5e8d1a451ebb1e4a867ed4cd90fd6639d01982fea0f290aeda4730fc40f917e4.jpg)  
Fig. 2. The overall architecture of IFW system. The internal structure of INN blocks is illustrated in Fig. 3.

## IV. PROPOSED FRAMEWORK

This work primarily aims to design a robust watermarking framework based on INN [39], [40], as illustrated in Fig. 2. The primary element of the framework is a neural network-based Encoder/Decoder consisting of several Invertible Neural Blocks (INBs). Due to the invertible structure of the encoder/decoder, it can achieve forward encoding and backward decoding with the same parameters.

## A. Encoder/Decoder Based on Invertible Neural Network

Normalized INN-based models can compute likelihood directly and are widely used in generative tasks. INN-based models can efficiently implement forward and inverse mappings with the same network and parameters, as well as full coupling of encoder and decoder. Thus, the invertibility of INN is well suited for normalized mapping and, of course, for robust watermarking. Previous studies demonstrated the powerful generative capabilities of INN-based models.

The encoder and decoder in IFW correspond to the forward and backward propagation paths of the INN, respectively. Their structures are completely symmetrical, and all module parameters are fully shared. Specifically, each INN block within the encoder consists of multiple coupling structures, and its internal subnetworks (such as the transformation functions $\rho ( \cdot )$ , η( ), φ( )) are used to compute transformation parameters of the feature maps. In the decoder, no separate inverse network is constructed. Instead, the model directly reuses the parameters from the forward process, and decoding is performed through the mathematical inversion enabled by the intrinsic reversibility of INNs. As a result, both the forward embedding and backward extraction processes share exactly the same architecture and weights. Parameter sharing is not only a fundamental property of INNs but also the key to ensuring consistent embedding and extraction in IFW.

![](images/02cb9fb817fdea665111a973a113e5759b0f7c0c308114e5ae9f884d95056962.jpg)  
Fig. 3. Detailed presentation of the $\it { i } ^ { t h }$ INB.

Fig. 3 illustrates the structure of the $i ^ { t h }$ INB, and Algorithm 1 shows more specific implementation details. We can see that each chunk is composed of an upstream subnetwork $\phi _ { i }$ and two downstream subnetworks $\rho _ { i }$ and $\eta _ { i } .$ . The role of $\phi _ { i }$ is to increase the watermark W to the same size as the network flow T. while $\rho _ { i }$ and $\eta _ { i }$ are to downsample $x _ { i + 1 }$ to the same size as $w _ { i }$ . Therefore, for the $i ^ { t h }$ INB in the forward coding process with inputs $w _ { i }$ and $x _ { i }$ , the outputs $w _ { i + 1 }$ and $x _ { i + 1 }$ can be formulated as follows:

$$
x _ {i + 1} = x _ {i} + \phi_ {i} (w _ {i}),\tag{1}
$$

$$
w _ {i + 1} = w _ {i} \odot \exp (\rho_ {i} (x _ {i + 1})) + \eta_ {i} (x _ {i + 1}),\tag{2}
$$

where $\odot$ denotes the dot product operation. After the last INB processing, the final outputs $w _ { n + 1 }$ and $x _ { n + 1 }$ are available. i.e., the redundant information R and the IPD(S) with watermark.

For the reverse decoding process, the flow moves from the $i + 1 ^ { t h }$ INB to the $i ^ { t h }$ INB, as shown in Fig. 3. Specifically, for the first INB, the inputs are the all-zero matrix M generated by the noise layer and the network flow NW after being disturbed by the noise, and the outputs of the first last INB in the reverse decoding are $z _ { n }$ and $x _ { n } ^ { \prime }$ . For the $i ^ { t h }$ INB, the inputs are $z _ { i + 1 }$ and $x _ { i + 1 } ^ { \prime }$ and the outputs are $z _ { i }$ and $x _ { i } ^ { \prime } .$ . This can be calculated using the following equation:

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: INB Architecture
Input : Input pair $(x_1, x_2)$, reverse flag rev
Output: Transformed pair $(y_1, y_2)$
1 Function ED $((x_1, x_2), rev)$
2    W, b ← ProjectionMatrix();
3    $\mathcal{N}_s, \mathcal{N}_t, \mathcal{N}_c \leftarrow \text{SubNetworks}()$;
4    if not rev then
5    $(x_a, x_b) \leftarrow split(x_1), s \leftarrow \mathcal{N}_s(x_2), t \leftarrow \mathcal{N}_t(x_2)$;
6    $y_a \leftarrow x_a \odot exp(s) + t \ y_b \leftarrow x_b + \mathcal{N}_c(y_a \oplus x_2)$;
7    $(y_1^{pre}, y_2^{pre}) \leftarrow shuffle(y_a, y_b, x_2)$;
8    $(y_1, y_2) \leftarrow W[y_1^{pre}; y_2^{pre}] + b$;
9    else
10    $(y_1^{pre}, y_2^{pre}) \leftarrow W^{-1}([y_1; y_2] - b)$;
11    $(y_a, y_b, x_2) \leftarrow inv\_shuffle(y_1^{pre}, y_2^{pre})$;
12    $x_b \leftarrow y_b - \mathcal{N}_c(y_a \oplus x_2); s \leftarrow \mathcal{N}_s(x_2)$;
13    $x_a \leftarrow (y_a - t) \odot \exp(-s)$;
14    $(y_1, y_2) \leftarrow concat(x_a, x_b), x_2$;
15    Return $(y_1, y_2)$
</div>

$$
z _ {i} = \big (z _ {i + 1} - \eta_ {i} \big (x _ {i + 1} ^ {\prime} \big) \big) \odot e x p \big (- \rho_ {i} \big (x _ {i + 1} ^ {\prime} \big) \big),\tag{3}
$$

$$
x _ {i} ^ {\prime} = x _ {i + 1} ^ {\prime} - \phi_ {i} (z _ {i}).\tag{4}
$$

## B. Network Noise

Network noise is one of the inevitable factors influencing watermarks in real-world applications. Due to network jitter causing delays in data packets, the watermark information added to the flow may also be lost or removed in the network jitter affecting the flow. Therefore, it is necessary to incorporate such considerations into the proposed scheme to evaluate its robustness. It is known that network jitter may follow a Laplacian distribution [21], [22], a multimodal distribution, or a heavy-tailed distribution. Accordingly, in the proposed framework, we simulate network perturbations by generating noise based on these three types of distributions, which facilitates subsequent evaluation of the robustness of our method.

## C. Loss Functions

RFW sets up two types of loss functions: watermark loss and IPD loss, which together form the total loss function. The watermark loss ensures the robustness of the embedded information, while the IPD loss ensures the invisibility of the network flow. Moreover, since we focus only on the performance related to watermark embedding and extraction, IFW does not set any restrictions regarding the redundant information R and the recovered IPD(T-). Obviously, these two results are not important in the whole process of watermarking.

1) IPD Loss: Forward propagation as an encoder, the IFW has to embed the watermark W into T to generate a watermarked IPD S. To achieve invisibility, the flow with embedded watermark information should closely mimic the host flow. Accordingly, the flow loss $\mathcal { L } _ { i p d }$ is defined as follows:

$$
\mathcal {L} _ {i p d} (\theta) = \mathbb {E} _ {t \sim T} \Big [ \| f _ {\theta} (t, W) - t \| _ {2} ^ {2} \Big ],\tag{5}
$$

where t denotes a time interval sample sampled from the original IPD traffic sequence T, and $f _ { \theta } ( \cdot )$ represents the forward mapping of the IFW encoder under parameter θ, whose output is the watermarked IPD sequence S.

2) Watermark Loss: When backward propagation is used as a decoder, the goal of IFW is to extract the watermark without loss from the jammed network stream. For this purpose, we define the watermark loss $\mathcal { L } _ { w m }$ as follows:

$$
\mathcal {L} _ {w m} (\theta) = \frac {1}{| W |} \sum_ {j = 1} ^ {| W |} \left(f _ {\theta} ^ {- 1} (N W, R) _ {j} - W _ {j}\right) ^ {2},\tag{6}
$$

where $\mid W \mid$ denotes the length of the watermark sequence, and $f _ { \theta } ^ { - 1 } ( \cdot )$ represents the inverse decoding process of IFW, taking as input the network flow NW after noise or interference and the auxiliary matrix R.

3) Total Loss: The total loss function $\mathcal { L } _ { t o t a l }$ is the weighted sum of watermark loss $L _ { w m }$ , IPD loss $L _ { i p d } .$ , defined as shown below:

$$
\mathcal {L} _ {t o t a l} = \lambda \mathcal {L} _ {w m} (\theta) + (1 - \lambda) \mathcal {L} _ {i p d} (\theta).\tag{7}
$$

Here, $\lambda ~ \in ~ ( 0 , 1 )$ is the weighting coefficient for the robustness objective, while the weight of the invisibility term is automatically determined by the complementary relationship. They jointly balance robustness and invisibility in watermark embedding: increasing λ favors watermark recoverability under noise or attacks, while increasing (1 λ) more strongly constrains perturbations to the original traffic.

## D. Practical Application

In practical Tor network tracking scenarios, law enforcers often attempt to identify or trace the anonymous communication traffic of criminals to undermine their privacy protection mechanisms. Utilizing the IFW framework, watermarking can be embedded into Tor traffic without significantly altering the external characteristics of the traffic. Since IFW employs INN for watermark embedding and extraction, this ensures that the embedding not only maintains a high level of invisibility but also allows for blind extraction in subsequent traffic. Therefore, when facing traffic analysis attacks, it is challenging to detect its presence even if attackers attempt to identify the watermark. Moreover, IFW’s robustness ensures that, even in imperfect environments subject to various noise and interference, the watermark can effectively maintain its invisibility and be successfully extracted. Thus, IFW can effectively enhance the stability of tracing, resist traffic analysis attacks, improve the attack resistance of darknet traceability, and provide a valuable solution for similar anonymous communication scenarios, such as VPNs or privacy-protecting instant messaging systems. Additionally, IFW’s invisibility and robustness make it widely applicable in other secure communication environments. For example, in corporate internal networks, IFW can be used to monitor and prevent data leakage. By embedding watermarks into sensitive flows, companies can track the flow, promptly detect abnormal behavior, and prevent the leakage of sensitive information.

## V. EXPERIMENTAL RESULTS

## A. Dataset

1) IPD: In this study, a traffic collection environment was set up to obtain actual traffic data in the real world. Two servers running Ubuntu 20.04 on AliCloud with Tor software version 0.4.2.7 were used, one located in Hong Kong and acting as a client, and the other located in Singapore and acting as a hidden server. The clients access the hidden server through six Tor relays in the real world and generate traffic by uploading a random byte file of 3MB in size. In total, they were divided into two groups of 500 uploads each to obtain the dataset, i.e., the timestamps of the packets. Due to Tor’s automatic circuit switching, the data we collected did not always go through the same circuit. By leveraging IP addresses and protocol information, distinct destination streams can be identified, and the corresponding timestamps can be extracted. We then use the timestamps to calculate the IPD data needed for the experiment.

To enhance dataset diversity and validate the scalability of our proposed scheme, we constructed an extended test environment using the NS2 network simulator [33]. This environment simulates a 6-hop Tor network topology consisting of 5 clients and 5 servers. By systematically adjusting network parameters, we collected data under the following three representative network scenarios: (1) a baseline scenario (2 Mbps bandwidth, 300 ms latency), (2) a high-latency, lowbandwidth scenario (2 Mbps bandwidth, 800 ms latency), and (3) a high-bandwidth, low-latency scenario (20 Mbps bandwidth, 300 ms latency). At the topology implementation level, we defined duplex-link parameters between nodes using NS2’s OTcl scripts, applied the DropTail queuing model for traffic control, and introduced random delay perturbations ( 5 ms) to simulate realistic network jitter [34], [35].

For each scenario, we simulated approximately 2,000 flow timestamp sequences, covering a continuous distribution from short flows (<100 packets) to long flows (>500 packets). This layered design allows the dataset to capture traffic feature variations under different network transmission qualities, path diversity across multiple topology structures, and the statistical characteristics of multi-scale traffic patterns. By comparing data collected from real-world and simulated environments, we are able to effectively isolate inherent network noise from the embedded watermark features, thereby validating the robustness of our scheme under complex network conditions.

2) Watermark: The watermark is one of the data entered into the IFW and is the identifying information we use to correlate flows. In general, it can be considered to choose binary or One-hot encoding to represent the watermark. The scheme in this paper uses One-hot encoding to construct the watermark dataset. A One-hot set has a total of H bits, where there is only one 1 and the rest of the bits are all 0. For example, we want to embed 2 bits of information in each flow. Using binary representation, the watermark could be 01, 00, 11, 10. But for One-hot representation, there are the following Onehot encoding options to represent the watermark information: 0001, 0010, 0100, 1000. That means, if the watermark length is H, we can embed log H bits of information in each flow. Taking One-hot encoding as an example, when H=4, we can embed $\log _ { 2 } 4 ~ = ~ 2$ bits of information in each flow. This method utilizes a single encoding scheme to efficiently and discreetly embed information, ensuring the robustness and invisibility of the watermark within the network flow. The performance of IFW is better when the data is represented by One-hot. Therefore, the second format is chosen to represent the watermark in this paper.

## B. Evaluation Metrics

True Positive Rate (TPR): Defined as the fraction of correctly identified watermarks relative to all extracted ones, TPR reflects the model’s effectiveness—an increased TPR signifies an enhanced ability to correctly recognize genuine cases.

False Positive Rate (FPR): Calculated by comparing the count of incorrect watermark identifications to the total extracted, FPR measures the tendency of the model to erroneously mark negative samples as positive. A reduced FPR denotes improved handling of negative examples.

Bit Error Rate (BER): The bit error rate reflects inaccuracies in each incorrectly extracted watermark. To compute it, each watermark is translated into binary format, allowing us to measure how many bits were altered by network-induced noise.

## C. Robustness Measurement

1) Effect of Different Flow Lengths: The flow length f is one of the most important parameters influencing IFW performance, and we aim to identify an ‘optimal’ f for subsequent evaluations. Increasing flow length enlarges the watermark’s embeddable positions, improves invisibility, and thereby enhances model performance—a trend also supported by our experiments. With a watermark length of 50 and noise intensity of 0.1, the results in Figs. 4 and 5 show that as f grows, TPR gradually increases while FPR and BER gradually decrease.

2) Effect of Different Watermark Lengths: The watermark length l is also a major parameter of IFW, and we conduct experiments to assess how this parameter influences overall performance. To make the results more comparable, we fix the other parameters except l. The size of r is continuously increased until the TPR decreases significantly. Figs. 6 and 7 show the performance of the method presented in this work when the noise intensity ϑ <sub>=</sub> 0.1 for l values of 10, 20, 30, 50, and 70 (f 50), respectively. It is obvious that the FPR and BER increase with the length of the watermark, when the TPR decreases from 100% at l <sub>=</sub> 10 to 98.74% at l <sub>=</sub> 70.

![](images/50cab24aee25f68a8e55be8e6983d0ec42f3a51f8ce871cec96aec86d24548ee.jpg)

Fig. 4. Results of TPR/FPR variation with flow length f.  
![](images/d82cbfef1f82de1f2e254b57308ff025da8e73f486f29ebd8504bc17830f8b00.jpg)  
Fig. 5. Results of BER variation with flow length f.

![](images/481ef686a5a7051816e7f9252af7cabe95f2905d499a914b5ee85c147a17ed35.jpg)  
Fig. 6. Results of TPR/FPR variation with watermark length l.

However, it is undeniable that the model in this paper still maintains high TPR and low BER performance at this stage.

To increase per-flow watermark capacity, we explore more compact encoding schemes. Without modifying the IFW architecture, compressed label encodings such as binary or Gray code is introduced to replace the original one-hot vectors with shorter sparse integer codes, thereby increasing the information payload per flow to $\log _ { 2 } n$ bits.

Experimental results show that using binary encoding causes minimal performance degradation, with variations in TPR and BER remaining within 3%, and the K-S test p-value consistently above 0.85. This indicates that the compact encoding significantly improves capacity without noticeably increasing detectability. Moreover, IFW demonstrates strong adaptability to different encoding strategies, and future work may incorporate learnable embedding mechanisms to further enhance the watermarking capability.

![](images/9b3043f8a4c50bcea7d21e624473df412de21733d0d6193ec8982efecdbbf549.jpg)  
Fig. 7. Results of BER variation with watermark length l.

![](images/cb0507fcf359cfe9145fe9818404bb27089f2702ad375cae0e40bd5eca3e77bb.jpg)  
Fig. 8. Results of TPR/FPR variation with noise intensity ϑ.

3) Impact of Different Levels of Noise: The noise intensity ϑ in the network flow is another factor affecting IFW performance. We treat ϑ as a variable and, using a singlevariable setup, fix other parameters (f=50, l=100) to observe how TPR, FPR, and BER vary with ϑ. Fig. 8 shows that the TPR of extracted watermarks when ϑ<sub>=</sub>0.1, 0.12, 0.14, 0.16, 0.18 is 99.26%, 97.59%, 96.30%, 95.15%, 94.92%. And Fig. 9 similarly shows that the BER is 0.38%, 1.18%, 1.84%, 2.39%, and 2.55% at this time, respectively. Obviously, as ϑ increases, the TPR of the watermark shows a downward trend, while the FPR and BER exhibit an upward trend.

## D. Coupling Measurement

Based on the previous section, END architectures for current applications face a potential limitation that the desired tight coupling between the encoder and decoder may not be achieved. However, to address this challenge, the IFW architecture proposed in this paper cleverly solves the problem, where INN ensures an effective and tight synergy between the encoder and decoder. This section will verify that the coupling of IFW with an integrated encoder-decoder design is superior to other existing works.

![](images/e8c794d4701fd5b4a07f870fd327f6e68604fe492eec891cd545ba494bc5c272.jpg)  
Fig. 9. Results of BER variation with noise intensity ϑ.

Evaluating the coupling of the encoder and decoder is a relatively complex process. This is because coupling is usually not a directly measured parameter in neural networks, but is indirectly assessed by observing the interaction and behavior of the encoder and decoder during data transmission.

Reconstruction Error (RE) is an important metric for evaluating the performance of a self-encoder. For a given input data, the encoder converts it into a coded representation and then the decoder attempts to reconstruct the original input from that coded representation. By calculating the reconstruction error (e.g., mean square error, cross-entropy, etc.), the coupling between the encoder and decoder can be evaluated. We use the MSE loss of the extracted watermark and the original watermark information to represent the reconstruction error. As shown in Table I, the MSE loss for IFW is 0.0009, while the MSE loss for diffident Encoder/Decoder is 0.4314. A lower reconstruction error usually implies a better coupling between the encoder and decoder.

Normalizing features is an important step in neural networks, especially when using the END architecture. It helps to speed up training, improve model performance, and prevent problems such as vanishing or exploding gradients. The normalized features embedded by the encoder and those needed by the decoder should theoretically be consistent since they deal with the representation of the same type of data at different stages.

We test the coupling by comparing whether the encoderembedded normalization feature E and the decoder-required normalization feature D exhibit the same properties. We use Euclidean Distance (ED), Manhattan Distance (MD), Chebyshev Distance (CD), and Mean Squared Error (MSE) to measure the similarity between E and D when RFW and the Encoder/Decoder are not the same. The results, as shown in Table I, show that the similarity between E and D in IFW is much higher than the similarity between E and D when the Encoder/Decoder is different, regardless of the method. This may be because the encoder and decoder have the same structure, which effectively avoids the embedding of redundant features. As a result, the encoder and decoder in IFW are more tightly coupled.

TABLE I  
COUPLING COMPARISON IFW AND DIFFERENT ENCODERS/DECODERS

<table><tr><td>Method</td><td>RE</td><td>ED</td><td>MD</td><td>CD</td><td>MSE</td></tr><tr><td>Different E/D</td><td>0.4314</td><td>2.8148</td><td>6.3473</td><td>0.7667</td><td>0.7438</td></tr><tr><td>IFW</td><td>0.0009</td><td>0.0134</td><td>1.0118</td><td>0.0391</td><td>0.0059</td></tr></table>

TABLE II

RESULTS OF PERFORMANCE COMPARISON WITH EXISTING METHODS UNDER THE TOR COUNTERMEASURE

<table><tr><td>Method</td><td>Type</td><td>f</td><td>l</td><td>p</td><td>TPR</td><td>BER</td></tr><tr><td>FINN</td><td>Blind</td><td>150</td><td>80</td><td>0.514</td><td>87.35%</td><td>12.81%</td></tr><tr><td>SWIRL</td><td>Blind</td><td>150</td><td>/</td><td>0.378</td><td>56.84%</td><td>/</td></tr><tr><td>RAINBOW</td><td>Non-blind</td><td>150</td><td>80</td><td>0.452</td><td>65.80%</td><td>/</td></tr><tr><td>IFW</td><td>Blind</td><td>150</td><td>80</td><td>0.763</td><td>93.64%</td><td>6.58%</td></tr></table>

## E. Compare IFW With State-of-the-Arts

In this section, IFW will be compared with previous work on network flow watermarking. FINN [30] pioneered the application of deep learning techniques in flow fingerprinting. It generates a delayed sequence of fingerprints using deep learning, which makes it resemble a natural network jitter and enhances its invisibility. Compared to a fingerprint, a watermark simply carries fewer bits of information and is otherwise roughly the same. Therefore, the method can also be applied to running watermark recognition and the performance of FINN when used as a watermark is also evaluated in that paper. SWIRL and RAINBOW are also well known for their work on running watermarks, and even though they are not neural network-based methods, this does not prevent us from comparing them. In this paper, we would like to compare IFW with FINN, SWIRL, and RAINBOW on the same dataset and in the same experimental environment as shown in Table II.

As shown in Table II, Tor’s defenses significantly degrade the performance of traditional watermarking methods, but deep learning methods are able to provide some resistance. FINN’s 87.35% is inferior to IFW’s 93.64%, while SWIRL and RAINBOW reach only 56.84% and 65.80%, respectively. Notably, the detection algorithms in SWIRL and RAINBOW are designed solely to determine the presence of a watermark rather than to reconstruct the original watermark information, making it impossible to compute their BER. In contrast, IFW demonstrates a significantly stronger noise resilience, which can be attributed to our explicitly designed residual learning mechanism for modeling channel noise.

To comprehensively assess the strengths and limitations of IFW, we further categorized the noise intensity parameter ϑ to analyze each method’s recovery capability, robustness, and imperceptibility under varying noise conditions. As shown in Table III, the watermarks embedded by IFW consistently exhibit superior resilience and imperceptibility compared to state-of-the-art (SOTA) approaches across all noise levels. It is worth noting that although RAINBOW, as a non-blind watermarking method, is theoretically expected to outperform blind schemes due to access to side information, our experimental results indicate that IFW still surpasses it in practice. Despite non-blind schemes benefiting from an upper performance bound through information sharing, they often suffer from high deployment costs and inherent vulnerabilities to synchronization attacks. In contrast, IFW—being a blind watermarking approach—achieves comparable recognition performance while retaining deployment flexibility. This underscores the critical value of neural network-based feature learning in enhancing watermark robustness.

TABLE III  
RESULTS OF PERFORMANCE COMPARISON WITH EXISTING METHODS AT DIFFERENT NOISE INTENSITIES

<table><tr><td rowspan="2">Method</td><td colspan="2">Invisibility</td><td colspan="2"> $\vartheta=0.1$ </td><td colspan="2"> $\vartheta=0.13$ </td><td colspan="2"> $\vartheta=0.16$ </td></tr><tr><td>D</td><td>p</td><td>TPR</td><td>BER</td><td>TPR</td><td>BER</td><td>TPR</td><td>BER</td></tr><tr><td>FINN</td><td>0.104</td><td>0.957</td><td>98.71%</td><td>1.29%</td><td>96.55%</td><td>3.44%</td><td>93.78%</td><td>6.21%</td></tr><tr><td>SWIRL</td><td>0.078</td><td>0.981</td><td>98.01%</td><td>/</td><td>96.09%</td><td>/</td><td>92.13%</td><td>/</td></tr><tr><td>RAINBOW</td><td>0.120</td><td>0.869</td><td>93.80%</td><td>/</td><td>91.60%</td><td>/</td><td>88.58%</td><td>/</td></tr><tr><td>IFW</td><td>0.060</td><td>0.994</td><td>99.26%</td><td>0.38%</td><td>97.65%</td><td>2.35%</td><td>94.92%</td><td>5.08%</td></tr></table>

In addition, many other recent flow watermarking works such as Inflow [31] are non-blind watermarking recognition methods, and comparing them with ours is unfair. This is because non-blind flow watermarking techniques can access more information and naturally provide better performance for watermark recognition. Therefore, this paper does not compare them with IFW.

## F. Scalability Validation of IFW

This section validates the scalability of IFW under the following three scenarios: (1) a baseline scenario (2 Mbps, 300 ms), (2) a high-latency, low-bandwidth scenario (2 Mbps, 800 ms), and (3) a low-latency, high-bandwidth scenario (20 Mbps, 300 ms).

When faced with harsh network environments (e.g., high perturbation, high latency, or low bandwidth), increasing the strength of the watermark enhances the robustness of the watermark extraction. However, an excessively strong watermark may significantly interfere with the original network traffic, potentially causing increased packet processing delay and reduced throughput, while also resulting in modified traffic that statistically deviates from the original distribution, thereby compromising invisibility. Conversely, reducing the watermark strength diminishes the interference on network traffic, which is beneficial for maintaining network performance and the traffic’s stealth; however, in high-noise environments, the accuracy of watermark extraction may decrease. Therefore, in practical deployments, it is necessary to comprehensively balance the watermark embedding strength, network performance metrics, and imperceptibility according to the specific network conditions (e.g., bandwidth, latency) and application requirements. This balance can be achieved through the meticulous adjustment of hyperparameters.

To prevent enhanced robustness from compromising invisibility, this paper introduces an upper-bound mechanism for watermark embedding strength, ensuring that the invisibility remains above a predefined threshold. The K-S test is employed to evaluate statistical similarity, using the maximum distribution distance D and the corresponding p-value as metrics to constrain the embedding strength. Empirical results show that when the p-value exceeds 0.85, the embedded watermark is difficult to detect. Therefore, a safety threshold of $p = 0 . 8 5$ is selected, and the embedding strength $\omega _ { m a x }$ is defined as the maximum value before the p-value falls below this threshold. This constraint ensures that the watermarked traffic remains statistically indistinguishable from the original. In real-world deployment, when facing high-intensity noise or adversarial perturbations, the system may enhance watermark embedding to meet robustness requirements, but the embedding strength must not exceed ω<sub>max</sub>.

To address the issue of watermark parameter sensitivity in dynamic network environments, this work employs an environment-aware adaptive parameter tuning mechanism to balance the conflicts among watermark robustness, imperceptibility, and network performance. The loss function weights are dynamically adjusted by capturing network traffic characteristics (e.g., noise intensity, bandwidth volatility, sensitivity to anti-perturbation gradients). Specifically, this module maps the input features (including traffic temporal statistics, noise parameters, and estimated adversarial perturbation intensities) to an optimal combination of weights through a multi-layer perceptron (MLP), rather than relying on manually preset static parameters.

During the training phase, a meta-learning strategy is adopted to jointly optimize the parameters of the INN and the MLP, enabling the model to learn a generalized parameter adjustment strategy from various noise distributions and bandwidth fluctuation scenarios. At deployment, the parameter tuning module updates the weights in real time with extremely low computational overhead (approximately 5K FLOPs per inference), ensuring that λ is adaptively enhanced or attenuated according to the network noise level. For example, when a high-noise environment is detected, the module automatically increases the embedding strength to bolster watermark robustness; conversely, in low-noise scenarios, it reduces the embedding strength to prioritize the watermark’s imperceptibility.

TABLE IV  
RESULTS OF IFW SCALABILITY VALIDATION

<table><tr><td rowspan="2">Scenarios</td><td rowspan="2">Bandwidth</td><td rowspan="2">Latency</td><td colspan="3"> $\vartheta=0.1$ </td><td colspan="3"> $\vartheta=0.15$ </td><td colspan="3"> $\vartheta=0.2$ </td></tr><tr><td>TPR</td><td>BER</td><td>p</td><td>TPR</td><td>BER</td><td>p</td><td>TPR</td><td>BER</td><td>p</td></tr><tr><td>A</td><td>2Mb</td><td>300ms</td><td>99.24%</td><td>0.38%</td><td>0.927</td><td>98.78%</td><td>0.67%</td><td>0.911</td><td>97.06%</td><td>1.49%</td><td>0.895</td></tr><tr><td>B</td><td>2Mb</td><td>800ms</td><td>99.07%</td><td>0.57%</td><td>0.869</td><td>98.14%</td><td>0.96%</td><td>0.861</td><td>96.61%</td><td>1.68%</td><td>0.857</td></tr><tr><td>C</td><td>20Mb</td><td>300ms</td><td>99.89%</td><td>0.05%</td><td>0.992</td><td>99.43%</td><td>0.48%</td><td>0.986</td><td>98.74%</td><td>0.75%</td><td>0.979</td></tr></table>

Experiments demonstrate that under conditions of dynamic noise and bandwidth fluctuations, the adaptive tuning mechanism improves the watermark extraction success rate by 11.5%, significantly outperforming fixed-weight strategies. In addition, by incorporating adversarial perturbation sensitivity as an input feature, the tuning module effectively identifies malicious attack patterns (such as traffic shaping or delay injection) and dynamically adjusts the model’s robustness to adversarial examples. Future work will explore an end-to-end parameter tuning framework based on reinforcement learning, combining network state feedback in a closed-loop system to further enhance adaptive capability in complex adversarial environments.

To further enhance the practical usability of the model in dynamic network environments, this paper extends the original adaptive parameter tuning mechanism by introducing a range-threshold-based dynamic adjustment strategy. Specifically, for key network indicators, a tolerable fluctuation range ( ε) is predefined. When detected variations in network conditions remain within this range, IFW retains its current hyperparameter settings without re-training or re-tuning, thereby avoiding unnecessary computation and maintaining system stability. Only when network metrics exceed the threshold does a lightweight MLP module trigger a onetime parameter adjustment process. This strategy significantly reduces the frequency of model interventions and system resource consumption, improving IFW’s stability and deployment efficiency under frequently changing network conditions. Experimental results show that even in environments with high-frequency bandwidth jitter and latency fluctuations, IFW maintains stable watermark extraction performance with the proposed threshold-controlled adaptation mechanism: the TPR degradation remains within 1.2%, and the BER variation is controlled within 0.6%.

As shown in Table IV, as the noise intensity θ increases, the watermark embedded in the traffic is subjected to stronger noise interference, resulting in a decline in extraction accuracy. Consequently, a higher watermark strength is required to maintain a high TPR and low BER. Meanwhile, the variation in the p-value from the KS test reflects that increasing the watermark embedding strength amplifies the statistical discrepancy between the modified traffic distribution and that of the original traffic, thereby reducing the watermark’s imperceptibility. Notably, in scenarios with limited bandwidth and high latency (Scenario B), some challenges may arise regarding the stealth and extraction of the watermark. In contrast, in high-bandwidth, low-latency environments (Scenario C), IFW demonstrates high robustness.

## G. Complexity Analysis

1) Parameter Scale and Space Complexity: The IFW framework proposed in this paper is based on the symmetric design of the INN, and its parameter scale is jointly determined by the number of INBs, the channel dimension, and the linear transformation of the differential enhancement module. Suppose the number of INBs is N, and each block contains three convolutional submodules (f, r, y), with a fixed kernel size of $3 \times 3$ and a channel dimension of C. Then, the parameter count of a single block is on the order of ${ \mathrm { O } } ( 3 { \mathrm { C } } ^ { 2 } )$ , and the total parameter count is ${ \mathrm { O } } ( 3 \mathrm { N C } ^ { 2 } )$ . If the differential module is enabled, two fully connected layers are introduced, whose parameter count is $0 ( L _ { i n } \cdot L _ { o u t } )$ , where $L _ { i n }$ and $L _ { o u t }$ are the input and output feature dimensions, respectively. Thanks to the parameter sharing mechanism, the encoder and decoder are completely symmetric, which avoids the redundant parameter storage seen in traditional dual-branch architectures (for example, a conventional encoder-decoder typically requires O(2NC<sup>2</sup>) parameters), reducing the spatial complexity by approximately 50%. Furthermore, due to the invertible nature of the network, the reverse decoding process does not require storing intermediate activation values, further compressing the memory footprint during inference to O(NC<sup>2</sup>), which is significantly more efficient than conventional networks that necessitate caching intermediate states.

2) Time Complexity and FLOPs: The computational complexity of IFW is primarily concentrated in the affine coupling operations within the INB. Assuming the input traffic feature has dimensions H W, each INB’s f module comprises K layers of transposed convolution, with the FLOPs per layer on the order of ${ \mathrm { O } } ( { \mathrm { C } } ^ { 2 } { \mathrm { K } } ^ { 2 } { \mathrm { H W } } )$ . Similarly, the r and y modules each contain K layers of down-sampling convolution, with perlayer FLOPs also on the order of ${ \mathrm { O } } ( { \mathrm { C } } ^ { 2 } { \mathrm { K } } ^ { 2 } { \mathrm { H W } } )$ . Therefore, the FLOPs for a single INB are on the order of O(3KC<sup>2</sup>HW), and the overall model complexity is O(3NKC<sup>2</sup>HW). Under the experimental conditions (N=6, K=4, C=32, H=128, W=128), the per-sample inference FLOPs amount to approximately $1 . 6 3 \times 1 0 ^ { 9 }$ . Due to the bidirectional symmetry of the invertible structure, the encoder and decoder share the same computation graph, and the reverse decoding process only requires recomputation of activation values, thereby avoiding the extra overhead associated with an independent decoder in traditional methods.

Empirical results show that under a batch size of 32, the end-to-end average inference latency is 18.2 ms, corresponding to approximately 0.57 ms per sample. This meets the millisecond-level response requirements of most real-time traffic analysis systems. On a high-performance GPU, IFW achieves a single-thread throughput of up to 1750 flows per second, making it suitable for typical real-time network environments. However, in scenarios requiring sub-millisecond latency and extremely high throughput (e.g., core routers), further improvements in scalability may require lightweight architectural design and hardware acceleration optimizations.

The design significantly reduces the computational cost of hardware deployment by lightweight convolutional operation with parameter reuse strategy, while guaranteeing the watermarking performance.

## VI. INVISIBILITY MEASUREMENT

Invisibility is one of the key metrics for evaluating the effectiveness of watermark embedding. An effective watermarking scheme for network flows must remain invisible to avoid detection and removal by attackers, and to ensure it does not disrupt normal traffic. However, there is often a trade-off between the robustness and invisibility of the watermark [36], [37], [38]. On the one hand, to enhance the robustness of the watermark, more IPD values in the traffic often need to be altered, which might reduce the invisibility of the watermark and affect the normal use of network data. On the other hand, overemphasizing invisibility could weaken its robustness, making it more susceptible to damage when under attack. Due to the embedding of watermarks with a large magnitude in the flow, previous flow watermarking schemes do not have invisibility. Therefore, the following sections will conduct invisibility testing on the proposed scheme to examine whether it maintains good robustness while also possessing invisibility.

## A. Kolmogorov–Smirnov Similarity Test

The Kolmogorov–Smirnov (K-S) test is employed to assess whether two samples—whether as a pair of observations or a single observation compared to a reference sample— originate from the same distribution. This is achieved by evaluating the maximum difference between their cumulative distribution functions. Thus, given an empirical function F(x), the maximum gap D (i.e., the K-S statistic) is calculated as follows:

$$
D _ {n, m} = \sup _ {x} \left| F _ {1, n} (x) - F _ {1, m} (x) \right|,\tag{8}
$$

where sup denotes the difference that takes the largest value, and $F _ { 1 , n } ( x )$ and $F _ { 1 , m } ( x )$ denote the observed cumulative distribution functions derived from n observations in each stream. If

$$
D _ {n, m} > c (\alpha) \sqrt {\frac {n + m}{n m}}.\tag{9}
$$

The hypothesis asserting that the streams are drawn from the same distribution is dismissed at the α level. In this context, n and m represent the sample counts for each stream, and the value c(α) is determined by the following expression:

$$
c (\alpha) = \sqrt {- 0 . 5 l n \alpha}.\tag{10}
$$

In summary, the imperceptibility of the watermark can be verified by measuring the maximum distribution distance between two flows using the K-S test. When the D value approaches 0 (in our experiments, D=0.06) and the p-value is significantly greater than the 0.05 threshold (in our experiments, $\scriptstyle p = 0 . 9 9 4 )$ , it indicates that the watermarked traffic and the non-watermarked traffic are statistically indistinguishable. Specifically, a p-value of 0.994 implies that, at a 5% significance level, the probability of accepting the null hypothesis is nearly 20 times higher than what would be expected by chance (i.e., $p / \alpha = 0 . 9 9 4 / 0 . 0 5 \approx 1 9 . 8 8 )$ . This suggests that even if an attacker collects more than 1,000 traffic samples (as per the statistical power curve of the K-S test), there is still a 95% probability that statistical tests will fail to detect the presence of the watermark. This characteristic renders traffic watermarking detection methods based on statistical analysis ineffective in practical adversarial scenarios.

## B. Clustering

The clustering algorithm groups data so that samples in the same group are more similar than samples in other groups. We use clustering algorithms to see if watermarked and nonwatermarked samples can be clustered in two groups. We use the two main clustering algorithms in the Python Scikit-learn package: center-of-mass-based and density-based clustering.

For center-of-mass-based clustering, we use the K-Means algorithm. K-Means represents each cluster with a single mean vector. It has fast convergence and is suitable for large datasets. It works better when the clusters are dense and the clusters are clearly differentiated from each other. We use Principal Component Analysis (PCA) to reduce the dimensionality of the samples and represent them as two-dimensional. Fig. 10 illustrates the distribution of the actual watermarked and nonwatermarked flows, which overlap almost completely. It is obvious that the embedding of watermarks has almost no effect on the original flows. The clustering results of K-Means are shown in Fig. 11, and the clustering results differ greatly from the real classification results.

By calculating the Adjusted Rand Index (ARI 0) and the Normalized Mutual Information (NMI 0), we found that the clustering results are nearly equivalent to random classification (ideal value being 0). This indicates that the association between the clustering outcomes and the actual labels is no better than random assignment. Furthermore, after applying label alignment optimization (Aligned accuracy 50%), the classification accuracy is equivalent to random guessing (50%). This further demonstrates that even under the most ideal conditions (i.e., with a known number of clusters and optimal label alignment), an attacker cannot distinguish watermarked traffic from non-watermarked traffic using unsupervised learning methods.

![](images/01169e6e7dfc02821b179065b64b60fb0e9eb8eae612e70afaf0582c3cb3be35.jpg)  
Fig. 10. True distribution of watermarked and non-watermarked flow.

![](images/108e111d6f0b8a4ac4dbd7e36faac2a997bc4cea27c22e16ce7376f836b0a699.jpg)  
Fig. 11. K-Means clustering results for watermarked and non-watermarked flows.

DBSCAN is a clustering algorithm based on density that groups data points into contiguous areas of high density while treating sparse regions as noise [32]. This method can identify clusters of any shape. In our experiments, we use IPD measurements as feature vectors of length 100 and then apply Principal Component Analysis (PCA) to reduce these vectors to two dimensions. As shown in Fig. 12, the blue and orange dots are the real labels and the rest of the colors are the clustering results. DBSCAN divides many classes and cannot distinguish between watermarked and non-watermarked flows.

The DBSCAN algorithm divides the feature space into multiple tiny clusters and discards 1.19% of the samples as noise. It was verified by chi-square test (p=0.8793) that the mix of watermarked and non-watermarked traffic in the retained samples (50.08%:49.92%) was not significantly different from the original distribution (50%:50%). According to the statistical decision criterion (α<sub>=</sub>0.05), the original hypothesis was accepted when p>0.05, proving that watermarking did not change the macroscopic distribution structure of the traffic. Further calculation of the local density ratio (watermarked point density/original point density $= 0 . 9 9 \pm 0 . 0 8 )$ complies with the density ratio safety threshold $( 0 . 9 < \mathrm { r a t i o } < 1 . 1 )$ indicating that the embedding strength of the watermark is tightly controlled to be within the fluctuation range of the flow’s own noise (<2% difference). This also explains the root cause of the clustering failure on a physical level.

![](images/cf603fc6e5cf186a3413eeb58b20a414db3f1bb2cb29e90bc98fbb96b0d64824.jpg)  
Fig. 12. DBSCSN clustering results for watermarked and non-watermarked flows.

## C. Conclusion

In summary, both clustering algorithms cannot group data correctly. The quantitative analysis shows that if an attacker tries to detect watermarks through machine learning, the theoretical detection accuracy is capped at only 53.8% (based on the Bayesian error rate calculated from the distribution in Fig. 10), which is only an improvement of 3.8 percentage points over random guessing (50%). In a real deployment, the true detection performance will be much closer to the random level, taking into account the feature extraction error and the degradation of the model generalization capability. The fully overlapping distributions of the two types of traffic in Fig. 10 visually validate this conclusion, demonstrating that the watermarking perturbations of IFW are fully wrapped within the normal traffic variance. Therefore, it can be judged that IFW has invisibility.

Future work could be tuned to further enhance the invisibility under high noise conditions. Specifically, the Invertible Noise Layer (INL) can be designed to dynamically model the noise features and separate the noise interference from the watermarked signals through a layered embedding and decoupling mechanism. In addition, the statistical homology between the watermarked signal and the carrier traffic is strengthened by the implicit feature alignment mechanism, and the bi-directional mapping capability of INN is used to constrain the consistency of the traffic distribution before and after the watermark embedding, so that the watermarked features can still maintain the similar statistical characteristics with the original traffic under the noise interference, thus circumventing the adversarial analysis based on anomaly detection.

## VII. CONCLUSION

This work introduces IFW, a blind flow marking framework built on INN technology. The encoder of watermarking in this method also acts as a decoder, which can tightly couple the encoder and decoder under the same parameters. As a result, the encoded features maintain a high degree of consistency with the features needed by the decoder, and the embedding of redundant features is greatly avoided. This study conducts extensive experiments to analyze various parameters and determine the optimal configurations for each scenario. The experiments also demonstrate that the framework performs well under different noise conditions and can resist certain network perturbations. Finally, we demonstrate the invisibility of this paper’s scheme using the K-S similarity test and two clustering methods, revealing that attackers face significant challenges recognizing IFW watermarks.

## VIII. DISCUSSION AND FUTURE WORK

The INN-based blind flow watermarking framework (IFW) proposed in this paper demonstrates its significant advantages in improving the coupling of encoding and decoding. However, although the framework performs well in terms of robustness and invisibility, it still has some limitations.

(1) The current INN-based architecture is relatively sensitive to structural and parametric variations, which may affect its stability and flexibility across diverse scenarios. Future research can focus on designing dynamically reconfigurable INN architectures. Integrating protocol-agnostic feature extraction layers with neural architecture search (NAS) techniques could enhance model generalization.

(2) In real-world environments, attackers may adopt complex adversarial behaviors. Future studies could incorporate adversarial sample generation methods that simulate realistic attacker strategies, to further evaluate and improve IFW’s robustness and generalization under adversarial settings.

(3) The current IFW framework uses fixed one-hot encoding for watermark representation, which, while simple and intuitive, limits the per-flow watermark capacity. Future work will explore learnable watermark embeddings, such as trained low-dimensional vector representations, adaptive bit-level distribution control, or information-theoretic optimal coding strategies, aiming to enhance watermark bandwidth while maintaining invisibility.

(4) Although the model is trained on real Tor traffic, evaluations are mostly performed in simulated environments. Systematic testing in heterogeneous real-world settings (e.g., VPNs, enterprise networks, mobile devices) remains limited. Future work aims to extend IFW to other encrypted protocols such as OpenVPN and QUIC. Since application-layer protocols differ in flow control, packet sizes, and congestion behavior, the current design lacks explicit adaptation. Combining protocol-agnostic feature extraction with transfer learning may improve cross-protocol generalization and deployment flexibility.

(5) While clustering and K-S tests verify IFW’s invisibility against basic statistical detection, its resilience against advanced adversarial detection techniques (e.g., timing-based or GAN-based detectors) has not been systematically evaluated. Future directions involve integrating adversarial training strategies, introducing auxiliary discriminators during training to provide feedback and regularization for the embedded samples, thereby enhancing resistance to sophisticated detection methods.

(6) In extremely high-throughput scenarios, the computational and memory costs introduced by the invertible architecture may become a deployment bottleneck. To meet the low-latency and high-throughput demands of core networks, future work will explore hardware-friendly architecture optimizations, such as lightweight INN blocks, parameter sharing, and traffic segmentation-based processing.

(7) The current MLP-based parameter tuning module offers low training overhead and fast response, which suffices for typical network environments. However, against evolving adversarial threats, static tuning strategies may be insufficient. Future research may incorporate reinforcement learning or adversarial training mechanisms, using auxiliary discriminators or environmental feedback to construct a closed-loop optimization pipeline, thus improving the system’s adaptability to detection threats and ensuring long-term stability.

## ETHICS STATEMENT

This study fully considers ethical concerns, especially in tracking potentially anonymous users. We declare no conflict of interest and commit to using all research outcomes for lawful and ethical purposes only. To prevent misuse, we will not share code, data, or models with parties intending unethical applications.

We emphasize that misuse of IFW may threaten privacy and freedom, particularly under unauthorized surveillance. Thus, we advocate for ethical oversight and transparent usage. IFW should only be applied in legal scenarios, such as cybersecurity defense and malicious activity monitoring.

We recommend the following principles: (1) transparency and compliance with laws, (2) minimal and necessary data collection, (3) strong data protection, (4) clear boundaries to prevent misuse, and (5) inclusion of ethical reviews and user feedback mechanisms.

By adhering to these principles, we aim to ensure IFW is used responsibly, with respect for user rights, and to encourage ethical development in traffic tracking and cybersecurity fields.

## AVAILABILITY

The implementation code and source code sets used to reproduce our results are publicly available at https://github.com/rlinlinlin/IFW.git.

## REFERENCES

[1] A. Blum, D. Song, and S. Venkataraman, “Detection of interactive steppingstones: Algorithms and confidence bounds,” in Proc. 7th Int. Symp. Recent Adv. Intrusion Detection, Sophia Antipolis, France, Sep. 2004, pp. 258–277.

[2] X. Wang, D. S. Reeves, and S. F. Wu, “Inter-packet delay based correlation for tracing encrypted connections through stepping stones,” in Proc. 7th Eur. Symp. Res. Comput. Security, Zurich, Switzerland, Oct. 2002, pp. 244–263.

[3] T. He and L. Tong, “Detecting encrypted stepping-stone connections,” IEEE Trans. Signal Process., vol. 55, no. 5, pp. 1612–1623, May 2007.

[4] R. Shullich, J. Chu, P. Ji, and W. F. Chen, “A survey of research in stepping-stone detection,” Int. J. Electron. Commerce Stud., vol. 2, no. 2, pp. 103–126, 2011.

[5] R. Dingledine, N. Mathewson, and P. Syverson, “Tor: The secondgeneration onion router,” in Proc. USENIX Security Symp., 2004, p. 21.

[6] M. K. Reiter and A. D. Rubin, “Anonymous Web transactions with crowds,” Commun. ACM, vol. 42, no. 2, pp. 32–38, 1999.

[7] M. J. Freedman and R. Morris, “Tarzan: A peer-to-peer anonymizing network layer,” in Proc. Conf. Comput. Commun. Security, 2002, pp. 193–206.

[8] Y. Zhu, X. Fu, B. Graham, R. Bettati, and W. Zhao, “Correlation-based traffic analysis attacks on anonymity networks,” IEEE Trans. Parallel Distrib. Syst., vol. 21, no. 7, pp. 954–967, Jul. 2010.

[9] Y. Lu and Y. Zhu, “Correlation-based traffic analysis on encrypted VoIP traffic,” in Proc. 2nd Int. Conf. Netw. Security, Wireless Commun. Trusted Comput., Wuhan, China, 2010, pp. 45–48.

[10] X. Wang and D. S. Reeves, “Robust correlation of encrypted attack traffic through stepping stones by manipulation of interpacket delays,” in Proc. 10th ACM Conf. Comput. Commun. Security, 2003, pp. 20–29.

[11] Y. Zhang and V. Paxson, “Detecting stepping stones,” in Proc. USENIX Security Symp., 2000, p. 13.

[12] K. Yoda and H. Etoh, “Finding a connection chain for tracing intruders,” in Proc. Eur. Symp. Res. Comput. Security, 2000, pp. 191–205.

[13] Y. Zhu, X. Fu, B. Graham, R. Bettati, and W. Zhao, “On flow correlation attacks and countermeasures in mix networks,” in Proc. Int. Symp. Privacy Enhanc. Technol., 2004, pp. 207–225.

[14] D. L. Donoho, “Stepping-stone detection: Detecting pairs of jittered interactive streams by exploiting maximum tolerable delay,” in Proc. Int. Symp. Recent Adv. Intrusion Detection, 2002, pp. 1–9.

[15] G. Danezis, “The traffic analysis of continuous-time mixes,” in Proc. PETS, 2004, pp. 35–50.

[16] B. N. Levine, M. K. Reiter, C. Wang, and M. Wright, “Timing attacks in low-latency mix systems,” in Proc. 8th Int. Conf. Financ. Cryptogr., 2004, pp. 251–265.

[17] X. Wang, S. Chen, and S. Jajodia, “Network flow watermarking attack on low-latency anonymous communication systems,” in Proc. IEEE Symp. Security Privacy (SP), Berkeley, CA, USA, 2007, pp. 116–130.

[18] X. Wang, S. Chen, and S. Jajodia, “Tracking anonymous peer-to-peer VoIP calls on the Internet,” in Proc. 12th ACM Conf. Comput. Commun. Security, Alexandria, VA, USA, Nov. 2005, pp. 81–91.

[19] W. Yu, X. Fu, S. Graham, D. Xuan, and W. Zhao, “DSSS-based flow marking technique for invisible traceback,” in Proc. IEEE Symp. Security Privacy (SP), Berkeley, CA, USA, 2007, pp. 18–32.

[20] P. Peng, P. Ning, and D. S. Reeves, “On the secrecy of timingbased active watermarking trace-back techniques,” in Proc. IEEE Symp. Security Privacy (S&P), 2006, pp. 15–349.

[21] X. Wang, D. S. Reeves, S. F. Wu, and J. Yuill, “Sleepy watermark tracing: An active network-based intrusion response framework,” in Proc. 16th Int. Conf. Inf. Security Trusted Inf. New Decade Challenge (Sec), 2001, pp. 369–384.

[22] J. Huang, X. Pan, X. Fu, and J. Wang, “Long PN code based DSSS watermarking,” in Proc. 30th IEEE Int. Conf. Comput. Commun., Shanghai, China, Apr. 2011, pp. 2426–2434.

[23] X. Pan, J. Huang, Z. Ling, B. Lu, and X. Fu, “Long PN code based traceback in wireless networks,” Int. J. Performability Eng., vol. 8, no. 2, pp. 173–182, 2012.

[24] A. Houmansadr, N. Kiyavash, and N. Borisov, “RAINBOW: A robust and invisible non-blind watermark for network flows,” in Proc. 16th Annu. Netw. Distrib. Syst. Security Symp., San Diego, CA, USA, Feb. 2009, pp. 224–236.

[25] A. Houmansadr, N. Kiyavash, and N. Borisov, “Non-blind watermarking of network flows,” IEEE/ACM Trans. Netw., vol. 22, no. 4, pp. 1232–1244, Aug. 2014.

[26] A. Houmansadr and N. Borisov, “Towards improving network flow watermarking using the repeat-accumulate codes,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process., Prague, Czech Republic, May 2011, pp. 1852–1855.

[27] A. Houmansadr and N. Borisov, “SWIRL: A scalable watermark to detect correlated network flows,” in Proc. 18th Annu. Netw. Distrib. Syst. Security Symp., San Diego, CA, USA, Feb. 2011, pp. 1–15.

[28] X. Wang, M. Yang, and J. Luo, “A novel sequential watermark detection model for efficient traceback of secret network attack flows,” J. Netw. Comput. Appl., vol. 36, no. 6, pp. 1660–1670, 2013.

[29] M. Lin, G. Liu, W. Liu, and Y. Dai, “Network flow watermarking method based on centroid matching of interval group,” in Proc. Int. Conf. Progr. Inform. Comput., Nanjing, China, Dec. 2015, pp. 628–632.

[30] F. Rezaei and A. Houmansadr, “FINN: Fingerprinting network flows using neural networks,” in Proc. 37th Annu. Comput. Security Appl. Conf., 2021, pp. 1011–1024.

[31] A. Iacovazzi, S. Sarda, and Y. Elovici, “Inflow: Inverse network flow watermarking for detecting hidden servers,” in Proc. IEEE Conf. Comput. Commun., Honolulu, HI, USA, 2018, pp. 747–755.

[32] “Cluster analysis,” 2025. [Online]. Available: https://en.wikipedia.org/ wiki/Cluster\_analysis

[33] A. Majidi, N. Jahanbakhsh, X. Gao, J. Zheng, and G. Chen, “DC-ECN: A machine-learning based dynamic threshold control scheme for ECN marking in DCN,” Comput. Commun., vol. 150, pp. 334–345, Jan. 2020.

[34] X. Gao et al., “Nous: Drop-freeness and duplicate-freeness for consistent updating in SDN multicast routing,” IEEE/ACM Trans. Netw., vol. 32, no. 5, pp. 3685–3698, Oct. 2024.

[35] A. Majidi, X. Gao, S. Zhu, N. Jahanbakhsh, J. Zheng, and G. Chen, “MiFi: Bounded update to optimize network performance in software-defined data centers,” IEEE/ACM Trans. Netw., vol. 31, no. 1, pp. 322–335, Feb. 2023.

[36] D. Li, L. Deng, B. B. Gupta, H. Wang, and C. Choi, “A novel CNN based security guaranteed image watermarking generation scenario for smart city applications,” Inf. Sci., vol. 479, pp. 432–447, 2019.

[37] S. Mehraj et al., “RBWCI: Robust and blind watermarking framework for cultural images,” IEEE Trans. Consum. Electron., vol. 69, no. 2, pp. 128–139, May 2023.

[38] J. Li, C. Yu, B. B. Gupta, and X. Ren, “Color image watermarking scheme based on quaternion Hadamard transform and Schur decomposition,” Multimedia Tools Appl., vol. 77, pp. 4545–4561, 2018.

[39] L. Dinh, D. Krueger, and Y. Bengio, “NICE: Non-linear independent components estimation,” in Proc. ICLR Workshop, 2015, pp. 1–11.

[40] A. N. Gomez, M. Ren, R. Urtasun, and R. B. Grosse, “The reversible residual network: Backpropagation without storing activations,” in Proc. NeurIPS, 2017, pp. 1–14.

![](images/b6f5fb7fac20eff31f2eecbaed484aec2633296e2f30cb65399dbd316e3531dc.jpg)  
Yali Yuan received the Ph.D. degree from Göttingen University, Göttingen, Germany, in 2018. She joined the School of Cyber Science and Engineering, Southeast University, Nanjing, China, as an Assistant Professor in 2021. Her research interests include network traffic analysis and network security.

![](images/909e1f24a57aef6eb3c06dc94ffd3b9ee58a7487d6c57ceea36acf61cd6b4b53.jpg)

Ruolin Ma is currently pursuing the master’s degree with the School of Cyber Science and Engineering, Southeast University, Nanjing, China. Her research interests include network traffic analysis and darknet traffic tracing.

![](images/0fcf8b6872458acf84e89e00de3b030b5df89a1fe3cae7aa89475276f77bec2e.jpg)

Jian Ge is currently pursuing the M.S. degree with the School of Cyber Science and Engineering, Southeast University, Nanjing, China. His research interests include network traffic analysis and network security.

![](images/fc68505d27c6a1e66585a10cc3f4428c0d4ec36e53c7e8d3fce57de8352fce30.jpg)

Guang Cheng (Member, IEEE) received the B.S. degree in traffic engineering from Southeast University in 1994, the M.S. degree in computer application from the Hefei University of Technology in 2000, and the Ph.D. degree in computer network from Southeast University, Nanjing, China, in 2003, where he is a Full Professor with the School of Cyber Science and Engineering. He has authored or coauthored seven monographs and more than 100 technical papers, including top journals and top conferences. His research interests include network

security, network measurement, and traffic behavior analysis. He is a Senior Member of CCF.
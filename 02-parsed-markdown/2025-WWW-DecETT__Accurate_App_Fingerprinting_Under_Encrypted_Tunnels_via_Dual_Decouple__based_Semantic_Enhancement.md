# DecETT: Accurate App Fingerprinting Under Encrypted Tunnels via Dual Decouple-based Semantic Enhancement

Zheyuan Gu Institute of Information Engineering, Chinese Academy of Sciences Beijing, China School of Cyber Security, University of Chinese Academy of Sciences Beijing, China guzheyuan@iie.ac.cn

Chen Yang Institute of Information Engineering, Chinese Academy of Sciences Beijing, China School of Cyber Security, University of Chinese Academy of Sciences Beijing, China yangchen@iie.ac.cn

Chang Liu∗ Institute of Information Engineering, Chinese Academy of Sciences Beijing, China School of Cyber Security, University of Chinese Academy of Sciences Beijing, China liuchang@iie.ac.cn

Gaopeng Gou Institute of Information Engineering, Chinese Academy of Sciences Beijing, China School of Cyber Security, University of Chinese Academy of Sciences Beijing, China gougaopeng@iie.ac.cn

Xiyuan Zhang Institute of Information Engineering, Chinese Academy of Sciences Beijing, China School of Cyber Security, University of Chinese Academy of Sciences Beijing, China zhangxiyuan@iie.ac.cn

Gang Xiong Institute of Information Engineering, Chinese Academy of Sciences Beijing, China School of Cyber Security, University of Chinese Academy of Sciences Beijing, China xionggang@iie.ac.cn

Zhen Li Institute of Information Engineering, Chinese Academy of Sciences Beijing, China School of Cyber Security, University of Chinese Academy of Sciences Beijing, China lizhen@iie.ac.cn

Sijia Li Zhongguancun Laboratory Beijing, China lisj@zgclab.edu.cn

# Abstract

Due to the growing demand for privacy protection, encrypted tunnels have become increasingly popular among mobile app users, which brings new challenges to app fingerprinting (AF)-based network management. Existing methods primarily transfer traditional AF methods to encrypted tunnels directly, ignoring the core obfuscation and re-encapsulation mechanism of encrypted tunnels, thus resulting in unsatisfactory performance. In this paper, we propose DecETT, a dual decouple-based semantic enhancement method for accurate AF under encrypted tunnels. Specifically, DecETT improves AF under encrypted tunnels from two perspectives: app-specific feature enhancement and irrelevant tunnel feature decoupling. Considering the obfuscated app-specific information in encrypted tunnel traffic, DecETT introduces TLS traffic with stronger app-specific information as a semantic anchor to guide

![](images/0731255f5299703bec1e41cec545b28bf0e170cd175eeab24952999fc90ab6cf.jpg)

This work is licensed under a Creative Commons Attribution 4.0 International License. WWW ’25, Sydney, NSW, Australia © 2025 Copyright held by the owner/author(s). ACM ISBN 979-8-4007-1274-6/25/04 https://doi.org/10.1145/3696410.3714643

and enhance the fingerprint generation for tunnel traffic. Furthermore, to address the app-irrelevant tunnel feature introduced by the re-encapsulation mechanism, DecETT is designed with a dual decouple-based fingerprint enhancement module, which decouples the tunnel feature and app semantic feature from tunnel traffic separately, thereby minimizing the impact of tunnel features on accurate app fingerprint extraction. Evaluation under five prevalent encrypted tunnels indicates that DecETT outperforms state-of-theart methods in accurate AF under encrypted tunnels, and further demonstrates its superiority under tunnels with more complicated obfuscation. Project page: https://github.com/DecETT/DecETT

# CCS Concepts

• Information systems → Traffic analysis; • Security and privacy → Network security; • Networks → Network privacy and anonymity.

# Keywords

App Fingerprinting; Encrypted Tunnel; Encrypted Traffic Analysis; Decouple-based Representation Learning

# ACM Reference Format:

Zheyuan Gu, Chang Liu, Xiyuan Zhang, Chen Yang, Gaopeng Gou, Gang Xiong, Zhen Li, and Sijia Li. 2025. DecETT: Accurate App Fingerprinting

Under Encrypted Tunnels via Dual Decouple-based Semantic Enhancement. In Proceedings of the ACM Web Conference 2025 (WWW ’25), April 28-May 2, 2025, Sydney, NSW, Australia. ACM, New York, NY, USA, 11 pages. https: //doi.org/10.1145/3696410.3714643

# 1 Introduction

Over the past few years, we have witnessed the widespread use of encrypted tunnels in mobile network communications[10, 34, 40]. Serving as intermediaries that forward traffic between apps and servers, encrypted tunnels conceal both the identities of the communicating parties and the transmitted traffic characteristics, thus providing an effective way for privacy protection[3] and anonymous communication[25]. However, the prevalence of encrypted tunnels also poses new challenges to network management, such as Quality of Service (QoS)[41] and behavior auditing[1]. Traditional network management strategies primarily rely on app fingerprinting (AF) that identifies app usage activities by analyzing server information[26, 33] (e.g., IP address or Server Name Indicator) or TLS traffic characteristics[20, 30, 37]. However, encrypted tunnels obfuscate these two distinctive features, making accurate AF more challenging than in the traditional TLS scenario.

While prior work has developed some AF methods under encrypted tunnels, most of them directly transfer traditional AF methods, ignoring the core impact caused by tunnel mechanism. As illustrated in Figure 1, there exist three primary challenges in employing AF under encrypted tunnels compared with traditional TLS scenarios. (1) Diversity of encrypted tunnels. Currently, numerous kinds of encrypted tunnels have been widely used. Some studies design effective AF methods for specific encrypted tunnels[9, 14, 35], such as Shadowsocks and SSH. However, since different encrypted tunnels employ varying forwarding policies and encapsulation protocols for the original TLS traffic, developing specific AF methods for each tunnel type is labor-intensive and inefficient. (2) Lack of server information. In traditional TLS scenarios, server information, such as IP addresses, TLS certificates, and high-level interaction patterns, can be directly extracted from the original TLS traces to facilitate fingerprint construction. However, in encrypted tunnels, all traffic is forwarded to the tunnel server instead of the actual app servers, concealing all server-related information. As a result, server information-based methods, which perform excellently in TLS scenario[5, 26, 33], cannot be applied under encrypted tunnels. (3) Weaker AF semantic representations caused by reencapsulation. Existing methods attempt to extract discriminative features directly from the tunnel traffic[17, 21, 24, 39, 42]. However, encrypted tunnels employ re-encapsulation mechanism on the forwarded TLS traffic to ensure the confidentiality of tunnel communication. This process not only obfuscates the raw app-specific information, but also introduces tunnel-related information that is irrelevant to apps into the tunnel traffic, resulting in unsatisfactory performance and making accurate AF more challenging.

To address the aforementioned issues, in this paper, we propose DecETT, a dual decouple-based semantic enhancement method for accurate AF under encrypted tunnels. DecETT utilizes flow sequences as traffic representations to avoid the limitations of inaccessible server information. Specifically, DecETT consists of three key steps. Firstly, to mitigate the obfuscated app-specific features

![](images/c222b58eda07964a38c807bb8e47ed7cab822fd2014a1a0a32075cdb2a70e134.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Apps"] -->|Standard TLS Protocol| B["Server"]
    B -->|Raw TLS Traffic| A
    C["Apps"] -->|Re-encapsulated By Tunnel-specific Protocol| D["Proxy"]
    D -->|TLS Traffic| E["Server"]
    style A fill:#f9f,stroke:#333
    style C fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
    style E fill:#ccf,stroke:#333
```
</details>

Figure 1: Three main challenges in App Fingerprinting under encrypted tunnels: (1) Diversity of encrypted tunnels, (2) Server concealment, and (3) Traffic re-encapsulation.

caused by re-encapsulation, in the model-training phase, we introduce TLS traffic as a stronger and more stable semantic anchor to guide and enhance the fingerprint generation for tunnel traffic. Each tunnel flow is correlated with its corresponding original TLS flow for further analysis. Secondly, to address the negative impact of tunnel-related features, DecETT incorporates a dual decouplebased fingerprint enhancement module, which adopts a dual-branch Siamese network to tackle TLS and tunnel traffic separately. By decoupling the disentangled protocol features and app semantic features within the traffic, DecETT isolates protocol-related features that are irrelevant to app fingerprints, therefore reducing the impact of the re-encapsulation mechanism on capturing distinguishable app-specific information. Finally, the app semantic features extracted from tunnel traffic are input into the classifier as the generated fingerprint for the final AF results. Note that TLS traffic is only required during the training phase. Once DecETT has been well-trained, both TLS traffic and the TLS-branch model are no longer needed for inference. Therefore, the applicability of DecETT is not limited by the availability of TLS traffic in real-world scenarios. To validate the effectiveness of DecETT, we conduct extensive experiments under five widely used encrypted tunnels.

# Contributions. Our contributions can be summarized as:

• We propose a dual decouple-based semantic enhancement method, DecETT, which can achieve accurate app fingerprinting under various encrypted tunnels.   
• Considering the obfuscation of app-specific information caused by re-encapsulation, we introduce TLS traffic with stronger and more stable app semantic information to guide and enhance effective fingerprint generation.   
• We design a dual decouple-based semantic enhancement module to decouple tunnel-related features and app-specific semantic features, which mitigates the negative impact of re-encapsulation on accurate fingerprint extraction.   
• Evaluated under five widely-used encrypted tunnels, DecETT outperforms state-of-the-art methods on multiple metrics, and shows superiority under tunnels with more complicated obfuscation.

The remainder of this paper is organized as follows. Section 2 summarizes the prior research related to our work. Section 3 introduces the necessary foundational knowledge of this paper.

Section 4 highlights the overall design of DecETT, and Section 5 illustrates the experiments. Section 6 concludes the paper.

# 2 Related Work

From the task perspective, prior relevant works mainly focus on app fingerprinting and encrypted tunnel traffic analysis, respectively. In this section, we briefly review and discuss these works.

# 2.1 App Fingerprinting

App Fingerprinting (AF) refers to a side-channel network management technique that identifies app usage activities through encrypted traffic analysis. Although packet payloads are encrypted, certain traffic characteristics, such as server profiles, TLS certificates, and flow sequences, still allow for successful AF under encrypted traffic. Generally, prior works mainly fall into two groups, including server information analysis and flow feature mining.

Server Information Analysis. Server information analysisbased methods refer to using server-related features for accurate AF. Van Ede et al. [33] and Pham et al. [26] explore temporal correlations among destination-related features of network traffic and use these correlations to generate app fingerprints.

Flow Feature Mining. These methods focus on extracting fingerprints from the transmitted traffic flows and can be further divided into three parts. A typical approach is to utilize statistical features that are independent of encryption, such as packet lengths[30] and time-related features[4]. Another kind of approach[36, 38, 42] extracts the raw bytes of packets and employs deep learning to identify distinguishable app features based on the pseudo-randomness of encryption algorithms. For instance, ET-Bert[17] transforms the packet payloads into word-like tokens and achieves satisfactory performance based on the pre-training technique. Besides, deep mining of flow sequences also provides effective AF strategies. Liu et al. [18] utilize multi-layer end-to-end encoder-decoder structure to mine the potential sequence characteristics. Shen et al. [28] construct each flow sequence as a graph by burst division and association, and transform AF to a graph classification task.

While these methods have demonstrated high accuracy in traditional TLS scenario, their performance diminishes under encrypted tunnels since both server information and traffic characteristics are obfuscated, making effective AF more challenging.

# 2.2 Encrypted Tunnel Traffic Analysis

Currently, works for encrypted tunnel traffic analysis mainly focus on detecting tunnel flows from a massive amount of traffic. Several studies [16, 19, 22, 23] analyze and extract tunnel-specific protocol features to achieve accurate identification. For instance, Xue et al. [40] constructs OpenVPN traffic fingerprints from the aspects of byte pattern, packet size, and server response to achieve accurate OpenVPN traffic identification. Alice et al. [2] observe that the length and entropy value of the first packet in a flow can be used as specific features for Shadowsocks traffic detection, and combine active probing to further improve the identification accuracy.

Some other methods [8, 13, 24] dive into AF under encrypted tunnels for more fine-grained analysis. Xu et al. [39] convert each tunnel flow into a graph and combine it with statistical features to realize app classification. Wang et al. [35] add the sliding window JS divergence feature based on the traditional packet length and timestamp-related statistics to promote the accuracy and robustness of AF under Shadowsocks.

In summary, existing AF methods under encrypted tunnels mainly follow the technical roadmap of traditional TLS traffic classification and lack targeted solutions for the tunnel mechanism. Therefore, their performance is still limited by the weak app semantic features in tunnel traffic. In this work, we aim to mitigate the negative impact of tunnel obfuscation by both irrelevant tunnel feature decoupling and app semantic feature enhancement with the help of TLS traffic, thereby achieving accurate AF under various tunnels.

# 3 Preliminaries

In this section, we first provide the threat model of app fingerprinting, and then conduct a detailed analysis of the core principle of the tunnel re-encapsulation mechanism and its impact on tunnel flow sequences, to provide the necessary theoretical foundation.

# 3.1 Threat Model

In this paper, we refer to the threat model [26, 33] in previous app fingerprinting studies, with the critical difference that we focus on the more complex encrypted tunnel scenario. Specifically, an app fingerprinting system is located at the network boundary, where it can collect and analyze all traffic sent out from this network. The primary goal of AF is to identify app usage activities concealed in encrypted tunnels of specific mobile devices by analyzing the corresponding tunnel traffic. We assume that only one app is executed at a time, i.e., composite app fingerprints are not considered[33].

# 3.2 Re-encapsulation Mechanism

Firstly, to reveal the principle of the re-encapsulation mechanism intuitively, we summarize the source code of traffic re-encapsulation and forwarding process in Shadowsocks[27], a widely used encrypted tunnel tool for mobile devices, as shown in Figure 6 in Appendix A. Unnecessary functions and parameters are omitted, and annotations are added for clarity. When a local app attempts to send data through the tunnel, the tunnel client establishes a connection with the local app via ??????????\_???????? and creates a corresponding ????????????\_???????? to the tunnel server simultaneously. The tunnel client then receives and encrypts the data from the local app according to the tunnel protocol, and forwards it to the tunnel server. Similarly, upon receiving responses from the tunnel server, the tunnel client decrypts the data and sends it back to the local app, thereby achieving traffic forwarding of encrypted tunnels.

In summary, the tunnel client maintains two TCP connections and their correlation: one for communicating with the local app called ?????????????? and another for data transmission with the tunnel server called ????????????????. Both connections are implemented via socket communication, so the process of data encryption and forwarding does not vary based on the class of app data. Therefore, tunnel protocol features and app semantic features can be viewed as two independent variables for tunnel traffic generation, thereby ensuring the feasibility of the feature decoupling.

# 3.3 Impact on Tunnel Flow Sequences

Based on the principle of the re-encapsulation mechanism above, this section discusses its impact on tunnel flow sequences. We select a TLS flow and its two corresponding tunnel flows forwarded by V2Ray[31] for comparison.

![](images/e062038d017745c79331ca42bf094a38a26174ea84086c0b4428d943b83acf50.jpg)

<details>
<summary>bar_stacked</summary>

| Category | Original TLS Flow R | Tunnel Flow A | Tunnel Flow B |
| -------- | ------------------- | ------------- | ------------- |
| 110      | 586                 |               |               |
| 517      |                     | -1440         | 589           |
| -1448    |                     | -63           |             |
| -62      |                     | -1448         |             |
| -62      | -1448               | -24           |             |
| -65      |                     | -1448         |             |
| -1448    |                     | -72           |             |
| -1448    | -1432               | -15           |             |
| -84      |                     | -477          | -481          |
| -70      |                     | 74            | 82            |
| -70      |                     | -70           | -88           |
</details>

Figure 2: Flow sequence variation caused by tunnel reencapsulation mechanism.

As shown in Figure 2, the tunnel flow sequences differ from the TLS flow sequence after being forwarded by the tunnel. This variation can be attributed to the fact that tunnel flow sequences are affected by both the original app and tunnel re-encapsulation. Specifically, the impact of the latter on flow sequences mainly lies in three aspects. (1) Packet length variation. Compared to the original TLS traffic, the packet lengths in both flow ?? and ?? increase to varying degrees due to the additional byte overhead caused by tunnel re-encapsulation. Furthermore, TLS packets with the same length may correspond to packets of different lengths after re-encapsulation. For example, a packet with a length of 517 in flow ?? corresponds to packets of 586 and 589 in flows ?? and ??, respectively. (2) Packet fragmentation. Due to the extra byte overhead and the limitation of the Maximum Transmission Unit (MTU), the payload data of a single TLS packet may be split into two packets for transmission in tunnel traffic. For instance, a packet with a payload of 1440 bytes in flow ?? is split into two packets of 1448 bytes and 62 bytes in flow ??. (3) Packet redundancy. Some packets, such as the first packet in flow ?? with a payload of 110 bytes, are not generated by the upper-layer app and are more likely to serve as control packets for tunnel communication.

These variations indicate that tunnel mechanism obfuscate the app-specific information hidden in the flow sequences, resulting in poor AF performance. Considering that TLS traffic remains unaffected by the tunnel mechanism and shares the same app-specific information with tunnel traffic, it can serve as a robust semantic anchor for learning representative app semantic features in tunnel traffic, thereby facilitating accurate AF under encrypted tunnels.

# 4 Design of DecETT

Based on the aforementioned analysis of tunnel mechanism, in this section, we introduce our dual decouple-based semantic enhancement app fingerprinting method, DecETT. As shown in Figure 3, the architecture of DecETT could be divided into three main processes: traffic preprocess and correlation, dual decouple-based fingerprint enhancement, and generated AF classification.

# 4.1 Traffic Preprocess and Correlation

DecETT utilizes TLS traffic as a semantic anchor to mitigate app semantics loss and enhance the representation learning of the tunnel traffic. In this process, we construct parallel correlation flow pairs from the obfuscated network traffic to facilitate subsequent work.

Firstly, we reassemble TLS and tunnel flows separately based on 5-tuple information of the packets, including source IP, source port $( S _ { P o r t } )$ , destination IP, destination port $( D _ { P o r t } )$ , and protocol, and then pad or truncate them to the unified flow sequence length ??.

Next, the reassembled TLS and tunnel traffic flows are correlated according to the mapping table ?? maintained by the tunnel client. As we mentioned in Section 3.2, the tunnel client maintains a socket mapping relation (??????????????, ????????????????) ∈ ?? for each pair of the forwarded traffic. The ?????????????? keyword records the $S _ { P o r t }$ of the TCP connection established with the app, while the ???????????????? keyword records the $S _ { P o r t }$ of the TCP connection established with the tunnel server. Therefore, TLS flow that satisfies $S _ { P o r t } = =$ ?????????????? and tunnel flow that satisfies $S _ { P o r t } = = o u t b o u n d$ share the same app-specific information and are correlated as a parallel flow pair. Moreover, in order to avoid the confusion caused by port reuse, we restrict the time difference between the two flow start timestamps $t _ { F _ { t l s } } , t _ { F _ { t u n } }$ of the correlated flows to be less than a certain threshold ??. In summary, the flow correlation process can be formally described as the concatenation of $F _ { t l s }$ and $F _ { t u n }$ that satisfy:

$$
\left\{ \begin{array}{l} \left(S _ {p o r t} ^ {t l s}, S _ {p o r t} ^ {t u n}\right) = = (i n b o u n d, o u t b o u n d) \in M \\ \left| t _ {F _ {t l s}} - t _ {F _ {t u n}} \right| \leq \varepsilon \end{array} \right. \tag {1}
$$

By correlating each tunnel flow with its corresponding TLS flow that shares the same app-specific information, an additional semantic supervisory signal is provided for fingerprint learning of the tunnel flow, thereby facilitating its accurate AF.

Furthermore, in order to enrich the information retained in the packets, each parallel flow pair $F _ { t l s - t u n }$ is mapped through a trainable embedding layer ?????? (·). Formally, given a flow pair sequence as $F _ { t l s - t u n } = \{ [ { p } _ { 1 , t l s } , \ldots , { p } _ { n , t l s } ] , [ { p } _ { 1 , t u n } , \ldots , { p } _ { n , t u n } ] \}$ }, the embedding layer ??????(·) maps each packet ???? to an embedding vector ???? of dimension ??. Therefore, the raw flow pair is mapped to representation $x _ { t l s - t u n } = [ [ e _ { 1 , t l s } , \ldots , e _ { n , t l s } ] , [ e _ { 1 , t u n } , \ldots , e _ { n , t u n } ] ] \in \mathbb { R } ^ { 2 n \times d }$ for further analysis.

# 4.2 Dual decouple-based Fingerprint Enhancement

As we discussed in Section 3.2, the representation of encrypted tunnel traffic is jointly influenced by both app semantic and tunnel protocol features. Therefore, irrelevant protocol features inevitably hinder the learning of accurate app semantic features and thus bring negative impact to AF. In this process, we aim to decouple the protocol and app semantic features entangled in the traffic, and further enhance the semantic features with the help of TLS traffic to reduce the negative impact of tunnel re-encapsulation.

Specifically, DecETT employs a partially parameter-shared Siamese Network[7] with two branches to process TLS traffic and tunnel traffic separately. Each branch comprises a protocol-view encoder $E n c ^ { P } ( \cdot )$ , an AF-view encoder $E n c ^ { A } ( \cdot )$ , a decoder ?????? (·), and a MLP classifier ???????????? ?? ?????? (·). Each of the encoders and decoders utilizes a 2-layer stacked Bi-GRU[6] as the backbone to model the contextual bidirectional information of the flow sequences. The protocol-view encoder aims at learning protocol features $Z ^ { P } = E n \overset { \cdot } { c } ^ { P } ( x )$ that are independent of the app, while the AF-view encoder focuses on extracting app semantic features $Z ^ { A } = E n c ^ { A } ( x )$ from the raw traffic. In order to facilitate the decoupling process and enhance accurate fingerprint extraction, we propose two specific sub-modules to train DecETT. In the following, we present each of them in detail.

![](images/efa9f2ad5429ac403f7dad172ac99438236d08b59c93f3a534dbe4a7c926e7f5.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["TTL flow"] --> B["Correlation"]
    B --> C["Embedding"]
    C --> D["Tunnel flow"]
    D --> E["Server"]
    F["P-view Encoder"] --> G["Z^P_tls"]
    H["AF-view Encoder"] --> I["Z^A_tls"]
    J["GRL"] --> K["Decoder → x'_tls"]
    L["TTL-Branch"] --> M["Classifier"]
    N["Tunnel-Branch"] --> O["Classifier"]
    P["AF-view Encoder"] --> Q["Z^A_tun"]
    R["Decoder → x'_tun"]
    S["GRL"] --> T["Classifier"]
    U["Self Reconstruction Constraint (SRC)"] --> V["Decoder"]
    W["Protocol-feature Semantic Minimization (PSM)"] --> X["Decoder"]
    Y["Cross-Protocol Semantic Decoupling (CPD)"] --> Z["Decoder"]
    AA["App-specific Semantic Alignment (ASA)"] --> AB["Decoder"]
    AC["App Semantic Feature Classification (ASC)"] --> AD["Decoder"]
    AE["Shared Parameters"] --> AF["Decoder"]
    AG["AF-view Encoder And Decoder"] --> AH["Decoder"]
    AI["Non-shared Parameters Protocol-view Encoder"] --> AJ["Decoder"]
    AK["Classifier"] --> AL["Output"]
```
</details>

Figure 3: The overall architecture of DecETT.

4.2.1 Flow Representation Decoupling. In this sub-module, we force the app semantic features to be decoupled with the tunnel protocol features to reduce the negative impact of tunnel re-encapsulation.

Self Reconstruction Constraint (SRC). Since the original flow representation is decoupled into two independent features $Z ^ { P }$ and $Z ^ { \hat { A } }$ , it is essential to ensure that these two features retain as much of the original flow information as possible. Therefore, we first introduce self-reconstruction loss to ensure the fundamental correctness of feature decoupling, which can be calculated as follows:

$$
x _ {i, t l s} ^ {\prime} = \operatorname{Dec} \left(Z _ {i, t l s} ^ {P}, Z _ {i, t l s} ^ {A}\right) \tag {2}
$$

$$
x _ {i, t u n} ^ {\prime} = D e c (Z _ {i, t u n} ^ {P}, Z _ {i, t u n} ^ {A}) \tag {3}
$$

$$
\mathcal {L} _ {S R C} = - \frac {1}{N} \sum_ {i = 1} ^ {N} (| | x _ {i, t l s} ^ {\prime} - x _ {i, t l s} | | ^ {2} + | | x _ {i, t u n} ^ {\prime} - x _ {i, t u n} | | ^ {2}) \tag {4}
$$

where ?? stands for the total number of flow pairs. By minimizing the difference between the reconstructed and the original flow representations, SRC loss constrains the two decoupled features to fully preserve essential characteristics of the original traffic flow, ensuring that no critical information in the original flow is lost during feature decoupling.

Protocol-feature Semantic Minimization (PSM). Based on the assurance from SRC that app-specific information is preserved by either $Z ^ { A } \mathrm { o r } Z ^ { P }$ , minimizing the app-specific information in $\dot { Z ^ { P } }$ equals to maximizing the app-specific information captured by $Z _ { A }$ . To achieve this goal, we propose the Protocol-feature Semantic Minimization cross-entropy loss for $Z ^ { P }$ under the fingerprint classification task. Suppose $\hat { y } _ { i } ^ { P }$ is the predicted app label of $\overline { { Z _ { i } ^ { P } } }$ , the PSM loss can be formulated as:

$$
\mathcal {L} _ {P S M} = - \frac {1}{N} \sum_ {i = 1} ^ {N} y _ {i} (l o g (\hat {y} _ {i, t l s} ^ {P}) + l o g (\hat {y} _ {i, t u n} ^ {P})) \tag {5}
$$

During the training process, we apply Gradient Reversal Layer (GRL) [11] to reverse the gradient during back-propagation to maximize $\mathcal { L } _ { P S M }$ , thereby minimizing the app-specific information captured by $Z ^ { P }$ . Under the dual constraints of both SRC and PSM, DecETT encourages $Z ^ { A }$ to capture more app-specific information, thereby achieving effective feature decoupling and extraction.

Cross-Protocol Semantic Decoupling (CPD). To further facilitate the feature decoupling, we propose the cross-protocol semantics decoupling that swaps the extracted app semantic features $Z ^ { A }$ gether with to reconstruct the original flow representations $Z _ { t l s } ^ { P }$ and $Z _ { t u n } ^ { \bar { A } } .$ respectively. Formally, the cross-protocol $x _ { t l s }$ and $x _ { t u n }$ toreconstruction process can be described as follows:

$$
\hat {x} _ {i, t l s} = D e c (Z _ {i, t l s} ^ {P}, Z _ {i, t u n} ^ {A}) \tag {6}
$$

$$
\hat {x} _ {i, t u n} = D e c (Z _ {i, t u n} ^ {P}, Z _ {i, t l s} ^ {A}) \tag {7}
$$

Thus the CPD loss can be calculated as:

$$
\mathcal {L} _ {C P D} = - \frac {1}{N} \sum_ {i = 1} ^ {N} (| | \hat {x} _ {i, t l s} - x _ {i, t l s} | | ^ {2} + | | \hat {x} _ {i, t u n} - x _ {i, t u n} | | ^ {2}) \tag {8}
$$

By minimizing CPD loss, DecETT not only reduces the amount of protocol information irrelevant to apps contained in $Z ^ { A }$ , but also implicitly aligns the app semantic features extracted from the parallel flow pairs.

Therefore, the total loss of flow representation decoupling submodule $\mathcal { L } _ { F R D }$ can be summarized as:

$$
\mathcal {L} _ {F R D} = \lambda_ {1} \mathcal {L} _ {S R C} + \lambda_ {2} \mathcal {L} _ {P S M} + \lambda_ {3} \mathcal {L} _ {C P D} \tag {9}
$$

4.2.2 App Semantic Feature Augmentation. In this sub-module, the app semantic features decoupled from the tunnel traffic are further augmented by aligning with two supervisory signals with strong semantics.

App-specific Semantic Alignment (ASA). Based on the two decoupled features, ASA explicitly aligns the app semantic features $Z _ { t l s } ^ { A }$ and $Z _ { t u n } ^ { A }$ decoupled from TLS traffic and tunnel traffic, respectively. Specifically, DecETT achieves semantic alignment between $Z _ { t l s } ^ { A }$ and $Z _ { t u n } ^ { A }$ by minimizing their cosine similarity loss:

$$
\mathcal {L} _ {A S A} = - \frac {1}{N} \sum_ {i = 1} ^ {N} (1 - \frac {Z _ {i , t l s} ^ {A} \cdot Z _ {i , t u n} ^ {A}}{| | Z _ {i , t l s} ^ {A} | | \cdot | | Z _ {i , t u n} ^ {A} | |}) \tag {10}
$$

By increasing the similardimensional semantic space, etween serves ???? $Z _ { t l s } ^ { A }$ ???????? and n add $Z _ { t u n } ^ { A }$ in the high-al class-level $Z _ { t l s } ^ { A }$ supervisory signal that provides richer and more stable app-specific information than the class label, thus facilitating more accurate fingerprint generation under encrypted tunnels.

App Semantic Feature Classification (ASC). To ensure the correct semantic mapping between the generated fingerprint $Z ^ { A }$ and the corresponding app label, we calculate another classification loss as follows:

$$
\mathcal {L} _ {A S C} = - \frac {1}{N} \sum_ {i = 1} ^ {N} y _ {i} \left(\log \left(\hat {y} _ {i, t l s} ^ {A}\right) + \log \left(\hat {y} _ {i, t u n} ^ {A}\right)\right) \tag {11}
$$

Therefore, the loss of app semantic feature augmentation submodule $\mathcal { L } _ { A F A }$ is calculated as:

$$
\mathcal {L} _ {A F A} = \lambda_ {4} \mathcal {L} _ {A S A} + \lambda_ {5} \mathcal {L} _ {A S C} \tag {12}
$$

Combined with $\mathcal { L } _ { F R D }$ , the total loss of DecETT can be summarized as follows:

$$
\mathcal {L} _ {\text { DecETT }} = \mathcal {L} _ {\text { FRD }} + \mathcal {L} _ {\text { AFA }} \tag {13}
$$

# 4.3 Generated Fingerprint Classification

Once DecETT is well-trained, only ??????(·), $E n c _ { t u n } ^ { A } ( \cdot )$ and the tunnel traffic flows $F _ { t u n }$ instead of parallel flow pairs are needed to generate corresponding fingerprints. This allows DecETT to be employed in real network environments, since parallel flows are inaccessible in real-world deployment. Formally, for a tunnel flow $F _ { t u n } = \{ p 1 , p 2 , \cdot \cdot \cdot , p _ { n } \}$ , the corresponding fingerprint $F P _ { F _ { t u n } }$ can be generated as:

$$
F P _ {F _ {t u n}} = E n c _ {t u n} ^ {A} (E m b (F _ {t u n})) \tag {14}
$$

Ultimately, the corresponding AF result can be calculated as:

$$
y _ {p r e d} = \text { Classifier } (F P _ {F _ {t u n}}) \tag {15}
$$

# 5 Experiments

In this section, we perform empirical evaluations to demonstrate the effectiveness of DecETT. We first provide the dataset collection and composition, and then introduce the experimental setup, including baselines, evaluation metrics and implementation details. Finally, we proceed to detail the experimental results and their analysis.

# 5.1 Dataset

DecETT utilizes parallel TLS and tunnel flow pairs to realize accurate app fingerprinting. Although there have been previous related studies, datasets that provide parallel flow pairs have not been established yet. Consequently, we first select 5 representative encrypted tunnels and 54 widely-used apps for our study, and invite several volunteers to interact with these apps through the 5 tunnels separately, thereby producing corresponding traffic flows. In order to purify the collected traffic without noise flows generated by other apps, we follow the traffic collection framework proposed in [15] that uses iptables and NFLOG to mirror and capture pure TLS traffic generated by specific apps. The configurations of 5 tunnels and the detailed information of 5 datasets can be found in Appendix B and C, respectively, and the full list of apps is shown in Appendix F.

# 5.2 Experimental Setup

Comparison Methods. We compare our proposed DecETT with four categories of AF or encrypted tunnel traffic analysis methods, including (1) Statistical-based method (AppScanner[30]), which extracts time or packet-related statistical features for further classification; (2) Server information-related method (i.e. FlowPrint[33]) where the communicated server information is considered; (3) Payload-based methods (ET-BERT[17], YaTC[42]) which directly use the raw packet payload content to achieve AF, and (4) Sequencebased methods, such as DF[29], FS-Net[18] and GraphDApp[28], that dedicate to mining the flow sequences for accurate AF.

Evaluation Metrics. In this paper, we choose the four widelyused metrics in multi-class classification tasks, i.e., Accuracy, Precision, Recall, and F1-score, to comprehensively evaluate the performance of different methods on AF under encrypted tunnels.

Implementation Details. The implementation details can be found in Appendix D.

# 5.3 Analysis of AF Results Under Single Tunnel

Firstly, we evaluate the performance of all the comparison methods on accurate app fingerprinting under the specific single tunnel. The corresponding results are reported in Table 1.

5.3.1 Main Evaluation. From Table 1, we can draw the following conclusions:

(1) In terms of the four comprehensive evaluation metrics, our approach DecETT outperforms all the other comparison methods by significant margins. Specifically, DecETT achieves the best performance of 94.2% Accuracy, Recall, and F1-score under ShadowsocksR. The following method is FS-Net, which reaches the F1-score of 61% under V2Ray and around 85% under the other tunnels. The performance of FlowPrint is the worst among all the comparison methods, with nearly all metrics lower than 10% under all five tunnels.

(2) DecETT shows more significant performance superiority under tunnels with more complicated obfuscation. Results of various methods across 5 tunnels show that V2Ray employs more obfuscated encapsulation to the raw TLS traffic. Under the other 4 tunnels, DecETT achieves a performance improvement of approximately 7% to 10% compared to the second best-performed method, FS-Net, while under the V2Ray tunnel, the performance gap rises to nearly 20%. By decoupling the app-irrelevant protocol features and enhancing the fingerprint representations through semantic-shared TLS traffic, DecETT minimizes the negative impact caused by the re-encapsulation mechanism, thereby significantly improving AF performance under complex tunnels.

(3) The performance of both statistical and server informationbased methods is not satisfactory enough. Specifically, AppScanner achieves nearly 100% Precision, but fails in Recall value of only around 30% to 60%, indicating its insufficient capability in fully characterizing app-specific information from tunnel traffic. The server information-based method FlowPrint is also ineffective, with an average F1-score of only 1.4% across five tunnels. FlowPrint relies on the flow interaction relationships with various app servers; however, server information is no longer visible in tunnel traffic, thus resulting in severe performance degradation. These results indicate that statistical and server information-based features cannot provide sufficient flow representation as flow sequences used in DecETT for accurate AF under encrypted tunnels.

Table 1: Performance comparison results w.r.t. Accuracy (Acc), Precision (P), Recall (R) and F1-score (F1) under 5 tunnels. Bold represents the best and underline refers to the second. 

<table><tr><td rowspan="2">Method</td><td>Dataset</td><td colspan="4">Shadowsocks</td><td colspan="4">ShadowsocksR</td><td colspan="4">V2Ray</td><td colspan="4">Trojan</td><td colspan="4">OpenVPN</td></tr><tr><td>Metric</td><td>Acc</td><td>P</td><td>R</td><td>F1</td><td>Acc</td><td>P</td><td>R</td><td>F1</td><td>Acc</td><td>P</td><td>R</td><td>F1</td><td>Acc</td><td>P</td><td>R</td><td>F1</td><td>Acc</td><td>P</td><td>R</td><td>F1</td></tr><tr><td>Statistic</td><td>AppScanner[30]</td><td>0.630</td><td>0.995</td><td>0.630</td><td>0.764</td><td>0.631</td><td>0.996</td><td>0.631</td><td>0.767</td><td>0.295</td><td>0.993</td><td>0.295</td><td>0.429</td><td>0.609</td><td>0.996</td><td>0.609</td><td>0.748</td><td>0.582</td><td>0.995</td><td>0.582</td><td>0.725</td></tr><tr><td>Server</td><td>FlowPrint[33]</td><td>0.122</td><td>0.015</td><td>0.122</td><td>0.027</td><td>0.053</td><td>0.003</td><td>0.053</td><td>0.005</td><td>0.103</td><td>0.013</td><td>0.103</td><td>0.022</td><td>0.050</td><td>0.008</td><td>0.050</td><td>0.012</td><td>0.027</td><td>0.001</td><td>0.027</td><td>0.002</td></tr><tr><td rowspan="2">Payload</td><td>ET-BERT[17]</td><td>0.079</td><td>0.085</td><td>0.079</td><td>0.045</td><td>0.098</td><td>0.134</td><td>0.098</td><td>0.085</td><td>0.055</td><td>0.072</td><td>0.055</td><td>0.032</td><td>0.280</td><td>0.216</td><td>0.203</td><td>0.203</td><td>0.265</td><td>0.300</td><td>0.265</td><td>0.256</td></tr><tr><td>YaTC[42]</td><td>0.596</td><td>0.656</td><td>0.596</td><td>0.592</td><td>0.771</td><td>0.825</td><td>0.771</td><td>0.785</td><td>0.436</td><td>0.496</td><td>0.436</td><td>0.407</td><td>0.602</td><td>0.678</td><td>0.602</td><td>0.606</td><td>0.884</td><td>0.934</td><td>0.884</td><td>0.899</td></tr><tr><td rowspan="3">Sequence</td><td>DF[29]</td><td>0.739</td><td>0.746</td><td>0.739</td><td>0.738</td><td>0.762</td><td>0.764</td><td>0.762</td><td>0.760</td><td>0.656</td><td>0.659</td><td>0.656</td><td>0.651</td><td>0.726</td><td>0.730</td><td>0.726</td><td>0.724</td><td>0.816</td><td>0.818</td><td>0.816</td><td>0.816</td></tr><tr><td>FS-Net[18]</td><td>0.845</td><td>0.837</td><td>0.838</td><td>0.837</td><td>0.856</td><td>0.849</td><td>0.850</td><td>0.849</td><td>0.610</td><td>0.610</td><td>0.606</td><td>0.610</td><td>0.822</td><td>0.828</td><td>0.822</td><td>0.823</td><td>0.876</td><td>0.874</td><td>0.873</td><td>0.874</td></tr><tr><td>GraphDApp[28]</td><td>0.786</td><td>0.800</td><td>0.786</td><td>0.789</td><td>0.817</td><td>0.812</td><td>0.811</td><td>0.812</td><td>0.503</td><td>0.516</td><td>0.501</td><td>0.516</td><td>0.767</td><td>0.763</td><td>0.760</td><td>0.763</td><td>0.810</td><td>0.805</td><td>0.806</td><td>0.805</td></tr><tr><td>Ours</td><td>DecETT</td><td>0.925</td><td>0.926</td><td>0.925</td><td>0.925</td><td>0.942</td><td>0.942</td><td>0.942</td><td>0.942</td><td>0.802</td><td>0.803</td><td>0.802</td><td>0.801</td><td>0.920</td><td>0.922</td><td>0.920</td><td>0.921</td><td>0.941</td><td>0.941</td><td>0.941</td><td>0.941</td></tr></table>

![](images/74625f677df3a93d86605122a8f114ede51a06ea32f855c516d90dbb6057d8dc.jpg)

<details>
<summary>line</summary>

| Flow Length | DecETT | FS-Net |
| ----------- | ------ | ------ |
| 0           | 0.0    | 0.0    |
| 50          | 0.8    | 0.6    |
| 100         | 0.7    | 0.5    |
| 150         | 0.9    | 0.7    |
| 200         | 1.0    | 0.8    |
</details>

Figure 4: Comparison results of different flow lengths.

(4) As for the two payload-based methods, ET-BERT performs poorly across five datasets, with the highest F1-score of only 25.6%. YaTC achieves better performance than ET-BERT, but still has the maximum performance gap of approximately 40% compared to DecETT. These methods rely on specific plaintext fields in TLS protocol or the pseudo-randomness of encryption algorithms to construct app fingerprints. However, compared to flow sequences, the impact of the re-encapsulation mechanism on these two features is more pronounced and difficult to model, rendering these methods insufficient for effectively modeling app fingerprints under tunnels. These results further highlight the superiority of using flow sequences as the form of tunnel traffic representation in DecETT.

(5) Sequence-based methods perform better than other approaches, with FS-Net achieving the second-best performance across four tunnels. Reasons can be owing to that although the re-encapsulation mechanism affects the packet lengths, changes in flow sequences and packet transmitting directions stay relatively stable compared to the packet payload. Based on utilizing flow sequence as the form of traffic representations, DecETT introduces TLS traffic to provide stronger app-specific information for fingerprint learning, and further decouples the app semantic features hidden in the raw tunnel traffic, thereby achieving accurate app fingerprinting.

5.3.2 Performance Analysis on Short Flows. To better illustrate the superiority of DecETT, we analyze its AF performance on flows

![](images/9deaf5c36852208cf979e64af320e7574fe9f88bb8e5ff1532a46ca914cb1cdc.jpg)

<details>
<summary>scatter</summary>

| x    | y    | cluster |
| ---- | ---- | ------- |
| -50  | 20   | blue    |
| -40  | 30   | blue    |
| -30  | 10   | blue    |
| -20  | -10  | blue    |
| -10  | -20  | blue    |
| 0    | -30  | blue    |
| 10   | -40  | blue    |
| 20   | -50  | blue    |
| 30   | -60  | blue    |
| 40   | -50  | blue    |
| 50   | -40  | blue    |
| -50  | -30  | purple  |
| -40  | -20  | purple  |
| -30  | -10  | purple  |
| -20  | 0    | purple  |
| -10  | 10   | purple  |
| 0    | 20   | purple  |
| 10   | 30   | purple  |
| 20   | 40   | purple  |
| 30   | 50   | purple  |
| 40   | 60   | purple  |
| -50  | -40  | yellow  |
| -40  | -30  | yellow  |
| -30  | -20  | yellow  |
| -20  | -10  | yellow  |
| -10  | 0    | yellow  |
| 0    | 10   | yellow  |
| 10   | 20   | yellow  |
| 20   | 30   | yellow  |
| 30   | 40   | yellow  |
| 40   | 50   | yellow  |
| 50   | 60   | yellow  |
| -50  | -50  | red     |
| -40  | -40  | red     |
| -30  | -30  | red     |
| -20  | -20  | red     |
| -10  | -10  | red     |
| 0    | 0    | red     |
| 10   | 10   | red     |
| 20   | 20   | red     |
| 30   | 30   | red     |
| 40   | 40   | red     |
| 50   | 50   | red     |
| -50  | -60  | green   |
| -40  | -50  | green   |
| -30  | -40  | green   |
| -20  | -30  | green   |
| -10  | -20  | green   |
| 0    | -10  | green   |
| 10   | 0    | green   |
| 20   | 10   | green   |
| 30   | 20   | green   |
| 40   | 30   | green   |
| 50   | 40   | green   |
| -50  | -70  | orange  |
| -40  | -60  | orange  |
| -30  | -50  | orange  |
| -20  | -40  | orange  |
| -10  | -30  | orange  |
| 0    | -20  | orange  |
| 10   | -10  | orange  |
| 20   | 0    | orange  |
| 30   | 10   | orange  |
| 40   | 20   | orange  |
| 50   | 30   | orange  |
| -50  | -80  | brown   |
| -40  | -70  | brown   |
| -30  | -60  | brown   |
| -20  | -50  | brown   |
| -10  | -40  | brown   |
| 0    | -30  | brown   |
| 10   | -20  | brown   |
| 20   | -10  | brown   |
| 30   | 0    | brown   |
| 40   | 10   | brown   |
| 50   | 20   | brown   |
| -50  | -90  | white   |
| -40  | -80  | white   |
| -30  | -70  | white   |
| -20  | -60  | white   |
| -10  | -50  | white   |
| 0    | -40  | white   |
| 10   | -30  | white   |
| 20   | -20  | white   |
| 30   | -10  | white   |
| 40   | 0    | white   |
| 50   | 10   | white   |
| -50  | -100 | black   |
| -40  | -90  | black   |
| -30  | -80  | black   |
| -20  | -70  | black   |
| -10  | -60  | black   |
| 0    | -50  | black   |
| 10   | -40  | black   |
| 20   | -30  | black   |
| 30   | -20  | black   |
| 40   | -10  | black   |
| 50   | 0    | black   |
| -50  | +10  | white   |
| -40  | +20  | white   |
| -30  | +30  | white   |
| -20  | +40  | white   |
| -10  | +50  | white   |
| \      | +6    | white   |
| \      (additional points) for visual comparison: visual scatterplot from left to right. The original data points are not explicitly labeled. Values are estimated based on the visual representation of the color space. Values are estimated based on the color space used for visualization. Legend indicates different colors for each point.
</details>

![](images/0b9e0129178b69b05a8067d06e7f0fa0e8073b9ed599c0f1ce6e721c2fba936c.jpg)

<details>
<summary>scatter</summary>

| x    | y    | group |
| ---- | ---- | ----- |
| -50  | 20   | A     |
| -40  | 15   | A     |
| -30  | 10   | A     |
| -20  | 5    | A     |
| -10  | 0    | A     |
| 0    | -5   | A     |
| 10   | -10  | A     |
| 20   | -15  | A     |
| 30   | -20  | A     |
| 40   | -25  | A     |
| 50   | -30  | A     |
| -50  | -30  | B     |
| -40  | -25  | B     |
| -30  | -20  | B     |
| -20  | -15  | B     |
| -10  | -10  | B     |
| 0    | -5   | B     |
| 10   | 0    | B     |
| 20   | 5    | B     |
| 30   | 10   | B     |
| 40   | 15   | B     |
| 50   | 20   | B     |
| -50  | -40  | C     |
| -40  | -35  | C     |
| -30  | -30  | C     |
| -20  | -25  | C     |
| -10  | -20  | C     |
| 0    | -15  | C     |
| 10   | -10  | C     |
| 20   | -5   | C     |
| 30   | 0    | C     |
| 40   | 5    | C     |
| 50   | 10   | C     |
| -50  | -50  | D     |
| -40  | -45  | D     |
| -30  | -40  | D     |
| -20  | -35  | D     |
| -10  | -30  | D     |
| 0    | -25  | D     |
| 10   | -20  | D     |
| 20   | -15  | D     |
| 30   | -10  | D     |
| 40   | -5   | D     |
| 50   | 0    | D     |
| -50  | -60  | E     |
| -40  | -55  | E     |
| -30  | -50  | E     |
| -20  | -45  | E     |
| -10  | -40  | E     |
| 0    | -35  | E     |
| 10   | -30  | E     |
| 20   | -25  | E     |
| 30   | -20  | E     |
| 40   | -15  | E     |
| 50   | -10  | E     |
| -50  | -70  | F     |
| -40  | -65  | F     |
| -30  | -60  | F     |
| -20  | -55  | F     |
| -10  | -50  | F     |
| 0    | -45  | F     |
| 10   | -40  | F     |
| 20   | -35  | F     |
| 30   | -30  | F     |
| 40   | -25  | F     |
| 50   | -20  | F     |
| -50  | -80  | G     |
| -40  | -75  | G     |
| -30  | -70  | G     |
| -20  | -65  | G     |
| -10  | -60  | G     |
| 0    | -55  | G     |
| 10   | -50  | G     |
| 20   | -45  | G     |
| 30   | -40  | G     |
| 40   | -35  | G     |
| 50   | -30  | G     |
| -50  | -90  | H     |
| -40  | -85  | H     |
| -30  | -80  | H     |
| -20  | -75  | H     |
| -10  | -70  | H     |
| 0    | -65  | H     |
| 10   | -60  | H     |
| 20   | -55  | H     |
| 30   | -50  | H     |
| 40   | -45  | H     |
| 50   | -40  | H     |
| -50  | -100 | I     |
| -40  | -95  | I     |
| -30  | -90  | I     |
| -20  | -85  | I     |
| -10  | -80  | I     |
| 0    | -75  | I     |
| 10   | -70  | I     |
| 20   | -65  | I     |
| 30   | -60  | I     |
| 40   | -55  | I     |
| 50   | -50  | I     |
| -50  | +10  | J     |
| -40  | +15  | J     |
| -30  | +20  | J     |
| -20  | +25  | J     |
| -10  | +30  | J     |
| 0    | +35  | J     |
| 10   | +40  | J     |
| 20   | +45  | J     |
| 30   | +50  | J     |
| 40   | +55  | J     |
| 50   | +60  | J     |
| -50  | +2           | K     |
| -40  | +2.5         | K     |
| -30  | +3.0         | K     |
| -20  | +2.5         | K     |
| -10  | +2.0         | K     |
| 0    | +1.5         | K     |
| 10   | +1.0         | K     |
| 20   | +1.5         | K     |
| 30   | +2.0         | K     |
| 40   | +2.5         | K     |
| 50   | +3.0         | K     |
| -50  | +4           | L     |
| -40  | +4.5         | L     |
| -30  | +5.0         | L     |
| -20  | +4.5         | L     |
| -10  | +4.0         | L     |
| 0    | +3.5         | L     |
| 10   | +3.0         | L     |
| 20   | +2.5         | L     |
| 30   | +2.0         | L     |
| 40   | +1.5         | L     |
| 50   | +1.0         | L     |
| -50  | +6           | M     |
| -40  | +6.5         | M     |
| -30  | +7.0         | M     |
| -20  | +6.5         | M     |
| -10  | +6.0         | M     |
| \textbf{-1} / \textbf{-M} / \textbf{-L} / \textbf{-H} / \textbf{-I} / \textbf{-J} / \textbf{-K} / \textbf{-L} / \textbf{-M} / \textbf{-N} / \textbf{-O} / \textbf{-P} / \textbf{-Q} / \textbf{-R} / \textbf{-S} / \textbf{-T} / \textbf{-U} / \textbf{-V} / \textbf{-W} / \textbf{-X} / \textbf{-Y} / \textbf{-Z} / \textbf{-A} / \textbf{-B} / \textbf{-C} / \textbf{-D} / \textbf{-E} / \textbf{-F} / \textbf{-G} / \textbf{-H} / \textbf{-I} / \textbf{-J} / \textbf{-K} / \textbf{-L} / \textbf{-M} / \textbf{-N} / \textbf{-O} / \textbf{-P} / \textbf{-Q} / \textbf{-R} / \textbf{-S} / \textbf{-T} / \textbf{-U} ,\textbf{-V} / \textbf{-W} / \textbf{-X} / \textbf{-Y} / \textbf{-Z} / \textbf{-I} / \textbf{-J} / \textbf{-K} / \textbf{-L} / \textbf{-M} / \textbf{-N} / \textbf{-O} / \textbf{-P} / \textbf{-Q} / \textbf{-R} / \textbf{-S} / \textbf{-T} / \textbf{-U} / \textbf{-V} \\ \textbf{-V} / \textbf{-M} / \textbf{-H} / \textbf{-I} / \textbf{-J} / \textbf{-K} / \textbf{-L} / \textbf{-M} / \textbf{-N} / \textbf{-O} / \textbf{-P} / \textbf{-Q} / \textbf{-R} / \textbf{-S} / \textbf{-T} / \textbf{-U} \\ \textbf{-V} / \textbf{-M} / \textbf{-H} / \textbf{-I} / \textbf{-J} / \textbf{-K} / \textbf{-L} / \textbf{-M} / \textbf{-N} / \textbf{-O} / \textbf{-P} / \textbf{-Q} / \textbf{-R} / \textbf{-S} \\ \textbf{-V} / \textbf{-M} / \textbf{-H} / \textbf{-I} / \textbf{-J} / \textbf{-K} / \textbf{-L} / \textbf{-M} / \textbf{-N} / \textbf{-O} / \textbf{-P} \\ \textbf{-V} / \textbf{-M} / \textbf{-H} / \textbf{-I} / \textbf{-J} / \textbf{-K} / \textbf{-L} / \textbf{-M} / \textbf{-N} / \textbf{-O} \\ \textbf{-V} / \textbf{-M} / \textbf{-H} / \textbf{-I} / \textbf{-J} / \textbf{-K} / \textbf{-L} / \textbf{-M} / \textbf{-N} \\ \textbf{H}{\mathfrak{k}}^{+}\mathfrak{k}_{\mathfrak{k}}^{+}\mathfrak{k}_{\mathfrak{k}}^{+}\mathfrak{k}_{\mathfrak{k}}^{+}\mathfrak{k}_{\mathfrak{k}}^{+}\mathfrak{k}_{\mathfrak{k}}^{+}\mathfrak{k}_{\mathfrak{k}}^{+}\mathfrak{k}_{\mathfrak{k}}^{+}\mathfrak{k}_{\mathrm{m}}^{+}\mathfrak{k}_{\mathrm{m}}^{+}\mathfrak{k}_{\mathrm{m}}^{+}\mathfrak{k}_{\mathrm{m}}^{+}\mathfrak{k}_{\mathrm{m}}^{+}\mathfrak{k}_{\mathrm{m}}^{+}\mathfrak{k}_{\mathrm{m}}^{+}\mathfrak{k}_{\mathrm{m}}^{+}\mathfrak{k}_ {\mathrm{m}}^{+}\mathfrak{k}_{\mathrm{m}}^{+}\mathfrak{k}_{\mathrm{m}}^{+}\mathfrak{k}_{\mathrm{m}}^{+}\mathfrak{k}_{\mathrm{m}}^{+}\mathfrak{k}_{\mathrm{m}}^{+}\mathfrak{k}_{\mathrm{m}}^{+}\mathfrak{k}_{\mathrm{m}}^{+}\mathsf{q}_{\mathrm{m}}^{+}\mathsf{q}_{\mathrm{m}}^{+}\mathsf{q}_{\mathrm{m}}^{+}\mathsf{q}_{\mathrm{m}}^{+}\mathsf{q}_{\mathrm{m}}^{+}\mathsf{q}_{\mathrm{m}}^{+}\mathsf{q}_{\mathrm{m}}^{+}\mathsf{q}_{\mathrm{m}}^{+}
</details>

Figure 5: Visual distinction of generated fingerprints where different colors stand for different classes.

of varying lengths. Figure 4 shows the Accuracy results of both DecETT and FS-Net on V2Ray flows with lengths ranging from 0 to 200. As shown in Figure 4, DecETT demonstrates a remarkable improvement in fingerprinting short flows with lengths below 100 compared to FS-Net. This improvement can be attributed to both the introduction of TLS traffic as the semantic anchor and the decoupling of tunnel information. By correlating each tunnel flow with its corresponding semantic-shared TLS flow, DecETT provides richer app-specific information than simple label-based approaches. This information is particularly important for short flows, which are easier to suffer from insufficient feature extraction due to their limited lengths. Additionally, the decoupling of tunnel features further mitigates the negative impact caused by tunnel mechanism. Therefore, DecETT can be effectively utilized in AF scenarios that are sensitive to short flows, such as gambling activity detection[12].

5.3.3 Visualization. In addition to the above quantitative evaluations, we conduct a qualitative visualization to further discuss the performance of DecETT. Figure 5 shows the t-SNE[32] visualization of random 5 app fingerprints learned by FS-Net and DecETT under V2Ray, respectively. It can be observed that DecETT enables a more significant aggregation of fingerprints from the same app compared to FS-Net while reducing the overlapping area of fingerprints from different apps, thereby achieving better AF results.

# 5.4 Analysis of AF Results Under Mixed-Tunnel

Evaluation in the previous section is conducted under a specific single tunnel. However, due to the diversity of encrypted tunnels, it is not always feasible to know the exact type of tunnel traffic in advance in real network environments. To address this issue, in this section, we further evaluate the AF performance of DecETT and comparison methods under mixed tunnels.

Table 2: Performance comparison results w.r.t. Accuracy, Precision, Recall and F1-score on mixed-tunnels. Bold represents the best and underline refers to the second. 

<table><tr><td></td><td>Method</td><td>Accuracy</td><td>Precision</td><td>Recall</td><td>F1-score</td></tr><tr><td>Statistic</td><td>AppScanner[30]</td><td>0.542</td><td>0.996</td><td>0.542</td><td>0.694</td></tr><tr><td>Server</td><td>FlowPrint[33]</td><td>0.075</td><td>0.015</td><td>0.075</td><td>0.023</td></tr><tr><td rowspan="2">Payload</td><td>ET-Bert[17]</td><td>0.102</td><td>0.126</td><td>0.107</td><td>0.099</td></tr><tr><td>YaTC[42]</td><td>0.601</td><td>0.652</td><td>0.601</td><td>0.603</td></tr><tr><td rowspan="3">Sequence</td><td>DF[29]</td><td>0.741</td><td>0.745</td><td>0.741</td><td>0.739</td></tr><tr><td>FS-Net[18]</td><td>0.785</td><td>0.790</td><td>0.785</td><td>0.786</td></tr><tr><td>GraphDApp[28]</td><td>0.656</td><td>0.661</td><td>0.656</td><td>0.650</td></tr><tr><td>Ours</td><td>DecETT</td><td>0.842</td><td>0.844</td><td>0.842</td><td>0.842</td></tr></table>

To conduct this evaluation, we first mix the flows of five encrypted tunnels, where flows generated by the same app share the same label, regardless of whether they are forwarded by the same encrypted tunnel. Each method is required to extract unified app fingerprints from the mixed tunnel traffic. Table 2 concludes the performance of DecETT and other comparison methods. As can be seen from the table, DecETT still outperforms all other baselines under mixed tunnels, achieving 84.2% on the four evaluation metrics. GraphDApp, which relies on burst division, shows significant performance degradation compared to the single-tunnel scenario. This may be due to the fact that different tunnels may employ different packet-sending strategies, thus leading to different burst division results. DF and FS-Net demonstrate relatively better stability, in which FS-Net achieves an F1-score of 78.6%. These results further highlight the superiority of DecETT. By decoupling the appirrelevant tunnel information from flow representations, DecETT enables the model to focus on learning unified app-specific representations across various tunnels, and further provides TLS traffic as the robust semantic anchor, thereby achieving more accurate app fingerprinting in real and complex network environments.

# 5.5 Ablation Study

To validate the effectiveness of DecETT, we conduct an ablation study by evaluating its variants, i.e., DecETT/SRC, DecETT/PSM, DecETT/CPD, DecETT/ASA, and DecETT/ASC, to indicate its superiority sufficiently. Figure 7 shows all results of the ablation study.

(1) After removing SRC, the performance of DecETT/SRC declines by 1% to 4% across 5 tunnels, which can be owing to the lack of constraints on decoupling features to fully retain the information in original flow sequences.   
(2) Compared to DecETT, both DecETT/PSM and DecETT/CPD show performance decreases, with average F1-score losses of 3.56% and 2.01%, respectively. These results further indicate that decoupling app-irrelevant tunnel features to lower their negative impact on fingerprint generation is essential for accurate AF under tunnels.   
(3) The removal of ASA has the most significant impact on DecETT compared with other components despite ASC, with a maximum F1-score drop of 9% under V2Ray. This result demonstrates the importance of stronger app-specific information provided by TLS traffic in accurate AF.

(4) After removing ASC, the performance of DecETT drops drastically, with a maximum F1-score of only 0.5%, highlighting the importance of label supervision in feature decoupling. Without app labels as supervisory signals, DecETT/ASC fails to distinguish useful semantic features for downstream fingerprinting task, resulting in meaningless feature decoupling.

(5) Our model performance gets worse by removing any key components, which proves that each of them contributes to the improvement in accurate AF under encrypted tunnels. Furthermore, the performance gaps between DecETT and its variants are further widened when confronting tunnels with more complex obfuscation, such as V2Ray, highlighting its powerful AF capability against tunnel mechanism.

# 5.6 Sensitivity Analysis

In this section, we perform sensitivity analysis on the critical hyperparameter in DecETT, the flow sequence length, which determines the amount of flow sequence information DecETT can utilize for fingerprint learning. In the experimental setup for this section, only the flow sequence length is varied, while all other parameters remain the same as previously described.

Figure 8 shows the results under five tunnels. From this figure, we can observe that: (1) DecETT maintains stable performance across different flow sequence lengths, consistently outperforming other comparison methods shown in Table 1; (2) DecETT still achieves remarkable performance even with relatively short flow sequence length (e.g., length=20), highlighting its strong capability in accurate fingerprint construction; (3) Excessively long flow sequences lead to performance decline. This can be attributed to that the later stages of flow transmission mainly focus on transmitting large amounts of data, resulting in packet length sequences with high similarity (e.g., numerous packets of MTU size). Overall, we thus conclude that DecETT is relatively insensitive to different flow sequence lengths, demonstrating its robustness to hyperparameter perturbations.

# 6 Conclusion

In this work, we propose DecETT, a dual decouple-based semantic enhancement method to achieve accurate app fingerprinting under encrypted tunnels. Considering the negative impact caused by re-encapsulation mechanism of encrypted tunnels on accurate fingerprint extraction, we first introduce TLS traffic as a relatively stronger and robust semantic anchor to enhance fingerprint learning, and further decouple the protocol features and app semantic features to reduce the impact of encrypted tunnels in fingerprint generation. Finally, the decoupled app semantic features are utilized for fingerprint generation and classification. Experiments under five representative encrypted tunnels indicate that DecETT outperforms state-of-the-art methods in accurate AF under encrypted tunnels by significant margins, and further demonstrates its superiority under tunnels with more complicated obfuscation.

# 7 Acknowledgments

This work was supported by the National Natural Science Foundation of China (Grant No. 62402492). We would also like to thank the anonymous reviewers for their valuable comments on improving this paper.

# References

[1] Haider Abbas, Naina Emmanuel, Muhammad Faisal Amjad, Tahreem Yaqoob, Mohammed Atiquzzaman, Zafar Iqbal, Narmeen Shafqat, Waleed Bin Shahid, Ali Tanveer, and Umer Ashfaq. 2023. Security assessment and evaluation of VPNs: a comprehensive survey. Comput. Surveys 55, 13s (2023), 1–47.   
[2] Alice, Bob, Carol, Jan Beznazwy, and Amir Houmansadr. 2020. How china detects and blocks shadowsocks. In Proceedings of the ACM Internet Measurement Conference. 111–124.   
[3] Ahmad Reda Alzighaibi. 2023. Detection of DoH Traffic Tunnels Using Deep Learning for Encrypted Traffic Classification. Computers 12, 3 (2023), 47.   
[4] Blake Anderson and David McGrew. 2017. Machine Learning for Encrypted Malware Traffic Classification: Accounting for Noisy Labels and Non-Stationarity. In Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining. Association for Computing Machinery, 1723–1732.   
[5] Blake Anderson and David McGrew. 2020. Accurate TLS fingerprinting using destination context and knowledge bases. arXiv preprint arXiv:2009.01939 (2020).   
[6] Kyunghyun Cho. 2014. Learning phrase representations using RNN encoderdecoder for statistical machine translation. arXiv preprint arXiv:1406.1078 (2014).   
[7] Sumit Chopra, Raia Hadsell, and Yann LeCun. 2005. Learning a similarity metric discriminatively, with application to face verification. In 2005 IEEE computer society conference on computer vision and pattern recognition (CVPR’05), Vol. 1. IEEE, 539–546.   
[8] Gerard Draper-Gil, Arash Habibi Lashkari, Mohammad Saiful Islam Mamun, and Ali A Ghorbani. 2016. Characterization of encrypted and vpn traffic using time-related. In Proceedings of the 2nd international conference on information systems security and privacy (ICISSP). 407–414.   
[9] Maurizio Dusi, Alice Este, Francesco Gringoli, and Luca Salgarelli. 2014. Identify ing the traffic of SSH-encrypted applications. (2014).   
[10] Anja Feldmann, Oliver Gasser, Franziska Lichtblau, Enric Pujol, Ingmar Poese, Christoph Dietzel, Daniel Wagner, Matthias Wichtlhuber, Juan Tapiador, Narseo Vallina-Rodriguez, et al. 2020. The lockdown effect: Implications of the COVID-19 pandemic on internet traffic. In Proceedings of the ACM internet measurement conference. 1–18.   
[11] Yaroslav Ganin and Victor Lempitsky. 2015. Unsupervised domain adaptation by backpropagation. In International conference on machine learning. PMLR, 1180– 1189.   
[12] Zheyuan Gu, Gaopeng Gou, Chang Liu, Chen Yang, Xiyuan Zhang, Zhen Li, and Gang Xiong. 2024. Let gambling hide nowhere: Detecting illegal mobile gambling apps via heterogeneous graph-based encrypted traffic analysis. Computer Networks 243 (2024), 110278.   
[13] Lulu Guo, Qianqiong Wu, Shengli Liu, Ming Duan, Huijie Li, and Jianwen Sun. 2020. Deep learning-based real-time VPN encrypted traffic identification methods. Journal of Real-Time Image Processing 17, 1 (2020), 103–114.   
[14] Liuyong He and Yijie Shi. 2018. Identification of SSH applications based on convolutional neural network. In Proceedings of the 2018 1st International Conference on Internet and e-Business. 198–201.   
[15] Minghao Jiang, Zhen Li, Peipei Fu, Wei Cai, Mingxin Cui, Gang Xiong, and Gaopeng Gou. 2022. Accurate mobile-app fingerprinting using flow-level relationship with graph neural networks. Computer Networks 217 (2022), 109309.   
[16] Danielle Lambion, Michael Josten, Femi Olumofin, and Martine De Cock. 2020. Malicious DNS tunneling detection in real-traffic DNS data. In 2020 IEEE International Conference on Big Data (Big Data). IEEE, 5736–5738.   
[17] Xinjie Lin, Gang Xiong, Gaopeng Gou, Zhen Li, Junzheng Shi, and Jing Yu. 2022. Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification. In Proceedings of the ACM Web Conference 2022. 633–642.   
[18] Chang Liu, Longtao He, Gang Xiong, Zigang Cao, and Zhen Li. 2019. Fs-net: A flow sequence network for encrypted traffic classification. In IEEE INFOCOM 2019-IEEE Conference On Computer Communications. IEEE, 1171–1179.   
[19] Sicai Lv, Chao Wang, Zibo Wang, Shuo Wang, Bailing Wang, and Yongzheng Zhang. 2023. AAE-DSVDD: A one-class classification model for VPN traffic identification. Computer Networks 236 (2023), 109990.   
[20] Fatemeh Marzani, Fatemeh Ghassemi, Zeynab Sabahi-Kaviani, Thijs Van Ede, and Maarten Van Steen. 2023. Mobile App Fingerprinting through Automata Learning and Machine Learning. In 2023 IFIP Networking Conference (IFIP Networking). IEEE, 1–9.   
[21] Yongwei Meng, Tao Qin, Haonian Wang, and Zhouguo Chen. 2022. TPIPD: A Robust Model for Online VPN Traffic Classification. In 2022 IEEE International Conference on Trust, Security and Privacy in Computing and Communications (TrustCom). IEEE, 105–110.   
[22] Rikima Mitsuhashi, Yong Jin, Katsuyoshi Iida, Takahiro Shinagawa, and Yoshiaki Takai. 2022. Malicious DNS tunnel tool recognition using persistent DoH traffic analysis. IEEE Transactions on Network and Service Management 20, 2 (2022), 2086–2095.   
[23] Rikima Mitsuhashi, Akihiro Satoh, Yong Jin, Katsuyoshi Iida, Takahiro Shinagawa, and Yoshiaki Takai. 2021. Identifying malicious dns tunnel tools from doh traffic using hierarchical machine learning classification. In Information Security: 24th International Conference, ISC 2021, Virtual Event, November 10–12, 2021,

Proceedings 24. Springer, 238–256.   
[24] Sanghak Oh, Minwook Lee, Hyunwoo Lee, Elisa Bertino, and Hyoungshick Kim. 2023. Appsniffer: Towards robust mobile app fingerprinting against VPN. In Proceedings of the ACM Web Conference 2023. 2318–2328.   
[25] Annapurna P Patil and Lalitha Chinmayee M Hurali. 2023. Discerning the traffic in anonymous communication networks using machine learning: concepts, techniques and future trends. International Journal of Information and Decision Sciences 15, 1 (2023), 94–115.   
[26] Thai-Dien Pham, Thien-Lac Ho, Tram Truong-Huu, Tien-Dung Cao, and Hong-Linh Truong. 2021. Mappgraph: Mobile-app classification on encrypted network traffic using deep graph convolution neural networks. In Proceedings of the 37th Annual Computer Security Applications Conference. 1025–1038.   
[27] Shadowsocks. 2024. Shadowsocks | A fast tunnel proxy that helps you bypass firewalls. https://shadowsocks.org/. Accessed: 2024-10-10.   
[28] Meng Shen, Jinpeng Zhang, Liehuang Zhu, Ke Xu, and Xiaojiang Du. 2021. Accurate decentralized application identification via encrypted traffic analysis using graph neural networks. IEEE Transactions on Information Forensics and Security 16 (2021), 2367–2380.   
[29] Payap Sirinam, Mohsen Imani, Marc Juarez, and Matthew Wright. 2018. Deep fingerprinting: Undermining website fingerprinting defenses with deep learning. In Proceedings of the 2018 ACM SIGSAC conference on computer and communications security. 1928–1943.   
[30] Vincent F Taylor, Riccardo Spolaor, Mauro Conti, and Ivan Martinovic. 2016. Appscanner: Automatic fingerprinting of smartphone apps from encrypted network traffic. In 2016 IEEE European Symposium on Security and Privacy (EuroS&P). IEEE, 439–454.   
[31] Project V. 2020. Project V·Project V Official. https://www.v2ray.com/en/index. html. Accessed: 2024-10-10.   
[32] Laurens Van der Maaten and Geoffrey Hinton. 2008. Visualizing data using t-SNE. Journal of machine learning research 9, 11 (2008).   
[33] Thijs Van Ede, Riccardo Bortolameotti, Andrea Continella, Jingjing Ren, Daniel J Dubois, Martina Lindorfer, David Choffnes, Maarten Van Steen, and Andreas Peter. 2020. Flowprint: Semi-supervised mobile-app fingerprinting on encrypted network traffic. In Network and distributed system security symposium (NDSS), Vol. 27.   
[34] Chenxu Wang, Jiangyi Yin, Zhao Li, Hongbo Xu, Zhongyi Zhang, and Qingyun Liu. 2024. Identifying VPN Servers through Graph-Represented Behaviors. In Proceedings of the ACM on Web Conference 2024. 1790–1799.   
[35] Suixing Wang, Chao Yang, Gang Guo, Mingzhe Chen, and Jianfeng Ma. 2022. SSAPPIDENTIFY: a robust system identifies application over Shadowsocks’s traffic. Computer Networks 203 (2022), 108659.   
[36] Wei Wang, Ming Zhu, Jinlin Wang, Xuewen Zeng, and Zhongzhen Yang. 2017. End-to-end encrypted traffic classification with one-dimensional convolution neural networks. In 2017 IEEE international conference on intelligence and security informatics (ISI). IEEE, 43–48.   
[37] Xin Wang, Shuhui Chen, and Jinshu Su. 2020. App-net: A hybrid neural network for encrypted mobile traffic classification. In IEEE INFOCOM 2020-IEEE Conference on Computer Communications Workshops (INFOCOM WKSHPS). IEEE, 424–429.   
[38] Xi Xiao, Wentao Xiao, Rui Li, Xiapu Luo, Haitao Zheng, and Shutao Xia. 2022. EB-SNN: Extended Byte Segment Neural Network for Network Traffic Classification. IEEE Transactions on Dependable and Secure Computing 19, 5 (2022), 3521–3538. doi:10.1109/TDSC.2021.3101311   
[39] Hongbo Xu, Shuhao Li, Zhenyu Cheng, Rui Qin, Jiang Xie, and Peishuai Sun. 2022. VT-GAT: A Novel VPN Encrypted Traffic Classification Model Based on Graph Attention Neural Network. In International Conference on Collaborative Computing: Networking, Applications and Worksharing. Springer, 437–456.   
[40] Diwen Xue, Reethika Ramesh, Arham Jain, Michaelis Kallitsis, J Alex Halderman, Jedidiah R Crandall, and Roya Ensafi. 2022. OpenVPN is open to VPN fingerprinting. Commun. ACM (2022).   
[41] Jingjing Zhao, Xuyang Jing, Zheng Yan, and Witold Pedrycz. 2021. Network traffic classification for data fusion: A survey. Information Fusion 72 (2021), 22–47.   
[42] Ruijie Zhao, Mingwei Zhan, Xianwen Deng, Yanhao Wang, Yijun Wang, Guan Gui, and Zhi Xue. 2023. Yet another traffic classifier: A masked autoencoder based traffic transformer with multi-level flow representation. In Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 37. 5420–5427.

# A Re-encapsulation Mechanism Illustration of Encrypted Tunnels

In section 3.2, we analyze the source code of the re-encapsulation mechanism summarized from Shadowsocks (shown in Figure 6) to illustrate the independence of tunnel features and app semantic features. In this section, we extend the discussion to the other four tunnels: ShadowsocksR, V2Ray, Trojan, and OpenVPN. Some of these tunnels are implemented by different programming languages, such as Go, C and C++, which are not as concise as Python used by Shadowsocks. As a result, the source code pipeline can be too lengthy to be fully presented in this paper. To this end, we provide a brief overview of the other four re-encapsulation mechanisms together with the corresponding source code link for interested readers.

# socket init and connection establishment
local_sock = TCPRelay.socket.accept()
remote_sock = create_remote_socket(server_ip, server_port)
# read raw data from local
data = local_sock.recv(BUF_SIZE)
# encrypte and send data
data = encryptor.encrypt(data)
write_to_sock(data, remote_sock)
# receive and decrypt data from remote
data = remote_sock.recv(BUF_SIZE)
data = encryptor.decrypt(data)
# send raw data to local
write_to_sock(data, local_sock)   
Figure 6: Source code of re-encapsulation mechanism summarized from Shadowsocks. Illustrations for the other 4 encrypted tunnels can be found in Appendix A.

In summary, the other four tunnels also forward data by maintaining two socket communications and their correlation. The core difference lies in the encryption algorithms and protocols used for re-encapsulation: (1) ShadowsocksR1 employs the same reencryption mechanism as Shadowsocks. (2) V2Ray2, on the other hand, uses closures requestDone() and responseDone() operations to implement the re-encapsulation mechanism, in which the encryption algorithms and encapsulation details follows its private protocol Vmess. (3) Trojan3 conceals its traffic characteristics using the standard SSL protocol, and applies the SSL mechanism in Boost.Asio for re-encapsulation of the forwarded data. (4) Open-VPN4 also implements its re-encapsulation mechanism based on OpenSSL protocol, while further developing its private protocol, OpenVPN, on top of OpenSSL.

Overall, the varied re-encapsulation mechanisms pose challenges to accurate app fingerprinting under encrypted tunnels. However, their reliance on socket communication underscores the generalizability and correctness of decouple-based AF methods across various encrypted tunnels.

# B Configurations of Five Encrypted Tunnels

Table 3 provides detailed configurations of the five encrypted tunnels used in our experiments. In the following, we illustrate each of the configurations in detail.

• Encrypted Algorithm(EA). Encrypted algorithm refers to the algorithm during the re-encryption of the forwarded traffic data. In our experiments, ShadowsocksR uses AES-256-CFB as the encrypted algorithm, while the other four tunnels use AES-256-GCM.   
• Protocol. Protocol refers to the specific communication protocol used by the encrypted tunnel, which determines the

way of data re-encapsulation and transmission between the tunnel client and tunnel server. Some encrypted tunnels use their specific private protocols, such as Origin used by ShadowsocksR, Vmess used by V2Ray, and OpenVPN protocol used by OpenVPN.

• Obfuscation(Obfs). Obfuscation refers to techniques used to disguise the existence of the encrypted tunnel by modifying the appearance of the traffic, making it harder to detect. Obfuscation can be achieved by altering packet characteristics or mimicking other types of traffic.   
• Notes. OpenVPN provides two different tunneling modes, TUN mode and TAP mode. TUN mode operates at the network layer and is designed for routing IP packets, while TAP mode operates at the data link layer, which emulates a virtual Ethernet adapter. Since we focus on the task of app fingerprinting, we choose TUN mode to implement OpenVPN, which is more suitable for this scenario.

Table 3: Detailed configurations of 5 encrypted tunnels in our evaluation. 

<table><tr><td>Tunnel</td><td>EA</td><td>Protocol</td><td>Obfs</td><td>Notes</td></tr><tr><td>Shadowsocks</td><td>AES-256-GCM</td><td>SOCKS</td><td>-</td><td>-</td></tr><tr><td>ShadowsocksR</td><td>AES-256-CFB</td><td>Origin</td><td>tls1.2_ticket_auth</td><td>-</td></tr><tr><td>V2Ray</td><td>AES-128-GCM</td><td>Vmess</td><td>-</td><td></td></tr><tr><td>Trojan</td><td>AES-128-GCM</td><td>HTTPS</td><td>-</td><td>-</td></tr><tr><td>OpenVPN</td><td>AES-128-GCM</td><td>OpenVPN</td><td>-</td><td>TUN Mode</td></tr></table>

# C Detailed Information of Datasets

Table 4 illustrates the detailed information of the used five datasets for experimental evaluation.

Table 4: Details of 5 evaluation datasets. TLP refers to the abbreviation of Transport Layer Protocol used by the corresponding tunnel protocol. 

<table><tr><td>Dataset</td><td>TLP</td><td>#Apps</td><td>#Flows</td><td>#Payloads</td></tr><tr><td>Shadowsocks</td><td>TCP</td><td>54</td><td>346,388</td><td>29.70G</td></tr><tr><td>ShadowsocksR</td><td>TCP</td><td>54</td><td>346,418</td><td>22.78G</td></tr><tr><td>V2Ray</td><td>TCP</td><td>54</td><td>339,667</td><td>23.28G</td></tr><tr><td>Trojan</td><td>TCP</td><td>54</td><td>346,378</td><td>29.13G</td></tr><tr><td>OpenVPN</td><td>UDP</td><td>54</td><td>346,296</td><td>28.14G</td></tr></table>

# D Implementation Details

We conduct our evaluation on a server with two Intel(R) Xeon(R) Gold 6240R CPU @2.40 GHz processors, Ubuntu 20.04, 64GB RAM. An NVIDIA Tesla A800 GPU with 80GB VRAM is used to accelerate the computations. Our method is implemented based on Python 3.8.16 and PyTorch 1.12.1+cu113. As for the hyper-parameters, we set the mini-batch size as 256, the hidden size of GRU as 128, the embedding size as 3000, the flow sequence length as 200, and the five loss weights $\lambda _ { i }$ as 1. For all the baselines, we follow their official implementations.

![](images/71ffb867f80ce5924f3a54a827c4d297b2e3990a396bf9e3fcbe8ffc11487de4.jpg)

<details>
<summary>bar_line</summary>

| Dataset | DecETT/SRC | DecETT/PSM | DecETT/CPD | DecETT/ASA | DecETT/ASC | DecETT | F1-Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| SS | 0.92 | 0.92 | 0.92 | 0.92 | 0.015 | 0.93 | 0.92 |
| SSR | 0.93 | 0.93 | 0.93 | 0.93 | 0.035 | 0.945 | 0.93 |
| Vmess | 0.735 | 0.65 | 0.745 | 0.725 | 0.015 | 0.825 | 0.82 |
| Trojan | 0.915 | 0.915 | 0.915 | 0.915 | 0.015 | 0.93 | 0.92 |
| OpenVPN | 0.93 | 0.93 | 0.93 | 0.93 | 0.015 | 0.945 | 0.93 |
</details>

Figure 7: Ablation study results of key components in DecETT w.r.t. Accuracy and F1-score on 5 tunnel datasets.

Table 5: Full list of the mobile apps. 

<table><tr><td>No.</td><td>Package Name</td><td>No.</td><td>Package Name</td></tr><tr><td>1</td><td>air.tv.douyu.android</td><td>28</td><td>com.snapchat.android</td></tr><tr><td>2</td><td>cn.xdf.woxue.student</td><td>29</td><td>com.sohu.sohuvideo</td></tr><tr><td>3</td><td>com.amazon.mShop.android(shopping</td><td>30</td><td>com.ss.android.article.video</td></tr><tr><td>4</td><td>com.bilibili.app.in</td><td>31</td><td>com.ss.android.ugc.aweme</td></tr><tr><td>5</td><td>com.bilibili.comic</td><td>32</td><td>com.ss.android.ugc.trill</td></tr><tr><td>6</td><td>com.bittorrent.client</td><td>33</td><td>com.talk51.international</td></tr><tr><td>7</td><td>com.duowan.kiwi</td><td>34</td><td>com.taobao.idlefish</td></tr><tr><td>8</td><td>com.duowan.mobile</td><td>35</td><td>com.taobao.live</td></tr><tr><td>9</td><td>com.facebook.katana</td><td>36</td><td>com.taobao.taobao</td></tr><tr><td>10</td><td>com.google.android.youtube</td><td>37</td><td>com.tencent.androidqqmail</td></tr><tr><td>11</td><td>com.huajiao</td><td>38</td><td>com.tencent.mm</td></tr><tr><td>12</td><td>com.hunantv.imgo.activity</td><td>39</td><td>com.tencent.mobileqq</td></tr><tr><td>13</td><td>com.larksuite.suite</td><td>40</td><td>com.tencent.qqlive</td></tr><tr><td>14</td><td>com.meelive.ingkee</td><td>41</td><td>com.tencent.qqmusic</td></tr><tr><td>15</td><td>com.mogujie</td><td>42</td><td>com.tencent.weread</td></tr><tr><td>16</td><td>com.netease.cc</td><td>43</td><td>com.tmall.wireless</td></tr><tr><td>17</td><td>com.netease.edu.study</td><td>44</td><td>com.vipkid.ark.international.parent</td></tr><tr><td>18</td><td>com.nhn.android.nmap</td><td>45</td><td>com.xes.jazhanghui.activity</td></tr><tr><td>19</td><td>com.periscope.pscp</td><td>46</td><td>com.xiaomi.shop</td></tr><tr><td>20</td><td>com.pplive.androidphone</td><td>47</td><td>com.xingin.xhs</td></tr><tr><td>21</td><td>com.qihoo360.mobilesafe</td><td>48</td><td>com.xunlei.downloadprovider</td></tr><tr><td>22</td><td>com.qiyi.video</td><td>49</td><td>com.xunmeng.pinduoduo</td></tr><tr><td>23</td><td>com.sdu.didi.psnger</td><td>50</td><td>com.yandex.browser</td></tr><tr><td>24</td><td>com.shanbay.sentence</td><td>51</td><td>com.youku.phone</td></tr><tr><td>25</td><td>com.sina.weibo</td><td>52</td><td>com.zhihu.android</td></tr><tr><td>26</td><td>com.skype.raider</td><td>53</td><td>me.ele</td></tr><tr><td>27</td><td>com.smile.gifmaker</td><td>54</td><td>ru.ok.android</td></tr></table>

![](images/72b8d69320c9c7cc626ece24686b7f6c7059280b2e75e58ab1209501bcf1e0b4.jpg)

<details>
<summary>line</summary>

| Model | Accuracy | F1-score |
|---|---|---|
| Shadowsocks | 0.92 | 0.92 |
| ShadowsocksR | 0.94 | 0.94 |
| V2Ray | 0.79 | 0.80 |
| Trojan | 0.92 | 0.92 |
| OpenVPN | 0.88 | 0.88 |
</details>

Figure 8: Sensitivity analysis of DecETT with different flow sequence lengths on 5 tunnel datasets.

# E Results of Ablation Study and Sensitivity Analysis

Due to the page limits, we move the results of the ablation study (see Figure 7) and sensitivity analysis (see Figure 8) to the appendix section. The detailed analysis of these two experiments can be found in Section 5.5 and Section 5.6, respectively.

# F Full List of Mobile Apps

We provide a full list of 54 mobile apps selected in our experiments (see Table 5). The selection criteria for these apps primarily falls into the following three aspects:

(1) The scale of target audiences (i.e., popularity), such as Facebook and YouTube, which are popular worldwide; and WeChat and QQ, which have a huge number of users in China.   
(2) The provided service types, including streaming, social media, VoIP, online shopping, online education, etc., to cover as many daily usage scenarios as possible within a limited range of apps.   
(3) Real-world demand to be used under tunnels. For example, Facebook and YouTube, which are regionally restricted, and MangoTV and TikTok, which face copyright restrictions in different countries, are more likely to be accessed through encrypted tunnels.
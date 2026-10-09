# Mitigating Proxy-Induced Traffic Drift in Website Fingerprinting via Model-Agnostic Traffic Tailoring

Linxiao Yu<sup>∗†</sup>, Tianyu Cui<sup>†</sup>, Xinhao Deng<sup>‡</sup>, Yuqi Qing<sup>‡</sup>, Jun Tao<sup>∗†</sup>, Ke Xu<sup>§†</sup>, Qi Li<sup>‡†</sup>

<sup>∗</sup>School of Cyber Science and Engineering, Southeast University, <sup>†</sup>Zhongguancun Laboratory

<sup>‡</sup>Institute for Network Sciences and Cyberspace, Tsinghua University

<sup>§</sup>Department of Computer Science and Technology, Tsinghua University

Emails: {yulinxiaoybbb, juntao}@seu.edu.cn, cuity@zgclab.edu.cn, qyq21@mails.tsinghua.edu.cn {dengxinhao, xuke, qli01}@tsinghua.edu.cn

Abstract—Website fingerprinting (WF) based on deep learning can effectively identify websites from encrypted traffic. However, users often rely on proxy protocols to bypass censorship, and the diversity of these protocols poses a major challenge, as WF models trained on traffic from one set of protocols perform poorly when evaluated on that from unseen protocols. We attribute this issue to proxy-induced feature drift, where traffic patterns of the same website vary with the proxy protocol, leading to discrepancies that WF models fail to capture and severe performance degradation. To tackle this issue, we propose PA3, a modelagnostic preprocessing framework to analyze and mitigate the proxy-induced drift. PA3 first fingerprints the protocol-specific drift. These fingerprints are then used to tailor the proxied traffic for feature alignment, which mitigates the drift and considerably improves the generalization of WF models on traffic from unseen protocols. Extensive evaluations demonstrate that PA3 substantially enhances generalization on unseen protocols with an average improvement of 0.12 in F1-score (roughly 27% relative), achieving up to a 0.41 absolute gain across models, which narrows the performance gap introduced by the drift. In the best case, PA3 enables WF models to obtain F1-scores above 0.96 on traffic from unseen protocols.

Index Terms—Website fingerprinting, proxy protocol analysis, traffic drift

## I. INTRODUCTION

The recent decades have witnessed the regulation and censorship on the Internet across multiple countries, which aim to monitor or block user activities deemed improper [1], [2], such as sending sensitive content or accessing restricted websites. Common censorship techniques include website blocking [3], [4] and DNS redirection [5]. In reaction to the surveillance, proxy techniques have been developed to bypass such restrictions [2]. Users typically resort to a proxy client and server to encapsulate original traffic into proxied traffic. A proxy protocol specifies how the client communicates with the server, often obfuscating the traffic to evade inspection. Despite the obfuscation, the proxied traffic still leaks informative features. For example, censors can locate the TLS handshake prologue via packet sizes [1], or exploit RTT discrepancies across layers [2] to detect proxy usage. Additionally, active probing techniques allow censors to even identify the specific proxy protocol in use [6]–[8].

To analyze user behavior at a finer granularity, the adversaries have proposed Website Fingerprinting (WF) [9], which infers the visited websites from encrypted traffic by leveraging traffic pattern discrepancies. With the rise of deep learning (DL), numerous studies [10]–[15] have demonstrated over 95% accuracy in website identification. Recent works have also shown that WF can remain effective on the proxied traffic [16]–[18].

Most existing WF works implicitly rely on a protocol consistency assumption that the same set of proxy protocols appears in both training and testing traffic datasets. In practice, however, users might freely switch among diverse proxy protocols (e.g., VMess, Shadowsocks, Trojan), and a model trained on one protocol may encounter traffic from a completely different one at test time. We find that this mismatch causes severe performance degradation. Models tend to learn and compress protocol-specific communication patterns (e.g., handshake sequence pattern) that are shared across all training samples, since such commonality provides little discriminative information for distinguishing websites [19], [20]. When the testing traffic uses an unseen protocol with different such patterns, the learned compression no longer applies, leading the model to incorrectly process the test features and suffer substantial accuracy loss.

Our key observation is that proxy-induced drift originates from the extra bytes inserted by proxy protocols for encryption and proxy-layer communication. These bytes are irrelevant to website identity, yet they perturb the packet sizes and segmentation patterns observed by WF models. Moreover, proxy software handles each connection independently, which means that the drift is introduced at the flow level, while a website trace is only a mixture of multiple concurrent flows. Therefore, the intuition is to remove these extraneous bytes from each flow to align the traffic in the testing set with that in the training set. In other words, we tailor the traffic to make the protocol consistency assumption feasible.

Directly removing these irrelevant bytes is infeasible in practice because the user traffic available during the actual WF attack is encrypted. We therefore propose PA3<sup>1</sup> to remove the packets carrying such bytes to implicitly achieve bytelevel alignment. PA3 works with a two-phase strategy: (i) Structural fingerprinting of proxied traffic: It generates the decrypted probe traffic for each proxy protocol in a controlled environment. It then performs a payload-aware comparison of same-website traffic across protocols and records the discrepant packets as protocol-specific drift fingerprints. (ii) Traffic tailoring for drift mitigation: PA3 compiles modelagnostic rules based on payload-agnostic packet metadata from fingerprints to tailor encrypted traffic, thereby indirectly removing irrelevant bytes. When performing a WF attack, the adversary eavesdrops the user traffic, where decryption is no longer available. She applies the tailoring rules for traffic feature alignment, which effectively mitigates the proxy-layer distortions to improve the WF generalization on traffic from unseen protocols. Our main contributions are threefold.

TABLE I: Overview of proxy protocol usage by proxy service providers. indicates protocols currently in use, indicates protocols that were formerly used, and  indicates protocols that have never been used by the providers.

<table><tr><td></td><td>WgetCloud</td><td>SS ONE</td><td>Youxin Cloud</td><td>CLM</td><td>STC-Server</td><td>RioLU.443</td><td>DoggyGo</td><td>Nexitally</td><td>Erwan Cloud</td><td>JustMySocks</td></tr><tr><td>Trojan</td><td>●</td><td>○</td><td>●</td><td>➀</td><td>○</td><td>●</td><td>○</td><td>➁</td><td>○</td><td>○</td></tr><tr><td>VMess</td><td>➁</td><td>●</td><td>○</td><td>○</td><td>●</td><td>○</td><td>○</td><td>○</td><td>●</td><td>●</td></tr><tr><td>Shadowsocks</td><td>➁</td><td>●</td><td>○</td><td>●</td><td>○</td><td>●</td><td>●</td><td>●</td><td>●</td><td>●</td></tr><tr><td>VLess</td><td>○</td><td>○</td><td>○</td><td>○</td><td>○</td><td>●</td><td>○</td><td>○</td><td>○</td><td>○</td></tr><tr><td>hy2</td><td>○</td><td>○</td><td>○</td><td>○</td><td>○</td><td>➁</td><td>●</td><td>○</td><td>○</td><td>○</td></tr><tr><td>ShadowsocksR</td><td>➁</td><td>○</td><td>○</td><td>○</td><td>●</td><td>○</td><td>○</td><td>○</td><td>○</td><td>○</td></tr></table>

• We conduct the first study on the ground truth of the proxyinduced drift in a payload-aware way, which reveals that the proxies affect traffic characteristics heterogeneously at each stage of the proxied website visit lifecycle;

• We propose model-agnostic methods to tailor the fully encrypted proxied traffic for proxy-induced drift mitigation. Crucially, they operate entirely at the preprocessing stage, requiring no changes to the model architecture and thus enabling plug-and-play integration with existing WF models;

• We collect a proxied website traffic dataset using commercial proxy services, and extensive evaluations demonstrate that PA3 substantially outperforms existing drift-mitigating methods. Across 6 state-of-the-art WF models, PA3 improves the F1-score by 0.12 on average (27% relative) over the unmitigated baseline and achieves up to a 0.41 absolute gain. In the best case, the WF model obtains F1-scores above 0.96 on traces from unseen proxy protocols.

The source code of PA3 and all the datasets are available at https://github.com/wesly2000/PA3.

## II. RELATED WORK

Website Fingerprinting Attack. Website fingerprinting captures the traffic feature discrepancies, which encode the uniqueness of website resources, e.g., images and videos, to classify the websites even when the traffic is encrypted [22]. With the flourishing of deep learning (DL), researchers began to adopt DL models in WF analysis [9], [23], which achieved significant success in classification accuracy and scale [14]. Previous works have demonstrated the strength of DL-based WF, which could precisely classify the websites from HTTPS [22], [24]–[26] or Tor traffic [10], [11], [13], [14], by automatically extracting high-level representations from simple traffic features like packet direction. Even when obfuscation is applied, recent WF works show considerable potential in breaking these safeguards [27], [28].

![](images/0eba1240d1992ab7943f820806cb45de1611c65c9be8e84c26d1040b2d752cd4.jpg)  
Fig. 1: The threat model for fingerprinting proxied traffic.

Proxy-Based Censorship Evasion. Internet censorship techniques, such as website blocking [3], [4] and DNS redirection [5], have motivated the development of proxy techniques that encapsulate user traffic to evade inspection [2]. A variety of proxy protocols have emerged, including Trojan, VMess (V2Ray), Shadowsocks, VLess, and Hysteria 2 (hy2). We survey 10 popular commercial proxy service providers in Table I, and select the three most commonly deployed protocols— VMess, Shadowsocks, and Trojan—for this work. Despite the obfuscation these protocols provide, censors can still detect proxy usage [1], [2], [6]–[8]. Assuming the role of the censors, recent works start to apply WF techniques on proxied traffic for a more fine-grained traffic analysis, i.e., to identify the specific websites requested with proxy protocols [16]–[18].

Traffic Drift in WF. WF performance can deteriorate because of changes in network conditions [29], [30], HTTP versions [25], website content [11], etc. For proxied traffic, the drift comes from the variety of the proxy protocols used, where the protocol consistency assumption is often violated. To tackle this issue, [18] proposes the first framework to select the optimal feature set that is robust to this drift. However, its features depend on both the selected websites and access to protocols in the testing dataset, producing substantial variation across common-set selections. Moreover, it means that the features used in WF are not website-independent, limiting its generalizability. In contrast, PA3 learns website-independent protocol characteristics and does not require WF models to access traces from protocols in the testing dataset.

## III. THREAT MODEL

Given a set of monitored websites W, users may access them using protocols from the set $P ~ = ~ \{ P _ { 1 } , . . . , P _ { k } ,$ $P _ { k + 1 } , . . . , P _ { k + r } \}$ . For simplicity, we use NoProxy as a protocol to represent the case when no proxy is used. Let $P _ { \mathrm { t r a i n } } ~ =$ $\{ P _ { 1 } , . . . , P _ { k } \}$ be the set of protocols whose traffic is available during training, and $P _ { \mathrm { t e s t } } = \{ P _ { k + 1 } , . . . , P _ { k + r } \}$ be the set of protocols only occurring in the testing traffic. Visiting websites in W using protocols in $P$ generates a traffic dataset $D =$ $\{ D _ { 1 } , . . . , D _ { k + r } \}$ , where $D _ { i }$ represents traffic to W proxied by protocol $P _ { i }$ . Accordingly, we define $D _ { \mathrm { t r a i n } } = \{ D _ { 1 } , . . . , D _ { k } \}$ and $D _ { \mathrm { t e s t } } = \{ D _ { k + 1 } , . . . , D _ { k + r } \}$ to represent training and testing datasets, respectively. We assume $P _ { \mathrm { t r a i n } } \cap P _ { \mathrm { t e s t } } = \emptyset$ , i.e., the model has no access to $P _ { \mathrm { t e s t } }$ traffic during training.

![](images/8f858bc8fc9a223688ed2007de44f77737f25f952c0866dbcd6e89c5f77190ac.jpg)  
Fig. 2: Overview of our methodology. In the knowledge extraction phase, the adversary collects decrypted probe traffic to structurally fingerprint proxied traffic and derive traffic tailoring knowledge. In the knowledge application phase, the adversary applies the learned knowledge to encrypted target traffic and feeds the tailored traces to existing WF models.

The adversary trains a WF model on $D _ { \mathrm { t r a i n } }$ and seeks to improve its generalization to $D _ { \mathrm { t e s t } }$ . She generates a small amount of controlled, decryptable probe traffic to learn protocolspecific tailoring knowledge. During the attack, however, she can only passively observe encrypted traffic between the proxy client and server. Because the incoming protocol is unknown, she first identifies it using prior protocol knowledge and then applies the corresponding payload-agnostic tailoring rules.

## IV. METHODOLOGY

## A. Overall Framework

We develop PA3, which extracts knowledge from the fingerprints of the protocol-specific drift, and applies the knowledge to tailor the flows for drift mitigation. The intuition behind PA3 is that proxy-induced drift originates from the extra bytes introduced for proxy-layer communication. Therefore, we could remove the packets carrying these bytes to indirectly remove them for drift mitigation. We present the framework overview in Fig. 2. PA3 consists of two phases:

Structural Fingerprinting of Proxied Traffic: For a given stage in the proxied website visit lifecycle, the packets carrying the extra bytes of different proxy protocols expose protocol-specific patterns. Such regularity allows us to extract stage-specific structural fingerprints for each protocol. The proxy-layer encryption hides the semantic information of each packet. Therefore, we collect a small amount of controlled probe traffic for each proxy protocol, which is decrypted and parsed using the toolchain we developed to build the ground truth on which packets carry the extra bytes. The extracted fingerprints are converted to traffic tailoring knowledge which is applicable when the traffic is encrypted.

Traffic Tailoring for Drift Mitigation: In this phase, PA3 applies the traffic tailoring knowledge extracted from the previous phase to encrypted target traffic, where payload inspection is no longer available. PA3 scans through each flow to compute the likelihood that the packet sequence matches the patterns in the knowledge. Once the likelihood exceeds some threshold, PA3 marks these packets as the ones that carry extra bytes and strips them from the flow. The drift would be mitigated after all flows are tailored, and the WF model would obtain better generalization on the tailored traffic.

## B. Structural Fingerprinting of Proxied Traffic

Structural fingerprinting explains how each lifecycle stage is distorted by the proxy layer. We generate a small amount of controlled probe traffic, record the decryption keys, and compare flows to the same hostname across proxy protocols. This payload-aware comparison isolates proxy-induced effects from ordinary noise such as network congestion, retransmissions, and flow interleaving. The goal is not to use decrypted information during the real WF attack, but to turn the observations into payload-agnostic knowledge that can later be applied to encrypted traces.

Background Flow Fingerprinting. When visiting a website, the browser determines not only the hostnames associated with the target website, but also a set of browser-specific service domains used for auto-update checks, security verification, telemetry, and similar tasks. We refer to these background domains as Browser Intrinsic Hostnames (BIHs). For example, Firefox periodically requests content-signature-2. cdn.mozilla.net to retrieve certificate-chain information for Mozilla service data [31]. Although BIH flows carry no website-discriminative information, proxy-layer overhead shifts their sizes in protocol-specific ways, turning them into protocol-dependent noise that exacerbates cross-protocol feature drift. We therefore need to identify and filter BIH flows.

![](images/af0bae0f13581a40c8b1f78d2580656139c44313c0e9aa75e55b942873f2a810.jpg)  
Fig. 3: BIH flow size statistics. Each row shows the size histograms of the same hostname under different proxy protocols.

![](images/2cbdbbcc462ea014f9dd40b93449877e0dc8f9fffd5dbfb2f582cb7ae8f36bde.jpg)  
Fig. 4: BIH and website flow size distributions. Most of the website flows have sizes between 0 ∼ 30 KB, and the zoomed views show that the BIH flows have different modes from the website flows within this range.

Because BIH flows perform stable background tasks, their sizes concentrate around protocol-specific modes. Fig. 3 shows that these modes form sharp peaks, which provide fingerprints for identifying background flows and enable size-matched flow filtering. We also compare BIH flow sizes with website flow sizes. Fig. 4 shows that many website flows fall within the 0 ∼ 30KB range, where BIH flows may also appear. Therefore, background flow tailoring must balance BIH removal against preservation of website flows. BIH flows at larger sizes overlap less with website flows and are less risky to filter.

Knowledge I: Background flows in the proxied traffic form protocol-specific flow-size modes, enabling their identification and filtering through size matching.

Proxy Handshake Fingerprinting. Before connecting to the target web server, the proxy client first establishes communication with the proxy server, and the inner TLS handshake with the web server follows. This delays the TLS handshake by inserting a proxy handshake packet sequence before it. Since each proxy protocol follows its own handshake procedure, the delay is protocol-specific.

![](images/9297c20bf32748409c8fc6fa567fa389239b34a6814dde7ff335405ea1a3cf72.jpg)  
Fig. 5: Distribution of intra-flow packet indices of TLS Client Hello and Server Hello.

To quantify this effect, we record the intra-flow packet indices of TLS Client Hello and Server Hello across flows. Fig. 5 shows how proxy protocols delay both packets compared with the NoProxy case, and that the indices concentrate around protocol-specific modes. Client Hello is especially stable, while Server Hello has slightly more variation because that other packets may appear between Client Hello and Server Hello, like the delayed TCP ACK [32] packets triggered by the proxy handshake packets. This concentration indicates that proxy handshake packets form a consecutive anomalous subsequence near the beginning of each flow. The structural regularity of these packet sequences makes them suitable for sequence-based fingerprinting and later packet trimming.

Knowledge II: Proxy handshakes form protocol-specific directional packet-size patterns near the beginning of each flow, which can guide sequence-based packet trimming.

Proxy Overhead Fingerprinting. After connection establishment, website resources are carried through the proxy tunnel. The proxy layer appends headers and encryption tags to proxied data units, so the payloads passed to TCP are proxyencapsulated payloads rather than the original TLS payloads. This changes TCP segmentation throughout the flow, which means the drift is distributed rather than localized in removable packets. To fingerprint this distributed overhead, we construct the Byte-Segment Map (BSM) structure. BSM(i) returns the intra-flow index of the TCP segment containing the i-th HTTP byte in a flow. For the same hostname, comparing the BSMs generated under different protocols reveals how the same upper-layer bytes are segmented into TCP packets.

Fig. 6 (a)-(b) show the BSMs for short flows to highlight local changes. The starting points of proxied flows are slightly higher than those of NoProxy flows because of the additional proxy handshake. The occasional vertical jumps are caused by TCP ACK packets, which acknowledge the reception of the data but carry no HTTP bytes, thus the byte index remains fixed while the segment index advances. Fig. 6 (c)-(d) show the BSMs for long flows. This large-scale view reveals that the accumulated proxy overhead during content transmission leads to steeper lines than for NoProxy. These extra bytes are encapsulated into the TCP payloads, so the same HTTP bytes require more TCP segments. The slopes also differ across protocols because of different header formats and encryption strategies. Fig. 7 summarizes the ratio between BSM slopes of protocol pairs. For protocols $P _ { 1 }$ and $P _ { 2 } ,$ we denote the slope ratio as $\lambda _ { P _ { 2 } } ^ { P _ { 1 } }$ . Although the ratio varies across hostnames because of different chunking strategies [33], the low mean squared error (MSE) suggests that the ratios concentrate in a narrow band. It means that the slope ratio is a useful statistical description of inter-protocol segmentation drift and motivates the burst-size rescaling method during traffic tailoring.

![](images/eae9d23fa2a8bec51707c437a83cfc505c422a451968f5333f3084fed7a63e63.jpg)  
Fig. 6: BSMs of HTTP and TCP for several hostnames, which depict how the TCP segmentation of the HTTP contents differs across proxy protocols.

![](images/99ff4810d23c55ddc3bf24ebb713e37b6118ee01ba0884e0d738a8ba1da84bab.jpg)  
Fig. 7: Ratio of slopes between BSMs of different protocols.

Knowledge III: Proxy overhead makes each flow inflate at a protocol-specific ratio, which can be used to rescale intra-flow bursts for protocol-specific overhead alignment.

## C. Traffic Tailoring for Drift Mitigation

Proxy protocols distort traffic at each stage of the website visit lifecycle. These distortions all arise from extraneous bytes injected by the proxy layer for encryption and communication. Mitigating these impacts therefore reduces to eliminating these bytes. However, since proxy protocols encrypt their payloads, directly locating and stripping these bytes from the eavesdropped traffic is infeasible. Therefore, we tailor the encrypted target traffic using the knowledge learned from decrypted probe traffic, which leverages only flow sizes, packet positions, and directional packet sizes. This metadata is observable despite encryption, which makes drift mitigation practical in the real-world scenario.

Background Flow Tailoring. We empirically remove BIH flows by matching flow sizes against the BIH flow size modes. The main design choice is the filter coverage threshold $\alpha ,$ i.e., the fraction of the BIH flow-size histogram covered by the filter. A small α leaves many BIH flows unfiltered, whereas a large α risks removing website flows whose sizes overlap with BIH flows. We therefore design the scoring function

$$
U (\alpha) = (1 + \beta) \frac {C _ {f i l t} \cdot C _ {r e}}{\beta C _ {f i l t} + C _ {r e}},\tag{1}
$$

to select α by balancing the proportions of filtered BIH flows and retained website flows, where $C _ { f i l t }$ is the proportion of BIH flows filtered and $C _ { r e }$ is the proportion of website flows retained under $\alpha .$ The weight β controls how the score prioritizes BIH flow removal against website flow preservation. We choose the protocol-specific optimal $\alpha ^ { * }$ maximizing $U ( \alpha )$

Since different proxy protocols may yield different $\alpha ^ { * }$ values, applying each protocol’s optimum independently can leave different amounts of BIH noise in different protocols and introduce a new cross-protocol mismatch. To keep the remaining background flow distribution aligned, we use the shared threshold $\alpha _ { o p t } = \operatorname* { m i n } \{ \alpha _ { 1 } ^ { * } , \alpha _ { 2 } ^ { * } , \ldots , \alpha _ { n } ^ { * } \}$ across n protocols. Given an $\alpha _ { o p t } .$ , we sort the BIH histogram bins from the highest bar to the lowest and include bins in that order until the selected bins occupy $\alpha _ { o p t }$ of the whole histogram. The resulting union of bins is the filter, and any flow whose size falls into this scope will be removed.

Proxy Handshake Tailoring. To detect and trim the anomalous packet sequence introduced during proxy handshake, we represent each flow as a sequence of directional packet sizes and apply an n-gram approach [34] for proxy handshake detection. A sliding window is marked anomalous if it matches patterns learned from proxy handshake sequences in the probe traffic. Consecutive anomalous windows are merged, and the corresponding packets are removed from the flow. Because the proxy handshake region appears near the beginning of a flow, the search can be limited to the initial packets.

Packet sizes range over many possible values, so we discretize directional packet sizes before constructing the n-gram vocabulary. Given vocabulary size $v \ = \ | V | ,$ , we divide the range $\left[ - r , r \right]$ into v equal bins of width $\Delta = 2 r / v$ . Packet $p _ { i }$ with direction $d _ { i } \in \{ + 1 , - 1 \}$ and size $s _ { i }$ is mapped to

$$
Q _ {v} (p _ {i}) = d _ {i} \cdot \left\lfloor \frac {s _ {i}}{\Delta} \right\rfloor ,\tag{2}
$$

and window $W _ { i } = ( p _ { i } , \dots , p _ { i + k } )$ is represented as $Q _ { v } ( W _ { i } ) =$ $\big ( Q _ { v } ( p _ { i } ) , \dots , Q _ { v } ( p _ { i + k } ) \big )$ . The vocabulary size controls the trade-off between precision and recall. Smaller vocabularies conflate distinct patterns, while larger vocabularies increase miss rates. We select the optimal vocabulary size by maximizing the mutual-information objective

![](images/1bc3e967b1c0b8a141be673a2b0168f815928272128321994f2e064c8509662e.jpg)  
Fig. 8: Rescale the burst sizes according to the empirical ratio range, and re-insert ACK according to the empirical ACK frequency CDF.

$$
\begin{array}{c} {v ^ {*} = \arg \max J (v),} \\ {J (v) = I (Q _ {v} (W); Y) - \gamma \log v,} \end{array}\tag{3}
$$

where $Y \in \{ 0 , 1 \}$ indicates whether a window is anomalous, and $\gamma$ controls the penalty. After anomalous packet trimming, we perform SEQ-ACK analysis to remove ACK packets triggered by the proxy handshake. The same anomaly dictionaries also support proxy protocol identification. The flow-level protocol is the one whose dictionary matches the handshake pattern of the target flow. The session-level protocol, i.e., the protocol of the complete traffic from a single website visit, is determined by the majority voting of the flows within it.

Proxy Overhead Tailoring. Since the proxy headers and encryption tags are co-carried with website content, the overhead during content transmission is dispersed throughout the entire flow, and removing individual packets would discard useful website information. Instead, we treat the overhead as a burstscaling effect. Let $B _ { 1 }$ and $B _ { 2 }$ be burst sizes under protocols $P _ { 1 }$ and $P _ { 2 }$ for the same upper-layer content. The BSM slope ratio $\lambda _ { P _ { 2 } } ^ { P _ { 1 } }$ approximates the scaling relation

$$
B _ {1} \approx \lambda_ {P _ {2}} ^ {P _ {1}} \cdot B _ {2}.\tag{4}
$$

Fig. 8 illustrates the augmentation procedure. From the probe traffic, the adversary computes the mean $\mu _ { P _ { 2 } } ^ { P _ { 1 } }$ and standard deviation $\sigma _ { P _ { 2 } } ^ { P _ { 1 } }$ of the BSM slope ratios for each protocol pair. We model the scaling factor as a Gaussian random variable $\lambda \sim N ( \mu _ { P _ { 2 } } ^ { P _ { 1 } } , \sigma _ { P _ { 2 } } ^ { P _ { 1 } } )$ . During augmentation, the adversary samples λ and rescales each original burst $B _ { o r i g }$ to $B _ { a u g } = \lambda \cdot B _ { o r i g }$ . The rescaled burst is reconstructed into a valid packet sequence by filling packets up to TCP Maximum Segment Size (MSS) [35], with the final packet carrying any remainder. Timestamps are reconstructed by sampling interpacket delays from the empirical delay distribution of the original flow. Moreover, TCP ACKs often appear after every few data packets. Within a single flow, they divide packets in the same direction into small bursts, and directly rescaling these tiny bursts can create unrealistic packet sequences. We therefore remove ACK packets before burst rescaling, and then re-insert them back after rescaling according to the empirical ACK frequency of the original flow.

## V. EVALUATION

In this section, we evaluate how our mitigation methods improve WF generalization on unseen protocols.

![](images/c608afde0bd0a4da263eefaa75699dd2096a62a25be72cf8ae6825651d784930.jpg)  
Fig. 9: Performance of WF models trained with traffic from protocols in the training dataset $( P _ { \mathrm { t r a i n } } )$ , and tested on that from protocols in the testing dataset $( P _ { \mathrm { t e s t } } )$ . When $P _ { \mathrm { t r a i n } } \cap P _ { \mathrm { t e s t } } = \emptyset$ (off-diagonal cases), the performance deteriorates severely.

## A. Experiment Setup

Implementation. We prototype PA3 with more than 4,500 lines of C code to enable payload-aware analysis, and with more than 3,500 lines of Python code for drift mitigation. Selenium [36] and the modified Clash Core [37] are used to automate traffic and key material collection.

Dataset. Existing proxied traffic datasets for WF are either heavily processed into statistical features [16]–[18], leaving little space for our payload-aware analysis and flow-level processing, or remain private and difficult to obtain [1], [2]. Recognizing the importance of raw traffic for reproducible traffic analysis research, we collect our proxied traffic dataset with the corresponding key materials to facilitate future studies, which is released along with the PA3 repository. Specifically, we collect around 1 TB of traffic data from 80 websites using 4 protocols (NoProxy, VMess, Shadowsocks and Trojan) under diverse network settings.

• We use commercial proxy services rather than a laboratory deployment to collect more realistic proxied traffic. Moreover, we collect traffic through proxy servers in several regions, including Japan, Singapore, and the United States, to capture geographic diversity.

• We deploy 3 client machines across China and the United States. Two clients operate on university campus networks in China, while the third runs as a virtual machine in a U.S. region of a commercial cloud platform.

• To understand how the browser version affects the BIH flow size, besides the main dataset we collect another traffic dataset for proxy protocols using Firefox from 10 different versions, i.e., from version 132 (released in October 2024) to version 141 (released in July 2025) individually.

## B. Mitigating Protocol-specific Distortions

In this section, we apply our mitigation approaches proposed in Section IV-C to improve the model generalization. We consider the F1-score as the main performance metric. In this work, we evaluate 6 state-of-the-art WF models, namely,

TABLE II: Proxy protocol identification results.

<table><tr><td>Protocol</td><td>Flow-level Error Rate</td><td>Session-level Error Rate</td></tr><tr><td>VMess</td><td>0.255% (1,127/442,068)</td><td>0.005% (1/18,207)</td></tr><tr><td>Shadowsocks</td><td>0.587% (2,266/386,017)</td><td>0.000% (0/16,912)</td></tr><tr><td>Trojan</td><td>0.556% (2,269/408,340)</td><td>0.059% (10/16,823)</td></tr></table>

DF [9], BAPM [38], TF [39], NetCLR [10], TikTok [40], and RF [27], to validate consistent performance gains across different model architectures.

Performance Degradation on Unseen Protocols. First, we demonstrate in Fig. 9 how WF performance degrades when the model encounters traffic from unseen protocols. Let $P _ { \mathrm { t r a i n } }$ and $P _ { \mathrm { t e s t } }$ represent the protocols in the training and testing datasets, respectively. Along the diagonal of Fig. 9, where $P _ { \mathrm { t r a i n } } = P _ { \mathrm { t e s t } }$ all WF models achieve extremely high performance, with F1- scores above 0.94. In contrast, when $P _ { \mathrm { t r a i n } } \cap P _ { \mathrm { t e s t } } = \emptyset$ , the models suffer severe performance degradation. For example, the F1-score of DF drops below 0.56. Even relatively drifttolerant models such as TF and TikTok perform much worse than in the protocol-consistent setting. These results indicate that existing WF models cannot effectively handle the feature drift caused by proxy-protocol inconsistency.

Proxy Protocol Identification. Before applying protocolspecific tailoring knowledge, PA3 first identifies the proxy protocol used by each incoming trace. We leverage the ngram method to identify the proxy protocols. The anomalous patterns that the n-gram method learns are extracted from no more than 400 flows per protocol. The identification results are listed in Table II. In flow-level identification, fewer than 0.6% of samples are misclassified for all protocols. In session-level identification, i.e., the protocol identification of the complete traffic from a single website visit, a session consists of multiple flows, so we assign its protocol by majority vote over the flowlevel predictions. This aggregation is robust and reduces the session-level error rate to below 0.06% for every protocol. The high accuracy suggests that the mitigation methods could be applied to the proxied traffic reliably without introducing further distortions the traffic features.

Generalization Improvements. Now we apply PA3 for proxy-induced drift to achieve generalization improvement. For comparison, we consider 4 drift mitigating methods adopted in previous works:

• NetAugment [10]: It augments the traffic by manipulating the bursts to simulate the traffic from different network environments. It samples packet size and timestamps from historical CDFs to generate more realistic traces;

• DyWin [41]: DyWin applies window-level stochastic augmentation by masking, jittering, or preserving packet-count windows to simulate burst insertion, merging, and timestamp perturbation in various network conditions;

• Rosetta [29]: Rosetta is a TCP-aware augmentation method that simulates transport-level effects such as packet aggregation and packet loss.

• NetRandAugment [42]: It integrates multiple augmentation operators and samples from them randomly to make the training dataset more diverse for robustness enhancement.

![](images/dae3072b3f17e2781d49d3915b479cc60bc209b5fec162869a74dd4264d8387b.jpg)  
Fig. 10: The proportions of BIH flows filtered and website flows retained under different coverage thresholds α. We use the balance scoring function $U ( \alpha )$ to measure the tradeoff between the proportion of filtered BIH flows and that of website flows retained. The optimal $\alpha ^ { * }$ is the one that maximizes $U ( \alpha )$

![](images/b4d4a0ce20b47b5729693ff93ac63ed4731b2b8483466de6217a66f59ec54b6c.jpg)  
Fig. 11: The optimal vocabulary size $| V | ^ { * }$ for n-gram approach for each proxy protocol. When the MI objective function is optimized, the n-gram reaches the best performance.

We evaluate PA3 under different choices of $P _ { \mathrm { t r a i n } }$ and across multiple WF architectures to examine whether the improvement is tied to a specific training protocol or model design. Table III shows that PA3 consistently improves crossprotocol generalization over the unmitigated baseline for all evaluated WF models and all protocol pairs. The gains are especially pronounced for drift-sensitive models such as DF, BAPM, and NetCLR, while even more drift-tolerant models such as TF and TikTok still benefit from PA3. The standard deviations are generally small, indicating that the improvement is stable across repeated runs.

Compared with existing augmentation-based mitigation methods, PA3 achieves the best results in almost all settings, with only one exception for TikTok. This comparison suggests that generic traffic augmentation, which mainly simulates network- or transport-layer variations, is insufficient for proxylayer drift. In contrast, PA3 explicitly uses protocol-specific fingerprints of proxy-induced distortions to align traffic across protocols, which explains its stronger and more consistent generalization performance.

## C. Parameter Selection from Limited Probe Traffic

In practice, the amount of probe traffic should be as small as possible. We estimate parameters for the three tailoring modules from a small amount of probe traffic covering only five websites and accounting for 5% of the complete dataset. Once selected, these parameters are fixed for drift mitigation.

TABLE III: Performance comparison across WF models and mitigation methods, with standard deviations reported for stability. PA3 consistently improves cross-protocol generalization and outperforms existing mitigation methods in almost all settings.

<table><tr><td rowspan="2"> $P_{train}$ </td><td rowspan="2"> $P_{test}$ </td><td rowspan="2">Mitigation Method</td><td colspan="6">WF Attack Model</td></tr><tr><td>DF</td><td>BAPM</td><td>TF</td><td>NetCLR</td><td>TikTok</td><td>RF</td></tr><tr><td rowspan="12">VMess</td><td rowspan="6">Shadowsocks</td><td>Baseline</td><td>0.518 (±0.029)</td><td>0.382 (±0.007)</td><td>0.909 (±0.005)</td><td>0.332 (±0.011)</td><td>0.874 (±0.007)</td><td>0.634 (±0.006)</td></tr><tr><td>NetAugment</td><td>0.563 (±0.029)</td><td>0.339 (±0.008)</td><td>0.930 (±0.004)</td><td>0.430 (±0.013)</td><td>0.881 (±0.007)</td><td>0.649 (±0.005)</td></tr><tr><td>DyWin</td><td>0.587 (±0.030)</td><td>0.332 (±0.012)</td><td>0.925 (±0.002)</td><td>0.449 (±0.044)</td><td>0.873 (±0.007)</td><td>0.678 (±0.010)</td></tr><tr><td>NetRandAugment</td><td>0.634 (±0.015)</td><td>0.239 (±0.008)</td><td>0.922 (±0.003)</td><td>0.522 (±0.027)</td><td>0.886 (±0.005)</td><td>0.644 (±0.006)</td></tr><tr><td>Rosetta</td><td>0.589 (±0.038)</td><td>0.302 (±0.011)</td><td>0.927 (±0.002)</td><td>0.508 (±0.011)</td><td>0.876 (±0.006)</td><td>0.719 (±0.006)</td></tr><tr><td>PA3</td><td>0.774 (±0.008)</td><td>0.653 (±0.008)</td><td>0.966 (±0.001)</td><td>0.743 (±0.008)</td><td>0.927 (±0.003)</td><td>0.758 (±0.007)</td></tr><tr><td rowspan="6">Trojan</td><td>Baseline</td><td>0.481 (±0.030)</td><td>0.428 (±0.007)</td><td>0.873 (±0.004)</td><td>0.389 (±0.012)</td><td>0.782 (±0.005)</td><td>0.603 (±0.014)</td></tr><tr><td>NetAugment</td><td>0.514 (±0.010)</td><td>0.404 (±0.008)</td><td>0.892 (±0.002)</td><td>0.429 (±0.007)</td><td>0.790 (±0.010)</td><td>0.598 (±0.009)</td></tr><tr><td>DyWin</td><td>0.544 (±0.030)</td><td>0.410 (±0.009)</td><td>0.885 (±0.001)</td><td>0.455 (±0.020)</td><td>0.766 (±0.007)</td><td>0.588 (±0.002)</td></tr><tr><td>NetRandAugment</td><td>0.599 (±0.017)</td><td>0.408 (±0.008)</td><td>0.874 (±0.004)</td><td>0.491 (±0.007)</td><td>0.787 (±0.002)</td><td>0.552 (±0.012)</td></tr><tr><td>Rosetta</td><td>0.428 (±0.049)</td><td>0.363 (±0.014)</td><td>0.866 (±0.002)</td><td>0.328 (±0.022)</td><td>0.765 (±0.007)</td><td>0.658 (±0.009)</td></tr><tr><td>PA3</td><td>0.633 (±0.011)</td><td>0.582 (±0.005)</td><td>0.931 (±0.004)</td><td>0.572 (±0.009)</td><td>0.830 (±0.007)</td><td>0.686 (±0.012)</td></tr><tr><td rowspan="12">Shadowsocks</td><td rowspan="6">VMess</td><td>Baseline</td><td>0.489 (±0.004)</td><td>0.360 (±0.006)</td><td>0.900 (±0.002)</td><td>0.367 (±0.003)</td><td>0.688 (±0.008)</td><td>0.449 (±0.012)</td></tr><tr><td>NetAugment</td><td>0.529 (±0.012)</td><td>0.428 (±0.005)</td><td>0.907 (±0.002)</td><td>0.445 (±0.012)</td><td>0.690 (±0.007)</td><td>0.474 (±0.011)</td></tr><tr><td>DyWin</td><td>0.491 (±0.020)</td><td>0.438 (±0.006)</td><td>0.898 (±0.002)</td><td>0.415 (±0.015)</td><td>0.632 (±0.007)</td><td>0.489 (±0.010)</td></tr><tr><td>NetRandAugment</td><td>0.555 (±0.005)</td><td>0.454 (±0.012)</td><td>0.891 (±0.004)</td><td>0.492 (±0.003)</td><td>0.750 (±0.007)</td><td>0.438 (±0.009)</td></tr><tr><td>Rosetta</td><td>0.489 (±0.016)</td><td>0.439 (±0.014)</td><td>0.908 (±0.004)</td><td>0.446 (±0.012)</td><td>0.662 (±0.006)</td><td>0.511 (±0.012)</td></tr><tr><td>PA3</td><td>0.605 (±0.006)</td><td>0.497 (±0.006)</td><td>0.930 (±0.003)</td><td>0.524 (±0.009)</td><td>0.727 (±0.006)</td><td>0.580 (±0.018)</td></tr><tr><td rowspan="6">Trojan</td><td>Baseline</td><td>0.459 (±0.014)</td><td>0.454 (±0.002)</td><td>0.876 (±0.005)</td><td>0.424 (±0.001)</td><td>0.703 (±0.007)</td><td>0.491 (±0.010)</td></tr><tr><td>NetAugment</td><td>0.496 (±0.016)</td><td>0.482 (±0.003)</td><td>0.882 (±0.003)</td><td>0.456 (±0.005)</td><td>0.699 (±0.004)</td><td>0.502 (±0.010)</td></tr><tr><td>DyWin</td><td>0.450 (±0.030)</td><td>0.446 (±0.003)</td><td>0.866 (±0.003)</td><td>0.420 (±0.016)</td><td>0.678 (±0.004)</td><td>0.501 (±0.005)</td></tr><tr><td>NetRandAugment</td><td>0.482 (±0.019)</td><td>0.510 (±0.006)</td><td>0.864 (±0.001)</td><td>0.445 (±0.002)</td><td>0.744 (±0.008)</td><td>0.467 (±0.019)</td></tr><tr><td>Rosetta</td><td>0.457 (±0.007)</td><td>0.440 (±0.006)</td><td>0.873 (±0.001)</td><td>0.400 (±0.005)</td><td>0.691 (±0.008)</td><td>0.534 (±0.009)</td></tr><tr><td>PA3</td><td>0.600 (±0.010)</td><td>0.528 (±0.005)</td><td>0.905 (±0.001)</td><td>0.518 (±0.009)</td><td>0.783 (±0.006)</td><td>0.619 (±0.004)</td></tr><tr><td rowspan="12">Trojan</td><td rowspan="6">VMess</td><td>Baseline</td><td>0.494 (±0.008)</td><td>0.391 (±0.007)</td><td>0.902 (±0.002)</td><td>0.331 (±0.008)</td><td>0.737 (±0.005)</td><td>0.593 (±0.008)</td></tr><tr><td>NetAugment</td><td>0.541 (±0.022)</td><td>0.472 (±0.011)</td><td>0.919 (±0.003)</td><td>0.449 (±0.012)</td><td>0.749 (±0.006)</td><td>0.579 (±0.011)</td></tr><tr><td>DyWin</td><td>0.530 (±0.029)</td><td>0.445 (±0.017)</td><td>0.894 (±0.003)</td><td>0.458 (±0.017)</td><td>0.710 (±0.007)</td><td>0.575 (±0.010)</td></tr><tr><td>NetRandAugment</td><td>0.538 (±0.005)</td><td>0.527 (±0.012)</td><td>0.902 (±0.002)</td><td>0.457 (±0.015)</td><td>0.747 (±0.004)</td><td>0.530 (±0.010)</td></tr><tr><td>Rosetta</td><td>0.472 (±0.016)</td><td>0.465 (±0.014)</td><td>0.891 (±0.003)</td><td>0.415 (±0.017)</td><td>0.700 (±0.003)</td><td>0.590 (±0.004)</td></tr><tr><td>PA3</td><td>0.606 (±0.012)</td><td>0.530 (±0.013)</td><td>0.928 (±0.003)</td><td>0.538 (±0.016)</td><td>0.750 (±0.007)</td><td>0.636 (±0.011)</td></tr><tr><td rowspan="6">Shadowsocks</td><td>Baseline</td><td>0.558 (±0.043)</td><td>0.359 (±0.009)</td><td>0.922 (±0.002)</td><td>0.319 (±0.013)</td><td>0.838 (±0.007)</td><td>0.667 (±0.016)</td></tr><tr><td>NetAugment</td><td>0.618 (±0.032)</td><td>0.374 (±0.009)</td><td>0.941 (±0.003)</td><td>0.372 (±0.024)</td><td>0.847 (±0.002)</td><td>0.646 (±0.028)</td></tr><tr><td>DyWin</td><td>0.515 (±0.058)</td><td>0.273 (±0.006)</td><td>0.923 (±0.003)</td><td>0.357 (±0.031)</td><td>0.837 (±0.007)</td><td>0.654 (±0.009)</td></tr><tr><td>NetRandAugment</td><td>0.601 (±0.032)</td><td>0.335 (±0.010)</td><td>0.925 (±0.004)</td><td>0.429 (±0.021)</td><td>0.844 (±0.006)</td><td>0.612 (±0.017)</td></tr><tr><td>Rosetta</td><td>0.613 (±0.009)</td><td>0.374 (±0.013)</td><td>0.927 (±0.003)</td><td>0.539 (±0.025)</td><td>0.831 (±0.003)</td><td>0.651 (±0.007)</td></tr><tr><td>PA3</td><td>0.691 (±0.021)</td><td>0.523 (±0.019)</td><td>0.942 (±0.003)</td><td>0.576 (±0.030)</td><td>0.860 (±0.006)</td><td>0.737 (±0.006)</td></tr></table>

TABLE IV: Ablation study of PA3. It demonstrates that each tailoring module mitigates the drift in the corresponding stage.

<table><tr><td> $P_{train}$ </td><td colspan="2">VMess</td><td colspan="2">Shadowsocks</td><td colspan="2">Trojan</td></tr><tr><td> $P_{test}$ </td><td>Shadowsocks</td><td>Trojan</td><td>VMess</td><td>Trojan</td><td>VMess</td><td>Shadowsocks</td></tr><tr><td>Baseline</td><td>0.518 (±0.029)</td><td>0.481 (±0.030)</td><td>0.489 (±0.004)</td><td>0.459 (±0.014)</td><td>0.494 (±0.008)</td><td>0.558 (±0.043)</td></tr><tr><td>w/o BFT</td><td>0.726 (±0.008)</td><td>0.600 (±0.018)</td><td>0.522 (±0.012)</td><td>0.510 (±0.011)</td><td>0.601 (±0.029)</td><td>0.565 (±0.039)</td></tr><tr><td>w/o PHT</td><td>0.759 (±0.007)</td><td>0.580 (±0.008)</td><td>0.572 (±0.021)</td><td>0.514 (±0.028)</td><td>0.599 (±0.017)</td><td>0.670 (±0.019)</td></tr><tr><td>w/o POT</td><td>0.688 (±0.013)</td><td>0.597 (±0.012)</td><td>0.571 (±0.010)</td><td>0.574 (±0.010)</td><td>0.527 (±0.018)</td><td>0.599 (±0.010)</td></tr><tr><td>PA3</td><td>0.774 (±0.008)</td><td>0.633 (±0.011)</td><td>0.605 (±0.006)</td><td>0.600 (±0.010)</td><td>0.606 (±0.012)</td><td>0.691 (±0.021)</td></tr></table>

Background Flow Tailoring (BFT). Fig. 10 reports the empirical threshold search for background flow tailoring. In our experiments, we set $\beta ~ = ~ 5$ to prioritize website-flow preservation when computing U(α). The optimal thresholds are $\alpha ^ { * } = 0 . 5$ for VMess, $\alpha ^ { * } = 0 . 5$ for Shadowsocks, and $\alpha ^ { * } = 0 . 4$ for Trojan. Following the alignment rule that we choose the minimal α among all protocols, we select the shared threshold $\alpha _ { o p t } = 0 .$ 4 in this work.

Proxy Handshake Tailoring (PHT). The key parameter is the n-gram vocabulary size v, which controls the granularity of discretization. As defined in Eq. 3, we choose v by maximizing the mutual-information objective $J ( v )$ , which rewards discriminative anomalous windows and penalizes excessive vocabulary growth. Fig. 11 validates our strategy. The vocabulary size that maximizes J(v) also gives the best F1-score for detecting proxy handshake packets. We therefore use the corresponding $v ^ { * }$ to build the anomaly dictionary for each protocol.

Proxy Overhead Tailoring (POT). For proxy overhead tailoring, we estimate the Gaussian parameters µ and σ using randomly selected probe websites for each protocol pair. The learned distribution is used to sample the burst-scaling factor λ. In this evaluation, we sample slope ratios using 5 websites. The parameters for VMess as $P _ { \mathrm { t r a i n } } \mathrm { a r e } \mu _ { \mathrm { V M e s s } } ^ { \mathrm { S h a d o w s o c k s } } =$ $1 . 1 7 , \sigma _ { \mathrm { V M e s s } } ^ { \mathrm { S h a d o w s o c k s } } = 0 . 1 5 , \mu _ { \mathrm { V M e s s } } ^ { \mathrm { T r o j a n } } = 0 . 9 8 , \sigma _ { \mathrm { V M e s s } } ^ { \mathrm { T r o j a n } } = 0 . 1 2$

## D. Ablation Study

Now we conduct an ablation study on the 3 traffic tailoring modules within PA3 to assess their effects.

• Background Flow Tailoring (BFT): Filter out flows whose sizes lie in the BIH flow size range;

• Proxy Handshake Tailoring (PHT): Search for proxy handshake packets and their corresponding ACK packets, and then remove them from each flow;

TABLE V: Stability of the selected optimal coverage $\alpha ^ { * }$ and the corresponding balance score $U ( \alpha ^ { * } )$ range under different sampling ratios.

<table><tr><td rowspan="2">Protocol</td><td colspan="4"> $\alpha^{*}$  under sampling ratio</td><td rowspan="2"> $\max \Delta\alpha^{*}$ </td><td rowspan="2"> $U(\alpha^{*})$  range</td></tr><tr><td>20%</td><td>15%</td><td>10%</td><td>5%</td></tr><tr><td>VMess</td><td>0.50</td><td>0.50</td><td>0.50</td><td>0.50</td><td>0.00</td><td>0.93–0.94</td></tr><tr><td>Shadowsocks</td><td>0.50</td><td>0.50</td><td>0.50</td><td>0.50</td><td>0.00</td><td>0.90–0.92</td></tr><tr><td>Trojan</td><td>0.40</td><td>0.40</td><td>0.40</td><td>0.40</td><td>0.00</td><td>0.80–0.83</td></tr></table>

• Proxy Overhead Tailoring $( P O T ) { \mathrm { : } }$ : Augment the data transmission part of each flow by rescaling the burst sizes according to the empirical slope ratio range.

Table IV shows that every ablated variant improves over the unmitigated baseline in all settings, confirming that each individual module can reduce part of the proxy-induced distortion. Moreover, full PA3 consistently achieves the best F1- score across all protocol pairs. The performance improvements are also consistent across protocol pairs. This indicates that the three modules are complementary. BFT removes protocolspecific noise introduced during flow initialization, PHT aligns the extra proxy handshake sequence, and POT compensates for segmentation shifts during content transmission.

## E. Mitigation Stability under Limited Probe Traffic

In this section, we evaluate the stability of parameter selection when the amount of probe traffic is reduced. The results show that parameters estimated from limited data closely approximate those obtained with sufficient data.

Stability of BFT. We evaluate how the selected coverage threshold $\alpha ^ { * }$ and its corresponding balance score $U ( \alpha ^ { * } )$ change when fewer BIH flows are available. Since BIH flows are uniformly distributed across websites, we randomly sample BIH flows and reduce the sampling ratio from 20% to 5%. The results in Table V show that $U ( \alpha ^ { * } )$ is stable for all proxy protocols, and $\alpha ^ { * }$ remains unchanged as the amount of data is reduced, which suggests that the BIH filtration method is stable even with few probe samples.

Fig. 12 further evaluates stability of the BFT filter ranges under different browser versions. We collect the traffic generated by Firefox version 132 to 141 separately, and compute the ranges for each version across all proxy protocols with $\alpha _ { o p t } ~ = ~ 0 . 4$ . The filter ranges remain stable through version 136 but increase from version 137, mainly because of large firefox-settings-attachments.cdn .mozilla.net flows, which are related to some remotesetting content. Firefox may upgrade its browser configuration policies from version 137. We therefore recommend updating the ranges every 2 or 3 Firefox versions.

Stability of PHT. The core parameter in identifying the proxy handshake packet sequence is the n-gram vocabulary size $v ,$ which balances precision and recall. We assess whether $v ^ { * }$ can be reliably estimated with limited data by reducing the ratio between the numbers of training and testing samples. The ratio is reduced from 25% down to 5%. For each ratio and each protocol, we search for $v ^ { * }$ via $J ( v )$ to report the best F1-score. Table VI shows that the optimal vocabulary size $v ^ { * }$ remains unchanged for each protocol, and F1-score stays consistently high $( \ge 0 . 9 7 3 )$ even when the ratio is only 5%. The results indicate the robustness of MI-based vocabulary size selection, and that the proxy handshake patterns are sufficiently regular and distinctive such that limited data suffice to learn an appropriate discretization granularity.

![](images/9481bad1e08b328802bbd183406bbec464eda6736c64cf705aac51d5d0da0c67.jpg)  
Fig. 12: BFT ranges for Firefox versions from 132 to 141.

TABLE VI: Optimal vocabulary size and best F1-score under different training ratios.

<table><tr><td rowspan="2">Protocol</td><td colspan="5">Best F1-score under training ratio</td><td rowspan="2"> $v^*$ </td></tr><tr><td>25%</td><td>20%</td><td>15%</td><td>10%</td><td>5%</td></tr><tr><td>VMess</td><td>0.973</td><td>0.976</td><td>0.975</td><td>0.975</td><td>0.976</td><td>90</td></tr><tr><td>Shadowsocks</td><td>0.977</td><td>0.979</td><td>0.978</td><td>0.980</td><td>0.977</td><td>7</td></tr><tr><td>Trojan</td><td>0.981</td><td>0.983</td><td>0.982</td><td>0.980</td><td>0.983</td><td>30</td></tr></table>

Stability of POT. We reduce the number of websites within the probe traffic to estimate Gaussian parameters $\mu$ and $\sigma .$ Suppose that $\mu _ { u } , \sigma _ { u }$ are target parameters. We use

$$
e _ {\mu} (k) = \frac {| \hat {\mu} _ {k} - \mu_ {u} |}{\mu_ {u}}, e _ {\sigma} (k) = \frac {| \hat {\sigma} _ {k} - \sigma_ {u} |}{\sigma_ {u}},\tag{5}
$$

to measure the normalized estimation error, where $\hat { \mu } _ { k }$ and $\hat { \sigma } _ { k }$ are mean and standard deviation estimates from k websites. Fig. 13 shows how the errors change when k declines. For each k, we repeatedly subsample the candidate websites. Fig. 13 shows median errors below 0.2 for both protocols, although smaller samples increase the upper-tail variance. Notably, the improvements in Table III use only $k = 5$ probe websites, demonstrating that limited probe traffic remains effective.

## VI. CONCLUSION

We present the first systematic study of proxy-induced traffic drift in WF, showing that the diversity among proxy protocols leads to poor generalization to unseen protocols. Through payload-aware analysis, we find that proxy protocols introduce distinct distortions throughout a website visit. Based on these findings, we develop PA3, which extracts structural fingerprints from a small amount of decryptable probe traffic and converts them into payload-agnostic rules for tailoring encrypted target traffic. Experiments on real-world proxied traffic show that PA3 considerably improves generalization to unseen protocols. These results demonstrate that explainable traffic alignment can substantially improve WF robustness under realistic proxy protocol changes.

![](images/9bd1ade3eff2d8ae44ba031a90ff86ec78d19b33dcc0114281ebed3e563e2401.jpg)  
Fig. 13: Stability of Gaussian parameter estimation under reduced sampling sizes. VMess is used as $P _ { \mathrm { t r a i n } }$ . Estimation errors $e _ { \mu } ( k ) , e _ { \sigma } ( k )$ are used to measure the effects of target mean $( \mu _ { u } )$ and std. $( \sigma _ { u } )$ approximation, respectively.

## REFERENCES

[1] D. Xue, M. Kallitsis, A. Houmansadr, and R. Ensafi, “Fingerprinting obfuscated proxy traffic with encapsulated TLS handshakes,” in USENIX Security. Philadelphia, PA: USENIX Association, Aug. 2024, pp. 2689– 2706.

[2] D. Xue, R. Stanley, P. Kumar, and R. Ensafi, “The discriminative power of cross-layer rtts in fingerprinting proxy traffic,” in NDSS. The Internet Society, 2025.

[3] N. P. Hoang, J. Dalek, M. Crete-Nishihata, N. Christin, V. Yegneswaran, M. Polychronakis, and N. Feamster, “GFWeb: Measuring the great firewall’s web censorship at scale,” in USENIX Security. Philadelphia, PA: USENIX Association, Aug. 2024, pp. 2617–2633.

[4] ——, “Exposing and circumventing sni-based quic censorship of the great firewall of china,” in USENIX Security. USENIX Association, 2025.

[5] Anonymous, A. A. Niaki, N. P. Hoang, P. Gill, and A. Houmansadr, “Triplet censors: Demystifying great Firewall’s DNS censorship behavior,” in FOCI. USENIX Association, Aug. 2020.

[6] R. Ensafi, D. Fifield, P. Winter, N. Feamster, N. Weaver, and V. Paxson, “Examining how the great firewall discovers hidden circumvention servers,” in IMC, K. Cho, K. Fukuda, V. S. Pai, and N. Spring, Eds. ACM, 2015, pp. 445–458.

[7] M. Wu, J. Sippe, D. Sivakumar, J. Burg, P. Anderson, X. Wang, K. Bock, A. Houmansadr, D. Levin, and E. Wustrow, “How the great firewall of china detects and blocks fully encrypted traffic,” in USENIX Security, J. A. Calandrino and C. Troncoso, Eds. USENIX Association, 2023, pp. 2653–2670.

[8] S. Frolov, J. Wampler, and E. Wustrow, “Detecting probe-resistant proxies,” in NDSS. The Internet Society, 2020.

[9] P. Sirinam, M. Imani, M. Juarez, and M. Wright, “Deep fingerprinting: Undermining website fingerprinting defenses with deep learning,” in CCS, D. Lie, M. Mannan, M. Backes, and X. Wang, Eds. ACM, 2018, pp. 1928–1943.

[10] A. Bahramali, A. Bozorgi, and A. Houmansadr, “Realistic website fingerprinting by augmenting network traces,” in CCS, W. Meng, C. D. Jensen, C. Cremers, and E. Kirda, Eds. ACM, 2023, pp. 1035–1049.

[11] X. Deng, Q. Yin, Z. Liu, X. Zhao, Q. Li, M. Xu, K. Xu, and J. Wu, “Robust multi-tab website fingerprinting attacks in the wild,” in IEEE S&P. IEEE, 2023, pp. 1005–1022.

[12] B. Gao, W. Liu, G. Liu, F. Nie, and J. Huang, “Multi-level resourcecoherented graph learning for website fingerprinting attacks,” IEEE Trans. Inf. Forensics Secur., vol. 20, pp. 693–708, 2025.

[13] X. Deng, Q. Li, and K. Xu, “Robust and reliable early-stage website fingerprinting attacks via spatial-temporal distribution analysis,” in CCS, B. Luo, X. Liao, J. Xu, E. Kirda, and D. Lie, Eds. ACM, 2024, pp. 1997–2011.

[14] X. Zhao, X. Deng, Q. Li, Y. Liu, Z. Liu, K. Sun, and K. Xu, “Towards fine-grained webpage fingerprinting at scale,” in CCS, B. Luo, X. Liao, J. Xu, E. Kirda, and D. Lie, Eds. ACM, 2024, pp. 423–436.

[15] Y. Xie, J. Feng, W. Huang, Y. Zhang, X. Sun, X. Chen, and X. Luo, “Contrastive fingerprinting: A novel website fingerprinting attack over few-shot traces,” in WWW, T. Chua, C. Ngo, R. Kumar, H. W. Lauw, and R. K. Lee, Eds. ACM, 2024, pp. 1203–1214.

[16] X. Ma, M. Shi, B. An, J. Li, D. X. Luo, J. Zhang, and X. Guan, “Context-aware website fingerprinting over encrypted proxies,” in IEEE INFOCOM. IEEE, 2021, pp. 1–10.

[17] X. Ma, J. Qu, M. Shi, B. An, J. Li, X. Luo, J. Zhang, Z. Li, and X. Guan, “Website fingerprinting on encrypted proxies: A flow-contextaware approach and countermeasures,” IEEE/ACM Trans. Netw., vol. 32, no. 3, pp. 1904–1919, 2024.

[18] J. Li, D. Wang, Y. Liu, Y. Gao, X. Zhang, Z. Lin, X. Ma, X. Luo, and X. Guan, “Cross-environmental website fingerprinting,” in IEEE INFOCOM. IEEE, 2025, pp. 1–10.

[19] R. Shwartz-Ziv and N. Tishby, “Opening the black box of deep neural networks via information,” arXiv preprint arXiv:1703.00810, 2017.

[20] A. M. Saxe, Y. Bansal, J. Dapello, M. Advani, A. Kolchinsky, B. D. Tracey, and D. D. Cox, “On the information bottleneck theory of deep learning,” in ICLR. OpenReview.net, 2018.

[21] J. Althouse, J. Atkinson, and J. Atkins, “Tls fingerprinting with JA3 and JA3S,” 2017. [Online]. Available: https://github.com/salesforce/ja3

[22] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “ET-BERT: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in WWW, F. Laforest, R. Troncy, E. Simperl, D. Agarwal, A. Gionis, I. Herman, and L. Medini, Eds.´ ACM, 2022, pp. 633–642.

[23] V. Rimmer, D. Preuveneers, M. Juarez, T. van Goethem, and W. Joosen, “Automated website fingerprinting through deep learning,” in NDSS. The Internet Society, 2018.

[24] X. Tan, C. Peng, P. Xie, H. Wang, M. Li, S. Chen, and C. C. Zou, “Interflow spatio-temporal correlation analysis based website fingerprinting using graph neural network,” IEEE Trans. Inf. Forensics Secur., vol. 19, pp. 7619–7632, 2024.

[25] Y. Cheng, Y. Zhu, B. Li, P. Sun, Y. Ding, X. Deng, and Q. Liu, “HOLMES & WATSON: A robust and lightweight HTTPS website fingerprinting through HTTP version parallelism,” in WWW, G. Long, M. Blumestein, Y. Chang, L. Lewin-Eytan, Z. H. Huang, and E. Yom-Tov, Eds. ACM, 2025, pp. 1078–1092.

[26] B. Cebere and C. Rossow, “Understanding web fingerprinting with a protocol-centric approach,” in RAID, 2024, pp. 17–34.

[27] M. Shen, K. Ji, Z. Gao, Q. Li, L. Zhu, and K. Xu, “Subverting website fingerprinting defenses with robust traffic representation,” in USENIX Security, J. A. Calandrino and C. Troncoso, Eds. USENIX Association, 2023, pp. 607–624.

[28] A. Mitseva and A. Panchenko, “Stop, don’t click here anymore: Boosting website fingerprinting by considering sets of subpages,” in USENIX Security, D. Balzarotti and W. Xu, Eds. USENIX Association, 2024.

[29] R. Xie, J. Cao, E. Dong, M. Xu, K. Sun, Q. Li, L. Shen, and M. Zhang, “Rosetta: Enabling robust TLS encrypted traffic classification in diverse network environments with TCP-Aware traffic augmentation,” in USENIX Security. Anaheim, CA: USENIX Association, Aug. 2023, pp. 625–642.

[30] X. Deng, Y. Zhang, Q. Li, Z. Liu, Y. Wang, and K. Xu, “Enhancing website fingerprinting attacks against traffic drift,” in Network and Distributed System Security (NDSS) Symposium, 2026.

[31] J. Vehent, “Protecting firefox data with content signatures,” in Enigma. Santa Clara, CA: USENIX Association, Jan. 2018.

[32] R. T. Braden, “Requirements for Internet Hosts - Communication Layers,” RFC 1122, Oct. 1989. [Online]. Available: https://www. rfc-editor.org/info/rfc1122

[33] J. Graham-Cumming, “Optimizing tls over tcp to reduce latency,” 2016. [Online]. Available: https://blog.cloudflare.com/ optimizing-tls-over-tcp-to-reduce-latency/

[34] S. Siby, M. Juarez, C. Diaz, N. Vallina-Rodriguez, and C. Troncoso, “Encrypted dns –¿ privacy? a traffic analysis perspective.” in NDSS. The Internet Society, 2020.

[35] D. Borman, “TCP Options and Maximum Segment Size (MSS),” RFC 6691, Jul. 2012. [Online]. Available: https://www.rfc-editor.org/info/ rfc6691

[36] “Selenium,” accessed: 2025-08-24. [Online]. Available: https://www. selenium.dev/

[37] “Clash core,” accessed: 2025-09-04. [Online]. Available: https: //github.com/Kuingsmile/clash-core

[38] Z. Guan, G. Xiong, G. Gou, Z. Li, M. Cui, and C. Liu, “Bapm: block attention profiling model for multi-tab website fingerprinting attacks on tor,” in ACSAC, 2021, pp. 248–259.

[39] P. Sirinam, N. Mathews, M. S. Rahman, and M. Wright, “Triplet fingerprinting: More practical and portable website fingerprinting with n-shot learning,” in CCS, 2019, pp. 1131–1148.

[40] M. S. Rahman, P. Sirinam, N. Mathews, K. G. Gangadhara, and M. Wright, “Tik-Tok: The utility of packet timing in website fingerprinting attacks,” PETS, vol. 2020, no. 3, pp. 5–24, 2020.

[41] H. Jeon, S. Kim, N. Mathews, H. Kang, and S. E. Oh, “Rofire: Robust website fingerprinting on real-world tor traffic via improved augmentation and normalization,” in WWW. Association for Computing Machinery, 2026, p. 3332–3343. [Online]. Available: https://doi.org

[42] Z. Jin, T. Lu, H. Chen, and F. Yu, “Enhancing website fingerprinting through combined data augmentation strategies,” Computers & Security, 2026.
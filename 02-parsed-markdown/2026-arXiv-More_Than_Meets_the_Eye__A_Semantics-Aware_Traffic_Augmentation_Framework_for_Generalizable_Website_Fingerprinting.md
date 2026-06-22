# More Than Meets the Eye: A Semantics-Aware Traffic Augmentation Framework for Generalizable Website Fingerprinting

Youquan Xian∗§∥, Xueying Zeng†∥, Lingjia Meng§, Lei Cui§B, Runhan Song§¶, Wei Wang§, Zhengquan Ding§, Peng Liu‡, Zhiyu Hao§B

∗School of Cyberspace Security, Beijing University of Posts and Telecommunications, Beijing, China

†School of Computer Science and Engineering, Beihang University, Beijing, China

¶Faculty of Computing, Harbin Institute of Technology, Harbin, China

‡School of Computer Science and Engineering, Guangxi Normal University, Guilin, China

§Zhongguancun Laboratory, Beijing, China

Abstract—Deep learning-based website fingerprinting has emerged as an effective technique for inferring the websites users visit. Although existing methods achieve strong performance on closed-world datasets, they often fail to generalize to real-world environments, especially under geographic and temporal shifts. This limitation fundamentally stems from the coupled effects of two key challenges: application-layer resource composition variability and observable feature instability induced by cross-layer encapsulation. Intertwined, these factors induce systematic shifts between underlying application semantics and observable traffic features. To address the above challenges, we propose SATA, a semantics-aware traffic augmentation framework. Specifically, SATA first performs application-layer semantic augmentation based on protocol rules, expanding the resource composition patterns within each flow and frame sequence patterns under protocol constraints. Based on these augmented frame sequences, we further introduce a cross-layer feature alignment mechanism via knowledge distillation. It aligns frame sequence with packetlength sequence features, enabling cross-layer feature alignment between enhanced semantics and observable sequences. Extensive experiments show that SATA successfully generates traffic patterns that are absent from the training set but genuinely exist in the test set, and significantly improves the performance of mainstream models across diverse and complex scenarios. In particular, in open-world settings, SATA improves ACC by 90.81% and AUROC by 48.37%. The source code of the prototype system is available at https://anonymous.4open.science/r/SATA-B6C2/.

# I. INTRODUCTION

In recent years, end-to-end encrypted protocols, exemplified by TLS 1.3 [1], along with privacy-enhancing technologies such as encrypted DNS [2]–[4] and Encrypted Client Hello [5], have fundamentally reshaped the privacy landscape of

∥ Equal contribution.   
BCorresponding author.

![](images/07528b9146baa6228880406d0bd732f8897be62833a6b7b8e106260ae90d5a3e.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Servers"] -->|Flow| B["Router"]
    B --> C["User"]
    C --> D["Attacker"]
    D --> E["CFM"]
    E --> F["Application"]
    style A fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
    style C fill:#cfc,stroke:#333
    style D fill:#fcc,stroke:#333
    style E fill:#cff,stroke:#333
    style F fill:#ffc,stroke:#333
```
</details>

Fig. 1. Overview of a WF attack scenario and its two major generalization challenges. Blue dashed lines denote the attacker’s workflow, and red dashed regions indicate the challenges faced by the attacker.

cyberspace. The widespread deployment of these mechanisms has rendered traditional traffic analysis methods that rely on deep packet inspection and plaintext metadata increasingly ineffective [6]–[10]. However, protocol-level encryption does not eliminate the risk of privacy leakage. During communication, side channels such as packet length and packet direction can still expose observable features [11], [12]. With their strong capability for non-linear representation learning, advanced website fingerprinting (WF) models can bypass payload encryption and infer high-level application behaviors solely from these observable signals, thereby posing a new threat to network privacy [13]–[17].

Although existing WF models have achieved promising performance on closed-world datasets, variations in resource scheduling and multilayer protocol encapsulation mechanisms in real networks pose severe generalization challenges in the real world. To improve generalization, existing studies have primarily relied on the data augmentation paradigm, addressing the problem from two perspectives: data distribution fitting and network simulation. On the one hand, methods based on deep generative models such as generative adversarial networks (GANs) and large language models (LLMs) are mostly limited to generating intermediate representations or nonfunctional fields [18]–[22]. Such purely data-driven paradigms are highly dependent on the training set’s original distribution and struggle to extend beyond the existing probability space to generate plausible out-of-domain (OOD) data [23], [24]. On the other hand, existing simulation-based augmentation strategies, such as those simulating perturbations in roundtrip time (RTT) and maximum transmission unit (MTU), remain confined to TCP/IP stack–level effects [13], [25]–[28]. More importantly, both paradigms overlook how applicationlayer resource scheduling and cross-layer encapsulation jointly shape traffic features. As a result, the mapping from application semantics, namely the actual conveyed resources, to observed traffic features exhibits a systematic shift that is difficult to correct.

We observe that the systematic shift of observed traffic features fundamentally arises from the coupled effects of two challenges during traffic generation, as illustrated in Fig. 1. First, at the application layer, the interplay of dynamic DNS [29], [30] and HTTP/2 multiplexing [31] continuously alters the composition of resources within a flow, resulting in resource composition variability (C1). Second, during crosslayer encapsulation, application resources undergo structural perturbations induced by state-dependent header compression [32], fragmentation, and dynamic scheduling mechanisms [31], [33], [34], resulting in unstable observed features, such as packet-length sequences (C2). The systematic feature shift induced by these challenges significantly degrades the generalization capability of WF models in real-world environments.

To address the aforementioned challenges, this paper provides an analysis of the multilayer factors underlying the systematic shift of observed traffic features. On this basis, we propose a semantics-aware traffic augmentation framework, SATA. Specifically, SATA first expands the resource composition patterns within each flow and the application-layer frame sequence patterns under protocol constraints through a resource recomposition module and a frame sequence augmentation module. It then introduces a cross-layer feature alignment mechanism that uses frame sequence representations to guide the learning of packet-length sequences. This design mitigates the systematic shift of observed features, improving the generalization and robustness of existing WF models in the real world. To the best of our knowledge, this is the first work to leverage application-layer semantics for traffic augmentation.

The main contributions are summarized as follows:

• We analyze the multilayer factors underlying the systematic shift of observed traffic features, revealing how application-layer behaviors and cross-layer protocol mechanisms jointly reshape traffic features. It provides a theoretical foundation for understanding the mechanisms driving such feature shifts.   
• We propose a semantic-aware traffic augmentation framework, SATA, which simulates realistic network protocol processes to enrich application-layer frame sequences,

while also constructing a cross-layer feature alignment mechanism to align observed features with semantic features.

• Extensive experimental results validate the effectiveness of SATA. It improves ACC and AUROC by 90.81% and 48.37% in open-world settings, respectively, and increases pattern coverage by 9.93%, generating frame sequence patterns unobserved in the training set but present in the test set.

# II. RELATED WORK

# A. Advances in Website Fingerprinting

With the widespread adoption of end-to-end encryption, the focus of WF research has transitioned from labor-intensive, pioneering manual feature engineering [14], [16], [35], [36] to deep learning-based automatic representation learning. The selection of model input features has been extensively investigated in previous works. Although some recent studies directly learn from raw payload bytes in an end-to-end manner [37]–[48], the latest research demonstrates that the pseudorandomness of encrypted payloads can easily induce such models to rely on dataset-specific biases through shortcut learning [10]. In contrast, packet length sequences and associated side-channel features, such as timing and direction, circumvent payload-level obfuscation and have been shown to provide more fundamental and reliable representations. They have therefore become the central focus of current WF research [9].

For sequence features such as packet length, researchers have developed a wide range of deep learning models and architectures at different granularities. From the perspective of granularity, flow-level methods leverage models such as CNN and LSTM to perform lightweight modeling of single-flow features [49]–[55]. Trace-level methods, by contrast, incorporate more complex architectures to integrate global session context [15], [17], [56]–[59]. Benefiting from these powerful deep neural architectures and refined feature engineering, existing WF models generally achieve remarkable classification accuracy on public closed-world datasets, with performance nearing saturation. However, such performance advantages obtained in controlled environments frequently collapse in the wild [13], [27], [60].

# B. Data Augmentation

Recent studies have widely adopted data augmentation strategies to expand the training space, thereby addressing the generalization bottlenecks in existing models. The mainstream strategies can be broadly categorized into two categories: data distribution fitting and network simulation.

The first category relies on data-driven distribution fitting and extensively employs deep generative models, such as generative adversarial networks (GANs), diffusion models, and large language models (LLMs), to synthesize and augment traffic representations. Specifically, to mitigate class imbalance, ILETC [20], CS-BiGAN [18], and NetDiffusion [19] generate samples with high statistical similarity by directly learning traffic sequences or implicitly fine-tuning image-like representations to accurately capture the latent distribution of traffic. Hajaj et al. [22] employed LSTMs to perform temporal extrapolation on traffic feature images. AdvTG [21], in contrast, leverages a fine-tuned LLM to selectively mutate non-functional fields in payloads, achieving semantic-level adversarial augmentation. However, distribution fitting methods often overlook the generation logic of traffic features, making it difficult for existing generative models to synthesize an interpretable, valid OOD packet length sequences [23], [24].

The second category augments traffic representations by manually manipulating network states, such as MTU and RTT, or by simulating packet loss and packet reordering, to force models to learn invariant features under diverse transmission conditions. Specifically, Rosetta [27] and Zion et al. [26] dynamically adjust network transmission parameters to generate synthetic samples characterized by sequence shifts and size variations. Horowicz et al. [28] further extend such delay and packet-loss perturbations to customized augmentation of twodimensional traffic images. At the granularity of structural operations on packet sequences, NetAugment [13] and Zion et al. [26] simulate feature shifts caused by bandwidth fluctuations through fine-grained modification of burst sequences and averaging of cross-flow features, respectively. Meanwhile, Nuwa [25] further introduces masking strategies for packet loss and reordering, leveraging self-supervised learning to reconstruct corrupted complete features dynamically. However, these methods mainly operate on TCP/IP-stack-level observations, without touching the application-layer semantics that generate traffic.

Therefore, it is imperative to develop a traffic augmentation mechanism that bridges application semantics and observable features to enhance model generalization in the real world.

# III. CHALLENGES

Expanding on the challenges previously outlined, we examine the multilayer factors driving the systematic shift of traffic features from two perspectives: (C1) Application-Layer Resource Composition Variability, and (C2) Observation-Level Feature Instability induced by similar application semantics.

# A. Application-Layer Resource Composition Variability

Regarding resource composition variation, two representative scenarios are observed, as illustrated in Fig. 2 and Fig. 3, namely changes in domain combination within a flow and the absence of multiplexing for same-domain resources within a single flow.

The first scenario arises from the interplay of dynamic DNS, shared infrastructure, and HTTP/2 connection coalescing. In practice, diverse domains may be resolved to the same service endpoint via CDNs [6] or reverse proxies [61]. When these domains satisfy connection reuse criteria, such as TLS certificate compatibility, the client may leverage a single TCP connection to transmit logically independent cross-domain requests. Consequently, resources from multiple domains are consolidated into one flow, altering the original domain composition and traffic distribution patterns. As illustrated in Fig. 2, across different visits, resources of domain emp.bbci.co.uk may co-occur within the same flow as static.files.bbci.co.uk or static.bbci.co.uk due to HTTP/2 connection coalescing, leading to variations in resource composition within the flow.

![](images/b4416443e7d49ba48372b4349f96d2923ec01d3d593049777c7feaa2566e3189.jpg)

<details>
<summary>text_image</summary>

(a) Trace 1
https://static.files.bbci.co.uk/.../958cd2585.js
172.18.0.2:59336->88.221.168.120:443
https://static.files.bbci.co.uk/.../07f766f6b.js
https://emp.bbci.co.uk/.../-4/bump-4.js
https://static.files.bbci.co.uk/.../aeba27237.js
https://static.files.bbci.co.uk/.../1d22ac4fa.js
(b) Trace 2
https://emp.bbci.co.uk/.../-4/bump-4.js
172.18.0.2:39004->88.221.168.120:443
https://static.bbci.co.uk/.../s/require.js
Resources (URI)
Flow
IP Destination
</details>

Fig. 2. Illustrative example of cross-domain resource aggregation caused by dynamic DNS and HTTP/2 connection coalescing.   
![](images/3caca4c443d5ace0e3e957c53b931b109f61d0e7fa69971d1bb82ad01a62e4ac.jpg)

<details>
<summary>bar_stacked</summary>

| Resource (URI) | Flow | IP Destination |
| --- | --- | --- |
| https://assets.nflxext.com/.../6cccad376.js | 172.18.0.2:47280->45.57.90.1:443 | |
| https://assets.nflxext.com/.../96_large.jpg | 172.18.0.2:47304->45.57.90.1:443 | |
| https://assets.nflxext.com/.../_W_Blk.woff2 | 172.18.0.2:47344->45.57.90.1:443 | |
| https://assets.nflxext.com/.../s_W_Bd.woff2 | 172.18.0.2:47342->45.57.90.1:443 | |
| https://assets.nflxext.com/.../s_W_Md.woff2 | 172.18.0.2:47342->45.57.90.1:443 | |
| https://assets.nflxext.com/.../6cccad376.js | 172.18.0.2:38802->45.57.91.1:443 | |
| https://assets.nflxext.com/.../96_large.jpg | 172.18.0.2:38820->45.57.91.1:443 | |
| https://assets.nflxext.com/.../_W_Md.woff2 | 172.18.0.2:38834->45.57.91.1:443 | |
| https://assets.nflxext.com/.../_W_Blk.woff2 | 172.18.0.2:38834->45.57.91.1:443 | |
</details>

Fig. 3. Illustrative example of flow-level resource distribution variation induced by HTTP/2 connection reuse.

The second scenario primarily arises from the inherent nondeterminism of HTTP/2 connection reuse strategies in practical implementations. Although HTTP/2 recommends reusing existing connections to enhance transmission efficiency, RFC 9113 explicitly states that clients are not mandated to enforce reuse [62]. The client may dynamically establish new TCP connections or shift scheduling across multiple connections under various triggers, such as existing connection loads approaching their thresholds, active termination by either party, or intervention by browser security isolation policies. Consequently, resource requests under the same domain may be distributed across multiple parallel flows, manifesting a multi-flow transmission pattern. As illustrated in Fig. 3, the red-marked resource from assets.nflxext.com occupies an exclusive flow in one visit, while in another it shares a flow with other resources, leading to significantly different transmission structures (Appendix B). This volatility decouples flows from semantics, rendering models overfitted to static training distributions fragile against the real world.

![](images/e0948073ed33b3c91e0b92f3776344290ed9feaca32237f87444310363fa6e13.jpg)

<details>
<summary>line</summary>

| Packet Index | Packet Length (Log) | Detailed View |
| ------------ | ------------------- | ------------- |
| 0            | ~10^3               | ~1.2 × 10^4   |
| 5            | ~10^3               | ~1.4 × 10^4   |
| 10           | ~10^4               | ~1.6 × 10^4   |
| 15           | ~10^4               | ~1.8 × 10^4   |
| 20           | ~10^4               | ~2.0 × 10^4   |
| 25           | ~10^4               | ~2.2 × 10^4   |
| 30           | ~10^4               | ~2.2 × 10^4   |
</details>

Fig. 4. Illustrative example of packet length sequence instability caused by HTTP/2 scheduling and cross-layer encapsulation.

# B. Observation-Level Feature Instability

Beyond variations in resource composition, packet length sequences of the same resource can exhibit significant variations, as illustrated in Fig. 4. In the mapping from applicationlayer resources to HTTP/2 frames, such uncertainty primarily originates from state dependencies and scheduling coupling within the protocol. On the one hand, HPACK, the header compression mechanism used in HTTP/2, leverages a stateful dynamic table to reduce redundant header transmission. Its stateful nature leads HEADER frames to alternate between indexed header field representation and literal encoding, resulting in variable frame sizes [32]. On the other hand, the concurrent requests of partial resources under multiplexing drives the protocol stack to transmit HEADERS frames in compacted bursts, disrupting the expected sequential structure of HEADERS and DATA frames in observed traces (Appendix D).

Furthermore, during cross-layer encapsulation, buffering and asynchronous scheduling across the HTTP, TLS, and TCP layers undermine the stability of data unit boundaries as they propagate through the protocol stack. Dynamic buffer write patterns, evolving window states, and transmission scheduling jointly drive continuous fragmentation of data units, resulting in non-linear segmentation in the top-down mapping of application-layer semantics (Appendix C). Finally, at the transport layer, the mapping from TLS records to TCP segments is further modulated by factors such as maximum segment size (MSS) [63] negotiation, exacerbating this cross-layer structural perturbation. It disrupts learned temporal dependencies, constraining the generalization capability of conventional WF models in the real world.

# IV. SYSTEM DESIGN

# A. Threat Model

We consider a website fingerprinting scenario in real-world HTTP/2 traffic, where deep learning models are deployed in operational networks to perform classification based solely on observable packet-length sequences extracted from TCP flows. However, modern web infrastructure and the HTTP/2 protocol jointly lead to significant variability in traffic features. These factors collectively induce significant distribution shifts between training and deployment environments, impeding the generalization of existing models in realistic settings.

SATA aims to improve the classification robustness of existing deep learning models when handling real-world HTTP/2 traffic. It does not require prior knowledge of the network environment. In practice, mechanisms such as dynamic scheduling and protocol stack encapsulation on both the client and server sides are highly time-varying and largely unobservable, making them extremely difficult to capture accurately in real time. Moreover, SATA maintains compatibility with existing models without requiring architectural modifications. It only necessitates a knowledge distillation framework, where the original WF model is instantiated as both teacher and student, and trained in a two-stage scheme across distinct tasks.

# B. Overview

This paper presents SATA, a semantics-aware traffic augmentation framework, as illustrated in Fig. 5. SATA is designed to mitigate the systematic shift stemming from both application-layer resource composition variability (C1) and observation-level feature instability (C2), thereby enhancing the robustness of mainstream deep learning models on realworld HTTP/2 traffic.

SATA establishes a systematic pipeline spanning dataset construction, traffic augmentation, and feature alignment. Specifically, it first formalizes a semantic correspondence between plaintext resources and encrypted traffic. Subsequently, by incorporating resource recomposition and frame-sequence augmentation tailored to mechanisms like dynamic DNS and HTTP/2 multiplexing, the framework diversifies flow-level application semantics to encompass the varied traffic patterns encountered in operational networks. Finally, a knowledge distillation-based feature alignment mechanism transfers semantic knowledge from frame sequences to the observations packet-length representation, enabling the model to inherit the enriched semantics while mitigating systematic shift. SATA maintains full compatibility with existing architectures; it involves instantiating the original WF model as both a teacher and a student within a two-stage knowledge distillation paradigm. In the following subsections, we introduce the four core modules of SATA in detail.

# C. Dataset Construction

To address the lack of fine-grained alignment between plaintext resources and encrypted observations in existing encrypted traffic datasets, this paper leverages Tshark 1 and TLS session keys to perform cross-layer parsing of raw traffic, thereby establishing correspondences among resources, HTTP/2 frame sequences, and packet length sequences. Specifically, two types of mappings are constructed. First, TLS traffic is decrypted to extract the HTTP/2 frame sequence corresponding to each resource, consisting of the sizes of HEADER and DATA frames, establishing a mapping between resources and frame sequences. Second, at the flow level, resource compositions and their corresponding TCP packet length sequences are extracted to establish a mapping between resource compositions and observable traffic representations. Through this process, a cross-layer aligned dataset linking resources, frame sequences, and packet length sequences is constructed, providing the data foundation for subsequent resource recomposition, frame sequence augmentation, and cross-layer feature alignment.

![](images/af92e39149c145d7e63f0e12ad10fd00ee3d8772bc6371d2af7a1add78aef8b6.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Dataset Construction"] --> B["Resource Recomposition"]
    B --> C["Frame Sequence Augmentation"]
    C --> D["Feature Alignment"]

    subgraph_A["Dataset Construction"]
        E["google.com"] --> F["apple.com"]
        G["github.com"] --> H["Flow1"]
        G --> I["Flow2"]
        G --> J["..."]
        K["A B"] --> L["Resources"]
        M["C D E"] --> L
        L --> N["TCP Packet Length Sequence"]
    end

    subgraph_B["Resource Recomposition"]
        O["SAN1"] --> P["SAN2"]
        Q["IP1"] --> R["Empirical Flow Reuse Pattern Resampling"]
        S["IC D E"] --> T["Empirical Flow Reuse Pattern Resampling"]
        U["Flow1"] --> V["Flow2"]
        W["Flow4"] --> X["Flow4"]
    end

    subgraph_C["Frame Sequence Augmentation"]
        Y["Structure-preserving"] --> Z["Stable Changeable"]
        AA["Distribution-constrained Sequence Augmentation"] --> AB["[205, -1623, 64, -15645"]]
        AC["Header"] --> AD["Forward Temporal Shift Mechanism"]
        AE["Aug HTTP Frame Sequence"] --> AF["H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H H_H"]
    end

    subgraph_D["Feature Alignment"]
        AG["Aug Set"] --> AH["Generated PLS"]
        AI["Train Set"] --> AJ["Teacher Model"]
        AK["PLS"] --> AL["Student Model"]
        AM["Embedding"] --> AN["Soft-label Distillation (KL Divergence)"]
        AO["Latent Feature Alignment (Cosine Loss)"] --> AP["Teacher stage"]
        AQ["Student stage"] --> AR["Student stage"]
    end

    subgraph D
        AS["Soft-label Distillation (KL Divergence)"] --> AT["Teacher stage"]
        AU["Latent Feature Alignment (Cosine Loss)"] --> AV["Teacher stage"]
        AW["Student stage"]
    end
```
</details>

Fig. 5. The workflow of SATA is as follows: (1) Dataset Construction module establishes precise alignment between plaintext resources and encrypted traffic, providing the data foundation. (2) Resource Recomposition module operates on this dataset to simulate dynamic DNS and HTTP/2 multiplexing, generating flows with diverse resource composition patterns. (3) Frame Sequence Augmentation module perturbs the transmission volume and positional distribution of frame sequences within the recombined flows, and models header coalescing behavior, expanding frame sequence patterns. (4) The Feature Alignment module employs knowledge distillation to transfer semantically aligned representations from augmented sequences into the WF model.

D. Resource Recomposition   
```cpp
bool VerifyDomainAuthentication(domain) {
    if (session_is_draining)
    return false;
    if (!GetSSInfo())
    return true; // non-TLS session
    return CanPool(domain);
}
bool CanPool(new_hostname) {
    if (IsCertStatusError())
    return false;
    if (!cert->VerifyNameMatch(new_hostname))
    return false; // SAN validation (core constraint)
    if (IsPKPViolated())
    return false;
    return true;
} 
```  
Listing 1. HTTP/2 reuse logic via certificate SAN validation (Chromium).

As shown in Listing 1, an analysis of the HTTP/2 protocol stack implementation in Chromium reveals that when two domains share the same Subject Alternative Name (SAN) [64] and are resolved to the same IP address via DNS, the protocol stack may reuse a TCP connection. This mechanism changes the allocation of resources to different flows, affecting resource composition patterns within a flow. To simulate this phenomenon, we propose a SAN-constrained resource remapping method. The overall procedure is illustrated in Fig. 5. Specifically, we first extract SAN information from raw traffic and establish a mapping from resources to their registered domains and corresponding SAN sets. Next, we analyze the distribution of the number of IP nodes associated with each SAN in traffic traces and model it using a Gaussian distribution parameterized by the mean $\mu _ { s a n }$ and standard deviation $\sigma _ { s a n }$ . During the data augmentation phase, given an input trace, we sample a target number of IP nodes N from the distribution $\mathcal { N } ( \mu _ { s a n } , \sigma _ { s a n } )$ , and reassign the M domains within the same SAN set in the trace to these N IP nodes. This process modifies the domain-to-IP mapping under protocol constraints, thereby adjusting how resources are distributed across concurrent flows and effectively augmenting the resource composition patterns within the original trace.

Furthermore, to address variations in flow reuse patterns for resources within the same domain, we design an empirically driven resampling method to augment flow reuse patterns. In the offline phase, we analyze historical traffic to collect allocation patterns of resources within the same domain across different flows, remove duplicate patterns, and construct a domain-specific pool of flow reuse patterns along with their empirical probability distributions. As illustrated in Fig. 5, for a domain containing resources C, D, two reuse patterns may exist in historical observations: either C, D are transmitted within the same flow, or C and D are distributed across two different flows. In the online augmentation phase, given an input trace, we first extract the set of resources associated with the test set and search for matching historical reuse patterns with the same resource set in the related pattern pool. If matching patterns exist, one is randomly sampled according to its empirical probability and used to reorganize the current resource composition. If no matching pattern exists, a flow reuse pattern is randomly constructed for the current resource set under the constraint of a maximum number of concurrent flows.

In summary, these two resource recomposition strategies effectively simulate the variations in resource composition induced by the interplay between dynamic DNS and protocol stack reuse. By enriching the boundaries of the data distribution, they encourage the model to learn more generalizable representations of resource semantic grouping.

# E. Frame Sequence Augmentation

We observe that the total upstream and downstream traffic volumes exhibit pronounced multimodal distributions, driven by factors such as HPACK index hit states, accompanied by a clear static–dynamic separation in frame sequences, where some frame lengths remain stable while others vary within bounded ranges (Appendix C).

Based on the above observations, we propose a frame sequence augmentation method with structure preservation and distributional constraints. It aims to generate HTTP frame sequences that conform to historical statistical distributions while retaining the stable structural patterns of applicationlayer frame sequences. Given the historical set of HTTP frame sequences for a certain resource, denoted as $s ,$ each sequence can be represented as $S ~ = ~ [ s _ { 1 } , s _ { 2 } , \ldots , s _ { L } ]$ , where positive values indicate upstream requests and negative values indicate downstream responses.

First, the method aligns the sample sequences in S and identifies positions where frame sizes remain nearly constant as anchor positions, which preserve the stable structural patterns of the resource’s frame sequence. Meanwhile, it detects the set of positions $\mathcal { M }$ where frame sizes exhibit variability, which are treated as adjustable positions for subsequent augmentation. For each adjustable position $i \in \mathcal { M }$ , the historical variance $\sigma _ { i } ^ { 2 }$ and value range $[ b _ { i } ^ { m i n } , b _ { i } ^ { m a x } ]$ are estimated to constrain the magnitude of local perturbations. In addition, for each historical sequence, the total upstream volume U and downstream volume D are computed, and their probability distributions $\hat { f } _ { U } ( u )$ and ${ \hat { f } } _ { D } ( d )$ are estimated via kernel density estimation (KDE), capturing the global traffic volume variation patterns of the resource.

During the generation phase, the algorithm randomly selects a historical sequence $S ^ { b a s e } \in \mathcal { S }$ as the base sequence, and samples a target upstream volume $U ^ { t g t }$ from the KDE distribution (the downstream sequence is generated analogously). The target volume is then allocated across the adjustable positions. Specifically, let the adjustable upstream frame vector to be generated be $\mathbf { x } = [ x _ { 1 } , \ldots , x _ { k } ] ^ { T }$ , with base values $\mathbf { x } ^ { b a s e }$ . This process is formulated as a constrained quadratic programming problem: under the constraints of total volume conservation and per-position value bounds, the objective is to minimize the deviation from the historical distribution weighted by variance. The optimization problem can be formally expressed as follows:

$$
\min _ {\mathbf {x}} \sum_ {i = 1} ^ {k} \frac {(x _ {i} - x _ {i} ^ {b a s e}) ^ {2}}{\sigma_ {i} ^ {2} + \epsilon}
$$

$$
\text { s.t. } \quad \sum_ {i = 1} ^ {k} x _ {i} = U ^ {t g t}, \tag {1}
$$

$$
b _ {i} ^ {m i n} \leq x _ {i} \leq b _ {i} ^ {m a x}, \quad \forall i
$$

where ϵ is a small constant introduced to prevent division by zero. After solving the above optimization problem using the Sequential Least Squares Programming algorithm [65], we further incorporate a greedy heuristic to discretize the continuous solution x and correct residual errors. This procedure produces augmented sequences for individual resources that conform to historical statistical patterns in both local frame size variations and overall traffic volume.

After performing application-layer frame sequence augmentation, we further introduce a forward temporal shifting mechanism to simulate the combined transmission behavior of request HEADER frames under HTTP/2 multiplexing. Given a flow-level frame sequence $S ^ { f l o w }$ , formed by aggregating the frame sequences of all resources within a flow, we define $\begin{array} { r } { { S ^ { f l o w } = [ S _ { 1 } , S _ { 2 } , \dots , S _ { N } ] } } \end{array}$ , where ${ { S } _ { t } } \mathrm { ~ = ~ } \left[ { { s } _ { t , 1 } } , { { s } _ { t , 2 } } , \ldots , { { s } _ { t , L _ { t } } } \right]$ denotes the frame sequence of the t-th resource. The algorithm then processes these sequences in a backward manner. For any request HEADER frames $s _ { t , j } > 0$ in $S _ { t }$ (for $t > 1 )$ , the algorithm removes it from the current sequence with probability $p _ { m o v e } = 0 . 2$ and inserts it after the request HEADER frames in the preceding resource sequence $S _ { t - 1 }$ . Frames that have been shifted forward may continue to move further upstream in subsequent iterations with probability $p _ { m o v e }$ , forming a cascading forward-shifting process. Through this mechanism, requests HEADER from multiple resources can form localized aggregation patterns within the flow-level frame sequence, effectively simulating the coalesced transmission behavior induced by HTTP/2 multiplexing and mitigating the strict temporal patterns introduced by naive resource concatenation.

# F. Cross-Layer Feature Alignment

Furthermore, to bridge the gap between application-layer frame sequences (FS) and transport-layer packet length sequences (PLS), we construct an intermediate proxy by generating an ideal packet length sequence from the frame sequence, and introduce a cross-layer feature alignment mechanism. In this mechanism, a teacher model equipped with framelevel semantic knowledge guides a student model to align its latent representations when processing observed packet length sequences. As a result, the model learns to suppress transmission perturbations and environmental noise.

First, we introduce an intermediate representation, termed the Generated Packet Length Sequence (GPLS), to mitigate the substantial discrepancies between FS and PLS in both feature dimensionality and value distribution. It represents a stable, idealized generation form of real traffic, free from transmission-induced perturbations such as buffering, fragmentation, and scheduling. In this form, each frame is independently encapsulated across protocol layers, yielding a packetlength structure that closely approximates an MSS-constrained segmentation pattern. Let a single application-layer data frame be denoted as $f _ { i } ,$ where $\operatorname { s g n } ( f _ { i } )$ indicates the transmission direction and $| f _ { i } |$ denotes its size. The reconstruction process consists of two sequential transformations. First, during crosslayer encapsulation, a fixed encapsulation and encryption overhead $\Delta _ { T L S }$ is added to each application-layer frame to account for protocol stack overhead 2, yielding the ideal encapsulated frame $f _ { i } ^ { \prime } { \mathrm { : } }$

Phase 1: Teacher Pre-training   
![](images/aeac9de07389f26420e1559e5a0bc96c690ed70c5485ac079a3aa2290466f3e5.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["AUG Set"] --> C["Teacher Model (Trainable)"]
    B["Train Set"] --> C
    C --> D["Cross-Entropy Loss"]
    style A fill:#f9f,stroke:#333
    style B fill:#f9f,stroke:#333
    style C fill:#bbf,stroke:#333
    style D fill:#dfd,stroke:#333
```
</details>

Phase 2: Cross-layer Distillation

![](images/567a0c69e88114488a5cf627e1e38609f47e1673669ca32a1a703b76198f36fa.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Train Set"] --> B["Pretrained Weights"]
    A --> C["Teacher Model (Frozen)"]
    A --> D["Student Model (Trainable)"]
    B --> E["KL-Divergence Loss"]
    B --> F["Cosine Similarity Loss"]
    B --> G["Cross-Entropy Loss"]
    C --> H["Distillation Loss"]
    D --> H
    E --> H
    F --> H
    G --> H
```
</details>

Phase 3: Deployment   
![](images/5ce35fe77d6f55712c3306e53518d9b67df55fa1dcdfcd6406a2538c60ddf2b1.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Test Set"] --> B["PLS"]
    B --> C["Student Model (Deployed)"]
    C --> D["Final Prediction"]
```
</details>

Fig. 6. Cross-layer feature alignment architecture.

$$
f _ {i} ^ {\prime} = \operatorname{sgn} (f _ {i}) (| f _ {i} | + \Delta_ {T L S}) \tag {2}
$$

Subsequently, based on the MSS threshold $\tau _ { M S S }$ of the target network environment, the encapsulated frame is subjected to idealized segmentation modeling. Specifically, when $| f ^ { \prime } i | >$ τMSS, it is sequentially divided into a packet length subsequence $P _ { i } .$ In this process, $P _ { i }$ consists of $k = \lfloor | f ^ { \prime } i | / \tau _ { M S S } \rfloor$ full-sized segments, along with an additional residual segment when the division is not exact, thereby characterizing the ideal segmentation structure.

$$
P _ {i} = \operatorname{sgn} (f _ {i}) \left[ \underbrace {\tau_ {M S S} , \dots , \tau_ {M S S}} _ {k}, | f _ {i} ^ {\prime} | \bmod \tau_ {M S S} \right] \tag {3}
$$

As shown in Fig. 6, based on the augmented data described above, we first perform supervised pretraining of a teacher model $\tau .$ It uses frame sequences to construct an ideal semantic representation space that is free from interference

$^ 2 \Delta _ { T L S }$ primarily consists of the fixed overhead introduced by the HTTP/2 frame header and the TLS Record layer. Under the widely used AES-GCM encryption mode, TLS 1.3 incurs approximately 31 bytes (including a 9B HTTP/2 frame header, 5B TLS Record header, 1B content type field, and 16B authentication tag), while TLS 1.2 introduces an additional ∼8B explicit initialization vector on top of this.

introduced by lower-layer transmission protocols. Given the GPLS $X _ { \mathrm { c l e a n } }$ and corresponding labels y from both the original training set and its augmented counterpart, the model parameters are optimized by minimizing a standard classification loss $\mathcal { L } _ { c l s } ^ { \mathcal { T } }$ (e.g., cross-entropy loss). After sufficient training, the teacher model can learn highly abstract and noise-robust semantic representations in its projection layer. Once training is complete, the parameters of the teacher model are frozen, and its output soft predictions and high-dimensional feature representations serve as reference targets for subsequent knowledge distillation [66].

During the cross-layer distillation stage, the student model (S) inherits the architecture and initialization of the teacher model and is trained on paired samples: the ideal sequence $X _ { \mathrm { c l e a n } }$ (GPLS) is fed into the teacher model, while the corresponding noisy observed sequence $X _ { \mathrm { n o i s y } }$ (PLS) is fed into the student model. To guide the student model to approximate the semantic space under noisy inputs, we introduce a softlabel distillation mechanism in the decision space based on the Kullback–Leibler (KL) divergence. Let $z _ { t }$ and $z _ { s }$ denote the logits produced by the teacher and student models, respectively. A temperature parameter $T$ is applied to soften the output distributions, and the objective is to minimize the discrepancy between the two predictive distributions:

$$
\mathcal {L} _ {k l} = T ^ {2} \cdot \mathcal {D} _ {K L} \left(\sigma \left(\frac {z _ {t}}{T}\right) \| \sigma \left(\frac {z _ {s}}{T}\right)\right) \tag {4}
$$

where $\sigma ( \cdot )$ denotes the Softmax function. This process enables the student model to capture the implicit inter-class structural relationships learned by the teacher model. To further mitigate the impact of fragmentation and cross-layer perturbations on sequence representations, we introduce a cosine alignment constraint in the latent feature space. Specifically, let $v _ { t }$ and $v _ { s }$ denote the feature vectors output by the projection layers of the teacher and student models, respectively. Feature alignment is achieved by minimizing their cosine distance, thereby enforcing directional consistency between the PLSbased representation and the GPLS-based representation in the feature space.

$$
\mathcal {L} _ {c o s} = 1 - \frac {1}{N} \sum_ {j = 1} ^ {N} \frac {v _ {s} ^ {(j)} \cdot v _ {t} ^ {(j)}}{\| v _ {s} ^ {(j)} \| _ {2} \| v _ {t} ^ {(j)} \| _ {2}} \tag {5}
$$

Finally, by including the supervision from ground-truth labels, the overall optimization objective of the student model is defined as $\mathcal { L } _ { s t u d e n t }$ , where $\alpha , \ \beta ,$ and $\gamma$ are weighting coefficients. In this multi-objective joint optimization framework, the student model is able to progressively approximate the stable semantic representations characterized by GPLS, starting from perturbed PLS inputs. It enables more robust traffic fingerprinting performance in real-world network environments.

$$
\mathcal {L} _ {\text { student }} = \alpha \mathcal {L} _ {c l s} ^ {\mathcal {S}} + \beta \mathcal {L} _ {k l} + \gamma \mathcal {L} _ {\text { cos }} \tag {6}
$$

# V. EVALUATION

# A. Experimental Setup

a) Dataset Construction: To validate the effectiveness of SATA, we construct an encrypted traffic dataset, as shown in Table I, to evaluate model robustness in complex conditions such as cross-region and cross-time scenarios. Data collection is executed within Docker containers, where each URL visit is driven by an independent subprocess. Browser interactions are automated using Playwright 3, while network traffic is captured by Tshark. In addition, TLS session keys are preserved to enable joint analysis of plaintext and encrypted traffic features. The augmented dataset (AUG) is built by the Singapore-A dataset. The training set consists of 70% of the Singapore-A data, with the remaining 15% used for validation during training and 15% reserved for testing. The training set contains both GPLS and their corresponding PLS, while the test set only includes observable PLS. Importantly, to strictly evaluate the adaptability of SATA under complex protocols such as HTTP/2, we use only HTTP/2 traffic in both training and evaluation stages.

TABLE I DATASET OVERVIEW. 

<table><tr><td>Dataset Name</td><td>Collection Date</td><td>Collection Location</td><td>Description</td><td>Number of Flows</td><td>Number of Traces</td></tr><tr><td>Singapore-A</td><td>2025/12</td><td>Singapore</td><td>Top-110 Alexa sites</td><td>160,604</td><td>5,500</td></tr><tr><td>SouthKorea-A</td><td>2025/12</td><td>South Korea</td><td>Top-110 Alexa sites</td><td>175,472</td><td>5,500</td></tr><tr><td>France-A</td><td>2025/12</td><td>France</td><td>Top-110 Alexa sites</td><td>70,703</td><td>5,500</td></tr><tr><td>Singapore-B</td><td>2026/01</td><td>Singapore</td><td>Top-110 Alexa sites</td><td>156,753</td><td>5,500</td></tr><tr><td>China-C</td><td>2025/03</td><td>China</td><td>Top-9853 China sites</td><td>334,414</td><td>9,853</td></tr></table>

b) Model and Hyperparameter Settings: The experimental evaluation employs commonly used deep learning models for WF, including FSNet [49], BERT-PS [55], Transformer, LSTM, and GRU. The main hyperparameters are configured as follows: the learning rate is set to $1 \times 1 0 ^ { - 4 }$ , and the maximum input sequence length is 500. Models are trained using the Adam optimizer. The maximum number of training epochs is set to 300, with early stopping terminating training if the validation F1 score does not improve for 15 consecutive epochs.

c) Experimental Environment: To ensure reproducibility, all experiments are conducted on a consistent computing platform. The software environment comprises Ubuntu 22.04, Python 3.12, and PyTorch 2.7.0. The hardware configuration is anchored by an NVIDIA RTX 5090 GPU (32 GB) and a 32-core Intel(R) Xeon(R) Gold 6459C CPU.

Our evaluation is structured to address the following research questions:

• RQ1: Performance. Does SATA significantly improve the classification accuracy and unknown-sample detection capabilities of representative baseline models across diverse scenarios?   
• RQ2: Effectiveness of Key Components. How do the individual components of SATA contribute to the overall performance enhancement?

3https://playwright.dev/

• RQ3: Robustness and Generalization. Can SATA maintain stable performance and resilience under highly volatile network conditions and complex deployment environments?   
• RQ4: Efficacy under Controlled Settings. Does SATA sustain its efficacy in controlled environments where dynamic noise is minimized?

# B. RQ1: Performance

a) Overall Performance: Table II presents the performance comparison across different datasets and models. Overall, the proposed method consistently yields stable performance improvements across all evaluation scenarios and model configurations, validating its effectiveness in various settings. In both cross-region scenarios (France-A and SouthKorea-A) and the cross-time scenario (Singapore-B), all models achieve varying degrees of performance improvement after incorporating the proposed method. In particular, under crossregion scenarios with more pronounced distribution shifts, the method achieves average improvements of 5.57% and 5.47% in ACC and F1, respectively, which are substantially higher than those observed in the closed-world setting (Singapore-A). It indicates that, by expanding resource composition patterns and mitigating structural perturbations, the proposed method effectively bridges the structural gap between source and target domains, thereby yielding more substantial gains under pronounced distribution shifts. From a model perspective, the method exhibits strong adaptability and architectural compatibility. Notably, larger improvements are observed in more expressive models such as BERT-PS and FSNet, with gains of up to 12.23%. It suggests that more expressive models can better leverage the enriched semantic information in the augmented data when modeling packet-length sequences.

b) Open-World Performance: To evaluate the performance of SATA in open-world scenarios, we use Singapore-A as the training set and conduct testing on France-A and China-C, where China-C is treated as unknown-class data to construct an open-world environment. During the inference stage, we further integrate several mainstream open-world recognition methods, including Softmax [35], OpenMax [67], and a series of KLND-based methods [68] (KLND-1, KLND-2, and KLND-3). These methods are integrated with FSNet to systematically evaluate performance under different openworld decision mechanisms.

Fig. 7 shows the performance improvements of FSNet in different open-world decision mechanisms after introducing the proposed method (FSNet+). The results show that, across all evaluation settings, the model achieves consistent improvements in ACC, F1, and AUROC, with particularly significant gains in ACC and AUROC, averaging 90.81% and 48.37%, respectively. It indicates that the proposed method not only enhances the model’s discriminative capability for known classes but also substantially improves its ability to identify unknown samples. In addition, the proposed method yields consistent performance gains across different open-world recognition methods, rather than relying on a specific decision strategy, further demonstrating its strong compatibility.

TABLE II PERFORMANCE IMPROVEMENTS OF SATA ACROSS DIFFERENT DATASETS AND MODELS. 

<table><tr><td rowspan="2">Methods</td><td colspan="2">Singapore-A</td><td colspan="2">France-A</td><td colspan="2">SouthKorea-A</td><td colspan="2">Singapore-B</td></tr><tr><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td></tr><tr><td>Transformer</td><td>73.24 (2.02%↑)</td><td>84.45 (0.84%↑)</td><td>64.78 (2.81%↑)</td><td>68.77 (2.44%↑)</td><td>52.53 (4.13%↑)</td><td>68.73 (2.15%↑)</td><td>62.55 (1.74%↑)</td><td>72.70 (1.28%↑)</td></tr><tr><td>LSTM</td><td>65.49 (1.07%↑)</td><td>79.93 (0.90%↑)</td><td>56.34 (3.39%↑)</td><td>61.10 (2.49%↑)</td><td>44.69 (2.26%↑)</td><td>58.54 (4.27%↑)</td><td>55.03 (1.07%↑)</td><td>67.22 (2.01%↑)</td></tr><tr><td>GRU</td><td>62.96 (0.83%↑)</td><td>76.71 (0.87%↑)</td><td>53.91 (2.71%↑)</td><td>59.43 (3.20%↑)</td><td>41.78 (3.78%↑)</td><td>55.14 (6.86%↑)</td><td>52.71 (1.40%↑)</td><td>65.42 (1.54%↑)</td></tr><tr><td>BERT-PS</td><td>83.92 (2.13%↑)</td><td>93.38 (0.88%↑)</td><td>44.88 (10.98%↑)</td><td>49.45 (7.14%↑)</td><td>39.91 (12.23%↑)</td><td>50.43 (8.96%↑)</td><td>70.92 (2.55%↑)</td><td>79.62 (1.82%↑)</td></tr><tr><td>FSNet</td><td>71.07 (5.81%↑)</td><td>82.77 (3.75%↑)</td><td>60.40 (5.76%↑)</td><td>62.90 (9.01%↑)</td><td>47.81 (7.66%↑)</td><td>61.79 (8.16%↑)</td><td>59.80 (5.43%↑)</td><td>70.81 (4.28%↑)</td></tr><tr><td>On Average</td><td>71.34 (2.37%↑)</td><td>83.45 (1.45%↑)</td><td>56.06 (5.13%↑)</td><td>60.33 (4.86%↑)</td><td>45.34 (6.01%↑)</td><td>58.93 (6.08%↑)</td><td>60.2 (2.44%↑)</td><td>71.15 (2.19%↑)</td></tr></table>

![](images/5c4fe17aa0615fca064742d13e46684d0d3fafd7bc4fb2e4e5a148979f7ce8cd.jpg)

<details>
<summary>bar</summary>

| Model | FSNet (%) | FSNet+ (%) |
| :--- | :--- | :--- |
| Softmax | 23.7 | 35.7 |
| OpenMax | 11.0 | 11.6 |
| KLND-1 | 18.5 | 32.5 |
| KLND-2 | 22.9 | 55.1 |
| KLND-3 | 23.4 | 54.8 |
</details>

(a) ACC

![](images/7474a4258ebb12f94e8181d45ff08f4b8e5e4dadf8da03999f8a808e49eee3d6.jpg)

<details>
<summary>bar</summary>

| Model | FSNet (%) | FSNet+ (%) |
| :--- | :--- | :--- |
| Softmax | 53.4 | 55.8 |
| OpenMax | 49.3 | 49.7 |
| KLND-1 | 48.6 | 49.4 |
| KLND-2 | 49.9 | 53.2 |
| KLND-3 | 49.7 | 52.5 |
</details>

(b) F1-score

![](images/2c3f1112aa9ff801f8223dd73205d8c4c9516925153129252688c383e210b704.jpg)

<details>
<summary>bar</summary>

| Model | FSNet (%) | FSNet+ (%) |
| :--- | :--- | :--- |
| Softmax | 50.8 | 75.7 |
| OpenMax | 52.5 | 72.3 |
| KLND-1 | 47.5 | 71.9 |
| KLND-2 | 51.8 | 77.8 |
| KLND-3 | 50.9 | 78.4 |
</details>

(c) AUROC   
Fig. 7. Performance improvements of SATA across different open-world recognition mechanisms.

Answer to RQ1: Experimental results demonstrate that SATA consistently outperforms representative baselines across all scenarios. Notably, it achieves a 5.47% average F1-score gain in cross-region deployments. In challenging open-world settings, SATA yields remarkable improvements, boosting average Acc and AUROC by 90.81% and 48.37%, respectively.

# C. RQ2: Effectiveness of Key Components

We evaluate the individual contribution of each key component to the overall performance through four distinct lenses: expansion of resource composition and frame sequence patterns, cross-layer feature alignment, and module ablation.

a) Effect of resource recomposition: To evaluate the effectiveness of the resource recomposition module, we remove the interference of dynamic resources and retain only a stable resource set. We then measure the coverage of resource composition patterns at both the flow and trace granularities. Specifically, we divide the dataset into train and test sets with an equal split, progressively increase the number of augmented samples generated, and compute the coverage between the resource composition patterns in the augmented training set and those in the test set.

The results in Fig. 8 show that the coverage of resource composition patterns between the train and test sets increases as the number of augmented samples grows. On the Singapore-A, SouthKorea-A, and France-A datasets, the flow-level coverage reaches up to 98.95%, 99.50%, and 99.49%, respectively, representing significant improvements over the baseline. In contrast, the improvement at the trace level is relatively limited. These results indicate that the proposed recomposition module can introduce richer composition patterns at the flow granularity, effectively expanding the pattern distribution of the training set.

It is worth noting that the above evaluation is based on a strict exact-match standard. Even in this constraint, the proposed method can generate resource composition patterns that are absent from the training set but genuinely present in the test set, demonstrating its ability to synthesize ‘unobserved yet feasible’ structures. Furthermore, despite the relatively limited resource diversity in the current test set, the coverage still improves consistently, indicating that the method can effectively expand the coverage of composition patterns within a constrained distribution space. Given that resource compositions in real-world environments are typically more diverse and exhibit more complex variations, the proposed method is expected to provide greater advantages in highly diverse out-of-distribution scenarios.

b) Effect of frame sequence augmentation: We evaluate the effectiveness of the proposed frame-sequence augmentation method. Using Venn diagrams, we analyze the pattern coverage relationships among the augmented data, training set, and test set at two granularities: resource-level frame sequences, corresponding to individual resources, and flowlevel frame sequences, corresponding to the aggregation of all resources within a flow. As shown in Fig. 9, the augmented dataset (AUG) constructed from Singapore-A is able to generate a large number of frame-sequence patterns that do not appear in the training set but genuinely exist in the test set, substantially expanding the data distribution. Using the SouthKorea-A dataset as the test set, as shown in Fig. 9(b) and Fig. 9(e), the augmented dataset introduces an additional 3,649 resource-level frame sequence patterns and 231 flowlevel frame sequence patterns, increasing the corresponding pattern coverage by 9.93% and 8.31%, respectively. This result directly demonstrates that the proposed frame sequence augmentation method can effectively uncover and supplement latent structural variants, compensating for the insufficient coverage of training data in the sequence pattern space.

![](images/7baeba5f93c358a60f7ec08e8738086a4285d1c26165a7df72538f86e6eb1f2f.jpg)

<details>
<summary>line</summary>

| Number of Samples | Flow   | Trace  |
| ----------------- | ------ | ------ |
| Base              | 97.60  | 94.89  |
| 5                 | 98.15  | 94.93  |
| 10                | 98.52  | 95.00  |
| 25                | 98.61  | 95.08  |
| 100               | 98.69  | 95.08  |
| 300               | 98.95  | 95.11  |
</details>

(a) Singapore-A

![](images/40f9cd25252cbff3718accfb01f936057011768dbb1a8ebe3032f9c3f391a2aa.jpg)

<details>
<summary>line</summary>

| Number of Samples | Flow   | Trace  |
| ----------------- | ------ | ------ |
| Base              | 98.55  | 95.85  |
| 5                 | 99.01  | 95.92  |
| 10                | 99.13  | 96.00  |
| 25                | 99.38  | 96.00  |
| 100               | 99.50  | 96.00  |
| 300               | 99.50  | 96.00  |
</details>

(b) SouthKorea-A

![](images/ca918d618a7d34d866157efb454ba095f817af078ec2a1bdda04b8d81fd653aa.jpg)

<details>
<summary>line</summary>

| Number of Samples | Flow   | Trace  |
| ----------------- | ------ | ------ |
| Base              | 98.98  | 99.11  |
| 5                 | 99.32  | 99.15  |
| 10                | 99.49  | 99.15  |
| 25                | 99.49  | 99.33  |
| 100               | 99.49  | 99.33  |
| 300               | 99.49  | 99.33  |
</details>

(c) France-A

Fig. 8. Impact of resource recomposition on pattern coverage at flow and trace granularities.   
![](images/701885726f4483efd1fb5a893345ff6830dbf60626864ef981fcafd5b6cd47da.jpg)

<details>
<summary>other</summary>

| Region | Count |
| :--- | :--- |
| August | 260501 |
| Singapore-A | 159963 |
| Singapore-B | 175988 |
| Intersection (A) | 36170 |
| Intersection (B) | 25112 |
| Intersection (C) | 16451 |
| All three | 2303 |
</details>

(a) Singapore-B@Resource

![](images/4893c7ba43e604d147392a74855ad0bc9ffbb8af3f8f58e05bb2dea3ffaf4576.jpg)

<details>
<summary>other</summary>

| Region | Count |
| :--- | :--- |
| AUG | 259155 |
| Singapore-A | 162820 |
| SouthKorea-A | 222388 |
| Both | 3649 |
| Intersection (A) | 38138 |
| Intersection (B) | 14483 |
| Intersection (C) | 22255 |
</details>

(b) SouthKorea-A@Resource

![](images/8c9f6a1b2b698fddf93cb534560712dee7d146afec952c5cfda9901cd35cec0e.jpg)

<details>
<summary>other</summary>

| Region       | Count  |
| ------------ | ------ |
| AUG only     | 261568 |
| Singapore-A  | 173890 |
| France-A     | 110099 |
| AUG ∩ Singapore-A | 48017 |
| France-A ∩ Singapore-A | 1236 |
| AUG ∩ Singapore-A | 4604 |
| France-A ∩ Singapore-A | 11185 |
</details>

(c) France-A@Resource

![](images/5beddebd974d3f7affc1fb34474a4902dd0cd633b426e003757417df79c44bbf.jpg)

<details>
<summary>other</summary>

| Region | Count |
| :--- | :--- |
| AUG only | 85062 |
| Singapore-A only | 70377 |
| Singapore-B only | 74356 |
| Both (AUG ∩ Singapore-A) and (AUG ∩ Singapore-B) | 8133 |
| Both (Singapore-A ∩ Singapore-B) and (AUG ∩ Singapore-B) | 3268 |
| All three categories | 303 |
</details>

(d) Singapore-B@Flow

![](images/2d189ac0949cf24a62aba3b05a191ad22bfb2fa7a48811dc9e8d1e3ff961c3fc.jpg)

<details>
<summary>other</summary>

| Region | Count |
| :--- | :--- |
| AUG only | 85134 |
| Singapore-A only | 73757 |
| SouthKorea-A only | 90179 |
| Both (AUG ∩ Singapore-A) and (AUG ∩ SouthKorea-A) | 231 |
| Both (Singapore-A ∩ SouthKorea-A) and (AUG ∩ Singapore-A ∩ SouthKorea-A) | 1557 |
| All three categories are shared by 9844. The triple intersection between the two groups is 231. The overlapping region contains 9844 elements.
</details>

(e) SouthKorea-A@Flow

![](images/9a1562bda83a9b40ec4efe8f4fa46273c5fb833c97aee2c3c3e0c8666d8f31af.jpg)

<details>
<summary>other</summary>

| Region | Count |
| :--- | :--- |
| AUG only | 85291 |
| Singapore-A only | 74688 |
| France-A only | 35448 |
| Both (AUG ∩ Singapore-A) and (AUG ∩ France-A) | 11074 |
| Both (AUG ∩ Singapore-A ∩ France-A) and (AUG ∩ Singapore-A ∩ France-A) | 327 |
| All three categories | 74 |
</details>

(f) France-A@Flow

Fig. 9. Impact of frame sequence augmentation on pattern coverage at resource and flow granularities.   
![](images/008e4a7d156b5f7ba9d9a0378763e5f6bdaed622ad6cca565481c8749558e568.jpg)

<details>
<summary>bar_stacked</summary>

| Region | Others (×10⁵) | Overlap between GPLS and PLS (%) |
| :--- | :--- | :--- |
| Singapore-A | 1.1 | 30.7 |
| SouthKorea-A | 1.2 | 32.3 |
| France-A | 0.55 | 21.8 |
| Singapore-B | 1.05 | 31.9 |
</details>

Fig. 10. Overlap between GPLS and real PLS across datasets.

c) Effect of feature alignment: As shown in Fig. 10, we analyze the necessity and validity of the proposed generated packet length sequence. Results across the four datasets show that the generated packet length sequence (GPLS) from frame sequences exactly matches the real packet length sequence (PLS) in nearly 30% of cases. This finding first indicates that the network protocol stack indeed introduces substantial nonlinear perturbations into PLS during transmission, rendering the mapping from application semantics to physical observations inherently uncertain. More importantly, it also validates the necessity and validity of the constructed GPLS, which, to some extent, captures the packet length generation process in the absence of transmission perturbations. Thus, it provides an effective approximation for bridging application semantics and physical observations.

![](images/21f531af933e8e7c28ce4bb0095ffbd6fbae95de702c2912054ae29d36c489fb.jpg)

<details>
<summary>bar</summary>

| Region       | PLS   | GPLS  | FS    |
| ------------ | ----- | ----- | ----- |
| Singapore-A  | 1.44  | 14.86 | 15.37 |
| SouthKorea-A | 2.12  | 13.62 | 14.37 |
| France-A     | 1.64  | 18.64 | 18.99 |
</details>

Fig. 11. Robustness evaluation of different feature levels against transmission perturbations.

Fig. 11 measures the stability of different feature representations while keeping the resource composition within each flow unchanged. The results show that, for PLS, only about 1.73% of flows remain stable on average, indicating that PLS is highly sensitive to low-level transmission perturbations. In contrast, higher-level feature representations, namely frame sequences (FS) and the GPLS, exhibit average stability levels approximately 9.37× and 9.06× that of PLS, respectively, demonstrating markedly stronger robustness. This finding confirms that higher-level representations are substantially more resilient to cross-layer perturbations and helps explain why low-level features alone are poor for stable representation learning. It further motivates our feature alignment method, which leverages application-layer semantic guidance to encourage more consistent and noise-robust PLS representations.

TABLE III PERFORMANCE COMPARISON OF DIFFERENT FEATURE REPRESENTATIONS AND ABLATION STUDY. 

<table><tr><td rowspan="2">Feature/Methods</td><td colspan="2">France-A</td><td colspan="2">SouthKorea-A</td></tr><tr><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td></tr><tr><td>GPLS+</td><td>64.93 (7.50%↑)</td><td>71.28 (13.32%↑)</td><td>54.05 (13.05%↑)</td><td>73.19 (18.45%↑)</td></tr><tr><td>FS</td><td>65.78 (8.91%↑)</td><td>70.49 (12.07%↑)</td><td>53.84 (12.61%↑)</td><td>71.42 (15.59%↑)</td></tr><tr><td>GPLS</td><td>62.86 (4.07%↑)</td><td>69.23 (10.06%↑)</td><td>51.70 (8.14%↑)</td><td>70.95 (14.82%↑)</td></tr><tr><td>SATA</td><td>63.88 (5.76%↑)</td><td>68.57 (9.01%↑)</td><td>51.47 (7.66%↑)</td><td>66.83 (8.16%↑)</td></tr><tr><td>SATA w/o RR</td><td>64.18 (6.26%↑)</td><td>67.73 (7.68%↑)</td><td>51.31 (7.32%↑)</td><td>65.77 (6.44%↑)</td></tr><tr><td>SATA w/o FSA</td><td>62.66 (3.74%↑)</td><td>66.4 (5.56%↑)</td><td>50.07 (4.73%↑)</td><td>64.58 (4.52%↑)</td></tr><tr><td>SATA w/o AUG</td><td>62.79 (3.96%↑)</td><td>66.5 (5.72%↑)</td><td>50.52 (5.67%↑)</td><td>65.34 (5.75%↑)</td></tr><tr><td>PLS</td><td>60.40</td><td>62.90</td><td>47.81</td><td>61.79</td></tr></table>

Table III presents the performance comparison of different features on FSNet. Compared with the PLS, both GPLS and FS yield significant performance gains across datasets, with FS achieving the largest F1 improvement of 15.59% on SouthKorea-A. Overall, as the feature moves from PLS to GPLS and further to FS, model performance improves consistently, which aligns with the observation in Fig. 11 that higher-level features exhibit stronger stability. Furthermore, after joint training with GPLS generated from the AUG dataset, GPLS+ improves F1 by 13.32% and 18.45% over PLS on France-A and SouthKorea-A, respectively. It indicates that frame sequence augmentation can effectively expand the application-layer feature distribution and enhance its discriminative capability. Finally, although SATA uses only PLS as input during testing, it still achieves an average F1 improvement of 8.56% over PLS and approaches the performance of GPLS. It demonstrates that cross-layer feature alignment can guide observed features to approximate more stable application-layer semantic representations, improving overall classification performance.

d) Ablation Study: We conduct an ablation study to analyze the contribution of each key module to the overall performance. Specifically, we compare the full method (SATA) with variants that remove the resource recomposition module (w/o RR), remove the frame sequence augmentation module (w/o FSA), and exclude augmented data (w/o AUG). In the w/o AUG setting, the teacher model is trained solely on GPLS derived from the original training set.

The results in Table III show that the proposed method outperforms all ablation variants on both datasets, indicating that each module provides effective gains. Removing RR leads to a slight performance drop, suggesting that resource composition modeling helps expand high-level semantic patterns. Removing FSA causes a more pronounced degradation, demonstrating that frame sequence augmentation plays a critical role in expanding the frame sequence pattern space. Notably, w/o AUG still outperforms w/o FSA, indicating that, without FSA, naively assembled GPLS deviates substantially from the real distribution. It further verifies the importance of FSA in structural correction and realism enhancement. Meanwhile, w/o AUG still significantly outperforms the PLS, showing that even without augmented data, the cross-layer feature alignment mechanism can effectively transfer highlevel semantic knowledge to low-level features. Overall, RR, FSA, and the cross-layer feature alignment module improve representation stability and discriminative capability from the perspectives of pattern expansion and feature alignment, respectively, validating the effectiveness and rationality of the proposed design.

Answer to RQ2: The results indicate that all three modules contribute substantially to performance gains. The first two reconstruct realistic yet unobserved resource composition and frame-sequence patterns, while the feature alignment module improves the stability of packet-length sequence representations.

TABLE IV PERFORMANCE IMPROVEMENTS OF SATA IN FEW-SHOT SETTINGS. 

<table><tr><td rowspan="2">Methods</td><td colspan="2">Singapore-A</td><td colspan="2">France-A</td><td colspan="2">SouthKorea-A</td><td colspan="2">Singapore-B</td></tr><tr><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td></tr><tr><td>FSNet-3</td><td>32.14 (30.96%↑)</td><td>42.38 (25.79%↑)</td><td>27.84 (24.60%↑)</td><td>32.79 (23.30%↑)</td><td>21.02 (29.88%↑)</td><td>30.00 (28.87%↑)</td><td>26.48 (27.79%↑)</td><td>36.45 (22.36%↑)</td></tr><tr><td>FSNet-10</td><td>54.27 (17.91%↑)</td><td>67.24 (13.37%↑)</td><td>45.12 (13.30%↑)</td><td>49.83 (14.89%↑)</td><td>34.08 (18.87%↑)</td><td>47.21 (19.76%↑)</td><td>43.35 (15.52%↑)</td><td>55.39 (13.59%↑)</td></tr><tr><td>FSNet-20</td><td>69.05 (1.04%↑)</td><td>80.48 (1.14%↑)</td><td>53.95 (4.97%↑)</td><td>58.72 (4.89%↑)</td><td>42.31 (6.88%↑)</td><td>56.39 (8.19%↑)</td><td>52.87 (4.50%↑)</td><td>65.62 (1.74%↑)</td></tr><tr><td>FSNet-50</td><td>71.07 (5.81%↑)</td><td>82.77 (3.75%↑)</td><td>60.40 (5.76%↑)</td><td>62.90 (9.01%↑)</td><td>47.81 (7.66%↑)</td><td>61.79 (8.16%↑)</td><td>59.80 (5.43%↑)</td><td>70.81 (4.28%↑)</td></tr><tr><td>On Average</td><td>56.63 (13.93%↑)</td><td>68.22 (11.01%↑)</td><td>46.83 (12.16%↑)</td><td>51.06 (13.02%↑)</td><td>36.31 (15.82%↑)</td><td>48.85 (16.24%↑)</td><td>45.63 (13.31%↑)</td><td>57.07 (10.49%↑)</td></tr></table>

# D. RQ3: Robustness and Generalization

We further investigate the robustness and generalization of our method by analyzing its performance across several key dimensions: few-shot settings, feature granularity, class scale, and feature length.

a) Few-Shot: Table IV presents the data generation and feature enhancement capability of the proposed method in fewshot settings. The results show that, even in extremely datascarce conditions, where only three access traces per website are used for training (FSNet-3), the proposed method remains effective and achieves significant performance gains. Across the four datasets, the average F1 improvement reaches 25.08%, demonstrating the strong effectiveness of the proposed mechanism in clearing severe data scarcity. In addition, from the overall cross-dataset performance, the proposed method consistently yields substantial gains across all datasets, improving ACC by 12.16%-15.82% and F1 by 10.49%-16.24% on average. These results indicate that SATA exhibits strong robustness and cross-environment generalization. Even when training samples are extremely limited, it can effectively enhance the model’s discriminative ability and representation quality, substantially reducing the model’s dependence on large-scale, high-quality labeled data.

TABLE V PERFORMANCE IMPROVEMENTS ACROSS FEATURE GRANULARITIES. 

<table><tr><td rowspan="2">Methods</td><td colspan="2">Singapore-A</td><td colspan="2">France-A</td></tr><tr><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td></tr><tr><td>UDFS</td><td>91.20</td><td>91.05</td><td>50.23</td><td>45.09</td></tr><tr><td>PLS-Trace</td><td>90.82</td><td>90.74</td><td>27.42</td><td>23.66</td></tr><tr><td>PLS</td><td>71.07</td><td>82.77</td><td>60.40</td><td>62.90</td></tr><tr><td> $UDFS^{+}$ </td><td>91.56</td><td>91.33</td><td>54.49</td><td>47.52</td></tr><tr><td> $PLS-Trace^{++}$ </td><td>90.94</td><td>90.89</td><td>37.26</td><td>32.58</td></tr><tr><td> $PLS^{++}$ </td><td>75.20</td><td>85.87</td><td>63.88</td><td>68.57</td></tr><tr><td>On Average</td><td>84.36 (1.82%↑)</td><td>88.19 (1.33%↑)</td><td>46.02 (12.73%↑)</td><td>43.88 (12.93%↑)</td></tr></table>

b) Feature Granularity: Table V presents the performance improvements of the proposed method at different granularities of features, including trace-level UDFS and PLS-Trace features, as well as flow-level PLS features. Among them, UDFS [59] is a trace-level statistical sequence feature constructed by sequentially concatenating the upstream and downstream transmitted byte volumes of each flow within the same trace, while PLS-Trace globally merges all packet length sequences within the entire trace. It should be noted that PLS-based features are enhanced using the complete proposed method, denoted $\mathrm { b y \ ^ { + + } }$ , whereas UDFS is augmented only with the resource recomposition module, denoted by +.

The results show that, after introducing SATA, all types of features achieve consistent improvements in both ACC and F1 on the closed-world dataset (Singapore-A) and the crossdomain dataset (France-A), with the average improvement in the cross-domain scenario exceeding 12%. This result fully demonstrates the effectiveness and generalizability of the proposed augmentation mechanism. Notably, since UDFS features are constructed solely through the recomposition of flow-level macroscopic statistics, the performance gains of $\mathrm { U D F S ^ { + } }$ can be entirely attributed to the resource recomposition module. It further provides strong evidence that the module can generate plausible resource composition patterns and effectively expand the boundaries of the pattern space.

In addition, by comparing the performance of features at different granularities, we observe a notable phenomenon: tracelevel features, including UDFS and PLS-Trace, perform well on the Singapore-A dataset, with F1 scores exceeding 90%. However, they suffer from significant performance degradation on the cross-domain France-A dataset. For example, the F1 score of PLS-Trace drops to 23.66%. A possible reason is that local distribution shifts at the flow level introduce error accumulation and sequence misalignment during global aggregation, causing substantial representation degradation and feature collapse for trace-level features in cross-domain scenarios.

TABLE VI PERFORMANCE IMPROVEMENTS IN DIFFERENT NUMBERS OF CLASSES. 

<table><tr><td rowspan="2">Methods</td><td colspan="2">Singapore-A</td><td colspan="2">France-A</td></tr><tr><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td></tr><tr><td>FSNet@5</td><td>95.45 (3.32%↑)</td><td>95.51 (3.28%↑)</td><td>87.61 (3.86%↓)</td><td>87.77 (0.60%↑)</td></tr><tr><td>FSNet@10</td><td>90.54 (2.93%↑)</td><td>91.42 (2.96%↑)</td><td>77.98 (2.33%↑)</td><td>83.69 (1.05%↑)</td></tr><tr><td>FSNet@30</td><td>81.94 (3.53%↑)</td><td>85.99 (3.09%↑)</td><td>67.60 (1.79%↑)</td><td>70.59 (4.87%↑)</td></tr><tr><td>FSNet@110</td><td>71.07 (5.81%↑)</td><td>82.77 (3.75%↑)</td><td>60.40 (5.76%↑)</td><td>62.90 (9.01%↑)</td></tr><tr><td>On Average</td><td>84.75 (3.90%↑)</td><td>88.92 (3.27%↑)</td><td>73.40 (1.51%↑)</td><td>76.24 (3.89%↑)</td></tr></table>

TABLE VII PERFORMANCE IMPROVEMENTS IN DIFFERENT SEQUENCE LENGTHS. 

<table><tr><td rowspan="2">Methods</td><td colspan="2">Singapore-A</td><td colspan="2">France-A</td></tr><tr><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td></tr><tr><td>FSNet-100</td><td>65.60 (12.58%↑)</td><td>77.12 (8.71%↑)</td><td>56.44 (8.13%↑)</td><td>59.58 (8.68%↑)</td></tr><tr><td>FSNet-200</td><td>66.71 (12.74%↑)</td><td>79.58 (7.78%↑)</td><td>57.34 (11.58%↑)</td><td>61.70 (10.47%↑)</td></tr><tr><td>FSNet-500</td><td>71.07 (5.81%↑)</td><td>82.77 (3.75%↑)</td><td>60.40 (5.76%↑)</td><td>62.90 (9.01%↑)</td></tr><tr><td>On Average</td><td>67.79 (10.38%↑)</td><td>79.82 (6.75%↑)</td><td>58.06 (8.49%↑)</td><td>61.39 (9.39%↑)</td></tr></table>

c) Number of Classes: Table VI shows the impact of the number of classes k on performance. As k increases, stronger inter-class similarity and denser decision boundaries make the task more challenging, leading to performance degradation. Nevertheless, the proposed method consistently delivers stable gains across all scales, demonstrating robustness to class expansion. Notably, on the cross-domain France-A dataset, it achieves an average F1 improvement of 3.89%, with larger gains at higher scales k = 110. It indicates that the method effectively mitigates challenges such as data sparsity and feature overlap, exhibiting strong scalability in complex settings.   
d) Feature Length: Table VII presents the performance under different PLS truncation lengths, where FSNet-100/200/500 denotes using the first 100, 200, and 500 packet lengths as input, respectively. Overall, as the truncation length increases, the model can access more complete sequence information, leading to gradual improvements in absolute performance. Meanwhile, the proposed method consistently brings stable gains at all length settings, achieving an average F1 improvement of 9.39% on the France-A dataset. It indicates that the method can effectively improve model performance regardless of whether the input information is limited, demonstrating strong adaptability and robustness at different observation conditions and enabling stable effectiveness across multiple feature scales.

Answer to RQ3: Experimental results demonstrate that SATA consistently bolsters model performance under complex conditions, exhibiting superior robustness and generalization capabilities across volatile environments.

# E. RQ4: Efficacy under Controlled Settings

We further construct a controlled dataset to eliminate the influence of dynamic application-layer resource variation and scheduling, enabling a more accurate evaluation of SATA.

First, Table VIII ensures cross-domain resource homogeneity at the flow level, excluding noise introduced by resource composition variation with an ideal stable-flow setting. In this controlled condition, the overall performance of the baseline model improves substantially. Meanwhile, even in the generation setting without resource recomposition (w/o RR), the F1 improvements on the Singapore-A and SouthKorea-A datasets reach 2.1% and 6.67%, respectively, both of which are higher than those observed in the standard experiments in Table II. It indicates that, after excluding the influence of resource composition variation, the proposed method can effectively mitigate structural perturbations introduced during transmission by enhancing frame-sequence patterns and performing cross-layer feature alignment.

Furthermore, Table IX constructs an ideal stable-webpage setting in which the resource sets are strictly isomorphic across domains. In this clean environment, where interference from dynamic resources is excluded, the benefits of the proposed augmentation strategy are further increased, with the relative F1 gains on the two datasets increasing to 2.84% and 8.54%, respectively. This improvement beyond the results in Table VIII demonstrates the necessity of resource recomposition. It shows that, when the core resource pool of a webpage remains stable, the framework can efficiently generate plausible dynamic resource composition patterns, providing an effective solution for addressing the impact of resource composition variation.

TABLE VIII PERFORMANCE IMPROVEMENTS IN STABLE-FLOW SETTING. 

<table><tr><td rowspan="2">Methods</td><td colspan="2">Singapore-A</td><td colspan="2">SouthKorea-A</td></tr><tr><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td></tr><tr><td>Transformer</td><td>76.09 (1.85%↑)</td><td>84.53 (1.55%↑)</td><td>65.61 (5.75%↑)</td><td>72.30 (4.92%↑)</td></tr><tr><td>LSTM</td><td>67.31 (2.21%↑)</td><td>78.66 (1.18%↑)</td><td>56.13 (4.49%↑)</td><td>65.49 (3.65%↑)</td></tr><tr><td>GRU</td><td>65.18 (1.46%↑)</td><td>76.52 (1.36%↑)</td><td>53.64 (2.05%↑)</td><td>59.82 (5.78%↑)</td></tr><tr><td>BERT-PS</td><td>88.67 (1.29%↑)</td><td>94.06 (0.85%↑)</td><td>41.24 (10.31%↑)</td><td>45.98 (9.05%↑)</td></tr><tr><td>FSNet</td><td>72.48 (8.06%↑)</td><td>81.39 (5.57%↑)</td><td>60.48 (9.42%↑)</td><td>65.31 (9.97%↑)</td></tr><tr><td>On Average</td><td>73.95 (2.97%↑)</td><td>83.03 (2.10%↑)</td><td>55.42 (6.40%↑)</td><td>61.78 (6.67%↑)</td></tr></table>

TABLE IX PERFORMANCE IMPROVEMENTS IN STABLE-WEBPAGE SETTING. 

<table><tr><td rowspan="2">Methods</td><td colspan="2">Singapore-A</td><td colspan="2">SouthKorea-A</td></tr><tr><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td></tr><tr><td>Transformer</td><td>83.87 (1.48%↑)</td><td>88.52 (0.98%↑)</td><td>74.60 (3.43%↑)</td><td>77.31 (2.03%↑)</td></tr><tr><td>LSTM</td><td>68.29 (6.57%↑)</td><td>76.33 (5.03%↑)</td><td>58.13 (10.41%↑)</td><td>61.15 (12.95%↑)</td></tr><tr><td>GRU</td><td>72.34 (0.08%↑)</td><td>78.96 (0.84%↑)</td><td>61.21 (2.19%↑)</td><td>64.19 (3.79%↑)</td></tr><tr><td>BERT-PS</td><td>93.50 (1.03%↑)</td><td>96.14 (0.86%↑)</td><td>41.87 (15.64%↑)</td><td>42.75 (13.82%↑)</td></tr><tr><td>FSNet</td><td>78.23 (9.88%↑)</td><td>83.90 (6.50%↑)</td><td>67.47 (12.41%↑)</td><td>70.20 (10.10%↑)</td></tr><tr><td>On Average</td><td>79.25 (3.81%↑)</td><td>84.77 (2.84%↑)</td><td>60.66 (8.82%↑)</td><td>63.12 (8.54%↑)</td></tr></table>

Answer to RQ4: The results under controlled settings demonstrate that the performance gains of SATA originate from the intrinsic effectiveness of its module design, rather than being artifactually driven by environmental noise.

# VI. DISCUSSION AND FUTURE WORK

First, SATA is specifically designed for mechanisms such as multiplexing and currently focuses on the HTTP/2 protocol. Given the prevalence of HTTP/2 in modern networks and our core focus on structural perturbations induced by multiplexing and cross-layer encapsulation, this specialization ensures a targeted and effective analysis in website fingerprinting.

Second, consistent with established literature like Rosetta [27], SATA primarily addresses the network transmission process. While it does not explicitly model the long-term evolution of web resources, the framework provides a robust foundation that can be extended to accommodate additional distribution shifts introduced by content changes.

Finally, while SATA demonstrates exceptional efficacy on packet-length sequences, it currently concentrates on this primary side channel rather than auxiliary features like timing. Generalizing this cross-layer modeling to a multi-modal feature space represents a promising direction for future research.

# VII. CONCLUSION

This paper presents SATA, a semantics-aware traffic augmentation framework for addressing the systematic shift between application semantics and observable traffic features in real-world environments. Under protocol constraints, SATA expands resource-composition and frame-sequence patterns to enrich application-layer semantic representations, and introduces a cross-layer feature alignment module that distills enhanced semantics to align with observable packet-length features, improving representation stability. Extensive evaluations demonstrate that SATA not only synthesizes traffic patterns that are absent in the training set but present in the test set, but also consistently improves the performance of mainstream models across diverse and complex scenarios, validating its effectiveness in mitigating systematic feature shifts in realistic settings.

# APPENDIX A STABILITY ANALYSIS OF RESOURCE COMPOSITION AND PROTOCOL

To further validate the objective existence of the discussed challenges and the rationale for focusing on HTTP/2-specific modeling, we provide additional statistical analysis on the stability of resource compositions and protocol-level behaviors.

![](images/75f9785958457400a0ae56887c09bd2f8b5e882a5356ae5724af86676e378fef.jpg)

<details>
<summary>bar_stacked</summary>

| Country | Others (×10⁵) | Stable Flows (%) |
| :--- | :--- | :--- |
| Singapore-A | 1.25 | 39.2 |
| SouthKorea-A | 1.45 | 36.5 |
| France-A | 0.35 | 58.8 |
</details>

Fig. 12. Stable flow ratio across datasets.

![](images/4c16814647d3741000baa855cb31f888e532d56f0cf4b259a03a0d32d6581f57.jpg)

<details>
<summary>bar</summary>

| Region | Stable Flow Ratio (%) |
| :--- | :--- |
| Singapore-A | 22.4 |
| SouthKorea-A | 22.1 |
| France-A | 16.7 |
</details>

Fig. 13. Resource consistency in stable subset.

a) Stability of resource composition within Flows: We first examine the consistency of the resource set carried by a single flow for the same webpage across different traffic traces. As shown in Fig. 12, across all datasets, the proportion of stable flows, defined as flows whose resource composition remains similar across all traces, does not exceed 45% on average. It indicates that even when accessing the same webpage, the set of resources within a flow can vary due to factors such as dynamic web content and network scheduling strategies.

To further eliminate the influence of intrinsic webpage content dynamics, we restrict the analysis to a subset of stable resources. As shown in Fig. 13, even when considering only these stable resources, more than 20% of flows still exhibit inconsistent resource composition patterns on average. It provides strong empirical evidence for the existence of C1, demonstrating that the instability of in-flow resource compositions is not solely caused by content variation, but is also closely related to resource scheduling and protocol-level mechanisms.

b) Protocol-level Variability: Finally, we analyze the distribution of different application-layer protocols and their impact on FSNet classification performance. As shown in Fig. 14, we present both the proportion of various TCP applicationlayer protocols across datasets and their distribution within misclassified samples. Notably, the Unknown category typically corresponds to pre-connection requests without an actual payload. The results show that HTTP/2 dominates overall traffic, which is consistent with existing measurement reports 4. Meanwhile, HTTP/2 also accounts for a significantly higher proportion of misclassified samples compared to HTTP/1.

Furthermore, as illustrated in Fig. 15, the classification error rate of HTTP/2 is substantially higher than that of HTTP/1, exceeding it by approximately 86.7%. It indicates that HTTP/2 is not only the dominant protocol in the dataset but also the primary source of model misclassification. Its characteristics, such as multiplexing, dynamic header compression, and complex scheduling mechanisms, introduce stronger structural perturbations, making it more challenging for models to learn stable discriminative features. These findings highlight the necessity and rationality of focusing on HTTP/2-specific modeling and enhancement.

![](images/ce5f3624be22284b9d7c09464ce8a29d14e6a33c50dc4e60dd08578ae3d21631.jpg)

<details>
<summary>bar</summary>

| Category | Protocol Distribution (%) | Misclassification Distribution (%) |
| :--- | :--- | :--- |
| HTTP/2 | 66.4 | 69.0 |
| Unknown | 24.2 | 25.8 |
| HTTP/1 | 9.4 | 5.2 |
</details>

Fig. 14. Protocol distribution in the dataset and misclassified samples.

4https://radar.cloudflare.com/en-us/year-in-review/2025

![](images/183c8249ab3d185ddcfe8cbd6970787c87af3286fc58af128f83fef274502b0d.jpg)

<details>
<summary>bar</summary>

| Category | Classification Error Rate (%) |
| :--- | :--- |
| HTTP/2 | 46.3 |
| Unknown | 47.5 |
| HTTP/1 | 24.8 |
</details>

Fig. 15. Classification error rate of different protocol.

# APPENDIX B RESOURCE COMPOSITION VARIABILITY

To further intuitively illustrate the causes of resource composition variations within a flow, Fig. 16 provides an intuitive description of the interaction process between dynamic DNS and HTTP/2 connection coalescing. In real-world networks, influenced by dynamic DNS mechanisms such as CDN scheduling, logically independent cross-domain requests are often resolved to the same physical edge server. For example, when a client establishes a TLS connection $C _ { 1 }$ with emp.bbci.co.uk, the server typically provides a certificate containing a SAN list that covers multiple related domains. If the client subsequently requests resources from static.files.bbci.co.uk and the domain resolves to the same IP address, the browser performs HTTP/2 connection coalescing validation. If the connection $C _ { 1 }$ remains active, the IP address matches exactly, and the new domain is included in the SAN list, the browser avoids establishing a new connection and instead reuses $C _ { 1 }$ to transmit subsequent requests.

![](images/75bc2a6cb5e3253d8d7e69185f82046e44adbeca03d202c1710e233c222abdc0.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Browser"] --> B["Resolve emp.bbci.co.uk"]
    B --> C["IP: 88.221.168.120"]
    C --> D["Create H2"]
    D --> E["connection C1 (SAN=SAN1)"]
    E --> F["C1 is still alive"]
    F --> G["static.files.bbci.co.uk is covered by SAN1"]
    G --> H["H2 connection multiplexing verification"]
    H --> I["When all met, reuse connection C1"]
    I --> J["If not met, create H2 connection C2"]
    J --> K["×509ce.dNSName&quot;: {&quot;www.bbc.co.uk&quot;, &quot;*.bbcimg.co.uk&quot;, &quot;*.bbc.co.uk&quot;, &quot;*.api.bbci.co.uk&quot;, &quot;*.api.bbci.com&quot;, &quot;wsdownload.bbco.co.uk&quot;, &quot;static.bbco.co.uk&quot;, &quot;polling.bbco.co.uk&quot;, &quot;open.live.bbco.co.uk&quot;, &quot;newsrss.bbco.co.uk&quot;, &quot;newsmbc.co.uk&quot;, &quot;ichef.bbco.co.uk&quot;, &quot;ichef-1.bbco.co.uk&quot;, &quot;emp.bbco.co.uk&quot;, &quot;downloads.bbco.co.uk&quot;, &quot;cdnedge.bbco.co.uk&quot;, &quot;bbc.co.uk"]
```
</details>

Fig. 16. An illustration of the HTTP/2 connection coalescing mechanism. It demonstrates how cross-domain resources are aggregated into the same underlying TLS flow due to dynamic DNS resolution to the same IP and TLS certificate SAN matching.

At the same time, even for resources within the same domain, requests are not always multiplexed over a single connection. This may occur when the number of concurrent streams reaches implementation limits, when the connection times out, or when either endpoint actively closes the connection, rendering the existing connection $C _ { 1 }$ unavailable for reuse. As a result, subsequent requests from the same domain may be routed to new connections, leading to resource dispersion across multiple flows.

This protocol-level optimization, while designed to improve transmission efficiency, ultimately leads to two types of non-deterministic behaviors: flow-level aggregation of crossdomain resources and flow-level dispersion of same-domain resources. From the perspective of a traffic observer, such dynamic reorganization not only alters the actual resource set and traffic volume carried by a flow but also disrupts the stable mapping between application-layer webpage semantics and observation-layer packet length sequences. As a result, it introduces significant distribution shifts in the feature space. This mechanism fundamentally explains the origin of the application-layer resource composition variation generalization challenge discussed in this work.

# APPENDIX CFRAME SEQUENCE VARIATIONS FOR A SINGLE RESOURCE

To further characterize the variability of frame sequences, we analyze them from both microscopic and macroscopic perspectives.

First, at the microscopic level, as shown in Fig. 17, the frame sequences corresponding to the same resource exhibit a clear static dynamic separation. On the one hand, some frames remain highly stable at specific temporal positions. For example, the DATA1 frame consistently maintains a fixed size of about 173 bytes across multiple observations, reflecting the stable encapsulation of fixed-structure data units at the protocol layer. On the other hand, frame lengths also exhibit nondeterministic variations. For instance, the server may append a 0-byte DATA frame at the end of transmission to indicate the end-of-stream state. In addition, during cross-layer encapsulation, the same logical payload may be segmented into different data chunks across visits due to asynchronous I/O buffer scheduling at the server side and dynamic changes in the HTTP/2 flow-control window. As a result, frame lengths may vary within a certain range at local temporal positions, as illustrated by DATA1 and DATA2 in Fig. 17b. This characteristic, where stable structure and random perturbation coexist, leads to pronounced instability in frame sequences at the microscopic level. It also constitutes a key source of structural noise introduced during cross-protocol-stack encapsulation and scheduling.

1.简述资源组合模式变化的协议流程 Second, at the macroscopic level, as shown in Fig. 17, 2.放一个SAN的内容，对应这个 we observe that although frame sequences exhibit significant local changes at the microscopic level, their total upstream and downstream traffic volumes still approximately follow a multimodal distribution. Further analysis shows that this discretized distribution mainly arises from the state-dependent nature of HPACK dynamic compression, together with variations in request parameters and header fields, Huffman encoding, and other factors. The Wireshark 5 packet analysis

5https://www.wireshark.org/

![](images/659253d7d95cb99ac693d663ff57f600ce46f0ee5771d41762873ae9f287c72b.jpg)

<details>
<summary>sankey</summary>

| Header | Value |
|--------|-------|
| 1100-1150 | 173 |
| 450-500 | 654 |
| 950-1000 | 657 |
| 600-650 | 658 |
| 1000-1050 | 655 |
| 750-800 | 654 |
| 650-700 | 656 |
| 550-600 | 657 |
| 700-750 | 658 |
| 1050-1100 | 658 |
| 900-950 | 658 |
DATA 1↓
DATA 2↓
Header ↑
Header ↓
Data 1 ↓
Data 2 ↓
</details>

(a) Resource A

![](images/29742fb7d491d64987c062f2ac92a81367e06b62948c46ac0e6ffcc1871bfac2.jpg)  
(b) Resource B   
Fig. 17. Frame sequence variability for the same resource, showing stable structures and local perturbations across repeated accesses.

of Fig. 17b, shown in Fig. 18, further validates this phenomenon. When the HPACK dynamic table cache is hit, as shown in Fig. 18a, HTTP header fields can be efficiently compressed using Indexed Header Field, resulting in a HEADERS packet length of only 160 bytes. In contrast, during initial connection establishment or cache misses, as shown in Fig. 18b, the headers must be explicitly transmitted using Literal Header Field, increasing the overhead of the same logical headers to 635 bytes. This binary behavior caused by compression-state switching makes the transmission overhead of a single request jump among several discrete baseline values. When combined with minor perturbations introduced by dynamic fields and Huffman encoding, it ultimately leads to the multimodal distribution of total upstream and downstream traffic volumes at the macroscopic statistical level.

# APPENDIX D FRAME SEQUENCE VARIATIONS FOR A FLOW

Fig. 19 illustrates a commonly observed phenomenon in real HTTP/2 traffic, where HEADERS frames may appear in sub-millisecond bursts for certain resources. This is caused by HTTP/2 multiplexing together with constraints from the HPACK header compression mechanism. When a client issues concurrent requests for multiple static resources, HTTP/2 assigns distinct stream IDs and transmits them over a shared TCP connection. To preserve HPACK dynamic table consistency and comply with the requirement that each header block must be transmitted contiguously without interruption, the protocol stack schedules the corresponding HEADERS frames in a tightly packed and bursty manner.

# REFERENCES

[1] H. Lee, D. Kim, and Y. Kwon, “Tls 1.3 in practice: How tls 1.3 contributes to the internet,” in Proceedings of the Web Conference 2021, 2021, pp. 70–79.   
[2] P. E. Hoffman and P. McManus, “DNS Queries over HTTPS (DoH),” RFC 8484, Oct. 2018. [Online]. Available: https://www.rfc-editor.org/ info/rfc8484   
[3] S. Dickinson, D. K. Gillmor, and T. Reddy.K, “Usage Profiles for DNS over TLS and DNS over DTLS,” RFC 8310, Mar. 2018. [Online]. Available: https://www.rfc-editor.org/info/rfc8310

[4] C. Huitema, S. Dickinson, and A. Mankin, “DNS over Dedicated QUIC Connections,” RFC 9250, May 2022. [Online]. Available: https://www.rfc-editor.org/info/rfc9250   
[5] E. Rescorla, K. Oku, N. Sullivan, and C. A. Wood, “TLS Encrypted Client Hello,” RFC 9849, Mar. 2026. [Online]. Available: https://www.rfc-editor.org/info/rfc9849   
[6] B. Zolfaghari, G. Srivastava, S. Roy, H. R. Nemati, F. Afghah, T. Koshiba, A. Razi, K. Bibak, P. Mitra, and B. K. Rai, “Content delivery networks: State of the art, trends, and future roadmap,” ACM Comput. Surv., vol. 53, no. 2, Apr. 2020. [Online]. Available: https://doi.org/10.1145/3380613   
[7] M. Shen, K. Ye, X. Liu, L. Zhu, J. Kang, S. Yu, Q. Li, and K. Xu, “Machine learning-powered encrypted network traffic analysis: A comprehensive survey,” IEEE Communications Surveys & Tutorials, vol. 25, no. 1, pp. 791–824, 2022.   
[8] E. Papadogiannaki and S. Ioannidis, “A survey on encrypted network traffic analysis applications, techniques, and countermeasures,” ACM Computing Surveys (CSUR), vol. 54, no. 6, pp. 1–35, 2021.   
[9] N. Wickramasinghe, A. Shaghaghi, G. Tsudik, and S. Jha, “Sok: Decoding the enigma of encrypted network traffic classifiers,” in 2025 IEEE Symposium on Security and Privacy (SP). IEEE, 2025, pp. 1825– 1843.   
[10] Y. Zhao, G. Dettori, M. Boffa, L. Vassio, and M. Mellia, “The sweet danger of sugar: Debunking representation learning for encrypted traffic classification,” in Proceedings of the ACM SIGCOMM 2025 Conference, 2025, pp. 296–310.   
[11] A. Sharma and A. H. Lashkari, “A survey on encrypted network traffic: A comprehensive survey of identification/classification techniques, challenges, and future directions,” Computer Networks, vol. 257, p. 110984, 2025.   
[12] Y. Feng, J. Li, J. Mirkovic, C. Wu, C. Wang, H. Ren, J. Xu, and Y. Liu, “Unmasking the internet: A survey of fine-grained network traffic analysis,” IEEE Communications Surveys & Tutorials, 2025.   
[13] A. Bahramali, A. Bozorgi, and A. Houmansadr, “Realistic website fingerprinting by augmenting network traces,” in Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security, 2023, pp. 1035–1049.   
[14] J. Hayes and G. Danezis, “k-fingerprinting: A robust scalable website fingerprinting technique,” in 25th USENIX Security Symposium (USENIX Security 16), 2016, pp. 1187–1203.   
[15] P. Sirinam, M. Imani, M. Juarez, and M. Wright, “Deep fingerprinting: Undermining website fingerprinting defenses with deep learning,” in Proceedings of the 2018 ACM SIGSAC conference on computer and communications security, 2018, pp. 1928–1943.   
[16] T. Van Ede, R. Bortolameotti, A. Continella, J. Ren, D. J. Dubois, M. Lindorfer, D. Choffnes, M. Van Steen, and A. Peter, “Flowprint: Semi-supervised mobile-app fingerprinting on encrypted network traffic,” in Network and distributed system security symposium (NDSS), vol. 27, 2020.   
[17] J. Qu, X. Ma, J. Li, X. Luo, L. Xue, J. Zhang, Z. Li, L. Feng, and X. Guan, “An {Input-Agnostic} hierarchical deep learning frame-

![](images/6b27ebe2b02d6b8cc3dc745521608963cbc1ff7b1441b934d114bbff789ab147.jpg)

<details>
<summary>text_image</summary>

http stream eq 1 and http streamid eq 7
Destination	Protocol	LengthInfo
146.75.45.111	HTTP2	160 HEADERS[7]: GET /assets/frameworks.client.web.4b5ae4374a438e969b45.js
172.19.0.2	HTTP2	710 HEADERS[7]: 200 OK
172.19.0.2	HTTP2	137 DATA[7],DATA[7]
✓ Header: sec-ch-ua: "Chromium";v="140", "Not=A?Brand";v="24", "HeadlessChrome";v="140"
Name Length: 9
Name: sec-ch-ua
Value Length: 66
Value: "Chromium";v="140", "Not=A?Brand";v="24", "HeadlessChrome";v="140"
[Unescaped: "Chromium";v="140", "Not=A?Brand";v="24", "HeadlessChrome";v="140"]
Representation: Indexed Header Field
Index: 79
✓ Header: sec-purpose: prefetch
Name Length: 11
Name: sec-purpose
Value Length: 8
Value: prefetch
[Unescaped: prefetch]
Representation: Indexed Header Field
Index: 69
> Header: accept-language: en-US
Cached
</details>

(a) Indexed Header Field

![](images/9d62a61a145a9fbdec5c555776b416cdcdd0fa0d3dec3297e5568eb1712fa1e5.jpg)

<details>
<summary>text_image</summary>

146.75.45.111 HTTP2 635 HEADERS[1]: GET /assets/frameworks.client.web.4b5ae4374a438e969b45.js
172.19.0.2 HTTP2 742 HEADERS[1]: 200 OK
172.19.0.2 HTTP2 1478 DATA[1][TLS segment of a reassembled PDU]

✓ Header: sec-ch-ua: "Chromium";v="140", "Not=A?Brand";v="24", "HeadlessChrome";v="140"
Name Length: 9
Name: sec-ch-ua
Value Length: 66
Value: "Chromium";v="140", "Not=A?Brand";v="24", "HeadlessChrome";v="140"
[Unescaped: "Chromium";v="140", "Not=A?Brand";v="24", "HeadlessChrome";v="140"]
Representation: Literal Header Field with Incremental Indexing - New Name

✓ Header: sec-purpose: prefetch
Name Length: 11
Name: sec-purpose
Value Length: 8
Value: prefetch
[Unescaped: prefetch]
Representation: Literal Header Field with Incremental Indexing - New Name

> Header: accept-language: en-US
✓ Header: sec-ch-ua-mobile: ?0
Name Length: 16
</details>

(b) Literal Header Field   
Fig. 18. Wireshark-based analysis of HTTP/2 header compression, illustrating the impact of HPACK states on frame size.

<table><tr><td colspan="8">http2</td></tr><tr><td>No.</td><td>Time</td><td>Source</td><td>Destination</td><td>Protocol</td><td>Length</td><td>Info</td><td></td></tr><tr><td>705</td><td>0_343829900</td><td>172.19.0.2</td><td>13.35.202.104</td><td>HTTP2</td><td>143</td><td>HEADERS[13]</td><td>GET /static/js/api-key_js</td></tr><tr><td>706</td><td>0_343891224</td><td>172.19.0.2</td><td>13.35.202.104</td><td>HTTP2</td><td>135</td><td>HEADERS[13]</td><td>GET /static/js/common.min_js</td></tr><tr><td>707</td><td>0_343126151</td><td>172.19.0.2</td><td>13.35.202.104</td><td>HTTP2</td><td>141</td><td>HEADERS[15]</td><td>GET /static/js/content-service.min.js</td></tr><tr><td>708</td><td>0_343154670</td><td>172.19.0.2</td><td>13.35.202.104</td><td>HTTP2</td><td>140</td><td>HEADERS[17]</td><td>GET /static/js/image-lazylodging.js</td></tr><tr><td>709</td><td>0_343185794</td><td>172.19.0.2</td><td>13.35.202.104</td><td>HTTP2</td><td>144</td><td>HEADERS[19]</td><td>GET /static/img/icon-title-pc_1.png</td></tr><tr><td>710</td><td>0_343215504</td><td>172.19.0.2</td><td>13.35.202.104</td><td>HTTP2</td><td>141</td><td>HEADERS[21]</td><td>GET /static/img/icon-title-sp_1.png</td></tr><tr><td>711</td><td>0_343243739</td><td>172.19.0.2</td><td>13.35.202.104</td><td>HTTP2</td><td>140</td><td>HEADERS[23]</td><td>GET /static/img/icon-lang_b_1.png</td></tr><tr><td>712</td><td>0_343274671</td><td>172.19.0.2</td><td>13.35.202.104</td><td>HTTP2</td><td>140</td><td>HEADERS[25]</td><td>GET /static/img/icon-lang_w_1.png</td></tr><tr><td>713</td><td>0_343381931</td><td>172.19.0.2</td><td>13.35.202.104</td><td>HTTP2</td><td>140</td><td>HEADERS[27]</td><td>GET /static/img/icon-line_w_1.png</td></tr><tr><td>714</td><td>0_343335166</td><td>172.19.0.2</td><td>13.35.202.104</td><td>HTTP2</td><td>138</td><td>HEADERS[29]</td><td>GET /static/imgIcon-line_1.png</td></tr></table>

Fig. 19. Concurrent transmission of continuous HEADERS frames driven by HTTP/2 multiplexing mechanism in Wireshark.

work for traffic fingerprinting,” in 32nd USENIX security symposium (USENIX Security 23), 2023, pp. 589–606.   
[18] B. AlOmar, Z. Trabelsi, and S. Alrabaee, “Detection of tor network obfuscated traffic using bidirectional generative adversarial network,” Computer Networks, p. 111586, 2025.   
[19] X. Jiang, S. Liu, A. Gember-Jacobson, A. N. Bhagoji, P. Schmitt, F. Bronzino, and N. Feamster, “Netdiffusion: Network data augmentation through protocol-constrained traffic generation,” Proceedings of the ACM on Measurement and Analysis of Computing Systems, vol. 8, no. 1, pp. 1–32, 2024.   
[20] W. Zhu, X. Ma, Y. Jin, and R. Wang, “Iletc: Incremental learning for encrypted traffic classification using generative replay and exemplar,” Computer Networks, vol. 224, p. 109602, 2023.   
[21] P. Sun, X. Yun, S. Li, T. Yin, C. Si, and J. Xie, “Advtg: An adversarial traffic generation framework to deceive dl-based malicious traffic detection models,” in Proceedings of the ACM on Web Conference 2025, 2025, pp. 3147–3159.   
[22] C. Hajaj, P. Aharon, R. Dubin, and A. Dvir, “The art of time-bending: Data augmentation and early prediction for efficient traffic classification,” Expert Systems with Applications, vol. 252, p. 124166, 2024.   
[23] A. Schoen, G. Blanc, P.-F. Gimenez, Y. Han, F. Majorczyk, and L. Me, “A tale of two methods: Unveiling the limitations of gan and the rise of bayesian networks for synthetic network traffic generation,” in 2024 IEEE European Symposium on Security and Privacy Workshops (EuroS&PW), 2024, pp. 273–286.   
[24] K. Zhou, Z. Liu, Y. Qiao, T. Xiang, and C. C. Loy, “Domain generalization: A survey,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 45, no. 4, pp. 4396–4415, 2023.   
[25] F. Zhao, W. Li, H. Bao, Z. Li, G. Zhou, W. Wang, and F. Liu, “Nuwa: ¨ Enhancing network traffic analysis with pre-trained side-channel feature imputation,” IEEE Transactions on Networking, 2025.   
[26] Y. Zion, P. Aharon, R. Dubin, A. Dvir, and C. Hajaj, “Enhancing encrypted internet traffic classification through advanced data augmentation techniques,” in ICC 2025-IEEE International Conference on Communications. IEEE, 2025, pp. 1–6.   
[27] R. Xie, J. Cao, E. Dong, M. Xu, K. Sun, Q. Li, L. Shen, and M. Zhang, “Rosetta: Enabling robust {TLS} encrypted traffic classification in diverse network environments with {TCP-Aware} traffic augmentation,” in 32nd USENIX Security Symposium (USENIX Security 23), 2023, pp. 625–642.   
[28] E. Horowicz, T. Shapira, and Y. Shavitt, “A few shots traffic classification

with mini-flowpic augmentations,” in Proceedings of the 22nd ACM internet measurement conference, 2022, pp. 647–654.   
[29] Z. Wang, J. Huang, and S. Rose, “Evolution and challenges of dnsbased cdns,” Digital Communications and Networks, vol. 4, no. 4, pp. 235–243, 2018.   
[30] K. Schomp, O. Bhardwaj, E. Kurdoglu, M. Muhaimen, and R. K. Sitaraman, “Akamai dns: Providing authoritative answers to the world’s queries,” in Proceedings of the Annual conference of the ACM Special Interest Group on Data Communication on the applications, technologies, architectures, and protocols for computer communication, 2020, pp. 465–478.   
[31] M. Belshe, R. Peon, and M. Thomson, “Hypertext Transfer Protocol Version 2 (HTTP/2),” RFC 7540, May 2015. [Online]. Available: https://www.rfc-editor.org/info/rfc7540   
[32] R. Peon and H. Ruellan, “HPACK: Header Compression for HTTP/2,” RFC 7541, May 2015. [Online]. Available: https://www.rfc-editor.org/ info/rfc7541   
[33] W. Eddy, “Transmission Control Protocol (TCP),” RFC 9293, Aug. 2022. [Online]. Available: https://www.rfc-editor.org/info/rfc9293   
[34] E. Rescorla and T. Dierks, “The Transport Layer Security (TLS) Protocol Version 1.2,” RFC 5246, Aug. 2008. [Online]. Available: https://www.rfc-editor.org/info/rfc5246   
[35] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “Appscanner: Automatic fingerprinting of smartphone apps from encrypted network traffic,” in 2016 IEEE European Symposium on Security and Privacy (EuroS&P). IEEE, 2016, pp. 439–454.   
[36] M. Shen, J. Zhang, L. Zhu, K. Xu, X. Du, and Y. Liu, “Encrypted traffic classification of decentralized applications on ethereum using feature fusion,” in Proceedings of the International Symposium on Quality of Service, 2019, pp. 1–10.   
[37] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in Proceedings of the ACM Web Conference 2022, 2022, pp. 633–642.   
[38] L. Peng, X. Xie, S. Huang, Z. Wang, and Y. Cui, “Ptu: Pre-trained model for network traffic understanding,” in 2024 IEEE 32nd International Conference on Network Protocols (ICNP). IEEE, 2024, pp. 1–12.   
[39] T. Wang, X. Xie, W. Wang, C. Wang, Y. Zhao, and Y. Cui, “Netmamba: Efficient network traffic classification via pre-training unidirectional mamba,” in 2024 IEEE 32nd International Conference on Network Protocols (ICNP). IEEE, 2024, pp. 1–11.   
[40] X.-Y. Chen, L. Han, D.-C. Zhan, and H.-J. Ye, “Miett: Multi-instance encrypted traffic transformer for encrypted traffic classification,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 39, no. 15, 2025, pp. 15 922–15 929.   
[41] G. Zhou, X. Guo, Z. Liu, T. Li, Q. Li, and K. Xu, “Trafficformer: an efficient pre-trained model for traffic data,” in 2025 IEEE Symposium on Security and Privacy (SP). IEEE, 2025, pp. 1844–1860.   
[42] W. Peng, L. Cui, W. Cai, W. Wang, X. Cui, Z. Hao, and X. Yun, “Bottom aggregating, top separating: An aggregator and separator network for encrypted traffic understanding,” IEEE Transactions on Information Forensics and Security, 2025.   
[43] R. Zhao, M. Zhan, X. Deng, Y. Wang, Y. Wang, G. Gui, and Z. Xue, “Yet another traffic classifier: A masked autoencoder based traffic transformer

with multi-level flow representation,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 37, no. 4, 2023, pp. 5420– 5427.   
[44] Y. Liu, X. Wang, B. Qu, and F. Zhao, “Atvitsc: A novel encrypted traffic classification method based on deep learning,” IEEE Transactions on Information Forensics and Security, 2024.   
[45] H. Zhang, L. Yu, X. Xiao, Q. Li, F. Mercaldo, X. Luo, and Q. Liu, “Tfe-gnn: A temporal fusion encoder using graph neural networks for fine-grained encrypted traffic classification,” in Proceedings of the ACM web conference 2023, 2023, pp. 2066–2075.   
[46] Z. Li, H. Zhao, J. Zhao, Y. Jiang, and F. Bu, “Sat-net: A staggered attention network using graph neural networks for encrypted traffic classification,” Journal of Network and Computer Applications, vol. 233, p. 104069, 2025.   
[47] X. Han, G. Xu, M. Zhang, Z. Yang, Z. Yu, W. Huang, and C. Meng, “Degnn: Dual embedding with graph neural network for fine-grained encrypted traffic classification,” Computer Networks, vol. 245, p. 110372, 2024.   
[48] H. Zhang, H. Yue, X. Xiao, L. Yu, Q. Li, Z. Ling, and Y. Zhang, “Revolutionizing encrypted traffic classification with mh-net: A multi-view heterogeneous graph model,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 39, no. 1, 2025, pp. 1048–1056.   
[49] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “Fs-net: A flow sequence network for encrypted traffic classification,” in IEEE INFOCOM 2019-IEEE Conference On Computer Communications. IEEE, 2019, pp. 1171–1179.   
[50] J. Piet, D. Nwoji, and V. Paxson, “Ggfast: Automating generation of flexible network traffic classifiers,” in Proceedings of the ACM SIGCOMM 2023 Conference, 2023, pp. 850–866.   
[51] Z. Chen, G. Cheng, B. Jiang, S. Tang, S. Guo, and Y. Zhou, “Length matters: Fast internet encrypted traffic service classification based on multi-pdu lengths,” in 2020 16th International Conference on Mobility, Sensing and Networking (MSN). IEEE, 2020, pp. 531–538.   
[52] Z. Chen, G. Cheng, Z. Xu, S. Guo, Y. Zhou, and Y. Zhao, “Length matters: Scalable fast encrypted internet traffic service classification based on multiple protocol data unit length sequence with composite deep learning,” Digital Communications and Networks, vol. 8, no. 3, pp. 289–302, 2022.   
[53] Z. Wu, Y.-n. Dong, X. Qiu, and J. Jin, “Online multimedia traffic classification from the qos perspective using deep learning,” Computer Networks, vol. 204, p. 108716, 2022.   
[54] W. Cai, Z. Li, P. Fu, C. Hou, G. Xiong, and G. Gou, “Metc-mvae: Mobile encrypted traffic classification with masked variational autoencoders,” in 2022 IEEE 24th Int Conf on High Performance Computing & Communications; 8th Int Conf on Data Science & Systems; 20th Int Conf on Smart City; 8th Int Conf on Dependability in Sensor, Cloud & Big Data Systems & Application (HPCC/DSS/SmartCity/DependSys). IEEE, 2022, pp. 1422–1429.   
[55] L. Yang, L. Liu, J.-J. Huang, J. Shi, S. Fu, Y. Wang, and J. Su, “Robustness matters: Pre-training can enhance the performance of encrypted traffic analysis,” IEEE Transactions on Information Forensics and Security, vol. 20, pp. 10 588–10 603, 2025.   
[56] C. Li, L. Nie, and L. Zhao, “Rltree: Website fingerprinting through resource loading tree,” in International Conference on Network and System Security. Springer, 2021, pp. 3–16.   
[57] Z. Chen, G. Cheng, Z. Wei, D. Niu, and N. Fu, “Classify traffic rather than flow: Versatile multi-flow encrypted traffic classification with flow clustering,” IEEE Transactions on Network and Service Management, vol. 21, no. 2, pp. 1446–1466, 2023.   
[58] C. Fu, Q. Li, M. Shen, and K. Xu, “Detecting tunneled flooding traffic via deep semantic analysis of packet length patterns,” in Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security, 2024, pp. 3659–3673.   
[59] Y. Xian, X. Zeng, M. Huang, A. Zhou, X. Cui, P. Liu, and L. Cui, “Udfs: Lightweight representation-driven robust network traffic classification,” arXiv preprint arXiv:2509.11157, 2025.   
[60] W. Dong, J. Yu, X. Lin, G. Gou, and G. Xiong, “Deep learning and pretraining technology for encrypted traffic classification: A comprehensive review,” Neurocomputing, vol. 617, p. 128444, 2025.   
[61] W. Reese, “Nginx: the high-performance web server and reverse proxy,” Linux Journal, vol. 2008, no. 173, p. 2, 2008.   
[62] M. Thomson and C. Benfield, “HTTP/2,” RFC 9113, Jun. 2022. [Online]. Available: https://www.rfc-editor.org/info/rfc9113

[63] “The TCP Maximum Segment Size and Related Topics,” RFC 879, Nov. 1983. [Online]. Available: https://www.rfc-editor.org/info/rfc879   
[64] S. Boeyen, S. Santesson, T. Polk, R. Housley, S. Farrell, and D. Cooper, “Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile,” RFC 5280, May 2008. [Online]. Available: https://www.rfc-editor.org/info/rfc5280   
[65] P. E. Gill and E. Wong, “Sequential quadratic programming methods,” in Mixed integer nonlinear programming. Springer, 2011, pp. 147–224.   
[66] J. Gou, B. Yu, S. J. Maybank, and D. Tao, “Knowledge distillation: A survey,” International journal of computer vision, vol. 129, no. 6, pp. 1789–1819, 2021.   
[67] L. Yang, A. Finamore, F. Jun, and D. Rossi, “Deep learning and zero-day traffic classification: Lessons learned from a commercial-grade dataset,” IEEE Transactions on Network and Service Management, vol. 18, no. 4, pp. 4103–4118, 2021.   
[68] T. Dahanayaka, Y. Ginige, Y. Huang, G. Jourjon, and S. Seneviratne, “Robust open-set classification for encrypted traffic fingerprinting,” Computer Networks, vol. 236, p. 109991, 2023.
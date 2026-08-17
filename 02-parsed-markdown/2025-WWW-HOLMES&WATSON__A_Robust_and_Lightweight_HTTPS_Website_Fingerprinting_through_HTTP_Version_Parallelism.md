# HOLMES & WATSON: A Robust and Lightweight HTTPS Website Fingerprinting through HTTP Version Parallelism

Yifei Cheng Institute of Information Engineering, Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences Beijing, China

Peishuai Sun Yong Ding Institute of Information Engineering, Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences Beijing, China

Yujia Zhu<sup>∗</sup> Institute of Information Engineering, Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences Beijing, China

Xinhao Deng Institute for Network Sciences and Cyberspace, Tsinghua University Beijing, China

Baiyang Li Institute of Information Engineering, Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences Beijing, China

Qingyun Liu Institute of Information Engineering, Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences Beijing, China

## Abstract

Website Fingerprinting (WF) is a trafic analysis technique that aims to identify websites visited by users through the analysis of en crypted trafic patterns. Existing approaches often exhibit limited ro bustness against network variability and concept drift, resulting in significant performance degradation under real-world HTTPS con ditions. Moreover, these methods typically require large-scale train ing datasets and substantial computational resources, which further increases the complexity of deployment. In this paper, we propose HOLMES, a novel approach that exploits HTTP version parallelism to extract enhanced application-layer features. These features, in cluding the number of web resources transmitting in various HTTP versions, expose up to 4.28 bits of information—surpassing 98% of previously reported features and demonstrate increased stabil ity across varying network conditions. Complementary to this, we introduce WATSON, a lightweight classification method based on lazy learning, which substantially reduces the dependency on large training datasets. To further enhance the identification accuracy, we incorporate two fingerprint-specific distance metrics that ensure high intra-class similarity. Our experimental evaluation demonstrates that HOLMES & WATSON significantly enhance both robustness and eficiency, achieving an average accuracy of 87.7% with only a single sample per website, marking an improvement of over 15% compared to state-of-the-art methods.

## CCS Concepts

• Networks → Network privacy and anonymity; • Security and privacy → Pseudonymity, anonymity and untraceability.

![](images/744e3ccaa5f46f64de411bffa372ef43f22f4fc14fc02fa7a4f5dac20aa08464.jpg)  
Figure 1: Five main kinds of methods to identify websites from encrypted trafic: (a) Using IP addresses with entropybased matching. (b) Using trafic trace sequence features with deep learning. (c) Using trafic statistical features with machine learning. (d) Using TLS SNI parameters. (e) Using web resource features with lazy learning.

## Keywords

Website fingerprinting, HTTP version parallelism, Protocol analysis

## ACM Reference Format:

Yifei Cheng, Yujia Zhu, Baiyang Li, Peishuai Sun, Yong Ding, Xinhao Deng, and Qingyun Liu. 2025. HOLMES & WATSON: A Robust and Lightweight HTTPS Website Fingerprinting through HTTP Version Parallelism. In Proceedings of the ACM Web Conference 2025 (WWW ’25), April 28-May 2, 2025, Sydney, NSW, Australia. ACM, New York, NY, USA, 15 pages. https: //doi.org/10.1145/3696410.3714578

## 1 INTRODUCTION

The increasing adoption of HTTPS has significantly improved user privacy by encrypting communication content. However, adversaries can still deduce web activities by exploiting side-channel information, such as DNS queries [32], the TLS Server Name Indication (SNI) field [88], and corresponding server IP addresses [53]. To mitigate these privacy vulnerabilities, privacy-enhancing technologies such as encrypted DNS (DoH [34], DoT [23], DoQ [36]) and TLS Encrypted Client Hello (ECH [17, 62]) have been in troduced. Additionally, the increasing prevalence of IP co-location, largely facilitated by content delivery networks (CDNs), has further diminished the efectiveness of IP-based identification methods[5].

While these countermeasures reduce the eficacy of traditional side-channel attacks, they do not fully eliminate the risk posed by trafic analysis. Notably, website fingerprinting (WF) attacks continue to represent a significant threat [4, 21, 29, 31, 65, 70, 86]. WF enables adversaries to analyze patterns in encrypted trafic and infer the websites a user visits [67]. Although the majority of research on WF has been concentrated on anonymity networks, such as Tor [24], there is growing interest in applying these techniques to HTTPS due to their potential impact on encrypted web trafic.

However, existing WF attacks struggle in realistic HTTPS scenarios due to their reliance on unrealistic assumptions [15, 39, 80] that conflict with the actual nature of HTTPS trafic. These assumptions often include stable network conditions, the absence of concept drift, and the availability of large labeled datasets, all of which are misaligned with the dynamic and diverse nature of network trafic. While several work have demonstrated high accuracy in controlled environments [6, 29, 52, 58, 70, 71], their performance degrades substantially in realistic HTTPS scenarios. For instance, Juarez et al. [39] showed that concept drift leads to a significant reduction in WF accuracy, and our experiments corroborate this finding, revealing a 20% drop in accuracy under varying network conditions (§4.4). Furthermore, the training process for a typical WF classifier requires over 10 days of data collection [71], which presents significant limitations for its practical deployment.

We argue that the limitations mentioned above largely stem from inadequate feature extraction layer. Existing WF attacks mainly rely on transport-layer features, such as packet direction sequences and inter-packet delays. As shown in Figure 1, these features, situated at the transport layer of the TCP/IP model, are distant from the actual characteristics of website resources, making them more vulnerable to network condition changes and less robust [84]. Moreover, these transport-layer features are often sparse and fragmented, requiring complex machine learning or deep learning models, as well as large training datasets, which limits their practicality [12].

To address these challenges, we propose a novel WF method that leverages features at the application layer. Despite content encryption and multiplexing in HTTPS, signals such as resource count and connection numbers can be inferred from the browser request side [3, 48]. More importantly, we identified a growing phenomenon in the modern internet ecosystem: HTTP version parallelism. Due to multiple HTTP versions running concurrently without manda tory upgrades, website owners independently choose which version to adopt. This results in distinct patterns across HTTP versions for diferent websites, as illustrated in Figure 2(a). By expanding the feature space with HTTP version parallelism, we significantly enhance the distinguishing power of application-layer features; for instance, the quantity of HTTP/2 resources alone reveals 4.28 bits of information (see Figure 2(b)), exceeding 98% of existing features. Moreover, these features demonstrate greater stability across varying network conditions, as shown in Figure 2(c).

![](images/28ac6626d3b30fd576970389733fd4aa0a460658607b74eeea163fd62419d6d0.jpg)  
Figure 2: HTTP Version Parallelism and Privacy Implications. (a) Demonstrate HTTP version parallelism in popular websites. (b) Assess the information leakage [45] potential caused by the quantity of HTTP resources in relation to a known 3043-dimensional feature set (300 monitored websites). (c) Use the coeficient of variation [60] to illustrate the intra-class stability of various features in crossnetwork conditions.

Based on the identified features, we propose a rich and robust website fingerprint representation—H123 fingerprint—utilizing characteristics such as web resource quantity, HTTP versions, and loading sequences. To diferentiate websites using this representation, we employ a hybrid distance metric that combines Wasserstein distance and a modified Longest Common Subsequence (LCS) metric, assigning diferent weights to enhance their contributions to fingerprint similarity assessment. Considering practical requirements for a lightweight solution, we adopt a Lazy Learning paradigm (e.g., k-Nearest Neighbor [18]) that computes predictions on demand, eliminating the need for prior model training [2]. This approach allows for rapid deployment and flexible adjustments to the monitored set of websites. Moreover, by relying on direct distance measurements rather than model fitting, our method requires only a minimal number of reference samples for efective WF attack. Notably, our approach attains an average accuracy of 87.7% with only one sample per website, reflecting an enhancement of more than 15% compared to current state-of-the-art methods.

Our contributions are as follows:

• We are the first to identify and analyze the privacy risks posed by application-layer features under the context of modern HTTP version parallelism. We propose the HTTP resOurce extrapoLating Method under Encrypted Scheme (HOLMES), which extracts these features without decryption, enabling the generation of robust and information-dense H123 fingerprints.

![](images/5bdbb5c67fe4fc40decca493ffc064314f6dc43998b3954200bd9bd2e68b70f9.jpg)  
Figure 3: The overview of HOLMES & WATSON.

• We present the WAsserstein and Textual Similarity-based recOgNizer (WATSON), a lightweight website fingerprinting attack method based on lazy learning and specific distance mea sures that performs well even in few-shot scenarios.

• We collect and publish<sup>1</sup> a comprehensive dataset containing over 1.5TB of HTTPS trafic, covering 220,000 samples from 80,000 websites across 12 experimental scenarios. This is the first HTTPS WF dataset to include trafic generated under challenging network conditions, from multiple mainstream browsers, and with more realistic monitored website sets.

• We conducted comprehensive experiments, comparing our method with state-of-the-art approaches, demonstrating its effectiveness, robustness, and lightweight nature. We release the source code of H&W [14].

## 2 BACKGROUND AND MOTIVATION

## 2.1 HTTP Version Parallelism

The HyperText Transfer Protocol (HTTP) is fundamental to web browsing, enabling the transfer of content between clients and servers. Over time, HTTP evolved from HTTP/1.1 [26], which in troduced persistent connections and chunked transfer encoding, to HTTP/2 [75] and HTTP/3 [7], which improved performance. HTTP/2’s multiplexing and header compression reduced latency, while HTTP/3’s use of QUIC [38] enhanced security and reliability. These advancements support modern encrypted web trafic, form ing the backbone of HTTPS [61], where HTTP works with TLS or QUIC to protect user data from eavesdropping.

The phenomenon of concurrent HTTP versions has been somewhat acknowledged by the scientific community, primarily not in the context of privacy concerns. Discussions on the IETF mailing list regarding HTTP/3 have highlighted the challenges for browser and server implementers in maintaining support for all HTTP ver sions [37]. Nonetheless, we argue that the inevitability, ubiquity, and distinctiveness of HTTP version parallelism position it as a critical factor in potential privacy leakage.

Inevitability of HTTP Version Parallelism. Despite the in creasing adoption of HTTP/3 due to its eficiency and stability, many websites continue to support older versions for compatibility [77]. Furthermore, the specific connection establishment process of HTTP/3 complicates its direct adoption; in most cases, an initial connection is made using an older HTTP version to exchange necessary information, after which data transmission rights are negotiated in a competitive manner [7, 50].

Ubiquity of HTTP Version Parallelism. In our survey of the top 100,000 websites (see Appendix B), we found that over 80% utilize at least two HTTP versions, with nearly half employing all three—HTTP/1.1, HTTP/2, and HTTP/3—during a single visit. This widespread parallelism has become a standard characteristic of modern web trafic.

Distinctiveness of HTTP Version Parallelism. Figure 2 illustrates how diverse patterns of HTTP version usage can form unique signatures. By combining various HTTP versions and the number of resources, these patterns create privacy risks that can be exploited to identify websites. This underscores the necessity for further investigation into how HTTP version parallelism impacts privacy.

## 2.2 Threat Model

This study follows an attacker capability assumption similar to that in existing WF research [4, 10, 35, 70, 86]. We assume a local passive eavesdropper (e.g., an ISP) positioned along the communication path between the user’s terminal and the website server. The eavesdropper can monitor but not alter, delay, drop, or decrypt trafic, aiming to identify whether the user is visiting a monitored website and, if so, which one.

We also account for realistic environmental constraints faced by attackers, such as monitoring multiple website sets instead of focusing only on popular sites [33], using fewer samples for WF attacks [51, 71, 86], and testing under varying network conditions [4, 65, 86] and concept drift [4, 21, 33, 68]. Variations in browser behavior [35] and potential defense mechanisms [66, 68] are also considered. To maintain comparability with previous work and concentrate on privacy breaches, our attacks focus on websites’ homepages. Although this may not fully represent real-world user behavior [15], Mitseva et al.[49] recently proposed a generalizable framework that could be applied to extend existing methods and address these limitations in future research.

## 3 METHODOLOGY

Unlike existing WF attacks, our approach extracts features at the trafic flow level [54]. Specifically, we generate a unified set of fingerprint features for each flow identified by a five-tuple: <source IP, source port, destination IP, destination port, protocol>. This analysis at the flow level ofers a balance between the eficiency of packet-level features and the information richness of session-level features.

Figure 3 outlines the core components of our approach. In the following sections, we describe HOLMES for feature extraction and WATSON for fingerprinting attacks, following the typical steps of a WF attack.

## 3.1 HOLMES

As a first step, we define the direction of packets sent by the client as out and those received by the client as in. In typical HTTPS scenarios, a network connection first undergoes a transport-layer handshake, followed by a security-layer handshake, before entering the application-layer request-response cycle. The encryption at the security layer introduces packet obfuscation, which complicates eforts to focus solely on the HTTP phase [44]. Based on our analysis of protocol specifications, we identify the start of the HTTP phase as the first ‘application data’ TLS packet in the out direction, or, for HTTP/3, the first short-header QUIC packet in the out direction.

Moreover, we observe that metadata within the trafic can reveal the HTTP version and even the number ofresources requested. This is because content encryption does not alter the HTTP requestresponse pattern, which varies across HTTP versions. Multiplexing, which afects the merging of responses, does not obscure the num ber of resources, as it can still be inferred from the request-side signals. Figure 14 ofers a visual explanation of these characteristics.

3.1.1 Inferring HTTP Versions. HTTP/3 uses the novel QUIC pro tocol as its transport layer, enabling a simple distinction between HTTP/3 and earlier versions by checking whether QUIC (UDP) is in use. HTTP/1 lacks multiplexing (though pipelining exists, it is not widely supported by browsers [16, 82]), meaning that HTTP/1 requests and responses occur sequentially. This pattern is reflected in the first two packets of the HTTP phase, where we always see an "out" request followed by an "in" response. In contrast, HTTP/2 sends a "preface" packet before the first request to establish multiplexing configurations, resulting in the first two packets both being "out" requests. Thus, by observing the direction of the first two packets in the HTTP phase, we can easily distinguish between HTTP/1 and HTTP/2.

3.1.2 Inferring Resource Quantity. We propose using the number of "out" packets in the HTTP phase to estimate the number of web resources requested. Through further protocol analysis and empirical testing across multiple browsers, we identify two main sources of estimation bias: (1) Setup/control packet bias—in HTTP/2 and HTTP/3, additional setup packets and control frames are sent, leading to an overestimation of resource count. We address this by filtering out small packets that do not carry actual content. (2) HTTP request method bias—when requests are sent via POST, browsers may split the request header and body into multiple packets, even though only one resource is being requested. We disregard this bias, as it consistently occurs and does not significantly afect the inference process.

Based on these observations, we design protocol state machines that implement these rules to accurately infer resource quantities across diferent HTTP versions. Details of this state machine design are presented in Appendix C.

3.1.3 Constructing H123 fingerprint. The H123 fingerprint is constructed by encoding each connection (i.e., trafic flow) based on its HTTP version and corresponding resource quantity. For � connections, let $\mathrm { H T T P } _ { i } \in \{ 1 , 2 , 3 \}$ represent the HTTP version of the �-th connection, and $R _ { i }$ denote the resource quantity. The fingerprint is represented by a matrix $F \in \mathbb { R } ^ { 3 \times x }$ , where each column corresponds to a connection, and the rows represent HTTP/1, HTTP/2, and HTTP/3.

The value $F _ { v , i }$ at row � and column � is defined as:

$$
F _ {v, i} = \left\{ \begin{array}{l l} R _ {i}, & \text { if   HTTP } _ {i} = v \\ 0, & \text { otherwise } \end{array} \right.\tag{1}
$$

where $v \in \{ 1 , 2 , 3 \}$ . This matrix encodes the HTTP version and resource quantity for each connection, forming the H123 fingerprint. Additionally, it is interesting to observe how diferent websites perform under the proposed H123 fingerprint. To illustrate this more clearly, we provide examples of H123 fingerprints for some of the most popular websites in Appendix D.

## 3.2 WATSON

3.2.1 Lazy Learning. Lazy learning (also known as instance-based learning) defers the training process to the prediction stage, unlike eager learning models such as decision trees or neural networks, which build a model during training [2]. In lazy learning, the algorithm makes predictions by comparing a new sample directly with stored reference samples, computing similarity or distance metrics to assign the sample to a category.

In the context of WF attacks, lazy learning ofers the advantage of not requiring model pre-training, thus allowing for flexible addition or updating of website categories and samples [71, 79]. Additionally, by computing distances at the prediction stage, the method avoids overfitting risks commonly associated with insuficient training data.

To improve the eficiency of lazy learning, especially with large datasets, we introduced a resource-based sample pre-selection process. During prediction, a band-pass filter is applied to the reference set, retaining only samples whose resource quantities fall within 20% of the target sample’s total. This optimization reduces unnecessary distance calculations, resulting in an approximately 85% reduction in comparisons during our experiments.

3.2.2 Distance Metrics: Wasserstein and LCSS. Accurate classification in WF attacks requires distance metrics that capture the unique characteristics of encrypted web trafic. Our analysis of H123 fingerprints identified three primary forms of intra-class variability: sequence permutation, division/aggregation, and temporal misalignment (as shown in Figure 4). These variations, though subtle, are intrinsic to fingerprint data and must be accounted for in our classification method. To address these issues, we designed a composite distance metric using Wasserstein distance [76] and LCSS (Longest Common Similar Subsequence) distance, tailored specifically to handle these types of variability.

Wasserstein Distance (also known as Earth Mover’s Distance) measures the diference between two probability distributions. It calculates the minimum "work" required to transform one distribution into another, considering the spatial relationship between

a. Sequence Permutation

b. Division / Aggregation

$$
\begin{array}{l} \left[ 2 ^ {h _ {1}}, 1 0 ^ {h _ {3}}, 6 ^ {h _ {2}}, \boxed {1 8 ^ {h _ {3}}}, \boxed {1 ^ {h _ {1}}}, 1 ^ {h _ {1}}, 9 ^ {h _ {2}} \right] \\ \left[ 2 ^ {h _ {1}}, 1 0 ^ {h _ {3}}, 6 ^ {h _ {2}}, \boxed {1 ^ {h _ {1}}}, \boxed {1 8 ^ {h _ {3}}}, 1 ^ {h _ {1}}, 9 ^ {h _ {2}} \right] \\ \left[ 2 ^ {h _ {1}}, 1 0 ^ {h _ {3}}, 6 ^ {h _ {2}}, \boxed {1 8 ^ {h _ {3}}}, 1 ^ {h _ {1}}, 1 ^ {h _ {1}}, 9 ^ {h _ {2}} \right] \\ \left[ 2 ^ {h _ {1}}, 1 0 ^ {h _ {3}}, 6 ^ {h _ {2}}, \boxed {8 ^ {h _ {3}}}, \boxed {1 0 ^ {h _ {3}}}, 1 ^ {h _ {1}}, 1 ^ {h _ {1}}, 9 ^ {h _ {2}} \right] \\ \left[ 2 ^ {h _ {1}}, 1 0 ^ {h _ {3}}, 6 ^ {h _ {2}}, 1 8 ^ {h _ {3}}, 1 ^ {h _ {1}}, 1 ^ {h _ {1}}, 9 ^ {h _ {2}} \right] \\ \left[ 1 ^ {h _ {1}}, 2 ^ {h _ {1}}, 1 0 ^ {h _ {3}}, 6 ^ {h _ {2}}, 1 8 ^ {h _ {3}}, 1 ^ {h _ {1}}, 1 ^ {h _ {1}}, 9 ^ {h _ {2}} \right] \end{array}
$$

c. Misalignment

elements. This makes it particularly suitable for addressing small shifts in sequence elements or aggregation/division patterns in fingerprint data. The distance is calculated using the following formula:

$$
W (P, Q) = \inf _ {\gamma \in \Gamma (P, Q)} \int | x - y | d \gamma (x, y)\tag{2}
$$

where $P$ and $Q$ are probability distributions, and � represents a transport plan.

LCSS Distance measures local similarity by identifying common subsequences between two sequences. It captures variations in temporal sequences, such as the misalignment of elements, which are common in H123 fingerprints. We introduce a relaxed similarity threshold, allowing for slight deviations between elements to account for these shifts. The similarity criterion, denoted as $\epsilon ,$ ensures robustness against small misalignments between subsequences. The adjusted LCSS distance improves sensitivity to local patterns while handling sequence-level discrepancies efectively.

The combination of these two metrics, weighted appropriately, provides a tailored measure for comparing website fingerprints, improving classification accuracy and robustness. Detailed pseudocode for the implementation of these distance measures is provided in Appendix E.

3.2.3 Classification Strategy. In a closed-world scenario, where all categories are known, we adopt the classical Nearest Neighbor (NN) approach to classify a test sample based on the closest reference sample. This method provides high classification accuracy within the range of known categories.

In contrast, the open-world scenario introduces the challenge of unknown categories. To address this, we combine the K-Nearest Neighbors (KNN) algorithm with the Gini coeficient [11] to assess whether a test sample belongs to any reference category. Specifi cally, we calculate the distances to the 2N nearest reference samples for the test sample, where N represents the number of reference samples per category.

The Gini coeficient, which measures inequality, helps us assess the distribution of these distances. If the test sample belongs to a known category, we expect the 2N nearest samples to include N samples with much smaller distances, representing the same category, and N samples with larger distances, representing other categories. This leads to an unequal distribution of distances and a lower Gini coeficient. Conversely, if the test sample does not belong to any known category, the distances will be more uniformly distributed, leading to a higher Gini coeficient. By setting a threshold on the Gini coeficient, we can reliably distinguish between samples that belong to the monitored set and those that do not.

Figure 4: H123 Fingerprint Characterizes. Here for the sake of simplicity we have compressed the http version information into a one-dimensional representation.  
Table 1: Overview of datasets. For OW datasets, one sample per website; for other datasets, 40 samples per website.

<table><tr><td>Task</td><td>Scenario</td><td># Websites</td><td># Samples</td><td>Task</td><td>Scenario</td><td># Websites</td><td># Samples</td></tr><tr><td rowspan="3">CW</td><td>popular</td><td>1600</td><td>64,000</td><td rowspan="3">Browser</td><td>chrome</td><td>200</td><td>8,000</td></tr><tr><td>random</td><td>320</td><td>12,800</td><td>chrome-legacy</td><td>200</td><td>8,000</td></tr><tr><td>censorship</td><td>320</td><td>12,800</td><td>firefox</td><td>200</td><td>8,000</td></tr><tr><td rowspan="3">Bandwidth</td><td>unconstrained</td><td>200</td><td>8,000</td><td rowspan="2">Time-Drift</td><td>18-day</td><td>200</td><td>8,000</td></tr><tr><td>starlink-like</td><td>200</td><td>8,000</td><td>30-day</td><td>200</td><td>8,000</td></tr><tr><td>slow</td><td>200</td><td>8,000</td><td>OW</td><td>open world</td><td>80,000</td><td>80,000</td></tr></table>

## 4 EXPERIMENTAL EVALUATION

## 4.1 Datasets

To evaluate the efectiveness of our method, we constructed a comprehensive dataset encompassing 12 distinct scenarios with over 220,000 website visits. The dataset includes closed-world (CW), open-world (OW), bandwidth, browser, and time-drift scenarios, designed to reflect realistic attack conditions. Key statistics of the dataset are summarized in Table 1. Data collection was conducted using an automated approach with Selenium and tcpdump, deployed across 10 Amazon cloud servers from July to September 2024. Further details on dataset construction and collection methodology are provided in Appendix F.

## 4.2 Experimental Setup

4.2.1 Optimization ofHyperparameters. We independently optimized hyperparameters for H&W using supplementary data, ensuring no involvement of test sets from later validation experiments to avoid data leakage. We ultimately selected the maximum length of the H123 fingerprint (L) as 50, set the similarity threshold for the LCSS distance (�) to 0.24, and assigned equal weights of 0.5 for both distance measures (see Appendix G for details).

4.2.2 WF atacksfor comparison. To make a comprehensive comparison, we selected 5 state-of-the-art WF attacks: k-FP [29], DF [70], TF [71], RF [65], and IP-WF [33]. Each was implemented using the authors’ released code and fine-tuned for fairness in our experiments, which involved hyperparameter search and early stopping to mitigate overfitting in few-shot scenarios. We also introduced several optimizations: enabling packet length features in k-FP for better performance in HTTPS scenarios (k-FP+), mapping packet length information onto trace sequences to enhance DF (DF+), and constructing an ideal IP-WF scenario by utilizing IP addresses from browser logs rather than trafic flows to eliminate interference, thereby estimating the upper accuracy limit of this attack. All WF attacks were executed on a server running Ubuntu 23.10, equipped with an NVIDIA A100 80GB GPU, Intel Xeon 2.9GHz CPU, and 128GB RAM. To avoid random errors, we applied k-fold cross-validation to all attacks.

4.2.3 Metrics. We adopt the evaluation metrics from [70]. In closedworld tasks Accuracy is used to assess the performance of WF attacks in multi-class classification of monitored websites. In open world tasks, while WF attacks still involve multi-class classification, we focus more on their ability to distinguish monitored websites from unmonitored ones. Thus, we treat it as a binary classification problem and use Precision, Recall, and F1-score as evaluation metrics. Compared to TPR and FPR, these metrics are more robust in handling class imbalance, as they provide a more comprehensive assessment of both positive and negative class performance.

Table 2: Closed-world: Accuracy (%) of WF attacks across diferent datasets in a few-shot scenario. We bolded results over 95% as suficiently reliable for attacks and marked the best results in each scenario.

<table><tr><td rowspan="2" colspan="2">Attacks</td><td colspan="3"> $N=1 BST^1=20$  hours</td><td colspan="3"> $N=2 BST=40$  hours</td><td colspan="3"> $N=3 BST=60$  hours</td><td colspan="3"> $N=10 BST=8$  days</td><td colspan="3"> $N=30 BST=25$  days</td><td colspan="2">Time Overhead $^2$ </td></tr><tr><td>pop.</td><td>rand.</td><td>cens.</td><td>pop.</td><td>rand.</td><td>cens.</td><td>pop.</td><td>rand.</td><td>cens.</td><td>pop.</td><td>rand.</td><td>cens.</td><td>pop.</td><td>rand.</td><td>cens.</td><td>train↓</td><td>pred.↑</td></tr><tr><td colspan="2">k-FP [29]</td><td>40.1 ± 0.6</td><td>50.3 ± 0.5</td><td>58.3 ± 0.9</td><td>60.2 ± 0.1</td><td>70.6 ± 0.4</td><td>76.9 ± 1.0</td><td>69.5 ± 0.2</td><td>80.3 ± 0.7</td><td>84.0 ± 0.5</td><td>84.2 ± 0.1</td><td>90.8 ± 0.4</td><td>92.8 ± 0.2</td><td>90.6 ± 0.3</td><td>94.9 ± 0.6</td><td>95.9 ± 0.3</td><td>10.9s</td><td>&gt;5k</td></tr><tr><td colspan="2">DF [70]</td><td>16.7 ± 2.2</td><td>38.6 ± 1.2</td><td>29.0 ± 1.4</td><td>39.7 ± 1.9</td><td>53.5 ± 1.1</td><td>49.5 ± 0.7</td><td>58.0 ± 1.1</td><td>82.9 ± 0.4</td><td>62.1 ± 0.4</td><td>91.9 ± 0.3</td><td>96.9 ± 0.1</td><td>93.1 ± 0.5</td><td>98.0 ± 0.2</td><td>99.0 ± 0.2</td><td>98.6 ± 0.4</td><td>254.4s</td><td>3,765</td></tr><tr><td colspan="2">TF [71]</td><td>57.3 ± 0.4</td><td>69.7 ± 0.9</td><td>66.9 ± 0.7</td><td>67.9 ± 0.3</td><td>79.3 ± 0.8</td><td>74.3 ± 0.5</td><td>72.6 ± 0.4</td><td>83.3 ± 0.5</td><td>78.8 ± 0.5</td><td>79.7 ± 0.2</td><td>88.8 ± 0.4</td><td>83.3 ± 0.3</td><td>81.8 ± 0.3</td><td>90.9 ± 0.3</td><td>84.8 ± 0.3</td><td>205.9s</td><td>873</td></tr><tr><td colspan="2">RF [65]</td><td>10.6 ± 1.1</td><td>40.2 ± 0.9</td><td>33.2 ± 1.9</td><td>37.0 ± 1.0</td><td>56.9 ± 1.2</td><td>52.3 ± 1.4</td><td>46.1 ± 1.1</td><td>78.1 ± 0.4</td><td>74.0 ± 1.0</td><td>78.3 ± 0.5</td><td>91.1 ± 0.6</td><td>87.0 ± 0.8</td><td>89.5 ± 0.9</td><td>97.8 ± 0.4</td><td>96.0 ± 0.5</td><td>26.5s</td><td>&gt;5k</td></tr><tr><td colspan="2">k-FP+</td><td>64.1 ± 1.0</td><td>69.4 ± 1.2</td><td>76.5 ± 1.3</td><td>87.1 ± 0.3</td><td>90.8 ± 0.3</td><td>92.6 ± 0.3</td><td>93.0 ± 0.1</td><td>95.2 ± 0.5</td><td>95.8 ± 0.4</td><td>98.0 ± 0.1</td><td>98.3 ± 0.2</td><td>98.8 ± 0.2</td><td>99.1 ± 0.1</td><td>99.5 ± 0.1</td><td>99.4 ± 0.1</td><td>16.3s</td><td>&gt;5k</td></tr><tr><td colspan="2">DF+</td><td>15.6 ± 1.5</td><td>46.9 ± 2.1</td><td>38.7 ± 1.1</td><td>44.8 ± 1.2</td><td>56.6 ± 1.5</td><td>56.4 ± 1.2</td><td>63.6 ± 1.2</td><td>83.5 ± 0.5</td><td>68.8 ± 1.0</td><td>94.3 ± 0.3</td><td>97.6 ± 0.1</td><td>96.3 ± 0.4</td><td>98.5 ± 0.1</td><td>99.5 ± 0.1</td><td>99.4 ± 0.1</td><td>277.5s</td><td>4,298</td></tr><tr><td colspan="2">IP-WF (primary) [33]</td><td>52.4 ± 0.2</td><td>60.3 ± 0.2</td><td>74.7 ± 0.5</td><td>52.4 ± 0.3</td><td>62.7 ± 0.4</td><td>76.9 ± 0.5</td><td>53.2 ± 0.4</td><td>64.1 ± 0.4</td><td>77.4 ± 0.6</td><td>54.0 ± 0.3</td><td>66.4 ± 0.3</td><td>78.7 ± 0.3</td><td>54.9 ± 0.2</td><td>67.1 ± 0.2</td><td>79.2 ± 0.2</td><td>-</td><td>&gt;5k</td></tr><tr><td colspan="2">IP-WF [33]</td><td>65.2 ± 0.3</td><td>64.9 ± 0.2</td><td>81.4 ± 0.4</td><td>68.3 ± 0.6</td><td>67.8 ± 0.3</td><td>84.7 ± 0.4</td><td>69.4 ± 0.4</td><td>70.0 ± 0.5</td><td>85.6 ± 0.8</td><td>72.5 ± 0.2</td><td>73.8 ± 0.3</td><td>89.0 ± 0.3</td><td>73.4 ± 0.2</td><td>74.9 ± 0.1</td><td>90.2 ± 0.2</td><td>50.1s</td><td>4,023</td></tr><tr><td colspan="2">IP-WF (ideal)</td><td>79.5 ± 0.5</td><td>79.3 ± 0.6</td><td>85.2 ± 0.5</td><td>84.3 ± 1.0</td><td>84.9 ± 0.4</td><td>88.4 ± 0.5</td><td>87.0 ± 0.5</td><td>87.4 ± 0.5</td><td>89.5 ± 0.7</td><td>92.1 ± 0.3</td><td>93.8 ± 0.4</td><td>93.8 ± 0.7</td><td>93.9 ± 0.2</td><td>96.2 ± 0.2</td><td>95.0 ± 0.1</td><td>50.1s</td><td>3,819</td></tr><tr><td rowspan="5">HOLMES</td><td>Cosine</td><td>42.4 ± 1.6</td><td>48.9 ± 0.7</td><td>53.8 ± 1.8</td><td>52.2 ± 1.2</td><td>61.9 ± 1.1</td><td>62.2 ± 1.1</td><td>59.5 ± 0.8</td><td>69.2 ± 0.7</td><td>67.2 ± 0.8</td><td>75.0 ± 0.8</td><td>82.7 ± 0.4</td><td>82.1 ± 0.4</td><td>82.4 ± 0.6</td><td>91.2 ± 0.5</td><td>89.7 ± 0.5</td><td>-</td><td>&gt;5k</td></tr><tr><td>Edit</td><td>73.9 ± 0.8</td><td>83.3 ± 0.5</td><td>77.8 ± 0.4</td><td>82.6 ± 0.6</td><td>90.3 ± 0.7</td><td>85.5 ± 0.5</td><td>85.5 ± 0.6</td><td>93.3 ± 0.6</td><td>89.2 ± 0.7</td><td>93.3 ± 0.4</td><td>97.0 ± 0.3</td><td>94.2 ± 0.6</td><td>96.4 ± 0.4</td><td>98.6 ± 0.3</td><td>96.4 ± 0.2</td><td>-</td><td>1,091</td></tr><tr><td>Wasserstein</td><td>80.1 ± 0.6</td><td>88.3 ± 0.6</td><td>82.4 ± 1.0</td><td>86.1 ± 0.7</td><td>92.9 ± 0.8</td><td>86.7 ± 0.6</td><td>88.3 ± 0.6</td><td>96.3 ± 0.5</td><td>89.1 ± 0.9</td><td>94.1 ± 0.4</td><td>98.1 ± 0.3</td><td>94.4 ± 0.6</td><td>96.6 ± 0.3</td><td>98.9 ± 0.2</td><td>95.5 ± 0.5</td><td>-</td><td>&gt;5k</td></tr><tr><td>LCSS</td><td>78.8 ± 1.1</td><td>87.6 ± 1.4</td><td>81.0 ± 1.2</td><td>87.9 ± 1.0</td><td>91.9 ± 0.7</td><td>88.7 ± 0.7</td><td>89.3 ± 0.6</td><td>95.2 ± 0.5</td><td>89.9 ± 0.8</td><td>95.1 ± 0.4</td><td>97.2 ± 0.5</td><td>95.1 ± 0.8</td><td>97.8 ± 0.4</td><td>98.7 ± 0.4</td><td>96.2 ± 0.6</td><td>-</td><td>2,819</td></tr><tr><td>WATSON</td><td>85.3 ± 0.8</td><td>90.4 ± 1.0</td><td>87.3 ± 0.8</td><td>91.9 ± 0.6</td><td>95.8 ± 1.0</td><td>92.9 ± 0.7</td><td>94.4 ± 0.7</td><td>96.4 ± 0.5</td><td>94.6 ± 0.4</td><td>96.7 ± 0.3</td><td>98.6 ± 0.3</td><td>96.4 ± 0.3</td><td>98.7 ± 0.3</td><td>99.5 ± 0.2</td><td>97.6 ± 0.2</td><td>-</td><td>2,068</td></tr></table>

<sup>1</sup> Bootstrap time is the total time required to initiate a comprehensive WF attack, including data collection and model training.  
<sup>2</sup> Time overhead when validated on popular datasets with N=3. We record the training time and prediction throughput (websites/second).

## 4.3 Closed-world Evaluation

We first evaluate H&W in a closed-world scenario, assuming the clients visit only a set of monitored sites of interest to the attacker. The evaluation results are presented in Table 2.

Experiment 1: WF attacks with diferent data distributions. Traditional WF attacks require a large, regularly updated dataset, leading to excessive bootstrap time that renders the attack impracti cal for adversaries [71]. We evaluated the performance of various methods under diferent training sample sizes, with N = {1, 2, 3, 10, 30}, where the first four settings represent typical few-shot learning tasks. Results show that H&W achieves an attack accuracy (average across diferent monitored sets) of 87.7% with N = 1 . This implies that using H&W, an attacker only needs to visit each monitored site once to launch an efective WF attack, significantly outperforming the best existing IP-WF method, which achieves 70.5%. As N increases, the accuracy of all WF attacks improves. With N = 30 (bootstrap time exceeding 25 days), k-FP+ achieves the highest accuracy of 99.3%. Although H&W was not designed for this scenario, it still achieves a top-tier performance of 98.6%, while the widely discussed IP-WF under HTTPS scenarios delivers a mediocre performance, achieving only 79.5%.

Experiment 2: WF attacks with diferent monitored sets. We evaluated the performance of various attacks across diferent monitored website sets to comprehensively assess their applicability in more realistic and diverse scenarios. H&W consistently performed well, achieving, e.g., 95.8% accuracy in the random set with 320 websites using only two training samples. There is a positive correlation between the number of websites in the monitored set and attack dificulty, as most attacks performed worse on the popular set compared to the random and censorship sets. In comparisons across sets with the same number of websites, H&W, DF,

TF, and RF slightly outperformed in the random set, while k-FP performed better in the censorship set. IP-WF showed a notable advantage in the censorship set, likely due to the more distinct IP addresses of the websites, with less IP co-location observed.

Experiment 3: Time overhead analysis. The training time and prediction throughput of an attack are crucial factors that influence its practicality. Frequent changes in website resources necessitate periodic data updates and retraining, and long training times can compromise the attack’s timeliness. We conducted experiments on a high-performance computing platform, recording both training times and prediction throughput (websites/second) for various attacks. Notably, H&W, a lightweight, distance-based lazy learning method, requires no parameterized model training, eliminating training time overhead and allowing flexibility for periodic updates or incremental learning. In contrast, other methods require extensive training (e.g., TF requires pre-training, and IP-WF needs entropy fingerprint training), with deep learning-based approaches typically being the most time-consuming. In the prediction phase, we evaluated the throughput of each method, which better reflects their performance in real-world scenarios. Across all website fingerprinting attack methods, prediction throughput reached acceptable levels. H&W, for example, can handle at least 2,000 website visits per second, demonstrating its eficiency in high-trafic situations.

Experiment 4: H&W with diferent distance metrics. The results in table 2 show that Wasserstein distance and LCSS significantly outperform cosine distance and edit distance in distinguishing H123 fingerprints. By combining these two distances, WATSON achieves an average accuracy improvement of 3%, demonstrating their complementary nature in handling fingerprint features and enhancing overall performance.

## 4.4 Robustness Evaluation

Evaluating the robustness of attack methods in realistic settings is essential. As in prior work, we focus on cross-network conditions scenario [4, 65, 86] and concept drift scenario [4, 21, 33, 68].

Experiment 1: WF attacks under cross-network conditions. We performed cross-training and validation of various attacks on three typical network condition datasets: unconstrained, starlink like, and slow. The results on the diagonal of Figure 5 show the performance of baseline attacks without cross-training, with k-FP+ and H&W achieving the best results. The of-diagonal results indicate that all attack methods experience varying degrees of per formance degradation under cross-network conditions, with band width changes (unconstrained-slow) having a greater impact than packet loss changes (unconstrained-starlink). Notably, H&W per forms better than existing methods under cross-network conditions, thanks to the application-layer resource features of H123 being in dependent of network conditions, which enhances its robustness. Additionally, k-FP+ and RF exhibit the most severe accuracy decline due to their features being strongly correlated with loading time, while IP-WF demonstrates the highest stability under cross network conditions but with mediocre attack performance. Similar trends were observed for the N = 1 case, as shown in Figure 12.

![](images/34cf635168e9b718fff78efd07f0f28a8a75bc3fc571cee2ebdce555f8c24beb.jpg)  
Figure 5: Comparison of attack robustness across network conditions with N = 10 in the Bandwidth dataset.

Experiment 2: WF attacks under concept drift. When a website’s contents (such as images or ads) are updated, its trafic representation changes accordingly. This results in growing discrepancies between training data and actual attack data over time, a phenomenon known as concept drift [27]. Figure 6(b) illustrates how the attack performance of the initial model varies after 18 and 30 days. The figure shows that as the time interval increases, concept drift intensifies, which directly leads to a decrease in attack performance across all methods. Furthermore, increasing the number of training samples (from N=1 to N=10) does not alleviate the efects of concept drift. Notably, with only 1 training sample and a 30-day interval, H&W still achieves nearly 80% attack accu racy. For N=10, although k-FP+ and H&W both achieve over 98% accuracy without concept drift, k-FP+’s accuracy drops to 72% after 30 days of concept drift, while H&W maintains 88% accuracy. This better performance of H&W is due to the H123 fingerprints’ focus on HTTP version and resource quantity, rather than resource size, which is sensitive to content updates (e.g., ads). This design makes H123 more resilient to concept drift, as it is less afected by changes in content.

## 4.5 Open-world Evaluation

The open-world scenario ofers a more realistic assessment of WF attacks by accounting for the vast, unexhausted range of websites users might visit. We simulate a more practical setting by using the CW-censorship dataset as the monitored set to reflect the potential of real-world network censors, and we consider N = {1, 2, 3, 10} as training samples, with the rest used for testing. Initially, we evaluate various attacks using a random sample of 10k websites from the OW dataset as the unmonitored test set. We then further assess the impact of a larger open-world set on H&W performance.

![](images/525e840459e396cb2265e8852ea8b010033d8eb23e6e4413295dbb19bc2930ef.jpg)  
Figure 6: Evaluation of concept drift in the Time dataset. (a) Cosine distance measures concept drift’s impact on trafic features, shown by the empirical CDF of average distances for the same site. (b) Shows the robustness and stability of diferent attacks under concept drift.

Experiment 1: WF attacks in the open-world scenario. As shown in Table 3, in the open-world scenario, network censors using H&W can achieve over 85% micro F1 with just one training sample, significantly outperforming k-FP+ and DF+ in few-shot settings. While IP-WF excels in distinguishing between monitored and unmonitored sets, its performance declines when identifying specific websites. With increased training costs, H&W achieves 92.1% binary F1 and 94.2% micro F1 with N=10, slightly below the performance of k-FP+ and DF+.

Experiment 2: H&W deep dive in the open-world scenario. As with previous works [49, 70, 71], we analyze H&W’s performance in larger open-world scenarios. We assert that increasing the number of open-world websites does not afect the training data but instead expands the number of negative samples in the test set. As the number of negative samples grows, more are incorrectly classified as positive, leading to a decrease in precision, though recall remains unafected. Figure 7(a) shows the relationship between H&W’s attack performance and the size of the open world for N = {1, 10}. The P-R curve, representing attack performance, gradually declines as the number of negative samples increases. With 80,000 unmonitored websites, H&W still demonstrates reasonable performance under N = 10, achieving a precision of 70.2% and recall of 81.0%. Figure 7(b), on the other hand, shows the cumulative distribution curves of Gini coeficient values for samples processed by H&W in both monitored and unmonitored sets. The clear distinction between the two curves demonstrates H&W’s strong discriminative ability.

## 4.6 Case Study: Applicability of H&W

H&W, as an attack method utilizing application-layer fingerprint features, presents an interesting and meaningful area of study re garding its applicability under various factors. We primarily explore the efects of diferent website characteristics, browser types, and defense strategies on H&W performance. To ensure generalizability, we conducted experiments on the CW-random and Browser datasets with N = {1, 10}.

Table 3: Open-world: Binary and micro F1 (%) of WF attacks.

<table><tr><td rowspan="2">Att.</td><td colspan="2"> $N = 1$ </td><td colspan="2"> $N = 2$ </td><td colspan="2"> $N = 3$ </td><td colspan="2"> $N = 10$ </td></tr><tr><td>binary $^{1}$ </td><td>micro $^{2}$ </td><td>binary</td><td>micro</td><td>binary</td><td>micro</td><td>binary</td><td>micro</td></tr><tr><td> $k\text{-FP+}$ </td><td> $79.3 \pm 0.8$ </td><td> $77.9 \pm 1.0$ </td><td> $81.5 \pm 0.4$ </td><td> $87.1 \pm 0.4$ </td><td> $85.1 \pm 0.5$ </td><td> $90.4 \pm 0.4$ </td><td> $92.8 \pm 0.3$ </td><td> $95.8 \pm 0.2$ </td></tr><tr><td>DF+</td><td> $46.0 \pm 1.1$ </td><td> $43.1 \pm 1.1$ </td><td> $65.0 \pm 0.5$ </td><td> $60.7 \pm 0.8$ </td><td> $81.4 \pm 0.5$ </td><td> $75.3 \pm 0.6$ </td><td> $93.9 \pm 0.3$ </td><td> $95.1 \pm 0.3$ </td></tr><tr><td>IP-WF</td><td> $88.1 \pm 0.5$ </td><td> $84.7 \pm 0.4$ </td><td> $89.5 \pm 0.5$ </td><td> $87.1 \pm 0.4$ </td><td> $90.1 \pm 0.1$ </td><td> $87.9 \pm 0.3$ </td><td> $91.2 \pm 0.1$ </td><td> $90.1 \pm 0.2$ </td></tr><tr><td>H&amp;W</td><td> $84.7 \pm 0.6$ </td><td> $85.9 \pm 0.6$ </td><td> $88.2 \pm 0.7$ </td><td> $90.5 \pm 0.7$ </td><td> $90.2 \pm 0.6$ </td><td> $92.4 \pm 0.5$ </td><td> $92.1 \pm 0.5$ </td><td> $94.2 \pm 0.4$ </td></tr></table>

measures the attack’s ability to distinguish monitored vs. unmonitored websites. 2 measures detailed classification performance with website-specific identification.

![](images/0aa546ffa68fae6f13d7c034d1dd1f08272cd08141029e852fee0754bd20444f.jpg)

![](images/e4457f977fe0720c41d643d878ee4f54cf95aa6d058b1e3a69c900dbe41ac37f.jpg)

![](images/4024cefbd2ee1810d5f89c77836a0e082443e40d73532a3593d8cf6222672c62.jpg)  
(a) Impact of a larger open world  
(b) Discriminability of Websites in OW  
Figure 7: In-depth analysis of H&W in open world. (a) Analyze the impact of unmonitored website quantity on H&W attack per formance. (b) Examine the distinguishability between monitored and unmonitored sets in H&W and optimal threshold selection.

We first analyzed target websites, collecting data on resource quantity, connection quantity, and HTTP version density (measured by the Shannon entropy [64] of the version sequence). The cumulative distribution of these metrics is shown in Figure 8. We constructed value intervals based on quartiles and conducted inde pendent training and testing of H&W within these intervals. The results in Table 4 indicate that websites with resource and connec tion quantities in the (Q2, Q3] range are more vulnerable to the attack. Additionally, HTTP version density positively correlates with attack performance, meaning websites using multiple HTTP versions are more susceptible to H&W than those using only one. As websites adopt higher HTTP versions or as new versions emerge, version parallelism will intensify, making H&W increasingly threat ening.

We validated H&W across three major browsers, showing strong performance on all. While it performed slightly worse on Firefox than Chrome, it still achieved over 98% accuracy with N = 10. We also evaluated the impact of padding-based defense strategies, finding that known defenses reduced attack accuracy by about 3%, maintaining a practical 95.5%. For detailed experimental setup and analysis, refer to Appendix H.

The above study demonstrates that H&W is not only lightweight and robust at the method level but also applicable across diferent server- and client-side environments. It is important to highlight that existing typical defense strategies are insuficient to mitigate H&W attacks, and with the growth ofversion parallelism, the threat will increase.

## 5 LIMITATIONS AND DISCUSSION

While our study demonstrates the efectiveness of H123 fingerprint ing through HTTP version parallelism, certain limitations should be noted. First, the method’s performance is primarily validated on mainstream browsers (e.g., Chrome, Firefox), and cross-browser scenarios remain challenging due to diferences in protocol handling. Second, the reliance on website resource stability means that significant changes in resources can reduce attack efectiveness, necessitating periodic data updates and model retraining.

Table 4: Case study: Impact of website characteristics.

<table><tr><td colspan="2">Main Factors</td><td>[0, Q1]</td><td>(Q1, Q2]</td><td>(Q2, Q3]</td><td>(Q3, max]</td></tr><tr><td rowspan="2">Resource Quantity</td><td>N = 1</td><td>83.8 ± 1.5</td><td>87.5 ± 0.6</td><td>91.1 ± 0.9</td><td>86.8 ± 1.7</td></tr><tr><td>N = 10</td><td>95.5 ± 1.1</td><td>98.6 ± 0.3</td><td>98.7 ± 0.3</td><td>98.1 ± 0.8</td></tr><tr><td rowspan="2">Connection Quantity</td><td>N = 1</td><td>83.2 ± 1.0</td><td>87.8 ± 1.7</td><td>90.7 ± 1.3</td><td>88.2 ± 1.6</td></tr><tr><td>N = 10</td><td>94.9 ± 0.8</td><td>98.0 ± 0.8</td><td>99.1 ± 0.4</td><td>98.5 ± 0.3</td></tr><tr><td rowspan="2">HTTP Version Diversity</td><td>N = 1</td><td>83.7 ± 1.4</td><td>88.8 ± 1.1</td><td>89.3 ± 1.4</td><td>90.6 ± 1.3</td></tr><tr><td>N = 10</td><td>96.2 ± 0.3</td><td>98.2 ± 0.5</td><td>98.3 ± 0.3</td><td>99.2 ± 0.2</td></tr></table>

![](images/b9bba5ba81ec453452740d0485533ae0ffd2de70618ea0266b5841c8d07300c1.jpg)

![](images/6db35629c14e9967086203364aa0ff0204fe26aef1260b84b707ef6aced0e6b4.jpg)

![](images/89a5e6312eef3a999dac39981c80cc179a909cb13a74d59c32a8766635079bc5.jpg)  
Figure 8: Distribution of main factors in H123 fingerprints. The distribution of resource and connection quantities is afected by the maximum fingerprint length $\left( L = 5 0 \right)$ . HTTP version density is represented by the Shannon entropy of the version sequence.

Despite these limitations, our approach highlights the potential of protocol version parallelism, which could extend to other layers such as TLS (e.g., TLS 1.2 and TLS 1.3) and the coexistence of IPv4 and IPv6. Combining multiple layers of protocol information may reveal deeper insights, further exacerbating privacy risks in encrypted trafic.

In our current implementation of H123 fingerprints, we assumed equal importance for each fingerprint part. However, inspired by recent research on early detection [20, 89], we suggest assigning more weight to the earlier parts—given their stability and reliability—to enhance accuracy. Additionally, leveraging the characteristics of H123 fingerprints summarized in Figure 4 for data augmentation [4, 85, 90] could further strengthen attack performance. This weighted approach and data augmentation represent promising directions for future work.

## 6 CONCLUSION

In conclusion, this paper introduced a method for HTTPS website fingerprinting using HTTP version parallelism, proving highly effective in small-sample scenarios and achieving robust performance with just one sample per monitored website. The experimental results demonstrated resilience across various network conditions and an ability to handle concept drift. As version parallelism grows with the adoption of diferent protocol versions, the privacy risks identified are likely to become more significant, highlighting the need for further research to mitigate these emerging threats.

## Acknowledgments

This work is supported by the Scaling Program of Institute of Information Engineering, CAS (Grant No. E3Z0191101 and No. E3Z0041101)

## References

[1] Kota Abe and Shigeki Goto. 2016. Fingerprinting attack on Tor anonymity using deep learning. Proceedings ofthe Asia-Pacific Advanced Network 42, 0 (2016), 15–20.

[2] David W Aha, Dennis Kibler, and Marc K Albert. 1991. Instance-based learning algorithms. Machine learning 6 (1991), 37–66.

[3] Blake Anderson, Andrew Chi, Scott Dunlop, and David McGrew. 2019. Limitless http in an https world: Inferring the semantics of the https protocol without decryption. In Proceedings ofthe Ninth ACM conference on data and application security and privacy. 267–278.

[4] Alireza Bahramali, Ardavan Bozorgi, and Amir Houmansadr. 2023. Realistic website fingerprinting by augmenting network traces. In Proceedings ofthe 2023 ACM SIGSAC Conference on Computer and Communications Security. 1035–1049.

[5] Ignacio N Bermudez, Marco Mellia, Maurizio M Munafo, Ram Keralapura, and Antonio Nucci. 2012. Dns to the rescue: Discerning content and services in a tangled web. In Proceedings ofthe 2012 Internet Measurement Conference. 413–426.

[6] Sanjit Bhat, David Lu, Albert Kwon, and Srinivas Devadas. 2018. Var-CNN: A data-eficient website fingerprinting attack based on deep learning. arXiv preprint arXiv:1802.10215 (2018).

[7] Mike Bishop. 2022. HTTP/3. RFC 9114. https://doi.org/10.17487/RFC9114

[8] Manuel Bülo, Jörg Deutschmann, Kai-Stefen Hielscher, and Reinhard Ger man. 2024. Crowdsourced Starlink Performance Measurements from https://starlinkstatus. space. In ICC 2024-IEEE International Conference on Communications. IEEE, 5596–5603.

[9] Xiang Cai, Rishab Nithyanand, Tao Wang, Rob Johnson, and Ian Goldberg. 2014. A systematic approach to developing and evaluating website fingerprinting defenses. In Proceedings of the 2014 ACM SIGSAC Conference on Computer and Communications Security. 227–238.

[10] Xiang Cai, Xin Cheng Zhang, Brijesh Joshi, and Rob Johnson. 2012. Touching from a distance: Website fingerprinting attacks and defenses. In Proceedings of the 2012 ACM conference on Computer and communications security. 605–616.

[11] Lidia Ceriani and Paolo Verme. 2012. The origins of the Gini index: extracts from Variabilità e Mutabilità (1912) by Corrado Gini. The Journal ofEconomic Inequality 10 (2012), 421–443.

[12] Zihan Chen, Guang Cheng, Zijun Wei, Ziheng Xu, Nan Fu, and Yuyang Zhou. 2022. Higher Layers, Better Results: Application Layer Feature Engineering in En crypted Trafic Classification. In International Conference on Wireless Algorithms, Systems, and Applications. Springer, 548–556.

[13] Heyning Cheng and Ron Avnur. 1998. Trafic analysis of SSL encrypted web browsing. Project paper, University ofBerkeley (1998).

[14] Yifei Cheng. 2024. H123 Website Fingerprinting. https://github.com/2654400439/ H123-Website-Fingerprinting Accessed: 2024-10-12.

[15] Giovanni Cherubin, Rob Jansen, and Carmela Troncoso. 2022. Online website fingerprinting: Evaluating website fingerprinting attacks on tor in the real world. In 31st USENIX Security Symposium (USENIX Security 22). 753–770.

[16] Chromium Developers. 2024. HTTP Pipelining. https://www.chromium.org/ developers/design-documents/network-stack/http-pipelining/ Accessed: 2024- 09-30.

[17] OpenSSL Contributors. 2024. OpenSSL ECH Feature Branch. https://github.com/ openssl/openssl/tree/feature/ech. Accessed: 2024-09-24.

[18] Thomas Cover and Peter Hart. 1967. Nearest neighbor pattern classification. IEEE transactions on information theory 13, 1 (1967), 21–27.

[19] Wladimir De la Cadena, Asya Mitseva, Jens Hiller, Jan Pennekamp, Sebastian Reuter, Julian Filter, Thomas Engel, Klaus Wehrle, and Andriy Panchenko. 2020. Traficsliver: Fighting website fingerprinting attacks with trafic splitting. In Proceedings ofthe 2020 ACMSIGSAC Conference on Computerand Communications Security. 1971–1985.

[20] Xinhao Deng, Qi Li, and Ke Xu. 2024. Robust and reliable early-stage Website fingerprinting attacks via spatial-temporal distribution analysis. arXiv preprint arXiv:2407.00918 (2024).

[21] Xinhao Deng, Qilei Yin, Zhuotao Liu, Xiyuan Zhao, Qi Li, Mingwei Xu, Ke Xu, and Jianping Wu. 2023. Robust multi-tab website fingerprinting attacks in the wild. In 2023 IEEE Symposium on Security and Privacy (SP). IEEE, 1005–1022.

[22] Chrome Developers. 2023. Network Throttling - Chrome DevTools. https: //developer.chrome.com/docs/devtools/settings/throttling. Accessed: 2024-09-13.

[23] Sara Dickinson, Daniel Kahn Gillmor, and Tirumaleswar Reddy.K. 2018. Usage Profiles for DNS over TLS and DNS over DTLS. RFC 8310. https://doi.org/10. 17487/RFC8310

[24] Roger Dingledine, Nick Mathewson, Paul F Syverson, et al. 2004. Tor: The second-generation onion router.. In USENIX security symposium, Vol. 4. 303–320.

[25] Gerard Draper-Gil, Arash Habibi Lashkari, Mohammad Saiful Islam Mamun, and Ali A Ghorbani. 2016. Characterization of encrypted and vpn trafic using time-related. In Proceedings ofthe 2nd international conference on information systems security and privacy (ICISSP). 407–414.

[26] Roy T. Fielding, Mark Nottingham, and Julian Reschke. 2022. HTTP/1.1. RFC 9112. https://doi.org/10.17487/RFC9112

[27] João Gama, Indre Žliobait˙ e, Albert Bifet, Mykola Pechenizkiy, and Abdelhamid˙ Bouchachia. 2014. A survey on concept drift adaptation. ACM computing surveys (CSUR) 46, 4 (2014), 1–37.

[28] Jiajun Gong and Tao Wang. 2020. Zero-delay lightweight defenses against website fingerprinting. In 29th USENIX Security Symposium (USENIX Security 20). 717–734.

[29] Jamie Hayes and George Danezis. 2016. k-fingerprinting: A robust scalable website fingerprinting technique. In 25th USENIX Security Symposium (USENIX Security 16). 1187–1203.

[30] Dominik Herrmann, Rolf Wendolsky, and Hannes Federrath. 2009. Website fingerprinting: attacking popular privacy enhancing technologies with the multinomial naïve-bayes classifier. In Proceedings ofthe 2009 ACM workshop on Cloud computing security. 31–42.

[31] Andrew Hintz. 2002. Fingerprinting websites using trafic analysis. In International workshop on privacy enhancing technologies. Springer, 171–178.

[32] Nguyen Phong Hoang, Arian Akhavan Niaki, Jakub Dalek, Jefrey Knockel, Pellaeon Lin, Bill Marczak, Masashi Crete-Nishihata, Phillipa Gill, and Michalis Polychronakis. 2021. How Great is the Great Firewall? Measuring China’s {DNS} Censorship. In 30th USENIX Security Symposium (USENIX Security 21). 3381–3398.

[33] Nguyen Phong Hoang, Arian Akhavan Niaki, Phillipa Gill, and Michalis Polychronakis. 2021. Domain name encryption is not enough: Privacy leakage via IP-based website fingerprinting. arXiv preprint arXiv:2102.08332 (2021).

[34] Paul E. Hofman and Patrick McManus. 2018. DNS Queries over HTTPS (DoH). RFC 8484. https://doi.org/10.17487/RFC8484

[35] Guodong Huang, Chuan Ma, Ming Ding, Yuwen Qian, Chunpeng Ge, Liming Fang, and Zhe Liu. 2023. Eficient and low overhead website fingerprinting attacks and defenses based on TCP/IP trafic. In Proceedings ofthe ACM Web Conference 2023. 1991–1999.

[36] Christian Huitema, Sara Dickinson, and Allison Mankin. 2022. DNS over Dedicated QUIC Connections. RFC 9250. https://doi.org/10.17487/RFC9250

[37] IETF. [n. d.]. QUIC Mailing List Archive. https://mailarchive.ietf.org/arch/browse/ quic/. Accessed: 2024-09-26.

[38] Jana Iyengar and Martin Thomson. 2021. QUIC: A UDP-Based Multiplexed and Secure Transport. RFC 9000. https://doi.org/10.17487/RFC9000

[39] Marc Juarez, Sadia Afroz, Gunes Acar, Claudia Diaz, and Rachel Greenstadt. 2014. A critical evaluation of website fingerprinting attacks. In Proceedings ofthe 2014 ACM SIGSAC conference on computer and communications security. 263–274.

[40] Marc Juarez, Mohsen Imani, Mike Perry, Claudia Diaz, and Matthew Wright. 2016. Toward an eficient website fingerprinting defense. In Computer Security– ESORICS 2016: 21st European Symposium on Research in Computer Security, Heraklion, Greece, September 26-30, 2016, Proceedings, Part I 21. Springer, 27–46.

[41] George Kadianakis. 2012. Packet size pluggable transport and trafic morphing. Technická Zpráva (2012), 03–004.

[42] Sunjae Kim and Wonjun Lee. 2023. HTTP Steady Connections for Robust Web Acceleration. In Proceedings ofthe ACM Web Conference 2023. 3154–3163.

[43] Citizen Lab and Others. 2014. URL testing lists intended for discovering website censorship. https://github.com/citizenlab/test-lists https://github.com/citizenlab/test-lists.

[44] Hyunwoo Lee, Doowon Kim, and Yonghwi Kwon. 2021. TLS 1.3 in practice: How TLS 1.3 contributes to the internet. In Proceedings ofthe Web Conference 2021. 70–79.

[45] Shuai Li, Huajun Guo, and Nicholas Hopper. 2018. Measuring information leakage in website fingerprinting attacks and defenses. In Proceedings ofthe 2018 ACM SIGSAC Conference on Computer and Communications Security. 1977–1992.

[46] FoxIO LLC. 2023. JA4+ Network Fingerprinting. https://github.com/FoxIO-LLC/ja4 Accessed: 2023-09-20.

[47] Liming Lu, Ee-Chien Chang, and Mun Choon Chan. 2010. Website fingerprinting and identification using ordered feature sequences. In Computer Security– ESORICS 2010: 15th European Symposium on Research in ComputerSecurity, Athens, Greece, September 20-22, 2010. Proceedings 15. Springer, 199–214.

[48] Gargi Mitra, Prasanna Karthik Vairam, Patanjali Slpsk, Nitin Chandrachoodan, and V Kamakoti. 2020. Depending on HTTP/2 for privacy? Good luck!. In 2020 50th Annual IEEE/IFIP International Conference on Dependable Systems and Networks (DSN). IEEE, 278–285.

[49] Asya Mitseva and Andriy Panchenko. 2024. Stop, Don’t Click Here Anymore: Boosting Website Fingerprinting By Considering Sets ofSubpages. In 33rdUSENIX Security Symposium (USENIX Security 24). 4139–4156.

[50] Marcin Nawrocki, Pouyan Fotouhi Tehrani, Raphael Hiesgen, Jonas Mücke, Thomas C Schmidt, and Matthias Wählisch. 2022. On the interplay between TLS certificates and QUIC performance. In Proceedings ofthe 18th International Conference on emerging Networking EXperiments and Technologies. 204–213.

[51] Se Eun Oh, Nate Mathews, Mohammad Saidur Rahman, Matthew Wright, and Nicholas Hopper. 2021. GANDaLF: GAN for data-limited fingerprinting. Proceedings on Privacy Enhancing Technologies 2021, 2 (2021).

[52] Andriy Panchenko, Fabian Lanze, Jan Pennekamp, Thomas Engel, Andreas Zin nen, Martin Henze, and Klaus Wehrle. 2016. Website Fingerprinting at Internet Scale.. In NDSS.

[53] Simran Patil and Nikita Borisov. 2019. What can you learn from an IP?. In Proceedings ofthe Applied Networking Research Workshop. 45–51.

[54] Vern Paxson. 1994. Empirically derived analytic models of wide-area TCP con nections. IEEE/ACM transactions on Networking 2, 4 (1994), 316–336.

[55] Julien Piet, Dubem Nwoji, and Vern Paxson. 2023. Ggfast: Automating generation of flexible network trafic classifiers. In Proceedings ofthe ACM SIGCOMM 2023 Conference. 850–866.

[56] Victor Le Pochat, Tom Van Goethem, Samaneh Tajalizadehkhoob, Maciej Kor czyński, and Wouter Joosen. 2018. Tranco: A research-oriented top sites ranking hardened against manipulation. arXiv preprint arXiv:1806.01156 (2018).

[57] Cloudflare radar team. 2024. Worldwide Internet Quality. https://radar.cloudflare. com/quality. Accessed: 2024-09-12

[58] Mohammad Saidur Rahman, Payap Sirinam, Nate Mathews, Kantha Girish Gan gadhara, and Matthew Wright. 2019. Tik-tok: The utility of packet timing in website fingerprinting attacks. arXiv preprint arXiv:1902.06421 (2019).

[59] Aaditya Ramdas, Nicolás García Trillos, and Marco Cuturi. 2017. On wasserstein two-sample testing and related families of nonparametric tests. Entropy 19, 2 (2017), 47.

[60] George F Reed, Freyja Lynn, and Bruce D Meade. 2002. Use of coeficient of variation in assessing variability of quantitative assays. Clinical and Vaccine Immunology 9, 6 (2002), 1235–1239.

[61] Eric Rescorla. 2000. HTTP Over TLS. RFC 2818. https://doi.org/10.17487/RFC2818

[62] Eric Rescorla, Kazuho Oku, Nick Sullivan, and Christopher A. Wood. 2024. TLS Encrypted Client Hello. Internet-Draft draft-ietf-tls-esni-22. Internet Engineering Task Force. https://datatracker.ietf.org/doc/draft-ietf-tls-esni/22/ Work in Progress.

[63] Vera Rimmer, Davy Preuveneers, Marc Juarez, Tom Van Goethem, and Wouter Joosen. 2017. Automated website fingerprinting through deep learning. arXiv preprint arXiv:1708.06376 (2017).

[64] Claude Elwood Shannon. 1948. A mathematical theory of communication. The Bell system technical journal 27, 3 (1948), 379–423.

[65] Meng Shen, Kexin Ji, Zhenbo Gao, Qi Li, Liehuang Zhu, and Ke Xu. 2023. Subvert ing website fingerprinting defenses with robust trafic representation. In 32nd USENIX Security Symposium (USENIX Security 23). 607–624.

[66] Meng Shen, Yiting Liu, Liehuang Zhu, Xiaojiang Du, and Jiankun Hu. 2020. Fine-grained webpage fingerprinting using only packet length information of encrypted trafic. IEEE Transactions on Information Forensics and Security 16 (2020), 2046–2059.

[67] Meng Shen, Ke Ye, Xingtong Liu, Liehuang Zhu, Jiawen Kang, Shui Yu, Qi Li, and Ke Xu. 2022. Machine learning-powered encrypted network trafic analysis: A comprehensive survey. IEEE Communications Surveys & Tutorials 25, 1 (2022), 791–824.

[68] Sandra Siby, Ludovic Barman, Christopher Wood, Marwan Fayed, Nick Sullivan, and Carmela Troncoso. 2023. Evaluating practical QUIC website fingerprinting defenses for the masses. Proceedings on Privacy Enhancing Technologies (2023)

[69] Sandra Siby, Marc Juarez, Claudia Diaz, Narseo Vallina-Rodriguez, and Carmela Troncoso. 2019. Encrypted DNS–> privacy? A trafic analysis perspective. arXiv preprint arXiv:1906.09682 (2019).

[70] Payap Sirinam, Mohsen Imani, Marc Juarez, and Matthew Wright. 2018. Deep fingerprinting: Undermining website fingerprinting defenses with deep learning. In Proceedings of the 2018 ACM SIGSAC conference on computer and communications security. 1928–1943.

[71] Payap Sirinam, Nate Mathews, Mohammad Saidur Rahman, and Matthew Wright. 2019. Triplet fingerprinting: More practical and portable website fingerprinting with n-shot learning. In Proceedings of the 2019 ACM SIGSAC Conference on Computer and Communications Security. 1131–1148.

[72] Jean-Pierre Smith, Luca Dolfi, Prateek Mittal, and Adrian Perrig. 2022. {QCSD}: A {QUIC} {Client-Side} {Website-Fingerprinting} Defence Framework. In 31st USENIX Security Symposium (USENIX Security 22). 771–789.

[73] Statcounter Global Stats. 2024. Desktop Browser Market Share Worldwide. https: //gs.statcounter.com/browser-market-share/desktop/worldwide. Accessed: 2024- 09-12.

[74] Qixiang Sun, Daniel R Simon, Yi-Min Wang, Wilf Russell, Venkata N Padman abhan, and Lili Qiu. 2002. Statistical identification of encrypted web browsing trafic. In Proceedings 2002 IEEE Symposium on Security and Privacy. IEEE, 19–30.

[75] Martin Thomson and Cory Benfield. 2022. HTTP/2. RFC 9113. https://doi.org/ 10.17487/RFC9113

[76] Cédric Villani et al. 2009. Optimal transport: old and new. Vol. 338. Springer.

[77] W3Techs. 2024. HTTP/3 - Usage Statistics of HTTP/3 for Websites. https: //w3techs.com/technologies/details/ce-http3 Accessed: 2024-01-21.

[78] David Wagner, Bruce Schneier, et al. 1996. Analysis of the SSL 3.0 protocol. In The Second USENIX Workshop on Electronic Commerce Proceedings, Vol. 1. 29–40.

[79] Tao Wang, Xiang Cai, Rishab Nithyanand, Rob Johnson, and Ian Goldberg. 2014. Efective attacks and provable defenses for website fingerprinting. In 23rd USENIX Security Symposium (USENIX Security 14). 143–157.

[80] Tao Wang and Ian Goldberg. 2016. On realistically attacking tor with website fingerprinting. Proceedings on Privacy Enhancing Technologies (2016).

[81] Tao Wang and Ian Goldberg. 2017. {Walkie-Talkie}: An eficient defense against passive website fingerprinting attacks. In 26th USENIX Security Symposium (USENIX Security 17). 1375–1390.

[82] Wikipedia. 2024. HTTP pipelining. https://en.wikipedia.org/wiki/HTTP\_ pipelining Accessed: 2024-09-30.

[83] Charles V Wright, Fabian Monrose, and Gerald M Masson. 2006. On inferring application protocol behaviors in encrypted network trafic. Journal of Machine Learning Research 7, 12 (2006).

[84] Hua Wu, Qiuyan Wu, Guang Cheng, Shuyi Guo, Xiaoyan Hu, and Shen Yan. 2021. SFIM: Identify user behavior based on stable features. Peer-to-Peer Networking and Applications 14, 6 (2021), 3674–3687.

[85] Renjie Xie, Yixiao Wang, Jiahao Cao, Enhuan Dong, Mingwei Xu, Kun Sun, Qi Li, Licheng Shen, and Menghao Zhang. 2023. Rosetta: Enabling robust tls encrypted trafic classification in diverse network environments with tcp-aware trafic augmentation. In Proceedings ofthe ACM Turing Award Celebration Conference-China 2023. 131–132.

[86] Yi Xie, Jiahao Feng, Wenju Huang, Yixi Zhang, Xueliang Sun, Xiaochou Chen, and Xiapu Luo. 2024. Contrastive Fingerprinting: A Novel Website Fingerprinting Attack over Few-shot Traces. In Proceedings of the ACM on Web Conference 2024. 1203–1214.

[87] Diwen Xue, Michalis Kallitsis, Amir Houmansadr, and Roya Ensafi. 2024. Fingerprinting Obfuscated Proxy Trafic with Encapsulated {TLS} Handshakes. In 33rd USENIX Security Symposium (USENIX Security 24). 2689–2706.

[88] Hiroaki Yamauchi, Akihiro Nakao, Masato Oguchi, Shu Yamamoto, and Saneyasu Yamaguchi. 2020. Service identification based on SNI analysis. In 2020 IEEE 17th Annual Consumer Communications & Networking Conference (CCNC). IEEE, 1–6.

[89] Pengwei Zhan, Liming Wang, and Yi Tang. 2021. Website fingerprinting on early QUIC trafic. Computer Networks 200 (2021), 108538.

[90] Xiyuan Zhao, Xinhao Deng, Qi Li, Yunpeng Liu, Zhuotao Liu, Kun Sun, and Ke Xu. 2024. Towards Fine-Grained Webpage Fingerprinting at Scale. In Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security. 423–436.

## A Related work

The foundational premise of WF asserts that unique trafic characteristics can distinguish websites, even when the trafic is encrypted or obscured. This concept emerged in the 1990s [78], and was first prominently featured in academic discourse by Andrew Hintz, who analyzed the number and sizes of web resources to conduct fingerprinting [31]. Concurrent studies also leveraged network resource metrics for diferentiation [13, 74].

The advent of application-layer pipelining and multiplexing, alongside advancements in privacy technologies like the Tor network, rendered early fingerprinting techniques less efective, redirecting focus to transport-layer packet features. Herrmann et al. [30] employed frequency analysis of packet sizes in conjunction with Bayesian classifiers to execute fingerprinting within ssh tunnel. Subsequent research utilized edit distance on packet size sequences for website identification [10, 47]. Wang et al. combined a manual feature set of 4226 features with k-nearest neighbor classifiers for WF attacks [79], while Hayes and Danezis [29] proposed k-FP method, which used a refined set of 150 features with random forest models for the same proposal. The introduction of deep learning techniques to WF by [1] has marked a significant evolution in the field, with subsequent research leveraging a variety of advanced deep learning models. These include convolutional neural networks [6, 63, 70], triplet networks [71], and generative adversarial networks [51], establishing a new research trajectory and representing the state-of-the-art in performance.

Building on the extensive evolution of WF techniques over the past two decades, targeted research on refining fingerprinting features has emerged as a critical focus within the domain. Panchenko et al. [52] introduced the CUMUL fingerprint, which leverages cumulative representations of packet sizes. Rahman et al. [58] developed the tik-tok attack, significantly utilizing the temporal characteristics of website packets. Shen et al. [65] proposed a robust fingerprinting feature based on time-window analysis. Beyond the traditional focus on transport layer information for WF, Siby et al. [69] introduced WF using side-channel encrypted DNS trafic; Nguyen et al. [33] constructed fingerprints combining IP addresses with browser rendering characteristics for large-scale WF. Li et al. [45] evaluated the website fingerprints themselves, proposing WeFDE method using information quantification theory to reason ably assess the information leakage of fingerprints, avoiding the potential biases of model selection and accuracy judgment.

![](images/75b1d124b550bb8c03cff4db37799193954ddf14dfd367f81155bd156ed48525.jpg)

<table><tr><td colspan="2">Discrete: 21%</td><td colspan="2">Overlap: 35%</td><td>Inclusive: 44%</td></tr><tr><td colspan="2"></td><td colspan="2"></td><td></td></tr><tr><td colspan="2"></td><td colspan="2"></td><td></td></tr><tr><td colspan="3">No HTTP/3: 35%</td><td></td><td></td></tr></table>

Figure 9: HTTP Version Parallelism Measurement. Venn dia gram showing the percentage of parallelism of various http versions for top 100k sites. The discrete, overlap, and inclusive in the bar chart represent that these websites use only one http version, use two http versions, and use three http versions in their web resources, respectively.

The research most aligned with the methodologies in this paper involves inferring protocol semantics from encrypted trafic [3, 25, 42, 55, 83, 87], utilizing attributes not concealed by encryption.

## B Measurement of HTTP Version Parallelism across Top 100k Websites

In our study, we conducted extensive measurements of HTTP version parallelism on the real internet to demonstrate the widespread occurrence of this phenomenon. Specifically, we automated access to the top 100k websites from the Tranco top-site ranking list. By retrieving browser log information, we assessed whether the access attempts were successful and recorded the HTTP version information used for each network resource within a single visit. Our definition of HTTP version parallelism is as follows: if the set of HTTP versions used across all network resources within a website contains only one element, we refer to this as "discrete"; if the set contains two elements, we call it "overlap"; and if network resources use HTTP/1.1, HTTP/2, and HTTP/3 concurrently, we describe this situation as "conclusive".

![](images/bba8519cba85e60d47260a71f83fb9f9459c508645c12f595b7749e1a58bff2d.jpg)  
Figure 10: Protocol State Machines Designed for Diferent HTTP Versions. In the diagram, ellipses represent system states, rounded rectangles indicate state transition conditions, and rectangles with cut corners denote functions bound to a specific state.

Table 5: Explanation of Protocol State Machine Elements

<table><tr><td>Identifier</td><td>Type</td><td>Description</td></tr><tr><td>Idle</td><td>state</td><td>Initial state of the protocol state machine</td></tr><tr><td>Request</td><td>state</td><td>Client requests a resource</td></tr><tr><td>Standby</td><td>state</td><td>Waiting for event trigger standby</td></tr><tr><td>Preface</td><td>state</td><td>Client sends preface packet</td></tr><tr><td>Settings</td><td>state</td><td>Client sends settings packet</td></tr><tr><td>End</td><td>state</td><td>Final state of the protocol state machine</td></tr><tr><td>get_pkt</td><td>transition</td><td>Retrieve any packet</td></tr><tr><td>get_s_pkt</td><td>transition</td><td>Retrieve short packet</td></tr><tr><td>get_l_pkt</td><td>transition</td><td>Retrieve long packet</td></tr><tr><td>EOF</td><td>transition</td><td>Process to end of file</td></tr><tr><td> $\epsilon$ </td><td>transition</td><td>Automatic state transition</td></tr><tr><td>Counter</td><td>variable</td><td>Resource quantity counter</td></tr><tr><td>counter++</td><td>function</td><td>Increment operation on counter</td></tr><tr><td>read_counter</td><td>function</td><td>Read counter value</td></tr></table>

The measurement results, as shown in Figure 9, indicate that nearly 80% of the websites exhibit HTTP version parallelism. Among these, over half of the websites show a relatively severe phenomenon: every version of the HTTP currently in use coexists among all their network resources. Additionally, we found that websites utilizing the HTTP/3 protocol almost invariably exhibit version parallelism, which can be attributed to the fact that new technologies are typically deployed incrementally. Our findings regarding the use of the HTTP/3 protocol diverge from other authoritative results [77]. This discrepancy arises because those studies focus on the homepage resource’s support for the protocol, whereas our discussion encompasses the application of the protocol across all network resources of the website.

## C Inferring resource quantity using protocol state machines

Our protocol state machines keep meticulous track of the state of encrypted trafic, as shown in Figure 10. The state machines start processing packets from the client in the idle state and recognize resource requests based on the transition conditions defined in Table 5. When a packet meets these conditions and triggers a resource request state, the corresponding counter is incremented. This approach focuses only on the number of resources transmitted in the data stream and is not afected by encryption masking content information.

It is worth noting that the packets generated by the application layer control features introduced by HTTP/2 and HTTP/3 are in dependent of the number of network resources. We blocked these control packets using two main methods: (1) adding an initial step that does not inflate the counter to ofset the efect of the setting packet, and (2) using packet size thresholds that filtered out control packets during resource transfers (in particular, packets below 40 bytes in HTTP/2 and packets below 120 bytes in HTTP/3).

## D Examples of H123 fingerprints

```txt
[ 1, 0, 0, 0, 0, 0] - h1
[ 0, 1, 0, 1, 2, 1] - h2
[ 0, 0, 20, 0, 0, 0] - h3

[ 0, 0, 0, 0, 0] - h1
[ 3, 10, 0, 0, 0] - h2
[ 0, 0, 3, 9, 13] - h3

[ 0, 0, 0, 4, 0, ..., 0, 0, 0] - h1
[ 7, 0, 2, 0, 2, ..., 0, 0, 1] - h2
[ 0, 17, 0, 0, 0, ..., 3, 14, 0] - h3

[ 0, 0, 0, 0, 0, 0] - h1
[ 4, 0, 17, 0, 0, 1] - h2
[ 0, 26, 0, 1, 2, 0] - h3

[ 0, 0, 0, 0, 0] - h1
[ 2, 0, 1, 1, 0] - h2
[ 0, 22, 0, 0, 40] - h3

[ 0, 0, 0, 6, 3, ..., 1, 0, 0] - h1
[ 3, 0, 3, 0, 0, ..., 0, 1, 2] - h2
[ 0, 34, 0, 0, 0, ..., 0, 0, 0] - h3

[ 0, 0, 0, 0, 0, 2] - h1
[ 3, 3, 0, 0, 1, 0] - h2
[ 0, 0, 82, 3, 0, 0] - h3

[ 1, 0, 0, 0, 5, ..., 0, 5, 0] - h1
[ 0, 3, 0, 2, 0, ..., 0, 0, 6] - h2
[ 0, 0, 2, 0, 0, ..., 115, 0, 0] - h3

[ 0, 0, 0, 0, 0, ..., 0, 0, 0] - h1
[ 2, 2, 4, 4, 0, ..., 1, 1, 1] - h2
[ 0, 0, 0, 0, 2, ..., 0, 0, 0] - h3

[ 1, 0, 0, 0, 0, ..., 0, 0, 0] - h1
[ 0, 3, 6, 5, 2, ..., 1, 1, 3] - h2
[ 0, 0, 0, 0, ... , ... , ... , ... , ... , ... , ... , ...
```  
Figure 11: H123 Fingerprint examples. Some of the fingerprints in the figure are not shown completely due to length reasons, with "L" indicating the length of the fingerprints.

Figure 11 presents real examples of H123 fingerprints for the 10 most frequently visited websites. These fingerprints combine the sequence of HTTP versions and the sequence of resource quantity generated during a website visit, resulting in a final fingerprint form of 3×L dimensions (where rows represent diferent HTTP versions, and columns represent each network flow). These examples of H123 fingerprints demonstrate two characteristics: (1) H123 fingerprints are concise and direct, stemming from their direct representation of the characteristics at the website’s network resource layer; (2)

H123 fingerprints are distinguishable. The quantity of network resources and the distribution of HTTP versions vary across diferent websites, creating a vast fingerprint space.

## E WATSON Distance-metric Pseudocode

Wasserstein distance, also known as Earth Mover’s Distance (EMD), is a method used in mathematics and data science to measure the diference between two probability distributions and is widely applied in various scenarios. We interpret the H123 fingerprint as a discrete distribution and calculate the one-dimensional Wasserstein distance for resource sequences of diferent HTTP versions, averaging the three results in the end. The one-dimensional Wasserstein distance for discrete distributions, as required in our case, has been proven to be equivalent to the cumulative distribution function (CDF) distance between two sequences [59], which greatly enhances computational eficiency and theoretical simplicity. Furthermore, based on preliminary experimental results, we decided to sort the sequence data numerically before computing the Wasserstein distance. The pseudocode for calculating the Wasserstein distance is shown in Algorithm 1

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Wasserstein Distance
Require: Two H123 fingerprints  $F_{1}$  and  $F_{2}$ 
Ensure: Normalized Wasserstein distance
1:  $W \leftarrow 0$  {Sum of Wasserstein distances}
2:  $T \leftarrow 0$  {Total sum of F1 elements for normalization}
3: for i = 0 to 2 do
4:  $C_{1} \leftarrow \text{ComputeCumulativeDistribution(Sort}(F_{1}[i]))$ 
5:  $C_{2} \leftarrow \text{ComputeCumulativeDistribution(Sort}(F_{2}[i]))$ 
6:  $W \leftarrow W + \sum_{j} |C_{1}[j] - C_{2}[j]|$  {Accumulate the absolute differences}
7:  $T \leftarrow T + \sum_{j} F_{1}[i][j]$  {Accumulate the total sum of  $F_{1}$  elements}
8: end for
9:  $W \leftarrow \frac{W}{T}$  {Normalize the Wasserstein distance}
10: return W
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 LCSS Distance
Require: Two H123 fingerprints $F_{1}$ and $F_{2}$, similarity threshold $\epsilon$
Ensure: Normalized LCSS distance
1: Initialize LCS matrix $dp$ with size $(len(F_{1}) + 1) \times (len(F_{2}) + 1)$
2: for $i = 1$ to $len(F_{1})$ do
3:    for $j = 1$ to $len(F_{2})$ do
4:    threshold $\leftarrow \epsilon \cdot \max(F_{1}[i - 1], F_{2}[j - 1])$ {Calculate similarity threshold}
5:    if $|F_{1}[i - 1] - F_{2}[j - 1]| \leq threshold$ then
6:    $dp[i][j] \leftarrow dp[i - 1][j - 1] + 1$
7:    else
8:    $dp[i][j] \leftarrow \max(dp[i - 1][j], dp[i][j - 1])$
9:    end if
10:    end for
11: end for
12: Compute LCSS by tracing back through $dp$ matrix
13: return $1 - \frac{\text{sum of LCSS}}{\text{sum of } F_{1}}$
</div>

Table 6: Detail of network conditions.

<table><tr><td>Scenario</td><td>Upload Bandwidth</td><td>Download Bandwidth</td><td>Network Latency</td><td>Packet Loss Rate</td></tr><tr><td>Unconstrained</td><td>&gt;500mbps</td><td>&gt;500mbps</td><td>&lt;10ms</td><td>&lt;1%</td></tr><tr><td>Starlink-like</td><td>8mbps</td><td>70mbps</td><td>50ms</td><td>6%</td></tr><tr><td>Slow</td><td>300kbps</td><td>800kbps</td><td>350ms</td><td>3%</td></tr></table>

The Longest Common Subsequence (LCS) algorithm is a method used to find the longest shared subsequence between two sequences. It has broad applications in fields such as text comparison and data mining. In our application scenario, sequence elements (the number of resources) may exhibit minor variations due to various reasons, making the traditional LCS algorithm less suitable, as it requires exact matching of sequence elements. To address this issue, we pro pose the Longest Common Similar Subsequence (LCSS) distance, which introduces a similarity threshold, allowing for certain varia tions in the elements of the sequence. This distance focuses more on assessing the overall similarity of non-sparse sequences, and we choose to use network resource sequence fingerprints (which do not explicitly label HTTP versions) for measurement. The pseudocode for calculating LCSS distance is shown in Algorithm 2.

## F Dataset details

Closed-World (CW) dataset. As in most related work [33, 49, 70], we first construct attack scenarios for popular websites based on the most recent Tranco top-site ranking list<sup>2</sup> [56]. We focus on and collect data from the top 1600 websites, which, to our knowledge, constitutes the closed-world dataset with the largest number of categories involved. In addition, we consider more realistic scenar ios of interest to attackers, including a random selection of 320 websites from the top 10k websites of the Tranco list; and a scenario that simulates network censorship by conducting a WF attack on 320 websites from the Citizenlab list [43], which are known to be susceptible to such scrutiny.

Bandwidth dataset. Cross-network condition scenarios (where there are significant diferences between the network environments during training and testing data collection) are considered a major challenge in making WF attacks practical [4, 15, 86]. Since it is impossible to cover all possible network conditions, we designed three network scenarios with typical diferences and used them for cross-validation of the attack method (training the model in one network condition and testing it in others).

We primarily considered the following four network perfor mance metrics: Upload Bandwidth, Download Bandwidth, Network Latency and Packet Loss Rate. As shown in Table 6, the first scenario is unconstrained, representing a good network environment typical for most users. This setup is based on network measurement results from Cloudflare Radar [57]. The second scenario is starlink like, simulating users accessing websites via Starlink’s commercial satellite internet service. According to the measurement results in [8], Starlink is characterized by relatively slow speeds and higher packet loss rates. The final scenario is slow, which simulates condi tions in countries with poor network infrastructure or in situations of sustained slow network speeds due to congestion, characterized by low bandwidth and high latency.

During data collection phase, to accurately simulate these network conditions, we referred to the Chrome Developer documentation [22] and used Chrome’s network throttling feature to create custom network conditions.

Browser dataset. As in related work [35, 68], we selected the two most prevalent cross-platform browsers [73], Google Chrome and Mozilla Firefox, to construct our dataset. Given that Microsoft Edge utilizes the same rendering engine as Chrome, it was deemed non-distinctive for our purposes and thus excluded. To capture a broader range of user update practices, we also included a legacy Chrome (v104) along with the latest Chrome (v126) and Firefox (v129). Across diferent scenarios, we collected trafic data from the top (Tranco list) 200 websites.

Time-Drift dataset. During the data collection process, we purposefully introduced time intervals, which naturally led to the above three datasets exhibiting concept drift. Specifically, we initiated the collection of the Bandwidth dataset on the 18th day and the Browser dataset on the 30th day following the completion of the CW dataset. To construct a temporal sequence dataset, we selected the CW-popular dataset (0 day) as a temporal reference and combined it with the Bandwidth-unconstrained dataset (18 days later) and the Browser-chrome dataset (30 days later). Consistency in the collection environment across these datasets ensures the comparability of our temporal analysis.

Open-World (OW) dataset and Supplementary data. We selected the first 80,000 unique websites from the Tranco list that were not previously collected to serve as the open-world scenario. Additionally, we have supplementary data consisting of the top 400 websites, each with 40 samples, collected half a year ago. This additional data only serves two specific purposes: (1) independent hyperparameter tuning for the H&W method, and (2) acting as essential pre-training data for Triplet Fingerprinting [71].

During the data collection process, we followed the methodology established in prior work [4, 49, 70], excluding websites that failed to load, displayed CAPTCHA, had no meaningful content, or involved fewer than 50 packets. These sites are generally not of interest to attackers since they lack practical relevance for users [49]. In line with previous research [66, 68], we employed an automated approach using Selenium (v4.15.2) to control Chrome browser (v126) (except for the browser dataset) and visit the homepage of each website. This method produces more realistic trafic compared to tools like wget or curl. The network trafic generated during the process was captured using tcpdump.

Following the recommendation in [39], we used a round-robin fashion during data collection to ensure more realistic and representative trafic. We deployed 10 Amazon cloud servers, located in North America, running Ubuntu 24.04 to execute the data collection in parallel batches. The data collection was conducted from July 2024 to September 2024. For the open-world scenario, each website was accessed once, whereas for other scenarios, we collected 50 samples per website and retained 40 valid samples. After each round of data collection, we conducted a separate DNS resolution for all web resources to build IP-WF [33].

![](images/b069584d36e10d06f2ca5024092eb1f7d3f8861d4bff8b43a13c10d1e9fe1a2f.jpg)  
Figure 12: Comparison of attack robustness across network conditions with N = 1 in the Bandwidth dataset.

![](images/dce360c9ad120623ffcf9a2644560ce6b90fa1b6f30a33d361392b274e5adb0d.jpg)  
Figure 13: Impact of Hyperparameters on WF Attack Accu racy

## G Detailed Hyperparameter Optimization of H&W

In this section, we will discuss the impact of hyperparameters in HOLMES and WATSON on the efectiveness of WF, and ultimately select hyperparameters that achieve a trade-of between performance and eficiency.

Maximum Fingerprint Length, L. HOLMES-generated finger prints are $3 \times L$ two-dimensional matrices, where L represents the number of HTTP connections established by the website. L is another factor afecting fingerprint matching performance and eficiency. By truncating overly long fingerprints, we studied the impact of diferent fingerprint retention lengths on performance (Figure 13(a)) and determined L to be 50.

LCSS Similarity Threshold, �. In the LCSS algorithm, we set a similarity threshold � for judging similar subsequences, reflecting the algorithm’s tolerance for fluctuations in website resource num bers. Through experimentation, we established � as 0.24 (Figure 13(b)).

WATSON’s Distance Measurement Weight, w. Tailoring to the characteristics of the H123 fingerprint, we use Wasserstein and LCSS distances to comprehensively evaluate the similarity between two fingerprints. We set the weight for the Wasserstein distance measure as w, and for the LCSS distance measure as 1-w. Based on the experimental results shown in Figure 13(c), we determined w to be 0.5.

H Case study: browsers and defense strategies In this section, we will provide a detailed overview of H&W’s applicability across diferent browsers and the impact of existing defense mechanisms on its attack performance.

Table 7: Evaluation results on diferent browsers.

<table><tr><td rowspan="2">Scenario</td><td colspan="2">Individual</td><td colspan="2">Cross-version</td><td colspan="2">Cross-browser</td></tr><tr><td>N=1</td><td>N=10</td><td>N=1</td><td>N=10</td><td>N=1</td><td>N=10</td></tr><tr><td>Chrome</td><td>88.4 ± 0.6</td><td>98.6 ± 0.3</td><td>62.2 ± 1.2</td><td>73.3 ± 1.2</td><td>4.9 ± 0.9</td><td>6.8 ± 0.5</td></tr><tr><td>Chrome-legacy</td><td>87.5 ± 0.9</td><td>98.2 ± 0.3</td><td>58.9 ± 1.1</td><td>74.6 ± 1.2</td><td>-</td><td>-</td></tr><tr><td>Firefox</td><td>83.6 ± 1.8</td><td>98.0 ± 0.5</td><td>-</td><td>-</td><td>4.2 ± 0.9</td><td>6.3 ± 0.7</td></tr></table>

## H.1 Attack performance on diferent browsers

We conducted cross-training and testing of H&W on the Browser dataset, with results presented in Table 7. Training and testing on the same data distribution (within the same browser) yielded reasonable results across diferent browser scenarios; for instance, in Chrome with N = 1, the attack accuracy was 88.4%. When N increased to 10, the attack accuracy exceeded 98% across all browsers. We observed a slight decrease in accuracy on Firefox, likely due to the greater diversity of control frames triggered during resource loading, which complicates resource inference.

Initially, we expected H&W to demonstrate strong cross-browser capability since it extracts application layer resource features. However, the actual results showed high sensitivity to changes in data distribution when switching browsers. In cross-browser version experiments, we noted about a 20% drop in accuracy, and H&W became inefective in cross-browser tests. This is attributed to significant diferences in how Chrome and Firefox handle website resources, leading to noticeable discrepancies in the resource sequences extracted by HOLMES for the same website.

We must emphasize that cross-browser applicability remains an open problem in website fingerprinting attacks. Similar to the results in [68], we conducted the same cross-browser validation for k-FP+ and obtained comparable outcomes, with an accuracy of 6.5% when N = 10. To address the challenges of cross-browser scenarios, we suggest incorporating samples from multiple browsers during the training phase or using JA4 fingerprinting [46] to identify the browser before conducting the attack. However, these considerations are beyond the scope of this paper and will be left for future work.

Table 8: Evaluation results under padding-based defense.

<table><tr><td rowspan="2">Scenario</td><td colspan="2">k-FP+</td><td colspan="2">DF+</td><td colspan="2">H&amp;W</td></tr><tr><td>N=1</td><td>N=10</td><td>N=1</td><td>N=10</td><td>N=1</td><td>N=10</td></tr><tr><td>No defense</td><td>69.4 ± 1.2</td><td>98.3 ± 0.2</td><td>46.9 ± 2.1</td><td>97.6 ± 0.1</td><td>90.4 ± 1.0</td><td>98.6 ± 0.3</td></tr><tr><td>Defense with prior know.</td><td>50.3 ± 0.5</td><td>90.8 ± 0.4</td><td>38.6 ± 1.2</td><td>96.9 ± 0.1</td><td>81.0 ± 1.2</td><td>95.5 ± 0.7</td></tr><tr><td>Defense without prior know.</td><td>3.5 ± 1.0</td><td>6.4 ± 0.6</td><td>2.1 ± 1.1</td><td>5.9 ± 0.6</td><td>5.7 ± 0.9</td><td>6.9 ± 0.9</td></tr></table>

## H.2 Attack performance under defense strategies

In existing research on anonymous networks, various advanced WF defenses have been proposed to counter WF attacks. These strategies typically introduce perturbations to standard trafic characteristics by adding redundant packets [28, 40], delaying transmissions [9, 81], or splitting application flows [19]. However, the use of these defenses in anonymous networks relies on bidirectional cooperation within the system, meaning that the perturbations added by the Tor client must be removed at the relay nodes so that the trafic reaching the actual server is free of these disturbances. In contrast, there is no such communication mechanism or protocol in standard HTTPS that enables coordinated defense between the client and server to implement these advanced trafic defenses.

![](images/e3049143d01a20b802b803aac79311103ddfd2ccd1d34b3d10b9ae78c07e1e3f.jpg)  
Figure 14: Network Protocol Stack in HTTP Version Parallelism Scenario. HTTP/1.1 and HTTP/2 protocols can use TLS 1.2 and TLS 1.3, respectively, as their security layers; HTTP/3 can only use QUIC as its security layer.

Packet padding is a simple yet efective method of trafic ob fuscation [41]. In the context of standard HTTPS, some studies have explored using the padding mechanism provided by QUIC at the transport layer to introduce server-agnostic defense perturba tions [68, 72]. Although this technique has not yet been adopted by mainstream browsers, we simulate this feasible defense strategy and evaluate its impact on WF attacks. Specifically, we use the CW-random dataset, padding each packet to its maximum length to construct a defense dataset. Existing work often assumes that attackers have prior knowledge of the defense strategies being im plemented [65, 70], meaning they can train models on the defense dataset. We also consider a more challenging scenario where the attacker is unaware of the defense strategy.

We evaluated the performance of k-FP+, DF+, and H&W under the defense mechanism. First, we trained and tested on the dataset without packet padding as a performance baseline. Next, we assessed the performance of various methods when the attackers had prior knowledge of the defense strategy. As shown in Table 8, packet-padding defenses did not efectively mitigate website fingerprinting attacks under adversarial conditions. For instance, when N= 10, the accuracy of H&W remained at 95.5%, only about 3% lower compared to the scenario without defense.

In the experiments where attackers were unaware of the defense implementation, most website fingerprinting methods became nearly inefective, losing practical utility. This is because the packet-padded test data introduced significant distribution diferences compared to the original training data. However, it is important to emphasize that users cannot rely on attackers’ ignorance of the defense strategy. Instead, eforts should focus on developing more robust defense mechanisms.
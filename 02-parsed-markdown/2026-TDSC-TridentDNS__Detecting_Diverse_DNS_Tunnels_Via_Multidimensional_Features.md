# TridentDNS: Detecting Diverse DNS Tunnels via Multidimensional Features

Lin Ye, Runze Xie, Zhongyun Hua, Yunting Zhang, Wei Jiang

Abstract—Domain Name System (DNS) tunneling encapsulates data in DNS messages to establish covert communication channels. It is widely employed by adversaries for data exfiltration and network intrusion. Existing detection studies primarily focus on conventional DNS tunnels that employ centralized architectures and domain-relay communication for high-throughput data exfiltration. However, heterogeneous DNS tunnels that depart from this design, such as those employing IP-direct communication or distributed architectures, remain largely underexplored, as their stealthier and more diverse behaviors make them harder to systematically model and detect. To address these challenges, we propose TridentDNS, a heterogeneous DNS tunnel detection framework based on multidimensional features. TridentDNS adopts an unsupervised anomaly detection paradigm to learn normal DNS patterns from benign traffic and detect anomalous traffic. To ensure anomaly-free training data, TridentDNS employs a multistage-filtering-based online learning framework that filters anomalous samples during training. Recognizing that heterogeneous DNS tunnels may employ distributed architectures or IP-direct communication, TridentDNS jointly analyzes DNS sessions, domain names, and traffic flows via a multidimensional fusion strategy. It further introduces novel features at both the domain and flow dimensions. To overcome the shortage of heterogeneous DNS tunneling data, we developed HiveTunnel, a highly customizable DNS tunneling testing tool. Experimental results demonstrate that TridentDNS achieves strong detection performance on conventional high-throughput DNS tunnels and benign DNS traffic, while effectively detecting all evaluated heterogeneous DNS tunnel types.

Index Terms—DNS tunneling detection, anomaly detection, data exfiltration, distributed DNS tunneling, autoencoder

## I. INTRODUCTION

S a core infrastructure of the Internet, the Domain Name System (DNS) primarily provides the mapping between domain names and IP addresses [1], [2]. However, the DNS protocol was not originally designed for data transmission. As a result, traditional security mechanisms provide insufficient inspection of DNS traffic, creating opportunities for adversarial exploitation [3], [4]. The widespread deployment of DNS further amplifies this issue, making DNS tunneling a widely adopted technique by bypassing conventional security defenses. In DNS tunneling attacks, adversaries embed data within DNS query and response messages to establish covert communication channels for data exfiltration and remote command delivery. By leveraging the permissive and trusted nature of DNS traffic, such attacks can evade existing detection mechanisms and pose a serious threat to network security. The working principle of DNS tunneling [5] is illustrated in Fig. 1, where the numbered arrows indicate the sequence of packet interactions. For simplicity, throughout this paper, the term “DNS tunnel server” refers to the authoritative DNS server controlled by attackers and used for DNS tunneling.

Existing DNS tunnel detection schemes face significant challenges in identifying heterogeneous DNS tunnels. On the one hand, most previous studies have focused on domain-relay DNS tunnels, in which compromised hosts communicate with tunnel servers through the standard DNS resolution process. These works commonly assume that IP-direct DNS tunnels, where compromised hosts communicate directly with tunnel servers using IP addresses, are easily regulated in strictly controlled network environments and therefore pose limited threats [6], [7]. However, in minimally restricted environments, such as home networks, IP-direct DNS tunnels can be even more harmful than domain-relay tunnels due to their higher transmission efficiency. Moreover, by bypassing the standard domain resolution processes, IP-direct DNS tunnels enable attackers to arbitrarily manipulate the primary domain in DNS packets or even masquerade it as a legitimate domain, thereby effectively evading domain-based detection mechanisms.

On the other hand, existing detection approaches typically assume that a DNS tunnel is established using a single primary domain between a single pair of IP addresses [8], [9], [10]. In contrast, real-world attacks increasingly adopt distributed DNS tunneling strategies. For example, Infoblox reported in 2024 that the BlackCat ransomware group rapidly rotated multiple malicious domains while employing DNS tunneling [11], [12]. A case documented by Unit42 further revealed an attack against financial-sector organizations that involved 22 tunnel domains sharing 7 name-server IPs [13]. Similarly, Infoblox observed the simultaneous use of multiple tunnel domains and server IPs in the Decoy Dog campaign disclosed in 2023 [14]. These incidents indicate that DNS tunnels in real-world attacks often adopt distributed architectures, which distribute traffic across multiple independent sessions and thereby significantly enhance stealthiness [15]. These architectural differences limit the effectiveness of conventional, single-dimensional detection methods [16], [17] against distributed DNS tunneling attacks.

Existing DNS tunnel detection schemes face significant challenges in real-world networks. Current research primarily employs model-based approaches [18], categorized into offline and online learning paradigms [19]. Offline learning trains models on static datasets and deploys them for inference, while online learning incrementally updates models with streaming data for continuous adaptation to evolving traffic patterns [20]. Most existing schemes [8], [17], [21] rely on offline learning. These approaches achieve satisfactory performance for highthroughput tunnels but struggle in low-throughput scenarios, where higher detection precision is required to distinguish stealthy DNS tunnels from dynamic legitimate traffic. Although several studies [22], [23] introduce online learning mechanisms, they typically assume all training traffic is benign. This assumption creates a critical vulnerability. If tunneling traffic is already present during training, models risk data poisoning, leading to degraded detection performance [24].

![](images/b8010b312b0ae02bf7e5bd59eb9b3e858c4ef1e991a81d75b1b923295d8b7274.jpg)  
Fig. 1. Illustration of domain-relay and IP-direct DNS tunneling.

To address the aforementioned challenges, this paper proposes TridentDNS, a heterogeneous DNS tunnel detection framework based on multidimensional features. TridentDNS is designed as an unsupervised anomaly detection system trained exclusively on benign traffic. It consists of three main components: a traffic acquisition module, a traffic parsing module, and a DNS tunnel detection module. To overcome the limited robustness of existing approaches in real-world network environments and their excessive dependence on training data, we introduce an online learning mechanism with self-purification capability in the traffic acquisition module. This mechanism effectively filters DNS tunnel traffic through three core components: feature clustering, VirusTotal filtering, and large language model discrimination.

To effectively detect diverse DNS tunneling behaviors, TridentDNS adopts a multidimensional fusion strategy across the traffic parsing and detection modules, structured as a “trident” paradigm. Specifically, TridentDNS performs detection across three dimensions: DNS sessions, domain names, and data flows. The DNS session dimension serves as the tip of the trident, providing first-layer aggregation and enabling fast and accurate detection of high-throughput DNS tunnels. The domain dimension forms one wing of the trident and targets distributed DNS tunnels that distribute traffic across multiple server IPs. The flow dimension forms the other wing of the trident and captures IP-direct DNS tunnels as well as distributed DNS tunnels that rotate multiple domain names. Both the domain and flow dimensions leverage crosssession aggregation and focus on detecting low-throughput DNS tunnels that are difficult to distinguish when analyzing individual sessions alone. By jointly analyzing these dimensions, TridentDNS can effectively detect DNS tunnels with varying throughput, architectures, and communication modes.

Furthermore, due to the lack of publicly available datasets for distributed DNS tunneling, we develop HiveTunnel to support the evaluation of TridentDNS. HiveTunnel can flexibly generate various types of domain-based heterogeneous DNS tunneling traffic, providing comprehensive data support for detection schemes targeting heterogeneous DNS tunnels.

The main contributions are summarized as follows:

1) We characterize the structural heterogeneity of DNS tunnels and propose a multidimensional detection strategy structured as a trident paradigm. This strategy maps the session, domain, and flow dimensions to different DNS tunnel types. Based on the targeted tunnel types, we design new features for the corresponding dimensions.

2) We propose TridentDNS, an unsupervised anomaly detection framework targeting diverse DNS tunnels. TridentDNS introduces an online learning strategy with a self-purification capability to prevent model contamination during updates. To enable systematic evaluation, we develop HiveTunnel, a highly customizable heterogeneous DNS tunnel testing tool, and release it on GitHub<sup>1</sup>.

3) Experimental results demonstrate that TridentDNS achieves strong detection performance on both benign DNS traffic and conventional high-throughput DNS tunnels, while effectively detecting all evaluated DNS tunnel types in the heterogeneous DNS tunnel dataset and significantly outperforming existing approaches.

The remainder of this paper is organized as follows. Section II introduces different types of DNS tunnels and their definitions considered in this work. Section III reviews related work on DNS tunnel detection. Section IV details the system architecture of TridentDNS, along with the design principles of each component. Section V describes the experimental setup, including the environment and datasets employed, and presents the evaluation results. Section VI discusses the limitations of our approach and directions for future work. Finally, Section VII concludes the paper.

## II. PRELIMINARIES AND PROBLEM DEFINITION

Existing studies [25], [18], [26] have shown that DNS tunnels differ substantially in their communication modes, throughput, and architectures, which directly impact their stealthiness and potential harm. As outlined in Section I, DNS tunnels can be classified by communication mode into domain-relay and IP-direct types [5]. IP-direct tunnels, due to the absence of recursive resolution, achieve higher efficiency and can evade domain-based detection by dynamically altering domains.

DNS tunnels also vary in throughput. Low-throughput tunnels restrict both query payload size and transmission frequency, producing traffic patterns that closely resemble legitimate DNS. Following Gan et al. [26], we use a domain name length of 30 bytes as an effective threshold. In this paper, queries shorter than this and below the average frequency observed in our experimental environment are considered lowthroughput, while all remaining cases are classified as highthroughput. Attackers of low-throughput tunnels may leverage distributed architectures such as domain rotation, Fast-Flux [27], and domain-based load balancing to enhance transmission efficiency and evade single-dimensional detection. In contrast, high-throughput tunnels, due to their pronounced traffic patterns, are typically detectable from individual packets, making the advantages of diverse communication modes and architectures difficult to realize.

For clarity, in this paper, “distributed DNS tunnels” specifically refer to distributed low-throughput tunnels, whereas “conventional DNS tunnels” denote centralized highthroughput tunnels widely studied in prior work. The term “heterogeneous DNS tunnels” broadly encompasses lowthroughput tunnels, both centralized and distributed. The formal definitions are summarized in Table I. Our work primarily focuses on heterogeneous DNS tunnels, which remain challenging for existing detection methods.

TABLE I  
DEFINITIONS OF VARIOUS DNS TUNNELS IN THIS PAPER

<table><tr><td rowspan="2">Category</td><td rowspan="2">Throughput</td><td colspan="3">Architecture</td><td colspan="2">Mode</td></tr><tr><td>Type</td><td>#IPs</td><td>#Domains</td><td>DR</td><td>ID</td></tr><tr><td>CDT</td><td>High</td><td>Centralized</td><td>1</td><td>1</td><td>√</td><td>√</td></tr><tr><td rowspan="4">HDT</td><td rowspan="4">Low</td><td>Centralized</td><td>1</td><td>1</td><td>√</td><td>√</td></tr><tr><td rowspan="3">Distributed</td><td>1</td><td>&gt;1</td><td>√</td><td>√</td></tr><tr><td>&gt;1</td><td>1</td><td>√</td><td>√</td></tr><tr><td>&gt;1</td><td>&gt;1</td><td>√</td><td>√</td></tr></table>

CDT and HDT represent Conventional and Heterogeneous DNS Tunnels, respectively; DR and ID represent Domain-Relay and IP-Direct, respectively.

## III. RELATED WORK

This section provides a systematic analysis of studies on DNS tunneling detection. Existing methods can be broadly classified into five categories: packet-based, DNS sessionbased, domain-based, flow-based, and multi-dimension-based methods. We evaluate the methods based on detection mechanisms, online learning capability, and their performance in identifying low-throughput DNS tunnels. A detailed comparison of representative methods is provided in Table II.

## A. Packet-Based Methods

Packet-based detection schemes [17], [29], [57], [33] treat individual packets as the detection unit and are mainly effective against high-throughput DNS tunnels with distinct anomalies. By contrast, malicious behavior in low-throughput DNS tunnels is often difficult to infer from individual packets alone, making packet-based detection schemes generally ineffective.

Signature-based methods [9] detect DNS tunnels by matching predefined signatures of known tunneling tools. Despite their simplicity, such methods require substantial manual effort for signature generation, are vulnerable to evasion, and demand frequent updates. Adiwal et al. [9] proposed a signaturebased approach that constructs signatures for representative DNS tunneling activities and integrates them into SNORT rule sets. However, such methods exhibit limited effectiveness against previously unseen DNS tunneling.

Machine learning (ML)-based methods [28], [29] and deep learning (DL)-based methods [8], [16], [17] train models on manually or automatically extracted feature data to identify and classify DNS tunnels. These approaches partially overcome limitations of rule-based detection and have become mainstream in recent years. For example, Wu et al. [28] proposed an ML-based system that extracts feature vectors from the domain names in DNS packets, which are then classified using Random Forest and other ensemble algorithms. Similarly, Altuncu et al. [17] proposed a DL-based system using deep neural networks to extract features and classify individual packets for real-time blocking of DNS tunneling attacks. However, both of these approaches perform poorly when detecting low-throughput DNS tunnels.

## B. DNS Session-Based Methods

In existing research [7], [26], a DNS session is typically defined as a single query-response pair, referred to here as a narrow DNS session. However, a single domain query often triggers multiple related interactions in real traffic, which a query-response pair cannot fully capture. To address this, we define a broad DNS session as all consecutive DNS packets exchanged between the same endpoints for the same primary domain. Detection schemes based on narrow DNS sessions [26], [6], [54] aggregate traffic by the (src ip, src port, domain, dst port, dst ip) tuple, focusing on evaluating the overall reasonableness of messages and capturing anomalies in either queries or responses. In contrast, schemes based on broad DNS sessions [36] aggregate traffic by the (src ip, domain, dst ip) tuple, providing more complete traffic data and offering advantages in detecting lowthroughput tunnels. Nevertheless, both session types have limited observation scope, reducing detection efficiency against distributed DNS tunnels when either domains or IPs change.

TABLE II  
SUMMARY OF EXISTING DNS TUNNEL DETECTION METHODS

<table><tr><td>Detection Dimensions</td><td>Study</td><td>Detection Mechanism</td><td>Low-Throughput Detection</td><td>Online Learning</td></tr><tr><td rowspan="3">Packet-based</td><td>Adiwal [9]</td><td>Signature-based</td><td>×</td><td>×</td></tr><tr><td>Wu2020 [28], Mahdavifar [29], Ahmed [30], Abualghanam [31], Wu2020b [32], Liu2025 [33]</td><td>ML-based</td><td>×</td><td>×</td></tr><tr><td>Zhang [8], Chen [16], Altuncu [17], Lal [10], Liang [34], Kuang [35]</td><td>DL-based</td><td>×</td><td>×</td></tr><tr><td rowspan="3">DNS Session-based</td><td>Paxson [36]</td><td>Threshold-based</td><td>√</td><td>×</td></tr><tr><td>Wang2022 [7], Yang [6], Ruiling [26], Aiello [37], Shafieian [38], Duan [39]</td><td>ML-based</td><td>×</td><td>×</td></tr><tr><td>Tu [40], D’Angelo [41], De Bernardi [42]</td><td>DL-based</td><td>×</td><td>×</td></tr><tr><td rowspan="6">Domain-based</td><td>Ozery [23]</td><td>Threshold-based</td><td>√</td><td>√</td></tr><tr><td>Joback [43], Nadler [44]</td><td>ML-based</td><td>√</td><td>×</td></tr><tr><td>Liu2017 [45], Liu2020b [46], Luo [21]</td><td>ML-based</td><td>×</td><td>×</td></tr><tr><td>Marchal [47]</td><td>ML-based</td><td>×</td><td>√</td></tr><tr><td>Zou [48]</td><td>DL-based</td><td>√</td><td>×</td></tr><tr><td>Ishikura [49], Gao [50]</td><td>DL-based</td><td>×</td><td>×</td></tr><tr><td rowspan="4">Flow-based</td><td>Bai [51], Nguyen [52]</td><td>ML-based</td><td>×</td><td>×</td></tr><tr><td>Liu2023 [53]</td><td>ML-based</td><td>√</td><td>×</td></tr><tr><td>Willems [54], Sammour [55]</td><td>DL-based</td><td>×</td><td>×</td></tr><tr><td>Mirsky [22]</td><td>DL-based</td><td>×</td><td>√</td></tr><tr><td rowspan="3">Multi-Dimension-based</td><td>Jiang [56]</td><td>ML-based</td><td>×</td><td>×</td></tr><tr><td>Lambion [57]</td><td>DL-based</td><td>×</td><td>×</td></tr><tr><td>TridentDNS (Ours)</td><td>DL-based</td><td>√</td><td>√</td></tr></table>

ML and DL represent machine learning and deep learning, respectively.

Threshold-based methods [23], [36] statistically analyze selected features and compare the results with predefined thresholds. They provide better generality and flexibility, enabling the detection of unknown tunnels, though their adaptability remains limited. Paxson et al. [36] proposed a threshold-based method that applies lossless compression to information vectors within broad DNS sessions to estimate and bound the amount of information transmitted through DNS tunnels, thereby detecting low-throughput DNS tunnels. However, since the estimated upper bound of information is used as the threshold, this method may produce relatively high false positive rates when encountering legitimate high-entropy DNS packets, such as those generated by CDN domains.

## C. Domain-Based Methods

The primary domain consists of the second-level domain and top-level domain, identifying the core part of a domain name [58]. The prefix attached to it is the subdomain, used to distinguish different services or hosts under the same primary domain [58]. Domain-based detection schemes [43], [33], [44] aggregate traffic by the primary domain (domain) for detection. Compared to packet-based or session-based methods, they are more effective for detecting low-throughput DNS tunnels but have limited effectiveness against tunnels that frequently change the domains, such as IP-direct DNS tunnels.

For threshold-based detection, the method proposed by Ozery et al. [23] uses an information-based heavy hitter to estimate the real-time amount of information transmitted to domains, thereby detecting DNS data exfiltration. Nevertheless, since this method performs threshold-based detection on the amount of information associated with a primary domain, it may become ineffective against IP-direct DNS tunnels where domain names can be frequently changed. For MLbased detection, the method proposed by Nadler et al. [44] extracts domain features from logs and applies Isolation Forest for anomaly detection. The use of time windows, however, narrows the observation scope, which reduces its capability to detect low-throughput DNS tunnels. For DL-based detection, Gao et al. [50] proposed a method that constructs DNS recursive resolution graphs and applies GraphSage to aggregate node and edge features, enabling effective detection. This method relies on a complex graph neural network, which results in relatively low detection efficiency.

## D. Flow-Based Methods

A data flow comprises all packets exchanged between the same endpoints. Flow-based detection schemes [51], [22] use the (src ip, dst ip) tuple to aggregate traffic, enabling the identification of IP-direct and low-throughput DNS tunnels. Unlike DNS session-based methods, such schemes do not consider domains or the interactions within the flow. However, flow-based methods exhibit reduced performance against distributed DNS tunnels that utilize multiple server IPs.

For example, Liu et al. [53] proposed an ML-based method that uses SVM to classify traffic based on time-frequency domain features for DNS tunnel detection. Nevertheless, benign DNS traffic in real-world environments may also exhibit periodicity similar to DNS tunnels, potentially confounding frequency-domain analysis. Mirsky et al. [22] proposed a DL-based method that clusters flow features and employs an ensemble of autoencoders for anomaly detection. However, as a general intrusion detection system, it is not tailored to DNS tunnels, which may limit its effectiveness in this context.

## E. Multi-Dimension-Based Methods

A few studies [56], [57] propose detection approaches based on multiple objects, but with limitations in object selection.

Lambion et al. [57] proposed an ML- and DL-based detection method that analyzes individual DNS query packets and narrow DNS sessions using random forests and convolutional neural networks, respectively, enabling efficient identification of DNS tunneling. However, the associations between these objects are weak, lacking an effective coordination mechanism. Moreover, due to the fine granularity of the selected objects, the observation perspective is limited, making the approach less effective against distributed DNS tunnels.

Although prior studies [36], [33] have recognized distributed DNS tunneling, few approaches specifically address this challenge. Existing methods, whether based on single- or multidimensional detection objects, lack dedicated mechanisms for handling distributed DNS tunnels. To bridge this gap, we propose TridentDNS, a heterogeneous DNS tunneling detection framework. TridentDNS leverages multidimensional features to identify various DNS tunnels that use domain names as carriers, including distributed DNS tunnels.

Furthermore, as shown in Table II, most existing studies adopt model-based detection methods. Among these, supervised learning approaches achieve high detection accuracy with sufficient labeled data, but their reliance on labeled datasets and limited generalization to unseen or zero-day attacks reduce their practicality. In contrast, unsupervised learning methods do not require labeled data and can detect novel attacks, though they may incur higher false positive rates due to the lack of explicit guidance. Online learning strategies have been explored in only a few works [23], [47], [22], most of which rely on unsupervised anomaly detection. However, such approaches typically introduce security risks. Specifically, both Ozery et al. [23] and Mirsky et al. [22] adopt the Peacetime/Wartime online learning strategy [59], which presupposes that all traffic collected during the training phase is benign. When the detection system is deployed in real-world network environments that contain malicious traffic, malicious samples may be incorrectly labeled as benign and incorporated into the model training process, thereby compromising the training procedure and degrading detection performance. To mitigate this vulnerability, this paper proposes an online learning scheme for TridentDNS based on unsupervised anomaly detection, with self-purification capabilities enabled by a multi-stage filtering mechanism.

## IV. METHODOLOGY

TridentDNS consists of three main components, namely a traffic acquisition module, a traffic parsing module, and a DNS tunnel detection module. This section details the design and implementation of these modules. The overall framework of TridentDNS is illustrated in Fig. 2.

## A. Traffic Acquisition

In prior research, benign DNS traffic has primarily been sourced from three categories: simulated traffic targeting popular domains, public datasets, and real-world network traffic. Simulated traffic targeting popular domains generates datasets by scripting queries to domains from popularity rankings and receiving responses. However, the resulting traffic often exhibits simplistic domain structures and resolution processes that differ from real environments. Public datasets offer ease of access and use, yet the network environments they reflect may not fully align with the application scenarios required for experiments. Real network traffic more comprehensively reflects actual usage environments, but its purity remains difficult to ensure, as it may contain malicious traffic [60]. Removing anomalies requires substantial manual effort for identification.

To address the aforementioned issues, this paper proposes a DNS traffic acquisition scheme based on Selenium and virtual machines. The scheme constructs an isolated network via virtual machines to ensure traffic purity. It employs Selenium scripts to simulate user browsing behaviors, thereby guaranteeing traffic authenticity. This approach simplifies the acquisition process, reduces manual intervention, and produces traffic that closely mimics real user behavior patterns. Fig. 3 illustrates its implementation.

![](images/3b56cc5b13477ce827b7f69274e50221e60d66b3b236ba92737052555c807901.jpg)  
Fig. 3. Traffic Acquisition Environment

The user side deploys two virtual machines on a single host. Virtual machine A (VM A) functions as the DNS client, while virtual machine B (VM B) serves as the local recursive resolver. The server side consists of multiple public DNS resolvers that provide normal resolution services and several tunnel servers for DNS tunneling communication. In VM A, a Selenium program simulates user browser operations by selecting keywords from 11 categories of the THUOCL corpus<sup>2</sup> as initial search seeds, including IT, finance, and place names. The system automatically iterates and expands the queries using related search terms recommended by the search engine, thereby generating richer access sequences that more closely resemble real user behavior. In VM B, a Scapy-based traffic sniffing program captures all DNS packets in real time and saves them as PCAP files. This node monitors all DNS traffic originating from VM A, realistically simulating the traffic environment at key network nodes. During DNS tunnel traffic acquisition, the network structure remains unchanged. VM A executes the DNS tunnel client program, while the corresponding server programs run on the tunnel servers, establishing complete DNS tunnel communication.

![](images/f6b5774873d3c402856c66999f6ab39b9a0bf0d0c0433de703ff479b58a1979b.jpg)  
Fig. 2. The framework of TridentDNS.

To address the shortage of heterogeneous DNS tunneling data in current public datasets, we develop HiveTunnel, a highly customizable testing system. Users can flexibly construct domain-based DNS tunnels by adjusting various parameters. The system supports both domain-relay mode and IP-direct mode and provides three operational roles, namely client, relay, and server. Users can also configure parameters such as packet sending ports, maximum length and number of domain labels, sending intervals, query types, and encoding methods to meet diverse experimental requirements. Its operational principle appears in Fig. 4.

![](images/ed0ea54c8497eb62ef8f8d2453f542ad669a5c87012a1f81abcf5df29ec89905.jpg)  
Fig. 4. Working Principle of HiveTunnel

The traffic acquisition module supports two modes. In offline mode, the system obtains traffic by importing PCAP files. When constructing benign traffic datasets, it identifies DNS packets using Wireshark dissectors via PyShark and discards non-DNS traffic. For DNS tunneling traffic datasets, it filters packets according to a predefined set of tunneling domains and discards legitimate DNS traffic, preserving solely the DNS packets associated with tunneling activities. The offline mode is illustrated in Fig. 5.

![](images/d81293beee61376b3c91f3b307b7a15ba2ce7ab5dddbf1c05dfa39154380fbed.jpg)  
Fig. 5. Offline Mode

In online mode, the system filters anomalous traffic through a multi-stage filtering mechanism. After feature extraction, each traffic packet first undergoes feature clustering using DBSCAN. The features used for clustering are listed in Table III. DBSCAN efficiently filters the majority of normal traffic, and packets not assigned to the primary clusters are then forwarded to the advanced analysis phase. In this phase, we combine VirusTotal and large language models (LLMs) to further analyze the remaining packets. Specifically, VirusTotal is employed to identify known malicious domains, while the LLM assesses potentially anomalous domains from two perspectives: structural characteristics and semantic information of the domain name. Ultimately, traffic deemed benign after passing the multi-stage filtering mechanism is stored in the training set following metadata extraction.

To enhance the efficiency of the multi-stage filtering mechanism, the system incorporates a blacklist/whitelist caching mechanism, where domains previously evaluated by VirusTotal or the LLM are cached in the corresponding lists. When the same domain reappears in subsequent traffic, it can be rapidly classified without repeated assessments. The blacklist and whitelist are time-sensitive and undergo periodic updates to ensure accuracy. Furthermore, the packet processing pipeline adopts an asynchronous architecture in which VirusTotal queries and LLM inference are executed concurrently. This design reduces latency and prevents expensive operations from blocking other packets. This online detection mechanism can also be extended to offline scenarios for dataset purification. The online mode is illustrated in Fig. 6.

TABLE III  
PACKET-DIMENSION FEATURES

<table><tr><td>Feature</td><td>Description</td></tr><tr><td>packet_size</td><td>Packet size</td></tr><tr><td>domain_length</td><td>Domain name length</td></tr><tr><td>domain_label_num</td><td>Number of domain name labels</td></tr><tr><td>domain_lowcase_ratio</td><td>Proportion of lowercase letters in the domain name</td></tr><tr><td>domain_entropy</td><td>Information entropy of the domain name</td></tr></table>

![](images/56b281d35813e3393ff8279543c102fb7b9343be696c6496c6a53abeac24b9f1.jpg)  
Fig. 6. Online Mode

## B. Traffic Parsing

The traffic parsing module receives packet-dimension metadata transmitted from the traffic acquisition module and performs session-dimension aggregation using the broad DNS session aggregation key (src ip, domain, $d s t \_ i p )$ . This process generates session-dimension metadata and associated features. Subsequently, the system further aggregates the sessiondimension metadata using the keys $( s r c \_ i p , d s t \_ i p )$ and (domain) respectively to extract flow-dimension features and domain-dimension features, as illustrated in Fig. 7.

The features used in this study appear in Table IV. In addition to the common features widely adopted in existing research, we design several new features based on the characteristics of heterogeneous DNS tunnels. We expect that features at the session dimension can effectively distinguish benign DNS traffic from conventional DNS tunnels, while features at the domain dimension and the flow dimension can further enhance the identification capability for heterogeneous

![](images/26ed326f6f3d0949abb55e7270569d7ea822a595d9cc10e41f6c902909ffe713.jpg)  
Fig. 7. Traffic Parsing Module

DNS tunnels. Among them, the flow dimension is effective for detecting IP-direct DNS tunnels and distributed DNS tunnels that use multiple domain names, whereas the domain dimension is effective for detecting distributed DNS tunnels that employ multiple server IPs.

1) Existing Features: We adopt eight features widely used in previous studies [5], [61] and apply them across the DNS session, domain, and flow dimensions. These features effectively capture the differences between benign DNS traffic and conventional DNS tunnels.

Macro traffic features: The DNS protocol was not designed for data transmission and is constrained by the domain name length limit in RFC1034 [1]. A single DNS packet carries only a limited amount of data. To achieve large-scale data transfer from compromised hosts to the Internet, DNS tunnels tend to continuously send large DNS query packets. Consequently, DNS tunnels exhibit significantly higher values than normal DNS sessions in duration, packet count, and query packet size, as shown in Eq. (1).

$$
\left\{ \begin{array}{l} T \approx \frac {I}{S} \\ I \approx I _ {p} \cdot N _ {p} \end{array} \right..\tag{1}
$$

Here, I represents the information volume transmitted in the session (bytes) and S denotes the throughput (bytes/second). $T$ is the session duration, which corresponds to feature $F _ { 1 }$ $N _ { p }$ is the packet count, which corresponds to feature $F _ { 2 } , I _ { p }$ is the payload per packet, which corresponds to feature $F _ { 3 }$ For a fixed information volume I, lower throughput $S$ in a DNS tunnel results in longer session duration $F _ { 1 }$ . Meanwhile, fewer packets usually imply larger individual packet sizes. Attackers typically trade off between the number of packets $F _ { 2 }$ and the transmission volume per packet $F _ { 3 }$ . High-throughput DNS tunnels prioritize transmission efficiency and therefore tend to show larger $F _ { 3 }$ , whereas low-throughput DNS tunnels emphasize stealthiness with smaller payload per packet but higher $F _ { 2 }$

TABLE IV  
MULTIDIMENSIONAL FEATURES EMPLOYED IN THIS PAPER

<table><tr><td rowspan="2">Feature ID</td><td rowspan="2">Feature Name</td><td rowspan="2">Description</td><td colspan="3">Applied Dimension</td><td rowspan="2">New Feature</td></tr><tr><td>Session-Dimension</td><td>Domain-Dimension</td><td>Flow-Dimension</td></tr><tr><td>F1</td><td>duration_time</td><td>Duration</td><td>✓</td><td>✓</td><td>✓</td><td>×</td></tr><tr><td>F2</td><td>packet_num</td><td>Number of packets</td><td>✓</td><td>✓</td><td>✓</td><td>×</td></tr><tr><td>F3</td><td>output_packet_size</td><td>Outgoing packet average size</td><td>✓</td><td>✓</td><td>✓</td><td>×</td></tr><tr><td>F4</td><td>domain_label_length</td><td>Average domain length</td><td>✓</td><td>✓</td><td>✓</td><td>×</td></tr><tr><td>F5</td><td>domain_label_num</td><td>Average number of domain labels</td><td>✓</td><td>✓</td><td>✓</td><td>×</td></tr><tr><td>F6</td><td>domain_lowcase_ratio</td><td>Ratio of lowercase characters in domain</td><td>✓</td><td>✓</td><td>✓</td><td>×</td></tr><tr><td>F7</td><td>domain_entropy</td><td>Average domain entropy</td><td>✓</td><td>✓</td><td>✓</td><td>×</td></tr><tr><td>F8</td><td>domain_ttl</td><td>Average domain TTL</td><td>✓</td><td>✓</td><td>✓</td><td>×</td></tr><tr><td>F9</td><td>query_score</td><td>Average query type score</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>F10</td><td>domain_diversity</td><td>Diversity of subdomains under a domain</td><td>×</td><td>✓</td><td>×</td><td>✓</td></tr><tr><td>F11</td><td>domain_num</td><td>Number of domains</td><td>×</td><td>×</td><td>✓</td><td>✓</td></tr><tr><td>F12</td><td>addr_relevance</td><td>Communication address relevance</td><td>×</td><td>×</td><td>✓</td><td>✓</td></tr></table>

We compute features $F _ { 1 } , F _ { 2 }$ , and $F _ { 3 }$ according to Eq. (2).

$$
\left\{ \begin{array}{l} F _ {1} ^ {(k)} = \max _ {p \in P _ {k}} t _ {p} - \min _ {p \in P _ {k}} t _ {p} \\ F _ {2} ^ {(k)} = | P _ {k} ^ {q u e r y} | \\ F _ {3} ^ {(k)} = \frac {\sum_ {p \in P _ {k} ^ {q u e r y}} | p |}{| P _ {k} ^ {q u e r y} |} \end{array} , \right.\tag{2}
$$

where $P _ { k }$ denotes the packet set corresponding to the $k \mathrm { - }$ th aggregation key, $t _ { p }$ is the timestamp of packet $p \in P _ { k }$ $\operatorname* { m a x } _ { p \in P _ { k } } t _ { p }$ is the timestamp of the latest packet in the session, and $\mathrm { m i n } _ { p \in P _ { k } } t _ { p }$ is the timestamp of the first packet. Thus, $F _ { 1 } ^ { ( k ) }$ represents the session duration under this aggregation key. $P _ { k } ^ { \bar { q } u e r y }$ denotes the query packet set for the k-th aggregation key, and $F _ { 2 } ^ { ( k ) }$ is the total number of query packets in the session under this key. |p| represents the byte size of packet $p ,$ and $F _ { 3 } ^ { ( k ) }$ is the average size of query packets in the session under this aggregation key.

Micro domain features: According to RFC1035 [2], a domain name consists of a series of labels. Each label has a maximum length of 63 bytes and the total domain name length must not exceed 255 bytes. To maximize the transmission capacity of a single DNS packet, high-throughput DNS tunnels tend to make full use of each label within the allowed limits [5]. Consequently, DNS tunnels generally exhibit significantly higher average label length and average number of labels than normal DNS sessions [35], as shown in Eq. (3).

$$
I _ {p} \approx L _ {p} \cdot N _ {l},\tag{3}
$$

where $L _ { p }$ represents the average label length in the domain name, which corresponds to feature $F _ { 4 } , N _ { l }$ denotes the average number of labels in the domain name, which corresponds to feature $F _ { 5 }$ . For a fixed information volume $I _ { p }$ transmitted in a single packet, shorter average label length $F _ { 4 }$ leads to a larger number of labels $F _ { 5 }$ . Attackers typically trade off between the average label length $F _ { 4 }$ and the number of labels $F _ { 5 }$

We compute features $F _ { 4 }$ and $F _ { 5 }$ according to Eq. (4).

$$
\left\{ \begin{array}{l} F _ {4} ^ {(k)} = \frac {\sum_ {p \in P _ {k} ^ {q u e r y}} \sum_ {l \in \text {labels} (p)} | l |}{\sum_ {p \in P _ {k} ^ {q u e r y}} \sum_ {l \in \text {labels} (p)} 1} \\ F _ {5} ^ {(k)} = \frac {\sum_ {p \in P _ {k} ^ {q u e r y}} \sum_ {l \in \text {labels} (p)} 1}{| P _ {k} ^ {q u e r y} |}, \end{array} \right.\tag{4}
$$

where labels(p) denotes the set of all domain labels in packet $p ,$ and |l| represents the length of label $l . \ F _ { 4 } ^ { ( k ) }$ is the average label length of the domain names under this aggregation key. $F _ { 5 } ^ { ( k ) }$ describes the average number of labels in the domain names under this aggregation key.

According to RFC 1035 [2], domain names must follow the LDH rule, which permits only ASCII letters (A-Z, az), digits (0-9), and hyphens (-). Although subsequent RFC documents have relaxed the legal character range for domain names to some extent by introducing Internationalized Domain Names (IDN), mainstream domain systems still rely on the LDH rule. In DNS tunnel communication scenarios, attackers tend to encode or encrypt plaintext data to evade detection [62]. This practice introduces characters that are rare or even violate RFC specifications in normal sessions and alters the character frequency [63]. Consequently, domain names generated by DNS tunnels often exhibit a significantly lower proportion of lowercase letters compared with benign DNS traffic. Information entropy serves as an important indicator for measuring the randomness and uncertainty of information. Due to the use of encoding or encryption on plaintext data, the resulting domain names display greater randomness and thus significantly higher entropy than those in benign DNS traffic [64]. Based on the above analysis, we compute features $F _ { 6 }$ and $F _ { 7 }$ using Eq. (5).

$$
\left\{ \begin{array}{l} F _ {6} ^ {(k)} = \frac {\sum_ {p \in P _ {k} ^ {q u e r y}} \sum_ {l \in \text {labels} (p)} | \{c \in l \mid c \in \mathcal {C} \} |}{\sum_ {p \in P _ {k} ^ {q u e r y}} \sum_ {l \in \text {labels} (p)} | l |} \\ F _ {7} ^ {(k)} = \frac {\sum_ {p \in P _ {k} ^ {q u e r y}} H (d (p))}{| P _ {k} ^ {q u e r y} |} \end{array} , \right.\tag{5}
$$

where c denotes a single character in label $l , \mathcal { C }$ is the lowercase character set $\{ a , b , c , \ldots , z \}$ , and $| \{ c \in l \ | \ c \in { \mathcal { C } } \} |$ represents the number of lowercase letters in label l. Thus, $\dot { F } _ { 6 } ^ { ( \dot { k } ) }$ is the average proportion of lowercase characters in domain names under this aggregation key. $d ( p )$ denotes the domain name string in packet $p ,$ and $H ( d ( p ) )$ is the information entropy of this domain name string, computed according to Eq. (6). ${ \bf \ddot { \cal F } } _ { 7 } ^ { ( k ) }$ represents the average information entropy of domain names under this aggregation key.

$$
H (d (p)) = - \sum_ {c \in \{x | x \in d (p) \}} q (c) \log_ {2} q (c),\tag{6}
$$

where the set $\{ x \mid x \in d ( p ) \}$ contains all characters appearing in the domain name string $d ( p )$ , and $q ( c )$ is the occurrence probability of character c in the domain name string.

To ensure that DNS query packets successfully reach the tunnel server, DNS tunnels tend to avoid hitting the local DNS cache [49]. Reducing TTL allows domain records to be quickly evicted from the cache. Consequently, the average TTL of DNS tunnels is often lower than that of normal DNS sessions. Because a single response packet may contain multiple Answer fields with different TTL values, we use the maximum TTL as the TTL of the response packet. The computation of feature $F _ { 8 }$ follows Eq. (7).

$$
F _ {8} ^ {(k)} = \frac {\sum_ {p \in P _ {k} ^ {\mathrm{resp}}} \max (T T L (p))}{| P _ {k} ^ {\mathrm{resp}} |},\tag{7}
$$

where $P _ { k } ^ { \mathrm { r e s p } }$ denotes the set of response packets under the k-th aggregation key, $T T L ( p )$ represents the TTL values in response packet $p ,$ and max $\because ( T T L ( p ) )$ is the maximum TTL in that response packet. Thus, $F _ { 8 } ^ { ( k ) }$ represents the average TTL of domain names under this aggregation key.

2) Proposed Features: Based on the operational mechanisms of various heterogeneous DNS tunnels, we design four novel features. These features effectively distinguish benign DNS traffic from heterogeneous DNS tunnels.

query score: Some DNS tunnels may exploit uncommon DNS query types for data transmission [5]. To quantify their anomaly degree, we design a dynamic scoring mechanism for query types. A higher score indicates that the query type is rarer in benign traffic. Consequently, the average query type score in DNS tunnel sessions is typically much higher than in normal sessions. In this paper, query types with an occurrence ratio below 1% are defined as rare types. For rare query types with few appearances, we ensure they receive sufficiently high scores. For common query types, the score should drop rapidly once their count exceeds a preset threshold. Our query type scoring method follows Eq. (8).

$$
\mathrm{score} ^ {(k)} = 1 - \frac {1}{1 + \alpha \cdot e ^ {- \beta (n _ {q} ^ {(k)} - \gamma)}},\tag{8}
$$

where ${ n } _ { q } ^ { ( k ) }$ represents the number of packets of query type $q$ under the k-th aggregation key, and $\alpha , ~ \beta , ~ \gamma$ are tunable parameters that control the shape of the scoring curve as the query count changes, as shown in Fig. 8. We conducted statistics on benign DNS traffic over the past 3 hours and found that the most frequent rare query type is NS, accounting for approximately 0.35%, as presented in Table V. To prevent the score of rare query types from decreasing due to time accumulation, we maintain a first-in-first-out (FIFO) queue to record and count query types. Considering hardware resource constraints, the queue length is set to 10000, meaning the method tracks the query types of the most recent 10000 packets under each aggregation key. On this basis, we set the parameters $\alpha , \beta ,$ and $\gamma$ to 0.008, 0.2, and 60, respectively. The corresponding threshold is approximately 35. When the count of a certain query type under an aggregation key exceeds 35, its type score begins to decrease significantly.

TABLE V STATISTICS OF DNS QUERY TYPES

<table><tr><td>Query Type</td><td>Count</td><td>Percentage</td><td>Description</td></tr><tr><td>HTTPS</td><td>55,273</td><td>46.94%</td><td>Retrieves HTTPS service parameters</td></tr><tr><td>A</td><td>51,525</td><td>43.76%</td><td>Requests IPv4 address</td></tr><tr><td>DS</td><td>5,469</td><td>4.65%</td><td>Secures subdomain delegation</td></tr><tr><td>AAAA</td><td>4,906</td><td>4.17%</td><td>Requests IPv6 address</td></tr><tr><td>NS</td><td>413</td><td>0.35%</td><td>Delegates zone authority</td></tr><tr><td>DNSKEY</td><td>134</td><td>0.11%</td><td>Provides DNSSEC public key</td></tr><tr><td>SRV</td><td>14</td><td>0.01%</td><td>Locates specific services</td></tr></table>

![](images/e59e672c704ac910d2b9199bf5e38760f1f6644bd15ea66508cdb35bc734346f.jpg)  
${ \mathrm { F i g } } .$ . 8. Score curve for DNS query types.

We compute feature $F _ { 9 }$ according to Eq. (9).

$$
F _ {9} ^ {(k)} = \frac {\sum_ {p \in P _ {k} ^ {q u e r y}} \mathbf {s c o r e} ^ {(k)} (t y p e (p))}{| P _ {k} ^ {q u e r y} |},\tag{9}
$$

where $t y p e ( p )$ denotes the query type of packet $p ,$ and $\operatorname { s c o r e } ^ { ( k ) } ( t y p e ( p ) )$ ) represents the score of that type under the k-th aggregation key. Thus, $F _ { 9 } ^ { ( k ) }$ is the average query type score under this aggregation key.

domain diversity: In normal DNS sessions, certain subdomains under the same primary domain are often reused multiple times due to recurring business requirements or user access patterns. In contrast, DNS tunnels rarely reuse the same subdomain, as attackers prefer unique subdomains for each query to transmit different payloads and bypass local DNS caches [49]. Consequently, DNS tunneling traffic typically exhibits significantly higher subdomain diversity than benign DNS traffic. Feature $F _ { 1 0 }$ is computed according to Eq. (10).

$$
F _ {1 0} ^ {(k)} = \frac {\left| \{d (p) \mid p \in P _ {k} ^ {q u e r y} \} \right|}{\left| P _ {k} ^ {q u e r y} \right|},\tag{10}
$$

where $\left| \{ d ( p ) \mid p \in P _ { k } ^ { q u e r y } \} \right|$ represents the number of distinct domain names under the aggregation key. This feature is primarily applied at the domain dimension, and $F _ { 1 0 } ^ { ( k ) }$ denotes the subdomain diversity ratio under a given primary domain. It is designed to distinguish wildcard domains with complex structures in benign traffic from domains generated by DNS tunnels.

domain num: In normal DNS flows, different applications or websites typically correspond to distinct primary domains, resulting in a relatively large number of primary domains.

In contrast, domain-relay DNS tunnels usually communicate using only a single or a limited number of primary domains. Consequently, the number of primary domains in normal DNS flows is generally higher than in domain-relay DNS tunnels. Feature $F _ { 1 1 }$ is computed according to Eq. (11).

$$
F _ {1 1} ^ {(k)} = \big | \{d _ {m a i n} (p) \mid p \in P _ {k} \} \big |,\tag{11}
$$

where $d _ { m a i n } ( p )$ denotes the primary domain of packet $p .$ This feature is primarily applied at the flow dimension, and $F _ { 1 1 } ^ { ( k ) }$ represents the number of primary domains within a given flow. It is designed to distinguish benign client-to-local-resolver DNS communication from compromised-host-to-tunnel-server communication in domain-relay DNS tunnels.

addr relevance: IP-direct DNS tunnels typically manifest as prolonged, packet-intensive communication between a compromised host and a tunnel server. Normal DNS sessions exhibit similar patterns between clients and local recursive resolvers. To distinguish legitimate DNS servers from DNS tunnel servers, we define a communication address relevance metric. The metric is set to 1 if the communicating parties belong to the same subnet or autonomous system, or if either party is a known public DNS resolver. Otherwise, it is set to 0. This feature is primarily applied at the flow dimension, and $F _ { 1 2 } ^ { ( k ) }$ represents the address relevance between the two parties in a given flow. Its computation follows Eq. (12).

$$
\left\{ \begin{array}{l} F _ {1 2} ^ {(k)} = R _ {m} \vee R _ {a s} \vee R _ {d} \\ R _ {m} = \bigvee_ {m \in M} \big ((\text { src\_ip } \& m) = (\text { dst\_ip } \& m) \big) \\ R _ {a s} = (\text { AS } (\text { src\_ip }) = \text { AS } (\text { dst\_ip })) \\ R _ {d} = (\text { src\_ip } \in D \lor \text { dst\_ip } \in D) \end{array} , \right.\tag{12}
$$

where M denotes the set of client subnet masks, $\lor _ { m \in M }$ denotes the logical OR operation, which evaluates all conditions corresponding to masks in the set M one by one, and the result is true as long as any one condition is true. $\operatorname { A S } ( \cdot )$ is the function that identifies the autonomous system to which an IP belongs. D represents the set of public DNS resolver IPs.

## C. DNS Tunnel Detection

Supervised learning requires labeled training data, which is labor-intensive and often insufficient for detecting zero-day attacks. To overcome these limitations, this work adopts an unsupervised learning approach. Specifically, relatively clean normal traffic is obtained from the traffic acquisition module, and feature data are extracted via the traffic parsing module. The extracted features are then used to train three independent Pre-Norm Self-Attention Autoencoders (SAAEs) [65], [66], [67] to perform anomaly detection across the session, domain, and flow dimensions. The DNS tunnel detection module is illustrated in Fig. 9.

The SAAE consists of an encoder and a decoder. The encoder maps the input to a latent representation and the decoder reconstructs the data from this latent representation. Since the SAAEs are trained exclusively on benign traffic, anomalous samples yield significantly higher reconstruction errors, which form the basis for anomaly detection. The incorporation of the self-attention mechanism enables the model to adaptively model inter-feature dependencies and capture higherorder interactions among input features. During the training phase, the three SAAEs are trained separately using sessiondimension, domain-dimension, and flow-dimension features from benign traffic by minimizing the error between input and reconstruction. In the testing phase, the reconstruction error of each SAAE constitutes a single-dimension anomaly score that indicates the degree of anomaly for the input data in that dimension. To integrate the outputs from the three detectors, the system employs the Mahalanobis distance algorithm [68]. This algorithm takes the anomaly scores from the three SAAEs as input and produces the final multidimensional anomaly score. During training, benign traffic features are fed into the trained SAAEs to obtain reconstruction errors, which are then used to estimate the parameters of the Mahalanobis distance.

In the proposed method, the anomaly score for each packet is derived from aggregated feature data computed under the aggregation keys associated with that packet across the DNS session, domain, and flow dimensions. Packets involved in low-throughput DNS tunneling may initially appear similar to benign traffic because only limited aggregated data are available. As additional packets associated with the same aggregation keys are observed, the corresponding aggregated features become increasingly distinguishable from those of benign traffic, which in turn leads to higher anomaly scores. We then apply the Local Outlier Factor (LOF) algorithm to evaluate each packet’s anomaly score against a benign reference set for anomaly detection. Notably, LOF itself is a static point-level detector and does not model temporal dynamics. The apparent progressive separation is caused by the increasing discriminative power of aggregated features rather than any temporal sensitivity of LOF. During each training phase, the benign reference set of anomaly scores is updated to reflect current network conditions and is used as the baseline for LOF evaluation in the testing phase.

To mitigate false positives caused by rare wildcard DNS queries and to prevent bias introduced by unbounded accumulation over time, we introduce a dynamic anomaly counting mechanism [69], [70]. This mechanism assigns an independent counter to each client IP, applies a decay to the accumulated anomaly count based on the number of processed packets associated with that IP, and triggers an alert only when the count reaches a predefined threshold. The update rule of this mechanism is given by Eq. (13).

$$
C _ {k} (t _ {k}) = \max \left(0, C _ {k} (t _ {k} - 1) + d _ {t _ {k}} - \mathbf {1} \{t _ {k} \bmod p _ {1} = 0 \}\right),\tag{13}
$$

where $t _ { k }$ denotes the index of instances associated with client IP k, i.e., the $t _ { k }$ -th packet observed for client IP k, starting from 1. $C _ { k } ( t _ { k } )$ denotes the cumulative anomaly counter after processing the $t _ { k } \mathrm { - t h }$ instance, with $C _ { k } ( 0 ) = 0 . \ d _ { t _ { k } } \in \{ 0 , 1 \}$ indicates the LOF anomaly decision for the $t _ { k }$ -th DNS packet associated with client IP k, where $d _ { t _ { k } } ~ = ~ 1$ represents an anomalous event. The indicator function 1{·} equals 1 when the condition holds and 0 otherwise. The decay interval and anomaly threshold are denoted by p<sub>1</sub> and p<sub>2</sub>, respectively.

![](images/014ca2ad909df1ce3142addc679b2ef52953ead32f25a5ef45e07d32724eed1d.jpg)  
Fig. 9. DNS Tunnel Detection Module

When the counter $C _ { k } ( t _ { k } )$ reaches the anomaly threshold $p _ { 2 } ,$ the detector triggers an anomaly alert.

In practical deployments, we recommend applying a percentile-based dynamic threshold to the anomaly scores produced by the session-dimension SAAE, using the resulting decision as a real-time alert to achieve fast and accurate detection of both normal traffic and conventional DNS tunnels. In contrast, heterogeneous DNS tunnels are detected by applying an LOF-based threshold to multidimensional anomaly scores. The process is illustrated in Fig. 10.

![](images/d3e8963bf975163921e021a4c280fd22ad2b5a6f336133685b74897f61e524d6.jpg)  
Fig. 10. Practical Deployment Strategy of TridentDNS

During both training and testing, the input data are preprocessed using Min-Max normalization [71]. The loss function employs a weighted combination of mean squared error (MSE) and mean absolute error (MAE), defined in Eq. (14).

$$
\mathcal {L} = \alpha \sum_ {f = 1} ^ {F} w _ {f} (x _ {f} - \hat {x} _ {f}) ^ {2} + (1 - \alpha) \sum_ {f = 1} ^ {F} w _ {f} | x _ {f} - \hat {x} _ {f} |,\tag{14}
$$

where $\alpha \in [ 0 , 1 ]$ controls the balance between the MSE and MAE terms in the loss function. $F$ denotes the number of features. $w _ { f }$ is the weight assigned to the f-th feature. $x _ { f }$ and $\hat { x } _ { f }$ denote the ground-truth and reconstructed values of the f-th feature, respectively.

## V. EVALUATION

In this section, we evaluate the performance of TridentDNS, focusing on its detection effectiveness and operational efficiency across diverse scenarios, including benign traffic, conventional DNS tunnels, and heterogeneous DNS tunnels.

## A. Experimental Setup

Our model is implemented in PyTorch 2.8.0 with CUDA 12.9 on Ubuntu and trained using the AdamW optimizer with a learning rate of 1e-6, weight decay of 0.0001, and a dropout rate of 0.05 for 100 epochs with a batch size of 512. The loss function and normalization method are as described in Section IV-C. The autoencoder components of the SAAE are configured according to the number of features in each dimension, with GELU used as the activation function. Specifically, the encoder layer sizes for the session, flow, and domain dimensions are [9, 7, 5, 3], [11, 9, 7, 5, 3], and [10, 8, 6, 4], respectively, with symmetric decoders. In addition, a multi-head attention module with an embedding dimension of 4 and 2 heads is incorporated. To further improve robustness, Gaussian noise with a standard deviation of 0.01 is injected into the latent representations during training. As training progresses, the loss decreases steadily and stabilizes after approximately 75 epochs, indicating reliable convergence.

1) Datasets and Evaluation Metrics: The datasets used in this study comprise internally collected DNS traffic and several publicly available datasets. Tables VI and VII summarize the composition and traffic statistics of the datasets, respectively. In Table VII, Sessions, Flows, and Domains are counted based on the aggregation keys (src ip, domain, dst ip), (src ip, dst ip), and (domain), respectively. These counts indicate the numbers of unique aggregation keys in each dimension, rather than the numbers of model input samples used for training or evaluation.

TABLE VI  
DATASET COMPOSITION

<table><tr><td>Dataset</td><td>Traffic Type</td><td>IDDT</td><td>LTDT</td></tr><tr><td rowspan="2">Training Set</td><td>Benign</td><td>N/A</td><td>N/A</td></tr><tr><td>Malicious</td><td>√</td><td>×</td></tr><tr><td>Benign Test Set</td><td>Benign</td><td>N/A</td><td>N/A</td></tr><tr><td>CDT Test Set</td><td>Malicious</td><td>√</td><td>×</td></tr><tr><td>HDT Test Set</td><td>Malicious</td><td>√</td><td>√</td></tr></table>

CDT and HDT denote Conventional and Heterogeneous DNS Tunnels,  
respectively; IDDT and LTDT denote IP-Direct and Low-throughput DNS Tunnels, respectively.

Training set: TridentDNS adopts an unsupervised learning paradigm and is therefore trained exclusively on benign traffic. Following the traffic acquisition environment and online-mode methodology described in Section IV-A, we collected benign traffic over five days at different time periods to construct the training set $D a t a s e t _ { t r a i n \_ o u r }$ . Because traffic generation and acquisition were conducted in a newly established and isolated virtual machine network, and the collected traffic was further processed through multi-stage filtering in online mode, all samples in $D a t a s e t _ { t r a i n \_ o u r }$ can be regarded as benign. Since not all baseline methods are unsupervised, we additionally use the publicly available dataset released by Gao et al. [50], which contains DNS tunneling traffic generated by multiple opensource tools. From this dataset, we extract traffic generated by Ozymandns, Cobalt Strike, and tcp-over-dns to construct the DNS tunnel training set $\textit { D a t a s e t } _ { t r a i n \_ g r a p h }$ . The training sets used in this study do not overlap with any of the subsequent test sets. Therefore, all DNS tunneling traffic in the test sets can be regarded as zero-day attacks.

TABLE VII  
DATASET TRAFFIC STATISTICS

<table><tr><td>Dataset</td><td>Traffic Type</td><td>Packets</td><td>Sessions</td><td>Flows</td><td>Domains</td></tr><tr><td rowspan="2">Training Set</td><td>Benign</td><td>4,914,727</td><td>68,898</td><td>7,658</td><td>8,997</td></tr><tr><td>Malicious</td><td>363,637</td><td>3</td><td>3</td><td>1</td></tr><tr><td>Benign Test Set</td><td>Benign</td><td>477,223</td><td>49,074</td><td>4,670</td><td>1,461</td></tr><tr><td>CDT Test Set</td><td>Malicious</td><td>739,275</td><td>6</td><td>6</td><td>2</td></tr><tr><td>HDT Test Set</td><td>Malicious</td><td>212,787</td><td>11,685</td><td>24</td><td>11,637</td></tr></table>

Benign DNS traffic test set: To evaluate the false positive performance, we select four datasets collected from diverse scenarios. $D a t a s e t _ { f p \_ o u r }$ is collected from the same network environment as $D a t a s e t _ { t r a i n \_ o u r } ,$ but at non-overlapping times. $D a t a s e t _ { f p \_ c i c }$ is derived from synthetic traffic generated in a controlled laboratory environment by Mahdavifar et al. [29], where queries are scripted to domains from popularity rankings and responses are recorded. $D a t a s e t _ { f p \_ c t u }$ comprises real-world traffic captured by Garcia et al. [72], with traffic collected directly at individual personal computers. Finally, $\textit { D a t a s e t } _ { f p \_ s c h o o l }$ consists of traffic collected from a real campus network by Singh et al. [73], with traffic captured at critical network nodes.

Conventional DNS tunnel test set: This test set evaluates the false negative rate and detection accuracy of the detection scheme on centralized high-throughput DNS tunnel traffic. It consists of two parts, namely $\it { D a t a s e t } _ { h i g h . }$ our and $D a t a s e t _ { h i g h \_ g r a p h }$ . The dataset $D a t a s e t _ { h i g h \_ o u r }$ is constructed using the acquisition environment described in Section IV-A and covers traffic from five open-source DNS tunneling tools<sup>3</sup>, which are DNS2TCP, DNSCAT2, DNSExfiltrator, Iodine, and TUNS. The dataset $D a t a s e t _ { h i g h \_ g r a p h }$ originates from the public dataset released by Gao et al. [50]. We select traffic generated by four tools for testing, namely DNSCAT2, DNSPOT, Iodine, and TUNS.

Heterogeneous DNS tunnel test set: Publicly available datasets for heterogeneous DNS tunneling traffic remain scarce. To address this limitation, we develop HiveTunnel and improve the conventional DNS tunneling tool DNS-Shell to generate and capture heterogeneous DNS tunneling traffic under a strict throughput constraint of no greater than 6.67 bytes per second. The constructed heterogeneous DNS tunnel dataset includes both centralized and distributed lowthroughput scenarios. Among them, the domain-relay DNS tunnel dataset is denoted as $D a t a s e t _ { d d \_ n \times m } .$ , and the IP-direct DNS tunnel dataset is denoted as $D a t a s e t _ { i d \_ n \times m }$ . Here, n represents the number of domains used and m represents the number of tunnel server IPs used. To simplify the experimental setup, this study uses only three authoritative name servers with different IPs and registers three DNS tunnel domains for constructing domain-relay DNS tunnels. In distributed IPdirect DNS tunnels, domains can be replaced more flexibly. Accordingly, we select candidate domains from the Tranco ranking list [74] and use N domains in the dataset.

The evaluation metrics are chosen according to the type of DNS traffic under consideration. For benign DNS traffic and conventional DNS tunnels, the primary metrics are the false positive rate $( F P R ) _ { \mathrm { { \scriptsize { ( F } } } }$ , false negative rate $( F N R )$ overall accuracy (Acc), and average detection latency (t<sub>mean</sub>, in microseconds), reflecting the model’s detection capability and efficiency for individual packets. For heterogeneous DNS tunnels, identifying tunnel traffic based solely on a single packet is difficult. Therefore, greater emphasis is placed on the time required for successful detection $( T _ { \mathrm { d e t e c t } } ,$ , in seconds) and the amount of information leakage $( I _ { \mathrm { l e a k } }$ , in KB).

2) Baseline Methods: To evaluate the performance of the proposed scheme, several representative baseline methods are selected for comparison. As summarized in Table VIII, these methods cover different feature sets and detector designs.

1) ibHH. Proposed by Ozery et al. [23], it uses Hyper-LogLog++ (HLL++) to estimate information volume transmitted across subdomains and detects potential anomalies via thresholding. Since it requires a manually configured domain whitelist, this paper provides the top one million domains from Tranco [74].

2) DNS-Images. Proposed by D’Angelo et al. [41], it converts features extracted from DNS query-response pairs into 2D images and performs traffic classification using a CNN combined with fully connected layers.

3) TF-SVM. Proposed by Liu et al. [53], it extracts timefrequency features from flows within time windows, and then applies an SVM-based classifier for low-throughput DNS tunnel detection. As suggested in the original paper, we set T1 = 300 and $T 2 = 1 0 .$

TABLE VIII  
COMPARISON OF FEATURES AND DETECTORS ACROSS METHODS

<table><tr><td rowspan="2">Approach</td><td colspan="2">Feature</td><td colspan="2">Detector</td></tr><tr><td>Granularity</td><td>Category</td><td>Type</td><td>Method</td></tr><tr><td>ibHH</td><td>Domain</td><td>Information volume</td><td>Threshold</td><td>HLL++</td></tr><tr><td>DNS-Images</td><td>N-Session</td><td>Statistical</td><td>DL</td><td>CNN</td></tr><tr><td>TF-SVM</td><td>Flow</td><td>Time-frequency</td><td>ML</td><td>SVM</td></tr><tr><td>TridentDNS</td><td>B-Session, Domain, Flow</td><td>Statistical, behavioral</td><td>DL</td><td>SAAE</td></tr></table>

N-Session and B-Session denote narrow DNS session and broad DNS session, respectively.

## B. Evaluation Results

1) Performance of Multi-Stage Filtering Mechanisms: To evaluate the effectiveness of the multi-stage filtering mechanism in online mode, we conduct experiments on the benign

DNS traffic test set $D a t a s e t _ { f p \_ o u r }$ and the conventional DNS tunnel test set $D a t a s e t _ { h i g h \_ g r a p h }$ . The results are shown in Fig. 11. On $D a t a s e t _ { f p _ { - } o u r } ,$ the multi-stage filtering mechanism achieves a detection accuracy of 1 while maintaining an average processing time per packet below 0.21 seconds. This demonstrates that the online mode introduces negligible impact on benign traffic, which dominates real-world DNS query volumes. On $D a t a s e t _ { h i g h \_ g r a p h }$ , the multi-stage filtering mechanism attains detection accuracy exceeding 99%. Although the average processing time increases slightly, the asynchronous design prevents individual packet processing from blocking the overall system. Notably, our method is an unsupervised anomaly detection system trained exclusively on benign traffic. It learns normal traffic patterns and identifies deviations, and therefore does not rely on frequent retraining to capture newly emerging attacks. In addition, the training phase is subject to less stringent real-time constraints and can therefore tolerate higher processing latency.

![](images/9fa16084e3fddea3f39185aabbef8c8ea069de7b3c1a7eeb9f98d0af340b9935.jpg)

![](images/21550663b1545b0036ebb221a7b143563ecc4da64026c2656efa1d13a82edbb9.jpg)  
(b) Average detection latency (s)  
Fig. 11. Performance of the multi-stage filtering mechanism on Datase $t _ { f p \_ o u r }$ and Datase $\cdot _ { h i g h \_ g r a p h }$

2) Performance of TridentDNS and Baselines: The proposed method and baseline schemes are evaluated on three test sets: the benign DNS traffic test set, the conventional DNS tunnel test set, and the heterogeneous DNS tunnel test set.

Impact on benign traffic. To assess the false positive rate of TridentDNS on benign traffic, we evaluate its performance on the benign DNS traffic test set and compare the results with those of baseline methods. Unsupervised detection schemes, which rely on anomaly detection principles, are trained exclusively on Dataset<sub>train our</sub>. In contrast, for the supervised methods DNS-Images [41] and TF-SVM [53], we construct the training set by sampling from $D a t a s e t _ { t r a i n \_ o u r }$ and the malicious training set $\textit { D a t a s e t } _ { t r a i n \_ g r a p h }$ with a benign-tomalicious ratio of 7:3, following their original experimental settings. The results are summarized in Table IX.

TABLE IX  
PERFORMANCE OF THE DETECTION SCHEMES ON THE BENIGN DNS TRAFFIC TEST SET

<table><tr><td rowspan="2">Method</td><td colspan="3"> $Dataset_{fp\_our}$ </td><td colspan="3"> $Dataset_{fp\_cic}$ </td><td colspan="3"> $Dataset_{fp\_ctu}$ </td></tr><tr><td>FPR</td><td>Acc</td><td> $t_{mean}$ </td><td>FPR</td><td>Acc</td><td> $t_{mean}$ </td><td>FPR</td><td>Acc</td><td> $t_{mean}$ </td></tr><tr><td>ibHH</td><td>0.0000</td><td>1.0000</td><td>2.13</td><td>0.0000</td><td>1.0000</td><td>2.94</td><td>0.0000</td><td>1.0000</td><td>3.23</td></tr><tr><td>DNS-Images</td><td>0.0012</td><td>0.9988</td><td>151.43</td><td>0.0000</td><td>1.0000</td><td>226.74</td><td>0.0000</td><td>1.0000</td><td>229.97</td></tr><tr><td>TF-SVM</td><td>0.0061</td><td>0.9939</td><td>0.94</td><td>0.0000</td><td>1.0000</td><td>1.46</td><td>0.0000</td><td>1.0000</td><td>10.75</td></tr><tr><td>TridentDNS</td><td>0.0001</td><td>0.9999</td><td>9.12</td><td>0.0000</td><td>1.0000</td><td>1.71</td><td>0.0000</td><td>1.0000</td><td>1.80</td></tr></table>

The experimental results on the benign DNS traffic test set show that TridentDNS and the baseline methods achieve detection accuracy exceeding 99% in most cases, with false positive rates below 1%. This demonstrates the high reliability of the proposed approach. It is worth noting that TF-SVM incurs a relatively high time cost on $D a t a s e t _ { f p \_ c t u }$ . We infer that this is because it performs detection based on time windows, while the DNS packets in $D a t a s e t _ { f p \_ c t u }$ are more sparsely distributed over time. Consequently, each time window tends to contain fewer DNS packets, making TF-SVM less efficient on this dataset.

Detection Performance on Conventional DNS Tunnels. To evaluate the detection performance of TridentDNS against conventional DNS tunnels, we test TridentDNS and baseline methods on the self-collected test set $D a t a s e t _ { h i g h \_ o u r }$ and the publicly available test set $D a t a s e t _ { h i g h \_ g r a p h }$ . The detection results are summarized in Table X.

The experimental results indicate that all methods achieve excellent performance with minor differences on both the conventional DNS tunnel test set $D a t a s e t _ { h i g h \_ o u r }$ and $D a t a s e t _ { h i g h \_ g r a p h }$ , with accuracy exceeding 99% across all cases. This indicates that existing research on conventional DNS tunnel detection has become relatively mature.

Detection Performance on Heterogeneous DNS Tunnels. To evaluate the detection performance of TridentDNS and baseline methods against heterogeneous DNS tunnels, we test all schemes on the heterogeneous DNS tunnel test set. The detection results are summarized in Table XI.

TABLE XI  
PERFORMANCE OF DETECTION SCHEMES ON HETEROGENEOUS DNS TUNNEL TEST SETS

<table><tr><td rowspan="2">Method</td><td rowspan="2">Dataset</td><td colspan="2">HiveTunnel</td><td colspan="2">DNS-Shell</td></tr><tr><td> $I_{\text{leak}}$ </td><td> $T_{\text{detect}}$ </td><td> $I_{\text{leak}}$ </td><td> $T_{\text{detect}}$ </td></tr><tr><td rowspan="8">ibHH</td><td> $Dataset_{dd\_1\times 1}$ </td><td>0.12</td><td>31.23</td><td>0.09</td><td>21.39</td></tr><tr><td> $Dataset_{dd\_1\times 3}$ </td><td>0.12</td><td>31.97</td><td>0.09</td><td>20.72</td></tr><tr><td> $Dataset_{dd\_3\times 1}$ </td><td>0.19</td><td>56.99</td><td>0.12</td><td>30.63</td></tr><tr><td> $Dataset_{dd\_3\times 3}$ </td><td>0.19</td><td>61.16</td><td>0.11</td><td>29.04</td></tr><tr><td> $Dataset_{id\_1\times 1}$ </td><td>0.19</td><td>49.10</td><td>0.16</td><td>32.17</td></tr><tr><td> $Dataset_{id\_1\times 3}$ </td><td>0.18</td><td>47.55</td><td>0.16</td><td>32.18</td></tr><tr><td> $Dataset_{id\_N\times 1}$ </td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td> $Dataset_{id\_N\times 3}$ </td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td rowspan="2">DNS-Images</td><td> $Dataset_{dd\_all}$ </td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td> $Dataset_{id\_all}$ </td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td rowspan="8">TF-SVM</td><td> $Dataset_{dd\_1\times 1}$ </td><td>1.10</td><td>300</td><td>1.16</td><td>300</td></tr><tr><td> $Dataset_{dd\_1\times 3}$ </td><td>1.07</td><td>300</td><td>1.15</td><td>300</td></tr><tr><td> $Dataset_{dd\_3\times 1}$ </td><td>1.01</td><td>300</td><td>1.19</td><td>300</td></tr><tr><td> $Dataset_{dd\_3\times 3}$ </td><td>0.95</td><td>300</td><td>1.18</td><td>300</td></tr><tr><td> $Dataset_{id\_1\times 1}$ </td><td>1.12</td><td>300</td><td>1.33</td><td>300</td></tr><tr><td> $Dataset_{id\_1\times 3}$ </td><td>16.73</td><td>4500</td><td>1.35</td><td>300</td></tr><tr><td> $Dataset_{id\_N\times 1}$ </td><td>1.90</td><td>600</td><td>1.38</td><td>300</td></tr><tr><td> $Dataset_{id\_N\times 3}$ </td><td>11.17</td><td>3600</td><td>1.35</td><td>300</td></tr><tr><td rowspan="8">TridentDNS</td><td> $Dataset_{dd\_1\times 1}$ </td><td>0.78</td><td>214.76</td><td>0.13</td><td>34.84</td></tr><tr><td> $Dataset_{dd\_1\times 3}$ </td><td>0.79</td><td>223.09</td><td>0.14</td><td>35.31</td></tr><tr><td> $Dataset_{dd\_3\times 1}$ </td><td>0.68</td><td>204.71</td><td>0.15</td><td>38.69</td></tr><tr><td> $Dataset_{dd\_3\times 3}$ </td><td>0.69</td><td>217.71</td><td>0.13</td><td>37.08</td></tr><tr><td> $Dataset_{id\_1\times 1}$ </td><td>1.59</td><td>429.75</td><td>0.29</td><td>60.19</td></tr><tr><td> $Dataset_{id\_1\times 3}$ </td><td>1.62</td><td>434.29</td><td>0.29</td><td>60.18</td></tr><tr><td> $Dataset_{id\_N\times 1}$ </td><td>1.27</td><td>388.41</td><td>0.64</td><td>141.46</td></tr><tr><td> $Dataset_{id\_N\times 3}$ </td><td>1.27</td><td>392.85</td><td>0.65</td><td>144.43</td></tr></table>

— indicates that the detection scheme fails to identify any attack.

The experimental results indicate that DNS-Images exhibits relatively weak performance in detecting heterogeneous DNS tunnels. DNS-Images targets narrow DNS sessions (i.e., queryresponse pairs), making long-term effective monitoring of heterogeneous DNS tunnels inherently challenging. In contrast, ibHH achieves strong performance in most cases, but it shows limited effectiveness against multi-domain IP-direct DNS tunnels. This limitation arises because ibHH targets individual domains, whereas multi-domain IP-direct DNS tunnels can arbitrarily switch domains to evade detection.

TABLE X  
PERFORMANCE OF THE DETECTION SCHEMES ON CONVENTIONAL DNS TUNNEL TEST SETS

<table><tr><td rowspan="2" colspan="2">Dataset</td><td colspan="3">ibHH</td><td colspan="3">DNS-Images</td><td colspan="3">TF-SVM</td><td colspan="3">TridentDNS</td></tr><tr><td>FNR</td><td>Acc</td><td> $t_{mean}$ </td><td>FNR</td><td>Acc</td><td> $t_{mean}$ </td><td>FNR</td><td>Acc</td><td> $t_{mean}$ </td><td>FNR</td><td>Acc</td><td> $t_{mean}$ </td></tr><tr><td rowspan="5"> $Dataset_{high\_our}$ </td><td>DNS2TCP</td><td>0.0000</td><td>1.0000</td><td>7.65</td><td>0.0000</td><td>1.0000</td><td>228.89</td><td>0.0000</td><td>1.0000</td><td>2.90</td><td>0.0000</td><td>1.0000</td><td>3.61</td></tr><tr><td>DNSCAT2</td><td>0.0000</td><td>1.0000</td><td>7.21</td><td>0.0000</td><td>1.0000</td><td>234.26</td><td>0.0000</td><td>1.0000</td><td>2.42</td><td>0.0000</td><td>1.0000</td><td>3.57</td></tr><tr><td>DNSExfiltrator</td><td>0.0000</td><td>1.0000</td><td>4.68</td><td>0.0000</td><td>1.0000</td><td>230.33</td><td>0.0000</td><td>1.0000</td><td>6.04</td><td>0.0000</td><td>1.0000</td><td>3.63</td></tr><tr><td>Iodine</td><td>0.0002</td><td>0.9998</td><td>6.98</td><td>0.0000</td><td>1.0000</td><td>234.90</td><td>0.0000</td><td>1.0000</td><td>5.10</td><td>0.0000</td><td>1.0000</td><td>3.66</td></tr><tr><td>TUNS</td><td>0.0000</td><td>1.0000</td><td>4.75</td><td>0.0000</td><td>1.0000</td><td>232.98</td><td>0.0000</td><td>1.0000</td><td>1.00</td><td>0.0000</td><td>1.0000</td><td>3.66</td></tr><tr><td rowspan="4"> $Dataset_{high\_graph}$ </td><td>DNSPOT</td><td>0.0000</td><td>1.0000</td><td>8.26</td><td>0.0000</td><td>1.0000</td><td>234.25</td><td>0.0000</td><td>1.0000</td><td>1.19</td><td>0.0000</td><td>1.0000</td><td>3.58</td></tr><tr><td>DNSCAT2</td><td>0.0000</td><td>1.0000</td><td>10.20</td><td>0.0000</td><td>1.0000</td><td>229.75</td><td>0.0000</td><td>1.0000</td><td>2.19</td><td>0.0000</td><td>1.0000</td><td>3.58</td></tr><tr><td>Iodine</td><td>0.0013</td><td>0.9987</td><td>6.79</td><td>0.0000</td><td>1.0000</td><td>230.10</td><td>0.0000</td><td>1.0000</td><td>5.28</td><td>0.0001</td><td>0.9999</td><td>3.71</td></tr><tr><td>TUNS</td><td>0.0000</td><td>1.0000</td><td>4.71</td><td>0.0002</td><td>0.9998</td><td>230.63</td><td>0.0000</td><td>1.0000</td><td>6.12</td><td>0.0001</td><td>0.9999</td><td>3.70</td></tr></table>

Further analysis shows that TF-SVM achieves broader detection coverage than the other baseline methods, mainly because it relies on the Flow dimension. However, this design also limits its effectiveness for multi-IP DNS tunnels, especially in IP-direct scenarios. In IP-direct DNS tunnels, clients communicate with the tunnel server without passing through recursive resolvers. As a result, the absence of such traffic aggregation points makes traffic toward multiple destination IPs less concentrated. Moreover, the use of fixed time windows further constrains the detection capability of TF-SVM for heterogeneous DNS tunnels. In contrast, TridentDNS integrates the Session, Domain, and Flow dimensions with a realtime aggregation scheme, enabling it to detect all evaluated heterogeneous DNS tunnels with lower information leakage and shorter detection time.

Additionally, we observe that DNS-Shell poses a lower threat compared to HiveTunnel. This is due to the inherent traffic patterns of DNS-Shell. In particular, the control characters in DNS-Shell occupy more than 9 bits, whereas those in HiveTunnel occupy no more than 7 bits. Given the same throughput constraints, longer control characters reduce the effective length available for transmitting information. Moreover, the domain name lengths and sending frequencies in DNS-Shell are highly repetitive, while HiveTunnel introduces random variations.

3) Ablation Study: We conducted ablation experiments on the multi-stage filtering mechanisms in the Traffic Acquisition module and the multidimensional fusion method in the DNS Tunnel Detection module.

Multi-Stage Filtering Mechanisms. To investigate the contribution of each component in the multi-stage filtering mechanism under online mode, we successively ablate the DBSCAN clustering, VirusTotal filtering, and large language model judgment modules. Experiments are conducted on $D a t a s e t _ { f p . }$ our and $D a t a s e t _ { h i g h \_ g r a p h }$ . The results are summarized in Fig. 12.

For benign traffic, ablating the DBSCAN component significantly increases average detection latency while slightly reducing detection accuracy. In contrast, ablating VirusTotal or the LLM module has only minor effects on both latency and accuracy. These results indicate that DBSCAN plays a more substantial role in efficiently processing benign traffic.

![](images/7e2343d3e3f56c891927e8bfbdd9421fc6f21e327f60ddc2969a6f839e5a8b80.jpg)  
Fig. 12. Ablation experiments on the multi-stage filtering mechanism in the online learning scheme. Here D denotes DBSCAN whereas V denotes VirusTotal and L denotes LLM.

For conventional DNS tunneling traffic, ablating the DB-SCAN component only slightly increases average latency while exerting minimal influence on detection accuracy. Since most malicious domains in $D a t a s e t _ { h i g h \_ g r a p h }$ are not recorded in VirusTotal, ablating VirusTotal has limited impact on both average latency and detection accuracy. In contrast, ablating the LLM module substantially reduces average latency but leads to a sharp decline in detection accuracy. These findings demonstrate that the LLM module plays a critical role in identifying malicious traffic, especially for threats not recorded in VirusTotal.

Multidimensional Fusion Method. To justify the choice of the fusion method, we conduct a comparative study among several representative approaches, including Isolation Forest, One-Class SVM, Autoencoder, and the Mahalanobis distance. Since the choice of the fusion method only affects the detection performance of heterogeneous DNS tunnels, we select the heterogeneous DNS tunnel datasets generated by HiveTunnel as the evaluation sets. The results are presented in Table XII.

TABLE XII  
PERFORMANCE COMPARISON OF MULTIDIMENSIONAL FUSION METHODS

<table><tr><td rowspan="2">Dataset</td><td colspan="2">Autoencoder</td><td colspan="2">Isolation Forest</td><td colspan="2">One-Class SVM</td><td colspan="2">Mahalanobis Distance</td></tr><tr><td> $I_{\text{leak}}$ </td><td> $T_{\text{detect}}$ </td><td> $I_{\text{leak}}$ </td><td> $T_{\text{detect}}$ </td><td> $I_{\text{leak}}$ </td><td> $T_{\text{detect}}$ </td><td> $I_{\text{leak}}$ </td><td> $T_{\text{detect}}$ </td></tr><tr><td> $Dataset_{dd\_1\times 1}$ </td><td>0.99</td><td>269.28</td><td>0.21</td><td>56.13</td><td>9.58</td><td>2617.70</td><td>0.78</td><td>214.76</td></tr><tr><td> $Dataset_{dd\_1\times 3}$ </td><td>0.97</td><td>272.55</td><td>0.24</td><td>67.25</td><td>9.26</td><td>2625.44</td><td>0.79</td><td>223.09</td></tr><tr><td> $Dataset_{dd\_3\times 1}$ </td><td>0.88</td><td>261.70</td><td>0.25</td><td>72.38</td><td>10.92</td><td>3259.22</td><td>0.68</td><td>204.71</td></tr><tr><td> $Dataset_{dd\_3\times 3}$ </td><td>0.56</td><td>175.99</td><td>0.26</td><td>84.90</td><td>—</td><td>—</td><td>0.69</td><td>217.71</td></tr><tr><td> $Dataset_{id\_1\times 1}$ </td><td>7.96</td><td>2153.97</td><td>—</td><td>—</td><td>20.10</td><td>5420.83</td><td>1.59</td><td>429.75</td></tr><tr><td> $Dataset_{id\_1\times 3}$ </td><td>14.35</td><td>3857.05</td><td>—</td><td>—</td><td>20.08</td><td>5399.79</td><td>1.62</td><td>434.29</td></tr><tr><td> $Dataset_{id\_N\times 1}$ </td><td>0.37</td><td>101.37</td><td>5.43</td><td>1797.48</td><td>0.63</td><td>184.31</td><td>1.27</td><td>388.41</td></tr><tr><td> $Dataset_{id\_N\times 3}$ </td><td>0.37</td><td>109.00</td><td>17.46</td><td>5647.67</td><td>0.70</td><td>208.73</td><td>1.27</td><td>392.85</td></tr></table>

indicates that the detection scheme fails to identify any attack.

Experimental results demonstrate that unsupervised anomaly detection methods, such as Isolation Forest and

One-Class SVM, which rely on spatial isolation or boundary modeling, perform poorly in detecting heterogeneous DNS tunnel traffic that closely resembles benign traffic. Further evaluation indicates that the Mahalanobis distance exhibits greater stability than the Autoencoder in low-dimensional scenarios. One possible explanation is that the Autoencoder, as a high-capacity nonlinear model, is better suited for high-dimensional representation learning. In low-dimensional scenarios, its excessive model capacity tends to result in overfitting on the training data. Based on these findings, we adopt the Mahalanobis distance as the final fusion approach.

Impact of Different Detection Dimensions. To justify the necessity of the detection dimensions used in TridentDNS, we conduct dimension-wise ablation experiments on different test sets. Since conventional DNS tunnels usually adopt centralized architectures with relatively concentrated traffic, a single dimension is often sufficient for effective detection. We therefore compare the detection capability of individual dimensions. In contrast, heterogeneous DNS tunnels may distribute tunneling traffic across multiple IPs or domains, thereby diluting anomalous signals along the corresponding detection dimension. We thus evaluate different dimension combinations. The ablation results are summarized in Tables XIII and XIV.

TABLE XIII  
DIMENSION-WISE ABLATION RESULTS ON BENIGN TRAFFIC AND CONVENTIONAL DNS TUNNELS

<table><tr><td rowspan="2">Dimension</td><td colspan="3"> $Dataset_{fp\_our}$ </td><td colspan="3"> $Dataset_{high\_our}$ </td><td colspan="3"> $Dataset_{high\_graph}$ </td></tr><tr><td>FPR</td><td>Acc</td><td> $t_{mean}$ </td><td>FNR</td><td>Acc</td><td> $t_{mean}$ </td><td>FNR</td><td>Acc</td><td> $t_{mean}$ </td></tr><tr><td>Session</td><td>0.0001</td><td>0.9999</td><td>8.97</td><td>0.0000</td><td>1.0000</td><td>3.1582</td><td>0.0001</td><td>0.9999</td><td>3.1566</td></tr><tr><td>Domain</td><td>0.0214</td><td>0.9786</td><td>9.93</td><td>0.0000</td><td>1.0000</td><td>3.1639</td><td>0.0001</td><td>0.9999</td><td>3.1622</td></tr><tr><td>Flow</td><td>0.0001</td><td>0.9999</td><td>9.95</td><td>0.0002</td><td>0.9998</td><td>3.1795</td><td>0.0016</td><td>0.9984</td><td>3.1801</td></tr></table>

TABLE XIV

DIMENSION-WISE ABLATION RESULTS ON HETEROGENEOUS DNS TUNNELS

<table><tr><td rowspan="2">Dataset</td><td colspan="2">D+F</td><td colspan="2">S+D</td><td colspan="2">S+F</td><td colspan="2">S+D+F</td></tr><tr><td> $I_{\text{leak}}$ </td><td> $T_{\text{detect}}$ </td><td> $I_{\text{leak}}$ </td><td> $T_{\text{detect}}$ </td><td> $I_{\text{leak}}$ </td><td> $T_{\text{detect}}$ </td><td> $I_{\text{leak}}$ </td><td> $T_{\text{detect}}$ </td></tr><tr><td> $Dataset_{dd\_1\times 1}$ </td><td>4.13</td><td>1133.81</td><td>3.90</td><td>1070.65</td><td>—</td><td>—</td><td>0.78</td><td>214.76</td></tr><tr><td> $Dataset_{dd\_1\times 3}$ </td><td>11.66</td><td>3322.71</td><td>7.59</td><td>2135.55</td><td>—</td><td>—</td><td>0.79</td><td>223.09</td></tr><tr><td> $Dataset_{dd\_3\times 1}$ </td><td>11.89</td><td>3556.78</td><td>12.28</td><td>3672.43</td><td>—</td><td>—</td><td>0.68</td><td>204.71</td></tr><tr><td> $Dataset_{dd\_3\times 3}$ </td><td>10.03</td><td>3133.04</td><td>9.96</td><td>3110.56</td><td>—</td><td>—</td><td>0.69</td><td>217.71</td></tr><tr><td> $Dataset_{id\_1\times 1}$ </td><td>8.32</td><td>2252.29</td><td>7.85</td><td>2126.31</td><td>—</td><td>—</td><td>1.59</td><td>429.75</td></tr><tr><td> $Dataset_{id\_1\times 3}$ </td><td>8.30</td><td>2234.57</td><td>7.88</td><td>2122.52</td><td>—</td><td>—</td><td>1.62</td><td>434.29</td></tr><tr><td> $Dataset_{id\_N\times 1}$ </td><td>1.41</td><td>431.38</td><td>17.87</td><td>5751.16</td><td>6.84</td><td>2222.56</td><td>1.27</td><td>388.41</td></tr><tr><td> $Dataset_{id\_N\times 3}$ </td><td>1.39</td><td>434.27</td><td>17.84</td><td>5767.43</td><td>20.15</td><td>6511.77</td><td>1.27</td><td>392.85</td></tr></table>

S, D, and F denote the Session, Domain, and Flow dimensions, respectively. — indicates that the detection scheme fails to identify any attack.

Table XIII shows that all three dimensions are effective for conventional DNS tunnel detection. Among them, the Session dimension achieves the best overall performance, indicating its strong capability in distinguishing conventional tunnel behaviors from benign traffic. We note that the Domain dimension produces a relatively higher false-positive rate on the benign traffic test set. This may be because benign complex domains, such as CDN domains, exhibit patterns that resemble conventional DNS tunnel traffic in the Domain dimension.

For heterogeneous DNS tunnels, we further observe that the Session and Flow dimensions provide limited effectiveness when the Domain dimension is absent. Although the Session dimension can contribute useful information to heterogeneous DNS tunnel detection, it is primarily designed to capture conventional DNS tunnel behaviors and thus does not include features specifically tailored to heterogeneous tunnels. The Flow dimension also shows limited effectiveness in this setting. Compared with a Domain aggregation key, a Flow aggregation key in benign traffic usually covers a larger and more diverse set of packets. As a result, heterogeneous tunnel packets need to be accumulated in larger quantities before their anomalous patterns become evident in the Flow dimension, which may exceed the 10,000-packet evaluation window used in our tests. In contrast, the inclusion of the Domain dimension substantially improves detection performance in most heterogeneous DNS tunnel cases, as it enables anomalous behaviors to be captured with fewer accumulated tunnel packets. It is worth noting that the Flow dimension provides an important contribution on the $D a t a s e t _ { i d \_ N \times a l l }$ test sets, mainly due to the introduction of the domain num feature.

4) Real-World and Class-Imbalanced Evaluation: To evaluate the false positive rate of TridentDNS in real-world and enterprise-scale scenarios, we use the traffic dataset $\textit { D a t a s e t } _ { f p \_ s c h o o l }$ , captured in a real campus network environment by Singh et al. [73], to conduct false positive testing. This dataset includes traffic from over 4,000 active users during peak periods, providing a realistic approximation of enterprise-scale traffic conditions. Following the near-realistic class imbalance ratio of 994:6 proposed by Lambion et al. [57], we then sample 99,400 instances from $\textit { D a t a s e t } _ { f p \_ s c h o o l }$ and 600 instances from each subclass of the conventional and heterogeneous DNS tunnel test sets. These samples are combined separately, ensuring that they are evenly distributed, to form the evaluation datasets, where the conventional DNS tunnel samples are drawn from $D a t a s e t _ { h i g h \_ o u r }$ and the heterogeneous DNS tunnel samples are generated by HiveTunnel. The injected anomalous traffic retains its original aggregation keys. The results are presented in Fig. 13.

![](images/e7915f52485cc6182e67795dc527a6ccff76871690bca514ff358ce1ae84d30e.jpg)  
(a) Metrics for CDT Detection

![](images/1dcfddef3688334828b33ac5f3433070d161272fbbb3138e8e8087b32c70e272.jpg)  
(b) $I _ { \mathrm { l e a k } }$ for HDT Detection  
Fig. 13. Detection performance in real-world network environments. CDT and HDT denote conventional and heterogeneous DNS tunnels, respectively.

The evaluation results demonstrate that TridentDNS achieves an accuracy of 99.59% and a false positive rate (FPR) of 0.41% on the benign traffic dataset $D a t a s e t _ { f p _ { - } }$ <sub>school</sub>, indicating strong practicality. On the conventional DNS tunnel test set, TridentDNS achieves consistently high performance across all subsets, with a precision of 94.49%, an FPR of 0.04%, and an F1-score of 97.17%. The recall reaches 100%, indicating that all conventional DNS tunnel traffic is correctly detected. On the heterogeneous DNS tunnel test set, TridentDNS maintains excellent detection performance. Because the injected anomalous traffic has different aggregation keys, it is treated as traffic from newly introduced devices. As a result, the detection of this anomalous traffic is not interfered

with by normal traffic.

5) Time and Space Efficiency Analysis: To assess the time and space efficiency of TridentDNS in real-world settings, we evaluate various detection methods on the dataset $D a t a s e t _ { h i g h \_ o u r } .$ . We select peak memory usage (PMU) and average processing time per packet (APT) as the primary metrics. The detailed results are summarized in Fig. 14. Note that APT differs from the previously defined average detection latency $t _ { m e a n } .$ Specifically, APT measures the average time from packet ingestion to completion of detection, whereas $t _ { m e a n }$ captures only the model’s inference latency.

![](images/bafdb2b4f508a08c0cef23d92e6282500b9661c7c3942cc357ee741df9785005.jpg)  
(a) Average Processing Time (µs)

![](images/7e5520c77d8571aba803e482fcbc9b713333cf5e96b4311d1e8e7962de84f7ea.jpg)  
(b) Peak Memory Usage (MB)  
Fig. 14. Time and Space Overhead of the Detection Schemes.

The experimental results reveal significant differences in time and space overhead among the detection schemes. In terms of time overhead, ibHH achieves the shortest APT due to its lightweight threshold-based detection mechanism. In contrast, TF-SVM records the highest APT of 826.69 µs per packet, mainly because of its time-window-based feature computation. DNS-Images also incurs a relatively high APT of 227.24 µs per packet, owing to its complex CNN architecture, which imposes a greater computational burden. TridentDNS achieves an APT of 123.77 µs per packet, with the primary cost arising from the traffic parsing module. To further reduce the time overhead of TridentDNS, multi-threading can be employed when sufficient memory is available, enabling parallel processing between the flow and domain dimensions.

Regarding space overhead, ibHH achieves the lowest PMU, while DNS-Images incurs the highest PMU at 1436.77 MB due to the substantial demands of its complex CNN model. TF-SVM consumes 565.01 MB. TridentDNS falls within an intermediate range, with a PMU of 1206.55 MB, primarily due to the use of PyTorch.

## VI. DISCUSSION

The experimental results demonstrate that TridentDNS effectively detects various types of DNS tunneling attacks that use domain names as the information carrier, while maintaining a low false positive rate. Despite these promising results, the framework has some limitations that merit discussion.

First, the multi-stage filtering mechanism relies on external APIs for both VirusTotal and the LLM. While this contributes to strong detection performance, it introduces practical deployment challenges, including service availability, API rate limits, query latency, and operational costs. To reduce external dependencies, these APIs could be replaced by an offline malicious URL database and a locally deployed LLM. However, offline databases may suffer from stale threat intelligence, reducing effectiveness against zero-day tunneling attacks. Similarly, local general-purpose LLM deployment involves tradeoffs between detection capability and resource consumption: lightweight models often achieve lower detection accuracy, whereas large-scale models require substantial computational resources. Future work may focus on training lightweight LLMs specialized for DNS tunneling detection, sacrificing generality to achieve accurate, fast, and efficient detection.

Second, TridentDNS primarily focuses on determining the presence of DNS tunneling, while its capability to distinguish between legitimate and malicious tunneling activities remains limited. Since DNS tunneling by benign applications is relatively rare, we adopt a domain whitelist strategy to allow known legitimate tunneling domains. This approach still has limitations: multi-domain IP-direct tunneling may bypass the whitelist by masquerading as legitimate domains to exfiltrate data. Future work could focus on verifying whether queries for legitimate domains are directed to their intended servers.

## VII. CONCLUSION

This paper proposes TridentDNS, a heterogeneous DNS tunnel detection framework based on multidimensional features. It integrates a self-purifying online learning mechanism with a “Trident” multidimensional feature fusion detection paradigm. Experiments demonstrate that TridentDNS maintains a false positive rate below 1% on benign traffic while achieving near 100% single-packet detection accuracy for conventional DNS tunnels. Moreover, it effectively detects various types of heterogeneous DNS tunnels, exhibiting low memory footprint and real-time detection capability. To support evaluation, we developed HiveTunnel, a highly customizable tool that pro vides a practical means for generating heterogeneous DNS tunneling traffic. Future work will mainly focus on two directions. First, we will explore training lightweight LLMs specialized for DNS tunneling detection, sacrificing generality to achieve accurate, fast, and efficient detection. Second, we will investigate methods for verifying whether queries for legitimate domains are directed to their intended servers.

## REFERENCES

[1] P. Mockapetris, “Domain names – concepts and facilities,” document RFC 1034, Nov. 1987. [Online]. Available: https://www.rfc-editor.org/ info/rfc1034

[2] P. Mockapetris, “Domain names – implementation and specification,” document RFC 1035, Nov. 1987. [Online]. Available: https://www.rfceditor.org/info/rfc1035

[3] C. Patsakis, F. Casino, and V. Katos, “Encrypted and covert DNS queries for botnets: Challenges and countermeasures,” Comput. Secur., vol. 88, p. 101614, 2020.

[4] M. Lyu, H. H. Gharakheili, C. Russell, and V. Sivaraman, “Enterprise DNS asset mapping and cyber-health tracking via passive traffic analysis,” IEEE Trans. Netw. Serv. Manag., vol. 20, no. 3, pp. 3699–3716, 2022.

[5] Y. Wang, A. Zhou, S. Liao, R. Zheng, R. Hu, and L. Zhang, “A comprehensive survey on DNS tunnel detection,” Comput. Netw., vol. 197, p. 108322, 2021.

[6] Z. Yang, Y. Hongzhi, L. Lingzi, H. Cheng, and Z. Tao, “Detecting DNS tunnels using session behavior and random forest method,” in Proc. 2020 IEEE 5th Int. Conf. Data Sci. Cyberspace (DSC), 2020, pp. 45–52.

[7] S. Wang, L. Sun, S. Qin, W. Li, and W. Liu, “KRTunnel: DNS channel detector for mobile devices,” Comput. Secur., vol. 120, p. 102818, 2022.

[8] J. Zhang, L. Yang, S. Yu, and J. Ma, “A DNS tunneling detection method based on deep learning models to prevent data exfiltration,” in Proc. Int. Conf. Netw. Syst. Secur., 2019, pp. 520–535.

[9] S. Adiwal, B. Rajendran, S. D. Sudarsan et al., “DNS intrusion detection (DID)—a Snort-based solution to detect DNS amplification and DNS tunneling attacks,” Franklin Open, vol. 2, p. 100010, 2023.

[10] A. Lal, A. Prasad, A. Kumar, and S. Kumar, “DNS-tunnet: A hybrid approach for DNS tunneling detection,” in Proc. 2022 4th Int. Conf. Adv. Comput. Technol., Inf. Sci. Commun. (CTISC), 2022, pp. 1–6.

[11] Infoblox, “2024 DNS threat landscape,” Infoblox Blog. [Online]. Available: https://blogs.infoblox.com/threat- intelligence/2024- dns- threatlandscape/, Accessed: Sep. 8, 2025.

[12] M. Zuckerman, “DNS early detection: Breaking the BlackCat ransomware kill chain,” Infoblox Blog. [Online]. Available: https://blogs. infoblox . com / threat - intelligence / dns - early - detection - breaking - the - blackcat-ransomware-kill-chain/, Accessed: Sep. 8, 2025.

[13] R. Duan and D. Liu, “Understanding DNS tunneling traffic in the wild,” Unit 42. [Online]. Available: https://unit42.paloaltonetworks.com/dnstunneling-in-the-wild/, Accessed: Sep. 8, 2025.

[14] Infoblox, “Decoy Dog: Unveiling a sophisticated DNS-based malware toolkit,” Infoblox Report. [Online]. Available: https://insights.infoblox. com/resources-report/infoblox-report-decoy-dog-is-no-ordinary-pupydistinguishing-malware-via-dns, Accessed: Sep. 8, 2025.

[15] M. Lyu, H. H. Gharakheili, and V. Sivaraman, “PEDDA: Practical and effective detection of distributed attacks on enterprise networks via progressive multi-stage inference,” Comput. Netw., vol. 233, p. 109873, 2023.

[16] Y. Chen and X. Li, “A high accuracy DNS tunnel detection method without feature engineering,” in Proc. 2020 16th Int. Conf. Comput. Intell. Secur. (CIS), 2020, pp. 374–377.

[17] M. A. Altuncu, F. K. Gulagiz, H. Ozcan, O. F. Bayir, A. Gezgin, A. Niyazov, M. A. Cavuslu, and S. Sahin, “Deep learning based DNS tunneling detection and blocking system,” Adv. Electr. Comput. Eng., vol. 21, no. 3, pp. 39–48, 2021.

[18] J. Hou, X. Li, K. Zhao, W. Liang, Y. Li, T. Jiang, and Z. Liu, “A survey of DNS tunnel detection,” in Proc. 2022 7th Int. Conf. Signal Image Process. (ICSIP), 2022, pp. 338–342.

[19] S. C. Hoi, D. Sahoo, J. Lu, and P. Zhao, “Online learning: A comprehensive survey,” Neurocomputing, vol. 459, pp. 249–289, 2021.

[20] S. Yang, X. Zheng, J. Li, J. Xu, X. Zhang, and E. C. H. Ngai, “Selfsupervised adaptation method to concept drift for network intrusion detection,” IEEE Trans. Dependable Secure Comput., vol. 22, no. 6, pp. 7632–7646, 2025.

[21] M. Luo, Q. Wang, Y. Yao, X. Wang, P. Yang, and Z. Jiang, “Towards comprehensive detection of DNS tunnels,” in Proc. 2020 IEEE Symp. Comput. Commun. (ISCC), 2020, pp. 1–7.

[22] Y. Mirsky, T. Doitshman, Y. Elovici, and A. Shabtai, “Kitsune: an ensemble of autoencoders for online network intrusion detection,” arXiv preprint arXiv:1802.09089, 2018.

[23] Y. Ozery, A. Nadler, and A. Shabtai, “Information based heavy hitters for real-time DNS data exfiltration detection,” in Proc. Netw. Distrib. Syst. Secur. Symp., 2024, pp. 1–15.

[24] Y. Siriwardhana, P. Porambage, M. Liyanage, S. Marchal, and M. Ylianttila, “Shield - secure aggregation against poisoning in hierarchical federated learning,” IEEE Trans. Dependable Secure Comput., vol. 22, no. 2, pp. 1845–1863, 2025.

[25] K. P. Rao, S. H. Nayak, and G. Poornalatha, “A comprehensive review of DNS tunneling detection methods in cybersecurity,” IAENG Int. J. Comput. Sci., vol. 53, no. 3, p. 947, 2026.

[26] G. Ruiling, D. Jiawen, C. Xiang, and S. Shouyou, “A DNS-based data exfiltration traffic detection method for unknown samples,” in Proc. 2022 IEEE 7th Int. Conf. Data Sci. Cyberspace (DSC), 2022, pp. 191–198.

[27] T. Holz, C. Gorecki, K. Rieck, and F. C. Freiling, “Measuring and detecting fast-flux service networks,” in NDSS, 2008.

[28] K. Wu, Y. Zhang, and T. Yin, “FTPB: a three-stage DNS tunnel detection method based on character feature extraction,” in Proc. 2020 IEEE 19th Int. Conf. Trust, Secur. Privacy Comput. Commun. (TrustCom), 2020, pp. 250–258.

[29] S. Mahdavifar, A. Hanafy Salem, P. Victor, A. H. Razavi, M. Garzon, N. Hellberg, and A. H. Lashkari, “Lightweight hybrid detection of data exfiltration using DNS based on machine learning,” in Proc. 2021 11th Int. Conf. Commun. Netw. Secur., 2021, pp. 80–86.

[30] J. Ahmed, H. H. Gharakheili, Q. Raza, C. Russell, and V. Sivaraman, “Monitoring enterprise DNS queries for detecting data exfiltration from internal hosts,” IEEE Trans. Netw. Serv. Manag., vol. 17, no. 1, pp. 265–279, 2019.

[31] O. Abualghanam, H. Alazzam, B. Elshqeirat, M. Qatawneh, and M. A. Almaiah, “Real-time detection system for data exfiltration over DNS tunneling using machine learning,” Electronics, vol. 12, no. 6, p. 1467, 2023.

[32] K. Wu, Y. Zhang, and T. Yin, “TDAE: Autoencoder-based automatic feature learning method for the detection of DNS tunnel,” in Proc. IEEE Int. Conf. Commun. (ICC), 2020, pp. 1–7.

[33] D. Liu, R. Duan, and J. Wang, “Resolution without dissent: In-path perquery sanitization to defeat surreptitious communication over DNS,” in Proc. 2025 IEEE Symp. Secur. Privacy (SP), 2025, pp. 1808–1824.

[34] J. Liang, S. Wang, S. Zhao, and S. Chen, “FECC: DNS tunnel detection model based on CNN and clustering,” Comput. Secur., vol. 128, p. 103132, 2023.

[35] S. Kuang, W. Wang, Y. Ye, and L. Peng, “HHBT: DNS tunneling detection via hybrid hierarchical bidirectional transformer,” Comput. Netw., p. 111919, 2025.

[36] V. Paxson, M. Christodorescu, M. Javed, J. Rao, R. Sailer, D. L. Schales, M. Stoecklin, K. Thomas, W. Venema, and N. Weaver, “Practical comprehensive bounds on surreptitious communication over DNS,” in 22nd USENIX Security Symposium (USENIX Security 13), 2013, pp. 17–32.

[37] M. Aiello, M. Mongelli, and G. Papaleo, “Basic classifiers for DNS tunneling detection,” in Proc. 2013 IEEE Symp. Comput. Commun. (ISCC), 2013, pp. 880–885.

[38] S. Shafieian, D. Smith, and M. Zulkernine, “Detecting DNS tunneling using ensemble learning,” in Proc. Int. Conf. Netw. Syst. Secur., 2017, pp. 112–127.

[39] G. Duan, Q. Li, Z. Zhang, D. Zhao, G. Xie, Y. Yang, Z. Yuan, Y. Jiang, and M. Xu, “DNSGuard: In-network defense against DNS attacks,” IEEE Trans. Dependable Secure Comput., vol. 22, no. 1, pp. 597–613, 2024.

[40] Y. Tu, S. Liu, and Q. Sun, “DNS tunnelling detection by fusing encoding feature and behavioral feature,” Comput. Secur., vol. 132, p. 103357, 2023.

[41] G. D’Angelo, A. Castiglione, and F. Palmieri, “DNS tunnels detection via DNS-images,” Inf. Process. Manag., vol. 59, no. 3, p. 102930, 2022.

[42] G. De Bernardi, G. B. Gaggero, F. Patrone, S. Zappatore, M. Marchese, and M. Mongelli, “Rule-Based eXplainable Autoencoder for DNS tunneling detection,” Computers, vol. 14, no. 9, p. 375, 2025.

[43] E. Joback, L. Shing, K. Alperin, S. R. Gomez, S. Jorgensen, and G. Elkin, “A statistical approach to detecting low-throughput exfiltration through the domain name system protocol,” in Proc. 2020 Workshop on DYnamic and Novel Adv. Mach. Learn. and Intell. Cyber Secur., 2020, pp. 1–10.

[44] A. Nadler, A. Aminov, and A. Shabtai, “Detection of malicious and low throughput data exfiltration over the DNS protocol,” Comput. Secur., vol. 80, pp. 36–53, 2019.

[45] J. Liu, S. Li, Y. Zhang, J. Xiao, P. Chang, and C. Peng, “Detecting DNS tunnel through binary-classification based on behavior features,” in Proc. 2017 IEEE Trustcom/BigDataSE/ICESS, 2017, pp. 339–346.

[46] Y. Liu and X. Gou, “Research on application of feature analysis method in DNS tunnel detection,” in J. Phys.: Conf. Ser., vol. 1575, no. 1. IOP Publishing, 2020, p. 012069.

[47] S. Marchal, J. Franc¸ois, C. Wagner, R. State, A. Dulaunoy, T. Engel, and O. Festor, “DNSSM: A large scale passive DNS security monitoring framework,” in 2012 IEEE Netw. Oper. Manag. Symp., 2012, pp. 988– 993.

[48] F. Zou, Y. Ren, J. Zhu, and J. Tang, “Detecting data leakage in DNS traffic based on time series anomaly detection,” in Proc. 2021 IEEE 23rd Int. Conf. High Performance Computing & Communications; 7th Int. Conf. Data Science & Systems; 19th Int. Conf. Smart City; 7th Int. Conf. Dependability in Sensor, Cloud & Big Data Systems & Application (HPCC/DSS/SmartCity/DependSys), 2021, pp. 503–510.

[49] N. Ishikura, D. Kondo, V. Vassiliades, I. Iordanov, and H. Tode, “DNS tunneling detection by cache-property-aware features,” IEEE Trans. Netw. Serv. Manag., vol. 18, no. 2, pp. 1203–1217, 2021.

[50] G. Gao, W. Niu, J. Gong, D. Gu, S. Li, M. Zhang, and X. Zhang, “GraphTunnel: Robust DNS tunnel detection based on DNS recursive resolution graph,” IEEE Trans. Inf. Forensics Security, vol. 19, pp. 7705– 7719, 2024.

[51] H. Bai, W. Liu, G. Liu, Y. Dai, and S. Huang, “Application behavior identification in DNS tunnels based on spatial-temporal information,” IEEE Access, vol. 9, pp. 80 639–80 653, 2021.

[52] T. Q. Nguyen, R. Laborde, A. Benzekri, A. Oglaza, and M. Mounsif, “AutoRoC-DBSCAN: automatic tuning of DBSCAN to detect malicious DNS tunnels,” Ann. Telecommun., vol. 80, no. 3, pp. 227–249, 2025.

[53] X. Liu, W. Mao, A. Wang, Z. Li, H. Xue, Y. Zhang, J. Lin, X. Yang, Z. Chen, and B. Sun, “DNS tunnel detection for low throughput data exfiltration via time-frequency domain analysis,” in Proc. IEEE Int. Conf. Commun. (ICC), 2023, pp. 2331–2337.

[54] D. Willems, K. Kohls, B. van der Kamp, and H. Vranken, “Data exfiltration detection on network metadata with autoencoders,” Electronics, vol. 12, no. 12, p. 2584, 2023.

[55] M. Sammour, M. F. I. Othman, A. Hassan, O. Bhais, and M. S. Talib, “Advanced DNS tunneling detection: a hybrid reinforcement learning and metaheuristic approach,” Front. Comput. Sci., vol. 7, p. 1728980, 2025.

[56] K. Jiang and F. Wang, “Detecting DNS tunnel based on multidimensional analysis,” in Proc. 2020 5th Int. Conf. Mech., Control Comput. Eng. (ICMCCE), 2020, pp. 272–275.

[57] D. Lambion, M. Josten, F. Olumofin, and M. De Cock, “Malicious DNS tunneling detection in real-traffic DNS data,” in Proc. 2020 IEEE Int. Conf. Big Data (Big Data), 2020, pp. 5736–5738.

[58] P. E. Hoffman, A. Sullivan, and K. Fujiwara, “DNS Terminology,” document RFC 8499, Jan. 2019. [Online]. Available: https://www.rfceditor.org/info/rfc8499

[59] Y. Afek, A. Bremler-Barr, E. Cohen, S. L. Feibish, and M. Shagam, “Efficient distinct heavy hitters for DNS DDoS attack detection,” arXiv preprint arXiv:1612.02636, 2016.

[60] M. Lyu, H. H. Gharakheili, and V. Sivaraman, “Classifying and tracking enterprise assets via dual-grained network behavioral analysis,” Comput. Netw., vol. 218, p. 109387, 2022.

[61] H. Yan, X. Li, W. Zhang, R. Wang, H. Li, X. Zhao, F. Li, and X. Lin, “Automatic evasion of machine learning-based network intrusion detection systems,” IEEE Trans. Dependable Secure Comput., vol. 21, no. 1, pp. 153–167, 2024.

[62] A. Almadhor, S. Alsubai, M. Mohamed Zaidi, N. Kryvinska, A. Al Hejaili, and S. Abbas, “An intelligent feature engineering-driven hybrid framework for adversarial domain name system tunneling detection,” Adv. Intell. Syst., p. e202501311, 2026.

[63] K. Born and D. Gustafson, “Detecting DNS tunnels using character frequency analysis,” arXiv preprint arXiv:1004.4358, 2010.

[64] I. Homem, P. Papapetrou, and S. Dosis, “Information-entropy-based DNS tunnel prediction,” in Proc. IFIP Int. Conf. Digit. Forensics, 2018, pp. 127–140.

[65] R. Xiong, Y. Yang, D. He, K. Zheng, S. Zheng, C. Xing, H. Zhang, Y. Lan, L. Wang, and T. Liu, “On layer normalization in the transformer architecture,” in Int. Conf. Mach. Learn., 2020, pp. 10 524–10 533.

[66] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, “Attention is all you need,” Adv. Neural Inf. Process. Syst., vol. 30, 2017.

[67] G. E. Hinton and R. Zemel, “Autoencoders, minimum description length and Helmholtz free energy,” Adv. Neural Inf. Process. Syst., vol. 6, 1993.

[68] P. C. Mahalanobis, “On the generalized distance in statistics,” Proc. Natl. Inst. Sci. India, vol. 2, no. 1, pp. 49–55, 1936.

[69] E. S. Page, “Continuous inspection schemes,” Biometrika, vol. 41, no. 1/2, pp. 100–115, 1954.

[70] M. Basseville, I. V. Nikiforov et al., Detection of Abrupt Changes: Theory and Application. Prentice Hall, 1993, vol. 104.

[71] S. Patro and K. K. Sahu, “Normalization: A preprocessing stage,” arXiv preprint arXiv:1503.06462, 2015.

[72] S. Garcia, M. Grill, J. Stiborek, and A. Zunino, “An empirical comparison of botnet detection methods,” Comput. Secur., vol. 45, pp. 100–123, 2014.

[73] M. Singh, M. Singh, and S. Kaur, “Detecting bot-infected machines using DNS fingerprinting,” Digit. Investig., vol. 28, pp. 14–33, 2019.

[74] V. L. Pochat, T. Van Goethem, S. Tajalizadehkhoob, M. Korczynski,´ and W. Joosen, “Tranco: A research-oriented top sites ranking hardened against manipulation,” arXiv preprint arXiv:1806.01156, 2018.

![](images/1f2eef22a317405475a631c209b44a44aee794770411e64287086dd9e29a7a50.jpg)  
Lin Ye received the Ph.D. degree in Information Security from Harbin Institute of Technology in 2011. He is currently an Associate Professor with the School of Cyberspace Science, Harbin Institute of Technology. His research interests include software security, system security, and network attack and defense.

![](images/12f849089a9bc4ab2ae06601a0fa622f5f04176bf9e51ead6def8d62217d3c42.jpg)

Runze Xie received the B.S. degree in Cyberspace Science from the Harbin Institute of Technology in 2024. He is currently working toward the Ph.D. degree with the Harbin Institute of Technology. His primary research interests include traffic detection.

![](images/3b87b2c4d3f9373a8396d74efe848f82c0698fb1124dc289379908643e580b51.jpg)

Zhongyun Hua received the Ph.D. degree in Computer and Information Science from the University of Macau in 2016. He is currently a Professor with the School of Computer Science and Technology, Harbin Institute of Technology. His research interests include applied cryptography, AI security, multimedia information security, multimedia forensics, and nonlinear systems and their applications.

![](images/f38e8b6c439342fb07383f5d60219acab020fd61996fc2f5f64534a1cdb5afe3.jpg)

Yunting Zhang received the B.S. degree in information security from the Harbin Engineering University, in 2019, and the Ph.D. degree in computer science from the Harbin Institute of Technology, in 2025. Her research interests include textual adversarial attacks and adversarial robustness evaluation of large language models.

![](images/a02cf17d735bc343a681753a6be3551bed40cac8853cd26e053e87910ea80c61.jpg)

Wei Jiang received the Ph.D. degree in Information Security from Harbin Institute of Technology in 2010. He is currently the Dean of the School of Cyberspace Science and the Associate Director of the Computing Department, Harbin Institute of Technology, as well as a Second-Level Professor. His research interests include network security, data security, artificial intelligence security, cyber governance, and online communication.
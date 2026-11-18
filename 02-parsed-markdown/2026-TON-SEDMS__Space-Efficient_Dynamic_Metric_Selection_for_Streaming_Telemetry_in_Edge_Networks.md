# SEDMS: Space-Efficient Dynamic Metric Selection for Streaming Telemetry in Edge Networks

Shuyu Pei, Kun Xie, Member, IEEE, Jigang Wen, Dafang Zhang, Yuxiang Chen, Kun Huang, Wei Liang, Gaogang Xie, Member, IEEE

Abstract—Fine-grained network telemetry provides a rich foundation for downstream monitoring tasks such as clusteringbased traffic identification and anomaly detection. However, continuously processing and uploading all per-packet telemetry metrics at the edge is challenging under tight memory and bandwidth constraints. Existing telemetry schemes predefine the set of metrics to monitor, yet IoT traffic is inherently nonstationary, and the discriminative value of metrics changes as traffic distributions evolve, causing a fixed telemetry metric subset to yield degraded effectiveness for monitoring tasks.

We propose SEDMS, a Space-Efficient framework for Dynamic Metric Selection. SEDMS enables edge gateways to maintain a compact and informative metric subset in an online manner without storing raw traffic or repeatedly retraining models. It combines (i) a bounded-memory matrix sketch to summarize high-volume telemetry data, (ii) a spectral-sparse optimization that performs metric selection directly on the sketch, and (iii) a lightweight dynamic update strategy that tracks the covariance approximation error of the sketch so that new key metrics are captured as the traffic distribution shifts.

We provide theoretical guarantees that SEDMS achieves a bounded approximation error to the optimal metric subset using only a fixed-size sketch. Extensive experiments on real-world telemetry datasets demonstrate that SEDMS achieves competitive performance on network traffic type analysis by selecting only 30%-70% of the original telemetry metrics. Moreover, SEDMS quickly captures the latest metric subset in response to evolving traffic distributions, maintaining the effectiveness of downstream clustering-based traffic identification and anomaly detection while significantly reducing storage and uplink bandwidth overhead on resource-constrained edge gateways. These results confirm that SEDMS enables resource-efficient telemetry

monitoring at the edge.

Index Terms—Network Telemetry, Telemetry Metric Selection, Edge Network

## I. INTRODUCTION

## A. Motivation and Problem Statement

Edge networks are witnessing a rapid growth of Internet of Things (IoT) devices [1], generating highly dynamic traffic patterns in which legitimate communications mix with malicious activity. Due to the non-stationary nature of IoT traffic [2], [3] and the increasing diversity of attacks, traditional coarse-grained counters can no longer capture such complex patterns. Fine-grained network telemetry is therefore essential for downstream monitoring tasks including traffic type identification and anomaly detection [4]–[8].

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/d5e7250c1d4442dc6670202542e2627f29bf13f5b51a281fcf6425917c2aa595.jpg)  
Fig. 1: Edge telemetry scenarios and research problem.

Fine-grained telemetry usually operates per packet [4], [9], [10]. As shown in Fig. 1, a common deployment mirrors LAN traffic to an edge gateway. The gateway extracts telemetry metrics from each packet, takes each IoT device (identified by its MAC address) as the basic monitoring unit, aggregates statistics at device granularity, and uploads the selected telemetry data to the cloud for different downstream monitoring tasks including cluster-based traffic identification and anomaly detection. Since different traffic types and attacks exhibit distinct patterns across aggregation dimensions and time scales [9], fine-grained telemetry is performed over multiple dimensions, statistical measures, and time scales for each incoming packet.

Following the telemetry scheme in [9], for every packet associated with a device (uplink or downlink), the gateway computes statistical measures (e.g., packet size mean/variance, jitter) across 5 time scales (100ms, 500ms, 1.5s, 10s, 1min) and 4 aggregation dimensions (Source IP, Channel, MAC– IP, Socket), producing a per-packet telemetry snapshot with a total of $D = 1 1 5$ candidate telemetry metrics. These metrics are maintained incrementally, so that each per-packet update requires only $\mathcal { O } ( D )$ time and $\mathcal { O } ( D )$ memory, enabling the gateway to keep pace with the incoming packet rate. As a result, snapshots are generated at full packet rate, producing a high volume of telemetry data.

After fine-grained telemetry metrics are collected, packets can be further grouped according to their similarity in packetlevel telemetry snapshots. Since packets belonging to the same traffic type follow consistent communication behavior in terms of aggregation dimensions, statistical measures, and time scales, their snapshots naturally form clusters in nearby regions of the feature space. This ensures that differences between traffic types and deviations caused by anomalous activities are effectively captured, providing a foundation for cluster-based traffic identification and anomaly detection.

However, uploading and processing such rich telemetry data is costly. Even in a moderate deployment with dozens of IoT devices at 50 packets per second per device, uploading all $D = 1 1 5$ metrics per packet with 32-bit encoding generates hundreds of KB/s to several MB/s of telemetry data. This overhead consumes a significant portion of the available uplink bandwidth, leaving less capacity for actual IoT traffic, and scales linearly with the number of devices, making uploading all metrics increasingly impractical in large deployments.

Existing methods either use all telemetry metrics for network monitoring tasks [9], [11], incurring the full bandwidth cost, or adopt polling and query-driven telemetry schemes [12]–[14] that require predefining statistical measures, reporting frequencies, and aggregation dimensions. However, since traffic characteristics evolve dynamically and attacks grow increasingly diverse, it is difficult even for security experts to predict which metric combinations will be most discriminative.

This raises a central question: How can an edge gateway dynamically select a compact subset of informative per-packet telemetry metrics from high-volume telemetry data under bounded memory, so as to support monitoring tasks including cluster-based traffic identification and anomaly detection?

## B. Challenges

Addressing this question requires overcoming two main technical challenges:

Challenge 1: Streaming efficiency under bounded memory.

Fine-grained per-packet telemetry across |d| aggregation dimensions, |s| statistical measures, and |w| time scales yields up to $D = | d | \times | s | \times | w |$ candidate metrics. Monitoring $N _ { T }$ consecutive snapshots per device incurs $\mathcal { O } ( N _ { T } D )$ memory, which grows without bound as $N _ { T }$ increases, making full storage and repeated optimization over historical data infeasible on resource-constrained edge gateways. It is therefore necessary to reduce memory from $\mathcal { O } ( N _ { T } D )$ to $\mathcal { O } ( L D )$ , where $L \ll N _ { T }$ is a small constant.

## Challenge 2: Adaptation to evolving distributions.

On the one hand, the selected metric subset must preserve the statistical and structural properties of the original data to support downstream analytics. On the other hand, IoT traffic is non-stationary: metric relevance shifts over time as workloads change or attackers adapt their strategies. A metric that is informative today may become irrelevant tomorrow. Edge systems must therefore continuously update the selected metric subset to track these distribution changes without revisiting historical data.

While traditional metric selection techniques (e.g., based on variance or mutual information) [15]–[18] are computationally efficient, they often ignore inter-metric dependencies and may select redundant metrics. More advanced methods leverage spectral graph theory and sparse optimization [19]–[21], $\mathrm { e . g . }$ using $l _ { 2 , 1 }$ -norm regularization, to model inter-metric structure. However, these techniques are typically designed for offline settings and assume full access to the data, making them unsuitable for streaming scenarios.

## C. Our Contributions

To address the above core challenges, we propose SEDMS, a Space-Efficient framework for Dynamic Metric Selection. SEDMS enables real-time metric selection over per-device streaming telemetry while maintaining close approximation guarantees and adapting to evolving network conditions. Our main contributions are as follows:

• A memory-efficient matrix sketching framework. We design a fixed-size matrix sketch for each IoT device to summarize high-volume streaming telemetry data with bounded memory in real time. This compact representation eliminates the need to store raw telemetry data, significantly reducing memory overhead while retaining essential structure.

• An orthogonal spectral-sparse optimization model. We introduce a novel objective function that jointly enforces data reconstruction fidelity, graph Laplacian regularization to capture inter-metric structure, and row-wise sparsity for metric selection, all applied directly to the small matrix sketch.

• Provable approximation guarantees and convergence analysis. We provide theoretical analysis demonstrating that: (i) the indicator matrix learned from the matrix sketch closely approximates that derived from the full telemetry data; and (ii) our optimization strategy achieves provable convergence.

• Extensive evaluation on real-world datasets. Results show that SEDMS achieves competitive performance in cluster-based traffic type identification and anomaly detection while selecting only 30%–70% of the original metrics. As traffic distributions shift, SEDMS dynamically updates the selected metric subset and maintains downstream effectiveness.

This article has been accepted for publication in IEEE Transactions on Networking. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TON.2026.3748593

## II. RELATED WORK

## A. Metric Selection in Network Telemetry Systems

Reducing monitoring overhead under limited bandwidth, memory, and processing resources is a central objective of network telemetry systems. Existing studies pursue this objective at different stages of the telemetry pipeline, ranging from efficient execution of predefined measurement tasks to the prioritization and selection of collected telemetry metrics.

Predefined metrics and query-driven telemetry. Some studies reduce telemetry overhead by optimizing the execution of predefined monitoring tasks [13], [14], [22]–[25]. Elastic Sketch [22] accurately estimates predefined per-flow statistics, such as flow sizes and heavy hitters, under dynamically changing traffic conditions. In query-driven telemetry, Sonata [14], DynATOS [23], and DynaMap [24] dynamically manage the limited hardware resources of programmable switches, deciding at which pipeline stage to deploy each monitoring task, which registers to use, and how to allocate fixed-capacity resources under hardware capacity constraints. These approaches require a predefined set of telemetry metrics, and focus on how to execute monitoring tasks efficiently rather than questioning which metrics are most informative.

Post-collection metric selection. A few network telemetry studies more directly consider the relative importance of telemetry metrics. NetScope [26] assigns higher priority to metrics that exhibit anomalous values during failures while remaining stable under normal conditions. InfoSen [18] ranks telemetry metrics according to the information content estimated from historical data. However, both methods evaluate individual metrics independently and may overlook subsets whose metrics are weak in isolation but jointly discriminative. Moreover, their reliance on separately computed metric scores or historical observations limits their ability to preserve the evolving joint structure of high-rate telemetry streams.

These systems address different concerns in the telemetry pipeline: Elastic Sketch [22] answers how to measure a predefined metric accurately, Sonata [14], DynATOS [23], and DynaMap [24] decide where and when to deploy monitoring tasks on limited switch resources, and SEDMS determines which collected metrics are most discriminative and should be exported. Together, they can achieve end-to-end bandwidth and resource savings that neither stage achieves alone.

## B. Unsupervised Metric Selection in the Machine Learning Literature

Outside of networking, unsupervised metric selection has been extensively studied. Existing methods are commonly categorized as wrapper, filter, and embedded approaches.

Wrapper methods. Wrapper methods evaluate candidate metric subsets based on downstream task performance, often using greedy or heuristic search [27], [28]. While effective in some settings, they are computationally expensive due to repeated model training and are generally unsuitable for realtime, high-rate streaming telemetry.

Filter methods. Filter methods rank metrics using intrinsic criteria such as variance, entropy, or mutual information [29]. Representative examples include Laplacian Score [16], which favors features that preserve local neighborhood structure, and InfUFS [17], which models metric relevance via graph-based centrality. Although computationally attractive, filter methods may ignore dependencies between metrics and can select redundant metrics, which is undesirable in structured domains such as network telemetry.

Embedded methods. Embedded methods incorporate metric selection into model learning via sparsity-inducing regularization. For instance, $\ell _ { 2 , 1 }$ or $\ell _ { 2 , 0 }$ regularization [30], [31] encourages row-wise sparsity in a projection/weight matrix, thereby selecting a small set of metrics. SPCAFS [21] combines PCA-style objectives with sparsity to discard uninformative features. In addition, several unsupervised selection methods preserve data geometry using similarity graphs, such as MVUFS [32], RUSLP [19], and OCLSP [33].

Despite their effectiveness, most embedded and graphregularized methods assume batch access to the entire data. Some extensions consider sliding windows, but still require storing raw samples and repeatedly retraining models, which is often incompatible with memory-bounded edge gateways and high-rate telemetry.

## III. PROBLEM AND OVERVIEW

## A. Scenario and Problem Statement

1) Fine-grained Edge Telemetry in IoT Networks: We consider an edge-based IoT network where heterogeneous IoT devices (e.g., cameras and appliances) access the Internet through an access point and an L2 switch. The switch mirrors traffic to an edge gateway for monitoring and analytics. Compared to coarse-grained counters, fine-grained telemetry computes rich per-packet statistical measures across multiple aggregation dimensions and time scales, enabling the gateway to capture subtle behavioral anomalies that only emerge at specific dimensions or time scales.

Telemetry Metric Types and Telemetry Snapshot. We define a telemetry metric type $f _ { i }$ as a triplet (d, s, w), where d denotes an aggregation dimension (e.g., Source IP, Channel, MAC-IP, Socket), s denotes a statistical measure (e.g., packet count, packet variance), and w denotes a temporal window. Following the fine-grained telemetry scheme [9], [10], four aggregation dimensions are used, each capturing traffic behavior at a different granularity: Source $I P$ aggregates all traffic originating from the same source IP address; Channel aggregates traffic between the same source–destination IP pair; MAC-IP aggregates traffic originating from the same source MAC and source IP address, linking device identity to its network address; and Socket aggregates traffic between the same source and destination sockets (IP address + port number). The gateway computes metrics over five temporal window durations: W = {100ms, 500ms, 1.5s, 10s, 1min}.

For example, for a packet from source IP 192.168.1.5, one telemetry metric $f _ { i } ~ = ~ ( \mathrm { S o u r c e ~ I P }$ , packet count, 10s) is the number of packets observed from that source IP 192.168.1.5 within the past 10s.

At each packet arrival time t, the gateway computes 23 telemetry metrics per window (summarized in Table I) across $| \mathcal { W } | = 5$ time scales, yielding $D = 2 3 \times 5 = 1 1 5$ telemetry metrics in total and forming a 115-dimensional telemetry snapshot $\mathbf { x } _ { t } \in \mathbb { R } ^ { 1 1 5 }$ . Stacking telemetry snapshots over time gives the monitoring matrix $\mathbf { \bar { \boldsymbol { X } } } _ { t } \in \mathbb { R } ^ { N _ { t } \times D }$ , where $N _ { t }$ is the number of packets observed so far.

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/4ae85aec85e9385d120dd1c61b62ca5cf7cc086d044af66a9aa57a9b969d505e.jpg)  
Fig. 2: SEDMS Workflow on the Edge Gateway

TABLE I: 23 Telemetry Metric Types per Time Scale

<table><tr><td>Aggregation Dimensions</td><td>Statistical Measures</td><td>Total</td></tr><tr><td>Source IP, Channel, MAC-IP, Socket</td><td>Packet size: mean, variance</td><td>4 × 2 = 8</td></tr><tr><td>Source IP, Channel, MAC-IP, Socket</td><td>Packet count: count</td><td>4 × 1 = 4</td></tr><tr><td>Channel</td><td>Packet jitter: mean, variance, count</td><td>1 × 3 = 3</td></tr><tr><td>Channel, Socket</td><td>Bidirectional relationship: magnitude, radius, covariance, correlation coefficient</td><td>2 × 4 = 8</td></tr></table>

2) Problem Statement and Goal: Continuously exporting all D telemetry metrics per snapshot is infeasible at the edge due to limited uplink bandwidth and constrained memory. Moreover, a static metric subset is insufficient, since IoT traffic is non-stationary and metric relevance shifts over time. This motivates dynamic metric selection under streaming and resource constraints.

Formally, at any time t, the objective is to dynamically select a compact subset of $k < D$ informative metrics, denoted as ${ \cal { F } } _ { t } \subseteq { \cal { F } } = \{ f _ { 1 } , f _ { 2 } , . . . , f _ { D } \}$ , that preserves key structural and statistical properties of the full telemetry data:

$$
F _ {t} ^ {*} = \arg \min _ {F _ {t} \subseteq F} \mathcal {L} (X _ {t}, F _ {t}),\tag{1}
$$

where $\mathcal { L } ( \cdot )$ is a loss function that quantifies the information loss incurred when using the optimal subset $F _ { t } ^ { * }$ rather than the full metric set. Our goal is to dynamically select a compact informative telemetry metric subset for each device from the streaming telemetry snapshots, subject to three requirements:

• Bandwidth Efficiency: For each telemetry snapshot, export at most $k < D$ of the $D$ total metrics, reducing the telemetry volume from $D$ to k values per snapshot.

• Space Efficiency: Summarize $X _ { t }$ using a bounded-size structure, without storing raw snapshots, with memory usage independent of the stream length.

• Dynamics and Accuracy: Despite memory constraints, the selected subset $F _ { t } ^ { * }$ should approximate the optimal selection based on the complete data distribution, and adapt as traffic distributions evolve.

## B. Overview and Workflow of the SEDMS Scheme

To address the above problem, we propose SEDMS, a sketch-driven framework that performs per-device metric selection at an edge gateway with bounded memory.

Key Insights. SEDMS maintains a fixed-size matrix sketch per device that continuously summarizes incoming telemetry snapshots without storing raw data, reducing memory from $\mathcal { O } ( N _ { T } D )$ to $\mathcal { O } ( L D )$ where $L \ll N _ { T }$ . When the sketch is full, SEDMS performs metric selection directly on it using an orthogonal spectral-sparse optimization model that captures inter-metric dependencies, and then releases space by discarding low-energy components while retaining the dominant structure needed to identify informative metrics. An errordriven update mechanism refreshes the selected telemetry metric subset when the current matrix sketch preserves the main structure of the data beyond the acceptable error threshold.

The SEDMS workflow is shown in Fig. 2, and consists of the following tightly integrated stages:

• MAC-based Device Recognition and Matrix Sketch Localization. SEDMS uses the MAC address as the device identifier, with each device maintaining its own sketch. For each packet, the gateway parses the source or destination MAC addresses, extracts telemetry metrics to form a snapshot, and updates the sketch of any matched device with the snapshot, covering both uplink (device → Internet) and downlink (Internet → device) traffic. If both MACs match monitored devices, both sketches are updated.

• Sketch-Based Metric Selection Module. Built on a device’s matrix sketch, this module applies matrix factorization and spectral graph learning to uncover latent dependencies among telemetry metrics, producing a metric indicator matrix that quantifies the importance of each metric and enables selection of the top-k most discriminative ones. As shown in Fig. 2, the module selects device-specific metric subsets: for instance, $\{ f _ { 1 } , f _ { 2 } \}$ for device A and $\{ f _ { 1 } , f _ { 3 } \}$ for device B, reflecting each device’s distinct traffic characteristics.

• Dynamic Telemetry Metric Update Module. When the approximation error of the current matrix sketch exceeds a predefined threshold, it indicates that the underlying data patterns have shifted sufficiently that the current metric subset may no longer be representative. The module then triggers metric re-selection on the latest sketch. For example, as shown in Fig. 2, device A’s metrics adapt from $\{ f _ { 1 } , f _ { 2 } \}$ to $\{ f _ { 1 } , f _ { 3 } \}$ and device B’s from $\{ f _ { 1 } , f _ { 3 } \}$ to $\{ f _ { 1 } , f _ { 4 } \}$

• Telemetry Export. After selection, SEDMS exports only the telemetry values corresponding to the top-k metrics $( \mathrm { e . g . }$ $k = 1 0 { - } 2 0$ out of $D = 1 1 5 )$ per device to the cloud backend, achieving $80 \% - 9 0 \%$ bandwidth reduction while retaining the most informative data for downstream monitoring tasks.

Key Advantages. SEDMS maintains bounded per-device memory via a fixed-size matrix sketch and customizes metric selection through separate per-device sketches. Together, these properties bridge the gap between fine-grained telemetry and edge deployment constraints, with theoretical guarantees provided in Section IV-B and Section V-B.

## IV. DETAILED SOLUTION

## A. Space-Efficient Metric Selection Method

In this subsection, we begin by analyzing the limitations of conventional metric selection methods that require access to all historical telemetry snapshots, and then introduce our sketch-based solution.

Limitations of Metric Selection over Full Telemetry Snapshots. For each IoT device, every incoming packet yields one telemetry snapshot $\mathbf { x } _ { t } \in \mathbb { R } ^ { D }$ . Let $X _ { t } \in \overline { { \mathbb { R } ^ { N _ { t } \times D } } }$ denote the monitoring matrix stacking all snapshots up to time t. A common way is to solve the following optimization over a sparse orthonormal projection matrix $\mathbf { \bar { \boldsymbol { W } } } _ { t } ^ { \mathbf { \bar { \boldsymbol { \mathbf { \Lambda } } } } } \in \mathbb { R } ^ { D \times C }$ that minimizes reconstruction error:

$$
\min _ {W _ {t}, W _ {t} ^ {\top} W _ {t} = \mathbb {I}} \| X _ {t} ^ {\top} - W _ {t} W _ {t} ^ {\top} X _ {t} ^ {\top} \| _ {F} ^ {2} + \mathcal {R} (W _ {t}),\tag{2}
$$

where $\mathcal { R } ( W _ { t } )$ is a sparsity-inducing regularization term. The importance of metric $f _ { i }$ is defined as $\mathrm { W e i g h t } ( f _ { i } ) = \| W _ { t } ( i ,$ $) \big | \big | _ { 2 }$ , and the top-k metrics form the selected subset $F _ { t } ^ { * }$

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/16d2d9e45063a28e8a226ecb4a5de74debf4cc7b61e92c9e63bdcdebc7b98f56.jpg)

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/6808b121513954c5cefef36d8ccc75e22520569ceab8cd333295588c1938cf4f.jpg)  
(a) at time t  
Fig. 3: Diagram of conventional metric selection in streams.

Note that computing telemetry metrics from each packet is incremental, which means snapshots are produced at full packet rate, generating a large volume of telemetry data. The bottleneck therefore lies not in metric computation but in metric selection, which must capture inter-metric correlations across many snapshots and thus requires access to the full monitoring matrix $X _ { t }$ , whose storage grows as $\mathcal { O } ( N _ { t } D )$ with the length of the snapshot stream.

Fig. 3 illustrates this limitation. As packets arrive continuously, the monitoring matrix $X _ { t + 1 }$ grows without bound and must be fully reprocessed to obtain a new projection matrix $W _ { t + 1 }$ and updated metric subset, which is unsustainable for long-running edge telemetry systems. This reveals two major issues: (1) Unbounded Storage: As packets arrive continuously, $X _ { t }$ grows without bound, quickly exceeding the memory capacity of edge gateways. (2) High Computation Cost: Each update requires solving the projection problem in $\operatorname { E q . } ( 2 )$ , over an ever-growing matrix, which severely limits scalability.

Sketch-Based Telemetry Data Representation. To overcome these limitations, we maintain a matrix sketch $B _ { t } \in  \Psi$ $\mathbb { R } ^ { L \times D }$ per device (identified by MAC address), where $L \ll$ $N _ { t }$ , instead of storing the full matrix $X _ { t }$ . The sketch preserves the covariance structure and essential statistical properties of $X _ { t }$ in a memory-efficient form. For each incoming packet, the gateway extracts the device MAC address and updates the corresponding sketch with the current telemetry snapshot $\mathbf { x } _ { t } ,$ covering both uplink and downlink traffic.

Unlike the conventional monitoring matrix $X _ { t } ,$ , which grows unboundedly, the sketch $B _ { t }$ maintains a fixed size of $L \times D$ throughout the stream. Incoming snapshots are appended row by row. When no zero-valued rows remain, we apply the Frequent Directions (FD) algorithm [34], [35], which offers deterministic accuracy guarantees. FD performs an SVD $\begin{array} { r c l } { B _ { t } } & { = } & { U \Sigma V ^ { \top } } \end{array}$ and shrinks the spectrum as $\begin{array} { r l } { \stackrel { \circ } { \Sigma } } & { { } = } \end{array}$ $\sqrt { \operatorname* { m a x } ( \Sigma ^ { 2 } - \sigma _ { \ell } ^ { 2 } \mathbb { I } , 0 ) }$ , where $\sigma _ { \ell }$ is the ℓ-th singular value, then sets $B _ { t }  \mathring { \Sigma } V ^ { \top }$ . This evicts low-energy components and frees rows for new snapshots while preserving the dominant covariance structure. After shrinking, $B _ { t }$ consists of two parts: $B _ { t _ { 1 } } ~ \in ~ \mathbb { R } ^ { L _ { 1 } \times D } ~ ( L _ { 1 } ~ = ~ \ell ~ - ~ 1 )$ , retaining dominant information from previous shrink steps, and $B _ { t _ { 2 } } \ \in \ \mathbb { R } ^ { L _ { 2 } \times D }$ $( L _ { 2 } \ = \ L - \ell + 1 )$ , serving as a buffer for newly arriving snapshots.

Metric Selection via Orthogonality Sparse Projection. Although $B _ { t }$ is significantly smaller than $X _ { t }$ , it retains sufficient structural information to support effective metric selection. Our goal is to seek a sparse orthonormal projection matrix $W _ { B } \in \bar { \mathbb { R } ^ { D \times C } } \ ( C \ll D )$ as the metric indicator matrix, which maps the original metric space to a lower-dimensional latent subspace and reconstructs $B _ { t }$ via orthogonal projection while maintaining row sparsity for metric selection.

We formulate the following optimization problem:

$$
\min _ {W _ {B}, W _ {B} ^ {T} W _ {B} = \mathbb {I}} \| B _ {t} ^ {T} - W _ {B} W _ {B} ^ {T} B _ {t} ^ {T} \| _ {F} ^ {2} + \mathcal {R} (W _ {B}),\tag{3}
$$

where $\mathcal { R } ( W _ { B } )$ is a sparsity-inducing regularization term such as the $l _ { 2 , 1 }$ norm, promoting row-level sparsity in $W _ { B }$ . Due to $W _ { B } ^ { T } W _ { B } = \mathbb { I } , \operatorname { E q . } ( 3 )$ can be written using trace identities $t r ( \cdot ) \colon$

$$
\begin{array}{l} \| W _ {B} W _ {B} ^ {T} B _ {t} ^ {T} - B _ {t} ^ {T} \| _ {F} ^ {2} \\ = \operatorname{tr} (B _ {t} W _ {B} W _ {B} ^ {T} W _ {B} W _ {B} ^ {T} B _ {t} ^ {T}) - 2 \operatorname{tr} (B _ {t} W _ {B} W _ {B} ^ {T} B _ {t} ^ {T}) + \operatorname{tr} (B _ {t} B _ {t} ^ {T}) \\ = - \operatorname{tr} (B _ {t} W _ {B} (B _ {t} W _ {B}) ^ {T}) + \operatorname{tr} (B _ {t} B _ {t} ^ {T}), \end{array} \tag {4}
$$

Since $\operatorname { t r } ( B B ^ { T } )$ is constant with respect to $W _ { B }$ , the optimization simplifies to:

$$
\min _ {W _ {B}, W _ {B} ^ {T} W _ {B} = \mathbb {I}} - \mathrm{tr} (W _ {B} ^ {T} B _ {t} ^ {T} B _ {t} W _ {B}) + \mathcal {R} (W _ {B})\tag{5}
$$

The three components of Eq. (5) serve distinct roles, yielding a compact and interpretable metric indicator matrix $W _ { B } { : }$

• Variance Maximization $( - \mathrm { t r } ( W _ { B } ^ { T } B _ { t } ^ { T } B _ { t } W _ { B } ) )$ : aligns $W _ { B }$ with the directions of greatest variance in the telemetry data, selecting the most informative projection directions.

• Orthogonality $( W _ { B } ^ { T } W _ { B } \ = \ \mathbb { I } )$ : ensures projection directions are mutually uncorrelated, avoiding redundancy.

• Sparsity $( \mathcal { R } ( W _ { B } ) )$ : drives entire rows of $W _ { B }$ to zero, retaining only metrics that contribute significantly to the projection.

Selecting Metrics from $W _ { B } .$ . The learned matrix $W _ { B }$ naturally encodes metric importance. The $\ell _ { 2 } { \mathrm { - n o r m } }$ of each row, $\| W _ { B } ( i , : ) \| _ { 2 } ,$ quantifies the contribution of metric $f _ { i }$ to the latent space. Metrics with larger norms are selected as the top-k subset and exported for downstream analysis. Overall, this sketch-based framework enables online, space-efficient, and interpretable metric selection without requiring access to the original telemetry matrix $X _ { t }$

## B. Theoretical Analysis of Equivalence

To ensure that sketch-based metric selection remains effective, in this subsection, we theoretically justify that the indicator matrix $W _ { B }$ derived from the compact sketch $B _ { t }$ closely approximates that derived from the full telemetry matrix $X _ { t }$ , based on the covariance-preserving property of matrix sketching techniques.

Covariance-Preserving Property. A fundamental guarantee of the FD sketch is the preservation of second-order statistics of the telemetry stream [7], [36]. Specifically, the sketch $B _ { t }$ provides the following covariance approximation:

$$
B _ {t} ^ {\top} B _ {t} \approx X _ {t} ^ {\top} X _ {t},\tag{6}
$$

where $X _ { t } ~ \in ~ \mathbb { R } ^ { N _ { t } \times D }$ is the full telemetry matrix and $B _ { t } \ \in$ $\mathbb { R } ^ { L \times D }$ is the sketch with $L \ll N _ { t }$ . This implies that optimization objectives involving $X _ { t } ^ { \top } X _ { t }$ can be replaced by $B _ { t } ^ { \top } B _ { t }$ with bounded error. Applying this to Eq. (5):

$$
\begin{array}{c} \min _ {W _ {B}, W _ {B} ^ {\top} W _ {B} = \mathbb {I}} - \mathrm{tr} (W _ {B} ^ {\top} B _ {t} ^ {\top} B _ {t} W _ {B}) + \mathcal {R} (W _ {B}) \\ \approx \min _ {W _ {B}, W _ {B} ^ {\top} W _ {B} = \mathbb {I}} - \mathrm{tr} (W _ {B} ^ {\top} X _ {t} ^ {\top} X _ {t} W _ {B}) + \mathcal {R} (W _ {B}). \end{array}\tag{7}
$$

Following the trace expansion in Eq. (4), the full-data objective converts to:

$$
\begin{array}{c} \min _ {W _ {B}, W _ {B} ^ {\top} W _ {B} = \mathbb {I}} - \mathrm{tr} (W _ {B} ^ {\top} X _ {t} ^ {\top} X _ {t} W _ {B}) + \mathcal {R} (W _ {B}) \\ = \min _ {W _ {B}, W _ {B} ^ {\top} W _ {B} = \mathbb {I}} \| W _ {B} W _ {B} ^ {\top} X _ {t} ^ {\top} - X _ {t} ^ {\top} \| _ {F} ^ {2} + \mathcal {R} (W _ {B}). \end{array}\tag{8}
$$

Comparing Eq. (8) with Eq. (2) establishes the approximate equivalence:

$$
\begin{array}{r l} & {\underset {W _ {B}, W _ {B} ^ {\top} W _ {B} = \mathbb {I}} {\min} \| W _ {B} W _ {B} ^ {\top} B _ {t} ^ {\top} - B _ {t} ^ {\top} \| _ {F} ^ {2} + \mathcal {R} (W _ {B})} \\ & {\approx \underset {W _ {B}, W _ {B} ^ {\top} W _ {B} = \mathbb {I}} {\min} \| W _ {B} W _ {B} ^ {\top} X _ {t} ^ {\top} - X _ {t} ^ {\top} \| _ {F} ^ {2} + \mathcal {R} (W _ {B})} \\ & {\approx \underset {W _ {t}, W _ {t} ^ {\top} W _ {t} = \mathbb {I}} {\min} \| W _ {t} W _ {t} ^ {\top} X _ {t} ^ {\top} - X _ {t} ^ {\top} \| _ {F} ^ {2} + \mathcal {R} (W _ {t}).} \end{array}\tag{9}
$$

This theoretical analysis establishes that $W _ { B }$ derived from the compact sketch $B _ { t }$ closely approximates the optimal $W _ { t }$ derived from the full telemetry matrix $X _ { t } ,$ enabling effective metric selection on resource-constrained edge gateways without storing raw telemetry data.

## C. Graph-Regularized Metric Selection

Beyond reconstruction quality and sparsity, effective metric selection should also capture intrinsic inter-metric relationships and preserve the geometric structure of the data. In IoT traffic, metrics often exhibit complex correlations: for instance, packet size mean and variance under the same aggregation dimension are inherently correlated, and bidirectional metrics such as magnitude, radius, and covariance jointly characterize device-peer interactions yet individually may appear uninformative. Ignoring such dependencies can lead to redundant or suboptimal selections.

To address this, we incorporate graph Laplacian regularization into the objective, enforcing local geometric consistency: if two telemetry snapshots are similar in the original space, their projections should remain close in the latent space. Since $B _ { 2 }$ buffers the most recent telemetry snapshots, we construct a similarity graph over $B _ { 2 }$ to capture local structure. If two snapshots $B _ { 2 } ( i , : )$ and $B _ { 2 } ( j , : )$ are similar, their projections $W _ { B } ^ { \dagger } B _ { 2 } ( i , : ) ^ { \top }$ and $W _ { B } ^ { \top } B _ { 2 } ( j , : ) ^ { \top }$ should also be close:

$$
\sum_ {i, j = 1} ^ {L _ {2}} \left\| W _ {B} ^ {\top} B _ {2} (i,:) ^ {\top} - W _ {B} ^ {\top} B _ {2} (j,:) ^ {\top} \right\| _ {2} ^ {2} s _ {i, j}.\tag{10}
$$

Combining this with the reconstruction objective yields:

$$
\begin{array}{l} \min _ {W _ {B}, W _ {B} ^ {\top} W _ {B} = \mathbb {I}} \left\| B _ {t} ^ {\top} - W _ {B} W _ {B} ^ {\top} B _ {t} ^ {\top} \right\| _ {F} ^ {2} \\ + \alpha \sum_ {i, j = 1} ^ {L _ {2}} \left\| W _ {B} ^ {\top} B _ {2} (i,:) ^ {\top} - W _ {B} ^ {\top} B _ {2} (j,:) ^ {\top} \right\| _ {2} ^ {2} s _ {i, j}, \end{array}\tag{11}
$$

where $\alpha > 0$ controls the strength of local structure preservation, and $s _ { i , j }$ denotes the similarity between snapshots i and $j$ in $B _ { 2 } .$ , computed via a Gaussian kernel over local neighborhoods $\mathcal { N } ( \cdot )$

$$
s _ {i, j} = \left\{\begin{array}{l l}\exp \left(\frac {| | B _ {2} (i , :) - B _ {2} (j , :) | | ^ {2}}{- 2 \sigma^ {2}}\right),&B _ {2} \left( \right.i,:) \in \mathcal {N} \left(B _ {2} \left(j,:)\right)\right.\\&o r B _ {2} \left( \right.j,:) \in \mathcal {N} \left(B _ {2} \left(i,:)\right)\right.\\0,&o t h e r w i s e\end{array}\right.\tag{12}
$$

To support metric selection, we apply $\ell _ { 2 , 1 }$ -norm regularization on $\dot { W } _ { B }$ to encourage row-wise sparsity, driving uninformative telemetry metrics to zero and retaining only the most discriminative ones. The resulting joint objective becomes:

$$
\begin{array}{l} \min _ {W _ {B}, W _ {B} ^ {T} W _ {B} = \mathbb {I}} \left\| \left[ \begin{array}{c} B _ {1} \\ B _ {2} \end{array} \right] ^ {T} - W _ {B} W _ {B} ^ {T} \left[ \begin{array}{c} B _ {1} \\ B _ {2} \end{array} \right] ^ {T} \right\| _ {F} ^ {2} \\ + \alpha \sum_ {i, j = 1} ^ {L _ {2}} \left\| W _ {B} ^ {T} B _ {2} (i,:) ^ {T} - W _ {B} ^ {T} B _ {2} (j,:) ^ {T} \right\| _ {2} ^ {2} s _ {i, j} + \beta \| W _ {B} \| _ {2, 1} \end{array} \tag {13}
$$

where $\beta > 0$ controls the sparsity level of the selected telemetry metrics. The graph regularization term in Eq. (13) can be equivalently expressed using the graph Laplacian matrix. Let $\boldsymbol { S } ^ { \dot { \mathbf { \Upsilon } } } = [ s _ { i , j } ] \dot { \in } \mathbb { R } ^ { \hat { L } _ { 2 } \times L _ { 2 } }$ denote the similarity matrix, and define the Laplacian $L _ { B }$ as $\begin{array} { r } { L _ { B } = D _ { B } - \frac { S + S ^ { T } } { 2 } } \end{array}$ , where $D _ { B } \in \mathbb { R } ^ { L _ { 2 } \times L _ { 2 } }$ is the degree matrix with diagonal entries:

$$
D _ {B} = \operatorname{diag} \left(\sum_ {j = 1} ^ {L _ {2}} \frac {s _ {1 j} + s _ {j 1}}{2}, \dots , \sum_ {j = 1} ^ {L _ {2}} \frac {s _ {L _ {2} j} + s _ {j L _ {2}}}{2}\right).\tag{14}
$$

Using the Laplacian, the graph smoothness term simplifies to:

$$
\sum_ {i, j = 1} ^ {L _ {2}} \left\| W _ {B} ^ {T} B _ {2} (i,:) ^ {T} - W _ {B} ^ {T} B _ {2} (j,:) ^ {T} \right\| _ {2} ^ {2} s _ {i, j} = \mathfrak {t r} (W _ {B} ^ {T} B _ {2} ^ {T} L _ {B} B _ {2} W _ {B}).\tag{15}
$$

To simplify notation, we define the projected data matrix as $P = \left[ P _ { 1 } ^ { 1 } \right] = \left[ B _ { 1 } \right] W _ { B }$ , substituting into Eq. (13), the final optimization problem becomes:

$$
\begin{array}{l} \min _ {W _ {B}, P} \left\| \left[ \begin{array}{c} B _ {1} \\ B _ {2} \end{array} \right] ^ {T} - W _ {B} P ^ {T} \right\| _ {F} ^ {2} + \alpha \operatorname{tr} (P _ {2} ^ {T} L _ {B} P _ {2}) + \beta \| W _ {B} \| _ {2, 1} \\ \text { s.t. } \quad W _ {B} ^ {T} W _ {B} = \mathbb {I}, \quad \left[ \begin{array}{c} B _ {1} \\ B _ {2} \end{array} \right] W _ {B} = P. \end{array} \tag {16}
$$

## V. OPTIMIZATION AND ANALYSIS

To solve Eq. (16), we propose an efficient alternating optimization framework that decomposes the joint objective into two subproblems, iteratively updating one variable while keeping the other fixed. This yields simple closed-form multiplicative update rules with provable convergence guarantees.

## A. Optimization Strategy

The objective in Eq. (16) combines reconstruction loss, graph-based regularization over recent snapshots in $B _ { 2 }$ , and $\ell _ { 2 , 1 }$ <sub>1</sub> sparsity on $W _ { B }$ for metric selection. We relax the hard constraints into soft penalties, yielding the augmented objective:

$$
\begin{array}{l} \mathcal {J} (W _ {B}, P) = \left\| \left[ \begin{array}{c} B _ {1} \\ B _ {2} \end{array} \right] ^ {T} - W _ {B} P ^ {T} \right\| _ {F} ^ {2} + \alpha \mathrm{tr} (P _ {2} ^ {T} L _ {B} P _ {2}) \\ \qquad + \beta \| W _ {B} \| _ {2, 1} + \gamma_ {1} \| W _ {B} ^ {T} W _ {B} - \mathbb {I} \| _ {F} ^ {2} + \gamma_ {2} \left\| \left[ \begin{array}{c} B _ {1} \\ B _ {2} \end{array} \right] W _ {B} - P \right\| _ {F} ^ {2} \end{array}\tag{17}
$$

where $B = \left\lceil { B _ { 1 } } \right\rceil$ , and $\gamma _ { 1 } , \gamma _ { 2 }$ are penalty parameters enforcing orthonormality and projection consistency, respectively. We minimize $\mathcal { I } ( W _ { B } , P )$ by alternating between updating $W _ { B }$ and updating P.

Updating $W _ { B }$ . We first update $W _ { B }$ by fixing P. Taking the derivative of J with respect to $W _ { B }$ and setting it to zero yields:

$$
\begin{array}{l} \frac {\partial \mathcal {J}}{\partial W _ {B}} = - 2 (1 + \gamma_ {2}) B ^ {T} P + 2 W _ {B} P ^ {T} P + \beta Q W _ {B} \\ + 4 \gamma_ {1} W _ {B} W _ {B} ^ {T} W _ {B} - 4 \gamma_ {1} W _ {B} + 2 \gamma_ {2} B ^ {T} B W _ {B} = 0 \end{array}
$$

where $\begin{array} { r c l } { Q } & { \in } & { \mathbb { R } ^ { D \times D } } \end{array}$ is a diagonal matrix with $\begin{array} { r l } { Q _ { i i } } & { { } = } \end{array}$ $\begin{array} { r l } & { \frac { \mathbf { 1 } } { 2 \sqrt { \| W _ { B } ( i , : ) \| _ { 2 } ^ { 2 } + \varepsilon } } } \\ & { \mathsf { b y ~ z e r o } . } \end{array}$ 1 , and ε is a small constant to avoid division

To obtain an efficient update rule, we employ a nonnegative multiplicative approach for $W _ { B }$ . Since $B _ { 1 }$ may contain negative entries, we write $B = \left[ \begin{array} { l } { B _ { 1 } } \\ { B _ { 2 } } \end{array} \right] , B _ { 1 } = B _ { 1 } ^ { + } - B _ { 1 } ^ { - }$ , where

$B _ { 1 } ^ { + } = \operatorname* { m a x } ( B _ { 1 } , 0 )$ and $B _ { 1 } ^ { - } = \operatorname* { m a x } ( - B _ { 1 } , 0 )$ . We then adopt the multiplicative update rule:

$$
W _ {B} \leftarrow W _ {B} \odot \sqrt {\frac {\operatorname{Num} _ {W _ {B}}}{\operatorname{Den} _ {W _ {B}} + \epsilon}},\tag{18}
$$

where ⊙ denotes element-wise multiplication, ϵ is a small constant for numerical stability, and

$$
\mathbf {N u m} _ {W _ {B}} = (1 + \gamma_ {2}) (B _ {1} ^ {+ T} P _ {1} + B _ {2} ^ {T} P _ {2}) + 2 \gamma_ {1} W _ {B}\tag{19}
$$

$$
\begin{array}{r l} \mathsf {D e n} _ {W _ {B}} = & W _ {B} P ^ {T} P + \frac {\beta}{2} Q W _ {B} + 2 \gamma_ {1} W _ {B} W _ {B} ^ {T} W _ {B} \\ & + \gamma_ {2} (B _ {1} ^ {+ T} B _ {1} ^ {+} + B _ {1} ^ {- T} B _ {1} ^ {-} + B _ {2} ^ {T} B _ {2}) W _ {B} \\ & + (1 + \gamma_ {2}) B _ {1} ^ {- T} P _ {1} \end{array}\tag{20}
$$

Updating P. Next, we fix $W _ { B }$ and update ${ \cal P } \_ { = }$ $[ P _ { 1 } ; { \mathsf { \bar { P } } } _ { 2 } ] \in { \mathbb { R } } ^ { L \times C }$ . The derivative of J with respect to P is:

$$
\frac {\partial \mathcal {J}}{\partial P} = 2 (1 + \gamma_ {2}) \left(P W _ {B} ^ {T} W _ {B} - B W _ {B}\right) + \left[ \begin{array}{c} \mathbf {0} _ {L _ {1} \times C} \\ 2 \alpha L _ {B} P _ {2} \end{array} \right].
$$

Let $\alpha L _ { B } = M ^ { + } - M ^ { - }$ , where $M ^ { + } = \textstyle { \frac { 1 } { 2 } } \left( \left| \alpha L _ { B } \right| + \alpha L _ { B } \right)$ and $M ^ { - } = \textstyle { \frac { 1 } { 2 } } ( | \alpha L _ { B } | - \alpha L _ { B } )$ . We partition $P = \left\lceil { P _ { 1 } } \right\rceil$ and derive the multiplicative update rules for $P _ { 1 }$ and $P _ { 2 }$ as follows: a) Update for $P _ { 1 }$ :

$$
P _ {1} \leftarrow P _ {1} \odot \sqrt {\frac {(1 + \gamma_ {2}) B _ {1} ^ {+} W _ {B}}{(1 + \gamma_ {2}) P _ {1} W _ {B} ^ {T} W _ {B} + (1 + \gamma_ {2}) B _ {1} ^ {-} W _ {B}}}\tag{21}
$$

b) Update for $P _ { 2 } .$

$$
P _ {2} \leftarrow P _ {2} \odot \sqrt {\frac {M ^ {-} P _ {2} + (1 + \gamma_ {2}) B _ {2} W _ {B}}{(1 + \gamma_ {2}) P _ {2} W _ {B} ^ {T} W _ {B} + M ^ {+} P _ {2}}}.\tag{22}
$$

The unified update can be written as:

$$
P \leftarrow P \odot \sqrt {\frac {\operatorname{Num} _ {P}}{\operatorname{Den} _ {P} + \epsilon}},\tag{23}
$$

with

$$
\mathbf {N u m} _ {P} = \left[ \begin{array}{c} (1 + \gamma_ {2}) B _ {1} ^ {+} W _ {B} \\ M ^ {-} P _ {2} + (1 + \gamma_ {2}) B _ {2} W _ {B} \end{array} \right],\tag{24}
$$

$$
\mathbf {D e n} _ {P} = \left[ \begin{array}{c} (1 + \gamma_ {2}) P _ {1} W _ {B} ^ {T} W _ {B} + (1 + \gamma_ {2}) B _ {1} ^ {-} W _ {B} \\ (1 + \gamma_ {2}) P _ {2} W _ {B} ^ {T} W _ {B} + M ^ {+} P _ {2} \end{array} \right].\tag{25}
$$

## B. Convergence Analysis

We analyze the convergence of the alternating optimization for $\mathcal { I } ( W _ { B } , P )$ in Eq. (17). Following the framework of multiplicative update rules [37], we show that the updates for $W _ { B }$ and P monotonically reduce the objective value and the iterative sequence converges to a KKT stationary point.

Theorem 1 The multiplicative updates in Eqs. (18) and (23) monotonically decrease the objective function $\mathcal { I } ( W _ { B } , P )$ in Eq. (17), and the sequence $\{ \mathcal { \bar { I } } ( W _ { B } ^ { ( t ) } , \bar { P } ^ { ( t ) } ) \} _ { t = 0 } ^ { \infty }$ generated by the alternating optimization is non-increasing and converges to a KKT stationary point.

Proof sketch. The proof proceeds in three steps. First, we construct an auxiliary function $G ( W _ { B } , W _ { B } ^ { ( t ) } )$ that upperbounds the objective J and coincides with it at the current iterate $( G ( W _ { B } , W _ { B } ) = \mathcal { I } )$ . Minimizing G recovers the multiplicative update rule and guarantees $\mathcal { I } ( W _ { B } ^ { ( t + 1 ) } , P ^ { ( t + 1 ) } ) \ \leq$ $\mathcal { I } ( W _ { B } ^ { ( t ) } , P ^ { ( t ) } )$ , establishing monotonic decrease. Second, since $\mathcal { I } \geq 0$ is bounded below and the sequence is nonincreasing, the monotone convergence theorem guarantees that $\mathcal { I }$ converges to a finite limit ${ \mathcal { T } } ^ { * }$ . Third, at convergence the multiplicative update reduces to $W _ { B } ^ { ( t + 1 ) } = W _ { B } ^ { ( t ) }$ , which implies $\ N _ { } \mathrm { u m } _ { W _ { B } } = \mathrm { D e n } _ { W _ { B } }$ (i.e., zero gradient) for all positive entries, while non-negativity ensures $\partial \mathcal { I } / \partial W _ { B i j } ~ \geq ~ 0$ for zero entries. Together these satisfy the KKT complementary slackness conditions, confirming that the limit point $( W _ { B } ^ { * } , P ^ { * } )$ is a KKT stationary point. The detailed proof is given in the supplementary material.

## C. Space and Time Complexity

We analyze the per-device space and time complexity, where each IoT device maintains an independent sketch keyed by MAC address.

Space Complexity. The main memory cost per device comes from the sketch $B _ { t } \ \in \ \mathbb { R } ^ { L \times D }$ , the projection matrix $W _ { B } ~ \in ~ \mathbb { R } ^ { D \times C }$ , and the embedding $P ~ \in ~ \bar { \mathbb { R } ^ { L \times C } }$ , totaling $\mathcal { O } ( L D + D C + L C )$ . Since $C \ll \operatorname* { m i n } ( D , L )$ , this is dominated by $\mathcal { O } ( L D )$ , which remains constant regardless of the number of observed packets, in contrast to $\mathcal { O } ( N _ { t } D )$ for the full matrix $X _ { t }$

Time Complexity. The time complexity is dominated by the alternating optimization of the two variables $W _ { B }$ and $P$ in Eqs. (18) and (23).

Updating $W _ { B } .$ . The dominant costs arise from $B ^ { \top } P$ at $\mathcal { O } ( L D C ) , B ^ { \top } B W _ { B }$ computed as $B ^ { \top } ( B W _ { B } )$ at $\mathcal { O } ( L D C )$ and $W _ { B } W _ { B } ^ { \top } W _ { B }$ at $\mathcal { O } ( D C ^ { 2 } )$ . The per-iteration cost is $\mathcal { O } ( L D C + \bar { D } C ^ { 2 } )$

Updating P. The dominant costs are $B W _ { B }$ at $\mathcal { O } ( L D C )$ $P ( W _ { B } ^ { \top } W _ { B } )$ at $\mathcal { O } ( L C ^ { 2 } )$ , and Laplacian smoothing at $\mathcal { O } ( L _ { 2 } ^ { 2 } C )$ for dense.

Overall Time Complexity with Convergence. Combining both updates, the total time complexity per iteration is $\mathcal { O } ( L D \bar { C } + D C ^ { 2 } + L C ^ { 2 } + L _ { 2 } ^ { 2 } C )$ . Here, D denotes the number of metrics, L is the number of rows in the sketch matrix, and C is the dimensionality of the projection subspace; In general, $C \ll \{ D , L \}$ and is typically small, with its value dependent on downstream tasks. The overall time complexity is dominated by the terms $\mathcal { O } ( L D C + L _ { 2 } ^ { 2 } C )$ . Let r denote the average number of iterations until convergence. Thus, the total time overhead for solving Eq. (17) is is $\bar { \mathcal { O } } ( r \cdot ( L D C + L _ { 2 } ^ { 2 } C ) )$ Empirically, r remains small due to the efficiency of the multiplicative updates, which ensures fast practical convergence.

## VI. UPDATE STRATEGY AND APPLICATIONS

## A. Update Strategy

In edge IoT monitoring, a static metric subset often fails to capture timely changes in key metrics, thereby degrading the performance of downstream tasks such as anomaly detection and traffic classification. Therefore, it is crucial to design a dynamically updating strategy under resource constraints.

SEDMS maintains a fixed-size sketch $\boldsymbol { B } _ { t } ~ \in ~ \mathbb { R } ^ { L \times D }$ per device to summarize incoming telemetry snapshots, instead of storing the full monitoring matrix $X _ { t } \in \mathbb { R } ^ { N _ { t } \times D }$ . As packets arrive continuously, $B _ { t }$ preserves the dominant covariance structure of the telemetry stream within bounded memory, enabling metric selection without access to raw historical data.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: SEDMS Procedure

Input: A warm-up snapshot $\{\mathbf{x}_1, \ldots, \mathbf{x}_{T_0}\}$ for a device; error budget $\eta$; parameters $\ell, \alpha, \beta, \gamma_1, \gamma_2, C, k$

Output: Top-$k$ metric subset $F_t^*$ for a device
// Initialization

1 Initialize sketch $B_t \in \mathbb{R}^{L \times D}$ by Eq.(26);
2 threshold $\delta = \frac{1}{L}$;
3 $c \leftarrow 1$, $e \leftarrow 0$, $E \leftarrow 0$;
// Streaming loop

4 for each arriving packet do
5 Compute snapshot $\mathbf{x}_t \in \mathbb{R}^D$, and match the matrix sketch for Mac Addr;
6 Insert $\mathbf{x}_t$ into $B_t(c, :)$;
7 $c \leftarrow c + 1$;
8 $E \leftarrow E + \| \mathbf{x}_t\|_2^2$;
// Trigger-1: capacity trigger
9 if $c &gt; L$ then
10 METRICSELECTIONANDSHRINK;
// Trigger-2: error trigger
11 else if $e/E &gt; \delta$ then
12 METRICSELECTIONANDSHRINK;

13 Procedure METRICSELECTIONANDSHRINK:
14 Construct Laplacian $L_B$;
// Converged if $|\mathcal{J}^{(t)} - \mathcal{J}^{(t+1)}|/\mathcal{J}^{(t)} &lt; \epsilon$ or max iterations reached
15 while not converged do
16 Update $W_B$ via Eq. (18);
17 Update $P$ via Eq. (23);
18 $F_t^* \leftarrow$ top-$k\{ \| W_B(j, :) \|_2\}_{j=1}^D$;
// FD shrink: accumulate discarded energy
19 $[U, \Sigma, V] \leftarrow \text{SVD}(B_t)$;
20 $e \leftarrow e + \sigma_\ell^2$;
21 $B_t \leftarrow \sqrt{\max(\Sigma^2 - \sigma_\ell^2\mathbb{I}, 0)} V^\top$;
22 $c \leftarrow \ell$;
23 if $E &gt; \eta \cdot L$ then
24 $L \leftarrow [E/\eta]$;
25 Reinitialize $B_t$ and $\delta$; $c \leftarrow 1$; $e \leftarrow 0$; $E \leftarrow 0$;

26 return $F_t^*$;
</div>

According to the theoretical guarantees in [34], the covariance approximation error of the sketch satisfies $\| X _ { t } ^ { \top } X _ { t } ~ -$ $\begin{array} { r } { B _ { t } ^ { \top } B _ { t } \| _ { 2 } \leq \frac { 1 } { L } \| X _ { t } \| _ { F } ^ { 2 } } \end{array}$ , indicating that a larger sketch size yields a more accurate approximation. To ensure the error does not exceed a predefined threshold $\eta ,$ the sketch size is set as:

$$
L \geq \left\lceil \frac {\| X _ {t} \| _ {F} ^ {2}}{\eta} \right\rceil = \left\lceil \frac {\sum_ {i = 1} ^ {T _ {0}} \| \mathbf {x} _ {i} \| _ {2} ^ {2}}{\eta} \right\rceil ,\tag{26}
$$

where $\begin{array} { r } { \sum _ { i = 1 } ^ { T _ { 0 } } \| \mathbf { x } _ { i } \| _ { 2 } ^ { 2 } } \end{array}$ is estimated from $T _ { 0 }$ warm-up snapshots per device. For example, if this value is approximately $1 0 ^ { 6 }$ and $\eta = 1 0 ^ { 3 }$ , then $L \ge 1 0 0 0$

To trace the approximation error, we define two parameters $E$ and $\delta .$ The cumulative energy counter E tracks the total squared ℓ<sub>2</sub>-norm of all snapshots observed in the streaming phase, i.e., $\begin{array} { r } { E = \sum _ { t } \| \mathbf { x } _ { t } \| _ { 2 } ^ { 2 } , } \end{array}$ providing a running estimate of $\| X _ { t } \| _ { F } ^ { 2 }$ without storing any raw data. The drift threshold δ defines the maximum tolerable fraction of structural information that may be discarded by cumulative FD shrinks before metric re-selection is triggered; setting $\delta = 1 / L$ ties this tolerance directly to the approximation error budget $\eta ,$ so that Trigger-2 fires at the same error level guaranteed by the sketch size.

Trigger-1 (Capacity Trigger). When the sketch $B _ { t }$ is full $\left( \mathrm { i } . \mathrm { e } . , \mathrm { } c > L \right)$ , it preserves the dominant covariance structure of the observed telemetry stream. METRICSELECTIONAND-SHRINK is invoked to perform metric re-selection and release sketch capacity.

Trigger-2 (Error-Driven Trigger). When $e / E > \delta$ before the sketch is full, the proportion of structural information discarded by cumulative FD shrinks has exceeded δ, signaling a distribution shift. Under a stable distribution, incoming snapshots align well with the sketch’s retained directions, so each FD shrink discards only a small $\sigma _ { \ell } ^ { 2 } ,$ keeping the ratio low. Under a shift, new snapshots introduce directions not captured by the current sketch, causing $\sigma _ { \ell } ^ { 2 }$ to spike, and $e / E$ to rise rapidly above δ.

After each invocation of METRICSELECTIONANDSHRINK, if $E > \eta \cdot L$ , the sketch is reinitialized with $L \gets \lceil E / \eta \rceil$ $\delta  1 / L$ , and counters reset $( c \gets 1 , e \gets 0 , E \gets 0 )$ , ensuring the approximation error bound remains valid as data volume grows.

Algorithm 1 summarizes the complete procedure. Each incoming packet produces a D-dimensional snapshot ${ \bf x } _ { t } ,$ which SEDMS matches to the corresponding device sketch via MAC address. Upon either trigger, METRICSELECTIO-NANDSHRINK is invoked to perform metric re-selection on the current sketch, followed by an FD shrink to free sketch capacity for incoming snapshots.

## B. Applications and Discussion

SEDMS dynamically selects the most discriminative telemetry metrics from the complete metric set. Only the telemetry values corresponding to the selected metrics are exported to the cloud backend for downstream monitoring tasks such as clustering-based traffic identification and anomaly detection.

Unlike signature-based approaches that rely on predefined patterns over specific aggregation dimensions or features, clustering-based traffic identification using SEDMS-selected metrics groups packets by their similarity in the telemetry snapshot space. Since each snapshot captures statistics across multiple aggregation dimensions, statistical measures, and time scale, the resulting clusters reflect underlying communication behaviors across these complementary views, exposing suspicious patterns that may be hidden in any single dimension. Because the scheme does not need to know in advance whether the threat is a UDP flood, a port scan, or any other specific attack type, any traffic that deviates from dominant behavioral clusters can be detected, making the scheme less sensitive to attack variants.

Directed telemetry query schemes such as Sonata require operators to predefine which telemetry metrics to monitor, making them may effective for known threat scenarios. In contrast, SEDMS identifies discriminative metrics based solely on the statistical structure of the data, offering greater flexibility against traffic evolving and threats. However, SEDMS requires access to all D candidate metrics before selection, which may be challenging when certain metrics are costly to collect or unavailable on some devices.

## VII. EXPERIMENTAL EVALUATION

We conduct experiments on four real-world network telemetry datasets to evaluate SEDMS in two downstream tasks, namely cluster-based traffic type identification and anomaly detection, answering the following research questions:

• Q1 (Hyperparameter Sensitivity): How sensitive is SEDMS to its hyperparameters and how should they be configured? (Section VII-B and Section VII-C)

• Q2 (Optimization Efficiency): How efficiently does SEDMS converge during iterative optimization? (Section VII-D)

• Q3 (Metric Selection Efficiency): How does SEDMS compare with state-of-the-art metric selection methods under varying metric selection ratios? (Section VII-E and Section VII-F)

• Q4 (Time Efficiency): Can SEDMS keep pace with streaming telemetry snapshots in real time? (Section VII-G)

• Q5 (Adaptability in Dynamic Environments): Can SEDMS robustly maintain high downstream performance in streaming scenarios? (Section VII-H)

## A. Experimental Setup

(1) Evaluation Scenarios. We evaluate SEDMS in two representative downstream scenarios in networks:

• Scenario 1: network traffic type identification, where unsupervised clustering is performed on per-packet telemetry snapshots using the selected metrics to distinguish different traffic types;

• Scenario 2: network anomaly detection, where the selected telemetry metrics are used to differentiate anomalous telemetry snapshots from the normal ones.

(2) Datasets Description. We conduct experiments on four real-world network telemetry datasets: IoT1 and IoT2 for Scenario 1, and KitsuneIoT1 and KitsuneIoT2 for Scenario 2, each with $D = 1 1 5$ telemetry metrics extracted per packet following Kitsune [9].

• IoT1, IoT2 [10]: These datasets contain traffic traces from the N-BaIoT dataset, collected from an Ennio Doorbell (IoT1) and a Provision PT-737E Security Camera (IoT2) during botnet attacks launched by the Gafgyt and Mirai families. IoT1 contains 5 classes (5 attack types from the Gafgyt family); IoT2 contains 10 classes (5 attack types from each of Gafgyt and Mirai).

• KitsuneIoT1, KitsuneIoT2 [9]: These traffic traces are captured from a video surveillance network. KitsuneIoT1 captures an SSL Renegotiation attack against an SSL-enabled surveillance camera, and KitsuneIoT2 captures a SYN DoS attack targeting a camera’s web server. Each trace contains two classes, normal and malicious traffic.

(3) Dataset Splitting. We employ distinct data-splitting strategies for the two evaluation scenarios, as each serves a distinct experimental objective.

• Scenario 1: Network Traffic Type Identification.

For the IoT1 and IoT2 datasets, we extract 100000 telemetry snapshots with proportional representation: the number of snapshots drawn from each traffic type matches its proportion in the original dataset. Each traffic type is independently split into 60%/20%/20% segments while preserving the within-type order. The corresponding segments from all traffic types are then concatenated sequentially to form the training, validation, and test sets, respectively.

Taking IoT1 as an example (5 Gafgyt attack types, denoted G-combo, G-junk, G-scan, G-tcp, and G-udp), the 100000 telemetry snapshots comprise: G-combo = 16755, G-junk = 9418, G-scan = 8887, $\mathrm { G } { \cdot } \mathrm { t c p } = 3 2 0 9 1$ , and $\mathrm { G - u d p } = 3 2 8 4 9$ consistent with the original proportions of the Ennio Doorbell trace. Each type is split 60/20/20 independently; for instance, the 16755 G-combo snapshots are divided into 10053 (training), 3351 (validation), and 3351 (test). The training set is then formed by concatenating the first 60% of G-combo, followed by the first 60% of G-junk, and so on through G-udp.

## • Scenario 2: Network Anomaly Detection.

For KitsuneIoT1 and KitsuneIoT2, we extract 100000 consecutive telemetry snapshots from each trace in strict temporal order. In each trace, the device first operates normally; the attack is then launched while normal traffic continues, producing a mixed stream of benign and malicious snapshots. Each sequence is divided into training (first 60%), validation (middle 20%), and test (final 20%) subsets. Since benign traffic precedes the attack, the training set consists entirely of normal snapshots, while both the validation and test sets contain a mixture of benign and malicious snapshots.

(4) Baseline Methods. We compare SEDMS with seven state-of-the-art metric selection algorithms. Among them, NetScope [26] and InfoSen [18] are dynamic filter-based methods that adapt metric selection over time, while InfUFS [17] and LScore [16] are static filter-based methods. SPCAFS [21], RUSLP [19], and OCLSP [33] are static embedded methods that require full access to the data. The details of these methods are described in Section II. Hyperparameters are tuned on the validation set, and all reported performance results are measured on the test set.

(5) Evaluation Platform. All experiments are conducted on a desktop machine equipped with an Intel<sup>®</sup> Core i5- 8300H CPU @2.30GHz and 32GB RAM. Each configuration is repeated 30 times, and the average performance is reported.

(6) Evaluation Indicators. To assess the discriminative power of the selected metrics, we adopt two widely used unsupervised algorithms for downstream tasks. We apply K-Means clustering on per-packet telemetry snapshots using the selected metrics to identify diverse network traffic types in Scenario 1, and deploy Isolation Forest for anomaly detection in Scenario 2. Although complex traffic identification algorithms like deep learning possess strong pattern recognition capabilities, their application often masks the true impact of the metric selection module, making it difficult to accurately evaluate the specific contribution of each metric.

For Scenario 1, cluster-based traffic type identification is evaluated using Clustering Accuracy (Clust-Acc), Normalized Mutual Information (NMI), and F-measure, defined as follows:

• Clustering Accuracy (Clust-Acc): Clust-Acc = $\begin{array} { r } { \frac { 1 } { N } \sum _ { i = 1 } ^ { N } f ( g _ { i } , \operatorname* { m a p } ( r _ { i } ) ) } \end{array}$ , where $g _ { i }$ and $r _ { i }$ are the ground-truth and cluster labels; map(·) is the optimal mapping via the Kuhn-Munkres algorithm [38]; $f ( a , b ) = 1 { \mathrm { ~ i f ~ } } a = b ,$ and 0 otherwise.

• NMI: $\begin{array} { r } { \mathbf { N M I } = \frac { I ( T , P ) } { \sqrt { H ( T ) \times H ( P ) } } } \end{array}$ , where T and P are groundtruth and predicted label sets, I(·) is mutual information, and $H ( \cdot )$ denotes entropy.

• F-measure: F-measure $\begin{array} { r l } { = } & { { } \frac { 2 \times \mathrm { P r e c i s i o n } \times \mathrm { R e c a l l } } { \mathrm { P r e c i s i o n } + \mathrm { R e c a l l } } } \end{array}$ , which balances precision and recall and reflects clustering quality comprehensively.

For Scenario 2, anomaly detection performance is evaluated using Anomaly Detection Accuracy (AD-Acc) and Anomaly Detection Recall (AD-Recall), defined as follows:

• Anomaly Detection Accuracy (AD-Acc): AD-Acc = $\frac { \mathrm { T P + T N } } { \mathrm { T P + T N + F P + F N } } .$ , where TP and TN denote the numbers of correctly detected anomalous and normal packets, respectively, while FP and FN denote the numbers of normal packets incorrectly identified as anomalous and anomalous packets incorrectly identified as normal, respectively.

• Anomaly Detection Recall (AD-Recall): AD-Recall = $\scriptstyle { \frac { \mathrm { T P } } { \mathrm { T P + F N } } }$ , the proportion of actual anomalous snapshots that are correctly detected.

## B. Discussion on the Setting of Matrix Sketch Size

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/0b441859abb1324543dd3dc1af60aebac8ea0a4c758a4dcf8066e8dfd87d5d78.jpg)  
Fig. 4: Evolution of cumulative energy $\begin{array} { r } { \| X \| _ { F } ^ { 2 } = \sum _ { i = 1 } ^ { t } \| \mathbf { x } _ { i } \| _ { 2 } ^ { 2 } } \end{array}$ with increasing per-packet telemetry snapshots across datasets.

The sketch size L controls the trade-off between memory efficiency and covariance approximation quality and is set via the condition in Eq. (26). We track the cumulative energy $\begin{array} { r } { \| X \| _ { F } ^ { 2 } = \sum _ { i = 1 } ^ { t } \| \mathbf { x } _ { i } \| _ { 2 } ^ { 2 } } \end{array}$ over warm-up snapshots, which exhibits roughly linear growth on all datasets. Taking IoT2 as an example, which exhibits the fastest energy growth among all datasets, the energy reaches $6 . 6 6 4 \times 1 0 ^ { 4 }$ at 5000 snapshots, yielding an estimated energy of $2 . 6 6 6 \times 1 0 ^ { 5 }$ at 20000 snapshots. With a target error threshold $\eta = 1 3 5$ , Eq. (26) gives $L \ge \lceil 2 . 6 6 6 \times 1 0 ^ { 5 } / 1 3 5 \rceil = 1 9 7 5$ , so we set $L = 2 0 0 0$ for IoT2. Following the same procedure, $L = 1 5 0 0$ suffices for IoT1, KitsuneIoT1, and KitsuneIoT2 due to their lower energy growth rates.

This analysis confirms that the sketch size L can be systematically determined via the condition in Eq. (26), guided by energy growth trends estimated from warm-up snapshots. The chosen values ensure high-quality covariance approximation with significant memory savings, making SEDMS well-suited for resource-constrained edge deployments.

## C. Parameter Sensitivity Analysis

In this subsection, we analyze the sensitivity of SEDMS to its key hyperparameters: $\alpha , ~ \beta , ~ \gamma _ { 1 }$ , and $\gamma _ { 2 } .$ Each of these parameters governs a different component of the optimization objective: α controls the influence of graph regularization, promoting local structure preservation; $\beta$ enforces row-wise sparsity in the projection matrix $W _ { B }$ , thereby guiding metric selection; $\gamma _ { 1 }$ imposes orthogonality constraints on $W _ { B } ;$ γ<sub>2</sub> balances the projection consistency term. To strictly enforce orthogonality, we empirically fix $\gamma _ { 1 } = 1 0 ^ { 7 }$ for all experiments. We then focus our analysis on the sensitivity of $\alpha , \beta ,$ and $\gamma _ { 2 } .$

## 1) Effect of Graph Regularization (α).

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/29a6d7d6929f5ce9460f4e7fc3c3d71e7d1a0396cc82974e1f433a8d9b6909ab.jpg)

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/957067f2755f0b9d07a242052550207d5cf0c78eed48e19f7e3b4f12e42630f6.jpg)  
(a) Clust-Acc  
(b) NMI

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/fb5bffa9ff05379df957b522eaf63d18177fb4f8f92c8fc23e17b164548bd95b.jpg)  
(c) F-measure  
Fig. 5: Effect of α on clustering performance in Scenario 1.

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/32d02c0357b1a63e68da390546a4afe7f2db59356d9492ac60a2bfafd8491cd0.jpg)  
(a) AD-Acc

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/d316d424c68485b11b794ee73677e63d37b188af9001a062a84fdf261d42ca5c.jpg)  
(b) AD-Recall  
Fig. 6: Effect of α on anomaly detection performance in Scenario 2.

Figures 5 and 6 show the impact of varying $\alpha \in$ {1, 50, 100, 500, 1000, 5000, 10000} on clustering performance in Scenario 1 and anomaly detection performance in Scenario 2 across different datasets. Overall, SEDMS exhibits strong robustness to α: despite a four-order-of-magnitude range from 1 to 10000, all evaluation metrics remain stable without significant degradation. In Scenario 1, for example, on the IoT1 dataset, the best performance is achieved at $\alpha = 5 0 0 0$ with Clust-Acc = 0.921, $\mathbf { N M I } \ = \ 0 . 8 8 3$ , and F-measure = 0.922; even at $\alpha = 1 0 0$ , these scores only slightly decrease but remain competitive (Clust-Acc = 0.851, $\mathbf { N M I } = 0 . 8 3 8 .$ , Fmeasure = 0.864). In Scenario 2, AD-Acc and AD-Recall vary within a narrow range of 0.94–0.99 on both KitsuneIoT1 and KitsuneIoT2. This robustness across both scenarios suggests that the tuned hyperparameters are reasonable. Based on these observations, we set $\alpha = 5 0 0 0$ for IoT1 and IoT2, $\alpha = 1 0 0$ for KitsuneIoT1, and $\alpha = 1 0 0 0$ for KitsuneIoT2.

## 2) Effects of Sparsity and Projection Consistency (β and γ<sub>2</sub>).

Figures 7 and 8 show the effects of different combinations of $\bar { \beta ~ } \in ~ \{ 1 0 ^ { 0 } , 1 0 ^ { 1 } , . . . , 1 0 ^ { 4 } \}$ and $\gamma _ { 2 } ~ \in ~ \{ 1 0 ^ { 1 } , 1 0 ^ { 2 } , \dots , 1 0 ^ { 5 } \}$ in both scenarios. The hyperparameter $\beta$ controls the tradeoff between sparsity and informativeness. Specifically, low $\beta$ values allow more telemetry metrics to be included, which may improve accuracy at the cost of reduced sparsity, whereas high β values enforce greater sparsity, which may degrade performance if too many informative metrics are removed. For $\gamma _ { 2 } ,$ a large value (e.g., $1 0 ^ { 4 }$ or $1 0 ^ { 5 } )$ places greater weight on projection consistency.

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/71e52876f8f586bca13cfdf6ec1362e18e5ec42f830edb28d354051907753a25.jpg)  
(a) Clust-Acc on IoT1

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/8fd7c5aa20754a77cb32d28f619db234ca3faa4d700475cc0964f1f5dfdc055a.jpg)  
(b) Clust-Acc on IoT2

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/b13f96168caccb80f8ffa4c49fd7297a717a80090ec8bed6b4daf563dd498f0f.jpg)

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/2d8a639ad4cdb8509e6f99f6755fa553559bfb7487126a25dc4d242482415ddd.jpg)  
(d) NMI on IoT2

(c) NMI on IoT1  
![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/557a06fa76d28b45416a06bf48fb7ac4ed51d015e227afc7025deb49a525200b.jpg)

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/7d89c86eacd2e91649e9dd8f948bf23cc1f42cc616f451f60e7df03e70a2e637.jpg)  
(e) F-measure on IoT1  
(f) F-measure on IoT2  
Fig. 7: Impact of $\beta$ and $\gamma _ { 2 }$ on clustering performance in Scenario 1.

In Scenario 1, the optimal $( \beta , \gamma _ { 2 } )$ settings are $\begin{array} { r l } { ( \beta } & { { } = } \end{array}$ $1 0 0 , \gamma _ { 2 } = 1 0 ^ { 5 } )$ for IoT1, achieving an F-measure of 0.919, and $( \beta = 1 0 0 , \gamma _ { 2 } = 1 0 ^ { 4 } )$ for IoT2, achieving an F-measure of 0.648. In Scenario 2, the optimal settings are $( \beta = 1 0 0 0 , \gamma _ { 2 } =$ $1 0 ^ { 5 } )$ for KitsuneIoT1, achieving an AD-Acc of 0.980, and $( \beta = 1 0 , \gamma _ { 2 } = 1 0 ^ { 5 } )$ for KitsuneIoT2, achieving an AD-Acc of 0.984. Overall, as $\beta$ and $\gamma _ { 2 }$ vary, the evaluation metrics tend to move in the same direction: they generally improve or degrade together, with no case where one metric remains high while another degrade drastically. This consistency across metrics suggests that the tuned hyperparameters are reasonable.

## D. Convergence Behavior

To assess optimization efficiency, we monitor the objective function value over 40 iterations. As shown in Figure 9, SEDMS converges rapidly across all datasets. For instance, on IoT1, the objective value drops substantially from $9 . 7 \times 1 0 ^ { 5 }$ within 20 iterations. This demonstrates that the alternating update strategy effectively minimizes the loss and captures the essential structure of the data in a few iterations.

Percentage of selected metrics

Percentage of selected metrics  
![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/a4ac0514aa4101ab92928ce3e6148476d6d9b05826c5b97fa43f312c0b452431.jpg)  
(a) AD-Acc on KitsuneIoT1

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/e5b83770921699dc36e210e5fab2ed8dd156637f093e6f37ced44881ba719a86.jpg)  
(b) AD-Acc on KitsuneIoT2

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/c3b400cbb6d2aecb505c693a844f1049413807903eac1c171d4fa75f115959d8.jpg)  
(c) AD-Recall on KitsuneIoT1

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/6307ad66e9091c4d14ab56f3f91c4cc4b05c20fab4e688acc1af07be892e1af4.jpg)  
(d) AD-Recall on KitsuneIoT2

Fig. 8: Impact of $\beta$ and $\gamma _ { 2 }$ on anomaly detection performance in Scenario 2.  
![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/1d25b31cfc42e9b5ca3fb41b79cd5581f8d4f690ff216bbd5004cac1f010b8a1.jpg)  
(a) IoT1

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/2f15accf4231e79843081ac3fea3d6574bb67cea7c9425d1d19c1639fbd9bfb6.jpg)

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/0ce7314fcbb1877d0f1288104e9339957dbca0cf94e68cc7a8eb04566d18343a.jpg)

(b) IoT2  
![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/5f22aca279c022208026907410dac1bd984679fc7841c9e94b7ff142868ed8e7.jpg)  
(c) KitsuneIoT1  
(d) KitsuneIoT2  
Fig. 9: Convergence of the objective function in Eq. (16) across datasets.

## E. Performance Comparison Under Different Metric Selection Ratios

In this subsection, we evaluate SEDMS under varying metric selection ratios from 10% to 100% (i.e., all metrics) and compare it with state-of-the-art methods. This analysis reveals how the number of selected metrics affects downstream task performance and highlights the trade-off between discrimination quality and bandwidth overhead on resource-constrained edge gateways. For Scenario 1, we report clustering results in terms of Clust-Acc, NMI, and F-measure on IoT1 and IoT2. For Scenario 2, we report anomaly detection results in terms of AD-Acc and AD-Recall on KitsuneIoT1 and KitsuneIoT2. As shown in Figures 10 and 11, we summarize the key observations across both scenarios as follows:

<table><tr><td></td><td>SEDMS</td><td>LScore</td><td>SPCAFS</td><td>RUSLP</td></tr><tr><td></td><td>OCLSP</td><td>InfUFS</td><td>NetScope</td><td>InfoSen</td></tr></table>

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/63b58a9de8e9abf39c1f91afff7d4965d6db87f4b11bb47a7755d8dd37b6f25a.jpg)

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/c229273e2b786a74cde414f74397c55a4d9feac02afdf059237e2d272feb0220.jpg)  
Percentage of selected metrics  
(b) Clust-Acc on IoT2

(a) Clust-Acc on IoT1  
![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/9e740e7f430e70f63e2535ea63a031207dbf376f958c2c37b55f08d2d8c0df8d.jpg)  
(c) NMI on IoT1

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/4930e0a6df41a58c299c1dc4f9d685357cff6c160ddf1aa9596b809cd4158ec3.jpg)  
(d) NMI on IoT2

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/849db2138197b3b5b3a4b9e27c9e8f96377c11f74bfe786c3b9154fbaf6f2ca7.jpg)

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/95fcb605542318c340f4ffccc3ef0a38c9f5aaa2aece66a4fb6795f1c2ad275b.jpg)  
(e) F-measure on IoT1  
(f) F-measure on IoT2  
Fig. 10: Comparison of clustering performance under different metric selection ratios in Scenario 1.

1) Performance Trends. In Scenario 1, Clust-Acc, NMI, and F-measure all improve as the metric selection ratio increases, but performance tends to level off or slightly decrease beyond a certain threshold, possibly due to redundant metrics. The same trend holds in Scenario 2: AD-Acc and AD-Recall increase with more metrics but yield no further improvement once each method reaches its optimal ratio.

2) Optimal Selection Ratios. The optimal selection ratio for each method is summarized in Table II. In Scenario 1, SEDMS achieves its best performance at 40% on IoT1 and 70% on IoT2. For example, on IoT2, Clust-Acc increases from 0.490 at 10% to 0.660 at 70%, but drops slightly to 0.648 at 100%. In Scenario 2, SEDMS reaches its best AD-Acc of 0.974 and AD-Recall of 0.987 at 40% on KitsuneIoT1, and its best AD-Acc of 0.984 at 30% on KitsuneIoT2, both comparable to full-metric performance.

3) Comparison with Full Metrics. Using 100% metrics does not necessarily yield the best performance. In Scenario 1, on IoT1, SEDMS achieves its highest F-measure of 0.904 at 40%, while the score drops to 0.875 at 100%. On IoT2, SEDMS reaches a peak NMI of 0.748 at 70%, with almost no improvement at 100%. In Scenario 2, on KitsuneIoT1, SEDMS achieves near-identical detection performance at 40% compared to 100%, confirming that a carefully selected compact subset is more effective than using all metrics.

(d) AD-Recall on kitsuneIoT2

<table><tr><td></td><td>SEDMS</td><td>LScore</td><td>SPCAFS</td><td>RUSLP</td></tr><tr><td></td><td>OCLSP</td><td>InfUFS</td><td>NetScope</td><td>InfoSen</td></tr></table>

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/299894d92e66b4c45a5e9134b86312984ef41d4f5007d7ab38b616aae2a9e1cd.jpg)  
Percentage of selected metrics

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/1fddef8df56750203d693f0b0d8c2027ce5fb0414bede78426fd355ddaf59399.jpg)  
Percentage of selected metrics

(a) AD-Acc on kitsuneIoT1  
(b) AD-Acc on kitsuneIoT2  
![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/1b4cc0bb4670fcc268645807ac7a9e8f9ca645c4a26a319e46ddc416c7c1daf5.jpg)  
(c) AD-Recall on kitsuneIoT1

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/664398dc3df44b8e9eaecfb778d0692dc3a7be7397351be441cda73fdcc99957.jpg)  
Fig. 11: Comparison of anomaly detection performance under different metric selection ratios in scenario 2.

4) Comparison with Baselines. SEDMS consistently achieves competitive or superior performance with fewer metrics across both scenarios. In Scenario 1, on IoT1, SEDMS achieves a Clust-Acc of 0.903 at 40%, surpassing the secondranked OCLSP (0.875) and third-ranked NetScope (0.861). Notably, at the more aggressive ratio of 10%, SEDMS significantly outperforms all competing methods, demonstrating its ability to retain highly discriminative metrics under strict bandwidth constraints. In Scenario 2, on KitsuneIoT1 at 40%, the top four methods ranked by AD-Acc are SEDMS (0.974), OCLSP (0.974), InfoSen (0.968), and NetScope (0.962), confirming that SEDMS consistently selects the most discriminative metrics across both tasks.

## F. Comparison of Optimal Metric Selection Ratios

TABLE II: Optimal Metric Selection Ratios

<table><tr><td rowspan="2">Method</td><td colspan="2">Scenario 1</td><td colspan="2">Scenario 2</td></tr><tr><td>IoT1</td><td>IoT2</td><td>KitsuneIoT1</td><td>KitsuneIoT2</td></tr><tr><td>SEDMS</td><td>40%</td><td>70%</td><td>40%</td><td>30%</td></tr><tr><td>LScore</td><td>100%</td><td>100%</td><td>90%</td><td>80%</td></tr><tr><td>SPCAFS</td><td>60%</td><td>70%</td><td>60%</td><td>60%</td></tr><tr><td>RUSLP</td><td>60%</td><td>70%</td><td>50%</td><td>40%</td></tr><tr><td>OCLSP</td><td>40%</td><td>70%</td><td>40%</td><td>30%</td></tr><tr><td>InfUFS</td><td>60%</td><td>70%</td><td>60%</td><td>40%</td></tr><tr><td>NetScope</td><td>40%</td><td>70%</td><td>50%</td><td>40%</td></tr><tr><td>InfoSen</td><td>50%</td><td>70%</td><td>50%</td><td>50%</td></tr></table>

Based on the performance curves in Figure 10-Figure 11, we summarize the optimal metric selection ratio for each method across different downstream tasks and datasets in Table II. The optimal ratio is defined as the smallest ratio at which a method achieves its best downstream task performance, i.e., the point beyond which adding more metrics yields no further improvement. Several observations are summarized as follows:

1) More traffic types require higher selection ratios. As the number of traffic types increases, more metrics are InfUFS NetScope InfoSenneeded to capture the greater structural differences among them. In Scenario 1, IoT1 contains 5 traffic types while IoT2 contains 10 traffic types spanning two distinct attack families. As shown in Table II, most methods require a higher optimal selection ratio on IoT2 than on IoT1. For example, both SEDMS and OCLSP increase from 40% on IoT1 to 70% on IoT2. In contrast, Scenario 2 focuses on distinguishing anomalous traffic from normal traffic, and SEDMS requires only 30%–40% across both KitsuneIoT1 and KitsuneIoT2 datasets, further confirming that fewer traffic types demand fewer metrics.

2) SEDMS and OCLSP require the fewest metrics. Among all compared methods, SEDMS and OCLSP consistently require the fewest metrics to reach their best performance. A lower selection ratio directly translates to fewer metric values uploaded per telemetry snapshot, yielding greater bandwidth savings for resource-constrained edge gateways. However, SEDMS incurs significantly lower computational overhead than OCLSP, as shown in Table III, making it more practical for real-time edge deployment.

## G. Comparison of Time Overhead

TABLE III: Processing Throughput and Latency

<table><tr><td rowspan="3">Method</td><td colspan="4">Throughput (snapshots/s)</td><td colspan="2">Avg. Latency (ms)</td></tr><tr><td colspan="2">Scenario 1</td><td colspan="2">Scenario 2</td><td rowspan="2">Scenario 1</td><td rowspan="2">Scenario 2</td></tr><tr><td>IoT1</td><td>IoT2</td><td>KitsuneIoT1</td><td>KitsuneIoT2</td></tr><tr><td>SEDMS</td><td>5597</td><td>5495</td><td>5606</td><td>5729</td><td>0.18</td><td>0.18</td></tr><tr><td>LScore</td><td>272</td><td>260</td><td>284</td><td>263</td><td>3.76</td><td>3.66</td></tr><tr><td>SPCAFS</td><td>8287</td><td>8876</td><td>8647</td><td>8602</td><td>0.12</td><td>0.12</td></tr><tr><td>RUSLP</td><td>469</td><td>470</td><td>484</td><td>454</td><td>2.13</td><td>2.13</td></tr><tr><td>OCLSP</td><td>14</td><td>13</td><td>14</td><td>14</td><td>74.18</td><td>71.43</td></tr><tr><td>InfUFS</td><td>35012</td><td>35714</td><td>35992</td><td>36118</td><td>0.03</td><td>0.03</td></tr><tr><td>NetScope</td><td>10791</td><td>10135</td><td>10597</td><td>10706</td><td>0.10</td><td>0.09</td></tr><tr><td>InfoSen</td><td>6550</td><td>6466</td><td>6543</td><td>6781</td><td>0.15</td><td>0.15</td></tr></table>

To validate the time efficiency of SEDMS, we report the processing throughput (in snapshots/s) at each method’s optimal selection ratio in Table III, along with the corresponding average per-snapshot latency derived as the reciprocal of throughput. We observe the following:

1) Throughput Analysis. The five most efficient methods in terms of throughput are InfUFS, NetScope, SPCAFS, InfoSen, and SEDMS. Our SEDMS achieves a throughput of approximately 5500–5750 snapshots/s across all datasets, corresponding to an average latency of 0.18 ms per snapshot. In contrast, OCLSP achieves only 13–14 snapshots/s with a latency exceeding 70 ms, approximately 400× slower than SEDMS, making it impractical for real-time edge deployment.

2) Comprehensive Advantages of SEDMS. While InfUFS, NetScope, SPCAFS, and InfoSen achieve higher throughput than SEDMS, they generally require higher optimal metric selection ratios as shown in Table II, resulting in greater uplink bandwidth consumption. Moreover, in Figures 10 and 11, their discrimination performance degrades significantly at low selection ratios compared to SEDMS in both scenarios. SEDMS therefore offers the best trade-off among throughput, bandwidth efficiency, and downstream task performance.

## H. Dynamic Metric Selection under Evolving Traffic Distributions

A key feature of SEDMS is its ability to continuously adapt to evolving metric importance via compact matrix sketching and a dynamic update mechanism. This subsection evaluates the stability of SEDMS under evolving traffic distributions. We fix the metric selection ratios as follows: 40% for IoT1, 70% for IoT2, 40% for KitsuneIoT1, 30% for KitsuneIoT2. SEDMS, NetScope, and InfoSen dynamically update their selected metric subsets, while the remaining baselines use a static subset obtained from an initial data batch.

For Scenario 1, each dataset is formed by concatenating different traffic types sequentially. As the packet sequence progresses, both the dominant traffic type and the secondary types shift, causing the data distribution to evolve continuously. For example, IoT2 comprises 10 traffic types spanning two attack families; the dominant type transitions from Gafgyt-combo to Gafgyt-tcp and then to Mirai-udp, while the secondary types shift accordingly from Gafgyt variants to Mirai variants. For brevity, Gafgyt and Mirai attack types are prefixed with G- and M- respectively (e.g., G-combo, G-tcp, M-udp) in the figures throughout this section.

Figure 12 shows the changes in Clust-Acc, NMI, and Fmeasure as the traffic composition evolves over the packet sequence in Scenario1. We observe the following:

1) Degradation of Static Methods. At the early streaming stage, static and dynamic methods perform similarly since all methods use the same initial telemetry snapshots for metric selection. As the dominant type shifts, e.g., shifts from Gcombo to G-udp, static methods (SPCAFS, RUSLP, OCLSP, LScore, and InfUFS) exhibit clear performance degradation. Their fixed metric subsets become misaligned with the current data distribution, leading to declines in per-packet telemetry snapshot type discrimination performance. This degradation is particularly pronounced on IoT2, where the transition crosses two distinct attack families.

2) Stability of SEDMS. In contrast, SEDMS maintains stable and consistently high discrimination performance over time, for example, On IoT1, Clust-Acc remains above 0.89 across all evaluation points despite the shift from G-combo to G-udp. Its error-driven update mechanism continuously refreshes the selected metric subset, ensuring that the most informative telemetry metrics are retained.

3) Slightly Outperforming Dynamic Methods. Compared to dynamic baselines (NetScope and InfoSen), SEDMS achieves slightly higher and more stable performance across both datasets. More importantly, as shown in Figure 10, SEDMS achieves this performance with fewer metrics, meaning that SEDMS provides greater bandwidth savings while maintaining superior discrimination quality under evolving traffic distributions.

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/dc7580c45722e8ffb7c3f38bd5c60139574887be1a92a5b55edafbdbbeb06c5d.jpg)

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/ed854ba3b0628c31185a749d4e37280c61c674a831987589d0d85c7d60b6a2c5.jpg)  
(b) Clust-Acc on IoT2

(a) Clust-Acc on IoT1  
![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/5c5c599f27b3dfa8410cbd4b87ec947ae7f296302ba1bcd584f1eb2da4eccf66.jpg)

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/6f072c033b245a86990422e61dea8973e1e47d5fb69d141bc702e93a8fed347d.jpg)

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/9f7ade1441152baf42a11198a03b52d21817280bee81e145b5b6bf472c25b003.jpg)  
(e) F-measure on IoT1

(d) NMI on IoT2  
![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/cfb86a4d03a453e277b3cb28d563956deca7db4adcb5476b2eb96dde1d4d94d2.jpg)  
(d) F-measure on IoT2  
Fig. 12: Comparison of clustering performance under evolving traffic distributions in Scenario 1.

Unlike Scenario 1, in Scenario 2 the SSL Renegotiation attack coexists with normal traffic, i.e., benign and malicious snapshots are continuously interleaved, resulting in a relatively stable mixture of benign and malicious snapshots across the packet sequence.

Figure 13 shows the AD-Acc and AD-Recall over the packet sequence in Scenario 2. Since benign and malicious snapshots are continuously interleaved throughout the test period, the data distribution remains relatively stable, and all methods exhibit only minor fluctuations without significant degradation. This demonstrates that SEDMS maintains consistent detection quality over an extended mixed traffic stream without performance drift. Among them, SEDMS, OCLSP, and InfoSen consistently rank as the top three, which is consistent with the results in Figure 11, further confirming that SEDMS selects the most discriminative metrics for anomaly detection under resource-constrained conditions.

Summary. SEDMS demonstrates strong adaptability and stability in dynamic streaming telemetry scenarios. By continuously updating the selected metric subset based on incoming telemetry snapshots, it outperforms both static and dynamic baseline methods, making it well-suited for resourceconstrained edge gateways where traffic evolves over time.

<table><tr><td></td><td>SEDMS</td><td>LScore</td><td>SPCAFS</td><td>RUSLP</td></tr><tr><td></td><td>OCLSP</td><td>InfUFS</td><td>NetScope</td><td>InfoSen</td></tr></table>

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/2ee4aae35a635be1355abeeccc3774930c6bc568a62d15c55412b6a51c11d335.jpg)  
(a) AD-Acc on KitsuneIoT1 benign and malicious

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/fc902abec368c71ea6507e2ea43f047923d612f88b2551300fc2d82e5655ef6d.jpg)  
(b) AD-Acc on KitsuneIoT2

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/e286bf17adfdb550b336a625e94267813f3c1fb0181bf381d14a3dca1ca97b3e.jpg)  
(c) AD-Recall on  
KitsuneIoT1

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/7b68e96b898914bfd46bdee61e5a2a4be28be0f037fc5418985f9bd87941f31d.jpg)  
(d) AD-Recall on  
KitsuneIoT2  
Fig. 13: Comparison of anomaly detection performance under evolving traffic distributions in Scenario 2.

## VIII. CONCLUSION

This paper presents SEDMS, a space-efficient framework for dynamic metric selection from high-dimensional streaming telemetry in resource-constrained edge networks. SEDMS addresses limited memory and time-varying metric relevance via a bounded-memory matrix sketch, a spectral-sparse optimization model, and a lightweight dynamic update strategy, with theoretical guarantees on approximation error. Experiments on real-world datasets show that SEDMS reduces metric dimensionality by 30–70% while maintaining competitive clusteringbased traffic identification and anomaly detection performance, and adapts to evolving traffic distributions with low overhead, making it suitable for scalable edge monitoring. The source code is available at: https://github.com/SyCode2005/SEDMS.

## REFERENCES

[1] J. Xiao, Y. Chen, C. Yang, K. Li, K. Xie, X. Li, K. Li, and W. Liang, “Communication-efficient federated learning based on a two-stage adaptive basis matrix for gradient compression,” IEEE Transactions on Mobile Computing, vol. 25, no. 10, pp. 18 403–18 420, 2026.

[2] L. Yang, D. M. Manias, and A. Shami, “Pwpae: An ensemble framework for concept drift adaptation in iot data streams,” in IEEE Globecom 2021. IEEE, 2021, pp. 01–06.

[3] A. Pashamokhtari, N. Okui, M. Nakahara, A. Kubota, G. Batista, and H. H. Gharakheili, “Dynamic inference from iot traffic flows under concept drifts in residential isp networks,” IEEE Internet of Things Journal, vol. 10, no. 17, pp. 15 761–15 773, 2023.

[4] Y. Cong, K. Xie, J. Wen, J. Zhang, Y. Yin, Q. Zhang, G. Xie, and W. Liang, “Per-packet traffic measurement in storage, computation and bandwidth limited data plane,” IEEE/ACM Transactions on Networking, vol. 32, no. 5, pp. 3730–3742, 2024.

[5] F. Gong, D. Raghunathan, A. Gupta, and M. Apostolaki, “Zoom2net: Constrained network telemetry imputation,” in Proceedings of the ACM SIGCOMM 2024 Conference, 2024, pp. 764–777.

[6] A. G. Alcoz, M. Strohmeier, V. Lenders, and L. Vanbever, “Aggregatebased congestion control for pulse-wave ddos defense,” in Proceedings of the ACM SIGCOMM 2022 Conference, 2022, pp. 693–706.

[7] S. Pei, J. Wen, K. Xie, G. Xie, and K. Li, “On-line network traffic anomaly detection based on tensor sketch,” IEEE Transactions on Parallel and Distributed Systems, vol. 34, no. 12, pp. 3028–3045, 2023.

[8] S. He, G. Li, K. Xie, and P. K. Sharma, “Fusion graph structure learningbased multivariate time series anomaly detection with structured prior knowledge,” IEEE Transactions on Information Forensics and Security, vol. 19, pp. 8760–8772, 2024.

[9] Y. Mirsky, T. Doitshman, Y. Elovici, and A. Shabtai, “Kitsune: An ensemble of autoencoders for online network intrusion detection,” in 25th Annual Network and Distributed System Security Symposium, NDSS 2018, 2018.

[10] Y. Meidan, M. Bohadana, Y. Mathov, Y. Mirsky, A. Shabtai, D. Breitenbacher, and Y. Elovici, “N-baiot—network-based detection of iot botnet attacks using deep autoencoders,” IEEE Pervasive Computing, vol. 17, no. 3, pp. 12–22, 2018.

[11] H. Ji, K. Xie, J. Wen, Q. Zhang, G. Xie, and W. Liang, “Finemon: An innovative adaptive network telemetry scheme for fine-grained, multi-metric data monitoring with dynamic frequency adjustment and enhanced data recovery,” Proceedings of the ACM on Management of Data, vol. 2, no. 1, pp. 1–26, 2024.

[12] Z. Liu, H. Namkung, G. Nikolaidis, J. Lee, C. Kim, X. Jin, V. Braverman, M. Yu, and V. Sekar, “Jaqen: A high-performance switch-native approach for detecting and mitigating volumetric ddos attacks with programmable switches,” in 30th USENIX Security Symposium (USENIX Security 21), 2021, pp. 3829–3846.

[13] Z. Xi, Y. Zhou, D. Zhang, K. Gao, C. Sun, J. Cao, Y. Wang, M. Xu, and J. Wu, “Newton: Intent-driven network traffic monitoring,” IEEE/ACM Transactions on Networking, vol. 30, no. 2, pp. 939–952, 2021.

[14] A. Gupta, R. Harrison, M. Canini, N. Feamster, J. Rexford, and W. Willinger, “Sonata: Query-driven streaming network telemetry,” in Proceedings of the ACM SIGCOMM 2018 Conference, 2018, pp. 357– 371.

[15] C. Yao, Y.-F. Liu, B. Jiang, J. Han, and J. Han, “Lle score: A new filter-based unsupervised feature selection method based on nonlinear manifold embedding and its application to image recognition,” IEEE Transactions on Image Processing, vol. 26, no. 11, pp. 5257–5269, 2017.

[16] X. He, D. Cai, and P. Niyogi, “Laplacian score for feature selection,” Advances in neural information processing systems, vol. 18, 2005.

[17] G. Roffo, S. Melzi, U. Castellani, A. Vinciarelli, and M. Cristani, “Infinite feature selection: a graph-based feature filtering approach,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 43, no. 12, pp. 4396–4410, 2021.

[18] Z. Xu, Z. Lu, and Z. Zhu, “Information-sensitive in-band network telemetry in p4-based programmable data plane,” IEEE/ACM Transactions on Networking, 2024.

[19] C. Luo, J. Zheng, T. Li, H. Chen, Y. Huang, and X. Peng, “Orthogonally constrained matrix factorization for robust unsupervised feature selection with local preserving,” Information Sciences, vol. 586, pp. 662–675, 2022.

[20] X. Huang and X. Nie, “Multi-view feature selection for polsar image classification via $\ell _ { 2 , 1 }$ sparsity regularization and manifold regularization,” IEEE Transactions on Image Processing, vol. 30, pp. 8607–8618, 2021.

[21] Z. Li, F. Nie, J. Bian, D. Wu, and X. Li, “Sparse pca via $\ell _ { 2 , p }$ -norm regularization for unsupervised feature selection,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 45, no. 4, pp. 5322– 5328, 2023.

[22] T. Yang, J. Jiang, P. Liu, Q. Huang, J. Gong, Y. Zhou, R. Miao, X. Li, and S. Uhlig, “Elastic sketch: Adaptive and fast network-wide measurements,” in Proceedings of the ACM SIGCOMM 2018 Conference, 2018, pp. 561–575.

[23] C. Misa, W. O’Connor, R. Durairajan, R. Rejaie, and W. Willinger, “Dynamic scheduling of approximate telemetry queries,” in 19th USENIX Symposium on Networked Systems Design and Implementation (NSDI 22), 2022, pp. 701–717.

[24] C. Shou, R. Bhatia, A. Gupta, R. Harrison, D. Lokshtanov, and W. Willinger, “Query planning for robust and scalable hybrid network telemetry systems,” Proceedings ofthe ACM on Networking, vol. 2, no. CoNEXT1, pp. 1–27, 2024.

[25] J. Wen, S. Pei, C. Yan, K. Xie, and W. Liang, “Extensible bloom filters: Adaptive strategies for scalability and efficiency in network and distributed systems to handle increased data,” Tsinghua Science and Technology, vol. 30, no. 4, pp. 1846–1864, 2025.

[26] H. Chen, B. Wang, G. Yu, Z. He, P. Chen, C. Sun, and Z. Zheng, “Netscope: Fault localization in programmable networking systems with low-cost in-band network telemetry and in-network detection,” IEEE Transactions on Networking, 2025.

[27] J. Li, K. Cheng, S. Wang, F. Morstatter, R. P. Trevino, J. Tang, and H. Liu, “Feature selection: A data perspective,” ACM computing surveys (CSUR), vol. 50, no. 6, pp. 1–45, 2017.

[28] S. Maldonado and R. Weber, “A wrapper method for feature selection using support vector machines,” Information Sciences, vol. 179, no. 13, pp. 2208–2217, 2009.

[29] H. Peng, F. Long, and C. Ding, “Feature selection based on mutual information criteria of max-dependency, max-relevance, and minredundancy,” IEEE Transactions on pattern analysis and machine intelligence, vol. 27, no. 8, pp. 1226–1238, 2005.

[30] F. Nie, H. Huang, X. Cai, and C. Ding, “Efficient and robust feature selection via joint ℓ<sub>2,1</sub>-norms minimization,” Advances in neural information processing systems, vol. 23, 2010.

[31] R. Wang, C. Zhang, J. Bian, Z. Wang, F. Nie, and X. Li, “Sparse and flexible projections for unsupervised feature selection,” IEEE Transactions on Knowledge and Data Engineering, vol. 35, no. 6, pp. 6362–6375, 2022.

[32] M. Qian and C. Zhai, “Unsupervised feature selection for multi-view clustering on text-image web news data,” in Proceedings of the 23rd ACM international conference on conference on information and knowledge management, 2014, pp. 1963–1966.

[33] X. Lin, J. Guan, B. Chen, and Y. Zeng, “Unsupervised feature selection via orthogonal basis clustering and local structure preserving,” IEEE Transactions on Neural Networks and Learning Systems, vol. 33, no. 11, pp. 6881–6892, 2022.

[34] E. Liberty, “Simple and deterministic matrix sketching,” in Proceedings of the 19th ACM SIGKDD international conference on Knowledge discovery and data mining, 2013, pp. 581–588.

[35] M. Ghashami, E. Liberty, J. M. Phillips, and D. P. Woodruff, “Frequent directions: Simple and deterministic matrix sketching,” SIAM Journal on Computing, vol. 45, no. 5, pp. 1762–1792, 2016.

[36] Z. Huang, “Near optimal frequent directions for sketching dense and sparse matrices,” Journal ofMachine Learning Research, vol. 20, no. 56, pp. 1–23, 2019.

[37] D. Lee and H. S. Seung, “Algorithms for non-negative matrix factorization,” Advances in neural information processing systems, vol. 13, 2000.

[38] H. W. Kuhn, “The hungarian method for the assignment problem,” Naval research logistics quarterly, vol. 2, no. 1-2, pp. 83–97, 1955.

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/649e4dc04a64ca4a00e7197cb146e115755f6e8e46513a4edc92369a5f631bd8.jpg)

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/a14ebc9f4c3e7d0a1d9e307b4f03a3c3630904ac38f8a84b450aed8bbf676a54.jpg)

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/9ec8921cc34a8a4976a72eafb043a73ba8b71483caf463e1634f89fb5309c88b.jpg)

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/6d8e1d1ae14110027672d0de4be680d0e3f2d2ef17c59a9959029a0353537dbb.jpg)  
Shuyu Pei received the Ph.D. degree in computer science and technology from Hunan University, Changsha, China, in 2024. She is now a postdoctoral fellow at the College of Computer Science and Electronics Engineering, Hunan University. Her research interests include probabilistic data structures and anomaly detection over streaming data.

Jigang Wen received the Ph.D. degree in computer science and technology from Hunan University in 2013. He was a Post-Doctoral Scholar at Lehigh University from 2014 to 2016. He is currently a Professor and the Dean of the School of Computer Science and Engineering, Hunan University of Science and Technology, China. His research interests include blockchain security technology, networks security protection, embedded system and hardware IP protection.

Dafang Zhang received the Ph.D. degree in application mathematics from Hunan University, Changsha, China, in 1997. He is currently a Professor with Hunan University. His research interests include packet processing, Internet measurement, wireless network and mobile computing, and big data.

Yuxiang Chen received a PhD degree in computer application from Hunan University in 2021. He worked as a postdoctoral fellow in the Department of Computing at Hunan University from 2021.7 to 2023.3, and is currently an assistant professor at Hunan University of Science and Technology. His research interests include network monitoring, parallel computing, and AI.

Kun Huang received the Ph.D. degree from Hunan University in 2009. He is an associate professor at Pengcheng Laboratory, China. His research interests include programmable networks, datacenter networks, emerging networks, and network security.

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/4043137768d8f2bbf5470d74311803f14082035f3a1ec41a34a7d074883821ff.jpg)

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/985703b7ce8eb560c410f8a5862577aae766589c75eff78db6346ba73379e9dd.jpg)

Wei Liang received the Ph.D. degree in computer science and technology from Hunan University in 2013. He is currently a Professor and the Dean of the School of Computer Science and Engineering, Hunan University of Science and Technology, China. He has authored or coauthored more than 140 journal/conference papers. His research interests include blockchain security technology, networks security protection, and security management in wireless sensor networks (WSN).

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/6756f71bcef7937ce75549d751a11b03328a7dd9ed5171f30b241159b521aad4.jpg)

Kun Xie received the Ph.D. degree in computer application from Hunan University, Changsha, China, in 2007. She is currently a Professor with Hunan University. She has published over 170 articles in major journals and conference proceedings, including journals IEEE/ACM TON, IEEE TMC, IEEE TC, and conferences, including ACM SIGMOD, IEEE INFOCOM, and IEEE ICDCS. Her research interests include network measurement, network security, big data, and AI.

![](../01-mineru-output/2026-TON-SEDMS__Space-Efficient_Dynamic_Metric_Selection_for_Streaming_Telemetry_in_Edge_Networks/images/20464e94aaff2d2b97be13454a437c0b43ca4bb56bc6d4c61afba2c1a3b803eb.jpg)

Gaogang Xie received the B.S. degree in physics, the M.S. and Ph.D. degrees in computer science from Hunan University in 1996, 1999, and 2002, respectively. He is currently a Professor with the Computer Network Information Center (CNIC), Chinese Academy of Sciences (CAS), and the University of Chinese Academy of Sciences and the Vice President of CNIC. His research interests include Internet architecture, packet processing and forwarding, and Internet measurement.
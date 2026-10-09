# Dynamic Malicious Encrypted Traffic Detection via Temporal Knowledge Graph in Cloud-Edge Networks

Qilong Huang <sup>1</sup>, Zihao Wang <sup>1</sup>, Yuxiang Hu <sup>1,2,3,∗</sup>, Le Tian <sup>1,2,3</sup>, Yufei Zhu <sup>1</sup>, Menglong Li <sup>1,2,3</sup> <sup>1</sup>Information Engineering University

<sup>2</sup>Key Laboratory of Cyberspace Endogenous Safety&Security of Henan Province <sup>3</sup>Key Laboratory of Cyberspace Security, Ministry of Education of China

Abstract—Traditional centralized security is inadequate for Cloud-Edge Networks, where massive distributed traffic and widespread protocol encryption create severe security blind spots. Continuous monitoring of network traffic is essential to identify malicious encrypted activities such as lateral movement and zero-day attacks. Existing graph-based detection methods typically model network flows as static graphs, which fail to capture the temporal dynamics of traffic patterns and face severe scalability bottlenecks when processing massive streaming data at resource-constrained edge nodes. Furthermore, supervised models heavily rely on exhaustive labeled datasets that are impractical to maintain in highly dynamic environments. To address these limitations, we propose TKG-ETA, a self-supervised Temporal Knowledge Graph (TKG) neural network equipped with an adaptive sketch mechanism for dynamic Encrypted Traffic Analysis in cloud-edge networks. We utilize a dynamically configurable sketch algorithm to efficiently compress and extract multi-dimensional statistical features from massive streaming traffic with minimal memory overhead, entirely bypassing payload inspection. These features are continuously transformed into a lightweight streaming TKG to model the fine-grained communication relations among network entities over time. Based on this temporal structure, we design a self-supervised time-aware message-passing mechanism to autonomously learn the evolutionary trajectories of normal encrypted traffic patterns without manual annotations. By capturing structural and temporal deviations, the proposed model accurately identifies malicious encrypted traffic. Extensive experiments on real-world network traffic datasets demonstrate that TKG-ETA achieves superior detection accuracy with an weighted F1 score exceeding 96% while maintaining the high throughput and low resource overhead imperative for cloud-edge collaborative deployment.

Index Terms—Cloud-Edge networks, encrypted traffic analysis, temporal knowledge graph, graph neural network, selfsupervised learning.

## I. INTRODUCTION

With the accelerated expansion of Cloud-Edge Networks [1], the distributed nature of modern computing [2] renders traditional centralized perimeter-based security models ineffective [3]. Massive heterogeneous devices connect and interact across network boundaries, generating voluminous distributed traffic. Concurrently, the widespread adoption of end-to-end encryption protocols protects user privacy but creates severe security blind spots. Advanced persistent threats and zeroday attacks increasingly disguise their malicious payloads within sequences of seemingly legitimate encrypted traffic.

Traditional payload-based Deep Packet Inspection (DPI) is computationally expensive and largely obsolete against encrypted threats, necessitating dynamic, flow-based behavioral analysis [4].

A critical requirement for malicious encrypted traffic detection in cloud-edge networks is the ability to model the spatiotemporal context of communications [5]. Viewed in isolation, a single encrypted flow from a compromised node performing lateral movement [6] may appear benign. The malicious intent only becomes evident when analyzing the historical trajectory and the structural dynamics over continuous time windows. Despite the proven efficacy of Graph Neural Networks (GNNs) in network anomaly detection [7], existing graph-based methods face critical limitations in cloud-edge collaborative environments. Most current approaches extract complex flow features through computationally expensive processing, creating severe scalability bottlenecks at resourceconstrained edge nodes. Furthermore, these methods typically model network flows as static and homogeneous graphs [8]. This static abstraction strips away critical temporal dynamics and heterogeneous semantics, leading to high false-positive rates in dynamic networks. Moreover, traditional supervised GNNs heavily rely on exhaustive labeled datasets, which is impractical to maintain as novel encrypted attack patterns frequently emerge [9].

To bridge these gaps, we propose TKG-ETA, a selfsupervised Temporal Knowledge Graph framework equipped with an adaptive sketch mechanism for encrypted traffic analysis. We utilize a dynamically configurable sketch algorithm to efficiently compress massive streaming traffic and extract statistical flow features with minimal memory overhead, completely bypassing payload dependency. Instead of relying on static graph snapshots, these features are continuously transformed into a lightweight streaming TKG, where events are modeled as temporal quadruples preserving sequential dynamics. Based on this, we introduce a time-aware message-passing mechanism optimized via self-supervised contrastive learning. By maximizing the mutual information between historical spatiotemporal context and current traffic embeddings, the model autonomously learns the intrinsic evolutionary trajectories of normal traffic patterns. Malicious encrypted activities are thus detected as structural and temporal deviations from these learned patterns without requiring manual labels.

The main contributions of this paper are summarized as follows:

• We formulate an adaptive sketch mechanism to efficiently compress massive streaming traffic and extract multidimensional statistical features, overcoming the scalability bottlenecks of DPI in resource-constrained cloud-edge environments.

• To capture the fine-grained semantics essential for detecting encrypted threats, we construct a lightweight streaming TKG that models complex cloud-edge network traffic as continuous heterogeneous quadruples.

• To eliminate the reliance on exhaustive labeled data, we design a framework integrating time-aware message passing with temporal contrastive learning to autonomously learn the spatiotemporal evolutionary trajectories of legitimate encrypted traffic.

• Extensive experiments on real-world datasets demonstrate that TKG-ETA significantly outperforms state-of-the-art baselines, achieving an F1-score exceeding 96% while maintaining extremely low resource overhead for edge deployment.

## II. RELATED WORK

## A. Graph-Based and Temporal Anomaly Detection

Traditional network anomaly detection typically relies on isolated flow statistics, struggling to identify sophisticated attacks. Recently, Graph Neural Networks (GNNs) have emerged as the dominant paradigm by capturing topological dependencies. For instance, Cui et al. [10] proposed a multiorder GNN to model high-order interactions. To preserve heterogeneous semantics, Zhou et al. [11] introduced a bipartite graph anomaly detection framework leveraging contrastive learning. However, these methods operate on static graph snapshots, fundamentally failing to capture the chronological evolution of network interactions. Temporal Knowledge Graphs (TKGs) address these limitations by modeling dynamically evolving multidimensional relations. Zhang et al. [12] explored an online anomaly detection mechanism over TKGs. Yet, existing TKG methods process raw topological updates directly, introducing massive memory overheads impractical for voluminous, high-speed streaming traffic typical of cloudedge environments.

## B. Encrypted Traffic Detection in Cloud-Edge Networks

In Cloud-Edge networks, the widespread adoption of encryption protocols necessitates flow-based behavioral analysis. Lin et al. [13] developed an anomaly detection approach based on the contextual semantics of behavior graphs to support dynamic network environments. By clustering benign behaviors in a self-supervised manner, they reduced false positives. Nevertheless, this behavior-context matching lacks an adaptive streaming extraction mechanism to cope with real-time traffic bursts. Focusing on the application layer, Souihi [14] integrated deep learning to detect anomalous

HTTP traffic. While achieving high detection rates, payloadbased deep packet inspection introduces significant latency and entirely fails against modern end-to-end encrypted traffic.

To overcome these limitations, our proposed TKG-ETA framework integrates an adaptive sketch mechanism to efficiently compress massive encrypted streaming traffic into temporal heterogeneous quadruples with minimal memory overhead, bypassing payload dependency.

## III. SYSTEM MODELING AND PROBLEM FORMULATION

This section formulates the dynamic encrypted traffic detection problem in cloud-edge networks. The physical network consists of heterogeneous edge devices and servers. The communications between them form continuous streaming encrypted traffic flows.

## A. Adaptive Sketch based Traffic Feature Extraction

To process massive streaming encrypted traffic with minimal memory overhead at resource-constrained edge nodes, we utilize an adaptive sketch mechanism. We dynamically adjust the number of hash functions d while keeping the total number of counters $M = d \times w$ constant based on the underlying traffic distribution, where w is the sketch width.

The traffic distribution variation is quantified using entropy:

$$
H = - \sum_ {i = 1} ^ {n} \frac {f _ {i}}{F} \log \frac {f _ {i}}{F}\tag{1}
$$

where $f _ { i }$ represents the size of the flow identifier $i ,$ and $\textstyle F = \sum _ { i = 1 } ^ { n } f _ { i }$ represents the total size of all flows. When the entropy change between consecutive time windows exceeds a threshold, a reconfiguration of the sketch parameters is triggered. Given $N$ measurement elements, the error between the estimated measurement value ${ \hat { f } } _ { i }$ and the true value $f _ { i }$ satisfies:

$$
\operatorname * {P r} \left[ \hat {f} _ {i} - f _ {i} \geq \frac {\delta N}{w} \right] \leq \delta^ {- d}\tag{2}
$$

where $\delta \ > \ 1$ . By letting $\delta \ = \ { \frac { \alpha } { d } }$ , the previous equation transforms into the precise error bound:

$$
\operatorname * {P r} \left[ \hat {f} _ {i} - f _ {i} \geq \frac {\alpha N}{M} \right] \leq \left(\frac {d}{\alpha}\right) ^ {d}\tag{3}
$$

## B. Streaming Temporal Knowledge Graph Construction

The statistical features extracted by the adaptive sketch without payload inspection are continuously transformed into a streaming Temporal Knowledge Graph, defined as a directed graph $\mathcal { G } = ( \mathcal { V } , \mathcal { E } , \mathcal { R } , \mathcal { T } )$ , where V is the entity node set, E is the temporal edge set, R is the relation set, and $\tau$ is the continuous time domain. Each encrypted communication event is represented as a temporal quadruple $( u , p , v , \tau ) \in \mathcal { E } .$ . Here, $u \in \mathcal V$ is the source node, $v \in \mathcal V$ is the destination node, $\tau \in \mathcal { T }$ is the timestamp, and $p \in \mathcal R$ encapsulates the extracted multi-dimensional flow features such as packet counts, byte counts, and flow rates.

Let $f _ { \theta }$ denote the TKG-ETA neural network model. For each incoming encrypted event $( u , p , v , \tau )$ , the model predicts its probability $P _ { n o r m } = f _ { \theta } ( u , p , v , \tau )$ of being a legitimate behavior. If $P _ { n o r m }$ falls below a dynamic threshold, the event is classified as malicious, mapping the deviation directly to a cumulative risk score for automated threat mitigation at the edge controller.

![](images/f04fc30db1d3a0168d3fefc5d17cded83944d493fb9e8ea5f59e8f47cc0a8181.jpg)  
Fig. 1. The overall architecture of the proposed TKG-ETA framework for dynamic malicious encrypted traffic detection in cloud-edge networks.

## IV. PROPOSED TKG-ETA METHODOLOGY

To bypass the limitations of traditional deep packet inspection on encrypted payloads, we propose the TKG-ETA framework. As illustrated in Fig. 1, the architecture continuously transforms extracted statistical features into temporal graph representations, subsequently identifying malicious encrypted traffic patterns via self-supervised contrastive learning.

## A. Time-Aware Message Passing for Encrypted Flows

After the adaptive sketch extracts multidimensional statistical features without inspecting payloads, these features are used to initialize the relation embeddings in our temporal knowledge graph. To effectively capture the highly dynamic topology of edge networks and the evolving context of encrypted communications, we design a time-aware messagepassing mechanism. This mechanism iteratively aggregates spatial neighborhood features while strictly preserving the chronological causality of network events.

Let $\Psi ( \tau )$ be a time encoding function that maps a continuous timestamp τ into a high-dimensional learnable vector space. This encoding is crucial for capturing the periodic burst patterns inherent in many encrypted IoT attacks such as DDoS attacks. For a target destination node v at time τ, the incoming message from a source node u under a specific communication property p is computed by concatenating the source’s historical state, the relation embedding $\mathbf { c } _ { p } ,$ and the temporal encoding $\Psi ( \tau )$ :

$$
\mu_ {u \rightarrow v} ^ {(k)} (\tau) = \mathbf {W} _ {m s g} ^ {(k)} \left[ \mathbf {x} _ {u} ^ {(k - 1)} (\tau^ {-}) \| \mathbf {c} _ {p} \| \Psi (\tau) \right]\tag{4}
$$

where $\mathbf { W } _ { m s g } ^ { ( k ) }$ represents the transformation weight matrix at the k-th message-passing layer, ∥ denotes vector concatenation, and $\mathbf { x } _ { u } ^ { ( k - 1 ) } ( \tau ^ { - } )$ is the hidden representation of node u just before time τ .

To consolidate the structural context, the target node v collects all incoming messages from its active historical neighborhood $\mathcal { N } ( v )$ . The aggregated neighborhood context is obtained via a permutation-invariant pooling function:

$$
\mathbf {x} _ {\mathcal {N} (v)} ^ {(k)} (\tau) = \operatorname{POOL} \left\{\mu_ {u \rightarrow v} ^ {(k)} (\tau) \mid u \in \mathcal {N} (v) \right\}\tag{5}
$$

Subsequently, the state of the destination node is updated by fusing its previous representation with the aggregated encrypted neighborhood context:

$$
\mathbf {x} _ {v} ^ {(k)} (\tau) = \operatorname{ReLU} \left(\mathbf {W} _ {u p d} ^ {(k)} \left[ \mathbf {x} _ {v} ^ {(k - 1)} (\tau^ {-}) \| \mathbf {x} _ {\mathcal {N} (v)} ^ {(k)} (\tau) \right]\right)\tag{6}
$$

By stacking K layers, the edge entities effectively perceive high-order spatiotemporal dependencies of the encrypted traffic flows.

## B. Self-Supervised Temporal Contrastive Learning

Obtaining accurately labeled datasets for zero-day encrypted attacks in cloud-edge environments is highly impractical. To overcome this, TKG-ETA employs a self-supervised contrastive learning objective, enabling the model to autonomously differentiate between legitimate communication trajectories and anomalous structural deviations.

For every valid encrypted communication event $( u , p , v , \tau )$ we construct an integrated temporal edge embedding by concatenating the final-layer node representations, the relation embedding, and the temporal context:

$$
\mathbf {y} _ {u, v} (\tau) = \mathbf {W} _ {p r o j} \left[ \mathbf {x} _ {u} ^ {(K)} (\tau) \parallel \mathbf {c} _ {p} \parallel \mathbf {x} _ {v} ^ {(K)} (\tau) \parallel \Psi (\tau) \right]\tag{7}
$$

Simultaneously, we generate a corrupted negative sample $( \tilde { u } , p , \tilde { v } , \tau )$ by randomly substituting either the source node u or the destination node v with an arbitrary node from the graph. The corresponding corrupted edge embedding is denoted as $\tilde { \mathbf { y } } _ { u , v } ( \tau )$

To establish a global spatiotemporal baseline for contrastive discrimination, we compute a global graph summary ${ \bf G } ( \tau )$ by aggregating all valid edge embeddings within the current observation window ${ \mathcal { E } } _ { \tau }$ :

$$
\mathbf {G} (\tau) = \sigma \left(\frac {1}{| \mathcal {E} _ {\tau} |} \sum_ {(u, p, v, \tau) \in \mathcal {E} _ {\tau}} \mathbf {y} _ {u, v} (\tau)\right)\tag{8}
$$

A learnable bilinear discriminator $f _ { d i s c }$ is utilized to score the mutual information between a given edge embedding and the global summary: $f _ { d i s c } ( \mathbf { y } , \mathbf { G } ) = \sigma ( \mathbf { y } ^ { \top } \mathbf { W } _ { b i l i n e a r } \mathbf { G } )$ The entire network is optimized using a binary cross-entropy formulation, forcing the model to maximize the score of valid encrypted patterns while minimizing the score of corrupted ones:

$$
\begin{array}{l} \mathcal {J} = - \frac {1}{2 | \mathcal {E} _ {\tau} |} \sum_ {\mathcal {E} _ {\tau}} \Big [ \log f _ {d i s c} (\mathbf {y} _ {u, v} (\tau), \mathbf {G} (\tau)) \\ \qquad + \log \big (1 - f _ {d i s c} (\tilde {\mathbf {y}} _ {u, v} (\tau), \mathbf {G} (\tau)) \big) \Big ] \end{array}\tag{9}
$$

## C. Automated Threat Scoring and Edge Mitigation

Once the self-supervised training phase converges, the bilinear discriminator $f _ { d i s c }$ acts as an automated threat scoring engine. For any newly arriving encrypted flow, the model projects its spatiotemporal attributes into the latent space and outputs a normality probability $P _ { n o r m } = f _ { d i s c } ( \mathbf { y } _ { u , v } ( \tau ) , \mathbf { G } ( \tau ) )$

A low $P _ { n o r m }$ indicates significant deviation from the benign evolutionary trajectories, strongly implying malicious intent disguised in the encrypted channel. To bridge detection and mitigation in the cloud-edge architecture, this probability is mapped to a continuous risk accumulation mechanism for the source entity u. The risk increment $\Delta R$ is formulated as max $\left\{ 0 , \beta ( \theta _ { b a s e } - P _ { n o r m } ) \right\}$ }, where $\theta _ { b a s e }$ is a strict decision boundary and $\beta$ is a scaling weight. The dynamic risk score of the node is updated as $R _ { u } = R _ { u } + \Delta R$ If $R _ { u }$ exceeds the system’s safety threshold, the edge controller immediately triggers network isolation for the compromised device.

## V. EXPERIMENTAL SIMULATION AND ANALYSIS

This section presents a comprehensive experimental evaluation of the proposed TKG-ETA framework. We aim to verify its detection superiority, robustness, and stability for encrypted traffic in resource-constrained cloud-edge environments.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: Dynamic Encrypted Traffic Detection via TKG-ETA

Input : Streaming encrypted flows at $\tau$, TKG $\mathcal{G}_{\tau}$, layers $K$
Output: Anomaly probability $P_{norm}$, Updated risk score $R_u$

for each observation window $\Delta\tau$ do

Calculate flow distribution entropy $H(\tau)$;

if entropy variation exceeds threshold then

Reconfigure adaptive sketch depth $d$;

Extract non-payload statistical features to initialize $c_p$;

for each node $n \in \mathcal{V}$ in $\mathcal{G}_{\tau}$ do

Update messages $\mu_{u \to v}^{(k)}(\tau)$ via Eq. 4;

Aggregate context $\mathbf{x}_{\mathcal{N}(v)}^{(k)}(\tau)$ via Eq. 5;

Update representations $\mathbf{x}_v^{(k)}(\tau)$ via Eq. 6;

for each training epoch do

Generate corrupted encrypted flow samples ($\tilde{u}, p, \tilde{v}, \tau$);

Construct embeddings $\mathbf{y}_{u,v}(\tau)$ and $\tilde{\mathbf{y}}_{u,v}(\tau)$ via Eq. 7;

Compute global summary $\mathbf{G}(\tau)$ via Eq. 8;

Update model parameters by minimizing loss $\mathcal{J}$ in Eq. 9;

for each incoming encrypted flow do

Evaluate probability $P_{norm} \leftarrow f_{disc}(\mathbf{y}_{u,v}(\tau), \mathbf{G}(\tau))$;

Calculate risk increment

$\Delta R \leftarrow \max \{0, \beta(\theta_{base} - P_{norm})\}$;

Increase source node risk $R_u \leftarrow R_u + \Delta R$;

return $P_{norm}, R_u$;
</div>

TABLE I

STATISTICS OF THE THREE NETFLOW BENCHMARKS AFTER PREPROCESSING.

<table><tr><td>Dataset</td><td>Train</td><td>Val</td><td>Test</td><td>Features</td><td>Attack (%)</td></tr><tr><td>UNSW-NB15</td><td>156,641</td><td>35,481</td><td>35,482</td><td>12</td><td>5.4</td></tr><tr><td>ToN-IoT</td><td>14,995</td><td>3,695</td><td>3,696</td><td>12</td><td>13.0</td></tr><tr><td>CIC-IoT2023</td><td>101,046</td><td>24,958</td><td>24,959</td><td>12</td><td>13.2</td></tr></table>

## A. Experimental Setup

1) Datasets: We select three publicly available network traffic benchmarks that collectively span diverse edge network environments and encrypted threat models: UNSW-NB15 [15], ToN-IoT [16], and CIC-IoT2023 [17]. Following standard practice, all datasets are preprocessed into an identical Net-Flow schema, which strictly relies on flow-level statistics without any payload inspection. This preprocessing naturally fits the encrypted traffic detection scenario where payload signatures are unavailable. Stratified random sampling is applied to UNSW-NB15 and ToN-IoT, while CIC-IoT2023 retains the full dataset. The detailed statistics after preprocessing are summarized in Table I.

2) Baselines and Evaluation Metrics: We compare TKG-ETA against three representative unsupervised and selfsupervised anomaly detection methods: Kitsune [18], Anomal-E [19], and NF [20]. To comprehensively assess detection performance and cloud-edge feasibility, we adopt Accuracy, F1-Score, Macro F1, Weighted F1, False Positive Rate (FPR), False Negative Rate (FNR), and AUC-ROC as evaluation metrics.

TKG-ETA (Ful ) w/o Time Encoding w/o Recon. Loss w/o Hard Negatives Anomal-E (Static)

TABLE II  
ANOMALY DETECTION PERFORMANCE ON THE THREE BENCHMARKS. ALL METRICS ARE REPORTED IN %. THE BEST RESULT ON EACH METRIC PERDATASET IS UNDERLINED.

<table><tr><td>Dataset</td><td>Method</td><td>Accuracy</td><td>F1</td><td>Macro F1</td><td>Weighted F1</td><td>FPR</td><td>FNR</td><td>AUC-ROC</td></tr><tr><td rowspan="4">UNSW-NB15</td><td>Kitsune</td><td>90.93</td><td>38.38</td><td>66.74</td><td>92.04</td><td>6.86</td><td>47.70</td><td>74.62</td></tr><tr><td>Anomal-E</td><td>88.43</td><td>48.29</td><td>70.89</td><td>91.05</td><td>12.23</td><td>0.00</td><td>98.83</td></tr><tr><td>NF</td><td>90.61</td><td>53.19</td><td>73.99</td><td>92.54</td><td>9.86</td><td>1.20</td><td>98.39</td></tr><tr><td>TKG-ETA</td><td>97.06</td><td>78.61</td><td>88.51</td><td>97.35</td><td>3.11</td><td>0.00</td><td>99.99</td></tr><tr><td rowspan="4">ToN-IoT</td><td>Kitsune</td><td>86.63</td><td>52.59</td><td>72.41</td><td>87.05</td><td>8.90</td><td>43.15</td><td>65.20</td></tr><tr><td>Anomal-E</td><td>82.03</td><td>59.01</td><td>73.75</td><td>84.65</td><td>20.54</td><td>0.83</td><td>95.66</td></tr><tr><td>NF</td><td>90.94</td><td>74.21</td><td>84.36</td><td>91.86</td><td>10.42</td><td>0.00</td><td>99.99</td></tr><tr><td>TKG-ETA</td><td>94.70</td><td>83.04</td><td>89.95</td><td>95.06</td><td>6.04</td><td>0.41</td><td>98.69</td></tr><tr><td rowspan="4">CIC-IoT2023</td><td>Kitsune</td><td>93.03</td><td>78.91</td><td>87.37</td><td>93.58</td><td>7.80</td><td>1.51</td><td>99.08</td></tr><tr><td>Anomal-E</td><td>74.77</td><td>21.59</td><td>53.28</td><td>76.57</td><td>17.81</td><td>73.77</td><td>43.88</td></tr><tr><td>NF</td><td>91.21</td><td>74.81</td><td>84.75</td><td>92.05</td><td>9.90</td><td>1.48</td><td>99.13</td></tr><tr><td>TKG-ETA</td><td>95.42</td><td>85.04</td><td>91.17</td><td>95.67</td><td>5.03</td><td>1.63</td><td>99.24</td></tr></table>

## B. Encrypted Traffic Detection Performance

Table II reports the main detection results across the three benchmarks. TKG-ETA attains the highest Accuracy, Macro F1, and Weighted F1 on every dataset and simultaneously delivers the lowest FPR. On UNSW-NB15, the proposed model reaches 97.06% Accuracy and 88.51% Macro F1, outperforming the strongest baseline NF by 6.45 and 14.52 percentage points, respectively. The AUC-ROC of 99.99% confirms that explicitly modeling the spatiotemporal trajectories of encrypted flows provides near-perfect ranking quality compared to isolated flow density estimation.

The advantage becomes extremely pronounced on CIC-IoT2023, which contains dense temporal burst patterns. TKG-ETA achieves 95.42% Accuracy and 91.17% Macro F1, while the static-graph baseline Anomal-E collapses to 53.28% Macro F1. This demonstrates the critical limitation of static graph representations when confronted with dynamically evolving encrypted attacks at the edge. Averaged over the three benchmarks, TKG-ETA attains a mean Macro F1 of 89.88% and a mean FPR of 4.73%, making it highly reliable for cloud-edge deployment where high false alarms trigger unjustified node isolations.

## C. Ablation Study in Edge Environments

To quantify the contribution of each architectural component, we evaluate ablated variants alongside the full TKG-ETA model. Fig. 2 visualizes the results. The time encoding module contributes the single largest performance gain, particularly on CIC-IoT2023 where Macro F1 drops significantly when temporal input is zeroed. This confirms that encrypted bursts in IoT testbeds exhibit strong temporal signatures that a purely static structural encoder cannot capture. The full model consistently achieves the best result on every metric, validating that adaptive sketching and temporal encoding are highly complementary for robust detection under limited edge resources.

![](images/f4706245d609b0a990c01dbbc80506230267adb0cdfbcc0b081585938c6d2669.jpg)

Fig. 2. Ablation study visualization. Subfigures report the Macro F1-score and False Positive Rate across model variants.  
![](images/5d441ff5cb26e91e06c4637c9cda5f94b999a51941f8ef11507d97aed95112b7.jpg)  
Fig. 3. Two-dimensional t-SNE projections of the edge embeddings learned by TKG-ETA. Legitimate flows and anomalous flows form clearly separated clusters.

## D. Embedding Visualization

To provide intuitive evidence of the learned representation quality, we apply t-SNE to project the edge embeddings produced by TKG-ETA into a two-dimensional plane. As plotted in Fig. 3, legitimate encrypted flows and malicious encrypted flows form clearly separated clusters with negligible overlap on UNSW-NB15 and CIC-IoT2023. On ToN-IoT, the legitimate cluster remains tightly concentrated. The clear margin between clusters confirms that the temporal contrastive objective successfully learns an embedding geometry that naturally separates normal evolutionary patterns from anomalous structural deviations, despite the lack of payload visibility.

## E. Stability Analysis

Operational deployment of a detection engine in cloud-edge environments demands not only high average performance but also low variance across different distributed edge conditions. Fig. 4 presents the box-and-strip plots collecting Macro F1- scores from multiple independent runs. TKG-ETA exhibits the most compact and highest distribution among all methods, with a median Macro F1 near 90% and a narrow interquartile range. In contrast, Anomal-E displays a substantially wider spread due to the sensitivity of its static graph encoder to initial node feature assignments. The high stability of TKG-ETA confirms that the temporal contrastive learning framework produces robust edge embeddings that are not overly sensitive to environmental dynamics.

![](images/cd85dfd6707fc8ce333706917ed678f679f52c2c2d1e9859adb01cdce42a3723.jpg)  
Fig. 4. Stability analysis via box-and-strip plots. Each data point represents an independent experimental run. The yellow triangle marks the mean.

## VI. CONCLUSION

This paper presented TKG-ETA, a self-supervised Temporal Knowledge Graph framework equipped with an adaptive sketch mechanism for dynamic malicious encrypted traffic detection in cloud-edge networks. The framework addresses fundamental limitations of existing graph-based detectors: the inability to inspect encrypted payloads, the failure to capture temporal dynamics in streaming traffic, and the scalability bottlenecks at resource-constrained edge nodes. By compressing massive streaming traffic into compact statistical features via a constant-memory sketch and transforming them into a streaming TKG, the model captures rich heterogeneous communication semantics. The time-aware message-passing mechanism autonomously learns evolutionary trajectories of normal encrypted traffic. Extensive experiments demonstrate that TKG-ETA attains an average Accuracy of 95.73% and a mean Macro F1 of 89.88%, consistently outperforming representative baselines. The linear-in-edge training complexity and negligible inference latency firmly position the framework within the resource envelope of edge gateways for real-time continuous verification.

## REFERENCES

[1] S. Krishna Moorthy and J. Jagannath, “Survey of graph neural network for internet of things and nextg networks,” IEEE Communications Surveys & Tutorials, vol. 28, pp. 1803–1844, 2026.

[2] W. Zhang, D. Zhan, H. Yu, L. Zhang, B. Zhao, X. Du, and Z. Tian, “Distributed machine learning for next-generation communication networks: A survey on privacy, fairness, efficiency, and trade-offs,” Information Fusion, vol. 126, p. 103657, 2026.

[3] A. Poirrier, L. Cailleux, and T. Heide Clausen, “Is trust misplaced? a zero-trust survey,” Proceedings of the IEEE, vol. 113, no. 1, pp. 5–39, 2025.

[4] L. Wang, Z. Lu, M. Li, J. Wang, K. Gai, and X. Chen, “Desa: Decentralized secure aggregation for federated learning in zero-trust d2d networks,” IEEE Transactions on Information Forensics and Security, vol. 21, pp. 1987–2001, 2026.

[5] X. Lian, Y. Zheng, Y. Liu, F. Zhou, C. Peng, and X. Gao, “Contextual masking distillation for network traffic anomaly detection,” IEEE Transactions on Information Forensics and Security, vol. 21, pp. 1273–1286, 2026.

[6] A. Sharma and K. Bhushan, “A comprehensive survey on iot security: Challenges, security issues, and countermeasures,” Computer Science Review, vol. 59, p. 100839, 2026.

[7] K. Ahmad Awan, I. Ud Din, A. Almogren, Z. Han, and M. Guizani, “Trustaware-gnn: Graph-neural-network-based trust management for iot anomaly detection,” IEEE Internet of Things Journal, vol. 12, no. 18, pp. 37 670–37 681, 2025.

[8] Z. Yuan, Q. Sun, H. Zhou, M. Shao, and X. Fu, “A comprehensive survey on gnn-based anomaly detection: taxonomy, methods, and the role of large language models,” International Journal of Machine Learning and Cybernetics, pp. 1–26, 2025.

[9] J. P. Sahoo, B. Kar, A. M. Abdelmoniem, and D. Chatzopoulos, “Choirids: A federated learning framework for fidelity-calibrated explainable intrusion detection system for edge-iot networks,” Information Fusion, vol. 125, p. 103473, 2026.

[10] Z. Cui, D. Zang, J. Zhang, and K. Tang, “Mgcl: Multiorder graph neural network with cross-learning for multivariate time-series anomaly detection,” IEEE Transactions on Instrumentation and Measurement, vol. 74, pp. 1–14, 2025.

[11] P. Zhou, J. Wu, and W. Gan, “Bipartite graph anomaly detection with contrastive learning,” IEEE Transactions on Computational Social Systems, vol. 12, no. 6, pp. 5362–5374, 2025.

[12] J. Zhang, R. Ying, and J. Shao, “Online detection of anomalies in temporal knowledge graphs with interpretability,” Proceedings of the ACM on Management of Data, vol. 2, no. 6, pp. 1–26, 2024.

[13] Q. Lin, S. Chang, Y. Huo et al., “Anomaly detection in smart IoT systems based on contextual semantics of behavior graphs,” IEEE Internet of Things Journal, vol. 12, no. 10, pp. 13 683–13 696, 2025.

[14] M. T. A. Nguyen, V. Tong, S. B. Souihi, and S. Souihi, “Zero trust: Deep learning and nlp for http anomaly detection in ids,” IEEE Journal on Selected Areas in Communications, vol. 43, no. 6, pp. 2215–2229, 2025.

[15] N. Moustafa and J. Slay, “Unsw-nb15: a comprehensive data set for network intrusion detection systems (unsw-nb15 network data set),” in 2015 military communications and information systems conference (MilCIS). IEEE, 2015, pp. 1–6.

[16] A. Alsaedi, N. Moustafa, Z. Tari, A. Mahmood, and A. Anwar, “Ton iot telemetry dataset: A new generation dataset of iot and iiot for data-driven intrusion detection systems,” IEEE Access, vol. 8, pp. 165 130–165 150, 2020.

[17] E. C. P. Neto, S. Dadkhah, R. Ferreira, A. Zohourian, R. Lu, and A. A. Ghorbani, “Ciciot2023: A real-time dataset and benchmark for largescale attacks in iot environment,” Sensors, vol. 23, no. 13, p. 5941, 2023.

[18] Y. Mirsky, T. Doitshman, Y. Elovici, and A. Shabtai, “Kitsune: An ensemble of autoencoders for online network intrusion detection. arxiv 2018,” arXiv preprint arXiv:1802.09089, 1802.

[19] E. Caville, W. W. Lo, S. Layeghy, and M. Portmann, “Anomal-e: A selfsupervised network intrusion detection system based on graph neural networks,” Knowledge-based systems, vol. 258, p. 110030, 2022.

[20] L. Shafir, R. Giryes, and A. Wool, “Explainable anomaly detection in network traffic using normalizing flows,” IEEE Transactions on Networking, vol. 34, pp. 1205–1220, 2026.
# Bias in the Shadows: Explore Shortcuts in Encrypted Network Traffic Classification

Chuyi Wang, Xiaohui Xie\* , Tongze Wang, Yong Cui\*

Department of Computer Science and Technology, Tsinghua University

Abstract—Pre-trained models operating directly on raw bytes have achieved promising performance in encrypted network traffic classification (NTC), but often suffer from shortcut learning—relying on spurious correlations that fail to generalize to real-world data. Existing solutions heavily rely on model-specific interpretation techniques, which lack adaptability and generality across different model architectures and deployment scenarios.

In this paper, we propose BiasSeeker, the first semi-automated framework that is both model-agnostic and data-driven for detecting dataset-specific shortcut features in encrypted traffic. By performing statistical correlation analysis directly on raw binary traffic, BiasSeeker identifies spurious or environment-entangled features that may compromise generalization, independent of any classifier. To address the diverse nature of shortcut features, we introduce a systematic categorization and apply category-specific validation strategies that reduce bias while preserving meaningful information.

We evaluate BiasSeeker on 19 public datasets across three NTC tasks. By emphasizing context-aware feature selection and dataset-specific diagnosis, BiasSeeker offers a novel perspective for understanding and addressing shortcut learning in encrypted network traffic classification, raising awareness that feature selection should be an intentional and scenario-sensitive step prior to model training.

Index Terms—shortcut learning, detection, categorization, encrypted network traffic classification

## I. INTRODUCTION

Encrypted Network Traffic Classification (NTC), which aims to identify categories of network communication patterns, has become an increasingly important research area. This task is critical for ensuring cybersecurity, enhancing service quality and user experience, and enabling efficient network management.

With the rapid advancement of deep learning (DL), NTC has benefited from a wide range of intelligent methods, including traditional machine learning approaches based on flow statistics [1], [2], deep learning methods based on flow sequences [3]–[5], and pre-trained models operating directly on raw datagram bytes [6]–[10]. Among these, pre-trained models have achieved state-of-the-art classification performance. However, they are notably susceptible to the shortcut learning problem [11]–[14], wherein models learn to exploit spurious correlations that appear predictive in both training and testing datasets but fail to generalize to real-world, out-of-distribution scenarios [15]. For instance, pre-trained Transformer models have been observed to rely on TCP Timestamp Options to classify mobile application traffic [12], [13].

Existing efforts to prevent shortcut learning in NTC generally fall into two categories: model-agnostic interventions and model-dependent diagnoses. Model-agnostic approaches aim to eliminate widely recognized shortcut features [13], [14], but they often depend heavily on expert domain knowledge and overlook dataset-specific characteristics. In contrast, modeldependent diagnosis techniques seek to interpret a classifier’s decision-making process to identify shortcuts [11], [16], but their effectiveness is constrained by the particular models and interpretability tools employed. Outside of NTC, the broader AI community has also investigated methods for detecting and mitigating shortcut learning [17], [18], though such techniques are difficult to transfer due to fundamental differences in data modality between binary network traffic and image or text data.

Addressing shortcut learning in NTC faces two core challenges: (1) High diversity in traffic data distributions. Although prior work attempts to define generic shortcut feature categories, it is extremely difficult to capture the full range of traffic patterns found in diverse environments. For example, traffic collected from backbone networks differs significantly from that of end-user devices in terms of speed, volume, and structure. (2) Varying impact of shortcut features across applications. Previous methods often indiscriminately remove all suspected shortcut features, regardless of context. We argue that shortcut features should instead be carefully categorized and processed based on their intrinsic characteristics to more effectively support robust and generalizable NTC.

In this paper, we introduce BiasSeeker, the first semiautomated framework that is both model-agnostic and datacentric, offering a new perspective on shortcut learning in encrypted network traffic classification. Operating directly on raw binary traffic, it employs statistical analysis to detect spurious or environment-entangled features that may compromise generalization.

To promote meaningful learning and mitigate shortcut reliance, we further propose a principled taxonomy of shortcut feature types and develop corresponding validation strategies tailored to their behavioral patterns. These approaches aim not to eliminate features indiscriminately, but to retain valuable traffic information while suppressing dataset-induced biases. Feature selection should thus be an intentional and scenariosensitive step prior to model training or benchmarking.

Our evaluations span 19 publicly available datasets across VPN, malware, and encrypted application classification tasks, providing empirical evidence of BiasSeeker’s effectiveness in detecting shortcut features. By emphasizing context-aware feature selection and dataset-specific diagnosis, BiasSeeker contributes a data-centric foundation for building more robust, generalizable, and trustworthy network traffic classifiers.

Our main contributions are summarized as follows:

• We introduce a model-agnostic, data-specific perspective that detects feature instabilities through a mathematicallydriven semi-automated framework combining statistical analysis.  
• We develop a systematic categorization of feature instability patterns and design targeted mitigation strategies that preserve valuable traffic information while addressing specific types of unreliable feature dependencies.  
• We conduct comprehensive evaluations across 19 diverse datasets spanning VPN, malware, and encrypted application classification tasks, empirically validating the effectiveness of our approach in detecting and mitigating unstable feature behaviors.  
• We propose actionable insights and research directions about the development of accurate, generalizable, and real-world applicable network traffic classifiers through data-centric resolution.

## II. RELATED WORKS

## A. Shortcut Learning in AI Community

In classification tasks, the tendency of models to rely on spurious correlations between input data and ground truth labels, rather than meaningful features, are referred to as shortcuts [15]. To prevent models from relying on such shorts, researchers have explored a variety of model-dependent detection methods.

Assuming that shortcuts are easier to learn than the relevant features, Nam et al. [19] trained an auxiliary detector to identify shortcut samples by increasing their loss gradients. Similarly, Spare [20] detects shortcut samples by applying clustering techniques during the early stages of training.

Inspired by perturbation-based feature importance, Wang et al. [21] assesses the importance of frequency-based feature by sequentially removing specific frequency bands, revealing shortcuts in image classification through changes in model performance.

To identify spurious features based on domain knowledge, researchers have also adopted techniques from eXplainable Artificial Intelligent (XAI). In addition to widely used libraries such as InterpretML [22] and Captum [23], more advanced methods such as heatmap clustering [24] or feature disentanglement [25] have also been proposed.

Departing from the focus on textual or visual modalities, our work explores the detection of potential shortcut features specifically within network traffic data.

## B. Shortcut Learning in NTC

To develop more robust network traffic classification models, researchers have explored two main approaches to mitigate shortcut learning: model-agnostic prior intervention and model-dependent post-hoc diagnosis.

Model-agnostic prior intervention methods aim to remove features that are commonly assumed to be shortcuts. For example, YaTC [7] and NetMamba [8] remove Ethernet header and IP addresses; ET-BERT [6] excludes both Ethernet and IP headers; and netFound [13] and TrafficFormer [10] go further by removing or randomizing fields such as sequence numbers, acknowledgment numbers, TCP timestamp options, and server name indication (SNI) in TLS handshake messages. More recently, NTC-Enigma [14] provides a comprehensive summary of these shortcut-related fields based on RFC specifications. However, all of these approaches rely on predefined assumptions about which features constitute shortcuts, which may not accurately reflect the actual feature distributions of a given dataset. This limitation motivates a data-driven approach to detecting shortcuts more precisely.

Conversely, model-dependent post-hoc diagnosis methods seek to interpret a classifier’s decision-making process or analyze feature importance to identify and mitigate shortcuts. For example, Trustee [11] identifies shortcuts by distilling blackbox models into interpretable ones such as random forests. However, the effectiveness of these methods is constrained by the specific classifiers and interpretation techniques used. Furthermore, explanations provided by interpretable models are often not inherently easier to understand [26]. This underscores the need for a model-agnostic method with greater potential to reveal dataset-level biases in a more general and scalable manner.

In contrast to these existing efforts, our work introduces a data-driven and model-agnostic framework for detecting potential shortcut features in network traffic.

## III. PRELIMINARIES

In this section, we introduce the theoretical foundations and statistical criteria underpinning our framework for shortcut detection in encrypted traffic classification. Our goal is to identify features whose apparent correlation with class labels arises from dataset-specific artifacts—rather than genuine protocol semantics—and which thus pose risks to model generalization.

## A. Shortcut Definition

In machine learning, shortcut learning refers to the phenomenon where models rely on non-causal signals to make predictions [15]. These shortcuts typically emerge from incidental patterns in training data that are predictive of labels but do not reflect true task semantics. Models exploiting shortcuts perform well in-distribution but generalize poorly under domain shifts.

In encrypted network traffic classification, shortcut learning manifests uniquely. With packet payloads inaccessible, models rely solely on side-channel information such as headers, timing patterns, or flow metadata. When header fields or timing signals correlate with labels due to capture artifacts or protocol idiosyncrasies—rather than intrinsic traffic characteristics—they become shortcuts. For example, TCP timestamp options may uniquely identify mobile applications in specific datasets but fail when timestamps are randomized or disabled [12]. Similarly, IP addresses may appear predictive in static network environments but become unreliable under NAT or dynamic addressing [13]. These shortcuts create brittle models that fail in real-world deployments.

## B. Problem Formulation

Let $\boldsymbol { \mathcal { D } } = \{ ( x _ { i } , y _ { i } ) \} _ { i = } ^ { N }$ 1 denote a dataset, where $x _ { i } \in \mathbb { R } ^ { d }$ is a d-dimensional feature vector and $y _ { i } ~ \in ~ \mathcal { V }$ its label. Let $x _ { i } ^ { ( j ) }$ xi denote the j-th feature of the i-th sample, and $X _ { j } ~ =$ $\{ \bar { x } _ { i } ^ { ( j ) } \} _ { i = 1 } ^ { N }$ the empirical realization of feature $j .$ . Our goal is to quantify the statistical dependence between $X _ { j }$ and labels $Y \overset { = } { = } \{ y _ { i } \} _ { i = 1 } ^ { \overset { . } { N } }$ from genuine semantics or potential shortcut mechanisms.

## C. Mutual Information (MI)

For discrete-valued feature $X _ { j }$ and categorical label Y , mutual information quantifies the reduction in uncertainty about one variable given knowledge of the other:

$$
I (X _ {j}; Y) = \sum_ {x \in \mathcal {X} _ {j}} \sum_ {y \in \mathcal {Y}} P (x, y) \log \left(\frac {P (x , y)}{P (x) P (y)}\right),
$$

where $P ( x , y )$ is the joint empirical distribution and $P ( x ) , P ( y )$ the marginals.

High MI indicates that $X _ { j }$ provides substantial information about Y . In traffic classification, this suggests strong predictiveness, potentially from semantic patterns or spurious correlations.

However, MI is sensitive to feature cardinality and label imbalance, leading to overestimation of dependence. It also lacks a natural upper bound, complicating cross-feature comparisons.

## D. Adjusted Mutual Information (AMI)

To address these limitations, we use Adjusted Mutual Information (AMI), which normalizes MI against its expected value under a random null model and bounds the score between 0 and 1.

For discrete variables $X _ { j }$ and $Y$ :

$$
\operatorname{AMI} (X _ {j}, Y) = \frac {I (X _ {j} ; Y) - \mathbb {E} [ I (X _ {j} ; Y) ]}{\max \left\{H (X _ {j}) , H (Y) \right\} - \mathbb {E} [ I (X _ {j} ; Y) ]},
$$

where $H ( \cdot )$ is Shannon entropy, and $\mathbb { E } [ I ( X _ { j } ; Y ) ]$ is the expected MI under random permutation. AMI offers key advantages:

• Normalization: Bounded in [0, 1], enabling fair comparison across features.  
• Adjustment for Chance: Discounts spurious agreement from random correlations.  
• Robustness: Less sensitive to class imbalance, suitable for traffic classification.

## IV. METHODOLOGY

In this section, we present our integrated framework for detecting, categorizing, and further validating shortcut features in encrypted traffic classification. Our approach combines data-driven statistical analysis with domain knowledge to systematically identify problematic features and develop targeted mitigation strategies.

## A. Intuition

Our intuition is that shortcut features tend to exhibit disproportionately high statistical association with the label. Thus, we first identify the most label-correlated features from the full feature set as candidates for further examination.

We identify a feature as a potential shortcut if:

1) It exhibits a high AMI score with respect to the class label, indicating strong predictive power;  
2) Its semantics suggest no causal or protocol-level connection to the class (e.g., hardware identifiers, checksum fields, timestamp offsets);  
3) It shows fragile behavior across environments or datasets, which we investigate further in Section V.

By systematically auditing such features, we aim to reduce shortcut learning and promote generalizable, protocol-aware classification.

## B. Overview

The overall workflow of our framework includes:

1) Extraction of all raw packet fields using advanced packet parsing tools.  
2) Preprocessing and conversion of raw fields into a uniform integer-based format.  
3) Calculation of Adjusted Mutual Information (AMI) between each feature and the class label.  
4) Selection of the top-k features ranked by AMI as candidate shortcut features.  
5) Categorization of these features based on domain knowledge into three types.  
6) Category-specific validation and mitigation strategies (detailed in Section V).

![](images/e3f33ac0a7e3671942c48d8153287dce94e9b1214f68458506734d11c6316e1d.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
  A["Raw Field Extraction"] --> B["Field Normalization & Encoding"]
  B --> C["AMI Range Delineation"]
  C --> D["Top-k Feature Selection & Shortcut Hypothesis"]
  D --> E["Granular Feature Analysis"]
  E --> F["Feature Categorization"]
  F --> G["Data-Leakage Identifiers"]
  F --> H["Relative Artifacts"]
  F --> I["Task-Agnostic Fields"]
  F --> J["Domain Knowledge"]
  J --> F
  K["Experimental Validation"] --> F
```
</details>

Fig. 1: Workflow of the Feature Analysis Process

## C. Pipeline

The workflow of our framework shown in Fig 1is designed to systematically analyze, categorize, and mitigate shortcut features. We now detail each component.

1) Raw Field Extraction: We utilize tshark1 to extract full packet-level fields, owing to its extensive protocol support, structured output, and community-maintained dissectors. tshark built atop Wireshark, offers the richest set of fields and the most precise dissection of encrypted traffic layers.

2) Field Normalization and Encoding: To compute statistical measures such as AMI, all fields must be transformed into numerical formats. Our preprocessing pipeline includes unified packet-level feature extraction and encoding routines, designed to handle a wide range of protocol layers and field types:

• IP Address Conversion: IP addresses are converted into 32-bit integers by treating each octet as a base-256 digit.  
• Hexadecimal Decoding: Fields are parsed from hexadecimal or string representations to integers using robust fallback conversion routines.  
• Floating-Point Preservation: Temporal fields are retained as floating-point values to preserve fine-grained resolution.  
• Domain Name Normalization: For TLS/DTLS server names, we extract second-level domains and map them to consistent integer indices using a global dictionary constructed during parsing.  
• Missing Value Handling: Empty or structurally invalid values are assigned a default excluded value to prevent NaNs or spurious outliers from affecting downstream statistics.

To ensure data quality, we filter out redundant or incomplete traffic flows, such as samples with less than 5% valid fields or malformed IP address mappings.

3) AMI Range Delineation: We assess the informativeness of each feature using Adjusted Mutual Information (AMI) between the feature and the classification label.

To ensure reliable estimates:

• Categorical fields are encoded using LabelEncoder.  
• Numerical fields are discretized if their distributions are highly skewed or multimodal.

Prior to AMI computation, we remove constant fields, lowentropy fields, and structurally trivial attributes (e.g., frame number, stream index, Ethernet padding) to avoid misleadingly high or spurious AMI scores.

4) Top-k Feature Selection and Shortcut Hypothesis: We rank features by their AMI scores and retain the top-ranked for further inspection. We formally justify that high-AMI features are necessary (though not sufficient) conditions for shortcut presence:

If a feature $X _ { j }$ is exploited as a shortcut by a model $f ,$ then $X _ { j }$ must exhibit non-trivial dependence with the label Y , i.e., $I ( X _ { j } ; Y ) ~ > ~ 0$ . Therefore, shortcut features are expected to appear in the top-ranked AMI list.

This provides a sound basis for focusing on top-AMI features in the initial detection phase.

## D. Categorization

Network traffic classification (NTC) models often rely on unintended correlations between features and labels, these issues vary across tasks and datasets. We introduce a method to categorize such features based on domain knowledge. Our categorization framework identifies three distinct types of potential shortcut features:

• Data-Leakage Identifiers: Features that reveal labelrelevant information due to data collection or labeling artifacts.  
• Relative Artifacts: Fields that contain absolute values encoding host- or session-specific behavior, which, though not explicitly leaking labels, produce learnable patterns irrelevant to true semantics.  
• Task-Agnostic Fields: Low-level protocol features that correlate with environmental conditions rather than application behavior. Their shortcut effect emerges from spurious alignment with label distributions across datasets.

This categorization enables targeted analysis and validation strategies for each type of potential shortcut feature, as detailed in the following subsection.

## E. Validation

To support our categorization and better understand the shortcut behaviors of different feature types, we design two complementary validation strategies: model-based validation and category-specific analyses. Together, these approaches verify the practical impact of suspected shortcut features and inform mitigation design.

1) Model-Based Validation: To quantify how shortcutprone features influence downstream classification performance, we apply three occlusion strategies at the feature level: zero padding, relative transformation, and random masking. These strategies are designed to suppress shortcut signals while preserving feature structure as much as possible.  
These strategies are later applied in Section V to assess how performance shifts when suspected shortcut features are occluded or transformed, offering an indirect yet practical measurement of their influence.  
2) Category-Specific Analyses: Beyond model-agnostic occlusion, we develop tailored validation methods that exploit the intrinsic statistical properties of feature categories.  
a) Relative Artifacts: To validate whether absolutevalued features encode spurious host/session information, we measure the change in feature-label dependence before and after relative transformation using Adjusted Mutual Information (AMI):

$$
\Delta_ {\mathrm{AMI}} = \operatorname{AMI} (X _ {j}, Y) - \operatorname{AMI} (X _ {j} ^ {\text { rel }}, Y)
$$

A significant drop in AMI score indicates that absolute values contribute little beyond host-specific bias, supporting the shortcut hypothesis. This analysis justifies using relative encoding as a mitigation strategy.

b) Task-Agnostic Fields: These low-level protocol fields often correlate with environment-specific properties. We quantify their cross-dataset generalizability using class-conditional Kullback-Leibler divergence:

$$
\mathrm{KL} _ {\text { avg }} (X _ {j}) = \frac {1}{| C |} \sum_ {y \in C} \mathrm{KL} (P _ {X _ {j}} ^ {(D _ {1})} (y) \| P _ {X _ {j}} ^ {(D _ {2})} (y))
$$

where $P _ { X _ { i } } ^ { ( D ) } ( y )$ (D) is the empirical distribution of feature $X _ { j }$ under class y in dataset D. High divergence suggests dataset entanglement and poor transferability. Distribution-aware normalization may reduce this bias.

The category-specific analyses ensure that our categorization is not only theoretically sound but also practically actionable, providing targeted validation strategies for each type of potential shortcut feature. Feature selection is grounded not only in intuition but also in quantifiable evidence.

## V. EXPERIMENTS

## A. Experimental Settings

1) Datasets: To evaluate the effectiveness of the proposed approach, we perform experiments on a diverse set of publicly available traffic datasets, covering three primary encrypted traffic classification tasks.

1. VPN Traffic Classification: This task involves identifying different categories of network traffic routed through VPN services. Specifically, datasets such as NordVPN [12], SuperVPN [12], Surfshark [12], TurboVPN [12] include traffic captured from 100 Android mobile applications. In addition, ISCXVPN2016 [27] contains both VPN and non-VPN traffic collected in real-world scenarios, covering diverse activities such as web browsing, email communication, and streaming.

2. Malware Traffic Classification: The goal is to distinguish malware-generated traffic from benign traffic. We use all four malware categories from CIC-AndMal2017 [28], namely Adware, Scareware, SMS-Malware and Ransomware. Additionally, we employ the USTC-TFC2016 [29], which comprises both benign and malicious traffic samples.

3. Encrypted Application Classification: This task aims to classify encrypted traffic according to the originating applications. The CrossPlatform(Android) [30] and CrossPlatform(iOS) [30] contain traffic traces from over 200 mobile applications. CrossNet2021 [31] captures traffic from the same applications under varying network conditions. Both CSTNET-TLS1.3 [6] and CipherSpectrum [14] feature application-level traffic encrypted using the TLS 1.3 protocol.

2) Shortcut Detection Setting: To uncover shortcuts in each dataset, we compute AMI in a per-packet granularity. Our choice to use packet-level features is driven by the desire to maintain high fidelity and alignment across diverse datasets. Shortcut signals often reside in individual packet-level metadata, such as specific TCP flags, TTL values, or timestamp behaviors. While flow-level aggregation could capture longterm dependencies, it also introduces challenges: flow lengths vary greatly, making truncation or padding necessary, which often leads to bias or information loss. Flow-level statistics in shortcut detection may obscure such subtle yet discriminative patterns. Therefore, a per-packet approach allows us to retain and highlight these fine-grained correlations.

3) Model Selection: To assess the impact of the identified shortcuts on model classification performance, we employ two types of test models: (1) NetMamba $[ 8 ] ,$ , a state-of-the-art pretrained model for network traffic classification, and (2) a decision tree, representing a classical shallow machine learning approach. The input data is prepared following NetMamba’s original design: for each flow, we select the first 5 packets, extracting the first 80 header bytes and first 240 payload bytes. The main differences concerning data representation are twofolds:

1. We replace the uni-directional flow with bi-directional session flows.

2. We keep or discard certain header fields according to our mitigation strategies.

We pre-train NetMamba on 6 public datasets: CI-CIoT2022 [32], CrossPlatform(Android), CrossPlatform(iOS), ISCXVPN2016, USTC-TFC2016 and ISCXTor2016 [33].

To reduce resource costs for model fine-tuning and mitigation evaluation, we select two datasets from each classification task. For datasets with class numbers more than 30 (i.e., CSTNET-TLS1.3 and SurfsharkVPN), we randomly sampled a small proportion of original categories. For each dataset, we randomly sample at most 500 flows. All flows in each category are divided into training/validation/test in an 8:1:1 ratio. To mitigate randomness, we repeat the sampling process three times per dataset and report the average model performance across these runs.

Detailed statistics of datasets used for shortcut mitigation are outlined in Table I.

TABLE I: The Statistics of Shortcut Mitigation Datasets

<table><tr><td>Task</td><td>Dataset</td><td>#Class</td><td>#Flows</td><td>#Used Class</td><td>#Used Flows</td></tr><tr><td rowspan="2">Application</td><td>CrossNet2021</td><td>20</td><td>4443</td><td>20</td><td>4443</td></tr><tr><td>CSTNET-TLS1.3</td><td>120</td><td>46372</td><td>18</td><td>7108</td></tr><tr><td rowspan="2">VPN</td><td>ISCXVPN2016</td><td>13</td><td>37770</td><td>13</td><td>6124</td></tr><tr><td>SurfsharkVPN</td><td>151</td><td>7500</td><td>30</td><td>1500</td></tr><tr><td rowspan="2">Malware</td><td>USTC-TFC2016</td><td>20</td><td>489139</td><td>20</td><td>10000</td></tr><tr><td>Ransomware</td><td>10</td><td>196803</td><td>10</td><td>5000</td></tr></table>

4) Model-based Validation Strategies: To assess the influence of suspicious shortcut features on a given NTC model, we design three feature occlusion strategies: zero padding, relative transformation, and random masking.

Zero padding is the simplest approach, where the target feature is replaced with zeros.

Relative transformation operates by computing the difference in target feature values between two adjacent packets.

![](images/41dc05b9dec0e9ecc734e178e4b1b64b06934db1aa723b8938c8b3957f8d3412.jpg)

<details>
<summary>bar chart</summary>

Android150_with_TurboVPN
| Category | AMI Score |
|---|---|
| ip.fd | 0.0393 |
| ip.flg | 0.0394 |
| ip.len | 0.0988 |
| udp.len | 0.0988 |
| ip.chk | 0.1497 |
| ip.ttl | 0.2714 |
| ip.dst | 0.3800 |
| ip.src | 0.4194 |
| sport | 0.5072 |
| dport | 0.6138 |
</details>

![](images/bba0ad0951dff4af75761934f128ba0b1cb30a94e5e48c32fc10d9996480fa20.jpg)

<details>
<summary>bar chart</summary>

Android150_with_NordVPN
| Source | AMI Score |
|---|---|
| ip.flg | 0.0039 |
| eth.dst | 0.0424 |
| eth.src | 0.0584 |
| udp.len | 0.1048 |
| ip.len | 0.1048 |
| sport | 0.1646 |
| ip.ttl | 0.1783 |
| dport | 0.2337 |
| ip.dst | 0.3145 |
| ip.src | 0.3284 |
</details>

![](images/908c0e815bbc5d9e2a0cea7d84e6d335e3200be027546fea289ba1f8e78013ef.jpg)

<details>
<summary>bar chart</summary>

Android150_with_SuperVPN
| Version | AMI Score |
| :--- | :--- |
| ip.fd | 0.0049 |
| udp.chks | 0.0049 |
| ip.flg | 0.0050 |
| ip.len | 0.0911 |
| udp.len | 0.0911 |
| ip.ttl | 0.2087 |
| ip.dst | 0.3358 |
| ip.src | 0.3780 |
| dport | 0.4808 |
| sport | 0.4808 |
</details>

![](images/1a57111f46a03f3e259455d7adff02639d8d10f7632df63acf4247ef95e1dea5.jpg)

<details>
<summary>bar chart</summary>

Android150_with_Surfshark
| Protocol | AMI Score |
| :--- | :--- |
| tcp.len | 0.0703 |
| tcp.tsv | 0.1069 |
| sport | 0.1636 |
| tcp.tse | 0.2616 |
| ip.dst | 0.2971 |
| tcp.ak | 0.3046 |
| tcp.akr | 0.3054 |
| ip.ttl | 0.3185 |
| ip.src | 0.5231 |
| dport | 0.6064 |
</details>

![](images/f34272e53bb4784e7706307eb1de588ca804a92c0377d102c7d12df00a4e3017.jpg)

<details>
<summary>bar chart</summary>

ISCXVPN2016
| Protocol | AMI Score |
| :--- | :--- |
| tls.ct | 0.3294 |
| tcp.flg | 0.3296 |
| tls.rl | 0.3352 |
| udp.len | 0.3395 |
| tcp.ws | 0.4866 |
| ip.ttl | 0.4867 |
| dport | 0.5084 |
| sport | 0.5136 |
| ip.dst | 0.5788 |
| ip.src | 0.5967 |
</details>

Fig. 2: Top-k AMI Features in VPN Traffic Datasets

This strategy specifically targets features classified as relative artifacts. While the absolute values of such features are typically initialized based on the TCP connection startup timestamp, their differences encode meaningful semantics. For instance, the difference in TCP sequence numbers reflects packet length, whereas the difference in TCP timestamp options represents packet inter-arrival time.

Random masking provides a more robust occlusion mechanism. We randomize both source and destination IP addresses and ports of the first packet, then adjust those in subsequent packets within the session accordingly. For relative artifacts, we randomize the feature values of the first packet while preserving the relative differences in subsequent packets. For all other features, field values are randomized independently.

## B. Detection Experiments

We present experimental evidence supporting our shortcut detection framework. Our analysis is organized into four major components: (1) top-k shortcut field selection using AMI, (2) task-specific and cross-task feature behaviors, and (3) granular inspection of different types of suspected shortcuts.

1) Top-k Selection and Hypothesis: We compute Adjusted Mutual Information (AMI) between each field and the class label across three classification tasks: VPN detection, malware detection, and encrypted app classification. Features are then ranked by their AMI scores, and the top-k fields are identified as potentially shortcut-prone. Here we present the AMI top10 ranked features for the VPN detection task, as illustrated in Figure 2.  
2) Task-Specific and Cross-Task Feature Behavior: As shown in Fig 3(L), identifier fields such as ip.src, ip.dst, srcport and dstport consistently appear among the top-ranked fields across all tasks (VPN, malware, and app classification), implying a generalized shortcut tendency. These fields, while highly discriminative, often reflect dataset artifacts rather than meaningful semantics.

While demonstrating notable feature stability across tasks, our analysis reveals distinct task-specific field preferences:

• VPN Traffic Classification: Relies heavily on IP address and port-based features.  
• Malware Traffic Classification: Leverages MAC and timing-level features such as eth.dst and tcp.window size.  
• Encrypted Application Classification: Exhibits mixedlayer reliance, including TLS-layer metadata, sequence numbers, and TCP timestamp options.

These findings support the existence of both task-shared and task-specific shortcut fields and reinforce the necessity of careful feature selection and mitigation strategies to ensure robust encrypted traffic classification.

3) Granular Feature Analysis: We further partition AMIranked features into three categories(shown in Table II) for detailed analysis according to further experimental validations.

Data-leakage identifiers. Fields such as TCP Server Name Indication (SNI) and other Strong Identification Indicators (SII), including source/destination IP addresses and ports, serve as strong signals of potential overfitting, as they are often directly used for labeling or exhibit high correlation with labels. Leveraging domain knowledge, these fields can be identified and are typically removed in fair evaluation settings.

Relative artifacts. Due to their large bit widths, TCP-level fields such as timestamps, sequence numbers, and acknowledgment numbers within the same session often exhibit constant high-order bits, making them potential shortcut features. To mitigate shortcuts arising from these high-order bits, we apply relative transformations to these fields (e.g., converting tsval to the difference tsval–tsecr, or seq raw to normalized seq). We then compute the AMI of both absolute and relative versions across datasets and plot them for visual comparison.

Specifically, we evaluate three field pairs: (tsval vs. time relative), (seq raw vs. seq), and (ack raw vs. ack). These pairs reflect a transition from raw values to semantics-aware or relative measurements. Figure 3(R) presents a row-wise comparison across three traffic classification scenarios (VPN, Malware, and Encrypted Application), with each column representing different datasets within the same task, and each row corresponding to one of the three field pairs. The vertical axis denotes the AMI score, representing feature-task alignment.

• Malware traffic classification exhibits the most significant reduction in AMI after relative transformation. Particularly for timestamp-related fields (tsval vs. time relative), the raw field consistently shows strong task alignment, while its relative counterpart demonstrates reduced utility. This suggests that malware traffic families may encode fixed or correlated timing patterns exploitable by the classifier.  
• VPN traffic classification displays the lowest AMI drop across all three field pairs. The relative and absolute versions of sequence and acknowledgement fields show comparable AMI values, indicating that these fields do not serve as strong shortcuts. VPN tools might exhibit

![](images/cefd814804366c7b2f2c2c20c24c5916229de6a4323e3f9d27be522d4a2812cd.jpg)

![](images/5d34fefb98b8466402c0b8b1834dd46a480a94e1e61a01252bb9fea55c4d0550.jpg)

<details>
<summary>line chart</summary>

| Workload | tsval | time relative |
| --- | --- | --- |
| VPN | 3.0 | 1.0 |
| Malware | 2.5 | 0.5 |
| App | 3.5 | 1.5 |
| CrossNetA2021 | 2.0 | 3.0 |
| CrossNetB2021 | 2.5 | 2.0 |
| CrossPlatform(Android) | 2.0 | 2.5 |
| CrossPlatform(OS) | 2.0 | 3.0 |
| CyberSpectrumA128 | 2.0 | 3.0 |
| CyberSpectrumA256 | 2.0 | 3.0 |
| CyberSpectrum | 2.0 | 2.5 |
| CSTNETTL5.1.3 | 3.0 | 2.5 |
| TCP | 2.5 | 2.0 |
| TCP | 2.0 | 1.5 |
| TCP | 1.5 | 1.0 |
| TCP | 1.0 | 0.5 |
| TCP | 0.5 | 0.5 |
| TCP | 0.5 | 0.5 |
| TCP | 0.5 | 0.5 |
| TCP | 0.5 | 0.5 |
| TCP | 0.5 | 0.5 |
| TCP | 0.5 | 0.5 |
| TCP | 0.5 | 0.5 |
| TCP | 0.5 | 0.5 |
| TCP - IPCVN2016 | 2.5 | 1.5 |
| ISCKVPN2016 | 3.0 | 2.0 |
| Aдвare | 1.5 | 1.0 |
| Ransomware | 2.0 | 1.5 |
| Scawware | 2.0 | 1.5 |
| SMSMalware | 2.0 | 1.5 |
| USTC-TEC2016 | 2.5 | 3.0 |
| IAVN | 2.0 | 1.5 |
| IAVN | 1.5 | 1.0 |
| IAVN | 1.0 | 0.5 |
| IAVN | 1.0 | 0.5 |
| IAVN | 1.0 | 0.5 |
| IAVN | 1.0 | 0.5 |
| IAVN | 1.0 | 0.5 |
| IAVN | 1.0 | 0.5 |
| IAVN | 1.0 | 0.5 |
| IAVN | 1.5 | 1.5 |
| IAVN | 2.0 | 2.0 |
| IAVN | 2.5 | 2.5 |
| IAVN | 3.0 | 3.0 |
| IAVN | 3.5 | 3.5 |
| IAVN | 4.0 | 4.0 |
| IAVN | 4.5 | 4.5 |
| IAVN | 5.0 | 5.0 |
| IAVN | 5.5 | 5.5 |
| IAVN | 6.0 | 6.0 |
| IAVN | 6.5 | 6.5 |
| IAVN | 7.0 | 7.0 |
| IAVN | 7.5 | 7.5 |
| IAVN | 8.0 | 8.0 |
| IAVN | 8.5 | 8.5 |
| IAVN | 9.0 | 9.0 |
| IAVN | 9.5 | 9.5 |
| IAVN | 10.0 | 10.0 |
| IAVN | 10.5 | 10.5 |
| IAVN | 11.0 | 11.0 |
| IAVN | 11.5 | 11.5 |
| IAVN | 12.0 | 12.0 |
| IAVN | 12.5 | 12.5 |
| IAVN | 13.0 | 13.0 |
| IAVN | 13.5 | 13.5 |
| IAVN | 14.0 | 14.0 |
| IAVN | 14.5 | 14.5 |
| IAVN | 15.0 | 15.0 |
| IAVN | 15.5 | 15.5 |
| IAVN | 16.0 | 16.0 |
| IAVN | 16.5 | 16.5 |
| IAVN | 17.0 | 17.0 |
| IAVN | 17.5 | 17.5 |
| IAVN | 18.0 | 18.0 |
| IAVN | 18.5 | 18.5 |
| IAVN | 19.0 | 19.0 |
| IAVN | 19.5 | 19.5 |
| IAVN | 20.0 | 20.0 |
| IAVN | 20.5 | 20.5 |
| IAVN | 21.0 | 21.0 |
| IAVN | 21.5 | 21.5 |
| IAVN | 22.0 | 22.0 |
| IAVN | 22.5 | 22.5 |
| IAVN | 23.0 | 23.0 |
| IAVN | 23.5 | 23.5 |
| IAVN | 24.0 | 24.0 |
| IAVN | 24.5 | 24.5 |
| IAVN | 25.0 | 25.0 |
| IAVN | 25.5 | 25.5 |
| IAVN | 26.0 | 26.0 |
| IAVN | 26.5 | 26.5 |
| IAVN | 27.0 | 27.0 |
| IAVN | 27.5 | 27.5 |
| IAVN | 28.0 | 28.0 |
| IAVN | 28.5 | 28.5 |
| IAVN | 29.0 | 29.0 |
| IAVN | 29.5 | 29.5 |
| IAVN | 30.0 | 30.0 |
</details>

Fig. 3: (L) Average AMI Scores of Key Features Across Tasks; (R) AMI Comparison of Relative Artifacts Across Tasks.

more consistent behavior across instances, limiting the impact of alignment-based artifacts.

• In Encrypted Application classification, relative timestamp fields (time relative) show lower AMI than their absolute counterparts (tsval), but the drop is less severe than in Malware. Notably, this difference is magnified in Cross-Platform datasets (e.g., CrossPlatform-Android vs. CrossPlatform-iOS), suggesting that OS-level stack behaviors introduce shortcut potentials in timestamp fields.

This comparison reveals that absolute field values may encode environment-specific or implementation-specific artifacts that adversely affect classifier generalization. Converting to relative representations not only mitigates reliance on these artifacts but also enhances cross-domain generalization capability.

Task-Agnostic fields. Fields such as IP TTL, IP checksum, TCP window size, and TCP checksum carry limited relevance to NTC tasks. For these fields, we inspect their statistical distributions and environmental sensitivity. Among these, we select TCP Window Size as a representative example to illustrate our analysis procedure, due to its known dependence on bandwidth and congestion dynamics.

Defined as the amount of data a sender is willing to receive, TCP Window Size is known to vary with bandwidth and congestion conditions. We conduct a comparison using two datasets: CrossNet-A and CrossNet-B.

• Scenario A was collected under a stable 100 Mbps environment with low latency and no artificial delay or jitter.  
• Scenario B comes from a 10 Mbps network with a random packet loss rate (2.5% to 5%) and approximately 200 ms of delay due to unstable links.

The distributions of TCP Window Size for different applications in both datasets are shown in Figure 4. We observe significant distributional differences for the same application type under different network conditions. The window size distribution in CrossNet-B is more concentrated, while CrossNet-A shows a more dispersed distribution, indicating that network conditions significantly impact TCP Window Size.

![](images/37a0a74369ab93023331566705529c46a95a7e280e5ac78f33c62d6305d3f092.jpg)

<details>
<summary>bar chart</summary>

|        | tcp window size |
| ------ | --------------- |
| steam  | 2.00            |
| huya   | 0.00            |
| csdn   | 1.50            |
| yoku   | 0.50            |
| pptv   | 0.25            |
| zhihu  | 0.25            |
| jd     | 0.25            |
| weibo  | 0.25            |
| youdao | 0.00            |
| baidupan | 0.00           |
| TIM    | 0.00            |
| 360    | 0.00            |
| sohu   | 0.25            |
| wps    | 0.25            |
| aiqiyi | 0.00            |
| microsoft | 0.25          |
| apple  | 0.25            |
| netcmusic | 0.25         |
| mgtv   | 0.25            |
| sougou | 0.00            |
</details>

CrossNetB2021  
![](images/f76cfb7774aeb41889a593830975f904a308b12a6e8954be205ada4957514957.jpg)

<details>
<summary>bar chart</summary>

|        | tcp: window size |
| ------ | ----------------- |
| steam  | 0.25              |
| huya   | 0.00              |
| csdn   | 0.00              |
| youku  | 0.00              |
| pptv   | 0.00              |
| zhihu  | 0.00              |
| jd     | 0.00              |
| weibo  | 0.00              |
| youdao | 0.25              |
| baldupan | 0.00             |
| TIM    | 0.00              |
| 360    | 0.00              |
| sohu   | 0.00              |
| wps    | 0.15              |
| aiqiyi | 0.00              |
| microsoft | 0.00            |
| apple  | 0.00              |
| netcrmusic | 0.15         |
| mgtv   | 0.00              |
| sougou | 0.00              |
</details>

Fig. 4: TCP Window Size Distributions Across Different Network Quality Conditions

To further quantify the correlation between TCP Window Size and network quality, we employ KDE to estimate the probability density distributions of the field in both datasets and compute KL divergence to measure distributional differences. For intuitive comparison, we also calculate KL divergence for more stable fields like TCP length, TCP flags, and IP length. The KL divergence of TCP Window Size (2.36) is significantly higher than others (e.g., TCP length (0.06), TCP flags (0.53), IP length (0.05)), validating its sensitivity to network conditions and potential role as an unstable feature.

We evaluate other fields such as Checksum and IP TTL using similar methods. While some fields exhibit mild sensitivity due to routing behavior differences, others like Checksum are primarily determined by payload content and packet structure, showing less environmental variance. Combining domain knowledge, IP Checksum is used to verify the integrity of packet header bytes, where any change in header bytes causes Checksum value changes, making it semantically unrelated to network traffic classification. IP TTL reflects the number of hops during packet transmission, typically preventing infinite loops in networks. Although TTL values may vary with network topology or routing policies, they generally do not directly impact traffic classification outcomes.

TABLE II: Potential Shortcut Feature

<table><tr><td>Category</td><td>Representative Features</td></tr><tr><td>Data-Leakage Identifiers</td><td>SII(Src IP, Dst IP, Src Port, Dst Port), SNI</td></tr><tr><td>Relative Artifacts</td><td>Seq Num, Ack Num, Timestamp Option</td></tr><tr><td>Task-Agnostic Fields</td><td>Window Size, Checksum, TTL</td></tr></table>

## C. Mitigation Evaluation

We further examine and mitigate the influence of shortcut features on NTC models, with the corresponding evaluation results presented in Table III. Prior studies [12]–[14] have reported that the classification accuracy of NTC models typically decreases when shortcut features are mitigated in the input data. However, as shown in Table III, we unexpectedly observe that both NTC models achieve accuracy improvements under several occlusion settings. Our analysis is as follows:

1) NTC models exhibit susceptibility to shortcut features: With the exception of USTC-TFC2016 and Ransomware, both NTC models experience accuracy degradation under most occlusion settings for the remaining four datasets. This suggests that, prior to occlusion, the models partially rely on shortcut features for classification.  
2) Data leakage constitutes a stable shortcut category: Across all six datasets, removing SII or SNI consistently results in noticeable accuracy drops. In contrast, removing relative artifacts or task-agnostic fields produces less consistent effects. This indicates that strong identifiers serve as critical shortcuts for NTC models across these three task types.  
3) Random masking introduces additional noise: Compared with zero padding, random masking injects extra noise into the traffic features, causing larger average performance degradation. However, spatial or temporal patterns introduced by relative transformation have relatively minor effects compared to the other occlusion strategies.

## VI. DISCUSSION

Shortcut features in encrypted network traffic classification are not universally harmful nor easily dismissed. Instead, their presence and influence are deeply tied to dataset-specific properties, labeling strategies, and operational contexts. We introduce BiasSeeker, a hybrid detection framework that combines statistical analysis with domain-informed validation to identify shortcut-prone features. Beyond this, we argue that feature selection must become a deliberate preliminary step in model design, grounded in thorough assessment of data characteristics and deployment constraints.

## A. The BiasSeeker Framework: A Hybrid Approach

Our goal is to design a model-agnostic framework generalizable across architectures. BiasSeeker implements a three-stage pipeline: (1) data-driven feature ranking, (2) candidate filtering via domain knowledge, and (3) category-specific validation strategies. This structured process integrates data signals with domain reasoning to ensure systematic shortcut identification, moving beyond purely manual approaches while delivering clear, actionable outcomes.

1) Data-Driven Feature Prioritization via AMI: We employ Adjusted Mutual Information (AMI) as a robust, interpretable, and low-cost statistical tool to prioritize features by capturing their first-order correlations with labels. This approach is justified by three key advantages:

• First, AMI serves as a transparent, model-agnostic metric that operates independently of specific models or training dynamics.  
• Second, its ability to detect statistical associations is particularly critical in encrypted traffic contexts where feature semantics are often unknown.  
• Crucially, this method systematically narrows the candidate space of potential shortcut features, compressing the manual inspection scope from hundreds of raw features to a limited candidate set.

By leveraging AMI’s statistical screening instead of relying on prior protocol semantics, we significantly reduce dependency on expert knowledge while maintaining detection efficacy. This strategy proves indispensable for high-dimensional traffic datasets where exhaustive manual feature examination is computationally infeasible.

## 2) Domain-Enhanced Feature Interpretation Pipeline:

Once highly correlated features are identified, we incorporate domain knowledge to interpret their semantics and assess whether they are likely to be spurious or task-relevant. We then categorize these features into intuitive groups, each with an associated validation strategy tailored to its nature.

We acknowledge that the final decision still requires human inspection. However, this is a significant improvement over fully manual processes, which require inspecting hundreds of raw features. BiasSeeker acts as a taxonomy system, highlighting suspicious signals that are more likely to encode datasetspecific bias.

Building an automatic shortcut detector is a challenging open problem. We hope our framework provides a structured first step, and we are actively exploring causal analysis and representation-based criteria for more automated shortcut diagnosis in future work.

Takeaway 1: BiasSeeker effectively narrows down potential shortcut features by combining statistical screening, significantly reducing manual inspection effort, and provides a first step toward automated shortcut detection in high-dimensional traffic datasets.

## B. Shortcut Features Are Contextual, Not Universal

Shortcut features should not be treated as inherently flawed nor universally detrimental. Our study underscores the necessity of dataset-specific, context-aware analysis when identifying and mitigating shortcut behaviors. Across our evaluations, we observe that certain features may act as strong shortcut indicators in some datasets, yet serve valid semantic or operational roles in others. For instance, SNI may be a valid signal in app identification, but fragile in malware detection due to dynamic evasion. These discrepancies arise from variations in traffic composition, network conditions, labeling strategies, and deployment environments.

TABLE III: Classification Accuracies on Different Shortcut Feature Mitigation Strategies

<table><tr><td rowspan="2">Shortcut</td><td rowspan="2">Mitigation Strategy</td><td colspan="2">CrossNet2021 [31]</td><td colspan="2">CSTNET-TLS1.3 [6]</td><td colspan="2">ISCXVPN2016 [27]</td><td colspan="2">SurfsharkVPN [12]</td><td colspan="2">USTC-TFC2016 [29]</td><td colspan="2">Ransomware [28]</td></tr><tr><td>NM</td><td>DT</td><td>NM</td><td>DT</td><td>NM</td><td>DT</td><td>NM</td><td>DT</td><td>NM</td><td>DT</td><td>NM</td><td>DT</td></tr><tr><td>None</td><td>Full Feature</td><td>0.9472</td><td>0.8936</td><td>0.9891</td><td>0.9703</td><td>0.8847</td><td>0.9132</td><td>0.9619</td><td>0.9661</td><td>0.9799</td><td>0.9810</td><td>0.3905</td><td>0.3810</td></tr><tr><td rowspan="4">DL</td><td>Zero SII</td><td>0.9213</td><td>0.8786</td><td>0.9733</td><td>0.9564</td><td>0.8314</td><td>0.8590</td><td>0.9405</td><td>0.9579</td><td>0.9656</td><td>0.9654</td><td>0.2871</td><td>0.2718</td></tr><tr><td>Zero SNI</td><td>0.9294</td><td>0.8794</td><td>0.9862</td><td>0.9657</td><td>0.8858</td><td>0.9143</td><td>0.9776</td><td>0.9598</td><td>0.9840</td><td>0.9797</td><td>0.3785</td><td>0.3696</td></tr><tr><td>Random SII</td><td>0.9164</td><td>0.8561</td><td>0.9812</td><td>0.9576</td><td>0.7821</td><td>0.8339</td><td>0.9155</td><td>0.9440</td><td>0.9732</td><td>0.9680</td><td>0.2552</td><td>0.2574</td></tr><tr><td>Random SNI</td><td>0.9142</td><td>0.8752</td><td>0.9877</td><td>0.9635</td><td>0.8982</td><td>0.9145</td><td>0.9141</td><td>0.9423</td><td>0.9796</td><td>0.9800</td><td>0.4139</td><td>0.3983</td></tr><tr><td rowspan="6">RA</td><td>Zero TCP Timestamp</td><td>0.9333</td><td>0.8830</td><td>0.9839</td><td>0.9623</td><td>0.8708</td><td>0.8771</td><td>0.9585</td><td>0.9474</td><td>0.9840</td><td>0.9820</td><td>0.4075</td><td>0.3495</td></tr><tr><td>Zero SEQ/ACK No</td><td>0.9358</td><td>0.8922</td><td>0.9829</td><td>0.9672</td><td>0.8835</td><td>0.9096</td><td>0.8566</td><td>0.9523</td><td>0.9864</td><td>0.9840</td><td>0.4136</td><td>0.3867</td></tr><tr><td>Relative TCP Timestamp</td><td>0.9416</td><td>0.8984</td><td>0.9857</td><td>0.9617</td><td>0.8697</td><td>0.8835</td><td>0.9373</td><td>0.9508</td><td>0.9813</td><td>0.9787</td><td>0.3877</td><td>0.3732</td></tr><tr><td>Relative SEQ/ACK No</td><td>0.9248</td><td>0.8857</td><td>0.9798</td><td>0.9692</td><td>0.8786</td><td>0.9032</td><td>0.8701</td><td>0.9615</td><td>0.9833</td><td>0.9813</td><td>0.3882</td><td>0.3801</td></tr><tr><td>Random TCP Timestamp</td><td>0.9394</td><td>0.8923</td><td>0.9838</td><td>0.9727</td><td>0.8564</td><td>0.8753</td><td>0.9640</td><td>0.9527</td><td>0.9826</td><td>0.9800</td><td>0.4035</td><td>0.3641</td></tr><tr><td>Random SEQ/ACK No</td><td>0.9250</td><td>0.8787</td><td>0.9880</td><td>0.9713</td><td>0.8890</td><td>0.9012</td><td>0.8527</td><td>0.9547</td><td>0.9847</td><td>0.9803</td><td>0.3632</td><td>0.3888</td></tr><tr><td rowspan="8">TA</td><td>Zero IP TTL</td><td>0.9420</td><td>0.8803</td><td>0.9857</td><td>0.9701</td><td>0.8705</td><td>0.9163</td><td>0.9506</td><td>0.9539</td><td>0.9786</td><td>0.9784</td><td>0.3971</td><td>0.3965</td></tr><tr><td>Zero TCP Window</td><td>0.9281</td><td>0.8667</td><td>0.9880</td><td>0.9481</td><td>0.8898</td><td>0.9077</td><td>0.9598</td><td>0.9456</td><td>0.9863</td><td>0.9756</td><td>0.4057</td><td>0.3810</td></tr><tr><td>Zero IP Checksum</td><td>0.9412</td><td>0.8900</td><td>0.9808</td><td>0.9695</td><td>0.8778</td><td>0.9072</td><td>0.9434</td><td>0.9360</td><td>0.9830</td><td>0.9840</td><td>0.3937</td><td>0.3903</td></tr><tr><td>Zero TCP/UDP Checksum</td><td>0.9406</td><td>0.8910</td><td>0.9859</td><td>0.9641</td><td>0.8844</td><td>0.9201</td><td>0.9431</td><td>0.9544</td><td>0.9829</td><td>0.9776</td><td>0.3871</td><td>0.3988</td></tr><tr><td>Random IP TTL</td><td>0.9197</td><td>0.8606</td><td>0.9898</td><td>0.9682</td><td>0.8691</td><td>0.9019</td><td>0.9051</td><td>0.9486</td><td>0.9797</td><td>0.9810</td><td>0.3611</td><td>0.3664</td></tr><tr><td>Random TCP Window</td><td>0.9201</td><td>0.8652</td><td>0.9857</td><td>0.9562</td><td>0.8825</td><td>0.8996</td><td>0.9231</td><td>0.9346</td><td>0.9808</td><td>0.9810</td><td>0.3984</td><td>0.3739</td></tr><tr><td>Random IP Checksum</td><td>0.9212</td><td>0.8745</td><td>0.9827</td><td>0.9645</td><td>0.8716</td><td>0.9000</td><td>0.9502</td><td>0.9566</td><td>0.9803</td><td>0.9766</td><td>0.3919</td><td>0.3961</td></tr><tr><td>Random TCP/UDP Checksum</td><td>0.9368</td><td>0.8759</td><td>0.9801</td><td>0.9650</td><td>0.8912</td><td>0.9100</td><td>0.9366</td><td>0.9544</td><td>0.9821</td><td>0.9779</td><td>0.4159</td><td>0.3828</td></tr></table>

1 NM: NetMamba, DT: Decision Tree.  
2 DL: Data Leakage, RA: Relative Artifacts, TA: Task Agnostic.  
3 We highlight the metric higher than the full feature in purple and lower in blue.

Importantly, we do not advocate for a blanket exclusion of such fields. In certain scenarios—e.g., controlled industrial deployments or static topologies—these features may yield practical benefits despite limited generalizability. However, their inclusion must be preceded by critical examination of environmental coupling, transferability risks, and labeling entanglement.

Our findings are not intended to be prescriptive or exhaustive but rather to raise awareness. Shortcut detection must be grounded in the specific goals, data properties, and deployment constraints of each use case. Feature selection should thus be an intentional and scenario-sensitive step prior to model training or benchmarking.

Takeaway 2: Shortcut features are not inherently harmful; their impact is highly dataset- and context-dependent. Feature selection should be a scenario-sensitive process that considers environmental coupling and transferability before model training.

## C. Semantic Learning vs. Shortcut Reliance in Encrypted NTC

Our findings prompt a fundamental reconsideration: are current traffic classification models truly capturing the semantic structure of encrypted flows, or are they instead overfitting to superficial, dataset-specific artifacts? As network protocols, application behaviors, and operational environments continue to evolve, models built on brittle correlations—such as fixed IP mappings or length-based heuristics—face rapid obsolescence.

This prompts a rethinking of design goals in encrypted NTC. To foster robust and future-proof classifiers, we advocate for a shift from accuracy-centric optimization to resilienceoriented modeling, and argue that future research should prioritize the following directions:

• Learning semantic, protocol-invariant representations that remain stable across evolving network conditions and deployment scenarios.  
• Systematic detection and mitigation of shortcut features, especially those arising from collection artifacts or labeling leakage.  
• Development of realistic and diverse benchmarks that reflect the operational heterogeneity of real-world environments, rather than static or synthetic setups.

By shifting the focus from short-term accuracy to longterm resilience, the community can better align network traffic classification research with practical deployment needs and evolving security challenges.

Takeaway 3: Many models rely on dataset-specific shortcuts rather than true encrypted-flow semantics. Future work should emphasize resilient, semantic representations and realistic benchmarks over short-term accuracy.

## VII. CONCLUSION

We presented BiasSeeker, a semi-automated framework that combines model-agnostic analysis with data-centric insights to address shortcut learning in encrypted network traffic classification (NTC). Recognizing the limitations of existing approaches—which often depend on expert heuristics or are tightly coupled with specific model architectures—BiasSeeker provides a principled methodology for examining shortcut learning risks inherent in raw traffic data.

Our framework introduces a principled, taxonomy-based understanding of shortcut behaviors, along with categoryspecific mitigation strategies. Extensive evaluations across 19 public datasets spanning three tasks, demonstrate BiasSeeker’s effectiveness in uncovering hidden biases, and enhancing transferability under distribution shifts.

Importantly, BiasSeeker is not intended to prescribe universal solutions, but to promote awareness and provide actionable tools for shortcut diagnosis. We highlight the need for intentional, context-aware feature selection as a critical step before model design and benchmarking.

## REFERENCES

[1] J. Zhang, X. Chen, Y. Xiang, W. Zhou, and J. Wu, “Robust network traffic classification,” IEEE/ACM transactions on networking, vol. 23, no. 4, pp. 1257–1270, 2014.  
[2] Y. Mirsky, T. Doitshman, Y. Elovici, and A. Shabtai, “Kitsune: an ensemble of autoencoders for online network intrusion detection,” arXiv preprint arXiv:1802.09089, 2018.  
[3] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “Fs-net: A flow sequence network for encrypted traffic classification,” in IEEE INFOCOM 2019- IEEE Conference On Computer Communications. IEEE, 2019, pp. 1171–1179.  
[4] J. Piet, D. Nwoji, and V. Paxson, “Ggfast: Automating generation of flexible network traffic classifiers,” in Proceedings of the ACM SIGCOMM 2023 Conference, 2023, pp. 850–866.  
[5] D. Xue, M. Kallitsis, A. Houmansadr, and R. Ensafi, “Fingerprinting obfuscated proxy traffic with encapsulated {TLS} handshakes,” in 33rd USENIX Security Symposium (USENIX Security 24), 2024, pp. 2689– 2706.  
[6] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in Proceedings of the ACM Web Conference 2022, 2022, pp. 633–642.  
[7] R. Zhao, M. Zhan, X. Deng, Y. Wang, Y. Wang, G. Gui, and Z. Xue, “Yet another traffic classifier: A masked autoencoder based traffic transformer with multi-level flow representation,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 37, no. 4, 2023, pp. 5420–5427.  
[8] T. Wang, X. Xie, W. Wang, C. Wang, Y. Zhao, and Y. Cui, “Netmamba: Efficient network traffic classification via pre-training unidirectional mamba,” in 2024 IEEE 32nd International Conference on Network Protocols (ICNP). IEEE, 2024, pp. 1–11.  
[9] L. Peng, X. Xie, S. Huang, Z. Wang, and Y. Cui, “Ptu: Pre-trained model for network traffic understanding,” in 2024 IEEE 32nd International Conference on Network Protocols (ICNP). IEEE, 2024, pp. 1–12.  
[10] G. Zhou, X. Guo, Z. Liu, T. Li, Q. Li, and K. Xu, “Trafficformer: an efficient pre-trained model for traffic data,” in 2025 IEEE Symposium on Security and Privacy (SP). IEEE Computer Society, 2024, pp. 102–102.  
[11] A. S. Jacobs, R. Beltiukov, W. Willinger, R. A. Ferreira, A. Gupta, and L. Z. Granville, “Ai/ml for network security: The emperor has no clothes,” in Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security, 2022, pp. 1537–1551.  
[12] S. Oh, M. Lee, H. Lee, E. Bertino, and H. Kim, “Appsniffer: Towards robust mobile app fingerprinting against vpn,” in Proceedings of the ACM Web Conference 2023, 2023, pp. 2318–2328.  
[13] S. Guthula, R. Beltiukov, N. Battula, W. Guo, and A. Gupta, “netfound: Foundation model for network security,” arXiv preprint arXiv:2310.17025, 2023.  
[14] N. Wickramasinghe, A. Shaghaghi, G. Tsudik, and S. Jha, “ SoK: Decoding the Enigma of Encrypted Network Traffic Classifiers ,” in 2025 IEEE Symposium on Security and Privacy (SP), May 2025, pp. 1825–1843.  
[15] R. Geirhos, J.-H. Jacobsen, C. Michaelis, R. Zemel, W. Brendel, M. Bethge, and F. A. Wichmann, “Shortcut learning in deep neural networks,” Nature Machine Intelligence, vol. 2, no. 11, pp. 665–673, 2020.  
[16] D. Han, Z. Wang, R. Feng, M. Jin, W. Chen, K. Wang, S. Wang, J. Yang, X. Shi, X. Yin et al., “Rules refine the riddle: Global explanation for deep learning-based anomaly detection in security applications,” in Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security, 2024, pp. 4509–4523.  
[17] W. Ye, G. Zheng, X. Cao, Y. Ma, and A. Zhang, “Spurious correlations in machine learning: A survey,” arXiv preprint arXiv:2402.12715, 2024.  
[18] D. Steinmann, F. Divo, M. Kraus, A. Wust, L. Struppek, F. Friedrich, ¨ and K. Kersting, “Navigating shortcuts, spurious correlations, and confounders: From origins via detection to mitigation,” arXiv preprint arXiv:2412.05152, 2024.  
[19] J. Nam, H. Cha, S. Ahn, J. Lee, and J. Shin, “Learning from failure: Debiasing classifier from biased classifier,” Advances in Neural Information Processing Systems, vol. 33, pp. 20 673–20 684, 2020.  
[20] Y. Yang, E. Gan, G. K. Dziugaite, and B. Mirzasoleiman, “Identifying spurious biases early in training through the lens of simplicity bias,” in International Conference on Artificial Intelligence and Statistics. PMLR, 2024, pp. 2953–2961.  
[21] S. Wang, R. Veldhuis, C. Brune, and N. Strisciuglio, “What do neural networks learn in image classification? a frequency shortcut perspective,” in Proceedings of the IEEE/CVF International Conference on Computer Vision, 2023, pp. 1433–1442.  
[22] H. Nori, S. Jenkins, P. Koch, and R. Caruana, “Interpretml: A unified framework for machine learning interpretability,” arXiv preprint arXiv:1909.09223, 2019.  
[23] N. Kokhlikyan, V. Miglani, M. Martin, E. Wang, B. Alsallakh, J. Reynolds, A. Melnikov, N. Kliushkina, C. Araya, S. Yan et al., “Captum: A unified and generic model interpretability library for pytorch,” arXiv preprint arXiv:2009.07896, 2020.  
[24] S. Lapuschkin, S. Waldchen, A. Binder, G. Montavon, W. Samek, and ¨ K.-R. Muller, “Unmasking clever hans predictors and assessing what ¨ machines really learn,” Nature communications, vol. 10, no. 1, p. 1096, 2019.  
[25] N. M. Muller, S. Roschmann, S. Khan, P. Sperl, and K. B ¨ ottinger, ¨ “Shortcut detection with variational autoencoders,” in 2024 International Joint Conference on Neural Networks (IJCNN). IEEE, 2024, pp. 1–7.  
[26] J. Mink, H. Benkraouda, L. Yang, A. Ciptadi, A. Ahmadzadeh, D. Votipka, and G. Wang, “Everybody’s got ml, tell me what else you have: Practitioners’ perception of ml-based security tools and explanations,” in 2023 IEEE Symposium on Security and Privacy (SP). IEEE, 2023, pp. 2068–2085.  
[27] G. D. Gil, A. H. Lashkari, M. Mamun, and A. A. Ghorbani, “Characterization of encrypted and vpn traffic using time-related features,” in Proceedings of the 2nd international conference on information systems security and privacy (ICISSP 2016). SciTePress, 2016, pp. 407–414.  
[28] A. H. Lashkari, A. F. A. Kadir, L. Taheri, and A. A. Ghorbani, “Toward developing a systematic approach to generate benchmark android malware datasets and classification,” 2018 International Carnahan Conference on Security Technology (ICCST), pp. 1–7, 2018. [Online]. Available: https://api.semanticscholar.org/CorpusID:56718203  
[29] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware traffic classification using convolutional neural network for representation learning,” in 2017 International conference on information networking (ICOIN). IEEE, 2017, pp. 712–717.  
[30] J. Ren, D. Dubois, and D. Choffnes, “An international view of privacy risks for mobile apps,” 2019.  
[31] W. Li, X.-Y. Zhang, H. Bao, Q. Wang, and Z. Li, “Robust network traffic identification with graph matching,” Computer Networks, vol. 218, p. 109368, 2022.  
[32] S. Dadkhah, H. Mahdikhani, P. K. Danso, A. Zohourian, K. A. Truong, and A. A. Ghorbani, “Towards the development of a realistic multidimensional iot profiling dataset,” in 2022 19th Annual International Conference on Privacy, Security & Trust (PST). IEEE, 2022, pp. 1–11.  
[33] A. H. Lashkari, G. D. Gil, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of tor traffic using time based features,” in International Conference on Information Systems Security and Privacy, vol. 2. SciTePress, 2017, pp. 253–262.
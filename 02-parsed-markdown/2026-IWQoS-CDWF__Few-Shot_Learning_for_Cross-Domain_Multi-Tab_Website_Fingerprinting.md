# CDWF: Few-Shot Learning for Cross-Domain Multi-Tab Website Fingerprinting

Xinlei Ju <sup>†,</sup> <sup>‡</sup>, Zhen Li<sup>†,</sup> <sup>‡</sup>, Yang Li<sup>†,</sup> <sup>‡</sup>, Lihua Yin<sup>§</sup>, Zhong Guan<sup>†,</sup> <sup>‡,</sup> <sup>\*</sup> Gaopeng Gou<sup>†,</sup> <sup>‡</sup>, Mi Zhou<sup>†,</sup> <sup>‡</sup>, Junzheng Shi<sup>†,</sup> <sup>‡</sup>, and Gang Xiong<sup>†,</sup> <sup>‡</sup>

<sup>†</sup>Institute of Information Engineering, Chinese Academy of Sciences, Beijing, China

<sup>‡</sup>School of Cyber Security, University of Chinese Academy of Sciences, Beijing, China

<sup>§</sup>Cyberspace Institute of Advanced Technology, Guangzhou University, Guangzhou, China

†{jvxinlei, lizhen, liyang2022, guanzhong, gougaopeng, zhoumi, shijunzheng, xionggang}@iie.ac.cn, §yinlh@gzhu.edu.cn

Abstract—Website fingerprinting attacks allow an eavesdropper to determine which websites a user is visiting by analyzing metadata from encrypted traffic, thereby posing a significant threat to online privacy. Most current methods rely on the assumption that a user visits only a single webpage at a time, which fails to account for the prevalence of multi-tab browsing in realistic scenarios. In such environments, traffic from multiple websites is interleaved, and practical attacks are further hindered by the scarcity of target-domain data, which limits the training efficacy and generalization of conventional models. To address these challenges, this paper proposes CDWF, a cross-domain fewshot website fingerprinting framework for multi-tab settings. The framework utilizes a three-stage progressive learning pipeline. First, traffic-augmented pre-training on public datasets extracts generalizable traffic representations through contrastive learning with diverse packet-level perturbations. Next, adversarial domain adaptation to align feature distributions between the source and target domains. Finally, few-shot target adaptation using a minimal set of target-domain samples and their augmented versions for rapid deployment. Experimental results demonstrate that CDWF significantly outperforms existing baselines in closedworld, open-world, and various defense scenarios. CDWF maintains superior robustness and recognition accuracy even when the number of tabs is unknown and under strong defensive conditions. This work provides an effective solution for practical website fingerprinting attacks in environments with limited data and constrained resources.

Index Terms—Multi-tab Website fingerprinting, Tor, Privacy, Few-shot learning, Cross-Domain

## I. INTRODUCTION

The rapid expansion of the Internet and the widespread adoption of various online activities, such as e-commerce and instant messaging, have increased user concerns regarding privacy protection. Consequently, numerous privacy-enhancing technologies have been developed to safeguard web browsing activities. Among these, the Onion Router (Tor) stands as one of the most widely deployed anonymous communication systems [1]. By employing a three-layer relay architecture with multi-layered encryption, Tor provides anonymity for millions of users. However, the anonymity offered by Tor remains vulnerable to website fingerprinting (WF) attacks. In a typical WF attack, an adversary exploits observable network traffic features, including packet direction, size, and timing, to infer users’ browsing behavior [2] [3] [4] [5].

The effectiveness of WF attacks arises from distinct variations in resource composition and traffic patterns among different websites [4] [5]. Existing research typically formulates WF as a supervised classification task. However, the majority of current studies focus exclusively on single-tab scenarios, assuming that users access only one website at a time [6], [7]. This assumption often fails to hold in practical network environments, where users commonly browse multiple websites concurrently. Such multi-tab behavior generates overlapping and interleaved traffic traces, which substantially degrade the performance of conventional single-tab WF classifiers [6].

To address these limitations, several WF methods for concurrent tab browsing have been proposed [8]–[11]. However, existing approaches exhibit three critical limitations:

1) Many frameworks assume a fixed number of concurrent tabs [9], though this number is typically unknown in real networks, limiting practical applicability.

2) Existing methods lack robustness against standard WF defenses; even simple countermeasures like random padding or packet delays substantially degrade performance [10], [12].

3) The combinatorial explosion of possible website combinations in multi-tab browsing necessitates prohibitively large labeled datasets to cover realistic traffic patterns, rendering exhaustive labeling infeasible in practice.

In response to these challenges, we propose CDWF, a three-stage cross-domain few-shot framework for multi-tab website fingerprinting. First, Traffic-Augmented Pre-training leverages self-supervised contrastive learning on public data to learn perturbation-invariant traffic representations, eliminating the need for exhaustive labeled tab combinations. Second, Adversarial Domain Adaptation jointly optimizes classification accuracy and domain confusion, yielding features that are both website-discriminative and invariant to network shifts, thereby enhancing resilience against common defenses. Third, Few-shot Target Adaptation fine-tunes the aligned model with minimal labeled target traces, enabling accurate identification even without prior knowledge of the concurrent tab count.

Experimental results demonstrate the efficacy of CDWF under practical constraints. In closed-world evaluations with 2 tabs, CDWF achieves a mean average precision at 2 (MAP@2) of 95.1%, indicating highly accurate identification of co-browsing websites. More importantly, the framework maintains strong generalization in open-world settings, attaining a MAP@2 of 79.51% with only minimal target-domain supervision. This design enables accurate multi-tab website identification under practical constraints.

In summary, the paper makes the following contributions:

• We propose CDWF, a unified three-stage framework for multi-tab website fingerprinting that addresses domain shift and data scarcity, thereby achieving robust crossenvironment generalization with minimal reliance on target-domain labeling.

• We propose Traffic-Augmented Pre-training, a selfsupervised framework that leverages traffic-aware augmentations to learn robust, domain-invariant representations from unlabeled public datasets via a hybrid CNN-Transformer architecture, thereby enhancing resilience to traffic perturbations and cross-domain distribution shifts.

• We jointly optimize classification and domain discrimination losses to align features across different networks. This produces website-discriminative features invariant to network variations, reducing performance gaps during domain adaptation.

• Our method achieves state-of-the-art performance in concurrent tab fingerprinting, attaining a MAP@2 of 95.1% in closed-world evaluations and 79.51% in open-world scenarios with only minimal target-domain supervision.

## II. RELATED WORK

## A. Single-tab WF Attacks

Single-tab WF attacks typically formulate website identification as a supervised classification task based on encrypted network traffic features. These approaches analyze packet sequences by leveraging observable characteristics such as packet size, direction, and timing to distinguish target websites. Existing methods can be broadly categorized into traditional machine learning and deep learning paradigms.

Traditional approaches rely on handcrafted traffic features combined with classical classifiers, including k-nearest neighbors (k-NN) [4], support vector machines (SVM) [5], [13], and random forests [14]. While effective under controlled conditions, these methods often require extensive feature engineering and exhibit limited adaptability to network variations.

In contrast, deep learning methods automatically extract discriminative representations from raw or minimally processed traffic traces, reducing reliance on manual feature design. Early efforts employed autoencoders for unsupervised representation learning [15]. Recent advances have further enhanced robustness and data efficiency through few-shot learning frameworks [16], domain adaptation techniques to mitigate environmental shifts [17], and self-supervised learning strategies that exploit unlabeled traffic for pre-training [18]– [20]. These developments have progressively narrowed the performance gap between idealized laboratory settings and practical deployment scenarios.

Critically, all these methods assume users visit only one website per session. This limitation significantly reduces practical applicability, as real-world browsing typically involves multiple concurrent sites whose interleaved traffic interferes with single-tab identification.

## B. Multi-tab WF Attacks

Research on multi-tab WF has emerged to address the limitations of single-tab assumptions and better model realistic browsing behavior [6]. Existing approaches can be broadly categorized into two paradigms: traffic disaggregation, which seeks to isolate individual website flows from interleaved traffic sequences, and end-to-end recognition, which directly classifies composite traffic without explicit segmentation.

Early disaggregation approaches focused on segmenting mixed traffic. Wang et al. [7] split two-tab sequences using k-NN, while Yin et al. [9] identified page boundaries for clean packet classification. Cui et al. [21] extracted initial and final packets for two-tab identification. These methods are limited by fixed tab counts and sensitivity to packet segmentation errors, especially under high traffic overlap.

Recent end-to-end methods bypass explicit segmentation. BAPM [22] uses attention mechanisms to aggregate webpagespecific features from raw traffic. TMWF [23] employs Transformer queries for simultaneous multi-website recognition. FMWF [11] combines transfer learning and data augmentation for data-limited scenarios. While avoiding segmentation errors, these approaches still struggle with performance degradation when applied across different network environments.

Current solutions inadequately address distribution shifts between training and deployment networks. This gap limits practical applicability in heterogeneous real-world settings where traffic characteristics vary significantly.

## C. WF Defenses

WF defenses aim to thwart attacks by eliminating identifiable patterns in encrypted traffic. Tamaraw [2] maintains a constant transmission rate and packet size by combining dummy packet insertion with real packet delays, thereby obfuscating traffic features. WTF-PAD [12] employs an adaptive padding strategy that dynamically injects dummy packets during traffic imbalance and idle periods to mask request–response interaction patterns. This method, which maintains two histograms to randomly insert dummy packets when the channel is idle, achieves low-latency, low-overhead protection. Studies indicate that the discriminative features relied upon by most attacks are concentrated within the first few seconds after connection establishment; thus, disrupting traffic during this initial period can significantly degrade attack performance. Building on this, FRONT [24] randomizes the number and distribution of dummy packets in early-stage traffic to enhance defense. RegulaTor [25] reorganizes webpage traffic into consecutive decaying bursts that concentrate transmissions within short intervals, further masking original traffic characteristics through strategic dummy insertion and packet delay.

![](images/c527816f2d242fd22d1b9f02cda9a67e8516bc75e25a8d8ded65b27f71e1f3f1.jpg)  
Fig. 1. Threat Model for Flow Correlation.

## D. Cross-Domain

Acquiring sufficient labeled training data in target networks remains a significant challenge for multi-tab website fingerprinting. Although researchers can leverage publicly available datasets, this approach introduces domain shift, referring to distributional discrepancies between source and target network environments that degrade model performance. Such degradation arises because conventional machine learning methods assume that training and testing data are independently and identically distributed (i.i.d.), an assumption often violated in cross-environment deployments.

In single-tab fingerprinting, domain shift causes performance drops across different network conditions [26] or against traffic obfuscation defenses [6]. Solutions include discriminative feature learning [26], snapshot ensembles for concept drift [27], and adversarial domain adaptation [17]. Recent approaches combine data augmentation with selfsupervision [28] or distribution calibration [19] to improve cross-environment robustness.

However, these methods target single-tab scenarios. Concurrent tab browsing creates complex interleaved traffic where page flows overlap, making feature extraction fundamentally harder. This work addresses the dual challenges of limited labeled data and cross-domain distribution shift in multi-tab settings, a gap that remains unresolved by conventional singletab adaptation techniques.

## III. THREAT MODEL

This study assumes users employ privacy tools like Tor while browsing multiple websites simultaneously. The adversary is a passive observer such as an internet service provider or network administrator positioned between the user and the Tor entry node [5] [11] [23], as shown in Fig. 1. The attacker cannot modify traffic through injection, delay, or dropping packets, and only observes metadata from encrypted flows:

packet timestamps, sizes, and directions. Based on this sidechannel information, the adversary applies a trained deep learning model to identify concurrently visited websites via multi-label classification.

Since users may access multiple websites simultaneously or in rapid succession, the resulting traffic flows are multiplexed over the common link between the user and the Tor entry node. Consequently, the traffic captured by the adversary is inherently an interleaved composite of multiple website flows. Furthermore, the potential deployment of WF defenses at the user’s browser introduces additional entropy, further complicating the extraction of salient traffic features.

We consider a resource-constrained adversary unable to collect large-scale labeled multi-tab traffic in the target network. The combinatorial explosion of concurrent website combinations renders exhaustive data collection infeasible, as it risks network disruption, attack exposure, and privilege violations. Consequently, the adversary relies on a large public source dataset, supplemented by a minimal set of labeled targetdomain traces, for model training and adaptation.

We evaluate CDWF under two standard paradigms. In the closed-world setting, users only visit a predefined set of monitored websites, and the adversary obtains limited target traffic from these domains. In the more realistic open-world setting, users browse arbitrary sites, while the attacker only holds fingerprints for the monitored list. The task thus reduces to binary detection: determining whether any monitored site was visited among concurrent tabs.

## IV. METHOD

## A. Overview

To address the challenges of data scarcity and cross-domain generalization in multi-tab website fingerprinting, we propose CDWF, a three-stage cross-domain few-shot attack framework. As illustrated in Fig. 2, CDWF progressively adapts models from source to target domains while minimizing reliance on labeled target data.

The framework operates through three sequential stages. First, Traffic-augmented pre-training leverages a largescale public dataset to learn generalized traffic representations from raw packet sequences, establishing a robust feature foundation. Second, adversarial domain adaptation jointly utilizes labeled source-domain data and unlabeled targetdomain traffic. Through adversarial training between a feature extractor and a domain discriminator, this stage produces domain-invariant representations that mitigate distributional shifts across network environments. Third, few-shot target adaptation fine-tunes the model using minimally labeled target samples enhanced by traffic-aware augmentation, enabling accurate concurrent website identification under realistic data constraints. This sequential design decouples representation learning from domain alignment and task-specific adaptation, substantially reducing target-domain labeling costs while enabling lightweight deployment in dynamic network environments.

![](images/74c21cad8aef15c9c489594f9feb5ba0e19d0d1fc4cdf2a374ff32ffce0d6d6c.jpg)  
Fig. 2. The overview of CDWF.

## B. Traffic-Augmented Pre-training

This stage trains a general-purpose feature extractor using large-scale unlabeled public traffic data without manual annotation. It addresses a key limitation of conventional fewshot website fingerprinting approaches: although such methods adapt with minimal labeled samples during fine-tuning, they still require substantial labeled data for pre-training.

Self-Supervised Pre-training Strategy. Following the Sim-Siam framework, we construct a Siamese network with sharedweight feature extractors to embed two augmented views of the same traffic sequence. To prevent representation collapse, a phenomenon in which the model maps all inputs to an indistinguishable constant vector, we introduce architectural asymmetry through a predictor head combined with a stopgradient operation. Specifically, one branch actively predicts the representation of the other branch, while gradients from the target branch are stopped during back-propagation. This design enables the model to learn discriminative representations simply by pulling the features of different augmented views of the same sequence closer together, without requiring explicitly constructed negative pairs.

Concretely, the encoder consists of the aforementioned feature extractor followed by a three-layer MLP projection head, and the predictor is implemented as a two-layer MLP. For each original traffic sequence $\mathbf { x } _ { i } ~ \in ~ { \mathcal { X } }$ , we generate two augmented views $\mathbf { x } _ { i } ^ { ( 1 ) }$ and $\mathbf { x } _ { i } ^ { ( 2 ) }$ using four types of traffic-specific augmentations:

• Insert injects background noise packets at a rate of 0.5% to 2% of the original sequence length to simulate concurrent traffic;

• Delete randomly removes 0.5% to 2% of packets to emulate network loss;

• Swap exchanges adjacent packet pairs with a probability of 2% to disrupt local ordering;

• Flip reverses the direction flags of 2% of packets to perturb uplink/downlink patterns.

Insert and Delete are applied to every view as mandatory perturbations, while Swap and Flip are optional and triggered independently with a 10% probability to increase augmentation diversity. Given an augmented pair $( \mathbf { x } _ { i } ^ { ( 1 ) } , \mathbf { x } _ { i } ^ { ( 2 ) } )$ , the shared-weight encoder $f _ { \Theta }$ extracts features, yielding projected vectors $( p _ { i } ^ { ( \ 1 ) } , p _ { i } ^ { ( 2 ) } )$ . These are then passed through the predictor head to obtain the predicted vectors $( z _ { i } ^ { ( 1 ) } , z _ { i } ^ { ( 2 ) } )$ ). The final loss is defined as the symmetrized negative cosine similarity:

![](images/43feaadbf4ca4a695b867c8a64c36e5bfda75f0f573ec8ea47c1ad13636e101b.jpg)  
Fig. 3. The feature extractor of CDWF.

$$
\mathcal {L} _ {i} = - \frac {1}{2} \left[ D \left(\mathbf {p} _ {i} ^ {(1)}, \operatorname{sg} \left(\mathbf {z} _ {i} ^ {(2)}\right)\right) + D \left(\mathbf {p} _ {i} ^ {(2)}, \operatorname{sg} \left(\mathbf {z} _ {i} ^ {(1)}\right)\right) \right],\tag{1}
$$

where $D ( \mathbf { u } , \mathbf { v } ) \ = \ { \frac { \mathbf { u } ^ { \top } \mathbf { v } } { \| \mathbf { u } \| \left\| \mathbf { v } \right\| } }$ denotes the negative cosine similarity, and sg(·) indicates that gradients are stopped for the argument.

The self-supervised pre-training phase enables the model to learn domain-invariant representations that are robust to traffic perturbations and domain shifts. This process prepares the model for the subsequent few-shot adaptation stage and requires no labeled data from the target domain.

Feature Extractor Architecture. The feature extractor adopts a hybrid architecture combining convolutional and Transformer modules to process raw packet sequences. First, the input sequence passes through M convolutional blocks (each comprising batch normalization and pooling operations) to capture local statistical patterns and short-term temporal features. The extracted features are then fed into N Transformer blocks, which model long-range global dependencies through a hierarchical attention mechanism. Specifically, we integrate full attention with Top-k attention, focusing progressively on discriminative traffic burst patterns as the representation transitions from local details to global structure. This design effectively enhances the model’s robustness to perturbations introduced by WF defenses such as traffic obfuscation and padding. The complete architecture is illustrated in Fig. 3.

In Top-k Attention, only the most relevant k key-value pairs are retained for each query. After computing the attention logits, the top-k values in each row are preserved, while the remaining positions are set to negative infinity:

$$
\tilde {\mathbf {A}} _ {i,:} = \left\{ \begin{array}{l l} \frac {\mathbf {q} _ {i} \mathbf {k} _ {j} ^ {\top}}{\sqrt {d}}, & \text { if } j \in \mathcal {T} _ {i} \\ - \infty , & \text { otherwise } \end{array} \right.\tag{2}
$$

where $\mathcal { T } _ { i } = \mathrm { T o p K } \left( \left\{ \mathbf { q } _ { i } \mathbf { k } _ { j } ^ { \top } \right\} _ { i = 1 } ^ { N } , K = M \right)$ denotes the set of indices of the top-M keys for the i-th query. The final attention output is given by:

$$
\mathrm{Topk-Attention} (\mathbf {Q}, \mathbf {K}, \mathbf {V}) = \mathrm{Softmax} (\tilde {\mathbf {A}}) \mathbf {V}\tag{3}
$$

## C. Adversarial Domain Adaptation

This stage adapts the pre-trained feature extractor to produce domain invariant representations by integrating labeled source domain data with unlabeled target domain traffic. The goal is to generate features that are statistically indistinguishable across different network environments.

We augment the feature extractor with two modules: a multi class classifier for website identification and a binary domain discriminator. During training, each mini batch contains samples from both domains. Source samples feed into the classifier to compute cross entropy loss, while target samples pass to the domain discriminator for domain discrimination loss. Classification loss updates both the feature extractor and classifier through standard backpropagation. Domain discrimination loss flows through a gradient reversal layer that inverts gradient signs during backpropagation. This compels the feature extractor to generate domain agnostic features that confuse the discriminator. The total loss combines both components:

$$
\mathcal {L} _ {\text { total }} = \mathcal {L} _ {\text { cls }} + \lambda \cdot \mathcal {L} _ {\text { adv }}\tag{4}
$$

where the hyperparameter λ balances the contributions of the two loss terms.

Classification Loss $L _ { \mathrm { c l s } }$ . This term is the standard multiclass cross-entropy loss, which ensures accurate classification of source-domain samples:

$$
\mathcal {L} _ {\mathrm{cls}} = - \frac {1}{N _ {s}} \sum_ {i = 1} ^ {N _ {s}} \sum_ {c = 1} ^ {C} y _ {i, c} \log (\hat {y} _ {i, c})\tag{5}
$$

where $N _ { s }$ is the number of source-domain samples, C is the total number of classes, $y _ { i , c }$ is the ground-truth label (one-hot vector) of sample i, and $\hat { y } _ { i , c }$ is the predicted probability that sample i belongs to class c.

Adversarial Loss $L _ { \mathrm { a d v } }$ . This term is realized by a domain discriminator DA, which takes the features produced by the feature extractor $G _ { f }$ as input and encourages $G _ { f }$ to learn domain-invariant features.

$$
\mathcal {D} _ {m} ^ {n} = D A (G _ {f} (x _ {m} ^ {n}))\tag{6}
$$

$$
\mathcal {L} _ {\mathrm{adv}} = - \frac {1}{N _ {s} + N _ {t}} \left[ \sum_ {i = 1} ^ {N _ {s}} \log (1 - D _ {i} ^ {s}) + \sum_ {j = 1} ^ {N _ {t}} \log (D _ {j} ^ {t}) \right]\tag{7}
$$

where $D _ { i } ^ { s }$ denote the discriminator’s output (i.e., the predicted probability of belonging to the target domain) for the i-th source-domain sample, and $D _ { j } ^ { t }$ the corresponding output for the j-th target-domain sample. This loss function operates in conjunction with a gradient reversal layer: the feature extractor $G _ { f }$ is trained to maximize $L _ { \mathrm { a d v } }$ , thereby confusing the domain discriminator. Conversely, the domain discriminator D is trained to minimize $L _ { \mathrm { a d v } }$

After adversarial training, the feature extractor produces domain invariant representations with two essential properties: First, features retain sufficient discriminative power to distinguish different websites. Second, features remain consistent across source and target network environments despite distribution shifts. This joint optimization of discriminative feature learning and domain invariance yields accurate website identification with robust generalization across heterogeneous network environments.

## D. Few-Shot Target Adaptation

This final stage achieves rapid adaptation to the target domain by fine-tuning the model (inherited from the domainadversarial stage) with only a few labeled samples. To combat overfitting under extreme data scarcity, we employ a targeted data augmentation strategy that expands the effective training set without additional labeling cost.

We apply two random perturbation operations to each labeled sequence: random packet insertion to simulate background or cross-tab traffic interference, and random packet deletion to emulate network packet loss. Crucially, the proportion of inserted or deleted packets is kept within a low range (5%–15%). This ensures that the global structure and discriminative burst patterns of the original traffic are preserved, while preventing the model from over-relying on fragile, sequencespecific details. The augmented and original samples together form the support set for fine-tuning.

We freeze the feature extractor’s lower layers and only finetune the top Transformer blocks and the classifier head using a small learning rate. This allows the model to subtly adjust its previously learned domain-invariant representations to the specific distribution of the target domain, while maintaining stability. The combination of limited updates and augmented data diversity effectively boosts the model’s tolerance to noise and its final classification performance, enabling robust fewshot recognition even in complex multi-tab environments.

## V. EXPERIMENTAL EVALUATIONS

## A. Experimental Setup

Datasets. We evaluate CDWF across three multi-tab scenarios to assess cross-environment generalization. Following established practices [11], we partition each target domain dataset into three parts: a small labeled subset for fine-tuning, unlabeled data for domain adversarial training, and the remaining samples equally divided into five folds for testing. All results are averaged over five independent runs to ensure statistical reliability. This strategy ensures consistent evaluation while reflecting practical data constraints. The detailed statistics of the three datasets are shown in Table I.

TABLE I  
SUMMARY OF MULTI-TAB WF DATASETS.

<table><tr><td>Dataset</td><td>CW Traces</td><td>OW Traces</td><td>Classes</td></tr><tr><td>Meng Dataset [11]</td><td>10k×5</td><td>1.1k</td><td>100(+1)</td></tr><tr><td>Deng Dataset [10]</td><td>58k×5</td><td>64k×5</td><td>100(+1)</td></tr><tr><td>Defense Dataset [29]</td><td>58k×3</td><td>-</td><td>100</td></tr></table>

• Meng Dataset [11]: Traffic from Alexa Top 100 sites collected across 15 geographically distributed servers. Contains 10,000 closed-world traces per tab configuration (2 to 5 tabs); open-world evaluation uses 1,100 traces from the 2-tab scenario.

• Deng Dataset [10]: The largest publicly available realworld concurrent tab dataset, captured via Seleniumdriven Tor Browser. Each trace is labeled with an orderagnostic 100-dimensional multi-hot vector, comprising 58,000 closed-world and 64,000 open-world traces per tab configuration (2 to 5 tabs).

• Defense Enhanced Dataset [29]: Synthesized traces generated via TMWF methodology with random overlap ratios (0.1 to 0.5) to model traffic interleaving, incorporating standard countermeasures including random padding and packet timing perturbations for robust defense evaluation.

Baseline Methods. All baselines receive data access aligned with their original designs: identical source labels and fewshot target samples as CDWF, with unlabeled target traffic provided only to methods natively supporting domain adaptation. Evaluation is conducted on the same target test set. We select four state-of-the-art multi-tab WF approaches:

• BAPM [22] pioneers end-to-end multi-tab WF by directly processing raw interleaved traffic without explicit flow segmentation.

• ARES [10] employs a hybrid CNN and multi-head top-M attention architecture to extract local traffic patterns and associate them with website fingerprints.

• TMWF [23] addresses variable tab counts by introducing learnable query vectors that retrieve webpage-specific features from a global traffic representation.

TABLE II  
NETWORK ARCHITECTURE CONFIGURATION

<table><tr><td>Component</td><td>Parameter</td><td>Value</td></tr><tr><td rowspan="5">CNN Module</td><td>Number of blocks</td><td>4</td></tr><tr><td>Filters per block</td><td>[32, 64, 128, 256]</td></tr><tr><td>Kernel size</td><td>[8, 8, 8, 8]</td></tr><tr><td>Pooling size</td><td>[8, 8, 8, 8]</td></tr><tr><td>Output dimension</td><td>256</td></tr><tr><td rowspan="3">Transformer Module</td><td>Number of blocks</td><td>4</td></tr><tr><td>Attention heads</td><td>8</td></tr><tr><td>Attention schedule</td><td>[full, full, top-32, top-16]</td></tr></table>

• FMWF [11] mitigates data scarcity through synthetic-toreal transfer learning, pre-training on simulated traces and adapting to real traffic with minimal labeled samples.

Implementation Details. All experiments are implemented in Python 3.8.2 and executed on an NVIDIA V100 GPU. The input sequence length is fixed at 10,000 packets. During the adversarial domain adaptation stage, the feature extractor, multi-label classifier, and domain discriminator are optimized synchronously within a unified training loop via joint backpropagation. Network architecture parameters and training hyperparameters are summarized in Table II.

Metrics. We evaluate multi-tab identification using standard multi-label metrics: Top-k precision (P@k), mean average precision (MAP@k), Top-k hit rate (Hit@k), Precision, Recall and F1-score. Let N be the monitored website count. For each session, ground truth $y \in \{ 0 , 1 \} ^ { N }$ indicates visited sites, while predictions $\hat { y } \in [ 0 , 1 ] ^ { N }$ give visitation probabilities. The top-k sites with highest yˆ values form the predicted set.

P@k measures precision in top-k predictions:

$$
\mathbf {P @} k = \frac {1}{k} \sum_ {j \in \mathrm{Top} _ {k} (\hat {y})} y _ {j}\tag{8}
$$

MAP@k extends this by weighting early correct predictions more heavily:

$$
\mathbf {M A P @} k = \frac {1}{k} \sum_ {i = 1} ^ {k} \mathbf {P @} i\tag{9}
$$

Hit@k indicates success if any ground-truth site appears in top-k predictions:

$$
\operatorname{Hit} @ k = \mathbb {I} (\mathcal {R} \cap \{r _ {1}, \dots , r _ {k} \} \neq \emptyset)\tag{10}
$$

where I (·) denotes the indicator function, which equals 1 if the condition inside is true and 0 otherwise.

The AUC evaluates the model’s overall ability to distinguish between positive and negative samples by considering its performance across all possible classification thresholds, as given by:

$$
\mathrm{AUC} _ {\text {samples}} = \frac {\sum_ {p \in \mathcal {P}} \sum_ {n \in \mathcal {N}} \left[ \mathbb {I} (\hat {y} _ {p} > \hat {y} _ {n}) + \frac {1}{2} \mathbb {I} (\hat {y} _ {p} = \hat {y} _ {n}) \right]}{| \mathcal {P} | \cdot | \mathcal {N} |}\tag{11}
$$

where P denotes the set of all positive samples (i.e., visited websites) in the test set, and N denotes the set of all negative samples (non-visited websites).

![](images/817f916c5cf6f7d4f37aadae2272cc63b647706055f200f515b88eebcc621ffd.jpg)  
Fig. 4. Comparison of CDWF with state-of-the-art multi-tab WF attacks.

We also employ Precision, Recall and F1-score. These metrics are computed by first calculating precision and recall for each website individually, then averaging the results. Precision and F1-score are derived from standard confusion matrix metrics (TP, FP, TN, FN) with F1-score defined as the harmonic mean of precision and recall. There metrics can be computed as: $\begin{array} { r } { \mathrm { P r e c i s i o n } = \frac { T P } { T P + F P } } \end{array}$ , Recall $\begin{array} { r } { \mathbf { \Phi } = \frac { T P } { T P + F N } } \end{array}$ and $\begin{array} { r } { \mathrm { F 1 - s c o r e } = \frac { \mathrm { 2 \cdot T P } } { \mathrm { 2 \cdot T P + F P + F N } } } \end{array}$

## B. Closed-world Evaluation

We evaluate CDWF in the closed world setting using the Meng Dataset [11] for pretraining and the Deng Dataset [10] as target domain data. We compare against leading baselines with performance assessed through five fold cross validation. Final results represent averages over five independent runs to ensure statistical reliability.

Precision Comparison. Figure 4 compares the precision of different methods in the closed-world scenario across varying tab counts and fine-tuning sample sizes $( N = 1 , 3 , 5 , 7 , 1 0 )$ Overall, CDWF outperforms all baselines in the vast majority of experimental settings. CDWF achieves the highest precision in the vast majority of experimental settings. The only exception occurs in the 2-tab case with $N = 1$ , where ARES slightly exceeds CDWF. Results further indicate that precision generally improves with larger N while declining as the number of concurrent tabs increases, reflecting the growing complexity of traffic disentanglement.

Ranking Performance. Table III presents the P@K and MAP@K for each method under different settings. The data show that CDWF significantly outperforms all compared baselines in both P@K and MAP@K across nearly all combinations of tab numbers and sample sizes N. Even under the highly constrained scenario of $N = 1$ , CDWF demonstrates strong robustness. The only exceptions occur in the 2-tab case, where ARES surpasses CDWF by 1.44% and 1.22% in P@2 and MAP@2, respectively. As N increases, the performance advantage of CDWF becomes more pronounced, reaching its peak and largest margin at N = 10. Moreover, CDWF exhibits better adaptability to complex multi-tab scenarios: although all methods degrade as the number of tabs grows from 2 to 5, CDWF shows the smallest decline. Its superiority is most evident in the most challenging 5-tab setting. For instance, at

$N = 1 0 .$ CDWF outperforms the second-best method ARES by 12.45% and 8.42% in P@5 and MAP@5, respectively. These results indicate that CDWF not only achieves higher predictive confidence and a lower false positive rate, but also consistently ranks truly visited websites higher in its prediction list. This capability is of critical practical value for an attacker to quickly identify target websites.

![](images/598d66ef95f89953875308083523ecdd81dc422fbaa4f718de1c3a3f9e3dd025.jpg)  
Fig. 5. Comparison with existing multi-tab WF attacks in the multi-label classification evaluation, where P@K is the precision at top k.

Ranking Stability Analysis. To evaluate ranking stability, we analyze P@k across different k values. As Figure 5 shows, CDWF consistently outperforms all baselines across all tab configurations. Even in the most complex five concurrent tab scenario, CDWF maintains P@5 above 0.80 while all competing methods remain below 0.75. CDWF exhibits superior stability as k increases, with the slowest performance decline among all methods. In contrast, TMWF suffers significant degradation in high tab-count settings, while BAPM and FMWF show moderate but inconsistent performance. These results confirm that CDWF achieves both robustness and high recognition accuracy in complex concurrent browsing environments, enabling reliable identification of multiple visited websites under challenging traffic conditions.

TABLE III  
COMPARISONS WITH PRIOR ARTS WITH DIFFERENT TABS AND SAMPLE NUMBERS (N) IN THE CLOSED-WORLD.

<table><tr><td rowspan="2">Method</td><td rowspan="2">N</td><td colspan="2">2-tab</td><td colspan="2">3-tab</td><td colspan="2">4-tab</td><td colspan="2">5-tab</td></tr><tr><td>P@2</td><td>MAP@2</td><td>P@3</td><td>MAP@3</td><td>P@4</td><td>MAP@4</td><td>P@5</td><td>MAP@5</td></tr><tr><td rowspan="5">BAPM</td><td>1</td><td> $24.07 \pm 0.36$ </td><td> $28.31 \pm 0.59$ </td><td> $17.30 \pm 0.25$ </td><td> $20.6 \pm 0.38$ </td><td> $14.90 \pm 0.37$ </td><td> $17.81 \pm 0.45$ </td><td> $13.66 \pm 0.22$ </td><td> $16.20 \pm 0.42$ </td></tr><tr><td>3</td><td> $34.64 \pm 0.48$ </td><td> $41.05 \pm 0.57$ </td><td> $27.88 \pm 0.23$ </td><td> $34.50 \pm 0.33$ </td><td> $23.33 \pm 0.33$ </td><td> $28.81 \pm 0.39$ </td><td> $20.01 \pm 0.42$ </td><td> $24.31 \pm 0.54$ </td></tr><tr><td>5</td><td> $41.08 \pm 0.48$ </td><td> $48.03 \pm 0.49$ </td><td> $35.65 \pm 0.72$ </td><td> $43.09 \pm 0.74$ </td><td> $30.58 \pm 0.08$ </td><td> $37.40 \pm 0.32$ </td><td> $25.47 \pm 0.36$ </td><td> $31.14 \pm 0.37$ </td></tr><tr><td>7</td><td> $46.22 \pm 0.42$ </td><td> $53.36 \pm 0.45$ </td><td> $40.04 \pm 0.61$ </td><td> $47.93 \pm 1.07$ </td><td> $24.10 \pm 0.35$ </td><td> $41.43 \pm 0.30$ </td><td> $29.17 \pm 0.33$ </td><td> $35.62 \pm 0.29$ </td></tr><tr><td>10</td><td> $51.07 \pm 0.26$ </td><td> $58.44 \pm 0.37$ </td><td> $46.31 \pm 0.98$ </td><td> $54.16 \pm 0.83$ </td><td> $41.16 \pm 0.51$ </td><td> $49.01 \pm 0.56$ </td><td> $34.34 \pm 0.24$ </td><td> $41.53 \pm 0.46$ </td></tr><tr><td rowspan="5">ARES</td><td>1</td><td> $44.17 \pm 0.51$ </td><td> $54.10 \pm 0.58$ </td><td> $34.41 \pm 0.69$ </td><td> $45.05 \pm 0.90$ </td><td> $27.38 \pm 0.31$ </td><td> $37.37 \pm 0.40$ </td><td> $20.35 \pm 0.21$ </td><td> $26.92 \pm 0.37$ </td></tr><tr><td>3</td><td> $59.66 \pm 0.44$ </td><td> $69.84 \pm 0.54$ </td><td> $52.90 \pm 0.86$ </td><td> $65.52 \pm 0.93$ </td><td> $43.76 \pm 0.49$ </td><td> $56.98 \pm 0.43$ </td><td> $35.26 \pm 0.66$ </td><td> $46.13 \pm 0.87$ </td></tr><tr><td>5</td><td> $66.26 \pm 0.33$ </td><td> $75.73 \pm 0.32$ </td><td> $62.11 \pm 0.52$ </td><td> $72.23 \pm 0.47$ </td><td> $54.54 \pm 0.41$ </td><td> $66.67 \pm 0.33$ </td><td> $46.79 \pm 0.64$ </td><td> $58.04 \pm 0.73$ </td></tr><tr><td>7</td><td> $70.20 \pm 0.41$ </td><td> $78.73 \pm 0.44$ </td><td> $69.38 \pm 0.58$ </td><td> $78.64 \pm 0.41$ </td><td> $63.49 \pm 0.15$ </td><td> $73.98 \pm 0.13$ </td><td> $55.25 \pm 0.52$ </td><td> $65.74 \pm 0.66$ </td></tr><tr><td>10</td><td> $75.06 \pm 0.28$ </td><td> $82.53 \pm 0.31$ </td><td> $75.06 \pm 0.57$ </td><td> $81.91 \pm 0.49$ </td><td> $71.30 \pm 0.33$ </td><td> $79.83 \pm 0.33$ </td><td> $63.35 \pm 0.39$ </td><td> $72.43 \pm 0.33$ </td></tr><tr><td rowspan="5">TMWF</td><td>1</td><td> $22.12 \pm 0.47$ </td><td> $26.09 \pm 0.39$ </td><td> $15.45 \pm 0.31$ </td><td> $18.18 \pm 0.36$ </td><td> $13.66 \pm 0.19$ </td><td> $16.42 \pm 0.33$ </td><td> $11.81 \pm 0.06$ </td><td> $13.79 \pm 0.06$ </td></tr><tr><td>3</td><td> $22.57 \pm 0.19$ </td><td> $26.09 \pm 0.01$ </td><td> $15.94 \pm 0.32$ </td><td> $18.54 \pm 0.38$ </td><td> $19.32 \pm 0.26$ </td><td> $24.23 \pm 0.43$ </td><td> $20.60 \pm 0.57$ </td><td> $25.09 \pm 0.64$ </td></tr><tr><td>5</td><td> $32.16 \pm 0.41$ </td><td> $38.07 \pm 0.58$ </td><td> $19.15 \pm 0.39$ </td><td> $23.35 \pm 0.51$ </td><td> $21.24 \pm 0.29$ </td><td> $26.83 \pm 0.39$ </td><td> $21.53 \pm 0.26$ </td><td> $27.37 \pm 0.51$ </td></tr><tr><td>7</td><td> $41.78 \pm 0.28$ </td><td> $49.69 \pm 0.39$ </td><td> $25.25 \pm 0.37$ </td><td> $31.89 \pm 0.51$ </td><td> $33.65 \pm 0.39$ </td><td> $41.17 \pm 0.47$ </td><td> $24.06 \pm 0.34$ </td><td> $30.06 \pm 0.33$ </td></tr><tr><td>10</td><td> $43.39 \pm 0.39$ </td><td> $50.90 \pm 0.34$ </td><td> $47.96 \pm 0.51$ </td><td> $57.74 \pm 0.51$ </td><td> $36.58 \pm 0.35$ </td><td> $44.61 \pm 0.33$ </td><td> $29.43 \pm 0.48$ </td><td> $36.76 \pm 0.62$ </td></tr><tr><td rowspan="5">FMWF</td><td>1</td><td> $33.51 \pm 0.18$ </td><td> $40.89 \pm 0.22$ </td><td> $25.36 \pm 0.59$ </td><td> $32.71 \pm 0.54$ </td><td> $17.87 \pm 0.19$ </td><td> $22.93 \pm 0.40$ </td><td> $16.53 \pm 0.24$ </td><td> $21.08 \pm 0.28$ </td></tr><tr><td>3</td><td> $53.07 \pm 0.56$ </td><td> $63.19 \pm 0.62$ </td><td> $42.83 \pm 0.56$ </td><td> $54.28 \pm 0.54$ </td><td> $32.15 \pm 0.17$ </td><td> $42.37 \pm 0.21$ </td><td> $25.09 \pm 0.36$ </td><td> $32.86 \pm 0.54$ </td></tr><tr><td>5</td><td> $59.67 \pm 0.62$ </td><td> $69.33 \pm 0.77$ </td><td> $50.74 \pm 0.23$ </td><td> $62.71 \pm 0.20$ </td><td> $40.52 \pm 0.25$ </td><td> $55.20 \pm 0.37$ </td><td> $31.26 \pm 0.33$ </td><td> $40.70 \pm 0.48$ </td></tr><tr><td>7</td><td> $63.98 \pm 0.49$ </td><td> $73.56 \pm 0.53$ </td><td> $55.09 \pm 0.38$ </td><td> $67.81 \pm 0.43$ </td><td> $45.78 \pm 0.38$ </td><td> $57.44 \pm 0.30$ </td><td> $35.83 \pm 0.60$ </td><td> $46.52 \pm 0.70$ </td></tr><tr><td>10</td><td> $68.59 \pm 0.43$ </td><td> $77.46 \pm 0.47$ </td><td> $62.27 \pm 0.50$ </td><td> $73.36 \pm 0.24$ </td><td> $52.76 \pm 0.42$ </td><td> $64.33 \pm 0.29$ </td><td> $41.52 \pm 0.66$ </td><td> $52.75 \pm 0.77$ </td></tr><tr><td rowspan="5">CDWF</td><td>1</td><td> $42.73 \pm 0.31$ </td><td> $52.88 \pm 0.55$ </td><td> $37.05 \pm 0.35$ </td><td> $48.17 \pm 0.53$ </td><td> $28.85 \pm 0.22$ </td><td> $38.61 \pm 0.23$ </td><td> $22.94 \pm 0.29$ </td><td> $29.99 \pm 0.48$ </td></tr><tr><td>3</td><td> $61.94 \pm 0.52$ </td><td> $71.79 \pm 0.52$ </td><td> $60.20 \pm 0.33$ </td><td> $71.15 \pm 1.17$ </td><td> $50.90 \pm 0.33$ </td><td> $62.44 \pm 0.46$ </td><td> $45.64 \pm 0.47$ </td><td> $55.80 \pm 0.56$ </td></tr><tr><td>5</td><td> $70.32 \pm 0.21$ </td><td> $78.80 \pm 0.24$ </td><td> $70.05 \pm 0.57$ </td><td> $78.90 \pm 0.52$ </td><td> $63.88 \pm 0.44$ </td><td> $73.56 \pm 0.40$ </td><td> $59.97 \pm 0.86$ </td><td> $68.40 \pm 0.78$ </td></tr><tr><td>7</td><td> $74.26 \pm 0.04$ </td><td> $81.38 \pm 0.83$ </td><td> $76.66 \pm 0.30$ </td><td> $83.71 \pm 0.30$ </td><td> $72.62 \pm 0.16$ </td><td> $80.24 \pm 0.14$ </td><td> $68.31 \pm 0.50$ </td><td> $75.36 \pm 0.48$ </td></tr><tr><td>10</td><td> $78.94 \pm 0.44$ </td><td> $85.15 \pm 0.44$ </td><td> $82.52 \pm 0.43$ </td><td> $87.77 \pm 0.32$ </td><td> $79.64 \pm 0.35$ </td><td> $85.21 \pm 0.29$ </td><td> $75.80 \pm 0.49$ </td><td> $80.85 \pm 0.51$ </td></tr></table>

Unknown Tab Count Scenario. This experiment evaluates CDWF in a closed-world scenario where the attacker has no prior knowledge of the number of concurrently accessed tabs. As shown in Table IV, CDWF significantly outperforms all baseline methods in precision and F1-score. With a fine-tuning sample size of $N ~ = ~ 1 0 .$ , CDWF achieves a precision of 72.37%, surpassing the best baseline by 32.94%. Its F1-score also consistently improves, reaching 47.47% at $N = 1 0$ and maintaining the lead among all compared methods (ARES reaches 42.79% under the same conditions). The AUC metric further confirms the discriminative robustness of CDWF: across all settings with $N \ \geq \ 3 ,$ CDWF yields the highest AUC values. These results demonstrate that CDWF maintains strong class separability and reliable identification capability even under the practical constraint of unknown tab counts.

PERFORMANCE OF CDWF WITHOUT PRIOR KNOWLEDGE OF THE NUMBER OF TABS.  
TABLE IV

<table><tr><td>N</td><td>Metrics</td><td>BAPM</td><td>ARES</td><td>TMWF</td><td>FMWF</td><td>CDWF</td></tr><tr><td rowspan="3">1</td><td>AUC</td><td>65.35</td><td>74.78</td><td>67.50</td><td>69.76</td><td>73.13</td></tr><tr><td>Pre</td><td>10.84</td><td>21.39</td><td>10.80</td><td>13.71</td><td>38.95</td></tr><tr><td>F1-score</td><td>12.26</td><td>23.92</td><td>12.14</td><td>15.59</td><td>19.56</td></tr><tr><td rowspan="3">3</td><td>AUC</td><td>70.51</td><td>80.63</td><td>71.03</td><td>76.91</td><td>81.04</td></tr><tr><td>Pre</td><td>14.05</td><td>29.83</td><td>14.12</td><td>21.03</td><td>54.46</td></tr><tr><td>F1-score</td><td>16.01</td><td>32.80</td><td>16.30</td><td>23.81</td><td>35.63</td></tr><tr><td rowspan="3">5</td><td>AUC</td><td>72.51</td><td>82.86</td><td>73.91</td><td>80.01</td><td>84.00</td></tr><tr><td>Pre</td><td>15.95</td><td>33.54</td><td>17.07</td><td>24.86</td><td>59.06</td></tr><tr><td>F1-score</td><td>18.15</td><td>36.59</td><td>19.67</td><td>28.12</td><td>42.47</td></tr><tr><td rowspan="3">7</td><td>AUC</td><td>74.81</td><td>84.65</td><td>76.39</td><td>81.65</td><td>85.92</td></tr><tr><td>Pre</td><td>17.67</td><td>36.33</td><td>19.13</td><td>26.48</td><td>63.63</td></tr><tr><td>F1-score</td><td>20.28</td><td>39.54</td><td>22.04</td><td>30.47</td><td>44.55</td></tr><tr><td rowspan="3">10</td><td>AUC</td><td>76.47</td><td>86.42</td><td>77.84</td><td>83.40</td><td>86.78</td></tr><tr><td>Pre</td><td>18.97</td><td>39.43</td><td>19.65</td><td>29.72</td><td>72.37</td></tr><tr><td>F1-score</td><td>21.95</td><td>42.79</td><td>22.77</td><td>34.17</td><td>47.47</td></tr></table>

## C. Open-world Evaluation

We evaluate CDWF in the open-world setting by pretraining on the closed-world traces from Meng Dataset [11] and fine-tuning/testing on the open-world traces from the Deng Dataset [10]. All other experimental configurations follow the closed-world setup described previously.

all alternatives. hese results reveal CDWF’s critical capability: it effectively identifies target websites using extremely limited labeled data even when the complete set of possible sites is unknown. This practical advantage stems from its robust feature representations that generalize across unknown traffic patterns, making it suitable for real-world deployment where comprehensive labeling is infeasible.

Open-World Performance. Performance is measured using P@2 and MAP@2 as shown in Table V. CDWF demonstrates superior adaptability in this challenging scenario. While ARES achieves marginally better results at minimal data $( N = 1 )$ CDWF becomes dominant with just three labeled samples and maintains consistent advantage as training data increases. At N = 10, CDWF achieves MAP@2 above 79%, outperforming

Scalability Across Tab Counts. Figure 6 evaluates method scalability under increasing tab concurrency. As expected, all approaches suffer performance degradation with higher tab counts, confirming that traffic interleaving substantially elevates identification difficulty. CDWF and ARES exhibit the strongest robustness, with CDWF maintaining the highest AUC across all settings. Notably, while FMWF performs competitively in low-concurrency scenarios, it experiences a steeper decline (22.3%) than CDWF (19.0%) when scaling to five tabs, revealing inferior stability under traffic complexity. On Hit@K, CDWF consistently outperforms alternatives in high-concurrency regimes, whereas BAPM and TMWF exhibit unstable or rapidly degrading performance. These trends indicate that CDWF’s domain-adversarial training and traffic-aware augmentation effectively preserve discriminative features amid severe traffic overlap, enabling more reliable scaling to realistic multi-tab browsing conditions compared to methods relying solely on architectural innovations or synthetic pretraining.

TABLE V  
COMPARISON WITH THE EXISTING MULTI-TAB WF ATTACKS IN THE OPEN-WORLD SCENARIO.

<table><tr><td>N</td><td>Metrics</td><td>BAPM</td><td>ARES</td><td>TMWF</td><td>FMWF</td><td>CDWF</td></tr><tr><td rowspan="2">1</td><td>P@2</td><td>22.01</td><td>39.79</td><td>19.15</td><td>30.97</td><td>38.67</td></tr><tr><td>MAP@2</td><td>26.09</td><td>48.96</td><td>22.29</td><td>37.36</td><td>47.41</td></tr><tr><td rowspan="2">3</td><td>P@2</td><td>33.41</td><td>55.79</td><td>30.34</td><td>48.52</td><td>56.64</td></tr><tr><td>MAP@2</td><td>39.38</td><td>65.75</td><td>36.13</td><td>57.87</td><td>65.99</td></tr><tr><td rowspan="2">5</td><td>P@2</td><td>37.67</td><td>61.56</td><td>25.03</td><td>56.13</td><td>64.52</td></tr><tr><td>MAP@2</td><td>43.87</td><td>70.83</td><td>29.66</td><td>65.50</td><td>72.86</td></tr><tr><td rowspan="2">7</td><td>P@2</td><td>42.23</td><td>64.90</td><td>42.18</td><td>60.23</td><td>68.12</td></tr><tr><td>MAP@2</td><td>48.72</td><td>73.60</td><td>50.05</td><td>69.38</td><td>75.56</td></tr><tr><td rowspan="2">10</td><td>P@2</td><td>46.85</td><td>69.38</td><td>39.73</td><td>64.20</td><td>72.85</td></tr><tr><td>MAP@2</td><td>53.74</td><td>77.19</td><td>47.64</td><td>72.88</td><td>79.51</td></tr></table>

![](images/3c99903ab8655e9d6719e34c936a23faf389e19815696851a7bc6ed6f506db35.jpg)

![](images/c96ea192b1a2ff3b3562d2fc1200b8966ba4276a9086f6b1fab6c6dce900349d.jpg)  
Fig. 6. The AUC and Hit@k of multi-tab WF attacks with different numbers of tabs in the open-world scenario.

## D. WF Defenses Evaluations

We evaluate CDWF’s resilience against three representative website fingerprinting defenses, namely WTF-PAD, FRONT, and RegulaTor, in the closed-world setting. The model is pretrained on the Meng Dataset [11] and fine-tuned/tested on Defense Enhanced Dataset derived from the Deng Dataset [29]. All other experimental configurations follow the closed-world setup described previously.

Resilience Against WF Defenses. CDWF consistently outperforms all baselines across all evaluated defensive scenarios, as shown in Figure 7, demonstrating superior resilience to defensive traffic perturbations. Even against strong defenses, CDWF maintains clear advantages. Under padding based obfuscation [12], CDWF achieves the highest accuracy and ranking performance among all methods. Against the most effective known defense RegularTor, CDWF sustains meaningful identification capability despite substantial performance degradation affecting all approaches. Analysis reveals that conventional defenses effectively disrupt methods relying on superficial traffic patterns. While some approaches retain partial effectiveness under moderate obfuscation, they fail to generalize under strong adversarial conditions. In contrast, CDWF’s targeted data augmentation strategy enhances feature stability against noise perturbations. This enables the model to extract discriminative traffic patterns that persist through defensive transformations, resulting in consistently reliable identification even when traffic characteristics are deliberately obscured.

![](images/729d69b526bace62198d1203dddbeb95a452d8261daf8ae2e5cc4533e27106a4.jpg)

![](images/3cc448222ca9e8e38fefb0feca535429e47e41b2baedc9cf4b70943fed978ea9.jpg)  
Fig. 7. Precision and P@2 of WF attacks under different defenses.

## E. Ablation Study

TABLE VI  
ABLATION STUDY RESULTS.

<table><tr><td>Model</td><td>Precision</td><td>MAP@5</td><td>P@5</td><td>F1-score</td><td>Recall</td></tr><tr><td>w/o DataAug</td><td>0.7868</td><td>0.7708</td><td>0.6934</td><td>0.6908</td><td>0.6224</td></tr><tr><td>w/o DomAda</td><td>0.8113</td><td>0.8000</td><td>0.7416</td><td>0.7445</td><td>0.6925</td></tr><tr><td>Extractor (w ARES)</td><td>0.7571</td><td>0.7966</td><td>0.7412</td><td>0.7345</td><td>0.7214</td></tr><tr><td>Extractor (w CNN)</td><td>0.3480</td><td>0.3275</td><td>0.2351</td><td>0.0750</td><td>0.0498</td></tr><tr><td>Extractor (w ResNet)</td><td>0.6996</td><td>0.5483</td><td>0.4103</td><td>0.3677</td><td>0.2609</td></tr><tr><td>Ours</td><td>0.8615</td><td>0.8090</td><td>0.7571</td><td>0.7558</td><td>0.7046</td></tr></table>

We conduct an ablation study to quantify the contribution of each core component. Three variants are evaluated: removing domain adaptation (w/o DomAda), removing data augmentation (w/o DataAug), and replacing the feature extractor. As shown in Table VI, the full CDWF model consistently outperforms all ablated variants across every metric.

Component Effectiveness. The full model achieves a precision of 0.8615, representing relative improvements of 9.5% and 6.2% over w/o DataAug (0.7868) and w/o DomAda (0.8113), respectively. This confirms that joint optimization of both modules is essential for accurate multi-website identification. Removing data augmentation causes the largest precision drop (12.1%), validating its role in enhancing recognition stability through diverse synthetic samples. Removing domain adaptation reduces F1-score and recall by 1.6%, verifying its necessity for mitigating cross-domain distribution shifts.

Feature Extractor Ablation. Replacing our hybrid CNN-Transformer extractor with the ARES backbone increases recall but substantially degrades precision and F1-score, revealing a coverage-accuracy trade-off that compromises overall identification reliability. CNN and ResNet variants exhibit markedly inferior performance across all metrics. Our codesigned extractor, synergistically integrated with traffic-aware augmentation and domain adaptation, achieves optimal balance between precision and recall while effectively addressing data scarcity and cross-domain distribution shift.

## VI. CONCLUSION

This paper proposes CDWF, a multi-tab Website Fingerprinting framework for cross-domain few-shot scenarios. By leveraging self-supervised pre-training on public data and labeled source samples for domain alignment, CDWF drastically reduces the target-domain labeling burden, requiring only a minimal few-shot set for final adaptation. Moreover, the framework integrates domain-adversarial adaptation and targeted data augmentation to enhance both classification accuracy and cross-domain generalization. Experimental results demonstrate that in the highly challenging 5-tab scenario, CDWF outperforms the state-of-the-art method by up to 19.65% in P@k, confirming its effectiveness and practical relevance in realworld deployments.

## REFERENCES

[1] R. Dingledine, N. Mathewson, and P. Syverson, “Tor: The Second-Generation onion router,” in 13th USENIX Security Symposium (USENIX Security 04), Aug. 2004.

[2] X. Cai, R. Nithyanand, T. Wang, R. Johnson, and I. Goldberg, “A systematic approach to developing and evaluating website fingerprinting defenses,” in Proceedings of the 2014 ACM SIGSAC conference on computer and communications security, 2014, pp. 227–238.

[3] X. Deng, Q. Li, and K. Xu, “Robust and reliable early-stage website fingerprinting attacks via spatial-temporal distribution analysis,” in Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security, 2024, pp. 1997–2011.

[4] T. Wang, X. Cai, R. Nithyanand, R. Johnson, and I. Goldberg, “Effective attacks and provable defenses for website fingerprinting,” in 23rd USENIX Security Symposium (USENIX Security 14), 2014, pp. 143– 157.

[5] A. Panchenko, F. Lanze, J. Pennekamp, T. Engel, A. Zinnen, M. Henze, and K. Wehrle, “Website fingerprinting at internet scale.” in NDSS, vol. 1, 2016, p. 23477.

[6] M. Juarez, S. Afroz, G. Acar, C. Diaz, and R. Greenstadt, “A critical evaluation of website fingerprinting attacks,” in Proceedings of the 2014 ACM SIGSAC conference on computer and communications security, 2014, pp. 263–274.

[7] T. Wang and I. Goldberg, “On realistically attacking tor with website fingerprinting,” Proceedings on Privacy Enhancing Technologies, 2016.

[8] W. Cui, T. Chen, C. Fields, J. Chen, A. Sierra, and E. Chan-Tin, “Revisiting assumptions for website fingerprinting attacks,” in Proceedings of the 2019 ACM asia conference on computer and communications security, 2019, pp. 328–339.

[9] Q. Yin, Z. Liu, Q. Li, T. Wang, Q. Wang, C. Shen, and Y. Xu, “An automated multi-tab website fingerprinting attack,” IEEE Transactions on Dependable and Secure Computing, vol. 19, no. 6, pp. 3656–3670, 2021.

[10] X. Deng, Q. Yin, Z. Liu, X. Zhao, Q. Li, M. Xu, K. Xu, and J. Wu, “Robust multi-tab website fingerprinting attacks in the wild,” in 2023 IEEE symposium on security and privacy (SP). IEEE, 2023, pp. 1005– 1022.

[11] W. Meng, C. Ma, M. Ding, C. Ge, Y. Qian, and T. Xiang, “Beyond single tabs: A transformative few-shot approach to multi-tab website fingerprinting attacks,” in Proceedings of the ACM on Web Conference 2025, 2025, pp. 1068–1077.

[12] M. Juarez, M. Imani, M. Perry, C. Dıaz, and M. Wright, “Wtf-´ pad: toward an efficient website fingerprinting defense for tor,” CoRR, abs/1512.00524, 2015.

[13] X. Cai, X. C. Zhang, B. Joshi, and R. Johnson, “Touching from a distance: Website fingerprinting attacks and defenses,” in Proceedings of the 2012 ACM conference on Computer and communications security, 2012, pp. 605–616.

[14] J. Hayes and G. Danezis, “k-fingerprinting: A robust scalable website fingerprinting technique,” in USENIX Security Symposium, 2016.

[15] K. Abe and S. Goto, “Fingerprinting attack on tor anonymity using deep learning,” Proceedings of the Asia-Pacific Advanced Network, vol. 42, no. 0, pp. 15–20, 2016.

[16] P. Sirinam, N. Mathews, M. S. Rahman, and M. Wright, “Triplet fingerprinting: More practical and portable website fingerprinting with n-shot learning,” in Proceedings of the 2019 ACM SIGSAC Conference on Computer and Communications Security, 2019, pp. 1131–1148.

[17] C. Wang, J. Dani, X. Li, X. Jia, and B. Wang, “Adaptive fingerprinting: Website fingerprinting over few encrypted traffic,” in Proceedings of the Eleventh ACM Conference on Data and Application Security and Privacy, 2021, pp. 149–160.

[18] Y. Xie, J. Feng, W. Huang, Y. Zhang, X. Sun, X. Chen, and X. Luo, “Contrastive fingerprinting: A novel website fingerprinting attack over few-shot traces,” in Proceedings of the ACM Web Conference 2024, 2024, pp. 1203–1214.

[19] C. Luo, W. Tang, Q. Wang, and D. Zheng, “Few-shot website fingerprinting with distribution calibration,” IEEE Transactions on Dependable and Secure Computing, vol. 22, no. 1, pp. 632–648, 2024.

[20] X. Zhu, J. Wang, W. Ge, Y. Huang, and T. Lu, “Wf-tfc: An openworld few-shot anonymous website fingerprinting via time-frequency consistency,” IEEE Transactions on Information Forensics and Security, 2025.

[21] W. Cui, T. Chen, and E. Chan-Tin, “More realistic website fingerprinting using deep learning,” in 2020 IEEE 40th International Conference on Distributed Computing Systems (ICDCS). IEEE, 2020, pp. 333–343.

[22] Z. Guan, G. Xiong, G. Gou, Z. Li, M. Cui, and C. Liu, “Bapm: block attention profiling model for multi-tab website fingerprinting attacks on tor,” in Proceedings of the 37th Annual Computer Security Applications Conference, 2021, pp. 248–259.

[23] Z. Jin, T. Lu, S. Luo, and J. Shang, “Transformer-based model for multitab website fingerprinting attack,” in Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security, 2023, pp. 1050–1064.

[24] J. Gong and T. Wang, “Zero-delay lightweight defenses against website fingerprinting,” in 29th USENIX Security Symposium (USENIX Security 20), 2020, pp. 717–734.

[25] J. K. Holland and N. Hopper, “Regulator: A straightforward website fingerprinting defense,” Proceedings on Privacy Enhancing Technologies, vol. 2022, pp. 344 – 362, 2020.

[26] V. Rimmer, D. Preuveneers, M. Juarez, T. Van Goethem, and W. Joosen, “Automated website fingerprinting through deep learning,” in 25th Annual Network and Distributed System Security Symposium. The Internet Society, 2018.

[27] Y. Wang, H. Xu, Z. Guo, Z. Qin, and K. Ren, “Snwf: Website fingerprinting attack by ensembling the snapshot of deep learning,” IEEE Transactions on Information Forensics and Security, vol. 17, pp. 1214– 1226, 2022.

[28] A. Bahramali, A. Bozorgi, and A. Houmansadr, “Realistic website fingerprinting by augmenting network traces,” in Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security, 2023, pp. 1035–1049.

[29] X. Deng, R. Zhao, Y. Wang, M. Zhan, Z. Xue, and Y. Wang, “Countmamba: A generalized website fingerprinting attack via coarse-grained representation and fine-grained prediction,” in 2025 IEEE Symposium on Security and Privacy (SP). IEEE, 2025, pp. 1419–1437.
# Drift-Aware Adaptive Website Fingerprinting

Zhengge Yi, Tengyao Li, Jingxi Zhang, Yifei Meng, Xiangyang Luo

Abstract—Website fingerprinting (WF) attacks infer websites visited by Tor users from encrypted traffic metadata. Deeplearning-based WF attacks achieve high accuracy under controlled conditions but degrade substantially under traffic drift, where the deployment distribution progressively deviates from the training distribution. Recent unsupervised self-training methods address this problem by using high-confidence predictions on unlabeled drifted traffic as pseudo-labels to refine deployed models. However, fixed unsupervised adaptation strategies cannot adequately handle heterogeneous drift across websites, and severely drifted classes may fail to produce reliable pseudo-labels, resulting in persistent adaptation blind spots. We propose Aion, a hybrid drift-aware adaptive WF framework that combines unsupervised self-training with limited labeled target-domain supervision for continuous deployment under traffic drift. Aion dynamically regulates the source-domain constraint according to measured distributional divergence, broadens pseudo-label coverage through dual-classifier collaborative generation to accelerate performance recovery, and selectively restores supervision for classes where purely unsupervised adaptation fails. Extensive experiments on real Tor traces across multiple drift scenarios show that Aion consistently outperforms existing methods. Under 270 days of real-world traffic drift, Aion achieves F1-scores of 88.14%, 82.84%, and 86.32% in the closed-world, open-world, and streaming settings, exceeding the best baselines by 5.87, 8.90, and 10.92 percentage points, respectively.

Index Terms—Website fingerprinting, traffic drift, adaptive attack, pseudo-labeling, Tor anonymity.

## I. INTRODUCTION

Website fingerprinting (WF) attacks analyze encrypted traffic metadata exchanged between users and Tor entry nodes, including packet direction, size, and timing patterns, to infer the websites being visited [1]–[5]. Such attacks threaten the privacy of anonymous communication systems such as Tor. Recent deep-learning-based WF attacks have achieved classification accuracy exceeding 95% under controlled experimental conditions [6]–[10].

However, in practical deployments, the statistical properties of Tor encrypted traffic continuously shift due to website content evolution, Tor Browser updates, and changes in user browsing behavior. These factors are collectively referred to as traffic drift [11]–[13]. As drift accumulates over time, the traffic distribution observed during deployment progressively deviates from the distribution used for training, causing WF classifiers to degrade. Empirical observations show that, after 270 days of temporal drift, the performance of existing WF attacks can decline from around 95% to approximately 30%– 60% [11]. Without post-deployment adaptation, an attacker would need to frequently re-collect and re-label traffic traces, which incurs substantial operational cost. Therefore, enabling WF models to adapt continuously to traffic drift while maintaining effective classification performance is a key challenge for assessing the real-world threat of WF attacks.

Several research directions have been explored to address traffic drift. Periodic retraining [6]–[10], [12], [14], [15] relies on large-scale labeled traffic collection, which is costly and cannot promptly respond to continuously evolving drift. Fewshot fine-tuning methods [16]–[18] reduce labeling requirements through data augmentation and contrastive learning, yet they still require the labeled samples to reflect the traffic conditions at deployment time. Online update methods based on exit-node observations [19] leverage labels observable at the Tor exit side for model updates, but their applicability is limited by the distribution mismatch between exit-side supervision and entry-side WF deployment. Recently, Proteus [11] introduced an unsupervised adaptation framework that fine-tunes WF models using high-confidence unlabeled drifted traffic collected during deployment, achieving notable performance recovery across multiple drift scenarios.

Among these directions, unsupervised self-training represents a promising starting point for continuous adaptation, since it can exploit unlabeled post-deployment traffic without requiring labels for every target-domain trace [20]–[22]. Under this paradigm, the attacker trains an initial model on labeled pre-deployment traffic and then iteratively generates pseudolabels for unlabeled post-deployment traffic to adapt the model. Source-domain knowledge provides the initial discriminative basis for pseudo-labeling and helps prevent semantic drift. However, continuous traffic drift introduces two core challenges. First, the strength of source-domain constraints is difficult to tune. Strong constraints can hinder adaptation when drift becomes severe, whereas weak constraints make the model more vulnerable to semantic drift. Existing methods usually rely on a fixed constraint strength, which cannot remain effective across different drift levels. Second, severely drifted classes are difficult to recover through purely unsupervised pseudo-labeling. When some websites undergo drastic changes, their predictions may become near-random, making confidence-based pseudo-label selection unable to extract reliable supervisory signals. As a result, these classes may remain uncovered throughout the adaptation process. This motivates a hybrid adaptation setting in which the model primarily adapts from unlabeled target-domain traffic, but can selectively request a very small number of labeled targetdomain samples for classes where unsupervised adaptation demonstrably fails.

To address these challenges, we propose Aion, a drift-aware hybrid adaptive WF attack framework that continuously finetunes existing WF models during deployment. Aion integrates three complementary components. First, a drift-aware adaptive regulation mechanism quantifies distributional divergence and adjusts the source-domain constraint strength according to the current drift severity. Second, a dual-classifier collaborative pseudo-labeling scheme introduces an auxiliary classifier free from source-domain constraints, improving target-domain adaptation and broadening pseudo-label class coverage. Third, a coverage-diagnosis-based targeted labeling strategy identifies monitored classes where self-training fails and restores their supervision with a limited active target-domain label budget. Together, these modules form a multi-round cyclic adaptation framework for progressive refinement. Since Aion modifies only the training procedure rather than the underlying network architecture, it can be integrated into existing deep-learningbased WF attacks.

We conduct a systematic evaluation of Aion on a largescale dataset comprising over 300,000 real Tor traffic traces and covering multiple drift scenarios. Under 270 days of real-world traffic drift, Aion achieves an F1-score of 88.14% in the closed-world setting, improving over the state-of-theart adaptive WF method [11] by 5.87 percentage points. It achieves 82.84% in the open-world setting, an improvement of 8.90 percentage points, and 86.32% in the streaming setting, an improvement of 10.92 percentage points.

We make the following contributions.

• We propose Aion, a hybrid drift-aware adaptive WF attack framework that combines unsupervised self-training with limited labeled target-domain supervision to continuously adapt deployed WF models under traffic drift, thereby sustaining effective classification performance over extended deployment periods.

We design a drift-aware adaptive regulation mechanism that dynamically calibrates the source-domain constraint strength based on measured distributional divergence, together with a dual-classifier collaborative pseudo-labeling scheme that accelerates early-stage adaptation and performance recovery while broadening pseudo-label class coverage.

• We propose a lightweight targeted labeling strategy driven by coverage diagnosis that automatically identifies classes where adaptation fails and restores their supervision at minimal cost, eliminating structural blind spots in purely unsupervised adaptation under severe drift.

• We evaluate Aion on real Tor traces spanning 270 days of temporal drift across multiple traffic drift scenarios. Results show that Aion consistently outperforms existing methods under moderate-to-severe drift while remaining effective during long-term deployment.

## II. BACKGROUND

## A. Threat Model

As illustrated in Fig. 1, the WF attacker is positioned on the network path between the user and the Tor entry node, such as a local gateway, an ISP, or an autonomous system boundary. The attacker passively observes metadata of encrypted traffic, including packet direction, size, and timing information. The attacker maintains a monitored list of W target websites, and the objective is to determine which website the user is visiting based on the observed traffic. Prior to deployment, the attacker actively visits each website on the monitored list through the Tor network and collects labeled traffic traces as the sourcedomain data $\mathcal { D } _ { s } = \{ ( x _ { i } , y _ { i } ) \} _ { i = 1 } ^ { n _ { s } }$ , where $x _ { i }$ denotes a traffic sequence and $y _ { i } ~ \in ~ \{ 1 , \ldots , W \}$ denotes the corresponding website label. The attacker then trains a deep learning classifier C on $\mathcal { D } _ { s }$

![](images/ff15877ff740a09073ac98d8b6702fd0a0daa3aaba901b330197679f8406032e.jpg)  
Fig. 1: The threat model of WF.

However, after deployment, the statistical properties of Tor encrypted traffic continuously evolve due to multiple independent drift sources, including website content updates, page restructuring, Tor Browser version updates, and changes in user browsing behavior. As shown in the lower part of Fig. 1, the feature clusters of a WF model trained at time t are initially separable but gradually overlap by deployment time $t _ { n } ,$ leading to a substantial decline in classification accuracy. During passive monitoring, the attacker can continuously collect encrypted traffic passing through the monitoring point, but cannot obtain ground-truth labels for these user traces. This traffic constitutes the unlabeled target-domain data $\mathcal { D } _ { t } ^ { u } = \{ x _ { j } \} _ { j = 1 } ^ { n _ { u } }$

In addition, we consider a limited re-collection capability that is commonly assumed in WF studies: after deployment, the attacker can actively revisit a small subset of selected monitored websites on the monitored list through Tor. Since the attacker knows the URLs of the monitored websites, these actively collected traces can be labeled by construction. This process yields a small labeled target-domain set $\mathcal { D } _ { t } ^ { l } =$ $\{ ( x _ { k } , y _ { k } ) \} _ { k = 1 } ^ { n _ { l } }$ at the current time point, where $n _ { l } \ll n _ { u } .$ . The complete target-domain data is therefore $\mathcal { D } _ { t } = \mathcal { D } _ { t } ^ { u } \cup \mathcal { D } _ { t } ^ { l }$ . Unlike periodic full re-collection, this capability is used only for a small number of diagnosed classes and is explicitly quantified in our cost analysis.

WF attacks are evaluated under two standard settings [7]. In the closed-world setting, the user is assumed to visit only websites within the monitored list, which forms a Wclass classification problem. In the open-world setting, the user may also visit a large number of unmonitored websites, requiring the attacker to correctly identify monitored website traffic while rejecting unmonitored traffic. This setting forms a $( W + 1 )$ -class problem with a rejection option. The openworld setting more closely reflects real deployment scenarios and is more challenging, since traffic drift may cause the features of some monitored websites to become confused with unmonitored traffic, increasing the false positive rate.

## B. Self-Training Adaptation Paradigm

Self-training is a classical semi-supervised learning paradigm widely adopted in domain adaptation scenarios. Its core idea is to use the model’s own high-confidence predictions on unlabeled data as pseudo-labels and incorporate them into the training set to iteratively expand the supervisory signal. In the WF scenario, the attacker first trains a classifier $C$ on the source domain $\mathcal { D } _ { s }$ and then adapts $C$ to the target domain $\mathcal { D } _ { t }$ through an iterative cycle. The model first generates predicted labels $\hat { y } _ { i }$ and prediction probability distributions $p _ { i }$ for samples from $\mathcal { D } _ { t }$ . A confidence-based criterion then selects a reliable subset $\mathcal { P } _ { C }$ from $\mathcal { D } _ { t }$ as the pseudo-label set. Finally, $C$ is fine-tuned using $\mathcal { P } _ { C }$ , typically with a source-domain supervisory loss retained to maintain semantic knowledge:

$$
\mathcal {L} = \lambda \mathcal {L} _ {\mathrm{src}} + \mathcal {L} _ {\mathrm{pl}}\tag{1}
$$

where $\mathcal { L } _ { \mathrm { s r c } }$ is the source-domain cross-entropy loss, ${ \mathcal L } _ { \mathrm { p l } }$ is the pseudo-label cross-entropy loss, and λ controls the sourcedomain constraint strength. This cycle repeats for multiple rounds, with the updated model generating higher-quality pseudo-labels in subsequent rounds.

Pseudo-label quality is critical to self-training. An effective filtering method [11] fits a two-component Gaussian Mixture Model (GMM) to the distribution of prediction entropies $H ( p _ { i } )$ over all target-domain samples:

$$
p (H) = \pi_ {1} \mathcal {N} (H; \mu_ {1}, \sigma_ {1} ^ {2}) + \pi_ {2} \mathcal {N} (H; \mu_ {2}, \sigma_ {2} ^ {2})\tag{2}
$$

where the low-entropy component corresponds to highconfidence and likely correct predictions, while the highentropy component corresponds to uncertain or erroneous predictions. The posterior probability $w _ { i }$ of each sample belonging to the low-entropy component quantifies its prediction reliability. Samples with $w _ { i } > \tau$ are included in the pseudolabel set $\mathcal { P } _ { C } .$ . Compared with fixed confidence thresholds, the data-driven nature of GMM enables the filtering boundary to adapt automatically to different entropy distributions across adaptation rounds, and this strategy has been shown to be effective in WF drift adaptation [11].

To supplement the discrete supervisory signal provided by pseudo-labels, the information maximization (IM) loss [23] encourages the model to produce target-domain predictions that are both confident and diverse:

$$
\mathcal {L} _ {\mathrm{IM}} = \mathbb {E} [ H (p _ {i}) ] - H (\mathbb {E} [ p _ {i} ])\tag{3}
$$

The first term minimizes the average prediction entropy to encourage confident predictions, while the second term maximizes the entropy of the batch-averaged prediction distribution to prevent mode collapse, where the model concentrates predictions of multiple classes into a few dominant classes. The IM loss is particularly important for maintaining classbalanced predictions when pseudo-labels cover only a subset of classes.

GMM filtering and IM loss provide effective technical components for self-training by selecting reliable pseudo-labels and preventing prediction collapse. However, this paradigm is inherently limited by the quality of the model’s own predictions. When a website undergoes severe drift, its target-domain samples may receive high-entropy or erroneous predictions and are therefore excluded by the pseudo-label filter. Such exclusion avoids injecting noisy labels, but it also prevents these classes from receiving corrective supervision during adaptation. This limitation motivates the need for an adaptation mechanism that can identify and repair classes where purely unsupervised self-training fails.

## III. RELATED WORK

## A. Website Fingerprinting Attacks and Traffic Drift

Network traffic fingerprinting aims to infer application, device, or behavior-level information from observable traffic patterns and has been studied in a wide range of security scenarios, including Tor website fingerprinting and IIoT device identification [2], [24]. In the Tor setting, website fingerprinting (WF) attacks exploit information inevitably leaked from encrypted traffic, including packet size, direction, timing, and burst patterns, to infer the target website visited by the user. Early WF attacks relied on hand-crafted traffic statistical features, such as packet length histograms, burst sequences, and cumulative traffic representations, combined with traditional classifiers such as k-NN [25] and SVM [26]. The performance of these methods depends heavily on feature engineering, making them less robust against traffic obfuscation and defense mechanisms.

The introduction of deep learning substantially improved WF attacks. DF [7] was the first to apply convolutional neural networks to raw packet direction sequences, outperforming traditional methods in both closed-world and open-world settings. Subsequent studies improved WF attacks from two directions, namely input representation and model architecture. RF [10] proposed the Traffic Aggregation Matrix (TAM) as a compact two-dimensional input representation, Holmes [27] designed hybrid architectures that fuse multi-scale features, and Transformer-based methods [14] capture long-range dependencies through self-attention. Under controlled conditions where training and test data are identically distributed, these advanced attacks achieve classification accuracy exceeding 95%.

However, Tor traffic characteristics change continuously over time due to website content updates, page restructuring, embedded resource changes, Tor circuit selection dynamics, Tor Browser version updates, and user browsing behavior changes [12]. These drift sources are largely independent and can occur simultaneously, producing compound distributional shifts that continuously degrade model performance. An early strategy is to periodically collect large-scale labeled traffic and retrain the model [7], [12], but collecting and labeling data for hundreds of monitored websites is costly and cannot promptly respond to continuously evolving drift. NetCLR [16] reduces labeling dependence through contrastive learning pre-training but still requires the attacker to periodically collect labeled data for all monitored websites, lacking the ability to adapt autonomously to drift. OnlineWF [19] leverages website labels observable at Tor exit nodes for real-time model updating, but WF attacks are typically deployed at the entry side. Since traffic observed at the entry and exit sides can differ substantially, models updated from exit-side observations may not directly match the traffic distribution encountered by entryside WF attackers.

Meanwhile, WF defenses can also interact with traffic drift. By padding, delaying, or reshaping packet sequences, defenses reduce website-specific leakage but also introduce additional distributional perturbations [28]–[30]. These perturbations persist in the traffic traces observed along the circuit and can compound temporal drift, making pseudo-labels less reliable and adaptation more difficult. Aion differs from fixed adaptation methods by measuring drift severity, dynamically regulating the source-domain constraint, and selectively restoring supervision when unsupervised adaptation fails.

## B. Self-Training and Domain Adaptation

Self-training was originally proposed as a classical semisupervised learning paradigm [21]. Its core idea is to use the model’s high-confidence predictions on unlabeled data as pseudo-labels and incorporate them into the training set to iteratively expand supervisory signals. This paradigm was later introduced into unsupervised domain adaptation to mitigate distributional shift between source and target domains. In the domain adaptation self-training framework, the model is pre-trained on source-domain labeled data and then continues learning from pseudo-labeled target-domain data, while maintaining training stability through source-domain replay, distribution alignment, or entropy regularization [22], [31].

Semi-supervised and unsupervised learning have also been explored in broader traffic analysis tasks where labeled data is limited or new traffic patterns appear after deployment. For example, AutoIoT updates IoT device fingerprints through semi-supervised learning on newly observed traffic [32], and heuristic clustering has been used to classify unknown attack traffic in SCADA networks without relying on complete supervision [33]. Other studies investigate distributed or transferable learning for industrial and IoT traffic identification, reflecting the broader need to maintain traffic-analysis models under changing environments [34]–[36]. These studies are related in their use of limited labels or unlabeled traffic, but they focus on device identification, attack classification, or distributed intrusion detection rather than Tor website fingerprinting under long-term temporal drift.

Thirumuruganathan et al. [20] used unlabeled data to fine-tune models via self-training and achieved good results across multiple cross-domain cybersecurity tasks. In the WF domain, UAF [37] made an early attempt at unsupervised adaptive fingerprinting by leveraging unlabeled target-domain traffic for continual model updates. Building on this direction, Proteus [11] proposed a more comprehensive self-training framework for traffic drift adaptation. It combines GMMbased pseudo-label filtering with source-domain supervision, distribution alignment, and information maximization, and progressively refines the model through repeated adaptation rounds. These results demonstrate the viability of unsupervised self-adaptive WF attacks.

Overall, existing self-training and unsupervised domain adaptation methods provide effective mechanisms for adapting WF models with unlabeled target-domain traffic, and Proteus represents a strong example of general-purpose adaptation under traffic drift. However, realistic WF deployment poses challenges that are not fully addressed by a fixed and purely unsupervised adaptation policy. Drift severity varies across websites, making a fixed source-domain constraint or a uniform pseudo-labeling rule difficult to maintain across different drift conditions. Severely drifted classes may also produce near-random predictions and remain without reliable supervision throughout adaptation. In addition, continuous deployment requires timely performance recovery, whereas multi-round adaptation can leave a non-negligible degradation window after drift occurs. Aion addresses these limitations through a drift-aware and class-sensitive design that dynamically regulates source-domain constraints, expands pseudolabel coverage with complementary classifiers, and selectively restores supervision for classes where purely unsupervised adaptation is likely to fail.

## IV. DESIGN OF AION

## A. Overview

Aion is a cyclic hybrid adaptive framework that combines unsupervised self-training with limited labeled target-domain supervision to adapt a pre-trained WF model under traffic drift. During deployment, Aion primarily leverages unlabeled drifted traffic naturally observed by the attacker for PAD estimation and pseudo-label-based self-training, and introduces limited supervision only for classes that cannot be reliably recovered by unsupervised adaptation. It adjusts only model parameters without modifying the model architecture, enabling seamless integration with existing deep-learning-based WF attacks.

Fig. 2 illustrates the complete adaptation pipeline. Before adaptation begins, the drift-aware adaptive regulation module (§IV-B) measures the distributional divergence between source and target domains via Proxy A-distance and computes a regulation coefficient $\lambda _ { \mathrm { d r i f t } }$ that controls source-domain constraint strength throughout all subsequent cycles. In each adaptation cycle, the dual-classifier pseudo-label generation module (§IV-C) produces pseudo-labels through collaborative filtering: the primary classifier C provides conservative pseudolabels under source-domain constraints, while an auxiliary classifier $C ^ { \prime }$ , trained solely on current pseudo-labels without source-domain constraints, provides complementary coverage for heavily drifted classes. In the first cycle only, the selfdiagnostic targeted labeling module (§IV-D) diagnoses classes where pseudo-label coverage remains insufficient and restores their supervision through minimal targeted re-collection. Finally, cyclic adaptation (§IV-E) performs joint fine-tuning under the composite loss and advances to the next cycle, enabling progressive refinement across rounds.

![](images/010eca7487ac655ce17e61569bfb22b902825440c53cb4f1b07788e6bbd55725.jpg)  
Fig. 2: Overall framework of Aion. It continuously fine-tunes the deployed model during the deployment phase to adapt to traffic drift.

## B. Drift-Aware Adaptive Regulation

In practical WF attack scenarios, the impact of drift on model performance varies across different time spans. Shortterm drift may involve only routine Tor routing rotations or minor website changes, where source-domain data retains high reference value and a strong source-domain constraint helps suppress pseudo-label noise. After several months, however, many websites may undergo redesigns or architectural migration, substantially diminishing the guidance value of sourcedomain knowledge and necessitating a relaxed constraint to grant the model sufficient adaptation freedom. Rather than relying on a fixed constraint strength, Aion automatically quantifies drift severity and adjusts the training configuration accordingly.

Drift quantification. Aion employs the Proxy A-distance (PAD) [38] to quantify distributional divergence between source and target domains in the model’s feature space. For each drift point, we reserve a PAD-estimation subset from both the source and target domains, using 20% of the samples from each domain. These samples are disjoint from the data used to evaluate the WF classifier. We feed the reserved source-domain and target-domain samples into the feature extraction layer of the pre-trained WF model and obtain their feature vectors $f ( x _ { s } )$ and $f ( x _ { t } )$ . A lightweight linear domain classifier is then trained in this feature space to distinguish source features from target features, with domain labels 0 and 1 assigned to source and target samples, respectively. The domain classifier is optimized with binary cross-entropy loss over the source and target domain labels. Let ϵ denote the held-out validation error of the domain classifier. PAD is computed as:

$$
d _ {\mathcal {A}} = 2 (1 - 2 \epsilon)\tag{4}
$$

where ϵ denotes the held-out validation error of the domain classifier. In implementation, the computed value is clipped to [0, 2] to avoid invalid values caused by finite-sample estimation noise. When the two domains are indistinguishable, the domain classifier approaches random guessing, $\epsilon \approx 0 . 5 ,$ and $d _ { \cal A } \approx 0 .$ , corresponding to mild or negligible drift. When the two domains are easily separable, ϵ approaches 0 and $d _ { \mathcal { A } }$ approaches 2, corresponding to severe drift. PAD therefore measures source-target discrepancy through a discriminative task directly in the current WF feature space.

Adaptive training regulation. Given the measured divergence $d _ { A } ,$ , the next step is to translate it into a concrete training configuration. A natural choice is a smooth monotonically decreasing mapping, ensuring gradual transition rather than abrupt switching between constraint regimes. Aion adopts a sigmoid mapping for this purpose:

$$
\lambda_ {\mathrm{drift}} = \lambda_ {\mathrm{min}} + (\lambda_ {\mathrm{max}} - \lambda_ {\mathrm{min}}) \cdot \sigma (- k (d _ {\mathcal {A}} - d _ {0}))\tag{5}
$$

where $\sigma ( \cdot )$ is the sigmoid function, $\lambda _ { \mathrm { m a x } }$ and $\lambda _ { \mathrm { m i n } }$ are the upper and lower bounds of the regulation coefficient, $d _ { 0 }$ is the drift center threshold, and k controls the transition sharpness. When $d _ { A } \ll d _ { 0 } , \lambda _ { \mathrm { d r i f t } } \to \lambda _ { \mathrm { m a x } }$ , strengthening the sourcedomain constraint to fully exploit source-domain knowledge that retains reference value. When $d _ { A } \gg d _ { 0 } , \lambda _ { \mathrm { d r i f t } }  \lambda _ { \mathrm { m i n } } ,$ relaxing the source-domain constraint to grant the model greater adaptation freedom.

$\lambda _ { \mathrm { d r i f t } }$ acts only on the source-domain supervisory loss ${ \mathcal { L } } _ { \mathrm { s r c } } .$ The rationale is that the effectiveness of $\mathcal { L } _ { \mathrm { s r c } }$ depends on the degree of association between source-domain and targetdomain traffic, which diminishes as drift intensifies and thus requires dynamic regulation. The target-domain adaptation losses—including the pseudo-label loss and the information maximization loss—are computed directly from the current traffic and do not depend on source-domain association, hence they are not regulated by $\lambda _ { \mathrm { d r i f t } }$ . Note that the PAD computation is performed only once before the entire adaptation process begins, involving one forward pass and one lightweight classifier training, with negligible additional computational overhead.

## C. Dual-Classifier Pseudo-Label Generation

In existing self-training methods, a single classifier simultaneously bears the objectives of source-domain knowledge preservation and target-domain adaptation. The source-domain supervisory loss continuously pulls the model toward the old traffic distribution in every training step, limiting the effective step size toward the new distribution and thereby constraining pseudo-label generation efficiency and class coverage.

Key insight. Although post-drift traffic undergoes shifts in underlying features, the vast majority of websites still maintain distinguishable traffic fingerprints. These fingerprints are often shaped by page-level structures, such as page size, embedded resources, request-response interaction patterns, and loading timing. Since such structures are largely determined by website functionality and content architecture, their discriminative patterns do not completely vanish under Tor circuit rotation or CDN node switching. This means that a classifier trained solely on current traffic data, free from source-domain constraints, can more efficiently exploit these persistent cross-site differences to mine pseudo-labels for heavily drifted classes.

Primary classifier pseudo-label generation. Aion maintains two classifiers during the first R adaptation cycles. The primary classifier C is trained under a loss that includes source-domain supervision; since its classification boundary is biased toward the source-domain traffic distribution, C tends to produce high-confidence predictions for samples whose features remain close to those of the source domain, yielding high pseudo-label precision but insufficient coverage for heavily drifted classes. Unlabeled target-domain traffic is fed into $C ,$ and the GMM filtering mechanism described in Section II-B is applied to the predictions for reliability filtering; samples with posterior probability exceeding the threshold τ constitute the pseudo-label set $\mathcal { P } _ { C }$ of C.

Auxiliary classifier training and pseudo-label generation. The parameters of C are deep-copied to obtain the auxiliary classifier $C ^ { \prime } .$ , which is trained on $\mathcal { P } _ { C }$ using the standard crossentropy loss for $E ^ { \prime }$ epochs:

$$
\mathcal {L} _ {C ^ {\prime}} = \mathbb {E} _ {(x, \hat {y}) \in \mathcal {P} _ {C}} \left[ - \log C _ {\hat {y}} ^ {\prime} (x) \right]\tag{6}
$$

The training involves no source-domain data or sourcedomain-related loss, enabling $C ^ { \prime }$ to rapidly shift its classification boundary toward the current traffic distribution and cover a broader range of classes. After training, $C ^ { \prime }$ similarly uses the GMM filtering mechanism to generate its pseudo-label set $\mathcal { P } _ { C ^ { \prime } }$ on the target-domain traffic. The bias directions of the two classifiers are complementary: heavily drifted classes that $C$ misses can be captured by $C ^ { \prime }$ due to its rapid adaptation, while ambiguous samples can be controlled by the merging rule described below.

Before fine-tuning C, Aion merges $\mathcal { P } _ { C }$ and $\mathcal { P } _ { C ^ { \prime } }$ by taking their union. If a target sample is selected by only one classifier, its pseudo-label is directly included in the merged pseudolabel pool. If the same target sample is selected by both classifiers with the same pseudo-label, Aion retains only one copy to avoid duplicated supervision. If the same target sample is selected by both classifiers but assigned different pseudolabels, Aion regards it as a conflicting sample and discards it from the current round. This conflict-discarding rule prevents the model from receiving contradictory supervision for the same target trace, which could otherwise introduce inconsistent gradients and amplify pseudo-label noise. In this way,

Aion preserves the auxiliary classifier’s benefit of expanding pseudo-label coverage while excluding ambiguous samples. The merged pseudo-label set is then used to fine-tune C. After each round of fine-tuning, $C ^ { \prime }$ is discarded. From round $R { + 1 }$ to round $T ,$ the dual-classifier mechanism is deactivated and only pseudo-labels from C are used, because C has already shifted toward the current distribution through R rounds of adaptation, diminishing the marginal benefit of $C ^ { \prime } ,$ , while accumulated noise in the pseudo-labels produced by $C ^ { \prime }$ would risk error amplification.

## D. Self-Diagnostic Targeted Labeling

The above two modules can handle most drift scenarios. However, in real Internet environments, some websites may undergo fundamental changes during the monitoring period, such as comprehensive redesigns, architectural migrations, or CDN provider switches, causing qualitative changes in their traffic fingerprints and reducing the model’s predictions for these classes to near-random. In such cases, neither the primary nor the auxiliary classifier can produce reliable pseudolabels, constituting structural blind spots of purely unsupervised self-training. Aion automatically identifies these classes through coverage diagnosis and restores their classification capability via low-cost targeted labeling.

Coverage diagnosis. In the first adaptation cycle, after $C$ generates pseudo-labels $\mathcal { P } _ { C }$ , Aion computes two per-class metrics for each monitored website class k. Let

$$
n _ {k} = | \{(x, \hat {y}) \in \mathcal {P} _ {C}: \hat {y} = k \} |
$$

denote the total number of pseudo-labels assigned to class $k ,$ and

$$
n _ {k} ^ {\mathrm{high}} = | \{(x, \hat {y}) \in \mathcal {P} _ {C}: \hat {y} = k \land w _ {i} > \tau_ {\mathrm{high}} \} |
$$

denote the count of high-confidence pseudo-labels, where $w _ { i }$ is the GMM posterior probability and $\tau _ { \mathrm { h i g h } }$ is a high-confidence threshold. Class k is flagged as coverage-deficient if and only if $n _ { k } < n _ { \mathrm { m i n } }$ or $n _ { k } ^ { \mathrm { h i g h } } < n _ { \mathrm { m i n } }$ , where $n _ { \mathrm { m i n } }$ is the minimum pseudo-label count threshold (applied to both total and highconfidence counts). The set of flagged classes $\kappa _ { \mathrm { d e f } }$ constitutes the minimal set requiring external annotation.

Targeted labeling and data augmentation. For each class in $\kappa _ { \mathrm { d e f } } ,$ the attacker visits the corresponding website through the Tor network to collect S labeled samples. Under the WF attack threat model, the attacker already knows the URL of each website in the monitored list; this operation requires only a few visits to the diagnosed subset of websites. To amplify the supervisory signal of these scarce labeled samples, two augmentation operations—random insertion and random dropping [16]—are applied to each labeled sample. Random insertion simulates the introduction of redundant packets by Tor relay nodes, while random dropping simulates packet loss due to network congestion. Each original sample generates γ augmented variants, expanding the effective training samples per coverage-deficient class from S to $\gamma \cdot S .$ . The augmented labeled samples are merged into the pseudo-label pool ${ \mathcal { P } } _ { C } ,$ providing direct supervisory signals for coverage-deficient classes.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Cyclic Adaptation of Aion
Require: Classifier C; source data  $D_{s}$ ; target data  $D_{t}$ ; cycles T; dual rounds R; threshold  $\tau$ ; epochs E,  $E'$ ; coverage thresholds  $\tau_{high}, n_{min}$ ; query budget S
Ensure: Adapted classifier C
1:  $d_{A} \leftarrow \text{COMPUTEPAD}(C, \mathcal{D}_{s}, \mathcal{D}_{t})$   ▷ Eq. (4)
2:  $\lambda_{\text{drift}} \leftarrow \text{ADAPTIVEWEIGHT}(d_{A})$   ▷ Eq. (5)
3: for t = 1 to T do
4:  $P_{C} \leftarrow \text{GMMSELECT}(C, \mathcal{D}_{t}, \tau)$ 
5: if t = 1 and S &gt; 0 then
6:  $K_{def} \leftarrow \text{DIAGNOSECOVERAGE}(P_{C}, \tau_{high}, n_{min})$ 
7: for all  $k \in K_{def}$  do
8: Query and augment S labeled samples for website k
9:  $P_{C} \leftarrow P_{C} \cup P_{lab}^{k}$ 
10: end for
11: end if
12: if  $t \leq R$  then
13:  $\theta_{C'} \leftarrow \theta_{C}$ 
14:  $\text{TRAIN}(C', P_{C}, E')$   ▷ Eq. (6)
15:  $P_{C'} \leftarrow \text{GMMSELECT}(C', D_{t}, \tau)$ 
16: else
17:  $P_{C'} \leftarrow \emptyset$ 
18: end if
19: for e = 1 to E do
20: Compute L and update  $\theta_{C}$   ▷ Eq. (7)
21: end for
22: end for
23: return C
</div>

It is important to note that Aion’s targeted labeling is fundamentally different from traditional few-shot methods such as NetCLR [16]. The latter lacks drift-awareness capability and can only collect labeled data for all monitored websites at fixed intervals, with overhead proportional to the size of the monitored list. Aion, through coverage diagnosis, precisely identifies the classes requiring annotation, collecting only S samples for each of $| \boldsymbol { \mathcal { K } } _ { \mathrm { d e f } } |$ websites, executed only once in the first adaptation round. This operation only requires a small number of Tor visits, incurring negligible overhead in practical deployment.

## E. Cyclic Adaptation

Aion organizes the above modules into a multi-round adaptation cycle. In the joint fine-tuning phase of each cycle, the primary classifier C is updated under the following composite loss:

$$
\mathcal {L} = \lambda_ {\mathrm{drift}} \mathcal {L} _ {\mathrm{src}} + \mathcal {L} _ {\mathrm{pl}} ^ {C} + \mathcal {L} _ {\mathrm{pl}} ^ {C ^ {\prime}} + \mathcal {L} _ {\mathrm{IM}}\tag{7}
$$

where $\mathcal { L } _ { \mathrm { s r c } }$ is the cross-entropy supervisory loss on sourcedomain labeled traffic, $\mathcal { L } _ { \mathfrak { p l } } ^ { C }$ and $\dot { \mathcal { L } } _ { \mathfrak { p l } } ^ { C ^ { \prime } }$ are the pseudo-label cross-entropy losses generated by C and $C ^ { \prime }$ respectively $( \mathcal { L } _ { \mathrm { p l } } ^ { C ^ { \prime } } = 0$ after the dual-classifier is deactivated), and ${ \mathcal { L } } _ { \mathrm { I M } }$ is the information maximization loss that prevents mode collapse by encouraging confident and diverse predictions. $\lambda _ { \mathrm { d r i f t } }$ is automatically determined by the drift-aware mechanism. Algorithm 1 presents the complete cyclic adaptation procedure.

Multi-round cycling enables pseudo-label quality to improve progressively across rounds. Suppose round t introduces some erroneous pseudo-labels; in round t + 1, the model— now with improved discriminative ability—re-evaluates all target-domain traffic and performs GMM filtering. Previously mislabeled samples may be rejected due to high prediction entropy, while previously omitted correct samples may be included due to low prediction entropy. This re-evaluation mechanism enables the quality and coverage of the pseudolabel set to increase with each round. Each cycle comprises one GMM fitting, an optional training round for $C ^ { \prime } .$ , and one joint fine-tuning round; the PAD computation is performed only once before adaptation begins. In practice, 3 to 5 rounds are typically sufficient, each completing within minutes on a single GPU, meeting the efficiency requirements of WF attacks.

## V. EXPERIMENTAL EVALUATION

This section systematically evaluates Aion from multiple dimensions. We first assess Aion’s performance under traffic drift across closed-world, open-world, and defense settings, as well as under browsing behavior drift and Tor version drift (§V-B). We then analyze Aion’s convergence speed and efficiency under streaming constraints (§V-C). Next, we examine Aion’s recovery capability for severely degraded classes (§V-D). Finally, we conduct configuration and mechanism analyses (§V-E), including drift-aware weight regulation, dualclassifier pseudo-label statistics, cost-effectiveness analysis, coverage-diagnosis validation, parameter sensitivity, and runtime overhead.

## A. Experimental Setup

Dataset. We use the publicly available temporal drift dataset released by Deng et al. [11] for evaluation. The dataset comprises over 300,000 real-world Tor traffic traces collected from 102 monitored websites selected from the Tranco list across multiple drift scenarios. Each trace is a sequence of length 5000 encoding packet direction and size information. Sourcedomain data is traffic collected at the initial time point (Day 0) for pre-training. Target-domain data spans five subsequent time points—Day 14, 30, 90, 150, and 270—covering drift from mild to severe over a nine-month period. For open-world experiments, traffic from 20,000 non-monitored websites is additionally introduced. For browsing behavior drift, sourcedomain traffic comes from homepage-only visits while targetdomain traffic includes in-depth subpage browsing across the same 102 websites. For Tor version drift, the model is trained on traffic collected under Tor 0.4.8 and evaluated on traffic from Tor 0.4.5. For defense experiments, we use the simulated WTF-PAD [28] defended dataset provided by Deng et al. [11].

Baseline methods. We compare Aion against eleven baseline methods: AWF [12], BAPM [39], ARES [15], DF [7], Net-CLR [16], Tik-Tok [8], Var-CNN [9], RF [10], Holmes [27], UAF [37], and Proteus [11]. Among these, Proteus and UAF are self-adaptive WF methods that leverage unlabeled drifted traffic through unsupervised self-training to continuously update the deployed model, requiring no labeled target-domain data; the remaining methods are standard WF attacks applied directly to drifted traffic without adaptation. All baseline implementations are reproduced using the open-source WF benchmark library [40]; for methods evaluated under identical experimental settings (same dataset, traffic representation, and evaluation protocol), we adopt the results reported in [11] to ensure consistency.

TABLE I: Parameter search ranges and default values of Aion.

<table><tr><td>Parameter</td><td>Search range</td><td>Final value</td></tr><tr><td>Training epochs per cycle E</td><td>[3, 10]</td><td>5</td></tr><tr><td>Dual-classifier active rounds R</td><td>[1, 5]</td><td>2</td></tr><tr><td>Auxiliary training epochs E&#x27;</td><td>[3, 10]</td><td>5</td></tr><tr><td>GMM filtering threshold τ</td><td>[0.3, 0.9]</td><td>0.6</td></tr><tr><td>High-confidence threshold τhigh</td><td>{0.8, 0.85, 0.9, 0.95}</td><td>0.9</td></tr><tr><td>PAD upper weight λmax</td><td>{0.8, 1.0, 1.2}</td><td>1.0</td></tr><tr><td>PAD lower weight λmin</td><td>{0.05, 0.1, 0.2}</td><td>0.1</td></tr><tr><td>PAD center threshold d0</td><td>{0.35, 0.45, 0.55, 0.65, 0.75}</td><td>0.55</td></tr><tr><td>PAD transition sharpness k</td><td>{2, 4, 6, 8, 10}</td><td>6</td></tr></table>

Evaluation metrics. Following standard practice in WF attack research [7], [11], we adopt accuracy (Acc), macroaveraged precision (P), recall (R), and F1-score (F1) as primary evaluation metrics, with F1 serving as the comprehensive metric for main comparisons. In the severe drift analysis, we additionally introduce the Acc@min-k metric, defined as the average accuracy of the k worst-performing classes, to measure recovery capability for tail-end degraded classes.

For open-world evaluation, we further report false-positiveoriented metrics using ROC curves and AUROC. Monitored traces are treated as positive samples and unmonitored traces as negative samples. We use the maximum predicted probability over all monitored classes as the monitored detection score and vary the decision threshold to compute the true positive rate (TPR) and false positive rate (FPR). AUROC summarizes the overall ability of a method to distinguish monitored traffic from unmonitored traffic across different thresholds.

Implementation details. Aion is implemented in PyTorch. All experiments are conducted on a server equipped with an NVIDIA RTX 4090 GPU, with each experiment independently run 3 times and averaged. The base WF model adopts the RF [10] architecture, pre-trained using the Adam optimizer with a learning rate of $1 \times 1 0 ^ { - 3 }$

For each target drift point, target-domain traces are split into a target-adaptation set and a held-out test set with a ratio of 9:1. The target-adaptation set is used for pseudolabel selection, PAD estimation, targeted labeling, and model adaptation, while the held-out test set is used only for final evaluation. For PAD estimation, Aion samples 20% of the source-domain data and 20% of the target-adaptation data to train a lightweight domain classifier in the feature space of the pre-trained WF model. The sampled source and target features are further split into 80% for domain-classifier fitting and 20% for domain validation using stratified sampling by domain. The PAD domain classifier is implemented as an SGD logistic-regression classifier with log loss. The SGD classifier is trained with a maximum of 1,000 iterations, convergence tolerance $1 0 ^ { - 3 }$ , and random seed 42.

Table I summarizes the search ranges and final values of Aion’s key parameters. These parameters are selected without using the held-out target test set and then fixed across all drift checkpoints. The same GMM filtering threshold τ is used for both the primary and auxiliary classifiers. Since the GMM is fitted separately to each classifier’s entropy distribution, the resulting posterior reliability score is computed with respect to the corresponding classifier. Using the same τ therefore provides a consistent pseudo-label reliability criterion for both classifiers.

For coverage diagnosis and targeted labeling, we set the minimum pseudo-label coverage requirement to $n _ { \mathrm { m i n } } = 5 .$ For each diagnosed coverage-deficient class, Aion uses $S = 5$ labeled samples for targeted labeling and applies data augmentation with factor $\gamma = 5$

## B. Performance Evaluation Under Traffic Drift

Temporal drift in the closed-world setting. Table II presents the performance of each method at five temporal drift points in the closed-world setting. AWF drops from 48.84% F1 at Day 14 to 28.64% at Day 270, a cumulative decline of 20.20%. Tik-Tok, Var-CNN, and DF exhibit similar trends, with cumulative F1 declines of 31.31%, 28.93%, and 27.46%, respectively. Methods that incorporate robustnessoriented architectural or training designs, such as TF, RF, BAPM, and TMWF, partially alleviate this degradation yet still fall short of adaptive methods over longer time horizons. Among them, RF achieves the highest F1 of 59.57% at Day 270, compared to 87.63% at Day 14, a decrease of 28.06%. These results confirm that temporal drift constitutes the primary performance bottleneck for long-term WF attack deployment.

Aion outperforms the state-of-the-art adaptive WF method Proteus at most drift checkpoints, while the two methods remain comparable when drift is still mild. In the early stage of drift, source-domain knowledge remains highly relevant to the target domain, allowing both methods to obtain similar performance. As drift intensifies, however, Aion shows a clearer advantage. At Day 150, Aion achieves 89.00% F1, exceeding Proteus by 2.68 percentage points. At Day 270, where drift is most severe, Aion reaches 88.14% while Proteus drops to 82.27%, widening the gap to 5.87 percentage points.

Over the full span from Day 14 to Day 270, Proteus’s F1 cumulatively decreases by 10.26%, whereas Aion decreases by only 4.17%. This advantage under moderate-tosevere drift stems from the drift-aware regulation mechanism, which grants the model greater adaptation freedom when the distribution gap is large, and the targeted labeling mechanism, which restores supervisory signals for classes where fails to provide reliable supervision.

Temporal drift in the open-world setting. The open-world setting requires WF attacks to correctly identify monitored website traffic while rejecting large volumes of unmonitored traffic. After drift, the features of monitored websites may become confused with unmonitored traffic, leading to elevated false positive rates. Table III presents the F1-scores of each method in the open-world setting.

All unadapted attacks exhibit larger degradation than in the closed-world setting; for example, RF drops from 85.97% at Day 14 to 36.83% at Day 270, a cumulative decrease of 49.14 percentage points. Aion consistently outperforms Proteus across all drift points, with the performance gap increasing from 2.52 percentage points at Day 14 to 8.90 percentage points at Day 270. In particular, Aion still achieves 82.84% F1 after 270 days of drift, exceeding Proteus’s 79.15% F1 at Day 150. This result indicates that Aion is more robust to accumulated open-world drift and better preserves classification effectiveness over extended deployment periods.

TABLE II: Performance comparison of WF methods at five temporal drift points in the closed-world setting (%). P, R, and F1 denote macro-averaged Precision, Recall, and F1-score, respectively. Best results are in bold.

<table><tr><td rowspan="2">Attack</td><td colspan="3">Day 14</td><td colspan="3">Day 30</td><td colspan="3">Day 90</td><td colspan="3">Day 150</td><td colspan="3">Day 270</td></tr><tr><td>P</td><td>R</td><td>F1</td><td>P</td><td>R</td><td>F1</td><td>P</td><td>R</td><td>F1</td><td>P</td><td>R</td><td>F1</td><td>P</td><td>R</td><td>F1</td></tr><tr><td>AWF</td><td>50.36</td><td>49.29</td><td>48.84</td><td>46.42</td><td>46.05</td><td>45.36</td><td>38.28</td><td>39.09</td><td>37.49</td><td>33.12</td><td>33.63</td><td>32.21</td><td>29.40</td><td>30.07</td><td>28.64</td></tr><tr><td>BAPM</td><td>64.62</td><td>62.83</td><td>62.08</td><td>58.89</td><td>57.33</td><td>56.28</td><td>48.48</td><td>48.78</td><td>46.75</td><td>44.28</td><td>43.92</td><td>41.89</td><td>38.38</td><td>38.30</td><td>35.98</td></tr><tr><td>ARES</td><td>71.36</td><td>69.07</td><td>68.82</td><td>66.74</td><td>64.72</td><td>64.17</td><td>56.53</td><td>55.96</td><td>54.05</td><td>49.06</td><td>49.21</td><td>47.43</td><td>46.04</td><td>45.51</td><td>43.48</td></tr><tr><td>DF</td><td>73.30</td><td>72.10</td><td>71.94</td><td>67.12</td><td>66.49</td><td>65.79</td><td>55.91</td><td>57.17</td><td>55.24</td><td>50.11</td><td>50.49</td><td>48.91</td><td>45.47</td><td>46.69</td><td>44.48</td></tr><tr><td>NetCLR</td><td>73.78</td><td>72.93</td><td>72.71</td><td>68.27</td><td>67.47</td><td>66.92</td><td>56.99</td><td>57.94</td><td>55.81</td><td>49.29</td><td>50.82</td><td>49.03</td><td>44.72</td><td>46.80</td><td>43.92</td></tr><tr><td>Tik-Tok</td><td>78.98</td><td>78.35</td><td>77.89</td><td>73.46</td><td>73.25</td><td>72.36</td><td>62.01</td><td>63.08</td><td>60.87</td><td>53.89</td><td>54.90</td><td>52.56</td><td>48.70</td><td>49.47</td><td>46.58</td></tr><tr><td>Var-CNN</td><td>81.23</td><td>79.93</td><td>79.77</td><td>76.20</td><td>74.76</td><td>74.30</td><td>65.03</td><td>65.43</td><td>63.14</td><td>57.43</td><td>58.14</td><td>55.68</td><td>52.79</td><td>53.49</td><td>50.84</td></tr><tr><td>RF</td><td>88.46</td><td>87.99</td><td>87.63</td><td>82.92</td><td>82.15</td><td>81.62</td><td>73.83</td><td>73.85</td><td>72.02</td><td>68.07</td><td>68.13</td><td>66.25</td><td>61.00</td><td>62.81</td><td>59.57</td></tr><tr><td>Proteus</td><td>92.53</td><td>92.59</td><td>92.53</td><td>91.21</td><td>91.23</td><td>91.18</td><td>90.67</td><td>90.77</td><td>90.65</td><td>86.15</td><td>86.82</td><td>86.32</td><td>81.90</td><td>83.21</td><td>82.27</td></tr><tr><td>Aion</td><td>92.33</td><td>92.29</td><td>92.31</td><td>91.19</td><td>92.32</td><td>91.33</td><td>91.02</td><td>90.91</td><td>90.89</td><td>89.16</td><td>89.34</td><td>89.00</td><td>88.12</td><td>88.98</td><td>88.14</td></tr></table>

![](images/590fcf75e05624148d6f402d12ac28c3784836f386657297134f591a75628d50.jpg)  
(a) Day 90

![](images/092e1f954e2931274cff7f0464e2102a2b1b46ab447bb890ebffd56f9ecec2be.jpg)  
(b) Day 150

![](images/a5afc2d85082c0bb242db61ccbccb199e4e10c4442d2dafe952fe88ebf61953b.jpg)  
(c) Day 270  
Fig. 3: ROC curves of different WF methods in the open-world setting at Day 90, Day 150, and Day 270.

TABLE III: F1-scores (%) of WF methods at five temporal drift points in the open-world setting.

<table><tr><td>Attack</td><td>Day 14</td><td>Day 30</td><td>Day 90</td><td>Day 150</td><td>Day 270</td></tr><tr><td>AWF</td><td>46.30</td><td>44.34</td><td>35.61</td><td>31.02</td><td>26.52</td></tr><tr><td>BAPM</td><td>59.74</td><td>54.70</td><td>44.91</td><td>40.00</td><td>33.63</td></tr><tr><td>ARES</td><td>67.88</td><td>63.73</td><td>50.96</td><td>40.95</td><td>26.42</td></tr><tr><td>DF</td><td>67.85</td><td>62.93</td><td>50.41</td><td>40.50</td><td>25.92</td></tr><tr><td>NetCLR</td><td>71.94</td><td>66.28</td><td>54.50</td><td>46.06</td><td>32.81</td></tr><tr><td>Tik-Tok</td><td>75.41</td><td>70.24</td><td>58.43</td><td>50.88</td><td>37.86</td></tr><tr><td>Var-CNN</td><td>78.53</td><td>73.16</td><td>60.45</td><td>47.33</td><td>26.49</td></tr><tr><td>RF</td><td>85.97</td><td>79.88</td><td>68.54</td><td>60.59</td><td>36.83</td></tr><tr><td>Proteus</td><td>88.23</td><td>84.98</td><td>82.97</td><td>79.15</td><td>73.94</td></tr><tr><td>Aion</td><td>90.75</td><td>88.87</td><td>87.53</td><td>84.30</td><td>82.84</td></tr></table>

To further evaluate false-positive-sensitive performance, we report ROC curves and AUROC in the open-world setting. Monitored traces are treated as positive samples and unmonitored traces as negative samples. Given the (W+1)-class softmax output, we use the maximum monitored-class probability $s ( x ) = \mathrm { m a x } _ { 1 \leq k \leq W } p _ { k } ( x )$ as the monitored detection score and sweep the decision threshold to compute the trade-off between true positive rate and false positive rate. As shown in Fig. 3, Aion consistently achieves the highest AUROC across Day 90, Day 150, and Day 270, reaching 0.9802, 0.9467, and 0.8912, respectively. Compared with Proteus, Aion improves AUROC by 3.89, 4.15, and 3.21 percentage points at the three drift points.

The ROC results show that Aion improves not only fixedthreshold F1-score but also monitored/unmonitored separability across different decision thresholds. As drift becomes more severe, the curves of non-adaptive attacks move substantially closer to the diagonal. At Day 270, most non-adaptive methods obtain AUROC values around 0.60–0.66, indicating that temporal drift severely weakens their ability to reject unmonitored traffic. In contrast, Aion maintains an AUROC of 0.8912 and its curve remains clearly above Proteus and all non-adaptive baselines, especially in the low-FPR region. This demonstrates that Aion better preserves open-world rejection capability, which is critical when non-monitored traffic dominates practical WF deployment.

To evaluate Aion as a general-purpose adaptation module, we integrate it into RF, ARES, NetCLR, and DF, which represent four architecturally diverse state-of-the-art WF models.

TABLE IV: F1-scores (%) under WTF-PAD defense with temporal drift.

<table><tr><td>Attack</td><td>Day 14</td><td>Day 30</td><td>Day 90</td><td>Day 150</td><td>Day 270</td></tr><tr><td>Base</td><td>74.33</td><td>65.92</td><td>60.95</td><td>53.71</td><td>50.63</td></tr><tr><td>Proteus</td><td>82.09</td><td>78.02</td><td>80.44</td><td>73.80</td><td>70.91</td></tr><tr><td>Aion</td><td>83.45</td><td>79.08</td><td>83.05</td><td>77.34</td><td>77.47</td></tr></table>

TABLE V: Performance comparison under browsing behavior drift (%).

<table><tr><td rowspan="2">Attack</td><td colspan="3">Homepage</td><td colspan="3">Subpages</td></tr><tr><td>P</td><td>R</td><td>F1</td><td>P</td><td>R</td><td>F1</td></tr><tr><td>AWF</td><td>54.74</td><td>53.74</td><td>53.04</td><td>22.18</td><td>22.87</td><td>21.68</td></tr><tr><td>BAPM</td><td>70.29</td><td>65.68</td><td>65.38</td><td>29.98</td><td>27.67</td><td>25.96</td></tr><tr><td>ARES</td><td>75.36</td><td>73.28</td><td>72.77</td><td>31.87</td><td>31.96</td><td>29.87</td></tr><tr><td>DF</td><td>77.73</td><td>77.11</td><td>76.72</td><td>32.12</td><td>33.56</td><td>31.36</td></tr><tr><td>NetCLR</td><td>78.66</td><td>77.58</td><td>77.27</td><td>34.10</td><td>35.50</td><td>33.58</td></tr><tr><td>Tik-Tok</td><td>83.48</td><td>82.00</td><td>81.82</td><td>36.07</td><td>36.66</td><td>34.56</td></tr><tr><td>Var-CNN</td><td>85.08</td><td>83.60</td><td>83.59</td><td>39.58</td><td>39.19</td><td>37.24</td></tr><tr><td>RF</td><td>89.85</td><td>89.21</td><td>89.00</td><td>48.79</td><td>46.74</td><td>44.76</td></tr><tr><td>Proteus</td><td>91.28</td><td>91.40</td><td>91.18</td><td>55.32</td><td>56.32</td><td>55.24</td></tr><tr><td>Aion</td><td>91.19</td><td>92.23</td><td>91.21</td><td>57.48</td><td>58.87</td><td>57.56</td></tr></table>

As shown in Fig. 4, Aion consistently delivers substantial performance recovery over the corresponding non-adaptive base models across all settings. Among the four backbones, the largest improvement is observed when RF is used as the base model. At Day 270, the accuracy of RF drops to 37.12% without adaptation, recovers to 74.93% after integrating Proteus, and further increases to 83.31% after integrating Aion. These results indicate that Aion’s adaptation mechanisms are model-agnostic and can be effectively transferred to existing WF attacks.

Temporal drift under defense. We further evaluate Aion under the compound challenge of temporal drift and WF defense perturbations. We use WTF-PAD as the representative defense because it is a widely studied lightweight padding method that injects dummy packets to confuse website fingerprints [28]. It is also practically relevant, as WTF-PAD-style randomized padding has inspired variants incorporated into Tor’s deployed padding framework after Tor v3 [41].

Table IV presents performance under the WTF-PAD defense. Here, Base denotes the RF classifier evaluated without adaptation under WTF-PAD. The Base model degrades steadily as drift accumulates, with its F1-score decreasing from 74.33% at Day 14 to 50.63% at Day 270, showing that temporal drift further amplifies the perturbation effect introduced by defense.

Both adaptive methods substantially recover performance over the Base model, but Aion consistently outperforms Proteus at all time points. At Day 270, Proteus improves F1 from 50.63% to 70.91%, whereas Aion further increases it to 77.47%, exceeding Proteus by 6.56 percentage points and the Base model by 26.84 percentage points. These results show that Aion remains effective when temporal drift is combined with defense-induced perturbations.

Other traffic drift. Beyond temporal evolution, changes in user browsing behavior and Tor Browser version updates also induce traffic drift. Table V presents performance under browsing behavior drift, where source-domain traffic comes from a homepage-only browsing pattern and target-domain traffic includes in-depth subpage browsing. This setting differs from ordinary temporal drift because the monitored website remains the same, but the user interacts with different page depths and content paths. Subpage visits usually trigger more HTTP requests, more diverse embedded resources, longer loading sequences, and more variable session durations. As a result, the traffic fingerprint learned from homepage visits no longer fully represents the target-domain browsing behavior. RF drops from 89.00% in the homepage scenario to 44.76% in the subpage scenario, showing that behavior-induced drift can substantially weaken a static WF classifier.

TABLE VI: F1-score comparison of Proteus, UAF, and Holmes across three drift scenarios (%).

<table><tr><td>Attack</td><td>Day 0→270</td><td>Tor 0.4.8→0.4.5</td><td>Homepage→Subpage</td></tr><tr><td>UAF</td><td>50.31</td><td>51.15</td><td>36.50</td></tr><tr><td>Holmes</td><td>54.31</td><td>55.62</td><td>38.82</td></tr><tr><td>Proteus</td><td>82.27</td><td>88.28</td><td>55.24</td></tr><tr><td>Aion</td><td>88.14</td><td>93.50</td><td>57.56</td></tr></table>

Aion achieves 57.56% in the subpage scenario, exceeding Proteus’s 55.24% by 2.32%. The improvement is smaller than that under long-term temporal drift because homepage and subpage traffic still share part of the same website-level structure, such as domain-specific resource organization and service interaction patterns. Therefore, unsupervised pseudolabeling can still recover part of the target distribution, leaving fewer severe coverage-deficient classes for targeted labeling to repair. Nevertheless, Aion remains consistently better than Proteus because its drift-aware regulation relaxes the sourcedomain constraint when the homepage-only source data becomes less representative, while the dual-classifier mechanism helps expand pseudo-label coverage for subpage traces that deviate from homepage patterns.

Table VI further compares Aion with two additional drift adaptation methods, UAF [37] and Holmes [27], across three drift scenarios. Aion outperforms all methods in every scenario: under 270 days of temporal drift, Aion achieves 88.14% F1 compared to 82.27% (Proteus), 54.31% (Holmes), and 50.31% (UAF); under Tor version drift, Aion achieves 93.50%, exceeding Proteus by 5.22 percentage points.

The performance gap varies across drift scenarios, suggesting that different drift sources affect WF fingerprints with different degrees of severity and heterogeneity. Long-term temporal drift may be caused by multiple factors, including website content updates, embedded resource changes, Tor network dynamics, and browser-side changes. Its effect can therefore be more uneven across website classes. The larger improvement of Aion in this setting indicates that the combination of PAD-based regulation, dual-classifier pseudo-label expansion, and targeted labeling provides stronger recovery capability.

By comparison, Tor-version drift and browsing-behavior drift appear to be more structured in our evaluation. Torversion drift mainly reflects changes in the Tor/browser environment, and some website-discriminative patterns may remain available, leading to relatively high absolute performance for adaptive methods. In homepage-to-subpage drift, the browsing path and resource-loading process change, but traces from the same website may still preserve partial shared structure. Therefore, Aion still improves over the baselines in these two scenarios, but the margin is more moderate than under long-term temporal drift.

![](images/fe42b9b8116dd06ab7a6a07437390d683c8557c49a3a0a56532208052f468ff7.jpg)  
（a) RF

![](images/20ceb6277a3a307db099d7865f6acce0d97cea4a28b411d28d1eff4c0a921d4f.jpg)  
（b) ARES

![](images/b7966b28234038012b2bf154c0c47fc00748d890eb64a7a1bdcd1f8183704d29.jpg)  
（c) NetCLR

![](images/52d601c847007226303b9192f3bbf10a9d37d2742feb2306497a642f1edab44d.jpg)  
（d) DF  
Fig. 4: Accuracy variation when Aion and Proteus are integrated into four base WF models in the open-world setting.

TABLE VII: F1-score comparison (%) under single-pass streaming constraint.

<table><tr><td>Attack</td><td>Day 14</td><td>Day 30</td><td>Day 90</td><td>Day 150</td><td>Day 270</td></tr><tr><td>Proteus</td><td>87.77</td><td>88.18</td><td>83.62</td><td>80.77</td><td>75.40</td></tr><tr><td>Aion</td><td>89.91</td><td>89.33</td><td>87.45</td><td>86.40</td><td>86.32</td></tr><tr><td>Improvement</td><td>↑ 2.14</td><td>↑ 1.15</td><td>↑ 3.83</td><td>↑ 5.63</td><td>↑ 10.92</td></tr></table>

## C. Adaptation Efficiency Analysis

In practical deployment, when model performance degrades due to temporal drift, the attacker needs to complete adaptation as quickly as possible to restore monitoring capability. Each additional training round extends the performance degradation window. We refer to this setting as the single-pass streaming constraint.

To evaluate adaptation efficiency under realistic constraints, we design a single-pass experiment in which all methods perform pseudo-label selection only once, fine-tune the model for 5 epochs on the selected pseudo-labels, and immediately discard all unselected samples. Specifically, Proteus performs one round of GMM filtering with its single classifier, while Aion’s primary classifier $C$ and auxiliary classifier C<sup>′</sup> each perform one round of pseudo-label selection independently. This setting simulates a streaming scenario where traffic is processed once and not revisited.

Table VII presents the results under this constraint. Under mild drift at Day 14 and Day 30, Aion leads Proteus by 1–3 percentage points, as both methods can obtain sufficient highconfidence pseudo-labels in a single selection. As drift intensifies, the gap widens substantially. At Day 150, Aion reaches 86.40% against Proteus’s 80.77%, a lead of 5.63 percentage points. At Day 270, Aion achieves 86.32% while Proteus drops to 75.40%, widening the gap to 10.92 percentage points.

![](images/8372533eb22ddb56402d1249d1a09c1af1e80f1e7b178a6daadca4b437debb68.jpg)  
Fig. 5: Number of cliff-edge degraded classes (accuracy <10%) at each time point. The number of degraded classes increases continuously with drift duration, and is particularly pronounced in the open-world setting.

Notably, Aion’s 86.32% from a single pseudo-label selection at Day 270 already exceeds Proteus’s final result of 82.27% after complete multi-round cyclic adaptation. This advantage stems from two factors. Aion’s dual-classifier complementary filtering improves pseudo-label coverage in a single operation, and the drift-aware mechanism directs more gradient updates toward target-domain signals under severe drift.

## D. Severe Drift Class Analysis

The impact of temporal drift is highly non-uniform across website classes. Some websites undergo only gradual stylistic adjustments, while others experience fundamental changes in traffic features due to page structure redesign or CDN switching. We term the phenomenon where certain classes drop from high accuracy to near-complete unrecognizability as cliff-edge degradation. Fig. 5 shows that the number of classes with accuracy below 10% on the unadapted RF model grows from 0 at Day 30 to 10 at Day 270 in the closed-world setting, and further increases to 45 in the open-world setting, indicating that this phenomenon intensifies with drift duration.

While cliff-edge degraded classes may have limited impact on the overall F1-score, their practical impact is nonnegligible, because they may correspond to privacy-sensitive monitored websites or security-critical classes in risk assessment. Therefore, evaluating only aggregate metrics can obscure the failure of WF models on the most severely drifted websites. We introduce the Acc@min-k metric, defined as the average accuracy of the k lowest-performing classes, to measure recovery capability for the most severely degraded classes. Fig. 6 presents the Acc@min-k comparison at Day 150 and Day 270.

![](images/97a57016f44b1dcf91f53aad55bc3bb25d0ae8e6391ae2e5b804c7e9e87045b6.jpg)

![](images/294f01a816969689ec42b96e082b4e7825d80c4795b2b91e98ea7ea649bd72ec.jpg)  
（a) Closed World Acc@min-�

![](images/2ed922b37f468ad958d9cc12684e5c2e3b3db1a623f1dc2f348ceb0ea98d3726.jpg)  
（b) Open World Acc@min-�  
Fig. 6: Recovery performance for severely degraded classes (Acc@min-k, %) at Day 150 and Day 270. (a) Closedworld setting: left shows Acc@min-5, right shows Acc@min-10. (b) Open-world setting: same layout. Aion consistently recovers tail-end degraded classes that remain near-zero under both the unadapted baseline and Proteus.

TABLE VIII: Impact of source-domain constraint weight λ on F1-score (%).

<table><tr><td>Weight λ</td><td>Day 14</td><td>Day 30</td><td>Day 90</td><td>Day 150</td><td>Day 270</td></tr><tr><td>0.1 (weak)</td><td>89.01</td><td>84.90</td><td>87.51</td><td>86.59</td><td>87.17</td></tr><tr><td>0.2</td><td>89.58</td><td>87.08</td><td>89.45</td><td>87.55</td><td>87.64</td></tr><tr><td>0.5</td><td>91.40</td><td>89.60</td><td>90.74</td><td>87.59</td><td>87.44</td></tr><tr><td>1.0 (strong)</td><td>92.45</td><td>91.11</td><td>90.51</td><td>86.59</td><td>84.97</td></tr><tr><td>PAD (adaptive)</td><td>92.31</td><td>91.33</td><td>90.89</td><td>89.00</td><td>88.14</td></tr></table>

Fig. 7: Pseudo-label statistics of the dual-classifier mechanism at Day 270 in the closed-world and open-world settings. The left y-axis reports the number of pseudo-labels selected by C, selected by $C ^ { \prime }$ , and shared by both classifiers, while the right y-axis reports pseudo-label accuracy and the error rate of C on conflict samples.

In the closed-world Day 270 scenario, the baseline model’s Acc@min-5 is 0%, and Proteus recovers to only 1.06%— because GMM filtering cannot extract reliable supervisory signals from classes whose predictions are near-random, leaving them without effective labels throughout adaptation. In contrast, Aion’s coverage diagnosis module identifies these classes and injects supervisory signals through targeted labeling, achieving an Acc@min-5 of 36.51% in the closedworld setting. In the open-world Day 270 setting, Proteus’s Acc@min-5 and Acc@min-10 both drop to near 0%, while Aion maintains 32.91% and 51.12%, respectively. Under the milder drift of Day 150, Aion maintains a consistent advantage. These results demonstrate that coverage-diagnosis-driven targeted labeling effectively fills the structural blind spots of purely unsupervised self-training under extreme drift.

## E. Configuration Analysis of Aion

Drift-Aware Mechanism Analysis. To validate the effectiveness of PAD-based drift-aware adaptive weight regulation, we compare Aion’s adaptive weight with multiple fixed weight configurations. As shown in Table VIII, no single fixed weight achieves optimal performance across all drift scenarios. A strong constraint with $\lambda = 1 . 0$ performs well under mild drift, reaching 92.45% F1 at Day 14, but degrades to 84.97% at Day 270 because it overly restricts migration toward the severely drifted target domain. A weak constraint with $\lambda = 0 . 1$ yields better Day 270 performance of 87.17% but underperforms at Day 14 with only 89.01%, as it fails to leverage source-domain knowledge for pseudo-label noise suppression. A compromise at $\lambda = 0 . 5$ remains suboptimal at both extremes.

The PAD adaptive weight matches or closely approximates the optimal fixed weight at each checkpoint by automatically mapping drift severity to appropriate constraint strength. When drift is mild, $d _ { \mathcal { A } }$ remains low and $\lambda _ { \mathrm { d r i f t } }$ stays close to 1.0, preserving strong source-domain regularization to suppress pseudo-label noise; as drift intensifies, $\lambda _ { \mathrm { d r i f t } }$ decreases proportionally, dropping to approximately 0.14 at Day 270 and granting the model sufficient freedom to adapt to the shifted distribution. This result demonstrates that the PAD mechanism reduces the need for manually selecting a fixed source-domain weight across drift checkpoints.

Dual-Classifier Mechanism Analysis. To substantiate the role of the auxiliary classifier $C ^ { \prime } ,$ , we analyze fine-grained pseudo-label statistics on Day 270. Specifically, we allow $C ^ { \prime }$ to participate in different numbers of adaptation cycles and report the number of pseudo-labels selected by the primary classifier C, the number selected by the auxiliary classifier $C ^ { \prime } ,$ their overlap, and the corresponding pseudo-label accuracy in both closed-world and open-world settings. A conflict sample is defined as a target sample selected by both classifiers but assigned different pseudo-labels. According to Aion’s merging rule, such samples are discarded in the current cycle to avoid injecting contradictory supervision. Fig. 7 presents the results, where the left y-axis reports the number of pseudo-labels and the right y-axis reports accuracy or error rate. The auxiliary classifier’s additional contribution can be reflected by the gap between the pseudo-labels selected by $C ^ { \prime }$ and the overlap between $C$ and $C ^ { \prime }$

In the closed-world setting, $C ^ { \prime }$ provides the most significant benefit in the first two adaptation cycles. In the first cycle, the primary classifier selects only a limited number of high-confidence pseudo-labels, while the auxiliary classifier mines additional target-domain samples. By the second cycle, the numbers of pseudo-labels selected by $C ,$ selected by $C ^ { \prime } ,$ and shared by both classifiers all increase substantially, indicating that $C ^ { \prime }$ helps accelerate early adaptation toward the target distribution. However, as adaptation continues, the overlap between the two classifiers becomes increasingly high, suggesting that the auxiliary classifier contributes fewer new samples. Meanwhile, the pseudo-label accuracy of $C ^ { \prime }$ starts to decrease, indicating a higher risk of introducing noisy labels if $C ^ { \prime }$ remains active for too many cycles. Therefore, in the closed-world setting, the main benefit of $C ^ { \prime }$ lies in the early adaptation stage.

The open-world setting shows a more pronounced effect. Since open-world WF contains a large amount of nonmonitored traffic, the model must not only distinguish monitored classes but also reject unmonitored samples, making early pseudo-label noise more harmful. In the first cycle, the primary classifier selects many pseudo-labels but with relatively low accuracy. More importantly, the error rate of the primary classifier on conflict samples is very high, meaning that these samples would likely become incorrect supervision if only the primary classifier were used. By introducing $C ^ { \prime } ,$ Aion can identify such inconsistent samples and discard them through the conflict-filtering rule, thereby reducing error accumulation. As adaptation proceeds, the accuracy of $C$ recovers quickly, the overlap between $C$ and $C ^ { \prime }$ increases, and the marginal contribution of $C ^ { \prime }$ decreases. This indicates that $C ^ { \prime }$ not only expands pseudo-label coverage but also helps filter high-risk samples in the open-world setting, which partly explains Aion’s larger advantage in open-world evaluation.

Overall, the dual-classifier mechanism contributes in two ways. First, it expands high-confidence pseudo-label coverage in early adaptation cycles, helping the model move more quickly toward the target distribution. Second, in noisier settings such as open-world WF, disagreement between $C$ and $C ^ { \prime }$ helps detect and remove potentially incorrect pseudolabels, suppressing error propagation. At the same time, the results show that keeping $C ^ { \prime }$ active throughout all cycles is unnecessary: its additional coverage decreases as adaptation progresses, while its pseudo-label noise risk increases. Therefore, Aion activates the dual-classifier mechanism only in the first R = 2 cycles by default, achieving a better balance between coverage expansion and noise control.

Cost-Effectiveness Analysis. Since Aion uses a small number of actively labeled target-domain samples, we further compare different methods under controlled label budgets at Day 270 in the closed-world setting. Fine-tuning(0) and Proteus(0) denote the non-adaptive RF model and the purely unsupervised Proteus baseline, respectively. Aion(0) disables targeted labeling and keeps only the drift-aware regulation and dual-classifier pseudo-labeling components. For the equallabel-budget comparison, Fine-tuning(35), Proteus(35), and Aion(35) all use the same 35 labeled target-domain samples, while Fine-tuning(510) uses five labeled samples for every monitored website as a higher-cost reference.

![](images/f816bc3f32b8c310185265244e909153284ad20844f4a44b39951d548435aaa6.jpg)  
Fig. 8: Cost-effectiveness comparison of different methods at Day 270 under closed-world conditions, where N denotes the total number of labeled samples used by each method.

Fig. 8 reports the results. Fine-tuning(0) achieves 59.57% F1 under severe Day 270 drift, and using 35 labeled targetdomain samples only improves it to 64.43%. Even with 510 labeled samples, Fine-tuning(510) reaches 71.81%, showing that sparse target-domain labels alone are not sufficient without an effective adaptation mechanism. Proteus(0) achieves 82.27%, and Proteus(35) improves slightly to 83.81% with the same 35 labels. Aion(0) achieves 83.03% without targeted labeling, indicating that its unsupervised components already provide competitive adaptation.

With the same 35-label budget, Aion(35) reaches 88.14% F1, outperforming Proteus(35) and Fine-tuning(35). Since Proteus(35) uses the same labeled target-domain samples, this improvement is not simply due to the label budget itself. Instead, it indicates that Aion’s drift-aware regulation, dualclassifier pseudo-label expansion, and coverage-guided label selection make the limited labeled samples more effective, especially for classes that are difficult to recover through pseudo-labeling alone.

Targeted Labeling Budget Analysis. We further investigate how targeted labeling affects both aggregate and worst-case performance. We vary S from 0 to 10 while keeping the set of diagnosed classes fixed at the seven classes identified as coverage-deficient under 270 days of drift. Fig. 9 shows that increasing the label budget simultaneously improves overall F1, Acc@min-5, and Acc@min-10. Without targeted labels (S=0), the model obtains 83.03% F1 but only 1.69% and 28.18% on Acc@min-5 and Acc@min-10, indicating that several classes remain unrecovered. Adding a single targeted sample per diagnosed class (S=1) lifts these metrics to 84.98%, 25.74%, and 38.31%, respectively. With S=5, F1 reaches 88.14% while Acc@min-5 and Acc@min-10 climb to

![](images/34e41b4662af212e401a62ada68935e9e8bb3eb3578c387aea34222c089926e5.jpg)  
Fig. 9: Performance of targeted labeling at Day 270 under closed-world conditions. The curves report overall F1, Acc@min-5, and Acc@min-10 as functions of the number of labeled samples S collected per coverage-deficient class.

36.51% and 48.70%, capturing most of the available gain with fewer than 40 targeted visits in total. Larger budgets continue to benefit severely drifted classes: at S=10, F1 increases to 90.23% and the Acc@min-5/10 metrics rise to 41.97% and 57.15%, demonstrating that targeted labeling directly recovers the classes where unsupervised adaptation alone is insufficient.

Runtime Overhead Analysis. To quantify the computational overhead introduced by PAD and the dual-classifier mechanism, we measure the runtime of each component on the moderately drifted Day 90 setting using an NVIDIA RTX 4090 GPU. This setting contains 102 monitored classes with approximately 100 samples per class, following the same data split protocol described in Section V-A. As shown in Fig. 10, PAD computation takes only 2.55s, and the auxiliary classifier C<sup>′</sup> training takes 5.15s. These two components introduce limited overhead because PAD is computed only once before adaptation, and C<sup>′</sup> is trained only in the first two adaptation rounds.

We further compare the per-round adaptation time of Aion and Proteus, where each adaptation round contains five training epochs. Aion takes 61.73s per adaptation round, which is comparable to and slightly lower than Proteus’s 67.95s. This is because Aion introduces lightweight PAD and auxiliaryclassifier operations, but does not require the MMD calculation used in Proteus during each adaptation round. Therefore, the additional mechanisms of Aion have a small impact on total runtime while improving adaptation effectiveness. In practice, Aion can reach stronger drift adaptation performance with fewer effective adaptation rounds, making the overall overhead controllable for long-term WF deployment.

## VI. DISCUSSION

## A. Summary

This paper presents Aion, a drift-aware adaptive website fingerprinting framework designed for continuous deployment under temporal traffic drift. Our investigation reveals that the key bottleneck in self-training-based WF adaptation is not pseudo-label noise per se, but rather the mismatch between a fixed training strategy and time-varying drift severity, compounded by the inability of a single unsupervised classifier to maintain adequate class coverage under extreme distributional shift. Aion addresses this through three complementary mechanisms. The drift-aware adaptive regulation module automatically adjusts source-domain constraint strength according to the measured drift severity. The dual-classifier collaborative pseudo-label generation mechanism broadens class coverage and accelerates target-domain adaptation. The coverage-diagnosis-based targeted labeling strategy repairs the structural blind spots of purely unsupervised self-training at minimal annotation cost.

![](images/4e11ff2fd6a228de82c5144da65b3e478f671508c7f46b7b5928ac8021c61994.jpg)  
Fig. 10: Runtime overhead of PAD, auxiliary classifier training, and per-round adaptation on the Day 90 drift setting.

Extensive experiments spanning 270 days of real-world traffic drift across closed-world, open-world, defense, and streaming settings demonstrate that Aion consistently outperforms existing methods under moderate-to-severe drift. Under 270 days of drift, Aion achieves F1 improvements of 5.87, 8.90, and 10.92 percentage points over the state-of-the-art adaptive method Proteus in closed-world, open-world, and streaming settings, respectively, while reducing the magnitude of long-term performance degradation by over half. Singlepass experiments further confirm that Aion’s one-shot adaptation already exceeds Proteus’s full multi-round performance, demonstrating practical feasibility under streaming constraints.

## B. Limitations and Future Work

Aion demonstrates strong performance across diverse drift scenarios, yet some limitations deserve discussion.

Targeted labeling requires limited re-collection. Aion’s targeted labeling mechanism substantially reduces annotation cost by focusing collection on the small subset of coveragedeficient classes, yet it still requires the attacker to re-visit a limited number of monitored websites via Tor. This requirement reflects a fundamental trade-off in WF attack deployment between adaptation quality and collection feasibility. In the extreme case where re-collection is entirely infeasible, Aion gracefully degrades to a purely unsupervised mode that still outperforms existing unsupervised baselines, though coverage of the most severely drifted classes becomes constrained.

Global PAD may miss localized class-level drift. PAD estimates a global source-target discrepancy in the current feature space and therefore provides a single regulation coefficient for all monitored classes. This design is simple and stable, but it may be suboptimal when drift is highly localized.

For example, if only a small subset of websites undergoes severe redesign while most websites remain stable, the overall PAD value may still be moderate and the resulting $\lambda _ { \mathrm { d r i f t } }$ may preserve a stronger source-domain constraint than those severely drifted classes require. Aion partially mitigates this issue through coverage diagnosis and targeted labeling, which identify and repair classes that fail to obtain reliable pseudolabels. Nevertheless, designing class-wise drift estimates and per-class source regularization remains an important direction for future work.

## C. Ethical Considerations

This work studies website fingerprinting attacks under realistic traffic drift, aiming to understand the long-term robustness of adaptive WF attacks and provide evidence for evaluating durable defenses. All experiments are conducted on previously collected Tor traffic traces and controlled website visits. We do not collect real user identities, account information, plaintext browsing content, or any personally identifiable information. The monitored labels correspond to websites selected for experimental evaluation rather than to user-specific browsing histories.

We restrict the scope of the study to offline evaluation. Aion is evaluated as an adaptive attack framework on benchmark traces, and the targeted labeling component revisits attackerside controlled monitored websites without interacting with real user traffic. Understanding adaptive attacks under realistic drift is necessary for designing and evaluating robust anonymity defenses. The results highlight that defenses should be evaluated not only against static classifiers but also against attackers capable of limited adaptation over time.

## VII. CONCLUSION

We propose Aion, a drift-aware adaptive framework that systematically addresses temporal drift in website fingerprinting through drift-aware regulation, dual-classifier pseudo-label generation, and coverage-guided targeted labeling. Evaluated over 270 days of real-world drift, Aion outperforms the best existing adaptive method by up to 10.92 percentage points in F1-score and achieves effective one-shot adaptation under streaming constraints.

## ACKNOWLEDGMENTS

This work is supported by the National Natural Science Foundation of China (No. 62402523, No. U23A20305, No. 62172435), Innovation Scientists and Technicians Troop Construction Projects of Henan Province(No. 254000510007), National Key R&D Program of China (No. 2022YFB3102900), Key Research and Development Project of Henan Province (No. 252102211087).

## REFERENCES

[1] C. Wang, J. Luo, Z. Ling et al., “A comprehensive and long-term evaluation of Tor v3 onion services,” in IEEE Conference on Computer Communications (INFOCOM), 2023, pp. 1–10.

[2] D. Herrmann, R. Wendolsky, and H. Federrath, “Website fingerprinting: Attacking popular privacy enhancing technologies with the multinomial Na¨ıve-bayes classifier,” in ACM Workshop on Cloud Computing Security (CCSW), 2009, pp. 31–42.

[3] T. Li, K. Liu, and S. Du, “A survey on network flow watermarking: A problem-oriented perspective,” Computers & Security, vol. 119, p. 104813, 2025.

[4] J. Huang, W. Liu, G. Liu, B. Gao, and F. Nie, “QuicCourier: Leveraging the dynamics of QUIC-based website browsing behaviors through proxy for covert communication,” IEEE Transactions on Dependable and Secure Computing, vol. 22, no. 5, pp. 4516–4533, 2025.

[5] A. Shusterman, Z. Avraham, E. Croitoru, Y. Haskal, L. Kang, D. Levi, Y. Meltser, P. Mittal, Y. Oren, and Y. Yarom, “Website fingerprinting through the cache occupancy channel and its real world practicality,” IEEE Transactions on Dependable and Secure Computing, vol. 18, no. 5, pp. 2042–2060, 2021.

[6] Z. Yi, T. Li, M. Zhang, X. Yuan, S. Du, and X. Luo, “An efficient website fingerprinting for new websites emerging based on incremental learning,” IEEE Trans. Netw. Service Manag., vol. 23, pp. 365–381, 2025.

[7] P. Sirinam, M. Imani, M. Juarez, and R. Wright, “Deep fingerprinting: Undermining website fingerprinting defenses with deep learning,” in ACM SIGSAC Conference on Computer and Communications Security (CCS), 2018, pp. 1928–1943.

[8] M. S. Rahman, P. Sirinam, N. Mathews et al., “Tik-tok: The utility of packet timing in website fingerprinting attacks,” in Proceedings on Privacy Enhancing Technologies (PoPETs), vol. 2020, no. 3, 2020, pp. 5–24.

[9] S. Bhat, D. Lu, A. Kwon, and S. Devadas, “Var-CNN: A data-efficient website fingerprinting attack based on deep learning,” in Proceedings on Privacy Enhancing Technologies (PoPETs), vol. 2019, no. 4, 2019, pp. 292–310.

[10] M. Shen, K. Ji, Z. Gao et al., “Subverting website fingerprinting defenses with robust traffic representation,” in USENIX Security Symposium (USENIX Security), 2023, pp. 607–624.

[11] X. Deng, Y. Zhang, L. Qi et al., “Enhancing website fingerprinting attacks against traffic drift,” in Network and Distributed System Security Symposium (NDSS), 2026, pp. 1–18.

[12] V. Rimmer, D. Preuveneers, M. Juarez et al., “Automated website fingerprinting through deep learning,” in Network and Distributed System Security Symposium (NDSS), 2018, pp. 1–16.

[13] A. Shusterman, R. David, and Y. Oren, “Understanding and addressing concept drift in website fingerprinting,” Computer Networks, vol. 275, p. 111811, 2026.

[14] Z. Jin, T. Lu, S. Luo et al., “Transformer-based model for multi-tab website fingerprinting attack,” in ACM SIGSAC Conference on Computer and Communications Security (CCS), 2023, pp. 1050–1064.

[15] X. Deng, Q. Yin, Z. Liu et al., “Robust multi-tab website fingerprinting attacks in the wild,” in IEEE Symposium on Security and Privacy (SP), 2023, pp. 1005–1022.

[16] A. Bahramali, A. Bozorgi, and A. Houmansadr, “Realistic website fingerprinting by augmenting network traces,” in ACM SIGSAC Conference on Computer and Communications Security (CCS), 2023, pp. 1035– 1049.

[17] P. Sirinam, N. Mathews, M. S. Rahman, and R. Wright, “Triplet fingerprinting: More practical and portable website fingerprinting with n-shot learning,” in ACM SIGSAC Conference on Computer and Communications Security (CCS), 2019, pp. 1131–1148.

[18] C. Luo, W. Tang, Q. Wang, and D. Zheng, “Few-shot website fingerprinting with distribution calibration,” IEEE Transactions on Dependable and Secure Computing, vol. 22, no. 1, pp. 632–648, 2025.

[19] G. Cherubin, R. Jansen, and C. Troncoso, “Online website fingerprinting: Evaluating website fingerprinting attacks on Tor in the real world,” in USENIX Security Symposium (USENIX Security), 2022, pp. 753–770.

[20] S. Thirumuruganathan, F. Deniz, I. Khalil, T. Yu, M. Nabeel, and M. Ouzzani, “Detecting and mitigating sampling bias in cybersecurity with unlabeled data,” in USENIX Security Symposium (USENIX Security), 2024, pp. 1741–1758.

[21] H. J. Scudder, “Probability of error of some adaptive pattern-recognition machines,” IEEE Trans. Inf. Theory, vol. 11, no. 3, pp. 363–371, 1965.

[22] Z.-H. Zhou, “A brief introduction to weakly supervised learning,” National Science Review, vol. 5, no. 1, pp. 44–53, 2018.

[23] J. Liang, D. Hu, and J. Feng, “Do we really need to access the source data? source hypothesis transfer for unsupervised domain adaptation,” in Int. Conf. Machine Learning (ICML), 2020, pp. 6028–6039.

[24] C. Sheng, W. Zhou, Q.-L. Han, W. Ma, X. Zhu, S. Wen, and Y. Xiang, “Network traffic fingerprinting for iiot device identification: A survey,”

IEEE Transactions on Industrial Informatics, vol. 21, no. 5, pp. 3541– 3554, 2025.

[25] J. Hayes and G. Danezis, “k-fingerprinting: A robust scalable website fingerprinting technique,” in USENIX Security Symposium (USENIX Security), 2016, pp. 1187–1203.

[26] A. Panchenko, F. Lanze, J. Pennekamp et al., “Website fingerprinting at internet scale,” in Network and Distributed System Security Symposium (NDSS), 2016, pp. 1–15.

[27] X. Deng, Q. Li, K. Xu et al., “Robust and reliable early-stage website fingerprinting attacks via spatial-temporal distribution analysis,” in ACM SIGSAC Conference on Computer and Communications Security (CCS), 2024, pp. 1997–2011.

[28] M. Juarez, M. Imani, M. Perry, C. Diaz, and M. Wright, “Toward an efficient website fingerprinting defense,” in European Symposium on Research in Computer Security (ESORICS), 2016, pp. 27–46.

[29] R. Nithyanand, X. Cai, and R. Johnson, “Glove: A bespoke website fingerprinting defense,” in ACM Workshop on Privacy in the Electronic Society (WPES), 2014, pp. 131–134.

[30] K. Alnaami, N. Xi, and E. Bertino, “Bimorphing: A bi-directional bursting defense against website fingerprinting attacks,” IEEE Transactions on Dependable and Secure Computing, vol. 18, no. 6, pp. 2731–2745, 2021.

[31] K. Saito, Y. Ushiku, T. Harada, and K. Saenko, “Maximum classifier discrepancy for unsupervised domain adaptation,” in IEEE Conf. Computer Vision and Pattern Recognition (CVPR), 2018, pp. 3723–3732.

[32] L. Fan, Q. Xu, W. Ding, X. Chen, S. Xu, and P. Li, “Autoiot: Automatically updated iot device identification with semi-supervised learning,” IEEE Transactions on Mobile Computing, vol. 22, no. 10, pp. 5769–5786, 2023.

[33] C. Sheng, Y. Yao, W. Li, W. Yang, and Y. Liu, “Unknown attack traffic classification in scada network using heuristic clustering technique,” IEEE Transactions on Network and Service Management, vol. 20, no. 3, pp. 2625–2638, 2023.

[34] B. Li, Y. Wu, J. Song, R. Lu, T. Li, and L. Zhao, “Deepfed: Federated deep learning for intrusion detection in industrial cyber–physical systems,” IEEE Transactions on Industrial Informatics, vol. 17, no. 8, pp. 5615–5624, 2021.

[35] P. K. Danso, S. Dadkhah, H. Mahdikhani, A. Zohourian, and A. A. Ghorbani, “Transferability of machine learning algorithm for iot device profiling and identification,” IEEE Internet of Things Journal, vol. 11, no. 2, pp. 2322–2335, 2024.

[36] C. Sheng, Y. Yao, L. Zhao, P. Zeng, and J. Zhao, “Scanner-hunter: An effective ics scanning group identification system,” IEEE Transactions on Information Forensics and Security, vol. 19, pp. 3077–3092, 2024.

[37] G. Zhang, J. Cao, M. Xu, and X. Deng, “Unsupervised and adaptive tor website fingerprinting,” in International Conference on Security and Privacy in Communication Systems. Springer, 2023, pp. 209–229.

[38] S. Ben-David, J. Blitzer, K. Crammer, A. Kulesza, F. Pereira, and J. W. Vaughan, “A theory of learning from different domains,” Machine Learning, vol. 79, no. 1–2, pp. 151–175, 2010.

[39] Z. Guan, G. Xiong, G. Gou et al., “BAPM: Block attention profiling model for multi-tab website fingerprinting attacks on Tor,” in Annual Computer Security Applications Conference (ACSAC), 2021, pp. 248– 259.

[40] X. Deng, Q. Li, and K. Xu, “Website fingerprinting library (wflib),” https://github.com/XinhaoDeng/Website-Fingerprinting-Library, 2024, online; accessed 2025.

[41] The Tor Project, “Circuit-level Padding,” 2023. [Online]. Available: https://spec.torproject.org/padding-spec/circuitlevel-padding.html

![](images/5522048dd8934982c64b2c0e58dba7d046bb3253e0ed3bcb6a1470213c82402a.jpg)

Zhengge Yi received B.S. and M.S. degrees in information security in 2020 and 2022 respectively from Engineering University of PAP, Xi’an, China. He is currently pursuing a Doctorate degree in Henan Key Laboratory of Cyberspace Situation Awareness, Zhengzhou, Henan, China. His current research interests include anonymous communication security and traffic analysis.

![](images/fe2e82d835b0a197258d12500a896d96d809728a1a0e0926df83aeec8cf3c5c9.jpg)

Tengyao Li received B.S. and M.S. degrees in computer science and technology in 2014 and 2016 respectively, Ph.D. degree in cyberspace security in 2020 from Air Force Engineering University, Xi’an, Shaanxi, China. He is now a lecturer at the Henan Key Laboratory of Cyberspace Situation Awareness, Zhengzhou, Henan, China. His current research has focused on active defense against uncertain attacks in large scale network systems.

![](images/1c47374622fe184086c4c4c7e0aa75786552371f21e2d599085631327b6fb284.jpg)

Jingxi Zhang received B.S. degree in cyberspace security in 2024 from Information Engineering University, Zhengzhou, Henan, China. She is currently pursuing a doctoral degree at Henan Key Laboratory of Cyberspace Situation Awareness, Zhengzhou, Henan, China. Her current research focuses on anonymous network security and anonymous traffic analysis.

![](images/c72760a8213ec45fce41021e21283d83c5b81601118c5414ea604fc99c0e65d9.jpg)

Yifei Meng received B.S. and M.S. degrees in information security in 2022 and 2024 respectively from Engineering University of PAP, Xi’an, China. He is currently pursuing a Ph.D. degree in Henan Key Laboratory of Cyberspace Situation Awareness, Zhengzhou, Henan, China. His current research interests include dark web anonymity analysis, deanonymization techniques.

![](images/9f1a15e678fa204948a7cc22e562d47afec2d05fb0b7cc7f758e731e8dc94a96.jpg)

Xiangyang Luo received his B.S., M.S., and Ph.D. degrees from the Henan Key Laboratory of Cyberspace Situation Awareness, Zhengzhou, Henan, China, in 2001, 2004, and 2010, respectively. He is the author or co-author of more than 150 refereed international journal and conference manuscripts. He is currently a professor of the Henan Key Laboratory of Cyberspace Situation Awareness. His research interests are image steganography and steganalysis technique.